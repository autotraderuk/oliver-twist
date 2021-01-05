# -*- coding: utf-8 -*-
"""Document __init__.py here.

Copyright (C) 2020, Auto Trader UK
Created 23. Dec 2020 13:40

"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

from dataclasses_jsonschema import JsonSchemaMixin


class Severity(Enum):
    WARNING = "warning"
    ERROR = "error"


@dataclass
class RuleConfig(JsonSchemaMixin):
    id: str
    enabled: bool
    severity: Optional[Severity] = Severity.ERROR


@dataclass
class Config(JsonSchemaMixin):
    universal: List[RuleConfig]

    def get_disabled_rule_ids(self) -> List[str]:
        return [r.id for r in self.universal if r.enabled is False]

    def get_config_for_rule_id(self, rule_id: str) -> RuleConfig:
        for rule_config in self.universal:
            if rule_config.id == rule_id:
                return rule_config

        return None
