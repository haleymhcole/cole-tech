# -*- coding: utf-8 -*-
"""
Created on Sun Nov 30 18:52:40 2025

@author: haley
"""
import os 
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
# from mpl_toolkits.basemap import Basemap
import pandas as pd
import xarray as xr
from matplotlib.colors import LogNorm
from matplotlib.patches import Circle

def create_map_plot(fig, grid_density):
    """
    Create a world map heatmap (scatter plot) using Basemap
    and draw it on the provided Matplotlib figure.
    """

    # Add subplot to the provided figure
    ax = fig.add_subplot(111)

    # Create Basemap on that axis
    m = Basemap(
        projection='mill',
        llcrnrlat=-90, urcrnrlat=90,
        llcrnrlon=-180, urcrnrlon=180,
        resolution='l',
        ax=ax
    )

    # Extract data
    lats = grid_density['Lat'].values
    lons = grid_density['Lon'].values
    vals = grid_density['Plasma Density'].values
    vals[np.where(vals==0)[0]] = 1 # 1e-20

    # Convert to map projection coords
    x, y = m(lons, lats)
    
    # 1. Base map fill (background)
    m.fillcontinents(color='lightgray', lake_color='gray')
    m.drawmapboundary(fill_color='gray')
    
    # 2. Heatmap scatter
    sc = m.scatter(
        x, y,
        s=40,
        c=vals,
        cmap='plasma',
        alpha=0.75,
        edgecolors='none',
        zorder=4, norm=LogNorm()
    )
    
    # 3. Now draw map lines *over* the heatmap (higher zorders)
    m.drawcoastlines(linewidth=0.8, zorder=6, color='k')
    m.drawcountries(linewidth=0.6, zorder=6, color='k')
    m.drawparallels(range(-90, 91, 30), labels=[1,0,0,0], linewidth=0.3, zorder=6)
    m.drawmeridians(range(-180, 181, 60), labels=[0,0,0,1], linewidth=0.3, zorder=6)


    # Add a colorbar
    cb = fig.colorbar(sc, ax=ax, orientation='vertical', pad=0.02)
    cb.set_label("Plasma Density")

    # Labels
    ax.set_title("Plasma Density at 1 AU from Earth's Surface")
    ax.set_xlabel("Longitude", labelpad=25)
    ax.set_ylabel("Latitude", labelpad=30)
    


def map_window_2D(grid_density):
    """Create a Tkinter popup window containing the world heatmap."""
    root = tk.Tk()
    root.title("World Heatmap Viewer")

    # Create the figure ONLY once
    fig = Figure(figsize=(9, 6), dpi=100)
    create_map_plot(fig, grid_density)

    # Embed inside Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Add toolbar
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    toolbar.pack(side=tk.TOP, fill=tk.X)

    root.mainloop()
    
def map_window_polar(grid_density, vmax):
    """Create a Tkinter popup window containing the world heatmap."""
    root = tk.Tk()
    root.title("World Heatmap Viewer")

    # Create the figure ONLY once
    fig = Figure(figsize=(9, 6), dpi=100)
    create_map_plot(fig, grid_density, vmax)

    # Embed inside Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Add toolbar
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    toolbar.pack(side=tk.TOP, fill=tk.X)

    root.mainloop()

def describe_grid(grid):
    for var in ['Lat', 'Lon', 'Plasma Density']:
        print(f"{var}: {grid[var].min()} - {grid[var].max()}")
        
def convert_lon(lon):
    # Convert from 0 to 360 range to -180 to 180 range.
    # lons_new_range = []
    # for lon in lons:
    #     new_lon = ((lon+180)%360)-180
    #     lons_new_range.append(new_lon)
    # return lons_new_range
    return ((lon+180)%360)-180


def read_nc(file):
    # Load the netCDF file using xarray
    ds = xr.open_dataset(file)
    
    # # Display basic information about the dataset
    # print("\nDataset Information:")
    # print(ds.info())
    
    # Example: Plot a variable if available
    if 'bz' in ds.variables:
        plt.figure(figsize=(10, 6))
        ds['bz'].plot()
        plt.title('Bz Component of Magnetic Field')
        plt.xlabel('Time')
        plt.ylabel('Bz (nT)')
        plt.show()
    return ds

