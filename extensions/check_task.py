import datetime
import sqlite3
from typing import List

from discord.ext import commands, tasks

from constants import NOTICE_ROLE_ID, NOTICE_CHANNEL_ID
from models import Task


class CheckTask(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.notice_task.start()

    @staticmethod
    async def generate_task_list_text(task_list: List[Task], check_tomorrow=True) -> str:
        response = ""
        tomorrow_task = []
        for task in task_list:
            response += str(task)
            if task.is_deadline_tomorrow():
                tomorrow_task.append(task)

        if check_tomorrow:
            if tomorrow_task:
                response += "\n期限が明日の課題があります。\n"
                for task in tomorrow_task:
                    response += str(task)
            else:
                response += "\n期限が明日の課題はありません。"

        return response

    @tasks.loop(minutes=1)
    async def notice_task(self) -> None:
        await self.bot.wait_until_ready()
        now = datetime.datetime.now()
        if not(now.hour == 17 and now.minute == 0):
            return

        with sqlite3.connect('tasks.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE task_deadline > ?', (now.timestamp(),))
            task_list = cursor.fetchall()

        response = f"<@&{NOTICE_ROLE_ID}>\n{now.month}月{now.day}日時点の課題状況をお知らせします。\n"

        task_list = [Task(*task) for task in task_list]
        if task_list:
            response += await self.generate_task_list_text(task_list)
        else:
            response += "今のところ課題はないよ！やったね！！"

        notice_channel = self.bot.get_channel(NOTICE_CHANNEL_ID)
        await notice_channel.send(response)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CheckTask(bot))
