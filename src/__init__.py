import interactions
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    TOKEN_BOT = os.getenv("BOT_TOKEN")

    bot = interactions.Client(
        token=TOKEN_BOT,
        intents=interactions.Intents.ALL
    )

    for cog_file in os.listdir('src/cogs'):
        if cog_file.endswith('.py'):
            bot.load(f'src.cogs.{cog_file[:-3]}')

    bot.start()