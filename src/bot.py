import os

import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
intents.members = True

bot = commands.Bot(command_prefix="k!", intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    for filename in os.listdir("extensions"):
        if filename.endswith(".py"):
            await bot.load_extension(f"extensions.{filename[:-3]}")

if __name__ == "__main__":
    load_dotenv("../.env")
    bot.run(getenv("DISCORD_TOKEN"))