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

# sns.set_style('darkgrid')

def open_figure_popup(root, result, Rc):
    # Get parent window's position and size
    parent_x = root.winfo_x()
    parent_y = root.winfo_y()
    parent_width = root.winfo_width()

    # Calculate pop-up window's position (to the right of the parent)
    popup_x = parent_x + parent_width
    popup_y = parent_y # Align top edges
    
    # Create the Toplevel window for the pop-up
    popup = tk.Toplevel()
    popup.title("Figure Pop-up")
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

    # Embed the Matplotlib figure into the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=popup)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()

    # Optional: Add a close button
    close_button = ttk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)
    
    