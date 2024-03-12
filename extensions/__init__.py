from discord.ext import commands
from extensions.manage_task import setup as manage_task_setup


async def setup(bot: commands.Bot) -> None:
    await manage_task_setup(bot)
