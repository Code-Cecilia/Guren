import discord
from discord.ext import commands


class Fun(commands.Cog):
    """A bunch of fun commands i made."""

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

    @commands.command(name="Yuichiro")
    async def yui(self, ctx):
        """My lord"""
        await ctx.send("Yuichiro is my lord.")

    @commands.command(name="chatkiller")
    async def chatkiller(self, ctx):
        """Yui's Spoopy Comrades only command."""
        await ctx.send(f"<@&714860016536125451>, hello you killed chat, congratulations.")

    @commands.command(name="senjan")
    async def senjan(self, ctx):
        """The truth about Senjan21"""
        await ctx.message.delete()
        await ctx.send("Pro lengthy pp user.")

    @commands.command()
    @commands.is_owner()
    async def ric(self, ctx):
        await ctx.send("comer merda")


def setup(bot):
    bot.add_cog(Fun(bot))
