from logging import getLogger
from pathlib import Path
from typing import List, NamedTuple, Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from kedro.io import DataCatalog, MemoryDataSet
from kedro.runner import SequentialRunner
from pydantic import create_model_from_namedtuple

LOGGER = getLogger(__name__)


def _convert_np_to_fastapi_types(x: np.dtype):
    # TODO: make a better conversion, see
    # https://pbpython.com/pandas_dtypes.html and
    # https://stackoverflow.com/questions/47423930/how-to-convert-pandas-dataframe-columns-to-native-python-data-types

    mapping_np_typing = {
        "object": "str",
        "bool": "bool",
        "bool_": "bool",
        "int_": "int",
        "int8": "int",
        "int16": "int",
        "int32": "int",
        "int64": "int",
        "uint8": "int",
        "uint16": "int",
        "uint32": "int",
        "uint64": "int",
        "float_": "float",
        "float16": "float",
        "float32": "float",
        "float64": "float",
        "datetime64": "datetime.datetime",
        "datetime64[ns]": "datetime.datetime",
    }
    return mapping_np_typing.get(x.name, "str")


def create_pipeline_input_base_model(data: pd.DataFrame):
    """This functions creates a pydantic model
    out of an example dataset
    """
    typed_columns = [
        (k, _convert_np_to_fastapi_types(v)) for k, v in data.dtypes.iteritems()
    ]
    model_schema = NamedTuple("PipelineInput", typed_columns)

    class PipelineInputConfig:
        extra = "forbid"
        schema_extra = {"example": data.iloc[0:1, :].to_dict(orient="records")[0]}

    PipelineInputModel = create_model_from_namedtuple(
        model_schema, __config__=PipelineInputConfig
    )

    return PipelineInputModel


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
            name: MemoryDataSet(copy_mode="assign") for name in pipeline.inputs()
        }
    )

    kedro_artifacts = pipeline.inputs() - {input_name}
    for artifact_name in kedro_artifacts:
        LOGGER.info(f"Loading '{artifact_name}' in memory...")
        artifact_data = catalog.load(artifact_name)
        memory_catalog.save(artifact_name, artifact_data)

    # get input schema
    input_data = catalog.load(input_name)
    PipelineInput = create_pipeline_input_base_model(input_data)

    # get output schema
    output_name = list(pipeline.outputs())[
        0
    ]  # TODO: add a check on the number and types of outputs

    @kedro_app.get("/health")
    async def health():
        return {"code": 200, "status": "Ok"}

    @kedro_app.post("/run")
    async def run(data: List[PipelineInput]):
        print(data)
        print([record.dict() for record in data])
        # print(
        #     pd.DataFrame.from_records(
        #         [record.dict() for record in data], index=range(len(data))
        #     )
        # )
        data_df = pd.DataFrame.from_records(
            [record.dict() for record in data], index=range(len(data))
        )
        print(data_df)
        memory_catalog.save(input_name, data_df)
        result = runner.run(pipeline, memory_catalog)

        return result[output_name].to_dict(orient="records")

    return kedro_app
