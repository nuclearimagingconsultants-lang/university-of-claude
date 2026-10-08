# -*- coding: utf-8 -*-
"""CSCE 658 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Concentration",
 "subtitle": "The whole course in one module.",
 "question": "How do you bound the probability that a random variable "
             "misbehaves?",
 "outcomes": [
     "Apply Markov's inequality and know its weakness.",
     "Apply Chebyshev and explain what the variance buys.",
     "Apply Chernoff bounds and state the independence "
     "requirement.",
     "Apply the union bound and recognise when it is wasteful.",
     "Choose the right inequality for a given situation.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The ladder",
   "blurb": "Four inequalities, increasing in strength and in what they "
            "assume."},

  {"t": "eq", "kicker": "The ladder", "title": "Four bounds, in order",
   "eqs": [
     ("Markov:  P(X ≥ a) ≤ E[X] / a",
      "Needs only non-negativity and the mean. Very weak, and it "
      "always applies."),
     ("Chebyshev:  P(|X − μ| ≥ kσ) ≤ "
      "1/k²",
      "Needs the variance. Polynomial decay — much better, and "
      "still weak."),
     ("Chernoff:  P(X ≥ (1+δ)μ) ≤ "
      "e^(−δ²μ/3)",
      "Needs INDEPENDENCE. Exponential decay — and that is the "
      "bound the whole subject rests on."),
     ("Union bound:  P(∪ Aᵢ) ≤ Σ P(Aᵢ)",
      "Needs nothing at all. Combines bounds across many events."),
   ],
   "caption": "<b>Each step up assumes more and gives more</b> — "
              "and <b>the jump from polynomial to exponential at Chernoff "
              "is where randomised algorithms become practical.</b>",
   "note": "Present it as a ladder; students otherwise learn four "
           "unrelated facts."},

  {"t": "callout", "title": "Markov is weak, always applies, and is the source of the others",
   "kind": "Why the weakest bound matters",
   "body": ["<b>P(X ≥ a) ≤ E[X]/a, for non-negative "
            "X.</b> <b>That is all it needs</b> — no variance, no "
            "independence, no distribution.",
            "<b>And it is very weak:</b> it gives only 1/k decay, so "
            "the probability of exceeding ten times the mean is bounded "
            "by 1/10 — which is usually a vast overestimate.",
            "<b>But Chebyshev is Markov applied to "
            "(X − μ)²</b>, and <b>Chernoff is Markov "
            "applied to e^(tX)</b> — <b>so the whole ladder is "
            "Markov with a cleverly chosen function.</b>",
            "<b>Which is worth knowing because it tells you how to "
            "derive a bound you have not memorised:</b> <b>find a "
            "non-negative function whose expectation you can compute, and "
            "apply Markov to it.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Chernoff",
   "blurb": "The bound that does the work."},

  {"t": "code", "kicker": "Chernoff", "title": "The form to remember, and what it requires",
   "lang": "text", "code": """
  FOR X = sum of n INDEPENDENT indicator variables, with
  mean mu:

      upper tail:  P(X >= (1+d) mu) <= exp(-d^2 mu / 3)
                                          for 0 < d <= 1
      lower tail:  P(X <= (1-d) mu) <= exp(-d^2 mu / 2)

  THE EXPONENT CONTAINS mu, which is the whole point: the
  MORE trials, the TIGHTER the concentration. A sum of a
  million coin flips is within 0.5% of its mean with
  probability about 1 - 2e^-8.

  WHAT IT REQUIRES: INDEPENDENCE. State it every time. The
  bound is simply false for dependent variables, and the
  commonest error in this subject is applying it to
  variables that are not independent.

  WHAT TO DO WHEN THEY ARE NOT
      NEGATIVE ASSOCIATION -- Chernoff still holds. Balls
          into bins has this (Module 03).
      MARTINGALES / Azuma -- bounded differences along a
          process. Covers many dependent cases.
      McDIARMID -- a function of independent variables that
          changes little when one input changes.
      OR Chebyshev, which needs only pairwise independence
          and is much weaker (Module 12 uses this).
""",
   "caption": "<b>Independence is the assumption to state out loud</b> "
              "— and the three alternatives cover most of the cases "
              "where it fails.",
   "note": "The dependent-variable fallback list is what makes this "
           "usable in practice."},

  {"t": "section", "label": "Part 3", "title": "The union bound",
   "blurb": "Cheap, general, and sometimes wasteful."},

  {"t": "callout", "title": "The union bound turns one bound into many, at a linear cost",
   "kind": "The workhorse for 'all of them are fine'",
   "body": ["<b>P(some bad event happens) ≤ Σ P(each "
            "bad event).</b> <b>No independence needed, which is why it "
            "is used constantly.</b>",
            "<b>The standard pattern:</b> <b>bound one bin's overflow "
            "by 1/n², union over n bins, and conclude no bin "
            "overflows with probability 1 − 1/n</b> — <b>which "
            "is how every 'with high probability, all of them' result is "
            "obtained.</b>",
            "<b>So design the per-event bound to be 1/n^c</b>, because "
            "the union over n events then still leaves you "
            "1/n^(c−1).",
            "<b>And it is wasteful when events are strongly "
            "correlated</b> — <b>the Lovász local lemma</b> "
            "(Module 07 §3) <b>is the tool for when a union "
            "bound gives something greater than one and the events are "
            "only locally dependent.</b>"]},

  {"t": "table", "kicker": "Choosing", "title": "Which inequality to reach for",
   "header": ["Situation", "Use", "Why"],
   "widths": [3.4, 2.8, 4.9],
   "rows": [
     ["<b>Only the mean known</b>", "<b>Markov</b>", "<b>It is all you can do</b>"],
     ["<b>Variance known, dependence unclear</b>", "<b>Chebyshev</b>", "<b>Needs only pairwise independence</b>"],
     ["<b>Sum of independent indicators</b>", "<b>Chernoff</b>", "<b>Exponential. Almost always this one</b>"],
     ["<b>'All n of them are fine'</b>", "<b>Union bound</b>", "<b>On top of whichever per-event bound</b>"],
     ["<b>Bounded-difference function</b>", "<b>McDiarmid</b>", "<b>Dependence handled by the structure</b>"],
     ["<b>Locally dependent bad events</b>", "<b>Local lemma</b>", "<b>When the union bound exceeds 1 (M07)</b>"],
   ],
   "footnote": "<b>The third row covers most of what you will do</b> "
               "— and <b>recognising a quantity as a sum of "
               "independent indicators is the skill</b>, more than "
               "knowing the inequality.",
   "note": "Framing it as a lookup table makes the module usable."},

  {"t": "section", "label": "Part 4", "title": "Amplification",
   "blurb": "Why the failure exponent is a design parameter."},

  {"t": "callout", "title": "Repetition converts a weak guarantee into any guarantee you want",
   "kind": "The practical consequence",
   "body": ["<b>One-sided error: repeat k times and accept only if all "
            "k accept.</b> <b>Failure probability "
            "p^k</b> — exponential in k, for linear cost.",
            "<b>Two-sided error: repeat and take the majority.</b> "
            "<b>A Chernoff bound on the number of correct runs gives "
            "exponential decay</b> — which is "
            "CSCE 637 §08's error amplification, derived here.",
            "<b>So a 1/3-error algorithm run 100 times has failure "
            "probability below 2⁻³⁰</b>, and <b>the "
            "exponent is yours to choose.</b>",
            "<b>Which is the single most useful fact in this "
            "module:</b> <b>you do not have to accept the algorithm's "
            "natural error rate</b>, and the cost of improving it is "
            "linear while the improvement is exponential."]},

  {"t": "bullets", "kicker": "Errors", "title": "The four mistakes people make with these bounds",
   "items": [
     "<b>Applying Chernoff without independence.</b> <b>The "
     "commonest error, and the bound is simply false</b> — check "
     "the assumption and name a fallback if it fails.",
     "",
     "<b>Confusing the expectation with the tail.</b> <b>An "
     "expected-time bound is not a latency guarantee</b> "
     "(Module 01 §4).",
     "",
     "<b>Union-bounding over too many events.</b> <b>If the per-event "
     "bound is 1/n and there are n events, you have proved "
     "nothing.</b>",
     "",
     "<b>Using Chebyshev where Chernoff applied</b> — which gives "
     "a polynomial bound where an exponential one was available, and "
     "looks like a weak result.",
     "",
     "<b>And reporting the bound rather than measuring.</b> "
     "<b>Measure, and compare against the bound</b> "
     "(Module 13).",
   ],
   "footnote": "<b>The independence check is the one to make "
               "habitual</b> — write the assumption down before "
               "applying the bound, every time."},
 ],
 "takeaways": [
   "The four bounds form a ladder — Markov, Chebyshev, Chernoff, "
   "union — each assuming more and giving more.",
   "Chebyshev is Markov applied to the squared deviation and Chernoff is "
   "Markov applied to an exponential, so the whole ladder is one "
   "inequality with a chosen function.",
   "Chernoff's exponent contains the mean, so more trials means tighter "
   "concentration — and it requires independence, which must be "
   "stated.",
   "When independence fails, use negative association, martingales, "
   "McDiarmid, or fall back to Chebyshev.",
   "Design per-event bounds to be 1/n^c so the union over n events still "
   "leaves something.",
   "Repetition converts a weak guarantee into any guarantee you want "
   "— linear cost, exponential improvement, and the exponent is "
   "yours.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The ladder"),
  ("eq", "Markov: &nbsp; P(X &ge; a) &le; E[X] / a &nbsp;&nbsp; "
         "(X &ge; 0)"),
  ("eq", "Chebyshev: &nbsp; P(|X &minus; &mu;| &ge; k&sigma;) &le; "
         "1/k&#178;"),
  ("eq", "Chernoff: &nbsp; P(X &ge; (1+&delta;)&mu;) &le; "
         "exp(&minus;&delta;&#178;&mu;/3)"),
  ("eq", "Union bound: &nbsp; P(A<sub>1</sub> &cup; &hellip; &cup; "
         "A<sub>n</sub>) &le; &Sigma; P(A<sub>i</sub>)"),
  ("p", "<b>Each step up the ladder assumes more and gives more.</b> "
        "Markov needs only non-negativity and the mean; Chebyshev needs "
        "the variance; Chernoff needs independence. <b>And the jump from "
        "polynomial decay (Chebyshev's 1/k&#178;) to exponential decay "
        "(Chernoff's e<super>&minus;&delta;&#178;&mu;/3</super>) is where "
        "randomised algorithms become practical</b> — a polynomial "
        "tail bound rarely gives a usable failure probability and an "
        "exponential one almost always does. <b>Presenting these as a "
        "ladder rather than as four facts is the right framing</b>, "
        "because the question in practice is always 'how much can I "
        "assume, and therefore which rung am I on'."),
  ("callout", "Markov is weak, always applies, and is the source of the "
              "others",
   ["<b>P(X &ge; a) &le; E[X]/a, for any non-negative X.</b> <b>That is "
    "all it needs</b> — no variance, no independence, no "
    "distributional assumption of any kind.",
    "<b>And it is correspondingly weak:</b> it gives only 1/k decay, so "
    "the probability of exceeding ten times the mean is bounded by 1/10 "
    "— <b>which is usually a vast overestimate</b>, and is "
    "frequently a useless bound in practice.",
    "<b>But Chebyshev is Markov applied to the non-negative variable "
    "(X &minus; &mu;)&#178;</b>, whose expectation is the variance; "
    "<b>and Chernoff is Markov applied to e<super>tX</super></b>, "
    "optimised over t. <b>So the whole ladder is Markov with a cleverly "
    "chosen function.</b>",
    "<b>Which is worth knowing because it tells you how to derive a "
    "bound you have not memorised:</b> <b>find a non-negative function "
    "of your variable whose expectation you can compute, apply Markov to "
    "it, and translate back.</b> <b>That procedure is the actual "
    "technique</b>, and the three named inequalities are three instances "
    "of it."]),

  ("h1", "2 &nbsp; Chernoff"),
  ("code", """FOR X = a sum of n INDEPENDENT indicator variables, with
mean mu:

    upper tail:  P(X >= (1+d) mu) <= exp(-d^2 mu / 3)
                                        for 0 < d <= 1
    lower tail:  P(X <= (1-d) mu) <= exp(-d^2 mu / 2)

THE EXPONENT CONTAINS mu, which is the whole point: the
MORE trials, the TIGHTER the concentration. A sum of a
million fair coin flips lies within 0.5% of its mean with
probability about 1 - 2e^-8.

WHAT IT REQUIRES: INDEPENDENCE. State it every time. The
bound is simply FALSE for dependent variables, and applying
it to variables that are not independent is the commonest
error in this subject.

