# PlotPilot 🚀

## Description
PlotPilot is an interactive web application built with Streamlit that allows users to upload a dataset (CSV or Excel) and instantly generate a wide variety of customized, interactive plots. The app also provides the Python code used to create each visualization.

### Key Features
- **Advanced Data Cleaning**:
  - Trim whitespace & normalize text columns
  - Fill missing values using median/mode or drop rows
  - Convert numeric-like text safely
  - Standardize categorical text
  - Detect and optionally remove numeric outliers using IQR
  - Drop duplicates and constant columns
  - Summary of all cleaning actions performed
- **Data Analysis**:
  - Statistical overview of numeric and categorical columns
  - Row count metrics (original vs cleaned)
- **Visualization**:
  - Interactive plots including Scatter, Line, Bar, Histogram, Box, Violin, Count, Heatmap, Bubble, Pie, Dot, and Radar charts
  - Python code for every plot provided for reproducibility
- **Download Option**:
  - Export cleaned dataset as CSV for further use

## How to Run Locally
1. Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd PlotPilot
    ```
2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## Usage
1. Upload a CSV or Excel file.
2. Use the sidebar to clean and prepare your data:
   - Choose missing value handling
   - Optionally drop empty columns, normalize text, or remove outliers
3. Preview your cleaned data and see cleaning summaries.
4. Select your preferred chart type and visualize your data.
5. Download the cleaned dataset for offline use.


## License
MIT License
