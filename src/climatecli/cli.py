# cli.py
import argparse
import warnings

from climatecli.core import detect_coords, global_mean, load_dataset, running_mean
from climatecli.plots import plot_map, plot_timeseries

warnings.filterwarnings("ignore", category=FutureWarning)


def main():
    parser = argparse.ArgumentParser(description="Climate data CLI")
    parser.add_argument(
        "--files", nargs="+", required=True, help="Paths to NetCDF files to process"
    )
    parser.add_argument(
        "--plot", action="store_true", help="Plot global mean time series"
    )
    parser.add_argument("--map", action="store_true", help="Plot spatial map")
    parser.add_argument(
        "--window", type=int, default=10, help="Running mean window size"
    )

    args = parser.parse_args()

    for filepath in args.files:
        print(f"\nProcessing file '{filepath}'")
        ds = load_dataset(filepath)

        # Loop through all variables
        for var in ds.data_vars:
            da = ds[var]

            # Skip variables without time dimension
            if "time" not in da.dims:
                print(
                    f"Skipping '{var}' because it has no time dimension for analysis."
                )
                continue

            # Detect coordinates
            lat_name, lon_name, time_name = detect_coords(da)

            # Compute global mean
            try:
                gm = global_mean(da)
            except Exception as e:
                print(f"Skipping '{var}': {e}")
                continue

            # Apply running mean
            try:
                smoothed = running_mean(gm, window=args.window)
            except Exception as e:
                print(f"Running mean failed for '{var}': {e}")
                smoothed = gm

            # Print crossing year for 1.5°C
            try:
                crossing_year = smoothed.where(smoothed >= 1.5, drop=True).time.values[
                    0
                ]
                print(f"{var} 1.5°C crossing year: {crossing_year}")
            except Exception:
                print(f"{var}: 1.5°C crossing year could not be computed.")

            # Plot time series
            if args.plot:
                plot_timeseries(smoothed, title=f"{var} Global Mean (Smoothed)")

            # Plot map (last time step)
            if args.map and lat_name and lon_name:
                plot_map(
                    da.isel(time=-1),
                    lat_name=lat_name,
                    lon_name=lon_name,
                    title=f"{var} Last Time Step",
                )


if __name__ == "__main__":
    main()