WHAT TO DO WHEN THEY ARE NOT INDEPENDENT
    NEGATIVE ASSOCIATION -- Chernoff still holds. Balls
        thrown into bins has this property (Module 03).
    MARTINGALES / Azuma -- bounded differences along a
        process; covers many dependent cases naturally.
    McDIARMID -- a function of independent variables that
        changes by at most c_i when input i changes.
    OR Chebyshev, which needs only PAIRWISE independence
        and is much weaker (and is exactly what Module 12's
        derandomisation exploits)."""),
  ("p", "<b>Independence is the assumption to state out loud</b>, every "
        "time — <b>and the three alternatives above cover most of "
        "the cases where it fails.</b> <b>McDiarmid in particular is "
        "underused</b>: a great many quantities are functions of "
        "independent inputs that change only a little when one input "
        "changes, and that is enough for an exponential bound without "
        "the quantity being a sum at all."),

  ("h1", "3 &nbsp; The union bound"),
  ("callout", "The union bound turns one bound into many, at a linear cost",
   ["<b>P(some bad event happens) &le; the sum of the individual "
    "probabilities.</b> <b>No independence is needed</b>, which is why "
    "it is used constantly and why it is the glue in almost every "
    "high-probability argument.",
    "<b>The standard pattern:</b> <b>bound one bin's overflow "
    "probability by 1/n&#178;, union over the n bins, and conclude that "
    "<i>no</i> bin overflows with probability at least "
    "1 &minus; 1/n</b> — <b>which is how every 'with high "
    "probability, all of them are fine' result in this course is "
    "obtained</b> (Module 03 &sect;1 is the first instance).",
    "<b>So design the per-event bound to be 1/n<super>c</super> for "
    "c &gt; 1</b>, because the union over n events then still leaves you "
    "with 1/n<super>c&minus;1</super> — <b>and that is why "
    "'with high probability' conventionally means "
    "1 &minus; 1/n<super>c</super> in this literature</b>, rather than "
    "being an arbitrary convention.",
    "<b>And it is wasteful when the events are strongly "
    "correlated</b> — if ten thousand nearly identical events each "
    "have probability 1/1000, the union bound gives 10, which is no "
    "bound at all. <b>The Lov&aacute;sz local lemma</b> (Module 07 "
    "&sect;3) <b>is the tool for exactly that situation</b>, when the "
    "events are only <i>locally</i> dependent."]),
  ("table", ["Situation", "Use", "Why"],
   [["<b>Only the mean is known</b>", "<b>Markov</b>",
     "<b>It is all you can do, and it always works.</b>"],
    ["<b>Variance known, dependence unclear</b>", "<b>Chebyshev</b>",
     "<b>It needs only pairwise independence</b>, which is far easier to "
     "establish — and is what makes Module 12's limited-independence "
     "derandomisation possible."],
    ["<b>A sum of independent indicators</b>", "<b>Chernoff</b>",
     "<b>Exponential decay. Almost always this one</b>, and see the "
     "note."],
    ["<b>'All n of them are fine'</b>", "<b>Union bound</b>",
     "<b>Applied on top of whichever per-event bound you used.</b>"],
    ["<b>A function of independent inputs with bounded "
     "differences</b>", "<b>McDiarmid</b>",
     "<b>The dependence is handled by the function's structure</b> rather "
     "than needing to be removed."],
    ["<b>Many locally dependent bad events</b>",
     "<b>Lov&aacute;sz local lemma</b>",
     "<b>When the union bound exceeds 1 and the dependencies are "
     "local</b> (Module 07 &sect;3)."]],
   [0.30, 0.22, 0.48]),
  ("p", "<b>The third row covers most of what you will actually do</b> "
        "— and <b>recognising a quantity as a sum of independent "
        "indicator variables is the skill</b>, considerably more than "
        "knowing the inequality's statement. <b>Most of Modules 03 "
        "through 05 consists of finding that framing for a problem that "
        "did not obviously have it.</b>"),

  ("break",),
  ("h1", "4 &nbsp; Amplification"),
  ("callout", "Repetition converts a weak guarantee into any guarantee you "
              "want",
   ["<b>One-sided error: repeat k times and accept only if all k runs "
    "accept.</b> <b>The failure probability becomes "
    "p<super>k</super></b> — exponential in k, for linear cost, and "
    "no concentration bound is even needed.",
    "<b>Two-sided error: repeat and take the majority answer.</b> <b>A "
    "Chernoff bound on the number of correct runs gives exponential "
    "decay</b> — which is <b>CSCE 637 Module 08 &sect;1's error "
    "amplification, derived here rather than asserted.</b>",
    "<b>So a 1/3-error algorithm run a hundred times has failure "
    "probability below 2<super>&minus;30</super></b>, and <b>the "
    "exponent is yours to choose</b> by choosing k.",
    "<b>Which is the single most useful fact in this module:</b> <b>you "
    "do not have to accept the algorithm's natural error rate</b>, and "
    "<b>the cost of improving it is linear while the improvement is "
    "exponential.</b> <b>That trade is what makes Module 01 "
    "&sect;3's hardware-reliability argument available</b>, and it is "
    "the reason the subject's guarantees are engineering parameters rather "
    "than facts to live with."]),
  ("ul", ["<b>Applying Chernoff without independence.</b> <b>The "
          "commonest error by a wide margin, and the bound is simply "
          "false rather than merely loose</b> — so <b>check the "
          "assumption and name a fallback if it fails</b> (&sect;2's "
          "list).",
          "<b>Confusing the expectation with the tail.</b> <b>An "
          "expected-time bound is not a latency guarantee</b> "
          "(Module 01 &sect;4, CSCE 678 Module 06) — and this "
          "is the error most likely to reach production.",
          "<b>Union-bounding over too many events.</b> <b>If the "
          "per-event bound is 1/n and there are n events, you have proved "
          "nothing at all</b> — the bound is 1, which is true of "
          "every probability.",
          "<b>Using Chebyshev where Chernoff applied.</b> This gives a "
          "polynomial bound where an exponential one was available, which "
          "<b>makes a perfectly good algorithm look weak</b> — and "
          "it happens because the independence was available and "
          "unnoticed.",
          "<b>And reporting the bound rather than measuring the actual "
          "rate.</b> <b>Measure it, and compare against the bound</b> "
          "(Module 13 &sect;1) — the bound is usually loose, and "
          "reporting the measured rate alongside it is both more honest "
          "and more impressive. <b>The independence check is the one to "
          "make habitual:</b> write the assumption down before applying "
          "the bound, every time."]),
 ],
 "resources": [
   ("Mitzenmacher & Upfal &mdash; chapters 3–5",
    "https://www.cambridge.org/core/books/probability-and-computing/7D2016B2EB4B5E5F4F2C4E4F4F4C4E4F",
    "<b>The ladder, derived</b> — including the Markov-to-Chernoff "
    "derivation of &sect;1's callout."),
   ("Motwani & Raghavan &mdash; chapters 3–4",
    "https://www.cambridge.org/core/books/randomized-algorithms/6A3E5CD760413BEF7D0D01BFD5497ACB",
    "<b>The same material with more applications</b>, and the "
    "martingale treatment of &sect;2's fallbacks."),
   ("Boucheron, Lugosi & Massart &mdash; Concentration Inequalities",
    "https://academic.oup.com/book/26549",
    "<b>The comprehensive reference</b> — McDiarmid, Azuma, and "
    "everything beyond. Library copy; the authors' survey papers are "
    "free."),
   ("Dubhashi & Panconesi &mdash; Concentration of Measure for the "
    "Analysis of Randomised Algorithms",
    "https://www.cambridge.org/core/books/concentration-of-measure-for-the-analysis-of-randomized-algorithms/5BE6E5716E1B78D77A1C6ADA4D7948F8",
    "<b>&sect;2's negative association and martingale material</b>, "
    "aimed exactly at this course's needs. Library copy."),
 ],
 "exercises": [
   "<b>Derive Chebyshev from Markov</b> and Chernoff from Markov, "
   "showing the chosen function in each case.",
   "<b>Compare all three bounds numerically</b> for a sum of 1000 fair "
   "coin flips at several deviations.",
   "<b>Plot the three bounds and the true probability</b> on a log scale "
   "and report the gaps.",
   "<b>Apply Chernoff to dependent variables deliberately</b> and "
   "construct a case where it fails.",
   "<b>Find a negatively associated example</b> and confirm Chernoff "
   "still holds empirically.",
   "<b>Apply McDiarmid to a function that is not a sum</b>, and verify "
   "the bound.",
   "<b>Construct a union-bound argument</b> giving a "
   "1 − 1/n guarantee from a per-event 1/n² bound.",
   "<b>Construct one where the union bound exceeds 1</b> and say what you "
   "would need instead.",
   "<b>Amplify a 1/3-error algorithm</b> to below 10⁻¹⁵ and "
   "measure the empirical rate.",
   "<b>Measure the empirical failure rate of one algorithm</b> and "
   "compare against your derived bound.",
 ],
 "selfcheck": [
   "State all four inequalities and what each assumes.",
   "Derive Chebyshev and Chernoff from Markov.",
   "Why is the jump to exponential decay the important one?",
   "What does Chernoff require, and name four fallbacks.",
   "Give the standard union-bound pattern and why 1/n^c is the "
   "target.",
   "When is the union bound wasteful, and what replaces it?",
   "Give the six-row lookup table.",
   "Explain amplification for one-sided and two-sided error.",
   "Name the four common errors and the habit that prevents the first.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Balls and Bins",
 "subtitle": "The model behind hashing, load balancing, and caching.",
 "question": "If you throw n things into n places at random, what "
             "happens?",
 "outcomes": [
     "Derive the maximum load for n balls in n bins.",
     "Explain the birthday and coupon-collector results and their "
     "uses.",
     "Explain the power of two choices and why it is so effective.",
     "Apply the model to hashing and load balancing.",
     "Explain where the model's assumptions fail in practice.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The basic results",
   "blurb": "Three numbers worth knowing by heart."},

  {"t": "table", "kicker": "The results", "title": "n balls into n bins, and the numbers that follow",
   "header": ["Question", "Answer", "Used for"],
   "widths": [3.4, 3.4, 4.3],
   "rows": [
     ["<b>Maximum load</b>", "<b>Θ(log n / log log n)</b>", "<b>Worst-case hash chain length</b>"],
     ["<b>Empty bins</b>", "<b>About n/e ≈ 37%</b>", "<b>Hash table occupancy</b>"],
     ["<b>First collision</b>", "<b>After about √n balls</b>", "<b>Birthday attacks, hash sizing</b>"],
     ["<b>Balls to fill every bin</b>", "<b>About n ln n</b>", "<b>Coupon collector; cache warming</b>"],
     ["<b>Load with n log n balls</b>", "<b>Concentrated within O(√(log n))</b>", "<b>Why over-provisioning works</b>"],
   ],
   "footnote": "<b>The first and third are the ones to remember:</b> "
               "<b>maximum load is log n / log log n, and collisions "
               "start at √n</b> — and both are "
               "counterintuitive in the useful direction.",
   "note": "These five numbers answer most practical sizing questions."},

  {"t": "code", "kicker": "Maximum load", "title": "Why log n / log log n, in one derivation",
   "lang": "text", "code": """
  P(a specific bin gets >= k balls)
      <= C(n,k) * (1/n)^k        # choose which k balls
      <= (1/k!)                  # since C(n,k) <= n^k/k!
      <= (e/k)^k                 # Stirling

  UNION BOUND over n bins:
      P(any bin gets >= k) <= n * (e/k)^k

  We want this below 1/n, so we need (e/k)^k <= 1/n^2,
  i.e. k log(k/e) >= 2 log n.

  Setting k = c log n / log log n satisfies it for suitable
  c. So WITH HIGH PROBABILITY the maximum load is
  O(log n / log log n).

  AND A MATCHING LOWER BOUND holds, so the answer is tight.

  NOTE THE STRUCTURE: a per-bin bound, then a union bound
  over bins, designed so the per-bin probability is 1/n^2
  -- which is EXACTLY Module 02 Part 3's pattern. Almost
  every result in Modules 03 to 05 has this shape.
""",
   "caption": "<b>Per-event bound, then union bound, with the per-event "
              "target set at 1/n²</b> — learn the shape and "
              "most of these derivations become routine.",
   "note": "Emphasise the reusable shape over the specific answer."},

  {"t": "section", "label": "Part 2", "title": "The power of two choices",
   "blurb": "An exponential improvement from almost nothing."},

  {"t": "callout", "title": "Two random choices instead of one changes log n / log log n to log log n",
   "kind": "The most surprising result in the module",
   "body": ["<b>Pick <i>two</i> bins at random and put the ball in the "
            "less loaded one.</b> <b>The maximum load drops to "
            "log log n / log 2 + O(1).</b>",
            "<b>At n = one million, that is about 20 versus "
            "about 4</b> — <b>an exponential improvement from one "
            "extra random choice and one comparison.</b>",
            "<b>And three choices gives log log n / log 3, which is a "
            "constant-factor further improvement</b> — <b>so almost "
            "all the benefit is in the second choice.</b>",
            "<b>Which is why it is used everywhere:</b> <b>load "
            "balancers, distributed hash tables, cuckoo hashing, and work "
            "stealing all use two-choice selection</b>, and the reason is "
            "this theorem."]},

  {"t": "callout", "title": "Why two choices works, intuitively",
   "kind": "The mechanism",
   "body": ["<b>With one choice, a bin's load grows whenever it is "
            "picked</b> — so the load distribution's tail is governed "
            "by a simple Poisson-like process.",
            "<b>With two choices, a bin only grows if it is picked "
            "<i>and</i> is the lighter of two</b> — so a heavily "
            "loaded bin is very unlikely to grow further.",
            "<b>The effect compounds up the load distribution:</b> "
            "<b>the fraction of bins with load at least k+1 is roughly "
            "the square of the fraction with load at least k</b>, which "
            "gives doubly exponential decay.",
            "<b>And that squaring is where the second logarithm comes "
            "from</b> — <b>the number of levels before the fraction "
            "hits zero is log log n</b>, which is a satisfying "
            "derivation to have in mind rather than a formula to "
            "recall."]},

  {"t": "section", "label": "Part 3", "title": "Applications",
   "blurb": "Where you have already used this."},

  {"t": "bullets", "kicker": "Applications", "title": "The model in systems you have built",
   "items": [
     "<b>Hash table chain lengths.</b> <b>Maximum chain is "
     "log n / log log n with random hashing</b>, which is why a lookup "
     "is 'O(1)' with a caveat.",
     "",
     "<b>Birthday attacks.</b> <b>Collisions at √n means a "
     "128-bit hash gives 64 bits of collision resistance</b> "
     "(CSCE 711) — the single most consequential application of "
     "the model.",
     "",
     "<b>Cache warming and coupon collecting.</b> <b>n ln n accesses "
     "to touch n distinct items</b>, which sizes a warm-up period.",
     "",
     "<b>Load balancing.</b> <b>Two-choice selection, universally</b> "
     "(Module 11 §3, CSCE 678).",
     "",
     "<b>And sharding.</b> <b>The maximum-load result is why uniform "
     "hashing still produces hot shards</b>, and why consistent hashing "
     "uses virtual nodes.",
   ],
   "footnote": "<b>The virtual-node trick is the model applied "
               "deliberately:</b> many small bins per server concentrates "
               "the per-server load far better than one bin each."},

  {"t": "section", "label": "Part 4", "title": "Where the model fails",
   "blurb": "And the failures are the interesting part."},

  {"t": "callout", "title": "Real workloads are not uniform, and the model's predictions change",
   "kind": "The honest qualification",
   "body": ["<b>The analysis assumes balls are thrown uniformly and "
            "independently.</b> <b>Real keys are skewed</b> — Zipf "
            "distributed, in most systems — <b>so a few bins get a "
            "constant fraction of the traffic regardless of the hash.</b>",
            "<b>Which means the maximum-load result does not apply "
            "to hot keys</b>, and the response is different: "
            "replication, caching, or key splitting rather than better "
            "hashing.",
            "<b>And balls are frequently not independent:</b> "
            "<b>sequential keys, timestamps, and structured identifiers "
            "all correlate</b>, which a weak hash function will "
            "preserve.",
            "<b>So the practical procedure is:</b> <b>measure the "
            "actual load distribution rather than assuming the model, and "
            "use the model to tell you what <i>uniform</i> would have "
            "looked like</b> — which is the right baseline and not the "
            "prediction."]},

  {"t": "bullets", "kicker": "Practice", "title": "Using the model correctly",
   "items": [
     "<b>Use it as a baseline, not a prediction.</b> <b>'Uniform "
     "hashing would give a maximum load of 20; we observe 400' is a "
     "diagnosis.</b>",
     "",
     "<b>Over-provision by a log factor if you need concentration.</b> "
     "<b>n log n balls into n bins concentrates tightly</b>, which is "
     "why larger tables behave better than the ratio suggests.",
     "",
     "<b>Use two choices wherever the second choice is "
     "affordable</b> — which it almost always is.",
     "",
     "<b>And use many small bins rather than few large ones</b> when "
     "you control the mapping (virtual nodes).",
     "",
     "<b>Then measure the tail.</b> <b>The maximum load, not the "
     "mean, is what causes the incident</b> (CSCE 678 §06).",
   ],
   "footnote": "<b>'Measure the tail' is the recurring instruction</b> "
               "— and this module gives you the number the tail "
               "should be, which is what makes the measurement "
               "interpretable."},
 ],
 "takeaways": [
   "n balls in n bins gives maximum load Θ(log n / log log n), about "
   "37% empty bins, first collision at √n, and n ln n balls to fill "
   "every bin.",
   "The derivation is a per-bin bound plus a union bound with the per-bin "
   "target set at 1/n², which is the reusable shape for most of this "
   "course.",
   "Two random choices instead of one reduces maximum load to log log n "
   "— an exponential improvement from one extra choice and one "
   "comparison.",
   "The mechanism is that the fraction of bins at load k+1 is roughly the "
   "square of the fraction at load k, which gives the second logarithm.",
   "Collisions at √n is why a 128-bit hash gives 64 bits of collision "
   "resistance — the most consequential application of the model.",
   "Real workloads are skewed, so use the model as a baseline for what "
   "uniform would look like rather than as a prediction.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The basic results"),
  ("table", ["Question", "Answer", "What it is used for"],
   [["<b>Maximum load, n balls in n bins</b>",
     "<b>&Theta;(log n / log log n)</b>",
     "<b>Worst-case hash chain length</b>, and the caveat on 'O(1) "
     "lookup'."],
    ["<b>Number of empty bins</b>",
     "<b>About n/e, which is roughly 37%</b>",
     "<b>Hash table occupancy</b> — and why a table at load factor 1 "
     "wastes more than a third of its slots."],
    ["<b>When the first collision occurs</b>",
     "<b>After about &radic;n balls</b>",
     "<b>Birthday attacks and hash output sizing</b> "
     "(CSCE 711)."],
    ["<b>Balls needed to hit every bin</b>", "<b>About n ln n</b>",
     "<b>The coupon collector problem; cache warming periods; test "
     "coverage by random sampling.</b>"],
    ["<b>Maximum load with n log n balls</b>",
     "<b>Concentrated within O(&radic;(log n)) of the mean</b>",
     "<b>Why over-provisioning works</b> — see &sect;4."]],
   [0.28, 0.28, 0.44]),
  ("p", "<b>The first and third are the ones to remember:</b> "
        "<b>maximum load is log n / log log n, and collisions start at "
        "&radic;n</b> — <b>and both are counterintuitive in the "
        "useful direction.</b> The maximum load is larger than people "
        "expect (so hash tables have longer worst-case chains than the "
        "average suggests) and the collision point is much earlier than "
        "people expect (so hash outputs need twice the bits you would "
        "naively want)."),
  ("code", """P(a specific bin receives >= k balls)
    <= C(n,k) * (1/n)^k        # choose which k balls land
    <= 1/k!                    # since C(n,k) <= n^k / k!
    <= (e/k)^k                 # Stirling

