import discord
from discord.ext import commands

import datetime

class Minecraft(commands.Cog):
    """ Commands for the server Originals """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command()
    async def mc(self, ctx, member: discord.Member = None):
        """ Status about the Originals Server """
        member = ctx.author if not member else member
        embed = discord.Embed(title="MC Server Stats", timestamp=datetime.datetime.utcnow(), color=member.color)
        embed.add_field(name="Originals IP", value="play.comrades.digital")
        embed.add_field(name="Modpack Link", value=f"[Link](https://www.technicpack.net/modpack/ysp-originals.1726052)")
        embed.add_field(name="Server Stats", value="Open Beta")
        embed.add_field(name="Misc Information", value=f"The server is open to cracked and premium secured with a login plugin. Cracked launchers can be found here: [HackPhoenix](https://www.hackphoenix.com/technic-launcher/) | [McLauncher](https://mc-launcher.com/launcher/technic). You need to allocate 2GB of ram atleast and must use [Java 64BITS](https://java.com/en/download/).")
        embed.set_footer(text="Originals 2020")

        await ctx.send(embed=embed)

    @commands.command()
    async def vote(self, ctx, member: discord.Member = None):
        """ Can be run in game /vote """
        member = ctx.author if not member else member
        embed = discord.Embed(title="Websites to vote.", timestamp=datetime.datetime.utcnow(), color=member.color)
        embed.add_field(name="Vote Link 1", value=f"[Link](https://tinyurl.com/originals-vote1)")
        embed.add_field(name="Vote Link 2", value=f"[Link](https://tinyurl.com/originals-vote2)")
        embed.add_field(name="Vote Link 3", value=f"[Link](https://tinyurl.com/originals-vote3)")
        embed.set_footer(text="Originals 2020")
        await ctx.send(embed=embed)

    @commands.command()
    async def store(self, ctx, member: discord.Member = None):
        """ Originals store link """
        member = ctx.author if not member else member
        embed = discord.Embed(title="Buy vip here", timestamp=datetime.datetime.utcnow(), color=member.color)
        embed.add_field(name="Our Webstore", value=f"[YSP Originals](https://shop.comrades.digital/)")
        embed.set_footer(text="Ooriginals 2020")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Minecraft(bot))
