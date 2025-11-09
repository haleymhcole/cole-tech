# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 07:24:13 2025

@author: haley
"""
import os

class colors:
    violet = "#645c9f"
    light_periwinkle = "#CCCCFF"
    light_plum = "#bc90ba"
    dark_plum = "#563256"
    light_gray = "#dedbdb"
    white = "#ffffff"
    yellow = "#eed102"
    black = "#191319"
    darkblue = "darkblue"
    lightest_purple = "#faf0ff"
    
    window_bg = white
    panel_bg = lightest_purple 
    h1 = dark_plum
    h2 = light_plum
    body = black 
    btn_bg = black # dark_plum
    btn_text = white
        
class fonts:
    h1 = ("Arial", 24, 'bold')
    h2 = ("Arial", 10)
    btn = ("Arial", 12, 'bold')
    
    
class images:
    logo = os.path.join("Images", "logo.png") # Replace with your image file path
    