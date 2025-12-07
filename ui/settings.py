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
    st.title("Settings")
    theme = st.selectbox("Theme", ["Light", "Dark"])
    units = st.radio("Units", ["Metric", "Imperial"])
    st.write("Additional settings here...")