UNION BOUND over the n bins:
    P(any bin receives >= k) <= n * (e/k)^k

We want this below 1/n, so we need (e/k)^k <= 1/n^2, i.e.
k * log(k/e) >= 2 log n.

Setting k = c log n / log log n satisfies that for a
suitable constant c. So WITH HIGH PROBABILITY the maximum
load is O(log n / log log n).

AND A MATCHING LOWER BOUND holds, so the answer is tight
rather than merely an upper bound.

NOTE THE STRUCTURE: a per-bin bound, then a union bound
over bins, with the per-bin probability deliberately driven
to 1/n^2 so that the union over n bins leaves 1/n.
That is EXACTLY Module 02 section 3's pattern -- and almost
every result in Modules 03 through 05 has this shape."""),

  ("h1", "2 &nbsp; The power of two choices"),
  ("callout", "Two random choices instead of one changes log n / log log n "
              "to log log n",
   ["<b>Pick <i>two</i> bins uniformly at random and put the ball in "
    "whichever is currently less loaded.</b> <b>The maximum load drops "
    "to log log n / log 2 + O(1).</b>",
    "<b>At n = one million, that is about 20 against about 4</b> "
    "— <b>an exponential improvement obtained from one extra random "
    "choice and one comparison per insertion.</b> It is one of the best "
    "cost-benefit ratios in algorithms.",
    "<b>And d = 3 choices gives log log n / log 3, which is a "
    "constant-factor further improvement</b> — <b>so almost all the "
    "benefit is in the second choice</b>, and there is little reason to go "
    "beyond two or three.",
    "<b>Which is why it is used everywhere:</b> <b>load balancers, "
    "distributed hash tables, cuckoo hashing, work-stealing schedulers, "
    "and connection pools all use two-choice selection</b> "
    "(Module 11 &sect;3, CSCE 678), <b>and this theorem is the "
    "reason</b> rather than folklore."]),
  ("callout", "Why two choices works, intuitively",
   ["<b>With one choice, a bin's load grows whenever it happens to be "
    "picked</b> — so the load distribution's tail is governed by a "
    "straightforward Poisson-like process, with the tail decaying only as "
    "fast as factorials.",
    "<b>With two choices, a bin grows only if it is picked <i>and</i> is "
    "the lighter of the two</b> — so <b>a heavily loaded bin is "
    "very unlikely to grow further</b>, because its partner will usually "
    "be lighter.",
    "<b>The effect compounds up the load distribution:</b> <b>the "
    "fraction of bins with load at least k+1 is roughly the <i>square</i> "
    "of the fraction with load at least k</b>, because the ball must hit "
    "two bins both already at load k. <b>Which gives doubly exponential "
    "decay in k.</b>",
    "<b>And that squaring is exactly where the second logarithm comes "
    "from</b> — <b>the number of squarings needed to drive a "
    "fraction from 1/2 down below 1/n is log log n</b>. <b>Which is a "
    "satisfying derivation to carry rather than a formula to "
    "recall</b>, and it also tells you immediately that d choices gives "
    "log log n / log d."]),

  ("break",),
  ("h1", "3 &nbsp; Applications"),
  ("ul", ["<b>Hash table chain lengths.</b> <b>The maximum chain is "
          "&Theta;(log n / log log n) with random hashing</b>, which is "
          "<b>why a hash lookup is described as O(1) with a caveat</b> "
          "— the average is constant and the worst case over n "
          "lookups is not.",
          "<b>Birthday attacks.</b> <b>Collisions beginning at &radic;n "
          "means a 128-bit hash provides only 64 bits of collision "
          "resistance</b> (CSCE 711) — <b>which is the single "
          "most consequential application of this model</b>, and is why "
          "hash output sizes are doubled relative to the security level "
          "wanted.",
          "<b>Cache warming and the coupon collector.</b> <b>About "
          "n ln n random accesses are needed to touch n distinct "
          "items</b>, which sizes a warm-up period or a random-sampling "
          "test campaign — and the ln n factor is frequently "
          "forgotten.",
          "<b>Load balancing.</b> <b>Two-choice selection, "
          "essentially universally</b>, in software load balancers and in "
          "distributed task queues (Module 11 &sect;3).",
          "<b>And sharding.</b> <b>The maximum-load result is why "
          "uniform hashing still produces hot shards</b>, and <b>why "
          "consistent hashing implementations use many virtual nodes per "
          "physical server</b> — which is the model applied "
          "deliberately: <b>many small bins per server concentrates the "
          "per-server total far better than one bin each</b>, by the "
          "n log n row of &sect;1's table."]),

  ("h1", "4 &nbsp; Where the model fails"),
  ("callout", "Real workloads are not uniform, and the model's predictions "
              "change",
   ["<b>The analysis assumes balls are thrown uniformly and "
    "independently.</b> <b>Real keys are skewed</b> — Zipf "
    "distributed, in most systems with human-generated traffic — "
    "<b>so a few bins receive a constant fraction of the traffic "
    "regardless of how good the hash function is.</b>",
    "<b>Which means the maximum-load result simply does not apply to hot "
    "keys</b>, and <b>the engineering response is correspondingly "
    "different: replication, caching in front, or splitting the key</b> "
    "— not a better hash function, which cannot help.",
    "<b>And the balls are frequently not independent either:</b> "
    "<b>sequential identifiers, timestamps, and structured keys all "
    "correlate</b>, and <b>a weak hash function will preserve the "
    "correlation</b> rather than destroy it — which is a real cause "
    "of unexpected clustering.",
    "<b>So the practical procedure is:</b> <b>measure the actual load "
    "distribution rather than assuming the model, and use the model to "
    "tell you what <i>uniform</i> would have looked like</b> — "
    "<b>which is the right use of it: a baseline for comparison rather "
    "than a prediction.</b> <b>'Uniform would give 20 and we observe "
    "400' is a diagnosis</b>, and it is a far more useful output than "
    "either number alone."]),
  ("ul", ["<b>Use it as a baseline, not a prediction.</b> <b>'Uniform "
          "hashing would give a maximum load of 20; we observe 400' is a "
          "diagnosis</b> that points at key skew or a bad hash.",
          "<b>Over-provision by a logarithmic factor if you need "
          "concentration.</b> <b>n log n balls into n bins concentrates "
          "tightly</b> (&sect;1's last row) — <b>which is why larger "
          "hash tables behave better than the load-factor ratio "
          "suggests</b>, and is an argument for more shards rather than "
          "bigger ones.",
          "<b>Use two choices wherever the second choice is "
          "affordable</b> — <b>which it almost always is</b>, since "
          "it costs one extra lookup and one comparison for an exponential "
          "improvement in the tail.",
          "<b>And use many small bins rather than few large ones</b> "
          "when you control the mapping — the virtual-node trick, "
          "which is the same over-provisioning argument applied to the "
          "bin count instead of the ball count.",
          "<b>Then measure the tail.</b> <b>The maximum load, not the "
          "mean, is what causes the incident</b> (CSCE 678 "
          "Module 06) — <b>and 'measure the tail' is the recurring "
          "instruction of this program.</b> <b>What this module adds is "
          "the number the tail <i>should</i> be</b>, which is what makes "
          "the measurement interpretable rather than merely a "
          "number."]),
 ],
 "resources": [
   ("Mitzenmacher & Upfal &mdash; chapters 5 and 14",
    "https://www.cambridge.org/core/books/probability-and-computing/7D2016B2EB4B5E5F4F2C4E4F4F4C4E4F",
    "<b>Balls and bins, the Poisson approximation, and the power of two "
    "choices</b> — the reference for this module."),
   ("Azar, Broder, Karlin & Upfal &mdash; Balanced Allocations (free)",
    "https://dl.acm.org/doi/10.1145/225058.225143",
    "<b>&sect;2's result, in the original</b> — the paper that "
    "introduced the power of two choices."),
   ("Mitzenmacher &mdash; The Power of Two Choices: A Survey (free)",
    "https://www.eecs.harvard.edu/~michaelm/postscripts/handbook2001.pdf",
    "<b>&sect;2 and &sect;3, surveyed</b> — including the "
    "applications and the variants."),
   ("Karger, Lehman et al. &mdash; Consistent Hashing (free)",
    "https://dl.acm.org/doi/10.1145/258533.258660",
    "<b>&sect;3's last row</b>, and the virtual-node technique in its "
    "original setting."),
 ],
 "exercises": [
   "<b>Simulate n balls into n bins</b> for n up to 10⁶ and plot the "
   "maximum load against log n / log log n.",
   "<b>Measure the fraction of empty bins</b> and compare against "
   "1/e.",
   "<b>Find the first collision empirically</b> for several n and confirm "
   "the √n scaling.",
   "<b>Measure the coupon-collector time</b> and compare against "
   "n ln n.",
   "<b>Implement two-choice allocation</b> and plot its maximum load "
   "against one-choice on the same axes.",
   "<b>Confirm the log log n scaling</b> and the diminishing return at "
   "d = 3.",
   "<b>Verify the squaring intuition</b> by measuring the fraction of "
   "bins at each load level.",
   "<b>Throw Zipf-distributed balls</b> and report how the maximum load "
   "changes.",
   "<b>Use a weak hash on sequential keys</b> and observe the "
   "clustering.",
   "<b>Implement virtual nodes</b> and measure the per-server load "
   "concentration against one bin per server.",
 ],
 "selfcheck": [
   "Give the five numbers for n balls in n bins.",
   "Which two matter most, and why are both counterintuitive?",
   "Derive the maximum load bound and name the reusable shape.",
   "State the power of two choices and the improvement at "
   "n = 10⁶.",
   "Explain the squaring intuition and where log log n comes from.",
   "Why does a 128-bit hash give 64 bits of collision resistance?",
   "Name five applications of the model.",
   "Where does the model fail, and what is the correct response to hot "
   "keys?",
   "Give five practical rules for using the model.",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Randomised Data Structures",
 "subtitle": "Expected balance instead of enforced balance.",
 "question": "Why would you choose a structure that is only probably "
             "balanced?",
 "outcomes": [
     "Explain skip lists and derive their expected height.",
     "Explain treaps and their relationship to quicksort.",
     "Explain universal hashing and what it guarantees.",
     "Explain perfect and cuckoo hashing.",
     "Compare randomised against deterministic balancing honestly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Skip lists",
   "blurb": "A balanced structure with no balancing code."},

  {"t": "code", "kicker": "Skip lists", "title": "The whole structure, and its analysis",
   "lang": "text", "code": """
  A sorted linked list, plus express lanes.
  Each element appears at level i with probability 1/2^i --
  flip a coin on insertion until it comes up tails.

  SEARCH: start at the top level, move right while the next
  key is smaller, drop down when it is not. Repeat.

  EXPECTED HEIGHT: O(log n). The probability any element
  reaches level c log n is n * 2^-(c log n) = n^(1-c),
  which is small for c > 1.
      -- Module 02's per-event-plus-union pattern again.

  EXPECTED SEARCH TIME: O(log n). At each level you move
  right an expected constant number of steps before
  dropping, and there are O(log n) levels.

  WHY IT IS USED: there is NO REBALANCING CODE. No
  rotations, no colour invariants, no case analysis. The
  insert is: find the position, flip coins, splice in.
  Twenty lines against a red-black tree's two hundred.

  AND IT IS EASIER TO MAKE CONCURRENT, because there is no
  global rebalancing step to lock -- which is why
  concurrent skip lists are common and concurrent balanced
  trees are hard (CSCE 611, CSCE 678).
