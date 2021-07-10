from discord.ext import commands
from discordTogether import DiscordTogether


class Activities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.togetherControl = DiscordTogether(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(
        description=f"Currently Only supports youtube.\nStarts a youtube together activity, "
                    f"must be on a voice channel!\n**Usage:** g$start"
        )
    async def start(self, ctx):
        link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
        await ctx.send(f"Click the blue link!\n{link}")


def setup(client):
    client.add_cog(Activities(client))
