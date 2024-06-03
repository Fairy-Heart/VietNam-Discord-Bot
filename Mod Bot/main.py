import discord
from discord.ext import commands
import json
from typing import Literal, Optional

config_path = './config.json'

with open(config_path) as config_file:
    data = json.load(config_file)
    Token = data['Token']
    Prefix = data['Prefix']


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
    command_prefix = Prefix,
    intents = intents,
    help_command = None,
    strip_after_prefix = True
)

cogs_list = [
    'cogs.ulti.userinfo',
    'cogs.events.cooldown',
    'cogs.moderator.ban',
    'cogs.moderator.kick',
    'cogs.moderator.rename',
    'cogs.events.cooldown'
]

async def load_cogs():
    for cogs in cogs_list:
        try:
            await bot.load_extension(cogs)
            print('Load cogs thành công')
        except Exception as error_on_load_cogs:
            print(f'Gặp lỗi khi load cogs ^^^{error_on_load_cogs}')

@bot.event
async def on_ready():
    print(f'Online vào bot {bot.user}')
    await load_cogs()

# SyncSlash. Mỗi lần chỉnh sửa lệnh nên syncslash lại 1 lần :D
# ?syncslash 
@bot.command()
@commands.is_owner()
async def syncslash(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")    

bot.run(Token)