

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

## Configuration

Create a configuration file called `oliver_twist.yml` in the same directory you are running `olivertwist`. An example configuration is shown below:

```yaml
universal:
    - id: no-rejoin-models
      enabled: false
    - id: no-disabled-models
      enabled: true
```

All rules are enabled by default

## Local Development

##### Clone this repo and install all the projects packages:

`poetry install`

##### To get the latest versions of the dependencies and to update the poetry.lock file run:

`poetry update`

##### To run oliver-twist and generate the summary report run:

`poetry run olivertwist example_manifest.json`

##### Working with diagrams 
To update and regenerate the images that illustrate rule failures in the documentation follow the next steps:
- update the diagrams using the [mermaid syntax](https://mermaid-js.github.io/mermaid/#/)
- install [yarn](https://classic.yarnpkg.com/en/docs/install/)
- `cd diagrams`
- `./generate.sh`
- inspect the generated images in `/diagrams/output/`
- if you're happy with the results, run `./copy.sh` so that they are copied over to `images`
- you can now reference those images. ie. in RULES.md

##### Creating a distribution

```poetry build --format wheel```
