import asyncio

import discord
from discord.ext import commands


class Events(commands.Cog):
    """Comtains a number of events when errors happen"""
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.author == self.bot.user:
            return 


        user = message.author
        msg = message.content
        print(f"{user} said {msg}")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) is 0 and int(m) is 0:
                await ctx.send(f' You must wait {int(s)} seconds to use this command!')
            elif int(h) is 0 and int(m) is not 0:
                await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
            else:
                await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("Hey! You lack permission to use this command.")     
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found!")
        else:    
            raise error


def setup(bot):
    bot.add_cog(Events(bot))
