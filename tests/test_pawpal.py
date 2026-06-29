"""Tests for the PawPal+ backend logic in pawpal_system.py."""

from pawpal_system import Pet, Task, Priority


def test_mark_complete_changes_status():
    """Calling mark_complete() should flip a task from incomplete to complete."""
    task = Task("Morning walk", 30, Priority.HIGH, "exercise", "daily")
    assert task.is_completed is False   # tasks start incomplete

    task.mark_complete()

    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    """Adding a task to a Pet should grow that pet's task list by one."""
    pet = Pet("Biscuit", "Golden Retriever")
    assert len(pet.get_tasks()) == 0    # a new pet has no tasks

    pet.add_task(Task("Feeding", 10, Priority.HIGH, "feeding", "daily"))

    assert len(pet.get_tasks()) == 1
