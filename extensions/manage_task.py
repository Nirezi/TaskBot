import discord
from discord.ext import commands
from discord import app_commands

import sqlite3


class ManageTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="add", description="Add a task")
    @app_commands.guild_only()
    async def add(self, interaction: discord.Interaction, title: str, description: str, deadline: str) -> None:
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks VALUES (?, ?, ?, ?, ?)',
                       (interaction.id, title, description, "YET", deadline))
        conn.commit()
        conn.close()
        await interaction.response.send_message("Task added")

    @app_commands.command(name="list", description="List all tasks")
    @app_commands.guild_only()
    async def _list(self, interaction: discord.Interaction) -> None:
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE task_status = "YET"')
        tasks = cursor.fetchall()
        conn.close()
        await interaction.response.send_message("\n".join(str(task) for task in tasks)+" tasks")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ManageTask(bot))
