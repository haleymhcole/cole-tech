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
    st.title("Help & Documentation")
    st.write("""
    - **How to use the app**
    - **What the models mean**
    - **Data sources**
    - **FAQs**
    """)


