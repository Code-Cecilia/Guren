from discord.ext import commands

import utils.json_loader


class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def dump_gif(self, ctx):
        kiss = "kiss"
        hug = "hug"
        pet = "pet"
        rub = "rub"

        data = utils.json_loader.read_json("gifs")
        data[str(kiss, hug, pet, rub)] = {
            "kiss": None, "hug": None, "pet": None, "rub": None}
        utils.json_loader.write_json(data, "gifs")
        data = utils.json_loader.read_json("gifs")

        print("not ready.")


def setup(bot):
    bot.add_cog(Eval(bot))
