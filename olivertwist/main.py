# -*- coding: utf-8 -*-
"""Main entry point for olivertwist.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 15:32

"""
import json
import logging
from typing import List

import click

from olivertwist.manifest import Manifest
from olivertwist.metricengine.engine import MetricEngine
from olivertwist.reporter.adapter import to_html_report
from olivertwist.reporter.model import MyEncoder
from olivertwist.reporter.reporter import output_json, render_html_report
from olivertwist.ruleengine.engine import RuleEngine
from olivertwist.ruleengine.result import Result

logger = logging.getLogger("olivertwist")


@click.command()
@click.argument("input", type=click.File("r"))
@click.option("--html/--no-html", default=True, help="Do/Don't output report in HTML")
def main(input, html=True, browser=False):
    manifest = Manifest(json.load(input))
    rule_engine = RuleEngine.with_default_rules()
    results = rule_engine.run(manifest)
    format_for_terminal(results)
    metric_results = MetricEngine().run(manifest)
    report = to_html_report(results, metric_results)
    oliver_twist = json.loads(MyEncoder().encode(report))
    output_json(oliver_twist)
    if html or browser:
        logger.debug("Generating HTML report...")
        render_html_report(oliver_twist)

    exit_message(results)


def format_for_terminal(results: List[Result]):
    for result in results:
        colour = "red" if result.has_failures else "green"
        click.secho(f"{result.rule.name}:", fg=colour)
        for node in result.failures:
            click.secho(f" - {node.id}", fg="red")

        click.echo()


def exit_message(results: List[Result]):
    if any([result.has_failures for result in results]):
        click.get_current_context().exit("🔀 Twisted!")
    else:
        click.echo("🟢 Oliver (all of your) models look good!")


if __name__ == "__main__":
    main()
