import datetime
from discord.ext.commands import Bot
import discord.utils
import discord
import data
from tokenid import tokenid
from embedcreator import infoembed, joinembed, serverinfoembed, deleteembed, editembed, badwordembed, linkembed

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

    print(guild.owner.mention)


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
    global channelcounter, musicchannelcounter

    try:
        if after.channel is not None and after.channel.id == 742109026426290176:
            category: discord.CategoryChannel = discord.utils.get(member.guild.categories, id=554265879463067659)
            channel = await category.create_voice_channel(name=f"Kanal Nr. {str(channelcounter)}")
            await member.move_to(channel)

            channelcounter += 1

        if after.channel is not None and after.channel.id == 742108180531642720:
            category: discord.CategoryChannel = discord.utils.get(member.guild.categories, id=554265879463067659)
            channel = await category.create_voice_channel(name=f"Musikkanal Nr. {str(musicchannelcounter)}")
            everyone: discord.Role = discord.utils.get(member.guild.roles, name="@everyone")
            await channel.set_permissions(target=everyone, speak=False)
            await member.move_to(channel)

        try:
            if after.channel is None and not before.channel.id == 742109026426290176 or after.channel \
                    is None and not before.channel.id == 742108180531642720:

                if not before.channel.members:
                    await before.channel.delete()
        except Exception as e:
            print(e)

    except Exception as e:
        print(e)


@bot.event
async def on_raw_reaction_add(ctx: discord.RawReactionActionEvent):
    if ctx.message_id == 696020561876353036:
        if ctx.emoji.name in data.reactions:
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
    if not before.author == bot.user and not before.content == after.content:
        channel: discord.TextChannel = bot.get_channel(data.modchannel_id)
        embed = editembed(before, after)
        await channel.send(embed=embed)


@bot.event
async def on_message(ctx: discord.Message):
    if ctx.author == bot.user:
        return

    for word in data.badwords:
        if word in ctx.content.lower():
            await ctx.delete()
            await ctx.author.send(f"Bitte verzichte darauf, solche Wörter weiterhin auf "
                                  f"**{ctx.guild.name}** zu verwenden!")

            logchannel: discord.TextChannel = bot.get_channel(562665126646382602)

            embed = badwordembed(ctx)
            await logchannel.send(embed=embed)

            return

        if "discord.gg" in ctx.content and "discord.gg/Sx2saFx" not in ctx.content:
            await ctx.delete()
            await ctx.author.send(f"Werbung für andere Server ist auf **{ctx.guild.name}** untersagt!")

            ctx.channel.send(embed=linkembed(ctx))

            return

    await bot.process_commands(ctx)


channelcounter = 1
musicchannelcounter = 1

bot.run(tokenid)
