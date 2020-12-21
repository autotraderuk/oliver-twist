from olivertwist.manifest import Node
from olivertwist.metricengine.result import MetricResult
from olivertwist.reporter.adapter import to_html_report
from olivertwist.reporter.model import *
from olivertwist.ruleengine.result import Result
from olivertwist.ruleengine.rule import Rule

expected_html_report: Report = Report(
    ReportSummary(1, 0, 1),
    [
        ReportModel(
            "model1",
            "",
            "model1",
            [
                ReportMetrics("degree_centrality", 0),
                ReportMetrics("in_degree_centrality", 0),
                ReportMetrics("out_degree_centrality", 0),
                ReportMetrics("closeness_centrality", 0),
                ReportMetrics("betweenness_centrality", 0),
                ReportMetrics("pagerank", 0),
            ],
            [ReportRule("a-rule", "a rule name", ReportStatus.PASSED)],
            ReportSummary(1, 0, 0),
        ),
        ReportModel(
            "model2",
            "",
            "model2",
            [
                ReportMetrics("degree_centrality", 0),
                ReportMetrics("in_degree_centrality", 0),
                ReportMetrics("out_degree_centrality", 0),
                ReportMetrics("closeness_centrality", 0),
                ReportMetrics("betweenness_centrality", 0),
                ReportMetrics("pagerank", 0),
            ],
            [
                ReportRule("a-failed-rule", "a rule name", ReportStatus.ERRORED,)
            ],
            ReportSummary(0, 0, 1),
        ),
    ],
)


def test_should_convert_to_html_output():
    rule: Rule = Rule("a-failed-rule", "a rule name", None)
    model1 = Node({"unique_id": "model1"})
    model2 = Node({"unique_id": "model2"})
    passes: List[Node] = [model1]
    failures: List[Node] = [model2]
    domain_results: List[Result] = [Result(rule, passes, failures)]
    metric_results: List[MetricResult] = [
        MetricResult(model1, 0, 0, 0, 0, 0, 0),
        MetricResult(model2, 0, 0, 0, 0, 0, 0),
    ]

    actual: Report = to_html_report(domain_results, metric_results)

    assert actual == expected_html_report


def test_json_serialisation():
    actual = MyEncoder().encode(expected_html_report)

    expected_serialisation = """{"summary": {"passed": 1, "skipped": 0, "errored": 1}, "models": [{"model_key": "model1", "file_path": "", "model_name": "model1", "metrics": [{"name": "degree_centrality", "score": 0, "pretty_name": "Degree centrality"}, {"name": "in_degree_centrality", "score": 0, "pretty_name": "In degree centrality"}, {"name": "out_degree_centrality", "score": 0, "pretty_name": "Out degree centrality"}, {"name": "closeness_centrality", "score": 0, "pretty_name": "Closeness centrality"}, {"name": "betweenness_centrality", "score": 0, "pretty_name": "Betweenness centrality"}, {"name": "pagerank", "score": 0, "pretty_name": "Pagerank"}], "rules": [{"id": "a-rule", "name": "a rule name", "status": "passed"}], "summary": {"passed": 1, "skipped": 0, "errored": 0}}, {"model_key": "model2", "file_path": "", "model_name": "model2", "metrics": [{"name": "degree_centrality", "score": 0, "pretty_name": "Degree centrality"}, {"name": "in_degree_centrality", "score": 0, "pretty_name": "In degree centrality"}, {"name": "out_degree_centrality", "score": 0, "pretty_name": "Out degree centrality"}, {"name": "closeness_centrality", "score": 0, "pretty_name": "Closeness centrality"}, {"name": "betweenness_centrality", "score": 0, "pretty_name": "Betweenness centrality"}, {"name": "pagerank", "score": 0, "pretty_name": "Pagerank"}], "rules": [{"id": "a-failed-rule", "name": "a rule name", "status": "errored"}], "summary": {"passed": 0, "skipped": 0, "errored": 1}}]}"""

    assert actual == expected_serialisation
