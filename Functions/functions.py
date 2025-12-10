# ----------------------------
# FUNCTIONS
# ----------------------------

import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

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


# ----------------------------
# Function 5: Plot PCA scores for overview (INTERACTIVE)
# ----------------------------
def plot_pca_scores_plotly(df, countries, score_column):
    """
    Creates an interactive Plotly line chart for PCA scores across multiple countries.
    Works with df structure: ['Country Name', 'Year', 'score_pca_economics', 'score_pca_wellbeing']
    
    Parameters:
    - df: DataFrame with columns ['Country Name', 'Year', score_column]
    - countries: List of country names to plot
    - score_column: String, either 'score_pca_economics' or 'score_pca_wellbeing'
    
    Returns:
    - Plotly figure object
    """
    # Filter data
    df_filtered = df[
        (df["Country Name"].isin(countries)) &
        (df["Year"] >= 2000) &
        (df["Year"] <= 2020)
    ].sort_values("Year")
    
    # Check if data exists
    if df_filtered.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#999999")
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#151b3d",
            plot_bgcolor="#151b3d",
            height=500
        )
        return fig
    
    # Create figure
    fig = go.Figure()
    
    # Color palette that works well with dark backgrounds
    colors = ['#667eea', '#f093fb', '#4facfe', '#fa709a', '#fee140', '#30cfd0', '#a8edea', '#fed6e3', '#96fbc4', '#f9f586']
    
    # Add a line for each country
    for i, country in enumerate(countries):
        df_country = df_filtered[df_filtered["Country Name"] == country]
        
        if not df_country.empty:
            fig.add_trace(go.Scatter(
                x=df_country["Year"],
                y=df_country[score_column],
                mode='lines+markers',
                name=country,
                line=dict(width=2.5, color=colors[i % len(colors)]),
                marker=dict(size=6),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             'Year: %{x}<br>' +
                             'Score: %{y:.2f}<br>' +
                             '<extra></extra>'
            ))
    
    # Determine title based on score column
    title_text = "Economic Prosperity Score" if "economics" in score_column else "Well-being Score"
    
    # Update layout for dark theme
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#151b3d",
        plot_bgcolor="#151b3d",
        font=dict(color="#e0e0e0", size=11),
        title=dict(
            text=title_text,
            font=dict(size=14, color="#ffffff"),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Year",
            gridcolor="#2a3358",
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title="Score",
            gridcolor="#2a3358",
            showgrid=True,
            zeroline=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(21, 27, 61, 0.8)",
            bordercolor="#2a3358",
            borderwidth=1
        ),
        hovermode='x unified',
        height=500,
        margin=dict(l=60, r=20, t=60, b=60)
    )
    
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
        line, = ax1.plot(df_plot["Year"], df_plot["Value"],
                         color=colors[i % len(colors)],
                         linewidth=2, marker='o')
        handles.append(line)

    ax1.set_xlabel("Year", fontsize=12)
    ax1.set_ylabel(ind1, fontsize=12)
    ax1.tick_params(axis='both', which='major', labelsize=10)
    ax1.grid(True, linestyle='--', alpha=0.4)

    # Plot ind2 (dashed) on right axis
    ax2 = ax1.twinx()
    for i, country in enumerate(countries):
        df_plot = df_f[(df_f["Country Name"] == country) & (df_f["Indicator Name"] == ind2)]
        ax2.plot(df_plot["Year"], df_plot["Value"],
                 color=colors[i % len(colors)],
                 linestyle='--', linewidth=2, marker='x')

    ax2.set_ylabel(ind2, fontsize=12)
    ax2.tick_params(axis='both', which='major', labelsize=10)

    # ax1.legend(handles, countries, bbox_to_anchor=(1.15, 1), loc='upper left', fontsize=10)

    # plt.title(f"{ind1} (solid) and {ind2} (dashed) — {countries} (2000-2023)", fontsize=14)

    plt.tight_layout()
    fig.canvas.draw()

    return fig


