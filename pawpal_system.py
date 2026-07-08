"""PawPal — a simple pet care scheduling system.

Skeleton classes generated from the UML class diagram in diagrams/uml.mmd.
Fill in the method bodies as you build out the app.
"""

from __future__ import annotations

from datetime import datetime, timedelta


class Pet:
    """A pet that tasks can be assigned to."""

    def __init__(
        self,
        name: str,
        species: str,
        breed: str | None = None,
        birthday: datetime | None = None,
    ) -> None:
        """Create a pet with a name, species, and optional breed and birthday."""
        self.name = name
        self.species = species      # e.g. "dog", "cat"
        self.breed = breed          # e.g. "Labrador"; None if unknown
        self.birthday = birthday    # date of birth; None if unknown


class Task:
    """A care task (e.g. walk, give medicine) for a specific pet."""

    def __init__(
        self,
        name: str,
        pet: Pet,
        time: datetime,
        priority: int,
        frequency: str | None = None,
    ) -> None:
        """Create a task for a pet at a given time with a priority (1-10)."""
        self.name = name          # what to do, e.g. "walk" or "give medicine"
        self.pet = pet            # the pet this task concerns
        self.time = time          # when the task is scheduled
        self.priority = priority  # 1 (low) to 10 (high)
        self.complete = False     # whether the task has been carried out
        self.frequency = frequency  # "daily", "weekly", or None for one-off

    def next_occurrence(self) -> Task | None:
        """Return a fresh, incomplete copy at the next due time, or None if one-off."""
        delta = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}.get(self.frequency)
        if delta is None:
            return None
        return Task(self.name, self.pet, self.time + delta, self.priority, self.frequency)


class Owner:
    """A pet owner who keeps pets and carries out tasks."""

    def __init__(self, name: str, pets: list[Pet] | None = None) -> None:
        """Create an owner with a name and an optional list of pets."""
        self.name = name
        self.pets: list[Pet] = pets if pets is not None else []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def execute_task(self, task: Task) -> None:
        """Carry out the given task."""
        raise NotImplementedError


class Scheduler:
    """Organizes tasks: what's due now, what's upcoming, and by priority."""

    def __init__(self, tasks: list[Task] | None = None) -> None:
        """Create a scheduler with an optional initial list of tasks."""
        self.tasks: list[Task] = tasks if tasks is not None else []

    def add_task(self, task: Task) -> None:
        """Add a task to the schedule."""
        self.tasks.append(task)

    def mark_complete(self, task: Task) -> Task | None:
        """Mark task complete; if it recurs, schedule and return the next occurrence."""
        task.complete = True
        next_task = task.next_occurrence()
        if next_task is not None:
            self.add_task(next_task)
        return next_task

    def mark_incomplete(self, task: Task) -> None:
        """Mark the given task as not yet complete."""
        task.complete = False

    def sort_by_time(self) -> list[Task]:
        """Return tasks sorted by their scheduled time (earliest first)."""
        return sorted(self.tasks, key=lambda task: task.time)

    def filter_by_status(self, complete: bool) -> list[Task]:
        """Return tasks matching the given completion status."""
        return [task for task in self.tasks if task.complete == complete]

    def filter_by_pet(self, pet_name: str) -> list[Task]:
        """Return tasks belonging to the pet with the given name."""
        return [task for task in self.tasks if task.pet.name == pet_name]

    def detect_conflicts(self) -> list[str]:
        """Return a warning for each pair of tasks scheduled at the same time."""
        warnings: list[str] = []
        tasks = self.tasks
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                if tasks[i].time == tasks[j].time:
                    warnings.append(
                        f"Conflict at {tasks[i].time:%H:%M}: "
                        f"'{tasks[i].name}' ({tasks[i].pet.name}) and "
                        f"'{tasks[j].name}' ({tasks[j].pet.name})"
                    )
        return warnings

    def get_current_tasks(self) -> list[Task]:
        """Return pending tasks whose scheduled time has already arrived."""
        now = datetime.now()
        return [task for task in self.tasks if not task.complete and task.time <= now]

    def get_upcoming_tasks(self) -> list[Task]:
        """Return pending tasks scheduled for later than now."""
        now = datetime.now()
        return [task for task in self.tasks if not task.complete and task.time > now]

    def sort_by_priority(self) -> list[Task]:
        """Return tasks sorted by priority (highest first)."""
        return sorted(self.tasks, key=lambda task: task.priority, reverse=True)
