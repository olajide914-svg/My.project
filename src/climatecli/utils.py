import xarray as xr


def concat_datasets(files):
    """Concatenate multiple datasets along the time dimension."""
    datasets = [xr.open_dataset(f) for f in files]
    combined = xr.concat(datasets, dim="time")
    return combined
