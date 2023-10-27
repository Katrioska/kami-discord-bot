from discord import Embed
from discord.ext.commands.context import Context
import discord

async def errorEmbed(ctx: Context, message):
    embed = Embed(
        title="Error!",
        description=message,
        color=discord.Color.red()
    )
    await ctx.reply(embed=embed)

def denyEmbed(command, text="No tienes permisos para ejecutar este comando."):
    embed = discord.Embed(
        title=f"{command}",
        description=text,
        color=discord.Color.red()
    )
    return embed

def allowEmbed(command, text):
    embed = discord.Embed(
        title=f"{command}",
        description=text,
        color=discord.Color.green()
    )
    return embed