from discord.ext import commands, tasks
from datetime import datetime
import sqlite3

class VoiceReward(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_users = {}  
        self.db = sqlite3.connect("coins.db")
        self.create_tables()
        self.check_voice.start()

    def create_tables(self):
        """Создаём таблицы в базе данных"""
        with self.db:
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    nick_name TEXT,
                    coins INTEGER DEFAULT 0,
                    last_reward_time TIMESTAMP
                )
            """)
            self.db.commit()

    def cog_unload(self):
        self.check_voice.cancel()
    
    @tasks.loop(minutes=1)
    async def check_voice(self):
        now = datetime.now()
        reward_rate = 5  # 5 монет в минуту

        for user_id, data in list(self.voice_users.items()):
            channel_id, join_time = data
            time_spent = (now - join_time).total_seconds() // 60

            if time_spent >= 1:
                coins_to_add = int(time_spent) * reward_rate
                user = self.bot.get_user(user_id)
                
                try:
                    with self.db:
                        self.db.execute(
                            "INSERT OR IGNORE INTO users (user_id, nick_name, coins) VALUES (?, ?, 0)",
                            (user_id, user.name if user else "Unknown")
                        )
                        self.db.execute(
                            "UPDATE users SET coins = coins + ?, last_reward_time = ? WHERE user_id = ?",
                            (coins_to_add, now.isoformat(), user_id)
                        )
                    self.voice_users[user_id] = (channel_id, now)
                except sqlite3.Error as e:
                    print(f"Database error: {e}")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Отслеживаем вход/выход из голосовых каналов"""
        # Игнорируем изменения состояния, не связанные с подключением/отключением
        if before.channel == after.channel:
            return
            
        if before.channel is None and after.channel is not None:
            self.voice_users[member.id] = (after.channel.id, datetime.now())
        elif before.channel is not None and after.channel is None:
            self.voice_users.pop(member.id, None)

async def setup(bot):
    await bot.add_cog(VoiceReward(bot))