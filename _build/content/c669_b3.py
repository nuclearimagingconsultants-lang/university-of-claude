# -*- coding: utf-8 -*-
"""CSCE 669 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Stochastic and Large-Scale Methods",
 "subtitle": "When you cannot afford a full gradient.",
 "question": "What happens when each gradient is only an estimate?",
 "outcomes": [
     "State SGD's convergence rate and why it is what it is.",
     "Explain the noise floor and why the step size must decay.",
     "Explain variance reduction and when it applies.",
     "Explain coordinate descent and when it wins.",
     "Connect the theory to CSCE 636's practice honestly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The trade",
   "blurb": "Cheap noisy steps against expensive exact ones."},

  {"t": "callout", "title": "SGD trades accuracy per step for steps per second",
   "kind": "The bargain",
   "body": ["<b>A full gradient over n examples costs n times a single "
            "example's gradient</b> and gives one step.",
            "<b>A stochastic gradient costs one</b> and gives one step "
            "— n times as many steps for the same work.",
            "<b>Each step is worse, and there are far more of them.</b> "
            "For large n that trade is overwhelmingly favourable in the "
            "early phase.",
            "<b>But not in the late phase.</b> <b>The noise does not "
            "shrink as you approach the optimum</b>, so progress stalls "
            "at a noise floor — which is why the step size must "
            "decay (Part 2)."]},

  {"t": "table", "kicker": "Rates", "title": "Deterministic against stochastic",
   "header": ["Setting", "Rate in iterations", "Rate in gradient evaluations"],
   "widths": [3.0, 3.8, 5.3],
   "rows": [
     ["<b>GD, strongly convex</b>", "<b>Linear \u2014 log(1/\u03b5)</b>", "<b>n \u00b7 \u03ba log(1/\u03b5)</b>"],
     ["<b>SGD, strongly convex</b>", "<b>O(1/k) \u2014 sublinear</b>", "<b>O(1/\u03b5) \u2014 INDEPENDENT of n</b>"],
     ["<b>SGD, convex</b>", "O(1/\u221ak)", "O(1/\u03b5&#178;)"],
     ["<b>SVRG / SAGA</b>", "<b>Linear</b>", "<b>(n + \u03ba) log(1/\u03b5)</b>"],
   ],
   "footnote": "<b>The second column is the important one.</b> SGD's cost "
               "per unit of accuracy does not grow with the dataset, which "
               "is why it is the method for large n.",
   "note": "Measuring in gradient evaluations rather than iterations is "
           "what makes SGD look good."},

  {"t": "section", "label": "Part 2", "title": "The noise floor",
   "blurb": "Why the step size must decay."},

  {"t": "callout", "title": "A constant step size converges to a ball, not a point",
   "kind": "The result that explains schedules",
   "body": ["<b>With a fixed step η, SGD converges to a "
            "neighbourhood of the optimum whose radius is proportional to "
            "η times the gradient variance.</b>",
            "<b>It then bounces around inside that ball "
            "indefinitely</b> — more iterations do not help.",
            "<b>So reduce η to shrink the ball.</b> The classical "
            "Robbins–Monro conditions are Σηₖ = "
            "∞ and Σηₖ² &lt; ∞ "
            "— large enough to travel anywhere, small enough to settle.",
            "<b>This is the theoretical content of CSCE 636's "
            "schedules</b> — <b>'explore then exploit' is 'traverse the "
            "space, then shrink the noise ball'</b>, now with a quantity "
            "attached."]},

  {"t": "callout", "title": "Larger batches shrink the noise, at a cost",
   "kind": "The other lever",
   "body": ["<b>Gradient variance falls as 1/B with batch size B</b>, so "
            "the noise ball shrinks as the batch grows.",
            "<b>But the cost per step grows linearly in B</b>, so the "
            "trade is not free — and past a point the variance reduction "
            "stops buying anything.",
            "<b>That point is the 'critical batch size'</b>, which is "
            "measurable and problem-dependent, and beyond it you are "
            "paying for steps that are no better.",
            "<b>And the linear scaling rule</b> — double the batch, "
            "double the learning rate — <b>holds approximately up to that "
            "point and fails beyond it</b>, which is why very large batch "
            "training needs warmup and LARS (CSCE 636 M08)."]},

  {"t": "section", "label": "Part 3", "title": "Variance reduction",
   "blurb": "Getting linear convergence back."},

  {"t": "code", "kicker": "SVRG", "title": "Using a stale full gradient as a control variate",
   "lang": "text", "code": """
  THE PROBLEM: SGD's variance does not vanish near the optimum,
  so it cannot converge linearly.

  SVRG: occasionally compute a FULL gradient at a snapshot point
  x~, then correct each stochastic gradient with it:

      g = grad f_i(x) - grad f_i(x~) + grad F(x~)
                        \\___________________________/
                              control variate

  UNBIASED (the correction has expectation zero) and its
  VARIANCE SHRINKS as x approaches x~ and both approach x*.

  SO: linear convergence, with (n + kappa) log(1/eps) gradient
  evaluations -- better than both GD and SGD when n and kappa
  are comparable.

  WHERE IT APPLIES
    finite sums with a FIXED dataset, which is exactly the
    empirical risk minimisation of CSCE 633.

  WHERE IT DOES NOT
    streaming or infinite data (no full gradient exists), and
    deep learning -- where it reliably underperforms plain SGD,
    for reasons still debated.
""",
   "caption": "<b>A beautiful result that does not help deep learning</b>, "
              "which is worth stating rather than implying.",
   "note": "Honesty about where the theory stops being useful matters "
           "here."},

  {"t": "section", "label": "Part 4", "title": "Coordinate descent",
   "blurb": "One variable at a time."},

  {"t": "callout", "title": "Coordinate descent wins when a single coordinate is cheap",
   "kind": "When this is the right method",
   "body": ["<b>Update one coordinate at a time, exactly, holding the "
            "others fixed.</b>",
            "<b>For the lasso, each coordinate update has a closed "
            "form</b> — soft thresholding again (Module 05 §3) "
            "— and costs O(n) rather than O(np).",
            "<b>So it is the standard method for the lasso and for "
            "elastic net</b>, and it is what <code>glmnet</code> and "
            "scikit-learn use.",
            "<b>It also handles non-smooth <i>separable</i> penalties "
            "naturally</b>, which is exactly the L1 case — <b>and fails "
            "on non-separable ones</b>, such as the fused lasso, because "
            "a single coordinate cannot move without violating the "
            "coupling."]},

  {"t": "bullets", "kicker": "Summary", "title": "Which large-scale method",
   "items": [
     "<b>Huge n, moderate accuracy wanted: SGD</b> with a decaying "
     "schedule.",
     "",
     "<b>Fixed finite sum, high accuracy wanted: SVRG or SAGA</b> "
     "\u2014 if it is convex.",
     "",
     "<b>Separable non-smooth penalty: coordinate descent.</b>",
     "",
     "<b>Composite objective, structure to split: ADMM</b> "
     "(Module 06 §3).",
     "",
     "<b>And deep learning: SGD with momentum, or Adam</b> \u2014 where "
     "the theory offers guidance rather than guarantees.",
   ],
   "footnote": "<b>The gap between the convex theory and deep learning "
               "practice is real</b> and is narrowest at the "
               "learning-rate schedule."},
 ],
 "takeaways": [
   "SGD trades accuracy per step for far more steps, and its cost per unit "
   "of accuracy is independent of the dataset size.",
   "With a constant step size SGD converges to a ball around the optimum "
   "whose radius scales with the step and the gradient variance.",
   "Robbins\u2013Monro's conditions \u2014 steps summing to infinity with "
   "squares summing finitely \u2014 are the theoretical content of "
   "CSCE 636's schedules.",
   "Batch size reduces variance as 1/B at linear cost, and past the "
   "critical batch size the reduction stops buying anything.",
   "SVRG uses a stale full gradient as a control variate to recover linear "
   "convergence \u2014 and it reliably underperforms plain SGD in deep "
   "learning.",
   "Coordinate descent suits separable non-smooth penalties and is what "
   "lasso solvers actually use.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The trade"),
  ("callout", "SGD trades accuracy per step for steps per second",
   ["<b>A full gradient over n training examples costs n times a single "
    "example's gradient and produces one parameter update.</b> Every "
    "example is consulted before anything moves.",
    "<b>A stochastic gradient costs one example's gradient and also "
    "produces one update</b> \u2014 so for the same computational budget "
    "you take n times as many steps.",
    "<b>Each individual step is worse, and there are vastly more of "
    "them.</b> For large n that trade is overwhelmingly favourable in the "
    "early phase, where any descent direction is useful and precision is "
    "wasted.",
    "<b>But it is unfavourable in the late phase.</b> <b>The gradient "
    "noise does not shrink as the iterate approaches the optimum</b> "
    "\u2014 at x* the full gradient is zero and the individual gradients "
    "are not \u2014 so progress stalls at a noise floor (&sect;2). <b>The "
    "method that is best early is not the method that is best late</b>, "
    "which is the whole reason schedules exist."]),
  ("table", ["Setting", "Rate per iteration",
             "Rate per <i>gradient evaluation</i>"],
   [["<b>Gradient descent, strongly convex</b>",
     "<b>Linear \u2014 log(1/&epsilon;) iterations</b> (Module 05 "
     "&sect;1).",
     "<b>n &middot; &kappa; log(1/&epsilon;)</b> \u2014 every iteration "
     "costs n gradients."],
    ["<b>SGD, strongly convex</b>",
     "<b>O(1/k) \u2014 sublinear, which looks much worse.</b>",
     "<b>O(1/&epsilon;), independent of n.</b> <b>This is the row that "
     "matters</b> \u2014 the cost to reach a given accuracy does not grow "
     "with the dataset at all."],
    ["<b>SGD, convex but not strongly</b>", "O(1/&radic;k).",
     "O(1/&epsilon;&#178;)."],
    ["<b>SVRG, SAGA (variance-reduced)</b>", "<b>Linear.</b>",
     "<b>(n + &kappa;) log(1/&epsilon;)</b> \u2014 better than both when "
     "n and &kappa; are comparable (&sect;3)."]],
   [0.26, 0.30, 0.44]),
  ("p", "<b>Measuring in gradient evaluations rather than in iterations is "
        "what makes SGD look good</b>, and it is the honest accounting "
        "because gradient evaluations are what cost money. <b>Comparing "
        "iteration counts between a full-batch and a stochastic method is "
        "meaningless</b>, and it is done surprisingly often."),

  ("h1", "2 &nbsp; The noise floor"),
  ("callout", "A constant step size converges to a ball, not a point",
   ["<b>With a fixed step size &eta;, SGD converges to a neighbourhood of "
    "the optimum whose radius is proportional to &eta; times the gradient "
    "variance</b> \u2014 and then stays there.",
    "<b>It bounces around inside that ball indefinitely.</b> Additional "
    "iterations at the same step size do not improve the solution; they "
    "move it around within the same region, which is exactly what a loss "
    "curve that has flattened at a disappointing value looks like.",
    "<b>So reduce &eta; to shrink the ball.</b> The classical "
    "<b>Robbins\u2013Monro conditions</b> are "
    "&Sigma;&eta;<sub>k</sub> = &infin; (the steps must sum to infinity, "
    "so the iterate can reach anywhere in the space) and "
    "&Sigma;&eta;<sub>k</sub>&#178; &lt; &infin; (the squares must sum "
    "finitely, so the noise is eventually suppressed). A schedule of "
    "1/k satisfies both.",
    "<b>This is the theoretical content of CSCE 636 Module 03's learning "
    "rate schedules.</b> <b>'Explore then exploit' is precisely 'traverse "
    "the space while the ball is large, then shrink the ball'</b> \u2014 "
    "and the informal framing there now has a quantity attached to it. "
    "<b>Decaying too early traps you with a small ball far from the "
    "optimum; never decaying leaves you orbiting it forever.</b>"]),
  ("callout", "Larger batches shrink the noise, at a cost",
   ["<b>Gradient variance falls as 1/B with batch size B</b> \u2014 "
    "averaging B independent estimates \u2014 so the noise ball of the "
    "previous callout shrinks as the batch grows.",
    "<b>But the cost per step grows linearly in B</b>, so the trade is not "
    "free: doubling the batch halves the variance and doubles the work per "
    "step. <b>Past some point the variance is no longer what limits "
    "progress</b>, and further batch growth buys nothing.",
    "<b>That point is the <i>critical batch size</i></b>, it is measurable "
    "for a given problem, and beyond it you are paying linearly for steps "
    "that are not meaningfully better \u2014 which is the regime very large "
    "distributed training runs operate in, and why their scaling "
    "efficiency falls off.",
    "<b>And the linear scaling rule \u2014 double the batch, double the "
    "learning rate \u2014 holds approximately up to that point and fails "
    "beyond it.</b> <b>Which is why very large batch training requires "
    "warmup and layer-wise rate scaling</b> (CSCE 636 Module 08 "
    "&sect;2): the naive rule puts the step size outside the stable range "
    "that Module 05 &sect;1's smoothness constant permits."]),

  ("break",),
  ("h1", "3 &nbsp; Variance reduction"),
  ("code", """THE PROBLEM: SGD's gradient variance does not vanish near the
optimum, so it cannot converge linearly.

SVRG: occasionally compute a FULL gradient at a snapshot x~,
then correct each stochastic gradient with it:

    g = grad f_i(x) - grad f_i(x~) + grad F(x~)
                      \\__________________________/
                            control variate

UNBIASED -- the correction has expectation zero -- and its
VARIANCE SHRINKS as x approaches x~ and both approach x*.

RESULT: linear convergence, at (n + kappa) log(1/eps) gradient
evaluations. Better than GD and SGD when n and kappa are
comparable.

WHERE IT APPLIES
  finite sums over a FIXED dataset -- exactly the empirical
  risk minimisation of CSCE 633.

