import discord
from discord.ext import commands

class Owner(commands.Cog):
    """Owner only commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog):
        """Reloads a module"""
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"`{cog}` was reloaded.")
        except Exception as e:
            print(f"{cog} can not be loaded.")
            raise e    

    @reload.error
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("What should i reload?")
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"{ctx.author.name}, you don't have permission to use this command.")    

            raise error

    @commands.command()
    @commands.is_owner()
    async def pp(self, ctx):
        """:flushed:"""
        await ctx.send(f"My master, `Yuichiro#0001` has a pp with a length of 69CM, **8=====================================================================D**") 


def setup(bot):
    bot.add_cog(Owner(bot))