""",
   "caption": "<b>The absence of rebalancing code is the actual "
              "benefit</b> — and the concurrency consequence is why "
              "it shows up in real systems.",
   "note": "The concurrency point is the one practitioners care about."},

  {"t": "callout", "title": "Treaps: a binary search tree whose shape is a random quicksort",
   "kind": "The structure, and the connection",
   "body": ["<b>Each node carries a key and a random priority.</b> "
            "<b>The tree is a search tree on keys and a heap on "
            "priorities</b>, which determines the shape uniquely.",
            "<b>And that shape is exactly the recursion tree of "
            "quicksort with random pivots</b> — the highest priority "
            "is the root, which is the first pivot.",
            "<b>So the expected depth is O(log n) by the same analysis "
            "as randomised quicksort</b>, and the analysis transfers "
            "without modification.",
            "<b>Which is a satisfying unification:</b> <b>skip lists, "
            "treaps, and randomised quicksort are three presentations of "
            "one analysis</b>, and recognising that is worth more than "
            "learning three."]},

  {"t": "section", "label": "Part 2", "title": "Hashing",
   "blurb": "What a random hash function actually buys."},

  {"t": "callout", "title": "Universal hashing: a family where any two keys collide with probability 1/m",
   "kind": "The right definition",
   "body": ["<b>A family H is universal if, for any two distinct keys, "
            "a randomly chosen h ∈ H collides on them with "
            "probability at most 1/m.</b>",
            "<b>That is all you need for the expected-chain-length "
            "analysis</b> — <b>the full independence of a random "
            "function is not required, which is what makes a small, "
            "efficiently computable family sufficient.</b>",
            "<b>And the family can be tiny:</b> "
            "<b>h(x) = ((ax+b) mod p) mod m</b> over a prime p is "
            "universal, with a and b the only randomness.",
            "<b>Which is Module 12's limited-independence idea arriving "
            "early</b> — <b>you need pairwise independence, not full "
            "independence, and pairwise is cheap.</b>"]},

  {"t": "table", "kicker": "Hashing", "title": "The hashing schemes and what each guarantees",
   "header": ["Scheme", "Guarantee", "Cost"],
   "widths": [2.7, 4.3, 5.0],
   "rows": [
     ["<b>Universal, chaining</b>", "<b>O(1) expected lookup</b>", "<b>Worst case log n / log log n (M03)</b>"],
     ["<b>Perfect hashing</b>", "<b>O(1) WORST CASE lookup</b>", "<b>Static set only; randomised construction</b>"],
     ["<b>Cuckoo hashing</b>", "<b>O(1) worst case lookup; dynamic</b>", "<b>Insertion may rehash; load factor under ~0.5</b>"],
     ["<b>Linear probing</b>", "<b>Excellent cache behaviour</b>", "<b>Needs 5-independence for the analysis</b>"],
     ["<b>Bloom filter</b>", "<b>O(1), one-sided error</b>", "<b>No deletion; false positives only</b>"],
   ],
   "footnote": "<b>Perfect and cuckoo hashing give worst-case O(1) "
               "lookup</b>, which chaining does not — and both "
               "achieve it by using randomness in the <i>construction</i> "
               "rather than in the query.",
   "note": "The construction-versus-query distinction is the useful "
           "insight."},

  {"t": "section", "label": "Part 3", "title": "Cuckoo hashing",
   "blurb": "Two choices, applied to hashing."},

  {"t": "callout", "title": "Cuckoo hashing gives worst-case constant lookup by moving the work to insertion",
   "kind": "The trade",
   "body": ["<b>Each key has two possible positions, from two hash "
            "functions. A lookup checks both</b> — <b>so lookup is "
            "worst-case two probes, always.</b>",
            "<b>Insertion places the key in one position, evicting "
            "whatever was there, which is then reinserted in its "
            "alternative position</b> — possibly cascading.",
            "<b>The cascade terminates with high probability below a "
            "load factor of about 0.5</b>, and above it the structure "
            "must be rebuilt with new hash functions.",
            "<b>So the randomness has moved from the query to the "
            "construction</b> — <b>which is the right place for it "
            "when reads vastly outnumber writes</b>, and is the same "
            "reasoning as perfect hashing. <b>And it is Module 03's two "
            "choices, applied.</b>"]},

  {"t": "section", "label": "Part 4", "title": "The honest comparison",
   "blurb": "Against deterministic structures."},

  {"t": "table", "kicker": "Comparison", "title": "Randomised against deterministic balancing",
   "header": ["", "Randomised (skip list, treap)", "Deterministic (red-black, B-tree)"],
   "widths": [2.1, 4.4, 5.5],
   "rows": [
     ["<b>Guarantee</b>", "<b>Expected, with a tail bound</b>", "<b>Worst case</b>"],
     ["<b>Code size</b>", "<b>Much smaller. No rebalancing</b>", "<b>Large case analysis</b>"],
     ["<b>Concurrency</b>", "<b>Easier — no global rebalance</b>", "<b>Hard</b>"],
     ["<b>Cache behaviour</b>", "<b>Worse — pointer chasing</b>", "<b>B-trees are far better</b>"],
     ["<b>Adversary</b>", "<b>Safe if the randomness is hidden</b>", "<b>Safe always</b>"],
     ["<b>In practice</b>", "<b>Skip lists in concurrent maps</b>", "<b>B-trees in every database</b>"],
   ],
   "footnote": "<b>The cache row is why B-trees dominate storage and "
               "skip lists do not</b> — the asymptotics are the same "
               "and the constants are not (CSCE 637 §01).",
   "note": "Being honest that deterministic structures often win is "
           "important."},

  {"t": "callout", "title": "Which to choose",
   "kind": "The practical answer",
   "body": ["<b>Concurrent in-memory ordered map: skip list.</b> <b>The "
            "absence of global rebalancing is decisive</b>, and it is why "
            "concurrent skip lists are in standard libraries.",
            "<b>On-disk or cache-sensitive ordered structure: "
            "B-tree.</b> <b>Node-per-block locality beats "
            "everything</b>, and the asymptotics do not distinguish "
            "them.",
            "<b>Static set, worst-case lookup needed: perfect "
            "hashing.</b> <b>Dynamic with the same requirement: "
            "cuckoo.</b>",
            "<b>And for a sketch or a teaching implementation: the "
            "randomised one, always</b> — <b>twenty lines that you can "
            "verify beats two hundred that you cannot.</b>"]},
 ],
 "takeaways": [
   "A skip list's benefit is the absence of rebalancing code, and the "
   "consequence is that it is far easier to make concurrent.",
   "A treap's shape is exactly randomised quicksort's recursion tree, so "
   "skip lists, treaps, and quicksort share one analysis.",
   "Universal hashing needs only pairwise collision probability 1/m, not "
   "full independence — so a tiny family suffices.",
   "Perfect and cuckoo hashing achieve worst-case O(1) lookup by putting "
   "the randomness in the construction rather than the query.",
   "Cuckoo hashing is the power of two choices applied to hashing, and it "
   "terminates below a load factor of about 0.5.",
   "B-trees beat skip lists on cache and disk behaviour despite identical "
   "asymptotics, which is why databases use them.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Skip lists and treaps"),
  ("code", """A sorted linked list, plus express lanes above it.
Each element appears at level i with probability 1/2^i --
flip a coin on insertion until it comes up tails.

SEARCH: start at the top level, move right while the next
key is smaller than the target, drop down a level when it
is not. Repeat until the bottom.

EXPECTED HEIGHT: O(log n). The probability that any element
reaches level c log n is n * 2^-(c log n) = n^(1-c), which
is small for c > 1.
    -- Module 02's per-event-plus-union-bound pattern, for
       the third time.

EXPECTED SEARCH TIME: O(log n). At each level you move
right an expected constant number of steps before dropping,
and there are O(log n) levels.

WHY IT IS ACTUALLY USED: there is NO REBALANCING CODE. No
rotations, no colour invariants, no case analysis on
uncle nodes. Insertion is: find the position, flip coins,
splice in. Twenty lines against a red-black tree's two
hundred.

AND IT IS FAR EASIER TO MAKE CONCURRENT, because there is
no global rebalancing step that must be locked -- which is
why concurrent skip lists appear in standard libraries and
concurrent balanced trees are a research topic
(CSCE 611, CSCE 678)."""),
  ("callout", "Treaps: a binary search tree whose shape is a random "
              "quicksort",
   ["<b>Each node carries a key and a randomly assigned priority.</b> "
    "<b>The structure is a binary search tree with respect to the keys "
    "and a heap with respect to the priorities</b> — and those two "
    "constraints together determine the shape uniquely, given the "
    "priorities.",
    "<b>And that shape is exactly the recursion tree of quicksort with "
    "random pivots</b>: the highest-priority element is the root, which "
    "is the element quicksort would have chosen as its first pivot, and "
    "the recursion proceeds identically.",
    "<b>So the expected depth is O(log n) by precisely the same analysis "
    "as randomised quicksort</b> (CSCE 629), and <b>the analysis "
    "transfers without any modification</b> — you do not need a new "
    "argument.",
    "<b>Which is a satisfying unification:</b> <b>skip lists, treaps, "
    "and randomised quicksort are three presentations of one "
    "analysis</b>, and <b>recognising that is worth considerably more "
    "than learning the three separately</b> — it is the same "
    "level-by-level or depth-by-depth argument in three costumes."]),

  ("h1", "2 &nbsp; Hashing"),
  ("callout", "Universal hashing: a family where any two keys collide with "
              "probability 1/m",
   ["<b>A family H of hash functions into m buckets is <i>universal</i> "
    "if, for any two distinct keys, a uniformly chosen h from H collides "
    "on them with probability at most 1/m.</b>",
    "<b>That is all you need for the expected-chain-length analysis.</b> "
    "<b>The full independence of a truly random function is not "
    "required</b> — the analysis only ever considers pairs — "
    "<b>which is what makes a small, efficiently computable, "
    "explicitly storable family sufficient.</b>",
    "<b>And the family can be tiny:</b> <b>h(x) = ((ax + b) mod p) "
    "mod m</b> for a prime p larger than the key range is universal, "
    "<b>with a and b being the only randomness</b> — two numbers, "
    "rather than a table of n random values.",
    "<b>Which is Module 12's limited-independence idea arriving "
    "early</b> — <b>you need pairwise independence rather than full "
    "independence, and pairwise independence is cheap to obtain and cheap "
    "to store.</b> <b>That observation is the whole reason hashing "
    "works in practice</b>, since a truly random function cannot be "
    "stored."]),
  ("table", ["Scheme", "What it guarantees", "What it costs"],
   [["<b>Universal hashing with chaining</b>",
     "<b>O(1) <i>expected</i> lookup.</b>",
     "<b>Worst-case chain of log n / log log n</b> (Module 03 "
     "&sect;1), so the tail is not constant."],
    ["<b>Perfect hashing (FKS)</b>",
     "<b>O(1) <i>worst-case</i> lookup.</b>",
     "<b>Static key set only</b>, and the construction is randomised "
     "(Las Vegas — retry until it succeeds)."],
    ["<b>Cuckoo hashing</b>",
     "<b>O(1) worst-case lookup, and the set may be dynamic.</b>",
     "<b>Insertion may cascade and may require a full rehash; the load "
     "factor must stay below about 0.5</b> for two choices (&sect;3)."],
    ["<b>Linear probing</b>",
     "<b>Excellent cache behaviour — the fastest in practice for "
     "many workloads.</b>",
     "<b>The analysis needs 5-wise independence</b>, which was only "
     "established relatively recently and is why its theoretical status "
     "lagged its practical use."],
    ["<b>Bloom filter</b>",
     "<b>O(1) membership test with one-sided error.</b>",
     "<b>No deletion; false positives only and never false "
     "negatives</b> — which is what makes it usable as a pre-filter "
     "(Module 01 &sect;2)."]],
   [0.22, 0.34, 0.44]),
  ("p", "<b>Perfect and cuckoo hashing give worst-case O(1) lookup, which "
        "chaining does not</b> — and <b>both achieve it by using the "
        "randomness in the <i>construction</i> rather than in the "
        "<i>query</i>.</b> <b>That construction-versus-query distinction "
        "is the useful insight here</b>, and it generalises: when reads "
        "vastly outnumber writes, moving the probabilistic work to build "
        "time converts an expected guarantee into a worst-case one."),

  ("break",),
  ("h1", "3 &nbsp; Cuckoo hashing"),
  ("callout", "Cuckoo hashing gives worst-case constant lookup by moving "
              "the work to insertion",
   ["<b>Each key has exactly two possible positions, given by two hash "
    "functions. A lookup checks both.</b> <b>So lookup is worst-case two "
    "probes, always</b> — no chains, no probing sequences, no tail.",
    "<b>Insertion places the key in one of its two positions, evicting "
    "whatever occupant was there; the evicted key is then placed in its "
    "own alternative position, evicting in turn</b> — possibly "
    "cascading for some distance, hence the name.",
    "<b>The cascade terminates with high probability as long as the load "
    "factor stays below about 0.5 for two hash functions</b> (higher for "
    "more functions or for buckets holding several items), <b>and above "
    "that threshold the structure must be rebuilt with fresh hash "
    "functions.</b>",
    "<b>So the randomness has moved from the query to the "
    "construction</b> — <b>which is the right place for it when "
    "reads vastly outnumber writes</b>, and is the same reasoning as "
    "perfect hashing. <b>And the two-position structure is "
    "Module 03's power of two choices, applied to hashing</b>: the "
    "insertion is choosing the better of two locations, and the "
    "exponential improvement in the load tail is what makes the scheme "
    "work."]),

  ("h1", "4 &nbsp; The honest comparison"),
  ("table", ["", "Randomised (skip list, treap)",
             "Deterministic (red-black, B-tree)"],
   [["<b>Guarantee</b>", "<b>Expected, with a tail bound.</b>",
     "<b>Worst case.</b>"],
    ["<b>Code size</b>",
     "<b>Much smaller — no rebalancing logic at all.</b>",
     "<b>Large case analysis</b>, and a frequent source of bugs."],
    ["<b>Concurrency</b>",
     "<b>Easier — no global rebalancing step to serialise.</b>",
     "<b>Hard</b>, and lock-free variants are genuinely research-level."],
    ["<b>Cache and disk behaviour</b>",
     "<b>Worse — pointer chasing with poor locality.</b>",
     "<b>B-trees are far better</b>, because a node is sized to a cache "
     "line or a disk block."],
    ["<b>Adversarial safety</b>",
     "<b>Safe provided the randomness is hidden from the adversary</b> "
     "(Module 01 &sect;1).",
     "<b>Safe always</b>, since there is nothing to learn."],
    ["<b>What ships</b>",
     "<b>Skip lists in concurrent ordered maps.</b>",
     "<b>B-trees in every database and filesystem.</b>"]],
   [0.15, 0.40, 0.45]),
  ("p", "<b>The cache row is why B-trees dominate storage and skip lists "
        "do not</b> — <b>the asymptotics are identical and the "
        "constants are not</b>, which is exactly CSCE 637 "
        "Module 01 &sect;4's point about what asymptotic analysis hides. "
        "<b>Being honest that the deterministic structure frequently wins "
        "is important</b>, because a course on randomised algorithms has "
        "an obvious bias to resist."),
  ("callout", "Which to choose",
   ["<b>A concurrent in-memory ordered map: skip list.</b> <b>The "
    "absence of global rebalancing is decisive</b>, and it is why "
    "concurrent skip lists appear in standard libraries while concurrent "
    "balanced trees generally do not.",
    "<b>An on-disk or cache-sensitive ordered structure: B-tree.</b> "
    "<b>Node-per-block locality beats everything else</b>, and the "
    "asymptotics do not distinguish the candidates at all.",
    "<b>A static set needing worst-case lookup: perfect hashing.</b> "
    "<b>Dynamic with the same requirement: cuckoo hashing</b> "
    "(&sect;3).",
    "<b>And for a sketch, a prototype, or a teaching "
    "implementation: the randomised one, always</b> — <b>twenty "
    "lines that you can read and verify beats two hundred that you "
    "cannot</b>, and the expected guarantee is almost certainly adequate "
    "for a prototype. <b>Which is Module 01 &sect;1's second use of "
    "randomness, and it is the one most often undervalued.</b>"]),
 ],
 "resources": [
   ("Pugh &mdash; Skip Lists: A Probabilistic Alternative to Balanced "
    "Trees (free)",
    "https://www.epaperpress.com/sortsearch/download/skiplist.pdf",
    "<b>&sect;1's structure, in the original</b> — short, and the "
    "argument for the code-size benefit is made explicitly."),
   ("Seidel & Aragon &mdash; Randomized Search Trees (free)",
    "https://link.springer.com/article/10.1007/BF01940876",
    "<b>&sect;1's treaps</b>, including the quicksort correspondence."),
   ("Carter & Wegman &mdash; Universal Classes of Hash Functions "
    "(free)",
    "https://www.sciencedirect.com/science/article/pii/0022000079900448",
    "<b>&sect;2's definition</b>, and the construction that made hashing "
    "analysable."),
   ("Pagh & Rodler &mdash; Cuckoo Hashing (free)",
    "https://web.archive.org/web/20240918112948/https://www.itu.dk/people/pagh/papers/cuckoo-jour.pdf",
    "<b>&sect;3's scheme</b>, with the load-factor threshold derived."),
 ],
 "exercises": [
   "<b>Implement a skip list</b> and measure its height distribution "
   "against the predicted O(log n).",
   "<b>Count the lines</b> against a red-black tree implementation.",
   "<b>Implement a treap</b> and verify its shape matches a randomised "
   "quicksort recursion tree on the same input.",
   "<b>Implement universal hashing</b> with the ((ax+b) mod p) mod m "
   "family and measure collision rates.",
   "<b>Verify the 1/m pairwise collision bound</b> empirically.",
   "<b>Implement perfect hashing</b> for a static set and measure the "
   "construction retries.",
   "<b>Implement cuckoo hashing</b> and plot the insertion cascade length "
   "against the load factor.",
   "<b>Find the threshold empirically</b> and compare against 0.5.",
   "<b>Benchmark a skip list against a B-tree</b> on a large dataset and "
   "report the cache-miss rates.",
   "<b>Make a skip list concurrent</b> and then attempt the same for a "
   "red-black tree. Report the difference in effort.",
 ],
 "selfcheck": [
   "Describe a skip list and derive its expected height.",
   "What is its actual benefit, and what follows for concurrency?",
   "What determines a treap's shape, and what is it equal to?",
   "Define universal hashing and say what it does not require.",
   "Why can the family be tiny?",
   "Compare five hashing schemes and their guarantees.",
   "What distinction do perfect and cuckoo hashing share?",
   "Explain cuckoo hashing and its load threshold.",
   "Compare randomised against deterministic balancing on six axes.",
   "Why do B-trees dominate storage?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Sketches and Streams",
 "subtitle": "Answers from data you cannot store.",
 "question": "What can you compute in one pass with sublinear memory?",
 "outcomes": [
     "Explain the streaming model and its constraints.",
     "Implement and analyse a count-min sketch.",
     "Explain HyperLogLog and distinct counting.",
     "Explain reservoir sampling and its correctness.",
     "Choose a sketch for a problem and state its error bound.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The model",
   "blurb": "One pass, sublinear memory, approximate answer."},

  {"t": "callout", "title": "The streaming model, and what it forces",
   "kind": "The constraints",
   "body": ["<b>Items arrive one at a time, you may not store them, "
            "and memory is polylogarithmic in the stream length.</b>",
            "<b>Which forces approximation.</b> <b>Exact distinct "
            "counting provably requires linear space</b>, so every "
            "sublinear answer is approximate — and the model's value "
            "is that <b>the approximation comes with a bound.</b>",
            "<b>And the guarantees are (ε, δ):</b> "
            "<b>within a relative error ε with probability at "
            "least 1 − δ</b>, with the memory depending on "
            "both.",
            "<b>So the design question is always the same:</b> <b>how "
            "much memory for what accuracy at what confidence</b> "
            "— and all three are tunable, which is what makes "
            "sketches engineering tools rather than curiosities."]},

  {"t": "table", "kicker": "Sketches", "title": "The sketches worth knowing",
   "header": ["Sketch", "Answers", "Memory"],
   "widths": [2.6, 4.3, 5.1],
   "rows": [
     ["<b>Count-min</b>", "<b>Item frequencies; heavy hitters</b>", "<b>O((1/ε) log(1/δ))</b>"],
     ["<b>HyperLogLog</b>", "<b>Distinct count</b>", "<b>About 1.5 KB for 2% error at any scale</b>"],
     ["<b>Bloom filter</b>", "<b>Membership, one-sided</b>", "<b>About 10 bits per item at 1% error</b>"],
     ["<b>AMS / tug-of-war</b>", "<b>Second moment, self-join size</b>", "<b>O((1/ε²) log(1/δ))</b>"],
     ["<b>Reservoir sample</b>", "<b>A uniform sample of size k</b>", "<b>O(k) — exact, not approximate</b>"],
     ["<b>t-digest, KLL</b>", "<b>Quantiles</b>", "<b>O((1/ε) log) — the practical choice</b>"],
   ],
   "footnote": "<b>HyperLogLog's memory is independent of the "
               "cardinality</b>, which is the result that makes distinct "
               "counting at scale possible at all — 1.5 KB whether "
               "you have a thousand items or a billion.",
   "note": "The scale-independence of HLL is what makes people adopt "
           "it."},

  {"t": "section", "label": "Part 2", "title": "Count-min",
   "blurb": "The sketch to understand properly."},

  {"t": "code", "kicker": "Count-min", "title": "The structure, the analysis, and the one-sided error",
   "lang": "text", "code": """
  A d x w table of counters, and d independent hash
  functions.

  UPDATE(x, c):  for each row i, add c to
                     table[i][h_i(x)]
  QUERY(x):      return the MINIMUM over rows of
                     table[i][h_i(x)]

  WHY THE MINIMUM: each cell holds x's true count PLUS the
  counts of everything else hashing there. So every row
  OVERESTIMATES, and the minimum is the least bad
  overestimate.
      -> ONE-SIDED ERROR. The answer is never too small.

  THE BOUND: with w = e/eps and d = ln(1/delta),
      estimate <= true + eps * (total stream weight)
  with probability at least 1 - delta.

  NOTE WHAT THE ERROR IS RELATIVE TO: the TOTAL weight, not
  x's own count. So count-min is excellent for HEAVY
  HITTERS and useless for rare items -- a item with count 3
  in a stream of weight 10^9 will have an estimate
  dominated by noise.

  WHICH IS THE QUESTION TO ASK OF ANY SKETCH: the error is
  relative to WHAT?
