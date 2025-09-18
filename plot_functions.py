import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def generate_scatter_plot(df):
    st.subheader("3. Options for: Scatter Plot")
    numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
    categorical_columns = list(df.select_dtypes(['object', 'category']).columns)
    x_axis = st.selectbox("Select the X-axis (numeric)", numeric_columns, key="scatter_x")
    y_axis = st.selectbox("Select the Y-axis (numeric)", numeric_columns, key="scatter_y")
    hue_column = st.selectbox("Color by (optional)", [None] + categorical_columns, key="scatter_hue")
    
    if st.button(f"Generate Plot"):
        fig = px.scatter(df, x=x_axis, y=y_axis, color=hue_column, title=f"{x_axis} vs. {y_axis}")
        st.plotly_chart(fig, use_container_width=True)
        code_string = f"fig = px.scatter(df, x='{x_axis}', y='{y_axis}', color={repr(hue_column)})\nfig.show()"
        st.code(code_string, language='python')

def generate_line_plot(df):
    st.subheader("3. Options for: Line Plot")
    numeric_columns = list(df.select_dtypes(['float', 'int', 'datetime']).columns)
    categorical_columns = list(df.select_dtypes(['object', 'category']).columns)
    x_axis_line = st.selectbox("Select the X-axis (time or numeric)", numeric_columns, key="line_x")
    y_axis_line = st.selectbox("Select the Y-axis (numeric)", numeric_columns, key="line_y")
    color_line = st.selectbox("Break lines by (optional)", [None] + categorical_columns, key="line_color")
    
    if st.button(f"Generate Plot"):
        fig = px.line(df, x=x_axis_line, y=y_axis_line, color=color_line, title=f"Trend of {y_axis_line} over {x_axis_line}")
        st.plotly_chart(fig, use_container_width=True)
        code_string = f"fig = px.line(df, x='{x_axis_line}', y='{y_axis_line}', color={repr(color_line)})\nfig.show()"
        st.code(code_string, language='python')

def generate_bar_chart(df):
    st.subheader("3. Options for: Bar Chart")
    categorical_columns = list(df.select_dtypes(['object', 'category']).columns)
    numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
    x_axis_bar = st.selectbox("Select the X-axis (categorical)", categorical_columns, key="bar_x")
    y_axis_bar = st.selectbox("Select the Y-axis (numeric)", numeric_columns, key="bar_y")
    
    if st.button(f"Generate Plot"):
        fig = px.histogram(df, x=x_axis_bar, y=y_axis_bar, color=x_axis_bar, histfunc='avg', title=f"Average {y_axis_bar} by {x_axis_bar}")
        fig.update_layout(yaxis_title=f"Average of {y_axis_bar}")
        st.plotly_chart(fig, use_container_width=True)
        code_string = f"fig = px.histogram(df, x='{x_axis_bar}', y='{y_axis_bar}', color='{x_axis_bar}', histfunc='avg')\nfig.show()"
        st.code(code_string, language='python')

def generate_histogram(df):
    st.subheader("3. Options for: Histogram")
    numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
    hist_column = st.selectbox("Select a column (numeric)", numeric_columns, key="hist_col")
    
    if st.button(f"Generate Plot"):
        fig = px.histogram(df, x=hist_column, title=f"Distribution of {hist_column}", marginal="box")
        st.plotly_chart(fig, use_container_width=True)
        code_string = f"fig = px.histogram(df, x='{hist_column}', title='Distribution of {hist_column}', marginal='box')\nfig.show()"
        st.code(code_string, language='python')

