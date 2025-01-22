---

# YouTube Playlist Length Calculator - Telegram Bot

This Telegram bot, built with Python, calculates the total duration and average length of videos in YouTube playlists. Share a playlist link with the bot, and it will return the total duration (in hours and minutes) and the average duration per video.

---

## Features
- **Total Video Duration**: Calculates the total duration of all videos in a playlist.  
- **Average Video Duration**: Computes the average duration per video in the playlist.  
- **Flexible URL Parsing**: Handles various YouTube playlist URL formats, including URLs with additional parameters.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/https-guru/yt-playlist-calc
cd yt-playlist-length-calculator
```

### 2. Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project directory and add your **Telegram Bot Token** and **YouTube API Key**:
```plaintext
TELEGRAM_TOKEN=your_telegram_bot_token
YOUTUBE_API_KEY=your_youtube_api_key
```

---

## Usage

### Running the Bot Locally
Start the bot with the following command:
```bash
python bot.py
```

### Interacting with the Bot
1. Use the `/start` command to get a welcome message.  
2. Send a YouTube playlist link as a message.  
3. The bot will reply with:
   - The **total duration** of the playlist.  
   - The **average video duration**.  
   - The **total number of videos**.

---

## Deployment

You can deploy the bot to a cloud service like [Render](https://render.com).  

### Deployment Steps
1. Create a **new web service** on Render.  
2. Use this repository as the source.  
3. Configure the environment variables (`TELEGRAM_TOKEN` and `YOUTUBE_API_KEY`) in the Render dashboard.  
4. Set the **start command** to:
   ```bash
   ./start.sh
   ```

---

## Project Structure
```plaintext
.
├── bot.py                # Main bot script
├── requirements.txt      # Dependencies
├── start.sh              # Start script for deployment
├── .env                  # Environment variables (not included in the repository)
├── README.md             # Documentation (this file)
```

---

## Requirements

The bot requires the following Python libraries:
- `python-telegram-bot==20.3`  
- `google-api-python-client`  
- `requests`  
- `python-dotenv`  

Ensure these dependencies are installed before running the bot.

---
