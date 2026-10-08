# -*- coding: utf-8 -*-
"""CSCE 637 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "P, and What Tractable Means",
 "subtitle": "The class, and the thesis behind it.",
 "question": "Why is polynomial time the dividing line?",
 "outcomes": [
     "Define P and state the Cobham–Edmonds thesis.",
     "Explain the arguments for and against the thesis.",
     "Give examples of problems whose membership in P was hard "
     "won.",
     "Explain closure properties of P and why they matter.",
     "State honestly what P does and does not capture.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The class",
   "blurb": "And the thesis that makes it interesting."},

  {"t": "callout", "title": "P is the problems decidable in polynomial time, and the choice is defended, not obvious",
   "kind": "The Cobham–Edmonds thesis",
   "body": ["<b>P is the class of decision problems solvable by a "
            "deterministic Turing machine in time O(n^k) for some "
            "fixed k.</b>",
            "<b>The Cobham–Edmonds thesis claims P captures "
            "'tractable'</b> — and like the Church–Turing "
            "thesis it is a claim about a definition's adequacy "
            "(CSCE 627 §01), not a theorem.",
            "<b>The case for it:</b> <b>polynomials compose and are "
            "closed under addition and multiplication</b>, so P is "
            "robust to the model and to composition of algorithms — "
            "which no other natural class is.",
            "<b>And the case against it is obvious:</b> "
            "<b>n¹⁰⁰ is not tractable and "
            "1.0001ⁿ is fine for n up to a million.</b> <b>Both "
            "objections are correct and neither has produced a better "
            "definition.</b>"]},

  {"t": "table", "kicker": "The defence", "title": "Why P survives its obvious objections",
   "header": ["Objection", "Response"],
   "widths": [4.6, 6.4],
   "rows": [
     ["<b>n¹⁰⁰ is not tractable</b>", "<b>True — and in practice natural problems in P have small exponents. The high-degree cases are artificial</b>"],
     ["<b>1.0001ⁿ is fine for real n</b>", "<b>True — and such algorithms are rare; real exponential algorithms have base 2 or more</b>"],
     ["<b>Constants are ignored</b>", "<b>True — and they are model-dependent, so including them would destroy robustness (M01 §1)</b>"],
     ["<b>It is a worst-case notion</b>", "<b>True — and Module 12 addresses it; the alternatives need unjustifiable assumptions</b>"],
     ["<b>It says nothing about parallelism or memory</b>", "<b>True — which is why NC and L exist (M06)</b>"],
   ],
   "footnote": "<b>Every objection is correct, and the class survives "
               "because no proposed replacement is both robust and "
               "closer to practice</b> — which is a weaker defence "
               "than people assume and is the honest one.",
   "note": "Being candid that the defence is weak is more useful than "
           "overselling it."},

  {"t": "section", "label": "Part 2", "title": "Hard-won membership",
   "blurb": "Problems whose place in P took decades."},

  {"t": "bullets", "kicker": "In P", "title": "Membership results that were not easy",
   "items": [
     "<b>Linear programming.</b> <b>Khachiyan's ellipsoid method, "
     "1979</b> — the first polynomial algorithm, and it is "
     "unusable in practice (CSCE 669 §07).",
     "",
     "<b>Primality.</b> <b>AKS, 2002</b> — and the practical "
     "tests are still randomised (M08), so the polynomial algorithm "
     "settled the theory and changed nothing operationally.",
     "",
     "<b>Maximum matching.</b> <b>Edmonds, 1965</b> — and the "
     "paper is where the polynomial-time thesis was first argued "
     "explicitly.",
     "",
     "<b>Graph isomorphism.</b> <b>Not known to be in P</b>, not "
     "known NP-complete, and Babai's 2015 quasi-polynomial algorithm "
     "is the state of the art. <b>Probably neither.</b>",
     "",
     "<b>And integer factoring</b>, which is in neither P nor "
     "known NP-complete, and on which most of cryptography rests.",
   ],
   "footnote": "<b>The last two matter:</b> <b>NP-intermediate "
               "problems are believed to exist</b>, and factoring and "
               "graph isomorphism are the candidates — so NP is not "
               "a two-tier structure."},

  {"t": "callout", "title": "Edmonds' 1965 argument is the original statement",
   "kind": "Where the thesis comes from",
   "body": ["<b>Edmonds, presenting a matching algorithm, distinguished "
            "'good' algorithms from exponential search</b> and argued "
            "the distinction was the right one.",
            "<b>His argument was that an exponential algorithm "
            "expresses no insight</b> — it is organised enumeration, "
            "and finding a polynomial one requires understanding the "
            "problem's structure.",
            "<b>Which is a better defence of the thesis than the "
            "robustness argument</b>, because it says what a polynomial "
            "algorithm <i>means</i> rather than only that the class is "
            "well behaved.",
            "<b>And it predicts the empirical pattern:</b> <b>natural "
            "problems in P have small exponents because the insight that "
            "puts them there is usually a strong one</b> — which is "
            "Part 1's first response, with a reason."]},

  {"t": "section", "label": "Part 3", "title": "Closure",
   "blurb": "Why P is a usable class."},

  {"t": "callout", "title": "P is closed under the operations you actually use",
   "kind": "And that is what makes it workable",
   "body": ["<b>Closed under complement</b> — swap the answer. "
            "<b>Which NP is not known to be</b> (Module 05 "
            "§1), and that asymmetry is the whole of co-NP.",
            "<b>Closed under union, intersection, and "
            "concatenation</b>, and under polynomial-time composition: "
            "<b>a polynomial algorithm calling a polynomial subroutine "
            "polynomially many times is polynomial.</b>",
            "<b>Which is what makes modular programming compatible with "
            "complexity analysis</b> — you can reason about a "
            "subroutine's complexity independently.",
            "<b>And it means polynomial-time reductions compose</b> "
            "(Module 04 §1) — <b>without which NP-completeness "
            "would not be a transitive notion and the catalogue would not "
            "work.</b>"]},

  {"t": "section", "label": "Part 4", "title": "What P misses",
   "blurb": "The honest limits."},

  {"t": "bullets", "kicker": "Limits", "title": "What membership in P does not tell you",
   "items": [
     "<b>Whether it is fast.</b> <b>O(n⁵) with a large constant "
     "is in P and unusable</b> on a million-element input.",
     "",
     "<b>Whether it parallelises.</b> <b>NC is the parallel-tractable "
     "class, and whether NC = P is open</b> (Module 06 §4).",
     "",
     "<b>Whether it fits in memory</b> — a polynomial-time "
     "algorithm may use polynomial space, which is an entirely "
     "different constraint (Module 06).",
     "",
     "<b>Whether it streams</b>, or works online, or tolerates "
     "approximation — all of which are real requirements the class "
     "does not express.",
     "",
     "<b>And whether the problem you have is the worst case</b> "
     "— which is Module 12, and is frequently the only question "
     "that matters.",
   ],
   "footnote": "<b>So 'it is in P' is good news and not an engineering "
               "answer</b> — it tells you to look for an efficient "
               "algorithm rather than a proof that none exists."},

  {"t": "callout", "title": "The practical reading of P",
   "kind": "What to do with the classification",
   "body": ["<b>'In P' means: a polynomial algorithm exists, so keep "
            "looking for a good one.</b> <b>The search is not futile, "
            "which is the useful information.</b>",
            "<b>'NP-hard' means: stop looking for an exact "
            "polynomial algorithm and start on Module 11's "
            "approximations or Module 12's parameters.</b>",
            "<b>'Neither known' means: both searches are live</b>, and "
            "graph isomorphism is the standing example of a problem that "
            "stayed there for fifty years.",
            "<b>Which is the whole operational content of the "
            "classification</b> — <b>it redirects effort, and that is "
            "worth a great deal more than it sounds.</b>"]},
 ],
 "takeaways": [
   "P is polynomial-time decidable problems, and the Cobham–Edmonds "
   "thesis that this captures tractability is a claim about a definition "
   "rather than a theorem.",
   "Every objection to the thesis is correct, and it survives because no "
   "proposed replacement is both robust and closer to practice.",
   "Edmonds' original argument — that a polynomial algorithm "
   "expresses insight and an exponential one does not — is the better "
   "defence.",
   "Graph isomorphism and factoring are in neither P nor known "
   "NP-complete, so NP is not a two-tier structure.",
   "P is closed under complement and under polynomial composition, which "
   "is what makes reductions transitive and modular reasoning valid.",
   "'In P' means keep looking for a good algorithm; 'NP-hard' means start "
   "on approximations or parameters. That redirection is the "
   "classification's operational content.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The class, and the thesis"),
  ("callout", "P is the problems decidable in polynomial time, and the "
              "choice is defended rather than obvious",
   ["<b>P is the class of decision problems solvable by a deterministic "
    "Turing machine in time O(n<super>k</super>) for some fixed k</b>, "
    "where n is the input length in bits (Module 01 &sect;2).",
    "<b>The Cobham–Edmonds thesis claims that P captures the "
    "informal notion of 'tractable'</b> — and <b>like the "
    "Church–Turing thesis it is a claim about a definition's "
    "adequacy</b> (CSCE 627 Module 01 &sect;2) <b>rather than a "
    "theorem</b>, so it is argued for rather than proved.",
    "<b>The case for it:</b> <b>polynomials are closed under addition, "
    "multiplication, and composition</b>, so P is robust to the choice "
    "of machine model (Module 01 &sect;1) <i>and</i> to composing "
    "algorithms (&sect;3) — <b>and no other natural time bound has "
    "both properties.</b>",
    "<b>And the case against it is immediate and correct:</b> "
    "<b>n<super>100</super> is not tractable by any standard, and "
    "1.0001<super>n</super> is perfectly fine for n up to a "
    "million.</b> <b>Both objections hold, and neither has produced a "
    "better definition in fifty years</b> — which is the honest "
    "state of the matter rather than a defence."]),
  ("table", ["The objection", "The response"],
   [["<b>n<super>100</super> is not tractable, so P is too "
     "generous.</b>",
     "<b>True — and in practice the natural problems known to be in "
     "P have small exponents, mostly 1 to 4. The high-degree cases are "
     "artificial constructions</b> (and &sect;2's callout gives a reason "
     "why)."],
    ["<b>1.0001<super>n</super> is fine for realistic n, so P is too "
     "restrictive.</b>",
     "<b>True — and such algorithms are rare. Real exponential "
     "algorithms arising from search have base 2 or more</b>, where the "
     "asymptotic and practical pictures agree."],
    ["<b>Constants are ignored entirely.</b>",
     "<b>True — and they are model-dependent, so including them "
     "would destroy the robustness that makes the class meaningful</b> "
     "(Module 01 &sect;1). The omission is load-bearing."],
    ["<b>It is a worst-case notion.</b>",
     "<b>True — and Module 12 addresses it directly; the "
     "average-case alternatives require distributional assumptions nobody "
     "can justify</b> (Module 01 &sect;3)."],
    ["<b>It says nothing about parallelism or memory.</b>",
     "<b>True — which is why NC and L exist as separate classes</b> "
     "(Module 06), and why P is one measurement rather than the "
     "measurement."]],
   [0.40, 0.60]),
  ("p", "<b>Every objection is correct, and the class survives because no "
        "proposed replacement is both robust and closer to "
        "practice</b> — <b>which is a weaker defence than people "
        "generally assume, and it is the honest one.</b> <b>Being candid "
        "about this is more useful than overselling the thesis</b>, "
        "because it sets the right expectation for what a P-membership "
        "result tells you (&sect;4)."),

  ("h1", "2 &nbsp; Membership results that were hard won"),
  ("ul", ["<b>Linear programming.</b> <b>Khachiyan's ellipsoid method, "
          "1979, was the first polynomial-time algorithm</b> — and "
          "<b>it is unusable in practice</b>, while the practical "
          "interior-point methods came later and the practical simplex "
          "method is exponential in the worst case (CSCE 669 "
          "Modules 03 and 07). <b>A clean case of the theory and the "
          "practice settling the same question differently.</b>",
          "<b>Primality.</b> <b>AKS, 2002</b> — and <b>the "
          "practical tests remain randomised</b> (Module 08), so the "
          "polynomial algorithm settled a long-standing theoretical "
          "question and changed nothing operationally. <b>Which is worth "
          "knowing as an example of what a complexity result is and is "
          "not for.</b>",
          "<b>Maximum matching in general graphs.</b> <b>Edmonds, "
          "1965</b> — and that paper is where the polynomial-time "
          "thesis was first argued explicitly (see the callout).",
          "<b>Graph isomorphism.</b> <b>Not known to be in P, not known "
          "to be NP-complete</b>, and <b>Babai's 2015 quasi-polynomial "
          "algorithm is the state of the art</b> — faster than any "
          "known exponential bound and slower than any polynomial. "
          "<b>Probably in neither class.</b>",
          "<b>And integer factoring</b>, which is in neither P nor known "
          "to be NP-complete, <b>and on which most of deployed public-key "
          "cryptography rests</b> (CSCE 711's subject). <b>The last two "
          "matter structurally:</b> <b>NP-intermediate problems are "
          "believed to exist</b>, and these are the standing candidates "
          "— <b>so NP is not a two-tier structure of easy and "
          "complete, which Module 05 develops.</b>"]),
  ("callout", "Edmonds' 1965 argument is the original statement",
   ["<b>Edmonds, presenting his matching algorithm, distinguished "
    "'good' algorithms from exponential search</b> and argued explicitly "
    "that the distinction was the right one to draw — six years "
    "before Cook's theorem gave the field its central question.",
    "<b>His argument was that an exponential algorithm expresses no "
    "insight</b>: it is organised enumeration of possibilities, which is "
    "always available and tells you nothing. <b>Finding a polynomial "
    "algorithm requires understanding something about the problem's "
    "structure.</b>",
    "<b>Which is a better defence of the thesis than the robustness "
    "argument of &sect;1</b>, because <b>it says what a polynomial "
    "algorithm <i>means</i></b> rather than only that the class is "
    "mathematically well behaved.",
    "<b>And it predicts the empirical pattern:</b> <b>natural problems "
    "in P have small exponents because the insight that puts them there "
    "is usually a strong structural one</b> — a matroid "
    "(CSCE 669 Module 11 &sect;2), a flow formulation, a total "
    "unimodularity — <b>and strong structure gives fast algorithms, "
    "not merely polynomial ones.</b> <b>Which is &sect;1's first "
    "response, with a reason attached rather than an observation.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Closure, and why it matters"),
  ("callout", "P is closed under the operations you actually use",
   ["<b>Closed under complement</b> — run the algorithm and swap "
    "the answer. <b>Which NP is <i>not</i> known to be</b> "
    "(Module 05 &sect;1), <b>and that asymmetry is the entire content "
    "of co-NP</b> and one of the most useful structural facts in the "
    "course.",
    "<b>Closed under union, intersection, and concatenation</b>, and "
    "most importantly <b>under polynomial-time composition: a polynomial "
    "algorithm that calls a polynomial subroutine polynomially many times "
    "runs in polynomial time.</b>",
    "<b>Which is what makes modular programming compatible with "
    "complexity analysis</b> — you can reason about a subroutine's "
    "complexity in isolation and compose the results, which is not true "
    "for every resource bound (it fails for logarithmic space without "
    "care, Module 06 &sect;1).",
    "<b>And it means polynomial-time reductions compose</b> "
    "(Module 04 &sect;1) — <b>without which NP-completeness would "
    "not be a transitive notion and Garey and Johnson's catalogue of 300 "
    "problems would not be usable</b>, since each new proof relies on "
    "chaining through earlier ones. <b>The closure property is load-"
    "bearing for the whole practice of the field.</b>"]),

  ("h1", "4 &nbsp; What membership in P does not tell you"),
  ("ul", ["<b>Whether it is fast.</b> <b>An O(n&#8309;) algorithm with a "
          "large constant is in P and is unusable</b> on an input of a "
          "million elements — which is Module 01 &sect;4's point, "
          "and it applies to every P-membership result.",
          "<b>Whether it parallelises.</b> <b>NC is the "
          "parallel-tractable class, and whether NC = P is open</b> "
          "(Module 06 &sect;4) — so a problem in P may be "
          "inherently sequential, which matters a great deal given "
          "CSCE 735's hardware.",
          "<b>Whether it fits in memory.</b> A polynomial-time "
          "algorithm may use polynomial <i>space</i>, which is an "
          "entirely separate and frequently binding constraint "
          "(Module 06).",
          "<b>Whether it streams, works online, or tolerates "
          "approximation</b> — all real engineering requirements "
          "that the class does not express at all.",
          "<b>And whether the problem instances you have are anything "
          "like the worst case</b> — which is Module 12, and is "
          "<b>frequently the only question that actually matters.</b> "
          "<b>So 'it is in P' is good news and not an engineering "
          "answer:</b> it tells you to look for an efficient algorithm "
          "rather than for a proof that none exists."]),
  ("callout", "The practical reading of P",
   ["<b>'In P' means: a polynomial algorithm exists, so keep looking for "
    "a good one.</b> <b>The search is not futile, and that is the useful "
    "information</b> — it licenses spending time.",
    "<b>'NP-hard' means: stop looking for an exact polynomial algorithm, "
    "and start on Module 11's approximations or Module 12's "
    "parameters</b> — which is CSCE 627 Module 06 &sect;4's "
    "redirection argument, with a weaker but still useful conclusion.",
    "<b>'Neither known' means both searches are live</b>, and <b>graph "
    "isomorphism is the standing example of a problem that stayed in that "
    "position for fifty years</b> while serious people worked on both "
    "sides.",
    "<b>Which is the whole operational content of the "
    "classification.</b> <b>It redirects effort</b> — and that is "
    "worth a great deal more than it sounds, because <b>the alternative "
    "is spending months on a search whose outcome was determined before "
    "you started.</b>"]),
 ],
 "resources": [
   ("Arora & Barak &mdash; chapter 1, and the discussion of the thesis "
    "(free draft)",
    "https://theory.cs.princeton.edu/complexity/",
    "<b>P, the thesis, and the objections of &sect;1</b>, stated "
    "carefully."),
   ("Edmonds &mdash; Paths, Trees, and Flowers (free)",
    "https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/paths-trees-and-flowers/08B492B72322C4130AE800C0610E0E21",
    "<b>&sect;2's callout, in the original</b> — and the "
    "introduction is where the thesis is argued. Worth reading for the "
    "argument rather than the algorithm."),
   ("Babai &mdash; Graph Isomorphism in Quasipolynomial Time (free)",
    "https://arxiv.org/abs/1512.03547",
    "<b>&sect;2's fourth row</b> — the current state of the "
    "best-known NP-intermediate candidate."),
   ("Agrawal, Kayal & Saxena &mdash; PRIMES is in P (free)",
    "https://www.cse.iitk.ac.in/users/manindra/algebra/primality_v6.pdf",
    "<b>&sect;2's second row</b>, and remarkably short for what it "
    "settled."),
 ],
 "exercises": [
   "<b>State the Cobham–Edmonds thesis</b> and write the strongest "
   "objection you can.",
   "<b>Find the exponents of ten algorithms you know</b> and check "
   "&sect;1's claim about natural problems.",
   "<b>Construct a problem artificially in P with a large exponent</b> "
   "and note why it feels contrived.",
   "<b>Verify that P is closed under polynomial composition</b>, with the "
   "exponent arithmetic.",
   "<b>Show that P is closed under complement</b> and state why the same "
   "argument fails for NP.",
   "<b>Look up the current best algorithm for graph isomorphism</b> and "
   "state its running time.",
   "<b>Implement a Miller–Rabin primality test</b> and compare it "
   "against an AKS implementation if you can find one.",
   "<b>Pick three problems from your own work</b> and determine which are "
   "in P.",
   "<b>For one in P, find its best-known exponent</b> and assess whether "
   "that is practically adequate.",
   "<b>Write down what 'in P' licenses you to do</b>, in one sentence.",
 ],
 "selfcheck": [
   "Define P and state the Cobham–Edmonds thesis.",
   "What kind of claim is the thesis?",
   "Give five objections and the response to each.",
   "What is Edmonds' argument, and why is it better?",
   "Name four hard-won membership results and one still open.",
   "What does graph isomorphism's status suggest about NP's structure?",
   "Why does closure under composition matter so much?",
   "Name five things membership in P does not tell you.",
   "What does the classification operationally license?",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "NP, and Verification",
 "subtitle": "The class, and the question it poses.",
 "question": "Is checking an answer easier than finding one?",
 "outcomes": [
     "Define NP by certificates and by non-determinism, and prove "
     "them equivalent.",
     "Explain why the certificate definition is the useful one.",
     "Place problems in NP by exhibiting certificates.",
     "State P versus NP precisely and explain what it asks.",
     "Explain what a resolution either way would mean.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two definitions",
   "blurb": "And they are the same class."},

  {"t": "callout", "title": "NP is 'verifiable with a short certificate', and that is the definition to use",
   "kind": "The two formulations",
   "body": ["<b>Certificate definition:</b> L is in NP if there is a "
            "polynomial-time verifier V and a polynomial p such that "
            "x ∈ L exactly when some certificate c with "
            "|c| ≤ p(|x|) makes V(x,c) accept.",
            "<b>Non-determinism definition:</b> L is in NP if a "
            "non-deterministic Turing machine decides it in polynomial "
            "time.",
            "<b>They are equivalent</b> — the certificate is the "
            "sequence of non-deterministic choices, and the verifier is "
            "the machine following them.",
            "<b>And the certificate definition is the one to "
            "use</b>, because <b>it makes membership proofs "
            "concrete:</b> to show a problem is in NP, say what the "
            "certificate is and how it is checked. <b>Two sentences, "
            "every time.</b>"]},

  {"t": "table", "kicker": "Certificates", "title": "Membership in NP, by exhibiting the witness",
   "header": ["Problem", "Certificate", "Checked in polynomial time by"],
   "widths": [2.6, 3.4, 5.6],
   "rows": [
     ["<b>SAT</b>", "<b>A satisfying assignment</b>", "<b>Evaluating the formula</b>"],
     ["<b>Hamiltonian cycle</b>", "<b>The cycle</b>", "<b>Checking edges and that each vertex appears once</b>"],
     ["<b>Composite</b>", "<b>A non-trivial factor</b>", "<b>One division</b>"],
     ["<b>Subset sum</b>", "<b>The subset</b>", "<b>Adding it up</b>"],
     ["<b>Graph isomorphism</b>", "<b>The vertex mapping</b>", "<b>Checking edges correspond</b>"],
     ["<b>Sudoku solvability</b>", "<b>The completed grid</b>", "<b>Checking rows, columns, boxes</b>"],
   ],
   "footnote": "<b>If you can name the certificate in a sentence, the "
               "problem is in NP</b> — which makes the membership "
               "half of an NP-completeness proof routine, and it is the "
               "half people omit.",
   "note": "Insist on the membership half; it is graded and it is easy."},

  {"t": "section", "label": "Part 2", "title": "The question",
   "blurb": "P versus NP, stated precisely."},

  {"t": "callout", "title": "P versus NP asks whether verification is genuinely easier than search",
   "kind": "The informal reading, which is accurate",
   "body": ["<b>P is 'solvable quickly'. NP is 'checkable quickly, "
            "given the answer'.</b> <b>P ⊆ NP trivially</b> "
            "— if you can solve it you can check it, ignoring the "
            "certificate.",
            "<b>P = NP would mean that whenever a solution can be "
            "recognised, it can be found</b> — that checking and "
            "finding are the same difficulty.",
            "<b>Which is why the question matters outside the "
            "field.</b> <b>Mathematics is the search for proofs, which "
            "are checkable; design is the search for artefacts meeting "
            "checkable criteria.</b>",
            "<b>And it has been open since Cook's 1971 paper</b>, with "
            "<b>a widely shared belief that P ≠ NP and no proof "
            "in either direction</b> — which Modules 07 and 09 explain "
            "rather than excuse."]},

  {"t": "table", "kicker": "Consequences", "title": "What each resolution would mean",
   "header": ["If P = NP", "If P ≠ NP"],
   "widths": [5.5, 5.5],
   "rows": [
     ["<b>Public-key cryptography breaks</b>", "<b>Cryptography's assumptions remain plausible — though it needs more than P ≠ NP</b>"],
     ["<b>Optimisation becomes tractable — scheduling, design, routing</b>", "<b>The approximation and parameter work of M11–M12 is the right response</b>"],
     ["<b>Mathematical proof search becomes automatic</b>", "<b>Proof remains a creative act, in a provable sense</b>"],
     ["<b>And the constant matters enormously</b>", "<b>And we still do not know <i>how</i> hard — n² lower bounds are not proved either</b>"],
   ],
   "footnote": "<b>Note the asymmetry:</b> <b>P = NP would be "
               "transformative and P ≠ NP would change almost "
               "nothing operationally</b>, since everyone already assumes "
               "it — which is part of why the proof effort is "
               "intellectual rather than practical.",
   "note": "The asymmetry of consequences is worth stating."},

  {"t": "section", "label": "Part 3", "title": "The evidence",
   "blurb": "Why people believe it, and how good the reasons are."},

  {"t": "bullets", "kicker": "Evidence", "title": "Why P ≠ NP is believed",
   "items": [
     "<b>Fifty years of serious effort on thousands of NP-complete "
     "problems</b> has produced no polynomial algorithm for any of "
     "them. <b>The best single argument.</b>",
     "",
     "<b>And a polynomial algorithm for one gives one for all</b> "
     "(Module 04 §1), so the failures are jointly rather than "
     "separately informative.",
     "",
     "<b>The hierarchy theorems</b> (Module 07) <b>show that more "
     "time does buy more power</b>, so the general shape of the belief "
     "is consistent.",
     "",
     "<b>Circuit lower bounds for restricted models</b> "
     "(Module 09) <b>are real, non-trivial, and in the expected "
     "direction.</b>",
     "",
     "<b>And the honest counterweight:</b> <b>this is all empirical, "
     "and the field has theorems saying its techniques are "
     "inadequate</b> (M07 §4, M09 §3).",
   ],
   "footnote": "<b>The evidence is substantial and circumstantial</b>, "
               "and <b>a field that can prove its own methods "
               "insufficient has reason for humility about its "
               "beliefs.</b>"},

  {"t": "section", "label": "Part 4", "title": "NP's structure",
   "blurb": "Not two tiers."},

  {"t": "callout", "title": "If P ≠ NP, there are problems strictly between",
   "kind": "Ladner's theorem",
   "body": ["<b>Ladner's theorem: if P ≠ NP, then there exist "
            "NP problems that are neither in P nor NP-complete.</b> "
            "<b>NP-intermediate problems exist.</b>",
            "<b>The proof is a diagonalisation</b> "
            "(CSCE 627 §05) constructing a problem that is "
            "deliberately too hard for P and too easy for completeness "
            "— and the constructed problem is artificial.",
            "<b>The natural candidates are graph isomorphism and "
            "factoring</b> (Module 02 §2), both of which have "
            "resisted both classifications for decades.",
            "<b>So NP is not a two-tier structure of easy and "
            "complete</b> — <b>which matters when you meet a problem "
            "that resists both a polynomial algorithm and a hardness "
            "proof.</b> <b>That may be the correct answer rather than a "
            "failure.</b>"]},

  {"t": "bullets", "kicker": "Summary", "title": "What to carry from this module",
   "items": [
     "<b>Use the certificate definition.</b> <b>Membership in NP is "
     "two sentences: the witness and the check.</b>",
     "",
     "<b>P versus NP is 'is finding as easy as checking'</b>, which "
     "is a natural question and explains why it matters beyond the "
     "field.",
     "",
     "<b>The belief is empirically grounded and not proved</b>, and "
     "the field knows why it cannot prove it.",
     "",
     "<b>NP has a middle</b>, by Ladner, so 'neither' is a real "
     "answer.",
     "",
     "<b>And P = NP would be transformative while P ≠ NP would "
     "change almost nothing</b> — the practical world already "
     "assumes it.",
   ],
   "footnote": "<b>The certificate habit is the single most useful "
               "thing here</b>, and it is what Module 04's proofs are "
               "built on."},
 ],
 "takeaways": [
   "NP has two equivalent definitions, and the certificate one is the "
   "useful one — membership is two sentences: the witness and the "
   "check.",
   "P versus NP asks whether finding is as easy as checking, which is why "
   "it matters outside the field: mathematics and design are both searches "
   "for checkable things.",
   "P = NP would be transformative; P ≠ NP would change almost "
   "nothing operationally, since everyone already assumes it.",
   "The evidence is fifty years of failure across thousands of problems, "
   "made jointly informative by the fact that one algorithm would give "
   "all.",
   "And the field has theorems showing its own techniques cannot settle "
   "the question, which is grounds for humility.",
   "Ladner's theorem says NP has a middle if P ≠ NP, so 'neither in P "
   "nor NP-complete' is a real answer and not a failure to classify.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The two definitions"),
  ("callout", "NP is 'verifiable with a short certificate', and that is the "
              "definition to use",
   ["<b>Certificate definition:</b> a language L is in NP if there is a "
    "polynomial-time verifier V and a polynomial p such that x is in L "
    "exactly when there exists a certificate c with |c| at most p(|x|) "
    "for which V(x, c) accepts.",
    "<b>Non-determinism definition:</b> L is in NP if some "
    "non-deterministic Turing machine decides it in polynomial time "
    "— which is where the N comes from, and note it is "
    "<i>non-deterministic</i> rather than <i>non</i>-polynomial, a "
    "confusion worth heading off.",
    "<b>They are equivalent, and the proof is immediate in both "
    "directions</b> — <b>the certificate is precisely the sequence "
    "of non-deterministic choices the machine would make, and the verifier "
    "is the machine following them deterministically.</b>",
    "<b>And the certificate definition is the one to use in practice</b>, "
    "because <b>it makes membership proofs concrete:</b> to show a "
    "problem is in NP, state what the certificate is and how it is "
    "checked in polynomial time. <b>Two sentences, every time</b> "
    "(&sect;1's table) — whereas the non-deterministic formulation "
    "requires describing a machine."]),
  ("table", ["Problem", "Certificate", "Checked in polynomial time by"],
   [["<b>SAT</b>", "<b>A satisfying truth assignment.</b>",
     "<b>Evaluating the formula under it.</b>"],
    ["<b>Hamiltonian cycle</b>", "<b>The cycle, as a vertex "
     "sequence.</b>",
     "<b>Checking each consecutive pair is an edge and that every vertex "
     "appears exactly once.</b>"],
    ["<b>Compositeness</b>", "<b>A non-trivial factor.</b>",
     "<b>One division.</b> Note the contrast with primality, whose "
     "certificate is far less obvious — which is why PRIMES in "
     "co-NP, then NP, then P took decades."],
    ["<b>Subset sum</b>", "<b>The subset achieving the target.</b>",
     "<b>Adding it up.</b>"],
    ["<b>Graph isomorphism</b>",
     "<b>The vertex mapping between the two graphs.</b>",
     "<b>Checking that edges correspond under the mapping.</b>"],
    ["<b>Sudoku solvability</b>", "<b>The completed grid.</b>",
     "<b>Checking every row, column, and box.</b>"]],
   [0.21, 0.28, 0.51]),
  ("p", "<b>If you can name the certificate in a sentence, the problem is "
        "in NP</b> — <b>which makes the membership half of an "
        "NP-completeness proof routine</b>, and <b>it is the half people "
        "omit.</b> <b>A hardness proof alone establishes NP-hardness, not "
        "NP-completeness</b>, and the distinction matters because "
        "NP-hardness is compatible with the problem being far harder than "
        "NP (Module 05)."),

  ("h1", "2 &nbsp; The question"),
  ("callout", "P versus NP asks whether verification is genuinely easier "
              "than search",
   ["<b>P is 'solvable quickly'. NP is 'checkable quickly, given the "
    "right answer'.</b> <b>P is contained in NP trivially</b> — if "
    "you can solve a problem you can verify a claimed solution by ignoring "
    "the certificate and solving it yourself.",
    "<b>So P = NP would mean that whenever a solution can be recognised, "
    "it can be found</b> — that checking and finding are the same "
    "difficulty, up to a polynomial.",
    "<b>Which is why the question matters well outside the field.</b> "
    "<b>Mathematics is the search for proofs, and a proof is "
    "checkable</b> (CSCE 627 Module 10 &sect;1); <b>engineering "
    "design is the search for an artefact meeting criteria that can be "
    "checked</b>; so is drug design, circuit layout, and scheduling. "
    "<b>P = NP would make all of those mechanical.</b>",
    "<b>And the question has been open since Cook's 1971 paper</b> (and "
    "Levin's independent 1973 work), with <b>a widely shared belief that "
    "P &ne; NP and no proof in either direction</b> — <b>which "
    "Modules 07 and 09 explain rather than excuse</b>, since the field "
    "has theorems about why its techniques are insufficient."]),
  ("table", ["If P = NP", "If P ≠ NP"],
   [["<b>Public-key cryptography as deployed breaks</b> — the "
     "problems it rests on are in NP.",
     "<b>Cryptography's assumptions remain plausible</b> — though "
     "<b>it needs considerably more than P &ne; NP</b>, since it needs "
     "average-case hardness and one-way functions (CSCE 711)."],
    ["<b>Optimisation becomes tractable</b> — scheduling, routing, "
     "layout, protein design, all of it.",
     "<b>The approximation and parameterised work of Modules 11 and 12 "
     "is the correct response</b>, which is what the field has been "
     "doing."],
    ["<b>Mathematical proof search becomes automatic</b> for "
     "statements with short proofs, which is most of them.",
     "<b>Proof remains a creative act, in a provable sense</b> — "
     "which is a striking thing for a theorem to establish."],
    ["<b>And the constant and exponent would matter "
     "enormously</b> — an n<super>20</super> algorithm for SAT "
     "would be a mathematical earthquake and a practical "
     "irrelevance.",
     "<b>And we still would not know <i>how</i> hard</b> — "
     "<b>even quadratic lower bounds for SAT are not proved</b>, so "
     "P &ne; NP would leave most quantitative questions open."]],
   [0.50, 0.50]),
  ("p", "<b>Note the asymmetry:</b> <b>P = NP would be transformative, "
        "and P &ne; NP would change almost nothing operationally</b>, "
        "because everyone already assumes it and has built accordingly. "
        "<b>Which is part of why the proof effort is intellectual rather "
        "than practical</b>, and is worth saying when the question's "
        "importance is being justified by its applications."),

  ("break",),
  ("h1", "3 &nbsp; The evidence"),
  ("ul", ["<b>Fifty years of serious effort on thousands of NP-complete "
          "problems has produced no polynomial algorithm for any of "
          "them.</b> <b>The best single argument</b>, and it is a "
          "straightforwardly empirical one.",
          "<b>And a polynomial algorithm for any one of them would give "
          "one for all of them</b> (Module 04 &sect;1), <b>so the "
          "failures are jointly informative rather than separately</b> "
          "— thousands of independent research programmes all "
          "failing at what is formally one task.",
          "<b>The hierarchy theorems</b> (Module 07) <b>establish that "
          "more time genuinely does buy more computational power</b>, so "
          "the general shape of the belief is at least consistent with "
          "what is proved — the alternative would be strange.",
          "<b>Circuit lower bounds for restricted models</b> "
          "(Module 09) <b>are real, non-trivial, and in the expected "
          "direction</b> — monotone circuits, bounded-depth "
          "circuits, and certain algebraic models all have proved "
          "exponential lower bounds for NP-complete problems.",
          "<b>And the honest counterweight:</b> <b>all of this is "
          "circumstantial, and the field has proved theorems stating that "
          "its own principal techniques are inadequate to settle the "
          "question</b> (Module 07 &sect;4's relativisation and "
          "Module 09 &sect;3's natural proofs). <b>A field that can "
          "prove its own methods insufficient has reason for humility "
          "about its beliefs</b> — and stating that is more useful "
          "than reciting the consensus."]),

  ("h1", "4 &nbsp; NP's structure"),
  ("callout", "If P ≠ NP, there are problems strictly between",
   ["<b>Ladner's theorem: if P &ne; NP, then there exist problems in NP "
    "that are neither in P nor NP-complete.</b> <b>NP-intermediate "
    "problems exist</b>, conditionally on the central conjecture.",
    "<b>The proof is a diagonalisation</b> (CSCE 627 Module 05 "
    "&sect;3) <b>constructing a language that is deliberately made too "
    "hard to be in P and too easy to be complete</b>, by alternating "
    "between the two behaviours on sparse intervals — <b>and the "
    "constructed problem is entirely artificial</b>, which is the usual "
    "character of a diagonalisation's output.",
    "<b>The natural candidates are graph isomorphism and integer "
    "factoring</b> (Module 02 &sect;2), both of which have resisted "
    "both classifications for decades despite substantial attention.",
    "<b>So NP is not a two-tier structure of easy and complete.</b> "
    "<b>Which matters when you meet a problem that resists both a "
    "polynomial algorithm and a hardness proof:</b> <b>that may be the "
    "correct answer rather than a failure on your part</b>, and knowing "
    "the middle exists prevents a certain amount of wasted effort in both "
    "directions."]),
  ("ul", ["<b>Use the certificate definition.</b> <b>Membership in NP is "
          "two sentences: the witness, and how it is checked</b> "
          "(&sect;1).",
          "<b>P versus NP is 'is finding as easy as checking'</b>, which "
          "is a natural question and <b>explains why it matters beyond "
          "complexity theory</b> (&sect;2).",
          "<b>The belief that P &ne; NP is empirically grounded and not "
          "proved</b>, and <b>the field knows, as a theorem, why it has "
          "not been able to prove it.</b>",
          "<b>NP has a middle</b>, by Ladner, <b>so 'neither' is a real "
          "classification</b> rather than an admission of defeat.",
          "<b>And P = NP would be transformative while P &ne; NP would "
          "change almost nothing</b> — the practical world has "
          "already assumed it for fifty years. <b>The certificate habit "
          "is the single most useful thing in this module</b>, and it is "
          "what Module 04's proofs are built on."]),
 ],
 "resources": [
   ("Arora & Barak &mdash; chapter 2 (free draft)",
    "https://theory.cs.princeton.edu/complexity/",
    "<b>Both definitions of NP, their equivalence, and the structural "
    "material of &sect;4.</b>"),
   ("Cook &mdash; The Complexity of Theorem-Proving Procedures (free)",
    "https://dl.acm.org/doi/10.1145/800157.805047",
    "<b>The 1971 paper</b>, which is short and is where the question "
    "originates."),
   ("Aaronson &mdash; P =? NP (free survey)",
    "https://www.scottaaronson.com/papers/pnp.pdf",
    "<b>&sect;2 and &sect;3 assessed honestly</b> — the "
    "consequences, the evidence, and what the evidence is actually worth. "
    "The best thing written on the question for a general technical "
    "audience."),
   ("Ladner &mdash; On the Structure of Polynomial Time Reducibility "
    "(free)",
    "https://dl.acm.org/doi/10.1145/321864.321877",
    "<b>&sect;4's theorem</b>, with the alternating construction."),
 ],
 "exercises": [
   "<b>Give certificates and verifiers for six problems</b>, including "
   "three not in &sect;1's table.",
   "<b>Prove the two definitions of NP equivalent</b>, in both "
   "directions.",
   "<b>Find a problem where the certificate is not obvious</b> and work "
   "out what it is. Primality is a good one.",
   "<b>State P versus NP precisely</b> and then informally, and check the "
   "informal version is faithful.",
   "<b>Write the consequences of each resolution</b> for a domain you "
   "work in.",
   "<b>Explain why P ≠ NP would change little operationally.</b>",
   "<b>Assess the evidence for P ≠ NP</b> and state how convincing "
   "you find it, with reasons.",
   "<b>State Ladner's theorem</b> and explain why the constructed problem "
   "is artificial.",
   "<b>Look up graph isomorphism's and factoring's current status.</b>",
   "<b>Find a problem in your own work whose status you cannot "
   "determine</b>, and say what you tried.",
 ],
 "selfcheck": [
   "Give both definitions of NP and prove them equivalent.",
   "Why is the certificate definition the useful one?",
   "Give six problems with their certificates.",
   "Which half of an NP-completeness proof does the certificate give?",
   "State P versus NP and its informal reading.",
   "Give four consequences of each resolution, and note the asymmetry.",
   "Give five pieces of evidence for P ≠ NP and the counterweight.",
   "State Ladner's theorem and name the natural candidates.",
   "What does the existence of a middle mean for a problem you cannot "
   "classify?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "NP-Completeness",
 "subtitle": "One problem's difficulty, shared by thousands.",
 "question": "How can thousands of unrelated problems have exactly the "
             "same difficulty?",
 "outcomes": [
     "Define NP-hardness and NP-completeness and distinguish them.",
     "Explain the Cook–Levin theorem and what it establishes.",
     "Construct an NP-completeness proof with both halves.",
     "Choose the right problem to reduce from.",
     "Explain what NP-completeness does and does not predict.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The definitions",
   "blurb": "And the distinction people collapse."},

  {"t": "callout", "title": "NP-hard is about difficulty; NP-complete is about difficulty <i>and</i> membership",
   "kind": "The distinction that matters",
   "body": ["<b>L is NP-hard if every problem in NP reduces to it in "
            "polynomial time.</b> <b>L is NP-complete if it is NP-hard "
            "<i>and</i> in NP.</b>",
            "<b>So the halting problem is NP-hard and not "
            "NP-complete</b> — it is far harder, and not in NP at "
            "all. <b>NP-hard alone is a lower bound with no upper "
            "one.</b>",
            "<b>Which is why a hardness proof is only half a "
            "proof.</b> <b>The membership half takes two sentences</b> "
            "(Module 03 §1) <b>and is the half people omit.</b>",
            "<b>And the consequence of completeness is the striking "
            "part:</b> <b>a polynomial algorithm for any NP-complete "
            "problem gives one for every problem in NP</b>, so they stand "
            "or fall together."]},

  {"t": "code", "kicker": "Why it works", "title": "Polynomial reductions compose, and that is the whole mechanism",
   "lang": "text", "code": """
  A <=_p B means: a polynomial-time computable f with
      x in A  <=>  f(x) in B

  TRANSITIVITY: if A <=_p B and B <=_p C then A <=_p C,
  because the composition of two polynomials is a
  polynomial (Module 02 Part 3).

  SO: once ONE problem is known NP-complete, proving a
  second requires only a reduction FROM the first --
  not from all of NP.

      every problem in NP  <=_p  SAT      (Cook-Levin)
      SAT                  <=_p  3-SAT
      3-SAT                <=_p  your problem
      -------------------------------------------
      every problem in NP  <=_p  your problem

  WITHOUT TRANSITIVITY there would be no catalogue and
  every proof would start from scratch. The closure
  property of Module 02 Part 3 is doing all the work here.

  AND THE DIRECTION IS THE SAME AS CSCE 627 MODULE 06:
  reduce the KNOWN HARD problem TO yours. Reducing yours to
  3-SAT proves your problem is IN NP, which is the other
  half and is a different claim.
