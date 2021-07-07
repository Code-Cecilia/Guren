import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext
import aiohttp

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @cog_ext.cog_slash(
        name="ping",
        description="shows bot latency"
    )
    async def ping(self, ctx):
        await ctx.send("a")

def setup(bot):
    bot.add_cog(Slash(bot))