# bot.py
import math
import os
from datetime import datetime

import aiosqlite
import discord
from aiosqlite import Cursor
from discord import Member
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, CommandInvokeError
from dotenv import load_dotenv

from Commons.Exceptions.InvalidTeamException import InvalidTeamException
from Commons.Types.Match.CurrentMatch import CurrentMatch
from Commons.Types.Match.FutureMatch import FutureMatch
from Commons.Types.Match.MatchByTeam import MatchByTeam
from Commons.Types.Match.PastMatch import PastMatch
from Commons.Types.MatchType import MatchType
from Commons.Types.News import News
from Commons.Types.SeriesStats.MatchStats import MatchStats
from Commons.Types.SeriesStats.SeriesStats import SeriesStats
from Commons.Types.Team import HLTVTeams
from Commons.Types.TopTeam import TopTeam
from DiscordBot.DB.UserTimezone import UserTimezone
from DiscordBot.DB.db import UserTimezoneDB
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
from geopy.geocoders import GoogleV3
import pytz

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

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

empty_char = '\u200b'
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='!', intents=intents)
db = UserTimezoneDB()


# https://stackoverflow.com/questions/57182398/is-it-possible-to-attach-multiple-images-in-a-embed/57191891#:~:text=Yes%20and%20no.,shown%20separately%20from%20the%20embed.
# await ctx.author.edit(nick =ctx.author.name + " [timezone]")

@bot.event
async def on_ready():
    await db.set_up_db()
    print("I'm ready!")


# TODO: give list of commands
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server! Type !help to see commands I can response to!'
    )


@bot.event
async def on_command_error(ctx, error):
    pass


@bot.command(name="top_teams",
             help="Shows HLTV's Top 25 Teams. You can also specify number of teams you want to see as a number (Between 1 and 25).")
async def top_teams(ctx, number: int = 25):
    if number < 1:
        await ctx.send("Can't pass a number less than 1")
        return
    if number > 25:
        await ctx.send("Number can't be more than 25")
        return
    if number is None:
        number = 25
    teams = scraper.getTopTeams()
    await ctx.send(embed=top_teams_embed(teams[:number], ctx.author.display_name, ctx.author.avatar_url))


@top_teams.error
async def top_teams_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        message = "Please provide a whole number."
    else:
        message = ":( Something went wrong. Please try again."
    await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


def error_embed(message, author_name, author_icon):
    embed = discord.Embed(title='Error:', description=message, color=discord.Color.red())
    embed.set_author(name=author_name, icon_url=author_icon)
    embed.set_image(url='https://i.ibb.co/dKDw6y0/error.jpg')
    return embed


def top_teams_embed(teams: [TopTeam], author_name, author_icon):
    embed = discord.Embed(title=f'HLTV Top {len(teams)} teams:', url=urlBuilder.buildGetTopTeamsUrl(),
                          color=discord.Color.gold())
    embed.set_author(name=f'hey {author_name}, here you go!', icon_url=author_icon)
    for rank, team in enumerate(teams):
        if team.change == "-":
            rank_change_title = ''
        else:
            rank_change_title = f'({team.change})'
        embed.add_field(name=f'#{str(rank + 1)}  {rank_change_title}',
                        value=f'[{team.teamName}]({team.link}): {team.points[1:-1]}',
                        inline=True)
    return embed


@bot.command(name="news", help="Shows HLTV's recent news.")
async def news(ctx):
    recent_news = scraper.getNews()
    await ctx.send(embed=news_embed(recent_news[:10], ctx.author.display_name, ctx.author.avatar_url))


@news.error
async def news_error(ctx, error):
    message = ":( Something went wrong. Please try again."
    await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


def news_embed(recent_news: [News], author_name, author_icon):
    embed = discord.Embed(title=f'HLTV\'s recent news:', url=urlBuilder.buildGetNewsUrl(),
                          color=discord.Color.teal())
    embed.set_author(name=f'hey {author_name}, here you go!', icon_url=author_icon)
    embed.set_thumbnail(
        url="https://i.ibb.co/Zm6hzzN/Breaking-news-World-news-with-map-backgorund-Breaking-news-TV-concept-Vector-stock.jpg")
    for the_news in recent_news:
        embed.add_field(name="---", value=f'[{the_news.title}]({the_news.link})', inline=False)
    return embed


@bot.command(name="matches_for", help=f'Supported teams: {", ".join(list(HLTVTeams().HLTV_teams.keys()))}')
async def matches_for(ctx, *, team):
    user_timezone = await db.get_by_id(ctx.author.id)
    if user_timezone is not None:
        timezone = user_timezone.timezone
    else:
        timezone = "America/Phoenix"
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
        message = ":( Something went wrong. Please try again."
    await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


