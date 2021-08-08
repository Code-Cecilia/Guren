import json

import discord
from discord.ext import commands

from utils import get_color
import datetime

class Modlogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("./bot_config/logging/modlogs_channels.json", "r") as modlogsFile:
            self.modlogsFile = json.load(modlogsFile)

    @commands.command(name="messagelogschannel",
                      aliases=["seteditedlogschannel", "setdeletedlogschannel", "setlogschannel", "setlogchannel"],
                      description="Sets the channel in which edited/deleted message logs are sent.")
    async def set_modlogs_channel(self, ctx, channel: discord.TextChannel):
        channel_id = channel.id
        self.modlogsFile[str(ctx.guild.id)] = int(channel_id)
        with open("./bot_config/logging/modlogs_channels.json", "w") as modlogsFile:
            json.dump(self.modlogsFile, modlogsFile, indent=4)
        await ctx.send(f"Edited/Deleted logs channel set as {channel.mention} succesfully.")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if self.modlogsFile.get(str(before.guild.id)) is None:
            return

        embed = discord.Embed(title=f"Message edited in {before.channel.name}",
                              color=get_color.get_color(before.author), timestamp=after.created_at)
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)
        embed.set_footer(text=f"Author  •  {before.author}  |  Edited", icon_url=before.author.avatar_url)
        # the edited timestamp would come in the right, so we dont need to specify it in the footer
        message_channel = self.bot.get_channel(id=int(self.modlogsFile.get(str(before.guild.id))))
        if message_channel is None:
            return
        await message_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        embed = discord.Embed(title=f"Message deleted in {message.channel.name}",
                              color=get_color.get_color(message.author), timestamp=message.created_at)
        embed.add_field(name="Content", value=message.content, inline=False)
        embed.set_footer(text=f"Author  •  {message.author}  |  Created", icon_url=message.author.avatar_url)
        # the edited timestamp would come in the right, so we dont need to specify it in the footer

        message_channel = self.bot.get_channel(id=int(self.modlogsFile.get(str(message.guild.id))))
        if message_channel is None:
            return
        await message_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        if self.modlogsFile.get(str(messages[0].guild.id)) is None:
            return

        with open(f"./bot_config/tempText/{messages[0].guild.id}.txt", "w") as  temp_textfile:
            for x in messages:
                line1 = f"From: {x.author} | in: {x.channel.name} | Created at: {x.created_at}\n"
                temp_textfile.write(line1)
                temp_textfile.write(f"{x.content}\n\n")

        file = discord.File(f"./bot_config/tempText/{messages[0].guild.id}.txt")
        message_channel = self.bot.get_channel(id=int(self.modlogsFile.get(str(messages[0].guild.id))))
        if message_channel is None:
            return
        await message_channel.send(file=file, content=f"{len(messages)} messages deleted. "
                                                      f"Sending information as text file.")

    # member update event
    @commands.Cog.listener()
    async def on_member_update(self, after, before):
        message_channel = self.bot.get_channel(id=int(self.modlogsFile.get(str(after.guild.id))))
        if message_channel is None:
            return
        if before.display_name != after.display_name:
            embed = discord.Embed(title=f"{after} changed their nickname", color=after.color,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=f"{after.avatar_url}")
            embed.set_footer(text=f"UUID: {after.id}")
            fields = [("After", before.display_name, False),
                      ("Before", after.display_name, False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await message_channel.send(embed=embed)
        elif before.roles != after.roles:
            embed = discord.Embed(title=f"Roles updated for {after}", color=after.color,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=f"{after.avatar_url}")
            embed.set_footer(text=f"UUID: {after.id}")
            fields = [("After", " |\u200B".join([r.mention for r in before.roles]), False),
                      ("Before", " |\u200B ".join([r.mention for r in after.roles]), False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await message_channel.send(embed=embed)

    # ban event
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member:discord.Member):
        message = discord.Message
        message_channel = self.bot.get_channel(id=int(self.modlogsFile.get(str(guild.id))))
        if message_channel is None:
            return
        embed = discord.Embed(title="**Member Banned**",
                              color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.add_field(name=f"{member} was banned from the server",
                        value=f"**Moderator**: {message.author}")
        embed.set_footer(text=f"UUID: {member.id}")
        await message_channel.send(embed=embed)

    # unban event
    @commands.Cog.listener()
    async def on_member_unban(self, guild, member: discord.Member):
        message_channel = self.bot.get_channel(id=int(self.modlogsFile.get(str(guild.id))))
        if message_channel is None:
            return
        embed = discord.Embed(title=f"{member} has been unbanned", description=f"ID: {member.id}", color=get_color.get_color(discord.Color.random()))
        embed.set_thumbnail(url=member.avatar_url)
        await message_channel.send(embed=embed)
    
    # join event
    @commands.Cog.listener()
    async def on_member_join(self, guild, member: discord.Member):
        message_channel = self.bot.get_channel(id=int(self.modlogsFile.get(str(guild.id))))
        if message_channel is None:
            return
        embed = discord.Embed(title=f"Member {member} joined the the server.", color=member.color,
                              timestamp=datetime.datetime.utcnow(),
                              description=f"**Their account was created at:** {member.created_at}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"UUID: {member.id}")
        await message_channel.send(embed=embed)

    # leave event
    @commands.Cog.listener()
    async def on_member_remove(self, guild, member: discord.Member):
        message_channel = self.bot.get_channel(id=int(self.modlogsFile.get(str(guild.id))))
        if message_channel is None:
            return
        roles = [role for role in member.roles]
        embed = discord.Embed(title=f"Member {member} left from the server.", color=member.color,
                              timestamp=datetime.datetime.utcnow(),
                              description=f"**Their account was created at:** {member.created_at}")
        embed.add_field(name="Their roles:", value=" ".join(
            [role.mention for role in roles]))
        embed.set_footer(text=f"UUID: {member.id}")
        embed.set_thumbnail(url=member.avatar_url)
        await message_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Modlogs(bot))