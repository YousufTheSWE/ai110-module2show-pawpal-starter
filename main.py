"""Testing ground for the PawPal system.

Builds a small scenario in memory and exercises the scheduler's sorting,
filtering, recurring-task, and conflict-detection logic in the terminal.
Run with: python main.py
"""

from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def show(title: str, tasks: list[Task]) -> None:
    """Print a titled list of tasks, one per line."""
    print(f"\n{title}")
    print("-" * len(title))
    if not tasks:
        print("  (none)")
    for task in tasks:
        status = "done" if task.complete else "pending"
        freq = f", {task.frequency}" if task.frequency else ""
        print(
            f"  {task.time:%H:%M}  {task.name} ({task.pet.name})"
            f"  [priority {task.priority}, {status}{freq}]"
        )


def main() -> None:
    # An owner with two pets.
    rex = Pet(name="Rex", species="dog", breed="Labrador")
    whiskers = Pet(name="Whiskers", species="cat", breed="Tabby")
    owner = Owner(name="Sam", pets=[rex, whiskers])

    today = datetime.now()

    def at(hour: int, minute: int = 0) -> datetime:
        return today.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # Add tasks deliberately OUT OF ORDER to prove sorting works.
    scheduler = Scheduler()
    scheduler.add_task(Task("Evening feeding", rex, at(18, 0), priority=5))
    scheduler.add_task(Task("Morning walk", rex, at(8, 0), priority=7, frequency="daily"))
    scheduler.add_task(Task("Give medicine", whiskers, at(12, 30), priority=9))
    # A second task at the SAME time as the morning walk -> conflict.
    scheduler.add_task(Task("Litter cleaning", whiskers, at(8, 0), priority=4))

    print(f"Today's Schedule for {owner.name}")
    print("=" * 40)

    # Sorting by time.
    show("Sorted by time", scheduler.sort_by_time())

    # Sorting by priority (highest first).
    show("Sorted by priority", scheduler.sort_by_priority())

    # Filtering by pet.
    show("Rex's tasks only", scheduler.filter_by_pet("Rex"))

    # Conflict detection (does not crash — returns warnings).
    print("\nConflict check")
    print("--------------")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print(f"  {warning}")
    else:
        print("  No conflicts.")

    # Recurring task: completing the daily walk spawns tomorrow's walk.
    walk = scheduler.sort_by_time()[0]  # 8:00 morning walk (daily)
    print(f"\nCompleting '{walk.name}' (frequency={walk.frequency})...")
    next_walk = scheduler.mark_complete(walk)
    if next_walk is not None:
        print(f"  Auto-scheduled next occurrence for {next_walk.time:%Y-%m-%d %H:%M}")

    # Filtering by status now that one task is done.
    show("Completed tasks", scheduler.filter_by_status(complete=True))
    show("Pending tasks", scheduler.filter_by_status(complete=False))


if __name__ == "__main__":
    main()
