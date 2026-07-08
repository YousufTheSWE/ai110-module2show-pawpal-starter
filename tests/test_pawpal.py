"""Unit tests for the PawPal system."""

import os
import sys
from datetime import datetime

# Make the project root importable so `pawpal_system` resolves when pytest
# runs from inside the tests/ directory.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pawpal_system import Pet, Scheduler, Task


def make_task(
    pet: Pet,
    name: str = "walk",
    priority: int = 5,
    time: datetime = datetime(2026, 7, 8, 9, 0),
    frequency: str | None = None,
) -> Task:
    """Build a Task for the given pet, defaulting time/priority/frequency."""
    return Task(name=name, pet=pet, time=time, priority=priority, frequency=frequency)


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


def test_sort_by_time_returns_chronological_order():
    """Sorting Correctness: tasks come back earliest-time first, regardless of insertion order."""
    pet = Pet(name="Rex", species="dog")
    scheduler = Scheduler()

    evening = make_task(pet, name="feed", time=datetime(2026, 7, 8, 18, 0))
    morning = make_task(pet, name="walk", time=datetime(2026, 7, 8, 8, 0))
    noon = make_task(pet, name="meds", time=datetime(2026, 7, 8, 12, 30))

    # Add deliberately out of order.
    for task in (evening, morning, noon):
        scheduler.add_task(task)

    ordered = scheduler.sort_by_time()

    assert [t.name for t in ordered] == ["walk", "meds", "feed"]
    # Edge case: sorting an empty scheduler must not error and returns [].
    assert Scheduler().sort_by_time() == []


def test_completing_daily_task_creates_next_day():
    """Recurrence Logic: completing a daily task schedules an identical task one day later."""
    pet = Pet(name="Rex", species="dog")
    scheduler = Scheduler()
    daily = make_task(
        pet, name="walk", time=datetime(2026, 7, 8, 8, 0), frequency="daily"
    )
    scheduler.add_task(daily)

    next_task = scheduler.mark_complete(daily)

    # The next occurrence exists and was added to the scheduler.
    assert next_task is not None
    assert next_task in scheduler.tasks
    assert len(scheduler.tasks) == 2

    # It is due exactly one day later, still pending, same name/pet/frequency.
    assert next_task.time == datetime(2026, 7, 9, 8, 0)
    assert next_task.complete is False
    assert next_task.name == "walk"
    assert next_task.frequency == "daily"

    # Edge case: a one-off task spawns nothing on completion.
    one_off = make_task(pet, name="vet visit")
    scheduler.add_task(one_off)
    assert scheduler.mark_complete(one_off) is None
    assert len(scheduler.tasks) == 3


def test_detect_conflicts_flags_same_time():
    """Conflict Detection: two tasks at the exact same time produce a warning."""
    pet_a = Pet(name="Rex", species="dog")
    pet_b = Pet(name="Whiskers", species="cat")
    scheduler = Scheduler()

    same_time = datetime(2026, 7, 8, 8, 0)
    scheduler.add_task(make_task(pet_a, name="walk", time=same_time))
    scheduler.add_task(make_task(pet_b, name="litter", time=same_time))
    scheduler.add_task(make_task(pet_a, name="feed", time=datetime(2026, 7, 8, 18, 0)))

    conflicts = scheduler.detect_conflicts()

    # Exactly one clashing pair is reported.
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]

    # Edge case: no two tasks share a time -> no conflicts, no crash.
    clean = Scheduler()
    clean.add_task(make_task(pet_a, time=datetime(2026, 7, 8, 8, 0)))
    clean.add_task(make_task(pet_a, time=datetime(2026, 7, 8, 9, 0)))
    assert clean.detect_conflicts() == []
