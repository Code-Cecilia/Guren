from discord.ext import commands, tasks
import topgg

class TopGG(commands.Cog):

    def __init__(self, bot):
        self.topggtoken = ""
        self.bot = bot
        self.bot.topggpy = topgg.DBLClient(self.bot, self.topggtoken)

    @tasks.loop(minutes=60)
    async def update_stats(self):
        try:
            await self.bot.topggpy.post_guild_count()
            print("Updated bot server count in top.gg")
        except Exception as e:
            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

    @commands.Cog.listener()
    async def on_ready(self):
        TopGG.update_stats.start(self)


def setup(bot):
    bot.add_cog(TopGG(bot))