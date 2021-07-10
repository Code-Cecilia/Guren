import discord
from discord.ext import commands
import os
import asyncio
import traceback
import utils.json_loader


class Owner(commands.Cog):
    """Owner only commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(
        name='reload', description="Reload all/one of the bots cogs!"
    )
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"cogs.{ext[:-3]}")
                            self.bot.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(
                                name=f"Reloaded: `{ext}`",
                                value='\uFEFF',
                                inline=False
                            )
                        except Exception as e:
                            embed.add_field(
                                name=f"Failed to reload: `{ext}`",
                                value=e,
                                inline=False
                            )
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            # reload the specific cog
            async with ctx.typing():
                embed = discord.Embed(
                    title="Reloading all cogs!",
                    color=0x808080,
                    timestamp=ctx.message.created_at
                )
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    # if the file does not exist
                    embed.add_field(
                        name=f"Failed to reload: `{ext}`",
                        value="This cog does not exist.",
                        inline=False
                    )

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(
                            name=f"Reloaded: `{ext}`",
                            value='\uFEFF',
                            inline=False
                        )
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(
                            name=f"Failed to reload: `{ext}`",
                            value=desired_trace,
                            inline=False
                        )
                await ctx.send(embed=embed)

    @commands.command()
    async def pp(self, ctx):
        """:flushed:"""
        if ctx.author.id == 219410026631135232:
            await ctx.send(f"My master, `Yuichiro#0001` has a pp with a length of 69CM, "
                           f"**8=====================================================================D**")
            return 0
        if ctx.author.id == 436174748939190274:
            await ctx.send("Your boyfriend `Yuichiro#0001` has a pp with a length of 69CM, "
                           "**8=====================================================================D**")
        else:
            await ctx.send("You have no permission to use this command")

    @commands.command(
        name="blacklist", description="Blacklist a user from the bot", usage="<user>"
    )
    @commands.is_owner()
    async def blacklist(self, ctx, user: discord.Member):
        if ctx.message.author.id == user.id:
            await ctx.send("Hey, you cannot blacklist yourself!")
            return

        self.bot.blacklisted_users.append(user.id)
        data = utils.json_loader.read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        utils.json_loader.write_json(data, "blacklist")
        await ctx.send(f"Hey, I have blacklisted {user.name} for you.")

    @commands.command(
        name="unblacklist",
        description="Unblacklist a user from the bot",
        usage="<user>",
    )
    @commands.is_owner()
    async def unblacklist(self, ctx, user: discord.Member):
        """
        Unblacklist someone from the bot
        """
        self.bot.blacklisted_users.remove(user.id)
        data = utils.json_loader.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        utils.json_loader.write_json(data, "blacklist")
        await ctx.send(f"Hey, I have unblacklisted {user.name} for you.")

    @commands.command(
        name="logout",
        aliases=["disconnect", "close", "stopbot"],
        description="Log the bot out of discord!",
    )
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:")
        await self.bot.logout()

    @commands.command()
    @commands.cooldown(1, 1500, commands.BucketType.user)
    @commands.is_owner()
    async def annoy(self, ctx, user: discord.Member, *, string=None):
        """Annoys a specific person"""
        if not string:
            if ctx.message.attachments:
                string = ctx.message.attachments[0].url
            else:
                return await ctx.send("Provide an attachment or message.")

        if string:
            if ctx.message.attachments:
                string = f"{string} \n{ctx.message.attachments[0].url}"
            else:
                pass

        await ctx.send("I will now annoy them for the next 25 minutes in 5 minute intervals.")

        timer = 1500
        active = True
        while active:
            timer -= 300
            try:
                await user.send(f"Congratulations :tada: You have been chosen by {str(ctx.author)}"
                                f" to be annoyed with this message every five minutes: {string}")
            except discord.Forbidden:
                return await ctx.send("It appears I have been blocked or the user has disabled DMs.")
            await asyncio.sleep(300)

            if timer == 0:
                active = False


def setup(bot):
    bot.add_cog(Owner(bot))
