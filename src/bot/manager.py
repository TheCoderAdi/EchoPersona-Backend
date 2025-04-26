import os
from multiprocessing import Process
from dotenv import load_dotenv
import asyncio
from src.database.mongo_manager import log_away_message

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
FASTAPI_ENDPOINT = os.getenv("FASTAPI_ENDPOINT")

class BotManager:
    def __init__(self):
        self.bots = {}  
        self.greeted_users = {}  

    def initialize_bot(self, user_id, bot_token):
        if user_id in self.bots:
            return f"Bot for {user_id} already initialized."

        process = Process(target=self._run_bot, args=(user_id, bot_token))
        process.start()

        self.bots[user_id] = process
        self.greeted_users[user_id] = set()

        return f"Bot initialized for {user_id}"

    def _run_bot(self, user_id, token):
        import discord
        from discord.ext import commands
        import requests
        from src.database.mongo_manager import get_user_profile

        intents = discord.Intents.default()
        intents.message_content = True

        bot = commands.Bot(command_prefix="!",intents=intents)
        greeted_users = set()

        @bot.event
        async def on_ready():
            print(f"🤖 MimicBot for {user_id} logged in as {bot.user}")

        @bot.event
        async def on_message(message):
            if message.author == bot.user:
                return

            profile = get_user_profile(user_id=user_id)

            if not profile or not profile.get("away", False):
                return

            if message.author.id not in greeted_users:
                greeted_users.add(message.author.id)
                intro = (
                    f"Heya! 😎 This is EchoPersonaAI, standing in for {user_id}. "
                    "They’re away right now 🛸 but I can keep you company!"
                )
                await message.channel.send(intro)

            await message.channel.typing()
            log_away_message(
                user_id=user_id,
                sender_id=message.author.id,
                sender_name=str(message.author),
                content=message.content
            )

            payload = {
                "user_id": user_id,
                "message": message.content
            }

            try:
                response = requests.post(FASTAPI_ENDPOINT, json=payload)
                if response.status_code == 200:
                    auto_reply = response.json().get("auto_reply")
                    await message.channel.send(f"{auto_reply}" if auto_reply else "❌ No reply generated.")
                else:
                    await message.channel.send("⚠️ Could not process message.")
            except Exception as e:
                print(f"[Bot error for {user_id}]:", e)
                await message.channel.send("⚠️ Error while contacting the server.")

        try:
            bot.run(token)
        except discord.LoginFailure:
            return f"[⚠️ Login failed] Invalid token for {user_id}."
        except Exception as e:
            print(f"[Unhandled bot error for {user_id}]:", e)

    def stop_bot(self, user_id):
        if user_id not in self.bots:
            return f"No bot found for {user_id}"

        process = self.bots[user_id]
        process.terminate()
        process.join()

        del self.bots[user_id]
        self.greeted_users.pop(user_id, None)

        print(f"🤖 Bot for {user_id} stopped.")
        return f"Bot stopped for {user_id}"

    def is_bot_running(self, user_id):
        return user_id in self.bots and self.bots[user_id].is_alive()

    async def monitor_bots(self):
        """Periodically checks and restarts crashed bots."""
        while True:
            await asyncio.sleep(5)
            for user_id, process in list(self.bots.items()):
                if not process.is_alive():
                    print(f"[⚠️ Bot crash detected] Restarting bot for {user_id}")
                    bot_token = self.tokens.get(user_id)
                    if bot_token:
                        self.initialize_bot(user_id, bot_token)