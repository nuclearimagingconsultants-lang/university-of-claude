# -*- coding: utf-8 -*-
"""CSCE 625 Artificial Intelligence — original course content."""

COURSE = {
    "code": "CSCE 625",
    "title": "Artificial Intelligence",
    "tagline": "Search, logic, and decision-making — the AI that "
               "ships in game engines and runs without a GPU",
    "term": "Semester 7 (with CSCE 753 and CSCE 642)",
    "prereqs": "CSCE 629 Analysis of Algorithms; CSCE 669 "
               "Computational Optimization is helpful for Modules 06 "
               "and 10; probability",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "An agent that solves a real problem, with the "
                   "approach justified against the alternatives, the "
                   "search or inference instrumented, and an honest "
                   "account of what it cannot do",
    "description": [
        "<b>This is the AI that is not a neural network</b>, and the "
        "ordering of this semester is deliberate: CSCE 753 and "
        "CSCE 642 cover the learned approaches, and <b>this course "
        "covers the enormous amount of working AI that predates them and "
        "has not been displaced.</b>",
        "<b>Every game that ships contains the contents of this "
        "course.</b> Pathfinding is Module 04. Enemy behaviour is "
        "Module 11. Procedural generation is Module 06. Tactical "
        "decision-making is Module 07 or Module 10. <b>None of it is "
        "learned, all of it is debuggable, and it runs in a millisecond "
        "on a CPU core</b> — which are the three properties a game "
        "engine actually requires.",
        "<b>The organising idea is that intelligence can be search.</b> "
        "<b>Modules 02 through 07 are all the same algorithm wearing "
        "different clothes</b> — a frontier, a successor function, "
        "and a way of deciding what to expand next — and the "
        "differences between pathfinding, game-tree search, constraint "
        "solving, and planning are differences in the state space and the "
        "heuristic, not in the method.",
        "<b>The second idea is that a good heuristic is worth more than "
        "a faster computer.</b> Module 03 makes this precise: an "
        "admissible heuristic that is twice as informative cuts the "
        "search exponentially, and <b>deriving heuristics automatically "
        "from relaxed problems</b> (Module 07) <b>is one of the field's "
        "genuinely beautiful results.</b>",
        "<b>The third is that an agent must act under "
        "uncertainty</b>, which Modules 09 and 10 treat properly — "
        "and which connects directly to CSCE 642, where the same "
        "Markov decision process is solved by learning instead of by "
        "computation.",
    ],
    "outcomes": [
        "Formulate a problem as a state space and choose a search "
        "strategy.",
        "State and verify admissibility and consistency, and design "
        "heuristics.",
        "Implement production-quality pathfinding, including on "
        "navigation meshes.",
        "Implement adversarial search with alpha-beta and Monte Carlo "
        "tree search.",
        "Model and solve a constraint satisfaction problem, including "
        "for content generation.",
        "Explain classical planning and derive heuristics from "
        "relaxations.",
        "Use a SAT solver and explain what it is doing.",
        "Build and query a Bayesian network, and explain conditional "
        "independence.",
        "Solve a Markov decision process by value and policy "
        "iteration.",
        "Choose and implement a game AI architecture and justify the "
        "choice.",
        "State what an AI system can be trusted to do, and why.",
    ],
    "materials": [
        ("Russell & Norvig — Artificial Intelligence: A Modern "
         "Approach, 4th edition",
         "https://aima.cs.berkeley.edu/",
         "<b>The primary source for this course.</b> The site hosts free "
         "pseudocode for every algorithm, free Python implementations, "
         "and the figures. Library copy for the text; everything "
         "algorithmic is free."),
        ("Berkeley CS188 — Introduction to Artificial Intelligence "
         "(free lectures, notes, and the Pacman projects)",
         "https://inst.eecs.berkeley.edu/~cs188/",
         "<b>The best free AI course available, and the Pacman "
         "assignments are outstanding.</b> Modules 02–05 and 10 "
         "follow it closely."),
        ("Millington — AI for Games, 3rd edition",
         "https://www.gameaipro.com/",
         "<b>The reference for Modules 04 and 11</b> — the "
         "engineering detail that academic treatments omit. The free "
         "<i>Game AI Pro</i> volumes at this link are chapters by "
         "shipping practitioners and are excellent."),
        ("Ghallab, Nau & Traverso — Automated Planning and Acting "
         "(free draft)",
         "http://projects.laas.fr/planning/",
         "<b>Module 07's reference</b>, with the relaxation-based "
         "heuristics developed properly."),
        ("Biere, Heule, van Maaren & Walsh — Handbook of "
         "Satisfiability (chapters free)",
         "https://satassociation.org/",
         "<b>Module 08's CDCL material</b>, and the competition results "
         "that show how far solvers have come."),
        ("Sutton & Barto — Reinforcement Learning, 2nd edition "
         "(free PDF)",
         "http://incompleteideas.net/book/the-book.html",
         "<b>Chapters 3 and 4 are Module 10</b>, and the rest is "
         "CSCE 642 — so the two courses share one free book, which "
         "makes the connection easy to follow."),
    ],
    "tooling": [
        "<b>Python for the algorithms, and a profiler.</b> <b>Search "
        "performance is dominated by the successor function and the "
        "frontier data structure</b>, and both are easy to get wrong in "
        "ways only a profiler reveals.",
        "<b>A visualiser you write yourself.</b> <b>Watching a search "
        "expand is worth more than any amount of reading</b>, and a "
        "hundred-line grid renderer will serve the whole course.",
        "<b>A SAT solver:</b> MiniSat, CaDiCaL, or PySAT. <b>Module 08 "
        "is much more convincing when you watch a solver dispatch a "
        "problem you could not.</b>",
        "<b>A game engine or a simple simulation loop</b> for "
        "Modules 04 and 11. <b>Godot is free and adequate</b>; so is "
        "a Pygame loop, and the point is the agent rather than the "
        "renderer.",
        "<b>pgmpy or similar for Module 09</b>, after implementing "
        "variable elimination yourself once.",
        "<b>Node counts instrumented everywhere.</b> <b>This course's "
        "measurements are nodes expanded and time per decision</b>, and "
        "neither is visible unless you count it.",
    ],
    "projects": [
        {"title": "A searching agent, instrumented", "after": 7,
         "brief": "Build an agent that solves a non-trivial problem by "
                  "search or planning, and measure what the search "
                  "actually does.",
         "reqs": [
             "<b>A state space formulation</b> written out: states, "
             "actions, successor function, goal test, costs.",
             "<b>At least three search strategies compared</b> on the "
             "same problem, with nodes expanded reported for each.",
             "<b>At least two heuristics</b>, with admissibility argued "
             "or disproved for each.",
             "<b>A plot of nodes expanded against problem size</b> for "
             "each configuration.",
             "<b>A visualisation of the search</b> — what was "
             "expanded, in what order.",
             "<b>One problem instance your agent cannot solve</b>, with "
             "the reason identified as branching factor, depth, or "
             "heuristic weakness.",
         ],
         "done": [
             "<b>Nodes expanded reported, not just wall-clock time</b> "
             "— time confounds the algorithm with the "
             "implementation.",
             "<b>The admissibility arguments correct</b>, including the "
             "one you disprove.",
             "<b>The better heuristic demonstrably dominating</b>, with "
             "the node-count ratio stated.",
             "<b>The failure case explained in terms of the state "
             "space</b>, not described as slowness.",
         ]},
        {"title": "An agent that decides", "after": 12,
         "brief": "Build an agent that acts under uncertainty or against "
                  "an opponent, in a real-time loop, and justify the "
                  "architecture.",
         "reqs": [
             "<b>A real-time loop with a per-decision time budget</b> "
             "stated and measured.",
             "<b>An architecture chosen from Module 11's options</b>, "
             "with the alternatives considered and rejected in "
             "writing.",
             "<b>Either adversarial search</b> (Module 05) <b>or an MDP "
             "solved</b> (Module 10), <b>with the state space "
             "size reported.</b>",
             "<b>Behaviour that is debuggable</b> — a way to ask "
             "the agent why it did what it did.",
             "<b>A comparison against a trivial baseline</b> policy. "
             "<b>CSCE 633's discipline, unchanged.</b>",
             "<b>Latency at the 99th percentile</b>, not the mean.",
         ],
         "done": [
             "<b>The time budget met at p99</b>, with the measurement "
             "shown.",
             "<b>The architecture choice justified against at least two "
             "alternatives</b>, in terms of this problem.",
             "<b>The agent beats the trivial baseline</b>, measurably, or "
             "you explain why it does not.",
             "<b>A written account of what the agent cannot do</b> and "
             "what would be needed — which is the graded part.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Agents and Rationality",
 "subtitle": "What the subject is actually about.",
 "question": "What makes a program an agent, and what makes an agent "
             "good?",
 "outcomes": [
     "Define an agent in terms of percepts and actions.",
     "State what rationality means and what it does not.",
     "Classify environments and explain what each property costs.",
     "Explain the AI effect and why the field's definition keeps "
     "moving.",
     "Place the rest of the course against that classification.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Agents",
   "blurb": "Percepts in, actions out, and a performance measure."},

  {"t": "callout", "title": "An agent is a function from percept histories to actions",
   "kind": "The definition, and why it is useful",
   "body": ["<b>Percepts in, actions out.</b> That is the whole "
            "interface, and everything in this course is an "
            "implementation of that function.",
            "<b>The agent is rational if it acts to maximise its "
            "expected performance measure</b>, given what it knows "
            "— which makes 'good behaviour' a measurable property "
            "rather than a judgement.",
            "<b>Note what rationality is not.</b> It is not omniscience "
            "(you act on percepts, not on truth), not perfection (the "
            "outcome may be bad), and not introspection.",
            "<b>And the performance measure is chosen by you</b>, which "
            "is where the real difficulty sits — <b>a vacuum agent "
            "rewarded for dirt collected will dump dirt and re-collect "
            "it</b>, and that is a correct solution to the problem you "
            "specified."]},

  {"t": "table", "kicker": "Architectures", "title": "Four agent designs, by what they keep",
   "header": ["Design", "What it uses", "Example"],
   "widths": [2.7, 4.3, 5.1],
   "rows": [
     ["<b>Reflex</b>", "<b>The current percept only</b>", "<b>Steering away from a wall; a thermostat</b>"],
     ["<b>Model-based</b>", "<b>Percepts plus internal state</b>", "<b>An enemy that remembers where you went</b>"],
     ["<b>Goal-based</b>", "<b>State plus a goal; searches for a plan</b>", "<b>Pathfinding, planning (M04, M07)</b>"],
     ["<b>Utility-based</b>", "<b>State plus a utility over outcomes</b>", "<b>Choosing between imperfect options (M10, M11)</b>"],
   ],
   "footnote": "<b>Each row costs more and does more.</b> <b>The "
               "engineering question is always the cheapest design that "
               "produces the required behaviour</b>, and reflex agents "
               "are underrated.",
   "note": "Framing it as a cost ladder is more useful than presenting "
           "four equal options."},

  {"t": "section", "label": "Part 2", "title": "Environments",
   "blurb": "The properties that decide which methods are available."},

  {"t": "table", "kicker": "Properties", "title": "What each environment property costs you",
   "header": ["Property", "If it fails", "Consequence"],
   "widths": [2.8, 4.2, 5.1],
   "rows": [
     ["<b>Fully observable</b>", "<b>Partially observable</b>", "<b>You need belief states — a POMDP (M10)</b>"],
     ["<b>Deterministic</b>", "<b>Stochastic</b>", "<b>Plans become policies; search becomes an MDP</b>"],
     ["<b>Static</b>", "<b>Dynamic</b>", "<b>Deliberation has a deadline (M04 replanning)</b>"],
     ["<b>Discrete</b>", "Continuous", "<b>Discretise, or use a continuous method</b>"],
     ["<b>Single agent</b>", "<b>Multi-agent</b>", "<b>Adversarial search, or game theory (M05, M12)</b>"],
     ["<b>Known rules</b>", "Unknown rules", "<b>You must learn them — CSCE 642</b>"],
   ],
   "footnote": "<b>Classify your environment first.</b> <b>Each 'no' in "
               "the second column removes a family of methods</b>, and "
               "that single table determines most of the design.",
   "note": "This table is the most practically useful thing in the "
           "module."},

  {"t": "callout", "title": "Most real problems are the hard case, and the fix is to lie carefully",
   "kind": "The practical response",
   "body": ["<b>A real game world is partially observable, stochastic, "
            "dynamic, continuous, and multi-agent</b> — which is the "
            "worst column of every row.",
            "<b>So the standard move is to approximate it into a "
            "tractable one:</b> discretise space into a navigation mesh, "
            "treat the world as static for 100 ms, assume full "
            "observability within a radius.",
            "<b>Each approximation is a deliberate, documented lie</b>, "
            "and <b>knowing which lie you told is how you predict the "
            "failure</b> — an agent that assumes a static world will "
            "walk into a closing door.",
            "<b>That is CSCE 669 Module 12's modelling discipline, "
            "arriving in a different subject</b> — and it is the "
            "single most transferable habit in this course."]},

  {"t": "section", "label": "Part 3", "title": "The moving definition",
   "blurb": "Why nobody can say what AI is."},

  {"t": "callout", "title": "The AI effect: solved problems stop counting",
   "kind": "A real phenomenon with real consequences",
   "body": ["<b>Chess was the archetype of intelligence until a program "
            "won, at which point it became 'just search'.</b> The same "
            "happened to character recognition, speech, and "
            "translation.",
            "<b>So AI is partly defined as the set of problems not yet "
            "solved</b>, which means the field appears to make no "
            "progress by construction.",
            "<b>The consequence for you is practical:</b> <b>a great "
            "deal of extremely useful AI is no longer called AI</b> and "
            "is therefore under-taught — route planning, scheduling, "
            "constraint solving, SAT.",
            "<b>And it is why this course matters for the track.</b> "
            "<b>The AI in a shipped game is almost entirely the "
            "'solved' kind</b>, because solved means reliable, fast, and "
            "debuggable."]},

  {"t": "bullets", "kicker": "Scope", "title": "Where this course goes",
   "items": [
     "<b>Modules 02–05: search.</b> <b>Intelligence as "
     "systematic exploration of possibilities</b> — the unifying "
     "idea, and Module 04 is the track's payoff.",
     "",
     "<b>Modules 06–08: structure.</b> Constraints, planning, "
     "logic. <b>Search with the problem's structure exploited</b>, "
     "including SAT, which is the most under-appreciated tool here.",
     "",
     "<b>Modules 09–10: uncertainty.</b> Probabilistic "
     "reasoning and sequential decisions. <b>The direct bridge to "
     "CSCE 642.</b>",
     "",
     "<b>Modules 11–12: agents in practice.</b> Game AI "
     "architectures, crowds, and multi-agent behaviour.",
     "",
     "<b>Module 13: choosing, and claiming honestly.</b>",
   ],
   "footnote": "<b>No neural networks appear until Module 13</b>, and "
               "that is deliberate — the other two courses this "
               "semester cover them."},

  {"t": "section", "label": "Part 4", "title": "Why this is still the "
   "right place to start",
   "blurb": "The case for the unlearned methods."},

  {"t": "callout", "title": "Four properties learned systems do not have",
   "kind": "Why this material has not been displaced",
   "body": ["<b>Guarantees.</b> A* returns the optimal path, provably "
            "(Module 03). A learned policy returns something.",
            "<b>Debuggability.</b> <b>You can ask a search why it chose "
            "a path and get an answer in terms of costs</b>; asking a "
            "network produces a saliency map and a shrug.",
            "<b>No training data and no training.</b> Change the level "
            "layout and the pathfinder works; change it and the learned "
            "policy must be retrained.",
            "<b>And cost.</b> <b>A* on a navigation mesh costs "
            "microseconds on one CPU core</b> and a game has sixteen "
            "milliseconds for everything. <b>That constraint alone "
            "explains most of game AI.</b>"]},
 ],
 "takeaways": [
   "An agent is a function from percept histories to actions, and "
   "rationality is maximising an expected performance measure that you "
   "chose.",
   "The four agent designs form a cost ladder, and the engineering "
   "question is the cheapest one that produces the required behaviour.",
   "Six environment properties determine which methods are available, and "
   "each failure removes a family of techniques.",
   "Real problems are the hard case, so the standard move is to "
   "approximate into a tractable one — and knowing which "
   "approximation you made is how you predict the failure.",
   "The AI effect means solved problems stop being called AI, which leaves "
   "a great deal of useful, reliable technique under-taught.",
   "Unlearned methods have guarantees, debuggability, no training "
   "requirement, and microsecond cost — which is why game engines use "
   "them.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Agents"),
  ("callout", "An agent is a function from percept histories to actions",
   ["<b>Percepts in, actions out.</b> That is the entire interface, and "
    "<b>everything in this course is an implementation of that "
    "function</b> — a search, a rule set, a policy table, a decision "
    "tree over the world state. Holding the interface fixed makes the "
    "methods comparable.",
    "<b>The agent is <i>rational</i> if it acts so as to maximise its "
    "expected performance measure, given the percepts it has "
    "received</b> — which converts 'good behaviour' from a judgement "
    "into a measurable property, and is the reason the definition is "
    "worth stating formally.",
    "<b>Note carefully what rationality is not.</b> It is not "
    "omniscience: the agent acts on percepts, not on the true world "
    "state. It is not perfection: a rational action can have a bad "
    "outcome, and that does not make it irrational. And it is not "
    "introspection: nothing requires the agent to know why it acted.",
    "<b>And the performance measure is chosen by you</b>, which is where "
    "the real difficulty sits. <b>A vacuum-cleaner agent rewarded for "
    "dirt collected will dump dirt on the floor and collect it again</b>, "
    "and <b>that is a correct solution to the problem you specified</b>. "
    "<b>This is CSCE 633 Module 01 &sect;3's point about loss "
    "functions and CSCE 642's reward-specification problem, arriving "
    "before either</b> — the objective is the hard part, and it is "
    "hard in exactly the same way whether the agent searches or learns."]),
  ("table", ["Design", "What it uses", "Example"],
   [["<b>Reflex agent</b>",
     "<b>The current percept only, through a set of condition-action "
     "rules.</b>",
     "<b>Steering away from a wall; a thermostat; a flocking boid</b> "
     "(Module 11 &sect;4). <b>Underrated</b> — a great deal of "
     "convincing behaviour needs nothing more."],
    ["<b>Model-based reflex agent</b>",
     "<b>Percepts plus internal state tracking what it cannot currently "
     "see.</b>",
     "<b>An enemy that remembers where it last saw you</b> and searches "
     "there — which is most of what makes game enemies feel "
     "intelligent."],
    ["<b>Goal-based agent</b>",
     "<b>State plus an explicit goal, and a search for a sequence of "
     "actions achieving it.</b>",
     "<b>Pathfinding (Module 04), classical planning "
     "(Module 07).</b>"],
    ["<b>Utility-based agent</b>",
     "<b>State plus a utility function over outcomes, so it can rank "
     "imperfect options and trade off competing goals.</b>",
     "<b>Choosing between several imperfect actions</b> "
     "(Modules 10 and 11) — necessary as soon as goals "
     "conflict or outcomes are uncertain."]],
   [0.21, 0.36, 0.43]),
  ("p", "<b>Each row costs more to build and run, and does more.</b> "
        "<b>The engineering question is always the cheapest design that "
        "produces the required behaviour</b> — and in game AI the "
        "answer is a reflex or model-based agent far more often than the "
        "literature's emphasis would suggest, because the requirement is "
        "<i>plausible</i> behaviour under a time budget rather than "
        "optimal behaviour."),

  ("h1", "2 &nbsp; Environments"),
  ("table", ["Property", "If it fails", "Consequence for your methods"],
   [["<b>Fully observable</b>", "<b>Partially observable.</b>",
     "<b>You must reason over belief states rather than states — a "
     "partially observable Markov decision process</b> (Module 10 "
     "&sect;4), which is enormously more expensive."],
    ["<b>Deterministic</b>", "<b>Stochastic.</b>",
     "<b>Plans become policies</b>: you cannot commit to a sequence, "
     "because you do not know where you will be. Search becomes a Markov "
     "decision process (Module 10)."],
    ["<b>Static</b>", "<b>Dynamic.</b>",
     "<b>Deliberation has a deadline, and the world changes while you "
     "think</b> — so you need anytime algorithms and replanning "
     "(Module 04 &sect;4)."],
    ["<b>Discrete</b>", "Continuous.",
     "<b>Discretise (a grid, a navigation mesh, a waypoint graph) or use "
     "a continuous method.</b> Discretisation is the usual answer and its "
     "resolution is a real design parameter."],
    ["<b>Single agent</b>", "<b>Multi-agent.</b>",
     "<b>Adversarial search if interests conflict</b> (Module 05), or "
     "game theory and coordination (Module 12)."],
    ["<b>Known rules</b>", "Unknown rules.",
     "<b>You must learn the dynamics — which is exactly "
     "CSCE 642's subject</b>, and the reason it is the third course "
     "this semester."]],
   [0.17, 0.21, 0.62]),
  ("callout", "Most real problems are the hard case, and the fix is to lie "
              "carefully",
   ["<b>A real game world is partially observable, stochastic, dynamic, "
    "continuous, and multi-agent</b> — the worst column of every row "
    "in the table, simultaneously.",
    "<b>So the standard move is to approximate it into something "
    "tractable:</b> discretise continuous space into a navigation mesh, "
    "treat the world as static for the next 100 milliseconds, assume full "
    "observability within a radius and nothing beyond it, treat other "
    "agents as part of the environment rather than as reasoners.",
    "<b>Each approximation is a deliberate lie</b>, and <b>knowing which "
    "lie you told is how you predict the failure</b> — an agent that "
    "assumes a static world will walk into a door that is closing, and an "
    "agent that treats others as environment will not anticipate being "
    "flanked. <b>Both failures are derivable in advance from the "
    "approximation list</b>, which is why writing the list down is worth "
    "the ten minutes.",
    "<b>That is CSCE 669 Module 12's modelling discipline arriving in "
    "a different subject</b>, and the same warning applies: <b>the agent "
    "will exploit your approximation</b>, because it is optimising against "
    "the model and not against the world. <b>It is the single most "
    "transferable habit in this course.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; The moving definition"),
  ("callout", "The AI effect: solved problems stop counting",
   ["<b>Chess was the archetype of machine intelligence until a program "
    "beat the world champion, at which point it was reclassified as 'just "
    "tree search'.</b> The same has happened to optical character "
    "recognition, speech recognition, machine translation, and route "
    "planning — each was AI until it worked.",
    "<b>So AI is partly defined as the set of problems not yet "
    "solved</b>, which means <b>the field appears to make no progress by "
    "construction</b>: every success is subtracted from the definition. "
    "This is worth knowing both as intellectual history and as "
    "inoculation against the surrounding discourse.",
    "<b>The consequence for you is practical.</b> <b>A great deal of "
    "extremely useful AI is no longer called AI and is therefore "
    "under-taught</b> — route planning, scheduling, constraint "
    "solving, satisfiability, and automated planning are all industrial "
    "technologies with decades of engineering behind them, and all of them "
    "are in this course.",
    "<b>And it is precisely why this course matters for this track.</b> "
    "<b>The AI in a shipped game is almost entirely the 'solved' "
    "kind</b>, because <b>solved means reliable, fast, and "
    "debuggable</b> — the three properties a production system "
    "requires and the three that &sect;4 argues learned systems lack."]),
  ("ul", ["<b>Modules 02 through 05 are search.</b> <b>Intelligence as "
          "systematic exploration of possibilities</b> — the "
          "unifying idea of the course, and <b>Module 04 is the track's "
          "immediate payoff</b>, since pathfinding is in every game "
          "engine.",
          "<b>Modules 06 through 08 are structure.</b> Constraint "
          "satisfaction, classical planning, and logic. <b>Search with "
          "the problem's structure exploited rather than ignored</b> "
          "— including satisfiability solvers, which are the most "
          "under-appreciated tool in the course.",
          "<b>Modules 09 and 10 are uncertainty.</b> Probabilistic "
          "reasoning and sequential decision-making. <b>The direct bridge "
          "to CSCE 642</b>, which solves Module 10's problem by "
          "learning rather than by computing.",
          "<b>Modules 11 and 12 are agents in practice.</b> Game AI "
          "architectures, steering, crowds, and multi-agent behaviour "
          "— the engineering that academic treatments omit.",
          "<b>Module 13 is choosing between all of it, and claiming "
          "honestly.</b> <b>No neural networks appear until then</b>, "
          "and that is deliberate: the other two courses this semester "
          "cover them, and the point of this one is everything else."]),

  ("h1", "4 &nbsp; Why this is still the right place to start"),
  ("callout", "Four properties learned systems do not have",
   ["<b>Guarantees.</b> <b>A* returns the optimal path, provably, given "
    "an admissible heuristic</b> (Module 03 &sect;2). A learned policy "
    "returns something, and the only way to know how good it is is to "
    "measure it on a distribution you hope matches deployment "
    "(CSCE 753 Module 12).",
    "<b>Debuggability.</b> <b>You can ask a search why it chose a path "
    "and get an answer in terms of path costs and heuristic values</b> "
    "— a complete, checkable explanation. <b>Asking a network "
    "produces a saliency map and a shrug</b> (CSCE 753 Module 08 "
    "&sect;4). <b>For a system a designer must tune, this difference "
    "dominates everything else.</b>",
    "<b>No training data and no training.</b> Change the level layout "
    "and the pathfinder works on the new layout immediately; change it "
    "and a learned policy must be retrained, which means the content "
    "pipeline and the AI are coupled. <b>Decoupling them is worth a "
    "great deal in practice.</b>",
    "<b>And cost.</b> <b>A* on a navigation mesh costs microseconds on a "
    "single CPU core</b>, and <b>a game at 60 frames per second has "
    "sixteen milliseconds for physics, rendering, audio, animation, and "
    "every agent's decision combined.</b> <b>That constraint alone "
    "explains most of the design of game AI</b> — not a preference "
    "for classical methods, but an arithmetic limit, and one that "
    "Module 11 &sect;1 returns to with numbers."]),
 ],
 "resources": [
   ("Russell & Norvig &mdash; AIMA, chapters 1–2 (pseudocode and "
    "code free)",
    "https://aima.cs.berkeley.edu/",
    "<b>The agent and environment definitions of &sect;1 and &sect;2</b>, "
    "in their standard form."),
   ("Berkeley CS188 &mdash; lecture 1 and the course overview (free)",
    "https://inst.eecs.berkeley.edu/~cs188/",
    "<b>The same material with better motivation</b>, and the Pacman "
    "project framework you will use from Module 02."),
   ("McCorduck &mdash; Machines Who Think",
    "https://www.pamelamccorduck.com/machines-who-think",
    "<b>The history behind &sect;3's AI effect</b>, written by someone "
    "who interviewed the people involved. Library copy."),
   ("Game AI Pro &mdash; the free volumes (free)",
    "https://www.gameaipro.com/",
    "<b>Chapters by shipping practitioners</b>, and the clearest evidence "
    "for &sect;4's argument about what production systems actually "
    "use."),
 ],
 "exercises": [
   "<b>Write the percept and action spaces</b> for three agents you can "
   "think of, including one from a game you have played.",
   "<b>Specify a performance measure for a vacuum agent</b>, then find "
   "the degenerate behaviour it rewards.",
   "<b>Fix the measure</b> and find the next degenerate behaviour.",
   "<b>Classify three environments</b> against &sect;2's six properties.",
   "<b>For a game you know, write down every approximation</b> its AI "
   "must be making.",
   "<b>Predict a failure from each approximation</b>, then look for it in "
   "the game.",
   "<b>Implement the four agent designs</b> for one simple environment "
   "and compare behaviour and code size.",
   "<b>Find the cheapest design that produces acceptable behaviour</b> "
   "and report which it was.",
   "<b>List five technologies that were once AI and are no longer "
   "called that.</b>",
   "<b>Time an A* query on a grid</b> and compare against a frame budget "
   "of 16 ms.",
 ],
 "selfcheck": [
   "Define an agent and define rationality.",
   "Name three things rationality is not.",
   "Why is the performance measure the hard part?",
   "Name the four agent designs and what each keeps.",
   "Name six environment properties and the consequence of each "
   "failing.",
   "What is the standard response to a hard environment, and what does "
   "it cost?",
   "What is the AI effect, and what is its practical consequence?",
   "Name four properties unlearned methods have that learned ones do "
   "not.",
 ],
},

]

for _b in ("c625_b2", "c625_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
