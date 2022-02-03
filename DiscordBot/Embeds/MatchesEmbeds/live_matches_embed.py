import discord

from Commons.Types.Match.CurrentMatch import CurrentMatch
from DiscordBot.helpers import get_embed_author_title
from HLTVScraper.Helpers.UrlBuilder import URLBuilder


def live_matches_embed(live_matches: [CurrentMatch], predefinedFilter, author_name, author_icon):
    embed = discord.Embed(title='Live matches:',
                          url=URLBuilder().buildGetUpcomingMatchesUrl(predefinedFilter),
                          color=discord.Color.green())
    embed.set_author(name=get_embed_author_title(author_name), icon_url=author_icon)
    for live_match in live_matches:
        embed.add_field(
            name=f'--- {live_match.team1} vs {live_match.team2} ---',
            value=f'BO{live_match.bestOf}. Maps won: {live_match.team1MapsWon} : {live_match.team2MapsWon}'
                  f'\nCurrent map score: {live_match.team1CuMapScore} : {live_match.team2CuMapScore}'
                  f'\n[Click here]({live_match.link}) for more details.',
            inline=False)
    return embed