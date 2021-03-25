# -*- coding: utf-8 -*-
"""Domain objects for reporting."""

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
        score: float,
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

    @classmethod
    def from_models(cls, models: List["ReportModel"]):
        # TODO: Implement summary.skipped
        skipped = 0
        errored = len([a_model for a_model in models if a_model.summary.errored > 0])
        warned = len([a_model for a_model in models if a_model.summary.warned > 0])
        passed = len(models) - errored - warned

        return cls(passed, skipped, errored, warned)


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

    @classmethod
    def from_models(cls, models: List[ReportModel]):
        return cls(ReportSummary.from_models(models), models)
