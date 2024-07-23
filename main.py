import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import json
import requests
from os import path, makedirs
import asyncio
from pathlib import Path

with open('config.json') as f:
    vars = json.load(f)
    print(vars)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=".", intents=intents)

# Other functions

def savemp3(file, path):
    with open(path, 'wb') as fd:
        fd.write(file.content)

def doesitexist(filepath, type):
    if type == 0:
        if Path(filepath).is_file(): return True
        else: return False
    elif type == 1:
        if Path(filepath).is_dir(): return True
        else: return False

def mkdir(filepath):
    if not path.isdir(Path(filepath)):
        makedirs(Path(filepath))


# Other functions
@bot.command(brief='Stores attached audio for later use in soundboard',
            description='Stores attached audio for later use in soundboard \n Can be played in current vc with the .play [soundname] command')
async def addsound(ctx, name=""):
    print(ctx)
    print(ctx.message.attachments)
    if len(ctx.message.attachments) < 1:
        await ctx.send("No files supplied")
    else:
        await ctx.send("Processing files")
        file = requests.get(ctx.message.attachments[0])
        if not doesitexist(path.join("resources", str(ctx.author)), 1):
            mkdir(path.join("resources", str(ctx.author)))
        down_path = path.join("resources", str(ctx.author), name)
        try:
            savemp3(file, down_path)
        except:
            await ctx.send("Unexpected error occurred while saving file")


@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='stop', brief="Stops the bot and kicks it from the vc",
             description="Stops the bot and kicks it from the vc")
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play', help='Plays sound')
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
    filepath = path.join("resources", str(ctx.author), file)
    if doesitexist(filepath, 0):
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filepath))
    else:
        await ctx.send("sound does not exist")


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

bot.run(vars["TOKEN"])