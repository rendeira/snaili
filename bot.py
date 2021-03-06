import os
import platform
import time
from datetime import datetime

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from tzlocal import get_localzone_name

"""
.env template

language=en
token=token_do_discord
prefix=/
text-channel-id=914152523523512604
users-message-id=23523562673737712
voice-channel-id=8584726352352510
guild-id=991014224975257670
ms-login=SIM
ms-email=@gmail.com
ms-client-id=13214214-43242ji432-324-4323
ms-admin-email=admin@microsoft.com
ms-admin-password=1234slaoq

Code:

from dotenv import load_dotenv
# load_dotenv()
"""

from classes import contas
from classes.linguagem import lang

from complemento import nome, versao

tempo_inicial = time.time()
intents = disnake.Intents.default()

intents.bans = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True
intents.emojis = True
intents.emojis_and_stickers = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_scheduled_events = True
intents.guild_typing = True
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.messages = True
intents.reactions = True
intents.typing = True
intents.voice_states = True
intents.webhooks = True
intents.members = True
intents.message_content = True
intents.presences = True
intents.message_content = True

bot = Bot(command_prefix=commands.when_mentioned_or(os.environ["prefix"]), intents=intents, help_command=None)
bot.config = os.environ


@bot.event
async def on_ready() -> None:
    print(lang['separator'])
    print(f"{nome} {versao}")
    print(f"{lang['info-icon']} {lang['running-as']} {platform.system()} {platform.release()} ({os.name})")
    print(f"{lang['info-icon']} {lang['logged-dc']} {bot.user.name}")
    print(f"{lang['info-icon']} Disnake {disnake.__version__}")
    print(f"{lang['info-icon']} Python {platform.python_version()}")
    guild = bot.get_guild(int(os.environ['guild-id']))
    status_task.start()
    if guild is not None:
        print(f"{lang['info-icon']} {lang['login-ms']}")
        try:
            contas.login()
        except Exception as e:
            print(f"{lang['alert-icon']} {lang['there-was-an-error-ms']} ({e})")
            try:
                channel = guild.get_channel(int(os.environ['text-channel-id']))
                message = await channel.fetch_message(int(os.environ['users-message-id']))
                embed = disnake.Embed(
                    title=f"{lang['not-possible-title-ms']}",
                    description=f"{lang['not-possible-desc-ms']}",
                    color=0x9C84EF,
                )
                await message.edit(embed=embed)
            except:
                pass
        else:
            registred_task.start()
    print(lang['separator'])


@tasks.loop(minutes=10.0)
async def registred_task() -> None:
    try:
        now = datetime.now()
        tempo = now.strftime("%d/%m/%Y %H:%M:%S")
        guild = bot.get_guild(int(os.environ['guild-id']))
        embed = disnake.Embed(
            title=f"{lang['registred-users-title']}",
            description=f"{lang['registred-users-desc']} \n" + contas.get_accounts(),
            color=0x9C84EF,
        )
        embed.set_footer(
            text=f"\n{lang['updated']} " + tempo + f" ({lang['timezone']}: " + get_localzone_name() + ")"
        )
        channel = guild.get_channel(int(os.environ['text-channel-id']))
        message = await channel.fetch_message(int(os.environ['users-message-id']))
        await message.edit(embed=embed)
    except:
        print(f"{lang['error-icon']} {lang['there-was-an-error-ul']}")


@tasks.loop(minutes=1.0)
async def status_task() -> None:
    guild = bot.get_guild(int(os.environ['guild-id']))
    channel = guild.get_channel(int(os.environ['voice-channel-id']))
    uptime = time.time() - tempo_inicial
    hours = uptime / 60 / 60
    minutes = uptime / 60
    seconds = uptime
    tempo = f"{f'{round(hours)} h' if round(hours) > 0 else ''} {f'{round(minutes)} min' if round(minutes) > 0 and round(hours) <= 0 else ''} {f'{round(seconds)} s' if round(seconds) > 0 and round(minutes) <= 0 and round(hours) <= 0 else ''}"
    await channel.edit(name=f"{lang['active-time']} {tempo}")
    print(f"{lang['info-icon']} {lang['active-time']} {tempo} ({uptime}s)")
    await bot.change_presence(activity=disnake.Game(f"{nome} {versao}"))


def load_commands(command_type: str) -> None:
    for file in os.listdir(f"./extensoes/{command_type}"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"extensoes.{command_type}.{extension}")
                print(f"{lang['info-icon']} {lang['loaded-extension']} '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"{lang['info-icon']} {lang['error-extension']} {extension}\n{exception}")


if __name__ == "__main__":
    load_commands("slash")


@bot.event
async def on_message(message: disnake.Message) -> None:
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_slash_command(interaction: ApplicationCommandInteraction) -> None:
    print(
        f"{lang['info-icon']} {lang['command']} {interaction.data.name} {lang['in']} {interaction.guild.name} {lang['success-run']} (ID: {interaction.guild.id}) {lang['by']} {interaction.author} (ID: {interaction.author.id})")


@bot.event
async def on_slash_command_error(interaction: ApplicationCommandInteraction, error: Exception) -> None:
    if isinstance(error, commands.errors.MissingPermissions):
        embed = disnake.Embed(
            title=f"{lang['error']}",
            description=f"{lang['missing-permissions']} `" + ", ".join(
                error.missing_permissions) + "`",
            color=0xE02B2B
        )
        return await interaction.send(embed=embed, ephemeral=True)
    else:
        embed = disnake.Embed(
            title=lang['error'],
            description=str(error),
            color=0xE02B2B
        )
        return await interaction.send(embed=embed, ephemeral=True)


bot.run(os.environ["token"])
