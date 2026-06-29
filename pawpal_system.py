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
    fixed_time: Optional[str] = None       # input constraint: must happen at this time, e.g. "08:00"
    scheduled_start: Optional[str] = None  # output: time the Scheduler actually assigned
    pet_name: Optional[str] = None         # which pet this task belongs to (set by Pet.add_task)
    is_completed: bool = False

    def mark_complete(self):
        """Toggle the completion status of this task."""
        self.is_completed = not self.is_completed

    def update_details(self, duration: int = None, priority: Priority = None, fixed_time: str = None):
        """Update editable constraints. Any argument left as None is unchanged."""
        if duration is not None:
            self.duration_minutes = duration
        if priority is not None:
            self.priority = priority
        if fixed_time is not None:
            self.fixed_time = fixed_time


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Attach a care task to this pet, tagging it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return all tasks belonging to this pet."""
        return self.tasks


class Owner:
    def __init__(self, name: str, available_time_minutes: int, preferences: dict = None):
        """Create an owner with a daily time budget and optional preferences."""
        self.name = name
        self.available_time_minutes = available_time_minutes
        self.preferences = preferences or {}
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        """Link a pet to this owner."""
        self.pets.append(pet)

    def get_pets(self) -> list[Pet]:
        """Return all pets belonging to this owner."""
        return self.pets

    def get_all_tasks(self) -> list[Task]:
        """Combine every pet's task list into one list.

        This answers "how does the Scheduler get task data?" — it asks the
        Owner, who delegates to each pet's get_tasks(). The Scheduler never
        has to know how a Pet stores its tasks.
        """
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """Stateless logic engine. Reads an Owner's time budget and the tasks
    across all of their pets, then produces one ordered daily plan."""

    PRIORITY_ORDER = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}

    def generate_daily_plan(self, owner: Owner) -> list[Task]:
        """Build today's plan across ALL of the owner's pets, respecting the
        owner's time budget.

        Order matters (see reflection 1b): SORT by priority first, then FILTER
        by time, so a high-priority task is never dropped just because
        lower-priority tasks used up the budget.
        """
        tasks = [t for t in owner.get_all_tasks() if not t.is_completed]  # 1. all pets, skip done
        tasks = self._sort_tasks_by_priority(tasks)                       # 2. high priority first
        tasks = self._filter_tasks(tasks, owner.available_time_minutes)   # 3. keep what fits
        tasks = self._resolve_conflicts(tasks)                            # 4. drop fixed-time clashes
        day_start = owner.preferences.get("day_start", "08:00")
        return self._assign_times(tasks, day_start)                       # 5. lay out the timeline

    def _sort_tasks_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered high -> medium -> low."""
        return sorted(tasks, key=lambda t: self.PRIORITY_ORDER[t.priority])

    def _filter_tasks(self, tasks: list[Task], available_time: int) -> list[Task]:
        """Greedily keep tasks (already priority-sorted) until time runs out."""
        kept, total = [], 0
        for task in tasks:
            if total + task.duration_minutes <= available_time:
                kept.append(task)
                total += task.duration_minutes
        return kept

    def _resolve_conflicts(self, tasks: list[Task]) -> list[Task]:
        """Drop a fixed-time task if its window overlaps one already kept.
        Since the list is priority-sorted, the higher-priority task wins."""
        kept = []
        for task in tasks:
            if task.fixed_time is None:
                kept.append(task)            # flexible tasks can't clash by time
                continue
            start = self._to_minutes(task.fixed_time)
            end = start + task.duration_minutes
            clashes = any(
                start < self._to_minutes(o.fixed_time) + o.duration_minutes
                and self._to_minutes(o.fixed_time) < end
                for o in kept if o.fixed_time is not None
            )
            if not clashes:
                kept.append(task)
        return kept

    def _assign_times(self, tasks: list[Task], day_start: str) -> list[Task]:
        """Give each task a real start time. Fixed-time tasks anchor at their
        time; flexible tasks fill the gaps. Returns tasks in time order."""
        fixed = sorted((t for t in tasks if t.fixed_time),
                       key=lambda t: self._to_minutes(t.fixed_time))
        flexible = [t for t in tasks if not t.fixed_time]

        plan, cursor, fi = [], self._to_minutes(day_start), 0
        for flex in flexible:
            while fi < len(fixed) and self._to_minutes(fixed[fi].fixed_time) <= cursor:
                anchor = fixed[fi]
                anchor.scheduled_start = anchor.fixed_time
                cursor = self._to_minutes(anchor.fixed_time) + anchor.duration_minutes
                plan.append(anchor)
                fi += 1
            flex.scheduled_start = self._to_clock(cursor)
            cursor += flex.duration_minutes
            plan.append(flex)

        while fi < len(fixed):                # any fixed tasks left at the end
            anchor = fixed[fi]
            anchor.scheduled_start = anchor.fixed_time
            plan.append(anchor)
            fi += 1

        plan.sort(key=lambda t: self._to_minutes(t.scheduled_start))
        return plan

    def explain_plan(self, tasks: list[Task], owner: Owner = None) -> str:
        """Return a human-readable summary, grouped by pet."""
        if not tasks:
            return "No tasks scheduled for today."

        total = sum(t.duration_minutes for t in tasks)
        owner_name = owner.name if owner else "you"
        species_by_name = {p.name: p.species for p in owner.get_pets()} if owner else {}

        # Group tasks under each pet, keeping each pet's tasks in time order.
        tasks_by_pet = {}
        for t in tasks:
            tasks_by_pet.setdefault(t.pet_name, []).append(t)

        lines = [f"Today's Schedule for {owner_name} ({total} min total)", ""]
        for pet_name, pet_tasks in tasks_by_pet.items():
            species = species_by_name.get(pet_name)
            lines.append(f"{pet_name} ({species})" if species else str(pet_name))
            for t in pet_tasks:
                lines.append(
                    f"  {t.scheduled_start}  {t.title:<14} "
                    f"{t.duration_minutes:>2}m  [{t.priority.value.upper()}]"
                )
            lines.append("")  # blank line between pets
        return "\n".join(lines).rstrip()

    # --- clock-string <-> minutes-since-midnight helpers ---
    @staticmethod
    def _to_minutes(clock: str) -> int:
        """Convert an "HH:MM" clock string into minutes since midnight."""
        hours, minutes = clock.split(":")
        return int(hours) * 60 + int(minutes)

    @staticmethod
    def _to_clock(minutes: int) -> str:
        """Convert minutes since midnight back into an "HH:MM" clock string."""
        return f"{minutes // 60:02d}:{minutes % 60:02d}"


if __name__ == "__main__":
    # CLI-first check: prove the backend works before touching Streamlit.
    owner = Owner("Sam", available_time_minutes=90, preferences={"day_start": "08:00"})

    biscuit = Pet("Biscuit", "Golden Retriever")
    alfie = Pet("Alfie", "Cat")
    owner.add_pet(biscuit)
    owner.add_pet(alfie)

    biscuit.add_task(Task("Feeding", 10, Priority.HIGH, "feeding", "daily", fixed_time="08:00"))
    biscuit.add_task(Task("Morning walk", 30, Priority.HIGH, "exercise", "daily"))
    biscuit.add_task(Task("Enrichment", 20, Priority.LOW, "enrichment", "daily"))
    alfie.add_task(Task("Feeding", 10, Priority.HIGH, "feeding", "daily"))
    alfie.add_task(Task("Litter box", 5, Priority.MEDIUM, "grooming", "daily"))

    scheduler = Scheduler()
    plan = scheduler.generate_daily_plan(owner)
    print(scheduler.explain_plan(plan, owner))
