from discord import Embed, User, Guild, Message
from data import avatar_url, repository_url, color, version, features, servericon_url, loc_mention


def infoembed():
    embed = Embed(title="LoCBot",
                  description="Ein Discordbot für den NorthDiscord-Discordserver von LoC",
                  color=color,
                  url=repository_url)
    embed.set_thumbnail(url=avatar_url)
    embed.add_field(name="Features", value="\n".join(f"- {feature}" for feature in features), inline=False)
    embed.add_field(name="Version", value=version, inline=True)
    embed.add_field(name="GitHub", value=repository_url, inline=False)
    embed.add_field(name="Help-Befehl", value="§help", inline=False)
    embed.add_field(name="Entwickler", value=f"Dieser Discordbot wird von {loc_mention} entwickelt! Bitte teile mir "
                                             f"Fehler oder Featurewünsche auf meinem Discordserver, per PN oder auf "
                                             f"der Issue-Seite des Github-Repositories des Bots mit!", inline=False)

    return embed


def joinembed(user: User):
    embed = Embed(title="Nezugang",
                  description="Eine neue Person hat den Weg auf diesen Server gefunden. Herzlich Willkommen!",
                  color=color,
                  url="https://discord.gg/Sx2saFx")
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Name", value=user.mention, inline=True)
    embed.add_field(name="Auf Discord seit", value=user.created_at.strftime("%d.%m.%Y"))
    embed.set_footer(text="Du kannst Freunde über den Link https://discord.gg/Sx2saFx auf diesen Server einladen!",
                     icon_url=servericon_url)

    return embed


def serverinfoembed(guild: Guild):
    embed = Embed(title="NorthDiscord",
                  description="Dies ist der offizielle Discordserver von LoC",
                  color=color,
                  url="https://discord.gg/Sx2saFx")
    embed.set_thumbnail(url=servericon_url)
    embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
    embed.add_field(name="Erstellungsdatum", value=guild.created_at.strftime("%d.%m.%Y"), inline=True)
    embed.add_field(name="Members", value=guild.member_count, inline=True)
    embed.add_field(name="Rollen", value=str(len(guild.roles)), inline=True)
    embed.add_field(name="Invitelink", value="https://discord.gg/Sx2saFx", inline=True)

    embed.set_footer(text="Lade deine Freunde zu diesem Server ein, um ihn noch großartiger zu machen!",
                     icon_url=avatar_url)

    return embed


def deleteembed(message: Message):
    embed = Embed(title="Nachricht gelöscht",
                  description=f"Eine Nachricht von {message.author.mention} "
                              f"wurde in {message.channel.mention} gelöscht",
                  color=color,
                  url=message.jump_url)
    embed.set_author(name=message.author.name, url="https://discord.gg/Sx2saFx", icon_url=message.author.avatar_url)
    embed.add_field(name="Inhalt der Nachricht", value=message.content, inline=False)
    if message.mentions:
        print(message.mentions)
        embed.add_field(name="Erwähnungen", value="\n".join(f"- {mention}" for mention in message.mentions))
    embed.set_footer(text=f"ID: {message.id}", icon_url=servericon_url)

    return embed


def editembed(before: Message, after: Message):
    embed = Embed(title="Nachricht bearbeitet",
                  description=f"Eine Nachricht von {before.author.mention} "
                              f"wurde in {before.channel.mention} bearbeitet",
                  color=color,
                  url=after.jump_url)
    embed.set_author(name=after.author.name, url="https://discord.gg/Sx2saFx", icon_url=after.author.avatar_url)
    embed.add_field(name="Vorherige Nachricht", value=before.content, inline=False)
    embed.add_field(name="Nachricht nach Bearbeitung", value=after.content, inline=False)
    embed.set_footer(text=f"ID: {after.id}", icon_url=servericon_url)

    return embed