WHERE IT DOES NOT
  streaming or infinite data (no full gradient exists), and
  DEEP LEARNING, where it reliably underperforms plain SGD for
  reasons still debated."""),
  ("p", "<b>It is a beautiful result that does not help deep learning</b>, "
        "and saying so is better than implying otherwise. The leading "
        "explanations are that the snapshot goes stale too quickly when "
        "the iterate moves far, that data augmentation makes the 'fixed "
        "finite sum' assumption false, and that <b>SGD's noise may be "
        "beneficial rather than merely tolerated</b> (CSCE 636 "
        "Module 03 &sect;2) \u2014 in which case reducing it is "
        "counterproductive. <b>None is settled</b>, and the honest summary "
        "is that the method works where its assumptions hold and the "
        "assumptions do not hold in the setting that currently matters "
        "most."),

  ("h1", "4 &nbsp; Coordinate descent"),
  ("callout", "Coordinate descent wins when a single coordinate is cheap",
   ["<b>Update one coordinate at a time, exactly, holding all the others "
    "fixed</b>, and cycle (or choose randomly). Each update solves a "
    "one-dimensional problem.",
    "<b>For the lasso, each coordinate update has a closed form</b> "
    "\u2014 <b>soft thresholding again</b> (Module 05 &sect;3) \u2014 and "
    "costs O(n) rather than the O(np) of a full gradient step. <b>With "
    "active-set tracking, most coordinates are zero and are skipped "
    "entirely</b>, which is where the real speed comes from.",
    "<b>So it is the standard method for the lasso and elastic net</b>, "
    "and it is what <code>glmnet</code> and scikit-learn's coordinate "
    "descent solver implement \u2014 it is why fitting a full "
    "regularisation path is so fast (CSCE 633 Module 04 &sect;1).",
    "<b>It handles non-smooth <i>separable</i> penalties naturally</b>, "
    "which is exactly the &ell;<sub>1</sub> case: the penalty decomposes "
    "across coordinates, so a one-dimensional subproblem is well posed. "
    "<b>And it fails on non-separable penalties</b> \u2014 the fused lasso, "
    "group lasso with overlaps \u2014 <b>because no single coordinate can "
    "move without violating a coupling</b>, so the method stalls at a "
    "non-optimal point. <b>Separability is the precondition, and checking "
    "it is the first thing to do.</b>"]),
  ("ul", ["<b>Huge n, moderate accuracy sufficient: SGD</b> with a "
          "decaying schedule satisfying &sect;2's conditions.",
          "<b>Fixed finite sum, high accuracy required, convex: SVRG or "
          "SAGA</b> \u2014 where the linear rate genuinely pays.",
          "<b>Separable non-smooth penalty: coordinate descent</b> "
          "(&sect;4).",
          "<b>Composite objective with exploitable structure: ADMM</b> "
          "(Module 06 &sect;3).",
          "<b>And deep learning: SGD with momentum, or AdamW</b> \u2014 "
          "<b>where this course's theory offers guidance rather than "
          "guarantees</b>. <b>The gap between the convex theory and deep "
          "learning practice is real</b>, and it is narrowest at the "
          "learning-rate schedule (&sect;2) and widest at the question of "
          "why the resulting solutions generalise (CSCE 636 Module 03 "
          "&sect;4)."]),
 ],
 "resources": [
   ("Bottou, Curtis & Nocedal &mdash; Optimization Methods for Large-Scale "
    "Machine Learning (free)",
    "https://arxiv.org/abs/1606.04838",
    "<b>The reference for this whole module.</b> The clearest treatment of "
    "the &sect;1 trade and the &sect;2 noise analysis."),
   ("Johnson & Zhang &mdash; Accelerating Stochastic Gradient Descent "
    "using Predictive Variance Reduction (SVRG) (free)",
    "https://papers.nips.cc/paper/2013/hash/ac1dd209cbcc5e5d1c6e28598e8cbbe8-Abstract.html",
    "The &sect;3 method, with the control variate argument."),
   ("Goyal et al. &mdash; Accurate, Large Minibatch SGD (free)",
    "https://arxiv.org/abs/1706.02677",
    "<b>The linear scaling rule of &sect;2</b>, its warmup requirement, "
    "and where it breaks."),
   ("Friedman, Hastie & Tibshirani &mdash; Regularization Paths for "
    "Generalized Linear Models via Coordinate Descent (free)",
    "https://www.jstatsoft.org/article/view/v033i01",
    "<b>The &sect;4 method as implemented in glmnet</b>, including the "
    "active set and path-following tricks."),
 ],
 "exercises": [
   "<b>Compare GD and SGD on the same problem</b>, plotting error against "
   "gradient evaluations rather than iterations.",
   "<b>Run SGD with a constant step size</b> and plot the iterate's "
   "distance from the optimum. Show it plateaus.",
   "<b>Vary the step size and show the plateau radius scales with it.</b>",
   "Add a 1/k schedule and show convergence to the optimum.",
   "<b>Measure gradient variance against batch size</b> and confirm the "
   "1/B relationship.",
   "<b>Find the critical batch size</b> for your problem by plotting steps "
   "to a target loss against batch size.",
   "Implement SVRG and compare against SGD on a convex finite sum.",
   "<b>Then try SVRG on a small neural network</b> and report what "
   "happens.",
   "<b>Implement coordinate descent for the lasso</b> and compare against "
   "proximal gradient.",
   "Apply coordinate descent to a fused lasso and show it stalls.",
 ],
 "selfcheck": [
   "What does SGD trade, and why is the gradient-evaluation column the "
   "right one?",
   "Why does SGD's noise not vanish near the optimum?",
   "What does a constant step size converge to, and what are the "
   "Robbins\u2013Monro conditions?",
   "How does batch size affect variance and cost, and what is the critical "
   "batch size?",
   "Explain SVRG's control variate and the rate it achieves.",
   "Where does SVRG not apply, and what are the explanations?",
   "When does coordinate descent win, and what precondition does it need?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Integer Programming",
 "subtitle": "NP-hard, and solved every day.",
 "question": "How do solvers handle a problem that is intractable?",
 "outcomes": [
     "Formulate with integer and binary variables.",
     "Explain branch and bound and what makes it work.",
     "Explain cutting planes and strengthening.",
     "Explain the integrality gap and formulation strength.",
     "Model the standard logical constructs.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Branch and bound",
   "blurb": "Divide, bound, prune."},

  {"t": "code", "kicker": "Branch and bound", "title": "The algorithm, and why it terminates early",
   "lang": "text", "code": """
  solve the LP RELAXATION (drop integrality)
      -> a LOWER bound on the true minimum (Module 04: weak duality)
      -> if the solution happens to be integral, you are DONE

  otherwise pick a fractional variable x_j = 3.4 and BRANCH:
      child A:  x_j <= 3        child B:  x_j >= 4
      -- the two children partition the feasible region and
         exclude the current fractional point

  maintain an INCUMBENT: the best integral solution found so far,
  which is an UPPER bound.

  PRUNE a node when:
      its LP bound exceeds the incumbent   -- cannot contain better
      its LP is infeasible                 -- nothing there
      its LP solution is integral          -- update the incumbent

  THE GAP between the best remaining bound and the incumbent is
  reported continuously. You can STOP EARLY with a guarantee:
  "within 2% of optimal" is a complete, checkable claim.

  THAT is why NP-hardness does not prevent use.
""",
   "caption": "<b>Stopping early with a proven gap is what makes integer "
              "programming practical</b> \u2014 you rarely need the exact "
              "optimum, and you always need to know how far off you are.",
   "note": "The early-stopping-with-a-bound property is the practical "
           "heart of the module."},

  {"t": "callout", "title": "The bound quality decides everything",
   "kind": "Where the performance is",
   "body": ["<b>A tight relaxation prunes aggressively and the tree stays "
            "small.</b> A loose one prunes nothing and the tree is "
            "exponential.",
            "<b>So formulation strength matters more than anything "
            "else</b> — two correct formulations of the same problem can "
            "differ by orders of magnitude in solve time.",
            "<b>Branching choice matters too:</b> which fractional "
            "variable to split on determines the tree shape, and "
            "pseudo-cost branching is the standard heuristic.",
            "<b>And a good incumbent early helps enormously</b>, because "
            "pruning requires something to prune against — which is why "
            "solvers run primal heuristics before and during the search."]},

  {"t": "section", "label": "Part 2", "title": "Cutting planes",
   "blurb": "Tightening the relaxation."},

  {"t": "callout", "title": "A cut removes fractional points without removing integer ones",
   "kind": "The idea",
   "body": ["<b>Add an inequality valid for every integer-feasible "
            "point but violated by the current fractional LP "
            "solution.</b>",
            "<b>The relaxation gets tighter, the bound improves, and no "
            "feasible integer solution is lost.</b>",
            "<b>Gomory cuts are derived mechanically from the simplex "
            "tableau</b> and always exist — pure cutting-plane methods "
            "terminate finitely, and converge too slowly to use alone.",
            "<b>So modern solvers do branch <i>and</i> cut:</b> generate "
            "cuts at nodes, then branch. <b>Problem-specific cuts — "
            "clique, cover, flow — are far stronger than general "
            "ones.</b>"]},

  {"t": "eq", "kicker": "Gap", "title": "Integrality gap and formulation strength",
   "eqs": [
     ("gap = (IP optimum − LP optimum) / IP optimum",
      "How much the relaxation understates the true optimum."),
     ("The CONVEX HULL of the integer points is the ideal formulation",
      "Its LP relaxation is exact — the gap is zero and no branching is "
      "needed."),
     ("It usually has exponentially many facets",
      "So you generate the useful ones on demand rather than writing "
      "them all."),
   ],
   "caption": "<b>Every valid inequality you add moves the relaxation "
              "toward the convex hull.</b> That is what cuts are for, "
              "geometrically.",
   "note": "The convex hull framing unifies cuts and formulation "
           "strength."},

  {"t": "section", "label": "Part 3", "title": "Modelling",
   "blurb": "The logical constructs, and the big-M trap."},

  {"t": "code", "kicker": "Modelling", "title": "Logic as linear constraints",
   "lang": "text", "code": """
  WITH BINARY y:

    either-or         x <= u*y,   x' <= u*(1-y)
    if-then           y1 <= y2            ("y1 implies y2")
    at most k of n    sum y_i <= k
    fixed charge      cost = f*y + c*x,   x <= M*y
                      -- pay f only if x > 0
    piecewise linear  SOS2 constraints, or binaries per segment

  THE BIG-M TRAP
      "x <= M*y" enforces x = 0 when y = 0, for any sufficiently
      large M. It is correct for ANY large M.

      BUT a loose M makes the LP RELAXATION WEAK. With M = 10^6
      and x <= 10, setting y = 0.00001 satisfies the constraint
      and the relaxation learns nothing. The bound is useless and
      the tree explodes.

      USE THE SMALLEST VALID M. Derive it from the problem's
      actual bounds. This single discipline routinely changes
      solve times by orders of magnitude, and it is the most
      common modelling error in practice.
""",
   "caption": "<b>Big-M is correct for any large M and only useful for a "
              "tight one</b> \u2014 which is the clearest case of "
              "formulation strength mattering.",
   "note": "The big-M discipline is the single highest-value practical "
           "tip in this module."},

  {"t": "section", "label": "Part 4", "title": "In practice",
   "blurb": "What solvers do, and what you should."},

  {"t": "bullets", "kicker": "Practice", "title": "Getting an integer program solved",
   "items": [
     "<b>Tighten every big-M.</b> The highest-value single action "
     "available.",
     "",
     "<b>Break symmetry.</b> Identical items produce identical subtrees "
     "\u2014 add ordering constraints to explore each once.",
     "",
     "<b>Supply a good incumbent</b> from a heuristic, so pruning can "
     "begin immediately.",
     "",
     "<b>Set a gap tolerance and a time limit.</b> <b>Proving the last "
     "0.1% frequently costs more than the first 99.9%.</b>",
     "",
     "<b>And reformulate before tuning solver parameters</b> \u2014 the "
     "formulation is worth more than every parameter combined.",
   ],
   "footnote": "<b>Symmetry is the quiet killer:</b> n identical machines "
               "give n! equivalent solutions, all of which the tree will "
               "visit unless told not to."},

  {"t": "callout", "title": "What has made solvers fast",
   "kind": "The measured history",
   "body": ["<b>Between 1990 and 2020, integer programming solvers "
            "improved by a factor of roughly a million.</b>",
            "<b>Hardware contributed about a thousand of that. "
            "Algorithms contributed the other thousand.</b>",
            "<b>And the algorithmic gains were mostly cuts, presolve, "
            "and heuristics</b> — not a better branching rule or a "
            "faster LP solve.",
            "<b>So the practical lesson matches the theoretical one:</b> "
            "<b>strengthening the formulation is where the gains are</b>, "
            "whether the solver does it or you do."]},
 ],
 "takeaways": [
   "Branch and bound solves the relaxation for a lower bound, branches on a "
   "fractional variable, and prunes against an incumbent upper bound.",
   "The continuously-reported gap lets you stop early with a proven "
   "guarantee, which is why NP-hardness does not prevent practical use.",
   "Bound quality decides everything \u2014 two correct formulations of the "
   "same problem can differ by orders of magnitude.",
   "A cut is valid for every integer point and violated by the current "
   "fractional solution, moving the relaxation toward the convex hull.",
   "Big-M is correct for any large M and only useful for a tight one, which "
   "is the most common modelling error in practice.",
   "Solvers improved a millionfold in thirty years, split evenly between "
   "hardware and algorithms \u2014 and the algorithms were mostly cuts and "
   "presolve.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Branch and bound"),
  ("code", """solve the LP RELAXATION (drop integrality)
  -> a LOWER bound on the true minimum (Module 04, weak duality)
  -> if the solution is already integral, DONE

otherwise pick a fractional variable x_j = 3.4 and BRANCH
  child A:  x_j <= 3      child B:  x_j >= 4
  the children partition the region and exclude the fractional
  point

maintain an INCUMBENT -- the best integral solution so far,
which is an UPPER bound

PRUNE a node when
  its LP bound exceeds the incumbent   -- nothing better inside
  its LP is infeasible                 -- nothing there at all
  its LP solution is integral          -- update the incumbent

