import os
import discord
import datetime
from discord.ext import commands
import asyncio
import random
import dashcord
import routes

description = ''' A clever discord bot written in python for the guild Uploading Nation'''

bot = commands.Bot(
    commands.when_mentioned_or('g$'), 
    description=description,
    owner_id=219410026631135232,
    case_insensitive=True
)

@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)
    print("Bot ID:", bot.user.id)
    print('Bot latency:', bot.latency*1000, 2)
    print('Running discord.py version ' + discord.__version__)
    # await bot.dashboard.start("", 5000)

# app = dashcord.App(bot, template_path="templates", static_path="static", routing_file="routes");

for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            print(f'Loaded {cog} successfully')
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} can not be loaded:")
            raise e

async def chng_pr():
    await bot.wait_until_ready()

    statuses = ["g$help", "with Yuichiro!", "with epic lines of code", "getting fancy"]

    while not bot.is_closed():
        status = random.choice(statuses)

        await bot.change_presence(activity=discord.Game(status))

        await asyncio.sleep(60)    



bot.loop.create_task(chng_pr())
bot.load_extension("jishaku")
bot.run(""your mom fat")
