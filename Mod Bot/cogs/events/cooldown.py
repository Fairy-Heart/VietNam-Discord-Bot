from discord.ext import commands
import time
import discord

class Cooldown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(
        self,
        ctx,
        error
    ):
        if not ctx.guild:
            return False
        
        if isinstance(error, commands.CommandOnCooldown):
            current_time = time.time()
            if current_time - self.last_cooldown_embed < 25:
                return False
            
            embed = discord.Embed(
                title = 'Lỗi',
                description = f'* Vui lòng sử dụng bot chậm lại {ctx.author}',
                color = 0xf0000
            )
            await ctx.send(embed = embed)
            self.last_cooldown_embed = current_time

async def setup(bot):
    await bot.add_cog(Cooldown(bot))