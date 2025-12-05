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
#   /.../Well-Being-Economics-
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

@st.cache_data
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
tabs = ["Overview", "Asia", "Europe", "Africa", "Americas", "Conclusions"]
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
elif selected_tab == "Asia":
    st.subheader("Asia")
    st.write("Analysis for Asian countries.")

elif selected_tab == "Europe":
    st.subheader("Europe")
    st.write("Analysis for European countries.")

elif selected_tab == "Africa":
    st.subheader("Africa")
    st.write("Analysis for African countries.")

elif selected_tab == "Americas":
    st.subheader("Americas")
    st.write("Analysis for countries in North and South America.")

elif selected_tab == "Conclusions":
    st.subheader("Conclusions")
    st.write("Summary and key insights.")


# -----------------------------------
# EXTRA BUTTON
# -----------------------------------
if st.button("Send balloons!"):
    st.balloons()
