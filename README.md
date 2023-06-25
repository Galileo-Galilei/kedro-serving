**General informations**

[![Python Version](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue.svg)](https://pypi.org/project/kedro-serving/) [![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Code Style: Black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/ambv/black)
[![SemVer](https://img.shields.io/badge/semver-2.0.0-green)](https://semver.org/)

----------------------------------------------------------
| Software repository | Latest release                                                                                         | Total downloads                                                                                |
| ------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| Pypi                | [![PyPI version](https://badge.fury.io/py/kedro-serving.svg)](https://pypi.org/project/kedro-serving/) | [![Downloads](https://pepy.tech/badge/kedro-serving)](https://pepy.tech/project/kedro-serving) |

**Code health**

----------------------------------------------------------
| Branch | Tests                                                                                                                                                                                          | Coverage                                                                                                                                                       | Links                                                                                                                                                                                                         | Documentation                                                                                                                             | Deployment                                                                                                                                                                                              | Activity                                                                                                                                                            |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `main` | [![test](https://github.com/Galileo-Galilei/kedro-serving/workflows/test/badge.svg?branch=main)](https://github.com/Galileo-Galilei/kedro-serving/actions?query=workflow%3Atest+branch%3Amain) | [![codecov](https://codecov.io/gh/Galileo-Galilei/kedro-serving/branch/main/graph/badge.svg)](https://codecov.io/gh/Galileo-Galilei/kedro-serving/branch/main) | [![links](https://github.com/Galileo-Galilei/kedro-serving/workflows/check-links/badge.svg?branch=main)](https://github.com/Galileo-Galilei/kedro-serving/actions?query=workflow%3Acheck-links+branch%3Amain) | [![Documentation](https://readthedocs.org/projects/kedro-serving/badge/?version=stable)](https://kedro-serving.readthedocs.io/en/stable/) | [![publish](https://github.com/Galileo-Galilei/kedro-serving/workflows/publish/badge.svg?branch=main)](https://github.com/Galileo-Galilei/kedro-serving/actions?query=branch%3Amain+workflow%3Apublish) | [![commit](https://img.shields.io/github/commits-since/Galileo-Galilei/kedro-serving/0.0.1)](https://github.com/Galileo-Galilei/kedro-serving/compare/0.0.1...main) |

# What is kedro-serving?

`kedro-serving` is a kedro-plugn for serving kedro pipelines. It aims to be easy to use, flexible, robust to be production ready. **As it is in its early stage of developpement, it is highly discouraged to use it for production in its current state.**  

Coming soon:
- enable parameters injection at runtime
- supporting other inputs than pandas dataframe
- documentation & examples
- support for production-ready ASGI server (e.g., gunicorn)
- extended configuration for artifacts
- tests

# How do I install kedro-serving?


``kedro-serving`` is available on PyPI, so you can install it with ``pip``:

```console
pip install kedro-serving
```

If you want to use the most up to date version of the package which is under development and not released yet, you can install the package from github:

```console
pip install --upgrade git+https://github.com/Galileo-Galilei/kedro-serving.git
```


# Getting started

- Run `kedro info` to check if kedro recognizes kedro-serving as a plugin.
- Change directory into your kedro project.
- `kedro serving serve --pipeline my_pipeline_name --input-name my-input-name`
  - For example, using the [spaceflight starter](https://docs.kedro.org/en/stable/tutorial/tutorial_template.html) project, I could run kedro-serving with this command: `kedro serving serve --pipeline data_processing --input-name companies`
  - This sets up a server at http://localhost:5000 with two endpoints, `health` and `run`
- Go to [http://localhost:5000/health](http://localhost:5000/health) to verify the server is running.
- Use postman or similar to POST to [http://localhost:5000/run](http://localhost:5000/run) with a body containing a JSON list of records, like this example that works for the spaceflights starter:
  - `[{"id": 1, "company_rating": 3, "company_location": "TX", "total_fleet_count": 23, "iata_approved": "n"}]`
  - These records replace the input-name called out in the kedro-serving command when running the pipeline called out in the kedro-serving command.
- If the records you pass in do not match the schema of the input-name you selected when initiating kedro-server, you will receive an error in JSON form.
- If the pipeline run is successful, you will receive a response in JSON form containing the output data from the pipeline.

# Release and roadmap

The [release history](https://github.com/Galileo-Galilei/kedro-serving/blob/main/CHANGELOG.md) centralizes packages improvements across time. The main features coming in next releases are [listed on github milestones](https://github.com/Galileo-Galilei/kedro-serving/milestones). Feel free to upvote/downvote and discuss prioritization in associated issues.

# Disclaimer

This package is still in active development. We use [SemVer](https://semver.org/) principles to version our releases. Until we reach `1.0.0` milestone, breaking changes will lead to `<minor>` version number increment, while releases which do not introduce breaking changes in the API will lead to `<patch>` version number increment.

If you want to see how to migrate from one version of `kedro-serving` to another, see the [migration guide](../docs/migration_guide.md).

# Can I contribute?

We'd be happy to receive help to maintain and improve the package. Any PR will be considered (from typo in the docs to core features add-on) Please check the [contributing guidelines](https://github.com/Galileo-Galilei/kedro-serving/blob/main/CONTRIBUTING.md).

# Main contributors

The following people actively maintain, enhance and discuss design to make this package as good as possible:

- [Yolan Honoré-Rougé](https://github.com/Galileo-Galilei)
