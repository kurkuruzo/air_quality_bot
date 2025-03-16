import logging
import aiohttp
from typing import Dict, Any, Optional, Union, TypedDict, cast

from app.config.config import IQAIR_API_KEY, IQAIR_API_URL

class AirQualityData(TypedDict, total=False):
    """Type definition for air quality data"""
    city: str
    state: str
    country: str
    location: Dict[str, float]
    current: Dict[str, Any]

async def get_nearest_station_data(lat: float, lon: float) -> Optional[AirQualityData]:
    """
    Get air quality data from the nearest station
    
    Args:
        lat: Latitude coordinate
        lon: Longitude coordinate
        
    Returns:
        Air quality data dictionary or None if not available
    """
    try:
        # Get data from the nearest station
        async with aiohttp.ClientSession() as session:
            params: Dict[str, Union[str, float]] = {
                "lat": lat,
                "lon": lon,
                "key": IQAIR_API_KEY
            }
            
            # Get nearest station data
            async with session.get(f"{IQAIR_API_URL}/nearest_station", params=params) as response:
                if response.status == 200:
                    data: Dict[str, Any] = await response.json()
                    if data.get("status") == "success":
                        return cast(AirQualityData, data.get("data"))
                    else:
                        logging.error(f"API error: {data.get('data')}")
                        
                        # Fallback to nearest city if station data is not available
                        return await get_nearest_city_data(lat, lon)
                else:
                    logging.error(f"API request failed with status {response.status}")
                    
                    # Fallback to nearest city if station request fails
                    return await get_nearest_city_data(lat, lon)
        
        return None
    except Exception as e:
        logging.error(f"Error getting station data: {e}")
        
        # Fallback to nearest city if an exception occurs
        return await get_nearest_city_data(lat, lon)

async def get_nearest_city_data(lat: float, lon: float) -> Optional[AirQualityData]:
    """
    Fallback function to get air quality data from the nearest city
    
    Args:
        lat: Latitude coordinate
        lon: Longitude coordinate
        
    Returns:
        Air quality data dictionary or None if not available
    """
    try:
        async with aiohttp.ClientSession() as session:
            params: Dict[str, Union[str, float]] = {
                "lat": lat,
                "lon": lon,
                "key": IQAIR_API_KEY
            }
            
            # Get nearest city data
            async with session.get(f"{IQAIR_API_URL}/nearest_city", params=params) as response:
                if response.status == 200:
                    data: Dict[str, Any] = await response.json()
                    if data.get("status") == "success":
                        return cast(AirQualityData, data.get("data"))
                    else:
                        logging.error(f"API error: {data.get('data')}")
                else:
                    logging.error(f"API request failed with status {response.status}")
        
        return None
    except Exception as e:
        logging.error(f"Error getting city data: {e}")
        return None 