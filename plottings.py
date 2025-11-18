import matplotlib.pyplot as plt


def plot_summer_anomalies(anomaly_data):
    """Plots the summer anomaly time series."""
    print("\n--- Generating Plot 1: Summer (JJA) Temperature Anomalies ---")

    params = [
        ("tmean_anom", "Mean Temperature"),
        ("tmax_anom", "Max Temperature"),
        ("tmin_anom", "Min Temperature"),
    ]

    fig, axes = plt.subplots(3, 1, figsize=(15, 18), sharex=True)
    fig.suptitle(
        "Summer (JJA) Temperature Anomalies for Graz (1922–2025)\nReference Period: 1991–2020",
        fontsize=16,
    )

    for i, (param_col, title) in enumerate(params):
        ax = axes[i]

        # Plot all bars
        colors = ["#d62728" if x > 0 else "#1f77b4" for x in anomaly_data[param_col]]
        ax.bar(anomaly_data["year"], anomaly_data[param_col], color=colors, width=0.7)

        # Find and highlight top 5
        top_5 = anomaly_data.nlargest(5, param_col)
        ax.bar(
            top_5["year"],
            top_5[param_col],
            color="#ff7f0e",
            edgecolor="black",
            linewidth=1,
            label="Top 5 Hottest",
        )

        # Add labels to top 5
        for _, row in top_5.iterrows():
            ax.text(
                row["year"],
                row[param_col] + 0.1 * (1 if row[param_col] > 0 else -1),
                f"{int(row['year'])}",
                ha="center",
                va="bottom" if row[param_col] > 0 else "top",
                fontsize=9,
            )

        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_ylabel("Temperature Anomaly (°C)")
        ax.set_title(f"Summer (JJA) {title} Anomaly")
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.7)

        print(f"\n5 Hottest Summers ({title}):")
        print(top_5[["year", param_col]].to_string(index=False))

    ax.set_xlabel("Year")
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    plt.show()


def plot_monthly_statistics(df, birth_year):
    """Plots monthly statistics (median, IQR, IDR) and overlays specific years."""
    print("\n--- Generating Plot 2: Monthly Temperature Statistics ---")

    years_to_plot = sorted(list(set([birth_year, 2023, 2024, 2025])))
    params = [
        ("tmean", "Mean Temperature"),
        ("tmax", "Max Temperature"),
        ("tmin", "Min Temperature"),
    ]

    # Calculate statistics for all years
    quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]
    monthly_stats = (
        df.groupby("month")[["tmax", "tmin", "tmean"]].quantile(quantiles).unstack()
    )

    # Get monthly data for the specific years to overlay
    monthly_data_plot = (
        df.groupby(["year", "month"])[["tmax", "tmin", "tmean"]].mean().reset_index()
    )
    yearly_data_to_plot = monthly_data_plot[
        monthly_data_plot["year"].isin(years_to_plot)
    ]

    fig, axes = plt.subplots(3, 1, figsize=(15, 20), sharex=True)
    fig.suptitle(
        "Monthly Temperature Statistics for Graz (Full Period: 1922–2025)", fontsize=16
    )

    months = range(1, 13)
    month_names = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    if len(years_to_plot) > 1:
        colors = plt.cm.jet(
            [i / (len(years_to_plot) - 1) for i in range(len(years_to_plot))]
        )
    else:
        colors = [plt.cm.jet(0.5)]

    for i, (param, title) in enumerate(params):
        ax = axes[i]
        stats = monthly_stats[param]

        # Plot IDR (10th-90th)
        ax.fill_between(
            months,
            stats[0.1],
            stats[0.9],
            color="#cccccc",
            alpha=0.7,
            label="10th–90th Percentile (IDR)",
        )
        # Plot IQR (25th-75th)
        ax.fill_between(
            months,
            stats[0.25],
            stats[0.75],
            color="#a0a0a0",
            alpha=0.9,
            label="25th–75th Percentile (IQR)",
        )
        # Plot Median
        ax.plot(
            months,
            stats[0.5],
            color="black",
            linestyle="--",
            linewidth=2,
            label="Median (All Years)",
        )

        # Overlay specific years
        for j, year in enumerate(years_to_plot):
            year_data = yearly_data_to_plot[yearly_data_to_plot["year"] == year]
            if not year_data.empty:
                year_data = year_data.sort_values(by="month")
                ax.plot(
                    year_data["month"],
                    year_data[param],
                    marker="o",
                    markersize=5,
                    linestyle="-",
                    label=f"Year {year}",
                    color=colors[j],
                    linewidth=2,
                )

        ax.set_title(f"Monthly {title}")
        ax.set_ylabel("Temperature (°C)")
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        ax.legend(loc="upper left")
        ax.set_xticks(months)
        ax.set_xticklabels(month_names)

    ax.set_xlabel("Month")
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    plt.show()


def plot_extreme_heat_days(yearly_extremes):
    """Plots the yearly count of hot days and tropical nights."""
    print("\n--- Generating Plot 3: Extreme Heat Days ---")

    fig, axes = plt.subplots(2, 1, figsize=(15, 12), sharex=True)
    fig.suptitle("Yearly Extreme Heat Events in Graz (1922–2025)", fontsize=16)

    # Plot Hot Days
    axes[0].bar(
        yearly_extremes["year"],
        yearly_extremes["hot_day"],
        color="#d62728",
        label="Hot Days",
    )
    axes[0].set_title("Yearly Number of Hot Days (Tmax ≥ 30°C)")
    axes[0].set_ylabel("Number of Days")
    axes[0].grid(axis="y", linestyle="--", alpha=0.7)

    # 10-year running mean
    yearly_extremes["hot_day_10yr_mean"] = (
        yearly_extremes["hot_day"].rolling(window=10, center=True, min_periods=1).mean()
    )
    axes[0].plot(
        yearly_extremes["year"],
        yearly_extremes["hot_day_10yr_mean"],
        color="black",
        linewidth=2,
        label="10-yr running mean",
    )
    axes[0].legend()

    # Plot Tropical Nights
    axes[1].bar(
        yearly_extremes["year"],
        yearly_extremes["tropical_night"],
        color="#1f77b4",
        label="Tropical Nights",
    )
    axes[1].set_title("Yearly Number of Tropical Nights (Tmin ≥ 20°C)")
    axes[1].set_ylabel("Number of Days")
    axes[1].grid(axis="y", linestyle="--", alpha=0.7)

    # 10-year running mean
    yearly_extremes["tropical_night_10yr_mean"] = (
        yearly_extremes["tropical_night"]
        .rolling(window=10, center=True, min_periods=1)
        .mean()
    )
    axes[1].plot(
        yearly_extremes["year"],
        yearly_extremes["tropical_night_10yr_mean"],
        color="black",
        linewidth=2,
        label="10-yr running mean",
    )
    axes[1].legend()

    axes[1].set_xlabel("Year")
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    plt.show()