The GAP between the best remaining bound and the incumbent is
reported CONTINUOUSLY. You can stop early with a guarantee:
"within 2% of optimal" is a complete, checkable claim."""),
  ("p", "<b>Stopping early with a proven gap is what makes integer "
        "programming practical.</b> You rarely need the exact optimum "
        "\u2014 a schedule 1% from optimal is operationally "
        "indistinguishable from the best one \u2014 <b>and you always need "
        "to know how far off you are</b>. <b>That combination is why "
        "NP-hardness does not prevent daily industrial use</b> "
        "(Module 01 &sect;2), and it is the practical heart of this "
        "module."),
  ("callout", "The bound quality decides everything",
   ["<b>A tight relaxation prunes aggressively and the search tree stays "
    "small.</b> A loose one prunes almost nothing and the tree grows "
    "exponentially \u2014 the difference between seconds and never.",
    "<b>So formulation strength matters more than anything else.</b> "
    "<b>Two mathematically correct formulations of the same problem can "
    "differ by orders of magnitude in solve time</b>, purely through the "
    "quality of their relaxations \u2014 which means modelling is not a "
    "preliminary to solving but the largest part of it (&sect;3, "
    "Module 12).",
    "<b>Branching choice matters too.</b> Which fractional variable to "
    "split on determines the tree's shape; <b>pseudo-cost branching</b> "
    "\u2014 estimating each variable's historical effect on the bound "
    "\u2014 is the standard heuristic and is substantially better than "
    "picking the most fractional variable.",
    "<b>And obtaining a good incumbent early helps enormously</b>, because "
    "pruning requires something to prune <i>against</i> \u2014 with no "
    "incumbent, no node can be discarded. <b>Which is why solvers run "
    "primal heuristics before and throughout the search</b>, spending real "
    "time looking for merely good solutions in order to make the proof of "
    "optimality cheap."]),

  ("h1", "2 &nbsp; Cutting planes"),
  ("callout", "A cut removes fractional points and no integer ones",
   ["<b>Add an inequality that is satisfied by every integer-feasible "
    "point but violated by the current fractional LP solution.</b> The cut "
    "is <i>valid</i> (loses no real solutions) and <i>separating</i> (cuts "
    "off the current one).",
    "<b>The relaxation becomes tighter, the bound improves, and nothing "
    "feasible is lost.</b> Re-solving the LP gives a better bound and "
    "possibly an integral solution.",
    "<b>Gomory cuts are derived mechanically from the simplex tableau</b> "
    "and always exist, and <b>a pure cutting-plane method provably "
    "terminates</b> \u2014 but converges so slowly, and suffers such "
    "numerical difficulty, that it is unusable alone. This was known by "
    "1960 and the method was abandoned for thirty years.",
    "<b>So modern solvers do branch <i>and</i> cut:</b> generate cuts at "
    "the root and at nodes to tighten the local relaxation, then branch. "
    "<b>Problem-specific cuts \u2014 clique, cover, flow cover, "
    "mixed-integer rounding \u2014 are far stronger than general-purpose "
    "ones</b>, which is why a solver that recognises your problem's "
    "structure vastly outperforms one that does not, and why stating "
    "structure explicitly in the model pays."]),
  ("eq", "gap = (z<sub>IP</sub> &minus; z<sub>LP</sub>) / "
         "z<sub>IP</sub>"),
  ("p", "<b>The integrality gap measures how far the relaxation understates "
        "the true optimum</b>, and it is the quantity that predicts solve "
        "difficulty. <b>The ideal formulation is the convex hull of the "
        "integer feasible points</b> \u2014 its LP relaxation has gap zero, "
        "every vertex is integral, and no branching is required at all "
        "(which is exactly the totally unimodular case of Module 03 "
        "&sect;3, where the hull is described by the original "
        "constraints). <b>For a general problem the hull has exponentially "
        "many facets</b>, so it cannot be written down \u2014 <b>and every "
        "valid inequality you add moves the relaxation toward it.</b> "
        "<b>That is what cuts are for, geometrically</b>, and it unifies "
        "cuts, formulation strength, and the gap under one picture."),

  ("break",),
  ("h1", "3 &nbsp; Modelling with integers"),
  ("code", """WITH BINARY y:

  either-or        x <= u*y,  x' <= u*(1-y)
  if-then          y1 <= y2          ("y1 implies y2")
  at most k of n   sum y_i <= k
  fixed charge     cost = f*y + c*x,  x <= M*y
                   -- pay the fixed cost f only if x > 0
  piecewise linear SOS2 constraints, or a binary per segment

THE BIG-M TRAP
  "x <= M*y" forces x = 0 when y = 0, for ANY sufficiently
  large M. It is CORRECT for any large M.

  BUT a loose M makes the LP RELAXATION WEAK. With M = 10^6
  and x bounded by 10 in reality, setting y = 0.00001 satisfies
  the constraint, the relaxation learns nothing, the bound is
  useless, and the tree explodes.

  USE THE SMALLEST VALID M, derived from the problem's real
  bounds. This single discipline routinely changes solve times
  by orders of magnitude."""),
  ("p", "<b>Big-M is the clearest available case of formulation strength "
        "mattering:</b> the constraint is logically correct for any large "
        "M and <i>useful</i> only for a tight one, so correctness and "
        "performance come apart completely. <b>It is the most common "
        "modelling error in practice</b>, partly because the symptom "
        "\u2014 a solver that runs forever on a correct model \u2014 does "
        "not point at the cause."),

  ("h1", "4 &nbsp; In practice"),
  ("ul", ["<b>Tighten every big-M.</b> Derive each from the problem's real "
          "bounds rather than picking a safe large number. <b>The "
          "highest-value single action available</b> (&sect;3).",
          "<b>Break symmetry.</b> <b>n identical machines, bins, or "
          "shifts produce n! equivalent solutions</b>, and the search tree "
          "will visit all of them unless prevented \u2014 add ordering "
          "constraints (machine 1's load &ge; machine 2's, or lexicographic "
          "ordering on assignment vectors) so each distinct solution is "
          "explored once. <b>Symmetry is the quiet killer of integer "
          "models</b>, and it is invisible until you look for it.",
          "<b>Supply a good incumbent</b> from a heuristic or from a "
          "previous run, so that pruning can begin at the first node rather "
          "than after the solver has found something itself.",
          "<b>Set a gap tolerance and a time limit.</b> <b>Proving the "
          "last 0.1% of optimality frequently costs more than finding the "
          "first 99.9%</b>, because the remaining nodes are precisely the "
          "ones the bound cannot distinguish. A 1% tolerance is usually "
          "generous and usually free.",
          "<b>And reformulate before tuning solver parameters.</b> <b>The "
          "formulation is worth more than every parameter setting "
          "combined</b>, and parameter tuning is where people reach first "
          "because it feels like action."]),
  ("callout", "What has actually made solvers fast",
   ["<b>Between roughly 1990 and 2020, integer programming solvers improved "
    "by a factor of about a million on standard benchmark sets.</b> This "
    "has been measured repeatedly by running old solver versions on modern "
    "hardware.",
    "<b>Hardware contributed roughly a factor of a thousand. The "
    "algorithms contributed the other thousand.</b> <b>The two are "
    "comparable</b>, which is an unusual and striking result \u2014 in most "
    "fields hardware dominates.",
    "<b>And the algorithmic gains were mostly cutting planes, presolve, "
    "and primal heuristics</b> \u2014 not a better branching rule, not a "
    "faster LP solve, and not a fundamentally new search strategy. "
    "<b>The gains came from making each node's bound tighter and from "
    "finding good solutions sooner.</b>",
    "<b>So the practical lesson matches the theoretical one:</b> "
    "<b>strengthening the formulation is where the gains are</b>, whether "
    "the solver's presolve does it automatically or you do it by hand. "
    "<b>And it is a reason to keep solvers updated</b>, which organisations "
    "frequently do not."]),
 ],
 "resources": [
   ("MIT 15.093 &mdash; integer programming lectures (free, OCW)",
    "https://ocw.mit.edu/courses/15-093j-optimization-methods-fall-2009/",
    "<b>Branch and bound, cutting planes, and formulation strength</b> "
    "\u2014 the core of &sect;1 and &sect;2."),
   ("Wolsey &mdash; Integer Programming",
    "https://www.wiley.com/en-us/Integer+Programming%2C+2nd+Edition-p-9781119606536",
    "The standard reference, strong on formulation and on the convex hull "
    "view of &sect;2."),
   ("Klotz & Newman &mdash; Practical Guidelines for Solving Difficult "
    "Mixed Integer Linear Programs (free)",
    "https://www.sciencedirect.com/science/article/pii/S1876735413000020",
    "<b>The &sect;4 checklist, from solver developers.</b> The big-M and "
    "symmetry advice is here with worked examples."),
   ("Bixby &mdash; Solving Real-World Linear Programs, and the MIP "
    "benchmark histories (free)",
    "https://plato.asu.edu/bench.html",
    "<b>The &sect;4 callout's measurements</b>, and current solver "
    "benchmarks."),
 ],
 "exercises": [
   "<b>Implement branch and bound</b> for small integer programs and "
   "report node counts.",
   "<b>Solve the LP relaxation and measure the integrality gap</b> on "
   "several instances.",
   "<b>Formulate one problem two ways</b> \u2014 a weak and a strong "
   "formulation \u2014 and compare node counts and solve times.",
   "Implement a simple cover cut and measure its effect on the bound.",
   "<b>Set up a big-M model with a loose M</b>, then tighten it, and "
   "report the solve times.",
   "<b>Construct a symmetric instance</b> with identical items and measure "
   "the tree size with and without symmetry-breaking constraints.",
   "Supply an incumbent from a greedy heuristic and measure the effect.",
   "<b>Plot the gap against time</b> for a hard instance and identify "
   "where the last 1% begins.",
   "Model three logical constructs from &sect;3 and verify each.",
   "<b>Compare an old solver version against a current one</b> on the "
   "same instances, if you can obtain both.",
 ],
 "selfcheck": [
   "Describe branch and bound and name the three pruning conditions.",
   "Why can you stop early with a guarantee, and why does that matter?",
   "What decides the tree size?",
   "What is a cutting plane, and what two properties must it have?",
   "Define the integrality gap and relate cuts to the convex hull.",
   "Give five logical constructs as linear constraints.",
   "Explain the big-M trap.",
   "Give five practical steps for a hard integer program.",
   "What has made solvers fast, and in what proportion?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Approximation and Relaxation",
 "subtitle": "Provably close, provably fast.",
 "question": "If you cannot solve it exactly, how close can you "
             "guarantee?",
 "outcomes": [
     "Define an approximation ratio and a PTAS.",
     "Derive a guarantee from an LP relaxation and rounding.",
     "Apply randomised rounding and its analysis.",
     "Explain semidefinite relaxation and the Goemans\u2013Williamson "
     "result.",
     "Explain hardness of approximation.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The framework",
   "blurb": "Guarantees relative to an optimum you cannot compute."},

  {"t": "callout", "title": "The guarantee is against a bound, not against the optimum",
   "kind": "How the trick works",
   "body": ["<b>You cannot compare your answer to the optimum, because "
            "you cannot compute the optimum.</b>",
            "<b>So compare it to a <i>bound</i> on the optimum</b> — "
            "usually the LP relaxation's value, which is a lower bound by "
            "weak duality (Module 04 §1).",
            "<b>If your solution is within a factor α of the "
            "bound, it is within α of the optimum</b>, because the "
            "optimum lies between them.",
            "<b>That is the entire mechanism of approximation "
            "analysis.</b> <b>Every ratio in this module is proved against "
            "a relaxation</b>, which is why Module 04 had to come "
            "first."]},

  {"t": "table", "kicker": "Classes", "title": "Approximability, from best to worst",
   "header": ["Class", "Means", "Example"],
   "widths": [2.5, 4.4, 5.2],
   "rows": [
     ["<b>FPTAS</b>", "<b>(1+\u03b5) in time polynomial in n and 1/\u03b5</b>", "<b>Knapsack</b>"],
     ["<b>PTAS</b>", "(1+\u03b5), polynomial in n for each fixed \u03b5", "Euclidean TSP"],
     ["<b>Constant factor</b>", "<b>Within a fixed \u03b1</b>", "<b>Vertex cover (2), MAX-CUT (1.138)</b>"],
     ["<b>Logarithmic</b>", "Within O(log n)", "<b>Set cover \u2014 and that is optimal</b>"],
     ["<b>No constant</b>", "<b>No constant-factor approximation unless P = NP</b>", "<b>General TSP, max clique</b>"],
   ],
   "footnote": "<b>These classes are provably distinct</b> under standard "
               "assumptions, so the hierarchy is real rather than a "
               "reflection of current ignorance.",
   "note": "That the classes are provably separated is the striking "
           "part."},

  {"t": "section", "label": "Part 2", "title": "LP rounding",
   "blurb": "Solve the relaxation, then round."},

  {"t": "code", "kicker": "Vertex cover", "title": "A complete 2-approximation, in ten lines",
   "lang": "text", "code": """
  PROBLEM: choose a minimum-weight set of vertices touching
  every edge.

  INTEGER PROGRAM
      minimise  sum w_v x_v
      s.t.      x_u + x_v >= 1   for every edge (u,v)
                x_v in {0,1}

  RELAX x_v in [0,1]  and solve the LP.  Then ROUND:
      take v  if  x_v >= 1/2

  FEASIBLE: every edge has x_u + x_v >= 1, so at least one
  endpoint has x >= 1/2 and is taken. Every edge is covered.

  COST: rounding at most DOUBLES each variable, so
      ALG <= 2 * LP <= 2 * OPT
  because LP <= OPT (it is a relaxation of a minimisation).

  A 2-APPROXIMATION, PROVED, IN TEN LINES.

  And the analysis shows exactly where the factor 2 comes from:
  the threshold. The integrality gap of this formulation IS 2,
  so no better rounding of THIS LP exists.
