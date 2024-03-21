import datetime
import sqlite3

from discord.ext import commands, tasks

from constants import NOTICE_ROLE_ID, NOTICE_CHANNEL_ID


class CheckTask(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.notice_task.start()

    @staticmethod
    async def generate_task_list_text(task_list: list, check_tomorrow=True) -> str:
        now = datetime.datetime.now()
        response = ""
        tomorrow_task = []
        for (_, title, description, deadline) in task_list:
            deadline = datetime.datetime.fromtimestamp(deadline)
            if (deadline - now) < datetime.timedelta(days=1):
                tomorrow_task.append(title)
            response += f"- {title}　～{deadline.month}月{deadline.day}日\n{description}\n"

        if check_tomorrow:
            if tomorrow_task:
                response += "\n期限が明日の課題があります。\n"
                response += await CheckTask.generate_task_list_text(tomorrow_task)
            else:
                response += "\n期限が明日の課題はありません。"

        return response

    @tasks.loop(minutes=1)
    async def notice_task(self) -> None:
        await self.bot.wait_until_ready()
        now = datetime.datetime.now()
        if not(now.hour == 17 and now.minute == 0):
            return

        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE task_deadline > ?', (now.timestamp(),))
        task_list = cursor.fetchall()
        conn.close()

        response = f"<@&{NOTICE_ROLE_ID}>\n{now.month}月{now.day}日時点の課題状況をお知らせします。\n"
        if not task_list:
            response += "今のところ課題はないよ！やったね！！"
        else:
            response += await self.generate_task_list_text(task_list)

        notice_channel = self.bot.get_channel(NOTICE_CHANNEL_ID)
        await notice_channel.send(response)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CheckTask(bot))
