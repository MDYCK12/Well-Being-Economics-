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
