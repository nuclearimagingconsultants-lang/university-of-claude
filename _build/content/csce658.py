# -*- coding: utf-8 -*-
"""CSCE 658 Randomized Algorithms — original course content."""

COURSE = {
    "code": "CSCE 658",
    "title": "Randomized Algorithms",
    "tagline": "A coin as an engineering primitive — and the "
               "concentration bounds that make it trustworthy",
    "term": "Semester 8 (with CSCE 627 and CSCE 637)",
    "prereqs": "CSCE 629 Analysis of Algorithms; probability through "
               "expectation, variance, and independence; CSCE 637 "
               "Module 08 for the complexity-class view; linear algebra "
               "for Modules 09–10",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A randomised algorithm you implemented, with its "
                   "failure probability derived and then measured against "
                   "the derivation — plus one deterministic baseline "
                   "it had to beat",
    "description": [
        "<b>CSCE 627 asked what is possible and CSCE 637 asked what it "
        "costs. This course is about a technique</b> — and it is the "
        "most immediately usable of the three, because <b>almost every "
        "system you have built already depends on it.</b> Hash tables, "
        "load balancers, caches, sampling, Bloom filters, Monte Carlo "
        "rendering, stochastic gradient descent: all randomised, and all "
        "analysed by the tools of Module 02.",
        "<b>The organising idea is that a probabilistic guarantee is a "
        "guarantee.</b> <b>Module 02 is the whole course in one "
        "module</b>: Markov, Chebyshev, Chernoff, and the union bound, "
        "which between them bound the failure probability of almost "
        "every randomised algorithm anyone writes. <b>A failure "
        "probability of 2⁻⁴⁰ is below the probability "
        "that the hardware computed a deterministic answer correctly</b>, "
        "which is the argument that makes the whole subject respectable.",
        "<b>The second theme is that randomness buys three distinct "
        "things and they are worth separating.</b> <b>It defeats an "
        "adversary</b> (hashing, quicksort's pivot), <b>it simplifies an "
        "algorithm</b> (skip lists against balanced trees), and <b>it "
        "allows sampling where exact computation is infeasible</b> "
        "(streaming, Monte Carlo integration). <b>Module 01 makes the "
        "distinction and the rest of the course keeps it.</b>",
        "<b>The third is that randomness is also a proof technique.</b> "
        "<b>Module 07's probabilistic method proves objects exist by "
        "showing a random one works</b> — which produces "
        "existence results no constructive argument has matched, and "
        "then <b>Module 12 shows how to remove the randomness "
        "afterwards.</b>",
        "<b>And the closing position is about honesty with the "
        "randomness itself.</b> <b>Module 13 is about seeds, "
        "reproducibility, the quality of your generator, and reporting a "
        "failure probability you have actually measured</b> — "
        "because a randomised algorithm whose randomness is not what you "
        "assumed has no guarantee at all.",
    ],
    "outcomes": [
        "Distinguish the three things randomness buys and choose "
        "accordingly.",
        "Apply Markov, Chebyshev, Chernoff, and the union bound "
        "correctly.",
        "Analyse balls-and-bins problems and the power of two choices.",
        "Explain and implement randomised data structures.",
        "Design a sketch for a streaming problem and bound its error.",
        "Explain phase transitions in random graphs.",
        "Use the probabilistic method to prove existence.",
        "Apply randomised rounding to an approximation problem.",
        "Bound a Markov chain's mixing time.",
        "Apply dimension reduction with a stated distortion bound.",
        "Explain where randomness is essential in distributed systems.",
        "Derandomise an algorithm by conditional expectations or limited "
        "independence.",
        "Report a randomised result with its failure probability "
        "measured.",
    ],
    "materials": [
        ("Motwani & Raghavan — Randomized Algorithms",
         "https://www.cambridge.org/core/books/randomized-algorithms/6A3E5CD760413BEF7D0D01BFD5497ACB",
         "<b>The primary source and still the standard.</b> "
         "Modules 02–09 follow it. Library copy; the authors' "
         "lecture notes from the courses it grew out of are free."),
        ("Mitzenmacher & Upfal — Probability and Computing, 2nd "
         "edition",
         "https://www.cambridge.org/core/books/probability-and-computing/7D2016B2EB4B5E5F4F2C4E4F4F4C4E4F",
         "<b>The better first book</b>, and stronger on Modules 02, "
         "03, and 09. Library copy; the authors' course pages carry free "
         "problem sets."),
        ("Alon & Spencer — The Probabilistic Method",
         "https://onlinelibrary.wiley.com/doi/book/10.1002/9781119061957",
         "<b>Module 07's reference</b>, and the book that made the "
         "method a subject. Library copy; Spencer's free lecture notes "
         "cover the core."),
        ("Cormode & Yi — Small Summaries for Big Data (free)",
         "https://web.archive.org/web/20260413113221/http://dimacs.rutgers.edu/~graham/ssbd.html",
         "<b>Module 05's reference, free in full</b> — sketches "
         "and streaming algorithms with their error bounds, written for "
         "practitioners."),
        ("Levin & Peres — Markov Chains and Mixing Times (free "
         "PDF)",
         "https://pages.uoregon.edu/dlevin/MARKOV/",
         "<b>Module 09's reference, free from the authors</b> "
         "— the definitive treatment of mixing, and chapters "
         "1–7 are what this course needs."),
        ("Vadhan — Pseudorandomness (free)",
         "https://people.seas.harvard.edu/~salil/pseudorandomness/",
         "<b>Module 12's reference, free in full</b> — expanders, "
         "extractors, and generators, which is where derandomisation "
         "actually lives."),
    ],
    "tooling": [
        "<b>A language with a decent generator and the ability to seed "
        "it explicitly.</b> <b>Module 13 requires every experiment to be "
        "reproducible</b>, so build seeding in from the first line.",
        "<b>NumPy, or equivalent.</b> <b>Most of this course's "
        "experiments are vectorised sampling</b>, and a loop-based "
        "implementation will make the large-n experiments painful.",
        "<b>A plotting setup for empirical distributions.</b> <b>The "
        "central activity of this course is deriving a bound and then "
        "measuring whether it holds</b>, and that is a histogram against "
        "a curve.",
        "<b>A proper statistical random source available</b> — "
        "<code>secrets</code> or <code>/dev/urandom</code> — "
        "<b>so you can compare it against a weak generator and see the "
        "guarantee fail</b> (Module 13 §2).",
        "<b>A streaming data source</b> for Module 05: a log file, a "
        "packet capture, or a generated stream too large for memory.",
        "<b>And a deterministic baseline for everything.</b> <b>Every "
        "randomised algorithm in this course has a deterministic rival</b>, "
        "and the comparison is the point.",
    ],
    "projects": [
        {"title": "Derive the bound, then measure it", "after": 7,
         "brief": "Implement several randomised algorithms, derive each "
                  "one's failure probability, and measure whether the "
                  "derivation was right.",
         "reqs": [
             "<b>Four algorithms implemented</b> from Modules "
             "03–05, including one data structure and one sketch.",
             "<b>A derived bound for each</b>, with the concentration "
             "inequality named and the steps shown.",
             "<b>An empirical failure rate for each</b>, over enough "
             "trials to resolve the bound.",
             "<b>A plot of empirical against predicted</b> for each, on "
             "a log scale.",
             "<b>One case where the bound is loose</b>, with an "
             "explanation of why.",
             "<b>A deterministic comparison</b> for at least two of the "
             "four.",
         ],
         "done": [
             "<b>Every bound derived rather than cited</b>, with the "
             "inequality named and the independence assumption stated.",
             "<b>The empirical rate consistent with the bound</b>, or "
             "an explanation of the discrepancy — both of which are "
             "acceptable and one of which is more interesting.",
             "<b>The loose case identified and explained</b> — "
             "usually Chebyshev where Chernoff applied, or a union bound "
             "over correlated events.",
             "<b>And the deterministic comparison honest</b>, including "
             "where the deterministic structure wins.",
         ]},
        {"title": "A randomised solution to a real problem", "after": 12,
         "brief": "Solve a problem you care about with randomness, and "
                  "establish what the guarantee actually is.",
         "reqs": [
             "<b>A real problem</b>, with the deterministic approach "
             "implemented first and measured.",
             "<b>A randomised algorithm</b>, with the failure "
             "probability or approximation quality derived.",
             "<b>The seeds fixed and reported</b>, and results across "
             "at least ten seeds.",
             "<b>A sensitivity test on the random source</b>: run it "
             "with a weak generator and report what changes.",
             "<b>A derandomisation attempt</b> (Module 12), or an "
             "argument that none is practical.",
             "<b>The honest claim</b>, in Module 13's form.",
         ],
         "done": [
             "<b>The deterministic baseline measured, not assumed</b> "
             "— and it may win, which is a complete result.",
             "<b>The failure probability derived and measured</b>, and "
             "the two compared.",
             "<b>The weak-generator test performed</b>, because it is "
             "the one thing nobody does and it is where real failures "
             "come from.",
             "<b>And a statement of what the algorithm guarantees, "
             "scoped to the randomness assumption</b> — which is "
             "the graded part.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Why Randomness",
 "subtitle": "Three distinct things a coin buys.",
 "question": "What does randomness actually give you?",
 "outcomes": [
     "Distinguish the three uses of randomness and give examples.",
     "Distinguish Las Vegas from Monte Carlo algorithms.",
     "Explain why a probabilistic guarantee is a guarantee.",
     "Explain the adversary model and what randomness does to it.",
     "Decide whether randomness is the right tool for a problem.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The three uses",
   "blurb": "Worth separating, because they have different "
            "alternatives."},

  {"t": "table", "kicker": "Uses", "title": "What randomness buys, in three kinds",
   "header": ["Use", "Mechanism", "Examples"],
   "widths": [2.7, 4.0, 5.3],
   "rows": [
     ["<b>Defeat an adversary</b>", "<b>The input cannot be chosen against your choices</b>", "<b>Hashing, quicksort pivot, cuckoo hashing</b>"],
     ["<b>Simplify the algorithm</b>", "<b>Expected balance instead of enforced balance</b>", "<b>Skip lists, treaps, random contraction</b>"],
     ["<b>Sample instead of compute</b>", "<b>Estimate from a subset</b>", "<b>Streaming, Monte Carlo integration, SGD</b>"],
   ],
   "footnote": "<b>The alternatives differ:</b> <b>the first can be "
               "replaced by a secret key, the second by a more complex "
               "deterministic structure, and the third frequently cannot "
               "be replaced at all.</b>",
   "note": "Separating the three uses is the organising move of the "
           "course."},

  {"t": "callout", "title": "Defeating an adversary is the use that cannot be replaced by effort",
   "kind": "The first use, examined",
   "body": ["<b>A deterministic hash function has a worst-case input "
            "— whatever collides.</b> <b>And an adversary who knows "
            "your function can construct it</b>, which is how hash-flood "
            "denial of service works.",
            "<b>Randomising the hash choice means the adversary must "
            "beat a function they cannot see</b> — <b>the worst case "
            "still exists and they cannot find it.</b>",
            "<b>So the guarantee changes from 'no bad input exists' "
            "(false) to 'a bad input is unlikely to be hit' "
            "(true).</b>",
            "<b>And this is the use where randomness is irreplaceable "
            "by cleverness</b> — <b>no amount of deterministic "
            "ingenuity removes a worst case that an adversary can "
            "compute.</b> <b>Only a secret does</b>, and a random choice "
            "is the cheapest secret."]},

  {"t": "section", "label": "Part 2", "title": "Two kinds of algorithm",
   "blurb": "And the distinction decides how you report results."},

  {"t": "callout", "title": "Las Vegas is always right; Monte Carlo is usually right",
   "kind": "The distinction that matters most in practice",
   "body": ["<b>Las Vegas: the answer is always correct and the "
            "<i>running time</i> is random.</b> Randomised quicksort, "
            "treaps, Las Vegas perfect hashing construction.",
            "<b>Monte Carlo: the running time is bounded and the "
            "<i>answer</i> may be wrong.</b> Miller–Rabin, "
            "Bloom filters, sketches.",
            "<b>And the difference decides what you must do about "
            "it.</b> <b>A Las Vegas algorithm can simply be re-run, and "
            "a Monte Carlo failure is undetectable</b> unless you can "
            "verify the answer.",
            "<b>So prefer Las Vegas when the choice exists</b>, and "
            "<b>when using Monte Carlo, know which direction the error "
            "goes</b> — <b>a Bloom filter's false positives are "
            "handled differently from false negatives, and it has only "
            "one kind.</b>"]},

  {"t": "table", "kicker": "Comparison", "title": "Reporting the two kinds",
   "header": ["", "Las Vegas", "Monte Carlo"],
   "widths": [2.4, 4.3, 5.3],
   "rows": [
     ["<b>Report</b>", "<b>Expected and tail running time</b>", "<b>Failure probability, and its direction</b>"],
     ["<b>On failure</b>", "<b>It took longer. Re-run</b>", "<b>Wrong answer, possibly silent</b>"],
     ["<b>Detectable?</b>", "<b>Yes — the clock</b>", "<b>Only if you can verify</b>"],
     ["<b>Amplify by</b>", "<b>Re-running on timeout</b>", "<b>Repetition and majority (if two-sided)</b>"],
     ["<b>Example</b>", "<b>Randomised quicksort</b>", "<b>Bloom filter, count-min sketch</b>"],
   ],
   "footnote": "<b>'Which direction does the error go?' is the question "
               "to ask of every Monte Carlo algorithm</b> — "
               "one-sided error is far easier to design around.",
   "note": "The error-direction question is the practical habit to "
           "instil."},

  {"t": "section", "label": "Part 3", "title": "Why a probabilistic guarantee is a guarantee",
   "blurb": "The argument that makes the subject respectable."},

  {"t": "callout", "title": "2⁻⁴⁰ is below the hardware error rate",
   "kind": "The argument, with numbers",
   "body": ["<b>A randomised algorithm with failure probability "
            "2⁻⁴⁰ fails about once in a trillion "
            "runs.</b>",
            "<b>Uncorrected DRAM bit-flip rates are on the order of one "
            "error per gigabyte per month</b>, and a long deterministic "
            "computation touches a great deal of memory.",
            "<b>So the randomised algorithm is more reliable than the "
            "machine running the deterministic one</b> — which "
            "<b>answers the objection that randomised algorithms 'might "
            "be wrong' completely.</b>",
            "<b>And the amplification is cheap:</b> <b>repetition drives "
            "the failure probability down exponentially</b> "
            "(Module 02 §4, CSCE 637 §08), so the "
            "exponent is a design parameter rather than a fact about the "
            "algorithm."]},

  {"t": "section", "label": "Part 4", "title": "When not to",
   "blurb": "The honest limits."},

  {"t": "bullets", "kicker": "When not", "title": "When randomness is the wrong choice",
   "items": [
     "<b>When reproducibility is required and seeding is "
     "impractical.</b> <b>A randomised build or compiler output is a "
     "real problem</b>, and determinism is a feature.",
     "",
     "<b>When the deterministic algorithm is simpler.</b> <b>It "
     "frequently is not</b> — but when it is, take it.",
     "",
     "<b>When you cannot get good randomness.</b> <b>An embedded "
     "device at boot has none</b>, and a weak source voids the "
     "guarantee entirely (Module 13 §2).",
     "",
     "<b>When failure is unbounded in cost.</b> <b>2⁻⁴⁰ "
     "is fine for a cache and not for an irreversible action</b>, "
     "whatever the arithmetic says.",
     "",
     "<b>And when the guarantee is about the average and the "
     "requirement is about the tail</b> — <b>which is the error "
     "to watch for</b> (Module 02 §1).",
   ],
   "footnote": "<b>The average-versus-tail error is the commonest "
               "misuse</b>: an expected-time guarantee says nothing "
               "useful about a latency service level objective."},

  {"t": "callout", "title": "Where this course goes",
   "kind": "The shape of the semester",
   "body": ["<b>Module 02 is the toolkit</b> — Markov, Chebyshev, "
            "Chernoff, the union bound. <b>The whole course in one "
            "module, and the one to know cold.</b>",
            "<b>Modules 03–06: the classical "
            "analyses.</b> Balls and bins, data structures, sketches, "
            "random graphs — <b>the things you have already "
            "used.</b>",
            "<b>Modules 07–10: randomness as a "
            "method.</b> The probabilistic method, randomised rounding, "
            "Markov chains, dimension reduction.",
            "<b>Modules 11–13: distributed systems, "
            "derandomisation, and honesty about the randomness "
            "itself.</b>"]},
 ],
 "takeaways": [
   "Randomness buys three distinct things — defeating an adversary, "
   "simplifying an algorithm, and sampling instead of computing — and "
   "their alternatives differ.",
   "Defeating an adversary is the use that cannot be replaced by "
   "cleverness, only by a secret, and a random choice is the cheapest "
   "secret.",
   "Las Vegas algorithms are always right with random running time; Monte "
   "Carlo have bounded time and may be wrong.",
   "A Las Vegas failure can be re-run and a Monte Carlo failure is "
   "undetectable unless you can verify — so ask which direction the "
   "error goes.",
   "A failure probability of 2⁻⁴⁰ is below the hardware "
   "error rate, which answers the 'might be wrong' objection completely.",
   "The commonest misuse is treating an expected-time guarantee as a "
   "statement about the tail.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The three uses"),
  ("table", ["Use", "The mechanism", "Examples"],
   [["<b>Defeat an adversary</b>",
     "<b>The input cannot be chosen against choices the adversary cannot "
     "see.</b>",
     "<b>Universal hashing, randomised quicksort pivots, cuckoo "
     "hashing, randomised load balancing.</b> See the callout."],
    ["<b>Simplify the algorithm</b>",
     "<b>Expected balance instead of explicitly enforced balance.</b>",
     "<b>Skip lists against balanced trees, treaps against "
     "red-black trees, Karger's random contraction against "
     "deterministic min-cut.</b> The randomised versions are "
     "dramatically shorter."],
    ["<b>Sample instead of computing</b>",
     "<b>Estimate a quantity from a subset rather than examining "
     "everything.</b>",
     "<b>Streaming sketches (Module 05), Monte Carlo integration "
     "(CSCE 647), stochastic gradient descent (CSCE 669 "
     "Module 08).</b>"]],
   [0.22, 0.32, 0.46]),
  ("p", "<b>The alternatives differ, which is why the three are worth "
        "separating:</b> <b>the first can be replaced by a secret key "
        "(and nothing else), the second by a more complex deterministic "
        "structure (which exists and is longer), and the third frequently "
        "cannot be replaced at all</b> — if the data does not fit in "
        "memory, no deterministic algorithm examines all of it either. "
        "<b>So 'can I derandomise this?' has three different answers "
        "depending on which use you are making</b> (Module 12)."),
  ("callout", "Defeating an adversary is the use that cannot be replaced by "
              "effort",
   ["<b>A deterministic hash function has a worst-case input — "
    "whatever set of keys happens to collide.</b> <b>And an adversary "
    "who knows your hash function can construct that input</b>, which is "
    "exactly how hash-flooding denial-of-service attacks work and why "
    "language runtimes now randomise their string hashing.",
    "<b>Randomising the choice of hash function means the adversary must "
    "defeat a function they cannot see</b> — <b>the worst-case "
    "input still exists, and they cannot find it.</b>",
    "<b>So the guarantee changes from 'no bad input exists' (which is "
    "false) to 'a bad input is unlikely to be hit' (which is true and "
    "quantifiable)</b> — and the second guarantee is the one you can "
    "actually have.",
    "<b>And this is the use where randomness is irreplaceable by "
    "cleverness.</b> <b>No amount of deterministic ingenuity removes a "
    "worst case that an adversary can compute</b>, because the adversary "
    "gets to see your algorithm. <b>Only a secret helps, and a random "
    "choice is the cheapest available secret</b> — which is also why "
    "this use is the one that overlaps with cryptography "
    "(CSCE 711)."]),

  ("h1", "2 &nbsp; Las Vegas and Monte Carlo"),
  ("callout", "Las Vegas is always right; Monte Carlo is usually right",
   ["<b>Las Vegas: the answer is always correct, and the <i>running "
    "time</i> is a random variable.</b> Randomised quicksort, treaps, the "
    "construction phase of perfect hashing.",
    "<b>Monte Carlo: the running time is bounded, and the <i>answer</i> "
    "may be wrong.</b> Miller–Rabin primality, Bloom filters, "
    "count-min sketches, almost all of Module 05.",
    "<b>And the difference decides what you must do about it.</b> <b>A "
    "Las Vegas algorithm can simply be re-run when it takes too long "
    "— you can see that it has — whereas a Monte Carlo failure "
    "is silent</b> unless you have an independent way to verify the "
    "answer.",
    "<b>So prefer Las Vegas whenever the choice exists</b>, and <b>when "
    "using Monte Carlo, establish which direction the error goes</b> "
    "— <b>a Bloom filter has false positives and never false "
    "negatives, which is what makes it usable as a pre-filter</b>, and a "
    "structure with the opposite asymmetry would be useless for that "
    "purpose. <b>One-sided error is far easier to design around, and "
    "knowing which side you have is the first question.</b>"]),
  ("table", ["", "Las Vegas", "Monte Carlo"],
   [["<b>What to report</b>",
     "<b>Expected running time <i>and</i> a tail bound.</b>",
     "<b>The failure probability, and the direction of the error.</b>"],
    ["<b>What a failure is</b>",
     "<b>It took longer than expected. Re-run it.</b>",
     "<b>A wrong answer, possibly silent.</b>"],
    ["<b>Detectable?</b>", "<b>Yes — by the clock.</b>",
     "<b>Only if you can independently verify the answer</b>, which for "
     "primality you cannot cheaply and for a found factor you can."],
    ["<b>How to amplify</b>",
     "<b>Re-run on a timeout</b>, which bounds the tail.",
     "<b>Repetition and majority vote</b>, if the error is two-sided; "
     "repetition alone if one-sided (Module 02 &sect;4)."],
    ["<b>Canonical example</b>", "<b>Randomised quicksort.</b>",
     "<b>Bloom filter, count-min sketch.</b>"]],
   [0.19, 0.36, 0.45]),

  ("break",),
  ("h1", "3 &nbsp; Why a probabilistic guarantee is a guarantee"),
  ("callout", "2⁻⁴⁰ is below the hardware error rate",
   ["<b>A randomised algorithm with failure probability "
    "2<super>&minus;40</super> fails roughly once in a trillion runs.</b> "
    "At a thousand runs per second it fails about once every thirty "
    "thousand years.",
    "<b>Measured uncorrected DRAM bit-flip rates are on the order of one "
    "error per gigabyte per month</b>, and <b>a long deterministic "
    "computation touches a great deal of memory for a long time.</b> So "
    "its probability of producing a wrong answer is not zero either, and "
    "is frequently larger.",
    "<b>So the randomised algorithm is more reliable than the machine "
    "running the deterministic one</b> — <b>which answers the "
    "objection that randomised algorithms 'might be wrong' completely "
    "rather than partially.</b> <b>Everything might be wrong; the "
    "question is the probability, and only one of the two has a bound you "
    "can compute.</b>",
    "<b>And the amplification is cheap:</b> <b>repetition drives the "
    "failure probability down exponentially</b> (Module 02 &sect;4, "
    "CSCE 637 Module 08 &sect;1), <b>so the exponent is a design "
    "parameter rather than a fixed property of the algorithm</b> — "
    "you choose how reliable you want it to be, and pay linearly for an "
    "exponential improvement. <b>That trade is the best one in this "
    "course.</b>"]),

  ("h1", "4 &nbsp; When randomness is the wrong choice"),
  ("ul", ["<b>When reproducibility is required and seeding is "
          "impractical.</b> <b>A randomised build process or a compiler "
          "whose output varies between runs is a real operational "
          "problem</b>, and reproducible builds are a security property "
          "— so <b>determinism is sometimes the feature</b> "
          "(Module 13 &sect;1).",
          "<b>When the deterministic algorithm is genuinely simpler.</b> "
          "<b>It frequently is not</b> — a skip list against a "
          "red-black tree is the standard illustration — <b>but when "
          "it is, take it.</b>",
          "<b>When you cannot get good randomness.</b> <b>An embedded "
          "device at first boot has essentially no entropy</b>, and "
          "<b>a weak source voids the guarantee entirely</b> rather than "
          "degrading it (Module 13 &sect;2) — which has caused "
          "real and serious failures.",
          "<b>When the cost of a failure is unbounded.</b> "
          "<b>2<super>&minus;40</super> is fine for a cache lookup and "
          "not for an irreversible financial or physical action</b>, "
          "whatever &sect;3's arithmetic says — because the "
          "arithmetic multiplies probability by cost and one of the two "
          "may not be finite.",
          "<b>And when the guarantee is about the average and the "
          "requirement is about the tail.</b> <b>Which is the commonest "
          "misuse</b> (Module 02 &sect;1): <b>an expected-time "
          "guarantee says nothing useful about a 99th-percentile latency "
          "objective</b> (CSCE 678 Module 06), and the two are "
          "routinely conflated by people who have read the expected-case "
          "analysis and stopped."]),
  ("callout", "Where this course goes",
   ["<b>Module 02 is the toolkit</b> — Markov, Chebyshev, "
    "Chernoff, and the union bound. <b>It is the whole course in one "
    "module, and the one to know cold</b>: almost every subsequent "
    "analysis is one of those four applied to a well-chosen random "
    "variable.",
    "<b>Modules 03 through 06 are the classical analyses.</b> Balls "
    "and bins, randomised data structures, sketches and streaming, and "
    "random graphs — <b>which is to say, the things you have already "
    "used without analysing.</b>",
    "<b>Modules 07 through 10 are randomness as a method.</b> The "
    "probabilistic method as a proof technique, randomised rounding for "
    "approximation, Markov chains and mixing, and dimension reduction.",
    "<b>Modules 11 through 13 are randomness in systems, "
    "derandomisation, and honesty about the randomness itself</b> "
    "— and the last of those is the one with the most practical "
    "consequence."]),
 ],
 "resources": [
   ("Mitzenmacher & Upfal &mdash; Probability and Computing, chapter 1",
    "https://www.cambridge.org/core/books/probability-and-computing/7D2016B2EB4B5E5F4F2C4E4F4F4C4E4F",
    "<b>The three uses and the two kinds of algorithm</b>, with the "
    "verifying-matrix-multiplication example that motivates &sect;2."),
   ("Motwani & Raghavan &mdash; Randomized Algorithms, chapter 1",
    "https://www.cambridge.org/core/books/randomized-algorithms/6A3E5CD760413BEF7D0D01BFD5497ACB",
    "<b>The Las Vegas / Monte Carlo distinction</b> and the "
    "adversary framing of &sect;1."),
   ("Crosby & Wallach &mdash; Denial of Service via Algorithmic "
    "Complexity Attacks (free)",
    "https://www.usenix.org/legacy/events/sec03/tech/full_papers/crosby/crosby.pdf",
    "<b>&sect;1's adversary use, as an attack</b> — and the paper "
    "that caused language runtimes to randomise their hashing."),
   ("Schroeder, Pinheiro & Weber &mdash; DRAM Errors in the Wild "
    "(free)",
    "https://www.cs.toronto.edu/~bianca/papers/sigmetrics09.pdf",
    "<b>&sect;3's hardware error rates, measured at scale</b> — "
    "which is what makes the argument quantitative rather than "
    "rhetorical."),
 ],
 "exercises": [
   "<b>Classify five randomised algorithms you have used</b> by which of "
   "the three uses they make.",
   "<b>For each, say what the deterministic alternative is</b> and "
   "whether one exists.",
   "<b>Construct a hash-collision attack</b> against a deterministic hash "
   "function, and measure the slowdown.",
   "<b>Randomise the hash choice</b> and confirm the attack fails.",
   "<b>Classify five algorithms as Las Vegas or Monte Carlo</b>, and for "
   "the Monte Carlo ones state the error direction.",
   "<b>Implement randomised quicksort</b> and plot its running-time "
   "distribution over many runs.",
   "<b>Compute how many repetitions of a 1/3-error algorithm</b> give "
   "failure below 2⁻⁴⁰.",
   "<b>Find the uncorrected error rate</b> for a machine you use, and "
   "compare.",
   "<b>Find a case where a randomised algorithm was the wrong "
   "choice</b> — reproducibility, entropy, or cost — and "
   "describe it.",
   "<b>Write down what you expect randomness to be good for</b>, and "
   "keep it for Module 13.",
 ],
 "selfcheck": [
   "Name the three uses of randomness and an example of each.",
   "How do their deterministic alternatives differ?",
   "Why is the adversary use irreplaceable by cleverness?",
   "Distinguish Las Vegas from Monte Carlo on five axes.",
   "Why does the error direction matter for Monte Carlo?",
   "Give the hardware-error argument with numbers.",
   "Why is the failure exponent a design parameter?",
   "Name five situations where randomness is the wrong choice.",
   "What is the commonest misuse of a randomised guarantee?",
 ],
},

]

for _b in ("c658_b2", "c658_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
