from datetime import date, datetime

import streamlit as st

# Step 1: bring the backend classes into the Streamlit script.
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# Step 2: persist the Owner and Scheduler in session_state so they survive
# reruns. Streamlit re-runs this script top-to-bottom on every interaction, so
# we only create fresh objects the first time — after that we reuse the ones
# already stored in the session "vault".
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner: Owner = st.session_state.owner
scheduler: Scheduler = st.session_state.scheduler

owner.name = st.text_input("Owner name", value=owner.name)

st.subheader("Pets")

# Step 3: wire "Add a Pet" to Owner.add_pet().
with st.form("add_pet", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    breed = st.text_input("Breed (optional)")
    if st.form_submit_button("Add pet") and pet_name:
        owner.add_pet(Pet(name=pet_name, species=species, breed=breed or None))
        st.success(f"Added {pet_name}.")

if owner.pets:
    st.write("Current pets:", ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Tasks")

# Step 3: wire "Schedule a Task" to Scheduler.add_task(). A task needs a pet,
# so this section only appears once at least one pet exists.
if not owner.pets:
    st.info("Add a pet before scheduling tasks.")
else:
    with st.form("add_task", clear_on_submit=True):
        pet = st.selectbox("Pet", owner.pets, format_func=lambda p: p.name)
        task_title = st.text_input("Task title", value="Morning walk")
        task_time = st.time_input("Time")
        priority = st.slider("Priority (1 = low, 10 = high)", 1, 10, 5)
        # Recurring tasks: "one-off" maps to None so the task never repeats.
        frequency_label = st.selectbox("Repeat", ["one-off", "daily", "weekly"])
        if st.form_submit_button("Add task") and task_title:
            when = datetime.combine(date.today(), task_time)
            frequency = None if frequency_label == "one-off" else frequency_label
            scheduler.add_task(
                Task(name=task_title, pet=pet, time=when, priority=priority, frequency=frequency)
            )
            st.success(f"Scheduled '{task_title}' for {pet.name}.")

# Conflict detection: surface warnings prominently instead of failing silently.
# A time clash is actionable for the owner, so lead with a count and list each
# clashing pair as its own warning line.
conflicts = scheduler.detect_conflicts()
if conflicts:
    st.warning(f"⚠️ {len(conflicts)} scheduling conflict(s) — two tasks share a time slot:")
    for warning in conflicts:
        st.markdown(f"- {warning}")

st.divider()

st.subheader("Manage Tasks")
st.caption("Tick the box to mark a task done. Completing a recurring task schedules its next occurrence.")

if not scheduler.tasks:
    st.info("No tasks yet. Add one above.")
else:
    # Filtering controls (Scheduler.filter_by_pet / filter_by_status).
    fcol1, fcol2 = st.columns(2)
    with fcol1:
        pet_filter = st.selectbox(
            "Filter by pet", ["All pets"] + [p.name for p in owner.pets]
        )
    with fcol2:
        status_filter = st.selectbox("Filter by status", ["All", "Pending", "Done"])

    # Sorting choice (Scheduler.sort_by_time / sort_by_priority).
    sort_choice = st.radio("Sort by", ["Time", "Priority"], horizontal=True)
    visible = (
        scheduler.sort_by_time() if sort_choice == "Time" else scheduler.sort_by_priority()
    )

    # Apply filters on top of the chosen ordering. Each filter method returns a
    # matching subset; we intersect by object identity to preserve the sort.
    if pet_filter != "All pets":
        keep = set(map(id, scheduler.filter_by_pet(pet_filter)))
        visible = [t for t in visible if id(t) in keep]
    if status_filter != "All":
        keep = set(map(id, scheduler.filter_by_status(status_filter == "Done")))
        visible = [t for t in visible if id(t) in keep]

    if not visible:
        st.info("No tasks match the current filters.")
    for task in visible:
        freq = f" · {task.frequency}" if task.frequency else ""
        label = f"{task.time:%H:%M} — {task.name} ({task.pet.name}) · P{task.priority}{freq}"
        # id(task) is a stable key for the object's lifetime, so the checkbox
        # tracks the right task even as the list is re-sorted or re-filtered.
        checked = st.checkbox(label, value=task.complete, key=f"task_{id(task)}")
        if checked and not task.complete:
            next_task = scheduler.mark_complete(task)
            if next_task is not None:
                st.toast(f"Next '{next_task.name}' scheduled for {next_task.time:%b %d}")
            st.rerun()
        elif not checked and task.complete:
            scheduler.mark_incomplete(task)
            st.rerun()

st.divider()

st.subheader("All Scheduled Tasks")
st.caption("Every task across all days, earliest first. Recurring tasks add future-dated occurrences.")

if not scheduler.tasks:
    st.info("Add some tasks to see the schedule.")
else:
    # Due now vs. upcoming (Scheduler.get_current_tasks / get_upcoming_tasks).
    due_now = scheduler.get_current_tasks()
    upcoming = scheduler.get_upcoming_tasks()
    scol1, scol2 = st.columns(2)
    scol1.metric("Due now", len(due_now))
    scol2.metric("Upcoming", len(upcoming))

    rows = [
        {
            "Date": task.time.strftime("%a %b %d"),
            "Time": task.time.strftime("%H:%M"),
            "Priority": task.priority,
            "Task": task.name,
            "Pet": task.pet.name,
            "Repeat": task.frequency or "—",
            "Status": "done" if task.complete else "pending",
        }
        for task in scheduler.sort_by_time()
    ]
    st.table(rows)
