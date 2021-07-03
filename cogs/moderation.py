import asyncio
import datetime
import json
import re
from copy import deepcopy

import discord
from discord import User
from discord.ext import commands, tasks
from dateutil.relativedelta import relativedelta
from discord.utils import get

from utils.util import Pag

import utils.json_loader
from utils import default, permissions
from dateutil.relativedelta import relativedelta

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(
                    f"{value} is an invalid time key! h|m|s|d are valid arguments"
                )
            except ValueError:
                raise commands.BadArgument(f"{key} is not a number!")
        return round(time)


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
    

class Moderation(commands.Cog):
    """Various Moderation Commands."""
    def __init__(self, bot):
        self.bot = bot
        self.mute_task = self.check_current_mutes.start()

    def cog_unload(self):
        self.mute_task.cancel()

    @tasks.loop(minutes=5)
    async def check_current_mutes(self):
        guild = self.bot.get_guild
        currentTime = datetime.datetime.now()
        mutes = deepcopy(self.bot.muted_users)
        for key, value in mutes.items():
            if value['muteDuration'] is None:
                continue
        
            unmuteTime = value['mutedAt'] + relativedelta(seconds=value['muteDuration'])

            if currentTime >= unmuteTime:
                guild = self.bot.get_guild(value['guildId'])
                member = guild.get_member(value['_id'])

                role = discord.utils.get(guild.roles, name="Muted")
                if role in member.roles:
                    await member.remove_roles(role)
                    print(f"Unmuted: {member.display.name}")

                await self.bot.mutes.delete(member.id)
                try:
                    self.bot.muted_users.pop(member.id)
                except KeyError:
                    pass
    
    @check_current_mutes.before_loop
    async def before_check_current_mutes(self):
        await self.bot.wait_until_ready()

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
            await ctx.send("Is that a person?")
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.name}, you don't have permission to use this command.")    

            raise error

    @commands.command(
        name='mute',
        description="Mutes a given user for x time!",
        ussage='<user> [time]'
    )
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, time: TimeConverter=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            await ctx.send("No muted role was found! Please create one called `Muted`")
            return

        try:
            if self.bot.muted_users[member.id]:
                await ctx.send("This user is already muted")
                return
        except KeyError:
            pass

        data = {
            '_id': member.id,
            'mutedAt': datetime.datetime.now(),
            'muteDuration': time or None,
            'mutedBy': ctx.author.id,
            'guildId': ctx.guild.id,
        }
        await self.bot.mutes.upsert(data)
        self.bot.muted_users[member.id] = data

        await member.add_roles(role)

        if not time:
            await ctx.send(f"Muted {member.display_name}")
        else:
            minutes, seconds = divmod(time, 60)
            hours, minutes = divmod(minutes, 60)
            if int(hours):
                await ctx.send(
                    f"Muted {member.display_name} for {hours} hours, {minutes} minutes and {seconds} seconds"
                )
            elif int(minutes):
                await ctx.send(
                    f"Muted {member.display_name} for {minutes} minutes and {seconds} seconds"
                )
            elif int(seconds):
                await ctx.send(f"Muted {member.display_name} for {seconds} seconds")

        if time and time < 300:
            await asyncio.sleep(time)

            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f"Unmuted `{member.display_name}`")

            await self.bot.mutes.delete(member.id)
            try:
                self.bot.muted_users.pop(member.id)
            except KeyError:
                pass

    @commands.command(
        name='unmute',
        description="Unmuted a member!",
        usage='<user>'
    )
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            await ctx.send("No muted role was found! Please create one called `Muted`")
            return

        await self.bot.mutes.delete(member.id)
        try:
            self.bot.muted_users.pop(member.id)
        except KeyError:
            pass

        if role not in member.roles:
            await ctx.send("This member is not muted.")
            return

        await member.remove_roles(role)
        await ctx.send(f"Unmuted `{member}`")


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
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason):
        """warns an user. ID, Mention or name."""
        if member.id in [ctx.author.id, self.bot.user.id]:
            return await ctx.send("You cannot warn yourself or the bot!")
        
        current_warn_count = len(
            await self.bot.warns.find_many_by_custom(
                {
                    "user_id": member.id,
                    "guild_id": member.guild.id
                }
            )
        ) + 1
        
        warn_filter = {"user_id": member.id, "guild_id": member.guild.id, "number": current_warn_count}
        warn_data = {"reason": reason, "timestamp": ctx.message.created_at, "warned_by": ctx.author.id}
        
        await self.bot.warns.upsert_custom(warn_filter, warn_data)
        
        embed = discord.Embed(
            title="You are being warned:",
            description=f"__**Reason**__:\n{reason}",
            colour=discord.Colour.red(),
            timestamp=ctx.message.created_at
        )
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.set_footer(text=f"Warn: {current_warn_count}")
        
        try:
            await member.send(embed=embed)
            await ctx.send("Warned that user in dm's")
        except discord.HTTPException:
            await ctx.send(member.mention, embed=embed)
            
    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def warns(self, ctx, member: discord.Member):
        """Shows all warnings for a specified user. ID, Mention or Name"""
        warn_filter = {"user_id": member.id, "guild_id": member.guild.id}
        warns = await self.bot.warns.find_many_by_custom(warn_filter)
        
        if not bool(warns):
            return await ctx.send(f"Couldn't find any warns for: `{member.display_name}`")
        
        warns = sorted(warns, key=lambda x: x["number"])
        
        pages = []
        for warn in warns:
            description = f"""
            Warn Number: `{warn['number']}`
            Warn Reason: `{warn['reason']}`
            Warned By: <@{warn['warned_by']}>
            Warn Number: {warn['timestamp'].strftime("%I:%M %p %B %d, %Y")}
            """
            pages.append(description)
        
        await Pag(
            title=f"Warns for `{member.display_name}`",
            colour=0xCE2029,
            entries=pages,
            length=1
        ).start(ctx)

def setup(bot):
    bot.add_cog(Moderation(bot))
