#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 05:39:16 2025

@author: haleycole
"""

# GUI.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from GTF import get_GTF

class GTFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Geomagnetic Transmission Function Viewer")
        self.root.geometry("600x600")

        # --- Input Frame ---
        frame = ttk.LabelFrame(root, text="Input Parameters", padding=10)
        frame.pack(padx=10, pady=10, fill="x")

        # Latitude
        ttk.Label(frame, text="Latitude (°):").grid(row=0, column=0, sticky="e")
        self.lat_entry = ttk.Entry(frame)
        self.lat_entry.insert(0, "40.0")
        self.lat_entry.grid(row=0, column=1)

        # Longitude
        ttk.Label(frame, text="Longitude (°):").grid(row=1, column=0, sticky="e")
        self.lon_entry = ttk.Entry(frame)
        self.lon_entry.insert(0, "-105.3")
        self.lon_entry.grid(row=1, column=1)

        # Altitude
        ttk.Label(frame, text="Altitude (km):").grid(row=2, column=0, sticky="e")
        self.alt_entry = ttk.Entry(frame)
        self.alt_entry.insert(0, "1.6")
        self.alt_entry.grid(row=2, column=1)

        # Date/time
        ttk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, sticky="e")
        self.date_entry = ttk.Entry(frame)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=3, column=1)

        # Compute button
        compute_btn = ttk.Button(frame, text="Compute GTF", command=self.compute_gtf)
        compute_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # --- Output Frame ---
        self.output_frame = ttk.LabelFrame(root, text="Results", padding=10)
        self.output_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.output_label = ttk.Label(self.output_frame, text="Enter values and press Compute GTF")
        self.output_label.pack()

        # --- Plot area ---
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.output_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def compute_gtf(self):
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
            alt = float(self.alt_entry.get())
            date_str = self.date_entry.get()
            date = datetime.strptime(date_str, "%Y-%m-%d")

            result = get_GTF(lat, lon, alt, date)

            Rc = result["Rc"][0]
            lam = result["geomag_lat"][0]

            # Update label
            self.output_label.config(text=f"Geomagnetic lat: {lam:.2f}°,  Rc: {Rc:.2f} GV")

            # Plot
            self.ax.clear()
            self.ax.plot(result["R"], result["T"], label="Transmission Function")
            self.ax.axvline(Rc, color='r', linestyle='--', label=f"Rc = {Rc:.2f} GV")
            self.ax.set_xlabel("Rigidity [GV]")
            self.ax.set_ylabel("Transmission T(R)")
            self.ax.set_title("Geomagnetic Transmission Function")
            self.ax.legend()
            self.ax.grid(True)
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", f"Could not compute GTF:\n{e}")

# --- Run the GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = GTFApp(root)
    root.mainloop()
