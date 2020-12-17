# -*- coding: utf-8 -*-
"""Document engine here.

Copyright (C) 2020, Auto Trader UK
Created 16. Dec 2020 14:45

"""
from typing import List

import networkx as nx

from olivertwist.manifest import Manifest
from olivertwist.metricengine.result import MetricResult


class MetricEngine:
    def run(self, manifest: Manifest) -> List[MetricResult]:
        graph = manifest.graph
        degree_centrality = nx.centrality.degree_centrality(graph)
        in_degree_centrality = nx.centrality.in_degree_centrality(graph)
        out_degree_centrality = nx.centrality.out_degree_centrality(graph)
        closeness_centrality = nx.centrality.closeness_centrality(graph)
        betweenness_centrality = nx.centrality.betweenness_centrality(graph)
        pagerank = nx.link_analysis.pagerank_alg.pagerank(graph)

        results = []
        for node in graph.nodes:
            results.append(
                MetricResult(
                    manifest.get_node(node),
                    degree_centrality[node],
                    in_degree_centrality[node],
                    out_degree_centrality[node],
                    closeness_centrality[node],
                    betweenness_centrality[node],
                    pagerank[node],
                )
            )

        return results
