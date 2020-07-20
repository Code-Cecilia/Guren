import asyncio
import datetime
import json

import discord
from discord import User
from discord.ext import commands
from discord.utils import get

import utils.json_loader
from utils import default, permissions


class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
        else:
            return m.id


class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = argument

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(f'reason is too long ({len(argument)}/{reason_max})')
        return ret

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

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def ban(self, ctx, member: MemberID, *, reason: str = None):
        """ Bans a user from the current server. """
        m = ctx.guild.get_member(member)
        if m is not None and await permissions.check_priv(ctx, m):
            return

        try:
            await ctx.guild.ban(discord.Object(id=member), reason=default.responsible(ctx.author, reason))
            await ctx.send(default.actionmessage("banned"))
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @commands.max_concurrency(1, per=commands.BucketType.user)
    @permissions.has_permissions(ban_members=True)
    async def massban(self, ctx, reason: ActionReason, *members: MemberID):
        """ Mass bans multiple members from the server. """
        try:
            for member_id in members:
                await ctx.guild.ban(discord.Object(id=member_id), reason=default.responsible(ctx.author, reason))
            await ctx.send(default.actionmessage("massbanned", mass=True))
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def unban(self, ctx, member: MemberID, *, reason: str = None):
        """ Unbans a user from the current server. """
        try:
            await ctx.guild.unban(discord.Object(id=member), reason=default.responsible(ctx.author, reason))
            await ctx.send(default.actionmessage("unbanned"))
        except Exception as e:
            await ctx.send(e)

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
        roles = [role for role in member.roles]
        guild_ID = ctx.guild.id
        data = utils.json_loader.read_json("server_config")
        modlogs = self.bot.get_channel(data[str(guild_ID)]["mod-logID"])

        embed = discord.Embed(title=f"`{member}` was kicked from the server", color=member.color, timestamp=datetime.datetime.utcnow(), description=f"**Moderator:** {ctx.author}")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.add_field(name="Their roles:", value=" ".join([role.mention for role in roles]))
        embed.set_footer(text=f"UUID: {member.id}")
        await modlogs.send(embed=embed)



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
        await ctx.send("Command disabled until its fixed.")


    @commands.command()
    async def unmute(self, ctx, user: Redeemed):
        """Unmutes a muted user"""  
        await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
        await ctx.send(f"{user.mention} has been unmuted")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def tempmute(self, ctx, member: discord.Member, time=0, reason=None):
        guild_ID = ctx.guild.id
        data = utils.json_loader.read_json("server_config")
        modlogs = self.bot.get_channel(data[str(guild_ID)]["mod-logID"])
        
        if not member or time == 0 or time == str:
            await ctx.channel.send(embed=commanderror)
            return
        elif reason == None:
            reason = "No Reason Provided"

        muteRole = discord.utils.get(ctx.guild.id, name="Muted")
        await member.add_roles(muteRole)
        tempMuteEmbed = discord.Embed(colour=embedcolour, description=f"**Reason:** {reason}")
        tempMuteEmbed.set_author(name=f"{member} Has Been Muted", icon_url=f"{member.avatar_url}")
        tempMuteEmbed.set_footer(text=embedfooter)

        await ctx.channel.send(embed=tempMuteEmbed)

        tempMuteModLogEmbed = discord.Embed(color=embedcolour)
        tempMuteModLogEmbed.set_author(name=f"[MUTE] {member}", icon_url=f"{member.avatar_url}")
        tempMuteModLogEmbed.add_field(name="User", value=f"{member.mention}")
        tempMuteModLogEmbed.add_field(name="Moderator", value=f"{ctx.message.author}")
        tempMuteModLogEmbed.add_field(name="Reason", value=f"{reason}")
        tempMuteModLogEmbed.add_field(name="Duration", value=f"{str(time)}")
        tempMuteModLogEmbed.set_footer(text=embedfooter)
        await modlogs.send(embed=tempMuteModLogEmbed)

        tempMuteDM = discord.Embed(color=embedcolour, title="Mute Notification", description=f"You Were Muted In **{ctx.guild.name}**")
        tempMuteDM.set_footer(text=embedfooter)
        tempMuteDM.add_field(name="Reason", value=f"{reason}")
        tempMuteDM.add_field(name="Duration", value=f"{time}")

        userToDM = client.get_user(member.id)
        await userToDM.send(embed=tempMuteDM)

        await asyncio.sleep(time)
        await member.remove_roles(muteRole)

        unMuteModLogEmbed = discord.Embed(color=embedcolour)
        unMuteModLogEmbed.set_author(name=f"[UNMUTE] {member}", icon_url=f"{member.avatar_url}")
        unMuteModLogEmbed.add_field(name="User", value=f"{member.mention}")
        unMuteModLogEmbed.set_footer(text=embedfooter)
        await modlogs.send(embed=unMuteModLogEmbed)

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
