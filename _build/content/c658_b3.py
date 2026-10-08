# -*- coding: utf-8 -*-
"""CSCE 658 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Randomised Rounding",
 "subtitle": "Turning a fractional solution into a real one.",
 "question": "What do you do with an answer of 0.37?",
 "outcomes": [
     "Explain randomised rounding and why it analyses cleanly.",
     "Derive the set cover guarantee.",
     "Explain how feasibility is restored.",
     "Explain dependent rounding and when it is needed.",
     "Apply rounding to a problem of your own.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The technique",
   "blurb": "Treat the fraction as a probability."},

  {"t": "callout", "title": "A fractional value is a probability, and that makes the analysis one line",
   "kind": "The technique",
   "body": ["<b>Solve the linear programming relaxation, then include "
            "each item independently with probability equal to its "
            "fractional value.</b>",
            "<b>The expected cost is exactly the LP value</b>, by "
            "linearity of expectation (Module 07 §1) — "
            "<b>which is why this analyses so cleanly:</b> no "
            "independence is needed for the cost bound.",
            "<b>And the LP value is a lower bound on the optimum</b> "
            "(CSCE 669 §04) — <b>so the expected cost is at "
            "most the optimum</b>, which is the whole "
            "approximation-analysis mechanism.",
            "<b>Feasibility, however, holds only in expectation</b> "
            "— and <b>restoring it is where the approximation factor "
            "comes from</b> (Part 2). <b>The cost analysis is free and "
            "the feasibility analysis is the work.</b>"]},

  {"t": "code", "kicker": "Set cover", "title": "The guarantee, derived",
   "lang": "text", "code": """
  SET COVER: cover every element with the fewest sets.
  LP relaxation gives a fractional x_S per set.

  ROUND: include set S with probability x_S, independently.

  COST: E[cost] = sum_S c_S * x_S = the LP value. Done.

  COVERAGE: for an element e covered fractionally to 1,
      P(e uncovered) = prod_{S containing e} (1 - x_S)
                    <= exp(-sum x_S) = e^-1
  because 1 - z <= e^-z and the fractional coverage is
  at least 1.

  So each element is covered with probability 1 - 1/e.
  Not good enough -- some elements will be uncovered.

  THE FIX: repeat the rounding ln(4n) times independently
  and take the union of all chosen sets.
      P(e uncovered after k rounds) <= e^-k
      Set k = ln(4n): P(any e uncovered) <= n/4n = 1/4
          by the union bound (Module 02 Part 3).
      And E[cost] = k * LP = O(log n) * OPT.

  SO: an O(log n)-approximation, which CSCE 669 Module 10
  said was OPTIMAL (CSCE 637 Module 11). The trivial
  algorithm is the best one.
""",
   "caption": "<b>Repeat-and-union is the standard way to turn "
              "expected feasibility into actual feasibility</b>, and the "
              "cost of the repetition is the approximation factor.",
   "note": "This derivation is the module's core; walk it slowly."},

  {"t": "section", "label": "Part 2", "title": "Restoring feasibility",
   "blurb": "Four ways, and the choice sets the ratio."},

  {"t": "table", "kicker": "Feasibility", "title": "How to fix a solution that is only feasible in expectation",
   "header": ["Method", "How", "Cost"],
   "widths": [2.6, 4.2, 5.2],
   "rows": [
     ["<b>Repeat and union</b>", "<b>Round several times, take the union</b>", "<b>A log n factor. Set cover</b>"],
     ["<b>Scale up first</b>", "<b>Round with probability min(1, αx)</b>", "<b>A factor of α</b>"],
     ["<b>Repair afterwards</b>", "<b>Fix violations greedily</b>", "<b>Bound the repair cost separately</b>"],
     ["<b>Condition</b>", "<b>Round sequentially, conditioning on feasibility</b>", "<b>Harder to analyse; tighter</b>"],
     ["<b>Dependent rounding</b>", "<b>Preserve constraints exactly during rounding</b>", "<b>Part 3. The best when it applies</b>"],
   ],
   "footnote": "<b>Scale-up is the simplest and is usually tried "
               "first</b> — round with probability "
               "min(1, αxₛ) for a suitable α, which "
               "multiplies both the cost and the coverage probability.",
   "note": "Students need the menu; the techniques are otherwise ad hoc."},

  {"t": "callout", "title": "Why the LP bound is what makes any of this work",
   "kind": "The connection to CSCE 669",
   "body": ["<b>The approximation ratio is proved against the LP value, "
            "not against the optimum</b> — which you cannot "
            "compute.",
            "<b>And the LP value bounds the optimum by weak "
            "duality</b> (CSCE 669 §04 §1), so a ratio "
            "against the LP is a ratio against the optimum.",
            "<b>Which means the <i>integrality gap</i> limits what any "
            "rounding can achieve</b> "
            "(CSCE 669 §10 §2) — <b>set cover's LP has "
            "a logarithmic gap, so no rounding of it beats "
            "log n.</b>",
            "<b>So the first question about a rounding scheme is the "
            "integrality gap of the relaxation</b> — <b>it tells you "
            "the best ratio available before you design the rounding, and "
            "a better ratio needs a stronger relaxation.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Dependent rounding",
   "blurb": "When independence breaks the constraints."},

  {"t": "callout", "title": "Dependent rounding preserves constraints exactly while keeping the marginals",
   "kind": "The refinement",
   "body": ["<b>Independent rounding of a constraint like 'choose "
            "exactly k items' will almost never choose exactly k.</b> "
            "<b>So independence is sometimes the problem rather than the "
            "tool.</b>",
            "<b>Dependent rounding: pick two fractional variables, move "
            "them in opposite directions until one hits 0 or 1, "
            "preserving their sum.</b> Repeat until all are "
            "integral.",
            "<b>Each variable's marginal probability is preserved</b> "
            "— so the expected-cost analysis still works — "
            "<b>and the sum constraint is satisfied exactly.</b>",
            "<b>And the variables become <i>negatively "
            "correlated</i></b>, which means <b>Chernoff bounds still "
            "apply</b> (Module 02 §2's negative association) "
            "— so you keep the concentration as well as the "
            "feasibility."]},

  {"t": "section", "label": "Part 4", "title": "Using it",
   "blurb": "The procedure, and where it applies."},

  {"t": "bullets", "kicker": "Procedure", "title": "Applying randomised rounding to a new problem",
   "items": [
     "<b>1 · Write the integer program</b>, then relax the "
     "integrality (CSCE 669 §09).",
     "",
     "<b>2 · Compute the integrality gap</b>, or look it up. "
     "<b>It bounds what you can achieve.</b>",
     "",
     "<b>3 · Round independently</b> and compute the expected cost "
     "by linearity. <b>One line.</b>",
     "",
     "<b>4 · Check feasibility</b> and choose a repair from "
     "Part 2's menu. <b>This is the work.</b>",
     "",
     "<b>5 · And if a constraint must hold exactly, use dependent "
     "rounding</b> (Part 3).",
   ],
   "footnote": "<b>Step 2 is the one to do first and the one most "
               "often skipped</b> — it tells you the best achievable "
               "ratio before you invest in the rounding scheme."},

  {"t": "callout", "title": "Where rounding is used in practice",
   "kind": "The applications",
   "body": ["<b>Facility location, scheduling, and network design</b> "
            "— the classical approximation applications, and the "
            "ratios are frequently the best known.",
            "<b>Ad allocation and matching.</b> <b>Dependent rounding "
            "of an LP is how large-scale ad serving allocates "
            "impressions</b>, because the budget constraints must hold "
            "exactly.",
            "<b>Routing and load balancing</b>, where the fractional "
            "solution is a flow and the rounding produces integral "
            "paths.",
            "<b>And inside integer programming solvers</b> — "
            "<b>rounding heuristics are how a solver finds an early "
            "incumbent</b> (CSCE 669 §09 §1), which is what "
            "makes the pruning work."]},
 ],
 "takeaways": [
   "A fractional value is a probability, and the expected cost is exactly "
   "the LP value by linearity — so the cost analysis needs no "
   "independence.",
   "The ratio is proved against the LP value, which bounds the optimum by "
   "weak duality.",
   "So the integrality gap limits what any rounding can achieve, and it is "
   "the first thing to compute.",
   "Set cover's derivation gives O(log n) by repeat-and-union, and that is "
   "provably optimal — the trivial algorithm is the best one.",
   "Feasibility holds only in expectation, and restoring it is where the "
   "approximation factor comes from.",
   "Dependent rounding preserves constraints exactly while keeping "
   "marginals and negative correlation, so Chernoff still applies.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The technique"),
  ("callout", "A fractional value is a probability, and that makes the "
              "analysis one line",
   ["<b>Solve the linear programming relaxation of the integer program, "
    "then include each item independently with probability equal to its "
    "fractional value.</b> That is the whole method, and it is almost too "
    "simple to be a technique.",
    "<b>The expected cost is exactly the LP value</b>, by linearity of "
    "expectation (Module 07 &sect;1) — <b>which is why this "
    "analyses so cleanly: no independence assumption is needed for the "
    "cost bound at all</b>, only for the feasibility analysis.",
    "<b>And the LP value is a lower bound on the integer optimum</b>, "
    "because the relaxation admits every integral solution "
    "(CSCE 669 Module 04 &sect;1's weak duality) — <b>so the "
    "expected cost is at most the optimum</b>, which is the entire "
    "mechanism of approximation analysis (CSCE 669 Module 10 "
    "&sect;1).",
    "<b>Feasibility, however, holds only in expectation</b> — the "
    "rounded solution may violate constraints — and <b>restoring it "
    "is where the approximation factor comes from</b> (&sect;2). <b>The "
    "cost analysis is free and the feasibility analysis is the work</b>, "
    "which is the right expectation to have before starting."]),
  ("code", """SET COVER: cover every element with the fewest sets.
The LP relaxation gives a fractional x_S for each set.

ROUND: include set S with probability x_S, independently.

COST: E[cost] = sum_S c_S * x_S = exactly the LP value.
Done, by linearity.

COVERAGE: for an element e whose fractional coverage is at
least 1,
    P(e uncovered) = prod over S containing e of (1 - x_S)
                  <= exp(- sum of x_S)
                  <= e^-1
using 1 - z <= e^-z and the fact that the fractional
coverage sums to at least 1.

So each element is covered with probability 1 - 1/e.
NOT GOOD ENOUGH -- a constant fraction of elements will be
left uncovered.

THE FIX: repeat the whole rounding ln(4n) times
independently and take the UNION of all chosen sets.
    P(e uncovered after k rounds) <= e^-k
    Set k = ln(4n): P(ANY element uncovered) <= n/(4n)
        = 1/4, by the union bound (Module 02 section 3).
    And E[cost] = k * LP = O(log n) * OPT.