""",
   "caption": "<b>'Relative to what?' is the question</b> — and "
              "count-min's error being relative to the total weight is "
              "exactly why it is a heavy-hitter sketch.",
   "note": "The relative-to-what question is the most useful habit "
           "here."},

  {"t": "section", "label": "Part 3", "title": "Distinct counting",
   "blurb": "The cleverest idea in the module."},

  {"t": "callout", "title": "HyperLogLog counts distinct items by looking at leading zeros",
   "kind": "The idea",
   "body": ["<b>Hash each item and record the maximum number of leading "
            "zeros seen.</b> <b>If you have seen k leading zeros, you "
            "have probably seen about 2ᵏ distinct items</b> "
            "— because that pattern has probability "
            "2⁻ᵏ.",
            "<b>And duplicates do not affect it</b>, because hashing is "
            "deterministic — <b>which is what makes it a distinct "
            "counter rather than a counter.</b>",
            "<b>One such estimate is extremely noisy, so use many "
            "registers</b> — bucket by the first few hash bits and "
            "take a harmonic mean of the per-bucket estimates.",
            "<b>Giving about 2% error from 1.5 KB, at any "
            "cardinality</b> — <b>and the memory is independent of "
            "the count, because it stores an exponent rather than a "
            "number.</b>"]},

  {"t": "callout", "title": "Reservoir sampling, which is exact",
   "kind": "The one that is not approximate",
   "body": ["<b>To keep a uniform sample of k items from a stream of "
            "unknown length:</b> keep the first k, then for the "
            "n-th item replace a random reservoir slot with "
            "probability k/n.",
            "<b>The result is exactly uniform</b> — a short "
            "induction shows every item has probability k/n of being in "
            "the reservoir after n items.",
            "<b>So this is not a sketch in the approximate sense:</b> "
            "<b>the sample is exactly correct, and only the choice of "
            "which items is random.</b>",
            "<b>Which makes it the most broadly useful tool in the "
            "module</b> — <b>a uniform sample lets you compute anything "
            "approximately</b>, rather than answering one specific "
            "question."]},

  {"t": "section", "label": "Part 4", "title": "Choosing and using",
   "blurb": "The practical questions."},

  {"t": "bullets", "kicker": "Practice", "title": "Using a sketch correctly",
   "items": [
     "<b>Ask what the error is relative to.</b> <b>Count-min's error "
     "is relative to the total weight; HLL's is relative to the "
     "cardinality</b> — completely different guarantees.",
     "",
     "<b>Check mergeability.</b> <b>Count-min, HLL, and Bloom filters "
     "all merge</b>, which is what makes them usable in a distributed "
     "aggregation (CSCE 678 §04).",
     "",
     "<b>Check the error direction.</b> <b>Count-min overestimates "
     "and never underestimates</b>, which matters when you threshold on "
     "the result.",
     "",
     "<b>Measure the achieved error against the bound.</b> <b>It is "
     "usually far better</b>, and reporting the measurement is more "
     "useful than reporting the bound.",
     "",
     "<b>And consider a sample first.</b> <b>Reservoir sampling plus "
     "exact computation on the sample answers many questions</b> that a "
     "specialised sketch would also answer.",
   ],
   "footnote": "<b>Mergeability is the property that makes sketches "
               "infrastructure</b> — a mergeable sketch can be "
               "computed per shard and combined, which is what a "
               "distributed system needs."},

  {"t": "callout", "title": "Why sketches are the most used material in this course",
   "kind": "The assessment",
   "body": ["<b>Every large-scale monitoring, analytics, or "
            "observability system is built from these</b> — "
            "cardinality estimation, heavy hitters, quantiles, and "
            "membership tests, at volumes where exact answers are "
            "impossible.",
            "<b>And the guarantees are the selling point:</b> <b>'2% "
            "error with 99% confidence from 1.5 KB' is a specification "
            "an engineer can design against</b>, which an "
            "unquantified approximation is not.",
            "<b>So this module is where the concentration bounds of "
            "Module 02 pay off most visibly</b> — every one of these "
            "bounds is a Chernoff or Chebyshev argument.",
            "<b>And the honest caveat:</b> <b>the bounds are "
            "worst-case over streams, and your stream is not "
            "adversarial</b> — <b>so measure, and expect to do much "
            "better than the guarantee.</b>"]},
 ],
 "takeaways": [
   "The streaming model forces approximation — exact distinct "
   "counting provably needs linear space — and the value is that the "
   "approximation comes with an (ε, δ) bound.",
   "Count-min takes the minimum across rows because every row "
   "overestimates, which gives one-sided error.",
   "Count-min's error is relative to the total stream weight, which makes "
   "it a heavy-hitter sketch and useless for rare items.",
   "'Relative to what?' is the question to ask of every sketch.",
   "HyperLogLog's memory is independent of the cardinality because it "
   "stores an exponent, giving 2% error from 1.5 KB at any scale.",
   "Mergeability is what makes sketches infrastructure — compute per "
   "shard and combine.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The streaming model"),
  ("callout", "The streaming model, and what it forces",
   ["<b>Items arrive one at a time, you may not store them, and the "
    "available memory is polylogarithmic in the stream length.</b> One "
    "pass, or sometimes a small constant number.",
    "<b>Which forces approximation.</b> <b>Exact distinct counting "
    "provably requires space linear in the number of distinct items</b> "
    "(by a communication-complexity argument), so every sublinear-space "
    "answer is necessarily approximate — <b>and the model's value is "
    "that the approximation comes with a bound</b> rather than being a "
    "hope.",
    "<b>And the guarantees take the (&epsilon;, &delta;) form:</b> "
    "<b>the answer is within a relative error &epsilon; with probability "
    "at least 1 &minus; &delta;</b>, with the memory requirement "
    "depending on both parameters.",
    "<b>So the design question is always the same:</b> <b>how much "
    "memory, for what accuracy, at what confidence</b> — and "
    "<b>all three are tunable</b>, which is precisely what makes sketches "
    "engineering tools rather than theoretical curiosities. <b>You pick "
    "the point on the surface that your application needs.</b>"]),
  ("table", ["Sketch", "What it answers", "Memory"],
   [["<b>Count-min</b>",
     "<b>Item frequencies, and heavy hitters.</b>",
     "<b>O((1/&epsilon;) log(1/&delta;))</b> counters (&sect;2)."],
    ["<b>HyperLogLog</b>", "<b>The number of distinct items.</b>",
     "<b>About 1.5 KB for 2% error, at any cardinality</b> — see "
     "the note."],
    ["<b>Bloom filter</b>",
     "<b>Membership, with one-sided error.</b>",
     "<b>About 10 bits per item for 1% false positives.</b>"],
    ["<b>AMS / tug-of-war</b>",
     "<b>The second frequency moment, and self-join size.</b>",
     "<b>O((1/&epsilon;&#178;) log(1/&delta;))</b> — note the "
     "squared dependence, which is worse."],
    ["<b>Reservoir sample</b>",
     "<b>A uniform random sample of size k.</b>",
     "<b>O(k) — and it is <i>exact</i>, not approximate</b> "
     "(&sect;3)."],
    ["<b>t-digest, KLL</b>", "<b>Quantiles and percentiles.</b>",
     "<b>O((1/&epsilon;) log) — and KLL is the one with proved "
     "bounds</b>, while t-digest is the one in wide use."]],
   [0.20, 0.36, 0.44]),
  ("p", "<b>HyperLogLog's memory being independent of the cardinality is "
        "the result that makes distinct counting at scale possible at "
        "all</b> — <b>1.5 kilobytes whether the stream contains a "
        "thousand distinct items or a billion</b>, which is why it is "
        "deployed essentially universally for unique-visitor and "
        "cardinality metrics. <b>The scale-independence is what makes "
        "people adopt it</b>, more than the error bound."),

  ("h1", "2 &nbsp; Count-min"),
  ("code", """A d x w table of counters, and d independent hash functions
mapping items into [w].

UPDATE(x, c):  for each row i, add c to table[i][h_i(x)]
QUERY(x):      return the MINIMUM over rows i of
                   table[i][h_i(x)]

WHY THE MINIMUM: each cell holds x's true count PLUS the
counts of every other item that happens to hash to that
cell. So EVERY row OVERESTIMATES, and the minimum across
rows is the least bad overestimate available.
    -> ONE-SIDED ERROR. The answer is never too small,
       which is a useful property when thresholding.

THE BOUND: with w = e/eps and d = ln(1/delta),
    estimate <= true count + eps * (total stream weight)
with probability at least 1 - delta.

NOTE CAREFULLY WHAT THE ERROR IS RELATIVE TO: the TOTAL
stream weight, not x's own count. So count-min is excellent
for HEAVY HITTERS and essentially useless for rare items --
an item with true count 3 in a stream of total weight 10^9
will have an estimate completely dominated by noise.