# ----------------------------
# Function 4: Plot single indicator with Plotly (INTERACTIVE)
# ----------------------------
def plot_indicator_plotly(df, countries, indicator):
    """
    Creates an interactive Plotly line chart for one indicator across multiple countries.
    Works well with dark themes, legend shows ONLY dots.
    """

    # Filter data
    df_filtered = df[
        (df["Country Name"].isin(countries)) &
        (df["Indicator Name"] == indicator) &
        (df["Year"] >= 2000) &
        (df["Year"] <= 2023)
    ].sort_values("Year")

    # Handle empty dataset
    if df_filtered.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#999999")
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#1a2035",
            plot_bgcolor="#1a2035",
            height=400
        )
        return fig

    # Create figure
    fig = go.Figure()
    colors = ['#667eea', '#f093fb', '#4facfe', '#fa709a', '#fee140', '#30cfd0', '#a8edea', '#fed6e3']

    # Add traces
    for i, country in enumerate(countries):
        df_c = df_filtered[df_filtered["Country Name"] == country]
        if df_c.empty:
            continue
        color = colors[i % len(colors)]

        # Trace with lines + markers
        fig.add_trace(go.Scatter(
            x=df_c["Year"],
            y=df_c["Value"],
            mode="lines+markers",
            line=dict(width=2.5, color=color),
            marker=dict(size=7, color=color),
            name=country,
            showlegend=False
        ))

        # Legend dot only
        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode="markers",
            marker=dict(size=10, color=color),
            name=country,
            showlegend=True
        ))

    # Layout
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1a2035",
        plot_bgcolor="#1a2035",
        font=dict(color="#e0e0e0", family="Arial, sans-serif", size=12),
        title=dict(
            text=indicator,
            font=dict(size=16, color="#ffffff"),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text="Year", standoff=20),  # moves "Year" label away from legend
            gridcolor="#2a3358",
            showgrid=True,
            zeroline=False,
            automargin=True
        ),
        yaxis=dict(
            title="Value",
            gridcolor="#2a3358",
            showgrid=True,
            zeroline=False,
            automargin=True
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.32,               # move legend further down
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.03)",
            bordercolor="rgba(255,255,255,0.15)",
            borderwidth=1,
            traceorder="normal",
            itemwidth=60,          # tighter spacing between dot and country name
            font=dict(size=11, color="#e0e0e0"),
            itemsizing="constant"
        ),
        hovermode='x unified',
        height=450,
        margin=dict(l=60, r=20, t=60, b=140)
    )

    return fig


# def plot_indicator_plotly(df, countries, indicator):
#     """
#     Creates an interactive Plotly line chart for one indicator across many countries.
#     Styled similar to StockPeers (clean, modern, dark theme).
#     """

#     # Filter
#     df_filtered = df[
#         (df["Country Name"].isin(countries)) &
#         (df["Indicator Name"] == indicator) &
#         (df["Year"] >= 2000) &
#         (df["Year"] <= 2023)
#     ].sort_values("Year")

#     if df_filtered.empty:
#         fig = go.Figure()
#         fig.add_annotation(
#             text="No data available",
#             xref="paper", yref="paper",
#             x=0.5, y=0.5, showarrow=False,
#             font=dict(size=16, color="#999")
#         )
#         fig.update_layout(
#             template="plotly_dark",
#             paper_bgcolor="#151b3d",
#             plot_bgcolor="#151b3d",
#             height=400
#         )
#         return fig
    
#     # Figure
#     fig = go.Figure()

#     # Smooth color palette
#     colors = [
#         "#6C8CFF", "#F79AFF", "#45C9FF", "#FF7AA2",
#         "#FFE066", "#3EE0D0", "#A8FFE8", "#F4D6FF"
#     ]

#     # Add series
#     for i, country in enumerate(countries):
#         df_c = df_filtered[df_filtered["Country Name"] == country]
#         if df_c.empty:
#             continue

#         fig.add_trace(go.Scatter(
#             x=df_c["Year"],
#             y=df_c["Value"],
#             mode="lines+markers",
#             name=country,
#             line=dict(
#                 width=2,
#                 color=colors[i % len(colors)],
#                 shape="spline",
#                 smoothing=1.2
#             ),
#             marker=dict(
#                 size=5,
#                 color=colors[i % len(colors)],
#                 opacity=0.9
#             ),
#             legendgroup=country,
#             showlegend=True,
#             hovertemplate="<b>%{fullData.name}</b><br>"
#                           "Year: %{x}<br>"
#                           "Value: %{y:.2f}<extra></extra>"
#         ))

