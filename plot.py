# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 06:56:37 2025

@author: haley
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from visual_design_elements import colors, fonts, images
import spaceweather as sw
from tkinter import messagebox
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime, timedelta

# sns.set_style('darkgrid')

def open_figure_popup(root):
    # Get parent window's position and size
    parent_x = root.winfo_x()
    parent_y = root.winfo_y()
    parent_width = root.winfo_width()

    # Calculate pop-up window's position (to the right of the parent)
    popup_x = parent_x + parent_width
    popup_y = parent_y # Align top edges
    
    # Create the Toplevel window for the pop-up
    popup = tk.Toplevel()
    popup.title("GTF Plotting Window")
    #popup.geometry("600x500")
    
    # Set the geometry of the pop-up window
    popup.geometry(f"600x500+{popup_x}+{popup_y}")
    
    # Update rcParams to set the default text color
    plt.rcParams.update({
        'text.color': colors.plot_text,
        'axes.labelcolor': colors.plot_text,  # For axis labels
        'xtick.color': colors.plot_axes,      # For x-axis tick labels
        'ytick.color': colors.plot_axes       # For y-axis tick labels
    })
    
    return popup

def finalize_popup(fig, popup):
    # Embed the Matplotlib figure into the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=popup)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()
    
    # Optional: Add a close button
    close_button = ttk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)
    return popup


def plot_kp(root, time_frame):
    popup = open_figure_popup(root)
    
    # --- Load and slice the data ---
    sw_data = sw.celestrak.sw_daily(update=True)
    
    # Ensure datetime index
    sw_data.index = pd.to_datetime(sw_data.index)
    
    current_datetime = datetime.utcnow()
    one_week_ago = current_datetime - timedelta(weeks=1)
    one_month_ago = current_datetime - timedelta(days=30)
    
    if time_frame == "Week":
        ago = one_week_ago
    elif time_frame == "Month":
        ago = one_month_ago
    else:
        messagebox.showerror("Error", "Invalid time frame selected for Kp trend.")
    
    # Filter data for the last week
    data_range = sw_data.loc[ago:current_datetime]
    
    # Extract datetime and Kp
    times = data_range.index
    kp_values = data_range["Kp0"].astype(float)  # make sure it's numeric
    
    # --- Plot ---
    fig = plt.figure(figsize=(6,5))
    scatter = plt.scatter(
        times,
        kp_values,
        c=kp_values,
        cmap="RdYlGn_r",  # reversed so low=green, high=red
        s=50,
        edgecolor="k",
        zorder=10
    )
    
    # Colorbar
    #cbar = plt.colorbar(scatter)
    #cbar.set_label("Kp Index", fontsize=12)
    
    # Axes and formatting
    plt.title(f"Kp Index — Past {time_frame}", fontsize=14)
    plt.ylabel("Kp Value")
    plt.xlabel("Date (UTC)")
    plt.ylim(0, 9)
    plt.grid(True, linestyle="--", alpha=0.5)
    
    # Format date axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    plt.xticks(rotation=45)
    plt.tight_layout(pad=3)
    plt.close(fig)
    
    finalize_popup(fig, popup)
    
    
def plot_gtf(root, result, Rc, make_gif):
    popup = open_figure_popup(root)

    if make_gif:
        frames = []
    
    # Create a Matplotlib figure and axes
    fig, ax = plt.subplots(figsize=(6,5))
    ax.clear()
    ax.plot(result["R"], result["T"], label="Transmission Function")
    ax.axvline(Rc, color='r', linestyle='--', label=f"Rc = {Rc:.2f} GV")
    ax.set_title("Geomagnetic Transmission Function", fontweight='bold')
    ax.set_xlabel("Rigidity [GV]", fontweight='bold')
    ax.set_ylabel("Transmission T(R)", fontweight='bold')
    ax.legend()
    ax.grid(True, ls='dashed', color=colors.plot_grid)
    
    # Access and modify all spines
    # You can iterate through the ax.spines dictionary to access each spine
    for spine in ['left', 'right', 'top', 'bottom']:
        ax.spines[spine].set_color(colors.plot_spines)
        ax.spines[spine].set_linewidth(1)
        # ax.spines['top'].set_visible(False) # Hide top spine
    
    plt.tight_layout(pad=3)

    # if make_gif:
    #     frames.append(filename)
        
    plt.close(fig)

    finalize_popup(fig, popup)
    