WHICH IS THE QUESTION TO ASK OF ANY SKETCH: the error is
relative to WHAT?"""),

  ("break",),
  ("h1", "3 &nbsp; Distinct counting, and sampling"),
  ("callout", "HyperLogLog counts distinct items by looking at leading "
              "zeros",
   ["<b>Hash each incoming item and record the maximum number of leading "
    "zeros observed in any hash value.</b> <b>If you have seen a hash "
    "with k leading zeros, you have probably processed about "
    "2<super>k</super> distinct items</b> — because a random hash "
    "has k leading zeros with probability 2<super>&minus;k</super>.",
    "<b>And duplicates do not affect the estimate at all</b>, because "
    "hashing is deterministic and a repeated item produces the same hash "
    "and therefore the same leading-zero count — <b>which is exactly "
    "what makes it a <i>distinct</i> counter rather than a counter.</b> "
    "The idea is genuinely elegant.",
    "<b>A single such estimate is extremely noisy, so use many "
    "registers:</b> use the first few hash bits to select one of m "
    "registers, record the leading-zero count in each, and <b>combine "
    "with a harmonic mean</b>, which suppresses the influence of "
    "individual large outliers.",
    "<b>Giving about 2% relative error from roughly 1.5 kilobytes, at "
    "any cardinality</b> — <b>and the memory is independent of the "
    "count because each register stores an <i>exponent</i> (a small "
    "integer, 6 bits) rather than a count.</b> <b>That substitution of "
    "an exponent for a number is the whole trick.</b>"]),
  ("callout", "Reservoir sampling, which is exact",
   ["<b>To maintain a uniform random sample of k items from a stream "
    "whose length you do not know in advance:</b> keep the first k items, "
    "then for the n-th item (n &gt; k), replace a uniformly chosen "
    "reservoir slot with probability k/n.",
    "<b>The result is exactly uniform</b> — a short induction shows "
    "that after n items every item seen has probability exactly k/n of "
    "being in the reservoir, which is what uniformity means.",
    "<b>So this is not a sketch in the approximate sense:</b> <b>the "
    "sample is exactly correct, and only the <i>choice</i> of which items "
    "are in it is random.</b> No &epsilon; and no &delta; appear.",
    "<b>Which makes it the most broadly useful tool in the module</b> "
    "— <b>a uniform sample lets you estimate essentially anything</b> "
    "(with error governed by Module 02's bounds on the sample), "
    "<b>rather than answering one specific pre-chosen question like the "
    "other sketches do.</b> <b>So it is worth trying first</b> "
    "(&sect;4), and a specialised sketch is worth it when the sample is "
    "too small to resolve what you need."]),

  ("h1", "4 &nbsp; Choosing and using a sketch"),
  ("ul", ["<b>Ask what the error is relative to.</b> <b>Count-min's "
          "error is relative to the <i>total stream weight</i>; "
          "HyperLogLog's is relative to the <i>cardinality</i>; a "
          "sample's is relative to the quantity being estimated</b> "
          "— <b>completely different guarantees</b>, and this is the "
          "question that decides whether a sketch answers your question "
          "at all.",
          "<b>Check mergeability.</b> <b>Count-min, HyperLogLog, and "
          "Bloom filters all merge</b> (cellwise maximum or sum, "
          "register-wise maximum, bitwise OR) — <b>which is what "
          "makes them usable in a distributed aggregation</b> "
          "(CSCE 678 Module 04), where each shard sketches locally and "
          "the sketches are combined.",
          "<b>Check the error direction.</b> <b>Count-min overestimates "
          "and never underestimates</b>, which matters a great deal when "
          "you threshold on the result — you will get false heavy "
          "hitters and never miss a real one.",
          "<b>Measure the achieved error against the bound.</b> <b>It "
          "is usually far better</b>, because the bound is worst-case over "
          "all streams — <b>and reporting the measured error "
          "alongside the guarantee is more useful than reporting the "
          "guarantee alone</b> (Module 13 &sect;1).",
          "<b>And consider a plain sample first.</b> <b>Reservoir "
          "sampling plus exact computation on the sample answers a great "
          "many questions</b> that a specialised sketch would also answer, "
          "with far less machinery and a guarantee you can derive in two "
          "lines. <b>Mergeability is the property that makes sketches "
          "infrastructure</b>, and it is the one to check first when "
          "designing for a distributed setting."]),
  ("callout", "Why sketches are the most used material in this course",
   ["<b>Every large-scale monitoring, analytics, or observability system "
    "is built from these</b> — cardinality estimation for unique "
    "counts, heavy hitters for top-k, quantile sketches for latency "
    "percentiles, Bloom filters for negative lookups — <b>at volumes "
    "where exact answers are simply not available.</b>",
    "<b>And the guarantees are the selling point:</b> <b>'2% error with "
    "99% confidence from 1.5 kilobytes' is a specification an engineer can "
    "design against</b>, which an unquantified approximation is not. "
    "<b>The bound is the product.</b>",
    "<b>So this module is where Module 02's concentration bounds pay "
    "off most visibly</b> — <b>every error bound in &sect;1's table "
    "is a Chernoff or Chebyshev argument</b>, and deriving one yourself is "
    "the fastest way to make the toolkit feel useful rather than "
    "abstract.",
    "<b>And the honest caveat:</b> <b>the bounds are worst-case over "
    "all streams, and your stream is not adversarial</b> — <b>so "
    "measure, and expect to do considerably better than the "
    "guarantee</b>, which is CSCE 637 Module 01 &sect;3's "
    "worst-case qualification arriving in a setting where it is good "
    "news."]),
 ],
 "resources": [
   ("Cormode & Yi &mdash; Small Summaries for Big Data (free)",
    "https://web.archive.org/web/20260413113221/http://dimacs.rutgers.edu/~graham/ssbd.html",
    "<b>Free in full, and the reference for this whole module</b> "
    "— every sketch in &sect;1's table, with its bound and its "
    "merge operation."),
   ("Cormode & Muthukrishnan &mdash; An Improved Data Stream Summary: "
    "The Count-Min Sketch (free)",
    "https://web.archive.org/web/20260709152436/http://dimacs.rutgers.edu/~graham/pubs/papers/cm-full.pdf",
    "<b>&sect;2's sketch, in the original</b>, with the bound derived."),
   ("Flajolet et al. &mdash; HyperLogLog (free)",
    "https://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf",
    "<b>&sect;3's method</b>, including why the harmonic mean is the "
    "right combiner."),
   ("Vitter &mdash; Random Sampling with a Reservoir (free)",
    "https://www.cs.umd.edu/~samir/498/vitter.pdf",
    "<b>&sect;3's reservoir sampling</b>, with the uniformity proof and "
    "the faster variants."),
 ],
 "exercises": [
   "<b>Implement a count-min sketch</b> and measure its error on a real "
   "stream against the derived bound.",
   "<b>Confirm the error is one-sided</b> by comparing estimates against "
   "exact counts.",
   "<b>Query a rare item</b> and report how bad the estimate is. Relate "
   "it to the total weight.",
   "<b>Implement HyperLogLog</b> with 1024 registers and measure the "
   "error at several cardinalities.",
   "<b>Confirm the memory is independent of the cardinality.</b>",
   "<b>Implement reservoir sampling</b> and verify the uniformity "
   "empirically over many runs.",
   "<b>Use the sample to estimate three different quantities</b> and "
   "bound each error with Module 02's tools.",
   "<b>Merge two count-min sketches</b> and two HLL sketches, and verify "
   "the results match sketching the combined stream.",
   "<b>Compare a sketch against a sample</b> for one question, and report "
   "which was better.",
   "<b>Measure the achieved error against the bound</b> for every sketch "
   "you implemented, and report the ratio.",
 ],
 "selfcheck": [
   "State the streaming model's constraints and what they force.",
   "What is the (ε, δ) form, and what is tunable?",
   "Name six sketches and what each answers.",
   "Why is HyperLogLog's memory independent of the cardinality?",
   "Describe count-min and explain why the minimum is taken.",
   "What is count-min's error relative to, and what follows?",
   "Explain HyperLogLog's leading-zero idea and why duplicates do not "
   "matter.",
   "Why is reservoir sampling exact, and why is it the most broadly "
   "useful?",
   "Give five practical checks when choosing a sketch.",
   "Why is mergeability the key infrastructure property?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Random Graphs",
 "subtitle": "Phase transitions, and why they matter.",
 "question": "What does a random graph look like, and why does it change "
             "suddenly?",
 "outcomes": [
     "Define the Erdős–Rényi models.",
     "Explain the giant component transition.",
     "Explain the connectivity and other thresholds.",
     "Explain the first and second moment methods.",
     "Relate random graph thresholds to real phase transitions.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The model",
   "blurb": "And the thresholds."},

  {"t": "callout", "title": "G(n, p): n vertices, each edge present independently with probability p",
   "kind": "The model, and the striking fact",
   "body": ["<b>The simplest possible random graph model</b>, and "
            "<b>almost every property appears suddenly at a threshold "
            "rather than gradually.</b>",
            "<b>At p = 1/n the giant component appears.</b> Below, all "
            "components are O(log n); above, one component contains a "
            "constant fraction of all vertices.",
            "<b>At p = ln n / n the graph becomes connected</b>, and "
            "the last isolated vertex disappears at the same moment "
            "— which is not a coincidence.",
            "<b>And the transitions are sharp:</b> <b>the window in "
            "which the property goes from unlikely to likely shrinks as n "
            "grows</b>, so for large n the behaviour is effectively a step "
            "function."]},

  {"t": "table", "kicker": "Thresholds", "title": "What appears when",
   "header": ["Property", "Threshold", "Note"],
   "widths": [3.0, 3.4, 4.7],
   "rows": [
     ["<b>Giant component</b>", "<b>p = 1/n</b>", "<b>Average degree 1. The famous one</b>"],
     ["<b>Connectivity</b>", "<b>p = ln n / n</b>", "<b>Same as no isolated vertices</b>"],
     ["<b>A triangle appears</b>", "<b>p = 1/n</b>", "<b>Constant expected number at this scale</b>"],
     ["<b>Hamiltonian cycle</b>", "<b>p = ln n / n</b>", "<b>Same as connectivity, which is surprising</b>"],
     ["<b>Perfect matching</b>", "<b>p = ln n / n</b>", "<b>Also the same</b>"],
     ["<b>Diameter 2</b>", "<b>p ≈ √(2 ln n / n)</b>", "<b>Much denser</b>"],
   ],
   "footnote": "<b>That Hamiltonicity appears at the same threshold as "
               "connectivity is striking</b> — the obvious obstacle "
               "to a Hamiltonian cycle is a low-degree vertex, and once "
               "those are gone the cycle exists.",
   "note": "The Hamiltonicity coincidence is genuinely surprising and "
           "worth dwelling on."},

  {"t": "section", "label": "Part 2", "title": "The two methods",
   "blurb": "How threshold results are proved."},

  {"t": "code", "kicker": "The methods", "title": "First moment up, second moment down",
   "lang": "text", "code": """
  TO SHOW A STRUCTURE DOES NOT APPEAR (below threshold):
  FIRST MOMENT METHOD.
      Let X = number of copies of the structure.
      If E[X] -> 0, then P(X >= 1) <= E[X] -> 0
          by Markov (Module 02).
      So with high probability there are NONE.

  TO SHOW IT DOES APPEAR (above threshold):
  SECOND MOMENT METHOD.
      E[X] -> infinity is NOT enough -- the mass could sit
          on rare instances with huge X.
      But if Var[X] / E[X]^2 -> 0, then Chebyshev gives
          P(X = 0) -> 0.
      So with high probability there is at least one.

  THAT IS THE WHOLE TOOLKIT for threshold results, and it
  is just Markov and Chebyshev (Module 02 Part 1).

  THE ASYMMETRY IS THE POINT: showing something is ABSENT
  needs only the mean; showing it is PRESENT needs the
  variance. Which is why the second moment calculation is
  the hard half of every such proof.
""",
   "caption": "<b>Absence needs the mean; presence needs the "
              "variance</b> — and that asymmetry recurs throughout "
              "probabilistic combinatorics.",
   "note": "The asymmetry is the transferable insight, not the specific "
           "thresholds."},

  {"t": "section", "label": "Part 3", "title": "Real phase transitions",
   "blurb": "Where this shows up outside graph theory."},

  {"t": "bullets", "kicker": "Transitions", "title": "Thresholds in systems you care about",
   "items": [
     "<b>Random SAT.</b> <b>3-SAT is easy below a clause/variable "
     "ratio of about 4.27 and easy above it, and hard at it</b> "
     "— which is CSCE 637 §12's parameter, and it is a "
     "genuine sharp transition.",
     "",
     "<b>Percolation.</b> <b>Connectivity in a random network, "
     "which is the model for epidemic spread, forest fire, and material "
     "fracture.</b>",
     "",
     "<b>Network robustness.</b> <b>Remove a fraction of nodes and "
     "the giant component vanishes at a threshold</b> — which is "
     "how resilience is analysed (CSCE 678).",
     "",
     "<b>Cuckoo hashing's load factor</b> (Module 04 §3), "
     "<b>which is a threshold in a random bipartite graph.</b>",
     "",
     "<b>And community detection's detectability threshold</b> "
     "— below a certain signal strength, no algorithm can recover "
     "the communities, provably.",
   ],
   "footnote": "<b>The detectability threshold is the most striking:</b> "
               "<b>an information-theoretic limit below which no amount "
               "of computation helps</b>, which is a different kind of "
               "impossibility from CSCE 627's."},

  {"t": "callout", "title": "Why real networks are not Erdős–Rényi",
   "kind": "The honest qualification",
   "body": ["<b>Real networks have heavy-tailed degree distributions, "
            "high clustering, and community structure.</b> <b>G(n,p) has "
            "none of those</b> — its degrees are Poisson and its "
            "clustering is zero.",
            "<b>So the thresholds are not quantitatively predictive for "
            "a real network</b>, and models that are (preferential "
            "attachment, configuration models, stochastic block models) "
            "have different thresholds.",
            "<b>But the <i>existence</i> of sharp transitions "
            "transfers</b> — <b>real networks also have thresholds, "
            "and the methods of Part 2 are how they are found.</b>",
            "<b>So use G(n,p) as the null model</b>: <b>'a random graph "
            "with this degree sequence would have clustering 0.001 and we "
            "observe 0.3' is the useful form</b> — the same "
            "baseline-not-prediction use as Module 03 §4."]},

  {"t": "section", "label": "Part 4", "title": "Random graphs as a tool",
   "blurb": "Not just an object of study."},

  {"t": "bullets", "kicker": "As a tool", "title": "Where random graphs are used constructively",
   "items": [
     "<b>Expander graphs</b> — <b>a random graph is an expander "
     "with high probability</b>, and expanders are the key object in "
     "derandomisation (Module 12 §3).",
     "",
     "<b>Error-correcting codes.</b> <b>Random sparse parity-check "
     "matrices give near-optimal codes</b> (LDPC), which is a "
     "probabilistic existence proof with a practical consequence.",
     "",
     "<b>Testing and benchmarking.</b> <b>Random instances are the "
     "standard benchmark</b> — with the caveat that they are "
     "frequently easier than real ones (CSCE 637 §01).",
     "",
     "<b>Network design.</b> <b>Random regular graphs have small "
     "diameter and good fault tolerance</b>, which is why some "
     "datacentre topologies are randomised.",
     "",
     "<b>And the probabilistic method</b>, which is Module 07 and is "
     "the general form of all of these.",
   ],
   "footnote": "<b>'A random object has the property, therefore one "
               "exists' is the move</b> — and it is Module 07's "
               "subject, with random graphs as its most productive "
               "setting."},
 ],
 "takeaways": [
   "In G(n,p) almost every property appears suddenly at a threshold, and "
   "the transition window shrinks as n grows.",
   "The giant component appears at p = 1/n and connectivity at ln n / n "
   "— the same point at which the last isolated vertex disappears.",
   "Hamiltonicity appears at the same threshold as connectivity, which is "
   "striking: once low-degree vertices are gone, the cycle exists.",
   "First moment with Markov shows absence; second moment with Chebyshev "
   "shows presence — and that asymmetry is the transferable insight.",
   "Real networks are not Erdős–Rényi, so use G(n,p) as a "
   "null model rather than a prediction.",
   "Random graphs are also a construction tool: expanders, LDPC codes, and "
   "randomised network topologies all come from 'a random one works'.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The model and its thresholds"),
  ("callout", "G(n, p): n vertices, each edge present independently with "
              "probability p",
   ["<b>The simplest possible random graph model</b> — and the "
    "striking fact about it is that <b>almost every property of interest "
    "appears suddenly at a threshold value of p rather than increasing "
    "gradually.</b>",
    "<b>At p = 1/n the giant component appears.</b> Below that, all "
    "connected components have size O(log n); above it, a single component "
    "contains a constant fraction of all n vertices. <b>Average degree "
    "exactly 1 is the tipping point</b>, which is the most famous result "
    "in the subject.",
    "<b>At p = ln n / n the graph becomes connected</b>, and <b>the last "
    "isolated vertex disappears at precisely the same moment</b> — "
    "which is not a coincidence: the isolated vertex is the binding "
    "obstacle, and once none remains the graph is connected.",
    "<b>And the transitions are sharp:</b> <b>the window of p in which "
    "the property goes from unlikely to likely shrinks as n grows</b>, so "
    "<b>for large n the behaviour is effectively a step function</b> "
    "rather than a smooth curve. That sharpness is what makes 'threshold' "
    "the right word."]),
  ("table", ["Property", "Threshold", "Note"],
   [["<b>A giant component exists</b>", "<b>p = 1/n</b>",
     "<b>Average degree 1. The famous one</b>, and the basis of "
     "percolation theory."],
    ["<b>The graph is connected</b>", "<b>p = ln n / n</b>",
     "<b>Exactly the same threshold as 'no isolated vertices'</b>, and "
     "for the reason in the callout."],
    ["<b>A triangle appears</b>", "<b>p = 1/n</b>",
     "<b>The expected number of triangles is constant at this scale</b>, "
     "which is where the first-moment calculation turns over."],
    ["<b>A Hamiltonian cycle exists</b>", "<b>p = ln n / n</b>",
     "<b>The same threshold as mere connectivity</b>, which is "
     "surprising — see the note."],
    ["<b>A perfect matching exists</b>", "<b>p = ln n / n</b>",
     "<b>Also the same</b>, and for a related reason."],
    ["<b>Diameter at most 2</b>",
     "<b>p about &radic;(2 ln n / n)</b>",
     "<b>Much denser</b> — every pair needs a common neighbour, "
     "which is a far stronger requirement."]],
   [0.26, 0.26, 0.48]),
  ("p", "<b>That Hamiltonicity appears at the same threshold as "
        "connectivity is genuinely striking.</b> <b>The obvious obstacle "
        "to a Hamiltonian cycle is a vertex of degree less than two, and "
        "once those have all disappeared — which happens at the "
        "connectivity threshold — the cycle exists with high "
        "probability.</b> <b>So the only obstruction is the local "
        "one</b>, which is not at all what you would expect given that "
        "Hamiltonicity is NP-complete in general (CSCE 637 "
        "Module 04 &sect;2)."),

  ("h1", "2 &nbsp; The first and second moment methods"),
  ("code", """TO SHOW A STRUCTURE DOES NOT APPEAR (below threshold):
