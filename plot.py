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

sns.set_style('darkgrid')

def open_figure_popup(result, Rc):
    # Create the Toplevel window for the pop-up
    popup = tk.Toplevel()
    popup.title("Figure Pop-up")
    popup.geometry("600x500")

    # Create a Matplotlib figure and axes
    fig, ax = plt.subplots(figsize=(6,5))
    ax.clear()
    ax.plot(result["R"], result["T"], label="Transmission Function")
    ax.axvline(Rc, color='r', linestyle='--', label=f"Rc = {Rc:.2f} GV")
    ax.set_title("Geomagnetic Transmission Function")
    ax.set_xlabel("Rigidity [GV]")
    ax.set_ylabel("Transmission T(R)")
    ax.legend()
    ax.grid(True)
    plt.tight_layout(pad=3)

    # Embed the Matplotlib figure into the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=popup)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()

    # Optional: Add a close button
    close_button = ttk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=10)
    
    
    # # Show loading message and launch Kp fetch in background
    # self.loading_label.config(text="Fetching Kp index from GFZ...")
    # thread = threading.Thread(target=self.fetch_and_update_kp, args=(date, Rc))
    # thread.daemon = True
    # thread.start()
    
    
    
    
    