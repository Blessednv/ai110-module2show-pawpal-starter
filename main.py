"""Demo script: a temporary testing ground to verify the PawPal+ backend
logic works in the terminal before connecting it to Streamlit."""

from pawpal_system import Owner, Pet, Task, Priority, Scheduler


def main():
    # 1. Create an owner with a daily time budget and a preferred start time.
    owner = Owner("Sam", available_time_minutes=90, preferences={"day_start": "07:30"})

    # 2. Create at least two pets and link them to the owner.
    biscuit = Pet("Biscuit", "Golden Retriever")
    alfie = Pet("Alfie", "Cat")
    owner.add_pet(biscuit)
    owner.add_pet(alfie)

    # 3. Add at least three tasks with different times across the pets.
    biscuit.add_task(Task("Morning walk", 30, Priority.HIGH, "exercise", "daily"))
    biscuit.add_task(Task("Breakfast", 10, Priority.HIGH, "feeding", "daily", fixed_time="07:30"))
    alfie.add_task(Task("Medication", 5, Priority.HIGH, "medication", "daily", fixed_time="08:00"))
    alfie.add_task(Task("Playtime", 20, Priority.LOW, "enrichment", "daily"))

    # 4. Generate and print today's schedule.
    scheduler = Scheduler()
    plan = scheduler.generate_daily_plan(owner)

    print(scheduler.explain_plan(plan, owner))


if __name__ == "__main__":
    main()
