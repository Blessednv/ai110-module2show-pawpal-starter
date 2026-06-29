import streamlit as st

from pawpal_system import Owner, Pet, Task, Priority, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def get_owner() -> Owner:
    """Return the one Owner stored in Streamlit's session "vault".

    Streamlit re-runs this whole script top-to-bottom on every click, so an
    Owner made the normal way would be rebuilt empty each time (amnesia).
    st.session_state survives those re-runs. So: if no Owner is saved yet,
    build one and stash it; otherwise hand back the same Owner from before,
    with all its pets and tasks still attached.
    """
    if "owner" not in st.session_state:
        st.session_state.owner = Owner("Sam", available_time_minutes=90)
    return st.session_state.owner


# Grab the persistent owner once; every re-run points to the SAME object.
owner = get_owner()

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

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {"title": task_title, "duration_minutes": int(duration), "priority": priority}
    )

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )

st.divider()

# ============================================================
# LIVE SECTION — wired to the backend in pawpal_system.py.
# (The "UI only" section above is kept for reference.)
# ============================================================
st.header("✅ PawPal+ (wired to logic)")

# Keep the stored owner's name/time in sync with the text boxes.
owner.name = st.text_input("Owner name", value=owner.name, key="live_owner_name")
owner.available_time_minutes = st.number_input(
    "Time available today (minutes)",
    min_value=0, max_value=600, value=owner.available_time_minutes, step=5,
    key="live_owner_time",
)

# ---- Add a pet ----  (Owner.add_pet handles the data)
st.subheader("Add a Pet")
live_pet_name = st.text_input("New pet name", value="Biscuit", key="live_pet_name")
live_species = st.selectbox("Species", ["dog", "cat", "other"], key="live_species")

if st.button("Add pet", key="live_add_pet"):
    owner.add_pet(Pet(live_pet_name, live_species))
    st.success(f"Added {live_pet_name} the {live_species}.")

if owner.get_pets():
    st.write("Your pets: " + ", ".join(p.name for p in owner.get_pets()))
else:
    st.info("No pets yet. Add one above.")

# ---- Add a task to a pet ----  (Pet.add_task handles the data)
st.subheader("Add a Task")
if not owner.get_pets():
    st.info("Add a pet first, then you can give it tasks.")
else:
    chosen_pet = st.selectbox(
        "Which pet?", [p.name for p in owner.get_pets()], key="live_task_pet"
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        live_task_title = st.text_input("Task title", value="Morning walk", key="live_task_title")
    with c2:
        live_duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20, key="live_task_dur"
        )
    with c3:
        live_priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="live_task_prio")
    live_fixed = st.text_input("Fixed time (optional, e.g. 08:00)", value="", key="live_task_fixed")

    if st.button("Add task", key="live_add_task"):
        pet = next(p for p in owner.get_pets() if p.name == chosen_pet)
        pet.add_task(Task(
            title=live_task_title,
            duration_minutes=int(live_duration),
            priority=Priority(live_priority),   # "high" -> Priority.HIGH
            category="general",
            recurrence="daily",
            fixed_time=live_fixed or None,      # blank box -> None
        ))
        st.success(f"Added '{live_task_title}' to {chosen_pet}.")

# ---- Generate the schedule ----  (Scheduler reads the owner)
st.subheader("Today's Plan")
if st.button("Generate plan", key="live_generate"):
    scheduler = Scheduler()
    plan = scheduler.generate_daily_plan(owner)
    if plan:
        st.text(scheduler.explain_plan(plan, owner))
    else:
        st.warning("No tasks to schedule yet. Add some tasks above.")
