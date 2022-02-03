import discord

from DiscordBot.helpers import get_embed_author_title


def timezone_embed(user_timezone, author_name, author_icon):
    if user_timezone is None:
        timezone = "not set. To set it, run !set_timezone [your_city]"
    else:
        timezone = user_timezone.timezone
    embed = discord.Embed(title=f"Your timezone is {timezone}", color=discord.Color.green())
    embed.set_author(name=get_embed_author_title(author_name), icon_url=author_icon)
    return embed