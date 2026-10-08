# -*- coding: utf-8 -*-
"""CSCE 625 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Search",
 "subtitle": "One algorithm, five strategies.",
 "question": "How do you systematically explore a space of "
             "possibilities?",
 "outcomes": [
     "Formulate a problem as a state space.",
     "State the one generic search algorithm and what varies in it.",
     "Compare the uninformed strategies on four criteria.",
     "Explain why graph search needs a closed set and tree search does "
     "not.",
     "Estimate whether a state space is searchable at all.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The formulation",
   "blurb": "Five components, and the choice of state is the "
            "consequential one."},

  {"t": "callout", "title": "A search problem is five things, and one of them is a design decision",
   "kind": "The formulation",
   "body": ["<b>An initial state; a set of actions available in each "
            "state; a transition function; a goal test; a cost per "
            "action.</b> That is all.",
            "<b>The choice of what counts as a state is the "
            "consequential decision</b>, and it is yours — exactly "
            "CSCE 669 Module 12's variable choice, in a different "
            "subject.",
            "<b>A grid cell, or a grid cell plus a facing direction, or "
            "plus an inventory?</b> Each gives a different state space "
            "size and a different set of solvable problems.",
            "<b>Too coarse and the solution is wrong</b> (a path that "
            "ignores which doors you have keys for); <b>too fine and the "
            "space is unsearchable.</b> <b>Get this right before writing "
            "any code.</b>"]},

  {"t": "code", "kicker": "The algorithm", "title": "All of search 1/2: the loop",
   "lang": "text", "code": """
  frontier = { start }
  explored = { }

  while frontier not empty:
      node = frontier.REMOVE()      # <-- the only difference
      if goal(node): return path(node)
      explored.add(node.state)
      for each successor s of node:
          if s.state not in explored and s not in frontier:
              frontier.add(s)
  return failure

  THE EXPLORED SET is what makes this GRAPH search. Without
  it you have TREE search, which revisits states and can
  loop forever in a cyclic space. With it, memory grows
  with the number of distinct states reached.
""",
   "caption": "<b>Writing this loop once and parameterising "
              "<code>REMOVE</code> is the right implementation</b> "
              "— it makes the comparisons of Part 2 a one-line "
              "change.",
   "note": "Implement it exactly once; everything else is a frontier."},

  {"t": "code", "kicker": "The algorithm", "title": "All of search 2/2: the taxonomy",
   "lang": "text", "code": """
  THE ONLY THING THAT VARIES BETWEEN ALGORITHMS IS WHICH
  NODE REMOVE() RETURNS:

      a queue      (FIFO)           -> breadth-first
      a stack      (LIFO)           -> depth-first
      a priority queue on g(n)      -> uniform cost
      a priority queue on h(n)      -> greedy best-first
      a priority queue on g(n)+h(n) -> A*            (M03)

  THAT IS THE WHOLE TAXONOMY. Every search algorithm in
  Modules 02 through 07 is that loop with a different
  frontier discipline and a different state space.
""",
   "caption": "<b>Five famous algorithms are five data "
              "structures</b> — which is worth knowing before "
              "memorising any of them separately.",
   "note": "Students who see the unification here stop memorising "
           "algorithms."},

  {"t": "section", "label": "Part 2", "title": "The strategies",
   "blurb": "Compared on completeness, optimality, time, and space."},

  {"t": "table", "kicker": "Comparison", "title": "The uninformed strategies",
   "header": ["Strategy", "Complete?", "Optimal?", "Space"],
   "widths": [2.8, 2.3, 2.6, 4.7],
   "rows": [
     ["<b>Breadth-first</b>", "<b>Yes</b>", "<b>If costs are equal</b>", "<b>O(b^d) — usually the binding constraint</b>"],
     ["<b>Depth-first</b>", "<b>No (infinite depth)</b>", "<b>No</b>", "<b>O(bm) — linear. Its only virtue</b>"],
     ["<b>Uniform cost</b>", "<b>Yes</b>", "<b>Yes</b>", "<b>O(b^(C*/ε)) — can exceed BFS</b>"],
     ["<b>Iterative deepening</b>", "<b>Yes</b>", "<b>If costs equal</b>", "<b>O(bd) — BFS guarantees at DFS memory</b>"],
     ["<b>Bidirectional</b>", "Yes", "If costs equal", "<b>O(b^(d/2)) — a square root</b>"],
   ],
   "footnote": "<b>Iterative deepening is the right default when there "
               "is no heuristic:</b> it repeats work and the repetition "
               "is a constant factor, because the last level dominates "
               "the node count.",
   "note": "The iterative-deepening result is counterintuitive and worth "
           "proving on the slide."},

  {"t": "callout", "title": "Memory, not time, is what stops a search",
   "kind": "The practical fact",
   "body": ["<b>Breadth-first search at branching factor 10 and depth "
            "12 stores on the order of 10¹² nodes.</b> At even 100 "
            "bytes a node that is 100 terabytes.",
            "<b>The time would be tolerable on a cluster; the memory is "
            "not available anywhere.</b> <b>So the frontier size is the "
            "binding constraint in practice</b>, and it is the first "
            "thing to estimate.",
            "<b>Which is why iterative deepening exists</b>, and why "
            "memory-bounded variants like IDA* and SMA* exist for the "
            "heuristic case (Module 03).",
            "<b>Estimate b and d before implementing anything.</b> "
            "<b>b^d tells you immediately whether the problem needs a "
            "heuristic, a reformulation, or an approximation</b> — "
            "and that estimate takes two minutes."]},

  {"t": "section", "label": "Part 3", "title": "Graph against tree",
   "blurb": "Why the explored set matters."},

  {"t": "bullets", "kicker": "Repeated states", "title": "What happens without an explored set",
   "items": [
     "<b>In a cyclic space, tree search can loop forever</b> "
     "— walking back and forth between two states.",
     "",
     "<b>In an acyclic space it still explodes:</b> a grid with 4 "
     "actions has exponentially many paths to each cell and tree search "
     "explores all of them.",
     "",
     "<b>So the explored set converts exponential to polynomial</b> in "
     "the number of states, which is frequently the difference between "
     "possible and not.",
     "",
     "<b>The cost is memory proportional to states reached</b>, which "
     "is why depth-first search's linear memory is lost.",
     "",
     "<b>And the state must be hashable and compared correctly</b> "
     "— <b>a subtle equality bug here produces a search that is "
     "merely slow, not broken, so nothing alerts you.</b>",
   ],
   "footnote": "<b>Instrument the duplicate-detection rate.</b> If "
               "almost nothing is a duplicate, your state "
               "representation is probably too fine (Part 1)."},

  {"t": "section", "label": "Part 4", "title": "Reformulation",
   "blurb": "When the space is too big, change the space."},

  {"t": "callout", "title": "Shrinking the state space beats speeding up the search",
   "kind": "Where the real gains are",
   "body": ["<b>Abstraction:</b> search over rooms rather than tiles, "
            "then refine within each room. <b>This is hierarchical "
            "pathfinding</b> (Module 04 §3) and it reduces d "
            "dramatically.",
            "<b>Symmetry elimination:</b> if two states are equivalent "
            "under a symmetry, search one. <b>CSCE 669 Module 09's "
            "symmetry breaking</b>, in a different subject.",
            "<b>Macro-actions:</b> collapse common action sequences "
            "into one, reducing depth at the cost of branching.",
            "<b>And a better state encoding:</b> dropping an irrelevant "
            "variable divides the space by its range. <b>Ask of every "
            "state component whether the solution depends on it.</b>"]},

  {"t": "callout", "title": "Where this goes next",
   "kind": "The rest of the search modules",
   "body": ["<b>Module 03 adds a heuristic</b>, which is the single "
            "largest available improvement — it changes the effective "
            "branching factor rather than the constant.",
            "<b>Module 04 applies it to the track's problem</b>, with "
            "the engineering that production pathfinding needs.",
            "<b>Module 05 searches against an opponent</b>, where the "
            "successor function alternates whose choice it is.",
            "<b>Modules 06 and 07 exploit structure</b> — "
            "constraints and action preconditions — <b>to prune and "
            "to derive heuristics automatically.</b> <b>All of it is "
            "this loop.</b>"]},
 ],
 "takeaways": [
   "A search problem is an initial state, actions, a transition function, "
   "a goal test, and costs — and the choice of what counts as a state "
   "is yours and consequential.",
   "There is one search algorithm; the only thing that varies is which "
   "node the frontier returns, which is the whole taxonomy.",
   "Memory, not time, is what stops a search in practice, so estimate the "
   "frontier size before implementing.",
   "Iterative deepening gets breadth-first guarantees at depth-first "
   "memory, because the deepest level dominates the node count.",
   "The explored set converts exponential to polynomial in the number of "
   "states, at the cost of memory proportional to states reached.",
   "Shrinking the state space by abstraction, symmetry, or a better "
   "encoding beats speeding up the search.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Formulating a search problem"),
  ("callout", "A search problem is five things, and one of them is a design "
              "decision",
   ["<b>An initial state; the set of actions available in each state; a "
    "transition function giving the resulting state; a goal test; and a "
    "cost for each action.</b> That is the complete specification, and "
    "every problem in Modules 02 through 07 is written in this form.",
    "<b>The choice of what counts as a state is the consequential "
    "decision, and it is yours</b> — <b>which is exactly "
    "CSCE 669 Module 12 &sect;1's decision-variable choice arriving "
    "in a different subject</b>, with the same property that it "
    "determines tractability more than any later optimisation.",
    "<b>Is a state a grid cell? A grid cell plus a facing direction? "
    "Plus which keys you are carrying? Plus the positions of movable "
    "crates?</b> Each gives a different state space size and a different "
    "set of problems that are solvable at all.",
    "<b>Too coarse and the solution is wrong</b> — a path that "
    "ignores which doors you have keys for is not a path. <b>Too fine and "
    "the space is unsearchable</b>, because every added component "
    "multiplies the size. <b>Get this right before writing any code</b>, "
    "and write the state space size down as a number."]),
  ("code", """frontier = { start }
explored = { }

while frontier not empty:
    node = frontier.REMOVE()      # <-- the only difference
    if goal(node): return path(node)
    explored.add(node.state)
    for each successor s of node:
        if s.state not in explored and s not in frontier:
            frontier.add(s)
return failure

THE ONLY THING THAT VARIES BETWEEN ALGORITHMS IS WHICH NODE
REMOVE() RETURNS:

    a FIFO queue                   -> breadth-first
    a LIFO stack                   -> depth-first
    a priority queue on g(n)       -> uniform cost
    a priority queue on h(n)       -> greedy best-first
    a priority queue on g(n)+h(n)  -> A*       (Module 03)

THAT IS THE WHOLE TAXONOMY. Every search algorithm in
Modules 02 through 07 is this loop with a different frontier
discipline and a different state space.

