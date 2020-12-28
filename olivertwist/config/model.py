# -*- coding: utf-8 -*-
"""Document __init__.py here.

Copyright (C) 2020, Auto Trader UK
Created 23. Dec 2020 13:40

"""

from dataclasses import dataclass
from typing import List

from dataclasses_jsonschema import JsonSchemaMixin


@dataclass
class RuleConfig(JsonSchemaMixin):
    id: str
    enabled: bool


@dataclass
class Config(JsonSchemaMixin):
    universal: List[RuleConfig]

    def get_disabled_rule_ids(self) -> List[str]:
        return [r.id for r in self.universal if r.enabled is False]
