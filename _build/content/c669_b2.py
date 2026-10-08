# -*- coding: utf-8 -*-
"""CSCE 669 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Convexity",
 "subtitle": "The property everything else depends on.",
 "question": "How do you recognise a convex problem?",
 "outcomes": [
     "Define convex sets and convex functions.",
     "Prove convexity by the standard tests.",
     "Apply the operations that preserve convexity.",
     "Recognise the standard convex functions.",
     "Explain disciplined convex programming.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The definitions",
   "blurb": "Two, and the second follows from the first."},

  {"t": "eq", "kicker": "Definitions", "title": "Convex sets and convex functions",
   "eqs": [
     ("C convex  ⟺  x,y ∈ C ⟹ θx + (1−θ)y ∈ C  for θ ∈ [0,1]",
      "The whole segment between any two points stays inside."),
     ("f convex  ⟺  f(θx + (1−θ)y) ≤ θf(x) + (1−θ)f(y)",
      "The chord lies above the function."),
     ("f convex  ⟺  its epigraph {(x,t) : f(x) ≤ t} is a convex set",
      "So the two definitions are one definition."),
   ],
   "caption": "<b>The epigraph formulation unifies them</b>, and makes "
              "several later results obvious rather than separate.",
   "note": "The epigraph view is worth teaching explicitly; it saves "
           "work later."},

  {"t": "table", "kicker": "Tests", "title": "Three ways to prove convexity",
   "header": ["Test", "Condition", "Use when"],
   "widths": [2.6, 4.4, 5.1],
   "rows": [
     ["<b>Zeroth order</b>", "<b>The definition, directly</b>", "<b>Small cases; non-differentiable f</b>"],
     ["<b>First order</b>", "<b>f(y) ≥ f(x) + ∇f(x)ᵀ(y−x)</b>", "<b>The tangent underestimates everywhere</b>"],
     ["<b>Second order</b>", "<b>∇&#178;f ⪰ 0 (positive semidefinite)</b>", "<b>Twice differentiable f. The usual test</b>"],
     ["<b>By construction</b>", "<b>Built from convex pieces by preserving operations</b>", "<b>Almost always the practical route</b>"],
   ],
   "footnote": "<b>The first-order condition is the important one "
               "conceptually</b> — it says the tangent is a global "
               "underestimator, which is where duality comes from.",
   "note": "Flag that the first-order condition seeds Module 04."},

  {"t": "section", "label": "Part 2", "title": "The calculus",
   "blurb": "Building convex things from convex things."},

  {"t": "code", "kicker": "Preservation", "title": "Operations that preserve convexity",
   "lang": "text", "code": """
  THESE PRESERVE CONVEXITY:
      non-negative weighted sum     sum of a_i f_i,  a_i >= 0
      affine composition            f(Ax + b)
      POINTWISE MAXIMUM             max(f_1, ..., f_k)
          -- even of infinitely many. Hugely useful.
      partial minimisation          inf over y of f(x,y), jointly convex
      perspective                   t * f(x/t)  for t > 0
      composition                   h(g(x)) if h convex AND
                                    NON-DECREASING, g convex

  THESE DO NOT:
      pointwise MINIMUM             min(f_1, f_2)  -- generally not
      product                       f * g          -- generally not
      difference                    f - g          -- generally not

  THE COMPOSITION RULE IS WHERE MISTAKES HAPPEN.
      exp(convex)          convex   -- exp is convex, increasing
      log(concave)         concave  -- log is concave, increasing
      sqrt(convex)         NOT      -- sqrt is increasing but CONCAVE
      (convex)^2           NOT      -- unless the inner f >= 0

  Build convexity up from known pieces. Proving it from the
  definition is almost never necessary and almost never done.
""",
   "caption": "<b>Pointwise maximum preserving convexity is the single "
              "most useful rule</b> — it is why a maximum of linear "
              "functions is convex, which underlies a great deal.",
   "note": "The sqrt counterexample catches people reliably."},

  {"t": "callout", "title": "Disciplined convex programming automates this",
   "kind": "Why CVXPY refuses things",
   "body": ["<b>CVXPY will not accept an expression it cannot verify is "
            "convex</b> by applying the rules above to a library of known "
            "atoms.",
            "<b>So <code>sqrt(x**2 + 1)</code> is accepted</b> — it "
            "recognises the norm — <b>while an equivalent expression "
            "written differently may be rejected.</b>",
            "<b>That is frustrating and it is the point:</b> if the "
            "modelling language cannot verify convexity, neither can the "
            "solver, and the guarantee is gone.",
            "<b>Learning to write a problem in a form DCP accepts is "
            "learning the convexity calculus</b>, enforced. <b>It is the "
            "fastest way to internalise Part 2.</b>"]},

  {"t": "section", "label": "Part 3", "title": "The standard functions",
   "blurb": "The vocabulary you will build everything from."},

  {"t": "table", "kicker": "Atoms", "title": "Convex functions worth knowing by sight",
   "header": ["Function", "Convex?", "Note"],
   "widths": [3.0, 2.6, 6.5],
   "rows": [
     ["<b>Any norm</b>", "<b>Convex</b>", "<b>By the triangle inequality. ℓ1 gives sparsity (CSCE 633 M04)</b>"],
     ["<b>xᵀPx, P ⪰ 0</b>", "Convex", "<b>Quadratic forms; least squares is one</b>"],
     ["<b>exp(ax), x log x</b>", "Convex", "Entropy is −x log x, which is concave"],
     ["<b>log-sum-exp</b>", "<b>Convex</b>", "<b>A smooth max; softmax's normaliser</b>"],
     ["<b>max of affine</b>", "<b>Convex</b>", "<b>Hinge loss is one (CSCE 633 M07)</b>"],
     ["<b>log det X, X ≻ 0</b>", "<b>Concave</b>", "Appears throughout SDP"],
     ["Indicator of a convex set", "Convex", "<b>How constraints become part of the objective</b>"],
   ],
   "footnote": "<b>Most losses you have used are on this list</b> "
               "— squared error, hinge, logistic, and all the norms.",
   "note": "Connecting back to the loss functions they already know is "
           "the point of this table."},

  {"t": "section", "label": "Part 4", "title": "Why it matters",
   "blurb": "The consequences, collected."},

  {"t": "bullets", "kicker": "Consequences", "title": "What convexity buys",
   "items": [
     "<b>Local minimum = global minimum.</b> The reason local methods "
     "work at all (Module 01 §3).",
     "",
     "<b>The tangent is a global underestimator</b>, which gives you "
     "lower bounds for free — and bounds are certificates.",
     "",
     "<b>Strong duality holds</b> under mild conditions (Module 04), "
     "so the dual certifies optimality.",
     "",
     "<b>Convergence rates are provable</b>, and they depend on "
     "conditioning rather than on luck (Module 05).",
     "",
     "<b>And the feasible set is connected</b>, so you can move between "
     "any two feasible points without leaving the set.",
   ],
   "footnote": "<b>Every guarantee in this course descends from the first "
               "bullet</b>, and the second is where duality comes from."},

  {"t": "callout", "title": "When it is not convex, convexify",
   "kind": "The standard move",
   "body": ["<b>Change variables.</b> Geometric programs become convex "
            "under a log substitution — a large class of engineering "
            "problems.",
            "<b>Relax.</b> Replace an integer constraint by its interval, "
            "or a rank constraint by a nuclear norm (Modules 09 "
            "and 10).",
            "<b>Restrict.</b> Optimise over a convex subset you can "
            "handle, accepting a possibly worse answer with a guarantee.",
            "<b>Or accept local optimality and say so</b> — which is "
            "CSCE 636's entire position, and is legitimate when stated "
            "rather than assumed."]},
 ],
 "takeaways": [
   "A set is convex if it contains every segment between its points, and a "
   "function is convex if its epigraph is a convex set — one "
   "definition, two forms.",
   "The first-order condition says the tangent is a global underestimator, "
   "which is where duality and all the bounds come from.",
   "Convexity is established by construction from known pieces far more "
   "often than from the definition.",
   "Pointwise maximum preserves convexity and pointwise minimum does not, "
   "which is the most useful asymmetry in the calculus.",
   "The composition rule needs the outer function to be both convex and "
   "non-decreasing — sqrt of a convex function is not convex.",
   "Disciplined convex programming enforces the calculus, which is the "
   "fastest way to learn it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The definitions"),
  ("eq", "C convex &hArr; &theta;x + (1&minus;&theta;)y &isin; C "
         "&nbsp;&nbsp;&nbsp; f convex &hArr; f(&theta;x + "
         "(1&minus;&theta;)y) &le; &theta;f(x) + (1&minus;&theta;)f(y)"),
  ("p", "A set is convex when the entire segment joining any two of its "
        "points lies inside it. A function is convex when the chord between "
        "any two points on its graph lies above the function. <b>And the "
        "two are the same definition:</b> f is convex exactly when its "
        "<b>epigraph</b> — the set of points lying on or above its "
        "graph, {(x,t) : f(x) &le; t} — is a convex set. <b>The "
        "epigraph formulation unifies them and makes several later results "
        "immediate rather than separate</b>, which is why it is worth "
        "carrying rather than treating the two definitions as a "
        "coincidence."),
  ("table", ["Test", "Condition", "Use when"],
   [["<b>Zeroth order</b>", "<b>The definition, applied directly.</b>",
     "<b>Small cases, and functions that are not differentiable</b> "
     "— where the other tests do not apply."],
    ["<b>First order</b>",
     "<b>f(y) &ge; f(x) + &nabla;f(x)<super>T</super>(y &minus; x) for all "
     "x, y.</b>",
     "<b>The tangent plane at any point lies below the function "
     "everywhere.</b> <b>Conceptually the most important of the three</b> "
     "— a global underestimator from purely local information, which "
     "is exactly what Module 01 &sect;3 said was otherwise impossible, and "
     "is where duality originates."],
    ["<b>Second order</b>",
     "<b>The Hessian &nabla;&#178;f is positive semidefinite "
     "everywhere.</b>",
     "<b>Twice-differentiable functions, and the usual working test.</b> "
     "Checking positive semidefiniteness is itself work in high "
     "dimensions."],
    ["<b>By construction</b>",
     "<b>Built from known convex pieces using operations that preserve "
     "convexity.</b>",
     "<b>Almost always the practical route</b> — &sect;2. Proving "
     "convexity from the definition is rare in practice."]],
   [0.17, 0.35, 0.48]),

  ("h1", "2 &nbsp; The convexity calculus"),
  ("code", """PRESERVE CONVEXITY
  non-negative weighted sum    sum a_i f_i,  a_i >= 0
  affine composition           f(Ax + b)
  POINTWISE MAXIMUM            max(f_1, ..., f_k)
      -- even of INFINITELY many. The most useful rule here.
  partial minimisation         inf_y f(x,y), f jointly convex
  perspective                  t * f(x/t),  t > 0
  composition                  h(g(x)) if h convex AND NON-DECREASING

DO NOT PRESERVE IT
  pointwise MINIMUM            min(f_1, f_2)
  product                      f * g
  difference                   f - g

