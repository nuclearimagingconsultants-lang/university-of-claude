# -*- coding: utf-8 -*-
"""CSCE 637 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Randomised Complexity",
 "subtitle": "Does a coin help?",
 "question": "Can randomness make a problem tractable?",
 "outcomes": [
     "Define BPP, RP, co-RP, and ZPP and distinguish them.",
     "Explain error amplification and why one-sided error matters.",
     "Explain why BPP is believed to equal P.",
     "Explain derandomisation and its connection to lower bounds.",
     "State what randomness demonstrably buys.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The classes",
   "blurb": "Four ways a coin can be used."},

  {"t": "table", "kicker": "Randomised classes", "title": "What error each class permits",
   "header": ["Class", "Error allowed", "Example"],
   "widths": [2.3, 4.4, 5.3],
   "rows": [
     ["<b>BPP</b>", "<b>Two-sided, bounded away from 1/2</b>", "<b>Polynomial identity testing</b>"],
     ["<b>RP</b>", "<b>One-sided: never wrong on a NO</b>", "<b>Compositeness — a found factor is certain</b>"],
     ["<b>co-RP</b>", "<b>One-sided: never wrong on a YES</b>", "<b>Primality by Miller–Rabin</b>"],
     ["<b>ZPP</b>", "<b>None — but the runtime is random</b>", "<b>RP ∩ co-RP. Las Vegas algorithms</b>"],
     ["<b>PP</b>", "<b>Two-sided, any gap from 1/2</b>", "<b>Too permissive; contains NP</b>"],
   ],
   "footnote": "<b>PP is the warning:</b> <b>'majority of random "
               "choices accept' with no gap requirement is a useless "
               "guarantee</b>, because you cannot distinguish 1/2 from "
               "1/2 + 2⁻ⁿ by sampling.",
   "note": "The PP row teaches why the 'bounded away' condition is "
           "essential."},

  {"t": "callout", "title": "Error amplification is why the constant does not matter",
   "kind": "The fact that makes BPP robust",
   "body": ["<b>Run a BPP algorithm k times and take the "
            "majority.</b> <b>The error falls exponentially in k</b>, by "
            "a Chernoff bound.",
            "<b>So an error of 1/3 and an error of 2⁻¹⁰⁰ "
            "define the same class</b> — a hundred repetitions "
            "converts one into the other, and a hundred is a "
            "constant.",
            "<b>Which is why the definition requires the error "
            "<i>bounded away</i> from 1/2</b>: if the gap can shrink "
            "with n, amplification needs polynomially many repetitions "
            "and the argument fails. <b>That is PP.</b>",
            "<b>And the practical reading is that 2⁻¹⁰⁰ is "
            "smaller than the probability of a hardware "
            "fault</b> — <b>so a BPP algorithm is more reliable than "
            "the machine running a deterministic one.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Where randomness won",
   "blurb": "The genuine successes."},

  {"t": "bullets", "kicker": "Successes", "title": "What randomness demonstrably bought",
   "items": [
     "<b>Primality testing.</b> <b>Miller–Rabin was the "
     "practical algorithm for twenty-five years before AKS</b>, and it "
     "is still what everyone uses (M02 §2).",
     "",
     "<b>Polynomial identity testing.</b> <b>Is this symbolic "
     "expression identically zero? In BPP, and not known to be in P</b> "
     "— the headline open case.",
     "",
     "<b>Volume estimation of convex bodies.</b> <b>Randomised "
     "approximation is possible and deterministic approximation is "
     "provably not</b>, which is a real separation.",
     "",
     "<b>Quicksort's pivot, hashing, load balancing, and "
     "fingerprinting</b> — where randomness buys simplicity and "
     "robustness rather than asymptotic power.",
     "",
     "<b>And cryptography</b>, which <b>needs randomness "
     "irreducibly</b> — a deterministic cipher is a lookup table.",
   ],
   "footnote": "<b>Note the pattern:</b> <b>randomness most often buys "
               "simplicity and adversary-resistance, and only rarely a "
               "complexity class</b> — which is what Part 3 "
               "explains."},

  {"t": "section", "label": "Part 3", "title": "Why BPP is believed to equal P",
   "blurb": "The derandomisation argument."},

  {"t": "callout", "title": "BPP = P is the expectation, and the reason is pseudorandomness",
   "kind": "The surprising belief",
   "body": ["<b>A pseudorandom generator stretches a short seed into a "
            "long string no efficient algorithm can distinguish from "
            "random.</b>",
            "<b>If such generators exist, a BPP algorithm can be run on "
            "pseudorandom bits from every seed, and the majority "
            "taken</b> — which is deterministic and polynomial, since "
            "the seeds are short.",
            "<b>And strong enough generators follow from circuit lower "
            "bounds</b> (Module 09): <b>if some problem in E requires "
            "exponential-size circuits, then BPP = P.</b>",
            "<b>So hardness implies derandomisation</b> — "
            "<b>the existence of hard problems is what makes randomness "
            "unnecessary</b>, which is the most counterintuitive result "
            "in the course and is genuinely beautiful."]},

  {"t": "code", "kicker": "The connection", "title": "Hardness gives pseudorandomness",
   "lang": "text", "code": """
  THE INTUITION: a sequence is random ENOUGH if no
  efficient observer can tell it from random. That is a
  COMPUTATIONAL notion, not a statistical one.

  SO: take a function f that is HARD to compute. Its output
  bits look unpredictable to anything that cannot compute
  it. Use f to stretch a seed.

      Nisan-Wigderson: if f in E requires circuits of size
      2^(eps n), then there is a pseudorandom generator
      fooling polynomial-size circuits -- which gives
      BPP = P.

  THE SHAPE OF THE ARGUMENT
      HARD PROBLEMS EXIST  =>  PSEUDORANDOMNESS EXISTS
                           =>  RANDOMNESS IS REMOVABLE

  AND THE CONVERSE DIRECTION ALSO HOLDS partially:
  derandomising certain problems would imply circuit lower
  bounds (Impagliazzo-Kabanets). So the two questions are
  tied together.

  WHICH MEANS: whether randomness helps is not an
  independent question. It is the SAME question as whether
  hard problems exist -- and that is Module 09's subject.
""",
   "caption": "<b>Randomness and hardness are two views of one "
              "question</b>, which is the deepest connection in the "
              "course.",
   "note": "The hardness-to-randomness direction surprises everyone; "
           "dwell on it."},

  {"t": "section", "label": "Part 4", "title": "What follows",
   "blurb": "For practice, and for the rest of the course."},

  {"t": "bullets", "kicker": "Practical", "title": "The practical reading",
   "items": [
     "<b>Use randomised algorithms freely.</b> <b>2⁻¹⁰⁰ "
     "error is below the hardware fault rate</b>, and the algorithms "
     "are usually simpler.",
     "",
     "<b>Prefer one-sided error when available.</b> <b>A found factor "
     "is a certainty; a Miller–Rabin 'probably prime' is "
     "not</b> — and the difference matters in a protocol.",
     "",
     "<b>And distinguish Las Vegas from Monte Carlo.</b> <b>Random "
     "runtime with a certain answer (ZPP) is usually preferable to a "
     "certain runtime with a random answer.</b>",
     "",
     "<b>Randomness does not escape NP-hardness.</b> <b>BPP is not "
     "believed to contain NP</b>, so a coin will not solve your "
     "NP-complete problem.",
     "",
     "<b>And the quality of your randomness matters</b> — a weak "
     "generator can break the guarantee entirely (CSCE 711).",
   ],
   "footnote": "<b>'Randomness will not help with NP-hardness' is the "
               "practical headline</b>, and it is the thing people most "
               "often hope for."},

  {"t": "callout", "title": "The bridge to CSCE 658",
   "kind": "Where this goes next",
   "body": ["<b>This module is the complexity-class view. CSCE 658 is "
            "the algorithm-design view</b> — how to build randomised "
            "algorithms and analyse them.",
            "<b>And the two meet at derandomisation:</b> <b>CSCE 658 "
            "covers the method of conditional expectations and limited "
            "independence</b>, which remove randomness from specific "
            "algorithms rather than from a class.",
            "<b>So the question 'does randomness help?' has a "
            "class-level answer (probably not, conditionally) and an "
            "algorithm-level answer (frequently, for simplicity).</b>",
            "<b>Which are both correct and are about different "
            "things</b> — and keeping them apart is the main thing to "
            "take from this module into the next course."]},
 ],
 "takeaways": [
   "BPP permits two-sided error bounded away from a half; PP permits any "
   "gap and is useless, which shows why the bounded condition is "
   "essential.",
   "Error amplification makes the constant irrelevant, so an error of a "
   "third and an error of 2⁻¹⁰⁰ define the same "
   "class.",
   "Randomness most often buys simplicity and adversary-resistance, and "
   "only rarely a complexity class.",
   "BPP = P is expected, because pseudorandom generators would "
   "derandomise and strong generators follow from circuit lower bounds.",
   "So hardness implies derandomisation — the existence of hard "
   "problems is what makes randomness unnecessary.",
   "Randomness does not escape NP-hardness, which is the thing people "
   "most often hope for.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The classes"),
  ("table", ["Class", "Error allowed", "Canonical example"],
   [["<b>BPP</b>",
     "<b>Two-sided error, bounded away from 1/2 by a constant.</b>",
     "<b>Polynomial identity testing</b> — the headline problem in "
     "BPP and not known to be in P."],
    ["<b>RP</b>",
     "<b>One-sided: it may say no when the answer is yes, and never says "
     "yes when the answer is no.</b>",
     "<b>Compositeness</b> — a found factor is a certainty, so a yes "
     "is never wrong."],
    ["<b>co-RP</b>",
     "<b>One-sided the other way: never wrong on a yes.</b>",
     "<b>Primality by Miller–Rabin</b> — a declared composite "
     "is certainly composite, and 'probably prime' is probabilistic."],
    ["<b>ZPP</b>",
     "<b>No error at all — but the <i>running time</i> is "
     "random.</b>",
     "<b>RP &cap; co-RP.</b> Las Vegas algorithms: always correct, "
     "expected polynomial time."],
    ["<b>PP</b>",
     "<b>Two-sided error with <i>any</i> gap from 1/2, however "
     "small.</b>",
     "<b>Too permissive to be useful — it contains NP.</b> See the "
     "note."]],
   [0.17, 0.38, 0.45]),
  ("p", "<b>PP is the instructive warning:</b> <b>'a majority of random "
        "choices accept', with no requirement on the size of the "
        "majority, is a useless guarantee</b>, because <b>you cannot "
        "distinguish a probability of 1/2 from 1/2 + "
        "2<super>&minus;n</super> by sampling polynomially many times.</b> "
        "<b>So the 'bounded away' condition in BPP is doing essential "
        "work</b>, and it is the part of the definition that looks "
        "arbitrary and is not."),
  ("callout", "Error amplification is why the constant does not matter",
   ["<b>Run a BPP algorithm k independent times and take the "
    "majority.</b> <b>The error probability falls exponentially in k</b>, "
    "by a Chernoff bound (CSCE 658's material).",
    "<b>So an error bound of 1/3 and an error bound of "
    "2<super>&minus;100</super> define exactly the same class</b> "
    "— about a hundred repetitions converts one into the other, and "
    "a hundred is a constant factor. <b>Which makes BPP robust to the "
    "choice of constant</b>, in the same way Module 01 &sect;1's "
    "robustness arguments work.",
    "<b>Which is precisely why the definition requires the error to be "
    "<i>bounded away</i> from 1/2 by a constant:</b> if the gap is "
    "allowed to shrink with n, amplification requires polynomially many "
    "repetitions and the argument fails. <b>That is PP, and it is why PP "
    "is not a useful class.</b>",
    "<b>And the practical reading is that 2<super>&minus;100</super> is "
    "smaller than the probability of a cosmic-ray bit flip during the "
    "computation</b> — <b>so a randomised algorithm with amplified "
    "error is more reliable than the hardware running a deterministic "
    "one</b>, which is the correct answer to the objection that "
    "randomised algorithms 'might be wrong'."]),

  ("h1", "2 &nbsp; Where randomness demonstrably won"),
  ("ul", ["<b>Primality testing.</b> <b>Miller–Rabin was the "
          "practical algorithm for twenty-five years before AKS</b>, and "
          "<b>it is still what every cryptographic library uses</b>, "
          "because the deterministic algorithm is far slower "
          "(Module 02 &sect;2). <b>A case where the complexity result "
          "and the engineering choice diverge permanently.</b>",
          "<b>Polynomial identity testing.</b> <b>Is this symbolic "
          "arithmetic expression identically zero? In BPP — evaluate "
          "at random points — and not known to be in P</b>, which "
          "makes it the headline open case and the problem whose "
          "derandomisation would imply circuit lower bounds (&sect;3).",
          "<b>Volume estimation of convex bodies.</b> <b>Randomised "
          "approximation is possible, and deterministic approximation is "
          "provably not</b> (within the oracle model) — <b>a real "
          "and unconditional separation</b>, which is rare and worth "
          "knowing about.",
          "<b>Quicksort's pivot choice, hashing, load balancing, "
          "fingerprinting, and skip lists</b> — where <b>randomness "
          "buys simplicity and resistance to adversarial inputs rather "
          "than asymptotic power</b> (Module 01 &sect;3's quicksort "
          "note).",
          "<b>And cryptography</b>, which <b>needs randomness "
          "irreducibly</b> — <b>a deterministic cipher with a fixed "
          "key is a lookup table</b>, and key generation, nonces, and "
          "padding all require genuine entropy (CSCE 711). "
          "<b>Note the pattern across the list:</b> <b>randomness most "
          "often buys simplicity and adversary-resistance, and only rarely "
          "a complexity class</b> — which is exactly what &sect;3 "
          "explains."]),

  ("break",),
  ("h1", "3 &nbsp; Why BPP is believed to equal P"),
  ("callout", "BPP = P is the expectation, and the reason is "
              "pseudorandomness",
   ["<b>A pseudorandom generator stretches a short random seed into a "
    "long string that no efficient algorithm can distinguish from a truly "
    "random one.</b> <b>Note that this is a <i>computational</i> notion "
    "of randomness, not a statistical one</b> — the output is "
    "demonstrably not random and no efficient test can tell.",
    "<b>If such generators exist, a BPP algorithm can be run on "
    "pseudorandom bits derived from <i>every</i> seed in turn, and the "
    "majority taken</b> — which is entirely deterministic, and "
    "polynomial-time because the seeds are short (logarithmically many "
    "bits) so there are polynomially many of them.",
    "<b>And strong enough generators follow from circuit lower "
    "bounds</b> (Module 09): <b>Nisan and Wigderson showed that if "
    "some problem in E requires circuits of size "
    "2<super>&epsilon;n</super>, then BPP = P.</b>",
    "<b>So hardness implies derandomisation.</b> <b>The existence of "
    "hard problems is what makes randomness unnecessary</b> — "
    "<b>which is the most counterintuitive result in this course</b>, and "
    "is genuinely beautiful: you would expect hardness and the usefulness "
    "of randomness to point the same way, and they point opposite ways."]),
  ("code", """THE INTUITION: a sequence is random ENOUGH if no efficient
