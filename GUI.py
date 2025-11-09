# GUI.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
import threading
from GTF import get_GTF
from GUI_screenshot import take_window_screenshot
from plot import open_figure_popup
from visual_design_elements import colors, fonts, images
from PIL import Image, ImageTk

# -------------------------------------------------------
# Helper function: fetch Kp index
# -------------------------------------------------------
def fetch_kp_index(date_time):
    """
    Fetch the 3-hour planetary Kp index for the given datetime (UTC).
    Returns float Kp or None if failed.
    Uses GFZ Helmholtz Centre API.
    """
    ts = date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"https://kp.gfz.de/app/json/?start={ts}&end={ts}&index=Kp"

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if "data" in data and len(data["data"]) > 0:
            val = float(data["data"][0]["value"])
            return val
        else:
            return None
    except Exception as e:
        print("Error fetching Kp index:", e)
        return None


# -------------------------------------------------------
# GUI Application Class
# -------------------------------------------------------
class GTFApp:
    def __init__(self, root):
        # Create a Style object
        s = ttk.Style()
        
        # Configure the "TLabelframe" style to set the background color
        # You can choose any valid color name or hex code
        s.configure("TLabelframe", background=colors.panel_bg, foreground=colors.h1, font=fonts.h1) 
        s.configure("TransparentLabel.TLabel", background=colors.panel_bg, foreground=colors.h1, font=fonts.h2)
        s.configure("TButton", background=colors.btn_bg,  foreground=colors.dark_plum, font=fonts.btn) #, activebackground="lightgreen", activeforeground="black")
        #s.map("TButton", background=[('active', 'pink')]) # Optional: change color on hover
        s.configure("h1.TLabelframe", bg='pink') # , bg=colors.panel_bg, fg=colors.h1, font=fonts.h1) 

        self.root = root
        self.root.title("Geomagnetic Transmission Function (GTF) Calculator")
        self.root.geometry("650x550")
        
        # Set the background color of the window
        # Can use color names (e.g., "blue", "lightpink")
        # or hexadecimal color codes (e.g., "#FF0000" for red)
        root.configure(bg=colors.window_bg) 

        # --- Input Frame ---
        frame = ttk.LabelFrame(root, text="Input Parameters", padding=10, style='h1.TLabelframe')
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Latitude
        ttk.Label(frame, text="Latitude (°):", style="TransparentLabel.TLabel").grid(row=0, column=0, sticky="e")
        self.lat_entry = ttk.Entry(frame)
        self.lat_entry.insert(0, "40.0")
        self.lat_entry.grid(row=0, column=1)

        # Longitude
        ttk.Label(frame, text="Longitude (°):", style="TransparentLabel.TLabel").grid(row=1, column=0, sticky="e")
        self.lon_entry = ttk.Entry(frame)
        self.lon_entry.insert(0, "-105.3")
        self.lon_entry.grid(row=1, column=1)

        # Altitude
        ttk.Label(frame, text="Altitude (km):", style="TransparentLabel.TLabel").grid(row=2, column=0, sticky="e")
        self.alt_entry = ttk.Entry(frame)
        self.alt_entry.insert(0, "1.6")
        self.alt_entry.grid(row=2, column=1)

        # Date/time
        ttk.Label(frame, text="Date (YYYY-MM-DD):", style="TransparentLabel.TLabel").grid(row=3, column=0, sticky="e")
        self.date_entry = ttk.Entry(frame)
        self.date_entry.insert(0, datetime.utcnow().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=3, column=1)

        ttk.Label(frame, text="Time (HH:MM, UTC):", style="TransparentLabel.TLabel").grid(row=4, column=0, sticky="e")
        self.time_entry = ttk.Entry(frame)
        self.time_entry.insert(0, datetime.utcnow().strftime("%H:%M"))
        self.time_entry.grid(row=4, column=1)

        # Optional manual Kp input
        ttk.Label(frame, text="Manual Kp (optional):", style="TransparentLabel.TLabel").grid(row=5, column=0, sticky="e")
        self.kp_entry = ttk.Entry(frame)
        self.kp_entry.grid(row=5, column=1)

        # Compute button
        compute_btn = ttk.Button(frame, text="Compute GTF", command=self.compute_gtf, style="TButton")
        compute_btn.grid(row=6, column=0, columnspan=2, pady=10)

        # --- Output Frame ---
        self.output_frame = ttk.LabelFrame(root, text="Analysis", padding=10)
        self.output_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.output_label = ttk.Label(self.output_frame, text="Enter values and press Compute GTF", style="TransparentLabel.TLabel")
        self.output_label.pack()

        # Kp & environment results
        self.kp_label = ttk.Label(self.output_frame, text="Kp Index: --", font=("Helvetica", 10), style="TransparentLabel.TLabel")
        self.kp_label.pack(pady=2)
        self.severity_label = ttk.Label(self.output_frame, text="Environment Level: --",
                                        font=("Helvetica", 12, "bold"), style="TransparentLabel.TLabel")
        self.severity_label.pack(pady=(0, 10))

        # # --- Plot area ---
        # self.fig, self.ax = plt.subplots(figsize=(8,6), dpi=300)
        # self.canvas = FigureCanvasTkAgg(self.fig, master=self.output_frame)
        # self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # canvas_widget = self.canvas.get_tk_widget()
        # canvas_widget.config(width=600, height=400)
        # canvas_widget.pack()


        # Loading label for async updates
        self.loading_label = ttk.Label(self.output_frame, text="", foreground="gray")
        self.loading_label.pack(pady=(5, 0))


        logo = Image.open(images.logo)
        logo.thumbnail((100,100), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(logo)
        image_label = ttk.Label(root, image=tk_image)
        image_label.pack()
        # Place the image in the lower-right corner
        # rely=1.0 and relx=1.0 position the anchor point at the bottom-right of the parent
        # anchor=tk.SE sets the anchor of the image_label itself to its southeast corner
        image_label.place(rely=1.0, relx=1.0, anchor=tk.SE)
        
        # Keep a reference to the image to prevent garbage collection
        image_label.image = tk_image 
        
    # ---------------------------------------------------
    # Main compute routine
    # ---------------------------------------------------
    def compute_gtf(self):
        try:
            lat = float(self.lat_entry.get())
            lon = float(self.lon_entry.get())
            alt = float(self.alt_entry.get())
            date_str = self.date_entry.get().strip()
            time_str = self.time_entry.get().strip()
            dt_str = f"{date_str} {time_str}"
            date = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")

            # Compute GTF (fast local)
            result = get_GTF(lat, lon, alt, date)
            Rc = result["Rc"][0]
            lam = result["geomag_lat"][0]

            # # Fetch Kp index automatically
            # kp_val = fetch_kp_index(date)
            # if kp_val is None:
            #     # fallback to manualFGTF
            #     try:
            #         kp_val = float(self.kp_entry.get())
            #     except:
            #         kp_val = 0.0

            # # Analyze environment
            # severity = self.analyze_environment(Rc, kp_val)
            

            # Update labels
            self.output_label.config(
                text=f"Geomagnetic latitude: {lam:.2f}°    Cutoff Rigidity: {Rc:.2f} GV")
            # self.kp_label.config(text=f"Kp Index (3-hr): {kp_val:.1f}")
            # color = "green" if severity == "Nominal" else ("orange" if severity == "Moderate" else "red")
            # self.severity_label.config(text=f"Environment Level: {severity}", foreground=color)

            # # Plot
            # self.ax.clear()
            # self.ax.plot(result["R"], result["T"], label="Transmission Function")
            # self.ax.axvline(Rc, color='r', linestyle='--', label=f"Rc = {Rc:.2f} GV")
            # self.ax.set_xlabel("Rigidity [GV]")
            # self.ax.set_ylabel("Transmission T(R)")
            # self.ax.set_title("Geomagnetic Transmission Function")
            # self.ax.legend()
            # self.ax.grid(True)
            # self.canvas.draw()
            
            # Show loading message and launch Kp fetch in background
            self.loading_label.config(text="Fetching Kp index from GFZ...")
            thread = threading.Thread(target=self.fetch_and_update_kp, args=(date, Rc))
            thread.daemon = True
            thread.start()
            
            
            open_figure_popup(root, result, Rc)

        except Exception as e:
            messagebox.showerror("Error", f"Could not compute GTF:\n{e}")
            
    # ---------------------------------------------------
    # Threaded Kp fetch + environment analysis
    # ---------------------------------------------------
    def fetch_and_update_kp(self, date, Rc):
        kp_val = fetch_kp_index(date)
        if kp_val is None:
            try:
                kp_val = float(self.kp_entry.get())
            except Exception:
                kp_val = 0.0

        severity = self.analyze_environment(Rc, kp_val)

        # Schedule safe GUI update from main thread
        self.root.after(0, lambda: self.update_kp_display(kp_val, severity))

    def update_kp_display(self, kp_val, severity):
        """Update GUI with Kp and severity after thread completes."""
        color = "green" if severity == "Nominal" else ("orange" if severity == "Moderate" else "red")
        self.kp_label.config(text=f"Kp Index (3-hr): {kp_val:.1f}")
        self.severity_label.config(text=f"Environment Level: {severity}", foreground=color)
        self.loading_label.config(text="")  # clear "fetching" text

    # ---------------------------------------------------
    # Environment analysis
    # ---------------------------------------------------
    def analyze_environment(self, Rc, Kp):
        """
        Classify environment as Nominal / Moderate / Severe.
        """
        if Kp >= 6 or Rc < 5.0:
            return "Severe"
        elif Kp >= 4 or Rc < 8.0:
            return "Moderate"
        else:
            return "Nominal"


# -------------------------------------------------------
# Run the app
# -------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = GTFApp(root)
    root.mainloop()
