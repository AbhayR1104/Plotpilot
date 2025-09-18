import streamlit as st
import pandas as pd
import numpy as np
# Import all the functions from our new file
from plot_functions import *

# --- App Configuration ---
st.set_page_config(
    page_title="PlotPilot - Your Automated Chart Assistant",
    layout="wide"
)

# --- Initialize Session State ---
if 'chart_type' not in st.session_state:
    st.session_state.chart_type = None

# --- Functions to update session state ---
def set_chart_type(chart):
    st.session_state.chart_type = chart

# --- App Title ---
st.title("Welcome to PlotPilot 🚀")
st.write("Upload your cleaned data and get instant visualizations with ready-to-use code.")

# --- Sidebar for Data Upload ---
with st.sidebar:
    st.header("1. Upload Your Data")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

    st.divider()

    # --- NEW: CLEAR SELECTION BUTTON ---
    st.write("Done with a plot?")
    if st.button("Clear Plot Selection"):
        st.session_state.chart_type = None
        st.rerun()


# --- Main Panel ---
if uploaded_file is not None:
    try:
        # Read data based on file type
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success("File uploaded successfully!")
        
        # Attempt to convert all object columns to numeric where possible
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except:
                    pass

        st.subheader("Data Preview:")
        st.dataframe(df.head())
        st.divider()

        # --- Chart Selection Buttons ---
        st.subheader("2. Select a Chart Type")
        
        # A dictionary to map chart names to their functions
        plot_functions = {
            "Scatter Plot": generate_scatter_plot,
            "Line Plot": generate_line_plot,
            "Bar Chart": generate_bar_chart,
            "Histogram": generate_histogram,
            "Box Plot": generate_box_plot,
            "Violin Plot": generate_violin_plot,
            "Count Plot": generate_count_plot,
            "Heatmap": generate_heatmap,
            "Bubble Chart": generate_bubble_chart,
            "Pie Chart": generate_pie_chart,
            "Dot Plot": generate_dot_plot,
            "Radar Chart": generate_radar_chart,
        }

        # Create the 3x4 grid of buttons
        chart_names = list(plot_functions.keys())
        for i in range(0, len(chart_names), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(chart_names):
                    chart_name = chart_names[i+j]
                    with cols[j]:
                        st.button(chart_name, on_click=set_chart_type, args=(chart_name,), use_container_width=True)
        
        st.divider()

        # --- Call the selected plot function ---
        if st.session_state.chart_type:
            # Look up the function in the dictionary and call it
            selected_function = plot_functions[st.session_state.chart_type]
            selected_function(df)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Upload a CSV or Excel file to begin.")