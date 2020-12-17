# -*- coding: utf-8 -*-
"""Models should all be enabled.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 15:51

"""
from typing import List, Tuple

from olivertwist.manifest import Manifest, Node
from olivertwist.rules.utils import partition


def no_disabled_models(manifest: Manifest) -> Tuple[List[Node], List[Node]]:
    passes, failures = partition(lambda x: not x.is_enabled, manifest.nodes())
    return list(passes), list(failures)
