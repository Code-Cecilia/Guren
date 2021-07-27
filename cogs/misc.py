import datetime
import json
import os
import re

import aiohttp
import discord
from discord.ext import commands
from discord_slash import SlashContext

from utils import time_custom
from utils import UrbanDict
from utils import count_lines
from utils import quotes


class Misc(commands.Cog):
    """Commands that i don't know where to put."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(
        name="ping",
        description="Shows the bot latency"
    )
    @commands.guild_only()
    async def ping(self, ctx: SlashContext, member: discord.Member = None):
        """Shows the bot ping"""
        member = ctx.author if not member else member
        embed = discord.Embed(
            title="Bot's latency", colour=member.color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Websocket Latency",
                        value=f"{'Pong! {0}'.format(round(self.bot.latency * 1000, 2))}ms")
        embed.set_footer(
            text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(
            url=f"{self.bot.user.avatar_url}")

        await ctx.send(embed=embed)

    @commands.command(
        name="fact",
        description="Sends a random fact."
    )
    async def fact(self, ctx):
        """Random fact"""
        url = f'https://uselessfacts.jsph.pl/random.json?language=en'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                r = await response.json()
                fact = r['text']
                embed = discord.Embed(
                    title=f'Random Fact', colour=ctx.author.colour, timestamp=ctx.message.created_at)
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/669973636156751897/734100544918126592/article-fact-or-opinion.jpg")
                embed.set_footer(text="Useless Facts")
                embed.add_field(name='***Fun Fact***',
                                value=fact, inline=False)
                await ctx.send(embed=embed)

    @commands.command(
        name="invite",
        aliases=['botinvite', 'i'],
        description="Sends an invite link for the bot."
    )
    async def invite(self, ctx):
        await ctx.send(
            "Invite me to your server using this link: https://discord.com/oauth2/authorize?client_id=669973381067571240&scope=bot&permissions=8")

    @commands.command(name='setoffset', description='Sets the user\'s time offset.\n'
                                                    'Format for offset: `-2:30`, `+2:30`, or just `2:30`\n'
                                                    '**Nerd note**: the regex for the offset is '
                                                    r'`^[+\-]?\d+:\d+$`')
    async def set_offset(self, ctx, offset):
        pattern = r'^[+\-]?\d+:\d+$'
        # matches the pattern, and if it fails, returns an error message
        if not re.match(pattern, offset):
            return await ctx.send('Improper offset format. Please read the help command for more info.')

        if not os.path.exists('./bot_config/time.json'):  # create file if not exists
            with open('./bot_config/time.json', 'w') as jsonFile:
                print('./bot_config/time.json has been created')
                json.dump({}, jsonFile)

        with open('./bot_config/time.json', 'r') as timeFile:
            time_data = json.load(timeFile)

        time_data[ctx.author.id] = offset

        with open('./bot_config/time.json', 'w') as timeFile:
            json.dump(time_data, timeFile)

        await ctx.send(f'Time offset set as {offset} successfully.')

    @commands.command(name='time',
                      description='Gets the time of the user. if user does not have a timezone set, '
                                  'they can use an offset like "+2:30"')
    async def get_time(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        user_id = str(user.id)

        if not os.path.exists('./bot_config/time.json'):  # create file if not exists
            with open('./bot_config/time.json', 'w') as jsonFile:
                print('./bot_config/time.json has been created')
                json.dump({}, jsonFile)

        with open('./bot_config/time.json', 'r') as timeFile:
            time_data = json.load(timeFile)

        user_offset = time_data.get(user_id)

        if user_offset is None:
            return await ctx.send(
                f'_{user.display_name}_ has not set their offset. They can do so using the `setoffset` command.')

        """None of the following code is executed if user_offset is None"""

        final_time_string = time_custom.time_bm(user_offset)

        await ctx.send(final_time_string)

    @commands.command(name='define', description='Pulls a description from Urban Dictionary of the term entered as '
                                                 'argument.\n '
                                                 'Take caution, as sometimes it can be a bit... too accurate.')
    async def define_from_urban(self, ctx, *, term):
        try:
            word, definition, likes, dislikes, example, author = await UrbanDict.define(term)
        except:
            await ctx.send(f'Could not load definition for **{term}**.')
            return
        embed = discord.Embed(
            title=word, description=definition, color=discord.Color.random())
        embed.set_footer(
            text=f'Powered by UrbanDictionary | Author - {author}')
        embed.add_field(name="Example", value=example, inline=False)
        embed.add_field(
            name='Likes', value=f"👍 {likes} | 👎 {dislikes}", inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='countlines', aliases=['countline'], description='Counts the number of lines of python code '
                                                                            'the bot currently has.')
    async def countlines_func(self, ctx):
        lines = count_lines.countlines('./')
        final_str = f"I am made of {lines} lines of python code. Pretty cool, imo."
        await ctx.send(final_str)

    @commands.command(name='inspire', aliases=['quote'], description='Sends a random quote')
    async def get_quote_func(self, ctx):
        quote = quotes.get_quote()
        await ctx.send(quote)


def setup(bot):
    bot.add_cog(Misc(bot))