THE EXPLORED SET is what makes this GRAPH search. Without
it you have TREE search, which revisits states and can loop
forever in a cyclic space. With it, memory grows with the
number of distinct states reached (section 3)."""),
  ("p", "<b>Writing this loop once and parameterising the frontier is the "
        "right implementation decision</b> — it makes the "
        "comparisons of &sect;2 a one-line change rather than five "
        "separate programs, and it makes the unification visible in the "
        "code rather than only in the prose."),

  ("h1", "2 &nbsp; The uninformed strategies"),
  ("table", ["Strategy", "Complete?", "Optimal?", "Space"],
   [["<b>Breadth-first</b>", "<b>Yes.</b>",
     "<b>Only if all step costs are equal.</b>",
     "<b>O(b<super>d</super>) — and this is usually the binding "
     "constraint, not the time</b> (see the callout)."],
    ["<b>Depth-first</b>",
     "<b>No — it can descend an infinite branch forever.</b>",
     "<b>No.</b>",
     "<b>O(bm) — linear in depth. This is its only virtue, and it "
     "is a substantial one.</b>"],
    ["<b>Uniform cost</b>", "<b>Yes.</b>",
     "<b>Yes — for any non-negative costs.</b>",
     "<b>O(b<super>C*/&epsilon;</super>)</b>, which <b>can exceed "
     "breadth-first</b> when there are many cheap steps."],
    ["<b>Iterative deepening</b>", "<b>Yes.</b>",
     "<b>If costs are equal.</b>",
     "<b>O(bd) — breadth-first's guarantees at depth-first's "
     "memory.</b> See the footnote."],
    ["<b>Bidirectional</b>", "Yes.", "If costs are equal.",
     "<b>O(b<super>d/2</super>) — a square root, which is the "
     "largest asymptotic win available without a heuristic.</b> Requires "
     "a predecessor function and a way to test frontier intersection."]],
   [0.21, 0.17, 0.21, 0.41]),
  ("p", "<b>Iterative deepening is the right default when no heuristic is "
        "available</b>, and the reason is worth working through because it "
        "is counterintuitive: it re-searches the top of the tree at every "
        "iteration, which sounds wasteful. <b>But the number of nodes at "
        "depth d is b<super>d</super>, and the sum of all shallower levels "
        "is about b<super>d</super>/(b&minus;1)</b> — so the repeated "
        "work is a constant factor, around 11% at b = 10. <b>The deepest "
        "level dominates the node count, so repeating everything above it "
        "is nearly free.</b>"),
  ("callout", "Memory, not time, is what stops a search",
   ["<b>Breadth-first search at branching factor 10 and depth 12 stores on "
    "the order of 10<super>12</super> nodes.</b> At even 100 bytes per "
    "node that is 100 terabytes of frontier.",
    "<b>The time would be tolerable on a cluster; the memory is not "
    "available anywhere.</b> <b>So the frontier size is the binding "
    "constraint in practice</b>, and it is the first quantity to "
    "estimate — which is the opposite of the intuition most people "
    "bring, that search is slow.",
    "<b>Which is why iterative deepening exists at all</b> (it trades "
    "time for memory, in the favourable direction), and why "
    "memory-bounded heuristic variants such as IDA* and SMA* exist for "
    "the informed case (Module 03 &sect;4).",
    "<b>So estimate b and d before implementing anything.</b> "
    "<b>b<super>d</super> tells you immediately whether the problem needs "
    "a heuristic, a reformulation (&sect;4), or an "
    "approximation</b> — and the estimate takes two minutes while "
    "discovering it empirically takes a day."]),

  ("break",),
  ("h1", "3 &nbsp; Graph search against tree search"),
  ("ul", ["<b>In a cyclic state space, tree search can loop "
          "forever</b> — walking back and forth between two states, "
          "each time generating the other as a fresh successor. The search "
          "is not slow; it does not terminate.",
          "<b>In an acyclic space it still explodes.</b> A grid with four "
          "movement actions has exponentially many distinct paths to each "
          "cell, and <b>tree search explores all of them</b>, although "
          "they all arrive at the same place.",
          "<b>So the explored set converts an exponential node count into "
          "one polynomial in the number of states</b> — which is "
          "frequently the difference between a search that finishes and "
          "one that does not, and is a far larger effect than any "
          "constant-factor optimisation.",
          "<b>The cost is memory proportional to the number of states "
          "reached</b>, which is <b>why depth-first search's linear "
          "memory advantage is lost</b> as soon as you add duplicate "
          "detection — a trade worth making explicitly rather than "
          "by default.",
          "<b>And the state must be hashable and compared correctly.</b> "
          "<b>A subtle equality bug here produces a search that is merely "
          "slow rather than broken</b> — duplicates are not detected, "
          "the node count inflates, and <b>nothing alerts you because the "
          "answers are still correct</b>. <b>Instrument the "
          "duplicate-detection rate</b> and look at it: if almost nothing "
          "is detected as a duplicate, either your state representation is "
          "too fine (&sect;1) or your equality is wrong."]),

  ("h1", "4 &nbsp; Reformulation"),
  ("callout", "Shrinking the state space beats speeding up the search",
   ["<b>Abstraction.</b> Search over rooms rather than individual tiles, "
    "find a room-level path, then refine within each room. <b>This is "
    "hierarchical pathfinding</b> (Module 04 &sect;3), it reduces the "
    "effective depth dramatically, and it is the single most used "
    "reformulation in games.",
    "<b>Symmetry elimination.</b> If two states are equivalent under a "
    "symmetry of the problem, search only one of them. <b>This is "
    "CSCE 669 Module 09 &sect;4's symmetry breaking</b> arriving in a "
    "different subject, with the same enormous effect — and the same "
    "property of being invisible until you look for it.",
    "<b>Macro-actions.</b> Collapse a commonly useful action sequence "
    "into a single action, reducing depth at the cost of increasing the "
    "branching factor. <b>Since depth is in the exponent and branching "
    "is the base, this is usually favourable</b>, which is the same "
    "arithmetic as bidirectional search's square root.",
    "<b>And a better state encoding.</b> <b>Dropping a state component "
    "that the solution does not depend on divides the space by that "
    "component's range</b> — so <b>ask of every state component "
    "whether any solution's correctness depends on it</b>, and remove the "
    "ones that fail. This is the cheapest and most frequently available "
    "win, and &sect;1's warning applies in the other direction too."]),
  ("callout", "Where this goes next",
   ["<b>Module 03 adds a heuristic</b>, which is the single largest "
    "available improvement — <b>it changes the effective branching "
    "factor rather than a constant</b>, so the effect compounds with "
    "depth.",
    "<b>Module 04 applies it to the track's problem</b>, pathfinding, "
    "with the engineering that production systems require and that the "
    "algorithm alone does not supply.",
    "<b>Module 05 searches against an opponent</b>, where the successor "
    "function alternates whose choice it is, and the evaluation becomes a "
    "minimax rather than a cost.",
    "<b>Modules 06 and 07 exploit problem structure</b> — "
    "constraint networks and action preconditions — <b>to prune "
    "the frontier and to derive heuristics automatically rather than by "
    "hand</b>. <b>All of it is the loop in &sect;1</b>, which is worth "
    "keeping in mind as the state spaces get stranger."]),
 ],
 "resources": [
   ("Russell & Norvig &mdash; AIMA, chapter 3 (pseudocode free)",
    "https://aima.cs.berkeley.edu/",
    "<b>The reference for this module.</b> The generic algorithm of "
    "&sect;1 and the comparison table of &sect;2 are from here."),
   ("Berkeley CS188 &mdash; search lectures and Project 1 (free)",
    "https://inst.eecs.berkeley.edu/~cs188/",
    "<b>The Pacman search project</b>, which is the best available "
    "exercise for this material and includes the state-formulation "
    "decisions of &sect;1."),
   ("Korf &mdash; Depth-First Iterative-Deepening (free)",
    "https://www.sciencedirect.com/science/article/pii/0004370285900840",
    "<b>The &sect;2 result</b>, with the node-count argument worked out "
    "properly."),
   ("Red Blob Games &mdash; Introduction to Graph Search (free, "
    "interactive)",
    "https://www.redblobgames.com/pathfinding/a-star/introduction.html",
    "<b>Interactive visualisations of every strategy in &sect;2</b>, and "
    "the clearest intuition-builder available."),
 ],
 "exercises": [
   "<b>Implement the generic search loop once</b> and parameterise the "
   "frontier. Instantiate all five strategies.",
   "<b>Formulate one problem three ways</b> with different state "
   "definitions, and report the state space size of each.",
   "<b>Report nodes expanded for each strategy</b> on the same problem.",
   "<b>Confirm iterative deepening's overhead</b> empirically and compare "
   "against the predicted constant factor.",
   "<b>Run tree search on a cyclic space</b> and confirm it does not "
   "terminate.",
   "<b>Instrument the duplicate-detection rate</b> and report it for two "
   "state representations.",
   "<b>Introduce an equality bug deliberately</b> and measure the node "
   "count inflation. Confirm the answers stay correct.",
   "<b>Estimate b and d</b> for a problem you care about, and compute "
   "b^d.",
   "<b>Implement bidirectional search</b> and verify the square-root node "
   "count.",
   "<b>Apply one reformulation from &sect;4</b> and report the state "
   "space reduction.",
 ],
 "selfcheck": [
   "Name the five components of a search problem.",
   "Why is the state definition the consequential decision?",
   "Write the generic search loop and say what varies between "
   "algorithms.",
   "Compare five strategies on completeness, optimality, and space.",
   "Why is iterative deepening's overhead only a constant factor?",
   "Why is memory rather than time the binding constraint?",
   "What does the explored set buy and cost?",
   "Why is an equality bug in the state particularly dangerous?",
   "Name four reformulations and what each reduces.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Heuristic Search",
 "subtitle": "A* and where the information comes from.",
 "question": "How much is a good estimate worth?",
 "outcomes": [
     "State A* and prove its optimality conditions.",
     "Distinguish admissibility from consistency and know when each "
     "matters.",
     "Explain dominance and the effective branching factor.",
     "Derive heuristics from relaxations and pattern databases.",
     "Choose a memory-bounded or suboptimal variant deliberately.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "A*",
   "blurb": "Expand by cost-so-far plus estimate-to-go."},

  {"t": "eq", "kicker": "A*", "title": "The evaluation function, and what it means",
   "eqs": [
     ("f(n) = g(n) + h(n)",
      "Cost to reach n, plus the estimated cost from n to a goal."),
     ("Expand the node with the lowest f",
      "Uniform cost is h = 0; greedy best-first is g = 0. A* is "
      "the combination, and the combination is what gives the "
      "guarantee."),
     ("f(n) is an estimate of the best solution THROUGH n",
      "So A* expands nodes in order of how promising the complete "
      "solution through them looks, which is the right order."),
   ],
   "caption": "<b>The two degenerate cases are instructive:</b> h = 0 "
              "is optimal and slow; g = 0 is fast and wrong. "
              "<b>A* is the only point on that line with both "
              "properties.</b>",
   "note": "Framing A* as the interpolation between two known algorithms "
           "makes it inevitable rather than clever."},

  {"t": "callout", "title": "Admissible for optimality; consistent for efficiency",
   "kind": "The two conditions, and the difference matters",
   "body": ["<b>Admissible: h(n) never overestimates the true remaining "
            "cost.</b> <b>This is what makes A* optimal</b> — an "
            "overestimate can make the optimal path look worse than it "
            "is, so A* commits early and wrongly.",
            "<b>Consistent (monotone): h(n) ≤ cost(n,n′) + "
            "h(n′) for every edge.</b> A triangle inequality on "
            "the heuristic.",
            "<b>Consistency implies admissibility</b>, and it is what "
            "lets you close a node permanently on first expansion. "
            "<b>With an inconsistent heuristic you must allow "
            "reopening</b>, or you lose optimality in graph search.",
            "<b>Nearly every natural heuristic is consistent</b>, so "
            "this rarely bites — <b>but it bites hard when it "
            "does</b>, and the symptom is suboptimal paths from a "
            "provably admissible heuristic."]},

  {"t": "section", "label": "Part 2", "title": "How much it is worth",
   "blurb": "Dominance, and the effective branching factor."},

  {"t": "callout", "title": "A better heuristic reduces the exponent's base",
   "kind": "Why this is the biggest available win",
   "body": ["<b>If h₁(n) ≥ h₂(n) everywhere and both are "
            "admissible, h₁ <i>dominates</i></b> and A* with "
            "h₁ never expands more nodes than with h₂.",
            "<b>So always prefer the larger admissible heuristic</b>, "
            "and <b>the maximum of several admissible heuristics is "
            "admissible</b> — which is a free improvement if you can "
            "afford the computation.",
            "<b>The measure is the <i>effective branching factor</i> "
            "b*</b>, defined by N = (b*)^d. <b>Dropping b* from 2.8 to "
            "1.4 at depth 20 is a factor of a million</b>, not a factor "
            "of two.",
            "<b>Which is why heuristic design beats "
            "micro-optimisation</b> by an enormous margin — and why "
            "Part 3's automatic derivation is one of the field's best "
            "results."]},

  {"t": "table", "kicker": "Trade", "title": "Heuristic accuracy against computation cost",
   "header": ["Heuristic", "Cost to compute", "Nodes expanded"],
   "widths": [3.0, 3.6, 5.4],
   "rows": [
     ["<b>h = 0</b>", "<b>Free</b>", "<b>Everything within the optimal cost</b>"],
     ["<b>Manhattan</b>", "<b>O(1)</b>", "<b>Far fewer; the standard grid default</b>"],
     ["<b>Pattern database</b>", "<b>Hours, once, offline</b>", "<b>Orders of magnitude fewer</b>"],
     ["<b>Exact h</b>", "As hard as the problem", "<b>Exactly the solution path. Useless</b>"],
   ],
   "footnote": "<b>The right point depends on how many queries you will "
               "make:</b> an offline precomputation that costs hours and "
               "is reused a million times is obviously correct, and for "
               "one query it is not.",
   "note": "The amortisation argument is what justifies pattern "
           "databases."},

  {"t": "section", "label": "Part 3", "title": "Where heuristics come from",
   "blurb": "Deriving them rather than inventing them."},

  {"t": "code", "kicker": "Derivation", "title": "Three systematic sources",
   "lang": "text", "code": """
  1. RELAXATION -- remove a constraint, solve exactly.
     The relaxed solution cost is an ADMISSIBLE heuristic
     for the original, because any real solution is also a
     relaxed solution.

     8-puzzle: allow tiles to pass through each other
         -> each tile moves independently
         -> MANHATTAN DISTANCE, summed. Admissible, free.
     Allow a tile to teleport
         -> MISPLACED TILE COUNT. Admissible, weaker.

     THIS IS CSCE 669 MODULE 10's BOUND-FROM-A-RELAXATION
     ARGUMENT, in a different subject. Same idea exactly.

  2. PATTERN DATABASE -- abstract the state (track only
     some tiles), solve EVERY abstract state exhaustively
     offline, store the costs. Look up at search time.
     Very strong. Memory-hungry. Precomputed once.

     DISJOINT pattern databases can be ADDED rather than
     maxed, if the subproblems share no moves -- which
     multiplies their strength.

  3. LEARNED -- fit h from solved instances. Fast, and
     ADMISSIBILITY IS LOST, so optimality goes with it.
     Sometimes an acceptable trade; say so when you make it.
""",
   "caption": "<b>Relaxation is the one to internalise</b> — it "
              "turns heuristic design from invention into a mechanical "
              "procedure, and it generalises to planning (Module 07).",
   "note": "The link to the approximation-algorithms argument is the "
           "intellectual high point of the module."},

  {"t": "section", "label": "Part 4", "title": "When A* is too expensive",
   "blurb": "Memory bounds and bounded suboptimality."},

  {"t": "bullets", "kicker": "Variants", "title": "The deliberate compromises",
   "items": [
     "<b>IDA*</b> — iterative deepening on f. <b>Linear memory, "
     "optimal, and it repeats work.</b> The right choice when memory is "
     "the constraint.",
     "",
     "<b>Weighted A*: f = g + w·h with w > 1.</b> <b>Returns a "
     "solution at most w times optimal</b>, far faster. <b>A bounded, "
     "stated compromise.</b>",
     "",
     "<b>Beam search</b> — keep only the best k nodes. Fast, no "
     "guarantee at all, and it can miss the solution entirely.",
     "",
     "<b>Anytime A*</b> — return a solution quickly, improve it "
     "while time remains. <b>The right shape for a game loop</b> "
     "(Module 04 §4).",
     "",
     "<b>And bidirectional A*</b>, which is harder than it looks "
     "because the two searches must meet correctly.",
   ],
   "footnote": "<b>Weighted A* is the one to reach for first:</b> "
               "<b>w = 1.5 is typically several times faster and within "
               "a few percent of optimal in practice</b>, and the bound "
               "is proved."},

  {"t": "callout", "title": "Report nodes expanded, not seconds",
   "kind": "The measurement discipline",
   "body": ["<b>Wall-clock time confounds the algorithm with your "
            "implementation</b>, your language, and your successor "
            "function's efficiency.",
            "<b>Nodes expanded isolates the algorithmic question</b>, "
            "and it is what the theory predicts — so it is the "
            "number that can be compared against anything.",
            "<b>Report both.</b> <b>A heuristic that halves nodes and "
            "triples time per node is a loss</b>, and only reporting "
            "both reveals it.",
            "<b>And report the effective branching factor</b>, which "
            "normalises for problem depth and is therefore the only "
            "figure comparable across instances."]},
 ],
 "takeaways": [
   "A* expands by g plus h, interpolating between uniform cost (h = 0, "
   "optimal and slow) and greedy best-first (g = 0, fast and wrong).",
   "Admissibility gives optimality; consistency additionally lets you "
   "close nodes permanently, and without it graph search must allow "
   "reopening.",
   "A dominating heuristic never expands more nodes, and the maximum of "
   "several admissible heuristics is admissible — a free "
   "improvement.",
   "The measure is the effective branching factor, and reducing it from "
   "2.8 to 1.4 at depth 20 is a factor of a million.",
   "Relaxation derives admissible heuristics mechanically, and it is "
   "CSCE 669's bound-from-a-relaxation argument in a different subject.",
   "Weighted A* gives a proved bound of w times optimal for a large "
   "speedup, which is the right first compromise.",
 ],
 "notes": [
  ("h1", "1 &nbsp; A*"),
  ("eq", "f(n) = g(n) + h(n)"),
  ("p", "<b>Cost to reach n, plus the estimated cost from n to a "
        "goal</b> — so f(n) estimates the cost of the best complete "
        "solution <i>through</i> n, and expanding the lowest f means "
        "expanding in order of how promising the whole solution looks. "
        "<b>The two degenerate cases are the most useful way to see "
        "it:</b> <b>h = 0 gives uniform cost search</b> (optimal and "
        "slow, expanding everything within the optimal cost), and "
        "<b>g = 0 gives greedy best-first</b> (fast and not optimal, "
        "because it ignores what it has already spent). <b>A* is the "
        "combination, and it is the only point on that line with both "
        "properties</b> — which makes it inevitable rather than "
        "clever."),
  ("callout", "Admissible for optimality; consistent for efficiency",
   ["<b>Admissible: h(n) never overestimates the true remaining cost to "
    "the nearest goal.</b> <b>This is the condition that makes A* "
    "optimal</b>, and the reason is worth holding: an overestimate can "
    "make the node on the optimal path look worse than a node that is "
    "not, so A* expands the wrong one and may reach a goal by a worse "
    "route before the better route's f value comes up.",
    "<b>Consistent (or monotone): h(n) &le; cost(n, n&prime;) + "
    "h(n&prime;) for every edge n to n&prime;.</b> A triangle inequality "
    "on the heuristic — the estimate cannot drop by more than the "
    "step cost.",
    "<b>Consistency implies admissibility</b>, and it is the condition "
    "that lets you <b>close a node permanently on first expansion</b>, "
    "because f is then non-decreasing along any path and the first "
    "expansion of a state is along an optimal path to it. <b>With an "
    "inconsistent (but admissible) heuristic you must allow reopening "
    "closed nodes</b>, or graph search loses optimality.",
    "<b>Nearly every natural heuristic is consistent</b>, so this rarely "
    "bites in practice — <b>but it bites hard when it does</b>, and "
    "<b>the symptom is suboptimal paths returned by an implementation "
    "using a heuristic you have correctly proved admissible</b>. It is "
    "worth knowing the distinction purely so that this symptom is "
    "diagnosable, because otherwise it looks like a code bug and is "
    "not."]),

  ("h1", "2 &nbsp; What a heuristic is worth"),
  ("callout", "A better heuristic reduces the exponent's base",
   ["<b>If h<sub>1</sub>(n) &ge; h<sub>2</sub>(n) at every node and both "
    "are admissible, then h<sub>1</sub> <i>dominates</i> h<sub>2</sub></b>, "
    "and A* with h<sub>1</sub> never expands more nodes than A* with "
    "h<sub>2</sub> — a clean result with no caveats.",
    "<b>So always prefer the larger admissible heuristic.</b> <b>And "
    "the pointwise maximum of several admissible heuristics is itself "
    "admissible</b>, which is a free improvement whenever you can afford "
    "to compute all of them — and the cost-benefit of doing so is "
    "exactly the trade in the table below.",
    "<b>The right measure is the <i>effective branching factor</i> b*</b>, "
    "defined by N = (b*)<super>d</super> where N is the nodes expanded "
    "and d the solution depth — the uniform branching factor that "
    "would have produced the same node count. <b>Dropping b* from 2.8 to "
    "1.4 at depth 20 is a factor of about a million</b>, not a factor of "
    "two, because the improvement is in the base of an exponential.",
    "<b>Which is why heuristic design beats micro-optimisation by an "
    "enormous margin</b>, and why &sect;3's systematic derivation is one "
    "of the field's genuinely good results — it converts the largest "
    "available lever from a matter of inspiration into a procedure."]),
  ("table", ["Heuristic", "Cost to compute", "Nodes expanded"],
   [["<b>h = 0</b>", "<b>Free.</b>",
     "<b>Everything within the optimal cost</b> — the uniform cost "
     "baseline."],
    ["<b>Manhattan distance (grid)</b>", "<b>O(1) per node.</b>",
     "<b>Far fewer. The standard default for grid pathfinding</b>, and "
     "nearly always the right starting point."],
    ["<b>Pattern database</b>",
     "<b>Hours, once, offline; then O(1) per lookup.</b>",
     "<b>Orders of magnitude fewer</b> — the strongest practical "
     "option for puzzle-like problems (&sect;3)."],
    ["<b>Exact h</b>", "As hard as solving the original problem.",
     "<b>Exactly the solution path and nothing else — and therefore "
     "useless</b>, since computing it was the problem."]],
   [0.24, 0.29, 0.47]),
  ("p", "<b>The right point on that table depends on how many queries you "
        "will make.</b> <b>An offline precomputation costing hours and "
        "reused a million times is obviously correct; for a single query "
        "it is obviously not</b> — and in a game, where the same "
        "level is searched thousands of times per session, the "
        "amortisation argument favours precomputation far more than it "
        "does in a one-shot academic benchmark. <b>This is the argument "
        "behind Module 04 &sect;3's precomputed hierarchies.</b>"),

  ("break",),
  ("h1", "3 &nbsp; Where heuristics come from"),
  ("code", """1. RELAXATION -- remove a constraint from the problem and
   solve the relaxed version exactly. The relaxed solution
   cost is an ADMISSIBLE heuristic for the original,
   because every real solution is also a relaxed solution
   and therefore costs at least as much.

   8-puzzle, allow tiles to pass through each other:
       each tile moves independently
       -> MANHATTAN DISTANCE summed over tiles.
          Admissible, O(1), and the standard choice.
   8-puzzle, allow a tile to teleport anywhere:
       -> MISPLACED TILE COUNT. Admissible, weaker,
          dominated by Manhattan.

   THIS IS CSCE 669 MODULE 10's BOUND-FROM-A-RELAXATION
   ARGUMENT, in a different subject, with the inequality
   pointing the same way. Same idea, exactly.

