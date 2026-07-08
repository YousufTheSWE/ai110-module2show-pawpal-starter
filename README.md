# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule for Sam
========================================
08:00  Morning walk (Rex)  [priority 7, pending]
12:30  Give medicine (Whiskers)  [priority 9, pending]
18:00  Evening feeding (Rex)  [priority 5, pending]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
py -m pytest
```

Tests cover sorting and conflicts and some other methods.

Sample test output:

```
==================================== test session starts ====================================
platform win32 -- Python 3.14.0, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\yousu\Codepath\ai110-module2show-pawpal-starter
plugins: anyio-4.14.1
collected 5 items                                                                            

tests\test_pawpal.py .....                                                             [100%]

===================================== 5 passed in 0.02s =====================================
```

Based on the output, I would give a 5 star confidence rating.


## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
Sort by time	Scheduler.sort_by_time()	Earliest task first
Sort by priority	Scheduler.sort_by_priority()	Highest priority first
Filter by status	Scheduler.filter_by_status()	Done vs. pending
Filter by pet	Scheduler.filter_by_pet()	Tasks for one pet
Conflict detection	Scheduler.detect_conflicts()	Warns on same-time tasks; never crashes
Recurring task	Task.next_occurrence()	Builds next copy (+day/+week) via timedelta
Complete + recur	Scheduler.mark_complete()	Marks done, auto-adds next occurrence

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Put in pet name/species and add Pet. Do this for all pets first.
2. Put in tasks after specifying pet, make sure to watch out for any conflict notifications.
3. Check the schedule and see what is next and needs to done.
4. When a task is done, check it off in the current tasks area.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
