# -*- coding: utf-8 -*-
"""Document terminal here.

Copyright (C) 2021, Auto Trader UK
Created 13. Jan 2021 20:44

"""
from typing import List

import click

from olivertwist.ruleengine.result import Result


def get_colour(result: Result):
    colour = "green"
    if result.has_errors:
        colour = "red"
    if result.has_warnings:
        colour = "yellow"
    return colour


def report_to_terminal(results: List[Result]):
    for result in results:
        colour = get_colour(result)
        name = click.style(f"{result.rule.name}:", fg=colour)
        link = click.style(
            f"https://github.com/autotraderuk/oliver-twist/blob/main/RULES.md#{result.rule.id}",
            fg="blue",
        )
        click.echo(f"{name} [{link}]:")
        for node in result.failures:
            click.secho(f" - {node.id}", fg=colour)

        click.echo()
