import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
import altair as alt
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="NYC Motor Vehicle Collisions Dashboard")

# Load the dataset
st.title("NYC Motor Vehicle Collisions Dashboard")
df = pd.read_csv("Motor_Vehicle_Collisions_-_Crashes_20241120.csv")

# Data overview
st.sidebar.header("Data Overview")
st.sidebar.write("Number of rows: ", df.shape[0])
st.sidebar.write("Number of columns: ", df.shape[1])
st.write("### Sample Data")
st.write(df.tail())

# Clean data for geospatial plots
df = df.dropna(subset=['LATITUDE', 'LONGITUDE'])
df = df[(df['LATITUDE'] != 0) & (df['LONGITUDE'] != 0)]

# Create CRASH_DATETIME column
df['CRASH_DATETIME'] = pd.to_datetime(df['CRASH DATE'] + ' ' + df['CRASH TIME'], errors='coerce')

# Geospatial Crash Heatmap
st.write("## Geospatial Crash Heatmap")
nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)
heat_data = df[['LATITUDE', 'LONGITUDE']].values.tolist()
HeatMap(heat_data).add_to(nyc_map)
st.components.v1.html(nyc_map._repr_html_(), height=500)

# Contributing Factors Bar Plot
st.write("## Top Contributing Factors to Collisions")
factors = pd.concat([df['CONTRIBUTING FACTOR VEHICLE 1'],
                     df['CONTRIBUTING FACTOR VEHICLE 2'],
                     df['CONTRIBUTING FACTOR VEHICLE 3'],
                     df['CONTRIBUTING FACTOR VEHICLE 4'],
                     df['CONTRIBUTING FACTOR VEHICLE 5']])
factor_counts = factors.value_counts().drop('Unspecified', errors='ignore').head(20)
plt.figure(figsize=(10, 6))
sns.barplot(y=factor_counts.index, x=factor_counts.values, palette='viridis')
plt.title('Top Contributing Factors to Collisions')
plt.xlabel('Number of Occurrences')
plt.ylabel('Contributing Factor')
st.pyplot(plt)

# Injuries by Category of User-Groups
st.write("## Injuries by User-Groups")
injuries = df[['NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF CYCLIST INJURED', 'NUMBER OF MOTORIST INJURED']].sum()
injury_data = pd.DataFrame({
    'Category': ['Pedestrians', 'Cyclists', 'Motorists'],
    'Injuries': injuries.values
})
injury_chart = alt.Chart(injury_data.melt(id_vars='Category', var_name='Type', value_name='Count')).mark_bar().encode(
    x='Category:N', y='Count:Q', color='Type:N', tooltip=['Category', 'Type', 'Count']
)
st.altair_chart(injury_chart, use_container_width=True)

# Fatalities by Category of User-Groups
st.write("## Fatalities by User-Groups")
fatalities = df[['NUMBER OF PEDESTRIANS KILLED', 'NUMBER OF CYCLIST KILLED', 'NUMBER OF MOTORIST KILLED']].sum()
fatality_data = pd.DataFrame({
    'Category': ['Pedestrians', 'Cyclists', 'Motorists'],
    'Fatalities': fatalities.values
})
fatality_chart = alt.Chart(fatality_data.melt(id_vars='Category', var_name='Type', value_name='Count')).mark_bar().encode(
    x='Category:N', y='Count:Q', color='Type:N', tooltip=['Category', 'Type', 'Count']
)
st.altair_chart(fatality_chart, use_container_width=True)

# Vehicle Types Bar Plot
st.write("## Top Vehicle Types Involved in Collisions")
vehicles = pd.concat([df['VEHICLE TYPE CODE 1'], df['VEHICLE TYPE CODE 2']]).value_counts().head(10)
vehicle_chart = alt.Chart(pd.DataFrame({
    'Vehicle Type': vehicles.index,
    'Count': vehicles.values
})).mark_bar().encode(
    x='Count:Q',
    y=alt.Y('Vehicle Type:N', sort='-x'),
    tooltip=['Vehicle Type', 'Count']
).properties(title="Top Vehicle Types Involved in Collisions")
st.altair_chart(vehicle_chart, use_container_width=True)

# Collisions Over Time
st.write("## Daily Collisions Over Time")
df_timeseries = df.set_index('CRASH_DATETIME').resample('D').size().reset_index(name='Collisions')
timeseries_chart = alt.Chart(df_timeseries).mark_line().encode(
    x='CRASH_DATETIME:T', y='Collisions:Q', tooltip=['CRASH_DATETIME', 'Collisions']
).properties(title="Daily Collisions Over Time")
st.altair_chart(timeseries_chart, use_container_width=True)

