import asyncio
import datetime
import json

import discord
from discord import User
from discord.ext import commands
from discord.utils import get


class Sinner(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)
        permission = argument.guild_permissions.manage_messages 
        if not permission:
            return argument 
        else:
            raise commands.BadArgument("You cannot punish other staff members") 


class Redeemed(commands.Converter):
    async def convert(self, ctx, argument):
        argument = await commands.MemberConverter().convert(ctx, argument)
        muted = discord.utils.get(ctx.guild.roles, name="Muted") 
        if muted in argument.roles:
            return argument
        else:
            raise commands.BadArgument("The user was not muted.") 
            

async def mute(ctx, user, reason="No reason"):
    role = discord.utils.get(ctx.guild.roles, name="Muted")  
    if not role: 
        try: 
            muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
            for channel in ctx.guild.channels: 
                await channel.set_permissions(muted, send_messages=False,
                                              read_message_history=False,
                                              read_messages=False)
        except discord.Forbidden:
            return await ctx.send("I have no permissions to make a muted role")
        await user.add_roles(muted) 
        await ctx.send(f"{user.mention} has been muted for {reason}")
    else:
        await user.add_roles(role) 
        await ctx.send(f"{user.mention} has been muted for {reason}")
        channel = ctx.bot.get_channel(718865797006753892)
        await channel.send(f"{user.mention}, welcome to the bad kids club.")

class Moderation(commands.Cog):
    """Moderation Commands"""
    def __init__(self, bot):
        self.bot = bot

        with open(r'/root/bots/Guren Beta/Guren/bot_config/reports.json', 'r') as f:
            try:
                self.report = json.load(f)
            except ValueError:
                self.report = {}
                self.report["users"] = []
    async def report(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(r'/root/bots/Guren Beta/Guren/bot_config/reports.json', 'w') as f:
                f.write(json.dumps(self.report))

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        """Bans someone"""
        try: 
            await member.ban(reason=reason)
        except discord.Forbidden:
            await ctx.send(f"It looks like i dont have the permission `BAN_MEMBERS` to do this. Please check my permissions and try running the command again.")    
        else:
            embed = discord.Embed(title=f"`{ctx.author}` banned {member}", colour=member.color, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="● Details:", value=f" - Reason: {reason}")
            embed.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"{ctx.author.top_role.name} ")
            await ctx.send(embed=embed)
        print(ctx.author.name, 'used the command ban')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member, *, reason="No reason"):
        print("unbanned")
        try:
            member =  await self.bot.fetch_user(int(member))
            await ctx.guild.unban(member, reason=reason)
        except discord.Forbidden:
            await ctx.send(f"It looks like i dont have the permission `BAN_MEMBERS` to do this. Please check my permissions and try running the command again.")
        else:
            await ctx.send(f"`{member}` was unbanned by **{ctx.author.name}**.")
        print(ctx.author.name, 'used the command unban')

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        """Kicks someone"""
        try:
            await member.kick(reason=reason)
        except discord.Forbidden:    
            await ctx.send(f"It looks like i dont have the permission `KICK_MEMBERS` to do this. Please check my permissions and try running the command again.")
        else:
            embed = discord.Embed(title=f"`{ctx.author}` kicked {member}", colour=member.color, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="● Details:", value=f" - Reason: {reason}")
            embed.set_footer(icon_url=f"{ctx.author.avatar_url}", text=f"{ctx.author.top_role.name} ")
            await ctx.send(embed=embed)
        print(ctx.author.name, 'used the command kick')


    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """Clears messages."""
        channel = ctx.channel
        try:
            await channel.purge(limit=amount+1)
        except discord.Forbidden:
            await ctx.send(f"It looks like i dont have the permission `MANAGE_MESSAGES` to do this. Please check my permissions and try running the command again.")
        else:
            await ctx.send(f"{amount} messages deleted.")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to specify an amount of messages, i can't purge air...")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Give me a valid number.")
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.name}, you don't have permission to use this command.")    

            raise error        

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to tell me who to kick.")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Is that a person?")
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.name}, you don't have permission to use this command.")        

            raise error     


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to tell me who to ban.")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Is that a person?.")
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.name}, you don't have permission to use this command.")    

            raise error

    @commands.command()
    async def mute(self, ctx, user: Sinner, reason=None):
        """Mutes a user."""
        mute_time = int  
        await mute(ctx, user, reason or "treason")
        await asyncio.sleep(mute_time)
        await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        await ctx.send(f"{user.mention} has been unmuted")

    @commands.command()
    async def unmute(self, ctx, user: Redeemed):
        """Unmutes a muted user"""  
        await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        await ctx.send(f"{user.mention} has been unmuted")


    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to tell me who do you want to mute.")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Is that a person?")
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.name}, you don't have permissions to use this command.")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to tell me who do you want to unmute.")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Is that a person?")
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.name}, you don't have permissions to use this command.")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to tell me who do you want to unban.")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Is that a person?")
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.name}, you don't have permissions to use this command.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def warn(self, ctx, user: discord.User, *reason:str):
        if not reason:
            await ctx.send("Provide a reason.")
        reason = ' '.join(reason)
        for current_user in self.report["users"]:
            if current_user['name'] == user.name:
                current_user['reasons'].append(reason)
            else:
                self.report["users"].append({
                    'Name': user.name,
                    'reasons': [reason,]
                })
            await ctx.send(f"User `{user}` has been warned for `{reason}`.")

    @commands.command(aliases=['warns'])
    @commands.has_permissions(ban_members=True)
    async def warnings(self, ctx, user: discord.User):
        for current_user in self.report["users"]:
            if user.name == current_user['name']:
                embed = discord.Embed(title=f"Warnings for {user}", color=user.color, timestamp=datetime.datetime.utcnow())
                embed.add_field(name=f"This user has been warned {len(current_user['reasons'])} times.", value=f"{' '.join(current_user['reasons'])}",)
                embed.set_footer(text=f"UUID: {user.id}")
                await ctx.send(embed=embed)
                           
def setup(bot):
    bot.add_cog(Moderation(bot))
