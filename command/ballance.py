from discord.ext import commands
from bot_config import db

@commands.command(name='bal')
async def ballance(ctx):
    try:

        user_id = ctx.author.id
        ballance = db.get_balance(user_id=user_id)
        await ctx.reply(f'У тебя {ballance} коинов')
    except Exception as e:
        await ctx.reply(f'Ошибка : {e}')
