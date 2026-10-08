# -*- coding: utf-8 -*-
"""CSCE 676 Data Mining — original course content."""

COURSE = {
    "code": "CSCE 676",
    "title": "Data Mining",
    "tagline": "Finding structure in data too large to look at, without "
               "finding structure that is not there",
    "term": "Semester 10 (with CSCE 638 and CSCE 670)",
    "prereqs": "CSCE 629 Analysis of Algorithms and CSCE 658 Randomized "
               "Algorithms, both used heavily; CSCE 633 Machine Learning "
               "for the evaluation discipline; CSCE 678 Distributed "
               "Systems for Module 10",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A mining study on a dataset of at least a few "
                   "million records — a pattern you found, a "
                   "significance argument that survives the number of "
                   "hypotheses you tested, a baseline that explains the "
                   "pattern more cheaply, and a statement of what you "
                   "would need to call it causal",
    "description": [
        "<b>Data mining is the search for structure in data too large "
        "to inspect</b> — which makes it <b>two problems rather "
        "than one: finding candidate structure efficiently, and "
        "deciding whether what you found is real.</b> <b>Module 01 "
        "establishes both</b>, and the course alternates between them "
        "deliberately rather than treating the second as an "
        "afterthought.",
        "<b>The algorithmic half is about trading exactness for "
        "feasibility, deliberately and with a stated bound.</b> "
        "<b>Hashing, sketching, sampling, and sublinear approximation "
        "appear throughout</b> (Modules 02, 06, and 10) — and <b>they "
        "are all applications of CSCE 658's machinery</b>, which is "
        "why that course is a prerequisite rather than a "
        "recommendation.",
        "<b>The statistical half is about the fact that searching "
        "hard enough guarantees a finding.</b> <b>Module 11 is the "
        "course's centre</b>: if you test ten thousand hypotheses at "
        "the five percent level, you will find five hundred "
        "'significant' patterns in pure noise — <b>so a pattern "
        "found by search needs a different standard of evidence than "
        "one predicted in advance</b>, and most published mining "
        "results do not meet it.",
        "<b>The third theme is that scale changes which algorithm is "
        "correct.</b> <b>An O(n²) method is not slow at a "
        "billion records; it is impossible</b> (Module 10) — and "
        "<b>the constraint is usually memory and passes over the data "
        "rather than arithmetic</b>, which is why the streaming and "
        "sketching material is practical rather than exotic.",
        "<b>And the closing position is about honest claims.</b> "
        "<b>Module 12 covers what mining does to the people in the "
        "data</b>, and <b>Module 13 is about stating what a found "
        "pattern establishes</b> — because <b>'we discovered a "
        "correlation' is a statement about a search procedure</b>, and "
        "saying how hard you looked is what makes it "
        "interpretable.",
    ],
    "outcomes": [
        "Explain the two problems and why they need separate "
        "treatment.",
        "Find near-duplicates and similar items at scale.",
        "Mine frequent patterns and assess the rules they produce.",
        "Cluster large data and evaluate the result honestly.",
        "Reduce dimension and explain what each method preserves.",
        "Process a stream with bounded memory and a stated error.",
        "Mine a graph for communities and centrality.",
        "Detect anomalies and explain the base rate problem.",
        "Build and evaluate a recommender.",
        "Explain what scale does to algorithm choice.",
        "Correct for multiple testing and defend a found pattern.",
        "Explain re-identification and the privacy mechanisms.",
        "State what a discovered pattern honestly establishes.",
    ],
    "materials": [
        ("Leskovec, Rajaraman & Ullman — Mining of Massive Datasets "
         "(free PDF)",
         "http://www.mmds.org/",
         "<b>The primary text, free in full from the authors.</b> "
         "Modules 02, 04, 06, 07, and 09 follow it closely, and its "
         "treatment of locality-sensitive hashing is the best "
         "available."),
        ("Tan, Steinbach, Karpatne & Kumar — Introduction to Data "
         "Mining, 2nd edition",
         "https://www-users.cse.umn.edu/~kumar001/dmbook/index.php",
         "<b>The broader companion, with free chapters.</b> Stronger "
         "on Modules 03, 05, and 08, and on the evaluation material "
         "generally."),
        ("Aggarwal — Outlier Analysis, 2nd edition",
         "https://link.springer.com/book/10.1007/978-3-319-47578-3",
         "<b>Module 08 in depth</b> — and honest about how badly "
         "anomaly detection is usually evaluated. Library copy."),
        ("Benjamini & Hochberg, and the replication literature "
         "(free)",
         "https://www.jstor.org/stable/2346101",
         "<b>Module 11's methods and its motivation.</b> The FDR "
         "paper itself, read alongside the reproducibility work that "
         "made it urgent."),
        ("Dwork & Roth — The Algorithmic Foundations of Differential "
         "Privacy (free PDF)",
         "https://www.cis.upenn.edu/~aaroth/privacybook.html",
         "<b>Module 12's formal half, free in full.</b> Read the "
         "first three chapters; the definition is what matters for this "
         "course."),
        ("Stanford CS246 — Mining Massive Data Sets (free)",
         "http://web.stanford.edu/class/cs246/",
         "<b>The course this one is shaped against</b>, with free "
         "lectures and assignments by the authors of the primary "
         "text."),
    ],
    "tooling": [
        "<b>Python with NumPy, SciPy, scikit-learn, and "
        "pandas</b> — and <b>the exercises require you to implement "
        "the core algorithms before using the library versions</b>, "
        "because the approximation guarantees are invisible from "
        "outside.",
        "<b>A dataset of at least a few million records.</b> "
        "<b>Below that, everything fits in memory and the course's "
        "central constraint disappears</b> — which makes the "
        "material feel arbitrary. Public options are "
        "listed in the map.",
        "<b>Spark or Dask</b> for Module 10 — <b>run it on one "
        "machine first</b>, which is where you learn what the "
        "partitioning is doing, and only then on more.",
        "<b><code>datasketch</code> and <code>networkx</code></b> for "
        "Modules 06 and 07. <b>Read <code>datasketch</code>'s error "
        "parameters and verify its bounds empirically</b>, which is "
        "Module 06 §4's exercise.",
        "<b>A notebook, and a discipline about it:</b> <b>record "
        "every hypothesis you test, because Module 11 requires the "
        "count</b> and reconstructing it afterwards is not "
        "possible.",
        "<b>And a held-out portion you look at once.</b> <b>The same "
        "requirement as CSCE 638's and CSCE 633's</b>, and in this "
        "course it is the only defence against Module 11's "
        "problem.",
    ],
    "projects": [
        {"title": "Similar items at scale", "after": 6,
         "brief": "Build a near-duplicate detector on a few million "
                  "documents, with the approximation bounds verified.",
         "reqs": [
             "<b>Shingling, minhashing, and LSH implemented "
             "yourself</b> (Module 02), not from a library.",
             "<b>The Jaccard estimate's error measured against exact "
             "computation</b> on a sample, and compared to the "
             "theoretical bound.",
             "<b>The LSH parameters chosen deliberately</b>, with the "
             "S-curve plotted and the threshold justified.",
             "<b>The candidate pair count and the false positive and "
             "negative rates reported</b> at your chosen "
             "parameters.",
             "<b>A runtime comparison</b> against the exact all-pairs "
             "computation, extrapolated honestly.",
             "<b>And an inspection of fifty detected pairs</b>, with "
             "the failure categories named.",
         ],
         "done": [
             "<b>The empirical error matching the theoretical "
             "bound</b> — <b>and an explanation if it does "
             "not</b>, which is the part that demonstrates "
             "understanding.",
             "<b>The S-curve plotted and the parameters derived from "
             "it</b> rather than tuned by trial.",
             "<b>Both error rates reported</b>, because <b>reporting "
             "only recall is the standard omission</b> and it hides "
             "the trade.",
             "<b>And the fifty pairs actually inspected</b>, with "
             "categories that came from the data.",
         ]},
        {"title": "A pattern, defended", "after": 12,
         "brief": "Find a pattern in a large dataset and then attack "
                  "it until you believe it or do not.",
         "reqs": [
             "<b>A pattern found by search</b>, stated precisely, "
             "with the effect size and not only the "
             "significance.",
             "<b>The number of hypotheses you tested</b> — "
             "<b>counted, including the ones you abandoned</b> — and "
             "the correction applied (Module 11).",
             "<b>Validation on held-out data you had not "
             "touched</b>, with the result reported whichever way it "
             "came out.",
             "<b>At least three cheaper explanations tested and "
             "ruled out</b>: a confounder, a sampling artefact, and a "
             "data-collection effect.",
             "<b>A statement of what you would need to call it "
             "causal</b>, and why you do not have it.",
             "<b>And the privacy assessment</b> "
             "(Module 12) if the data concerns people.",
         ],
         "done": [
             "<b>The hypothesis count honest</b> — <b>which is "
             "graded hardest, because it is the number everyone "
             "understates</b> and the whole correction depends on "
             "it.",
             "<b>The held-out validation reported whichever way it "
             "went.</b> <b>A pattern that failed validation is a "
             "complete and passing project</b>, and a project with "
             "no failed validation is suspicious.",
             "<b>Three alternatives genuinely tested</b>, not "
             "dismissed in prose.",
             "<b>And the causal statement specific:</b> <b>naming "
             "the experiment or the instrument you would need</b> is "
             "the deliverable, not a disclaimer.",
         ]},
    ],
    "map": [
        ("Mining of Massive Datasets (free PDF, and video lectures)",
         "http://www.mmds.org/",
         "<b>Modules 02, 04, 06, 07, 09, and 10.</b> Free in full, "
         "and the chapter order is close to this course's."),
        ("Stanford CS246 (free)",
         "http://web.stanford.edu/class/cs246/",
         "<b>The same material with assignments</b> — do the "
         "LSH and the streaming ones in particular."),
        ("Tan et al. — Introduction to Data Mining (sample chapters "
         "free)",
         "https://www-users.cse.umn.edu/~kumar001/dmbook/index.php",
         "<b>Modules 03, 05, and 08</b>, and the cluster evaluation "
         "material is better here than in the primary text."),
        ("Dwork & Roth — Algorithmic Foundations of Differential "
         "Privacy (free PDF)",
         "https://www.cis.upenn.edu/~aaroth/privacybook.html",
         "<b>Module 12's formal treatment</b> — the first three "
         "chapters are what this course needs."),
        ("Ioannidis — Why Most Published Research Findings Are False "
         "(free)",
         "https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124",
         "<b>Module 11's argument, stated starkly</b> — short, "
         "and the arithmetic is the part to follow."),
        ("Public large datasets: Common Crawl, the SNAP collection, "
         "OpenStreetMap (free)",
         "https://snap.stanford.edu/data/",
         "<b>Both projects' raw material.</b> SNAP's graphs suit "
         "Module 07; Common Crawl suits Project 1."),
    ],
}

MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Two Problems, Not One",
 "subtitle": "Finding structure, and deciding whether it is there.",
 "question": "You found a pattern. Why should anyone believe it?",
 "outcomes": [
     "State the two problems and why both are necessary.",
     "Explain what scale does to algorithm choice.",
     "Explain why search guarantees a finding.",
     "Explain the kinds of pattern this course looks for.",
     "Set up a study so its findings can be defended.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The two problems",
   "blurb": "Algorithmic and statistical, and both are hard."},

  {"t": "callout", "title": "Finding candidate structure efficiently, and deciding whether it is real, are different problems",
   "kind": "The course's organisation",
   "body": ["<b>The algorithmic problem is that the data is too large "
            "for the obvious method</b> — all-pairs comparison, a "
            "full sort, or holding everything in memory — so you "
            "need an approximation with a stated bound.",
            "<b>The statistical problem is that a large search space "
            "contains apparent patterns by chance</b> — so finding "
            "one tells you about your search as much as about the "
            "world.",
            "<b>And they pull in opposite directions.</b> <b>Making "
            "the search more efficient lets you test more hypotheses, "
            "which makes the second problem worse</b> — which is why "
            "treating them separately fails.",
            "<b>So this course alternates between them "
            "deliberately</b> — and <b>Module 11 is its "
            "centre</b> rather than a late caveat, because every "
            "technique before it generates candidates that need to "
            "survive it."]},

  {"t": "table", "kicker": "Tasks", "title": "What this course looks for",
   "header": ["Task", "The question", "Module"],
   "widths": [2.8, 4.6, 3.8],
   "rows": [
     ["<b>Similar items</b>", "<b>Which records are near-duplicates?</b>", "<b>02</b>"],
     ["<b>Frequent patterns</b>", "<b>Which combinations co-occur?</b>", "<b>03</b>"],
     ["<b>Clusters</b>", "<b>Are there natural groups?</b>", "<b>04</b>"],
     ["<b>Low-dimensional structure</b>", "<b>Does it lie near a simpler space?</b>", "<b>05</b>"],
     ["<b>Stream summaries</b>", "<b>What can one pass tell you?</b>", "<b>06</b>"],
     ["<b>Graph structure</b>", "<b>Communities, and who is central?</b>", "<b>07</b>"],
     ["<b>Anomalies</b>", "<b>Which records do not belong?</b>", "<b>08</b>"],
   ],
   "footnote": "<b>Every row is unsupervised</b>, which is what makes "
               "evaluation hard throughout — there is no label "
               "saying whether the cluster or the anomaly was "
               "correct.",
   "note": "The unsupervised framing explains why evaluation recurs in "
           "every module."},

  {"t": "section", "label": "Part 2", "title": "What scale does",
   "blurb": "It changes which algorithm is correct."},

  {"t": "code", "kicker": "Scale", "title": "The thresholds at which the answer changes",
   "lang": "text", "code": """
  n = 10^3    everything works. Use the exact method.

  n = 10^6    O(n^2) is 10^12 operations -- hours to
              days. Approximation becomes attractive.

  n = 10^9    O(n^2) is impossible. O(n log n) is
              fine. The data does not fit in memory,
              so the number of PASSES matters more
              than the arithmetic.

  n = 10^12   one pass, bounded memory, distributed.
              Many exact answers are unavailable at
              any price.

  AND THE BINDING CONSTRAINT IS USUALLY NOT ARITHMETIC
      memory, because the working set must fit
      disk and network, because a pass costs more
          than the computation on it
      and random access, which is catastrophic on
          data that is not in memory

  WHICH IS WHY sequential single-pass algorithms win
  at scale even when they do more arithmetic.
""",
   "caption": "<b>Passes over the data, not operations</b>, is the "
              "right cost model once the data exceeds memory.",
   "note": "The passes-not-operations point reframes the whole "
           "course."},

  {"t": "callout", "title": "So approximation is not a compromise; it is frequently the only available answer",
   "kind": "The framing to adopt",
   "body": ["<b>An approximate answer with a stated error bound is a "
            "real result</b> — and <b>an exact answer you cannot "
            "compute is not an answer at all.</b>",
            "<b>Which is why CSCE 658 is a prerequisite:</b> "
            "<b>hashing, sampling, and concentration bounds are what let "
            "you say <i>how</i> approximate</b>, and an approximation "
            "without a bound is a guess.",
            "<b>And the bound has to be verified "
            "empirically</b> — <b>theoretical guarantees are "
            "asymptotic and assume things about your data</b> that are "
            "worth checking.",
            "<b>So the discipline is:</b> <b>choose the "
            "approximation, state the bound, then measure whether the "
            "bound holds on your data</b> — which is Project 1's "
            "requirement."]},

  {"t": "section", "label": "Part 3", "title": "Why search finds things",
   "blurb": "The problem that defines the field's honesty."},

  {"t": "eq", "kicker": "Multiplicity", "title": "The arithmetic that should govern every claim",
   "eqs": [
     ("test m independent hypotheses at level α",
      "The expected number of false positives is mα, regardless of "
      "whether any effect exists."),
     ("m = 10,000,  α = 0.05  ⟹  500 false findings",
      "In pure noise. And every one of them has p < 0.05."),
     ("P(at least one false positive) = 1 − (1−α)ᵐ",
      "Which is 0.9999… for any large m. Finding something is "
      "guaranteed."),
   ],
   "caption": "<b>With enough hypotheses, finding something "
              "significant is certain</b> — so the finding carries "
              "no information until the search is accounted for.",
   "note": "This equation is the course's moral centre; state it "
           "early."},

  {"t": "callout", "title": "And data mining searches enormous hypothesis spaces by construction",
   "kind": "Why this field has the problem worst",
   "body": ["<b>Frequent itemset mining over a thousand items "
            "considers 2¹⁰⁰⁰ candidate sets</b> — and reports the "
            "ones that pass a threshold, which is a search over an "
            "astronomical space.",
            "<b>Correlation mining over ten thousand variables tests "
            "fifty million pairs</b> — so at the five percent level, "
            "two and a half million pairs look significant with no "
            "structure at all.",
            "<b>And the searches are not independent</b>, which makes "
            "the correction harder rather than unnecessary — the "
            "naive Bonferroni bound is valid and very "
            "conservative.",
            "<b>So the field's central honesty requirement is "
            "counting the hypotheses</b> — <b>and the count is the "
            "number everybody understates</b>, including the "
            "abandoned analyses, which is Module 11 §1."]},

  {"t": "section", "label": "Part 4", "title": "Setting up to be believed",
   "blurb": "Decisions made before you look."},

  {"t": "bullets", "kicker": "Setup", "title": "What to do before the first query",
   "items": [
     "<b>Split off a validation portion and do not touch "
     "it.</b> <b>A pattern that survives data you had not seen is a "
     "different kind of evidence</b> from one found in all of "
     "it.",
     "",
     "<b>Write down what you expect to find.</b> <b>A predicted "
     "pattern confirmed is far stronger than an unpredicted one "
     "found</b>, and the record has to predate the "
     "search.",
     "",
     "<b>Keep a log of every hypothesis tested</b>, including "
     "the abandoned ones — <b>because Module 11 needs the count "
     "and it cannot be reconstructed.</b>",
     "",
     "<b>Decide the effect size that would matter</b>, in "
     "advance — which prevents a significant and useless "
     "finding from counting as a result.",
     "",
     "<b>And work out what would explain the pattern more "
     "cheaply</b>: a confounder, a sampling artefact, or how the data "
     "was collected.",
   ],
   "footnote": "<b>The hypothesis log is the cheapest of these and "
               "the one nobody keeps</b> — and without it, "
               "Module 11's correction cannot be applied honestly at "
               "all."},

  {"t": "callout", "title": "How to read this course",
   "kind": "Orientation",
   "body": ["<b>Modules 02 to 08 are the techniques</b>, each with "
            "its approximation, its bound, and its evaluation "
            "problem.",
            "<b>Modules 09 and 10 are application and "
            "scale</b> — recommendation as the worked system, and "
            "what distribution actually costs.",
            "<b>Module 11 is the centre</b>, and every technique "
            "before it produces candidates that have to pass "
            "it.",
            "<b>And Modules 12 and 13 are about the people in the "
            "data and about honest claims</b> — <b>because mining "
            "data about people has consequences for them</b>, and a "
            "found pattern is a claim about a search."]},
 ],
 "takeaways": [
   "Finding structure efficiently and deciding whether it is real are "
   "different problems that pull in opposite directions.",
   "Once data exceeds memory, passes over the data rather than operations "
   "is the right cost model.",
   "An approximate answer with a stated bound is a real result; an exact "
   "answer you cannot compute is not an answer.",
   "Testing ten thousand hypotheses at the five percent level yields five "
   "hundred findings in pure noise, each with p < 0.05.",
   "Data mining searches enormous hypothesis spaces by construction, which "
   "is why this field has the multiplicity problem worst.",
   "Keep a hypothesis log including abandoned analyses — it is the "
   "cheapest discipline here and the one nobody keeps.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The two problems"),
  ("callout", "Finding candidate structure efficiently, and deciding whether "
              "it is real, are different problems",
   ["<b>The algorithmic problem is that the data is too large for the "
    "obvious method</b> — all-pairs comparison, a full sort, holding "
    "everything in memory, or an exact count — <b>so you need an "
    "approximation with a stated bound</b> (&sect;2).",
    "<b>The statistical problem is that a large search space contains "
    "apparent patterns purely by chance</b> — so <b>finding one "
    "tells you about your search procedure at least as much as about the "
    "world</b> (&sect;3).",
    "<b>And they pull in opposite directions.</b> <b>Making the search "
    "more efficient lets you test many more hypotheses, which makes the "
    "second problem strictly worse</b> — so an advance in the first "
    "problem is a liability in the second unless it is accounted for. "
    "<b>Which is exactly why treating them separately fails.</b>",
    "<b>So this course alternates between them deliberately</b> "
    "— and <b>Module 11 is its centre rather than a late "
    "caveat</b>, because <b>every technique before it generates "
    "candidates that need to survive it</b>, and a course that taught the "
    "techniques without it would be teaching how to generate false "
    "findings efficiently."]),
  ("table", ["Task", "The question it asks", "Module"],
   [["<b>Similar items</b>",
     "<b>Which records are near-duplicates or near-neighbours?</b>",
     "<b>02</b>, with the approximation that makes it feasible."],
    ["<b>Frequent patterns</b>",
     "<b>Which combinations of items co-occur more than expected?</b>",
     "<b>03</b>"],
    ["<b>Clusters</b>",
     "<b>Are there natural groups, and how would you know?</b>",
     "<b>04</b>"],
    ["<b>Low-dimensional structure</b>",
     "<b>Does the data lie near a much simpler space?</b>",
     "<b>05</b>"],
    ["<b>Stream summaries</b>",
     "<b>What can a single pass with bounded memory tell you?</b>",
     "<b>06</b>"],
    ["<b>Graph structure</b>",
     "<b>Which nodes form communities, and which are central?</b>",
     "<b>07</b>"],
    ["<b>Anomalies</b>",
     "<b>Which records do not belong, and compared to what?</b>",
     "<b>08</b>"]],
   [0.20, 0.52, 0.28]),
  ("p", "<b>Every row is unsupervised</b>, <b>which is what makes "
        "evaluation hard throughout the course</b> — <b>there is no "
        "label telling you whether a cluster was correct or an anomaly was "
        "genuinely anomalous.</b> So each module has to construct its own "
        "answer to 'how would I know', and that recurring question is as "
        "much the course's content as the algorithms are."),

  ("h1", "2 &nbsp; What scale does"),
  ("code", """n = 10^3    everything works. Use the exact method
            and do not be clever.

n = 10^6    O(n^2) is 10^12 operations -- hours to
            days. Approximation becomes attractive.

n = 10^9    O(n^2) is impossible. O(n log n) is fine.
            The data does not fit in memory, so the
            number of PASSES matters more than the
            arithmetic does.

n = 10^12   one pass, bounded memory, distributed.
            Many exact answers are unavailable at any
            price.

AND THE BINDING CONSTRAINT IS USUALLY NOT ARITHMETIC
    memory, because the working set must fit
    disk and network, because a pass over the data
        costs more than the computation performed
        on it
    and random access, which is catastrophic on data
        that is not in memory

WHICH IS WHY sequential single-pass algorithms win at
scale even when they perform more arithmetic."""),
  ("p", "<b>Passes over the data, not operations, is the right cost "
        "model once the data exceeds memory</b> — and <b>that "
        "reframes the whole course</b>: it is why the streaming material "
        "of Module 06 is practical rather than exotic, why "
        "Module 03's algorithms are organised around pass count, and "
        "why Module 10's distributed systems care about shuffles. "
        "<b>CSCE 629's complexity analysis is still correct and is "
        "answering a question that is no longer the binding one.</b>"),
  ("callout", "So approximation is not a compromise; it is frequently the "
              "only available answer",
   ["<b>An approximate answer with a stated error bound is a real "
    "result</b> — and <b>an exact answer you cannot compute is not "
    "an answer at all</b>, which is the framing to adopt before the "
    "approximation starts feeling like a concession.",
    "<b>Which is exactly why CSCE 658 is a prerequisite rather than "
    "a recommendation:</b> <b>hashing, sampling, and concentration "
    "bounds are what let you say <i>how</i> approximate your answer "
    "is</b>, and <b>an approximation without a bound is simply a "
    "guess</b> with no claim attached.",
    "<b>And the bound has to be verified empirically.</b> "
    "<b>Theoretical guarantees are asymptotic and assume things about "
    "your data</b> — independence, a hash function's behaviour, a "
    "distribution's tails — <b>all of which are worth checking</b> "
    "rather than assuming.",
    "<b>So the discipline is:</b> <b>choose the approximation, state "
    "the bound, then measure whether the bound holds on your "
    "data</b> — which is <b>Project 1's central requirement</b> and "
    "is the habit that distinguishes using these methods from invoking "
    "them."]),

  ("break",),
  ("h1", "3 &nbsp; Why search finds things"),
  ("eq", "E[false positives] = m&alpha; &nbsp;&nbsp;&nbsp; "
         "P(at least one) = 1 &minus; (1&minus;&alpha;)<sup>m</sup>"),
  ("ul", ["<b>Test m independent hypotheses at level &alpha;</b>, and "
          "<b>the expected number of false positives is m&alpha;</b> "
          "— <b>regardless of whether any real effect exists "
          "anywhere.</b>",
          "<b>So m = 10,000 at &alpha; = 0.05 gives 500 false "
          "findings</b> in pure noise — <b>and every single one of "
          "them has p &lt; 0.05</b>, which is the whole difficulty: they "
          "are indistinguishable from real findings by the statistic "
          "alone.",
          "<b>And the probability of at least one false positive is "
          "1 &minus; (1&minus;&alpha;)<sup>m</sup></b>, which is "
          "0.9999&hellip; for any large m — <b>so finding something "
          "is not merely likely but effectively guaranteed.</b>",
          "<b>Which means the finding carries no information until the "
          "search is accounted for.</b> <b>This equation is the course's "
          "moral centre</b>, and it is stated in Module 01 rather than "
          "Module 11 because every technique in between has to be read "
          "with it in mind."]),
  ("callout", "And data mining searches enormous hypothesis spaces by "
              "construction",
   ["<b>Frequent itemset mining over a thousand items considers "
    "2<sup>1000</sup> candidate sets</b> in principle — and reports "
    "whichever ones pass a support threshold, <b>which is a search over "
    "an astronomically large space</b> conducted on your behalf by the "
    "algorithm (Module 03).",
    "<b>Correlation mining over ten thousand variables tests "
    "approximately fifty million pairs</b> — so <b>at the five "
    "percent level, two and a half million pairs look significant with no "
    "structure in the data at all</b>, and the top of that list looks "
    "extremely compelling.",
    "<b>And the searches are not independent</b>, which <b>makes the "
    "correction harder rather than unnecessary</b> — the naive "
    "Bonferroni bound remains valid and becomes very conservative, and "
    "Module 11 &sect;2's methods exist to do better.",
    "<b>So the field's central honesty requirement is counting the "
    "hypotheses</b> — and <b>the count is the number everybody "
    "understates</b>, because <b>it includes the analyses you abandoned, "
    "the parameters you tried, and the preprocessing choices you "
    "made</b>, all of which were hypothesis tests whether or not you "
    "recorded them (Module 11 &sect;1)."]),

  ("h1", "4 &nbsp; Setting up to be believed"),
  ("ul", ["<b>Split off a validation portion and do not touch "
          "it.</b> <b>A pattern that survives data you had not seen when "
          "you found it is a categorically different kind of "
          "evidence</b> from one found in all of the data — and the "
          "split has to happen first.",
          "<b>Write down what you expect to find.</b> <b>A predicted "
          "pattern confirmed is far stronger evidence than an unpredicted "
          "one found</b>, because the prediction fixed the hypothesis "
          "count at one — <b>and the record has to predate the "
          "search</b> to mean anything.",
          "<b>Keep a log of every hypothesis tested</b>, including the "
          "abandoned ones, the parameter sweeps, and the alternative "
          "preprocessing — <b>because Module 11 needs the count "
          "and it genuinely cannot be reconstructed afterwards</b> from "
          "memory or from the notebook.",
          "<b>Decide in advance what effect size would actually "
          "matter</b> — which <b>prevents a statistically "
          "significant and practically useless finding from counting as a "
          "result</b>, a failure mode that large n makes near-certain "
          "(Module 11 &sect;3).",
          "<b>And work out in advance what would explain the pattern "
          "more cheaply:</b> a confounder, a sampling artefact, or "
          "something about how the data was collected. <b>The hypothesis "
          "log is the cheapest of these five and the one nobody "
          "keeps</b> — and <b>without it, Module 11's correction "
          "cannot be applied honestly at all</b>, which makes everything "
          "downstream unverifiable."]),
  ("callout", "How to read this course",
   ["<b>Modules 02 to 08 are the techniques</b>, and each one comes "
    "with three things: <b>its approximation, the bound on that "
    "approximation, and its evaluation problem</b> — which is the "
    "pattern to look for in each.",
    "<b>Modules 09 and 10 are application and scale</b> — "
    "recommendation as the worked end-to-end system, and what "
    "distribution actually costs once you stop assuming it is free.",
    "<b>Module 11 is the centre</b>, and <b>every technique before "
    "it produces candidates that have to pass it</b> — so it is "
    "worth reading its first section early and returning to it.",
    "<b>And Modules 12 and 13 are about the people in the data and "
    "about honest claims</b> — <b>because mining data about people "
    "has consequences for those people</b>, and <b>a found pattern is a "
    "claim about a search procedure</b> rather than about the world, "
    "until the work in Module 11 has been done."]),
 ],
 "resources": [
   ("Mining of Massive Datasets, chapter 1 (free)",
    "http://www.mmds.org/",
    "<b>&sect;1 through &sect;3</b> — and its section on "
    "'bonferroni's principle' is this course's &sect;3, stated by the "
    "authors with a memorable example."),
   ("Ioannidis &mdash; Why Most Published Research Findings Are False "
    "(free)",
    "https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124",
    "<b>&sect;3's argument with the arithmetic</b> — short, and it "
    "changed how several fields report results."),
   ("Simmons, Nelson & Simonsohn &mdash; False-Positive Psychology "
    "(free)",
    "https://journals.sagepub.com/doi/10.1177/0956797611417632",
    "<b>&sect;4's motivation</b> — how ordinary analytic flexibility "
    "produces significant findings from nothing."),
   ("Stanford CS246, lecture 1 (free)",
    "http://web.stanford.edu/class/cs246/",
    "<b>&sect;2's scale thresholds</b>, with the cost model argued "
    "concretely."),
 ],
 "exercises": [
   "<b>State the two problems</b> and explain how an improvement in one "
   "worsens the other.",
   "<b>Compute the operation count</b> for all-pairs comparison at a "
   "million and a billion records.",
   "<b>Time a single sequential pass</b> over a large file and compare "
   "against random access over the same data.",
   "<b>Generate pure noise with 10,000 variables</b> and count the pairs "
   "with p < 0.05.",
   "<b>Report the most significant one</b> and note how compelling it "
   "looks.",
   "<b>Compute the probability of at least one false positive</b> for "
   "m = 100, 10,000, and 10 million.",
   "<b>Count the candidate itemsets</b> over 1,000 items.",
   "<b>Split a dataset into exploration and validation</b>, and write "
   "down your predictions before looking.",
   "<b>Start a hypothesis log</b> and commit to it for the "
   "semester.",
   "<b>Write down three cheaper explanations</b> for a pattern you "
   "expect to find.",
 ],
 "selfcheck": [
   "State the two problems and why they pull in opposite directions.",
   "Why is Module 11 the centre rather than a caveat?",
   "Name seven tasks and say what they have in common.",
   "What is the right cost model above memory size, and why?",
   "Why is approximation not a compromise?",
   "Why must a bound be verified empirically?",
   "Give the multiplicity arithmetic and what it implies.",
   "Why does data mining have this problem worst?",
   "Give five things to do before the first query.",
   "Which is cheapest, and why does its absence break everything "
   "downstream?",
 ],
},

]

for _b in ("c676_b2", "c676_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
