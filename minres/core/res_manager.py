#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import platform
import re
import subprocess
import yaml
from dataclasses import dataclass
from typing import List, Optional

from minres.core.logger import logger


@dataclass
class ResConfig:
    path: List[str]
    pattern: str
    elems: List[str]


class ResManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_config(self, file_path: str) -> None:
        logger.info(f"Loading configuration from {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            logger.debug("YAML data loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load YAML file: {e}")
            raise

        self.configs = {}
        for key, val in data.items():
            self.configs[key] = ResConfig(**val)
        self.keys = list(data.keys())
        logger.info(f"Configuration loaded with keys: {self.keys}")

    def get_keys(self) -> List[str]:
        return self.keys

    def get_res_columns(self, key) -> List[str]:
        """Get column names for a specific resource type."""
        if key not in self.configs:
            logger.warning(f"Key '{key}' not found in configs")
            return []

        return self.configs[key].elems

    def parse_name(self, key: str, name: str) -> Optional[List[str]]:
        result = re.findall(self.configs[key].pattern, name)

        if len(result) != 1:
            logger.debug(f"Pattern match failed for file '{name}' with key '{key}'")
            return None

        elems = result[0]
        if len(elems) != len(self.configs[key].elems):
            logger.debug(f"Element count mismatch for file '{name}' with key '{key}'")
            return None

        return list(elems)

    def get_res_data(self, key: str) -> List[List[str]]:
        logger.info(f"Retrieving resource data for key '{key}'")
        data = []

        if key not in self.configs:
            logger.warning(f"Key '{key}' not found in configs")
            return []

        for path in self.configs[key].path:
            logger.debug(f"Scanning path: {path}")
            for root, _, files in os.walk(path):
                for file in files:
                    result = self.parse_name(key, file)
                    if not result:
                        logger.debug(f"Invalid name: {file}")
                        continue
                    result.insert(0, os.path.join(root, file))
                    data.append(result)

        logger.info(f"Retrieved {len(data)} resource entries for key '{key}'")
        return data


def open_file_with_default_app(file_path: str) -> bool:
    """
    Open file with system default application, supports Windows, macOS, Linux
    Returns True on success, False on failure
    """
    # Check if file exists
    if not os.path.exists(file_path):
        logger.error(f"File does not exist: {file_path}")
        return False

    system = platform.system()
    logger.debug(f"Opening file '{file_path}' on {system}")

    try:
        if system == "Windows":
            subprocess.run(["start", file_path], shell=True, check=True)
        elif system == "Darwin":
            subprocess.run(["open", file_path], check=True)
        else:
            subprocess.run(["xdg-open", file_path], check=True)
        logger.info(f"Successfully opened: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to open file: {e}")
        return False
