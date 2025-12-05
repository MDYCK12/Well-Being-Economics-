import streamlit as st
import io
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

st.cache_data.clear()
st.cache_resource.clear()

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
    plot_two_indicators_long
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Evolution of economic prosperity and well-being globally",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

st.markdown(
    "# Evolution of economic prosperity and well-being globally\n"
    "#### Which countries are best at converting economic prosperity into well-being?"
)

# -----------------------------------
# LOAD DATA ONCE (GLOBAL)
# -----------------------------------
df_url = "https://docs.google.com/spreadsheets/d/1E0lyCSxlC0ajNtzjpWo17TX5DEeEjd33E-j6c7fOBcg/export?format=csv"

# @st.cache_data
def load_data():
    return pd.read_csv(df_url)

try:
    df = load_data()
except Exception as e:
    df = None
    st.error(f"Could not load the dataset: {e}")

# Clean column names
if df is not None:
    df.columns = [c.strip() for c in df.columns]

# -----------------------------------
# NAVIGATION TABS
# -----------------------------------
tabs = ["Overview", "Health", "Poverty and unemployment", "GDP and birth rate", "Conclusions"]
selected_tab = st.radio("Navigation", tabs, horizontal=True)

st.write("---")

# -----------------------------------
# OVERVIEW TAB
# -----------------------------------
if selected_tab == "Overview":
    st.subheader("Overview")
    st.write("General introduction and global analysis.")

    if df is not None:

        # ---------------------------------------
        # PARAMETERS FOR THE COMPARISON FUNCTION
        # ---------------------------------------
        countries = ["United States", "Germany", "Japan"]
        ind1 = "Life expectancy at birth, total (years)"
        ind2 = "GDP per capita"

        # ---------------------------------------
        # CALL THE FUNCTION FROM functions.py
        # ---------------------------------------
        fig = plot_two_indicators_long(df, countries, ind1, ind2)

        # ---------------------------------------
        # DISPLAY FIGURE IN STREAMLIT
        # ---------------------------------------
        st.pyplot(fig)

        st.write("---")

        # Show dataset
        st.write(f"Loaded {len(df)} rows of data")
        st.dataframe(df, use_container_width=True)

    else:
        st.error("Dataset not available.")

# -----------------------------------
# OTHER TABS
# -----------------------------------
# -----------------------------------
# HEALTH TAB
# -----------------------------------
elif selected_tab == "Health":
    st.subheader("Health")
    st.write("Visualisation of health care expenditure and life expectancy across countries.")

    if df is not None:
        # ----------------------------
        # First row: Europe & Americas
        # ----------------------------
        col1, col2 = st.columns(2)

        # Plot 1: Europe
        with col1:
            st.markdown("### Europe")
            countries_europe = ["Germany", "Poland", "Denmark"]
            ind1 = "Current health expenditure (% of GDP)"
            ind2 = "Life expectancy at birth, total (years)"
            fig1 = plot_two_indicators_long(df, countries_europe, ind1, ind2)
            st.pyplot(fig1)
            st.caption(f"{ind1} vs {ind2}")

        # Plot 2: Americas
        with col2:
            st.markdown("### Americas")
            countries_americas = ["United States", "Chile", "Costa Rica"]
            fig2 = plot_two_indicators_long(df, countries_americas, ind1, ind2)
            st.pyplot(fig2)
            st.caption(f"{ind1} vs {ind2}")

        # ----------------------------
        # Second row: Asia & Africa
        # ----------------------------
        col3, col4 = st.columns(2)

        # Plot 3: Asia
        with col3:
            st.markdown("### Asia")
            countries_asia = ["Japan", "China", "Indonesia"]
            fig3 = plot_two_indicators_long(df, countries_asia, ind1, ind2)
            st.pyplot(fig3)
            st.caption(f"{ind1} vs {ind2}")

        # Plot 4: Africa
        with col4:
            st.markdown("### Africa")
            countries_africa = ["South Africa", "Ghana", "Cote d'Ivoire"]
            fig4 = plot_two_indicators_long(df, countries_africa, ind1, ind2)
            st.pyplot(fig4)
            st.caption(f"{ind1} vs {ind2}")

    else:
        st.error("Dataset not available.")




elif selected_tab == "Poverty and unemployment":
    st.subheader("Poverty and unemployment")
    st.write("Visualisation of poverty and unemployment rates across countries")

elif selected_tab == "GDP and birth rate":
    st.subheader("GDP and birth rate")
    st.write("Visualisation of GDP per capita and birth rates across countries.")

elif selected_tab == "Conclusions":
    st.subheader("Conclusions")
    st.write("Summary and key insights.")

# -----------------------------------
# EXTRA BUTTON
# -----------------------------------
if st.button("Send balloons!"):
    st.balloons()
