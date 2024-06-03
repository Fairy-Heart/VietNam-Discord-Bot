from discord.ext import commands
import discord
from discord import app_commands
import datetime

class Rename(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = 'rename',
        description = 'Đổi tên một thành viên trong server'
    )
    @app_commands.default_permissions(change_nickname = True)
    @app_commands.describe(
        member = 'Người dùng bạn muốn đổi nickname của họ',
        new_name = 'Nickname mới bạn muốn đổi',
        reason = 'Lí do (nếu có)'
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def rename(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        new_name: app_commands.Range[str, 1, 32],
        reason: str = f'Không đề cập lí do'
    ):
        bot_member = interaction.guild.get_member(self.bot.user.id)

        if member.id == interaction.guild.owner_id:
            embed = discord.Embed (
                title = 'Lỗi',
                description = '* Bot không thể đổi tên của owner server',
                color = 0x407b04,
                timestamp = datetime.datetime.now()
            )
            await interaction.response.send_message(embed = embed)
            return False
        
        if member.top_role >= interaction.user.top_role and interaction.guild.owner_id != interaction.user.id:
            embed = discord.Embed(
                title = 'Lỗi',
                description = 'Bạn không thể đổi tên người có vai trò cao hơn bản thân',
                color = 0x407b04,
                timestamp = datetime.datetime.now()
            )
            await interaction.response.send_message(embed = embed)
            return False
        
        if bot_member.top_role <= member.top_role:
            embed = discord.Embed(
                title = 'Lỗi',
                description = 'Vai trò của bot thấp hơn vai trò của người bạn muốn đổi nickname',
                color = 0x407b04,
                timestamp = datetime.datetime.now()
            )
            await interaction.response.send_message(embed = embed)
            return False
        
        await member.edit(
            nick = new_name,
            reason = f'{reason} | Thực hiện bởi {interaction.user.name}'
        )
        embed = discord.Embed(
            description = f'* Đổi nickname của {member.name} thành công\n* Lí do đổi : {reason}',
            color = 0x04eefb,
            timestamp = datetime.datetime.now()
        )
        await interaction.response.defer()
        await interaction.followup.send(embed = embed)
    

async def setup(bot):
    await bot.add_cog(Rename(bot))