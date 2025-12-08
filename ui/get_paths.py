#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  7 20:54:00 2025

@author: haleycole
"""
from pathlib import Path

def get_root():
    # Path to project root (one directory up from ui/)
    ROOT = Path(__file__).resolve().parents[1]
    #DATA_DIR = os.path.join(ROOT, "data")
    return ROOT