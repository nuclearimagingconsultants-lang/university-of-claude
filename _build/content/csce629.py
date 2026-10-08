# -*- coding: utf-8 -*-
"""CSCE 629 Analysis of Algorithms — original course content."""

COURSE = {
    "code": "CSCE 629",
    "title": "Analysis of Algorithms",
    "tagline": "Design techniques, rigorous analysis, and the boundary "
               "between tractable and intractable",
    "term": "Semester 1 (with CSCE 641 and CSCE 614)",
    "prereqs": "Discrete mathematics and proof technique (UC MATH 600); "
               "comfort with a programming language",
    "effort": "10–12 hours per week · 13 modules + 2 project weeks",
    "deliverable": "An algorithms portfolio: every technique implemented, "
                   "benchmarked against its predicted complexity, with the "
                   "gap between theory and measurement explained",
    "description": [
        "An algorithms course is usually sold as a catalogue of algorithms. "
        "That is the least durable part of it. The algorithms you will need "
        "in five years mostly have library implementations; what you will "
        "need is the judgement to recognise which problem you are holding, "
        "which technique it yields to, and whether the thing you want is "
        "possible at all.",
        "So this course is organised around <i>techniques</i> and "
        "<i>arguments</i> rather than around a list. Divide and conquer, "
        "greedy exchange, dynamic programming, flow, randomisation, "
        "amortisation — and for each, the proof pattern that tells you "
        "whether your instinct is correct. A greedy algorithm that happens to "
        "work on your test cases is worth nothing; a greedy algorithm with an "
        "exchange argument is a theorem.",
        "The second half turns to limits. Lower bounds tell you when to stop "
        "optimising. NP-completeness tells you when to stop looking for an "
        "exact algorithm and start designing an approximation. Knowing where "
        "those walls are is what separates an engineer who ships from one who "
        "spends a month on a problem that was proven impossible in 1972.",
        "Throughout, you implement and measure. Asymptotic analysis is a "
        "model, and models have domains of validity. Part of this course is "
        "learning exactly where the model stops predicting your machine "
        "— a theme CSCE 614 takes up in earnest.",
    ],
    "outcomes": [
        "Choose and justify an algorithm design technique from the structure "
        "of a problem.",
        "Solve recurrences by substitution, recursion tree, and the master "
        "theorem, and say when each applies.",
        "Prove greedy algorithms correct with exchange arguments, and "
        "recognise when greed fails.",
        "Design dynamic programs by identifying subproblem structure, and "
        "analyse their complexity.",
        "Model problems as network flow or matching, and apply the "
        "max-flow min-cut theorem.",
        "Prove a problem NP-complete by reduction from a known hard problem.",
        "Design approximation algorithms with proven ratios when exactness is "
        "unavailable.",
        "Explain where asymptotic analysis stops predicting real running "
        "time, and why.",
    ],
    "materials": [
        ("MIT 6.046J Design and Analysis of Algorithms (OCW, full video)",
         "https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/",
         "Primary lecture series. Graduate level, closely matched to this "
         "course's order. Watch the mapped lecture before each module."),
        ("MIT 6.006 Introduction to Algorithms, Spring 2020 (OCW, full video)",
         "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
         "The undergraduate predecessor. Use it when a 6.046 lecture assumes "
         "background you do not have — particularly for hashing, graph "
         "search, and basic DP."),
        ("Jeff Erickson, Algorithms (free book)",
         "https://jeffe.cs.illinois.edu/teaching/algorithms/",
         "The best free algorithms textbook in existence, and unusually good "
         "on <i>how to think</i> rather than only what is true. Primary "
         "written reference for this course."),
        ("Tim Roughgarden, Algorithms Illuminated (free videos)",
         "https://www.algorithmsilluminated.org/",
         "A third voice, strong on intuition and on why each analysis is "
         "structured the way it is."),
        ("Competitive Programmer's Handbook (free)",
         "https://cses.fi/book/book.pdf",
         "Implementation-focused. Use for the practical details the theory "
         "courses skip, and pair it with the CSES problem set."),
        ("CSES Problem Set (free, auto-graded)",
         "https://cses.fi/problemset/",
         "300 problems ordered by technique. The best free source of "
         "exercises with immediate feedback."),
    ],
    "tooling": [
        "<b>One language you are fluent in.</b> C++ or Python. C++ if you "
        "want the constant factors to be visible; Python if you want to "
        "iterate faster. Do not learn a language and algorithms at once.",
        "<b>A benchmarking harness</b> you write in Module 01 and reuse all "
        "term: time a function across input sizes, write a CSV, plot it.",
        "<b>matplotlib</b> or equivalent. Every complexity claim in this "
        "course should be checked against a measured curve at least once.",
        "<b>A portfolio repository</b>, public, one directory per module.",
    ],
    "projects": [
        {"title": "Measured complexity", "after": 5,
         "brief": "Implement eight algorithms from the first five modules and "
                  "measure them against their predicted asymptotics. The "
                  "deliverable is not the code — it is a written account "
                  "of where measurement and theory diverged, and why.",
         "reqs": [
             "Mergesort, quicksort (randomised), heapsort, insertion sort, "
             "binary search, randomised selection, a hash table with chaining, "
             "and a dynamic array with doubling.",
             "A harness that times each across at least six input sizes "
             "spanning three orders of magnitude, with repeated trials.",
             "Log-log plots with fitted slopes, compared against predicted "
             "exponents.",
             "At least three documented cases where the measured curve "
             "departs from the predicted one.",
         ],
         "done": [
             "Insertion sort beats mergesort below some crossover size. "
             "Report the size and explain it.",
             "Quicksort beats mergesort despite identical asymptotics. "
             "Explain in terms of memory, not operation counts.",
             "A hash table's performance degrades at a specific load factor. "
             "Show the curve and name the cause.",
         ]},
        {"title": "A hard problem, three ways", "after": 12,
         "brief": "Take one NP-hard problem and attack it three ways: an "
                  "exact exponential algorithm, an approximation with a "
                  "proven ratio, and a heuristic with no guarantee. Compare "
                  "them honestly on real instances.",
         "reqs": [
             "Choose from: vertex cover, TSP (metric), set cover, knapsack, "
             "graph colouring, or maximum independent set.",
             "An exact algorithm with branch and bound or DP over subsets, "
             "with the instance size at which it becomes unusable reported.",
             "An approximation algorithm with the ratio <b>proved</b>, not "
             "cited.",
             "A heuristic (local search, greedy with restarts, simulated "
             "annealing) with no guarantee.",
             "A written comparison on at least twenty instances: solution "
             "quality against running time.",
         ],
         "done": [
             "A plot of solution quality versus time for all three methods.",
             "A proof of your approximation ratio, written out.",
             "An instance where the heuristic beats the approximation "
             "algorithm, and one where it loses badly. Both explained.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "What Analysis Means",
 "subtitle": "Models of computation, growth, and the honest limits of "
             "asymptotic reasoning.",
 "question": "What exactly are we measuring, and what is the measurement "
             "worth?",
 "outcomes": [
     "State what a model of computation is and why analysis requires one.",
     "Use O, Ω, and Θ precisely, including what each does not say.",
     "Distinguish worst-case, average-case, and amortised analysis.",
     "Explain where asymptotic analysis stops predicting real running time.",
     "Build a benchmarking harness and read a log-log plot.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Counting what?",
   "blurb": "Before you can analyse an algorithm you must say what a step is."},

  {"t": "bullets", "kicker": "Models", "title": "Analysis requires a model",
   "items": [
     "'How long does this take?' is meaningless without saying on what "
     "machine.",
     "A <b>model of computation</b> fixes what counts as one step.",
     "",
     "<b>RAM model</b> — the default. Arithmetic, comparison, and memory "
     "access on word-sized values each cost 1.",
     ("Memory is uniform: every access costs the same.", 1),
     ("That assumption is <i>false</i> on real hardware, and Module 05 of "
      "CSCE 614 is about how false.", 1),
     "",
     "Other models exist because they make different questions answerable:",
     ("Comparison model — gives the Ω(n log n) sorting bound.", 1),
     ("Cell-probe, external memory, parallel — each isolates a "
      "different resource.", 1),
   ],
   "note": "The point is not that the RAM model is wrong, but that it is a "
           "choice with consequences. Students who never hear this treat "
           "asymptotics as physics."},

  {"t": "callout", "title": "A model is a decision about what to ignore",
   "kind": "Key idea",
   "body": ["The RAM model ignores the memory hierarchy, so it cannot "
            "distinguish an algorithm with good locality from one without. "
            "Those differ by 10–50× on real machines.",
            "That is not a defect. It is the price of a model simple enough "
            "to prove theorems in. The defect would be forgetting you made "
            "the trade.",
            "Rule for this course: prove in the model, measure on the "
            "machine, and explain every gap."]},

  {"t": "eq", "kicker": "Notation", "title": "O, Ω, Θ — stated precisely",
   "eqs": [
     ("f = O(g)   ⟺   ∃ c, n₀ : f(n) ≤ c·g(n)  for all n ≥ n₀",
      "Upper bound. An <i>at most</i> claim."),
     ("f = Ω(g)   ⟺   ∃ c, n₀ : f(n) ≥ c·g(n)  for all n ≥ n₀",
      "Lower bound. An <i>at least</i> claim."),
     ("f = Θ(g)   ⟺   f = O(g) and f = Ω(g)",
      "Tight. The one you should be aiming for."),
   ],
   "caption": "Note 'for all n ≥ n₀': these say nothing whatsoever "
              "about small inputs, which is exactly where most real programs "
              "live.",
   "note": "Hammer the quantifiers. 'O(n log n)' is a statement with "
           "existential constants in it, and students who never unpack them "
           "misuse it for years."},

  {"t": "bullets", "kicker": "Notation", "title": "What the notation does not say",
   "items": [
     "<b>O is an upper bound, not a description.</b> Binary search is "
     "O(n³). True, and useless.",
     ("Say Θ when you mean Θ.", 1),
     "",
     "<b>Constants are hidden, and constants decide real programs.</b>",
     ("An O(n) algorithm with a 10⁶ constant loses to O(n²) until "
      "n is enormous.", 1),
     "",
     "<b>Nothing is claimed below n₀.</b> Hybrid sorts exist precisely "
     "because of this.",
     "",
     "<b>Worst case is a guarantee, not a prediction.</b> Quicksort's worst "
     "case is Θ(n²) and nobody cares.",
   ]},

  {"t": "section", "label": "Part 2", "title": "Which case?",
   "blurb": "Worst, average, amortised — three different questions."},

  {"t": "table", "kicker": "Cases", "title": "Three kinds of claim",
   "header": ["Analysis", "Answers", "Use when"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Worst case", "What is the guarantee?",
      "Real-time deadlines; adversarial input; anything safety-related"],
     ["Average case", "What happens on a random input?",
      "You can characterise the input distribution honestly"],
     ["Amortised", "What is the cost per operation over a sequence?",
      "Occasional expensive operations pay for many cheap ones"],
     ["Expected (randomised)", "What happens over the algorithm's own coins?",
      "The randomness is yours, so no adversary can target it"],
   ],
   "note": "The last row is the one worth dwelling on: expected-case for a "
           "randomised algorithm is a far stronger claim than average-case, "
           "because it does not depend on an assumption about the input."},

  {"t": "callout", "title": "Average case and expected case are not the same",
   "kind": "Distinction that matters",
   "body": ["<b>Average case</b> assumes the <i>input</i> is random. If your "
            "inputs are not — and they usually are not — the "
            "analysis does not apply. Sorted or nearly-sorted data is "
            "extremely common in practice.",
            "<b>Expected case</b> for a randomised algorithm averages over "
            "the <i>algorithm's own coin flips</i>. It holds for every input, "
            "including adversarial ones, because the adversary cannot see "
            "your randomness.",
            "This is why randomised quicksort is used and deterministic "
            "median-of-first-element quicksort is not. Module 03 develops "
            "this."]},

  {"t": "section", "label": "Part 3", "title": "Where the model breaks",
   "blurb": "The honest part, usually left out."},

  {"t": "table", "kicker": "Reality", "title": "Why measurement disagrees with theory",
   "header": ["Cause", "Effect", "Seen in"],
   "widths": [3.3, 4.6, 4.2],
   "rows": [
     ["Cache hierarchy", "Sequential access beats random by 10–50×",
      "Array vs linked list; mergesort vs quicksort"],
     ["Branch prediction", "Unpredictable branches cost ~15 cycles",
      "Branchy binary search vs branchless"],
     ["Constant factors", "Hidden in Θ, decisive below n₀",
      "Insertion sort inside mergesort"],
     ["Allocation", "Not a step in the RAM model; expensive in reality",
      "Any algorithm that allocates per element"],
     ["Vectorisation", "8–16× on predictable loops",
      "Linear scan beating a tree at small n"],
   ],
   "footnote": "None of these appear in the RAM model. All of them decide "
               "real benchmarks.",
   "note": "This table is the bridge to CSCE 614 and should be framed that "
           "way. The two courses run concurrently for exactly this reason."},

  {"t": "code", "kicker": "Practice", "title": "The harness you will reuse all term",
   "lang": "python", "code": """
import time, statistics

def bench(fn, make_input, sizes, trials=5):
    rows = []
    for n in sizes:
        ts = []
        for _ in range(trials):
            data = make_input(n)        # build OUTSIDE the timed region
            t0 = time.perf_counter()
            fn(data)
            ts.append(time.perf_counter() - t0)
        rows.append((n, statistics.median(ts)))   # median, not mean:
    return rows                                   # one slow trial should
                                                  # not move the estimate

# Read the exponent straight off a log-log fit:
#   slope ~ 1.0  -> linear      slope ~ 2.0 -> quadratic
#   slope ~ 1.1  -> n log n     slope ~ 0.0 -> constant
""",
   "caption": "Median rather than mean, and input construction outside the "
              "timed region. Both mistakes are easy to make and both quietly "
              "invalidate the measurement.",
   "note": "n log n and n are hard to tell apart on a log-log plot over a "
           "small range — worth saying, so students span three orders of "
           "magnitude."},

  {"t": "bullets", "kicker": "Growth", "title": "The hierarchy, and where the cliffs are",
   "items": [
     "<b>O(1)</b> → <b>O(log n)</b> → <b>O(n)</b> → "
     "<b>O(n log n)</b> → <b>O(n²)</b> → <b>O(2ⁿ)</b> "
     "→ <b>O(n!)</b>",
     "",
     "The practical cliffs on a modern machine, for a one-second budget:",
     ("O(n²) stops being usable around n ≈ 10⁴.", 1),
     ("O(n log n) handles n ≈ 10⁷ comfortably.", 1),
     ("O(2ⁿ) stops around n ≈ 25; with memoisation over subsets, "
      "n ≈ 20 at O(2ⁿ·n).", 1),
     "",
     "These numbers are worth memorising. They let you reject a design in "
     "ten seconds rather than a week.",
   ],
   "footnote": "Knowing which cliff you are near is more useful day to day "
               "than knowing any particular algorithm."},
 ],
 "takeaways": [
   "Analysis requires a model of computation, and every model is a decision "
   "about what to ignore. The RAM model ignores the memory hierarchy.",
   "O is an upper bound, Θ is tight. Say Θ when you mean it.",
   "Asymptotic claims say nothing below n₀ and hide all constants "
   "— which is where real programs live.",
   "Average case assumes a random input; expected case averages over your "
   "own randomness and holds for every input. The second is far stronger.",
   "Cache behaviour, branch prediction, and allocation decide real benchmarks "
   "and appear in no model you will prove things in.",
   "Prove in the model, measure on the machine, explain every gap. That is "
   "the whole method of this course.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What are we counting?"),
  ("p", "The question 'how fast is this algorithm?' has no answer until you "
        "say what machine it runs on, and real machines are far too "
        "complicated to prove anything about. So we analyse algorithms "
        "against a <b>model of computation</b>: an idealised machine simple "
        "enough to reason about and close enough to reality to be useful."),
  ("p", "The default is the <b>RAM model</b>. It assumes a processor "
        "executing instructions one at a time, with arithmetic, comparison, "
        "and memory access on word-sized values each costing one unit of "
        "time. Memory is uniform — every access costs the same, "
        "regardless of address or history."),
  ("callout", "That last assumption is false",
   ["On real hardware, an L1 cache hit costs about 4 cycles and a main-memory "
    "miss about 200. Memory access is not uniform; it is not close to "
    "uniform.",
    "This means the RAM model <i>cannot distinguish</i> an algorithm with "
    "good memory locality from one without. Two algorithms with identical "
    "&Theta; bounds can differ by an order of magnitude on a real machine, "
    "and the model is blind to it.",
    "This is not a reason to abandon the model. It is a reason to know what "
    "it does not see. CSCE 614 runs alongside this course precisely so you "
    "learn both halves at once."]),
  ("h2", "1.1 &nbsp; Other models, and what each is for"),
  ("table", ["Model", "One step is", "Lets you prove"],
   [["RAM", "An arithmetic op or a memory access",
     "Nearly everything in this course. The default."],
    ["Comparison model", "A comparison between two elements",
     "The &Omega;(n log n) sorting lower bound, which is a statement about "
     "<i>all possible</i> comparison sorts."],
    ["External memory", "A block transfer between disk and memory",
     "Why B-trees have the branching factor they do."],
    ["Cell probe", "A read or write of one memory cell",
     "Data-structure lower bounds, independent of computation cost."],
    ["PRAM / work-span", "A parallel step across many processors",
     "Parallel speedup limits. CSCE 735 uses this."]],
   [0.20, 0.33, 0.47]),
  ("p", "Choosing a model is choosing which resource you think is scarce. "
        "That is a modelling judgement, and getting it wrong is how you end "
        "up optimising something that was never the bottleneck."),

  ("h1", "2 &nbsp; Asymptotic notation, precisely"),
  ("p", "The definitions are worth writing out in full, because almost every "
        "common misuse comes from forgetting a quantifier."),
  ("eq", "f = O(g) &nbsp;&hArr;&nbsp; &exist; c &gt; 0, n&#8320; : f(n) &le; c&middot;g(n) for all n &ge; n&#8320;"),
  ("eq", "f = &Omega;(g) &nbsp;&hArr;&nbsp; &exist; c &gt; 0, n&#8320; : f(n) &ge; c&middot;g(n) for all n &ge; n&#8320;"),
  ("eq", "f = &Theta;(g) &nbsp;&hArr;&nbsp; f = O(g) and f = &Omega;(g)"),
  ("h2", "2.1 &nbsp; Four things the notation does not say"),
  ("ol", ["<b>O is not a description.</b> It is an upper bound, and upper "
          "bounds compose upward freely. Binary search is O(n&#179;). The "
          "statement is true and conveys nothing. When you know the tight "
          "bound, say &Theta;.",
          "<b>Constants are invisible, and constants decide programs.</b> An "
          "O(n) algorithm with a constant of 10&#8310; loses to an O(n&#178;) "
          "algorithm until n exceeds a million. Galactic algorithms — "
          "asymptotically optimal, never used — are an entire genre.",
          "<b>Nothing is claimed below n&#8320;.</b> This is not a technicality: "
          "most real inputs are small. Production sort implementations switch "
          "to insertion sort below about 16 elements for exactly this reason.",
          "<b>Worst case is a guarantee, not a prediction.</b> Quicksort's "
          "worst case is &Theta;(n&#178;); it is the standard sort anyway, "
          "because the worst case is vanishingly unlikely once randomised."]),

  ("h1", "3 &nbsp; Which case are you analysing?"),
  ("table", ["Kind", "Averages over", "Strength"],
   [["Worst case", "Nothing — it is a maximum over all inputs",
     "A guarantee. Holds always, including under attack."],
    ["Average case", "An assumed distribution on inputs",
     "Only as good as the assumption. Real data is rarely uniformly random "
     "— sorted, nearly sorted, and heavily duplicated inputs are all "
     "common."],
    ["Expected case (randomised)", "The algorithm's own coin flips",
     "Holds for <i>every</i> input. Strictly stronger than average case, and "
     "the reason randomisation is so useful."],
    ["Amortised", "A sequence of operations",
     "A guarantee on the total, not on any single operation. Different from "
     "average case: no probability is involved at all."]],
   [0.22, 0.30, 0.48]),
  ("callout", "The distinction that matters most",
   ["<b>Average case</b> says: if your input is drawn from distribution D, "
    "the expected cost is X. An adversary who knows your algorithm can simply "
    "supply an input outside D.",
    "<b>Expected case</b> for a randomised algorithm says: for <i>any</i> "
    "input whatsoever, the expected cost over my internal randomness is X. "
    "The adversary cannot do anything about this, because they cannot see "
    "your coins.",
    "This is precisely why randomised quicksort replaced deterministic "
    "quicksort. The deterministic version has a worst case an attacker can "
    "trigger; the randomised version has one that no attacker can target. "
    "Module 03 makes this rigorous."]),
  ("p", "<b>Amortised</b> analysis is a separate idea that students routinely "
        "conflate with average case. It involves no probability at all. It is "
        "a worst-case statement about a <i>sequence</i>: the total cost of n "
        "operations is bounded, even though individual operations may be "
        "expensive. Module 05 covers it properly."),

  ("break",),
  ("h1", "4 &nbsp; Where the model stops predicting"),
  ("p", "This section is normally omitted from algorithms courses, which is a "
        "mistake. The gap between analysis and measurement is not noise; it "
        "is structured, explicable, and worth understanding."),
  ("table", ["Effect", "Why the model misses it", "Typical magnitude"],
   [["<b>Memory hierarchy</b>",
     "The RAM model charges 1 for every access regardless of locality.",
     "10&ndash;50&times;. Sequential array traversal versus pointer chasing "
     "through a linked list is the canonical example, and the asymptotics are "
     "identical."],
    ["<b>Branch misprediction</b>",
     "Control flow is free in the model.",
     "~15 cycles per miss. A branchless binary search can beat a branchy one "
     "substantially despite doing more work."],
    ["<b>Constant factors</b>",
     "Deliberately discarded by &Theta;.",
     "Decisive below n&#8320;. Real sorts hybridise for this reason."],
    ["<b>Allocation</b>",
     "Memory is free and infinite in the model.",
     "An allocation costs far more than an arithmetic operation, and "
     "allocating per element can dominate everything else."],
    ["<b>Vectorisation</b>",
     "No notion of parallel execution within one step.",
     "8&ndash;16&times; on predictable loops, which is why a linear scan can "
     "beat a binary search on small arrays."]],
   [0.20, 0.34, 0.46]),
  ("p", "The method this course adopts: <b>prove in the model, measure on the "
        "machine, and explain every gap</b>. A gap you cannot explain is a "
        "sign that you have misunderstood either the algorithm or the "
        "machine, and either way it is worth finding out which."),

  ("h1", "5 &nbsp; Measuring properly"),
  ("code", """import time, statistics

def bench(fn, make_input, sizes, trials=5):
    rows = []
    for n in sizes:
        ts = []
        for _ in range(trials):
            data = make_input(n)         # build OUTSIDE the timed region
            t0 = time.perf_counter()
            fn(data)
            ts.append(time.perf_counter() - t0)
        rows.append((n, statistics.median(ts)))
    return rows"""),
  ("h2", "5.1 &nbsp; Four ways to get this wrong"),
  ("ul", ["<b>Timing input construction.</b> Generating a random array of a "
          "million elements can take longer than sorting it. Build it outside "
          "the timed region.",
          "<b>Using the mean.</b> One unlucky trial — a GC pause, a "
          "context switch, a thermal event — moves a mean and does not "
          "move a median. Use the median.",
          "<b>Too narrow a size range.</b> n log n and n are nearly "
          "indistinguishable over one order of magnitude. Span at least "
          "three.",
          "<b>Letting the optimiser delete your work.</b> If the result is "
          "unused, a compiler may remove the computation entirely. Consume "
          "the output — accumulate it, print a checksum."]),
  ("p", "Read exponents off a log-log plot: the slope of log(time) against "
        "log(n) is the exponent. Slope 1 is linear, slope 2 is quadratic, "
        "and n log n shows as a slope slightly above 1 that drifts upward "
        "very slowly — which is why a wide range matters."),

  ("h1", "6 &nbsp; The growth hierarchy, with numbers"),
  ("table", ["Growth", "n for ~1 second", "Where you meet it"],
   [["O(1)", "Any", "Hash lookup, array index."],
    ["O(log n)", "Any", "Binary search, balanced tree operations."],
    ["O(n)", "~10&#8312;", "Linear scan, counting sort, BFS/DFS."],
    ["O(n log n)", "~10&#8311;", "Comparison sorting, most divide and conquer."],
    ["O(n&#178;)", "~10&#8308;", "Nested loops, naive all-pairs, bubble sort."],
    ["O(n&#179;)", "~10&#179;", "Floyd&ndash;Warshall, naive matrix multiply."],
    ["O(2&#8319;)", "~25", "Subset enumeration, brute-force search."],
    ["O(2&#8319;&middot;n&#178;)", "~20", "Held&ndash;Karp TSP over subsets."],
    ["O(n!)", "~11", "Permutation enumeration."]],
   [0.17, 0.20, 0.63],
   "Order-of-magnitude figures for a modern machine, assuming modest "
   "constants. They are not precise and do not need to be — their value "
   "is in letting you reject an approach in ten seconds."),
  ("callout", "The most useful table in the course",
   ["If n is 10&#8310; and your idea is O(n&#178;), it will not work. You now "
    "know this before writing any code, and you can spend the time looking "
    "for an O(n log n) formulation instead.",
    "Most of the practical value of complexity analysis is exactly this: "
    "cheap, early rejection of designs that cannot possibly meet the budget."]),
 ],
 "resources": [
   ("MIT 6.046J Lecture 01 — Course Overview, Interval Scheduling",
    "https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/",
    "Sets the level and the style of argument the course expects."),
   ("MIT 6.006 Lecture 01 — Algorithms and Computation",
    "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
    "Gentler entry point covering models and asymptotic notation carefully. "
    "Start here if the notation is not yet automatic."),
   ("Jeff Erickson, Algorithms — Chapter 0 and the Introduction",
    "https://jeffe.cs.illinois.edu/teaching/algorithms/",
    "Unusually honest about what analysis is for. Read the introduction even "
    "if you skip the chapter."),
   ("Latency Numbers Every Programmer Should Know",
    "https://gist.github.com/jboner/2841832",
    "The constants the RAM model hides, in one page. Worth memorising the "
    "orders of magnitude."),
 ],
 "exercises": [
   "Build the benchmarking harness from &sect;5 and verify it on a function "
   "with known complexity — a triple-nested loop is &Theta;(n&#179;). "
   "Confirm your log-log fit recovers a slope near 3.",
   "Prove from the definitions that 2n&#178; + 3n + 7 = &Theta;(n&#178;). "
   "State explicit constants c&#8321;, c&#8322;, and n&#8320;.",
   "Find a counterexample to the claim 'if f = O(g) then 2&#7584; = "
   "O(2&#7580;)'. Explain why exponentiation breaks the relation.",
   "Implement linear search and binary search over a sorted array. Find the "
   "n below which linear search is faster, and explain the result in terms of "
   "cache lines and branch prediction rather than operation counts.",
   "Implement array traversal in sequential order and in a random "
   "permutation. Both are &Theta;(n). Measure both across sizes spanning L1, "
   "L2, L3, and main memory, and plot the ratio. This is the single most "
   "instructive measurement in the module.",
   "Write down the growth-hierarchy table from &sect;6 from memory. Then for "
   "three problems from your own work, state n and the complexity you can "
   "afford.",
 ],
 "selfcheck": [
   "What is a model of computation, and what specifically does the RAM model "
   "choose to ignore?",
   "State the definition of O precisely, including both quantifiers. What "
   "does 'binary search is O(n&#179;)' mean, and why is saying it unhelpful?",
   "Give the difference between average-case and expected-case analysis, and "
   "explain why the latter is a stronger guarantee.",
   "Amortised analysis involves no probability. What kind of statement is it, "
   "then?",
   "Name three effects that cause measured running time to diverge from "
   "asymptotic prediction, and give the rough magnitude of each.",
   "Roughly what input size can an O(n&#178;) algorithm handle in a second? "
   "An O(2&#8319;) one? Why are these numbers worth memorising?",
 ],
},

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Divide and Conquer, and Recurrences",
 "subtitle": "Breaking a problem into pieces, and pricing the result.",
 "question": "When does splitting a problem help, and how do you compute the "
             "cost?",
 "outcomes": [
     "Recognise when a problem has exploitable divide-and-conquer structure.",
     "Solve recurrences by recursion tree, substitution, and the master "
     "theorem.",
     "State the master theorem's three cases and know when it does not apply.",
     "Analyse mergesort, Karatsuba, Strassen, and closest-pair.",
     "Explain why the combine step determines whether the technique pays.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The shape of the technique",
   "blurb": "Three steps, and only one of them is usually interesting."},

  {"t": "bullets", "kicker": "Structure", "title": "Divide, conquer, combine",
   "items": [
     "<b>Divide</b> the instance into smaller instances of the same problem.",
     "<b>Conquer</b> them recursively.",
     "<b>Combine</b> the sub-answers into an answer for the whole.",
     "",
     "Almost all of the design effort is in <b>combine</b>.",
     ("Divide is usually trivial — cut the array in half.", 1),
     ("Conquer is a recursive call.", 1),
     ("Combine is where the algorithm actually lives, and where the cost is.", 1),
     "",
     "If combine costs as much as solving the problem outright, you have "
     "gained nothing.",
   ],
   "note": "Students fixate on the split. Push them toward the merge: that is "
           "where mergesort, Karatsuba, and closest-pair all get their power."},

  {"t": "eq", "kicker": "Cost", "title": "The generic recurrence",
   "eqs": [
     ("T(n)  =  a · T(n/b)  +  f(n)",
      "a subproblems, each of size n/b, plus f(n) to divide and combine."),
     ("mergesort:  T(n) = 2T(n/2) + Θ(n)",
      "Two halves, linear merge. Gives Θ(n log n)."),
     ("binary search:  T(n) = T(n/2) + Θ(1)",
      "One half, constant work. Gives Θ(log n)."),
   ],
   "caption": "Three numbers decide everything: how many subproblems, how much "
              "smaller, and how much work outside the recursion.",
   "note": "Have them identify a, b, f(n) for several algorithms before "
           "introducing the master theorem. The pattern-matching is the "
           "skill."},

  {"t": "section", "label": "Part 2", "title": "Solving recurrences",
   "blurb": "Three methods, in order of how much they tell you."},

  {"t": "bullets", "kicker": "Method 1", "title": "Recursion tree — draw it",
   "items": [
     "Each node is a subproblem; its label is the non-recursive work f(n).",
     "Sum each level, then sum the levels.",
     "",
     "At depth i: <b>aⁱ</b> nodes, each of size <b>n/bⁱ</b>.",
     "Depth of the tree: <b>log_b n</b>.",
     "Leaves: <b>a^(log_b n) = n^(log_b a)</b>.",
     "",
     "The whole question is: does the work <b>grow</b>, <b>shrink</b>, or "
     "<b>stay level</b> as you descend?",
     ("Top-heavy → root dominates. Bottom-heavy → leaves dominate. "
      "Level → multiply by depth.", 1),
   ],
   "footnote": "This is the method to reach for first. It explains the master "
               "theorem rather than merely applying it.",
   "note": "Insist on drawing the tree at least five times before anyone uses "
           "the master theorem. Otherwise it is a black box they will misuse."},

  {"t": "eq", "kicker": "Method 2", "title": "The master theorem",
   "eqs": [
     ("Case 1:  f(n) = O(n^(log_b a − ε))   ⇒   T(n) = Θ(n^log_b a)",
      "Leaves dominate. Most of the work is at the bottom."),
     ("Case 2:  f(n) = Θ(n^log_b a)   ⇒   T(n) = Θ(n^log_b a · log n)",
      "Every level costs the same. Multiply by the number of levels."),
     ("Case 3:  f(n) = Ω(n^(log_b a + ε))  + regularity   ⇒   T(n) = Θ(f(n))",
      "Root dominates. The top-level combine is the whole cost."),
   ],
   "caption": "Compare f(n) against n^(log_b a) — the leaf count. "
              "Whichever is bigger wins; if they tie, you pay a log factor.",
   "note": "Frame it as 'compare combine work against leaf work'. That is the "
           "whole content, and it is memorable in a way the three cases are "
           "not."},

  {"t": "two", "kicker": "Master theorem", "title": "Using it, and when you cannot",
   "lh": "Works",
   "l": ["T(n) = 2T(n/2) + n → Θ(n log n)",
         ("a=2, b=2, n^log₂ 2 = n. Case 2.", 1),
         "T(n) = 4T(n/2) + n → Θ(n²)",
         ("n^log₂ 4 = n² beats n. Case 1.", 1),
         "T(n) = 2T(n/2) + n² → Θ(n²)",
         ("n² beats n. Case 3.", 1)],
   "rh": "Does not apply",
   "r": ["Unequal splits: T(n) = T(n/3) + T(2n/3) + n",
         ("Use a recursion tree instead.", 1),
         "T(n) = 2T(n/2) + n/log n",
         ("Falls in the gap between cases — no polynomial ε.", 1),
         "T(n) = T(n−1) + n",
         ("Not of the right form at all. Expand directly.", 1)],
   "note": "The gap cases matter: students who only know the master theorem "
           "assume every recurrence yields to it."},

  {"t": "bullets", "kicker": "Method 3", "title": "Substitution — guess and prove",
   "items": [
     "Guess the answer, then prove it by induction.",
     "The only general method — works when the others do not.",
     "",
     "<b>The trap:</b> the induction often fails with the obvious guess, even "
     "when the guess is correct.",
     ("Fix by <i>strengthening</i> the hypothesis — prove something "
      "stronger, which gives you more to work with.", 1),
     ("E.g. prove T(n) ≤ cn − d rather than T(n) ≤ cn.", 1),
     "",
     "Counterintuitive but standard: a stronger claim can be easier to prove "
     "by induction, because the inductive step gets a stronger assumption.",
   ],
   "note": "Strengthening the hypothesis is one of the genuinely "
           "non-obvious ideas in the course. Worth a worked example."},

  {"t": "section", "label": "Part 3", "title": "The classics",
   "blurb": "Four algorithms, each making a different point."},

  {"t": "table", "kicker": "Examples", "title": "What each one teaches",
   "header": ["Algorithm", "Recurrence", "Result", "The lesson"],
   "widths": [2.6, 3.1, 2.2, 4.2],
   "rows": [
     ["Mergesort", "2T(n/2) + Θ(n)", "Θ(n log n)",
      "The baseline. Combine is the merge."],
     ["Karatsuba", "3T(n/2) + Θ(n)", "Θ(n^1.585)",
      "Algebra reduced 4 multiplies to 3"],
     ["Strassen", "7T(n/2) + Θ(n²)", "Θ(n^2.807)",
      "Same trick on matrices; 8 → 7"],
     ["Closest pair", "2T(n/2) + Θ(n)", "Θ(n log n)",
      "Combine is clever, not obvious"],
   ],
   "note": "Karatsuba and Strassen are the same idea twice. Make that "
           "explicit — saving one subproblem changes the exponent."},

  {"t": "callout", "title": "Karatsuba: why saving one multiply changes the exponent",
   "kind": "Worth understanding deeply",
   "body": ["Naive multiplication of two n-digit numbers splits into four "
            "half-size products: T(n) = 4T(n/2) + O(n) = Θ(n²). No "
            "gain.",
            "Karatsuba computes the three products ac, bd, and (a+b)(c+d), "
            "then recovers the middle term by subtraction. Three "
            "subproblems instead of four.",
            "T(n) = 3T(n/2) + O(n) = Θ(n^log₂ 3) = "
            "Θ(n^1.585).",
            "The exponent is log₂(subproblems). Removing a single "
            "recursive call changed it, because it is inside a logarithm. "
            "This is the whole reason Strassen matters too."]},

  {"t": "code", "kicker": "Closest pair", "title": "The combine step is the algorithm",
   "lang": "python", "code": """
def closest(points_by_x, points_by_y):
    if len(points_by_x) <= 3:
        return brute_force(points_by_x)

    mid = len(points_by_x) // 2
    midx = points_by_x[mid].x
    dl = closest(left_half...)          # conquer
    dr = closest(right_half...)
    d  = min(dl, dr)

    # COMBINE: could a closer pair straddle the dividing line?
    strip = [p for p in points_by_y if abs(p.x - midx) < d]

    for i, p in enumerate(strip):
        # The key fact: at most 7 later points can be within d.
        # A d x 2d box holds at most 8 points that are pairwise >= d
        # apart -- otherwise one half would violate d.  So this inner
        # loop is O(1), and the whole combine is O(n).
        for q in strip[i+1 : i+8]:
            d = min(d, dist(p, q))
    return d
""",
   "caption": "Without the constant-7 bound the strip scan is "
              "Θ(n²) and the whole algorithm gains nothing. A "
              "geometric fact is what makes the recurrence work.",
   "note": "This is the best example in the module of combine being the "
           "entire intellectual content."},

  {"t": "bullets", "kicker": "Judgement", "title": "When divide and conquer pays",
   "items": [
     "<b>Pays</b> when subproblems are independent and combine is cheaper "
     "than solving directly.",
     "<b>Pays</b> when you can reduce the number of subproblems by algebra "
     "(Karatsuba, Strassen).",
     "",
     "<b>Does not pay</b> when subproblems overlap — you recompute the "
     "same thing exponentially often.",
     ("That is the signal for dynamic programming, Module 10.", 1),
     "",
     "<b>Does not pay</b> when combine is as expensive as the problem.",
     "",
     "Bonus: it parallelises and it is cache-friendly — subproblems "
     "eventually fit in cache without being told to.",
   ],
   "footnote": "Cache-oblivious algorithms exploit exactly that last "
               "property.",
   "note": "Flag overlapping subproblems as the DP signal now. It makes "
           "Module 10 land as a fix for a problem they have already met."},
 ],
 "takeaways": [
   "Divide, conquer, combine — and combine is where the algorithm "
   "actually lives.",
   "T(n) = aT(n/b) + f(n). Three numbers: how many subproblems, how much "
   "smaller, how much work outside the recursion.",
   "Draw the recursion tree first. The master theorem is a shortcut for a "
   "tree you should be able to draw.",
   "Compare f(n) against n^(log_b a). Bigger wins; a tie costs a log factor.",
   "The exponent is log_b(number of subproblems), so eliminating one "
   "recursive call changes the exponent — that is Karatsuba and Strassen.",
   "Overlapping subproblems mean divide and conquer is the wrong technique. "
   "That is the dynamic programming signal.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The technique"),
  ("p", "Divide and conquer has three steps, and it is worth being clear "
        "which one carries the weight."),
  ("ol", ["<b>Divide</b> the problem into subproblems of the same kind. "
          "Usually trivial: split the array, split the point set, split the "
          "digits.",
          "<b>Conquer</b> by recursing. Mechanical.",
          "<b>Combine</b> the subproblem answers into an answer for the "
          "original. <i>This is the algorithm.</i>"]),
  ("callout", "Combine is the whole design problem",
   ["In mergesort, the merge is what makes it work. In closest-pair, the "
    "strip scan is the entire intellectual content — and it depends on a "
    "geometric fact that is not obvious.",
    "If your combine step costs as much as solving the problem from scratch, "
    "the recursion has bought you nothing. When a divide-and-conquer idea "
    "fails to pay off, the combine step is almost always why."]),

  ("h1", "2 &nbsp; Recurrences"),
  ("eq", "T(n) = a &middot; T(n/b) + f(n)"),
  ("table", ["Symbol", "Means", "Mergesort", "Binary search", "Strassen"],
   [["a", "Number of subproblems", "2", "1", "7"],
    ["b", "Size shrink factor", "2", "2", "2"],
    ["f(n)", "Divide + combine cost", "&Theta;(n)", "&Theta;(1)", "&Theta;(n&#178;)"],
    ["T(n)", "Result", "&Theta;(n log n)", "&Theta;(log n)", "&Theta;(n^2.807)"]],
   [0.14, 0.28, 0.20, 0.19, 0.19]),
  ("p", "Note that <i>a</i> and <i>b</i> are independent. Binary search makes "
        "one recursive call on half the data (a = 1, b = 2); mergesort makes "
        "two (a = 2, b = 2). That difference is the whole distance between "
        "&Theta;(log n) and &Theta;(n log n)."),

  ("h1", "3 &nbsp; Method 1: the recursion tree"),
  ("p", "Draw the tree of recursive calls, label each node with its "
        "non-recursive work, sum each level, then sum the levels. It is the "
        "method to reach for first, because it tells you <i>why</i> the answer "
        "is what it is."),
  ("table", ["At depth i", "Count", "Size each", "Work each", "Level total"],
   [["", "a&#7522;", "n/b&#7522;", "f(n/b&#7522;)", "a&#7522; &middot; f(n/b&#7522;)"]],
   [0.17, 0.16, 0.16, 0.22, 0.29]),
  ("ul", ["Tree depth is log<sub>b</sub> n — how many times you can "
          "divide n by b before reaching 1.",
          "Leaf count is a<super>log<sub>b</sub> n</super> = "
          "n<super>log<sub>b</sub> a</super>. Worth deriving once; it is the "
          "quantity the master theorem compares against."]),
  ("p", "Now ask one question: as you descend, does the per-level work grow, "
        "shrink, or stay constant?"),
  ("ul", ["<b>Shrinks</b> going down → the root dominates → "
          "T(n) = &Theta;(f(n)).",
          "<b>Stays level</b> → every level costs the same → "
          "multiply by the depth → an extra log factor.",
          "<b>Grows</b> going down → the leaves dominate → "
          "T(n) = &Theta;(n<super>log<sub>b</sub> a</super>)."]),
  ("p", "Those three cases <i>are</i> the master theorem. Having seen them in "
        "a tree, the theorem stops being three arbitrary conditions to "
        "memorise."),

  ("h1", "4 &nbsp; Method 2: the master theorem"),
  ("p", "For T(n) = aT(n/b) + f(n) with a &ge; 1, b &gt; 1, compare f(n) "
        "against n<super>log<sub>b</sub> a</super> — the leaf work."),
  ("table", ["Case", "Condition", "Result", "Reading"],
   [["1", "f(n) = O(n<super>log<sub>b</sub>a &minus; &epsilon;</super>) for "
     "some &epsilon; &gt; 0",
     "&Theta;(n<super>log<sub>b</sub>a</super>)",
     "Leaves dominate: combine is cheap relative to the recursion."],
    ["2", "f(n) = &Theta;(n<super>log<sub>b</sub>a</super>)",
     "&Theta;(n<super>log<sub>b</sub>a</super> log n)",
     "Balanced: every level costs the same, so pay the depth."],
    ["3", "f(n) = &Omega;(n<super>log<sub>b</sub>a + &epsilon;</super>) and "
     "a&middot;f(n/b) &le; c&middot;f(n) for c &lt; 1",
     "&Theta;(f(n))",
     "Root dominates: the top-level combine is essentially the whole cost."]],
   [0.07, 0.36, 0.22, 0.35]),
  ("callout", "Three situations where it does not apply",
   ["<b>Unequal splits.</b> T(n) = T(n/3) + T(2n/3) + n is not of the form "
    "aT(n/b). Draw the tree instead — it gives &Theta;(n log n), with "
    "the unbalanced branches making the analysis more interesting than the "
    "answer.",
    "<b>The gaps between cases.</b> T(n) = 2T(n/2) + n/log n has f(n) smaller "
    "than n but not <i>polynomially</i> smaller, so no &epsilon; exists and "
    "Case 1 does not apply. There is a gap between each pair of cases.",
    "<b>Wrong form entirely.</b> T(n) = T(n&minus;1) + n is not a divide "
    "and conquer recurrence. Expand it directly: it telescopes to "
    "&Theta;(n&#178;)."]),

  ("break",),
  ("h1", "5 &nbsp; Method 3: substitution"),
  ("p", "Guess the answer and prove it by induction. The only fully general "
        "method, and the one worth knowing when the others fail."),
  ("p", "The characteristic difficulty is that the obvious guess often fails "
        "to carry through the induction <i>even when it is correct</i>. The "
        "standard fix is to <b>strengthen the hypothesis</b> — prove "
        "something stronger, which paradoxically makes the proof easier "
        "because the inductive step then has more to work with."),
  ("p", "For T(n) = 2T(n/2) + 1, guessing T(n) &le; cn fails: the inductive "
        "step gives 2&middot;c(n/2) + 1 = cn + 1, which exceeds cn. Guessing "
        "the <i>stronger</i> T(n) &le; cn &minus; d succeeds: "
        "2(c(n/2) &minus; d) + 1 = cn &minus; 2d + 1 &le; cn &minus; d "
        "whenever d &ge; 1."),
  ("callout", "Why a stronger claim can be easier",
   ["Induction gives you the hypothesis for smaller inputs and asks you to "
    "establish it for n. A stronger hypothesis hands you more at the start of "
    "the step — the extra &minus;d is slack you can spend.",
    "This is a general and genuinely non-obvious proof technique, not a trick "
    "specific to recurrences. It recurs in Module 09 and throughout "
    "CSCE 627."]),

  ("h1", "6 &nbsp; The classics"),
  ("h2", "6.1 &nbsp; Karatsuba multiplication"),
  ("p", "Multiplying two n-digit numbers naively splits each into halves and "
        "forms four products: T(n) = 4T(n/2) + O(n), which is &Theta;(n&#178;). "
        "No improvement over long multiplication."),
  ("p", "Writing x = a&middot;10^(n/2) + b and y = c&middot;10^(n/2) + d, the "
        "product needs ac, bd, and (ad + bc). Karatsuba's observation is that "
        "the middle term can be recovered from a third product:"),
  ("eq", "ad + bc = (a+b)(c+d) &minus; ac &minus; bd"),
  ("p", "So three multiplications suffice, with additions and subtractions "
        "that cost only O(n):"),
  ("eq", "T(n) = 3T(n/2) + O(n) = &Theta;(n<super>log&#8322;3</super>) = &Theta;(n<super>1.585</super>)"),
  ("callout", "Why removing one call changes the exponent",
   ["The exponent is log<sub>b</sub> a — the number of subproblems sits "
    "inside a logarithm. Going from 4 subproblems to 3 moves the exponent "
    "from log&#8322;4 = 2 to log&#8322;3 &asymp; 1.585.",
    "Strassen's algorithm is the same idea applied to matrix multiplication: "
    "eight half-size products reduced to seven by a similar algebraic "
    "identity, giving &Theta;(n<super>log&#8322;7</super>) = "
    "&Theta;(n<super>2.807</super>).",
    "Both are practical only above a crossover size — the constant "
    "factors and the numerical stability are worse — but the idea that "
    "<i>algebra can change an exponent</i> is one of the genuinely surprising "
    "results in the subject."]),
  ("h2", "6.2 &nbsp; Closest pair of points"),
  ("p", "Given n points in the plane, find the closest pair. Brute force is "
        "&Theta;(n&#178;). Divide and conquer gives &Theta;(n log n), and the "
        "entire difficulty is in the combine."),
  ("p", "Split by a vertical line, recurse on each half, and let d be the "
        "smaller of the two results. A closer pair, if one exists, must "
        "straddle the line, so both of its points lie within distance d of "
        "it — in a vertical strip of width 2d. The strip may contain all "
        "n points, so scanning it pairwise would be &Theta;(n&#178;) and the "
        "whole approach would collapse."),
  ("callout", "The geometric fact that saves it",
   ["Sort the strip by y. For any point p, only points within d in y can "
    "matter, so consider a d &times; 2d rectangle.",
    "Each half of that rectangle is a d/2 &times; d square... and any two "
    "points in the <i>same</i> half were already at distance &ge; d from each "
    "other, since they came from the same recursive call. A square of side "
    "d/2 cannot contain two points &ge; d apart beyond a fixed number.",
    "The conclusion is that at most a constant number of later points — "
    "seven suffices — can be within d of p. The inner loop is O(1), the "
    "strip scan is O(n), and the recurrence becomes T(n) = 2T(n/2) + O(n) = "
    "&Theta;(n log n).",
    "A purely geometric observation is what makes the complexity work. This "
    "is the module's best illustration that combine is where the thinking "
    "happens."]),

  ("h1", "7 &nbsp; When to reach for it"),
  ("table", ["Signal", "Verdict"],
   [["Subproblems are independent and combine is cheap",
     "<b>Use it.</b> This is the ideal case."],
    ["Algebra can reduce the subproblem count",
     "<b>Use it.</b> Karatsuba, Strassen, FFT."],
    ["Subproblems <i>overlap</i> — the same subproblem recurs",
     "<b>Do not.</b> You will recompute exponentially. This is the dynamic "
     "programming signal (Module 10)."],
    ["Combine costs as much as solving directly",
     "<b>Do not.</b> The recursion has bought nothing."],
    ["You need parallelism or cache efficiency",
     "<b>Consider it anyway.</b> Independent subproblems parallelise "
     "trivially, and shrinking subproblems eventually fit in cache without "
     "being tuned for it — the basis of cache-oblivious algorithms."]],
   [0.42, 0.58]),
 ],
 "resources": [
   ("MIT 6.046J — Divide and Conquer, Master Theorem",
    "https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/",
    "The master theorem derived from the recursion tree rather than stated, "
    "plus Strassen and closest-pair."),
   ("MIT 6.006 Lecture — Divide and Conquer",
    "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
    "Gentler treatment with more worked recurrences."),
   ("Jeff Erickson, Algorithms — Chapter 1 (Recursion)",
    "https://jeffe.cs.illinois.edu/teaching/algorithms/",
    "The best written treatment of recursion trees, with unusually good "
    "exercises."),
   ("Tim Roughgarden — Karatsuba and the Master Method",
    "https://www.algorithmsilluminated.org/",
    "Part 1 covers both at an unhurried pace, with the intuition for why the "
    "three cases exist."),
 ],
 "exercises": [
   "Solve by recursion tree, then check with the master theorem: "
   "T(n) = 3T(n/2) + n; T(n) = 2T(n/4) + &radic;n; T(n) = 7T(n/3) + n&#178;.",
   "Solve T(n) = T(n/3) + T(2n/3) + n by drawing the tree. The master theorem "
   "does not apply. Explain why the answer is &Theta;(n log n) despite the "
   "imbalance.",
   "Prove T(n) = 2T(n/2) + 1 is O(n) by substitution. First try the guess "
   "T(n) &le; cn and show where it fails; then strengthen to cn &minus; d.",
   "Implement Karatsuba for big integers and measure it against schoolbook "
   "multiplication. Find the crossover size and explain why it is not 2.",
   "Implement closest-pair in O(n log n). Then deliberately remove the "
   "constant bound on the strip scan and measure both versions, confirming "
   "the second is quadratic.",
   "Implement mergesort with a cutoff to insertion sort below size k. Tune k "
   "by measurement and explain the optimum in terms of Module 01's discussion "
   "of n&#8320; and constant factors.",
 ],
 "selfcheck": [
   "Which of the three steps carries the design effort, and why?",
   "What do a, b, and f(n) represent? Give them for binary search, mergesort, "
   "and Strassen.",
   "Derive the leaf count n<super>log<sub>b</sub>a</super> from the recursion "
   "tree.",
   "State the three master-theorem cases as a single comparison, and give one "
   "recurrence for which it does not apply.",
   "Why can strengthening an induction hypothesis make a proof succeed where "
   "the weaker one fails?",
   "Karatsuba replaces four multiplications with three. Why does that change "
   "the <i>exponent</i> rather than just the constant?",
   "What property of a problem tells you divide and conquer is the wrong "
   "technique, and what is the right one?",
 ],
},

]

# --- additional module batches ----------------------------------------------
for _b in ("c629_b2", "c629_b3", "c629_b4"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
