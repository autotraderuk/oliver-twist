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

You can also tell Oliver to load and run your own custom rules using the `--add-rules-from` option:

```shell
olivertwist check --add-rules-from=./custom_rules_dir/ manifest.json
```

In order to be discovered and run, rules must be instances of `olivertwist.ruleengine.rule.Rule`. This can be achieved by instantiating an instance of the class directly, or by applying the `@rule` decorator to a plain function with the signature `(manifest: Manifest) -> (passes: List[Node], failures: List[Node])` e.g.:

```python
from olivertwist.ruleengine.rule import rule

@rule(id="my-pointless-rule", name="Everything is allowed!")
def pass_everything(manifest: Manifest) -> Tuple[List[Node], List[Node]]:
    return list(manifest.nodes()), []

```

Full options are available with:

```shell
olivertwist check --help
```

## Configuration

[All rules](./rules.md) are enabled by default. To change this you need a configuration file called `olivertwist.yml` in the same directory you are running `olivertwist`. An example configuration is shown below:

```yaml
version: '1.0'
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
