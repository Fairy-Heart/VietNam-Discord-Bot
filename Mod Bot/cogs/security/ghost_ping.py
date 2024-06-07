from discord.ext import commands
import discord
import datetime
<<<<<<< HEAD
from discord import app_commands
=======

>>>>>>> 87ce6fb7e643c01154534d36a8153a063c1a85f2

class GhostPing(commands.Cog):
    def __init__(self,  bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
<<<<<<< HEAD

        if message.mentions and message.author.bot:
            return False

=======
>>>>>>> 87ce6fb7e643c01154534d36a8153a063c1a85f2
        if message.mentions:
            embed = discord.Embed(
                title = 'Đã phát hiện Ghost Ping !',
                description = f'* Nội dung tin nhắn ban đầu :\n* `{message.content}`\n* Gửi vào lúc : `{message.created_at}`',
                color = 0x00ffff,
                timestamp = datetime.datetime.now()
            )
            embed.set_thumbnail(
                url = f'{message.author.avatar}'
            )
            await message.channel.send(embed = embed)

async def setup(bot):
<<<<<<< HEAD
    await bot.add_cog(GhostPing(bot))
=======
    await bot.add_cog(GhostPing(bot))
>>>>>>> 87ce6fb7e643c01154534d36a8153a063c1a85f2
