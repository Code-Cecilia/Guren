import datetime
import discord
from discord.ext import commands

class Utilities(commands.Cog):
    """Usefull commands, mainly information commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="avatar")
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        embed = discord.Embed(title=f"{member} avatar", colour=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=f"{member.avatar_url}")
        await ctx.send(embed=embed)
        print(ctx.author.name, 'used the command avatar')


    @commands.command(name="userinfo")
    @commands.guild_only()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        roles = [role for role in member.roles]
        embed = discord.Embed(color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"User Info - {member}")
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="ID:", value=member.id)
        embed.add_field(name="Guild name:", value=member.display_name)
        embed.add_field(name="Created at:", value=member.created_at)
        embed.add_field(name="Joined at:", value=member.joined_at)
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Top Role:", value=member.top_role.mention)
        embed.add_field(name="Bot?", value=member.bot)
        await ctx.send(embed=embed)
        print(ctx.author.name, "used the command userinfo")

    @commands.command(name="serverinfo")
    @commands.guild_only()
    async def serverinfo(self, ctx, guild: discord.Guild = None, member: discord.Member = None):
        guild = ctx.guild if not guild else guild
        embed = discord.Embed(title=f"{guild.name}", colour=ctx.author.color, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="ID:", value=guild.id)
        embed.add_field(name="Server name:", value=guild.name)
        embed.add_field(name="Server Owner:", value=guild.owner.name)
        embed.add_field(name="Created at:", value=ctx.guild.created_at)
        embed.add_field(name="Role count:", value=len(guild.roles))
        embed.add_field(name="Booster Count", value=guild.premium_subscription_count)
        embed.add_field(name="Member Count", value=guild.member_count)
        embed.add_field(name="Max Emojis", value=guild.emoji_limit)
        await ctx.send(embed=embed)
        print(ctx.author.name, "used the command serverinfo")

    @commands.command()
    async def stats(self, ctx):

        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name='Bot Version:', value="1.0BETA")
        embed.add_field(name='Discord.Py Version', value=dpyVersion)
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Bot Developer:', value="<@219410026631135232>")
        embed.add_field(name="Support Server", value=f"[I live here.](https://discord.gg/8wCez2n)")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def help(self,ctx,*cog):
        """Gets all cogs and commands of mine."""
        try:
            if not cog:
                """Cog listing.  What more?"""
                halp=discord.Embed(title='Command category listing',
                                description=f'Use `gb$ *cog*` to find out more about them!', timestamp=datetime.datetime.utcnow(), color=ctx.author.color)
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

    @commands.command()
    async def permissions(self, ctx, member: discord.Member = None):
        '''Displays my current permissions'''
        permissions = ctx.channel.permissions_for(ctx.me)
        member = ctx.author if not member else member
        embed = discord.Embed(title=':customs:  Permissions', colour=member.color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name='Server', value=ctx.guild)
        embed.add_field(name='Channel', value=ctx.channel, inline=False)

        for item, valueBool in permissions:
            if valueBool == True:
                value = ':white_check_mark:'
            else:
                value = ':x:'
            embed.add_field(name=item, value=value)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=embed)            
            
def setup(bot):
    bot.remove_command('Help')
    bot.add_cog(Utilities(bot))
