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
from core import real_time

def render():
    # --- Main Page Content ---
    st.title("Forecasting")
    st.write("Select forecast window:")
    # window = st.selectbox("Window", ["1 Day", "3 Day", "7 Day", "30 Day"])
    
    sw_data, current_datetime, agos, properties = real_time.get_data() # TODO: Avoid repeating this function (currently also in dashboard.py for real-time stats) and benchmarking for historical
    
    
    st.subheader("📈 Forecasting")
    selected_option = "Ap"
    fig = real_time.plot(sw_data, current_datetime, "Forecasting", agos[2], selected_option, properties[selected_option])
    st.plotly_chart(fig, use_container_width=True)
    
    