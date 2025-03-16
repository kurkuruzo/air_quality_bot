import asyncio
import logging

from app.bot import start_bot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

async def main() -> None:
    """
    Main function to start the bot
    """
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main()) 