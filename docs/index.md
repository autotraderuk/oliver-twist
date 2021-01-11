---
title: Homepage
description: A dbt dag auditing tool
---
# Oliver Twist

DAG Auditor

oliver-twist is a dag auditing tool that audits the [DBT](https://www.getdbt.com/) DAG and generates a summary report.

## Getting Started

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

[All rules](./rules.md) are enabled by default. To change this you need a configuration file called `olivertwist.yml` in the same directory you are running `olivertwist`. An example configuration is shown below:

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