""",
   "caption": "<b>Transitivity is why a catalogue exists</b> — and "
              "the direction error here is the same error as in "
              "CSCE 627, with the same fix: write down what reduces to "
              "what.",
   "note": "The two-halves-two-directions point prevents the most common "
           "mistake."},

  {"t": "section", "label": "Part 2", "title": "Cook–Levin",
   "blurb": "The first one, and how it was obtained."},

  {"t": "callout", "title": "Cook–Levin: SAT is NP-complete, by encoding a computation as a formula",
   "kind": "The bootstrapping theorem",
   "body": ["<b>Given any non-deterministic polynomial-time machine M "
            "and input x, construct a formula satisfiable exactly when M "
            "accepts x.</b>",
            "<b>The formula's variables describe a computation "
            "<i>tableau</i></b> — a grid of cells recording the "
            "machine's tape, head, and state at each of polynomially many "
            "steps.",
            "<b>And the clauses enforce local consistency:</b> the "
            "first row is the start configuration, each row follows from "
            "the previous by a transition, and some row accepts.",
            "<b>So satisfiability of the formula <i>is</i> the "
            "existence of an accepting computation.</b> <b>The theorem "
            "works because logic is expressive enough to describe "
            "computation, which is CSCE 627 §10's "
            "arithmetisation idea in a different setting.</b>"]},

  {"t": "table", "kicker": "The library", "title": "The problems to reduce from",
   "header": ["Problem", "Use it when your problem involves"],
   "widths": [3.4, 7.6],
   "rows": [
     ["<b>3-SAT</b>", "<b>Logical constraints, or nothing else fits. The default</b>"],
     ["<b>Vertex cover / independent set / clique</b>", "<b>Selecting a set of objects subject to conflicts</b>"],
     ["<b>Hamiltonian cycle / path</b>", "<b>Ordering or sequencing everything exactly once</b>"],
     ["<b>3-dimensional matching</b>", "<b>Grouping into triples</b>"],
     ["<b>Subset sum / partition</b>", "<b>Numbers and arithmetic targets</b>"],
     ["<b>Graph colouring</b>", "<b>Assignment with conflict constraints</b>"],
     ["<b>Set cover</b>", "<b>Covering, and note it is also the hardness-of-approximation case (M11)</b>"],
   ],
   "footnote": "<b>Choose the one structurally closest to your "
               "problem</b> — the reduction will be far shorter, "
               "which is CSCE 627 §06's library argument with a "
               "bigger library.",
   "note": "This table is the practical core; it is what people actually "
           "need."},

  {"t": "section", "label": "Part 3", "title": "Constructing one",
   "blurb": "The procedure, and where it goes wrong."},

  {"t": "code", "kicker": "Procedure", "title": "An NP-completeness proof, step by step",
   "lang": "text", "code": """
  1. MEMBERSHIP. Name the certificate and the check.
     Two sentences (Module 03 Part 1). Do this FIRST,
     because if it fails your problem is not in NP and you
     are proving something else.

  2. CHOOSE the source problem from Part 2's table.

  3. CONSTRUCT f: an instance of the source -> an instance
     of yours.

  4. PROVE both directions:
         source YES  =>  your problem YES
         your YES    =>  source YES
     The second direction is where proofs fail. It requires
     showing that EVERY solution to your instance comes
     from a source solution -- including solutions the
     construction did not intend.

  5. VERIFY f is polynomial-time. Usually obvious, and
     state it; a reduction that blows up the instance size
     exponentially is not a reduction.

  THE COMMON ERRORS
     omitting step 1 -> you proved NP-hardness only
     reversing step 3 -> you proved membership, not hardness
     hand-waving step 4's second direction -> the proof is
         simply incomplete, and this is the usual failure
