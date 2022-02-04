from discord.ext import commands
from DiscordBot.Embeds.ErrorEmbeds.error_embed import error_embed
from DiscordBot.Embeds.OtherEmbeds.top_teams_embed import top_teams_embed
from DiscordBot.constants import error_messages
from DiscordBot.validators import validateTopTeamsNumber


class TopTeamsCommand(commands.Cog):
    def __init__(self, bot, scraper):
        self.bot = bot
        self.scraper = scraper

    @commands.command(name="top_teams",
             help="Shows HLTV's Top 25 Teams. You can also specify number of teams you want to see as a number (Between 1 and 25).")
    async def top_teams(self, ctx, number: int = 25):
        validateTopTeamsNumber(number)
        teams = self.scraper.getTopTeams()
        await ctx.send(embed=top_teams_embed(teams[:number], ctx.author.display_name, ctx.author.avatar_url))

    @top_teams.error
    async def top_teams_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            message = error_messages["number_param"]
        elif isinstance(error, commands.CommandInvokeError) and error.original is not None:
            message = error.original
        else:
            message = error_messages["general"]
        await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


def setup(bot):
    bot.add_cog(TopTeamsCommand(bot, bot.scraper))