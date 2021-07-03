import discord
from discord.ext import commands
import datetime
import random

class Roleplay(commands.Cog):
    """Roleplay commands. If you'd like to add a gif to the bot database please contact me on discord: Yuichiro#0001"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def cookie(self, ctx, member: discord.Member = None):
        """Give a cookie to someone."""
        member = ctx.author if not member else member
        embed = discord.Embed(title="Nom nom nom!", description="**{1}** gave a cookie to **{0}**! :cookie:".format(member.name, ctx.message.author.name), color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        """Hugs someone."""
        member = ctx.author if not member else member
        embed = discord.Embed(title="Huggies!", description="**{1}** hugs **{0}**!".format(member.name, ctx.message.author.name), color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_image(url="https://media1.tenor.com/images/0be55a868e05bd369606f3684d95bf1e/tenor.gif?itemid=7939558")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def pet(self, ctx, member: discord.Member):
        """Pets someone."""
        member = ctx.author if not member else member
        embed = discord.Embed(title="Petpet!", description="**{1}** gave **{0}** a pat on the head!".format(member.name, ctx.message.author.name), color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_image(url="https://media.giphy.com/media/TA6Fq1irTioFO/giphy.gif")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx, member: discord.Member):
        """Kisses someone."""
        member = ctx.author if not member else member
        embed = discord.Embed(title="Kisses!", description="**{1}** gave **{0}** a kiss!".format(member.name, ctx.message.author.name), color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_image(url="https://cdn.discordapp.com/attachments/765604084057112579/813427435054956615/tenor.gif")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def bite(self, ctx, member: discord.Member):
        """Bites someone."""
        member = ctx.author if not member else member
        embed = discord.Embed(title="O-O", description="**{1}** has bitten **{0}**'s hand!".format(member.name, ctx.message.author.name), color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_image(url="https://media.giphy.com/media/YW3obh7zZ4Rj2/giphy.gif")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def eat(self, ctx, member: discord.Member):
        """Vore your friends."""
        member = ctx.author if not member else member
        embed = discord.Embed(title="Nom nom!", description="**{1}** ate **{0}**!".format(member.name, ctx.message.author.name), color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_image(url="https://cdn.discordapp.com/emojis/588077285412962304.gif?v=1")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, member: discord.Member):
        """Slap lordofpc."""
        member = ctx.author if not member else member
        embed = discord.Embed(title="Slapped!", description="**{1}** slapped **{0}**!".format(member.name, ctx.message.author.name), color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_image(url="https://media.giphy.com/media/Gf3AUz3eBNbTW/giphy.gif")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def rub(self, ctx, member: discord.Member):
        """Rubs someone."""
        member = ctx.author if not member else member
        embed = discord.Embed(title="Rubrub!", description="**{1}** rubbed **{0}**!".format(member.name, ctx.message.author.name), color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_image(url="https://media1.tenor.com/images/7e88f0b6abbd8d695ce253f37a8291d7/tenor.gif?itemid=5026974")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def fart(self, ctx):
        """:thinking:."""
        replies = ["Ew", "Toot", "Stinky", "Disgusting", "Poot"]
        await ctx.send(random.choice(replies))

    @commands.command()
    async def cry(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        embed = discord.Embed(title=f"{ctx.author} is crying! :(", color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_image(url="https://cdn.discordapp.com/attachments/716649261449740329/852646200645517352/c4f0d6c08257f3a75725a7583894b1b8.gif")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Roleplay(bot))