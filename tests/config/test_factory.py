# -*- coding: utf-8 -*-
"""Document test_config here.

Copyright (C) 2020, Auto Trader UK
Created 22. Dec 2020 19:10

"""
from pathlib import Path

import pytest

from olivertwist.config.factory import (
    ConfigFactory,
    InvalidConfigError,
)
from olivertwist.config.model import (
    Config,
    RuleConfig,
)

PATH_TO_VALID_CONFIG = Path(__file__).parent / "valid_config.yml"
PATH_TO_INVALID_CONFIG = Path(__file__).parent / "invalid_config.yml"
PATH_TO_DUPLICATE_CONFIG = Path(__file__).parent / "duplicate_config.yml"


def test_parsing_valid_config():
    config = ConfigFactory.create_config_from_path(PATH_TO_VALID_CONFIG)

    assert config == Config(
        universal=[
            RuleConfig(id="no-rejoin-models", enabled=False),
            RuleConfig(id="no-disabled-models", enabled=True),
        ]
    )


def test_getting_disabled_rule_ids_from_config():
    config = ConfigFactory.create_config_from_path(PATH_TO_VALID_CONFIG)

    assert config.get_disabled_rule_ids() == ["no-rejoin-models"]


def test_parsing_invalid_config():
    with pytest.raises(InvalidConfigError):
        ConfigFactory.create_config_from_path(PATH_TO_INVALID_CONFIG)


def test_config_with_duplicates_raises_error():
    with pytest.raises(InvalidConfigError):
        ConfigFactory.create_config_from_path(PATH_TO_DUPLICATE_CONFIG)