THE COMPOSITION RULE IS WHERE MISTAKES HAPPEN
  exp(convex)     convex    -- exp is convex and increasing
  log(concave)    concave   -- log is concave and increasing
  sqrt(convex)    NOT       -- sqrt is increasing but CONCAVE
  (convex)^2      NOT       -- unless the inner f is >= 0"""),
  ("p", "<b>That pointwise maximum preserves convexity while pointwise "
        "minimum does not is the most useful asymmetry in the "
        "calculus.</b> It is why a maximum of affine functions is convex "
        "— which makes hinge loss convex, makes the dual function "
        "concave (Module 04), and underlies piecewise-linear modelling "
        "generally. <b>And it is why 'the best of several options' is "
        "usually <i>not</i> convex</b>, which is the formal reason "
        "discrete choice makes problems hard."),
  ("callout", "Disciplined convex programming automates this",
   ["<b>CVXPY and its relatives refuse any expression they cannot verify "
    "is convex</b>, by applying the rules of &sect;2 mechanically to a "
    "library of known atoms with known curvature and monotonicity.",
    "<b>So <code>cp.sqrt(cp.sum_squares(x) + 1)</code> may be rejected "
    "while <code>cp.norm(cp.hstack([x, 1]))</code> is accepted</b>, even "
    "though they are mathematically identical — the second is "
    "recognisably a norm and the first is a square root of a convex "
    "function, which the rules correctly decline to certify.",
    "<b>That is frustrating the first time and it is exactly the "
    "point.</b> <b>If the modelling language cannot verify convexity, "
    "neither can the solver</b>, and the polynomial-time guarantee the "
    "solver offers is contingent on the problem actually being convex. A "
    "solver handed a non-convex problem returns a number with no "
    "warranty.",
    "<b>Learning to write a problem in a form DCP accepts is learning the "
    "convexity calculus, enforced by a compiler.</b> <b>It is the fastest "
    "way to internalise &sect;2</b>, and it is a rare case of a tool "
    "teaching the theory as a side effect of being strict."]),

  ("break",),
  ("h1", "3 &nbsp; The standard atoms"),
  ("table", ["Function", "Curvature", "Note"],
   [["<b>Any norm &#8214;x&#8214;</b>", "<b>Convex</b>",
     "<b>Directly from the triangle inequality and homogeneity.</b> "
     "&ell;<sub>1</sub> gives sparsity, &ell;<sub>2</sub> gives shrinkage "
     "(CSCE 633 Module 04 &sect;1) — <b>and the geometric argument "
     "there is this convexity, seen as a constraint set.</b>"],
    ["<b>x<super>T</super>Px with P positive semidefinite</b>", "Convex",
     "<b>Quadratic forms.</b> Least squares is one; so is the SVM's "
     "objective."],
    ["<b>exp(ax), x log x</b>", "Convex",
     "And <b>entropy &minus;&Sigma;p log p is concave</b>, which is why "
     "maximum-entropy problems are tractable."],
    ["<b>log-sum-exp</b>", "<b>Convex</b>",
     "<b>A smooth approximation to the maximum</b>, and the normalising "
     "term of the softmax (CSCE 633 Module 02 &sect;3) — so "
     "cross-entropy's convexity in the logits comes from here."],
    ["<b>max of affine functions</b>", "<b>Convex</b>",
     "<b>Hinge loss is exactly this</b> (CSCE 633 Module 07), which is "
     "why the SVM is a convex problem."],
    ["<b>log det X over positive definite X</b>", "<b>Concave</b>",
     "Appears throughout semidefinite programming and in "
     "maximum-likelihood covariance estimation."],
    ["<b>Indicator of a convex set</b>", "Convex",
     "<b>Zero inside, +&infin; outside.</b> <b>This is how constraints "
     "are folded into an objective</b>, which unifies constrained and "
     "unconstrained formulations."]],
   [0.21, 0.17, 0.62]),
  ("p", "<b>Most of the losses used in the previous two courses are on "
        "this list</b> — squared error, hinge, logistic, and every "
        "norm-based regulariser. <b>Which retroactively explains why those "
        "problems were well behaved</b>, and why neural networks "
        "(CSCE 636), which compose these atoms non-monotonically through "
        "many layers, are not."),

  ("h1", "4 &nbsp; What convexity buys"),
  ("ul", ["<b>Every local minimum is a global minimum.</b> <b>The reason "
          "local methods work at all</b> (Module 01 &sect;3), and the "
          "root of every other item on this list.",
          "<b>The tangent is a global underestimator</b> (the first-order "
          "condition), <b>so lower bounds come for free</b> — and a "
          "bound is a certificate. This is where Module 04's duality "
          "originates and why a dual solution <i>proves</i> optimality "
          "rather than merely suggesting it.",
          "<b>Strong duality holds under mild regularity conditions</b> "
          "(Module 04 &sect;2), so the primal and dual optimal values "
          "coincide and either certifies the other.",
          "<b>Convergence rates are provable</b>, and they depend on "
          "measurable properties of the problem — the condition number "
          "— rather than on the starting point or on luck "
          "(Module 05).",
          "<b>And the feasible set is connected</b>, so any feasible point "
          "can be reached from any other without leaving the set, which is "
          "what makes interior point methods (Module 07) possible at all."]),
  ("callout", "When it is not convex, convexify",
   ["<b>Change variables.</b> <b>Geometric programs — which look "
    "thoroughly non-convex — become convex under a logarithmic "
    "substitution</b>, and that single transformation covers a large class "
    "of engineering design problems in circuits, structures, and chemical "
    "processes. <b>Looking for a change of variables is the first thing to "
    "try</b> and is frequently forgotten.",
    "<b>Relax.</b> Replace an integer constraint x &isin; {0,1} with the "
    "interval 0 &le; x &le; 1 (Module 09), or a rank constraint with a "
    "nuclear norm (Module 10). <b>The relaxation is convex, its optimum "
    "bounds the true one, and the gap is measurable.</b>",
    "<b>Restrict.</b> Optimise over a convex subset of the feasible "
    "region — accepting a possibly worse answer in exchange for a "
    "guarantee about it, which is frequently the better trade.",
    "<b>Or accept local optimality and say so.</b> <b>That is CSCE 636's "
    "entire position</b>, and it is a perfectly legitimate engineering "
    "stance <b>when it is stated rather than assumed</b> — the "
    "failure is claiming a global optimum from a local method, not using "
    "one."]),
 ],
 "resources": [
   ("Boyd & Vandenberghe &mdash; Convex Optimization, chapters 2 and 3 "
    "(free)",
    "https://web.stanford.edu/~boyd/cvxbook/",
    "<b>The definitive treatment of &sect;1 through &sect;3</b>, including "
    "the full atom library and every preservation rule with proof."),
   ("Grant, Boyd & Ye &mdash; Disciplined Convex Programming (free)",
    "https://web.stanford.edu/~boyd/papers/disc_cvx_prog.html",
    "<b>The &sect;2 callout's ruleset</b>, stated formally — which "
    "explains exactly why CVXPY rejects what it rejects."),
   ("CVXPY &mdash; the atomic function library and DCP tutorial (free)",
    "https://www.cvxpy.org/tutorial/dcp/",
    "The atoms of &sect;3 with their curvature and monotonicity, "
    "machine-readable and worth browsing."),
   ("Boyd &mdash; EE364A lectures 2 and 3 (free video)",
    "https://www.youtube.com/playlist?list=PL3940DD956CDF0622",
    "The same material lectured, with the geometric intuition that the "
    "book states more tersely."),
 ],
 "exercises": [
   "<b>Prove three functions convex by three different tests</b> "
   "— definition, first order, second order.",
   "<b>Show that sqrt of a convex function need not be convex</b> with an "
   "explicit counterexample.",
   "Show the pointwise maximum of two convex functions is convex, and "
   "that the minimum need not be.",
   "<b>Prove that every norm is convex</b> from the triangle inequality.",
   "Verify that log-sum-exp is convex by computing its Hessian.",
   "<b>Write ten expressions in CVXPY</b>, five it accepts and five it "
   "rejects, and explain each rejection.",
   "<b>Rewrite a rejected expression</b> into an equivalent accepted one.",
   "Take three loss functions from CSCE 633 and classify each as convex or "
   "not.",
   "<b>Convert a geometric program to convex form</b> by logarithmic "
   "change of variables.",
   "Take a non-convex problem you care about and apply each of &sect;4's "
   "four moves.",
 ],
 "selfcheck": [
   "Define convex sets and convex functions, and relate them via the "
   "epigraph.",
   "Give three tests for convexity and say when each applies.",
   "Why is the first-order condition conceptually important?",
   "Name six operations that preserve convexity and three that do not.",
   "State the composition rule and give a case where it fails.",
   "Why is pointwise maximum convex and pointwise minimum not?",
   "Name seven standard convex atoms.",
   "Give five consequences of convexity.",
   "Give four ways to handle a non-convex problem.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Linear Programming",
 "subtitle": "The most useful special case.",
 "question": "What can you do when everything is linear?",
 "outcomes": [
     "Put a problem into standard form.",
     "Explain the geometry — polyhedra, vertices, and why the "
     "optimum is at one.",
     "Explain the simplex method and its complexity paradox.",
     "Model with linear programs, including the standard tricks.",
     "Recognise when a problem is secretly linear.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The geometry",
   "blurb": "Why the answer is at a corner."},

  {"t": "callout", "title": "The optimum of a linear program is at a vertex",
   "kind": "The fact that makes everything work",
   "body": ["<b>The feasible set of a linear program is a "
            "<i>polyhedron</i></b> — an intersection of half-spaces, "
            "which is convex by construction (Module 02 §2).",
            "<b>A linear objective has a constant gradient</b>, so there "
            "is no interior stationary point — moving in the improving "
            "direction always improves, until a constraint stops you.",
            "<b>So an optimum, if one exists, occurs at a vertex</b> of "
            "the polyhedron. (Or along an edge or face, in which case a "
            "vertex attains it too.)",
            "<b>That reduces a continuous problem to a finite one:</b> "
            "search the vertices. <b>There are exponentially many</b>, "
            "which is why you need an intelligent search rather than "
            "enumeration."]},

  {"t": "code", "kicker": "Standard form", "title": "Getting any LP into one shape",
   "lang": "text", "code": """
  STANDARD FORM:   minimise c'x   subject to  Ax = b,  x >= 0

  ANY linear program converts into it:

    maximise c'x          ->  minimise -c'x
    a'x <= b              ->  a'x + s = b,  s >= 0    (slack)
    a'x >= b              ->  a'x - s = b,  s >= 0    (surplus)
    x unrestricted        ->  x = x+ - x-,  x+,x- >= 0
    |x| in the objective  ->  x = x+ - x-, minimise x+ + x-
                              (works only when MINIMISING |x|)

  THE LAST ONE IS THE MOST USEFUL TRICK HERE.
      It is how L1 regression, L1 regularisation, and robust
      fitting become linear programs -- and it is why the lasso
      (CSCE 633 M04) has an LP formulation at all.

  IT ALSO SHOWS THE LIMIT: minimising |x| is fine; MAXIMISING
  |x| is not, because max of |x| is not concave. The direction
  of the optimisation decides whether a trick is legal.
""",
   "caption": "<b>The absolute-value trick only works in one "
              "direction</b>, which is Module 02's convexity calculus "
              "showing up as a modelling constraint.",
   "note": "That the trick is directional is the instructive part."},

  {"t": "section", "label": "Part 2", "title": "Simplex",
   "blurb": "Walk the vertices, improving."},

  {"t": "callout", "title": "Simplex walks edges from vertex to vertex",
   "kind": "The algorithm",
   "body": ["<b>Start at a feasible vertex.</b> Look at the adjacent "
            "vertices; move to one that improves the objective; repeat "
            "until none does.",
            "<b>Convexity guarantees that a vertex with no improving "
            "neighbour is globally optimal</b> (Module 02 §4) — "
            "so the local stopping test is a global certificate.",
            "<b>Degeneracy can stall it:</b> several bases describing the "
            "same vertex, so a pivot changes nothing. <b>Bland's rule "
            "prevents cycling at the cost of speed.</b>",
            "<b>And the pivoting rule is the whole engineering.</b> "
            "Which improving neighbour to choose determines the path "
            "length, and no rule is known to be polynomial."]},

  {"t": "callout", "title": "Simplex is exponential in theory and excellent in practice",
   "kind": "The paradox worth understanding",
   "body": ["<b>Klee and Minty constructed a polytope on which simplex "
            "visits every one of its 2ⁿ vertices.</b> So the worst "
            "case is exponential for the standard pivoting rules.",
            "<b>On real problems it takes a number of pivots roughly "
            "linear in the number of constraints.</b> The gap between "
            "worst case and typical is enormous.",
            "<b>Smoothed analysis explains it:</b> on any instance "
            "perturbed slightly, simplex runs in expected polynomial time "
            "— so the bad instances are isolated and fragile.",
            "<b>This is the clearest example in the program of worst-case "
            "complexity failing to describe practice</b> (Module 01 "
            "§2), and smoothed analysis was invented to close exactly "
            "this gap."]},

  {"t": "section", "label": "Part 3", "title": "Modelling",
   "blurb": "The useful formulations."},

  {"t": "table", "kicker": "Models", "title": "Problems that are linear programs",
   "header": ["Problem", "Formulation", "Note"],
   "widths": [2.9, 4.3, 4.9],
   "rows": [
     ["<b>Diet / blending</b>", "Minimise cost subject to requirements", "<b>The original application, 1940s</b>"],
     ["<b>Transportation</b>", "<b>Ship from supplies to demands</b>", "<b>Integral optimum automatically</b>"],
     ["<b>Max flow</b>", "Flow conservation plus capacities", "<b>LP whose optimum is integral (CSCE 629)</b>"],
     ["<b>Shortest path</b>", "<b>The dual of a flow problem</b>", "Also integral"],
     ["<b>L₁ regression</b>", "<b>Split residuals into ± parts</b>", "<b>Robust to outliers; not least squares</b>"],
     ["<b>Chebyshev fitting</b>", "Minimise t s.t. |rᵢ| ≤ t", "<b>Minimax; one variable and 2m constraints</b>"],
     ["Game theory", "Minimax over mixed strategies", "<b>Von Neumann; the dual is the opponent</b>"],
   ],
   "footnote": "<b>Several of these have integral optima "
               "automatically</b>, which is why they are easy when general "
               "integer programs are not (Module 11).",
   "note": "Total unimodularity is the reason, and it is worth naming."},

  {"t": "callout", "title": "Why flow and matching are easy",
   "kind": "The structural reason",
   "body": ["<b>Their constraint matrices are <i>totally "
            "unimodular</i></b> — every square submatrix has determinant "
            "0, +1, or −1.",
            "<b>When that holds and the right-hand side is integral, every "
            "vertex of the polyhedron is integral.</b>",
            "<b>So solving the LP relaxation gives an integer "
            "answer</b> — the integrality constraint is free, and the "
            "NP-hardness of integer programming simply does not bite.",
            "<b>That is the precise reason max flow, bipartite matching, "
            "and shortest path are polynomial while the travelling "
            "salesman is not</b> — not a difference of effort but of "
            "matrix structure."]},

  {"t": "section", "label": "Part 4", "title": "In practice",
   "blurb": "What solvers actually do."},

  {"t": "bullets", "kicker": "Practice", "title": "Using a linear programming solver",
   "items": [
     "<b>Use a solver.</b> HiGHS is free and excellent; Gurobi and "
     "CPLEX are faster on hard instances and have academic licences.",
     "",
     "<b>Solvers use both simplex and interior point</b> (Module 07) "
     "and pick per instance — and <b>only simplex gives a warm "
     "start</b>, which matters when resolving.",
     "",
     "<b>Presolve matters enormously</b> — removing redundant "
     "constraints and fixing variables frequently shrinks a problem by "
     "half before any iteration.",
     "",
     "<b>Numerical conditioning is real</b> — coefficients spanning "
     "many orders of magnitude cause genuine failures.",
     "",
     "<b>And scale your model.</b> Keeping coefficients within a few "
     "orders of magnitude is the cheapest robustness fix available.",
   ],
   "footnote": "<b>Scaling is CSCE 633 Module 02's feature scaling, "
               "arriving as a numerical rather than an optimisation "
               "concern.</b>"},
 ],
 "takeaways": [
   "A linear program's feasible set is a polyhedron and its objective has "
   "constant gradient, so an optimum occurs at a vertex.",
   "That reduces a continuous problem to a finite one — with "
   "exponentially many vertices, so intelligent search is required.",
   "The absolute-value trick works when minimising and not when "
   "maximising, which is the convexity calculus appearing as a modelling "
   "constraint.",
   "Simplex is exponential on Klee–Minty constructions and roughly "
   "linear in constraints on real problems; smoothed analysis explains the "
   "gap.",
   "Totally unimodular constraint matrices give integral vertices, which is "
   "precisely why flow and matching are easy.",
   "Model scaling is the cheapest robustness fix, and it is CSCE 633's "
   "feature scaling arriving as a numerical concern.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The geometry"),
  ("callout", "The optimum is at a vertex",
   ["<b>The feasible set of a linear program is a polyhedron</b> — an "
    "intersection of finitely many half-spaces — and an intersection "
    "of convex sets is convex (Module 02 &sect;2), so the feasible region "
    "is convex by construction.",
    "<b>A linear objective has a constant gradient</b>, so there is no "
    "interior point where the gradient vanishes. Moving in the improving "
    "direction always improves, <b>until a constraint stops you.</b>",
    "<b>So an optimum, where one exists, is attained at a vertex</b> of "
    "the polyhedron. (The optimal face may be an edge or a higher-"
    "dimensional face, in which case its vertices attain the optimum too, "
    "so looking only at vertices loses nothing.)",
    "<b>That reduces a continuous optimisation over infinitely many points "
    "to a finite search over vertices</b> — which is the key "
    "structural fact. <b>There are exponentially many vertices</b>, so "
    "enumeration is not available and an intelligent walk is required "
    "(&sect;2)."]),
  ("code", """STANDARD FORM:  minimise c'x  subject to  Ax = b,  x >= 0

