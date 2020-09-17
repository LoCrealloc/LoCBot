from discord.ext.commands import Bot, errors, Context
import discord.utils
from discord import Message, Game, TextChannel, Member
import data
from tokenid import tokenid
from embedcreator import joinembed, deleteembed, editembed, badwordembed, linkembed
from cogs.administration import Administration
from cogs.information import Information
from util import add_cogs

bot = Bot(command_prefix="§", case_insensitive=True)


@bot.event
async def on_ready():
    activity = Game(name="§info")

    await bot.change_presence(activity=activity, status=discord.Status.online)

    channel: TextChannel = bot.get_channel(data.rolechannel_id)

    message: Message = await channel.fetch_message(data.rolemessage_id)

    for i in data.reactions:
        await message.add_reaction(i)

    print("Bot has logged in succesfully")


@bot.event
async def on_member_join(member: Member):
    channel: discord.TextChannel = member.guild.system_channel
    embed = joinembed(member)
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
async def on_raw_reaction_add(reaction: discord.RawReactionActionEvent):
    if reaction.message_id == data.rolemessage_id:
        if reaction.emoji.name in data.reactions:
            try:
                color = data.reactord[reaction.emoji.name]
            except KeyError:
                channel = bot.get_channel(reaction.channel_id)
                message = await channel.fetch_message(reaction.message_id)
                await message.remove_reaction(reaction.emoji.name)
            guild: discord.Guild = await bot.fetch_guild(data.guild_id)
            role = discord.utils.get(guild.roles, name=color)
            member: discord.Member = await guild.fetch_member(reaction.user_id)
            await member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(reaction: discord.RawReactionActionEvent):
    if reaction.message_id == data.rolemessage_id:
        try:
            color = data.reactord[reaction.emoji.name]
        except KeyError:
            return
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

            await message.channel.send(embed=linkembed(message))

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

    elif isinstance(error, errors.CommandNotFound):
        await ctx.channel.send("Dieser Befehl konnte nicht gefunden werden!")

    else:
        print(error)

    await ctx.channel.send("Für eine Übersicht, schreibe §help")


channelcounter = 1
musicchannelcounter = 1

add_cogs(bot, [Administration, Information])

bot.run(tokenid)
