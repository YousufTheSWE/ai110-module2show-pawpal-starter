# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  - It will be based on a Owner, Pet, and Task model, where owner carries out a task on a pet.
- What classes did you include, and what responsibilities did you assign to each?
  - We will have Owner, which has basic information like name and pets underneath. Owner can execute task.
  - There will be Pet, which has the name of the pet.
  - Tasks will include the name of task (walk or give medicine), and the pet that needs the task done.

**b. Design changes**

- Did your design change during implementation?
  - Yes.
- If yes, describe at least one change and why you made it.
  - We created a Scheduler class in order to get tasks that need to be done now, and tasks that need to be done in the future.
  - An attribute was created to mark task as complete or incomplete, which can be done through Scheduler.
  
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  - It considers priority and time.
- How did you decide which constraints mattered most?
  - Mostly on priority, since its a direct matter of how much a task matters.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  - detect_conflicts() returns a list of strings and the UI renders them as warnings — the app never refuses to add a conflicting task.
- Why is that tradeoff reasonable for this scenario?
  - It's reasonable because the owner may be able to perform two tasks at the same time (for example, feeding two pets at once from the same bowl).

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
  - I used it for design, brainstorming, debugging, and refactoring for almost all files.
- What kinds of prompts or questions were most helpful?
  - Prompts with specific instructions and those that say "give a simple response". 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
  - Ai suggested making the schedule only show today's task.
- How did you evaluate or verify what the AI suggested?
  - I did not like the suggestion as owner's may be curious about what they needed to do tomorrow. So I enforced a design where the schedule showed all tasks.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
  - Conflict detection and correct sorting.
- Why were these tests important?
  - To ensure that owners know which task to do first, and if they need to do tasks simultaneosly.

**b. Confidence**

- How confident are you that your scheduler works correctly?
  - Very confident.
- What edge cases would you test next if you had more time?
  - Conflict Resolution of different owners at certain times.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
  - How helpful the AI was.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  - I'd double check the UI myself and maybe add some features related to tasks.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  - It's important to have a very solid design before attempting to code a system.
