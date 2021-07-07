import datetime
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext, cog_ext

class Help(commands.Cog):
    def __init__(self, bot):
        """Main help command"""
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(pass_context=True)
    async def help(self,ctx,*cog):
        """Gets all cogs and commands of mine."""
        try:
            if not cog:
                """Cog listing.  What more?"""
                halp=discord.Embed(title='Command category listing',
                                description=f'Use `g$ *cog*` to find out more about them!', timestamp=datetime.datetime.utcnow(), color=ctx.author.color)
                cogs_desc = ''
                for x in self.bot.cogs:
                    cogs_desc += ('{} - {}'.format(x,self.bot.cogs[x].__doc__)+'\n')
                halp.add_field(name='Available categories:',value=cogs_desc[0:len(cogs_desc)-1],inline=False)
                halp.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                halp.set_thumbnail(url=self.bot.user.avatar_url)
                cmds_desc = ''
                for y in self.bot.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name,y.help)+'\n')
                await ctx.message.add_reaction(emoji='✅')
                await ctx.message.channel.send('',embed=halp)
            else:
                """Helps me remind you if you pass too many args."""
                if len(cog) > 1:
                    halp = discord.Embed(title='Error!',description='That is way too many cogs!',color=ctx.author.color())
                    halp.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                    halp.set_thumbnail(url=self.bot.user.avatar_url)
                    await ctx.message.channel.send('',embed=halp)
                else:
                    """Command listing within a cog."""
                    found = False
                    for x in self.bot.cogs:
                        for y in cog:
                            if x == y:
                                halp=discord.Embed(title=cog[0]+' Command Listing',description=self.bot.cogs[cog[0]].__doc__, color=ctx.author.color)
                                for c in self.bot.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(name=c.name,value=c.help,inline=False)
                                        halp.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                                        halp.set_thumbnail(url=self.bot.user.avatar_url)
                                found = True
                    if not found:
                        """Reminds you if that cog doesn't exist."""
                        halp = discord.Embed(title='Error!',description='How do you even use "'+cog[0]+'"?',color=ctx.author.color)
                        halp.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
                        halp.set_thumbnail(url=self.bot.user.avatar_url)
                    else:
                        await ctx.message.add_reaction(emoji='✅')
                    await ctx.message.channel.send('',embed=halp)
        except:
            await ctx.send("An error happened.")

def setup(bot):
    bot.remove_command('Help')
    bot.add_cog(Help(bot))