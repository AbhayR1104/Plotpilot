import streamlit as st
import pandas as pd
import numpy as np
import io
from contextlib import redirect_stdout
from plot_functions import *

# ----------------------------
# App Configuration
# ----------------------------
st.set_page_config(page_title="PlotPilot", layout="wide")

# ----------------------------
# Initialize Session State
# ----------------------------
if 'chart_type' not in st.session_state:
    st.session_state.chart_type = None
if 'cleaned_df' not in st.session_state:
    st.session_state.cleaned_df = None
if 'original_df' not in st.session_state:
    st.session_state.original_df = None
if 'cleaning_summary' not in st.session_state:
    st.session_state.cleaning_summary = []
if 'uploaded_file_name' not in st.session_state:
    st.session_state.uploaded_file_name = None

# ----------------------------
# Functions
# ----------------------------
def set_chart_type(chart):
    st.session_state.chart_type = chart

def clean_data(df, normalize_text=True, drop_empty_cols=True, missing_choice="Fill", remove_outliers=False):
    df = df.copy()
    summary = []

    # 1. Remove duplicates
    duplicates_before = df.duplicated().sum()
    if duplicates_before > 0:
        df.drop_duplicates(inplace=True)
        summary.append(f"✅ Removed {duplicates_before} duplicate row(s).")

    # 2. Trim and normalize text
    object_cols = df.select_dtypes(include=['object']).columns
    if len(object_cols) > 0:
        df[object_cols] = df[object_cols].apply(lambda x: x.str.strip())
        if normalize_text:
            df[object_cols] = df[object_cols].apply(lambda x: x.str.lower())
            summary.append("✅ Trimmed whitespace & normalized text columns to lowercase.")
        else:
            summary.append("✅ Trimmed whitespace in text columns.")

    # 3. Drop completely empty columns
    if drop_empty_cols:
        empty_cols = [col for col in df.columns if df[col].isnull().all()]
        if empty_cols:
            df.drop(columns=empty_cols, inplace=True)
            summary.append(f"🗑️ Dropped {len(empty_cols)} empty column(s): {empty_cols}")

    # 4. Handle missing values
    if missing_choice == "Fill":
        for col in df.columns:
            if df[col].isnull().any():
                missing_count = df[col].isnull().sum()
                if pd.api.types.is_numeric_dtype(df[col]):
                    median = df[col].median()
                    df[col].fillna(median, inplace=True)
                    summary.append(f"✅ Filled {missing_count} missing value(s) in numeric column '{col}' with median ({median:.2f}).")
                else:
                    mode = df[col].mode().iloc[0] if not df[col].mode().empty else "Unknown"
                    df[col].fillna(mode, inplace=True)
                    summary.append(f"✅ Filled {missing_count} missing value(s) in categorical column '{col}' with mode ('{mode}').")
    elif missing_choice == "Drop":
        before_rows = df.shape[0]
        df.dropna(inplace=True)
        dropped = before_rows - df.shape[0]
        summary.append(f"🗑️ Dropped {dropped} row(s) containing missing values.")
    else:
        summary.append("⚠️ Left missing values as NaN (no imputation).")

    # 5. Convert numeric-like text safely
    conversion_report = {}
    for col in object_cols:
        try:
            df[col] = pd.to_numeric(df[col], errors="raise")
            conversion_report[col] = "Converted to numeric"
        except Exception:
            df[col] = df[col].astype(str).str.strip()
            conversion_report[col] = "Kept as text"
    if conversion_report:
        for k, v in conversion_report.items():
            summary.append(f"🔄 Column '{k}': {v}")

    # 6. Standardize categorical text (title case)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.title()

    # 7. Convert datetime columns
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ['date', 'time', 'day']):
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                summary.append(f"📅 Converted '{col}' to datetime.")
            except:
                pass

    # 8. Drop irrelevant columns (all null or constant)
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, df.nunique() > 1]

    # 9. Outlier handling
    numeric_cols = df.select_dtypes(include=np.number).columns
    if remove_outliers:
        outlier_report = {}
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            before = df.shape[0]
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
            removed = before - df.shape[0]
            if removed > 0:
                outlier_report[col] = removed
        if outlier_report:
            for k, v in outlier_report.items():
                summary.append(f"🗑️ Removed {v} outlier(s) from '{k}' using IQR.")
        else:
            summary.append("✅ No outliers detected/removed with IQR.")
    else:
        for col in numeric_cols:
            mean, std = df[col].mean(), df[col].std()
            if std > 0:
                outliers = df[(df[col] - mean).abs() > 3 * std].shape[0]
                if outliers > 0:
                    summary.append(f"⚠️ Detected {outliers} potential outlier(s) in '{col}' (|z| > 3). Not removed.")

    return df, summary

