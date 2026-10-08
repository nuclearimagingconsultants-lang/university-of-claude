# -*- coding: utf-8 -*-
"""CSCE 627 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Undecidability in the Wild",
 "subtitle": "The theorems, in tools you used this week.",
 "question": "Where does undecidability actually show up?",
 "outcomes": [
     "Identify undecidable problems in compilers and type systems.",
     "Identify them in program analysis and verification.",
     "Explain why they appear and what the tool does instead.",
     "Explain the Halting-adjacent problems in security.",
     "Read a tool's documentation for its soundness position.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "In your compiler",
   "blurb": "Every phase meets one."},

  {"t": "table", "kicker": "Compilers", "title": "Undecidable problems a compiler faces",
   "header": ["Question", "Status", "What the compiler does"],
   "widths": [3.2, 2.6, 5.2],
   "rows": [
     ["<b>Is this code reachable?</b>", "<b>Undecidable</b>", "<b>Conservative: assume reachable unless provably not</b>"],
     ["<b>Do these two pointers alias?</b>", "<b>Undecidable</b>", "<b>Assume they might — and lose optimisations</b>"],
     ["<b>Does this loop terminate?</b>", "<b>Undecidable</b>", "<b>Recognise the easy patterns only</b>"],
     ["<b>Is this grammar ambiguous?</b>", "<b>Undecidable</b>", "<b>Report conflicts (M03 §2)</b>"],
     ["<b>Are these two expressions equal?</b>", "<b>Undecidable</b>", "<b>Syntactic matching plus known identities</b>"],
     ["<b>Is this the optimal code?</b>", "<b>Undecidable</b>", "<b>Apply a fixed sequence of rewrites</b>"],
   ],
   "footnote": "<b>Every row is Rice's theorem</b> (Module 06 §2) "
               "— these are all semantic properties of programs, "
               "and the pattern of response is always 'be conservative' "
               "or 'handle the easy cases'.",
   "note": "Students are surprised how many; the table is the point."},

  {"t": "callout", "title": "Alias analysis is the most expensive one",
   "kind": "Why it matters disproportionately",
   "body": ["<b>'Can these two pointers refer to the same "
            "location?'</b> If the compiler cannot rule it out, it must "
            "assume they can.",
            "<b>And that assumption blocks reordering, caching in "
            "registers, and vectorisation</b> — so <b>the "
            "undecidability of aliasing costs measurable performance in "
            "every C program.</b>",
            "<b>Which is why <code>restrict</code> exists</b>, and why "
            "Fortran historically outperformed C on numerical code: "
            "<b>Fortran's rules let the compiler assume no aliasing.</b>",
            "<b>And why Rust's borrow checker is interesting here:</b> "
            "<b>it makes the programmer supply the proof the compiler "
            "cannot find</b> — which is Module 12 §3's third "
            "strategy, in a shipping language."]},

  {"t": "section", "label": "Part 2", "title": "In your type checker",
   "blurb": "And why it rejects programs that work."},

  {"t": "callout", "title": "Type checking is decidable because the language was designed to make it so",
   "kind": "The design constraint",
   "body": ["<b>Type inference for the full lambda calculus with "
            "polymorphic recursion is undecidable.</b> So languages "
            "restrict it.",
            "<b>Hindley–Milner inference is decidable</b> "
            "(and DEXPTIME-complete in theory, linear in practice) "
            "— <b>because let-polymorphism is restricted in exactly "
            "the way that keeps it decidable.</b>",
            "<b>And dependent types push the boundary:</b> "
            "<b>type checking stays decidable only if the language "
            "guarantees termination</b>, which is why Agda and Idris have "
            "totality checkers.",
            "<b>So the rule is:</b> <b>a type checker rejects some "
            "programs that would have worked, and that is the price of "
            "terminating</b> — <b>the alternative is a checker that "
            "sometimes does not answer.</b>"]},

  {"t": "code", "kicker": "The trade", "title": "Pick two of three",
   "lang": "text", "code": """
  SOUND       never accepts a bad program
              (no false negatives)
  COMPLETE    never rejects a good program
              (no false positives)
  TERMINATING always gives an answer

  RICE SAYS YOU CANNOT HAVE ALL THREE. Pick two.

  And which two a tool picked is exactly what its output
  licenses you to believe -- so it is the first thing to
  find out about any analyser.
""",
   "caption": "<b>Pick two of three is the whole design space</b> "
              "— and the next slide places the tools you "
              "already use.",
   "note": "This frame is the most useful thing in the module."},

  {"t": "code", "kicker": "Positions", "title": "Who picks which two",
   "lang": "text", "code": """
  TYPE CHECKERS            sound + terminating
      -> they reject valid programs. You have met this.

  MOST LINTERS             neither + terminating
      -> false positives AND false negatives, and still
         useful, because they are cheap and fast.

  VERIFIERS (Astree,       sound + terminating
  SPARK, bounded CBMC)
      -> many false positives, BY DESIGN, because in
         their domain a missed bug is unacceptable.

  BUG FINDERS (Infer,      complete-ish + terminating
  Coverity)
      -> they prefer not to cry wolf, so they miss bugs
         deliberately. A product decision, not a defect.

  PROOF ASSISTANTS         sound + complete
      -> and NOT automatically terminating. A human
         supplies the search the tool cannot.
""",
   "caption": "<b>The proof-assistant row is the only one with both "
              "soundness and completeness</b>, and it pays for them with "
              "a human (Module 12 §3).",
   "note": "Have students place their own toolchain in this list."},

  {"t": "section", "label": "Part 3", "title": "In verification and security",
   "blurb": "Where the stakes are higher."},

  {"t": "bullets", "kicker": "Elsewhere", "title": "More undecidable problems you have met",
   "items": [
     "<b>'Is this program malware?'</b> <b>Undecidable</b> "
     "— behavioural properties are semantic. So detection is "
     "signatures, heuristics, and sandboxing.",
     "",
     "<b>'Does this program leak secrets?'</b> Non-interference is "
     "undecidable; practical systems use type systems or taint "
     "tracking, both approximate.",
     "",
     "<b>'Can this race occur?'</b> Undecidable, which is why race "
     "detectors report both false positives and false negatives.",
     "",
     "<b>'Will this smart contract terminate?'</b> <b>Which is why "
     "Ethereum charges gas</b> — bounding the resource makes it "
     "decidable (Module 06 §2).",
     "",
     "<b>And 'is this virus signature sufficient?'</b> — "
     "Cohen's 1987 result that virus detection is undecidable.",
   ],
   "footnote": "<b>The gas mechanism is the cleanest engineering "
               "response in this list:</b> rather than deciding "
               "termination, make non-termination expensive and bounded "
               "by construction."},

  {"t": "callout", "title": "Bounded model checking: give up the quantifier on purpose",
   "kind": "The most successful response",
   "body": ["<b>'Is there a bug?' is undecidable. 'Is there a bug "
            "within k steps?' is decidable</b> — unroll k steps and "
            "hand it to a SAT solver (CSCE 625 §08).",
            "<b>So the tool answers a strictly weaker question "
            "completely</b>, rather than the real question partially.",
            "<b>And it is the dominant industrial verification "
            "technique</b> for exactly that reason: <b>the answer is "
            "trustworthy within its bound, and the bound is "
            "stated.</b>",
            "<b>The honest claim is 'no bug within 20 steps', not 'no "
            "bug'</b> — and <b>a tool that says the first and a "
            "reader who hears the second is the failure mode to "
            "watch.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Reading a tool honestly",
   "blurb": "What its documentation should tell you."},

  {"t": "bullets", "kicker": "Reading", "title": "Questions to ask of any analyser",
   "items": [
     "<b>Which of sound, complete, terminating did it give up?</b> "
     "<b>If the documentation does not say, assume neither sound nor "
     "complete.</b>",
     "",
     "<b>What is the bound?</b> Loop unrolling depth, call depth, "
     "timeout — <b>and what happens when it is hit.</b>",
     "",
     "<b>What does 'no issues found' mean?</b> <b>'Proved safe' and "
     "'found nothing' are completely different claims.</b>",
     "",
     "<b>What are the documented unsoundness sources?</b> Reflection, "
     "dynamic loading, native code, concurrency — most analysers "
     "simply do not model these.",
     "",
     "<b>And can you construct a false positive and a false "
     "negative?</b> <b>If you can, you understand the tool; if you "
     "cannot, you do not.</b>",
   ],
   "footnote": "<b>The last question is the project.</b> <b>Constructing "
               "both is the fastest way to calibrate how much to trust an "
               "analyser's output.</b>"},

  {"t": "callout", "title": "What to take from this module",
   "kind": "The summary",
   "body": ["<b>Undecidability is not abstract.</b> <b>It is why your "
            "tools behave the way they do</b>, and the behaviour is "
            "derivable from the theorem rather than from the "
            "implementation.",
            "<b>Every analyser gave up one of sound, complete, "
            "terminating</b>, and <b>which one determines what its "
            "output licenses you to believe.</b>",
            "<b>Bounding a resource is the most successful response</b> "
            "— gas, unrolling depth, timeouts — <b>because it "
            "converts an undecidable question into a decidable weaker "
            "one with a stated scope.</b>",
            "<b>And the tools are genuinely useful anyway</b>, which is "
            "the point. <b>Undecidability constrains what a tool can "
            "promise and not whether it is worth having.</b>"]},
 ],
 "takeaways": [
   "Reachability, aliasing, termination, grammar ambiguity, expression "
   "equality, and optimality are all undecidable, and all are Rice's "
   "theorem.",
   "Aliasing is the most expensive one, which is why `restrict` exists and "
   "why Rust makes the programmer supply the proof.",
   "Type checking is decidable because languages were designed to make it "
   "so, and a checker rejecting valid programs is the price of "
   "terminating.",
   "Pick two of three — sound, complete, terminating — is the "
   "whole design space, and which two a tool picked tells you what its "
   "output means.",
   "Bounded model checking gives up the quantifier on purpose and answers "
   "a weaker question completely, which is why it dominates industrially.",
   "If you cannot construct a false positive and a false negative for an "
   "analyser, you do not understand it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; In your compiler"),
  ("table", ["Question", "Status", "What the compiler does instead"],
   [["<b>Is this code reachable?</b>", "<b>Undecidable</b>",
     "<b>Conservative approximation: assume reachable unless provably "
     "not.</b> Which is why dead-code elimination misses dead code."],
    ["<b>Do these two pointers alias?</b>", "<b>Undecidable</b>",
     "<b>Assume they might, and lose the optimisation</b> — see the "
     "callout, which is the most consequential row here."],
    ["<b>Does this loop terminate?</b>", "<b>Undecidable</b>",
     "<b>Recognise the easy patterns only</b> — a monotone counter "
     "against a constant bound — and give up otherwise."],
    ["<b>Is this grammar ambiguous?</b>", "<b>Undecidable</b>",
     "<b>Report the conflicts the particular method found</b> "
     "(Module 03 &sect;2), which is a diagnostic rather than a "
     "verdict."],
    ["<b>Are these two expressions equal?</b>", "<b>Undecidable</b>",
     "<b>Syntactic matching plus a fixed list of known identities</b> "
     "— which is why common-subexpression elimination misses "
     "obvious cases."],
    ["<b>Is this the optimal code for this program?</b>",
     "<b>Undecidable</b>",
     "<b>Apply a fixed sequence of rewrites and stop.</b> Which is why "
     "<code>-O3</code> is sometimes slower than <code>-O2</code>: the "
     "sequence is a heuristic, not an optimisation."]],
   [0.27, 0.18, 0.55]),
  ("p", "<b>Every row is Rice's theorem</b> (Module 06 &sect;2) "
        "— these are all non-trivial semantic properties of "
        "programs — and <b>the pattern of response is always the "
        "same: be conservative, or handle the easy cases, or bound a "
        "resource.</b> <b>Which means a compiler's limitations are "
        "largely predictable from the theory</b>, and that is a genuinely "
        "useful thing when you are wondering why an optimisation did not "
        "fire."),
  ("callout", "Alias analysis is the most expensive one",
   ["<b>'Can these two pointers refer to the same memory location?'</b> "
    "If the compiler cannot rule it out, <b>it must assume they can</b>, "
    "because assuming otherwise would change the program's meaning.",
    "<b>And that assumption blocks instruction reordering, caching values "
    "in registers across stores, and vectorisation</b> — so "
    "<b>the undecidability of aliasing costs measurable performance in "
    "every C and C++ program ever compiled.</b>",
    "<b>Which is why <code>restrict</code> exists</b> — a promise "
    "from the programmer that the compiler cannot verify — <b>and "
    "why Fortran historically outperformed C on numerical code: "
    "Fortran's aliasing rules let the compiler assume non-aliasing by "
    "default</b>, so it did not have to prove anything.",
    "<b>And it is why Rust's borrow checker is interesting in this "
    "context:</b> <b>it makes the programmer supply, in the type system, "
    "the proof the compiler could not find</b> — the aliasing "
    "information becomes a checkable annotation rather than an undecidable "
    "inference. <b>Which is Module 12 &sect;3's third strategy, in a "
    "shipping language</b>, and it is the clearest case in the program of "
    "an undecidability result shaping a language's design."]),

  ("h1", "2 &nbsp; In your type checker"),
  ("callout", "Type checking is decidable because the language was designed "
              "to make it so",
   ["<b>Type inference for the full lambda calculus with polymorphic "
    "recursion is undecidable.</b> So languages restrict what they will "
    "infer, deliberately, to stay inside a decidable fragment.",
    "<b>Hindley–Milner inference is decidable</b> — "
    "DEXPTIME-complete in the worst case and effectively linear on real "
    "programs — <b>because let-polymorphism is restricted in "
    "precisely the way that preserves decidability.</b> <b>The "
    "restriction is not an oversight; it is the design.</b>",
    "<b>And dependent types push against the boundary:</b> <b>type "
    "checking remains decidable only if the language guarantees that "
    "type-level computation terminates</b> — which is why Agda and "
    "Idris ship totality checkers, and why they reject some programs "
    "whose termination they cannot establish (Module 05 &sect;4's "
    "restriction response).",
    "<b>So the rule is:</b> <b>a type checker rejects some programs that "
    "would have worked, and that is the price of always terminating with "
    "an answer</b> — <b>the only alternative is a checker that "
    "sometimes does not answer at all.</b> <b>Which reframes the "
    "familiar frustration of fighting a type checker: it is not being "
    "obtuse, it is being total.</b>"]),
  ("code", """SOUND        never accepts a bad program
             (no false negatives)
COMPLETE     never rejects a good program
             (no false positives)

RICE SAYS YOU CANNOT HAVE BOTH AND TERMINATE. Pick two of
three: SOUND, COMPLETE, TERMINATING.

