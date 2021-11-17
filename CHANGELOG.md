# Changelog

## [Unreleased]

### Added

- :sparkles: The ``kedro serving serve`` command enable tos erve a pipeline as a FastAPI application
- :sparkles: :zap: The artifacts (i.e. any inputs of the pipeline different from the body) are loaded as `MemoryDataSet(copy_mode=assign)` to reduce I/O operations and increase speed
- :sparkles: The input schema is automatically inferred from the input DataFrame
