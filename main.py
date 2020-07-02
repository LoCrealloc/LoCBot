import datetime
from discord.ext.commands import Bot
import discord.utils
import discord
import data
from tokenid import tokenid

bot = Bot(command_prefix="§")


@bot.event
async def on_ready():
    activity = discord.Game(name="§info")

    await bot.change_presence(activity=activity, status=discord.Status.online)

    channel: discord.TextChannel = bot.get_channel(686286732693733482)

    message: discord.Message = await channel.fetch_message(696020561876353036)

    for i in data.reactions:
        await message.add_reaction(i)

    print("Bot has logged in succesfully")


@bot.event
async def on_raw_reaction_add(ctx: discord.RawReactionActionEvent):
    if ctx.message_id == 696020561876353036:
        color = data.reactord[ctx.emoji.name]
        guild: discord.Guild = await bot.fetch_guild(514449077094580274)
        role = discord.utils.get(guild.roles, name=color)
        member: discord.Member = await guild.fetch_member(ctx.user_id)
        await member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(ctx: discord.RawReactionActionEvent):
    if ctx.message_id == 696020561876353036:
        color = data.reactord[ctx.emoji.name]
        guild: discord.Guild = await bot.fetch_guild(514449077094580274)
        role = discord.utils.get(guild.roles, name=color)
        member: discord.Member = await guild.fetch_member(ctx.user_id)
        await member.remove_roles(role)


@bot.event
async def on_message(ctx: discord.Message):
    words = ctx.content.split(" ")
    if any(word.lower() in data.badwords for word in words):
        await ctx.delete()
        await ctx.author.send("Bitte verzichte darauf, solche Wörter weiterhin auf **" + ctx.guild.name +
                              "** zu verwenden!")
        logchannel: discord.TextChannel = await bot.fetch_channel(562665126646382602)

        embed = discord.Embed(title="Nachricht gelöscht",
                              description=f"{ctx.author.mention}" + " hat eine Nachricht mit unangebrachtem Inhalt in " +
                                          f"{ctx.channel.mention}" + " gesendet:",
                              color=data.color)
        print(bot.user.colour)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.add_field(name="Inhalt der Nachricht:", value=ctx.content)
        embed.set_footer(text="Nachricht gelöscht am " + datetime.datetime.now().strftime("%d.%m.%Y") + " um "
                              + datetime.datetime.now().strftime("%H:%M"))

        await logchannel.send(embed=embed)

bot.run(tokenid)
