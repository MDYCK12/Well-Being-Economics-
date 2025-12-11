import streamlit as st
import io
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os


# -----------------------------------------------------
# FIX IMPORTS (works locally AND on Streamlit Cloud)
# -----------------------------------------------------

# Get absolute path to repository root:
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add repo root to Python search path
if repo_root not in sys.path:
    sys.path.append(repo_root)

# Now import functions from the Functions folder
from Functions.functions import (
    filter_data,
    plot_indicator,
    plot_two_indicators_long,
    plot_indicator_plotly,
    plot_pca_scores_plotly,
    plot_esi_ranking_bar,
    plot_esi_wti_quadrants
)

st.cache_data.clear()  # clears cached data
st.cache_resource.clear()  # clears cached models/resources


# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Economic Prosperity & Well-being",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------
# CUSTOM CSS FOR DARK THEME
# -----------------------------------
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0a0e27;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 300 !important;
    }
    
    h1 {
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h4 {
        color: #b0b0b0 !important;
        font-weight: 300 !important;
    }
    
    /* Text */
    p, div, span, label {
        color: #e0e0e0 !important;
    }
    
    /* Navigation tabs - Button style (smaller) */
    div.row-widget.stRadio > div {
        background-color: #151b3d;
        padding: 0.75rem;
        border-radius: 0px;
        gap: 0.75rem;
        display: flex;
        justify-content: center;
    }
    
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] {
        background-color: #1e2749 !important;
        color: #b0b0b0 !important;
        padding: 0.6rem 1.75rem !important;
        border-radius: 8px !important;
        border: 1px solid #2a3358 !important;
        transition: all 0.3s ease !important;
        font-weight: 400 !important;
        font-size: 0.95rem !important;
        cursor: pointer !important;
        margin: 0 !important;
    }
    
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"]:hover {
        background-color: #2a3358 !important;
        border-color: #667eea !important;
        color: #ffffff !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    /* Hide the radio button dot */
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
        display: none !important;
    }
    
    /* Selected tab styling */
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"][aria-checked="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border-color: #667eea !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"]:has(input:checked) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border-color: #667eea !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Multiselect - darker background */
    .stMultiSelect {
        max-width: 50% !important;
    }
    
    .stMultiSelect [data-baseweb="select"] {
        background-color: #1e2749 !important;
        border-color: #2a3358 !important;
    }
    
    .stMultiSelect [data-baseweb="select"] > div {
        background-color: #1e2749 !important;
    }
    
    /* Multiselect input background */
    .stMultiSelect input {
        background-color: #1e2749 !important;
        color: #e0e0e0 !important;
    }
    
    /* Selected country tags */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #1e3a8a !important;
        border-color: #2563eb !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] span {
        color: #ffffff !important;
    }
    
    /* Selectbox styling */
    .stSelectbox [data-baseweb="select"] {
        background-color: #1e2749 !important;
        border-color: #2a3358 !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #1e2749 !important;
        color: #e0e0e0 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Dataframe background - DARK THEME */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        background-color: #1a1a1a;
    }

    /* Table itself */
    div[data-testid="stDataFrame"] table {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }

    /* Table header */
    div[data-testid="stDataFrame"] th {
        background-color: #2a2a2a !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Table cells */
    div[data-testid="stDataFrame"] td {
        background-color: #1f1f1f !important;
        color: #e0e0e0 !important;
    }
    
    /* Alternating rows */
    div[data-testid="stDataFrame"] tr:nth-child(even) td {
        background-color: #252525 !important;
    }
            
    /* Divider */
    hr {
        border-color: #3a3a3a !important;
        margin: 2rem 0 !important;
    }
    
    /* Column containers */
    [data-testid="column"] {
        background-color: #2a2a2a;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #3a3a3a;
    }
    
    /* Caption text */
    .caption {
        color: #909090 !important;
        font-size: 0.85rem !important;
    }
    
    /* Section headers in Deep Dive */
    .section-header {
        color: #667eea !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        margin-bottom: 1rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 8px;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #1e2749 !important;
        color: #ffffff !important;
        border-radius: 8px;
    }
    
    .streamlit-expanderContent {
        background-color: #1a1a1a !important;
        border: 1px solid #3a3a3a;
        border-radius: 0 0 8px 8px;
    }
    
    /* Info box styling for methodology */
    .methodology-box {
        background-color: #1e2749;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# LOAD DATA ONCE (GLOBAL) - WITH CACHING FOR FASTER LOAD
# -----------------------------------
df_url = "https://docs.google.com/spreadsheets/d/1E0lyCSxlC0ajNtzjpWo17TX5DEeEjd33E-j6c7fOBcg/export?format=csv"
df_overview_url = "https://docs.google.com/spreadsheets/d/1M8VQzniWDbRQIgaQ6bmgylWPGtMc3dBzPnQWxwBJPqU/export?format=csv&gid=147164817"


@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    return pd.read_csv(df_url)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_overview_data():
    return pd.read_csv(df_overview_url)

# Show loading spinner
with st.spinner('Loading data...'):
    try:
        df = load_data()
        df_overview = load_overview_data()
    except Exception as e:
        df = None
        df_overview = None
        st.error(f"Could not load the dataset: {e}")

# Clean column names
if df is not None:
    df.columns = [c.strip() for c in df.columns]
    
if df_overview is not None:
    df_overview.columns = [c.strip() for c in df_overview.columns]





# -----------------------------------
# HEADER
# -----------------------------------
st.markdown("# Evolution of Economic Prosperity and Well-being")


st.write("")
st.write("---")

# -----------------------------------
# NAVIGATION TABS - AT THE TOP
# -----------------------------------
tabs = ["Overview", "Analytical Insights", "Conclusions"]
selected_tab = st.radio("", tabs, horizontal=True, label_visibility="collapsed", key="main_tabs")

st.write("---")

# -----------------------------------
# GLOBAL COUNTRY SELECTOR - 60% WIDTH
# Only show for Overview and Analytical Insights tabs
# -----------------------------------
if selected_tab in ["Overview", "Analytical Insights"]:
    if df_overview is not None:
        all_countries = sorted(df_overview['Country Name'].unique())
        
        # Default selection
        default_countries = [
            "Japan", "China", "Indonesia",  # Asia
            "Germany", "Denmark", "Poland",  # Europe
            "South Africa", "Ghana", "Cote d'Ivoire",  # Africa
            "United States", "Chile", "Costa Rica"  # Americas
        ]
        
        # Filter default countries to only those available
        default_countries = [c for c in default_countries if c in all_countries]
        
        # Create a column layout for 60% width
        col_select, col_empty = st.columns([0.6, 0.4])
        
        with col_select:
            selected_countries = st.multiselect(
                "🌍 Select countries to compare",
                all_countries,
                default=default_countries,
                key="global_country_selector"
            )
    else:
        selected_countries = []
        st.write("")
        st.write("")
        st.write("")
        st.write("")
else:
    # No country selector for Conclusions tab
    selected_countries = []


# -----------------------------------
# OVERVIEW TAB
# -----------------------------------
if selected_tab == "Overview":
    st.write("---")
    st.write("")
    st.subheader("Which countries are best at converting economic prosperity into well-being?")
    st.write("")
    st.write("---")

    if df_overview is not None and len(selected_countries) > 0:
        # Filter data for selected countries
        df_filtered = df_overview[df_overview['Country Name'].isin(selected_countries)]
        
        # Rename columns to match the function expectations
        df_filtered_renamed = df_filtered.rename(columns={
            'score_pca_economics': 'Economic Success (PCA)',
            'score_pca_wellbeing': 'Well-Being (PCA)'
        })
        
        st.write("")
        
        # Create two columns for side-by-side bar charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Economic Index (EI)")
            fig_esi = plot_esi_ranking_bar(df_filtered_renamed, top_n=0, bottom_n=0)
            
            # Update styling to match Deep Dive charts
            fig_esi.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0', size=12),
                title=dict(
                    text='Country Ranking: Economic Index (EI, 2000-2023 Average)',
                    font=dict(size=16, color='#ffffff')
                ),
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    zerolinecolor='rgba(255,255,255,0.2)'
                ),
                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)'
                )
            )
            
            st.plotly_chart(fig_esi, use_container_width=True, key="esi_bar_chart")
        
        with col2:
            st.markdown("### Well-Being Index (WBI)")
            # Create a version of the function for well-being
            df_ranking = df_filtered_renamed.groupby('Country Name')['Well-Being (PCA)'].mean().reset_index()
            df_ranking.rename(columns={'Well-Being (PCA)': 'Avg_WTI'}, inplace=True)
            df_ranking_sorted = df_ranking.sort_values(by='Avg_WTI', ascending=False).reset_index(drop=True)
            
            import plotly.express as px
            fig_wti = px.bar(
                df_ranking_sorted,
                x='Avg_WTI',
                y='Country Name',
                orientation='h', 
                color='Avg_WTI',
                color_continuous_scale=px.colors.sequential.Teal,
                title='Country Ranking: Well-Being Index (WBI, 2000-2023 Average)',
                labels={'Avg_WTI': 'WBI', 'Country Name': ''}
            )
            
            sorted_country_list = df_ranking_sorted['Country Name'].tolist()
            fig_wti.update_layout(
                yaxis={
                    'categoryorder': 'array',
                    'categoryarray': sorted_country_list 
                },
                yaxis_autorange='reversed',
                showlegend=False,
                # Add styling to match Deep Dive charts
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e0e0e0', size=12),
                title=dict(font=dict(size=16, color='#ffffff')),
                xaxis=dict(
                    gridcolor='rgba(255,255,255,0.1)',
                    zerolinecolor='rgba(255,255,255,0.2)'
                ),
                yaxis_gridcolor='rgba(255,255,255,0.1)'
            )
            fig_wti.add_vline(x=0, line_width=2, line_dash="dash", line_color="red")
            
            st.plotly_chart(fig_wti, use_container_width=True, key="wti_bar_chart")

        st.write("---")
        
        # Quadrant analysis below
        st.markdown("### EI vs. WBI Quadrant Analysis")
        st.write("This chart shows how countries convert economic success into well-being.")
        st.write("")
        
        fig_quadrant = plot_esi_wti_quadrants(df_filtered_renamed)
        
        # Update styling to match Deep Dive charts - FIXED
        fig_quadrant.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0', size=12),
            title=dict(font=dict(size=16, color='#ffffff')),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                zerolinecolor='rgba(255,255,255,0.2)',
                title='Economic Index (EI)'
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                zerolinecolor='rgba(255,255,255,0.2)',
                title='Well-Being Index (WBI)'
            ),
            legend=dict(
                bgcolor='rgba(30,39,73,0.8)',
                bordercolor='rgba(255,255,255,0.2)',
                borderwidth=1,
                font=dict(color='#e0e0e0')
            )
        )
        
        st.plotly_chart(fig_quadrant, use_container_width=True, key="quadrant_chart")

        st.write("---")
        st.markdown(
            "### Key Findings\n\n"
            "Countries in the upper-right quadrant (Successful Translators) demonstrate both high economic success and high well-being outcomes. "
            "The analysis reveals different strategies countries employ to convert economic prosperity into quality of life improvements.\n\n"
            "Our indices are based on PCA (Principal Component Analysis) combining multiple economic and well-being indicators."
        )

        # Show both datasets
        st.write("---")
        with st.expander("📊 View Raw Data - Overview Dataset"):
            st.write(f"Loaded {len(df_overview)} rows of overview data")
            st.dataframe(df_overview, use_container_width=True)
        
        if df is not None:
            with st.expander("📊 View Raw Data - Detailed Indicators Dataset"):
                st.write(f"Loaded {len(df)} rows of detailed indicator data")
                st.dataframe(df, use_container_width=True)
        
    elif len(selected_countries) == 0:
        st.info("Please select at least one country from the selector above to view the comparison.")
    else:
        st.error("Overview dataset not available.")

