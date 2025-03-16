import logging
from typing import Dict, Any, Optional, Union, Final
from aiogram import types, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.services.air_quality import get_nearest_station_data, AirQualityData
from app.utils.formatting import format_air_quality_message

# Define states
class AirQualityStates(StatesGroup):
    waiting_for_location: State = State()

# Start command handler
async def cmd_start(message: Message, state: FSMContext) -> None:
    """
    Handler for the /start command
    
    Args:
        message: Incoming message object
        state: FSM context for state management
    """
    await message.answer(
        "Welcome to the Air Quality Bot! 🌬️\n\n"
        "I can provide you with air quality information for your location.\n"
        "Please share your location to get started.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Share Location and get Air Quality Data 📍", request_location=True)]
            ],
            resize_keyboard=True
        )
    )
    await state.set_state(AirQualityStates.waiting_for_location)

# Help command handler
async def cmd_help(message: Message) -> None:
    """
    Handler for the /help command
    
    Args:
        message: Incoming message object
    """
    help_text: Final[str] = (
        "🤖 <b>Air Quality Bot Help</b>\n\n"
        "This bot provides real-time air quality information based on your location.\n\n"
        "<b>Commands:</b>\n"
        "/start - Start the bot and share your location\n"
        "/refresh - Get updated air quality data for your last shared location\n"
        "/help - Show this help message\n\n"
        "<b>How to use:</b>\n"
        "1. Send /start command\n"
        "2. Share your location using the button\n"
        "3. Receive air quality information\n"
        "4. Use the /refresh command to get updated data\n\n"
        "<b>Air Quality Index (AQI) Scale:</b>\n"
        "✅ 0-50: Good\n"
        "✳️ 51-100: Moderate\n"
        "⚠️ 101-150: Unhealthy for Sensitive Groups\n"
        "❗ 151-200: Unhealthy\n"
        "❌ 201-300: Very Unhealthy\n"
        "☣️ 301+: Hazardous"
    )
    
    await message.answer(help_text, parse_mode="HTML")

# Refresh command handler
async def cmd_refresh(message: Message, state: FSMContext) -> None:
    """
    Handler for the /refresh command to get updated air quality data
    
    Args:
        message: Incoming message object
        state: FSM context for state management
    """
    # Get the last location from state
    user_data: Dict[str, Any] = await state.get_data()
    lat: Optional[float] = user_data.get("last_latitude")
    lon: Optional[float] = user_data.get("last_longitude")
    
    if lat and lon:
        processing_message = await message.answer("Refreshing air quality data... Please wait.")
        
        # Get updated air quality data
        air_quality_data: Optional[AirQualityData] = await get_nearest_station_data(lat, lon)
        
        if air_quality_data:
            logging.info("Air quality data refreshed successfully")
            await processing_message.edit_text(
                format_air_quality_message(air_quality_data), 
                parse_mode="HTML",
            )
        else:
            logging.error("Failed to refresh air quality data")
            await processing_message.edit_text(
                "Sorry, I couldn't refresh the air quality data. Please try again later.",
            )
    else:
        await message.answer(
            "I don't have your location saved. Please share your location first.",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="Share Location 📍", request_location=True)]
                ],
                resize_keyboard=True
            )
        ) 