def past_matches_by_team_embed(team, past_matches: [MatchByTeam], author_name, author_icon, author_timezone):
    embed = discord.Embed(title=f'{team.upper()}\'s recent matches:',
                          url=urlBuilder.buildGetMatchesByTeamUrl(team) + "#tab-matchesBox",
                          color=discord.Color.teal())
    embed.set_author(name=f'hey {author_name}, here you go!', icon_url=author_icon)
    if past_matches[0].team1Logo == "/img/static/team/placeholder.svg":
        past_matches[0].team1Logo = "https://hltv.org" + past_matches[0].team1Logo
    embed.set_thumbnail(url=past_matches[0].team1Logo)
    for past_match in past_matches:
        date = datetime.fromtimestamp(int(past_match.epochTime) // 1000, tz=pytz.timezone(author_timezone)).strftime('%Y-%m-%d')
        embed.add_field(name=f'--- {date} ---',
                        value=f'[{past_match.team1Score} : {past_match.team2Score} vs {past_match.team2}]({past_match.link}). '
                              f'\nRun: !stats {past_match.link} for more details',
                        inline=False)
    return embed


def future_matches_by_team_embed(team, future_matches: [MatchByTeam], author_name, author_icon, author_timezone):
    embed = discord.Embed(title=f'{team.upper()}\'s upcoming matches:',
                          url=urlBuilder.buildGetMatchesByTeamUrl(team) + "#tab-matchesBox",
                          color=discord.Color.blue())
    embed.set_author(name=f'hey {author_name}, here you go!', icon_url=author_icon)
    if len(future_matches) == 0:
        embed.add_field(name="No upcoming matches scheduled.", value="Please try again another time.")
        return embed
    if future_matches[0].team1Logo == "/img/static/team/placeholder.svg":
        future_matches[0].team1Logo = "https://hltv.org" + future_matches[0].team1Logo
    embed.set_thumbnail(url=future_matches[0].team1Logo)
    for future_match in future_matches:
        date = datetime.fromtimestamp(int(future_match.epochTime) // 1000, tz=pytz.timezone(author_timezone)).strftime('%Y-%m-%d %I:%M %p')
        embed.add_field(name=f'--- {date} ---', value=f'[vs {future_match.team2}]({future_match.link})', inline=False)
    return embed


@bot.command(name="recent",
             help=f'Shows recent matches. You can also provide number of matches (between 1-25) and the offset (non-negative number).')
async def recent_matches(ctx, number=10, offset=0):
    recent_matches: [PastMatch] = scraper.getAllMatches(MatchContainers.past, numberPast=number, offset=offset)
    await ctx.send(
        embed=recent_matches_embed(recent_matches[:number], offset, ctx.author.display_name, ctx.author.avatar_url))


@recent_matches.error
async def recent_matches_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        message = "Please provide a whole number."
    elif isinstance(error, CommandInvokeError) and isinstance(error.original, ValueError):
        message = error.original
    else:
        message = ":( Something went wrong. Please try again."
    await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


def recent_matches_embed(recent_matches: [PastMatch], offset, author_name, author_icon):
    embed = discord.Embed(title=f'Recent matches ({offset + 1}-{offset + len(recent_matches)}):',
                          url=urlBuilder.buildGetPastMatches(offset),
                          color=discord.Color.teal())
    embed.set_author(name=f'hey {author_name}, here you go!', icon_url=author_icon)
    for recent_match in recent_matches:
        embed.add_field(
            name=f'--- {recent_match.team1} vs {recent_match.team2} ---',
            value=f'[{recent_match.team1} {recent_match.team1Score} : {recent_match.team2Score} {recent_match.team2}]({recent_match.link})'
                  f'\nRun: !stats {recent_match.link} for more details',
            inline=False)
    return embed


@bot.command(name="live",
             help='Shows live matches. You can also provide a filter (top_tier or lan). If not provided, will return all matches.')
async def live_matches(ctx, match_filter="none"):
    if match_filter == "top_tier":
        match_type = MatchType.TopTier
    elif match_filter == "lan":
        match_type = MatchType.LanOnly
    elif match_filter == "none":
        match_type = MatchType.Default
    else:
        raise TypeError("Filter has to be either top_tier or lan")
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
        message = ":( Something went wrong. Please try again."
    await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


def live_matches_embed(live_matches: [CurrentMatch], predefinedFilter, author_name, author_icon):
    embed = discord.Embed(title='Live matches:',
                          url=urlBuilder.buildGetUpcomingMatchesUrl(predefinedFilter),
                          color=discord.Color.green())
    embed.set_author(name=f'hey {author_name}, here you go!', icon_url=author_icon)
    for live_match in live_matches:
        embed.add_field(
            name=f'--- {live_match.team1} vs {live_match.team2} ---',
            value=f'BO{live_match.bestOf}. Maps won: {live_match.team1MapsWon} : {live_match.team2MapsWon}'
                  f'\nCurrent map score: {live_match.team1CuMapScore} : {live_match.team2CuMapScore}'
                  f'\n[Click here]({live_match.link}) for more details.',
            inline=False)
    return embed


@bot.command(name="upcoming",
             help='Shows upcoming matches. You can also provide a filter (top_tier or lan). If not provided, will return all matches. You can also provide a number of matches to get.')
async def upcoming_matches(ctx, number=100, match_filter="none"):
    if match_filter == "top_tier":
        match_type = MatchType.TopTier
    elif match_filter == "lan":
        match_type = MatchType.LanOnly
    elif match_filter == "none":
        match_type = MatchType.Default
    else:
        raise TypeError("Filter has to be either top_tier or lan")
    if number < 1:
        raise ValueError("Number of matches has to be positive")
    user_timezone = await db.get_by_id(ctx.author.id)
    if user_timezone is not None:
        timezone = user_timezone.timezone
    else:
        timezone = "America/Chicago"
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
            embed=upcoming_matches_embed(batch_of_matches, match_type, ctx.author.display_name, ctx.author.avatar_url, timezone))


@upcoming_matches.error
async def upcoming_matches_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        message = error
    elif isinstance(error, CommandInvokeError) and isinstance(error.original, TypeError):
        message = "Filter has to be either top_tier or lan."
    elif isinstance(error, CommandInvokeError) and isinstance(error.original, ValueError):
        message = error.original
    else:
        message = ":( Something went wrong. Please try again."
    await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


def upcoming_matches_embed(future_matches: [FutureMatch], predefinedFilter, author_name, author_icon, author_timezone):
    embed = discord.Embed(title='Upcoming matches:',
                          url=urlBuilder.buildGetUpcomingMatchesUrl(predefinedFilter),
                          color=discord.Color.green())
    embed.set_author(name=f'hey {author_name}, here you go!', icon_url=author_icon)
    for future_match in future_matches:
        date = datetime.fromtimestamp(int(future_match.epochTime) // 1000, tz=pytz.timezone(author_timezone)).strftime('%Y-%m-%d %I:%M %p')
        if future_match.emptyMatchDescription is not None:
            embed.add_field(
                name=f'--- {date} ---',
                value=f'BO{future_match.bestOf}. [{future_match.emptyMatchDescription}]({future_match.link})',
                inline=False)
        else:
            embed.add_field(
                name=f'--- {date} ---',
                value=f'BO{future_match.bestOf}. [{future_match.team1} vs {future_match.team2}]({future_match.link})',
                inline=False)
    return embed


@bot.command(name="set_timezone",
             help='Sets your timezone.')
async def set_timezone(ctx, *, city):
    tz = get_timezone_from_city(city)
    user_timezone = await db.upsert(ctx.author.id, tz)
    await ctx.send(embed=timezone_embed(user_timezone, ctx.author.display_name, ctx.author.avatar_url))


@set_timezone.error
async def set_timezone_error(ctx, error):
    print(error)
    await ctx.send(
        embed=error_embed("Could not connect to DB. Please try again.", ctx.author.display_name, ctx.author.avatar_url))


@bot.command(name="timezone",
             help='Shows your timezone.')
async def timezone(ctx):
    user_timezone = await db.get_by_id(str(ctx.author.id))
    await ctx.send(embed=timezone_embed(user_timezone, ctx.author.display_name, ctx.author.avatar_url))


@timezone.error
async def timezone_error(ctx, error):
    print(error)
    await ctx.send(
        embed=error_embed("Could not connect to DB. Please try again.", ctx.author.display_name, ctx.author.avatar_url))


def timezone_embed(user_timezone, author_name, author_icon):
    if user_timezone is None:
        timezone = "not set. To set it, run !set_timezone [your_city]"
    else:
        timezone = user_timezone.timezone
    embed = discord.Embed(title=f"Your timezone is {timezone}", color=discord.Color.green())
    embed.set_author(name=f'hey {author_name}, here you go!', icon_url=author_icon)
    return embed


def get_timezone_from_city(city):
    geolocator = GoogleV3(api_key=GOOGLE_API_KEY)
    location = geolocator.geocode(city)
    if location is None:
        raise LookupError("Invalid location")
    timezone = geolocator.reverse_timezone((location.latitude, location.longitude))
    return timezone



bot.run(TOKEN)