# -----------------------------------
# ANALYTICAL INSIGHTS TAB
# -----------------------------------
elif selected_tab == "Analytical Insights":
    st.write("---")
    st.write("")
    st.subheader("How do countries compare across indicator level?")

    if df is not None and len(selected_countries) > 0:
        st.write("---")
        
        # Create two columns for Economic and Well-being indicators
        col_economic, col_wellbeing = st.columns(2)
        
        # Available indicators
        economic_indicators = [
            "GDP per capita",
            "Unemployment levels (%)",
            "Inflation (CPI, %))"
        ]
        
        wellbeing_indicators = [
            "Life expectancy at birth, total (years)",
            "Gini index"
        ]
        
        # ECONOMIC INDICATORS (Left Column)
        with col_economic:
            st.markdown('<p class="section-header">Economic Indicators</p>', unsafe_allow_html=True)
            
            selected_economic = st.selectbox(
                "Select Economic Indicator",
                economic_indicators,
                key="economic_selector"
            )
            
            fig_econ = plot_indicator_plotly(df, selected_countries, selected_economic)
            st.plotly_chart(fig_econ, use_container_width=True, key="economic_chart")
        
        # WELL-BEING INDICATORS (Right Column)
        with col_wellbeing:
            st.markdown('<p class="section-header">Well-being Indicators</p>', unsafe_allow_html=True)
            
            selected_wellbeing = st.selectbox(
                "Select Well-being Indicator",
                wellbeing_indicators,
                key="wellbeing_selector"
            )
            
            fig_well = plot_indicator_plotly(df, selected_countries, selected_wellbeing)
            st.plotly_chart(fig_well, use_container_width=True, key="wellbeing_chart")
            
    elif len(selected_countries) == 0:
        st.info("Please select at least one country from the selector above to view comparisons.")
    else:
        st.error("Dataset not available.")

