# -*- coding: utf-8 -*-
"""Auto-magic rule discovery.

Copyright (C) 2021, Auto Trader UK
Created 08. Jan 2021 18:01

"""
import importlib
import os
from pathlib import Path
from typing import List, Union

from olivertwist.ruleengine.rule import Rule


def rules_in_path(path: Union[Path, str]) -> List[Rule]:
    if isinstance(path, str):
        path = Path(path)

    rules = []
    for root, dirs, files in os.walk(path):
        rule_files = [Path(root) / f for f in files if Path(f).suffix == ".py"]
        for p in rule_files:
            mod_name = f"ot_custom_rule_file_{hash(p)}"
            loader = importlib.machinery.SourceFileLoader(mod_name, str(p))
            spec = importlib.util.spec_from_loader(mod_name, loader)
            mod = importlib.util.module_from_spec(spec)
            loader.exec_module(mod)
            for obj in mod.__dict__.values():
                if isinstance(obj, Rule):
                    rules.append(obj)

    return rules


def _might_contain_rules(path: Union[Path, str]) -> bool:
    p = Path(path)
    return p.suffix == ".py"
