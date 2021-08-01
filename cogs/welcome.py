from discord.ext import commands
from discord.utils import get
import json
import os

with open('bot_config/config.json', 'r') as detailsFile:
    details_data = json.load(detailsFile)
    main_prefix = details_data.get('prefix')


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        owner = guild.owner
        try:
            await owner.send(f"Hello, I am {self.bot.user.name}! I was invited to {guild.name} just now.\n"
                             f"My prefix `{main_prefix}`, and "
                             f"Do `{main_prefix}help to find out more about me`.\n")
                             
        except:
            print('couldn\'t send message to owner')
        if not os.path.exists(f'bot_config/guilds/guild{guild.id}.json'):
            with open(f'bot_config/guilds/guild{guild.id}.json', 'a+') as createFile:
                json.dump({}, createFile, indent=4)

        with open('./bot_config/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = ['bm-', 'Bm-']

        with open('./bot_config/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        owner = guild.owner
        try:
            await owner.send(f"Thanks for having me in: {guild.name}.\n"
                             f"Your server's config files will be deleted, along with the mute files, and custom prefix.")
        except:
            print(f'couldn\'t send message to owner of {guild.owner}')
        if os.path.exists(f'bot_config/guilds/guild{guild.id}.json'):
            os.remove(f'./bot_config/guilds/guild{guild.id}.json')

        if os.path.exists(f'./bot_config/mute_files/guild{guild.id}.json'):
            os.remove(f'./bot_config/mute_files/guild{guild.id}.json')

        with open('bot_config/prefixes.json', 'r') as prefixFile:
            data = json.load(prefixFile)
        if str(guild.id) in data.keys():
            data.pop(str(guild.id))

        with open('prefixes.json', 'w') as prefixFile:
            json.dump(data, prefixFile)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open(f'./bot_config/guilds/guild{member.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)
            welcome_channel_id = dict(data).get('welcome_channel')
            member_role_id = data.get('member_role')
        welcome_channel = self.bot.get_channel(id=int(welcome_channel_id))
        await welcome_channel.send(f'{member.mention} has joined **{member.guild.name}**! Say hi!')
        if not member.bot:
            # add the member role
            await member.add_roles(get(member.guild.roles, id=int(member_role_id)))
        else:
            # doesnt add the member role
            await welcome_channel.send('Oh, it\'s a bot')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member == self.bot.user:
            return
        with open(f'./bot_config/guilds/guild{member.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)
            welcome_channel_id = dict(data).get('welcome_channel')
        welcome_channel = self.bot.get_channel(id=int(welcome_channel_id))
        await welcome_channel.send(f'{member.mention} has left **{member.guild.name}**. Until Next time!')
        if member.bot:
            await welcome_channel.send('It\'s a bot. Oh, well...')


def setup(bot):
    bot.add_cog(Welcome(bot))