WHO PICKS WHAT:

  TYPE CHECKERS          sound + terminating
      -> they reject valid programs. You have met this.

  MOST LINTERS           neither + terminating
      -> false positives AND false negatives, and they are
         still useful because they are cheap and fast.

  VERIFIERS (Astree,     sound + terminating
  SPARK, bounded CBMC)
      -> many false positives, BY DESIGN, because in their
         domain a missed bug is unacceptable.

  BUG FINDERS (Infer,    complete-ish + terminating
  Coverity)
      -> they prefer not to cry wolf, so they miss bugs
         deliberately. A product decision, not a defect.

  PROOF ASSISTANTS       sound + complete
      -> and NOT automatically terminating. A human
         supplies the search the tool cannot."""),
  ("p", "<b>'Pick two of three' is the whole design space</b>, and "
        "<b>knowing which two a tool picked tells you exactly what its "
        "output licenses you to believe.</b> <b>It is the most useful "
        "frame in this module</b>, and it applies to every analyser you "
        "will ever use — including ones that do not describe "
        "themselves in these terms, which is most of them."),

  ("break",),
  ("h1", "3 &nbsp; In verification and security"),
  ("ul", ["<b>'Is this program malware?'</b> <b>Undecidable</b> — "
          "malicious behaviour is a semantic property, so Rice applies "
          "directly, <b>and Cohen proved the virus-detection version in "
          "1987.</b> So detection is signatures, behavioural heuristics, "
          "and sandboxed execution, all of which are approximations with "
          "both error types.",
          "<b>'Does this program leak secrets?'</b> Non-interference "
          "— that public outputs do not depend on secret inputs "
          "— is undecidable in general; practical systems use "
          "security type systems or dynamic taint tracking, both "
          "approximate in opposite directions.",
          "<b>'Can this data race occur?'</b> Undecidable, <b>which is "
          "why race detectors report both false positives (a race the "
          "program's logic prevents) and false negatives (a race on a path "
          "not exercised)</b> — and knowing which your detector is "
          "biased toward tells you how to use it.",
          "<b>'Will this smart contract terminate?'</b> <b>Which is why "
          "Ethereum charges gas</b> — <b>rather than deciding "
          "termination, make execution cost money and bound the budget, so "
          "non-termination becomes self-limiting by construction</b> "
          "(Module 06 &sect;2's bounded escape). <b>The cleanest "
          "engineering response in this list</b>, and a good example of "
          "designing around a theorem rather than against it.",
          "<b>And 'is this set of signatures sufficient?'</b> — "
          "which is the same undecidability one level up, and is why no "
          "detection product can claim completeness."]),
  ("callout", "Bounded model checking: give up the quantifier on purpose",
   ["<b>'Is there a bug?' is undecidable. 'Is there a bug reachable "
    "within k steps?' is decidable</b> — unroll the transition "
    "relation k times, encode it as a propositional formula, and hand it "
    "to a SAT solver (CSCE 625 Module 08 &sect;3).",
    "<b>So the tool answers a strictly weaker question completely, rather "
    "than the real question partially.</b> <b>Which is a different and "
    "better trade than it first appears</b>: a complete answer to a "
    "stated weaker question is something you can reason about, and a "
    "partial answer to the real question is not.",
    "<b>And it is the dominant industrial verification technique</b> for "
    "exactly that reason — <b>the answer is trustworthy within its "
    "bound, and the bound is explicit.</b> Hardware verification runs on "
    "this.",
    "<b>The honest claim is 'no bug within 20 steps', not 'no "
    "bug'</b> — and <b>a tool that reports the first while its users "
    "hear the second is the failure mode to watch for</b>, because the "
    "tool is not wrong and the belief is. <b>Which is this program's "
    "scoped-claim discipline, in the one subject where the scope is a "
    "theorem rather than a measurement.</b>"]),

  ("h1", "4 &nbsp; Reading a tool honestly"),
  ("ul", ["<b>Which of sound, complete, and terminating did it give "
          "up?</b> <b>If the documentation does not say, assume it is "
          "neither sound nor complete</b> — which is the correct "
          "default and is the position most linters are in.",
          "<b>What is the bound?</b> Loop unrolling depth, call-graph "
          "depth, path count, timeout — <b>and what happens when the "
          "bound is hit.</b> <b>Silently giving up is very different "
          "from reporting that it gave up</b>, and the distinction is "
          "frequently undocumented.",
          "<b>What does 'no issues found' mean?</b> <b>'Proved safe' and "
          "'found nothing' are completely different claims</b>, and tools "
          "report both with the same green tick. <b>Find out which one "
          "yours means.</b>",
          "<b>What are the documented sources of unsoundness?</b> "
          "Reflection, dynamic class loading, native calls, concurrency, "
          "generated code — <b>most analysers simply do not model "
          "these and say so in a section nobody reads.</b>",
          "<b>And can you construct a false positive and a false "
          "negative?</b> <b>If you can, you understand the tool; if you "
          "cannot, you do not.</b> <b>This is the project, and it is the "
          "fastest way to calibrate how much to trust an analyser's "
          "output</b> — twenty minutes of adversarial construction "
          "tells you more than the manual."]),
  ("callout", "What to take from this module",
   ["<b>Undecidability is not abstract.</b> <b>It is why your tools "
    "behave the way they do</b>, and <b>the behaviour is derivable from "
    "the theorem rather than from the implementation</b> — which "
    "means you can predict a tool's limitations before using it.",
    "<b>Every analyser gave up one of sound, complete, and "
    "terminating</b> (&sect;2), and <b>which one it gave up determines "
    "what its output licenses you to believe.</b>",
    "<b>Bounding a resource is the most successful response</b> — "
    "gas, unrolling depth, timeouts, step limits — <b>because it "
    "converts an undecidable question into a decidable weaker one with an "
    "explicitly stated scope</b>, and a stated scope is what makes a "
    "claim usable.",
    "<b>And the tools are genuinely useful anyway, which is the "
    "point.</b> <b>Undecidability constrains what a tool can promise, "
    "not whether it is worth having</b> — and Module 12 is about "
    "the engineering that lives in that gap."]),
 ],
 "resources": [
   ("Landi &mdash; Undecidability of static analysis (free)",
    "https://dl.acm.org/doi/10.1145/161494.161501",
    "<b>&sect;1's aliasing result, proved</b> — may-alias is "
    "undecidable and so is may-alias for a restricted language."),
   ("Pierce &mdash; Types and Programming Languages",
    "https://www.cis.upenn.edu/~bcpierce/tapl/",
    "<b>&sect;2's decidability boundaries</b> — which type systems "
    "are decidable and why the restrictions are where they are. Library "
    "copy; the exercises are free."),
   ("Cohen &mdash; Computer Viruses: Theory and Experiments (free)",
    "https://all.net/books/virus/index.html",
    "<b>&sect;3's virus-detection undecidability</b>, in the paper that "
    "introduced the term."),
   ("Clarke, Biere, Raimi & Zhu &mdash; Bounded Model Checking (free)",
    "https://www.cs.cmu.edu/~emc/papers/Papers%20In%20Refereed%20Journals/Bounded%20Model%20Checking%20Using%20Satisfiability%20Solving.pdf",
    "<b>&sect;3's method</b> — and the clearest statement of what a "
    "bounded result does and does not establish."),
 ],
 "exercises": [
   "<b>Write code where a compiler must assume aliasing</b> and inspect "
   "the generated assembly.",
   "<b>Add <code>restrict</code> or equivalent</b> and compare. Report "
   "the difference.",
   "<b>Find a dead branch your compiler does not eliminate</b> and "
   "explain why.",
   "<b>Write a program your type checker rejects that would have "
   "worked</b>, and identify the restriction responsible.",
   "<b>Classify five tools you use</b> as sound, complete, terminating "
   "— two of three each.",
   "<b>Construct a false positive</b> for one of them, with code.",
   "<b>Construct a false negative</b> for the same tool.",
   "<b>Read that tool's documentation</b> for its unsoundness sources and "
   "report what it admits.",
   "<b>Run a bounded model checker</b> with two different bounds and "
   "report what changes.",
   "<b>Write the honest claim</b> its output supports, in one "
   "sentence.",
 ],
 "selfcheck": [
   "Name six undecidable problems a compiler faces and what it does "
   "about each.",
   "Why is aliasing the most expensive one, and what are three responses "
   "to it?",
   "Why is type checking decidable, and what does that cost?",
   "State the pick-two-of-three frame and give five tools' positions.",
   "Name four undecidable problems in security or verification.",
   "Why does Ethereum charge gas, in this module's terms?",
   "What does bounded model checking give up, and what does it gain?",
   "Give five questions to ask of an analyser.",
   "What is the fastest way to calibrate a tool?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Computable Functions",
 "subtitle": "The positive theory, and a theorem about self-reference.",
 "question": "What is the structure of what <i>can</i> be computed?",
 "outcomes": [
     "Define primitive recursion and explain what it cannot "
     "express.",
     "Explain μ-recursion and why it recovers full power.",
     "State the recursion theorem and use it.",
     "Explain Kolmogorov complexity and its uncomputability.",
     "Explain the busy beaver function and what it demonstrates.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Primitive recursion",
   "blurb": "Total by construction, and not enough."},

  {"t": "callout", "title": "Primitive recursive functions always terminate, and miss some that do",
   "kind": "The first positive class",
   "body": ["<b>Build functions from zero, successor, and projection, "
            "using composition and recursion on a single decreasing "
            "argument.</b>",
            "<b>Every primitive recursive function is total</b> "
            "— it terminates on every input, by construction, <b>so "
            "termination is decidable for this class</b> "
            "(Module 05 §4's restriction response).",
            "<b>And it is the class of bounded loops:</b> every "
            "primitive recursive function is a program whose loops have "
            "bounds computed in advance. <b>No <code>while</code>.</b>",
            "<b>But it misses total computable functions.</b> "
            "<b>Ackermann's function is total, computable, and grows "
            "faster than any primitive recursive function</b> — by a "
            "diagonal argument over the class."]},

  {"t": "code", "kicker": "The gap", "title": "Why bounded loops are not enough",
   "lang": "text", "code": """
  THE PRIMITIVE RECURSIVE functions can be enumerated:
  f_0, f_1, f_2, ...

  Define g(n) = f_n(n) + 1.

  g is total and computable -- enumerate, run, add one.
  And g differs from every f_n at n.
  So g is NOT primitive recursive.
      -- Module 05's diagonalisation, applied to a class
         rather than to all machines.

  ACKERMANN'S FUNCTION is the standard concrete witness,
  and it grows unmanageably fast:
      A(1,n) ~ 2n,   A(2,n) ~ 2^n,
      A(3,n) ~ a tower of 2s,  A(4,2) is already larger
      than the number of particles in the observable
      universe.

  THE LESSON: TOTALITY CANNOT BE GUARANTEED BY SYNTAX
  WITHOUT LOSING EXPRESSIVENESS.
      -- which is exactly the trade a total functional
         language makes (Agda, Idris): every program
         terminates, and some computable total functions
         cannot be written.
""",
   "caption": "<b>Total languages are strictly less expressive, "
              "provably</b> — which is a precise statement of what "
              "a termination guarantee costs.",
   "note": "The Agda connection makes the abstract result concrete."},

  {"t": "section", "label": "Part 2", "title": "Recovering full power",
   "blurb": "One unbounded search."},

  {"t": "callout", "title": "μ-recursion adds unbounded search, and that is exactly the missing piece",
   "kind": "The characterisation",
   "body": ["<b>Add the μ operator: μy.R(x,y) is the "
            "least y such that R(x,y) holds.</b> Search upward from "
            "zero, forever if necessary.",
            "<b>The resulting class — the μ-recursive "
            "functions — is exactly the Turing-computable "
            "functions</b> (Module 01 §2's coincidence, in "
            "this form).",
            "<b>And the μ operator is exactly where "
            "non-termination enters</b> — if no y satisfies R, the "
            "search never ends.",
            "<b>So full computational power costs precisely one "
            "unbounded <code>while</code> loop.</b> <b>The whole "
            "undecidability of the subject is traceable to that single "
            "construct</b>, which is a remarkably clean "
            "localisation."]},

  {"t": "section", "label": "Part 3", "title": "The recursion theorem",
   "blurb": "Every program can refer to itself."},

  {"t": "code", "kicker": "Recursion theorem", "title": "Self-reference is always available",
   "lang": "text", "code": """
  THE RECURSION THEOREM: for any computable function t,
  there is a program p with

      the behaviour of p = t(description of p)

  In other words: you may write a program that uses its own
  source code, and such a program always exists.

  WHY THIS IS NOT OBVIOUS: you cannot simply embed your own
  source in yourself -- that is circular, since embedding
  the text makes the text longer. The theorem says a fixed
  point exists anyway.

  CONSEQUENCES

    QUINES exist -- programs printing their own source.
        Not a party trick; a corollary.
    VIRUSES can copy themselves, for the same reason.
    MODULE 05's PROOF becomes cleaner: build a machine that
        obtains its own description and contradicts the
        decider, with no diagonal construction needed.
    RICE'S THEOREM has a short proof from it.
    AND THE Y COMBINATOR is the lambda-calculus version --
        recursion from a language with no recursion
        (Module 11).

  SELF-REFERENCE IS A THEOREM, NOT A LOOPHOLE.
""",
   "caption": "<b>Self-reference is guaranteed rather than permitted</b> "
              "— which is why Module 05's proof is not a trick and "
              "why quines are inevitable.",
   "note": "Students find the recursion theorem reassuring after "
           "Module 05."},

  {"t": "section", "label": "Part 4", "title": "Describing things",
   "blurb": "Kolmogorov complexity, and a function that outgrows "
            "everything."},

  {"t": "callout", "title": "Kolmogorov complexity: the length of the shortest program that prints it",
   "kind": "A definition of randomness",
   "body": ["<b>K(x) is the length of the shortest program outputting "
            "x.</b> <b>A string is random if K(x) ≈ |x|</b> "
            "— if it has no shorter description than itself.",
            "<b>Most strings are random</b>, by counting: there are "
            "fewer short programs than long strings. <b>So "
            "incompressibility is the norm, not the exception.</b>",
            "<b>And K is uncomputable</b> — by the Berry paradox "
            "made precise: a program that found the shortest program "
            "would itself be a short description of its output.",
            "<b>Which gives a one-line proof that general lossless "
            "compression cannot work</b> and <b>a formal definition of "
            "randomness that does not mention probability</b> — both "
            "of which are worth having."]},

  {"t": "callout", "title": "The busy beaver function grows faster than anything computable",
   "kind": "The most concrete uncomputable function",
   "body": ["<b>BB(n) is the largest number of steps any halting "
            "n-state Turing machine takes.</b> A perfectly well-defined "
            "function of n.",
            "<b>And it is uncomputable</b> — if you could compute "
            "BB(n), you could decide halting for n-state machines by "
            "running them BB(n) steps.",
            "<b>It grows faster than every computable function</b>, "
            "which is a stronger statement than merely being "
            "uncomputable.",
            "<b>And the known values stop almost immediately:</b> "
            "<b>BB(1) through BB(4) are known, BB(5) was settled in "
            "2024 after decades, and BB(6) is known to exceed "
            "10↑↑15</b> — <b>BB(748) is independent of standard "
            "set theory.</b>"]},

  {"t": "bullets", "kicker": "Summary", "title": "What this module establishes",
   "items": [
     "<b>Totality by syntax costs expressiveness, provably</b> "
     "— which is what a total language trades.",
     "",
     "<b>Full power costs exactly one unbounded search</b>, and all "
     "the undecidability traces to it.",
     "",
     "<b>Self-reference is a theorem</b>, so Module 05's construction "
     "was inevitable rather than clever.",
     "",
     "<b>Randomness has a definition that does not mention "
     "probability</b>, and it is uncomputable.",
     "",
     "<b>And uncomputable functions can be perfectly concrete</b> "
     "— BB(5) is a specific number that took sixty years to "
     "find.",
   ],
   "footnote": "<b>BB(748)'s independence from set theory is the "
               "striking fact here:</b> a question about a finite number "
               "that no amount of mathematics can settle."},
 ],
 "takeaways": [
   "Primitive recursive functions are total by construction and are "
   "exactly the bounded-loop programs — and they miss Ackermann's "
   "function, by diagonalisation.",
   "So totality guaranteed by syntax costs expressiveness provably, which "
   "is precisely what a total functional language trades.",
   "μ-recursion adds one unbounded search and recovers exactly the "
   "Turing-computable functions — so all undecidability traces to one "
   "construct.",
   "The recursion theorem guarantees that self-reference is always "
   "available, so quines, viruses, and Module 05's construction are "
   "corollaries.",
   "Kolmogorov complexity defines randomness without mentioning "
   "probability, and it is uncomputable by the Berry paradox made "
   "precise.",
   "The busy beaver function grows faster than every computable function, "
   "and BB(748) is independent of standard set theory.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Primitive recursion"),
  ("callout", "Primitive recursive functions always terminate, and miss "
              "some that do",
   ["<b>Build functions from the constant zero, the successor function, "
    "and the projections, using composition and recursion on a single "
    "argument that decreases.</b> That is the primitive recursive "
    "class.",
    "<b>Every primitive recursive function is total</b> — it "
    "terminates on every input, by construction, since the recursion "
    "always decreases a well-founded measure — <b>so termination is "
    "decidable for this class</b>, trivially, which is Module 05 "
    "&sect;4's restriction response in its purest form.",
    "<b>And it is exactly the class of bounded loops:</b> every "
    "primitive recursive function corresponds to a program whose loop "
    "bounds are computed in advance of entering the loop. <b>No "
    "<code>while</code>, only <code>for</code> with a precomputed "
    "count.</b>",
    "<b>But it misses total computable functions.</b> <b>Ackermann's "
    "function is total, obviously computable, and grows faster than every "
    "primitive recursive function</b> — established by a diagonal "
    "argument over the class (&sect;1's code), which is Module 05's "
    "method applied to a restricted class rather than to all machines."]),
  ("code", """THE PRIMITIVE RECURSIVE functions can be enumerated:
f_0, f_1, f_2, ...

Define g(n) = f_n(n) + 1.

g is total and computable -- enumerate until you reach the
nth, run it on n, add one.
And g differs from every f_n at the input n.
So g is NOT primitive recursive.
    -- Module 05's diagonalisation, applied to a CLASS
       rather than to all machines.

ACKERMANN'S FUNCTION is the standard concrete witness, and
it grows unmanageably fast:
    A(1,n) is about 2n
    A(2,n) is about 2^n
    A(3,n) is a tower of 2s of height n
    A(4,2) already exceeds the number of particles in the
        observable universe

THE LESSON: TOTALITY CANNOT BE GUARANTEED BY SYNTAX WITHOUT
LOSING EXPRESSIVENESS.
    -- which is exactly the trade a total functional
       language makes (Agda, Idris, Coq's terminating
       fragment): every program provably terminates, and
       some computable total functions cannot be
       written."""),
  ("p", "<b>Total languages are strictly less expressive, provably</b> "
        "— <b>which is a precise statement of what a termination "
        "guarantee costs</b>, and a more useful framing than the usual "
        "informal complaint that total languages are awkward. <b>The "
        "awkwardness is a theorem</b>, and the question for a language "
        "designer is whether the functions lost are ones anyone wanted "
        "— which, in practice, they mostly are not."),

  ("h1", "2 &nbsp; Recovering full power"),
  ("callout", "μ-recursion adds unbounded search, and that is exactly "
              "the missing piece",
   ["<b>Add the &mu; operator: &mu;y.R(x,y) is the least y such that "
    "R(x,y) holds.</b> Search upward from zero, testing each candidate, "
    "forever if necessary.",
    "<b>The resulting class — the &mu;-recursive functions — "
    "is exactly the Turing-computable functions</b>, which is "
    "Module 01 &sect;2's coincidence of independent formalisations in "
    "this particular form.",
    "<b>And the &mu; operator is precisely where non-termination "
    "enters</b> — if no y satisfies R, the search runs forever, and "
    "nothing else in the definition can fail to terminate.",
    "<b>So full computational power costs exactly one unbounded "
    "<code>while</code> loop.</b> <b>The entire undecidability of this "
    "subject is traceable to that single construct</b> — which is a "
    "remarkably clean localisation, and it says something about language "
    "design: <b>the construct that makes a language Turing-complete is "
    "the same construct that makes its programs undecidable.</b> You "
    "cannot have one without the other."]),

  ("break",),
  ("h1", "3 &nbsp; The recursion theorem"),
  ("code", """THE RECURSION THEOREM: for any computable function t,
there is a program p with

    the behaviour of p = t(description of p)

In other words: you may write a program that uses its own
source code, and such a program is guaranteed to exist.

WHY THIS IS NOT OBVIOUS: you cannot simply embed your own
source text inside yourself -- that is circular, because
embedding the text makes the text longer, which changes
what must be embedded. The theorem says a fixed point
exists regardless.

CONSEQUENCES

  QUINES exist -- programs that print their own source.
      Not a party trick; a corollary of a theorem.
  VIRUSES can copy themselves, for the same reason.
  MODULE 05's PROOF becomes cleaner: build a machine that
      obtains its own description and then contradicts the
      decider, with no diagonal construction needed at all.
  RICE'S THEOREM has a short proof from it.
  AND THE Y COMBINATOR is the lambda-calculus version --
      recursion obtained in a language that has no
      recursion construct (Module 11 section 1).