#     # Updated Layout
#     fig.update_layout(
#         template="plotly_dark",
#         paper_bgcolor="#151b3d",
#         plot_bgcolor="#151b3d",
#         height=430,

#         font=dict(color="#e6e6e6", size=12),

#         title=dict(
#             text=indicator,
#             x=0.5,
#             font=dict(size=16, color="white")
#         ),

#         xaxis=dict(
#             title="Year",
#             gridcolor="#253055",
#             zeroline=False
#         ),
#         yaxis=dict(
#             title="Value",
#             gridcolor="#253055",
#             zeroline=False
#         ),

#         # ⭐ Clean, wider legend (StockPeers-style)
#         legend=dict(
#             orientation="h",
#             yanchor="bottom",
#             y=-0.32,
#             xanchor="center",
#             x=0.5,

#             bgcolor="rgba(255,255,255,0.03)",
#             bordercolor="rgba(255,255,255,0.12)",
#             borderwidth=1,

#             font=dict(size=11),
#             itemwidth=120,
#             itemsizing="constant",

#             # less space between items → better for many countries
#             tracegroupgap=4
#         ),

#         # unified hover like StockPeers
#         hovermode="x unified",

#         margin=dict(l=60, r=40, t=60, b=110),
#     )

#     # ⭐ Make legend show only DOT markers (no line segment)
#     fig.update_traces(
#         mode="lines+markers",
#         marker=dict(size=7),
#         selector=dict()
#     )
#     fig.update_layout(
#         legend_traceorder="normal"
#     )
#     for trace in fig.data:
#         trace.legendgroup = trace.name
#         trace.showlegend = True

#         # Override default legend icon to DOT only
#         trace.marker.symbol = "circle"
#         trace.marker.line.width = 0
#         trace.line.width = 2  # but only visible in chart, not in legend

#         trace.legendgrouptitle = None

#     return fig


# fig.update_layout(
#         template="plotly_dark",
#         paper_bgcolor="#151b3d",
#         plot_bgcolor="#151b3d",
#         font=dict(color="#e0e0e0", size=11),
#         title=dict(
#             text=indicator,
#             font=dict(size=14, color="#ffffff"),
#             x=0.5,
#             xanchor='center'
#         ),
#         xaxis=dict(
#             title="Year",
#             gridcolor="#2a3358",
#             showgrid=True,
#             zeroline=False
#         ),
#         yaxis=dict(
#             title="Value",
#             gridcolor="#2a3358",
#             showgrid=True,
#             zeroline=False
#         ),
#         legend=dict(
#             orientation="h",
#             yanchor="bottom",
#             y=1.02,
#             xanchor="right",
#             x=1,
#             bgcolor="rgba(21, 27, 61, 0.8)",
#             bordercolor="#2a3358",
#             borderwidth=1
#         ),
#         hovermode='x unified',
#         height=400,
#         margin=dict(l=60, r=20, t=60, b=60)
#     )
    
    #return fig

# ----------------------------
# FUNCTION 5: creating Scatterplot (Katha)
# ----------------------------



import numpy as np
import plotly.express as px
import pandas as pd

