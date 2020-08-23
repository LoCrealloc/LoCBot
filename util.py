from discord.ext.commands import Cog, Bot


def add_cogs(bot, cogs: list):
    for cog in cogs:
        bot.add_cog(cog(bot))
