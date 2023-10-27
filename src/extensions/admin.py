from discord.ext import commands
from discord.ext.commands.context import Context
# noinspection PyUnresolvedReferences
from utils import JsonManager
# noinspection PyUnresolvedReferences
from utils.response_embed import *

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def disable_command(self, ctx: Context):
        command = ctx.message.content.split()[-1]
        if command in JsonManager.get(ctx.guild.id, "disabled_commands"):
            await ctx.reply(embed=allowEmbed("disable_command", f"El comando `{command}` ya esta desactivado."))
        else:
            JsonManager.change_value(ctx.guild.id, "disabled_commands", command)
            await  ctx.reply(embed=allowEmbed("disable_command", f"Se ha desactivado el comando `{command}`"))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def enable_command(self, ctx: Context):
        command = ctx.message.content.split()[-1]
        if command not in JsonManager.get(ctx.guild.id, "disabled_commands"):
            await ctx.reply(embed=allowEmbed("disable_command", f"El comando `{command}` ya esta activado."))
        else:
            JsonManager.restore_value(ctx.guild.id, "disabled_commands", ctx.message.content.split()[-1])
            await  ctx.reply(embed=allowEmbed("disable_command", f"Se ha activado el comando `{ctx.message.content.split()[-1]}`"))


async def setup(bot):
    await bot.add_cog(Admin(bot))