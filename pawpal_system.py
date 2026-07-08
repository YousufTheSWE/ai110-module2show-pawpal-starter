"""PawPal — a simple pet care scheduling system.

Skeleton classes generated from the UML class diagram in diagrams/uml.mmd.
Fill in the method bodies as you build out the app.
"""

from __future__ import annotations

from datetime import datetime


class Pet:
    """A pet that tasks can be assigned to."""

    def __init__(
        self,
        name: str,
        species: str,
        breed: str | None = None,
        birthday: datetime | None = None,
    ) -> None:
        self.name = name
        self.species = species      # e.g. "dog", "cat"
        self.breed = breed          # e.g. "Labrador"; None if unknown
        self.birthday = birthday    # date of birth; None if unknown


class Task:
    """A care task (e.g. walk, give medicine) for a specific pet."""

    def __init__(self, name: str, pet: Pet, time: datetime, priority: int) -> None:
        self.name = name          # what to do, e.g. "walk" or "give medicine"
        self.pet = pet            # the pet this task concerns
        self.time = time          # when the task is scheduled
        self.priority = priority  # 1 (low) to 10 (high)
        self.complete = False     # whether the task has been carried out


class Owner:
    """A pet owner who keeps pets and carries out tasks."""

    def __init__(self, name: str, pets: list[Pet] | None = None) -> None:
        self.name = name
        self.pets: list[Pet] = pets if pets is not None else []

    def execute_task(self, task: Task) -> None:
        """Carry out the given task."""
        raise NotImplementedError


class Scheduler:
    """Organizes tasks: what's due now, what's upcoming, and by priority."""

    def __init__(self, tasks: list[Task] | None = None) -> None:
        self.tasks: list[Task] = tasks if tasks is not None else []

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule."""
        self.tasks.append(task)

    def mark_complete(self, task: Task) -> None:
        """Mark the given task as complete."""
        task.complete = True

    def mark_incomplete(self, task: Task) -> None:
        """Mark the given task as not yet complete."""
        task.complete = False

    def get_current_tasks(self) -> list[Task]:
        """Return tasks that need to be done now."""
        raise NotImplementedError

    def get_upcoming_tasks(self) -> list[Task]:
        """Return tasks scheduled for the future."""
        raise NotImplementedError

    def sort_by_priority(self) -> list[Task]:
        """Return tasks sorted by priority (highest first)."""
        raise NotImplementedError
