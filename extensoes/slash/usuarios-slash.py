import json
import os

import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands

from classes import contas
from classes.linguagem import lang


class usuarios(commands.Cog, name="usuarios-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name=lang['cmd-create'],
        description=lang['cmd-create-desc'],
        options=[
            Option(

                name=lang['cmd-name'],
                description=lang['cmd-name-desc'],
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
            raise Exception(lang['ms-role-error'])

        roles_user_has = []
        for role in interaction.author.roles:
            roles_user_has.append(str(role))

        if lang['ms-role'] in roles_user_has:
            password = contas.random_password()
            await interaction.response.send_message(lang['creating-user'], ephemeral=True)
            user = '{ "accountEnabled": true, "displayName": "' + nome + \
                   '", "mailNickname": "' + nome + '","userPrincipalName": "' + nome + \
                   os.environ["ms-email"] + '", ' \
                                            '"passwordProfile": { "forceChangePasswordNextSignIn": true, "password": "' \
                   + password + '" }}'
            response = contas.client.post("/users", json=json.loads(user))
            json_data = response.json()
            if 'error' in json_data:
                error = json_data['error']
                await interaction.edit_original_message(" " + error['message'])
            else:
                await interaction.author.remove_roles(
                    disnake.utils.get(interaction.author.guild.roles, name=lang['ms-role']))
                embed = disnake.Embed(
                    description=f"{nome}",
                    color=0x9C84EF,
                )
                embed.set_author(
                    name=lang['cmd-name-desc']
                )
                embed.add_field(
                    name="Email",
                    value=f"{nome}{os.environ['ms-email']}",
                    inline=False
                )
                embed.add_field(
                    name=lang['temp-pass'],
                    value=f"{password}",
                    inline=False
                )
                await interaction.edit_original_message(lang['user-created'], embed=embed)
        else:
            await interaction.response.send_message(
                lang['ms-role-error'],
                ephemeral=True)


def setup(bot):
    bot.add_cog(usuarios(bot))
