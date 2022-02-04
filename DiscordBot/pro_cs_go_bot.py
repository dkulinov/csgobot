import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from DiscordBot.DB.db import UserTimezoneDB
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


class ProCsgoBot(commands.Bot):
    def __init__(self, command_prefix, scraper: Scraper, db: UserTimezoneDB):
        commands.Bot.__init__(self, command_prefix, intents=discord.Intents().all())
        self.scraper = scraper
        self.db = db
        self.cog_files = ['Commands.news_command', 'Commands.default_commands', 'Commands.top_teams_command',
                          'Commands.matches_by_team_command', 'Commands.matches_by_timeframe_commands',
                          'Commands.timezone_commands', 'Commands.matches_by_day_commands']

    def add_commands(self):
        for cog_file in self.cog_files:
            self.load_extension(cog_file)
            print("%s has loaded." % cog_file)

    async def on_ready(self):
        await self.db.set_up_db()
        print("DB is ready.")
        self.add_commands()
        print("I'm ready!")


def main():
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
    db = UserTimezoneDB()

    bot = ProCsgoBot(command_prefix="!", scraper=scraper, db=db)
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
