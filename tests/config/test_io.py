# -*- coding: utf-8 -*-
"""Document test_config here.

Copyright (C) 2020, Auto Trader UK
Created 22. Dec 2020 19:10

"""
from pathlib import Path
from tempfile import mkdtemp

import pytest

from olivertwist.config.io import (
    ConfigIO,
    InvalidConfigError,
)
from olivertwist.config.model import (
    Config,
    RuleConfig,
)

PATH_TO_CONFIGS = Path(__file__).parent / "examples"
PATH_TO_VALID_CONFIG = PATH_TO_CONFIGS / "valid_config.yml"
PATH_TO_INVALID_CONFIG = PATH_TO_CONFIGS / "invalid_config.yml"
PATH_TO_DUPLICATE_CONFIG = PATH_TO_CONFIGS / "duplicate_config.yml"
PATH_TO_NO_VERSION_CONFIG = PATH_TO_CONFIGS / "no_version_config.yml"


@pytest.fixture
def config():
    return Config(
        universal=[
            RuleConfig(id="no-rejoin-models", enabled=False),
            RuleConfig(id="no-disabled-models", enabled=True),
        ]
    )


def test_parsing_valid_config(config: Config):
    parsed_config = ConfigIO.read(PATH_TO_VALID_CONFIG)

    assert parsed_config == config


def test_getting_disabled_rule_ids_from_config():
    config = ConfigIO.read(PATH_TO_VALID_CONFIG)

    assert config.get_disabled_rule_ids() == ["no-rejoin-models"]


def test_parsing_invalid_config():
    with pytest.raises(InvalidConfigError):
        ConfigIO.read(PATH_TO_INVALID_CONFIG)


def test_parsing_config_with_no_version_raises_error():
    with pytest.raises(InvalidConfigError):
        ConfigIO.read(PATH_TO_NO_VERSION_CONFIG)


def test_parsing_config_with_duplicates_raises_error():
    with pytest.raises(InvalidConfigError):
        ConfigIO.read(PATH_TO_DUPLICATE_CONFIG)


def test_parsing_missing_config_file():
    path_to_non_existent_config = Path() / "non_existent_config.yml"
    with pytest.raises(FileNotFoundError):
        ConfigIO.read(path_to_non_existent_config)


def test_serializing_config(config: Config):
    work_dir = mkdtemp()
    path = Path(work_dir) / "olivertwist.yml"

    ConfigIO.write(config, path)

    assert ConfigIO.read(path) == ConfigIO.read(PATH_TO_VALID_CONFIG)
