import datetime
import re
import sqlite3

import discord
from discord import app_commands
from discord.ext import commands


class ManageTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def convert_to_datetime(date: str) -> datetime.datetime:
        """Convert date string(YYYYMMDD or MMDD or DD) to datetime object"""
        now = datetime.datetime.now()
        year = now.year
        month = now.month

        if len(date) == 8:
            year = int(date[:4])
            month = int(date[4:6])
            day = int(date[6:])
        elif len(date) == 4:
            month = int(date[:2])
            day = int(date[2:])
        else:  # len(date) == 2
            day = int(date)

        return datetime.datetime(year, month, day, 9, 00)

    @app_commands.command(name="add", description="Add a task")
    @app_commands.guild_only()
    async def add(self, interaction: discord.Interaction, title: str, description: str, deadline: str) -> None:
        match = re.search(r'\d{2,8}', deadline)
        if not match:
            await interaction.response.send_message("締切日の形式が不正です。20241231(2024年12月31日)の形式で入力してください。")
            return

        try:
            deadline_datetime = await self.convert_to_datetime(match.group())
        except ValueError as e:
            await interaction.response.send_message(str(e))
            return

        # check deadline is not past
        if deadline_datetime < datetime.datetime.now():
            await interaction.response.send_message("締切日が過去の日付です。")
            return

        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO tasks VALUES (?, ?, ?, ?)',
                           (interaction.id, title, description, deadline_datetime.timestamp()))
            conn.commit()
        await interaction.response.send_message("Task added")

    @app_commands.command(name="list", description="List all tasks")
    @app_commands.guild_only()
    async def _list(self, interaction: discord.Interaction, include_past: bool = False) -> None:
        now = datetime.datetime.now()
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE task_deadline > ?', (now.timestamp(),))
            task_list = cursor.fetchall()

            cursor.execute('SELECT * FROM tasks WHERE task_deadline <= ?', (now.timestamp(),))
            past_task_list = cursor.fetchall()

        if task_list:
            response = await self.bot.get_cog("CheckTask").generate_task_list_text(task_list)
        else:
            response = "今のところ課題はないよ！やったね！！"

        if include_past and past_task_list:
            response += "\n\n過去の課題\n"
            response += await self.bot.get_cog("CheckTask").generate_task_list_text(past_task_list, check_tomorrow=False)

        await interaction.response.send_message(response)

    @app_commands.command(name="search", description="Search tasks")
    @app_commands.guild_only()
    async def search(self, interaction: discord.Interaction, keyword: str) -> None:
        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE task_title LIKE ?', (f'%{keyword}%',))  # keyword in title
            task_list = cursor.fetchall()

        if task_list:
            response = await self.bot.get_cog("CheckTask").generate_task_list_text(task_list)
        else:
            response = "該当する課題はありませんでした。"

        await interaction.response.send_message(response)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ManageTask(bot))