2. PATTERN DATABASE -- abstract the state so that only
   some components are tracked, solve EVERY abstract state
   exhaustively offline by backward breadth-first search,
   and store the exact abstract costs. Look up at search
   time in O(1).
   Very strong. Memory-hungry. Precomputed once.

   DISJOINT pattern databases can be ADDED rather than
   maxed, if the subproblems share no moves -- which
   multiplies rather than merely improves their strength.

3. LEARNED -- fit h from solved instances. Fast to
   evaluate, and ADMISSIBILITY IS LOST, so optimality goes
   with it. Sometimes an acceptable trade. Say so when you
   make it, and report the suboptimality you measured."""),
  ("p", "<b>Relaxation is the one to internalise.</b> <b>It turns "
        "heuristic design from an act of invention into a mechanical "
        "procedure</b>: list the problem's constraints, drop one, check "
        "whether the relaxed problem is easy, and if so you have an "
        "admissible heuristic with a one-line proof. <b>And it "
        "generalises</b> — <b>Module 07 &sect;3 derives planning "
        "heuristics by exactly this method, automatically, from the action "
        "descriptions</b>, which is what made modern planners work."),

  ("h1", "4 &nbsp; When A* is too expensive"),
  ("ul", ["<b>IDA*</b> — iterative deepening on the f value rather "
          "than on depth. <b>Linear memory, still optimal, and it repeats "
          "work</b> (Module 02 &sect;2's constant-factor argument "
          "applies). <b>The right choice when memory is the binding "
          "constraint</b>, which Module 02 argued is usual.",
          "<b>Weighted A*: f = g + w&middot;h with w &gt; 1.</b> "
          "<b>Returns a solution at most w times the optimal cost</b>, "
          "and does so far faster because the heuristic is effectively "
          "trusted more. <b>A bounded and stated compromise</b>, which is "
          "the kind worth making.",
          "<b>Beam search</b> — keep only the best k nodes at each "
          "level and discard the rest. Fast, constant memory, <b>no "
          "guarantee at all, and it can discard the only path to the "
          "goal</b> and report failure on a solvable problem.",
          "<b>Anytime A*</b> — return a solution quickly, then "
          "continue improving it while time remains, reporting the current "
          "best when interrupted. <b>The right shape for a game "
          "loop</b> (Module 04 &sect;4), because the deadline is "
          "external and non-negotiable.",
          "<b>And bidirectional A*</b>, which is substantially harder "
          "than bidirectional uniform-cost search because the two "
          "searches' f values are not comparable and the meeting "
          "condition is subtle — worth knowing exists, and not worth "
          "implementing casually.",
          "<b>Weighted A* is the one to reach for first.</b> <b>w = 1.5 "
          "is typically several times faster and within a few percent of "
          "optimal in practice</b>, well inside its 50% bound — and "
          "the bound is proved, so the compromise is quantified rather "
          "than hoped."]),
  ("callout", "Report nodes expanded, not seconds",
   ["<b>Wall-clock time confounds the algorithm with your implementation, "
    "your language, your data structures, and the efficiency of your "
    "successor function</b> — four things that have nothing to do "
    "with the question you are usually asking.",
    "<b>Nodes expanded isolates the algorithmic question</b>, and it is "
    "the quantity the theory predicts, <b>so it is the number that can be "
    "compared against a textbook, a paper, or someone else's "
    "implementation.</b>",
    "<b>Report both, though.</b> <b>A heuristic that halves the nodes "
    "expanded and triples the time per node is a net loss</b>, and only "
    "reporting both reveals it — which is a real and common outcome "
    "with expensive heuristics.",
    "<b>And report the effective branching factor</b> (&sect;2), which "
    "normalises for solution depth and is therefore <b>the only figure "
    "comparable across problem instances of different sizes</b> — "
    "nodes expanded alone conflates the heuristic's quality with the "
    "instance's difficulty."]),
 ],
 "resources": [
   ("Russell & Norvig &mdash; AIMA, chapter 3 (sections on informed "
    "search)",
    "https://aima.cs.berkeley.edu/",
    "<b>A*, admissibility, consistency, and the relaxation argument of "
    "&sect;3</b>, with the 8-puzzle worked through."),
   ("Hart, Nilsson & Raphael &mdash; A Formal Basis for the Heuristic "
    "Determination of Minimum Cost Paths (free)",
    "https://ieeexplore.ieee.org/document/4082128",
    "<b>The original A* paper</b>, with the optimality proof. Short and "
    "readable."),
   ("Korf &mdash; Disjoint Pattern Database Heuristics (free)",
    "https://www.sciencedirect.com/science/article/pii/S0004370201001048",
    "<b>The &sect;3 pattern database method</b>, including the additivity "
    "condition that makes them so strong."),
   ("Red Blob Games &mdash; Heuristics (free, interactive)",
    "https://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html",
    "<b>The practical guide for grid heuristics</b>, including weighted "
    "A* and tie-breaking, with interactive demonstrations."),
 ],
 "exercises": [
   "<b>Implement A*</b> on top of Module 02's generic loop and verify it "
   "reduces to uniform cost at h = 0.",
   "<b>Prove Manhattan distance admissible</b> for the 8-puzzle via the "
   "relaxation argument.",
   "<b>Construct an inadmissible heuristic</b> and exhibit a problem "
   "where A* returns a suboptimal path.",
   "<b>Construct an admissible but inconsistent heuristic</b> and show "
   "that closing nodes permanently loses optimality.",
   "<b>Compare misplaced-tiles against Manhattan</b> and confirm "
   "dominance empirically.",
   "<b>Compute the effective branching factor</b> for each and report the "
   "ratio.",
   "<b>Build a pattern database</b> for a subset of the 15-puzzle tiles "
   "and measure the improvement.",
   "<b>Implement weighted A*</b> and plot nodes expanded and solution "
   "cost against w from 1.0 to 3.0.",
   "<b>Confirm the w-bound holds</b> on every instance.",
   "<b>Implement IDA*</b> and compare peak memory against A*.",
 ],
 "selfcheck": [
   "State A* and explain why the combination of g and h is necessary.",
   "Define admissibility and consistency, and say what each buys.",
   "What is the symptom of an inconsistent heuristic in graph search?",
   "Define dominance, and state the free improvement it implies.",
   "What is the effective branching factor and why is it the right "
   "measure?",
   "Derive two 8-puzzle heuristics by relaxation.",
   "What other course does the relaxation argument come from?",
   "What is a pattern database, and when can two be added?",
   "Name four variants of A* and the compromise each makes.",
   "Why report nodes expanded rather than seconds?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Pathfinding in Practice",
 "subtitle": "The search that ships in every engine.",
 "question": "How does a game actually move a character across a level?",
 "outcomes": [
     "Choose a spatial representation and justify it.",
     "Explain navigation meshes and how they are built.",
     "Implement hierarchical and any-angle pathfinding.",
     "Handle dynamic obstacles and replanning under a frame budget.",
     "Separate pathfinding from path following.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Representation",
   "blurb": "The graph you search is a design decision."},

  {"t": "table", "kicker": "Representations", "title": "What to search over",
   "header": ["Representation", "Nodes", "Trade"],
   "widths": [2.7, 3.9, 5.4],
   "rows": [
     ["<b>Grid</b>", "<b>One per cell</b>", "<b>Trivial to build; huge node count; paths look blocky</b>"],
     ["<b>Waypoint graph</b>", "<b>Hand-placed points</b>", "<b>Tiny and fast; manual; agents hug the waypoints</b>"],
     ["<b>Navigation mesh</b>", "<b>Convex polygons of walkable floor</b>", "<b>The standard. Few nodes, free space, any-angle paths</b>"],
     ["<b>Visibility graph</b>", "Obstacle corners", "<b>Exactly optimal in 2D; O(n²) to build</b>"],
     ["<b>Probabilistic roadmap</b>", "<b>Random samples + local planner</b>", "<b>For high-DoF configuration spaces, not floors</b>"],
   ],
   "footnote": "<b>The navigation mesh won because its node count "
               "scales with the <i>complexity</i> of the level rather "
               "than with its area</b> — a large empty room is one "
               "polygon and ten thousand grid cells.",
   "note": "That scaling argument is the whole reason navmeshes "
           "dominate."},

  {"t": "callout", "title": "A navigation mesh is a convex decomposition of walkable floor",
   "kind": "How it works and how it is built",
   "body": ["<b>Partition the walkable surface into convex "
            "polygons</b>, adjacent where an agent can cross between "
            "them. Search the adjacency graph.",
            "<b>Convexity is the point:</b> <b>inside one polygon, "
            "straight-line movement is guaranteed collision-free</b>, so "
            "the search only has to find the sequence of polygons.",
            "<b>Built by voxelising the level, extracting the walkable "
            "surface by slope and height clearance, then region-growing "
            "and polygonising</b> — which is what Recast does, and "
            "it runs offline per level.",
            "<b>Agent radius is baked in by eroding the walkable "
            "area</b>, so a mesh is per-agent-size. <b>Which is why "
            "engines build several</b>, and why a large enemy sometimes "
            "cannot follow you through a gap."]},

  {"t": "section", "label": "Part 2", "title": "Any-angle paths",
   "blurb": "The graph path is not the path you want."},

  {"t": "code", "kicker": "Smoothing", "title": "Why the A* result is not the answer",
   "lang": "text", "code": """
  A* ON A GRID gives a path restricted to grid edges, so it
  zigzags along 45-degree diagonals when a straight line was
  available. It is OPTIMAL ON THE GRAPH and wrong for the
  world -- the graph was your approximation (Module 01).

  THREE FIXES:

  STRING PULLING / FUNNEL ALGORITHM
      walk the polygon sequence from the navmesh and pull
      the path taut within the corridor. O(n) and EXACT
      within the corridor the search found. The standard
      answer for navmeshes.

  THETA* / LAZY THETA*
      during the search, let a node's parent be any
      ancestor with line of sight, not just the previous
      node. Produces any-angle paths directly, at the cost
      of line-of-sight checks.

  POST-HOC SMOOTHING
      repeatedly try to replace two segments with one if
      line of sight permits. Simple, and it can cut corners
      the agent cannot physically take.

  NOTE THE CAVEAT ON STRING PULLING: it is optimal within
  the corridor, and the corridor may not contain the
  globally optimal path. Usually fine, occasionally not.
