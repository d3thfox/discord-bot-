import random
from discord.ext import commands

@commands.command(name="пися")
async def penis_command(ctx, *args):
    size = random.randint(0, 99)
    sm = random.choice(['см', 'мм'])
    location = random.choice(["спереди","сзади "])
    await ctx.reply(f'{size} {sm} {location}')