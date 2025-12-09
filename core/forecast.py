#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 21:24:28 2025

@author: haleycole
"""
import numpy as np

def moving_average_np(data, window_size):
    """
    Calculates the simple moving average of a 1D array using numpy.convolve.

    Args:
        data (np.array): The input array.
        window_size (int): The size of the moving average window.

    Returns:
        np.array: The array containing the moving average.
    """
    weights = np.ones(window_size) / window_size
    return np.convolve(data, weights, mode='valid')

def forecast(x, y):
    # Get last X days worth, find general trend.
    # Note that 1 row of data = 1 day. 
    y_ave = moving_average_np(y, 30)
    
    # Fit the general trendline.
    
    # # Fit a linear trend (degree = 1)
    # coefficients_linear = np.polyfit(x, y_ave, 1)
    # linear_trend = np.poly1d(coefficients_linear)
    
    # Fit a quadratic trend (degree = 2)
    coefficients_quadratic = np.polyfit(x, y_ave, 2)
    quadratic_trend = np.poly1d(coefficients_quadratic)
    
    return quadratic_trend