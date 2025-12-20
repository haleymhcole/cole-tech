#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 15:40:48 2025

@author: haleycole

Settings page:
    output folder picker
    
    image file format
    
    data export file format
    
    units (metric vs imperial)
    
    theme (dark vs light)
    
    persistent storage in config/settings.yaml
    
    a small helper module that makes these settings available globally to all other files (e.g., in your calculation scripts)
"""
import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
from pathlib import Path
from config.settings_manager import get_settings, save_settings
# from generate_config import update_toml

def render():    
    # st.title("Settings")
    # theme = st.selectbox("Theme", ["Light", "Dark"])
    # units = st.radio("Units", ["Metric", "Imperial"])
    # st.write("Additional settings here...")
    
    

    st.title("Settings")

    settings = get_settings()

    

    # ---- Output Folder ----
    # output_folder = st.text_input(
    #     "Output Folder",
    #     value=settings.get("output_folder", "outputs"),
    #     help="Folder where exported results will be saved."
    # )
    # output_folder = st.file_uploader("Upload CSV", type=['directory'])
    # if output_folder != settings["output_folder"]:
    #     Path(output_folder).mkdir(parents=True, exist_ok=True)
    #     update_setting("output_folder", output_folder)

    
    # with st.form("settings_form"):
    st.subheader("Output Options")
    # ---- Data Format ----
    data_format = st.selectbox(
        "Data Export Format",
        ["csv", "excel"],
        index=["csv", "excel"].index(settings["data_format"])
    )
    
        
    # ---- Image Format ----
    image_format = st.selectbox(
        "Image File Format",
        ["png", "jpeg", "tiff"],
        index=["png", "jpeg", "tiff"].index(settings["image_format"])
    )
    
        
    # ---- Video Format ----
    video_format = st.selectbox(
        "Video File Format",
        ["gif", "mp4"],
        index=["gif", "mp4"].index(settings["video_format"])
    )
    


    # st.subheader("Units")

    # units = st.radio(
    #     "Units System",
    #     ["metric", "imperial"],
    #     index=["metric", "imperial"].index(settings["units"])
    # )
    

    st.subheader("Appearance")

    theme = st.radio(
        "Theme",
        ["light", "dark"],
        index=["light", "dark"].index(settings["theme"])
    )
    
    # st.subheader("Advanced Settings")
    # plot_color = st.color_picker("Plotting Color")
    
    if st.button("Save Settings"):
        # if data_format != settings["data_format"]:
        #     update_setting("data_format", data_format)
        
        # if image_format != settings["image_format"]:
        #     update_setting("image_format", image_format)
        
        # if video_format != settings["video_format"]:
        #     update_setting("video_format", video_format)
        
        # if units != settings["units"]:
        #     update_setting("units", units)
            
        # if theme != settings["theme"]:
        #     update_setting("theme", theme)
        #     # update_toml(theme)
        
        with st.spinner("Please wait..."):
            save_settings(settings)
        st.success("Settings saved.")
        # st.rerun()
        # print("Settings saved.")
        # print("New settings:", settings)
