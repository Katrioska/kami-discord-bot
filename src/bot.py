import os

import discord
from discord.ext import commands
from discord.message import Message
from os import getenv
from dotenv import load_dotenv

from utils import JsonManager

intents = discord.Intents.all()
intents.typing = False
intents.presences = False
intents.members = True

bot = commands.Bot(command_prefix="k!", intents=intents)
bot.remove_command('help')

@bot.event
async def on_message(message: Message):
    if message.content.startswith(bot.command_prefix):
        if not message.content.split(" ")[0].replace(bot.command_prefix, "") in JsonManager.get(message.guild.id, "disabled_commands"):
            await bot.process_commands(message)

@bot.event
async def on_ready():
    for filename in os.listdir("extensions"):
        if filename.endswith(".py"):
            await bot.load_extension(f"extensions.{filename[:-3]}")

    for guild in bot.guilds:
        JsonManager.register_new_guild(guild.id)

if __name__ == "__main__":
    load_dotenv("../.env")
    bot.run(getenv("DISCORD_TOKEN"))