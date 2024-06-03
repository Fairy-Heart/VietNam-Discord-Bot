import discord
from discord.ext import commands
from discord import app_commands

class userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = 'userinfo',
        description = 'Thông tin về người dùng'
    )
    @app_commands.describe(
        user = 'Người bạn muốn xem thông tin'
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def test(
        self,
        interaction: discord.Integration,
        user: discord.Member
    ):
        
        embed = discord.Embed(
            title = f'Thông tin về người dùng {user}',
            description = (
                f'* Tên người dùng : {user.name}\n' +\
                f'* ID người dùng : {user.id}\n' +\
                f'* Tạo tài khoản vào lúc : `{user.created_at}`\n' +\
                f'* Tham gia server vào lúc : `{user.joined_at}`\n' +\
                (f'* Đăng kí nitro vào lúc : `{user.premium_since}`\n' if user.premium_since else f'* Người dùng chưa đăng kí nitro !\n') +\
                (f'* Người dùng là bot !\n' if user.bot == True else f'* Người dùng không phải là bot !\n') +\
                (f'* Banner của người dùng [Tải về tại đây]({user.banner})' if user.banner else f'* Người dùng không có banner !\n')
            ),
            color = 0xe2941d
        )
        embed.set_thumbnail(
            url = f'{user.avatar}'
        )

        await interaction.response.defer()
        await interaction.followup.send(embed = embed)
    

async def setup(bot):
    await bot.add_cog(userinfo(bot))