**NYC Motor Vehicle Collisions Analysis
**
This repository contains the code and data used for the analysis of motor vehicle collisions in New York City. The study includes data preprocessing, statistical analysis and the creation of visualizations to understand the patterns and factors contributing to these collisions.

**Repository Structure
**Data Preprocessing & Visualization:
Jupyter Notebook used to clean and prepare the dataset for analysis.
Generating visualizations for exploratory data analysis and insights.

**Statistical Analysis:
**Python script containing the ANOVA test analysis performed in this study.

**Visualization using D3.js
**D3.js is utilized to create various charts and maps for analysis.

**Interactive Dashboard:
**Code for a centralized dashboard to grasp key findings with crash hotspots and insights.
Includes geospatial heatmaps, bar plots, line charts and more.

**Instructions:
**1. Ensure that the dataset Motor_Vehicle_Collisions_-_Crashes_20241120.csv is in the same directory.
2. Data Preprocessing & Visualization: Run each cell of data_visualization.ipynb on Jupyter Lab sequentially and see the results. to clean the dataset and generate initial visualizations.
3. Statistical Analysis: Use the command 'python statistical_test.py' to perform ANOVA test.
4. Visualization using D3.js: Open the index.html file in browser to view the results. (If not running directly, then execute command python -m http.server 8000 from the project location and then view the http://localhost:8000/index.html in browser)
5. Interactive Dashboard: Use the command 'streamlit run interactive_dashboard.py' to launch the Streamlit dashboard. Use the dashboard to explore crash hotspots, contributing factors, and other insights interactively.

**Requirements:
**Python 3.x
Pandas
Streamlit
Matplotlib
Seaborn
Folium
Altair
Plotly
Scipy
D3.js