""",
   "caption": "<b>The integrality gap bounds what any rounding of that "
              "relaxation can achieve</b> \u2014 to do better you need a "
              "stronger formulation.",
   "note": "This is the cleanest complete proof in the course; use it."},

  {"t": "callout", "title": "Randomised rounding, and why it analyses well",
   "kind": "The second technique",
   "body": ["<b>Treat the fractional value xᵥ as a "
            "<i>probability</i> and include v with that probability.</b>",
            "<b>The expected cost is exactly the LP value</b>, by "
            "linearity of expectation — which is why the analysis is so "
            "clean.",
            "<b>Feasibility holds only in expectation</b>, so you repeat "
            "or condition until it holds, and concentration bounds "
            "(CSCE 658's material) control the failure probability.",
            "<b>Set cover's O(log n) guarantee comes from exactly "
            "this</b> — round repeatedly, and after O(log n) rounds every "
            "element is covered with high probability."]},

  {"t": "section", "label": "Part 3", "title": "Semidefinite relaxation",
   "blurb": "A stronger relaxation, and a famous result."},

  {"t": "callout", "title": "Goemans\u2013Williamson: relax to vectors, round by a random hyperplane",
   "kind": "The most elegant result here",
   "body": ["<b>MAX-CUT asks for a partition maximising the weight of "
            "edges crossing it.</b> Assign each vertex ±1 — "
            "non-convex.",
            "<b>Relax: assign each vertex a unit <i>vector</i></b>, and "
            "maximise the same objective with inner products. <b>That is "
            "a semidefinite program</b> — convex, and solvable.",
            "<b>Then round with a random hyperplane</b> through the "
            "origin: vertices on each side form a partition.",
            "<b>The probability an edge is cut is θ/π</b>, "
            "where θ is the angle between its endpoints' vectors "
            "— and the ratio of that to the SDP term is at least 0.878. "
            "<b>A 0.878-approximation, from geometry.</b>"]},

  {"t": "callout", "title": "And 0.878 is probably optimal",
   "kind": "The hardness side",
   "body": ["<b>Under the Unique Games Conjecture, no polynomial "
            "algorithm beats 0.878 for MAX-CUT.</b>",
            "<b>So the Goemans–Williamson constant — which looks "
            "like an artifact of the analysis — is the true "
            "boundary.</b>",
            "<b>That is a remarkable convergence</b> of an algorithmic "
            "result and a hardness result on an arbitrary-looking "
            "number.",
            "<b>UGC is unproved</b> and widely believed, and a great deal "
            "of approximation hardness is conditional on it — which is "
            "worth stating when citing these results."]},

  {"t": "section", "label": "Part 4", "title": "Hardness",
   "blurb": "Why some ratios are impossible."},

  {"t": "bullets", "kicker": "Hardness", "title": "Inapproximability results worth knowing",
   "items": [
     "<b>Set cover:</b> no better than (1\u2212o(1))\u00b7ln n unless "
     "P = NP. <b>And the greedy algorithm achieves it</b> \u2014 the "
     "simplest method is optimal.",
     "",
     "<b>Max clique:</b> no n^(1\u2212\u03b5) approximation. Essentially "
     "inapproximable.",
     "",
     "<b>General TSP:</b> no constant factor \u2014 but <b>metric TSP "
     "has a 3/2 approximation</b> (Christofides), recently improved.",
     "",
     "<b>Vertex cover:</b> no better than 2 under UGC. <b>So the "
     "ten-line algorithm of Part 2 is optimal.</b>",
     "",
     "<b>The PCP theorem is what makes these provable</b> \u2014 a "
     "characterisation of NP by probabilistically checkable proofs.",
   ],
   "footnote": "<b>That trivial algorithms are frequently optimal</b> is "
               "the most useful practical message: check the greedy bound "
               "before building something clever."},
 ],
 "takeaways": [
   "An approximation guarantee is proved against a computable bound \u2014 "
   "usually an LP relaxation \u2014 not against the optimum itself.",
   "FPTAS, PTAS, constant-factor, logarithmic, and inapproximable are "
   "provably distinct classes under standard assumptions.",
   "Vertex cover's 2-approximation is ten lines: relax, round at a half, "
   "and the cost at most doubles.",
   "The integrality gap bounds what any rounding of that relaxation can "
   "achieve, so beating it requires a stronger formulation.",
   "Randomised rounding treats fractional values as probabilities, so "
   "expected cost equals the LP value by linearity of expectation.",
   "Goemans\u2013Williamson's 0.878 comes from a random hyperplane, and "
   "under the Unique Games Conjecture it is optimal.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The framework"),
  ("callout", "The guarantee is against a bound, not against the optimum",
   ["<b>You cannot compare your algorithm's output to the optimum, because "
    "computing the optimum is exactly the intractable problem you are "
    "avoiding.</b> This is the obstacle that makes approximation analysis "
    "look impossible at first.",
    "<b>So compare it to a <i>bound</i> on the optimum instead</b> "
    "\u2014 almost always the value of a relaxation, which is a lower "
    "bound for a minimisation problem by weak duality (Module 04 "
    "&sect;1).",
    "<b>If your solution's cost is within a factor &alpha; of the bound, "
    "it is within &alpha; of the optimum</b>, because the optimum lies "
    "between the bound and your solution. <b>The optimum never has to be "
    "computed; it only has to be sandwiched.</b>",
    "<b>That is the entire mechanism of approximation analysis.</b> "
    "<b>Every ratio in this module is proved against a relaxation</b>, "
    "which is why Module 04's duality had to come first \u2014 and why "
    "this module, Module 04, and Module 09's branch and bound are all "
    "applications of one idea."]),
  ("table", ["Class", "What it means", "Example"],
   [["<b>FPTAS</b>",
     "<b>A (1+&epsilon;)-approximation in time polynomial in both n and "
     "1/&epsilon;.</b> The best you can hope for short of exact.",
     "<b>Knapsack</b>, via dynamic programming on scaled profits."],
    ["<b>PTAS</b>",
     "A (1+&epsilon;)-approximation in time polynomial in n for each fixed "
     "&epsilon; \u2014 the dependence on 1/&epsilon; may be terrible.",
     "Euclidean TSP (Arora, Mitchell), where the exponent depends on "
     "1/&epsilon;."],
    ["<b>Constant factor</b>", "<b>Within a fixed ratio &alpha;.</b>",
     "<b>Vertex cover (2), MAX-CUT (1.138 by Goemans\u2013Williamson), "
     "metric TSP (3/2).</b>"],
    ["<b>Logarithmic</b>", "Within O(log n).",
     "<b>Set cover \u2014 and the logarithm is provably optimal</b> "
     "(&sect;4)."],
    ["<b>No constant factor</b>",
     "<b>No constant-factor approximation exists unless P = NP.</b>",
     "<b>General (non-metric) TSP, maximum clique.</b>"]],
   [0.17, 0.42, 0.41]),
  ("p", "<b>These classes are provably distinct under standard complexity "
        "assumptions</b>, so the hierarchy reflects genuine structure "
        "rather than current ignorance \u2014 which is a strong and "
        "somewhat surprising thing to be able to say about approximation."),

  ("h1", "2 &nbsp; LP rounding"),
  ("code", """VERTEX COVER: minimum-weight set of vertices touching every edge.

INTEGER PROGRAM
    minimise  sum w_v x_v
    s.t.      x_u + x_v >= 1   for every edge (u,v)
              x_v in {0,1}

RELAX  x_v in [0,1],  solve the LP, then ROUND:
    take v  if  x_v >= 1/2

FEASIBLE: every edge has x_u + x_v >= 1, so at least one
endpoint has x >= 1/2 and is taken. Every edge is covered.

COST: rounding at most DOUBLES each variable, so
    ALG <= 2 * LP <= 2 * OPT
since LP <= OPT for a relaxed minimisation.

A 2-APPROXIMATION, PROVED, IN TEN LINES.

And the analysis shows where the 2 comes from: the threshold.
The INTEGRALITY GAP of this formulation IS 2 (take a triangle:
LP gives 1/2 everywhere for cost 3/2; the true optimum is 2).
So no better rounding of THIS relaxation exists."""),
  ("p", "<b>The integrality gap bounds what <i>any</i> rounding of that "
        "relaxation can achieve.</b> To beat the factor you need a "
        "stronger formulation \u2014 more constraints, or a semidefinite "
        "relaxation (&sect;3) \u2014 <b>not a cleverer rounding "
        "rule</b>. <b>That observation connects this module directly to "
        "Module 09's formulation strength</b>: the same quantity governs "
        "branch-and-bound tree size and approximation ratio, which is not a "
        "coincidence."),
  ("callout", "Randomised rounding, and why it analyses well",
   ["<b>Treat each fractional value x<sub>v</sub> as a <i>probability</i> "
    "and include v independently with that probability.</b> The idea is "
    "almost too simple to be a technique.",
    "<b>The expected cost is exactly the LP value</b>, by linearity of "
    "expectation \u2014 and linearity holds regardless of dependence, "
    "which is why the cost analysis is a single line and requires no "
    "independence assumption at all.",
    "<b>Feasibility holds only in expectation</b>, so a single round may "
    "leave constraints violated. Repeat the rounding, or round "
    "conditionally, and use concentration bounds (Chernoff; CSCE 658) to "
    "control the probability of failure.",
    "<b>Set cover's O(log n) guarantee comes from exactly this</b>: round "
    "repeatedly, and after O(log n) independent rounds every element is "
    "covered with high probability, at O(log n) times the LP cost. "
    "<b>Which matches the hardness bound of &sect;4</b> \u2014 the "
    "technique is optimal for that problem."]),

  ("break",),
  ("h1", "3 &nbsp; Semidefinite relaxation"),
  ("callout", "Goemans\u2013Williamson: relax to vectors, round by a random hyperplane",
   ["<b>MAX-CUT asks for a partition of the vertices maximising the total "
    "weight of edges crossing it.</b> Assign each vertex a value "
    "&plusmn;1 and maximise &Sigma;w<sub>ij</sub>(1 &minus; "
    "x<sub>i</sub>x<sub>j</sub>)/2 \u2014 which is non-convex because of "
    "the discrete constraint.",
    "<b>Relax it by assigning each vertex a unit <i>vector</i> in "
    "high-dimensional space</b> instead of a scalar, and maximising the "
    "same expression with the product replaced by an inner product. "
    "<b>That is a semidefinite program</b> \u2014 convex (Module 01 "
    "&sect;2) and solvable in polynomial time.",
    "<b>Then round with a random hyperplane through the origin:</b> the "
    "vertices whose vectors fall on each side form the two sides of the "
    "cut. A uniformly random direction, and nothing more.",
    "<b>The probability that an edge is cut is &theta;/&pi;</b>, where "
    "&theta; is the angle between its endpoints' vectors \u2014 the "
    "fraction of hyperplane orientations that separate them. <b>The ratio "
    "of &theta;/&pi; to the SDP's contribution for that edge is at least "
    "0.878 for every angle</b>, which is a one-variable calculus exercise. "
    "<b>A 0.878-approximation, derived from geometry</b>, and it is one of "
    "the most elegant results in algorithms."]),
  ("callout", "And 0.878 is probably optimal",
   ["<b>Under the Unique Games Conjecture, no polynomial-time algorithm "
    "achieves a better ratio than 0.878 for MAX-CUT.</b>",
    "<b>So the Goemans\u2013Williamson constant \u2014 which looks "
    "entirely like an artifact of their particular analysis, being the "
    "minimum of a transcendental ratio \u2014 is the true boundary of what "
    "is achievable.</b>",
    "<b>That is a remarkable convergence.</b> An algorithmic result and a "
    "hardness result, developed independently by different methods, "
    "meeting on an arbitrary-looking number \u2014 which is reasonable "
    "evidence that the number is describing something real about the "
    "problem rather than about the technique.",
    "<b>The Unique Games Conjecture is unproved and widely believed</b>, "
    "and <b>a great deal of modern approximation hardness is conditional "
    "on it</b>. <b>That conditionality should be stated when citing these "
    "results</b> \u2014 'optimal unless UGC fails' is the honest form, and "
    "it is a weaker claim than 'optimal unless P = NP'."]),

  ("h1", "4 &nbsp; Hardness of approximation"),
  ("ul", ["<b>Set cover:</b> no approximation better than "
          "(1 &minus; o(1))&middot;ln n unless P = NP. <b>And the simple "
          "greedy algorithm achieves exactly that</b> \u2014 <b>the most "
          "obvious method is provably optimal</b>, which is both "
          "satisfying and a useful warning against assuming sophistication "
          "helps.",
          "<b>Maximum clique:</b> no n<super>1&minus;&epsilon;</super> "
          "approximation unless P = NP. <b>Essentially "
          "inapproximable</b> \u2014 you cannot do meaningfully better than "
          "returning a single vertex.",
          "<b>General TSP:</b> no constant-factor approximation at all "
          "\u2014 <b>and metric TSP has a 3/2-approximation</b> "
          "(Christofides, 1976, improved only in 2021). <b>The triangle "
          "inequality is what makes the difference</b>, which is a good "
          "illustration that a problem's approximability depends on "
          "structure rather than on its exact-solution complexity.",
          "<b>Vertex cover:</b> no better than 2 under UGC. <b>So the "
          "ten-line algorithm of &sect;2 is optimal</b>, and the decades "
          "of effort spent trying to beat it were spent against a wall.",
          "<b>The PCP theorem is what makes these results provable</b> "
          "\u2014 a characterisation of NP in terms of probabilistically "
          "checkable proofs, which converts approximation hardness into a "
          "gap-preserving reduction. <b>It is one of the deepest results in "
          "complexity theory</b> (CSCE 637), and its practical "
          "consequence here is that <b>'nobody has found a better "
          "algorithm' can be upgraded to 'no better algorithm "
          "exists'.</b>"]),
 ],
 "resources": [
   ("Williamson & Shmoys &mdash; The Design of Approximation Algorithms "
    "(free PDF)",
    "https://www.designofapproxalgs.com/",
    "<b>Free in full, and the reference for this entire module.</b> The "
    "LP rounding and randomised rounding chapters cover &sect;2 "
    "completely."),
   ("Goemans & Williamson &mdash; Improved Approximation Algorithms for "
    "Maximum Cut (free)",
    "https://dl.acm.org/doi/10.1145/227683.227684",
    "<b>The &sect;3 result.</b> The geometric argument is followable and "
    "worth working through."),
   ("Vazirani &mdash; Approximation Algorithms (free PDF)",
    "https://www.ics.uci.edu/~vazirani/book.pdf",
    "Free, and complementary \u2014 stronger on the primal-dual method "
    "and on the combinatorial algorithms."),
   ("Khot &mdash; On the Unique Games Conjecture (free survey)",
    "https://www.cs.nyu.edu/~khot/papers/UGCSurvey.pdf",
    "<b>The &sect;3 and &sect;4 conditionality</b>, explained by the "
    "person who proposed the conjecture."),
 ],
 "exercises": [
   "<b>Implement the vertex cover 2-approximation</b> and verify the ratio "
   "empirically against exact solutions on small instances.",
   "<b>Construct the triangle instance</b> showing the integrality gap is "
   "exactly 2.",
   "Implement greedy set cover and measure its ratio against the LP bound "
   "on random instances.",
   "<b>Implement randomised rounding for set cover</b> and measure how "
   "many rounds are needed for feasibility.",
   "<b>Solve a small MAX-CUT by semidefinite programming</b> with CVXPY "
   "and round with a random hyperplane.",
   "<b>Repeat the rounding many times</b> and plot the distribution of cut "
   "values against the SDP bound.",
   "Compare the SDP relaxation's bound against the LP relaxation's on the "
   "same instances.",
   "<b>Measure the achieved ratio</b> and compare against 0.878.",
   "Take a problem from your own work and <b>find or derive an "
   "approximation guarantee</b> for a simple algorithm on it.",
   "<b>Compute the integrality gap</b> of a formulation you wrote in "
   "Module 09.",
 ],
 "selfcheck": [
   "How is an approximation guarantee proved without computing the "
   "optimum?",
   "Name five approximability classes and an example of each.",
   "Derive the vertex cover 2-approximation and say where the 2 comes "
   "from.",
   "What does the integrality gap bound?",
   "Why does randomised rounding analyse cleanly?",
   "Describe the Goemans\u2013Williamson relaxation and rounding.",
   "What is the status of the 0.878 bound?",
   "Give four inapproximability results and say which algorithms are "
   "already optimal.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Combinatorial Optimisation",
 "subtitle": "The problems with special structure.",
 "question": "Why are some discrete problems easy?",
 "outcomes": [
     "Explain network flow and its integrality.",
     "Explain matching and its duality.",
     "Explain matroids and why greedy works on them.",
     "Explain submodularity and the greedy guarantee.",
     "Recognise exploitable structure in a new problem.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Flow",
   "blurb": "The structure that makes a family of problems easy."},

  {"t": "callout", "title": "Max-flow min-cut is LP duality made concrete",
   "kind": "The connection",
   "body": ["<b>The maximum flow from source to sink equals the minimum "
            "capacity of a cut separating them.</b>",
            "<b>That is not a coincidence — it is strong duality</b> "
            "(Module 04 §1) for the flow linear program, whose dual "
            "is the cut problem.",
            "<b>And the constraint matrix is totally unimodular</b> "
            "(Module 03 §3), so the LP optimum is integral "
            "automatically.",
            "<b>So the problem is polynomial for a structural reason</b>, "
            "not because a clever algorithm was found. <b>The algorithms "
            "exploit the structure; they do not create it.</b>"]},

  {"t": "table", "kicker": "Reductions", "title": "What reduces to flow",
   "header": ["Problem", "Reduction", "Note"],
   "widths": [3.0, 4.3, 4.8],
   "rows": [
     ["<b>Bipartite matching</b>", "<b>Unit capacities, source to left, right to sink</b>", "<b>Integral flow = a matching</b>"],
     ["<b>Vertex-disjoint paths</b>", "Split each vertex, capacity 1", "Menger's theorem"],
     ["<b>Project selection</b>", "<b>Min cut on a profit/cost graph</b>", "<b>Maximum closure</b>"],
     ["<b>Image segmentation</b>", "<b>Min cut with smoothness terms</b>", "<b>Graph cuts; CSCE 748</b>"],
     ["Scheduling with deadlines", "Flow over a time-expanded graph", "Common in practice"],
     ["<b>Baseball elimination</b>", "<b>Flow feasibility</b>", "The classic surprising reduction"],
   ],
   "footnote": "<b>Recognising a flow problem is the highest-value "
               "pattern-match in this module</b> \u2014 it converts an "
               "apparently hard problem into a polynomial one.",
   "note": "Graph cuts in vision is the connection the track cares "
           "about."},

  {"t": "section", "label": "Part 2", "title": "Matroids",
   "blurb": "The abstraction that explains greedy."},

  {"t": "code", "kicker": "Matroids", "title": "When greedy is exactly right",
   "lang": "text", "code": """
  A MATROID is a ground set E with a family of INDEPENDENT
  subsets satisfying:
      1. the empty set is independent
      2. subsets of independent sets are independent (hereditary)
      3. EXCHANGE: if |A| < |B| and both independent, then some
         element of B can be added to A keeping it independent

  THEOREM: the greedy algorithm -- sort by weight, add greedily
  whenever independence is preserved -- finds the MAXIMUM WEIGHT
  independent set, EXACTLY, for ANY matroid.

  AND THE CONVERSE: if greedy is optimal for every weighting,
  the structure IS a matroid.

  SO MATROIDS ARE EXACTLY THE STRUCTURES WHERE GREEDY WORKS.
  That is a complete characterisation, which is rare.

  EXAMPLES
    graphic matroid   forests in a graph  -> KRUSKAL'S MST
    linear matroid    linearly independent column sets
    partition matroid at most k_i from each group
    uniform matroid   any set of size <= k

  So Kruskal is not a clever trick; it is the matroid greedy
  algorithm applied to the graphic matroid.