SELF-REFERENCE IS A THEOREM, NOT A LOOPHOLE."""),
  ("p", "<b>Self-reference is guaranteed rather than merely "
        "permitted</b> — <b>which is why Module 05's proof is not a "
        "trick</b> (the objection answered there gets its formal answer "
        "here) <b>and why quines are inevitable rather than ingenious.</b> "
        "<b>Students generally find the recursion theorem reassuring "
        "after Module 05</b>, because it converts an uncomfortable "
        "construction into a routine application of a general result."),

  ("h1", "4 &nbsp; Describing things, and growing fast"),
  ("callout", "Kolmogorov complexity: the length of the shortest program "
              "that prints it",
   ["<b>K(x) is the length of the shortest program that outputs x and "
    "halts.</b> <b>A string is <i>random</i> if K(x) is approximately "
    "|x|</b> — that is, if it has no description shorter than itself. "
    "<b>Which is a definition of randomness for an individual object</b>, "
    "something probability theory cannot provide.",
    "<b>Most strings are random</b>, by counting: there are fewer "
    "programs shorter than n bits than there are strings of length n, so "
    "most strings cannot have short descriptions. <b>So "
    "incompressibility is the norm and compressibility the exception</b> "
    "— which is the information-theoretic reason general-purpose "
    "compression works on real files and not on arbitrary ones.",
    "<b>And K is uncomputable</b> — by the Berry paradox made "
    "precise. A program that computed K could find 'the smallest number "
    "not describable in fewer than a thousand bits', which it has just "
    "described in far fewer. <b>Formally: a K-computing program would "
    "itself be a short description of outputs it certifies as having no "
    "short description.</b>",
    "<b>Which gives a one-line proof that no general lossless "
    "compressor can shrink every input</b> (most inputs are "
    "incompressible) <b>and a formal definition of randomness that does "
    "not mention probability at all</b> — both of which are worth "
    "having, and the second connects to CSCE 658's derandomisation "
    "questions."]),
  ("callout", "The busy beaver function grows faster than anything "
              "computable",
   ["<b>BB(n) is the largest number of steps that any halting "
    "n-state Turing machine takes before halting.</b> A perfectly "
    "well-defined function of n — there are finitely many n-state "
    "machines, so the maximum over the halting ones exists.",
    "<b>And it is uncomputable</b> — <b>if you could compute "
    "BB(n), you could decide halting for n-state machines</b> by running "
    "a machine for BB(n) steps and concluding it never halts if it has "
    "not. So BB's uncomputability is immediate from Module 05.",
    "<b>It grows faster than every computable function</b>, which is "
    "strictly stronger than merely being uncomputable — it eventually "
    "exceeds any computable function you care to name.",
    "<b>And the known values stop almost immediately:</b> <b>BB(1) "
    "through BB(4) are small and known, BB(5) = 47,176,870 was "
    "established in 2024 after decades of effort by a distributed "
    "collaboration, and BB(6) is known to exceed 10 to a tower of "
    "15</b> — <b>while BB(748) is independent of standard set "
    "theory</b>, because a 748-state machine can search for a "
    "contradiction in ZFC. <b>A question about one specific finite number "
    "that no amount of mathematics can settle</b>, which is the most "
    "striking fact in this module and a good bridge to Module 10."]),
  ("ul", ["<b>Totality guaranteed by syntax costs expressiveness, "
          "provably</b> — which is what a total language trades "
          "(&sect;1).",
          "<b>Full power costs exactly one unbounded search</b>, and all "
          "of the subject's undecidability traces to it (&sect;2).",
          "<b>Self-reference is a theorem</b>, so Module 05's "
          "construction was inevitable rather than clever (&sect;3).",
          "<b>Randomness has a definition that does not mention "
          "probability</b>, and that definition is uncomputable "
          "(&sect;4).",
          "<b>And uncomputable functions can be perfectly concrete</b> "
          "— <b>BB(5) is a specific integer that took sixty years "
          "to determine</b>, which is a useful corrective to the "
          "impression that uncomputability is about exotic objects."]),
 ],
 "resources": [
   ("Sipser &mdash; sections 6.1–6.2 and 6.4",
    "https://math.mit.edu/~sipser/book.html",
    "<b>The recursion theorem of &sect;3 and an introduction to "
    "&sect;4's Kolmogorov complexity.</b>"),
   ("Li & Vitányi &mdash; An Introduction to Kolmogorov Complexity "
    "and Its Applications",
    "https://link.springer.com/book/10.1007/978-3-030-11298-1",
    "<b>The reference for &sect;4</b>, including the randomness "
    "definition and its applications. Library copy."),
   ("Aaronson &mdash; The Busy Beaver Frontier (free)",
    "https://www.scottaaronson.com/papers/bb.pdf",
    "<b>&sect;4's busy beaver material</b>, including the independence "
    "results and the state of knowledge. Unusually readable."),
   ("The bbchallenge collaboration (free)",
    "https://bbchallenge.org/",
    "<b>The BB(5) proof, completed in 2024</b>, with the whole effort "
    "documented — a good example of what settling one value of an "
    "uncomputable function actually requires."),
 ],
 "exercises": [
   "<b>Write addition, multiplication, and exponentiation</b> as "
   "primitive recursive definitions.",
   "<b>Implement Ackermann's function</b> and compute A(3,n) for n up to "
   "a limit your machine tolerates.",
   "<b>Write out the diagonal argument</b> showing a total computable "
   "function that is not primitive recursive.",
   "<b>Express a μ-recursive function</b> that is not primitive "
   "recursive, and identify where the unbounded search is.",
   "<b>Write a quine</b> in a language of your choice.",
   "<b>Explain, using the recursion theorem, why that was possible.</b>",
   "<b>Re-prove the halting problem using the recursion theorem</b> and "
   "compare against Module 05's proof.",
   "<b>Estimate K(x) for three strings</b> by compressing them, and "
   "explain why compression is only an upper bound.",
   "<b>Prove no compressor shrinks every input</b>, by counting.",
   "<b>Look up the BB(5) result</b> and summarise what the proof had to "
   "establish.",
 ],
 "selfcheck": [
   "Define primitive recursion and say what programs it corresponds "
   "to.",
   "Why is every primitive recursive function total?",
   "Show that it misses a total computable function.",
   "What does a total functional language trade, and is that a theorem?",
   "What does μ add, and what class results?",
   "Where does non-termination enter, and what follows?",
   "State the recursion theorem and say why it is not obvious.",
   "Name five of its consequences.",
   "Define Kolmogorov complexity and explain why it is uncomputable.",
   "Define BB(n), prove it uncomputable, and say what is known.",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Logic and Incompleteness",
 "subtitle": "Gödel, as a corollary.",
 "question": "Can every true statement be proved?",
 "outcomes": [
     "Explain what a formal system is and what provability means.",
     "Derive incompleteness from undecidability.",
     "State both incompleteness theorems precisely.",
     "Explain what they do and do not establish.",
     "Explain the consequences for verification.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Formal systems",
   "blurb": "Axioms, rules, and mechanical checking."},

  {"t": "callout", "title": "A formal system makes provability mechanical, which is the point",
   "kind": "The setup",
   "body": ["<b>Axioms, inference rules, and proofs that are finite "
            "sequences each step of which follows by a rule.</b>",
            "<b>So <i>checking</i> a proof is decidable</b> — it is "
            "a syntactic verification, and that is exactly what makes "
            "formalisation worth the trouble.",
            "<b>Which means the set of provable statements is "
            "recognisable</b> (Module 04 §2): enumerate all "
            "proofs, and every theorem eventually appears.",
            "<b>Recognisable, and the question is whether it is "
            "<i>decidable</i></b> — can you also determine that "
            "something is <i>not</i> provable? <b>That is "
            "incompleteness, in computability terms.</b>"]},

  {"t": "section", "label": "Part 2", "title": "The derivation",
   "blurb": "Incompleteness from halting, in half a page."},

  {"t": "code", "kicker": "The argument", "title": "Why undecidability forces incompleteness",
   "lang": "text", "code": """
  SUPPOSE a formal system F is
      SOUND     -- it proves only true statements
      COMPLETE  -- it proves every true statement
      and strong enough to describe Turing machines

  "M does not halt on w" is a statement about arithmetic
  (Module 09's encoding makes this precise).

  Then a halting decider would exist:
      given (M, w), enumerate ALL proofs in F
      if a proof of "M halts on w" appears, answer YES
      if a proof of "M does not halt on w" appears,
          answer NO

  By COMPLETENESS one of the two is provable, so the search
  terminates. By SOUNDNESS the answer is correct.
  So this procedure DECIDES HALTING.

  But Module 05 proved no such procedure exists.

  THEREFORE: no sound, complete, sufficiently strong formal
  system exists. Any sound system strong enough to talk
  about computation is INCOMPLETE -- there are true
  statements it cannot prove.

  THAT IS GODEL'S FIRST INCOMPLETENESS THEOREM, derived
  from halting in half a page.
""",
   "caption": "<b>Incompleteness is a corollary of undecidability</b> "
              "— which is the cleanest route to it and is why this "
              "module comes after Module 05.",
   "note": "This derivation is the intellectual high point of the "
           "course."},

  {"t": "callout", "title": "And Gödel's original route, for contrast",
   "kind": "The same result, obtained differently",
   "body": ["<b>Gödel, in 1931 and before Turing, built a sentence "
            "asserting its own unprovability</b> — 'this statement "
            "is not provable in F'.",
            "<b>If F proves it, F proves a falsehood "
            "(unsound).</b> <b>If F proves its negation, F proves "
            "something false too.</b> <b>So F proves neither, and the "
            "statement is true and unprovable.</b>",
            "<b>The hard part was arithmetisation</b> — encoding "
            "statements and proofs as numbers so that 'is a proof of' "
            "becomes an arithmetic predicate. <b>Which is "
            "Module 04 §3's encoding, invented five years "
            "earlier for a different purpose.</b>",
            "<b>So both routes are Module 05 §3's "
            "diagonalisation</b> — and <b>Gödel essentially "
            "invented computability theory in order to prove a theorem "
            "about logic</b>, which is why the two subjects are "
            "inseparable."]},

  {"t": "section", "label": "Part 3", "title": "Both theorems",
   "blurb": "Stated carefully, because they are widely misstated."},

  {"t": "table", "kicker": "The theorems", "title": "What they say, precisely",
   "header": ["", "First theorem", "Second theorem"],
   "widths": [2.1, 4.5, 5.4],
   "rows": [
     ["<b>Says</b>", "<b>Any consistent, sufficiently strong, effectively axiomatised system is incomplete</b>", "<b>Such a system cannot prove its own consistency</b>"],
     ["<b>Needs</b>", "<b>Enough arithmetic to encode computation</b>", "<b>The same, plus formalised provability</b>"],
     ["<b>Escape 1</b>", "<b>Weaker systems are complete — e.g. Presburger arithmetic</b>", "<b>A stronger system can prove a weaker one consistent</b>"],
     ["<b>Escape 2</b>", "<b>Non-effective axiom sets are complete — and useless</b>", "<b>Consistency can be assumed, and usually is</b>"],
   ],
   "footnote": "<b>The escapes matter:</b> <b>incompleteness is not a "
               "statement about all mathematics but about systems strong "
               "enough to encode computation and weak enough to be "
               "mechanically checkable.</b>",
   "note": "The escape conditions are what the popular accounts omit."},

  {"t": "callout", "title": "What the theorems do not say",
   "kind": "Correcting the usual misreadings",
   "body": ["<b>They do not say there are truths nobody can ever "
            "know.</b> <b>A statement unprovable in F may be provable "
            "in a stronger system</b>, and routinely is.",
            "<b>They do not say mathematics is broken or arbitrary.</b> "
            "Essentially all working mathematics is provable in standard "
            "set theory.",
            "<b>They do not apply to systems too weak to encode "
            "computation</b> — <b>Presburger arithmetic (addition "
            "without multiplication) is complete and decidable</b>, which "
            "is why SMT solvers can handle it.",
            "<b>And they say nothing about human minds.</b> <b>The "
            "arguments that they do require assuming humans are both "
            "consistent and formalisable</b>, which is precisely what "
            "would need establishing."]},

  {"t": "section", "label": "Part 4", "title": "Consequences",
   "blurb": "For verification, and for this program."},

  {"t": "bullets", "kicker": "Consequences", "title": "What follows for engineering",
   "items": [
     "<b>No verification system can prove every true property</b> "
     "— so a verifier failing to prove something does not mean it "
     "is false.",
     "",
     "<b>Which is why proof assistants are interactive.</b> <b>The "
     "human supplies what no complete automatic procedure could</b> "
     "(Module 08 §2's sound+complete+non-terminating row).",
     "",
     "<b>Decidable logical fragments are therefore valuable</b> "
     "— Presburger, linear arithmetic, bit-vectors, "
     "EPR. <b>This is what SMT solvers are built from.</b>",
     "",
     "<b>And a verified system's guarantee is relative to its "
     "axioms</b>, which include a model of the hardware that may be "
     "wrong.",
     "",
     "<b>So 'proved correct' means 'proved correct relative to this "
     "specification, in this logic, assuming this model'.</b>",
   ],
   "footnote": "<b>That last point is the practical one:</b> every "
               "verification result has a trusted base, and the "
               "interesting question is always what is in it."},

  {"t": "callout", "title": "Why this module is here",
   "kind": "Closing",
   "body": ["<b>Incompleteness is usually taught as a result about "
            "logic and presented as mysterious.</b> <b>Derived from "
            "halting it is neither</b> — it is a corollary, and the "
            "proof fits on one slide.",
            "<b>And the direction of discovery was the reverse:</b> "
            "<b>Gödel's arithmetisation came first, and Turing "
            "formalised computation partly to settle a question "
            "Gödel's work raised.</b>",
            "<b>So the two subjects are one subject.</b> <b>Provability "
            "is a computational notion and computation is a logical "
            "one</b>, and the limits of each are the limits of the "
            "other.",
            "<b>Which is why Module 09's BB(748) result is the right "
            "preparation:</b> <b>a question about a finite number that "
            "standard set theory cannot settle</b> is incompleteness "
            "made as concrete as it gets."]},
 ],
 "takeaways": [
   "A formal system makes proof-checking decidable, so the provable "
   "statements are recognisable — and the question is whether they "
   "are decidable.",
   "Incompleteness follows from undecidability in half a page: a sound and "
   "complete strong system would give a halting decider.",
   "Gödel's original route built a self-referential sentence, and the "
   "hard part was arithmetisation — which is the same encoding idea "
   "as Module 04's.",
   "The theorems require the system to be strong enough to encode "
   "computation and effectively axiomatised, and weaker systems like "
   "Presburger arithmetic are complete.",
   "They do not say there are unknowable truths, that mathematics is "
   "broken, or anything about human minds.",
   "'Proved correct' means 'relative to this specification, in this logic, "
   "assuming this model' — and the trusted base is always the "
   "interesting question.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Formal systems"),
  ("callout", "A formal system makes provability mechanical, which is the "
              "point",
   ["<b>Axioms, inference rules, and proofs that are finite sequences of "
    "statements, each of which follows from earlier ones by a rule.</b> "
    "Nothing in a proof requires insight to <i>check</i>.",
    "<b>So <i>checking</i> a proof is decidable</b> — it is a "
    "purely syntactic verification — <b>and that is exactly what "
    "makes formalisation worth the considerable trouble it takes.</b> A "
    "proof assistant is a proof checker.",
    "<b>Which means the set of provable statements is "
    "recognisable</b> (Module 04 &sect;2): enumerate all finite "
    "strings in order, check each for being a valid proof, and every "
    "theorem eventually appears. <b>Slow, and a genuine enumeration.</b>",
    "<b>Recognisable, and the question is whether it is also "
    "<i>decidable</i></b> — can you determine that a statement is "
    "<i>not</i> provable, in finite time? <b>That is incompleteness "
    "restated in computability terms</b>, and putting it that way is what "
    "makes &sect;2's derivation available."]),

  ("h1", "2 &nbsp; Incompleteness from undecidability"),
  ("code", """SUPPOSE a formal system F is
    SOUND     -- it proves only true statements
    COMPLETE  -- it proves every true statement
    and strong enough to describe Turing machines

"M does not halt on w" is a statement about arithmetic
(Godel's arithmetisation, or Module 09's encodings, make
this precise).

Then a halting decider would exist:
    given (M, w), enumerate ALL proofs in F
    if a proof of "M halts on w" appears, answer YES
    if a proof of "M does not halt on w" appears, answer NO

By COMPLETENESS one of the two statements is true and
therefore provable, so the search terminates.
By SOUNDNESS whichever proof appears is correct.
So this procedure DECIDES HALTING.

But Module 05 proved that no such procedure exists.

THEREFORE: no sound, complete, sufficiently strong formal
system exists. Any sound system strong enough to talk about
computation is INCOMPLETE -- there are true statements it
cannot prove.

THAT IS GODEL'S FIRST INCOMPLETENESS THEOREM, derived from
halting in half a page."""),
  ("p", "<b>Incompleteness is a corollary of undecidability</b> — "
        "<b>which is the cleanest available route to it and is why this "
        "module comes after Module 05 rather than before.</b> <b>It is "
        "also the intellectual high point of the course</b>: a result "
        "usually presented as profound and mysterious becomes a short "
        "argument from a theorem you proved four modules ago."),
  ("callout", "And Gödel's original route, for contrast",
   ["<b>G&ouml;del, in 1931 and five years before Turing, constructed a "
    "sentence asserting its own unprovability</b> — informally, "
    "'this statement is not provable in F'.",
    "<b>If F proves it, then F has proved a false statement, so F is "
    "unsound.</b> <b>If F proves its negation, F has proved that the "
    "statement is provable, which is also false.</b> <b>So F proves "
    "neither, and the statement is true and unprovable in F.</b>",
    "<b>The hard part was <i>arithmetisation</i></b> — encoding "
    "statements, proofs, and the relation 'is a proof of' as arithmetic "
    "predicates about numbers, so that the system could talk about its own "
    "syntax. <b>Which is Module 04 &sect;3's programs-as-data "
    "encoding, invented independently and five years earlier, for a "
    "different purpose.</b>",
    "<b>So both routes are Module 05 &sect;3's diagonalisation</b> "
    "— construct the object that differs from everything the "
    "enumeration covers — and <b>G&ouml;del essentially invented the "
    "techniques of computability theory in order to prove a theorem about "
    "logic.</b> <b>Which is why the two subjects are inseparable</b>, and "
    "why Turing's paper five years later reads as a continuation."]),

  ("break",),
  ("h1", "3 &nbsp; Both theorems, stated carefully"),
  ("table", ["", "First incompleteness theorem",
             "Second incompleteness theorem"],
   [["<b>What it says</b>",
     "<b>Any consistent, sufficiently strong, effectively axiomatised "
     "formal system is incomplete — there are true statements of its "
     "language it cannot prove.</b>",
     "<b>Any such system cannot prove its own consistency.</b>"],
    ["<b>What it requires</b>",
     "<b>Enough arithmetic to encode computation, and an effectively "
     "enumerable axiom set</b> — both conditions are essential.",
     "<b>The same conditions, plus the ability to formalise provability "
     "inside the system.</b>"],
    ["<b>Escape route 1</b>",
     "<b>Weaker systems are complete</b> — Presburger arithmetic "
     "(addition without multiplication) is complete <i>and</i> decidable, "
     "and so is the first-order theory of the reals.",
     "<b>A stronger system can prove a weaker one consistent</b> "
     "— set theory proves arithmetic consistent, and the regress "
     "simply continues upward."],
    ["<b>Escape route 2</b>",
     "<b>A non-effective axiom set is complete</b> — take all true "
     "arithmetic statements as axioms. <b>And useless</b>, since you "
     "cannot recognise an axiom.",
     "<b>Consistency can be assumed rather than proved, and in practice "
     "always is</b> — which is what a trusted base amounts to "
     "(&sect;4)."]],
   [0.16, 0.42, 0.42]),
  ("p", "<b>The escape conditions matter and are exactly what popular "
        "accounts omit.</b> <b>Incompleteness is not a statement about "
        "all of mathematics; it is a statement about systems strong enough "
        "to encode computation and weak enough to be mechanically "
        "checkable</b> — and that pair of conditions is what the "
        "theorem is really about."),
  ("callout", "What the theorems do not say",
   ["<b>They do not say there are truths nobody can ever know.</b> <b>A "
    "statement unprovable in F may be perfectly provable in a stronger "
    "system</b>, and routinely is — Goodstein's theorem is "
    "unprovable in Peano arithmetic and provable in set theory, which is "
    "an ordinary mathematical situation rather than a limit on knowledge.",
    "<b>They do not say mathematics is broken, arbitrary, or "
    "unreliable.</b> <b>Essentially all working mathematics is provable "
    "in standard set theory</b>, and the independent statements are "
    "mostly carefully constructed or drawn from set theory itself.",
    "<b>They do not apply to systems too weak to encode "
    "computation.</b> <b>Presburger arithmetic is complete and "
    "decidable</b> — <b>which is precisely why SMT solvers can "
    "handle linear integer arithmetic and cannot handle general "
    "arithmetic</b> (CSCE 625 Module 08 &sect;4's decidable fragments), "
    "so the escape route is a load-bearing engineering fact rather than a "
    "technicality.",
    "<b>And they say nothing whatsoever about human minds.</b> <b>The "
    "arguments that they establish something about human intelligence "
    "require assuming that humans are both consistent and "
    "formalisable</b> — <b>which is precisely what would have needed "
    "establishing</b>, so the argument assumes its conclusion. This is "
    "worth being able to state, because the claim is common."]),

  ("h1", "4 &nbsp; Consequences for engineering"),
  ("ul", ["<b>No verification system can prove every true property</b> "
          "of the programs in its scope — <b>so a verifier's failure "
          "to prove something does not mean it is false</b>, and treating "
          "a failed proof as a bug report is a category error.",
          "<b>Which is why proof assistants are interactive rather than "
          "automatic.</b> <b>The human supplies the search that no "
          "complete automatic procedure could perform</b> — which is "
          "<b>Module 08 &sect;2's sound-and-complete-but-not-"
          "terminating row</b>, and it is the only position that gets "
          "both soundness and completeness.",
          "<b>So decidable logical fragments are extremely "
          "valuable.</b> Presburger arithmetic, linear real arithmetic, "
          "bit-vectors, arrays, uninterpreted functions, the "
          "effectively-propositional fragment. <b>This is what SMT "
          "solvers are assembled from</b>, and the engineering is in "
          "staying inside the decidable parts.",
          "<b>And a verified system's guarantee is relative to its "
          "axioms</b>, which include a formal model of the hardware, the "
          "compiler, and the specification — any of which may be "
          "wrong. <b>A proof about a model is not a proof about a "
          "machine.</b>",
          "<b>So 'proved correct' means 'proved correct relative to this "
          "specification, in this logic, assuming this model of the "
          "machine'.</b> <b>That is the practical consequence:</b> every "
          "verification result has a trusted base, <b>and the interesting "
          "question is always what is in it</b> — which is this "
          "program's state-your-assumptions discipline in the one subject "
          "where the assumptions are axioms."]),
  ("callout", "Why this module is here",
   ["<b>Incompleteness is usually taught as a result about logic and "
    "presented as mysterious.</b> <b>Derived from halting it is "
    "neither</b> — it is a corollary, and &sect;2's proof fits on a "
    "slide.",
    "<b>And the historical direction of discovery was the "
    "reverse:</b> <b>G&ouml;del's arithmetisation came first, and Turing "
    "formalised computation partly to settle a question that G&ouml;del's "
    "work had raised</b> (Hilbert's decision problem for first-order "
    "logic). <b>The corollary is older than the theorem it follows "
    "from.</b>",
    "<b>So the two subjects are one subject.</b> <b>Provability is a "
    "computational notion — it is recognisability (&sect;1) — "
    "and computation is a logical one</b>, and the limits of each are the "
    "limits of the other.",
    "<b>Which is why Module 09 &sect;4's BB(748) result is the right "
    "preparation:</b> <b>a question about one specific finite integer "
    "that standard set theory cannot settle</b> is incompleteness made as "
    "concrete as it is possible to make it, and it removes any suspicion "
    "that the phenomenon concerns only artificial self-referential "
    "sentences."]),
 ],
 "resources": [
   ("Sipser &mdash; section 6.2",
    "https://math.mit.edu/~sipser/book.html",
    "<b>&sect;2's derivation of incompleteness from undecidability</b>, "
    "which is the route this module takes."),
   ("Smith &mdash; An Introduction to Gödel's Theorems (free study "
    "guide)",
    "https://www.logicmatters.net/igt/",
    "<b>The careful treatment of &sect;3</b>, with the conditions stated "
    "properly. The author's free Teach Yourself Logic guide is also "
    "excellent."),
   ("Nagel & Newman &mdash; Gödel's Proof",
    "https://nyupress.org/9780814758373/godels-proof/",
    "<b>The short classic account of &sect;2's original route</b>, "
    "including arithmetisation. Library copy, and under 150 pages."),
   ("Franzén &mdash; Gödel's Theorem: An Incomplete Guide to "
    "Its Use and Abuse",
    "https://www.routledge.com/Godels-Theorem-An-Incomplete-Guide-to-Its-Use-and-Abuse/Franzen/p/book/9781568812380",
    "<b>&sect;3's callout, at book length</b> — the standard "
    "correction of the misreadings, and worth reading before citing the "
    "theorems anywhere."),
 ],
 "exercises": [
   "<b>Write out the derivation of incompleteness from halting</b> in "
   "your own words.",
   "<b>Identify exactly which steps use soundness and which use "
   "completeness.</b>",
   "<b>Explain why the provable statements are recognisable</b> and what "
   "it would take for them to be decidable.",
   "<b>State both theorems precisely</b>, including every condition.",
   "<b>For each condition, give a system that fails it</b> and is "
   "therefore complete.",
   "<b>Use an SMT solver on Presburger arithmetic</b> and then on a "
   "formula requiring multiplication. Report what happens.",
   "<b>Find a popular claim about Gödel's theorems</b> and assess it "
   "against &sect;3's callout.",
   "<b>Take a verified system</b> (seL4, CompCert) and find its stated "
   "trusted base.",
   "<b>List what is in that base</b> and what could be wrong in each "
   "item.",
   "<b>Write the honest form of 'proved correct'</b> for a verification "
   "you would want to perform.",
 ],
 "selfcheck": [
   "What makes proof-checking decidable, and what does that imply about "
   "provability?",
   "Derive incompleteness from undecidability.",
   "Where do soundness and completeness each enter the argument?",
   "Describe Gödel's original route and name the hard part.",
   "State both theorems with their conditions.",
   "Give two escape routes for each.",
   "Name four things the theorems do not say.",
   "Why can SMT solvers handle linear arithmetic?",
   "What does 'proved correct' actually mean?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Other Models",
 "subtitle": "The same class, reached many ways.",
 "question": "Why do all the definitions agree?",
 "outcomes": [
     "Explain the lambda calculus and its equivalence.",
     "Explain universality in cellular automata.",
     "Explain minimal Turing-complete systems.",
     "Explain what quantum computation changes and what it does "
     "not.",
     "Explain hypercomputation proposals and what they assume.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Lambda calculus",
   "blurb": "Functions and nothing else."},

  {"t": "code", "kicker": "Lambda calculus", "title": "Three rules, and everything follows",
   "lang": "text", "code": """
  THE ENTIRE SYNTAX:
      x                  a variable
      (lambda x . M)     a function
      (M N)              an application

  THE ONLY RULE: beta reduction.
      ((lambda x . M) N)  ->  M with N substituted for x

  NO numbers. NO booleans. NO data structures. NO
  recursion construct. NO state.

  AND IT IS TURING COMPLETE.

  CHURCH NUMERALS: represent n as the function applying f
  n times.  2 = lambda f x . f (f x)
  BOOLEANS: true = lambda a b . a ;  false = lambda a b . b
  PAIRS, lists, trees: all encodable as functions.
  RECURSION: the Y COMBINATOR, which is the recursion
      theorem's fixed point (Module 09 Part 3) made
      syntactic.

  WHY IT MATTERS TO YOU: this is the foundation of every
  functional language, and of the typed core of every
  language with closures. Your lambda expression is this,
  and so is the theory behind CSCE 605's type checking.
""",
   "caption": "<b>Turing completeness from function application "
              "alone</b> — which is why 'what is the minimal "
              "sufficient mechanism' has such a surprising answer.",
   "note": "The Y combinator as the recursion theorem is the connection "
           "to make."},

  {"t": "section", "label": "Part 2", "title": "Universality from nothing",
   "blurb": "Systems with no control flow at all."},

  {"t": "table", "kicker": "Minimal", "title": "Turing-complete systems with almost no features",
   "header": ["System", "Has", "Note"],
   "widths": [2.8, 4.0, 5.2],
   "rows": [
     ["<b>Two-counter machine</b>", "<b>Increment, decrement, test zero</b>", "<b>Minsky. Two counters suffice</b>"],
     ["<b>Rule 110</b>", "<b>A 1D cellular automaton, one rule</b>", "<b>Cook, 2004. No control flow at all</b>"],
     ["<b>Game of Life</b>", "<b>A 2D automaton, four rules</b>", "<b>Gliders as signals; a built universal machine</b>"],
     ["<b>Tag systems</b>", "<b>Delete from the front, append by rule</b>", "<b>Post. Two symbols suffice</b>"],
     ["<b>SKI combinators</b>", "<b>Three constants, application</b>", "<b>No variables at all</b>"],
     ["<b>Magic: The Gathering</b>", "<b>Published card interactions</b>", "<b>Genuinely proved, 2019</b>"],
   ],
   "footnote": "<b>Universality is cheap</b>, which is a useful warning: "
               "<b>any sufficiently expressive configuration language, "
               "template system, or rule engine is probably "
               "Turing-complete</b>, and therefore undecidable.",
   "note": "The practical warning about configuration languages is the "
           "takeaway."},

  {"t": "callout", "title": "Accidental Turing completeness is a real engineering hazard",
   "kind": "The practical consequence",
   "body": ["<b>If your configuration format, template language, or "
            "rule engine is Turing-complete, then whether a config "
            "terminates is undecidable</b> — and you have built a "
            "programming language by accident.",
            "<b>It has happened repeatedly:</b> C++ templates, "
            "<code>sendmail</code> configuration, spreadsheet formulas "
            "with iteration, and several build systems.",
            "<b>The symptom is a config that hangs, or a build that "
            "does not terminate</b> — and no static check can rule it "
            "out, by Module 05.",
            "<b>So design deliberately for weakness.</b> <b>A "
            "non-Turing-complete config language can be analysed, "
            "validated, and bounded</b> — which is Module 03 "
            "§4's weakest-sufficient-model principle, with "
            "teeth."]},

  {"t": "section", "label": "Part 3", "title": "Quantum",
   "blurb": "What it changes, precisely."},

  {"t": "callout", "title": "Quantum computation changes the speed, not the class",
   "kind": "Stated carefully, because it is widely misstated",
   "body": ["<b>A quantum computer computes exactly the same functions "
            "as a Turing machine.</b> It can be simulated classically, "
            "with exponential slowdown.",
            "<b>So it does not decide the halting problem, and no "
            "undecidability result in this course is affected.</b> "
            "<b>Not even slightly.</b>",
            "<b>What changes is complexity.</b> <b>BQP is believed to "
            "exceed P</b> — Shor's factoring algorithm is the "
            "evidence — <b>which is CSCE 637 and CSCE 640's "
            "subject.</b>",
            "<b>And the Church–Turing thesis is "
            "untouched</b>, while the <i>extended</i> thesis (that "
            "everything physical is efficiently simulable classically) "
            "is what quantum computing challenges. <b>Two different "
            "claims.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Hypercomputation",
   "blurb": "Proposals to exceed the class, and what each assumes."},

  {"t": "bullets", "kicker": "Proposals", "title": "Ways to compute more, and what each requires",
   "items": [
     "<b>An oracle.</b> <b>Works, trivially</b> "
     "(Module 07 §1) — and assumes you have one, "
     "which is the entire question.",
     "",
     "<b>Infinitely many steps in finite time</b> (Zeno machines, "
     "relativistic computation). <b>Requires unbounded energy density "
     "or exotic spacetime.</b>",
     "",
     "<b>Infinite precision real numbers.</b> <b>Assumes a physical "
     "quantity can carry infinite information</b>, which thermodynamics "
     "disputes.",
     "",
     "<b>Analog computation.</b> Looks promising and <b>reduces to the "
     "previous item</b> once noise is modelled.",
     "",
     "<b>And a true random source.</b> <b>Does not help</b> — "
     "randomness does not add computability, only speed "
     "(CSCE 658).",
   ],
   "footnote": "<b>The pattern is that every proposal assumes an "
               "infinity somewhere</b> — infinite precision, "
               "infinite energy, or infinite time compressed — and "
               "that is what makes the thesis robust."},

  {"t": "callout", "title": "Why the agreement of the models is the real result",
   "kind": "Closing the module",
   "body": ["<b>Every reasonable definition of computation, proposed "
            "for different reasons across ninety years, defines the same "
            "class.</b>",
            "<b>And wildly dissimilar systems reach it</b> — "
            "function application, cellular automata, two counters, a "
            "card game — <b>which suggests the class is a natural "
            "object rather than an artefact of any formalism.</b>",
            "<b>So the impossibility results of this course are about "
            "computation</b>, not about Turing machines — which is "
            "what makes them worth a semester.",
            "<b>And the engineering lesson is the other way "
            "round:</b> <b>universality is cheap, so weakness must be "
            "designed for deliberately</b> (Part 2) if you want a "
            "language you can analyse."]},
 ],
 "takeaways": [
   "The lambda calculus has three syntactic forms and one rule, no "
   "numbers, no recursion construct, and no state — and it is Turing "
   "complete.",
   "The Y combinator is the recursion theorem's fixed point made "
   "syntactic, which is why recursion is available in a language without "
   "it.",
   "Universality is cheap: two counters, one cellular automaton rule, or a "
   "card game suffices.",
   "So accidental Turing completeness is a real hazard — a "
   "Turing-complete config language makes termination undecidable, and it "
   "has happened repeatedly.",
   "Quantum computation changes the complexity and not the class, so no "
   "undecidability result here is affected at all.",
   "Every hypercomputation proposal assumes an infinity somewhere, which "
   "is what makes the Church–Turing thesis robust.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The lambda calculus"),
  ("code", """THE ENTIRE SYNTAX:
    x                  a variable
    (lambda x . M)     a function
    (M N)              an application

THE ONLY RULE: beta reduction.
    ((lambda x . M) N)  ->  M with N substituted for x

NO numbers. NO booleans. NO data structures. NO recursion
construct. NO state. NO control flow.

AND IT IS TURING COMPLETE.

CHURCH NUMERALS: represent n as the function that applies
    f n times.    2 = lambda f x . f (f x)
BOOLEANS: true = lambda a b . a ; false = lambda a b . b
    and then if-then-else is just application
PAIRS, lists, trees: all encodable as functions
RECURSION: the Y COMBINATOR, which is the recursion
    theorem's fixed point (Module 09 section 3) made
    syntactic -- a term Y with Y f = f (Y f)

WHY IT MATTERS TO YOU: this is the foundation of every
functional language and of the typed core of every language
with closures. Your lambda expression is literally this,
and the theory behind CSCE 605's type checking is the typed
version of it."""),
  ("p", "<b>Turing completeness from function application alone</b> "
        "— <b>which is why 'what is the minimal sufficient "
        "mechanism for computation' has such a surprising answer</b>, and "
        "why the coincidence of Module 01 &sect;2 is evidence rather "
        "than coincidence. <b>Church and Turing's formalisms could hardly "
        "look less alike, and they define the same functions.</b>"),

  ("h1", "2 &nbsp; Universality from almost nothing"),
  ("table", ["System", "What it has", "Note"],
   [["<b>Two-counter machine</b>",
     "<b>Two unbounded counters; increment, decrement, test for "
     "zero.</b>",
     "<b>Minsky. Two counters suffice; one does not.</b>"],
    ["<b>Rule 110</b>",
     "<b>A one-dimensional cellular automaton with a single local "
     "rule.</b>",
     "<b>Proved universal by Cook, 2004. No control flow, no memory "
     "addressing, no instructions at all.</b>"],
    ["<b>Conway's Game of Life</b>",
     "<b>A two-dimensional automaton with four rules.</b>",
     "<b>Gliders act as signals, and a full universal machine has been "
     "constructed within it.</b>"],
    ["<b>Tag systems</b>",
     "<b>Delete symbols from the front of a string and append according "
     "to a rule.</b>",
     "<b>Post. Two symbols and a deletion number of two suffice.</b>"],
    ["<b>SKI combinator calculus</b>",
     "<b>Three constants and application.</b>",
     "<b>No variables at all</b> — the lambda calculus with "
     "variables eliminated."],
    ["<b>Magic: The Gathering</b>",
     "<b>Published card interactions, in a legal game state.</b>",
     "<b>Genuinely proved Turing-complete, 2019</b>, which makes certain "
     "questions about a game state undecidable."]],
   [0.22, 0.36, 0.42]),
  ("p", "<b>Universality is cheap</b>, which is a genuinely useful "
        "warning rather than a curiosity: <b>any sufficiently expressive "
        "configuration language, template system, macro facility, or rule "
        "engine is probably Turing-complete</b>, and therefore every "
        "interesting question about it is undecidable (Module 06 "
        "&sect;2)."),
  ("callout", "Accidental Turing completeness is a real engineering hazard",
   ["<b>If your configuration format, template language, or rule engine "
    "turns out to be Turing-complete, then whether a given configuration "
    "terminates is undecidable</b> — <b>and you have built a "
    "programming language by accident, without a debugger, a profiler, or "
    "a specification.</b>",
    "<b>It has happened repeatedly and consequentially:</b> C++ "
    "templates (discovered rather than designed), "
    "<code>sendmail</code> configuration, spreadsheet formulas with "
    "iterative calculation enabled, several build systems, and a number "
    "of policy and markup languages.",
    "<b>The symptom is a configuration that hangs, or a build that does "
    "not terminate</b> — <b>and no static check can rule it out</b>, "
    "by Module 05. The problem cannot be fixed by better tooling, only "
    "by changing the language.",
    "<b>So design deliberately for weakness.</b> <b>A "
    "non-Turing-complete configuration language can be statically "
    "analysed, validated, bounded, and optimised</b> — which is "
    "<b>Module 03 &sect;4's weakest-sufficient-model principle with "
    "real teeth</b>, and is why formats like Dhall and Starlark are "
    "deliberately restricted. <b>Expressiveness is not free, and the "
    "price is paid in analysability.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Quantum computation"),
  ("callout", "Quantum computation changes the speed, not the class",
   ["<b>A quantum computer computes exactly the same functions as a "
    "Turing machine.</b> <b>It can be simulated classically</b>, with "
    "exponential slowdown, by tracking the amplitudes — so the "
    "computable functions are unchanged.",
    "<b>So it does not decide the halting problem, and no undecidability "
    "result in this course is affected.</b> <b>Not partially, not in "
    "some cases, not in principle</b> — the class of computable "
    "functions is identical.",
    "<b>What changes is complexity.</b> <b>BQP, the class of problems "
    "solvable in polynomial quantum time, is believed to strictly exceed "
    "P</b> — Shor's factoring algorithm is the main evidence "
    "— <b>which is CSCE 637 and CSCE 640's subject rather than "
    "this one.</b>",
    "<b>And the Church–Turing thesis is untouched</b>, while the "
    "<i>extended</i> Church–Turing thesis — that every "
    "physical process can be <i>efficiently</i> simulated classically "
    "— <b>is what quantum computing challenges.</b> <b>These are "
    "two different claims and conflating them is the usual error</b>: "
    "quantum computing is evidence against the second and says nothing "
    "about the first."]),

  ("h1", "4 &nbsp; Hypercomputation"),
  ("ul", ["<b>An oracle.</b> <b>Works, trivially</b> (Module 07 "
          "&sect;1) — <b>and assumes you have one</b>, which is the "
          "entire question rather than an answer to it. The oracle is a "
          "mathematical device for comparing difficulties, not a "
          "proposal.",
          "<b>Infinitely many steps in finite time</b> — Zeno "
          "machines that halve the time per step, or relativistic "
          "computation using time dilation near a rotating black hole. "
          "<b>Requires unbounded energy density, or spacetime geometry "
          "nobody has access to.</b>",
          "<b>Infinite precision real numbers as state.</b> <b>Assumes "
          "a physical quantity can carry infinite information</b>, which "
          "thermodynamics and the Bekenstein bound both dispute — "
          "and which, if granted, makes the result unsurprising.",
          "<b>Analog computation.</b> Looks promising, and <b>reduces to "
          "the previous item once measurement noise is modelled</b> "
          "— the extra power comes entirely from the assumed "
          "precision, and vanishes with any finite noise floor.",
          "<b>And a true random source.</b> <b>Does not help</b> "
          "— <b>randomness does not add computability, only "
          "speed</b> (and possibly not even that, which is CSCE 658's "
          "derandomisation question). A randomised machine computes the "
          "same functions.",
          "<b>The pattern is that every proposal assumes an infinity "
          "somewhere</b> — infinite precision, infinite energy, or "
          "infinitely many steps compressed into finite time — "
          "<b>and that regularity is a substantial part of why the "
          "Church–Turing thesis is robust after ninety years.</b>"]),
  ("callout", "Why the agreement of the models is the real result",
   ["<b>Every reasonable definition of computation, proposed for "
    "different reasons by different people across ninety years, defines "
    "exactly the same class of functions.</b>",
    "<b>And wildly dissimilar systems reach it</b> — pure function "
    "application, a one-dimensional cellular automaton, two counters, a "
    "string-rewriting system, a trading card game — <b>which "
    "suggests the class is a natural mathematical object rather than an "
    "artefact of any particular formalism.</b>",
    "<b>So the impossibility results of this course are about "
    "computation itself</b>, not about Turing machines — <b>which is "
    "what makes them worth a semester</b> and what makes Module 05's "
    "permanence claim defensible.",
    "<b>And the engineering lesson runs the other way round:</b> "
    "<b>universality is cheap, so weakness has to be designed for "
    "deliberately</b> (&sect;2) <b>if you want a language whose programs "
    "you can analyse.</b> <b>The two halves of this module are the same "
    "fact read in opposite directions</b>, and the second is the one you "
    "will use."]),
 ],
 "resources": [
   ("Barendregt &mdash; The Lambda Calculus; and Pierce's TAPL "
    "chapter 5",
    "https://www.cis.upenn.edu/~bcpierce/tapl/",
    "<b>&sect;1's calculus</b>, with Pierce's treatment being the right "
    "entry point for a programmer."),
   ("Cook &mdash; Universality in Elementary Cellular Automata (free)",
    "https://wpmedia.wolfram.com/sites/13/2018/02/15-1-1.pdf",
    "<b>&sect;2's Rule 110 result</b>, which is remarkable and "
    "surprisingly readable."),
   ("Churchill, Biderman & Herrick &mdash; Magic: The Gathering is "
    "Turing Complete (free)",
    "https://arxiv.org/abs/1904.09828",
    "<b>&sect;2's last row</b>, done properly — and a good "
    "illustration of how little a system needs."),
   ("Aaronson &mdash; NP-complete Problems and Physical Reality (free)",
    "https://www.scottaaronson.com/papers/npcomplete.pdf",
    "<b>&sect;3 and &sect;4 assessed carefully</b> — what physics "
    "does and does not offer computation, including every proposal in "
    "&sect;4."),
 ],
 "exercises": [
   "<b>Implement a lambda calculus interpreter</b> with beta reduction "
   "and capture-avoiding substitution.",
   "<b>Define Church numerals and addition</b> and verify 2 + 3.",
   "<b>Define booleans and if-then-else</b> as lambda terms.",
   "<b>Implement the Y combinator</b> and use it to write factorial "
   "without a recursion construct.",
   "<b>Relate Y to the recursion theorem</b> in writing.",
   "<b>Implement a two-counter machine</b> and simulate a small Turing "
   "machine on it.",
   "<b>Build a glider gun in the Game of Life</b> and describe how "
   "signals compose.",
   "<b>Determine whether a configuration language you use is "
   "Turing-complete</b>, and say how you decided.",
   "<b>Write a configuration that does not terminate</b>, if it is.",
   "<b>Pick one hypercomputation proposal</b> and identify precisely "
   "where the infinity is assumed.",
 ],
 "selfcheck": [
   "Give the lambda calculus's syntax and its single rule.",
   "How are numbers, booleans, and recursion obtained?",
   "What is the Y combinator, in Module 09's terms?",
   "Name six Turing-complete systems and what each has.",
   "Why is accidental Turing completeness a hazard, and what is the "
   "response?",
   "What does quantum computation change, and what does it not?",
   "Distinguish the Church–Turing thesis from its extended "
   "version.",
   "Name five hypercomputation proposals and the assumption behind "
   "each.",
   "Why is the agreement of the models the real result?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "The Engineering Response",
 "subtitle": "What to do about an undecidable problem.",
 "question": "The question is undecidable. Now what?",
 "outcomes": [
     "Name the four strategies and choose between them.",
     "Explain abstract interpretation and soundness by "
     "construction.",
     "Explain the certificate strategy and its trade.",
     "Design an analysis with a stated soundness position.",
     "Explain why the choice is a product decision.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The four strategies",
   "blurb": "And every tool uses at least one."},

  {"t": "table", "kicker": "Strategies", "title": "Four ways to live with undecidability",
   "header": ["Strategy", "Give up", "Example"],
   "widths": [2.8, 3.6, 5.4],
   "rows": [
     ["<b>Approximate</b>", "<b>Precision</b>", "<b>Abstract interpretation; type systems</b>"],
     ["<b>Restrict the input</b>", "<b>Expressiveness</b>", "<b>Total languages; non-Turing configs</b>"],
     ["<b>Bound a resource</b>", "<b>Coverage</b>", "<b>Bounded model checking; gas; timeouts</b>"],
     ["<b>Demand a certificate</b>", "<b>Automation</b>", "<b>Proof-carrying code; Rust lifetimes; proof assistants</b>"],
   ],
   "footnote": "<b>Each gives up something different</b>, which is why "
               "they combine — a real tool typically uses two or "
               "three at once, and stating which is what makes its output "
               "interpretable.",
   "note": "This table is the practical core of the course."},

  {"t": "callout", "title": "Approximation can be sound by construction",
   "kind": "The idea behind abstract interpretation",
   "body": ["<b>Instead of computing exact values, compute an "
            "over-approximation.</b> Instead of 'x = 7', compute "
            "'x ∈ [0, 10]' or 'x is positive'.",
            "<b>Design the abstract domain and operations so that the "
            "abstract result always contains the concrete one</b> "
            "— then <b>soundness is a property of the construction "
            "rather than something to test.</b>",
            "<b>And the analysis terminates because the abstract domain "
            "has finite height</b>, or a widening operator forces "
            "convergence. <b>Termination is also built in.</b>",
            "<b>So you get sound and terminating, and lose "
            "precision</b> — <b>which is Module 08 §2's "
            "pick-two, with the loss located in a place you can measure "
            "and tune.</b>"]},

  {"t": "code", "kicker": "Abstract interpretation", "title": "The machinery, concretely",
   "lang": "text", "code": """
  CONCRETE: x = 5; y = 3; z = x + y;      -> z = 8

  ABSTRACT, with the SIGN domain:
      x : positive
      y : positive
      z : positive + positive = positive

  The abstract result is correct and less informative, and
  it was computed WITHOUT running the program.

  THE DESIGN OBLIGATIONS
      a DOMAIN (signs, intervals, octagons, polyhedra)
      a TRANSFER FUNCTION per operation, over-approximating
      a JOIN for merging branches
          positive join negative = unknown
      and WIDENING for loops, forcing convergence
          [0,1] then [0,2] then [0,3] ... widen to
          [0, infinity]

  PRECISION IS A DIAL: signs are cheap and coarse,
  intervals better, octagons (x - y <= c) better again,
  polyhedra precise and expensive.

  ASTREE verified absence of runtime errors in Airbus
  flight control code with this. Sound, terminating, and
  it required engineers to tune the domains per module.
""",
   "caption": "<b>Precision is a tunable dial and soundness is not</b> "
              "— which is exactly the right place to put the "
              "engineering effort.",
   "note": "The Astree result is the proof this approach scales."},

  {"t": "section", "label": "Part 2", "title": "Restriction and bounding",
   "blurb": "The other two, briefly."},

  {"t": "bullets", "kicker": "Restriction", "title": "Give up expressiveness, gain decidability",
   "items": [
     "<b>Total functional languages.</b> Agda, Idris. "
     "<b>Termination guaranteed, and some computable functions cannot "
     "be written</b> (Module 09 §1).",
     "",
     "<b>Non-Turing-complete configuration.</b> Dhall, Starlark. "
     "<b>Deliberate weakness</b> (Module 11 §2).",
     "",
     "<b>Decidable logical fragments.</b> Presburger, linear "
     "arithmetic, bit-vectors — which is how SMT solvers are "
     "built (Module 10 §4).",
     "",
     "<b>Structured programming.</b> <b>Bounded loops and no "
     "<code>goto</code> make many analyses easy</b> — which is a "
     "retrospective theoretical justification for a style argument.",
     "",
     "<b>And type systems themselves</b>, which restrict what can be "
     "expressed in order to decide something about it.",
   ],
   "footnote": "<b>Restriction is the most underused strategy</b>, "
               "because it must be chosen at design time — and it is "
               "the only one that makes the problem genuinely go away."},

  {"t": "callout", "title": "Bounding is the easiest and the most honest",
   "kind": "If you state the bound",
   "body": ["<b>Unroll loops k times; explore to depth d; stop after t "
            "seconds.</b> <b>The bounded question is decidable, always, "
            "by Module 06 §2.</b>",
            "<b>And the claim is clean <i>if you state the "
            "bound</i>:</b> 'no error within 20 steps' is a complete, "
            "checkable, useful statement.",
            "<b>The failure mode is reporting the bounded result as "
            "unbounded</b> — which Module 08 §3 flagged, and "
            "which is a documentation failure rather than a technical "
            "one.",
            "<b>And it composes with the others:</b> <b>bounded "
            "abstract interpretation, bounded search over a restricted "
            "language</b> — <b>real tools stack them.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Certificates",
   "blurb": "Make someone else find the proof."},

  {"t": "callout", "title": "If finding the proof is undecidable, checking one is not",
   "kind": "The asymmetry to exploit",
   "body": ["<b>Module 04 §2's recognisability means a proof "
            "can be <i>checked</i> mechanically even when it cannot be "
            "<i>found</i>.</b>",
            "<b>So demand the proof as input.</b> <b>Proof-carrying "
            "code, verified compilers' certificates, dependently typed "
            "programs, and Rust's lifetime annotations are all "
            "this.</b>",
            "<b>The cost is that a human or a separate tool must "
            "produce it</b> — which is real work and is why "
            "verification is expensive.",
            "<b>And the gain is a sound and complete checker</b> "
            "— <b>the only position that gets both, because the "
            "search has been moved outside the tool.</b> <b>That is the "
            "whole trade.</b>"]},

  {"t": "table", "kicker": "Certificates", "title": "Who produces the certificate",
   "header": ["Approach", "Certificate", "Produced by"],
   "widths": [2.9, 3.8, 5.1],
   "rows": [
     ["<b>Rust ownership</b>", "<b>Lifetime annotations</b>", "<b>The programmer, partly inferred</b>"],
     ["<b>Dependent types</b>", "<b>The type itself</b>", "<b>The programmer</b>"],
     ["<b>Proof-carrying code</b>", "<b>A machine-checkable proof</b>", "<b>A compiler, or a prover</b>"],
     ["<b>Verified compilation</b>", "<b>A translation validation</b>", "<b>The compiler, per compilation</b>"],
     ["<b>SAT unsat proofs</b>", "<b>A DRAT refutation</b>", "<b>The solver</b> (CSCE 625 §08)"],
   ],
   "footnote": "<b>The solver-produced certificate is the best case:</b> "
               "<b>the tool does the work and emits something an "
               "independent checker can verify</b>, so you need not trust "
               "the tool.",
   "note": "The independent-checker point is the real value of "
           "certificates."},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "It is a product decision, not a technical one."},

  {"t": "callout", "title": "Which strategy depends on what a wrong answer costs",
   "kind": "The decision",
   "body": ["<b>A missed bug is catastrophic (avionics, medical, "
            "cryptography)?</b> <b>Be sound, accept the false "
            "positives, and staff the triage.</b> Astrée, SPARK.",
            "<b>Developers will ignore a noisy tool?</b> <b>Be "
            "near-complete, miss bugs deliberately</b>, and keep the "
            "signal-to-noise high enough to be used. Infer's explicit "
            "position.",
            "<b>The guarantee is the product?</b> <b>Demand "
            "certificates</b> and accept the cost in developer "
            "effort.",
            "<b>And always: state the position in the "
            "documentation.</b> <b>A tool whose users do not know "
            "whether 'no issues' means 'proved safe' is harmful "
            "regardless of its technical quality.</b>"]},

  {"t": "bullets", "kicker": "Designing", "title": "Designing an analysis, in order",
   "items": [
     "<b>1 · Prove the problem undecidable</b>, or recognise it "
     "by Rice's theorem (Module 06 §2). <b>Ten minutes.</b>",
     "",
     "<b>2 · Decide what a wrong answer costs</b>, in each "
     "direction, separately.",
     "",
     "<b>3 · Choose which of sound, complete, terminating to "
     "give up</b>, and write it down.",
     "",
     "<b>4 · Choose strategies from Part 1's table</b>, usually "
     "two or three combined.",
     "",
     "<b>5 · Then build it, and construct your own false "
     "positive and false negative</b> before anyone else does.",
   ],
   "footnote": "<b>Steps 1 through 3 take an hour and determine "
               "everything after</b> — which makes them the "
               "highest-value hour in building an analysis tool."},
 ],
 "takeaways": [
   "The four strategies are approximate, restrict the input, bound a "
   "resource, and demand a certificate — each gives up something "
   "different, so they combine.",
   "Abstract interpretation makes soundness a property of the construction "
   "and precision a tunable dial, which is the right place for the "
   "engineering effort.",
   "Restriction is the most underused strategy because it must be chosen "
   "at design time, and it is the only one that makes the problem go "
   "away.",
   "Bounding is easiest and most honest if you state the bound; the "
   "failure mode is reporting a bounded result as unbounded.",
   "Checking a proof is decidable even when finding one is not, so "
   "certificates are the only route to a sound and complete checker.",
   "Which strategy to choose depends on what a wrong answer costs in each "
   "direction, which makes it a product decision rather than a technical "
   "one.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The four strategies"),
  ("table", ["Strategy", "What it gives up", "Examples"],
   [["<b>Approximate</b>", "<b>Precision.</b>",
     "<b>Abstract interpretation, type systems, dataflow analysis.</b> "
     "See the callout."],
    ["<b>Restrict the input language</b>", "<b>Expressiveness.</b>",
     "<b>Total functional languages, non-Turing-complete configuration "
     "formats, decidable logical fragments</b> (&sect;2)."],
    ["<b>Bound a resource</b>", "<b>Coverage.</b>",
     "<b>Bounded model checking, Ethereum's gas, timeouts, loop unrolling "
     "limits</b> (Module 06 &sect;2)."],
    ["<b>Demand a certificate</b>", "<b>Automation.</b>",
     "<b>Proof-carrying code, dependent types, Rust lifetimes, proof "
     "assistants</b> (&sect;3)."]],
   [0.24, 0.24, 0.52]),
  ("p", "<b>Each gives up something different</b>, which is why they "
        "compose rather than compete — <b>a real tool typically uses "
        "two or three at once</b> (a bounded abstract interpretation over "
        "a restricted language, with programmer annotations where it gets "
        "stuck), <b>and stating which is what makes its output "
        "interpretable.</b>"),
  ("callout", "Approximation can be sound by construction",
   ["<b>Instead of computing exact values, compute a deliberate "
    "over-approximation.</b> Instead of 'x = 7', compute 'x is in "
    "[0, 10]' or 'x is positive' — less information, and "
    "obtainable without running the program.",
    "<b>Design the abstract domain and its operations so that the "
    "abstract result always <i>contains</i> the concrete one</b> — "
    "then <b>soundness is a property of the construction rather than "
    "something to test for</b>, which is the central idea of abstract "
    "interpretation and is what makes it suitable for safety-critical "
    "work.",
    "<b>And the analysis terminates because the abstract domain has "
    "finite height</b>, or because a <i>widening</i> operator forces "
    "convergence after finitely many steps. <b>Termination is built in "
    "as well.</b>",
    "<b>So you get sound and terminating, and lose precision</b> "
    "— <b>which is Module 08 &sect;2's pick-two-of-three, with "
    "the loss placed somewhere you can measure, tune, and trade "
    "against cost.</b> <b>Putting the unavoidable loss in a tunable "
    "place is the engineering achievement</b>, not the soundness "
    "itself."]),
  ("code", """CONCRETE: x = 5; y = 3; z = x + y;      -> z = 8

ABSTRACT, with the SIGN domain:
    x : positive
    y : positive
    z : positive + positive = positive

The abstract result is CORRECT and LESS INFORMATIVE, and it
was computed WITHOUT running the program.

THE DESIGN OBLIGATIONS
    a DOMAIN       signs, intervals, octagons, polyhedra
    a TRANSFER FUNCTION per operation, which must
        over-approximate the concrete one
    a JOIN for merging control-flow branches
        positive join negative = unknown
    and WIDENING for loops, to force convergence
        [0,1] then [0,2] then [0,3] ... widen to
        [0, infinity]

PRECISION IS A DIAL: signs are cheap and coarse; intervals
better; octagons (constraints of the form x - y <= c)
better again; convex polyhedra precise and expensive.

ASTREE verified the ABSENCE OF RUNTIME ERRORS in Airbus
flight control code using exactly this. Sound, terminating,
and it required engineers to select and tune domains per
module -- which is what the approach costs in practice."""),

  ("h1", "2 &nbsp; Restriction and bounding"),
  ("ul", ["<b>Total functional languages.</b> Agda, Idris, Coq's "
          "terminating fragment. <b>Termination is guaranteed by the "
          "type system, and some computable total functions cannot be "
          "written</b> (Module 09 &sect;1's theorem, which is exactly "
          "the price).",
          "<b>Non-Turing-complete configuration languages.</b> Dhall, "
          "Starlark, and similar. <b>Deliberate weakness</b> "
          "(Module 11 &sect;2), chosen so that configurations can be "
          "analysed, diffed, and bounded.",
          "<b>Decidable logical fragments.</b> Presburger arithmetic, "
          "linear real arithmetic, bit-vectors, arrays, "
          "effectively-propositional formulas — <b>which is how SMT "
          "solvers are assembled</b> (Module 10 &sect;4), and the "
          "engineering consists in staying inside them.",
          "<b>Structured programming.</b> <b>Bounded loops and the "
          "absence of arbitrary <code>goto</code> make reaching-definition "
          "and dominance analyses straightforward</b> — which is a "
          "retrospective theoretical justification for what was argued on "
          "stylistic grounds in 1968.",
          "<b>And type systems themselves</b>, which restrict what can "
          "be expressed precisely in order to decide something about what "
          "remains. <b>Restriction is the most underused of the four "
          "strategies</b>, because <b>it has to be chosen at design "
          "time</b> and cannot be retrofitted — <b>and it is the "
          "only one that makes the problem genuinely go away</b> rather "
          "than managing it."]),
  ("callout", "Bounding is the easiest and the most honest",
   ["<b>Unroll loops k times; explore to depth d; stop after t "
    "seconds.</b> <b>The bounded question is decidable, always</b>, by "
    "Module 06 &sect;2's bounded-property observation — there is "
    "no cleverness required.",
    "<b>And the resulting claim is clean <i>provided you state the "
    "bound</i>:</b> 'no error reachable within 20 transitions' is a "
    "complete, checkable, and genuinely useful statement about a "
    "system.",
    "<b>The failure mode is reporting the bounded result as though it "
    "were unbounded</b> — which Module 08 &sect;3 flagged, and "
    "which is <b>a documentation failure rather than a technical one</b>, "
    "and therefore entirely avoidable.",
    "<b>And it composes with the others:</b> <b>bounded abstract "
    "interpretation, bounded search over a restricted language, bounded "
    "checking with programmer annotations where the bound bites</b> "
    "— <b>real tools stack them</b>, and the stacking is where the "
    "practical capability comes from."]),

  ("break",),
  ("h1", "3 &nbsp; Certificates"),
  ("callout", "If finding the proof is undecidable, checking one is not",
   ["<b>Module 04 &sect;2's recognisability result means a proof can "
    "be <i>checked</i> mechanically even when it cannot be "
    "<i>found</i></b> — the asymmetry between &Sigma;<sub>1</sub> and "
    "decidable, put to work.",
    "<b>So demand the proof as an input.</b> <b>Proof-carrying code, "
    "verified compilers' translation certificates, dependently typed "
    "programs, and Rust's lifetime annotations are all instances of "
    "this</b> — the programmer or an upstream tool supplies the "
    "witness, and the checker verifies it.",
    "<b>The cost is that a human or a separate tool must produce the "
    "certificate</b> — which is real work, and <b>is why formal "
    "verification is expensive</b> rather than why it is rare.",
    "<b>And the gain is a sound <i>and</i> complete checker</b> "
    "— <b>the only position in Module 08 &sect;2's table that "
    "achieves both, because the undecidable search has been moved outside "
    "the tool.</b> <b>That is the whole trade, and it is worth seeing "
    "clearly:</b> you have not escaped the theorem, you have relocated "
    "the work to somewhere a human can apply judgement."]),
  ("table", ["Approach", "The certificate is", "Produced by"],
   [["<b>Rust ownership and borrowing</b>",
     "<b>Lifetime annotations, mostly inferred.</b>",
     "<b>The programmer, with substantial inference</b> — which is "
     "why Rust feels like an ordinary language most of the time and like a "
     "proof assistant occasionally."],
    ["<b>Dependent types</b>", "<b>The type itself is the proof.</b>",
     "<b>The programmer</b>, and this is the whole development effort in "
     "Agda or Idris."],
    ["<b>Proof-carrying code</b>",
     "<b>A machine-checkable proof shipped with the binary.</b>",
     "<b>A certifying compiler, or a separate prover.</b>"],
    ["<b>Verified compilation (CompCert)</b>",
     "<b>A proof that this output matches this input's semantics.</b>",
     "<b>The compiler, once per compilation</b> — or, in CompCert's "
     "case, a once-and-for-all proof about the compiler."],
    ["<b>SAT unsatisfiability proofs</b>",
     "<b>A DRAT refutation.</b>",
     "<b>The solver itself</b> (CSCE 625 Module 08 &sect;2)."]],
   [0.25, 0.33, 0.42]),
  ("p", "<b>The solver-produced certificate is the best case:</b> <b>the "
        "tool does all the work and emits something an independent, much "
        "simpler checker can verify</b> — so <b>you need not trust "
        "the complicated tool at all</b>, only the small checker. <b>That "
        "is the real value of certificates</b>, and it is why "
        "unsatisfiability proofs changed how SAT solvers are used in "
        "verification."),

  ("h1", "4 &nbsp; Choosing, and designing"),
  ("callout", "Which strategy depends on what a wrong answer costs",
   ["<b>A missed bug is catastrophic — avionics, medical devices, "
    "cryptographic implementations?</b> <b>Be sound, accept the false "
    "positives, and staff the triage.</b> Astr&eacute;e and SPARK are in "
    "this position, and their users accept a high alarm rate because the "
    "alternative is unacceptable.",
    "<b>Developers will ignore a noisy tool entirely?</b> <b>Be "
    "near-complete, miss bugs deliberately</b>, and keep the "
    "signal-to-noise ratio high enough that the tool stays in the "
    "build. <b>Infer's team state this explicitly</b>, and it is a "
    "correct engineering judgement rather than a compromise: a sound tool "
    "nobody runs finds nothing.",
    "<b>The guarantee itself is the product?</b> <b>Demand "
    "certificates</b> (&sect;3) and accept the cost in developer effort "
    "— which is the seL4 and CompCert position.",
    "<b>And in every case: state the position in the "
    "documentation.</b> <b>A tool whose users do not know whether 'no "
    "issues found' means 'proved safe' or 'found nothing' is harmful "
    "regardless of its technical quality</b>, because the users will "
    "assume whichever is more convenient. <b>This is the one failure in "
    "the module that is purely a writing failure.</b>"]),
  ("ul", ["<b>1 &middot; Prove the problem undecidable</b>, or recognise "
          "it immediately by Rice's theorem (Module 06 &sect;2). "
          "<b>Ten minutes, and it prevents a month of searching for an "
          "exact algorithm.</b>",
          "<b>2 &middot; Decide what a wrong answer costs, in each "
          "direction separately.</b> <b>A false positive and a false "
          "negative almost never cost the same</b>, and the asymmetry "
          "determines everything downstream.",
          "<b>3 &middot; Choose which of sound, complete, and "
          "terminating to give up</b>, and <b>write it down where users "
          "will see it.</b>",
          "<b>4 &middot; Choose strategies from &sect;1's table</b>, "
          "usually two or three in combination.",
          "<b>5 &middot; Then build it — and construct your own "
          "false positive and false negative before anyone else "
          "does</b> (Module 08 &sect;4). <b>Steps 1 through 3 take an "
          "hour and determine everything after them</b>, which makes them "
          "<b>the highest-value hour in building an analysis tool</b> and "
          "the one most often skipped."]),
 ],
 "resources": [
   ("Cousot & Cousot &mdash; Abstract Interpretation papers (free)",
    "https://www.di.ens.fr/~cousot/COUSOTpapers.shtml",
    "<b>&sect;1's framework from its originators</b>, including the "
    "widening operator and the soundness-by-construction argument."),
   ("Blanchet et al. &mdash; A Static Analyzer for Large Safety-Critical "
    "Software (Astrée) (free)",
    "https://www.astree.ens.fr/",
    "<b>&sect;1's industrial result</b>, including what the domain tuning "
    "actually involved."),
   ("Necula & Lee &mdash; Proof-Carrying Code (free)",
    "https://dl.acm.org/doi/10.1145/263699.263712",
    "<b>&sect;3's approach</b>, and the clearest statement of the "
    "check-versus-find asymmetry."),
   ("Facebook Infer &mdash; the design documentation (free)",
    "https://fbinfer.com/docs/about-Infer/",
    "<b>&sect;4's near-complete position, stated explicitly by its "
    "authors</b> — a rare and commendable piece of honest tool "
    "documentation."),
 ],
 "exercises": [
   "<b>Implement a sign-domain abstract interpreter</b> for a small "
   "imperative language.",
   "<b>Extend it to intervals</b> and report where the precision "
   "improves.",
   "<b>Add a widening operator</b> and confirm loops now converge.",
   "<b>Construct a program where the sign domain loses the answer</b> and "
   "the interval domain keeps it.",
   "<b>Verify your transfer functions over-approximate</b> by testing "
   "against concrete execution.",
   "<b>Take an analysis problem and apply all four strategies</b>, "
   "sketching each.",
   "<b>Find a configuration language that is deliberately weak</b> and "
   "identify what it gave up.",
   "<b>Run a bounded checker at two bounds</b> and write the honest claim "
   "for each.",
   "<b>Get a DRAT proof from a SAT solver</b> and verify it with an "
   "independent checker.",
   "<b>Design an analysis for a problem you care about</b>, following "
   "&sect;4's five steps, and write down steps 1 to 3 before coding.",
 ],
 "selfcheck": [
   "Name the four strategies and what each gives up.",
   "Why do they compose?",
   "Explain soundness by construction in abstract interpretation.",
   "Name the four design obligations of an abstract domain.",
   "Why is precision the right place to put the loss?",
   "Name five restriction examples and why restriction is underused.",
   "What makes bounding honest, and what is its failure mode?",
   "Why does a certificate give both soundness and completeness?",
   "Why is a solver-produced certificate the best case?",
   "Give the five design steps and say which three matter most.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "The Limits, Honestly",
 "subtitle": "What this course does and does not tell you.",
 "question": "What should you actually take from a semester of "
             "impossibility?",
 "outcomes": [
     "State what the results do and do not constrain.",
     "Avoid the standard overreaches.",
     "Explain how to use an impossibility result productively.",
     "Place this course relative to CSCE 637 and CSCE 658.",
     "State what a claim about computability can honestly assert.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What is established",
   "blurb": "The results, listed."},

  {"t": "bullets", "kicker": "Established", "title": "What a semester of proofs gives you",
   "items": [
     "<b>There is a definition of algorithm</b>, it is robust across "
     "every reasonable model, and it is almost certainly the right one "
     "(M01, M04, M11).",
     "",
     "<b>A strict hierarchy of language classes</b>, each separation "
     "proved, with practical consequences at every level "
     "(M02, M03).",
     "",
     "<b>Specific, natural, important problems are undecidable</b> "
     "— and almost every semantic property of programs is "
     "(M05, M06).",
     "",
     "<b>'Undecidable' is infinitely many levels</b>, measured by "
     "quantifier alternation (M07).",
     "",
     "<b>And no sound, complete, mechanically checkable system of "
     "sufficient strength exists</b> (M10) — which is "
     "M05 again.",
   ],
   "footnote": "<b>All of it permanent, and all of it independent of "
               "hardware, language, and era</b> — which no other "
               "course in this program can say."},

  {"t": "section", "label": "Part 2", "title": "The overreaches",
   "blurb": "What people claim from these results, incorrectly."},

  {"t": "table", "kicker": "Overreach", "title": "Common claims, and what is wrong with them",
   "header": ["Claim", "Why it is wrong"],
   "widths": [5.0, 6.0],
   "rows": [
     ["<b>'Static analysis is pointless'</b>", "<b>Undecidability constrains the guarantee, not the usefulness (M08, M12)</b>"],
     ["<b>'Gödel shows minds exceed machines'</b>", "<b>Assumes minds are consistent and formalisable — the thing to be shown (M10 §3)</b>"],
     ["<b>'Quantum computers break undecidability'</b>", "<b>Same computable class; only the speed changes (M11 §3)</b>"],
     ["<b>'The halting problem means we cannot verify software'</b>", "<b>We verify software routinely, by M12's four strategies</b>"],
     ["<b>'Undecidable means practically impossible'</b>", "<b>Conflates the universal quantifier with the typical case (M01 §3)</b>"],
     ["<b>'AI cannot be intelligent because of Gödel'</b>", "<b>Applies equally to any formalisable reasoner, including a human</b>"],
   ],
   "footnote": "<b>Every overreach has the same shape:</b> a result about "
               "a universally quantified claim is read as a result about "
               "practice, or about minds.",
   "note": "Students will meet all six; the table is worth memorising."},

  {"t": "callout", "title": "The most useful correction",
   "kind": "Said once more",
   "body": ["<b>'No algorithm decides X for all inputs' and 'X is hard "
            "for the inputs I have' are different claims.</b>",
            "<b>The first is proved. The second is an empirical "
            "question about your inputs</b>, and is frequently false "
            "— most real programs are obviously terminating.",
            "<b>So an undecidability result tells you what a <i>total "
            "and exact</i> tool cannot promise</b>, and nothing about "
            "what a tool can deliver on your workload.",
            "<b>Which is why Module 12's strategies work at all</b>, "
            "and why the correct response to an impossibility proof is to "
            "design the approximation rather than to abandon the "
            "problem."]},

  {"t": "section", "label": "Part 3", "title": "Using it",
   "blurb": "The productive response."},

  {"t": "bullets", "kicker": "Productive", "title": "What to do with an impossibility result",
   "items": [
     "<b>Stop looking for the exact algorithm.</b> <b>An hour "
     "proving impossibility saves a month</b> "
     "(M06 §4).",
     "",
     "<b>Identify what you actually need.</b> Frequently a sound "
     "approximation, or an answer on your inputs, is the whole "
     "requirement.",
     "",
     "<b>Choose from Module 12's four strategies</b>, and state which "
     "of sound, complete, terminating you gave up.",
     "",
     "<b>Consider restricting the problem</b> — the most "
     "underused move, and the only one that removes the difficulty.",
     "",
     "<b>And document the limit</b>, so the next person does not "
     "repeat your month.",
   ],
   "footnote": "<b>The documentation step is the one that compounds:</b> "
               "an impossibility recorded in a design document is worth "
               "more than one proved and forgotten."},

  {"t": "section", "label": "Part 4", "title": "The semester",
   "blurb": "Three courses, three kinds of limit."},

  {"t": "table", "kicker": "Semester 8", "title": "Three theory courses, three questions",
   "header": ["Course", "Asks", "Answers of the form"],
   "widths": [2.5, 3.9, 5.4],
   "rows": [
     ["<b>CSCE 627</b>", "<b>Can it be done at all?</b>", "<b>No algorithm exists. Proved, permanent</b>"],
     ["<b>CSCE 637</b>", "<b>Can it be done efficiently?</b>", "<b>Not in polynomial time, unless P = NP</b>"],
     ["<b>CSCE 658</b>", "<b>Does randomness help?</b>", "<b>Sometimes, provably — and perhaps never essentially</b>"],
   ],
   "footnote": "<b>Note the certainty gradient:</b> this course's results "
               "are unconditional, CSCE 637's are mostly conditional, and "
               "CSCE 658's include an open question about whether its own "
               "subject matter is necessary.",
   "note": "The certainty gradient is the honest framing of the "
           "semester."},

  {"t": "callout", "title": "What a claim about computability can honestly assert",
   "kind": "The scoped claim, in this subject",
   "body": ["<b>'This problem is undecidable, by reduction from the "
            "halting problem; here is the reduction.'</b> <b>Checkable, "
            "and the strongest form available.</b>",
            "<b>'This property is semantic and non-trivial, so Rice's "
            "theorem applies.'</b> <b>Also checkable, and much "
            "faster.</b>",
            "<b>'Our analyser is sound and incomplete; here is a false "
            "positive we constructed.'</b> <b>The position stated and "
            "demonstrated.</b>",
            "<b>And what you cannot say: 'this is impossible'</b> "
            "— unqualified. <b>Impossible for a total exact "
            "algorithm, and that is a different and much narrower "
            "claim.</b>"]},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can prove a language non-regular, place a problem "
            "in the hierarchy, construct a reduction, and apply Rice's "
            "theorem in under a minute.</b>",
            "<b>You can derive incompleteness from halting</b>, and "
            "state both theorems with their conditions rather than their "
            "popular versions.",
            "<b>And you can look at a tool and say which of sound, "
            "complete, terminating it gave up</b> — which is the "
            "practical skill, and it changes how you read every "
            "analyser's output.",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it means saying what the "
            "quantifier ranges over</b> — because the whole subject "
            "lives in the difference between 'for all inputs' and 'for my "
            "inputs'."]},
 ],
 "takeaways": [
   "The results are permanent and independent of hardware, language, and "
   "era, which no other course in this program can claim.",
   "Every standard overreach has the same shape — a result about a "
   "universally quantified claim read as a result about practice or about "
   "minds.",
   "'No algorithm decides X for all inputs' and 'X is hard for my inputs' "
   "are different claims, and the second is frequently false.",
   "The productive response is to stop looking, identify what you need, "
   "choose a strategy, consider restricting, and document the limit.",
   "The semester has a certainty gradient: unconditional here, mostly "
   "conditional in CSCE 637, and partly open in CSCE 658.",
   "You cannot say 'this is impossible' unqualified — only impossible "
   "for a total exact algorithm, which is much narrower.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What the semester establishes"),
  ("ul", ["<b>There is a definition of algorithm</b>, it is robust "
          "across every reasonable model, and the coincidence of "
          "independent formalisations makes it almost certainly the right "
          "one (Modules 01, 04, 11).",
          "<b>A strict hierarchy of language classes</b> — regular, "
          "context-free, context-sensitive, recognisable, decidable "
          "— each separation proved, <b>with practical consequences "
          "at every level</b>: lexers, parsers, semantic analysis "
          "(Modules 02, 03).",
          "<b>Specific, natural, and practically important problems are "
          "undecidable</b> — halting, equivalence, reachability, "
          "aliasing — <b>and almost every semantic property of "
          "programs is, by Rice's theorem</b> (Modules 05, 06).",
          "<b>'Undecidable' names infinitely many distinct levels</b>, "
          "measured by quantifier alternation, <b>with the "
          "safety/liveness distinction as its most useful practical "
          "instance</b> (Module 07).",
          "<b>And no sound, complete, mechanically checkable formal "
          "system of sufficient strength exists</b> (Module 10) — "
          "<b>which is Module 05 again, in a different vocabulary.</b> "
          "<b>All of it permanent, and all of it independent of hardware, "
          "language, and era</b> — which no other course in this "
          "program can say about its contents."]),

  ("h1", "2 &nbsp; The overreaches"),
  ("table", ["The claim", "What is wrong with it"],
   [["<b>'Static analysis is pointless, because the problems are "
     "undecidable.'</b>",
     "<b>Undecidability constrains what a tool can <i>promise</i>, not "
     "whether it is <i>useful</i></b> (Modules 08, 12). Type "
     "checkers are undecidable-problem solvers and are used by "
     "everyone."],
    ["<b>'G&ouml;del shows human minds exceed machines.'</b>",
     "<b>The argument assumes human reasoning is consistent and "
     "formalisable</b> — which is precisely what would need to be "
     "established, so the argument assumes its conclusion "
     "(Module 10 &sect;3)."],
    ["<b>'Quantum computers will break undecidability.'</b>",
     "<b>A quantum computer computes exactly the same class of "
     "functions; only the speed of some computations changes</b> "
     "(Module 11 &sect;3)."],
    ["<b>'The halting problem means software cannot be verified.'</b>",
     "<b>Software is verified routinely</b>, by Module 12's four "
     "strategies — seL4, CompCert, and Airbus flight control are "
     "existence proofs."],
    ["<b>'Undecidable means practically impossible.'</b>",
     "<b>It conflates the universal quantifier with the typical "
     "case</b> (Module 01 &sect;3). Most instances of most "
     "undecidable problems are easy."],
    ["<b>'AI cannot be genuinely intelligent, because of "
     "G&ouml;del.'</b>",
     "<b>The argument applies equally to any formalisable reasoner, "
     "including a human one</b> — so either it proves too much or it "
     "assumes humans are not formalisable, which is the claim at "
     "issue."]],
   [0.42, 0.58]),
  ("p", "<b>Every overreach has the same shape:</b> <b>a result about a "
        "universally quantified claim is read as a result about practice, "
        "or about minds.</b> <b>Recognising the shape is quicker than "
        "refuting each instance</b>, and you will meet all six."),
  ("callout", "The most useful correction",
   ["<b>'No algorithm decides X for all inputs' and 'X is hard for the "
    "inputs I actually have' are different claims.</b>",
    "<b>The first is proved. The second is an empirical question about "
    "your particular inputs</b>, <b>and it is frequently false</b> "
    "— most real programs are obviously terminating, most real "
    "pointers obviously do not alias, and most real grammars are "
    "obviously unambiguous.",
    "<b>So an undecidability result tells you what a <i>total and "
    "exact</i> tool cannot promise, and nothing whatsoever about what a "
    "tool can deliver on your workload.</b>",
    "<b>Which is why Module 12's strategies work at all</b>, and why "
    "<b>the correct response to an impossibility proof is to design the "
    "approximation rather than to abandon the problem.</b> <b>If one "
    "sentence from this course should survive, it is this one.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Using an impossibility result"),
  ("ul", ["<b>Stop looking for the exact algorithm.</b> <b>An hour "
          "spent proving impossibility saves a month of searching</b> "
          "(Module 06 &sect;4), and Rice's theorem frequently makes it "
          "ten minutes.",
          "<b>Identify what you actually need.</b> <b>Frequently a sound "
          "approximation, or a correct answer on the inputs you have, is "
          "the entire requirement</b> — and nobody asked for "
          "totality.",
          "<b>Choose from Module 12's four strategies</b>, and <b>state "
          "which of sound, complete, and terminating you gave up</b>, "
          "where users will see it.",
          "<b>Consider restricting the problem.</b> <b>The most "
          "underused move, and the only one that removes the difficulty "
          "rather than managing it</b> (Module 12 &sect;2) — and "
          "it is available far more often than people assume.",
          "<b>And document the limit</b>, so the next person does not "
          "repeat your month. <b>The documentation step is the one that "
          "compounds:</b> <b>an impossibility recorded in a design "
          "document is worth considerably more than one proved and "
          "forgotten</b>, and it is the cheapest step on the list."]),

  ("h1", "4 &nbsp; The semester, and the honest claim"),
  ("table", ["Course", "Asks", "Answers take the form"],
   [["<b>CSCE 627 (this one)</b>", "<b>Can it be done at all?</b>",
     "<b>No algorithm exists. Proved, unconditional, permanent.</b>"],
    ["<b>CSCE 637</b>", "<b>Can it be done efficiently?</b>",
     "<b>Not in polynomial time, unless P = NP</b> — mostly "
     "conditional on an open question."],
    ["<b>CSCE 658</b>", "<b>Does randomness help?</b>",
     "<b>Sometimes, provably — and possibly never essentially</b>, "
     "since whether randomness can always be removed is itself open."]],
   [0.23, 0.30, 0.47]),
  ("p", "<b>Note the certainty gradient across the semester:</b> <b>this "
        "course's results are unconditional, CSCE 637's central claims "
        "are conditional on P &ne; NP, and CSCE 658 contains an open "
        "question about whether its own subject matter is "
        "necessary</b> (derandomisation). <b>Which is the honest framing "
        "of a theory semester</b> — the further you move from "
        "computability toward resources, the more the results depend on "
        "conjectures, and <b>saying so is more useful than presenting all "
        "three as equally settled.</b>"),
  ("callout", "What a claim about computability can honestly assert",
   ["<b>'This problem is undecidable, by reduction from the halting "
    "problem; here is the reduction.'</b> <b>Checkable by anyone, and "
    "the strongest form of claim available in this program.</b>",
    "<b>'This property is semantic and non-trivial, so Rice's theorem "
    "applies.'</b> <b>Also fully checkable, and much faster to "
    "establish</b> — and it is the claim you will make most often.",
    "<b>'Our analyser is sound and incomplete; here is a false positive "
    "we constructed, and here is the documented unsoundness source we "
    "accept.'</b> <b>The position stated and demonstrated rather than "
    "asserted.</b>",
    "<b>And what you cannot honestly say: 'this is impossible'</b>, "
    "unqualified. <b>Impossible for a total, exact algorithm — and "
    "that is a different and much narrower claim than the unqualified "
    "one</b>, which is where every overreach in &sect;2 begins."]),
  ("callout", "Where this course leaves you",
   ["<b>You can prove a language non-regular, place a problem in the "
    "Chomsky hierarchy, construct a mapping reduction in the right "
    "direction, and apply Rice's theorem in under a minute</b> — "
    "which is the technical content, and the last of those is the one you "
    "will use most.",
    "<b>You can derive G&ouml;del's first incompleteness theorem from the "
    "halting problem</b>, and <b>state both theorems with their actual "
    "conditions rather than their popular versions</b> — which is "
    "unusual and worth having.",
    "<b>And you can look at a tool and say which of sound, complete, and "
    "terminating it gave up.</b> <b>That is the practical skill of the "
    "course</b>, and it changes how you read every analyser's output, "
    "every type error, and every 'no issues found'.",
    "<b>The closing rule is the program's, unchanged across twenty-two "
    "courses:</b> <b>state what you measured, state what you assumed, "
    "and never claim more than you established.</b> <b>In computability "
    "it means saying what the quantifier ranges over</b> — because "
    "<b>the entire subject lives in the difference between 'for all "
    "inputs' and 'for my inputs'</b>, and so does every mistake people "
    "make with it."]),
 ],
 "resources": [
   ("Franzén &mdash; Gödel's Theorem: An Incomplete Guide to "
    "Its Use and Abuse",
    "https://www.routledge.com/Godels-Theorem-An-Incomplete-Guide-to-Its-Use-and-Abuse/Franzen/p/book/9781568812380",
    "<b>&sect;2's second and sixth rows, at book length</b> — the "
    "standard correction, and worth reading before citing the theorems."),
   ("Aaronson &mdash; Why Philosophers Should Care About Computational "
    "Complexity (free)",
    "https://www.scottaaronson.com/papers/philos.pdf",
    "<b>The honest version of what these results do and do not bear "
    "on</b>, spanning this course and CSCE 637."),
   ("Sipser &mdash; the whole book, reread",
    "https://math.mit.edu/~sipser/book.html",
    "<b>It is short, and the second reading is substantially different "
    "from the first</b> — which is unusual for a textbook and is "
    "worth the weekend."),
   ("Rice's theorem, Module 06, reread",
    "https://math.mit.edu/~sipser/book.html",
    "<b>If one result from this course should be at your fingertips, it "
    "is this one</b> — it answers 'is this analysis possible?' in "
    "ten minutes, repeatedly, for the rest of your career."),
 ],
 "exercises": [
   "<b>Write out the five established results</b> of &sect;1 in your own "
   "words, with the module each came from.",
   "<b>Find three of &sect;2's overreaches in the wild</b> and write the "
   "correction for each.",
   "<b>Explain the for-all-inputs versus for-my-inputs distinction</b> to "
   "someone who has not taken this course.",
   "<b>Take an unsolved problem from your own work</b> and spend an hour "
   "on &sect;3's first step.",
   "<b>Whatever the outcome, document it</b> in a form the next person "
   "could use.",
   "<b>For a tool you use daily, write its soundness position</b> in one "
   "sentence.",
   "<b>Compare the three Semester 8 courses' claim forms</b> and say "
   "which you find most and least satisfying.",
   "<b>Write the honest claim</b> for the undecidability result you proved "
   "in Project 1.",
   "<b>Revisit what you wrote in Module 01's last exercise</b> and report "
   "what changed.",
   "<b>Project 2 is now due.</b> Submit the tool, the undecidable problem "
   "identified with its argument, the soundness position, the false "
   "positive, the false negative, and your assessment of the "
   "documentation.",
 ],
 "selfcheck": [
   "Name the five results the semester established.",
   "What makes them different from every other result in this program?",
   "Give six overreaches and the correction to each.",
   "What shape do all of them share?",
   "State the for-all versus for-mine distinction and why it matters.",
   "Give the five productive responses to an impossibility result.",
   "Which compounds, and why?",
   "Compare the three theory courses' claim forms.",
   "Give three honest claims and the one thing you cannot say.",
   "In this course, what does 'state what you assumed' mean?",
 ],
},

]
