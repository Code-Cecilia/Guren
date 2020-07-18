import datetime
import os

import aiohttp
import discord
import pendulum
from discord.ext import commands


class Misc(commands.Cog):
    """Commands that i dont know where to put"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="ping")
    @commands.guild_only()
    async def ping(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        embed = discord.Embed(title="Bot's latency", colour=member.color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Websocket Latency", value=f"{'Pong! {0}'.format(round(self.bot.latency*1000, 2))}ms")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/669973381067571240/350b378596401f453fb4d5bd3411a682.webp?size=1024")
            
        await ctx.send(embed=embed)
        print(ctx.author.name, 'used the command ping')

    @commands.command()
    async def fact(self, ctx):
        url = f'https://uselessfacts.jsph.pl/random.json?language=en'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                r = await response.json()
                fact = r['text']
                embed = discord.Embed(title=f'Random Fact', colour=ctx.author.colour, timestamp=ctx.message.created_at)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/669973636156751897/734100544918126592/article-fact-or-opinion.jpg")
                embed.set_footer(text="Useless Facts")
                embed.add_field(name='***Fun Fact***', value=fact, inline=False)
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))