""",
   "caption": "<b>Optimal on the graph is not optimal in the world</b>, "
              "and the gap is exactly the discretisation you chose "
              "— Module 01 §2's lie, with a visible "
              "symptom.",
   "note": "The zigzag is the most recognisable artefact in game AI and "
           "makes the point concretely."},

  {"t": "section", "label": "Part 3", "title": "Scaling",
   "blurb": "Many agents, large levels, one frame budget."},

  {"t": "bullets", "kicker": "Scaling", "title": "How production systems get the cost down",
   "items": [
     "<b>Hierarchy.</b> Search clusters first, then within clusters. "
     "<b>HPA* reduces node counts by orders of magnitude</b> for "
     "near-optimal paths (Module 02 §4's abstraction).",
     "",
     "<b>Precomputation.</b> <b>All-pairs cluster distances, or a "
     "full flow field</b> if many agents share one destination.",
     "",
     "<b>Flow fields.</b> <b>One Dijkstra from the goal gives every "
     "agent its direction</b> — the cost is independent of agent "
     "count, which is how RTS games move hundreds of units.",
     "",
     "<b>Time-slicing.</b> <b>Spread one search over several frames</b> "
     "and budget a fixed number of node expansions per frame.",
     "",
     "<b>And caching.</b> Agents repeat queries constantly; a path "
     "cache keyed on polygon pairs pays immediately.",
   ],
   "footnote": "<b>Flow fields are the key insight for crowds:</b> "
               "<b>invert the problem</b> — one search from the "
               "goal, rather than one search per agent."},

  {"t": "callout", "title": "Dynamic obstacles, and when to replan",
   "kind": "The hard part in practice",
   "body": ["<b>A door closes, a crate is pushed, another agent blocks "
            "a corridor.</b> The path you computed is now invalid.",
            "<b>Full replanning every frame is unaffordable</b>, and "
            "<b>replanning only on collision is too late</b> — the "
            "agent is already stuck.",
            "<b>D* Lite repairs the previous search</b> rather than "
            "redoing it, at a cost proportional to what changed. <b>The "
            "right tool for a mostly-static world with local "
            "changes.</b>",
            "<b>And local avoidance is a separate layer:</b> <b>agents "
            "avoid each other by steering, not by replanning</b> "
            "(Module 11 §3), because the path is a plan and "
            "avoidance is a reflex."]},

  {"t": "section", "label": "Part 4", "title": "Following",
   "blurb": "The path is not the motion."},

  {"t": "callout", "title": "Pathfinding and path following are different problems",
   "kind": "The separation that keeps it tractable",
   "body": ["<b>Pathfinding answers 'which way'. Path following "
            "answers 'how to move along it' —</b> with "
            "acceleration limits, turn radius, animation, and other "
            "agents.",
            "<b>Conflating them produces a search over a far larger "
            "state space</b> (position, velocity, heading) <b>for little "
            "benefit in most games.</b>",
            "<b>So the standard architecture is three layers:</b> a "
            "global path from the navmesh, local steering along it, and "
            "collision resolution underneath.",
            "<b>And when the vehicle's constraints genuinely "
            "matter</b> — a car, a tank with a turn radius — "
            "<b>you need kinodynamic planning, which is a different and "
            "much harder problem.</b> <b>Know which case you are "
            "in.</b>"]},

  {"t": "bullets", "kicker": "Debugging", "title": "Diagnosing bad pathfinding",
   "items": [
     "<b>Agent walks into a wall:</b> navmesh does not match "
     "collision geometry. <b>The most common bug, and it is a content "
     "problem.</b>",
     "",
     "<b>Agent takes a long way round:</b> a missing mesh connection, "
     "or a cost that does not reflect intent.",
     "",
     "<b>Agent oscillates between two paths:</b> <b>replanning "
     "flip-flops between near-equal options.</b> Add hysteresis.",
     "",
     "<b>Agents bunch up at a doorway:</b> all share one path and "
     "local avoidance is fighting it. <b>This is Module 11's "
     "problem.</b>",
     "",
     "<b>Frame spikes:</b> an unbounded search. <b>Cap expansions per "
     "frame and measure p99, not the mean.</b>",
   ],
   "footnote": "<b>Render the navmesh and the computed path in the "
               "game.</b> <b>Almost every pathfinding bug is visible "
               "immediately and invisible otherwise</b> — the same "
               "'look at the frame' discipline as CSCE 647."},
 ],
 "takeaways": [
   "The navigation mesh won because its node count scales with level "
   "complexity rather than area — a large empty room is one polygon, "
   "not ten thousand cells.",
   "Convexity is the point of a navmesh: inside one polygon, straight-line "
   "movement is guaranteed collision-free.",
   "Optimal on the graph is not optimal in the world, and the zigzag "
   "artefact is exactly the discretisation you chose.",
   "Flow fields invert the problem — one search from the goal rather "
   "than one per agent — which is how hundreds of units are moved.",
   "D* Lite repairs the previous search at a cost proportional to what "
   "changed, which suits a mostly-static world.",
   "Pathfinding and path following are different problems, and conflating "
   "them explodes the state space for little benefit.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Spatial representation"),
  ("table", ["Representation", "Nodes are", "Trade"],
   [["<b>Grid</b>", "<b>One per cell.</b>",
     "<b>Trivial to build from a tilemap; huge node count; paths look "
     "blocky</b> (&sect;2). Fine for tile-based games, poor for "
     "continuous worlds."],
    ["<b>Waypoint graph</b>", "<b>Hand-placed points with edges.</b>",
     "<b>Tiny and extremely fast; requires manual placement; agents visibly "
     "hug the waypoints</b> rather than using the free space, which was "
     "the characteristic look of late-1990s game AI."],
    ["<b>Navigation mesh</b>",
     "<b>Convex polygons covering the walkable floor.</b>",
     "<b>The standard answer.</b> Few nodes, agents use the full free "
     "space, and any-angle paths come naturally (&sect;2)."],
    ["<b>Visibility graph</b>", "Obstacle corners.",
     "<b>Yields exactly optimal 2D paths</b> (the optimal path bends only "
     "at corners), <b>and costs O(n&#178;) to build</b> — "
     "CSCE 620 Module 06's structure, used here."],
    ["<b>Probabilistic roadmap / RRT</b>",
     "<b>Random configuration samples joined by a local planner.</b>",
     "<b>For high-degree-of-freedom configuration spaces</b> — a "
     "robot arm, a vehicle with a turn radius — <b>not for walking "
     "on floors.</b> See &sect;4."]],
   [0.21, 0.30, 0.49]),
  ("p", "<b>The navigation mesh won because its node count scales with the "
        "<i>complexity</i> of the level rather than with its area.</b> "
        "<b>A large empty room is one polygon and ten thousand grid "
        "cells</b> — and since Module 03 &sect;2 established that "
        "search cost is exponential in depth, reducing the node count by "
        "three orders of magnitude is not a constant-factor saving."),
  ("callout", "A navigation mesh is a convex decomposition of walkable "
              "floor",
   ["<b>Partition the walkable surface into convex polygons</b>, marked "
    "adjacent where an agent can cross directly from one to the next. "
    "<b>Search the polygon adjacency graph with A*</b>, exactly as in "
    "Module 03.",
    "<b>Convexity is the entire point.</b> <b>Inside a single convex "
    "polygon, straight-line movement between any two points is guaranteed "
    "collision-free</b> — so the search only needs to find the "
    "<i>sequence</i> of polygons, and the geometry within each is solved "
    "(which is what makes &sect;2's funnel algorithm exact).",
    "<b>Built by voxelising the level geometry, extracting the walkable "
    "surface by slope and height clearance, then region-growing the voxel "
    "surface into areas and polygonising those</b> — which is what "
    "Recast does, and it runs offline per level as part of the content "
    "pipeline. <b>CSCE 645's surface representations and CSCE 620's "
    "polygon decomposition both appear here</b>, which is why those "
    "courses preceded this one.",
    "<b>Agent radius is baked in by eroding the walkable area by that "
    "radius</b>, so <b>a navigation mesh is specific to one agent "
    "size</b>. <b>Which is why engines build several</b> — one per "
    "size class — and <b>why a large enemy sometimes cannot follow "
    "you through a gap it visually appears to fit</b>: it is using a "
    "different, more eroded mesh."]),

  ("h1", "2 &nbsp; Any-angle paths"),
  ("code", """A* ON A GRID gives a path restricted to grid edges, so it
zigzags along 45-degree diagonals where a straight line was
available. It is OPTIMAL ON THE GRAPH and wrong for the
world -- because the graph was your approximation of the
world (Module 01 section 2).

THREE FIXES:

STRING PULLING / THE FUNNEL ALGORITHM
    take the polygon sequence from the navmesh search and
    pull the path taut within that corridor. O(n) in the
    corridor length and EXACT within the corridor. The
    standard answer for navigation meshes.

THETA* / LAZY THETA*
    during the search, allow a node's parent to be any
    ancestor with line of sight rather than only the
    immediately preceding node. Produces any-angle paths
    directly, at the cost of line-of-sight checks during
    search.

POST-HOC SMOOTHING
    repeatedly attempt to replace two consecutive segments
    with one, where line of sight permits. Simple, and it
    can cut corners the agent cannot physically take, so
    it needs a clearance check.

THE CAVEAT ON STRING PULLING: it is optimal WITHIN THE
CORRIDOR the search found, and that corridor need not
contain the globally optimal path -- because the search
optimised polygon-sequence cost, not Euclidean length.
Usually immaterial, occasionally visible."""),

  ("break",),
  ("h1", "3 &nbsp; Scaling to many agents and large levels"),
  ("ul", ["<b>Hierarchy.</b> Partition the level into clusters, "
          "precompute paths between cluster entrances, search the cluster "
          "graph, then refine within clusters. <b>HPA* reduces node "
          "counts by orders of magnitude for paths within a few percent "
          "of optimal</b> — Module 02 &sect;4's abstraction, with "
          "numbers.",
          "<b>Precomputation.</b> <b>All-pairs distances between cluster "
          "entrances, or a full flow field</b> where many agents share one "
          "destination — justified by Module 03 &sect;2's "
          "amortisation argument, since a level is searched thousands of "
          "times.",
          "<b>Flow fields.</b> <b>One Dijkstra outward from the goal "
          "labels every node with its direction-to-goal, and then every "
          "agent simply reads its cell</b>. <b>The cost is independent of "
          "the number of agents</b>, which is how real-time strategy games "
          "move hundreds of units to one destination. <b>The key insight "
          "is to invert the problem</b>: one search from the goal rather "
          "than one search per agent.",
          "<b>Time-slicing.</b> <b>Spread a single search across several "
          "frames</b>, budgeting a fixed number of node expansions per "
          "frame and returning the result when it completes. Requires the "
          "search state to be resumable, and requires the game to tolerate "
          "a few frames of latency — which it almost always "
          "does.",
          "<b>And caching.</b> Agents repeat queries constantly, "
          "especially to common destinations. <b>A cache keyed on "
          "(start polygon, goal polygon) pays immediately</b> and needs "
          "invalidation only when the mesh changes."]),
  ("callout", "Dynamic obstacles, and when to replan",
   ["<b>A door closes, a crate is pushed into a corridor, another agent "
    "stops in a doorway.</b> The path you computed three seconds ago is "
    "now invalid, and the agent does not know.",
    "<b>Full replanning every frame is unaffordable</b> at any realistic "
    "agent count, and <b>replanning only when a collision occurs is too "
    "late</b> — the agent is already pressed against the obstacle, "
    "which is exactly the visible failure.",
    "<b>D* Lite repairs the previous search result rather than redoing "
    "it</b>, at a cost proportional to how much of the world changed "
    "rather than to the level size. <b>The right tool for a "
    "mostly-static world with local changes</b>, which is what a game "
    "level is.",
    "<b>And local avoidance is a separate layer entirely.</b> <b>Agents "
    "avoid each other by steering, not by replanning</b> (Module 11 "
    "&sect;3), <b>because the path is a plan and avoidance is a "
    "reflex</b> — Module 01 &sect;1's agent ladder, with the "
    "cheapest design handling the fast-changing part and the expensive one "
    "handling the slow-changing part. <b>Getting that division wrong is "
    "the most common architectural error in game navigation.</b>"]),

  ("h1", "4 &nbsp; Path following, and debugging"),
  ("callout", "Pathfinding and path following are different problems",
   ["<b>Pathfinding answers 'which way'. Path following answers 'how to "
    "move along it'</b> — subject to acceleration limits, turn "
    "radius, animation state, foot placement, and the presence of other "
    "agents.",
    "<b>Conflating them means searching over a far larger state space</b> "
    "— position <i>and</i> velocity <i>and</i> heading, which is "
    "Module 02 &sect;1's state-choice decision made expensively "
    "— <b>for very little benefit in a game where characters can "
    "turn in place.</b>",
    "<b>So the standard architecture is three layers:</b> a global path "
    "from the navigation mesh (slow, replanned rarely), local steering "
    "along it (fast, every frame), and collision resolution underneath "
    "(every frame, geometric). <b>Each layer handles a different "
    "timescale, which is why the decomposition works.</b>",
    "<b>And when the vehicle's constraints genuinely matter</b> — a "
    "car, a tank with a minimum turn radius, a robot arm — <b>you "
    "need kinodynamic planning, which is a different and substantially "
    "harder problem</b> and is where &sect;1's RRT and probabilistic "
    "roadmaps belong. <b>Know which case you are in before choosing a "
    "method</b>, because the floor-walking case is far easier and the "
    "methods do not transfer."]),
  ("ul", ["<b>The agent walks into a wall.</b> <b>The navigation mesh "
          "does not match the collision geometry</b> — the mesh says "
          "walkable, physics says solid. <b>The most common bug in "
          "practice, and it is a content problem rather than a code "
          "problem</b>, usually caused by geometry edited after the mesh "
          "was baked.",
          "<b>The agent takes an obviously long way round.</b> A missing "
          "mesh connection (a jump link, a ladder), or an edge cost that "
          "does not reflect designer intent — both visible by "
          "rendering the mesh.",
          "<b>The agent oscillates between two paths.</b> <b>Replanning "
          "is flip-flopping between two near-equal options</b> as "
          "conditions change slightly. <b>Add hysteresis</b>: require the "
          "new path to be better by a margin before switching.",
          "<b>Agents bunch up at a doorway.</b> They all share one "
          "optimal path and local avoidance is fighting the path. "
          "<b>This is Module 11 &sect;3's problem</b>, and the fixes "
          "are path variation, queueing behaviour, or a crowd model rather "
          "than a pathfinding change.",
          "<b>Frame-time spikes.</b> An unbounded search ran to "
          "completion inside one frame. <b>Cap expansions per frame, and "
          "measure the 99th percentile rather than the mean</b> "
          "— CSCE 678 Module 06's lesson, which is what a frame "
          "budget actually requires.",
          "<b>Render the navigation mesh and the computed path inside the "
          "running game.</b> <b>Almost every pathfinding bug is "
          "immediately visible this way and effectively invisible "
          "otherwise</b> — the same 'look at the frame rather than "
          "the numbers' discipline as CSCE 647 and CSCE 753 "
          "Module 05."]),
 ],
 "resources": [
   ("Recast & Detour (free, open source)",
    "https://recastnav.com/",
    "<b>The navigation mesh builder of &sect;1</b>, used in many shipped "
    "games. Readable, and worth reading for the voxelisation pipeline."),
   ("Botea, Müller & Schaeffer &mdash; Near Optimal Hierarchical "
    "Path-Finding (HPA*) (free)",
    "https://web.archive.org/web/20250526142416/http://webdocs.cs.ualberta.ca/~mmueller/ps/hpastar.pdf",
    "<b>The &sect;3 hierarchy</b>, with the node-count reductions "
    "measured."),
   ("Koenig & Likhachev &mdash; D* Lite (free)",
    "http://idm-lab.org/bib/abstracts/papers/aaai02b.pdf",
    "<b>The &sect;3 replanning method</b>, and notably simpler than the "
    "original D*."),
   ("Red Blob Games &mdash; A* and pathfinding articles (free, "
    "interactive)",
    "https://www.redblobgames.com/pathfinding/",
    "<b>The best practical treatment of this module available</b>, "
    "including grids, navmeshes, smoothing, and flow fields, all "
    "interactive."),
 ],
 "exercises": [
   "<b>Implement grid A* and render the path</b> in a level. Observe the "
   "zigzag.",
   "<b>Implement the funnel algorithm</b> on a navigation mesh corridor "
   "and compare path lengths.",
   "<b>Implement Theta*</b> and compare its paths and node counts against "
   "smoothed A*.",
   "<b>Build a navigation mesh</b> for a level, by hand or with Recast, "
   "and report the node count against the grid's.",
   "<b>Implement HPA*</b> and report nodes expanded and path suboptimality "
   "against plain A*.",
   "<b>Implement a flow field</b> and move 500 agents to one goal. Report "
   "the cost against 500 individual searches.",
   "<b>Time-slice a search</b> across frames with a fixed expansion budget "
   "and verify the frame time stays bounded.",
   "<b>Close a door mid-path</b> and compare full replanning against D* "
   "Lite in node counts.",
   "<b>Create the oscillation bug deliberately</b> and fix it with "
   "hysteresis.",
   "<b>Measure p50 and p99 pathfinding time</b> with 100 agents and "
   "report both.",
 ],
 "selfcheck": [
   "Compare five spatial representations and say why navmeshes won.",
   "Why is convexity the essential property of a navmesh polygon?",
   "How is a navmesh built, and why is it per-agent-size?",
   "Why does grid A* zigzag, and what are three fixes?",
   "What is the caveat on string pulling?",
   "Name five scaling techniques and what each exploits.",
   "Why are flow fields the answer for crowds?",
   "When should you replan, and what does D* Lite do?",
   "Why separate pathfinding from path following?",
   "Give five pathfinding bugs and the cause of each.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Adversarial Search",
 "subtitle": "Searching when someone else chooses too.",
 "question": "How do you plan against an opponent who is planning "
             "against you?",
 "outcomes": [
     "Explain minimax and its assumptions.",
     "Explain alpha-beta pruning and why move ordering decides its "
     "value.",
     "Explain evaluation functions and the horizon effect.",
     "Explain Monte Carlo tree search and when it beats minimax.",
     "Choose between the two for a given game.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Minimax",
   "blurb": "Assume the opponent plays best."},

  {"t": "callout", "title": "Minimax assumes a perfect opponent, and that assumption is a choice",
   "kind": "What it means",
   "body": ["<b>At your nodes take the maximum; at the opponent's take "
            "the minimum.</b> The value of a position is what you can "
            "guarantee against best play.",
            "<b>This is the right assumption against a strong "
            "opponent</b> and a conservative one against a weak "
            "one — <b>minimax will not set a trap that only works "
            "if the opponent errs.</b>",
            "<b>Which is why game AI frequently does not want "
            "minimax:</b> a game opponent should be <i>beatable and "
            "interesting</i>, not optimal, and minimax gives neither "
            "knob.",
            "<b>Cost is O(bᵈ) and the full tree is almost never "
            "searchable</b> — chess has roughly 10⁴⁰ reachable "
            "positions — so you search to a depth and evaluate "
            "(Part 3)."]},

  {"t": "code", "kicker": "Alpha-beta", "title": "Pruning, and why move ordering is everything",
   "lang": "text", "code": """
  alpha = the best value MAX can already guarantee
  beta  = the best value MIN can already guarantee

  While searching a MIN node, if its value drops to or below
  alpha, MAX will never choose this branch -- so STOP. The
  remaining children cannot change the decision.

  Symmetrically for MAX nodes against beta.

  THE RESULT IS EXACT. Alpha-beta returns the SAME value as
  full minimax. It only skips nodes that cannot affect it.

  THE SPEEDUP DEPENDS ENTIRELY ON MOVE ORDERING:
      worst ordering  -> O(b^d).     No saving at all.
      random ordering -> O(b^(3d/4))
      BEST ordering   -> O(b^(d/2))  Twice the depth for
                                     the same cost.

  SO THE ENGINEERING IS IN THE ORDERING, not the pruning:
      try the previous iteration's best move first
          (iterative deepening gives you this free)
      killer moves -- those that pruned elsewhere
      captures and threats before quiet moves
      a transposition table, which also catches repeated
          positions reached by different move orders

  A chess engine's strength is mostly ordering and
  evaluation. The search algorithm is thirty lines.
