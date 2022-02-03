import math
import os
from datetime import datetime

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, CommandInvokeError
from dotenv import load_dotenv

from Commons.Exceptions.InvalidTeamException import InvalidTeamException
from Commons.Types.Match.CurrentMatch import CurrentMatch
from Commons.Types.Match.FutureMatch import FutureMatch
from Commons.Types.Match.PastMatch import PastMatch
from Commons.Types.MatchType import MatchType
from Commons.Types.Team import HLTVTeams
from DiscordBot.DB.db import UserTimezoneDB
from DiscordBot.Embeds.MatchesByTeamEmbeds.future_matches_by_team_embed import future_matches_by_team_embed
from DiscordBot.Embeds.MatchesEmbeds.live_matches_embed import live_matches_embed
from DiscordBot.Embeds.OtherEmbeds.news_embed import news_embed
from DiscordBot.Embeds.MatchesByTeamEmbeds.past_matches_by_team_embed import past_matches_by_team_embed
from DiscordBot.Embeds.MatchesEmbeds.recent_matches_embed import recent_matches_embed
from DiscordBot.Embeds.OtherEmbeds.timezone_embed import timezone_embed
from DiscordBot.Embeds.OtherEmbeds.top_teams_embed import top_teams_embed
from DiscordBot.Embeds.MatchesEmbeds.upcoming_matches_embed import upcoming_matches_embed
from DiscordBot.constants import error_messages
from DiscordBot.geolocator import get_timezone_from_location
from DiscordBot.helpers import mapToMatchType
from DiscordBot.validators import validateTopTeamsNumber, validateNumberIsPositive
from HLTVScraper.HLTVConsts.MatchContainers import MatchContainers
from HLTVScraper.HLTVConsts.MatchTime import MatchTime
from HLTVScraper.Helpers.Factories.MatchFactories.CurrentMatchFactory import CurrentMatchFactory
from HLTVScraper.Helpers.Factories.MatchFactories.FutureMatchFactory import FutureMatchFactory
from HLTVScraper.Helpers.Factories.MatchFactories.MatchByTeamFactory import MatchByTeamFactory
from HLTVScraper.Helpers.Factories.MatchFactories.PastMatchFactory import PastMatchFactory
from HLTVScraper.Helpers.Factories.NewsFactory import NewsFactory
from HLTVScraper.Helpers.Factories.SeriesFactory import SeriesFactory
from HLTVScraper.Helpers.Factories.TopTeamFactory import TopTeamFactory
from HLTVScraper.Helpers.SoupChef import SoupChef
from HLTVScraper.Helpers.UrlBuilder import URLBuilder
from HLTVScraper.scraper import Scraper
from DiscordBot.Embeds.ErrorEmbeds.error_embed import error_embed

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

urlBuilder = URLBuilder()
soupChef = SoupChef(urlBuilder)
pastMatchFactory = PastMatchFactory()
currentMatchFactory = CurrentMatchFactory()
futureMatchFactory = FutureMatchFactory()
seriesFactory = SeriesFactory()
matchByTeamFactory = MatchByTeamFactory()
newsFactory = NewsFactory()
topTeamFactory = TopTeamFactory()

scraper = Scraper(urlBuilder, soupChef, pastMatchFactory, currentMatchFactory, futureMatchFactory,
                  seriesFactory, matchByTeamFactory, newsFactory, topTeamFactory)

intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
db = UserTimezoneDB()


# TODO: https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html
# TODO: https://stackoverflow.com/questions/50678419/how-to-make-multiple-files-python-bot
# https://stackoverflow.com/questions/57182398/is-it-possible-to-attach-multiple-images-in-a-embed/57191891#:~:text=Yes%20and%20no.,shown%20separately%20from%20the%20embed.

@bot.event
async def on_ready():
    await db.set_up_db()
    print("I'm ready!")


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to this Discord server! Type !help to see commands I can response to!'
    )


