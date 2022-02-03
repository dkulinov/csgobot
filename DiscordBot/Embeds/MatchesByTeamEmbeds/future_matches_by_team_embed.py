from datetime import datetime

import discord
import pytz

from Commons.Types.Match.MatchByTeam import MatchByTeam
from DiscordBot.helpers import get_embed_author_title
from HLTVScraper.Helpers.UrlBuilder import URLBuilder


def future_matches_by_team_embed(team, future_matches: [MatchByTeam], author_name, author_icon, author_timezone):
    embed = discord.Embed(title=f'{team.upper()}\'s upcoming matches:',
                          url=URLBuilder().buildGetMatchesByTeamUrl(team) + "#tab-matchesBox",
                          color=discord.Color.blue())
    embed.set_author(name=get_embed_author_title(author_name), icon_url=author_icon)
    if len(future_matches) == 0:
        embed.add_field(name="No upcoming matches scheduled.", value="Please try again another time.")
        return embed
    if future_matches[0].team1Logo == "/img/static/team/placeholder.svg":
        future_matches[0].team1Logo = "https://hltv.org" + future_matches[0].team1Logo
    embed.set_thumbnail(url=future_matches[0].team1Logo)
    for future_match in future_matches:
        date = datetime.fromtimestamp(int(future_match.epochTime) // 1000, tz=pytz.timezone(author_timezone)).strftime(
            '%Y-%m-%d %I:%M %p')
        embed.add_field(name=f'--- {date} ---', value=f'[vs {future_match.team2}]({future_match.link})', inline=False)
    return embed
