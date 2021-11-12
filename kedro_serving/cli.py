import click
from kedro_serving.running_server import init_app
import uvicorn


@click.group(name="Serving")
def commands():
    """Kedro plugin for interactions with mlflow."""
    pass  # pragma: no cover


@commands.command(name="serving")
def serving_commands():
    """Use mlflow-specific commands inside kedro project."""
    pass  # pragma: no cover


@serving_commands.command
@click.option(
    "--pipeline",
    help="The name of the kedro pipeline to serve. Default to '__default__'",
)
@click.option(
    "--input-name",
    "-i",
    help="The name of the kedro DataSet which contains the input data. Default to 'local'",
)
@click.option(
    "--env",
    "-e",
    default="local",
    help="The name of the kedro environment where the 'mlflow.yml' should be created. Default to 'local'",
)
def serve(
    pipeline,
    input_name,
    env,
    port,
    host,  # extra_params,
):
    app = init_app(
        pipeline,
        input_name,
        env,
        # extra_params,
    )

    # TODO: remove hardcoded config
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
