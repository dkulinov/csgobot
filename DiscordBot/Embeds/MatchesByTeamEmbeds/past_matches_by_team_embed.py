from datetime import datetime

import discord
import pytz

from Commons.Types.Match.MatchByTeam import MatchByTeam
from DiscordBot.helpers import get_embed_author_title
from HLTVScraper.Helpers.UrlBuilder import URLBuilder


def past_matches_by_team_embed(team, past_matches: [MatchByTeam], author_name, author_icon, author_timezone):
    embed = discord.Embed(title=f'{team.upper()}\'s recent matches:',
                          url=URLBuilder().buildGetMatchesByTeamUrl(team) + "#tab-matchesBox",
                          color=discord.Color.teal())
    embed.set_author(name=get_embed_author_title(author_name), icon_url=author_icon)
    if past_matches[0].team1Logo == "/img/static/team/placeholder.svg":
        past_matches[0].team1Logo = "https://hltv.org" + past_matches[0].team1Logo
    embed.set_thumbnail(url=past_matches[0].team1Logo)
    for past_match in past_matches:
        date = datetime.fromtimestamp(int(past_match.epochTime) // 1000, tz=pytz.timezone(author_timezone)).strftime(
            '%Y-%m-%d')
        embed.add_field(name=f'--- {date} ---',
                        value=f'[{past_match.team1Score} : {past_match.team2Score} vs {past_match.team2}]({past_match.link}). ',
                        inline=False)
    return embed
