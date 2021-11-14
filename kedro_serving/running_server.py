from pathlib import Path
from fastapi import FastAPI
from typing import Optional, Dict

from kedro.framework.session import KedroSession
from kedro.runner import SequentialRunner
from kedro.io import DataCatalog, MemoryDataSet
from kedro.framework.startup import bootstrap_project


def init_app(
    pipeline: str,
    input_name: str,
    env: Optional[str] = None,
    # extra_params: str = "",
    # copy_mode: Dict[str, str] = None,
):
    pipeline_name = pipeline
    kedro_app = FastAPI()
    # TODO: remove extra_params hardcoding
    bootstrap_project(Path.cwd())
    with KedroSession.create(env=env, extra_params="") as session:
        runner = SequentialRunner()
        context = session.load_context()
        pipeline = context.pipelines[pipeline_name]
        catalog = context.catalog

    # TODO: make copy mode customisable!
    memory_catalog = DataCatalog(
        data_sets={
            name: MemoryDataSet(copy_mode="assign") for name in pipeline.data_sets()
        }
    )

    kedro_artifacts = pipeline.inputs() - {input_name}
    for artifact_name in kedro_artifacts:
        artifact_data = catalog.load(artifact_name)
        memory_catalog.save(artifact_name, artifact_data)

    @kedro_app.get("/health")
    async def health():
        return {"code": 200, "status": "Ok"}

    @kedro_app.post("/run")
    async def run(data):
        memory_catalog.save(input_name, data)
        result = runner.run(pipeline, memory_catalog)
        return result

    return kedro_app
