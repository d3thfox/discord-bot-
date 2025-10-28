import discord 
from discord.ext import commands
from dotenv import load_dotenv
import os

from command.penis import penis_command
from command.register import register_command
from command.ballance import ballance
from command.mute import mute_for_price
from command.add_coins import setup as voice_reward_setup
from command.casino import casino_command
from command.fight import fight,pvp,accept_pvp

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True  # Необходимо для отслеживания голосовых каналов

bot = commands.Bot(command_prefix="!", intents=intents)

async def setup_extensions():
    await voice_reward_setup(bot)
    bot.add_command(penis_command)

    bot.add_command(register_command)
    bot.add_command(ballance)
    bot.add_command(casino_command)
    bot.add_command(mute_for_price)
    bot.add_command(fight)
    bot.add_command(pvp)
    bot.add_command(accept_pvp)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} запущен!')
    await setup_extensions()

load_dotenv()
bot.run(os.getenv('TOKEN'))
