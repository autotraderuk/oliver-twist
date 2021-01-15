from dataclasses import dataclass
from enum import Enum
from json import JSONEncoder
from typing import List


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


@dataclass
class ReportStatus(str, Enum):
    PASSED = "passed"
    SKIPPED = "skipped"
    ERRORED = "errored"
    WARNED = "warned"


@dataclass
class ReportRule:
    def __init__(
        self,
        id: str,
        name: str,
        status: ReportStatus,
    ):
        self.id = id
        self.name = name
        self.status = status


@dataclass
class ReportMetrics:
    def __init__(
        self,
        name: str,
        score: int,
    ) -> None:
        self.name = name
        self.score = score
        self.pretty_name = name.replace("_", " ").capitalize()


@dataclass
class ReportSummary:
    def __init__(
        self,
        passed: int,
        skipped: int,
        errored: int,
        warned: int,
    ) -> None:
        self.passed = passed
        self.skipped = skipped
        self.errored = errored
        self.warned = warned


@dataclass
class ReportModel:
    def __init__(
        self,
        model_key: str,
        file_path: str,
        model_name: str,
        metrics: List[ReportMetrics],
        rules: List[ReportRule],
        summary: ReportSummary,
    ) -> None:
        self.model_key = model_key
        self.file_path = file_path
        self.model_name = model_name
        self.metrics = metrics
        self.rules = rules
        self.summary = summary


@dataclass
class Report:
    def __init__(self, summary: ReportSummary, models: List[ReportModel]) -> None:
        self.summary = summary
        self.models = models