@bot.event
async def on_command_error(ctx, error):
    pass


@bot.command(name="top_teams",
             help="Shows HLTV's Top 25 Teams. You can also specify number of teams you want to see as a number (Between 1 and 25).")
async def top_teams(ctx, number: int = 25):
    validateTopTeamsNumber(number)
    teams = scraper.getTopTeams()
    await ctx.send(embed=top_teams_embed(teams[:number], ctx.author.display_name, ctx.author.avatar_url))


@top_teams.error
async def top_teams_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        message = error_messages["number_param"]
    elif isinstance(error, commands.CommandInvokeError) and error.original is not None:
        message = error.original
    else:
        message = error_messages["general"]
    await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


@bot.command(name="news", help="Shows HLTV's recent news.")
async def news(ctx):
    recent_news = scraper.getNews()
    await ctx.send(embed=news_embed(recent_news[:10], ctx.author.display_name, ctx.author.avatar_url))


@news.error
async def news_error(ctx, error):
    await ctx.send(embed=error_embed(error_messages["general"], ctx.author.display_name, ctx.author.avatar_url))


@bot.command(name="matches_for", help=f'Supported teams: {", ".join(list(HLTVTeams().HLTV_teams.keys()))}')
async def matches_for(ctx, *, team):
    timezone = await db.get_user_timezone_or_default(ctx.author.id)
    past_matches_by_team = scraper.getMatchesByTeam(team, MatchTime.past)[::-1]
    future_matches_by_team = scraper.getMatchesByTeam(team, MatchTime.future)
    await ctx.send(embed=past_matches_by_team_embed(team, past_matches_by_team[:25], ctx.author.display_name,
                                                    ctx.author.avatar_url, timezone))
    await ctx.send(embed=future_matches_by_team_embed(team, future_matches_by_team[:25], ctx.author.display_name,
                                                      ctx.author.avatar_url, timezone))


@matches_for.error
async def matches_for_error(ctx, error):
    if isinstance(error, CommandInvokeError) and isinstance(error.original, InvalidTeamException):
        message = f'Please enter a supported team: {", ".join(list(HLTVTeams().HLTV_teams.keys()))}'
    elif isinstance(error, MissingRequiredArgument):
        message = f'Please provide a team'
    else:
        message = error_messages["general"]
    await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


@bot.command(name="recent",
             help=f'Shows recent matches. You can also provide number of matches (between 1-25) and the offset (non-negative number).')
async def recent_matches(ctx, number=10, offset=0):
    recent_matches: [PastMatch] = scraper.getAllMatches(MatchContainers.past, numberPast=number, offset=offset)
    await ctx.send(
        embed=recent_matches_embed(f'Recent matches ({offset + 1}-{offset + len(recent_matches)}):',
                                   recent_matches[:number], offset, ctx.author.display_name, ctx.author.avatar_url))


@recent_matches.error
async def recent_matches_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        message = error_messages["number_param"]
    elif isinstance(error, CommandInvokeError) and isinstance(error.original, ValueError):
        message = error.original
    else:
        message = error_messages["general"]
    await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


@bot.command(name="live",
             help='Shows live matches. You can also provide a filter (top_tier or lan). If not provided, will return all matches.')
async def live_matches(ctx, match_filter="none"):
    match_type = mapToMatchType(match_filter)
    live_matches: [CurrentMatch] = scraper.getAllMatches(MatchContainers.present, predefinedFilter=match_type)
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
async def live_matches_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        message = "Filter has to be either top_tier or lan."
    elif isinstance(error, CommandInvokeError) and isinstance(error.original, TypeError):
        message = "Filter has to be either top_tier or lan."
    elif isinstance(error, CommandInvokeError) and isinstance(error.original, ValueError):
        message = error.original
    else:
        message = error_messages["general"]
    await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


@bot.command(name="upcoming",
             help='Shows upcoming matches. You can also provide a filter (top_tier or lan). If not provided, will return all matches. You can also provide a number of matches to get.')
