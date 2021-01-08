
import asyncio
import aiohttp
import json
import os
import random
import logging


import discord
from discord.ext import commands
from pathlib import Path
import motor.motor_asyncio

import utils.json_loader
from utils.mongo import Document


cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")


description = '''A clever discord bot written in python for the guild Uploading Nation'''

async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("gb$")(bot, message)

    try:
        data = await bot.config.find(message.guild.id)

        if not data or "prefix" not in data:
            return commands.when_mentioned_or("g$")(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or("g$")(bot, message)


secret_file = utils.json_loader.read_json('secrets')


bot = commands.Bot(
    command_prefix=get_prefix, 
    description=description,
    owner_id=219410026631135232,
    case_insensitive=True
)

bot.config_token = secret_file["token"]
logging.basicConfig(level=logging.INFO)
bot.blacklisted_users = []
bot.connection_url = secret_file["mongo"]
bot.muted_users = {}
bot.cwd = cwd

bot.version = "1.0"

bot.colors = {
    "WHITE": 0xFFFFFF,
    "AQUA": 0x1ABC9C,
    "GREEN": 0x2ECC71,
    "BLUE": 0x3498DB,
    "PURPLE": 0x9B59B6,
    "LUMINOUS_VIVID_PINK": 0xE91E63,
    "GOLD": 0xF1C40F,
    "ORANGE": 0xE67E22,
    "RED": 0xE74C3C,
    "NAVY": 0x34495E,
    "DARK_AQUA": 0x11806A,
    "DARK_GREEN": 0x1F8B4C,
    "DARK_BLUE": 0x206694,
    "DARK_PURPLE": 0x71368A,
    "DARK_VIVID_PINK": 0xAD1457,
    "DARK_GOLD": 0xC27C0E,
    "DARK_ORANGE": 0xA84300,
    "DARK_RED": 0x992D22
}
bot.color_list = [c for c in bot.colors.values()]

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)
    print("Bot ID:", bot.user.id)
    print('Bot latency:', bot.latency*1000, 2)
    print('Running discord.py version ' + discord.__version__)
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo["menudocs"]
    bot.config = Document(bot.db, "config")
    bot.mutes = Document(bot.db, "mutes")

    print("Initialized Database\n-----")
    for document in await bot.config.get_all():
        print(document)

    currentMutes = await bot.mutes.get_all()
    for mute in currentMutes:
        bot.muted_users[mute["_id"]] = mute

    print(bot.muted_users)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.author.id in bot.blacklisted_users:
        return

    if message.content.startswith(f"<@!{bot.user.id}>") and \
        len(message.content) == len(f"<@!{bot.user.id}>"
    ):
        data = await bot.config.get_by_id(message.guild.id)
        if not data or "prefix" not in data:
            prefix = "g$"
        else:
            prefix = data["prefix"]
        await message.channel.send(f"My prefix here is `{prefix}`", delete_after=15)

    await bot.process_commands(message)

async def chng_pr():
    await bot.wait_until_ready()

    statuses = ["g$help", "with Yuichiro!", "with epic lines of code", "getting fancy"]

    while not bot.is_closed():
        status = random.choice(statuses)

        await bot.change_presence(activity=discord.Game(status))

        await asyncio.sleep(60)  

if __name__ == "__main__":
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.load_extension("jishaku")
    bot.loop.create_task(chng_pr())
    bot.run(bot.config_token)
