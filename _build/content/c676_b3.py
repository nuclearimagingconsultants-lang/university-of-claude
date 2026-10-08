# -*- coding: utf-8 -*-
"""CSCE 676 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Anomaly Detection",
 "subtitle": "Unusual compared to what?",
 "question": "Which records do not belong, and how would you know?",
 "outcomes": [
     "Explain the three problem settings and why they differ.",
     "Explain the method families and their assumptions.",
     "Explain the base rate problem in this setting.",
     "Explain why evaluation is especially hard here.",
     "Deploy a detector with a defensible threshold.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Three problems",
   "blurb": "Usually conflated, and genuinely different."},

  {"t": "table", "kicker": "Settings", "title": "The three settings",
   "header": ["Setting", "What you have", "What follows"],
   "widths": [2.7, 4.0, 5.1],
   "rows": [
     ["<b>Unsupervised</b>", "<b>Unlabelled data, assumed mostly normal</b>", "<b>You find outliers, not anomalies you care about</b>"],
     ["<b>Semi-supervised</b>", "<b>Clean normal data only</b>", "<b>You model normality and flag departures</b>"],
     ["<b>Supervised</b>", "<b>Labelled examples of both</b>", "<b>It is imbalanced classification (CSCE 633)</b>"],
   ],
   "footnote": "<b>The third row is the one to recognise:</b> if you "
               "have labels, this is a classification problem with a "
               "class imbalance, and the anomaly detection literature is "
               "the wrong one to read.",
   "note": "Identifying the supervised case saves people a great deal "
           "of wasted effort."},

  {"t": "callout", "title": "Statistically unusual and operationally interesting are different properties",
   "kind": "The distinction that determines whether this works",
   "body": ["<b>An unsupervised detector finds records far from the "
            "rest of the distribution</b> — which includes "
            "<b>measurement errors, missing-value sentinels, duplicated "
            "rows, and legitimate rare events</b>, as well as whatever "
            "you were looking for.",
            "<b>And the ratio is unfavourable.</b> <b>In most real "
            "data, the top outliers are overwhelmingly data quality "
            "problems</b> — which is a useful finding and is not the "
            "one you wanted.",
            "<b>So the first run of any detector is a data cleaning "
            "exercise</b>, and expecting otherwise is the commonest "
            "disappointment with these methods.",
            "<b>Which means you need to specify what kind of unusual "
            "you care about</b> — <b>a feature set that excludes the "
            "artefacts, or a semi-supervised setup with clean normal "
            "data</b>, both of which require knowing the domain."]},

  {"t": "section", "label": "Part 2", "title": "The methods",
   "blurb": "Each with an assumption about what normal means."},

  {"t": "code", "kicker": "Families", "title": "The families, and what each assumes",
   "lang": "text", "code": """
  STATISTICAL
      fit a distribution, flag the low-probability
      tail. Assumes you know the distribution.
      Robust versions use the median and MAD rather
      than the mean and standard deviation, because
      the outliers corrupt the estimate otherwise.

  DISTANCE AND DENSITY
      kNN distance, or Local Outlier Factor, which
      compares a point's density to its neighbours'.
      LOF handles varying density; both suffer from
      Module 05's distance concentration.

  ISOLATION-BASED
      Isolation Forest: random splits isolate
      outliers in fewer splits than inliers. Fast,
      scales, few assumptions, and it is the right
      default for tabular data.

  RECONSTRUCTION
      autoencoder or PCA residual: flag what the
      model cannot reconstruct. Assumes normal data
      lies on a learnable manifold.

  AND EACH DEFINES "normal" DIFFERENTLY, so they
  disagree -- which is Module 04's situation again.
""",
   "caption": "<b>Isolation Forest is the right default for tabular "
              "data</b> — few assumptions, near-linear, and it "
              "degrades gracefully in high dimension.",
   "note": "Give a default; students otherwise try everything."},

  {"t": "section", "label": "Part 3", "title": "The base rate",
   "blurb": "Which makes most detectors unusable as deployed."},

  {"t": "eq", "kicker": "Precision", "title": "The arithmetic that governs deployment",
   "eqs": [
     ("precision = TP / (TP + FP)",
      "What fraction of flagged records are real. The number a "
      "human reviewer experiences."),
     ("base rate 0.1%, recall 90%, FPR 1%  ⟹  precision ≈ 8%",
      "So 92 of every 100 alerts are false, with a detector that "
      "sounds excellent."),
     ("base rate 0.01%  ⟹  precision ≈ 0.9%",
      "A tenfold rarer event makes it unusable. The same detector."),
   ],
   "caption": "<b>Precision depends on the base rate, and the base "
              "rate is usually tiny</b> — which is why a "
              "99%-accurate detector produces mostly false "
              "positives.",
   "note": "This is CSCE 701 §12's arithmetic, in its original "
           "setting."},

  {"t": "callout", "title": "So the design question is review capacity, not detector accuracy",
   "kind": "What follows from the arithmetic",
   "body": ["<b>Work backwards from how many records a person can "
            "review per day</b> — and <b>set the threshold so the "
            "alert volume matches it</b>, then report the recall you "
            "achieved at that volume.",
            "<b>Which inverts the usual framing.</b> <b>'What recall "
            "can we get at 50 alerts per day' is answerable and "
            "actionable; 'what is our AUC' is neither.</b>",
            "<b>And correlate weak signals rather than improving one "
            "detector</b> — <b>three independent weak signals on one "
            "record beats any of them</b>, because the base rate "
            "improves multiplicatively "
            "(CSCE 701 §09 §3).",
            "<b>Or change the problem:</b> <b>rank rather than "
            "classify, and give a reviewer the top k with the reasons "
            "attached</b> — which is a usable system where a classifier "
            "is not."]},

  {"t": "section", "label": "Part 4", "title": "Evaluation",
   "blurb": "Which is harder here than anywhere else in the course."},

  {"t": "bullets", "kicker": "Evaluation", "title": "Why, and what to do instead",
   "items": [
     "<b>You have almost no labels</b>, and the few you have are "
     "the anomalies somebody already found — <b>which biases the "
     "set toward the easy ones.</b>",
     "",
     "<b>Accuracy is useless.</b> <b>Predicting 'normal' always "
     "gives 99.9% accuracy</b>, so report precision and recall at a "
     "specific threshold.",
     "",
     "<b>AUC flatters.</b> <b>It averages over thresholds you "
     "would never use</b> — prefer precision at the k you can "
     "actually review, or average precision.",
     "",
     "<b>And injected synthetic anomalies are easier than real "
     "ones</b>, so a detector evaluated on them is "
     "overstated.",
     "",
     "<b>What works:</b> <b>precision at k by expert review, plus "
     "the time to detection on historical incidents you "
     "know about.</b>",
   ],
   "footnote": "<b>Time to detection on known past incidents is the "
               "most convincing evaluation available</b> — it uses "
               "real anomalies and measures the thing the system is for."},

  {"t": "callout", "title": "And the honest summary of this material",
   "kind": "Closing",
   "body": ["<b>Anomaly detection is reliably oversold</b>, because "
            "<b>the methods are easy to run and the base rate makes them "
            "hard to deploy</b> — and the gap is invisible until "
            "somebody reviews the alerts.",
            "<b>It works best where the base rate is not "
            "tiny</b> — quality control, systems monitoring, and data "
            "cleaning — and worst where it is, which includes most "
            "fraud and security framing.",
            "<b>And it works best as a ranking fed to an expert</b>, "
            "rather than as a decision.",
            "<b>So the claim to make is narrow:</b> <b>'at 50 alerts "
            "per day, the detector surfaces 30% of known incidents a "
            "median of 4 hours earlier'</b> — <b>which is checkable "
            "and modest</b>, and is what Module 13 asks for."]},
 ],
 "takeaways": [
   "If you have labels for both classes, this is imbalanced "
   "classification, and the anomaly detection literature is the wrong one.",
   "Statistically unusual and operationally interesting are different, and "
   "the top outliers in real data are overwhelmingly data quality "
   "problems.",
   "Isolation Forest is the right default for tabular data — few "
   "assumptions, near-linear, and it degrades gracefully in high dimension.",
   "At a 0.1% base rate, 90% recall and a 1% false positive rate gives "
   "about 8% precision — so 92 of 100 alerts are false.",
   "The design question is review capacity rather than detector accuracy, "
   "which inverts the usual framing.",
   "Time to detection on known historical incidents is the most convincing "
   "evaluation available.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Three problems"),
  ("table", ["Setting", "What you have", "What follows"],
   [["<b>Unsupervised</b>",
     "<b>Unlabelled data, assumed to be mostly normal.</b>",
     "<b>You find statistical outliers, which are not necessarily the "
     "anomalies you care about</b> — see the callout."],
    ["<b>Semi-supervised (one-class)</b>",
     "<b>A clean sample of normal data, and nothing else.</b>",
     "<b>You model normality and flag departures from it</b>, which is "
     "a better-posed problem than the first row."],
    ["<b>Supervised</b>",
     "<b>Labelled examples of both normal and anomalous records.</b>",
     "<b>This is imbalanced classification</b> (CSCE 633) — see "
     "the note."]],
   [0.20, 0.34, 0.46]),
  ("p", "<b>The third row is the one to recognise early:</b> <b>if you "
        "have labels for both classes, this is a classification problem "
        "with a class imbalance, and the anomaly detection literature is "
        "the wrong one to read</b>. Use a classifier, handle the "
        "imbalance with the standard methods, and evaluate with precision "
        "and recall. <b>Identifying this case saves people a great deal "
        "of wasted effort</b>, because the unsupervised methods will "
        "underperform a straightforward classifier that uses the labels "
        "you already have."),
  ("callout", "Statistically unusual and operationally interesting are "
              "different properties",
   ["<b>An unsupervised detector finds records far from the rest of the "
    "distribution</b> — which includes <b>measurement errors, "
    "missing-value sentinels (the row where age is 999), duplicated rows, "
    "encoding failures, and genuinely legitimate rare events</b>, as well "
    "as whatever it was you were hoping to find.",
    "<b>And the ratio is unfavourable.</b> <b>In most real data, the "
    "top outliers are overwhelmingly data quality problems</b> — "
    "which is <b>a genuinely useful finding and is not the one you "
    "wanted</b>, and discovering it is a rite of passage with these "
    "methods.",
    "<b>So the first run of any detector is a data cleaning "
    "exercise</b>, and <b>expecting otherwise is the commonest "
    "disappointment with this material</b>. Budget for it, and treat the "
    "cleaning as a deliverable.",
    "<b>Which means you have to specify what kind of unusual you care "
    "about</b> — <b>a feature set that excludes the artefacts, or a "
    "semi-supervised setup with verified clean normal data</b> — "
    "<b>both of which require knowing the domain</b>, and neither of "
    "which is a modelling decision you can make from the data alone."]),

  ("h1", "2 &nbsp; The methods"),
  ("code", """STATISTICAL
    fit a distribution, flag the low-probability tail.
    Assumes you know the distribution. Robust versions
    use the median and the median absolute deviation
    rather than the mean and standard deviation,
    because the outliers corrupt those estimates --
    which is the whole point of robust statistics.

DISTANCE AND DENSITY
    kNN distance, or Local Outlier Factor, which
    compares a point's local density to its
    neighbours'. LOF handles varying density; both
    suffer from Module 05's distance concentration in
    high dimension.

ISOLATION-BASED
    Isolation Forest: random splits isolate outliers
    in fewer splits than inliers. Fast, near-linear,
    few assumptions, and the right default for
    tabular data.

RECONSTRUCTION
    autoencoder or PCA residual: flag whatever the
    model cannot reconstruct well. Assumes normal
    data lies on a learnable manifold.