# Temporal Heatmap
st.write("## Temporal Heatmap of Collisions")
df['Hour'] = df['CRASH_DATETIME'].dt.hour
df['DayOfWeek'] = df['CRASH_DATETIME'].dt.day_name()
heatmap_data = df.groupby(['Hour', 'DayOfWeek']).size().reset_index(name='Collisions')
heatmap_data['DayOfWeek'] = pd.Categorical(heatmap_data['DayOfWeek'], categories=[
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
heatmap_chart = alt.Chart(heatmap_data).mark_rect().encode(
    x=alt.X('DayOfWeek:N'), y=alt.Y('Hour:O'), color='Collisions:Q',
    tooltip=['DayOfWeek', 'Hour', 'Collisions']
).properties(title="Collisions Heatmap by Day and Hour")
st.altair_chart(heatmap_chart, use_container_width=True)

# Collisions by Borough
st.write("## Collisions by Borough")
borough_data = df.groupby('BOROUGH').agg({
    'CRASH DATE': 'count',
    'NUMBER OF PERSONS INJURED': 'sum',
    'NUMBER OF PERSONS KILLED': 'sum'
}).rename(columns={'CRASH DATE': 'Total Collisions'}).reset_index()
bubble_chart = alt.Chart(borough_data).mark_circle().encode(
    x='Total Collisions:Q', y='NUMBER OF PERSONS INJURED:Q', size='NUMBER OF PERSONS KILLED:Q',
    tooltip=['BOROUGH', 'Total Collisions', 'NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED']
).properties(title="Collisions by Borough")
st.altair_chart(bubble_chart, use_container_width=True)

# Additional Innovative Plot: Hourly Collision Trends by Borough
st.write("## Hourly Collision Trends by Borough")
hourly_data = df.groupby(['Hour', 'BOROUGH']).size().reset_index(name='Collisions')
hourly_chart = alt.Chart(hourly_data).mark_line().encode(
    x='Hour:Q', y='Collisions:Q', color='BOROUGH:N',
    tooltip=['Hour', 'BOROUGH', 'Collisions']
).properties(title="Hourly Collision Trends by Borough")
st.altair_chart(hourly_chart, use_container_width=True)

# Additional Innovative Plot: Average Severity by Day of the Week
st.write("## Average Severity by Day of the Week")
df['Severity'] = (df['NUMBER OF PERSONS INJURED'] + df['NUMBER OF PERSONS KILLED']).fillna(0)
avg_severity = df.groupby('DayOfWeek')['Severity'].mean().reset_index()
avg_severity['DayOfWeek'] = pd.Categorical(avg_severity['DayOfWeek'], categories=[
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
severity_chart = alt.Chart(avg_severity).mark_bar().encode(
    x='DayOfWeek:N', y='Severity:Q', tooltip=['DayOfWeek', 'Severity']
).properties(title="Average Severity by Day of the Week")
st.altair_chart(severity_chart, use_container_width=True)

# Adding crash markers to the map
st.write("## Crash Markers on NYC Map")

boroughs = df['BOROUGH'].dropna().unique().tolist()
selected_borough = st.sidebar.selectbox("Select Borough", ["All"] + boroughs)

if selected_borough != "All":
    data_filtered = df[df['BOROUGH'] == selected_borough]
else:
    data_filtered = df

data_sample = data_filtered.sample(n=1000)  # Sampling to avoid performance issues

nyc_map_markers = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

for _, row in data_sample.iterrows():
    crash_info = f"""
    <b>Date:</b> {row['CRASH DATE']}<br>
    <b>Time:</b> {row['CRASH TIME']}<br>
    <b>Borough:</b> {row['BOROUGH']}<br>
    <b>Injuries:</b> {row['NUMBER OF PERSONS INJURED']}<br>
    <b>Fatalities:</b> {row['NUMBER OF PERSONS KILLED']}<br>
    <b>Contributing Factor:</b> {row['CONTRIBUTING FACTOR VEHICLE 1']}
    """
    icon_color = 'red' if row['NUMBER OF PERSONS KILLED'] > 0 else 'orange'
    folium.Marker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        popup=folium.Popup(crash_info, max_width=300),
        icon=folium.Icon(icon="car-crash", prefix="fa", color=icon_color)
    ).add_to(nyc_map_markers)

st.components.v1.html(nyc_map_markers._repr_html_(), height=500)

