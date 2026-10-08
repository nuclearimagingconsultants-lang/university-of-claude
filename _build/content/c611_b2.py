# -*- coding: utf-8 -*-
"""CSCE 611 — Modules 03-07."""

MODULES = [

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "CPU Scheduling",
 "subtitle": "Deciding who runs, with no idea what will happen next.",
 "question": "How do you schedule jobs whose running times you do not know?",
 "outcomes": [
     "State the scheduling objectives and show they conflict.",
     "Analyse FIFO, SJF, round robin, and MLFQ.",
     "Explain why MLFQ approximates SJF without knowing job lengths.",
     "Explain priority inversion and inheritance.",
     "Explain how real schedulers handle multicore and fairness.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Objectives that conflict",
   "blurb": "You cannot optimise all of these at once."},

  {"t": "table", "kicker": "Metrics", "title": "What a scheduler could optimise",
   "header": ["Metric", "Definition", "Matters for"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Turnaround", "Completion − arrival", "Batch jobs, compiles"],
     ["Response time", "First run − arrival", "Interactive use"],
     ["Throughput", "Jobs completed per unit time", "Servers"],
     ["Fairness", "Each gets a proportional share", "Multi-user systems"],
     ["Predictability", "Bounded worst case", "<b>Real time</b>"],
   ],
   "note": "The conflict is the point: SJF optimises turnaround and starves "
           "long jobs, which destroys fairness."},

  {"t": "callout", "title": "The fundamental tension", "kind": "Key idea",
   "body": ["<b>Turnaround</b> wants to run short jobs first — finishing "
            "them quickly keeps the average low.",
            "<b>Response time</b> wants to switch frequently — so "
            "everything gets attention soon.",
            "<b>Throughput</b> wants to switch rarely — every switch "
            "costs a cold cache (Module 02).",
            "<b>Fairness</b> wants everyone to progress — which forbids "
            "always preferring short jobs.",
            "No policy wins on all four. Every scheduler is a position taken "
            "in this trade, and knowing which position is how you judge one."]},

  {"t": "section", "label": "Part 2", "title": "The basic policies",
   "blurb": "Each fixes the previous one's problem and creates a new one."},

  {"t": "table", "kicker": "Policies", "title": "Four policies, four failures",
   "header": ["Policy", "Rule", "Fixes", "Breaks"],
   "widths": [2.4, 3.2, 3.2, 3.3],
   "rows": [
     ["FIFO", "First come, first served", "Nothing — the baseline", "<b>Convoy effect</b>"],
     ["SJF", "Shortest job first", "Optimal turnaround", "Needs the future; starves long jobs"],
     ["STCF", "Preemptive SJF", "Arrivals mid-run", "Same two problems"],
     ["RR", "Fixed quantum, rotate", "<b>Response time</b>", "Worse turnaround"],
   ],
   "note": "The convoy effect is the most memorable: one long job at the "
           "front destroys everyone's turnaround."},

  {"t": "callout", "title": "SJF is optimal and unusable",
   "kind": "The problem to solve",
   "body": ["Shortest-job-first provably minimises average turnaround time. "
            "It is also unimplementable, because it requires knowing how long "
            "each job will run — which the kernel cannot know.",
            "And it <b>starves</b>: a long job never runs while short ones "
            "keep arriving.",
            "So the real question of this module is: <i>can we get SJF-like "
            "behaviour without knowing the future and without starvation?</i>",
            "The answer is yes, by observing the past. That is MLFQ."]},

  {"t": "section", "label": "Part 3", "title": "Multi-level feedback queues",
   "blurb": "Learning job behaviour from how it has behaved."},

  {"t": "code", "kicker": "MLFQ", "title": "The rules",
   "lang": "text", "code": """
Several queues, each at a different priority.

1. Higher priority runs first.
2. Same priority -> round robin among them.
3. A NEW job starts at the HIGHEST priority.
      (optimistic: assume it is short and interactive)
4. A job that uses its ENTIRE quantum drops one level.
      (it behaved like a CPU-bound job, so treat it as one)
5. A job that YIELDS before its quantum ends stays put.
      (it blocked on I/O -- interactive -- keep it responsive)
6. PERIODICALLY, move every job back to the top.
      (prevents starvation; handles jobs that change behaviour)
""",
   "caption": "Rules 4 and 5 infer job type from behaviour. Rule 6 is the "
              "aging that stops long jobs starving — and the one people "
              "forget.",
   "note": "Each rule fixes a specific failure. Walking through what breaks "
           "without each one is the clearest way to teach this."},

  {"t": "bullets", "kicker": "MLFQ", "title": "Why this approximates SJF",
   "items": [
     "Short and interactive jobs block quickly, so they <b>stay</b> at high "
     "priority (rule 5).",
     "",
     "Long CPU-bound jobs consume full quanta, so they <b>sink</b> (rule 4).",
     "",
     "The effect: short jobs run first — which is SJF — without "
     "ever being told how long anything will take.",
     "",
     "Rule 6 (periodic boost) prevents starvation and handles a job that "
     "changes character — a compile that becomes interactive.",
     "",
     "<b>Without rule 6, long jobs starve</b> under a steady stream of short "
     "ones.",
   ],
   "note": "The 'infer from behaviour instead of asking' idea generalises far "
           "beyond scheduling."},

  {"t": "callout", "title": "Gaming the scheduler", "kind": "The attack",
   "body": ["A process that issues a trivial I/O operation just before its "
            "quantum expires never fully consumes a quantum, so it never "
            "drops a level — and monopolises the CPU at top priority.",
            "This is a real attack, and the fix is <b>accounting over a "
            "window</b> rather than per quantum: track total CPU time used at "
            "a level and demote when the budget is exhausted, regardless of "
            "how it was split up.",
            "The general lesson: any scheduler that infers intent from "
            "behaviour can be manipulated by faking the behaviour. Measure "
            "cumulative resource use, not individual events."]},

  {"t": "section", "label": "Part 4", "title": "Priority inversion",
   "blurb": "A low-priority task blocking a high-priority one."},

  {"t": "code", "kicker": "The bug", "title": "How inversion happens",
   "lang": "text", "code": """
LOW  acquires lock L
MED  becomes runnable, preempts LOW   (higher priority)
HIGH becomes runnable, needs lock L -> BLOCKS on LOW

Now: HIGH waits on LOW.
     LOW cannot run, because MED keeps preempting it.
     MED -- which never touches L -- effectively blocks HIGH.

Priority order is INVERTED. HIGH runs only when MED finishes,
which could be never.

This shut down the Mars Pathfinder rover in 1997. The watchdog
kept resetting the system; the fix was uploaded from Earth.
""",
   "caption": "The Pathfinder case is the standard example because the fix "
              "— enabling priority inheritance — was deployed "
              "remotely to Mars.",
   "note": "The story makes it stick, and the mechanism is genuinely subtle."},

  {"t": "bullets", "kicker": "The fix", "title": "Priority inheritance",
   "items": [
     "When HIGH blocks on a lock held by LOW, <b>temporarily raise LOW to "
     "HIGH's priority</b>.",
     "",
     "LOW now preempts MED, finishes its critical section, releases the lock, "
     "and reverts.",
     "",
     "HIGH proceeds. The inversion window is bounded by the length of the "
     "critical section, not by MED's runtime.",
     "",
     "<b>Alternative:</b> priority ceiling — a lock carries the highest "
     "priority of any task that may take it, and the holder is raised "
     "immediately on acquisition.",
   ],
   "footnote": "Required in Project 1. Most real-time kernels implement one "
               "or the other."},

  {"t": "table", "kicker": "Reality", "title": "What real schedulers do",
   "header": ["Scheduler", "Approach", "Notable for"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Linux CFS", "Track virtual runtime; run the least-advanced", "Fairness without fixed quanta"],
     ["Linux EEVDF", "Latency-aware successor to CFS", "Bounded latency guarantees"],
     ["Windows", "Priority with boosts for I/O and foreground", "Interactive responsiveness"],
     ["Real time (EDF)", "Earliest deadline first", "Provable deadline guarantees"],
     ["Multicore", "Per-CPU run queues, periodic load balancing", "Affinity vs balance"],
   ],
   "note": "CFS is worth explaining: 'run whoever has had least CPU so far' "
           "is a very clean fairness definition."},

  {"t": "callout", "title": "Multicore scheduling adds a new trade",
   "kind": "Affinity",
   "body": ["A single global run queue means every CPU contends on one lock "
            "— a scalability disaster (CSCE 614 Module 11).",
            "So each CPU gets its own run queue, with periodic load "
            "balancing.",
            "Now a new tension: <b>cache affinity</b> says keep a process on "
            "the CPU whose cache holds its data; <b>load balance</b> says "
            "move it to an idle CPU.",
            "Migrating a process costs a cold cache — often more than "
            "the idle time it was meant to fill. Real schedulers migrate "
            "reluctantly, and NUMA makes the penalty larger still (CSCE 614 "
            "Module 07)."]},
 ],
 "takeaways": [
   "Turnaround, response time, throughput, fairness, and predictability "
   "conflict. Every scheduler is a position in that trade.",
   "SJF is optimal for turnaround, requires knowing the future, and starves "
   "long jobs — so it defines the goal rather than the solution.",
   "MLFQ infers job type from behaviour: jobs that block stay high, jobs that "
   "consume quanta sink. That approximates SJF with no foreknowledge.",
   "The periodic priority boost is what prevents starvation, and it is the "
   "rule people omit.",
   "Any scheduler that infers intent can be gamed. Account for cumulative CPU "
   "use, not individual quanta.",
   "Priority inheritance bounds inversion by the critical section length. It "
   "is what fixed Mars Pathfinder.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Objectives, and why they conflict"),
  ("table", ["Metric", "Definition", "Who cares"],
   [["<b>Turnaround time</b>", "Completion time minus arrival time.",
     "Batch work: compiles, renders, analyses."],
    ["<b>Response time</b>", "First time scheduled, minus arrival time.",
     "Interactive use. A shell that takes 200 ms to echo a keystroke is "
     "unusable regardless of its throughput."],
    ["<b>Throughput</b>", "Jobs completed per unit time.",
     "Servers and batch systems."],
    ["<b>Fairness</b>", "Each runnable job receives a proportional share.",
     "Multi-user and multi-tenant systems."],
    ["<b>Predictability</b>", "A bounded worst case.",
     "Real-time systems, where a late answer is a wrong answer."]],
   [0.20, 0.36, 0.44]),
  ("callout", "They pull against each other",
   ["Minimising <b>turnaround</b> means running short jobs first, which "
    "requires knowing which are short and which starves the long ones.",
    "Minimising <b>response time</b> means switching often, so everything "
    "gets attention quickly.",
    "Maximising <b>throughput</b> means switching rarely, because each switch "
    "costs a cold cache and a TLB flush (Module 02) — the direct "
    "opposite.",
    "<b>Fairness</b> forbids systematically preferring one class of job, "
    "which rules out pure shortest-first.",
    "No policy optimises all of them. Judging a scheduler means identifying "
    "which trade it has taken and whether that matches the workload."]),

  ("h1", "2 &nbsp; The basic policies"),
  ("table", ["Policy", "Rule", "Strength", "Failure"],
   [["<b>FIFO</b>", "Run to completion in arrival order.",
     "Trivial; no starvation.",
     "<b>Convoy effect</b>: one long job at the front delays everyone. "
     "Average turnaround is terrible."],
    ["<b>SJF</b>", "Run the shortest job first, to completion.",
     "<b>Provably optimal</b> average turnaround.",
     "Requires knowing job lengths. Starves long jobs. A long job that "
     "arrives first still blocks everything."],
    ["<b>STCF</b>", "Preemptive SJF: switch when a shorter job arrives.",
     "Handles arrivals during execution.",
     "Still needs the future; still starves."],
    ["<b>Round robin</b>", "Fixed quantum; rotate through runnable jobs.",
     "<b>Excellent response time</b>; obviously fair.",
     "Poor turnaround — everything finishes at roughly the same late "
     "time. Quantum too small and switch overhead dominates."]],
   [0.13, 0.28, 0.26, 0.33]),
  ("callout", "SJF defines the target, not the solution",
   ["Shortest-job-first minimises average turnaround time, and that is a "
    "theorem rather than an observation.",
    "It is also unimplementable: the kernel cannot know how long a process "
    "will run. And it starves long jobs indefinitely under a steady arrival "
    "of short ones.",
    "So the question this module actually answers is: <i>can a scheduler "
    "behave like SJF without knowing the future, and without "
    "starvation?</i> The answer is to infer job behaviour from its past, "
    "which is MLFQ."]),

  ("h1", "3 &nbsp; Multi-level feedback queues"),
  ("code", """Maintain several queues at descending priority.

RULE 1  A job in a higher queue runs before any job in a lower one.
RULE 2  Jobs in the same queue run round robin.
RULE 3  A new job enters at the HIGHEST priority.
RULE 4  If a job uses its entire quantum, it drops one level.
RULE 5  If a job yields before the quantum expires, it stays.
RULE 6  Periodically, move ALL jobs back to the highest queue."""),
  ("p", "Rules 4 and 5 do the work. A job that blocks for I/O before its "
        "quantum expires is interactive and keeps its high priority, so it "
        "responds quickly. A job that burns a full quantum is CPU-bound and "
        "sinks, so it does not interfere with interactive work."),
  ("callout", "Why this is SJF without clairvoyance",
   ["Short and interactive jobs block early and often, so rule 5 keeps them "
    "near the top and they are scheduled first — which is what SJF would "
    "have done.",
    "Long CPU-bound jobs consume whole quanta and sink under rule 4, so they "
    "run only when nothing shorter is waiting — again what SJF would "
    "have done.",
    "The scheduler has reproduced SJF's behaviour by <b>observing the past "
    "instead of predicting the future</b>, which is a general and transferable "
    "idea."]),
  ("h2", "3.1 &nbsp; Rule 6 is the one people forget"),
  ("p", "Without the periodic boost, a long-running job that has sunk to the "
        "bottom never rises again. Under a steady stream of short interactive "
        "jobs it starves permanently."),
  ("p", "The boost also handles jobs that <b>change character</b>: a compiler "
        "that spends ten minutes CPU-bound and then begins waiting for input "
        "should be treated as interactive from that point. Rule 6 gives it "
        "the chance to demonstrate its new behaviour."),
  ("callout", "Gaming the scheduler is a real attack",
   ["A process that issues a trivial I/O call just before its quantum expires "
    "never <i>fully</i> consumes a quantum, so rule 4 never demotes it. It "
    "sits at top priority indefinitely and monopolises the CPU.",
    "The fix is to account for CPU time <b>cumulatively</b> rather than per "
    "quantum: track the total time a job has used at its current level and "
    "demote when that budget is exhausted, however the usage was divided up.",
    "The general lesson applies well beyond scheduling: any policy that "
    "infers intent from observed behaviour can be manipulated by producing "
    "the behaviour deliberately. Measure cumulative resource consumption, not "
    "individual events."]),

  ("break",),
  ("h1", "4 &nbsp; Priority inversion"),
  ("code", """LOW   acquires lock L and begins its critical section.
MED   becomes runnable and preempts LOW (higher priority).
HIGH  becomes runnable, tries to take L, and BLOCKS.

HIGH is now waiting for LOW.
LOW cannot run because MED preempts it.
MED, which never touches L, is effectively blocking HIGH.

The priority ordering is inverted, and it persists for as long
as MED has work to do."""),
  ("callout", "Mars Pathfinder, 1997",
   ["The Pathfinder lander began resetting itself repeatedly on the Martian "
    "surface. A high-priority bus management task blocked on a mutex held by "
    "a low-priority meteorological task, while a medium-priority "
    "communications task kept the low-priority one off the CPU. The watchdog "
    "timer observed the high-priority task missing its deadline and reset the "
    "system.",
    "The VxWorks kernel supported priority inheritance; it had been disabled. "
    "Engineers reproduced the fault on the ground replica, identified the "
    "inversion, and uploaded a patch enabling inheritance — to Mars.",
    "It is the standard example because the diagnosis and the fix are both "
    "exactly this module's material, and because it demonstrates that "
    "scheduling subtleties have consequences beyond benchmark numbers."]),
  ("h2", "4.1 &nbsp; Inheritance and ceilings"),
  ("table", ["Mechanism", "How", "Effect"],
   [["<b>Priority inheritance</b>", "When a high-priority task blocks on a "
     "lock, the holder is temporarily raised to the blocked task's priority "
     "until it releases.",
     "The holder now preempts medium-priority tasks, finishes its critical "
     "section promptly, and the inversion window is bounded by the length of "
     "that critical section rather than by unrelated work."],
    ["<b>Priority ceiling</b>", "Each lock carries the highest priority of "
     "any task that may acquire it. A task is raised to that ceiling as soon "
     "as it takes the lock.",
     "Prevents inversion before it starts and also prevents certain deadlocks "
     "(Module 05). Requires knowing in advance which tasks use which locks."]],
   [0.20, 0.42, 0.38]),

  ("h1", "5 &nbsp; Real schedulers"),
  ("table", ["System", "Policy", "Idea"],
   [["<b>Linux CFS</b>", "Completely Fair Scheduler.",
     "Track each task's <i>virtual runtime</i> — CPU time received, "
     "scaled by weight — and always run whichever has the least. There "
     "is no fixed quantum: a task runs until it is no longer the least "
     "advanced. Fairness becomes a definition rather than an approximation."],
    ["<b>Linux EEVDF</b>", "Earliest Eligible Virtual Deadline First.",
     "CFS's successor, adding explicit latency targets so that interactive "
     "tasks get bounded response without sacrificing fairness."],
    ["<b>Windows</b>", "Priority-based with dynamic boosts.",
     "Threads get priority boosts on I/O completion and for foreground "
     "windows, decaying over time — tuned heavily for perceived "
     "interactive responsiveness."],
    ["<b>EDF</b>", "Earliest Deadline First.",
     "Real-time. Provably schedules any feasible task set on one CPU, "
     "provided total utilisation does not exceed 1. Used where deadlines are "
     "hard."]],
   [0.17, 0.28, 0.55]),
  ("h2", "5.1 &nbsp; Multicore"),
  ("callout", "Per-CPU queues, and a new trade",
   ["A single global run queue requires every CPU to take the same lock on "
    "every scheduling decision — exactly the contended-atomic "
    "scalability failure of CSCE 614 Module 11. Real kernels use per-CPU run "
    "queues with periodic load balancing.",
    "That creates a tension. <b>Cache affinity</b> argues for keeping a "
    "process on the CPU whose caches hold its working set. <b>Load "
    "balancing</b> argues for moving it to an idle CPU.",
    "Migrating costs a cold cache, which Module 02 noted is often the "
    "dominant context-switch cost — frequently more than the idle time "
    "the migration was meant to recover. On a NUMA machine it is worse still, "
    "because the process's pages remain on the old node and every access "
    "becomes remote (CSCE 614 Module 07).",
    "Real schedulers therefore migrate reluctantly, with hysteresis, and "
    "expose affinity controls for when the administrator knows better."]),
 ],
 "resources": [
   ("OSTEP — Chapters 7&ndash;10 (Scheduling, MLFQ, Lottery, "
    "Multiprocessor)",
    "https://pages.cs.wisc.edu/~remzi/OSTEP/",
    "The best free treatment of scheduling policy, and the source of the MLFQ "
    "rule formulation used here."),
   ("MIT 6.1810 — scheduling lecture and lab",
    "https://pdos.csail.mit.edu/6.1810/",
    "xv6's scheduler in code, and the lab that replaces it."),
   ("Jones — What really happened on Mars (free)",
    "https://www.cs.unc.edu/~anderson/teach/comp790/papers/mars_pathfinder_long_version.html",
    "The Pathfinder priority inversion, told by someone close to it. Short "
    "and worth reading in full."),
   ("Linux kernel documentation — CFS and EEVDF",
    "https://docs.kernel.org/scheduler/",
    "How a production scheduler is actually structured."),
 ],
 "exercises": [
   "Simulate FIFO, SJF, STCF, and round robin on the same set of jobs. "
   "Compute average turnaround and average response time for each and "
   "tabulate them.",
   "Demonstrate the convoy effect: construct a job set where FIFO's average "
   "turnaround is many times SJF's.",
   "Implement MLFQ in xv6, replacing the round-robin scheduler. Instrument it "
   "to record each process's queue level over time.",
   "Remove rule 6 from your MLFQ and construct a workload that starves a long "
   "job. Then restore the rule and show the starvation disappears.",
   "Write a process that games the scheduler by yielding just before its "
   "quantum expires. Demonstrate it monopolising the CPU, then implement "
   "cumulative accounting and show it no longer can.",
   "Construct priority inversion in xv6 with three processes and a lock. "
   "Measure the high-priority process's delay, then implement priority "
   "inheritance and measure again.",
   "Measure the cost of migrating a process between cores: pin a "
   "memory-intensive process to one core, then to another, and compare "
   "throughput immediately after the move.",
 ],
 "selfcheck": [
   "Name five scheduling metrics and give a pair that directly conflict, with "
   "the reason.",
   "Why is SJF optimal, and why is it unusable?",
   "State the six MLFQ rules and say which two infer job type.",
   "What goes wrong without the periodic priority boost?",
   "How can a process game MLFQ, and what accounting change prevents it?",
   "Describe priority inversion and explain how inheritance bounds it.",
   "Why do multicore schedulers use per-CPU run queues, and what new trade "
   "does that create?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Synchronization",
 "subtitle": "Making concurrent access to shared state correct.",
 "question": "How do you let many threads touch the same data safely?",
 "outcomes": [
     "Explain race conditions and critical sections.",
     "Implement a spinlock and explain what hardware support it needs.",
     "Explain why spinning is sometimes right and usually wrong.",
     "Use condition variables correctly, including why the wait is a loop.",
     "Choose between locks, lock-free structures, and message passing.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "An increment is not one operation."},

  {"t": "code", "kicker": "Race", "title": "Why counter++ is three operations",
   "lang": "asm", "code": """
counter++;      # looks atomic. It is not.

    ld   t0, counter     # 1. read
    addi t0, t0, 1       # 2. modify
    sd   t0, counter     # 3. write

Thread A              Thread B
  ld  t0 <- 5
                        ld  t0 <- 5       # same value!
  addi t0 = 6
                        addi t0 = 6
  sd  counter = 6
                        sd  counter = 6   # one increment LOST

Two increments, one result. The interleaving decides the answer,
and the interleaving is not under your control.
""",
   "caption": "A <b>race condition</b>: the result depends on timing. It will "
              "pass every test you write and fail in production.",
   "note": "Students know this abstractly. Showing the three instructions "
           "makes it concrete."},

  {"t": "bullets", "kicker": "Definitions", "title": "The vocabulary",
   "items": [
     "<b>Critical section</b> — code that accesses shared state and must "
     "not be interleaved.",
     "",
     "<b>Mutual exclusion</b> — at most one thread in the critical "
     "section at a time.",
     "",
     "A correct solution needs three properties:",
     ("<b>Safety</b> — never two threads inside.", 1),
     ("<b>Liveness</b> — a waiting thread eventually enters.", 1),
     ("<b>Bounded waiting</b> — no thread waits indefinitely while "
      "others repeatedly overtake it.", 1),
   ]},

  {"t": "section", "label": "Part 2", "title": "Building a lock",
   "blurb": "Software alone is not enough."},

  {"t": "callout", "title": "You need an atomic read-modify-write",
   "kind": "Why hardware is required",
   "body": ["A lock implemented with ordinary loads and stores has the same "
            "problem it is trying to solve: test-then-set is two operations, "
            "and two threads can both pass the test.",
            "Purely software solutions exist — Peterson's algorithm "
            "— but they do not generalise past two threads and they "
            "depend on memory ordering guarantees that modern hardware does "
            "not provide (CSCE 614 Module 12).",
            "So processors supply an <b>atomic read-modify-write</b>: "
            "<code>test-and-set</code>, <code>compare-and-swap</code>, or "
            "<code>fetch-and-add</code>. The hardware acquires the cache line "
            "exclusively and completes the whole operation without "
            "interruption.",
            "Every lock on every platform is built on one of these."]},

  {"t": "code", "kicker": "Spinlock", "title": "The simplest correct lock",
   "lang": "c", "code": """
void acquire(struct spinlock *lk) {
    push_off();                    // disable interrupts on this CPU
    while (__sync_lock_test_and_set(&lk->locked, 1) != 0)
        ;                          // spin until we see it was 0
    __sync_synchronize();          // memory barrier: no reordering
    lk->cpu = mycpu();             //   of the critical section
}                                  //   above the acquire

void release(struct spinlock *lk) {
    lk->cpu = 0;
    __sync_synchronize();          // barrier before releasing
    __sync_lock_release(&lk->locked);
    pop_off();                     // re-enable interrupts
}
""",
   "caption": "The barriers are not optional. Without them the compiler and "
              "the hardware may move critical-section accesses outside the "
              "lock (CSCE 614 Module 12).",
   "note": "Also note push_off: holding a spinlock with interrupts enabled "
           "risks deadlocking against your own interrupt handler."},

  {"t": "callout", "title": "Never hold a spinlock and sleep",
   "kind": "The rule",
   "body": ["A spinning thread burns a CPU doing nothing. That is acceptable "
            "only if the holder will release very soon.",
            "If the holder <b>sleeps</b> while holding the lock, every "
            "spinner burns a full CPU until it wakes — possibly "
            "milliseconds.",
            "Worse, on a single CPU, a spinner can prevent the holder from "
            "ever being scheduled. The system deadlocks completely.",
            "<b>Rule:</b> spinlocks protect short, non-blocking critical "
            "sections. Anything that might sleep needs a sleeping lock."]},

  {"t": "two", "kicker": "Two kinds", "title": "Spin or sleep",
   "lh": "Spinlock",
   "l": ["Busy-waits.",
         "No context switch — very low latency.",
         "Burns CPU while waiting.",
         "<b>Use when:</b> the critical section is a few instructions, on "
         "multicore, and cannot block.",
         ("Kernel data structures, queue manipulation.", 1)],
   "rh": "Sleeping lock (mutex)",
   "r": ["Blocks the thread; the scheduler runs something else.",
         "Context switch cost on both sides.",
         "Wastes nothing while waiting.",
         "<b>Use when:</b> the critical section may be long or may block.",
         ("Anything touching I/O, or any user-level code.", 1)],
   "note": "The practical rule: if the wait could exceed two context "
           "switches, sleep."},

  {"t": "section", "label": "Part 3", "title": "Condition variables",
   "blurb": "Waiting for a condition rather than for a lock."},

  {"t": "code", "kicker": "Condition variables", "title": "The pattern, and the loop",
   "lang": "c", "code": """
// CONSUMER
acquire(&lock);
while (queue_is_empty())        // <-- WHILE, never IF
    sleep(&queue, &lock);       // atomically: release lock, sleep;
                                //   reacquire lock on wake
item = dequeue();
release(&lock);

// PRODUCER
acquire(&lock);
enqueue(item);
wakeup(&queue);                 // wake waiters
release(&lock);
""",
   "caption": "<code>sleep</code> must release the lock and block "
              "<b>atomically</b>. If it did them separately, a wakeup "
              "arriving in between would be lost forever.",
   "note": "The lost-wakeup race is the classic bug and the reason sleep "
           "takes the lock as a parameter."},

  {"t": "callout", "title": "Why the wait is a while loop, not an if",
   "kind": "The thing everyone gets wrong",
   "body": ["Three independent reasons, any one of which is sufficient:",
            "<b>Spurious wakeups.</b> Some implementations may wake a thread "
            "with no corresponding signal. The specification permits it.",
            "<b>Multiple waiters.</b> <code>wakeup</code> may wake several "
            "threads for one item. Only one gets it; the rest must re-check "
            "and sleep again.",
            "<b>Stolen condition.</b> Between the wakeup and reacquiring the "
            "lock, a third thread may have taken the item.",
            "In all three cases, the condition must be re-tested after "
            "waking. <b>Always <code>while</code>.</b>"]},

  {"t": "table", "kicker": "Primitives", "title": "The synchronisation toolkit",
   "header": ["Primitive", "Use for", "Watch out for"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Spinlock", "Very short kernel critical sections", "Never sleep holding one"],
     ["Mutex", "General mutual exclusion", "Deadlock (Module 05)"],
     ["Condition variable", "Wait for a state change", "<b>Always use while</b>"],
     ["Semaphore", "Counting resources", "Easy to misuse; no owner"],
     ["RW lock", "Many readers, rare writers", "Writer starvation"],
     ["RCU", "Read-mostly, lock-free readers", "Complex; deferred reclamation"],
   ],
   "note": "RCU is worth a mention: it is how Linux achieves zero-cost reads "
           "on read-mostly structures."},

  {"t": "bullets", "kicker": "Advice", "title": "Writing correct concurrent code",
   "items": [
     "<b>Minimise sharing first.</b> Per-thread state combined at the end "
     "removes the problem instead of synchronising it.",
     "",
     "<b>Use a mutex</b> unless profiling says otherwise. Uncontended locks "
     "are cheap (CSCE 614 Module 12).",
     "",
     "<b>Establish a lock ordering</b> and document it. This is Module 05's "
     "main defence against deadlock.",
     "",
     "<b>Never invent a primitive</b> without a correctness argument.",
     "",
     "<b>Use ThreadSanitizer.</b> It finds races your tests will not.",
   ],
   "footnote": "Concurrency bugs pass tests. Reason, do not test your way to "
               "confidence."},
 ],
 "takeaways": [
   "<code>counter++</code> is three instructions, and the interleaving "
   "decides the answer. That is a race condition.",
   "Mutual exclusion needs safety, liveness, and bounded waiting — all "
   "three.",
   "Locks require an atomic read-modify-write from hardware; software-only "
   "solutions do not survive modern memory models.",
   "Spinlocks are for short non-blocking critical sections. Sleeping while "
   "holding one can deadlock the machine.",
   "<code>sleep</code> must release the lock and block atomically, or a "
   "wakeup arriving in between is lost forever.",
   "Always wait in a <code>while</code> loop: spurious wakeups, multiple "
   "waiters, and stolen conditions each require re-checking.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Race conditions"),
  ("code", """counter++;

// compiles to three separate instructions:
    ld   t0, counter        // read
    addi t0, t0, 1          // modify
    sd   t0, counter        // write"""),
  ("p", "Two threads executing this concurrently can interleave so that both "
        "read the same value, both increment it, and both write back the same "
        "result. Two increments produce one. The outcome depends on timing "
        "that neither thread controls."),
  ("p", "This is a <b>race condition</b>, and its defining practical "
        "property is that it is intermittent. The bad interleaving may occur "
        "once in a million executions, which means it passes every test and "
        "appears in production under load."),
  ("h2", "1.1 &nbsp; What a solution must provide"),
  ("table", ["Property", "Requirement"],
   [["<b>Safety (mutual exclusion)</b>",
     "Never more than one thread inside the critical section."],
    ["<b>Liveness (progress)</b>",
     "If no thread is in the critical section and some are waiting, one of "
     "them must eventually enter. No deadlock."],
    ["<b>Bounded waiting</b>",
     "A waiting thread is not overtaken indefinitely. No starvation."]],
   [0.34, 0.66]),
  ("p", "All three matter. A lock that is safe but can deadlock is not "
        "usable; one that is safe and live but permits a thread to wait "
        "forever while others repeatedly acquire is not fair."),

  ("h1", "2 &nbsp; Building a lock"),
  ("callout", "Why hardware support is necessary",
   ["The obvious lock — read the flag, and if it is clear, set it "
    "— has exactly the problem it is meant to solve. Two threads can "
    "both read 'clear' before either writes.",
    "Pure software solutions exist. Peterson's algorithm achieves mutual "
    "exclusion for two threads with only loads and stores. It does not "
    "generalise cleanly beyond two, and critically it depends on sequentially "
    "consistent memory, which no real processor provides (CSCE 614 "
    "Module 12). On actual hardware it requires explicit barriers to work at "
    "all.",
    "So processors provide an <b>atomic read-modify-write</b> instruction: "
    "test-and-set, compare-and-swap, or fetch-and-add. The hardware obtains "
    "the cache line in Modified state (CSCE 614 Module 11) and completes the "
    "entire operation before releasing it.",
    "Every lock on every platform is built on one of these primitives."]),
  ("code", """void acquire(struct spinlock *lk) {
    push_off();                          // disable interrupts, this CPU
    while (__sync_lock_test_and_set(&lk->locked, 1) != 0)
        ;                                // spin while it was already 1
    __sync_synchronize();                // barrier
    lk->cpu = mycpu();
}

void release(struct spinlock *lk) {
    lk->cpu = 0;
    __sync_synchronize();                // barrier
    __sync_lock_release(&lk->locked);
    pop_off();                           // restore interrupts
}"""),
  ("ul", ["<b>The barriers are mandatory.</b> Without them, the compiler or "
          "the processor may move loads and stores from inside the critical "
          "section to outside it. The lock would be acquired correctly and "
          "protect nothing. CSCE 614 Module 12 covers why.",
          "<b><code>push_off</code> disables interrupts.</b> If a thread "
          "holds a spinlock and an interrupt handler on the same CPU tries to "
          "take it, the handler spins forever waiting for a thread that "
          "cannot resume until the handler returns. Disabling interrupts "
          "while holding the lock prevents this self-deadlock."]),
  ("callout", "Never sleep while holding a spinlock",
   ["A spinning thread occupies a CPU doing no work. That is a reasonable "
    "trade only when the holder will release within a few hundred cycles "
    "— less than the cost of two context switches.",
    "If the holder blocks on I/O while holding the lock, every spinner burns "
    "an entire CPU for the duration — possibly milliseconds.",
    "On a uniprocessor it is worse than wasteful: the spinner never yields, "
    "so the holder is never scheduled, so the lock is never released. The "
    "system stops entirely.",
    "<b>Spinlocks protect short, non-blocking critical sections.</b> Anything "
    "that could sleep needs a sleeping lock."]),
  ("table", ["", "Spinlock", "Sleeping lock (mutex)"],
   [["While waiting", "Busy-waits, occupying a CPU.",
     "Blocks; the scheduler runs something else."],
    ["Latency to acquire", "Very low — no context switch.",
     "Two context switches."],
    ["Cost of waiting", "A whole CPU.", "Nothing."],
    ["Use when", "The critical section is a handful of instructions, you are "
     "on multicore, and the code cannot block.",
     "The critical section may be long, or may block on I/O, or you are in "
     "user space."],
    ["Typical use", "Kernel data structures, run queues, free lists.",
     "Essentially everything else."]],
   [0.17, 0.41, 0.42]),

  ("break",),
  ("h1", "3 &nbsp; Condition variables"),
  ("p", "A lock provides mutual exclusion. It does not provide a way to wait "
        "for a <i>condition</i> — for the queue to become non-empty, for "
        "a child to exit, for a buffer to have space. Polling in a loop while "
        "holding the lock would prevent anyone from ever making the condition "
        "true."),
  ("code", """// CONSUMER
acquire(&lock);
while (queue_is_empty())          // WHILE, not IF
    sleep(&queue, &lock);         // atomically release lock + block;
                                  // reacquire lock before returning
item = dequeue();
release(&lock);

// PRODUCER
acquire(&lock);
enqueue(item);
wakeup(&queue);
release(&lock);"""),
  ("callout", "sleep must release and block atomically",
   ["Suppose <code>sleep</code> released the lock and then blocked as two "
    "separate steps. A producer could run in the gap: it acquires the lock, "
    "enqueues an item, calls <code>wakeup</code> — and nobody is asleep "
    "yet, so the wakeup is discarded.",
    "The consumer then blocks, waiting for an event that has already "
    "happened. It sleeps forever with an item sitting in the queue.",
    "This is the <b>lost wakeup</b> problem, and it is why "
    "<code>sleep</code> takes the lock as a parameter: it holds a separate "
    "internal lock, marks the thread as sleeping, releases the caller's lock, "
    "and only then yields — so no wakeup can slip through the gap."]),
  ("h2", "3.1 &nbsp; Why the wait is a while loop"),
  ("callout", "Three independent reasons, each sufficient on its own",
   ["<b>Spurious wakeups.</b> Implementations are permitted to wake a thread "
    "with no corresponding signal, and some do — it simplifies the "
    "implementation and is explicitly allowed by POSIX and by the C++ "
    "standard.",
    "<b>Multiple waiters, one resource.</b> A <code>wakeup</code> may wake "
    "every waiter. One of them gets the item; the others find the queue empty "
    "again and must sleep.",
    "<b>Stolen condition.</b> Between being woken and successfully "
    "reacquiring the lock, a different thread may have entered and consumed "
    "the item.",
    "In every case the woken thread must <b>re-test the condition</b>. "
    "Writing <code>if</code> instead of <code>while</code> produces a bug "
    "that is rare, timing-dependent, and extremely difficult to reproduce "
    "— which is why it is worth learning as a reflex rather than as a "
    "judgement call."]),

  ("h1", "4 &nbsp; The toolkit"),
  ("table", ["Primitive", "Provides", "Hazards"],
   [["<b>Spinlock</b>", "Mutual exclusion by busy-waiting.",
     "Never sleep while holding one. Always disable interrupts if an "
     "interrupt handler may take the same lock."],
    ["<b>Mutex</b>", "Mutual exclusion by blocking.",
     "Deadlock (Module 05). Must be released by the thread that acquired it."],
    ["<b>Condition variable</b>", "Waiting for a state change, with a lock.",
     "<b>Always use <code>while</code>.</b> Signal while holding the lock to "
     "avoid races."],
    ["<b>Semaphore</b>", "A counter with atomic wait and post.",
     "No concept of an owner, so misuse is easy and priority inheritance is "
     "impossible. Good for counting resources; poor as a general mutex."],
    ["<b>Reader-writer lock</b>", "Concurrent readers, exclusive writers.",
     "Writer starvation under continuous read load. Often slower than a plain "
     "mutex unless reads are both frequent and long."],
    ["<b>RCU</b>", "Read-mostly structures with <i>zero-cost</i> readers.",
     "Readers take no lock at all; writers publish a new version and defer "
     "reclaiming the old one until all pre-existing readers have finished. "
     "Powerful, and complex. Heavily used in Linux."]],
   [0.21, 0.34, 0.45]),

  ("h1", "5 &nbsp; Practical advice"),
  ("ol", ["<b>Reduce sharing before synchronising it.</b> Per-thread state "
          "combined once at the end eliminates the problem rather than making "
          "it safe. CSCE 614 Module 11 showed this is also faster.",
          "<b>Use a plain mutex unless you have measured a need for "
          "something else.</b> Uncontended locks cost about twenty cycles; "
          "nearly all lock cost is contention cost.",
          "<b>Establish and document a lock ordering.</b> This is the main "
          "defence against deadlock, and Module 05 develops it.",
          "<b>Keep critical sections short</b>, and never perform I/O inside "
          "one if it can be avoided.",
          "<b>Do not invent synchronisation primitives</b> without a written "
          "correctness argument. This is the area where plausible reasoning "
          "is least reliable.",
          "<b>Run everything under ThreadSanitizer.</b> It detects races that "
          "no amount of testing will surface, because it reasons about "
          "happens-before rather than about observed outcomes."]),
 ],
 "resources": [
   ("OSTEP — Chapters 26&ndash;31 (Concurrency, Locks, Condition "
    "Variables, Semaphores)",
    "https://pages.cs.wisc.edu/~remzi/OSTEP/",
    "The clearest written treatment of locks and condition variables, "
    "including the lost-wakeup derivation."),
   ("xv6 book — Chapter 6 (Locking)",
    "https://pdos.csail.mit.edu/6.1810/2023/xv6/book-riscv-rev3.pdf",
    "Real spinlocks, including the interrupt and memory-barrier reasoning."),
   ("Paul McKenney — Is Parallel Programming Hard? (free book)",
    "https://mirrors.edge.kernel.org/pub/linux/kernel/people/paulmck/perfbook/perfbook.html",
    "The practitioner's reference, and the definitive treatment of RCU by its "
    "author."),
   ("Jeff Preshing — locks and lock-free programming",
    "https://preshing.com/",
    "Excellent on memory ordering in lock implementations. Pairs with "
    "CSCE 614 Module 12."),
 ],
 "exercises": [
   "Write a program where two threads increment a shared counter ten million "
   "times without synchronisation. Report the final value across twenty runs "
   "and observe the variation.",
   "Implement a spinlock with an atomic test-and-set. Verify it fixes the "
   "counter, then remove the memory barriers and look for reordering effects "
   "in the generated assembly.",
   "Deliberately sleep while holding a spinlock in xv6 on a single CPU and "
   "observe the deadlock. Explain precisely why it cannot recover.",
   "Implement a bounded producer-consumer queue with a mutex and two "
   "condition variables. Test with multiple producers and consumers.",
   "Change the condition variable wait from <code>while</code> to "
   "<code>if</code> and construct a workload that exposes the bug. This may "
   "take effort, which is itself the lesson.",
   "Implement the lost-wakeup bug by separating release and sleep into two "
   "steps, and demonstrate a consumer blocking forever with an item in the "
   "queue.",
   "Measure uncontended and contended mutex cost against spinlock cost at 1, "
   "2, 4, and 8 threads, with a short and a long critical section. Identify "
   "where each wins.",
   "Run any of the above under ThreadSanitizer and compare what it reports "
   "against what your tests found.",
 ],
 "selfcheck": [
   "Why is <code>counter++</code> not atomic, and what makes the resulting "
   "bug so hard to catch?",
   "Name the three properties a mutual exclusion solution must provide.",
   "Why can a lock not be built from ordinary loads and stores on real "
   "hardware?",
   "Give two reasons a spinlock implementation needs memory barriers, and one "
   "reason it disables interrupts.",
   "What happens if you sleep while holding a spinlock on a uniprocessor?",
   "Why must <code>sleep</code> release the lock and block atomically?",
   "Give three independent reasons a condition variable wait must be a "
   "<code>while</code> loop.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Deadlock",
 "subtitle": "Four conditions, and four ways to attack them.",
 "question": "Why do correctly-locked programs stop, and what do you do "
             "about it?",
 "outcomes": [
     "State the four necessary conditions for deadlock.",
     "Detect deadlock with a wait-for graph.",
     "Apply prevention, avoidance, detection, and the ostrich algorithm.",
     "Explain lock ordering and why it is the practical answer.",
     "Distinguish deadlock from livelock and starvation.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Four conditions",
   "blurb": "All four must hold. Break any one and deadlock is impossible."},

  {"t": "table", "kicker": "Coffman conditions", "title": "The four, and how to break each",
   "header": ["Condition", "Means", "Break it by"],
   "widths": [2.8, 4.4, 4.9],
   "rows": [
     ["Mutual exclusion", "A resource is held exclusively", "Lock-free structures; immutability"],
     ["Hold and wait", "Hold one, request another", "Acquire all at once, or release first"],
     ["No preemption", "A resource cannot be taken back", "Timeouts; rollback; trylock"],
     ["Circular wait", "A cycle of waiting", "<b>Global lock ordering</b>"],
   ],
   "note": "The last row is the one used in practice. The others are "
           "theoretically available and usually impractical."},

  {"t": "code", "kicker": "Deadlock", "title": "The classic two-lock deadlock",
   "lang": "c", "code": """
// Thread A                    // Thread B
acquire(&lock1);               acquire(&lock2);
acquire(&lock2);   <--------   acquire(&lock1);
  // ... work                    // ... work
release(&lock2);               release(&lock1);
release(&lock1);               release(&lock2);

A holds 1, wants 2.  B holds 2, wants 1.  Neither can proceed.

All four conditions present:
  mutual exclusion - locks are exclusive
  hold and wait    - each holds one and waits for another
  no preemption    - neither lock can be taken away
  circular wait    - A -> B -> A
""",
   "caption": "Both threads are individually correct. The bug exists only in "
              "their interaction, which is why code review of one function "
              "cannot find it.",
   "note": "The 'each function is correct in isolation' point is why "
           "deadlocks survive review."},

  {"t": "section", "label": "Part 2", "title": "The practical answer",
   "blurb": "Impose an order on locks and always take them in it."},

  {"t": "callout", "title": "Global lock ordering",
   "kind": "What actually works",
   "body": ["Define a total order on all locks — by address, by a "
            "documented hierarchy, by a numbered level — and require "
            "that every thread acquires locks in increasing order.",
            "A cycle requires some thread to acquire a lower-numbered lock "
            "while holding a higher-numbered one. If nobody ever does, "
            "<b>circular wait is impossible</b> and deadlock cannot occur.",
            "This costs nothing at run time and is checkable: a debug build "
            "can record the highest lock level held per thread and assert on "
            "violation. Linux's lockdep does exactly this.",
            "<b>The discipline is documenting the order.</b> An undocumented "
            "order is one someone will violate."]},

  {"t": "code", "kicker": "Ordering", "title": "Two ways to apply it",
   "lang": "c", "code": """
// 1. Order by address -- works when locks have no natural hierarchy
void transfer(Account *a, Account *b, int amount) {
    Account *first  = (a < b) ? a : b;      // consistent order
    Account *second = (a < b) ? b : a;
    acquire(&first->lock);
    acquire(&second->lock);
    ...
}

// 2. Order by level -- when there IS a hierarchy
//    filesystem (1) -> inode (2) -> buffer cache (3)
//    Never acquire a lower level while holding a higher one.
//    Assert it in debug builds.
""",
   "caption": "Ordering by address handles the common case of many "
              "interchangeable objects. Ordering by level handles layered "
              "subsystems.",
   "note": "The account-transfer example is the canonical one and appears in "
           "real banking code."},

  {"t": "section", "label": "Part 3", "title": "The other strategies",
   "blurb": "What you do when ordering is not available."},

  {"t": "table", "kicker": "Strategies", "title": "Four responses",
   "header": ["Strategy", "Idea", "Cost"],
   "widths": [2.6, 4.8, 4.7],
   "rows": [
     ["Prevention", "Make a condition structurally impossible", "Usually ordering; free"],
     ["Avoidance", "Refuse requests leading to unsafe states", "Needs advance knowledge; impractical"],
     ["Detection", "Let it happen; find cycles; recover", "Recovery means killing or rolling back"],
     ["Ostrich", "Ignore it; reboot if it happens", "<b>Honestly, what most systems do</b>"],
   ],
   "note": "Being honest that general-purpose OSes use the ostrich algorithm "
           "is more useful than pretending otherwise."},

  {"t": "callout", "title": "Why Banker's algorithm is not used",
   "kind": "Honest assessment",
   "body": ["Deadlock <i>avoidance</i> — the Banker's algorithm — "
            "requires each process to declare in advance the maximum "
            "resources it will ever need.",
            "No real program can do this. A process does not know how many "
            "file descriptors or locks it will need before it runs.",
            "It also costs an O(n²m) safety check on every resource "
            "request.",
            "<b>It is worth knowing as an idea</b> — the concept of a "
            "safe state is genuinely useful — and it is not used in any "
            "general-purpose operating system. Textbooks give it more space "
            "than its practical importance warrants."]},

  {"t": "bullets", "kicker": "Detection", "title": "When detection is the right answer",
   "items": [
     "<b>Databases</b> use detection, because they can.",
     ("A transaction can be rolled back and retried — that machinery "
      "already exists.", 1),
     ("Build a wait-for graph, find cycles, abort the cheapest victim.", 1),
     "",
     "<b>Operating systems</b> mostly cannot, because killing a process "
     "mid-operation leaves inconsistent state.",
     "",
     "<b>Debugging tools</b> use detection: lockdep in Linux, ThreadSanitizer "
     "in user space.",
     ("They detect <i>potential</i> deadlock from ordering violations even "
      "when no deadlock occurred.", 1),
   ],
   "note": "The lockdep point is important: it finds the bug on a run where "
           "the deadlock did not actually happen."},

  {"t": "section", "label": "Part 4", "title": "Related failures",
   "blurb": "Not everything that stops is deadlock."},

  {"t": "table", "kicker": "Distinguish", "title": "Three ways to make no progress",
   "header": ["Failure", "What happens", "Example"],
   "widths": [2.6, 4.8, 4.7],
   "rows": [
     ["Deadlock", "Threads blocked forever in a cycle", "Two locks, two threads, opposite order"],
     ["Livelock", "Threads <b>run</b> but make no progress", "Both back off and retry in lockstep"],
     ["Starvation", "One thread never gets a resource", "Writer blocked by continuous readers"],
   ],
   "note": "Livelock is the nastiest to diagnose because CPU usage looks "
           "healthy."},

  {"t": "callout", "title": "Livelock looks like work",
   "kind": "Hardest to diagnose",
   "body": ["In deadlock, threads are blocked and CPU use drops to zero "
            "— conspicuous, and easy to catch with a debugger.",
            "In <b>livelock</b>, threads are actively running: acquiring, "
            "detecting a conflict, backing off, retrying, conflicting again. "
            "CPU use is 100% and nothing is accomplished.",
            "The classic cause is a symmetric retry: both threads detect the "
            "conflict at the same moment, both release, both retry "
            "immediately, and the cycle repeats indefinitely.",
            "<b>Fix:</b> randomised exponential backoff — break the "
            "symmetry. The same fix as Ethernet collision handling, for "
            "exactly the same reason."]},

  {"t": "bullets", "kicker": "Practice", "title": "Avoiding deadlock in real code",
   "items": [
     "<b>Define a lock order and write it down</b> in the file that defines "
     "the locks.",
     "",
     "<b>Hold as few locks as possible</b>, for as short a time as possible.",
     "",
     "<b>Never call unknown code while holding a lock</b> — a callback "
     "or a virtual method may acquire anything.",
     "",
     "<b>Use <code>trylock</code> with backoff</b> where ordering is "
     "genuinely impossible.",
     "",
     "<b>Enable lockdep</b> (kernel) or ThreadSanitizer (user space) in test "
     "builds. They find ordering violations without needing the deadlock to "
     "occur.",
   ],
   "footnote": "The callback rule catches a large fraction of real "
               "deadlocks."},
 ],
 "takeaways": [
   "Deadlock requires all four Coffman conditions. Breaking any one makes it "
   "impossible.",
   "Global lock ordering breaks circular wait, costs nothing at run time, and "
   "is the answer used in practice.",
   "Order by address when locks are interchangeable; by documented level when "
   "there is a hierarchy.",
   "Banker's algorithm needs advance knowledge no real program has. Know the "
   "idea; do not expect to use it.",
   "Databases detect and roll back because that machinery exists. Operating "
   "systems largely use the ostrich algorithm and are honest about it.",
   "Livelock burns CPU while making no progress. Break the symmetry with "
   "randomised backoff.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The four conditions"),
  ("p", "Coffman's conditions are <b>necessary</b>: deadlock requires all "
        "four simultaneously. That makes them a checklist for defence — "
        "eliminate any one structurally and deadlock becomes impossible "
        "rather than unlikely."),
  ("table", ["Condition", "Statement", "How it could be broken"],
   [["<b>Mutual exclusion</b>", "At least one resource is held in a "
     "non-shareable mode.",
     "Use lock-free data structures, or immutable data that needs no "
     "exclusion. Rarely available in general."],
    ["<b>Hold and wait</b>", "A thread holding a resource requests another.",
     "Acquire everything needed in one atomic step, or release everything "
     "before requesting more. Hurts concurrency and is often impractical."],
    ["<b>No preemption</b>", "A resource cannot be forcibly taken from its "
     "holder.",
     "Use <code>trylock</code> and release on failure; or allow rollback. "
     "Databases do this."],
    ["<b>Circular wait</b>", "A cycle exists in the wait-for graph.",
     "<b>Impose a global ordering on locks</b> and always acquire in "
     "increasing order. This is the one used in practice."]],
   [0.20, 0.36, 0.44]),
  ("code", """// Thread A                 // Thread B
acquire(&lock1);            acquire(&lock2);
acquire(&lock2);            acquire(&lock1);
...                         ...
release(&lock2);            release(&lock1);
release(&lock1);            release(&lock2);"""),
  ("p", "Each thread is individually correct: it acquires what it needs, does "
        "its work, and releases in reverse order. The defect exists only in "
        "the <i>interaction</i>, which is why reviewing either function alone "
        "cannot find it and why deadlocks survive careful code review."),

  ("h1", "2 &nbsp; Lock ordering: the practical answer"),
  ("callout", "Break circular wait and the rest does not matter",
   ["Define a total order over all locks. Require every thread to acquire "
    "locks in strictly increasing order.",
    "For a cycle to form, some thread must be holding a higher-ordered lock "
    "while requesting a lower-ordered one. If the discipline is never "
    "violated, that cannot happen, so no cycle can form, so deadlock is "
    "<b>structurally impossible</b> — not merely unlikely.",
    "The run-time cost is zero. The cost is discipline, and discipline is "
    "enforceable: a debug build can record the highest-ordered lock each "
    "thread holds and assert when a lower one is requested. Linux's "
    "<b>lockdep</b> does exactly this, and it reports violations even on runs "
    "where no deadlock actually occurred."]),
  ("code", """// Ordering by address: for many interchangeable objects
void transfer(Account *a, Account *b, int amount) {
    Account *first  = (a < b) ? a : b;
    Account *second = (a < b) ? b : a;
    acquire(&first->lock);
    acquire(&second->lock);
    a->balance -= amount;
    b->balance += amount;
    release(&second->lock);
    release(&first->lock);
}

// Ordering by level: for layered subsystems
//    1. filesystem lock
//    2. inode lock
//    3. buffer cache lock
// Never acquire level N while holding level > N."""),
  ("p", "Address ordering handles the common case of many structurally "
        "identical objects — accounts, inodes, connections — where "
        "no natural hierarchy exists. Level ordering handles layered "
        "subsystems, and has the advantage of being documentable in a way "
        "humans can follow."),
  ("p", "<b>Write the order down</b>, in the header that declares the locks. "
        "An undocumented ordering is one that a new contributor will violate "
        "within a month, and the resulting bug will appear six months later "
        "under load."),

  ("break",),
  ("h1", "3 &nbsp; The four strategies"),
  ("table", ["Strategy", "Approach", "Assessment"],
   [["<b>Prevention</b>", "Make one of the four conditions structurally "
     "impossible.",
     "In practice this means lock ordering. Free at run time, enforceable in "
     "debug builds. <b>The right default.</b>"],
    ["<b>Avoidance</b>", "Analyse each request and refuse any that could lead "
     "to an unsafe state (Banker's algorithm).",
     "Requires each process to declare its maximum future resource needs in "
     "advance. No real program can. Not used in any general-purpose OS."],
    ["<b>Detection and recovery</b>", "Allow deadlock; periodically search "
     "the wait-for graph for cycles; break them.",
     "Requires a way to recover, which means killing or rolling back a "
     "participant. Databases can; operating systems generally cannot."],
    ["<b>The ostrich algorithm</b>", "Ignore the possibility. If the system "
     "hangs, reboot.",
     "<b>What general-purpose operating systems actually do</b>, and a "
     "defensible engineering decision: deadlocks are rare, detection is "
     "expensive, and recovery is often impossible anyway."]],
   [0.19, 0.38, 0.43]),
  ("callout", "On the Banker's algorithm",
   ["Textbooks devote considerable space to deadlock avoidance, and it is "
    "worth understanding the idea of a <b>safe state</b> — one from "
    "which some completion order exists for all processes.",
    "But the algorithm requires advance declaration of maximum resource "
    "needs, which no real program can supply, and it costs an "
    "O(n&#178;m) safety check on every request.",
    "It is not used in any general-purpose operating system. Knowing why it "
    "is impractical is more useful than being able to execute it."]),
  ("h2", "3.1 &nbsp; Where detection is right"),
  ("ul", ["<b>Databases</b> detect and recover, because the machinery already "
          "exists: a transaction can be aborted and retried, and users expect "
          "that. The system builds a wait-for graph among transactions, finds "
          "cycles, and aborts the cheapest victim — typically the one "
          "holding the fewest locks or having done the least work.",
          "<b>Operating systems</b> generally cannot, because killing a "
          "process in the middle of a kernel operation leaves data structures "
          "half-updated with no way to roll back.",
          "<b>Debugging tools</b> are the important exception: lockdep in the "
          "Linux kernel and ThreadSanitizer in user space detect <i>ordering "
          "violations</i>, which are evidence of a potential deadlock, even "
          "on executions where no deadlock occurred. This is far more useful "
          "than detecting the deadlock itself, because it finds the bug "
          "before a customer does."]),

  ("h1", "4 &nbsp; Deadlock, livelock, starvation"),
  ("table", ["Failure", "Behaviour", "CPU use", "Cause"],
   [["<b>Deadlock</b>", "Threads blocked permanently in a cycle.",
     "Zero — conspicuous.",
     "All four Coffman conditions hold."],
    ["<b>Livelock</b>", "Threads run continuously and accomplish nothing.",
     "<b>100% — looks healthy.</b>",
     "Symmetric detect-and-retry with no backoff."],
    ["<b>Starvation</b>", "One thread never obtains a resource while others "
     "proceed.", "Normal.",
     "An unfair policy: continuous readers blocking a writer, or a scheduler "
     "without aging (Module 03)."]],
   [0.17, 0.33, 0.20, 0.30]),
  ("callout", "Livelock is the hardest to diagnose",
   ["A deadlocked system is obviously stuck: CPU use falls to nothing and a "
    "debugger shows every thread blocked.",
    "A livelocked system is at full utilisation with every thread actively "
    "executing. Monitoring shows a busy, healthy machine doing no work. The "
    "classic cause is perfect symmetry: two threads detect a conflict at the "
    "same instant, both release their resources, both retry immediately, and "
    "they collide again.",
    "The fix is to <b>break the symmetry</b> with randomised exponential "
    "backoff — each retry waits a random interval, growing with each "
    "failure. This is exactly Ethernet's collision resolution, for exactly "
    "the same reason, and it works for the same reason: randomness makes "
    "repeated collision exponentially unlikely."]),

  ("h1", "5 &nbsp; Rules for real code"),
  ("ol", ["<b>Define a lock order and document it</b> in the header where the "
          "locks are declared.",
          "<b>Hold the fewest locks for the shortest time.</b> Every "
          "additional simultaneously-held lock multiplies the opportunities "
          "for a cycle.",
          "<b>Never call unknown code while holding a lock.</b> A callback, a "
          "virtual method, or a plugin may acquire any lock at all, including "
          "one you hold. This single rule prevents a large fraction of real "
          "deadlocks and is the one most often broken.",
          "<b>Use <code>trylock</code> with backoff</b> where a consistent "
          "ordering is genuinely unavailable — but prefer fixing the "
          "ordering.",
          "<b>Enable lockdep or ThreadSanitizer in test builds.</b> They find "
          "ordering violations without requiring the deadlock to occur, which "
          "is the only reliable way to catch these before production."]),
 ],
 "resources": [
   ("OSTEP — Chapter 32 (Common Concurrency Problems)",
    "https://pages.cs.wisc.edu/~remzi/OSTEP/",
    "Deadlock and the non-deadlock bugs, with a study of what actually occurs "
    "in real code."),
   ("Linux kernel documentation — lockdep",
    "https://docs.kernel.org/locking/lockdep-design.html",
    "How runtime lock-order validation works. Worth reading for the design "
    "even if you never use Linux."),
   ("Coffman, Elphick & Shoshani — System Deadlocks (1971)",
    "https://dl.acm.org/doi/10.1145/356586.356588",
    "The paper that identified the four conditions."),
   ("xv6 book — Chapter 6 (Locking), deadlock discussion",
    "https://pdos.csail.mit.edu/6.1810/2023/xv6/book-riscv-rev3.pdf",
    "xv6's lock ordering and why it is documented where it is."),
 ],
 "exercises": [
   "Write a program with two threads and two locks that deadlocks "
   "reproducibly. Attach a debugger and inspect both threads' stacks.",
   "Fix it with address-based lock ordering. Verify by running it a million "
   "times.",
   "Implement a bank transfer function for N accounts with M threads doing "
   "random transfers. Demonstrate the deadlock without ordering and its "
   "absence with ordering.",
   "Implement a wait-for graph and a cycle detector. Run it periodically "
   "against a deadlocking program and report the cycle it finds.",
   "Implement a lock-order validator: record the highest-level lock each "
   "thread holds and assert on violations. Test it against deliberately "
   "wrong code.",
   "Construct a livelock: two threads that each acquire one lock, detect the "
   "other is held, release, and retry immediately. Observe 100% CPU with no "
   "progress, then fix it with randomised backoff.",
   "Construct starvation: a reader-writer lock under continuous read load "
   "where the writer never proceeds. Then implement writer-preference and "
   "show it resolves.",
 ],
 "selfcheck": [
   "State the four Coffman conditions and give one way to break each.",
   "Why does global lock ordering make deadlock structurally impossible "
   "rather than merely unlikely?",
   "When would you order locks by address and when by level?",
   "Why is the Banker's algorithm not used in real operating systems?",
   "Why can databases use detection and recovery while operating systems "
   "largely cannot?",
   "Distinguish deadlock, livelock, and starvation, and say which is hardest "
   "to notice from monitoring.",
   "Why is 'never call unknown code while holding a lock' such an effective "
   "rule?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Memory Allocation",
 "subtitle": "Handing out memory, and the fragmentation that follows.",
 "question": "Why is malloc hard, and why is it fast anyway?",
 "outcomes": [
     "Explain internal and external fragmentation.",
     "Compare first fit, best fit, and segregated free lists.",
     "Explain buddy and slab allocation and where each is used.",
     "Explain why allocator performance depends on usage pattern.",
     "Explain arena and pool allocation and when to use them.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "Variable sizes, arbitrary lifetimes, and no advance notice."},

  {"t": "bullets", "kicker": "The job", "title": "What an allocator must do",
   "items": [
     "Satisfy requests of <b>arbitrary size</b>, in <b>arbitrary order</b>, "
     "with <b>arbitrary lifetimes</b>.",
     "",
     "Never move an allocation — the caller holds a raw pointer.",
     ("This is the constraint that makes compaction impossible and "
      "fragmentation inevitable.", 1),
     "",
     "Be fast. <code>malloc</code> is called constantly and shows up in "
     "profiles.",
     "",
     "Be space-efficient: minimise both bookkeeping overhead and wasted "
     "space.",
   ],
   "note": "The 'cannot move' constraint is what separates C allocators from "
           "garbage collectors, and it is worth stating first."},

  {"t": "two", "kicker": "Fragmentation", "title": "Two kinds, two causes",
   "lh": "Internal",
   "l": ["Wasted space <b>inside</b> an allocation.",
         "Ask for 33 bytes, get a 48-byte block.",
         "Caused by size classes and alignment.",
         ("Predictable and bounded.", 1),
         ("Reduce with finer size classes.", 1)],
   "rh": "External",
   "r": ["Wasted space <b>between</b> allocations.",
         "Plenty free, none contiguous enough.",
         "Caused by mixed sizes and lifetimes.",
         ("Unpredictable; depends on history.", 1),
         ("Cannot be fixed without moving — which you cannot do.", 1)],
   "note": "External fragmentation being unfixable without relocation is the "
           "central difficulty."},

  {"t": "callout", "title": "Allocation is an online problem",
   "kind": "Why it is hard",
   "body": ["If you knew every future request in advance, optimal placement "
            "would be computable.",
            "You do not. Each decision is made without knowing what comes "
            "next, and a decision that looks fine now may strand memory "
            "later.",
            "This is an <b>online algorithm</b> problem, and online "
            "algorithms are judged by competitive ratio against the "
            "offline optimum.",
            "No allocator is optimal for all workloads, which is why there "
            "are many and why 'which allocator is best' has no answer without "
            "naming the program."]},

  {"t": "section", "label": "Part 2", "title": "Placement policies",
   "blurb": "Given a free list, which block do you use?"},

  {"t": "table", "kicker": "Policies", "title": "Choosing a block",
   "header": ["Policy", "Rule", "Behaviour"],
   "widths": [2.6, 4.2, 5.3],
   "rows": [
     ["First fit", "First block large enough", "Fast; fragments the front of the list"],
     ["Next fit", "Resume scanning from last position", "Spreads wear; worse locality"],
     ["Best fit", "Smallest block that fits", "Less waste per block; <b>many tiny slivers</b>"],
     ["Worst fit", "Largest block", "Leaves usable remainders; destroys large blocks"],
     ["Segregated", "Separate lists per size class", "<b>O(1); what real allocators do</b>"],
   ],
   "note": "Best fit being worse than first fit in practice surprises people "
           "and is a good lesson about intuition."},

  {"t": "callout", "title": "Best fit is usually worse than first fit",
   "kind": "Counterintuitive",
   "body": ["Best fit minimises the leftover from each individual allocation, "
            "which sounds obviously right.",
            "The leftovers are therefore as small as possible — and "
            "small leftovers are <b>useless</b>. The heap accumulates "
            "thousands of fragments too small to satisfy anything.",
            "First fit leaves larger, more usable remainders and scans less, "
            "so it is typically both faster and less fragmenting.",
            "A good reminder that locally optimal decisions can be globally "
            "poor — the same lesson as greedy algorithms in CSCE 629 "
            "Module 09."]},

  {"t": "section", "label": "Part 3", "title": "Real allocators",
   "blurb": "Size classes, and specialisation."},

  {"t": "bullets", "kicker": "Segregated lists", "title": "How malloc is actually fast",
   "items": [
     "Keep a separate free list per <b>size class</b> — 16, 32, 48, 64 "
     "bytes, and so on.",
     "",
     "Allocation: round the request up to a class, pop the head of that list. "
     "<b>O(1).</b>",
     "Free: push onto the matching list. <b>O(1).</b>",
     "",
     "Cost: internal fragmentation, bounded by the class spacing.",
     "",
     "Large allocations bypass this entirely and go to <code>mmap</code>.",
     ("Which is why freeing a large block returns memory to the OS and "
      "freeing a small one usually does not.", 1),
   ],
   "note": "The large-allocation-bypass explains a common observed behaviour "
           "and is worth mentioning."},

  {"t": "table", "kicker": "Specialised", "title": "Allocators for known patterns",
   "header": ["Allocator", "Idea", "Used for"],
   "widths": [2.6, 4.8, 4.7],
   "rows": [
     ["Buddy", "Split and merge power-of-two blocks", "Kernel page allocation"],
     ["Slab", "Pre-initialised caches of one object type", "Kernel objects: inodes, PCBs"],
     ["Arena/region", "Bump-allocate; free everything at once", "Per-request, per-frame"],
     ["Pool", "Fixed-size objects, free list", "Particles, nodes, entities"],
     ["Stack", "LIFO only", "Scratch space within a scope"],
   ],
   "note": "Arena allocation is the one game and server code should use far "
           "more than it does."},

  {"t": "callout", "title": "Arena allocation: the biggest practical win",
   "kind": "Worth knowing",
   "body": ["Allocate a large block. Satisfy requests by bumping a pointer. "
            "Free <b>everything at once</b> by resetting the pointer.",
            "<b>Allocation is three instructions.</b> Free is one. There is "
            "no free list, no coalescing, no fragmentation, and no "
            "per-allocation metadata.",
            "It works whenever allocations share a lifetime: everything for "
            "one HTTP request, one frame, one parse, one compilation unit.",
            "That covers an enormous fraction of real allocation. Replacing "
            "general-purpose <code>malloc</code> with an arena in a hot path "
            "is frequently a several-fold improvement — and the code "
            "usually gets simpler, because nothing needs individual freeing."]},

  {"t": "bullets", "kicker": "Multicore", "title": "Why allocators have per-thread caches",
   "items": [
     "A single global heap lock is a contended atomic — CSCE 614 Module "
     "11's scalability failure.",
     "",
     "So modern allocators give each thread a <b>private cache</b> of free "
     "blocks.",
     ("Most allocations and frees touch no shared state at all.", 1),
     "",
     "Complication: a block allocated on thread A may be freed on thread B.",
     ("Handled by remote free lists, batched back to the owner.", 1),
     "",
     "This is why tcmalloc, jemalloc, and mimalloc exist and beat the system "
     "allocator on threaded workloads.",
   ]},

  {"t": "table", "kicker": "Choosing", "title": "Which allocator",
   "header": ["Situation", "Use"],
   "widths": [5.6, 6.5],
   "rows": [
     ["General-purpose, unknown pattern", "The system allocator; measure before replacing"],
     ["Many threads allocating heavily", "jemalloc, tcmalloc, or mimalloc"],
     ["Allocations share a lifetime", "<b>Arena</b> — usually the biggest win"],
     ["Many identical objects", "Pool or slab"],
     ["Real-time, bounded latency required", "Pre-allocate; never call malloc in the hot path"],
   ],
   "footnote": "The last row matters for audio, control systems, and game "
               "frame loops."},
 ],
 "takeaways": [
   "An allocator cannot move allocations, because callers hold raw pointers. "
   "That is why external fragmentation is unfixable.",
   "Internal fragmentation is waste inside a block and is bounded; external "
   "is waste between blocks and depends on history.",
   "Allocation is an online problem — no allocator is best for all "
   "workloads, which is why there are many.",
   "Best fit is usually worse than first fit, because minimal leftovers are "
   "useless leftovers.",
   "Real allocators use segregated free lists for O(1) allocation, trading "
   "bounded internal fragmentation for speed.",
   "Arena allocation — bump a pointer, free everything at once — is "
   "the largest easy win when allocations share a lifetime.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What makes allocation hard"),
  ("p", "A general-purpose allocator must satisfy requests of arbitrary size, "
        "arriving in arbitrary order, with arbitrary and unknown lifetimes "
        "— and it must be fast, because <code>malloc</code> appears in "
        "the profile of almost every program."),
  ("callout", "The constraint that makes it genuinely hard",
   ["<b>An allocation can never be moved.</b> The caller holds a raw pointer, "
    "possibly copied into other structures, and the allocator has no way to "
    "find and update those copies.",
    "A garbage-collected runtime <i>can</i> move objects, because it knows "
    "where every reference lives. That is precisely why compacting collectors "
    "can eliminate fragmentation entirely and C allocators cannot.",
    "Everything difficult about <code>malloc</code> follows from this one "
    "restriction."]),
  ("h2", "1.1 &nbsp; Two fragmentations"),
  ("table", ["", "Internal fragmentation", "External fragmentation"],
   [["What", "Wasted space <i>inside</i> an allocated block.",
     "Wasted space <i>between</i> allocated blocks."],
    ["Example", "A 33-byte request served by a 48-byte size class wastes 15 "
     "bytes.",
     "Several free blocks totalling 10 KB, none individually large enough for "
     "a 4 KB request."],
    ["Cause", "Size classes, alignment requirements, per-block headers.",
     "Interleaved allocation and freeing of mixed sizes with mixed lifetimes."],
    ["Predictability", "Bounded and computable from the size classes.",
     "Depends on the entire allocation history. Essentially unpredictable."],
    ["Fix", "Finer size classes, at the cost of more lists.",
     "<b>Requires moving allocations</b> — which is forbidden. Can only "
     "be mitigated."]],
   [0.15, 0.42, 0.43]),
  ("callout", "Allocation is an online problem",
   ["Given the complete sequence of future requests, optimal placement could "
    "be computed. The allocator does not have it: each decision is made "
    "blind, and a placement that is fine now may strand memory later.",
    "This is an <b>online algorithm</b> in the sense of CSCE 629, judged by "
    "its competitive ratio against the offline optimum, and no online "
    "allocator is optimal across all workloads.",
    "That is why many allocators exist and why 'which allocator is fastest' "
    "has no answer without naming the program. Measure on your workload."]),

  ("h1", "2 &nbsp; Placement policies"),
  ("table", ["Policy", "Rule", "Behaviour in practice"],
   [["<b>First fit</b>", "Scan from the start; take the first block large "
     "enough.",
     "Fast in the common case. Tends to fragment the front of the list, which "
     "then has to be scanned repeatedly."],
    ["<b>Next fit</b>", "Like first fit, but resume scanning where the last "
     "search ended.",
     "Spreads allocations across the heap. Usually <i>worse</i>, because it "
     "destroys locality."],
    ["<b>Best fit</b>", "Scan everything; take the smallest block that fits.",
     "Minimises per-allocation waste and produces many unusably small "
     "remainders. Slow, because it scans the whole list."],
    ["<b>Worst fit</b>", "Take the largest block.",
     "Leaves large usable remainders and consumes the big blocks you will "
     "later need. Rarely used."],
    ["<b>Segregated free lists</b>", "One list per size class; take from the "
     "matching list.",
     "<b>O(1).</b> What real allocators do."]],
   [0.19, 0.36, 0.45]),
  ("callout", "Best fit is usually worse than first fit",
   ["Best fit sounds obviously correct: minimise the waste on every "
    "allocation.",
    "The consequence is that every leftover is as small as possible — "
    "and a very small leftover is useless. The heap fills with thousands of "
    "fragments too small to satisfy any request, which is external "
    "fragmentation in its purest form.",
    "First fit leaves larger, more reusable remainders and scans far less. It "
    "is typically both faster and less fragmenting.",
    "This is the same lesson as greedy algorithms in CSCE 629 Module 09: a "
    "locally optimal choice is not globally optimal, and the plausible rule "
    "needs an argument rather than an intuition."]),

  ("break",),
  ("h1", "3 &nbsp; How real allocators work"),
  ("h2", "3.1 &nbsp; Segregated free lists"),
  ("p", "Maintain a separate free list for each <b>size class</b> — 16, "
        "32, 48, 64, 80 bytes, and so on, often with geometric spacing above "
        "some threshold."),
  ("ul", ["<b>Allocate:</b> round the request up to the next class, pop the "
          "head of that list. O(1), a handful of instructions.",
          "<b>Free:</b> push onto the list for that block's class. O(1).",
          "<b>Cost:</b> internal fragmentation bounded by the class spacing "
          "— at most 15 bytes with 16-byte spacing.",
          "<b>Large allocations bypass the mechanism</b> and go straight to "
          "<code>mmap</code>. This is why freeing a very large allocation "
          "often returns memory to the operating system immediately, while "
          "freeing many small ones usually does not."]),
  ("h2", "3.2 &nbsp; Specialised allocators"),
  ("table", ["Allocator", "Mechanism", "Where used"],
   [["<b>Buddy</b>", "Memory is split into power-of-two blocks. A block is "
     "halved repeatedly until the right size is reached; on free, a block is "
     "merged with its 'buddy' if that is also free.",
     "Kernel physical page allocation. Coalescing is O(log n) and finding the "
     "buddy is a single XOR."],
    ["<b>Slab</b>", "A cache per <i>object type</i>, holding pre-initialised "
     "objects. Allocation returns one that is already constructed.",
     "Kernel objects created and destroyed constantly: inodes, file "
     "structures, process control blocks. Avoids repeated initialisation and "
     "keeps objects cache-aligned."],
    ["<b>Arena / region</b>", "Bump a pointer. Free everything at once by "
     "resetting it.", "Per-request, per-frame, per-parse. See below."],
    ["<b>Pool</b>", "Fixed-size objects with a simple free list.",
     "Particles, tree nodes, entities — anywhere objects are "
     "homogeneous."],
    ["<b>Stack</b>", "Strictly LIFO allocation and deallocation.",
     "Scratch buffers within a scope. Trivially fast and trivially "
     "constrained."]],
   [0.17, 0.44, 0.39]),
  ("callout", "Arena allocation is the largest easy win available",
   ["Allocate one large block up front. Satisfy each request by returning the "
    "current pointer and advancing it. Release everything in one operation by "
    "resetting the pointer to the start.",
    "Allocation is three instructions. Deallocation is one. There is no free "
    "list, no coalescing, no search, no per-allocation header, and no "
    "fragmentation of any kind.",
    "It applies whenever a set of allocations <b>shares a lifetime</b>: "
    "everything needed to serve one HTTP request, to render one frame, to "
    "parse one document, to compile one translation unit. That describes a "
    "very large fraction of real allocation.",
    "Replacing general-purpose <code>malloc</code> with an arena in a hot "
    "path is routinely a several-fold speedup, and the surrounding code "
    "usually becomes <i>simpler</i>, because individual objects no longer "
    "need to be freed and ownership questions disappear."]),

  ("h1", "4 &nbsp; Allocators on multicore"),
  ("p", "A single global heap protected by one lock is precisely the "
        "contended-atomic scalability failure of CSCE 614 Module 11: every "
        "thread competes for one cache line, and adding cores makes it "
        "worse."),
  ("p", "Modern allocators therefore give each thread a <b>private cache</b> "
        "of free blocks, refilled in batches from a shared pool. The great "
        "majority of allocations and frees then touch no shared state at "
        "all."),
  ("p", "The complication is that a block allocated on thread A may be freed "
        "on thread B. Allocators handle this with per-thread remote free "
        "lists, batching freed blocks back to their owning thread "
        "periodically rather than synchronising on each one. This is the "
        "design behind tcmalloc, jemalloc, and mimalloc, and it is why they "
        "substantially outperform older system allocators on threaded "
        "workloads."),

  ("h1", "5 &nbsp; Choosing"),
  ("table", ["Situation", "Recommendation"],
   [["General purpose, unknown allocation pattern.",
     "Use the system allocator. Measure before replacing it — modern "
     "ones are good."],
    ["Many threads allocating heavily.",
     "jemalloc, tcmalloc, or mimalloc. Often a large improvement for a "
     "one-line change."],
    ["A set of allocations sharing a lifetime.",
     "<b>An arena.</b> Usually the single biggest win, and it simplifies "
     "ownership."],
    ["Many objects of one type.",
     "A pool or slab allocator."],
    ["Hard latency bounds — audio, control loops, game frame loops.",
     "Pre-allocate everything. Never call <code>malloc</code> in the hot "
     "path: a general allocator's worst case is unbounded, and the "
     "occasional slow allocation is exactly what blows a frame budget."]],
   [0.42, 0.58]),
 ],
 "resources": [
   ("OSTEP — Chapter 17 (Free-Space Management)",
    "https://pages.cs.wisc.edu/~remzi/OSTEP/",
    "Placement policies, coalescing, buddy and slab allocation, with worked "
    "examples."),
   ("Wilson et al. — Dynamic Storage Allocation: A Survey and Critical "
    "Review (free)",
    "https://www.cs.northwestern.edu/~pdinda/ics-s05/doc/dsa.pdf",
    "The definitive survey, and unusually sharp about how much allocator "
    "research measured the wrong things."),
   ("Bonwick — The Slab Allocator (free)",
    "https://people.eecs.berkeley.edu/~kubitron/courses/cs194-24-S14/hand-outs/bonwick_slab.pdf",
    "The original slab paper. Short, and the reasoning about object "
    "construction cost is still relevant."),
   ("mimalloc technical report (free)",
    "https://www.microsoft.com/en-us/research/publication/mimalloc-free-list-sharding-in-action/",
    "A modern multithreaded allocator explained by its authors, including the "
    "remote-free problem."),
 ],
 "exercises": [
   "Implement a simple free-list allocator with first fit, best fit, and "
   "worst fit. Run a mixed workload through each and measure fragmentation "
   "and allocation time.",
   "Measure external fragmentation directly: allocate and free in a pattern "
   "designed to strand memory, then report total free bytes against the "
   "largest contiguous free block.",
   "Implement segregated free lists and compare allocation time against your "
   "first-fit implementation. Measure the internal fragmentation you traded "
   "for it.",
   "Implement an arena allocator. Replace <code>malloc</code> with it in a "
   "parser or a per-frame workload and measure the speedup.",
   "Implement a buddy allocator and verify that freeing merges blocks "
   "correctly. Confirm that finding a buddy is a single XOR.",
   "Measure the system allocator against jemalloc or mimalloc on a workload "
   "with eight threads allocating concurrently. Report the scaling of each.",
   "Write a program that allocates a 1 GB block, frees it, and checks whether "
   "resident memory returns to the OS. Repeat with a million small "
   "allocations and explain the difference.",
 ],
 "selfcheck": [
   "Why can a C allocator not move allocations, and what does that make "
   "impossible?",
   "Distinguish internal from external fragmentation, including which is "
   "predictable.",
   "Why is allocation an online problem, and what follows about choosing an "
   "allocator?",
   "Explain why best fit is usually worse than first fit.",
   "How do segregated free lists achieve O(1) allocation, and what do they "
   "trade for it?",
   "What is arena allocation, when does it apply, and why does it also "
   "simplify code?",
   "Why do modern allocators maintain per-thread caches, and what "
   "complication does that introduce?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Virtual Memory and Paging Policy",
 "subtitle": "The kernel side of the mechanism CSCE 614 described.",
 "question": "What does the kernel do when a page is not there?",
 "outcomes": [
     "Implement demand paging via the page fault handler.",
     "Implement copy-on-write and lazy allocation.",
     "Compare page replacement policies against the optimal.",
     "Explain thrashing and the working set model.",
     "Explain mmap and the unification of files and memory.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The page fault handler",
   "blurb": "An exception that is usually not an error."},

  {"t": "table", "kicker": "Page faults", "title": "Most faults are routine",
   "header": ["Cause", "Kernel response", "Enables"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["Page never touched", "Allocate a zero page, map it", "Lazy allocation"],
     ["Write to a COW page", "Copy, remap writable", "Cheap fork (Module 02)"],
     ["Page swapped out", "Read from backing store", "Over-subscription"],
     ["File-backed, not resident", "Read the file block", "mmap"],
     ["<b>Genuinely invalid</b>", "SIGSEGV", "Catching bugs"],
   ],
   "note": "Only the last row is an error. The first four are the mechanism "
           "doing its job."},

  {"t": "code", "kicker": "Handler", "title": "The structure of a fault handler",
   "lang": "c", "code": """
void pagefault(uint64 va, int cause) {
    struct vma *v = find_vma(myproc(), va);

    if (!v)                         return kill("SIGSEGV");
    if (cause == WRITE && !(v->perm & W))
                                    return kill("SIGSEGV");

    if (cause == WRITE && is_cow(va)) {
        copy_page(va);              // Module 02: COW fork
    } else if (v->file) {
        read_page_from_file(v, va); // mmap
    } else if (swapped_out(va)) {
        read_page_from_swap(va);    // demand paging
    } else {
        map_zero_page(va);          // lazy allocation
    }
    // return -> the hardware RETRIES the faulting instruction
}
""",
   "caption": "The instruction is re-executed after the handler returns. The "
              "process never knows a fault occurred — which is what "
              "makes the illusion work.",
   "note": "The retry semantics are what make all of this transparent. Worth "
           "emphasising."},

  {"t": "section", "label": "Part 2", "title": "Replacement",
   "blurb": "Memory is full. Which page goes?"},

  {"t": "table", "kicker": "Policies", "title": "Replacement policies, against the optimum",
   "header": ["Policy", "Rule", "Assessment"],
   "widths": [2.6, 4.4, 5.1],
   "rows": [
     ["OPT", "Evict the page used furthest in the future", "<b>Optimal, unimplementable.</b> The yardstick"],
     ["FIFO", "Evict the oldest", "Simple; <b>Belady's anomaly</b>"],
     ["LRU", "Evict the least recently used", "Good; exact LRU is too expensive"],
     ["Clock", "Approximate LRU with a reference bit", "<b>What real kernels use</b>"],
     ["Random", "Evict anything", "Surprisingly not terrible"],
   ],
   "note": "OPT as a measuring stick rather than an algorithm is the right "
           "framing — same as SJF in Module 03."},

  {"t": "callout", "title": "Belady's anomaly", "kind": "Why FIFO is wrong",
   "body": ["Intuition says more memory cannot make things worse.",
            "For FIFO, it can. There exist reference strings where "
            "<b>increasing</b> the number of frames <b>increases</b> the "
            "number of faults.",
            "The reason: FIFO's eviction order has nothing to do with "
            "usefulness, so a larger cache can retain the wrong pages for "
            "longer.",
            "Policies with the <b>stack property</b> — LRU and OPT "
            "— cannot exhibit this: the set of pages held with n frames "
            "is always a subset of the set held with n+1. FIFO has no such "
            "guarantee."]},

  {"t": "code", "kicker": "Clock", "title": "Approximating LRU in hardware terms",
   "lang": "c", "code": """
// Exact LRU needs a timestamp update on EVERY access. Impossible.
// Hardware gives us one bit per page: the REFERENCE bit, set
// automatically on access.

int clock_evict(void) {
    for (;;) {
        if (!pages[hand].referenced)
            return hand;              // not used since last sweep: evict
        pages[hand].referenced = 0;   // give it a second chance
        hand = (hand + 1) % nframes;
    }
}

// A page gets evicted only if it survives a full sweep untouched.
// One bit, a circular scan, and behaviour close to LRU.
""",
   "caption": "The reference bit is set by hardware on every access and "
              "cleared by the kernel. That division of labour is what makes "
              "the approximation affordable.",
   "note": "Extending to a second bit (dirty) gives the classic four-class "
           "NRU, worth mentioning."},

  {"t": "section", "label": "Part 3", "title": "Thrashing",
   "blurb": "When the system spends all its time paging."},

  {"t": "callout", "title": "Thrashing is a cliff, not a slope",
   "kind": "The failure mode",
   "body": ["As load rises, throughput rises — until the combined "
            "working sets exceed physical memory.",
            "Then every process faults constantly, each fault evicts a page "
            "another process is about to need, and throughput "
            "<b>collapses</b>. The CPU is idle; the disk is saturated.",
            "The feedback is vicious: the scheduler sees idle CPU and admits "
            "<i>more</i> processes, which makes it worse.",
            "<b>Fix:</b> reduce the degree of multiprogramming. Swap entire "
            "processes out so the remainder fit. Modern systems use the OOM "
            "killer, which is blunter and more honest."]},

  {"t": "bullets", "kicker": "Working set", "title": "The model that explains it",
   "items": [
     "The <b>working set</b> W(t, τ) is the set of pages referenced in "
     "the last τ units of time.",
     "",
     "<b>Principle:</b> a process runs efficiently if its working set is "
     "resident, and thrashes if it is not.",
     "",
     "So: admit processes only while the sum of working sets fits in physical "
     "memory.",
     "",
     "This is the same locality argument as CSCE 614 Module 05 — the "
     "cache hierarchy at a different scale, with the same cliff.",
   ],
   "note": "Framing paging as 'caching at a coarser granularity' unifies it "
           "with 614 and makes the policies feel familiar."},

  {"t": "section", "label": "Part 4", "title": "mmap",
   "blurb": "Files and memory are the same thing."},

  {"t": "bullets", "kicker": "mmap", "title": "What mapping a file buys",
   "items": [
     "Map a file into the address space; access it with ordinary loads and "
     "stores.",
     "",
     "<b>No read() calls, no copy</b> into a user buffer — the page "
     "cache <i>is</i> your memory.",
     "",
     "Pages load on demand, through the fault handler.",
     "",
     "<b>Shared mappings</b> let processes communicate through memory, backed "
     "by a file.",
     "",
     "And: this is how executables are loaded. Your program's code is an mmap "
     "of the binary.",
   ],
   "footnote": "The page cache serving both read() and mmap is why the two "
               "are coherent."},

  {"t": "table", "kicker": "Trade", "title": "mmap against read/write",
   "header": ["mmap", "read/write"],
   "widths": [6.0, 6.1],
   "rows": [
     ["No copy; the page cache is your memory", "A copy into your buffer"],
     ["Random access is natural", "Sequential access is natural"],
     ["Page faults are invisible but real", "Costs are explicit"],
     ["<b>I/O errors arrive as SIGBUS</b>", "Errors are a return value"],
     ["Address space limits apply", "No such limit"],
   ],
   "note": "The SIGBUS point is the practical gotcha: you cannot handle a "
           "read error from a mapped file conventionally."},

  {"t": "callout", "title": "Where CSCE 614 and this course meet",
   "kind": "Connection",
   "body": ["CSCE 614 Module 07 described the <b>hardware</b>: page tables, "
            "the TLB, translation, huge pages.",
            "This module is the <b>software</b> on the other side of the "
            "fault: what the kernel does when the hardware cannot complete "
            "a translation.",
            "Together they are one mechanism. The hardware detects and "
            "reports; the kernel decides and repairs; the hardware retries.",
            "Every feature in this module — lazy allocation, COW, "
            "demand paging, mmap — is the same page fault handled "
            "differently, which is an unusually economical piece of design."]},
 ],
 "takeaways": [
   "Most page faults are not errors. Lazy allocation, COW, demand paging, and "
   "mmap are all the fault handler doing its job.",
   "The faulting instruction is retried after the handler returns, which is "
   "what makes all of it invisible to the process.",
   "OPT is the yardstick, not an algorithm — the same role SJF plays in "
   "scheduling.",
   "FIFO suffers Belady's anomaly: more frames can mean more faults. LRU and "
   "OPT cannot, because they have the stack property.",
   "Clock approximates LRU with one hardware-set reference bit and a circular "
   "scan. That is what real kernels use.",
   "Thrashing is a cliff with vicious feedback: idle CPU tempts the scheduler "
   "to admit more work, making it worse.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The page fault handler"),
  ("p", "CSCE 614 Module 07 covered the hardware: page tables, the TLB, and "
        "address translation. This module covers what happens when "
        "translation <i>fails</i> — and that turns out to be the "
        "mechanism behind most of modern virtual memory."),
  ("table", ["Fault cause", "Kernel response", "Feature it implements"],
   [["Address is valid but no page has ever been allocated.",
     "Allocate a zeroed physical page and map it.",
     "<b>Lazy allocation.</b> <code>malloc</code> and <code>sbrk</code> "
     "return instantly; physical memory is committed only on first touch."],
    ["Write to a page marked read-only and flagged copy-on-write.",
     "Allocate a new page, copy the contents, map it writable, decrement the "
     "old page's reference count.",
     "<b>Copy-on-write fork</b> (Module 02)."],
    ["Page is valid but has been evicted to backing store.",
     "Find a free frame (evicting if necessary), read the page in, update the "
     "table.", "<b>Demand paging</b> and memory over-subscription."],
    ["Page belongs to a mapped file and is not resident.",
     "Read the corresponding file block into a frame and map it.",
     "<b>mmap</b>, and executable loading."],
    ["Address is genuinely not mapped, or permissions forbid the access.",
     "Deliver SIGSEGV.", "Catching program bugs."]],
   [0.28, 0.33, 0.39]),
  ("code", """void pagefault(uint64 va, int cause) {
    struct vma *v = find_vma(myproc(), va);
    if (!v)                                    return kill(SIGSEGV);
    if (cause == WRITE && !(v->perm & PERM_W)) return kill(SIGSEGV);

    if (cause == WRITE && is_cow(va))   copy_page(va);
    else if (v->file)                   read_page_from_file(v, va);
    else if (swapped_out(va))           read_page_from_swap(va);
    else                                map_zero_page(va);

    // On return, the hardware RE-EXECUTES the faulting instruction.
}"""),
  ("callout", "Retry is what makes it transparent",
   ["When the handler returns, the hardware restarts the instruction that "
    "faulted. This time the translation succeeds and the instruction "
    "completes normally.",
    "The process has no way to observe that anything happened — no "
    "signal, no return code, no change in its registers. The only evidence is "
    "that the instruction took longer.",
    "That is why the kernel can implement lazy allocation, copy-on-write, "
    "paging, and file mapping without any cooperation from the program, and "
    "it is an unusually economical piece of design: one hardware mechanism, "
    "five quite different features."]),

  ("h1", "2 &nbsp; Page replacement"),
  ("p", "Physical memory fills. To bring a page in, one must go out. Which?"),
  ("table", ["Policy", "Rule", "Assessment"],
   [["<b>OPT</b>", "Evict the page whose next use is furthest in the future.",
     "<b>Provably optimal and unimplementable</b> — it requires the "
     "future. Its role is as a yardstick: simulate it offline from a trace "
     "and measure how close your real policy comes. Exactly the role SJF "
     "plays in Module 03."],
    ["<b>FIFO</b>", "Evict the page that has been resident longest.",
     "Trivial to implement and genuinely bad: residence time has no "
     "relationship to future usefulness. Suffers Belady's anomaly."],
    ["<b>LRU</b>", "Evict the least recently used page.",
     "An excellent predictor, because of locality. <b>Exact</b> LRU requires "
     "updating a timestamp or list position on <i>every</i> memory access, "
     "which is far too expensive."],
    ["<b>Clock</b>", "Approximate LRU using a hardware reference bit and a "
     "circular scan.",
     "<b>What real kernels use.</b> Nearly LRU quality at nearly no cost."],
    ["<b>Random</b>", "Evict a page at random.",
     "Noticeably worse than LRU and noticeably better than one expects. Its "
     "merit is that it has no pathological cases."]],
   [0.12, 0.33, 0.55]),
  ("callout", "Belady's anomaly",
   ["It seems self-evident that giving a system more memory cannot increase "
    "its fault count. For FIFO, that is false: reference strings exist where "
    "increasing the number of frames <i>increases</i> the number of faults.",
    "The cause is that FIFO's eviction order is unrelated to usefulness, so a "
    "larger pool can hold the wrong pages for longer.",
    "Policies with the <b>stack property</b> cannot do this: the set of pages "
    "resident with n frames is always a subset of the set resident with n+1 "
    "frames, so more memory can only help. LRU and OPT have this property; "
    "FIFO does not.",
    "Beyond being a curiosity, it is a useful reminder that plausible "
    "monotonicity assumptions need proof."]),
  ("h2", "2.1 &nbsp; Clock"),
  ("code", """int clock_evict(void) {
    for (;;) {
        if (!frames[hand].referenced)
            return hand;                  // untouched since last sweep
        frames[hand].referenced = 0;      // second chance
        hand = (hand + 1) % nframes;
    }
}"""),
  ("p", "The hardware sets a <b>reference bit</b> in the page table entry "
        "whenever a page is accessed — one bit, set automatically, at no "
        "software cost. The kernel clears it. A page is evicted only if the "
        "clock hand reaches it and finds the bit still clear, meaning it has "
        "not been touched in a full sweep."),
  ("p", "The division of labour is the point: the hardware does the "
        "per-access work (setting one bit), and the kernel does the "
        "occasional work (sweeping). Adding a second bit — the dirty bit "
        "— gives the four-class refinement that prefers evicting clean "
        "pages, since those need no write-back."),

  ("break",),
  ("h1", "3 &nbsp; Thrashing and the working set"),
  ("callout", "Thrashing is a cliff with positive feedback",
   ["As more processes are admitted, throughput rises — until the sum of "
    "their active working sets exceeds physical memory.",
    "At that point each process faults almost immediately after being "
    "scheduled, and each fault evicts a page that some other process is about "
    "to need. Throughput does not degrade gracefully; it <b>collapses</b>. "
    "The CPU sits idle while the disk saturates.",
    "The feedback makes it worse: a scheduler observing idle CPU concludes "
    "the system is underloaded and admits more processes, deepening the "
    "problem.",
    "The classical fix is to reduce the degree of multiprogramming — "
    "swap whole processes out so that the remainder's working sets fit. "
    "Modern systems largely rely on the OOM killer instead, which is blunter "
    "and arguably more honest: if the workload does not fit, something has to "
    "go."]),
  ("eq", "W(t, &tau;) = { pages referenced in the interval (t &minus; &tau;, t] }"),
  ("p", "Denning's <b>working set</b> model formalises this. A process "
        "executes efficiently when its working set is resident and thrashes "
        "when it is not, so the admission rule is to keep the sum of resident "
        "working sets below physical memory."),
  ("p", "This is the locality argument of CSCE 614 Module 05 at a coarser "
        "granularity. Paging is caching, with main memory as the cache and "
        "the disk as the backing store, and the same concepts transfer: "
        "working set, capacity miss, replacement policy, and a sharp cliff "
        "when the working set exceeds capacity. Only the numbers change "
        "— a cache miss costs 250 cycles, a page fault costs a hundred "
        "thousand."),

  ("h1", "4 &nbsp; mmap"),
  ("p", "<code>mmap</code> maps a file into a process's address space. The "
        "file is then accessed with ordinary loads and stores, with pages "
        "brought in on demand by the fault handler."),
  ("table", ["<code>mmap</code>", "<code>read</code>/<code>write</code>"],
   [["No copy: the page cache pages <i>are</i> your memory.",
     "Data is copied from the page cache into your buffer."],
    ["Random access is natural — just index.",
     "Natural for sequential streaming; random access needs "
     "<code>lseek</code>."],
    ["Costs are invisible: a page fault looks like an ordinary memory access "
     "that happened to take a millisecond.",
     "Costs are explicit and easy to reason about."],
    ["<b>An I/O error arrives as SIGBUS</b>, not as a return value — "
     "awkward to handle.", "Errors are return values you can check."],
    ["Limited by address space and by the cost of setting up mappings.",
     "No such limit."],
    ["Shared mappings give processes shared memory backed by a file.",
     "Sharing requires explicit IPC."]],
   [0.5, 0.5]),
  ("p", "Two things worth knowing. First, the <b>page cache serves both</b> "
        "<code>read()</code> and <code>mmap</code>, which is why the two "
        "views of a file are coherent — a write through one is visible "
        "through the other. Second, <b>this is how executables are "
        "loaded</b>: the kernel maps the binary's text and data segments and "
        "lets demand paging bring in code as it is first executed, which is "
        "why starting a large program does not read the whole file."),
  ("callout", "Where CSCE 614 and this course join",
   ["CSCE 614 Module 07 described the hardware: multi-level page tables, the "
    "TLB, translation cost, huge pages, TLB reach.",
    "This module describes the software on the other side of the fault: what "
    "the kernel does when the hardware cannot complete a translation, and "
    "what it chooses to evict when memory runs out.",
    "Together they form one mechanism. <b>Hardware detects and reports; the "
    "kernel decides and repairs; hardware retries.</b> Lazy allocation, "
    "copy-on-write, demand paging, memory-mapped files, and executable "
    "loading are all the same fault, handled five different ways."]),
 ],
 "resources": [
   ("OSTEP — Chapters 21&ndash;24 (Beyond Physical Memory, Swapping, "
    "Policies)",
    "https://pages.cs.wisc.edu/~remzi/OSTEP/",
    "Replacement policies with simulations, Belady's anomaly, and the working "
    "set model."),
   ("MIT 6.1810 — page tables lecture and the COW and lazy allocation "
    "labs",
    "https://pdos.csail.mit.edu/6.1810/",
    "The labs are precisely Project 2's requirements."),
   ("xv6 book — Chapter 3 (Page tables)",
    "https://pdos.csail.mit.edu/6.1810/2023/xv6/book-riscv-rev3.pdf",
    "The implementation, with the fault path through real code."),
   ("Denning — The Working Set Model for Program Behavior (free)",
    "https://dl.acm.org/doi/10.1145/363095.363141",
    "The original working set paper. Still the clearest statement of why "
    "locality makes paging work at all."),
 ],
 "exercises": [
   "Implement lazy allocation in xv6: make <code>sbrk</code> only adjust the "
   "size, and allocate pages in the fault handler. Verify that allocating 1 "
   "GB and touching one page uses one page of physical memory.",
   "Implement copy-on-write <code>fork</code> with page reference counting. "
   "Fork a process with a large heap and show that physical memory does not "
   "double until writes occur.",
   "Implement <code>mmap</code> and <code>munmap</code> for file-backed "
   "mappings in xv6.",
   "Simulate FIFO, LRU, Clock, Random, and OPT against the same reference "
   "string. Plot fault count against frame count for each.",
   "Construct a reference string exhibiting Belady's anomaly for FIFO. Verify "
   "that LRU does not show it on the same string.",
   "Implement demand paging with a backing store and a replacement policy of "
   "your choice. Plot fault count against working-set size and identify the "
   "cliff.",
   "Induce thrashing deliberately: run several processes whose combined "
   "working sets exceed physical memory. Measure CPU utilisation and disk "
   "activity as it collapses.",
   "Compare <code>mmap</code> against <code>read</code> for sequential and "
   "random access to a large file. Explain both results.",
 ],
 "selfcheck": [
   "Name four page faults that are not errors and say what feature each "
   "implements.",
   "Why is the faulting instruction retried, and what does that make "
   "possible?",
   "What role does OPT play, given that it cannot be implemented?",
   "Explain Belady's anomaly and say why LRU is immune to it.",
   "How does Clock approximate LRU, and what is the division of labour "
   "between hardware and kernel?",
   "Why does thrashing collapse rather than degrade, and what makes the "
   "feedback vicious?",
   "Give two advantages and two disadvantages of <code>mmap</code> over "
   "<code>read</code>.",
 ],
},

]