def quadrant_scatter_plot(final_df):
    """
    Creates a quadrant scatter plot of average economic vs wellbeing PCA scores per country.
    
    Parameters:
    - final_df (pd.DataFrame): DataFrame containing 'Country Name', 'score_pca_economics', 'score_pca_wellbeing'
    """
    
    # 1. CALCULATE THE AVERAGE SCORES PER COUNTRY
    df_final_ranking = final_df.groupby('Country Name').agg(
        {'score_pca_economics': 'mean',
         'score_pca_wellbeing': 'mean'}
    ).reset_index()

    # Rename columns for clarity
    df_final_ranking.rename(columns={
        'score_pca_economics': 'Avg_Econ',
        'score_pca_wellbeing': 'Avg_Wellbeing'
    }, inplace=True)

    # 2. CALCULATE QUADRANTS RELATIVE TO 0 (or global mean)
    conditions = [
        (df_final_ranking['Avg_Econ'] > 0) & (df_final_ranking['Avg_Wellbeing'] > 0),  # Top-Right
        (df_final_ranking['Avg_Econ'] < 0) & (df_final_ranking['Avg_Wellbeing'] > 0),  # Top-Left
        (df_final_ranking['Avg_Econ'] < 0) & (df_final_ranking['Avg_Wellbeing'] < 0),  # Bottom-Left
        (df_final_ranking['Avg_Econ'] > 0) & (df_final_ranking['Avg_Wellbeing'] < 0)   # Bottom-Right
    ]
    choices = [
        'High Econ / High Wellbeing',
        'Low Econ / High Wellbeing',
        'Low Econ / Low Wellbeing',
        'High Econ / Low Wellbeing'
    ]
    df_final_ranking['Quadrant'] = np.select(conditions, choices, default='Center/Edge Case')

    # 3. CREATE THE SCATTER PLOT
    # *** FIXES APPLIED HERE ***
    fig = px.scatter(
        df_final_ranking, 
        x='Avg_Econ',           # CORRECTED: Changed from 'Avg_ESI'
        y='Avg_Wellbeing',      # CORRECTED: Changed from 'Avg_WTI'
        text='Country Name',
        color='Quadrant',       # CORRECTED: Changed from 'Country Group' to use the calculated 'Quadrant'
        size_max=10,
        hover_name='Country Name',
        title='ESI vs. WTI Quadrant Analysis (Average 2000-2023)',
        labels={
            'Avg_Econ': 'Economic Success Index (ESI)',        # CORRECTED: Key changed from 'Avg_ESI'
            'Avg_Wellbeing': 'Well-Being Translation Index (WTI)' # CORRECTED: Key changed from 'Avg_WTI'
        }
    )

    # 4. FIX LABEL OVERLAP
    fig.update_traces(
        mode='markers+text',
        textposition='top center',
        textfont=dict(size=10)
    )

    # 5. ADD CENTER LINES
    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="gray", annotation_text="Wellbeing Avg")
    fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="gray", annotation_text="Economic Avg")

    # 6. LAYOUT ADJUSTMENTS
    fig.update_layout(
        height=600,
        showlegend=True
    )

    fig.show()

# Note: You may need to ensure you have these imports at the top of your script:
# import pandas as pd
# import numpy as np
# import plotly.express as px

# ----------------------------
# FUNCTION 6: Creation of individual Line Chart for the economic indicator
# ----------------------------
 

def plot_economic_timeseries(pivot_econ_wellbeing):
    # Melt the DataFrame to long format for plotting
    plot_df = pivot_econ_wellbeing[[
        "Country Name", "Year", "GDP per capita", "Unemployment_rev", "Inflation_rev","score_pca_economics"
    ]].melt(
        id_vars=["Country Name", "Year"],
        value_vars=["score_pca_economics"],
        var_name="Indicator",
        value_name="Score"
    )

    # Create line chart
    fig = px.line(
        plot_df,
        x="Year",
        y="Score",
        color="Country Name",      # each country gets a line
        line_dash="Indicator",     # different dash style per indicator
        markers=True,
        title="Economic PCA Score Over Time per Country"
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Score (normalized)",
        legend_title="Country / Indicator",
        template="plotly_white"
    )

    fig.show()

# ----------------------------
# FUNCTION 6: Creation of individual Line Chart for the well-being indicator
# ----------------------------

def plot_wellbeing_timeseries(pivot_econ_wellbeing):
    # Melt the DataFrame to long format for plotting
    plot_df = pivot_econ_wellbeing[[
        "Country Name", "Year", "gini_rev", "life_expectancy", "score_pca_wellbeing"
    ]].melt(
        id_vars=["Country Name", "Year"],
        value_vars=["score_pca_wellbeing"],
        var_name="Indicator",
        value_name="Score"
    )

    # Create line chart Katha
    fig = px.line(
        plot_df,
        x="Year",
        y="Score",
        color="Country Name",      # each country gets a line
        line_dash="Indicator",     # different dash style per indicator
        markers=True,
        title="Well-being PCA Score Over Time per Country"
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Score (normalized)",
        legend_title="Country / Indicator",
        template="plotly_white"
    )

    fig.show()

    #--- Function to create Quadrant Scatter Plot for all countries across two indicators Max 


