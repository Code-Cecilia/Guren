import discord
from discord.ext import commands
import json
import asyncio


class Levels(commands.Cog):
    """A clumsy leveling system"""

    def __init__(self, bot):
        self.bot = bot

        self.bot.loop.create_task(self.save_users())

        with open(r"/home/bot/python/Guren/bot_config/users.json", "r") as f:
            self.users = json.load(f)

    async def save_users(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(r"/home/bot/python/Guren/bot_config/users.json", "w") as f:
                f.write(json.dumps(self.users, indent=4))

            await asyncio.sleep(5)

    def lvl_up(self, author_id):
        cur_xp = self.users[author_id]['exp']
        cur_lvl = self.users[author_id]['level']

        if cur_xp >= round((600 * (cur_lvl ** 3)) / 5):
            self.users[author_id]['level'] += 1
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message, guild: discord.Guild = None):
        guild = guild if not guild else guild
        if message.author.bot:
            return
        if message.channel.id in [556116525128613888, 656880750142160926, 696804345311657995, 612675164227764254,
                                  676698027028905999, 694525461639725070, 694525883129528410]:
            return
        if message.channel.category.id in [556117715077693458, 610628703789252627, 718897154835349534]:
            return
        if message.guild.id in [463737113091899412, 698244553718890537]:
            return

        author_id = str(message.author)

        if not author_id in self.users:
            self.users[author_id] = {}
            self.users[author_id]['level'] = 0
            self.users[author_id]['exp'] = 0

        self.users[author_id]['exp'] += 1

        if self.lvl_up(author_id):
            embed = discord.Embed(color=message.author.color, timestamp=message.created_at)

            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_author(name=f"LEVELUP",
                             icon_url="https://cdn.discordapp.com/attachments/717128065653932053/718842463250284605/ezgif.com-resize_1.gif")

            embed.add_field(name=f"{message.author} ranked up to", value=f"Level: `{self.users[author_id]['level']}`")

            embed.set_footer(text=f"Leveling system by Guren Ichinose#6762",
                             icon_url="https://cdn.discordapp.com/avatars/669973381067571240/350b378596401f453fb4d5bd3411a682.webp?size=1024")
            await message.channel.send(embed=embed)

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        """Check your Level"""
        member = ctx.author if not member else member
        member_id = str(member.id)

        if not member_id in self.users:
            await ctx.send("Member doesn't have a level")
        else:
            embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)

            embed.set_author(name=f"{member.name}'s status ")
            embed.set_thumbnail(url=ctx.author.avatar_url)
            embed.add_field(name="Level:", value=self.users[member_id]['level'])
            embed.add_field(name="Xp:", value=self.users[member_id]['exp'])
            embed.add_field(name="Rank:", value="Feature coming soon.")
            embed.set_footer(text=f"Leveling system by Guren Ichinose#6762",
                             icon_url="https://cdn.discordapp.com/avatars/669973381067571240/350b378596401f453fb4d5bd3411a682.webp?size=1024")

            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def leaderboard(self, ctx):
        """Displays the top 5 users"""
        leaderboard = sorted(self.users, key=lambda x: self.users[x]["exp"], reverse=True)[:5]
        level = sorted(self.users, key=lambda x: self.users[x]["level"], reverse=True)[:5]
        await ctx.send(f"\n".join(leaderboard))
        await ctx.send(f"\n".join(level))


def setup(bot):
    bot.add_cog(Levels(bot))
