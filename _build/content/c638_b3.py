# -*- coding: utf-8 -*-
"""CSCE 638 — Modules 09-13."""

MODULES = [

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Generation and Decoding",
 "subtitle": "The model gives a distribution. You still have to choose.",
 "question": "Why does the same model produce different quality text?",
 "outcomes": [
     "Explain the decoding strategies and their trade.",
     "Explain why the most likely sequence is not the best "
     "output.",
     "Explain the degeneration failure and its cause.",
     "Explain constrained and structured generation.",
     "Choose a strategy for a stated requirement.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The choice",
   "blurb": "Which is separate from the model."},

  {"t": "callout", "title": "The model gives P(next token). Decoding is a separate algorithm with its own behaviour.",
   "kind": "The distinction that is frequently missed",
   "body": ["<b>A language model outputs a distribution at each "
            "step</b> — and <b>turning a sequence of distributions "
            "into one sequence of text requires a search or a sampling "
            "procedure</b>, which is a design decision independent of "
            "the model.",
            "<b>So two systems with the identical model can differ "
            "substantially in output quality</b> — and reports that "
            "omit the decoding configuration are not "
            "reproducible.",
            "<b>And the right strategy depends on the task.</b> <b>A "
            "translation wants the single best rendering; a story wants "
            "variety</b> — and no single setting serves "
            "both.",
            "<b>Which makes decoding a parameter of your system "
            "rather than a detail</b> — and one of the few places "
            "where a large quality change costs no training "
            "whatsoever."]},

  {"t": "code", "kicker": "Strategies", "title": "The strategies, and what each does",
   "lang": "text", "code": """
  GREEDY      take the argmax at every step.
              Deterministic, fast, and myopic -- one
              early mistake is unrecoverable.

  BEAM SEARCH keep the k best partial sequences.
              Better for tasks with one right answer.
              Needs length normalisation, or it
              prefers short outputs.

  SAMPLING    draw from the distribution. Diverse,
              and it occasionally draws something
              absurd from the tail.

  TOP-k       sample from the k most likely tokens.
              Fixed k is wrong when the distribution
              is very peaked or very flat.

  TOP-p       sample from the smallest set whose
              probability mass exceeds p. Adapts to
              the distribution's shape, which is why
              it displaced top-k.

  TEMPERATURE scales the logits before the softmax.
              Low -> sharper, high -> flatter.
              Orthogonal to the above.
""",
   "caption": "<b>Top-p adapts to the distribution's shape</b> — "
              "which is exactly the property fixed-k lacks, and the "
              "reason it won.",
   "note": "The adapts-to-shape argument is what makes top-p make "
           "sense."},

  {"t": "section", "label": "Part 2", "title": "The likelihood trap",
   "blurb": "Why maximising probability produces bad text."},

  {"t": "callout", "title": "The most likely sequence is repetitive and dull, which is a real and surprising result",
   "kind": "Why pure search fails for open-ended generation",
   "body": ["<b>Increasing the beam width past a modest size makes "
            "output <i>worse</i> on open-ended tasks</b> — which is "
            "backwards if you believe the model's probability is a "
            "quality score.",
            "<b>And the explanation is that human text is not the "
            "maximum of the distribution it came from.</b> <b>People "
            "produce surprising text; the mode is bland</b>, and "
            "high-probability continuations include degenerate loops.",
            "<b>So repetition is the characteristic "
            "failure:</b> <b>once a phrase repeats, its probability "
            "rises, which makes repeating it again more likely</b> "
            "— a positive feedback loop in the decoding, not in the "
            "model.",
            "<b>Which is why sampling-based methods win for "
            "open-ended text</b> and <b>beam search still wins for "
            "translation</b> — <b>because translation genuinely does "
            "have one right answer</b>, so the mode is the target."]},

  {"t": "bullets", "kicker": "Repetition", "title": "And the fixes, with their costs",
   "items": [
     "<b>Sampling with top-p</b>, which avoids the mode "
     "entirely — the standard answer for open-ended "
     "text.",
     "",
     "<b>A repetition penalty</b>, which reduces the probability "
     "of already-used tokens — <b>effective and crude</b>, since "
     "some repetition is correct.",
     "",
     "<b>Blocking repeated n-grams</b>, which is cruder still and "
     "<b>breaks legitimately repeated names and "
     "terms.</b>",
     "",
     "<b>And contrastive methods</b>, which penalise tokens that "
     "are too similar to the recent context — better quality for "
     "more computation.",
     "",
     "<b>Note that all four are decoding-time fixes to a "
     "decoding-time problem</b>, which is why none requires "
     "retraining.",
   ],
   "footnote": "<b>The repetition penalty's crudeness is worth "
               "stating:</b> it also penalises the correct repetition of "
               "a proper noun, which produces its own characteristic "
               "errors."},

  {"t": "section", "label": "Part 3", "title": "Structured output",
   "blurb": "When the output must parse."},

  {"t": "callout", "title": "Constrained decoding makes invalid output impossible rather than unlikely",
   "kind": "The right answer when the format matters",
   "body": ["<b>If the output must be valid JSON, matching a schema, "
            "or drawn from a fixed set, enforce it during "
            "decoding</b> — by masking the tokens that would make "
            "the output invalid at each step.",
            "<b>Which is strictly better than generating and then "
            "validating</b> — <b>a retry loop is slower, sometimes "
            "unbounded, and silently biases toward whatever the model "
            "happens to produce.</b>",
            "<b>And it is the same argument as CSCE 713 "
            "Module 10 §2's:</b> <b>make the invalid state "
            "unrepresentable rather than detecting it "
            "afterwards.</b>",
            "<b>With one caveat worth measuring:</b> <b>constraining "
            "the output can degrade content quality</b>, because the "
            "model is pushed off its preferred distribution — so "
            "compare against the unconstrained version."]},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "By what the task requires."},

  {"t": "table", "kicker": "Choosing", "title": "Strategy by requirement",
   "header": ["Requirement", "Use", "Why"],
   "widths": [3.0, 3.6, 5.3],
   "rows": [
     ["<b>One correct answer</b>", "<b>Beam search</b>", "<b>The mode is the target (translation, parsing)</b>"],
     ["<b>Open-ended text</b>", "<b>Top-p sampling</b>", "<b>The mode is degenerate (Part 2)</b>"],
     ["<b>Determinism required</b>", "<b>Greedy, or temperature 0</b>", "<b>Reproducibility, at a quality cost</b>"],
     ["<b>Valid structure</b>", "<b>Constrained decoding</b>", "<b>Invalid output made impossible (Part 3)</b>"],
     ["<b>Diversity wanted</b>", "<b>Higher temperature or p</b>", "<b>And measure the quality cost</b>"],
   ],
   "footnote": "<b>Report your decoding configuration with every "
               "result</b> — it is as much a part of the system as "
               "the model weights, and omitting it makes a number "
               "unreproducible.",
   "note": "The reporting requirement is the module's practical "
           "demand."},

  {"t": "callout", "title": "And the thing to measure",
   "kind": "Closing",
   "body": ["<b>Sweep temperature and p against your task "
            "metric</b> — <b>the curve is usually non-monotonic with "
            "a clear best region</b>, and finding it costs an hour and "
            "no training.",
            "<b>Measure variance, not only the mean.</b> <b>A "
            "sampling strategy produces a distribution of "
            "outputs</b>, and reporting one sample's score is "
            "reporting a draw rather than a system.",
            "<b>And measure the failure rate separately</b> — "
            "<b>repetition, truncation, and invalid format are different "
            "failures</b> and respond to different fixes.",
            "<b>Which is the cheapest available quality "
            "improvement in this course</b> — <b>no training, no "
            "data, and frequently a larger effect than a model "
            "upgrade.</b>"]},
 ],
 "takeaways": [
   "Decoding is an algorithm separate from the model, so two systems with "
   "the same weights can differ substantially in output quality.",
   "Top-p adapts to the distribution's shape, which is the property "
   "fixed-k lacks and the reason it won.",
   "The most likely sequence is repetitive and dull, because human text is "
   "not the maximum of the distribution it came from.",
   "Repetition is a positive feedback loop in the decoding rather than a "
   "flaw in the model, which is why decoding-time fixes work.",
   "Constrained decoding makes invalid output impossible, which beats "
   "generate-and-retry — and can degrade content quality, so measure "
   "it.",
   "Report your decoding configuration with every result; it is as much "
   "part of the system as the weights.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The choice"),
  ("callout", "The model gives P(next token). Decoding is a separate "
              "algorithm with its own behaviour.",
   ["<b>A language model outputs a probability distribution at each "
    "step</b> — and <b>turning a sequence of distributions into one "
    "concrete sequence of text requires a search or sampling "
    "procedure</b>, which is a design decision entirely independent of "
    "the model's parameters.",
    "<b>So two systems using the identical model can differ "
    "substantially in output quality</b> — and <b>any report that "
    "omits the decoding configuration is not reproducible</b>, which "
    "makes a surprising fraction of published generation comparison "
    "ambiguous.",
    "<b>And the right strategy depends entirely on the task.</b> <b>A "
    "translation wants the single best rendering; a story wants "
    "variety</b> — and <b>no single setting serves both</b>, which "
    "is &sect;2's subject and is a real tension rather than a tuning "
    "problem.",
    "<b>Which makes decoding a parameter of your system rather than an "
    "implementation detail</b> — and <b>one of the very few places "
    "where a large quality change costs no training whatsoever</b>, "
    "which is why &sect;4 ends on measuring it."]),
  ("code", """GREEDY      take the argmax at every step.
            Deterministic, fast, and myopic -- one
            early mistake is unrecoverable.

BEAM SEARCH keep the k best partial sequences.
            Better for tasks with one right answer.
            Needs length normalisation, or it prefers
            short outputs (shorter sequences have
            higher probability).

SAMPLING    draw from the distribution. Diverse, and
            it occasionally draws something absurd
            from the long tail.

TOP-k       sample from the k most likely tokens.
            A fixed k is wrong when the distribution
            is very peaked or very flat.

TOP-p       sample from the smallest set whose
            cumulative probability exceeds p. Adapts
            to the distribution's shape, which is why
            it displaced top-k.

TEMPERATURE scales the logits before the softmax.
            Low -> sharper, high -> flatter.
            Orthogonal to all of the above."""),
  ("p", "<b>Top-p adapts to the distribution's shape</b> — when the "
        "model is confident the set is small, and when it is uncertain the "
        "set is large — <b>which is exactly the property a fixed k "
        "lacks</b>, and <b>is the reason it won</b>. <b>The "
        "length-normalisation point about beam search is worth "
        "remembering</b>: without it, beam search systematically prefers "
        "short outputs, because every additional token multiplies the "
        "probability by something less than one, and this produces "
        "truncated translations in a way that looks like a model failure."),

  ("h1", "2 &nbsp; The likelihood trap"),
  ("callout", "The most likely sequence is repetitive and dull, which is a "
              "real and surprising result",
   ["<b>Increasing the beam width past a fairly modest size makes "
    "output <i>worse</i> on open-ended tasks</b> — which is exactly "
    "backwards if you believe the model's probability is a quality score, "
    "and it is a reliably reproducible finding.",
    "<b>And the explanation is that human text is not the maximum of "
    "the distribution it came from.</b> <b>People produce surprising, "
    "informative text; the mode of the distribution is bland</b>, and "
    "the highest-probability continuations include outright degenerate "
    "loops that no human would write.",
    "<b>So repetition is the characteristic failure, and its mechanism "
    "is specific:</b> <b>once a phrase has repeated, its probability "
    "rises, which makes repeating it again more likely still</b> — "
    "<b>a positive feedback loop in the <i>decoding</i>, not in the "
    "model</b>, which is why the fixes are all decoding-time.",
    "<b>Which is why sampling-based methods win for open-ended "
    "text</b> and <b>beam search still wins decisively for "
    "translation</b> — <b>because translation genuinely does have "
    "approximately one right answer</b>, so the mode <i>is</i> the "
    "target and searching for it is correct."]),
  ("ul", ["<b>Sampling with top-p</b>, which avoids the mode "
          "entirely — <b>the standard answer for open-ended "
          "text</b>, and the first thing to try.",
          "<b>A repetition penalty</b>, which reduces the probability "
          "of tokens already used — <b>effective and crude</b>, "
          "since <b>some repetition is correct</b>: a proper noun, a "
          "technical term, or a deliberate refrain.",
          "<b>Blocking repeated n-grams</b> outright, which is cruder "
          "still and <b>breaks legitimately repeated names and "
          "terms</b> — usable for short outputs and a poor idea for "
          "long ones.",
          "<b>And contrastive methods</b>, which penalise tokens whose "
          "representations are too similar to the recent context — "
          "<b>better quality for more computation</b>, and a more "
          "principled version of the same idea.",
          "<b>Note that all four are decoding-time fixes to a "
          "decoding-time problem</b>, <b>which is why none of them "
          "requires retraining</b> — and is the clearest "
          "demonstration that &sect;1's separation is a real one. "
          "<b>The repetition penalty's crudeness is worth stating "
          "explicitly</b>, because it produces its own characteristic "
          "errors that are easy to misattribute to the model."]),

  ("break",),
  ("h1", "3 &nbsp; Structured output"),
  ("callout", "Constrained decoding makes invalid output impossible rather "
              "than unlikely",
   ["<b>If the output must be valid JSON, must match a schema, or must "
    "be drawn from a fixed set of options, enforce that during "
    "decoding</b> — by masking out, at each step, every token that "
    "would make the output invalid or unparseable.",
    "<b>Which is strictly better than generating and then "
    "validating</b> — <b>a retry loop is slower, is sometimes "
    "unbounded, and silently biases the output distribution toward "
    "whatever the model happens to produce validly</b>, which is a bias "
    "nobody chose and nobody measures.",
    "<b>And it is precisely the same argument as CSCE 713 "
    "Module 10 &sect;2's:</b> <b>make the invalid state "
    "unrepresentable rather than detecting it after the fact</b> — "
    "and <b>CSCE 713 Module 04 &sect;4's parse-don't-validate</b>, "
    "arriving in a generation setting. <b>Three courses, one "
    "principle.</b>",
    "<b>With one caveat worth measuring rather than assuming "
    "away:</b> <b>constraining the output can degrade content "
    "quality</b>, because the model is being pushed off its preferred "
    "distribution and may have no good continuation within the permitted "
    "set — <b>so compare against the unconstrained version on "
    "content, not only on validity.</b>"]),

  ("h1", "4 &nbsp; Choosing, and measuring"),
  ("table", ["The requirement", "Use", "Why"],
   [["<b>One correct answer exists</b>",
     "<b>Beam search</b>, with length normalisation.",
     "<b>The mode is the target</b> — translation, parsing, "
     "structured extraction."],
    ["<b>Open-ended text</b>", "<b>Top-p sampling</b>.",
     "<b>The mode is degenerate</b> (&sect;2), so searching for it "
     "actively hurts."],
    ["<b>Determinism required</b>",
     "<b>Greedy, or temperature 0</b>.",
     "<b>Reproducibility, at a real quality cost</b> — and worth it "
     "when the output feeds another system."],
    ["<b>Output must parse</b>", "<b>Constrained decoding</b>.",
     "<b>Invalid output made impossible</b> (&sect;3), rather than "
     "merely unlikely."],
    ["<b>Diversity wanted</b>",
     "<b>Higher temperature, or higher p</b>.",
     "<b>And measure the quality cost</b>, which is real and "
     "non-linear."]],
   [0.22, 0.26, 0.52]),
  ("p", "<b>Report your decoding configuration with every "
        "result</b> — strategy, temperature, p or k, length penalty, "
        "and repetition penalty. <b>It is as much a part of the system as "
        "the model weights are</b>, and <b>omitting it makes a number "
        "unreproducible</b> in a way that is entirely avoidable. "
        "<b>Module 13 &sect;2 treats this as part of an honest "
        "claim.</b>"),
  ("callout", "And the thing to measure",
   ["<b>Sweep temperature and p against your actual task "
    "metric</b> — <b>the curve is usually non-monotonic with a "
    "fairly clear best region</b>, and <b>finding it costs an hour and "
    "no training at all.</b>",
    "<b>Measure variance, not only the mean.</b> <b>A sampling "
    "strategy produces a <i>distribution</i> of outputs</b>, so "
    "<b>reporting one sample's score is reporting a draw rather than a "
    "system</b> — run it several times and report the spread "
    "(Module 10 &sect;1).",
    "<b>And measure the failure modes separately</b> — "
    "<b>repetition, premature truncation, and invalid format are "
    "different failures</b> with different causes and different fixes, "
    "and an aggregate quality score hides all three.",
    "<b>Which is the cheapest available quality improvement in this "
    "entire course</b> — <b>no training, no data, no new "
    "model</b> — and <b>frequently a larger effect than upgrading "
    "to a bigger model would produce</b>, which makes skipping it an "
    "expensive habit."]),
 ],
 "resources": [
   ("Holtzman et al. &mdash; The Curious Case of Neural Text "
    "Degeneration (free)",
    "https://arxiv.org/abs/1904.09751",
    "<b>&sect;2 in the original</b>, and the paper that introduced "
    "top-p — the human-text-is-not-the-mode argument is made with "
    "data."),
   ("Jurafsky & Martin, the decoding sections (free)",
    "https://web.stanford.edu/~jurafsky/slp3/",
    "<b>&sect;1's strategies</b>, with beam search and length "
    "normalisation done carefully."),
   ("Welleck et al. &mdash; Neural Text Degeneration with Unlikelihood "
    "Training (free)",
    "https://arxiv.org/abs/1908.04319",
    "<b>&sect;2's repetition problem attacked at training time "
    "instead</b> — a useful contrast with the decoding-time "
    "fixes."),
   ("The guidance and outlines libraries (free)",
    "https://github.com/dottxt-ai/outlines",
    "<b>&sect;3 as working code</b> — grammar-constrained decoding "
    "you can use today."),
 ],
 "exercises": [
   "<b>Generate from one model with greedy, beam, and top-p</b> and "
   "compare the outputs.",
   "<b>Increase the beam width</b> on an open-ended prompt and observe "
   "the quality.",
   "<b>Remove length normalisation</b> from beam search and report what "
   "happens to the output length.",
   "<b>Produce a repetition loop</b> and trace the probability of the "
   "repeated phrase as it goes.",
   "<b>Fix it four ways</b> and compare the side effects of each.",
   "<b>Show the repetition penalty breaking a repeated proper "
   "noun.</b>",
   "<b>Implement constrained decoding</b> for a small JSON schema.",
   "<b>Compare constrained against generate-and-retry</b> on latency and "
   "on content quality.",
   "<b>Sweep temperature against your task metric</b> and find the best "
   "region.",
   "<b>Report the variance</b> across ten samples at your chosen "
   "setting.",
 ],
 "selfcheck": [
   "Why is decoding separate from the model, and what follows for "
   "reporting?",
   "Name six strategies and what each does.",
   "Why did top-p displace top-k?",
   "Why does beam search prefer short outputs without normalisation?",
   "Why is the most likely sequence bad for open-ended text?",
   "Give the mechanism of the repetition loop.",
   "Why does beam search still win for translation?",
   "Give four repetition fixes and the cost of the crudest.",
   "Why is constrained decoding better than generate-and-validate, and "
   "what is the caveat?",
   "What three things should you measure?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Evaluation",
 "subtitle": "The hard part, and usually the weakest part.",
 "question": "Does your number mean what you think it means?",
 "outcomes": [
     "Design an evaluation from the decision it supports.",
     "Choose and justify a baseline.",
     "Explain why generation metrics mislead.",
     "Explain benchmark contamination and leakage.",
     "Run an error analysis that changes decisions.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "From the decision",
   "blurb": "Backwards, like Module 01's logging."},

  {"t": "callout", "title": "Start from what someone will do differently, and derive the metric from that",
   "kind": "The design direction",
   "body": ["<b>A metric chosen because it is standard measures what "
            "was convenient to measure</b> — which may correlate with "
            "what you care about, and the correlation is an empirical "
            "claim rather than an assumption.",
            "<b>So ask: what decision does this output "
            "support?</b> <b>If a person will read the top three "
            "results, measure the top three; if a system will act "
            "automatically on one, measure precision at one.</b>",
            "<b>And the error costs are usually asymmetric.</b> <b>A "
            "false positive and a false negative rarely cost the "
            "same</b>, so a single accuracy number averages over a "
            "distinction that matters.",
            "<b>Which is CSCE 633 §12's "
            "choose-the-metric-from-the-use argument</b> — and "
            "<b>CSCE 701 Module 09 §1's design-backwards "
            "direction</b>, applied to measurement."]},

  {"t": "bullets", "kicker": "Splits", "title": "And the splits, which determine whether the number means anything",
   "items": [
     "<b>Look at the test set once.</b> <b>Every look is a "
     "decision informed by it</b>, and after a dozen looks you have "
     "fitted the test set with your own judgement.",
     "",
     "<b>Split by the unit you will generalise over</b> — "
     "<b>by document, user, or time, not by sentence</b>, if sentences "
     "from one document would otherwise span the "
     "split.",
     "",
     "<b>And split by time if your data is temporal</b>, because a "
     "random split lets the model see the future "
     "(CSCE 633 §11).",
     "",
     "<b>Check for near-duplicates across splits</b>, which are "
     "extremely common in scraped text and inflate every "
     "score.",
     "",
     "<b>And report the confidence interval</b>, because a "
     "difference of half a point on a thousand examples is "
     "noise.",
   ],
   "footnote": "<b>Near-duplicate leakage is the one that silently "
               "ruins text experiments</b> — web-derived corpora are "
               "full of reposted and templated content, and a hash check "
               "is not enough."},

  {"t": "section", "label": "Part 2", "title": "Baselines",
   "blurb": "Which is where most claims fail."},

  {"t": "code", "kicker": "Baselines", "title": "The baselines you must beat",
   "lang": "text", "code": """
  MAJORITY CLASS
      the single most common label. On a skewed task
      this is embarrassingly strong, and reporting
      accuracy without it is uninformative.

  RANDOM, AND HUMAN AGREEMENT
      the floor and a realistic ceiling. If annotators
      agree only 80% of the time, 85% accuracy is not
      obviously improvable.

  LEXICAL / RETRIEVAL
      TF-IDF or BM25 plus logistic regression. Cheap,
      and it beats a surprising number of published
      neural systems (CSCE 670).

  EMBEDDINGS + LOGISTIC REGRESSION
      Module 04 section 4's baseline. One hour.

  THE PREVIOUS SIMPLEST THING
      whatever the system you are replacing does,
      measured on the same split

  AND A SHORTCUT CHECK: train on a corrupted version
  of the input (shuffled words, labels only, the
  question without the passage). If it still scores
  well, the task has an artefact.
""",
   "caption": "<b>The shortcut check is the most informative single "
              "experiment here</b> — it tells you whether your "
              "benchmark measures the ability you named.",
   "note": "The input-ablation check has invalidated several famous "
           "benchmarks."},

  {"t": "callout", "title": "A system that beats a strawman has established nothing",
   "kind": "The requirement, and why it is resisted",
   "body": ["<b>The baseline has to be the best cheap alternative, "
            "tuned with the same effort as your system</b> — and "
            "<b>an untuned baseline against a tuned system is not a "
            "comparison.</b>",
            "<b>Which is resisted because a strong baseline sometimes "
            "wins</b> — and that is a result worth having, since it "
            "saves the cost of the complicated system.",
            "<b>And the replication literature is "
            "unambiguous:</b> <b>a substantial share of reported gains "
            "disappear when baselines are tuned equally</b>, across "
            "several subfields.",
            "<b>So Project 2 grades the baseline first</b> — "
            "<b>because an unbeaten strong baseline is a finding and a "
            "beaten weak one is not.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Generation metrics",
   "blurb": "Where the measurement is genuinely unsolved."},

  {"t": "table", "kicker": "Metrics", "title": "The generation metrics, and what each misses",
   "header": ["Metric", "Measures", "Misses"],
   "widths": [2.6, 3.9, 5.1],
   "rows": [
     ["<b>BLEU</b>", "<b>N-gram overlap with references</b>", "<b>Any correct paraphrase; meaning entirely</b>"],
     ["<b>ROUGE</b>", "<b>Overlap, recall-oriented</b>", "<b>The same, plus factual correctness</b>"],
     ["<b>BERTScore</b>", "<b>Embedding similarity to references</b>", "<b>Factuality; and it inherits the model's biases</b>"],
     ["<b>Perplexity</b>", "<b>Model fit</b>", "<b>Usefulness (M03 §3)</b>"],
     ["<b>LLM-as-judge</b>", "<b>Another model's preference</b>", "<b>Calibration; and it prefers its own style</b>"],
     ["<b>Human rating</b>", "<b>What a rater thought</b>", "<b>Consistency, unless the protocol is tight</b>"],
   ],
   "footnote": "<b>Every row misses factual correctness</b>, which for "
               "most real applications is the thing that matters — "
               "and that gap is why generation evaluation is still an "
               "open problem.",
   "note": "The all-miss-factuality observation is the honest "
           "summary."},

  {"t": "callout", "title": "The judge-model problem deserves naming",
   "kind": "A specific caution about a popular method",
   "body": ["<b>Using a strong model to score outputs is cheap, fast, "
            "and correlates with human judgement better than overlap "
            "metrics do</b> — which is why it spread quickly, and the "
            "correlation is real.",
            "<b>And it has specific biases:</b> <b>a preference for "
            "longer answers, for its own stylistic conventions, and for "
            "the first option presented</b> — all measured, and all "
            "correctable only partially.",
            "<b>Which means it cannot evaluate a competitor "
            "fairly</b> if that competitor writes differently — and "
            "<b>it certainly cannot evaluate factuality it does not "
            "itself know.</b>",
            "<b>So use it for development and triage, calibrate it "
            "against human judgement on a sample, and report that "
            "calibration</b> — which almost nobody does and which is "
            "what would make the method trustworthy."]},

  {"t": "section", "label": "Part 4", "title": "Error analysis",
   "blurb": "The step that changes decisions."},

  {"t": "bullets", "kicker": "Analysis", "title": "How to do it so it is worth the time",
   "items": [
     "<b>Read at least twenty errors individually</b>, with the "
     "input, the prediction, and the correct answer side by "
     "side.",
     "",
     "<b>Let the categories come from the data</b>, not from your "
     "expectations — <b>which is the whole point, and the step "
     "people skip by starting with a taxonomy.</b>",
     "",
     "<b>Count the categories</b>, so you know which is worth "
     "fixing — and <b>the distribution is usually much more "
     "skewed than anticipated.</b>",
     "",
     "<b>Check the labels while you are there</b>, because <b>a "
     "meaningful fraction of 'errors' are annotation "
     "mistakes</b> in most datasets.",
     "",
     "<b>And look at the <i>confident</i> errors "
     "specifically</b>, which are the dangerous ones and the most "
     "diagnostic.",
   ],
   "footnote": "<b>Reading twenty errors is a better use of an hour "
               "than any hyperparameter sweep</b> — and it is the "
               "only method that finds a mislabelled test set."},

  {"t": "callout", "title": "And benchmark contamination",
   "kind": "Closing",
   "body": ["<b>A pretrained model may have seen your test set</b>, "
            "because it was trained on a crawl of the web and your "
            "benchmark is published on the web.",
            "<b>Which inflates scores in a way that is hard to "
            "detect</b> and impossible to rule out without access to the "
            "training data — <b>which you generally do not "
            "have.</b>",
            "<b>So prefer a test set you constructed, from data after "
            "the training cutoff</b>, or at minimum check for verbatim "
            "overlap and report what you checked.",
            "<b>And treat public benchmark scores as weak "
            "evidence</b> — <b>the ranking may reflect exposure "
            "rather than capability</b>, and your own held-out data is "
            "worth more than a leaderboard position."]},
 ],
 "takeaways": [
   "Derive the metric from the decision the output supports, because a "
   "standard metric measures what was convenient to measure.",
   "Split by the unit you generalise over, and check for near-duplicates "
   "— which silently ruin text experiments.",
   "Train on corrupted input: if the score holds up, the task has an "
   "artefact rather than requiring the ability you named.",
   "A substantial share of reported gains disappear when baselines are "
   "tuned equally, so an unbeaten strong baseline is a finding.",
   "Every generation metric misses factual correctness, which is the thing "
   "that matters for most applications.",
   "Reading twenty errors is a better use of an hour than any "
   "hyperparameter sweep, and it is the only way to find a mislabelled "
   "test set.",
 ],
 "notes": [
  ("h1", "1 &nbsp; From the decision"),
  ("callout", "Start from what someone will do differently, and derive the "
              "metric from that",
   ["<b>A metric chosen because it is standard measures what was "
    "convenient to measure</b> — which may correlate with what you "
    "care about, <b>and the correlation is an empirical claim rather than "
    "an assumption you are entitled to make.</b>",
    "<b>So ask: what decision does this output support?</b> <b>If a "
    "person will read the top three results, measure the top three; if a "
    "system will act automatically on the single top answer, measure "
    "precision at one</b> — and those two systems should be "
    "optimised differently.",
    "<b>And the error costs are almost always asymmetric.</b> <b>A "
    "false positive and a false negative rarely cost the same thing</b>, "
    "so <b>a single accuracy number averages over a distinction that "
    "determines whether the system is usable</b>.",
    "<b>Which is CSCE 633 Module 12's "
    "choose-the-metric-from-the-use argument</b> — and <b>CSCE 701 "
    "Module 09 &sect;1's design-backwards direction</b>, applied to "
    "measurement rather than to logging. <b>Three courses, one "
    "direction of reasoning.</b>"]),
  ("ul", ["<b>Look at the test set once.</b> <b>Every look is a "
          "decision informed by it</b> — which architecture, which "
          "hyperparameters, which preprocessing — and <b>after a "
          "dozen looks you have fitted the test set with your own "
          "judgement</b> as surely as gradient descent would have.",
          "<b>Split by the unit you will generalise over</b> — "
          "<b>by document, by user, or by time, rather than by "
          "sentence</b>, if sentences from a single document would "
          "otherwise appear on both sides of the split and leak.",
          "<b>And split by time if your data is temporal</b>, because "
          "<b>a random split lets the model see the future</b> "
          "(CSCE 633 Module 11) — which is the commonest "
          "serious leak in applied work and makes a system look far "
          "better than it will be.",
          "<b>Check for near-duplicates across the splits</b>, which "
          "are <b>extremely common in scraped text</b> and inflate every "
          "score — reposted articles, templated pages, and "
          "boilerplate. <b>This is the one that silently ruins text "
          "experiments</b>, and <b>an exact-hash check is not "
          "enough</b>; you need near-duplicate detection "
          "(CSCE 676).",
          "<b>And report a confidence interval</b>, because <b>a "
          "difference of half a point on a thousand examples is "
          "noise</b> — and a great deal of reported improvement is "
          "within the interval that was not computed."]),

  ("h1", "2 &nbsp; Baselines"),
  ("code", """MAJORITY CLASS
    the single most common label. On a skewed task
    this is embarrassingly strong, and reporting
    accuracy without it is uninformative.

RANDOM, AND HUMAN AGREEMENT
    the floor and a realistic ceiling. If annotators
    agree with each other only 80% of the time, then
    85% accuracy is not obviously improvable.

LEXICAL / RETRIEVAL
    TF-IDF or BM25 plus logistic regression. Cheap,
    and it beats a surprising number of published
    neural systems (CSCE 670 Module 03).

EMBEDDINGS + LOGISTIC REGRESSION
    Module 04 section 4's baseline. One hour of work.

THE PREVIOUS SIMPLEST THING
    whatever the system you are replacing already
    does, measured on the same split

AND A SHORTCUT CHECK: train on a corrupted version of
the input (shuffled words, labels only, the question
without the passage). If it still scores well, the
task has an artefact."""),
  ("p", "<b>The shortcut check is the most informative single experiment "
        "in this module</b>, and it costs almost nothing: <b>it tells you "
        "whether your benchmark measures the ability you named or something "
        "else entirely.</b> <b>The input-ablation check has invalidated "
        "several famous benchmarks</b> — natural language inference "
        "datasets where the hypothesis alone predicted the label, reading "
        "comprehension sets answerable without the passage, and "
        "visual-question datasets answerable without the image. <b>Run it "
        "on your own task before trusting any number from it.</b>"),
  ("callout", "A system that beats a strawman has established nothing",
   ["<b>The baseline has to be the best cheap alternative, tuned with "
    "the same effort you spent on your own system</b> — and <b>an "
    "untuned baseline against a carefully tuned system is not a "
    "comparison</b>, it is a demonstration of where the effort went.",
    "<b>Which is resisted because a strong baseline sometimes "
    "wins</b> — and <b>that is a result worth having</b>, since it "
    "saves the entire cost of building, deploying, and maintaining the "
    "complicated system. A negative result that saves a quarter of "
    "engineering is valuable.",
    "<b>And the replication literature is unambiguous on this "
    "point:</b> <b>a substantial share of reported gains disappear when "
    "the baselines are tuned with equal effort</b>, a finding reproduced "
    "across recommendation, retrieval, and language modelling.",
    "<b>So Project 2 grades the baseline first</b> — <b>because an "
    "unbeaten strong baseline is a finding and a beaten weak one is "
    "not</b>, and getting that ordering right is most of what "
    "distinguishes a useful evaluation from a persuasive one."]),

  ("break",),
  ("h1", "3 &nbsp; Generation metrics"),
  ("table", ["Metric", "What it measures", "What it misses"],
   [["<b>BLEU</b>", "<b>N-gram overlap with one or more references.</b>",
     "<b>Any correct paraphrase, and meaning entirely</b> — a "
     "perfect translation using different words scores poorly."],
    ["<b>ROUGE</b>", "<b>Overlap, recall-oriented, for summarisation.</b>",
     "<b>The same, plus factual correctness</b> — a summary can "
     "score well while asserting something false."],
    ["<b>BERTScore and similar</b>",
     "<b>Embedding similarity to the references.</b>",
     "<b>Factuality; and it inherits the scoring model's own biases</b> "
     "(Module 04 &sect;3)."],
    ["<b>Perplexity</b>", "<b>How well the model fits held-out text.</b>",
     "<b>Usefulness</b> (Module 03 &sect;3)."],
    ["<b>LLM-as-judge</b>", "<b>Another model's stated preference.</b>",
     "<b>Calibration; and it prefers its own style</b> — see the "
     "callout."],
    ["<b>Human rating</b>", "<b>What a particular rater thought.</b>",
     "<b>Consistency, unless the protocol is tight</b> — and "
     "inter-rater agreement must be reported."]],
   [0.20, 0.34, 0.46]),
  ("p", "<b>Every row misses factual correctness</b>, which <b>for most "
        "real applications is precisely the thing that matters</b> — "
        "and <b>that gap is why generation evaluation remains an open "
        "problem</b> rather than a solved one with a preferred metric. "
        "<b>The honest consequence is that a generation system's quality "
        "claim needs a task-specific factuality check</b> that you build, "
        "and that no general metric supplies."),
  ("callout", "The judge-model problem deserves naming",
   ["<b>Using a strong model to score outputs is cheap, fast, and "
    "correlates with human judgement considerably better than overlap "
    "metrics do</b> — which is why it spread so quickly, and <b>the "
    "correlation is real</b> rather than illusory.",
    "<b>And it has specific, measured biases:</b> <b>a preference for "
    "longer answers, a preference for its own stylistic and formatting "
    "conventions, and a preference for whichever option is presented "
    "first</b> — all documented, and all correctable only "
    "partially (position bias by randomising, the others not "
    "really).",
    "<b>Which means it cannot evaluate a competitor fairly</b> if that "
    "competitor writes in a different style — and <b>it certainly "
    "cannot evaluate factuality that it does not itself know</b>, which "
    "is the failure that matters most and the one least often "
    "acknowledged.",
    "<b>So use it for development and for triage, calibrate it against "
    "human judgement on a sample, and report that calibration</b> — "
    "<b>which almost nobody does, and which is exactly what would make "
    "the method trustworthy.</b> The calibration sample can be small; "
    "it just has to exist."]),

  ("h1", "4 &nbsp; Error analysis, and contamination"),
  ("ul", ["<b>Read at least twenty errors individually</b>, with the "
          "input, the prediction, and the correct answer side by side "
          "— not aggregated, not sampled by score, just read.",
          "<b>Let the categories come from the data rather than from "
          "your expectations</b> — <b>which is the whole point, and "
          "is the step people skip by starting from a taxonomy they "
          "already had</b>, thereby learning nothing they did not already "
          "believe.",
          "<b>Count the categories</b>, so that you know which is worth "
          "fixing — and <b>the distribution is usually far more "
          "skewed than anticipated</b>, with one or two categories "
          "accounting for most of the loss and the rest being a long "
          "tail.",
          "<b>Check the labels while you are in there</b>, because <b>a "
          "meaningful fraction of apparent 'errors' are annotation "
          "mistakes</b> in most datasets — and a test set with a 5% "
          "label error rate caps your measurable accuracy at 95% no "
          "matter what you build.",
          "<b>And look at the <i>confident</i> errors "
          "specifically</b> — high-probability wrong "
          "answers — which <b>are the dangerous ones in deployment "
          "and the most diagnostic in analysis</b> (Module 12 "
          "&sect;3). <b>Reading twenty errors is a better use of an hour "
          "than any hyperparameter sweep</b>, and <b>it is the only "
          "method that finds a mislabelled test set.</b>"]),
  ("callout", "And benchmark contamination",
   ["<b>A pretrained model may well have seen your test set</b>, "
    "because <b>it was trained on a crawl of the web and your benchmark "
    "is published on the web</b> — frequently along with its "
    "answers, in papers, in repositories, and in blog posts.",
    "<b>Which inflates scores in a way that is hard to detect and "
    "impossible to rule out without access to the training data</b> "
    "— <b>which you generally do not have</b>, and which even the "
    "model's authors may not be able to search exhaustively.",
    "<b>So prefer a test set you constructed yourself, from data "
    "postdating the training cutoff</b>, or <b>at minimum check for "
    "verbatim and near-verbatim overlap and report what you "
    "checked</b> — which is a reportable fact rather than a "
    "guarantee.",
    "<b>And treat public benchmark scores as weak evidence.</b> <b>The "
    "ranking may reflect exposure rather than capability</b>, and <b>your "
    "own held-out data is worth more than a leaderboard position</b> "
    "— which is Module 13 &sect;2's claim form and is the "
    "practical conclusion of this module."]),
 ],
 "resources": [
   ("Jurafsky & Martin, the evaluation sections (free)",
    "https://web.stanford.edu/~jurafsky/slp3/",
    "<b>&sect;1 and &sect;3</b>, with the metric definitions and their "
    "known failures."),
   ("Gururangan et al. &mdash; Annotation Artifacts in NLI Data (free)",
    "https://aclanthology.org/N18-2017/",
    "<b>&sect;2's shortcut check, applied</b> — the hypothesis-only "
    "baseline that reframed a whole benchmark."),
   ("Reiter &mdash; A Structured Review of the Validity of BLEU (free)",
    "https://aclanthology.org/J18-3002/",
    "<b>&sect;3's first row, assessed carefully</b> — where BLEU "
    "correlates with judgement and where it does not."),
   ("Zheng et al. &mdash; Judging LLM-as-a-Judge (free)",
    "https://arxiv.org/abs/2306.05685",
    "<b>&sect;3's callout with the measurements</b> — the position, "
    "verbosity, and self-preference biases quantified."),
 ],
 "exercises": [
   "<b>Write the decision</b> your Project 2 output supports, then "
   "derive the metric from it.",
   "<b>State the cost asymmetry</b> between your two error types.",
   "<b>Check your splits for near-duplicates</b> and report how many you "
   "found.",
   "<b>Split your data by time</b> and compare the score against a "
   "random split.",
   "<b>Compute the majority-class and human-agreement numbers</b> for "
   "your task.",
   "<b>Run the shortcut check</b>: train on corrupted input and report "
   "the score.",
   "<b>Tune a strong baseline with the same effort</b> you spent on your "
   "system.",
   "<b>Score ten generated outputs with BLEU and by reading them</b>, and "
   "compare the rankings.",
   "<b>Calibrate a judge model</b> against your own judgement on twenty "
   "examples.",
   "<b>Read twenty errors</b>, derive the categories from them, count "
   "them, and report how many were label errors.",
 ],
 "selfcheck": [
   "Why derive the metric from the decision?",
   "Why is a metric's correlation with what you care about an empirical "
   "claim?",
   "Give five rules about splits, and the one that silently ruins text "
   "experiments.",
   "Name five baselines you must beat.",
   "What is the shortcut check, and what has it invalidated?",
   "Why is an unbeaten strong baseline a finding?",
   "Name six generation metrics and what each misses.",
   "What do they all miss?",
   "Give three biases of a judge model and the one correction that "
   "matters.",
   "Give five rules for error analysis and say which errors are most "
   "diagnostic.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Retrieval-Augmented Systems",
 "subtitle": "Giving the model the information it does not have.",
 "question": "How do you answer questions about your own documents?",
 "outcomes": [
     "Explain the architecture and what each stage contributes.",
     "Explain why retrieval quality dominates.",
     "Explain chunking and its trade-offs.",
     "Explain the failure modes specific to this design.",
     "Evaluate the retrieval and the generation separately.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The architecture",
   "blurb": "Retrieve, then condition."},

  {"t": "code", "kicker": "Pipeline", "title": "The stages, and what each decides",
   "lang": "text", "code": """
  INDEXING (once)
      split documents into chunks (Part 3)
      embed each chunk, or index for lexical search
      store with the metadata you will filter on

  RETRIEVAL (per query)
      embed the query, or build a lexical query
      retrieve the top N candidates
      optionally rerank them with a stronger model
      (CSCE 670 Module 07)

  GENERATION (per query)
      place the retrieved chunks in the prompt
      instruct the model to answer FROM them and to
      say so when they do not suffice
      return the answer with its citations

  AND THE CITATIONS ARE NOT OPTIONAL. They are what
  makes the answer checkable, which is the whole
  advantage of this design over asking the model
  directly (Module 12 section 3).
""",
   "caption": "<b>Citations are the point</b> — a retrieved answer "
              "that cannot be traced to a source has given up the design's "
              "main benefit.",
   "note": "Framing citations as the core benefit changes how people "
           "build these."},

  {"t": "callout", "title": "This is the answer to “the model does not know my data”",
   "kind": "What it solves, and what it does not",
   "body": ["<b>It solves currency, privacy, and "
            "attribution:</b> <b>the information can postdate training, "
            "can stay in your infrastructure, and the answer can be "
            "traced to a document.</b>",
            "<b>And it is far cheaper than fine-tuning for injecting "
            "knowledge</b>, because <b>updating the knowledge means "
            "updating an index rather than retraining "
            "anything.</b>",
            "<b>What it does not solve is reasoning across many "
            "documents</b> — <b>a question requiring the synthesis "
            "of twenty sources retrieves a handful and answers from "
            "those.</b>",
            "<b>Nor does it solve aggregation.</b> <b>'How many of "
            "our contracts expire this year' is a database query "
            "pretending to be a retrieval question</b> — and routing "
            "it to retrieval produces a confident wrong number."]},

  {"t": "section", "label": "Part 2", "title": "Retrieval dominates",
   "blurb": "Which determines where to spend effort."},

  {"t": "callout", "title": "If the right passage is not retrieved, no model can answer correctly",
   "kind": "The ordering of effort",
   "body": ["<b>The generation step can only work with what it is "
            "given</b> — so <b>retrieval recall is a hard ceiling on "
            "the whole system's accuracy</b>, and no prompt improvement "
            "raises it.",
            "<b>Which means measuring retrieval separately is "
            "essential</b> — <b>and a system reported only "
            "end-to-end cannot tell you which half to "
            "fix.</b>",
            "<b>And the practical finding is that hybrid retrieval "
            "beats either alone:</b> <b>lexical search handles exact "
            "terms, identifiers, and rare words; dense search handles "
            "paraphrase</b> (CSCE 670 §06).",
            "<b>So the effort order is: retrieval first, reranking "
            "second, prompt third</b> — <b>which is the reverse of "
            "how these systems are usually debugged.</b>"]},

  {"t": "bullets", "kicker": "Retrieval", "title": "What actually improves it",
   "items": [
     "<b>Hybrid lexical plus dense</b>, which is the single "
     "largest improvement available and is cheap.",
     "",
     "<b>A reranker over the top fifty</b>, which is more "
     "accurate than retrieval and too slow to apply to "
     "everything (CSCE 670 §07).",
     "",
     "<b>Query rewriting</b> — expanding, decomposing, or "
     "resolving pronouns against the conversation — which "
     "matters a great deal in multi-turn use.",
     "",
     "<b>Metadata filtering</b>, so that date, source, and "
     "permission constraints are applied before relevance rather than "
     "after.",
     "",
     "<b>And checking that the answer is in the corpus at "
     "all</b>, which is the diagnosis people skip.",
   ],
   "footnote": "<b>Permission filtering before retrieval is a security "
               "requirement, not a feature</b> — retrieving a "
               "document the user may not read and then summarising it is "
               "a disclosure (CSCE 701 Module 03)."},

  {"t": "section", "label": "Part 3", "title": "Chunking",
   "blurb": "An unglamorous decision with large effects."},

  {"t": "bullets", "kicker": "Chunking", "title": "The trade, and what to do",
   "items": [
     "<b>Small chunks retrieve precisely and lose "
     "context</b> — the retrieved passage may be accurate and "
     "unintelligible without its surroundings.",
     "",
     "<b>Large chunks preserve context and retrieve "
     "imprecisely</b>, because the embedding averages over several "
     "topics and matches none of them well.",
     "",
     "<b>So: split on structure where it exists</b> — "
     "sections, paragraphs, list items — <b>rather than on a fixed "
     "token count, which cuts mid-sentence and mid-table.</b>",
     "",
     "<b>Overlap adjacent chunks</b>, so that a fact spanning a "
     "boundary appears whole in one of them.",
     "",
     "<b>And retrieve the chunk, then expand to its "
     "neighbours</b> for generation — which gets precision in "
     "retrieval and context in the prompt.",
   ],
   "footnote": "<b>Retrieve small, generate large is the pattern worth "
               "adopting</b> — it resolves the trade rather than "
               "compromising on it."},

  {"t": "section", "label": "Part 4", "title": "The failure modes",
   "blurb": "Specific to this design."},

  {"t": "table", "kicker": "Failures", "title": "What goes wrong, and the fix",
   "header": ["Failure", "Cause", "Fix"],
   "widths": [2.8, 3.8, 5.0],
   "rows": [
     ["<b>Missing passage</b>", "<b>Retrieval recall</b>", "<b>Hybrid search, reranking (Part 2)</b>"],
     ["<b>Answers anyway</b>", "<b>No abstention instruction or no training for it</b>", "<b>Instruct and measure abstention</b>"],
     ["<b>Ignores the context</b>", "<b>Parametric knowledge overriding the passage</b>", "<b>Instruct to prefer the source; cite</b>"],
     ["<b>Lost in the middle</b>", "<b>Position effects in long contexts</b>", "<b>Fewer, better chunks; order by rank</b>"],
     ["<b>Contradicting sources</b>", "<b>The corpus disagrees with itself</b>", "<b>Surface the conflict rather than picking</b>"],
     ["<b>Stale index</b>", "<b>Documents changed, index did not</b>", "<b>Treat reindexing as an operation</b>"],
   ],
   "footnote": "<b>'Answers anyway' is the most dangerous "
               "row</b> — a confident answer assembled from "
               "irrelevant passages is worse than a refusal, and "
               "abstention has to be measured rather than "
               "assumed.",
   "note": "This table is the practically useful artefact."},

  {"t": "callout", "title": "And evaluate the two stages separately",
   "kind": "Closing",
   "body": ["<b>Retrieval:</b> <b>recall at k on a set of "
            "query-document pairs you labelled</b> — which requires "
            "building that set, and is the work people avoid.",
            "<b>Generation, given correct context:</b> <b>is the "
            "answer right when the passage is right?</b> — which "
            "isolates the generation quality.",
            "<b>Abstention:</b> <b>does it decline when the passage "
            "does not contain the answer?</b> — tested by "
            "deliberately retrieving irrelevant context.",
            "<b>And attribution:</b> <b>do the citations actually "
            "support the claims?</b> <b>Which must be checked by "
            "reading</b>, and is where these systems most often fail "
            "quietly."]},
 ],
 "takeaways": [
   "Citations are the point of this design — an untraceable retrieved "
   "answer has given up its main advantage over asking the model directly.",
   "It solves currency, privacy, and attribution, and does not solve "
   "multi-document reasoning or aggregation.",
   "Retrieval recall is a hard ceiling on the whole system, so measure the "
   "stages separately and fix retrieval first.",
   "Permission filtering must happen before retrieval, because summarising "
   "a document the user may not read is a disclosure.",
   "Retrieve small and generate large — which resolves the chunking "
   "trade rather than compromising on it.",
   "'Answers anyway' is the most dangerous failure, and abstention has to "
   "be measured rather than assumed.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The architecture"),
  ("code", """INDEXING (once, and on every update)
    split documents into chunks (section 3)
    embed each chunk, or index it for lexical search
    store with the metadata you will filter on

RETRIEVAL (per query)
    embed the query, or build a lexical query
    retrieve the top N candidates
    optionally rerank them with a stronger model
    (CSCE 670 Module 07)

GENERATION (per query)
    place the retrieved chunks in the prompt
    instruct the model to answer FROM them, and to say
    so when they do not suffice
    return the answer together with its citations

AND THE CITATIONS ARE NOT OPTIONAL. They are what
makes the answer checkable, which is the whole
advantage of this design over asking the model
directly (Module 12 section 3)."""),
  ("callout", "This is the answer to “the model does not know my "
              "data”",
   ["<b>It solves currency, privacy, and attribution together:</b> "
    "<b>the information can postdate the training cutoff, it can stay "
    "inside your own infrastructure, and the answer can be traced back to "
    "a specific document</b> — three different problems, one "
    "architecture.",
    "<b>And it is far cheaper than fine-tuning as a way of injecting "
    "knowledge</b>, because <b>updating the knowledge means updating an "
    "index rather than retraining anything</b> — and the update is "
    "incremental, immediate, and reversible.",
    "<b>What it does not solve is reasoning across many "
    "documents</b> — <b>a question genuinely requiring the "
    "synthesis of twenty sources retrieves a handful and answers "
    "confidently from those</b>, with no indication that it saw a "
    "fraction of the relevant material.",
    "<b>Nor does it solve aggregation.</b> <b>'How many of our "
    "contracts expire this year' is a database query pretending to be a "
    "retrieval question</b> — and <b>routing it to retrieval "
    "produces a confident wrong number</b>, which is the worst available "
    "outcome. <b>Recognising which questions are really queries is a "
    "design responsibility</b>, and the system should route them "
    "elsewhere."]),

  ("h1", "2 &nbsp; Retrieval dominates"),
  ("callout", "If the right passage is not retrieved, no model can answer "
              "correctly",
   ["<b>The generation step can only work with what it is given</b> "
    "— so <b>retrieval recall is a hard ceiling on the whole "
    "system's accuracy</b>, and <b>no amount of prompt improvement raises "
    "it</b>. This is arithmetic rather than a tendency.",
    "<b>Which means measuring the retrieval stage separately is "
    "essential</b> — <b>and a system reported only end-to-end "
    "cannot tell you which half to fix</b>, so the debugging proceeds by "
    "guesswork and usually lands on the prompt.",
    "<b>And the practical finding is that hybrid retrieval beats "
    "either method alone:</b> <b>lexical search handles exact terms, "
    "identifiers, product codes, and rare words; dense search handles "
    "paraphrase and synonymy</b> (CSCE 670 Module 06) — and "
    "real queries contain both.",
    "<b>So the effort order is: retrieval first, reranking second, "
    "prompt third</b> — <b>which is the exact reverse of how these "
    "systems are usually debugged</b>, since the prompt is the most "
    "visible and most easily changed component and therefore attracts the "
    "attention."]),
  ("ul", ["<b>Hybrid lexical plus dense retrieval</b>, which is "
          "<b>the single largest improvement available</b> and is cheap "
          "to implement — run both and combine the rankings.",
          "<b>A reranker over the top fifty candidates</b>, which is "
          "<b>more accurate than retrieval and far too slow to apply to "
          "the whole corpus</b> — which is exactly why the two-stage "
          "structure exists (CSCE 670 Module 07).",
          "<b>Query rewriting</b> — expanding with synonyms, "
          "decomposing a compound question, or resolving pronouns against "
          "the conversation history — <b>which matters a great deal "
          "in multi-turn use</b>, where 'what about last year' is "
          "unretrievable as written.",
          "<b>Metadata filtering</b>, so that date, source, and "
          "<b>permission constraints are applied before relevance rather "
          "than after</b> — see the note.",
          "<b>And checking whether the answer is in the corpus at "
          "all</b>, which is <b>the diagnosis people skip</b> and which "
          "accounts for a surprising share of 'the model is bad at this' "
          "complaints. <b>Permission filtering before retrieval is a "
          "security requirement rather than a feature:</b> <b>retrieving "
          "a document the user is not permitted to read and then "
          "summarising it for them is a disclosure</b>, and the "
          "summarisation does not launder it (CSCE 701 "
          "Module 03)."]),

  ("break",),
  ("h1", "3 &nbsp; Chunking"),
  ("ul", ["<b>Small chunks retrieve precisely and lose context</b> "
          "— the retrieved passage may be entirely accurate and "
          "<b>unintelligible without its surroundings</b>, referring to "
          "'this provision' or 'the above table' with no antecedent in "
          "view.",
          "<b>Large chunks preserve context and retrieve "
          "imprecisely</b>, because <b>the embedding averages over "
          "several topics and consequently matches none of them well</b> "
          "— which is a direct consequence of representing a long "
          "passage as one vector.",
          "<b>So: split on structure wherever it exists</b> — "
          "sections, paragraphs, list items, table rows, function "
          "definitions — <b>rather than on a fixed token count, "
          "which cuts mid-sentence, mid-table, and mid-code-block</b> and "
          "produces chunks that are hard to retrieve and useless when "
          "retrieved.",
          "<b>Overlap adjacent chunks</b>, so that <b>a fact spanning "
          "a boundary appears whole in at least one of them</b> — "
          "cheap insurance, at the cost of some index size.",
          "<b>And retrieve the chunk, then expand to its "
          "neighbours</b> before placing it in the prompt — <b>which "
          "gets precision in the retrieval and context in the "
          "generation</b>. <b>Retrieve small, generate large is the "
          "pattern worth adopting</b>, because <b>it resolves the trade "
          "rather than compromising on it</b>, and it is a small amount "
          "of code."]),

  ("h1", "4 &nbsp; The failure modes"),
  ("table", ["Failure", "The cause", "The fix"],
   [["<b>The passage was not retrieved</b>", "<b>Retrieval recall.</b>",
     "<b>Hybrid search and reranking</b> (&sect;2) — and check the "
     "answer is in the corpus."],
    ["<b>It answers anyway</b>",
     "<b>No abstention instruction, or no training that rewarded "
     "abstention.</b>",
     "<b>Instruct it to decline, and <i>measure</i> abstention</b> "
     "— see the note."],
    ["<b>It ignores the retrieved context</b>",
     "<b>Parametric knowledge overriding the provided passage.</b>",
     "<b>Instruct it to prefer the source, and require citations</b> so "
     "the override is visible."],
    ["<b>Lost in the middle</b>",
     "<b>Position effects in long contexts</b> — material in the "
     "middle is used less.",
     "<b>Fewer, better chunks; and order them by rank</b> rather than by "
     "document order."],
    ["<b>Contradicting sources</b>",
     "<b>The corpus genuinely disagrees with itself.</b>",
     "<b>Surface the conflict rather than silently picking one</b> "
     "— which is the honest behaviour."],
    ["<b>Stale index</b>",
     "<b>The documents changed and the index did not.</b>",
     "<b>Treat reindexing as an operational process</b> with monitoring, "
     "not a one-off script."]],
   [0.22, 0.32, 0.46]),
  ("p", "<b>'Answers anyway' is the most dangerous row.</b> <b>A "
        "confident answer assembled from irrelevant retrieved passages is "
        "worse than a refusal</b>, because it is both wrong and "
        "apparently sourced — the citations lend it credibility it "
        "has not earned. <b>And abstention has to be measured rather than "
        "assumed</b>, by deliberately retrieving irrelevant context and "
        "checking what happens, which is &sect;4's third evaluation."),
  ("callout", "And evaluate the two stages separately",
   ["<b>Retrieval:</b> <b>recall at k, measured on a set of "
    "query-document pairs that you have labelled</b> — which "
    "requires actually building that set, and <b>is the work people "
    "avoid</b>, with the result that they cannot tell retrieval failures "
    "from generation failures.",
    "<b>Generation, given correct context:</b> <b>is the answer right "
    "when the right passage <i>was</i> retrieved?</b> — which "
    "isolates generation quality from retrieval quality and is "
    "straightforward once you have the labelled set.",
    "<b>Abstention:</b> <b>does it decline when the retrieved "
    "passages do not contain the answer?</b> — tested by "
    "deliberately supplying irrelevant context and measuring how often it "
    "answers anyway. <b>This number is usually worse than people "
    "expect.</b>",
    "<b>And attribution:</b> <b>do the citations actually support the "
    "claims they are attached to?</b> <b>Which must be checked by "
    "reading</b>, cannot be automated reliably, and <b>is where these "
    "systems most often fail quietly</b> — a plausible answer with a "
    "citation to a document that does not say that is the characteristic "
    "defect, and nothing in the pipeline catches it."]),
 ],
 "resources": [
   ("Lewis et al. &mdash; Retrieval-Augmented Generation (free)",
    "https://arxiv.org/abs/2005.11401",
    "<b>&sect;1 in the original</b> — and worth reading for how much "
    "of the current practice was already there."),
   ("Liu et al. &mdash; Lost in the Middle (free)",
    "https://arxiv.org/abs/2307.03172",
    "<b>&sect;4's fourth row, measured</b> — the position effect "
    "across long contexts, which has direct design consequences."),
   ("Gao et al. &mdash; Retrieval-Augmented Generation: a survey (free)",
    "https://arxiv.org/abs/2312.10997",
    "<b>&sect;2 and &sect;3's design space</b>, organised — useful "
    "for finding the variant that matches your constraints."),
   ("Rashkin et al. &mdash; Measuring Attribution (free)",
    "https://aclanthology.org/2023.tacl-1.10/",
    "<b>&sect;4's last evaluation</b> — a framework for whether a "
    "citation actually supports a claim."),
 ],
 "exercises": [
   "<b>Build the three-stage pipeline</b> over a document collection you "
   "have.",
   "<b>Require citations</b> and check ten answers against their "
   "sources.",
   "<b>Find a question your corpus cannot answer</b> and see what the "
   "system does.",
   "<b>Label fifty query-document pairs</b> and measure retrieval recall "
   "at 5 and at 20.",
   "<b>Add lexical search alongside dense</b> and remeasure.",
   "<b>Add a reranker over the top fifty</b> and remeasure again.",
   "<b>Compare fixed-size and structure-based chunking</b> on retrieval "
   "precision.",
   "<b>Implement retrieve-small-generate-large</b> and compare.",
   "<b>Supply deliberately irrelevant context</b> and measure how often "
   "it answers anyway.",
   "<b>Check permission filtering happens before retrieval</b>, and fix "
   "it if not.",
 ],
 "selfcheck": [
   "Give the three stages and what each decides.",
   "Why are citations the point?",
   "What three problems does this solve, and what two does it not?",
   "Why is retrieval recall a hard ceiling?",
   "Why does hybrid retrieval win, and what does each half contribute?",
   "Give five ways to improve retrieval, and the security "
   "requirement.",
   "State the chunking trade and the pattern that resolves it.",
   "Name six failure modes with their causes and fixes.",
   "Why is 'answers anyway' the most dangerous?",
   "Give the four separate evaluations.",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Bias, Failure, and Fabrication",
 "subtitle": "How these systems fail people.",
 "question": "What goes wrong, and for whom?",
 "outcomes": [
     "Explain where bias enters and why it is not one thing.",
     "Explain distributional and dialectal failure.",
     "Explain fabrication and its mechanism.",
     "Explain what mitigations do and do not achieve.",
     "Build a failure analysis into a system's evaluation.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Where bias enters",
   "blurb": "At every stage, differently."},

  {"t": "table", "kicker": "Sources", "title": "The stages, and the bias each introduces",
   "header": ["Stage", "What enters", "Example"],
   "widths": [2.5, 4.1, 5.0],
   "rows": [
     ["<b>Corpus</b>", "<b>Who writes, and about whom</b>", "<b>Web text skews by language, region, and voice</b>"],
     ["<b>Tokeniser</b>", "<b>Which languages are efficient</b>", "<b>Several times more tokens for some scripts (M02 §3)</b>"],
     ["<b>Objective</b>", "<b>What is treated as normal</b>", "<b>The majority pattern becomes the prediction</b>"],
     ["<b>Annotation</b>", "<b>Whose judgement is the label</b>", "<b>Raters disagree systematically by group</b>"],
     ["<b>Evaluation</b>", "<b>Which failures are visible</b>", "<b>Aggregate metrics hide subgroup failure</b>"],
     ["<b>Deployment</b>", "<b>Who bears the error</b>", "<b>The same error rate, unequal consequences</b>"],
   ],
   "footnote": "<b>The evaluation row is the one that makes the others "
               "invisible</b> — an aggregate score can improve while "
               "a subgroup's experience worsens, which is why "
               "disaggregation is the minimum requirement.",
   "note": "Framing bias as entering at six stages prevents the "
           "single-cause framing."},

  {"t": "callout", "title": "“Bias” names several different things, and conflating them prevents fixing any",
   "kind": "The distinction worth making",
   "body": ["<b>A representational association</b> — the "
            "embedding geometry linking occupations to genders "
            "(Module 04 §3) — is a property of the "
            "representation.",
            "<b>A performance disparity</b> — higher error rates "
            "for one dialect or language — is a property of the "
            "model's accuracy, and is measurable per "
            "group.",
            "<b>An allocation harm</b> — a system's decisions "
            "distributing opportunity unequally — is a property of "
            "the deployment, not of the model.",
            "<b>And they need different responses.</b> <b>Measuring "
            "the first tells you little about the third</b>, which is "
            "why a debiased embedding can sit inside a system that "
            "allocates unfairly."]},

  {"t": "section", "label": "Part 2", "title": "Distributional failure",
   "blurb": "Who the system works less well for."},

  {"t": "bullets", "kicker": "Disparities", "title": "The measured disparities, and their causes",
   "items": [
     "<b>Dialect.</b> <b>Error rates are measurably higher for "
     "non-standard varieties</b> — because the training data "
     "contains less of them and the annotation often treats them as "
     "errors.",
     "",
     "<b>Language.</b> <b>Quality falls sharply outside the "
     "best-resourced languages</b>, and the tokenisation penalty "
     "compounds the data scarcity "
     "(Module 02 §3).",
     "",
     "<b>Names and entities.</b> <b>Recognition is worse for names "
     "underrepresented in the corpus</b>, which affects exactly the "
     "people least able to work around it.",
     "",
     "<b>Domain and register.</b> <b>Clinical, legal, and "
     "informal text all differ from the pretraining "
     "mixture.</b>",
     "",
     "<b>And the common cause is the training "
     "distribution</b> — which means <b>the fix is data, and "
     "data is expensive.</b>",
   ],
   "footnote": "<b>'The fix is data and data is expensive' is the "
               "honest statement</b> — which is why these "
               "disparities persist across model generations and are not "
               "solved by scale alone."},

  {"t": "callout", "title": "Which makes disaggregated evaluation the minimum requirement",
   "kind": "The practice that follows",
   "body": ["<b>Report performance by subgroup, not only in "
            "aggregate</b> — because <b>an aggregate number averages "
            "over exactly the disparity you need to "
            "see.</b>",
            "<b>And the subgroups have to be chosen from who uses the "
            "system</b>, which requires knowing that — and is a "
            "question to ask at design time rather than after "
            "deployment.",
            "<b>With the sample size per group large enough to "
            "measure</b>, which frequently means deliberately collecting "
            "more data for small groups rather than sampling "
            "proportionally.",
            "<b>Which is CSCE 633 §12's subgroup "
            "argument</b> — <b>and it is the single most actionable "
            "thing in this module</b>, because it converts a concern into "
            "a number somebody can be accountable for."]},

  {"t": "section", "label": "Part 3", "title": "Fabrication",
   "blurb": "And why it is structural rather than a bug."},

  {"t": "callout", "title": "The model was trained to produce plausible text, and false text can be plausible",
   "kind": "The mechanism",
   "body": ["<b>Next-token prediction optimises for what text looks "
            "like</b> (Module 03 §1) — and <b>a "
            "well-formed false statement looks exactly like a well-formed "
            "true one.</b>",
            "<b>There is no internal mechanism separating "
            "them.</b> <b>The model has no representation of 'I do not "
            "know this'</b> that reliably governs its output, because "
            "nothing in training required one.",
            "<b>And preference training makes it worse in a specific "
            "way</b> (Module 08 §4): <b>confident fluent "
            "answers rate better than hedged ones</b>, so the training "
            "rewards exactly the dangerous behaviour.",
            "<b>Which is why fabrication is structural rather than a "
            "bug to be fixed</b> — <b>and why it is most dangerous "
            "precisely where the model is most fluent</b>, which is also "
            "where people trust it most."]},

  {"t": "bullets", "kicker": "Mitigations", "title": "And what the mitigations actually achieve",
   "items": [
     "<b>Retrieval with citations</b> "
     "(Module 11) — <b>the most effective, because it "
     "makes the claim checkable</b> rather than making it "
     "true.",
     "",
     "<b>Abstention training and instruction</b>, which reduces "
     "the rate and does not eliminate it — and must be "
     "measured (Module 11 §4).",
     "",
     "<b>Calibration and confidence reporting</b>, which helps a "
     "reader weight the answer — <b>and these models are "
     "poorly calibrated on open-ended output.</b>",
     "",
     "<b>Verification against a source</b>, which works and costs "
     "a second system.",
     "",
     "<b>And designing so that a wrong answer is "
     "recoverable</b> — which is the only mitigation that does not "
     "depend on the model.",
   ],
   "footnote": "<b>The last one is the architectural "
               "answer:</b> <b>put the output where a person checks it "
               "before it matters</b>, which is "
               "CSCE 701 Module 11's "
               "consequence-reduction argument."},

  {"t": "section", "label": "Part 4", "title": "Building it in",
   "blurb": "As part of the evaluation, not after."},

  {"t": "bullets", "kicker": "Practice", "title": "What a failure analysis should contain",
   "items": [
     "<b>Performance disaggregated by the subgroups who will use "
     "it</b>, with sample sizes stated.",
     "",
     "<b>The input types on which it fails</b>, found by error "
     "analysis (Module 10 §4) rather than "
     "predicted.",
     "",
     "<b>The fabrication rate on questions your sources cannot "
     "answer</b>, measured deliberately.",
     "",
     "<b>The confident-error rate</b>, separately — because "
     "<b>a wrong answer the system is sure about is the one that "
     "causes harm.</b>",
     "",
     "<b>And what happens downstream when it is wrong</b> — "
     "<b>who notices, how quickly, and what it costs</b>.",
   ],
   "footnote": "<b>The last item is the one that turns this from an "
               "ethics section into an engineering "
               "requirement</b> — and it is a design question rather "
               "than a measurement."},

  {"t": "callout", "title": "The honest framing",
   "kind": "Closing",
   "body": ["<b>These systems are useful and they fail "
            "unevenly</b> — and both halves have to be stated "
            "together, because either one alone is misleading.",
            "<b>The failures are not random:</b> <b>they concentrate "
            "on the data the training distribution underrepresented</b>, "
            "which means they concentrate on particular people.",
            "<b>And the mitigations are partial.</b> <b>Nothing in "
            "Part 3 eliminates fabrication, and nothing in "
            "Part 2 equalises performance</b> — so the "
            "deployment has to assume both continue.",
            "<b>Which makes the design question 'what happens when "
            "this is wrong, and to whom'</b> — <b>and a system "
            "deployed without an answer to that has not been "
            "evaluated</b>, which is Module 13's position."]},
 ],
 "takeaways": [
   "Bias enters at six stages, and the evaluation stage is the one that "
   "makes the others invisible.",
   "Representational association, performance disparity, and allocation "
   "harm are different things needing different responses.",
   "The common cause of the disparities is the training distribution, so "
   "the fix is data and data is expensive.",
   "Disaggregated evaluation is the minimum requirement and the most "
   "actionable thing in the module, because it produces a number.",
   "Fabrication is structural: the objective rewards plausible text, and "
   "preference training rewards confident fluent answers specifically.",
   "Retrieval with citations works by making the claim checkable rather "
   "than by making it true.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Where bias enters"),
  ("table", ["Stage", "What enters there", "Example"],
   [["<b>Corpus</b>", "<b>Who writes, and about whom.</b>",
     "<b>Web text skews heavily by language, region, era, and "
     "voice</b> — and the skew is not random."],
    ["<b>Tokeniser</b>", "<b>Which languages are represented "
     "efficiently.</b>",
     "<b>Several times more tokens for the same content in some "
     "scripts</b> (Module 02 &sect;3)."],
    ["<b>Objective</b>", "<b>What gets treated as normal.</b>",
     "<b>The majority pattern becomes the prediction</b>, and the "
     "minority pattern becomes an error."],
    ["<b>Annotation</b>", "<b>Whose judgement becomes the label.</b>",
     "<b>Raters disagree systematically by group</b>, and the majority "
     "label erases the disagreement."],
    ["<b>Evaluation</b>", "<b>Which failures are visible at all.</b>",
     "<b>Aggregate metrics hide subgroup failure</b> — see the "
     "note."],
    ["<b>Deployment</b>", "<b>Who bears the cost of an error.</b>",
     "<b>The same error rate with unequal consequences</b>, depending on "
     "who can appeal or work around it."]],
   [0.16, 0.34, 0.50]),
  ("p", "<b>The evaluation row is the one that makes all the others "
        "invisible.</b> <b>An aggregate score can improve while a "
        "particular subgroup's experience gets worse</b> — and it "
        "will not show up anywhere — <b>which is why disaggregation "
        "is the minimum requirement</b> (&sect;2's callout) and why this "
        "row is the one to fix first: it is cheap, and it makes the rest "
        "measurable."),
  ("callout", "“Bias” names several different things, and "
              "conflating them prevents fixing any of them",
   ["<b>A representational association</b> — the embedding geometry "
    "linking occupations to genders (Module 04 &sect;3) — <b>is "
    "a property of the representation</b>, measurable with a "
    "similarity computation.",
    "<b>A performance disparity</b> — higher error rates for one "
    "dialect, language, or name distribution — <b>is a property of "
    "the model's accuracy, and is measurable per group</b> given a "
    "labelled sample (&sect;2).",
    "<b>An allocation harm</b> — a deployed system's decisions "
    "distributing opportunity, attention, or risk unequally — <b>is "
    "a property of the deployment rather than of the model at all</b>, "
    "and cannot be measured by examining the model.",
    "<b>And they require different responses.</b> <b>Measuring the "
    "first tells you very little about the third</b> — which is "
    "<b>why a debiased embedding can sit quite happily inside a system "
    "that allocates unfairly</b>, and why debiasing-the-vectors research "
    "answered a narrower question than it was taken to answer "
    "(Module 04 &sect;3's post-hoc correction warning)."]),

  ("h1", "2 &nbsp; Distributional failure"),
  ("ul", ["<b>Dialect.</b> <b>Error rates are measurably higher for "
          "non-standard varieties</b> — because the training data "
          "contains less of them, <b>and because the annotation "
          "frequently treats dialectal forms as errors</b>, which encodes "
          "the judgement into the label.",
          "<b>Language.</b> <b>Quality falls sharply outside the "
          "best-resourced languages</b>, and <b>the tokenisation penalty "
          "compounds the data scarcity</b> (Module 02 &sect;3) — "
          "so the same question costs more and is answered worse.",
          "<b>Names and entities.</b> <b>Recognition is measurably "
          "worse for names underrepresented in the corpus</b> — "
          "which <b>affects exactly the people least able to work around "
          "it</b>, since the workaround is usually to change how you "
          "write your own name.",
          "<b>Domain and register.</b> <b>Clinical notes, legal "
          "drafting, and informal conversational text all differ "
          "substantially from the pretraining mixture</b>, and the "
          "degradation is not always obvious because the output remains "
          "fluent.",
          "<b>And the common cause across all four is the training "
          "distribution</b> — which means <b>the fix is data, and "
          "data is expensive</b>. <b>That is the honest statement</b>, "
          "and it is <b>why these disparities persist across model "
          "generations and are not solved by scale alone</b>: scaling a "
          "skewed corpus preserves the skew."]),
  ("callout", "Which makes disaggregated evaluation the minimum requirement",
   ["<b>Report performance by subgroup rather than only in "
    "aggregate</b> — because <b>an aggregate number averages over "
    "precisely the disparity you need to see</b>, and an improvement in "
    "the mean is consistent with a regression for a minority of users.",
    "<b>And the subgroups have to be chosen from who actually uses the "
    "system</b>, which requires knowing that — <b>and is a question "
    "to ask at design time rather than after deployment</b>, since the "
    "data to answer it has to be collected.",
    "<b>With the sample size per group large enough to measure "
    "anything</b>, which <b>frequently means deliberately collecting "
    "more data for small groups rather than sampling "
    "proportionally</b> — a proportional sample gives you a wide "
    "confidence interval exactly where you most need a narrow one.",
    "<b>Which is CSCE 633 Module 12's subgroup argument</b> "
    "— and <b>it is the single most actionable thing in this "
    "module</b>, because <b>it converts a concern into a number that "
    "somebody can be held accountable for</b>, which is the step at which "
    "this material stops being a discussion and becomes engineering."]),

  ("break",),
  ("h1", "3 &nbsp; Fabrication"),
  ("callout", "The model was trained to produce plausible text, and false "
              "text can be entirely plausible",
   ["<b>Next-token prediction optimises for what text looks like</b> "
    "(Module 03 &sect;1's last point) — and <b>a well-formed "
    "false statement looks exactly like a well-formed true one</b>, "
    "token by token, which means the objective cannot distinguish them "
    "even in principle.",
    "<b>There is no internal mechanism separating them.</b> <b>The "
    "model has no representation of 'I do not know this' that reliably "
    "governs its output</b>, because nothing in the training process "
    "required one — and the probing evidence for partial internal "
    "signals of uncertainty does not yet translate into reliable "
    "behaviour.",
    "<b>And preference training makes it worse in a specific and "
    "predictable way</b> (Module 08 &sect;4): <b>confident, fluent, "
    "well-formatted answers rate better than hedged ones</b>, so <b>the "
    "training explicitly rewards the behaviour that causes the harm</b>. "
    "This is a Goodhart failure (CSCE 701 Module 12) inside the "
    "training pipeline.",
    "<b>Which is why fabrication is structural rather than a bug to be "
    "fixed</b> — and <b>why it is most dangerous precisely where "
    "the model is most fluent</b>, which is also, unfortunately, "
    "<b>where people trust it most.</b> The correlation runs the wrong "
    "way."]),
  ("ul", ["<b>Retrieval with citations</b> (Module 11) — "
          "<b>the most effective available mitigation, because it makes "
          "the claim <i>checkable</i></b> rather than making it true. "
          "<b>That distinction is the whole value</b>, and it is why "
          "Module 11 &sect;1 insists the citations are not "
          "optional.",
          "<b>Abstention training and explicit instruction</b>, which "
          "<b>reduces the rate and does not eliminate it</b> — and "
          "<b>must be measured</b> rather than assumed (Module 11 "
          "&sect;4's third evaluation).",
          "<b>Calibration and confidence reporting</b>, which helps a "
          "reader weight the answer appropriately — <b>and these "
          "models are poorly calibrated on open-ended output</b>, so the "
          "reported confidence is itself of limited reliability.",
          "<b>Verification against a source</b>, which genuinely works "
          "and <b>costs a second system</b> plus the latency — and is "
          "the right answer where the cost of a wrong answer is high.",
          "<b>And designing so that a wrong answer is "
          "recoverable</b> — <b>which is the only mitigation that "
          "does not depend on the model's behaviour at all</b>. <b>This "
          "is the architectural answer:</b> <b>put the output where a "
          "person checks it before it matters</b>, which is <b>CSCE 701 "
          "Module 11's consequence-reduction argument</b> applied here, "
          "and the same move as designing so that being phished does not "
          "matter."]),

  ("h1", "4 &nbsp; Building it into the evaluation"),
  ("ul", ["<b>Performance disaggregated by the subgroups who will "
          "actually use it</b>, <b>with the sample sizes stated</b> so a "
          "reader can see which comparisons are meaningful "
          "(&sect;2).",
          "<b>The input types on which it fails</b>, <b>found by error "
          "analysis</b> (Module 10 &sect;4) <b>rather than "
          "predicted</b> — because the predicted failures and the "
          "actual ones overlap less than anyone expects.",
          "<b>The fabrication rate on questions your sources cannot "
          "answer</b>, measured deliberately by constructing such "
          "questions — which is ten minutes of work and is almost "
          "never done.",
          "<b>The confident-error rate, separately from the overall "
          "error rate</b> — because <b>a wrong answer the system is "
          "sure about is the one that causes harm</b>, and it is invisible "
          "in an aggregate accuracy figure.",
          "<b>And what happens downstream when it is wrong</b> — "
          "<b>who notices, how quickly, and what it costs</b>. <b>This "
          "last item is the one that turns this from an ethics section "
          "into an engineering requirement</b>, and <b>it is a design "
          "question rather than a measurement</b>: the answer is "
          "determined by where you put the output, not by how good the "
          "model is."]),
  ("callout", "The honest framing",
   ["<b>These systems are genuinely useful and they fail "
    "unevenly</b> — and <b>both halves have to be stated "
    "together</b>, because either one on its own is misleading: the first "
    "alone oversells, and the second alone implies they should not be "
    "used.",
    "<b>The failures are not random:</b> <b>they concentrate on the "
    "data that the training distribution underrepresented</b>, which "
    "means <b>they concentrate on particular people</b> rather than being "
    "spread evenly across users.",
    "<b>And the mitigations are partial.</b> <b>Nothing in &sect;3 "
    "eliminates fabrication, and nothing in &sect;2 equalises "
    "performance</b> — so <b>the deployment has to be designed on "
    "the assumption that both continue</b>, rather than on the assumption "
    "that the next model fixes them.",
    "<b>Which makes the central design question 'what happens when "
    "this is wrong, and to whom'</b> — and <b>a system deployed "
    "without an answer to that question has not been evaluated</b>, "
    "whatever its benchmark scores. <b>That is Module 13's "
    "position</b>, and it is this course's version of the program's "
    "closing rule."]),
 ],
 "resources": [
   ("Bender et al. &mdash; On the Dangers of Stochastic Parrots (free)",
    "https://dl.acm.org/doi/10.1145/3442188.3445922",
    "<b>&sect;1 and &sect;2's argument</b>, and the paper that set the "
    "terms of this discussion. Read it in full."),
   ("Blodgett et al. &mdash; Language (Technology) is Power (free)",
    "https://aclanthology.org/2020.acl-main.485/",
    "<b>&sect;1's callout, argued carefully</b> — a survey of how "
    "'bias' is used inconsistently and what that costs."),
   ("Ji et al. &mdash; Survey of Hallucination in NLG (free)",
    "https://arxiv.org/abs/2202.03629",
    "<b>&sect;3's mechanisms and mitigations</b>, organised — and "
    "honest about how partial the mitigations are."),
   ("Mitchell et al. &mdash; Model Cards for Model Reporting (free)",
    "https://arxiv.org/abs/1810.03993",
    "<b>&sect;4's documentation practice</b> — the template that made "
    "disaggregated reporting a norm rather than an exception."),
 ],
 "exercises": [
   "<b>For your Project 2 system, name what enters at each of the six "
   "stages.</b>",
   "<b>Distinguish the three senses of bias</b> for one concrete "
   "concern you have.",
   "<b>Measure performance on standard and non-standard text</b> for one "
   "task.",
   "<b>Measure token counts</b> for the same content in three "
   "languages.",
   "<b>Disaggregate one evaluation by a subgroup</b> and report the "
   "sample sizes.",
   "<b>Construct ten questions your sources cannot answer</b> and "
   "measure the fabrication rate.",
   "<b>Measure the confident-error rate</b> separately from the overall "
   "one.",
   "<b>Add citations to one system</b> and check whether they support "
   "the claims.",
   "<b>Design one recovery path</b> so that a wrong answer is caught "
   "before it matters.",
   "<b>Write the two-sentence honest framing</b> for your own system.",
 ],
 "selfcheck": [
   "Name the six stages and what bias enters at each.",
   "Why is the evaluation stage the one to fix first?",
   "Distinguish the three senses of 'bias' and say why it matters.",
   "Give four measured disparities and their common cause.",
   "Why does scale not solve them?",
   "What is the minimum requirement, and why is it the most "
   "actionable?",
   "Give the mechanism of fabrication, and why preference training "
   "worsens it.",
   "Why is it most dangerous where the model is most fluent?",
   "Name five mitigations and say what the most effective one actually "
   "does.",
   "Give the five components of a failure analysis.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Claiming Language Understanding Honestly",
 "subtitle": "What a model's performance establishes.",
 "question": "The model scored well. What follows?",
 "outcomes": [
     "State what a benchmark result establishes.",
     "Identify the standard overclaims.",
     "Write a defensible system claim.",
     "Place this course relative to CSCE 676 and CSCE 670.",
     "State what you would need to claim understanding.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What a score establishes",
   "blurb": "Precisely, and it is narrow."},

  {"t": "callout", "title": "A benchmark score is a statement about that dataset, that metric, and that split",
   "kind": "The honest reading",
   "body": ["<b>It establishes that this model, under this decoding "
            "configuration, scored this on these examples by this "
            "measure</b> — all four clauses, and none of them "
            "optional.",
            "<b>It does not establish generalisation to your "
            "data</b>, unless your data is distributed like the "
            "benchmark's — which is an empirical question with a "
            "usually negative answer.",
            "<b>And it does not establish the <i>ability</i> the "
            "benchmark is named after</b>, because <b>a benchmark may be "
            "solvable by an artefact</b> "
            "(Module 10 §2's shortcut check).",
            "<b>Nor does it rule out contamination</b> "
            "(Module 10 §4) — <b>so a high score on a "
            "public benchmark is weak evidence</b>, and your own held-out "
            "data is stronger."]},

  {"t": "table", "kicker": "Overclaims", "title": "The standard overclaims, corrected",
   "header": ["Claim", "Correction"],
   "widths": [4.4, 6.6],
   "rows": [
     ["<b>'The model understands X'</b>", "<b>It produces text consistent with understanding X on these inputs</b>"],
     ["<b>'It achieves human-level performance'</b>", "<b>On this dataset, by this metric, against these annotators</b>"],
     ["<b>'It can reason'</b>", "<b>It produces reasoning-shaped text; check whether the steps are load-bearing</b>"],
     ["<b>'It knows that P'</b>", "<b>It asserts P here; check whether it asserts ¬P when asked differently</b>"],
     ["<b>'Hallucination is being solved'</b>", "<b>Rates fall; the mechanism is structural (M12 §3)</b>"],
     ["<b>'It scored 90%'</b>", "<b>With which decoding, which prompt, and what variance? (M09, M08 §3)</b>"],
   ],
   "footnote": "<b>The second row is the most consequential</b> — "
               "'human-level' invites a generalisation the measurement "
               "does not support, since the human comparison was on the "
               "same narrow distribution.",
   "note": "The human-level overclaim does the most damage in public "
           "discussion."},

  {"t": "section", "label": "Part 2", "title": "Claims you can defend",
   "blurb": "The form to use."},

  {"t": "bullets", "kicker": "Honest", "title": "Defensible claims",
   "items": [
     "<b>'On 2,000 held-out examples from our own data, F1 is 0.84 "
     "against a tuned BM25 baseline of 0.71, with a 95% interval of "
     "±0.02.'</b> <b>Checkable in every clause.</b>",
     "",
     "<b>'Performance on dialectal inputs is 7 points lower; the "
     "sample is 300 examples.'</b> <b>Disaggregated, with the "
     "sample stated</b> (Module 12 §2).",
     "",
     "<b>'On questions our corpus cannot answer, it abstains 62% "
     "of the time and fabricates 38%.'</b> <b>A measured failure "
     "rate.</b>",
     "",
     "<b>'Results are with top-p 0.9 at temperature 0.7, averaged "
     "over five prompts; variance across prompts is 3 "
     "points.'</b>",
     "",
     "<b>And: 'we have not evaluated on inputs longer than 500 "
     "tokens, or in any language but English.'</b>",
   ],
   "footnote": "<b>The last one is the limitation statement</b>, and it "
               "is what distinguishes a system report from a "
               "demonstration — which is Project 2's "
               "hardest-graded requirement."},

  {"t": "section", "label": "Part 3", "title": "Understanding",
   "blurb": "The question, treated carefully."},

  {"t": "callout", "title": "The honest position on understanding is that the question is not settled and the evidence is specific",
   "kind": "Both overclaim and dismissal are unsupported",
   "body": ["<b>'It is just predicting the next token' understates "
            "it.</b> <b>Predicting text well requires representations "
            "that support generalisation</b>, and probing finds "
            "structure — syntax, factual relations, and spatial "
            "information — in the activations.",
            "<b>'It understands language' overstates it.</b> "
            "<b>Performance is brittle to paraphrase, sensitive to "
            "formatting, and inconsistent under rephrasing of the same "
            "question</b> — which is not the profile of robust "
            "understanding.",
            "<b>So the useful move is to stop asking the general "
            "question and test specific capabilities:</b> <b>is the "
            "behaviour consistent under paraphrase? does it transfer to "
            "a novel composition? are the reasoning steps "
            "load-bearing?</b>",
            "<b>Each of those is measurable</b> — <b>and "
            "measuring them is more informative than any position on the "
            "general question</b>, which is where this course asks you to "
            "put the effort."]},

  {"t": "bullets", "kicker": "Tests", "title": "The tests that discriminate",
   "items": [
     "<b>Paraphrase consistency.</b> <b>Ask the same question "
     "five ways</b> — a model that answers differently has not "
     "represented the question.",
     "",
     "<b>Counterfactual sensitivity.</b> <b>Change the fact the "
     "answer depends on</b>, and check the answer changes.",
     "",
     "<b>Compositional generalisation.</b> <b>Test a novel "
     "combination of familiar parts</b>, which is where systems "
     "reliably break.",
     "",
     "<b>Load-bearing reasoning.</b> <b>Corrupt an intermediate "
     "step and see whether the answer changes</b> — if not, the "
     "steps were decoration.",
     "",
     "<b>And contamination control:</b> <b>construct the test "
     "after the training cutoff</b>, or accept that you cannot rule it "
     "out.",
   ],
   "footnote": "<b>The load-bearing test is the sharpest of these</b> "
               "— reasoning-shaped text that does not affect the "
               "answer is a presentation, and the test is cheap."},

  {"t": "section", "label": "Part 4", "title": "The semester",
   "blurb": "And where this course sits."},

  {"t": "table", "kicker": "Semester 10", "title": "The three courses",
   "header": ["Course", "Covers", "Shared concern"],
   "widths": [2.3, 3.8, 5.4],
   "rows": [
     ["<b>CSCE 638</b>", "<b>Language as input and output</b>", "<b>Evaluation that measures the right thing</b>"],
     ["<b>CSCE 676</b>", "<b>Finding structure at scale</b>", "<b>Patterns that are real versus found</b>"],
     ["<b>CSCE 670</b>", "<b>Satisfying an information need</b>", "<b>Relevance as a judgement, not a label</b>"],
   ],
   "footnote": "<b>All three are courses about measurement as much as "
               "about method</b> — because in all three the thing "
               "you want is a human judgement and the thing you have is a "
               "proxy.",
   "note": "The shared-concern framing is the semester's "
           "organisation."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can explain the arc from counting to attention to "
            "pretraining, and say what each step bought</b> — which "
            "is more durable than any current architecture.",
            "<b>You can build a system:</b> <b>choose and adapt a "
            "pretrained model, decode deliberately, retrieve when the "
            "knowledge is external, and evaluate against a baseline that "
            "is hard to beat.</b>",
            "<b>And you know the characteristic failure</b> — "
            "<b>fluent, confident, and wrong</b> — along with why it "
            "is structural and what reduces it.",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it means naming the "
            "dataset, the metric, the decoding, and the inputs you did "
            "not test</b> — because <b>'it understands' names none of "
            "them.</b>"]},
 ],
 "takeaways": [
   "A benchmark score is a statement about that dataset, metric, split, and "
   "decoding configuration — all four clauses.",
   "'Human-level performance' is the most consequential overclaim, because "
   "the human comparison was on the same narrow distribution.",
   "'It is just predicting the next token' understates it and 'it "
   "understands language' overstates it; both are unsupported.",
   "Stop asking the general question and test specific capabilities, each "
   "of which is measurable.",
   "The load-bearing test is the sharpest: corrupt an intermediate step "
   "and see whether the answer changes.",
   "All three Semester 10 courses are about measurement, because in each "
   "the thing you want is a human judgement and the thing you have is a "
   "proxy.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What a score establishes"),
  ("callout", "A benchmark score is a statement about that dataset, that "
              "metric, and that split",
   ["<b>It establishes that this model, under this decoding "
    "configuration, scored this value on these examples by this "
    "measure</b> — <b>all four clauses, and none of them "
    "optional</b> (Module 09 &sect;4's reporting requirement).",
    "<b>It does not establish generalisation to your data</b>, unless "
    "your data happens to be distributed like the benchmark's — "
    "<b>which is an empirical question with a usually negative "
    "answer</b>, and one you can settle cheaply by evaluating on your "
    "own held-out set.",
    "<b>And it does not establish the <i>ability</i> the benchmark is "
    "named after</b>, because <b>a benchmark may be solvable by an "
    "artefact</b> — which Module 10 &sect;2's shortcut check "
    "detects, and which has invalidated several well-known datasets.",
    "<b>Nor does it rule out contamination</b> (Module 10 "
    "&sect;4) — <b>so a high score on a public benchmark is weak "
    "evidence</b>, and <b>your own held-out data, collected after the "
    "training cutoff, is considerably stronger</b> even if it is "
    "smaller."]),
  ("table", ["The claim", "The correction"],
   [["<b>'The model understands X.'</b>",
     "<b>It produces text consistent with understanding X on these "
     "inputs</b> — which is a narrower and checkable claim "
     "(&sect;3)."],
    ["<b>'It achieves human-level performance.'</b>",
     "<b>On this dataset, by this metric, against these particular "
     "annotators</b> — see the note."],
    ["<b>'It can reason.'</b>",
     "<b>It produces reasoning-shaped text</b>; <b>check whether the "
     "steps are load-bearing</b> (&sect;3's fourth test)."],
    ["<b>'It knows that P.'</b>",
     "<b>It asserts P here</b>; <b>check whether it asserts &not;P when "
     "asked differently</b> — consistency is the test."],
    ["<b>'Hallucination is being solved.'</b>",
     "<b>Rates are falling; the mechanism is structural</b> "
     "(Module 12 &sect;3), so a rate is not an elimination."],
    ["<b>'It scored 90%.'</b>",
     "<b>With which decoding, which prompt, and what variance across "
     "prompts?</b> (Module 09, Module 08 &sect;3.)"]],
   [0.34, 0.66]),
  ("p", "<b>The second row is the most consequential of these.</b> "
        "<b>'Human-level' invites a generalisation that the measurement "
        "does not support</b> — because <b>the human comparison was "
        "performed on the same narrow distribution</b>, frequently with "
        "annotators working quickly on an unfamiliar task, and <b>the "
        "model's failures are distributed quite differently from the "
        "humans'</b>. Matching an average on one dataset is not matching "
        "a capability. <b>This overclaim does the most damage in public "
        "discussion</b>, because the phrase travels and the caveats do "
        "not."),

  ("h1", "2 &nbsp; Claims you can defend"),
  ("ul", ["<b>'On 2,000 held-out examples from our own data, F1 is "
          "0.84, against a tuned BM25 baseline of 0.71, with a 95% "
          "confidence interval of &plusmn;0.02.'</b> <b>Checkable in "
          "every clause</b>, and it names the baseline "
          "(Module 10 &sect;2).",
          "<b>'Performance on dialectal inputs is 7 points lower than "
          "on standard inputs; that estimate is from 300 "
          "examples.'</b> <b>Disaggregated, with the sample size "
          "stated</b> so a reader can judge the comparison "
          "(Module 12 &sect;2).",
          "<b>'On questions our corpus cannot answer, the system "
          "abstains 62% of the time and fabricates an answer 38% of the "
          "time.'</b> <b>A measured failure rate</b> rather than a "
          "mitigation claim (Module 11 &sect;4).",
          "<b>'Results are with top-p 0.9 at temperature 0.7, averaged "
          "over five prompt phrasings; the variance across prompts is 3 "
          "points.'</b> <b>Which makes the result reproducible</b> "
          "(Module 09 &sect;4, Module 08 &sect;3).",
          "<b>And: 'we have not evaluated on inputs longer than 500 "
          "tokens, or in any language other than English.'</b> <b>The "
          "last one is the limitation statement</b>, and <b>it is what "
          "distinguishes a system report from a demonstration</b> — "
          "which is <b>Project 2's hardest-graded requirement</b>, "
          "because stating it requires knowing what you did not test."]),

  ("break",),
  ("h1", "3 &nbsp; Understanding"),
  ("callout", "The honest position is that the question is not settled and "
              "the evidence is specific",
   ["<b>'It is just predicting the next token' understates it.</b> "
    "<b>Predicting text well requires representations that support "
    "generalisation</b> — and probing finds real structure in the "
    "activations: syntactic dependency information, factual relations, "
    "and even spatial and temporal information. <b>Dismissing that as "
    "'just statistics' is not an argument.</b>",
    "<b>'It understands language' overstates it.</b> <b>Performance "
    "is brittle to paraphrase, sensitive to formatting, and inconsistent "
    "under rephrasing of the same question</b> — <b>which is not the "
    "profile of robust understanding</b>, and a system that answers "
    "differently depending on the word order has not represented the "
    "question.",
    "<b>So the useful move is to stop asking the general question and "
    "instead test specific capabilities:</b> <b>is the behaviour "
    "consistent under paraphrase? does it transfer to a novel "
    "composition of familiar parts? are the stated reasoning steps "
    "load-bearing?</b>",
    "<b>Each of those is measurable</b> — and <b>measuring them is "
    "considerably more informative than any position on the general "
    "question</b>, which is where this course asks you to put the effort. "
    "<b>The general question may not have a decidable answer; the "
    "specific ones do.</b>"]),
  ("ul", ["<b>Paraphrase consistency.</b> <b>Ask the same question in "
          "five different ways</b> — <b>a model that answers "
          "differently has not represented the question</b>, it has "
          "responded to the surface form.",
          "<b>Counterfactual sensitivity.</b> <b>Change the specific "
          "fact the answer depends upon, and check that the answer "
          "changes</b> — if it does not, the answer was not derived "
          "from the fact.",
          "<b>Compositional generalisation.</b> <b>Test a novel "
          "combination of familiar parts</b> — which is <b>where "
          "these systems reliably break</b>, and which is "
          "Module 01 &sect;1's compositionality row returning as an "
          "evaluation.",
          "<b>Load-bearing reasoning.</b> <b>Corrupt an intermediate "
          "step in a stated chain of reasoning and see whether the final "
          "answer changes</b> — <b>if it does not, the steps were "
          "decoration</b> rather than computation. <b>This is the "
          "sharpest of the five</b>, and it is cheap.",
          "<b>And contamination control:</b> <b>construct the test set "
          "from material postdating the training cutoff</b>, or <b>accept "
          "explicitly that you cannot rule contamination out</b> and say "
          "so (Module 10 &sect;4). <b>Reasoning-shaped text that does "
          "not affect the answer is a presentation</b>, and the test for "
          "it takes minutes."]),

  ("h1", "4 &nbsp; The semester, and where this leaves you"),
  ("table", ["Course", "What it covers", "The shared concern"],
   [["<b>CSCE 638 (this one)</b>",
     "<b>Language as an input and as an output.</b>",
     "<b>Evaluation that measures the thing you care about</b> rather "
     "than the thing that is easy (Module 10)."],
    ["<b>CSCE 676</b>",
     "<b>Finding structure in data at scale.</b>",
     "<b>Distinguishing a pattern that is real from one that was "
     "found</b> by looking long enough."],
    ["<b>CSCE 670</b>",
     "<b>Satisfying an information need.</b>",
     "<b>Relevance as a human judgement rather than a label</b> — "
     "and the proxies for it."]],
   [0.22, 0.34, 0.44]),
  ("p", "<b>All three are courses about measurement as much as about "
        "method</b> — <b>because in all three cases the thing you "
        "actually want is a human judgement and the thing you have is a "
        "proxy for it</b>: a relevance label, a cluster's coherence, a "
        "summary's quality. <b>Which makes the choose-the-metric-from-the-"
        "use discipline the semester's organising idea</b>, arriving from "
        "CSCE 633 Module 12 and applied three different ways."),
  ("callout", "Where this course leaves you",
   ["<b>You can explain the arc from counting to dense representations "
    "to recurrence to attention to pretraining, and say what each step "
    "bought and what it cost</b> — <b>which is considerably more "
    "durable than familiarity with any current architecture</b>, since "
    "the arc's logic survives the next architecture.",
    "<b>You can build a system:</b> <b>choose and adapt a pretrained "
    "model against real constraints, decode deliberately rather than by "
    "default, retrieve when the knowledge is external, and evaluate "
    "against a baseline that is genuinely hard to beat.</b>",
    "<b>And you know the characteristic failure of everything in this "
    "course</b> — <b>fluent, confident, and wrong</b> — along "
    "with <b>why it is structural rather than incidental</b> "
    "(Module 12 &sect;3) <b>and which mitigations actually reduce "
    "it.</b>",
    "<b>The closing rule is the program's, unchanged across "
    "twenty-eight courses:</b> <b>state what you measured, state what "
    "you assumed, and never claim more than you established.</b> <b>In "
    "this subject it means naming the dataset, the metric, the decoding "
    "configuration, and the inputs you did not test</b> — because "
    "<b>'it understands' names none of them</b>, and &sect;1's table is "
    "what happens when that substitution goes unchallenged."]),
 ],
 "resources": [
   ("Bender & Koller &mdash; Climbing towards NLU (free)",
    "https://aclanthology.org/2020.acl-main.463/",
    "<b>&sect;3's question, argued from the sceptical side</b> — and "
    "worth rereading now that you have Module 07's evidence."),
   ("Rogers et al. &mdash; A Primer in BERTology (free)",
    "https://aclanthology.org/2020.tacl-1.54/",
    "<b>&sect;3's probing evidence, surveyed</b> — what has actually "
    "been found in the representations, with the caveats."),
   ("Turpin et al. &mdash; Language Models Don't Always Say What They "
    "Think (free)",
    "https://arxiv.org/abs/2305.04388",
    "<b>&sect;3's load-bearing test, applied</b> — stated reasoning "
    "that does not determine the answer."),
   ("Raji et al. &mdash; AI and the Everything in the Whole Wide World "
    "Benchmark (free)",
    "https://arxiv.org/abs/2111.15366",
    "<b>&sect;1's argument</b> — why a benchmark cannot establish a "
    "general capability, developed properly."),
 ],
 "exercises": [
   "<b>Take a published claim about a model</b> and rewrite it in "
   "§1's four-clause form.",
   "<b>Find a 'human-level' claim</b> and identify what the human "
   "comparison actually measured.",
   "<b>Write the defensible claim</b> for your own Project 2 system.",
   "<b>Write its limitation statement</b> — the inputs you did not "
   "test.",
   "<b>Run the paraphrase consistency test</b> with five phrasings of "
   "one question.",
   "<b>Run the counterfactual test</b> on a fact-dependent answer.",
   "<b>Construct a novel composition of familiar parts</b> and test "
   "it.",
   "<b>Corrupt an intermediate reasoning step</b> and check whether the "
   "answer changes.",
   "<b>Revisit Module 01's last exercise</b> and compare your "
   "predictions against what you met.",
   "<b>Project 2 is now due.</b> Submit the task and its decision, the "
   "tuned baseline, your system, the metric justification, the twenty-error "
   "analysis, and the failure and limitation statement.",
 ],
 "selfcheck": [
   "What four clauses does a benchmark score require?",
   "What does it not establish — give three things?",
   "Give six overclaims and the correction to each.",
   "Why is 'human-level' the most consequential?",
   "Give four defensible claim forms.",
   "What distinguishes a system report from a demonstration?",
   "Why is 'just predicting the next token' an understatement?",
   "Why is 'it understands language' an overstatement?",
   "Give the five discriminating tests and the sharpest one.",
   "What do the three Semester 10 courses share?",
 ],
},

]