def polar_map_grid(grid, vmax):
    # Assumptions:
    # grid has columns: longitude, latitude, value
    # longitude in degrees (0–360 or –180–180)
    # latitude in degrees (-90 to 90)
    
    # ---- PREPARE DATA FOR POLAR HEATMAP ----
    
    # # Convert longitudes to radians (polar angle)
    # theta = np.deg2rad(grid["Lon"].values)
    
    # # Convert latitude to "distance from pole" (radius)
    # # 90°N = center (0), 0° = mid, -90° = edge
    # radius = (90 - grid["Lat"].values)
    
    # Create pivot table regularly spaced around sphere
    # (matplotlib pcolormesh needs gridded 2D arrays)
    lon_sorted = np.sort(grid["Lon"].unique())
    alt_sorted = np.sort(grid["Alt"].unique())
    
    lon_grid, alt_grid = np.meshgrid(lon_sorted, alt_sorted)
    
    # Interpolate values into meshgrid
    value_grid = grid.pivot_table(
        index="Alt",
        columns="Lon",
        values="Plasma Density"
    ).values
    
    Earth_radius = 6371  # km
    
    # Convert meshgrid to polar coordinates
    theta_grid = np.deg2rad(lon_grid)
    radius_grid = alt_grid + Earth_radius
    
    # ---- PLOT ----
    
    fig = plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, projection="polar")
    
    # ----- ADD EARTH DIAGRAM -----

    earth = Circle(
        (0, 0),                       # center in polar coordinates
        Earth_radius,                 # radius of Earth
        transform=ax.transData._b,   # required for polar patches
        color='lightblue',
        ec='black',
        zorder=10
    )
    ax.add_patch(earth)

    
    # Heatmap rendered as polar pseudocolor mesh
    pcm = ax.pcolormesh(theta_grid, radius_grid, value_grid,
                        shading="auto", norm=LogNorm(vmin=1, vmax=1e4)) # vmin=1, vmax=vmax
    
    
    # Optional: coastlines-like rings for readability
    ax.set_yticks([0, 30, 60, 90])
    ax.set_yticklabels(["90°N", "60°N", "30°N", "0°"])
    
    # Optional: longitude labels
    ax.set_xticks(np.deg2rad(np.arange(0, 360, 45)))
    ax.set_xticklabels([f"{d}°" for d in range(0, 360, 45)])
    
    ax.set_title("Polar Heatmap (North-Pole View)", fontsize=16)
    fig.colorbar(pcm, ax=ax, label="Plasma Density")
    
    plt.show()
    

# swpc_wsaenlil_bkg_20251004_0000
yr = 2025
mo = 10
da = 4

data_file = os.path.join("dnata", "swpc_wsaenlil_bkg_20251004_0000", "wsa_enlil.mrid00000000.suball.nc") # BG#data_file = os.path.join("Data", "swpc_wsaenlil_cme_20251003_1036", "wsa_enlil.mrid00057579.suball.nc") # CME
if os.path.exists(data_file):
    ds = read_nc(data_file)
else:
    raise Exception(f"Data file does not exist: {data_file}")

# data_path = os.path.join("Data", f"swpc_wsaenlil_bkg_{yr:02d}{mo:02d}{da:02d}_0000")
# if os.path.exists(data_path):
#     data_file = os.path.join(data_path, "wsa_enlil.mrid00000000.suball.nc")
#     if os.path.exists(data_file):
#         # Open .nc data file.
#         ds = read_nc(data_file)
        
#     else:
#         print("Data file does not exist:", data_file)
# else:
#     print("Data path does not exist:", data_path)
    
    
radial_position_m = np.array(ds['x_coord']) # m
colatitudes_rad = np.array(ds['y_coord']) # radians
longitudes_rad = np.array(ds['z_coord']) # radians 

# Convert to desired units.
R_e = 6371 # radius of Earth in km
radial_position_km = radial_position_m / 1000
altitudes_km = radial_position_km - R_e
colatitudes_deg = colatitudes_rad * 180/np.pi
latitudes_deg = 90 - colatitudes_deg
longitudes_deg = longitudes_rad * 180/np.pi

# =============================================================================
# 2D World Map
# =============================================================================
# vals = np.array(ds['dd23_3d'])
# vals.shape # time, lon, colat

# longitudes_ls = []
# latitudes_ls = []
# density_ls = []
# for lo, lon in enumerate(longitudes_deg):
#     for la, lat in enumerate(latitudes_deg):
#         longitudes_ls.append(convert_lon(lon))
#         latitudes_ls.append(lat)
#         density_ls.append(vals[0,lo,la])

# grid_density = pd.DataFrame()
# grid_density['Lat'] = latitudes_ls
# grid_density['Lon'] = longitudes_ls
# #grid_density['Alt'] = altitudes_km
# grid_density['Plasma Density'] = density_ls

# describe_grid(grid_density)

# map_window_2D(grid_density)


# =============================================================================
# 3D Polar Map
# =============================================================================
var = 'pp13_3d'
vals = np.array(ds[var])
vals.shape # uncalibrated plasma density in rad-colat-time, longitude zero
#units = ds[var].attrs['units']

t=136
longitudes_ls = []
altitudes_ls = []
#latitudes_ls = []
density_ls = []
for a, alt in enumerate(altitudes_km):
    for lo, lon in enumerate(longitudes_deg):
        altitudes_ls.append(alt)
        longitudes_ls.append(convert_lon(lon))
        density_ls.append(vals[t,lo,a])

grid_density = pd.DataFrame()
grid_density['Lon'] = longitudes_ls
grid_density['Alt'] = altitudes_ls
grid_density['Plasma Density'] = density_ls

# describe_grid(grid_density)
# map_window_polar(grid_density)

polar_map_grid(grid_density, np.max(vals))




