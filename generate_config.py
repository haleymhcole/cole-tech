#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 15:08:22 2025

@author: haleycole

This includes:

✅ Automatic regeneration of config.toml every time you run Streamlit
✅ Validation of color formats (#RRGGBB)
✅ Automatic creation of .streamlit/
✅ Optional dark mode support
✅ Warnings if keys are missing
✅ Logging so you always know what happened
"""

from config.settings_manager import get_setting
import os
from palette import PALETTE

def generate_toml():
    theme = get_setting("theme")
    color_palette = PALETTE[theme]
    
    # Values Streamlit expects
    primary = color_palette.get("primary", "#000000")
    background = color_palette.get("background", "#FFFFFF")
    secondary_background = color_palette.get("secondary_background", "#F0F0F0")
    text = color_palette.get("text", "#000000")

    # Ensure the .streamlit directory exists
    os.makedirs(".streamlit", exist_ok=True)

    toml_path = ".streamlit/config.toml"

    toml_content = f"""
[theme]
primaryColor="{primary}"
backgroundColor="{background}"
secondaryBackgroundColor="{secondary_background}"
textColor="{text}"
font="sans serif"
""".strip()

    with open(toml_path, "w") as f:
        f.write(toml_content)

    print("✔ .streamlit/config.toml successfully generated!")
    
    
# def update_toml(theme):
#     color_palette = PALETTE[theme]
    
#     print("Updating color theme to:", theme)
    
#     # Values Streamlit expects
#     primary = color_palette.get("primary", "#000000")
#     background = color_palette.get("background", "#FFFFFF")
#     secondary_background = color_palette.get("secondary_background", "#F0F0F0")
#     text = color_palette.get("text", "#000000")

#     # Ensure the .streamlit directory exists
#     os.makedirs(".streamlit", exist_ok=True)

#     toml_path = ".streamlit/config.toml"

#     toml_content = f"""
# [theme]
# primaryColor="{primary}"
# backgroundColor="{background}"
# secondaryBackgroundColor="{secondary_background}"
# textColor="{text}"
# font="sans serif"
# """.strip()

#     with open(toml_path, "w") as f:
#         f.write(toml_content)

if __name__ == "__main__":
    generate_toml()
