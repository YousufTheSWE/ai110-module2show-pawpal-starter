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
        if st.form_submit_button("Add task") and task_title:
            when = datetime.combine(date.today(), task_time)
            scheduler.add_task(Task(name=task_title, pet=pet, time=when, priority=priority))
            st.success(f"Scheduled '{task_title}' for {pet.name}.")

if not scheduler.tasks:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Today's Schedule")
st.caption("Sorted by priority (highest first) via Scheduler.sort_by_priority().")

if st.button("Generate schedule"):
    if not scheduler.tasks:
        st.warning("No tasks to schedule yet.")
    else:
        rows = [
            {
                "Priority": task.priority,
                "Time": task.time.strftime("%H:%M"),
                "Task": task.name,
                "Pet": task.pet.name,
                "Status": "done" if task.complete else "pending",
            }
            for task in scheduler.sort_by_priority()
        ]
        st.table(rows)
