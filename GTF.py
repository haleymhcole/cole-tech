import numpy as np
import ppigrf
from datetime import datetime

def to_decimal_year(dt):
    """Convert datetime to decimal year."""
    year_start = datetime(dt.year, 1, 1)
    year_end = datetime(dt.year + 1, 1, 1)
    return dt.year + ((dt - year_start).total_seconds() /
                      (year_end - year_start).total_seconds())

def geomagnetic_latitude(lat, lon, alt_km, date_decimal):
    """
    Approximate geomagnetic latitude using IGRF field direction.
    """
    Be, Bn, Bu = ppigrf.igrf(lon, lat, alt_km, date_decimal)
    # inclination angle (positive down)
    inc = np.degrees(np.arctan2(Bu, np.sqrt(Be**2 + Bn**2)))
    # Approximate geomagnetic latitude (λm ≈ dip latitude)
    lam_m = np.degrees(np.arctan(0.5 * np.tan(np.radians(inc))))
    return lam_m

def compute_cutoff_rigidity(lat, lon, alt_km, date):
    """
    Compute vertical cutoff rigidity Rc [GV] using a simplified Störmer model.
    """
    # if not isinstance(date, (float, int)):
    #     date = to_decimal_year(date)
    lam_m = geomagnetic_latitude(lat, lon, alt_km, date)
    Rc = 14.9 * (np.cos(np.radians(lam_m)) ** 4)
    return Rc, lam_m

def geomagnetic_transmission(R, Rc, k=1.0):
    """
    Smooth transmission function T(R) for rigidity R [GV].
    """
    return 1.0 / (1.0 + np.exp(-k * (R - Rc)))

def get_GTF(lat, lon, alt_km, date, R_vals=None):
    """
    Compute the Geomagnetic Transmission Function (GTF) for given location/time.

    Returns:
        dict with keys:
        - "R": rigidity array [GV]
        - "T": transmission fraction [0–1]
        - "Rc": cutoff rigidity [GV]
        - "geomag_lat": geomagnetic latitude [deg]
    """
    if R_vals is None:
        R_vals = np.linspace(0, 20, 200)  # Rigidity range [GV]

    Rc, lam_m = compute_cutoff_rigidity(lat, lon, alt_km, date)
    T_vals = geomagnetic_transmission(R_vals, Rc, k=1.2)

    return {
        "R": R_vals,
        "T": T_vals,
        "Rc": Rc,
        "geomag_lat": lam_m
    }

# ---------------------------
# Example usage
# ---------------------------
if __name__ == "__main__":
    lat, lon, alt = 40.0, -105.3, 1.6  # Boulder, CO
    date = datetime(2025, 11, 9)

    gtf = get_GTF(lat, lon, alt, date)
    print("GTF:", list(gtf))
    print("geomag_lat:", gtf['geomag_lat'])
    print(f"Geomagnetic latitude: {gtf['geomag_lat'][0]:.2f}°")
    print(f"Cutoff rigidity: {gtf['Rc'][0]:.2f} GV")

    # Optional: plot
    import matplotlib.pyplot as plt
    plt.plot(gtf["R"], gtf["T"])
    plt.axvline(gtf["Rc"], color='r', linestyle='--', label=f"Rc = {gtf['Rc'][0]:.2f} GV")
    plt.xlabel("Rigidity [GV]")
    plt.ylabel("Transmission Fraction T(R)")
    plt.title("Geomagnetic Transmission Function")
    plt.legend()
    plt.grid(True)
    plt.show()
