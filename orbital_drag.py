import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Optional imports (uncomment when installed)
# from nrlmsise00 import msise_model
# from spaceweather import get_f107_ap   # hypothetical or custom wrapper

# -------------------------------------------------------------------
# Presets and placeholders
# -------------------------------------------------------------------
PRESETS = {
    "Custom": {"Cd": "", "A": "", "m": "", "rho": "", "v_rel": ""},
    "LEO 400 km": {"Cd": 2.2, "A": 1.0, "m": 100.0, "rho": 4e-12, "v_rel": 7700.0},
    "LEO 800 km": {"Cd": 2.2, "A": 1.0, "m": 100.0, "rho": 3e-13, "v_rel": 7500.0},
    "GEO 35786 km": {"Cd": 2.2, "A": 20.0, "m": 2000.0, "rho": 1e-17, "v_rel": 3070.0},
}


# -------------------------------------------------------------------
# Core physics & model utilities
# -------------------------------------------------------------------
def adjust_density_for_space_weather(rho, F10_7, Ap):
    F_ref, Ap_ref = 150, 15
    scale = (1.0 + 0.002 * (F10_7 - F_ref)) * (1.0 + 0.01 * (Ap - Ap_ref))
    return rho * max(scale, 0.1)


def compute_drag():
    """Compute drag acceleration from user input or model data."""
    try:
        Cd = float(cd_entry.get())
        A = float(area_entry.get())
        m = float(mass_entry.get())
        v = float(vrel_entry.get())
        lat = 45
        lon = 30
        alt = 1000

        # Determine how to get rho and space weather data
        if model_mode.get():
            # User selected to use NRLMSISE / SpaceWeather model
            rho, F10_7, Ap = fetch_model_data(lat, lon, alt)
        else:
            rho = float(density_entry.get())
            F10_7 = float(f107_entry.get()) if f107_entry.get() else 150
            Ap = float(ap_entry.get()) if ap_entry.get() else 15

        rho = adjust_density_for_space_weather(rho, F10_7, Ap)
        a_drag = 0.5 * Cd * (A / m) * rho * v**2
        result_label.config(text=f"Drag Acceleration: {a_drag:.6e} m/s²\nρ = {rho:.2e}")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")


from nrlmsise00 import msise_model
from spaceweather import get_f107_ap

def fetch_model_data(lat, lon, alt):
    dt = datetime.strptime(date_entry.get() + " " + time_entry.get(), "%Y-%m-%d %H:%M")
    F10_7, Ap = get_f107_ap(dt)
    atm = msise_model(dt, alt_km=alt, lat_deg=lat, lon_deg=lon, f107=F10_7, ap=Ap)
    rho = atm["Total"]["rho"]
    return rho, F10_7, Ap



# -------------------------------------------------------------------
# UI logic
# -------------------------------------------------------------------
def apply_preset(event=None):
    preset = preset_var.get()
    params = PRESETS[preset]
    for entry, key in zip(entries, ["Cd", "A", "m", "rho", "v_rel"]):
        entry.delete(0, tk.END)
        if params[key] != "":
            entry.insert(0, params[key])


def toggle_model_mode():
    """Switch between manual entry mode and model-based mode."""
    use_model = model_mode.get()
    for e in [density_entry, f107_entry, ap_entry]:
        e.config(state="disabled" if use_model else "normal")

    for w in [date_entry, time_entry]:
        w.config(state="normal" if use_model else "disabled")

    date_label.config(foreground="black" if use_model else "#888")
    time_label.config(foreground="black" if use_model else "#888")
    density_label.config(foreground="#888" if use_model else "black")
    ttk.Label(sw_frame, text="Mode").update()


# -------------------------------------------------------------------
# Build GUI
# -------------------------------------------------------------------
root = tk.Tk()
root.title("Orbital Drag Calculator")
root.geometry("520x650")
root.resizable(False, False)

ttk.Label(root, text="Orbital Drag Calculator", font=("Helvetica", 16, "bold")).pack(pady=10)

