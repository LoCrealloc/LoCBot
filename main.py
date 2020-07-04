import datetime
from discord.ext.commands import Bot
import discord.utils
import discord
import data
from tokenid import tokenid
from infoembed import create_embed

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
    embed = create_embed()
    await ctx.channel.send(embed=embed)


@bot.command(name="server", aliases=["serverinfo", "server_information"])
async def server(ctx: discord.Message):
    guild: discord.Guild = bot.get_guild(514449077094580274)

    embed = discord.Embed(title="NorthDiscord",
                          description="Dies ist der offizielle Discordserver von LoC",
                          color=data.color,
                          url="https://discord.gg/Sx2saFx")
    embed.set_thumbnail(url=data.servericon_url)
    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="Erstellungsdatum", value="20.11.2018", inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Rollen", value=str(len(guild.roles)), inline=True)
    embed.add_field(name="Invitelink", value="https://discord.gg/Sx2saFx", inline=True)

    embed.set_footer(text="Lade deine Freunde zu diesem Server ein, um ihn noch großartiger zu machen!",
                     icon_url=data.avatar_url)

    await ctx.channel.send(embed=embed)


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if after.channel is not None and after.channel.id == 728280381975035955:
        category: discord.CategoryChannel = discord.utils.get(member.guild.categories, id=554265879463067659)
        await category.create_voice_channel(name="Kanal von " + member.nick)
        channel = discord.utils.get(member.guild.voice_channels, name="Kanal von " + member.nick)
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

    await bot.process_commands(ctx)

bot.run(tokenid)
