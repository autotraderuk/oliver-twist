# -*- coding: utf-8 -*-
"""Main entry point for olivertwist.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 15:32

"""
import json
import logging
import os
import webbrowser
from pathlib import Path
from typing import List

import click

from olivertwist.config.configurator import Configurator
from olivertwist.config.io import ConfigIO
from olivertwist.config.model import Config
from olivertwist.manifest import Manifest
from olivertwist.metricengine.engine import MetricEngine
from olivertwist.reporter.adapter import to_report
from olivertwist.reporter.model import MyEncoder
from olivertwist.reporter.reporter import output_json, render_html_report
from olivertwist.reporter.terminal import report_to_terminal
from olivertwist.ruleengine.engine import RuleEngine
from olivertwist.ruleengine.result import Result

logger = logging.getLogger("olivertwist")


@click.group()
@click.option("--debug/--no-debug", default=False)
def main(debug):
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode on!")


@main.command()
@click.option(
    "--config",
    "config_path",
    type=click.Path(dir_okay=False),
    help="The path to the configuration file to create / edit",
)
def config(config_path):
    """Interactively create or edit configuration file"""
    config_path = Path(config_path or ConfigIO.DEFAULT_CONFIG_FILE_PATH)
    logging.debug(config_path)
    try:
        config_obj = ConfigIO.read(config_path)
    except FileNotFoundError:
        config_obj = Config.empty()

    config_obj = Configurator.update(config_obj)
    ConfigIO.write(config_obj, config_path)
    click.echo(f"Created/updated config in {config_path}")


@main.command()
@click.argument("input", type=click.File("r"))
@click.option(
    "--config", type=click.Path(exists=True), help="The path to the configuration file"
)
@click.option(
    "add_rules_paths",
    "--add-rules-from",
    multiple=True,
    type=click.Path(exists=True, readable=True, dir_okay=True, file_okay=False),
    help="Add custom rules from a directory (repeatable for multiple locations)",
)
@click.option("--html/--no-html", default=True, help="Do/Don't output report in HTML")
@click.option(
    "--browser/--no-browser",
    default=False,
    help="Do/Don't open HTML report in browser. Implies --html",
)
def check(input, config, add_rules_paths, html=True, browser=False):
    """Check dbt DAG against configured rules."""
    config = ConfigIO.read(config)
    manifest = Manifest(json.load(input))
    rule_engine = RuleEngine.with_configured_rules(config)
    for rule_path in add_rules_paths:
        rule_engine.extend(RuleEngine.with_configured_rules(config, rule_path))

    results = rule_engine.run(manifest)
    report_to_terminal(results)
    metric_results = MetricEngine().run(manifest)
    report = to_report(results, metric_results)
    oliver_twist = json.loads(MyEncoder().encode(report))
    output_json(oliver_twist)
    if html or browser:
        logger.debug("Generating HTML report...")
        render_html_report(oliver_twist)
        if browser:
            webbrowser.open(f"file://{os.getcwd()}/target/index.html")

    exit_message(results)


def exit_message(results: List[Result]):
    if any([result.has_errors for result in results]):
        click.get_current_context().exit("🔀 Twisted!")
    else:
        click.echo("🟢 Oliver (all of your) models look good!")


if __name__ == "__main__":
    main()