""",
   "caption": "<b>Doubling the searchable depth for the same cost is the "
              "single largest result in game-tree search</b>, and it is "
              "entirely contingent on ordering.",
   "note": "That the algorithm is trivial and the engineering is "
           "elsewhere is the useful lesson."},

  {"t": "section", "label": "Part 2", "title": "Evaluating",
   "blurb": "You cannot search to the end, so you guess."},

  {"t": "callout", "title": "The evaluation function and the horizon effect",
   "kind": "Where depth-limited search goes wrong",
   "body": ["<b>Search to depth d, then score the position with a "
            "heuristic evaluation</b> — material, position, mobility, "
            "king safety.",
            "<b>The horizon effect:</b> <b>a bad event just beyond the "
            "search depth is invisible</b>, so the agent makes pointless "
            "delaying moves that push it past the horizon and "
            "'disappear'.",
            "<b>Quiescence search is the fix:</b> extend the search "
            "beyond the depth limit while the position is volatile "
            "— captures pending, checks outstanding — <b>and "
            "only evaluate quiet positions.</b>",
            "<b>Because evaluating mid-exchange is meaningless:</b> you "
            "are up a queen because the recapture is one ply past your "
            "limit. <b>Quiescence is not optional in any real "
            "engine.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Monte Carlo tree search",
   "blurb": "No evaluation function needed."},

  {"t": "code", "kicker": "MCTS", "title": "Four steps, repeated until time runs out",
   "lang": "text", "code": """
  repeat until the time budget is exhausted:
      SELECT   descend the tree, at each node choosing by
                   UCB1 = mean_value + c * sqrt(ln(N)/n)
               -- which balances exploiting good moves
                  against exploring under-sampled ones
      EXPAND   add one new child
      SIMULATE play to the end (randomly, or with a policy)
      BACKUP   propagate the result up the path

  then play the most-visited child.

  WHY THIS IS DIFFERENT FROM MINIMAX
    NO EVALUATION FUNCTION NEEDED -- the simulation's
        outcome is the evaluation. Decisive for games where
        nobody knows how to evaluate a position (Go).
    ANYTIME -- stop whenever; the answer degrades smoothly.
        Exactly right for a frame budget (Module 04).
    ASYMMETRIC -- it deepens promising lines and ignores
        bad ones, rather than searching uniformly.
    HANDLES HIGH BRANCHING -- it samples rather than
        enumerating, so b = 250 is survivable.

  AND IT IS WEAKER where a good evaluation exists and
  tactics are sharp: random playouts miss forced sequences
  that alpha-beta finds exactly. Chess engines are still
  alpha-beta.
""",
   "caption": "<b>UCB1 is the explore-exploit trade from the bandit "
              "literature</b>, and it reappears in CSCE 642 "
              "§2 — the same formula, the same purpose.",
   "note": "The honest 'chess engines are still alpha-beta' point "
           "prevents overgeneralising from AlphaGo."},

  {"t": "table", "kicker": "Choosing", "title": "Minimax against MCTS",
   "header": ["Choose minimax when", "Choose MCTS when"],
   "widths": [5.5, 5.5],
   "rows": [
     ["<b>A good evaluation function exists</b>", "<b>Nobody knows how to evaluate a position</b>"],
     ["<b>Branching factor is modest (chess ~35)</b>", "<b>Branching factor is large (Go ~250)</b>"],
     ["<b>Tactics are sharp and forced lines matter</b>", "<b>Position is strategic and gradual</b>"],
     ["<b>You can search to a fixed depth in budget</b>", "<b>You need an anytime answer</b>"],
     ["Deterministic and fully observable", "<b>Stochastic — simulate the randomness</b>"],
   ],
   "footnote": "<b>And modern strong play is both:</b> AlphaZero is MCTS "
               "with a learned evaluation and a learned prior, which "
               "removes MCTS's weakness by supplying what it lacked.",
   "note": "The synthesis is the right place to end."},

  {"t": "section", "label": "Part 4", "title": "In a game",
   "blurb": "What a player actually wants."},

  {"t": "callout", "title": "An optimal opponent is usually the wrong product",
   "kind": "The design point",
   "body": ["<b>Players want an opponent that is challenging, "
            "readable, and beatable</b> — not one that is "
            "optimal.",
            "<b>So difficulty is tuned by handicapping the search "
            "deliberately:</b> shallower depth, a noisier evaluation, "
            "an occasional deliberate error, or a restricted move set.",
            "<b>Add noise to the evaluation rather than to the move "
            "choice.</b> <b>A noisy evaluation makes plausible "
            "mistakes; a random move choice makes absurd ones</b>, and "
            "players notice the difference immediately.",
            "<b>And make the agent's reasoning legible.</b> <b>An "
            "opponent whose plan the player can infer is more "
            "satisfying than a stronger opaque one</b> — which is a "
            "design constraint on the algorithm, not an afterthought."]},
 ],
 "takeaways": [
   "Minimax assumes a perfect opponent, which is conservative and gives no "
   "knob for difficulty — so game AI frequently does not want it.",
   "Alpha-beta returns exactly the minimax value and its speedup depends "
   "entirely on move ordering, from no saving to double the depth.",
   "A chess engine's strength is mostly move ordering and evaluation; the "
   "search algorithm is thirty lines.",
   "The horizon effect makes an agent push bad news past its search depth, "
   "and quiescence search is the non-optional fix.",
   "MCTS needs no evaluation function, is anytime, searches "
   "asymmetrically, and tolerates high branching — and misses sharp "
   "tactics.",
   "Add noise to the evaluation rather than to the move choice: a noisy "
   "evaluation makes plausible mistakes and a random choice makes absurd "
   "ones.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Minimax and alpha-beta"),
  ("callout", "Minimax assumes a perfect opponent, and that assumption is a "
              "choice",
   ["<b>At your own nodes take the maximum over children; at the "
    "opponent's take the minimum.</b> The resulting value is what you can "
    "guarantee against best play, which is a meaningful and "
    "well-defined thing to compute.",
    "<b>This is the right assumption against a strong opponent and a "
    "conservative one against a weak one.</b> <b>Minimax will never set "
    "a trap that only works if the opponent blunders</b>, because it "
    "assumes they will not — which makes it play solidly and "
    "unimaginatively against weak players.",
    "<b>Which is exactly why game AI frequently does not want "
    "minimax.</b> <b>A game opponent should be beatable and "
    "interesting, not optimal</b>, and minimax provides no knob for "
    "either (&sect;4).",
    "<b>The cost is O(b<super>d</super>) and the complete tree is almost "
    "never searchable</b> — chess has on the order of "
    "10<super>40</super> reachable positions — <b>so in practice you "
    "search to a fixed depth and apply a heuristic evaluation "
    "there</b> (&sect;2), which is where the method's real difficulties "
    "live."]),
  ("code", """alpha = the best value MAX can already guarantee
beta  = the best value MIN can already guarantee

While searching a MIN node, if its value drops to or below
alpha, MAX will never choose this branch -- so STOP. The
remaining children cannot change the decision above.

Symmetrically for MAX nodes against beta.

THE RESULT IS EXACT. Alpha-beta returns the SAME value as
full minimax; it only skips nodes that provably cannot
affect it. This is not an approximation.

THE SPEEDUP DEPENDS ENTIRELY ON MOVE ORDERING:
    worst ordering  -> O(b^d)      no saving whatsoever
    random ordering -> O(b^(3d/4))
    BEST ordering   -> O(b^(d/2))  TWICE THE DEPTH for the
                                   same node count

SO THE ENGINEERING IS IN THE ORDERING, not the pruning:
    try the previous iteration's best move first --
        iterative deepening (Module 02) hands you this
        for free, which is why engines use it
    killer moves: moves that caused a cutoff elsewhere at
        the same depth
    captures and threats before quiet moves
    a transposition table, which also catches positions
        reached by different move orders -- the explored
        set of Module 02, in a game tree

A chess engine's strength is mostly move ordering and
evaluation. The search algorithm itself is thirty lines."""),
  ("p", "<b>Doubling the searchable depth for the same node count is the "
        "single largest result in game-tree search</b>, and <b>it is "
        "entirely contingent on ordering</b> — which is why so much "
        "engine engineering goes into move ordering heuristics that look, "
        "from outside, like minor details. <b>The lesson generalises: the "
        "algorithm with the famous name is often the easy part.</b>"),

  ("h1", "2 &nbsp; Evaluation and the horizon"),
  ("callout", "The evaluation function and the horizon effect",
   ["<b>Search to depth d, then score the resulting position with a "
    "heuristic evaluation</b> — material balance, piece placement, "
    "mobility, pawn structure, king safety. The quality of this function "
    "is most of the engine's strength.",
    "<b>The horizon effect:</b> <b>a bad event just beyond the search "
    "depth is invisible to the search</b>, so the agent makes pointless "
    "delaying moves that push the event one ply further out, at which "
    "point it vanishes from view entirely. <b>The agent has not avoided "
    "the loss; it has avoided seeing it</b>, and it has spent material "
    "doing so.",
    "<b>Quiescence search is the fix:</b> <b>extend the search beyond "
    "the nominal depth limit while the position remains volatile</b> "
    "— captures available, checks outstanding, promotions pending "
    "— <b>and evaluate only quiet positions.</b>",
    "<b>Because evaluating a position mid-exchange is meaningless:</b> "
    "you appear to be a queen ahead because the recapture happens to lie "
    "one ply past your limit. <b>Quiescence search is not optional in any "
    "real engine</b>, and an engine without it plays recognisably badly in "
    "a specific way — which is a good illustration that the headline "
    "algorithm's correctness does not imply the system's."]),

  ("break",),
  ("h1", "3 &nbsp; Monte Carlo tree search"),
  ("code", """repeat until the time budget is exhausted:
    SELECT    descend the existing tree, at each node
              choosing the child maximising
                  UCB1 = mean_value + c*sqrt(ln(N)/n)
              which balances EXPLOITING children with good
              observed value against EXPLORING ones with
              few samples
    EXPAND    add one new child beyond the tree
    SIMULATE  play to the end of the game, randomly or
              with a cheap policy
    BACKUP    propagate the outcome up the visited path

then play the most-visited child.

WHY THIS DIFFERS FROM MINIMAX
  NO EVALUATION FUNCTION IS NEEDED -- the simulation's
      outcome IS the evaluation. Decisive for games where
      nobody knows how to evaluate a position, which was
      the situation in Go for forty years.
  ANYTIME -- stop at any moment; the answer degrades
      smoothly rather than being unavailable. Exactly the
      right shape for a frame budget (Module 04 section 3).
  ASYMMETRIC -- it deepens promising lines and ignores bad
      ones, rather than searching to uniform depth.
  TOLERATES HIGH BRANCHING -- it samples rather than
      enumerating, so b = 250 is survivable where
      alpha-beta is not.

