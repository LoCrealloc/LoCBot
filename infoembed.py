from discord import Embed
from data import avatar_url, repository_url, color, version, features


def create_embed():
    embed = Embed(title="LoCBot",
                  description="Ein Discordbot für den NorthDiscord-Discordserver von LoC",
                  color=color,
                  url=repository_url)
    embed.set_thumbnail(url=avatar_url)
    embed.add_field(name="Features", value="\n".join(f"- {feature}" for feature in features), inline=False)
    embed.add_field(name="Version", value=version, inline=True)
    embed.add_field(name="GitHub", value=repository_url, inline=False)
    embed.add_field(name="Entwickler", value="Dieser Discordbot wird von LoC entwickelt! Bitte teile mir Fehler oder"
                                             "Featurewünsche auf meinem Discordserver, per PN oder auf der Issue-Seite"
                                             "des Github-Repositories des Bots mit!")

    return embed
