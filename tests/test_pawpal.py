"""Unit tests for the PawPal system."""

import os
import sys
from datetime import datetime

# Make the project root importable so `pawpal_system` resolves when pytest
# runs from inside the tests/ directory.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pawpal_system import Pet, Scheduler, Task


def make_task(pet: Pet, name: str = "walk", priority: int = 5) -> Task:
    """Build a Task for the given pet at an arbitrary time."""
    return Task(name=name, pet=pet, time=datetime(2026, 7, 8, 9, 0), priority=priority)


def test_mark_complete_changes_status():
    """Task Completion: mark_complete() flips a task's status to done."""
    pet = Pet(name="Rex", species="dog")
    task = make_task(pet)
    scheduler = Scheduler()
    scheduler.add_task(task)

    # A new task starts out incomplete.
    assert task.complete is False

    scheduler.mark_complete(task)

    # After marking complete, the status must actually change.
    assert task.complete is True


def test_adding_task_increases_task_count():
    """Task Addition: adding a task increases a pet's task count."""
    pet = Pet(name="Whiskers", species="cat")
    scheduler = Scheduler()

    def tasks_for(p: Pet) -> int:
        return len([t for t in scheduler.tasks if t.pet is p])

    # No tasks for this pet to begin with.
    assert tasks_for(pet) == 0

    scheduler.add_task(make_task(pet))

    # Adding one task bumps the pet's task count by exactly one.
    assert tasks_for(pet) == 1
