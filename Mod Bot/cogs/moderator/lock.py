from discord.ext import commands
import discord
from discord import app_commands
import datetime


class Lock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = 'lock',
        description = 'Lock 1 kênh văn bản trong server'
    )
    @app_commands.default_permissions(manage_channels = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @app_commands.describe(
        channel= 'Kênh bạn muốn lock',
        reason = 'Lí do (nếu có)'
    )
    async def lock(
        self,
        interaction: discord.Integration,
        channel: discord.TextChannel,
        reason: str = 'Không đề cập lí do'
    ):
        if not interaction.guild:
            return False
        
        bot_user = interaction.guild.get_member(self.bot.user.id)

        if not bot_user.guild_permissions.manage_channels:
            embed = discord.Embed(
                title = 'Lỗi',
                description = '* Bot thiếu quyền hạn `manage_channels` để thực hiện lệnh này !',
                timestamp = datetime.datetime.now(),
                color = 0xff0000
            )
            await interaction.response.send_message(embed = embed)
            return False

        everyone_role = interaction.guild.default_role
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False

        await interaction.response.defer()
        await channel.set_permissions(
            target = everyone_role,
            overwrite = overwrite,
            reason = f'{reason} | Thực hiện bởi {interaction.user.name}'
        )
        embed = discord.Embed(
            description = f'* Lockdown kênh {channel.name} thành công\n* Lí do : {reason}',
            color = 0x00ffff,
            timestamp = datetime.datetime.now()
        )
        await interaction.followup.send(embed = embed)


async def setup(bot):
    await bot.add_cog(Lock(bot))