ANY linear program converts:
  maximise c'x         ->  minimise -c'x
  a'x <= b             ->  a'x + s = b,  s >= 0   (slack)
  a'x >= b             ->  a'x - s = b,  s >= 0   (surplus)
  x unrestricted       ->  x = x+ - x-,  both >= 0
  |x| in the objective ->  x = x+ - x-, minimise x+ + x-
                           -- ONLY when MINIMISING |x|

THE LAST IS THE MOST USEFUL TRICK HERE. It is how L1 regression,
L1 regularisation and robust fitting become linear programs --
and why the lasso (CSCE 633 M04) has an LP formulation.

IT ALSO SHOWS THE LIMIT: minimising |x| is fine; MAXIMISING |x|
is not, because |x| is convex and max of a convex function is
not a concave problem. The DIRECTION decides legality."""),
  ("p", "<b>That the absolute-value trick is directional is the "
        "instructive part</b> — it is Module 02's convexity calculus "
        "reappearing as a hard modelling constraint rather than as "
        "theory. <b>Whenever a reformulation seems too convenient, check "
        "which direction it works in</b>, and the answer is usually that "
        "it works in the convex direction only."),

  ("h1", "2 &nbsp; The simplex method"),
  ("callout", "Simplex walks edges from vertex to vertex",
   ["<b>Start at a feasible vertex.</b> Examine the adjacent vertices "
    "along the edges of the polyhedron; move to one that improves the "
    "objective; repeat until no neighbour improves.",
    "<b>Convexity guarantees that a vertex with no improving neighbour is "
    "globally optimal</b> (Module 02 &sect;4) — <b>so a purely local "
    "stopping test constitutes a global certificate.</b> That is the "
    "property doing all the work, and without it the walk would prove "
    "nothing.",
    "<b>Degeneracy can stall it.</b> Several different bases can describe "
    "the same geometric vertex, so a pivot changes the algebra without "
    "moving — and in principle the algorithm can cycle forever "
    "between them. <b>Bland's rule guarantees termination</b> by imposing "
    "a deterministic tie-break, <b>at a real cost in speed</b>, so "
    "implementations use faster rules and fall back to Bland's only when "
    "stalling is detected.",
    "<b>And the pivoting rule is where the engineering is.</b> Which "
    "improving neighbour to move to determines the path length, and "
    "<b>no pivoting rule is known to be polynomial</b> — a question "
    "open since the 1950s, and related to the Hirsch conjecture on "
    "polytope diameters, which was disproved in 2010."]),
  ("callout", "Exponential in theory, excellent in practice",
   ["<b>Klee and Minty constructed a deformed hypercube on which the "
    "standard pivoting rule visits every one of its 2<super>n</super> "
    "vertices.</b> So the worst case is exponential, provably, for Dantzig's "
    "rule and for most others.",
    "<b>On real problems simplex takes a number of pivots roughly linear "
    "in the number of constraints</b> — typically two to three times "
    "m. <b>The gap between worst case and typical behaviour is enormous</b> "
    "and was an embarrassment to complexity theory for decades.",
    "<b>Smoothed analysis explains it.</b> Spielman and Teng showed that "
    "for <i>any</i> instance, a small random perturbation of its data makes "
    "simplex run in expected polynomial time — <b>so the bad "
    "instances are isolated and fragile</b>, destroyed by arbitrarily small "
    "noise, which is why they do not arise from measured data.",
    "<b>This is the clearest example in the whole program of worst-case "
    "complexity failing to describe practice</b> (Module 01 &sect;2), "
    "<b>and smoothed analysis was invented specifically to close this "
    "gap</b> — a case where the theory was extended to match a "
    "stubborn empirical fact rather than the other way round."]),

  ("break",),
  ("h1", "3 &nbsp; Modelling with linear programs"),
  ("table", ["Problem", "Formulation", "Note"],
   [["<b>Diet and blending</b>",
     "Minimise cost subject to meeting nutritional or compositional "
     "requirements.",
     "<b>The original application</b>, from the 1940s, and still the "
     "standard teaching example."],
    ["<b>Transportation and assignment</b>",
     "<b>Ship goods from supply nodes to demand nodes at minimum cost.</b>",
     "<b>The optimum is automatically integral</b> — see the callout."],
    ["<b>Maximum flow</b>",
     "Flow conservation at each node, capacity on each edge.",
     "<b>A linear program whose optimum is integral</b> (CSCE 629), which "
     "is why the combinatorial algorithms work."],
    ["<b>Shortest path</b>", "<b>The dual of a unit flow problem.</b>",
     "Also integral; the dual variables are the distance labels, which is "
     "Module 04's interpretation arriving concretely."],
    ["<b>&ell;<sub>1</sub> regression</b>",
     "<b>Split each residual into positive and negative parts</b> and "
     "minimise their sum.",
     "<b>Robust to outliers in a way least squares is not</b> "
     "(CSCE 633 Module 01 &sect;3) — and it is an LP, not a "
     "least-squares problem."],
    ["<b>Chebyshev (minimax) fitting</b>",
     "minimise t subject to |r<sub>i</sub>| &le; t for every i.",
     "<b>One extra variable and 2m constraints</b> turns a minimax problem "
     "into an LP — a trick worth remembering."],
    ["<b>Two-player zero-sum games</b>",
     "Minimax over mixed strategies.",
     "<b>Von Neumann's theorem is LP duality</b>, and the dual program is "
     "the opponent's problem (Module 04)."]],
   [0.20, 0.38, 0.42]),
  ("callout", "Why flow and matching are easy",
   ["<b>Their constraint matrices are <i>totally unimodular</i></b> "
    "— every square submatrix has determinant 0, +1, or &minus;1. "
    "Node-arc incidence matrices of directed graphs have this property, as "
    "do the constraint matrices of bipartite matching.",
    "<b>When a constraint matrix is totally unimodular and the right-hand "
    "side is integral, every vertex of the polyhedron has integer "
    "coordinates.</b> This follows from Cramer's rule: the vertex "
    "coordinates are ratios of determinants, and the denominators are "
    "&plusmn;1.",
    "<b>So solving the linear programming relaxation returns an integer "
    "answer with no rounding and no branching</b> — the integrality "
    "constraint is satisfied for free, and the NP-hardness of integer "
    "programming (Module 09) simply does not apply.",
    "<b>That is the precise reason maximum flow, bipartite matching, and "
    "shortest path are polynomial while the travelling salesman problem is "
    "not.</b> <b>It is a difference of matrix structure, not of "
    "effort</b> — and recognising total unimodularity in a "
    "formulation is one of the most valuable skills in this subject, "
    "because it converts a hard problem into an easy one at a stroke."]),

  ("h1", "4 &nbsp; In practice"),
  ("ul", ["<b>Use a solver.</b> <b>HiGHS is free, open source, and "
          "excellent</b>; Gurobi and CPLEX are substantially faster on hard "
          "instances and have free academic licences. Writing your own is "
          "for understanding, not for use.",
          "<b>Solvers implement both simplex and interior point methods</b> "
          "(Module 07) and select between them per instance — "
          "<b>and only simplex supports a warm start</b>, which matters "
          "enormously when re-solving a slightly modified problem, as "
          "branch and bound does thousands of times (Module 09).",
          "<b>Presolve matters enormously.</b> Removing redundant "
          "constraints, fixing variables whose values are forced, and "
          "tightening bounds frequently halves a problem before a single "
          "iteration runs — and on badly-written models it does far "
          "more than that.",
          "<b>Numerical conditioning is a real and frequent source of "
          "failure.</b> Coefficients spanning many orders of magnitude "
          "produce genuinely wrong answers, infeasibility reports on "
          "feasible problems, and non-reproducible results — which is "
          "CSCE 620 Module 01's lesson in another domain.",
          "<b>So scale your model.</b> <b>Keeping all coefficients within "
          "a few orders of magnitude is the cheapest robustness improvement "
          "available</b>, and it is <b>CSCE 633 Module 02's feature "
          "scaling arriving as a numerical concern rather than an "
          "optimisation one</b> — the same fix, for a related "
          "reason."]),
 ],
 "resources": [
   ("MIT 15.093 &mdash; linear programming lectures (free, OCW)",
    "https://ocw.mit.edu/courses/15-093j-optimization-methods-fall-2009/",
    "<b>The reference for &sect;1 through &sect;3</b>, including the "
    "geometry and the simplex development."),
   ("Spielman & Teng &mdash; Smoothed Analysis of Algorithms (free)",
    "https://arxiv.org/abs/cs/0111050",
    "<b>The &sect;2 resolution.</b> Read the introduction for the argument "
    "even if the analysis is heavy."),
   ("Schrijver &mdash; Theory of Linear and Integer Programming",
    "https://www.wiley.com/en-us/Theory+of+Linear+and+Integer+Programming-p-9780471982326",
    "The reference for total unimodularity (&sect;3) and the polyhedral "
    "theory. Library copy."),
   ("HiGHS, and the CVXPY linear programming examples (free)",
    "https://highs.dev/",
    "A free solver that is genuinely competitive, with documentation on "
    "the &sect;4 practical concerns."),
 ],
 "exercises": [
   "<b>Convert three linear programs to standard form</b>, including one "
   "with an absolute value and one with unrestricted variables.",
   "<b>Show the absolute-value trick fails when maximising</b>, with a "
   "concrete instance.",
   "Implement simplex for small problems and verify against a solver.",
   "<b>Construct the Klee–Minty cube</b> for n = 4 and count the "
   "pivots your implementation takes.",
   "<b>Measure pivot count against constraint count</b> on random "
   "instances and plot it.",
   "Formulate and solve a transportation problem. <b>Verify the optimum is "
   "integral without being asked to be.</b>",
   "<b>Formulate L&#8321; regression as an LP</b> and compare its fit "
   "against least squares on data with outliers.",
   "Formulate Chebyshev fitting and compare against both.",
   "<b>Verify total unimodularity</b> of a small node-arc incidence matrix "
   "by checking submatrix determinants.",
   "<b>Scale a badly-conditioned model</b> and show the solver's behaviour "
   "changes.",
 ],
 "selfcheck": [
   "Why is a linear program's optimum at a vertex?",
   "Convert a general LP to standard form, naming each transformation.",
   "Why does the absolute-value trick only work in one direction?",
   "Describe simplex and say what convexity contributes.",
   "What is degeneracy and how is cycling prevented?",
   "State the simplex complexity paradox and its resolution.",
   "Name seven problems that are linear programs.",
   "What is total unimodularity and what does it buy?",
   "Give five practical concerns when using an LP solver.",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Duality",
 "subtitle": "Every minimisation has a shadow maximisation.",
 "question": "What is the dual, and what is it telling you?",
 "outcomes": [
     "Construct the Lagrangian and the dual function.",
     "State weak and strong duality and the conditions for each.",
     "Interpret dual variables as shadow prices.",
     "Apply complementary slackness.",
     "Use the dual as a certificate of optimality.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Constructing it",
   "blurb": "Move the constraints into the objective."},

  {"t": "eq", "kicker": "Construction", "title": "Lagrangian to dual",
   "eqs": [
     ("L(x, λ, ν) = f(x) + Σ λᵢgᵢ(x) + Σ νⱼhⱼ(x)",
      "Price each constraint violation and add it to the objective. λ ≥ 0."),
     ("g(λ, ν) = inf_x L(x, λ, ν)",
      "The dual function. An infimum of affine functions of (λ,ν), so it "
      "is CONCAVE — always, even if the primal is not convex."),
     ("maximise g(λ,ν)  subject to  λ ≥ 0",
      "The dual problem. Always a convex problem."),
   ],
   "caption": "<b>The dual is always convex</b>, whatever the primal is "
              "— which is why it is useful even for hard problems.",
   "note": "That concavity-always property is the thing that makes "
           "duality general."},

  {"t": "callout", "title": "Weak duality always holds; strong duality usually does",
   "kind": "The two results",
   "body": ["<b>Weak duality: g(λ,ν) ≤ p* for every "
            "feasible (λ,ν).</b> <b>Always true, for any "
            "problem whatsoever</b> — convex or not.",
            "<b>So any dual feasible point gives a lower bound on the "
            "primal optimum, for free.</b> That is the single most useful "
            "consequence.",
            "<b>Strong duality: the gap is zero.</b> For convex problems "
            "it holds under a mild condition — Slater's: there exists a "
            "strictly feasible point.",
            "<b>So for a convex problem, solving either one solves "
            "both</b>, and a dual solution <i>proves</i> that a primal "
            "solution is optimal. <b>A bound plus a matching feasible "
            "point is a certificate.</b>"]},

  {"t": "section", "label": "Part 2", "title": "What the dual variables mean",
   "blurb": "The interpretation that makes duality useful."},

  {"t": "callout", "title": "Dual variables are prices",
   "kind": "The interpretation to carry",
   "body": ["<b>λᵢ is the rate at which the optimal value "
            "improves if constraint i is relaxed by one unit.</b> "
            "Formally, ∂p*/∂bᵢ = −λᵢ.",
            "<b>So the dual variable prices the constraint.</b> 'An extra "
            "hour of machine time is worth $34' is a dual variable, stated "
            "in the problem's own vocabulary.",
            "<b>A zero dual variable means the constraint is not "
            "binding</b> — relaxing it buys nothing, because you are not "
            "pressed against it.",
            "<b>This is what makes duality practically valuable rather "
            "than formally elegant:</b> <b>it tells the problem owner "
            "where to invest</b>, which the primal solution alone does "
            "not."]},

  {"t": "eq", "kicker": "Complementary slackness", "title": "Either the constraint binds or its price is zero",
   "eqs": [
     ("λᵢ · gᵢ(x*) = 0   for every i",
      "At optimality, for each constraint, at least one of the two is "
      "zero."),
     ("gᵢ(x*) < 0 ⟹ λᵢ = 0",
      "Slack constraint ⟹ zero price. It is not limiting you."),
     ("λᵢ > 0 ⟹ gᵢ(x*) = 0",
      "Positive price ⟹ the constraint is tight. You are pressed "
      "against it."),
   ],
   "caption": "<b>This is the economic statement of the obvious:</b> you "
              "do not pay for something you are not using.",
   "note": "Framing it economically makes it memorable."},

  {"t": "section", "label": "Part 3", "title": "Using it",
   "blurb": "Where duality earns its keep."},

  {"t": "table", "kicker": "Uses", "title": "What duality is actually for",
   "header": ["Use", "How", "Where"],
   "widths": [2.9, 4.3, 4.9],
   "rows": [
     ["<b>Certify optimality</b>", "<b>Matching primal and dual values prove both</b>", "<b>Every solver reports this gap</b>"],
     ["<b>Bound a hard problem</b>", "<b>Any dual feasible point bounds below</b>", "<b>Branch and bound (M09)</b>"],
     ["<b>Sensitivity analysis</b>", "Shadow prices on each constraint", "<b>The main practical payoff</b>"],
     ["<b>Easier problem</b>", "<b>Sometimes the dual is simpler</b>", "<b>SVM: dual enables kernels (CSCE 633 M07)</b>"],
     ["Decomposition", "Split a coupled problem by pricing the coupling", "Large-scale; Dantzig–Wolfe"],
     ["<b>Theory</b>", "<b>Max-flow min-cut; minimax; LP duality</b>", "Several famous theorems are one theorem"],
   ],
   "footnote": "<b>Max-flow min-cut is LP duality</b>, and so is von "
               "Neumann's minimax theorem — which unifies results "
               "that look unrelated.",
   "note": "That unification is genuinely satisfying and worth stating."},

  {"t": "callout", "title": "The SVM dual is why kernels exist",
   "kind": "The connection back",
   "body": ["<b>The SVM primal optimises over the weight vector w</b>, "
            "whose dimension is the number of features.",
            "<b>Its dual optimises over one variable per training "
            "example</b>, and the data enters only through inner products "
            "xᵢᵀxⱼ.",
            "<b>That is exactly what makes the kernel trick "
            "possible</b> (CSCE 633 M07 §2) — you can substitute "
            "a kernel for the inner product only because the dual never "
            "touches the individual vectors.",
            "<b>So kernels are a consequence of taking the dual</b>, not "
            "an independent idea. <b>The representer theorem is the same "
            "observation stated differently.</b>"]},

  {"t": "section", "label": "Part 4", "title": "When it fails",
   "blurb": "Duality gaps."},

  {"t": "callout", "title": "The duality gap is where the difficulty lives",
   "kind": "For non-convex problems",
   "body": ["<b>For non-convex problems, strong duality generally "
            "fails</b> — the dual optimum is strictly below the primal "
            "optimum.",
            "<b>That gap is a measure of the problem's "
            "non-convexity</b>, and it is exactly what makes the problem "
            "hard.",
            "<b>The dual bound is still useful.</b> It gives a valid lower "
            "bound, which is what branch and bound prunes with "
            "(Module 09 §2).",
            "<b>And the integrality gap of Module 10 is this gap</b>, "
            "for the special case of integer programs — <b>so "
            "approximation guarantees are duality gaps with a ratio "
            "attached.</b>"]},
 ],
 "takeaways": [
   "The dual function is an infimum of affine functions, so it is concave "
   "always — the dual is a convex problem even when the primal is not.",
   "Weak duality holds for every problem, so any dual feasible point gives "
   "a free lower bound.",
   "Strong duality holds for convex problems under Slater's condition, so a "
   "dual solution certifies a primal one.",
   "Dual variables are shadow prices — the rate at which the optimum "
   "improves per unit of relaxation — which is duality's main "
   "practical payoff.",
   "Complementary slackness says you do not pay for a constraint you are "
   "not pressed against.",
   "The SVM dual is why kernels exist: the data enters only through inner "
   "products, which is exactly what the kernel trick substitutes into.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Constructing the dual"),
  ("eq", "L(x, &lambda;, &nu;) = f(x) + &Sigma;&lambda;<sub>i</sub>"
         "g<sub>i</sub>(x) + &Sigma;&nu;<sub>j</sub>h<sub>j</sub>(x) "
         "&nbsp;&rarr;&nbsp; g(&lambda;,&nu;) = inf<sub>x</sub> "
         "L(x,&lambda;,&nu;)"),
  ("p", "<b>The Lagrangian prices each constraint violation and adds it to "
        "the objective</b>, with &lambda; &ge; 0 for inequalities and "
        "&nu; unrestricted for equalities. <b>The dual function is the "
        "infimum of the Lagrangian over x</b> — and because it is a "
        "pointwise infimum of functions that are <i>affine</i> in "
        "(&lambda;, &nu;), <b>it is concave, always, regardless of whether "
        "the primal problem was convex</b> (Module 02 &sect;2's "
        "preservation rules, applied to the minimum of affine functions). "
        "<b>So the dual problem — maximise g subject to &lambda; &ge; "
        "0 — is a convex problem no matter what the primal was</b>, "
        "which is precisely why duality is useful for hard problems and not "
        "only for easy ones."),
  ("callout", "Weak duality always; strong duality usually",
   ["<b>Weak duality: g(&lambda;, &nu;) &le; p* for every dual feasible "
    "(&lambda;, &nu;).</b> <b>This holds for any optimisation problem "
    "whatsoever</b> — convex, non-convex, integer, combinatorial. The "
    "proof is two lines.",
    "<b>So any dual feasible point gives a lower bound on the primal "
    "optimum, for free.</b> <b>That is the single most useful consequence "
    "of duality</b>, and it is what branch and bound prunes with "
    "(Module 09) and what approximation guarantees are measured against "
    "(Module 10).",
    "<b>Strong duality: the gap is exactly zero, d* = p*.</b> For convex "
    "problems it holds under a mild regularity condition — "
    "<b>Slater's condition: there exists a strictly feasible point</b>, one "
    "satisfying every inequality constraint strictly.",
    "<b>So for a convex problem, solving either problem solves both</b>, "
    "and <b>a dual solution <i>proves</i> that a primal solution is "
    "optimal</b>. <b>A lower bound together with a matching feasible point "
    "is a certificate</b> — which converts 'I could not find anything "
    "better' into 'nothing better exists', and that is a categorically "
    "different kind of claim."]),

  ("h1", "2 &nbsp; What the dual variables mean"),
  ("callout", "Dual variables are prices",
   ["<b>&lambda;<sub>i</sub> is the rate at which the optimal value "
    "improves if constraint i is relaxed by one unit</b> — formally, "
    "&part;p*/&part;b<sub>i</sub> = &minus;&lambda;<sub>i</sub> where the "
    "problem is differentiable in the right-hand side.",
    "<b>So the dual variable <i>prices</i> the constraint.</b> 'An "
    "additional hour of machine time is worth thirty-four pounds' is a dual "
    "variable, reported in the problem's own vocabulary rather than in "
    "mathematical notation — <b>and stating it that way is what makes "
    "an optimisation result actionable to the person who owns the "
    "problem.</b>",
    "<b>A zero dual variable means the constraint is not binding.</b> "
    "Relaxing it buys nothing because you are not currently pressed against "
    "it, so no investment in that resource is worthwhile.",
    "<b>This is what makes duality practically valuable rather than merely "
    "formally elegant.</b> <b>It tells the problem owner where to "
    "invest</b> — which constraint to buy more of, which supplier to "
    "negotiate with, which deadline to extend — <b>and the primal "
    "solution alone does not.</b> Project 1 requires exactly this "
    "interpretation, and it is the part that converts a solved model into "
    "a decision."]),
  ("eq", "&lambda;<sub>i</sub> &middot; g<sub>i</sub>(x*) = 0 &nbsp; for "
         "every i &nbsp;&nbsp;&nbsp; (complementary slackness)"),
  ("p", "At optimality, for each constraint, at least one of the dual "
        "variable and the constraint slack is zero. <b>A slack constraint "
        "has zero price</b> — it is not limiting you, so relaxing it "
        "is worthless. <b>A positive price implies the constraint is "
        "tight</b> — you are pressed against it, which is why it has "
        "value. <b>This is the economic statement of the obvious: you do "
        "not pay for something you are not using</b>, and framing it that "
        "way makes it memorable in a way the algebra does not."),

  ("break",),
  ("h1", "3 &nbsp; What duality is actually for"),
  ("table", ["Use", "How", "Where it appears"],
   [["<b>Certifying optimality</b>",
     "<b>A primal feasible point and a dual feasible point with matching "
     "values prove each other optimal.</b>",
     "<b>Every solver reports this gap</b>, and it is how you know a "
     "solution is finished rather than merely stalled."],
    ["<b>Bounding a hard problem</b>",
     "<b>Any dual feasible point is a valid lower bound</b>, by weak "
     "duality, even when the primal is intractable.",
     "<b>Branch and bound</b> (Module 09 &sect;2) prunes entirely on "
     "these bounds."],
    ["<b>Sensitivity analysis</b>",
     "Shadow prices on every constraint (&sect;2).",
     "<b>The main practical payoff in applied work</b>, and the thing "
     "clients actually ask for."],
    ["<b>Solving an easier problem</b>",
     "<b>The dual is sometimes structurally simpler than the primal.</b>",
     "<b>The SVM: the dual has one variable per example and enables "
     "kernels</b> (CSCE 633 Module 07) — see the callout."],
    ["<b>Decomposition</b>",
     "Split a problem coupled by a few shared constraints by pricing the "
     "coupling and solving the parts independently.",
     "Large-scale structured problems; Dantzig–Wolfe and Benders "
     "decomposition."],
    ["<b>Theory</b>",
     "<b>Max-flow min-cut, von Neumann's minimax theorem, and LP duality "
     "are the same theorem.</b>",
     "Several famous results that look unrelated turn out to be instances "
     "of one — which is genuinely satisfying and worth noticing."]],
   [0.20, 0.38, 0.42]),
  ("callout", "The SVM dual is why kernels exist",
   ["<b>The support vector machine's primal problem optimises over the "
    "weight vector w</b>, whose dimension equals the number of features "
    "— which is a problem when the feature space is "
    "infinite-dimensional.",
    "<b>Its dual optimises over one variable per training example</b>, and "
    "<b>the data enters the dual only through inner products "
    "x<sub>i</sub><super>T</super>x<sub>j</sub></b> — individual "
    "feature vectors appear nowhere.",
    "<b>That is exactly what makes the kernel trick possible</b> "
    "(CSCE 633 Module 07 &sect;2). You can substitute a kernel function "
    "for the inner product <i>only because</i> the dual formulation never "
    "requires the vectors themselves — which is why that course "
    "could not fully justify the trick and this one can.",
    "<b>So kernels are a consequence of taking the dual, not an "
    "independent idea</b>, and <b>the representer theorem is the same "
    "observation stated differently</b> (CSCE 633 Module 07 &sect;2) "
    "— the solution lies in the span of the data because the dual has "
    "one variable per datum. <b>Three apparently separate results, one "
    "mechanism.</b>"]),

  ("h1", "4 &nbsp; When strong duality fails"),
  ("callout", "The duality gap is where the difficulty lives",
   ["<b>For non-convex problems strong duality generally fails:</b> the "
    "dual optimum is strictly below the primal optimum, and the difference "
    "is the <b>duality gap</b>.",
    "<b>That gap is a quantitative measure of the problem's "
    "non-convexity</b> — and it is precisely what makes the problem "
    "hard. A problem with zero gap can be solved through its dual; a "
    "problem with a large gap cannot.",
    "<b>The dual bound remains useful regardless.</b> Weak duality still "
    "holds, so the dual optimum is still a valid lower bound — "
    "<b>which is exactly what branch and bound prunes with</b> "
    "(Module 09 &sect;2), and the tighter the bound the smaller the "
    "search tree.",
    "<b>And the integrality gap of Module 10 is this gap</b>, specialised "
    "to integer programs and their linear relaxations. <b>So approximation "
    "guarantees are duality gaps with a ratio attached</b> — which "
    "unifies Modules 04, 09, and 10 under a single idea, and is the "
    "clearest reason to learn duality properly rather than treating it as "
    "a formality."]),
 ],
 "resources": [
   ("Boyd & Vandenberghe &mdash; Convex Optimization, chapter 5 (free)",
    "https://web.stanford.edu/~boyd/cvxbook/",
    "<b>The definitive treatment of this entire module</b>, including the "
    "sensitivity interpretation and Slater's condition."),
   ("Boyd &mdash; EE364A lectures on duality (free video)",
    "https://www.youtube.com/playlist?list=PL3940DD956CDF0622",
    "The geometric intuition for weak and strong duality, which the "
    "algebra alone does not convey."),
   ("MIT 15.093 &mdash; LP duality and sensitivity analysis (free)",
    "https://ocw.mit.edu/courses/15-093j-optimization-methods-fall-2009/",
    "<b>The &sect;2 shadow price material</b>, with worked economic "
    "interpretations."),
   ("Vanderbei &mdash; Linear Programming: Foundations and Extensions "
    "(free PDF)",
    "https://vanderbei.princeton.edu/LPbook/",
    "Free, and strong on duality's practical use and on the game theory "
    "connection in &sect;3."),
 ],
 "exercises": [
   "<b>Derive the dual</b> of a linear program by hand, from the "
   "Lagrangian.",
   "<b>Verify weak duality numerically</b> on a non-convex problem by "
   "evaluating the dual at several feasible points.",
   "Solve a convex problem and its dual and confirm the values match.",
   "<b>Construct a problem violating Slater's condition</b> and show a "
   "nonzero duality gap.",
   "<b>Interpret every dual variable</b> of your project model in the "
   "problem's own vocabulary.",
   "<b>Verify complementary slackness</b> on a solved instance, "
   "constraint by constraint.",
   "<b>Perturb a binding constraint by one unit</b> and confirm the "
   "objective changes by the dual variable.",
   "Derive the SVM dual and identify where the inner products appear.",
   "<b>Show max-flow min-cut is LP duality</b> by writing both programs.",
   "Use a dual bound to prune a small branch-and-bound search by hand.",
 ],
 "selfcheck": [
   "Construct the Lagrangian and the dual function, and say why the dual "
   "is always convex.",
   "State weak duality and say when it holds.",
   "State strong duality and the condition for it.",
   "What do dual variables mean, and why does that matter practically?",
   "State complementary slackness and give its economic reading.",
   "Name six uses of duality.",
   "Why does the SVM dual enable kernels?",
   "What is the duality gap, and what does it measure?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "First-Order Methods",
 "subtitle": "Gradient descent, with rates.",
 "question": "How fast does gradient descent converge, and on what does "
             "that depend?",
 "outcomes": [
     "State convergence rates for the standard assumptions.",
     "Explain the condition number's role.",
     "Explain acceleration and what it achieves.",
     "Apply proximal methods to non-smooth objectives.",
     "Connect the theory to CSCE 636's practice.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Rates",
   "blurb": "What the assumptions buy."},

  {"t": "table", "kicker": "Rates", "title": "Convergence, by assumption",
   "header": ["Assumptions", "Rate", "Iterations for ε"],
   "widths": [3.3, 3.4, 5.4],
   "rows": [
     ["<b>Convex, L-smooth</b>", "<b>O(1/k)</b>", "<b>O(1/ε) — sublinear</b>"],
     ["<b>+ accelerated</b>", "<b>O(1/k&#178;)</b>", "<b>O(1/√ε) — and this is optimal</b>"],
     ["<b>Strongly convex, smooth</b>", "<b>O((1−1/κ)ᵏ)</b>", "<b>O(κ log(1/ε)) — LINEAR</b>"],
     ["<b>+ accelerated</b>", "O((1−1/√κ)ᵏ)", "<b>O(√κ log(1/ε))</b>"],
     ["Convex, non-smooth", "O(1/√k)", "<b>O(1/ε&#178;) — much worse</b>"],
     ["<b>Non-convex, smooth</b>", "<b>O(1/√k) to a stationary point</b>", "<b>No global guarantee at all</b>"],
   ],
   "footnote": "<b>Strong convexity is what buys linear convergence</b> "
               "— the jump from O(1/ε) to O(log(1/ε)) is "
               "the single largest gain in this table.",
   "note": "The strongly-convex row is the one that matters; it explains "
           "why regularisation helps optimisation too."},

  {"t": "callout", "title": "The condition number decides the speed",
   "kind": "The quantity that governs everything here",
   "body": ["<b>κ = L / μ</b> — the ratio of the largest to "
            "the smallest curvature. <b>For a quadratic it is the ratio of "
            "the extreme Hessian eigenvalues.</b>",
            "<b>Large κ means a long thin valley</b>, and gradient "
            "descent zigzags across it while crawling along it "
            "(CSCE 633 M02 §2 — the same picture).",
            "<b>Iteration count scales with κ</b>, or with √κ "
            "when accelerated.",
            "<b>So conditioning is worth attacking directly:</b> "
            "<b>feature scaling, preconditioning, and L2 regularisation "
            "all reduce κ</b> — which is why regularisation speeds "
            "up optimisation as well as improving generalisation."]},

  {"t": "section", "label": "Part 2", "title": "Acceleration",
   "blurb": "Momentum, and why it is optimal."},

  {"t": "code", "kicker": "Nesterov", "title": "Acceleration, and what it is not",
   "lang": "text", "code": """
  HEAVY BALL (Polyak):
      v = beta*v + grad f(x)
      x = x - eta*v
  Accumulate a velocity. Damps oscillation across the valley.

  NESTEROV:
      y = x + beta*(x - x_prev)        # look ahead first
      x = y - eta * grad f(y)          # gradient AT the lookahead
  The gradient is evaluated at the EXTRAPOLATED point, not the
  current one. That one change gives the O(1/k^2) rate.

  WHY IT MATTERS: O(1/k^2) is OPTIMAL for first-order methods
  on smooth convex problems -- a LOWER BOUND, proved by Nemirovski
  and Yudin. No method using only gradients can do better.

  SO ACCELERATION IS NOT A HEURISTIC. It attains a known limit.

  WHAT IT IS NOT: it is not a descent method. The objective can
  INCREASE on individual steps, which alarms people watching
  the loss curve. That is expected behaviour.
