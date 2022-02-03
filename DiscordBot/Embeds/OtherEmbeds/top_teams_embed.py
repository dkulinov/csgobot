import discord

from Commons.Types.TopTeam import TopTeam
from DiscordBot.helpers import get_embed_author_title


def top_teams_embed(teams: [TopTeam], author_name, author_icon):
    embed = discord.Embed(title=f'HLTV Top {len(teams)} teams:', url=urlBuilder.buildGetTopTeamsUrl(),
                          color=discord.Color.gold())
    embed.set_author(name=get_embed_author_title(author_name), icon_url=author_icon)
    for rank, team in enumerate(teams):
        if team.change == "-":
            rank_change_title = ''
        else:
            rank_change_title = f'({team.change})'
        embed.add_field(name=f'#{str(rank + 1)}  {rank_change_title}',
                        value=f'[{team.teamName}]({team.link}): {team.points[1:-1]}',
                        inline=True)
    return embed
