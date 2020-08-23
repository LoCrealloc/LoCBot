from discord.ext.commands import Cog, command, Bot, has_permissions, Context
from discord import Member, Guild, Message, TextChannel
from data import muterole_id
from embedcreator import muteembed
from asyncio import sleep


class Administration(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="mute")
    @has_permissions(administrator=True)
    async def mute(self, ctx: Context, user: Member, time: int):
        """
        Mutes the specified user for 'time' seconds
        """

        guild: Guild = ctx.guild
        muterole = guild.get_role(muterole_id)

        await ctx.message.delete()

        await user.add_roles(muterole)

        embed = muteembed(author=ctx.author, user=user, time=time, newtime=time)

        message: Message = await ctx.channel.send(content=user.mention, embed=embed)

        for minute in range(time):
            minute += 1

            await sleep(60)

            embed = muteembed(author=ctx.author, user=user, time=time, newtime=time - minute)

            await message.edit(embed=embed)

        await message.delete()

        await user.remove_roles(muterole)

    @command(name="purge", aliases=["clear"])
    @has_permissions(administrator=True)
    async def purge(self, ctx: Context, amount: int):
        """
        Purges a number of messages in a channel
        """
        channel: TextChannel = ctx.channel

        await channel.purge(limit=amount)

        await sleep(3)
        await ctx.message.delete()
