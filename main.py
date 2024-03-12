import discord
from discord.ext import commands
import sqlite3

from constants import DISCORD_TOKEN


class TaskBot(commands.Bot):
    def __init__(self, **options) -> None:
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=True, users=True)
        intents = discord.Intents.all()
        super().__init__(command_prefix=commands.when_mentioned_or("/"),
                         allowed_mentions=allowed_mentions,
                         intents=intents,
                         help_command=None, **options)

    async def setup_hook(self) -> None:
        await self.load_extension('extensions')
        await self.tree.sync()

    async def on_ready(self):
        print(f"logging as {self.user}")


def main():
    TaskBot().run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()



