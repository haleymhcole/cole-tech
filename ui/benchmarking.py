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
    st.title("Historical Benchmarking")
    
    start = st.date_input("Start Date")
    end = st.date_input("End Date")
    st.write("Upload comparison data:")
    st.file_uploader("Upload CSV", type=["csv"])