AND IT IS WEAKER where a good evaluation exists and tactics
are sharp: random playouts miss forced sequences that
alpha-beta finds exactly. Top chess engines remain
alpha-beta based for this reason."""),
  ("p", "<b>UCB1 is the explore-exploit trade from the multi-armed bandit "
        "literature</b>, and <b>it reappears in CSCE 642 &sect;2 as "
        "the same formula for the same purpose</b> — which is worth "
        "noticing, because it means the exploration problem in "
        "reinforcement learning and the selection problem in game-tree "
        "search are literally the same problem with different payoffs."),
  ("table", ["Choose minimax with alpha-beta when", "Choose MCTS when"],
   [["<b>A good evaluation function exists and is cheap.</b>",
     "<b>Nobody knows how to evaluate a position reliably.</b>"],
    ["<b>The branching factor is modest — chess is about 35.</b>",
     "<b>The branching factor is large — Go is about 250.</b>"],
    ["<b>Tactics are sharp and forced sequences decide games.</b>",
     "<b>The position is strategic and advantages accumulate "
     "gradually.</b>"],
    ["<b>You can search to a useful fixed depth within budget.</b>",
     "<b>You need an anytime answer under an external deadline.</b>"],
    ["The game is deterministic and fully observable.",
     "<b>The game is stochastic — simulate the randomness "
     "directly</b>, which minimax handles only awkwardly."]],
   [0.50, 0.50]),
  ("p", "<b>And modern strong play is both.</b> <b>AlphaZero is MCTS "
        "with a learned evaluation function and a learned move prior</b> "
        "— which <b>removes MCTS's central weakness by supplying "
        "exactly what it lacked</b>: the prior guides selection away from "
        "nonsense moves, and the learned evaluation replaces the random "
        "playout. <b>The synthesis is the right place to leave this</b>, "
        "and it is also a good example of a learned component slotting "
        "into a classical algorithm rather than replacing it "
        "(CSCE 753 Module 03 &sect;4's pattern)."),

  ("h1", "4 &nbsp; Adversarial search in a game"),
  ("callout", "An optimal opponent is usually the wrong product",
   ["<b>Players want an opponent that is challenging, readable, and "
    "beatable</b> — not one that is optimal. <b>An unbeatable "
    "opponent is a solved design problem and a failed product.</b>",
    "<b>So difficulty is tuned by handicapping the search "
    "deliberately:</b> a shallower depth limit, a noisier evaluation "
    "function, an occasional deliberate suboptimal choice, or a "
    "restricted set of available tactics at lower difficulties.",
    "<b>Add the noise to the evaluation rather than to the move "
    "choice.</b> <b>A noisy evaluation function makes <i>plausible</i> "
    "mistakes — it misjudges a position the way a weaker player "
    "would — while a randomly perturbed move choice makes absurd "
    "ones</b>, and <b>players notice the difference immediately and "
    "describe the second as broken rather than as easy</b>. This is one of "
    "the most useful pieces of practical knowledge in game AI.",
    "<b>And make the agent's reasoning legible.</b> <b>An opponent whose "
    "plan the player can infer and counter is more satisfying than a "
    "stronger opaque one</b> — which means <b>legibility is a design "
    "constraint on the algorithm rather than an afterthought</b>, and it "
    "is another reason game AI favours the methods of this course "
    "(Module 01 &sect;4's debuggability argument, from the player's "
    "side rather than the developer's)."]),
 ],
 "resources": [
   ("Russell & Norvig &mdash; AIMA, chapter 5 (pseudocode free)",
    "https://aima.cs.berkeley.edu/",
    "<b>Minimax, alpha-beta, and the ordering results of &sect;1</b>, "
    "with the complexity derivations."),
   ("Chess Programming Wiki (free)",
    "https://www.chessprogramming.org/",
    "<b>The practical reference for &sect;1 and &sect;2</b> — move "
    "ordering, transposition tables, and quiescence search, written by "
    "engine authors."),
   ("Browne et al. &mdash; A Survey of Monte Carlo Tree Search Methods "
    "(free)",
    "https://ieeexplore.ieee.org/document/6145622",
    "<b>The &sect;3 reference</b>, with UCB1 derived and the variants "
    "catalogued."),
   ("Silver et al. &mdash; Mastering the Game of Go without Human "
    "Knowledge (free)",
    "https://www.nature.com/articles/nature24270",
    "<b>The synthesis of &sect;3's table footnote</b> — MCTS with "
    "learned evaluation and prior."),
 ],
 "exercises": [
   "<b>Implement minimax</b> for a small game and verify the value "
   "against exhaustive search.",
   "<b>Add alpha-beta</b> and confirm the value is unchanged while the "
   "node count drops.",
   "<b>Measure nodes expanded under worst, random, and best move "
   "ordering</b> and compare against the predicted exponents.",
   "<b>Add iterative deepening with a best-move-first ordering</b> and "
   "report the improvement.",
   "<b>Add a transposition table</b> and report the hit rate.",
   "<b>Construct a horizon-effect position</b> and show your engine "
   "making a delaying move.",
   "<b>Add quiescence search</b> and confirm the behaviour changes.",
   "<b>Implement MCTS</b> for the same game and compare against "
   "alpha-beta at equal time budgets.",
   "<b>Vary the UCB1 exploration constant</b> and plot playing strength "
   "against it.",
   "<b>Build three difficulty levels</b> — by depth, by evaluation "
   "noise, and by random move choice — and have someone play all "
   "three without being told which is which. Report what they said.",
 ],
 "selfcheck": [
   "What does minimax assume, and why is that sometimes wrong for a "
   "game?",
   "Explain alpha-beta and state that its result is exact.",
   "Give the three ordering complexities and what follows from them.",
   "Name four move-ordering techniques.",
   "What is the horizon effect, and what fixes it?",
   "Why is evaluating a mid-exchange position meaningless?",
   "Give MCTS's four steps and what UCB1 balances.",
   "Give four MCTS advantages and its main weakness.",
   "Compare minimax and MCTS on five axes.",
   "Why add noise to the evaluation rather than the move choice?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Constraint Satisfaction",
 "subtitle": "Search that knows about the problem's structure.",
 "question": "What if you could prune before searching rather than "
             "while?",
 "outcomes": [
     "Formulate a problem as a constraint satisfaction problem.",
     "Explain constraint propagation and arc consistency.",
     "Apply the standard variable and value ordering heuristics.",
     "Exploit problem structure, including tree decomposition.",
     "Apply constraint methods to procedural content generation.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The formulation",
   "blurb": "Variables, domains, constraints — and why the "
            "structure helps."},

  {"t": "callout", "title": "A CSP exposes structure that a generic search hides",
   "kind": "Why bother with a special formulation",
   "body": ["<b>Variables, each with a domain of possible values, and "
            "constraints restricting combinations.</b> A solution assigns "
            "every variable consistently.",
            "<b>A generic search sees only states and successors</b> "
            "(Module 02) <b>and cannot know that this state fails because "
            "of these two variables.</b>",
            "<b>A CSP solver can.</b> <b>So it prunes whole regions of "
            "the space from a single violated constraint</b>, and it can "
            "do so <i>before</i> search as well as during.",
            "<b>And the goal is uniform:</b> every variable assigned, "
            "every constraint satisfied — so <b>the solver can be "
            "entirely generic and still exploit your problem's "
            "structure.</b>"]},

  {"t": "table", "kicker": "Examples", "title": "What is a CSP",
   "header": ["Problem", "Variables", "Constraints"],
   "widths": [2.7, 3.9, 5.4],
   "rows": [
     ["<b>Sudoku</b>", "<b>81 cells, domain 1–9</b>", "<b>All-different per row, column, box</b>"],
     ["<b>Map colouring</b>", "Regions", "<b>Adjacent regions differ</b>"],
     ["<b>Timetabling</b>", "<b>Each class: time and room</b>", "<b>No clashes; capacity; availability</b>"],
     ["<b>Level layout</b>", "<b>Each tile: which piece</b>", "<b>Edges must match neighbours</b>"],
     ["<b>Puzzle generation</b>", "<b>Which clues to give</b>", "<b>Exactly one solution exists</b>"],
   ],
   "footnote": "<b>The last two are procedural content generation</b>, "
               "and they are the reason this module is in a "
               "game-engines track — Wave Function Collapse is a "
               "CSP solver.",
   "note": "The WFC connection makes this module immediately relevant to "
           "the track."},

  {"t": "section", "label": "Part 2", "title": "Propagation",
   "blurb": "Inferring before searching."},

  {"t": "code", "kicker": "Consistency", "title": "Three levels of inference",
   "lang": "text", "code": """
  NODE CONSISTENCY   remove values violating a unary
                     constraint. Trivial, do it once.

  ARC CONSISTENCY    for every constraint between X and Y,
                     remove any value of X with no
                     supporting value in Y. Repeat until
                     nothing changes -- removals cascade.
                     This is AC-3, O(ed^3), and it is the
                     workhorse.

  PATH / k-CONSISTENCY  stronger, more expensive, rarely
                     worth it in full.

  WHAT AC-3 BUYS: on Sudoku, arc consistency alone solves
  easy puzzles with NO SEARCH AT ALL, and reduces hard ones
  enormously. The pencil-marks technique humans use IS arc
  consistency.

  MAINTAINING ARC CONSISTENCY DURING SEARCH (MAC) is the
  standard: assign a variable, propagate, and if any domain
  empties, BACKTRACK IMMEDIATELY -- before exploring the
  subtree at all.

  GLOBAL CONSTRAINTS matter enormously. "All-different over
  n variables" expressed as n(n-1)/2 pairwise constraints
  propagates weakly; a dedicated all-different propagator
  using bipartite matching (CSCE 669 Module 11) prunes far
  more. USE THE GLOBAL CONSTRAINT WHEN ONE EXISTS.
""",
   "caption": "<b>The global-constraint point is the most practically "
              "valuable thing here</b> — the same logical condition "
              "expressed two ways prunes completely differently.",
   "note": "The pencil-marks observation makes arc consistency "
           "immediately intuitive."},

  {"t": "section", "label": "Part 3", "title": "Ordering",
   "blurb": "Which variable next, and which value first."},

  {"t": "bullets", "kicker": "Heuristics", "title": "The orderings that matter",
   "items": [
     "<b>Minimum remaining values</b> (most constrained variable). "
     "<b>Assign the variable with the smallest domain</b> — fail "
     "fast, high in the tree, where failing is cheap.",
     "",
     "<b>Degree heuristic</b> as a tie-break: prefer the variable "
     "involved in the most constraints on unassigned variables.",
     "",
     "<b>Least constraining value.</b> <b>Try the value that rules out "
     "fewest options for the neighbours</b> — because you want to "
     "<i>succeed</i> on values and <i>fail</i> on variables.",
     "",
     "<b>That asymmetry is the thing to remember:</b> fail fast on "
     "variables, succeed fast on values. <b>They point in opposite "
     "directions for a reason.</b>",
     "",
     "<b>And conflict-directed backjumping</b> — jump back to the "
     "variable that actually caused the failure, not the previous one.",
   ],
   "footnote": "<b>These heuristics routinely change solve times by "
               "orders of magnitude</b> and cost nothing — which "
               "makes them the best value in the module."},

  {"t": "callout", "title": "Structure decides tractability",
   "kind": "The theoretical result worth knowing",
   "body": ["<b>If the constraint graph is a tree, the CSP is solvable "
            "in O(nd²)</b> — polynomial, by a single sweep. No "
            "search at all.",
            "<b>So look for tree structure, or create it.</b> <b>Cutset "
            "conditioning</b> assigns a small set of variables to break "
            "cycles, then solves the remaining tree.",
            "<b>Tree decomposition</b> generalises this: the cost is "
            "exponential in the <i>treewidth</i> rather than in the "
            "number of variables.",
            "<b>Which means a problem with a thousand variables and "
            "treewidth 4 is easy</b>, and one with twenty variables and "
            "treewidth 19 is not. <b>Measure the structure, not the "
            "size.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Content generation",
   "blurb": "Constraints as an authoring tool."},

  {"t": "callout", "title": "Wave Function Collapse is a CSP solver with a tileset",
   "kind": "The track payoff",
   "body": ["<b>Variables are tile positions; domains are the tile "
            "set; constraints are the adjacency rules</b> — which "
            "edges may meet which.",
            "<b>The algorithm is minimum-remaining-values selection, a "
            "weighted random value choice, then arc "
            "consistency</b> — exactly Parts 2 and 3, with "
            "randomness added to get variety instead of one answer.",
            "<b>So the designer authors <i>constraints</i> rather than "
            "content</b>, and the solver produces unlimited valid "
            "content. <b>That is the actual appeal.</b>",
            "<b>And the failure mode is contradiction</b> — a "
            "position with an empty domain. <b>Backtrack, or restart, "
            "or design the tileset so it cannot happen</b>; the third is "
            "what shipping projects do."]},

  {"t": "bullets", "kicker": "Practice", "title": "Using constraints for generation",
   "items": [
     "<b>Guarantee playability as a constraint</b>, not as a "
     "post-hoc check — 'a path exists from entrance to exit' can "
     "be a constraint.",
     "",
     "<b>Author variety with weights</b> on value choice, so common "
     "tiles are common without being mandatory.",
     "",
     "<b>Expect contradictions</b> and decide the policy in advance: "
     "backtrack, restart the region, or relax a soft constraint.",
     "",
     "<b>And use a real solver for hard instances.</b> <b>MiniZinc or "
     "OR-Tools CP-SAT will dispatch problems your hand-rolled "
     "backtracker cannot</b> (CSCE 669 M13).",
     "",
     "<b>Then verify the output</b>, because a constraint you forgot "
     "to write is not a constraint.",
   ],
   "footnote": "<b>'A path exists' as a constraint rather than a filter "
               "is the single most useful trick here</b> — it "
               "eliminates the generate-and-reject loop entirely."},
 ],
 "takeaways": [
   "A CSP formulation exposes structure a generic search cannot see, so a "
   "single violated constraint prunes whole regions.",
   "Arc consistency is the pencil-marks technique humans use on Sudoku, "
   "and maintaining it during search is the standard approach.",
   "A global constraint such as all-different prunes far more than the "
   "equivalent pairwise constraints — use it when one exists.",
   "Fail fast on variables (minimum remaining values) and succeed fast on "
   "values (least constraining) — the asymmetry is deliberate.",
   "Cost is exponential in treewidth, not in variable count, so a thousand "
   "variables with treewidth 4 is easy.",
   "Wave Function Collapse is a CSP solver with a tileset, so the designer "
   "authors constraints rather than content.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The formulation"),
  ("callout", "A CSP exposes structure that a generic search hides",
   ["<b>Variables, each with a domain of possible values, and constraints "
    "restricting which combinations are allowed.</b> A solution is an "
    "assignment of every variable such that every constraint holds.",
    "<b>A generic search sees only opaque states and a successor "
    "function</b> (Module 02 &sect;1), <b>so it cannot know that the "
    "current state is doomed because of a conflict between two specific "
    "variables</b>. It discovers the failure only by exploring the "
    "subtree.",
    "<b>A CSP solver can see exactly that.</b> <b>So it prunes whole "
    "regions of the space from one violated constraint</b>, and crucially "
    "<b>it can do so <i>before</i> search begins as well as during "
    "it</b> (&sect;2) — which is the structural advantage over "
    "Module 02's black-box formulation.",
    "<b>And the goal is uniform across every CSP:</b> every variable "
    "assigned, every constraint satisfied. <b>So the solver can be "
    "entirely generic and still exploit your problem's particular "
    "structure</b>, which is why industrial constraint solvers exist as "
    "general tools — unlike Module 02's searches, which must be "
    "written per problem."]),
  ("table", ["Problem", "Variables", "Constraints"],
   [["<b>Sudoku</b>", "<b>81 cells, each with domain 1–9.</b>",
     "<b>All-different within each row, column, and 3&times;3 box.</b>"],
    ["<b>Map colouring</b>", "One per region, domain the colours.",
     "<b>Adjacent regions take different colours.</b>"],
    ["<b>Timetabling</b>",
     "<b>For each class, a time slot and a room.</b>",
     "<b>No two classes share a room and time; room capacity suffices; "
     "staff availability respected.</b> The canonical industrial "
     "application."],
    ["<b>Level layout generation</b>",
     "<b>For each tile position, which tile piece goes there.</b>",
     "<b>Adjacent tiles' edges must match.</b> See &sect;4."],
    ["<b>Puzzle generation</b>",
     "<b>Which clues to include in a generated puzzle.</b>",
     "<b>Exactly one solution exists</b> — a constraint on the "
     "number of solutions, which is a genuinely useful and unusual "
     "thing to be able to express."]],
   [0.20, 0.33, 0.47]),
  ("p", "<b>The last two rows are procedural content generation</b>, and "
        "they are why this module belongs in a game-engines track "
        "— <b>Wave Function Collapse, which generates a great deal "
        "of modern procedural level content, is a CSP solver</b> "
        "(&sect;4)."),

  ("h1", "2 &nbsp; Constraint propagation"),
  ("code", """NODE CONSISTENCY    remove values violating a unary
                    constraint. Trivial; do it once at the
                    start.

