from discord.ext import commands
from bot_config import db


@commands.command(name='регистрация')
async def register_command(ctx):
    try:

        user = ctx.author
        nick_name = user.name
        user_id = user.id
        
        db.add_user(nick_name=nick_name, user_id=user_id)
        await ctx.send(f'{user.mention} прошел регистрацию')
    except Exception as e :
        await ctx.send(f"Ошибка : {e}")
        
    

