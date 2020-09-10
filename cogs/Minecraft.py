import discord
from discord.ext import commands

import datetime
import mcstatus
from mcstatus import MinecraftServer

class Minecraft(commands.Cog):
    """ Commands for the network YSP """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command()
    async def originals(self, ctx, member: discord.Member = None):
        """ Status about the Originals Server """
        member = ctx.author if not member else member
        embed = discord.Embed(title="MC Server Stats", timestamp=datetime.datetime.utcnow(), color=member.color)
        embed.add_field(name="Version:", value="1.12.2 Modded")
        embed.add_field(name="Originals IP", value="hub.comrades.digital")
        embed.add_field(name="Modpack Link", value=f"[Link](https://www.technicpack.net/modpack/ysp-originals.1726052)")
        embed.add_field(name="Server Stats", value="Open Beta")
        embed.add_field(name="Misc Information", value=f"The server is open to cracked and premium secured with a login plugin. Cracked launchers can be found here: [HackPhoenix](https://www.hackphoenix.com/technic-launcher/) | [McLauncher](https://mc-launcher.com/launcher/technic). You need to allocate 2GB of ram atleast and must use [Java 64BITS](https://java.com/en/download/).", inline=False)
        embed.set_footer(text="YSP 2020")
        await ctx.send(embed=embed)

    @commands.command()
    async def sky(self, ctx, member: discord.Member = None):
        """ Status about the Sky Server """
        member = ctx.author if not member else member
        embed = discord.Embed(title="MC Server Stats", timestamp=datetime.datetime.utcnow(), color=member.color)
        embed.add_field(name="Version:", value="1.12.2 Modded")
        embed.add_field(name="Sky IP", value="hub.comrades.digital")
        embed.add_field(name="Modpack Link", value=f"[Link](https://www.technicpack.net/modpack/ysp-sky.1745227)")
        embed.add_field(name="Server Stats", value="COMING SOON! IN DEVELOPMENT!")
        embed.add_field(name="Misc Information", value=f"The server is open to cracked and premium secured with a login plugin. Cracked launchers can be found here: [HackPhoenix](https://www.hackphoenix.com/technic-launcher/) | [McLauncher](https://mc-launcher.com/launcher/technic). You need to allocate 2GB of ram atleast and must use [Java 64BITS](https://java.com/en/download/).", inline=False)
        embed.set_footer(text="YSP 2020")

        await ctx.send(embed=embed)

    @commands.command()
    async def classic(self, ctx, member: discord.Member = None):
        """ Status about the Classic Server """
        member = ctx.author if not member else member
        embed = discord.Embed(title="MC Server Stats", timestamp=datetime.datetime.utcnow(), color=member.color)
        embed.add_field(name="Version:", value="1.16.2 Vanilla")
        embed.add_field(name="Classic IP", value="hub.comrades.digital")
        embed.add_field(name="Misc Information", value=f"The server is open to cracked and premium secured with a login plugin. Cracked launchers can be found here: [HackPhoenix](https://www.hackphoenix.com/technic-launcher/) | [McLauncher](https://mc-launcher.com/launcher/technic). You need to allocate 2GB of ram atleast and must use [Java 64BITS](https://java.com/en/download/).", inline=False)
        embed.set_footer(text="YSP 2020")

        await ctx.send(embed=embed)

    @commands.command()
    async def vote(self, ctx, member: discord.Member = None):
        """ Can be run in game /vote """
        member = ctx.author if not member else member
        embed = discord.Embed(title="Websites to vote.", timestamp=datetime.datetime.utcnow(), color=member.color)
        embed.add_field(name="Vote Link 1", value=f"[Link](https://tinyurl.com/originals-vote1)")
        embed.add_field(name="Vote Link 2", value=f"[Link](https://tinyurl.com/originals-vote2)")
        embed.add_field(name="Vote Link 3", value=f"[Link](https://tinyurl.com/originals-vote3)")
        embed.set_footer(text="YSP 2020")
        await ctx.send(embed=embed)

    @commands.command()
    async def store(self, ctx, member: discord.Member = None):
        """ Originals store link """
        member = ctx.author if not member else member
        embed = discord.Embed(title="Buy vip here", timestamp=datetime.datetime.utcnow(), color=member.color, description="Note: Only the server Originals has a webstore. The others are yet still in development!")
        embed.add_field(name="Our Webstore", value=f"[YSP Originals](http://ysp-originals.tebex.io)")
        embed.set_footer(text="YSP 2020")
        await ctx.send(embed=embed)

    @commands.command()
    async def servers(self, ctx, member: discord.Member = None):
        """ Gathers the players online from all of the servers. """
        member = ctx.author if not member else member
        server1 = MinecraftServer.lookup("exposed ip :3")
        server2 = MinecraftServer.lookup("exposed ip :3")
        server3 = MinecraftServer.lookup("exposed ip :3")
        status1 = server1.status()
        query1 = server1.query()
        status2 = server2.status()
        query2 = server2.query()
        status3 = server3.status()
        query3 = server3.query()
        embed = discord.Embed(title="Network Metrics", timestamp=datetime.datetime.utcnow(), color=member.color)
        embed.add_field(name="Sky Status", value="The server has `{0}/48` players online: `{1}`".format(str(len(query3.players.names)), ", ".join(query3.players.names)), inline=False)
        embed.add_field(name="Originals Status", value="The server has `{0}/48` players online: `{1}`".format(str(len(query1.players.names)), ", ".join(query1.players.names)), inline=False)
        embed.add_field(name="Classic Status", value="The server has `{0}/48` players online: `{1}`".format(str(len(query2.players.names)), ", ".join(query2.players.names)), inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/655111976891973648/746888357795332246/large.jpg")
        embed.add_field(name="Network IP", value="hub.comrades.digital")
        embed.set_footer(text="YSP 2020")

        await ctx.send(embed=embed)
        # await ctx.send("The server has {0} players online: {1}".format(str(len(query.players.names)), ", ".join(query.players.names)))


def setup(bot):
    bot.add_cog(Minecraft(bot))
