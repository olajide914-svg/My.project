def calculate_anomalies(df, ref_start=1991, ref_end=2020):
    """Calculates monthly and summer (JJA) anomalies."""
    # 1. Calculate climatological monthly means
    ref_data = df.loc[f"{ref_start}-01-01" : f"{ref_end}-12-31"]
    monthly_climatology = ref_data.groupby("month")[["tmax", "tmin", "tmean"]].mean()
    monthly_climatology.columns = ["tmax_clim", "tmin_clim", "tmean_clim"]

    # 2. Calculate monthly means for the entire series
    monthly_data = (
        df.groupby(["year", "month"])[["tmax", "tmin", "tmean"]].mean().reset_index()
    )

    # 3. Merge and compute anomalies
    anomalies_df = monthly_data.merge(monthly_climatology, on="month", how="left")
    anomalies_df["tmax_anom"] = anomalies_df["tmax"] - anomalies_df["tmax_clim"]
    anomalies_df["tmin_anom"] = anomalies_df["tmin"] - anomalies_df["tmin_clim"]
    anomalies_df["tmean_anom"] = anomalies_df["tmean"] - anomalies_df["tmean_clim"]

    # 4. Filter for summer (JJA)
    summer_anomalies = anomalies_df[anomalies_df["month"].isin([6, 7, 8])]
    yearly_summer_anomalies = (
        summer_anomalies.groupby("year")[["tmax_anom", "tmin_anom", "tmean_anom"]]
        .mean()
        .reset_index()
    )

    return yearly_summer_anomalies


def calculate_yearly_extremes(df):
    """Calculates the count of hot days and tropical nights per year."""
    # Create working copy to avoid SettingWithCopyWarning on original df
    df = df.copy()

    df["hot_day"] = (df["tmax"] >= 30).astype(int)
    df["tropical_night"] = (df["tmin"] >= 20).astype(int)

    # Sum per year
    yearly_extremes = (
        df.groupby("year")[["hot_day", "tropical_night"]].sum().reset_index()
    )
    return yearly_extremes
