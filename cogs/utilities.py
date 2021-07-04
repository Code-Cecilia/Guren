import datetime
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext
import git
import os

class Utilities(commands.Cog):
    """Usefull commands, mostly informative commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
        
    
    @commands.command(name="avatar")
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member = None):
        """Shows your avatar."""
        member = ctx.author if not member else member
        embed = discord.Embed(title=f"{member} avatar", colour=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=f"{member.avatar_url}")
        await ctx.send(embed=embed)
        print(ctx.author.name, 'used the command avatar')    
 
    @commands.command(name="userinfo")
    @commands.guild_only()
    async def userinfo(self, ctx, member: discord.Member = None):
        """Shows information about a member."""
        member = ctx.author if not member else member
        roles = [role for role in member.roles]
        embed = discord.Embed(color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Guild name:", value=member.display_name)
        embed.add_field(name="Created at:", value=member.created_at)
        embed.add_field(name="Joined at:", value=member.joined_at)
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Top Role:", value=member.top_role.mention)
        embed.add_field(name="Bot?", value=member.bot)
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo")
    @commands.guild_only()
    async def serverinfo(self, ctx, guild: discord.Guild = None, member: discord.Member = None):
        """Shows information about the server."""
        guild = ctx.guild if not guild else guild
        embed = discord.Embed(title=f"{guild.name}", colour=ctx.author.color, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="ID:", value=guild.id, inline=False)
        embed.add_field(name="Server name:", value=guild.name, inline=False)
        embed.add_field(name="Server Owner:", value=f"<@{guild.owner_id}>", inline=False)
        embed.add_field(name="Created at:", value=ctx.guild.created_at, inline=False)
        embed.add_field(name="Role count:", value=len(guild.roles), inline=False)
        embed.add_field(name="Booster Count", value=guild.premium_subscription_count, inline=False)
        embed.add_field(name="Member Count", value=guild.member_count, inline=False)
        embed.add_field(name="Max Emojis", value=guild.emoji_limit, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        """Shows bot stats."""

        repo = git.Repo(os.getcwd())
        master = repo.head.reference
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name='Bot Version:', value="2.0")
        embed.add_field(name='Discord.Py Version', value=dpyVersion, inline=True)
        embed.add_field(name='Total Guilds:', value=serverCount, inline=True)
        embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Bot Developer:', value="<@219410026631135232>")
        embed.add_field(name='Latest commit:', value=f"`{master.commit.hexsha}`\n`{master.commit.message}`")
        embed.add_field(name="Support Server", value=f"[I live here.](https://discord.gg/8wCez2n)")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)          

def setup(bot):
    bot.add_cog(Utilities(bot))
