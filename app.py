#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 09:28:21 2025

@author: haleycole
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
from palette import PALETTE
from theme_sync import sync_theme
sync_theme()

st.set_page_config(page_title="Space Weather Demo", layout="wide")

#st.title("Real-Time Space Weather Demo")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #e3e4ef; 
        /* color: #ffffff; */
        
        .stButton button {
            /* color: #7f97e3 !important; */
            background-color: #ffffff; 
            border-color: #acb0ca;
            border-style: solid;
        }
        
         .stButton button:hover {
          /* background-color: #e8c496; Background color on hover */
          box-shadow: 0px 10px 15px rgba(0, 0, 0, 0.3);
          transform: translateY(-3px); /* Slight lift on hover */
        }
         
        .stButton button:focus {
            color: #000000;
            font-weight: bold;
            border-color: #e4a43d;
            background-color: #f8ebdb;
            }
        
    }
    </style>
    """,
    unsafe_allow_html=True
)



# --- Initialize session state ---
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "home"


logo_file = os.path.join("Images", "logo.png")
st.sidebar.image(logo_file) #, caption='Equinox Technologies logo')


# --- Sidebar Navigation ---
# st.sidebar.title("Navigation")


def nav_button(name):
    if st.sidebar.button(name):
        st.session_state.active_menu = name

nav_button("Home")
nav_button("Nowcasting")
nav_button("Forecasting")
nav_button("Historical Benchmarking")
nav_button("Settings")
nav_button("Submit Feedback")
nav_button("Help")

st.sidebar.markdown("---")

# --- Render sub-menu content in the sidebar ---
menu_selection = st.session_state.active_menu


def add_title(menu_selection):
    st.title(f"{menu_selection}")
    #st.write(f"This is the **{menu_selection}** page.")

if menu_selection == "Home":
    st.title("Space Weather Insights — Real-Time Monitoring, Smarter Forecasting")
    # st.write("Welcome to the main dashboard.")
    st.write("Track sunspots, CMEs, geomagnetic conditions, and predictive indicators **all in one place**.")
    
    # Launch Dashboard (free)
    # Unlock Pro Tools (links to pricing / comparison page)

elif menu_selection == "Settings":
    add_title(menu_selection)
    theme = st.selectbox("Theme", ["Light", "Dark"])
    units = st.radio("Units", ["Metric", "Imperial"])
    st.write("Additional settings here...")

elif menu_selection == "Nowcasting":
    # --- Main Page Content ---
    add_title(menu_selection)
    
    st.subheader("Select your environment...")
    st.write("Controls for real-time data.")
    refresh_rate = st.slider("Refresh interval (min)", 1, 60, 5)
    
    
    # --- User Inputs ---
    st.header("User Inputs")
    date = st.date_input("Date", datetime.now())
    time = st.time_input("Time", datetime.now().time())
    location = st.text_input("Location", "Boulder, CO")

    st.write(f"### Selected time: {date} {time}")
    st.write(f"### Location: {location}")

    # --- Example fake transmission values ---
    # Replace this with real atmospheric/space weather model later
    wavelengths = np.linspace(200, 1000, 100)
    transmission = np.exp(-0.002 * (wavelengths - 600)**2)

    df = pd.DataFrame({"Wavelength (nm)": wavelengths, "Transmission": transmission})

    st.line_chart(df, x="Wavelength (nm)", y="Transmission")


elif menu_selection == "Forecasting":
    add_title(menu_selection)
    st.write("Select forecast window:")
    window = st.selectbox("Window", ["1 Day", "3 Day", "7 Day", "30 Day"])

elif menu_selection == "Historical Benchmarking":
    add_title(menu_selection)
    start = st.date_input("Start Date")
    end = st.date_input("End Date")
    st.write("Upload comparison data:")
    st.file_uploader("Upload CSV", type=["csv"])

elif menu_selection == "Submit Feedback":
    add_title(menu_selection)
    name = st.text_input("Name (optional)")
    feedback = st.text_area("Your Feedback")
    if st.button("Submit"):
        st.success("Thank you — feedback submitted!")

elif menu_selection == "Help":
    st.subheader("Help & Documentation")
    st.write("""
    - **How to use the app**
    - **What the models mean**
    - **Data sources**
    - **FAQs**
    """)

