ARC CONSISTENCY     for each constraint between X and Y,
                    remove any value of X that has no
                    supporting value in Y's domain. Repeat
                    until nothing changes, because removals
                    CASCADE -- shrinking X's domain may
                    make a value of Z unsupported.
                    This is AC-3, O(e d^3), and it is the
                    workhorse of constraint solving.

PATH / k-CONSISTENCY  stronger inference, substantially
                    more expensive, rarely worth computing
                    in full.

WHAT AC-3 BUYS: on Sudoku, arc consistency alone solves
easy puzzles with NO SEARCH AT ALL and reduces hard ones
enormously. The pencil-marks technique human solvers use
IS arc consistency, applied by hand.

MAINTAINING ARC CONSISTENCY DURING SEARCH (MAC) is the
standard approach: assign a variable, propagate the
consequences, and if any domain becomes empty, BACKTRACK
IMMEDIATELY -- before exploring that subtree at all.

GLOBAL CONSTRAINTS MATTER ENORMOUSLY. "All-different over
n variables" expressed as n(n-1)/2 pairwise inequalities
propagates weakly: three variables each with domain {1,2}
violates all-different but satisfies every pairwise
constraint individually until two are assigned. A dedicated
all-different propagator, using bipartite matching
(CSCE 669 Module 11 section 1), detects it immediately.
USE THE GLOBAL CONSTRAINT WHENEVER ONE EXISTS."""),
  ("p", "<b>The global-constraint point is the most practically valuable "
        "thing in this module.</b> <b>The same logical condition "
        "expressed two ways prunes completely differently</b>, which means "
        "<b>modelling choice determines performance here exactly as it did "
        "in CSCE 669 Module 09</b> — and the lesson is the same: "
        "the formulation is worth more than the solver."),

  ("break",),
  ("h1", "3 &nbsp; Ordering heuristics"),
  ("ul", ["<b>Minimum remaining values (the most constrained "
          "variable).</b> <b>Assign the variable with the smallest "
          "remaining domain next</b> — so that if the assignment is "
          "going to fail, it fails high in the tree where the subtree "
          "being discarded is small. <b>Fail fast, and fail cheaply.</b>",
          "<b>The degree heuristic</b> as a tie-break: among variables "
          "with equally small domains, prefer the one involved in the most "
          "constraints on still-unassigned variables, since assigning it "
          "propagates furthest.",
          "<b>Least constraining value.</b> <b>Among the values "
          "available for the chosen variable, try the one that rules out "
          "the fewest options for its neighbours</b> — because you "
          "want to <i>succeed</i> on values, since any single success "
          "takes you forward.",
          "<b>That asymmetry is the thing to remember.</b> <b>Fail fast "
          "on variables; succeed fast on values.</b> <b>The two "
          "heuristics point in opposite directions and both are "
          "correct</b>, because you must try every value of a variable "
          "(so finding the failing variable early is good) and you need "
          "only one value to work (so finding the succeeding value early "
          "is good).",
          "<b>And conflict-directed backjumping</b> — on failure, "
          "jump back to the variable that actually participated in the "
          "conflict rather than the chronologically previous one, skipping "
          "intermediate assignments that were irrelevant. <b>These "
          "heuristics routinely change solve times by orders of magnitude "
          "and cost essentially nothing</b>, which makes them the best "
          "value available here."]),
  ("callout", "Structure decides tractability",
   ["<b>If the constraint graph is a tree, the CSP is solvable in "
    "O(nd&#178;)</b> — polynomial, by a single sweep that makes each "
    "node consistent with its parent, followed by a forward assignment "
    "pass. <b>No search at all</b>, which is a striking result given that "
    "CSP is NP-complete in general.",
    "<b>So look for tree structure, or create it.</b> <b>Cutset "
    "conditioning</b> assigns values to a small set of variables chosen "
    "to break every cycle, then solves the remaining tree in polynomial "
    "time for each assignment of the cutset — so the cost is "
    "exponential only in the cutset size.",
    "<b>Tree decomposition generalises this properly:</b> the cost is "
    "exponential in the <i>treewidth</i> of the constraint graph rather "
    "than in the number of variables — treewidth being, informally, "
    "how far the graph is from being a tree.",
    "<b>Which means a problem with a thousand variables and treewidth 4 "
    "is easy, and one with twenty variables and treewidth 19 is "
    "not.</b> <b>So measure the structure, not the size</b> — and "
    "<b>it is the same lesson as CSCE 669 Module 11 &sect;4's "
    "checklist</b>: whether a problem is tractable is a property of its "
    "structure, which is frequently a property of how you formulated "
    "it."]),

  ("h1", "4 &nbsp; Constraints for content generation"),
  ("callout", "Wave Function Collapse is a CSP solver with a tileset",
   ["<b>The variables are tile positions in a grid; the domains are the "
    "available tile pieces; the constraints are the adjacency rules "
    "stating which tile edges may meet which.</b> That is the entire "
    "formulation.",
    "<b>The algorithm is minimum-remaining-values variable selection "
    "(&sect;3), a weighted random choice among that variable's remaining "
    "values, then arc consistency propagation (&sect;2).</b> <b>It is "
    "exactly this module's machinery with randomness added to the value "
    "choice</b> — because a generator wants <i>variety</i> rather "
    "than one canonical solution, which is the only substantive "
    "difference from a solver.",
    "<b>So the designer authors <i>constraints</i> rather than "
    "content</b>, and the solver produces unlimited valid content from "
    "them. <b>That is the actual appeal, and it is a real shift in "
    "authoring</b>: a tileset with adjacency rules is a compact "
    "specification of an infinite family of levels.",
    "<b>And the failure mode is contradiction</b> — propagation "
    "empties some position's domain, so no valid completion exists from "
    "the current partial assignment. <b>Backtrack, restart the affected "
    "region, or design the tileset so that contradictions cannot "
    "arise</b>; <b>the third is what shipping projects do</b>, because it "
    "converts a runtime risk into a one-time authoring constraint."]),
  ("ul", ["<b>Express playability as a constraint rather than as a "
          "post-hoc check.</b> <b>'A path exists from the entrance to the "
          "exit' can be a constraint</b> (through a reachability "
          "propagator or a flow formulation), <b>which eliminates the "
          "generate-and-reject loop entirely</b> — and that loop is "
          "where naive procedural generation spends most of its time. "
          "<b>The single most useful trick in this section.</b>",
          "<b>Author variety with weights</b> on the value choice, so "
          "that common tiles appear commonly without being mandatory and "
          "rare ones appear occasionally — which is how a generated "
          "level gets a texture rather than a uniform distribution.",
          "<b>Expect contradictions and decide the policy in "
          "advance:</b> backtrack (correct, potentially slow), restart "
          "the affected region (fast, and can loop), or relax a soft "
          "constraint (always terminates, may produce something "
          "undesirable). <b>Deciding this at design time rather than at "
          "3 a.m. is worth the ten minutes.</b>",
          "<b>And use a real solver for hard instances.</b> <b>MiniZinc "
          "or OR-Tools CP-SAT will dispatch problems a hand-rolled "
          "backtracker cannot</b> (CSCE 669 Module 13 &sect;1), and "
          "they implement every global constraint in &sect;2 properly.",
          "<b>Then verify the output against the properties you "
          "wanted</b>, because <b>a constraint you forgot to write is not "
          "a constraint</b> — and a generator will happily produce "
          "something technically valid and completely unplayable, which is "
          "CSCE 669 Module 12 &sect;4's warning about optimisers "
          "exploiting your model."]),
 ],
 "resources": [
   ("Russell & Norvig &mdash; AIMA, chapter 6 (pseudocode free)",
    "https://aima.cs.berkeley.edu/",
    "<b>The reference for &sect;1 through &sect;3</b>, including AC-3 and "
    "the tree-structured result of &sect;3."),
   ("Google OR-Tools &mdash; CP-SAT documentation (free)",
    "https://developers.google.com/optimization/cp",
    "<b>A production constraint solver</b>, with the global constraints of "
    "&sect;2 and worked examples of every problem in &sect;1's table."),
   ("Gumin &mdash; Wave Function Collapse (free, open source)",
    "https://github.com/mxgmn/WaveFunctionCollapse",
    "<b>The &sect;4 algorithm</b>, with the original implementation and a "
    "large gallery of results."),
   ("Short & Adams (eds.) &mdash; Procedural Generation in Game Design",
    "https://www.routledge.com/Procedural-Generation-in-Game-Design/Short-Adams/p/book/9781498799195",
    "<b>The &sect;4 design perspective</b>, by practitioners. Library "
    "copy; the free PCG Book at procedural-generation sites covers "
    "similar ground."),
 ],
 "exercises": [
   "<b>Formulate Sudoku as a CSP</b> and solve it with plain "
   "backtracking. Report node counts.",
   "<b>Add arc consistency</b> and report the reduction. Confirm easy "
   "puzzles need no search.",
   "<b>Express all-different pairwise and then as a global "
   "constraint</b>, and compare pruning on the same instance.",
   "<b>Add minimum remaining values</b> and report the improvement.",
   "<b>Add least constraining value</b> and report it separately.",
   "<b>Construct a tree-structured CSP</b> and solve it without search.",
   "<b>Compute the treewidth</b> of a constraint graph you built, "
   "approximately, and relate it to the solve time.",
   "<b>Implement Wave Function Collapse</b> for a small tileset and "
   "generate twenty levels.",
   "<b>Add a reachability constraint</b> and confirm every generated "
   "level is completable.",
   "<b>Deliberately design a contradictory tileset</b> and implement each "
   "of the three failure policies.",
 ],
 "selfcheck": [
   "What does a CSP formulation expose that a generic search cannot?",
   "Give five example CSPs with their variables and constraints.",
   "Define arc consistency and say what human technique it corresponds "
   "to.",
   "What is MAC, and why is it standard?",
   "Why does a global constraint prune better than equivalent pairwise "
   "ones?",
   "State the variable and value ordering heuristics and explain their "
   "asymmetry.",
   "What is the complexity of a tree-structured CSP, and what "
   "generalises it?",
   "Explain Wave Function Collapse as a CSP solver.",
   "Why express playability as a constraint rather than a filter?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Classical Planning",
 "subtitle": "Search where the actions are described, not enumerated.",
 "question": "What if the agent is told what actions do rather than "
             "which to take?",
 "outcomes": [
     "Write a planning domain in terms of preconditions and effects.",
     "Explain why a declarative action description enables automatic "
     "heuristics.",
     "Derive the delete-relaxation heuristics.",
     "Explain goal-oriented action planning and why games use it.",
     "State the limits of classical planning.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Declarative actions",
   "blurb": "Describing what an action does, not how to choose it."},

  {"t": "code", "kicker": "STRIPS", "title": "An action is preconditions plus effects",
   "lang": "text", "code": """
  STATE: a set of true facts.
      { At(Agent, Room1), Has(Key), Closed(Door12) }

  ACTION:
      Open(d, r1, r2)
          PRECOND: At(Agent,r1), Connects(d,r1,r2),
                   Closed(d), Has(Key)
          ADD:     Open(d)
          DELETE:  Closed(d)

  A PLAN is a sequence of actions from the initial state to
  a state satisfying the goal. This is still Module 02's
  search -- states, successors, goal test.

  THE DIFFERENCE IS THAT THE ACTIONS ARE DESCRIBED, NOT
  CODED. And that single change is what makes everything
  else possible:

      the planner can REASON ABOUT the actions
      it can compute which actions are RELEVANT to a goal
      it can detect that two actions are INDEPENDENT
      and it can DERIVE A HEURISTIC AUTOMATICALLY (Part 2)

  THAT LAST ONE IS THE PAYOFF. With a coded successor
  function you must invent a heuristic by hand (Module 03).
  With a declarative domain, the planner invents it for you
  -- from the action descriptions, with no domain knowledge.
