import datetime
import os
import random
import traceback

import json
import asyncio
import discord
from discord.ext import commands
from discord import TextChannel


import utils.json_loader


class Config(commands.Cog):
    """Server configuration commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(
        name="prefix",
        aliases=["changeprefix", "setprefix"],
        description="Change your guilds prefix!",
        usage="[prefix]",
    )
    @commands.has_guild_permissions(manage_guild=True)
    async def prefix(self, ctx, *, prefix="py."):
        """Change your guild prefix"""
        await self.bot.config.upsert({"_id": ctx.guild.id, "prefix": prefix})
        await ctx.send(
            f"The guild prefix has been set to `{prefix}`. Use `{prefix}prefix [prefix]` to change it again!"
        )

    @commands.command(
        name="deleteprefix",
        aliases=["dp"],
        description="Delete your guilds prefix!"
    )
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def deleteprefix(self, ctx):
        """Delete the current guild prefix"""
        await self.bot.config.unset({"_id": ctx.guild.id, "prefix": 1})
        await ctx.send("This guilds prefix has been set back to the default")

    @commands.command(
        name="setsuggestionchannel",
        aliases=["sc"],
        description="Set a suggestion channel")
    @commands.has_guild_permissions(manage_channels=True)
    async def setsuggestionchannel(self, ctx, channel: discord.TextChannel):
        """Set a suggestion channel."""
        guild_ID = ctx.guild.id
        data = utils.json_loader.read_json("suggestionc")
        data[str(guild_ID)] = {"suggestionC": None, "ownerID": None}
        utils.json_loader.write_json(data, "suggestionc")
        await ctx.send("Guild ID stored successfully")
        data = utils.json_loader.read_json("suggestionc")
        data[str(ctx.guild.id)]["ownerID"] = ctx.guild.owner.id
        data[str(ctx.guild.id)]["suggestionC"] = channel.id
        utils.json_loader.write_json(data, "suggestionc")
        await ctx.send("Suggestions channel setup successfully")

    @commands.command(name='setmuterole', description='Sets the role assigned to muted people. '
                                                      'Use `createmuterole` for creating a muted role and '
                                                      'automatically setting permissions to every channel.')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def set_mute_role(self, ctx, role: discord.Role):
        if not os.path.exists(f'bot_config/guild{ctx.guild.id}.json'):
            with open(f'bot_config/guild{ctx.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile)

        with open(f'bot_config/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)

        data['mute_role'] = role.id

        with open(f'bot_config/guild{ctx.guild.id}.json', 'w') as jsonFile:
            json.dump(data, jsonFile)

        await ctx.send(f'Mute role set to **{role.name}** successfully.')

    @commands.command(name='createmuterole', description='Creates a mute role, and sets messaging permissions to '
                                                         'every channel.\n '
                                                         'the `rolename` argument is optional. (Defaults to "Muted")')
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def create_mute_role(self, ctx, rolename=None):
        if rolename is None:
            rolename = 'Muted'
        guild = ctx.guild
        mutedRole = await guild.create_role(name=rolename)  # creating the role
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, use_slash_commands=False)
            # setting permissions for each channel
        await ctx.send(f'Created role **{mutedRole}** and set permissions accordingly.')

    @commands.command(
        name="suggest",
        aliases=["sg"],
        description="Suggest something")
    async def suggest(self, ctx, *, message):
        data = utils.json_loader.read_json("suggestionc")
        guild_ID = ctx.guild.id
        suggestions = self.bot.get_channel(data[str(guild_ID)]["suggestionC"])
        await ctx.message.delete()
        await ctx.send("Suggestion sent.")
        embed = discord.Embed(
            title='Suggestion', description=f'Suggested by: {ctx.author.mention}', color=discord.Color.dark_purple())
        embed.set_author(name=f"{ctx.author}",
                         icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="Suggestion:", value=str(message))
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text="Vote for this suggestion!")
        poo = await suggestions.send(embed=embed)
        await poo.add_reaction("☑️")
        await poo.add_reaction("✖️")

    @suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description='❌ Please make sure to include your suggestion:\n```!suggest <suggestion>```', color=discord.Color.dark_red())
            embed.set_author(name=f"{ctx.author}",
                             icon_url=f"{ctx.author.avatar_url}")
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Config(bot))
