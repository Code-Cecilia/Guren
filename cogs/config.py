import datetime
import os
import random
import traceback

import json
import asyncio
import discord
from discord.ext import commands
from discord import TextChannel

with open('bot_config/config.json') as configFile:
    configs = json.load(configFile)
    prefix = configs.get("prefix")

class Config(commands.Cog):
    """Server configuration commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name='setup', description='Used to set the bot up, for welcome messages, mute roles, etc.\n'
                                                'Recommended to set the bot up as early as possible when it joins a '
                                                'server.')
    @commands.guild_only()
    async def setup_welcome(self, ctx):
        embed = discord.Embed(title='You can setup preferences for your server with these commands.',
                              timestamp=ctx.message.created_at,
                              color=discord.Color.random())

        embed.add_field(name='Set channel for welcome messages',
                        value=f'`{prefix}setwelcomechannel [channel]`\nExample: `{prefix}setwelcomechannel #welcome`\n'
                              f'__**What you\'d see:**__\n'
                              f':inbox_tray: | {ctx.author.mention} has joined **{ctx.guild.name}**! Say hi!\n'
                              f':outbox_tray: | {ctx.author.mention} has left **{ctx.guild.name}**. Until Next time!',
                        inline=False)

        embed.add_field(name='Set the mute role for this server',
                        value=f'`{prefix}setmuterole [role]`\nExample: `{prefix}setmuterole muted` '
                              f'(muted must be an actual role).\n'
                              f'You can create a mute role by `{prefix}createmuterole [role name]`',
                        inline=False)

        embed.add_field(name='Set the default Member role for this server',
                        value=f'`{prefix}setmemberrole [role]`\nExample: `{prefix}setmemberrole Member`'
                              f' (Member must be an actual role).\n'
                              f'If you want to turn off AutoRole, make a role, assign the member role to that role, and delete the role',
                        inline=False)

        embed.add_field(name='Set the default channel for BotChat.',
                        value=f'`{prefix}setbotchatchannel [channel]`\nExample: `{prefix}setbotchatchannel #botchat`'
                              f' (`channel` must be an actual channel).\n'
                              f'If you want to turn off botchat, make a channel, assign botchat to that channel, and delete the channel.',
                        inline=False)

        embed.add_field(name='Set a custom prefix for this server.',
                        value=f'`{prefix}setprefix [prefix]`',
                        inline=False)

        embed.set_footer(text=f'Command requested by {ctx.author.name}')
        await ctx.send(embed=embed)


    @commands.command(name='changeprefix', aliases=['setprefix'], description='Sets the server-specific prefix')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def change_prefix_func(self, ctx, prefix):
        with open('./bot_config/prefixes.json', 'r') as f:
            data = json.load(f)

        data[str(ctx.guild.id)] = prefix

        with open('./bot_config/prefixes.json', 'w') as f:
            json.dump(data, f, indent=4)
        await ctx.send(f'The prefix for this server has changed to {prefix}')

    @commands.command(
        name="setsuggestionchannel",
        aliases=["sc"],
        description="Set a suggestion channel")
    @commands.has_guild_permissions(manage_channels=True)
    async def setsuggestionchannel(self, ctx, channel: discord.TextChannel):
        """Set a suggestion channel."""
        guild_ID = ctx.guild.id
        with open('./bot_config/suggestionc.json', 'r') as f:
            data = json.load(f)
        
        data[str(ctx.guild.id)] = {'suggestionC:': channel.id}
        
        with open('./bot_config/suggestionc.json', 'w') as jsonFile:
            json.dump(data, jsonFile)
        
        await ctx.send("Channel setup successfully")

    @commands.command(name='setmuterole', description='Sets the role assigned to muted people. '
                                                      'Use `createmuterole` for creating a muted role and '
                                                      'automatically setting permissions to every channel.')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def set_mute_role(self, ctx, role: discord.Role):
        if not os.path.exists(f'bot_config/guilds/guild{ctx.guild.id}.json'):
            with open(f'bot_config/guild{ctx.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile)

        with open(f'bot_config/guilds/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)

        data['mute_role'] = role.id

        with open(f'bot_config/guilds/guild{ctx.guild.id}.json', 'w') as jsonFile:
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
        #data = utils.json_loader.read_json("suggestionc")
        with open('./bot_config/suggestionc', 'r') as f:
            data = json.load(f) # idk really what to do here for it to read ree
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


    @commands.command(name='setwelcomechannel', description="Used to set the channel welcome messages arrive. "
                                                            "See description of the `setup` command for more info.")
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def set_welcome_channel(self, ctx, channel: discord.TextChannel):
        channel_id = channel.id
        if not os.path.exists(f'./bot_config/guilds/guild{ctx.guild.id}.json'):
            with open(f'./bot_config/guilds/guild{ctx.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile, indent=4)

        with open(f'./bot_config/guilds/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)

        data['welcome_channel'] = channel_id

        with open(f'./bot_config/guilds/guild{ctx.guild.id}.json', 'w') as jsonFile:
            json.dump(data, jsonFile, indent=3)

        await ctx.send(f'Welcome channel set to {channel.mention} successfully.')

    @commands.command(name='setmemberrole', description='Used to set the role which is given to every member upon '
                                                        'joining. '
                                                        'Check description of `setup` command for more info.')
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def set_member_role(self, ctx, role: discord.Role):
        if not os.path.exists(f'./bot_config/guilds/guild{ctx.guild.id}.json'):
            with open(f'./bot_config/guilds/guild{ctx.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile, indent=4)

        with open(f'./bot_config/guilds/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)

        data['member_role'] = role.id

        with open(f'./bot_config/guilds/guild{ctx.guild.id}.json', 'w') as jsonFile:
            json.dump(data, jsonFile, indent=3)

        await ctx.send(f'Member role set to **{role.name}** successfully.')

def setup(bot):
    bot.add_cog(Config(bot))
