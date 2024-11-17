from telethon import TelegramClient, events
import requests
import json
from flask import Flask, request, jsonify, render_template
import threading

API_ID = "API_ID"         # Get this from https://my.telegram.org
API_HASH = "API_HASH"     # Get this from https://my.telegram.org
BOT_TOKEN = "BOT_TOKEN"   # Obtain from @BotFather
AUTHORIZATION_HEADER = "sk_wbYbmArZdbN3q1LB" 


SHORT_URL_ENDPOINT = "https://api.short.io/links"

client = TelegramClient('shorty_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

app = Flask(__name__)

user_states = {}


@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    """Handler for the /start command."""
    await event.respond(
        "Hello! Send the `originalURL` first, then send the `path`."
    )

@client.on(events.NewMessage)
async def handle_message(event):
    """Handles messages from users."""
    user_id = event.sender_id
    message = event.text.strip()

    if user_id not in user_states:
        if message.startswith("http://") or message.startswith("https://"):
            user_states[user_id] = {"originalURL": message}
            await event.respond("Got the original URL. Now send the path!")
        else:
            await event.respond("Please send a valid URL.")
        return

    if user_id in user_states and "originalURL" in user_states[user_id]:
        user_states[user_id]["path"] = message
        await process_short_url(event, user_id)

async def process_short_url(event, user_id):
    """Process the short URL creation."""
    headers = {
        "accept": "application/json",
        "authorization": AUTHORIZATION_HEADER, #or replace with yours
        "content-type": "application/json",
    }
    data = {
        "originalURL": user_states[user_id]["originalURL"],
        "path": user_states[user_id]["path"], 
        "domain": "h04d.short.gy", 
        "allowDuplicates": True
    }


    try:
        response = requests.post(SHORT_URL_ENDPOINT, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        short_url = response.json().get("shortURL", "No short URL found in response")

        # Reply with the short URL and clear state
        await event.respond(f"Short URL: {short_url}")
        del user_states[user_id]

    except requests.exceptions.RequestException as e:
        await event.respond(f"Error occurred: {str(e)}")
        del user_states[user_id]


@app.route("/")
def home():
    """Render the home page."""
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten():
    """Handle URL shortening from the web app."""
    original_url = request.form.get("originalURL")
    path = request.form.get("path")

    if not original_url or not path:
        return jsonify({"error": "Both 'originalURL' and 'path' are required"}), 400

    data = {
        "originalURL": original_url,
        "path": path,
        "domain": "h04d.short.gy",
        "source": "website",
        "allowDuplicates": True,
    }
    headers = {
        "accept": "/",
        "authorization": AUTHORIZATION_HEADER,
        "content-type": "application/json",
    }

    try:
        response = requests.post(SHORT_URL_ENDPOINT, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        short_url = response.json().get("shortURL", "No short URL found in response")
        return jsonify({"shortURL": short_url})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500



def run_flask():
    """Run the Flask app."""
    app.run(host="0.0.0.0", port=5000)

def run_telegram():
    """Run the Telegram bot."""
    print("Bot is running...")
    client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_telegram()
