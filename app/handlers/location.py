import logging
from typing import Optional
from aiogram import types, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from app.services.air_quality import get_nearest_station_data, AirQualityData
from app.utils.formatting import format_air_quality_message
from app.handlers.commands import AirQualityStates

# Location handler
async def process_location(message: Message, state: FSMContext) -> None:
    """
    Handler for receiving location
    
    Args:
        message: Incoming message object
        state: FSM context for state management
    """
    # Check if location is available
    if not message.location:
        await message.answer("Location data is missing. Please try sharing your location again.")
        return
    
    logging.info(f"Processing location: {message.location.latitude}, {message.location.longitude}")
    
    # Store location in state for refresh command
    await state.update_data(
        last_latitude=message.location.latitude,
        last_longitude=message.location.longitude
    )
    
    # Send a processing message
    processing_msg = await message.answer("Processing your location... Please wait.")
    
    lat: float = message.location.latitude
    lon: float = message.location.longitude
    
    # Get air quality data
    air_quality_data: Optional[AirQualityData] = await get_nearest_station_data(lat, lon)
    
    if air_quality_data:
        logging.info("Air quality data received successfully")
        # Send a new message with the results
        await processing_msg.edit_text(
            format_air_quality_message(air_quality_data), 
            parse_mode="HTML"
        )
    else:
        logging.error("Failed to get air quality data")
        # Send a new message with the error
        await message.answer(
            "Sorry, I couldn't find air quality data for your location. Please try again later."
        )
    
    await state.clear()

# Handle text messages when location is expected
async def location_not_shared(message: Message) -> None:
    """
    Handler for when user sends text instead of location
    
    Args:
        message: Incoming message object
    """
    await message.answer("Please share your location using the button below to get air quality information.") 