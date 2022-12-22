import pathlib

from setuptools import find_packages, setup

NAME = "kedro_serving"
HERE = pathlib.Path(__file__).parent


def _parse_requirements(path, encoding="utf-8"):
    with open(path, mode="r", encoding=encoding) as file_handler:
        requirements = [
            x.strip() for x in file_handler if x.strip() and not x.startswith("-r")
        ]
    return requirements


# get the dependencies and installs
base_requirements = _parse_requirements("requirements.txt")


# Get the long description from the README file
with open((HERE / "README.md").as_posix(), encoding="utf-8") as file_handler:
    README = file_handler.read()


setup(
    name=NAME,
    version="0.0.1",  # this will be bumped automatically by bump2version
    description="A kedro plugin to serve kedro pipelines",
    license="Apache Software License (Apache 2.0)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Galileo-Galilei/kedro-serving",
    python_requires=">=3.6, <3.9",
    packages=find_packages(exclude=["docs*", "tests*"]),
    setup_requires=["setuptools_scm"],
    include_package_data=True,
    install_requires=base_requirements,
    extras_require={
        "doc": [
            "sphinx==4.1.1",
            "recommonmark==0.7.1",
            "sphinx_rtd_theme==0.5.2",
            "sphinx-markdown-tables==0.0.15",
            "pandas>=1.0.0, <2.0.0",  # avoid to make readthedocs load rc version
            "numpy>=1.0.0, <2.0.0",  # bug on windows for numpy 1.19.0->1.19.4
        ],
        "test": [
            "pytest>=5.4.0, <7.0.0",
            "pytest-cov>=2.8.0, <3.0.0",
            "pytest-lazy-fixture>=0.6.0, <1.0.0",
            "pytest-mock>=3.1.0, <4.0.0",
            "scikit-learn>=0.23.0, <0.25.0",
            "flake8==4.0.1",  # ensure consistency with pre-commit
        ],
        "dev": [
            "black==21.10b0",  # pin black version because it is not compatible with a pip range (because of non semver version number)
            "isort==5.11.4",  # ensure consistency with pre-commit
            "pre-commit>=2.0.0,<3.0.0",
            "jupyter>=1.0.0,<2.0.0",
        ],
    },
    author="Yolan Honoré-Rougé",
    entry_points={
        "kedro.project_commands": ["kedro_serving =  kedro_serving.cli:commands"],
    },
    zip_safe=False,
    keywords="",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
