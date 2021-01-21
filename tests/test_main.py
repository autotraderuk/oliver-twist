# -*- coding: utf-8 -*-
"""Some CLI test

Copyright (C) 2021, Auto Trader UK
Created 21. Jan 2021 19:37

"""

from click.testing import CliRunner

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
