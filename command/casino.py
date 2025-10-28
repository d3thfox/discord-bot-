from discord.ext import commands
from bot_config import db
import random
import sqlite3

@commands.command(name="деп")
async def casino_command(ctx,amount : str):
    try:
        try:
            amount = int(amount)
        except ValueError:
            await ctx.send('Только числа, дружок! Не пытайся обмануть систему')
            return
        if amount < 0 :
            await ctx.send('Ты не можешь поставить отрицательное число  ')
            return
        
        user_id = ctx.author.id
        current_balance = db.get_balance(user_id=user_id)

        if current_balance < amount:
            await ctx.send(f"У тебя нет столько коинов  - {current_balance} у тебя коинов")
            return
        
        number = random.randint(1,15)

        if number <= 8:
            new_balance = current_balance - amount
            result = f'Увы проиграл {amount} '
        
        elif number <= 12:
            win = int(amount * 1.5 )
            new_balance = current_balance + win 
            result = f'БЭУ + {win}'
        else:
            win = amount * 2 
            new_balance = current_balance + win 
            result = f'ДЖЕЕКПООТ + {win}'
        
        db.update_coins(user_id, new_balance - current_balance)  

        await ctx.send(
            f'{result}\n'
            f'У тебя теперь {new_balance} коинов '
        )

    except ValueError:
        await ctx.send("❌ Пожалуйста, укажите корректную сумму ставки (число)!")
    except sqlite3.Error as e:
        await ctx.send("❌ Произошла ошибка при обновлении баланса")
        print(f"Database error: {e}")
    except Exception as e:
        await ctx.send("❌ Произошла непредвиденная ошибка")
        print(f"Error: {e}")



  
