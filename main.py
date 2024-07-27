import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import json
import requests
from os import path, remove
import asyncio
from pathlib import Path
import yt_dlp

with open('config.json') as f:
    vars = json.load(f)
    print(vars)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

# config for yt_dlp
yt_dlp_options = {
    'format':'bestaudio',
    'keepvideo':False,
    'outtmpl': "tmp/yt_audio",
}
# Other functions



def savemp3(file, path):
    with open(path, 'wb') as fd:
        fd.write(file.content)

path_exists = lambda x: Path(x).exists()

mkdir = lambda x: Path(x).mkdir(parents=True, exist_ok=True)

# Other functions

# Add and remove sounds
@bot.command(brief='Stores audio for later use in soundboard',
            description='Stores attached audio for later use in soundboard with .play \nUsage: .addsound [soundname] [url (only if from youtube)] \nNote that sound names cannot contain spaces',
            help="Stores audio for later use in soundboard.")
async def addsound(ctx, name=""):
    print(ctx)
    print(ctx.message.attachments)
    if len(ctx.message.attachments) < 1:
        await ctx.send("No files supplied")
    else:
        await ctx.send("Processing files")
        file = requests.get(ctx.message.attachments[0])
        if not path_exists(path.join("resources", str(ctx.author))):
            mkdir(path.join("resources", str(ctx.author)))
        down_path = path.join("resources", str(ctx.author), name)
        try:
            if not "./.." in down_path:
                savemp3(file, down_path)
            else:
                await ctx.send("Unexpected error occurred while saving file")
        except:
            await ctx.send("Unexpected error occurred while saving file")

@bot.command(brief='Removes existing sounds from your library',
            description='Removes existing sounds from your library',
            help="Removes existing sounds from your sounds. Usage: .removesound [name]")
async def removesound(ctx, name=""):
    filepath = path.join("resources", str(ctx.author), name)
    if not "./.." in filepath:
        remove(filepath)
    else:
        await ctx.send("Failed to remove file")

# manual join and leave
@bot.command(name='join', help='gets the bot to join the current vc')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='stop', brief="Stops the bot and kicks it from the vc",
             description="Stops the bot and kicks it from the vc")
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play', help='Plays sound.', description="Usage: .play [soundname] [channelname (if needed)]")
async def play(ctx, file="", custom_channel=""):
    try:
        if not ctx.message.author.voice:
            await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
            await channel.connect()
    except:
        print("failed to join vc or already in vc")
    server = ctx.message.guild
    voice_channel = server.voice_client
    # change to use regex for better reliability at some point
    if file.startswith("http"):
        await ctx.send("attempting to play youtube video")
        async with ctx.typing():
            remove("tmp/yt_audio")
            if yt_dlp.YoutubeDL(yt_dlp_options).download(file) != 0:
                await ctx.send("failed to download youtube video")
            else:
                voice_channel.play(discord.FFmpegPCMAudio(executable=vars['FFMPEG_PATH'], source="tmp/yt_audio"))
                await ctx.send("playing audio from youtube")
            
    else:
        filepath = path.join("resources", str(ctx.author), file)
        if path_exists(filepath):
            voice_channel.play(discord.FFmpegPCMAudio(executable=vars['FFMPEG_PATH'], source=filepath))
        else:
            await ctx.send("sound does not exist")
    while voice_channel.is_playing():
            await asyncio.sleep(1)
    if voice_channel.is_connected():
        await voice_channel.disconnect()


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

bot.run(vars["TOKEN"])