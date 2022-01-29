# bot.py
import os
from datetime import datetime

import discord
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, CommandInvokeError
from dotenv import load_dotenv

from Commons.Exceptions.InvalidTeamException import InvalidTeamException
from Commons.Types.Match.MatchByTeam import MatchByTeam
from Commons.Types.Match.PastMatch import PastMatch
from Commons.Types.News import News
from Commons.Types.Team import HLTVTeams
from Commons.Types.TopTeam import TopTeam
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

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

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
bot = commands.Bot(command_prefix='!')


# https://stackoverflow.com/questions/57182398/is-it-possible-to-attach-multiple-images-in-a-embed/57191891#:~:text=Yes%20and%20no.,shown%20separately%20from%20the%20embed.


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


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


@bot.command(help="Repeats after you")
async def echo(ctx, *arg):
    *response, = arg
    await ctx.send(" ".join(response))


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
    print(error)
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
    past_matches_by_team = scraper.getMatchesByTeam(team, MatchTime.past)[::-1]
    future_matches_by_team = scraper.getMatchesByTeam(team, MatchTime.future)
    await ctx.send(embed=past_matches_by_team_embed(team, past_matches_by_team[:25], ctx.author.display_name,
                                                    ctx.author.avatar_url))
    await ctx.send(embed=future_matches_by_team_embed(team, future_matches_by_team[:25], ctx.author.display_name,
                                                      ctx.author.avatar_url))


@matches_for.error
async def matches_for_error(ctx, error):
    if isinstance(error, CommandInvokeError) and isinstance(error.original, InvalidTeamException):
        message = f'Please enter a supported team: {", ".join(list(HLTVTeams().HLTV_teams.keys()))}'
    elif isinstance(error, MissingRequiredArgument):
        message = f'Please provide a team'
    else:
        message = ":( Something went wrong. Please try again."
    await ctx.send(embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))


def past_matches_by_team_embed(team, past_matches: [MatchByTeam], author_name, author_icon):
    embed = discord.Embed(title=f'{team.upper()}\'s recent matches:',
                          url=urlBuilder.buildGetMatchesByTeamUrl(team) + "#tab-matchesBox",
                          color=discord.Color.teal())
    embed.set_author(name=f'hey {author_name}, here you go!', icon_url=author_icon)
    if past_matches[0].team1Logo == "/img/static/team/placeholder.svg":
        past_matches[0].team1Logo = "https://hltv.org" + past_matches[0].team1Logo
    embed.set_thumbnail(url=past_matches[0].team1Logo)
    for past_match in past_matches:
        date = datetime.fromtimestamp(int(past_match.epochTime) // 1000).strftime('%Y-%m-%d')
        embed.add_field(name=f'--- {date} ---',
                        value=f'[{past_match.team1Score} : {past_match.team2Score} vs {past_match.team2}]({past_match.link}). '
                              f'\nRun: !series_stats {past_match.link} for more details',
                        inline=False)
    return embed


def future_matches_by_team_embed(team, future_matches: [MatchByTeam], author_name, author_icon):
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
        date = datetime.fromtimestamp(int(future_match.epochTime) // 1000).strftime('%Y-%m-%d %I:%M %p')
        embed.add_field(name=f'--- {date} ---', value=f'[vs {future_match.team2}]({future_match.link})', inline=False)
    return embed


@bot.command(name="recent_matches",
             help=f'Shows recent matches. You can also provide number of matches (between 1-25) and the offset (non-negative number).')
async def recent_matches(ctx, number=10, offset=0):
    recent_matches: [PastMatch] = scraper.getAllMatches(MatchContainers.past, numberPast=number, offset=offset)
    await ctx.send(embed=recent_matches_embed(recent_matches[:number], offset, ctx.author.display_name, ctx.author.avatar_url))


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
                  f'\nRun: !series_stats {recent_match.link} for more details',
            inline=False)
    return embed


bot.run(TOKEN)
