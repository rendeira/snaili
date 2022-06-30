import os
import platform

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from complemento import versao, nome, url, descricao


class General(commands.Cog, name="geral-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="botinfo",
        description="Informações sobre o bot.",
    )
    async def botinfo(self, interaction: ApplicationCommandInteraction) -> None:
        embed = disnake.Embed(
            description=f"{descricao}",
            color=0x9C84EF
        )

        embed.set_author(
            name=f"{nome} {versao}"
        )
        embed.add_field(
            name="Plataforma",
            value=f"Python {platform.python_version()}\n  {platform.system()} {platform.release()} ({os.name})",
            inline=True
        )
        embed.add_field(
            name="Prefixo:",
            value=f"/ (Slash) ou {os.environ['prefix']}",
            inline=False
        )
        embed.add_field(
            name="Site oficial",
            value=f"{url}",
            inline=False
        )
        await interaction.send(embed=embed)

    @commands.slash_command(
        name="serverinfo",
        description="Informações sobre o servidor.",
    )
    async def serverinfo(self, interaction: ApplicationCommandInteraction) -> None:
        roles = [role.name for role in interaction.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Mostrando[50/{len(roles)}] Cargos")
        roles = ", ".join(roles)

        embed = disnake.Embed(
            title="**Nome do servidor:**",
            description=f"{interaction.guild}",
            color=0x9C84EF
        )
        embed.set_thumbnail(
            url=interaction.guild.icon.url
        )
        embed.add_field(
            name="ID do servidor:",
            value=interaction.guild.id
        )
        embed.add_field(
            name="Quantidade de membros:",
            value=interaction.guild.member_count
        )
        embed.add_field(
            name="Canais de texto/voz:",
            value=f"{len(interaction.guild.channels)}"
        )
        embed.add_field(
            name=f"Cargos ({len(interaction.guild.roles)})",
            value=roles
        )
        embed.set_footer(
            text=f"Foi criado em {interaction.guild.created_at}"
        )
        await interaction.send(embed=embed)

    @commands.slash_command(
        name="ping",
        description="Verifica se o bot ainda está vivo.",
    )
    async def ping(self, interaction: ApplicationCommandInteraction) -> None:
        embed = disnake.Embed(
            title="🏓 Pong!",
            description=f"Latência: {round(self.bot.latency * 1000)}ms.",
            color=0x9C84EF
        )
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
