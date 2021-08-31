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
        message_channel_id = self.modlogsFile.get(str(before.guild.id))
        if message_channel_id is None:
            return
        message_channel = self.bot.get_channel(id=int(message_channel_id))
        if message_channel is None:
            return
        message_link = f"https://discord.com/channels/{before.guild.id}/{before.channel.id}/{before.id}"
        embed = discord.Embed(title=f"Message edited in {before.channel.name}",
                              color=get_color.get_color(before.author), timestamp=after.created_at)
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)
        embed.add_field(
            name="Link", value=f"__[Message]({message_link})__", inline=False)
        embed.set_footer(text=f"Author  •  {before.author}  |  Edited")
        embed.set_thumbnail(url=before.author.avatar_url)
        # the edited timestamp would come in the right, so we dont need to specify it in the footer
        try:
            await message_channel.send(embed=embed)
        except:  # embeds dont have a message.content, so it gives us an error
            pass

            # from mahasvan#0001 ape botman.py

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
    async def on_member_update(self, before, after):
        message_channel_id = self.modlogsFile.get(str(before.guild.id))
        if message_channel_id is None:
            return
        message_channel = self.bot.get_channel(id=int(message_channel_id))
        if message_channel is None:
            return

        # nickname change
        if not before.nick == after.nick:
            embed = discord.Embed(title=f"{before}'s nickname has been updated", description=f"ID: {before.id}",
                                  color=get_color.get_color(after), timestamp=before.created_at)

            embed.add_field(
                name="Before", value=before.display_name, inline=False)
            embed.add_field(
                name="After", value=after.display_name, inline=False)

            embed.set_thumbnail(url=after.avatar_url)
            embed.set_footer(text="Account created at")
            await message_channel.send(embed=embed)

        # role change
        if not before.roles == after.roles:
            embed = discord.Embed(title=f"{before}'s roles have been updated", description=f"ID: {before.id}",
                                  color=after.color, timestamp=before.created_at)
            before_roles_str, after_roles_str = "", ""
            for x in before.roles[::-1]:
                before_roles_str += f"{x.mention} "
            for x in after.roles[::-1]:
                after_roles_str += f"{x.mention} "
            embed.add_field(
                name="Before", value=before_roles_str, inline=False)
            embed.add_field(name="After", value=after_roles_str, inline=False)
            embed.set_thumbnail(url=after.avatar_url)
            embed.set_footer(text="Account created at")
            await message_channel.send(embed=embed)

            # from mahasvan#0001 ape botman.py

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
    async def on_member_join(self, member):
        message_channel_id = self.modlogsFile.get(str(member.guild.id))
        if message_channel_id is None:
            return
        message_channel = self.bot.get_channel(id=int(message_channel_id))
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
    async def on_member_remove(self, member):
        message_channel_id = self.modlogsFile.get(str(member.guild.id))
        if message_channel_id is None:
            return
        message_channel = self.bot.get_channel(id=int(message_channel_id))
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