FIRST MOMENT METHOD.
    Let X = the number of copies of the structure.
    If E[X] -> 0, then P(X >= 1) <= E[X] -> 0,
        by Markov's inequality (Module 02 section 1).
    So with high probability there are NONE.

TO SHOW IT DOES APPEAR (above threshold):
SECOND MOMENT METHOD.
    E[X] -> infinity is NOT sufficient -- the expectation
        could be carried by rare instances with enormous X,
        while most instances have X = 0.
    But if Var[X] / E[X]^2 -> 0, then Chebyshev gives
        P(X = 0) -> 0.
    So with high probability there is at least one.

THAT IS THE WHOLE TOOLKIT for threshold results, and it is
nothing more than Markov and Chebyshev (Module 02).

THE ASYMMETRY IS THE POINT: showing a structure is ABSENT
needs only the mean; showing it is PRESENT needs the
variance as well. Which is why the second moment
calculation is the hard half of every such proof, and why
lower-bound and upper-bound halves of a threshold result
have completely different difficulty."""),
  ("p", "<b>Absence needs the mean; presence needs the variance</b> "
        "— <b>and that asymmetry recurs throughout probabilistic "
        "combinatorics</b> and into Module 07's probabilistic method, "
        "where the same two-sided structure appears. <b>It is the "
        "transferable insight from this module</b>, considerably more so "
        "than any particular threshold value."),

  ("break",),
  ("h1", "3 &nbsp; Real phase transitions"),
  ("ul", ["<b>Random SAT.</b> <b>Random 3-SAT is easy below a "
          "clause-to-variable ratio of about 4.27 (because solutions are "
          "abundant) and easy above it (because unsatisfiability is easy "
          "to establish), and hard right at it</b> — which is "
          "<b>CSCE 637 Module 12's parameter</b>, and it is a genuine "
          "sharp transition with the hard instances concentrated in a "
          "narrowing window.",
          "<b>Percolation.</b> <b>Connectivity in a random network</b>, "
          "which is the standard model for epidemic spread, forest fire "
          "propagation, and material fracture — and the giant "
          "component threshold is the epidemic threshold.",
          "<b>Network robustness.</b> <b>Remove a random fraction of "
          "nodes and the giant component vanishes at a threshold</b> "
          "— <b>which is how network resilience is analysed</b> "
          "(CSCE 678), and the threshold differs sharply between random "
          "failure and targeted attack on high-degree nodes.",
          "<b>Cuckoo hashing's load factor</b> (Module 04 "
          "&sect;3) <b>is a threshold in a random bipartite graph</b> "
          "— the insertion cascade terminates exactly when that graph "
          "has no dense subgraph, which happens below 0.5.",
          "<b>And community detection's detectability threshold</b> "
          "— <b>below a certain signal strength in a stochastic "
          "block model, no algorithm whatsoever can recover the "
          "communities, provably</b>. <b>Which is the most striking item "
          "here: an information-theoretic limit below which no amount of "
          "computation helps</b>, and that is <b>a different kind of "
          "impossibility from CSCE 627's</b> — the information is "
          "absent rather than the computation infeasible."]),
  ("callout", "Why real networks are not Erdős–Rényi",
   ["<b>Real networks have heavy-tailed degree distributions, high "
    "clustering, and community structure.</b> <b>G(n,p) has none of "
    "those</b> — its degree distribution is Poisson (thin-tailed), "
    "its clustering coefficient tends to zero, and it has no communities "
    "by construction.",
    "<b>So the thresholds are not quantitatively predictive for a real "
    "network</b>, and the models that are — preferential attachment, "
    "the configuration model, stochastic block models — have "
    "different thresholds, sometimes dramatically so (scale-free networks "
    "have no epidemic threshold at all in the infinite limit).",
    "<b>But the <i>existence</i> of sharp transitions transfers</b> "
    "— <b>real networks also exhibit thresholds, and &sect;2's "
    "moment methods are how they are located</b> in whichever model is "
    "appropriate.",
    "<b>So use G(n,p) as the null model.</b> <b>'A random graph with "
    "this degree sequence would have a clustering coefficient of 0.001 and "
    "we observe 0.3' is the useful form</b> — <b>the same "
    "baseline-not-prediction use as Module 03 &sect;4</b>, and the "
    "pattern is worth noticing: <b>the simple random model's value is as "
    "a comparison point, not as a description.</b>"]),

  ("h1", "4 &nbsp; Random graphs as a construction tool"),
  ("ul", ["<b>Expander graphs.</b> <b>A random regular graph is an "
          "expander with high probability</b>, and <b>expanders are the "
          "central object in derandomisation</b> (Module 12 "
          "&sect;3) — so the existence proof is probabilistic and "
          "the explicit constructions came decades later and are harder.",
          "<b>Error-correcting codes.</b> <b>Random sparse "
          "parity-check matrices give codes approaching the channel "
          "capacity</b> (LDPC codes), <b>which is a probabilistic "
          "existence proof with a very large practical consequence</b> "
          "— these codes are in every modern wireless standard.",
          "<b>Testing and benchmarking.</b> <b>Random instances are the "
          "standard benchmark</b> for graph algorithms — <b>with the "
          "important caveat that they are frequently much easier than real "
          "instances</b> (CSCE 637 Module 01 &sect;3), because real "
          "instances have structure that random ones lack.",
          "<b>Network design.</b> <b>Random regular graphs have small "
          "diameter and good fault tolerance</b> for their degree, <b>which "
          "is why some datacentre network topologies are deliberately "
          "randomised</b> (Jellyfish and its successors) rather than "
          "structured.",
          "<b>And the probabilistic method</b>, which is Module 07 and "
          "is the general form of all four of these. <b>'A random object "
          "has the property, therefore an object with the property "
          "exists' is the move</b>, and <b>random graphs are its most "
          "productive setting.</b>"]),
 ],
 "resources": [
   ("Mitzenmacher & Upfal &mdash; chapters 5 and 6",
    "https://www.cambridge.org/core/books/probability-and-computing/7D2016B2EB4B5E5F4F2C4E4F4F4C4E4F",
    "<b>Random graphs and the moment methods of &sect;2</b>, at the right "
    "level for this course."),
   ("Bollobás &mdash; Random Graphs",
    "https://www.cambridge.org/core/books/random-graphs/5EAEC0F8E1DE4CBFC9D9FB2A8B5D6C8F",
    "<b>The comprehensive reference</b> for &sect;1's thresholds. Library "
    "copy."),
   ("Newman &mdash; Networks",
    "https://global.oup.com/academic/product/networks-9780198805090",
    "<b>&sect;3's real networks</b>, including why they differ from "
    "G(n,p) and which models fit. Library copy; the author's lecture "
    "notes are free."),
   ("Decelle, Krzakala, Moore & Zdeborová &mdash; the detectability "
    "threshold (free)",
    "https://arxiv.org/abs/1109.3041",
    "<b>&sect;3's most striking result</b> — the "
    "information-theoretic limit on community detection."),
 ],
 "exercises": [
   "<b>Generate G(n,p) for a range of p</b> and plot the largest "
   "component size. Locate the transition.",
   "<b>Confirm the transition sharpens as n grows.</b>",
   "<b>Plot the connectivity probability</b> against p and locate "
   "ln n / n.",
   "<b>Count isolated vertices</b> and confirm they vanish at the same "
   "point.",
   "<b>Test for Hamiltonicity</b> at several p and confirm it coincides "
   "with connectivity.",
   "<b>Apply the first moment method</b> to show triangles are absent "
   "below the threshold.",
   "<b>Apply the second moment method</b> to show they are present above "
   "it, and note which half was harder.",
   "<b>Generate random 3-SAT at several clause ratios</b> and plot solver "
   "time. Locate 4.27.",
   "<b>Compute the clustering coefficient</b> of a real network and of "
   "G(n,p) with matching density.",
   "<b>Generate a random regular graph</b> and measure its diameter "
   "against a structured topology of the same degree.",
 ],
 "selfcheck": [
   "Define G(n,p) and state the striking fact about its properties.",
   "Give six thresholds and what appears at each.",
   "Why do connectivity and 'no isolated vertices' coincide?",
   "Why is the Hamiltonicity threshold surprising?",
   "State the first and second moment methods and the inequality each "
   "uses.",
   "Why is the asymmetry between them the point?",
   "Name five real phase transitions.",
   "Which is information-theoretic rather than computational, and why "
   "does that differ?",
   "Why are real networks not G(n,p), and how should the model be "
   "used?",
   "Name four constructive uses of random graphs.",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "The Probabilistic Method",
 "subtitle": "Proving things exist by picking one at random.",
 "question": "How can a probability argument prove an object exists?",
 "outcomes": [
     "Apply the basic probabilistic method to an existence proof.",
     "Apply the expectation argument and the deletion method.",
     "State and apply the Lovász local lemma.",
     "Explain the alteration and second-moment variants.",
     "Explain how a probabilistic existence proof becomes an "
     "algorithm.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The basic method",
   "blurb": "If a random object works with positive probability, one "
            "exists."},

  {"t": "code", "kicker": "The method", "title": "The argument, and a complete example",
   "lang": "text", "code": """
  THE METHOD: to prove an object with property P exists,
  define a probability distribution over candidates and
  show P(a random candidate has P) > 0.

  Then at least one candidate has P. Done.
  No construction, no explicit object -- just existence.

  EXAMPLE: every graph has a cut containing at least half
  its edges.

      Put each vertex independently on side A or B, by a
      fair coin.
      Each edge crosses the cut with probability 1/2.
      So E[edges crossing] = m/2, by linearity.
      An average is attained or exceeded by some outcome.
      So SOME assignment cuts at least m/2 edges. Done.

  THAT IS A COMPLETE PROOF of a non-trivial combinatorial
  fact, in five lines, with no construction.

  AND IT IS CONSTRUCTIVE ANYWAY: the random assignment
  achieves m/2 in expectation, so it is a 1/2-approximation
  algorithm for MAX-CUT -- which is CSCE 669 Module 10,
  and is the baseline the SDP improves on.
