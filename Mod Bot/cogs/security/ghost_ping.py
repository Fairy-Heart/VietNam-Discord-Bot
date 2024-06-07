from discord.ext import commands
import discord
import datetime

class GhostPing(commands.Cog):
    def __init__(self,  bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.mentions and message.author.bot:
            return False

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
    await bot.add_cog(GhostPing(bot))
