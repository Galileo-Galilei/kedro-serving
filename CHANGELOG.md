# Changelog

## [Unreleased]

## [0.0.1] - 2021-11-17

### Added

-   :sparkles: The `kedro serving serve` command enable tos erve a pipeline as a FastAPI application
-   :sparkles: :zap: The artifacts (i.e. any inputs of the pipeline different from the body) are loaded as `MemoryDataSet(copy_mode=assign)` to reduce I/O operations and increase speed
-   :sparkles: The input schema is automatically inferred from the input DataFrame

[Unreleased]: https://github.com/Galileo-Galilei/kedro-serving/compare/0.0.1...HEAD

[0.0.1]: https://github.com/Galileo-Galilei/kedro-serving/compare/1259ff3638c08e48289bc50b549944fe3f47c93e...0.0.1
