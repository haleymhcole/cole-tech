#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 20:44:23 2025

@author: haleycole
"""
import pandas as pd

def load_CME_DB():
    file = "CDAW_CME_Catalog_Processed.csv"
    return pd.read_csv(file)