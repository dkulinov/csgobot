import discord


def error_embed(message, author_name, author_icon):
    embed = discord.Embed(title='Error:', description=message, color=discord.Color.red())
    embed.set_author(name=author_name, icon_url=author_icon)
    embed.set_image(url='https://i.ibb.co/dKDw6y0/error.jpg')
    return embed
