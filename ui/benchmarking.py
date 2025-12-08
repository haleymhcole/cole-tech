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
#from data import load_data
# from get_paths import get_root
import os

from pathlib import Path

def get_root():
    # Path to project root (one directory up from ui/)
    ROOT = Path(__file__).resolve().parents[1]
    #DATA_DIR = os.path.join(ROOT, "data")
    return ROOT

def swap_boolean_for_check(x):
    # Swap 1s and 0s (or True and False) for ✔ check marks.
    if x:
        return "✓"
    else:
        return ""

def render():
    # --- Main Page Content ---
    st.title("Historical Benchmarking")
    
    start = st.date_input("Start Date")
    end = st.date_input("End Date")
    st.write("Upload comparison data:")
    st.file_uploader("Upload CSV", type=["csv"])
    
    # CME Database
    ROOT = get_root()
    cme_db_file = os.path.join(ROOT, "data", "CDAW_CME_Catalog_Processed.csv")
    cme_db = pd.read_csv(cme_db_file)
    cme_db.drop(['2nd-order Speed at final height [km/s]',
                 '2nd-order Speed at 20 Rs [km/s]'], axis=1, inplace=True)
    
    cme_db['Mild Event'] = cme_db['Mild Event'].apply(swap_boolean_for_check)
    cme_db['Measurement Difficulties'] = cme_db['Measurement Difficulties'].apply(swap_boolean_for_check)
    
    
    num_rows = st.slider("Number of rows", 1, 100, 25)
    np.random.seed(42)
    data = []
    
    config = {
    #     #"Preview": st.column_config.ImageColumn(),
    #     "Linear Speed [km/s]": st.column_config.ProgressColumn(),
    }
    
    if st.toggle("Enable editing"):
        edited_data = st.data_editor(cme_db, column_config=config, use_container_width=True)
    else:
        st.dataframe(cme_db, column_config=config, use_container_width=True)