""",
   "caption": "<b>Acceleration attains a proved lower bound</b>, which is "
              "a much stronger statement than 'momentum helps'.",
   "note": "That it's provably optimal distinguishes it from the "
           "heuristics in CSCE 636."},

  {"t": "section", "label": "Part 3", "title": "Non-smooth objectives",
   "blurb": "What to do about the L1 penalty."},

  {"t": "callout", "title": "Proximal methods handle the non-smooth part exactly",
   "kind": "The right tool for L1",
   "body": ["<b>Many objectives split as f + g, with f smooth and g "
            "non-smooth but simple</b> — least squares plus an L1 "
            "penalty, for instance.",
            "<b>Subgradient descent works and is slow</b> — "
            "O(1/ε²) by Part 1.",
            "<b>Proximal gradient does better:</b> take a gradient step "
            "on f, then apply the <i>proximal operator</i> of g, which "
            "solves g's part exactly.",
            "<b>For the L1 penalty the proximal operator is soft "
            "thresholding</b> — shrink toward zero and clip at zero. "
            "<b>Which is why the lasso produces exact zeros</b> "
            "(CSCE 633 M04), now derived rather than asserted."]},

  {"t": "section", "label": "Part 4", "title": "Back to practice",
   "blurb": "What this says about CSCE 636."},

  {"t": "table", "kicker": "Theory to practice", "title": "What the theory explains, and does not",
   "header": ["Practice", "Theory says", "Status"],
   "widths": [3.0, 4.3, 4.8],
   "rows": [
     ["<b>Feature scaling</b>", "<b>Reduces κ, so fewer iterations</b>", "<b>Fully explained</b>"],
     ["<b>Momentum</b>", "<b>Attains the optimal rate</b>", "<b>Explained, for convex problems</b>"],
     ["<b>L2 regularisation</b>", "Adds μ, so strong convexity", "<b>Explained — and it speeds training</b>"],
     ["<b>Adam</b>", "<b>Diagonal preconditioning</b>", "<b>Partly — convergence proofs are delicate</b>"],
     ["<b>Why SGD finds good minima</b>", "<b>Nothing</b>", "<b>Open (CSCE 636 M03 §4)</b>"],
     ["Learning rate schedules", "Some, for convex", "<b>Mostly empirical</b>"],
   ],
   "footnote": "<b>The honest summary: the theory explains the convex "
               "practice completely and the deep learning practice "
               "partially.</b>",
   "note": "Being explicit about the boundary is better than implying "
           "coverage."},

  {"t": "callout", "title": "Why the convex theory is still worth having",
   "kind": "The argument for this module",
   "body": ["<b>It tells you what is achievable</b> — the lower bounds "
            "say no first-order method does better, so a slow run is a "
            "conditioning problem rather than an algorithm choice.",
            "<b>It identifies the quantity to attack</b> — κ "
            "— which is actionable: scale, precondition, regularise.",
            "<b>It explains why the tricks work</b>, which lets you "
            "predict when they will not.",
            "<b>And many sub-problems inside non-convex pipelines are "
            "convex</b> — the last layer, the proximal step, the "
            "line search — <b>so the theory applies locally even when it "
            "does not apply globally.</b>"]},
 ],
 "takeaways": [
   "Convex and smooth gives O(1/k); strong convexity gives linear "
   "convergence, which is the single largest gain available.",
   "The condition number governs the iteration count, and feature scaling, "
   "preconditioning, and L2 regularisation all reduce it.",
   "Nesterov acceleration evaluates the gradient at an extrapolated point "
   "and attains O(1/k²), which is a proved lower bound rather than a "
   "heuristic.",
   "Acceleration is not a descent method — the objective can increase "
   "on individual steps.",
   "The proximal operator of the L1 penalty is soft thresholding, which is "
   "why the lasso produces exact zeros.",
   "The theory explains convex practice completely and deep learning "
   "practice partially — and why SGD finds good minima remains open.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Convergence rates"),
  ("table", ["Assumptions", "Rate", "Iterations to reach &epsilon;"],
   [["<b>Convex and L-smooth</b>", "<b>O(1/k)</b>",
     "<b>O(1/&epsilon;)</b> — sublinear. Halving the error doubles "
     "the work."],
    ["<b>Convex, L-smooth, accelerated</b>", "<b>O(1/k&#178;)</b>",
     "<b>O(1/&radic;&epsilon;)</b> — <b>and this is optimal</b> "
     "(&sect;2)."],
    ["<b>Strongly convex (&mu; &gt; 0) and smooth</b>",
     "<b>O((1 &minus; 1/&kappa;)<super>k</super>)</b>",
     "<b>O(&kappa; log(1/&epsilon;))</b> — <b>linear convergence</b>. "
     "Each additional digit of accuracy costs a constant number of "
     "iterations rather than a multiplying factor."],
    ["<b>Strongly convex, accelerated</b>",
     "O((1 &minus; 1/&radic;&kappa;)<super>k</super>)",
     "<b>O(&radic;&kappa; log(1/&epsilon;))</b>"],
    ["<b>Convex, non-smooth</b>", "O(1/&radic;k)",
     "<b>O(1/&epsilon;&#178;)</b> — substantially worse, which "
     "motivates &sect;3."],
    ["<b>Non-convex, smooth</b>",
     "<b>O(1/&radic;k) to a stationary point.</b>",
     "<b>No global guarantee of any kind</b> — only that the gradient "
     "norm shrinks. CSCE 636's situation."]],
   [0.26, 0.26, 0.48]),
  ("p", "<b>Strong convexity is what buys linear convergence</b>, and the "
        "jump from O(1/&epsilon;) to O(log(1/&epsilon;)) is by far the "
        "largest gain in this table — the difference between a million "
        "iterations and twenty for six digits of accuracy. <b>Which means "
        "adding a small L2 term to make a problem strongly convex can be "
        "worth it for the optimisation alone</b>, independently of its "
        "regularisation effect (CSCE 633 Module 04)."),
  ("callout", "The condition number decides the speed",
   ["<b>&kappa; = L / &mu;</b> — the ratio of the largest to the "
    "smallest curvature of the objective. <b>For a quadratic it is exactly "
    "the ratio of the largest to the smallest eigenvalue of the "
    "Hessian</b>, and it is the same condition number as in numerical "
    "linear algebra (CSCE 633 Module 02 &sect;1).",
    "<b>A large &kappa; means a long thin valley</b>, and gradient descent "
    "zigzags across the narrow direction while crawling along the long one "
    "— <b>which is exactly the picture CSCE 633 Module 02 &sect;2 "
    "drew to motivate feature scaling</b>, now with a quantity attached to "
    "it.",
    "<b>The iteration count scales linearly with &kappa;, or with "
    "&radic;&kappa; when accelerated.</b> So a condition number of 10,000 "
    "means ten thousand iterations rather than a hundred — a "
    "difference that is visible as 'the model will not train'.",
    "<b>So conditioning is worth attacking directly</b>, and it is "
    "actionable: <b>feature scaling, preconditioning, batch normalisation, "
    "and L2 regularisation all reduce &kappa;</b>. <b>Which explains why "
    "regularisation speeds up optimisation as well as improving "
    "generalisation</b> — two benefits from one term, for two "
    "unrelated reasons, which is a coincidence worth knowing about."]),

  ("h1", "2 &nbsp; Acceleration"),
  ("code", """HEAVY BALL (Polyak)
    v = beta*v + grad f(x)
    x = x - eta*v
  accumulate a velocity; damps oscillation across the valley

