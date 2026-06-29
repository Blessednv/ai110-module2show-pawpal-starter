from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Priority     # Priority.HIGH, Priority.MEDIUM, or Priority.LOW
    category: str          # e.g. "feeding", "medication", "exercise"
    recurrence: str        # "daily", "weekly", or "one-off"
    fixed_time: Optional[str] = None       # input constraint: task must happen at this time, e.g. "08:00"
    scheduled_start: Optional[str] = None  # output: actual time the Scheduler assigned, e.g. "08:30"
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
