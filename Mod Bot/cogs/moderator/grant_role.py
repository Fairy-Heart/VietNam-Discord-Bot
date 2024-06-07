from discord.ext import commands
import discord
from discord import app_commands
import datetime


class GrantRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = 'grant_role',
        description = 'Gắn role cho một người dùng'
    )
    @app_commands.default_permissions(
        manage_roles = True
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @app_commands.describe(
        user = 'Người dùng bạn muốn gắn role',
        role = 'Role  bạn muốn gán cho  người dùng',
        reason = 'Lí do (nếu có)'
    )
    async def grantrole(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        role: discord.Role,
        reason: str = 'Không đề cập lí do'
    ):
        bot_user = interaction.guild.get_member(self.bot.user.id)

        if not interaction.guild:
            return False
        
        if interaction.guild.default_role.id == role.id:
            embed = discord.Embed(
                title = 'Lỗi',
                description = f'* Bạn không thể gán vai trò <@&{interaction.guild.default_role.id}> cho người dùng <@{user.id}> vì đây là vai trò mặc định của server',
                color = 0xff0000,
                timestamp = datetime.datetime.now()
            )
            await interaction.response.send_message(embed = embed)
            return False

        if interaction.user.top_role.position <= user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            embed = discord.Embed(
                title = 'Lỗi',
                description = '* Bạn không thể gán role cho người có vai trò cao hơn bản thân',
                color = 0xff0000,
                timestamp = datetime.datetime.now()
            )
            await interaction.response.send_message(embed = embed)
            return False
        
        if role.position <= user.top_role.position and interaction.user.id != interaction.guild.owner_id:
            embed = discord.Embed(
                title = 'Lỗi',
                description = 'Bạn không thể gắn một role có vị trí cao hơn bản thân',
                color = 0xff0000,
                timestamp = datetime.datetime.now()
            )
            await interaction.response.send_message(embed = embed)
            return False
        
        if role.position > bot_user.top_role.position:
            embed = discord.Embed(
                title = 'Lỗi',
                description = f'Vị trí vai trò cao nhất của bot là <@&{bot_user.top_role.id}> thấp hơn vai trò bạn muốn gán cho <@{user.id}> là <@&{role.id}>',
                color = 0xff0000,
                timestamp = datetime.datetime.now()
            )
            await interaction.response.send_message(embed = embed)
            return False
        

        await interaction.response.defer()
        await user.add_roles(
            role,
            reason = f'{reason} | Thực hiện bởi {interaction.user}'
        )
        embed = discord.Embed(
            description = f'* Gán vai trò <@&{role.id}> thành công cho người dùng <@{user.id}>\n* Lí do : {reason}',
            color = 0x80ffff,
            timestamp = datetime.datetime.now()
        )
        await interaction.followup.send(embed = embed)



async def setup(bot):
    await bot.add_cog(GrantRole(bot))