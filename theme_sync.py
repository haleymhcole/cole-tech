#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 15:14:22 2025

@author: haleycole

This script:

    Imports the palette
    
    Validates all hex codes
    
    Writes .streamlit/config.toml every time
    
    Detects missing keys
    
    Supports light & dark mode
    
    Logs results
"""

import os
import re
import sys
from palette import PALETTE

# --- Configuration ---
DEFAULT_MODE = "light"   # or "dark"
REQUIRED_KEYS = ["primary", "background", "secondary_background", "text"]
COLOR_REGEX = r"^#[0-9A-Fa-f]{6}$"


def validate_hex(color: str):
    """Return True if color is valid hex."""
    return bool(re.match(COLOR_REGEX, color))


def validate_palette(mode_dict, mode_name):
    """Validate that all required keys exist and are proper hex codes."""
    print(f"\n🔍 Validating {mode_name} color mode...")

    errors = []
    
    # Check missing keys
    for key in REQUIRED_KEYS:
        if key not in mode_dict:
            errors.append(f"Missing key '{key}' in {mode_name} mode.")

    # Check hex formatting
    for key, value in mode_dict.items():
        if not validate_hex(value):
            errors.append(f"Invalid hex format for {mode_name}.{key}: '{value}'")

    if errors:
        print("❌ Validation errors found:")
        for e in errors:
            print("  - " + e)
        sys.exit("\nFix errors in palette.py and try again.")

    print(f"✔ {mode_name} mode validated successfully.")


def write_toml(mode_dict):
    """Create .streamlit/config.toml from the palette."""
    os.makedirs(".streamlit", exist_ok=True)
    toml_path = ".streamlit/config.toml"

    toml = f"""
[theme]
primaryColor="{mode_dict['primary']}"
backgroundColor="{mode_dict['background']}"
secondaryBackgroundColor="{mode_dict['secondary_background']}"
textColor="{mode_dict['text']}"
font="sans serif"
""".strip()

    with open(toml_path, "w") as f:
        f.write(toml)

    print(f"✔ Theme written to {toml_path}")


def sync_theme():
    """Main routine to sync theme automatically."""
    if DEFAULT_MODE not in PALETTE:
        sys.exit(f"❌ Error: DEFAULT_MODE '{DEFAULT_MODE}' not in PALETTE keys {list(PALETTE.keys())}")

    mode_dict = PALETTE[DEFAULT_MODE]

    validate_palette(mode_dict, DEFAULT_MODE)
    write_toml(mode_dict)

    print("\n🌈 Theme sync complete. Ready to launch Streamlit!")


if __name__ == "__main__":
    sync_theme()
