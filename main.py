import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import json
import requests
from os import path
import asyncio

with open('config.json') as f:
    vars = json.load(f)
    print(vars)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents)

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
        down_path = path.join("resources", "download.mp3")
        with open(down_path, 'wb') as fd:
                fd.write(file.content)

@bot.command(pass_context=True)
async def join(ctx):
    author = ctx.message.author
    channel = author.voice_channel
    await bot.join_voice_channel(channel)

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

bot.run(vars["TOKEN"])