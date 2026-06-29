from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str          # "high", "medium", or "low"
    category: str          # e.g. "feeding", "medication", "exercise"
    recurrence: str        # "daily", "weekly", or "one-off"
    fixed_time: Optional[str] = None   # e.g. "08:00" if the task must happen at a set time
    is_completed: bool = False

    def mark_complete(self):
        pass

    def update_details(self, duration: int = None, priority: str = None, fixed_time: str = None):
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def get_tasks(self) -> list[Task]:
        pass


class Owner:
    def __init__(self, name: str, available_time_minutes: int, preferences: dict = None):
        self.name = name
        self.available_time_minutes = available_time_minutes
        self.preferences = preferences or {}
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def get_pets(self) -> list[Pet]:
        pass


class Scheduler:
    def generate_daily_plan(self, owner: Owner, pet: Pet) -> list[Task]:
        pass

    def _sort_tasks_by_priority(self, tasks: list[Task]) -> list[Task]:
        pass

    def _filter_tasks(self, tasks: list[Task], available_time: int) -> list[Task]:
        pass

    def _resolve_conflicts(self, tasks: list[Task]) -> list[Task]:
        pass

    def explain_plan(self, tasks: list[Task]) -> str:
        pass
