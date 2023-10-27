import hashlib
import json
import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.message import Message

# noinspection PyUnresolvedReferences
from utils import JsonManager
# noinspection PyUnresolvedReferences
from utils.response_embed import *

import requests
import io
import base64


URL = "http://127.0.0.1:7860"

class SD_Image_Generation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.preset_config = {
            "model" : None,
            "prompt": None,
            "negative_prompt": "",
            "sampler_index": "DDIM",
            "width": 512,
            "height": 512,
            "steps": 30,
            "enable_hr": False,
            "hr_upscaler": "Latent",
            "hr_scale": 2,
            "hr_sampler_name": "Euler",
            "hr_second_pass_steps": 10,
            "denoising_strength": 0.55
        }

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def create_sd_channel(self, ctx: Context):
        await ctx.message.guild.create_text_channel("image-generation", nsfw=True)
        channel = discord.utils.get(ctx.guild.channels, name="image-generation").id
        JsonManager.change_value(ctx.guild.id, "image_generation_channel", channel)
        await ctx.reply(embed=allowEmbed("Create-SD-Channel", "El canal `image-generation` ha sido creado."))

    @commands.command()
    async def models(self, ctx: Context):
        if not ctx.channel.id == JsonManager.get(ctx.guild.id, "image_generation_channel"):
            await ctx.message.delete()
            return

        model_list = ""
        response = requests.get(url=f"{URL}/sdapi/v1/sd-models")
        for model in response.json():
            model_list += f"`{model['model_name']}` \n"
        await ctx.reply(embed=allowEmbed("Lista de Modelos de Stable Diffusion", model_list))

    @commands.command()
    async def loras(self, ctx: Context):
        if not ctx.channel.id == JsonManager.get(ctx.guild.id, "image_generation_channel"):
            await ctx.message.delete()
            return

        loras = ""
        response = requests.get(url=f"{URL}/sdapi/v1/loras").json()
        for lora in response:
            print(lora.keys())
            loras += f"<lora:{lora['name']}:1.0>\n"

        await ctx.reply(embed = allowEmbed("Lista de LORAs:", loras))

    @commands.command()
    async def presets(self, ctx: Context):
        presets = JsonManager.get(ctx.guild.id, "sd_presets")
        sdcommand = ""
        for command in presets.keys():
            sdcommand += f"`{command}` Modelo: {presets[command]['model']} Descripcion: {presets[command]['description']}\n\n"

        await ctx.reply(embed=allowEmbed("Lista de Comandos para Generar Imagenes", sdcommand))

    @commands.Cog.listener("on_message")
    async def sd_preset(self, msg: Message):
        presets = JsonManager.get(msg.guild.id, "sd_presets")

        if not msg.content.startswith("k!"):
            return

        to_use_preset = None
        for preset in presets.keys():
            if preset in msg.content:
                to_use_preset = presets[preset]
                break

        if to_use_preset == None:
            return

        size_x = 512
        size_y = 512
        print(msg.content.split("--"))

        if "--" in msg.content:
            args = msg.content.split("--")
            prompt = args[0].replace(f"k!{preset}", "")
            args.pop(0)

            for arg in args:
                arg = arg.split()

                ### SIZE
                if arg[0] == "s":
                    if 400 <= int(arg[1]) <= 1536:
                        size_x = int(arg[1])

                    if 400 <= int(arg[1]) <= 1536:
                        size_y = int(arg[2])

                ### Negative Prompt
                if arg[0] == "n":
                    arg.pop(0)
                    to_use_preset["negative_prompt"] = "".join(i + " " for i in arg)

                ### CFG
                if arg[0] == "cfg":
                    to_use_preset["cfg_scale"] = int(arg[1])

                ### SEED
                if arg[0] == "seed":
                    to_use_preset["seed"] = int(arg[1])
        else:
            prompt = msg.content.replace(f"k!{preset}", "")

        requests.post(f"{URL}/sdapi/v1/options", json={"sd_model_checkpoint": to_use_preset["model"]})
        to_use_preset["prompt"] = prompt
        to_use_preset["width"] = size_x
        to_use_preset["height"] = size_y
        response = requests.post(url=f'{URL}/sdapi/v1/txt2img', json=to_use_preset).json()
        print()
        await msg.reply(f"Prompt: {json.loads(response['info'])['infotexts'][0]}",
                        file=discord.File(filename=f"{hashlib.sha1(response['images'][0].encode()).hexdigest()}.png",
                        fp=io.BytesIO(base64.b64decode(response['images'][0]))))

async def setup(bot):
    await bot.add_cog(SD_Image_Generation(bot))