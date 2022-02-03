import discord

from Commons.Types.News import News
from DiscordBot.helpers import get_embed_author_title
from HLTVScraper.Helpers.UrlBuilder import URLBuilder


def news_embed(recent_news: [News], author_name, author_icon):
    embed = discord.Embed(title=f'HLTV\'s recent news:', url=URLBuilder().buildGetNewsUrl(),
                          color=discord.Color.teal())
    embed.set_author(name=get_embed_author_title(author_name), icon_url=author_icon)
    embed.set_thumbnail(
        url="https://i.ibb.co/Zm6hzzN/Breaking-news-World-news-with-map-backgorund-Breaking-news-TV-concept-Vector-stock.jpg")
    for the_news in recent_news:
        embed.add_field(name="---", value=f'[{the_news.title}]({the_news.link})', inline=False)
    return embed
