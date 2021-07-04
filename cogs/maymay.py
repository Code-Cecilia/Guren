
import discord
from discord.ext import commands
import praw
import random
import datetime


reddit = praw.Reddit(client_id="nzXLSEZ7SOxHOg",
                    client_secret="8q1JBZE5_Mo7eXogVq6C2Yz6vNA",
                    redirect_uri="http://localhost:8080",
                    user_agent="discordapipythonlib:com.GURENBOT:v1.0.0 (by /u/yuichiro__)",
                    username="GurenBOT")


class Maymay(commands.Cog):
    """Big boy."""
    def __init__ (self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
 
    @commands.command()
    async def meme(self, ctx, member: discord.Member = None):
        """Sends a random meme"""
        member = ctx.author if not member else member

        memes_submissions = reddit.subreddit('memes').hot()
        post_to_pick = random.randint(1, 50)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        embed = discord.Embed(color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=f"{submission.url}")

        await ctx.send(embed=embed)
        print(f"{ctx.author} used the command meme.")

    @commands.command()
    async def penis(self, ctx, *, question = None, member: discord.Member = None):
        """100% legit pp size machine"""
        question = ctx.author if not question else question
        member = ctx.author if not member else member
        responses = [
            '8D', '8=D', '8=D', '8==D', '8===D', '8===D', '8=====D', '8====D',
            '8=====D', '8=====D', '8====D', '8====D',
            '8======================D', '8====================================D'
        ]
        embed = discord.Embed(title = "pp size machine", color = member.color, description=f'{question} pp size:\n{random.choice(responses)}', timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def ask(self, ctx, *, question = None, member: discord.Member = None):
        """Ask me anything"""
        question = ctx.author if not question else question
        member = ctx.author if not member else member
        responses = [
            'Definitely bruh', 'Ofcourse mate', 'Without a doubt my man',
            'Yeah definitely', 'As I see it, yes', 'Most likely', 'Outlook good',
            'Yeah', 'Signs point to yes', 'Reply hazy, try again bruh',
            'Ask again later', 'Better not tell you bruh sorry', 'Cant predict rn',
            'Concentrate and ***ask again***', 'Dont count on it',
            'My reply is no', 'My sources say no', 'Outlook aint so good my guy',
            'Very doubtful', 'HELL NAH', 'are you kidding bruh'
        ]
        embed = discord.Embed(color = member.color, description=f'Question: {question}\nAnswer: {random.choice(responses)}', timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def howgay(self, ctx, *, question = None, member: discord.Member = None):
        """I tell you how gay you are"""
        if ctx.author.id == 436174748939190274:
            await ctx.send("You are `200%` gay :heart:")
            return
        question = ctx.author if not question else question
        member = ctx.author if not member else member
        responses = [
            '1%', '9%', '17%', '26%', '35%', '0%', '40%', '53%', '69%', '73%',
            '88%', '95%', '100%', '200%'
        ]
        embed = discord.Embed(color = member.color, description=f'{question} is {random.choice(responses)} gay', timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def howsimp(self, ctx, *, question = None, member: discord.Member = None):
        """I tell you how simp you are"""
        question = ctx.author if not question else question
        member = ctx.author if not member else member
        if member.id == 219410026631135232:
            await ctx.send("My lord is not a simp. :triumph:")
            return
        responses = [
            '1%', '9%', '17%', '26%', '35%', '0%', '40%', '53%', '69%', '73%',
            '88%', '95%', '100%', '200%'
        ]
        embed = discord.Embed(color = member.color, description=f'{question} is {random.choice(responses)} simp', timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


print(f"PRAW succesfully logged in as {reddit.user.me()}")
def setup(bot):
    bot.add_cog(Maymay(bot))
