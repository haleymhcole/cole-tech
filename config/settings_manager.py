#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 23:58:56 2025

@author: haleycole
"""
import os
import yaml
from pathlib import Path

SETTINGS_PATH = Path(os.path.join("config","settings.yaml"))

def load_settings():
    """Load settings from YAML file."""
    if not SETTINGS_PATH.exists():
        #raise FileNotFoundError(f"{SETTINGS_PATH} missing.")
        txt = """
        data_format: excel
        image_format: tiff
        output_folder: outputs
        theme: dark
        units: metric
        video_format: mp4
        """
        with open(SETTINGS_PATH, "w") as f:
            f.write(txt)
    with open(SETTINGS_PATH, "r") as f:
        return yaml.safe_load(f)

def save_settings(updated_settings: dict):
    """Write updated settings to YAML file."""
    with open(SETTINGS_PATH, "w") as f:
        yaml.safe_dump(updated_settings, f, default_flow_style=False)

# Global cached settings
_settings_cache = None

def get_settings():
    """Return settings object globally."""
    global _settings_cache
    if _settings_cache is None:
        _settings_cache = load_settings()
    return _settings_cache

# def update_setting(key, value):
#     """Update one setting and persist it."""
#     global _settings_cache
#     settings = get_settings()
#     settings[key] = value
#     save_settings(settings)
#     _settings_cache = settings
