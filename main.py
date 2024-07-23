import discord

with open('config.json') as f:
    vars = json.load(f)
    print(vars)


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

bot.run(vars["token"])