""",
   "caption": "<b>Step 4's second direction is where real proofs "
              "fail</b> — unintended solutions to your constructed "
              "instance are the thing to rule out.",
   "note": "Emphasise the reverse direction; it is where grading "
           "bites."},

  {"t": "section", "label": "Part 4", "title": "What it predicts",
   "blurb": "And what it does not."},

  {"t": "callout", "title": "NP-completeness is a starting point, not a verdict",
   "kind": "The practical reading",
   "body": ["<b>It says: no polynomial algorithm is known, and finding "
            "one would resolve a famous open problem.</b> <b>That is "
            "strong evidence and not a proof of intractability.</b>",
            "<b>It says nothing about your instances.</b> <b>SAT "
            "solvers handle millions of variables</b> "
            "(CSCE 625 §08); <b>MIP solvers improved a millionfold "
            "in thirty years</b> (CSCE 669 §09).",
            "<b>It does not tell you the approximation picture</b> "
            "— which may be excellent (knapsack has an FPTAS) or "
            "hopeless (clique) — <b>and that is Module 11.</b>",
            "<b>Nor whether a parameter makes it easy</b> — vertex "
            "cover is NP-complete and fixed-parameter tractable, which "
            "is Module 12. <b>So the label begins the engineering.</b>"]},

  {"t": "bullets", "kicker": "After the proof", "title": "What to do once you know it is NP-complete",
   "items": [
     "<b>Try a solver.</b> <b>SAT, SMT, MIP, or CP</b> "
     "(CSCE 669 §13) — <b>and your instances may simply "
     "not be hard.</b>",
     "",
     "<b>Look for an approximation guarantee</b> "
     "(CSCE 669 §10, Module 11) <b>and the matching hardness "
     "bound.</b>",
     "",
     "<b>Look for a parameter</b> (Module 12) — treewidth, "
     "solution size, or a structural restriction.",
     "",
     "<b>Check whether a special case is in P</b> — planar, "
     "bipartite, bounded-degree, interval. <b>Frequently it is.</b>",
     "",
     "<b>And compute a bound even if you use a heuristic</b> "
     "(CSCE 669 §13 §3) — 'within 7% of optimal' "
     "is a far stronger claim than a number.",
   ],
   "footnote": "<b>All five are routinely productive</b>, which is why "
               "'NP-complete, therefore hopeless' is the wrong inference "
               "and the common one."},
 ],
 "takeaways": [
   "NP-hard is a lower bound with no upper one; NP-complete is NP-hard "
   "plus membership — so the halting problem is NP-hard and not "
   "NP-complete.",
   "Polynomial reductions compose, which is why one completeness proof "
   "bootstraps a catalogue of thousands.",
   "Cook–Levin encodes a computation tableau as a formula, so "
   "satisfiability becomes the existence of an accepting computation.",
   "Choose the source problem structurally closest to yours, and the "
   "reduction is far shorter.",
   "The reverse direction of the correctness proof is where real proofs "
   "fail — unintended solutions to the constructed instance are the "
   "thing to rule out.",
   "NP-completeness says nothing about your instances, the approximation "
   "picture, or whether a parameter helps — so the label begins the "
   "engineering rather than ending it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The definitions, and the mechanism"),
  ("callout", "NP-hard is about difficulty; NP-complete is about difficulty "
              "<i>and</i> membership",
   ["<b>L is NP-hard if every problem in NP reduces to it in polynomial "
    "time.</b> <b>L is NP-complete if it is NP-hard <i>and</i> is itself "
    "in NP.</b>",
    "<b>So the halting problem is NP-hard and emphatically not "
    "NP-complete</b> — it is undecidable, and therefore not in NP at "
    "all (CSCE 627 Module 05). <b>NP-hardness alone is a lower bound "
    "with no upper bound attached</b>, which is why the distinction is "
    "not pedantry.",
    "<b>Which is why a hardness proof is only half a proof.</b> <b>The "
    "membership half takes two sentences</b> (Module 03 &sect;1's "
    "certificate) <b>and is the half people omit</b> — and omitting "
    "it means you have proved a weaker and different statement.",
    "<b>And the consequence of completeness is the striking part:</b> "
    "<b>a polynomial-time algorithm for any single NP-complete problem "
    "yields one for every problem in NP</b>, by composing with the "
    "reductions. <b>So thousands of problems from unrelated fields stand "
    "or fall together</b>, which is the fact that makes the "
    "classification worth having."]),
  ("code", """A <=_p B means: there is a polynomial-time computable f with
    x in A  <=>  f(x) in B

