"""
Script for parsing the configuration for the app.
"""
import os
from functools import cache
from pathlib import Path

import tomllib
from config.config_models import APIConfig
from loguru import logger

# NOTE: This is the only magic variable that we use! All other things should be delcared
# via a BaseSettings object (in pydantic_models/config_models).
CONFIG_ENV_VARIABLE_NAME = "APP_CONFIG_PATH"


@cache
def parse_config(config_path: str | None = None) -> APIConfig:
    """
    Parse the config from the config_path and return an APIConfig object.
    
    If config_path is None, we will look for a path in the CONFIG_ENV_VARIABLE_NAME.
    """
    config_path = config_path or os.getenv(CONFIG_ENV_VARIABLE_NAME)
    if config_path is None:
        logger.info("No explicit config path found. Defaulting to /config/local_config.toml")
        path_obj = get_config_folder_path() / "local_config.toml"
    else:
        path_obj = Path(config_path)

    with open(path_obj, "rb") as f:
        raw_config = tomllib.load(f)

    return APIConfig.model_validate(raw_config)

@cache
def get_config_folder_path() -> Path:
    this_module_path = Path(__file__).absolute()
    return this_module_path.parent.parent.parent / Path("config")
