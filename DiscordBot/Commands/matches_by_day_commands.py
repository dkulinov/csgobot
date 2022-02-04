from datetime import datetime

from discord.ext import commands
from discord.ext.commands import CommandInvokeError

from Commons.Types.Match.CurrentMatch import CurrentMatch
from Commons.Types.Match.FutureMatch import FutureMatch
from Commons.Types.Match.PastMatch import PastMatch
from Commons.Types.MatchType import MatchType
from DiscordBot.Embeds.ErrorEmbeds.error_embed import error_embed
from DiscordBot.Embeds.MatchesEmbeds.live_matches_embed import live_matches_embed
from DiscordBot.Embeds.MatchesEmbeds.recent_matches_embed import recent_matches_embed
from DiscordBot.Embeds.MatchesEmbeds.upcoming_matches_embed import upcoming_matches_embed
from DiscordBot.constants import error_messages


class MatchesByDayCommands(commands.Cog):
    def __init__(self, bot, scraper, db):
        self.bot = bot
        self.scraper = scraper
        self.db = db

    @commands.command(name="by_day",
                 help='Shows matches for a day. Date should be in mm/dd/yyyy format. Can not go back more than a week in the past.')
    async def by_day(self, ctx, date):
        timezone = await self.db.get_user_timezone_or_default(ctx.author.id)
        matches = self.scraper.getMatchesByDay(date, timezone)
        if len(matches) < 1:
            await ctx.send(embed=error_embed(f"No matches on {date}", ctx.author.display_name, ctx.author.avatar_url))
            return
        past_matches = list(filter(lambda match: type(match) == PastMatch, matches))[::-1]
        live_matches = list(filter(lambda match: type(match) == CurrentMatch, matches))
        future_matches = list(filter(lambda match: type(match) == FutureMatch, matches))
        if len(past_matches) > 0:
            await ctx.send(embed=recent_matches_embed(f'Matches on {date}', past_matches, 0, ctx.author.display_name,
                                                      ctx.author.avatar_url))
        if len(live_matches) > 0:
            await ctx.send(
                embed=live_matches_embed(live_matches, MatchType.Default, ctx.author.display_name,
                                         ctx.author.avatar_url))
        if len(future_matches) > 0:
            await ctx.send(embed=upcoming_matches_embed(f'Matches on {date}', future_matches, MatchType.Default,
                                                        ctx.author.display_name, ctx.author.avatar_url, timezone))

    @by_day.error
    async def by_day_error(self, ctx, error):
        if isinstance(error, CommandInvokeError) and isinstance(error.original, ValueError):
            message = error.original
        else:
            message = error_messages["db_connection"]
        await ctx.send(
            embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))

    @commands.command(name="today", help="Shows today's matches")
    async def today(self, ctx):
        today = "/".join(
            [str(datetime.today().date().month), str(datetime.today().date().day), str(datetime.today().date().year)])
        await self.by_day(ctx, today)

    @today.error
    async def today_error(self, ctx, error):
        message = error_messages["db_connection"]
        await ctx.send(
            embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


def setup(bot):
    bot.add_cog(MatchesByDayCommands(bot, bot.scraper, bot.db))