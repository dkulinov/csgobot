from datetime import datetime

import discord
import pytz

from Commons.Types.Match.FutureMatch import FutureMatch
from DiscordBot.helpers import get_embed_author_title
from HLTVScraper.Helpers.UrlBuilder import URLBuilder


def upcoming_matches_embed(title, future_matches: [FutureMatch], predefinedFilter, author_name, author_icon,
                           author_timezone):
    embed = discord.Embed(title=f'{title}',
                          url=URLBuilder().buildGetUpcomingMatchesUrl(predefinedFilter),
                          color=discord.Color.green())
    embed.set_author(name=get_embed_author_title(author_name), icon_url=author_icon)
    for future_match in future_matches:
        date = datetime.fromtimestamp(int(future_match.epochTime) // 1000, tz=pytz.timezone(author_timezone)).strftime(
            '%Y-%m-%d %I:%M %p')
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