# ----------------------------
# Sidebar Controls
# ----------------------------
with st.sidebar:
    st.header("1. Upload Your Data")
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file and st.session_state.get('uploaded_file_name') != uploaded_file.name:
        st.session_state.cleaned_df = None
        st.session_state.original_df = None
        st.session_state.cleaning_summary = []
        st.session_state.uploaded_file_name = uploaded_file.name

    st.divider()
    st.header("2. Data Cleaning Options")

    missing_choice = st.radio(
        "Handle Missing Values:",
        ["Fill", "Drop", "Leave as NaN"],
        index=0
    )
    drop_empty_cols = st.checkbox("Drop completely empty columns", value=True)
    normalize_text = st.checkbox("Normalize text to lowercase", value=True)
    remove_outliers = st.checkbox("Remove numeric outliers (IQR method)", value=False)

    if uploaded_file:
        if st.button("Clean & Prepare Data", use_container_width=True):
            if st.session_state.original_df is not None:
                df, summary = clean_data(
                    st.session_state.original_df,
                    normalize_text=normalize_text,
                    drop_empty_cols=drop_empty_cols,
                    missing_choice=missing_choice,
                    remove_outliers=remove_outliers
                )
                st.session_state.cleaned_df = df
                st.session_state.cleaning_summary = summary
                st.toast("Data has been cleaned!", icon="✅")

        if st.session_state.cleaned_df is not None:
            if st.button("Revert to Raw Data", use_container_width=True):
                st.session_state.cleaned_df = None
                st.session_state.cleaning_summary = []
                st.toast("Reverted to raw data.", icon="↩️")

    st.divider()
    st.write("Done with a plot?")
    if st.button("Clear Plot Selection"):
        st.session_state.chart_type = None
        st.rerun()

# ----------------------------
# Main Panel
# ----------------------------
if uploaded_file is not None:
    try:
        if st.session_state.original_df is None:
            if uploaded_file.name.endswith('.csv'):
                st.session_state.original_df = pd.read_csv(uploaded_file)
            else:
                st.session_state.original_df = pd.read_excel(uploaded_file)

        df_to_display = (
            st.session_state.cleaned_df
            if st.session_state.cleaned_df is not None
            else st.session_state.original_df
        )

        st.success("File loaded successfully!")

        original_rows = st.session_state.original_df.shape[0]
        cleaned_rows = (
            st.session_state.cleaned_df.shape[0]
            if st.session_state.cleaned_df is not None
            else original_rows
        )
        rows_removed = original_rows - cleaned_rows

        st.subheader("Data Preview:")
        st.dataframe(df_to_display.head())
        st.divider()

        with st.expander("📊 Data Cleaning & Analysis"):
            if st.session_state.cleaning_summary:
                st.subheader("Cleaning Actions Performed")
                for action in st.session_state.cleaning_summary:
                    st.markdown(f"- {action}")
                st.divider()

            st.subheader("Cleaning Results")
            col1, col2, col3 = st.columns(3)
            col1.metric("Original Rows", f"{original_rows:,}")
            col2.metric("Cleaned Rows", f"{cleaned_rows:,}")
            col3.metric("Rows Removed", f"{rows_removed:,}")

            st.subheader("Statistical Overview of Displayed Data")
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                df_to_display.info()
            info_str = buffer.getvalue()
            st.text("Dataframe Info:")
            st.text(info_str)

            st.text("Numeric Column Statistics:")
            st.dataframe(df_to_display.describe(include=np.number))

            st.text("Categorical Column Statistics:")
            st.dataframe(df_to_display.describe(include=['object', 'category']))

            # ----------------------------
            # Download Button
            # ----------------------------
            csv_buffer = io.StringIO()
            df_to_display.to_csv(csv_buffer, index=False)
            st.download_button(
                "⬇️ Download Cleaned CSV",
                data=csv_buffer.getvalue(),
                file_name="cleaned_data.csv",
                mime="text/csv"
            )

        # ----------------------------
        # Chart Selection Buttons
        # ----------------------------
        st.subheader("3. Select a Chart Type")
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

        chart_names = list(plot_functions.keys())
        for i in range(0, len(chart_names), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(chart_names):
                    chart_name = chart_names[i+j]
                    with cols[j]:
                        st.button(
                            chart_name,
                            on_click=set_chart_type,
                            args=(chart_name,),
                            use_container_width=True,
                        )

        # Call the selected plot function
        if st.session_state.chart_type:
            selected_function = plot_functions[st.session_state.chart_type]
            selected_function(df_to_display)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Upload a CSV or Excel file to begin.")
