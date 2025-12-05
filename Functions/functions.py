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

    # IMPORTANT: Remove any title
    ax1.set_title("")  # ensures no title is shown

    plt.tight_layout()
    fig.canvas.draw()

    return fig


# ----------------------------
# Function 5: Animated GDP vs Life Expectancy Bubble Chart
# ----------------------------
import pandas as pd
import plotly.express as px

def animated_gdp_life_expectancy(df_long, target_countries=None):
    """
    Creates an animated bubble chart of GDP vs Life Expectancy over time.
    
    Parameters:
        df_long: long-format DataFrame with 'Country Name', 'Indicator Name', 'Year', 'Value'.
        target_countries: list of countries to include (default is None, includes all).
    
    Returns:
        fig: Plotly Figure object (animated bubble chart)
    """
    # --- Default countries if none provided ---
    if target_countries is None:
        target_countries = [
            'Germany', 'Denmark', 'Poland', 'United States', 'Chile', 
            'Costa Rica', 'Japan', 'China', 'Indonesia', 'South Africa', 
            'Ghana', "Cote d'Ivoire"
        ]
    
    # --- Indicators ---
    GDP_INDICATOR = 'GDP per capita'
    LIFE_EXPECTANCY_INDICATOR = 'Life expectancy at birth, total (years)'
    URBAN_POPULATION_INDICATOR = 'Urban population (% of total population)'
    
    # Filter
    df_filtered = df_long[df_long['Indicator Name'].isin(
        [GDP_INDICATOR, LIFE_EXPECTANCY_INDICATOR, URBAN_POPULATION_INDICATOR]
    ) & df_long['Country Name'].isin(target_countries)].copy()
    
    # Pivot to wide format
    df_wide = df_filtered.pivot_table(
        index=['Country Name', 'Year'],
        columns='Indicator Name',
        values='Value'
    ).reset_index()
    
    df_wide.columns.name = None
    df_wide.rename(columns={
        'Country Name': 'Country',
        GDP_INDICATOR: 'GDP',
        LIFE_EXPECTANCY_INDICATOR: 'Life Expectancy',
        URBAN_POPULATION_INDICATOR: 'Urban Population'
    }, inplace=True)
    
    # Convert numeric
    df_wide['GDP'] = pd.to_numeric(df_wide['GDP'], errors='coerce')
    df_wide['Life Expectancy'] = pd.to_numeric(df_wide['Life Expectancy'], errors='coerce')
    df_wide['Urban Population'] = pd.to_numeric(df_wide['Urban Population'], errors='coerce')
    df_wide['Year'] = pd.to_numeric(df_wide['Year'], errors='coerce').astype(int)
    
    # Drop rows with missing values
    df_wide = df_wide.dropna(subset=['GDP', 'Life Expectancy', 'Urban Population'])
    
    # Filter years every 2 steps
    all_years = sorted(df_wide['Year'].unique())
    df_wide = df_wide[df_wide['Year'].isin(all_years[::2])]
    
    # Create animated figure
    max_gdp = df_wide['GDP'].max() * 1.1
    fig = px.scatter(
        df_wide,
        x='GDP',
        y='Life Expectancy',
        size='Urban Population',
        color='Country',
        animation_frame='Year',
        animation_group='Country',
        hover_name='Country',
        log_x=False,
        size_max=60,
        labels={
            'GDP': 'GDP per Capita',
            'Life Expectancy': 'Life Expectancy (Years)',
            'Urban Population': 'Urban Population'
        },
        title="Evolution of GDP vs Life Expectancy"
    )
    fig.update_layout(
        xaxis=dict(range=[0, max_gdp]),
        yaxis=dict(range=[40, 90])
    )
    
    return fig