def generate_box_plot(df):
    st.subheader("3. Options for: Box Plot")
    categorical_columns = list(df.select_dtypes(['object', 'category']).columns)
    numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
    x_axis_box = st.selectbox("Select the X-axis (categorical)", categorical_columns, key="box_x")
    y_axis_box = st.selectbox("Select the Y-axis (numeric)", numeric_columns, key="box_y")

    if st.button(f"Generate Plot"):
        fig = px.box(df, x=x_axis_box, y=y_axis_box, color=x_axis_box, title=f"Distribution of {y_axis_box} by {x_axis_box}")
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("How to Read a Box Plot 📖"):
            st.markdown("A box plot shows the distribution of data. Hover over it to see the median, quartiles, and outliers.")
        code_string = f"fig = px.box(df, x='{x_axis_box}', y='{y_axis_box}', color='{x_axis_box}')\nfig.show()"
        st.code(code_string, language='python')

def generate_violin_plot(df):
    st.subheader("3. Options for: Violin Plot")
    categorical_columns = list(df.select_dtypes(['object', 'category']).columns)
    numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
    x_axis_violin = st.selectbox("Select the X-axis (categorical)", categorical_columns, key="violin_x")
    y_axis_violin = st.selectbox("Select the Y-axis (numeric)", numeric_columns, key="violin_y")

    if st.button(f"Generate Plot"):
        fig = px.violin(df, x=x_axis_violin, y=y_axis_violin, color=x_axis_violin, box=True, title=f"Distribution of {y_axis_violin} by {x_axis_violin}")
        st.plotly_chart(fig, use_container_width=True)
        code_string = f"fig = px.violin(df, x='{x_axis_violin}', y='{y_axis_violin}', color='{x_axis_violin}', box=True)\nfig.show()"
        st.code(code_string, language='python')

def generate_count_plot(df):
    st.subheader("3. Options for: Count Plot")
    categorical_columns = list(df.select_dtypes(['object', 'category']).columns)
    count_column = st.selectbox("Select a column to count (categorical)", categorical_columns, key="count_col")
    
    if st.button(f"Generate Plot"):
        fig = px.histogram(df, x=count_column, title=f"Count of {count_column}", color=count_column)
        fig.update_layout(yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)
        code_string = f"fig = px.histogram(df, x='{count_column}', title='Count of {count_column}', color='{count_column}')\nfig.show()"
        st.code(code_string, language='python')

def generate_heatmap(df):
    st.subheader("3. Options for: Heatmap")
    st.info("The heatmap shows the correlation between all numeric columns in your dataset.")
    if st.button(f"Generate Plot"):
        numeric_df = df.select_dtypes(include=np.number)
        corr_matrix = numeric_df.corr()
        fig = px.imshow(corr_matrix, text_auto=True, title="Correlation Heatmap of Numeric Variables")
        st.plotly_chart(fig, use_container_width=True)
        code_string = "numeric_df = df.select_dtypes(include=np.number)\ncorr_matrix = numeric_df.corr()\nfig = px.imshow(corr_matrix, text_auto=True)\nfig.show()"
        st.code(code_string, language='python')

def generate_bubble_chart(df):
    st.subheader("3. Options for: Bubble Chart")
    st.info("A bubble chart is a scatter plot where the size of the bubble represents a third numeric variable.")
    numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
    categorical_columns = list(df.select_dtypes(['object', 'category']).columns)
    
    x_axis = st.selectbox("Select the X-axis (numeric)", numeric_columns, key="bubble_x")
    y_axis = st.selectbox("Select the Y-axis (numeric)", numeric_columns, key="bubble_y")
    size_col = st.selectbox("Select the Size variable (numeric)", numeric_columns, key="bubble_size")
    color_col = st.selectbox("Color by (optional)", [None] + categorical_columns, key="bubble_color")
    
    if st.button(f"Generate Plot"):
        fig = px.scatter(df, x=x_axis, y=y_axis, size=size_col, color=color_col, title=f"{x_axis} vs. {y_axis}, Sized by {size_col}")
        st.plotly_chart(fig, use_container_width=True)
        code_string = f"fig = px.scatter(df, x='{x_axis}', y='{y_axis}', size='{size_col}', color={repr(color_col)})\nfig.show()"
        st.code(code_string, language='python')

