# -*- coding: utf-8 -*-
"""Some CLI test

Copyright (C) 2021, Auto Trader UK
Created 21. Jan 2021 19:37

"""
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from olivertwist.config.configurator import Configurator
from olivertwist.config.io import ConfigIO
from olivertwist.config.model import Config, RuleConfig
from olivertwist.main import main


def test_check_non_existent_manifest():
    runner = CliRunner()
    missing_manifest_json = "manifest.json"
    with runner.isolated_filesystem():
        result = runner.invoke(main, ["check", missing_manifest_json])

        assert result.exit_code != 0
        assert (
            f"Could not open file: {missing_manifest_json}: No such file or directory"
            in result.output
        )


def test_check_with_non_existent_config():
    runner = CliRunner()
    manifest_json = "manifest.json"
    with runner.isolated_filesystem():
        with open(manifest_json, "w") as fh:
            fh.write("{}")

        result = runner.invoke(main, ["check", "--config=twisted.yml", manifest_json])

        assert result.exit_code != 0
        assert "Invalid value for '--config'" in result.output


@patch.object(Configurator, "update", return_value=Config.empty())
def test_config_outputs_file(_):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(main, ["config"])

        assert result.exit_code == 0
        config_path = Path("olivertwist.yml")
        assert config_path.exists
        assert result.output == f"Created/updated config in {config_path}\n"


@patch.object(Configurator, "update", return_value=Config.empty())
def test_config_with_config_file_not_existing(_):
    runner = CliRunner()
    config_path = Path("twisted.yml")
    with runner.isolated_filesystem():
        assert not config_path.exists()

        result = runner.invoke(main, ["--debug", "config", f"--config={config_path}"])

        assert result.exit_code == 0
        assert result.output == f"Created/updated config in {config_path}\n"
        assert config_path.exists()


@patch.object(Configurator, "update", return_value=Config.empty())
def test_config_with_config_file_existing(_):
    runner = CliRunner()
    config_path = "twisted.yml"
    dummy_rule_config = RuleConfig("a", enabled=False)
    with runner.isolated_filesystem():
        ConfigIO.write(Config(universal=[dummy_rule_config]), config_path)

        result = runner.invoke(main, ["config", "--config=twisted.yml"])

        assert result.exit_code == 0
        assert result.output == f"Created/updated config in {config_path}\n"
        assert (
            ConfigIO.read(config_path) == Config.empty()
        ), "existing config not overwritten"