AND EACH DEFINES "normal" DIFFERENTLY, so they
disagree -- which is Module 04's situation again."""),
  ("p", "<b>Isolation Forest is the right default for tabular "
        "data</b> — <b>few assumptions, near-linear time, and it "
        "degrades gracefully in high dimension</b> where the distance-based "
        "methods degrade badly (Module 05 &sect;1). <b>Giving a default "
        "is worth doing</b>, because the alternative is trying all four "
        "families and then having no principled way to choose between "
        "their disagreeing outputs — which is Module 04 "
        "&sect;3's circularity in a new setting."),

  ("break",),
  ("h1", "3 &nbsp; The base rate"),
  ("eq", "precision = TP / (TP + FP)"),
  ("ul", ["<b>Precision is the fraction of flagged records that are "
          "genuinely anomalous</b> — and it is <b>the number a human "
          "reviewer actually experiences</b>, which is why it governs "
          "whether a system is usable.",
          "<b>With a base rate of 0.1%, a recall of 90%, and a false "
          "positive rate of 1%, the precision is about 8%</b> — so "
          "<b>92 of every 100 alerts are false</b>, from a detector whose "
          "stated performance sounds excellent.",
          "<b>And at a base rate of 0.01%, the precision falls to "
          "about 0.9%</b> — <b>a tenfold rarer event makes the same "
          "detector unusable</b>, with no change to the detector at all. "
          "<b>The detector's quality did not move; the deployment "
          "became impossible.</b>",
          "<b>Which is why a 99%-accurate detector produces mostly "
          "false positives on rare events</b> — and <b>this is "
          "CSCE 701 Module 09 &sect;3's arithmetic, in its original "
          "setting</b>, where it was first understood and is still most "
          "often ignored."]),
  ("callout", "So the design question is review capacity, not detector "
              "accuracy",
   ["<b>Work backwards from how many records a person can realistically "
    "review per day</b> — and <b>set the threshold so that the alert "
    "volume matches that capacity</b>, then <b>report the recall you "
    "achieved at that volume.</b>",
    "<b>Which inverts the usual framing entirely.</b> <b>'What recall "
    "can we achieve at fifty alerts per day' is answerable and "
    "actionable; 'what is our AUC' is neither</b>, because it does not "
    "correspond to any deployment you would choose.",
    "<b>And correlate weak signals rather than trying to improve a "
    "single detector</b> — <b>three independent weak signals on the "
    "same record beats any one of them substantially</b>, because the "
    "base rate improves multiplicatively while the recall falls only "
    "somewhat (CSCE 701 Module 09 &sect;3).",
    "<b>Or change the problem altogether:</b> <b>rank rather than "
    "classify, and present a reviewer with the top k ranked records with "
    "the reasons attached</b> — <b>which is a usable system in "
    "circumstances where a classifier is not</b>, and is how most "
    "successful deployments of this material actually work."]),

  ("h1", "4 &nbsp; Evaluation"),
  ("ul", ["<b>You have almost no labels</b>, and <b>the few you have "
          "are the anomalies somebody already found</b> — <b>which "
          "biases the evaluation set toward the easy ones</b> and "
          "systematically overstates performance on the hard cases that "
          "matter.",
          "<b>Accuracy is useless here.</b> <b>Predicting 'normal' "
          "for everything gives 99.9% accuracy</b> at a 0.1% base rate, "
          "<b>so report precision and recall at a specific threshold</b> "
          "and never an accuracy figure.",
          "<b>AUC flatters.</b> <b>It averages over thresholds you "
          "would never actually use</b> — including those producing "
          "thousands of alerts — so <b>prefer precision at the k you "
          "can genuinely review, or average precision</b>, which weights "
          "the useful region.",
          "<b>And injected synthetic anomalies are systematically "
          "easier than real ones</b>, because you generated them from "
          "your own idea of what anomalous looks like — <b>so a "
          "detector evaluated on them is overstated</b>, frequently by a "
          "large factor.",
          "<b>What works:</b> <b>precision at k established by expert "
          "review of the top k, plus the time to detection on historical "
          "incidents you know about.</b> <b>Time to detection on known "
          "past incidents is the most convincing evaluation "
          "available</b> — it uses real anomalies, requires no new "
          "labelling, and measures the thing the system is actually "
          "for."]),
  ("callout", "And the honest summary of this material",
   ["<b>Anomaly detection is reliably oversold</b>, because <b>the "
    "methods are easy to run and the base rate makes them hard to "
    "deploy</b> — and <b>the gap between those two facts is "
    "invisible until somebody actually reviews the alerts</b>, which is "
    "usually after the system has been bought.",
    "<b>It works best where the base rate is not tiny</b> — "
    "manufacturing quality control, systems monitoring, and data "
    "cleaning — <b>and worst where it is</b>, which unfortunately "
    "includes most fraud and security framings, where it is most often "
    "proposed.",
    "<b>And it works best as a ranking presented to an expert rather "
    "than as a decision</b> (&sect;3) — which is a smaller claim "
    "about the technology and a more defensible system.",
    "<b>So the claim to make is narrow:</b> <b>'at fifty alerts per "
    "day, the detector surfaces 30% of known incidents a median of four "
    "hours earlier than they were otherwise found'</b> — <b>which is "
    "checkable, modest, and genuinely useful</b>, and is exactly the form "
    "Module 13 asks for."]),
 ],
 "resources": [
   ("Aggarwal &mdash; Outlier Analysis, 2nd edition",
    "https://link.springer.com/book/10.1007/978-3-319-47578-3",
    "<b>The whole module</b> — and its chapter on evaluation is the "
    "most honest treatment available. Library copy."),
   ("Liu, Ting & Zhou &mdash; Isolation Forest (free)",
    "https://ieeexplore.ieee.org/document/4781136",
    "<b>&sect;2's default method in the original</b> — short, and the "
    "intuition is well explained."),
   ("Breunig et al. &mdash; LOF: Identifying Density-Based Local "
    "Outliers (free)",
    "https://dl.acm.org/doi/10.1145/342009.335388",
    "<b>&sect;2's density row</b> — and the varying-density problem "
    "it was designed to solve."),
   ("Campos et al. &mdash; On the evaluation of unsupervised outlier "
    "detection (free)",
    "https://link.springer.com/article/10.1007/s10618-015-0444-8",
    "<b>&sect;4's problem, measured</b> — a systematic study showing "
    "how much the evaluation choices change the conclusions."),
 ],
 "exercises": [
   "<b>Classify your own problem</b> into one of the three settings, and "
   "say what follows.",
   "<b>Run a detector on a real dataset</b> and read the top fifty "
   "outliers.",
   "<b>Categorise them</b> as data quality, legitimate rare events, or "
   "interesting.",
   "<b>Run all four method families</b> and measure how much their top "
   "fifty overlap.",
   "<b>Compute precision</b> at base rates of 1%, 0.1%, and 0.01% with "
   "fixed recall and FPR.",
   "<b>Set a threshold from a stated review capacity</b> and report the "
   "recall you get.",
   "<b>Correlate three weak detectors</b> and measure the precision "
   "improvement.",
   "<b>Compute accuracy, AUC, and precision at k</b> for one detector, "
   "and say which you would report.",
   "<b>Inject synthetic anomalies and compare</b> the detector's "
   "performance against its performance on real ones.",
   "<b>Measure time to detection</b> on an incident you know the date "
   "of.",
 ],
 "selfcheck": [
   "Name the three settings and what follows from each.",
   "Which should you recognise immediately, and why?",
   "Why are statistically unusual and operationally interesting "
   "different?",
   "What are the top outliers in real data usually?",
   "Name four method families and what each assumes.",
   "Which is the right default, and why?",
   "Give the precision arithmetic at a 0.1% base rate.",
   "What is the right design question, and how does it invert the usual "
   "framing?",
   "Give four reasons evaluation is hard here.",
   "What is the most convincing evaluation available?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Recommendation",
 "subtitle": "The worked system, and its specific traps.",
 "question": "What should this user see next?",
 "outcomes": [
     "Explain collaborative and content-based approaches.",
     "Explain matrix factorisation and the implicit feedback "
     "problem.",
     "Explain cold start and popularity bias.",
     "Explain why offline evaluation misleads here.",
     "Build and evaluate a recommender honestly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two approaches",
   "blurb": "And they fail in complementary ways."},

  {"t": "table", "kicker": "Approaches", "title": "Collaborative and content-based",
   "header": ["", "Collaborative", "Content-based"],
   "widths": [2.6, 4.2, 4.6],
   "rows": [
     ["<b>Uses</b>", "<b>Who liked what</b>", "<b>Item attributes</b>"],
     ["<b>Strength</b>", "<b>Finds surprising connections</b>", "<b>Works for a new item immediately</b>"],
     ["<b>Cold start</b>", "<b>Fails for new users and new items</b>", "<b>Fails for new users only</b>"],
     ["<b>Bias</b>", "<b>Toward the popular</b>", "<b>Toward the similar — a filter bubble</b>"],
     ["<b>Needs</b>", "<b>A lot of interaction data</b>", "<b>Good item features</b>"],
   ],
   "footnote": "<b>So real systems are hybrid</b> — "
               "content-based for the cold start and collaborative once "
               "there is interaction data, with the switch being a design "
               "decision.",
   "note": "The complementary-failure framing explains why hybrids "
           "dominate."},

  {"t": "callout", "title": "Collaborative filtering's strength is finding connections nobody could specify",
   "kind": "Why it works at all",
   "body": ["<b>It needs no understanding of the items.</b> <b>If "
            "users who liked A also liked B, that is enough</b> — "
            "and the connection may have no describable "
            "feature behind it.",
            "<b>Which is genuinely powerful</b>, because <b>the "
            "features that predict taste are frequently not the features "
            "anybody would have thought to record.</b>",
            "<b>And it is the same distributional argument as "
            "CSCE 638 §04's</b> — <b>meaning from "
            "co-occurrence</b>, applied to preferences rather than to "
            "words.",
            "<b>With the same limitation:</b> <b>it cannot say "
            "anything about an item nobody has interacted "
            "with</b> — which is the cold start problem and is "
            "structural rather than incidental."]},

  {"t": "section", "label": "Part 2", "title": "Matrix factorisation",
   "blurb": "And what implicit feedback changes."},

  {"t": "eq", "kicker": "Factorisation", "title": "The model, and the objective",
   "eqs": [
     ("r̂ᵤᵢ = μ + bᵤ + bᵢ + pᵤ · qᵢ",
      "A global mean, a user bias, an item bias, and a latent factor "
      "interaction. The biases matter more than people expect."),
     ("minimise Σ over OBSERVED (rᵤᵢ − r̂ᵤᵢ)² + λ(‖pᵤ‖² + ‖qᵢ‖²)",
      "Summed over observed entries only, which is what distinguishes "
      "this from SVD (Module 05)."),
     ("so it is not an SVD",
      "SVD requires a complete matrix. This is a regularised fit to "
      "the observed entries, solved by SGD or ALS."),
   ],
   "caption": "<b>The sum is over observed entries only</b>, which is "
              "why this cannot be solved by a standard decomposition.",
   "note": "The not-actually-SVD point is a common confusion worth "
           "clearing."},

  {"t": "callout", "title": "Implicit feedback changes the problem, because a missing entry is ambiguous",
   "kind": "The practically important distinction",
   "body": ["<b>Explicit ratings are rare and noisy; clicks, views, "
            "and purchases are abundant</b> — so real systems use "
            "implicit feedback almost exclusively.",
            "<b>But an absent interaction is not a negative "
            "rating.</b> <b>The user may dislike the item, or may never "
            "have seen it</b> — and the two are not "
            "distinguishable from the data.",
            "<b>So the standard approach treats all unobserved pairs "
            "as weak negatives with a confidence weight</b>, or samples "
            "negatives and optimises a ranking objective "
            "directly.",
            "<b>And it means the objective changes:</b> <b>you are "
            "ranking rather than predicting a value</b> — so <b>squared "
            "error on held-out ratings is the wrong metric</b>, which "
            "is Part 4."]},

  {"t": "section", "label": "Part 3", "title": "Cold start and bias",
   "blurb": "The two structural problems."},

  {"t": "bullets", "kicker": "Problems", "title": "What goes wrong structurally",
   "items": [
     "<b>New user cold start.</b> <b>No history, so no "
     "collaborative signal</b> — addressed by onboarding "
     "questions, demographic priors, or popular defaults, all of which "
     "are weak.",
     "",
     "<b>New item cold start.</b> <b>No interactions, so it "
     "cannot be recommended, so it gets no interactions</b> — a "
     "feedback loop that content features break.",
     "",
     "<b>Popularity bias.</b> <b>Popular items have more data, so "
     "they are recommended more, so they get more data</b> — "
     "<b>which the system amplifies rather than "
     "reflects.</b>",
     "",
     "<b>And the feedback loop.</b> <b>Your training data is the "
     "output of your previous recommender</b>, so the model learns from "
     "its own choices.",
     "",
     "<b>Which makes the logged data not a sample of "
     "preferences</b> but a sample of what you showed.",
   ],
   "footnote": "<b>The feedback loop is the deepest of these</b> "
               "— it means your offline evaluation data was "
               "generated by the policy you are trying to "
               "improve on."},

  {"t": "section", "label": "Part 4", "title": "Evaluation",
   "blurb": "Where this field has been embarrassed."},

  {"t": "callout", "title": "Offline evaluation on logged data systematically favours what the old system did",
   "kind": "The problem, stated plainly",
   "body": ["<b>You can only evaluate recommendations the user "
            "actually saw</b> — so <b>a new system that recommends "
            "something good and unshown scores zero for it</b>, and a "
            "system that imitates the old one scores well.",
            "<b>Which biases offline evaluation toward the "
            "status quo</b>, and is why offline gains frequently fail to "
            "appear in an online test.",
            "<b>And the replication findings are "
            "stark:</b> <b>several years of reported neural "
            "recommender improvements did not survive comparison against "
            "properly tuned simple baselines</b> "
            "(Module 13).",
            "<b>So: use ranking metrics, report popularity bias and "
            "coverage, correct for the logging policy where you can, and "
            "test online if the decision matters</b> — which is the "
            "honest programme."]},

  {"t": "bullets", "kicker": "Metrics", "title": "What to measure",
   "items": [
     "<b>Ranking metrics at a realistic k</b> — "
     "precision@k, recall@k, and NDCG — <b>not RMSE, which "
     "measures the wrong thing</b> for a ranked list.",
     "",
     "<b>Coverage:</b> <b>what fraction of the catalogue is ever "
     "recommended?</b> A system recommending 200 items out of a million "
     "is doing something you should know about.",
     "",
     "<b>Popularity bias:</b> <b>the recommended items' popularity "
     "distribution against the catalogue's</b>, which quantifies "
     "Part 3's amplification.",
     "",
     "<b>Diversity and novelty within a list</b>, since a list of "
     "ten near-identical items is worse than its per-item scores "
     "suggest.",
     "",
     "<b>And a properly tuned simple baseline</b> — "
     "<b>popularity, and item-item nearest neighbours</b> — which "
     "is the requirement most often skipped.",
   ],
   "footnote": "<b>Item-item nearest neighbours, properly tuned, is "
               "the baseline that has embarrassed a decade of published "
               "work</b> — so run it first."},
 ],
 "takeaways": [
   "Collaborative and content-based approaches fail in complementary ways, "
   "which is why real systems are hybrid.",
   "Collaborative filtering finds connections nobody could specify, which "
   "is CSCE 638's distributional argument applied to preferences.",
   "Matrix factorisation sums over observed entries only, which is why it "
   "is not an SVD.",
   "An absent interaction is ambiguous between dislike and never having "
   "seen it, which changes the objective to ranking.",
   "Your training data is the output of your previous recommender, so the "
   "logged data samples what you showed rather than what people prefer.",
   "Item-item nearest neighbours, properly tuned, is the baseline that has "
   "embarrassed a decade of published work.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two approaches"),
  ("table", ["", "Collaborative filtering", "Content-based"],
   [["<b>What it uses</b>", "<b>Who liked what</b> — the "
     "interaction matrix only.",
     "<b>Item attributes</b> — text, metadata, categories, "
     "features."],
    ["<b>Its strength</b>",
     "<b>Finds surprising connections nobody could specify</b> — see "
     "the callout.",
     "<b>Works for a brand-new item immediately</b>, with no "
     "interactions at all."],
    ["<b>Cold start</b>",
     "<b>Fails for new users <i>and</i> new items.</b>",
     "<b>Fails for new users only</b> — which is half the problem "
     "solved."],
    ["<b>Its bias</b>",
     "<b>Toward whatever is popular</b> (&sect;3).",
     "<b>Toward whatever is similar</b> — the filter bubble, which "
     "is a different failure."],
    ["<b>What it needs</b>", "<b>A great deal of interaction data.</b>",
     "<b>Good item features</b>, which someone has to produce and "
     "maintain."]],
   [0.20, 0.40, 0.40]),
  ("p", "<b>So real systems are hybrid</b> — <b>content-based for "
        "the cold start and collaborative once there is enough interaction "
        "data, with the switch between them being an explicit design "
        "decision</b> rather than an emergent one. <b>The "
        "complementary-failure framing explains why hybrids dominate "
        "practice</b> even though the research literature treats the two "
        "families separately."),
  ("callout", "Collaborative filtering's strength is finding connections "
              "nobody could specify",
   ["<b>It requires no understanding of the items whatsoever.</b> "
    "<b>If users who liked A also liked B, that is sufficient</b> — "
    "and <b>the connection may have no describable feature behind it at "
    "all</b>, which is the whole appeal.",
    "<b>Which is genuinely powerful</b>, because <b>the features that "
    "predict taste are frequently not the features anybody would have "
    "thought to record</b> — and a content-based system can only use "
    "features somebody chose to capture.",
    "<b>And it is the same distributional argument as CSCE 638 "
    "Module 04's</b> — <b>meaning from co-occurrence</b>, applied "
    "to preferences instead of to words, with the same mathematics "
    "(matrix factorisation of a co-occurrence structure) underneath.",
    "<b>With the same limitation, too:</b> <b>it cannot say anything "
    "at all about an item nobody has interacted with</b> — which is "
    "the cold start problem (&sect;3) and is <b>structural rather than "
    "incidental</b>, exactly as a word absent from the corpus has no "
    "embedding."]),

  ("h1", "2 &nbsp; Matrix factorisation"),
  ("eq", "r&#770;<sub>ui</sub> = &mu; + b<sub>u</sub> + b<sub>i</sub> + "
         "p<sub>u</sub> &middot; q<sub>i</sub>"),
  ("ul", ["<b>A global mean, a user bias, an item bias, and a latent "
          "factor interaction.</b> <b>The bias terms matter considerably "
          "more than people expect</b> — modelling that some users "
          "rate generously and some items are generally liked captures a "
          "large share of the variance before any factors are involved.",
          "<b>The objective is summed over the <i>observed</i> entries "
          "only</b>, with regularisation on the factors — <b>which "
          "is precisely what distinguishes this from the SVD of "
          "Module 05</b>.",
          "<b>So it is not an SVD</b>, despite being universally "
          "described as one. <b>SVD requires a complete matrix; this is "
          "a regularised fit to the observed entries</b>, solved by "
          "stochastic gradient descent or by alternating least "
          "squares. <b>The not-actually-SVD point is a common confusion "
          "worth clearing up</b>, because it explains why the "
          "Eckart&ndash;Young guarantee does not apply here.",
          "<b>And the regularisation is doing real work</b>, because "
          "the observed entries are a tiny and non-random fraction of the "
          "matrix — which is &sect;3's feedback loop arriving as a "
          "fitting problem."]),
  ("callout", "Implicit feedback changes the problem, because a missing "
              "entry is ambiguous",
   ["<b>Explicit ratings are rare, noisy, and unrepresentative; clicks, "
    "views, plays, and purchases are abundant</b> — so <b>real "
    "systems use implicit feedback almost exclusively</b>, and the "
    "explicit-rating literature describes a setting that mostly no longer "
    "exists.",
    "<b>But an absent interaction is not a negative rating.</b> "
    "<b>The user may dislike the item, or may simply never have seen "
    "it</b> — and <b>the two are not distinguishable from the logged "
    "data</b>, which is the central difficulty.",
    "<b>So the standard approaches are either to treat all unobserved "
    "pairs as weak negatives with a confidence weight</b> — "
    "weighting observed interactions by their strength — <b>or to "
    "sample negatives and optimise a ranking objective directly</b>, as "
    "in Bayesian personalised ranking.",
    "<b>And it means the objective changes fundamentally:</b> <b>you "
    "are producing a ranking rather than predicting a value</b> — so "
    "<b>squared error on held-out ratings is measuring the wrong "
    "thing</b>, which is &sect;4's first metric point and is still a "
    "common mistake."]),

  ("break",),
  ("h1", "3 &nbsp; Cold start and bias"),
  ("ul", ["<b>New user cold start.</b> <b>No history, so no "
          "collaborative signal exists</b> — addressed by onboarding "
          "questions, demographic priors, or popular defaults, <b>all of "
          "which are weak</b> and all of which annoy the user to some "
          "degree.",
          "<b>New item cold start.</b> <b>No interactions, so it "
          "cannot be recommended, so it receives no interactions</b> "
          "— <b>a self-reinforcing feedback loop that content "
          "features break</b> and that pure collaborative filtering "
          "cannot escape.",
          "<b>Popularity bias.</b> <b>Popular items have more "
          "interaction data, so they are predicted more confidently, so "
          "they are recommended more, so they accumulate more "
          "data</b> — <b>which means the system amplifies the "
          "popularity distribution rather than merely reflecting it.</b>",
          "<b>And the feedback loop, which is the general case.</b> "
          "<b>Your training data is the output of your previous "
          "recommender</b>, so <b>the model learns from its own past "
          "choices</b> rather than from independent evidence about "
          "preferences.",
          "<b>Which makes the logged data not a sample of user "
          "preferences but a sample of what you chose to show.</b> "
          "<b>The feedback loop is the deepest of these problems</b> "
          "— <b>it means your offline evaluation data was generated "
          "by the very policy you are trying to improve on</b>, which is "
          "&sect;4's subject and is not fixable by a better model."]),

  ("h1", "4 &nbsp; Evaluation"),
  ("callout", "Offline evaluation on logged data systematically favours what "
              "the old system did",
   ["<b>You can only evaluate recommendations the user actually "
    "saw</b> — there is no record of what they would have thought of "
    "anything else — so <b>a new system that recommends something "
    "genuinely good but previously unshown scores zero for it</b>, and "
    "<b>a system that imitates the old one scores well.</b>",
    "<b>Which biases offline evaluation systematically toward the "
    "status quo</b>, and <b>is why offline gains frequently fail to "
    "appear in an online A/B test</b> — a mismatch that is routine "
    "and widely underreported.",
    "<b>And the replication findings here are stark:</b> <b>several "
    "years of reported neural recommender improvements did not survive "
    "comparison against properly tuned simple baselines</b> — a "
    "result reproduced across multiple surveys, and one of the cleanest "
    "examples of Module 13's problem in any field.",
    "<b>So: use ranking metrics at a realistic k, report popularity "
    "bias and catalogue coverage, correct for the logging policy where "
    "you can (inverse propensity weighting), and test online if the "
    "decision matters</b> — <b>which is the honest programme</b>, "
    "and each step is achievable."]),
  ("ul", ["<b>Ranking metrics at a realistic k</b> — "
          "precision@k, recall@k, and NDCG, where k is the number of "
          "items you actually show — <b>not RMSE, which measures the "
          "wrong thing for a ranked list</b> (&sect;2).",
          "<b>Coverage:</b> <b>what fraction of the catalogue is ever "
          "recommended to anybody?</b> <b>A system recommending two "
          "hundred items out of a million is doing something you should "
          "know about</b>, and no accuracy metric reveals it.",
          "<b>Popularity bias:</b> <b>plot the recommended items' "
          "popularity distribution against the catalogue's</b>, which "
          "<b>quantifies &sect;3's amplification</b> and turns a concern "
          "into a number.",
          "<b>Diversity and novelty within a single list</b>, since "
          "<b>a list of ten near-identical items is worse than its "
          "per-item scores suggest</b> — the list is the unit the "
          "user experiences, and per-item metrics do not see it.",
          "<b>And a properly tuned simple baseline</b> — "
          "<b>popularity, and item-item nearest neighbours</b> — "
          "which is <b>the requirement most often skipped</b> and the one "
          "the replication work turned on. <b>Item-item nearest "
          "neighbours, properly tuned, is the baseline that has "
          "embarrassed a decade of published work</b>, so <b>run it "
          "first</b> and know what you have to beat."]),
 ],
 "resources": [
   ("Mining of Massive Datasets, chapter 9 (free)",
    "http://www.mmds.org/",
    "<b>&sect;1 and &sect;2</b>, with the collaborative filtering and "
    "latent factor material done cleanly."),
   ("Hu, Koren & Volinsky &mdash; Collaborative Filtering for Implicit "
    "Feedback (free)",
    "http://yifanhu.net/PUB/cf.pdf",
    "<b>&sect;2's callout in the original</b> — the confidence "
    "weighting approach, and why the problem differs."),
   ("Dacrema, Cremonesi & Jannach &mdash; Are We Really Making Much "
    "Progress? (free)",
    "https://arxiv.org/abs/1907.06902",
    "<b>&sect;4's replication finding</b> — the paper that forced the "
    "field to tune its baselines. Read it before Module 13."),
   ("Chaney, Stewart & Engelhardt &mdash; How algorithmic confounding "
    "biases recommendation (free)",
    "https://arxiv.org/abs/1710.11214",
    "<b>&sect;3's feedback loop, simulated</b> — what happens to the "
    "data over time under a deployed recommender."),
 ],
 "exercises": [
   "<b>Build a content-based and a collaborative recommender</b> on the "
   "same data, and compare their cold-start behaviour.",
   "<b>Implement biased matrix factorisation</b> and measure how much "
   "the bias terms alone achieve.",
   "<b>Explain why the objective is not an SVD</b>, in your own "
   "words.",
   "<b>Convert explicit ratings to implicit feedback</b> and refit with "
   "a ranking objective.",
   "<b>Measure the recommended items' popularity distribution</b> "
   "against the catalogue's.",
   "<b>Compute catalogue coverage</b> for your system.",
   "<b>Simulate the feedback loop</b>: retrain on your own "
   "recommendations' outcomes for several rounds and watch coverage.",
   "<b>Compute RMSE and NDCG@10</b> for the same system and compare the "
   "rankings of two models.",
   "<b>Tune item-item nearest neighbours properly</b> and compare "
   "against your best model.",
   "<b>Report the comparison honestly</b>, whichever way it came out.",
 ],
 "selfcheck": [
   "Contrast the two approaches on five dimensions.",
   "Why are real systems hybrid?",
   "What is collaborative filtering's distinctive strength, and which "
   "other course shares the argument?",
   "Give the factorisation model and say why the bias terms matter.",
   "Why is it not an SVD?",
   "Why is a missing implicit entry ambiguous, and what are the two "
   "responses?",
   "Name four structural problems, and which is deepest.",
   "Why does offline evaluation favour the status quo?",
   "What did the replication work find?",
   "Give five things to measure, and the baseline to run first.",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Scale and Systems",
 "subtitle": "What distribution actually costs.",
 "question": "When is a cluster the right answer, and when is it not?",
 "outcomes": [
     "Explain the shuffle and why it dominates cost.",
     "Explain the MapReduce and dataflow models.",
     "Explain skew and how it is handled.",
     "Explain when a single machine is the right answer.",
     "Design a computation for the cost model that applies.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The cost model",
   "blurb": "Communication, not computation."},

  {"t": "callout", "title": "The shuffle is the expensive operation, and everything else is arranged around it",
   "kind": "The thing to understand first",
   "body": ["<b>A distributed computation is cheap when every machine "
            "works on its own partition and expensive when data has to "
            "move between machines</b> — and the move is the "
            "shuffle.",
            "<b>So the design question is how many shuffles a "
            "computation needs</b> — <b>map-only work is nearly "
            "free, and anything requiring a global grouping, a join, or a "
            "sort costs a full data movement.</b>",
            "<b>Which means the goal is to reduce data before "
            "shuffling</b>: combine locally, filter early, project away "
            "unused columns, and broadcast a small side "
            "input rather than joining.",
            "<b>And it is Module 01 §2's cost model "
            "again</b> — <b>passes became shuffles, and the "
            "arithmetic is still not the constraint.</b>"]},

  {"t": "code", "kicker": "Models", "title": "The programming models, and what each assumes",
   "lang": "text", "code": """
  MAPREDUCE
      map -> shuffle -> reduce, with the intermediate
      result written to disk. Simple, fault-tolerant
      by re-execution, and slow for iteration because
      every round pays the disk cost.

  DATAFLOW (Spark and successors)
      a DAG of transformations over partitioned
      collections, kept in memory where possible.
      Lineage-based recovery rather than replication.
      Much better for iterative work -- which is most
      of this course.

  VERTEX-CENTRIC (Pregel)
      Module 07's model: each vertex computes and
      sends messages, synchronised in supersteps.
      Fits graph algorithms and little else.

  AND THE SHARED ASSUMPTION
      the computation decomposes into independent
      work on partitions, with occasional
      communication. Anything genuinely sequential
      does not fit any of them.
""",
   "caption": "<b>The shared assumption is the limit</b> — a "
              "genuinely sequential algorithm does not become parallel by "
              "being expressed in one of these.",
   "note": "Naming the shared assumption prevents the expectation that "
           "any algorithm distributes."},

  {"t": "section", "label": "Part 2", "title": "Skew",
   "blurb": "Which is the practical failure mode."},

  {"t": "callout", "title": "One slow partition sets the runtime, and heavy-tailed data guarantees one",
   "kind": "Why skew dominates real performance problems",
   "body": ["<b>A stage finishes when its slowest task finishes</b> "
            "— so <b>a partition with ten times the data takes ten "
            "times as long, and the other machines idle.</b>",
            "<b>And the data is heavy-tailed</b> "
            "(Module 07 §1): <b>one key with a hundred "
            "million records and a million keys with ten each is the "
            "normal case</b>, not the pathological one.",
            "<b>So the fixes are specific:</b> <b>salt the hot key "
            "across several partitions and combine afterwards; broadcast "
            "the small side of a skewed join; or handle the heavy keys "
            "separately.</b>",
            "<b>And diagnose it by looking at the task duration "
            "distribution</b> — <b>a long tail there is skew, and an "
            "average task time tells you nothing</b> about it, which is "
            "why aggregate metrics mislead."]},

  {"t": "bullets", "kicker": "Diagnosis", "title": "What to look at when it is slow",
   "items": [
     "<b>The task duration distribution per stage</b>, not the "
     "mean — <b>which is where skew is visible and nowhere "
     "else.</b>",
     "",
     "<b>The shuffle read and write volumes</b>, which tell you "
     "whether you are moving more data than you need to.",
     "",
     "<b>The number of stages</b>, since each boundary is a "
     "shuffle — and a query plan with eight stages is doing "
     "something you may be able to avoid.",
     "",
     "<b>Spill to disk</b>, which means a partition did not fit in "
     "memory and the stage is now paying disk "
     "costs.",
     "",
     "<b>And the input format</b> — <b>a columnar format with "
     "predicate pushdown frequently beats any amount of tuning</b>, by "
     "reading less.",
   ],
   "footnote": "<b>Reading less is the first optimisation</b>, and it "
               "is usually a format and projection decision rather than a "
               "parallelism one."},

  {"t": "section", "label": "Part 3", "title": "When not to distribute",
   "blurb": "Which is more often than assumed."},

  {"t": "callout", "title": "A single large machine beats a small cluster for a surprising range of problems",
   "kind": "The comparison worth making before you build",
   "body": ["<b>A commodity server now has hundreds of gigabytes of "
            "memory and dozens of cores</b> — so <b>a dataset of "
            "tens of gigabytes fits in memory with room to work</b>, and "
            "an in-memory computation has no shuffle at "
            "all.",
            "<b>And the published comparisons are "
            "uncomfortable:</b> <b>several well-known graph and mining "
            "benchmarks run faster on one well-programmed machine than on "
            "a modest cluster</b>, because the coordination overhead "
            "exceeds the parallelism gain.",
            "<b>So the question to ask first is: does it fit?</b> "
            "<b>And if it nearly fits, can sampling, projection, or a "
            "sketch (Module 06) make it fit?</b>",
            "<b>Which is worth asking because distribution has real "
            "costs</b> — <b>operational complexity, debugging "
            "difficulty, and a much slower development loop</b> — "
            "that do not appear in a throughput number."]},

  {"t": "section", "label": "Part 4", "title": "Designing for it",
   "blurb": "The decisions that matter."},

  {"t": "bullets", "kicker": "Design", "title": "What to decide deliberately",
   "items": [
     "<b>The partitioning key</b>, because it determines which "
     "operations are local — <b>partition by the key you join "
     "and group on</b>, and the shuffles disappear.",
     "",
     "<b>The storage format and layout.</b> <b>Columnar, "
     "compressed, and partitioned on disk by the column you filter "
     "on</b> — which is a one-time decision with a permanent "
     "effect.",
     "",
     "<b>Where to approximate.</b> <b>A sketch or a sample that "
     "removes a shuffle is usually worth its error</b> "
     "(Module 06).",
     "",
     "<b>And whether the algorithm is iterative</b>, because that "
     "determines the engine — MapReduce is the wrong choice for "
     "anything with a loop.",
     "",
     "<b>Then measure before tuning</b>, because the bottleneck is "
     "rarely where you expect.",
   ],
   "footnote": "<b>The partitioning key is the highest-leverage "
               "decision</b> — it converts shuffles into local work, "
               "and it is made once and lived with."},

  {"t": "callout", "title": "And the honest framing",
   "kind": "Closing",
   "body": ["<b>Distribution buys you the ability to process data "
            "that does not fit, at the cost of communication, complexity, "
            "and a slower loop.</b>",
            "<b>So use it when the data genuinely does not fit</b> "
            "— and <b>check that claim rather than assuming it</b>, "
            "which is Part 3.",
            "<b>And when you do, design around the "
            "shuffle</b> — <b>the partitioning key and the storage "
            "layout together determine most of the performance</b>, "
            "before any tuning.",
            "<b>Which is a systems conclusion rather than an "
            "algorithmic one</b> — and is why "
            "CSCE 678 is a prerequisite for this "
            "module."]},
 ],
 "takeaways": [
   "The shuffle is the expensive operation, so the design question is how "
   "many shuffles a computation needs.",
   "A genuinely sequential algorithm does not become parallel by being "
   "expressed in a distributed model.",
   "A stage finishes when its slowest task finishes, and heavy-tailed data "
   "guarantees one slow partition.",
   "Skew is visible in the task duration distribution and nowhere else, so "
   "an average task time tells you nothing.",
   "A single large machine beats a small cluster for a surprising range of "
   "problems, because coordination overhead exceeds the parallelism gain.",
   "The partitioning key is the highest-leverage decision, because it "
   "converts shuffles into local work.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The cost model"),
  ("callout", "The shuffle is the expensive operation, and everything else "
              "is arranged around it",
   ["<b>A distributed computation is cheap when every machine works "
    "independently on its own partition, and expensive when data has to "
    "move between machines</b> — and that movement is the shuffle, "
    "which involves serialisation, network transfer, and frequently a "
    "disk write.",
    "<b>So the design question is how many shuffles a computation "
    "requires</b> — <b>map-only work is nearly free, and anything "
    "requiring a global grouping, a join on a non-partitioning key, or a "
    "total sort costs a full movement of the data.</b>",
    "<b>Which means the goal is to reduce the data before shuffling "
    "it:</b> combine locally before the shuffle, filter as early as "
    "possible, project away columns you do not use, and <b>broadcast a "
    "small side input rather than performing a join</b> — four "
    "techniques that between them handle most cases.",
    "<b>And it is Module 01 &sect;2's cost model arriving "
    "again</b> — <b>passes became shuffles, and the arithmetic is "
    "still not the constraint</b>. The through-line of this course is "
    "that the obvious cost model is the wrong one at every scale."]),
  ("code", """MAPREDUCE
    map -> shuffle -> reduce, with the intermediate
    result written to disk. Simple, fault-tolerant by
    re-execution, and slow for iterative work because
    every round pays the full disk cost again.

DATAFLOW (Spark and its successors)
    a DAG of transformations over partitioned
    collections, kept in memory where possible.
    Lineage-based recovery rather than replication.
    Much better for iterative work -- which is most
    of this course's algorithms.

VERTEX-CENTRIC (Pregel)
    Module 07's model: each vertex computes and sends
    messages, synchronised in supersteps. Fits graph
    algorithms well and very little else.

AND THE SHARED ASSUMPTION
    the computation decomposes into independent work
    on partitions, with occasional communication.
    Anything genuinely sequential does not fit any of
    them."""),
  ("p", "<b>The shared assumption is the limit</b>, and naming it is "
        "worth doing: <b>a genuinely sequential algorithm does not become "
        "parallel by being expressed in one of these models</b>. An "
        "algorithm whose step n+1 depends on the complete result of step n "
        "will run with one machine working and the rest idle, whatever "
        "framework it is written in — <b>which prevents the "
        "expectation that any algorithm distributes</b> and saves a good "
        "deal of disappointment."),

  ("h1", "2 &nbsp; Skew"),
  ("callout", "One slow partition sets the runtime, and heavy-tailed data "
              "guarantees one",
   ["<b>A stage finishes when its slowest task finishes</b> — so "
    "<b>a partition holding ten times the data takes roughly ten times as "
    "long, and every other machine sits idle waiting for it.</b> The "
    "parallelism is lost entirely to the one key.",
    "<b>And the data is heavy-tailed</b> (Module 07 "
    "&sect;1): <b>one key with a hundred million records alongside a "
    "million keys with ten each is the normal case</b> in real data, not "
    "a pathological one you can design around.",
    "<b>So the fixes are specific and worth knowing:</b> <b>salt the "
    "hot key across several partitions and combine the partial results "
    "afterwards; broadcast the small side of a skewed join rather than "
    "shuffling both; or detect the heavy keys and handle them in a "
    "separate code path.</b>",
    "<b>And diagnose it by looking at the task duration distribution "
    "within a stage</b> — <b>a long tail there is skew, and an "
    "average task time tells you nothing at all about it</b>, <b>which is "
    "why aggregate metrics mislead here</b> exactly as they do in "
    "CSCE 638 Module 12's disaggregation argument."]),
  ("ul", ["<b>The task duration distribution per stage</b>, not the "
          "mean — <b>which is where skew is visible and nowhere "
          "else</b>, and which every framework's interface will show you "
          "if you look.",
          "<b>The shuffle read and write volumes</b>, which tell you "
          "directly whether you are moving more data than the computation "
          "needs — and a shuffle larger than the input is a "
          "signal.",
          "<b>The number of stages</b>, since <b>each stage boundary "
          "is a shuffle</b> — and a query plan with eight stages is "
          "doing something that you may well be able to express in "
          "three.",
          "<b>Spill to disk</b>, which means a partition did not fit "
          "in the available memory and the stage is now paying disk costs "
          "it was supposed to avoid — usually fixed by more "
          "partitions rather than more memory.",
          "<b>And the input format</b> — <b>a columnar format "
          "with predicate pushdown frequently beats any amount of "
          "tuning</b>, by simply reading less data from disk. <b>Reading "
          "less is the first optimisation</b>, and it is <b>usually a "
          "format and projection decision rather than a parallelism "
          "one</b>."]),

  ("break",),
  ("h1", "3 &nbsp; When not to distribute"),
  ("callout", "A single large machine beats a small cluster for a surprising "
              "range of problems",
   ["<b>A commodity server now has hundreds of gigabytes of memory and "
    "dozens of cores</b> — so <b>a dataset of tens of gigabytes fits "
    "comfortably in memory with room to work</b>, and <b>an in-memory "
    "computation has no shuffle at all</b>, which removes &sect;1's entire "
    "cost.",
    "<b>And the published comparisons are uncomfortable:</b> "
    "<b>several well-known graph processing and mining benchmarks run "
    "faster on one well-programmed machine than on a modest "
    "cluster</b> — because the coordination and communication "
    "overhead exceeds the parallelism gain at that scale, sometimes by a "
    "large factor.",
    "<b>So the first question to ask is simply: does it fit?</b> "
    "<b>And if it nearly fits, can sampling, column projection, or a "
    "sketch (Module 06) make it fit?</b> — all three of which are "
    "cheaper than a cluster.",
    "<b>Which is worth asking because distribution has real costs that "
    "do not appear in a throughput number:</b> <b>operational "
    "complexity, much harder debugging, a far slower development loop, "
    "and a class of failure modes that do not exist on one machine</b> "
    "(CSCE 678)."]),

  ("h1", "4 &nbsp; Designing for it"),
  ("ul", ["<b>The partitioning key</b>, because <b>it determines "
          "which operations are local and which require a "
          "shuffle</b> — <b>partition by the key you join and group "
          "on, and the shuffles disappear</b> for those operations.",
          "<b>The storage format and layout.</b> <b>Columnar, "
          "compressed, and partitioned on disk by the column you filter "
          "on</b> — which is <b>a one-time decision with a permanent "
          "effect</b> on every query that follows, and is usually worth "
          "more than any runtime tuning.",
          "<b>Where to approximate.</b> <b>A sketch or a sample that "
          "removes a shuffle is usually worth its error</b> "
          "(Module 06) — and this is where this course's two "
          "halves meet: the approximation is chosen for a systems reason "
          "and its bound is still stated.",
          "<b>And whether the algorithm is iterative</b>, because "
          "<b>that determines the engine</b> — <b>MapReduce is the "
          "wrong choice for anything with a loop</b>, and most of this "
          "course's algorithms have loops.",
          "<b>Then measure before tuning</b>, because <b>the "
          "bottleneck is rarely where you expect it</b> — and the "
          "diagnostics in &sect;2 take minutes while a speculative "
          "optimisation takes a day. <b>The partitioning key is the "
          "highest-leverage decision</b>: it converts shuffles into local "
          "work, and it is made once and then lived with."]),
  ("callout", "And the honest framing",
   ["<b>Distribution buys you the ability to process data that does not "
    "fit on one machine, at the cost of communication, operational "
    "complexity, and a considerably slower development loop.</b> That is "
    "the entire trade.",
    "<b>So use it when the data genuinely does not fit</b> — and "
    "<b>check that claim rather than assuming it</b>, which is "
    "&sect;3 and takes an afternoon to establish either way.",
    "<b>And when you do distribute, design around the "
    "shuffle</b> — <b>the partitioning key and the storage layout "
    "together determine most of the performance</b>, before any "
    "configuration tuning is considered.",
    "<b>Which is a systems conclusion rather than an algorithmic "
    "one</b> — and <b>is why CSCE 678 is a prerequisite for this "
    "module</b>: the partitioning, the failure model, and the consistency "
    "questions are all its material, arriving here with a data mining "
    "workload on top."]),
 ],
 "resources": [
   ("Mining of Massive Datasets, chapter 2 (free)",
    "http://www.mmds.org/",
    "<b>&sect;1's models, with the communication cost analysis</b> "
    "— and the replication-rate framework for designing "
    "MapReduce algorithms."),
   ("Zaharia et al. &mdash; Resilient Distributed Datasets (free)",
    "https://www.usenix.org/conference/nsdi12/technical-sessions/presentation/zaharia",
    "<b>&sect;1's second model in the original</b> — and the lineage "
    "recovery argument, which is the interesting part."),
   ("McSherry, Isard & Murray &mdash; Scalability! But at what COST? "
    "(free)",
    "https://www.usenix.org/conference/hotos15/workshop-program/presentation/mcsherry",
    "<b>&sect;3's argument, measured</b> — the paper every student of "
    "this material should read before provisioning a cluster."),
   ("Spark's tuning and SQL performance documentation (free)",
    "https://spark.apache.org/docs/latest/tuning.html",
    "<b>&sect;2 and &sect;4 practically</b> — the skew handling and "
    "the partitioning guidance, from the implementation."),
 ],
 "exercises": [
   "<b>Count the shuffles</b> in a query plan you wrote.",
   "<b>Rewrite it to use one fewer</b>, and measure the "
   "difference.",
   "<b>Broadcast a small join side</b> and compare against the shuffled "
   "version.",
   "<b>Construct a skewed key distribution</b> and observe the task "
   "duration tail.",
   "<b>Salt the hot key</b> and measure the improvement.",
   "<b>Convert a dataset to a columnar format</b> and measure the read "
   "volume for a filtered query.",
   "<b>Run your whole computation on one large machine</b> and compare "
   "end to end against the cluster.",
   "<b>Include the development time</b> in that comparison.",
   "<b>Change the partitioning key</b> to match your join key and "
   "remeasure.",
   "<b>Profile before and after one tuning change</b> and report whether "
   "the bottleneck was where you expected.",
 ],
 "selfcheck": [
   "Why is the shuffle the expensive operation?",
   "Name four ways to reduce data before shuffling.",
   "Name three programming models and what each suits.",
   "What is their shared assumption, and what does it exclude?",
   "Why does one slow partition set the runtime?",
   "Why does heavy-tailed data guarantee skew, and what are the three "
   "fixes?",
   "Where is skew visible, and where is it not?",
   "Give five diagnostics, and the first optimisation.",
   "Why might one machine beat a cluster?",
   "Name four design decisions, and the highest-leverage one.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "The Pattern You Found",
 "subtitle": "The course's centre: multiplicity, and what survives it.",
 "question": "You searched hard and found something. Now what?",
 "outcomes": [
     "Count the hypotheses you actually tested.",
     "Apply the corrections and explain what each controls.",
     "Explain why significance and importance diverge at "
     "scale.",
     "Explain validation and pre-registration.",
     "Defend a found pattern, or abandon it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Counting",
   "blurb": "The number everybody understates."},

  {"t": "callout", "title": "Every analytic decision you made was a hypothesis test, whether you recorded it or not",
   "kind": "What counts, and it is more than you think",
   "body": ["<b>The explicit tests, obviously</b> — but also "
            "<b>every parameter setting you tried, every preprocessing "
            "choice you compared, every subgroup you looked at, and every "
            "analysis you abandoned because it showed "
            "nothing.</b>",
            "<b>Which is why the count cannot be reconstructed "
            "afterwards.</b> <b>You do not remember the analyses that "
            "failed</b>, and those are exactly the ones that inflate the "
            "multiplicity.",
            "<b>And the garden of forking paths makes it worse:</b> "
            "<b>even one analysis per dataset is a selection, if the "
            "analysis chosen depended on what the data "
            "looked like</b> — so there is an implicit count even "
            "with no explicit tests.",
            "<b>So the discipline is to log as you go</b> "
            "(Module 01 §4) — <b>and a study whose "
            "hypothesis count is unknown cannot be corrected, which "
            "means its significance values cannot be "
            "interpreted.</b>"]},

  {"t": "code", "kicker": "Counting", "title": "What to record, and what the count includes",
   "lang": "text", "code": """
  RECORD, AS YOU GO
      every test, with its hypothesis and its result
      every parameter value you tried
      every feature set and preprocessing variant
      every subgroup you examined separately
      and every analysis you stopped because it was
          not working

  THE LAST LINE IS THE IMPORTANT ONE. An abandoned
  analysis is a test whose negative result you
  discarded, which is exactly what inflates the
  family.

  AND IN AUTOMATED MINING the count is the candidate
  space the algorithm searched, not the number of
  results it returned:
      frequent itemsets   -> candidates considered
      correlation mining  -> pairs tested
      model selection     -> configurations evaluated
      feature selection   -> features screened

  WHICH IS USUALLY ENORMOUS, and is the honest input
  to Part 2's correction.
""",
   "caption": "<b>For automated mining, the count is the search space "
              "rather than the output size</b> — which is the "
              "distinction that makes the correction meaningful.",
   "note": "The search-space-not-output-size point is the one people "
           "get wrong."},

  {"t": "section", "label": "Part 2", "title": "Corrections",
   "blurb": "Two, controlling different things."},

  {"t": "table", "kicker": "Corrections", "title": "The corrections, and what each guarantees",
   "header": ["Method", "Controls", "Use when"],
   "widths": [2.7, 4.0, 5.1],
   "rows": [
     ["<b>Bonferroni</b>", "<b>Family-wise error: P(any false positive)</b>", "<b>A single false claim is costly; m is small</b>"],
     ["<b>Holm</b>", "<b>The same, uniformly more powerful</b>", "<b>Always preferable to Bonferroni</b>"],
     ["<b>Benjamini-Hochberg</b>", "<b>False discovery rate: E[fraction of claims that are false]</b>", "<b>You will follow up on many findings</b>"],
     ["<b>Permutation</b>", "<b>The null distribution, empirically</b>", "<b>The test statistic's distribution is unknown</b>"],
   ],
   "footnote": "<b>The FDR is usually the right target in "
               "mining</b> — you are generating leads, and tolerating "
               "a known fraction of false ones is more useful than "
               "guaranteeing none.",
   "note": "Choosing the error rate to control is the real decision."},

  {"t": "callout", "title": "And a permutation test is the one that always applies",
   "kind": "Why it is worth the computation",
   "body": ["<b>Shuffle the labels or the structure that your pattern "
            "depends on, recompute the statistic, and repeat</b> — "
            "<b>which gives you the null distribution of your statistic "
            "on your data.</b>",
            "<b>So it needs no parametric assumption</b>, and it "
            "handles test statistics whose distribution nobody has "
            "derived — which includes most mining statistics, "
            "modularity and cluster quality among them.",
            "<b>And it accounts for your data's structure "
            "automatically</b>: the permuted data keeps the marginals, "
            "the degree sequence, or whatever you held fixed.",
            "<b>Which makes it the right tool when the null "
            "comparisons of Modules 04 and 07 are needed</b> — "
            "<b>and the only thing it costs is computation</b>, which is "
            "the resource this course assumes you have."]},

  {"t": "section", "label": "Part 3", "title": "Significance and importance",
   "blurb": "Which diverge completely at scale."},

  {"t": "callout", "title": "With a million records, a meaningless effect is significant",
   "kind": "Why p-values stop being useful here",
   "body": ["<b>The standard error falls as 1/√n</b> — so "
            "<b>at n = 10⁶, a correlation of 0.003 has "
            "p &lt; 0.01</b> and explains nine millionths of the "
            "variance.",
            "<b>Which means significance testing answers a question "
            "nobody asked</b>: <b>'is the effect exactly zero' is almost "
            "never the question</b>, and at large n the answer is almost "
            "always no.",
            "<b>So report the effect size, with a confidence "
            "interval</b> — <b>and decide in advance what magnitude "
            "would matter</b> (Module 01 §4), which makes the "
            "result interpretable.",
            "<b>And the multiplicity problem does not go away</b> "
            "— <b>you still need the correction, applied to effect "
            "sizes rather than to p-values</b>, because the largest "
            "observed effect among many is biased upward."]},

  {"t": "section", "label": "Part 4", "title": "What actually settles it",
   "blurb": "Held-out data, and prediction."},

  {"t": "bullets", "kicker": "Validation", "title": "The hierarchy of evidence, weakest first",
   "items": [
     "<b>A pattern found and reported.</b> <b>Essentially no "
     "evidence</b>, whatever its p-value, because the search is "
     "unaccounted for.",
     "",
     "<b>A pattern found and corrected for the hypothesis "
     "count.</b> <b>Better, and dependent on an honest "
     "count.</b>",
     "",
     "<b>A pattern that survives held-out data you had not "
     "touched.</b> <b>Substantially stronger</b>, because the holdout "
     "was not part of the search.",
     "",
     "<b>A pattern predicted in advance and then "
     "confirmed.</b> <b>Stronger still</b>, because the hypothesis "
     "count was one.",
     "",
     "<b>And a pattern that predicts new data collected "
     "afterwards.</b> <b>The strongest available short of an "
     "experiment.</b>",
   ],
   "footnote": "<b>The jump from the second to the third level is the "
               "largest</b> — and it costs only the discipline of "
               "splitting the data before you start."},

  {"t": "callout", "title": "And what you would need to call it causal",
   "kind": "Closing",
   "body": ["<b>None of the above establishes causation.</b> <b>A "
            "pattern that replicates perfectly can still be a "
            "confound</b> — replication establishes that the "
            "association is real, not that it is causal.",
            "<b>What would:</b> <b>a randomised experiment, a natural "
            "experiment, an instrumental variable, or a credible "
            "identification strategy</b> — all of which require "
            "something beyond the observational data.",
            "<b>So the honest statement names what is "
            "missing</b> — <b>'we would need to randomise exposure to "
            "X, which we cannot do because…'</b> — rather than "
            "a generic disclaimer.",
            "<b>Which is Project 2's requirement</b>: <b>stating the "
            "experiment you would run is the deliverable</b>, because it "
            "demonstrates that you know what your evidence does not "
            "cover."]},
 ],
 "takeaways": [
   "Every analytic decision was a hypothesis test, including the analyses "
   "you abandoned — which is why the count cannot be reconstructed.",
   "In automated mining the count is the candidate space the algorithm "
   "searched, not the number of results it returned.",
   "The false discovery rate is usually the right target in mining, "
   "because you are generating leads and will follow up on many.",
   "A permutation test always applies, needs no parametric assumption, and "
   "costs only computation.",
   "At a million records a correlation of 0.003 is significant and "
   "explains nine millionths of the variance, so report effect sizes.",
   "The jump from a corrected finding to one that survives untouched "
   "held-out data is the largest in the hierarchy, and it costs only "
   "discipline.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Counting the hypotheses"),
  ("callout", "Every analytic decision you made was a hypothesis test, "
              "whether you recorded it or not",
   ["<b>The explicit statistical tests, obviously</b> — but also "
    "<b>every parameter setting you tried, every preprocessing choice you "
    "compared, every subgroup you looked at separately, every outlier rule "
    "you considered, and every analysis you abandoned because it showed "
    "nothing interesting.</b>",
    "<b>Which is exactly why the count cannot be reconstructed "
    "afterwards.</b> <b>You do not remember the analyses that "
    "failed</b> — they were uninteresting at the time and left no "
    "trace — <b>and those are precisely the ones that inflate the "
    "multiplicity.</b>",
    "<b>And the garden of forking paths makes it worse still:</b> "
    "<b>even a single analysis of a single dataset is a selection, if the "
    "analysis you chose depended on what the data looked like</b> — "
    "so <b>there is an implicit hypothesis count even when there was no "
    "explicit testing at all</b>, which is Gelman and Loken's "
    "argument.",
    "<b>So the discipline is to log as you go</b> (Module 01 "
    "&sect;4) — and <b>a study whose hypothesis count is unknown "
    "cannot be corrected, which means its significance values cannot be "
    "interpreted</b>. That is a strong statement and it follows directly "
    "from &sect;2's arithmetic."]),
  ("code", """RECORD, AS YOU GO
    every test, with its hypothesis and its result
    every parameter value you tried
    every feature set and preprocessing variant
    every subgroup you examined separately
    and every analysis you stopped because it was not
        working

THE LAST LINE IS THE IMPORTANT ONE. An abandoned
analysis is a test whose negative result you
discarded, which is exactly what inflates the family.

AND IN AUTOMATED MINING the count is the candidate
space the algorithm searched, not the number of
results it returned:
    frequent itemsets   -> candidates considered
    correlation mining  -> pairs tested
    model selection     -> configurations evaluated
    feature selection   -> features screened

WHICH IS USUALLY ENORMOUS, and is the honest input to
section 2's correction."""),
  ("p", "<b>For automated mining, the count is the search space rather "
        "than the output size</b> — <b>which is the distinction that "
        "makes the correction meaningful</b>, and <b>it is the one people "
        "get wrong</b>: correcting for the fifty rules your algorithm "
        "returned, rather than for the millions of candidates it "
        "evaluated, understates the problem by orders of magnitude. "
        "<b>Module 03 &sect;3's point is this one, in the frequent "
        "pattern setting.</b>"),

  ("h1", "2 &nbsp; Corrections"),
  ("table", ["Method", "What it controls", "Use it when"],
   [["<b>Bonferroni</b>",
     "<b>The family-wise error rate: the probability of <i>any</i> false "
     "positive.</b>",
     "<b>A single false claim would be costly, and m is small.</b> "
     "Very conservative for large m."],
    ["<b>Holm&ndash;Bonferroni</b>",
     "<b>The same family-wise rate, uniformly more powerful.</b>",
     "<b>Always preferable to plain Bonferroni</b> — it is strictly "
     "better at no cost in assumptions."],
    ["<b>Benjamini&ndash;Hochberg</b>",
     "<b>The false discovery rate: the expected fraction of your claims "
     "that are false.</b>",
     "<b>You will follow up on many findings</b> — see the note."],
    ["<b>Permutation testing</b>",
     "<b>Nothing by itself — it gives you the null distribution "
     "empirically.</b>",
     "<b>The test statistic's distribution is unknown</b>, which in this "
     "course is most of the time."]],
   [0.20, 0.36, 0.44]),
  ("p", "<b>The false discovery rate is usually the right target in data "
        "mining</b> — <b>you are generating leads for investigation, "
        "and tolerating a known fraction of false ones is considerably "
        "more useful than guaranteeing none at the cost of finding "
        "nothing</b>. <b>Choosing which error rate to control is the real "
        "decision</b>, and it follows from what you will do with the "
        "findings: a claim that goes into a paper and a lead that goes "
        "into a queue deserve different standards."),
  ("callout", "And a permutation test is the one that always applies",
   ["<b>Shuffle the labels, or whatever structure your pattern depends "
    "upon, recompute your statistic, and repeat several thousand "
    "times</b> — <b>which gives you the null distribution of your "
    "statistic on your own data</b>, directly.",
    "<b>So it needs no parametric assumption at all</b>, and it "
    "handles test statistics whose distribution nobody has derived "
    "— <b>which includes most of this course's statistics: "
    "modularity (Module 07 &sect;3), silhouette (Module 04 "
    "&sect;3), rule lift (Module 03), and anomaly scores.</b>",
    "<b>And it accounts for your data's structure "
    "automatically</b>, because <b>the permuted data retains whatever "
    "you held fixed</b> — the marginals, the degree sequence, the "
    "time ordering — which is exactly what makes the null a fair "
    "comparison rather than an unrealistic one.",
    "<b>Which makes it the right tool whenever the null comparisons of "
    "Modules 04 and 07 are needed</b> — and <b>the only thing it "
    "costs is computation</b>, which is <b>the resource this course "
    "assumes you have</b>. There is no good excuse for omitting it."]),

  ("break",),
  ("h1", "3 &nbsp; Significance and importance"),
  ("callout", "With a million records, a meaningless effect is significant",
   ["<b>The standard error falls as 1/&radic;n</b> — so <b>at "
    "n = 10<sup>6</sup>, a correlation of 0.003 has p &lt; 0.01</b> and "
    "<b>explains nine millionths of the variance</b>, which is to say "
    "nothing at all.",
    "<b>Which means significance testing at this scale answers a "
    "question nobody asked:</b> <b>'is the effect exactly zero' is "
    "almost never the question of interest</b>, and <b>at large n the "
    "answer is almost always no</b> for any pair of variables with any "
    "shared cause whatsoever.",
    "<b>So report the effect size, with a confidence "
    "interval</b> — <b>and decide in advance what magnitude would "
    "actually matter</b> (Module 01 &sect;4), which is what makes a "
    "result interpretable rather than merely publishable.",
    "<b>And the multiplicity problem does not go away when you switch "
    "to effect sizes</b> — <b>you still need the correction, applied "
    "to the effect sizes rather than to the p-values</b>, because <b>the "
    "largest observed effect among many candidates is biased upward</b> "
    "by the selection: the winner's curse applies to effect estimates as "
    "much as to significance."]),

  ("h1", "4 &nbsp; What actually settles it"),
  ("ul", ["<b>A pattern found and reported.</b> <b>Essentially no "
          "evidence</b>, whatever its p-value, <b>because the search that "
          "produced it is unaccounted for</b> (&sect;1).",
          "<b>A pattern found and then corrected for the hypothesis "
          "count.</b> <b>Better, and entirely dependent on the count "
          "being honest</b> — which is unverifiable by a reader, "
          "which is why the next level matters.",
          "<b>A pattern that survives on held-out data you had not "
          "touched.</b> <b>Substantially stronger</b>, because <b>the "
          "holdout was not part of the search</b> — so the "
          "multiplicity does not apply to it, and a reader can verify "
          "that you had one.",
          "<b>A pattern predicted in advance and then "
          "confirmed.</b> <b>Stronger still</b>, because <b>the "
          "hypothesis count was one</b> and the prediction is on the "
          "record (Module 01 &sect;4's second item).",
          "<b>And a pattern that predicts data collected "
          "afterwards.</b> <b>The strongest available short of an "
          "experiment</b> — since no amount of analytic flexibility "
          "could have influenced data that did not exist. <b>The jump "
          "from the second level to the third is the largest in this "
          "list</b>, and <b>it costs only the discipline of splitting the "
          "data before you start</b>, which is free."]),
  ("callout", "And what you would need to call it causal",
   ["<b>None of the above establishes causation.</b> <b>A pattern that "
    "replicates perfectly on new data can still be a confound</b> — "
    "<b>replication establishes that the association is real, not that it "
    "is causal</b>, and the distinction is routinely elided.",
    "<b>What would establish it:</b> <b>a randomised experiment, a "
    "natural experiment, an instrumental variable, a regression "
    "discontinuity, or another credible identification "
    "strategy</b> — <b>all of which require something beyond the "
    "observational data you have.</b>",
    "<b>So the honest statement names what is specifically "
    "missing</b> — <b>'we would need to randomise exposure to X, "
    "which we cannot do because it is determined by Y'</b> — "
    "<b>rather than offering a generic 'correlation is not causation' "
    "disclaimer</b>, which conveys nothing and is usually a formality.",
    "<b>Which is Project 2's requirement:</b> <b>stating the "
    "experiment you would run is the deliverable</b>, <b>because it "
    "demonstrates that you know precisely what your evidence does not "
    "cover</b> — and that demonstration is worth more than the "
    "pattern."]),
 ],
 "resources": [
   ("Benjamini & Hochberg &mdash; Controlling the False Discovery Rate "
    "(free)",
    "https://www.jstor.org/stable/2346101",
    "<b>&sect;2's third row in the original</b> — and the argument "
    "for why the FDR is the right target when you are screening."),
   ("Gelman & Loken &mdash; The Garden of Forking Paths (free)",
    "http://www.stat.columbia.edu/~gelman/research/unpublished/forking.pdf",
    "<b>&sect;1's hardest point</b> — that an implicit hypothesis "
    "count exists even without explicit multiple testing."),
   ("Ioannidis &mdash; Why Most Published Research Findings Are False "
    "(free)",
    "https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124",
    "<b>&sect;1 and &sect;4's motivation</b>, with the arithmetic "
    "— reread it now that you have the methods."),
   ("Sullivan & Feinn &mdash; Using Effect Size (free)",
    "https://pmc.ncbi.nlm.nih.gov/articles/PMC3444174/",
    "<b>&sect;3's recommendation, practically</b> — which effect size "
    "measures to use and how to report them."),
 ],
 "exercises": [
   "<b>Count the hypotheses</b> in an analysis you have already done, "
   "including the abandoned branches.",
   "<b>Start a hypothesis log for a new analysis</b> and compare its "
   "count against your estimate.",
   "<b>Compute the candidate space</b> your frequent itemset mining "
   "searched.",
   "<b>Apply Bonferroni, Holm, and Benjamini-Hochberg</b> to the same "
   "p-values and compare what survives.",
   "<b>Explain which error rate each controls</b> and which you would "
   "choose for your task.",
   "<b>Run a permutation test</b> on a modularity score from "
   "Module 07.",
   "<b>Run one on a silhouette score</b> from Module 04.",
   "<b>Generate 10⁶ records of noise</b> and find a significant "
   "correlation; report its effect size.",
   "<b>Validate one of your own findings on untouched held-out "
   "data</b> and report the result either way.",
   "<b>Write the specific experiment</b> you would need to call one "
   "finding causal.",
 ],
 "selfcheck": [
   "What counts as a hypothesis test, and which category is most "
   "often omitted?",
   "Why can the count not be reconstructed afterwards?",
   "State the garden of forking paths argument.",
   "In automated mining, what is the count?",
   "Name four corrections and what each controls.",
   "Which error rate suits mining, and why?",
   "Why does a permutation test always apply?",
   "Why does significance stop being informative at large n?",
   "Give the five levels of evidence and the largest jump.",
   "What would you need to claim causation, and how should you state "
   "it?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Privacy",
 "subtitle": "What mining does to the people in the data.",
 "question": "Can you analyse data about people without exposing them?",
 "outcomes": [
     "Explain why anonymisation fails.",
     "Explain k-anonymity and its limits.",
     "Explain differential privacy and what it guarantees.",
     "Explain the inference problems beyond identification.",
     "Assess a mining study's privacy properties.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why anonymisation fails",
   "blurb": "Not occasionally, but as a matter of structure."},

  {"t": "callout", "title": "Removing identifiers does not anonymise data, because the remaining attributes identify people",
   "kind": "The repeatedly demonstrated result",
   "body": ["<b>A handful of apparently innocuous attributes is "
            "usually unique.</b> <b>Date of birth, postcode, and sex "
            "identify a large majority of a population</b> — none of "
            "which is an identifier.",
            "<b>And the re-identifications are numerous and "
            "varied:</b> <b>a released medical dataset linked to a "
            "voter roll; movie ratings linked to public reviews; "
            "mobility traces identified from a few visited "
            "locations.</b>",
            "<b>The mechanism is always the same:</b> <b>link the "
            "'anonymous' records against an auxiliary dataset that shares "
            "some attributes</b> — and <b>you cannot know what "
            "auxiliary data exists or will exist.</b>",
            "<b>So 'anonymised' is not a property you can establish "
            "by inspecting your own dataset</b> — which is what makes "
            "this a structural failure rather than a series of "
            "mistakes."]},

  {"t": "callout", "title": "And hashing an identifier does not anonymise it",
   "kind": "Because the input space is small",
   "body": ["<b>A hashed email address, phone number, or national "
            "identifier is recoverable by enumeration</b> — the space "
            "is small enough to hash exhaustively, which is "
            "CSCE 711 §05 §4's third "
            "misuse.",
            "<b>And a hash is a <i>join key</i></b>: <b>two parties "
            "who hash the same identifier can link their "
            "datasets</b>, which is frequently the actual purpose and is "
            "rarely the stated one.",
            "<b>So 'we only store hashed identifiers' is a claim "
            "about storage format rather than about "
            "privacy</b> — and it is presented to users and "
            "regulators as though it were the latter.",
            "<b>A salted, slow construction changes the "
            "answer</b> — <b>but then it is no longer a usable join "
            "key</b>, which is usually why it is not used."]},

  {"t": "section", "label": "Part 2", "title": "k-anonymity",
   "blurb": "An intuitive idea, and what it misses."},

  {"t": "code", "kicker": "k-anonymity", "title": "The definition, and its successive patches",
   "lang": "text", "code": """
  k-ANONYMITY
      every record is indistinguishable from at least
      k-1 others on the quasi-identifiers. Achieved
      by generalising (age -> age range) and
      suppressing.

  THE HOMOGENEITY ATTACK
      if all k records in a group share the same
      sensitive value, you learn it without
      identifying anyone. k-anonymity says nothing
      about the sensitive attribute.

  l-DIVERSITY patches that: require l distinct
      sensitive values per group.

  THE SKEWNESS ATTACK
      l distinct values with one at 95% still leaks.

  t-CLOSENESS patches that: require each group's
      distribution to resemble the whole.

  AND THE PATTERN IS THE PROBLEM: each definition is
  broken by an attack the previous one did not model,
  because none of them quantifies over all possible
  auxiliary information.
""",
   "caption": "<b>The patch sequence is the lesson</b> — a "
              "definition that enumerates attacks is always one attack "
              "behind.",
   "note": "The enumerate-attacks-versus-quantify-over-them "
           "distinction motivates Part 3."},

  {"t": "section", "label": "Part 3", "title": "Differential privacy",
   "blurb": "A definition that quantifies over everything."},

  {"t": "eq", "kicker": "The definition", "title": "What it actually says",
   "eqs": [
     ("P[M(D) ∈ S] ≤ eᵋ · P[M(D′) ∈ S]",
      "For all datasets D, D′ differing in one record, and all "
      "output sets S."),
     ("so: your presence barely changes any output's probability",
      "Which bounds what any observer can learn about you "
      "specifically, whatever else they know."),
     ("ε is the privacy budget, and it composes",
      "Each query spends from it. k queries at ε each gives kε — "
      "which is the practical constraint."),
   ],
   "caption": "<b>The quantifier over <i>all</i> auxiliary information "
              "is what distinguishes this</b> — it is a property of "
              "the mechanism rather than of the data.",
   "note": "The quantifier is the whole point; state it clearly."},

  {"t": "callout", "title": "And the honest account of what it costs",
   "kind": "Both halves",
   "body": ["<b>What it gives:</b> <b>a guarantee that holds against "
            "any adversary with any auxiliary information</b>, that "
            "composes predictably, and that is a property of the "
            "mechanism rather than of the dataset.",
            "<b>What it costs:</b> <b>accuracy, which falls as "
            "ε falls</b> — and <b>the loss is worst "
            "exactly where the data is sparse</b>, which means small "
            "subgroups are harmed most.",
            "<b>And the budget is the operational "
            "difficulty.</b> <b>Every query spends from it, so an "
            "interactive analysis exhausts it</b> — which is why "
            "deployments release a fixed set of statistics rather than "
            "answering questions.",
            "<b>So the honest claim names ε and the "
            "composition</b> — <b>'ε-differentially private' "
            "without the value and without the query count is not a "
            "claim</b>, and a large ε guarantees very "
            "little."]},

  {"t": "section", "label": "Part 4", "title": "Beyond identification",
   "blurb": "The problems that remain when nobody is identified."},

  {"t": "bullets", "kicker": "Inference", "title": "The harms that privacy mechanisms do not address",
   "items": [
     "<b>Group inference.</b> <b>A model can predict a sensitive "
     "attribute about people not in the training data</b> — which "
     "no per-record guarantee prevents, because the harm is "
     "statistical.",
     "",
     "<b>Inference of what was never collected</b> — "
     "pregnancy, health status, sexuality, and political view are all "
     "predictable from behaviour, which makes 'we never asked' "
     "irrelevant.",
     "",
     "<b>Reconstruction from aggregates.</b> <b>Enough published "
     "statistics determine individual records</b>, which is a linear "
     "algebra result rather than a leak.",
     "",
     "<b>And repurposing</b> — <b>data collected for one "
     "purpose used for another</b>, which is a governance failure that "
     "no mechanism addresses.",
     "",
     "<b>So the question is not only 'can anyone be "
     "identified'</b> but <b>'what can be inferred, about whom, and "
     "with what consequence'</b>.",
   ],
   "footnote": "<b>The reconstruction result is the one that surprises "
               "people</b> — publishing many exact aggregates is "
               "mathematically equivalent to publishing the "
               "records."},

  {"t": "callout", "title": "What to do in a mining study",
   "kind": "Closing",
   "body": ["<b>Collect less.</b> <b>The data you do not hold cannot "
            "be breached, subpoenaed, or repurposed</b> — which is "
            "CSCE 701 Module 01's reduce-the-surface "
            "principle.",
            "<b>Aggregate early and keep the raw data "
            "separate</b>, with access logged "
            "(CSCE 701 Module 09).",
            "<b>Use differential privacy for anything "
            "published</b>, with ε stated — and <b>do not "
            "claim anonymisation you have not "
            "established</b> (Part 1).",
            "<b>And state what can be inferred from your "
            "output</b> — <b>which is Part 4's question "
            "and is the part of a privacy assessment that is actually "
            "hard.</b>"]},
 ],
 "takeaways": [
   "A handful of innocuous attributes is usually unique, so removing "
   "identifiers does not anonymise data.",
   "You cannot know what auxiliary data exists, which makes anonymisation "
   "a structural failure rather than a series of mistakes.",
   "'We only store hashed identifiers' is a claim about storage format, "
   "and a hash is a join key.",
   "The k-anonymity patch sequence is the lesson: a definition that "
   "enumerates attacks is always one attack behind.",
   "Differential privacy's quantifier over all auxiliary information is "
   "what distinguishes it, and it is a property of the mechanism.",
   "Publishing many exact aggregates is mathematically equivalent to "
   "publishing the records.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why anonymisation fails"),
  ("callout", "Removing identifiers does not anonymise data, because the "
              "remaining attributes identify people",
   ["<b>A handful of apparently innocuous attributes is usually "
    "unique.</b> <b>Date of birth, postcode, and sex together identify a "
    "large majority of a population</b> — and <b>none of the three is "
    "an identifier</b> in the sense that any removal policy would "
    "recognise.",
    "<b>And the re-identifications are numerous and varied rather than "
    "exotic:</b> <b>a released hospital discharge dataset linked against "
    "a public voter roll; anonymised movie ratings linked against public "
    "reviews elsewhere; mobility traces identified from four visited "
    "locations.</b> Each used only public auxiliary data.",
    "<b>The mechanism is always the same:</b> <b>link the 'anonymous' "
    "records against an auxiliary dataset that shares some "
    "attributes</b> — and <b>you cannot know what auxiliary data "
    "exists, or what will exist next year.</b>",
    "<b>So 'anonymised' is not a property you can establish by "
    "inspecting your own dataset</b>, which is <b>what makes this a "
    "structural failure rather than a series of mistakes by careless "
    "people</b> — and is the argument that motivated &sect;3's "
    "definition."]),
  ("callout", "And hashing an identifier does not anonymise it",
   ["<b>A hashed email address, phone number, or national identifier is "
    "recoverable by enumeration</b> — the input space is small enough "
    "to hash exhaustively on commodity hardware — which is "
    "<b>CSCE 711 Module 05 &sect;4's third misuse</b>, arriving here "
    "with a privacy consequence.",
    "<b>And a hash is a <i>join key</i></b>: <b>two parties who hash "
    "the same identifier with the same function can link their datasets "
    "without ever exchanging the identifier</b> — which is "
    "<b>frequently the actual purpose of hashing it, and is rarely the "
    "stated one.</b>",
    "<b>So 'we only store hashed identifiers' is a claim about storage "
    "format rather than about privacy</b> — and <b>it is presented "
    "to users and to regulators as though it were the latter</b>, which "
    "is CSCE 638 Module 12's bias-term conflation in a different "
    "register.",
    "<b>A salted, slow construction does change the answer</b> "
    "(CSCE 711 Module 09) — <b>but then it is no longer usable "
    "as a join key</b>, because the salt is per-record, <b>which is "
    "usually the reason it is not used.</b>"]),

  ("h1", "2 &nbsp; k-anonymity"),
  ("code", """k-ANONYMITY
    every record is indistinguishable from at least
    k-1 others on the quasi-identifiers. Achieved by
    generalising (exact age -> age range) and by
    suppressing records that cannot be grouped.

THE HOMOGENEITY ATTACK
    if all k records in a group share the same
    sensitive value, you learn that value without
    identifying anyone. k-anonymity says nothing at
    all about the sensitive attribute.

l-DIVERSITY patches that: require l distinct
    sensitive values within each group.

THE SKEWNESS ATTACK
    l distinct values with one of them at 95% still
    leaks a great deal.

t-CLOSENESS patches that: require each group's
    distribution of the sensitive attribute to
    resemble the distribution in the whole dataset.

AND THE PATTERN IS THE PROBLEM: each definition is
broken by an attack the previous one did not model,
because none of them quantifies over all possible
auxiliary information."""),
  ("p", "<b>The patch sequence is the lesson rather than the "
        "definitions</b> — <b>a privacy definition that enumerates "
        "attacks is always one attack behind</b>, because the next "
        "auxiliary dataset or the next correlation was not in the model. "
        "<b>The distinction between enumerating attacks and quantifying "
        "over them is what motivates &sect;3</b>, and it is a general "
        "lesson that applies well beyond privacy — it is the same "
        "argument as CSCE 711 Module 01 &sect;3's definitional "
        "approach to security."),

  ("break",),
  ("h1", "3 &nbsp; Differential privacy"),
  ("eq", "P[M(D) &isin; S] &le; e<sup>&epsilon;</sup> &middot; "
         "P[M(D&prime;) &isin; S]"),
  ("ul", ["<b>For <i>all</i> datasets D and D&prime; differing in a "
          "single record, and <i>all</i> sets of outputs S.</b> The two "
          "universal quantifiers are where the strength lives.",
          "<b>So your presence in the dataset barely changes the "
          "probability of any output</b> — <b>which bounds what any "
          "observer can learn about you specifically, whatever else they "
          "already know</b>, because the bound holds against every "
          "possible auxiliary dataset by construction.",
          "<b>&epsilon; is the privacy budget, and it composes:</b> "
          "<b>each query spends from it, and k queries at &epsilon; each "
          "gives a total of k&epsilon;</b> — <b>which is the "
          "practical constraint</b> and the thing that makes deployment "
          "hard (&sect;3's callout).",
          "<b>The quantifier over <i>all</i> auxiliary information is "
          "what distinguishes this from &sect;2's definitions</b> — "
          "<b>it is a property of the mechanism rather than of the "
          "data</b>, which means it can be established by analysing the "
          "algorithm and does not depend on what else exists in the "
          "world. <b>That shift is the whole contribution.</b>"]),
  ("callout", "And the honest account of what it costs",
   ["<b>What it gives:</b> <b>a guarantee that holds against any "
    "adversary with any auxiliary information whatsoever, that composes "
    "predictably across queries, and that is a property of the mechanism "
    "rather than of the dataset</b> — three things no earlier "
    "definition provided.",
    "<b>What it costs:</b> <b>accuracy, which degrades as &epsilon; "
    "falls</b> — and critically, <b>the loss is worst exactly where "
    "the data is sparse</b>, <b>which means small subgroups are harmed "
    "most</b> by the noise, and that is an equity consequence worth "
    "stating (CSCE 638 Module 12 &sect;2's disaggregation "
    "argument).",
    "<b>And the budget is the real operational difficulty.</b> "
    "<b>Every query spends from it, so an exploratory interactive "
    "analysis exhausts it quickly</b> — <b>which is why real "
    "deployments release a fixed, pre-decided set of statistics rather "
    "than answering arbitrary questions</b>, and why the technology fits "
    "a census better than a data science team.",
    "<b>So the honest claim names &epsilon; and the "
    "composition</b> — <b>'&epsilon;-differentially private' without "
    "the value of &epsilon; and without the number of queries is not a "
    "claim at all</b>, and <b>a large &epsilon; guarantees very "
    "little</b>, which is worth checking when the term appears in a "
    "product description."]),

  ("h1", "4 &nbsp; Beyond identification"),
  ("ul", ["<b>Group inference.</b> <b>A model trained on willing "
          "participants can predict a sensitive attribute about people "
          "who were never in the training data at all</b> — <b>which "
          "no per-record guarantee prevents</b>, because the harm is "
          "statistical and operates through population-level "
          "correlation.",
          "<b>Inference of what was never collected</b> — "
          "pregnancy, health status, sexuality, political view, and "
          "immigration status are all predictable to some degree from "
          "ordinary behavioural data, <b>which makes 'we never asked' "
          "irrelevant as a privacy claim.</b>",
          "<b>Reconstruction from aggregates.</b> <b>Enough published "
          "exact statistics determine the individual records</b> — "
          "<b>which is a linear algebra result rather than a leak or a "
          "bug</b>, and is <b>the one that surprises people</b>: "
          "publishing many exact aggregates is mathematically equivalent "
          "to publishing the microdata, which is why one national census "
          "adopted differential privacy.",
          "<b>And repurposing</b> — <b>data collected for one "
          "stated purpose used for another</b>, which is <b>a governance "
          "failure that no mathematical mechanism addresses</b> and is "
          "probably the most common actual harm.",
          "<b>So the question is not only 'can anyone be identified' "
          "but 'what can be inferred, about whom, and with what "
          "consequence'</b> — and the second question is the one a "
          "privacy assessment usually omits."]),
  ("callout", "What to do in a mining study",
   ["<b>Collect less.</b> <b>The data you do not hold cannot be "
    "breached, subpoenaed, repurposed, or re-identified</b> — which "
    "is <b>CSCE 701 Module 01's reduce-the-surface principle</b> "
    "arriving as a privacy measure, and is the only one that is "
    "unconditionally effective.",
    "<b>Aggregate early and keep the raw data separate</b>, with "
    "access logged and reviewed (CSCE 701 Module 09 &sect;1's "
    "secret-access events) — so that the surface requiring the "
    "strongest protection is as small as possible.",
    "<b>Use differential privacy for anything published</b>, with "
    "&epsilon; and the query count stated — and <b>do not claim "
    "anonymisation you have not established</b>, which &sect;1 argues you "
    "generally cannot.",
    "<b>And state what can be inferred from your output</b> — "
    "<b>which is &sect;4's question and is the genuinely hard part of a "
    "privacy assessment</b>, since it requires thinking about what a "
    "determined party could do with what you released rather than about "
    "what you intended. <b>Project 2 requires this when the data "
    "concerns people.</b>"]),
 ],
 "resources": [
   ("Dwork & Roth &mdash; The Algorithmic Foundations of Differential "
    "Privacy (free PDF)",
    "https://www.cis.upenn.edu/~aaroth/privacybook.html",
    "<b>&sect;3's first three chapters</b> — the definition, the "
    "basic mechanisms, and composition, which is all this course "
    "needs."),
   ("Narayanan & Shmatikov &mdash; Robust De-anonymization of Large "
    "Sparse Datasets (free)",
    "https://www.cs.cornell.edu/~shmat/shmat_oak08.pdf",
    "<b>&sect;1's mechanism, demonstrated</b> — and the clearest "
    "account of why auxiliary information is the problem."),
   ("Machanavajjhala et al., and Li et al. &mdash; l-diversity and "
    "t-closeness (free)",
    "https://dl.acm.org/doi/10.1145/1217299.1217302",
    "<b>&sect;2's patch sequence in the originals</b> — read them as "
    "a sequence, which is the lesson."),
   ("Dinur & Nissim &mdash; Revealing Information while Preserving "
    "Privacy (free)",
    "https://dl.acm.org/doi/10.1145/773153.773173",
    "<b>&sect;4's reconstruction result</b> — the theorem that "
    "aggregates determine the records."),
 ],
 "exercises": [
   "<b>Compute how many people in a public census share your birth "
   "date, postcode, and sex.</b>",
   "<b>Find two public datasets with overlapping attributes</b> and "
   "describe how they could be linked.",
   "<b>Enumerate a hashed low-entropy space</b> — hash 10,000 "
   "plausible phone numbers and match them.",
   "<b>Make a dataset 5-anonymous</b> by generalising, and measure the "
   "information you destroyed.",
   "<b>Construct a homogeneity attack</b> against your own "
   "k-anonymous release.",
   "<b>Implement the Laplace mechanism</b> for a count query and verify "
   "the noise scale.",
   "<b>Measure the accuracy loss</b> against ε, and separately for "
   "a small subgroup.",
   "<b>Compute the total budget</b> for a ten-query analysis.",
   "<b>Reconstruct individual records</b> from a set of exact "
   "aggregates you publish.",
   "<b>Write the privacy assessment</b> for Project 2, including what "
   "can be inferred from your output.",
 ],
 "selfcheck": [
   "Why does removing identifiers not anonymise data?",
   "What is the common mechanism in every re-identification?",
   "Why can anonymisation not be established from your own dataset?",
   "Why does hashing not anonymise, and what is a hash really?",
   "Define k-anonymity and give the attack against it.",
   "Give the patch sequence and say what the pattern shows.",
   "State differential privacy and say what the quantifiers buy.",
   "What does it cost, and who is harmed most?",
   "Why is the budget the operational difficulty?",
   "Name four harms that privacy mechanisms do not address.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Claiming a Pattern Honestly",
 "subtitle": "What a discovery establishes.",
 "question": "You found something. What can you say?",
 "outcomes": [
     "State what a found pattern establishes.",
     "Identify the standard overclaims.",
     "Write a defensible discovery claim.",
     "Place this course relative to CSCE 638 and CSCE 670.",
     "State a proportionate practice for real mining work.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What a finding establishes",
   "blurb": "Precisely, and it depends on the search."},

  {"t": "callout", "title": "A found pattern is a statement about your search procedure until it has been validated",
   "kind": "The honest reading",
   "body": ["<b>It establishes that this statistic, computed on this "
            "data, after this search, exceeded this threshold</b> "
            "— all four clauses, and the third is the one usually "
            "omitted.",
            "<b>And without the hypothesis "
            "count</b> (Module 11 §1), <b>the "
            "significance cannot be interpreted</b> — because the "
            "same p-value means different things after one test and after "
            "a million.",
            "<b>With validation on untouched held-out data, it becomes "
            "a statement about the data</b> — which is the "
            "qualitative change and is why "
            "Module 11 §4's third level matters so "
            "much.",
            "<b>And it is still not causal</b> "
            "(Module 11 §4) — <b>which requires something "
            "the observational data cannot supply</b>, and saying what is "
            "the honest form."]},

  {"t": "table", "kicker": "Overclaims", "title": "The standard overclaims, corrected",
   "header": ["Claim", "Correction"],
   "widths": [4.4, 6.6],
   "rows": [
     ["<b>'We discovered that X causes Y'</b>", "<b>You found an association. Name the experiment you would need</b>"],
     ["<b>'Significant at p &lt; 0.001'</b>", "<b>Out of how many hypotheses? (M11 §1)</b>"],
     ["<b>'The data has four clusters'</b>", "<b>Your algorithm returned four. What does a null comparison score? (M04 §4)</b>"],
     ["<b>'The network has strong community structure'</b>", "<b>Modularity against a degree-preserving null? (M07 §3)</b>"],
     ["<b>'Our detector is 99% accurate'</b>", "<b>Precision at a reviewable alert volume? (M08 §3)</b>"],
     ["<b>'The data is anonymised'</b>", "<b>Not establishable from your dataset alone (M12 §1)</b>"],
   ],
   "footnote": "<b>Every row substitutes an algorithm's output for a "
               "property of the world</b> — which is this course's "
               "single characteristic error and the thing Module 01 "
               "§1 set up.",
   "note": "The shared structure across the rows is what makes the "
           "table worth memorising."},

  {"t": "section", "label": "Part 2", "title": "Claims you can defend",
   "blurb": "The form, with the search disclosed."},

  {"t": "bullets", "kicker": "Honest", "title": "Defensible claims",
   "items": [
     "<b>'Among 4.2 million tested pairs, 118 exceeded our "
     "threshold after Benjamini-Hochberg at 5%; of those, 31 replicated "
     "on held-out data.'</b> <b>The search is "
     "disclosed.</b>",
     "",
     "<b>'The effect is a 2.1% difference, with a 95% interval of "
     "1.8 to 2.4% — which exceeds the 1% we specified in advance "
     "as material.'</b>",
     "",
     "<b>'Our minhash estimates had a mean absolute error of "
     "0.031 against exact Jaccard on 10,000 sampled pairs, consistent "
     "with the 0.035 bound at k=200.'</b>",
     "",
     "<b>'Modularity is 0.71; a degree-preserving null achieves "
     "0.42 with a standard deviation of 0.01.'</b> <b>Which makes the "
     "0.71 interpretable.</b>",
     "",
     "<b>And: 'we cannot distinguish this from a selection effect "
     "in how the data was collected.'</b>",
   ],
   "footnote": "<b>The last one is the limitation statement</b>, and "
               "it is Project 2's hardest-graded requirement — "
               "because it requires knowing what your design cannot "
               "settle."},

  {"t": "section", "label": "Part 3", "title": "The semester",
   "blurb": "Three courses, one shared concern."},

  {"t": "table", "kicker": "Semester 10", "title": "Where this course sits",
   "header": ["Course", "Covers", "Its proxy problem"],
   "widths": [2.3, 3.6, 5.6],
   "rows": [
     ["<b>CSCE 638</b>", "<b>Language</b>", "<b>A metric standing in for a quality judgement</b>"],
     ["<b>CSCE 676</b>", "<b>Structure at scale</b>", "<b>A score standing in for a pattern being real</b>"],
     ["<b>CSCE 670</b>", "<b>Information need</b>", "<b>A label standing in for relevance to a person</b>"],
   ],
   "footnote": "<b>All three are courses about a proxy</b>, and in all "
               "three the discipline is the same: say what the proxy is, "
               "and say what it does not capture.",
   "note": "The proxy framing unifies the semester."},

  {"t": "section", "label": "Part 4", "title": "A proportionate practice",
   "blurb": "What to actually do."},

  {"t": "bullets", "kicker": "Practice", "title": "The habits that matter, in order",
   "items": [
     "<b>1 · Split the data before you look</b>, and keep the "
     "holdout untouched (Module 01 §4) — <b>free, and the "
     "largest single improvement in Module 11 §4's "
     "hierarchy.</b>",
     "",
     "<b>2 · Keep the hypothesis log</b>, including "
     "abandoned branches — <b>cheap, and nothing downstream works "
     "without it.</b>",
     "",
     "<b>3 · Report effect sizes with intervals</b>, and "
     "decide in advance what magnitude matters "
     "(Module 11 §3).",
     "",
     "<b>4 · Run the null comparison</b> for any "
     "unsupervised finding — clusters, communities, anomalies "
     "(Modules 04, 07, 08).",
     "",
     "<b>5 · And verify your approximation bounds on your own "
     "data</b> (Module 01 §2), which is the other half "
     "of the course.",
   ],
   "footnote": "<b>The first two cost essentially nothing and change "
               "what your findings are worth</b> — which makes "
               "omitting them hard to defend."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can find structure in data too large to inspect, "
            "with a stated approximation bound</b> — similar items, "
            "frequent patterns, clusters, low-dimensional structure, "
            "stream summaries, communities, and anomalies.",
            "<b>You know what scale does to the cost model</b> "
            "— <b>passes, then shuffles, and never arithmetic</b> "
            "— and when a single machine is the right "
            "answer.",
            "<b>And you know that searching hard enough guarantees a "
            "finding</b> — so <b>you count the hypotheses, correct, "
            "validate on held-out data, and report the effect size rather "
            "than the p-value.</b>",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it means saying how hard "
            "you looked</b> — because <b>a pattern reported without "
            "its search is uninterpretable.</b>"]},
 ],
 "takeaways": [
   "A found pattern establishes a statement about your search procedure "
   "until it has been validated on untouched data.",
   "Without the hypothesis count, the significance cannot be interpreted, "
   "because the same p-value means different things after one test and "
   "after a million.",
   "Every standard overclaim substitutes an algorithm's output for a "
   "property of the world, which is this course's characteristic error.",
   "A defensible claim discloses the search: how many hypotheses, which "
   "correction, and how many replicated.",
   "All three Semester 10 courses are about a proxy, and the discipline is "
   "to say what the proxy does not capture.",
   "Splitting the data before you look and keeping the hypothesis log cost "
   "essentially nothing and change what your findings are worth.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What a finding establishes"),
  ("callout", "A found pattern is a statement about your search procedure "
              "until it has been validated",
   ["<b>It establishes that this statistic, computed on this data, "
    "after this search, exceeded this threshold</b> — <b>all four "
    "clauses, and the third is the one usually omitted</b> entirely.",
    "<b>And without the hypothesis count</b> (Module 11 "
    "&sect;1), <b>the significance simply cannot be "
    "interpreted</b> — because <b>the same p-value means entirely "
    "different things after one test and after a million</b>, and the "
    "reader has no way to tell which happened.",
    "<b>With validation on untouched held-out data, it becomes a "
    "statement about the data rather than about your "
    "procedure</b> — <b>which is the qualitative change</b>, and is "
    "why <b>Module 11 &sect;4's third level matters so much more than "
    "the second.</b>",
    "<b>And it is still not causal</b> (Module 11 &sect;4's "
    "closing callout) — <b>which requires something the "
    "observational data cannot supply</b>, and <b>saying specifically "
    "what is the honest form</b> rather than appending a generic "
    "disclaimer."]),
  ("table", ["The claim", "The correction"],
   [["<b>'We discovered that X causes Y.'</b>",
     "<b>You found an association.</b> <b>Name the experiment you would "
     "need to make it causal</b> (Module 11 &sect;4)."],
    ["<b>'Significant at p &lt; 0.001.'</b>",
     "<b>Out of how many hypotheses tested?</b> (Module 11 "
     "&sect;1.) Without that, the number is uninterpretable."],
    ["<b>'The data has four clusters.'</b>",
     "<b>Your algorithm returned four, because you asked for four.</b> "
     "<b>What does a null comparison score?</b> (Module 04 "
     "&sect;4.)"],
    ["<b>'The network has strong community structure.'</b>",
     "<b>What is the modularity against a degree-preserving null "
     "model?</b> (Module 07 &sect;3.)"],
    ["<b>'Our detector is 99% accurate.'</b>",
     "<b>What is the precision at a reviewable alert volume?</b> "
     "(Module 08 &sect;3.) Accuracy is meaningless at a low base "
     "rate."],
    ["<b>'The data is anonymised.'</b>",
     "<b>Not establishable by inspecting your own dataset</b> "
     "(Module 12 &sect;1)."]],
   [0.34, 0.66]),
  ("p", "<b>Every row substitutes an algorithm's output for a property "
        "of the world</b> — four clusters returned for four clusters "
        "existing, a modularity score for community structure, an accuracy "
        "figure for usefulness. <b>Which is this course's single "
        "characteristic error</b>, and <b>it is the thing Module 01 "
        "&sect;1 set up by separating the two problems.</b> <b>The shared "
        "structure across the rows is what makes the table worth "
        "memorising</b> rather than the individual corrections."),

  ("h1", "2 &nbsp; Claims you can defend"),
  ("ul", ["<b>'Among 4.2 million tested pairs, 118 exceeded our "
          "threshold after Benjamini&ndash;Hochberg correction at 5%; of "
          "those, 31 replicated on held-out data we had not "
          "examined.'</b> <b>The search is disclosed, the correction is "
          "named, and the replication rate is the headline.</b>",
          "<b>'The effect is a 2.1% difference, with a 95% confidence "
          "interval of 1.8% to 2.4% — which exceeds the 1% we "
          "specified in advance as the threshold for "
          "materiality.'</b> (Module 11 &sect;3, and "
          "Module 01 &sect;4's fourth item.)",
          "<b>'Our minhash estimates had a mean absolute error of "
          "0.031 against exact Jaccard on 10,000 sampled pairs, which is "
          "consistent with the 0.035 bound at k = 200.'</b> <b>The "
          "approximation verified rather than assumed</b> "
          "(Module 02 &sect;4).",
          "<b>'Modularity is 0.71; a degree-preserving null model "
          "achieves 0.42 with a standard deviation of 0.01.'</b> "
          "<b>Which is what makes the 0.71 interpretable</b>, and without "
          "the second clause it is not (Module 07 &sect;3).",
          "<b>And: 'we cannot distinguish this pattern from a "
          "selection effect in how the data was collected.'</b> <b>The "
          "last one is the limitation statement</b>, and <b>it is "
          "Project 2's hardest-graded requirement</b> — because "
          "<b>it requires knowing what your design cannot settle</b>, "
          "which is harder than knowing what it did."]),

  ("break",),
  ("h1", "3 &nbsp; The semester"),
  ("table", ["Course", "What it covers", "The proxy it has to live with"],
   [["<b>CSCE 638</b>", "<b>Language as input and output.</b>",
     "<b>A metric standing in for a quality judgement</b> — BLEU for "
     "a good translation, ROUGE for a good summary."],
    ["<b>CSCE 676 (this one)</b>",
     "<b>Finding structure in data at scale.</b>",
     "<b>A score standing in for a pattern being real</b> — "
     "modularity for community structure, silhouette for clusters, "
     "support for an association."],
    ["<b>CSCE 670</b>",
     "<b>Satisfying an information need.</b>",
     "<b>A relevance label standing in for relevance to an actual "
     "person</b> with an actual need."]],
   [0.20, 0.30, 0.50]),
  ("p", "<b>All three are courses about a proxy</b>, and <b>in all "
        "three the discipline is the same: say what the proxy is, and say "
        "what it does not capture</b>. <b>Which makes the "
        "choose-the-metric-from-the-use argument</b> (CSCE 633 "
        "Module 12) <b>the semester's organising idea</b>, arriving in "
        "three settings with three different proxies and one shared "
        "requirement. <b>The proxy framing unifies the semester</b>, and "
        "it is worth carrying forward."),

  ("h1", "4 &nbsp; A proportionate practice"),
  ("ul", ["<b>1 &middot; Split the data before you look at it</b>, and "
          "keep the holdout genuinely untouched (Module 01 "
          "&sect;4) — <b>free, and the largest single improvement "
          "available in Module 11 &sect;4's hierarchy of "
          "evidence.</b>",
          "<b>2 &middot; Keep the hypothesis log</b>, including the "
          "abandoned branches (Module 11 &sect;1) — <b>cheap, and "
          "nothing downstream works without it</b>, because no correction "
          "can be applied to an unknown count.",
          "<b>3 &middot; Report effect sizes with confidence "
          "intervals</b>, and decide in advance what magnitude would "
          "matter (Module 11 &sect;3) — which prevents the "
          "significant-and-useless finding that large n guarantees.",
          "<b>4 &middot; Run the null comparison for any unsupervised "
          "finding</b> — clusters (Module 04 &sect;3), "
          "communities (Module 07 &sect;3), anomalies "
          "(Module 08 &sect;4) — <b>which is the only way any of "
          "those scores can be read.</b>",
          "<b>5 &middot; And verify your approximation bounds on your "
          "own data</b> (Module 01 &sect;2, Module 02 &sect;4, "
          "Module 06 &sect;4), <b>which is the other half of the "
          "course</b> and the half that makes the algorithms "
          "trustworthy. <b>The first two cost essentially nothing and "
          "change what your findings are worth</b> — <b>which makes "
          "omitting them quite hard to defend.</b>"]),
  ("callout", "Where this course leaves you",
   ["<b>You can find structure in data too large to inspect, with a "
    "stated approximation bound</b> — similar items, frequent "
    "patterns, clusters, low-dimensional structure, stream summaries, "
    "communities, and anomalies — <b>and you verify the bound rather "
    "than citing it.</b>",
    "<b>You know what scale does to the cost model</b> — <b>passes "
    "first, then shuffles, and never arithmetic</b> — and <b>you "
    "check whether a single machine is the right answer</b> before "
    "provisioning a cluster (Module 10 &sect;3).",
    "<b>And you know that searching hard enough guarantees a "
    "finding</b> — so <b>you count the hypotheses, apply the "
    "correction, validate on held-out data, and report the effect size "
    "rather than the p-value</b>, which together are what distinguish a "
    "result from an artefact.",
    "<b>The closing rule is the program's, unchanged across "
    "twenty-nine courses:</b> <b>state what you measured, state what you "
    "assumed, and never claim more than you established.</b> <b>In this "
    "subject it means saying how hard you looked</b> — because <b>a "
    "pattern reported without its search is uninterpretable</b>, and "
    "&sect;1's table is what happens when that is left out."]),
 ],
 "resources": [
   ("Mining of Massive Datasets, chapter 1 (free)",
    "http://www.mmds.org/",
    "<b>&sect;1's position, from the authors</b> — reread the "
    "bonferroni's-principle section now that you have Module 11."),
   ("Ioannidis, and the reproducibility literature (free)",
    "https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124",
    "<b>&sect;1 and &sect;4's motivation</b> — the third reading, and "
    "it reads differently each time."),
   ("Dacrema et al. &mdash; Are We Really Making Much Progress? (free)",
    "https://arxiv.org/abs/1907.06902",
    "<b>&sect;2's baseline requirement, demonstrated</b> — and "
    "Module 09 &sect;4's finding, which generalises."),
   ("Leek & Peng &mdash; Statistics: P values are just the tip of the "
    "iceberg (free)",
    "https://www.nature.com/articles/520612a",
    "<b>&sect;4's ordering</b> — why the design decisions matter more "
    "than the statistical test."),
 ],
 "exercises": [
   "<b>Take a published data mining finding</b> and assess it against "
   "§1's table.",
   "<b>Determine whether its hypothesis count is reported.</b>",
   "<b>Rewrite one of your own findings</b> in §2's form, with the "
   "search disclosed.",
   "<b>Write the limitation statement</b> for it.",
   "<b>Identify the proxy</b> in each of the three Semester 10 "
   "courses.",
   "<b>Audit your own practice</b> against §4's five habits and "
   "report the gaps.",
   "<b>Check whether your holdout is genuinely untouched.</b>",
   "<b>Count the entries in your hypothesis log</b> and compare against "
   "what you would have guessed in Module 01.",
   "<b>Revisit Module 01's last exercise</b> and compare your "
   "predictions.",
   "<b>Project 2 is now due.</b> Submit the pattern with its effect "
   "size, the hypothesis count and correction, the held-out validation, "
   "the three ruled-out alternatives, the causal statement, and the "
   "privacy assessment.",
 ],
 "selfcheck": [
   "What four clauses does a found pattern's claim require?",
   "Why can significance not be interpreted without the hypothesis "
   "count?",
   "What changes when a pattern survives untouched held-out data?",
   "Give six overclaims and the correction to each.",
   "What do all six have in common?",
   "Give four defensible claim forms.",
   "What is Project 2's hardest requirement, and why?",
   "Name the proxy in each of the three Semester 10 courses.",
   "Give the five habits in order, and which two are nearly free.",
   "In this course, what does 'never claim more than you established' "
   "mean?",
 ],
},

]