def generate_pie_chart(df):
    st.subheader("3. Options for: Pie Chart")
    categorical_columns = list(df.select_dtypes(['object', 'category']).columns)
    numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
    
    names_col = st.selectbox("Select the column for labels (categorical)", categorical_columns, key="pie_names")
    values_col = st.selectbox("Select the column for values (numeric)", numeric_columns, key="pie_values")
    
    if st.button(f"Generate Plot"):
        fig = px.pie(df, names=names_col, values=values_col, title=f"Proportion of {values_col} by {names_col}")
        st.plotly_chart(fig, use_container_width=True)
        code_string = f"fig = px.pie(df, names='{names_col}', values='{values_col}')\nfig.show()"
        st.code(code_string, language='python')

def generate_dot_plot(df):
    st.subheader("3. Options for: Dot Plot")
    st.info("A dot plot is a clean alternative to a bar chart for comparing values across categories.")
    numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
    categorical_columns = list(df.select_dtypes(['object', 'category']).columns)
    
    x_col = st.selectbox("Select the numeric axis", numeric_columns, key="dot_x")
    y_col = st.selectbox("Select the category axis", categorical_columns, key="dot_y")
    color_col = st.selectbox("Color by (optional)", [None] + categorical_columns, key="dot_color")
    
    if st.button(f"Generate Plot"):
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{x_col} by {y_col}")
        fig.update_traces(marker=dict(size=12)) # Make dots larger
        st.plotly_chart(fig, use_container_width=True)
        code_string = f"fig = px.scatter(df, x='{x_col}', y='{y_col}', color={repr(color_col)})\nfig.show()"
        st.code(code_string, language='python')

import plotly.graph_objects as go # Make sure this import is at the top of plot_functions.py

def generate_radar_chart(df):
    st.subheader("3. Options for: Radar Chart")
    st.info("A radar chart compares multiple numeric variables for one or more categories.")
    
    categorical_columns = list(df.select_dtypes(['object', 'category']).columns)
    numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
    
    category_col = st.selectbox("Select the main category to compare", categorical_columns, key="radar_cat")
    numeric_vars = st.multiselect("Select the numeric variables to display", numeric_columns, key="radar_num")
    
    if st.button("Generate Plot"):
        if not numeric_vars:
            st.warning("Please select at least one numeric variable.")
        elif len(df[category_col].unique()) > 10:
             st.warning("Radar charts are best for comparing a few categories (less than 10). Please filter your data.")
        else:
            # Melt dataframe
            id_vars = [category_col]
            value_vars = numeric_vars
            melted_df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='Metric', value_name='Value')

            # Build radar chart manually
            fig = go.Figure()
            for cat in melted_df[category_col].unique():
                subset = melted_df[melted_df[category_col] == cat]
                fig.add_trace(go.Scatterpolar(
                    r=subset["Value"],
                    theta=subset["Metric"],
                    mode='lines+markers',
                    name=str(cat),
                    fill='toself'  # <-- THIS IS THE KEY ADDITION
                ))

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                title=f"Comparison of Metrics for {category_col}"
            )

            st.plotly_chart(fig, use_container_width=True)
            
            # The generated code should also reflect this more robust method
            code_string = f"""
import plotly.graph_objects as go
# Radar charts often require reshaping the data from wide to long format
id_vars = ['{category_col}']
value_vars = {numeric_vars}
melted_df = pd.melt(df, id_vars=id_vars, value_vars=value_vars, var_name='Metric', value_name='Value')

fig = go.Figure()
for cat in melted_df['{category_col}'].unique():
    subset = melted_df[melted_df['{category_col}'] == cat]
    fig.add_trace(go.Scatterpolar(
        r=subset["Value"],
        theta=subset["Metric"],
        mode='lines+markers',
        name=str(cat),
        fill='toself'
    ))
fig.show()"""
            st.code(code_string, language='python')