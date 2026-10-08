# -*- coding: utf-8 -*-
"""CSCE 625 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Logic and Satisfiability",
 "subtitle": "The most useful tool nobody mentions.",
 "question": "What can you get from stating a problem as a logical "
             "formula?",
 "outcomes": [
     "Express a problem in propositional logic.",
     "Explain resolution and why it is complete.",
     "Explain what a modern SAT solver does and why it is fast.",
     "Encode a real problem into CNF and solve it.",
     "State what first-order logic adds and what it costs.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Propositional logic",
   "blurb": "Variables, clauses, and one normal form."},

  {"t": "callout", "title": "Everything reduces to conjunctive normal form",
   "kind": "Why one representation suffices",
   "body": ["<b>A CNF formula is a conjunction of clauses, each a "
            "disjunction of literals.</b> Every propositional formula "
            "has an equivalent CNF.",
            "<b>So a solver only needs to handle one syntactic "
            "form</b>, which is why SAT solvers take CNF and nothing "
            "else.",
            "<b>Naive conversion can blow up exponentially</b> "
            "— so the Tseitin transformation introduces auxiliary "
            "variables, giving a <i>linear-size</i> formula that is "
            "satisfiability-equivalent rather than logically "
            "equivalent.",
            "<b>That distinction matters:</b> <b>Tseitin preserves "
            "whether a model exists, not the set of models</b> — "
            "which is all you need for SAT and not enough for "
            "counting."]},

  {"t": "table", "kicker": "Encodings", "title": "Common patterns in CNF",
   "header": ["Want", "Clauses", "Note"],
   "widths": [2.8, 4.0, 5.3],
   "rows": [
     ["<b>At least one of xᵢ</b>", "<b>(x₁ ∨ x₂ ∨ …)</b>", "<b>One clause. Trivial</b>"],
     ["<b>At most one of xᵢ</b>", "<b>(¬xᵢ ∨ ¬xⱼ) for all pairs</b>", "<b>O(n²). Use a ladder encoding for large n</b>"],
     ["<b>Exactly one</b>", "<b>Both of the above</b>", "<b>The workhorse for 'choose one value'</b>"],
     ["<b>Implication a → b</b>", "(¬a ∨ b)", "One clause"],
     ["<b>Cardinality ≤ k</b>", "<b>Sequential counter encoding</b>", "<b>O(nk). Do not expand pairwise</b>"],
   ],
   "footnote": "<b>The at-most-one encoding is where naive CNF "
               "generation goes wrong</b> — pairwise is O(n²) "
               "clauses and a sequential encoding is O(n), which matters "
               "at scale.",
   "note": "Encoding skill is what separates usable SAT from unusable "
           "SAT."},

  {"t": "section", "label": "Part 2", "title": "How solvers got fast",
   "blurb": "CDCL, and why it is not just backtracking."},

  {"t": "code", "kicker": "CDCL", "title": "Conflict-driven clause learning",
   "lang": "text", "code": """
  DPLL (1962): backtracking plus UNIT PROPAGATION --
  if a clause has one unassigned literal and the rest are
  false, that literal must be true. Propagate; cascade.
      (This is Module 06's arc consistency, for clauses.)

  CDCL adds the thing that changed everything:

  WHEN A CONFLICT OCCURS, ANALYSE WHY.
      Walk the implication graph back to find the set of
      decisions responsible, and LEARN A NEW CLAUSE
      forbidding that combination.
      Add it permanently. Then BACKJUMP to the level that
      actually caused the conflict -- not one level up.

  WHY THIS IS SO POWERFUL
      the learned clause prunes EVERYWHERE in the remaining
          search, not just here -- it is a derived fact
      backjumping skips entire irrelevant subtrees
      and VSIDS activity-based variable ordering focuses
          on variables appearing in recent conflicts, which
          adapts to the formula's structure during search

  THE RESULT: solvers handle formulas with MILLIONS of
  variables routinely. SAT is NP-complete and solvers are
  industrial infrastructure -- the same situation as
  CSCE 669's integer programming, for the same reasons.
""",
   "caption": "<b>Learning from failure is the idea</b> — a "
              "conflict is not just a dead end to retreat from but "
              "information to generalise.",
   "note": "The 'conflict is information' framing is the key insight."},

  {"t": "callout", "title": "Resolution, and why completeness matters",
   "kind": "The theoretical basis",
   "body": ["<b>From (a ∨ X) and (¬a ∨ Y), infer "
            "(X ∨ Y).</b> That single rule is resolution.",
            "<b>It is refutation-complete:</b> <b>if a CNF formula is "
            "unsatisfiable, repeated resolution derives the empty "
            "clause</b> — so a proof always exists.",
            "<b>CDCL's learned clauses <i>are</i> resolution "
            "derivations</b>, which is why a CDCL solver can emit a "
            "machine-checkable proof of unsatisfiability.",
            "<b>And that is the practically important part:</b> "
            "<b>'unsatisfiable' is a checkable claim, not a trusted "
            "one</b> — which is why SAT is usable in verification "
            "where a wrong answer is unacceptable."]},

  {"t": "section", "label": "Part 3", "title": "Using it",
   "blurb": "Problems worth encoding."},

  {"t": "bullets", "kicker": "Applications", "title": "What people actually solve with SAT",
   "items": [
     "<b>Hardware and software verification.</b> <b>The largest real "
     "application by far</b> — bounded model checking is a SAT "
     "query.",
     "",
     "<b>Package dependency resolution.</b> Your package manager is "
     "running a SAT solver.",
     "",
     "<b>Scheduling and configuration</b> — though a CP or MIP "
     "solver is often better when there are costs (CSCE 669 M13).",
     "",
     "<b>Puzzle solving and generation</b>, including <b>'does this "
     "generated level have exactly one solution?'</b>",
     "",
     "<b>And SMT extends it</b> — SAT plus theories (arithmetic, "
     "arrays, bit-vectors), which is what program verifiers use.",
   ],
   "footnote": "<b>Reach for a SAT or SMT solver before writing a "
               "custom search</b> for anything with a purely "
               "combinatorial feasibility question — the solver is "
               "decades ahead of what you will write."},

  {"t": "section", "label": "Part 4", "title": "First-order logic",
   "blurb": "What quantifiers add, and what they cost."},

  {"t": "callout", "title": "First-order logic buys generality and loses decidability",
   "kind": "The trade, stated",
   "body": ["<b>Propositional logic has no variables over objects</b> "
            "— you must enumerate 'Mortal(Socrates)', "
            "'Mortal(Plato)', and so on.",
            "<b>First-order logic adds quantifiers and relations</b>, so "
            "one sentence covers all objects — which is enormously "
            "more compact and is how knowledge is naturally stated.",
            "<b>The cost is that validity becomes undecidable.</b> It "
            "is <i>semi</i>-decidable: a proof will be found if one "
            "exists, and otherwise the search may not terminate.",
            "<b>So practical systems restrict it:</b> <b>Datalog, "
            "description logics, and answer set programming each give up "
            "expressiveness for decidability</b> — and the "
            "restriction is the engineering, not a compromise."]},

  {"t": "callout", "title": "Where logic sits relative to the rest of the course",
   "kind": "Placing it honestly",
   "body": ["<b>Logic was the dominant paradigm for thirty years and is "
            "now a specialised tool</b>, which is a fair description "
            "rather than a dismissal.",
            "<b>What survived is the solvers.</b> <b>SAT and SMT are "
            "industrial infrastructure</b>; general-purpose logical "
            "knowledge bases largely are not.",
            "<b>What failed was brittleness:</b> real knowledge has "
            "exceptions, and classical logic has no graceful way to say "
            "'usually' — which is Module 09's subject.",
            "<b>So the honest summary is:</b> <b>use logic where the "
            "domain really is crisp and the question is feasibility; use "
            "probability where it is not.</b>"]},
 ],
 "takeaways": [
   "Every propositional formula has a CNF equivalent, which is why solvers "
   "accept only CNF — and Tseitin keeps the conversion linear by "
   "preserving satisfiability rather than models.",
   "Encoding skill decides usability: at-most-one is O(n²) pairwise "
   "and O(n) with a sequential encoding.",
   "Unit propagation is Module 06's arc consistency applied to clauses.",
   "CDCL's contribution is treating a conflict as information to "
   "generalise rather than a dead end to retreat from.",
   "Learned clauses are resolution derivations, so a solver can emit a "
   "checkable proof of unsatisfiability.",
   "First-order logic buys compactness and loses decidability, so "
   "practical systems use restricted fragments.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Propositional logic and CNF"),
  ("callout", "Everything reduces to conjunctive normal form",
   ["<b>A CNF formula is a conjunction of clauses, each clause a "
    "disjunction of literals (a variable or its negation).</b> <b>Every "
    "propositional formula has a logically equivalent CNF form.</b>",
    "<b>So a solver needs to handle only one syntactic form</b>, which is "
    "why SAT solvers accept CNF and nothing else — a deliberate "
    "simplification that pushes the conversion work onto the user and "
    "lets the solver be extremely well optimised for one case.",
    "<b>Naive conversion can blow up exponentially</b> (distributing a "
    "disjunction over a large conjunction), <b>so the Tseitin "
    "transformation introduces auxiliary variables naming each "
    "subformula</b>, producing a <i>linear-size</i> formula that is "
    "satisfiability-equivalent rather than logically equivalent.",
    "<b>That distinction matters.</b> <b>Tseitin preserves whether a "
    "model exists, not the set of models</b> — the auxiliary "
    "variables are determined by the originals, so a satisfying "
    "assignment restricts correctly, <b>but model <i>counting</i> over "
    "the Tseitin form is not the same as over the original</b>. <b>Which "
    "bites exactly when you want 'exactly one solution'</b> (&sect;3) and "
    "is worth knowing before you discover it."]),
  ("table", ["What you want", "Clauses", "Note"],
   [["<b>At least one of x<sub>1</sub>&hellip;x<sub>n</sub></b>",
     "<b>(x<sub>1</sub> &or; x<sub>2</sub> &or; &hellip; &or; "
     "x<sub>n</sub>)</b>",
     "<b>One clause. Trivial.</b>"],
    ["<b>At most one of x<sub>1</sub>&hellip;x<sub>n</sub></b>",
     "<b>(&not;x<sub>i</sub> &or; &not;x<sub>j</sub>) for every "
     "pair.</b>",
     "<b>O(n&#178;) clauses.</b> <b>Use a sequential (ladder) encoding "
     "with auxiliary variables for large n</b>, which is O(n) — see "
     "the footnote."],
    ["<b>Exactly one</b>", "<b>Both of the above conjoined.</b>",
     "<b>The workhorse for 'this variable takes exactly one value', "
     "which is how a CSP (Module 06) is encoded into SAT.</b>"],
    ["<b>Implication a &rarr; b</b>", "(&not;a &or; b)",
     "One clause. All of propositional reasoning about rules reduces to "
     "this shape."],
    ["<b>Cardinality: at most k of n</b>",
     "<b>A sequential counter encoding with auxiliary "
     "variables.</b>",
     "<b>O(nk) clauses. Do not expand it as all (k+1)-subsets</b>, which "
     "is what a naive implementation does and is immediately "
     "hopeless."]],
   [0.23, 0.33, 0.44]),
  ("p", "<b>The at-most-one encoding is where naive CNF generation goes "
        "wrong</b>, and it is worth internalising because it recurs in "
        "every encoding: <b>pairwise is O(n&#178;) clauses while a "
        "sequential encoding is O(n)</b>, and at n in the thousands the "
        "difference decides whether the solver sees the problem at all. "
        "<b>Encoding skill is what separates usable SAT from unusable "
        "SAT</b>, and it is the part that is learned by doing rather than "
        "by reading."),

  ("h1", "2 &nbsp; How solvers became fast"),
  ("code", """DPLL (1962): backtracking search plus UNIT PROPAGATION --
if a clause has exactly one unassigned literal and all the
others are false, that literal MUST be true. Propagate it,
and let the consequences cascade.
    (This is Module 06's arc consistency, specialised to
     clauses -- the same inference, the same cascade.)

CDCL adds the thing that changed everything:

WHEN A CONFLICT OCCURS, ANALYSE WHY IT OCCURRED.
    Walk the implication graph backwards to identify the
    set of decisions responsible, and LEARN A NEW CLAUSE
    forbidding exactly that combination. Add it to the
    formula permanently. Then BACKJUMP to the decision
    level that actually caused the conflict -- not merely
    one level up, which may be irrelevant.

WHY THIS IS SO POWERFUL
    the learned clause prunes EVERYWHERE in the remaining
        search, not only here -- it is a derived fact about
        the formula, valid globally
    backjumping skips entire irrelevant subtrees, which is
        Module 06's conflict-directed backjumping
    and VSIDS activity-based variable ordering focuses on
        variables appearing in recent conflicts, so the
        ordering ADAPTS to the formula's structure during
        the search rather than being fixed in advance

THE RESULT: solvers handle formulas with MILLIONS of
variables routinely. SAT is NP-complete and SAT solvers are
industrial infrastructure -- exactly the situation of
CSCE 669 Module 09's integer programming, for exactly the
same reasons."""),
  ("p", "<b>Learning from failure is the idea</b>, and it is worth stating "
        "in those terms: <b>a conflict is not merely a dead end to "
        "retreat from, but information about the formula that can be "
        "generalised and reused</b>. <b>That reframing is the whole "
        "advance</b>, and it generalises beyond SAT — the same "
        "principle appears in CSCE 669 Module 09's cutting planes, "
        "where a violated constraint becomes a globally valid inequality "
        "rather than a local rejection."),
  ("callout", "Resolution, and why completeness matters",
   ["<b>From (a &or; X) and (&not;a &or; Y), infer (X &or; Y).</b> That "
    "single inference rule is resolution, and it is the whole proof "
    "system for propositional logic.",
    "<b>It is refutation-complete:</b> <b>if a CNF formula is "
    "unsatisfiable, repeated application of resolution will derive the "
    "empty clause</b> — so a finite proof of unsatisfiability always "
    "exists, even though finding it may take exponential time.",
    "<b>And CDCL's learned clauses <i>are</i> resolution "
    "derivations</b> — conflict analysis is a sequence of "
    "resolutions along the implication graph. <b>Which is why a CDCL "
    "solver can emit a machine-checkable proof of unsatisfiability</b> "
    "(a DRAT proof), verified independently of the solver.",
    "<b>And that is the practically important part.</b> "
    "<b>'Unsatisfiable' becomes a checkable claim rather than a trusted "
    "one</b> — which is why SAT is usable in hardware verification, "
    "where 'the solver says there is no bug' must not depend on the "
    "solver being correct. <b>It is the same discipline this program has "
    "insisted on throughout: a result with a certificate beats a result "
    "with a reputation.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; What people actually solve with SAT"),
  ("ul", ["<b>Hardware and software verification.</b> <b>The largest "
          "real application by a wide margin</b> — bounded model "
          "checking unrolls a system's transitions k steps and asks "
          "whether a bad state is reachable, which is a SAT query. Every "
          "major chip is verified partly this way.",
          "<b>Package dependency resolution.</b> <b>Your package "
          "manager is running a SAT solver</b> — 'find a set of "
          "package versions satisfying every dependency and conflict' is "
          "literally a satisfiability problem, and the switch to real "
          "solvers is why modern package managers resolve where older "
          "ones gave up.",
          "<b>Scheduling and configuration</b> — though <b>a "
          "constraint-programming or integer-programming solver is "
          "frequently better when there are costs to minimise</b> rather "
          "than only feasibility to establish (CSCE 669 Module 13 "
          "&sect;1), since SAT has no native notion of an objective.",
          "<b>Puzzle solving and generation</b>, including <b>'does this "
          "generated level have exactly one solution?'</b> — asked "
          "by solving, forbidding the solution found, and solving "
          "again (and note &sect;1's warning about counting over a "
          "Tseitin encoding).",
          "<b>And SMT extends it</b> — satisfiability modulo "
          "theories, which is SAT plus decision procedures for "
          "arithmetic, arrays, bit-vectors, and strings. <b>This is what "
          "program verifiers, symbolic execution engines, and type "
          "checkers for dependent types actually use</b>, and Z3 is "
          "free.",
          "<b>So reach for a SAT or SMT solver before writing a custom "
          "search</b> for anything whose core is a combinatorial "
          "feasibility question. <b>The solver embodies decades of work "
          "that you will not reproduce</b>, which is CSCE 669 "
          "Module 13's argument in a different setting."]),

  ("h1", "4 &nbsp; First-order logic, and where logic sits"),
  ("callout", "First-order logic buys generality and loses decidability",
   ["<b>Propositional logic has no variables ranging over objects</b>, so "
    "you must enumerate: Mortal(Socrates), Mortal(Plato), and one "
    "proposition per individual — which does not scale and does not "
    "generalise to objects you have not met.",
    "<b>First-order logic adds quantifiers, variables, and relations</b>, "
    "so a single sentence covers all objects. <b>Enormously more "
    "compact, and it is how knowledge is naturally stated</b>, which is "
    "why it dominated knowledge representation.",
    "<b>The cost is that validity becomes undecidable.</b> It is "
    "<i>semi</i>-decidable: <b>a proof will eventually be found if one "
    "exists, and if none exists the search may simply never "
    "terminate</b> — so you cannot distinguish 'no' from 'not yet' "
    "(CSCE 627's subject, which arrives next semester).",
    "<b>So practical systems restrict it.</b> <b>Datalog (no function "
    "symbols, bounded), description logics (the basis of ontology "
    "languages), and answer set programming each give up expressiveness "
    "to regain decidability and efficient solving</b> — and <b>the "
    "choice of restriction is the engineering work, not a "
    "compromise</b>, exactly as the choice of a convex formulation was in "
    "CSCE 669 Module 02."]),
  ("callout", "Where logic sits relative to the rest of the course",
   ["<b>Logic was the dominant paradigm in AI for roughly thirty years "
    "and is now a specialised tool</b>, which is a fair description "
    "rather than a dismissal — and the specialisation is in areas "
    "where it is not merely useful but indispensable.",
    "<b>What survived is the solvers.</b> <b>SAT and SMT are industrial "
    "infrastructure</b> running in compilers, verifiers, and package "
    "managers; <b>general-purpose logical knowledge bases largely are "
    "not</b>, despite very substantial effort.",
    "<b>What failed was brittleness.</b> <b>Real-world knowledge has "
    "exceptions — birds fly, except penguins, except injured ones, "
    "except in a sealed room — and classical logic has no graceful "
    "way to say 'usually'</b>. The attempts (default logic, "
    "non-monotonic reasoning) are technically interesting and did not "
    "resolve it, which is <b>Module 09's subject and the reason "
    "probability displaced logic for reasoning about the world.</b>",
    "<b>So the honest summary is:</b> <b>use logic where the domain "
    "really is crisp and the question is feasibility or correctness; use "
    "probability where the domain is uncertain and the question is what "
    "to believe.</b> <b>Circuits and package dependencies are crisp; "
    "whether the player is hiding behind that crate is not.</b>"]),
 ],
 "resources": [
   ("Russell & Norvig &mdash; AIMA, chapters 7–9 (pseudocode free)",
    "https://aima.cs.berkeley.edu/",
    "<b>Propositional and first-order logic, resolution, and DPLL</b> "
    "— the reference for &sect;1, &sect;2, and &sect;4."),
   ("Marques-Silva, Lynce & Malik &mdash; Conflict-Driven Clause "
    "Learning (free chapter)",
    "https://satassociation.org/",
    "<b>The &sect;2 mechanism</b>, by its originators, with the "
    "implication-graph analysis worked through."),
   ("Z3 and MiniSat documentation and tutorials (free)",
    "https://microsoft.github.io/z3guide/",
    "<b>The practical tools of &sect;3.</b> The Z3 guide is interactive "
    "and is the fastest way to become useful with SMT."),
   ("Biere, Heule, van Maaren & Walsh &mdash; Handbook of Satisfiability",
    "https://satassociation.org/",
    "<b>The comprehensive reference</b>, with several chapters free and "
    "the annual competition results that document &sect;2's "
    "progress."),
 ],
 "exercises": [
   "<b>Convert a formula to CNF naively</b> and watch it blow up.",
   "<b>Implement the Tseitin transformation</b> and confirm the size is "
   "linear.",
   "<b>Encode at-most-one pairwise and sequentially</b> for n = 1000 and "
   "compare clause counts and solve times.",
   "<b>Implement DPLL with unit propagation</b> and solve small "
   "instances.",
   "<b>Add conflict analysis and clause learning</b> and report the "
   "reduction in decisions.",
   "<b>Encode Sudoku into CNF</b> and compare a SAT solver against your "
   "Module 06 CSP solver.",
   "<b>Encode graph colouring</b> and find the chromatic number by "
   "repeated SAT calls.",
   "<b>Get an unsatisfiability proof</b> from a solver and check it with "
   "an independent checker.",
   "<b>Use Z3 on a problem with arithmetic</b> and compare against "
   "encoding the arithmetic into pure SAT.",
   "<b>Use SAT to verify a generated puzzle has exactly one "
   "solution.</b>",
 ],
 "selfcheck": [
   "What is CNF and why do solvers require it?",
   "What does Tseitin preserve, and what does it not?",
   "Give five CNF encoding patterns and the cost of each.",
   "What is unit propagation, and what is it in Module 06's terms?",
   "What does CDCL add to DPLL, and why is each part powerful?",
   "State resolution and explain refutation completeness.",
   "Why does a checkable proof matter in practice?",
   "Name five SAT applications.",
   "What does first-order logic buy and cost, and what do practical "
   "systems do?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Probabilistic Reasoning",
 "subtitle": "Saying 'usually' properly.",
 "question": "How do you represent and update uncertain beliefs?",
 "outcomes": [
     "Apply Bayes' rule and explain base rates.",
     "Explain conditional independence and why it makes inference "
     "possible.",
     "Build a Bayesian network and read independence off its "
     "structure.",
     "Perform exact inference by variable elimination.",
     "Choose an approximate method when exact inference is "
     "infeasible.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Bayes",
   "blurb": "Updating a belief with evidence."},

  {"t": "eq", "kicker": "Bayes", "title": "The rule, and the term people drop",
   "eqs": [
     ("P(H | E) = P(E | H) · P(H) / P(E)",
      "Posterior equals likelihood times prior, normalised."),
     ("P(H) is the PRIOR, and it is not optional",
      "Dropping it is the base-rate fallacy, and it is the single most "
      "common error in applied probability."),
     ("A test 99% accurate for a disease affecting 1 in 10,000",
      "gives a positive predictive value of about 1%. The prior "
      "dominates."),
   ],
   "caption": "<b>The arithmetic is trivial and the intuition is "
              "terrible</b>, which is why this example is worth "
              "computing by hand once rather than accepting.",
   "note": "Make students compute the 1% rather than telling them."},

  {"t": "callout", "title": "Conditional independence is what makes any of this tractable",
   "kind": "The idea the whole module rests on",
   "body": ["<b>A full joint distribution over n binary variables needs "
            "2ⁿ − 1 numbers.</b> At n = 30 that is a "
            "billion, and nobody can specify or store it.",
            "<b>But most variables are conditionally independent given "
            "a few others</b> — once you know whether it rained, the "
            "sprinkler tells you nothing more about the grass.",
            "<b>So the joint factorises into a product of small "
            "conditional distributions</b>, and the parameter count "
            "drops from exponential to linear in n.",
            "<b>That is the entire reason probabilistic AI is "
            "possible</b> — <b>and it is the same structural argument "
            "as Module 06's treewidth and CSCE 669's sparsity:</b> "
            "<b>structure, not size, decides tractability.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Bayesian networks",
   "blurb": "A graph whose structure is a claim about independence."},

  {"t": "code", "kicker": "Bayes nets", "title": "The representation 1/2: the graph",
   "lang": "text", "code": """
  A DIRECTED ACYCLIC GRAPH. Each node is a variable; each
  node carries P(node | its parents).

  THE JOINT FACTORISES:
      P(x1..xn) = product over i of P(xi | parents(xi))

  SO THE GRAPH IS A CLAIM ABOUT INDEPENDENCE, and THE
  MISSING EDGES CARRY THE INFORMATION. A fully connected
  network asserts nothing and costs as much as the full
  joint distribution it was meant to replace.
""",
   "caption": "<b>The absent edges are the content</b> — which is "
              "why drawing the graph is a modelling act and not a "
              "diagram.",
   "note": "Stress that a dense network has bought you nothing."},

  {"t": "code", "kicker": "d-separation", "title": "The representation 2/2: reading independence off it",
   "lang": "text", "code": """
  THREE PATTERNS, AND THAT IS ALL OF d-SEPARATION:

    CHAIN    A -> B -> C
             A and C independent GIVEN B. Knowing the
             intermediate blocks the path.

    FORK     A <- B -> C
             A and C independent GIVEN B. A common cause
             explains the correlation.

    COLLIDER A -> B <- C
             A and C independent -- UNTIL you observe B,
             and then they become DEPENDENT.

  THE COLLIDER IS THE COUNTERINTUITIVE ONE AND IT MATTERS.
  Your car will not start; the cause is the battery or the
  fuel pump; learning the battery is fine makes the fuel
  pump more likely. THAT IS EXPLAINING AWAY.
""",
   "caption": "<b>Explaining away is the one to hold onto</b> — it "
              "is the mechanism behind a great many apparent paradoxes "
              "in conditional reasoning, including selection bias.",
   "note": "The car example makes the collider immediately intuitive."},

  {"t": "section", "label": "Part 3", "title": "Inference",
   "blurb": "Computing a posterior."},

  {"t": "callout", "title": "Variable elimination, and what decides its cost",
   "kind": "Exact inference",
   "body": ["<b>To compute P(query | evidence), sum out the "
            "non-query, non-evidence variables one at a time</b>, "
            "multiplying the factors that mention each.",
            "<b>The cost is exponential in the largest intermediate "
            "factor</b>, and the elimination <i>order</i> determines how "
            "large that gets.",
            "<b>Finding the best order is NP-hard</b>, and good "
            "heuristics (min-fill, min-degree) are cheap and usually "
            "adequate.",
            "<b>The best achievable cost is exponential in the "
            "treewidth</b> — <b>exactly Module 06 §3's "
            "quantity, in a different subject</b>, which is why that "
            "result was worth stating twice."]},

  {"t": "table", "kicker": "Methods", "title": "When exact inference is infeasible",
   "header": ["Method", "How", "When"],
   "widths": [2.7, 4.1, 5.3],
   "rows": [
     ["<b>Variable elimination</b>", "<b>Sum out in a good order</b>", "<b>Exact. Low treewidth</b>"],
     ["<b>Likelihood weighting</b>", "<b>Sample, weight by evidence</b>", "<b>Simple; degrades with much evidence</b>"],
     ["<b>Gibbs / MCMC</b>", "<b>Resample one variable at a time</b>", "<b>General; convergence is hard to verify</b>"],
     ["<b>Loopy belief propagation</b>", "Message passing, ignore cycles", "<b>Fast, approximate, may not converge</b>"],
     ["<b>Variational</b>", "<b>Fit a simpler distribution</b>", "<b>Fast, biased, and the bias is bounded</b>"],
   ],
   "footnote": "<b>Report which method and whether it converged.</b> "
               "<b>MCMC that has not mixed produces confident nonsense</b> "
               "and reports nothing about it — CSCE 753 "
               "§12's theme again.",
   "note": "The convergence-reporting point is the practical "
           "discipline."},

  {"t": "section", "label": "Part 4", "title": "In an agent",
   "blurb": "Where probabilistic reasoning is used, and where it is not."},

  {"t": "bullets", "kicker": "Uses", "title": "Probabilistic reasoning in a game or a robot",
   "items": [
     "<b>Tracking what the agent believes about hidden state</b> "
     "— where the player probably is, given sounds and last "
     "sighting. <b>A belief distribution, updated.</b>",
     "",
     "<b>Sensor fusion</b> — combining noisy evidence, which is "
     "CSCE 753 §07's Kalman filter as a special case.",
     "",
     "<b>Diagnosis and inference about causes</b>, where explaining "
     "away is genuinely needed.",
     "",
     "<b>And decision-making under uncertainty</b>, which is "
     "Module 10 — beliefs are only useful if they change what you "
     "do.",
     "",
     "<b>Not for most game AI.</b> <b>A designer-authored "
     "approximation is usually cheaper, more controllable, and "
     "indistinguishable to the player.</b>",
   ],
   "footnote": "<b>The last point is honest rather than "
               "dismissive:</b> probabilistic reasoning earns its place "
               "where the uncertainty is real and consequential, and not "
               "elsewhere."},

  {"t": "callout", "title": "What this buys over logic",
   "kind": "Closing the comparison",
   "body": ["<b>Logic cannot say 'usually'</b> (Module 08 §4), "
            "and adding exceptions to a logical rule base is "
            "open-ended.",
            "<b>Probability says it natively</b>, degrades gracefully "
            "as evidence accumulates, and combines independent evidence "
            "correctly without new rules.",
            "<b>The cost is that you must supply numbers</b>, and "
            "<b>the numbers are frequently guesses dressed as "
            "measurements</b> — which is a real objection and should "
            "be answered with sensitivity analysis rather than "
            "confidence.",
            "<b>And exact inference is intractable in general</b>, so "
            "you are usually approximating, which Part 3's footnote says "
            "to report."]},
 ],
 "takeaways": [
   "Bayes' rule requires the prior, and dropping it is the base-rate "
   "fallacy — a 99% accurate test for a 1-in-10,000 condition is "
   "about 1% predictive.",
   "Conditional independence reduces the parameter count from exponential "
   "to linear, which is the entire reason probabilistic AI is possible.",
   "A Bayesian network's missing edges carry the information; a fully "
   "connected network says nothing.",
   "The collider is the counterintuitive case: observing a common effect "
   "makes its independent causes dependent, which is explaining away.",
   "Variable elimination's cost is exponential in the treewidth — "
   "Module 06's quantity in a different subject.",
   "Report which inference method you used and whether it converged, "
   "because unmixed MCMC produces confident nonsense silently.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Bayes and independence"),
  ("eq", "P(H | E) = P(E | H) &middot; P(H) / P(E)"),
  ("p", "<b>Posterior equals likelihood times prior, normalised.</b> "
        "<b>P(H) is the prior and it is not optional</b> — "
        "<b>dropping it is the base-rate fallacy, and it is the single "
        "most common error in applied probability</b>, including in "
        "published work. <b>A test that is 99% accurate in both "
        "directions, applied to a condition affecting 1 in 10,000 people, "
        "has a positive predictive value of about 1%</b>: of 10,000 "
        "people, one has the condition and is probably detected, while "
        "about 100 healthy people test positive. <b>The arithmetic is "
        "trivial and the intuition is terrible</b>, which is why it is "
        "worth computing by hand once rather than accepting on "
        "authority — and why CSCE 633 Module 12 &sect;2's "
        "insistence on reporting precision rather than accuracy matters so "
        "much on imbalanced problems. <b>It is the same arithmetic.</b>"),
  ("callout", "Conditional independence is what makes any of this tractable",
   ["<b>A full joint distribution over n binary variables requires "
    "2<super>n</super> &minus; 1 numbers.</b> At n = 30 that is over a "
    "billion parameters — <b>nobody can specify them, store them, or "
    "estimate them from data.</b>",
    "<b>But most variables are conditionally independent given a few "
    "others.</b> Once you know whether it rained, whether the sprinkler "
    "ran tells you nothing further about whether the grass is wet having "
    "already accounted for both — and <b>that kind of structure is "
    "ubiquitous in real domains.</b>",
    "<b>So the joint factorises into a product of small conditional "
    "distributions</b>, one per variable given its few parents, <b>and "
    "the parameter count drops from exponential in n to linear in n</b> "
    "(with the constant set by the largest parent set).",
    "<b>That is the entire reason probabilistic AI is possible.</b> "
    "<b>And it is the same structural argument as Module 06 &sect;3's "
    "treewidth and CSCE 669 Module 11's sparsity</b>: <b>structure, "
    "not size, decides tractability</b> — which at the third "
    "appearance should be read as one of this program's load-bearing "
    "ideas rather than three separate facts."]),

  ("h1", "2 &nbsp; Bayesian networks"),
  ("code", """A DIRECTED ACYCLIC GRAPH. Each node is a variable; each
node carries the conditional distribution P(node | parents).

THE JOINT FACTORISES:
    P(x1..xn) = product over i of P(xi | parents(xi))

SO THE GRAPH IS A CLAIM ABOUT INDEPENDENCE, and THE MISSING
EDGES CARRY THE INFORMATION. A fully connected network
asserts nothing and costs as much as the full joint.

READING INDEPENDENCE OFF THE GRAPH (d-separation):

  CHAIN     A -> B -> C
            A and C are independent GIVEN B. Knowing the
            intermediate blocks the path.

  FORK      A <- B -> C
            A and C are independent GIVEN B. A common cause
            explains the correlation.

  COLLIDER  A -> B <- C
            A and C are independent -- UNTIL you observe B,
            and THEN THEY BECOME DEPENDENT.

THE COLLIDER IS THE COUNTERINTUITIVE CASE AND IT MATTERS:
two unrelated causes of one observed effect become
correlated once the effect is known. Your car will not
start; the cause is the battery or the fuel pump; learning
that the battery is fine makes the fuel pump more likely.

THIS IS EXPLAINING AWAY. It is why observing MORE can
CREATE dependence rather than remove it, and it is the
mechanism behind selection bias and Berkson's paradox."""),
  ("p", "<b>Explaining away is the one to hold onto.</b> <b>It is the "
        "mechanism behind a great many apparent paradoxes in conditional "
        "reasoning</b> — including selection bias, where "
        "conditioning on being in a sample (a collider) induces "
        "correlations between characteristics that are independent in the "
        "population. <b>And it is a reason to draw the graph before "
        "reasoning:</b> whether conditioning on a variable helps or hurts "
        "depends on its position, and that is not something intuition "
        "reliably gets right."),

  ("break",),
  ("h1", "3 &nbsp; Inference"),
  ("callout", "Variable elimination, and what decides its cost",
   ["<b>To compute P(query | evidence), sum out each variable that is "
    "neither the query nor evidence, one at a time</b> — "
    "multiplying together all the factors mentioning that variable, then "
    "summing it away to produce a new factor.",
    "<b>The cost is exponential in the size of the largest intermediate "
    "factor produced</b>, and <b>the elimination order determines how "
    "large that gets</b> — a good order keeps factors small, a bad "
    "one produces a factor over most of the network.",
    "<b>Finding the optimal order is NP-hard</b>, and <b>cheap "
    "heuristics (min-fill, min-degree) are usually adequate</b> — "
    "the same situation as Module 03's heuristics, applied to the "
    "ordering rather than to the search.",
    "<b>And the best achievable cost is exponential in the network's "
    "treewidth</b> — <b>exactly Module 06 &sect;3's quantity, in "
    "a different subject</b>. <b>Which is why that result was worth "
    "stating twice:</b> constraint satisfaction and probabilistic "
    "inference are both instances of a general computation over a "
    "factorised structure, and <b>the same graph property governs "
    "both.</b>"]),
  ("table", ["Method", "How it works", "When to use it"],
   [["<b>Variable elimination</b>",
     "<b>Sum out variables in a heuristically chosen order.</b>",
     "<b>Exact. Viable when the treewidth is low</b>, which many real "
     "networks are."],
    ["<b>Likelihood weighting</b>",
     "<b>Sample from the network with evidence fixed, weighting each "
     "sample by the evidence's likelihood.</b>",
     "<b>Simple to implement; degrades badly when there is a lot of "
     "evidence</b>, because almost all weight concentrates on a few "
     "samples."],
    ["<b>Gibbs sampling / MCMC</b>",
     "<b>Repeatedly resample one variable from its conditional given "
     "all the others.</b>",
     "<b>General and widely applicable; convergence is hard to verify</b> "
     "— see the note below."],
    ["<b>Loopy belief propagation</b>",
     "Pass messages as if the graph were a tree, ignoring cycles.",
     "<b>Fast and approximate, and it may fail to converge or converge to "
     "a wrong answer</b> — and it works surprisingly well on many "
     "real networks anyway."],
    ["<b>Variational inference</b>",
     "<b>Fit a tractable distribution to approximate the intractable "
     "posterior, by optimisation.</b>",
     "<b>Fast, biased, and the bias is characterisable</b> — and it "
     "is CSCE 669's optimisation applied to inference."]],
   [0.21, 0.37, 0.42]),
  ("p", "<b>Report which method you used and whether it converged.</b> "
        "<b>MCMC that has not mixed produces confident nonsense and "
        "reports nothing about it</b> — the chain returns samples, "
        "the samples have a mean, and the mean is wrong. <b>Run multiple "
        "chains from different starting points and compare them; report "
        "the diagnostic.</b> <b>Which is CSCE 753 Module 12's theme "
        "arriving in a different subject: a confident output is not a "
        "correct one, and the only defence is a check that the method "
        "itself does not perform.</b>"),

  ("h1", "4 &nbsp; Probabilistic reasoning in an agent"),
  ("ul", ["<b>Tracking what the agent believes about hidden state</b> "
          "— where the player probably is, given a sound heard "
          "fifteen seconds ago, a last confirmed sighting, and the "
          "connectivity of the level. <b>A belief distribution over "
          "locations, updated on each observation</b>, which is both "
          "principled and produces good search behaviour.",
          "<b>Sensor fusion</b> — combining multiple noisy sources "
          "of evidence about one quantity, which is <b>CSCE 753 "
          "Module 07's Kalman filter as a special case</b> (a Bayes net "
          "with Gaussian conditionals and linear dynamics).",
          "<b>Diagnosis and reasoning about causes</b>, where "
          "&sect;2's explaining away is genuinely needed — fault "
          "diagnosis, medical decision support, and root-cause analysis "
          "all have collider structure.",
          "<b>And decision-making under uncertainty</b>, which is "
          "Module 10 — <b>beliefs are only useful if they change "
          "what the agent does</b>, and a belief distribution with no "
          "decision attached is an expensive way to produce no "
          "behaviour.",
          "<b>Not for most game AI, honestly.</b> <b>A "
          "designer-authored approximation — a visibility cone, a "
          "decaying 'last known position' marker, a simple alertness "
          "counter — is usually cheaper, far more controllable, and "
          "indistinguishable to the player</b>. <b>Probabilistic "
          "reasoning earns its place where the uncertainty is real and "
          "consequential</b> (robotics, diagnosis, a stealth game whose "
          "whole design rests on modelling what enemies believe) <b>and "
          "not elsewhere</b> — which is Module 01 &sect;1's "
          "cheapest-sufficient-design argument applied to this module's "
          "own content."]),
  ("callout", "What this buys over logic",
   ["<b>Logic cannot say 'usually'</b> (Module 08 &sect;4), and "
    "patching a logical rule base with exceptions is open-ended — "
    "each exception needs a rule, and the exceptions have exceptions.",
    "<b>Probability says it natively</b>, <b>degrades gracefully as "
    "evidence accumulates rather than flipping between certainties, and "
    "combines independent evidence correctly without any new rules</b> "
    "— which is the structural advantage, not merely a notational "
    "one.",
    "<b>The cost is that you must supply numbers</b>, and <b>the numbers "
    "are frequently guesses dressed as measurements</b>. <b>This is a "
    "real objection</b> and the right answer is not confidence but "
    "<b>sensitivity analysis</b>: vary the numbers you are least sure of "
    "and report whether the conclusion changes (CSCE 669 Module 12 "
    "&sect;3's dual-variable check, in a probabilistic setting).",
    "<b>And exact inference is intractable in general</b> (&sect;3), so "
    "in practice you are approximating — which &sect;3's footnote "
    "says to report rather than to assume away. <b>The honest position is "
    "that probability is the right language for uncertainty and that using "
    "it well requires stating both the numbers you assumed and the "
    "approximation you computed with.</b>"]),
 ],
 "resources": [
   ("Russell & Norvig &mdash; AIMA, chapters 12–14 (pseudocode "
    "free)",
    "https://aima.cs.berkeley.edu/",
    "<b>Bayes nets, d-separation, and variable elimination</b> — the "
    "reference for the whole module."),
   ("Koller & Friedman &mdash; Probabilistic Graphical Models",
    "https://mitpress.mit.edu/9780262013192/probabilistic-graphical-models/",
    "<b>The comprehensive treatment</b>, strong on the treewidth "
    "connection of &sect;3. Library copy; the author's free Coursera "
    "lectures cover much of it."),
   ("Pearl &mdash; Causality, chapter 1; and The Book of Why",
    "http://bayes.cs.ucla.edu/BOOK-2K/",
    "<b>Where &sect;2's d-separation and explaining away come from</b>, "
    "and the causal reading of the graph that the standard treatment "
    "understates."),
   ("pgmpy documentation (free)",
    "https://pgmpy.org/",
    "<b>A working library for &sect;2 and &sect;3</b>, with every "
    "inference method in the table — after implementing variable "
    "elimination yourself once."),
 ],
 "exercises": [
   "<b>Compute the 1-in-10,000 test example by hand</b> and confirm the "
   "1% figure.",
   "<b>Plot positive predictive value against prevalence</b> for a fixed "
   "test accuracy.",
   "<b>Count the parameters</b> of a full joint over 20 binary variables "
   "and of a Bayes net with at most 3 parents each.",
   "<b>Build a Bayes net</b> for a domain you know, with at least eight "
   "variables.",
   "<b>Identify a chain, a fork, and a collider</b> in it and state the "
   "independence each implies.",
   "<b>Demonstrate explaining away numerically</b> on your collider.",
   "<b>Implement variable elimination</b> and verify against enumeration "
   "on a small network.",
   "<b>Compare two elimination orders</b> and report the largest "
   "intermediate factor for each.",
   "<b>Implement Gibbs sampling</b> and run four chains. Report whether "
   "they agree.",
   "<b>Deliberately run MCMC too briefly</b> and report the wrong answer "
   "it gives confidently.",
 ],
 "selfcheck": [
   "State Bayes' rule and explain the base-rate fallacy with numbers.",
   "Why does conditional independence make probabilistic AI possible?",
   "What does a Bayes net's structure assert, and what do missing edges "
   "mean?",
   "Describe chain, fork, and collider, and which is counterintuitive.",
   "Explain explaining away and name a paradox it accounts for.",
   "How does variable elimination work and what decides its cost?",
   "What quantity governs it, and where else in this program does it "
   "appear?",
   "Name five inference methods and when each applies.",
   "Why must you report convergence?",
   "What does probability buy over logic, and what does it cost?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Decisions Under Uncertainty",
 "subtitle": "Markov decision processes, solved by computation.",
 "question": "How do you act well when actions have uncertain outcomes?",
 "outcomes": [
     "Define a Markov decision process and a policy.",
     "Explain the Bellman equation and what discounting means.",
     "Implement value iteration and policy iteration.",
     "Explain what a POMDP adds and why it is so much harder.",
     "State the connection to CSCE 642 precisely.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The model",
   "blurb": "States, actions, transitions, rewards."},

  {"t": "callout", "title": "An MDP is a search problem where actions are unreliable",
   "kind": "The formulation",
   "body": ["<b>States, actions, a transition probability "
            "P(s′|s,a), and a reward R(s,a,s′).</b> "
            "That is the whole model.",
            "<b>The Markov property is the assumption that earns its "
            "name:</b> <b>the next state depends only on the current "
            "state and action, not on the history</b> — which is a "
            "constraint on your state definition, not a fact about the "
            "world.",
            "<b>So the solution is not a <i>plan</i> but a "
            "<i>policy</i></b> π(s) → a. <b>You cannot "
            "commit to a sequence, because you do not know where you "
            "will be.</b>",
            "<b>Which is exactly Module 01 §2's "
            "stochastic row, and Module 07 §4's first "
            "broken assumption</b> — this module is what replaces "
            "classical planning when actions can fail."]},

  {"t": "eq", "kicker": "Bellman", "title": "The value of a state, defined recursively",
   "eqs": [
     ("V*(s) = maxₐ Σ_s′ P(s′|s,a) [ R + γ·V*(s′) ]",
      "The value of a state is the best expected immediate reward plus "
      "discounted future value."),
     ("γ ∈ [0,1) is the discount factor",
      "It makes infinite-horizon sums finite, and it encodes how much "
      "the future matters."),
     ("1/(1−γ) is the effective horizon",
      "γ = 0.9 looks about 10 steps ahead; γ = 0.99 "
      "about 100. Set it from the problem, not by habit."),
   ],
   "caption": "<b>The effective-horizon reading is the useful one</b> "
              "— it turns an abstract parameter into a statement "
              "about how far the agent plans.",
   "note": "Students tune gamma blindly; the horizon framing fixes "
           "that."},

  {"t": "section", "label": "Part 2", "title": "Solving it",
   "blurb": "Two algorithms, both exact."},

  {"t": "code", "kicker": "Algorithms", "title": "Solving it 1/2: the two algorithms",
   "lang": "text", "code": """
  VALUE ITERATION
      initialise V arbitrarily
      repeat: V(s) <- max_a sum_s' P(s'|s,a)[R + g V(s')]
      until the largest change is below a threshold
      then the policy is the argmax at each state

  POLICY ITERATION
      repeat:
          EVALUATE the current policy (solve a linear
              system, or sweep V until it settles)
          IMPROVE: pi(s) <- argmax over a, given V
      until the policy stops changing

  WHICH ONE: policy iteration when evaluation is cheap
  (a small state space, or a solvable linear system);
  value iteration when it is not, or when you want
  anytime behaviour under a deadline.
""",
   "caption": "<b>Both are exact</b>, and both reduce to sweeping the "
              "Bellman equation until it stops changing.",
   "note": "Keep the two algorithms side by side before analysing "
           "either."},

  {"t": "code", "kicker": "Why it works", "title": "Solving it 2/2: convergence, and the real limit",
   "lang": "text", "code": """
  VALUE ITERATION CONVERGES because the Bellman update is a
  CONTRACTION with factor g: each full sweep shrinks the
  maximum error by g, so the error falls geometrically.
      -- This is CSCE 669 Module 05's LINEAR CONVERGENCE,
         with g in the role of the rate. The iteration
         count is logarithmic in the accuracy wanted.

  POLICY ITERATION CONVERGES IN FAR FEWER ITERATIONS --
  frequently under a dozen -- because each improvement step
  is a large jump rather than an incremental update. Each
  iteration costs more.

  AND BOTH ARE POLYNOMIAL IN THE NUMBER OF STATES --
  while the number of states is usually EXPONENTIAL in the
  problem's description. THAT is the real limit, and it
  has a name: the curse of dimensionality.
""",
   "caption": "<b>Polynomial in states and exponentially many states is "
              "the central difficulty</b> — and it is why "
              "CSCE 642 approximates the value function instead of "
              "tabulating it.",
   "note": "Naming the curse of dimensionality precisely sets up 642."},

  {"t": "section", "label": "Part 3", "title": "Partial observability",
   "blurb": "When the agent does not know its state."},

  {"t": "callout", "title": "A POMDP's state is a belief, and that changes everything",
   "kind": "Why this is so much harder",
   "body": ["<b>If the agent cannot observe its state, it must act on a "
            "<i>belief</i> — a probability distribution over "
            "states</b> (Module 09).",
            "<b>A POMDP is an MDP over belief space</b>, which is "
            "<i>continuous</i> even when the state space is finite "
            "— so the tabular methods of Part 2 do not apply.",
            "<b>And solving one exactly is PSPACE-hard.</b> Practical "
            "methods are point-based approximations (PBVI, SARSOP) or "
            "online tree search over beliefs (POMCP).",
            "<b>But the formulation is valuable even when you do not "
            "solve it:</b> <b>it makes 'the agent should gather "
            "information' a consequence rather than a special "
            "case</b> — looking around has value because it sharpens "
            "the belief."]},

  {"t": "section", "label": "Part 4", "title": "The bridge",
   "blurb": "Where this course ends and CSCE 642 begins."},

  {"t": "table", "kicker": "Bridge", "title": "This module against CSCE 642",
   "header": ["", "Here (planning)", "CSCE 642 (learning)"],
   "widths": [2.4, 4.3, 5.3],
   "rows": [
     ["<b>You know</b>", "<b>P and R — the model</b>", "<b>Nothing; you interact and observe</b>"],
     ["<b>Method</b>", "<b>Sweep every state (Part 2)</b>", "<b>Sample trajectories</b>"],
     ["<b>V stored as</b>", "<b>A table over states</b>", "<b>A function approximator — a network</b>"],
     ["<b>Limit</b>", "<b>State count</b>", "<b>Sample count and stability</b>"],
     ["<b>Equation</b>", "<b>Bellman</b>", "<b>Bellman — the same one</b>"],
   ],
   "footnote": "<b>The Bellman equation is identical in both.</b> "
               "<b>Reinforcement learning is this module's problem with "
               "the model unknown and the table replaced by a "
               "network</b>, which is the single most useful thing to "
               "carry forward.",
   "note": "Making this table explicit is the best preparation for 642."},

  {"t": "callout", "title": "Where MDPs are worth it in a game",
   "kind": "Honest scope",
   "body": ["<b>Small, discrete, high-stakes decisions.</b> Which of "
            "six abilities to use, given a known distribution over "
            "outcomes — a tabular MDP is tractable and optimal.",
            "<b>Precomputed policies.</b> <b>Solve offline, ship the "
            "table</b> — the runtime cost is a lookup, which suits a "
            "frame budget perfectly.",
            "<b>Not for continuous control or large state spaces</b>, "
            "where the state count defeats you and CSCE 642's "
            "approximation is needed.",
            "<b>And not where a designer wants direct control</b>, "
            "because <b>an optimal policy is not a tunable one</b> "
            "— Module 05 §4's point, and Module 11's reason "
            "for existing."]},
 ],
 "takeaways": [
   "An MDP is a search problem with unreliable actions, and its solution "
   "is a policy rather than a plan because you cannot know where you will "
   "be.",
   "The Markov property is a constraint on your state definition, not a "
   "fact about the world.",
   "The discount factor's effective horizon is 1/(1−γ), which "
   "turns an abstract parameter into a statement about planning depth.",
   "Value iteration converges because the Bellman update is a contraction "
   "with factor γ — CSCE 669's linear convergence.",
   "Both algorithms are polynomial in the state count and the state count "
   "is usually exponential in the problem description, which is the real "
   "limit.",
   "A POMDP is an MDP over continuous belief space, and its value is "
   "partly that information-gathering becomes a consequence rather than a "
   "special case.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The model"),
  ("callout", "An MDP is a search problem where actions are unreliable",
   ["<b>A set of states, a set of actions, a transition probability "
    "P(s&prime; | s, a), and a reward R(s, a, s&prime;).</b> That is the "
    "entire model, and it is Module 02's search problem with the "
    "deterministic transition function replaced by a distribution.",
    "<b>The Markov property is the assumption that earns the name:</b> "
    "<b>the next state depends only on the current state and action, not "
    "on how you arrived</b>. <b>Which is a constraint on your state "
    "definition rather than a fact about the world</b> — if history "
    "matters, put the relevant history in the state (Module 02 "
    "&sect;1's choice, with a specific criterion for once).",
    "<b>So the solution is not a <i>plan</i> but a <i>policy</i></b>, a "
    "mapping &pi;(s) from states to actions. <b>You cannot commit to a "
    "sequence of actions, because you do not know which state you will be "
    "in after the first one.</b>",
    "<b>Which is exactly Module 01 &sect;2's stochastic row, and "
    "Module 07 &sect;4's first broken assumption</b> — <b>this "
    "module is what replaces classical planning when actions can "
    "fail</b>, and it is worth seeing it as that rather than as an "
    "unrelated formalism."]),
  ("eq", "V*(s) = max<sub>a</sub> &Sigma;<sub>s&prime;</sub> "
         "P(s&prime;|s,a) [ R(s,a,s&prime;) + &gamma; V*(s&prime;) ]"),
  ("p", "<b>The value of a state is the best available expected immediate "
        "reward plus the discounted value of where you end up.</b> "
        "<b>&gamma; in [0,1) is the discount factor</b>, and it serves "
        "two purposes: mathematically it makes infinite-horizon sums "
        "finite, and substantively it encodes how much the future "
        "matters. <b>The useful reading is that 1/(1&minus;&gamma;) is "
        "the effective horizon</b>: &gamma; = 0.9 looks about ten steps "
        "ahead, &gamma; = 0.99 about a hundred. <b>So set it from the "
        "problem's actual timescale rather than by habit</b> — an "
        "agent whose decisions matter over five steps does not need "
        "&gamma; = 0.999, and giving it one makes the value function "
        "harder to compute for no benefit."),

  ("h1", "2 &nbsp; Solving an MDP"),
  ("code", """VALUE ITERATION
    initialise V arbitrarily
    repeat:
        V(s) <- max_a sum_s' P(s'|s,a)[R + g*V(s')]
    until the largest change over all states is below a
        threshold
    then the policy is the argmax action at each state

    CONVERGES because the Bellman update is a CONTRACTION
    with factor g: each full sweep shrinks the maximum
    error by a factor of g, so the error falls
    geometrically. This is CSCE 669 Module 05's LINEAR
    CONVERGENCE, with g in the role of the rate -- and it
    means the iteration count is logarithmic in the
    accuracy you want.

POLICY ITERATION
    repeat:
        EVALUATE the current policy: solve the linear
            system V = R_pi + g*P_pi*V, or sweep V until
            it settles
        IMPROVE: pi(s) <- argmax over a, using that V
    until the policy stops changing

    CONVERGES IN FAR FEWER ITERATIONS -- frequently under a
    dozen, even on large problems -- because each
    improvement step is a large jump rather than an
    incremental update. Each iteration costs more.

WHICH ONE: policy iteration when evaluation is cheap (a
small state space, or a solvable linear system); value
iteration when it is not, or when you want anytime
behaviour and a usable partial answer.

BOTH ARE POLYNOMIAL IN THE NUMBER OF STATES -- and the
number of states is usually EXPONENTIAL in the problem's
description. That is the real limit, and it has a name:
the curse of dimensionality."""),
  ("p", "<b>Polynomial in states, with exponentially many states, is the "
        "central difficulty of this module</b> — a game with ten "
        "binary flags and a position on a 100&times;100 grid has ten "
        "million states before anything interesting is modelled. <b>And "
        "it is precisely why CSCE 642 approximates the value function "
        "with a network instead of tabulating it</b>: the table is the "
        "problem, not the algorithm."),

  ("break",),
  ("h1", "3 &nbsp; Partial observability"),
  ("callout", "A POMDP's state is a belief, and that changes everything",
   ["<b>If the agent cannot observe its state directly, it must act on a "
    "<i>belief</i> — a probability distribution over states</b>, "
    "updated by Bayes' rule on each observation (Module 09 &sect;1).",
    "<b>A POMDP is therefore an MDP over belief space</b>, and <b>belief "
    "space is continuous even when the underlying state space is "
    "finite</b> — a distribution over n states is a point in an "
    "(n&minus;1)-dimensional simplex. <b>So &sect;2's tabular methods do "
    "not apply at all.</b>",
    "<b>And solving one exactly is PSPACE-hard</b>, which is worse than "
    "NP-hard. <b>Practical methods are point-based value iteration "
    "(PBVI, SARSOP), which approximate the value function at a "
    "representative set of beliefs, or online tree search over beliefs "
    "(POMCP), which is Module 05's MCTS applied to belief states.</b>",
    "<b>But the formulation is valuable even when you do not solve "
    "it.</b> <b>It makes 'the agent should gather information' a "
    "consequence of the model rather than a special case</b> — "
    "looking around, or opening a door to check, has <i>value</i> because "
    "it sharpens the belief and therefore improves every subsequent "
    "decision. <b>No special rule is needed to make a POMDP agent "
    "curious</b>, and that is a genuinely satisfying property: "
    "exploration falls out of correctly accounting for uncertainty, which "
    "is the same observation CSCE 642 &sect;2 makes about intrinsic "
    "motivation."]),

  ("h1", "4 &nbsp; The bridge to CSCE 642"),
  ("table", ["", "This module (planning)", "CSCE 642 (learning)"],
   [["<b>What you know</b>",
     "<b>P and R — you have the model.</b>",
     "<b>Nothing. You interact with the environment and observe "
     "outcomes.</b>"],
    ["<b>Method</b>",
     "<b>Sweep every state systematically</b> (&sect;2).",
     "<b>Sample trajectories and update from what you saw.</b>"],
    ["<b>V stored as</b>", "<b>A table indexed by state.</b>",
     "<b>A function approximator — typically a neural network</b> "
     "(CSCE 636)."],
    ["<b>The binding limit</b>", "<b>The number of states.</b>",
     "<b>The number of samples, and the stability of the "
     "approximation.</b>"],
    ["<b>The equation</b>", "<b>Bellman.</b>",
     "<b>Bellman — the same one, unchanged.</b>"]],
   [0.18, 0.37, 0.45]),
  ("p", "<b>The Bellman equation is identical in both courses.</b> "
        "<b>Reinforcement learning is this module's problem with the "
        "model unknown and the table replaced by a function "
        "approximator</b> — which is the single most useful thing to "
        "carry into CSCE 642, because it means every difficulty there "
        "is traceable to one of those two substitutions. <b>Instability "
        "comes from the approximator; sample inefficiency comes from not "
        "having the model.</b>"),
  ("callout", "Where MDPs are worth it in a game",
   ["<b>Small, discrete, high-stakes decisions.</b> Which of six "
    "abilities to use, given a known distribution over outcomes; whether "
    "to retreat or press an attack. <b>A tabular MDP is tractable and "
    "optimal here</b>, and it handles the probabilistic reasoning "
    "correctly where a hand-written rule would approximate it badly.",
    "<b>Precomputed policies.</b> <b>Solve the MDP offline and ship the "
    "policy table</b> — the runtime cost is a single array lookup, "
    "which suits a frame budget perfectly (Module 01 &sect;4's "
    "arithmetic). <b>This is the pattern that makes MDPs practical in "
    "games</b>, and it is Module 03 &sect;2's amortisation argument "
    "again.",
    "<b>Not for continuous control or large state spaces</b>, where "
    "&sect;2's state count defeats you and CSCE 642's function "
    "approximation is the only route.",
    "<b>And not where a designer wants direct control over "
    "behaviour</b>, because <b>an optimal policy is not a tunable "
    "one</b> — you can adjust the rewards and hope, which is "
    "indirect and frustrating. <b>That is Module 05 &sect;4's point "
    "about optimal opponents, and it is Module 11's entire reason for "
    "existing</b>: most game AI is built from architectures that trade "
    "optimality for authorial control, deliberately."]),
 ],
 "resources": [
   ("Sutton & Barto &mdash; Reinforcement Learning, chapters 3–4 "
    "(free PDF)",
    "http://incompleteideas.net/book/the-book.html",
    "<b>MDPs, the Bellman equation, and dynamic programming</b> — "
    "the reference for this module, and the rest of the book is "
    "CSCE 642."),
   ("Berkeley CS188 &mdash; MDP and reinforcement learning lectures "
    "(free)",
    "https://inst.eecs.berkeley.edu/~cs188/",
    "<b>&sect;1 and &sect;2 with excellent worked examples</b>, and a "
    "project implementing both algorithms."),
   ("Kaelbling, Littman & Cassandra &mdash; Planning and Acting in "
    "Partially Observable Stochastic Domains (free)",
    "https://www.sciencedirect.com/science/article/pii/S000437029800023X",
    "<b>The &sect;3 reference</b>, and the clearest statement of why "
    "belief space is the right formulation."),
   ("Kurniawati, Hsu & Lee &mdash; SARSOP (free)",
    "https://www.comp.nus.edu.sg/~leews/publications/rss08.pdf",
    "<b>A practical POMDP solver</b>, which makes &sect;3's "
    "approximations concrete."),
 ],
 "exercises": [
   "<b>Formulate a small problem as an MDP</b> and write out P and R "
   "explicitly.",
   "<b>Check the Markov property</b> and, if it fails, extend the state "
   "until it holds.",
   "<b>Implement value iteration</b> and plot the maximum error against "
   "sweep number on a log axis. Confirm the geometric rate.",
   "<b>Verify the rate equals γ</b> empirically.",
   "<b>Implement policy iteration</b> and report the iteration count "
   "against value iteration's.",
   "<b>Vary γ from 0.5 to 0.999</b> and report how the optimal "
   "policy changes.",
   "<b>Relate each γ to its effective horizon</b> and check whether "
   "the policy's lookahead matches.",
   "<b>Count the states</b> of an MDP for a game situation you care "
   "about. Report whether tabular methods are viable.",
   "<b>Implement a belief update</b> for a small partially observable "
   "problem.",
   "<b>Show that an information-gathering action has positive value</b> "
   "in your belief MDP, without special-casing it.",
 ],
 "selfcheck": [
   "Define an MDP and explain why the solution is a policy.",
   "What does the Markov property constrain?",
   "State the Bellman equation and interpret γ as a horizon.",
   "Why does value iteration converge, and at what rate?",
   "Compare value and policy iteration, and say when to use each.",
   "What is the real limit on tabular methods?",
   "What is a POMDP, why is it so much harder, and what does the "
   "formulation buy?",
   "Give the five-row comparison against CSCE 642.",
   "Where are MDPs worth it in a game, and where are they not?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Game AI Architecture",
 "subtitle": "What actually runs, sixty times a second.",
 "question": "How do you organise an agent's behaviour so a designer can "
             "work with it?",
 "outcomes": [
     "Compare finite state machines, behaviour trees, and utility "
     "systems.",
     "Implement a behaviour tree and explain its composability.",
     "Implement steering behaviours and local avoidance.",
     "Design for a frame budget across many agents.",
     "Choose an architecture and justify it against the "
     "alternatives.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The constraint",
   "blurb": "Sixteen milliseconds, shared with everything else."},

  {"t": "callout", "title": "The frame budget is the design constraint, with arithmetic",
   "kind": "Why game AI looks the way it does",
   "body": ["<b>Sixty frames per second is 16.7 ms for rendering, "
            "physics, animation, audio, networking, and every agent's "
            "decision.</b>",
            "<b>AI typically gets 1–2 ms.</b> With 50 agents "
            "that is 20–40 <i>microseconds</i> per agent per "
            "frame.",
            "<b>So most agents must do nothing most frames.</b> The "
            "standard answers are staggered updates (each agent decides "
            "every n-th frame), level-of-detail AI (distant agents think "
            "less), and event-driven rather than polled logic.",
            "<b>And the architecture must be interruptible and "
            "incremental</b> — <b>which rules out anything that "
            "must run to completion</b>, and is why anytime algorithms "
            "(M03 §4, M05 §3) keep appearing."]},

  {"t": "table", "kicker": "Architectures", "title": "The three that are used",
   "header": ["", "FSM", "Behaviour tree", "Utility"],
   "widths": [2.2, 3.1, 3.1, 2.9],
   "rows": [
     ["<b>Decides by</b>", "<b>Current state + transitions</b>", "<b>Walking a tree each tick</b>", "<b>Scoring every option</b>"],
     ["<b>Authoring</b>", "<b>O(n²) transitions</b>", "<b>Composable subtrees</b>", "<b>Tune curves</b>"],
     ["<b>Scales to</b>", "<b>~10 states</b>", "<b>Hundreds of nodes</b>", "<b>Many options</b>"],
     ["<b>Debugging</b>", "<b>Easy</b>", "<b>Easy — inspect the active path</b>", "<b>Hard — why did that score?</b>"],
     ["<b>Best for</b>", "<b>Simple, few modes</b>", "<b>The default. Most games</b>", "<b>Many competing concerns</b>"],
   ],
   "footnote": "<b>Behaviour trees won because of the authoring "
               "column:</b> the transition explosion is what killed "
               "state machines, and composability is what fixed it.",
   "note": "The O(n^2) transition problem is the concrete reason for the "
           "shift."},

  {"t": "section", "label": "Part 2", "title": "Behaviour trees",
   "blurb": "Four node types, and that is the whole language."},

  {"t": "code", "kicker": "Behaviour trees", "title": "The entire formalism",
   "lang": "text", "code": """
  Every node, when ticked, returns SUCCESS, FAILURE, or
  RUNNING. That is the whole interface.

  SEQUENCE   tick children in order; fail if any fails;
             succeed when all succeed.      ("AND", "then")
  SELECTOR   tick children in order; succeed if any
             succeeds; fail if all fail.    ("OR", "try")
  DECORATOR  wrap one child and modify it: invert, repeat,
             add a cooldown, add a precondition guard.
  LEAF       an action, or a condition check.

  THAT IS IT. Four node types.

  WHY IT COMPOSES: a subtree's interface is identical to a
  leaf's, so ANY subtree can be substituted anywhere a node
  is expected. Build "FightEnemy" once; reuse it in twelve
  places; improve it once.
      -- which is why authoring cost is LINEAR in
         behaviours rather than quadratic in states.

  RUNNING is the part people get wrong. It means "I am not
  finished; tick me again next frame". It is what makes the
  tree work in a game loop at all, and it means the tree
  carries state between ticks (which node is running), so
  it is NOT a pure function of the world.

  PRIORITY IS STRUCTURAL: a selector's left-to-right order
  IS the priority order. Put "flee if nearly dead" leftmost.
""",
   "caption": "<b>The substitutability of subtrees is the whole "
              "advantage</b> — it is the same compositional property "
              "that makes a good API good.",
   "note": "Emphasise RUNNING; it is the most common implementation "
           "error."},

  {"t": "callout", "title": "Utility systems, and when they beat trees",
   "kind": "The third option",
   "body": ["<b>Score every available action with a utility function "
            "over the world state, then take the best.</b> No structure "
            "at all.",
            "<b>The strength is many competing considerations:</b> "
            "health, ammunition, distance, cover, allies nearby — "
            "each contributes to each action's score via a curve.",
            "<b>And it degrades gracefully.</b> <b>There is always a "
            "best-scoring action</b>, so there is no 'no valid behaviour' "
            "state — which behaviour trees reach and must handle.",
            "<b>The weakness is debuggability.</b> <b>'Why did it do "
            "that?' means comparing twenty scores</b>, and tuning one "
            "curve shifts every decision it participates in. <b>Log the "
            "scores, always.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Movement",
   "blurb": "Steering, and the layer below the path."},

  {"t": "bullets", "kicker": "Steering", "title": "Steering behaviours, composed",
   "items": [
     "<b>Seek, flee, arrive</b> — a desired velocity toward or "
     "away from a point, with arrival slowing as distance falls.",
     "",
     "<b>Path following</b> — seek the next point on the path, "
     "looking ahead so the agent cuts corners naturally.",
     "",
     "<b>Separation, alignment, cohesion</b> — <b>the three "
     "rules that produce flocking</b>, and the classic demonstration "
     "that simple reflex agents produce complex behaviour.",
     "",
     "<b>Obstacle avoidance and RVO</b> — <b>reciprocal velocity "
     "obstacles have each agent assume others also avoid</b>, which "
     "prevents the oscillation naive avoidance produces.",
     "",
     "<b>Composed by weighted sum, or by priority.</b> <b>Weighted "
     "sums cancel</b> — two opposed avoidances sum to zero and the "
     "agent walks into the wall.",
   ],
   "footnote": "<b>The cancellation failure is the classic steering "
               "bug.</b> <b>Prioritised or truncated composition avoids "
               "it</b>, at the cost of less smooth motion."},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "And making the agent legible."},

  {"t": "callout", "title": "Layer by timescale",
   "kind": "The architecture that works",
   "body": ["<b>Strategic (seconds): which goal.</b> A behaviour tree, "
            "utility score, or planner. Runs rarely.",
            "<b>Tactical (hundreds of ms): which path, which cover "
            "point.</b> Pathfinding and queries. Runs on demand.",
            "<b>Steering (every frame): where to move now.</b> Reflex "
            "behaviours only — Module 01 §1's cheapest agent, "
            "doing the most frequent work.",
            "<b>Each layer runs at its own rate and the division is by "
            "how fast the information changes</b> — <b>which is the "
            "same decomposition as Module 04 §4's three layers, "
            "and getting it wrong is the commonest architectural "
            "mistake.</b>"]},

  {"t": "bullets", "kicker": "Legibility", "title": "Making behaviour readable, which is a requirement",
   "items": [
     "<b>Telegraph intent.</b> An animation or sound before the "
     "action, so the player can respond. <b>A perfectly-timed instant "
     "attack reads as unfair, not as skilled.</b>",
     "",
     "<b>Commit visibly.</b> <b>An agent that changes its mind every "
     "frame appears broken</b>, even when each decision is "
     "individually correct. Add hysteresis.",
     "",
     "<b>Fail legibly.</b> If the agent cannot reach you, it should "
     "visibly try and fail — not stand still.",
     "",
     "<b>And log the decision.</b> <b>Ship a debug overlay showing "
     "the active behaviour and why</b> — it pays for itself in a "
     "week.",
   ],
   "footnote": "<b>Legibility is a functional requirement, not "
               "polish:</b> <b>a player who cannot predict an agent "
               "cannot play against it</b>, so an unreadable agent is a "
               "broken one however good its decisions."},
 ],
 "takeaways": [
   "The frame budget gives roughly 20–40 microseconds per agent per "
   "frame, so most agents must do nothing most frames.",
   "Behaviour trees won on authoring cost: state machines need O(n²) "
   "transitions and subtrees compose linearly.",
   "A behaviour tree is four node types and a three-valued return, and "
   "RUNNING is what makes it work in a game loop.",
   "Any subtree can substitute for any node, which is the whole "
   "compositional advantage.",
   "Utility systems handle many competing concerns and degrade gracefully, "
   "at a real cost in debuggability — so log every score.",
   "Layer by timescale, and make behaviour legible: a player who cannot "
   "predict an agent cannot play against it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The frame budget"),
  ("callout", "The frame budget is the design constraint, with arithmetic",
   ["<b>Sixty frames per second is 16.7 milliseconds total</b>, shared "
    "between rendering, physics, animation, audio, networking, game "
    "logic, and every agent's decision-making.",
    "<b>AI typically gets one to two milliseconds of that.</b> <b>With "
    "fifty active agents that is twenty to forty "
    "<i>microseconds</i> per agent per frame</b> — which is a few "
    "thousand instructions, and will not accommodate a search.",
    "<b>So most agents must do nothing on most frames.</b> The standard "
    "answers are <b>staggered updates</b> (each agent re-decides every "
    "n-th frame, with the phases spread so the cost is even), <b>level-of"
    "-detail AI</b> (distant or off-screen agents think less often and "
    "more coarsely, or are simulated statistically), and <b>event-driven "
    "rather than polled logic</b> (react when something happens rather "
    "than checking every frame whether it has).",
    "<b>And the architecture must be interruptible and incremental</b> "
    "— <b>which rules out anything that must run to completion "
    "before producing a usable answer</b>, and is exactly why anytime "
    "algorithms keep appearing in this course (Module 03 &sect;4's "
    "anytime A*, Module 05 &sect;3's MCTS, Module 04 &sect;3's "
    "time-slicing). <b>The frame budget is not a detail of game AI; it is "
    "the reason game AI selected the methods it did.</b>"]),
  ("table", ["", "Finite state machine", "Behaviour tree", "Utility system"],
   [["<b>Decides by</b>", "<b>Current state plus transition "
     "conditions.</b>", "<b>Walking a tree from the root each tick.</b>",
     "<b>Scoring every available option.</b>"],
    ["<b>Authoring cost</b>",
     "<b>O(n&#178;) transitions — every state potentially needs an "
     "edge to every other.</b>",
     "<b>Composable subtrees; linear in behaviours.</b>",
     "<b>Tune a curve per consideration per action.</b>"],
    ["<b>Scales to</b>", "<b>About ten states before it is "
     "unmanageable.</b>", "<b>Hundreds of nodes.</b>",
     "<b>Many options, with care.</b>"],
    ["<b>Debugging</b>", "<b>Easy — you are in one state.</b>",
     "<b>Easy — inspect the currently active path.</b>",
     "<b>Hard — 'why did that score highest?'</b>"],
    ["<b>Best for</b>", "<b>Simple agents with few genuine modes.</b>",
     "<b>The default choice for most games.</b>",
     "<b>Agents balancing many competing concerns.</b>"]],
   [0.14, 0.30, 0.29, 0.27]),
  ("p", "<b>Behaviour trees won because of the authoring column.</b> "
        "<b>The transition explosion is what killed state machines</b> "
        "— adding a 'stunned' state to a ten-state machine means "
        "considering ten new transitions in and ten out, and the designer "
        "must get all twenty right — <b>and composability is what "
        "fixed it</b>."),

  ("h1", "2 &nbsp; Behaviour trees"),
  ("code", """Every node, when ticked, returns SUCCESS, FAILURE, or
RUNNING. That is the entire interface.

SEQUENCE    tick children in order; fail immediately if any
            child fails; succeed when all have succeeded.
            ("AND", or "do this, then this")
SELECTOR    tick children in order; succeed immediately if
            any child succeeds; fail if all fail.
            ("OR", or "try this, otherwise this")
DECORATOR   wrap exactly one child and modify it: invert
            its result, repeat it, add a cooldown, add a
            precondition guard, limit its runtime.
LEAF        an action to perform, or a condition to check.

THAT IS IT. Four node types.

WHY IT COMPOSES: a subtree's interface is identical to a
leaf's, so ANY subtree can be substituted anywhere a node
is expected. Build "FightEnemy" once, reuse it in twelve
places, and improve it once for all twelve.
    -- which is why the authoring cost is LINEAR in the
       number of behaviours rather than QUADRATIC in the
       number of states.

RUNNING is the part people get wrong. It means "I am not
finished; tick me again next frame". It is what makes the
tree usable in a game loop at all -- and it means the tree
carries state between ticks (which node is currently
running), so A BEHAVIOUR TREE IS NOT A PURE FUNCTION OF THE
WORLD. Implementations that forget this restart long
actions every frame.

PRIORITY IS STRUCTURAL: a selector's left-to-right child
order IS the priority order. Put "flee if nearly dead"
leftmost, and it pre-empts everything to its right."""),
  ("p", "<b>The substitutability of subtrees is the whole advantage</b>, "
        "and <b>it is the same compositional property that makes a good "
        "API good</b> — a uniform interface at every level of "
        "granularity, so that composition does not require knowing what "
        "you are composing. <b>Which is why behaviour trees are "
        "authorable by designers rather than only by programmers</b>, and "
        "that, rather than any runtime property, is why they are the "
        "industry default."),
  ("callout", "Utility systems, and when they beat trees",
   ["<b>Score every available action with a utility function over the "
    "current world state, then take the highest-scoring one.</b> No "
    "structure at all — a flat list of options and a scoring "
    "function per option.",
    "<b>The strength is handling many competing considerations.</b> "
    "Health, ammunition, distance to target, availability of cover, "
    "nearby allies, cooldown states — <b>each contributes to each "
    "action's score through a tunable response curve</b>, and the "
    "combination handles situations nobody enumerated. <b>A behaviour "
    "tree encoding the same trade-offs needs a condition per combination, "
    "which is the transition explosion in another form.</b>",
    "<b>And it degrades gracefully.</b> <b>There is always a "
    "highest-scoring action</b>, so there is no 'no valid behaviour' "
    "state — which a behaviour tree does reach (every child of the "
    "root selector fails) and must handle explicitly with a fallback.",
    "<b>The weakness is debuggability.</b> <b>'Why did it do that?' "
    "becomes a matter of comparing twenty scores and the dozen curve "
    "evaluations behind each</b>, and <b>tuning one curve shifts every "
    "decision that curve participates in</b> — so changes are "
    "non-local in a way behaviour-tree edits are not. <b>Log every "
    "score, always</b>, and ship the log in a debug overlay: it is the "
    "only thing that makes the architecture maintainable."]),

  ("break",),
  ("h1", "3 &nbsp; Movement and steering"),
  ("ul", ["<b>Seek, flee, and arrive.</b> A desired velocity toward or "
          "away from a target point, with <i>arrive</i> scaling the "
          "desired speed down as the distance falls so the agent stops "
          "rather than overshooting and oscillating.",
          "<b>Path following.</b> Seek the next point on the path from "
          "Module 04, <b>looking ahead along the path rather than at "
          "the immediate next node</b>, which makes the agent cut corners "
          "naturally and removes the need for much of &sect;2's "
          "smoothing.",
          "<b>Separation, alignment, and cohesion.</b> <b>The three "
          "rules that produce flocking</b> — stay apart, match "
          "neighbours' headings, move toward the local centre — and "
          "<b>the classic demonstration that simple reflex agents "
          "(Module 01 &sect;1) produce complex collective "
          "behaviour</b> with no coordination, no plan, and no "
          "communication.",
          "<b>Obstacle avoidance and reciprocal velocity obstacles.</b> "
          "<b>RVO has each agent assume the others are also avoiding, and "
          "take half the required correction</b> — which prevents the "
          "oscillation that naive mutual avoidance produces, where both "
          "agents dodge the same way, then both dodge back.",
          "<b>Composed by weighted sum, or by priority.</b> <b>Weighted "
          "sums cancel</b>: two avoidance forces from opposite walls in a "
          "corridor sum to approximately zero, <b>and the agent "
          "calmly walks into the wall ahead</b> because the only surviving "
          "component was the seek. <b>This is the classic steering "
          "bug.</b> <b>Prioritised composition (take the highest-priority "
          "non-zero behaviour) or truncated accumulation (add behaviours "
          "until the force budget is used) avoids it</b>, at the cost of "
          "less smooth motion — which is the right trade, since "
          "smoothness is cosmetic and walking into walls is not."]),

  ("h1", "4 &nbsp; Choosing, and legibility"),
  ("callout", "Layer by timescale",
   ["<b>Strategic layer (seconds): which goal to pursue.</b> A behaviour "
    "tree, a utility score, or a planner (Module 07). <b>Runs rarely</b> "
    "— every few hundred milliseconds, or on events.",
    "<b>Tactical layer (hundreds of milliseconds): which path, which "
    "cover point, which target.</b> Pathfinding (Module 04) and spatial "
    "queries. <b>Runs on demand</b>, and is time-sliced when it must.",
    "<b>Steering layer (every frame): where to move right now.</b> "
    "<b>Reflex behaviours only</b> (&sect;3) — <b>Module 01 "
    "&sect;1's cheapest agent design, doing the most frequent work</b>, "
    "which is the correct assignment and not a compromise.",
    "<b>Each layer runs at its own rate, and the division is by how fast "
    "the relevant information changes.</b> <b>Which is the same "
    "decomposition as Module 04 &sect;4's three movement layers</b>, "
    "and <b>getting the division wrong — putting avoidance in the "
    "planner, or target selection in the steering — is the commonest "
    "architectural mistake in game AI</b>, because it couples a "
    "fast-changing input to a slow-running computation."]),
  ("ul", ["<b>Telegraph intent.</b> An animation, a sound, or a stance "
          "change before the action, so the player has time to respond. "
          "<b>A perfectly-timed instant attack reads as unfair rather "
          "than as skilled</b>, and <b>deliberately slowing an agent's "
          "reaction is a feature</b> — which is the clearest case of "
          "optimality being the wrong objective (Module 05 "
          "&sect;4).",
          "<b>Commit visibly.</b> <b>An agent that changes its mind "
          "every frame appears broken even when every individual decision "
          "is correct</b>, because the player sees indecision rather than "
          "responsiveness. <b>Add hysteresis</b> — require a new "
          "option to beat the current one by a margin — which is "
          "Module 04 &sect;4's oscillation fix at a higher level.",
          "<b>Fail legibly.</b> If the agent cannot reach you, it should "
          "visibly try and fail — approach, pause, look, reposition "
          "— <b>rather than stand still</b>, which reads as a bug "
          "even when it is the correct response to an unreachable "
          "target.",
          "<b>And log the decision.</b> <b>Ship a debug overlay showing "
          "each agent's active behaviour and the reason for it</b> "
          "— the active tree path, or the top three utility scores. "
          "<b>It pays for itself within a week</b> and it is the "
          "practical form of Module 01 &sect;4's debuggability "
          "argument.",
          "<b>Legibility is a functional requirement rather than "
          "polish.</b> <b>A player who cannot predict an agent cannot "
          "play against it</b>, so <b>an unreadable agent is a broken "
          "agent however good its decisions are</b> — which means "
          "legibility belongs in the architecture's requirements alongside "
          "the frame budget, and not in a list of nice-to-haves."]),
 ],
 "resources": [
   ("Game AI Pro, volumes 1–3 (free online)",
    "https://www.gameaipro.com/",
    "<b>The reference for this entire module</b> — chapters by "
    "shipping practitioners on behaviour trees, utility systems, "
    "steering, and the frame-budget engineering of &sect;1."),
   ("Millington &mdash; AI for Games, 3rd edition",
    "https://www.routledge.com/AI-for-Games-Third-Edition/Millington/p/book/9780367670566",
    "<b>The systematic treatment of &sect;2 and &sect;3</b>, with "
    "pseudocode throughout. Library copy."),
   ("Colledanchise & Ögren &mdash; Behavior Trees in Robotics and "
    "AI (free PDF)",
    "https://arxiv.org/abs/1709.00084",
    "<b>&sect;2 treated formally</b>, including the relationship to state "
    "machines and the composability argument made precise."),
   ("Reynolds &mdash; Steering Behaviors For Autonomous Characters "
    "(free)",
    "https://www.red3d.com/cwr/steer/",
    "<b>The &sect;3 behaviours, from the originator</b>, with "
    "demonstrations. The flocking paper is here too."),
 ],
 "exercises": [
   "<b>Compute your own per-agent frame budget</b> for a target agent "
   "count and frame rate.",
   "<b>Implement staggered updates</b> and measure the frame-time "
   "variance before and after.",
   "<b>Build a ten-state FSM</b> for an agent, then add one state and "
   "count the transitions you had to consider.",
   "<b>Rebuild the same behaviour as a behaviour tree</b> and compare the "
   "authoring effort.",
   "<b>Implement the four node types</b> and confirm a subtree can "
   "substitute for a leaf.",
   "<b>Implement RUNNING incorrectly</b> (restart every frame) and "
   "observe the symptom.",
   "<b>Build a utility system</b> for the same agent and log every score "
   "each tick.",
   "<b>Change one curve</b> and report how many decisions changed.",
   "<b>Implement flocking</b> with the three rules and 200 agents.",
   "<b>Reproduce the weighted-sum cancellation bug</b> in a corridor, "
   "then fix it by prioritised composition.",
 ],
 "selfcheck": [
   "Compute the per-agent frame budget and name three ways to live "
   "within it.",
   "Why must a game AI architecture be interruptible?",
   "Compare FSMs, behaviour trees, and utility systems on five axes.",
   "Why did behaviour trees displace state machines?",
   "Name the four node types and state why subtrees compose.",
   "What does RUNNING mean, and what does it imply about purity?",
   "When does a utility system beat a tree, and what does it cost?",
   "Name five steering behaviours and the cancellation bug.",
   "Give the three layers and the principle dividing them.",
   "Why is legibility a functional requirement?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Multiple Agents",
 "subtitle": "Coordination, crowds, and emergence.",
 "question": "What happens when many agents act at once?",
 "outcomes": [
     "Explain why multi-agent problems are not just harder "
     "single-agent ones.",
     "Implement coordinated multi-agent pathfinding.",
     "Explain crowd simulation and its characteristic failures.",
     "Explain emergence and how to design for it.",
     "Explain the basic game-theoretic concepts an agent needs.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why it is different",
   "blurb": "The environment contains reasoners."},

  {"t": "callout", "title": "Other agents are not obstacles",
   "kind": "The structural difference",
   "body": ["<b>Treating other agents as moving obstacles is the "
            "cheap approximation and it fails in a specific way:</b> "
            "<b>both agents plan around the other's predicted path, and "
            "both predictions are now wrong.</b>",
            "<b>Two agents in a corridor each step aside, then each "
            "step back</b> — the oscillation is not a bug in either "
            "agent, it is the result of each modelling the other as "
            "non-reactive.",
            "<b>RVO fixes it by assumption</b> (Module 11 "
            "§3): assume the other is also avoiding, and take "
            "half the correction. <b>A convention, shared.</b>",
            "<b>And the general lesson is that coordination requires "
            "either communication or a shared convention</b> — and "
            "<b>in a game you can simply impose the convention</b>, "
            "which is a luxury robotics does not have."]},

  {"t": "section", "label": "Part 2", "title": "Multi-agent pathfinding",
   "blurb": "Finding paths that do not collide."},

  {"t": "code", "kicker": "MAPF", "title": "Three approaches, and the trade",
   "lang": "text", "code": """
  THE PROBLEM: k agents, k start/goal pairs, paths that
  never collide (in space or in time).

  COUPLED -- search the JOINT state space.
      Optimal. The state space is the PRODUCT of the
      individual ones, so it is exponential in k.
      Viable to maybe k = 5 on a small map.

  DECOUPLED / PRIORITISED -- plan agents one at a time,
  each treating the already-planned ones as moving
  obstacles.
      Fast and linear in k. INCOMPLETE: it can fail on a
      solvable instance, because an early agent's path may
      make a later one impossible. Standard anyway.

  CONFLICT-BASED SEARCH (CBS) -- plan independently, find
  a collision, then BRANCH on it: one child forbids agent A
  from that cell at that time, the other forbids agent B.
  Replan only the constrained agent.
      OPTIMAL, and far faster than coupled search in
      practice, because most agents never conflict.

  CBS IS BRANCH AND BOUND (CSCE 669 Module 09) WITH
  COLLISIONS AS THE BRANCHING VARIABLE -- and it is the
  same "learn from the conflict" idea as CDCL (Module 08).
""",
   "caption": "<b>CBS is the one worth knowing</b> — it is optimal, "
              "practical, and structurally identical to two other "
              "algorithms in this program.",
   "note": "The three-way connection (CBS, branch and bound, CDCL) is the "
           "intellectual payoff."},

  {"t": "section", "label": "Part 3", "title": "Crowds",
   "blurb": "Hundreds of agents, and what goes wrong."},

  {"t": "table", "kicker": "Crowds", "title": "Crowd models and their failures",
   "header": ["Model", "How", "Characteristic failure"],
   "widths": [2.5, 4.1, 5.4],
   "rows": [
     ["<b>Social forces</b>", "<b>Agents repel; goal attracts</b>", "<b>Agents visibly jitter and interpenetrate</b>"],
     ["<b>RVO / ORCA</b>", "<b>Velocity-space collision avoidance</b>", "<b>Deadlock in dense bidirectional flow</b>"],
     ["<b>Continuum / flow</b>", "<b>Treat the crowd as a fluid</b>", "<b>Individuals lose agency; no personal goals</b>"],
     ["<b>Flow fields</b>", "<b>Shared direction field (M04 §3)</b>", "<b>Everyone takes the same route</b>"],
     ["<b>Hybrid</b>", "Flow field + local avoidance", "<b>What production uses. Tuning is empirical</b>"],
   ],
   "footnote": "<b>Dense bidirectional flow through a narrow gap "
               "deadlocks every local method</b>, and the production fix "
               "is a global one — queueing, lane assignment, or "
               "capacity limits.",
   "note": "Naming the universal failure case prevents a lot of wasted "
           "tuning."},

  {"t": "callout", "title": "Emergence is designed, not hoped for",
   "kind": "The honest account",
   "body": ["<b>Flocking from three rules is the famous "
            "example</b> (Module 11 §3) <b>and it is "
            "genuinely striking</b> — complex coordinated motion from "
            "purely local reflexes.",
            "<b>But emergence is not free.</b> <b>Most simple rule sets "
            "produce either nothing interesting or chaos</b>, and "
            "Reynolds' three rules were found by iteration, not "
            "derived.",
            "<b>So designing for emergence means tuning toward a "
            "target behaviour</b>, with a way to measure whether you "
            "have it — which means defining the target first.",
            "<b>And emergent systems are hard to constrain.</b> <b>'The "
            "crowd should never block this doorway' is not expressible as "
            "a local rule</b>, so you end up adding global overrides "
            "— which is where most of the engineering goes."]},

  {"t": "section", "label": "Part 4", "title": "Reasoning about others",
   "blurb": "The minimum game theory an agent needs."},

  {"t": "bullets", "kicker": "Game theory", "title": "The concepts that actually come up",
   "items": [
     "<b>Nash equilibrium:</b> no agent can improve by changing "
     "alone. <b>It may not be unique, and it may be bad for "
     "everyone</b> — the prisoner's dilemma is an equilibrium.",
     "",
     "<b>Dominant strategy:</b> best regardless of others. <b>When "
     "one exists, the problem is easy</b>; usually none does.",
     "",
     "<b>Mixed strategies:</b> <b>randomising is sometimes "
     "optimal</b> — a predictable agent is exploitable, which is "
     "why game AI should sometimes be deliberately random.",
     "",
     "<b>Cooperative games and coalitions</b> — who should team "
     "up, and how to split the gain (CSCE 717's subject).",
     "",
     "<b>And mechanism design:</b> <b>choose the rules so that "
     "self-interested behaviour produces what you want.</b> The "
     "designer's tool.",
   ],
   "footnote": "<b>Mechanism design is the one to take away for game "
               "design:</b> <b>you control the rules</b>, so you can make "
               "cooperation or competition the rational choice rather "
               "than hoping for it."},

  {"t": "callout", "title": "What a game designer should take from this",
   "kind": "Closing the module",
   "body": ["<b>Impose conventions rather than negotiating them.</b> "
            "<b>You control every agent</b>, so coordination is a "
            "shared-code problem rather than a game-theoretic one.",
            "<b>Use CBS or prioritised planning for tactical "
            "coordination</b>, and flow fields plus local avoidance for "
            "crowds.",
            "<b>Expect the deadlock case and handle it globally</b> "
            "— every local method fails there, so plan for it rather "
            "than tuning against it.",
            "<b>And randomise deliberately.</b> <b>A deterministic "
            "agent is solved by the player on the second "
            "encounter</b> — mixed strategies are not just theory, "
            "they are the difference between a fight and a puzzle you "
            "already solved."]},
 ],
 "takeaways": [
   "Treating other agents as obstacles fails because both plan around the "
   "other's predicted path and both predictions become wrong.",
   "Coordination requires communication or a shared convention — and "
   "in a game you can simply impose the convention.",
   "Conflict-based search is optimal and practical, and it is branch and "
   "bound with collisions as the branching variable.",
   "Dense bidirectional flow through a narrow gap deadlocks every local "
   "crowd method, so the fix must be global.",
   "Emergence is tuned toward a target, not hoped for — and emergent "
   "systems are hard to constrain, which is where the engineering goes.",
   "A deterministic agent is solved by the player on the second encounter, "
   "so mixed strategies are practical rather than theoretical.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why multi-agent is different"),
  ("callout", "Other agents are not obstacles",
   ["<b>Treating other agents as moving obstacles is the cheap "
    "approximation, and it fails in a specific and diagnosable way:</b> "
    "<b>both agents plan around the other's <i>predicted</i> path, and "
    "the act of planning invalidates both predictions.</b>",
    "<b>Two agents meeting in a corridor each step aside, observe that "
    "the other has also stepped aside, and each step back</b> — and "
    "the oscillation is not a bug in either agent. <b>Each is behaving "
    "correctly given a model of the other as non-reactive</b>, and the "
    "model is what is wrong.",
    "<b>RVO fixes it by assumption</b> (Module 11 &sect;3): assume "
    "the other agent is also avoiding, and take only half the required "
    "correction yourself. <b>It is a convention, shared by "
    "construction</b>, and it works because both agents run the same "
    "code.",
    "<b>And the general lesson is that coordination requires either "
    "communication or a shared convention.</b> <b>In a game you can "
    "simply impose the convention</b>, because you wrote every agent "
    "— <b>which is a luxury robotics and economics do not have</b>, "
    "and it is why multi-agent game AI is substantially easier than the "
    "general problem. <b>Exploit it rather than solving the harder "
    "problem.</b>"]),

  ("h1", "2 &nbsp; Multi-agent pathfinding"),
  ("code", """THE PROBLEM: k agents with k start/goal pairs, and paths
that never collide -- neither occupying the same cell at the
same time, nor swapping through each other.

COUPLED -- search the JOINT state space directly.
    Optimal and complete. The joint state space is the
    PRODUCT of the individual state spaces, so it is
    exponential in k. Viable to perhaps k = 5 on a small
    map, and not beyond.

DECOUPLED / PRIORITISED -- plan agents one at a time in
priority order, each treating the already-planned agents as
moving obstacles in space-time.
    Fast, linear in k, and INCOMPLETE: it can fail on a
    solvable instance, because an early agent's path may
    make a later agent's goal unreachable. Used widely
    anyway, because it is fast and usually works.

CONFLICT-BASED SEARCH (CBS) -- plan every agent
independently, find the first collision, and BRANCH on it:
one child forbids agent A from that cell at that timestep,
the other forbids agent B. Replan only the newly
constrained agent, and recurse.
    OPTIMAL, and far faster than coupled search in
    practice, because MOST AGENTS NEVER CONFLICT and only
    the conflicts cost anything.

CBS IS BRANCH AND BOUND (CSCE 669 Module 09) WITH
COLLISIONS AS THE BRANCHING VARIABLE -- and it is the same
"learn from the conflict rather than retreating from it"
idea as CDCL (Module 08 section 2)."""),
  ("p", "<b>CBS is the one worth knowing.</b> It is optimal, practical at "
        "useful scales, and <b>structurally identical to two other "
        "algorithms in this program</b> — which is worth noticing, "
        "because <b>'search the relaxed problem, find the violated "
        "condition, branch on it' is a general pattern</b> rather than "
        "three coincidences, and recognising it lets you construct the "
        "algorithm for a new problem rather than looking one up."),

  ("h1", "3 &nbsp; Crowds"),
  ("table", ["Model", "How it works", "Characteristic failure"],
   [["<b>Social forces</b>",
     "<b>Agents exert repulsive forces on each other; the goal exerts "
     "attraction.</b>",
     "<b>Agents visibly jitter, and they interpenetrate under "
     "pressure</b> because a force-based method has no hard "
     "constraint."],
    ["<b>RVO / ORCA</b>",
     "<b>Collision avoidance computed in velocity space, choosing the "
     "nearest velocity that is collision-free for a time horizon.</b>",
     "<b>Deadlock in dense bidirectional flow</b> — see the note "
     "below."],
    ["<b>Continuum / flow models</b>",
     "<b>Treat the crowd as a fluid with a density and velocity "
     "field.</b>",
     "<b>Individuals lose agency: there are no personal goals and no "
     "individual decisions</b>, which is fine for background and wrong "
     "for anything the player interacts with."],
    ["<b>Flow fields</b>",
     "<b>One shared direction field per destination</b> (Module 04 "
     "&sect;3).",
     "<b>Everyone takes exactly the same route</b>, which looks "
     "mechanical and congests one corridor."],
    ["<b>Hybrid</b>",
     "A flow field for global direction plus local avoidance for "
     "immediate conflicts.",
     "<b>What production systems use</b>, and <b>the tuning is "
     "empirical</b> — there is no principled way to set the "
     "weights."]],
   [0.18, 0.37, 0.45]),
  ("p", "<b>Dense bidirectional flow through a narrow gap deadlocks every "
        "purely local method.</b> Two opposing streams meet in a doorway, "
        "each agent correctly refuses to collide, and nothing moves "
        "— and no amount of parameter tuning fixes it, because the "
        "information needed (who should go first) is not available "
        "locally. <b>The production fix is global:</b> explicit queueing, "
        "lane assignment by direction, or a capacity limit on the gap. "
        "<b>Knowing that this case is structurally unfixable locally "
        "prevents a great deal of wasted tuning</b>, which is the main "
        "reason to state it."),
  ("callout", "Emergence is designed, not hoped for",
   ["<b>Flocking from three local rules is the famous example</b> "
    "(Module 11 &sect;3) <b>and it is genuinely striking</b> — "
    "complex, coordinated, lifelike collective motion from purely local "
    "reflex behaviours with no communication and no plan.",
    "<b>But emergence is not free, and the famous example is "
    "selected.</b> <b>Most simple rule sets produce either nothing "
    "interesting or undirected chaos</b>, and <b>Reynolds' three rules "
    "were found by iteration against a target, not derived from "
    "principles.</b>",
    "<b>So designing for emergence means tuning toward a target "
    "behaviour, with a way to measure whether you have achieved "
    "it</b> — <b>which means defining the target first</b>, in "
    "measurable terms. 'The crowd should look alive' is not a target; "
    "'agents should maintain 0.5 to 1.5 metres of separation while "
    "sustaining 80% of free-flow speed' is.",
    "<b>And emergent systems are hard to constrain.</b> <b>'The crowd "
    "should never block this doorway' is not expressible as a local "
    "rule</b>, because no individual agent can perceive the global "
    "condition — <b>so you end up adding global overrides, and that "
    "is where most of the engineering goes</b>. <b>Which is the honest "
    "shape of emergent design:</b> a local system that produces the "
    "texture, plus global machinery that enforces the requirements, and "
    "the second is larger than the first."]),

  ("break",),
  ("h1", "4 &nbsp; Reasoning about other agents"),
  ("ul", ["<b>Nash equilibrium:</b> a joint strategy where no agent can "
          "improve its outcome by changing its own strategy alone. <b>It "
          "may not be unique, and it may be bad for everyone</b> — "
          "<b>mutual defection in the prisoner's dilemma is an "
          "equilibrium</b>, which is the standard illustration that "
          "equilibrium does not mean good.",
          "<b>Dominant strategy:</b> one that is best regardless of what "
          "others do. <b>When one exists the problem is easy and "
          "reasoning about others is unnecessary</b>; usually none "
          "exists, which is why the subject is hard.",
          "<b>Mixed strategies:</b> <b>randomising over actions is "
          "sometimes strictly optimal</b> — rock-paper-scissors has "
          "no good deterministic strategy. <b>Which means a predictable "
          "agent is exploitable, and game AI should sometimes be "
          "deliberately random</b>, not as a concession but as the correct "
          "play.",
          "<b>Cooperative games and coalitions:</b> which agents should "
          "team up, and how the joint gain should be divided (the Shapley "
          "value and the core) — which is CSCE 717's subject, "
          "arriving in Semester 12.",
          "<b>And mechanism design:</b> <b>choose the rules of the "
          "interaction so that self-interested behaviour produces the "
          "outcome you want.</b> <b>This is the designer's tool and it is "
          "the one to take away</b>: you are not a player in the game, you "
          "are the person who writes it, so you can make cooperation or "
          "competition the rational choice rather than hoping agents or "
          "players choose it."]),
  ("callout", "What a game designer should take from this",
   ["<b>Impose conventions rather than negotiating them.</b> <b>You "
    "control every agent's code</b>, so coordination is a shared-state and "
    "shared-convention problem rather than a game-theoretic one "
    "(&sect;1) — and solving the easy version deliberately is better "
    "engineering than solving the hard version by accident.",
    "<b>Use CBS or prioritised planning for tactical coordination</b> "
    "(a squad moving through a building, where the agent count is small "
    "and the paths matter), <b>and flow fields plus local avoidance for "
    "crowds</b> (where the count is large and individual paths do not).",
    "<b>Expect the deadlock case and handle it globally.</b> <b>Every "
    "local method fails at a congested bidirectional gap</b> (&sect;3), "
    "<b>so design the global mechanism up front</b> rather than "
    "discovering the failure in playtest and tuning against it.",
    "<b>And randomise deliberately.</b> <b>A deterministic agent is "
    "solved by the player on the second encounter</b> and is thereafter a "
    "puzzle rather than an opponent — <b>so mixed strategies are "
    "practical rather than theoretical</b>, and they are the difference "
    "between a fight and a sequence the player executes. <b>This is "
    "Module 05 &sect;4's point about tuned difficulty, reached from "
    "the other direction:</b> the agent needs unpredictability for the "
    "same reason it needs legibility — both are about what the "
    "encounter is like to play, which is the actual objective."]),
 ],
 "resources": [
   ("Sharon et al. &mdash; Conflict-Based Search for Optimal Multi-Agent "
    "Pathfinding (free)",
    "https://www.sciencedirect.com/science/article/pii/S0004370214001386",
    "<b>The &sect;2 algorithm</b>, with the branching argument and the "
    "comparison against coupled search."),
   ("van den Berg et al. &mdash; Reciprocal n-body Collision Avoidance "
    "(ORCA) (free)",
    "https://gamma.cs.unc.edu/ORCA/",
    "<b>The &sect;1 and &sect;3 method</b>, with a free reference "
    "implementation used widely in games."),
   ("Reynolds &mdash; Flocks, Herds, and Schools (free)",
    "https://www.red3d.com/cwr/papers/1987/boids.html",
    "<b>The &sect;3 emergence example</b>, and the paper is candid about "
    "the rules being found by iteration."),
   ("Shoham & Leyton-Brown &mdash; Multiagent Systems (free PDF)",
    "http://www.masfoundations.org/",
    "<b>Free in full, and the reference for &sect;4</b> — game "
    "theory, coalitions, and mechanism design, aimed at computer "
    "scientists."),
 ],
 "exercises": [
   "<b>Reproduce the corridor oscillation</b> with two agents treating "
   "each other as obstacles.",
   "<b>Fix it with RVO</b> and confirm the oscillation stops.",
   "<b>Implement coupled multi-agent search</b> and report the state "
   "count against k.",
   "<b>Implement prioritised planning</b> and construct an instance where "
   "it fails although a solution exists.",
   "<b>Implement CBS</b> and compare node counts against coupled search "
   "for k = 2 to 8.",
   "<b>Simulate 200 agents with a flow field plus local avoidance</b> and "
   "measure throughput through a doorway.",
   "<b>Create the bidirectional deadlock</b> and confirm no parameter "
   "setting resolves it.",
   "<b>Add a global lane assignment</b> and report the throughput "
   "improvement.",
   "<b>Implement flocking and define a measurable target</b>, then tune "
   "toward it and report the metric.",
   "<b>Build a deterministic agent and a mixed-strategy one</b> and have "
   "someone play both twice. Report what they said.",
 ],
 "selfcheck": [
   "Why does treating other agents as obstacles fail, specifically?",
   "What does RVO assume, and why can a game rely on it?",
   "Compare coupled, prioritised, and conflict-based multi-agent "
   "pathfinding.",
   "What is CBS structurally equivalent to, and in which two other "
   "courses?",
   "Name five crowd models and the failure of each.",
   "Why does dense bidirectional flow deadlock every local method?",
   "Why is emergence designed rather than hoped for?",
   "Why are emergent systems hard to constrain?",
   "Name five game-theoretic concepts and which is the designer's tool.",
   "Why should a game agent randomise?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Choosing an Approach",
 "subtitle": "And saying what the agent can do.",
 "question": "Given a problem, which of these twelve modules applies?",
 "outcomes": [
     "Choose a method from a problem's properties.",
     "Explain where learned and symbolic methods each belong.",
     "Explain hybrid architectures and why they dominate.",
     "Evaluate an agent honestly.",
     "State what an AI system can be trusted to do.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The decision",
   "blurb": "A checklist from the problem's properties."},

  {"t": "table", "kicker": "Choosing", "title": "From the problem to the method",
   "header": ["If the problem is", "Use", "Module"],
   "widths": [4.4, 3.4, 3.2],
   "rows": [
     ["<b>Find a route through space</b>", "<b>A* on a navmesh</b>", "<b>04</b>"],
     ["<b>Find a sequence of actions</b>", "<b>Planning, or A* on states</b>", "<b>07, 03</b>"],
     ["<b>Satisfy constraints, no costs</b>", "<b>CSP or SAT</b>", "<b>06, 08</b>"],
     ["<b>Beat an opponent</b>", "<b>Alpha-beta or MCTS</b>", "<b>05</b>"],
     ["<b>Act under known uncertainty</b>", "<b>MDP, solved offline</b>", "<b>10</b>"],
     ["<b>Infer hidden state</b>", "<b>Bayes net or a filter</b>", "<b>09</b>"],
     ["<b>Produce plausible behaviour cheaply</b>", "<b>Behaviour tree or utility</b>", "<b>11</b>"],
     ["<b>Unknown dynamics, lots of interaction</b>", "<b>Reinforcement learning</b>", "<b>CSCE 642</b>"],
   ],
   "footnote": "<b>Work down this table before reaching for a learned "
               "method</b> — most game and robotics problems are "
               "answered in the first seven rows, faster and more "
               "controllably.",
   "note": "This table is the single most useful artefact of the "
           "course."},

  {"t": "callout", "title": "Two questions that resolve most choices",
   "kind": "The short version",
   "body": ["<b>Do you have a model of the dynamics?</b> If yes, "
            "compute (this course). If no, learn (CSCE 642) or build "
            "one.",
            "<b>Does a designer need to control the behaviour "
            "directly?</b> If yes, use an authorable architecture "
            "(Module 11). If no, optimality is available.",
            "<b>Those two questions eliminate most of the "
            "table</b> — and they are both about your situation "
            "rather than about the algorithms.",
            "<b>Then the third question is the budget:</b> "
            "<b>microseconds per agent per frame</b> (Module 11 "
            "§1) <b>rules out most of what remains</b>, which is "
            "why precomputation keeps appearing as the answer."]},

  {"t": "section", "label": "Part 2", "title": "Symbolic and learned",
   "blurb": "Where each belongs, without advocacy."},

  {"t": "table", "kicker": "Comparison", "title": "What each is actually good at",
   "header": ["", "This course's methods", "Learned methods"],
   "widths": [2.3, 4.4, 5.3],
   "rows": [
     ["<b>Guarantees</b>", "<b>Optimality, completeness, proofs</b>", "<b>None</b>"],
     ["<b>Debugging</b>", "<b>Trace the decision</b>", "<b>Saliency and hope</b>"],
     ["<b>Data</b>", "<b>None needed</b>", "<b>A lot, matched to deployment</b>"],
     ["<b>Perception</b>", "<b>Cannot do it</b>", "<b>The only option (CSCE 753)</b>"],
     ["<b>Messy rules</b>", "<b>Must be stated</b>", "<b>Learned from examples</b>"],
     ["<b>Cost</b>", "<b>Microseconds</b>", "<b>Milliseconds, plus a GPU</b>"],
   ],
   "footnote": "<b>The division is clean:</b> <b>symbolic methods for "
               "crisp problems with known rules; learned methods for "
               "perception and for rules nobody can write down.</b>",
   "note": "Stating the division plainly is more useful than arguing for "
           "either side."},

  {"t": "callout", "title": "Every working system is a hybrid",
   "kind": "The actual state of practice",
   "body": ["<b>A self-driving stack is learned perception "
            "(CSCE 753) feeding symbolic planning and control</b> "
            "— and the division is at the interface between "
            "'what is out there' and 'what to do'.",
            "<b>AlphaZero is MCTS with a learned evaluation</b> "
            "(Module 05 §3) — a classical search with the "
            "hard part learned.",
            "<b>A game's AI is behaviour trees with learned "
            "animation</b>, and occasionally a learned component for one "
            "specific hard judgement.",
            "<b>The pattern is consistent:</b> <b>learning supplies "
            "what cannot be written down; structure supplies the "
            "guarantees and the control.</b> <b>Neither replaces the "
            "other, and the interface between them is where the "
            "engineering is.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Evaluating an agent",
   "blurb": "What to measure."},

  {"t": "bullets", "kicker": "Evaluation", "title": "What an agent evaluation contains",
   "items": [
     "<b>A trivial baseline.</b> <b>Random, greedy, or "
     "do-nothing</b> — and report it. <b>CSCE 633's discipline, "
     "unchanged across eight courses.</b>",
     "",
     "<b>Nodes expanded or decisions per second</b>, not only "
     "wall-clock time (Module 03 §4).",
     "",
     "<b>p99 latency</b>, because a frame budget is a hard deadline "
     "and the mean does not describe it.",
     "",
     "<b>Behaviour on the cases you did not design for</b> — "
     "the agent will meet them.",
     "",
     "<b>And a failure list.</b> <b>The situations where it does "
     "something wrong, with the cause of each</b>, which is the "
     "deliverable.",
   ],
   "footnote": "<b>For a game agent, add a human judgement:</b> "
               "<b>'is it fun to play against' is the real metric and no "
               "computation measures it.</b>"},

  {"t": "section", "label": "Part 4", "title": "Claiming honestly",
   "blurb": "The course, and the semester, closed."},

  {"t": "callout", "title": "What an AI system can honestly promise",
   "kind": "Scoped claims",
   "body": ["<b>'A* returns the shortest path on this navigation mesh, "
            "provably, in under 200 µs at p99 for 100 "
            "agents.'</b> <b>Every clause checkable.</b>",
            "<b>'The planner finds a plan when one exists within 8 "
            "actions; beyond that it times out and the agent falls back "
            "to the behaviour tree.'</b> <b>The limit stated, with the "
            "fallback.</b>",
            "<b>'The policy is optimal for this MDP. The MDP assumes "
            "the player moves independently of the agent, which is "
            "false.'</b> <b>Optimal <i>for this model</i></b> — "
            "CSCE 669 Module 13's four words.",
            "<b>And what you cannot say: 'the agent is "
            "intelligent'.</b> <b>It searches a space you defined with a "
            "heuristic you chose, under a model you approximated.</b> "
            "<b>Say that instead; it is more impressive and it is "
            "true.</b>"]},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can formulate a problem as a state space, choose a "
            "search, design a heuristic, and ship pathfinding that "
            "works.</b>",
            "<b>You can model constraints, plan with declarative "
            "actions, use a SAT solver, reason probabilistically, and "
            "solve an MDP.</b>",
            "<b>And you can choose an agent architecture and defend the "
            "choice</b> — which is the thing the track needed, because "
            "<b>every game engine contains most of this course.</b>",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it means saying which "
            "space you searched</b> — because the space was your "
            "approximation, and the agent is only as good as it."]},
 ],
 "takeaways": [
   "Work down the problem-to-method table before reaching for a learned "
   "approach — most game and robotics problems are answered in the "
   "first seven rows.",
   "Two questions resolve most choices: do you have a model, and does a "
   "designer need direct control?",
   "The division is clean: symbolic methods for crisp problems with known "
   "rules, learned methods for perception and unwritable rules.",
   "Every working system is a hybrid, and the interface between the "
   "learned and structured parts is where the engineering is.",
   "Report a trivial baseline, nodes or decisions rather than only "
   "seconds, p99 latency, and a failure list with causes.",
   "You cannot say 'the agent is intelligent'; you can say which space it "
   "searched, with which heuristic, under which model — which is "
   "more impressive and is true.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Choosing a method"),
  ("table", ["If the problem is", "Use", "Module"],
   [["<b>Find a route through space</b>",
     "<b>A* on a navigation mesh, with a hierarchy if the level is "
     "large.</b>", "<b>04, 03</b>"],
    ["<b>Find a sequence of actions to achieve a goal</b>",
     "<b>Classical planning if the actions are declarative; A* over "
     "states otherwise.</b>", "<b>07, 02, 03</b>"],
    ["<b>Satisfy a set of constraints, with no costs to minimise</b>",
     "<b>A constraint solver, or encode to SAT.</b>", "<b>06, 08</b>"],
    ["<b>Beat an opponent</b>",
     "<b>Alpha-beta if a good evaluation exists; MCTS if not.</b>",
     "<b>05</b>"],
    ["<b>Act under uncertainty you can model</b>",
     "<b>An MDP, solved offline and shipped as a policy table.</b>",
     "<b>10</b>"],
    ["<b>Infer hidden state from observations</b>",
     "<b>A Bayesian network, or a filter if it is sequential.</b>",
     "<b>09</b>"],
    ["<b>Produce plausible behaviour cheaply and controllably</b>",
     "<b>A behaviour tree, or a utility system if concerns "
     "compete.</b>", "<b>11</b>"],
    ["<b>Unknown dynamics, and a great deal of interaction "
     "available</b>", "<b>Reinforcement learning.</b>",
     "<b>CSCE 642</b>"]],
   [0.40, 0.38, 0.22]),
  ("p", "<b>Work down that table before reaching for a learned "
        "method.</b> <b>Most game and robotics problems are answered in "
        "the first seven rows — faster, more controllably, and with "
        "guarantees</b> — and reaching for the eighth row first is "
        "the most common and most expensive error in applied AI."),
  ("callout", "Two questions that resolve most choices",
   ["<b>Do you have a model of the dynamics?</b> If yes, you can compute "
    "— which is this entire course. If no, either learn the policy "
    "from interaction (CSCE 642) or build a model and then compute, and "
    "<b>building a model is underrated</b>: an approximate model plus "
    "exact computation frequently beats no model plus learning, and it is "
    "debuggable.",
    "<b>Does a designer need to control the behaviour directly?</b> If "
    "yes, use an authorable architecture (Module 11) and accept "
    "suboptimality. If no, optimality is available — <b>and 'no' is "
    "rarer than it sounds</b>, because somebody almost always needs to "
    "adjust the result later.",
    "<b>Those two questions eliminate most of the table</b>, and both are "
    "<b>questions about your situation rather than about the "
    "algorithms</b> — which is why method selection is not a "
    "technical comparison exercise.",
    "<b>Then the third question is the budget.</b> <b>Microseconds per "
    "agent per frame</b> (Module 11 &sect;1) <b>rules out most of what "
    "remains</b> — which is why <b>precomputation keeps appearing "
    "as the answer</b> throughout this course (pattern databases, "
    "hierarchies, flow fields, offline-solved MDPs). <b>If the budget is "
    "microseconds and the computation is milliseconds, move the "
    "computation offline</b>, and that single move resolves a remarkable "
    "number of apparent impossibilities."]),

  ("h1", "2 &nbsp; Symbolic and learned"),
  ("table", ["", "This course's methods", "Learned methods"],
   [["<b>Guarantees</b>",
     "<b>Optimality, completeness, and machine-checkable proofs</b> "
     "(Modules 03, 08).", "<b>None.</b>"],
    ["<b>Debugging</b>",
     "<b>Trace the decision — the costs, the heuristic values, the "
     "active tree path.</b>",
     "<b>A saliency map and hope</b> (CSCE 753 Module 08 "
     "&sect;4)."],
    ["<b>Data required</b>", "<b>None.</b>",
     "<b>A great deal, and matched to the deployment "
     "distribution</b> (CSCE 753 Module 12)."],
    ["<b>Perception</b>",
     "<b>Cannot do it at all</b> — these methods need symbols as "
     "input.",
     "<b>The only option</b> (CSCE 753)."],
    ["<b>Rules too messy to state</b>",
     "<b>Must be stated, or they are not in the system.</b>",
     "<b>Learned from examples, which is the whole advantage.</b>"],
    ["<b>Runtime cost</b>", "<b>Microseconds on a CPU core.</b>",
     "<b>Milliseconds, plus a GPU.</b>"]],
   [0.17, 0.40, 0.43]),
  ("p", "<b>The division is clean when stated plainly:</b> <b>symbolic "
        "methods for crisp problems with known rules; learned methods for "
        "perception and for rules nobody can write down.</b> <b>Arguing "
        "for either side in general is a category error</b>, because they "
        "are good at disjoint things — and the useful skill is "
        "recognising which part of your problem is which."),
  ("callout", "Every working system is a hybrid",
   ["<b>A self-driving stack is learned perception (CSCE 753) feeding "
    "symbolic planning and control</b> — and <b>the division falls "
    "exactly at the interface between 'what is out there' and 'what to "
    "do'</b>, which is the division the table above predicts.",
    "<b>AlphaZero is MCTS with a learned evaluation function and "
    "prior</b> (Module 05 &sect;3) — <b>a classical search with "
    "the part nobody could write down supplied by learning.</b>",
    "<b>A game's AI is behaviour trees and pathfinding, with learned "
    "animation blending</b>, and occasionally one learned component for a "
    "specific hard judgement that resisted authoring.",
    "<b>The pattern is consistent across all three:</b> <b>learning "
    "supplies what cannot be written down; structure supplies the "
    "guarantees, the speed, and the control.</b> <b>Neither replaces the "
    "other, and the interface between them is where the engineering "
    "is</b> — specifically, <b>the interface must carry uncertainty</b>, "
    "because the learned side is sometimes wrong and the symbolic side "
    "will otherwise act on it with full confidence (CSCE 753 "
    "Module 13 &sect;4's abstention argument, from the consuming "
    "side)."]),

  ("break",),
  ("h1", "3 &nbsp; Evaluating an agent"),
  ("ul", ["<b>A trivial baseline.</b> <b>Random action, greedy "
          "one-step, or do-nothing</b> — and <b>report it</b>. "
          "<b>CSCE 633 Module 02's discipline, unchanged across eight "
          "courses</b>, and it catches the case where your elaborate agent "
          "is worse than moving toward the player.",
          "<b>Nodes expanded, or decisions per second</b>, not only "
          "wall-clock time (Module 03 &sect;4) — so the "
          "measurement separates the algorithm from the implementation and "
          "can be compared against anything.",
          "<b>p99 latency, not the mean.</b> <b>A frame budget is a hard "
          "deadline and the mean does not describe compliance with "
          "it</b> — one search in a hundred overrunning is a visible "
          "stutter twice a second at 60 Hz (CSCE 678 Module 06, "
          "Module 04 &sect;4).",
          "<b>Behaviour on cases you did not design for.</b> The agent "
          "will meet them — a player will stand somewhere unexpected, "
          "a level will have a geometry you did not test — and "
          "<b>what it does then is a property of the system you should "
          "know rather than discover.</b>",
          "<b>And a failure list.</b> <b>The situations where it does "
          "something wrong, with the identified cause of each</b> "
          "— which is the deliverable, exactly as it was in "
          "CSCE 753 Module 12 &sect;4 and CSCE 633 Module 13. "
          "<b>For a game agent, add a human judgement:</b> <b>'is it "
          "interesting to play against' is the real metric and no "
          "computation measures it</b>, so the evaluation must include "
          "someone playing it."]),

  ("h1", "4 &nbsp; Claiming honestly"),
  ("callout", "What an AI system can honestly promise",
   ["<b>'A* returns the shortest path on this navigation mesh, provably, "
    "in under 200 microseconds at the 99th percentile with 100 active "
    "agents.'</b> <b>Every clause is checkable</b>, and the guarantee is "
    "a real one because the method has one (Module 03 &sect;1).",
    "<b>'The planner finds a plan whenever one exists within 8 actions; "
    "beyond that it times out and the agent falls back to the behaviour "
    "tree.'</b> <b>The limit stated, and the fallback stated</b> "
    "— which is what makes it a usable claim rather than an "
    "optimistic one.",
    "<b>'The policy is optimal for this MDP. The MDP assumes the player "
    "moves independently of the agent, which is false.'</b> <b>Optimal "
    "<i>for this model</i></b> — CSCE 669 Module 13 &sect;4's "
    "four words, and <b>the model's falsehood stated in the same "
    "breath</b> (Module 01 &sect;2's deliberate lie, written down "
    "where someone can read it).",
    "<b>And what you cannot honestly say: 'the agent is "
    "intelligent'.</b> <b>It searches a space you defined, with a "
    "heuristic you chose, under a model you approximated, within a budget "
    "you set.</b> <b>Say that instead — it is more impressive, it "
    "is checkable, and it is true.</b>"]),
  ("callout", "Where this course leaves you",
   ["<b>You can formulate a problem as a state space, choose a search "
    "strategy from its properties, design and verify a heuristic, and ship "
    "pathfinding that works at production scale</b> — which is the "
    "most immediately useful skill in the course for this track.",
    "<b>You can model a problem as constraints, plan with declarative "
    "actions and automatically derived heuristics, use a SAT or SMT solver "
    "rather than writing a custom search, reason probabilistically about "
    "hidden state, and solve a Markov decision process</b>.",
    "<b>And you can choose an agent architecture and defend the choice "
    "against the alternatives</b> — which is the thing this track "
    "needed, because <b>every game engine contains most of this "
    "course</b>, and the engineering question is almost never 'which "
    "algorithm' but 'which layer, at which rate, within which budget'.",
    "<b>The closing rule is the program's, unchanged across twenty "
    "courses:</b> <b>state what you measured, state what you assumed, and "
    "never claim more than you established.</b> <b>In artificial "
    "intelligence it means saying which space you searched</b> — "
    "<b>because the space was your approximation of the world "
    "(Module 01 &sect;2), and the agent is exactly as good as that "
    "approximation and no better.</b>"]),
 ],
 "resources": [
   ("Russell & Norvig &mdash; AIMA, chapter 1 and the concluding chapter",
    "https://aima.cs.berkeley.edu/",
    "<b>The field's own account of the symbolic/learned division of "
    "&sect;2</b>, from a source that covers both."),
   ("Game AI Pro &mdash; the architecture and postmortem chapters "
    "(free)",
    "https://www.gameaipro.com/",
    "<b>&sect;1's table as practitioners apply it</b>, with the "
    "constraints that drove each decision stated."),
   ("Sculley et al. &mdash; Hidden Technical Debt in Machine Learning "
    "Systems (free)",
    "https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html",
    "<b>Why the hybrid interface of &sect;2 is where the maintenance cost "
    "accumulates</b> — relevant well beyond machine learning."),
   ("Berkeley CS188 &mdash; the full project set (free)",
    "https://inst.eecs.berkeley.edu/~cs188/",
    "<b>If you want more practice</b>, the five Pacman projects cover "
    "Modules 02, 03, 05, 06, 09, and 10 with automatic grading."),
 ],
 "exercises": [
   "<b>Take three problems from your own work</b> and place each on "
   "&sect;1's table, with the reasoning written out.",
   "<b>Answer the two questions of &sect;1's callout</b> for each, and "
   "report whether they changed your choice.",
   "<b>Compute the budget</b> for each and check whether the chosen "
   "method fits.",
   "<b>For one problem, identify which part is symbolic and which is "
   "learned</b>, and describe the interface between them.",
   "<b>Specify what that interface must carry</b>, including the "
   "uncertainty.",
   "<b>Implement a trivial baseline</b> for your project agent and report "
   "how it compares.",
   "<b>Measure p50 and p99 decision latency</b> and report both.",
   "<b>Construct five situations you did not design for</b> and report "
   "the agent's behaviour in each.",
   "<b>Write the failure list</b> with a cause for each entry.",
   "<b>Project 2 is now due.</b> Submit the agent, the architecture "
   "justification against two alternatives, the baseline comparison, the "
   "p99 latency, and the honest statement of what it cannot do.",
 ],
 "selfcheck": [
   "Give the problem-to-method table from memory.",
   "What two questions resolve most method choices?",
   "Why is precomputation the recurring answer?",
   "Compare symbolic and learned methods on six axes.",
   "Why is arguing for either side in general a category error?",
   "Give three hybrid systems and say where the division falls in each.",
   "What must the interface between learned and symbolic parts carry?",
   "Name five components of an agent evaluation.",
   "Give three honest claims and the one thing you cannot say.",
   "In this course, what does 'state what you assumed' specifically "
   "mean?",
 ],
},

]
