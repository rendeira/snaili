import os
import platform
import random
import time
from datetime import datetime

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from disnake.ext.commands import Context
from tzlocal import get_localzone_name

from classes import contas
# Apenas ative isso se o bot estiver rodando localmente
# from dotenv import load_dotenv
# load_dotenv()
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
    print("===========================")
    print(f"{nome} {versao}")
    print(f"[i] Executando o programa no {platform.system()} {platform.release()} ({os.name})")
    print(f"[i] Logado no Discord como {bot.user.name}")
    print(f"[i] Disnake {disnake.__version__}")
    print(f"[i] Python {platform.python_version()}")
    print(f"[i] Rodando no {platform.system()} {platform.release()} ({os.name})")
    status_task.start()
    print(f"[i] Logando no M$")
    try:
        contas.login()
    except:
        print("[!] Houve um erro ao fazer o login na conta da M$")
        try:
            channel = bot.get_channel(int(os.environ['text-channel-id']))
            message = await channel.fetch_message(int(os.environ['users-message-id']))
            embed = disnake.Embed(
                title="Não foi possível gerar a lista de usuários nesse momento",
                description="As crendenciais são inválidas ou os servidores estão offline, por favor contacte o adminstrador.",
                color=0x9C84EF,
            )
            await message.edit(embed=embed)
        except:
            pass
    else:
        registred_task.start()
    print("===========================")


@tasks.loop(minutes=10.0)
async def registred_task() -> None:
    try:
        now = datetime.now()
        tempo = now.strftime("%d/%m/%Y %H:%M:%S")

        embed = disnake.Embed(
            title="Usuários cadastrados",
            description="Aqui contém uma lista dos usuários que foram cadastrados dentro do bot \n" + contas.get_accounts(),
            color=0x9C84EF,
        )
        embed.set_footer(
            text="\nAtualizado em " + tempo + " (Fuso horário: " + get_localzone_name() + ")"
        )
        channel = bot.get_channel(int(os.environ['text-channel-id']))
        message = await channel.fetch_message(int(os.environ['users-message-id']))
        await message.edit(embed=embed)
    except:
        print("[i] Algo deu errado ao pegar a lista de usuários.")


@tasks.loop(minutes=1.0)
async def status_task() -> None:
    channel = bot.get_channel(int(os.environ['voice-channel-id']))
    uptime = time.time() - tempo_inicial
    hours = uptime / 60 / 60
    minutes = uptime / 60
    seconds = uptime
    tempo = f"{f'{round(hours)} h' if round(hours) > 0 else ''} {f'{round(minutes)} min' if round(minutes) > 0 and round(hours) <= 0 else ''} {f'{round(seconds)} s' if round(seconds) > 0 and round(minutes) <= 0 and round(hours) <= 0 else ''}"
    await channel.edit(name=f"Bot ativo por {tempo}")
    print(f"[i] Bot ativo por {tempo} (Tempo em segundos: {uptime})")
    await bot.change_presence(activity=disnake.Game(f"{nome} {versao}"))


def load_commands(command_type: str) -> None:
    for file in os.listdir(f"./extensoes/{command_type}"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"extensoes.{command_type}.{extension}")
                print(f"[i] Extensao carregada '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"[!] Falha ao carregar extensao {extension}\n{exception}")


if __name__ == "__main__":
    load_commands("slash")


@bot.event
async def on_message(message: disnake.Message) -> None:
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_member_join(person):
    await person.add_roles(disnake.utils.get(person.guild.roles, name="Membro"))
    await person.add_roles(disnake.utils.get(person.guild.roles, name="Peixe"))


@bot.event
async def on_slash_command(interaction: ApplicationCommandInteraction) -> None:
    print(
        f"[i] Comando {interaction.data.name} em {interaction.guild.name} executado com sucesso (ID: {interaction.guild.id}) por {interaction.author} (ID: {interaction.author.id})")


@bot.event
async def on_slash_command_error(interaction: ApplicationCommandInteraction, error: Exception) -> None:
    if isinstance(error, commands.errors.MissingPermissions):
        embed = disnake.Embed(
            title="Erro",
            description="Falta as permissões `" + ", ".join(
                error.missing_permissions) + "` para executar esse comando!",
            color=0xE02B2B
        )
        return await interaction.send(embed=embed, ephemeral=True)
    else:
        embed = disnake.Embed(
            title="Erro",
            description=str(error),
            color=0xE02B2B
        )
        return await interaction.send(embed=embed, ephemeral=True)


@bot.event
async def on_command_completion(context: Context) -> None:
    # Quando um comando normal for executado
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    print(
        f"[i] Comando {executed_command} em {context.guild.name} executado com sucesso (ID: {context.message.guild.id}) por {context.message.author} (ID: {context.message.author.id})")


@bot.event
async def on_command_error(context: Context, error) -> None:
    # Quando um comando normal deu erro
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = disnake.Embed(
            title="Ei, por favor se acalme",
            description=f"Você pode executar o comando dnv em {f'{round(hours)} horas' if round(hours) > 0 else ''} {f'{round(minutes)} minutos' if round(minutes) > 0 else ''} {f'{round(seconds)} segundos' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = disnake.Embed(
            title="Erro!",
            description="Falta as permissões  `" + ", ".join(
                error.missing_permissions) + "` para executar esse comando",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = disnake.Embed(
            title="Erro!",
            # We need to capitalize because the command arguments have no capital letter in the code.
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error


# Rode o comando
bot.run(os.environ["token"])
