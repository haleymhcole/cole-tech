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

from ui import home
from ui import dashboard
from ui import settings
from ui import nowcasting
from ui import forecasting
from ui import benchmarking
from ui import feedback
from ui import help_docs

# Style
from palette import PALETTE
from theme_sync import sync_theme
sync_theme()

st.set_page_config(
    page_title="Space Weather Demo", 
    page_icon=os.path.join("assets", "favicon.png"),
    layout="wide"
    )

if "argos_on" not in st.session_state:
    st.session_state.argos_on = False

#st.title("Real-Time Space Weather Demo")

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #e3e4ef; 
        max-width: 250px; 
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
    
    
    /* Style for H1 titles 
    h1 {
        color: #1A5276; 
        font-family: 'Arial', sans-serif;
        font-size: 36px;
    }
    */
    /* Style for general body text */
    p {
        color: #333333; /* Dark Gray 
        font-family: 'Georgia', serif;
        font-size: 16px;
        */
    }
    
    
    /* Tertiary button style -- Target the specific button by its key or type 
    div[data-testid="stButton"] button[data-testid="stButton-tertiary"] 
    .stButton button[data-testid="stButtonTertiary"] 
    div[data-baseweb="button"] > div > button[kind="tertiary"] */
    
    .stButton button[data-testid="stButtonTertiary"]  {
        background-color: #acb0ca;
        color: red !important; /* Text color */
        border-radius: 8px; /* Optional: Add some roundness */
        font-size: 7;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

logo_file = os.path.join("assets", "logo.png")
st.sidebar.image(logo_file) #, caption='Equinox Technologies logo')


# # Start on home page.
# home.render()


st.sidebar.subheader("Main Tools")

MAIN_PAGES = {
    "Home": home,
    "Dashboard": dashboard,
    "Nowcasting": nowcasting,
    #"Forecasting": forecasting,
    "Historical Benchmarking": benchmarking,
}

SECOND_PAGES = {
    "Settings": settings,
    "Submit Feedback":feedback,
    "Help":help_docs,
}

def init_session_state():
    defaults = {
        "active_menu": "Home",
        # "theme": "dark",
        # "output_dir": None,
        # "units": "metric",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()


# --------------------------
# SECONDARY OPTIONS
# --------------------------


for p in MAIN_PAGES:
    if st.sidebar.button(p): # , type='primary'
        st.session_state.active_menu = p
        

st.sidebar.subheader("More")
for p in SECOND_PAGES:
    if st.sidebar.button(p): # , type='tertiary'
        st.session_state.active_menu = p
    
st.sidebar.markdown("---")



c1, c2, c3 = st.columns([3,2,1])
with c1:
    st.sidebar.header("🌟 Insight Engine: Argos")
    # # Markdown is supported within the help text
    # multi_line_help = """
    # **Markdown is supported!**
    # * Use bullet points
    # * Add **bold** or *italics*
    # """
    # st.number_input("Select a number", help=multi_line_help)
    
    st.sidebar.write("""
             ***Flip Argos ON to transform your workspace into a deep diagnostic suite.***\n
             """)

with c2:
    argos_help = "With Argos, your data comes alive through an operational insight engine with advanced analytics that revealing the why behind every number and turning raw metrics into actionable intelligence."
    
    # pro_on = st.toggle("Paid Subscription")
    argos_on = st.sidebar.toggle("Activate Argos", help=argos_help)
    
    if argos_on:
        pro_on = True
        st.sidebar.write("Insight engine activated ✨")
        #stars()
        st.balloons()
        
        if "argos_on" not in st.session_state:
            st.session_state.argos_on = True
        


all_pages = MAIN_PAGES | SECOND_PAGES

for page_name in all_pages:
    if st.session_state.active_menu == page_name:
        all_pages[page_name].render()





