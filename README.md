# Air Quality Telegram Bot

A Telegram bot that provides air quality information based on user location using the IQAir API.

## Features

- Asks users for their location
- Finds the closest air quality monitoring station using IQAir's `/nearest_station` endpoint
- Retrieves accurate pollution data from the nearest monitoring station
- Falls back to city-level data if station data is unavailable
- Sends formatted air quality reports to users

## Requirements

- Python 3.7+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- IQAir API Key (from [IQAir](https://www.iqair.com/air-pollution-data-api))

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/air_quality_bot.git
   cd air_quality_bot
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
   
   If you encounter any import errors, make sure all dependencies are installed correctly:
   ```
   pip install aiogram==3.2.0 python-dotenv==1.0.0 aiohttp~=3.9.0 geopy==2.3.0
   ```

3. Create a `.env` file in the project root and add your API keys:
   ```
   BOT_TOKEN=your_telegram_bot_token
   IQAIR_API_KEY=your_iqair_api_key
   ```

## Usage

1. Run the bot:
   ```
   python main.py
   ```

2. Open Telegram and start a chat with your bot.

3. Use the `/start` command to begin and share your location when prompted.

4. The bot will send you air quality information for your location.

## Air Quality Index (AQI) Scale

- 0-50: Good (✅)
- 51-100: Moderate (✳️)
- 101-150: Unhealthy for Sensitive Groups (⚠️)
- 151-200: Unhealthy (❗)
- 201-300: Very Unhealthy (❌)
- 301+: Hazardous (☣️)

## Commands

- `/start` - Start the bot and share your location
- `/help` - Show help information

## License

MIT 