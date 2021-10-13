import asyncio
import os
import random
import logging

import discord
from discord.ext import commands
from pathlib import Path

from discord_slash import SlashCommand

import json
from spotdl.search.spotifyClient import SpotifyClient

intents = discord.Intents(messages=True, bans=True, guilds=True)
intents.reactions = True
intents.guild_messages = True
intents.typing = True
intents.members = True
intents.voice_states = True

initial_extensions = ['cogs.leveling']
with open('./bot_config/secrets.json', 'r') as configFile:
    data = json.load(configFile)
    token = data.get("token") 


cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

description = '''A clever discord bot written in python.'''

class NewHelpName(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(
                description=page, color=discord.Color.random())
            embed.set_thumbnail(url=bot.user.avatar_url)
            embed.set_footer(text='')
            await destination.send(embed=embed)
try:
    SpotifyClient.init(
            client_id="854b92f0ab484611b4894281f83fce3d",
            client_secret="3da63e3827b24e51950bbedad7c1acbf",
            user_auth=False
        )
except:
    pass

def get_prefix(bot, message):
    with open('./bot_config/prefixes.json', 'r') as prefixFile:
        prefixes = json.load(prefixFile)
        try:
            prefix_server = prefixes.get(str(message.guild.id))
        except AttributeError:  # direct messages dont have a message.guild
            return 'g$'
            # its ignoring per server prefixes now smh smh smh smh smh smh smh smh smh, got an idea

        if prefix_server is None:
            prefix_server = "g$"  # default prefix
        data = prefix_server
        return commands.when_mentioned_or(data)(bot, message)

# it will allow the server and default prefix but the mention wont work at all the commands.when_mentioned_or in the command_prefix is enough as per the docs but it just does not work
# share the link to the docs, lets see
# okay, i got it
# im in pycharm now
bot = commands.Bot(
    command_prefix=get_prefix,
    description=description,
    owner_id=219410026631135232,
    case_insensitive=True,
    intents=intents,
    help_command=NewHelpName()
)

slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)
bot.config_token = data["token"]
logging.basicConfig(level=logging.INFO)
bot.cwd = cwd
bot.version = "2.0"


@bot.event
async def on_ready():
    print('Logged in as', bot.user.name)
    print("Bot ID:", bot.user.id)
    print('Bot latency:', bot.latency * 1000, 2)
    print('Running discord.py version ' + discord.__version__)


async def chng_pr():
    await bot.wait_until_ready()

    statuses = ["g$help", "with Yuichiro!",
                "with epic lines of code", "getting fancy"]

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
