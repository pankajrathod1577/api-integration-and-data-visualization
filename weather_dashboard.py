import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

# Set up API key and city
API_KEY = "ffa1b3c13f503ac9e8d97e9ea9138b33"
CITY = "Hyderabad"  # You can change this to any city
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Function to fetch weather data
def get_weather_data(city, api_key):
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # For Celsius
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Function to process weather data
def process_weather_data(data):
    if data and data.get('cod') != '404':
        weather_info = {
            'Temperature (°C)': data['main']['temp'],
            'Feels Like (°C)': data['main']['feels_like'],
            'Humidity (%)': data['main']['humidity'],
            'Pressure (hPa)': data['main']['pressure'],
            'Wind Speed (m/s)': data['wind']['speed'],
            'Cloud Cover (%)': data['clouds']['all'],
            'Timestamp': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S'),
            'Weather': data['weather'][0]['main']
        }
        return weather_info
    return None

# Function to create visualizations
def create_weather_dashboard(weather_data):
    if not weather_data:
        print("No data to visualize")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame([weather_data])
    
    sns.set_theme()  # This applies Seaborn's default styling
    
    fig = plt.figure(figsize=(15, 10))
    
    # 1. Temperature Comparison Bar Plot
    plt.subplot(2, 2, 1)
    temps = df[['Temperature (°C)', 'Feels Like (°C)']].melt()
    sns.barplot(x='variable', y='value', data=temps, palette='coolwarm')
    plt.title('Temperature vs Feels Like')
    plt.ylabel('Temperature (°C)')
    
    # 2. Humidity and Cloud Cover
    plt.subplot(2, 2, 2)
    conditions = df[['Humidity (%)', 'Cloud Cover (%)']].melt()
    sns.barplot(x='variable', y='value', data=conditions, palette='Blues')
    plt.title('Atmospheric Conditions')
    plt.ylabel('Percentage (%)')
    
    # 3. Wind Speed Gauge-like plot
    plt.subplot(2, 2, 3)
    sns.barplot(x=['Wind Speed'], y=[weather_data['Wind Speed (m/s)']], palette='Greens')
    plt.title('Wind Speed')
    plt.ylabel('Speed (m/s)')
    
    # 4. Weather Condition Text
    plt.subplot(2, 2, 4)
    plt.axis('off')
    weather_text = f"Current Weather: {weather_data['Weather']}\n"
    weather_text += f"Time: {weather_data['Timestamp']}"
    plt.text(0.5, 0.5, weather_text, ha='center', va='center', 
             bbox=dict(facecolor='lightblue', alpha=0.5))
    
    # Adjust layout and add main title
    plt.tight_layout()
    fig.suptitle(f'Weather Dashboard for {CITY}', fontsize=16, y=1.05)
    
    # Save and show
    plt.savefig('weather_dashboard.png', dpi=300, bbox_inches='tight')
    plt.show()

# Main execution
def main():
    raw_data = get_weather_data(CITY, API_KEY)
    
    if raw_data:
        weather_data = process_weather_data(raw_data)
        
        if weather_data:
            create_weather_dashboard(weather_data)
            print("Weather dashboard created successfully!")
        else:
            print("Failed to process weather data")
    else:
        print("Failed to fetch weather data")

if __name__ == "__main__":
    main()