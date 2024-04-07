import datetime
import dataclasses


@dataclasses.dataclass
class Task:
    id: int
    title: str
    description: str
    deadline_unix: dataclasses.InitVar[int]
    deadline: datetime.datetime = dataclasses.field(init=False)

    def __str__(self) -> str:
        return f"- {self.title}　～{self.deadline.year}年{self.deadline.month}月{self.deadline.day}日\n{self.description}\n"

    def __post_init__(self, deadline_unix) -> None:
        self.deadline = datetime.datetime.fromtimestamp(deadline_unix)

    def is_deadline_tomorrow(self) -> bool:
        now = datetime.datetime.now()
        return (self.deadline - now) < datetime.timedelta(days=1) and self.deadline > now