async def upcoming_matches(ctx, number=100, match_filter="none"):
    match_type = mapToMatchType(match_filter)
    validateNumberIsPositive(number)
    timezone = await db.get_user_timezone_or_default(ctx.author.id)
    future_matches: [FutureMatch] = scraper.getAllMatches(MatchContainers.future, predefinedFilter=match_type)[:number]
    max_fields_per_embed = 25
    num_embeds_required = math.ceil(len(future_matches) / max_fields_per_embed)
    if num_embeds_required < 1:
        await ctx.send(
            embed=error_embed(f'There are currently no upcoming {match_type.value} matches.', ctx.author.display_name,
                              ctx.author.avatar_url))
    for batch in range(num_embeds_required):
        start = batch * max_fields_per_embed
        end = start + max_fields_per_embed
        batch_of_matches = future_matches[start:end]
        await ctx.send(
            embed=upcoming_matches_embed("Upcoming matches:", batch_of_matches, match_type, ctx.author.display_name,
                                         ctx.author.avatar_url, timezone))


@upcoming_matches.error
async def upcoming_matches_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        message = error
    elif isinstance(error, CommandInvokeError) and isinstance(error.original, TypeError):
        message = "Filter has to be either top_tier or lan."
    elif isinstance(error, CommandInvokeError) and isinstance(error.original, ValueError):
        message = error.original
    else:
        message = error_messages["general"]
    await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


@bot.command(name="set_timezone",
             help='Sets your timezone. Please provide a location (city + state/country). Your location is not saved. It is only used to get your timezone.')
async def set_timezone(ctx, *, location):
    tz = await get_timezone_from_location(location)
    user_timezone = await db.upsert(ctx.author.id, tz)
    await ctx.send(embed=timezone_embed(user_timezone, ctx.author.display_name, ctx.author.avatar_url))


@set_timezone.error
async def set_timezone_error(ctx, error):
    if isinstance(error, CommandInvokeError) and error.original is not None:
        message = error.original
    else:
        message = error_messages["db_connection"]
    await ctx.send(
        embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


@bot.command(name="timezone",
             help='Shows your timezone. If incorrect, run !set_timezone [your location].)')
async def timezone(ctx):
    user_timezone = await db.get_by_id(str(ctx.author.id))
    await ctx.send(embed=timezone_embed(user_timezone, ctx.author.display_name, ctx.author.avatar_url))


@timezone.error
async def timezone_error(ctx, error):
    await ctx.send(
        embed=error_embed(error_messages["db_connection"], ctx.author.display_name, ctx.author.avatar_url))


@bot.command(name="by_day",
             help='Shows matches for a day. Date should be in mm/dd/yyyy format. Can not go back more than a week in the past.')
async def by_day(ctx, date):
    timezone = await db.get_user_timezone_or_default(ctx.author.id)
    matches = scraper.getMatchesByDay(date, timezone)
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
            embed=live_matches_embed(live_matches, MatchType.Default, ctx.author.display_name, ctx.author.avatar_url))
    if len(future_matches) > 0:
        await ctx.send(embed=upcoming_matches_embed(f'Matches on {date}', future_matches, MatchType.Default,
                                                    ctx.author.display_name, ctx.author.avatar_url, timezone))


@by_day.error
async def by_day_error(ctx, error):
    if isinstance(error, CommandInvokeError) and isinstance(error.original, ValueError):
        message = error.original
    else:
        message = error_messages["db_connection"]
    await ctx.send(
        embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


@bot.command(name="today", help="Shows today's matches")
async def today(ctx):
    today = "/".join(
        [str(datetime.today().date().month), str(datetime.today().date().day), str(datetime.today().date().year)])
    await by_day(ctx, today)


@today.error
async def today_error(ctx, error):
    message = error_messages["db_connection"]
    await ctx.send(
        embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


bot.run(TOKEN)
