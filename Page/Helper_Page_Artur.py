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
    plot_pca_scores_plotly
)

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
        background-color: #1a1a1a;
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
    
    /* Navigation tabs - Modern underline style */
    div.row-widget.stRadio > div {
        background-color: transparent;
        padding: 0;
        gap: 0;
        display: flex;
        justify-content: center;
        border-bottom: 2px solid #3a3a3a;
    }
    
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] {
        background-color: transparent !important;
        color: #b0b0b0 !important;
        padding: 1rem 2.5rem !important;
        border-radius: 0 !important;
        border: none !important;
        border-bottom: 3px solid transparent !important;
        transition: all 0.3s ease !important;
        font-weight: 400 !important;
        font-size: 1.3rem !important;
        cursor: pointer !important;
        margin: 0 !important;
        position: relative;
        bottom: -2px;
    }
    
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"]:hover {
        color: #ffffff !important;
        background-color: rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Hide the radio button dot */
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
        display: none !important;
    }
    
    /* Selected tab styling - using aria-checked attribute */
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"][aria-checked="true"] {
        color: #667eea !important;
        border-bottom-color: #667eea !important;
        font-weight: 700 !important;
        background-color: rgba(102, 126, 234, 0.15) !important;
    }
    
    /* Also try with input checked state */
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"]:has(input:checked) {
        color: #667eea !important;
        border-bottom-color: #667eea !important;
        font-weight: 700 !important;
        background-color: rgba(102, 126, 234, 0.15) !important;
    }
    
    /* Multiselect width control */
    .stMultiSelect {
        max-width: 50% !important;
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
    
    /* Dataframe */
    .stDataFrame {
        background-color: #2a2a2a;
        border-radius: 8px;
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
    
    /* Multiselect styling */
    .stMultiSelect [data-baseweb="select"] {
        background-color: #2a2a2a;
        border-color: #4a4a4a;
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# LOAD DATA ONCE (GLOBAL) - WITH CACHING FOR FASTER LOAD
# -----------------------------------
df_url = "https://docs.google.com/spreadsheets/d/1E0lyCSxlC0ajNtzjpWo17TX5DEeEjd33E-j6c7fOBcg/export?format=csv"
df_overview_url = "https://docs.google.com/spreadsheets/d/1JRp5v_2U4HMxl3aB_UZF7MHHPn3o0cAHSgn0ZeuFrvE/export?format=csv&gid=235949117"

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
st.markdown("# Evolution of Economic Prosperity and Well-being Globally")
st.markdown("#### Which countries are best at converting economic prosperity into well-being?")

st.write("")

# -----------------------------------
# NAVIGATION TABS
# -----------------------------------
tabs = ["Overview", "Deep Dive", "Conclusions"]
selected_tab = st.radio("", tabs, horizontal=True, label_visibility="collapsed")

st.write("---")

# -----------------------------------
# OVERVIEW TAB
# -----------------------------------
if selected_tab == "Overview":
    st.subheader("Overview")
    st.write("General introduction and global analysis.")

    if df_overview is not None:
        # Economic prosperity score comparison with country selector
        st.markdown("### Economic Prosperity Score Comparison (2000-2020)")
        st.write("This chart uses our calculated PCA-based economic prosperity scores.")
        st.write("")
        
        # Get unique countries from overview dataset
        all_countries_overview = sorted(df_overview['Country Name'].unique())
        
        # Default selection - key countries from different regions
        default_countries = [
            "Japan", "Indonesia",  # Asia
            "Germany", "Denmark", "Poland",  # Europe
            "South Africa",  # Africa
            "United States", "Chile", "Costa Rica"  # Americas
        ]
        
        # Filter default countries to only those available in dataset
        default_countries = [c for c in default_countries if c in all_countries_overview]
        
        selected_countries_overview = st.multiselect(
            "Select countries to compare",
            all_countries_overview,
            default=default_countries,
            key="overview_countries"
        )
        
        if len(selected_countries_overview) > 0:
            # Use the new PCA scores function
            fig_score = plot_pca_scores_plotly(df_overview, selected_countries_overview, "score_pca_economics")
            st.plotly_chart(fig_score, use_container_width=True, key="overview_chart")
        else:
            st.info("Please select at least one country to view the comparison.")

        st.write("---")
        st.markdown(
            "### Key Findings\n\n"
            "USA and Germany are most successful economically and excel at promoting well-being.\n\n"
            "For the purpose of our analysis we developed an economic indicator based on PCA (Principal Component Analysis)."
        )

        # Show dataset
        with st.expander("📊 View Raw Data"):
            st.write(f"Loaded {len(df_overview)} rows of overview data")
            st.dataframe(df_overview, use_container_width=True)
    else:
        st.error("Overview dataset not available.")

# -----------------------------------
# DEEP DIVE TAB
# -----------------------------------
elif selected_tab == "Deep Dive":
    st.subheader("How do countries compare across indicator level?")
    st.write("")

    if df is not None:
        # Country selection
        all_countries = sorted(df['Country Name'].unique())
        selected_countries = st.multiselect(
            "Select countries to compare (up to 5)",
            all_countries,
            default=["United States", "Germany", "Japan"],
            max_selections=5
        )
        
        if len(selected_countries) > 0:
            st.write("---")
            
            # Create two columns for Economic and Well-being indicators
            col_economic, col_wellbeing = st.columns(2)
            
            # ECONOMIC INDICATORS (Left Column)
            with col_economic:
                st.markdown('<p class="section-header">Economic Indicators</p>', unsafe_allow_html=True)
                
                # 1. GDP per capita
                fig1 = plot_indicator_plotly(df, selected_countries, "GDP per capita")
                st.plotly_chart(fig1, use_container_width=True)
                st.write("")
                
                # 2. Unemployment levels (%)
                fig2 = plot_indicator_plotly(df, selected_countries, "Unemployment levels (%)")
                st.plotly_chart(fig2, use_container_width=True)
                st.write("")
                
                # 3. Inflation (CPI, %))
                fig3 = plot_indicator_plotly(df, selected_countries, "Inflation (CPI, %))")
                st.plotly_chart(fig3, use_container_width=True)
            
            # WELL-BEING INDICATORS (Right Column)
            with col_wellbeing:
                st.markdown('<p class="section-header">Well-being Indicators</p>', unsafe_allow_html=True)
                
                # 4. Life expectancy at birth, total (years)
                fig4 = plot_indicator_plotly(df, selected_countries, "Life expectancy at birth, total (years)")
                st.plotly_chart(fig4, use_container_width=True)
                st.write("")
                
                # 5. Gini index
                fig5 = plot_indicator_plotly(df, selected_countries, "Gini index")
                st.plotly_chart(fig5, use_container_width=True)
                st.write("")
                
                # 6. Current health expenditure (% of GDP)
                fig6 = plot_indicator_plotly(df, selected_countries, "Current health expenditure (% of GDP)")
                st.plotly_chart(fig6, use_container_width=True)
        else:
            st.info("Please select at least one country to view comparisons.")
    else:
        st.error("Dataset not available.")

# -----------------------------------
# CONCLUSIONS TAB
# -----------------------------------
elif selected_tab == "Conclusions":
    st.subheader("Conclusions")
    st.write("Summary and key insights from our analysis.")
    
    st.write("")
    st.markdown("""
    ### Key Takeaways
    
    Our analysis reveals important patterns in how countries convert economic prosperity into well-being:
    
    - **Economic Performance**: Developed nations show strong GDP growth but varying efficiency in well-being conversion
    - **Health Outcomes**: Healthcare spending doesn't always correlate directly with life expectancy
    - **Inequality**: Income distribution varies significantly across similar GDP levels
    - **Regional Patterns**: Different continents show distinct approaches to balancing growth and well-being
    
    ### Future Considerations
    
    Understanding these relationships helps policymakers design more effective strategies for improving quality of life.
    """)

# -----------------------------------
# FOOTER
# -----------------------------------
st.write("---")
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("🎈 Celebrate Progress"):
        st.balloons()