""",
   "caption": "<b>The existence proof and the approximation algorithm "
              "are the same argument</b>, which is why this method is "
              "practically relevant and not merely elegant.",
   "note": "The MAX-CUT example does double duty and should be the one "
           "taught."},

  {"t": "callout", "title": "Linearity of expectation does most of the work",
   "kind": "The technical point",
   "body": ["<b>E[X + Y] = E[X] + E[Y], regardless of "
            "dependence.</b> <b>No independence assumption at all</b>, "
            "which is why it applies where Chernoff does not "
            "(Module 02 §2).",
            "<b>So a count of structures is a sum of indicators, and "
            "its expectation is a sum of probabilities</b> — "
            "computable even when the indicators are heavily "
            "dependent.",
            "<b>Which is the whole technique:</b> <b>express the "
            "quantity as a sum, take expectations termwise, and conclude "
            "that some outcome achieves the average.</b>",
            "<b>And it is the most underused tool in "
            "probability</b> — <b>people reach for independence when "
            "linearity would have sufficed</b>, and linearity is free."]},

  {"t": "section", "label": "Part 2", "title": "Variants",
   "blurb": "When the basic method is not enough."},

  {"t": "table", "kicker": "Variants", "title": "The standard refinements",
   "header": ["Variant", "When to use it", "How"],
   "widths": [2.6, 3.9, 5.5],
   "rows": [
     ["<b>Expectation</b>", "<b>You want a bound, not just existence</b>", "<b>Some outcome meets the average</b>"],
     ["<b>Alteration</b>", "<b>The random object is nearly right</b>", "<b>Fix it up and bound the damage</b>"],
     ["<b>Deletion</b>", "<b>Too many bad structures</b>", "<b>Delete them; bound how much is lost</b>"],
     ["<b>Second moment</b>", "<b>Need concentration, not just the mean</b>", "<b>Chebyshev (M06 §2)</b>"],
     ["<b>Local lemma</b>", "<b>Many bad events, locally dependent</b>", "<b>Part 3 — the strongest tool</b>"],
   ],
   "footnote": "<b>The deletion method is the one to reach for when a "
               "first attempt gives a positive expected number of "
               "violations</b> — build the object anyway and remove "
               "the violations.",
   "note": "The variants are what make the method usable beyond toy "
           "examples."},

  {"t": "section", "label": "Part 3", "title": "The local lemma",
   "blurb": "When the union bound fails and the dependence is local."},

  {"t": "callout", "title": "Lovász local lemma: if bad events are rare and only locally dependent, none need occur",
   "kind": "The strongest tool in the module",
   "body": ["<b>Suppose each bad event has probability at most p and "
            "depends on at most d others. If e·p·(d+1) ≤ "
            "1, then with positive probability none of them occur.</b>",
            "<b>Which the union bound cannot give:</b> <b>with many bad "
            "events the sum of their probabilities exceeds 1 and the "
            "union bound says nothing</b> (Module 02 §3).",
            "<b>And the condition depends on the <i>local</i> "
            "dependency degree rather than the total number of "
            "events</b> — so a million bad events each depending on "
            "ten others is fine.",
            "<b>The canonical application is k-SAT:</b> <b>a formula "
            "where each clause shares variables with few others is "
            "satisfiable</b>, however many clauses there are — which "
            "the union bound cannot establish."]},

  {"t": "callout", "title": "And Moser–Tardos made it constructive",
   "kind": "The result that turned a proof into an algorithm",
   "body": ["<b>The local lemma was non-constructive for thirty "
            "years</b> — it proved a satisfying assignment exists and "
            "gave no way to find one.",
            "<b>Moser and Tardos's algorithm: sample randomly; while "
            "some bad event holds, resample <i>only its variables</i>; "
            "repeat.</b> <b>It terminates in expected polynomial "
            "time.</b>",
            "<b>And the proof is an entropy-compression argument</b> "
            "— if the algorithm ran long, the log of its resamplings "
            "would compress the random bits below their entropy, which is "
            "impossible.",
            "<b>Which is one of the best results in the subject:</b> <b>a "
            "thirty-year-old non-constructive proof made constructive by "
            "an algorithm of three lines</b>, with a proof technique "
            "nobody had used before."]},

  {"t": "section", "label": "Part 4", "title": "From existence to algorithm",
   "blurb": "Why this is not just a proof technique."},

  {"t": "bullets", "kicker": "Algorithms", "title": "Probabilistic existence proofs that are algorithms",
   "items": [
     "<b>MAX-CUT at 1/2.</b> <b>Part 1's proof is the "
     "algorithm</b> — flip coins (CSCE 669 §10).",
     "",
     "<b>MAX-3SAT at 7/8.</b> <b>A random assignment satisfies 7/8 "
     "of the clauses in expectation, and that is "
     "optimal</b> (CSCE 637 §11).",
     "",
     "<b>Set cover's log n.</b> <b>Randomised rounding of the LP, "
     "which is Module 08.</b>",
     "",
     "<b>Moser–Tardos for the local lemma</b>, which is "
     "Part 3.",
     "",
     "<b>And expander and code constructions</b>, where the "
     "probabilistic proof came first and explicit constructions followed "
     "decades later (Module 06 §4).",
   ],
   "footnote": "<b>The pattern is that the expectation argument is "
               "usually also the algorithm</b>, and the "
               "derandomisation of it is Module 12 §1."},

  {"t": "callout", "title": "Why this method is worth learning as an engineer",
   "kind": "The practical case",
   "body": ["<b>It produces approximation algorithms "
            "immediately.</b> <b>'A random choice achieves the average' "
            "gives a guarantee with no algorithm design at all</b>, and "
            "it is frequently the best known.",
            "<b>It tells you what is achievable before you design "
            "anything</b> — the random baseline is a floor, and if "
            "your clever algorithm does not beat it, you have "
            "learned something.",
            "<b>And it is the fastest route to a lower bound on what a "
            "structure must contain</b> — which is useful in sizing "
            "and capacity arguments.",
            "<b>So the habit is:</b> <b>before designing an algorithm, "
            "compute what a random choice achieves in "
            "expectation</b> — <b>it takes five minutes and it is "
            "sometimes the answer.</b>"]},
 ],
 "takeaways": [
   "If a random candidate has a property with positive probability, an "
   "object with that property exists — and no construction is "
   "needed.",
   "Linearity of expectation needs no independence, which is why it "
   "applies where Chernoff does not, and it is the most underused tool in "
   "probability.",
   "The MAX-CUT half-the-edges proof is five lines and is simultaneously a "
   "1/2-approximation algorithm.",
   "The Lovász local lemma works where the union bound fails, because "
   "its condition depends on the local dependency degree rather than the "
   "event count.",
   "Moser–Tardos made the local lemma constructive with a three-line "
   "resampling algorithm and an entropy-compression proof.",
   "Before designing an algorithm, compute what a random choice achieves "
   "in expectation — five minutes, and sometimes it is the answer.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The basic method"),
  ("code", """THE METHOD: to prove that an object with property P exists,
define a probability distribution over candidate objects and
show that P(a random candidate has property P) > 0.

Then at least one candidate must have property P. Done.
No construction, no explicit object -- just existence.

EXAMPLE: every graph has a cut containing at least half its
edges.

    Put each vertex independently on side A or side B, by a
    fair coin flip.
    Each edge crosses the cut with probability exactly 1/2.
    So E[number of edges crossing] = m/2, by linearity of
        expectation.
    An average is attained or exceeded by some outcome.
    So SOME assignment cuts at least m/2 edges. Done.

THAT IS A COMPLETE PROOF of a non-trivial combinatorial
fact, in five lines, with no construction whatsoever.

AND IT IS CONSTRUCTIVE ANYWAY: the random assignment
achieves m/2 in expectation, so it is a 1/2-approximation
algorithm for MAX-CUT -- which is CSCE 669 Module 10, and
is exactly the baseline that the semidefinite programming
relaxation improves on (to 0.878)."""),
  ("callout", "Linearity of expectation does most of the work",
   ["<b>E[X + Y] = E[X] + E[Y], regardless of any dependence between X "
    "and Y.</b> <b>No independence assumption at all</b> — which is "
    "why it applies in situations where Chernoff bounds do not "
    "(Module 02 &sect;2's requirement).",
    "<b>So a count of structures is a sum of indicator variables, and "
    "its expectation is the sum of their probabilities</b> — "
    "<b>computable even when the indicators are heavily dependent</b>, "
    "which is the usual situation in combinatorics.",
    "<b>Which is the whole technique:</b> <b>express the quantity of "
    "interest as a sum, take expectations term by term, and conclude that "
    "some outcome achieves at least the average.</b>",
    "<b>And it is the most underused tool in applied probability</b> "
    "— <b>people reach for an independence assumption when linearity "
    "would have sufficed</b>, and linearity is free and unconditional. "
    "<b>Whenever you find yourself worrying about dependence, check "
    "whether you only need the mean.</b>"]),

  ("h1", "2 &nbsp; The variants"),
  ("table", ["Variant", "When to use it", "How it works"],
   [["<b>Expectation argument</b>",
     "<b>You want a quantitative bound, not merely existence.</b>",
     "<b>Some outcome meets or exceeds the average</b> — &sect;1's "
     "MAX-CUT argument."],
    ["<b>Alteration</b>",
     "<b>The random object is nearly right but has some "
     "violations.</b>",
     "<b>Fix the violations by hand and bound how much the fixing "
     "costs</b> — used for Ramsey-type and independent-set bounds."],
    ["<b>Deletion</b>",
     "<b>The expected number of bad structures is positive but "
     "small.</b>",
     "<b>Build the object anyway, delete the bad structures, and bound "
     "how much of the object is lost</b> — see the note."],
    ["<b>Second moment</b>",
     "<b>You need concentration rather than just the mean.</b>",
     "<b>Compute the variance and apply Chebyshev</b> (Module 06 "
     "&sect;2's second moment method)."],
    ["<b>Lov&aacute;sz local lemma</b>",
     "<b>Many bad events, each unlikely, with only local "
     "dependence.</b>",
     "<b>&sect;3 — the strongest tool in the module.</b>"]],
   [0.21, 0.31, 0.48]),
  ("p", "<b>The deletion method is the one to reach for when a first "
        "attempt gives a positive expected number of violations</b> "
        "— rather than concluding the method has failed, <b>build the "
        "object anyway and remove the violations</b>, and if the expected "
        "number removed is a small fraction of the whole, the surviving "
        "object is still large enough. <b>It converts a failed argument "
        "into a working one surprisingly often.</b>"),

  ("break",),
  ("h1", "3 &nbsp; The Lovász local lemma"),
  ("callout", "Lovász local lemma: if bad events are rare and only "
              "locally dependent, none need occur",
   ["<b>Suppose each bad event has probability at most p, and each "
    "depends on at most d of the others. If e&middot;p&middot;(d+1) "
    "&le; 1, then with positive probability none of the bad events "
    "occur.</b>",
    "<b>Which the union bound cannot give:</b> <b>when there are many "
    "bad events, the sum of their probabilities exceeds 1 and the union "
    "bound says nothing at all</b> (Module 02 &sect;3's wastefulness "
    "note). <b>The local lemma is what you use instead.</b>",
    "<b>And the condition depends on the <i>local</i> dependency degree "
    "rather than the total number of events</b> — <b>so a million "
    "bad events, each depending on only ten others, satisfies the "
    "condition perfectly well.</b> That independence from the total count "
    "is the entire power of the result.",
    "<b>The canonical application is k-SAT:</b> <b>a formula in which "
    "each clause shares variables with only a few others is satisfiable, "
    "however many clauses it has</b> — which <b>the union bound "
    "cannot establish for any formula with more than a handful of "
    "clauses.</b> It is also how edge-colouring, frequency-assignment, "
    "and scheduling existence results are proved."]),
  ("callout", "And Moser–Tardos made it constructive",
   ["<b>The local lemma was non-constructive for roughly thirty "
    "years</b> — it proved that a satisfying assignment exists and "
    "gave no indication of how to find one, which is the usual limitation "
    "of the probabilistic method.",
    "<b>Moser and Tardos's algorithm: sample all variables randomly; "
    "while some bad event currently holds, resample <i>only the variables "
    "that event depends on</i>; repeat.</b> <b>It terminates in expected "
    "polynomial time under the local lemma's condition.</b> Three lines.",
    "<b>And the proof is an entropy-compression argument</b> — if "
    "the algorithm ran for many steps, then a log of which events were "
    "resampled would constitute a compression of the random bits consumed "
    "to below their entropy, <b>which is impossible</b>. <b>So the "
    "algorithm cannot run long.</b>",
    "<b>Which is one of the best results in this subject:</b> <b>a "
    "thirty-year-old non-constructive proof made constructive by an "
    "algorithm of three lines, with a proof technique nobody had used for "
    "the purpose before.</b> <b>And it is worth knowing as an example "
    "that non-constructive proofs are sometimes waiting to become "
    "algorithms</b>, rather than being permanently different in kind."]),

  ("h1", "4 &nbsp; From existence to algorithm"),
  ("ul", ["<b>MAX-CUT at ratio 1/2.</b> <b>&sect;1's existence proof "
          "<i>is</i> the algorithm</b> — flip a coin per vertex "
          "(CSCE 669 Module 10 &sect;2).",
          "<b>MAX-3SAT at 7/8.</b> <b>A uniformly random assignment "
          "satisfies 7/8 of the clauses in expectation, and 7/8 is "
          "provably optimal</b> (CSCE 637 Module 11 &sect;1) "
          "— <b>so the trivial probabilistic algorithm is the best "
          "possible</b>, which is both satisfying and deflating.",
          "<b>Set cover's logarithmic ratio.</b> <b>Randomised rounding "
          "of the linear programming relaxation</b>, which is "
          "Module 08.",
          "<b>Moser–Tardos for the local lemma</b> (&sect;3), "
          "which turns the strongest existence tool into a working "
          "algorithm.",
          "<b>And expander graph and error-correcting code "
          "constructions</b>, where <b>the probabilistic existence proof "
          "came first and explicit constructions followed decades "
          "later</b> (Module 06 &sect;4) — and in the code case "
          "the random construction is still what is used. <b>The pattern "
          "is that the expectation argument is usually also the "
          "algorithm</b>, and <b>derandomising it is Module 12 "
          "&sect;1's subject.</b>"]),
  ("callout", "Why this method is worth learning as an engineer",
   ["<b>It produces approximation algorithms immediately.</b> <b>'A "
    "random choice achieves the average' gives a guarantee with no "
    "algorithm design at all</b>, and <b>it is frequently the best known "
    "ratio</b> (MAX-3SAT being the clearest case).",
    "<b>It tells you what is achievable before you design anything.</b> "
    "<b>The random baseline is a floor</b>, and <b>if your clever "
    "algorithm does not beat a coin flip, you have learned something "
    "important cheaply.</b>",
    "<b>And it is the fastest route to a lower bound on what a structure "
    "must contain</b> — 'every graph on n vertices has an "
    "independent set of size at least X' — <b>which is useful in "
    "sizing and capacity arguments</b> well outside combinatorics.",
    "<b>So the habit is:</b> <b>before designing an algorithm for an "
    "optimisation problem, compute what a uniformly random choice achieves "
    "in expectation.</b> <b>It takes five minutes, it gives you a "
    "baseline and sometimes a guarantee, and it is sometimes simply the "
    "answer.</b>"]),
 ],
 "resources": [
   ("Alon & Spencer &mdash; The Probabilistic Method",
    "https://onlinelibrary.wiley.com/doi/book/10.1002/9781119061957",
    "<b>The reference for this module</b> — all the variants of "
    "&sect;2 and the local lemma. Library copy; Spencer's free lecture "
    "notes cover the core."),
   ("Mitzenmacher & Upfal &mdash; chapter 6",
    "https://www.cambridge.org/core/books/probability-and-computing/7D2016B2EB4B5E5F4F2C4E4F4F4C4E4F",
    "<b>The method at this course's level</b>, with the MAX-CUT and "
    "MAX-3SAT examples worked."),
   ("Moser & Tardos &mdash; A Constructive Proof of the General "
    "Lovász Local Lemma (free)",
    "https://arxiv.org/abs/0903.0032",
    "<b>&sect;3's constructive result</b> — short, and the "
    "entropy-compression argument is worth reading in full."),
   ("Tao &mdash; Moser's entropy compression argument (free blog post)",
    "https://terrytao.wordpress.com/2009/08/05/mosers-entropy-compression-argument/",
    "<b>&sect;3's proof technique explained</b>, more accessibly than the "
    "paper."),
 ],
 "exercises": [
   "<b>Prove the MAX-CUT half-the-edges result</b> yourself, and then "
   "implement it and measure the achieved ratio.",
   "<b>Prove the MAX-3SAT 7/8 result</b> by the same argument.",
   "<b>Find a problem where linearity suffices and you were about to "
   "assume independence</b>, and note the difference.",
   "<b>Apply the deletion method</b> to a problem where the basic method "
   "gives a positive expected number of violations.",
   "<b>Apply the alteration method</b> to prove an independent-set lower "
   "bound.",
   "<b>Construct a case where the union bound fails</b> and the local "
   "lemma applies.",
   "<b>Verify the local lemma's condition</b> for a k-SAT instance with "
   "bounded clause overlap.",
   "<b>Implement Moser–Tardos</b> and measure its resampling count "
   "against the bound.",
   "<b>For an optimisation problem you care about, compute the random "
   "baseline</b> in expectation.",
   "<b>Then beat it, or report that you could not.</b>",
 ],
 "selfcheck": [
   "State the probabilistic method and give the MAX-CUT proof.",
   "Why is that proof also an algorithm?",
   "Why does linearity of expectation need no independence, and why is "
   "it underused?",
   "Name five variants and when each applies.",
   "What does the deletion method do?",
   "State the local lemma and say what the union bound cannot give.",
   "Why does the local dependency degree matter rather than the event "
   "count?",
   "What did Moser–Tardos achieve, and by what argument?",
   "Name five probabilistic existence proofs that are algorithms.",
   "Give the five-minute habit this module recommends.",
 ],
},

]
