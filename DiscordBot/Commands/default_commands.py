from discord.ext import commands


class DefaultCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome to this Discord server! Type !help to see commands I can response to!'
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)

def setup(bot):
    bot.add_cog(DefaultCommands(bot))