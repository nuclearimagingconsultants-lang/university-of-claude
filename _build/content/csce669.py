# -*- coding: utf-8 -*-
"""CSCE 669 Computational Optimization — original course content."""

COURSE = {
    "code": "CSCE 669",
    "title": "Computational Optimization",
    "tagline": "Convexity, duality, and relaxation — the theory "
               "underneath everything the last two courses did "
               "empirically",
    "term": "Semester 6 (with CSCE 633 and CSCE 636)",
    "prereqs": "CSCE 629 Analysis of Algorithms; linear algebra and "
               "multivariable calculus; CSCE 633 is helpful for "
               "motivation",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A real problem modelled as an optimisation program, "
                   "solved three ways, with the formulation justified, the "
                   "dual interpreted, and an honest account of where the "
                   "model stops matching the problem",
    "description": [
        "CSCE 633 and CSCE 636 ran gradient descent on things and "
        "reported what happened. <b>This course is about why it works, "
        "when it provably works, and what to do when it provably "
        "does not.</b>",
        "<b>The organising distinction is convexity.</b> A convex problem "
        "has one minimum, local information suffices to find it, and "
        "efficient algorithms with proven convergence rates exist. A "
        "non-convex problem has none of those guarantees. <b>Module 02 is "
        "about recognising which you have</b>, because that single "
        "determination tells you more about what is possible than any "
        "other property of a problem.",
        "The second theme is <b>duality</b>, which is the most useful idea "
        "in the subject and the least intuitive. <b>Every minimisation "
        "has a shadow maximisation whose value bounds it</b>, whose "
        "variables price the constraints, and whose solution certifies "
        "optimality. <b>Module 04 develops it for linear programs and "
        "Module 06 generalises it</b>, and the pattern recurs in support "
        "vector machines, in network flow, in economics, and in the "
        "approximation guarantees of Module 10.",
        "The third is that <b>modelling is the hard part and the "
        "under-taught part</b>. Solvers are excellent and freely "
        "available; the difficulty is turning a messy real objective into "
        "a program whose solution means something. <b>Module 12 is "
        "entirely about that translation</b>, and it is where most of the "
        "value in applied optimisation actually sits.",
    ],
    "outcomes": [
        "Recognise convexity and explain what it guarantees.",
        "Formulate and solve linear programs.",
        "Construct and interpret a dual, including shadow prices.",
        "State convergence rates for the first-order methods and what "
        "they depend on.",
        "Apply KKT conditions to constrained problems.",
        "Explain why interior point methods made linear programming "
        "polynomial in practice.",
        "Explain stochastic gradient convergence and variance "
        "reduction.",
        "Apply branch and bound and LP relaxation to integer programs.",
        "Derive an approximation guarantee from a relaxation.",
        "Model a real problem and say where the model fails.",
    ],
    "materials": [
        ("Boyd & Vandenberghe — Convex Optimization (free book) and "
         "Stanford EE364A (free lectures)",
         "https://web.stanford.edu/~boyd/cvxbook/",
         "<b>The primary source.</b> Free book, free video lectures, free "
         "problem sets with solutions. Modules 02 through 07 follow its "
         "development closely, and the modelling chapter informs "
         "Module 12."),
        ("MIT 15.093 — Optimization Methods (free, OCW)",
         "https://ocw.mit.edu/courses/15-093j-optimization-methods-fall-2009/",
         "<b>Stronger on linear and integer programming</b> than Boyd, "
         "which is convex-first. The reference for Modules 03, 09, and "
         "11."),
        ("Nocedal & Wright — Numerical Optimization",
         "https://link.springer.com/book/10.1007/978-0-387-40065-5",
         "The reference for the algorithmic detail of Modules 05 and 07 "
         "— line searches, trust regions, quasi-Newton. Library "
         "copy."),
        ("Williamson & Shmoys — The Design of Approximation "
         "Algorithms (free PDF)",
         "https://www.designofapproxalgs.com/",
         "<b>Free in full, and the reference for Module 10.</b> The LP "
         "rounding and randomised rounding chapters are the relevant "
         "ones."),
        ("CVXPY documentation and examples (free)",
         "https://www.cvxpy.org/",
         "<b>Disciplined convex programming</b> — a modelling "
         "language that refuses to accept a problem it cannot verify is "
         "convex, which is itself instructive."),
        ("Bixby — A Brief History of Linear Programming Computation "
         "(free)",
         "https://www.documents.clrc.ac.uk/",
         "<b>The Module 13 material:</b> solvers improved by roughly as "
         "much from algorithms as from hardware, over the same period."),
    ],
    "tooling": [
        "<b>Python with CVXPY and SciPy.</b> <b>CVXPY will refuse a "
        "non-convex formulation</b>, which teaches you convexity faster "
        "than any exercise.",
        "<b>A real solver:</b> HiGHS (free, excellent) for linear and "
        "integer programs; SCS or ECOS for conic problems. <b>Gurobi and "
        "Mosek have free academic licences</b> and are substantially "
        "faster on hard instances.",
        "<b>Implement the core algorithms yourself first</b> — "
        "gradient descent, simplex, branch and bound — then use the "
        "solver. The same pattern as the rest of this program.",
        "<b>A plotting setup for convergence curves</b>, on log axes. "
        "<b>Convergence rates are visible as slopes and invisible as "
        "tables.</b>",
        "<b>A problem you actually care about.</b> Module 12's project "
        "requires one, and a textbook instance will not expose the "
        "modelling difficulties.",
        "<b>Exact rational arithmetic available</b> for checking small "
        "instances — <b>linear programming is numerically delicate</b> "
        "and CSCE 620's lesson applies.",
    ],
    "projects": [
        {"title": "Model it, solve it, dualise it", "after": 7,
         "brief": "Take a real problem, formulate it as a mathematical "
                  "program, solve it three ways, and interpret the dual.",
         "reqs": [
             "<b>A written formulation</b>: decision variables, objective, "
             "constraints, each justified against the real problem.",
             "<b>A proof or argument that the problem is or is not "
             "convex.</b>",
             "Solved by your own implementation, by a general-purpose "
             "solver, and by a specialised one if applicable.",
             "<b>The dual written out and interpreted in the problem's own "
             "terms</b> — what does each dual variable price?",
             "<b>A sensitivity analysis</b>: which constraints bind, and "
             "what would relaxing each be worth?",
             "Convergence curves on log axes for the iterative method.",
         ],
         "done": [
             "<b>The three solutions agree</b>, or you can explain "
             "precisely why they do not.",
             "<b>The dual variables interpreted in the problem's "
             "vocabulary</b>, not in mathematical terms — 'an extra "
             "hour of machine time is worth $34'.",
             "<b>A statement of which constraints are binding</b> and what "
             "that tells the problem owner.",
             "<b>An account of where the model diverges from the real "
             "problem</b>, which is graded and is the point of the "
             "exercise.",
         ]},
        {"title": "When it is not convex", "after": 12,
         "brief": "Take a problem that is integer, combinatorial, or "
                  "genuinely non-convex, and get a usable answer with a "
                  "bound.",
         "reqs": [
             "<b>An integer or combinatorial formulation</b> of a problem "
             "you care about.",
             "<b>The LP relaxation solved, and the integrality gap "
             "measured.</b>",
             "Branch and bound implemented, with the node count reported.",
             "<b>At least one cut or one valid inequality</b> added, with "
             "its effect on the node count measured.",
             "<b>An approximation algorithm with a proven ratio</b>, or a "
             "heuristic with a measured gap against the bound.",
             "A comparison against a commercial or open solver.",
         ],
         "done": [
             "<b>A bound as well as a solution</b> — 'within 3% of "
             "optimal' is a far stronger claim than a number.",
             "<b>Node counts with and without your cuts</b>, measured.",
             "<b>The integrality gap reported</b>, with a comment on "
             "whether the relaxation was tight.",
             "<b>An honest comparison against the solver</b>, which will "
             "probably win. Report by how much.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "The Shape of the Problem",
 "subtitle": "What determines whether it can be solved.",
 "question": "What makes one optimisation problem easy and another "
             "intractable?",
 "outcomes": [
     "State the general optimisation problem and its components.",
     "Explain why convexity is the dividing line.",
     "Classify the standard problem families by difficulty.",
     "Explain what local information can and cannot establish.",
     "Recognise optimisation problems in disguise.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The general problem",
   "blurb": "Three components, and the difficulty is in their shape."},

  {"t": "eq", "kicker": "The problem", "title": "Stated generally",
   "eqs": [
     ("minimise  f(x)   over  x ∈ ℝⁿ",
      "The objective. Maximisation is minimising −f."),
     ("subject to  gᵢ(x) ≤ 0,  hⱼ(x) = 0",
      "Inequality and equality constraints. Together they define the "
      "feasible set."),
     ("Difficulty depends on the SHAPE of f and the feasible set",
      "Not on the number of variables. A million-variable convex problem "
      "is easier than a fifty-variable integer one."),
   ],
   "caption": "<b>The third line is the whole subject.</b> Size is "
              "secondary; structure decides everything.",
   "note": "Students expect difficulty to scale with n; it does not."},

  {"t": "callout", "title": "The dividing line is convexity, not linearity",
   "kind": "The claim this course rests on",
   "body": ["<b>For a convex problem, every local minimum is a global "
            "minimum.</b> So an algorithm that only ever looks nearby can "
            "nonetheless certify a global answer.",
            "<b>And that is the only reason local methods work.</b> "
            "Gradient descent sees a neighbourhood; convexity is what "
            "licenses a global conclusion from local evidence.",
            "<b>Without it, finding a global minimum is intractable in "
            "general</b> — you cannot rule out a better point somewhere "
            "you have not looked.",
            "<b>So the first question about any optimisation problem is "
            "'is it convex?'</b> and the answer determines what kind of "
            "guarantee is available at all. <b>Linearity is a special case "
            "and is not the relevant boundary.</b>"]},

  {"t": "section", "label": "Part 2", "title": "The hierarchy",
   "blurb": "What is solvable, and how fast."},

  {"t": "table", "kicker": "Families", "title": "The standard problem classes",
   "header": ["Class", "Form", "Difficulty"],
   "widths": [2.7, 4.3, 5.1],
   "rows": [
     ["<b>Least squares</b>", "<b>Minimise ‖Ax − b‖&#178;</b>", "<b>Closed form. Solved (CSCE 633 M02)</b>"],
     ["<b>Linear program</b>", "<b>Linear objective and constraints</b>", "<b>Polynomial; solvers handle millions of variables</b>"],
     ["<b>Quadratic program</b>", "Convex quadratic objective, linear constraints", "<b>Polynomial. SVMs are these (CSCE 633 M07)</b>"],
     ["<b>Conic / SDP</b>", "<b>Over cones; semidefinite constraints</b>", "<b>Polynomial, slower; powerful relaxations</b>"],
     ["<b>General convex</b>", "Convex f over a convex set", "<b>Polynomial, given an oracle</b>"],
     ["<b>Integer program</b>", "<b>Some variables must be integers</b>", "<b>NP-hard. Solved anyway, in practice (M09)</b>"],
     ["<b>General non-convex</b>", "No structure assumed", "<b>No global guarantee. CSCE 636's territory</b>"],
   ],
   "footnote": "<b>The boundary is between rows 5 and 6</b>, and it is a "
               "boundary of guarantee rather than of practice — "
               "integer programs are solved daily.",
   "note": "That the hard boundary doesn't match the practical one is "
           "important."},

  {"t": "callout", "title": "NP-hard does not mean unsolvable",
   "kind": "The distinction that matters practically",
   "body": ["<b>NP-hardness is a statement about worst-case behaviour on "
            "all instances</b>, including adversarial ones that nobody "
            "encounters.",
            "<b>Real instances have structure</b> — sparsity, symmetry, "
            "near-integrality — that solvers exploit aggressively.",
            "<b>So integer programs with hundreds of thousands of "
            "variables are solved routinely in industry</b>, while "
            "carefully constructed small ones remain open.",
            "<b>The practical question is not 'is it NP-hard?' but 'does "
            "the solver terminate on my instances?'</b> — which is an "
            "empirical question, answered by trying it. <b>CSCE 629's "
            "complexity classes bound the worst case, not your "
            "Tuesday.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Local information",
   "blurb": "What a gradient can and cannot tell you."},

  {"t": "callout", "title": "A gradient is a local statement",
   "kind": "What descent methods actually know",
   "body": ["<b>The gradient says which direction decreases f "
            "fastest</b> — <i>right here</i>. It says nothing about the "
            "function anywhere else.",
            "<b>So a point where the gradient vanishes is "
            "<i>stationary</i></b>, which could be a minimum, a maximum, "
            "or a saddle.",
            "<b>The Hessian distinguishes them locally</b> — positive "
            "definite means a local minimum — and still says nothing "
            "global.",
            "<b>Convexity is the bridge.</b> <b>For a convex function, "
            "stationary implies globally minimal</b>, and that single "
            "implication is what turns a local algorithm into a global "
            "method."]},

  {"t": "section", "label": "Part 4", "title": "Recognising them",
   "blurb": "Optimisation problems in disguise."},

  {"t": "bullets", "kicker": "In disguise", "title": "Things that are optimisation problems",
   "items": [
     "<b>Fitting a model</b> — minimise loss over parameters "
     "(CSCE 633).",
     "",
     "<b>Scheduling, routing, assignment</b> — integer programs, "
     "almost always.",
     "",
     "<b>Maximum likelihood</b> — minimise negative log-likelihood "
     "(CSCE 633 M10).",
     "",
     "<b>Shortest path, max flow, matching</b> — linear programs "
     "with integral optima (CSCE 629, Module 11).",
     "",
     "<b>Inverse rendering</b> — minimise image difference over "
     "scene parameters (CSCE 636 M11).",
     "",
     "<b>And portfolio choice, control, and equilibrium</b>, which is "
     "why this subject is shared with economics and engineering.",
   ],
   "footnote": "<b>Recognising a problem as an optimisation problem is "
               "most of solving it</b>, because then a century of "
               "machinery applies."},
 ],
 "takeaways": [
   "Difficulty depends on the shape of the objective and the feasible set, "
   "not on the number of variables.",
   "Convexity is the dividing line because it licenses a global conclusion "
   "from local evidence — which is why local methods work at all.",
   "Linearity is a special case and is not the relevant boundary.",
   "NP-hardness bounds the worst case, and real instances have structure "
   "solvers exploit — integer programs with hundreds of thousands of "
   "variables are solved daily.",
   "A gradient is a purely local statement; the Hessian distinguishes "
   "stationary points locally and still says nothing global.",
   "Recognising a problem as an optimisation problem is most of solving it, "
   "because a century of machinery then applies.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The general problem"),
  ("eq", "min f(x) &nbsp; s.t. &nbsp; g<sub>i</sub>(x) &le; 0, &nbsp; "
         "h<sub>j</sub>(x) = 0"),
  ("p", "Three components: an <b>objective</b> f to minimise (maximisation "
        "is minimising &minus;f, so nothing is lost), <b>inequality "
        "constraints</b>, and <b>equality constraints</b>. The constraints "
        "together define the <b>feasible set</b>. <b>The difficulty of the "
        "problem depends on the <i>shape</i> of f and of the feasible set, "
        "not on the number of variables</b> — a convex problem in a "
        "million variables is routinely solved, and a carefully "
        "constructed integer problem in fifty variables can be open. "
        "<b>That inversion of the expected relationship between size and "
        "difficulty is the first thing to internalise</b>, because it "
        "redirects effort from reducing dimensionality to improving "
        "structure."),
  ("callout", "The dividing line is convexity, not linearity",
   ["<b>For a convex problem, every local minimum is a global minimum.</b> "
    "There are no other candidates to rule out — the geometry forbids "
    "them.",
    "<b>And that is the only reason local methods work.</b> Gradient "
    "descent sees a neighbourhood and nothing more; <b>convexity is "
    "precisely what licenses the inference from 'I cannot improve locally' "
    "to 'this is the best point anywhere'.</b> Without it the inference is "
    "invalid, and every algorithm in this course that offers a guarantee "
    "offers it on the strength of this single property.",
    "<b>Without convexity, finding a global minimum is intractable in "
    "general.</b> You cannot rule out a better point in a region you have "
    "not examined, and the number of regions is exponential.",
    "<b>So the first question about any optimisation problem is 'is it "
    "convex?'</b>, and the answer determines what kind of guarantee is "
    "available at all — before any question of which algorithm to "
    "use. <b>Linearity is a special case of convexity and is not the "
    "relevant boundary</b>, which is a correction worth making early "
    "because the historical development (linear programming first) "
    "suggests otherwise."]),

  ("h1", "2 &nbsp; The hierarchy"),
  ("table", ["Class", "Form", "Difficulty"],
   [["<b>Least squares</b>",
     "<b>minimise &#8214;Ax &minus; b&#8214;&#178;</b>",
     "<b>Closed form</b> — the normal equations, though not computed "
     "that way (CSCE 633 Module 02 &sect;1). A solved problem."],
    ["<b>Linear program</b>",
     "<b>Linear objective, linear constraints.</b>",
     "<b>Polynomial time</b>, and modern solvers handle millions of "
     "variables. Modules 03, 04, 07."],
    ["<b>Quadratic program</b>",
     "Convex quadratic objective, linear constraints.",
     "<b>Polynomial.</b> <b>Support vector machines are exactly this</b> "
     "(CSCE 633 Module 07), as are many control and finance problems."],
    ["<b>Conic and semidefinite programs</b>",
     "<b>Optimisation over convex cones; constraints requiring a matrix to "
     "be positive semidefinite.</b>",
     "<b>Polynomial but slower.</b> <b>The source of the strongest known "
     "relaxations</b> for hard combinatorial problems (Module 10)."],
    ["<b>General convex</b>", "Convex f over a convex set.",
     "<b>Polynomial, given an oracle for f and its subgradients</b> "
     "— the ellipsoid method establishes this, and interior point "
     "methods make it practical."],
    ["<b>Integer program</b>",
     "<b>Some or all variables constrained to integers.</b>",
     "<b>NP-hard</b> — and solved routinely in practice (Module 09). "
     "See the callout."],
    ["<b>General non-convex continuous</b>", "No structure assumed.",
     "<b>No global guarantee available.</b> <b>CSCE 636's territory</b>, "
     "where the practice runs well ahead of the theory."]],
   [0.19, 0.34, 0.47]),
  ("callout", "NP-hard does not mean unsolvable",
   ["<b>NP-hardness is a statement about worst-case behaviour across all "
    "instances</b>, including adversarially constructed ones that arise "
    "nowhere outside complexity proofs (CSCE 629).",
    "<b>Real instances have structure.</b> Sparsity, symmetry, block "
    "structure, near-integral relaxations, and good warm starts — and "
    "commercial solvers exploit all of it aggressively, with decades of "
    "accumulated heuristics.",
    "<b>So integer programs with hundreds of thousands of variables are "
    "solved to optimality daily in logistics, scheduling, and "
    "manufacturing</b>, while carefully constructed instances with a few "
    "dozen variables remain intractable.",
    "<b>The practical question is therefore not 'is this problem class "
    "NP-hard?' but 'does the solver terminate on <i>my</i> "
    "instances?'</b> — which is an empirical question answered by "
    "trying it, not a theoretical one answered by classification. "
    "<b>CSCE 629's complexity classes bound the worst case, not your "
    "Tuesday</b>, and treating NP-hardness as a reason not to attempt a "
    "formulation is a common and costly error."]),

  ("break",),
  ("h1", "3 &nbsp; What local information establishes"),
  ("callout", "A gradient is a local statement",
   ["<b>The gradient gives the direction of steepest increase of f at a "
    "point</b> — <i>at that point</i>. It is a derivative: it "
    "describes the function's behaviour in an infinitesimal neighbourhood "
    "and says nothing whatsoever about the function elsewhere.",
    "<b>So a point where the gradient vanishes is <i>stationary</i></b>, "
    "which may be a local minimum, a local maximum, or a saddle point "
    "— and in high dimensions, overwhelmingly the last (CSCE 636 "
    "Module 03 &sect;4).",
    "<b>The Hessian distinguishes them locally:</b> positive definite "
    "means a strict local minimum, negative definite a maximum, indefinite "
    "a saddle. <b>This is still entirely local information</b> and "
    "establishes nothing about the global landscape.",
    "<b>Convexity is the bridge between the two.</b> <b>For a convex "
    "function, stationary implies globally minimal</b> — and that "
    "single implication is what converts a local algorithm into a global "
    "method with a certificate. <b>Everything in Modules 05 through 07 "
    "depends on it</b>, and Module 02 is about establishing it."]),

  ("h1", "4 &nbsp; Optimisation problems in disguise"),
  ("ul", ["<b>Fitting a model</b> — minimise a loss over parameters "
          "(CSCE 633 Module 01). The entire previous two courses are "
          "instances of this course's subject.",
          "<b>Scheduling, routing, assignment, packing, and covering</b> "
          "— integer programs almost without exception, and the "
          "largest commercial application of the subject.",
          "<b>Maximum likelihood estimation</b> — minimise the "
          "negative log-likelihood (CSCE 633 Module 10 &sect;1), which is "
          "convex for the exponential family and not in general.",
          "<b>Shortest path, maximum flow, and bipartite matching</b> "
          "— <b>linear programs whose optima happen to be integral</b> "
          "(CSCE 629, and Module 11), which is why they are easy when "
          "general integer programs are not.",
          "<b>Inverse rendering</b> — minimise the difference between "
          "a rendered image and a photograph, over scene parameters "
          "(CSCE 636 Module 11). Non-convex, and solved by gradient "
          "descent anyway.",
          "<b>And portfolio selection, optimal control, and economic "
          "equilibrium</b> — which is why this subject is shared "
          "between computer science, operations research, engineering, and "
          "economics, and why its vocabulary comes from all four. "
          "<b>Recognising a problem as an optimisation problem is most of "
          "solving it</b>, because at that moment a century of machinery "
          "becomes applicable."]),
 ],
 "resources": [
   ("Boyd & Vandenberghe &mdash; Convex Optimization, chapter 1 (free)",
    "https://web.stanford.edu/~boyd/cvxbook/",
    "<b>The &sect;1 and &sect;2 framing</b>, and the clearest available "
    "statement of why convexity rather than linearity is the boundary."),
   ("Stanford EE364A &mdash; lecture 1 (free video)",
    "https://www.youtube.com/playlist?list=PL3940DD956CDF0622",
    "Boyd lecturing the same material. Worth watching alongside the "
    "chapter."),
   ("MIT 15.093 &mdash; introduction and problem classification (free)",
    "https://ocw.mit.edu/courses/15-093j-optimization-methods-fall-2009/",
    "The &sect;2 hierarchy with more emphasis on the linear and integer "
    "end."),
   ("Bixby &mdash; Solving Real-World Linear Programs: A Decade and More "
    "of Progress (free)",
    "https://pubsonline.informs.org/doi/10.1287/opre.50.1.3.17780",
    "<b>Evidence for the &sect;2 callout</b> — what solvers actually "
    "achieve on real instances, and how far that is from the worst case."),
 ],
 "exercises": [
   "Write three problems you care about in the &sect;1 standard form.",
   "<b>For each, classify it</b> into one of &sect;2's seven families.",
   "Solve a least squares problem, a linear program, and a small integer "
   "program with a solver, and compare the solve times.",
   "<b>Construct a small integer program the solver struggles with</b>, "
   "and a large one it solves instantly. Explain the difference.",
   "<b>Plot a non-convex function in one dimension</b> and run gradient "
   "descent from many starting points. Record the distinct minima found.",
   "Do the same for a convex function and confirm every start converges to "
   "the same point.",
   "<b>Find a stationary point that is a saddle</b> and verify with the "
   "Hessian.",
   "Formulate shortest path as a linear program and verify the solution is "
   "integral.",
   "<b>Express a problem from CSCE 633 in this course's notation</b> and "
   "say whether it is convex.",
   "Install CVXPY and a solver, and reproduce one textbook example.",
 ],
 "selfcheck": [
   "State the general optimisation problem and say what determines its "
   "difficulty.",
   "Why is convexity the dividing line, and why not linearity?",
   "Name seven problem classes and their difficulty.",
   "Why does NP-hardness not mean unsolvable in practice?",
   "What does a gradient establish, and what does a Hessian add?",
   "What does convexity let you conclude that you otherwise could not?",
   "Name six problems that are optimisation problems in disguise.",
 ],
},

]

for _b in ("c669_b2", "c669_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