NESTEROV
    y = x + beta*(x - x_prev)      # look ahead FIRST
    x = y - eta * grad f(y)        # gradient AT the lookahead
  the gradient is evaluated at the EXTRAPOLATED point. That one
  change gives the O(1/k^2) rate.

WHY IT MATTERS
  O(1/k^2) is OPTIMAL for first-order methods on smooth convex
  problems -- a LOWER BOUND, proved by Nemirovski and Yudin.
  No method using only gradient information can do better.

  SO ACCELERATION IS NOT A HEURISTIC. It attains a known limit.

WHAT IT IS NOT
  it is not a descent method -- the objective can INCREASE on
  individual steps. Expected, and alarming to watch."""),
  ("p", "<b>That acceleration attains a proved lower bound is a much "
        "stronger statement than 'momentum helps'</b>, and it is the "
        "clearest distinction between this course and CSCE 636 "
        "Module 03: there, momentum was a technique that worked; here it "
        "is known to be optimal and known to be unimprovable without "
        "second-order information (Module 07)."),

  ("break",),
  ("h1", "3 &nbsp; Non-smooth objectives"),
  ("callout", "Proximal methods handle the non-smooth part exactly",
   ["<b>Many objectives split as f + g, where f is smooth and g is "
    "non-smooth but structurally simple</b> — least squares plus an "
    "&ell;<sub>1</sub> penalty being the standard case (CSCE 633 "
    "Module 04).",
    "<b>Subgradient descent handles it and is slow</b> — "
    "O(1/&epsilon;&#178;) by &sect;1, which is the worst row in the "
    "table, and it discards the fact that f was perfectly smooth.",
    "<b>Proximal gradient does much better:</b> take an ordinary gradient "
    "step on the smooth part f, then apply the <i>proximal operator</i> of "
    "g — which solves g's contribution exactly rather than "
    "approximating it by a subgradient. <b>The rate returns to O(1/k), and "
    "to O(1/k&#178;) when accelerated (FISTA).</b>",
    "<b>And for the &ell;<sub>1</sub> penalty the proximal operator is "
    "soft thresholding</b>: shrink each coordinate toward zero by a fixed "
    "amount and clip at zero. <b>Which is precisely why the lasso produces "
    "exact zeros</b> (CSCE 633 Module 04 &sect;1) — <b>the "
    "geometric corner argument there is now an algebraic fact about an "
    "operator</b>, derived rather than asserted, and the two explanations "
    "agree."]),

  ("h1", "4 &nbsp; Back to practice"),
  ("table", ["Practice from CSCE 636", "What the theory says", "Status"],
   [["<b>Feature scaling and normalisation</b>",
     "<b>Reduces &kappa;, so fewer iterations</b> (&sect;1).",
     "<b>Fully explained.</b>"],
    ["<b>Momentum</b>", "<b>Attains the optimal first-order rate</b> "
     "(&sect;2).",
     "<b>Explained, for convex problems.</b> The deep learning case is "
     "analogous rather than covered."],
    ["<b>L2 regularisation / weight decay</b>",
     "Adds &mu; &gt; 0, making the problem strongly convex and the "
     "convergence linear.",
     "<b>Explained — and it predicts that weight decay speeds "
     "training</b>, which it does, for a reason unrelated to "
     "generalisation."],
    ["<b>Adam</b>",
     "<b>Approximately diagonal preconditioning</b>, which reduces the "
     "effective condition number per coordinate.",
     "<b>Partly.</b> Convergence proofs for Adam are delicate and the "
     "original one was wrong — AMSGrad was proposed to fix it."],
    ["<b>Why SGD finds minima that generalise</b>", "<b>Nothing.</b>",
     "<b>Open</b> (CSCE 636 Module 03 &sect;4). The theory has nothing to "
     "say, and the flat-minima explanations remain contested."],
    ["<b>Learning rate schedules</b>",
     "Some results for convex problems; the explore-then-exploit framing "
     "is not derived.",
     "<b>Mostly empirical.</b>"]],
   [0.26, 0.37, 0.37]),
  ("callout", "Why the convex theory is still worth having",
   ["<b>It tells you what is achievable.</b> The lower bounds of &sect;2 "
    "say that no first-order method does better than O(1/k&#178;) — "
    "<b>so a slow run is a conditioning problem or a problem-structure "
    "problem, not a matter of finding a cleverer optimiser.</b> That "
    "redirects effort correctly.",
    "<b>It identifies the quantity to attack.</b> <b>&kappa;</b> is "
    "measurable and actionable: scale the features, precondition, add a "
    "regularisation term, reformulate. <b>Without the theory there is no "
    "named quantity to improve</b>, only a slow run.",
    "<b>It explains why the practical tricks work</b>, which is what lets "
    "you predict when they will <i>not</i> — a technique justified "
    "only by having worked before transfers unpredictably.",
    "<b>And many sub-problems inside non-convex pipelines are convex:</b> "
    "the final linear layer given fixed features, the proximal step, the "
    "line search, the dual problem (Module 04 &sect;1 — always "
    "convex). <b>So the theory applies locally even where it does not "
    "apply globally</b>, which is more often than the non-convexity of the "
    "overall problem suggests."]),
 ],
 "resources": [
   ("Nesterov &mdash; Introductory Lectures on Convex Optimization",
    "https://link.springer.com/book/10.1007/978-1-4419-8853-9",
    "<b>The rates of &sect;1 and the lower bounds of &sect;2</b>, from "
    "the person who proved most of them. Dense; the first two chapters are "
    "the relevant ones."),
   ("Boyd &mdash; EE364B, subgradient and proximal methods (free)",
    "https://web.stanford.edu/class/ee364b/",
    "<b>The &sect;3 material</b>, including the proximal operator "
    "catalogue and the soft-thresholding derivation."),
   ("Beck & Teboulle &mdash; FISTA (free)",
    "https://epubs.siam.org/doi/10.1137/080716542",
    "Accelerated proximal gradient — &sect;2 and &sect;3 combined, "
    "and the standard method for the lasso."),
   ("Sebastian Bubeck &mdash; Convex Optimization: Algorithms and "
    "Complexity (free)",
    "https://arxiv.org/abs/1405.4980",
    "<b>A free, modern, and readable treatment of this whole module</b>, "
    "with the lower bounds stated clearly."),
 ],
 "exercises": [
   "<b>Verify the O(1/k) rate empirically</b> on a smooth convex problem "
   "by plotting error against iteration on log axes.",
   "<b>Add an L2 term and verify the rate becomes linear.</b>",
   "<b>Construct quadratics with condition numbers 10, 100, and 1000</b> "
   "and measure the iteration count for each.",
   "Confirm the iteration count scales with &kappa; as predicted.",
   "Implement heavy ball and Nesterov acceleration and compare against "
   "plain gradient descent.",
   "<b>Verify the O(1/k&#178;) rate</b> and show the objective increases "
   "on some steps.",
   "<b>Derive the proximal operator of the L1 norm</b> and confirm it is "
   "soft thresholding.",
   "<b>Implement proximal gradient for the lasso</b> and compare its "
   "convergence against subgradient descent.",
   "Precondition a badly conditioned problem and measure the improvement.",
   "<b>Measure the condition number of a problem from CSCE 633</b> and "
   "predict its iteration count.",
 ],
 "selfcheck": [
   "Give convergence rates under six sets of assumptions.",
   "What does strong convexity buy, and why is it the largest gain?",
   "Define the condition number and say what reduces it.",
   "Describe Nesterov acceleration and what distinguishes it from heavy "
   "ball.",
   "Why is acceleration not a heuristic?",
   "Why is acceleration not a descent method?",
   "What is a proximal operator, and what is the L1 one?",
   "What does the theory explain about CSCE 636's practice, and what does "
   "it not?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Constrained Optimisation",
 "subtitle": "Optimality conditions when you cannot go everywhere.",
 "question": "What characterises an optimum subject to constraints?",
 "outcomes": [
     "State and apply the KKT conditions.",
     "Explain the geometric meaning of the stationarity condition.",
     "Apply projected and penalty methods.",
     "Explain augmented Lagrangian and ADMM.",
     "Recognise when constraints can be eliminated.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "KKT",
   "blurb": "The conditions, and what each one says."},

  {"t": "code", "kicker": "KKT", "title": "Four conditions",
   "lang": "text", "code": """
  At an optimum x* with multipliers lambda*, nu*:

  1. STATIONARITY
       grad f(x*) + sum lambda_i grad g_i(x*)
                  + sum nu_j grad h_j(x*)  =  0
       The objective gradient is a combination of the ACTIVE
       constraint gradients -- you cannot improve without
       violating something.

  2. PRIMAL FEASIBILITY     g_i(x*) <= 0,  h_j(x*) = 0

  3. DUAL FEASIBILITY       lambda_i >= 0
       Inequality prices cannot be negative: you would not pay
       to be MORE constrained.

  4. COMPLEMENTARY SLACKNESS  lambda_i * g_i(x*) = 0
       (Module 04 section 2 -- inactive constraints have no price)

  FOR A CONVEX PROBLEM satisfying a constraint qualification,
  KKT is NECESSARY AND SUFFICIENT. Finding a KKT point solves
  the problem.

  FOR A NON-CONVEX PROBLEM, KKT is only NECESSARY. A KKT point
  may be a saddle or a local maximum.
