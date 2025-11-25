# core.py
import numpy as np
import xarray as xr


def load_dataset(filepath):
    """Load a NetCDF dataset with Dask chunks for efficiency."""
    try:
        ds = xr.open_dataset(filepath, engine="netcdf4", chunks={"time": 100})
    except Exception as e:
        raise RuntimeError(f"Failed to load {filepath}: {e}")
    return ds


def detect_coords(da):
    """Detect latitude, longitude, and time coordinates in a DataArray."""
    lat_name = None
    lon_name = None
    time_name = None

    for name in da.coords:
        lname = name.lower()
        if "lat" in lname:
            lat_name = name
        elif "lon" in lname:
            lon_name = name
        elif "time" in lname:
            time_name = name

    if time_name is None:
        raise ValueError(
            f"Dataset has no 'time' dimension. Found coords: {list(da.coords.keys())}"
        )

    return lat_name, lon_name, time_name


def area_weights(da, lat_name="lat"):
    """Compute area weights based on latitude for global mean."""
    if lat_name is None:
        raise ValueError("Latitude coordinate not found for area weighting.")
    lat = da[lat_name]
    weights = np.cos(np.deg2rad(lat))
    # Normalize weights
    weights /= weights.mean()
    return weights


def global_mean(da):
    """Compute area-weighted global mean of a DataArray."""
    lat_name, lon_name, _ = detect_coords(da)

    if lat_name is None or lon_name is None:
        # No lat/lon: fallback to simple mean over time only
        return da.mean(dim="time")

    w = area_weights(da, lat_name=lat_name)

    # Broadcast weights to match DataArray dimensions
    dims = da.dims
    for d in dims:
        if d not in w.dims:
            w = w.expand_dims({d: da[d]})
    w_broadcast = w.transpose(*da.dims)

    return (da * w_broadcast).mean(dim=(lat_name, lon_name))


def running_mean(da, window=10):
    """Apply centered running mean along time dimension."""
    _, _, time_name = detect_coords(da)
    if time_name is None:
        raise ValueError("Dataset has no 'time' dimension.")
    return da.rolling({time_name: window}, center=True).mean()
