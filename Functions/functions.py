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

# ----------------------------
# Function 5: Animated GDP vs Life Expectancy Bubble Chart
# ----------------------------

import pandas as pd
import plotly.express as px

def animated_gdp_life_expectancy(df_long, 
                                 gdp_indicator='GDP per capita',
                                 life_expectancy_indicator='Life expectancy at birth, total (years)',
                                 urban_pop_indicator='Urban population (% of total population)',
                                 target_countries=None,
                                 year_step=2,
                                 size_max=60):
    """
    Transforms a long-format DataFrame and creates an animated Plotly bubble chart
    showing GDP vs Life Expectancy, with bubble size representing Urban Population.
    
  """

    if target_countries is None:
        target_countries = df_long['Country Name'].unique()

    # Filter for target countries and required indicators
    required_indicators = [gdp_indicator, life_expectancy_indicator, urban_pop_indicator]
    df_filtered = df_long[df_long['Indicator Name'].isin(required_indicators)]
    df_filtered = df_filtered[df_filtered['Country Name'].isin(target_countries)]

    # Pivot to wide format
    df_wide = df_filtered.pivot_table(
        index=['Country Name', 'Year'],
        columns='Indicator Name',
        values='Value'
    ).reset_index()
    df_wide.columns.name = None

    # Rename columns for clarity
    df_wide.rename(columns={
        'Country Name': 'Country',
        gdp_indicator: 'GDP',
        life_expectancy_indicator: 'Life Expectancy',
        urban_pop_indicator: 'Urban Population'
    }, inplace=True)

    # Convert to numeric
    for col in ['GDP', 'Life Expectancy', 'Urban Population', 'Year']:
        df_wide[col] = pd.to_numeric(df_wide[col], errors='coerce')

    # Drop rows with missing values
    df_wide = df_wide.dropna(subset=['GDP', 'Life Expectancy', 'Urban Population', 'Year'])

    # Filter years according to year_step
    all_years = sorted(df_wide['Year'].unique())
    filtered_years = all_years[::year_step]
    df_wide = df_wide[df_wide['Year'].isin(filtered_years)]

    # Maximum GDP for x-axis range
    max_gdp = df_wide['GDP'].max() * 1.1

    # Create animated Plotly scatter
    fig = px.scatter(
        df_wide,
        x="GDP",
        y="Life Expectancy",
        animation_frame="Year",
        animation_group="Country",
        size="Urban Population",
        color="Country",
        hover_name="Country",
        log_x=False,
        size_max=size_max,
        labels={
            "GDP": "GDP per Capita (Linear Scale)",
            "Life Expectancy": "Life Expectancy (Years)",
            "Urban Population": "Urban Population"
        },
        title="Evolution of GDP vs Life Expectancy"
    )

    # Set axis ranges
    fig.update_layout(
        xaxis=dict(range=[0, max_gdp], tickformat='.2s'),
        yaxis=dict(range=[40, 90])
    )

    # Adjust animation speed (250ms per frame)
    if fig.layout.updatemenus and fig.layout.updatemenus[0].buttons:
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 250
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 250

    return fig
