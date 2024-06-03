from discord.ext import commands
from discord import app_commands
import discord
import datetime


class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = 'ban',
        description = 'cấm một người dùng khỏi máy chủ'
    )
    @app_commands.describe(
        member = 'Người dùng bạn muốn cấm',
        reason = 'Lí do cấm (nếu có)',
        delete_day = 'Xóa tin nhắn trong bao nhiêu ngày, chọn 0 nếu không muốn xóa'
    )
    @app_commands.default_permissions(ban_members = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        delete_day: app_commands.Range[int, 0, 7],
        reason: str = 'Không đề cập lí do'
    ):
        bot_member = interaction.guild.get_member(self.bot.user.id)

        if member.id == bot_member.id:
            embed = discord.Embed (
                title = 'Lỗi',
                description = '* Bot không thể tự cấm chính mình !',
                color = 0xf0800f,
                timestamp = datetime.datetime.now()
            )
            await interaction.response.send_message(embed = embed)
            return False
        
        if member.id == interaction.user.id:
            embed = discord.Embed (
                title = 'Lỗi',
                description = '* Bạn không thể tự cấm chính mình !',
                color = 0xf0800f,
                timestamp = datetime.datetime.now()
            )
            await interaction.response.send_message(embed = embed)
            return False


        if member.id == interaction.guild.owner_id:
            embed = discord.Embed (
                title = 'Lỗi',
                description = '* Bạn không thể cấm owner server !',
                color = 0xf0800f,
                timestamp = datetime.datetime.now()
            )
            await interaction.response.send_message(embed = embed)
            return False
        
        
        if member.top_role >= bot_member.top_role:
            embed = discord.Embed (
                title = 'Lỗi',
                description = '* Vai trò của bot thấp hơn người bạn muốn cấm',
                color = 0xf0800f,
                timestamp = datetime.datetime.now()
            )
            await interaction.response.send_message(embed = embed)
            return False
        
        if member.top_role >= interaction.user.top_role and interaction.user.id != interaction.guild.owner_id:
            embed = discord.Embed (
                title = 'Lỗi',
                description = '* Bạn không thể cấm người có vai trò cao hơn bản thân',
                color = 0xf0800f,
                timestamp = datetime.datetime.now()
            )
            await interaction.response.send_message(embed = embed)
            return False
        

        await member.ban(
            delete_message_days = delete_day,
            reason = f'{reason} | Thực hiện bởi {interaction.user.name}'
        )
        embed = discord.Embed (
            title = f'Cấm thành công người dùng {member.name}',
            description = f'* Lí do cấm : {reason}\n* Số ngày tin nhắn bị xóa : `{delete_day}` ngày',
            color = 0x1be4a8,
            timestamp = datetime.datetime.now()
        )

        await interaction.response.defer()
        await interaction.followup.send(embed = embed)

async def setup(bot):
    await bot.add_cog(Ban(bot))