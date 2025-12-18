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

favicon = os.path.join("assets", "favicon.png")

st.set_page_config(
    page_title="Space Weather Demo", 
    page_icon=favicon,
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

# import base64
# def get_img_with_href(local_img_path, target_url):
#     # Encode local image to base64 string
#     with open(local_img_path, "rb") as f:
#         data = f.read()
#     encoded = base64.b64encode(data).decode()

#     # Construct the Markdown with embedded HTML for the link
#     img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
#     markdown = f'<a href="{target_url}"><img src="data:image/{img_format};base64,{encoded}" width="200"></a>'
#     return markdown

home_url = "http://localhost:8501"

tech_logo_file = os.path.join("assets", "logo.png")
app_logo_file = os.path.join("assets", "SWAN-logo.png")

#st.sidebar.markdown(get_img_with_href(app_logo_file, home_url), unsafe_allow_html=True)
#st.write("Click the image above to visit the page!")


# def clickable_image_in_same_tab(image_url, target_url, caption=None):
#     """
#     Displays a clickable image that opens a link in the same browser tab.

#     Args:
#         image_url (str): The URL or path to the image.
#         target_url (str): The URL to navigate to when the image is clicked.
#         caption (str, optional): A caption for the image. Defaults to None.
#     """
#     html_code = f"""
#     <a href="{target_url}" target="_self">
#         <img src="{image_url}" alt="Clickable Image" style="cursor: pointer; max-width: 100%; height: auto;">
#     </a>
#     """
#     st.markdown(html_code, unsafe_allow_html=True)
#     if caption:
#         st.caption(caption)

# # Example usage with an external image and link:
# clickable_image_in_same_tab(app_logo_file, home_url, caption="Visit Streamlit website")



st.sidebar.image(app_logo_file) #, caption='Equinox Technologies logo')

# # Add the logo to the sidebar and make it clickable
# st.logo(
#     image=app_logo_file,  # Replace with the path to your logo file
#     link=home_url,                 # The URL to navigate to when clicked
#     icon_image=favicon, # Optional: A smaller icon for when sidebar is closed
#     size='large'
# )

# # Start on home page.
# home.render()


# st.sidebar.subheader("Main Tools")

MAIN_PAGES = {
    "Home": home,
    "Dashboard": dashboard,
    #"Nowcasting": nowcasting,
    #"Forecasting": forecasting,
    #"Historical Benchmarking": benchmarking,
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

        

# # Define options for the dropdown
# options = ["Option A", "Option B", "Option C"]

# # Create the selectbox
# selection = st.sidebar.selectbox("Choose an action:", options)

# # Use an if/elif/else block to handle the selection
# if selection == "Option A":
#     st.sidebar.write("You selected Option A! Performing action A...")
#     st.sidebar.button("Action A Button") # This button appears after selection
# elif selection == "Option B":
#     st.sidebar.write("You selected Option B! Performing action B...")
#     st.sidebar.button("Action B Button")
# elif selection == "Option C":
#     st.sidebar.write("You selected Option C! Performing action C...")
#     st.sidebar.button("Action C Button")
    

# st.page_link(home.render(), label="Home", icon="🏠") 
# st.page_link("ui//settings.py", label="Settings", icon="⚙️") 
# st.page_link("ui//help_doc.py", label="Help", icon="📄") 
#st.markdown("Check out the official [Streamlit documentation](docs.streamlit.io)!")

    
#st.sidebar.markdown("---")



c1, c2, c3 = st.columns([3,2,1])
with c1:
    st.sidebar.header("🌟 Insight Engine")
    # # Markdown is supported within the help text
    # multi_line_help = """
    # **Markdown is supported!**
    # * Use bullet points
    # * Add **bold** or *italics*
    # """
    # st.number_input("Select a number", help=multi_line_help)
    
    # st.sidebar.write("""
    #          ***Flip Argos ON to transform your workspace into a deep diagnostic suite.***\n
    #          """)

with c2:
    argos_help = "With SWAN Premium, your data comes alive through an operational insight engine with advanced analytics that reveals the why behind every number and turns raw metrics into actionable intelligence."
    
    # pro_on = st.toggle("Paid Subscription")
    argos_on_toggle = st.sidebar.toggle("Activate SWAN Premium", help=argos_help)
    
    if argos_on_toggle:
        pro_on = True
        st.sidebar.write("Insight engine activated ✨")
        
        if not st.session_state.argos_on:
            # Only show balloons if changing the status.
            st.balloons()
        
        st.session_state.argos_on = True
        

st.sidebar.markdown("---")

for p in MAIN_PAGES:
    if st.sidebar.button(p): # , type='primary'
        st.session_state.active_menu = p

#st.sidebar.subheader("More")
for p in SECOND_PAGES:
    if st.sidebar.button(p): # , type='tertiary'
        st.session_state.active_menu = p





all_pages = MAIN_PAGES | SECOND_PAGES

for page_name in all_pages:
    if st.session_state.active_menu == page_name:
        all_pages[page_name].render()


st.sidebar.markdown("---")
st.sidebar.image(tech_logo_file) #, caption='Equinox Technologies logo')


