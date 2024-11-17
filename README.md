# Short.io Link Shortener Bot with WebApp Integration

This project is a Python-based Telegram bot and web application that uses Short.io's API to generate short links. The bot and web app allow users to input an original URL and a custom path, returning a shortened URL.

## Features

- **Telegram Bot Integration**: Users can send the original URL and desired path directly to the bot to receive a shortened URL.
- **Web Application**: A web interface for entering the original URL and path to get a shortened URL.
- **Custom Short Links**: Supports custom paths for better link readability.
- **Integration with Short.io API**: Uses Short.io for robust and secure link shortening.

## Demo

Try the Telegram bot here: [Shortgy Bot](https://t.me/shortgy_bot)

## Prerequisites

- Python 3.9 or above
- A valid Short.io API key with permissions to create links
- Dependencies listed in `requirements.txt`

## Installation

1. **Clone the Repository**
   ```
   git clone https://github.com/yourusername/shortgy_bot.git
   cd shortgy_bot
2. **Install Dependencies Install the required Python packages:**

    ```
    Copy code
    pip install -r requirements.txt
3. **Set Up Environment Variables Create a ```.env``` file in the project directory and add the following:**

    ```
    BOT_TOKEN=your_telegram_bot_token
    SHORT_IO_API_KEY=your_shortio_api_key
4. **Run the Project**

    ```
    python main.py

## Usage
### Telegram Bot
1. Start the bot by clicking the link: Shortgy Bot.
2. Send the original URL.
3. Provide the desired custom path.
4. Receive the shortened URL.
### Web Application
1. Visit http://127.0.0.1:5000 (or the deployed URL if hosted).
2. Enter the original URL and desired path.
3. Click Shorten to get the shortened URL.

## Project Structure
    
    shortio-bot/
    │
    ├── main.py                  # Main script integrating bot and web app
    ├── templates/
    │   └── index.html           # Web app's HTML template
    ├── requirements.txt         # Python dependencies

## Dependencies
[Telethon](https://github.com/LonamiWebs/Telethon) - For Telegram bot functionality
Flask - For web application
Requests - For API integration
