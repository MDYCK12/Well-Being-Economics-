# ----------------------------
# FUNCTIONS
# ----------------------------

import pandas as pd
import seaborn as sns
import plotly.express as pe
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
    Works in both Jupyter and Streamlit.
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

def plot_two_indicators_long(df, countries, ind1, ind2):
    """
    Compare two indicators across multiple countries (1980-2023).
    ind1: solid line on left axis
    ind2: dashed line on right axis
    Returns a Matplotlib figure.
    """
    # Filter for selected countries, indicators, and years
    df_f = df[
        df["Country Name"].isin(countries) & 
        df["Indicator Name"].isin([ind1, ind2]) & 
        df["Year"].between(1980, 2023)
    ]

    # Set up figure
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Color map
    colors = plt.cm.tab10.colors

    # Plot ind1 (solid) on ax1
    handles = []
    for i, country in enumerate(countries):
        df_plot = df_f[(df_f["Country Name"] == country) & (df_f["Indicator Name"] == ind1)]
        line, = ax1.plot(df_plot["Year"], df_plot["Value"],
                         color=colors[i % len(colors)],
                         linewidth=2,
                         marker='o')
        handles.append(line)

    ax1.set_xlabel("Year", fontsize=12)
    ax1.set_ylabel(ind1, fontsize=12)
    ax1.tick_params(axis='both', which='major', labelsize=10)
    ax1.grid(True, linestyle='--', alpha=0.4)

    # Plot ind2 (dashed) on ax2
    ax2 = ax1.twinx()
    for i, country in enumerate(countries):
        df_plot = df_f[(df_f["Country Name"] == country) & (df_f["Indicator Name"] == ind2)]
        ax2.plot(df_plot["Year"], df_plot["Value"],
                 color=colors[i % len(colors)],
                 linestyle='--',
                 linewidth=2,
                 marker='x')
    ax2.set_ylabel(ind2, fontsize=12)
    ax2.tick_params(axis='both', which='major', labelsize=10)

    # Legend with country names
    ax1.legend(handles, countries, bbox_to_anchor=(1.15,1), loc='upper left', fontsize=10)

    # Title
    plt.title(f"{ind1} (solid) and {ind2} (dashed) — {countries} (1980-2023)", fontsize=14)
    plt.tight_layout()

    # Force draw (ensures axes appear in some backends)
    fig.canvas.draw()

    return fig



# ----------------------------
# Function 4: Define function to assess two indicators per country
# ----------------------------

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def country_analysis(df,country_name, indicator):
    df_filter=df[df["Country Name"].isin(country_name)]
    df_filter=df_filter[df_filter["Indicator Name"].isin(indicator)]
    print(df_filter)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
    go.Scatter(x=df_filter["Year"],y=df_filter["Value"], name="indicator"),
    secondary_y=False,
    )
    fig.add_trace(
    go.Scatter(x=df_filter["Year"],y=df_filter["Value"], name="indicator"),
    secondary_y=True,
    )
    return fig
