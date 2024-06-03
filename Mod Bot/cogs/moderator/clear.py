from discord.ext import commands
import discord
import datetime
from discord import app_commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = 'clear',
        description = 'Clear tin nhắn'
    )
    @app_commands.default_permissions(
        manage_messages = True
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @app_commands.describe(
        amount = 'Nhập số lượng tin nhắn bạn muốn clear',
        reason = 'Nhập lí do (nếu có)'
    )
    async def clear(
        self,
        interaction: discord.Interaction,
        amount: app_commands.Range[int, 2, 100,],
        reason: str = 'Không đề cập lí do'
    ):
        
        embed = discord.Embed(
            description = f'* Clear`{amount}` tin nhắn thành công !',
            color = 0x00ffd9,
            timestamp = datetime.datetime.now()
        )
        await interaction.response.defer()
        await interaction.followup.send(embed = embed)

        await interaction.channel.purge(
            limit = amount,
            reason = f'{reason} | Thực hiện bởi {interaction.user.name}'
        )
        


async def setup(bot):
    await bot.add_cog(Clear(bot))