# -----------------------------------
# CONCLUSIONS TAB
# -----------------------------------
elif selected_tab == "Conclusions":
    
    # KEY TAKEAWAYS SECTION
    st.markdown("""
    ### Key Takeaways
        
    - **Economic Performance**: The US clearly performs best at economic level, followed by Japan, Denmark and Germany 
    - **Well-Being**: Despite comparable economic performance, countries show differences in well-being levels, which is a result of differences in life expectancy and inequality. 
                The difference is especially pronounced for the US, which ranks high on the economic indicator but relatively low on the well-being indicator  
    
  
    """)
    st.write("")
    st.write("")
    st.write("")
    # METHODOLOGY SECTION - Simple text-based approach
    st.markdown("### 📊 Methodology")
    
    st.markdown("""
    <div class="methodology-box">
    <h4 style="color: #667eea; margin-top: 0;">Indices Used</h4>
    
    <p><strong>Economic Index (EI)</strong><br/>
    Components: GDP per capita, Unemployment levels, Inflation (CPI)<br/>
    Weighting: Principal Component Analysis (PCA)<br/>
    Source: IMF Data, own calculations</p>
    
    <p><strong>Well-Being Index (WBI)</strong><br/>
    Components: Life expectancy at birth, Gini Index<br/>
    Weighting: Principal Component Analysis (PCA)<br/>
    Source: World Bank Data, own calculations</p>
    
    <h4 style="color: #667eea; margin-top: 1.5rem;">Individual Indicators</h4>
    
    <p><strong>GDP per capita</strong> (Thousands, USD) -  Measures a country's economic output per person, used as proxy to assess average economic prosperity | Source: IMF Data</p>
    
    <p><strong>Unemployment levels</strong> (%) - Assesses labor market health and utilization of a country's workforce | Source: IMF Data</p>
    
    <p><strong>Inflation</strong> (CPI, Index) - Measures changes in price level, reflecting one aspect of macroeconomic stability  | Source: IMF Data</p>
    
    <p><strong>Life expectancy at birth</strong> (Years) - Assesses overall public health, quality of health care and living conditions | Source: World Bank Data</p>
    
    <p><strong>Gini Index</strong> - Measures income inequality, a higher GINI index means greater income nequality  | Source: World Bank Data</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    # COUNTRY SELECTION - Simple text format
    st.markdown("""
    <div class="methodology-box">
    <h4 style="color: #667eea; margin-top: 0;">🌍 Country Selection</h4>
    
    <p><strong>Selected Countries:</strong><br/>
    Asia: Japan, Indonesia<br/>
    Europe: Germany, Denmark, Poland<br/>
    Africa: South Africa<br/>
    Americas: United States, Chile, Costa Rica</p>
    
    <p><strong>Selection Rationale:</strong><br/>
    Countries were selected based on geographic diversity, robust data availability, 
    and representation across a spectrum of economic development levels.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.write("---")
    
    

# -----------------------------------
# FOOTER
# -----------------------------------
st.write("---")
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("🎈 Celebrate Progress"):
        st.balloons()