""",
   "caption": "<b>A complete characterisation of when greedy is "
              "optimal</b> \u2014 which is an unusually clean answer to a "
              "question that usually has none.",
   "note": "That the converse holds too is what makes this satisfying."},

  {"t": "section", "label": "Part 3", "title": "Submodularity",
   "blurb": "Diminishing returns, and a guarantee."},

  {"t": "eq", "kicker": "Submodularity", "title": "Diminishing returns, formalised",
   "eqs": [
     ("f(A ∪ {x}) − f(A)  ≥  f(B ∪ {x}) − f(B)   for A ⊆ B",
      "Adding x to a smaller set helps at least as much as adding it to a "
      "larger one."),
     ("Maximising a monotone submodular f under a cardinality constraint",
      "NP-hard — and greedy achieves (1 − 1/e) ≈ 0.632 of the "
      "optimum."),
     ("And 1 − 1/e is optimal unless P = NP",
      "So greedy is the best polynomial algorithm, provably."),
   ],
   "caption": "<b>Submodularity is to discrete optimisation what convexity "
              "is to continuous</b> \u2014 the structural property that "
              "makes guarantees possible.",
   "note": "That analogy is the clearest way to place submodularity."},

  {"t": "callout", "title": "Where submodularity shows up",
   "kind": "Why this is practically useful",
   "body": ["<b>Coverage:</b> how many distinct items a chosen set covers "
            "— sensor placement, facility location, influence "
            "maximisation.",
            "<b>Entropy and mutual information</b> of a selected set of "
            "variables — so experimental design and active learning "
            "(CSCE 633 M11) are submodular.",
            "<b>Diversity and summarisation</b> — picking a "
            "representative subset.",
            "<b>And feature selection</b> under some models. <b>So the "
            "0.632 guarantee covers a wide class of selection problems "
            "where people otherwise use greedy and hope.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Recognising structure",
   "blurb": "The practical skill."},

  {"t": "bullets", "kicker": "Structure", "title": "What to look for in a new problem",
   "items": [
     "<b>Is it a flow problem in disguise?</b> Conservation, "
     "capacities, a bipartite assignment \u2014 check first.",
     "",
     "<b>Is the constraint matrix totally unimodular?</b> Then drop the "
     "integrality constraint entirely (Module 03 §3).",
     "",
     "<b>Is the feasible family a matroid?</b> Then greedy is exact.",
     "",
     "<b>Is the objective submodular and monotone?</b> Then greedy is "
     "within 0.632 and that is optimal.",
     "",
     "<b>Otherwise: integer programming</b> (Module 09) <b>with the "
     "best formulation you can find.</b>",
   ],
   "footnote": "<b>This checklist is worth running before writing any "
               "code</b> \u2014 each hit converts an intractable problem "
               "into a solved one."},

  {"t": "callout", "title": "Structure is found by modelling, not by searching",
   "kind": "The habit",
   "body": ["<b>Whether a problem has exploitable structure frequently "
            "depends on how you formulate it</b>, not on the problem "
            "itself.",
            "<b>The same situation modelled with different variables can "
            "be a flow problem or a general integer program.</b>",
            "<b>So spend time on the formulation before accepting that "
            "the problem is hard.</b>",
            "<b>Which is Module 12's subject</b>, and the reason it "
            "follows this one rather than preceding it — <b>you need the "
            "catalogue of structures before you can aim a formulation at "
            "one.</b>"]},
 ],
 "takeaways": [
   "Max-flow min-cut is strong duality for the flow linear program, and the "
   "integrality comes from total unimodularity.",
   "A great many apparently unrelated problems reduce to flow, and "
   "recognising one is the highest-value pattern-match here.",
   "Matroids are exactly the structures on which the greedy algorithm is "
   "optimal \u2014 a complete characterisation, including the converse.",
   "Kruskal's algorithm is the matroid greedy algorithm applied to the "
   "graphic matroid, not an independent trick.",
   "Submodularity formalises diminishing returns, and greedy achieves "
   "1 \u2212 1/e of the optimum \u2014 which is itself optimal unless "
   "P = NP.",
   "Submodularity is to discrete optimisation what convexity is to "
   "continuous.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Network flow"),
  ("callout", "Max-flow min-cut is LP duality made concrete",
   ["<b>The maximum flow from a source to a sink equals the minimum total "
    "capacity of any cut separating them.</b> Stated this way it looks like "
    "a combinatorial coincidence.",
    "<b>It is strong duality.</b> Write the maximum flow problem as a "
    "linear program; its dual is the minimum cut problem, and Module 04 "
    "&sect;1's strong duality for linear programs gives the equality "
    "\u2014 <b>the famous theorem is an instance of a general one.</b>",
    "<b>And the constraint matrix of a flow problem is totally "
    "unimodular</b> (Module 03 &sect;3), so every vertex of the "
    "polyhedron is integral and the LP optimum is automatically a valid "
    "integer flow.",
    "<b>So the problem is polynomial for a structural reason, not because "
    "a sufficiently clever algorithm was eventually found.</b> "
    "<b>Ford\u2013Fulkerson, Dinic, and push-relabel exploit the "
    "structure; they do not create it</b> \u2014 and that distinction is "
    "what this module is about, because it tells you where to look when "
    "facing a new problem."]),
  ("table", ["Problem", "Reduction", "Note"],
   [["<b>Bipartite matching</b>",
     "<b>Unit capacities: source to every left vertex, every right vertex "
     "to sink, edges in between.</b>",
     "<b>An integral maximum flow <i>is</i> a maximum matching</b>, and "
     "integrality is guaranteed."],
    ["<b>Vertex-disjoint paths</b>",
     "Split each vertex into an in-node and an out-node joined by a "
     "capacity-1 edge.",
     "Menger's theorem falls out as the min-cut."],
    ["<b>Project selection</b>",
     "<b>Minimum cut on a graph of projects and their prerequisite "
     "costs.</b>",
     "<b>Maximum closure</b> \u2014 a surprising and very useful "
     "reduction for selection problems with dependencies."],
    ["<b>Image segmentation</b>",
     "<b>Minimum cut with data terms on vertices and smoothness terms on "
     "edges.</b>",
     "<b>Graph cuts \u2014 the standard method before deep learning, and "
     "still used</b> (CSCE 748). Exact for binary labelling."],
    ["<b>Scheduling with release times and deadlines</b>",
     "Flow over a time-expanded graph.",
     "Common in practice, and frequently missed."],
    ["<b>Baseball elimination</b>", "<b>Flow feasibility.</b>",
     "The classic surprising reduction \u2014 determining whether a team "
     "can still win is a max-flow computation."]],
   [0.21, 0.40, 0.39]),

  ("h1", "2 &nbsp; Matroids"),
  ("code", """A MATROID is a ground set E with a family of INDEPENDENT
subsets satisfying:
  1. the empty set is independent
  2. subsets of independent sets are independent (hereditary)
  3. EXCHANGE: if |A| < |B| and both are independent, some
     element of B can be added to A keeping it independent

THEOREM: the greedy algorithm -- sort by weight, add greedily
whenever independence is preserved -- finds the MAXIMUM WEIGHT
independent set EXACTLY, for ANY matroid.

CONVERSE: if greedy is optimal for every weighting, the
structure IS a matroid.

SO MATROIDS ARE EXACTLY THE STRUCTURES WHERE GREEDY WORKS.

