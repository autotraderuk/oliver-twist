

![Alt text](http://olivertwi.st/images/oliver_twist_logo.png)
# oliver-twist

DAG Auditor

![Build status badge](https://github.com/autotraderuk/oliver-twist/workflows/CI/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

oliver-twist is a dag auditing tool that audits the [DBT](https://www.getdbt.com/) DAG and generates a summary report. There is a [docs site][1], including descriptions of all [currently implemented rules][2].

![please sir, can I automate my DAG auditing](http://olivertwi.st/images/oliver_dag_meme.jpg)

# Getting Started

To get started, install the package

```shell
$ pip install olivertwist
```

and then run it by passing it your dbt manifest JSON

```shell
olivertwist check manifest.json
```

This will report any failures to the console, and also in HTML format in a directory called `target`. You can optionally auto-open the report in a browser with:

```shell
olivertwist check manifest.json --browser
```

Full options are available with:


```shell
olivertwist check --help
```

## Configuration

[All rules][2] are enabled by default. To change this you need a configuration file called `olivertwist.yml` in the same directory you are running `olivertwist`. An example configuration is shown below:

```yaml
universal:
  - id: no-rejoin-models
    enabled: false
  - id: no-disabled-models
    enabled: true
```

There is a command to help you generate the config automatically:

```shell
olivertwist config
```

This will show all the available rules and allow you to toggle the ones that you want to enforce.

## Local Development

### Clone this repo and install the project:

`poetry install`

### Install pre-commit hooks for linting

This is optional, but highly recommended to avoid annoying linting failure in CI.

`poetry run pre-commit install`

To run the pre-commit hooks locally:

`poetry run pre-commit run`

### To get the latest versions of the dependencies and to update the poetry.lock file run:

`poetry update`

### To run oliver-twist and generate the summary report run:

`poetry run olivertwist example_manifest.json`

### Working with diagrams
 
To update and regenerate the images that illustrate rule failures in the documentation follow the next steps:
- update the diagrams using the [mermaid syntax](https://mermaid-js.github.io/mermaid/#/)
- install [yarn](https://classic.yarnpkg.com/en/docs/install/)
- `cd docs/diagrams`
- `./generate.sh`
- inspect the generated images in `./docs/diagrams/output/`
- if you're happy with the results, run `./copy.sh` so that they are copied over to `./docs/images`
- you can now reference those images. e.g. in `.docs/rules.md`

### Creating a distribution

```poetry build --format wheel```


[1]: http://olivertwi.st/
[2]: http://olivertwi.st/rules/
