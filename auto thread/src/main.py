import discord
from discord.ext import commands
import json

config_path = './config.json'

with open(config_path) as config_file:
    data = json.load(config_file)
    Token = data['TOKEN']


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot (
    command_prefix = '.',
    intents = intents
 )

channel_id = 1 # Thay thế
# bằng id kênh thực tế của bạn của bạn

@bot.event
async def on_ready():
    print(f'Online vào bot {bot.user}')

@bot.event
async def on_message(message):
    if message.channel.id == channel_id:
        await message.create_thread(
            name = f'{message.author}\'s thread',
            auto_archive_duration = 10080,
            reason = 'Chủ đề được tạo tự động'
        )

bot.run(Token)