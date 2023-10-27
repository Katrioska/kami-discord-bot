from discord.ext import commands
from discord.ext.commands.context import Context

class TestExtension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pinga(self, ctx: Context):
        await ctx.reply("Ping!")

async def setup(bot):
    await bot.add_cog(TestExtension(bot))