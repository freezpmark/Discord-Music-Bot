# music-discord-bot

<img src="https://github.com/freezpmark/music-discord-bot/blob/961c5fbe201b0583c3e7f1613efda06fa3ac8274/screenshot.png" height="400"/>

Discord Music bot supported with Slash Commands and Requests tracking. It has clean interface and is easy to run!  
Also includes the main template function that I use in my personal bot.

## 🧑‍💻 Usage:
 - install Python
 - `git clone https://github.com/freezpmark/music-discord-bot`
 - `cd music-discord-bot`
 - `pip install -r requirements.txt`
 - create credentials for your Google Sheets credentials in json (tutorial for getting in [here](https://lcalcagni.medium.com/how-to-manipulate-google-spreadsheets-using-python-b15657e6ed0d))
 - create `.env` file in the root directory and set these variables:
```env
GUILD_ID=133713371337133713              # Your server ID
glados_TOKEN=ABCDEFGHIJKLMNOPRS          # Your bot token
glados_ID=123456789012345678             # Your bot client ID
GOOGLE_CREDENTIALS={"type": "...", ...}  # Your Google Sheets credendials in json
```
 - `python main.py`

There are also some optional variable settings you can set in `config.json`:
```json
{
    "timezone": "Europe/Vienna",
    "bots_settings": {
        "glados": {
            "activity": "/play",
            "cog_blacklist": [],
            "prefix": "?"
        },
    }
}
```

## 🔥 Features:
 - enables searching and playing tracks from YouTube
 - supports playing playlist or picking tracks from it
 - real-time audio player that is being updated before every track
 - button interactivity with the audio player
 - track request tracking system integrated with google sheets
 - track request summarization over certain periods of time

## 📚 Commands
<details><summary>Click to View Commands</summary>

| Name        | Description                               | Options                                                   |
|-------------|-------------------------------------------|-----------------------------------------------------------|
| ⏸️         | Pauses the current song                    |                                                           |
| ▶️         | Resumes the current song                   |                                                           |
| ⏭️         | Skips the current song                     |                                                           |
| 🔁         | Loops the queue                            |                                                           |
| 🔂         | Loops currently playing track              |                                                           |
| 🔀         | Shuffles the queue of songs that weren't yet played          |                                         |
| `play`     | Searches and plays/adds the track into queue                  | `search`: search prompt / URL          |
| `playlist` | Allows you to pick tracks from 25 last songs in the playlist  | `playlist_url`: url of playlist        |
| `search`   | Gives you list of tracks to choose from the search prompt     | `search`: search prompt                |
| `seek`     | Gets into certain timestamp in currently playing track        | `second`: timestamp in seconds         |
| `jump`     | Skips to a specific song in the queue       | `index`: index number in the queue                       |
| `remove`   | Removes a song from the queue               | `index`: index number in the queue                       |
| `volume`   | Changes the volume (10% is default)         | `volume`: from 1 to 100 (in %)                           |
| `clear`    | Clears the queue                            | `song`: The song number                                  |
| `history`  | Saves all requests into google sheets log   | (use prefix) `limit`: amount of msgs to take into account|
| `create_stats` | Creates stats out from the requests log | (use prefix)                                             |
</details>

## 👀 Example
(There will be a gif file added soon that will showcase the usage)  

The app has not yet been fully tested and there are still a few TODOs to do in the code.