""",
   "caption": "<b>The convex case is the useful one:</b> KKT turns "
              "optimisation into solving a system of equations and "
              "inequalities.",
   "note": "The necessary-vs-sufficient split is the thing to retain."},

  {"t": "callout", "title": "Stationarity says the gradients balance",
   "kind": "The geometry",
   "body": ["<b>At an unconstrained optimum the gradient is zero</b> "
            "— no direction improves.",
            "<b>At a constrained optimum the gradient need not be "
            "zero</b> — it must point 'into' the constraints, so that "
            "every improving direction is infeasible.",
            "<b>Formally: the objective gradient lies in the cone spanned "
            "by the active constraint gradients.</b> That is what the "
            "stationarity equation says.",
            "<b>Picture a ball rolling downhill into a corner.</b> It "
            "stops not because the slope vanished but because the walls "
            "oppose it exactly — and λ measures how hard each "
            "wall pushes."]},

  {"t": "section", "label": "Part 2", "title": "Methods",
   "blurb": "How constraints are actually handled."},

  {"t": "table", "kicker": "Methods", "title": "Handling constraints",
   "header": ["Method", "Idea", "Character"],
   "widths": [2.8, 4.3, 5.0],
   "rows": [
     ["<b>Elimination</b>", "<b>Substitute equalities away</b>", "<b>Best when possible. Reduces dimension</b>"],
     ["<b>Projection</b>", "<b>Step, then project back onto the set</b>", "<b>Needs a cheap projection. Simple sets only</b>"],
     ["<b>Penalty</b>", "Add a penalty for violation", "<b>Ill-conditioned as the penalty grows</b>"],
     ["<b>Barrier</b>", "<b>+∞ at the boundary; stay strictly inside</b>", "<b>Interior point (M07)</b>"],
     ["<b>Augmented Lagrangian</b>", "<b>Penalty plus multiplier estimates</b>", "<b>Avoids the conditioning blow-up</b>"],
     ["<b>ADMM</b>", "Split variables; alternate", "<b>Decomposes; excellent for large problems</b>"],
   ],
   "footnote": "<b>The pure penalty method's conditioning problem is the "
               "reason augmented Lagrangian exists</b> — it gets "
               "exactness without an infinite penalty.",
   "note": "That progression penalty → augmented Lagrangian → ADMM is a "
           "clean story."},

  {"t": "callout", "title": "Why the pure penalty method fails",
   "kind": "The conditioning problem",
   "body": ["<b>Add ρ·(violation)² to the objective and "
            "minimise.</b> As ρ → ∞ the solution "
            "approaches the constrained optimum.",
            "<b>But the Hessian's condition number grows with "
            "ρ</b>, so the unconstrained problems become "
            "progressively harder to solve (Module 05 §1).",
            "<b>And with finite ρ the answer is never exactly "
            "feasible</b> — you are trading accuracy against "
            "conditioning.",
            "<b>The augmented Lagrangian fixes this</b> by adding "
            "multiplier estimates that are updated each round: <b>exact "
            "convergence at a finite, moderate penalty.</b> <b>Which is "
            "duality doing practical work.</b>"]},

  {"t": "section", "label": "Part 3", "title": "ADMM",
   "blurb": "Splitting, and why it scales."},

  {"t": "code", "kicker": "ADMM", "title": "Alternating direction method of multipliers",
   "lang": "text", "code": """
  Rewrite  min f(x) + g(z)   subject to  Ax + Bz = c
  -- that is, SPLIT the objective so each part is easy alone.

  Then alternate:
      x <- argmin_x  L_rho(x, z, u)      # f's part only
      z <- argmin_z  L_rho(x, z, u)      # g's part only
      u <- u + (Ax + Bz - c)             # dual update

  WHY IT IS USEFUL
    * each subproblem involves only ONE of f and g, so each can
      use whatever method suits it -- including a closed form
    * it DECOMPOSES: if f splits across data, the x-update is
      embarrassingly parallel (CSCE 735)
    * convergence is modest -- it gets to moderate accuracy
      quickly and high accuracy slowly

  LASSO IN ADMM
      x-update:  a ridge regression (closed form)
      z-update:  SOFT THRESHOLDING (Module 05 section 3)
      Each step is trivial; the coupling is handled by u.

  Boyd's 2011 monograph made this the standard tool for
  large-scale structured problems.
""",
   "caption": "<b>The pattern is: split so each piece is easy, and let "
              "the multipliers handle the coupling.</b>",
   "note": "ADMM is genuinely practical and underused outside its "
           "community."},

  {"t": "section", "label": "Part 4", "title": "Recognising structure",
   "blurb": "When a constraint is not really there."},

  {"t": "bullets", "kicker": "Simplification", "title": "Constraints that can be removed",
   "items": [
     "<b>Equalities can be substituted away</b>, reducing the dimension "
     "— always worth doing when the substitution is clean.",
     "",
     "<b>Simple bounds become projections</b>, which are free.",
     "",
     "<b>A simplex constraint becomes a softmax reparameterisation</b> "
     "— which is why neural network outputs are unconstrained.",
     "",
     "<b>Orthogonality becomes a manifold</b>, with its own gradient "
     "methods.",
     "",
     "<b>And a redundant constraint can simply be deleted</b> — "
     "which presolve does automatically and modellers routinely add by "
     "accident.",
   ],
   "footnote": "<b>The softmax reparameterisation is the one that "
               "connects:</b> CSCE 636's networks optimise freely because "
               "the constraint was absorbed into the parameterisation."},
 ],
 "takeaways": [
   "KKT has four conditions: stationarity, primal feasibility, dual "
   "feasibility, and complementary slackness.",
   "For a convex problem with a constraint qualification, KKT is necessary "
   "and sufficient — so finding a KKT point solves the problem.",
   "Stationarity says the objective gradient lies in the cone of active "
   "constraint gradients — every improving direction is infeasible.",
   "The pure penalty method's condition number grows with the penalty, "
   "which is why augmented Lagrangian exists.",
   "ADMM splits an objective so each piece is easy alone and lets the "
   "multipliers handle the coupling — and it decomposes across data.",
   "A simplex constraint becomes a softmax reparameterisation, which is why "
   "neural networks optimise unconstrained.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The KKT conditions"),
  ("code", """At an optimum x* with multipliers lambda*, nu*:

1. STATIONARITY
     grad f(x*) + sum lambda_i grad g_i(x*)
                + sum nu_j grad h_j(x*) = 0
   the objective gradient is a combination of the ACTIVE
   constraint gradients

2. PRIMAL FEASIBILITY    g_i(x*) <= 0,  h_j(x*) = 0

3. DUAL FEASIBILITY      lambda_i >= 0
   inequality prices cannot be negative -- you would not pay to
   be MORE constrained

4. COMPLEMENTARY SLACKNESS   lambda_i * g_i(x*) = 0
   (Module 04 section 2)

CONVEX + constraint qualification: KKT is NECESSARY AND
SUFFICIENT. Finding a KKT point SOLVES the problem.

