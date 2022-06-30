import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands


class Moderation(commands.Cog, name="moderacao-slash"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="kick",
        description="Kickar um usuário pra fora do servidor",
        options=[
            Option(
                name="usuario",
                description="O usuário que você queira kickar.",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="motivo",
                description="O motivo que você queira kickar o usuario",
                type=OptionType.string,
                required=False
            )
        ]
    )
    @commands.has_permissions(kick_members=True)
    async def kick(self, interaction: ApplicationCommandInteraction, usuario: disnake.User,
                   motivo: str = "Não especificado") -> None:
        member = await interaction.guild.get_or_fetch_member(usuario.id)
        if member.guild_permissions.administrator:
            embed = disnake.Embed(
                title="Erro!",
                description="Você está tentando kickar um admininstrador",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)
        else:
            try:
                embed = disnake.Embed(
                    title="Usuario chutado!",
                    description=f"**{member}** foi kickado por **{interaction.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Motivo:",
                    value=motivo
                )
                await interaction.send(embed=embed)
                try:
                    await member.send(
                        f"Voce foi kickado por **{interaction.author}**!\nmotivo: {motivo}"
                    )
                except disnake.Forbidden:
                    # Couldn't send a message in the private messages of the usuario
                    pass
                await member.kick(reason=motivo)
            except:
                embed = disnake.Embed(
                    title="Erro!",
                    description="Erro ao kickar o usuário",
                    color=0xE02B2B
                )
                await interaction.send(embed=embed)

    @commands.slash_command(
        name="nick",
        description="Mudar o nick de qualquer usuário",
        options=[
            Option(
                name="usuario",
                description="O usuario que voce deseja mudar o nick",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="nickname",
                description="O novo nome de usuário",
                type=OptionType.string,
                required=False
            )
        ],
    )
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, interaction: ApplicationCommandInteraction, usuario: disnake.User,
                   nickname: str = None) -> None:
        member = await interaction.guild.get_or_fetch_member(usuario.id)
        try:
            await member.edit(nick=nickname)
            embed = disnake.Embed(
                title="Nickname mudado!",
                description=f"**{member}'s** novo nome de usuário é **{nickname}**!",
                color=0x9C84EF
            )
            await interaction.send(embed=embed)
        except:
            embed = disnake.Embed(
                title="Erro!",
                description="Erro ao mudar o nome de usuário. Verifique se meu cargo está acima do seu",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)

    @commands.slash_command(
        name="ban",
        description="Banir o usuário do server",
        options=[
            Option(
                name="user",
                description="O usuario que voce quer banir",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="motivo",
                description="Motivo no qual vice baniu o usuario",
                type=OptionType.string,
                required=False
            )
        ],
    )
    @commands.has_permissions(ban_members=True)
    async def ban(self, interaction: ApplicationCommandInteraction, user: disnake.User,
                  motivo: str = "Nao especificado") -> None:
        member = await interaction.guild.get_or_fetch_member(user.id)
        try:
            if member.guild_permissions.administrator:
                embed = disnake.Embed(
                    title="Erro",
                    description="Usuario no qual voce quer banir tem permissões de admininstrador",
                    color=0xE02B2B
                )
                await interaction.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Usuario banido",
                    description=f"**{member}** foi banido por **{interaction.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Motivo:",
                    value=motivo
                )
                await interaction.send(embed=embed)
                try:
                    await member.send(f"Você foi banido por **{interaction.author}**!\nMotivo: {motivo}")
                except disnake.Forbidden:
                    # Couldn't send a message in the private messages of the user
                    pass
                await member.ban(reason=motivo)
        except:
            embed = disnake.Embed(
                title="Error!",
                description="Erro ocorrido ao banir usuário",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)

    @commands.slash_command(
        name="aviso",
        description="Avisa o usuário",
        options=[
            Option(
                name="usuario",
                description="O usuário no qual você quer avisar",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="motivo",
                description="O motivo no qual você quer enviar o aviso",
                type=OptionType.string,
                required=False
            )
        ],
    )
    @commands.has_permissions(manage_messages=True)
    async def aviso(self, interaction: ApplicationCommandInteraction, usuario: disnake.User,
                    motivo: str = "Não foi especificado") -> None:
        member = await interaction.guild.get_or_fetch_member(usuario.id)
        embed = disnake.Embed(
            title="Usuário foi avisado",
            description=f"**{member}** foi avisado por **{interaction.author}**!",
            color=0x9C84EF
        )
        embed.add_field(
            name="Motivo:",
            value=motivo
        )
        await interaction.send(embed=embed)
        try:
            await member.send(f"Você foi avisado por **{interaction.author}**!\nMotivo: {motivo}")
        except disnake.Forbidden:
            await interaction.send(
                f"{member.mention}, você foi avisado por **{interaction.author}**!\nMotivo: {motivo}")

    @commands.slash_command(
        name="limpar",
        description="Limpa uma quantidade de mensagens",
        options=[
            Option(
                name="quantidade",
                description="A quantidade de mensagens que deve ser limpada (número de 1 a 100)",
                type=OptionType.integer,
                required=True,
                min_value=1,
                max_value=100
            )
        ],
    )
    @commands.has_guild_permissions(manage_messages=True)
    async def limpar(self, interaction: ApplicationCommandInteraction, quantidade: int) -> None:
        limpard_messages = await interaction.channel.purge(limit=quantidade)
        embed = disnake.Embed(
            title="Chat limpo!",
            description=f"**{interaction.author}** limpou **{len(limpard_messages)}** mensagens!",
            color=0x9C84EF
        )
        await interaction.send(embed=embed)

    @commands.slash_command(
        name="hackban",
        description="Bane um usuário mesmo se ele não estiver no server",
        options=[
            Option(
                name="usuario_id",
                description="ID do usuário que deve ser banido",
                type=OptionType.string,
                required=True
            ),
            Option(
                name="motivo",
                description="motivo no qual voce baniu o usuário",
                type=OptionType.string,
                required=False
            )
        ]
    )
    @commands.has_permissions(ban_members=True)
    async def hackban(self, interaction: ApplicationCommandInteraction, usuario_id: str,
                      motivo: str = "Não foi especificado") -> None:
        try:
            await self.bot.http.ban(usuario_id, interaction.guild.id, reason=motivo)
            user = await self.bot.get_or_fetch_user(int(usuario_id))
            embed = disnake.Embed(
                title="Usuário banido!",
                description=f"**{user} (ID: {usuario_id}) ** foi banido por  **{interaction.author}**!",
                color=0x9C84EF
            )
            embed.add_field(
                name="Motivo:",
                value=motivo
            )
            await interaction.send(embed=embed)
        except Exception as e:
            embed = disnake.Embed(
                title="Erro",
                description="Erro ao banir usuário.",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)
            print(e)

    @commands.slash_command(
        name="mutar",
        description="Muta ou desmuta o usuário",
        options=[
            Option(
                name="user",
                description="O usuario que voce quer mutar",
                type=OptionType.user,
                required=True
            ),
            Option(
                name="motivo",
                description="Motivo no qual voce mutou o usuario",
                type=OptionType.string,
                required=False
            )
        ]
    )
    @commands.has_permissions(ban_members=True)
    async def mutar(self, interaction: ApplicationCommandInteraction, user: disnake.User,
                    motivo: str = "Não especificado") -> None:
        member = await interaction.guild.get_or_fetch_member(user.id)
        try:
            if member.guild_permissions.administrator:
                embed = disnake.Embed(
                    title="Erro",
                    description="Usuario no qual voce quer mutar tem permissões de admininstrador",
                    color=0xE02B2B
                )
                await interaction.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Usuario mutado",
                    description=f"**{member}** foi mutado por **{interaction.author}**!",
                    color=0x9C84EF
                )
                embed.add_field(
                    name="Motivo:",
                    value=motivo
                )
                await interaction.send(embed=embed)
                try:
                    await member.send(f"Você foi mutado por **{interaction.author}**!\nMotivo: {motivo}")
                except disnake.Forbidden:
                    pass
                role = await disnake.utils.get(interaction.author.guild.roles, name="Mutado")
                await member.add_roles(role)
        except:
            embed = disnake.Embed(
                title="Erro!",
                description="Um erro foi ocorrido ao mutar",
                color=0xE02B2B
            )
            await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