SO: an O(log n)-approximation -- which CSCE 669 Module 10
and CSCE 637 Module 11 both say is OPTIMAL. The trivial
algorithm is the best one."""),

  ("h1", "2 &nbsp; Restoring feasibility"),
  ("table", ["Method", "How it works", "What it costs"],
   [["<b>Repeat and union</b>",
     "<b>Round several times independently and take the union of the "
     "selections.</b>",
     "<b>A logarithmic factor in the cost.</b> Set cover (&sect;1)."],
    ["<b>Scale up first</b>",
     "<b>Round with probability min(1, &alpha;x) for some "
     "&alpha; &gt; 1.</b>",
     "<b>A factor of &alpha; in the cost</b>, and it improves the "
     "feasibility probability correspondingly. <b>The simplest, and "
     "usually tried first.</b>"],
    ["<b>Repair afterwards</b>",
     "<b>Round, then greedily fix whatever constraints are "
     "violated.</b>",
     "<b>Bound the repair cost separately</b>, which is sometimes easy "
     "and sometimes the whole difficulty."],
    ["<b>Conditioning</b>",
     "<b>Round variables one at a time, conditioning each choice on the "
     "remaining feasibility.</b>",
     "<b>Harder to analyse and frequently gives a tighter ratio</b> "
     "— and it is also the route to derandomisation "
     "(Module 12 &sect;1)."],
    ["<b>Dependent rounding</b>",
     "<b>Round in a way that preserves the constraints exactly "
     "throughout.</b>", "<b>&sect;3. The best option when it "
     "applies.</b>"]],
   [0.21, 0.36, 0.43]),
  ("callout", "Why the LP bound is what makes any of this work",
   ["<b>The approximation ratio is proved against the LP value rather "
    "than against the optimum</b> — which you cannot compute, since "
    "computing it is the NP-hard problem you are avoiding.",
    "<b>And the LP value bounds the optimum by weak duality</b> "
    "(CSCE 669 Module 04 &sect;1), <b>so a ratio established against "
    "the LP is automatically a ratio against the optimum.</b>",
    "<b>Which means the <i>integrality gap</i> of the relaxation limits "
    "what any rounding scheme can possibly achieve</b> (CSCE 669 "
    "Module 10 &sect;2) — <b>set cover's LP has a logarithmic "
    "integrality gap, so no rounding of that LP can beat "
    "O(log n)</b>, however clever.",
    "<b>So the first question about a rounding scheme is the integrality "
    "gap of the relaxation</b> — <b>it tells you the best ratio "
    "available before you design anything, and beating it requires a "
    "stronger relaxation rather than a better rounding</b> (a "
    "semidefinite one, or additional valid inequalities, which is "
    "CSCE 669 Module 09's formulation strength)."]),

  ("break",),
  ("h1", "3 &nbsp; Dependent rounding"),
  ("callout", "Dependent rounding preserves constraints exactly while "
              "keeping the marginals",
   ["<b>Independent rounding of a constraint like 'choose exactly k "
    "items' will essentially never choose exactly k</b> — the count "
    "is a binomial variable, concentrated near k and almost never equal "
    "to it. <b>So independence is sometimes the problem rather than the "
    "tool.</b>",
    "<b>Dependent rounding: pick two fractional variables, move one up "
    "and the other down by the same amount until one of them reaches 0 or "
    "1, preserving their sum.</b> Repeat until every variable is "
    "integral.",
    "<b>Each variable's marginal probability of ending at 1 is exactly "
    "its original fractional value</b> — so <b>the expected-cost "
    "analysis of &sect;1 still works unchanged</b> — <b>and the sum "
    "constraint is satisfied exactly rather than in expectation.</b>",
    "<b>And the variables become <i>negatively correlated</i> rather "
    "than independent</b>, which means <b>Chernoff bounds still "
    "apply</b> (Module 02 &sect;2's negative association fallback) "
    "— <b>so you keep the concentration as well as the "
    "feasibility.</b> <b>That is the property that makes the technique "
    "genuinely useful rather than merely feasible</b>, and it is why ad "
    "allocation systems use it (&sect;4)."]),

  ("h1", "4 &nbsp; Using it"),
  ("ul", ["<b>1 &middot; Write the integer program</b>, then relax the "
          "integrality constraints (CSCE 669 Module 09 &sect;1).",
          "<b>2 &middot; Compute the integrality gap, or look it "
          "up.</b> <b>It bounds what you can achieve</b> — and "
          "<b>this is the step to do first and the one most often "
          "skipped</b>, because it can tell you that your intended "
          "improvement is impossible.",
          "<b>3 &middot; Round independently and compute the expected "
          "cost by linearity.</b> <b>One line</b>, and it will equal the "
          "LP value.",
          "<b>4 &middot; Check feasibility and choose a repair from "
          "&sect;2's menu.</b> <b>This is the work</b>, and the choice "
          "determines the approximation factor.",
          "<b>5 &middot; And if a constraint must hold exactly rather "
          "than approximately, use dependent rounding</b> (&sect;3) "
          "— which is usually the case for budget, capacity, and "
          "cardinality constraints in a real system."]),
  ("callout", "Where rounding is used in practice",
   ["<b>Facility location, scheduling, and network design</b> — the "
    "classical approximation applications, and <b>the ratios obtained by "
    "LP rounding are frequently the best known</b> for these problems.",
    "<b>Ad allocation and matching.</b> <b>Dependent rounding of a "
    "linear program is how large-scale ad serving allocates impressions "
    "to advertisers</b>, <b>because the budget constraints must hold "
    "exactly</b> — you cannot overspend a budget in expectation.",
    "<b>Routing and load balancing</b>, where the fractional solution is "
    "a flow (CSCE 669 Module 11 &sect;1) and the rounding produces "
    "integral paths — which is how multi-commodity routing is "
    "approximated.",
    "<b>And inside integer programming solvers themselves</b> — "
    "<b>rounding heuristics are how a solver finds an early incumbent "
    "solution</b> (CSCE 669 Module 09 &sect;1), <b>which is what "
    "makes branch-and-bound's pruning effective at all.</b> So the "
    "technique is both an approximation method and a component of exact "
    "solvers, which is unusual."]),
 ],
 "resources": [
   ("Williamson & Shmoys &mdash; chapters 1 and 5 (free PDF)",
    "https://www.designofapproxalgs.com/",
    "<b>Randomised rounding, free in full</b> — the set cover "
    "derivation of &sect;1 and the feasibility methods of &sect;2."),
   ("Raghavan & Thompson &mdash; Randomized Rounding (free)",
    "https://link.springer.com/article/10.1007/BF02579324",
    "<b>The originating paper</b>, in the routing setting of &sect;4."),
   ("Gandhi, Khuller, Parthasarathy & Srinivasan &mdash; Dependent "
    "Rounding (free)",
    "https://dl.acm.org/doi/10.1145/1147954.1147956",
    "<b>&sect;3's technique</b>, with the negative correlation proved."),
   ("Motwani & Raghavan &mdash; chapter 4",
    "https://www.cambridge.org/core/books/randomized-algorithms/6A3E5CD760413BEF7D0D01BFD5497ACB",
    "<b>The same material from the randomised-algorithms side</b>, with "
    "the Chernoff analysis explicit."),
 ],
 "exercises": [
   "<b>Solve a set cover LP</b> and round it independently. Report the "
   "cost and how many elements were uncovered.",
   "<b>Implement the repeat-and-union fix</b> and verify the "
   "O(log n) cost and the coverage.",
   "<b>Measure the achieved ratio</b> against the LP bound on random "
   "instances.",
   "<b>Compute the integrality gap</b> of the set cover LP on a small "
   "instance.",
   "<b>Implement scale-up rounding</b> and plot the ratio against "
   "α.",
   "<b>Round a 'choose exactly k' constraint independently</b> and report "
   "how often you get exactly k.",
   "<b>Implement dependent rounding</b> and confirm the constraint holds "
   "exactly and the marginals are preserved.",
   "<b>Verify the negative correlation</b> empirically.",
   "<b>Apply the five-step procedure</b> to a problem of your own.",
   "<b>Compare your rounded solution against a solver's exact answer</b> "
   "on instances small enough to solve.",
 ],
 "selfcheck": [
   "Explain randomised rounding and why the cost analysis needs no "
   "independence.",
   "Why is the ratio proved against the LP rather than the optimum?",
   "Derive the set cover guarantee in full.",
   "Why is the repeat-and-union step needed, and what does it cost?",
   "Name five ways to restore feasibility.",
   "What limits any rounding of a given LP, and what is needed to beat "
   "it?",
   "Why is independent rounding wrong for an exact cardinality "
   "constraint?",
   "Describe dependent rounding and name its three preserved "
   "properties.",
   "Give the five-step procedure and say which step comes first.",
   "Name four practical applications.",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Markov Chains and Mixing",
 "subtitle": "Random walks, and how long until they forget.",
 "question": "How long must a random process run before its state is "
             "representative?",
 "outcomes": [
     "Define a Markov chain and its stationary distribution.",
     "Explain mixing time and why it is the quantity of interest.",
     "Explain the spectral gap and conductance bounds.",
     "Explain MCMC and the Metropolis–Hastings construction.",
     "Diagnose a chain that is not mixing.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Chains and stationarity",
   "blurb": "Where a random walk ends up."},

  {"t": "callout", "title": "An irreducible aperiodic chain converges to a unique stationary distribution",
   "kind": "The fundamental theorem",
   "body": ["<b>A Markov chain's next state depends only on the "
            "current one</b> (CSCE 625 §10 §1's property, "
            "without actions or rewards).",
            "<b>If it is <i>irreducible</i> (every state reachable from "
            "every other) and <i>aperiodic</i> (no forced cycle), it has "
            "a unique stationary distribution π and converges to "
            "it from any start.</b>",
            "<b>And for a random walk on a graph, "
            "π(v) ∝ deg(v)</b> — which is both simple "
            "and immediately useful: <b>a random walk spends time "
            "proportional to degree.</b>",
            "<b>So the question is never <i>whether</i> it converges "
            "but <i>how fast</i></b> — <b>which is the mixing time, "
            "and it is the only quantity that matters for an "
            "algorithm.</b>"]},

  {"t": "callout", "title": "Mixing time is the quantity, and it can be anything",
   "kind": "Why the theorem alone is useless",
   "body": ["<b>Mixing time is the number of steps until the "
            "distribution is within ε of π in total "
            "variation distance.</b>",
            "<b>And it varies enormously:</b> <b>a complete graph mixes "
            "in O(1) steps, a cycle in Θ(n²), and a "
            "dumbbell (two cliques joined by an edge) in exponential "
            "time.</b>",
            "<b>The dumbbell is the picture to hold:</b> <b>a "
            "bottleneck between two well-connected regions traps the walk "
            "on one side for a very long time</b>, and that is what slow "
            "mixing looks like.",
            "<b>So 'it converges eventually' is not a useful "
            "statement</b> — <b>every MCMC result depends on a mixing "
            "bound, and an unbounded one is an unsupported "
            "result</b> (Module 13)."]},

  {"t": "section", "label": "Part 2", "title": "Bounding the mixing time",
   "blurb": "Two techniques."},

  {"t": "code", "kicker": "Bounds", "title": "Spectral gap and conductance",
   "lang": "text", "code": """
  SPECTRAL GAP: let the transition matrix's eigenvalues be
  1 = l_1 > l_2 >= ... The gap is 1 - l_2.

      mixing time = O( (1/gap) * log(1/eps) )

  So a large gap means fast mixing. Exact, and frequently
  impossible to compute for the chain you have.

  CONDUCTANCE (Cheeger): for a set S, the conductance is
  the probability of leaving S in one step, given you are
  in S under stationarity. Phi is the minimum over S.

      gap >= Phi^2 / 2       (and gap <= 2 Phi)

  So BOUNDING THE WORST BOTTLENECK BOUNDS THE MIXING TIME.
  This is the usable technique: find the tightest cut and
  measure how much probability flows across it.

  THE DUMBBELL AGAIN: the cut between the two cliques has
  tiny conductance, so Phi is tiny, so the gap is tiny, so
  mixing is slow. The geometric picture and the algebraic
  bound agree.

  AND COUPLING is the third technique: run two copies of
  the chain from different starts, show they can be made to
  meet quickly, and the meeting time bounds the mixing
  time. Frequently the easiest in practice.
""",
   "caption": "<b>Conductance is the usable bound</b> — it turns "
              "mixing time into a question about bottlenecks, which you "
              "can reason about geometrically.",
   "note": "Coupling deserves the mention; it is what people actually "
           "use."},

  {"t": "section", "label": "Part 3", "title": "MCMC",
   "blurb": "Sampling from a distribution you cannot write down."},

  {"t": "callout", "title": "Metropolis–Hastings builds a chain with any stationary distribution you want",
   "kind": "The construction",
   "body": ["<b>Given a target π known only up to a "
            "normalising constant, construct a chain converging to "
            "it.</b> <b>The normalising constant is what you cannot "
            "compute, and the construction does not need it.</b>",
            "<b>Propose a move, then accept it with probability "
            "min(1, π(new)/π(old))</b> — <b>a ratio, "
            "in which the normalising constant cancels.</b> That "
            "cancellation is the whole trick.",
            "<b>The resulting chain is reversible with stationary "
            "distribution π</b>, by detailed balance — which "
            "is a two-line verification.",
            "<b>And it is why MCMC is used everywhere:</b> <b>Bayesian "
            "inference, statistical physics, and CSCE 647's path-space "
            "light transport all sample distributions known only up to a "
            "constant.</b>"]},

  {"t": "bullets", "kicker": "Uses", "title": "Where MCMC appears in this program",
   "items": [
     "<b>Bayesian posterior sampling</b> (CSCE 633 §09) "
     "— the posterior is known up to the evidence, which is "
     "exactly the intractable constant.",
     "",
     "<b>Metropolis light transport</b> (CSCE 647) — sampling "
     "light paths in proportion to their contribution, which cannot be "
     "normalised.",
     "",
     "<b>Simulated annealing</b> (CSCE 669 §13) — a "
     "Metropolis chain with a temperature schedule.",
     "",
     "<b>Approximate counting</b> — <b>counting perfect matchings "
     "or graph colourings reduces to sampling them</b>, which is a "
     "deep and useful connection.",
     "",
     "<b>And statistical physics</b>, where the method originated and "
     "where the partition function is the uncomputable constant.",
   ],
   "footnote": "<b>The counting-to-sampling reduction is the "
               "theoretically deepest item</b> — approximate "
               "counting and approximate sampling are equivalent for "
               "self-reducible problems, which is Jerrum and Sinclair's "
               "result."},

  {"t": "section", "label": "Part 4", "title": "Diagnosis",
   "blurb": "When your chain is not mixing."},

  {"t": "callout", "title": "An unmixed chain produces confident, wrong answers",
   "kind": "The failure mode",
   "body": ["<b>A chain that has not mixed returns samples from "
            "whatever region it started in</b> — which look like "
            "samples, have a mean and a variance, and are "
            "wrong.",
            "<b>And there is no internal signal.</b> <b>The chain does "
            "not know it has not mixed</b>, which is "
            "CSCE 625 §09 §3's warning in its most "
            "practical form.",
            "<b>So the diagnostics are all external:</b> <b>run "
            "multiple chains from different starts and compare; compute "
            "the autocorrelation; monitor the effective sample size; "
            "check the Gelman–Rubin statistic.</b>",
            "<b>And the fix is usually a better proposal rather than a "
            "longer run</b> — <b>if the chain has a bottleneck, "
            "running it ten times longer does not help</b>, and a "
            "proposal that crosses the bottleneck does."]},

  {"t": "bullets", "kicker": "Practice", "title": "Running MCMC responsibly",
   "items": [
     "<b>Run at least four chains from different "
     "initialisations</b>, always. <b>Agreement between chains is the "
     "only real evidence of mixing.</b>",
     "",
     "<b>Report the effective sample size</b>, not the number of "
     "iterations — <b>a million correlated samples may be worth "
     "fifty independent ones.</b>",
     "",
     "<b>Discard a burn-in period</b>, and be honest that the length "
     "is a guess.",
     "",
     "<b>Tune the proposal.</b> <b>Acceptance rates near 0.234 are "
     "optimal for random-walk Metropolis in high dimensions</b> "
     "— a genuinely useful constant.",
     "",
     "<b>And prefer a better algorithm when one exists</b> — "
     "<b>Hamiltonian Monte Carlo and its variants mix far better in high "
     "dimensions</b> (CSCE 633).",
   ],
   "footnote": "<b>'Four chains and the effective sample size' is the "
               "minimum reporting standard</b>, and it is directly "
               "analogous to CSCE 642 §12's five seeds."},
 ],
 "takeaways": [
   "An irreducible aperiodic chain converges to a unique stationary "
   "distribution, and for a random walk on a graph it is proportional to "
   "degree.",
   "The question is never whether it converges but how fast — and "
   "mixing time ranges from O(1) to exponential.",
   "The dumbbell graph is the picture of slow mixing: a bottleneck between "
   "two well-connected regions.",
   "Conductance turns mixing time into a question about the worst "
   "bottleneck, which is the usable bound; coupling is the easiest in "
   "practice.",
   "Metropolis–Hastings works because the acceptance ratio cancels "
   "the normalising constant you cannot compute.",
   "An unmixed chain produces confident wrong answers with no internal "
   "signal, so all diagnostics are external — four chains, minimum.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Chains, stationarity, and mixing"),
  ("callout", "An irreducible aperiodic chain converges to a unique "
              "stationary distribution",
   ["<b>A Markov chain's next state depends only on the current state</b> "
    "— CSCE 625 Module 10 &sect;1's Markov property, without "
    "the actions and rewards that made it a decision process.",
    "<b>If the chain is <i>irreducible</i> (every state is reachable "
    "from every other) and <i>aperiodic</i> (there is no forced cycle "
    "length), then it has a unique stationary distribution &pi; and "
    "converges to it from any starting state.</b> That is the "
    "fundamental theorem, and both conditions are easy to check.",
    "<b>And for a simple random walk on an undirected graph, &pi;(v) is "
    "proportional to the degree of v</b> — which is both simple to "
    "state and immediately useful: <b>a random walk spends time "
    "proportional to degree</b>, which is why PageRank needed a damping "
    "term and why degree-biased sampling is a hazard in network "
    "crawling.",
    "<b>So the question is never <i>whether</i> the chain converges but "
    "<i>how fast</i></b> — <b>which is the mixing time, and it is "
    "the only quantity that matters for an algorithm built on the "
    "chain.</b>"]),
  ("callout", "Mixing time is the quantity, and it can be anything",
   ["<b>The mixing time is the number of steps until the chain's "
    "distribution is within &epsilon; of &pi; in total variation "
    "distance</b>, from the worst starting state.",
    "<b>And it varies enormously between chains:</b> <b>a random walk on "
    "a complete graph mixes in O(1) steps; on a cycle it takes "
    "&Theta;(n&#178;); and on a dumbbell — two cliques joined by a "
    "single edge — it takes exponential time.</b>",
    "<b>The dumbbell is the picture to hold.</b> <b>A bottleneck between "
    "two well-connected regions traps the walk on one side for a very long "
    "time</b>, because escaping requires finding one particular edge "
    "among many. <b>That is what slow mixing looks like geometrically</b>, "
    "and &sect;2's conductance bound makes the picture quantitative.",
    "<b>So 'it converges eventually' is not a useful statement.</b> "
    "<b>Every MCMC-based result depends on a mixing bound, and an "
    "unbounded one is an unsupported result</b> (Module 13 &sect;1) "
    "— which is a real and widespread problem in applied Bayesian "
    "work, where the mixing time is typically unknown and the "
    "diagnostics of &sect;4 are the only available substitute."]),

  ("h1", "2 &nbsp; Bounding the mixing time"),
  ("code", """SPECTRAL GAP: let the transition matrix's eigenvalues be
1 = l_1 > l_2 >= ... The spectral gap is 1 - l_2.

    mixing time = O( (1/gap) * log(1/eps) )

So a large gap means fast mixing. Exact, and frequently
impossible to compute for the chain you actually have.

