# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

My UML contains four classes connected by two ownership relationships: `Owner` owns zero or more `Pet` objects, and each `Pet` holds zero or more `Task` objects. `Scheduler` sits outside that chain — it depends on `Owner` and `Pet` to do its work but does not own either. The first three classes are data containers; `Scheduler` is the pure logic layer.

Core User Actions:
1. Add a pet: 
The user can enter and save basic information about their pet (like name and species) so the system knows who it is planning for.

2. Schedule a walk (or other tasks): 
The user can input specific care tasks, such as a walk, and define constraints like how long the task takes and its priority level.

3. See today's tasks: 
The user can request the system to generate and display an organized daily plan that sorts and schedules these tasks for them.

- What classes did you include, and what responsibilities did you assign to each?

I included four classes. **Owner** holds the person's name, pet list, available time, and preferences — it manages who owns what. **Pet** holds the animal's name, species, and task list — it groups tasks by animal. **Task** is the core unit of work, storing everything the scheduler needs (duration, priority, category, recurrence, and an optional fixed time). **Scheduler** is a stateless logic engine that reads from `Owner` and `Pet` to sort, filter, resolve conflicts, and produce a daily plan with an explanation.

Below are building blocks for PawPal+:
1. The Owner Class
This represents the user managing the system.
Attributes (Information):
name (String): The owner's name.
pets (List): A collection of Pet objects belonging to this owner.
Methods (Actions):
add_pet(pet): Links a new Pet object to the owner.
get_pets(): Retrieves the list of pets.
2. The Pet Class
This represents the animal receiving care.
Attributes (Information):
name (String): The pet's name (e.g., Mochi).
species (String): Dog, cat, other.
tasks (List): A collection of Task objects associated with this specific pet.
Methods (Actions):
add_task(task): Assigns a new care task to the pet.
get_tasks(): Retrieves all tasks for this pet.
3. The Task Class
This is the core unit of work that needs to be scheduled.
Attributes (Information):
title (String): What the task is (e.g., Morning walk).
duration_minutes (Integer): How long the task takes.
priority (String/Enum): High, medium, or low.
is_completed (Boolean): Tracks if the task is done (defaults to False).
Methods (Actions):
mark_complete(): Toggles the completion status.
update_details(duration, priority): Allows editing the task constraints.
4. The Scheduler Class
This is the algorithmic engine of your backend. It doesn't represent a physical thing, but rather the business logic for organizing tasks.
Attributes (Information):
time_budget_minutes (Integer): The total time the owner has available for pet care today.
Methods (Actions):
generate_daily_plan(pet): The main function that pulls a pet's tasks, filters/sorts them based on constraints, and returns a schedule.
_sort_tasks_by_priority(tasks): An internal helper method to ensure high-priority items are scheduled first.

OR 

1. The Owner Class
This represents the user managing the system and holds their specific constraints.
Attributes (Information):
name (String): The owner's name.
pets (List): A collection of Pet objects belonging to this owner.
available_time_minutes (Integer): The total time the owner has available for pet care today.
preferences (Dictionary or List): Rules or specific owner preferences (e.g., "prefers morning walks" or "do not schedule tasks back-to-back").
Methods (Actions):
add_pet(pet): Links a new Pet object to the owner.
get_pets(): Retrieves the list of pets.
2. The Pet Class
This represents the animal receiving care.
Attributes (Information):
name (String): The pet's name (e.g., Mochi).  
species (String): Dog, cat, other.  
tasks (List): A collection of Task objects associated with this specific pet.
Methods (Actions):
add_task(task): Assigns a new care task to the pet.
get_tasks(): Retrieves all tasks for this pet.
3. The Task Class
This is the core unit of work that needs to be scheduled, including advanced constraints.
Attributes (Information):
title (String): What the task is (e.g., Morning walk).  
duration_minutes (Integer): How long the task takes.  
priority (String/Enum): High, medium, or low.  
category (String): The type of care (e.g., "feeding", "medication", "exercise").
recurrence (String): How often it happens (e.g., "daily", "weekly", "one-off").
fixed_time (String/Time): An optional specific time the task must occur (e.g., 08:00 for medication).
is_completed (Boolean): Tracks if the task is done (defaults to False).
Methods (Actions):
mark_complete(): Toggles the completion status.
update_details(duration, priority, fixed_time): Allows editing the task constraints.
4. The Scheduler Class
This is the algorithmic engine of your backend. It evaluates the constraints and outputs a smart schedule.
Attributes (Information):
(None explicitly required as state here; it pulls inputs directly from Owner and Pet objects)
Methods (Actions):
generate_daily_plan(owner, pet): The main function that evaluates the owner's available time against the pet's tasks and returns a final schedule.
_sort_tasks_by_priority(tasks): Helper method to ensure high-priority items are scheduled first.  
_filter_tasks(tasks, available_time): Helper method to drop low-priority tasks if the total duration exceeds the owner's time budget.
_resolve_conflicts(tasks): Helper method to handle overlapping time slots if multiple tasks have conflicting fixed_time requirements.  
explain_plan(): Generates a human-readable summary explaining the reasoning behind the generated schedule


**b. Design changes**

- Did your design change during implementation?

1b. Design changes
After an AI code review of the initial skeletons, I implemented several key architectural changes to prevent data errors and UI bottlenecks:
* Priority Enum: Converted the priority string into an Enum to prevent silent typing errors (e.g., mistyping "hgih" instead of "high"). I had `priority` as a plain string, but that
meant a typo like "hgih" would slip through silently and the task would never sort correctly. Using an Enum makes a bad value fail right away.
* Timeline Tracking: Added a scheduled_start: Optional[str] field to the Task class. While fixed_time is an input constraint, the system needed a way to record the actual assigned time to render a daily timeline on the UI. I  already had `fixed_time`, but
that's only the time a task *must* happen. I needed a separate field to store the time the scheduler actually *assigned*, so the UI can show a real timeline.
* Scheduler Logic Realignment: Identified a critical sorting bottleneck. The Scheduler must sort tasks by priority before filtering them by the owner's available time to ensure high-priority tasks are not accidentally dropped. I realized the scheduler has to
sort tasks by priority *before* filtering by available time. If it filters first, a high-priority task could get dropped just because lower-priority tasks used up the budget.

- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