# Preset orbit menu
preset_frame = ttk.Frame(root, padding=(10, 5))
preset_frame.pack(fill="x")
ttk.Label(preset_frame, text="Select Preset Orbit:").pack(side="left", padx=(0, 10))
preset_var = tk.StringVar(value="Custom")
preset_menu = ttk.Combobox(preset_frame, textvariable=preset_var, values=list(PRESETS.keys()), state="readonly")
preset_menu.pack(side="left", fill="x", expand=True)
preset_menu.bind("<<ComboboxSelected>>", apply_preset)

# Drag equation variables
frame = ttk.Frame(root, padding=10)
frame.pack(fill="x")

labels = [
    ("Drag Coefficient (Cd)", "dimensionless"),
    ("Cross-sectional Area (A)", "m²"),
    ("Mass (m)", "kg"),
    ("Atmospheric Density (ρ)", "kg/m³"),
    ("Relative Velocity (v_rel)", "m/s"),
]
entries = []
for label_text, unit in labels:
    row = ttk.Frame(frame)
    row.pack(fill="x", pady=5)
    lbl = ttk.Label(row, text=label_text, width=25)
    lbl.pack(side="left")
    entry = ttk.Entry(row)
    entry.pack(side="left", fill="x", expand=True)
    ttk.Label(row, text=unit, width=10).pack(side="right")
    entries.append(entry)
cd_entry, area_entry, mass_entry, density_entry, vrel_entry = entries
density_label = frame.winfo_children()[3].winfo_children()[0]  # label for ρ

# Space weather section
sw_frame = ttk.LabelFrame(root, text="Space Weather Settings", padding=10)
sw_frame.pack(fill="x", padx=10, pady=10)

model_mode = tk.BooleanVar(value=False)
ttk.Checkbutton(sw_frame, text="Use Date/Time and NRLMSISE-00 Model", variable=model_mode,
                command=toggle_model_mode).pack(anchor="w", pady=(0, 10))

# Manual space weather inputs
manual_frame = ttk.Frame(sw_frame)
manual_frame.pack(fill="x")
ttk.Label(manual_frame, text="Solar Flux (F10.7)", width=25).pack(side="left")
f107_entry = ttk.Entry(manual_frame)
f107_entry.pack(side="left", fill="x", expand=True)
ttk.Label(manual_frame, text="sfu", width=10).pack(side="right")

manual_frame2 = ttk.Frame(sw_frame)
manual_frame2.pack(fill="x", pady=5)
ttk.Label(manual_frame2, text="Geomagnetic Index (Ap)", width=25).pack(side="left")
ap_entry = ttk.Entry(manual_frame2)
ap_entry.pack(side="left", fill="x", expand=True)
ttk.Label(manual_frame2, text="unitless", width=10).pack(side="right")

# Date/time inputs for model mode
date_frame = ttk.Frame(sw_frame)
date_frame.pack(fill="x", pady=5)
date_label = ttk.Label(date_frame, text="Date (YYYY-MM-DD)", width=25, foreground="#888")
date_label.pack(side="left")
date_entry = ttk.Entry(date_frame, state="disabled")
date_entry.pack(side="left", fill="x", expand=True)
ttk.Label(date_frame, text="").pack(side="right")

time_frame = ttk.Frame(sw_frame)
time_frame.pack(fill="x", pady=5)
time_label = ttk.Label(time_frame, text="Time (HH:MM, UTC)", width=25, foreground="#888")
time_label.pack(side="left")
time_entry = ttk.Entry(time_frame, state="disabled")
time_entry.pack(side="left", fill="x", expand=True)

# Compute
ttk.Button(root, text="Compute Drag Acceleration", command=compute_drag).pack(pady=15)
result_label = ttk.Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

# Footer
ttk.Label(
    root,
    text="Supports manual inputs or model-based atmospheric data.\nNRLMSISE-00 integration placeholder.",
    font=("Helvetica", 8, "italic"),
    justify="center"
).pack(pady=(20, 0))

root.mainloop()
