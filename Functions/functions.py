# ----------------------------
# FUNCTIONS
# ----------------------------

import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# Function 1: Filter data by country + indicator
# ----------------------------
def filter_data(df, country, indicator):
    """
    Filters the dataframe by country and indicator,
    returns a dataframe sorted by Year.
    """
    df_filtered = df[
        (df["Country Name"] == country) &
        (df["Indicator Name"] == indicator)
    ].sort_values("Year")
    return df_filtered


# ----------------------------
# Function 2: Plot indicator as a line chart
# ----------------------------
def plot_indicator(df_filtered, country, indicator):
    """
    Creates a line plot from a filtered dataframe.
    Returns a Matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=(8, 5))

    if df_filtered.empty:
        ax.text(0.5, 0.5, "No data available",
                ha="center", va="center", fontsize=12)
        ax.set_axis_off()
        return fig

    ax.plot(df_filtered["Year"], df_filtered["Value"], marker="o", linewidth=2)
    ax.set_title(f"{indicator} in {country}")
    ax.set_xlabel("Year")
    ax.set_ylabel(indicator)
    ax.grid(alpha=0.3)

    plt.tight_layout()
    return fig


# ----------------------------
# Function 3: Compare two indicators across multiple countries
# ----------------------------
def plot_two_indicators_long(df, countries, ind1, ind2):
    """
    Plots two indicators for multiple countries.
    ind1 -> solid line (left axis)
    ind2 -> dashed line (right axis)
    """
    # Filter data
    df_f = df[
        df["Country Name"].isin(countries) &
        df["Indicator Name"].isin([ind1, ind2]) &
        df["Year"].between(2000, 2023)
    ]

    fig, ax1 = plt.subplots(figsize=(12, 7))
    colors = plt.cm.tab10.colors

    # Plot ind1 (solid) on left axis
    handles = []
    for i, country in enumerate(countries):
        df_plot = df_f[(df_f["Country Name"] == country) & (df_f["Indicator Name"] == ind1)]
        line, = ax1.plot(df_plot["Year"], df_plot["Value"], color=colors[i % len(colors)], linewidth=2, marker='o')
        handles.append(line)

    ax1.set_xlabel("Year", fontsize=12)
    ax1.set_ylabel(ind1, fontsize=12)
    ax1.tick_params(axis='both', which='major', labelsize=10)
    ax1.grid(True, linestyle='--', alpha=0.4)

    # Plot ind2 (dashed) on right axis
    ax2 = ax1.twinx()
    for i, country in enumerate(countries):
        df_plot = df_f[(df_f["Country Name"] == country) & (df_f["Indicator Name"] == ind2)]
        ax2.plot(df_plot["Year"], df_plot["Value"], color=colors[i % len(colors)], linestyle='--', linewidth=2, marker='x')
    ax2.set_ylabel(ind2, fontsize=12)
    ax2.tick_params(axis='both', which='major', labelsize=10)

    # Legend (only country names)
    ax1.legend(handles, countries, bbox_to_anchor=(1.15, 1), loc='upper left', fontsize=10)

    plt.title(f"{ind1} (solid) and {ind2} (dashed) — {countries} (2000-2023)", fontsize=14)
    plt.tight_layout()
    fig.canvas.draw()

    return fig
