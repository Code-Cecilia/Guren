import asyncio

import discord
from discord.ext import commands


class Events(commands.Cog):
    """Comtains a number of events when errors happen"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Hey! You lack permission to use this command.")
        if isinstance(error, commands.BadArgument):
            await ctx.send("A bad argument has been passed, please check the context and the needed arguments.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("An argument is missing or invalid. Input the argument in order to run this command.")
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found!")
        else:
            raise error

def setup(bot):
    bot.add_cog(Events(bot))
