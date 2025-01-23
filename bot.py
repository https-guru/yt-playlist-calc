import re
import os
from dotenv import load_dotenv
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables from the .env file
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Function to fetch playlist data
async def get_playlist_duration(playlist_url: str):
    try:
        # Extract playlist ID from the URL
        if "list=" not in playlist_url:
            return "Invalid playlist URL. Please provide a valid YouTube playlist link."
        playlist_id = playlist_url.split("list=")[1]

        # YouTube API endpoint
        url = f"https://www.googleapis.com/youtube/v3/playlistItems"
        params = {
            "part": "contentDetails",
            "maxResults": 50,  # Maximum results allowed per API call
            "playlistId": playlist_id,
            "key": YOUTUBE_API_KEY,
        }

        # Fetch all videos in the playlist
        total_duration_seconds = 0
        video_count = 0

        while True:
            response = requests.get(url, params=params).json()
            items = response.get("items", [])
            for item in items:
                video_id = item["contentDetails"]["videoId"]
                video_duration = get_video_duration(video_id)
                total_duration_seconds += video_duration
                video_count += 1

            # Check if there's a next page of results
            if "nextPageToken" in response:
                params["pageToken"] = response["nextPageToken"]
            else:
                break

        # Convert total duration to hours and minutes
        total_minutes, seconds = divmod(total_duration_seconds, 60)
        hours, minutes = divmod(total_minutes, 60)
        average_duration = total_duration_seconds // video_count if video_count else 0
        avg_minutes, avg_seconds = divmod(average_duration, 60)

        return (
            f"Playlist Duration:\n"
            f"- Total: {hours} hours, {minutes} minutes\n"
            f"- Videos: {video_count}\n"
            f"- Average per Video: {avg_minutes} minutes, {avg_seconds} seconds"
        )
    except Exception as e:
        logger.error(f"Error fetching playlist data: {e}")
        return "An error occurred while processing the playlist."

# Function to fetch video duration
def get_video_duration(video_id: str):
    url = f"https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "contentDetails",
        "id": video_id,
        "key": YOUTUBE_API_KEY,
    }
    response = requests.get(url, params=params).json()
    if "items" in response and response["items"]:
        duration = response["items"][0]["contentDetails"]["duration"]
        return parse_duration(duration)
    return 0

# Parse ISO 8601 duration (e.g., PT1H2M30S) into seconds
def parse_duration(duration: str):
    import isodate
    parsed_duration = isodate.parse_duration(duration)
    return int(parsed_duration.total_seconds())



# Command handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me a YouTube playlist link, and I'll calculate the total and average durations.")
# Updated function to process the message and extract the playlist URL
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    # Extract the playlist URL using regex
    playlist_url = extract_playlist_url(message)
    if not playlist_url:
        await update.message.reply_text(
            "I couldn't find a valid YouTube playlist link in your message. Please send a proper link!"
        )
        return

    # Process the playlist and send the result
    result = await get_playlist_duration(playlist_url)
    await update.message.reply_text(result)
    
    
def extract_playlist_url(text: str) -> str:
    # Regex pattern to match a YouTube playlist URL
    pattern = r"(https?://(?:www\.)?youtube\.com/playlist\?list=[\w-]+)"
    match = re.search(pattern, text)
    if match:
        # Return only the clean URL without extra parameters
        base_url = match.group(1)
        return base_url
    return None


# Main function to start the bot
def main():
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    logger.info("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
