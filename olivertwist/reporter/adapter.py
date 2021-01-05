from typing import Dict, List

from olivertwist.manifest import Node
from olivertwist.metricengine.result import MetricResult
from olivertwist.reporter.model import (
    Report,
    ReportMetrics,
    ReportModel,
    ReportRule,
    ReportStatus,
    ReportSummary,
)
from olivertwist.ruleengine.result import Result
from olivertwist.ruleengine.rule import Rule


def to_html_report(
    domain_results: List[Result], metric_results: List[MetricResult]
) -> Report:
    models: List[ReportModel] = __organise_by_model(domain_results, metric_results)
    summary: ReportSummary = __derive_summary(models)
    return Report(summary, models)


def __derive_summary(models: List[ReportModel]) -> ReportSummary:
    # TODO: summary.skipped?
    skipped = 0
    errored = len([a_model for a_model in models if a_model.summary.errored > 0])
    warned = len([a_model for a_model in models if a_model.summary.warned > 0])
    passed = len(models) - errored - warned

    return ReportSummary(passed, skipped, errored, warned)


def __organise_by_model(
    domain_results: List[Result], metric_results: List[MetricResult]
) -> List[ReportModel]:
    # model_key -> model
    deduped_nodes: Dict[str, Node] = __domain_node_by_model_name(domain_results)
    passed_rules_by_model: Dict[str, List[Rule]] = __passed_rules_by_model_name(
        domain_results
    )
    errored_rules_by_model: Dict[str, List[Rule]] = __errored_rules_by_model_name(
        domain_results
    )
    warned_rules_by_model: Dict[str, List[Rule]] = __warned_rules_by_model(
        domain_results
    )

    html_rules_by_model: Dict[str, List[ReportRule]] = __html_rules_by_model_name(
        passed_rules_by_model, errored_rules_by_model, warned_rules_by_model
    )
    metrics_results_by_model = __metric_results_by_model_name(metric_results)

    html_models = []
    for model_name in deduped_nodes.keys():
        html_summary = ReportSummary(
            len(passed_rules_by_model.get(model_name, [])),
            0,
            len(errored_rules_by_model.get(model_name, [])),
            len(warned_rules_by_model.get(model_name, [])),
        )
        html_model = ReportModel(
            model_name,
            "",
            model_name,
            metrics_results_by_model[model_name],
            html_rules_by_model[model_name],
            html_summary,
        )
        html_models.append(html_model)

    return html_models


def __html_rules_by_model_name(
    passed_rules_by_model: Dict[str, List[Rule]],
    errored_rules_by_model: Dict[str, List[Rule]],
    warned_rules_by_model: Dict[str, List[Rule]],
) -> Dict[str, List[ReportRule]]:
    result: Dict[str, List[ReportRule]] = {}
    for model_name, domain_rules in passed_rules_by_model.items():
        html_rules: List[ReportRule] = [
            ReportRule(domain_rule.id, domain_rule.name, ReportStatus.PASSED)
            for domain_rule in domain_rules
        ]
        result[model_name] = html_rules

    for model_name, domain_rules in errored_rules_by_model.items():
        html_rules: List[ReportRule] = [
            ReportRule(domain_rule.id, domain_rule.name, ReportStatus.ERRORED)
            for domain_rule in domain_rules
        ]
        result.setdefault(model_name, []).extend(html_rules)

    for model_name, domain_rules in warned_rules_by_model.items():
        html_rules: List[ReportRule] = [
            ReportRule(domain_rule.id, domain_rule.name, ReportStatus.WARNED)
            for domain_rule in domain_rules
        ]
        result.setdefault(model_name, []).extend(html_rules)

    return result


def __passed_rules_by_model_name(domain: List[Result]) -> Dict[str, List[Rule]]:
    passed_rules: Dict[str, List[Rule]] = {}
    for a_domain in domain:
        for node in a_domain.passes:
            passed_rules.setdefault(node.id, []).append(a_domain.rule)
    return passed_rules


def __errored_rules_by_model_name(domain: List[Result]) -> Dict[str, List[Rule]]:
    failed_rules: Dict[str, List[Rule]] = {}
    for a_domain in domain:
        if a_domain.has_errors:
            for node in a_domain.failures:
                failed_rules.setdefault(node.id, []).append(a_domain.rule)
    return failed_rules


def __warned_rules_by_model(domain: List[Result]) -> Dict[str, List[Rule]]:
    failed_rules: Dict[str, List[Rule]] = {}
    for a_domain in domain:
        if a_domain.has_warnings:
            for node in a_domain.failures:
                failed_rules.setdefault(node.id, []).append(a_domain.rule)
    return failed_rules


def __domain_node_by_model_name(domain: List[Result]) -> Dict[str, Node]:
    deduped_nodes: Dict[str, Node] = {}
    for a_domain in domain:
        all_nodes: List[Node] = a_domain.passes + a_domain.failures
        for duped_node in all_nodes:
            deduped_nodes[duped_node.id] = duped_node
    return deduped_nodes


def __metric_results_by_model_name(
    metric_results: List[MetricResult],
) -> Dict[str, List[ReportMetrics]]:
    results = {}
    for result in metric_results:
        metrics = []
        metrics.append(ReportMetrics("degree_centrality", result.degree_centrality))
        metrics.append(
            ReportMetrics("in_degree_centrality", result.in_degree_centrality)
        )
        metrics.append(
            ReportMetrics("out_degree_centrality", result.out_degree_centrality)
        )
        metrics.append(
            ReportMetrics("closeness_centrality", result.closeness_centrality)
        )
        metrics.append(
            ReportMetrics("betweenness_centrality", result.betweenness_centrality)
        )
        metrics.append(ReportMetrics("pagerank", result.pagerank))
        results[result.node.id] = metrics
    return results