TRANSITIVITY: if A <=_p B and B <=_p C then A <=_p C,
because the composition of two polynomials is a polynomial
(Module 02 section 3's closure property).

SO: once ONE problem is known to be NP-complete, proving a
second requires only a reduction FROM the first -- not from
all of NP.

    every problem in NP  <=_p  SAT        (Cook-Levin)
    SAT                  <=_p  3-SAT
    3-SAT                <=_p  your problem
    -------------------------------------------------
    every problem in NP  <=_p  your problem

WITHOUT TRANSITIVITY there would be no catalogue, and every
proof would have to start from the definition of NP. The
closure property of Module 02 is doing all the work here.

AND THE DIRECTION IS THE SAME AS CSCE 627 MODULE 06:
reduce the KNOWN HARD problem TO yours. Reducing YOURS to
3-SAT proves your problem is IN NP, which is the other half
and a different claim entirely."""),
  ("p", "<b>Transitivity is why a catalogue exists</b> — Garey and "
        "Johnson's three hundred problems are three hundred reductions "
        "chained through each other — <b>and the direction error "
        "here is exactly the same error as in CSCE 627 Module 06 "
        "&sect;1, with the same fix: write down explicitly what reduces "
        "to what, every time.</b> <b>Note also that reducing your problem "
        "to 3-SAT is not wasted work</b>: it is how you solve it with a "
        "SAT solver (&sect;4)."),

  ("h1", "2 &nbsp; Cook–Levin, and the library"),
  ("callout", "Cook–Levin: SAT is NP-complete, by encoding a "
              "computation as a formula",
   ["<b>Given any non-deterministic polynomial-time machine M and an "
    "input x, construct a propositional formula that is satisfiable "
    "exactly when M accepts x.</b> That is the whole statement, and it "
    "is what bootstraps the field.",
    "<b>The formula's variables describe a computation "
    "<i>tableau</i></b> — a grid with one row per time step and one "
    "column per tape cell, recording the symbol in each cell, the head's "
    "position, and the machine's state. <b>Polynomially many rows and "
    "columns, so polynomially many variables.</b>",
    "<b>And the clauses enforce local consistency:</b> the first row "
    "encodes the start configuration with x on the tape; each row follows "
    "from the one above by one of M's transitions, checked in 2&times;3 "
    "windows; and some row is accepting. <b>Every constraint is "
    "local</b>, which is why it fits in a formula of polynomial size.",
    "<b>So satisfiability of that formula <i>is</i> the existence of an "
    "accepting computation of M on x.</b> <b>The theorem works because "
    "propositional logic is expressive enough to describe computation "
    "step by step</b> — which is <b>CSCE 627 Module 10 "
    "&sect;2's arithmetisation idea in a different setting</b>, and is "
    "also exactly what bounded model checking exploits (CSCE 627 "
    "Module 08 &sect;3)."]),
  ("table", ["Reduce from", "When your problem involves"],
   [["<b>3-SAT</b>",
     "<b>Logical constraints, or nothing else fits. The default, and the "
     "usual answer.</b>"],
    ["<b>Vertex cover, independent set, clique</b>",
     "<b>Selecting a set of objects subject to pairwise conflicts</b> "
     "— and the three are trivially interreducible, so pick whichever "
     "matches your framing."],
    ["<b>Hamiltonian cycle or path</b>",
     "<b>Ordering or sequencing, visiting everything exactly once</b> "
     "— routing, scheduling without repetition, genome assembly."],
    ["<b>3-dimensional matching</b>",
     "<b>Grouping into triples</b> — and it is the right source for "
     "many partition-like problems where 3-SAT is awkward."],
    ["<b>Subset sum, partition</b>",
     "<b>Numbers and arithmetic targets</b> — and note these are the "
     "pseudo-polynomial ones (Module 01 &sect;2), so the hardness "
     "depends on large numbers."],
    ["<b>Graph colouring</b>",
     "<b>Assignment under conflict constraints</b> — register "
     "allocation (CSCE 605), frequency assignment, timetabling."],
    ["<b>Set cover</b>",
     "<b>Covering a universe with chosen subsets</b> — and note it "
     "is also the canonical hardness-of-approximation case "
     "(Module 11 &sect;3)."]],
   [0.30, 0.70]),
  ("p", "<b>Choose the source problem structurally closest to your "
        "own</b> — the reduction will be dramatically shorter and far "
        "less error-prone — <b>which is CSCE 627 Module 06 "
        "&sect;3's library argument, with a much bigger library.</b> "
        "<b>Garey and Johnson's appendix is the library</b>, and an hour "
        "spent finding the right source saves a day constructing a "
        "reduction from the wrong one."),

  ("break",),
  ("h1", "3 &nbsp; Constructing a proof"),
  ("code", """1. MEMBERSHIP. Name the certificate and the check. Two
   sentences (Module 03 section 1). DO THIS FIRST, because
   if it fails then your problem is not in NP and you are
   proving something other than what you intended.

2. CHOOSE the source problem from section 2's table.

3. CONSTRUCT f: an instance of the source -> an instance
   of your problem.

4. PROVE BOTH DIRECTIONS:
       source YES  =>  your problem YES
       your YES    =>  source YES
   The SECOND direction is where proofs fail. It requires
   showing that EVERY solution to your constructed instance
   arises from a solution to the source -- including
   solutions your construction did not anticipate and does
   not want.

5. VERIFY f runs in polynomial time. Usually obvious, and
   state it anyway: a reduction that blows up the instance
   size exponentially is not a reduction.

THE COMMON ERRORS
   omitting step 1  -> you proved NP-hardness only
   reversing step 3 -> you proved membership, not hardness
   hand-waving step 4's second direction -> the proof is
       simply incomplete, and this is the usual failure"""),
  ("p", "<b>Step 4's second direction is where real proofs fail.</b> "
        "<b>Unintended solutions to your constructed instance are the "
        "thing to rule out</b> — you built a graph intending the "
        "solver to find a particular kind of structure, and you must show "
        "no other structure satisfies the constraints, which frequently "
        "requires adding gadgets purely to forbid alternatives. <b>A "
        "proof that handles only the forward direction is not a flawed "
        "proof; it is half a proof.</b>"),

  ("h1", "4 &nbsp; What NP-completeness predicts"),
  ("callout", "NP-completeness is a starting point, not a verdict",
   ["<b>It says: no polynomial-time algorithm is known, and finding one "
    "would resolve a famous open problem in the affirmative.</b> <b>That "
    "is strong evidence of difficulty and it is not a proof of "
    "intractability</b> — which is Module 03 &sect;2's "
    "conditionality, and it is the honest reading.",
    "<b>It says nothing whatsoever about your particular "
    "instances.</b> <b>SAT solvers handle instances with millions of "
    "variables</b> (CSCE 625 Module 08 &sect;2); <b>mixed-integer "
    "programming solvers improved by a factor of a million in thirty "
    "years</b> (CSCE 669 Module 09 &sect;4). <b>Both on NP-complete "
    "problems.</b>",
    "<b>It does not tell you the approximation picture</b>, which may "
    "be excellent (knapsack has a fully polynomial approximation scheme) "
    "or hopeless (clique admits no constant factor) — <b>and those "
    "two are both NP-complete, so the label does not distinguish "
    "them.</b> <b>That is Module 11.</b>",
    "<b>Nor whether a parameter makes it easy.</b> <b>Vertex cover is "
    "NP-complete and fixed-parameter tractable</b>, solvable in time "
    "exponential only in the solution size — which is Module 12, "
    "and is the most practically useful material in the course. <b>So "
    "the label begins the engineering rather than concluding it.</b>"]),
  ("ul", ["<b>Try a solver.</b> <b>SAT, SMT, mixed-integer, or "
          "constraint programming</b> (CSCE 669 Module 13 "
          "&sect;1) — <b>and your instances may simply not be "
          "hard</b>, which you will not know until you try.",
          "<b>Look for an approximation guarantee</b> (CSCE 669 "
          "Module 10, and Module 11 here) <b>and for the matching "
          "hardness-of-approximation bound</b>, so you know whether a "
          "better ratio is available.",
          "<b>Look for a parameter</b> (Module 12) — treewidth, "
          "solution size, number of distinct values, a structural "
          "restriction. <b>This is the most reliably productive "
          "step.</b>",
          "<b>Check whether your special case is in P.</b> Planar, "
          "bipartite, bounded-degree, interval, chordal, series-parallel "
          "— <b>frequently it is</b>, and the restriction is "
          "frequently one your instances satisfy anyway.",
          "<b>And compute a bound even if you ultimately use a "
          "heuristic</b> (CSCE 669 Module 13 &sect;3) — "
          "<b>'within 7% of optimal' is a categorically stronger claim "
          "than a number</b>. <b>All five are routinely productive</b>, "
          "which is why <b>'NP-complete, therefore hopeless' is the wrong "
          "inference and the common one.</b>"]),
 ],
 "resources": [
   ("Arora & Barak &mdash; chapter 2, and Sipser chapter 7 (free "
    "draft)",
    "https://theory.cs.princeton.edu/complexity/",
    "<b>Cook–Levin with the tableau construction</b>, and the "
    "standard reductions."),
   ("Garey & Johnson &mdash; Computers and Intractability",
    "https://www.worldcat.org/title/1097888",
    "<b>&sect;2's library, in full</b> — three hundred problems with "
    "their status, and the guide to constructing reductions in chapter 3. "
    "Library copy, and still the reference."),
   ("Karp &mdash; Reducibility Among Combinatorial Problems (free)",
    "https://cgi.di.uoa.gr/~sgk/teaching/grad/handouts/karp.pdf",
    "<b>The 1972 paper that produced the first twenty-one</b>, and "
    "turned Cook's single theorem into a field."),
   ("Levin &mdash; Universal sequential search problems (translation, "
    "free)",
    "https://www.mathnet.ru/links/b7d0bfe5f12b7b0bc8d7c8c0eb73b9d3/ppi914.pdf",
    "<b>The independent 1973 formulation</b>, which is two pages and "
    "frames the question differently."),
 ],
 "exercises": [
   "<b>State the difference between NP-hard and NP-complete</b> and give "
   "a problem that is the first and not the second.",
   "<b>Prove that polynomial reductions compose</b>, with the exponent "
   "arithmetic.",
   "<b>Work through the Cook–Levin tableau construction</b> for a "
   "two-state machine and a three-cell tape.",
   "<b>Reduce 3-SAT to vertex cover</b> yourself, both directions.",
   "<b>Reduce 3-SAT to a problem from your own work</b>, following "
   "&sect;3's five steps.",
   "<b>Write the membership half explicitly</b>, with the certificate.",
   "<b>Find the unintended solutions</b> to your constructed instance and "
   "add a gadget to forbid them.",
   "<b>Encode an NP-complete problem for a SAT solver</b> and run it on "
   "instances of growing size. Report where it breaks.",
   "<b>Find a special case of your problem that is in P</b> and prove "
   "it.",
   "<b>Apply all five of &sect;4's steps</b> to one problem and report "
   "which helped.",
 ],
 "selfcheck": [
   "Distinguish NP-hard from NP-complete, with an example.",
   "Why is a hardness proof only half a proof?",
   "Why does transitivity matter, and what would be lost without it?",
   "Explain the Cook–Levin construction.",
   "Why is logic expressive enough for it to work?",
   "Name seven problems to reduce from and when to use each.",
   "Give the five steps of a completeness proof and the three common "
   "errors.",
   "Where do real proofs fail, and why?",
   "Name four things NP-completeness does not tell you.",
   "Give five things to do after proving it.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Beyond NP",
 "subtitle": "co-NP, PSPACE, and the hierarchy.",
 "question": "What is harder than NP, and how would you know?",
 "outcomes": [
     "Define co-NP and explain the asymmetry.",
     "Define PSPACE and explain why games live there.",
     "Explain the polynomial hierarchy and what it measures.",
     "Place problems using quantifier alternation.",
     "Explain what collapses would mean.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "co-NP",
   "blurb": "The asymmetry of certificates."},

  {"t": "callout", "title": "co-NP is 'short certificates for NO instances'",
   "kind": "And the asymmetry is not known to be removable",
   "body": ["<b>NP has short certificates for yes. co-NP has short "
            "certificates for no.</b> <b>A formula being satisfiable "
            "has a witness; being <i>un</i>satisfiable has no obvious "
            "one.</b>",
            "<b>So TAUTOLOGY and UNSAT are co-NP-complete</b>, and "
            "<b>whether NP = co-NP is open</b> — a separate open "
            "question from P versus NP, though P = NP would imply "
            "NP = co-NP.",
            "<b>And this is CSCE 627 §04's recognisable/co-"
            "recognisable asymmetry with a resource bound</b> — the "
            "same structure, where the complement question was settled "
            "and here it is not.",
            "<b>The practical trace is real:</b> <b>a SAT solver "
            "emitting an unsatisfiability proof is producing a co-NP "
            "certificate</b> (CSCE 625 §08) — <b>which is "
            "why those proofs can be long, and why the existence of short "
            "ones is the NP = co-NP question.</b>"]},

  {"t": "table", "kicker": "Certificates", "title": "Which direction has the witness",
   "header": ["Problem", "Class", "The certificate"],
   "widths": [3.0, 2.6, 5.6],
   "rows": [
     ["<b>SAT</b>", "<b>NP-complete</b>", "<b>A satisfying assignment (yes)</b>"],
     ["<b>UNSAT, TAUTOLOGY</b>", "<b>co-NP-complete</b>", "<b>A refutation — possibly exponentially long</b>"],
     ["<b>Primality</b>", "<b>In P (and in NP ∩ co-NP)</b>", "<b>Pratt certificate; and a factor for composite</b>"],
     ["<b>Factoring (decision)</b>", "<b>NP ∩ co-NP</b>", "<b>The factorisation, both ways</b>"],
     ["<b>Graph non-isomorphism</b>", "<b>Not known in NP</b>", "<b>No short certificate known — but see M10</b>"],
   ],
   "footnote": "<b>A problem in NP ∩ co-NP is unlikely to be "
               "NP-complete</b> — that would imply NP = co-NP "
               "— which is why factoring's membership there is "
               "evidence it is NP-intermediate (M03 §4).",
   "note": "The NP-intersect-co-NP argument is a genuinely useful "
           "heuristic."},

  {"t": "section", "label": "Part 2", "title": "PSPACE",
   "blurb": "Where games live."},

  {"t": "callout", "title": "PSPACE is polynomial space, and it contains the games",
   "kind": "Why alternation costs more than choice",
   "body": ["<b>PSPACE is the problems decidable with polynomial "
            "<i>space</i> and unbounded time.</b> <b>NP ⊆ "
            "PSPACE</b> — try every certificate, reusing the "
            "space.",
            "<b>And TQBF — is a fully quantified Boolean formula "
            "true? — is PSPACE-complete.</b> <b>Alternating "
            "quantifiers rather than a single existential.</b>",
            "<b>Which is why two-player games are PSPACE-complete:</b> "
            "<b>'I have a move such that for all your moves I have a "
            "move…' is exactly alternating quantification</b> "
            "(CSCE 625 §05's minimax).",
            "<b>Generalised geography, Go endgames, and Reversi are "
            "PSPACE-complete</b>, and <b>chess and Go on an "
            "n×n board are EXPTIME-complete</b> — harder "
            "still, because the game can be exponentially long."]},

  {"t": "code", "kicker": "The landscape", "title": "The classes, in order",
   "lang": "text", "code": """
  L  subset  NL  subset  P  subset  NP  subset  PH
     subset  PSPACE  subset  EXPTIME  subset  EXPSPACE

  EVERY INCLUSION SHOWN IS KNOWN.
  NOT ONE of the inclusions from P to PSPACE is known to be
  STRICT. P = PSPACE is not ruled out, though nobody
  believes it.

  WHAT IS PROVED STRICT:
      P != EXPTIME        (time hierarchy, Module 07)
      NL != PSPACE        (space hierarchy)
      L != PSPACE

  SO THE HIERARCHY THEOREMS GIVE SEPARATIONS ONLY WHEN THE
  RESOURCE GAP IS LARGE -- exponential, not polynomial.
  And P vs NP is a question about machines with the SAME
  resource bound and different determinism, which is
  exactly what those theorems cannot address (Module 07
  Part 4).

  THE PRACTICAL READING: "PSPACE-complete" means harder
  than NP-complete in all likelihood, and the solvers are
  correspondingly worse. A PSPACE-complete problem is where
  you should expect a solver to fail.
""",
   "caption": "<b>Almost nothing is known to be strict</b>, which is the "
              "honest state of the landscape and is worth seeing laid "
              "out.",
   "note": "Students assume these separations are known; they are not."},

  {"t": "section", "label": "Part 3", "title": "The polynomial hierarchy",
   "blurb": "Quantifier alternation, bounded."},

  {"t": "callout", "title": "The polynomial hierarchy is CSCE 627's arithmetic hierarchy with polynomial witnesses",
   "kind": "The same construction, bounded",
   "body": ["<b>Σ₁ᵖ is NP: ∃ a short witness. "
            "Π₁ᵖ is co-NP: ∀ short "
            "witnesses.</b>",
            "<b>Σ₂ᵖ is ∃ then ∀, and "
            "so on</b> — <b>exactly CSCE 627 §07's "
            "hierarchy with the quantifiers restricted to "
            "polynomial-length strings.</b>",
            "<b>Natural problems live at level 2:</b> <b>'is this the "
            "minimum-size circuit computing this function?' is "
            "∃ a circuit ∀ inputs</b> — which is why "
            "circuit minimisation is harder than SAT.",
            "<b>And the hierarchy is believed strict and not known to "
            "be.</b> <b>If any two adjacent levels coincide, the whole "
            "hierarchy collapses to that level</b> — so "
            "P = NP would collapse all of it."]},

  {"t": "bullets", "kicker": "Placing", "title": "Problems above NP",
   "items": [
     "<b>Circuit minimisation.</b> <b>Σ₂ᵖ</b> — "
     "exists a small circuit, for all inputs it agrees.",
     "",
     "<b>Succinct set cover, and most 'is this the best X' "
     "questions.</b> <b>Optimality is one quantifier above "
     "existence.</b>",
     "",
     "<b>Two-player games with polynomially many moves.</b> "
     "<b>PSPACE-complete</b> — TQBF in disguise.",
     "",
     "<b>Games of exponential length</b> (chess, Go generalised). "
     "<b>EXPTIME-complete.</b>",
     "",
     "<b>And model checking with full temporal logic</b>, which sits "
     "in PSPACE — which is why it is harder than SAT-based bounded "
     "checking (CSCE 627 §08).",
   ],
   "footnote": "<b>'Is this the best?' is systematically one level "
               "harder than 'is there a good one?'</b> — which is "
               "the most useful placing heuristic in this module."},

  {"t": "section", "label": "Part 4", "title": "What collapses mean",
   "blurb": "And why they are believed not to happen."},

  {"t": "callout", "title": "A collapse would be a structural surprise, which is the evidence against it",
   "kind": "How the field reasons under uncertainty",
   "body": ["<b>If NP = co-NP, then unsatisfiability has short "
            "certificates</b>, which decades of proof-complexity work "
            "suggests it does not.",
            "<b>If the polynomial hierarchy collapses, then adding "
            "quantifier alternation adds no power</b> — and "
            "CSCE 627 §07 showed it does add power when "
            "unbounded.",
            "<b>So the arguments are structural:</b> <b>a collapse "
            "would make a natural-looking distinction vanish</b>, and "
            "the field treats that as evidence against.",
            "<b>Which is weaker than proof and is what is "
            "available</b> — <b>and the collapse results are used "
            "<i>as</i> evidence:</b> 'X would collapse the hierarchy' is "
            "a standard argument that X is false."]},

  {"t": "callout", "title": "The practical content of everything above NP",
   "kind": "Honest summary",
   "body": ["<b>NP-complete: solvers work, sometimes very well.</b> "
            "<b>Try one.</b>",
            "<b>Above NP (Σ₂ᵖ and beyond): expect "
            "solvers to struggle</b>, and <b>QBF solvers exist and are "
            "much weaker than SAT solvers</b>, which is the practical "
            "trace of the separation.",
            "<b>PSPACE-complete: a solver will probably not help</b>, "
            "and the engineering response is restriction or "
            "approximation.",
            "<b>And the placing heuristic is quantifier "
            "alternation:</b> <b>count the alternations in the natural "
            "statement of your problem, and that is roughly where it "
            "sits</b> — the same method as CSCE 627 "
            "§07 §2."]},
 ],
 "takeaways": [
   "co-NP has short certificates for no-instances, and whether NP = co-NP "
   "is a separate open question — a SAT solver's unsatisfiability "
   "proof is a co-NP certificate.",
   "A problem in NP ∩ co-NP is unlikely to be NP-complete, which is "
   "why factoring's membership there is evidence it is NP-intermediate.",
   "PSPACE contains the two-player games, because alternating "
   "quantification is exactly what a game is.",
   "Not one inclusion from P to PSPACE is known to be strict, and the "
   "hierarchy theorems only separate exponentially different resource "
   "bounds.",
   "The polynomial hierarchy is CSCE 627's arithmetic hierarchy with "
   "polynomial witnesses, and if any two adjacent levels coincide it all "
   "collapses.",
   "'Is this the best?' is systematically one level harder than 'is there "
   "a good one?' — the most useful placing heuristic here.",
 ],
 "notes": [
  ("h1", "1 &nbsp; co-NP"),
  ("callout", "co-NP is 'short certificates for NO instances'",
   ["<b>NP has short certificates for yes-instances. co-NP has short "
    "certificates for no-instances.</b> <b>A formula being satisfiable "
    "has an obvious witness — the assignment — and a formula "
    "being <i>un</i>satisfiable has no obvious witness at all</b>, since "
    "every assignment must fail.",
    "<b>So TAUTOLOGY and UNSAT are co-NP-complete</b>, and <b>whether "
    "NP = co-NP is open</b> — <b>a genuinely separate question from "
    "P versus NP</b>, though P = NP would imply NP = co-NP (since P is "
    "closed under complement, Module 02 &sect;3).",
    "<b>And this is CSCE 627 Module 04 &sect;2's "
    "recognisable/co-recognisable asymmetry with a resource bound "
    "attached</b> — the same structural question, where in the "
    "unbounded setting it was settled (recognisable is not closed under "
    "complement, proved) and here it is open. <b>Which is a good "
    "illustration of how adding resources makes questions harder rather "
    "than easier.</b>",
    "<b>The practical trace is real:</b> <b>a SAT solver emitting an "
    "unsatisfiability proof is producing a co-NP certificate</b> "
    "(CSCE 625 Module 08 &sect;2) — <b>and that is why those "
    "proofs can be enormous, sometimes terabytes</b>. <b>Whether short "
    "ones always exist is precisely the NP = co-NP question</b>, which "
    "makes proof complexity a direct attack on it."]),
  ("table", ["Problem", "Class", "The certificate"],
   [["<b>SAT</b>", "<b>NP-complete</b>",
     "<b>A satisfying assignment, for a yes.</b>"],
    ["<b>UNSAT, TAUTOLOGY</b>", "<b>co-NP-complete</b>",
     "<b>A refutation — which exists and may be exponentially "
     "long.</b>"],
    ["<b>Primality</b>",
     "<b>In P</b> (Module 02 &sect;2), <b>and historically in "
     "NP &cap; co-NP</b>",
     "<b>A Pratt certificate for prime; a factor for composite.</b> The "
     "NP &cap; co-NP membership was known decades before AKS, and was "
     "evidence it would turn out to be in P."],
    ["<b>Factoring (decision version)</b>", "<b>NP &cap; co-NP</b>",
     "<b>The factorisation certifies both directions.</b> See the "
     "note."],
    ["<b>Graph non-isomorphism</b>", "<b>Not known to be in NP</b>",
     "<b>No short certificate is known</b> — <b>but there is an "
     "interactive proof</b>, which is Module 10 &sect;1 and is how the "
     "subject got started."]],
   [0.23, 0.24, 0.53]),
  ("p", "<b>A problem in NP &cap; co-NP is unlikely to be "
        "NP-complete</b>, because if it were then every co-NP problem "
        "would reduce into NP and NP = co-NP would follow. <b>Which is "
        "why factoring's membership in NP &cap; co-NP is evidence that it "
        "is NP-intermediate</b> (Module 03 &sect;4) — <b>and it "
        "is a genuinely useful heuristic:</b> if your problem has short "
        "certificates in both directions, expect it to be in P or "
        "intermediate rather than complete, and look harder for a "
        "polynomial algorithm."),

  ("h1", "2 &nbsp; PSPACE"),
  ("callout", "PSPACE is polynomial space, and it contains the games",
   ["<b>PSPACE is the class of problems decidable using polynomial space "
    "and unbounded time.</b> <b>NP is contained in PSPACE</b>, because "
    "you can try every candidate certificate one at a time, reusing the "
    "same space — exponential time and polynomial space.",
    "<b>And TQBF — is a fully quantified Boolean formula true? "
    "— is PSPACE-complete.</b> <b>The difference from SAT is "
    "alternating quantifiers rather than a single block of "
    "existentials</b>, and that alternation is what the extra power buys "
    "you.",
    "<b>Which is exactly why two-player games are PSPACE-complete:</b> "
    "<b>'I have a move such that for all your replies I have a move such "
    "that&hellip;' is alternating quantification written out</b> "
    "— <b>and it is CSCE 625 Module 05 &sect;1's minimax, "
    "which is now revealed as the canonical PSPACE computation.</b>",
    "<b>Generalised geography, Go endgames, Reversi, and Hex are "
    "PSPACE-complete</b>, while <b>chess and Go generalised to "
    "n&times;n boards are EXPTIME-complete</b> — harder still, "
    "<b>because those games can last exponentially many moves</b>, so the "
    "space to record the position history is not polynomial. <b>The "
    "distinction between the two classes of game is the game length</b>, "
    "which is a satisfying thing for a complexity class to be tracking."]),
  ("code", """L  subset  NL  subset  P  subset  NP  subset  PH
   subset  PSPACE  subset  EXPTIME  subset  EXPSPACE

EVERY INCLUSION SHOWN IS KNOWN.
NOT ONE of the inclusions from P up to PSPACE is known to
be STRICT. P = PSPACE is not ruled out, though essentially
nobody believes it.

WHAT IS PROVED STRICT:
    P != EXPTIME        (time hierarchy, Module 07)
    NL != PSPACE        (space hierarchy)
    L != PSPACE

SO THE HIERARCHY THEOREMS GIVE SEPARATIONS ONLY WHEN THE
RESOURCE GAP IS LARGE -- exponential, not polynomial.
And P vs NP is a question about machines with the SAME
resource bound differing only in determinism, which is
exactly what those theorems cannot address (Module 07
section 4).

THE PRACTICAL READING: "PSPACE-complete" means harder than
NP-complete in all likelihood, and the solvers are
correspondingly worse. A PSPACE-complete problem is where
you should expect a solver to fail rather than to
surprise you."""),

  ("break",),
  ("h1", "3 &nbsp; The polynomial hierarchy"),
  ("callout", "The polynomial hierarchy is CSCE 627's arithmetic hierarchy "
              "with polynomial witnesses",
   ["<b>&Sigma;<sub>1</sub><super>p</super> is NP: there exists a short "
    "witness. &Pi;<sub>1</sub><super>p</super> is co-NP: for all short "
    "witnesses.</b>",
    "<b>&Sigma;<sub>2</sub><super>p</super> is 'there exists, then for "
    "all', and the alternation continues</b> — <b>exactly "
    "CSCE 627 Module 07 &sect;2's hierarchy with the quantifiers "
    "restricted to polynomial-length strings and the inner predicate "
    "required to be polynomial-time rather than merely decidable.</b> "
    "<b>Same construction, resource-bounded.</b>",
    "<b>Natural problems live at level 2:</b> <b>'is this the "
    "minimum-size circuit computing this function?' is 'there exists a "
    "smaller circuit such that for all inputs it agrees' — negated, "
    "so it is &Pi;<sub>2</sub><super>p</super></b>. <b>Which is why "
    "circuit minimisation is harder than SAT</b>, and why nobody expects "
    "a SAT solver to do it.",
    "<b>And the hierarchy is believed strict and is not known to "
    "be.</b> <b>If any two adjacent levels coincide, the entire "
    "hierarchy collapses to that level</b> — the proof is a "
    "straightforward induction — <b>so P = NP would collapse all of "
    "it to P</b>, which is one reason the consequences in Module 03 "
    "&sect;2 are so sweeping."]),
  ("ul", ["<b>Circuit minimisation.</b> "
          "<b>&Pi;<sub>2</sub><super>p</super></b> — see the "
          "callout.",
          "<b>Succinct set cover, and most 'is this the best X' "
          "questions.</b> <b>Optimality is systematically one quantifier "
          "above existence</b>, because 'best' means 'and nothing is "
          "better', which is a universal quantification over "
          "alternatives.",
          "<b>Two-player games with polynomially many moves.</b> "
          "<b>PSPACE-complete</b> — TQBF in disguise (&sect;2).",
          "<b>Games of exponential length</b> — chess and Go "
          "generalised. <b>EXPTIME-complete</b>, and hence provably not "
          "in P.",
          "<b>And model checking against full temporal logic</b>, which "
          "sits in PSPACE — <b>which is precisely why it is harder "
          "than SAT-based bounded model checking</b> (CSCE 627 "
          "Module 08 &sect;3), and why the bounded version is the one "
          "that scaled. <b>'Is this the best?' being one level harder "
          "than 'is there a good one?' is the most useful placing "
          "heuristic in this module</b>, and it explains a great deal "
          "about which problems solvers handle."]),

  ("h1", "4 &nbsp; What a collapse would mean"),
  ("callout", "A collapse would be a structural surprise, which is the "
              "evidence against it",
   ["<b>If NP = co-NP, then unsatisfiability would have short "
    "certificates</b> — and decades of proof-complexity work, which "
    "studies exactly the lengths of refutations in various proof systems, "
    "suggests strongly that it does not.",
    "<b>If the polynomial hierarchy collapses, then adding quantifier "
    "alternation buys no computational power</b> — and "
    "<b>CSCE 627 Module 07 showed that it does add power in the "
    "unbounded setting</b>, where the question is settled. <b>A "
    "resource-bounded version behaving entirely differently would be "
    "surprising.</b>",
    "<b>So the arguments are structural:</b> <b>a collapse would make a "
    "natural-looking distinction vanish, and the field treats that as "
    "evidence against the collapse.</b>",
    "<b>Which is weaker than proof, and is what is available.</b> <b>And "
    "the collapse results are used <i>as</i> evidence:</b> <b>'if X were "
    "true, the polynomial hierarchy would collapse' is a standard and "
    "accepted argument that X is false</b> — a conditional result "
    "deployed as a plausibility argument, which is how this field reasons "
    "in the absence of proof and is worth recognising as a style rather "
    "than mistaking for a theorem."]),
  ("callout", "The practical content of everything above NP",
   ["<b>NP-complete: solvers work, sometimes extremely well.</b> "
    "<b>Try one</b> (Module 04 &sect;4).",
    "<b>Above NP — &Sigma;<sub>2</sub><super>p</super> and "
    "beyond: expect solvers to struggle.</b> <b>QBF solvers exist and "
    "are substantially weaker than SAT solvers</b>, which is the "
    "practical trace of a separation nobody has proved, and is reasonable "
    "circumstantial evidence for it.",
    "<b>PSPACE-complete: a solver will probably not help</b>, and the "
    "engineering response is restriction, bounding, or approximation "
    "(CSCE 627 Module 12).",
    "<b>And the placing heuristic is quantifier alternation:</b> "
    "<b>write your problem's natural statement, count the quantifier "
    "alternations, and that is roughly where it sits</b> — <b>the "
    "same method as CSCE 627 Module 07 &sect;2</b>, and it takes a "
    "minute and is usually right."]),
 ],
 "resources": [
   ("Arora & Barak &mdash; chapters 4–5 (free draft)",
    "https://theory.cs.princeton.edu/complexity/",
    "<b>co-NP, PSPACE, and the polynomial hierarchy</b> — the "
    "reference for this module."),
   ("Sipser &mdash; chapter 8",
    "https://math.mit.edu/~sipser/book.html",
    "<b>PSPACE, TQBF, and the games</b>, with the generalised geography "
    "reduction worked in full."),
   ("Hearn & Demaine &mdash; Games, Puzzles, and Computation",
    "https://www.routledge.com/Games-Puzzles-and-Computation/Hearn-Demaine/p/book/9781568813226",
    "<b>&sect;2's games, systematically</b> — which puzzles are "
    "NP-complete, PSPACE-complete, or EXPTIME-complete, and why. Library "
    "copy."),
   ("Beame & Pitassi &mdash; Propositional Proof Complexity (free "
    "survey)",
    "https://www.cs.toronto.edu/~toni/Papers/survey.ps",
    "<b>&sect;4's first argument</b> — why short refutations are not "
    "expected, which is the main line of attack on NP versus co-NP."),
 ],
 "exercises": [
   "<b>Place five problems in NP, co-NP, or both</b>, naming the "
   "certificate in each direction.",
   "<b>Explain why a problem in NP ∩ co-NP is unlikely to be "
   "NP-complete.</b>",
   "<b>Get an unsatisfiability proof from a SAT solver</b> and report its "
   "size relative to the instance.",
   "<b>Show NP ⊆ PSPACE</b> by the space-reuse argument.",
   "<b>Reduce a two-player game to TQBF</b>, or sketch the "
   "correspondence.",
   "<b>Write the landscape from memory</b> and mark which separations are "
   "known.",
   "<b>Place three problems in the polynomial hierarchy</b> by counting "
   "quantifier alternations.",
   "<b>Take an optimisation problem and its decision version</b> and show "
   "the optimality question is one level higher.",
   "<b>Run a QBF solver and a SAT solver</b> on comparable instances and "
   "compare.",
   "<b>Find a published argument of the form 'X would collapse the "
   "hierarchy'</b> and assess it.",
 ],
 "selfcheck": [
   "Define co-NP and explain the asymmetry.",
   "What is the practical trace of co-NP in a SAT solver?",
   "Why is a problem in NP ∩ co-NP unlikely to be complete?",
   "Define PSPACE and explain why games live there.",
   "Why are chess and Go EXPTIME-complete rather than PSPACE-complete?",
   "Write the class landscape and say which separations are known.",
   "Why do the hierarchy theorems not settle P versus NP?",
   "Define the polynomial hierarchy and relate it to CSCE 627's.",
   "What happens if two adjacent levels coincide?",
   "Give the placing heuristic and the practical reading of each "
   "class.",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Space",
 "subtitle": "A different resource, with different theorems.",
 "question": "What changes when memory rather than time is the "
             "constraint?",
 "outcomes": [
     "Define L and NL and explain the input-tape convention.",
     "State Savitch's theorem and its consequence.",
     "Explain NL-completeness and log-space reductions.",
     "Explain Immerman–Szelepcsényi and why it is "
     "surprising.",
     "Explain the parallel connection and NC.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Logarithmic space",
   "blurb": "And why the convention matters."},

  {"t": "callout", "title": "Log space means log <i>working</i> space, with the input read-only",
   "kind": "The convention, and it is not arbitrary",
   "body": ["<b>The input occupies n cells, so charging for it would "
            "make sublinear space impossible.</b> So the model gives a "
            "read-only input tape and charges only for the work tape.",
            "<b>With that convention, L is the problems solvable in "
            "O(log n) work space</b> — enough for a constant number "
            "of pointers into the input, and nothing more.",
            "<b>Which is a natural and practically meaningful "
            "class:</b> <b>a log-space algorithm is a streaming or "
            "pointer-chasing algorithm</b>, and the restriction matches "
            "real constraints.",
            "<b>And NL is the non-deterministic version</b>, whose "
            "canonical problem is <b>s-t connectivity in a directed "
            "graph</b> — guess the path one vertex at a time, "
            "remembering only where you are."]},

  {"t": "table", "kicker": "Space classes", "title": "What fits in each",
   "header": ["Class", "Means", "Canonical problem"],
   "widths": [2.3, 4.2, 5.5],
   "rows": [
     ["<b>L</b>", "<b>O(log n) work space, deterministic</b>", "<b>Undirected s-t connectivity (Reingold, 2004)</b>"],
     ["<b>NL</b>", "<b>O(log n), non-deterministic</b>", "<b>Directed s-t connectivity</b>"],
     ["<b>PSPACE</b>", "<b>Polynomial space</b>", "<b>TQBF (M05 §2)</b>"],
     ["<b>L ⊆ NL ⊆ P</b>", "<b>All known; none known strict</b>", "<b>The same situation as everywhere else</b>"],
   ],
   "footnote": "<b>Undirected connectivity in L was open for decades "
               "and was solved in 2004</b> — the directed version "
               "is NL-complete and is not expected to be in L.",
   "note": "The directed/undirected gap is a satisfying concrete "
           "separation question."},

  {"t": "section", "label": "Part 2", "title": "Savitch",
   "blurb": "Non-determinism costs little in space."},

  {"t": "callout", "title": "Savitch: non-deterministic space is at most squared",
   "kind": "The theorem, and why it surprises",
   "body": ["<b>NSPACE(f) ⊆ SPACE(f²).</b> So "
            "<b>PSPACE = NPSPACE</b>, and non-determinism buys nothing "
            "at polynomial space.",
            "<b>Contrast time, where the best known simulation of "
            "non-determinism is exponential</b> — and whether it can "
            "be polynomial is P versus NP.",
            "<b>The proof is a recursive reachability test:</b> can "
            "configuration A reach B in 2ᵏ steps? Try every "
            "midpoint, recursing. <b>Depth k, each level storing one "
            "configuration.</b>",
            "<b>And space is reusable in a way time is not</b>, which "
            "is the whole reason: <b>the recursion reuses the same cells "
            "at every branch, and you cannot reuse elapsed time.</b>"]},

  {"t": "callout", "title": "Immerman–Szelepcsényi: NL is closed under complement",
   "kind": "Which is genuinely surprising",
   "body": ["<b>NL = co-NL.</b> <b>So directed s-t "
            "<i>non</i>-connectivity is also in NL</b>, which has no "
            "obvious certificate.",
            "<b>The technique is inductive counting:</b> count "
            "reachable vertices at each distance, non-deterministically "
            "and verifiably — and if the count is right, you can "
            "certify that a vertex is <i>not</i> reachable.",
            "<b>And this is exactly where the space analogue of NP "
            "versus co-NP goes the other way</b> "
            "(Module 05 §1): <b>settled, and settled in the "
            "surprising direction.</b>",
            "<b>Which is a useful corrective:</b> <b>the analogy "
            "between time and space classes fails at the two most "
            "interesting points</b> — Savitch and "
            "Immerman–Szelepcsényi — so arguing from one "
            "to the other is unreliable."]},

  {"t": "section", "label": "Part 3", "title": "Reductions and completeness",
   "blurb": "A finer notion, for a finer class."},

  {"t": "callout", "title": "Log-space reductions, because polynomial ones are too coarse",
   "kind": "Why the notion changes",
   "body": ["<b>Polynomial-time reductions are useless for "
            "distinguishing within P</b> — every problem in P reduces "
            "to every other in polynomial time, trivially.",
            "<b>So the reduction must be weaker than the class it "
            "studies.</b> <b>Log-space reductions are the right notion "
            "for L, NL, and P-completeness.</b>",
            "<b>And they compose</b>, which requires care: you cannot "
            "store the intermediate result, so the composition "
            "recomputes it on demand. <b>The proof is not "
            "trivial.</b>",
            "<b>P-completeness under log-space reductions is the "
            "important application:</b> <b>a P-complete problem is one "
            "that probably does not parallelise</b>, which is Part 4 and "
            "is the practically useful part."]},

  {"t": "section", "label": "Part 4", "title": "Parallelism",
   "blurb": "The class that matters for CSCE 735."},

  {"t": "callout", "title": "NC is the parallel-tractable class, and P-completeness is evidence against parallelising",
   "kind": "The practical payoff of space complexity",
   "body": ["<b>NC is the problems solvable in polylogarithmic time "
            "with polynomially many processors</b> — 'efficiently "
            "parallelisable', formalised.",
            "<b>NC ⊆ P, and whether NC = P is open</b> — "
            "<b>the parallel analogue of P versus NP</b>, and believed "
            "false for the same kinds of reason.",
            "<b>So a P-complete problem is one that probably does not "
            "parallelise</b> — <b>circuit value, linear programming, "
            "and depth-first search ordering are P-complete</b>, and all "
            "three resist parallelisation in practice.",
            "<b>Which is the practically useful content of this "
            "module</b> (CSCE 735): <b>if your problem is P-complete, "
            "the difficulty you are having parallelising it is "
            "structural</b>, and the response is a different algorithm "
            "rather than more effort."]},

  {"t": "bullets", "kicker": "Summary", "title": "What space complexity gives you",
   "items": [
     "<b>Savitch: non-determinism costs at most a square in space</b>, "
     "so PSPACE = NPSPACE — and the time analogue is open.",
     "",
     "<b>Immerman–Szelepcsényi: NL = co-NL</b>, which has no "
     "time analogue and is surprising.",
     "",
     "<b>So the time/space analogy fails exactly where it would be "
     "most useful</b>, and arguing across it is unreliable.",
     "",
     "<b>Log-space reductions are needed to distinguish inside P</b>, "
     "because a reduction must be weaker than what it classifies.",
     "",
     "<b>And P-completeness is a practical warning about "
     "parallelisation</b> — the one result in this module you will "
     "use.",
   ],
   "footnote": "<b>'Is it P-complete?' is worth asking before "
               "investing in parallelising anything</b>, and it takes an "
               "hour against a catalogue."},
 ],
 "takeaways": [
   "Log space means log working space with a read-only input tape, which "
   "is what makes sublinear space classes possible at all.",
   "Savitch's theorem gives PSPACE = NPSPACE, so non-determinism buys "
   "nothing in space — because space is reusable and elapsed time is "
   "not.",
   "Immerman–Szelepcsényi gives NL = co-NL, which is surprising "
   "and has no known time analogue.",
   "So the time/space analogy fails at exactly the two most interesting "
   "points, which makes arguing across it unreliable.",
   "Log-space reductions are needed to distinguish inside P, because a "
   "reduction must be weaker than the class it classifies.",
   "P-completeness is evidence a problem does not parallelise, which is "
   "the one result here you will use.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Logarithmic space"),
  ("callout", "Log space means log <i>working</i> space, with the input "
              "read-only",
   ["<b>The input occupies n cells, so charging for it would make any "
    "sublinear space class empty.</b> So the model is adjusted: a "
    "read-only input tape that is not charged, and a separate read-write "
    "work tape that is.",
    "<b>With that convention, L is the class of problems solvable in "
    "O(log n) work space</b> — which is enough for a constant number "
    "of pointers into the input, a few counters, and nothing else. "
    "<b>You cannot store a list, a set, or a copy of anything.</b>",
    "<b>Which makes it a natural and practically meaningful class:</b> "
    "<b>a log-space algorithm is a streaming or pointer-chasing "
    "algorithm</b>, and the restriction corresponds to a real engineering "
    "constraint (processing data larger than memory, or a "
    "constant-memory embedded routine).",
    "<b>And NL is the non-deterministic version</b>, whose canonical "
    "problem is <b>s-t connectivity in a <i>directed</i> graph</b> "
    "— <b>guess the path one vertex at a time, remembering only the "
    "current vertex and a step counter</b>, which is log space. <b>The "
    "certificate is the path and it is too long to store, which is why "
    "non-determinism helps here.</b>"]),
  ("table", ["Class", "What it means", "Canonical problem"],
   [["<b>L</b>", "<b>O(log n) work space, deterministic.</b>",
     "<b>Undirected s-t connectivity</b> — which Reingold proved in "
     "L in 2004, after decades open."],
    ["<b>NL</b>", "<b>O(log n) work space, non-deterministic.</b>",
     "<b>Directed s-t connectivity</b>, which is NL-complete."],
    ["<b>PSPACE</b>", "<b>Polynomial space.</b>",
     "<b>TQBF</b> (Module 05 &sect;2)."],
    ["<b>L &sube; NL &sube; P</b>",
     "<b>All inclusions known; none known to be strict.</b>",
     "<b>The same situation as everywhere else in this course</b> "
     "(Module 05 &sect;2's landscape)."]],
   [0.19, 0.34, 0.47]),
  ("p", "<b>Undirected connectivity being in L was open for decades and "
        "was settled in 2004</b> by a randomness-free construction using "
        "expander graphs — <b>while the directed version is "
        "NL-complete and is not expected to be in L.</b> <b>The gap "
        "between directed and undirected is a satisfyingly concrete form "
        "of a separation question</b>, and the undirected result is one of "
        "the genuine recent successes in the field."),

  ("h1", "2 &nbsp; Savitch and Immerman–Szelepcsényi"),
  ("callout", "Savitch: non-deterministic space is at most squared",
   ["<b>NSPACE(f) is contained in SPACE(f&#178;).</b> So <b>PSPACE = "
    "NPSPACE</b>, and <b>non-determinism buys nothing at all at "
    "polynomial space</b>.",
    "<b>Contrast time, where the best known deterministic simulation of "
    "a non-deterministic machine is exponential</b> — and whether it "
    "can be made polynomial is exactly P versus NP. <b>So the two "
    "resources behave completely differently on the question that defines "
    "the field.</b>",
    "<b>The proof is a recursive reachability test:</b> can "
    "configuration A reach configuration B within 2<super>k</super> "
    "steps? Try every possible midpoint M, and recursively ask whether A "
    "reaches M and M reaches B in 2<super>k&minus;1</super> steps. "
    "<b>Recursion depth k, with one configuration stored per level.</b>",
    "<b>And space is reusable in a way that time is not</b>, which is "
    "the whole reason the theorem holds: <b>the recursion reuses the same "
    "memory cells across every branch it explores, and you cannot reuse "
    "elapsed time.</b> <b>That asymmetry between the two resources is "
    "the most important intuition in this module</b>, and it explains "
    "both of its theorems."]),
  ("callout", "Immerman–Szelepcsényi: NL is closed under "
              "complement",
   ["<b>NL = co-NL.</b> <b>So directed s-t <i>non</i>-connectivity is "
    "also in NL</b> — which is startling, because there is no "
    "obvious certificate for 't is not reachable from s' that fits in "
    "logarithmic space.",
    "<b>The technique is inductive counting:</b> non-deterministically "
    "compute the <i>number</i> of vertices reachable within i steps, for "
    "each i, in a way that can be verified — <b>and once you know "
    "the exact count, you can certify that a particular vertex is not "
    "among them</b>, by exhibiting the others.",
    "<b>And this is exactly where the space analogue of the NP versus "
    "co-NP question goes the other way</b> (Module 05 &sect;1): "
    "<b>settled, and settled in the direction nobody would have "
    "guessed.</b>",
    "<b>Which is a useful corrective:</b> <b>the analogy between time "
    "and space classes fails at the two most interesting points</b> "
    "— Savitch (where space collapses non-determinism and time is "
    "not known to) and Immerman–Szelepcs&eacute;nyi (where space "
    "closes under complement and time is not known to) — <b>so "
    "arguing from one resource to the other is unreliable</b>, and "
    "intuitions about P versus NP drawn from space results should be "
    "distrusted."]),

  ("break",),
  ("h1", "3 &nbsp; Log-space reductions"),
  ("callout", "Log-space reductions, because polynomial ones are too coarse",
   ["<b>Polynomial-time reductions are useless for distinguishing within "
    "P</b> — every problem in P reduces to every other problem in P "
    "in polynomial time, by simply solving it. <b>So the notion collapses "
    "exactly where you wanted to use it.</b>",
    "<b>So the reduction must be weaker than the class it studies.</b> "
    "<b>Log-space reductions are the right notion for L, NL, and "
    "P-completeness</b> — which is a general principle worth "
    "extracting: <b>a reduction is only informative if it is weaker than "
    "the distinction it is being used to draw.</b>",
    "<b>And they compose, which requires care.</b> <b>You cannot store "
    "the intermediate result</b> — it may be polynomially long and "
    "you have logarithmic space — <b>so the composition recomputes "
    "each needed bit of it on demand</b>, re-running the first reduction "
    "from scratch for every bit the second one reads. <b>The proof is not "
    "trivial</b>, and it is a good illustration of what log space forces "
    "you to do.",
    "<b>P-completeness under log-space reductions is the important "
    "application:</b> <b>a P-complete problem is one that probably does "
    "not parallelise</b>, which is &sect;4 and is the practically useful "
    "part of the module."]),

  ("h1", "4 &nbsp; Parallelism"),
  ("callout", "NC is the parallel-tractable class, and P-completeness is "
              "evidence against parallelising",
   ["<b>NC is the class of problems solvable in polylogarithmic time "
    "using polynomially many processors</b> — 'efficiently "
    "parallelisable', formalised. <b>Equivalently, problems with "
    "polylogarithmic-depth, polynomial-size circuits</b> "
    "(Module 09).",
    "<b>NC is contained in P, and whether NC = P is open</b> — "
    "<b>the parallel analogue of P versus NP</b>, believed false for "
    "broadly similar reasons and with correspondingly similar barriers to "
    "proof.",
    "<b>So a P-complete problem is one that probably does not "
    "parallelise.</b> <b>The circuit value problem, linear programming, "
    "and computing the lexicographically first depth-first search "
    "ordering are all P-complete</b> — <b>and all three resist "
    "parallelisation in practice</b>, which is reasonable circumstantial "
    "support.",
    "<b>Which is the practically useful content of this module</b>, and "
    "it is the part relevant to CSCE 735: <b>if your problem is "
    "P-complete, the difficulty you are having parallelising it is "
    "structural rather than a failure of effort</b>, <b>and the response "
    "is a different algorithm or a relaxed requirement rather than more "
    "engineering.</b> <b>'Is it P-complete?' is worth asking before "
    "investing in parallelising anything</b>, and checking against a "
    "catalogue takes an hour."]),
  ("ul", ["<b>Savitch: non-determinism costs at most a squaring in "
          "space</b>, so PSPACE = NPSPACE — <b>and the time "
          "analogue is the open question that defines the field.</b>",
          "<b>Immerman–Szelepcs&eacute;nyi: NL = co-NL</b>, which "
          "has no known time analogue and is genuinely surprising.",
          "<b>So the time/space analogy fails exactly where it would be "
          "most useful</b>, and reasoning across it is unreliable "
          "(&sect;2).",
          "<b>Log-space reductions are needed to distinguish inside P</b> "
          "— <b>because a reduction must be weaker than what it "
          "classifies</b>, which is a transferable principle.",
          "<b>And P-completeness is a practical warning about "
          "parallelisation</b> — <b>the one result in this module "
          "you will actually use</b>, and the reason space complexity "
          "deserves a module in a program with CSCE 735 in it."]),
 ],
 "resources": [
   ("Arora & Barak &mdash; chapter 4 (free draft)",
    "https://theory.cs.princeton.edu/complexity/",
    "<b>Space classes, Savitch, and "
    "Immerman–Szelepcsényi</b>, with both proofs."),
   ("Sipser &mdash; chapter 8",
    "https://math.mit.edu/~sipser/book.html",
    "<b>The same material more slowly</b>, and the input-tape convention "
    "of &sect;1 explained carefully."),
   ("Reingold &mdash; Undirected Connectivity in Log-Space (free)",
    "https://dl.acm.org/doi/10.1145/1391289.1391291",
    "<b>&sect;1's 2004 result</b>, which is a genuine recent success and "
    "uses expander graphs in a surprising way."),
   ("Greenlaw, Hoover & Ruzzo &mdash; Limits to Parallel Computation "
    "(free)",
    "https://homes.cs.washington.edu/~ruzzo/papers/limits.pdf",
    "<b>&sect;4's catalogue of P-complete problems, free in full</b> "
    "— the reference to check before parallelising anything."),
 ],
 "exercises": [
   "<b>Write a log-space algorithm</b> for a problem of your choosing and "
   "verify the space bound.",
   "<b>Explain why charging for the input tape would empty L.</b>",
   "<b>Implement directed s-t connectivity non-deterministically</b> and "
   "confirm the space usage is logarithmic.",
   "<b>Work through Savitch's recursion</b> and compute the space at each "
   "depth.",
   "<b>Explain why the same argument fails for time.</b>",
   "<b>Read the inductive counting argument</b> and summarise why it "
   "certifies non-reachability.",
   "<b>Show that polynomial-time reductions cannot distinguish within "
   "P.</b>",
   "<b>Explain how log-space reductions compose without storing the "
   "intermediate.</b>",
   "<b>Look up three P-complete problems</b> and check whether you have "
   "tried to parallelise any of them.",
   "<b>Take a problem you parallelised successfully</b> and find where it "
   "sits relative to NC.",
 ],
 "selfcheck": [
   "Why is the input tape not charged, and what would happen "
   "otherwise?",
   "Define L and NL and give the canonical problem for each.",
   "State Savitch's theorem and its consequence.",
   "Why does space collapse non-determinism when time is not known to?",
   "State Immerman–Szelepcsényi and say why it surprises.",
   "Where does the time/space analogy fail, and what follows?",
   "Why are log-space reductions needed, and what is the general "
   "principle?",
   "Define NC and state the open question.",
   "What does P-completeness tell you practically?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Hierarchies and Barriers",
 "subtitle": "What more resources buy, and why the method stops working.",
 "question": "Can you prove that more time helps? And why does that not "
             "settle P versus NP?",
 "outcomes": [
     "Prove the time hierarchy theorem.",
     "State the space hierarchy theorem and compare.",
     "Explain why hierarchy theorems do not separate P from NP.",
     "Explain relativisation and the Baker–Gill–Solovay "
     "result.",
     "Explain what a barrier result is and why it counts as "
     "progress.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "More time helps",
   "blurb": "Proved, by diagonalisation."},

  {"t": "code", "kicker": "Time hierarchy", "title": "The proof, which you have seen before",
   "lang": "text", "code": """
  CLAIM: there is a language decidable in time n^3 and not
  in time n^2. More time buys strictly more power.

  THE PROOF is Module 05 of CSCE 627, with a clock.

  Define D(M):               # M is a machine encoding
      simulate M on input M for n^2.5 steps
      if it halts and accepts, REJECT
      otherwise, ACCEPT

  D runs in about n^3 (simulation overhead is logarithmic).

  Suppose some machine M0 decides D's language in n^2.
  Run D on M0's own encoding. The simulation COMPLETES,
  because n^2 < n^2.5. So D does the opposite of M0.
  But D's language is M0's language. CONTRADICTION.

  SO: TIME(n^2) is strictly inside TIME(n^3).

  THE TWO INGREDIENTS
      DIAGONALISATION -- do the opposite of what the
          enumerated machine does (CSCE 627 Module 05)
      A CLOCK -- the simulation must be cut off, which is
          what makes this a complexity result rather than
          a computability one
""",
   "caption": "<b>Same technique as the halting problem, with a "
              "clock</b> — and <b>the space hierarchy is the same "
              "argument and tighter</b>, because space simulation has no "
              "overhead.",
   "note": "The clock is the whole difference; make it explicit."},

  {"t": "callout", "title": "What the hierarchy theorems give, and what they do not",
   "kind": "The scope",
   "body": ["<b>They give: P ≠ EXPTIME, NL ≠ PSPACE, "
            "and a strict hierarchy within each resource</b> "
            "(Module 05 §2).",
            "<b>So they do separate classes</b>, and that is more than "
            "the field manages elsewhere.",
            "<b>But only when the resource gap is large.</b> <b>The "
            "simulation overhead means you need more than a constant "
            "factor</b>, and the technique compares a resource bound "
            "against a larger one.",
            "<b>And P versus NP is not of that shape.</b> <b>It "
            "compares deterministic and non-deterministic polynomial "
            "time — the same resource bound, different machine "
            "mode</b> — <b>which diagonalisation has no handle on, "
            "and Part 2 explains why formally.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Relativisation",
   "blurb": "The first barrier, and it is a theorem."},

  {"t": "callout", "title": "Baker–Gill–Solovay: oracles go both ways, so diagonalisation cannot settle it",
   "kind": "The first barrier result",
   "body": ["<b>There is an oracle A with "
            "P^A = NP^A, and an oracle B with "
            "P^B ≠ NP^B.</b> Both constructed "
            "explicitly.",
            "<b>And diagonalisation arguments <i>relativise</i></b> "
            "— they go through unchanged when every machine has an "
            "oracle (CSCE 627 §07 §1 showed the halting "
            "proof does).",
            "<b>So no relativising proof can settle P versus NP</b>, "
            "because any such proof would hold for every oracle, and the "
            "answer differs between oracles.",
            "<b>Which rules out the entire technique that produced "
            "every separation in Part 1.</b> <b>That is a precise, "
            "proved statement about the inadequacy of the field's main "
            "tool</b>, and it is from 1975."]},

  {"t": "table", "kicker": "Barriers", "title": "The three barrier results",
   "header": ["Barrier", "Rules out", "Year"],
   "widths": [2.8, 5.8, 2.4],
   "rows": [
     ["<b>Relativisation</b>", "<b>Any proof that works with oracles — i.e. diagonalisation</b>", "<b>1975</b>"],
     ["<b>Natural proofs</b>", "<b>Combinatorial circuit lower bounds of the usual kind (M09)</b>", "<b>1994</b>"],
     ["<b>Algebrisation</b>", "<b>Algebraic extensions of relativising techniques, including IP=PSPACE's method</b>", "<b>2008</b>"],
   ],
   "footnote": "<b>Each barrier followed a period of optimism about a "
               "technique</b> — and the third was constructed "
               "specifically because arithmetisation (M10) had evaded the "
               "first.",
   "note": "The history is the point: each barrier closed off a "
           "promising route."},

  {"t": "section", "label": "Part 3", "title": "Non-relativising results",
   "blurb": "What does get past the first barrier."},

  {"t": "callout", "title": "Some results do not relativise, which is why there is hope",
   "kind": "The escape",
   "body": ["<b>IP = PSPACE</b> (Module 10) <b>does not "
            "relativise</b> — there are oracles making it false. "
            "<b>So non-relativising techniques exist and have proved real "
            "theorems.</b>",
            "<b>The technique is arithmetisation:</b> convert a Boolean "
            "formula into a polynomial over a field, and exploit "
            "properties of polynomials that have no oracle analogue.",
            "<b>Which is why the algebrisation barrier was "
            "constructed</b> — to determine whether arithmetisation "
            "alone could reach P versus NP. <b>It cannot.</b>",
            "<b>So the state of play is:</b> <b>three barriers, each "
            "closing a technique, and the open question is what a "
            "technique evading all three would look like.</b> <b>Nobody "
            "knows, and that is the honest summary.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Barriers as progress",
   "blurb": "Why this is not just failure."},

  {"t": "bullets", "kicker": "Barriers", "title": "Why a barrier result is a genuine contribution",
   "items": [
     "<b>It redirects effort.</b> <b>After 1975, nobody serious "
     "attempted a relativising proof of P ≠ NP</b> — which "
     "saved a great deal of time.",
     "",
     "<b>It is a theorem about proofs</b>, which is an unusual and "
     "respectable kind of result — and it is CSCE 627's "
     "undecidability argument applied to a methodology.",
     "",
     "<b>It specifies what a solution must look like</b>: "
     "non-relativising, non-naturalising, non-algebrising. <b>Three "
     "constraints is more guidance than none.</b>",
     "",
     "<b>And each barrier was proved by constructing a "
     "counterexample</b>, which required real technique and produced "
     "other results.",
     "",
     "<b>Which is the field's own honest assessment:</b> <b>fifty "
     "years of not proving it, and three theorems explaining why.</b>",
   ],
   "footnote": "<b>Few fields can point to proofs that their own "
               "methods are inadequate</b>, and treating that as "
               "intellectual honesty rather than failure is the right "
               "reading."},

  {"t": "callout", "title": "What to take from this module",
   "kind": "Closing",
   "body": ["<b>More resources provably help, when the gap is "
            "large.</b> <b>That is the positive result, and it is "
            "proved by the technique of CSCE 627 §05 plus a "
            "clock.</b>",
            "<b>And the same technique provably cannot settle P versus "
            "NP</b>, which is a sharper statement than 'nobody has "
            "managed it'.",
            "<b>Two further barriers close two further techniques</b> "
            "(Module 09 §3, and the algebrisation result).",
            "<b>So the honest position is: the question is open, the "
            "belief is empirical</b> (Module 03 §3), <b>and "
            "the field has mapped out three dead ends rigorously.</b> "
            "<b>Which is a form of progress, and is what is "
            "available.</b>"]},
 ],
 "takeaways": [
   "The time hierarchy theorem is CSCE 627's diagonalisation plus a "
   "clock, and the clock is what makes it a complexity result.",
   "The space hierarchy is tighter because space simulation has no "
   "overhead, so even a log factor more space buys power.",
   "Hierarchy theorems separate classes only when the resource gap is "
   "large, and P versus NP compares the same bound with different "
   "determinism.",
   "Baker–Gill–Solovay constructed oracles going both ways, so "
   "no relativising proof can settle P versus NP — which rules out "
   "diagonalisation.",
   "Arithmetisation does not relativise and proved IP = PSPACE, which is "
   "why the algebrisation barrier was then constructed.",
   "A barrier result redirects effort, is a theorem about proofs, and "
   "specifies what a solution must look like — which is genuine "
   "progress.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The hierarchy theorems"),
  ("code", """CLAIM: there is a language decidable in time n^3 and not in
time n^2. More time buys strictly more power.

THE PROOF is CSCE 627 Module 05, with a clock added.

Define D(M):                 # M is a machine encoding
    simulate M on input M for n^2.5 steps
    if it halts and accepts, REJECT
    otherwise, ACCEPT

D runs in about n^3 (the simulation overhead is
logarithmic, which is why the exponents have room).

Suppose some machine M0 decides D's language in time n^2.
Run D on M0's own encoding. The simulation COMPLETES,
because n^2 < n^2.5. So D does the opposite of M0 on that
input. But D's language is supposed to BE M0's language.
CONTRADICTION.

SO: TIME(n^2) is strictly contained in TIME(n^3).

THE TWO INGREDIENTS
    DIAGONALISATION -- do the opposite of what the
        enumerated machine does (CSCE 627 Module 05)
    A CLOCK -- the simulation must be cut off, and that
        cut-off is what makes this a COMPLEXITY result
        rather than a computability one

THE SPACE HIERARCHY is the same argument and is TIGHTER,
because space simulation has no overhead at all -- so even
a logarithmic factor more space buys strictly more power."""),
  ("callout", "What the hierarchy theorems give, and what they do not",
   ["<b>They give: P &ne; EXPTIME, NL &ne; PSPACE, L &ne; PSPACE, and a "
    "strict infinite hierarchy within each resource</b> (Module 05 "
    "&sect;2's landscape, where these are the only proved "
    "separations).",
    "<b>So they do separate complexity classes</b>, which is more than "
    "the field manages anywhere else — and it is worth noting that "
    "the separations we have are all from this one technique.",
    "<b>But only when the resource gap is large.</b> <b>The simulation "
    "overhead means you need more than a constant factor</b>, and more "
    "fundamentally <b>the technique works by comparing a resource bound "
    "against a strictly larger one of the same kind.</b>",
    "<b>And P versus NP is not of that shape.</b> <b>It compares "
    "deterministic and non-deterministic polynomial time — the same "
    "resource bound, differing only in the machine's mode</b> — "
    "<b>which diagonalisation has no handle on, because there is no "
    "larger bound to diagonalise into.</b> <b>&sect;2 makes that "
    "intuition into a theorem.</b>"]),

  ("h1", "2 &nbsp; Relativisation"),
  ("callout", "Baker–Gill–Solovay: oracles go both ways, so "
              "diagonalisation cannot settle it",
   ["<b>There is an oracle A for which P<super>A</super> = "
    "NP<super>A</super>, and an oracle B for which P<super>B</super> &ne; "
    "NP<super>B</super>.</b> <b>Both are constructed explicitly</b> "
    "— A can be taken to be any PSPACE-complete problem, and B is "
    "built by a diagonalisation.",
    "<b>And diagonalisation arguments <i>relativise</i></b> — they "
    "go through entirely unchanged when every machine in the argument is "
    "given the same oracle, because the argument never inspects what the "
    "machines do internally. <b>CSCE 627 Module 07 &sect;1 observed "
    "exactly this for the halting proof.</b>",
    "<b>So no relativising proof can settle P versus NP</b>: any such "
    "proof would establish the same answer relative to every oracle, and "
    "the answer demonstrably differs between A and B. <b>The technique is "
    "not merely insufficient; it is provably incapable.</b>",
    "<b>Which rules out the entire technique that produced every "
    "separation in &sect;1.</b> <b>That is a precise, proved statement "
    "about the inadequacy of the field's main tool</b>, <b>and it is from "
    "1975</b> — four years after the question was posed, which is "
    "part of why the field's attitude to it is as it is."]),
  ("table", ["Barrier", "What it rules out", "Year"],
   [["<b>Relativisation</b> (Baker, Gill, Solovay)",
     "<b>Any proof technique that works unchanged in the presence of an "
     "oracle — which includes diagonalisation and simulation</b>.",
     "<b>1975</b>"],
    ["<b>Natural proofs</b> (Razborov, Rudich)",
     "<b>Combinatorial circuit lower bound arguments of the kind that had "
     "been succeeding on restricted models</b> (Module 09 &sect;3), "
     "<b>assuming strong one-way functions exist.</b>",
     "<b>1994</b>"],
    ["<b>Algebrisation</b> (Aaronson, Wigderson)",
     "<b>Algebraic extensions of relativising techniques, including the "
     "arithmetisation method that had evaded the first barrier and proved "
     "IP = PSPACE</b> (&sect;3).",
     "<b>2008</b>"]],
   [0.26, 0.56, 0.18]),
  ("p", "<b>Each barrier followed a period of optimism about a "
        "technique</b> — and <b>the third was constructed "
        "specifically to determine whether arithmetisation, which had "
        "evaded the first barrier, could reach P versus NP.</b> <b>The "
        "history is the point:</b> each barrier closed off a route that "
        "serious people were pursuing, which is what makes them "
        "contributions rather than discouragements."),

  ("break",),
  ("h1", "3 &nbsp; What gets past the first barrier"),
  ("callout", "Some results do not relativise, which is why there is hope",
   ["<b>IP = PSPACE</b> (Module 10 &sect;2) <b>does not "
    "relativise</b> — there are oracles relative to which it is "
    "false. <b>So non-relativising techniques exist, and they have proved "
    "real and substantial theorems.</b> This was the news of the early "
    "1990s.",
    "<b>The technique is arithmetisation:</b> convert a Boolean formula "
    "into a polynomial over a finite field, and then exploit properties of "
    "low-degree polynomials — that they are determined by few "
    "points, that two distinct ones disagree almost everywhere — "
    "<b>which have no oracle analogue, because an oracle is an arbitrary "
    "function and polynomials are not.</b>",
    "<b>Which is precisely why the algebrisation barrier was "
    "constructed</b> — to determine whether arithmetisation alone "
    "could reach P versus NP. <b>It cannot</b>, and the proof constructs "
    "algebraic oracles going both ways, in the same shape as "
    "Baker–Gill–Solovay.",
    "<b>So the state of play is:</b> <b>three barriers, each closing a "
    "technique, and the open question is what a technique evading all "
    "three would even look like.</b> <b>Nobody knows, and that is the "
    "honest summary</b> — geometric complexity theory is the most "
    "developed proposal and has produced no separation."]),

  ("h1", "4 &nbsp; Barriers as progress"),
  ("ul", ["<b>It redirects effort.</b> <b>After 1975, no serious "
          "researcher attempted a relativising proof of P &ne; NP</b> "
          "— which saved a great deal of time and is exactly "
          "CSCE 627 Module 06 &sect;4's argument about proving "
          "impossibility early, one level up.",
          "<b>It is a theorem about proofs</b>, which is an unusual and "
          "respectable kind of result — <b>and it is "
          "CSCE 627's undecidability argument applied to a "
          "methodology</b> rather than to a problem.",
          "<b>It specifies what a solution must look like:</b> "
          "non-relativising, non-naturalising, and non-algebrising. "
          "<b>Three constraints is considerably more guidance than "
          "none</b>, and any claimed proof can be checked against them "
          "immediately — which is how most claimed proofs are "
          "dismissed.",
          "<b>And each barrier was proved by constructing an explicit "
          "counterexample</b>, which required genuine technique and "
          "produced other results along the way — the "
          "Baker–Gill–Solovay construction is a useful "
          "diagonalisation in its own right.",
          "<b>Which is the field's own honest assessment of its "
          "position:</b> <b>fifty years of not proving the central "
          "result, and three theorems explaining why the available "
          "methods cannot.</b> <b>Few fields can point to proofs that "
          "their own methods are inadequate</b>, and <b>treating that as "
          "intellectual honesty rather than as failure is the right "
          "reading.</b>"]),
  ("callout", "What to take from this module",
   ["<b>More resources provably help, when the gap is large.</b> "
    "<b>That is the positive result</b>, and it is proved by "
    "CSCE 627 Module 05's technique plus a clock — which is a "
    "satisfying reuse.",
    "<b>And the same technique provably cannot settle P versus NP</b>, "
    "which is <b>a sharper and more useful statement than 'nobody has "
    "managed it'.</b>",
    "<b>Two further barriers close two further techniques</b> "
    "(Module 09 &sect;3's natural proofs, and the 2008 algebrisation "
    "result) — so the closure is not a single historical accident.",
    "<b>So the honest position is: the question is open, the belief is "
    "empirical</b> (Module 03 &sect;3), <b>and the field has mapped out "
    "three dead ends rigorously.</b> <b>Which is a form of progress, and "
    "it is what is available</b> — and a course that presented the "
    "consensus without the barriers would be giving a false impression of "
    "how much is known."]),
 ],
 "resources": [
   ("Arora & Barak &mdash; chapters 3 and 23 (free draft)",
    "https://theory.cs.princeton.edu/complexity/",
    "<b>The hierarchy theorems and all three barriers</b> — "
    "chapter 23 is the best treatment of the barriers available."),
   ("Baker, Gill & Solovay &mdash; Relativizations of the P =? NP "
    "Question (free)",
    "https://epubs.siam.org/doi/10.1137/0204037",
    "<b>&sect;2's result</b>, and both oracle constructions."),
   ("Aaronson & Wigderson &mdash; Algebrization: A New Barrier in "
    "Complexity Theory (free)",
    "https://www.scottaaronson.com/papers/alg.pdf",
    "<b>&sect;2's third barrier</b>, with a good account of why it was "
    "needed."),
   ("Aaronson &mdash; P =? NP, the barriers section (free)",
    "https://www.scottaaronson.com/papers/pnp.pdf",
    "<b>All three barriers assessed together</b>, with a candid view of "
    "what remains."),
 ],
 "exercises": [
   "<b>Prove the time hierarchy theorem</b> in your own words, and "
   "identify where the clock enters.",
   "<b>Explain why the space hierarchy is tighter.</b>",
   "<b>Work out which separations in Module 05's landscape come from "
   "hierarchy theorems</b> and which are unproved.",
   "<b>Explain why diagonalisation relativises</b>, by checking the "
   "hierarchy proof step by step with oracles added.",
   "<b>State Baker–Gill–Solovay</b> and explain why it rules "
   "out a technique rather than an answer.",
   "<b>Verify that a PSPACE-complete oracle makes P = NP relative to "
   "it.</b>",
   "<b>Read about arithmetisation</b> and say why it does not "
   "relativise.",
   "<b>Find a claimed proof of P ≠ NP online</b> and check it "
   "against the three barriers.",
   "<b>Write an argument for why barrier results count as progress</b>, "
   "and the strongest objection to it.",
   "<b>State what a successful technique would have to avoid.</b>",
 ],
 "selfcheck": [
   "Prove the time hierarchy theorem and name the two ingredients.",
   "Why is the space hierarchy tighter?",
   "What do the hierarchy theorems separate, and what can they not?",
   "Why is P versus NP not of the right shape for them?",
   "State Baker–Gill–Solovay and what it rules out.",
   "Why does diagonalisation relativise?",
   "Name the three barriers and what each closes.",
   "What technique gets past the first, and what did it prove?",
   "Give five reasons a barrier result is a contribution.",
   "State the honest position on P versus NP.",
 ],
},

]
