# -*- coding: utf-8 -*-
"""CSCE 627 Theory of Computability — original course content."""

COURSE = {
    "code": "CSCE 627",
    "title": "Theory of Computability",
    "tagline": "What no computer can do, proved — and why that is "
               "a practical fact rather than a philosophical one",
    "term": "Semester 8 (with CSCE 637 and CSCE 658)",
    "prereqs": "CSCE 629 Analysis of Algorithms; CSCE 605 Compiler "
               "Design is helpful for Modules 02–03 and 12; comfort "
               "with proof by contradiction and induction",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A written portfolio of proofs — including one "
                   "undecidability result you reduced yourself and one "
                   "honest account of how an undecidable problem is "
                   "handled in a tool you actually use",
    "description": [
        "<b>This is the only course in the program whose results are "
        "permanent.</b> An algorithm can be improved and a model can be "
        "retrained; <b>a proof that no algorithm exists does not expire, "
        "and no amount of hardware or cleverness affects it.</b> That is "
        "worth a semester on its own, and it is why theory sits here "
        "rather than at the start.",
        "<b>The organising question is what a computation is.</b> "
        "<b>Module 01 takes that seriously</b>, because the "
        "undecidability results of Modules 05 and 06 are only "
        "meaningful if 'algorithm' has a definition — and the fact "
        "that every reasonable definition turned out to be equivalent "
        "(Module 11) is the strongest evidence available that the "
        "definition is the right one.",
        "<b>The second theme is that the proofs are reusable "
        "techniques rather than isolated results.</b> <b>Diagonalisation "
        "(Module 05) and reduction (Module 06) are the two methods</b>, "
        "and between them they establish essentially everything in the "
        "course — so learning them properly is learning the "
        "subject, and <b>reduction in particular is the same technique as "
        "CSCE 629's NP-hardness proofs</b>.",
        "<b>The third is that this material has immediate "
        "consequences.</b> <b>Module 08 catalogues the undecidable "
        "problems that appear in tools you use</b> — type checking, "
        "alias analysis, termination, optimisation — and "
        "<b>Module 12 is about what engineering does instead</b>: "
        "soundness, completeness, and the deliberate choice of which to "
        "give up. <b>Every static analyser you have used embodies that "
        "choice</b>, and knowing which choice it made tells you what its "
        "output means.",
        "<b>And the fourth is that undecidability is not defeat.</b> "
        "<b>Compilers optimise, verifiers verify, and type checkers "
        "check, all while the underlying questions are "
        "undecidable</b> — by restricting the input, accepting "
        "approximation, or declining to answer. <b>Which is the "
        "engineering response, and it is a good one.</b>",
    ],
    "outcomes": [
        "State the Church–Turing thesis and explain what kind of "
        "claim it is.",
        "Prove a language non-regular using the pumping lemma.",
        "Place a language in the Chomsky hierarchy and justify it.",
        "Explain Turing machine robustness and universality.",
        "Distinguish decidable from recognisable and prove the halting "
        "problem undecidable.",
        "Construct a mapping reduction to prove a problem "
        "undecidable.",
        "State and apply Rice's theorem.",
        "Place a problem in the arithmetic hierarchy.",
        "Identify undecidable problems in real tools.",
        "Explain Gödel's incompleteness via computability.",
        "Explain the soundness-completeness trade in static analysis.",
        "State what an undecidability result does and does not "
        "forbid.",
    ],
    "materials": [
        ("Sipser — Introduction to the Theory of Computation, 3rd "
         "edition",
         "https://math.mit.edu/~sipser/book.html",
         "<b>The primary source and the best-written textbook in "
         "theoretical computer science.</b> Chapters 1–6 are this "
         "course. Library copy; the first chapter is free from the "
         "publisher and MIT 18.404 follows it exactly."),
        ("MIT 18.404J — Theory of Computation (free lectures and "
         "problem sets, taught by Sipser)",
         "https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/",
         "<b>The author lecturing from his own book, free in full</b> "
         "— video, notes, problem sets, and exams with solutions. "
         "This is the single best free resource in the program."),
        ("Hopcroft, Motwani & Ullman — Introduction to Automata "
         "Theory, Languages, and Computation",
         "https://www.pearson.com/en-us/subject-catalog/p/introduction-to-automata-theory-languages-and-computation/P200000003517",
         "<b>Stronger on Modules 02–03</b> than Sipser, and the "
         "parsing material connects directly to CSCE 605. Library "
         "copy."),
        ("Soare — Turing Computability; and Rogers — Theory of "
         "Recursive Functions",
         "https://link.springer.com/book/10.1007/978-3-642-31933-4",
         "<b>Module 07 and Module 09's reference</b> — the "
         "arithmetic hierarchy and degrees, done properly. For the "
         "student who wants to go further."),
        ("Nagel & Newman — Gödel's Proof; and Smith — An "
         "Introduction to Gödel's Theorems",
         "https://www.logicmatters.net/igt/",
         "<b>Module 10.</b> Smith's book has a free study guide at this "
         "link, and it is the right level for someone who has just done "
         "Module 05."),
        ("Cousot & Cousot — Abstract Interpretation (free papers); "
         "and the Infer and Astrée documentation",
         "https://www.di.ens.fr/~cousot/COUSOTpapers.shtml",
         "<b>Module 12's material</b> — how production analysers "
         "live with undecidability, from the people who formalised the "
         "approach."),
    ],
    "tooling": [
        "<b>Paper, and a willingness to write proofs out in full.</b> "
        "<b>This is the one course in the program where the deliverable "
        "is prose</b>, and a proof you cannot write down is a proof you "
        "do not have.",
        "<b>A simulator you write yourself</b> — a DFA, an NFA, a "
        "Turing machine. <b>Implementing the models makes the "
        "constructions concrete</b>, and the equivalence proofs of "
        "Module 02 become code you can test.",
        "<b>A SAT or SMT solver</b> (CSCE 625 Module 08) to see where "
        "the decidable boundary actually sits in practice — Z3 will "
        "cheerfully report 'unknown' on the undecidable fragments.",
        "<b>A static analyser on your own code</b>: a type checker in "
        "strict mode, a linter, Infer, or a termination checker. "
        "<b>Module 12 requires you to find a false positive and a false "
        "negative</b>, and both exist.",
        "<b>A proof assistant, optionally</b> — Lean or Coq. "
        "<b>Not required, and formalising one proof from this course is "
        "unusually instructive</b> about what a proof actually is.",
        "<b>No GPU, no cluster, and no dataset.</b> <b>The only course "
        "in the program with no computational requirement at all</b>, "
        "which is itself worth noticing.",
    ],
    "projects": [
        {"title": "A portfolio of proofs", "after": 7,
         "brief": "Prove things, in writing, to a standard someone else "
                  "could check.",
         "reqs": [
             "<b>Two non-regularity proofs</b> by the pumping lemma, one "
             "of which needs a non-obvious decomposition.",
             "<b>One language shown context-free and one shown not</b>, "
             "with the argument in each case.",
             "<b>A Turing machine constructed and simulated</b> for a "
             "non-trivial task, with a trace.",
             "<b>The halting problem proved undecidable</b>, written out "
             "in your own words rather than reproduced.",
             "<b>Three mapping reductions</b> proving three different "
             "problems undecidable.",
             "<b>One application of Rice's theorem</b>, with the "
             "non-trivial-property condition verified.",
         ],
         "done": [
             "<b>Every proof checkable by someone else</b> without "
             "needing to ask you what a step meant.",
             "<b>The reductions in the right direction</b>, which is "
             "where most attempts fail — state explicitly what "
             "reduces to what.",
             "<b>The Rice condition actually verified</b>, not "
             "asserted.",
             "<b>At least one proof you got wrong first</b>, with the "
             "error and the fix both written down — which is graded "
             "and is the point.",
         ]},
        {"title": "Undecidability in a tool you use", "after": 12,
         "brief": "Take a real tool, find the undecidable problem it is "
                  "pretending to solve, and characterise what it does "
                  "instead.",
         "reqs": [
             "<b>A tool you actually use</b>: a type checker, a linter, "
             "an optimiser, a verifier, a race detector.",
             "<b>The undecidable problem identified</b>, with a citation "
             "or a reduction showing it is undecidable.",
             "<b>The tool's strategy characterised</b>: is it sound, "
             "complete, or neither? Which did it give up?",
             "<b>A false positive you constructed</b>, with the source "
             "code.",
             "<b>A false negative you constructed</b>, with the source "
             "code.",
             "<b>The documentation's own claim quoted</b>, and assessed "
             "against what you found.",
         ],
         "done": [
             "<b>Both the false positive and the false negative "
             "working</b>, with code anyone can run.",
             "<b>The soundness position stated correctly</b> — most "
             "tools are neither sound nor complete, and saying so "
             "precisely is the exercise.",
             "<b>The undecidability argument correct</b>, not merely "
             "cited.",
             "<b>An honest assessment of whether the tool's own "
             "documentation is accurate about its limits</b>, which "
             "frequently it is not.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "What a Computation Is",
 "subtitle": "Why the question needed answering.",
 "question": "What does it mean to say something can be computed?",
 "outcomes": [
     "Explain why a formal definition of algorithm was necessary.",
     "State the Church–Turing thesis and classify what kind of "
     "claim it is.",
     "Explain why multiple independent definitions coinciding is the "
     "evidence.",
     "Distinguish a problem from an instance and from a language.",
     "Explain what an impossibility result is and is not.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The question",
   "blurb": "Hilbert asked for a procedure, and nobody could say what "
            "that was."},

  {"t": "callout", "title": "You cannot prove no algorithm exists until you define algorithm",
   "kind": "Why the 1930s mattered",
   "body": ["<b>Hilbert's tenth problem asked for a procedure to decide "
            "whether a Diophantine equation has an integer "
            "solution.</b> Everyone understood the request.",
            "<b>And nobody could prove that no such procedure exists, "
            "because 'procedure' was not defined.</b> You cannot "
            "quantify over a class you have not specified.",
            "<b>So the 1930s produced definitions:</b> Church's lambda "
            "calculus, Turing's machines, Gödel and Herbrand's "
            "recursive functions, Post's rewriting systems.",
            "<b>And they all turned out to define the same class of "
            "functions</b> — which was not expected and is the "
            "central evidence of Part 2. <b>Hilbert's tenth was then "
            "settled, negatively, in 1970.</b>"]},

  {"t": "table", "kicker": "Vocabulary", "title": "Problem, instance, language",
   "header": ["Term", "Means", "Example"],
   "widths": [2.5, 4.3, 5.2],
   "rows": [
     ["<b>Instance</b>", "<b>One specific input</b>", "<b>'Is 91 prime?'</b>"],
     ["<b>Problem</b>", "<b>The family of all instances</b>", "<b>'Given n, is n prime?'</b>"],
     ["<b>Decision problem</b>", "<b>A problem with a yes/no answer</b>", "<b>Primality. Not factoring</b>"],
     ["<b>Language</b>", "<b>The set of strings whose answer is yes</b>", "<b>{ n : n is prime }, encoded</b>"],
     ["<b>Encoding</b>", "<b>How objects become strings</b>", "<b>Usually immaterial — but see the note</b>"],
   ],
   "footnote": "<b>Decision problems are the whole subject because a "
               "yes/no question is a <i>set</i></b>, and sets are what "
               "the mathematics handles — and most questions can be "
               "recast as decision problems without loss.",
   "note": "The problem/language identification is what makes everything "
           "else possible."},

  {"t": "callout", "title": "Encoding usually does not matter, and knowing when it does matters",
   "kind": "A detail with real teeth",
   "body": ["<b>Any reasonable encoding of a graph, a program, or a "
            "number can be converted to any other in polynomial "
            "time</b> — so decidability is encoding-independent, and "
            "so is polynomial-time complexity.",
            "<b>The exception is <i>unary</i> versus binary for "
            "numbers.</b> A number n written in unary takes n symbols "
            "and in binary takes log n.",
            "<b>So an algorithm polynomial in the unary length is "
            "exponential in the binary length</b> — which is exactly "
            "what 'pseudo-polynomial' means (CSCE 629's knapsack).",
            "<b>Decidability is unaffected</b> and <b>complexity is "
            "not</b> — <b>which is one of the differences between "
            "this course and CSCE 637</b>, and is worth filing now."]},

  {"t": "section", "label": "Part 2", "title": "The thesis",
   "blurb": "What kind of claim it is."},

  {"t": "callout", "title": "The Church–Turing thesis is not a theorem",
   "kind": "And this is important",
   "body": ["<b>The claim is that the intuitive notion of 'effectively "
            "computable' coincides with Turing computability.</b>",
            "<b>It cannot be proved, because one side is informal.</b> "
            "<b>It is a claim about the adequacy of a definition</b>, "
            "not a mathematical statement — and conflating the two is "
            "the commonest confusion about it.",
            "<b>The evidence is the coincidence of independent "
            "formalisations</b> (Module 11): lambda calculus, "
            "recursive functions, Post systems, register machines, "
            "cellular automata, and every programming language.",
            "<b>Nothing has ever been proposed that is effectively "
            "computable and not Turing computable</b> — ninety years "
            "of attempts, including quantum computation, which "
            "<b>changes the <i>speed</i> and not the class</b>."]},

  {"t": "table", "kicker": "Models", "title": "Independent definitions, one class",
   "header": ["Model", "Proposed by", "Nature"],
   "widths": [3.0, 3.4, 4.9],
   "rows": [
     ["<b>Lambda calculus</b>", "<b>Church, 1936</b>", "<b>Function abstraction and application</b>"],
     ["<b>Turing machines</b>", "<b>Turing, 1936</b>", "<b>A tape and a finite control</b>"],
     ["<b>μ-recursive functions</b>", "<b>Gödel, Herbrand</b>", "<b>Composition, recursion, minimisation</b>"],
     ["<b>Post systems</b>", "Post, 1936", "String rewriting"],
     ["<b>Register machines</b>", "Minsky", "<b>Two counters suffice</b>"],
     ["<b>Rule 110, Game of Life</b>", "Cook, Conway", "<b>Cellular automata (M11)</b>"],
   ],
   "footnote": "<b>These were designed for different purposes by people "
               "with different goals</b>, and they coincide exactly "
               "— which is why the thesis is believed rather than "
               "merely assumed.",
   "note": "The independence of the formalisations is the whole "
           "argument."},

  {"t": "section", "label": "Part 3", "title": "What a limit means",
   "blurb": "Reading an impossibility result correctly."},

  {"t": "bullets", "kicker": "Reading", "title": "What 'undecidable' does and does not say",
   "items": [
     "<b>It says: no single algorithm answers <i>every</i> "
     "instance.</b> That is the entire claim.",
     "",
     "<b>It does not say any particular instance is hard.</b> <b>Most "
     "programs you can write are obviously terminating or obviously "
     "not</b> — the difficulty is in the universal quantifier.",
     "",
     "<b>It does not forbid a useful tool.</b> <b>Answer yes, no, or "
     "'I cannot tell' and you have a decidable problem</b> "
     "(Module 12).",
     "",
     "<b>It does not forbid solving a restricted version.</b> "
     "Terminating for loops, well-founded recursion, total functional "
     "languages — all decidable.",
     "",
     "<b>And it is permanent.</b> <b>No hardware, no model, and no "
     "cleverness changes it</b>, which is unlike every other result in "
     "this program.",
   ],
   "footnote": "<b>'Undecidable' means the problem has no total "
               "algorithm</b>, and conflating that with 'intractable in "
               "practice' is the mistake to avoid for the next twelve "
               "modules."},

  {"t": "callout", "title": "Where this course goes",
   "kind": "The shape of the semester",
   "body": ["<b>Modules 02–03: what weaker machines "
            "cannot do.</b> Finite memory and a stack — and the "
            "proofs are the same techniques in miniature.",
            "<b>Modules 04–07: the Turing machine, "
            "undecidability, and the structure above it.</b> "
            "<b>Diagonalisation and reduction, which are the course's "
            "two methods.</b>",
            "<b>Modules 08–10: undecidability in practice, "
            "computable functions, and incompleteness</b> — "
            "<b>Gödel's theorem is a corollary of Module 05</b>, "
            "which is the most satisfying connection here.",
            "<b>Modules 11–13: other models, the "
            "engineering response, and an honest statement of the "
            "limits.</b>"]},
 ],
 "takeaways": [
   "You cannot prove no algorithm exists until 'algorithm' is defined, "
   "which is why the 1930s mattered and why Hilbert's tenth waited until "
   "1970.",
   "A decision problem is a language — the set of strings whose "
   "answer is yes — and that identification is what makes the "
   "mathematics work.",
   "Encoding does not affect decidability; unary versus binary does affect "
   "complexity, which is what 'pseudo-polynomial' means.",
   "The Church–Turing thesis is a claim about the adequacy of a "
   "definition, not a theorem, and the evidence is the coincidence of "
   "independent formalisations.",
   "'Undecidable' means no single algorithm answers every instance; it "
   "says nothing about any particular instance.",
   "And the results are permanent — unlike everything else in this "
   "program, no hardware or model change affects them.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The question, and the vocabulary"),
  ("callout", "You cannot prove no algorithm exists until you define "
              "algorithm",
   ["<b>Hilbert's tenth problem (1900) asked for a procedure to decide "
    "whether a given polynomial equation with integer coefficients has an "
    "integer solution.</b> Everyone understood what was being asked, and "
    "work on it proceeded for decades.",
    "<b>And nobody could prove that no such procedure exists, because "
    "'procedure' had no definition.</b> <b>You cannot prove a statement "
    "quantified over a class you have not specified</b> — which is "
    "an obvious point in retrospect and was not obvious at the time.",
    "<b>So the 1930s produced definitions, several at once:</b> Church's "
    "lambda calculus, Turing's machines, G&ouml;del and Herbrand's "
    "general recursive functions, Post's rewriting systems — all "
    "within about two years, by people pursuing different questions.",
    "<b>And they all turned out to define exactly the same class of "
    "functions.</b> <b>Which was not expected, and is the central "
    "evidence discussed in &sect;2.</b> <b>Hilbert's tenth was then "
    "settled negatively in 1970</b> (Matiyasevich, building on Davis, "
    "Putnam and Robinson) — <b>seventy years after it was asked and "
    "thirty-four after it became possible to answer it</b>, which is a "
    "fair measure of how much the definition was worth."]),
  ("table", ["Term", "What it means", "Example"],
   [["<b>Instance</b>", "<b>One specific input.</b>",
     "<b>'Is 91 prime?'</b> — a question with one answer."],
    ["<b>Problem</b>", "<b>The whole family of instances.</b>",
     "<b>'Given n, is n prime?'</b> — which is what an algorithm "
     "must answer for all n."],
    ["<b>Decision problem</b>", "<b>A problem whose answer is yes or "
     "no.</b>",
     "<b>Primality is a decision problem; factoring is not</b>, though it "
     "has a decision version."],
    ["<b>Language</b>",
     "<b>The set of strings whose answer is yes.</b>",
     "<b>{ n : n is prime }, suitably encoded as strings.</b>"],
    ["<b>Encoding</b>", "<b>How objects are represented as strings.</b>",
     "<b>Usually immaterial — but see the callout.</b>"]],
   [0.19, 0.36, 0.45]),
  ("p", "<b>Decision problems are the whole subject, because a yes/no "
        "question <i>is</i> a set</b> — the set of inputs whose "
        "answer is yes — <b>and sets of strings are what the "
        "mathematics handles well</b>. <b>Most questions can be recast as "
        "decision problems without losing anything essential</b>: instead "
        "of 'what is the shortest path', ask 'is there a path of length at "
        "most k', and binary-search on k. <b>That reduction is why the "
        "restriction costs nothing</b>, and the same move is standard in "
        "CSCE 637."),
  ("callout", "Encoding usually does not matter, and knowing when it does "
              "matters",
   ["<b>Any two reasonable encodings of a graph, a program, or a number "
    "can be converted into one another in polynomial time</b> — an "
    "adjacency matrix to an adjacency list, one source syntax to another "
    "— <b>so decidability is encoding-independent, and so is "
    "polynomial-time complexity.</b> This is why nobody specifies the "
    "encoding.",
    "<b>The exception is <i>unary</i> versus binary notation for "
    "numbers.</b> A number n written in unary occupies n symbols and in "
    "binary occupies about log n, so <b>the two encodings differ "
    "exponentially in length</b> — which is not a polynomial "
    "conversion in one direction.",
    "<b>So an algorithm that is polynomial in the unary input length is "
    "exponential in the binary length</b>, and <b>that is exactly what "
    "'pseudo-polynomial' means</b> — CSCE 629's dynamic-programming "
    "knapsack algorithm is polynomial in the capacity and exponential in "
    "the number of bits of the capacity.",
    "<b>Decidability is entirely unaffected by this and complexity is "
    "not</b> — <b>which is one of the clearest differences between "
    "this course and CSCE 637</b>, and is worth filing now because the "
    "two courses will otherwise blur together."]),

  ("h1", "2 &nbsp; The Church–Turing thesis"),
  ("callout", "The Church–Turing thesis is not a theorem",
   ["<b>The claim is that the intuitive notion of 'effectively "
    "computable by a mechanical procedure' coincides exactly with Turing "
    "computability.</b>",
    "<b>It cannot be proved, because one side of the claimed equality is "
    "informal.</b> <b>It is a claim about the adequacy of a "
    "definition</b> — that the formal notion captures the intuitive "
    "one — <b>rather than a mathematical statement</b>, and "
    "<b>conflating the two is the commonest confusion about it.</b>",
    "<b>The evidence is the coincidence of independent "
    "formalisations</b> (Module 11, and the table below): lambda "
    "calculus, &mu;-recursive functions, Post systems, register machines, "
    "cellular automata, and every general-purpose programming language "
    "ever designed. <b>Each was defined for its own reasons and each "
    "defines the same class.</b>",
    "<b>And nothing has ever been proposed that is effectively "
    "computable and not Turing computable</b> — ninety years of "
    "attempts, including <b>quantum computation, which changes the "
    "<i>speed</i> of some computations and not the class of computable "
    "functions at all</b>. A quantum computer cannot decide the halting "
    "problem (CSCE 640 returns to this)."]),
  ("table", ["Model", "Proposed by", "Its nature"],
   [["<b>Lambda calculus</b>", "<b>Church, 1936</b>",
     "<b>Function abstraction and application, with nothing else</b> "
     "— no numbers, no data structures, no state."],
    ["<b>Turing machines</b>", "<b>Turing, 1936</b>",
     "<b>An infinite tape and a finite control</b>, designed explicitly "
     "to model a person computing with paper."],
    ["<b>&mu;-recursive functions</b>",
     "<b>G&ouml;del and Herbrand, early 1930s</b>",
     "<b>Composition, primitive recursion, and unbounded "
     "minimisation</b> (Module 09)."],
    ["<b>Post systems</b>", "Post, 1936", "String rewriting rules."],
    ["<b>Register machines</b>", "Minsky, 1960s",
     "<b>Two counters and increment, decrement, and test suffice</b> "
     "— which is a striking minimality result."],
    ["<b>Rule 110, the Game of Life</b>", "Cook, Conway",
     "<b>Cellular automata with no control flow at all</b> "
     "(Module 11)."]],
   [0.23, 0.26, 0.51]),
  ("p", "<b>These were designed for different purposes by people pursuing "
        "different questions — Church was interested in the "
        "foundations of logic, Turing in what a human calculator does, "
        "G&ouml;del in arithmetic definability — and they coincide "
        "exactly.</b> <b>Which is why the thesis is believed rather than "
        "merely assumed</b>, and why it is reasonable to treat 'computable' "
        "as a settled notion for the rest of the course."),

  ("break",),
  ("h1", "3 &nbsp; What an impossibility result means"),
  ("ul", ["<b>It says: no single algorithm answers <i>every</i> "
          "instance correctly.</b> <b>That is the entire claim</b>, and "
          "reading it as more is the source of nearly every "
          "misunderstanding of this subject.",
          "<b>It does not say that any particular instance is hard.</b> "
          "<b>Most programs you can actually write are obviously "
          "terminating or obviously not</b> — the difficulty lives "
          "entirely in the universal quantifier, and a tool that handles "
          "the programs people write can be extremely useful "
          "(Module 12).",
          "<b>It does not forbid a useful tool.</b> <b>Answer 'yes', "
          "'no', or 'I cannot tell', and the resulting problem is "
          "decidable</b> — the third answer is what buys the "
          "decidability, and every real analyser uses it.",
          "<b>It does not forbid solving a restricted version.</b> "
          "Termination of <code>for</code> loops with constant bounds, "
          "recursion on a well-founded order, total functional languages "
          "like Agda — <b>all decidable, by construction</b>, and "
          "<b>restriction is the other engineering response</b> "
          "(Module 12 &sect;2).",
          "<b>And it is permanent.</b> <b>No faster hardware, no new "
          "computational model, and no amount of cleverness changes "
          "it</b> — <b>which is unlike every other result in this "
          "program</b>, where an algorithm can be improved or a model "
          "retrained. <b>'Undecidable' means the problem has no total "
          "algorithm, and conflating that with 'intractable in practice' "
          "is the mistake to avoid for the next twelve modules.</b>"]),
  ("callout", "Where this course goes",
   ["<b>Modules 02 and 03: what weaker machines cannot do.</b> Finite "
    "memory, and then finite memory plus a stack — <b>and the proofs "
    "there are the course's two techniques in miniature</b>, on objects "
    "simple enough to see all the way through.",
    "<b>Modules 04 through 07: the Turing machine, undecidability, and "
    "the structure above it.</b> <b>Diagonalisation (Module 05) and "
    "reduction (Module 06) are the course's two methods</b>, and between "
    "them they establish almost everything else.",
    "<b>Modules 08 through 10: undecidability in real tools, the theory "
    "of computable functions, and incompleteness.</b> "
    "<b>G&ouml;del's first incompleteness theorem is essentially a "
    "corollary of Module 05</b>, which is the most satisfying connection "
    "in the course and the reason Module 10 comes after rather than "
    "before.",
    "<b>Modules 11 through 13: alternative models, the engineering "
    "response to undecidability, and an honest statement of what the "
    "limits do and do not constrain.</b>"]),
 ],
 "resources": [
   ("Sipser &mdash; Introduction to the Theory of Computation, "
    "chapter 0 and section 3.3",
    "https://math.mit.edu/~sipser/book.html",
    "<b>The vocabulary of &sect;1 and the thesis discussion of "
    "&sect;2</b>, stated carefully."),
   ("MIT 18.404J &mdash; lecture 1 (free video and notes)",
    "https://ocw.mit.edu/courses/18-404j-theory-of-computation-fall-2020/",
    "<b>Sipser lecturing on this material</b>, which is the best "
    "available introduction and is free."),
   ("Turing &mdash; On Computable Numbers (1936) (free)",
    "https://www.cs.virginia.edu/~robins/Turing_Paper_1936.pdf",
    "<b>The original.</b> Section 9's argument that the machine captures "
    "what a human computer does is the thesis's actual "
    "justification, and it is readable."),
   ("Matiyasevich &mdash; Hilbert's Tenth Problem (free chapters)",
    "https://logic.pdmi.ras.ru/~yumat/H10Pbook/",
    "<b>&sect;1's motivating problem, resolved</b> — and a good "
    "illustration of how long a reduction can take to construct."),
 ],
 "exercises": [
   "<b>Write three decision problems from your own work</b> and express "
   "each as a language.",
   "<b>Find a problem that is not naturally a decision problem</b> and "
   "recast it as one. State what was lost.",
   "<b>Show that two encodings of a graph convert in polynomial "
   "time.</b>",
   "<b>Show that unary and binary do not</b>, and relate it to "
   "CSCE 629's knapsack algorithm.",
   "<b>Write down, in your own words, what kind of claim the "
   "Church–Turing thesis is</b>, and why it cannot be proved.",
   "<b>Find a claimed counterexample to the thesis</b> and identify what "
   "it assumes (usually infinite precision or infinite time).",
   "<b>For three programs you have written, decide whether they "
   "terminate</b> and note how long each took to settle.",
   "<b>Write a program whose termination you cannot determine.</b>",
   "<b>Find a tool that answers 'I cannot tell'</b> and note how often "
   "it does.",
   "<b>Write down what you expect to be impossible</b>, and keep it for "
   "Module 13.",
 ],
 "selfcheck": [
   "Why could Hilbert's tenth problem not be answered in 1900?",
   "Define instance, problem, decision problem, and language.",
   "Why is a decision problem a set?",
   "When does encoding matter, and what is the term for the "
   "consequence?",
   "What kind of claim is the Church–Turing thesis?",
   "What is the evidence for it, and why is independence important?",
   "Does quantum computation affect it?",
   "State four things 'undecidable' does not mean.",
   "What makes this course's results different from the rest of the "
   "program's?",
 ],
},

]

for _b in ("c627_b2", "c627_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
