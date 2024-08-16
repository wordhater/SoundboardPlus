# SoundboardPlus

Allows a user to upload extra files for use in voice calls similar to discord's soundboard in voice calls.

## Important

**DO NOT USE ON LARGER DISCORD SERVERS WITH PEOPLE WHO YOU DONT KNOW OR TRUST. THERE IS PROBABLY SOME WAY USERS CAN MODIFY OTHER FILES ON THE HOST COMPUTER**


## Setup

Windows: Download the ffmpeg binary and place in folder with main.py
Linux: Ensure ffmpeg is installed with you package manager

Create a file named *config.json* and fill out with the content below

## config.json

```json
{
    "TOKEN": "you bot token here",
    "FFMPEG_PATH": "enter the path to the ffmpeg binary (on linux if ffmpeg is installed from your package manager just enter ffmpeg)(windows: ffmpeg.exe or whatever it's called)"
}
```

Finally execute run.sh (if permission error ```chmod +x run.sh```)

I might make a batch script for windows at some point, for now just look at what the run.sh file does and do it manually.

## To Do

- Warn users if the bot is already playing sounds
- join vc that message author is not in

