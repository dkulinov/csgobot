from discord.ext import commands
from discord.ext.commands import CommandInvokeError, MissingRequiredArgument

from Commons.Exceptions.InvalidTeamException import InvalidTeamException
from Commons.Types.Team import HLTVTeams
from DiscordBot.Embeds.ErrorEmbeds.error_embed import error_embed
from DiscordBot.Embeds.MatchesByTeamEmbeds.future_matches_by_team_embed import future_matches_by_team_embed
from DiscordBot.Embeds.MatchesByTeamEmbeds.past_matches_by_team_embed import past_matches_by_team_embed
from DiscordBot.constants import error_messages
from HLTVScraper.HLTVConsts.MatchTime import MatchTime


class MatchesByTeamCommand(commands.Cog):
    def __init__(self, bot, scraper, db):
        self.bot = bot
        self.scraper = scraper
        self.db = db

    @commands.command(name="matches_for", help=f'Supported teams: {", ".join(list(HLTVTeams().HLTV_teams.keys()))}')
    async def matches_for(self, ctx, *, team):
        timezone = await self.db.get_user_timezone_or_default(ctx.author.id)
        past_matches_by_team = self.scraper.getMatchesByTeam(team, MatchTime.past)[::-1]
        future_matches_by_team = self.scraper.getMatchesByTeam(team, MatchTime.future)
        await ctx.send(embed=past_matches_by_team_embed(team, past_matches_by_team[:25], ctx.author.display_name,
                                                        ctx.author.avatar_url, timezone))
        await ctx.send(embed=future_matches_by_team_embed(team, future_matches_by_team[:25], ctx.author.display_name,
                                                          ctx.author.avatar_url, timezone))

    @matches_for.error
    async def matches_for_error(self, ctx, error):
        if isinstance(error, CommandInvokeError) and isinstance(error.original, InvalidTeamException):
            message = f'Please enter a supported team: {", ".join(list(HLTVTeams().HLTV_teams.keys()))}'
        elif isinstance(error, MissingRequiredArgument):
            message = f'Please provide a team'
        else:
            message = error_messages["general"]
        await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


def setup(bot):
    bot.add_cog(MatchesByTeamCommand(bot, bot.scraper, bot.db))