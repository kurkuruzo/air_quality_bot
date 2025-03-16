import logging
from typing import Optional
from aiogram.types import Message

# Debug handler - must be registered LAST to avoid blocking other handlers
async def debug_handler(message: Message) -> None:
    """
    Debug handler to log all messages that weren't caught by other handlers
    
    Args:
        message: Incoming message object
    """
    if message.location and hasattr(message.location, 'latitude') and hasattr(message.location, 'longitude'):
        logging.info(f"Debug: Unhandled location: {message.location.latitude}, {message.location.longitude}")
    else:
        logging.info(f"Debug: Unhandled message: {message.text if message.text else 'No text'}") 