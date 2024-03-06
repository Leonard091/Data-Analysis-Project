import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Bike Share Dashboard", layout="wide")


# Function load_data
@st.cache_data
def load_data(file_name):
    data = pd.read_csv(file_name)
    return data


# Data load
day_data = load_data("./day.csv")
hour_data = load_data("./hour.csv")


# Header
st.title("Bike Share Dashboard")

# Sidebar
st.sidebar.title("About")
st.sidebar.markdown("**• Nama: Leonardo Alfontus Mende Sirait**")
st.sidebar.markdown("**• Email: leonardosirait80@gmail.com**")
st.sidebar.markdown("**• Bangkit ID: M119D4KY3013**")
st.sidebar.markdown("**• Dicoding: [leonard80](https://www.dicoding.com/users/leonard80/)**")

# Show the datasets
st.sidebar.title("Bike Share Datasets")
if st.sidebar.checkbox("Show Dataset day.csv"):
    st.subheader("Raw Data")
    st.write(day_data)

if st.sidebar.checkbox("Show Dataset hour.csv"):
    st.subheader("Raw Data")
    st.write(hour_data)

# Display summary statistics
if st.sidebar.checkbox("Show Summary day.csv Statistics"):
    st.subheader("Summary Statistics")
    st.write(day_data.describe())

# Display summary statistics
if st.sidebar.checkbox("Show Summary hour.csv Statistics"):
    st.subheader("Summary Statistics")
    st.write(hour_data.describe())



# Main page
col1, col2 = st.columns([5, 1])

with col1:
    st.subheader("Daily Bike Rentals by Season and Weather Condition")

    # Mapping numbers to season names
    season_mapping = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
    day_data['season'] = day_data['season'].map(season_mapping)

    # Mapping numbers to weather conditions
    weather_mapping = {1: 'Clear', 2: 'Mist + Cloudy', 3: 'Light Snow', 4: 'Heavy Rain'}
    day_data['weathersit'] = day_data['weathersit'].map(weather_mapping)

    # Grouping data by season and weather situation
    season_weather_count = day_data.groupby(['season', 'weathersit'])['cnt'].mean().reset_index()

    # Create the bar chart
    fig_season_weather_count = px.bar(
        season_weather_count,
        x='season',
        y='cnt',
        color='weathersit',
        barmode='group',
        title='Daily Bike Rentals by Season and Weather Condition',
        labels={'cnt': 'Average Daily Rentals', 'season': 'Season', 'weathersit': 'Weather Condition'}
    )

    # Update layout for the chart
    fig_season_weather_count.update_layout(
        xaxis_title='Season',
        yaxis_title='Average Daily Rentals',
        legend_title='Weather Condition',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    # Show the plot
    st.plotly_chart(fig_season_weather_count)

with col2:
    # Displaying the analysis results
    st.subheader("Analysis Results")
    st.markdown("### Percentage Difference in Average Usage")
    percentage_diff = -3.54
    st.metric("Weekday vs Weekend", f"{percentage_diff}%")


st.markdown("""
#### Seasonal Impact
- **Winter:** Decreased usage due to cold and inclement weather.
- **Spring:** Significant increase as temperatures rise, indicating a preference for milder weather.
- **Summer:** Peak usage with the highest daily and hourly rentals, favored by warm and pleasant conditions.
- **Fall:** Slightly lower than summer, but still high, showing enjoyment of cooler, comfortable weather.

#### Weather Condition Impact
- **Clear Weather:** Highest rentals, showing a preference for predictable, comfortable conditions.
- **Mist + Cloudy:** Moderate reduction in usage, but not significantly discouraged.
- **Light Snow:** Notable drop in usage due to safety concerns and discomfort.
- **Heavy Rain (Hourly):** Drastic decrease, affecting commuting times and casual biking.

""")

for x in range(1, 5):
    st.markdown("<br>", unsafe_allow_html=True)

# Create columns for centering - left, center, right
left_col, center_col, right_col = st.columns([1, 5, 1])
with center_col:
    # Correlation matrix
    st.subheader("Correlation Matrix for Weather Conditions and Bike Usage")
    corr_matrix = day_data[['temp', 'hum', 'windspeed', 'cnt']].corr()
    fig_corr_matrix = px.imshow(corr_matrix, text_auto=True)
    st.plotly_chart(fig_corr_matrix)
    st.markdown("""
    #### Correlation Matrix Summary

    - **Temperature:** Shows a **strong positive relationship** with bike usage; higher temperatures increase rentals, more so for casual users.
    - **Humidity:** Exhibits a **weak negative correlation**; as humidity goes up, bike usage slightly drops, affecting casual users more.
    - **Wind Speed:** Has a **negligible negative impact** on bike usage; a slight decrease as wind speed rises, with casual users being more affected.
    """)

    for x in range(1,5):
        st.markdown("<br>", unsafe_allow_html=True)

    # Temperature vs. Total Daily Bike Usage
    st.subheader("Temperature vs. Total Daily Bike Usage")
    fig_temp_daily_usage = px.scatter(day_data, x='temp', y='cnt', trendline="ols")
    st.plotly_chart(fig_temp_daily_usage)

    # Humidity vs. Total Daily Bike Usage
    st.subheader("Humidity vs. Total Daily Bike Usage")
    fig_hum_daily_usage = px.scatter(day_data, x='hum', y='cnt', trendline="ols")
    st.plotly_chart(fig_hum_daily_usage)

    # Wind Speed vs. Total Daily Bike Usage
    st.subheader("Wind Speed vs. Total Daily Bike Usage")
    fig_wind_speed_daily_usage = px.scatter(day_data, x='windspeed', y='cnt', trendline="ols")
    st.plotly_chart(fig_wind_speed_daily_usage)

    st.markdown("""
    #### Weather Conditions vs. Bike Usage Summary

    - **Temperature:** Strong positive effect; warmer weather boosts rentals significantly.
    - **Humidity:** Minimal impact; slight decrease in rentals with higher humidity.
    - **Wind Speed:** Negligible influence; wind conditions do not notably deter bike usage.

    Overall, temperature is the key factor driving bike rentals, while humidity and wind speed have limited effects on user behavior.
    """)