import plotly.express as px
import pandas as pd
import numpy as np

def plot_esi_wti_quadrants(df_merged_scores: pd.DataFrame):

    df_final_ranking = df_merged_scores.groupby('Country Name').agg(
        {'Economic Success (PCA)': 'mean',
         'Well-Being (PCA)': 'mean'}
    ).reset_index()

    df_final_ranking.rename(columns={
        'Economic Success (PCA)': 'Avg_ESI',
        'Well-Being (PCA)': 'Avg_WTI'
    }, inplace=True)

    conditions = [
        (df_final_ranking['Avg_ESI'] > 0) & (df_final_ranking['Avg_WTI'] > 0),
        (df_final_ranking['Avg_ESI'] < 0) & (df_final_ranking['Avg_WTI'] > 0),
        (df_final_ranking['Avg_ESI'] < 0) & (df_final_ranking['Avg_WTI'] < 0),
        (df_final_ranking['Avg_ESI'] > 0) & (df_final_ranking['Avg_WTI'] < 0)
    ]
    choices = [
        'Successful Translator (High ESI, High WTI)',
        'Efficient Translator (Low ESI, High WTI)',
        'Poor Performer (Low ESI, Low WTI)',
        'Inefficient Translator (High ESI, Low WTI)'
    ]
    df_final_ranking['Country Group'] = np.select(conditions, choices, default='Central/Edge Case')

    fig = px.scatter(
        df_final_ranking,
        x='Avg_ESI',
        y='Avg_WTI',
        text='Country Name',
        color='Country Group',
        hover_name='Country Name',
        title='ESI vs. WTI Quadrant Analysis (Average 2000–2023)',
        labels={
            'Avg_ESI': 'Economic Success Index (ESI)',
            'Avg_WTI': 'Well-Being Translation Index (WTI)'
        }
    )

    fig.update_traces(
        mode='markers+text',
        marker=dict(size=10),
        textposition='top right',
        textfont=dict(size=10, color='black')
    )

    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="red", annotation_text="WTI Average (0)")
    fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="red", annotation_text="ESI Average (0)")

    fig.update_layout(showlegend=True, height=600, legend_title_text="Quadrant", hovermode="closest")

    return fig


# --- EXAMPLE USAGE ---
# Assuming you have run the ESI/WTI calculation and merged them into df_merged_scores
# fig = plot_esi_wti_quadrants(df_merged_scores)
# fig.show()

# Plot function to plot economic indicator and well-being indicator as horizontal bar charts - Max  

import plotly.express as px
import pandas as pd

def plot_esi_ranking_bar(df_merged_scores: pd.DataFrame, top_n: int = 0, bottom_n: int = 0):
    """
    Calculates the average ESI score for all countries, sorts them, and 
    generates a horizontal bar chart of the full ranking or a selection (Top/Bottom N).

    Args:
        df_merged_scores (pd.DataFrame): DataFrame containing yearly 'Economic Success (PCA)' scores.
        top_n (int): Number of top-ranked countries to display. If 0, all countries are included.
        bottom_n (int): Number of bottom-ranked countries to display.

    Returns:
        plotly.graph_objects.Figure: The final horizontal bar chart figure.
    """
    # 1. CALCULATE THE AVERAGE ESI SCORE PER COUNTRY
    df_ranking = df_merged_scores.groupby('Country Name')['Economic Success (PCA)'].mean().reset_index()

    # Rename the column
    df_ranking.rename(columns={'Economic Success (PCA)': 'Avg_ESI'}, inplace=True)

    # Sort the ranking from highest ESI to lowest
    df_ranking_sorted = df_ranking.sort_values(by='Avg_ESI', ascending=False).reset_index(drop=True)
    
    # 2. SELECT DATA FOR VISUALIZATION (Handles Top N, Bottom N, or All)
    if top_n > 0 or bottom_n > 0:
        df_top = df_ranking_sorted.head(top_n)
        df_bottom = df_ranking_sorted.tail(bottom_n)
        # Use concat to combine the selected slices
        df_bar_viz = pd.concat([df_top, df_bottom])
    else:
        # Default: Plot all countries
        df_bar_viz = df_ranking_sorted
        
    # 3. CREATE THE HORIZONTAL BAR CHART
    fig = px.bar(
        df_bar_viz,
        x='Avg_ESI',
        y='Country Name',
        orientation='h', 
        color='Avg_ESI',
        color_continuous_scale=px.colors.sequential.Teal,
        title='Country Ranking: Economic Success Index (ESI, 2000-2023 Average)',
        labels={'Avg_ESI': 'ESI', 'Country Name': ''}
    )

    # 4. FIX AXIS ORDER
    # The list must be taken directly from the data used for the figure.
    sorted_country_list = df_bar_viz['Country Name'].tolist() 

    fig.update_layout(
        yaxis={
            'categoryorder': 'array',
            'categoryarray': sorted_country_list 
        },
        # Reverse the Y-axis so the highest score is physically at the top of the chart
        yaxis_autorange='reversed',
        showlegend=False
    )

    # Add a vertical line at ESI = 0 (the sample average)
    fig.add_vline(x=0, line_width=2, line_dash="dash", line_color="red")
    
    return fig


