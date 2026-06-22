#!/usr/bin/env python3
"""
Weather CLI
===========
Command-line weather tool using OpenWeatherMap API.

Features:
- Current weather
- Temperature in C/F
- Feels like, humidity, wind, description
- Interactive mode for Pydroid
- Easy API key setup

Author: RetroMatt2077
"""

import argparse
import requests
import json
from pathlib import Path


def get_weather(city: str, api_key: str, units: str = "metric"):
    """Fetch current weather from OpenWeatherMap."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city,
        "appid": api_key,
        "units": units
    }

    try:
        print(f"🌤️ Fetching weather for {city}...")
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 401:
            print("❌ Invalid API key. Please check your OpenWeatherMap API key.")
            return None
        elif response.status_code == 404:
            print("❌ City not found. Please check the spelling.")
            return None
        elif response.status_code != 200:
            print(f"❌ Error: {response.status_code}")
            return None

        data = response.json()
        
        # Extract data
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description'].capitalize()
        wind_speed = data['wind']['speed']
        city_name = data['name']
        country = data['sys']['country']

        unit_symbol = "°C" if units == "metric" else "°F"
        speed_unit = "m/s" if units == "metric" else "mph"

        print(f"\n📍 Weather in {city_name}, {country}")
        print(f"   🌡️  Temperature : {temp}{unit_symbol}")
        print(f"   🤔 Feels like  : {feels_like}{unit_symbol}")
        print(f"   ☁️  Condition   : {description}")
        print(f"   💧 Humidity    : {humidity}%")
        print(f"   🌬️  Wind        : {wind_speed} {speed_unit}")
        
        return data

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        print("💡 Check your internet connection.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    return None


def main():
    parser = argparse.ArgumentParser(description="🌤️ Weather CLI Tool")
    parser.add_argument("city", nargs="?", help="City name (e.g. London, New York)")
    parser.add_argument("-i", "--imperial", action="store_true", 
                        help="Use Fahrenheit and mph (default is Celsius)")
    parser.add_argument("-p", "--prompt", action="store_true",
                        help="Interactive mode (recommended for Pydroid)")
    parser.add_argument("-k", "--key", help="OpenWeatherMap API key (optional)")

    args = parser.parse_args()

    # Get API key
    api_key = args.key
    if not api_key:
        # Try to load from file
        key_file = Path("openweather_key.txt")
        if key_file.exists():
            api_key = key_file.read_text().strip()
        else:
            print("🔑 OpenWeatherMap API Key required.")
            print("   1. Go to https://openweathermap.org/api")
            print("   2. Sign up and get a free API key")
            print("   3. Run again with: python weather_cli.py \"City\" --key YOUR_KEY")
            print("   (Optional: Save key to openweather_key.txt for future use)")
            return

    if args.prompt or not args.city:
        city = input("🌍 Enter city name: ").strip()
        if not city:
            city = "Phoenix"  # Default
    else:
        city = args.city

    units = "imperial" if args.imperial else "metric"
    
    get_weather(city, api_key, units)


if __name__ == "__main__":
    main()
