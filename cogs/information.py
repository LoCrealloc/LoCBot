from discord.ext.commands import Cog, command, Bot, Context
from embedcreator import infoembed, serverinfoembed
from discord import Guild


class Information(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="ping")
    async def ping(self, ctx: Context):
        """
        Displays the bot latency
        """
        latency = str(self.bot.latency * 100).split(".")[0]
        await ctx.channel.send(f"Pong! {latency} ms")

    @command(name="info", aliases=["infos", "about"])
    async def info(self, ctx: Context):
        """
        Gives you some information about the LoCbot
        """
        embed = infoembed()
        await ctx.channel.send(embed=embed)

    @command(name="server", aliases=["serverinfo", "server_information"])
    async def server(self, ctx: Context):
        """
        Gives you some information about the NorthDiscord
        """
        guild: Guild = ctx.guild
        embed = serverinfoembed(guild)

        await ctx.channel.send(embed=embed)