CONDUCTANCE (Cheeger's inequality): for a set S of states,
the conductance of S is the probability of leaving S in one
step, given that you are in S under stationarity. Phi is
the minimum of that over all S with stationary measure at
most 1/2.

    gap >= Phi^2 / 2        (and gap <= 2 Phi)

So BOUNDING THE WORST BOTTLENECK BOUNDS THE MIXING TIME.
This is the usable technique: find the tightest cut in the
state space and measure how much probability flows across
it.

THE DUMBBELL AGAIN: the cut between the two cliques has
tiny conductance, so Phi is tiny, so the gap is tiny, so
mixing is slow. The geometric picture and the algebraic
bound agree exactly.

AND COUPLING is the third technique: run two copies of the
chain from different starting states, show they can be
coupled so as to meet quickly, and the meeting time bounds
the mixing time. Frequently the easiest in practice."""),
  ("p", "<b>Conductance is the usable bound of the three</b> — "
        "<b>it turns mixing time into a question about bottlenecks, which "
        "you can reason about geometrically and frequently answer by "
        "inspection.</b> <b>And coupling deserves its mention: it is "
        "what people actually use</b> to prove mixing for specific chains, "
        "because exhibiting a coupling is often far easier than estimating "
        "either eigenvalues or the minimum conductance over all cuts."),

  ("break",),
  ("h1", "3 &nbsp; Markov chain Monte Carlo"),
  ("callout", "Metropolis–Hastings builds a chain with any stationary "
              "distribution you want",
   ["<b>Given a target distribution &pi; known only up to a normalising "
    "constant, construct a Markov chain that converges to it.</b> <b>The "
    "normalising constant is precisely what you cannot compute</b> "
    "— it is an integral over the whole space — <b>and the "
    "construction does not need it.</b>",
    "<b>Propose a move from the current state, then accept it with "
    "probability min(1, &pi;(new)/&pi;(old))</b> (times a proposal "
    "correction if the proposal is asymmetric) — <b>and that is a "
    "<i>ratio</i>, in which the normalising constant cancels.</b> "
    "<b>That cancellation is the whole trick, and it is why the method "
    "exists.</b>",
    "<b>The resulting chain is reversible with stationary distribution "
    "&pi;</b>, which follows from detailed balance and is a two-line "
    "verification — worth doing once.",
    "<b>And it is why MCMC is used everywhere:</b> <b>Bayesian posterior "
    "inference, statistical physics, and CSCE 647's path-space light "
    "transport all involve sampling from distributions known only up to a "
    "constant.</b> <b>The pattern is general:</b> whenever you can "
    "evaluate a density up to proportionality and cannot normalise it, "
    "Metropolis–Hastings applies."]),
  ("ul", ["<b>Bayesian posterior sampling</b> (CSCE 633 "
          "Module 09) — <b>the posterior is known up to the "
          "evidence, which is exactly the intractable normalising "
          "constant</b>, so this is the canonical application.",
          "<b>Metropolis light transport</b> (CSCE 647) — "
          "sampling light paths in proportion to their contribution to "
          "the image, which cannot be normalised because the total is what "
          "you are trying to compute.",
          "<b>Simulated annealing</b> (CSCE 669 Module 13 "
          "&sect;1) — <b>a Metropolis chain with a temperature "
          "schedule</b>, where the target distribution concentrates on "
          "the optimum as the temperature falls.",
          "<b>Approximate counting.</b> <b>Counting perfect matchings or "
          "proper graph colourings reduces to sampling them nearly "
          "uniformly</b> — a deep and extremely useful connection, "
          "and the route to the only known approximation algorithms for "
          "the permanent.",
          "<b>And statistical physics</b>, where the method originated "
          "in 1953 and where the partition function is the uncomputable "
          "constant. <b>The counting-to-sampling reduction is the "
          "theoretically deepest item in this list</b> — "
          "<b>approximate counting and approximate sampling are "
          "equivalent for self-reducible problems</b>, which is Jerrum, "
          "Valiant and Vazirani's result and is what made approximate "
          "counting a field."]),

  ("h1", "4 &nbsp; Diagnosis"),
  ("callout", "An unmixed chain produces confident, wrong answers",
   ["<b>A chain that has not mixed returns samples from whatever region "
    "of the space it started in</b> — <b>which look exactly like "
    "samples, have a mean and a variance and a tidy histogram, and are "
    "wrong.</b>",
    "<b>And there is no internal signal.</b> <b>The chain does not know "
    "it has not mixed</b>, and nothing in its output indicates the "
    "problem — which is <b>CSCE 625 Module 09 &sect;3's "
    "warning in its most practically consequential form.</b>",
    "<b>So the diagnostics are all external:</b> <b>run multiple chains "
    "from widely different starting points and compare their "
    "distributions; compute the autocorrelation at increasing lags; "
    "monitor the effective sample size; compute the Gelman–Rubin "
    "statistic comparing within-chain and between-chain variance.</b>",
    "<b>And the fix is usually a better proposal rather than a longer "
    "run.</b> <b>If the chain has a conductance bottleneck (&sect;2), "
    "running it ten times longer does not help</b> — the bottleneck "
    "is exponentially hard to cross — <b>and a proposal that can "
    "cross it directly does.</b> <b>Which is why diagnosing slow mixing "
    "as a bottleneck rather than as insufficient patience is the "
    "important distinction.</b>"]),
  ("ul", ["<b>Run at least four chains from different "
          "initialisations</b>, always. <b>Agreement between independently "
          "started chains is the only real evidence of mixing "
          "available</b>, and a single chain is uninformative however long "
          "it ran.",
          "<b>Report the effective sample size rather than the number of "
          "iterations</b> — <b>a million highly correlated samples "
          "may carry the information of fifty independent ones</b>, and "
          "the iteration count is actively misleading.",
          "<b>Discard a burn-in period</b>, and <b>be honest that its "
          "length is a guess</b> informed by the diagnostics rather than "
          "derived from a mixing bound.",
          "<b>Tune the proposal.</b> <b>An acceptance rate near 0.234 "
          "is asymptotically optimal for random-walk Metropolis in high "
          "dimensions</b> — <b>a genuinely useful constant</b>, and a "
          "rate far above or below it indicates a proposal that is too "
          "timid or too bold.",
          "<b>And prefer a better algorithm when one exists</b> — "
          "<b>Hamiltonian Monte Carlo and its adaptive variants mix "
          "dramatically better in high dimensions</b> (CSCE 633) by "
          "using gradient information. <b>'Four chains and the effective "
          "sample size' is the minimum reporting standard</b>, and <b>it "
          "is directly analogous to CSCE 642 Module 12's five "
          "seeds</b> — the same discipline, in a different "
          "stochastic setting."]),
 ],
 "resources": [
   ("Levin & Peres &mdash; Markov Chains and Mixing Times (free PDF)",
    "https://pages.uoregon.edu/dlevin/MARKOV/",
    "<b>Free from the authors, and the definitive treatment</b> — "
    "chapters 1–7 and 12–13 cover &sect;1 and &sect;2, "
    "including coupling."),
   ("Mitzenmacher & Upfal &mdash; chapters 7 and 12",
    "https://www.cambridge.org/core/books/probability-and-computing/7D2016B2EB4B5E5F4F2C4E4F4F4C4E4F",
    "<b>Markov chains and MCMC at this course's level</b>, with the "
    "Metropolis construction derived."),
   ("Gelman et al. &mdash; Bayesian Data Analysis, 3rd edition (free "
    "PDF)",
    "http://www.stat.columbia.edu/~gelman/book/",
    "<b>&sect;4's diagnostics, free in full</b> — including the "
    "Gelman–Rubin statistic and the effective sample size, by their "
    "originators."),
   ("Jerrum & Sinclair &mdash; The Markov chain Monte Carlo method "
    "(free survey)",
    "https://www.cs.berkeley.edu/~sinclair/jerrum-sinclair.pdf",
    "<b>&sect;3's counting-to-sampling connection</b>, and the "
    "conductance method applied to real chains."),
 ],
 "exercises": [
   "<b>Implement a random walk on a graph</b> and verify the stationary "
   "distribution is proportional to degree.",
   "<b>Measure the mixing time empirically</b> for a complete graph, a "
   "cycle, and a dumbbell.",
   "<b>Confirm the dumbbell is exponentially slow</b> by measuring "
   "crossing times.",
   "<b>Compute the spectral gap</b> for a small chain and compare against "
   "the measured mixing time.",
   "<b>Estimate the conductance</b> of the dumbbell's bottleneck cut and "
   "apply Cheeger.",
   "<b>Construct a coupling</b> for a simple chain and bound the mixing "
   "time with it.",
   "<b>Implement Metropolis–Hastings</b> for a distribution you know "
   "only up to a constant.",
   "<b>Verify detailed balance</b> numerically.",
   "<b>Run four chains from different starts</b> and compute the "
   "Gelman–Rubin statistic.",
   "<b>Deliberately under-run a chain</b> and report the wrong answer it "
   "gives confidently.",
 ],
 "selfcheck": [
   "State the fundamental theorem and its two conditions.",
   "What is the stationary distribution of a random walk on a graph, and "
   "what follows?",
   "Define mixing time and give three chains with very different "
   "ones.",
   "Describe the dumbbell and what it illustrates.",
   "Give the spectral gap and conductance bounds, and say which is "
   "usable.",
   "What is coupling, and why is it used in practice?",
   "Explain why Metropolis–Hastings does not need the normalising "
   "constant.",
   "Name five applications of MCMC.",
   "What does the counting-to-sampling reduction establish?",
   "Why are all mixing diagnostics external, and what is the minimum "
   "standard?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Dimension and Sampling",
 "subtitle": "Projecting, hashing, and sampling in high dimensions.",
 "question": "Can you shrink high-dimensional data without losing what "
             "matters?",
 "outcomes": [
     "State the Johnson–Lindenstrauss lemma and its "
     "consequences.",
     "Explain locality-sensitive hashing.",
     "Explain importance sampling and its variance behaviour.",
     "Explain sampling-based matrix approximation.",
     "Choose a technique for a high-dimensional problem.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Johnson–Lindenstrauss",
   "blurb": "Distances survive random projection."},

  {"t": "callout", "title": "Johnson–Lindenstrauss: project to O(log n / ε²) dimensions and keep all pairwise distances",
   "kind": "The result, and why it is remarkable",
   "body": ["<b>For any n points in any dimension, a random linear map "
            "into O(log n / ε²) dimensions preserves all "
            "pairwise distances to within a factor "
            "(1 ± ε), with high "
            "probability.</b>",
            "<b>Note what the target dimension does not depend on:</b> "
            "<b>the original dimension.</b> <b>A million-dimensional "
            "dataset of a thousand points projects to the same number of "
            "dimensions as a thousand-dimensional one.</b>",
            "<b>The proof is Module 02's Chernoff bound plus "
            "Module 02's union bound</b> — each distance is "
            "preserved with probability 1 − 1/n³, and "
            "there are fewer than n² pairs.",
            "<b>And the projection is just a random Gaussian "
            "matrix</b> — <b>no structure, no learning, no data "
            "dependence</b>, which is why it is so widely usable."]},

  {"t": "callout", "title": "What JL does and does not give",
   "kind": "The honest reading",
   "body": ["<b>It preserves <i>pairwise distances</i> among a "
            "<i>specified finite set</i>.</b> <b>Not the geometry of the "
            "whole space, and not distances to new points added "
            "later</b> — though a fresh point works with high "
            "probability.",
            "<b>The ε² in the denominator is "
            "harsh:</b> <b>10% distortion needs about 100 times more "
            "dimensions than 100% distortion</b>, so high accuracy is "
            "expensive.",
            "<b>And it does not preserve inner products as "
            "tightly</b>, nor does it help with anything that depends on "
            "the ambient dimension rather than on distances.",
            "<b>But within its scope it is unimprovable</b> — "
            "<b>the O(log n / ε²) bound is tight</b>, so no "
            "cleverer projection exists."]},

  {"t": "section", "label": "Part 2", "title": "Locality-sensitive hashing",
   "blurb": "Hashing designed to collide."},

  {"t": "code", "kicker": "LSH", "title": "A hash family where similar items collide on purpose",
   "lang": "text", "code": """
  A family H is LOCALITY-SENSITIVE if
      near points collide with probability >= p1
      far points collide with probability <= p2
      with p1 > p2.

  That gap is all you need. Amplify it:
      AND over k hashes -> p1^k vs p2^k
          (widens the ratio, lowers both)
      OR over L such bands -> 1-(1-p1^k)^L vs ...
          (raises both, steepens the transition)

  Tuning k and L gives a sharp step at the distance you
  care about -- which is Module 02's amplification applied
  to a similarity threshold.
""",
   "caption": "<b>Only a gap between near and far is needed</b> "
              "— amplification turns any gap into a step, which is "
              "why so many constructions qualify.",
   "note": "Hold the amplification before the constructions."},

  {"t": "code", "kicker": "Constructions", "title": "And the three families that are used",
   "lang": "text", "code": """
  HAMMING / JACCARD   MinHash: hash each set by the minimum
      of a random permutation of its elements.
      P(collision) = EXACTLY the Jaccard similarity.

  COSINE              random hyperplane: take the sign of
      the dot product with a random Gaussian vector.
      P(collision) = 1 - theta/pi.
      <-- this is CSCE 669 Module 10's Goemans-Williamson
          rounding, used as a hash function.

  EUCLIDEAN           project onto a random line and bucket
      by fixed-width intervals.

  RESULT: sublinear-time approximate nearest-neighbour
  search, with a stated recall.
""",
   "caption": "<b>The random-hyperplane construction is MAX-CUT's "
              "rounding reused as a hash function</b> — the same "
              "geometric fact, in two subjects.",
   "note": "The Goemans-Williamson connection is worth making "
           "explicitly."},

  {"t": "section", "label": "Part 3", "title": "Importance sampling",
   "blurb": "Sample where it matters, and reweight."},

  {"t": "callout", "title": "Importance sampling reweights, and the variance is everything",
   "kind": "The technique and its hazard",
   "body": ["<b>To estimate E_p[f], sample from a different "
            "distribution q and weight each sample by "
            "p(x)/q(x).</b> <b>The estimate is unbiased for any q with "
            "support covering p's.</b>",
            "<b>And the variance depends entirely on how well q matches "
            "the shape of p·f</b> — <b>a good q gives enormous "
            "variance reduction and a bad one gives enormous variance "
            "<i>increase</i>.</b>",
            "<b>The failure mode is a few samples with huge "
            "weights:</b> <b>the estimate becomes dominated by one "
            "sample and the apparent variance collapses while the true "
            "error does not</b> — which is the same silent failure as "
            "Module 09 §4.",
            "<b>So monitor the effective sample size from the "
            "weights</b> — <b>the same diagnostic as "
            "MCMC</b> — and <b>it is CSCE 647 §03's "
            "importance sampling and CSCE 642 §05's policy "
            "gradient, which are both this.</b>"]},

  {"t": "callout", "title": "Sampling for matrix computations",
   "kind": "Where this scales",
   "body": ["<b>Approximate a matrix product by sampling rows and "
            "columns in proportion to their norms</b> — the error "
            "depends on the number of samples and not on the matrix "
            "size.",
            "<b>Which gives randomised low-rank approximation:</b> "
            "<b>a random projection followed by an exact decomposition of "
            "the small result</b>, with a bound on the error relative to "
            "the best rank-k approximation.",
            "<b>And it is far faster than a full SVD</b>, which is why "
            "randomised linear algebra is the standard approach for very "
            "large matrices (CSCE 676).",
            "<b>With the same structural caveat as always:</b> "
            "<b>the error bound is in expectation or with high "
            "probability, and the norms you sample by must be computable "
            "cheaply</b> — which for a streamed matrix they may not "
            "be."]},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "Which technique for which problem."},

  {"t": "table", "kicker": "Choosing", "title": "The high-dimensional toolkit",
   "header": ["Problem", "Technique", "Guarantee"],
   "widths": [3.2, 3.4, 4.5],
   "rows": [
     ["<b>Reduce dimension, keep distances</b>", "<b>Random projection (JL)</b>", "<b>(1±ε) on all pairs</b>"],
     ["<b>Nearest neighbour search</b>", "<b>LSH</b>", "<b>Sublinear time, stated recall</b>"],
     ["<b>Estimate an expectation</b>", "<b>Importance sampling</b>", "<b>Unbiased; variance depends on q</b>"],
     ["<b>Approximate a matrix</b>", "<b>Randomised SVD</b>", "<b>Near-optimal rank-k error</b>"],
     ["<b>Deduplicate or cluster by similarity</b>", "<b>MinHash</b>", "<b>Exact Jaccard in expectation</b>"],
     ["<b>Count distinct</b>", "<b>HyperLogLog</b>", "<b>Module 05 §1</b>"],
   ],
   "footnote": "<b>MinHash is the one with the cleanest guarantee:</b> "
               "<b>the collision probability is exactly the Jaccard "
               "similarity</b>, so the estimate is unbiased with no "
               "approximation at all in the expectation.",
   "note": "This table is the practical output of the module."},

  {"t": "callout", "title": "Why randomness is unavoidable in high dimensions",
   "kind": "Closing the module",
   "body": ["<b>In high dimensions almost everything is almost "
            "orthogonal and almost equidistant</b> — the "
            "concentration of measure, which is Module 02's phenomenon "
            "applied to geometry.",
            "<b>Which makes deterministic structure useless:</b> "
            "<b>space-partitioning indexes degrade to linear scan above "
            "about twenty dimensions</b>, provably.",
            "<b>And makes randomness effective, for the same "
            "reason:</b> <b>a random projection works precisely because "
            "high-dimensional vectors concentrate</b>, so the projection's "
            "error concentrates too.",
            "<b>So the curse of dimensionality and the usefulness of "
            "randomness are the same fact</b> — <b>which is the most "
            "satisfying observation in this module, and it explains why "
            "high-dimensional methods are randomised essentially without "
            "exception.</b>"]},
 ],
 "takeaways": [
   "Johnson–Lindenstrauss projects to O(log n / ε²) "
   "dimensions preserving all pairwise distances — and the target "
   "dimension does not depend on the original one.",
   "The proof is Chernoff plus the union bound, and the projection is just "
   "a random Gaussian matrix with no data dependence.",
   "The ε² denominator is harsh, so high accuracy is expensive "
   "— and within its scope the bound is tight.",
   "LSH needs only a gap between near and far collision probabilities, and "
   "amplification by AND and OR sharpens it into a step.",
   "The random-hyperplane LSH is Goemans–Williamson's MAX-CUT "
   "rounding reused as a hash function.",
   "The curse of dimensionality and the usefulness of randomness are the "
   "same fact: concentration of measure defeats structure and enables "
   "projection.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Johnson–Lindenstrauss"),
  ("callout", "Johnson–Lindenstrauss: project to "
              "O(log n / ε²) dimensions and keep all pairwise "
              "distances",
   ["<b>For any set of n points in any dimension whatsoever, a random "
    "linear map into O(log n / &epsilon;&#178;) dimensions preserves all "
    "pairwise distances to within a factor of (1 &plusmn; &epsilon;), "
    "with high probability.</b>",
    "<b>Note carefully what the target dimension does <i>not</i> depend "
    "on: the original dimension.</b> <b>A million-dimensional dataset of "
    "a thousand points projects to the same number of dimensions as a "
    "thousand-dimensional dataset of a thousand points</b> — which is "
    "the remarkable part, and is what makes the result so widely "
    "applied.",
    "<b>The proof is Module 02's Chernoff bound plus Module 02's "
    "union bound</b>: each individual distance is preserved with "
    "probability 1 &minus; 1/n&#179;, and there are fewer than n&#178; "
    "pairs, so the union bound gives 1 &minus; 1/n overall. <b>Exactly "
    "the per-event-plus-union pattern of Module 03 &sect;1</b>, with "
    "the per-event target again set at a power of n.",
    "<b>And the projection is simply a random Gaussian matrix</b> "
    "— <b>no structure, no learning, no data dependence "
    "whatsoever</b>, which means you can generate it before seeing the "
    "data, apply it in a streaming setting, and share it across machines. "
    "<b>The data-independence is what makes it usable infrastructure "
    "rather than a preprocessing step.</b>"]),
  ("callout", "What JL does and does not give",
   ["<b>It preserves <i>pairwise distances</i> among a <i>specified "
    "finite set</i> of points.</b> <b>Not the geometry of the whole "
    "space, and not distances to points added later</b> — though a "
    "single fresh point is preserved with high probability, which is "
    "enough for most query workloads.",
    "<b>The &epsilon;&#178; in the denominator is harsh:</b> <b>10% "
    "distortion requires about a hundred times more dimensions than 100% "
    "distortion</b>, so <b>high accuracy is expensive</b> and the method "
    "is best suited to applications tolerating substantial "
    "distortion.",
    "<b>And it does not preserve inner products as tightly as "
    "distances</b> (the relative error on a small inner product can be "
    "large), <b>nor does it help with anything depending on the ambient "
    "dimension rather than on distances</b> — volumes, densities, and "
    "angles between subspaces are not covered.",
    "<b>But within its scope it is unimprovable:</b> <b>the "
    "O(log n / &epsilon;&#178;) bound is tight</b> (Larsen and Nelson), "
    "<b>so no cleverer projection exists</b> — which is a useful "
    "thing to know before attempting to improve on it."]),

  ("h1", "2 &nbsp; Locality-sensitive hashing"),
  ("code", """A family H is LOCALITY-SENSITIVE if
    near points collide with probability >= p1
    far points collide with probability <= p2
    with p1 > p2.

That gap is all you need. Then amplify it:
    AND over k independent hashes -> p1^k vs p2^k
        (widens the ratio; lowers both probabilities)
    OR over L such bands -> 1-(1-p1^k)^L vs the same for p2
        (raises both; steepens the transition)

Tuning k and L produces a sharp step at whatever distance
you care about -- which is Module 02 section 4's
amplification, applied to a similarity threshold rather
than to a failure probability.

THE CONSTRUCTIONS
  HAMMING / JACCARD   MinHash: hash each set by the minimum
      element under a random permutation.
      P(collision) = EXACTLY the Jaccard similarity.
  COSINE              random hyperplane: take the sign of
      the dot product with a random Gaussian vector.
      P(collision) = 1 - theta/pi.
      <-- this is exactly CSCE 669 Module 10's
          Goemans-Williamson rounding, used as a hash.
  EUCLIDEAN           project onto a random line and bucket
      by fixed-width intervals.

RESULT: sublinear-time approximate nearest neighbour
search, with a stated recall."""),
  ("p", "<b>The random-hyperplane construction is MAX-CUT's rounding "
        "reused as a hash function</b> — <b>the probability that a "
        "random hyperplane separates two unit vectors is &theta;/&pi;, "
        "which Goemans and Williamson used to bound a cut and which LSH "
        "uses to bound a collision.</b> <b>The same geometric fact, in "
        "two different subjects</b>, and noticing it is the kind of "
        "connection that makes the material cohere."),

  ("break",),
  ("h1", "3 &nbsp; Importance sampling and matrix approximation"),
  ("callout", "Importance sampling reweights, and the variance is "
              "everything",
   ["<b>To estimate an expectation under p, sample from a different "
    "distribution q and weight each sample by p(x)/q(x).</b> <b>The "
    "estimate is unbiased for any q whose support covers p's</b> "
    "— which is a strong and useful fact.",
    "<b>And the variance depends entirely on how well q matches the "
    "shape of p&middot;f</b> — <b>a well-chosen q gives enormous "
    "variance reduction and a badly chosen one gives enormous variance "
    "<i>increase</i></b>, which is the asymmetry to respect.",
    "<b>The failure mode is a small number of samples carrying huge "
    "weights:</b> <b>the estimate becomes dominated by one sample, and "
    "the <i>apparent</i> variance collapses while the true error does "
    "not</b> — because the remaining samples all have negligible "
    "weight and therefore agree with each other. <b>Which is the same "
    "silent failure as Module 09 &sect;4's unmixed chain.</b>",
    "<b>So monitor the effective sample size computed from the "
    "weights</b> — <b>the same diagnostic as MCMC uses</b> — "
    "<b>and note that CSCE 647 Module 03's importance sampling for "
    "light transport and CSCE 642 Module 05 &sect;3's off-policy "
    "correction are both exactly this technique</b>, with exactly this "
    "failure mode."]),
  ("callout", "Sampling for matrix computations",
   ["<b>Approximate a matrix product by sampling rows of one factor and "
    "columns of the other in proportion to their norms</b> — and "
    "<b>the error depends on the number of samples taken rather than on "
    "the size of the matrices</b>, which is the same scale-independence "
    "as JL's.",
    "<b>Which gives randomised low-rank approximation:</b> <b>apply a "
    "random projection to reduce the matrix to a small one, decompose the "
    "small result exactly, and lift back</b> — with a bound on the "
    "error relative to the best possible rank-k approximation.",
    "<b>And it is far faster than a full singular value "
    "decomposition</b>, which is <b>why randomised numerical linear "
    "algebra is the standard approach for very large matrices</b> "
    "(CSCE 676's subject, and CSCE 669's large-scale methods).",
    "<b>With the same structural caveat as always:</b> <b>the error "
    "bound holds in expectation or with high probability, and the norms "
    "you need to sample by must themselves be cheaply computable</b> "
    "— <b>which for a matrix arriving as a stream they may not "
    "be</b>, and uniform sampling in place of norm-proportional sampling "
    "gives a much weaker bound."]),

  ("h1", "4 &nbsp; Choosing"),
  ("table", ["Problem", "Technique", "Guarantee"],
   [["<b>Reduce dimension while keeping distances</b>",
     "<b>Random projection (JL)</b>",
     "<b>(1 &plusmn; &epsilon;) on all pairwise distances</b> "
     "(&sect;1)."],
    ["<b>Approximate nearest neighbour search</b>", "<b>LSH</b>",
     "<b>Sublinear query time with a stated recall</b> (&sect;2)."],
    ["<b>Estimate an expectation you cannot integrate</b>",
     "<b>Importance sampling</b>",
     "<b>Unbiased; the variance depends on the proposal</b> "
     "(&sect;3)."],
    ["<b>Approximate a large matrix or its decomposition</b>",
     "<b>Randomised SVD</b>",
     "<b>Near-optimal rank-k error, in expectation.</b>"],
    ["<b>Deduplicate or cluster by set similarity</b>",
     "<b>MinHash</b>",
     "<b>The collision probability is exactly the Jaccard "
     "similarity.</b>"],
    ["<b>Count distinct items</b>", "<b>HyperLogLog</b>",
     "<b>Module 05 &sect;1's 2% from 1.5 KB.</b>"]],
   [0.30, 0.25, 0.45]),
  ("p", "<b>MinHash is the one with the cleanest guarantee:</b> <b>the "
        "collision probability is <i>exactly</i> the Jaccard "
        "similarity</b>, with no approximation at all in the expectation "
        "— so a MinHash signature of k permutations gives an "
        "unbiased estimate whose variance is governed by Module 02's "
        "bounds on a sum of k independent indicators. <b>Which makes it "
        "the easiest technique in this module to reason about and the one "
        "to reach for when set similarity is the question.</b>"),
  ("callout", "Why randomness is unavoidable in high dimensions",
   ["<b>In high dimensions almost every pair of random vectors is almost "
    "orthogonal, and almost every pair of points is almost "
    "equidistant</b> — the concentration of measure, which is "
    "<b>Module 02's phenomenon applied to geometry</b> rather than to "
    "sums.",
    "<b>Which makes deterministic structure useless:</b> "
    "<b>space-partitioning indexes — kd-trees, R-trees, and their "
    "relatives — degrade to a linear scan above roughly twenty "
    "dimensions</b>, and this is provable rather than an implementation "
    "limitation (CSCE 620 Module 07's dimension dependence).",
    "<b>And it makes randomness effective, for the very same "
    "reason:</b> <b>a random projection works precisely <i>because</i> "
    "high-dimensional vectors concentrate</b> — the projection's "
    "length distortion is a sum of many small independent contributions, "
    "so it concentrates tightly around its mean.",
    "<b>So the curse of dimensionality and the usefulness of randomness "
    "are the same fact.</b> <b>Which is the most satisfying observation "
    "in this module</b>, and <b>it explains why high-dimensional methods "
    "are randomised essentially without exception</b> — not as a "
    "convenience, but because concentration is the only structure high "
    "dimensions reliably provide."]),
 ],
 "resources": [
   ("Blum, Hopcroft & Kannan &mdash; Foundations of Data Science (free "
    "PDF)",
    "https://www.cs.cornell.edu/jeh/book.pdf",
    "<b>Free in full, and the best treatment of this module</b> — "
    "JL, concentration of measure, LSH, and randomised linear algebra in "
    "one place."),
   ("Andoni & Indyk &mdash; Near-Optimal Hashing Algorithms for "
    "Approximate Nearest Neighbor (free)",
    "https://people.csail.mit.edu/indyk/p117-andoni.pdf",
    "<b>&sect;2's constructions and the amplification analysis.</b>"),
   ("Halko, Martinsson & Tropp &mdash; Finding Structure with "
    "Randomness (free)",
    "https://arxiv.org/abs/0909.4061",
    "<b>&sect;3's randomised matrix methods</b>, with the error bounds "
    "and practical algorithms. The standard reference."),
   ("Leskovec, Rajaraman & Ullman &mdash; Mining of Massive Datasets "
    "(free PDF)",
    "http://www.mmds.org/",
    "<b>&sect;2's MinHash and LSH from the practitioner's side</b>, free "
    "in full — and the chapter is the clearest introduction "
    "available."),
 ],
 "exercises": [
   "<b>Implement a JL random projection</b> and measure the distance "
   "distortion against the predicted (1±ε).",
   "<b>Confirm the target dimension does not depend on the original</b> "
   "by projecting from 1000 and from 100,000 dimensions.",
   "<b>Plot the required dimension against ε</b> and confirm the "
   "ε⁻² scaling.",
   "<b>Implement MinHash</b> and verify the collision probability equals "
   "the Jaccard similarity.",
   "<b>Implement random-hyperplane LSH</b> and relate it to "
   "CSCE 669's MAX-CUT rounding.",
   "<b>Tune k and L</b> and plot the collision probability against "
   "distance. Confirm the step sharpens.",
   "<b>Implement importance sampling</b> with a good and a bad proposal, "
   "and compare the variances.",
   "<b>Monitor the effective sample size</b> for the bad proposal and "
   "confirm it collapses.",
   "<b>Implement randomised SVD</b> and compare against an exact one for "
   "accuracy and time.",
   "<b>Measure a kd-tree's query time against dimension</b> and locate "
   "where it degrades to linear.",
 ],
 "selfcheck": [
   "State Johnson–Lindenstrauss and say what the target dimension "
   "does not depend on.",
   "What is the proof, in terms of Module 02?",
   "Name three things JL does not give.",
   "Define locality-sensitive hashing and explain the amplification.",
   "Give three LSH constructions and which other course one comes "
   "from.",
   "Explain importance sampling and its failure mode.",
   "What diagnostic catches it, and where else does it appear?",
   "How does sampling approximate a matrix, and what is the caveat?",
   "Give the six-row toolkit table.",
   "Why are the curse of dimensionality and the usefulness of randomness "
   "the same fact?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Randomness in Distributed Systems",
 "subtitle": "Where a coin is not an optimisation but a necessity.",
 "question": "Where is randomness the only thing that works?",
 "outcomes": [
     "Explain symmetry breaking and why determinism fails.",
     "Explain randomised consensus and the FLP circumvention.",
     "Explain gossip protocols and their convergence.",
     "Explain randomised load balancing in a distributed setting.",
     "Explain randomness in failure detection and backoff.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Symmetry breaking",
   "blurb": "The case where determinism provably cannot work."},

  {"t": "callout", "title": "Identical processes cannot break symmetry deterministically",
   "kind": "The impossibility, and the escape",
   "body": ["<b>Two identical processes in identical states, receiving "
            "identical messages, will do identical things.</b> <b>So "
            "neither can be chosen as leader by any deterministic "
            "algorithm.</b>",
            "<b>And this is a genuine impossibility rather than a "
            "difficulty</b> — there is no cleverer deterministic "
            "algorithm, because the executions are identical by "
            "construction.",
            "<b>A coin flip breaks it immediately.</b> <b>Each process "
            "flips; with probability 1 − 2⁻ᵏ after "
            "k rounds, they differ</b> — <b>so the problem is solved "
            "with high probability in a constant expected number of "
            "rounds.</b>",
            "<b>Which is the cleanest case in the whole subject of "
            "randomness being <i>necessary</i></b> rather than "
            "convenient — <b>Module 01 §1's first use, in "
            "its purest form.</b>"]},

  {"t": "callout", "title": "And the same argument gives randomised backoff",
   "kind": "The everyday application",
   "body": ["<b>Two senders colliding on a shared medium will collide "
            "again if they both retry deterministically</b> — the "
            "symmetry is preserved by the retry.",
            "<b>So retry after a random delay.</b> <b>Exponential "
            "backoff doubles the range each time</b>, which adapts the "
            "randomness to the observed contention.",
            "<b>And it is in Ethernet, TCP, every HTTP client's retry "
            "logic, and every distributed lock</b> — <b>which makes it "
            "the most widely deployed randomised algorithm in "
            "existence.</b>",
            "<b>With one practical refinement:</b> <b>add jitter.</b> "
            "<b>Deterministic backoff with the same schedule "
            "re-synchronises clients into waves</b>, which is the "
            "thundering-herd failure and is why AWS's published guidance "
            "is 'exponential backoff <i>with jitter</i>'."]},

  {"t": "section", "label": "Part 2", "title": "Consensus",
   "blurb": "Randomness circumvents an impossibility result."},

  {"t": "callout", "title": "FLP says deterministic consensus is impossible; randomisation escapes it",
   "kind": "The most important application",
   "body": ["<b>Fischer, Lynch and Paterson: in an asynchronous system "
            "with even one crash failure, no deterministic algorithm "
            "achieves consensus</b> (CSCE 678 §03).",
            "<b>The proof constructs an infinite execution that never "
            "decides</b> — not a wrong answer, but an indefinite "
            "delay.",
            "<b>And a randomised algorithm escapes it:</b> <b>Ben-Or's "
            "protocol terminates with probability 1, in expected "
            "constant rounds</b> — <b>because the adversarial "
            "execution FLP constructs has probability zero.</b>",
            "<b>Which is the precise form of the escape:</b> "
            "<b>randomisation does not contradict FLP — it changes "
            "the guarantee from 'always terminates' to 'terminates with "
            "probability 1'</b>, and the impossibility was about the "
            "first."]},

  {"t": "table", "kicker": "Consensus", "title": "What randomisation changes",
   "header": ["", "Deterministic", "Randomised"],
   "widths": [2.3, 4.3, 5.3],
   "rows": [
     ["<b>Safety</b>", "<b>Guaranteed</b>", "<b>Guaranteed — unchanged</b>"],
     ["<b>Liveness</b>", "<b>Impossible (FLP)</b>", "<b>With probability 1</b>"],
     ["<b>Rounds</b>", "<b>Unbounded in the worst case</b>", "<b>Expected O(1); unbounded worst case</b>"],
     ["<b>In practice</b>", "<b>Paxos, Raft — with timeouts</b>", "<b>Ben-Or; HoneyBadger; blockchain protocols</b>"],
   ],
   "footnote": "<b>Note that safety is never traded.</b> <b>A "
               "randomised consensus protocol never decides "
               "inconsistently</b> — the randomness affects only "
               "whether and when it decides, which is the right place for "
               "it.",
   "note": "That safety is preserved is the point practitioners need."},

  {"t": "section", "label": "Part 3", "title": "Gossip and load balancing",
   "blurb": "Randomness for scalability rather than for possibility."},

  {"t": "callout", "title": "Gossip spreads information in O(log n) rounds with constant work per node",
   "kind": "The epidemic model, applied",
   "body": ["<b>Each node, each round, picks a random peer and "
            "exchanges state.</b> <b>Information reaches every node in "
            "O(log n) rounds with high probability.</b>",
            "<b>Which is the random graph connectivity result of "
            "Module 06 in a different guise</b> — the union of the "
            "random choices forms an expanding graph.",
            "<b>And the work per node per round is constant</b>, which "
            "is what makes it scalable: <b>no node needs a global view, "
            "a membership list, or a coordinator.</b>",
            "<b>So it is used for membership, failure detection, "
            "configuration propagation, and anti-entropy "
            "repair</b> — <b>Cassandra, Consul, and Serf are built on "
            "it</b> (CSCE 678 §04). <b>The robustness to "
            "failure is the selling point, not the speed.</b>"]},

  {"t": "bullets", "kicker": "Load balancing", "title": "Two choices, in a distributed setting",
   "items": [
     "<b>Module 03 §2's power of two choices</b>, applied "
     "to servers: <b>query two at random and send to the less "
     "loaded.</b>",
     "",
     "<b>Which gives log log n maximum load with no coordination</b> "
     "— no central balancer, no global state, two probes.",
     "",
     "<b>And the practical caveat is stale information:</b> <b>if "
     "every balancer queries the same two and they all pick the same "
     "one, the advantage inverts</b> — which is the "
     "herd-behaviour failure.",
     "",
     "<b>So the load must be sampled freshly, or the choices "
     "randomised per balancer</b> — and this failure has been "
     "observed in production repeatedly.",
     "",
     "<b>And consistent hashing with bounded loads</b> combines the "
     "two: a hash-determined home plus a fallback to the next.",
   ],
   "footnote": "<b>The stale-information inversion is the one practical "
               "trap</b> — the theorem assumes each ball sees the "
               "current load, and a distributed system usually does "
               "not."},

  {"t": "section", "label": "Part 4", "title": "Where else",
   "blurb": "The remaining uses."},

  {"t": "bullets", "kicker": "Elsewhere", "title": "Randomness in the rest of a distributed system",
   "items": [
     "<b>Failure detection.</b> <b>Randomised probe targets avoid "
     "correlated false positives</b>, and SWIM's random-peer probing is "
     "the standard design.",
     "",
     "<b>Sampling for monitoring.</b> <b>Trace sampling, which is "
     "reservoir sampling</b> (Module 05 §3) <b>applied to "
     "requests.</b>",
     "",
     "<b>Randomised leader rotation</b>, which spreads load and "
     "limits the value of attacking any one leader.",
     "",
     "<b>Chaos engineering</b> — <b>randomly killing instances "
     "to test resilience</b>, which is sampling the failure space "
     "rather than enumerating it.",
     "",
     "<b>And cryptographic nonces and session identifiers</b>, where "
     "the randomness is a security requirement rather than a performance "
     "one (CSCE 711).",
   ],
   "footnote": "<b>The last item is the one where a weak source is "
               "catastrophic rather than merely degrading</b> "
               "— Module 13 §2."},

  {"t": "callout", "title": "Why this module matters",
   "kind": "The assessment",
   "body": ["<b>This is the setting where randomness is most clearly "
            "<i>necessary</i></b> rather than merely convenient — "
            "symmetry breaking and consensus are both impossibility "
            "results that randomisation escapes.",
            "<b>And the escapes are precise:</b> <b>the guarantee "
            "changes from 'always' to 'with probability 1', and the "
            "impossibility proof was about 'always'.</b>",
            "<b>Which is a better justification for randomness than any "
            "efficiency argument</b>, because it is not a trade at "
            "all — there is nothing deterministic to compare "
            "against.",
            "<b>And it means every distributed system you will build "
            "contains several of these</b> — <b>backoff with jitter at "
            "minimum, and probably gossip, two-choice balancing, and "
            "sampled tracing.</b>"]},
 ],
 "takeaways": [
   "Identical processes cannot break symmetry deterministically, which is "
   "a genuine impossibility that a coin flip escapes immediately.",
   "Randomised exponential backoff with jitter is the most widely deployed "
   "randomised algorithm in existence.",
   "FLP says deterministic asynchronous consensus is impossible, and "
   "randomisation changes the guarantee from 'always terminates' to "
   "'terminates with probability 1'.",
   "Safety is never traded in randomised consensus — only whether and "
   "when it decides.",
   "Gossip reaches every node in O(log n) rounds with constant work per "
   "node and no global view, which is why it is used for membership.",
   "The power of two choices inverts under stale load information, which "
   "is the one practical trap and has been observed in production.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Symmetry breaking"),
  ("callout", "Identical processes cannot break symmetry deterministically",
   ["<b>Two identical processes in identical states, receiving identical "
    "messages, will take identical actions.</b> <b>So neither can be "
    "selected as leader by any deterministic algorithm</b>, because the "
    "two executions are identical step for step.",
    "<b>And this is a genuine impossibility rather than a "
    "difficulty</b> — <b>there is no cleverer deterministic "
    "algorithm, because the executions are indistinguishable by "
    "construction</b> and any algorithm is a function of the execution.",
    "<b>A single coin flip breaks it immediately.</b> <b>Each process "
    "flips; with probability 1 &minus; 2<super>&minus;k</super> after k "
    "rounds the two have differed at least once</b> — <b>so the "
    "problem is solved with high probability in a constant expected number "
    "of rounds</b>, which is as good as it could be.",
    "<b>Which is the cleanest case in the entire subject of randomness "
    "being <i>necessary</i></b> rather than merely convenient — "
    "<b>Module 01 &sect;1's first use (defeating an adversary, or here "
    "defeating a symmetry) in its purest form</b>, with a provable "
    "impossibility on the other side and no deterministic alternative to "
    "compare against."]),
  ("callout", "And the same argument gives randomised backoff",
   ["<b>Two senders that collide on a shared medium will collide again if "
    "they both retry deterministically</b> — <b>the retry preserves "
    "the symmetry</b> that caused the collision, which is the same "
    "argument as the callout above.",
    "<b>So retry after a random delay.</b> <b>Exponential backoff "
    "doubles the range of the random delay after each collision</b>, which "
    "adapts the amount of randomness to the observed level of contention "
    "rather than fixing it in advance.",
    "<b>And it is in Ethernet, in TCP's congestion response, in every "
    "HTTP client's retry logic, and in every distributed lock "
    "implementation</b> — <b>which makes randomised exponential "
    "backoff the most widely deployed randomised algorithm in "
    "existence</b>, by a very large margin.",
    "<b>With one practical refinement that is frequently omitted:</b> "
    "<b>add jitter.</b> <b>Backoff with a deterministic schedule "
    "re-synchronises clients into waves</b> — all the clients that "
    "failed together retry together, fail together, and retry together "
    "again — <b>which is the thundering-herd failure, and is why the "
    "standard published guidance is 'exponential backoff <i>with "
    "jitter</i>'</b> rather than exponential backoff alone. <b>The jitter "
    "is doing the symmetry breaking and the exponential part is doing the "
    "congestion control, and they are two separate mechanisms.</b>"]),

  ("h1", "2 &nbsp; Consensus"),
  ("callout", "FLP says deterministic consensus is impossible; "
              "randomisation escapes it",
   ["<b>Fischer, Lynch and Paterson: in an asynchronous system with even "
    "a single crash failure, no deterministic algorithm achieves "
    "consensus</b> (CSCE 678 Module 03's central result).",
    "<b>The proof constructs an infinite execution that never "
    "decides</b> — <b>not a wrong answer, but an indefinite "
    "delay</b>, by repeatedly extending a bivalent configuration. <b>The "
    "impossibility is about liveness rather than safety.</b>",
    "<b>And a randomised algorithm escapes it:</b> <b>Ben-Or's protocol "
    "terminates with probability 1, in an expected constant number of "
    "rounds (for a small enough failure fraction)</b> — <b>because "
    "the adversarial execution that FLP constructs has probability "
    "zero</b> under the protocol's own randomisation. The adversary "
    "cannot steer the coin flips.",
    "<b>Which is the precise form of the escape, and it is worth stating "
    "exactly:</b> <b>randomisation does not contradict FLP</b> — it "
    "<b>changes the guarantee from 'always terminates' to 'terminates "
    "with probability 1'</b>, <b>and the impossibility result was about "
    "the first.</b> <b>So the theorem and the protocol are both "
    "correct</b>, which is a useful thing to be able to explain when "
    "someone points out the apparent contradiction."]),
  ("table", ["", "Deterministic", "Randomised"],
   [["<b>Safety (never decide inconsistently)</b>", "<b>Guaranteed.</b>",
     "<b>Guaranteed — unchanged.</b> See the note."],
    ["<b>Liveness (eventually decide)</b>",
     "<b>Impossible in the asynchronous model with one failure "
     "(FLP).</b>", "<b>With probability 1.</b>"],
    ["<b>Round complexity</b>",
     "<b>Unbounded in the worst case</b> — that is the content of "
     "FLP.",
     "<b>Expected O(1) for small failure fractions; still unbounded in "
     "the worst case.</b>"],
    ["<b>What is used in practice</b>",
     "<b>Paxos and Raft — which are deterministic and use "
     "<i>timeouts</i> to sidestep FLP by assuming partial "
     "synchrony</b> (and randomised election timeouts, which is this "
     "module again).",
     "<b>Ben-Or, HoneyBadger, and several blockchain consensus "
     "protocols</b>, where asynchrony cannot be assumed away."]],
   [0.22, 0.38, 0.40]),
  ("p", "<b>Note that safety is never traded.</b> <b>A randomised "
        "consensus protocol never decides inconsistently</b> — the "
        "randomness affects only <i>whether and when</i> it decides, "
        "<b>which is the right place for it</b> and is the point "
        "practitioners most need to hear. <b>And note that Raft's "
        "randomised election timeouts are this module's symmetry breaking "
        "inside an ostensibly deterministic protocol</b>, which is worth "
        "spotting."),

  ("break",),
  ("h1", "3 &nbsp; Gossip and load balancing"),
  ("callout", "Gossip spreads information in O(log n) rounds with constant "
              "work per node",
   ["<b>Each node, in each round, picks a random peer and exchanges "
    "state with it.</b> <b>Information reaches every node in O(log n) "
    "rounds with high probability</b> — the same doubling argument as "
    "an epidemic.",
    "<b>Which is Module 06's random graph connectivity result in a "
    "different guise</b> — the union of the random peer choices over "
    "several rounds forms a well-connected expanding graph, and the "
    "O(log n) is its diameter.",
    "<b>And the work per node per round is constant</b>, which is what "
    "makes it scalable: <b>no node needs a global membership view, a "
    "coordinator, or a consistent snapshot of anything.</b>",
    "<b>So it is used for membership, failure detection, configuration "
    "propagation, and anti-entropy repair</b> — <b>Cassandra, "
    "Consul, and Serf are all built on gossip</b> (CSCE 678 "
    "Module 04). <b>And the robustness to failure is the selling point "
    "rather than the speed:</b> a gossip protocol degrades gracefully as "
    "nodes fail, because there is nothing central to lose."]),
  ("ul", ["<b>Module 03 &sect;2's power of two choices, applied to "
          "servers:</b> <b>query two backends at random and send the "
          "request to whichever reports less load.</b>",
          "<b>Which gives log log n maximum load with no coordination "
          "whatsoever</b> — no central balancer, no global state, "
          "two probes per request.",
          "<b>And the practical caveat is stale information:</b> <b>if "
          "every load balancer queries the same two backends and they all "
          "see the same stale load figures, they all pick the same one, and "
          "the advantage inverts into a disadvantage</b> — the chosen "
          "backend receives everything. <b>This is the herd-behaviour "
          "failure, and it has been observed in production repeatedly.</b>",
          "<b>So the load must be sampled freshly, or the two choices "
          "must be randomised independently per balancer</b>, or an "
          "age-weighted estimate used — <b>and the theorem's "
          "assumption that each ball sees the <i>current</i> load is the "
          "one that a distributed system usually violates.</b>",
          "<b>And consistent hashing with bounded loads</b> combines the "
          "two approaches: a hash determines each request's preferred "
          "backend, and overflow spills to the next in the ring — "
          "<b>which gives locality (useful for caching) and bounded load "
          "together.</b>"]),

  ("h1", "4 &nbsp; The remaining uses"),
  ("ul", ["<b>Failure detection.</b> <b>Randomised probe targets avoid "
          "correlated false positives</b> — if every node probes the "
          "same monitor, a single slow monitor marks everything "
          "dead — <b>and SWIM's random-peer probing with indirect "
          "confirmation is the standard design</b>.",
          "<b>Sampling for monitoring and tracing.</b> <b>Distributed "
          "trace sampling is reservoir sampling</b> (Module 05 "
          "&sect;3) <b>applied to requests</b>, and head-based against "
          "tail-based sampling is a question about which distribution you "
          "want.",
          "<b>Randomised leader rotation</b>, which spreads the "
          "leadership load and <b>limits the value of attacking or "
          "predicting any single leader</b> — a security property as "
          "much as a performance one.",
          "<b>Chaos engineering.</b> <b>Randomly terminating instances "
          "to test resilience</b> is <b>sampling the failure space rather "
          "than attempting to enumerate it</b>, which is the only "
          "tractable approach given the number of possible failure "
          "combinations.",
          "<b>And cryptographic nonces, session identifiers, and "
          "tokens</b>, where <b>the randomness is a security requirement "
          "rather than a performance optimisation</b> (CSCE 711) "
          "— <b>and this is the one case where a weak source is "
          "catastrophic rather than merely degrading</b> (Module 13 "
          "&sect;2)."]),
  ("callout", "Why this module matters",
   ["<b>This is the setting where randomness is most clearly "
    "<i>necessary</i></b> rather than merely convenient — "
    "<b>symmetry breaking (&sect;1) and asynchronous consensus "
    "(&sect;2) are both impossibility results that randomisation "
    "escapes</b>, and there is no deterministic alternative to weigh it "
    "against.",
    "<b>And the escapes are precise rather than hand-waved:</b> <b>the "
    "guarantee changes from 'always' to 'with probability 1', and the "
    "impossibility proof was about 'always'.</b>",
    "<b>Which is a better justification for randomness than any "
    "efficiency argument</b>, because <b>it is not a trade at all</b> "
    "— Module 01 &sect;1's three uses each had a deterministic "
    "alternative to compare against, and here there is none.",
    "<b>And it means every distributed system you will ever build "
    "contains several of these</b> — <b>randomised backoff with "
    "jitter at an absolute minimum, and very probably gossip, two-choice "
    "balancing, randomised probing, and sampled tracing as well.</b> "
    "<b>Which makes this the module whose content you are most certain to "
    "have already deployed.</b>"]),
 ],
 "resources": [
   ("Fischer, Lynch & Paterson &mdash; Impossibility of Distributed "
    "Consensus with One Faulty Process (free)",
    "https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf",
    "<b>&sect;2's impossibility result</b> — short, and the "
    "bivalent-configuration argument is worth following."),
   ("Ben-Or &mdash; Another advantage of free choice (free)",
    "https://dl.acm.org/doi/10.1145/800221.806707",
    "<b>&sect;2's randomised escape</b>, in three pages."),
   ("Demers et al. &mdash; Epidemic Algorithms for Replicated Database "
    "Maintenance (free)",
    "https://dl.acm.org/doi/10.1145/41840.41841",
    "<b>&sect;3's gossip protocols</b>, in the paper that introduced "
    "them to systems."),
   ("Brooker &mdash; Exponential Backoff and Jitter (free, AWS "
    "Architecture Blog)",
    "https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/",
    "<b>&sect;1's jitter requirement, measured</b> — with the "
    "thundering-herd effect demonstrated and the variants compared."),
 ],
 "exercises": [
   "<b>Simulate two identical processes</b> attempting deterministic "
   "leader election, and confirm it never terminates.",
   "<b>Add coin flips</b> and measure the expected number of rounds.",
   "<b>Implement exponential backoff without jitter</b> for many clients "
   "and observe the retry waves.",
   "<b>Add jitter</b> and measure the improvement in collision rate.",
   "<b>Read the FLP proof</b> and identify the step a randomised protocol "
   "invalidates.",
   "<b>Implement Ben-Or's protocol</b> and measure the rounds to decide "
   "against the failure fraction.",
   "<b>Implement gossip</b> on 1000 nodes and measure the rounds to full "
   "propagation. Compare against log n.",
   "<b>Kill 30% of the nodes mid-propagation</b> and report what "
   "happens.",
   "<b>Implement two-choice load balancing with stale load data</b> and "
   "reproduce the herd inversion.",
   "<b>Fix it</b> and report which fix you used and why.",
 ],
 "selfcheck": [
   "Why can identical processes not break symmetry deterministically?",
   "How does a coin flip escape it, and how fast?",
   "Why does deterministic backoff fail, and what are jitter and "
   "exponential backoff each doing?",
   "State FLP and explain precisely how randomisation escapes it.",
   "What is never traded in randomised consensus?",
   "Why does gossip take O(log n) rounds, and what other module does "
   "that come from?",
   "What makes gossip scalable, and what is its real selling point?",
   "Describe the two-choice herd inversion and its fixes.",
   "Name five other uses of randomness in a distributed system.",
   "Why is this the module whose content you have most certainly already "
   "deployed?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Derandomisation",
 "subtitle": "Taking the randomness back out.",
 "question": "Having used randomness to design the algorithm, can you "
             "remove it?",
 "outcomes": [
     "Apply the method of conditional expectations.",
     "Explain limited independence and when it suffices.",
     "Explain expander graphs and their role.",
     "Explain pseudorandom generators at a working level.",
     "Decide whether derandomisation is worth attempting.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Conditional expectations",
   "blurb": "The technique that always works, when it works."},

  {"t": "code", "kicker": "Conditional expectations", "title": "Fix the choices one at a time, greedily",
   "lang": "text", "code": """
  THE PROBABILISTIC PROOF says E[value] = m/2, so some
  assignment achieves m/2 (Module 07 Part 1).

  THE DERANDOMISATION: decide the variables one at a time.
  At each step, compute the conditional expectation under
  each of the two choices, and take the larger.

      E[value] = (1/2) E[value | x=0]
               + (1/2) E[value | x=1]

  So at least one branch has conditional expectation >=
  the current one. Take it. The expectation never
  decreases.

  After all variables are fixed, the "expectation" is the
  actual value -- and it is at least the original m/2.
      -> A DETERMINISTIC algorithm with the same guarantee.

  FOR MAX-CUT this becomes: place each vertex on whichever
  side has fewer of its already-placed neighbours. A
  greedy algorithm, derived rather than invented.

  THE REQUIREMENT: you must be able to COMPUTE the
  conditional expectation efficiently. For MAX-CUT it is a
  count of neighbours. When it is intractable, the method
  fails -- and that is the usual obstacle.
""",
   "caption": "<b>A greedy algorithm derived from a probabilistic "
              "proof</b> — which is where a surprising number of "
              "natural greedy algorithms come from.",
   "note": "That the greedy algorithm is derived rather than guessed is "
           "the insight."},

  {"t": "callout", "title": "Why this is the method to try first",
   "kind": "The practical point",
   "body": ["<b>It is mechanical.</b> <b>Given the probabilistic "
            "analysis, the derandomisation follows</b> — no new idea "
            "is needed, only the ability to compute a conditional "
            "expectation.",
            "<b>It preserves the guarantee exactly.</b> <b>The "
            "deterministic algorithm achieves at least what the random "
            "one achieved in expectation</b>, which is the best you could "
            "ask.",
            "<b>And it frequently produces an algorithm you would "
            "recognise</b> — <b>greedy set cover, greedy MAX-CUT, and "
            "several approximation algorithms are conditional-expectation "
            "derandomisations</b> of their probabilistic proofs.",
            "<b>So when you have a probabilistic approximation "
            "algorithm, spend an hour on this</b> — <b>it may give you "
            "a deterministic version with the same ratio and no seed to "
            "manage.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Limited independence",
   "blurb": "Using less randomness rather than none."},

  {"t": "callout", "title": "Most analyses need pairwise independence, not full independence",
   "kind": "The observation that saves the randomness",
   "body": ["<b>n fully independent random bits cost n bits.</b> "
            "<b>n <i>pairwise</i> independent bits cost O(log n) "
            "bits</b> — generate them from a short seed by a linear "
            "map.",
            "<b>And many analyses only use pairwise "
            "independence</b> — <b>anything bounded by Chebyshev "
            "does</b> (Module 02 §1), including the hashing "
            "analysis of Module 04 §2.",
            "<b>So check what your analysis actually uses.</b> <b>If "
            "Chebyshev sufficed, O(log n) random bits suffice</b> "
            "— and <b>you can then enumerate all 2^O(log n) = "
            "poly(n) seeds deterministically.</b>",
            "<b>Which is a complete derandomisation</b> — <b>try "
            "every seed, take the best outcome, and the whole thing is "
            "deterministic and polynomial.</b> <b>k-wise independence "
            "for larger k costs O(k log n) bits and covers more "
            "analyses.</b>"]},

  {"t": "table", "kicker": "Independence", "title": "How much independence costs, and what it buys",
   "header": ["Independence", "Random bits", "Supports"],
   "widths": [2.6, 3.4, 5.0],
   "rows": [
     ["<b>Full</b>", "<b>n bits</b>", "<b>Chernoff, and everything else</b>"],
     ["<b>Pairwise</b>", "<b>O(log n)</b>", "<b>Chebyshev; universal hashing</b>"],
     ["<b>4-wise</b>", "<b>O(log n)</b>", "<b>Fourth-moment bounds; AMS sketch</b>"],
     ["<b>5-wise</b>", "<b>O(log n)</b>", "<b>Linear probing's analysis (M04 §2)</b>"],
     ["<b>k-wise</b>", "<b>O(k log n)</b>", "<b>Weaker Chernoff-like bounds</b>"],
   ],
   "footnote": "<b>All the limited-independence rows are O(log n) up to "
               "the k factor</b>, which is the point — <b>and "
               "poly(n) seeds can be enumerated, so any of them gives a "
               "full derandomisation.</b>",
   "note": "The enumerate-all-seeds move is what makes this a complete "
           "technique."},

  {"t": "section", "label": "Part 3", "title": "Expanders and generators",
   "blurb": "The heavier machinery."},

  {"t": "callout", "title": "Expander graphs let you reuse randomness",
   "kind": "The second technique",
   "body": ["<b>An expander is a sparse graph where every small set has "
            "many neighbours outside it</b> — equivalently, high "
            "conductance (Module 09 §2).",
            "<b>A random walk on an expander mixes in O(log n) "
            "steps</b>, so <b>k steps of a walk give k nearly-independent "
            "samples using only log n + O(k) random bits</b> rather than "
            "k log n.",
            "<b>Which derandomises error amplification:</b> "
            "<b>repetition normally costs k times the randomness, and an "
            "expander walk costs almost none of it</b> "
            "(Module 02 §4).",
            "<b>And a random graph is an expander</b> "
            "(Module 06 §4) — <b>so the existence proof is "
            "probabilistic and the explicit constructions, which came "
            "later, are what make the derandomisation effective.</b>"]},

  {"t": "callout", "title": "Pseudorandom generators, and the conditional result",
   "kind": "The theoretical answer",
   "body": ["<b>A pseudorandom generator stretches a short seed into a "
            "long string indistinguishable from random by any efficient "
            "test</b> (CSCE 637 §08 §3).",
            "<b>If strong enough ones exist, every randomised "
            "polynomial-time algorithm can be derandomised</b> — "
            "<b>BPP = P</b>, by enumerating all short seeds.",
            "<b>And they follow from circuit lower bounds</b> "
            "(CSCE 637 §09) — <b>so hardness implies "
            "derandomisation, which is the counterintuitive connection "
            "that course develops.</b>",
            "<b>So the theoretical answer is 'probably yes, "
            "conditionally'</b> — <b>and the practical answer is that "
            "Parts 1 and 2 are what you will actually use</b>, because "
            "they are unconditional and implementable."]},

  {"t": "section", "label": "Part 4", "title": "Should you",
   "blurb": "The honest decision."},

  {"t": "bullets", "kicker": "Decision", "title": "When derandomisation is worth the effort",
   "items": [
     "<b>When reproducibility is required.</b> <b>A deterministic "
     "algorithm needs no seed management</b>, which is a real "
     "operational benefit (Module 13 §1).",
     "",
     "<b>When good randomness is unavailable.</b> <b>Embedded, early "
     "boot, or a constrained environment</b> "
     "(Module 01 §4).",
     "",
     "<b>When conditional expectations are easy to compute.</b> "
     "<b>Then it is an hour's work and you lose nothing</b> "
     "(Part 1).",
     "",
     "<b>And not when the randomised algorithm is simpler and the "
     "seed is manageable</b> — <b>which is the usual case</b>, and "
     "the honest answer most of the time.",
     "",
     "<b>And never for the adversary use</b> "
     "(Module 01 §1) — <b>derandomising a hash function "
     "restores the worst case the randomness was defeating.</b>",
   ],
   "footnote": "<b>The last point is the important one:</b> "
               "<b>derandomisation is appropriate for the simplification "
               "and sampling uses and is self-defeating for the adversary "
               "use.</b>"},

  {"t": "callout", "title": "What this module adds to CSCE 637's view",
   "kind": "The division",
   "body": ["<b>CSCE 637 §08 asked whether randomness can "
            "be removed from a <i>complexity class</i></b> — and the "
            "answer is conditional and unresolved.",
            "<b>This module removes it from <i>specific "
            "algorithms</i></b> — and <b>the answer is frequently yes, "
            "unconditionally, in an hour.</b>",
            "<b>So the two questions have different answers and are "
            "about different things</b>, which is the point "
            "CSCE 637 §08 §4 flagged.",
            "<b>And the practical version is the useful one:</b> <b>you "
            "will never derandomise BPP and you may well derandomise your "
            "own algorithm</b>, and the techniques for the second are "
            "Parts 1 and 2."]},
 ],
 "takeaways": [
   "Conditional expectations derandomise mechanically: fix choices one at "
   "a time, taking whichever keeps the conditional expectation at least as "
   "high.",
   "The result frequently is a greedy algorithm you would recognise "
   "— greedy MAX-CUT and greedy set cover are derandomisations of "
   "probabilistic proofs.",
   "The requirement is that the conditional expectation be computable, and "
   "when it is not, the method fails.",
   "Most analyses need only pairwise independence, which costs O(log n) "
   "bits — and poly(n) seeds can be enumerated, giving a complete "
   "derandomisation.",
   "An expander walk gives k nearly-independent samples from log n + O(k) "
   "bits, which derandomises error amplification.",
   "Derandomise for reproducibility, scarce entropy, or when it is cheap "
   "— and never for the adversary use, where it restores the worst "
   "case.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The method of conditional expectations"),
  ("code", """THE PROBABILISTIC PROOF says E[value] = m/2, so some
assignment achieves at least m/2 (Module 07 section 1).

THE DERANDOMISATION: decide the variables one at a time. At
each step compute the conditional expectation under each of
the two choices, and take whichever is larger.

    E[value] = (1/2) E[value | x=0]
             + (1/2) E[value | x=1]

So at least one of the two branches has conditional
expectation at least as large as the current value. Take
it. The conditional expectation never decreases.

After all variables are fixed, the "expectation" is the
actual value of the assignment -- and it is at least the
original m/2.
    -> A DETERMINISTIC algorithm with the same guarantee.

FOR MAX-CUT this becomes: place each vertex on whichever
side currently has fewer of its already-placed neighbours.
A greedy algorithm, DERIVED rather than invented.

THE REQUIREMENT: you must be able to COMPUTE the
conditional expectation efficiently. For MAX-CUT it is a
count of neighbours, which is trivial. When the conditional
expectation is itself intractable, the method fails -- and
that is the usual obstacle."""),
  ("callout", "Why this is the method to try first",
   ["<b>It is mechanical.</b> <b>Given the probabilistic analysis, the "
    "derandomisation follows</b> — no new idea is required, only the "
    "ability to compute a conditional expectation.",
    "<b>It preserves the guarantee exactly.</b> <b>The deterministic "
    "algorithm achieves at least what the randomised one achieved in "
    "expectation</b>, which is the best outcome you could hope for from a "
    "derandomisation.",
    "<b>And it frequently produces an algorithm you would "
    "recognise.</b> <b>Greedy set cover, greedy MAX-CUT, and a number of "
    "standard approximation algorithms are conditional-expectation "
    "derandomisations of their probabilistic proofs</b> — <b>which "
    "means a surprising fraction of natural-looking greedy algorithms were "
    "derived rather than guessed</b>, and the probabilistic proof explains "
    "<i>why</i> the greedy choice is the right one.",
    "<b>So when you have a probabilistic approximation algorithm, spend "
    "an hour on this.</b> <b>It may give you a deterministic version "
    "with the identical ratio and no seed to manage</b>, which is "
    "frequently worth more than the randomised version's simplicity."]),

  ("h1", "2 &nbsp; Limited independence"),
  ("callout", "Most analyses need pairwise independence, not full "
              "independence",
   ["<b>n fully independent random bits cost n bits of randomness.</b> "
    "<b>n <i>pairwise</i> independent bits cost only O(log n) bits</b> "
    "— generate them from a short seed by a linear map over a finite "
    "field, which is exactly the universal hashing construction of "
    "Module 04 &sect;2.",
    "<b>And a great many analyses use only pairwise "
    "independence</b> — <b>anything bounded by Chebyshev does</b> "
    "(Module 02 &sect;1), <b>including the hash-table chain-length "
    "analysis</b> and the second-moment arguments of Module 06 "
    "&sect;2.",
    "<b>So check what your analysis actually uses rather than what it "
    "assumed.</b> <b>If Chebyshev sufficed, O(log n) random bits "
    "suffice</b> — <b>and then you can enumerate all "
    "2<super>O(log n)</super> = poly(n) possible seeds "
    "deterministically.</b>",
    "<b>Which is a complete derandomisation:</b> <b>try every seed, take "
    "the best outcome, and the whole algorithm is deterministic and "
    "polynomial-time.</b> <b>And k-wise independence for larger k costs "
    "O(k log n) bits and covers more analyses</b> — including weaker "
    "Chernoff-like bounds, which brings a good deal more within reach. "
    "<b>The enumerate-all-seeds move is what makes this a complete "
    "technique rather than an economy.</b>"]),
  ("table", ["Independence", "Random bits needed", "What it supports"],
   [["<b>Full independence</b>", "<b>n bits.</b>",
     "<b>Chernoff bounds, and every analysis.</b>"],
    ["<b>Pairwise</b>", "<b>O(log n).</b>",
     "<b>Chebyshev bounds; universal hashing</b> (Module 04 "
     "&sect;2)."],
    ["<b>4-wise</b>", "<b>O(log n).</b>",
     "<b>Fourth-moment bounds; the AMS sketch's analysis</b> "
     "(Module 05 &sect;1)."],
    ["<b>5-wise</b>", "<b>O(log n).</b>",
     "<b>Linear probing's analysis</b> (Module 04 &sect;2's "
     "table) — which is why that result took so long."],
    ["<b>k-wise</b>", "<b>O(k log n).</b>",
     "<b>Weaker Chernoff-like tail bounds</b>, which covers a "
     "substantial fraction of the remaining analyses."]],
   [0.24, 0.26, 0.50]),

  ("break",),
  ("h1", "3 &nbsp; Expanders and pseudorandom generators"),
  ("callout", "Expander graphs let you reuse randomness",
   ["<b>An expander is a sparse graph in which every small set of "
    "vertices has many neighbours outside it</b> — equivalently, a "
    "graph with high conductance (Module 09 &sect;2) and therefore a "
    "large spectral gap.",
    "<b>A random walk on an expander mixes in O(log n) steps</b>, so "
    "<b>k steps of such a walk give k nearly-independent samples using "
    "only log n + O(k) random bits</b> — rather than the k log n "
    "bits that k independent samples would require.",
    "<b>Which derandomises error amplification:</b> <b>repetition "
    "normally costs k times the randomness of a single run, and an "
    "expander walk costs almost none of it</b> (Module 02 &sect;4's "
    "amplification, made randomness-efficient) — so you keep the "
    "exponentially small failure probability at a logarithmic randomness "
    "cost.",
    "<b>And a random graph is an expander with high probability</b> "
    "(Module 06 &sect;4) — <b>so the existence proof is itself "
    "probabilistic, and the explicit constructions, which came decades "
    "later and are considerably harder, are what make the "
    "derandomisation actually effective.</b> <b>Which is a pleasing "
    "circularity: the probabilistic method proves that the object needed "
    "to remove randomness exists.</b>"]),
  ("callout", "Pseudorandom generators, and the conditional result",
   ["<b>A pseudorandom generator stretches a short seed into a long "
    "string that no efficient test can distinguish from truly random</b> "
    "(CSCE 637 Module 08 &sect;3's definition).",
    "<b>If strong enough generators exist, every randomised "
    "polynomial-time algorithm can be derandomised</b> — <b>BPP = "
    "P</b> — by running the algorithm on the output of the generator "
    "for every short seed and taking the majority.",
    "<b>And strong enough generators follow from circuit lower "
    "bounds</b> (CSCE 637 Module 09) — <b>so hardness implies "
    "derandomisation, which is the counterintuitive connection that course "
    "develops at length.</b>",
    "<b>So the theoretical answer is 'probably yes, "
    "conditionally'</b> — <b>and the practical answer is that "
    "&sect;1 and &sect;2 are what you will actually use</b>, because they "
    "are unconditional, implementable, and frequently take an "
    "afternoon."]),

  ("h1", "4 &nbsp; Should you derandomise"),
  ("ul", ["<b>When reproducibility is required.</b> <b>A deterministic "
          "algorithm needs no seed management at all</b>, which is a real "
          "operational benefit in builds, in regulated environments, and "
          "in anything that must be audited (Module 13 &sect;1).",
          "<b>When good randomness is unavailable.</b> <b>Embedded "
          "systems, early boot, and constrained environments</b> may "
          "simply not have an entropy source (Module 01 &sect;4), and "
          "a deterministic algorithm sidesteps the problem rather than "
          "working around it.",
          "<b>When the conditional expectations are easy to "
          "compute.</b> <b>Then it is an hour's work and you lose "
          "nothing</b> (&sect;1) — and you may end up with a "
          "recognisable greedy algorithm that is also faster.",
          "<b>And not when the randomised algorithm is simpler and the "
          "seed is manageable</b> — <b>which is the usual case</b>, "
          "and is the honest answer most of the time. A skip list that you "
          "can read beats a red-black tree that you cannot (Module 04 "
          "&sect;4).",
          "<b>And never for the adversary use</b> (Module 01 "
          "&sect;1) — <b>derandomising a hash function restores "
          "exactly the worst case that the randomness was there to "
          "defeat</b>, and an adversary who can read your code can then "
          "construct it. <b>Which is the important point:</b> "
          "<b>derandomisation is appropriate for the simplification and "
          "sampling uses of randomness, and is actively self-defeating for "
          "the adversary use.</b>"]),
  ("callout", "What this module adds to CSCE 637's view",
   ["<b>CSCE 637 Module 08 asked whether randomness can be removed "
    "from a <i>complexity class</i></b> — whether BPP = P — and "
    "<b>the answer there is conditional and unresolved.</b>",
    "<b>This module removes it from <i>specific algorithms</i></b> "
    "— and <b>the answer is frequently yes, unconditionally, in an "
    "afternoon.</b>",
    "<b>So the two questions have different answers and are about "
    "different things</b>, which is <b>the point CSCE 637 Module 08 "
    "&sect;4's closing callout flagged</b> and which this module makes "
    "concrete.",
    "<b>And the practical version is the useful one:</b> <b>you will "
    "never derandomise BPP, and you may well derandomise your own "
    "algorithm</b> — <b>and the techniques for the second are "
    "&sect;1 and &sect;2, neither of which depends on any open "
    "question.</b>"]),
 ],
 "resources": [
   ("Motwani & Raghavan &mdash; chapter 5",
    "https://www.cambridge.org/core/books/randomized-algorithms/6A3E5CD760413BEF7D0D01BFD5497ACB",
    "<b>Conditional expectations and limited independence</b> — the "
    "reference for &sect;1 and &sect;2."),
   ("Vadhan &mdash; Pseudorandomness (free)",
    "https://people.seas.harvard.edu/~salil/pseudorandomness/",
    "<b>Free in full, and the reference for &sect;3</b> — "
    "expanders, extractors, and generators, with the derandomisation "
    "applications."),
   ("Hoory, Linial & Wigderson &mdash; Expander Graphs and Their "
    "Applications (free)",
    "https://www.cs.huji.ac.il/~nati/PAPERS/expander_survey.pdf",
    "<b>&sect;3's expanders</b>, surveyed thoroughly and readably."),
   ("Luby & Wigderson &mdash; Pairwise Independence and Derandomization "
    "(free)",
    "https://people.eecs.berkeley.edu/~luca/cs278-08/luby-wigderson.pdf",
    "<b>&sect;2's technique</b>, with the constructions and the "
    "enumerate-all-seeds argument."),
 ],
 "exercises": [
   "<b>Derandomise the MAX-CUT algorithm</b> by conditional expectations "
   "and confirm the resulting greedy rule.",
   "<b>Verify the deterministic version achieves at least m/2</b> on "
   "random graphs.",
   "<b>Derandomise MAX-3SAT's 7/8 algorithm</b> the same way.",
   "<b>Find an algorithm where the conditional expectation is "
   "intractable</b> and say why the method fails.",
   "<b>Construct pairwise independent bits</b> from a logarithmic seed "
   "and verify the pairwise property.",
   "<b>Confirm they are not 3-wise independent.</b>",
   "<b>Take an analysis that used Chebyshev</b> and verify it still works "
   "with pairwise independence only.",
   "<b>Enumerate all seeds</b> for a small instance and confirm the "
   "derandomisation is complete.",
   "<b>Generate a random regular graph</b> and estimate its spectral gap "
   "to confirm it is an expander.",
   "<b>For your own randomised algorithm, decide whether to derandomise "
   "it</b>, using §4's five criteria.",
 ],
 "selfcheck": [
   "State the method of conditional expectations and derive the MAX-CUT "
   "greedy rule from it.",
   "What does the method require, and when does it fail?",
   "Why is it the method to try first?",
   "Why does pairwise independence cost only O(log n) bits?",
   "Which analyses does it support, and which does it not?",
   "Explain the enumerate-all-seeds argument.",
   "What is an expander, and what does a walk on one buy?",
   "What is the conditional result about BPP = P?",
   "Give five criteria for whether to derandomise.",
   "Why should you never derandomise the adversary use?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Using Randomness Honestly",
 "subtitle": "Seeds, sources, and claims you can support.",
 "question": "What does a randomised result actually guarantee?",
 "outcomes": [
     "Report a randomised result reproducibly.",
     "Explain how a weak random source voids a guarantee.",
     "Distinguish the kinds of random source and their uses.",
     "Measure a failure probability against its bound.",
     "State what a randomised algorithm honestly promises.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Reproducibility",
   "blurb": "The engineering discipline."},

  {"t": "bullets", "kicker": "Reproducibility", "title": "What a reproducible randomised experiment requires",
   "items": [
     "<b>An explicit seed, logged with the result.</b> <b>A result "
     "you cannot reproduce is a result you cannot debug</b>, and "
     "'it worked yesterday' is not a report.",
     "",
     "<b>Multiple seeds, with the spread reported</b> — "
     "<b>CSCE 642 §12's five minimum, and "
     "CSCE 658 §09's four chains, are the same "
     "discipline.</b>",
     "",
     "<b>A named generator and library version.</b> <b>Generators "
     "differ between versions and languages</b>, so a seed alone does "
     "not determine the stream.",
     "",
     "<b>Per-component seeding</b> — one global seed produces "
     "coupling between unrelated components, and a change in one shifts "
     "the others.",
     "",
     "<b>And a record of what was <i>not</i> controlled</b> "
     "— thread scheduling, hash iteration order, GPU "
     "non-determinism. <b>Full determinism is usually unattainable; "
     "say so.</b>",
   ],
   "footnote": "<b>The last point is the honest one:</b> <b>claim "
               "reproducibility only for what you actually "
               "controlled</b>, and list the rest."},

  {"t": "callout", "title": "Measure the failure rate, and compare it against your bound",
   "kind": "The central discipline of the course",
   "body": ["<b>You derived a bound in Module 02. Now run the algorithm "
            "enough times to estimate the actual failure rate.</b>",
            "<b>And they will differ</b> — <b>the bound is "
            "worst-case over inputs and the measurement is on yours, so "
            "the measured rate is usually far better.</b>",
            "<b>Report both.</b> <b>'Bound 10⁻⁶, measured "
            "3 × 10⁻⁹ over 10⁹ trials' is a far "
            "stronger statement than either alone</b> — it "
            "establishes the guarantee and demonstrates the "
            "practice.",
            "<b>And if the measurement is <i>worse</i> than the "
            "bound, something is wrong</b> — <b>usually an "
            "independence assumption that does not hold, or a weak "
            "generator</b> (Part 2). <b>Which makes the comparison a "
            "test of your analysis as well as of your code.</b>"]},

  {"t": "section", "label": "Part 2", "title": "The source",
   "blurb": "Where a guarantee actually goes wrong."},

  {"t": "table", "kicker": "Sources", "title": "The kinds of random source, and what each is for",
   "header": ["Source", "Use it for", "Never for"],
   "widths": [2.7, 4.1, 4.3],
   "rows": [
     ["<b>Mersenne Twister, PCG</b>", "<b>Simulation, algorithms, sampling</b>", "<b>Anything adversarial</b>"],
     ["<b>OS CSPRNG (urandom)</b>", "<b>Keys, nonces, tokens, salts</b>", "<b>Nothing — it is always safe</b>"],
     ["<b>A fixed seed</b>", "<b>Reproducible experiments</b>", "<b>Production, ever</b>"],
     ["<b>Time-based seed</b>", "<b>Nothing</b>", "<b>Everything — it is guessable</b>"],
     ["<b>Hardware RNG</b>", "<b>Seeding a CSPRNG</b>", "<b>Direct use without whitening</b>"],
   ],
   "footnote": "<b>The time-based seed row is not pedantry:</b> "
               "<b>seeding from the clock has broken real cryptographic "
               "systems</b>, because the clock's entropy is a handful of "
               "bits at best.",
   "note": "The time-seed failure is a real and repeated class of "
           "incident."},

  {"t": "callout", "title": "A weak source voids the guarantee rather than degrading it",
   "kind": "The failure mode to understand",
   "body": ["<b>Every bound in this course assumes the randomness is "
            "what you said it was</b> — independent, uniform, and "
            "unknown to the adversary.",
            "<b>And a weak source breaks the assumption "
            "completely</b> — <b>a predictable generator against an "
            "adversary gives a worst-case input, not a slightly worse "
            "average</b> (Module 01 §1).",
            "<b>The documented failures are real:</b> <b>predictable "
            "session tokens, keys generated with insufficient boot "
            "entropy, and hash-flooding against unrandomised hash "
            "tables</b> have all caused serious incidents.",
            "<b>So the test is cheap and worth doing:</b> <b>run your "
            "algorithm with a deliberately weak generator and see whether "
            "the guarantee survives</b> — <b>and if the result is "
            "unchanged, your randomness was not doing what you "
            "thought.</b>"]},

  {"t": "section", "label": "Part 3", "title": "The claim",
   "blurb": "What a randomised result honestly promises."},

  {"t": "bullets", "kicker": "Claims", "title": "What you can honestly assert",
   "items": [
     "<b>'Expected O(n log n), with probability at least "
     "1 − n⁻² of exceeding twice that; measured over "
     "10⁶ runs, the maximum was 1.3× the mean.'</b> <b>The "
     "bound and the measurement.</b>",
     "",
     "<b>'Failure probability at most 2⁻⁴⁰ assuming "
     "independent uniform bits from the OS source.'</b> <b>The "
     "assumption named, because it is where failures come from.</b>",
     "",
     "<b>'Estimate within 2% with 99% confidence, from 1.5 KB; "
     "measured error 0.4% on our data.'</b> <b>A sketch's claim, both "
     "sides.</b>",
     "",
     "<b>'Results over ten seeds; interquartile mean 312, range 280 to "
     "340; seeds and library version in the appendix.'</b>",
     "",
     "<b>And what you cannot say: 'it is fast' or 'it works'</b> "
     "— <b>without the probability, the assumption, or the "
     "seeds.</b>",
   ],
   "footnote": "<b>Every honest claim here names the probability and the "
               "randomness assumption</b> — the first because it is "
               "the guarantee and the second because it is what the "
               "guarantee rests on."},

  {"t": "callout", "title": "The three questions to ask of any randomised result",
   "kind": "Reading other people's work",
   "body": ["<b>What is the failure probability, and is it bounded or "
            "merely observed?</b> <b>An unbounded empirical rate is a "
            "measurement, not a guarantee.</b>",
            "<b>What does the analysis assume about the randomness?</b> "
            "<b>Independence is the usual assumption and the usual place "
            "it fails</b> (Module 02 §2).",
            "<b>How many seeds, and is the spread shown?</b> "
            "<b>CSCE 642 §12's question, and it applies "
            "here identically.</b>",
            "<b>And the three are in order of how often they are "
            "omitted</b> — <b>the seed count is usually missing, the "
            "independence assumption is usually unstated, and the failure "
            "probability is usually there.</b>"]},

  {"t": "section", "label": "Part 4", "title": "The semester",
   "blurb": "Three courses, closed."},

  {"t": "table", "kicker": "Semester 8", "title": "What each course established",
   "header": ["Course", "Asked", "And answered"],
   "widths": [2.3, 3.6, 5.4],
   "rows": [
     ["<b>CSCE 627</b>", "<b>Can it be done at all?</b>", "<b>Unconditionally. Proofs that do not expire</b>"],
     ["<b>CSCE 637</b>", "<b>What does it cost?</b>", "<b>Mostly conditionally; three barriers explain why</b>"],
     ["<b>CSCE 658</b>", "<b>Does a coin help?</b>", "<b>Demonstrably, in practice; removability open</b>"],
   ],
   "footnote": "<b>And this course is the one whose content you will use "
               "most</b> — hashing, sketches, sampling, backoff, and "
               "two choices are in everything, while the other two "
               "courses change how you think rather than what you "
               "write.",
   "note": "Being clear about which course is immediately practical is "
           "honest."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can derive a failure bound with the right "
            "inequality, state the independence assumption, and measure "
            "whether the derivation held.</b>",
            "<b>You can design a sketch, a randomised data structure, or "
            "a rounding scheme, and bound its error</b> — which covers "
            "most of what randomness is used for in systems.",
            "<b>And you can recognise where randomness is "
            "<i>necessary</i></b> (Module 11) <b>rather than "
            "convenient, and where it should be removed</b> "
            "(Module 12).",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it means naming the "
            "randomness assumption and the seed</b> — because <b>every "
            "guarantee in this course is conditional on a source being "
            "what you said it was.</b>"]},
 ],
 "takeaways": [
   "A result you cannot reproduce is a result you cannot debug, so log the "
   "seed, the generator, and the library version.",
   "Seed per component rather than globally, and record what you could not "
   "control — full determinism is usually unattainable.",
   "Derive the bound and then measure the rate, and report both: the bound "
   "is the guarantee and the measurement is the practice.",
   "If the measurement is worse than the bound, an independence assumption "
   "or the generator is wrong — so the comparison tests the analysis "
   "too.",
   "A weak source voids the guarantee rather than degrading it, because a "
   "predictable generator against an adversary gives a worst-case input.",
   "Every honest claim names the probability and the randomness "
   "assumption, because the second is what the first rests on.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Reproducibility, and measuring the bound"),
  ("ul", ["<b>An explicit seed, logged alongside the result.</b> <b>A "
          "result you cannot reproduce is a result you cannot debug</b>, "
          "and 'it worked yesterday' is not a report — which is "
          "obvious and is omitted constantly.",
          "<b>Multiple seeds, with the spread reported</b> — "
          "<b>CSCE 642 Module 12's five-seed minimum and Module 09 "
          "&sect;4's four chains are the same discipline in different "
          "settings</b>, and the reason is identical: a single run of a "
          "stochastic process is an anecdote.",
          "<b>A named generator and library version.</b> <b>Generators "
          "differ between library versions and between languages</b>, so "
          "<b>a seed alone does not determine the random stream</b> "
          "— and a library upgrade silently changing your results is "
          "a genuinely confusing failure.",
          "<b>Per-component seeding rather than one global seed.</b> "
          "<b>A single global generator couples unrelated components</b>, "
          "so adding one extra draw in one place shifts every subsequent "
          "value everywhere — which makes bisecting a regression "
          "impossible.",
          "<b>And a record of what was <i>not</i> controlled</b> "
          "— thread scheduling, hash iteration order, floating-point "
          "reduction order, GPU kernel non-determinism. <b>Full "
          "determinism is usually unattainable, and the honest position is "
          "to claim reproducibility only for what you actually controlled "
          "and to list the rest.</b>"]),
  ("callout", "Measure the failure rate, and compare it against your bound",
   ["<b>You derived a bound in Module 02. Now run the algorithm enough "
    "times to estimate the actual failure rate on your inputs.</b> <b>This "
    "is the central activity of the course</b>, and it is what the first "
    "project is built around.",
    "<b>And they will differ</b> — <b>the bound is worst-case over "
    "all inputs and the measurement is on yours, so the measured rate is "
    "usually far better</b>, frequently by orders of magnitude "
    "(Module 05 &sect;4's caveat, which is good news).",
    "<b>Report both.</b> <b>'Bound 10<super>&minus;6</super>, measured "
    "3 &times; 10<super>&minus;9</super> over 10<super>9</super> trials' "
    "is a far stronger statement than either figure alone</b> — the "
    "bound establishes the guarantee and the measurement demonstrates the "
    "practice.",
    "<b>And if the measurement is <i>worse</i> than the bound, something "
    "is wrong</b> — <b>usually an independence assumption that does "
    "not actually hold</b> (Module 02 &sect;4's commonest error) "
    "<b>or a weak generator</b> (&sect;2). <b>Which makes the comparison "
    "a test of your analysis as well as of your implementation</b>, and "
    "that dual role is why it is worth the effort."]),

  ("h1", "2 &nbsp; The source"),
  ("table", ["Source", "Use it for", "Never use it for"],
   [["<b>Mersenne Twister, PCG, xoshiro</b>",
     "<b>Simulation, randomised algorithms, sampling, shuffling for "
     "non-adversarial purposes.</b>",
     "<b>Anything adversarial</b> — these are predictable from a "
     "modest number of outputs."],
    ["<b>The OS cryptographic source</b> (<code>urandom</code>, "
     "<code>getrandom</code>, <code>BCryptGenRandom</code>)",
     "<b>Keys, nonces, session tokens, salts, and anything an adversary "
     "might try to predict.</b>",
     "<b>Nothing — it is always safe</b>, and the performance "
     "objection is obsolete on modern systems."],
    ["<b>A fixed, logged seed</b>",
     "<b>Reproducible experiments and tests.</b>",
     "<b>Production, ever</b> — a shipped fixed seed is a "
     "predictable system."],
    ["<b>A time-based seed</b>", "<b>Nothing.</b>",
     "<b>Everything</b> — see the note."],
    ["<b>A hardware RNG instruction or device</b>",
     "<b>Seeding a cryptographic generator.</b>",
     "<b>Direct use without whitening or health testing</b>, since the "
     "raw output may be biased."]],
   [0.24, 0.40, 0.36]),
  ("p", "<b>The time-based seed row is not pedantry.</b> <b>Seeding from "
        "the clock has broken real cryptographic systems</b>, because the "
        "clock's entropy as seen by an attacker who knows roughly when the "
        "key was generated is a handful of bits — which is "
        "exhaustively searchable. <b>It is a repeated class of incident "
        "rather than a theoretical concern</b>, and the fix is free."),
  ("callout", "A weak source voids the guarantee rather than degrading it",
   ["<b>Every bound in this course assumes the randomness is what you "
    "said it was</b> — independent, uniform, and (for the adversary "
    "use) unknown to whoever is choosing the input.",
    "<b>And a weak source breaks the assumption completely rather than "
    "partially.</b> <b>A predictable generator against an adversary gives "
    "you a worst-case input, not a slightly worse average</b> "
    "(Module 01 &sect;1) — the adversary computes your choices "
    "and constructs the input that defeats them. <b>The guarantee does "
    "not degrade; it disappears.</b>",
    "<b>The documented failures are real and numerous:</b> <b>predictable "
    "session tokens allowing account takeover, cryptographic keys "
    "generated with insufficient entropy at first boot (which produced "
    "thousands of duplicate keys in deployed devices), and hash-flooding "
    "denial of service against unrandomised hash tables</b> have all "
    "caused serious incidents.",
    "<b>So the test is cheap and worth doing:</b> <b>run your algorithm "
    "with a deliberately weak generator — a short-period one, or one "
    "seeded identically every time — and see whether the guarantee "
    "survives.</b> <b>And if the result is entirely unchanged, your "
    "randomness was not doing what you thought it was doing</b>, which is "
    "itself worth discovering. <b>This is the one experiment in the "
    "course that nobody runs.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; The claim"),
  ("ul", ["<b>'Expected O(n log n) time, with probability at least "
          "1 &minus; n<super>&minus;2</super> of not exceeding twice "
          "that; measured over 10<super>6</super> runs, the maximum "
          "observed was 1.3 times the mean.'</b> <b>The bound and the "
          "measurement together</b> (&sect;1).",
          "<b>'Failure probability at most 2<super>&minus;40</super>, "
          "assuming independent uniform bits from the operating system's "
          "source.'</b> <b>The assumption named explicitly, because that "
          "is where failures actually come from</b> (&sect;2).",
          "<b>'Estimates within 2% with 99% confidence from 1.5 KB of "
          "state; measured error 0.4% on our production data over a "
          "month.'</b> <b>A sketch's claim, with both sides</b> "
          "(Module 05 &sect;4).",
          "<b>'Results over ten seeds; interquartile mean 312, range 280 "
          "to 340; the seeds and the library version are in the "
          "appendix.'</b> <b>Which is CSCE 642 Module 12's "
          "reporting standard, and it transfers directly.</b>",
          "<b>And what you cannot honestly say: 'it is fast' or 'it "
          "works'</b> — <b>without the probability, without the "
          "randomness assumption, or without the seeds.</b> <b>Every "
          "honest claim above names the probability and the "
          "assumption</b>: the first because it <i>is</i> the guarantee, "
          "and the second because it is what the guarantee rests on."]),
  ("callout", "The three questions to ask of any randomised result",
   ["<b>What is the failure probability, and is it <i>bounded</i> or "
    "merely <i>observed</i>?</b> <b>An unbounded empirical rate is a "
    "measurement rather than a guarantee</b> — useful, and a "
    "different kind of claim.",
    "<b>What does the analysis assume about the randomness?</b> "
    "<b>Independence is the usual assumption and the usual place it "
    "fails</b> (Module 02 &sect;2), and an analysis that does not state "
    "its independence assumption has probably not checked it.",
    "<b>How many seeds, and is the spread shown?</b> <b>CSCE 642 "
    "Module 12's question, and it applies here identically</b> — a "
    "randomised algorithm reported from one run is reported from an "
    "anecdote.",
    "<b>And the three are listed in order of how often they are "
    "omitted</b> — <b>the seed count is usually missing entirely, "
    "the independence assumption is usually unstated, and the failure "
    "probability is usually present</b>, which means the reporting is "
    "weakest exactly where it is easiest to fix."]),

  ("h1", "4 &nbsp; The semester, and the close"),
  ("table", ["Course", "Asked", "And answered"],
   [["<b>CSCE 627</b>", "<b>Can it be done at all?</b>",
     "<b>Unconditionally, with proofs that do not expire</b> "
     "(CSCE 627 Module 13 &sect;1)."],
    ["<b>CSCE 637</b>", "<b>What does it cost?</b>",
     "<b>Mostly conditionally, and three barrier results explain why the "
     "central question is open</b> (CSCE 637 Module 13 "
     "&sect;1)."],
    ["<b>CSCE 658 (this one)</b>", "<b>Does a coin help?</b>",
     "<b>Demonstrably and repeatedly in practice; whether it is ever "
     "<i>essential</i> for a complexity class is open</b> "
     "(Module 12 &sect;3)."]],
   [0.22, 0.30, 0.48]),
  ("p", "<b>And this is the course whose content you will use most.</b> "
        "<b>Hashing, sketches, sampling, randomised backoff, and the power "
        "of two choices are in essentially everything you will "
        "build</b> — <b>while CSCE 627 and CSCE 637 change how you "
        "think about problems rather than what you write.</b> <b>Being "
        "clear about which of the three is immediately practical is "
        "honest</b>, and it is not a judgement about which is more "
        "valuable."),
  ("callout", "Where this course leaves you",
   ["<b>You can derive a failure bound using the right inequality from "
    "Module 02's ladder, state the independence assumption it needs, and "
    "measure whether the derivation actually held</b> — which is the "
    "core competence and is what the projects assess.",
    "<b>You can design a sketch, a randomised data structure, or a "
    "rounding scheme and bound its error</b> — <b>which covers most "
    "of what randomness is actually used for in systems</b> "
    "(Modules 04, 05, 08).",
    "<b>And you can recognise where randomness is "
    "<i>necessary</i></b> (Module 11's symmetry breaking and consensus) "
    "<b>rather than merely convenient, and where it should be removed "
    "again</b> (Module 12's four criteria).",
    "<b>The closing rule is the program's, unchanged across twenty-four "
    "courses:</b> <b>state what you measured, state what you assumed, "
    "and never claim more than you established.</b> <b>In this course it "
    "means naming the randomness assumption and the seed</b> — "
    "<b>because every single guarantee in these thirteen modules is "
    "conditional on a source being what you said it was</b>, and that is "
    "the assumption nobody writes down."]),
 ],
 "resources": [
   ("Agarwal et al. &mdash; Deep RL at the Edge of the Statistical "
    "Precipice (free)",
    "https://arxiv.org/abs/2108.13264",
    "<b>&sect;1's reporting standard</b>, developed for reinforcement "
    "learning and applicable unchanged here — with free tooling."),
   ("O'Neill &mdash; PCG, and the random number generator survey "
    "(free)",
    "https://www.pcg-random.org/",
    "<b>&sect;2's generators compared</b>, including the statistical "
    "tests and the predictability discussion."),
   ("Heninger et al. &mdash; Mining Your Ps and Qs (free)",
    "https://factorable.net/weakkeys12.extended.pdf",
    "<b>&sect;2's boot-entropy failure, measured in the wild</b> "
    "— thousands of duplicate keys in deployed devices. The "
    "canonical example."),
   ("Brooker &mdash; the AWS architecture posts on jitter and "
    "timeouts (free)",
    "https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/",
    "<b>Module 11 &sect;1's practice, documented</b> — and a "
    "model for how to report a randomised design decision."),
 ],
 "exercises": [
   "<b>Take every experiment from this course and make it "
   "reproducible</b>: explicit seeds, named generator, logged "
   "versions.",
   "<b>Switch to a global seed</b> and demonstrate the coupling between "
   "components.",
   "<b>Measure the failure rate of three algorithms</b> you implemented "
   "and compare against your bounds.",
   "<b>Find one where the measurement is worse than the bound</b>, and "
   "diagnose it.",
   "<b>Run one algorithm with a deliberately weak generator</b> and "
   "report whether the guarantee survived.",
   "<b>Seed a generator from the clock</b> and estimate how many seeds an "
   "attacker would need to try.",
   "<b>Write the honest claim</b> for each algorithm in your first "
   "project.",
   "<b>Apply the three questions</b> to a published randomised result and "
   "report what was missing.",
   "<b>Revisit what you wrote in Module 01's last exercise</b> and report "
   "what changed.",
   "<b>Project 2 is now due.</b> Submit the problem, the deterministic "
   "baseline measured, the randomised algorithm with its derived and "
   "measured failure probability, ten seeds with the spread, the "
   "weak-generator sensitivity test, a derandomisation attempt or an "
   "argument against one, and the honest claim.",
 ],
 "selfcheck": [
   "Name five requirements for a reproducible randomised experiment.",
   "Why seed per component rather than globally?",
   "Why report both the bound and the measured rate?",
   "What does it mean if the measurement is worse than the bound?",
   "Name five random sources and what each is and is not for.",
   "Why is a time-based seed never acceptable?",
   "Why does a weak source void rather than degrade a guarantee?",
   "Give four honest claims and the two things you cannot say.",
   "Give the three questions to ask of a randomised result, in order of "
   "omission.",
   "In this course, what does 'state what you assumed' mean?",
 ],
},

]
