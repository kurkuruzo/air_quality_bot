import logging
import asyncio
from typing import Tuple
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from app.config.config import BOT_TOKEN
from app.handlers.commands import cmd_start, cmd_help, cmd_refresh, AirQualityStates
from app.handlers.location import process_location, location_not_shared
from app.handlers.other import debug_handler

async def setup_bot() -> Tuple[Bot, Dispatcher]:
    """
    Set up the bot and register handlers
    
    Returns:
        Tuple containing the bot instance and dispatcher
    """
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Register command handlers
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_refresh, Command("refresh"))
    
    # Register location handlers
    dp.message.register(process_location, F.location)
    dp.message.register(location_not_shared, AirQualityStates.waiting_for_location)
    
    # Register debug handler (must be last)
    dp.message.register(debug_handler)
    
    return bot, dp

async def start_bot() -> Tuple[Bot, Dispatcher]:
    """
    Start the bot
    
    Returns:
        Tuple containing the bot instance and dispatcher
    """
    bot, dp = await setup_bot()
    
    # Start polling
    await dp.start_polling(bot)
    
    return bot, dp 