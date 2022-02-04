from discord.ext import commands
from discord.ext.commands import CommandInvokeError

from DiscordBot.Embeds.ErrorEmbeds.error_embed import error_embed
from DiscordBot.Embeds.OtherEmbeds.timezone_embed import timezone_embed
from DiscordBot.constants import error_messages
from DiscordBot.geolocator import get_timezone_from_location


class TimezoneCommands(commands.Cog):
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db

    @commands.command(name="set_timezone",
                 help='Sets your timezone. Please provide a location (city + state/country). Your location is not saved. It is only used to get your timezone.')
    async def set_timezone(self, ctx, *, location):
        tz = await get_timezone_from_location(location)
        user_timezone = await self.db.upsert(ctx.author.id, tz)
        await ctx.send(embed=timezone_embed(user_timezone, ctx.author.display_name, ctx.author.avatar_url))

    @set_timezone.error
    async def set_timezone_error(self, ctx, error):
        if isinstance(error, CommandInvokeError) and error.original is not None:
            message = error.original
        else:
            message = error_messages["db_connection"]
        await ctx.send(
            embed=error_embed(message, ctx.author.display_name, ctx.author.avatar_url))

    @commands.command(name="timezone",
                 help='Shows your timezone. If incorrect, run !set_timezone [your location].)')
    async def timezone(self, ctx):
        user_timezone = await self.db.get_by_id(str(ctx.author.id))
        await ctx.send(embed=timezone_embed(user_timezone, ctx.author.display_name, ctx.author.avatar_url))

    @timezone.error
    async def timezone_error(self, ctx, error):
        await ctx.send(
            embed=error_embed(error_messages["db_connection"], ctx.author.display_name, ctx.author.avatar_url))


def setup(bot):
    bot.add_cog(TimezoneCommands(bot, bot.db))