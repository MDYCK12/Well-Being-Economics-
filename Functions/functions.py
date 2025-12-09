# ----------------------------
# FUNCTIONS
# ----------------------------

import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

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
            paper_bgcolor="#2a2a2a",
            plot_bgcolor="#2a2a2a",
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
        paper_bgcolor="#2a2a2a",
        plot_bgcolor="#2a2a2a",
        font=dict(color="#e0e0e0", size=11),
        title=dict(
            text=title_text,
            font=dict(size=14, color="#ffffff"),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Year",
            gridcolor="#3a3a3a",
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title="Score",
            gridcolor="#3a3a3a",
            showgrid=True,
            zeroline=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(42, 42, 42, 0.8)",
            bordercolor="#3a3a3a",
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
    Works well with dark themes.
    
    Parameters:
    - df: DataFrame with columns ['Country Name', 'Indicator Name', 'Year', 'Value']
    - countries: List of country names to plot
    - indicator: String, the indicator name to plot
    
    Returns:
    - Plotly figure object
    """
    # Filter data
    df_filtered = df[
        (df["Country Name"].isin(countries)) &
        (df["Indicator Name"] == indicator) &
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
            paper_bgcolor="#2a2a2a",
            plot_bgcolor="#2a2a2a",
            height=400
        )
        return fig
    
    # Create figure
    fig = go.Figure()
    
    # Color palette that works well with dark backgrounds
    colors = ['#667eea', '#f093fb', '#4facfe', '#fa709a', '#fee140', '#30cfd0', '#a8edea', '#fed6e3']
    
    # Add a line for each country
    for i, country in enumerate(countries):
        df_country = df_filtered[df_filtered["Country Name"] == country]
        
        if not df_country.empty:
            fig.add_trace(go.Scatter(
                x=df_country["Year"],
                y=df_country["Value"],
                mode='lines+markers',
                name=country,
                line=dict(width=2.5, color=colors[i % len(colors)]),
                marker=dict(size=6),
                hovertemplate='<b>%{fullData.name}</b><br>' +
                             'Year: %{x}<br>' +
                             'Value: %{y:.2f}<br>' +
                             '<extra></extra>'
            ))
    
    # Update layout for dark theme
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#2a2a2a",
        plot_bgcolor="#2a2a2a",
        font=dict(color="#e0e0e0", size=11),
        title=dict(
            text=indicator,
            font=dict(size=14, color="#ffffff"),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Year",
            gridcolor="#3a3a3a",
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title="Value",
            gridcolor="#3a3a3a",
            showgrid=True,
            zeroline=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(42, 42, 42, 0.8)",
            bordercolor="#3a3a3a",
            borderwidth=1
        ),
        hovermode='x unified',
        height=400,
        margin=dict(l=60, r=20, t=60, b=60)
    )
    
    return fig



#creating Scatterplot (Katha)

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
    fig = px.scatter(
        df_final_ranking,
        x='Avg_Econ',
        y='Avg_Wellbeing',
        text='Country Name',
        color='Quadrant',
        size=[10]*len(df_final_ranking),  # fixed size for all points
        hover_name='Country Name',
        title='Economic vs Wellbeing PCA Quadrant Analysis'
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

#Creation of individual Line Chart for the economic indicator: 

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


    #Line Chart for the Wellbeing indicator: 

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

    # Create line chart
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