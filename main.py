"""Testing ground for the PawPal system.

Builds a small scenario in memory and prints today's schedule to the terminal.
Run with: python main.py
"""

from datetime import datetime

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    # Create an owner with two pets.
    rex = Pet(name="Rex", species="dog", breed="Labrador")
    whiskers = Pet(name="Whiskers", species="cat", breed="Tabby")
    owner = Owner(name="Sam", pets=[rex, whiskers])

    # Set up a scheduler and add three tasks at different times of the day.
    scheduler = Scheduler()
    today = datetime.now()

    scheduler.add_task(
        Task(
            name="Morning walk",
            pet=rex,
            time=today.replace(hour=8, minute=0, second=0, microsecond=0),
            priority=7,
        )
    )
    scheduler.add_task(
        Task(
            name="Give medicine",
            pet=whiskers,
            time=today.replace(hour=12, minute=30, second=0, microsecond=0),
            priority=9,
        )
    )
    scheduler.add_task(
        Task(
            name="Evening feeding",
            pet=rex,
            time=today.replace(hour=18, minute=0, second=0, microsecond=0),
            priority=5,
        )
    )

    # Print today's schedule, ordered by time.
    print(f"Today's Schedule for {owner.name}")
    print("=" * 40)
    for task in sorted(scheduler.tasks, key=lambda t: t.time):
        status = "done" if task.complete else "pending"
        print(
            f"{task.time:%H:%M}  {task.name} ({task.pet.name})"
            f"  [priority {task.priority}, {status}]"
        )


if __name__ == "__main__":
    main()
