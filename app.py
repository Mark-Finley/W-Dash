import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# OpenWeatherMap API URL and your API Key
OPENWEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Retrieve the API key from environment variables
API_KEY = os.getenv('WEATHER_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    
    if not city:
        return jsonify({"error": "Please provide a city name"}), 400

    # Fetch current weather data
    weather_data = requests.get(f"{OPENWEATHER_API_URL}?q={city}&appid={API_KEY}&units=metric")
    if weather_data.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    weather_data = weather_data.json()

    # Fetch 5-day forecast data
    forecast_data = requests.get(f"{OPENWEATHER_FORECAST_URL}?q={city}&appid={API_KEY}&units=metric")
    forecast_data = forecast_data.json()

    # Structure the weather data for easier use
    data = {
        "city": weather_data.get("name"),
        "temperature": weather_data.get("main", {}).get("temp"),
        "humidity": weather_data.get("main", {}).get("humidity"),
        "wind_speed": weather_data.get("wind", {}).get("speed"),
        "description": weather_data.get("weather", [])[0].get("description"),
        "icon": weather_data.get("weather", [])[0].get("icon"),
        "forecast": forecast_data.get("list", [])
    }

    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)
