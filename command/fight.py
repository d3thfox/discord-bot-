from discord.ext import commands
from bot_config import db
import random

class Fighter():
    def __init__(self, hp: int, attack: int, defense: int, regen: int):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.regen = regen

    def damage(self, damage: int):
        actual_damage = max(0, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage

    def heal(self):
        self.hp += self.regen

@commands.command(name="бой")
async def fight(ctx, amount: str):
    try:
        amount = int(amount)
    except ValueError:
        await ctx.reply("Пожалуйста, введи число (ставка).")
        return

    if amount < 0:
        await ctx.send('Ставка не может быть отрицательной.')
        return

    user_id = ctx.author.id
    current_balance = db.get_balance(user_id=user_id)

    if current_balance < amount:
        await ctx.send(f"У тебя недостаточно монет. У тебя: {current_balance}.")
        return

    fighter1 = Fighter(
        hp=random.randint(50, 100),
        attack=random.randint(30, 50),
        defense=random.randint(10, 20),
        regen=random.randint(5, 15)
    )
    fighter2 = Fighter(
        hp=random.randint(50, 100),
        attack=random.randint(30, 50),
        defense=random.randint(10, 20),
        regen=random.randint(5, 15)
    )

    battle_log = []
    round_count = 0

    while fighter1.hp > 0 and fighter2.hp > 0 and round_count < 10:
        round_count += 1
        battle_log.append(f'Раунд {round_count}')

        # Атака 1
        damage1 = fighter1.attack
        actual1 = fighter2.damage(damage1)
        battle_log.append(f'Ты наносишь {actual1} урона врагу. У врага осталось {fighter2.hp} хп.')

        if fighter2.hp <= 0:
            break

        # Атака 2
        damage2 = fighter2.attack
        actual2 = fighter1.damage(damage2)
        battle_log.append(f'Враг наносит {actual2} урона тебе. У тебя осталось {fighter1.hp} хп.')

        if fighter1.hp <= 0:
            break

        # Лечение
        fighter1.heal()
        fighter2.heal()
        battle_log.append(f'Ты восстановил здоровье до {fighter1.hp}, враг — до {fighter2.hp}.\n')

    # Определение победителя и изменение баланса
    if fighter1.hp > 0 and fighter2.hp <= 0:
        winner = '🎉 Победа! Ты выиграл бой.'
        profit = int(amount * 2)
        db.update_coins(user_id, profit)
        battle_log.append(f'{winner} Ты получаешь {profit} монет.')
    elif fighter2.hp > 0 and fighter1.hp <= 0:
        winner = '💀 Поражение! Враг оказался сильнее.'
        db.update_coins(user_id, -amount)
        battle_log.append(f'{winner} Ты теряешь {amount} монет.')
    else:
        winner = '🤝 Ничья!'
        battle_log.append(winner)

    # Отправка результата (ограничение длины до 2000 символов)
    message = "\n".join(battle_log)
    if len(message) > 1900:
        message = message[:1900] + "\n..."

    await ctx.send(message)

pending_fights = {}
@commands.command(name='пвп')
async def pvp(ctx,opponent : commands.MemberConverter, amount : int):
    challenger = ctx.author

    if amount <= 0:
        await ctx.reply('Положительные числа  ')
        return

    if opponent == challenger:
        await ctx.reply('Ты не можешь вызвать сам себя ')
        return
    
    if db.get_balance(user_id=challenger.id) < amount:
        await ctx.reply('У тебя нет столько ')
        return
    
    if db.get_balance(user_id=opponent.id) < amount:
        await ctx.reply('Твой противник бомж')
        return

    pending_fights[opponent.id] = {
            "challenger": challenger,
            "amount": amount,
            "channel": ctx.channel
        }
    
    await ctx.send(f"{opponent.mention}, тебя вызывает на бой {challenger.mention} на {amount} хуев! Напиши `!принять`, чтобы начать бой.")

@commands.command(name='принять')
async def accept_pvp(ctx):
    user = ctx.author

    if user.id not in pending_fights:
        await ctx.send('У тебя нет вызовов')
        return

    fight = pending_fights.pop(user.id)
    challenger = fight['challenger']
    amount = fight['amount']

    if db.get_balance(user_id=challenger.id) < amount or db.get_balance(user_id=user.id) < amount:
        await ctx.send("Один из игроков не может оплатить ставку.")
        return

    f1 = Fighter(hp=random.randint(50, 100), attack=random.randint(30, 50), defense=random.randint(10, 20), regen=random.randint(5, 15))
    f2 = Fighter(hp=random.randint(50, 100), attack=random.randint(30, 50), defense=random.randint(10, 20), regen=random.randint(5, 15))

    log = []
    round_count = 0

    while f1.hp > 0 and f2.hp > 0 and round_count < 10:
        round_count += 1
        log.append(f'Раунд {round_count}')

        dmg1 =  f1.attack
        dmg2 = f2.attack

        taken2 = f2.damage(dmg1)
        log.append(f"{challenger.display_name} наносит {taken2} урона. У {user.display_name} осталось {f2.hp} хп.")

        if f2.hp <= 0:
            break

        taken1 = f1.damage(dmg2)
        log.append(f"{user.display_name} наносит {taken1} урона. У {challenger.display_name} осталось {f1.hp} хп.")

        if f1.hp <= 0:
            break

        f1.heal()
        f2.heal()
        log.append(f"{challenger.display_name} восстановил здоровье до {f1.hp}, {user.display_name} — до {f2.hp}.\n")

    if f1.hp > 0 and f2.hp <= 0:
        winner, loser = challenger, user
    elif f2.hp > 0 and f1.hp <= 0:
        winner, loser = user, challenger
    else:
        await ctx.send("Ничья! Монеты возвращены игрокам.")
        return

    db.update_coins(winner.id, amount)
    db.update_coins(loser.id, -amount)
    log.append(f"🏆 Победитель: {winner.display_name}! Он получает {amount} монет от {loser.display_name}.")

    full_log = "\n".join(log)
    if len(full_log) > 1900:
        full_log = full_log[:1900] + "\n..."

    await fight["channel"].send(full_log)
