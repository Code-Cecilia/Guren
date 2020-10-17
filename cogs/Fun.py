import asyncio
import datetime
import os
import random

import discord
from discord.ext import commands


class Fun(commands.Cog):
    """A bunch of shitpost commands that i made"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="say")
    @commands.has_permissions(manage_messages=True)
    async def Say(self, ctx, *, message):
        """I say something"""
        await ctx.message.delete()
        embed = discord.Embed(color=ctx.author.color, timestamp=ctx.message.created_at)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name=f"{ctx.message.author} said:", value=str(message))
        await ctx.send(embed=embed)

    @commands.command(name="nsay")
    @commands.has_permissions(manage_messages=True)
    async def nsay(self, ctx, *, message):
        """Advanced say command"""
        await ctx.message.delete()
        await ctx.send(message)

    @nsay.error
    async def nsay_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("What do you want me to say for you?")

    @Say.error
    async def Say_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("What do you want me to say for you?")

    @commands.command(name="Yuichiro")
    async def yui(self, ctx):
        """My lord"""
        await ctx.send("Yuichiro is my lord.") 

    @commands.command(name="chatkiller")
    async def chatkiller(self, ctx):
        """Uploading Nation only command"""
        await ctx.send(f"<@&714860016536125451>, hello you killed chat, congratulations.")

    @commands.command(name="senjan")
    async def senjan(self, ctx):
        """The truth about Senjan21"""
        await ctx.message.delete()
        await ctx.send("Pro lengthy pp user.")

    @commands.command()
    @commands.cooldown(1, 1500, commands.BucketType.user)
    @commands.is_owner()
    async def annoy(self, ctx, user: discord.Member, *, string=None):
        """Annoys a specific person"""
        if not string:
            if ctx.message.attachments:
                string = ctx.message.attachments[0].url
            else:
                return await ctx.send("Provide an attachment or message.")

        if string:
            if ctx.message.attachments:
                string = f"{string} \n{ctx.message.attachments[0].url}"
            else:
                pass

        await ctx.send("I will now annoy them for the next 25 minutes in 5 minute intervals.")

        timer = 1500
        active = True
        while active:
            timer -= 300
            try:
                await user.send(f"Congratulations :tada: You have been chosen by {str(ctx.author)}"
                                f" to be annoyed with this message every five minutes: {string}")
            except discord.Forbidden:
                return await ctx.send("It appears I have been blocked or the user has disabled DMs.")
            await asyncio.sleep(300)

            if timer == 0:
                active = False

def setup(bot):
    bot.add_cog(Fun(bot))

