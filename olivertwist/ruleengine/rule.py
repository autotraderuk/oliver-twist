# -*- coding: utf-8 -*-
"""Document rule here.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 14:31

"""
from typing import Callable, List, Tuple

from olivertwist.manifest import Manifest, Node


class Rule:
    def __init__(
        self,
        name: str,
        url: str,
        func: Callable[[Manifest], Tuple[List[Node], List[Node]]],
    ):
        self.name = name
        self.url = url
        self.func = func

    def apply(self, manifest) -> Tuple[List[Node], List[Node]]:
        return self.func(manifest)
