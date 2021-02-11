# -*- coding: utf-8 -*-
"""Document terminal here.

Copyright (C) 2021, Auto Trader UK
Created 13. Jan 2021 20:44

"""
from typing import List

import click

from olivertwist.ruleengine.result import Result


def get_colour(result: Result):
    if result.has_errors:
        return "red"
    elif result.has_warnings:
        return "yellow"
    return "green"


def report_to_terminal(results: List[Result]):
    for result in results:
        colour = get_colour(result)
        name = click.style(f"{result.rule.name}:", fg=colour)
        link = click.style(
            f"https://olivertwi.st/rules/#{result.rule.id}",
            fg="blue",
        )
        click.echo(f"{name} [{link}]:")
        for node in result.failures:
            click.secho(f" - {node.id}", fg=colour)

        click.echo()
