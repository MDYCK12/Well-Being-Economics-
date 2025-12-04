import streamlit as st
import io
import pandas as pd
import matplotlib.pyplot as plt
import sys

# Allow importing from the Functions folder
sys.path.append("Functions")

# Import our functions
from functions import filter_data, plot_indicator


# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Economical growth vs wellbeing",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

st.markdown("# Economical growth vs wellbeing")


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

        st.markdown("### Indicators for Germany")

        # ---- Filter data using our function ----
        df_germany_unemp = filter_data(
            df,
            country="Germany",
            indicator="GDP per capita"
        )

        # ---- Create figure using our function ----
        fig = plot_indicator(
            df_germany_unemp,
            country="Germany",
            indicator="GDP per capita"
        )

        # ---- Save figure to in-memory PNG and display smaller ----
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=180, bbox_inches="tight")
        buf.seek(0)
        st.image(buf, width=300)  # adjust width in pixels as needed

        plt.close(fig)  # free memory

        # ---- Filter data using our function ----
        df_germany_unemp = filter_data(
            df,
            country="Germany",
            indicator="Inflation (CPI, %))"
        )

        # ---- Create figure using our function ----
        fig = plot_indicator(
            df_germany_unemp,
            country="Germany",
            indicator="Inflation (CPI, %))"
        )

        # ---- Save figure to in-memory PNG and display smaller ----
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=180, bbox_inches="tight")
        buf.seek(0)
        st.image(buf, width=300)  # adjust width in pixels as needed

        plt.close(fig)  # free memory


        # ---- Filter data using our function ----
        df_germany_unemp = filter_data(
            df,
            country="Germany",
            indicator="Unemployment levels (%)"
        )

        # ---- Create figure using our function ----
        fig = plot_indicator(
            df_germany_unemp,
            country="Germany",
            indicator="Unemployment levels (%)"
        )

        # ---- Save figure to in-memory PNG and display smaller ----
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=180, bbox_inches="tight")
        buf.seek(0)
        st.image(buf, width=300)  # adjust width in pixels as needed

        plt.close(fig)  # free memory



        # ---- Filter data using our function ----
        df_germany_unemp = filter_data(
            df,
            country="Germany",
            indicator="National savings (% GDP)"
        )

        # ---- Create figure using our function ----
        fig = plot_indicator(
            df_germany_unemp,
            country="Germany",
            indicator="National savings (% GDP)"
        )

        # ---- Save figure to in-memory PNG and display smaller ----
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=180, bbox_inches="tight")
        buf.seek(0)
        st.image(buf, width=300)  # adjust width in pixels as needed

        plt.close(fig)  # free memory


        

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
