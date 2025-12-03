import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from numpy.random import default_rng as rng

st.set_page_config(
    page_title="Economical growth vs wellbeing",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

# Big title that matches page title
st.markdown("# Economical growth vs wellbeing")

# --- TAB BUTTONS ---
tabs = ["Overview", "Asia", "Europe", "Africa", "Americas", "Conclusions"]
selected_tab = st.radio(
    "Navigation",
    tabs,
    horizontal=True
)

# defining the plot
arr = rng(0).normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

# Load the IMF data from Google Sheets
imf_url = "https://docs.google.com/spreadsheets/d/1BV0koOEqQs580tEPGv9bpZYUfY8q8UTfZGTcEoK_VtQ/export?format=csv&gid=1952168269"

st.write("---")  # a separator line

# --- CONTENT FOR EACH TAB ---
if selected_tab == "Overview":
    st.subheader("Overview")
    st.write("General introduction and global analysis.")
    st.pyplot(fig)

    with st.spinner("Loading IMF data..."):
        try:
            imf_data = pd.read_csv(imf_url)
            st.write(f"Loaded {len(imf_data)} rows of IMF data")
            st.dataframe(imf_data, use_container_width=True)
        except Exception as e:
            st.error(f"Could not load IMF data: {e}")
            st.write("Problem with loading the data")

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

# Example button
if st.button("Send balloons!"):
    st.balloons()


