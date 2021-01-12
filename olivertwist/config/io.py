# -*- coding: utf-8 -*-
"""Document __init__.py here.

Copyright (C) 2020, Auto Trader UK
Created 22. Dec 2020 19:36

"""
from collections import Counter
from pathlib import Path
from typing import Union

import yaml

try:
    from yaml import CSafeLoader as YamlLoader
except ImportError:
    from yaml import SafeLoader as YamlLoader

from dataclasses_jsonschema import ValidationError

from olivertwist.config.model import Config


class InvalidConfigError(Exception):
    """Thrown if an invalid configuration file is supplied."""


class DuplicateEntryError(InvalidConfigError):
    """Duplicate sections were present in the supplied config."""


class ConfigIO:
    DEFAULT_CONFIG_FILE_PATH = Path("./olivertwist.yml")
    CONFIG_FILE_VERSIONS = {"1.0": Config}
    LATEST_CONFIG_FILE_VERSION = list(sorted(CONFIG_FILE_VERSIONS))[-1]

    @classmethod
    def read(cls, path: Union[Path, str]) -> Config:
        if path is None:
            if cls.DEFAULT_CONFIG_FILE_PATH.exists():
                config = cls.__parse(cls.DEFAULT_CONFIG_FILE_PATH)
            else:
                return Config(universal=[])
        else:
            config = cls.__parse(path)

        return cls.__validate(config)

    @classmethod
    def write(cls, config: Config, path: Union[Path, str]):
        with open(path, "w") as handle:
            config_dict = config.to_dict()
            config_dict["version"] = cls.LATEST_CONFIG_FILE_VERSION
            yaml.dump(config_dict, handle)

    @classmethod
    def __parse(cls, config_file_path: Union[Path, str]) -> Config:
        try:
            with open(config_file_path, "rb") as handle:
                yaml_config_dict = yaml.load(
                    handle.read().decode("utf-8"), Loader=YamlLoader
                )
                # When we have a later version we can do something with the version...
                _ = yaml_config_dict.pop("version")
                return Config.from_dict(yaml_config_dict)
        except KeyError:
            raise InvalidConfigError("Version is missing.")
        except ValidationError as e:
            raise InvalidConfigError(e)

    @classmethod
    def __validate(cls, config: Config) -> Config:
        entry_counts = Counter(rule.id for rule in config.universal)
        duplicates = [id_ for id_, count in entry_counts.items() if count > 1]
        if duplicates:
            raise DuplicateEntryError(", ".join(duplicates))

        return config
