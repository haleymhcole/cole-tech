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
    

def open_popup_to_side():
    # Get parent window's position and size
    parent_x = root.winfo_x()
    parent_y = root.winfo_y()
    parent_width = root.winfo_width()

    # Calculate pop-up window's position (to the right of the parent)
    popup_x = parent_x + parent_width
    popup_y = parent_y # Align top edges

    # Create the Toplevel window
    popup_window = tk.Toplevel(root)
    popup_window.title("Pop-up Window")

    # Set the geometry of the pop-up window
    # Example: 200x150 pixels, positioned at popup_x, popup_y
    popup_window.geometry(f"200x150+{popup_x}+{popup_y}")

    # Add content to the pop-up window
    tk.Label(popup_window, text="This is a pop-up!").pack(pady=20)
    tk.Button(popup_window, text="Close", command=popup_window.destroy).pack()

# # Create the main window
# root = tk.Tk()
# root.title("Main Window")
# root.geometry("400x300") # Initial size for the main window

# # Button to open the pop-up
# open_button = tk.Button(root, text="Open Pop-up", command=open_popup_to_side)
# open_button.pack(pady=50)

# root.mainloop()
    
    
    