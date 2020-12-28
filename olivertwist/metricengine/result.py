# -*- coding: utf-8 -*-
"""Document rule here.

Copyright (C) 2020, Auto Trader UK
Created 16. Dec 2020 14:31

"""
from olivertwist.manifest import Node


class MetricResult:
    def __init__(
        self,
        node: Node,
        degree_centrality: float,
        in_degree_centrality: float,
        out_degree_centrality: float,
        closeness_centrality: float,
        betweenness_centrality: float,
        pagerank: float,
    ):
        self.node = node
        self.degree_centrality = degree_centrality
        self.in_degree_centrality = in_degree_centrality
        self.out_degree_centrality = out_degree_centrality
        self.closeness_centrality = closeness_centrality
        self.betweenness_centrality = betweenness_centrality
        self.pagerank = pagerank
