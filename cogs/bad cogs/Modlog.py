import datetime

import discord
from discord import TextChannel, Message
from discord.ext import commands

import utils.json_loader


class Modlog(commands.Cog):
    """Logging"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.has_permissions(administrator=True)
    @commands.command(
        name="modlog", description="setup mod-logs", usage="<user>"
    )
    async def modlog(self, ctx, channel: discord.TextChannel):
        guild_ID = ctx.guild.id
        data = utils.json_loader.read_json("server_config")
        data[str(guild_ID)] = {"mod-logID": None, "name": None, "guildID": ctx.guild.id}
        if [str(ctx.guild.id)] not in data:
            utils.json_loader.write_json(data, "server_config")
            data[str(ctx.guild.id)]["mod-logID"] = channel.id
            data[str(ctx.guild.id)]["guildID"] = ctx.guild.id
            data[str(ctx.guild.id)]["name"] = ctx.guild.name
            utils.json_loader.write_json(data, "server_config")
            await ctx.send("Mod logs channel id stored successfully")
        else:
            await ctx.send("Mod logs were already set!")
            return;

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        data = utils.json_loader.read_json("server_config")
        guild_ID = member.guild.id
        modlogs = self.bot.get_channel(data[str(guild_ID)]["mod-logID"])
        embed = discord.Embed(title=f"Member {member} joined the the server.", color=member.color,
                              timestamp=datetime.datetime.utcnow(),
                              description=f"**Their account was created at:** {member.created_at}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"UUID: {member.id}")
        await modlogs.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        data = utils.json_loader.read_json("server_config")
        guild_ID = member.guild.id
        roles = [role for role in member.roles]
        modlogs = self.bot.get_channel(data[str(guild_ID)]["mod-logID"])
        embed = discord.Embed(title=f"Member {member} left from the server.", color=member.color,
                              timestamp=datetime.datetime.utcnow(),
                              description=f"**Their account was created at:** {member.created_at}")
        embed.add_field(name="Their roles:", value=" ".join([role.mention for role in roles]))
        embed.set_footer(text=f"UUID: {member.id}")
        embed.set_thumbnail(url=member.avatar_url)
        await modlogs.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, after, before):
        guild_ID = after.guild.id
        data = utils.json_loader.read_json("server_config")
        modlogs = self.bot.get_channel(data[str(guild_ID)]["guild_ID"]["mod-logID"])
        if not after.author.bot:
            if before.content != after.content:
                embed = discord.Embed(title=f"Message Edited by {after.author}", color=after.author.color,
                                      description=f"Message edited in {after.channel.mention}",
                                      timestamp=datetime.datetime.utcnow())
                fields = [("Before", before.content, False)]
                embed.set_thumbnail(url=f"{after.author.avatar_url}")
                embed.set_footer(text=f"UUID: {after.id}")
                embed.add_field(name="After", value=after.content, inline=False)
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                await modlogs.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild_ID = message.guild.id
        data = utils.json_loader.read_json("server_config")
        modlogs = self.bot.get_channel(data[str(guild_ID)]["mod-logID"])
        if not message.author.bot:
            embed = discord.Embed(title=f"Message deleted by {message.author}",
                                  description=f"Message deleted in {message.channel.mention}", color=0xE74C3C,
                                  timestamp=datetime.datetime.utcnow())
            fields = [("Content", message.content, False)]
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_footer(text=f"UUID: {message.author.id}")
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await modlogs.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, after, before):
        guild_ID = after.guild.id
        data = utils.json_loader.read_json("server_config")
        modlogs = self.bot.get_channel(data[str(guild_ID)]["mod-logID"])
        if before.display_name != after.display_name:
            embed = discord.Embed(title=f"Nickname change made by {after}", color=after.color,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=f"{after.avatar_url}")
            embed.set_footer(text=f"UUID: {after.id}")
            fields = [("After", before.display_name, False),
                      ("Before", after.display_name, False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await modlogs.send(embed=embed)
        elif before.roles != after.roles:
            embed = discord.Embed(title=f"Roles updated for {after}", color=after.color,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=f"{after.avatar_url}")
            embed.set_footer(text=f"UUID: {after.id}")
            fields = [("After", " |\u200B".join([r.mention for r in before.roles]), False),
                      ("Before", " |\u200B ".join([r.mention for r in after.roles]), False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await modlogs.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user: discord.Member):
        message = Message
        data = utils.json_loader.read_json("server_config")
        member = user
        guild_ID = member.guild.id
        modlogs = self.bot.get_channel(data[str(guild_ID)]["mod-logID"])
        embed = discord.Embed(title="**Member Banned**", color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.add_field(name=f"{member} was banned from the server", value=f"**Moderator**: {message.author}")
        embed.set_footer(text=f"UUID: {member.id}")
        await modlogs.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user: discord.Member):
        message = Message
        data = utils.json_loader.read_json("server_config")
        member = user
        guild_ID = guild.id
        modlogs = self.bot.get_channel(data[str(guild_ID)]["mod-logID"])
        embed = discord.Embed(title="**Member Unbanned**", color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.add_field(name=f"{member} was unbanned from the server", value=f"**Moderator**: {message.author}")
        embed.set_footer(text=f"UUID: {member.id}")
        await modlogs.send(embed=embed)


def setup(bot):
    bot.add_cog(Modlog(bot))