""",
   "caption": "<b>Declarativeness buys automatic heuristics</b>, and "
              "that is why planning exists as a separate field rather "
              "than as an application of Module 02.",
   "note": "This is the single most important idea in the module."},

  {"t": "section", "label": "Part 2", "title": "Automatic heuristics",
   "blurb": "Module 03's relaxation, performed by the machine."},

  {"t": "callout", "title": "Ignore the delete lists, and the problem becomes easy",
   "kind": "The delete relaxation",
   "body": ["<b>Drop every action's delete list.</b> Facts can then "
            "only accumulate — nothing ever becomes false.",
            "<b>The relaxed problem is solvable in polynomial time</b> "
            "by forward chaining, and <b>its cost is an admissible "
            "heuristic for the original</b>, because any real plan is "
            "also a relaxed plan.",
            "<b>This is Module 03 §3's relaxation argument, "
            "applied automatically</b> — the planner derives it from "
            "the domain description with no human insight at all.",
            "<b>Three heuristics follow:</b> h_max (the most expensive "
            "subgoal — admissible, weak), h_add (the sum — "
            "inadmissible, stronger), and <b>h_FF (extract a relaxed "
            "plan and count it — the one that made planners "
            "work).</b>"]},

  {"t": "table", "kicker": "Heuristics", "title": "The relaxation heuristics compared",
   "header": ["Heuristic", "What it computes", "Property"],
   "widths": [2.4, 4.4, 5.2],
   "rows": [
     ["<b>h_max</b>", "<b>Cost of the most expensive subgoal</b>", "<b>Admissible, and weak</b>"],
     ["<b>h_add</b>", "<b>Sum of subgoal costs</b>", "<b>Inadmissible (double counts shared work), stronger</b>"],
     ["<b>h_FF</b>", "<b>Length of an extracted relaxed plan</b>", "<b>Inadmissible, strong, cheap. The practical winner</b>"],
     ["<b>Landmarks</b>", "<b>Facts every plan must achieve</b>", "<b>Admissible variants exist and are strong</b>"],
   ],
   "footnote": "<b>Modern planners mostly use inadmissible heuristics</b> "
               "with greedy best-first search, trading optimality for "
               "the ability to solve the problem at all.",
   "note": "The honest admission that optimality is usually sacrificed is "
           "worth making."},

  {"t": "section", "label": "Part 3", "title": "Planning in games",
   "blurb": "GOAP, and why it was adopted."},

  {"t": "callout", "title": "GOAP: plan backwards from a goal through action preconditions",
   "kind": "Why games use planning",
   "body": ["<b>Give each action preconditions and effects, give the "
            "agent a goal, and search backwards for a satisfying action "
            "sequence.</b> That is goal-oriented action planning.",
            "<b>The appeal is authoring:</b> <b>add a new action and "
            "every agent can use it immediately, in combinations you did "
            "not anticipate</b> — no state machine to rewire "
            "(Module 11 §1).",
            "<b>Which produces emergent, situation-appropriate "
            "behaviour</b> — an agent that reloads behind cover "
            "because the plan required cover and ammunition, not because "
            "anyone scripted it.",
            "<b>And the cost is debuggability.</b> <b>When the agent "
            "does something strange, the cause is an interaction between "
            "action descriptions, which is much harder to find than a bad "
            "transition</b> — which is why many studios moved back to "
            "behaviour trees."]},

  {"t": "section", "label": "Part 4", "title": "Limits",
   "blurb": "What classical planning assumes, and what breaks it."},

  {"t": "bullets", "kicker": "Assumptions", "title": "The classical assumptions, and what fails without them",
   "items": [
     "<b>Deterministic actions.</b> If actions can fail, you need a "
     "policy rather than a plan (Module 10) — or replanning on "
     "failure, which games use.",
     "",
     "<b>Full observability.</b> Otherwise you plan over belief "
     "states, and the space explodes.",
     "",
     "<b>A static world.</b> <b>Nothing else changes while you "
     "act</b> — false in any game with other agents.",
     "",
     "<b>Instantaneous, non-overlapping actions.</b> Real actions take "
     "time and overlap, which is temporal planning.",
     "",
     "<b>And discrete facts.</b> Numeric resources need numeric "
     "planning, which is substantially harder.",
   ],
   "footnote": "<b>Games survive these violations by replanning "
               "frequently</b> — a plan is treated as a current "
               "intention rather than a commitment, which is the "
               "practical resolution."},

  {"t": "callout", "title": "Hierarchical planning is how the scale problem is handled",
   "kind": "The practical extension",
   "body": ["<b>Hierarchical task networks decompose a high-level task "
            "into methods</b>, each a partially ordered set of subtasks, "
            "down to primitive actions.",
            "<b>So the domain author supplies the decomposition "
            "knowledge</b> rather than relying on search to discover "
            "long plans — which is why HTN planners solve much larger "
            "problems than classical ones.",
            "<b>The trade is that you are back to authoring "
            "structure</b>, so you lose some of Part 3's "
            "combinatorial-authoring benefit.",
            "<b>And this is Module 02 §4's abstraction "
            "again</b> — the same reduction in effective depth, with "
            "the hierarchy supplied by a person instead of derived."]},
 ],
 "takeaways": [
   "A planning action is preconditions plus add and delete effects, and "
   "describing actions declaratively is what the whole field rests on.",
   "Declarativeness buys automatic heuristic derivation, which is why "
   "planning is a separate field rather than an application of generic "
   "search.",
   "The delete relaxation makes the problem polynomial, and its cost is an "
   "admissible heuristic — Module 03's relaxation performed by "
   "machine.",
   "h_FF extracts a relaxed plan and counts it; it is inadmissible, "
   "strong, and cheap, and it is what made planners practical.",
   "GOAP's appeal is authoring: add an action and every agent can use it "
   "in combinations nobody anticipated — at the cost of "
   "debuggability.",
   "Games survive the classical assumptions by replanning frequently, "
   "treating a plan as a current intention rather than a commitment.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Declarative action descriptions"),
  ("code", """STATE: a set of facts taken to be true.
    { At(Agent, Room1), Has(Key), Closed(Door12) }

ACTION SCHEMA:
    Open(d, r1, r2)
        PRECOND: At(Agent,r1), Connects(d,r1,r2),
                 Closed(d), Has(Key)
        ADD:     Open(d)
        DELETE:  Closed(d)

A PLAN is a sequence of actions leading from the initial
state to a state satisfying the goal. This is still
Module 02's search: states, a successor function (apply an
action whose preconditions hold), and a goal test.

THE DIFFERENCE IS THAT THE ACTIONS ARE DESCRIBED RATHER
THAN CODED. And that single change is what makes everything
else in this module possible:

    the planner can REASON ABOUT the actions themselves
    it can compute which actions are RELEVANT to a goal
    it can detect that two actions are INDEPENDENT and so
        can be reordered or parallelised
    and it can DERIVE A HEURISTIC AUTOMATICALLY (section 2)

THAT LAST ONE IS THE PAYOFF. With a hand-coded successor
function you must invent a heuristic yourself (Module 03
section 3). With a declarative domain the planner derives
one from the action descriptions, with no domain-specific
insight whatsoever."""),
  ("p", "<b>Declarativeness buys automatic heuristics</b>, and <b>that is "
        "why planning exists as a separate field rather than as an "
        "application of Module 02</b>. It is worth sitting with the "
        "point: <b>the reason to write the domain in a restricted, "
        "inspectable language is to let the solver do work that would "
        "otherwise require you</b> — which is the same argument as "
        "CSCE 669 Module 13's case for a modelling layer, and the "
        "same argument as declarative query languages against hand-written "
        "loops (CSCE 608)."),

  ("h1", "2 &nbsp; Heuristics for free"),
  ("callout", "Ignore the delete lists, and the problem becomes easy",
   ["<b>Drop every action's delete list.</b> Facts can then only "
    "accumulate — nothing that becomes true ever becomes false "
    "again, so there is no possibility of undoing progress.",
    "<b>The relaxed problem is solvable in polynomial time</b> by "
    "forward chaining to a fixed point, <b>and its cost is an admissible "
    "heuristic for the original problem</b>, because every real plan is "
    "also a valid plan in the relaxed problem and therefore the relaxed "
    "optimum is a lower bound.",
    "<b>This is Module 03 &sect;3's relaxation argument applied "
    "automatically.</b> <b>The planner derives the relaxation from the "
    "domain description, mechanically, with no human insight</b> — "
    "which is why this result transformed automated planning from a field "
    "that could solve toy problems into one that solves large ones. "
    "<b>And it is CSCE 669 Module 10 &sect;1's bound-from-a-relaxation "
    "mechanism for the third time in this program</b>, which at this "
    "point should be read as a general technique rather than a "
    "coincidence.",
    "<b>Three heuristics follow from it:</b> <b>h_max</b> (the cost of "
    "the most expensive individual subgoal — admissible and weak), "
    "<b>h_add</b> (the sum of subgoal costs — inadmissible, because "
    "it double-counts work shared between subgoals, and stronger), and "
    "<b>h_FF</b> (extract an actual relaxed plan and count its "
    "actions — inadmissible, strong, cheap, and the heuristic that "
    "made planners work in practice)."]),
  ("table", ["Heuristic", "What it computes", "Property"],
   [["<b>h_max</b>",
     "<b>The cost of the single most expensive subgoal in the "
     "relaxation.</b>",
     "<b>Admissible, and weak</b> — it ignores that the other "
     "subgoals also cost something."],
    ["<b>h_add</b>", "<b>The sum of all subgoal costs.</b>",
     "<b>Inadmissible, because work shared between subgoals is counted "
     "more than once</b>; substantially stronger in practice."],
    ["<b>h_FF</b>",
     "<b>Extract an actual plan for the relaxed problem and count its "
     "actions.</b>",
     "<b>Inadmissible, strong, and cheap — the practical "
     "winner</b>, and it also yields <i>helpful actions</i> (the first "
     "actions of the relaxed plan) which prune the branching enormously."],
    ["<b>Landmark heuristics</b>",
     "<b>Facts or actions that every valid plan must achieve.</b>",
     "<b>Admissible variants exist and are strong</b>, and they are the "
     "basis of most current optimal planners."]],
   [0.16, 0.37, 0.47]),
  ("p", "<b>Modern planners mostly use inadmissible heuristics with greedy "
        "best-first search</b>, trading optimality for the ability to "
        "solve the problem at all — which is worth stating plainly, "
        "since Module 03 spent its effort on admissibility. <b>The "
        "honest position is that optimal planning is a much smaller field "
        "than satisficing planning</b>, and for most applications "
        "(including every game application) a good plan found quickly "
        "beats an optimal plan found slowly."),

  ("break",),
  ("h1", "3 &nbsp; Planning in games"),
  ("callout", "GOAP: plan backwards from a goal through action "
              "preconditions",
   ["<b>Give each action a set of preconditions and effects, give the "
    "agent a goal, and search backwards from the goal through actions "
    "whose effects satisfy it, until reaching the current world "
    "state.</b> That is goal-oriented action planning, and backwards "
    "search is used because the goal is specific and the state space is "
    "large.",
    "<b>The appeal is authoring.</b> <b>Add a new action and every agent "
    "can use it immediately, in combinations nobody anticipated</b> "
    "— there is no state machine to rewire and no transitions to "
    "add (Module 11 &sect;1's comparison). <b>The authoring cost is "
    "linear in actions rather than quadratic in states</b>, which is the "
    "concrete form of the advantage.",
    "<b>Which produces emergent, situation-appropriate behaviour.</b> An "
    "agent that takes cover and then reloads, because the plan required "
    "both ammunition and safety and the planner ordered them sensibly "
    "— <b>not because anyone scripted 'reload behind cover'</b>. "
    "This is what made GOAP notable when it shipped.",
    "<b>And the cost is debuggability.</b> <b>When the agent does "
    "something strange, the cause is an interaction between action "
    "descriptions, which is far harder to locate than a bad transition in "
    "a state machine</b> — and it may only manifest in one world "
    "configuration. <b>Which is why many studios moved back to behaviour "
    "trees</b> (Module 11 &sect;2), and is a genuine engineering "
    "trade rather than a failure of the technique: <b>the combinatorial "
    "authoring that makes GOAP powerful is exactly what makes it hard to "
    "reason about.</b>"]),

  ("h1", "4 &nbsp; Limits"),
  ("ul", ["<b>Deterministic actions.</b> If an action can fail, a "
          "sequence is not enough — <b>you need a policy that says "
          "what to do in each resulting state</b> (Module 10), <b>or "
          "replanning on failure</b>, which is what games actually do.",
          "<b>Full observability.</b> Otherwise you must plan over "
          "belief states rather than states, and the space explodes "
          "(Module 01 &sect;2).",
          "<b>A static world.</b> <b>Nothing else changes while you "
          "act</b> — which is false in any game containing other "
          "agents, and is the assumption most obviously violated.",
          "<b>Instantaneous, non-overlapping actions.</b> Real actions "
          "take time and can overlap, which requires temporal planning "
          "with durations and concurrency — a substantially harder "
          "problem.",
          "<b>And discrete facts.</b> Numeric resources — fuel, "
          "ammunition counts, health — require numeric planning, "
          "which is harder again and where planning starts to overlap "
          "with CSCE 669's optimisation.",
          "<b>Games survive these violations by replanning "
          "frequently</b>: a plan is treated as a <i>current "
          "intention</i> rather than a commitment, discarded as soon as "
          "the world invalidates it, and recomputed. <b>Which is "
          "Module 04 &sect;3's replanning discipline applied to "
          "behaviour rather than to paths</b>, and it is the practical "
          "resolution of all five assumptions at once."]),
  ("callout", "Hierarchical planning is how the scale problem is handled",
   ["<b>Hierarchical task networks decompose a high-level task into "
    "<i>methods</i></b>, each a partially ordered set of subtasks, "
    "recursively down to primitive actions — so the search is over "
    "decompositions rather than over action sequences.",
    "<b>So the domain author supplies the decomposition knowledge</b> "
    "rather than relying on search to discover a long plan from "
    "scratch — <b>which is why HTN planners solve substantially "
    "larger problems than classical ones</b> and are what most "
    "industrial planning applications actually use.",
    "<b>The trade is that you are back to authoring structure</b>, so "
    "<b>you lose part of &sect;3's combinatorial-authoring "
    "benefit</b> — adding an action no longer automatically makes it "
    "available everywhere, because it must appear in some method.",
    "<b>And this is Module 02 &sect;4's abstraction arriving "
    "again</b> — the same reduction in effective search depth, with "
    "<b>the hierarchy supplied by a person rather than derived from the "
    "problem</b>. <b>Which is the recurring trade of this whole "
    "course:</b> human knowledge reduces search, search reduces the need "
    "for human knowledge, and every practical system picks a point "
    "between them."]),
 ],
 "resources": [
   ("Russell & Norvig &mdash; AIMA, chapters 11–12 (pseudocode "
    "free)",
    "https://aima.cs.berkeley.edu/",
    "<b>STRIPS, the delete relaxation, and the heuristics of "
    "&sect;2</b>, developed carefully."),
   ("Hoffmann & Nebel &mdash; The FF Planning System (free)",
    "https://arxiv.org/abs/1106.0675",
    "<b>The h_FF heuristic and helpful actions of &sect;2</b>, which is "
    "the paper that changed the field's capability."),
   ("Orkin &mdash; Three States and a Plan: The AI of F.E.A.R. (free)",
    "https://web.archive.org/web/2020/https://alumni.media.mit.edu/"
    "~jorkin/gdc2006_orkin_jeff_fear.pdf",
    "<b>The &sect;3 GOAP case study</b>, by the person who shipped it. "
    "The clearest account of both the appeal and the cost."),
   ("Ghallab, Nau & Traverso &mdash; Automated Planning and Acting (free "
    "draft)",
    "http://projects.laas.fr/planning/",
    "<b>The reference for &sect;4</b>, including HTN planning and the "
    "treatment of acting under the violated assumptions."),
 ],
 "exercises": [
   "<b>Write a STRIPS domain</b> for a small problem with at least six "
   "action schemas.",
   "<b>Implement forward search over it</b> with h = 0 and report node "
   "counts.",
   "<b>Implement the delete relaxation</b> and compute h_max and h_add.",
   "<b>Compare node counts</b> with each heuristic and confirm h_add is "
   "stronger and inadmissible.",
   "<b>Implement h_FF</b> by extracting a relaxed plan, and report the "
   "improvement.",
   "<b>Extract helpful actions</b> from the relaxed plan and use them to "
   "prune. Report the effect.",
   "<b>Build a small GOAP agent</b> with eight actions and observe which "
   "plans it produces.",
   "<b>Add one new action</b> and report which new behaviours appeared "
   "without further authoring.",
   "<b>Then find a plan it produces that you consider wrong</b>, and "
   "trace it to the action interaction responsible.",
   "<b>Make an action fail at runtime</b> and implement replanning. "
   "Report how often it triggers.",
 ],
 "selfcheck": [
   "Write an action in STRIPS form and define a plan.",
   "What does declarative action description buy, and why is that the "
   "whole point?",
   "Explain the delete relaxation and why its cost is admissible.",
   "Compare h_max, h_add, h_FF, and landmarks.",
   "Why do modern planners mostly use inadmissible heuristics?",
   "What is GOAP's authoring advantage, stated precisely?",
   "What is GOAP's cost, and why did studios move away from it?",
   "Name five classical assumptions and what fails without each.",
   "How do games survive those violations?",
   "What does HTN planning trade, and what does it correspond to?",
 ],
},

]
