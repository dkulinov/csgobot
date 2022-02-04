from discord.ext import commands
from DiscordBot.Embeds.ErrorEmbeds.error_embed import error_embed
from DiscordBot.Embeds.OtherEmbeds.news_embed import news_embed
from DiscordBot.constants import error_messages


class NewsCommand(commands.Cog):
    def __init__(self, bot, scraper):
        self.bot = bot
        self.scraper = scraper

    @commands.command(name="news", help="Shows HLTV's recent news.")
    async def news(self, ctx):
        recent_news = self.scraper.getNews()
        await ctx.send(embed=news_embed(recent_news[:10], ctx.author.display_name, ctx.author.avatar_url))

    @news.error
    async def news_error(self, ctx, error):
        await ctx.send(embed=error_embed(error_messages["general"], ctx.author.display_name, ctx.author.avatar_url))


def setup(bot):
    bot.add_cog(NewsCommand(bot, bot.scraper))