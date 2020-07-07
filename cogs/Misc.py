import discord
import datetime
import os
from discord.ext import commands

class Misc(commands.Cog):
    """Commands that i dont know where to put"""
    def __init__(self, bot):
        self.bot = bot

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

    
def setup(bot):
    bot.add_cog(Misc(bot))