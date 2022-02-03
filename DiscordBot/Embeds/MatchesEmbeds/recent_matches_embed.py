import discord

from Commons.Types.Match.PastMatch import PastMatch
from DiscordBot.helpers import get_embed_author_title
from HLTVScraper.Helpers.UrlBuilder import URLBuilder


def recent_matches_embed(title, recent_matches: [PastMatch], offset, author_name, author_icon):
    embed = discord.Embed(title=title,
                          url=URLBuilder().buildGetPastMatches(offset),
                          color=discord.Color.teal())
    embed.set_author(name=get_embed_author_title(author_name), icon_url=author_icon)
    for recent_match in recent_matches:
        embed.add_field(
            name=f'--- {recent_match.team1} vs {recent_match.team2} ---',
            value=f'[{recent_match.team1} {recent_match.team1Score} : {recent_match.team2Score} {recent_match.team2}]({recent_match.link})',
            inline=False)
    return embed
