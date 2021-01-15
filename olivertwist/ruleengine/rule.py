# -*- coding: utf-8 -*-
"""Definition of the Rule class.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 14:31

"""
from typing import Callable, List, Tuple

from olivertwist.config.model import Severity
from olivertwist.manifest import Manifest, Node


class Rule:
    def __init__(
        self,
        id: str,
        name: str,
        func: Callable[[Manifest], Tuple[List[Node], List[Node]]],
    ):
        self.id = id
        self.name = name
        self.func = func
        self._severity = Severity.ERROR

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def apply(self, manifest) -> Tuple[List[Node], List[Node]]:
        return self.func(manifest)

    @property
    def severity(self):
        return self._severity

    @severity.setter
    def severity(self, severity: Severity):
        if not isinstance(severity, Severity):
            raise TypeError("severity must be an instance of Severity enum.")
        self._severity = severity


def rule(id, name):
    def class_constructor(func):
        nonlocal id, name
        if not name:
            name = func.__name__.replace("_", " ")

        return Rule(id, name, func)

    return class_constructor
