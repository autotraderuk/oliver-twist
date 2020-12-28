# -*- coding: utf-8 -*-
"""Models should all be enabled.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 15:51

"""
from typing import List, Tuple, Optional

from olivertwist.manifest import Manifest, Node
from olivertwist.ruleengine.rule import rule
from olivertwist.rules.utils import partition


@rule(id="no-owner-on-physical-models", name="No owner on physical models")
def no_owner_on_physical_models(manifest: Manifest) -> Tuple[List[Node], List[Node]]:
    passes, failures = partition(
        lambda x: x.is_db_relation and __is_none_or_blank(x.owner), manifest.nodes()
    )
    return list(passes), list(failures)


def __is_none_or_blank(owner: Optional[str]):
    return owner is None or owner.strip(" ") == ""
