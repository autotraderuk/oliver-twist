# -*- coding: utf-8 -*-
"""Document __init__.py here.

Copyright (C) 2020, Auto Trader UK
Created 22. Dec 2020 19:36

"""
import os.path
import yaml

try:
    from yaml import CSafeLoader as YamlLoader
except ImportError:
    from yaml import SafeLoader as YamlLoader

from dataclasses_jsonschema import ValidationError    

from olivertwist.config.model import Config

class InvalidConfigException(Exception):
    """Thrown if an invalid configuration file is supplied."""


DEFAULT_CONFIG_FILE_PATH = "./olivertwist.yml"


class ConfigFactory:
    @classmethod
    def __parse(cls, config_file_path) -> Config:
        try:
            with open(config_file_path, "rb") as handle:
                yaml_config_dict = yaml.load(
                    handle.read().decode("utf-8"), Loader=YamlLoader
                )
                return Config.from_dict(yaml_config_dict)
        except ValidationError as e:
            raise InvalidConfigException(e)

    @classmethod
    def create_congfig_from_path(cls, path: str) -> Config:
        if path is None:
            if os.path.isfile(DEFAULT_CONFIG_FILE_PATH):
                return cls.__parse(DEFAULT_CONFIG_FILE_PATH)
            else:
                return Config(universal=[])
        else:
            return cls.__parse(path)
