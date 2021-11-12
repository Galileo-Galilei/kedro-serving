from fastapi import FastAPI
from typing import Optional, Dict

from kedro.framework.session import KedroSession
from kedro.runner import SequentialRunner
from kedro.io import DataCatalog, MemoryDataSet


def init_app(
    pipeline: str,
    input_name: str,
    env: Optional[str] = None,
    # extra_params: str = "",
    # copy_mode: Dict[str, str] = None,
):

    kedro_app = FastAPI()
    # TODO: remove extra_params hardcoding
    with KedroSession.create(env=env, extra_params="") as session:
        runner = SequentialRunner()
        context = session.load_context()
        pipeline = context.pipelines["pipeline"]
        catalog = context.catalog

    # TODO: make copy mode customisable!
    memory_catalog = DataCatalog(
        data_sets={
            name: MemoryDataSet(copy_mode="assign") for name in pipeline.data_sets()
        }
    )

    kedro_artifacts = pipeline.inputs() - {input_name}
    for artifact in kedro_artifacts:
        memory_catalog.load(artifact)

    @kedro_app.get("/")
    async def health():
        return {"code": 200, "status": "Ok"}

    @kedro_app.post("/")
    async def run(data):
        memory_catalog.save(data)
        result = runner.run(memory_catalog, pipeline)
        return result

    return kedro_app
