from discord.ext.commands import Bot, has_permissions, errors, Context
import discord.utils
from discord import TextChannel, Message, Member, Guild
import data
from tokenid import tokenid
from embedcreator import infoembed, joinembed, serverinfoembed, deleteembed, editembed, badwordembed, linkembed, \
     muteembed
from asyncio import sleep

bot = Bot(command_prefix="§", case_insensitive=True)


@bot.event
async def on_ready():
    activity = discord.Game(name="§info")

    await bot.change_presence(activity=activity, status=discord.Status.online)

    channel: discord.TextChannel = bot.get_channel(data.rolechannel_id)

    message: discord.Message = await channel.fetch_message(data.rolemessage_id)

    for i in data.reactions:
        await message.add_reaction(i)

    print("Bot has logged in succesfully")


@bot.command(name="info", aliases=["infos", "about"])
async def info(ctx: discord.Message):
    """
    Gives you some information about the locbot
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


@bot.command(name="purge", aliases=["clear"])
@has_permissions(administrator=True)
async def purge(ctx: Context, amount: int):
    """
    Purges a number of messages in a channel
    """
    channel: TextChannel = ctx.channel

    await channel.purge(limit=amount)

    await sleep(3)
    await ctx.message.delete()


@bot.command(name="mute")
@has_permissions(administrator=True)
async def mute(ctx: Context, user: Member, time: int):
    guild: Guild = bot.get_guild(data.guild_id)
    muterole = guild.get_role(data.muterole_id)

    await ctx.message.delete()

    await user.add_roles(muterole)

    embed = muteembed(author=ctx.author, user=user, time=time, newtime=time)

    message: Message = await ctx.channel.send(content=user.mention, embed=embed)

    for minute in range(time):

        minute += 1

        await sleep(60)

        embed = muteembed(author=ctx.author, user=user, time=time, newtime=time-minute)

        await message.edit(embed=embed)

    await message.delete()

    await user.remove_roles(muterole)


@bot.event
async def on_member_join(guild: discord.Guild, user: discord.User):
    channel: discord.TextChannel = guild.system_channel
    embed = joinembed(user)
    await channel.send(embed=embed)


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    global channelcounter, musicchannelcounter

    try:
        if after.channel is not None and after.channel.id == data.new_channel_id:
            # if-Abfrage für den normalen Kanal

            category: discord.CategoryChannel = discord.utils.get(member.guild.categories, id=data.voice_category_id)
            channel = await category.create_voice_channel(name=f"Kanal Nr. {str(channelcounter)}")
            await member.move_to(channel)

            channelcounter += 1

        if after.channel is not None and after.channel.id == data.new_music_channel_id:
            # if-Abfrage für den Musikkanal

            category: discord.CategoryChannel = discord.utils.get(member.guild.categories, id=data.voice_category_id)
            channel = await category.create_voice_channel(name=f"Musikkanal Nr. {str(musicchannelcounter)}")
            everyone: discord.Role = discord.utils.get(member.guild.roles, name="@everyone")
            await channel.set_permissions(target=everyone, speak=False)
            await member.move_to(channel)

            musicchannelcounter += 1

        try:
            if after.channel is None and before.channel.id not in [data.new_channel_id, data.new_music_channel_id]:
                if not before.channel.members:
                    await before.channel.delete()
                    if before.channel.name.startswith("Kanal"):
                        channelcounter -= 1

                    elif before.channel.name.startswith("Musikkanal"):
                        musicchannelcounter -= 1

        except Exception as e:
            print(e)

    except Exception as e:
        print(e)


@bot.event
async def on_raw_reaction_add(ctx: discord.RawReactionActionEvent):
    if ctx.message_id == data.rolemessage_id:
        if ctx.emoji.name in data.reactions:
            color = data.reactord[ctx.emoji.name]
            guild: discord.Guild = await bot.fetch_guild(data.guild_id)
            role = discord.utils.get(guild.roles, name=color)
            member: discord.Member = await guild.fetch_member(ctx.user_id)
            await member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(reaction: discord.RawReactionActionEvent):
    if reaction.message_id == data.rolemessage_id:
        color = data.reactord[reaction.emoji.name]
        guild: discord.Guild = await bot.fetch_guild(data.guild_id)
        role = discord.utils.get(guild.roles, name=color)
        member: discord.Member = await guild.fetch_member(reaction.user_id)
        await member.remove_roles(role)


# Modkram
@bot.event
async def on_message_delete(message: discord.Message):
    if message.content:
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
async def on_message(message: Message):
    if message.author == bot.user:
        return

    for word in data.badwords:
        if word in message.content.lower():
            await message.delete()
            await message.author.send(f"Bitte verzichte darauf, solche Wörter weiterhin auf "
                                      f"**{message.guild.name}** zu verwenden!")

            logchannel: discord.TextChannel = bot.get_channel(data.logchannel_id)

            embed = badwordembed(message)
            await logchannel.send(embed=embed)

            return

        if "discord.gg" in message.content and "discord.gg/Sx2saFx" not in message.content:
            await message.delete()
            await message.author.send(f"Werbung für andere Server ist auf **{message.guild.name}** untersagt!")

            message.channel.send(embed=linkembed(message))

            return

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx: Context, error: errors.CommandError):
    if isinstance(error, errors.MissingRequiredArgument):
        await ctx.channel.send("Für deinen Befehl fehlen Argumente!")

    elif isinstance(error, errors.BadArgument):
        await ctx.channel.send("Dein Argument bzw. deine Argumente hatten einen ungültigen Wert!")

    elif isinstance(error, errors.MissingPermissions):
        await ctx.channel.send("Du hast keine Erlaubnis dazu, diesen Befehl zu verwenden!")

    else:
        print(error)

    await ctx.channel.send("Für eine Übersicht, schreibe §help")


channelcounter = 1
musicchannelcounter = 1

bot.run(tokenid)
