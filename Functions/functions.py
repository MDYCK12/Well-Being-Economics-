# ----------------------------
# FUNCTIONS
# ----------------------------

import pandas as pd
import seaborn as sns
import plotly.express as pe
import matplotlib as plt

# FUNCTION FILTERING DATA BASED ON COUNTRY NAME AND INDICATOR NAME
# filter_data(df, country, indicator)

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

# FUNCTION PLOTTING TIME SERIES BASED ON DATA FILTERED BY THE PREVIOUS FUNCTION
# plot_indicator(df_filtered, country, indicator)

def plot_indicator(df_filtered, country, indicator):
    """
    Creates a line plot from a filtered dataframe.
    Returns a Matplotlib figure object.
    """
    fig, ax = plt.subplots()

    if df_filtered.empty:
        ax.text(0.5, 0.5, "No data available",
                ha="center", va="center", fontsize=12)
        ax.set_axis_off()
        return fig

    ax.plot(df_filtered["Year"], df_filtered["Value"], marker="o")
    ax.set_title(f"{indicator} in {country}")
    ax.set_xlabel("Year")
    ax.set_ylabel(indicator)

    return fig

# How to use these functions inside our mypage.py file

# from functions import filter_data, plot_indicator

# # Filter the data
# df_germany_unemp = filter_data(df, "Germany", "Unemployment levels (%)")

# # Create the plot
# fig = plot_indicator(df_germany_unemp, "Germany", "Unemployment levels (%)")

# # Display in Streamlit
# st.pyplot(fig)









# OLD FUNCTION CRETAING PLOTS BASED ON COUNTRY AND TYPE OF INDICATOR - NOT VERY USEFUL

def plot_series(df, country, indicator):
    """Plot time series for a specific country and indicator."""
    # Filter and prepare data
    data = df[(df["INDICATOR"]==indicator) & (df["COUNTRY"]==country)]
    years = [c for c in data.columns if str(c).isdigit() and len(str(c))==4]
    melted = data.melt(id_vars=['COUNTRY', 'INDICATOR'], value_vars=years, var_name='YEAR', value_name='VALUE')
    melted['YEAR'] = pd.to_numeric(melted['YEAR'])
    
    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(melted.sort_values('YEAR')['YEAR'], melted.sort_values('YEAR')['VALUE'], marker='o', linewidth=2)
    plt.title(f"{country} - {indicator}")
    plt.xlabel('Year'); plt.ylabel('Value'); plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    return melted.sort_values('YEAR')

