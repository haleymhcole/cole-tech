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
    st.write("Select forecast window:")
    window = st.selectbox("Window", ["1 Day", "3 Day", "7 Day", "30 Day"])