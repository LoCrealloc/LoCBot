import datetime
from discord.ext.commands import Bot
import discord.utils
import discord
import data
from tokenid import tokenid
from embedcreator import infoembed, joinembed, serverinfoembed, deleteembed, editembed

bot = Bot(command_prefix="§", case_insensitive=True)


@bot.event
async def on_ready():
    activity = discord.Game(name="§info")

    await bot.change_presence(activity=activity, status=discord.Status.online)

    channel: discord.TextChannel = bot.get_channel(686286732693733482)

    message: discord.Message = await channel.fetch_message(696020561876353036)

    for i in data.reactions:
        await message.add_reaction(i)

    print("Bot has logged in succesfully")


@bot.command(name="info", aliases=["infos", "About"])
async def info(ctx: discord.Message):
    """
    Gives you some information about the bot
    """
    embed = infoembed()
    await ctx.channel.send(embed=embed)


@bot.command(name="server", aliases=["serverinfo", "server_information"])
async def server(ctx: discord.Message):
    """
    Gives you some information about the NorthDiscord
    """
    guild: discord.Guild = bot.get_guild(514449077094580274)
    embed = serverinfoembed(guild)

    await ctx.channel.send(embed=embed)


@bot.command(name="ping")
async def ping(ctx: discord.Message):
    """
    Displays the bot latency
    """
    latency = bot.latency * 100
    await ctx.channel.send(f"Pong! {latency} ms")


@bot.event
async def on_member_join(guild: discord.Guild, user: discord.User):
    channel: discord.TextChannel = guild.get_channel(552452481167261697)
    embed = joinembed(user)
    await channel.send(embed=embed)


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if after.channel is not None and after.channel.id == 728280381975035955:
        category: discord.CategoryChannel = discord.utils.get(member.guild.categories, id=554265879463067659)
        await category.create_voice_channel(name="Kanal von " + member.nick)
        channel = discord.utils.get(member.guild.voice_channels, name="Kanal von " + member.nick)
        await member.move_to(channel)

    if after.channel is not None and after.channel.id == 729640108269240321:
        category: discord.CategoryChannel = discord.utils.get(member.guild.categories, id=554265879463067659)
        await category.create_voice_channel(name="Musikkanal von " + member.nick)
        channel: discord.VoiceChannel = discord.utils.get(member.guild.voice_channels, name="Musikkanal von " + member.nick)
        everyone: discord.Role = discord.utils.get(member.guild.roles, name="@everyone")
        await channel.set_permissions(target=everyone, speak=False)
        await member.move_to(channel)

    elif after.channel is None:
        if not before.channel.members:
            await before.channel.delete()


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


# Modkram
@bot.event
async def on_message_delete(message: discord.Message):
    channel: discord.TextChannel = bot.get_channel(data.modchannel_id)
    embed = deleteembed(message)
    await channel.send(embed=embed)


@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if not before.author == bot.user:
        channel: discord.TextChannel = bot.get_channel(data.modchannel_id)
        embed = editembed(before, after)
        await channel.send(embed=embed)


@bot.event
async def on_message(ctx: discord.Message):
    words = ctx.content.split(" ")
    if any(word.lower() in data.badwords for word in words):
        await ctx.delete()
        await ctx.author.send("Bitte verzichte darauf, solche Wörter weiterhin auf **" + ctx.guild.name +
                              "** zu verwenden!")
        logchannel: discord.TextChannel = await bot.fetch_channel(562665126646382602)

        embed = discord.Embed(title="Nachricht gelöscht",
                              description=f"{ctx.author.mention}" + " hat eine Nachricht mit unangebrachtem Inhalt in "
                                          + f"{ctx.channel.mention}" + " gesendet:",
                              color=data.color)
        print(bot.user.colour)
        embed.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        embed.add_field(name="Inhalt der Nachricht:", value=ctx.content)
        embed.set_footer(text="Nachricht gelöscht am " + datetime.datetime.now().strftime("%d.%m.%Y") + " um "
                              + datetime.datetime.now().strftime("%H:%M"))

        await logchannel.send(embed=embed)

    await bot.process_commands(ctx)

try:
    bot.run(tokenid)
except Exception as e:
    print(e)
