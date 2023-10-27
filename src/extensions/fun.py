from discord.ext import commands
from discord.ext.commands.context import Context
from os import getenv
from dotenv import load_dotenv
import openai

load_dotenv("../.env")
openai.api_key = getenv("OPENAI_TOKEN")

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def owofy(self, ctx: Context):
        """
        if ctx.message.reference:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            message = message.content

        else:
            message = ctx.message.content.replace("k!owofy", "")

        response = openai.Completion.create(
            model = "text-davinci-003",
            prompt = f"Converts the user input in UwU text, be cute and use emojis\nText:{message}\nOwofy:",
            max_tokens = 512,
        )

        await ctx.send(response["choices"][0]["text"])
        """
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(Fun(bot))