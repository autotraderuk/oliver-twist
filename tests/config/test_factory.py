# -*- coding: utf-8 -*-
"""Document test_config here.

Copyright (C) 2020, Auto Trader UK
Created 22. Dec 2020 19:10

"""
import os

import pytest

from olivertwist.config.factory import (
    ConfigFactory,
    InvalidConfigException,
)
from olivertwist.config.model import (
    Config,
    RuleConfig,
)

PATH_TO_VALID_CONFIG = os.path.join(os.path.dirname(__file__), "valid_config.yml")
PATH_TO_INVALID_CONFIG = os.path.join(os.path.dirname(__file__), "invalid_config.yml")


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
    with pytest.raises(InvalidConfigException):
        ConfigFactory.create_config_from_path(PATH_TO_INVALID_CONFIG)
