# -*- coding: utf-8 -*-
"""Staging models should have a single source.

Copyright (C) 2020, Auto Trader UK
Created 15. Dec 2020 17:40

"""

from typing import List, Tuple

from olivertwist.manifest import Manifest, Node
from olivertwist.ruleengine.rule import rule
from olivertwist.rules.utils import partition


@rule(
    id="single-source-per-staging-model",
    name="Staging scripts can only reference a single source",
)
def staging_models_have_single_source(
    manifest: Manifest,
) -> Tuple[List[Node], List[Node]]:
    def staging_model_has_more_than_one_source(node: Node):
        sources = [
            p
            for p in manifest.graph.predecessors(node.id)
            if manifest.get_node(p).is_source
        ]
        return node.is_staging and len(list(sources)) > 1

    passes, failures = partition(
        staging_model_has_more_than_one_source, manifest.nodes()
    )
    return list(passes), list(failures)