NON-CONVEX: KKT is only NECESSARY. A KKT point may be a saddle
or a local maximum."""),
  ("p", "<b>The convex case is the useful one.</b> KKT converts an "
        "optimisation problem into a system of equations and inequalities "
        "— which can sometimes be solved directly by hand for small "
        "problems, and which is what interior point methods (Module 07) "
        "solve numerically. <b>The necessary-versus-sufficient distinction "
        "is the thing to retain</b>: in the non-convex case a solver "
        "reporting 'KKT conditions satisfied' has found a stationary point "
        "and established nothing about optimality."),
  ("callout", "Stationarity says the gradients balance",
   ["<b>At an unconstrained optimum the gradient is zero</b> — there "
    "is no direction in which the objective improves.",
    "<b>At a constrained optimum the gradient need not be zero.</b> It "
    "must instead point 'into' the constraints, so that every direction "
    "that would improve the objective is infeasible — blocked by a "
    "constraint.",
    "<b>Formally: the objective gradient lies in the cone spanned by the "
    "gradients of the <i>active</i> constraints.</b> That is exactly what "
    "the stationarity equation asserts, with the multipliers as the "
    "non-negative coefficients.",
    "<b>Picture a ball rolling downhill into a corner.</b> It comes to "
    "rest not because the slope vanished but because the walls push back "
    "exactly enough to cancel gravity — <b>and &lambda; measures how "
    "hard each wall is pushing</b>, which is Module 04 &sect;2's shadow "
    "price arriving as a physical quantity. <b>A wall the ball is not "
    "touching pushes with force zero</b>, which is complementary "
    "slackness."]),

  ("h1", "2 &nbsp; Methods"),
  ("table", ["Method", "Idea", "Character"],
   [["<b>Elimination</b>",
     "<b>Use the equality constraints to substitute variables away.</b>",
     "<b>The best option when it is available</b> — it reduces the "
     "dimension and removes the constraint entirely rather than handling "
     "it."],
    ["<b>Projection</b>",
     "<b>Take an unconstrained step, then project back onto the feasible "
     "set.</b>",
     "<b>Requires a cheap projection</b>, so it is limited to simple sets "
     "— boxes, balls, the simplex, the non-negative orthant. Where it "
     "applies it is excellent."],
    ["<b>Penalty</b>",
     "Add &rho; times the squared violation to the objective and minimise "
     "unconstrained.",
     "<b>Becomes ill-conditioned as &rho; grows</b> — see the "
     "callout."],
    ["<b>Barrier</b>",
     "<b>Add a term that goes to +&infin; at the boundary</b>, so "
     "iterates stay strictly interior.",
     "<b>The basis of interior point methods</b> (Module 07)."],
    ["<b>Augmented Lagrangian</b>",
     "<b>A penalty term plus explicit multiplier estimates, updated each "
     "outer iteration.</b>",
     "<b>Achieves exact convergence at a finite, moderate penalty</b>, "
     "avoiding the conditioning blow-up."],
    ["<b>ADMM</b>",
     "Split the variables so each subproblem is easy, and alternate "
     "between them.",
     "<b>Decomposes across data and across terms; excellent for "
     "large structured problems</b> (&sect;3)."]],
   [0.19, 0.36, 0.45]),
  ("callout", "Why the pure penalty method fails",
   ["<b>Add &rho;&middot;(violation)&#178; to the objective and minimise "
    "it as an unconstrained problem.</b> As &rho; &rarr; &infin; the "
    "solution approaches the constrained optimum, which is the right "
    "limiting behaviour.",
    "<b>But the Hessian's condition number grows with &rho;.</b> The "
    "penalty adds enormous curvature in the constraint directions and none "
    "elsewhere, so <b>&kappa; grows without bound and each unconstrained "
    "subproblem becomes progressively harder to solve</b> (Module 05 "
    "&sect;1) — the iteration count blows up exactly as the answer "
    "becomes accurate.",
    "<b>And at any finite &rho; the answer is never exactly feasible.</b> "
    "You are trading accuracy against conditioning with no setting that "
    "gives both.",
    "<b>The augmented Lagrangian resolves this</b> by adding explicit "
    "multiplier estimates that are updated after each inner solve: the "
    "multipliers absorb what the penalty would otherwise have to force, "
    "<b>so exact convergence is achieved at a finite and moderate "
    "&rho;</b>. <b>Which is duality doing practical work</b> — the "
    "multipliers of Module 04 turning out to be the fix for a numerical "
    "problem."]),

  ("break",),
  ("h1", "3 &nbsp; ADMM"),
  ("code", """Rewrite  min f(x) + g(z)  subject to  Ax + Bz = c
-- SPLIT the objective so that each part is easy ALONE.

Then alternate:
    x <- argmin_x L_rho(x, z, u)     # f's part only
    z <- argmin_z L_rho(x, z, u)     # g's part only
    u <- u + (Ax + Bz - c)           # dual update

WHY IT IS USEFUL
  * each subproblem touches only ONE of f and g, so each can
    use whatever method suits -- often a closed form
  * it DECOMPOSES: if f splits across data, the x-update is
    embarrassingly parallel (CSCE 735)
  * convergence is modest -- moderate accuracy fast, high
    accuracy slowly, which suits machine learning well

LASSO IN ADMM
    x-update:  ridge regression (closed form)
    z-update:  SOFT THRESHOLDING (Module 05 section 3)
    trivial steps; the coupling is carried by u"""),
  ("p", "<b>The pattern is: split the problem so each piece is easy, and "
        "let the multipliers handle the coupling.</b> Boyd's 2011 "
        "monograph collected the method and its applications and made it "
        "the standard tool for large-scale structured problems — "
        "<b>and it remains underused outside the optimisation community</b> "
        "relative to how well it fits distributed machine learning, where "
        "the data split is natural and moderate accuracy is sufficient."),

  ("h1", "4 &nbsp; Recognising removable constraints"),
  ("ul", ["<b>Equality constraints can frequently be substituted away</b>, "
          "reducing the problem's dimension and eliminating the constraint "
          "entirely. <b>Always worth attempting when the substitution is "
          "clean</b> — it makes every subsequent step easier.",
          "<b>Simple bounds become projections</b>, which for a box or the "
          "non-negative orthant cost one clamp per coordinate — "
          "effectively free, and projected gradient descent then applies "
          "directly.",
          "<b>A simplex constraint (non-negative, summing to one) becomes a "
          "softmax reparameterisation.</b> Optimise unconstrained over "
          "logits and map through the softmax; the constraint is satisfied "
          "by construction. <b>This is why neural network classifiers "
          "optimise freely</b> (CSCE 636) — <b>the probability "
          "simplex constraint was absorbed into the parameterisation and "
          "nobody had to mention it</b>, which is worth noticing as an "
          "instance of a general technique.",
          "<b>Orthogonality constraints define a manifold</b> (the Stiefel "
          "manifold), which has its own gradient methods — "
          "Riemannian optimisation — that respect the geometry rather "
          "than projecting onto it.",
          "<b>And a redundant constraint can simply be deleted.</b> "
          "Presolve (Module 03 &sect;4) does this automatically, and "
          "<b>modellers add redundant constraints routinely by "
          "accident</b> — expressing the same restriction twice in "
          "different forms, which costs nothing in correctness and a great "
          "deal in solve time."]),
 ],
 "resources": [
   ("Boyd & Vandenberghe &mdash; Convex Optimization, chapters 5 and 10 "
    "(free)",
    "https://web.stanford.edu/~boyd/cvxbook/",
    "KKT and the constrained methods of &sect;1 and &sect;2, with the "
    "geometric interpretation."),
   ("Boyd et al. &mdash; Distributed Optimization and Statistical Learning "
    "via ADMM (free)",
    "https://web.stanford.edu/~boyd/papers/admm_distr_stats.html",
    "<b>The &sect;3 monograph.</b> Comprehensive, readable, and full of "
    "worked formulations including the lasso."),
   ("Nocedal & Wright &mdash; Numerical Optimization, chapters 12 and 17",
    "https://link.springer.com/book/10.1007/978-0-387-40065-5",
    "The augmented Lagrangian development of &sect;2, with the "
    "conditioning analysis."),
   ("Absil, Mahony & Sepulchre &mdash; Optimization Algorithms on Matrix "
    "Manifolds (free PDF)",
    "https://press.princeton.edu/absil",
    "The manifold case of &sect;4, free from the publisher."),
 ],
 "exercises": [
   "<b>Write the KKT conditions</b> for your project model and check them "
   "at the solver's solution.",
   "<b>Solve a small constrained problem by hand from KKT</b> and verify "
   "against a solver.",
   "<b>Find a KKT point of a non-convex problem that is not optimal.</b>",
   "Implement projected gradient descent for a box constraint.",
   "<b>Implement the pure penalty method</b> and plot the condition number "
   "and iteration count against &rho;.",
   "<b>Implement the augmented Lagrangian</b> and show convergence at "
   "finite &rho;.",
   "<b>Implement ADMM for the lasso</b> and verify the z-update is soft "
   "thresholding.",
   "Compare ADMM against proximal gradient on the same lasso instance.",
   "<b>Eliminate an equality constraint by substitution</b> and compare "
   "solve times.",
   "<b>Reparameterise a simplex constraint as a softmax</b> and optimise "
   "unconstrained.",
 ],
 "selfcheck": [
   "State the four KKT conditions and what each says.",
   "When is KKT sufficient, and when only necessary?",
   "Explain stationarity geometrically.",
   "Compare six methods for handling constraints.",
   "Why does the pure penalty method fail, and what fixes it?",
   "Describe ADMM and say why it decomposes.",
   "Give the ADMM steps for the lasso.",
   "Name five constraints that can be eliminated or reparameterised.",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Newton and Interior Point",
 "subtitle": "Using curvature, and why linear programming is fast.",
 "question": "What does second-order information buy?",
 "outcomes": [
     "Explain Newton's method and its convergence.",
     "Explain why Newton is affine invariant and what that means.",
     "Explain quasi-Newton methods and when they are the right "
     "choice.",
     "Explain the barrier method and the central path.",
     "Explain why interior point methods transformed linear "
     "programming.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Newton's method",
   "blurb": "Fit a quadratic and jump to its minimum."},

  {"t": "eq", "kicker": "Newton", "title": "The step, and the rate",
   "eqs": [
     ("x ← x − [∇²f(x)]⁻¹ ∇f(x)",
      "Minimise the local second-order Taylor model exactly."),
     ("Quadratic convergence near the optimum",
      "The number of correct digits roughly DOUBLES each iteration."),
     ("Cost: O(n³) per step to solve the Newton system",
      "Which is the whole problem at scale."),
   ],
   "caption": "<b>Quadratic convergence means six iterations where "
              "gradient descent needs thousands</b> — if you can "
              "afford the step.",
   "note": "The digit-doubling framing makes quadratic convergence "
           "concrete."},

  {"t": "callout", "title": "Newton is affine invariant, and gradient descent is not",
   "kind": "The deep difference",
   "body": ["<b>Rescale the variables and Newton's iterates follow the "
            "same path</b>, transformed. Its behaviour does not depend on "
            "the coordinate system.",
            "<b>Gradient descent is not affine invariant.</b> Its path "
            "depends entirely on the scaling — which is why feature "
            "scaling matters so much (Module 05 §1).",
            "<b>So Newton is immune to the condition number</b>, in the "
            "sense that &kappa; does not appear in its local "
            "convergence rate.",
            "<b>That is the real content of 'Newton uses curvature'.</b> "
            "<b>It is not a faster first-order method; it is a method "
            "whose notion of distance comes from the problem rather than "
            "from the coordinates.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Making it affordable",
   "blurb": "Quasi-Newton and the middle ground."},

  {"t": "table", "kicker": "Spectrum", "title": "From gradient to full Newton",
   "header": ["Method", "Uses", "Cost per step"],
   "widths": [2.7, 4.3, 5.1],
   "rows": [
     ["<b>Gradient descent</b>", "<b>First derivatives only</b>", "<b>O(n)</b>"],
     ["<b>L-BFGS</b>", "<b>Hessian approximation from recent gradients</b>", "<b>O(mn), m ≈ 10. The practical default</b>"],
     ["<b>BFGS</b>", "Full dense Hessian approximation", "<b>O(n&#178;) storage — limits n</b>"],
     ["<b>Newton</b>", "<b>Exact Hessian</b>", "<b>O(n&#179;), or less if sparse</b>"],
     ["<b>Newton-CG</b>", "<b>Hessian-vector products only</b>", "<b>Never forms the Hessian. Scales</b>"],
     ["Gauss-Newton", "<b>Hessian approximated from the Jacobian</b>", "Least squares; the basis of Levenberg–Marquardt"],
   ],
   "footnote": "<b>L-BFGS is the right default for smooth unconstrained "
               "problems of moderate size</b>, and it is consistently "
               "under-used in machine learning.",
   "note": "Hessian-vector products via autodiff is the trick that makes "
           "Newton-CG viable."},

  {"t": "callout", "title": "You never need the Hessian, only its action",
   "kind": "The practical insight",
   "body": ["<b>Newton's step requires solving ∇²f·d = "
            "−∇f</b>, which an iterative solver can do "
            "using only Hessian-vector products.",
            "<b>And a Hessian-vector product costs about one extra "
            "gradient evaluation</b> — it is the directional derivative "
            "of the gradient, available from automatic differentiation "
            "(CSCE 636 M02).",
            "<b>So second-order methods scale to problems where the "
            "Hessian could never be stored.</b>",
            "<b>This is why Newton-CG and trust-region methods are "
            "viable on large problems</b>, and why dismissing second-order "
            "methods as 'O(n&#179;)' is out of date."]},

  {"t": "section", "label": "Part 3", "title": "Interior point",
   "blurb": "The barrier, and the central path."},

  {"t": "code", "kicker": "Barrier", "title": "Follow the central path to the boundary",
   "lang": "text", "code": """
  Replace the constraints with a BARRIER in the objective:

      minimise  t*f(x) - sum_i log(-g_i(x))

  The log barrier is +infinity at the boundary, so any iterate
  stays strictly feasible. Solve with Newton (it is smooth).

  THE CENTRAL PATH: the solution x*(t) as t varies. At small t
  the barrier dominates and x* sits in the analytic centre; as
  t -> infinity the objective dominates and x*(t) approaches
  the true constrained optimum.

  SO: solve for an increasing sequence of t, each time WARM
  STARTING from the previous solution. Each solve takes a few
  Newton steps because the start is close.

  THE GUARANTEE
    the duality gap at x*(t) is EXACTLY m/t, where m is the
    number of inequality constraints. So you always KNOW how
    suboptimal you are -- Module 04's certificate, continuously
    available, for free.

  Total complexity: O(sqrt(m)) outer iterations. POLYNOMIAL.
