# -*- coding: utf-8 -*-
"""CSCE 633 Machine Learning — original course content."""

COURSE = {
    "code": "CSCE 633",
    "title": "Machine Learning",
    "tagline": "Estimation, generalisation, and evaluation — with "
               "honest measurement treated as the subject rather than the "
               "last chapter",
    "term": "Semester 6 (with CSCE 636 and CSCE 669)",
    "prereqs": "CSCE 629 Analysis of Algorithms; linear algebra and "
               "probability; UC MATH 600 and UC LINA 600 if either is rusty",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A model trained on data you did not choose, with a "
                   "held-out evaluation you designed before seeing the "
                   "result, an honest baseline comparison, and a written "
                   "account of what it will do when deployed",
    "description": [
        "Machine learning is the first subject in this program where "
        "<b>the thing you are optimising is not the thing you want</b>. "
        "Every other course had a specification: the hull must be convex, "
        "the compiler must preserve meaning, the renderer must solve the "
        "rendering equation. Here you have a sample, a loss function that "
        "approximates a goal, and a hope that performance on data you have "
        "predicts performance on data you have not.",
        "<b>That hope is the entire subject.</b> Module 03 states it "
        "precisely as the bias–variance decomposition and Module 04 "
        "as the generalisation gap, and essentially every technique in the "
        "course — regularisation, cross-validation, ensembling, early "
        "stopping — is a way of managing the distance between "
        "training performance and the performance you actually care about.",
        "The second theme is that <b>evaluation is harder than "
        "training</b>, and is where almost all real failures live. A model "
        "that reports 99% accuracy on a dataset where 99% of examples are "
        "negative has learned nothing. A model evaluated on data that "
        "leaked from its own training set reports a number that means "
        "nothing. <b>Module 05 is about metrics and Module 12 is about the "
        "ways an evaluation lies</b>, and both are placed early enough to "
        "be used rather than late enough to be skipped.",
        "The emphasis throughout is on <b>what the model will do when it "
        "meets data drawn from a different distribution than it was "
        "trained on</b>, because it will. <b>Module 13 argues that the "
        "deployment questions — drift, feedback loops, and who is "
        "harmed when it is wrong — are engineering questions with "
        "technical answers</b>, not an ethics appendix.",
    ],
    "outcomes": [
        "State the supervised learning problem precisely and say what is "
        "assumed.",
        "Derive and implement linear and logistic regression from the "
        "loss.",
        "Decompose error into bias, variance, and noise, and act on it.",
        "Apply regularisation and explain what it buys.",
        "Choose and compute evaluation metrics appropriate to the "
        "problem.",
        "Build and tune tree ensembles, and say why they win on tabular "
        "data.",
        "Apply kernels and explain the representer theorem's "
        "consequence.",
        "Apply unsupervised methods and state what their output means.",
        "Diagnose leakage, imbalance, and distribution shift.",
        "Report a result honestly, including the baseline it beat.",
    ],
    "materials": [
        ("Stanford CS229 — Machine Learning (free lectures and notes)",
         "https://cs229.stanford.edu/",
         "<b>The primary source.</b> Andrew Ng's lecture notes are the "
         "best free derivation-level treatment of Modules 02 through 08, "
         "and the problem sets are worth doing."),
        ("James, Witten, Hastie & Tibshirani — An Introduction to "
         "Statistical Learning (free PDF)",
         "https://www.statlearning.com/",
         "<b>Free, and the right level for this course.</b> Strong on "
         "the bias–variance material of Module 03 and on resampling. "
         "The R and Python editions are both free."),
        ("Hastie, Tibshirani & Friedman — The Elements of "
         "Statistical Learning (free PDF)",
         "https://hastie.su.domains/ElemStatLearn/",
         "The deeper companion to the above, also free. Use it for the "
         "derivations the first book states without proof."),
        ("scikit-learn — the user guide (free)",
         "https://scikit-learn.org/stable/user_guide.html",
         "<b>Unusually good documentation</b> — the model selection "
         "and metrics chapters are genuinely instructional, not merely "
         "reference material."),
        ("Google — Rules of Machine Learning (free)",
         "https://developers.google.com/machine-learning/guides/rules-of-ml",
         "<b>The Module 13 material.</b> Forty-three rules from people "
         "who have deployed a great deal of this, and the early ones are "
         "about not using machine learning yet."),
        ("Kaufman, Rosset & Perlich — Leakage in Data Mining (free)",
         "https://dl.acm.org/doi/10.1145/2020408.2020496",
         "<b>The Module 12 reference.</b> Worked examples of evaluations "
         "that were wrong and the competitions they won."),
    ],
    "tooling": [
        "<b>Python with NumPy, scikit-learn, and pandas.</b> <b>Implement "
        "the first few algorithms from scratch in NumPy</b>, then use the "
        "library — the same pattern as CSCE 735's advice about "
        "libraries.",
        "<b>A notebook environment, used with discipline.</b> Notebooks "
        "make it very easy to evaluate on data you have already looked at, "
        "which is Module 12's central hazard.",
        "<b>A fixed random seed, and a results log.</b> <b>Record every "
        "experiment you run, including the ones that failed</b> — "
        "otherwise you will rediscover the same dead ends and will "
        "overstate your successes.",
        "<b>A dataset you did not choose.</b> The project requires one; "
        "picking a clean benchmark you already know the answer on defeats "
        "the purpose.",
        "<b>A plotting setup</b>, because learning curves, calibration "
        "plots, and confusion matrices are how you diagnose a model and "
        "none of them is a single number.",
        "<b>Version control for data as well as code.</b> A result you "
        "cannot reproduce because the preprocessing changed is not a "
        "result.",
    ],
    "projects": [
        {"title": "A model, and an honest evaluation of it", "after": 7,
         "brief": "Take a dataset you did not choose and build a "
                  "supervised model for it — with the evaluation "
                  "protocol written down <i>before</i> you see any "
                  "results.",
         "reqs": [
             "<b>A written evaluation protocol, dated, committed before "
             "the first model is trained.</b> Which split, which metric, "
             "which baseline.",
             "<b>A trivial baseline</b> — majority class, or the "
             "mean, or one feature — that every later model must "
             "beat.",
             "A proper train / validation / test split, with the test set "
             "used <b>exactly once</b>.",
             "<b>Learning curves</b> showing training and validation error "
             "against training set size and against model complexity.",
             "A bias–variance diagnosis stating which one limits you "
             "and what you did about it.",
             "<b>A leakage audit:</b> for each feature, could it have been "
             "known at prediction time?",
         ],
         "done": [
             "<b>The test set was evaluated once and the number is "
             "reported, whatever it was.</b> Re-running it after tuning "
             "invalidates it, and saying so is part of the exercise.",
             "<b>Learning curves with the diagnosis written on them</b> "
             "— high bias, high variance, or neither.",
             "<b>The trivial baseline's score, next to yours.</b> If the "
             "gap is small, that is the finding.",
             "<b>A list of what you tried that did not work.</b> This is "
             "graded, and omitting it is the normal dishonesty of the "
             "field.",
         ]},
        {"title": "Harder data, and what happens next", "after": 12,
         "brief": "Take the model further on data that is imbalanced, "
                  "shifted, or small — and say what it will do in "
                  "deployment.",
         "reqs": [
             "<b>A dataset with real class imbalance, missing data, or a "
             "temporal structure</b>, handled explicitly rather than "
             "ignored.",
             "An ensemble, with the individual models' scores reported "
             "alongside it.",
             "<b>Calibration measured and reported</b>, not just "
             "discrimination — a reliability diagram.",
             "<b>A distribution-shift experiment:</b> train on one slice, "
             "test on another, and report the degradation.",
             "An error analysis: a sample of the mistakes, categorised.",
             "Feature importance or another account of what the model is "
             "using.",
         ],
         "done": [
             "<b>A reliability diagram, with a statement of whether the "
             "probabilities mean anything.</b>",
             "<b>The measured drop under distribution shift</b>, with a "
             "stated expectation of how fast it would degrade in "
             "production.",
             "<b>An error analysis naming the categories of mistake</b> "
             "and which are acceptable.",
             "<b>A deployment statement:</b> who is affected when it is "
             "wrong, what the feedback loop is, and what would make you "
             "retrain it.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "What Learning From Data Means",
 "subtitle": "Optimising a proxy for a goal, and hoping it transfers.",
 "question": "What exactly is being assumed when a model is trained?",
 "outcomes": [
     "State the supervised learning problem formally.",
     "Explain the i.i.d. assumption and where it fails.",
     "Distinguish the loss you optimise from the goal you have.",
     "Explain why a held-out set is the only honest measurement.",
     "Decide whether a problem needs machine learning at all.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The setup",
   "blurb": "What is given, and what is assumed."},

  {"t": "eq", "kicker": "The problem", "title": "Supervised learning, stated",
   "eqs": [
     ("Given (x₁,y₁) … (xₙ,yₙ) drawn i.i.d. from unknown D",
      "A sample. The distribution D is never observed, only sampled."),
     ("Find f minimising  E₍ₓ,ᵧ₎~D [ L(f(x), y) ]",
      "The EXPECTED loss over the true distribution. This is what you "
      "want."),
     ("You can only compute  (1/n) Σ L(f(xᵢ), yᵢ)",
      "The loss on the sample you have. This is what you optimise. The "
      "gap between them is the whole subject."),
   ],
   "caption": "<b>Three lines, and the third one is the problem.</b> You "
              "minimise one quantity and are judged on another.",
   "note": "Everything in the course is managing the distance between "
           "lines 2 and 3."},

  {"t": "callout", "title": "Three substitutions, each of which can fail",
   "kind": "What is actually being assumed",
   "body": ["<b>The sample stands in for the distribution.</b> Fails if "
            "the data was collected in a way that does not match "
            "deployment — which is usual.",
            "<b>The loss function stands in for the goal.</b> Squared "
            "error is not 'good predictions'; cross-entropy is not "
            "'useful'. <b>You optimise what you can write down.</b>",
            "<b>Past data stands in for future data.</b> Fails whenever "
            "the world changes, and especially when the model's own "
            "deployment changes it (Module 13).",
            "<b>Every machine learning failure is one of these three</b>, "
            "and naming which one is most of a diagnosis."]},

  {"t": "section", "label": "Part 2", "title": "The i.i.d. assumption",
   "blurb": "The one that is almost never true."},

  {"t": "table", "kicker": "Violations", "title": "How independence and identical distribution fail",
   "header": ["Violation", "Example", "Consequence"],
   "widths": [2.8, 4.3, 5.0],
   "rows": [
     ["<b>Temporal correlation</b>", "<b>Stock prices; sensor streams</b>", "<b>Random splits leak the future</b>"],
     ["<b>Grouped data</b>", "Several samples per patient", "<b>Split by group or you test on training</b>"],
     ["<b>Selection bias</b>", "<b>Only approved loans have outcomes</b>", "<b>The model never sees rejections</b>"],
     ["Covariate shift", "Trained on one hospital's scans", "Features move; labels do not"],
     ["<b>Label shift</b>", "Disease prevalence changes", "<b>Base rates move under you</b>"],
     ["<b>Feedback</b>", "<b>The model changes the data</b>", "<b>Module 13. The worst case</b>"],
   ],
   "footnote": "<b>The random split is the default and is wrong for the "
               "first three rows</b>, which covers a large share of real "
               "problems.",
   "note": "The grouped-data row causes a lot of silently inflated "
           "results."},

  {"t": "callout", "title": "The random split is the wrong default more often than not",
   "kind": "The most common evaluation error",
   "body": ["<b>A random split assumes every row is independent.</b> When "
            "rows share a patient, a user, a session, or a time period, "
            "they are not.",
            "<b>So the same entity appears in both training and test</b>, "
            "and the model is rewarded for memorising it rather than "
            "generalising.",
            "<b>Split by the unit you will generalise over.</b> New "
            "patients? Split by patient. Future data? Split by time, "
            "always forward.",
            "<b>This single error inflates reported performance more than "
            "any other</b>, it is easy to make and hard to notice, and "
            "<b>published results have been retracted over it.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Loss and goal",
   "blurb": "What you can write down versus what you want."},

  {"t": "callout", "title": "You optimise the loss; you are judged on the goal",
   "kind": "The gap that stays open",
   "body": ["<b>'Predict well' is not a mathematical object.</b> Squared "
            "error, cross-entropy, and hinge loss are, so one of them is "
            "chosen as a stand-in.",
            "<b>And the choice has consequences.</b> Squared error is "
            "dominated by large errors, so it chases outliers; absolute "
            "error does not and is harder to optimise.",
            "<b>Asymmetric costs are the common case and the symmetric "
            "loss is the default.</b> A missed fraud and a false alarm "
            "cost different amounts, and the loss should say so.",
            "<b>So write down the cost of each kind of error before "
            "choosing a loss</b> — and if you cannot, that is worth "
            "discovering early rather than after deployment."]},

  {"t": "section", "label": "Part 4", "title": "Whether to use it",
   "blurb": "The first question, rarely asked."},

  {"t": "bullets", "kicker": "Before modelling", "title": "Reasons not to use machine learning",
   "items": [
     "<b>A rule works.</b> If three <code>if</code> statements get 95%, "
     "ship them — they are debuggable and explainable.",
     "",
     "<b>You have no labels</b>, and getting them costs more than the "
     "problem is worth.",
     "",
     "<b>The data is small.</b> Under a few hundred examples, a model "
     "mostly fits noise.",
     "",
     "<b>You cannot tolerate being wrong</b> in a way you cannot "
     "predict.",
     "",
     "<b>Or the cost of being wrong is borne by someone who did not "
     "choose this</b> — which is a reason for care, not necessarily for "
     "refusal.",
   ],
   "footnote": "<b>Google's first rule is 'don't be afraid to launch a "
               "product without machine learning'</b>, and the next few "
               "are about heuristics."},

  {"t": "callout", "title": "The baseline is not optional",
   "kind": "The discipline this course enforces",
   "body": ["<b>Always compute a trivial baseline first:</b> predict the "
            "majority class, or the mean, or last week's value.",
            "<b>A surprising number of reported models do not beat "
            "one</b> — and the paper or dashboard rarely says so, because "
            "nobody computed it.",
            "<b>A baseline also calibrates the problem.</b> If the "
            "majority class is 94%, then 95% accuracy is one percentage "
            "point of actual work.",
            "<b>So the baseline comes before the model, is reported "
            "beside it, and is the number any claim is relative to.</b> "
            "<b>Every course in this program has had this rule in some "
            "form</b> — CSCE 735's optimised serial baseline is the same "
            "idea."]},
 ],
 "takeaways": [
   "You minimise loss on a sample and are judged on expected loss over a "
   "distribution you never see — the gap between them is the whole "
   "subject.",
   "Three substitutions are being assumed: sample for distribution, loss "
   "for goal, past for future. Every failure is one of them.",
   "The random split assumes every row is independent, which is false for "
   "temporal, grouped, and selected data.",
   "Splitting by the wrong unit inflates reported performance more than any "
   "other error, and has caused retractions.",
   "The loss is chosen because it can be written down, not because it is "
   "the goal — and symmetric losses are the default while asymmetric "
   "costs are the norm.",
   "Compute a trivial baseline first, report it beside your result, and "
   "make every claim relative to it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The setup"),
  ("eq", "f* = argmin<sub>f</sub> &nbsp; "
         "E<sub>(x,y)~D</sub> [ L(f(x), y) ] &nbsp;&nbsp;&nbsp; "
         "but you compute &nbsp; (1/n) &Sigma;<sub>i</sub> "
         "L(f(x<sub>i</sub>), y<sub>i</sub>)"),
  ("p", "You are given a sample of n pairs drawn independently from an "
        "unknown distribution D. <b>You want the function minimising "
        "expected loss over D</b> — the risk. <b>You can only compute "
        "the average loss over the sample</b> — the empirical risk. "
        "<b>Minimising the second in the hope of minimising the first is "
        "the entire activity</b>, and the distance between them is what "
        "Modules 03 and 04 are about. It is worth sitting with how strange "
        "this is compared with everything else in this program: there is no "
        "specification to satisfy and no proof of correctness available, "
        "only an estimate of how well you will do on data you have not "
        "seen."),
  ("callout", "Three substitutions, each of which can fail",
   ["<b>The sample stands in for the distribution.</b> This fails whenever "
    "the data was collected in a way that does not match how the model will "
    "be used — which is the usual case, because data is collected by "
    "whatever process was convenient and models are deployed wherever they "
    "are useful.",
    "<b>The loss function stands in for the goal.</b> Squared error is not "
    "'good predictions'; cross-entropy is not 'useful'; accuracy is not "
    "'helpful to the user'. <b>You optimise what you can write down</b>, "
    "and the gap between that and what you wanted is permanent "
    "(&sect;3).",
    "<b>Past data stands in for future data.</b> This fails whenever the "
    "world changes — and <b>especially when the model's own "
    "deployment changes it</b>, which is Module 13's feedback loop and the "
    "most insidious of the three.",
    "<b>Every machine learning failure is one of these three</b>, and "
    "<b>naming which one is most of a diagnosis</b>. A model that worked in "
    "development and fails in production has almost always violated the "
    "first or the third, and knowing which determines whether the fix is "
    "better data or more frequent retraining."]),

  ("h1", "2 &nbsp; The i.i.d. assumption"),
  ("table", ["Violation", "Example", "Consequence"],
   [["<b>Temporal correlation</b>",
     "<b>Stock prices, sensor streams, user activity logs</b> — "
     "adjacent rows are nearly identical.",
     "<b>A random split puts the future in the training set</b>, so the "
     "model is evaluated on data it effectively already saw. Split "
     "forward in time, always."],
    ["<b>Grouped data</b>",
     "Several scans per patient; several sessions per user; several frames "
     "per video.",
     "<b>Split by group, or the same entity appears in train and test</b> "
     "and the score measures memorisation."],
    ["<b>Selection bias</b>",
     "<b>Only approved loans have repayment outcomes.</b> Only treated "
     "patients have treatment results.",
     "<b>The model never sees the rejected cases</b>, so it cannot learn "
     "about them — and it will be applied to them."],
    ["<b>Covariate shift</b>",
     "Trained on one hospital's scanner, deployed on another's.",
     "P(x) changes while P(y|x) does not. Sometimes correctable by "
     "reweighting."],
    ["<b>Label shift</b>", "Disease prevalence changes between seasons.",
     "<b>The base rates move</b>, so a calibrated model becomes "
     "miscalibrated even though nothing about the features changed."],
    ["<b>Feedback</b>",
     "<b>The model's predictions change the data it is later trained "
     "on.</b> A recommender shapes what gets watched.",
     "<b>Module 13, and the hardest case</b> — the distribution is no "
     "longer exogenous."]],
   [0.18, 0.38, 0.44]),
  ("callout", "The random split is the wrong default more often than not",
   ["<b>A random split assumes every row is independent of every other.</b> "
    "When rows share a patient, a user, a session, a device, or a time "
    "window, they are not — and this is extremely common.",
    "<b>So the same entity appears in both the training and the test "
    "set</b>, and the model is rewarded for recognising that entity rather "
    "than for generalising to new ones. The reported score measures "
    "something real; it just is not the thing you will deploy.",
    "<b>Split by the unit you intend to generalise over.</b> If the model "
    "will see new patients, split by patient. If it will see the future, "
    "split by time and never shuffle. <b>Ask 'what will be new at "
    "prediction time?' and make that the split key.</b>",
    "<b>This single error inflates reported performance more than any "
    "other in the field.</b> It is easy to make (the library default is a "
    "random split), hard to notice (the numbers look plausible, just too "
    "good), and <b>published results have been retracted over it</b> "
    "— including in medical imaging, where the consequences were "
    "real."]),

  ("break",),
  ("h1", "3 &nbsp; The loss and the goal"),
  ("callout", "You optimise the loss; you are judged on the goal",
   ["<b>'Predict well' is not a mathematical object and cannot be "
    "optimised.</b> Squared error, cross-entropy, hinge loss, and absolute "
    "error are mathematical objects, so one of them is chosen to stand in "
    "for the goal.",
    "<b>And the choice has real consequences.</b> Squared error grows "
    "quadratically, so it is dominated by the largest errors and the fitted "
    "model chases outliers; absolute error does not, and is less convenient "
    "to optimise. <b>The usual choice is made for differentiability and "
    "then rationalised.</b>",
    "<b>Asymmetric costs are the common case and the symmetric loss is the "
    "default.</b> A missed fraudulent transaction and a falsely declined "
    "legitimate one cost very different amounts to very different people, "
    "and a symmetric loss asserts they are equal. <b>So does accuracy</b>, "
    "which is why Module 05 spends its time on other metrics.",
    "<b>So write down the cost of each kind of error before choosing a "
    "loss.</b> If the business cannot state those costs, that is worth "
    "discovering in week one rather than after deployment — and the "
    "conversation frequently reveals that the stated goal was not the real "
    "one."]),

  ("h1", "4 &nbsp; Whether to use machine learning at all"),
  ("ul", ["<b>A rule works.</b> If three <code>if</code> statements reach "
          "95% of the achievable performance, ship them — they are "
          "debuggable, explainable, testable, and they do not drift. "
          "<b>Google's first rule of machine learning is 'don't be afraid "
          "to launch a product without machine learning'</b>, and several "
          "of the next few are about heuristics.",
          "<b>You have no labels</b>, and acquiring them costs more than "
          "the problem is worth. Labelling is usually the expensive part "
          "and is usually underestimated.",
          "<b>The data is small.</b> Below a few hundred examples a "
          "flexible model mostly fits noise, and the variance of your "
          "<i>evaluation</i> is large enough that you cannot tell whether "
          "it worked (Module 05).",
          "<b>You cannot tolerate being wrong in ways you cannot "
          "predict.</b> A learned model's failure modes are discovered "
          "empirically, not derived — which is a poor fit for systems "
          "with hard safety requirements.",
          "<b>Or the cost of being wrong falls on someone who did not "
          "choose to be subject to it.</b> That is a reason for "
          "considerably more care in evaluation and monitoring "
          "(Module 13), and it is not automatically a reason to refuse "
          "— but it changes what an acceptable error rate is, and who "
          "gets to decide."]),
  ("callout", "The baseline is not optional",
   ["<b>Always compute a trivial baseline before training anything:</b> "
    "predict the majority class, predict the mean, predict last week's "
    "value, or use the single most obvious feature.",
    "<b>A surprising number of reported models do not beat one</b>, and the "
    "paper or the dashboard rarely says so — because nobody computed "
    "it, which is a different and more forgivable failure than hiding it.",
    "<b>A baseline also calibrates the problem.</b> If the majority class "
    "is 94% of the data, then a model reporting 95% accuracy has done one "
    "percentage point of actual work, and 'our model is 95% accurate' is a "
    "deeply misleading sentence that is nonetheless true.",
    "<b>So the baseline is computed first, reported beside the result, and "
    "is the number every claim is relative to.</b> <b>Every course in this "
    "program has had this rule in some form</b> — CSCE 735 Module 07 "
    "insisted on an <i>optimised</i> serial baseline before claiming a "
    "speedup, for exactly the same reason. <b>A number without a "
    "comparison is not a result.</b>"]),
 ],
 "resources": [
   ("Stanford CS229 &mdash; lecture 1 and the supervised learning notes "
    "(free)",
    "https://cs229.stanford.edu/",
    "The &sect;1 formulation, derived rather than asserted."),
   ("James et al. &mdash; An Introduction to Statistical Learning, "
    "chapter 2 (free PDF)",
    "https://www.statlearning.com/",
    "<b>The best free statement of &sect;1 and &sect;3</b>, with the "
    "accuracy-versus-interpretability trade laid out honestly."),
   ("Google &mdash; Rules of Machine Learning (free)",
    "https://developers.google.com/machine-learning/guides/rules-of-ml",
    "<b>The &sect;4 material.</b> Rules 1 through 3 are about not using "
    "machine learning yet, which is the most useful advice in the "
    "document."),
   ("Kapoor & Narayanan &mdash; Leakage and the Reproducibility Crisis in "
    "ML-based Science (free)",
    "https://arxiv.org/abs/2207.07048",
    "<b>The &sect;2 callout, with a survey of how often it happens</b> "
    "— across seventeen fields, and the answer is 'constantly'."),
 ],
 "exercises": [
   "State a problem you care about in the &sect;1 formulation. Name D, "
   "L, and what the sample is.",
   "<b>For that problem, name which of the three substitutions is "
   "weakest</b> and why.",
   "Take a time series and evaluate a model with a random split and with "
   "a forward split. <b>Report both numbers and explain the gap.</b>",
   "<b>Construct a grouped dataset</b> (several rows per entity) and show "
   "how much a random split inflates the score.",
   "Fit a model with squared error and with absolute error on data "
   "containing outliers. Compare the fits visually.",
   "<b>Write down the cost of a false positive and a false negative</b> "
   "for a problem you know, and construct a loss that reflects it.",
   "Take a problem and <b>solve it with three <code>if</code> "
   "statements</b>. Report how far that gets you.",
   "Compute majority-class and mean baselines for three datasets and "
   "report them.",
   "<b>Find a published claim of model accuracy</b> and determine whether "
   "the baseline was reported.",
   "Write your project's evaluation protocol — split, metric, "
   "baseline — and commit it before training anything.",
 ],
 "selfcheck": [
   "State the supervised learning problem and say which quantity you can "
   "actually compute.",
   "Name the three substitutions and give a failure of each.",
   "Give six ways the i.i.d. assumption fails.",
   "Why is a random split usually wrong, and what should you split by?",
   "Why is the loss not the goal, and what should you do about it?",
   "Give five reasons not to use machine learning.",
   "Why is a trivial baseline mandatory, and what does it calibrate?",
 ],
},

]

for _b in ("c633_b2", "c633_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
