# plots.py
import matplotlib.pyplot as plt


def plot_timeseries(da, title="Global Mean Time Series"):
    """Plot a 1D time series."""
    plt.figure(figsize=(10, 5))
    da.plot()
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_map(da, lat_name="lat", lon_name="lon", title="Spatial Map"):
    """Plot a 2D map of a DataArray."""
    plt.figure(figsize=(8, 5))
    da.plot()
    plt.title(title)
    plt.xlabel(lon_name)
    plt.ylabel(lat_name)
    plt.tight_layout()
    plt.show()
