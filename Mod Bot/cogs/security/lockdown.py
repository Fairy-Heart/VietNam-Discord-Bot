from discord.ext import commands
import discord
from discord import app_commands
import datetime
import asyncio

class Lockdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = 'lockdown',
        description = 'Lockdown toàn bộ kênh văn bản trong server'
    )
    @app_commands.default_permissions(administrator = True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    @app_commands.describe(
        reason = 'Lí do lockdown server'
    )
    async def lockdown(
        self,
        interaction: discord.Integration,
        reason: str = 'Không đề cập lí do'
    ):
        bot_id = interaction.guild.get_member(self.bot.user.id)

        if not interaction.guild:
            return False

        if not bot_id.guild_permissions.administrator:
            embed = discord.embed (
                title = 'Lỗi',
                description = '* Bot yêu cầu quyền `Administrator` để thực hiện lệnh này',
                color = 0xff0000,
                timestamp = datetime.datetime.now()
            )
            await interaction.response.send(embed = embed)
            return False

        everyone_role = interaction.guild.default_role
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False


        await interaction.response.defer()
        for channel_list in interaction.guild.text_channels:
             await channel_list.set_permissions(
                everyone_role,
                overwrite = overwrite,
                reason = f'{reason} | Thực hiện bởi {interaction.user.name}'
            )
        
        text_channel_count  = len(interaction.guild.text_channels)
        embed = discord.Embed (
                description = f'* Lockdown `{text_channel_count}` text channel trong server \n Lí do lockdown : {reason}',
                color = 0x00ffff,
                timestamp = datetime.datetime.now()
            )
        await interaction.followup.send(embed = embed)
                    

async def setup(bot):
    await bot.add_cog(Lockdown(bot))