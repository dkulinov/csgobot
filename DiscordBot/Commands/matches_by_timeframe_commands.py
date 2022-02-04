import math

from discord.ext import commands
from discord.ext.commands import CommandInvokeError

from Commons.Types.Match.CurrentMatch import CurrentMatch
from Commons.Types.Match.FutureMatch import FutureMatch
from Commons.Types.Match.PastMatch import PastMatch
from DiscordBot.Embeds.ErrorEmbeds.error_embed import error_embed
from DiscordBot.Embeds.MatchesEmbeds.live_matches_embed import live_matches_embed
from DiscordBot.Embeds.MatchesEmbeds.recent_matches_embed import recent_matches_embed
from DiscordBot.Embeds.MatchesEmbeds.upcoming_matches_embed import upcoming_matches_embed
from DiscordBot.constants import error_messages
from DiscordBot.helpers import mapToMatchType
from DiscordBot.validators import validateNumberIsPositive
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers


class MatchesByTimeframeCommands(commands.Cog):
    def __init__(self, bot, scraper, db):
        self.bot = bot
        self.scraper = scraper
        self.db = db

    @commands.command(name="recent",
                      help=f'Shows recent matches. You can also provide number of matches (between 1-25) and the offset (non-negative number).')
    async def recent_matches(self, ctx, number=10, offset=0):
        recent_matches: [PastMatch] = self.scraper.getAllMatches(MatchContainers.past, numberPast=number, offset=offset)
        await ctx.send(
            embed=recent_matches_embed(f'Recent matches ({offset + 1}-{offset + len(recent_matches)}):',
                                       recent_matches[:number], offset, ctx.author.display_name, ctx.author.avatar_url))

    @recent_matches.error
    async def recent_matches_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            message = error_messages["number_param"]
        elif isinstance(error, CommandInvokeError) and isinstance(error.original, ValueError):
            message = error.original
        else:
            message = error_messages["general"]
        await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))

    @commands.command(name="live",
                      help='Shows live matches. You can also provide a filter (top_tier or lan). If not provided, will return all matches.')
    async def live_matches(self, ctx, match_filter="none"):
        match_type = mapToMatchType(match_filter)
        live_matches: [CurrentMatch] = self.scraper.getAllMatches(MatchContainers.present, predefinedFilter=match_type)
        max_fields_per_embed = 25
        num_embeds_required = math.ceil(len(live_matches) / max_fields_per_embed)
        if num_embeds_required < 1:
            await ctx.send(
                embed=error_embed(f'There are currently no live {match_type.value} matches.', ctx.author.display_name,
                                  ctx.author.avatar_url))
        for batch in range(num_embeds_required):
            start = batch * max_fields_per_embed
            end = start + max_fields_per_embed
            batch_of_matches = live_matches[start:end]
            await ctx.send(
                embed=live_matches_embed(batch_of_matches, match_type, ctx.author.display_name, ctx.author.avatar_url))

    @live_matches.error
    async def live_matches_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            message = "Filter has to be either top_tier or lan."
        elif isinstance(error, CommandInvokeError) and isinstance(error.original, TypeError):
            message = "Filter has to be either top_tier or lan."
        elif isinstance(error, CommandInvokeError) and isinstance(error.original, ValueError):
            message = error.original
        else:
            message = error_messages["general"]
        await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))

    @commands.command(name="upcoming",
                      help='Shows upcoming matches. You can also provide a filter (top_tier or lan). If not provided, will return all matches. You can also provide a number of matches to get.')
    async def upcoming_matches(self, ctx, match_filter="none", number=100):
        match_type = mapToMatchType(match_filter)
        validateNumberIsPositive(number)
        timezone = await self.db.get_user_timezone_or_default(ctx.author.id)
        future_matches: [FutureMatch] = self.scraper.getAllMatches(MatchContainers.future, predefinedFilter=match_type)[
                                        :number]
        max_fields_per_embed = 25
        num_embeds_required = math.ceil(len(future_matches) / max_fields_per_embed)
        if num_embeds_required < 1:
            await ctx.send(
                embed=error_embed(f'There are currently no upcoming {match_type.value} matches.',
                                  ctx.author.display_name,
                                  ctx.author.avatar_url))
        for batch in range(num_embeds_required):
            start = batch * max_fields_per_embed
            end = start + max_fields_per_embed
            batch_of_matches = future_matches[start:end]
            await ctx.send(
                embed=upcoming_matches_embed("Upcoming matches:", batch_of_matches, match_type, ctx.author.display_name,
                                             ctx.author.avatar_url, timezone))

    @upcoming_matches.error
    async def upcoming_matches_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            message = error
        elif isinstance(error, CommandInvokeError) and isinstance(error.original, TypeError):
            message = "Filter has to be either top_tier or lan."
        elif isinstance(error, CommandInvokeError) and isinstance(error.original, ValueError):
            message = error.original
        else:
            message = error_messages["general"]
        await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


def setup(bot):
    bot.add_cog(MatchesByTimeframeCommands(bot, bot.scraper, bot.db))
