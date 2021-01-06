# Oliver Twist

DAG Auditor

oliver-twist is a dag auditing tool that audits the [DBT](https://www.getdbt.com/) DAG and generates a summary report.

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
