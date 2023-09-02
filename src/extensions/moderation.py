from discord.ext import commands
from discord.ext.commands.context import Context

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Moderation(bot))