# -*- coding: utf-8 -*-
"""CSCE 637 Complexity Theory — original course content."""

COURSE = {
    "code": "CSCE 637",
    "title": "Complexity Theory",
    "tagline": "Not whether it can be done, but what it costs — and "
               "why the central question has been open for fifty years",
    "term": "Semester 8 (with CSCE 627 and CSCE 658)",
    "prereqs": "CSCE 629 Analysis of Algorithms; CSCE 627 Modules "
               "01–06 for the machine model and reductions; "
               "probability for Module 08",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A written portfolio containing one NP-completeness "
                   "proof you constructed, one honest account of how a "
                   "hard problem is handled in practice, and a correct "
                   "statement of what each result does and does not "
                   "establish",
    "description": [
        "<b>CSCE 627 asked whether a problem can be solved at all. "
        "This course asks what it costs</b> — and the difference is "
        "that <b>computability is settled and complexity is mostly "
        "not</b>. <b>The central question of the field has been open "
        "since 1971</b>, and a semester spent on a subject whose main "
        "question is unresolved teaches something about what evidence "
        "looks like when proof is unavailable.",
        "<b>The organising idea is that verification may be easier than "
        "search.</b> <b>Module 03 makes that precise as NP</b>, and "
        "<b>P versus NP is exactly the question of whether it "
        "is</b> — which is a far more natural question than the "
        "formal statement suggests, and is why it matters outside the "
        "field.",
        "<b>The second theme is that the field is honest about its own "
        "obstacles.</b> <b>Module 07 covers relativisation and "
        "Module 09 covers natural proofs</b> — two results showing "
        "that whole classes of proof technique cannot settle P versus NP. "
        "<b>Knowing why a question is hard is a genuine form of "
        "progress</b>, and few fields can point to theorems about the "
        "inadequacy of their own methods.",
        "<b>The third is that the practical consequences are not what "
        "the headline suggests.</b> <b>NP-hardness does not mean "
        "intractable</b> — CSCE 669 Module 09's solvers dispatch "
        "NP-hard problems with millions of variables daily. "
        "<b>Modules 11 and 12 are about what the theory actually "
        "predicts</b>: which approximation ratios are achievable, which "
        "parameters make a problem easy, and why some polynomial "
        "algorithms are too slow and some exponential ones are fine.",
        "<b>And the closing position is that the classification is a "
        "starting point rather than a verdict.</b> <b>'NP-complete' is "
        "the beginning of the engineering, not the end of it</b>, and "
        "Module 13 says what the label does and does not license you to "
        "conclude.",
    ],
    "outcomes": [
        "Explain why polynomial time is the robust notion of "
        "tractability.",
        "Define NP by verification and by non-determinism, and relate "
        "them.",
        "Prove a problem NP-complete by reduction.",
        "Place problems in co-NP, PSPACE, and the polynomial "
        "hierarchy.",
        "Explain space complexity and Savitch's theorem.",
        "Prove a hierarchy theorem and explain the relativisation "
        "barrier.",
        "Define BPP and explain the derandomisation question.",
        "Explain circuit complexity and the natural proofs barrier.",
        "Explain the PCP theorem and its approximation "
        "consequences.",
        "Apply parameterised and fine-grained complexity to a real "
        "problem.",
        "State what a hardness result does and does not establish.",
    ],
    "materials": [
        ("Arora & Barak — Computational Complexity: A Modern "
         "Approach (free draft)",
         "https://theory.cs.princeton.edu/complexity/",
         "<b>The primary source, and the full draft is free from the "
         "authors.</b> Chapters 1–11 and 17–20 are this "
         "course, and the barrier results of Modules 07 and 09 are "
         "treated better here than anywhere else."),
        ("Sipser — Introduction to the Theory of Computation, "
         "chapters 7–10",
         "https://math.mit.edu/~sipser/book.html",
         "<b>The gentler path through Modules 01–07</b>, and the "
         "same book as CSCE 627 — so the two courses share a "
         "text, which makes the computability/complexity boundary easy "
         "to follow."),
        ("MIT 18.404J — the complexity half (free lectures and "
         "problem sets)",
         "https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/",
         "<b>Free video lectures covering Modules 01–07</b>, by "
         "Sipser, with graded problem sets and solutions."),
        ("Garey & Johnson — Computers and Intractability",
         "https://www.worldcat.org/title/1097888",
         "<b>The catalogue of NP-complete problems</b>, and still the "
         "reference for Module 04's reductions. Its appendix of 300 "
         "problems is what you reduce from in practice. Library "
         "copy."),
        ("Cygan et al. — Parameterized Algorithms (free PDF)",
         "https://www.mimuw.edu.pl/~malcin/book/",
         "<b>Module 12's reference, free in full</b> — the most "
         "practically useful material in the course, and the least "
         "commonly taught."),
        ("Aaronson — P =? NP (free survey)",
         "https://www.scottaaronson.com/papers/pnp.pdf",
         "<b>The honest survey of the central question</b>, including "
         "the barriers of Modules 07 and 09 and an assessment of what "
         "the evidence is actually worth. Read it twice."),
    ],
    "tooling": [
        "<b>Paper, as in CSCE 627.</b> <b>The deliverable is "
        "proofs</b>, and a reduction you cannot write out is a reduction "
        "you have not got.",
        "<b>A SAT solver and a MIP solver</b> (CSCE 625 Module 08, "
        "CSCE 669 Module 13). <b>Module 04's theory is far more "
        "convincing once you have watched a solver dispatch a "
        "million-variable NP-complete instance.</b>",
        "<b>An instance generator</b>, so you can produce hard and easy "
        "instances of the same problem deliberately — which is "
        "Module 12's central observation made experimental.",
        "<b>A profiler and a plotting setup</b>, for Module 12's "
        "fine-grained work: <b>the difference between n² and "
        "n²·⁵ is visible on a log-log plot and invisible "
        "in a table.</b>",
        "<b>Garey and Johnson's appendix, or a modern equivalent.</b> "
        "<b>Reductions are built from a library</b> "
        "(CSCE 627 Module 06 §3), and the library is the "
        "tool.",
        "<b>And no GPU, no cluster, no data.</b> <b>The second course in "
        "the program with no computational requirement</b>, which is "
        "worth noticing twice.",
    ],
    "projects": [
        {"title": "A hardness proof, constructed", "after": 7,
         "brief": "Prove something NP-complete yourself, and place "
                  "several problems correctly in the classes.",
         "reqs": [
             "<b>One NP-completeness proof you constructed</b>, not "
             "reproduced — both directions, with the polynomial "
             "bound on the reduction verified.",
             "<b>The membership half done properly</b>, which is the "
             "half people skip: exhibit the certificate and the "
             "verifier.",
             "<b>Three problems placed</b> in P, NP-complete, or "
             "beyond, with justification.",
             "<b>One problem placed in co-NP</b> and the asymmetry "
             "explained.",
             "<b>One problem placed in PSPACE</b> with an argument for "
             "why it is probably not in NP.",
             "<b>A hierarchy theorem proved</b>, in your own words.",
         ],
         "done": [
             "<b>Both halves of the NP-completeness proof present</b> "
             "— membership and hardness. A hardness proof alone "
             "proves NP-hardness, not completeness, and the distinction "
             "is graded.",
             "<b>The reduction's polynomial bound actually argued</b>, "
             "not assumed.",
             "<b>The reduction in the correct direction</b>, stated "
             "explicitly.",
             "<b>And one problem you initially placed wrongly</b>, with "
             "the error and the correction written down.",
         ]},
        {"title": "A hard problem, handled", "after": 12,
         "brief": "Take an NP-hard problem you care about and establish "
                  "what the theory actually predicts about solving it.",
         "reqs": [
             "<b>An NP-hard problem from your own work or interest</b>, "
             "with its hardness established or cited.",
             "<b>A solver run on real instances</b>, with sizes and "
             "times reported.",
             "<b>An instance family where it fails</b>, and one where "
             "it succeeds easily, with the difference characterised.",
             "<b>A parameter identified</b> and the problem's "
             "fixed-parameter tractability assessed "
             "(Module 12).",
             "<b>The best approximation ratio known</b>, and the "
             "hardness-of-approximation result if one exists "
             "(Module 11).",
             "<b>A fine-grained lower bound</b> if one applies — "
             "SETH, 3SUM, or APSP-based.",
         ],
         "done": [
             "<b>The easy and hard instance families genuinely "
             "distinguished</b>, with a stated hypothesis about why.",
             "<b>The parameter assessed correctly</b> — including "
             "if the answer is that no useful parameter is small.",
             "<b>The approximation picture stated with both sides</b>: "
             "achievable ratio and hardness bound.",
             "<b>And a written answer to 'what does NP-hardness actually "
             "predict here?'</b> — which is the graded part, and "
             "'less than I expected' is a common correct answer.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Measuring Cost",
 "subtitle": "What a complexity class is, and what makes one robust.",
 "question": "How do you measure the cost of a computation so the answer "
             "means something?",
 "outcomes": [
     "Explain why the machine model matters here and not in "
     "CSCE 627.",
     "Define a complexity class and state what makes one natural.",
     "Explain why input length is measured in bits.",
     "Explain worst case, average case, and why worst case "
     "dominates.",
     "State what asymptotic analysis hides.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The model matters now",
   "blurb": "Which is the difference from CSCE 627."},

  {"t": "callout", "title": "Computability is model-free; complexity is not",
   "kind": "The division between the two courses",
   "body": ["<b>CSCE 627 Module 04 §1 showed every "
            "reasonable machine model computes the same functions</b> "
            "— so computability could be settled without choosing a "
            "model.",
            "<b>But the models differ in <i>time</i>.</b> A multi-tape "
            "machine simulated on one tape costs a quadratic slowdown; "
            "random access costs a polynomial one; non-determinism costs "
            "exponential.",
            "<b>So a complexity class is only meaningful if it is "
            "robust to those differences</b> — and <b>polynomial time "
            "is</b>, because polynomials compose.",
            "<b>Which is the entire reason P is the class of "
            "interest</b> (Module 02). <b>'Linear time' is not "
            "model-independent and 'polynomial time' is</b>, and that "
            "single fact shapes the field."]},

  {"t": "table", "kicker": "Robustness", "title": "What survives a change of model",
   "header": ["Notion", "Robust?", "Why it matters"],
   "widths": [2.8, 2.6, 5.6],
   "rows": [
     ["<b>Computable</b>", "<b>Yes, entirely</b>", "<b>CSCE 627's whole subject</b>"],
     ["<b>Polynomial time</b>", "<b>Yes</b>", "<b>Polynomials compose, so P is well defined</b>"],
     ["<b>Linear time</b>", "<b>No</b>", "<b>Model-dependent; not a useful class</b>"],
     ["<b>Logarithmic space</b>", "<b>Yes</b>", "<b>With care about the input tape (M06)</b>"],
     ["<b>Exact constants</b>", "<b>No</b>", "<b>Which is why theory ignores them, and you cannot</b>"],
   ],
   "footnote": "<b>Theory studies what is model-independent and "
               "engineering lives in what is not</b> — which is why "
               "a complexity result and a benchmark answer different "
               "questions and both are needed.",
   "note": "The robustness criterion is what students most often miss."},

  {"t": "section", "label": "Part 2", "title": "Measuring the input",
   "blurb": "In bits, and why that is not pedantry."},

  {"t": "callout", "title": "Input length is bits, which makes some 'polynomial' algorithms exponential",
   "kind": "The distinction that catches people",
   "body": ["<b>Complexity is measured against the input's length in "
            "bits</b>, because that is what is model-independent "
            "(CSCE 627 §01).",
            "<b>So an algorithm polynomial in the <i>value</i> of a "
            "number is exponential in its <i>length</i></b> — a "
            "number n takes log n bits, so O(n) in the value is "
            "O(2^bits).",
            "<b>That is what pseudo-polynomial means.</b> <b>Knapsack's "
            "dynamic program is O(nW), which is polynomial in W and "
            "exponential in W's bit length</b> — and knapsack is "
            "NP-complete.",
            "<b>And the same issue is why primality looked hard for so "
            "long:</b> trial division is O(√n), which is "
            "exponential in the bit length. <b>AKS in 2002 gave a "
            "genuinely polynomial algorithm.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Which case",
   "blurb": "Worst, average, and why the theory chose worst."},

  {"t": "table", "kicker": "Cases", "title": "Three ways to measure",
   "header": ["Measure", "Means", "Problem with it"],
   "widths": [2.6, 4.0, 5.4],
   "rows": [
     ["<b>Worst case</b>", "<b>The slowest input of each size</b>", "<b>May never occur. Still the default</b>"],
     ["<b>Average case</b>", "<b>Expectation over an input distribution</b>", "<b>Which distribution? Rarely justifiable</b>"],
     ["<b>Smoothed</b>", "<b>Worst case, perturbed slightly</b>", "<b>Explains simplex; harder to analyse</b>"],
     ["<b>Amortised</b>", "<b>Average over a sequence of operations</b>", "<b>Worst case per sequence, not per input</b>"],
   ],
   "footnote": "<b>Worst case dominates because it needs no "
               "assumptions</b> — an average-case result is only as "
               "good as its distribution, and nobody can justify a "
               "distribution over real inputs.",
   "note": "The 'which distribution' objection is the real reason worst "
           "case won."},

  {"t": "callout", "title": "And the worst case is sometimes the wrong question",
   "kind": "Stated now, developed in Module 12",
   "body": ["<b>Simplex has exponential worst case and is excellent in "
            "practice</b> (CSCE 669 §03) — <b>smoothed analysis "
            "explains it, and the worst case does not.</b>",
            "<b>SAT solvers dispatch million-variable instances</b> "
            "(CSCE 625 §08) <b>on a problem that is "
            "NP-complete.</b>",
            "<b>And quicksort's worst case is quadratic</b>, which no "
            "practitioner thinks about.",
            "<b>So worst-case complexity is a correct answer to a "
            "question that is sometimes not the one you have</b> "
            "— <b>which is Module 12's subject and the honest "
            "qualification to attach to everything in Modules "
            "02–11.</b>"]},

  {"t": "section", "label": "Part 4", "title": "What asymptotics hide",
   "blurb": "And why it matters in both directions."},

  {"t": "bullets", "kicker": "Hidden", "title": "What O-notation suppresses",
   "items": [
     "<b>Constants.</b> <b>An O(n) algorithm with a constant of "
     "10⁶ loses to an O(n log n) one at every realistic size</b>, "
     "and theory cannot see it.",
     "",
     "<b>The crossover point.</b> <b>Asymptotically better means "
     "better eventually</b>, and 'eventually' is sometimes past any "
     "input you will meet.",
     "",
     "<b>Galactic algorithms.</b> <b>Matrix multiplication at "
     "O(n^2.37) has constants making it slower than O(n³) for any "
     "n that fits in the universe.</b>",
     "",
     "<b>Memory behaviour.</b> <b>Cache locality can dominate "
     "asymptotics by an order of magnitude</b> (CSCE 735 §02), "
     "and the model does not represent it.",
     "",
     "<b>And parallelism</b>, which the sequential model does not "
     "express at all.",
   ],
   "footnote": "<b>So asymptotic analysis is necessary and not "
               "sufficient</b> — it tells you which algorithms are "
               "worth benchmarking and never which is faster."},

  {"t": "callout", "title": "Where this course goes",
   "kind": "The shape of the semester",
   "body": ["<b>Modules 02–05: the classes.</b> P, NP, "
            "NP-completeness, and what lies beyond — <b>the material "
            "everyone has heard of, done properly.</b>",
            "<b>Modules 06–09: space, hierarchies, "
            "randomness, and circuits</b> — <b>including two "
            "theorems about why the central question resists "
            "proof.</b>",
            "<b>Modules 10–12: interactive proofs, "
            "hardness of approximation, and the fine-grained and "
            "parameterised views</b> — <b>which is where the "
            "practically useful material is.</b>",
            "<b>Module 13: what the classification licenses you to "
            "conclude</b> — which is less than the labels "
            "suggest."]},
 ],
 "takeaways": [
   "Computability is model-free and complexity is not, which is why "
   "polynomial time rather than linear time is the class of interest "
   "— polynomials compose.",
   "Theory studies what is model-independent and engineering lives in what "
   "is not, so a complexity result and a benchmark answer different "
   "questions.",
   "Input length is measured in bits, which is what makes knapsack's "
   "O(nW) algorithm pseudo-polynomial rather than polynomial.",
   "Worst case dominates because it needs no assumptions — an "
   "average-case result is only as good as its unjustifiable "
   "distribution.",
   "And the worst case is sometimes the wrong question, which simplex and "
   "SAT solvers both demonstrate.",
   "Asymptotic analysis is necessary and not sufficient: it says which "
   "algorithms are worth benchmarking and never which is faster.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The model matters now"),
  ("callout", "Computability is model-free; complexity is not",
   ["<b>CSCE 627 Module 04 &sect;1 showed that every reasonable "
    "machine model computes exactly the same class of functions</b> "
    "— so computability could be settled once, without having to "
    "choose a model, which is why that course's results are "
    "unconditional.",
    "<b>But the models differ substantially in <i>time</i>.</b> A "
    "multi-tape machine simulated on a single tape costs a quadratic "
    "slowdown; a random-access machine simulated on a tape costs a "
    "polynomial one; a non-deterministic machine simulated "
    "deterministically costs exponential.",
    "<b>So a complexity class is only meaningful if it is robust to "
    "those differences</b> — otherwise the class is a fact about "
    "the formalism rather than about the problem. <b>And polynomial time "
    "is robust, because a polynomial of a polynomial is a "
    "polynomial</b>: a polynomial-time algorithm on one model is "
    "polynomial on any other.",
    "<b>Which is the entire reason P is the class of interest</b> "
    "(Module 02). <b>'Linear time' is not model-independent and "
    "'polynomial time' is</b>, and <b>that single fact shapes the whole "
    "field</b> — including the otherwise strange decision to treat "
    "n<super>100</super> as tractable and 1.0001<super>n</super> as "
    "not."]),
  ("table", ["Notion", "Robust across models?", "Why it matters"],
   [["<b>Computable</b>", "<b>Yes, entirely.</b>",
     "<b>CSCE 627's whole subject, and why it could be settled.</b>"],
    ["<b>Polynomial time</b>", "<b>Yes.</b>",
     "<b>Polynomials compose, so P is well defined independently of the "
     "model.</b>"],
    ["<b>Linear time</b>", "<b>No.</b>",
     "<b>Model-dependent, and therefore not a useful complexity "
     "class</b> — although it is a perfectly useful engineering "
     "target."],
    ["<b>Logarithmic space</b>", "<b>Yes.</b>",
     "<b>With care about not charging for the read-only input tape</b> "
     "(Module 06 &sect;1)."],
    ["<b>Exact constants</b>", "<b>No.</b>",
     "<b>Which is why theory ignores them, and why you cannot</b> "
     "(&sect;4)."]],
   [0.22, 0.22, 0.56]),
  ("p", "<b>Theory studies what is model-independent, and engineering "
        "lives in what is not.</b> <b>Which is why a complexity result "
        "and a benchmark answer different questions and both are "
        "needed</b> — and why a practitioner's dismissal of "
        "complexity theory and a theorist's dismissal of benchmarking are "
        "both mistakes about what the other is for."),

  ("h1", "2 &nbsp; Measuring the input"),
  ("callout", "Input length is bits, which makes some 'polynomial' "
              "algorithms exponential",
   ["<b>Complexity is measured against the input's length in bits</b>, "
    "because that is the quantity that is model-independent "
    "(CSCE 627 Module 01 &sect;1's encoding discussion).",
    "<b>So an algorithm polynomial in the <i>value</i> of a number is "
    "exponential in its <i>length</i></b> — a number n occupies "
    "about log n bits, so an O(n) algorithm is O(2<super>b</super>) where "
    "b is the bit length. <b>The algorithm has not changed; the "
    "accounting has.</b>",
    "<b>That is exactly what 'pseudo-polynomial' means.</b> "
    "<b>Knapsack's dynamic programming algorithm runs in O(nW) where W "
    "is the capacity</b> — polynomial in W, exponential in W's bit "
    "length — <b>and knapsack is NP-complete</b>, which is "
    "consistent precisely because of this distinction (CSCE 629's "
    "treatment, now with a reason).",
    "<b>And the same issue is why primality testing looked hard for so "
    "long:</b> trial division up to the square root is O(&radic;n), which "
    "is exponential in the bit length, so it is not a polynomial "
    "algorithm at all. <b>AKS gave a genuinely polynomial algorithm in "
    "2002</b>, resolving a question that had been open since the "
    "classification of problems began — <b>and the practical "
    "primality tests everybody uses are randomised</b> (Module 08)."]),

  ("h1", "3 &nbsp; Which case to measure"),
  ("table", ["Measure", "What it means", "The problem with it"],
   [["<b>Worst case</b>",
     "<b>The slowest input of each length.</b>",
     "<b>It may never occur in practice. Still the default</b> — see "
     "the note below."],
    ["<b>Average case</b>",
     "<b>Expected cost over a distribution of inputs.</b>",
     "<b>Which distribution?</b> <b>Rarely justifiable</b> — and a "
     "result over the uniform distribution says very little about real "
     "inputs, which are never uniform."],
    ["<b>Smoothed</b>",
     "<b>Worst case over inputs that have been randomly perturbed "
     "slightly.</b>",
     "<b>Explains simplex's practical success</b> (Spielman and Teng), "
     "and is substantially harder to analyse than either of the above."],
    ["<b>Amortised</b>",
     "<b>Average cost over a sequence of operations.</b>",
     "<b>Worst case per <i>sequence</i>, not per input</b> — so it "
     "is a worst-case guarantee and is frequently mistaken for an "
     "average-case one (CSCE 629's dynamic arrays)."]],
   [0.22, 0.34, 0.44]),
  ("p", "<b>Worst case dominates because it requires no "
        "assumptions.</b> <b>An average-case result is only as good as "
        "its distribution</b>, and <b>nobody can justify a distribution "
        "over the inputs a real system will see</b> — which is the "
        "actual reason worst case won, rather than any claim that the "
        "worst case is typical."),
  ("callout", "And the worst case is sometimes the wrong question",
   ["<b>The simplex method has exponential worst-case behaviour and is "
    "excellent in practice</b> (CSCE 669 Module 03 &sect;2) — "
    "<b>smoothed analysis explains this and worst-case analysis does "
    "not</b>, which is a case of the theory having needed a new notion "
    "rather than the practice having been lucky.",
    "<b>SAT solvers routinely dispatch instances with millions of "
    "variables</b> (CSCE 625 Module 08 &sect;2) <b>on a problem that "
    "is NP-complete</b> — and the instances that arise from "
    "verification and scheduling are simply not the hard ones.",
    "<b>And quicksort's worst case is quadratic</b>, which no "
    "practitioner thinks about for a moment, because the input orderings "
    "that trigger it do not arise (and randomisation removes them "
    "anyway — Module 08).",
    "<b>So worst-case complexity is a correct answer to a question that "
    "is sometimes not the one you have</b> — <b>which is "
    "Module 12's subject and is the honest qualification to attach to "
    "everything in Modules 02 through 11.</b> <b>Stating it now rather "
    "than at the end is deliberate</b>, because the alternative is twelve "
    "modules of results a practitioner will reasonably distrust."]),

  ("break",),
  ("h1", "4 &nbsp; What asymptotics hide"),
  ("ul", ["<b>Constants.</b> <b>An O(n) algorithm with a constant factor "
          "of 10<super>6</super> loses to an O(n log n) one at every "
          "realistic input size</b>, and asymptotic analysis cannot see "
          "the difference. <b>This is not a minor caveat; it is why some "
          "asymptotically optimal algorithms are never implemented.</b>",
          "<b>The crossover point.</b> <b>Asymptotically better means "
          "better <i>eventually</i></b>, and 'eventually' is sometimes "
          "past any input that will ever be presented — which makes "
          "the comparison true and useless.",
          "<b>Galactic algorithms.</b> <b>Matrix multiplication in "
          "O(n<super>2.37</super>) exists, and its constant factors make "
          "it slower than the O(n&#179;) algorithm for any n that would "
          "fit in the observable universe.</b> <b>So the exponent "
          "improvements after Strassen are mathematically real and "
          "practically irrelevant</b>, and saying so is more useful than "
          "citing the current record.",
          "<b>Memory behaviour.</b> <b>Cache locality routinely "
          "dominates asymptotic differences by an order of magnitude</b> "
          "(CSCE 735 Module 02, CSCE 753 Module 06 &sect;1's "
          "rectification), <b>and the standard model does not represent "
          "memory hierarchy at all.</b>",
          "<b>And parallelism</b>, which the sequential model does not "
          "express — so an algorithm with worse sequential "
          "complexity and better parallel structure can win decisively "
          "(CSCE 735's whole subject). <b>So asymptotic analysis is "
          "necessary and not sufficient</b>: <b>it tells you which "
          "algorithms are worth benchmarking, and never which one is "
          "faster.</b>"]),
  ("callout", "Where this course goes",
   ["<b>Modules 02 through 05: the classes.</b> P, NP, "
    "NP-completeness, and what lies beyond — <b>the material "
    "everyone has heard of, done properly</b>, including the parts the "
    "popular accounts get wrong.",
    "<b>Modules 06 through 09: space complexity, the hierarchy "
    "theorems, randomised classes, and circuits</b> — <b>including "
    "two theorems explaining why the central question resists proof</b>, "
    "which is the most intellectually interesting material in the "
    "course.",
    "<b>Modules 10 through 12: interactive proofs, hardness of "
    "approximation, and the fine-grained and parameterised views</b> "
    "— <b>which is where the practically useful material is</b>, "
    "and it is the part most complexity courses omit.",
    "<b>Module 13: what the classification actually licenses you to "
    "conclude</b> — which is <b>considerably less than the labels "
    "suggest</b>, and is the honest close to a course whose central "
    "question is open."]),
 ],
 "resources": [
   ("Arora & Barak &mdash; chapter 1 (free draft)",
    "https://theory.cs.princeton.edu/complexity/",
    "<b>The machine model, the robustness argument of &sect;1, and the "
    "definition of a complexity class.</b>"),
   ("Sipser &mdash; chapter 7, sections 7.1–7.2",
    "https://math.mit.edu/~sipser/book.html",
    "<b>The same material more gently</b>, with the encoding and "
    "measurement issues of &sect;2 stated carefully."),
   ("Spielman & Teng &mdash; Smoothed Analysis of Algorithms (free)",
    "https://arxiv.org/abs/math/0212413",
    "<b>&sect;3's third row</b>, and the resolution of the simplex "
    "puzzle — a good example of theory catching up with "
    "practice."),
   ("Lipton & Regan &mdash; Galactic algorithms (free blog series)",
    "https://rjlipton.wordpress.com/2010/10/23/galactic-algorithms/",
    "<b>&sect;4's third bullet</b>, where the term comes from, with "
    "examples."),
 ],
 "exercises": [
   "<b>Show that a polynomial-time algorithm on a two-tape machine is "
   "polynomial on one tape</b>, and give the exponent.",
   "<b>Show that linear time is not model-independent</b> by exhibiting "
   "a problem whose linear-time solvability depends on the model.",
   "<b>Implement knapsack's O(nW) algorithm</b> and plot its time against "
   "the bit length of W.",
   "<b>Confirm it is exponential in the bit length</b> and state why that "
   "is consistent with NP-completeness.",
   "<b>Implement trial division and a Miller–Rabin test</b> and "
   "compare their scaling in bit length.",
   "<b>Construct quicksort's worst-case input</b> and measure it, then "
   "randomise the pivot and measure again.",
   "<b>Find two algorithms for one problem with different asymptotics</b> "
   "and locate the crossover point empirically.",
   "<b>Implement naive and Strassen matrix multiplication</b> and find "
   "the crossover.",
   "<b>Measure the cache effect</b> by multiplying matrices in two loop "
   "orders, and report the ratio.",
   "<b>Write down which of the five hidden factors</b> in &sect;4 has "
   "most affected your own work.",
 ],
 "selfcheck": [
   "Why is computability model-free and complexity not?",
   "Why is polynomial time the robust notion and linear time not?",
   "Name five notions and whether each is robust.",
   "Why is input length measured in bits, and what is "
   "pseudo-polynomial?",
   "Why is knapsack's dynamic program consistent with its "
   "NP-completeness?",
   "Compare four ways of measuring cost.",
   "Why does worst case dominate, and what is the real reason?",
   "Give three cases where the worst case is the wrong question.",
   "Name five things asymptotics hide.",
 ],
},

]

for _b in ("c637_b2", "c637_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
