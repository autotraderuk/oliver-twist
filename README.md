

![Alt text](./images/oliver_twist_logo.png)
# oliver-twist

DAG Auditor

![Build status badge](https://github.com/autotraderuk/oliver-twist/workflows/CI/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

oliver-twist is a dag auditing tool that audits the [DBT](https://www.getdbt.com/) DAG and generates a summary report. The rules implemented can be found [here](RULES.md)

![please sir, can I automate my DAG auditing](./images/oliver_dag_meme.jpg)

# Getting Started

To get started, install the package

```shell
$ pip install olivertwist
```

and then run it by passing it your dbt manifest JSON

```shell
olivertwist manifest.json
```

This will report any failures to the console, and also in HTML format in a directory called `target`. You can optionally auto-open the report in a browser with:

```shell
olivertwist manifest.json --browser
```

Full options are available with:


```shell
olivertwist manifest.json --help
```

## Developer

### To dev locally

Clone this repo and install all the projects packages:

`poetry install`

To get the latest versions of the dependencies and to update the poetry.lock file run:

`poetry update`

To run oliver-twist and generate the summary report run:

`poetry run olivertwist example_manifest.json`


### Creating a distribution

```poetry build --format wheel```
