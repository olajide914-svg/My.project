import pandas as pd


def load_and_prepare_data(file_path):
    """Loads and cleans the Graz station data from a local file."""
    try:
        df = pd.read_csv(file_path, header=0, na_values=[""], parse_dates=["time"])
    except FileNotFoundError:
        print("--- ERROR ---")
        print(f"Data file not found at: {file_path}")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

    # Rename columns for easier use
    df.rename(
        columns={"tlmax": "tmax", "tlmin": "tmin", "tl_mittel": "tmean"}, inplace=True
    )

    # Convert temperature columns to numeric
    temp_cols = ["tmax", "tmin", "tmean"]
    for col in temp_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows where temperature data is missing
    df.dropna(subset=temp_cols, inplace=True)

    # Set datetime index
    df.set_index("time", inplace=True)

    # Extract year and month for grouping
    df["year"] = df.index.year
    df["month"] = df.index.month

    return df
