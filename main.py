from plotting import (
    plot_extreme_heat_days,
    plot_monthly_statistics,
    plot_summer_anomalies,
)

from analysis import calculate_anomalies, calculate_yearly_extremes
from data_loader import load_and_prepare_data


def main():
    """Main function to run the analysis pipeline."""
    # --- Settings ---
    MY_BIRTH_YEAR = 1992
    REF_PERIOD_START = 1991
    REF_PERIOD_END = 2020
    DATA_FILE_PATH = (
        "Messstationen_Graz_Tagesdaten_v2_Datensatz_19220101_20251031 (1).csv"
    )

    # --- 1. Load Data ---
    print("Loading data...")
    df_graz = load_and_prepare_data(DATA_FILE_PATH)

    if df_graz is not None:
        print("Data loaded successfully.")

        # --- 2. Run Analysis ---
        print("Calculating anomalies...")
        summer_anomalies_df = calculate_anomalies(
            df_graz, REF_PERIOD_START, REF_PERIOD_END
        )

        print("Calculating extreme heat events...")
        extremes_df = calculate_yearly_extremes(df_graz)

        # --- 3. Generate Plots ---
        plot_summer_anomalies(summer_anomalies_df)
        plot_monthly_statistics(df_graz, MY_BIRTH_YEAR)
        plot_extreme_heat_days(extremes_df)


if __name__ == "__main__":
    main()
