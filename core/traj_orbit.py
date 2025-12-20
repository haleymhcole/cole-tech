# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 19:13:55 2025

@author: haley
"""
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.animation import FuncAnimation, PillowWriter
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
import cartopy.io.img_tiles as cimgt

def make_trajectory_gif(
    lats,
    lons,
    alts,
    output_path="trajectory.gif",
    interval=100
):
    """
    Create an animated GIF of a trajectory on a world map.

    Parameters
    ----------
    lats, lons, alts : array-like
        Trajectory latitude [deg], longitude [deg], altitude [km or m]
    output_path : str
        Output GIF filename
    interval : int
        Frame delay in milliseconds
    """

    lats = np.asarray(lats)
    lons = np.asarray(lons)
    alts = np.asarray(alts)

    fig = plt.figure(figsize=(10, 5))
    ax = plt.axes(projection=ccrs.PlateCarree())

    ax.set_global()
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    # ax.add_feature(cfeature.LAND, facecolor="limegreen")
    # ax.add_feature(cfeature.OCEAN, facecolor="darkblue")
    ax.stock_img()
    
    # tiler = cimgt.Stamen('terrain-background')
    # ax.add_image(tiler, 4) # Zoom levels: 3 = global, 4 = good balance, 5+ = regional detail (slower)
    
    ax.coastlines(resolution="110m", linewidth=0.6, color="black")

    trajectory_color = "#c0392b"   # muted red
    point_color = "#2980b9"        # soft blue
    # ax.outline_patch.set_edgecolor("gray")
    # ax.outline_patch.set_linewidth(0.8)
    # line.set_alpha(0.85)



    # Trajectory line + moving point
    ax.plot(lons, lats, color="silver", linewidth=2, transform=ccrs.Geodetic())
    line, = ax.plot([], [], color="lime", linewidth=2, transform=ccrs.Geodetic())
    point, = ax.plot([], [], "o", color="red", markersize=8, transform=ccrs.Geodetic())

    title = ax.set_title("")
    
    gl = ax.gridlines(
        crs=ccrs.PlateCarree(),
        draw_labels=True,
        linewidth=0.5,
        color="gray",
        alpha=0.6,
        linestyle="--"
    )
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 10}
    gl.ylabel_style = {"size": 10}
    gl.xlocator = mticker.FixedLocator(range(-180, 181, 60))
    gl.ylocator = mticker.FixedLocator(range(-90, 91, 30))
    gl.xlabel_style = {"size": 8}
    gl.ylabel_style = {"size": 8}
    gl.linestyle = ":"
    # ax.set_extent([-140, 40, 10, 70], crs=ccrs.PlateCarree())


    def update(frame):
        line.set_data(lons[:frame+1], lats[:frame+1])
        # point.set_data([lons[frame]], [lats[frame]])
        point.set_data(
            np.array([lons[frame]]),
            np.array([lats[frame]])
        )

    
        title.set_text(
            f"Step {frame+1}/{len(lats)} | Altitude: {alts[frame]:.1f} km"
        )
        return line, point, title


    anim = FuncAnimation(
        fig,
        update,
        frames=len(lats),
        interval=interval,
        blit=False
    )

    anim.save(
        output_path,
        writer=PillowWriter(fps=1000 // interval)
    )

    plt.close(fig)
    
    print("DONE.")

    return output_path


if __name__ == "__main__":
    # Example trajectory
    lats = np.linspace(30, 60, 100)
    lons = np.linspace(-120, 30, 100)
    alts = np.linspace(200, 400, 100)  # km
    
    output_path = make_trajectory_gif(lats, lons, alts)