# build function to build table on website for indicator definition 

def display_streamlit_methodology():
    """
    Creates and displays the full methodology (indicators and country selection) 
    in structured tables using Streamlit commands.
    """
    
    # 1. Data for the main Indicators/Index table
    indicator_data = {
        'Index Name': [
            'Economic Index (EI)', 
            'Well-Being Index',
            'GDP per capita',
            'Unemployment levels (%)',
            'Inflation (CPI, Index)',
            'National savings (% GDP)',
            'Life expectancy at birth',
            'GINI Index'
        ],
        'Components/ Sub-Indicators': [
            'GDP, Inflation Rate, Unemployment Rate',
            'Life Expectancy, Gini Index',
            'Thousands, USD',
            'Percentage',
            'Index',
            'Percent of GDP',
            'Years',
            'Index'
        ],
        'Weighting Method': [
            'Principal Component Analysis (PCA)',
            'Principal Component Analysis (PCA)',
            'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A'
        ],
        'Rationale for Selection': [
            'Provides a comprehensive view of economic performance, covering growth (GDP), '
            'labor market health (Unemployment), and macroeconomic stability (Inflation).',
            'Measures key social outcomes: public health/longevity (Life Expectancy) and socio-economic inequality (Gini Index).',
            'Measures economic output and standard of living.',
            'Measures labor market health and resource utilization.',
            'Measures macroeconomic stability and price changes.',
            'Measures accumulated wealth for future growth.',
            'Measures overall public health and longevity.',
            'Measures socio-economic inequality in distribution of income.'
        ],
        'Source': [
            'IMF-Data, own calculations',
            'World-Bank data, own calculations',
            'IMF-Data', 'IMF-Data', 'IMF-Data', 'IMF-Data', 
            'World-Bank Data', 'World-Bank Data'
        ]
    }
    
    df_methodology = pd.DataFrame(indicator_data)

    # 2. Display the Methodology Table using Streamlit
    st.header("📊 Indicator Methodology Table")
    st.dataframe(df_methodology, hide_index=True) # st.dataframe is scrollable and searchable
    
    # 3. Data for country selection
    selected_countries = [
        'Japan', 'Indonesia', 'Germany', 'Denmark', 'Poland', 
        'South Africa', 'US', 'Chile', 'Costa Rica'
    ]
    
    country_rationale = (
        "Countries were selected based on **geographic diversity**, robust **data availability**, "
        "and representation across a spectrum of **economic development** levels."
    )
    
    # 4. Display the Country Selection in a structured block
    st.header("🌍 Country Selection and Rationale")
    
    # Use st.table() to display the list of countries clearly
    st.markdown("**Selected Countries:**")
    st.table(pd.DataFrame({'Country': selected_countries}))

    # Display the rationale using markdown for formatting
    st.markdown("**Selection Rationale:**")
    st.markdown(country_rationale)

# ---
# To use this in your Streamlit app, make sure you have imported streamlit and pandas, 
# and then call the function:
#
# if __name__ == '__main__':
#     display_streamlit_methodology()