EXAMPLES
  graphic matroid     forests in a graph  -> KRUSKAL'S MST
  linear matroid      linearly independent sets of columns
  partition matroid   at most k_i from each group
  uniform matroid     any set of size <= k"""),
  ("p", "<b>That the converse holds is what makes this result "
        "satisfying.</b> It is a <i>complete characterisation</i> of when "
        "greedy is optimal \u2014 an unusually clean answer to a question "
        "that is normally answered case by case. <b>So Kruskal's algorithm "
        "is not a clever trick specific to spanning trees; it is the "
        "matroid greedy algorithm applied to the graphic matroid</b> "
        "(CSCE 629), and recognising that explains why it works rather "
        "than merely that it does."),

  ("break",),
  ("h1", "3 &nbsp; Submodularity"),
  ("eq", "f(A &cup; {x}) &minus; f(A) &nbsp;&ge;&nbsp; f(B &cup; {x}) "
         "&minus; f(B) &nbsp;&nbsp; for A &sube; B"),
  ("p", "<b>Adding an element to a smaller set helps at least as much as "
        "adding it to a larger one</b> \u2014 diminishing returns, "
        "formalised. <b>Maximising a monotone submodular function subject "
        "to a cardinality constraint is NP-hard, and the greedy algorithm "
        "achieves (1 &minus; 1/e) &asymp; 0.632 of the optimum</b> "
        "\u2014 Nemhauser, Wolsey and Fisher, 1978. <b>And "
        "1 &minus; 1/e is itself optimal unless P = NP</b> (Module 10 "
        "&sect;4), <b>so greedy is the best polynomial-time algorithm "
        "available</b>. <b>Submodularity is to discrete optimisation what "
        "convexity is to continuous optimisation</b> \u2014 the structural "
        "property that converts an intractable problem into one with a "
        "guarantee, and the analogy is close enough to be worth carrying."),
  ("callout", "Where submodularity shows up",
   ["<b>Coverage functions.</b> How many distinct items a chosen set "
    "covers \u2014 sensor placement, facility location, influence "
    "maximisation in networks, test-case selection. <b>Any 'cover as much "
    "as possible with k choices' problem.</b>",
    "<b>Entropy and mutual information</b> of a selected set of random "
    "variables are submodular \u2014 <b>so experimental design, sensor "
    "selection, and active learning</b> (CSCE 633 Module 11 &sect;4) "
    "<b>all inherit the guarantee</b>, which is a genuinely useful fact "
    "that is not widely known in machine learning.",
    "<b>Diversity and summarisation objectives</b> \u2014 selecting a "
    "representative subset of documents, images, or data points, where "
    "adding a near-duplicate of something already chosen adds little.",
    "<b>And feature selection under certain independence assumptions.</b> "
    "<b>So the 0.632 guarantee covers a wide class of practical selection "
    "problems where people currently use greedy and hope</b> \u2014 "
    "checking submodularity converts the hope into a theorem, and it is "
    "frequently a short check."]),

  ("h1", "4 &nbsp; Recognising structure"),
  ("ul", ["<b>Is it a flow problem in disguise?</b> Look for conservation, "
          "capacities, a bipartite assignment, or a two-way partition. "
          "<b>Check this first</b> \u2014 it is the highest-value "
          "pattern-match in the module (&sect;1).",
          "<b>Is the constraint matrix totally unimodular?</b> Then drop "
          "the integrality constraints entirely and solve the LP "
          "(Module 03 &sect;3) \u2014 interval structure, node-arc "
          "incidence, and consecutive-ones structure are the usual "
          "signs.",
          "<b>Is the family of feasible sets a matroid?</b> Then the "
          "greedy algorithm is exact (&sect;2), and no further work is "
          "needed.",
          "<b>Is the objective monotone and submodular, under a "
          "cardinality or matroid constraint?</b> Then greedy is within "
          "0.632 and that is optimal (&sect;3).",
          "<b>Otherwise: integer programming</b> (Module 09) <b>with the "
          "strongest formulation you can construct.</b> <b>This checklist "
          "is worth running before writing any code</b> \u2014 each hit "
          "converts an apparently intractable problem into a solved one, "
          "and the check costs an hour."]),
  ("callout", "Structure is found by modelling, not by searching",
   ["<b>Whether a problem has exploitable structure frequently depends on "
    "how you formulate it rather than on the problem itself.</b> The "
    "structure is a property of the mathematical model, and you chose the "
    "model.",
    "<b>The same practical situation, modelled with different decision "
    "variables, can be a network flow problem or an arbitrary integer "
    "program.</b> Choosing 'how much flows along this arc' rather than "
    "'which assignment is made' can be the difference between a polynomial "
    "algorithm and an exponential search.",
    "<b>So spend real time on the formulation before accepting that a "
    "problem is hard.</b> <b>'This is NP-hard' is a statement about a "
    "formulation at least as often as about a problem</b>, and "
    "reformulating is cheaper than any algorithmic heroics.",
    "<b>Which is Module 12's subject</b>, and the reason it follows this "
    "module rather than preceding it \u2014 <b>you need the catalogue of "
    "exploitable structures before you can usefully aim a formulation at "
    "one.</b>"]),
 ],
 "resources": [
   ("Williamson & Shmoys, and Vazirani &mdash; the combinatorial chapters "
    "(free)",
    "https://www.designofapproxalgs.com/",
    "Flow, matching, and the primal-dual method, with the duality "
    "connections of &sect;1 made explicit."),
   ("Schrijver &mdash; Combinatorial Optimization: Polyhedra and "
    "Efficiency",
    "https://homepages.cwi.nl/~lex/",
    "The comprehensive reference for &sect;1 and &sect;2. The author's "
    "shorter lecture notes are free and are the right entry point."),
   ("Oxley &mdash; Matroid Theory; and Edmonds' greedy papers",
    "https://global.oup.com/academic/product/matroid-theory-9780198566946",
    "The &sect;2 characterisation and its converse. Edmonds' original "
    "papers are short and readable."),
   ("Krause & Golovin &mdash; Submodular Function Maximization (free "
    "survey)",
    "https://las.inf.ethz.ch/files/krause12survey.pdf",
    "<b>The &sect;3 material</b>, with the applications of the callout and "
    "the lazy-greedy speedup that makes it practical."),
 ],
 "exercises": [
   "<b>Formulate maximum flow as a linear program</b> and derive its dual. "
   "Confirm the dual is minimum cut.",
   "Solve the LP and verify the optimum is integral without being "
   "constrained to be.",
   "<b>Reduce bipartite matching to flow</b> and solve an instance both "
   "ways.",
   "<b>Implement graph-cut image segmentation</b> on a small image and "
   "connect it to CSCE 748.",
   "<b>Verify the matroid axioms</b> for forests in a graph.",
   "<b>Implement matroid greedy</b> generically and instantiate it as "
   "Kruskal's algorithm.",
   "<b>Construct a structure that is not a matroid</b> and exhibit a "
   "weighting where greedy fails.",
   "<b>Verify submodularity</b> of a coverage function by checking the "
   "diminishing-returns inequality.",
   "<b>Run greedy on a submodular maximisation</b> and compare against the "
   "exact optimum on small instances. Confirm the ratio exceeds 0.632.",
   "Take a problem from your own work and run &sect;4's checklist on it.",
 ],
 "selfcheck": [
   "Why is max-flow min-cut a duality result, and where does integrality "
   "come from?",
   "Name six problems that reduce to flow.",
   "State the matroid axioms and the greedy theorem, including its "
   "converse.",
   "Why is Kruskal's algorithm not a special trick?",
   "Define submodularity and state the greedy guarantee and its "
   "optimality.",
   "Give four places submodularity appears.",
   "Give the five-step structure checklist.",
   "Why is structure a property of the formulation?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Modelling",
 "subtitle": "The part that decides whether any of this helps.",
 "question": "How do you turn a real problem into a program?",
 "outcomes": [
     "Choose decision variables deliberately.",
     "Translate messy objectives into expressible ones.",
     "Handle multiple objectives honestly.",
     "Validate a model against the problem it represents.",
     "State where a model stops being valid.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Variables",
   "blurb": "The choice that determines everything after."},

  {"t": "callout", "title": "The variable choice decides the structure",
   "kind": "The most consequential decision",
   "body": ["<b>The same situation can be modelled with different "
            "decision variables</b>, and the formulations differ "
            "enormously in tractability (Module 11 §4).",
            "<b>Assignment variables x[i][j] versus flow variables on "
            "arcs</b> — one may be totally unimodular and the other a "
            "general integer program.",
            "<b>Sequence problems:</b> 'position of item i' versus 'item "
            "i immediately precedes j' give completely different "
            "formulations of the same problem.",
            "<b>So enumerate several variable choices before committing "
            "to one.</b> <b>This is the highest-leverage hour in an "
            "optimisation project and it is routinely skipped.</b>"]},

  {"t": "table", "kicker": "Patterns", "title": "Common variable patterns",
   "header": ["Pattern", "Meaning", "Watch for"],
   "widths": [2.8, 4.2, 5.1],
   "rows": [
     ["<b>Binary assignment</b>", "<b>x[i][j] = 1 if i goes to j</b>", "<b>Symmetry when the j are identical</b>"],
     ["<b>Flow on arcs</b>", "How much moves along each arc", "<b>Often totally unimodular. Prefer it</b>"],
     ["<b>Time-indexed</b>", "<b>x[i][t] = 1 if i starts at time t</b>", "<b>Huge, and the relaxation is strong</b>"],
     ["<b>Sequencing</b>", "y[i][j] = 1 if i precedes j", "Needs transitivity constraints"],
     ["<b>Set selection</b>", "<b>One variable per feasible set</b>", "<b>Exponential; use column generation</b>"],
   ],
   "footnote": "<b>Time-indexed formulations are large and have strong "
               "relaxations</b>, which is frequently the better trade "
               "\u2014 size is cheaper than a weak bound.",
   "note": "The size-vs-bound-strength trade is counterintuitive and "
           "real."},

  {"t": "section", "label": "Part 2", "title": "Objectives",
   "blurb": "What people actually want, and what you can write."},

  {"t": "callout", "title": "The stated objective is rarely the real one",
   "kind": "The modelling difficulty",
   "body": ["<b>'Minimise cost' usually means 'minimise cost without "
            "anything unacceptable happening'</b> — and the "
            "unacceptable things are unstated.",
            "<b>So the first model produces a solution nobody will "
            "accept</b>, which is informative: the objections are the "
            "missing constraints.",
            "<b>Iterate.</b> Show the solution, collect the objections, "
            "encode them, repeat. <b>The model converges on the real "
            "problem through rejection.</b>",
            "<b>And a solution that is optimal and unacceptable is more "
            "useful than one that is feasible and mediocre</b>, because it "
            "elicits the constraint."]},

  {"t": "table", "kicker": "Multiple objectives", "title": "When there is more than one",
   "header": ["Approach", "How", "Honest?"],
   "widths": [2.8, 4.3, 5.0],
   "rows": [
     ["<b>Weighted sum</b>", "<b>Minimise w\u2081f\u2081 + w\u2082f\u2082</b>", "<b>Requires an exchange rate. State it</b>"],
     ["<b>Constrain all but one</b>", "<b>Minimise f\u2081 subject to f\u2082 \u2264 c</b>", "<b>Usually the clearest formulation</b>"],
     ["<b>Pareto frontier</b>", "<b>Sweep and plot the trade-off</b>", "<b>Most honest \u2014 let the owner choose</b>"],
     ["Lexicographic", "Optimise in priority order", "When priorities are genuinely strict"],
     ["<b>Goal programming</b>", "Penalise deviation from targets", "Useful when targets are given"],
   ],
   "footnote": "<b>Plotting the Pareto frontier is the most honest "
               "response</b> \u2014 it shows the trade rather than hiding "
               "it in a weight nobody examined.",
   "note": "Presenting the frontier changes the conversation with the "
           "problem owner."},

  {"t": "section", "label": "Part 3", "title": "Validation",
   "blurb": "Does the model mean what you think?"},

  {"t": "bullets", "kicker": "Validation", "title": "Checking a model",
   "items": [
     "<b>Solve a tiny instance by hand</b> and compare. The most "
     "effective check and the least done.",
     "",
     "<b>Check the extremes:</b> zero demand, infinite capacity, one "
     "item. The answers should be obvious and should be right.",
     "",
     "<b>Look at the dual variables</b> (Module 04 §2). <b>If a "
     "shadow price is absurd, a constraint is wrong.</b>",
     "",
     "<b>Perturb an input and check the answer moves sensibly</b> "
     "\u2014 and in the right direction.",
     "",
     "<b>And show the solution to the person who owns the problem.</b> "
     "<b>They will spot in ten seconds what you would not find in a "
     "week.</b>",
   ],
   "footnote": "<b>The dual check is the underused one</b> and it "
               "localises errors to specific constraints."},

  {"t": "callout", "title": "Infeasible and unbounded are both diagnostics",
   "kind": "Reading the solver's complaints",
   "body": ["<b>Infeasible usually means over-constrained, not "
            "impossible.</b> Use an irreducible infeasible subset — most "
            "solvers compute one — to find the conflicting constraints.",
            "<b>Unbounded almost always means a missing constraint</b>, "
            "and it is a gift: the solver found a way to profit "
            "infinitely, which tells you exactly what you forgot to "
            "forbid.",
            "<b>Add elastic variables with large penalties</b> to see "
            "<i>which</i> constraint to relax, rather than guessing.",
            "<b>And a suspiciously good objective is the same signal as a "
            "suspiciously good test score</b> (CSCE 633 M12) — "
            "<b>audit before celebrating.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Limits",
   "blurb": "Where the model stops being the problem."},

  {"t": "callout", "title": "State where the model breaks",
   "kind": "The deliverable that matters",
   "body": ["<b>Every model omits things</b> — uncertainty treated as "
            "certain, human judgement not encoded, dynamics treated as "
            "static.",
            "<b>Optimisation exploits every simplification "
            "aggressively</b>, because it is searching for extremes — "
            "<b>so a simplification that is harmless in a simulation can "
            "be catastrophic in an optimum.</b>",
            "<b>That is the specific hazard of this subject:</b> the "
            "optimiser finds the corner of your model where it is least "
            "like reality, and sits there.",
            "<b>So write down the assumptions and test the solution "
            "against them.</b> <b>'This model assumes demand is known; "
            "under 20% demand error the solution costs 15% more' is the "
            "deliverable</b>, not the optimum alone."]},
 ],
 "takeaways": [
   "The choice of decision variables determines the structure and the "
   "tractability, and enumerating several before committing is the "
   "highest-leverage hour available.",
   "Time-indexed formulations are large with strong relaxations, which is "
   "frequently the better trade \u2014 size is cheaper than a weak bound.",
   "The stated objective is rarely the real one, and the first model's "
   "unacceptable solution is informative because the objections are the "
   "missing constraints.",
   "Plotting the Pareto frontier is the most honest response to multiple "
   "objectives \u2014 it shows the trade rather than hiding it in a weight.",
   "Infeasible usually means over-constrained and unbounded almost always "
   "means a missing constraint \u2014 both are diagnostics.",
   "Optimisation exploits every simplification aggressively, so it finds "
   "the corner of your model least like reality and sits there.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Choosing decision variables"),
  ("callout", "The variable choice decides the structure",
   ["<b>The same real situation can be modelled with entirely different "
    "decision variables</b>, and the resulting formulations differ "
    "enormously in tractability (Module 11 &sect;4) \u2014 by orders of "
    "magnitude, and sometimes by the difference between polynomial and "
    "NP-hard.",
    "<b>Assignment variables x[i][j] versus flow variables on arcs:</b> "
    "one formulation may have a totally unimodular constraint matrix "
    "(Module 03 &sect;3) and solve as a linear program, while the other "
    "requires branch and bound.",
    "<b>Sequencing problems are the clearest case.</b> 'The position of "
    "item i in the sequence', 'item i immediately precedes item j', and "
    "'item i starts at time t' give three completely different "
    "formulations of the same problem, with different sizes, different "
    "relaxation strengths, and different symmetry.",
    "<b>So enumerate several variable choices before committing to "
    "one.</b> Write each down, sketch the constraints, and consider the "
    "relaxation. <b>This is the highest-leverage hour in an optimisation "
    "project, and it is routinely skipped</b> in favour of implementing "
    "the first formulation that comes to mind."]),
  ("table", ["Pattern", "Meaning", "What to watch for"],
   [["<b>Binary assignment</b>", "<b>x[i][j] = 1 if item i is assigned to "
     "resource j.</b>",
     "<b>Symmetry when the resources are identical</b> (Module 09 "
     "&sect;4) \u2014 n! equivalent solutions unless broken."],
    ["<b>Flow on arcs</b>", "How much of something moves along each arc.",
     "<b>Frequently totally unimodular, so prefer it where the problem "
     "permits</b> \u2014 the integrality comes free (Module 11 &sect;1)."],
    ["<b>Time-indexed</b>",
     "<b>x[i][t] = 1 if activity i starts at time t.</b>",
     "<b>Very large \u2014 one variable per activity per period \u2014 and "
     "the relaxation is strong.</b> <b>Frequently the better trade</b>, "
     "because a large model with a tight bound beats a compact one with a "
     "weak bound (Module 09 &sect;1)."],
    ["<b>Sequencing / precedence</b>",
     "y[i][j] = 1 if i precedes j.",
     "Requires transitivity constraints, which are numerous, and the "
     "relaxation is typically weak."],
    ["<b>Set selection</b>",
     "<b>One variable per feasible set, pattern, or route.</b>",
     "<b>Exponentially many variables</b> \u2014 generate them on demand by "
     "column generation, which is Module 04's duality used as an "
     "algorithm."]],
   [0.20, 0.36, 0.44]),

  ("h1", "2 &nbsp; Objectives"),
  ("callout", "The stated objective is rarely the real one",
   ["<b>'Minimise cost' almost always means 'minimise cost without "
    "anything unacceptable happening'</b> \u2014 and the set of "
    "unacceptable things is unstated, because it is obvious to the person "
    "who owns the problem and invisible to you.",
    "<b>So the first model produces a solution nobody will accept.</b> "
    "<b>That is informative rather than a failure:</b> every objection "
    "raised is a constraint that was missing, and it is far easier to "
    "elicit an objection to a concrete solution than a specification in "
    "the abstract.",
    "<b>So iterate deliberately.</b> Show the solution, collect the "
    "objections, encode them as constraints, re-solve. <b>The model "
    "converges on the real problem through rejection</b>, and three or "
    "four rounds is typical.",
    "<b>And a solution that is optimal and unacceptable is more useful "
    "than one that is feasible and mediocre</b>, because the first elicits "
    "the missing constraint and the second does not. <b>Deliberately "
    "producing an extreme solution early is a legitimate and underused "
    "technique.</b>"]),
  ("table", ["Approach", "How it works", "Is it honest?"],
   [["<b>Weighted sum</b>",
     "<b>Minimise w<sub>1</sub>f<sub>1</sub> + "
     "w<sub>2</sub>f<sub>2</sub>.</b>",
     "<b>It requires an exchange rate between the objectives</b> \u2014 how "
     "many pounds is an hour of delay worth? <b>State the rate "
     "explicitly</b>, because the weights encode it whether or not anyone "
     "examined them."],
    ["<b>Constrain all but one</b>",
     "<b>Minimise f<sub>1</sub> subject to f<sub>2</sub> &le; c.</b>",
     "<b>Usually the clearest formulation</b>, because c is a quantity the "
     "problem owner can reason about directly, and the dual variable on "
     "that constraint prices the trade (Module 04 &sect;2)."],
    ["<b>Pareto frontier</b>",
     "<b>Sweep the trade-off and plot the achievable combinations.</b>",
     "<b>The most honest \u2014 it shows the trade rather than hiding it "
     "in a weight</b>, and lets the owner choose a point. Costs one solve "
     "per point."],
    ["<b>Lexicographic</b>",
     "Optimise the first objective, fix it, then optimise the second.",
     "Appropriate when the priorities are genuinely strict rather than "
     "merely ordered."],
    ["<b>Goal programming</b>",
     "Penalise deviation from stated targets in each dimension.",
     "Useful when the owner has targets rather than preferences, which is "
     "common in practice."]],
   [0.19, 0.37, 0.44]),

  ("break",),
  ("h1", "3 &nbsp; Validating a model"),
  ("ul", ["<b>Solve a tiny instance by hand and compare.</b> Three items "
          "and two machines, worked on paper. <b>The most effective check "
          "available and the least often performed</b>, because it feels "
          "beneath the problem.",
          "<b>Check the extremes:</b> zero demand, infinite capacity, a "
          "single item, identical costs. <b>The answers should be obvious "
          "in advance, and they should be right</b> \u2014 a model that "
          "gets an obvious case wrong is wrong everywhere.",
          "<b>Look at the dual variables</b> (Module 04 &sect;2). <b>If a "
          "shadow price is absurd \u2014 an extra hour of a resource worth "
          "a million, or a binding constraint priced at zero \u2014 a "
          "constraint is wrong.</b> <b>This is the underused check</b>, "
          "and it localises the error to a specific constraint rather than "
          "merely signalling that something is off.",
          "<b>Perturb an input and check the answer moves sensibly</b> and "
          "in the right direction. Increase a cost and the solution should "
          "use less of that thing.",
          "<b>And show the solution to the person who owns the "
          "problem.</b> <b>They will spot in ten seconds what you would "
          "not find in a week</b> \u2014 a schedule that violates an "
          "unwritten rule, a route that passes a site that closed last "
          "year, an assignment that ignores a qualification requirement."]),
  ("callout", "Infeasible and unbounded are both diagnostics",
   ["<b>'Infeasible' usually means over-constrained rather than genuinely "
    "impossible.</b> Use an <b>irreducible infeasible subset</b> \u2014 "
    "most commercial solvers compute one on request \u2014 to find the "
    "minimal set of mutually conflicting constraints, which is almost "
    "always a small and illuminating set.",
    "<b>'Unbounded' almost always means a missing constraint</b>, and "
    "<b>it is a gift</b>: the solver has found a way to improve the "
    "objective without limit, <b>which tells you precisely what you forgot "
    "to forbid</b>. Reading the unbounded ray identifies the omission "
    "directly.",
    "<b>Add elastic variables with large penalties</b> to constraints you "
    "suspect, so the model becomes feasible and the solution reports "
    "<i>which</i> constraint it had to violate and by how much \u2014 "
    "which turns 'infeasible' into a ranked list of problems rather than a "
    "single unhelpful word.",
    "<b>And a suspiciously good objective value is the same signal as a "
    "suspiciously good test score</b> (CSCE 633 Module 12 &sect;1). "
    "<b>Audit before celebrating</b> \u2014 the usual cause is a missing "
    "constraint that permits something the real world does not."]),

  ("h1", "4 &nbsp; Where the model stops being the problem"),
  ("callout", "State where the model breaks",
   ["<b>Every model omits things.</b> Uncertain quantities are treated as "
    "known; human judgement is not encoded; dynamics are treated as static; "
    "rare events are excluded; and the objective is a proxy for something "
    "nobody can write down (CSCE 633 Module 01 &sect;3 made the same "
    "point about loss functions).",
    "<b>And optimisation exploits every simplification aggressively</b>, "
    "because it is explicitly searching for extremes. <b>A simplification "
    "that is harmless in a simulation \u2014 which samples typical "
    "behaviour \u2014 can be catastrophic in an optimum, which deliberately "
    "seeks the boundary.</b>",
    "<b>That is the specific hazard of this subject.</b> <b>The optimiser "
    "finds the corner of your model where it least resembles reality, and "
    "sits there</b>, because that is where the model says the best "
    "solution is. A schedule with no slack, a portfolio concentrated in "
    "whatever the model underestimated the risk of, a route that depends "
    "on every connection being on time.",
    "<b>So write the assumptions down and test the solution against "
    "them.</b> <b>'This model assumes demand is known exactly; under a 20% "
    "demand error the recommended solution costs 15% more than the "
    "alternative' is the deliverable</b> \u2014 not the optimum alone. "
    "<b>Stochastic and robust optimisation exist to address this "
    "formally</b>, and even without them, a sensitivity analysis and a "
    "stated assumption list is the difference between a usable "
    "recommendation and a trap."]),
 ],
 "resources": [
   ("Williams &mdash; Model Building in Mathematical Programming",
    "https://www.wiley.com/en-us/Model+Building+in+Mathematical+Programming%2C+5th+Edition-p-9781118443330",
    "<b>The reference for this module</b>, and one of very few books about "
    "formulation rather than algorithms. Library copy; it is worth "
    "seeking out."),
   ("Klotz & Newman &mdash; Practical Guidelines (free)",
    "https://www.sciencedirect.com/science/article/pii/S1876735413000020",
    "The &sect;3 diagnostics, including irreducible infeasible subsets and "
    "elastic formulations."),
   ("Boyd & Vandenberghe &mdash; Convex Optimization, chapters 4 and 7 "
    "(free)",
    "https://web.stanford.edu/~boyd/cvxbook/",
    "Worked formulations and the multi-objective material of &sect;2, "
    "including the Pareto frontier treatment."),
   ("Ben-Tal, El Ghaoui & Nemirovski &mdash; Robust Optimization",
    "https://press.princeton.edu/books/hardcover/9780691143682/robust-optimization",
    "<b>The formal response to &sect;4</b> \u2014 optimising against the "
    "worst case within an uncertainty set rather than against a point "
    "estimate."),
 ],
 "exercises": [
   "<b>Formulate one problem three ways</b> with different decision "
   "variables, and compare size, relaxation strength, and solve time.",
   "<b>Build a time-indexed and a sequencing formulation</b> of the same "
   "scheduling problem and compare.",
   "<b>Solve a tiny instance of your project model by hand</b> and compare "
   "against the solver.",
   "Check three extreme cases and verify the answers are obvious and "
   "correct.",
   "<b>Inspect every dual variable</b> and flag any that is implausible.",
   "<b>Deliberately make your model infeasible</b> and find the "
   "irreducible infeasible subset.",
   "<b>Make it unbounded</b> and identify the missing constraint from the "
   "ray.",
   "Add elastic variables and report which constraint the model most wants "
   "to violate.",
   "<b>Plot the Pareto frontier</b> for a two-objective version of your "
   "problem.",
   "<b>Write the assumption list</b> for your model and measure the "
   "solution's sensitivity to the two you least trust.",
 ],
 "selfcheck": [
   "Why does the variable choice decide tractability?",
   "Give five variable patterns and what to watch for in each.",
   "Why is the first model's unacceptable solution useful?",
   "Give five ways to handle multiple objectives and say which is most "
   "honest.",
   "Give five ways to validate a model, and which is underused.",
   "What do infeasible and unbounded each usually mean?",
   "Why does optimisation exploit simplifications more aggressively than "
   "simulation?",
   "What is the deliverable, beyond the optimum?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Solvers and Shipping",
 "subtitle": "Using the tools, and saying what you solved.",
 "question": "What should you use, and what can you claim?",
 "outcomes": [
     "Choose a solver and a modelling layer.",
     "Diagnose numerical trouble.",
     "Explain what has actually made solvers fast.",
     "Decide between exact and heuristic approaches.",
     "State what an optimisation result can honestly promise.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The stack",
   "blurb": "Modelling layer, solver, and what each does."},

  {"t": "table", "kicker": "Tools", "title": "What to use",
   "header": ["Layer", "Options", "Note"],
   "widths": [2.5, 4.4, 5.2],
   "rows": [
     ["<b>Modelling</b>", "<b>CVXPY, JuMP, Pyomo, AMPL</b>", "<b>Write the problem, not the algorithm</b>"],
     ["<b>LP / MIP</b>", "<b>HiGHS (free), Gurobi, CPLEX</b>", "<b>Commercial are 10\u2013100\u00d7 on hard instances</b>"],
     ["<b>Conic / SDP</b>", "SCS, ECOS, Mosek, Clarabel", "<b>Free options are adequate for moderate sizes</b>"],
     ["<b>Nonlinear</b>", "<b>IPOPT (free), KNITRO</b>", "Interior point (M07)"],
     ["Constraint programming", "<b>OR-Tools CP-SAT</b>", "<b>Excellent on scheduling; different paradigm</b>"],
     ["<b>Local search</b>", "Simulated annealing, tabu, LNS", "<b>No bound. Use when nothing else fits</b>"],
   ],
   "footnote": "<b>Academic licences are free for Gurobi, CPLEX, and "
               "Mosek</b>, and the gap on hard instances is large enough "
               "to matter.",
   "note": "CP-SAT deserves the mention; it beats MIP on many scheduling "
           "problems."},

  {"t": "callout", "title": "Use a modelling layer",
   "kind": "The practical advice",
   "body": ["<b>Write the problem in CVXPY or JuMP and let it talk to the "
            "solver</b>, rather than constructing matrices by hand.",
            "<b>You can then change solvers in one line</b>, which makes "
            "comparison trivial and prevents lock-in.",
            "<b>And the modelling layer catches errors</b> — CVXPY's DCP "
            "rules (Module 02 §2) reject non-convex "
            "formulations before the solver silently returns a local "
            "answer.",
            "<b>The cost is a translation overhead</b> on very large "
            "models, which matters only at a scale where you would be "
            "building matrices deliberately anyway."]},

  {"t": "section", "label": "Part 2", "title": "Numerical trouble",
   "blurb": "When the solver lies."},

  {"t": "bullets", "kicker": "Symptoms", "title": "Signs of numerical difficulty",
   "items": [
     "<b>Different solvers disagree</b> on the objective value. The "
     "clearest signal.",
     "",
     "<b>'Optimal' solutions that violate constraints</b> by small "
     "amounts \u2014 tolerances, not bugs.",
     "",
     "<b>Infeasibility reported on a problem you know is feasible.</b>",
     "",
     "<b>Results that change with the constraint ordering</b>, which "
     "should be irrelevant.",
     "",
     "<b>And a huge range of coefficient magnitudes</b> \u2014 the usual "
     "cause, and the one to check first.",
   ],
   "footnote": "<b>Solvers report a condition estimate</b>; look at it "
               "before concluding the model is wrong."},

  {"t": "callout", "title": "Scale the model",
   "kind": "The fix, almost always",
   "body": ["<b>Keep every coefficient within a few orders of "
            "magnitude</b> — rescale units so that money is in thousands "
            "and time in hours rather than mixing pence and years.",
            "<b>Avoid very large big-M values</b> (Module 09 §3) "
            "— they are both a numerical and a relaxation problem.",
            "<b>Remove redundant constraints</b>, which presolve mostly "
            "does and which you can help with.",
            "<b>And tighten variable bounds</b>, which improves "
            "conditioning and the relaxation together. <b>This is "
            "CSCE 620's robustness lesson and CSCE 633's feature scaling, "
            "arriving once more.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Exact or heuristic",
   "blurb": "The decision."},

  {"t": "table", "kicker": "Decision", "title": "When to abandon the guarantee",
   "header": ["Situation", "Approach", "Why"],
   "widths": [3.2, 3.6, 5.3],
   "rows": [
     ["<b>Convex</b>", "<b>Exact solver</b>", "<b>Polynomial. There is no reason not to</b>"],
     ["<b>Integer, solver terminates</b>", "<b>Exact, with a gap tolerance</b>", "<b>You get a bound. Take it</b>"],
     ["<b>Integer, solver does not terminate</b>", "<b>Reformulate first</b>", "<b>Formulation beats everything (M09)</b>"],
     ["<b>Still intractable</b>", "<b>Heuristic + the LP bound</b>", "<b>Report the gap you achieved</b>"],
     ["Black-box objective", "Bayesian optimisation", "No gradients, expensive evaluations"],
     ["<b>Needs an answer in milliseconds</b>", "<b>Heuristic, or precompute</b>", "Real-time scheduling, routing"],
   ],
   "footnote": "<b>Even when you use a heuristic, compute the LP bound</b> "
               "\u2014 it costs little and converts 'this is our answer' "
               "into 'within 7% of optimal'.",
   "note": "That advice is cheap and almost nobody follows it."},

  {"t": "section", "label": "Part 4", "title": "Claiming honestly",
   "blurb": "The course, and the semester, closed."},

  {"t": "bullets", "kicker": "Claims", "title": "What an optimisation result can honestly promise",
   "items": [
     "<b>'Optimal for this model, proved, with gap 0.0%.'</b> Note "
     "<i>for this model</i> \u2014 which is the load-bearing phrase.",
     "",
     "<b>'Within 2.3% of optimal; the bound is from the LP "
     "relaxation.'</b> The gap and its source.",
     "",
     "<b>'The binding constraints are capacity at sites 3 and 7; "
     "relaxing site 3 by one unit is worth \u00a3340.'</b>",
     "",
     "<b>'Assumes demand known; under 20% error the solution costs 15% "
     "more than the robust alternative.'</b>",
     "",
     "<b>And what you cannot say: 'optimal'</b> \u2014 unqualified, as "
     "though the model were the problem.",
   ],
   "footnote": "<b>'Optimal for this model' is the whole discipline of "
               "Module 12 compressed into four words.</b>"},

  {"t": "callout", "title": "Where this leaves you",
   "kind": "Closing the semester",
   "body": ["You can recognise convexity, construct and interpret a dual, "
            "formulate an integer program that solves, and derive an "
            "approximation guarantee.",
            "<b>And you know what the previous two courses were doing:</b> "
            "why gradient descent converges, why the condition number "
            "matters, why regularisation is a prior, and why kernels "
            "follow from the dual.",
            "<b>CSCE 633 gave the evaluation discipline, CSCE 636 the "
            "representations, and this course the theory under "
            "both.</b>",
            "<b>And the closing rule has not changed in nine "
            "courses:</b> <b>state what you measured, state what you "
            "assumed, and never claim more than you established.</b>"]},
 ],
 "takeaways": [
   "Write the problem in a modelling layer and let it talk to the solver "
   "\u2014 you can then change solvers in one line.",
   "CVXPY's DCP rules reject non-convex formulations before a solver "
   "silently returns a local answer.",
   "Numerical trouble usually comes from a wide range of coefficient "
   "magnitudes, and scaling the model is almost always the fix.",
   "Even when you use a heuristic, compute the LP bound \u2014 it converts "
   "'this is our answer' into 'within 7% of optimal'.",
   "Commercial solvers are 10\u2013100\u00d7 faster on hard instances and "
   "have free academic licences.",
   "'Optimal for this model' is the honest claim; unqualified 'optimal' "
   "treats the model as the problem.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The stack"),
  ("table", ["Layer", "Options", "Note"],
   [["<b>Modelling layer</b>", "<b>CVXPY, JuMP (Julia), Pyomo, AMPL, "
     "GAMS.</b>",
     "<b>You write the problem; the layer writes the solver input.</b> "
     "See the callout."],
    ["<b>Linear and mixed-integer</b>",
     "<b>HiGHS (free and genuinely good), Gurobi, CPLEX, SCIP.</b>",
     "<b>The commercial solvers are 10 to 100&times; faster on hard "
     "instances</b> \u2014 a real gap, from decades of cut generation, "
     "presolve, and heuristics (Module 09 &sect;4). <b>Academic licences "
     "are free.</b>"],
    ["<b>Conic and semidefinite</b>", "SCS, ECOS, Clarabel, Mosek.",
     "<b>The free options are adequate at moderate sizes</b>; Mosek is "
     "substantially better on large semidefinite programs (Module 10 "
     "&sect;3)."],
    ["<b>Nonlinear</b>", "<b>IPOPT (free), KNITRO, SNOPT.</b>",
     "Interior point methods (Module 07 &sect;3), with the caveat that "
     "non-convex problems get local answers."],
    ["<b>Constraint programming</b>", "<b>OR-Tools CP-SAT.</b>",
     "<b>A different paradigm \u2014 propagation and clause learning "
     "rather than relaxation \u2014 and it beats mixed-integer solvers on "
     "many scheduling and sequencing problems.</b> Worth trying on any "
     "problem that is mostly combinatorial."],
    ["<b>Local search</b>",
     "Simulated annealing, tabu search, large neighbourhood search.",
     "<b>No bound, so no guarantee</b> \u2014 use when nothing else fits, "
     "and still compute a bound separately (&sect;3)."]],
   [0.17, 0.37, 0.46]),
  ("callout", "Use a modelling layer",
   ["<b>Write the problem in CVXPY, JuMP, or Pyomo and let it construct "
    "the solver's input</b>, rather than assembling constraint matrices by "
    "hand \u2014 which is error-prone, unreadable, and ties you to one "
    "solver.",
    "<b>You can then change solvers in a single line</b>, which makes "
    "comparison trivial and prevents lock-in to a commercial licence you "
    "may later lose. <b>Trying three solvers on a hard instance costs "
    "minutes and is frequently decisive.</b>",
    "<b>And the modelling layer catches errors.</b> <b>CVXPY's DCP rules "
    "(Module 02 &sect;2) reject a non-convex formulation at build time, "
    "rather than passing it to a solver that will silently return a local "
    "answer presented as optimal</b> \u2014 which is exactly the failure "
    "mode that makes non-convex results untrustworthy.",
    "<b>The cost is a translation overhead on very large models</b>, which "
    "becomes significant only at a scale where you would be constructing "
    "the matrices deliberately and carefully anyway. <b>For everything "
    "else the layer is free.</b>"]),

  ("h1", "2 &nbsp; Numerical trouble"),
  ("ul", ["<b>Different solvers disagree on the objective value.</b> "
          "<b>The clearest possible signal</b> that something is "
          "numerically wrong, and the reason to keep more than one solver "
          "available.",
          "<b>'Optimal' solutions that violate constraints by small "
          "amounts.</b> Solvers work to a feasibility tolerance, so a "
          "violation of 10<super>&minus;6</super> is expected \u2014 but if "
          "your constraint represents something that must hold exactly, the "
          "tolerance is a correctness problem and must be handled "
          "explicitly.",
          "<b>Infeasibility reported on a problem you know to be "
          "feasible</b>, or feasibility reported on one you know is not.",
          "<b>Results that change when you reorder the constraints</b>, "
          "which should be irrelevant and is a reliable sign of "
          "ill-conditioning.",
          "<b>And a huge range of coefficient magnitudes</b> \u2014 "
          "<b>the usual cause, and the first thing to check</b>. <b>Solvers "
          "report a condition estimate and a coefficient range statistic; "
          "look at them before concluding the model is wrong.</b>"]),
  ("callout", "Scale the model",
   ["<b>Keep every coefficient within a few orders of magnitude.</b> "
    "Rescale the units so that money is in thousands rather than pence and "
    "time is in hours rather than seconds \u2014 mixing units across six "
    "orders of magnitude is the usual way a model becomes ill-conditioned.",
    "<b>Avoid very large big-M values</b> (Module 09 &sect;3). <b>They "
    "are simultaneously a numerical problem and a relaxation-strength "
    "problem</b>, which is why tightening them pays twice.",
    "<b>Remove redundant constraints.</b> Presolve does most of this "
    "automatically, and helping it \u2014 by not writing the same "
    "restriction twice in different forms \u2014 costs nothing.",
    "<b>And tighten variable bounds wherever the problem justifies "
    "it</b>, which improves the conditioning and the relaxation together. "
    "<b>This is CSCE 620 Module 01's robustness lesson and CSCE 633 "
    "Module 02's feature scaling arriving for a third time</b> \u2014 "
    "<b>the same underlying fact about floating-point arithmetic, surfacing "
    "in three different subjects</b>, which at this point in the program "
    "should be read as a general property rather than a coincidence."]),

  ("break",),
  ("h1", "3 &nbsp; Exact or heuristic"),
  ("table", ["Situation", "Approach", "Why"],
   [["<b>The problem is convex</b>", "<b>An exact solver.</b>",
     "<b>Polynomial time, a certificate of optimality, and no reason "
     "whatsoever to do anything else</b> (Module 01 &sect;1)."],
    ["<b>Integer, and the solver terminates</b>",
     "<b>Exact, with a gap tolerance of perhaps 1%.</b>",
     "<b>You get a proven bound</b> \u2014 take it (Module 09 &sect;1)."],
    ["<b>Integer, and the solver does not terminate</b>",
     "<b>Reformulate before anything else.</b>",
     "<b>Formulation strength beats every other intervention</b> "
     "(Module 09 &sect;4) \u2014 tighten big-Ms, break symmetry, consider "
     "a different variable choice (Module 12 &sect;1)."],
    ["<b>Still intractable after reformulation</b>",
     "<b>A heuristic, plus the LP bound computed separately.</b>",
     "<b>Report the gap you achieved</b> \u2014 see below."],
    ["<b>Black-box objective, expensive to evaluate</b>",
     "Bayesian optimisation or a derivative-free method.",
     "No gradients available and each evaluation costs real money or time "
     "(CSCE 633 Module 04 &sect;3)."],
    ["<b>An answer is needed in milliseconds</b>",
     "<b>A heuristic, or precompute a policy offline.</b>",
     "Real-time dispatch, routing, and control \u2014 where an optimal "
     "answer that arrives late is worth nothing (CSCE 678 Module 06 "
     "&sect;4's argument, again)."]],
   [0.24, 0.29, 0.47]),
  ("p", "<b>Even when you use a heuristic, compute the LP bound.</b> It "
        "costs a single additional solve of a relaxation you have already "
        "written, <b>and it converts 'this is our answer' into 'this is "
        "within 7% of the best possible answer'</b> \u2014 a categorically "
        "stronger claim. <b>This advice is cheap and almost nobody follows "
        "it</b>, which means a great deal of heuristic optimisation is "
        "reported with no idea of how good it is."),

  ("h1", "4 &nbsp; Claiming honestly"),
  ("ul", ["<b>'Optimal for this model, proved, with a reported gap of "
          "0.0%.'</b> <b>Note <i>for this model</i></b> \u2014 which is "
          "the load-bearing phrase, and which Module 12 &sect;4 is "
          "entirely about.",
          "<b>'Within 2.3% of optimal; the bound comes from the LP "
          "relaxation after 600 seconds.'</b> The gap, its source, and the "
          "budget that produced it.",
          "<b>'The binding constraints are capacity at sites 3 and 7; "
          "relaxing site 3 by one unit is worth &pound;340 per week.'</b> "
          "<b>The dual variables, interpreted in the problem's own "
          "vocabulary</b> (Module 04 &sect;2) \u2014 which is frequently "
          "more valuable to the problem owner than the solution itself.",
          "<b>'This model assumes demand is known exactly. Under a 20% "
          "demand error, the recommended solution costs 15% more than the "
          "robust alternative.'</b> <b>The assumption and its "
          "consequence</b> (Module 12 &sect;4).",
          "<b>And what you cannot honestly say: 'optimal'</b>, unqualified, "
          "as though the model were the problem. <b>'Optimal for this "
          "model' is the whole discipline of Module 12 compressed into four "
          "words</b>, and the difference between the two phrasings is where "
          "optimisation projects fail."]),
  ("callout", "Where this leaves you",
   ["<b>You can recognise convexity and say what it guarantees, construct "
    "and interpret a dual, formulate an integer program that actually "
    "solves, derive an approximation guarantee from a relaxation, and "
    "recognise when a combinatorial problem has exploitable "
    "structure.</b>",
    "<b>And you know what the previous two courses were doing.</b> Why "
    "gradient descent converges and at what rate; why the condition number "
    "governs it; why regularisation is a prior and simultaneously a "
    "conditioning improvement; why the lasso produces exact zeros; and why "
    "kernels follow from taking the dual rather than being an independent "
    "invention.",
    "<b>CSCE 633 supplied the evaluation discipline, CSCE 636 supplied "
    "the representations, and this course supplied the theory underneath "
    "both</b> \u2014 which is why the semester was ordered as it was, with "
    "the practice first and the explanation after.",
    "<b>And the closing rule has not changed across nine consecutive "
    "courses:</b> <b>state what you measured, state what you assumed, and "
    "never claim more than you established.</b> <b>In this course it "
    "takes the form 'optimal for this model'</b> \u2014 four words that "
    "carry the entire difference between a result and an overreach."]),
 ],
 "resources": [
   ("Mittelmann &mdash; Benchmarks for Optimization Software (free)",
    "https://plato.asu.edu/bench.html",
    "<b>Independent, current solver benchmarks</b> across every problem "
    "class \u2014 the honest basis for the &sect;1 table."),
   ("CVXPY, JuMP, and Pyomo documentation (free)",
    "https://www.cvxpy.org/",
    "The &sect;1 modelling layers, with examples. JuMP's documentation is "
    "unusually good on solver interchange."),
   ("Google OR-Tools &mdash; CP-SAT documentation (free)",
    "https://developers.google.com/optimization/cp",
    "<b>The &sect;1 constraint programming option</b>, which is "
    "under-known and frequently wins on scheduling."),
   ("Klotz & Newman &mdash; Practical Guidelines for Solving Difficult "
    "Linear Programs (free)",
    "https://www.sciencedirect.com/science/article/pii/S1876735413000020",
    "<b>The &sect;2 numerical diagnostics</b>, from people who support "
    "solver users for a living."),
 ],
 "exercises": [
   "<b>Solve the same model with three different solvers</b> and compare "
   "times and reported objectives.",
   "<b>Deliberately construct an ill-conditioned model</b> with "
   "coefficients spanning eight orders of magnitude, and observe the "
   "solvers disagree.",
   "<b>Rescale it</b> and show the disagreement resolves.",
   "Check the solver's reported condition estimate before and after.",
   "<b>Solve a scheduling problem with a MIP solver and with CP-SAT</b> "
   "and compare.",
   "<b>Implement a local search heuristic</b> for a problem you cannot "
   "solve exactly.",
   "<b>Compute the LP bound separately</b> and report your heuristic's "
   "gap.",
   "Take a result you produced earlier this semester and <b>rewrite the "
   "claim</b> to meet &sect;4's standard.",
   "Find an optimisation claim in a paper or a vendor document and assess "
   "whether 'optimal' was qualified.",
   "<b>Project 2 is now due.</b> Submit the formulation, the relaxation "
   "and gap, the branch-and-bound results with and without your cuts, the "
   "approximation or heuristic comparison, and the honest claim.",
 ],
 "selfcheck": [
   "Name the layers of the optimisation stack and an option for each.",
   "Give three reasons to use a modelling layer.",
   "Name five symptoms of numerical trouble.",
   "What is the usual cause, and what is the fix?",
   "Give six situations and the exact-or-heuristic decision for each.",
   "Why compute the LP bound even when using a heuristic?",
   "Give four honest claims and the one thing you cannot say.",
 ],
},

]
