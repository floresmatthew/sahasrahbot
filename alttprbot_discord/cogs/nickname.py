from discord.ext import commands

from alttprbot.database import srlnick


class Nickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Register your Twitch name with SahasrahBot."
    )
    async def twitch(self, ctx, twitch):
        await srlnick.insert_twitch_name(ctx.author.id, twitch)

    @commands.command(
        help="List the nicknames registered with SahasrahBot."
    )
    async def getnick(self, ctx):
        nick = await srlnick.get_nickname(ctx.author.id)
        if nick:
            await ctx.reply(f"Your currently registered nickname for Twitch is `{nick[0]['twitch_name']}`")
        else:
            await ctx.reply("You currently do not have any nicknames registered with this bot.  Use the command `$twitch yournick` to do that!")


def setup(bot):
    bot.add_cog(Nickname(bot))
