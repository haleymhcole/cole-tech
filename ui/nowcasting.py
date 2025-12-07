#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 15:40:48 2025

@author: haleycole
"""
import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np

def render():
    # --- Main Page Content ---
    st.title("Nowcasting")
    
    st.subheader("Select your environment...")
    st.write("Controls for real-time data.")
    refresh_rate = st.slider("Refresh interval (min)", 1, 60, 5)
    
    
    # --- User Inputs ---
    st.header("User Inputs")
    date = st.date_input("Date", dt.datetime.now())
    time = st.time_input("Time", dt.datetime.now().time())
    location = st.text_input("Location", "Boulder, CO")

    st.write(f"### Selected time: {date} {time}")
    st.write(f"### Location: {location}")

    # --- Example fake transmission values ---
    # Replace this with real atmospheric/space weather model later
    wavelengths = np.linspace(200, 1000, 100)
    transmission = np.exp(-0.002 * (wavelengths - 600)**2)

    df = pd.DataFrame({"Wavelength (nm)": wavelengths, "Transmission": transmission})

    st.line_chart(df, x="Wavelength (nm)", y="Transmission")