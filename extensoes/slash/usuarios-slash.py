import json
import os

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

from classes import contas


class usuarios(commands.Cog, name="usuarios-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="criar",
        description="Comando só pode ser utilizado uma vez",
        options=[
            Option(
                name="nome",
                description="nome do usuário",
                type=OptionType.string,
                required=False
            )
        ]
    )
    async def criar(self, interaction: ApplicationCommandInteraction, nome: str):
        """
        Cria um usuário
        """
        if interaction.guild.id != int(os.environ['guild-id']):
            raise Exception("Esse comando está indisponível no momento, tente mais tarde.")

        roles_user_has = []
        for role in interaction.author.roles:
            roles_user_has.append(str(role))

        if ("Peixe") in roles_user_has:
            password = contas.random_password()
            await interaction.response.send_message("Criando usuário...", ephemeral=True)
            user = '{ "accountEnabled": true, "displayName": "' + nome + '", "mailNickname": "' + nome + '","userPrincipalName": "' + nome + \
                   os.environ[
                       "ms-email"] + '", "passwordProfile": { "forceChangePasswordNextSignIn": true, "password": "' + password + '" }}'
            response = contas.client.post("/users", json=json.loads(user))
            json_data = response.json()
            if 'error' in json_data:
                error = json_data['error']
                await interaction.edit_original_message("Erro: " + error['message'])
            else:
                await interaction.author.remove_roles(disnake.utils.get(interaction.author.guild.roles, name="Peixe"))
                embed = disnake.Embed(
                    description=f"{nome}",
                    color=0x9C84EF,
                )
                embed.set_author(
                    name="Nome de usuário"
                )
                embed.add_field(
                    name="Email",
                    value=f"{nome}@sexosexo.onmicrosoft.com",
                    inline=False
                )
                embed.add_field(
                    name="Senha temporária",
                    value=f"{password}",
                    inline=False
                )
                await interaction.edit_original_message("Usuário criado com sucesso!", embed=embed)
        else:
            await interaction.response.send_message(
                "Você não tem o cargo necessário para completar a ação. \nLembre-se: para evitar spam, você só pode pedir uma conta uma vez",
                ephemeral=True)


def setup(bot):
    bot.add_cog(usuarios(bot))
