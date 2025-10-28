from discord.ext import commands
from datetime import datetime
import discord
from bot_config import db
import asyncio

@commands.command("мут")
@commands.has_permissions(manage_roles=True)
async def mute_for_price(ctx, member: discord.Member, duration: int):
    try:
        if member == ctx.author:
            await ctx.send("Ты не можешь замутить самого себя!")
            return

        if duration <= 0:
            await ctx.send("Укажи положительное число минут!")
            return

        id = ctx.author.id
        price = duration * 100
        balance = db.get_balance(user_id=id)

        if balance < price:
            await ctx.send(f"Недостаточно монет. Нужно {price}, у тебя {balance}.")
            return

        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, send_messages=False)

        if mute_role in member.roles:
            await ctx.send("Этот пользователь уже в муте.")
            return

        db.update_coins(id, -price)

        await member.add_roles(mute_role)
        await ctx.send(f"{member.mention} замучен на {duration} минут(ы) за {price} монет.")

        await asyncio.sleep(duration * 60)
        await member.remove_roles(mute_role)
        await ctx.send(f'Мут для {member.mention} снят.')

    except Exception as e:
        await ctx.send(f"❌ Ошибка: {str(e)}")
        print(f"Mute error: {e}")



        



