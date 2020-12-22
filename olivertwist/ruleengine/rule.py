# -*- coding: utf-8 -*-
"""Definition of the Rule class.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 14:31

"""
from typing import Callable, List, Tuple

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

    def __call__(self, *args, **kwargs):
        return self.apply(*args, **kwargs)

    def apply(self, manifest) -> Tuple[List[Node], List[Node]]:
        return self.func(manifest)


def rule(id, name):
    def class_constructor(func):
        nonlocal id, name
        if not name:
            name = func.__name__.replace("_", " ")

        return Rule(id, name, func)

    return class_constructor