""",
   "caption": "<b>The m/t duality gap is what makes this a method with a "
              "guarantee</b> rather than a heuristic — you can always "
              "state how far from optimal you are.",
   "note": "The explicit gap is the most elegant thing in the module."},

  {"t": "callout", "title": "Why interior point changed linear programming",
   "kind": "The historical result",
   "body": ["<b>Khachiyan's ellipsoid method (1979) proved linear "
            "programming is polynomial</b> and was useless in practice.",
            "<b>Karmarkar's interior point method (1984) was polynomial "
            "<i>and</i> competitive</b> — the first method that was "
            "both.",
            "<b>The competition improved both:</b> simplex implementations "
            "got dramatically faster in response, and solvers now carry "
            "both and choose.",
            "<b>Interior point wins on large sparse problems; simplex "
            "wins when you need a warm start</b> — which is why branch and "
            "bound (Module 09) uses simplex for its thousands of "
            "re-solves."]},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "Which method, for which problem."},

  {"t": "bullets", "kicker": "Choosing", "title": "Second-order, or not",
   "items": [
     "<b>Smooth, unconstrained, n up to ~10⁴: L-BFGS.</b> "
     "Few hyperparameters and fast.",
     "",
     "<b>Constrained convex: interior point</b>, through a modelling "
     "layer like CVXPY.",
     "",
     "<b>Very large, stochastic, non-convex: first order</b> — "
     "curvature is expensive and noisy, and CSCE 636's methods win.",
     "",
     "<b>Least squares: Gauss–Newton or "
     "Levenberg–Marquardt</b>, which exploit the structure.",
     "",
     "<b>And second-order methods are under-used in machine "
     "learning</b> — partly for good reasons, partly from habit.",
   ],
   "footnote": "<b>The good reason: stochastic gradients make curvature "
               "estimates noisy, and the Hessian changes faster than it "
               "can be estimated.</b>"},
 ],
 "takeaways": [
   "Newton minimises the local quadratic model exactly and converges "
   "quadratically — the correct digits roughly double each iteration.",
   "Newton is affine invariant and gradient descent is not, which is why "
   "the condition number does not appear in Newton's local rate.",
   "A Hessian-vector product costs about one extra gradient, so "
   "second-order methods scale to problems where the Hessian cannot be "
   "stored.",
   "L-BFGS is the right default for smooth unconstrained problems of "
   "moderate size and is under-used in machine learning.",
   "The log barrier keeps iterates strictly feasible, and the duality gap "
   "on the central path is exactly m/t — a free, continuous "
   "certificate.",
   "Interior point was the first method for linear programming that was "
   "both polynomial and practically competitive, and the competition "
   "improved simplex too.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Newton's method"),
  ("eq", "x &larr; x &minus; [&nabla;&#178;f(x)]<super>&minus;1</super> "
         "&nabla;f(x)"),
  ("p", "<b>Build the second-order Taylor model of f at the current point "
        "and jump to that quadratic's exact minimum.</b> Near a "
        "non-degenerate optimum this converges <b>quadratically</b> "
        "— <b>the number of correct digits roughly doubles each "
        "iteration</b>, so six iterations can achieve what thousands of "
        "gradient steps would. <b>The cost is O(n&#179;) per step</b> to "
        "solve the Newton system (less for sparse or structured Hessians), "
        "and that cost is the entire obstacle at scale — which "
        "&sect;2 addresses."),
  ("callout", "Newton is affine invariant and gradient descent is not",
   ["<b>Rescale or linearly transform the variables, and Newton's iterates "
    "follow the same path under the same transformation.</b> Its behaviour "
    "does not depend on the coordinate system at all.",
    "<b>Gradient descent is not affine invariant.</b> Its path depends "
    "entirely on the scaling of the variables — <b>which is precisely "
    "why feature scaling matters so much</b> (Module 05 &sect;1, "
    "CSCE 633 Module 02 &sect;2). The method's notion of 'steepest' is a "
    "statement about the coordinates, not about the function.",
    "<b>So Newton is immune to the condition number</b>, in the sense that "
    "&kappa; does not appear in its local convergence rate — a "
    "badly scaled problem and a well scaled one take the same number of "
    "Newton steps.",
    "<b>That is the real content of the claim that 'Newton uses "
    "curvature'.</b> <b>It is not merely a faster first-order method; it "
    "is a method whose notion of distance is derived from the problem's own "
    "geometry rather than from an arbitrary choice of coordinates.</b> And "
    "it explains why preconditioning a first-order method is, in effect, an "
    "attempt to approximate this property cheaply."]),

  ("h1", "2 &nbsp; Making second order affordable"),
  ("table", ["Method", "What it uses", "Cost per step"],
   [["<b>Gradient descent</b>", "<b>First derivatives only.</b>",
     "<b>O(n)</b>, and O(&kappa;) iterations."],
    ["<b>L-BFGS</b>",
     "<b>An implicit Hessian approximation built from the last m gradient "
     "differences.</b>",
     "<b>O(mn) with m around 10.</b> <b>The practical default for smooth "
     "unconstrained problems</b>, and consistently under-used in machine "
     "learning."],
    ["<b>BFGS</b>", "A full dense Hessian approximation, updated each "
     "step.",
     "<b>O(n&#178;) storage</b>, which caps the problem size — hence "
     "the limited-memory variant."],
    ["<b>Newton</b>", "<b>The exact Hessian.</b>",
     "<b>O(n&#179;)</b> for a dense solve, far less if the Hessian is "
     "sparse or structured."],
    ["<b>Newton-CG (truncated Newton)</b>",
     "<b>Hessian-vector products only</b> — the Newton system is "
     "solved approximately by conjugate gradients.",
     "<b>Never forms or stores the Hessian</b>, so it scales to very large "
     "n — see the callout."],
    ["<b>Gauss-Newton</b>",
     "<b>The Hessian approximated from the Jacobian</b>, valid for least "
     "squares with small residuals.",
     "The basis of Levenberg–Marquardt, and the standard method for "
     "nonlinear least squares — including bundle adjustment "
     "(CSCE 748)."]],
   [0.19, 0.39, 0.42]),
  ("callout", "You never need the Hessian, only its action",
   ["<b>Newton's step requires solving &nabla;&#178;f &middot; d = "
    "&minus;&nabla;f</b>, and an iterative linear solver — conjugate "
    "gradients — requires only the ability to compute "
    "&nabla;&#178;f &middot; v for given vectors v. <b>It never needs the "
    "matrix itself.</b>",
    "<b>And a Hessian-vector product costs roughly one extra gradient "
    "evaluation.</b> It is the directional derivative of the gradient, "
    "which automatic differentiation computes directly (CSCE 636 "
    "Module 02) — a forward-over-reverse or reverse-over-reverse "
    "composition, available in every major framework.",
    "<b>So second-order methods scale to problems where the Hessian could "
    "never be stored</b>, let alone factorised — a million-parameter "
    "model has a Hessian with 10<super>12</super> entries and perfectly "
    "usable Hessian-vector products.",
    "<b>This is why Newton-CG and trust-region methods are viable on large "
    "problems</b>, and <b>why dismissing second-order methods as "
    "'O(n&#179;), therefore impractical' is out of date</b> — a "
    "dismissal that nonetheless remains common, and which the Hessian-free "
    "optimisation literature addressed directly."]),

  ("break",),
  ("h1", "3 &nbsp; Interior point methods"),
  ("code", """Replace the constraints with a BARRIER in the objective:

    minimise  t*f(x) - sum_i log(-g_i(x))

The log barrier is +infinity at the boundary, so every iterate
stays strictly feasible. The result is smooth -- solve it with
Newton.

THE CENTRAL PATH: the solution x*(t) as t varies. Small t: the
barrier dominates and x* sits near the analytic centre. Large t:
the objective dominates and x*(t) approaches the constrained
optimum.

SO: solve for an increasing sequence of t, WARM STARTING each
solve from the previous solution. Each takes a few Newton steps
because it begins close.

THE GUARANTEE
  the duality gap at x*(t) is EXACTLY m/t, with m the number of
  inequality constraints. You always KNOW how suboptimal you
  are -- Module 04's certificate, continuously available, free.

Total: O(sqrt(m)) outer iterations. POLYNOMIAL."""),
  ("p", "<b>The explicit m/t duality gap is the most elegant thing in this "
        "module.</b> It converts the barrier method from a plausible "
        "heuristic into an algorithm with a guarantee at every iterate "
        "— you can stop at any point and state exactly how far from "
        "optimal you are, which is Module 04's certificate delivered "
        "continuously and without extra work."),
  ("callout", "Why interior point changed linear programming",
   ["<b>Khachiyan's ellipsoid method (1979) proved that linear programming "
    "is solvable in polynomial time</b> — a major theoretical result "
    "— <b>and was entirely useless in practice</b>, being slower than "
    "simplex on every real instance.",
    "<b>Karmarkar's interior point method (1984) was polynomial "
    "<i>and</i> competitive</b> — the first algorithm that was both, "
    "and it caused a genuine upheaval, including a patent dispute and a "
    "great deal of commercial interest.",
    "<b>The competition improved both.</b> Simplex implementations got "
    "dramatically faster through the late 1980s and 1990s in direct "
    "response, with better pivoting, better factorisation updates, and "
    "much better presolve — <b>so the net effect was far larger than "
    "either method alone</b>, and solvers now carry both and select per "
    "instance.",
    "<b>Interior point wins on large sparse problems; simplex wins when a "
    "warm start is available</b> — <b>which is why branch and bound "
    "uses simplex for its thousands of nearly-identical re-solves</b> "
    "(Module 09 &sect;2), since interior point cannot warm start "
    "effectively. The two are complements rather than competitors, which "
    "was not obvious at the time."]),

  ("h1", "4 &nbsp; Choosing"),
  ("ul", ["<b>Smooth, unconstrained, n up to roughly 10<super>4</super>: "
          "L-BFGS.</b> Few hyperparameters, fast convergence, and a "
          "well-tested implementation in every scientific library.",
          "<b>Constrained convex: interior point</b>, reached through a "
          "modelling layer such as CVXPY so that you write the problem and "
          "not the algorithm.",
          "<b>Very large, stochastic, non-convex: first-order methods.</b> "
          "<b>Curvature estimates from mini-batches are noisy, and the "
          "Hessian of a neural network changes faster than it can be "
          "usefully estimated</b> — which is the good reason "
          "second-order methods have not displaced SGD in deep learning, "
          "as distinct from the habitual one.",
          "<b>Nonlinear least squares: Gauss–Newton or "
          "Levenberg–Marquardt</b>, which exploit the residual "
          "structure to approximate the Hessian from the Jacobian — "
          "and which underlie bundle adjustment and camera calibration "
          "(CSCE 748).",
          "<b>And second-order methods are genuinely under-used in machine "
          "learning</b> — partly for the good reason above, and partly "
          "from habit: <b>a deterministic full-batch problem of moderate "
          "size should usually be solved with L-BFGS rather than with Adam</b>, "
          "and frequently is not."]),
 ],
 "resources": [
   ("Boyd & Vandenberghe &mdash; Convex Optimization, chapters 9, 10 "
    "and 11 (free)",
    "https://web.stanford.edu/~boyd/cvxbook/",
    "<b>Newton, equality-constrained Newton, and the barrier method with "
    "the m/t result</b> — the core of this module."),
   ("Nocedal & Wright &mdash; Numerical Optimization, chapters 6, 7 and "
    "19",
    "https://link.springer.com/book/10.1007/978-0-387-40065-5",
    "Quasi-Newton methods and the practical detail of &sect;2, including "
    "L-BFGS's two-loop recursion."),
   ("Martens &mdash; Deep Learning via Hessian-Free Optimization (free)",
    "https://www.cs.toronto.edu/~jmartens/docs/Deep_HessianFree.pdf",
    "<b>The &sect;2 callout applied to neural networks</b> — "
    "Hessian-vector products via automatic differentiation, at scale."),
   ("Wright &mdash; Primal-Dual Interior-Point Methods",
    "https://epubs.siam.org/doi/book/10.1137/1.9781611971453",
    "The reference for &sect;3's method as actually implemented in "
    "solvers."),
 ],
 "exercises": [
   "<b>Implement Newton's method</b> and verify quadratic convergence by "
   "plotting the error on a log-log scale.",
   "<b>Demonstrate affine invariance:</b> rescale the variables and show "
   "Newton's iteration count is unchanged while gradient descent's is not.",
   "Implement L-BFGS, or use one, and compare against gradient descent and "
   "Newton on the same problem.",
   "<b>Compute a Hessian-vector product by automatic differentiation</b> "
   "and verify it against the explicit Hessian.",
   "<b>Implement Newton-CG</b> using only Hessian-vector products.",
   "Implement the log barrier method for a small linear program.",
   "<b>Trace the central path</b> by solving for a sequence of t, and plot "
   "it.",
   "<b>Verify the duality gap is m/t</b> at each point on the path.",
   "Compare simplex and interior point on a large sparse LP and on a small "
   "dense one.",
   "<b>Solve a full-batch problem from CSCE 633 with L-BFGS</b> and "
   "compare against Adam.",
 ],
 "selfcheck": [
   "State Newton's step and its convergence rate.",
   "What does affine invariance mean, and why does it matter?",
   "Compare six methods on what they use and what they cost.",
   "Why do you never need the Hessian itself?",
   "Describe the barrier method and the central path.",
   "What is the duality gap on the central path, and why does that "
   "matter?",
   "Why did interior point change linear programming, and what does "
   "simplex still win at?",
   "Give four situations and the method for each.",
 ],
},

]
