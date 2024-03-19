from discord.ext import commands
from extensions.manage_task import setup as manage_task_setup
from extensions.check_task import setup as check_task_setup


async def setup(bot: commands.Bot) -> None:
    await manage_task_setup(bot)
    await check_task_setup(bot)
