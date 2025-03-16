import logging
from typing import Dict, Any, Tuple, Optional, Union, cast

from app.services.air_quality import AirQualityData

def format_air_quality_message(data: AirQualityData) -> str:
    """
    Format air quality data into a readable message
    
    Args:
        data: Air quality data dictionary
        
    Returns:
        Formatted message string with HTML formatting
    """
    try:
        city = data.get("city", "Unknown")
        state = data.get("state", "Unknown")
        country = data.get("country", "Unknown")
        
        current = data.get("current", {})
        pollution = current.get("pollution", {})
        weather = current.get("weather", {})
        
        aqi = pollution.get("aqius", "N/A")
        main_pollutant = pollution.get("mainus", "N/A")
        
        temp = weather.get("tp", "N/A")
        humidity = weather.get("hu", "N/A")
        wind_speed = weather.get("ws", "N/A")
        
        # Determine AQI category and emoji
        aqi_category, emoji = get_aqi_category(aqi)
        
        message = (
            f"{emoji} <b>Air Quality Report</b> {emoji}\n\n"
            f"📍 <b>Location:</b> {city}, {state}, {country}\n\n"
            f"🔍 <b>Air Quality Index (US):</b> {aqi} - {aqi_category}\n"
            f"🦠 <b>Main Pollutant:</b> {get_pollutant_name(main_pollutant)}\n\n"
            f"🌡️ <b>Temperature:</b> {temp}°C\n"
            f"💧 <b>Humidity:</b> {humidity}%\n"
            f"💨 <b>Wind Speed:</b> {wind_speed} m/s\n\n"
            f"<i>Data provided by IQAir</i>"
        )
        
        return message
    except Exception as e:
        logging.error(f"Error formatting message: {e}")
        return "Sorry, there was an error formatting the air quality data."

def get_aqi_category(aqi: Union[int, str]) -> Tuple[str, str]:
    """
    Get AQI category and emoji based on AQI value
    
    Args:
        aqi: Air Quality Index value
        
    Returns:
        Tuple of (category_name, emoji)
    """
    try:
        aqi_value = int(aqi)
        
        if aqi_value <= 50:
            return "Good", "✅"
        elif aqi_value <= 100:
            return "Moderate", "✳️"
        elif aqi_value <= 150:
            return "Unhealthy for Sensitive Groups", "⚠️"
        elif aqi_value <= 200:
            return "Unhealthy", "❗"
        elif aqi_value <= 300:
            return "Very Unhealthy", "❌"
        else:
            return "Hazardous", "☣️"
    except:
        return "Unknown", "❓"

def get_pollutant_name(pollutant_code: str) -> str:
    """
    Convert pollutant code to full name
    
    Args:
        pollutant_code: Short code for the pollutant
        
    Returns:
        Full name of the pollutant
    """
    pollutants: Dict[str, str] = {
        "p1": "PM10",
        "p2": "PM2.5",
        "o3": "Ozone (O₃)",
        "n2": "Nitrogen Dioxide (NO₂)",
        "s2": "Sulfur Dioxide (SO₂)",
        "co": "Carbon Monoxide (CO)"
    }
    
    return pollutants.get(pollutant_code, pollutant_code) 