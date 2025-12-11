#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  8 21:24:28 2025

@author: haleycole
"""
import numpy as np
from datetime import datetime, timedelta

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

def get_trend(y):
    # Get last X days worth, find general trend.
    # Note that 1 row of data = 1 day. 
    x = np.arange(1, len(y)+1)
    y_ave = moving_average_np(y, 30)
    x_ave = x[15:-14]
    
    # Fit the general trendline.
    
    # # Fit a linear trend (degree = 1)
    # coefficients_linear = np.polyfit(x, y_ave, 1)
    # linear_trend = np.poly1d(coefficients_linear)
    
    # Fit a quadratic trend (degree = 2)
    coefficients_quadratic = np.polyfit(x_ave, y_ave, 2)
    quadratic_trend = np.poly1d(coefficients_quadratic)
    
    return quadratic_trend

if __name__ == "__main__":
    # from core.real_time import get_data
    # # Debugging. Check forecast/trendline model.
    # sw_data, current_datetime, agos, now_properties = get_data()
    # var_name = now_properties["Sunspot Number"][0]
    # data_range = sw_data.loc[current_datetime - timedelta(days=90):current_datetime]
    
    # #trendline = forecast(data_range.index, data_range[var_name])
    
    # y = data_range[var_name].values
    # x = np.arange(1, len(y)+1)
    # trendline = get_trend(x,y)
    
from datetime import datetime, timedelta
import spaceweather as sw  
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
sw_data = sw.celestrak.sw_daily(update=True)
sw_data.index = pd.to_datetime(sw_data.index)
current_datetime = datetime.utcnow()
current_data = sw_data.loc[:current_datetime].iloc[-1]
data = sw_data.loc[current_datetime - timedelta(weeks=45):current_datetime]
plt.figure(figsize=(10,5))
plt.scatter(data.index, data['isn'])

y = data['isn']
x = np.arange(1, len(y)+1)
window_size = 30
weights = np.ones(window_size) / window_size
y_ave = np.convolve(y, weights, mode='valid')
x_ave = x[15:-14]
plt.plot(data.index[15:14], y_ave)

plt.show()
plt.close()

