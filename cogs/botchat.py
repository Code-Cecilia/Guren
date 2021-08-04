import os
import json
import discord
from discord.ext import commands
from prsaw import RandomStuff

rs = RandomStuff(async_mode=True, api_key="")


class BotChat(commands.Cog, description='A Cog to... chat with the bot, i guess?\n'
                                        'Uses the __[RSA](https://docs.pgamerx.com/version-4/ai-response)__ API.\n'
                                        'Have fun!'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setbotchatchannel", description="Sets the channel for botchat")
    @commands.has_permissions(administrator=True)
    async def set_botchat_channel(self, ctx, channel: discord.TextChannel):
        channel_id = channel.id
        # create file if not exists
        if not os.path.exists(f'bot_config/guilds/guild{ctx.guild.id}.json'):
            with open(f'bot_config/guilds/guild{ctx.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile)

        with open(f'bot_config/guilds/guild{ctx.guild.id}.json', 'r') as jsonFile:
            data = json.load(jsonFile)
        data['botchat_channel'] = channel_id

        with open(f'bot_config/guilds/guild{ctx.guild.id}.json', 'w') as jsonFile:
            json.dump(data, jsonFile, indent=4)

        await ctx.send(f"Set botchat channel as {channel} succesfully!")

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return

        # create file if not exists
        if not os.path.exists(f'bot_config/guilds/guild{message.guild.id}.json'):
            with open(f'bot_config/guild{message.guild.id}.json', 'w') as jsonFile:
                json.dump({}, jsonFile)

        with open(f'bot_config/guilds/guild{message.guild.id}.json') as jsonFIle:
            data = json.load(jsonFIle)
            if data.get('botchat_channel') is not None:
                botchat_channel_id = int(data.get('botchat_channel'))
            else:
                botchat_channel_id = data.get('botchat_channel')
            botchat_channel = self.bot.get_channel(botchat_channel_id)
            if message.channel == botchat_channel:
                response = await rs.get_ai_response(message=message.content, language='english')
                response = response[0]
                response = response.get('message')
                await botchat_channel.send(response)

    @commands.command(name='chat', aliases=['botchat'], description='One-time chat command.')
    async def one_time_chat(self, ctx, *, message):
        # returns a list
        response = await rs.get_ai_response(message=message.content, language='english')
        response = response[0]  # getting the first entry, which is a dict
        # getting the message, which is inside the dict
        response = response.get('message')
        await ctx.send(response)  # sending the response


def setup(bot):
    bot.add_cog(BotChat(bot))