observer can tell it from random. That is a COMPUTATIONAL
notion, not a statistical one -- and it is the whole idea.

SO: take a function f that is HARD to compute. Its output
bits look unpredictable to anything that cannot compute it.
Use f to stretch a short seed into a long string.

    NISAN-WIGDERSON: if some f in E requires circuits of
    size 2^(eps n), then there is a pseudorandom generator
    fooling all polynomial-size circuits -- which gives
    BPP = P.

THE SHAPE OF THE ARGUMENT
    HARD PROBLEMS EXIST  =>  PSEUDORANDOMNESS EXISTS
                         =>  RANDOMNESS IS REMOVABLE

AND THE CONVERSE HOLDS PARTIALLY: derandomising polynomial
identity testing would imply circuit lower bounds
(Impagliazzo-Kabanets). So the two questions are tied
together in both directions.

WHICH MEANS: whether randomness helps is not an independent
question. It is the SAME question as whether hard problems
exist -- and that is Module 09's subject."""),

  ("h1", "4 &nbsp; What follows"),
  ("ul", ["<b>Use randomised algorithms freely.</b> "
          "<b>2<super>&minus;100</super> error is below the hardware "
          "fault rate</b> (&sect;1's callout), <b>and the randomised "
          "algorithm is usually simpler than the deterministic one</b> "
          "— which is a real engineering benefit independent of any "
          "complexity question.",
          "<b>Prefer one-sided error when it is available.</b> <b>A "
          "found factor is a certainty; a Miller–Rabin 'probably "
          "prime' is not</b> — and <b>the difference matters inside "
          "a protocol</b>, where a false positive and a false negative "
          "have different consequences.",
          "<b>And distinguish Las Vegas from Monte Carlo.</b> <b>Random "
          "runtime with a guaranteed-correct answer (ZPP) is usually "
          "preferable to guaranteed runtime with a possibly-wrong "
          "answer</b>, because the first can be retried and the second "
          "cannot be detected.",
          "<b>Randomness does not escape NP-hardness.</b> <b>BPP is not "
          "believed to contain NP</b>, so <b>a coin will not solve your "
          "NP-complete problem</b> — which is the practical headline "
          "and the thing people most often hope for.",
          "<b>And the quality of your randomness matters.</b> <b>A weak "
          "generator can void the guarantee entirely</b>, which is a "
          "security problem rather than a complexity one (CSCE 711) "
          "and has caused real failures — so 'randomised algorithm' "
          "assumes a source you have actually checked."]),
  ("callout", "The bridge to CSCE 658",
   ["<b>This module is the complexity-class view of randomness. "
    "CSCE 658 is the algorithm-design view</b> — how to construct "
    "randomised algorithms, analyse them with concentration bounds, and "
    "bound their failure probabilities.",
    "<b>And the two meet at derandomisation:</b> <b>CSCE 658 covers "
    "the method of conditional expectations and limited "
    "independence</b>, which remove randomness from <i>specific</i> "
    "algorithms rather than from a whole class — a concrete and "
    "achievable version of &sect;3's conditional result.",
    "<b>So the question 'does randomness help?' has a class-level answer "
    "(probably not, conditionally on circuit lower bounds) and an "
    "algorithm-level answer (frequently, for simplicity and "
    "robustness).</b>",
    "<b>Which are both correct and are about different things</b> "
    "— one is about the existence of an equally fast deterministic "
    "algorithm and the other is about which algorithm you should write "
    "— <b>and keeping them apart is the main thing to carry from "
    "this module into the next course.</b>"]),
 ],
 "resources": [
   ("Arora & Barak &mdash; chapters 7 and 20 (free draft)",
    "https://theory.cs.princeton.edu/complexity/",
    "<b>The randomised classes, and the derandomisation chapter</b> "
    "— the reference for &sect;1 and &sect;3."),
   ("Nisan & Wigderson &mdash; Hardness vs Randomness (free)",
    "https://www.sciencedirect.com/science/article/pii/002200009490001X",
    "<b>&sect;3's central result</b>, and the title is the whole "
    "point."),
   ("Impagliazzo & Kabanets &mdash; Derandomizing Polynomial Identity "
    "Tests Means Proving Circuit Lower Bounds (free)",
    "https://link.springer.com/article/10.1007/s00037-004-0182-6",
    "<b>&sect;3's converse direction</b>, which ties the two questions "
    "together."),
   ("Motwani & Raghavan &mdash; Randomized Algorithms",
    "https://www.cambridge.org/core/books/randomized-algorithms/6A3E5CD760413BEF7D0D01BFD5497ACB",
    "<b>The algorithm-design companion</b>, and CSCE 658's main text. "
    "Library copy."),
 ],
 "exercises": [
   "<b>Implement Miller–Rabin</b> and measure the error rate "
   "empirically against known composites.",
   "<b>Amplify the error by repetition</b> and confirm the exponential "
   "decay.",
   "<b>Compute how many repetitions give error below "
   "10⁻²⁰</b>, and compare against a hardware fault "
   "rate.",
   "<b>Implement randomised polynomial identity testing</b> and construct "
   "an expression where the symbolic approach is infeasible.",
   "<b>Classify five randomised algorithms you know</b> as BPP, RP, "
   "co-RP, or ZPP.",
   "<b>Explain why PP is not useful</b>, with the sampling argument.",
   "<b>Derandomise a simple randomised algorithm</b> by trying all seeds "
   "of logarithmic length.",
   "<b>Explain the hardness-to-randomness direction</b> in your own "
   "words.",
   "<b>Find a case where a weak random source broke a system</b> and "
   "describe it.",
   "<b>Write down whether you expect BPP = P</b>, with reasons.",
 ],
 "selfcheck": [
   "Define BPP, RP, co-RP, ZPP, and PP, and say which is useless and "
   "why.",
   "Explain error amplification and why the constant does not matter.",
   "Why must the error be bounded away from a half?",
   "Give five places randomness demonstrably helped, and the pattern "
   "across them.",
   "Why is BPP believed to equal P?",
   "State Nisan–Wigderson and the shape of its argument.",
   "Why is 'does randomness help' the same question as 'do hard problems "
   "exist'?",
   "Give five practical readings.",
   "Distinguish the class-level and algorithm-level answers.",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Circuits",
 "subtitle": "A non-uniform model, and the most promising attack.",
 "question": "If you allow a different program for each input length, "
             "does that help?",
 "outcomes": [
     "Define circuit complexity and the class P/poly.",
     "Explain non-uniformity and what it buys.",
     "State the known circuit lower bounds and their limits.",
     "Explain the natural proofs barrier.",
     "Explain why circuits were the favoured attack.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The model",
   "blurb": "A different circuit for each input length."},

  {"t": "callout", "title": "A circuit family is a non-uniform program, which is strictly more powerful",
   "kind": "The model, and the subtlety",
   "body": ["<b>A Boolean circuit computes one function on a fixed "
            "number of inputs.</b> <b>A <i>family</i> gives one circuit "
            "per input length</b>, and P/poly is the problems with "
            "polynomial-size families.",
            "<b>And nobody has to be able to <i>construct</i> the "
            "circuits</b> — that is the non-uniformity, and it is "
            "where the extra power comes from.",
            "<b>So P/poly contains undecidable problems:</b> <b>any "
            "unary language is decided by a trivial circuit per "
            "length</b>, including unary encodings of the halting "
            "problem.",
            "<b>Which means P/poly is not a model of computation</b> "
            "— <b>it is a model of <i>circuit size</i></b>, and its "
            "value is that lower bounds against it are strong and that "
            "P ⊆ P/poly."]},

  {"t": "callout", "title": "Why circuits were the favoured attack on P versus NP",
   "kind": "The programme",
   "body": ["<b>P ⊆ P/poly.</b> <b>So proving that SAT needs "
            "super-polynomial circuits would prove P ≠ NP</b> "
            "— a stronger statement, and a combinatorial one.",
            "<b>And circuits are finite combinatorial objects</b> with "
            "no computation, no time, and no simulation — which "
            "<b>evades the relativisation barrier</b> "
            "(Module 07 §2), because there is no machine to "
            "give an oracle to.",
            "<b>And the technique worked on restricted models:</b> "
            "<b>exponential lower bounds for monotone circuits, "
            "bounded-depth circuits, and formulas</b> are all proved.",
            "<b>So for a decade it looked like the route.</b> <b>Then "
            "Razborov and Rudich proved that the successful technique "
            "cannot be extended</b> (Part 3) — which is the second "
            "barrier."]},

  {"t": "section", "label": "Part 2", "title": "What is proved",
   "blurb": "Real lower bounds, on restricted models."},

  {"t": "table", "kicker": "Lower bounds", "title": "What has been proved, and against what",
   "header": ["Model", "Result", "Note"],
   "widths": [3.0, 3.8, 5.2],
   "rows": [
     ["<b>Monotone circuits</b>", "<b>Exponential for clique</b>", "<b>Razborov, 1985. No NOT gates allowed</b>"],
     ["<b>Bounded depth (AC⁰)</b>", "<b>Parity needs super-polynomial size</b>", "<b>Håstad's switching lemma</b>"],
     ["<b>AC⁰ with mod-p gates</b>", "<b>Lower bounds known</b>", "<b>Razborov–Smolensky, by polynomial approximation</b>"],
     ["<b>Formulas (fan-out 1)</b>", "<b>Quadratic for some functions</b>", "<b>Khrapchenko and successors</b>"],
     ["<b>General circuits</b>", "<b>Best known: about 5n</b>", "<b>For an explicit function. Essentially nothing</b>"],
   ],
   "footnote": "<b>The last row is the honest state:</b> <b>no "
               "super-linear lower bound is known for general circuits "
               "computing any explicit function</b>, and we believe SAT "
               "needs exponential size.",
   "note": "The 5n figure is the most sobering number in the course."},

  {"t": "callout", "title": "The gap between 5n and exponential is the whole problem",
   "kind": "Said plainly",
   "body": ["<b>We believe SAT requires circuits of size "
            "2^Ω(n).</b> <b>We can prove about 5n.</b>",
            "<b>And counting shows most Boolean functions require "
            "exponential circuits</b> — there are 2^(2ⁿ) "
            "functions and far fewer small circuits.",
            "<b>So hard functions are abundant, and we cannot exhibit "
            "one</b> — which is <b>exactly CSCE 627 §04's "
            "counting-versus-construction distinction</b>, in a different "
            "subject.",
            "<b>Which is a useful calibration:</b> <b>the field's "
            "central conjecture is an exponential gap away from what it "
            "can prove</b>, and knowing that number is more informative "
            "than knowing the consensus."]},

  {"t": "section", "label": "Part 3", "title": "Natural proofs",
   "blurb": "The second barrier."},

  {"t": "code", "kicker": "Natural proofs", "title": "Why the successful technique cannot be extended",
   "lang": "text", "code": """
  THE SUCCESSFUL LOWER BOUNDS all have one shape: find a
  PROPERTY of Boolean functions such that
      the hard function HAS it
      and every small-circuit function does NOT

  Razborov and Rudich called such a property NATURAL if it
  is
      CONSTRUCTIVE -- efficiently checkable from the
          function's truth table
      LARGE        -- most random functions have it

  Every known lower-bound proof uses a natural property.

  THE BARRIER: if strong one-way functions exist, then no
  natural property can separate P from NP.

  WHY: a natural property is an efficient test that
  distinguishes random functions from easy ones. But a
  pseudorandom function generator (which exists if one-way
  functions do) produces EASY functions that look RANDOM to
  every efficient test. So the property cannot exist.

  SO: the technique that proved every known lower bound
  cannot prove the one we want -- assuming exactly the kind
  of hardness we are trying to establish.
""",
   "caption": "<b>The barrier assumes the hardness it blocks you from "
              "proving</b>, which is the self-referential sting — "
              "and it is the same shape as CSCE 627's barriers.",
   "note": "The self-referential character is what makes this result so "
           "striking."},

  {"t": "section", "label": "Part 4", "title": "Where it stands",
   "blurb": "And the one useful circuit class."},

  {"t": "callout", "title": "Karp–Lipton: NP in P/poly would collapse the hierarchy",
   "kind": "The structural consequence",
   "body": ["<b>If NP ⊆ P/poly, then the polynomial hierarchy "
            "collapses to the second level.</b>",
            "<b>So NP is believed not to be in P/poly</b>, which means "
            "<b>SAT is believed to need super-polynomial circuits even "
            "allowing non-uniformity</b> — a stronger belief than "
            "P ≠ NP.",
            "<b>And this is Module 05 §4's reasoning "
            "style:</b> <b>'X would collapse the hierarchy' deployed as "
            "evidence that X is false.</b>",
            "<b>Which also means the circuit programme is attacking the "
            "right thing</b> — <b>a super-polynomial circuit lower "
            "bound for SAT is both sufficient for P ≠ NP and "
            "believed true.</b>"]},

  {"t": "bullets", "kicker": "Useful", "title": "The circuit classes that are practically meaningful",
   "items": [
     "<b>AC⁰: constant depth, unbounded fan-in.</b> <b>Parity is "
     "not in it</b> — which is a real, unconditional, and "
     "practically meaningful limitation.",
     "",
     "<b>NC: polylogarithmic depth.</b> <b>Efficiently "
     "parallelisable</b> (Module 06 §4) — <b>the circuit "
     "view is the natural one for parallelism.</b>",
     "",
     "<b>NC¹ and formulas</b>, which correspond to bounded-width "
     "and expression-depth notions in real hardware.",
     "",
     "<b>And circuit <i>depth</i> is latency and circuit "
     "<i>size</i> is area</b> — which is why this model is the "
     "natural one for hardware (CSCE 614).",
     "",
     "<b>So the model has engineering content independent of the P "
     "versus NP programme</b>, which is worth separating.",
   ],
   "footnote": "<b>Depth equals latency is the connection to "
               "CSCE 614</b> — a circuit lower bound on depth is a "
               "statement about how fast hardware can possibly be."},
 ],
 "takeaways": [
   "A circuit family is non-uniform — nobody has to be able to "
   "construct the circuits — so P/poly contains undecidable "
   "problems and is a model of size rather than of computation.",
   "Circuits were the favoured attack because P ⊆ P/poly, they are "
   "finite combinatorial objects, and they evade relativisation.",
   "Real exponential lower bounds are proved for monotone and "
   "bounded-depth circuits, and the best general bound is about 5n.",
   "Counting shows most functions need exponential circuits and we cannot "
   "exhibit one, which is CSCE 627's counting-versus-construction gap "
   "again.",
   "Every known lower bound uses a natural property, and no natural "
   "property can separate P from NP if strong one-way functions exist.",
   "Karp–Lipton says NP in P/poly would collapse the hierarchy, so "
   "the circuit programme is attacking something believed true.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The model, and why it was the favoured attack"),
  ("callout", "A circuit family is a non-uniform program, which is strictly "
              "more powerful",
   ["<b>A Boolean circuit computes a single function on a fixed number of "
    "input bits.</b> <b>A <i>family</i> provides one circuit per input "
    "length</b>, and <b>P/poly is the class of problems decided by "
    "families of polynomial size.</b>",
    "<b>And crucially, nobody has to be able to <i>construct</i> the "
    "circuits</b> — the family simply exists. <b>That is the "
    "non-uniformity, and it is where the extra power comes from</b>: a "
    "uniform model must produce its behaviour with one finite program, and "
    "a non-uniform one may have a different program for every length.",
    "<b>So P/poly contains undecidable problems.</b> <b>Any unary "
    "language is decided by a trivial circuit per length</b> — "
    "accept or reject, constant — <b>including a unary encoding of "
    "the halting problem.</b> Which settles immediately that P/poly is "
    "not a model of anything you can run.",
    "<b>Which means P/poly is not a model of computation</b> — "
    "<b>it is a model of <i>circuit size</i></b> — <b>and its value "
    "is twofold: lower bounds against it are correspondingly strong "
    "statements, and P is contained in it</b>, which is what makes those "
    "lower bounds relevant (&sect;1's second callout)."]),
  ("callout", "Why circuits were the favoured attack on P versus NP",
   ["<b>P is contained in P/poly</b> — convert the "
    "polynomial-time machine's computation on each input length into a "
    "circuit, which is the Cook–Levin tableau construction "
    "(Module 04 &sect;2) read as a circuit. <b>So proving that SAT "
    "requires super-polynomial circuits would prove P &ne; NP</b>, and it "
    "would prove something stronger.",
    "<b>And circuits are finite combinatorial objects</b> with no "
    "computation, no time, no simulation, and no machine — which "
    "<b>evades the relativisation barrier</b> (Module 07 &sect;2) "
    "<b>because there is nothing to attach an oracle to.</b> That was "
    "the hope, and it was a reasonable one.",
    "<b>And the technique worked on restricted models:</b> "
    "<b>exponential lower bounds were proved for monotone circuits, for "
    "bounded-depth circuits, and for formulas</b> (&sect;2's table) "
    "— real theorems, by real techniques, in the expected "
    "direction.",
    "<b>So for about a decade this looked like the route to P &ne; "
    "NP.</b> <b>Then Razborov and Rudich proved in 1994 that the "
    "technique behind every one of those successes cannot be extended to "
    "general circuits</b> (&sect;3) — <b>which is the second "
    "barrier, and the one that most changed the field's mood.</b>"]),

  ("h1", "2 &nbsp; What has been proved"),
  ("table", ["Model", "Result", "Note"],
   [["<b>Monotone circuits</b> (AND and OR only, no negation)",
     "<b>Exponential lower bound for clique.</b>",
     "<b>Razborov, 1985</b> — the result that started the "
     "optimism. And the restriction is severe: the same function has "
     "small non-monotone circuits in some related cases."],
    ["<b>Bounded depth, unbounded fan-in (AC<super>0</super>)</b>",
     "<b>Parity requires super-polynomial size.</b>",
     "<b>H&aring;stad's switching lemma</b> — unconditional, "
     "practically meaningful, and one of the field's genuine "
     "successes."],
    ["<b>AC<super>0</super> with mod-p counting gates</b>",
     "<b>Lower bounds known for appropriate functions.</b>",
     "<b>Razborov–Smolensky, by approximating circuits with "
     "low-degree polynomials.</b>"],
    ["<b>Formulas (circuits of fan-out 1)</b>",
     "<b>Quadratic lower bounds for explicit functions.</b>",
     "Khrapchenko and successors."],
    ["<b>General circuits</b>",
     "<b>The best known bound is about 5n gates</b>, for an explicit "
     "function.",
     "<b>Essentially nothing.</b> See the callout."]],
   [0.26, 0.32, 0.42]),
  ("callout", "The gap between 5n and exponential is the whole problem",
   ["<b>We believe SAT requires circuits of size "
    "2<super>&Omega;(n)</super>. We can prove about 5n.</b> <b>That is "
    "the state of the art, and it is worth stating as two numbers rather "
    "than as a description.</b>",
    "<b>And a counting argument shows that most Boolean functions "
    "require exponential-size circuits</b> — there are "
    "2<super>2<super>n</super></super> functions on n bits and far fewer "
    "circuits of subexponential size, so almost all functions are hard.",
    "<b>So hard functions are abundant, and we cannot exhibit a single "
    "one</b> — which is <b>exactly CSCE 627 Module 04 "
    "&sect;4's counting-versus-construction distinction</b>, arriving in "
    "a different subject with the same structure: an easy existence proof "
    "and no constructive one.",
    "<b>Which is a useful calibration.</b> <b>The field's central "
    "conjecture is an exponential gap away from what it can prove</b>, "
    "<b>and knowing that number is considerably more informative than "
    "knowing the consensus</b> — it is the most sobering figure in "
    "the course, and it should temper any sense that P &ne; NP is nearly "
    "established."]),

  ("break",),
  ("h1", "3 &nbsp; The natural proofs barrier"),
  ("code", """THE SUCCESSFUL LOWER BOUNDS all have one shape: find a
PROPERTY of Boolean functions such that
    the hard function HAS it
    and every small-circuit function does NOT

Razborov and Rudich called such a property NATURAL if it is
    CONSTRUCTIVE -- efficiently checkable from the
        function's truth table
    LARGE        -- a random function has it with
        non-negligible probability

Every known circuit lower-bound proof uses a property that
is natural in this sense.

THE BARRIER: if strong one-way functions exist, then no
natural property can separate P from NP.

WHY: a natural property is, by definition, an efficient
test that distinguishes random functions from functions
with small circuits. But a pseudorandom function generator
-- which exists if one-way functions do -- produces
functions that HAVE small circuits and that look RANDOM to
every efficient test. So no such test can exist.

SO: the technique that proved every known lower bound
cannot prove the one we want -- assuming exactly the kind
of hardness we are trying to establish."""),
  ("p", "<b>The barrier assumes the hardness it blocks you from "
        "proving</b>, which is the self-referential sting and is what "
        "makes the result so striking — <b>if one-way functions do "
        "not exist then cryptography fails and P versus NP is probably "
        "settled the other way, so the assumption is one almost everyone "
        "in the field already makes.</b> <b>And it is the same shape as "
        "CSCE 627 Module 05's proofs and Module 07 &sect;2's "
        "relativisation</b>: a technique's limits established by turning "
        "the technique on itself."),

  ("h1", "4 &nbsp; Where it stands, and the useful classes"),
  ("callout", "Karp–Lipton: NP in P/poly would collapse the hierarchy",
   ["<b>If NP is contained in P/poly, then the polynomial hierarchy "
    "collapses to its second level</b> (Module 05 &sect;3).",
    "<b>So NP is believed not to be in P/poly</b>, which means <b>SAT is "
    "believed to require super-polynomial circuits even when "
    "non-uniformity is allowed</b> — <b>a strictly stronger belief "
    "than P &ne; NP</b>, since P/poly contains P and much else.",
    "<b>And this is Module 05 &sect;4's reasoning style again:</b> "
    "<b>'X would collapse the hierarchy' deployed as evidence that X is "
    "false</b> — a conditional theorem used as a plausibility "
    "argument.",
    "<b>Which also means the circuit programme is attacking the right "
    "thing.</b> <b>A super-polynomial circuit lower bound for SAT is "
    "both sufficient for P &ne; NP and independently believed true</b>, "
    "so the programme is not aiming at something that might be false "
    "— it is aiming at something nobody can prove."]),
  ("ul", ["<b>AC<super>0</super>: constant depth, unbounded fan-in.</b> "
          "<b>Parity is provably not in it</b> — which is a real, "
          "unconditional, and practically meaningful limitation: no "
          "constant-depth circuit of polynomial size computes parity, "
          "whatever the technology.",
          "<b>NC: polylogarithmic depth, polynomial size.</b> "
          "<b>Efficiently parallelisable</b> (Module 06 &sect;4) "
          "— <b>and the circuit view is the natural one for "
          "parallelism</b>, because depth is parallel time directly rather "
          "than by analogy.",
          "<b>NC<super>1</super> and the formula classes</b>, which "
          "correspond to bounded-width and expression-depth notions that "
          "appear in real hardware design and in compiler expression "
          "trees.",
          "<b>And circuit <i>depth</i> is latency while circuit "
          "<i>size</i> is area</b> — <b>which is why this model is "
          "the natural one for hardware</b> (CSCE 614), and why circuit "
          "complexity has an engineering readership independent of its "
          "theoretical one.",
          "<b>So the model has engineering content independent of the P "
          "versus NP programme</b>, <b>which is worth separating</b>: "
          "the AC<super>0</super> parity bound is a useful fact about what "
          "hardware can do in constant depth, and it is true regardless of "
          "what happens to the central question."]),
 ],
 "resources": [
   ("Arora & Barak &mdash; chapters 6, 14, and 23 (free draft)",
    "https://theory.cs.princeton.edu/complexity/",
    "<b>Circuits, the known lower bounds, and the natural proofs "
    "barrier</b> — chapter 23 covers &sect;3 properly."),
   ("Razborov & Rudich &mdash; Natural Proofs (free)",
    "https://www.sciencedirect.com/science/article/pii/S0022000097914947",
    "<b>&sect;3's barrier, in the original</b> — and the "
    "definitions of constructive and large are worth reading exactly."),
   ("Håstad &mdash; Computational Limitations of Small-Depth "
    "Circuits",
    "https://people.kth.se/~johanh/thesis.pdf",
    "<b>&sect;2's switching lemma and the parity lower bound</b>, free "
    "from the author."),
   ("Aaronson &mdash; P =? NP, the circuit sections (free)",
    "https://www.scottaaronson.com/papers/pnp.pdf",
    "<b>&sect;2's calibration and &sect;4's assessment</b>, including the "
    "5n figure and what it means."),
 ],
 "exercises": [
   "<b>Build a circuit for a small function</b> and count its gates and "
   "depth.",
   "<b>Show that any unary language is in P/poly</b>, including an "
   "undecidable one.",
   "<b>Explain why that means P/poly is not a model of computation.</b>",
   "<b>Convert a polynomial-time algorithm into a circuit family</b> for "
   "a small input length, and verify the size is polynomial.",
   "<b>Count the Boolean functions on 5 inputs</b> and the circuits of "
   "size 20, and conclude.",
   "<b>Try to prove a super-linear lower bound</b> for an explicit "
   "function, and report where you get stuck.",
   "<b>State the two conditions for a natural property</b> and check them "
   "against one known lower bound.",
   "<b>Explain the natural proofs barrier</b> in your own words, "
   "including why the assumption is reasonable.",
   "<b>State Karp–Lipton</b> and explain how it is used as "
   "evidence.",
   "<b>Relate circuit depth to hardware latency</b> for a circuit you "
   "have seen in CSCE 614.",
 ],
 "selfcheck": [
   "Define a circuit family and P/poly, and say why it is "
   "non-uniform.",
   "Why does P/poly contain undecidable problems, and what does that "
   "mean?",
   "Give three reasons circuits were the favoured attack.",
   "Name five lower bound results and the model each is against.",
   "What is the best general circuit lower bound, and what do we "
   "believe?",
   "Why is the counting argument not enough?",
   "Define a natural property and state the barrier.",
   "Why is the barrier self-referential?",
   "State Karp–Lipton and its use.",
   "Name the practically meaningful circuit classes and the hardware "
   "connection.",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Interactive Proofs",
 "subtitle": "What you can be convinced of by a conversation.",
 "question": "If you may ask questions, what can be proved to you?",
 "outcomes": [
     "Define an interactive proof and explain the two conditions.",
     "Explain the graph non-isomorphism protocol.",
     "State IP = PSPACE and explain arithmetisation.",
     "State the PCP theorem and explain what it says.",
     "Explain zero-knowledge and its practical use.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The model",
   "blurb": "A prover, a verifier, and randomness."},

  {"t": "callout", "title": "An interactive proof is a conversation with a randomised verifier",
   "kind": "The model, and the two conditions",
   "body": ["<b>An unbounded prover and a polynomial-time randomised "
            "verifier exchange messages.</b> <b>The verifier accepts or "
            "rejects at the end.</b>",
            "<b>Completeness:</b> if the statement is true, an honest "
            "prover convinces the verifier with high probability.",
            "<b>Soundness:</b> if it is false, <i>no</i> prover "
            "convinces the verifier except with small probability.",
            "<b>And the two ingredients are both essential.</b> "
            "<b>Interaction alone adds nothing — a deterministic "
            "verifier's questions are predictable, so the prover can send "
            "the whole transcript</b> and you are back to NP. <b>It is "
            "the randomness that the prover cannot anticipate.</b>"]},

  {"t": "code", "kicker": "The example", "title": "Graph non-isomorphism, which has no known certificate",
   "lang": "text", "code": """
  TO PROVE: G1 and G2 are NOT isomorphic.
  (No short certificate is known -- Module 05 Part 1.)

  THE PROTOCOL
      the VERIFIER picks i in {1,2} at random, and a random
          permutation; sends the permuted copy of G_i
      the PROVER says which of G1, G2 it came from
      repeat k times; accept if the prover is always right

  IF THEY ARE NOT ISOMORPHIC: the prover can always tell,
  because the permuted graph is isomorphic to exactly one
  of them. Always right. ACCEPT.

  IF THEY ARE ISOMORPHIC: the permuted graph is isomorphic
  to BOTH, so the prover is guessing. Right with
  probability 2^-k. REJECT, almost certainly.

  NOTE WHAT MADE IT WORK: the verifier's random choice is
  HIDDEN FROM THE PROVER. A deterministic verifier's choice
  would be predictable and the protocol would prove
  nothing.

  SO INTERACTION PLUS RANDOMNESS CAN CERTIFY SOMETHING WITH
  NO CERTIFICATE.
""",
   "caption": "<b>The hidden random choice is the whole mechanism</b> "
              "— and it is why IP is not simply NP with extra "
              "steps.",
   "note": "This example is the best motivation for the whole module."},

  {"t": "section", "label": "Part 2", "title": "IP = PSPACE",
   "blurb": "Interaction is exactly as powerful as polynomial space."},

  {"t": "callout", "title": "IP = PSPACE, by arithmetisation",
   "kind": "The theorem, and why it matters methodologically",
   "body": ["<b>Interactive proofs capture exactly PSPACE</b> "
            "— so <b>anything decidable in polynomial space can be "
            "proved to a polynomial-time verifier by conversation</b>, "
            "which is far more than NP.",
            "<b>The technique is arithmetisation:</b> convert the "
            "Boolean formula of TQBF into a polynomial over a finite "
            "field, and have the prover make claims about its values "
            "— which the verifier spot-checks at random points.",
            "<b>And it works because low-degree polynomials are "
            "rigid:</b> <b>two distinct low-degree polynomials disagree "
            "almost everywhere</b>, so a lying prover is caught by a "
            "random check.",
            "<b>And this is the result that does not "
            "relativise</b> (Module 07 §3) — <b>which is "
            "why the technique mattered, and why the algebrisation "
            "barrier had to be constructed afterwards.</b>"]},

  {"t": "section", "label": "Part 3", "title": "The PCP theorem",
   "blurb": "A proof you can check by reading three bits."},

  {"t": "callout", "title": "PCP: every NP proof can be rewritten so that reading a constant number of bits suffices",
   "kind": "One of the deepest results in the field",
   "body": ["<b>NP = PCP(log n, 1).</b> <b>Every NP statement has a "
            "proof that a verifier using O(log n) random bits and reading "
            "a <i>constant</i> number of proof bits can check.</b>",
            "<b>A true statement's proof always passes; a false "
            "statement's purported proof fails with constant "
            "probability</b> — from reading three bits.",
            "<b>The mechanism is that the proof is written in an "
            "error-correcting form</b>, so any error is spread "
            "everywhere and a random spot-check finds it.",
            "<b>And its most useful consequence is hardness of "
            "approximation</b> (Module 11, CSCE 669 §10) "
            "— <b>the gap between a passing and failing proof becomes "
            "a gap in an optimisation problem, which is what makes "
            "inapproximability provable.</b>"]},

  {"t": "table", "kicker": "PCP", "title": "What the theorem gives",
   "header": ["Consequence", "Why it follows"],
   "widths": [4.4, 6.6],
   "rows": [
     ["<b>Hardness of approximation</b>", "<b>The accept/reject gap becomes an approximation gap (M11)</b>"],
     ["<b>MAX-3SAT cannot be approximated beyond 7/8</b>", "<b>Directly, and 7/8 is achievable — so the bound is tight</b>"],
     ["<b>Set cover's log n is optimal</b>", "<b>Which CSCE 669 §10 asserted and this proves</b>"],
     ["<b>Succinct, spot-checkable proofs in practice</b>", "<b>SNARKs and verifiable computation descend from this</b>"],
   ],
   "footnote": "<b>The practical descendants are real:</b> <b>succinct "
               "proof systems in deployed cryptographic systems are PCP's "
               "engineering grandchildren</b>, which is unusual for a "
               "result this abstract.",
   "note": "The SNARK connection makes PCP feel less remote."},

  {"t": "section", "label": "Part 4", "title": "Zero knowledge",
   "blurb": "Proving you know something without revealing it."},

  {"t": "callout", "title": "Zero-knowledge: the verifier learns the statement is true and nothing else",
   "kind": "The definition, and it is subtle",
   "body": ["<b>A proof is zero-knowledge if the verifier's view of the "
            "conversation could have been <i>simulated</i> without the "
            "prover</b> — so the transcript carries no information "
            "beyond the statement's truth.",
            "<b>The classic example is three-colouring:</b> commit to a "
            "colouring, let the verifier open one edge, repeat. <b>Each "
            "round reveals two different colours and nothing about the "
            "colouring.</b>",
            "<b>And every NP statement has a zero-knowledge proof</b>, "
            "assuming commitments exist — which is a striking general "
            "result.",
            "<b>The practical use is authentication and "
            "privacy-preserving verification</b> — <b>proving you "
            "are authorised without revealing which credential, or that a "
            "transaction is valid without revealing its contents.</b>"]},

  {"t": "bullets", "kicker": "Summary", "title": "What this module establishes",
   "items": [
     "<b>Interaction plus randomness certifies statements with no "
     "certificate</b> — graph non-isomorphism is the "
     "demonstration.",
     "",
     "<b>And the randomness must be hidden from the prover</b>, which "
     "is where the power comes from.",
     "",
     "<b>IP = PSPACE</b>, by arithmetisation — <b>and that is the "
     "technique that evaded relativisation</b> "
     "(Module 07 §3).",
     "",
     "<b>PCP rewrites NP proofs so three bits suffice</b>, which gives "
     "hardness of approximation and, eventually, SNARKs.",
     "",
     "<b>And every NP statement has a zero-knowledge proof</b>, which "
     "is the most directly applied result in the course.",
   ],
   "footnote": "<b>This is the module where complexity theory produced "
               "deployed technology</b>, which is worth noting in a "
               "course otherwise about what cannot be done."},
 ],
 "takeaways": [
   "An interactive proof needs completeness and soundness, and interaction "
   "alone adds nothing — it is the randomness the prover cannot "
   "anticipate that gives the power.",
   "Graph non-isomorphism has an interactive proof and no known "
   "certificate, which is the whole motivation for the model.",
   "IP = PSPACE by arithmetisation, and that technique is what evaded the "
   "relativisation barrier.",
   "Low-degree polynomials are rigid — two distinct ones disagree "
   "almost everywhere — which is why random spot-checking catches a "
   "lying prover.",
   "PCP says every NP proof can be rewritten so that reading a constant "
   "number of bits suffices, via an error-correcting encoding.",
   "Its most useful consequence is hardness of approximation, and its "
   "engineering descendants are deployed succinct proof systems.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The model"),
  ("callout", "An interactive proof is a conversation with a randomised "
              "verifier",
   ["<b>A computationally unbounded prover and a polynomial-time "
    "randomised verifier exchange messages for polynomially many "
    "rounds.</b> <b>The verifier then accepts or rejects.</b>",
    "<b>Completeness:</b> if the statement is true, an honest prover "
    "convinces the verifier with high probability.",
    "<b>Soundness:</b> if the statement is false, <i>no</i> prover "
    "— however powerful or dishonest — convinces the verifier "
    "except with small probability. <b>The quantifier over provers is the "
    "important part.</b>",
    "<b>And both ingredients are essential.</b> <b>Interaction alone "
    "adds nothing:</b> if the verifier is deterministic, its questions are "
    "predictable, so the prover can simply send the entire transcript in "
    "advance — <b>and you are back to NP</b> (Module 03 "
    "&sect;1's certificate). <b>It is the randomness, hidden from the "
    "prover, that the prover cannot anticipate</b>, and &sect;1's "
    "protocol shows exactly how that is exploited."]),
  ("code", """TO PROVE: G1 and G2 are NOT isomorphic.
(No short certificate is known -- Module 05 section 1.)

THE PROTOCOL
    the VERIFIER picks i in {1,2} at random, and a random
        permutation; sends the permuted copy of G_i
    the PROVER says which of G1, G2 it came from
    repeat k times; accept if the prover is always right

IF THEY ARE NOT ISOMORPHIC: the prover (being unbounded)
can always tell, because the permuted graph is isomorphic
to exactly one of the two. Always right. ACCEPT.

IF THEY ARE ISOMORPHIC: the permuted graph is isomorphic to
BOTH, so the prover has no information and is guessing.
Right with probability 2^-k. REJECT, almost certainly.

NOTE WHAT MADE IT WORK: the verifier's random choice of i
is HIDDEN FROM THE PROVER. A deterministic verifier's
choice would be predictable, and the protocol would prove
nothing at all.

SO INTERACTION PLUS RANDOMNESS CAN CERTIFY SOMETHING THAT
HAS NO CERTIFICATE."""),

  ("h1", "2 &nbsp; IP = PSPACE"),
  ("callout", "IP = PSPACE, by arithmetisation",
   ["<b>Interactive proofs capture exactly PSPACE</b> — so "
    "<b>anything decidable in polynomial space can be proved to a "
    "polynomial-time verifier by conversation</b>, which is far more than "
    "NP and was a considerable surprise when proved in 1990.",
    "<b>The technique is arithmetisation:</b> convert the quantified "
    "Boolean formula of TQBF (Module 05 &sect;2) into a polynomial "
    "over a finite field, with AND becoming multiplication and the "
    "quantifiers becoming sums or products over the field. <b>The prover "
    "then makes claims about the polynomial's values, which the verifier "
    "spot-checks at randomly chosen points.</b>",
    "<b>And it works because low-degree polynomials are rigid:</b> "
    "<b>two distinct polynomials of low degree agree at only a few "
    "points, so they disagree almost everywhere</b> — <b>which means "
    "a prover who lies about the polynomial is caught by a random check "
    "with high probability.</b> <b>The rigidity of polynomials is doing "
    "all the work</b>, and it is the same property behind "
    "error-correcting codes and Module 08's identity testing.",
    "<b>And this is the result that does not relativise</b> "
    "(Module 07 &sect;3) — <b>which is why the technique "
    "mattered methodologically</b>, far beyond the theorem itself, <b>and "
    "why the algebrisation barrier had to be constructed afterwards</b> to "
    "determine whether it could reach P versus NP. <b>It could not.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; The PCP theorem"),
  ("callout", "PCP: every NP proof can be rewritten so that reading a "
              "constant number of bits suffices",
   ["<b>NP = PCP(log n, 1).</b> <b>Every statement in NP has a proof "
    "that a verifier using O(log n) random bits and reading a "
    "<i>constant</i> number of the proof's bits can check.</b> Three bits "
    "suffice, in the sharpest versions.",
    "<b>A true statement's correctly written proof always passes; a "
    "false statement's purported proof fails with constant "
    "probability</b> — <b>from reading three bits of a proof that "
    "may be gigabytes long.</b>",
    "<b>The mechanism is that the proof is written in a highly "
    "redundant, error-correcting form</b>, so that <b>any error is spread "
    "throughout the whole encoding rather than localised</b> — and a "
    "random spot-check therefore finds it. <b>The proof format, not the "
    "verifier's cleverness, is what makes it possible.</b>",
    "<b>And its most useful consequence is hardness of "
    "approximation</b> (Module 11, and CSCE 669 Module 10 "
    "&sect;4's inapproximability results) — <b>the gap between a "
    "passing and a failing proof becomes a gap in an optimisation "
    "problem's achievable value, and that gap is what makes "
    "inapproximability provable.</b> <b>Before PCP, essentially no "
    "inapproximability results were known.</b>"]),
  ("table", ["Consequence", "Why it follows"],
   [["<b>Hardness of approximation, as a field</b>",
     "<b>The accept/reject gap becomes an approximation gap</b> "
     "(Module 11 &sect;1) — which is the whole technique."],
    ["<b>MAX-3SAT cannot be approximated better than 7/8</b>",
     "<b>Directly from PCP, and 7/8 is achievable by a simple randomised "
     "algorithm — so the bound is tight</b>, which is an unusually "
     "satisfying situation."],
    ["<b>Set cover's logarithmic ratio is optimal</b>",
     "<b>Which CSCE 669 Module 10 &sect;4 asserted, and this is the "
     "result that proves it.</b>"],
    ["<b>Succinct, spot-checkable proofs in practice</b>",
     "<b>SNARKs and verifiable computation systems descend from PCP's "
     "ideas</b>, through a long line of refinements."]],
   [0.40, 0.60]),
  ("p", "<b>The practical descendants are real:</b> <b>succinct proof "
        "systems deployed in cryptographic and blockchain systems are "
        "PCP's engineering grandchildren</b> — the line runs through "
        "interactive oracle proofs and polynomial commitments rather than "
        "directly, <b>but the core idea that a long computation can be "
        "verified by checking a few random positions of an encoded "
        "transcript is PCP's.</b> <b>Which is unusual for a result this "
        "abstract</b>, and is worth knowing when the theorem seems "
        "remote."),

  ("h1", "4 &nbsp; Zero knowledge"),
  ("callout", "Zero-knowledge: the verifier learns the statement is true "
              "and nothing else",
   ["<b>A proof is zero-knowledge if the verifier's entire view of the "
    "conversation could have been <i>simulated</i> by an efficient "
    "algorithm with no access to the prover</b> — so <b>the "
    "transcript demonstrably carries no information beyond the statement's "
    "truth</b>, since it could have been produced without anyone knowing a "
    "proof. <b>The simulation definition is the subtle and correct "
    "one.</b>",
    "<b>The classic example is graph three-colouring:</b> the prover "
    "commits to a randomly permuted valid colouring, the verifier picks "
    "one edge and the prover opens just that edge's two commitments, "
    "revealing two different colours. <b>Repeat many times.</b> <b>Each "
    "round reveals two differing colours — which the verifier could "
    "have generated itself — and nothing about the colouring.</b>",
    "<b>And every NP statement has a zero-knowledge proof</b>, assuming "
    "bit commitments exist — which follows from one-way functions. "
    "<b>A striking general result:</b> anything with a certificate can be "
    "proved without revealing the certificate.",
    "<b>The practical use is authentication and privacy-preserving "
    "verification</b> — <b>proving you hold an authorised credential "
    "without revealing which one, proving a transaction is valid without "
    "revealing its amounts, proving a computation was performed correctly "
    "without re-running it</b> (CSCE 711's subject). <b>This is the "
    "most directly applied result in the course.</b>"]),
  ("ul", ["<b>Interaction plus randomness certifies statements with no "
          "certificate</b> — and graph non-isomorphism is the "
          "demonstration (&sect;1).",
          "<b>And the randomness must be hidden from the prover</b>, "
          "which is precisely where the power comes from and why "
          "interaction alone is worthless.",
          "<b>IP = PSPACE, by arithmetisation</b> — <b>and that is "
          "the technique that evaded the relativisation barrier</b> "
          "(Module 07 &sect;3), which is its larger significance.",
          "<b>PCP rewrites NP proofs so that three bits suffice</b>, "
          "which gives hardness of approximation (Module 11) and, "
          "eventually, deployed succinct proof systems.",
          "<b>And every NP statement has a zero-knowledge proof</b>, "
          "which is the most directly applied result in the course. "
          "<b>This is the module where complexity theory produced deployed "
          "technology</b>, which is worth noting in a course otherwise "
          "about what cannot be done."]),
 ],
 "resources": [
   ("Arora & Barak &mdash; chapters 8 and 11 (free draft)",
    "https://theory.cs.princeton.edu/complexity/",
    "<b>Interactive proofs, IP = PSPACE, and the PCP theorem</b> — "
    "the reference for this module."),
   ("Shamir &mdash; IP = PSPACE (free)",
    "https://dl.acm.org/doi/10.1145/146585.146609",
    "<b>&sect;2's theorem</b>, with the arithmetisation worked "
    "through."),
   ("Arora, Lund, Motwani, Sudan & Szegedy &mdash; Proof Verification "
    "and the Hardness of Approximation Problems (free)",
    "https://dl.acm.org/doi/10.1145/278298.278306",
    "<b>&sect;3's theorem</b>, and the paper that created the hardness-of"
    "-approximation field."),
   ("Goldwasser, Micali & Rackoff &mdash; The Knowledge Complexity of "
    "Interactive Proof Systems (free)",
    "https://dl.acm.org/doi/10.1137/0218012",
    "<b>&sect;1 and &sect;4's originating paper</b> — the model and "
    "zero knowledge, in one place."),
 ],
 "exercises": [
   "<b>Implement the graph non-isomorphism protocol</b> and run it on "
   "isomorphic and non-isomorphic pairs.",
   "<b>Measure the acceptance rate</b> and confirm the "
   "2⁻ᵏ bound.",
   "<b>Make the verifier deterministic</b> and show the protocol proves "
   "nothing.",
   "<b>Arithmetise a small Boolean formula</b> into a polynomial and "
   "verify the correspondence.",
   "<b>Demonstrate polynomial rigidity</b> by comparing two low-degree "
   "polynomials at random points.",
   "<b>Explain the PCP theorem's statement precisely</b>, including what "
   "the two parameters mean.",
   "<b>Explain why an error-correcting proof format makes spot-checking "
   "work.</b>",
   "<b>Implement the three-colouring zero-knowledge protocol</b> with a "
   "hash-based commitment.",
   "<b>Write the simulator</b> and confirm it produces "
   "indistinguishable transcripts.",
   "<b>Find a deployed system using zero-knowledge proofs</b> and "
   "describe what it proves and hides.",
 ],
 "selfcheck": [
   "Define an interactive proof and state completeness and soundness.",
   "Why does interaction alone add nothing?",
   "Give the graph non-isomorphism protocol and explain both cases.",
   "State IP = PSPACE and describe arithmetisation.",
   "Why does polynomial rigidity make the protocol sound?",
   "Why does this result matter methodologically?",
   "State the PCP theorem and explain the mechanism.",
   "Name four consequences of PCP.",
   "Define zero-knowledge via simulation and give the three-colouring "
   "protocol.",
   "What is the most directly applied result here, and where is it "
   "used?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Hardness of Approximation",
 "subtitle": "Exactly how well you can do, proved.",
 "question": "If you cannot solve it exactly, how close can you "
             "guarantee?",
 "outcomes": [
     "Explain the gap technique and its connection to PCP.",
     "State the main inapproximability results.",
     "Explain the Unique Games Conjecture and its role.",
     "Explain why some problems have tight bounds and others do not.",
     "Use the approximability picture to choose an approach.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The gap technique",
   "blurb": "How PCP becomes an inapproximability result."},

  {"t": "callout", "title": "A gap in the proof system becomes a gap in the optimisation problem",
   "kind": "The mechanism, in one callout",
   "body": ["<b>PCP says: a false statement's proof fails a random "
            "check with constant probability</b> "
            "(Module 10 §3).",
            "<b>So encode an NP problem as 'satisfy as many checks as "
            "possible'.</b> <b>A true instance satisfies all of them; a "
            "false one satisfies at most a constant fraction.</b>",
            "<b>And an approximation algorithm better than that "
            "constant could distinguish the two cases</b> — which "
            "would decide the NP problem.",
            "<b>So no such approximation exists unless P = NP.</b> "
            "<b>The entire field of inapproximability is that one "
            "argument, applied through reductions that preserve the "
            "gap</b> — which is why PCP created the field rather than "
            "contributing to it."]},

  {"t": "table", "kicker": "Results", "title": "The approximability landscape",
   "header": ["Problem", "Best achievable", "Hardness"],
   "widths": [3.2, 3.5, 4.8],
   "rows": [
     ["<b>Knapsack</b>", "<b>(1+ε), FPTAS</b>", "<b>None — as good as it gets</b>"],
     ["<b>Euclidean TSP</b>", "<b>(1+ε), PTAS</b>", "<b>None</b>"],
     ["<b>Metric TSP</b>", "<b>About 1.5</b>", "<b>No better than 123/122</b>"],
     ["<b>MAX-3SAT</b>", "<b>7/8</b>", "<b>7/8 is optimal. TIGHT</b>"],
     ["<b>MAX-CUT</b>", "<b>0.878 (SDP)</b>", "<b>0.878 optimal under UGC</b>"],
     ["<b>Vertex cover</b>", "<b>2</b>", "<b>No better than 2 under UGC; 1.36 unconditionally</b>"],
     ["<b>Set cover</b>", "<b>ln n (greedy)</b>", "<b>ln n is optimal. TIGHT</b>"],
     ["<b>Max clique</b>", "<b>Essentially nothing</b>", "<b>No n^(1−ε). Inapproximable</b>"],
   ],
   "footnote": "<b>MAX-3SAT and set cover are the satisfying cases:</b> "
               "<b>the achievable ratio and the hardness bound "
               "coincide</b>, so the question is closed and the trivial "
               "algorithm is optimal.",
   "note": "This table is the practically useful artefact of the module."},

  {"t": "section", "label": "Part 2", "title": "Unique games",
   "blurb": "The conjecture a great deal depends on."},

  {"t": "callout", "title": "The Unique Games Conjecture, and why so much rests on it",
   "kind": "The conditionality to state",
   "body": ["<b>UGC asserts that a particular constraint-satisfaction "
            "problem is hard to approximate</b> — and from it follow "
            "optimal inapproximability results for many problems.",
            "<b>Under UGC, the Goemans–Williamson 0.878 for "
            "MAX-CUT is optimal</b> (CSCE 669 §10 §3) "
            "<b>and vertex cover's factor 2 is optimal</b> — both of "
            "which look like analysis artifacts and turn out to be "
            "boundaries.",
            "<b>And more strikingly:</b> <b>under UGC, a generic "
            "semidefinite-programming relaxation gives the optimal ratio "
            "for every constraint satisfaction problem</b> — so the "
            "algorithm is known and only the analysis is missing.",
            "<b>UGC is unproved and the evidence is mixed</b> — "
            "<b>subexponential algorithms for it exist, which is unusual "
            "for a hardness assumption</b>. <b>So state the "
            "conditionality when citing any of it.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Why some are tight",
   "blurb": "And others are not."},

  {"t": "bullets", "kicker": "Patterns", "title": "What determines approximability",
   "items": [
     "<b>Numeric problems with scalable precision get "
     "schemes.</b> <b>Knapsack's FPTAS works by rounding the "
     "profits</b> — the structure permits trading precision for "
     "time.",
     "",
     "<b>Geometric problems get schemes</b>, because space can be "
     "partitioned and the error bounded — Euclidean TSP.",
     "",
     "<b>Constraint satisfaction gets constant factors</b>, and the "
     "constant is set by how much a random assignment achieves "
     "(7/8 for MAX-3SAT is the random baseline).",
     "",
     "<b>Covering problems get logarithms</b>, because greedy's "
     "harmonic-sum analysis is tight.",
     "",
     "<b>And problems where the optimum is a tiny structure resist "
     "entirely</b> — clique, because missing it slightly gives "
     "nothing.",
   ],
   "footnote": "<b>The pattern is about what an approximate answer "
               "<i>is</i></b> — a 90%-good knapsack is nearly a "
               "knapsack and a 90%-good clique is not nearly a clique."},

  {"t": "section", "label": "Part 4", "title": "Using the picture",
   "blurb": "The practical procedure."},

  {"t": "callout", "title": "Look up both sides before writing an algorithm",
   "kind": "The practical advice",
   "body": ["<b>Find the best known approximation ratio and the best "
            "known hardness bound.</b> <b>If they coincide, the question "
            "is closed and you should implement the known "
            "algorithm.</b>",
            "<b>If there is a gap, the gap tells you how much "
            "improvement is possible</b> — metric TSP's gap between "
            "1.5 and 123/122 is where the research is.",
            "<b>And if the hardness is 'no constant factor', stop "
            "looking for one</b> and move to Module 12's parameters or a "
            "restricted case.",
            "<b>Which takes twenty minutes against a reference</b> "
            "— <b>and it is the same discipline as CSCE 627 "
            "§06 §4's prove-impossibility-first, with a "
            "quantitative answer instead of a binary one.</b>"]},

  {"t": "bullets", "kicker": "And", "title": "Two things the picture does not tell you",
   "items": [
     "<b>What your instances do.</b> <b>A 2-approximation may "
     "routinely achieve 1.01 on real data</b>, and the guarantee is a "
     "worst case (Module 01 §3).",
     "",
     "<b>So measure the achieved ratio</b> against a bound, rather "
     "than reporting the guarantee.",
     "",
     "<b>And whether exact is affordable.</b> <b>A solver may simply "
     "solve your instances exactly</b> (Module 04 §4), making "
     "the approximation question moot.",
     "",
     "<b>Which is the recurring correction:</b> <b>worst-case theory "
     "bounds what can be promised and not what will happen.</b>",
     "",
     "<b>So: look up the theory, then measure.</b> <b>Both, in that "
     "order.</b>",
   ],
   "footnote": "<b>'Look up the theory, then measure' is the whole "
               "practical content of this module</b>, and skipping either "
               "step is the common error."},
 ],
 "takeaways": [
   "A gap in the proof system becomes a gap in the optimisation problem, "
   "and the whole field of inapproximability is that one argument applied "
   "through gap-preserving reductions.",
   "MAX-3SAT at 7/8 and set cover at ln n are tight — the achievable "
   "ratio and the hardness bound coincide, so the trivial algorithm is "
   "optimal.",
   "A great deal of optimal inapproximability is conditional on the Unique "
   "Games Conjecture, which is unproved and whose evidence is mixed.",
   "Under UGC a generic semidefinite relaxation is optimal for every "
   "constraint satisfaction problem, so the algorithm is known and the "
   "analysis is missing.",
   "Approximability depends on what an approximate answer is — a "
   "90%-good knapsack is nearly a knapsack and a 90%-good clique is not.",
   "Look up both the achievable ratio and the hardness bound before "
   "writing anything, and then measure your instances.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The gap technique"),
  ("callout", "A gap in the proof system becomes a gap in the optimisation "
              "problem",
   ["<b>PCP says that a false statement's purported proof fails a random "
    "constant-size check with constant probability</b> (Module 10 "
    "&sect;3).",
    "<b>So encode an NP problem as an optimisation problem: 'satisfy as "
    "many of these checks as possible'.</b> <b>A true instance yields an "
    "assignment satisfying all of them; a false instance yields one "
    "satisfying at most a constant fraction.</b> <b>There are no "
    "instances in between.</b>",
    "<b>And an approximation algorithm with a ratio better than that "
    "constant could distinguish the two cases</b> — it would return "
    "a value above the false-instance ceiling exactly when the instance "
    "was true — <b>which would decide the NP problem in polynomial "
    "time.</b>",
    "<b>So no such approximation algorithm exists unless P = NP.</b> "
    "<b>The entire field of inapproximability is that one argument, "
    "applied through reductions that preserve the gap</b> — <b>which "
    "is why PCP created the field rather than merely contributing to "
    "it</b>, and why almost no inapproximability results predate 1992."]),
  ("table", ["Problem", "Best achievable ratio", "Hardness bound"],
   [["<b>Knapsack</b>", "<b>(1+&epsilon;) for any &epsilon;, in time "
     "polynomial in 1/&epsilon; — an FPTAS.</b>",
     "<b>None. This is as good as approximation gets</b> "
     "(CSCE 669 Module 10 &sect;1's classes)."],
    ["<b>Euclidean TSP</b>", "<b>(1+&epsilon;), a PTAS</b> (Arora, "
     "Mitchell).", "<b>None.</b>"],
    ["<b>Metric TSP</b>",
     "<b>About 1.5</b> (Christofides, improved slightly in 2021).",
     "<b>No better than 123/122</b> — <b>a large gap, and that is "
     "where the research is</b> (&sect;4)."],
    ["<b>MAX-3SAT</b>", "<b>7/8</b>, by a simple randomised assignment.",
     "<b>7/8 is optimal. TIGHT.</b> So the trivial algorithm cannot be "
     "beaten."],
    ["<b>MAX-CUT</b>",
     "<b>0.878, by semidefinite programming</b> (CSCE 669 "
     "Module 10 &sect;3).",
     "<b>0.878 is optimal under the Unique Games Conjecture</b> "
     "(&sect;2)."],
    ["<b>Vertex cover</b>", "<b>2</b>, by the ten-line LP rounding.",
     "<b>No better than 2 under UGC; no better than about 1.36 "
     "unconditionally.</b>"],
    ["<b>Set cover</b>", "<b>ln n, by the greedy algorithm.</b>",
     "<b>ln n is optimal. TIGHT</b> — the greedy algorithm cannot be "
     "improved."],
    ["<b>Maximum clique</b>",
     "<b>Essentially nothing useful.</b>",
     "<b>No n<super>1&minus;&epsilon;</super> approximation unless "
     "P = NP. Inapproximable.</b>"]],
   [0.24, 0.33, 0.43]),
  ("p", "<b>MAX-3SAT and set cover are the satisfying cases:</b> <b>the "
        "achievable ratio and the hardness bound coincide exactly</b>, so "
        "<b>the question is closed and the trivial algorithm is "
        "provably optimal</b> — which is a rare and useful thing to "
        "be able to say, and it means any time spent looking for something "
        "better is provably wasted."),

  ("h1", "2 &nbsp; The Unique Games Conjecture"),
  ("callout", "The Unique Games Conjecture, and why so much rests on it",
   ["<b>UGC asserts that a particular constraint-satisfaction problem "
    "— label assignment with permutation constraints — is hard "
    "to approximate</b>, and <b>from it follow optimal "
    "inapproximability results for a remarkable range of problems.</b>",
    "<b>Under UGC, the Goemans–Williamson 0.878 ratio for MAX-CUT "
    "is optimal</b> (CSCE 669 Module 10 &sect;3) <b>and vertex "
    "cover's factor of 2 is optimal</b> — <b>both of which look "
    "like artifacts of their particular analyses and turn out to be the "
    "true boundaries</b>, which is strong circumstantial support for the "
    "conjecture.",
    "<b>And more strikingly:</b> <b>under UGC, a generic semidefinite "
    "programming relaxation achieves the optimal approximation ratio for "
    "<i>every</i> constraint satisfaction problem</b> (Raghavendra) "
    "— <b>so for that whole class the best algorithm is known and "
    "only the analysis of its ratio is missing.</b> An unusual situation.",
    "<b>UGC is unproved and the evidence is mixed</b> — "
    "<b>subexponential-time algorithms for unique games exist, which is "
    "unusual for a problem conjectured hard</b> and is the main reason for "
    "doubt. <b>So state the conditionality when citing any of these "
    "results:</b> 'optimal under UGC' is a weaker claim than 'optimal "
    "unless P = NP', and the difference matters."]),

  ("break",),
  ("h1", "3 &nbsp; Why some bounds are tight and others are not"),
  ("ul", ["<b>Numeric problems with scalable precision get "
          "schemes.</b> <b>Knapsack's FPTAS works by rounding the "
          "profit values to fewer significant digits and then solving "
          "exactly by dynamic programming</b> — the structure permits "
          "trading precision for time continuously, which is exactly what "
          "a scheme requires.",
          "<b>Geometric problems get schemes</b>, because <b>space can "
          "be partitioned into cells and the error from treating each cell "
          "independently can be bounded</b> — which is how Euclidean "
          "TSP's PTAS works, and why the metric version (with no geometry) "
          "does not have one.",
          "<b>Constraint satisfaction gets constant factors</b>, and "
          "<b>the constant is usually set by how well a random assignment "
          "does</b> — a random assignment satisfies 7/8 of the "
          "clauses of a MAX-3SAT instance in expectation, <b>and that "
          "random baseline turns out to be optimal</b>, which is both "
          "satisfying and slightly deflating.",
          "<b>Covering problems get logarithms</b>, because <b>the "
          "greedy algorithm's harmonic-sum analysis is tight</b> — "
          "and the matching hardness result says the analysis was not "
          "merely the best available but the truth.",
          "<b>And problems where the optimum is a tiny structure resist "
          "approximation entirely</b> — <b>clique, because a clique "
          "that misses one vertex of a large clique may be tiny</b>: "
          "there is no partial credit. <b>The pattern across the list is "
          "about what an approximate answer <i>is</i></b>: <b>a 90%-good "
          "knapsack solution is nearly a knapsack solution, and a 90%-good "
          "clique is not nearly a clique.</b>"]),

  ("h1", "4 &nbsp; Using the picture"),
  ("callout", "Look up both sides before writing an algorithm",
   ["<b>Find the best known approximation ratio and the best known "
    "hardness bound for your problem.</b> <b>If they coincide, the "
    "question is closed and you should implement the known algorithm</b> "
    "rather than looking for a better one.",
    "<b>If there is a gap, the gap tells you how much improvement is "
    "possible</b> — <b>metric TSP's gap between 1.5 achievable and "
    "123/122 hard is where decades of research sits</b>, and knowing the "
    "gap tells you whether an improvement is worth attempting.",
    "<b>And if the hardness result says 'no constant factor', stop "
    "looking for one</b> and move to Module 12's parameters, a "
    "restricted case, or a heuristic with a measured bound "
    "(CSCE 669 Module 13 &sect;3).",
    "<b>Which takes twenty minutes against a reference</b> — "
    "<b>and it is the same discipline as CSCE 627 Module 06 "
    "&sect;4's prove-impossibility-first, with a quantitative answer "
    "instead of a binary one.</b> <b>The quantitative version is more "
    "useful</b>, because it tells you not only to stop but how much is "
    "available."]),
  ("ul", ["<b>What your instances actually do.</b> <b>A "
          "2-approximation may routinely achieve 1.01 on real data</b>, "
          "because <b>the guarantee is a worst case</b> (Module 01 "
          "&sect;3) and the worst case may be nowhere near your inputs.",
          "<b>So measure the achieved ratio against a computed bound</b> "
          "rather than reporting the theoretical guarantee — which "
          "is CSCE 669 Module 13 &sect;3's advice, and it turns a "
          "pessimistic claim into an accurate one.",
          "<b>And whether exact is affordable anyway.</b> <b>A solver "
          "may simply solve your instances exactly</b> (Module 04 "
          "&sect;4), <b>making the whole approximation question "
          "moot</b> — which happens more often than the theory would "
          "lead you to expect.",
          "<b>Which is the recurring correction of this course:</b> "
          "<b>worst-case theory bounds what can be promised and not what "
          "will happen.</b>",
          "<b>So: look up the theory, then measure.</b> <b>Both, in "
          "that order</b> — the theory first because it may stop you "
          "wasting effort, and the measurement second because the theory "
          "does not describe your inputs. <b>Skipping either step is the "
          "common error</b>, and the two errors are made by different "
          "kinds of person."]),
 ],
 "resources": [
   ("Williamson & Shmoys &mdash; The Design of Approximation Algorithms "
    "(free PDF)",
    "https://www.designofapproxalgs.com/",
    "<b>&sect;1's table from the algorithm side</b>, free in full, and "
    "the same book as CSCE 669 Module 10."),
   ("Arora & Barak &mdash; chapters 11 and 22 (free draft)",
    "https://theory.cs.princeton.edu/complexity/",
    "<b>PCP's consequences and the gap technique of &sect;1</b>, with "
    "the reductions."),
   ("Khot &mdash; On the Unique Games Conjecture (free survey)",
    "https://www.cs.nyu.edu/~khot/papers/UGCSurvey.pdf",
    "<b>&sect;2, by the person who proposed it</b> — including an "
    "honest account of the evidence against."),
   ("Raghavendra &mdash; Optimal Algorithms and Inapproximability "
    "Results for Every CSP? (free)",
    "https://dl.acm.org/doi/10.1145/1374376.1374414",
    "<b>&sect;2's striking consequence</b> — the generic SDP being "
    "optimal under UGC."),
 ],
 "exercises": [
   "<b>Work through the gap argument</b> for one problem, from PCP to "
   "inapproximability.",
   "<b>Implement the random-assignment 7/8 algorithm for MAX-3SAT</b> and "
   "measure its achieved ratio.",
   "<b>Confirm that 7/8 is the expected value</b> by direct "
   "calculation.",
   "<b>Implement greedy set cover</b> and measure its ratio against the "
   "LP bound on random instances.",
   "<b>Try to beat it</b> and relate your failure to the tightness "
   "result.",
   "<b>Look up both sides for three problems from your own work</b> and "
   "record the gap in each.",
   "<b>Identify which of your problems has a closed question</b> and "
   "implement the optimal algorithm.",
   "<b>Measure a 2-approximation's achieved ratio on real data</b> and "
   "compare against the guarantee.",
   "<b>Classify five problems by §3's patterns</b> and check the "
   "classification against the known results.",
   "<b>Find a result cited as 'optimal' that is conditional on UGC</b> "
   "and note whether the citation says so.",
 ],
 "selfcheck": [
   "Explain how a PCP gap becomes an inapproximability result.",
   "Why did PCP create the field rather than contribute to it?",
   "Give the approximability picture for eight problems.",
   "Which two are tight, and what does that mean practically?",
   "State UGC and three results that depend on it.",
   "Why is the evidence for UGC mixed?",
   "Give five patterns determining approximability.",
   "What is the underlying principle behind all five?",
   "Give the four-step procedure for using the picture.",
   "Name two things the picture does not tell you.",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Fine-Grained and Parameterised",
 "subtitle": "The complexity theory that answers your actual question.",
 "question": "Not 'is it polynomial' but 'what exactly is the exponent, "
             "and in what'?",
 "outcomes": [
     "Explain fixed-parameter tractability and give examples.",
     "Choose a parameter for a real problem.",
     "Explain kernelisation and its practical value.",
     "Explain fine-grained complexity and the standard hypotheses.",
     "Explain why this is the practically useful part of the field.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Parameterised complexity",
   "blurb": "Exponential in the right thing."},

  {"t": "callout", "title": "Fixed-parameter tractable: exponential in a parameter, polynomial in the size",
   "kind": "The reframing",
   "body": ["<b>A problem is FPT with respect to parameter k if it is "
            "solvable in time f(k)·nᶜ</b> — any function of k, "
            "times a polynomial in n with the exponent independent of "
            "k.",
            "<b>So vertex cover is NP-complete and FPT:</b> "
            "<b>O(2ᵏ·n) finds a cover of size k</b>, which is "
            "entirely practical for k up to 40 on a graph of any "
            "size.",
            "<b>And that is the right question for most real "
            "problems</b>, where <b>the thing that is large and the thing "
            "that is hard are different</b> — a huge graph with a small "
            "solution, or a long formula with few variables that "
            "matter.",
            "<b>Which makes parameterised complexity the practically "
            "useful branch of the field</b>, and <b>it is the one most "
            "often omitted from a complexity course.</b>"]},

  {"t": "table", "kicker": "Parameters", "title": "Parameters that work, and what they unlock",
   "header": ["Parameter", "Problems it makes tractable", "Note"],
   "widths": [2.7, 4.3, 5.2],
   "rows": [
     ["<b>Solution size k</b>", "<b>Vertex cover, feedback vertex set</b>", "<b>O(2ᵏ n) and better. The classic</b>"],
     ["<b>Treewidth</b>", "<b>Almost everything on graphs</b>", "<b>Courcelle: any MSO property, in linear time</b>"],
     ["<b>Number of variables</b>", "<b>Integer programming</b>", "<b>Lenstra: FPT in the dimension</b>"],
     ["<b>Clause–variable ratio</b>", "<b>SAT, empirically</b>", "<b>Not a theorem; a real phase transition</b>"],
     ["<b>Vertex cover number</b>", "<b>Even more than treewidth</b>", "<b>Stronger parameter, rarer small</b>"],
     ["<b>Distance from triviality</b>", "<b>The general design pattern</b>", "<b>How far from an easy case is your instance?</b>"],
   ],
   "footnote": "<b>Treewidth and Courcelle's theorem are the most "
               "powerful combination</b> — <b>any property "
               "expressible in monadic second-order logic is linear-time "
               "on bounded-treewidth graphs</b>, which covers an enormous "
               "range at once.",
   "note": "Courcelle is the single most leveraged result here."},

  {"t": "section", "label": "Part 2", "title": "Kernelisation",
   "blurb": "Shrink the instance, then solve it."},

  {"t": "code", "kicker": "Kernelisation", "title": "Preprocessing with a guarantee",
   "lang": "text", "code": """
  A KERNEL is a polynomial-time preprocessing that reduces
  any instance to an EQUIVALENT one whose size is bounded
  by a function of k alone -- independent of n.

  VERTEX COVER, size-k kernel:
      any vertex of degree > k MUST be in the cover
          (else all its neighbours are, exceeding k)
          -> take it, decrement k
      any isolated vertex is irrelevant -> delete it
      after these, if more than k^2 edges remain, there is
          no cover of size k -- each of k vertices covers
          at most k edges
      -> so the kernel has at most k^2 edges

  THEN SOLVE THE KERNEL by brute force. Total time is
  polynomial plus f(k).

  WHY THIS MATTERS PRACTICALLY: kernelisation is
  PREPROCESSING WITH A PROOF. Every solver does
  preprocessing; a kernel is preprocessing with a stated
  guarantee about how much it reduces.

  AND A PROBLEM IS FPT IF AND ONLY IF IT HAS A KERNEL,
  which is a clean characterisation and means looking for
  one is never wasted.
""",
   "caption": "<b>Kernelisation is the most directly applicable idea in "
              "this module</b> — it is presolve with a theorem "
              "attached (CSCE 669 §09).",
   "note": "The equivalence with FPT is the result that makes kernels "
           "worth seeking."},

  {"t": "section", "label": "Part 3", "title": "Fine-grained complexity",
   "blurb": "The exact exponent, and lower bounds for it."},

  {"t": "callout", "title": "Fine-grained complexity asks for the exponent, and proves lower bounds conditionally",
   "kind": "The newer branch",
   "body": ["<b>'Polynomial' is not the question when n is a "
            "billion.</b> <b>n² and n³ are both "
            "polynomial and only one is feasible.</b>",
            "<b>So the field assumes a specific hardness hypothesis and "
            "derives exact exponents.</b> <b>SETH: SAT needs essentially "
            "2ⁿ time.</b> <b>3SUM: needs n² "
            "time.</b> <b>APSP: needs n³.</b>",
            "<b>And from those follow tight lower bounds for polynomial "
            "problems:</b> <b>under SETH, edit distance needs "
            "n^(2−o(1))</b> — so the textbook dynamic program "
            "is optimal.",
            "<b>Which is exactly the practically useful kind of "
            "result:</b> <b>it tells you whether your quadratic algorithm "
            "can be improved</b>, which 'it is in P' does not."]},

  {"t": "table", "kicker": "Hypotheses", "title": "The standard assumptions and what they give",
   "header": ["Hypothesis", "Says", "Implies"],
   "widths": [2.3, 3.8, 5.9],
   "rows": [
     ["<b>SETH</b>", "<b>k-SAT needs 2ⁿ as k grows</b>", "<b>Edit distance, LCS need n². Orthogonal vectors hard</b>"],
     ["<b>3SUM</b>", "<b>3SUM needs n²</b>", "<b>Many computational geometry lower bounds</b>"],
     ["<b>APSP</b>", "<b>All-pairs shortest paths needs n³</b>", "<b>Negative triangle, graph radius, replacement paths</b>"],
     ["<b>ETH</b>", "<b>3-SAT needs 2^Ω(n)</b>", "<b>No subexponential algorithms for many problems</b>"],
   ],
   "footnote": "<b>These are conjectures and the results are "
               "conditional</b> — but <b>they are the only route to "
               "'your quadratic algorithm is optimal'</b>, which is a "
               "question unconditional theory cannot touch.",
   "note": "The conditionality is real and the alternative is no answer "
           "at all."},

  {"t": "section", "label": "Part 4", "title": "Why this matters most",
   "blurb": "The honest assessment of the field's usefulness."},

  {"t": "bullets", "kicker": "Practical", "title": "What to do with a hard problem, in order of value",
   "items": [
     "<b>1 · Find the parameter.</b> <b>Solution size, "
     "treewidth, dimension, distance from an easy case</b> — and "
     "check whether it is small in your instances.",
     "",
     "<b>2 · Look for a kernel</b>, or use a solver's presolve "
     "and measure the reduction.",
     "",
     "<b>3 · Check the approximation picture</b> "
     "(Module 11 §4).",
     "",
     "<b>4 · Check the fine-grained lower bound</b> if your "
     "problem is polynomial and too slow.",
     "",
     "<b>5 · And only then consider the worst-case "
     "classification</b>, which is where most courses start.",
   ],
   "footnote": "<b>The ordering is deliberate and is the opposite of the "
               "usual one</b> — the parameterised question is "
               "answerable and actionable, and the worst-case one "
               "frequently is neither."},

  {"t": "callout", "title": "Why this is the part of complexity theory that pays",
   "kind": "The assessment",
   "body": ["<b>Worst-case classification answers 'is there a "
            "polynomial algorithm for all inputs'</b> — which is "
            "rarely the question you have.",
            "<b>Parameterised complexity answers 'is there an algorithm "
            "fast on instances like mine'</b>, which usually is.",
            "<b>And fine-grained complexity answers 'can my quadratic "
            "algorithm be improved'</b>, which is the question an "
            "engineer with a slow program actually asks.",
            "<b>So the two newest branches are the two most "
            "useful</b> — <b>and they are the two most often omitted, "
            "which is a reasonable complaint about how the subject is "
            "taught.</b>"]},
 ],
 "takeaways": [
   "Fixed-parameter tractable means f(k) times a polynomial in n, so "
   "vertex cover is NP-complete and solvable in O(2ᵏ n) — "
   "practical for k up to 40 on any graph.",
   "The right question for most real problems is parameterised, because "
   "the thing that is large and the thing that is hard are usually "
   "different.",
   "Courcelle's theorem makes any monadic second-order property "
   "linear-time on bounded-treewidth graphs, which is the most leveraged "
   "result here.",
   "A kernel is preprocessing with a proof, and a problem is FPT exactly "
   "when it has a kernel — so looking for one is never wasted.",
   "Fine-grained complexity derives exact exponents from hypotheses like "
   "SETH, which is the only route to 'your quadratic algorithm is "
   "optimal'.",
   "The two newest branches are the two most useful and the two most often "
   "omitted, which is a reasonable complaint about how the subject is "
   "taught.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Parameterised complexity"),
  ("callout", "Fixed-parameter tractable: exponential in a parameter, "
              "polynomial in the size",
   ["<b>A problem is fixed-parameter tractable with respect to a "
    "parameter k if it is solvable in time f(k)&middot;n<super>c</super> "
    "— any function of k, however horrible, times a polynomial in n "
    "whose exponent does not depend on k.</b> <b>The exponent being "
    "independent of k is the essential part</b>; n<super>k</super> is not "
    "FPT.",
    "<b>So vertex cover is NP-complete and fixed-parameter "
    "tractable:</b> <b>O(2<super>k</super>&middot;n) finds a cover of "
    "size k, or reports that none exists</b> — branch on each edge, "
    "taking one endpoint or the other. <b>Which is entirely practical for "
    "k up to about 40 on a graph of any size whatsoever.</b>",
    "<b>And that is the right question for most real problems</b>, "
    "because <b>the thing that is large and the thing that is hard are "
    "usually different</b> — a huge graph with a small solution, a "
    "long formula with few genuinely interacting variables, a big "
    "instance with low treewidth. <b>Worst-case complexity conflates "
    "them by measuring only n.</b>",
    "<b>Which makes parameterised complexity the practically useful "
    "branch of the field</b>, and <b>it is the one most often omitted "
    "from a complexity course</b> — a situation this module exists to "
    "correct."]),
  ("table", ["Parameter", "What it makes tractable", "Note"],
   [["<b>Solution size k</b>",
     "<b>Vertex cover, feedback vertex set, k-path, hitting set.</b>",
     "<b>O(2<super>k</super>n), and better for several</b> — vertex "
     "cover is down to about 1.27<super>k</super>. The classic "
     "parameter."],
    ["<b>Treewidth</b>",
     "<b>Almost every graph problem.</b>",
     "<b>Courcelle's theorem: any property expressible in monadic "
     "second-order logic is decidable in linear time on graphs of bounded "
     "treewidth.</b> See the note."],
    ["<b>Number of variables</b>", "<b>Integer programming.</b>",
     "<b>Lenstra: integer programming is FPT in the dimension</b> "
     "— which is why small-dimension integer programs are easy "
     "regardless of the coefficients."],
    ["<b>Clause-to-variable ratio</b>", "<b>SAT, empirically.</b>",
     "<b>Not a theorem — but a real and sharp phase transition</b> "
     "around 4.27 for 3-SAT, with instances far from it being easy in "
     "practice."],
    ["<b>Vertex cover number</b>",
     "<b>More than treewidth does.</b>",
     "<b>A stronger parameter — bounded vertex cover number implies "
     "bounded treewidth — and correspondingly rarer to find "
     "small.</b>"],
    ["<b>Distance from triviality</b>",
     "<b>The general design pattern rather than a specific "
     "parameter.</b>",
     "<b>How many edges from being planar, how many vertices from being "
     "bipartite, how many clauses from being 2-SAT.</b> <b>The most "
     "transferable idea in the table.</b>"]],
   [0.22, 0.34, 0.44]),
  ("p", "<b>Treewidth and Courcelle's theorem are the most powerful "
        "combination here</b> — <b>any property expressible in "
        "monadic second-order logic is linear-time decidable on graphs of "
        "bounded treewidth</b>, which covers an enormous range of problems "
        "in one result and requires no per-problem algorithm design. "
        "<b>The constants are terrible and the existence result is "
        "frequently enough to justify building the dynamic program by "
        "hand</b>, which is how it is used in practice."),

  ("h1", "2 &nbsp; Kernelisation"),
  ("code", """A KERNEL is a polynomial-time preprocessing that reduces
any instance to an EQUIVALENT instance whose size is
bounded by a function of k alone -- independent of n.

VERTEX COVER, a size-k^2 kernel:
    any vertex of degree > k MUST be in the cover
        (otherwise all its neighbours must be, which
         exceeds k)
        -> take it, decrement k, remove it
    any isolated vertex is irrelevant -> delete it
    after these rules, if more than k^2 edges remain there
        is no cover of size k -- each of k vertices now
        covers at most k edges
    -> so the surviving kernel has at most k^2 edges

THEN SOLVE THE KERNEL by brute force. Total time is
polynomial in n, plus f(k) on a tiny instance.

WHY THIS MATTERS PRACTICALLY: kernelisation is
PREPROCESSING WITH A PROOF. Every real solver does
preprocessing (CSCE 669 Module 09 section 4); a kernel is
preprocessing with a stated guarantee about how much it
reduces and why the answer is preserved.

AND A PROBLEM IS FPT IF AND ONLY IF IT HAS A KERNEL, which
is a clean characterisation and means that looking for one
is never wasted effort."""),

  ("break",),
  ("h1", "3 &nbsp; Fine-grained complexity"),
  ("callout", "Fine-grained complexity asks for the exponent, and proves "
              "lower bounds conditionally",
   ["<b>'Polynomial' is not the question when n is a billion.</b> "
    "<b>n&#178; and n&#179; are both polynomial and only one of them is "
    "feasible</b> — and a great deal of real engineering lives in "
    "exactly that gap (Module 01 &sect;4).",
    "<b>So the field assumes a specific hardness hypothesis and derives "
    "exact exponents from it.</b> <b>SETH: satisfiability of k-SAT "
    "requires essentially 2<super>n</super> time as k grows. 3SUM "
    "requires n&#178;. All-pairs shortest paths requires n&#179;.</b>",
    "<b>And from those follow tight lower bounds for problems that are "
    "firmly in P:</b> <b>under SETH, edit distance requires "
    "n<super>2&minus;o(1)</super> time</b> — <b>so the textbook "
    "dynamic programming algorithm is essentially optimal, and the decades "
    "spent looking for a subquadratic one were spent against a wall.</b>",
    "<b>Which is exactly the practically useful kind of result:</b> "
    "<b>it tells you whether your quadratic algorithm can be "
    "improved</b> — <b>a question that 'it is in P' cannot even "
    "address</b>, and one that an engineer with a slow program actually "
    "has."]),
  ("table", ["Hypothesis", "What it says", "What it implies"],
   [["<b>SETH</b>",
     "<b>k-SAT requires 2<super>n</super> time as k grows.</b>",
     "<b>Edit distance and longest common subsequence require n&#178;; "
     "orthogonal vectors is hard</b>, and orthogonal vectors is the usual "
     "intermediate problem."],
    ["<b>3SUM</b>",
     "<b>Finding three numbers summing to zero requires n&#178;.</b>",
     "<b>A large family of computational geometry lower bounds</b> "
     "(CSCE 620) — collinearity, polygon containment, visibility."],
    ["<b>APSP</b>",
     "<b>All-pairs shortest paths requires n&#179;.</b>",
     "<b>Negative triangle detection, graph radius, replacement paths, "
     "and second shortest path</b> — all equivalent to APSP under "
     "subcubic reductions."],
    ["<b>ETH</b>",
     "<b>3-SAT requires 2<super>&Omega;(n)</super>.</b>",
     "<b>No subexponential algorithms for a wide range of NP-complete "
     "problems</b>, and tight bounds on FPT running times."]],
   [0.16, 0.34, 0.50]),
  ("p", "<b>These are conjectures and the results derived from them are "
        "conditional</b> — but <b>they are the only available route "
        "to statements like 'your quadratic algorithm is optimal'</b>, "
        "which unconditional theory cannot touch at all (Module 09 "
        "&sect;2's 5n bound is the measure of how little is "
        "unconditional). <b>So the conditionality is real and the "
        "alternative is no answer whatsoever</b>, which makes the trade "
        "worth taking."),

  ("h1", "4 &nbsp; Why this is the part that pays"),
  ("ul", ["<b>1 &middot; Find the parameter.</b> <b>Solution size, "
          "treewidth, dimension, distance from an easy case</b> "
          "(&sect;1's table) — <b>and then check whether it is "
          "actually small in your instances</b>, which is a measurement "
          "rather than a theorem.",
          "<b>2 &middot; Look for a kernel</b>, or use a solver's "
          "presolve and measure how much it reduces (&sect;2). <b>The "
          "reduction is frequently dramatic and is almost always worth "
          "measuring.</b>",
          "<b>3 &middot; Check the approximation picture</b> "
          "(Module 11 &sect;4) — both sides, which takes twenty "
          "minutes.",
          "<b>4 &middot; Check the fine-grained lower bound</b> if your "
          "problem is polynomial and your implementation is too slow "
          "(&sect;3) — it may tell you to stop optimising and change "
          "the problem.",
          "<b>5 &middot; And only then consider the worst-case "
          "classification</b>, which is where most courses start. <b>The "
          "ordering is deliberate and is the opposite of the usual "
          "one</b> — <b>the parameterised question is answerable and "
          "actionable, and the worst-case one is frequently neither.</b>"]),
  ("callout", "Why this is the part of complexity theory that pays",
   ["<b>Worst-case classification answers 'is there a polynomial-time "
    "algorithm correct on all inputs'</b> — <b>which is rarely the "
    "question you have</b>, and is the question Modules 02 through 05 "
    "are about.",
    "<b>Parameterised complexity answers 'is there an algorithm fast on "
    "instances like mine'</b>, which usually is the question — and "
    "it answers it with a theorem rather than a benchmark.",
    "<b>And fine-grained complexity answers 'can my quadratic algorithm "
    "be improved'</b>, which is the question an engineer with a slow "
    "program actually asks and which no other branch addresses.",
    "<b>So the two newest branches are the two most useful</b> — "
    "<b>and they are the two most often omitted from a complexity "
    "course</b>, which is a reasonable complaint about how the subject is "
    "taught and the reason this module is placed where it is rather than "
    "as an appendix."]),
 ],
 "resources": [
   ("Cygan et al. &mdash; Parameterized Algorithms (free PDF)",
    "https://www.mimuw.edu.pl/~malcin/book/",
    "<b>Free in full, and the reference for &sect;1 and &sect;2</b> "
    "— the most practically useful book in this course."),
   ("Williams &mdash; On Some Fine-Grained Questions in Algorithms and "
    "Complexity (free survey)",
    "https://people.csail.mit.edu/virgi/eccentri.pdf",
    "<b>&sect;3's hypotheses and their consequences</b>, surveyed by one "
    "of the field's founders."),
   ("Bringmann &mdash; Fine-Grained Complexity Theory (free lecture "
    "notes)",
    "https://people.mpi-inf.mpg.de/~kbringma/",
    "<b>&sect;3 taught</b>, with the edit-distance lower bound worked "
    "through."),
   ("Downey & Fellows &mdash; Fundamentals of Parameterized Complexity",
    "https://link.springer.com/book/10.1007/978-1-4471-5559-1",
    "<b>The founders' treatment</b>, including the W-hierarchy of "
    "parameterised intractability that this module does not cover. "
    "Library copy."),
 ],
 "exercises": [
   "<b>Implement the O(2ᵏ n) vertex cover algorithm</b> and run it "
   "on a large graph with a small cover.",
   "<b>Implement the vertex cover kernel</b> and measure the reduction on "
   "real graphs.",
   "<b>Verify the k² bound</b> empirically.",
   "<b>Compute the treewidth</b> (or an upper bound) of three graphs from "
   "your own work.",
   "<b>Write a dynamic program over a tree decomposition</b> for one "
   "problem.",
   "<b>Identify a parameter for a hard problem you care about</b> and "
   "measure whether it is small in your instances.",
   "<b>Implement edit distance</b> and confirm its quadratic scaling.",
   "<b>Look up the SETH-based lower bound</b> and state what it means for "
   "your implementation.",
   "<b>Find a 3SUM-hard geometry problem</b> and relate it to "
   "CSCE 620.",
   "<b>Apply §4's five steps</b> to one problem and report which "
   "step was most useful.",
 ],
 "selfcheck": [
   "Define fixed-parameter tractability precisely, including why the "
   "exponent must be independent of k.",
   "Why is vertex cover both NP-complete and practical?",
   "Why is the parameterised question the right one for real problems?",
   "Name six parameters and what each unlocks.",
   "State Courcelle's theorem and why it is so leveraged.",
   "Define a kernel and give the vertex cover one.",
   "What is the characterisation of FPT in terms of kernels?",
   "What does fine-grained complexity ask, and name four hypotheses.",
   "What does SETH imply about edit distance?",
   "Give the five-step procedure and say why the ordering is "
   "reversed.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "What Complexity Tells You",
 "subtitle": "The honest summary of a field with an open centre.",
 "question": "After thirteen modules, what has the classification "
             "bought?",
 "outcomes": [
     "State what is proved and what is conjectured.",
     "Avoid the standard overreaches.",
     "Use a hardness result productively.",
     "Place this course relative to CSCE 627 and CSCE 658.",
     "State what a complexity claim can honestly assert.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Proved and conjectured",
   "blurb": "The honest division."},

  {"t": "table", "kicker": "Status", "title": "What is actually proved",
   "header": ["Statement", "Status"],
   "widths": [6.0, 5.0],
   "rows": [
     ["<b>P ≠ EXPTIME; the hierarchy theorems</b>", "<b>PROVED</b> (M07 §1)"],
     ["<b>Cook–Levin; thousands of problems NP-complete</b>", "<b>PROVED</b> (M04)"],
     ["<b>PSPACE = NPSPACE; NL = co-NL</b>", "<b>PROVED</b> (M06)"],
     ["<b>IP = PSPACE; the PCP theorem</b>", "<b>PROVED</b> (M10)"],
     ["<b>Three barrier results</b>", "<b>PROVED</b> (M07, M09)"],
     ["<b>P ≠ NP</b>", "<b>OPEN. Believed</b>"],
     ["<b>NP ≠ co-NP; PH strict; NC ≠ P; BPP = P</b>", "<b>ALL OPEN</b>"],
     ["<b>Any super-linear general circuit lower bound</b>", "<b>OPEN. Best known ≈ 5n</b>"],
   ],
   "footnote": "<b>A great deal is proved and the central question is "
               "not</b> — and the proved results are mostly "
               "<i>equalities and completeness</i>, while almost every "
               "<i>separation</i> is open.",
   "note": "That the proved results are equalities and the open ones are "
           "separations is the structural observation."},

  {"t": "section", "label": "Part 2", "title": "The overreaches",
   "blurb": "What gets claimed, incorrectly."},

  {"t": "table", "kicker": "Overreach", "title": "Common claims, corrected",
   "header": ["Claim", "Correction"],
   "widths": [4.8, 6.2],
   "rows": [
     ["<b>'NP-complete means intractable'</b>", "<b>Solvers handle million-variable instances (M04 §4)</b>"],
     ["<b>'NP-hard means exponential'</b>", "<b>It means no known polynomial algorithm, conditionally (M03 §2)</b>"],
     ["<b>'Quantum computers solve NP-complete problems'</b>", "<b>BQP is not believed to contain NP (CSCE 627 §11)</b>"],
     ["<b>'Polynomial means fast'</b>", "<b>n⁵ with a large constant is neither (M01 §4)</b>"],
     ["<b>'P ≠ NP is basically proved'</b>", "<b>Best general circuit lower bound is 5n (M09 §2)</b>"],
     ["<b>'This problem is NP-complete, so give up'</b>", "<b>Five productive responses, all routine (M04 §4)</b>"],
   ],
   "footnote": "<b>Every overreach treats a conditional worst-case "
               "asymptotic statement as an unconditional practical "
               "one</b> — which is the same shape as "
               "CSCE 627 §13's errors, with conditionality "
               "added.",
   "note": "Students meet all six, and the common shape is the useful "
           "thing."},

  {"t": "section", "label": "Part 3", "title": "Using a hardness result",
   "blurb": "Productively."},

  {"t": "bullets", "kicker": "Productive", "title": "What to do with 'your problem is NP-hard'",
   "items": [
     "<b>Run a solver first.</b> <b>It costs an afternoon and it "
     "frequently just works</b> (CSCE 669 §13).",
     "",
     "<b>Find the parameter</b> (Module 12 §1), <b>and "
     "measure whether it is small in your data.</b> <b>The highest-value "
     "step.</b>",
     "",
     "<b>Look up both approximation sides</b> "
     "(Module 11 §4), and implement the optimal algorithm if the "
     "question is closed.",
     "",
     "<b>Restrict the problem</b> — planar, bounded degree, "
     "bipartite. <b>Frequently your instances already are.</b>",
     "",
     "<b>And always compute a bound</b>, so a heuristic's result "
     "becomes 'within 7% of optimal' rather than a number.",
   ],
   "footnote": "<b>All five are routine</b>, and <b>the hardness result "
               "is what tells you to do them rather than keep looking for "
               "an exact polynomial algorithm.</b>"},

  {"t": "section", "label": "Part 4", "title": "The semester and the claim",
   "blurb": "Closing honestly."},

  {"t": "table", "kicker": "Semester 8", "title": "Three courses, three certainties",
   "header": ["Course", "Central claim form", "Certainty"],
   "widths": [2.3, 4.4, 5.3],
   "rows": [
     ["<b>CSCE 627</b>", "<b>'No algorithm exists'</b>", "<b>Unconditional. Permanent</b>"],
     ["<b>CSCE 637</b>", "<b>'No polynomial algorithm, unless P = NP'</b>", "<b>Conditional on an open question</b>"],
     ["<b>CSCE 658</b>", "<b>'Randomness helps here'</b>", "<b>Proved in cases; removability open (M08 §3)</b>"],
   ],
   "footnote": "<b>The certainty decreases as the resource becomes more "
               "refined</b> — which is the honest shape of a theory "
               "semester and is worth stating rather than presenting all "
               "three as equivalent.",
   "note": "The certainty gradient is the semester's real lesson."},

  {"t": "bullets", "kicker": "Claims", "title": "What a complexity claim can honestly assert",
   "items": [
     "<b>'This problem is NP-complete; here is the reduction and the "
     "certificate.'</b> <b>Checkable, and both halves present.</b>",
     "",
     "<b>'No polynomial algorithm exists unless P = NP'</b> — "
     "<b>with the conditionality stated, because it is real.</b>",
     "",
     "<b>'The best achievable ratio is 7/8 and that is optimal unless "
     "P = NP.'</b> Both sides, with the condition.",
     "",
     "<b>'It is FPT in treewidth, and our instances have treewidth "
     "under 12.'</b> <b>A theorem plus a measurement, which is the "
     "strongest useful form.</b>",
     "",
     "<b>And what you cannot say: 'this is intractable'</b> — "
     "<b>unqualified, unconditional, and about your instances.</b>",
   ],
   "footnote": "<b>The fourth form is the one to aim for:</b> a theorem "
               "about a parameter plus a measurement of that parameter is "
               "both rigorous and about your actual problem."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can prove a problem NP-complete with both halves, "
            "place problems in co-NP, PSPACE, and the hierarchy, and "
            "prove a hierarchy theorem.</b>",
            "<b>You know why the central question is open — three "
            "barrier results — and what the field can and cannot "
            "prove, including the 5n figure.</b>",
            "<b>And you can take a hard problem and do something "
            "productive</b>: a parameter, a kernel, an approximation "
            "with both bounds, a fine-grained lower bound. <b>Which is "
            "the practical skill.</b>",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it means stating the "
            "conditionality</b> — because almost everything in this "
            "course rests on a conjecture, and saying so is the "
            "difference between a result and a slogan."]},
 ],
 "takeaways": [
   "A great deal is proved — hierarchy theorems, completeness, "
   "IP = PSPACE, PCP, three barriers — and almost every separation is "
   "open.",
   "The proved results are mostly equalities and completeness; the open "
   "ones are separations, which is a structural observation about the "
   "field's techniques.",
   "Every overreach treats a conditional worst-case asymptotic statement "
   "as an unconditional practical one.",
   "The productive response to NP-hardness is five routine steps, and the "
   "hardness result is what tells you to take them.",
   "The semester has a certainty gradient: unconditional in CSCE 627, "
   "conditional here, and partly open in CSCE 658.",
   "The strongest useful claim form is a theorem about a parameter plus a "
   "measurement of that parameter in your instances.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What is proved and what is conjectured"),
  ("table", ["Statement", "Status"],
   [["<b>P &ne; EXPTIME, NL &ne; PSPACE, and the hierarchy theorems "
     "generally</b>", "<b>PROVED</b> (Module 07 &sect;1)"],
    ["<b>Cook–Levin, and the NP-completeness of thousands of "
     "problems</b>", "<b>PROVED</b> (Module 04)"],
    ["<b>PSPACE = NPSPACE (Savitch); NL = co-NL "
     "(Immerman–Szelepcs&eacute;nyi)</b>",
     "<b>PROVED</b> (Module 06 &sect;2)"],
    ["<b>IP = PSPACE; the PCP theorem; zero-knowledge for all of "
     "NP</b>", "<b>PROVED</b> (Module 10)"],
    ["<b>Three barrier results: relativisation, natural proofs, "
     "algebrisation</b>", "<b>PROVED</b> (Modules 07, 09)"],
    ["<b>P &ne; NP</b>", "<b>OPEN. Widely believed</b> (Module 03 "
     "&sect;3)"],
    ["<b>NP &ne; co-NP; the polynomial hierarchy being strict; "
     "NC &ne; P; BPP = P</b>", "<b>ALL OPEN</b>"],
    ["<b>Any super-linear lower bound on general circuits for an "
     "explicit function</b>",
     "<b>OPEN. The best known is about 5n</b> (Module 09 &sect;2)"]],
   [0.55, 0.45]),
  ("p", "<b>A great deal is proved and the central question is not</b> "
        "— and the structural observation worth making is that "
        "<b>the proved results are mostly <i>equalities</i> and "
        "<i>completeness</i> results, while almost every <i>separation</i> "
        "is open.</b> <b>Which is exactly what the barrier results "
        "explain</b> (Module 07 &sect;4): the field's techniques are "
        "good at showing two things are the same and bad at showing they "
        "differ, and that is now a theorem rather than an observation."),

  ("h1", "2 &nbsp; The overreaches"),
  ("table", ["The claim", "The correction"],
   [["<b>'NP-complete means intractable.'</b>",
     "<b>SAT solvers handle instances with millions of variables</b> "
     "(Module 04 &sect;4, CSCE 625 Module 08). The label is about "
     "worst-case asymptotics, not about your instances."],
    ["<b>'NP-hard means it takes exponential time.'</b>",
     "<b>It means no polynomial algorithm is known and finding one would "
     "resolve P versus NP</b> — <b>which is conditional</b> "
     "(Module 03 &sect;2). <b>No exponential lower bound is "
     "proved</b> for any NP-complete problem."],
    ["<b>'Quantum computers will solve NP-complete problems.'</b>",
     "<b>BQP is not believed to contain NP</b>, and Grover's algorithm "
     "gives a quadratic speedup rather than an exponential one "
     "(CSCE 627 Module 11 &sect;3, CSCE 640)."],
    ["<b>'Polynomial means fast.'</b>",
     "<b>n&#8309; with a large constant is neither fast nor "
     "practical</b> (Module 01 &sect;4, Module 02 &sect;1's "
     "objections)."],
    ["<b>'P &ne; NP is basically proved.'</b>",
     "<b>The best general circuit lower bound is about 5n and we believe "
     "the truth is exponential</b> (Module 09 &sect;2). <b>The gap is "
     "the whole problem.</b>"],
    ["<b>'This problem is NP-complete, so give up.'</b>",
     "<b>Five productive responses, all routine</b> (Module 04 "
     "&sect;4, &sect;3 below). <b>The most consequential overreach, "
     "because it stops work that would have succeeded.</b>"]],
   [0.38, 0.62]),
  ("p", "<b>Every overreach treats a conditional, worst-case, asymptotic "
        "statement as an unconditional, typical-case, practical one.</b> "
        "<b>Which is the same shape as CSCE 627 Module 13 "
        "&sect;2's errors, with conditionality added as a fourth way to "
        "go wrong</b> — and recognising the shape is faster than "
        "refuting each instance."),

  ("break",),
  ("h1", "3 &nbsp; Using a hardness result productively"),
  ("ul", ["<b>Run a solver first.</b> <b>It costs an afternoon and it "
          "frequently just works</b> (CSCE 669 Module 13 "
          "&sect;1) — and discovering that your instances are easy "
          "is the cheapest possible outcome.",
          "<b>Find the parameter</b> (Module 12 &sect;1), <b>and "
          "measure whether it is actually small in your data.</b> "
          "<b>The highest-value step in the list</b>, and the one most "
          "often skipped because parameterised complexity is less widely "
          "taught.",
          "<b>Look up both approximation sides</b> (Module 11 "
          "&sect;4), <b>and implement the known optimal algorithm if the "
          "question is closed</b> — twenty minutes, and it sometimes "
          "ends the project in the best way.",
          "<b>Restrict the problem</b> — planar, bounded degree, "
          "bipartite, interval, chordal. <b>Frequently your instances "
          "already satisfy a restriction that makes the problem "
          "polynomial</b>, and nobody checked.",
          "<b>And always compute a bound</b>, even when using a "
          "heuristic, <b>so the result becomes 'within 7% of optimal' "
          "rather than a number</b> (CSCE 669 Module 13 &sect;3). "
          "<b>All five are routine</b>, and <b>the hardness result is "
          "what tells you to do them rather than continue looking for an "
          "exact polynomial algorithm</b> — which is the "
          "classification's whole operational value (Module 02 "
          "&sect;4)."]),

  ("h1", "4 &nbsp; The semester, and the honest claim"),
  ("table", ["Course", "Central claim form", "Certainty"],
   [["<b>CSCE 627</b>", "<b>'No algorithm exists.'</b>",
     "<b>Unconditional. Permanent.</b>"],
    ["<b>CSCE 637 (this one)</b>",
     "<b>'No polynomial-time algorithm, unless P = NP.'</b>",
     "<b>Conditional on a question open for fifty years</b>, with three "
     "theorems explaining why it is open."],
    ["<b>CSCE 658</b>", "<b>'Randomness helps here.'</b>",
     "<b>Proved in specific cases; whether it is ever <i>essential</i> is "
     "open</b> (Module 08 &sect;3's derandomisation question)."]],
   [0.21, 0.37, 0.42]),
  ("p", "<b>The certainty decreases as the resource under study becomes "
        "more refined</b> — computability is settled, time complexity "
        "is mostly conjectural, and the value of randomness is open in "
        "principle. <b>Which is the honest shape of a theory semester, "
        "and is worth stating rather than presenting the three as "
        "equivalent</b>: a student who leaves believing P &ne; NP is "
        "proved has been badly served."),
  ("ul", ["<b>'This problem is NP-complete; here is the reduction from "
          "3-SAT and here is the certificate.'</b> <b>Checkable by "
          "anyone, and both halves present</b> (Module 04 &sect;1).",
          "<b>'No polynomial-time algorithm exists unless P = NP'</b> "
          "— <b>with the conditionality stated, because it is "
          "real</b> and because omitting it is the overreach of "
          "&sect;2's second row.",
          "<b>'The best achievable approximation ratio is 7/8, and 7/8 is "
          "optimal unless P = NP.'</b> Both sides, with the condition "
          "attached (Module 11 &sect;1).",
          "<b>'The problem is fixed-parameter tractable in treewidth, and "
          "our instances have treewidth under 12.'</b> <b>A theorem plus "
          "a measurement, which is the strongest useful form available</b> "
          "— it is rigorous and it is about your actual problem, which "
          "no other claim form in this course manages simultaneously.",
          "<b>And what you cannot honestly say: 'this is "
          "intractable'</b> — unqualified, unconditional, and "
          "implicitly about your instances. <b>Three errors in one "
          "word</b>, and it is the most common thing said about an "
          "NP-complete problem."]),
  ("callout", "Where this course leaves you",
   ["<b>You can prove a problem NP-complete with both halves present, "
    "place problems in co-NP, PSPACE, and the polynomial hierarchy by "
    "counting quantifiers, and prove a hierarchy theorem from "
    "scratch.</b>",
    "<b>You know why the central question is open — three barrier "
    "results — and what the field can and cannot prove, including "
    "the 5n figure</b>, which is the single most calibrating number in "
    "the subject.",
    "<b>And you can take a hard problem and do something productive with "
    "it:</b> find a parameter, build a kernel, look up both "
    "approximation bounds, check a fine-grained lower bound. <b>Which is "
    "the practical skill, and it is Module 12's material rather than "
    "Module 04's.</b>",
    "<b>The closing rule is the program's, unchanged across twenty-three "
    "courses:</b> <b>state what you measured, state what you assumed, "
    "and never claim more than you established.</b> <b>In complexity "
    "theory it means stating the conditionality</b> — because "
    "<b>almost everything in this course rests on a conjecture, and saying "
    "so is the difference between a result and a slogan.</b>"]),
 ],
 "resources": [
   ("Aaronson &mdash; P =? NP (free survey)",
    "https://www.scottaaronson.com/papers/pnp.pdf",
    "<b>&sect;1 and &sect;2, done properly by someone in the field</b> "
    "— and the best single thing to read after this course."),
   ("Arora & Barak &mdash; the whole book, reread (free draft)",
    "https://theory.cs.princeton.edu/complexity/",
    "<b>Free, and the second reading is different from the first</b> "
    "— particularly chapters 23 and 20."),
   ("Cygan et al. &mdash; Parameterized Algorithms (free PDF)",
    "https://www.mimuw.edu.pl/~malcin/book/",
    "<b>If one book from this course should stay on your desk, it is this "
    "one</b> — Module 12 is where the practical value is."),
   ("Garey & Johnson, appendix; and the modern successors",
    "https://www.worldcat.org/title/1097888",
    "<b>The reduction library</b>, which is what you will actually use "
    "— keep a copy or a bookmark."),
 ],
 "exercises": [
   "<b>Write down which results from this course are proved and which are "
   "conjectured</b>, from memory.",
   "<b>Explain why the proved results are mostly equalities</b>, in terms "
   "of the barriers.",
   "<b>Find three of &sect;2's overreaches in the wild</b> and write the "
   "correction for each.",
   "<b>Explain the common shape of all six</b> in one sentence.",
   "<b>Take an NP-hard problem from your own work and apply all five of "
   "&sect;3's steps.</b> Report which helped.",
   "<b>Compare the three Semester 8 courses' claim forms</b> and say "
   "which you trust most.",
   "<b>Write the honest claim</b> for your Project 1 NP-completeness "
   "result.",
   "<b>Write the honest claim</b> for your Project 2 problem, in "
   "&sect;4's fourth form.",
   "<b>Revisit what you wrote in Module 01's last exercise</b> and report "
   "what changed.",
   "<b>Project 2 is now due.</b> Submit the problem with its hardness "
   "established, the solver results, the easy and hard instance families, "
   "the parameter assessment, the approximation picture with both sides, "
   "any fine-grained bound, and a written answer to 'what does NP-hardness "
   "actually predict here?'",
 ],
 "selfcheck": [
   "Name five proved results and four open ones.",
   "Why are the proved results mostly equalities?",
   "Give six overreaches and the correction to each.",
   "What shape do all six share?",
   "Give the five productive responses to a hardness result.",
   "Which is the highest-value step, and why is it most often skipped?",
   "Compare the three theory courses' claim forms and certainties.",
   "Give four honest claim forms and the one you cannot use.",
   "Which claim form is strongest, and why?",
   "In this course, what does 'state what you assumed' mean?",
 ],
},

]
