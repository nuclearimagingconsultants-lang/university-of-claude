# -*- coding: utf-8 -*-
"""CSCE 633 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Linear Models",
 "subtitle": "Derived from the loss, not recited from a formula.",
 "question": "Where does the fitting rule come from?",
 "outcomes": [
     "Derive the normal equations from squared loss.",
     "Explain why the closed form is rarely used.",
     "Implement gradient descent and reason about its step size.",
     "Derive logistic regression and explain why squared loss fails for "
     "it.",
     "Explain convexity and what it guarantees.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Least squares",
   "blurb": "The derivation, which is three lines."},

  {"t": "eq", "kicker": "Derivation", "title": "From loss to normal equations",
   "eqs": [
     ("J(w) = ‖Xw − y‖²",
      "Squared error over the whole dataset, in matrix form."),
     ("∇J = 2Xᵀ(Xw − y) = 0",
      "Set the gradient to zero. J is convex, so a stationary point is "
      "the global minimum."),
     ("w = (XᵀX)⁻¹Xᵀy",
      "The normal equations. Closed form, exact, and rarely what you "
      "should compute."),
   ],
   "caption": "<b>Three lines from 'minimise squared error' to the "
              "answer</b> — and the third line is where the practical "
              "problems start.",
   "note": "Students memorise line 3 and cannot derive it. The derivation "
           "is the point."},

  {"t": "callout", "title": "Do not invert the matrix",
   "kind": "The numerical point",
   "body": ["<b>Forming XᵀX squares the condition number</b>, so a "
            "mildly ill-conditioned X becomes a badly ill-conditioned "
            "system — and the solution loses half its digits.",
            "<b>Solve the least-squares problem directly with QR or "
            "SVD</b>, which never form XᵀX at all.",
            "<b>And explicit inversion is worse than solving</b> in every "
            "case — <code>solve(A, b)</code> rather than "
            "<code>inv(A) @ b</code>, always.",
            "<b>This is CSCE 620's predicate lesson in another "
            "domain:</b> the mathematically equivalent expression is not "
            "the numerically equivalent one, and the textbook form is "
            "chosen for legibility rather than for evaluation."]},

  {"t": "table", "kicker": "Scaling", "title": "Closed form against gradient descent",
   "header": ["", "Normal equations", "Gradient descent"],
   "widths": [2.6, 4.5, 5.0],
   "rows": [
     ["<b>Cost</b>", "<b>O(nd&#178; + d&#179;)</b>", "<b>O(nd) per step</b>"],
     ["<b>Large d</b>", "<b>d&#179; dominates; infeasible past ~10⁴</b>", "<b>Fine</b>"],
     ["<b>Large n</b>", "Must hold X in memory", "<b>Stochastic version streams</b>"],
     ["Exactness", "<b>Exact in one step</b>", "Iterative; needs a stopping rule"],
     ["<b>Other losses</b>", "<b>Only squared error</b>", "<b>Any differentiable loss</b>"],
   ],
   "footnote": "<b>The last row is the decisive one.</b> Gradient descent "
               "generalises to everything; the closed form does not "
               "generalise at all.",
   "note": "That's why everything downstream is gradient-based."},

  {"t": "section", "label": "Part 2", "title": "Gradient descent",
   "blurb": "The algorithm everything else is built on."},

  {"t": "code", "kicker": "GD", "title": "The algorithm, and the step size",
   "lang": "text", "code": """
  repeat:
      w <- w - eta * grad_J(w)

  THE STEP SIZE eta DECIDES EVERYTHING:
      too small  -> converges, slowly, and you conclude it is stuck
      too large  -> oscillates, or diverges to NaN in a few steps
      just right -> and "right" depends on the curvature, which
                    changes as you move

  FEATURE SCALING IS NOT OPTIONAL.
      If one feature ranges over [0,1] and another over [0,10^6],
      the loss surface is a long thin valley. Gradient descent
      oscillates across the narrow direction and crawls along the
      long one. The SAME model, with features standardised,
      converges in a fraction of the steps.

  VARIANTS, in the order they matter:
      stochastic / mini-batch  -- estimate the gradient from a
          subset. Noisier steps, far more of them per second.
      momentum  -- accumulate a velocity; damps the oscillation
      Adam  -- per-parameter adaptive step sizes. The default,
          and Module 03 of CSCE 636 is about when it is not.
""",
   "caption": "<b>Feature scaling is the single highest-value "
              "preprocessing step</b> and is routinely skipped.",
   "note": "The thin-valley picture is what makes scaling obviously "
           "necessary rather than superstition."},

  {"t": "callout", "title": "Convexity is what makes any of this safe",
   "kind": "Why linear models are a good starting point",
   "body": ["<b>A convex function has one minimum, and any local minimum "
            "is global.</b>",
            "<b>So gradient descent on a convex loss cannot get stuck "
            "somewhere wrong</b> — only converge slowly, which is a "
            "tuning problem rather than a correctness one.",
            "<b>Squared loss and logistic loss over linear models are "
            "both convex.</b> So is the SVM's hinge loss (Module 07).",
            "<b>Neural networks are not convex</b>, which is why "
            "CSCE 636 spends so much time on optimisation. <b>The "
            "surprising empirical fact is that it works anyway</b>, and "
            "nobody fully knows why."]},

  {"t": "section", "label": "Part 3", "title": "Logistic regression",
   "blurb": "Classification, derived the same way."},

  {"t": "eq", "kicker": "Derivation", "title": "Why the sigmoid, and why not squared loss",
   "eqs": [
     ("P(y=1 | x) = σ(wᵀx) = 1 / (1 + e^(−wᵀx))",
      "Squash the linear score into (0,1) so it can be a probability."),
     ("L = −Σ [ y log p + (1−y) log(1−p) ]",
      "Negative log-likelihood — cross-entropy. Convex in w."),
     ("∇L = Xᵀ(p − y)",
      "The same form as least squares, with p in place of the prediction. "
      "That is not a coincidence."),
   ],
   "caption": "<b>Squared loss on a sigmoid is non-convex</b>, and it "
              "produces vanishing gradients when the model is confidently "
              "wrong — which is exactly when you need a large "
              "gradient.",
   "note": "The vanishing-gradient-when-confidently-wrong argument is the "
           "real reason."},

  {"t": "callout", "title": "Logistic regression outputs probabilities, and that matters",
   "kind": "An underrated property",
   "body": ["<b>Most classifiers output a score; logistic regression "
            "outputs a <i>calibrated</i> probability</b> — at least when "
            "the model is well specified.",
            "<b>So the threshold is yours to choose</b>, from the cost of "
            "each error type (Module 01 §3), rather than fixed at 0.5 "
            "by convention.",
            "<b>And probabilities compose.</b> They can be combined, "
            "used in expected-value calculations, and compared across "
            "models.",
            "<b>Many stronger classifiers are badly calibrated</b> "
            "— boosted trees and neural networks both are — <b>which "
            "Module 05 addresses, and which is a real reason to keep a "
            "linear model in the comparison.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Why linear is still the first thing",
   "blurb": "Despite everything that followed it."},

  {"t": "bullets", "kicker": "Reasons", "title": "What a linear model gives you",
   "items": [
     "<b>A baseline that is frequently hard to beat</b> on tabular data "
     "with limited samples.",
     "",
     "<b>Coefficients you can read</b> — direction, magnitude, and "
     "significance, which is a genuine explanation rather than an "
     "attribution heuristic.",
     "",
     "<b>Calibrated probabilities</b>, per Part 3.",
     "",
     "<b>Training that is fast enough to cross-validate exhaustively</b> "
     "and to retrain constantly.",
     "",
     "<b>And a diagnostic:</b> if a linear model does nearly as well as "
     "a complex one, <b>the problem is mostly linear</b> — which is "
     "useful information about the problem.",
   ],
   "footnote": "<b>Fit a linear model first, always.</b> It costs minutes "
               "and tells you what kind of problem you have."},
 ],
 "takeaways": [
   "The normal equations fall out of setting the gradient of squared loss "
   "to zero, and convexity makes that stationary point the global minimum.",
   "Forming XᵀX squares the condition number — solve with QR or SVD "
   "and never invert explicitly.",
   "Gradient descent generalises to any differentiable loss while the "
   "closed form works only for squared error, which is why everything "
   "downstream is gradient-based.",
   "Feature scaling turns a long thin valley into a round bowl and is the "
   "highest-value preprocessing step available.",
   "Squared loss on a sigmoid is non-convex and gives vanishing gradients "
   "exactly when the model is confidently wrong; cross-entropy does not.",
   "Linear models give calibrated probabilities, readable coefficients, and "
   "a diagnostic about how linear the problem is.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Least squares"),
  ("eq", "J(w) = &#8214;Xw &minus; y&#8214;&#178; "
         "&nbsp;&rarr;&nbsp; &nabla;J = 2X<super>T</super>(Xw &minus; y) "
         "= 0 &nbsp;&rarr;&nbsp; w = (X<super>T</super>X)<super>&minus;1"
         "</super>X<super>T</super>y"),
  ("p", "<b>Three steps from 'minimise squared error' to the answer.</b> "
        "The loss is convex in w (it is a positive semidefinite quadratic), "
        "so setting the gradient to zero finds the global minimum rather "
        "than merely a stationary point. <b>Most people can recite the "
        "third expression and cannot derive it</b>, which matters because "
        "the derivation is what generalises — the same three steps "
        "with a different loss give you a different estimator, and "
        "&sect;3 does exactly that."),
  ("callout", "Do not invert the matrix",
   ["<b>Forming X<super>T</super>X squares the condition number of X</b>, "
    "so a matrix that was mildly ill-conditioned becomes badly so, and the "
    "computed solution loses roughly half its significant digits. This is a "
    "real effect on real data with correlated features.",
    "<b>Solve the least-squares problem directly with a QR decomposition "
    "or an SVD</b>, both of which work on X itself and never form "
    "X<super>T</super>X. Every numerical library does this; "
    "<code>lstsq</code> is the function, not <code>inv</code>.",
    "<b>And explicit inversion is worse than solving in every case.</b> "
    "<code>solve(A, b)</code> rather than <code>inv(A) @ b</code> — "
    "always, for any linear system, in any language. The inverse is a "
    "mathematical object that is almost never the right computational one.",
    "<b>This is CSCE 620 Module 01's lesson in a different domain:</b> "
    "<b>the mathematically equivalent expression is not the numerically "
    "equivalent one</b>. The textbook form is written for legibility and "
    "proof, not for evaluation, and taking it as an implementation "
    "specification is a recurring error across every computational "
    "subject."]),
  ("table", ["", "Normal equations", "Gradient descent"],
   [["<b>Cost</b>", "<b>O(nd&#178; + d&#179;)</b> — the cube is the "
     "solve.", "<b>O(nd) per iteration</b>, times the iteration count."],
    ["<b>Many features (large d)</b>",
     "<b>The d&#179; term dominates and becomes infeasible past roughly "
     "10<super>4</super> features.</b>", "<b>Fine.</b>"],
    ["<b>Many samples (large n)</b>",
     "X must fit in memory, or be processed in a streaming "
     "X<super>T</super>X accumulation.",
     "<b>The stochastic version streams</b> and never holds the full "
     "dataset."],
    ["<b>Exactness</b>", "<b>Exact, in one step.</b>",
     "Iterative, and needs a stopping criterion that is itself a judgement."],
    ["<b>Other loss functions</b>", "<b>Squared error only.</b>",
     "<b>Any differentiable loss.</b>"]],
   [0.21, 0.39, 0.40]),
  ("p", "<b>The last row is the decisive one.</b> The closed form is a "
        "special case that exists because squared loss happens to have a "
        "linear gradient; it generalises to nothing. <b>Gradient descent "
        "generalises to every model in this course and the next one</b>, "
        "which is why it, rather than the elegant solution, is what the "
        "field is built on."),

  ("h1", "2 &nbsp; Gradient descent"),
  ("code", """repeat:  w <- w - eta * grad_J(w)

THE STEP SIZE DECIDES EVERYTHING
  too small  -> converges slowly, and you conclude it is stuck
  too large  -> oscillates, or diverges to NaN within a few steps
  just right -> depends on the curvature, which changes as you move

FEATURE SCALING IS NOT OPTIONAL
  one feature over [0,1] and another over [0,1e6] makes the loss
  surface a long thin valley: GD oscillates across the narrow
  direction and crawls along the long one. The SAME model with
  standardised features converges in a fraction of the steps.

VARIANTS, in order of importance:
  stochastic / mini-batch  noisier steps, far more per second
  momentum                 accumulate velocity; damps oscillation
  Adam                     per-parameter adaptive steps; the
                           default, and CSCE 636 M03 is about
                           when it is not"""),
  ("callout", "Convexity is what makes this safe",
   ["<b>A convex function has a single minimum, and any local minimum is "
    "therefore the global one.</b> There are no other stationary points to "
    "be trapped in.",
    "<b>So gradient descent on a convex loss cannot converge to the wrong "
    "answer.</b> It can converge slowly, or oscillate, or stop early "
    "— all of which are tuning problems with diagnosable symptoms, "
    "not correctness problems.",
    "<b>Squared loss over a linear model is convex, and so is logistic "
    "loss</b> (&sect;3) <b>and the SVM's hinge loss</b> (Module 07). The "
    "whole of classical machine learning lives in this comfortable "
    "territory, which is why the theory is as clean as it is.",
    "<b>Neural networks are not convex</b> — the loss surface has "
    "enormous numbers of local minima and saddle points — which is "
    "why CSCE 636 Module 03 spends an entire module on optimisation. "
    "<b>The surprising empirical fact is that gradient descent works "
    "anyway</b>, reliably, on surfaces where the theory offers no "
    "guarantee whatsoever, <b>and nobody fully understands why.</b> It is "
    "worth knowing that this is an open question rather than a settled "
    "one."]),

  ("break",),
  ("h1", "3 &nbsp; Logistic regression"),
  ("eq", "P(y=1|x) = &sigma;(w<super>T</super>x) "
         "&nbsp;&nbsp;&nbsp; L = &minus;&Sigma; [ y log p + (1&minus;y) "
         "log(1&minus;p) ] &nbsp;&nbsp;&nbsp; &nabla;L = "
         "X<super>T</super>(p &minus; y)"),
  ("p", "The sigmoid squashes the linear score into (0,1) so it can be read "
        "as a probability; the loss is the negative log-likelihood, which "
        "is cross-entropy, and it is convex in w. <b>Note that the gradient "
        "has exactly the same form as least squares'</b> — the design "
        "matrix transposed, times the residual — <b>which is not a "
        "coincidence</b>: both are generalised linear models and the "
        "pattern holds for the whole family."),
  ("callout", "Why not squared loss on the sigmoid?",
   ["<b>It is not convex.</b> Composing the squared loss with the sigmoid "
    "produces a surface with local minima, so the guarantee of &sect;2 is "
    "lost for no benefit.",
    "<b>And the gradients vanish exactly when you need them most.</b> When "
    "the model predicts 0.99 and the true label is 0, the sigmoid is deep "
    "in its flat region, so its derivative is nearly zero and the squared "
    "loss produces almost no gradient. <b>The model is confidently wrong "
    "and barely corrects.</b>",
    "<b>Cross-entropy does the opposite.</b> Its gradient grows as the "
    "prediction becomes more confidently wrong — the log term diverges "
    "— so the correction is large precisely when the error is "
    "egregious.",
    "<b>This is the actual reason, and it is worth knowing rather than "
    "accepting cross-entropy as a convention.</b> The same argument "
    "recurs throughout CSCE 636: <b>a loss is chosen for the shape of its "
    "gradient, not only for what it measures.</b>"]),
  ("callout", "Logistic regression outputs probabilities, and that matters",
   ["<b>Most classifiers emit a score with no particular meaning; logistic "
    "regression emits a probability</b> that is calibrated when the model "
    "is reasonably well specified — among examples it rates at 0.7, "
    "about 70% are positive.",
    "<b>So the decision threshold is yours to choose</b>, from the "
    "relative cost of each error type (Module 01 &sect;3), rather than "
    "fixed at 0.5 by a convention that encodes equal costs. <b>Moving the "
    "threshold is free and is almost always worth doing</b>, and it is the "
    "cheapest way to respond to class imbalance (Module 05).",
    "<b>And probabilities compose.</b> They can be multiplied, used inside "
    "expected-value calculations, combined across models, and compared "
    "between systems — none of which is true of an arbitrary score.",
    "<b>Many stronger classifiers are badly calibrated.</b> Boosted trees "
    "are systematically overconfident and modern neural networks are "
    "dramatically so (a finding that surprised the field). <b>Module 05 "
    "covers measuring and fixing this</b>, and it is a real reason to keep "
    "a logistic regression in the comparison even when something else wins "
    "on accuracy."]),

  ("h1", "4 &nbsp; Why linear is still the first thing to fit"),
  ("ul", ["<b>A baseline that is frequently hard to beat</b>, particularly "
          "on tabular data with a few thousand rows — which describes "
          "a very large share of real problems.",
          "<b>Coefficients you can read.</b> Direction, magnitude, and "
          "statistical significance, which constitutes a genuine "
          "explanation of the model's behaviour rather than a post-hoc "
          "attribution heuristic applied to a black box.",
          "<b>Calibrated probabilities</b> (&sect;3), which many stronger "
          "models do not provide.",
          "<b>Training fast enough to cross-validate exhaustively</b>, to "
          "bootstrap confidence intervals, and to retrain on every data "
          "refresh without thinking about it.",
          "<b>And a diagnostic about the problem itself.</b> <b>If a linear "
          "model reaches nearly the performance of a complex one, the "
          "problem is mostly linear</b> — which tells you that further "
          "model capacity is not where the remaining gains are, and "
          "redirects effort toward features or data. <b>Fit a linear model "
          "first, always</b>; it costs minutes and it tells you what kind "
          "of problem you have."]),
 ],
 "resources": [
   ("Stanford CS229 &mdash; supervised learning notes, parts I and II "
    "(free)",
    "https://cs229.stanford.edu/",
    "<b>The derivations of &sect;1 and &sect;3</b>, including the "
    "generalised linear model framing that explains why the two gradients "
    "match."),
   ("James et al. &mdash; An Introduction to Statistical Learning, "
    "chapters 3 and 4 (free PDF)",
    "https://www.statlearning.com/",
    "Linear and logistic regression with the statistical interpretation of "
    "the coefficients, which &sect;4 relies on."),
   ("Sebastian Ruder &mdash; An Overview of Gradient Descent Optimization "
    "Algorithms (free)",
    "https://www.ruder.io/optimizing-gradient-descent/",
    "The &sect;2 variants, compared clearly, with the update rules written "
    "out."),
   ("Trefethen & Bau &mdash; Numerical Linear Algebra",
    "https://people.maths.ox.ac.uk/trefethen/text.html",
    "<b>Why not to form X<super>T</super>X</b> — the conditioning "
    "argument of &sect;1, done properly. Lecture 11 is the relevant one."),
 ],
 "exercises": [
   "Derive the normal equations from the squared loss by hand.",
   "<b>Implement least squares three ways</b> — explicit inverse, "
   "<code>solve</code>, and QR — and compare on an ill-conditioned "
   "design matrix.",
   "<b>Measure the digit loss</b>: construct X with a known condition "
   "number and compare each method against the exact answer.",
   "Implement gradient descent and sweep the step size over four orders of "
   "magnitude. Plot convergence for each.",
   "<b>Demonstrate the thin-valley problem</b>: fit with unscaled features, "
   "then standardised, and compare the step counts.",
   "Implement mini-batch gradient descent and compare wall-clock "
   "convergence against full-batch.",
   "Derive the logistic regression gradient by hand and verify it "
   "numerically.",
   "<b>Fit a sigmoid with squared loss and with cross-entropy</b> on "
   "confidently-wrong examples, and plot the gradient magnitude for each.",
   "Check whether your logistic regression is calibrated: bin the "
   "predictions and plot observed frequency against predicted probability.",
   "<b>Fit a linear model on your project dataset</b> and record the score "
   "as the benchmark every later model must beat.",
 ],
 "selfcheck": [
   "Derive the normal equations and say why the stationary point is the "
   "minimum.",
   "Why should you not form XᵀX, and what should you do instead?",
   "Compare the closed form and gradient descent on five axes, and say "
   "which row decides it.",
   "What does feature scaling fix, and why does it matter so much?",
   "What does convexity guarantee, and which models have it?",
   "Why is cross-entropy used rather than squared loss on a sigmoid?",
   "Why do calibrated probabilities matter?",
   "Give five reasons to fit a linear model first.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Bias, Variance, and Capacity",
 "subtitle": "Why more model is not more better.",
 "question": "Why does a model that fits the training data perfectly do "
             "badly?",
 "outcomes": [
     "State and interpret the bias–variance decomposition.",
     "Read a learning curve and diagnose from it.",
     "Explain capacity and how it is controlled.",
     "Distinguish underfitting from overfitting by evidence.",
     "Explain double descent and what it does not overturn.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The decomposition",
   "blurb": "Error splits into three pieces, and two are yours."},

  {"t": "eq", "kicker": "Decomposition", "title": "Expected error, split",
   "eqs": [
     ("E[(y − f̂(x))²] = Bias² + Variance + σ²",
      "For squared loss, the expected error over training sets "
      "decomposes exactly."),
     ("Bias: how wrong the average model is",
      "Error from the model class being too simple to represent the "
      "truth."),
     ("Variance: how much the model moves with the data",
      "Error from fitting the particular sample rather than the pattern. "
      "σ² is irreducible noise."),
   ],
   "caption": "<b>You control two of the three terms, and they trade "
              "against each other.</b> The third is the floor.",
   "note": "The irreducible term is what makes 'just get a better model' "
           "finite."},

  {"t": "table", "kicker": "Symptoms", "title": "Diagnosing which one you have",
   "header": ["Symptom", "Diagnosis", "What helps"],
   "widths": [3.3, 3.0, 5.8],
   "rows": [
     ["<b>Train error high, val ≈ train</b>", "<b>High bias</b>", "<b>More capacity; better features; less regularisation</b>"],
     ["<b>Train error low, val ≫ train</b>", "<b>High variance</b>", "<b>More data; regularisation; less capacity</b>"],
     ["<b>Both high, gap large</b>", "Both", "Features first, then capacity"],
     ["<b>Both low</b>", "<b>Done</b>", "<b>Stop. Check for leakage</b>"],
     ["Val error rising with training", "Overfitting over time", "<b>Early stopping</b>"],
   ],
   "footnote": "<b>'Both low' deserves suspicion</b> — it is the "
               "signature of leakage as often as of success "
               "(Module 12).",
   "note": "Teaching suspicion of good results is worth more than "
           "teaching how to get them."},

  {"t": "callout", "title": "More data fixes variance and does nothing for bias",
   "kind": "The asymmetry that decides your next move",
   "body": ["<b>High variance means the model is fitting the sample.</b> "
            "More samples make the sample look more like the distribution, "
            "so the problem shrinks.",
            "<b>High bias means the model class cannot represent the "
            "truth.</b> A line fitted to a parabola is equally wrong with "
            "a million points.",
            "<b>So diagnose before collecting.</b> Data acquisition is "
            "usually the most expensive action available and it is "
            "frequently the wrong one.",
            "<b>The learning curve tells you which</b> — if validation "
            "error has flattened well above training error, more data will "
            "help; if the two have converged, it will not."]},

  {"t": "section", "label": "Part 2", "title": "Learning curves",
   "blurb": "The diagnostic instrument."},

  {"t": "code", "kicker": "Learning curves", "title": "Two curves, four shapes",
   "lang": "text", "code": """
  Plot TRAINING error and VALIDATION error against training set
  size. Not against epochs -- against how much DATA you used.

  HIGH BIAS                      HIGH VARIANCE
    err |                          err |
        |___________ val               |  \\___________ val
        |___________ train             |
        |                              |   ___________ train
        +-------------- n              +-------------- n

    Both converge, HIGH.            Large persistent GAP.
    More data will not help.        More data WILL help.
    Need capacity or features.      Or regularise.

  WHAT THE SHAPES TELL YOU:
    curves converged and low     -> done (and be suspicious)
    curves converged and high    -> bias. Add capacity.
    gap still closing at max n   -> get more data; it is working
    gap flat and wide            -> regularise; data is not enough
    val curve RISING             -> early stop

  This single plot answers "what should I do next?" better than
  any other diagnostic, and it costs one training run per point.
""",
   "caption": "<b>Plot against dataset size, not epochs</b> — the two "
              "answer different questions and the second is routinely "
              "mistaken for the first.",
   "note": "The data-size versus epochs distinction matters and is often "
           "muddled."},

  {"t": "section", "label": "Part 3", "title": "Capacity",
   "blurb": "What there is more or less of."},

  {"t": "bullets", "kicker": "Capacity", "title": "What controls how much a model can fit",
   "items": [
     "<b>Parameter count</b> — the obvious one, and the least reliable "
     "predictor.",
     "",
     "<b>Function class</b> — polynomial degree, tree depth, kernel "
     "choice.",
     "",
     "<b>Regularisation strength</b> (Module 04) — which reduces "
     "<i>effective</i> capacity without changing the parameter count.",
     "",
     "<b>Training time</b> — early stopping is capacity control, "
     "because an under-trained model has not reached the flexible part of "
     "its class.",
     "",
     "<b>And data augmentation</b>, which raises the effective sample "
     "size rather than lowering capacity, with the same effect on the "
     "gap.",
   ],
   "footnote": "<b>'Effective capacity' is the useful notion</b> and it "
               "is not the parameter count — which is what makes the "
               "next slide possible."},

  {"t": "section", "label": "Part 4", "title": "Double descent",
   "blurb": "The modern complication, stated carefully."},

  {"t": "callout", "title": "Double descent: the curve has a second slope",
   "kind": "What was actually discovered",
   "body": ["<b>The classical picture:</b> test error falls, then rises "
            "as capacity grows past the sweet spot. A U.",
            "<b>What is observed in very large models:</b> error rises to "
            "a peak at the <i>interpolation threshold</i> — where the "
            "model has just enough capacity to fit the training data "
            "exactly — <b>and then falls again</b> as capacity grows "
            "further.",
            "<b>So heavily overparameterised models can generalise "
            "well</b>, which the classical account did not predict.",
            "<b>It does not overturn bias–variance.</b> The "
            "decomposition is an identity; it is always true. <b>What "
            "changed is the belief that variance must increase with "
            "parameter count</b> — implicit regularisation from the "
            "optimiser appears to keep it down."]},

  {"t": "callout", "title": "What this means for your project",
   "kind": "The practical reading",
   "body": ["<b>At the scale of this course, the classical picture "
            "holds.</b> With a few thousand samples and a tabular problem, "
            "more capacity past the sweet spot hurts.",
            "<b>Double descent shows up with enormous models and enormous "
            "data</b>, which is CSCE 636's territory rather than this "
            "module's.",
            "<b>And the diagnosis procedure is unchanged.</b> Plot the "
            "learning curves, read the gap, and act on it.",
            "<b>The useful lesson is epistemic:</b> <b>a well-established "
            "picture was incomplete and the correction came from "
            "measurement, not theory.</b> Which is a reason to keep "
            "plotting rather than reasoning from the textbook curve."]},
 ],
 "takeaways": [
   "Expected squared error decomposes exactly into bias squared, variance, "
   "and irreducible noise — you control two terms and the third is "
   "the floor.",
   "Train error high with validation close means bias; train error low with "
   "a large gap means variance.",
   "More data fixes variance and does nothing for bias, so diagnose before "
   "spending on data acquisition.",
   "Plot learning curves against training set size rather than epochs — "
   "they answer different questions.",
   "Effective capacity is controlled by function class, regularisation, and "
   "training time, not just parameter count.",
   "Double descent shows overparameterised models can generalise, which "
   "does not overturn the decomposition — it overturns the assumption "
   "that variance grows with parameter count.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The decomposition"),
  ("eq", "E[(y &minus; f&#770;(x))&#178;] = Bias&#178; + Variance + "
         "&sigma;&#178;"),
  ("p", "<b>For squared loss, the expected error over random draws of the "
        "training set decomposes exactly into three terms.</b> <b>Bias</b> "
        "is how wrong the <i>average</i> fitted model is — error from "
        "the model class being too restricted to represent the truth. "
        "<b>Variance</b> is how much the fitted model moves as the training "
        "sample changes — error from fitting this particular sample "
        "rather than the underlying pattern. <b>&sigma;&#178; is "
        "irreducible noise</b> in the labels themselves, and it is the "
        "floor: no model, however good, goes below it. <b>You control two "
        "of the three, and they trade against each other</b>, which is why "
        "the question is never 'is this model good' but 'which term is "
        "limiting me'."),
  ("table", ["Symptom", "Diagnosis", "What helps"],
   [["<b>Training error high, validation error close to it</b>",
     "<b>High bias (underfitting).</b>",
     "<b>More capacity, better features, or less regularisation.</b> "
     "<b>More data will not help</b> — see the callout."],
    ["<b>Training error low, validation error much higher</b>",
     "<b>High variance (overfitting).</b>",
     "<b>More data, stronger regularisation, or less capacity.</b> "
     "Also data augmentation, which raises the effective sample size."],
    ["<b>Both errors high <i>and</i> the gap is large</b>",
     "Both at once, which is common on hard problems.",
     "Features first — they attack bias without increasing variance "
     "— then capacity."],
    ["<b>Both errors low</b>", "<b>Done.</b>",
     "<b>Stop, and then be suspicious.</b> <b>This is the signature of "
     "leakage as often as of success</b> (Module 12 &sect;1), and the "
     "right response to an unexpectedly good result is an audit rather than "
     "a celebration."],
    ["<b>Validation error rising as training continues</b>",
     "Overfitting over training time rather than over capacity.",
     "<b>Early stopping</b>, which is capacity control in disguise "
     "(&sect;3)."]],
   [0.26, 0.22, 0.52]),
  ("callout", "More data fixes variance and does nothing for bias",
   ["<b>High variance means the model is fitting the particular sample.</b> "
    "More samples make that sample a better approximation of the "
    "distribution, so the error from fitting it shrinks — directly and "
    "reliably.",
    "<b>High bias means the model class cannot represent the truth at "
    "all.</b> A straight line fitted to a parabola is exactly as wrong with "
    "a million points as with a hundred; the extra data simply pins down "
    "the best wrong answer more precisely.",
    "<b>So diagnose before collecting.</b> <b>Data acquisition is usually "
    "the most expensive action available</b> — in money, in time, and "
    "frequently in labelling effort — <b>and it is frequently the "
    "wrong one</b>, chosen because it is the obvious response to 'the model "
    "is not good enough'.",
    "<b>The learning curve answers this directly</b> (&sect;2). If the "
    "validation curve is still descending at your current sample size, more "
    "data will help and you can extrapolate roughly how much. <b>If the "
    "two curves have converged, more data buys nothing and the money should "
    "go elsewhere.</b> This is one of the highest-value diagnostics in "
    "applied machine learning and it costs a handful of training runs."]),

  ("h1", "2 &nbsp; Learning curves"),
  ("code", """Plot TRAINING and VALIDATION error against TRAINING SET SIZE
(not against epochs -- they answer different questions).

HIGH BIAS                        HIGH VARIANCE
  err |                            err |
      |____________ val                |  \\___________ val
      |____________ train              |
      |                                |   ___________ train
      +--------------- n               +--------------- n

  Converged, HIGH.                  Large persistent GAP.
  More data will NOT help.          More data WILL help.
  Add capacity or features.         Or regularise.

READING THE SHAPES
  converged and low      -> done (and be suspicious: Module 12)
  converged and high     -> bias; add capacity
  gap still closing      -> get more data; it is working
  gap flat and wide      -> regularise; data alone is not enough
  validation RISING      -> early stop"""),
  ("p", "<b>Plotting against dataset size and plotting against epochs "
        "answer different questions, and the second is routinely mistaken "
        "for the first.</b> The epoch curve tells you when to stop "
        "training this model; <b>the data-size curve tells you whether to "
        "collect more data</b>, which is a far more consequential decision. "
        "<b>This single plot answers 'what should I do next?' better than "
        "any other diagnostic available</b>, and it costs one training run "
        "per point — which, for the models in this course, is "
        "minutes."),

  ("break",),
  ("h1", "3 &nbsp; Capacity"),
  ("ul", ["<b>Parameter count.</b> The obvious measure, and <b>the least "
          "reliable predictor of generalisation</b> — which &sect;4 "
          "makes vivid.",
          "<b>Function class.</b> Polynomial degree, tree depth, number of "
          "neighbours, kernel choice. Usually the most interpretable knob.",
          "<b>Regularisation strength</b> (Module 04), which reduces "
          "<i>effective</i> capacity while leaving the parameter count "
          "untouched — the model can still express complex functions "
          "and is penalised for doing so.",
          "<b>Training time.</b> <b>Early stopping is capacity "
          "control</b>, because an under-trained model has not yet reached "
          "the flexible region of its function class. This is not an "
          "analogy; for linear models with gradient descent it can be shown "
          "equivalent to a form of ridge regression.",
          "<b>And data augmentation</b>, which raises the effective sample "
          "size rather than lowering capacity — a different mechanism "
          "with the same effect on the generalisation gap. <b>'Effective "
          "capacity' is the useful notion and it is not the parameter "
          "count</b>, which is exactly what makes double descent "
          "possible."]),

  ("h1", "4 &nbsp; Double descent"),
  ("callout", "The curve has a second descent",
   ["<b>The classical picture:</b> as capacity grows, test error falls to a "
    "minimum and then rises, because variance overtakes the reduction in "
    "bias. A U-shaped curve, and the job is to find its bottom.",
    "<b>What is observed in very large models:</b> test error rises to a "
    "peak at the <i>interpolation threshold</i> — the capacity at "
    "which the model can just exactly fit the training data — "
    "<b>and then falls again, sometimes below the classical minimum</b>, as "
    "capacity continues to grow.",
    "<b>So heavily overparameterised models can generalise well</b>, which "
    "the classical account did not merely fail to predict but positively "
    "argued against. This is the empirical fact underneath modern deep "
    "learning working at all.",
    "<b>It does not overturn the bias–variance decomposition.</b> "
    "<b>That decomposition is an algebraic identity</b> — it is always "
    "true, for any estimator. <b>What was overturned is the separate "
    "assumption that variance necessarily increases with parameter "
    "count.</b> Among the many functions that interpolate the training "
    "data, gradient descent appears to find low-complexity ones — "
    "implicit regularisation from the optimiser itself — so the "
    "effective capacity does not grow the way the parameter count "
    "does."]),
  ("callout", "What this means for your project",
   ["<b>At the scale of this course, the classical picture holds.</b> With "
    "a few thousand samples and a tabular problem, adding capacity past the "
    "sweet spot degrades test performance exactly as the U-curve predicts, "
    "and you should act accordingly.",
    "<b>Double descent appears with very large models on very large "
    "data</b> — CSCE 636's territory, not this module's. Knowing it "
    "exists prevents you from concluding that a large model is "
    "<i>necessarily</i> overfitting, which is a conclusion people reach "
    "from the textbook curve alone.",
    "<b>And the diagnosis procedure is entirely unchanged.</b> Plot the "
    "learning curves, read the gap, act on it. <b>The empirical method "
    "survives the theory changing</b>, which is precisely why the course "
    "emphasises it.",
    "<b>The genuinely useful lesson here is epistemic.</b> <b>A "
    "well-established picture, taught confidently for decades, turned out "
    "to be incomplete — and the correction came from measurement "
    "rather than from theory</b>, when people trained models larger than "
    "the theory contemplated and plotted what happened. <b>That is a "
    "reason to keep plotting rather than reasoning from the remembered "
    "curve</b>, and it generalises well beyond this subject."]),
 ],
 "resources": [
   ("James et al. &mdash; An Introduction to Statistical Learning, "
    "chapter 2 (free PDF)",
    "https://www.statlearning.com/",
    "<b>The decomposition of &sect;1</b>, derived, with the clearest "
    "available figures."),
   ("Andrew Ng &mdash; Machine Learning Yearning (free)",
    "https://info.deeplearning.ai/machine-learning-yearning-book",
    "<b>The &sect;2 diagnostic procedure as an engineering "
    "discipline</b> — short chapters, entirely about deciding what to "
    "do next."),
   ("Belkin, Hsu, Ma & Mandal &mdash; Reconciling modern machine learning "
    "practice and the bias-variance trade-off (free)",
    "https://arxiv.org/abs/1812.11118",
    "<b>The double descent paper.</b> The figures are the argument."),
   ("Hastie et al. &mdash; The Elements of Statistical Learning, chapter 7 "
    "(free PDF)",
    "https://hastie.su.domains/ElemStatLearn/",
    "Model assessment and selection at depth, including the effective "
    "degrees of freedom notion behind &sect;3."),
 ],
 "exercises": [
   "<b>Fit polynomials of degree 1 to 15</b> to noisy data from a known "
   "function. Plot training and test error against degree.",
   "<b>Estimate bias and variance empirically</b> by refitting on many "
   "bootstrap samples and measuring the spread of predictions.",
   "Plot learning curves for your project dataset and <b>write the "
   "diagnosis on the plot</b>.",
   "<b>Demonstrate that more data does not fix bias</b>: fit a line to a "
   "parabola at n = 100 and n = 100,000.",
   "Demonstrate that more data does fix variance, with the same model on "
   "the same sizes.",
   "Plot error against epochs and against dataset size for the same model. "
   "Explain what each tells you.",
   "<b>Show that early stopping acts as regularisation</b> by comparing it "
   "against an explicit penalty.",
   "Push a model past the interpolation threshold on a small dataset and "
   "plot test error against capacity. <b>Report whether you see a second "
   "descent.</b>",
   "Take an unexpectedly good result and audit it for leakage before "
   "believing it.",
   "For your project, state which term currently limits you and what you "
   "will do about it.",
 ],
 "selfcheck": [
   "State the decomposition and say which terms you control.",
   "Give five learning-curve symptoms and the diagnosis for each.",
   "Why does more data fix variance and not bias?",
   "Why plot against dataset size rather than epochs?",
   "Name five things that control effective capacity.",
   "Why is early stopping a form of capacity control?",
   "State double descent and say precisely what it does and does not "
   "overturn.",
   "What should you do when both errors are low?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Regularisation and Model Selection",
 "subtitle": "Spending capacity carefully, and choosing without cheating.",
 "question": "How do you control overfitting and pick between models?",
 "outcomes": [
     "Explain L2 and L1 regularisation and what each produces.",
     "Explain why L1 gives sparsity, geometrically.",
     "Implement cross-validation correctly, including preprocessing.",
     "Explain the three-way split and why the test set is spent once.",
     "Compare hyperparameter search strategies.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Penalising complexity",
   "blurb": "Two penalties, two very different effects."},

  {"t": "eq", "kicker": "Penalties", "title": "Ridge and lasso",
   "eqs": [
     ("Ridge:  J(w) = ‖Xw − y‖² + λ‖w‖²",
      "L2 penalty. Shrinks all coefficients toward zero, none exactly to "
      "zero."),
     ("Lasso:  J(w) = ‖Xw − y‖² + λ‖w‖₁",
      "L1 penalty. Drives many coefficients exactly to zero — it selects "
      "features."),
     ("λ → 0 recovers least squares; λ → ∞ gives w = 0",
      "λ is the capacity dial, chosen by cross-validation, never by "
      "looking at the test set."),
   ],
   "caption": "<b>Ridge has a closed form; lasso does not</b>, because the "
              "L1 norm is not differentiable at zero — which is "
              "exactly why it produces zeros.",
   "note": "The non-differentiability is the mechanism, not an "
           "inconvenience."},

  {"t": "callout", "title": "Why L1 gives sparsity, geometrically",
   "kind": "The argument worth seeing once",
   "body": ["<b>Think of the penalty as a constraint region</b> that the "
            "solution must lie in, with the loss contours expanding until "
            "they touch it.",
            "<b>The L2 region is a sphere.</b> A smooth surface — the "
            "contact point is almost never on an axis, so no coefficient "
            "is exactly zero.",
            "<b>The L1 region is a diamond, with corners on the "
            "axes.</b> Expanding contours are disproportionately likely to "
            "touch a corner.",
            "<b>And a corner <i>is</i> a sparse solution</b> — the other "
            "coordinates are exactly zero there. <b>The sparsity comes "
            "from the shape of the constraint, which is worth drawing "
            "once.</b>"]},

  {"t": "table", "kicker": "Choosing", "title": "Which penalty",
   "header": ["Penalty", "Produces", "Use when"],
   "widths": [2.6, 4.4, 5.1],
   "rows": [
     ["<b>L2 (ridge)</b>", "<b>Small, spread-out coefficients</b>", "<b>Many weak correlated features. The default</b>"],
     ["<b>L1 (lasso)</b>", "<b>Exact zeros; a selected subset</b>", "<b>You want to know which features matter</b>"],
     ["<b>Elastic net</b>", "Both; groups of correlated features", "<b>Correlated features where lasso picks arbitrarily</b>"],
     ["Early stopping", "Implicit shrinkage", "Iterative models; costs nothing"],
     ["<b>Dropout, augmentation</b>", "Noise-based", "<b>Neural networks (CSCE 636)</b>"],
   ],
   "footnote": "<b>Lasso picks one of a correlated group arbitrarily</b>, "
               "which makes its feature selection unstable — elastic "
               "net exists because of this.",
   "note": "The lasso instability caveat matters for anyone reading "
           "selected features as a finding."},

  {"t": "section", "label": "Part 2", "title": "Cross-validation",
   "blurb": "Estimating performance without spending the test set."},

  {"t": "code", "kicker": "The trap", "title": "Preprocessing must be inside the fold",
   "lang": "python", "code": """
# WRONG -- and extremely common.
X_scaled = StandardScaler().fit_transform(X)      # <-- sees ALL data
scores = cross_val_score(model, X_scaled, y, cv=5)
#  The scaler learned the mean and std of the VALIDATION rows.
#  Information leaked from the held-out fold into the training.
#  The score is optimistic, and silently so.

# ALSO WRONG, and worse:
X_sel = SelectKBest(k=20).fit_transform(X, y)     # <-- sees ALL y
scores = cross_val_score(model, X_sel, y, cv=5)
#  Feature selection used the labels of the held-out rows.
#  On pure noise this can produce 80%+ "accuracy".

# RIGHT -- the pipeline is the estimator; it is refit per fold.
pipe = Pipeline([
    ("scale",  StandardScaler()),
    ("select", SelectKBest(k=20)),
    ("model",  LogisticRegression()),
])
scores = cross_val_score(pipe, X, y, cv=5)

# RULE: anything that LEARNS from data goes inside the pipeline.
""",
   "caption": "<b>Feature selection outside the fold can produce strong "
              "results on pure noise.</b> This is a reproducible "
              "demonstration and worth running.",
   "note": "Running the noise demo yourself is what makes this stick."},

  {"t": "callout", "title": "The three-way split, and spending the test set",
   "kind": "The protocol",
   "body": ["<b>Training set: fits the parameters. Validation set: "
            "chooses the hyperparameters. Test set: estimates "
            "performance, once.</b>",
            "<b>Every time you look at the test set and then change "
            "something, you have used it for selection</b> — and its "
            "estimate becomes optimistic.",
            "<b>So the test set is spent once, at the end, and the number "
            "is reported whatever it is.</b>",
            "<b>With cross-validation the validation set is the folds, "
            "and hyperparameter search needs <i>nested</i> CV</b> to be "
            "unbiased — an outer loop for estimation and an inner one for "
            "selection. <b>Rarely done, and the inner-loop score is "
            "therefore usually optimistic.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Searching",
   "blurb": "Finding the hyperparameters."},

  {"t": "table", "kicker": "Search", "title": "Hyperparameter search strategies",
   "header": ["Strategy", "How", "Character"],
   "widths": [2.7, 4.3, 5.1],
   "rows": [
     ["<b>Grid search</b>", "Every combination on a grid", "<b>Wasteful — most dimensions do not matter</b>"],
     ["<b>Random search</b>", "<b>Sample the space at random</b>", "<b>Beats grid at equal budget. Use this</b>"],
     ["<b>Bayesian / TPE</b>", "Model the response surface", "<b>Better per trial; worth it when trials are slow</b>"],
     ["<b>Successive halving</b>", "<b>Many configs briefly; promote the best</b>", "<b>Very effective for expensive training</b>"],
     ["Hand tuning", "A human looks at curves", "<b>Underrated; the human sees structure</b>"],
   ],
   "footnote": "<b>Bergstra and Bengio's result:</b> random search beats "
               "grid search at the same budget, because only a few "
               "hyperparameters matter and grid wastes trials on the "
               "others.",
   "note": "That result is simple, well-established, and widely ignored."},

  {"t": "section", "label": "Part 4", "title": "Choosing a model",
   "blurb": "When the difference is not real."},

  {"t": "callout", "title": "Most reported differences are within the noise",
   "kind": "The statistical point",
   "body": ["<b>A validation score is an estimate with a standard "
            "error.</b> On 1,000 validation samples, an accuracy near 90% "
            "has a standard error of about 1 percentage point.",
            "<b>So 90.4% against 89.8% is not a result.</b> It is the "
            "same number measured twice.",
            "<b>Report the variability</b> — the spread across "
            "cross-validation folds, or a bootstrap interval — rather "
            "than a point estimate.",
            "<b>And prefer the simpler model when they tie.</b> It trains "
            "faster, explains better, and degrades more predictably. "
            "<b>This is CSCE 735's 'report the distribution' rule in "
            "another domain.</b>"]},
 ],
 "takeaways": [
   "Ridge shrinks all coefficients and lasso drives many to exactly zero, "
   "because the L1 constraint region has corners on the axes.",
   "Lasso selects one of a correlated group arbitrarily, which makes its "
   "feature selection unstable — elastic net exists for that reason.",
   "Anything that learns from data — scaling, selection, imputation "
   "— must go inside the cross-validation fold.",
   "Feature selection performed outside the fold can produce strong "
   "apparent accuracy on pure noise.",
   "The test set is spent once; looking at it and then changing something "
   "converts it into a validation set.",
   "Random search beats grid search at equal budget, and most reported "
   "model differences are within the standard error of the estimate.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Penalising complexity"),
  ("eq", "Ridge: &#8214;Xw &minus; y&#8214;&#178; + "
         "&lambda;&#8214;w&#8214;&#178; "
         "&nbsp;&nbsp;&nbsp;&nbsp; Lasso: &#8214;Xw &minus; "
         "y&#8214;&#178; + &lambda;&#8214;w&#8214;<sub>1</sub>"),
  ("p", "&lambda; is the capacity dial of Module 03 &sect;3, made "
        "explicit. <b>&lambda; &rarr; 0 recovers ordinary least squares; "
        "&lambda; &rarr; &infin; drives every coefficient to zero.</b> It "
        "is chosen by cross-validation (&sect;2) and <b>never by looking "
        "at the test set</b>. <b>Ridge has a closed form</b> — "
        "(X<super>T</super>X + &lambda;I)<super>&minus;1</super>"
        "X<super>T</super>y, and the added &lambda;I incidentally fixes "
        "the conditioning problem of Module 02 &sect;1 — <b>while "
        "lasso does not, because the L1 norm is not differentiable at "
        "zero.</b> That non-differentiability is not an inconvenience to be "
        "worked around; it is precisely the mechanism that produces "
        "zeros."),
  ("callout", "Why L1 gives sparsity, geometrically",
   ["<b>Read the penalty as a constraint:</b> minimise the loss subject to "
    "the coefficient vector lying within a region whose size is set by "
    "&lambda;. The solution is where the expanding loss contours first "
    "touch that region.",
    "<b>The L2 constraint region is a sphere</b> — a smooth surface "
    "with no distinguished points. The contact point can be anywhere on it, "
    "and the probability of landing exactly on an axis (where a coefficient "
    "is zero) is essentially nil. <b>Ridge shrinks everything and zeroes "
    "nothing.</b>",
    "<b>The L1 constraint region is a diamond — a cross-polytope "
    "— with corners lying exactly on the axes.</b> Expanding elliptical "
    "contours are disproportionately likely to touch a corner first, "
    "because a corner protrudes.",
    "<b>And a corner <i>is</i> a sparse solution:</b> at a corner of the L1 "
    "ball, all but one coordinate is exactly zero. <b>The sparsity comes "
    "from the shape of the constraint region</b>, and the two-dimensional "
    "picture of the circle and the diamond is worth drawing once by hand "
    "— after which lasso's behaviour is obvious rather than "
    "memorised."]),
  ("table", ["Penalty", "What it produces", "When to use it"],
   [["<b>L2 (ridge)</b>", "<b>Small, spread-out coefficients; nothing "
     "exactly zero.</b>",
     "<b>Many weak, correlated features — the common case, and the "
     "sensible default.</b> It shares weight among correlated features "
     "rather than choosing."],
    ["<b>L1 (lasso)</b>",
     "<b>Exact zeros</b>, so the fit selects a subset of features.",
     "<b>When you want to know which features matter</b>, or need a small "
     "model for deployment. <b>With the caveat below.</b>"],
    ["<b>Elastic net</b>",
     "Both penalties combined; selects correlated features as groups.",
     "<b>Correlated features where lasso's arbitrary choice is a "
     "problem</b> — which is why it exists."],
    ["<b>Early stopping</b>", "Implicit shrinkage toward the "
     "initialisation.",
     "Any iterative model. Costs nothing and is frequently forgotten "
     "(Module 03 &sect;3)."],
    ["<b>Dropout, noise, augmentation</b>", "Noise-based regularisation.",
     "Neural networks — CSCE 636 Module 04."]],
   [0.18, 0.37, 0.45]),
  ("p", "<b>The lasso caveat matters.</b> Given several highly correlated "
        "features carrying the same information, <b>lasso selects one "
        "essentially arbitrarily and zeroes the rest</b> — and which "
        "one it picks can change with a small perturbation of the data. "
        "<b>So a lasso-selected feature set is not a stable finding about "
        "which variables matter</b>, and reporting it as one is a common "
        "and consequential error in applied work."),

  ("h1", "2 &nbsp; Cross-validation, done correctly"),
  ("code", """# WRONG -- and extremely common
X_scaled = StandardScaler().fit_transform(X)     # sees ALL data
cross_val_score(model, X_scaled, y, cv=5)
# the scaler learned the validation folds' mean and std.
# Optimistic, and silently so.

# ALSO WRONG, and much worse
X_sel = SelectKBest(k=20).fit_transform(X, y)    # sees ALL y
cross_val_score(model, X_sel, y, cv=5)
# selection used the HELD-OUT LABELS. On pure noise this can
# produce 80%+ "accuracy".

# RIGHT -- the pipeline IS the estimator, refit inside each fold
pipe = Pipeline([("scale",  StandardScaler()),
                 ("select", SelectKBest(k=20)),
                 ("model",  LogisticRegression())])
cross_val_score(pipe, X, y, cv=5)

# RULE: anything that LEARNS from data goes inside the pipeline."""),
  ("p", "<b>The second case is worth running yourself on random noise.</b> "
        "Generate a matrix of pure random features and random labels, "
        "select the twenty features most correlated with the labels across "
        "the whole dataset, then cross-validate. <b>You will get an "
        "accuracy far above chance on data containing no signal at "
        "all</b>, because the selection step found the features that "
        "happened to correlate with the labels <i>in the validation folds "
        "too</i>. It is a two-minute demonstration and it is considerably "
        "more convincing than the warning."),
  ("callout", "The three-way split, and spending the test set",
   ["<b>Training set fits the parameters. Validation set chooses the "
    "hyperparameters. Test set estimates performance, once.</b> The three "
    "roles are distinct and conflating any two of them produces an "
    "optimistic number.",
    "<b>Every time you look at the test set and then change something "
    "— anything — you have used it for selection.</b> It has "
    "become a validation set, and its estimate of generalisation is now "
    "biased upward by an amount you cannot measure.",
    "<b>So the test set is spent once, at the very end, and the number is "
    "reported whatever it turns out to be.</b> This requires discipline "
    "that notebooks actively undermine, which is why the project asks for "
    "the protocol to be committed before training.",
    "<b>With cross-validation the validation set is the folds themselves, "
    "and hyperparameter selection then requires <i>nested</i> "
    "cross-validation</b> to produce an unbiased estimate — an outer "
    "loop for estimating performance and an inner loop for choosing "
    "hyperparameters within each outer training set. <b>This is rarely "
    "done because it is expensive, which means most reported "
    "cross-validation scores are mildly optimistic</b> — a small "
    "effect, usually, and worth knowing about when comparing against "
    "published numbers."]),

  ("break",),
  ("h1", "3 &nbsp; Hyperparameter search"),
  ("table", ["Strategy", "How it works", "Character"],
   [["<b>Grid search</b>",
     "Every combination of a discrete grid over each hyperparameter.",
     "<b>Wasteful.</b> If only two of five hyperparameters actually matter, "
     "a grid spends most of its budget varying the irrelevant ones while "
     "sampling the important ones coarsely."],
    ["<b>Random search</b>",
     "<b>Sample configurations at random from a distribution over each "
     "hyperparameter.</b>",
     "<b>Beats grid search at the same budget</b> — Bergstra and "
     "Bengio's result — because every trial samples a new value of "
     "<i>every</i> hyperparameter, so the important ones get fine "
     "coverage. <b>Use this as the default.</b>"],
    ["<b>Bayesian optimisation / TPE</b>",
     "Build a surrogate model of the response surface and sample where it "
     "is promising or uncertain.",
     "<b>Better per trial</b>, with its own overhead. <b>Worth it when a "
     "single training run is slow</b>, which is the usual case in "
     "CSCE 636."],
    ["<b>Successive halving / Hyperband</b>",
     "<b>Train many configurations briefly, discard the worst, give the "
     "survivors more budget.</b>",
     "<b>Very effective when training is expensive and early performance "
     "predicts final performance</b> — which it usually does, but not "
     "always, and the exceptions are the configurations that start slowly "
     "and end well."],
    ["<b>Hand tuning</b>",
     "A person looks at learning curves and changes one thing.",
     "<b>Underrated.</b> A human reading a curve sees structure an "
     "automated search does not — 'this is diverging', 'this is "
     "underfitting' — and acts on the diagnosis of Module 03 rather "
     "than sampling blindly."]],
   [0.19, 0.37, 0.44]),

  ("h1", "4 &nbsp; Choosing a model"),
  ("callout", "Most reported differences are within the noise",
   ["<b>A validation score is an estimate, and it has a standard "
    "error.</b> For accuracy p measured on m validation samples, the "
    "standard error is roughly &radic;(p(1&minus;p)/m) — <b>on 1,000 "
    "samples at around 90% accuracy, that is about one percentage "
    "point.</b>",
    "<b>So 90.4% against 89.8% is not a result.</b> It is the same quantity "
    "measured twice, and declaring a winner from it is reading noise. "
    "<b>A great deal of model selection, and a great deal of published "
    "comparison, consists of exactly this.</b>",
    "<b>Report the variability.</b> The spread across cross-validation "
    "folds, or a bootstrap confidence interval, or a paired test across "
    "folds — anything that conveys how much the number would move if "
    "you had drawn a different sample.",
    "<b>And prefer the simpler model when they tie.</b> It trains faster, "
    "is easier to explain, has fewer ways to break, and degrades more "
    "predictably under distribution shift (Module 13). <b>This is "
    "CSCE 735 Module 07's 'report the distribution rather than the mean' "
    "rule, arriving in a different subject</b> — and it is the same "
    "underlying point: <b>a single number conceals whether the difference "
    "you are acting on is real.</b>"]),
 ],
 "resources": [
   ("Hastie et al. &mdash; The Elements of Statistical Learning, chapters "
    "3 and 7 (free PDF)",
    "https://hastie.su.domains/ElemStatLearn/",
    "<b>Ridge and lasso with the geometric argument of &sect;1</b>, and "
    "the model selection theory of &sect;2."),
   ("scikit-learn &mdash; cross-validation and model selection user guide "
    "(free)",
    "https://scikit-learn.org/stable/modules/cross_validation.html",
    "<b>The &sect;2 pipeline discipline</b>, with the leakage warning "
    "stated explicitly in the documentation — which is unusual and "
    "welcome."),
   ("Bergstra & Bengio &mdash; Random Search for Hyper-Parameter "
    "Optimization (free)",
    "https://www.jmlr.org/papers/v13/bergstra12a.html",
    "<b>The &sect;3 result.</b> The figures showing why grid search wastes "
    "its budget are the whole argument."),
   ("Cawley & Talbot &mdash; On Over-fitting in Model Selection and "
    "Subsequent Selection Bias (free)",
    "https://www.jmlr.org/papers/v11/cawley10a.html",
    "<b>Why the inner-loop score is optimistic</b> — the nested CV "
    "argument of &sect;2, measured."),
 ],
 "exercises": [
   "Fit ridge across a range of &lambda; and plot every coefficient's path.",
   "Do the same for lasso and <b>mark where each coefficient hits exactly "
   "zero</b>.",
   "<b>Draw the L1 and L2 constraint regions in two dimensions</b> with "
   "loss contours, and mark the contact points.",
   "<b>Demonstrate lasso's instability</b>: duplicate a feature with small "
   "noise, refit several times, and report which copy is selected.",
   "<b>Run the noise demonstration:</b> random features, random labels, "
   "feature selection outside the fold. Report the accuracy you obtain.",
   "Then put the selection inside a pipeline and report it again.",
   "Implement nested cross-validation and compare the outer-loop estimate "
   "against the inner-loop one.",
   "<b>Compare grid and random search at an equal trial budget</b> on a "
   "model with five hyperparameters of which two matter.",
   "Implement successive halving and compare against random search at "
   "equal cost.",
   "<b>Compute the standard error of your project's validation score</b> "
   "and decide whether your model differences are real.",
 ],
 "selfcheck": [
   "Write the ridge and lasso objectives and say what each produces.",
   "Explain geometrically why L1 gives sparsity.",
   "Why is lasso's feature selection unstable, and what fixes it?",
   "What must go inside the cross-validation fold, and why?",
   "What happens if feature selection is done outside the fold?",
   "State the three-way split and say what spending the test set means.",
   "Why does random search beat grid search?",
   "Why are most reported model differences not results?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Evaluation and Metrics",
 "subtitle": "Choosing the number you will be judged by.",
 "question": "What does 'the model is good' actually mean?",
 "outcomes": [
     "Read a confusion matrix and derive the metrics from it.",
     "Choose between precision, recall, F1, and the curves.",
     "Explain why ROC misleads under heavy imbalance.",
     "Measure and interpret calibration.",
     "Choose a metric from the costs of the errors.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The confusion matrix",
   "blurb": "Everything else is derived from four numbers."},

  {"t": "code", "kicker": "Definitions", "title": "Four cells, and what comes out of them",
   "lang": "text", "code": """
                     PREDICTED
                   positive  negative
    ACTUAL  pos  |    TP    |    FN    |   <- FN: the miss
            neg  |    FP    |    TN    |   <- FP: the false alarm

    precision = TP / (TP + FP)
        "of the things I flagged, how many were real?"
        -> the cost of a FALSE ALARM

    recall    = TP / (TP + FN)          (= sensitivity, TPR)
        "of the real things, how many did I find?"
        -> the cost of a MISS

    F1        = harmonic mean of the two
        -> only when the two costs are genuinely comparable

    specificity = TN / (TN + FP)
        "of the negatives, how many did I correctly pass?"

  ACCURACY = (TP + TN) / everything
    -> meaningless under imbalance. A model predicting "negative"
       always gets 99% accuracy on a 99%-negative dataset, and
       has recall of ZERO.
""",
   "caption": "<b>Precision and recall ask different questions and trade "
              "against each other</b> — the threshold moves you along "
              "the curve between them.",
   "note": "The 'which error costs what' framing is how to choose."},

  {"t": "callout", "title": "Accuracy is the wrong default",
   "kind": "The first thing to stop using",
   "body": ["<b>Accuracy weights every error equally and assumes balanced "
            "classes.</b> Both assumptions are usually false.",
            "<b>On a 99%-negative dataset, predicting 'negative' always "
            "scores 99%</b> — and a model doing that has learned "
            "nothing and found nothing.",
            "<b>Yet it is the default metric nearly everywhere</b>, and "
            "it is what gets reported in a summary.",
            "<b>So report the confusion matrix, not a scalar</b> — and "
            "if a scalar is required, choose it from the costs "
            "(Module 01 §3) rather than from convention."]},

  {"t": "section", "label": "Part 2", "title": "Curves",
   "blurb": "Performance across all thresholds."},

  {"t": "callout", "title": "ROC is optimistic under heavy imbalance; use PR",
   "kind": "The distinction that matters most here",
   "body": ["<b>ROC plots true positive rate against <i>false positive "
            "rate</i></b> — and FPR has the number of negatives in its "
            "denominator.",
            "<b>So when negatives vastly outnumber positives, a large "
            "absolute number of false positives is still a tiny FPR</b>, "
            "and the ROC curve looks excellent.",
            "<b>The precision–recall curve uses precision, whose "
            "denominator is the predictions you actually made</b> — so "
            "those same false positives dominate it, visibly.",
            "<b>At 1% positives, a model with an AUC of 0.95 can have "
            "precision near 10%.</b> <b>Report PR for imbalanced "
            "problems</b>, and ROC only when the classes are comparable."]},

  {"t": "table", "kicker": "Selection", "title": "Which metric, for which problem",
   "header": ["Situation", "Metric", "Why"],
   "widths": [3.2, 3.4, 5.5],
   "rows": [
     ["<b>Balanced, equal costs</b>", "Accuracy", "The one case it is honest"],
     ["<b>Rare positives</b>", "<b>PR curve, average precision</b>", "<b>ROC flatters; PR does not</b>"],
     ["<b>Misses are costly</b>", "<b>Recall at a precision floor</b>", "<b>Screening, safety, fraud</b>"],
     ["<b>False alarms are costly</b>", "Precision at a recall floor", "<b>Alerting; anything a human reviews</b>"],
     ["<b>Probabilities are used</b>", "<b>Log loss, Brier, calibration</b>", "<b>Discrimination is not enough</b>"],
     ["Ranking", "NDCG, MAP, MRR", "Order matters more than threshold"],
     ["<b>Regression</b>", "<b>MAE vs RMSE</b>", "<b>RMSE punishes outliers; MAE does not</b>"],
   ],
   "footnote": "<b>'X at a floor of Y' is usually the honest form</b> "
               "— it states the operating point rather than averaging "
               "over all of them.",
   "note": "Constrained metrics map to real deployments better than "
           "aggregate ones."},

  {"t": "section", "label": "Part 3", "title": "Calibration",
   "blurb": "Do the probabilities mean anything?"},

  {"t": "callout", "title": "Discrimination and calibration are different properties",
   "kind": "The distinction people miss",
   "body": ["<b>Discrimination: does the model rank positives above "
            "negatives?</b> AUC measures this.",
            "<b>Calibration: when it says 0.7, are 70% of those actually "
            "positive?</b> A reliability diagram measures this.",
            "<b>A model can discriminate perfectly and be badly "
            "calibrated</b> — monotonically transform every probability "
            "and the ranking is unchanged while the numbers become "
            "nonsense.",
            "<b>If any downstream decision uses the probability</b> — "
            "expected value, a cost threshold, combining with another "
            "model — <b>calibration is what you need and AUC does not "
            "measure it.</b>"]},

  {"t": "bullets", "kicker": "Calibration", "title": "Measuring and fixing it",
   "items": [
     "<b>Reliability diagram:</b> bin predictions, plot observed "
     "frequency against mean predicted probability. The diagonal is "
     "perfect.",
     "",
     "<b>Brier score and log loss</b> are proper scoring rules — they "
     "are minimised by the true probabilities, so they reward calibration "
     "and discrimination together.",
     "",
     "<b>Platt scaling</b> — fit a logistic regression on the scores, "
     "on held-out data.",
     "",
     "<b>Isotonic regression</b> — nonparametric, more flexible, needs "
     "more data.",
     "",
     "<b>And fit the calibrator on data the model did not train on</b>, "
     "or you have calibrated to the training set.",
   ],
   "footnote": "<b>Modern neural networks are badly calibrated and "
               "systematically overconfident</b>, which surprised the "
               "field when it was measured."},

  {"t": "section", "label": "Part 4", "title": "Imbalance",
   "blurb": "What to do, and what not to."},

  {"t": "table", "kicker": "Imbalance", "title": "Responses to class imbalance",
   "header": ["Approach", "Effect", "Caution"],
   "widths": [2.9, 4.2, 5.0],
   "rows": [
     ["<b>Move the threshold</b>", "<b>Trades precision for recall</b>", "<b>Free, reversible. Try this first</b>"],
     ["<b>Class weights</b>", "Reweights the loss", "<b>Usually enough; no data is invented</b>"],
     ["<b>Undersample majority</b>", "Balances; discards data", "<b>Throws away real information</b>"],
     ["<b>Oversample minority</b>", "<b>Duplicates; encourages memorising</b>", "<b>And breaks CV if done before splitting</b>"],
     ["<b>SMOTE</b>", "Synthesises interpolated minority points", "<b>Invents data; evidence is mixed</b>"],
     ["Collect more positives", "<b>The real fix</b>", "Usually expensive"],
   ],
   "footnote": "<b>Resampling must happen inside the cross-validation "
               "fold</b> (Module 04 §2) — oversampling before "
               "splitting puts copies of the same row in train and test.",
   "note": "The oversample-before-split error is extremely common and "
           "produces spectacular fake scores."},

  {"t": "callout", "title": "Threshold first, resampling last",
   "kind": "The practical ordering",
   "body": ["<b>A probabilistic model trained on imbalanced data is "
            "frequently fine</b> — it just needs a threshold other than "
            "0.5.",
            "<b>So move the threshold and look at the PR curve before "
            "touching the data.</b> It costs nothing and is reversible.",
            "<b>Then class weights, which reweight the loss without "
            "inventing or discarding anything.</b>",
            "<b>Resampling last, and inside the fold.</b> <b>A great deal "
            "of reported SMOTE improvement is leakage from resampling "
            "before splitting</b>, and the published evidence for it on "
            "properly-evaluated problems is genuinely mixed."]},
 ],
 "takeaways": [
   "Every classification metric is derived from four confusion matrix "
   "cells; precision asks the cost of a false alarm and recall the cost of "
   "a miss.",
   "Accuracy assumes balanced classes and equal costs, both usually false "
   "— a 99%-negative dataset gives 99% accuracy for predicting nothing.",
   "ROC's false positive rate is diluted by a large negative class, so "
   "under heavy imbalance it flatters; use the precision–recall curve.",
   "Discrimination and calibration are different: a model can rank "
   "perfectly and still have meaningless probabilities.",
   "Modern neural networks are systematically overconfident, which was "
   "discovered by measurement.",
   "For imbalance, move the threshold first, then class weights, and "
   "resample last — inside the fold.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The confusion matrix"),
  ("code", """                 PREDICTED
               positive  negative
ACTUAL  pos  |    TP    |    FN    |   <- FN: the MISS
        neg  |    FP    |    TN    |   <- FP: the FALSE ALARM

precision   = TP / (TP + FP)   "of what I flagged, how much was real?"
                               -> the cost of a FALSE ALARM
recall      = TP / (TP + FN)   "of what was real, how much did I find?"
                               -> the cost of a MISS
specificity = TN / (TN + FP)
F1          = harmonic mean of precision and recall

ACCURACY = (TP + TN) / everything
  -> meaningless under imbalance: predicting "negative" always
     scores 99% on a 99%-negative dataset, with recall of ZERO."""),
  ("callout", "Accuracy is the wrong default",
   ["<b>Accuracy weights every error equally and implicitly assumes "
    "balanced classes.</b> Both assumptions are false in most real "
    "problems, and neither is usually examined.",
    "<b>On a dataset that is 99% negative, a model that predicts "
    "'negative' unconditionally scores 99%</b> — and has found "
    "nothing, learned nothing, and is useless for the purpose it was built "
    "for. Its recall is exactly zero.",
    "<b>Yet accuracy remains the default metric nearly everywhere</b> "
    "— the library default, the first number in the notebook, and the "
    "one that reaches a summary slide where its denominator is invisible.",
    "<b>So report the confusion matrix rather than a scalar</b>, and when a "
    "scalar is genuinely required, <b>choose it from the costs of the two "
    "error types</b> (Module 01 &sect;3) rather than from convention. "
    "<b>Which metric you optimise is a statement about which error you are "
    "willing to make</b>, and making that statement explicitly is the "
    "point of this module."]),

  ("h1", "2 &nbsp; Curves"),
  ("callout", "ROC is optimistic under heavy imbalance; use PR",
   ["<b>The ROC curve plots the true positive rate against the <i>false "
    "positive</i> rate</b>, and FPR = FP / (FP + TN) — <b>its "
    "denominator is the total number of negatives.</b>",
    "<b>So when negatives vastly outnumber positives, even a large "
    "absolute number of false positives produces a tiny false positive "
    "rate</b>, and the ROC curve hugs the top-left corner while the model "
    "is, in practice, flagging mostly noise.",
    "<b>The precision–recall curve uses precision instead, whose "
    "denominator is the number of positive predictions you actually "
    "made</b> — so those same false positives dominate it and the "
    "curve shows the problem plainly.",
    "<b>At 1% positive prevalence, a model with an ROC AUC of 0.95 can "
    "easily have a precision around 10%</b> at a useful recall — nine "
    "false alarms for every real detection, which is the number the person "
    "reviewing the alerts experiences. <b>Report the PR curve for "
    "imbalanced problems</b>, and reserve ROC for when the classes are "
    "comparable in size."]),
  ("table", ["Situation", "Metric", "Why"],
   [["<b>Balanced classes, equal error costs</b>", "Accuracy.",
     "The one case in which it is honest."],
    ["<b>Rare positives</b>",
     "<b>Precision–recall curve; average precision.</b>",
     "<b>ROC flatters and PR does not</b> — see the callout."],
    ["<b>Misses are expensive</b>",
     "<b>Recall, reported at a stated precision floor.</b>",
     "<b>Medical screening, safety systems, fraud detection</b> — "
     "where a missed positive is the costly outcome."],
    ["<b>False alarms are expensive</b>",
     "Precision, at a stated recall floor.",
     "<b>Alerting, and anything a human must review</b> — alert "
     "fatigue is a real failure mode (CSCE 606 Module 11)."],
    ["<b>The probabilities are used downstream</b>",
     "<b>Log loss, Brier score, and a reliability diagram.</b>",
     "<b>Discrimination alone is not enough</b> — &sect;3."],
    ["<b>Ranking</b>", "NDCG, MAP, MRR.",
     "The order matters more than any threshold (CSCE 670 covers these)."],
    ["<b>Regression</b>", "<b>MAE against RMSE.</b>",
     "<b>RMSE punishes large errors disproportionately and MAE does "
     "not</b> — the same choice as Module 01 &sect;3's loss "
     "discussion, now at evaluation time."]],
   [0.26, 0.26, 0.48]),
  ("p", "<b>'X at a floor of Y' is usually the honest form of a "
        "metric</b> — 'recall of 0.82 at precision 0.90' states an "
        "operating point you could actually deploy, whereas an aggregate "
        "like AUC averages over thresholds including many you would never "
        "use."),

  ("break",),
  ("h1", "3 &nbsp; Calibration"),
  ("callout", "Discrimination and calibration are different properties",
   ["<b>Discrimination asks: does the model rank positives above "
    "negatives?</b> This is what AUC measures, and it is invariant to any "
    "monotonic transformation of the scores.",
    "<b>Calibration asks: when the model says 0.7, are about 70% of those "
    "cases actually positive?</b> This is what a reliability diagram "
    "measures.",
    "<b>A model can discriminate perfectly and be badly calibrated.</b> "
    "Take a perfectly calibrated model and square all its probabilities: "
    "the ranking is unchanged, so AUC is identical, and every probability "
    "is now wrong. <b>AUC cannot see this at all.</b>",
    "<b>And if any downstream decision uses the probability as a "
    "number</b> — an expected-value calculation, a cost-based "
    "threshold, combining with another model's output, or showing a "
    "confidence to a user — <b>calibration is the property you "
    "actually need, and the metric everyone reports does not measure "
    "it.</b>"]),
  ("ul", ["<b>Reliability diagram.</b> Bin the predictions by predicted "
          "probability, and plot the observed positive frequency in each "
          "bin against the mean predicted probability. <b>The diagonal is "
          "perfect calibration</b>; above it is underconfidence, below is "
          "overconfidence.",
          "<b>Brier score and log loss are <i>proper scoring rules</i></b> "
          "— they are minimised by reporting the true probabilities, "
          "so they reward calibration and discrimination together and "
          "cannot be gamed by distorting confidence.",
          "<b>Platt scaling:</b> fit a one-dimensional logistic regression "
          "mapping the model's scores to probabilities. Simple, needs "
          "little data, and assumes a sigmoid-shaped distortion.",
          "<b>Isotonic regression:</b> fit a monotonic step function "
          "instead. More flexible, makes no shape assumption, and needs "
          "considerably more data or it overfits.",
          "<b>And fit the calibrator on data the model did not train "
          "on</b>, or you have calibrated to the training set and learned "
          "nothing. This is Module 04 &sect;2's rule again — "
          "<b>calibration is a learned step and belongs inside the "
          "pipeline.</b> <b>Modern neural networks are badly calibrated "
          "and systematically overconfident</b>, which genuinely surprised "
          "the field when Guo and colleagues measured it, and older smaller "
          "networks were better."]),

  ("h1", "4 &nbsp; Class imbalance"),
  ("table", ["Approach", "Effect", "Caution"],
   [["<b>Move the decision threshold</b>",
     "<b>Trades precision against recall along the curve.</b>",
     "<b>Free, instant, and fully reversible. Try this first</b> — "
     "see the callout."],
    ["<b>Class weights in the loss</b>",
     "Reweights the contribution of each class.",
     "<b>Usually sufficient, and it invents nothing and discards "
     "nothing.</b>"],
    ["<b>Undersample the majority</b>", "Balances the classes.",
     "<b>Discards real information</b>, which is a strange thing to do "
     "when data is the scarce resource."],
    ["<b>Oversample the minority</b>",
     "<b>Duplicates minority rows, which encourages memorising them.</b>",
     "<b>And it breaks cross-validation if done before splitting</b> "
     "— copies of the same row land in both train and test."],
    ["<b>SMOTE and relatives</b>",
     "Synthesises new minority points by interpolating between neighbours.",
     "<b>Invents data that was never observed</b>, and <b>the published "
     "evidence on properly-evaluated problems is genuinely mixed</b> "
     "despite its popularity."],
    ["<b>Collect more positives</b>", "<b>The actual fix.</b>",
     "Usually expensive, and usually the right thing to ask for."]],
   [0.21, 0.36, 0.43]),
  ("callout", "Threshold first, resampling last",
   ["<b>A probabilistic model trained on imbalanced data is frequently "
    "perfectly fine.</b> It has learned the conditional probabilities; it "
    "simply needs a decision threshold other than the 0.5 that encodes "
    "equal costs and equal priors.",
    "<b>So move the threshold and examine the precision–recall curve "
    "before touching the data at all.</b> It costs one line, it is "
    "reversible, and it frequently resolves the problem entirely.",
    "<b>Then class weights</b>, which reweight the loss function so that "
    "minority errors count more — without inventing any data or "
    "discarding any.",
    "<b>Resampling last, and strictly inside the cross-validation "
    "fold.</b> <b>A substantial portion of reported SMOTE improvement is "
    "leakage from resampling before splitting</b> (Module 04 &sect;2): "
    "synthetic points interpolated from a row that then lands in the test "
    "set produce spectacular and entirely fictitious scores. <b>When the "
    "evaluation is done correctly, the gains largely evaporate</b>, which "
    "is a result worth knowing before adopting the technique."]),
 ],
 "resources": [
   ("Saito & Rehmsmeier &mdash; The Precision-Recall Plot Is More "
    "Informative than the ROC Plot (free)",
    "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0118432",
    "<b>The &sect;2 argument</b>, with worked examples at several "
    "prevalences. Short and conclusive."),
   ("Guo, Pleiss, Sun & Weinberger &mdash; On Calibration of Modern Neural "
    "Networks (free)",
    "https://arxiv.org/abs/1706.04599",
    "<b>The &sect;3 result.</b> Modern networks are far less calibrated "
    "than older ones, measured and explained."),
   ("scikit-learn &mdash; metrics and probability calibration guides "
    "(free)",
    "https://scikit-learn.org/stable/modules/model_evaluation.html",
    "The implementations, with unusually good discussion of when each "
    "metric is appropriate."),
   ("Blagec et al.; and the <code>imbalanced-learn</code> documentation "
    "(free)",
    "https://imbalanced-learn.org/stable/common_pitfalls.html",
    "<b>The &sect;4 resampling pitfalls</b>, including the "
    "resample-before-split error, documented by the library that "
    "implements the methods."),
 ],
 "exercises": [
   "Build a confusion matrix for your project model and derive all five "
   "metrics from it by hand.",
   "<b>Build the 99%-negative demonstration:</b> report accuracy, "
   "precision, recall, and F1 for a model that always predicts negative.",
   "Plot the ROC and PR curves for the same model at 50%, 10%, and 1% "
   "prevalence. <b>Report how differently they look.</b>",
   "Compute AUC and average precision at each prevalence and explain the "
   "divergence.",
   "<b>Plot a reliability diagram</b> for a logistic regression, a random "
   "forest, and a boosted model on the same data.",
   "<b>Square every predicted probability</b> and show AUC is unchanged "
   "while calibration is destroyed.",
   "Apply Platt scaling and isotonic regression and compare the "
   "reliability diagrams.",
   "<b>Tune the threshold</b> on an imbalanced problem and report the "
   "precision–recall trade at several points.",
   "<b>Oversample before splitting and after</b>, and report both scores. "
   "Explain the gap.",
   "Choose your project's reporting metric and write one paragraph "
   "justifying it from the error costs.",
 ],
 "selfcheck": [
   "Define precision, recall, specificity, and F1 from the confusion "
   "matrix.",
   "Why is accuracy the wrong default?",
   "Why does ROC flatter under heavy imbalance?",
   "Give seven situations and the right metric for each.",
   "Distinguish discrimination from calibration and give an example of "
   "high one and low the other.",
   "Name two calibration methods and say where the calibrator must be "
   "fitted.",
   "Give six responses to imbalance and the right ordering.",
   "Why does resampling before splitting produce fake scores?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Trees and Ensembles",
 "subtitle": "What actually wins on tabular data.",
 "question": "Why do gradient-boosted trees beat neural networks on "
             "spreadsheets?",
 "outcomes": [
     "Explain how a decision tree is grown and why it overfits.",
     "Explain bagging and what it reduces.",
     "Explain boosting and what it reduces.",
     "Contrast random forests with gradient boosting.",
     "Interpret feature importance correctly, including its traps.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "A single tree",
   "blurb": "Greedy splitting, and why it alone is not enough."},

  {"t": "callout", "title": "Trees split greedily on the best single question",
   "kind": "How one is grown",
   "body": ["<b>At each node, try every feature and every threshold, and "
            "take the split that most reduces impurity</b> — Gini or "
            "entropy for classification, variance for regression.",
            "<b>Recurse on each side until a stopping rule fires</b> "
            "— minimum samples, maximum depth, or no split improves "
            "anything.",
            "<b>A fully grown tree fits the training data exactly</b> and "
            "generalises badly. Pure high variance (Module 03).",
            "<b>And it is unstable:</b> changing one training point can "
            "change an early split and therefore the entire tree below it. "
            "<b>That instability is exactly what makes averaging work.</b>"]},

  {"t": "table", "kicker": "Properties", "title": "What trees are good and bad at",
   "header": ["Good at", "Bad at"],
   "widths": [6.0, 6.1],
   "rows": [
     ["<b>Mixed numeric and categorical features</b>", "<b>Smooth or linear relationships — approximated by steps</b>"],
     ["<b>No scaling required at all</b>", "<b>Extrapolating outside the training range</b>"],
     ["<b>Missing values, handled natively</b>", "High variance alone"],
     ["<b>Interactions, found automatically</b>", "<b>Diagonal boundaries — axis-aligned splits only</b>"],
     ["Monotonic transforms of features are irrelevant", "<b>Very wide data; many irrelevant features</b>"],
   ],
   "footnote": "<b>No scaling, native missing values, and automatic "
               "interactions</b> are why trees need so much less "
               "preprocessing than anything else.",
   "note": "The preprocessing advantage is underrated and explains a lot "
           "of their practical dominance."},

  {"t": "section", "label": "Part 2", "title": "Bagging",
   "blurb": "Averaging away the variance."},

  {"t": "callout", "title": "Bagging reduces variance and leaves bias alone",
   "kind": "The mechanism",
   "body": ["<b>Train many trees on bootstrap samples and average their "
            "predictions.</b> Averaging n independent estimates divides "
            "the variance by n.",
            "<b>But the trees are not independent</b> — they see "
            "overlapping data and will use the same strong features.",
            "<b>So random forests also sample the <i>features</i> at each "
            "split</b>, which decorrelates the trees and is the key "
            "addition over plain bagging.",
            "<b>And out-of-bag samples give a free validation "
            "estimate</b> — each tree omits about a third of the data, "
            "so every point can be scored by the trees that did not see "
            "it."]},

  {"t": "section", "label": "Part 3", "title": "Boosting",
   "blurb": "Fitting the errors."},

  {"t": "code", "kicker": "Boosting", "title": "Gradient boosting, and its difference from bagging",
   "lang": "text", "code": """
  BAGGING: many deep trees, in PARALLEL, averaged.
      each tree is a full model; averaging cancels their variance

  BOOSTING: many SHALLOW trees, in SEQUENCE, summed.
      F_0 = a constant (the mean)
      for m = 1 .. M:
          r = negative gradient of the loss at F_{m-1}
              (for squared loss this is just the residual)
          fit a shallow tree h_m to r
          F_m = F_{m-1} + eta * h_m        <- eta is the LEARNING RATE

      Each tree corrects what the ensemble so far got wrong.
      Summing weak learners REDUCES BIAS.
      Bagging averages strong learners and REDUCES VARIANCE.

  THE THREE KNOBS, which interact:
      n_estimators   more trees -> lower bias, eventual overfit
      learning_rate  smaller -> needs more trees, generalises better
      max_depth      3-8 typically. Deep trees in boosting overfit fast

  Lower the learning rate and raise the tree count together.
  This is the single most reliable tuning move available.
""",
   "caption": "<b>Bagging reduces variance; boosting reduces bias.</b> "
              "They are not two flavours of the same idea.",
   "note": "That contrast is the thing to carry away from the module."},

  {"t": "callout", "title": "Why gradient-boosted trees win on tabular data",
   "kind": "The empirical result, with reasons",
   "body": ["<b>Tabular features are heterogeneous</b> — different "
            "units, different scales, mixed types. Trees handle that "
            "natively; networks need it engineered away.",
            "<b>Relationships are often piecewise and non-smooth</b> "
            "— thresholds, categories, step changes. Trees represent "
            "those exactly; smooth function approximators do not.",
            "<b>Datasets are small by deep learning standards</b>, and "
            "boosting is extremely sample-efficient.",
            "<b>And there is no useful inductive bias to exploit.</b> "
            "Convolution assumes spatial locality and attention assumes "
            "sequence structure; <b>a spreadsheet has neither</b>, so the "
            "architectural advantage disappears."]},

  {"t": "section", "label": "Part 4", "title": "Feature importance",
   "blurb": "The number everyone reports and few interpret correctly."},

  {"t": "table", "kicker": "Importance", "title": "Three ways to measure it, and what each is wrong about",
   "header": ["Method", "What it measures", "The trap"],
   "widths": [2.7, 4.3, 5.1],
   "rows": [
     ["<b>Impurity (Gini)</b>", "<b>Total impurity reduction from splits</b>", "<b>Biased toward high-cardinality features</b>"],
     ["<b>Permutation</b>", "<b>Drop in score when a feature is shuffled</b>", "<b>Correlated features share credit, so both look weak</b>"],
     ["<b>SHAP</b>", "Per-prediction contribution, additively fair", "<b>Expensive; still correlation, not cause</b>"],
   ],
   "footnote": "<b>None of these is causal.</b> A feature can be important "
               "to the model and have no causal relationship to the "
               "outcome.",
   "note": "The high-cardinality bias in Gini importance is a real and "
           "widely-unknown problem."},

  {"t": "callout", "title": "Importance is about the model, not the world",
   "kind": "The interpretation that matters",
   "body": ["<b>Feature importance says what the model used.</b> It does "
            "not say what causes the outcome.",
            "<b>A proxy will look important.</b> If postcode predicts "
            "income and income causes the outcome, postcode scores highly "
            "— and intervening on postcode does nothing.",
            "<b>And correlated features split the credit</b>, so two "
            "features carrying the same signal both look half as important "
            "as either really is.",
            "<b>So importance is a debugging tool, not a finding.</b> "
            "<b>Use it to spot leakage</b> — an implausibly dominant "
            "feature is usually leakage (Module 12) — <b>and not to "
            "make claims about the world.</b>"]},
 ],
 "takeaways": [
   "A tree splits greedily on the best single question, fits the training "
   "data exactly, and is unstable — and that instability is what makes "
   "averaging work.",
   "Trees need no scaling, handle missing values natively, and find "
   "interactions automatically, which is most of their practical advantage.",
   "Bagging averages strong learners to reduce variance; random forests add "
   "feature subsampling to decorrelate them.",
   "Boosting sums shallow learners in sequence to reduce bias — it is "
   "not a variant of bagging but the opposite mechanism.",
   "Lowering the learning rate while raising the tree count is the single "
   "most reliable boosting tuning move.",
   "Feature importance describes the model, not the world; a proxy looks "
   "important and correlated features split the credit.",
 ],
 "notes": [
  ("h1", "1 &nbsp; A single tree"),
  ("callout", "Trees split greedily on the best single question",
   ["<b>At each node, consider every feature and every candidate "
    "threshold, and choose the split that most reduces impurity</b> "
    "— Gini or entropy for classification, variance for regression. "
    "The search is exhaustive over splits and greedy over depth.",
    "<b>Then recurse on each side until a stopping rule fires:</b> minimum "
    "samples per leaf, maximum depth, minimum impurity decrease, or no "
    "split improving anything.",
    "<b>A fully grown tree fits the training data exactly</b> — every "
    "leaf can be made pure — <b>and generalises badly.</b> It is the "
    "textbook high-variance model of Module 03 &sect;1.",
    "<b>And it is unstable.</b> Changing a single training point can change "
    "an early split, which changes every subtree beneath it, producing a "
    "completely different tree that performs about as well. <b>That "
    "instability looks like a flaw and is exactly what makes averaging "
    "effective</b> (&sect;2) — averaging helps most when the "
    "individual models' errors are uncorrelated, and unstable models "
    "trained on resampled data produce exactly that."]),
  ("table", ["Trees are good at", "Trees are bad at"],
   [["<b>Mixed numeric and categorical features</b> in one model, with no "
     "encoding required.",
     "<b>Smooth or linear relationships</b>, which must be approximated by "
     "a staircase of splits — inefficiently."],
    ["<b>Requiring no feature scaling whatsoever.</b> Splits are invariant "
     "to any monotonic transformation.",
     "<b>Extrapolating beyond the training range.</b> A tree's prediction "
     "is constant outside the data it saw, which is sometimes safe and "
     "sometimes badly wrong."],
    ["<b>Missing values, handled natively</b> by surrogate splits or by "
     "learning a default direction.",
     "High variance when used alone (&sect;1)."],
    ["<b>Finding interactions automatically</b> — a split below "
     "another split <i>is</i> an interaction, discovered rather than "
     "specified.",
     "<b>Diagonal decision boundaries.</b> Axis-aligned splits approximate "
     "a diagonal with a staircase, which costs depth and samples."],
    ["Being invariant to monotonic transforms of any feature.",
     "<b>Very wide data with many irrelevant features</b>, where the greedy "
     "search finds spurious splits."]],
   [0.5, 0.5]),
  ("p", "<b>No scaling, native missing-value handling, and automatic "
        "interaction discovery</b> together mean a tree ensemble needs "
        "dramatically less preprocessing than any other model family "
        "— which is a substantial and underrated part of why they "
        "dominate practical tabular work (&sect;3)."),

  ("h1", "2 &nbsp; Bagging and random forests"),
  ("callout", "Bagging reduces variance and leaves bias alone",
   ["<b>Train many trees on bootstrap samples of the data and average "
    "their predictions.</b> Averaging n independent estimates of the same "
    "quantity divides the variance by n while leaving the bias unchanged "
    "— which is exactly the right medicine for a high-variance, "
    "low-bias model.",
    "<b>But the trees are not independent.</b> They see heavily "
    "overlapping bootstrap samples, and more importantly they will all "
    "discover and use the same few strong features, so their errors "
    "correlate and the variance reduction falls short of 1/n.",
    "<b>So a random forest also samples the <i>features</i> considered at "
    "each split</b> — typically &radic;d of them for classification. "
    "<b>This is the key addition over plain bagging</b>: it forces "
    "different trees to use different features, decorrelating them and "
    "recovering much of the lost variance reduction.",
    "<b>And the out-of-bag samples provide a free validation "
    "estimate.</b> Each bootstrap sample omits about a third of the data, "
    "so every training point can be scored by the subset of trees that did "
    "not see it — giving a cross-validation-like estimate at no extra "
    "training cost, which is a genuinely elegant property."]),

  ("break",),
  ("h1", "3 &nbsp; Boosting"),
  ("code", """BAGGING   many DEEP trees, in PARALLEL, AVERAGED
          each is a full model; averaging cancels variance

BOOSTING  many SHALLOW trees, in SEQUENCE, SUMMED
    F_0 = constant (the mean)
    for m = 1..M:
        r = negative gradient of the loss at F_{m-1}
            (for squared loss, just the residual)
        fit a shallow tree h_m to r
        F_m = F_{m-1} + eta * h_m          <- eta = learning rate

    Each tree corrects what the ensemble so far got wrong.
    Summing weak learners REDUCES BIAS.
    Averaging strong learners REDUCES VARIANCE.

THREE KNOBS, which interact:
    n_estimators   more -> lower bias, eventually overfits
    learning_rate  smaller -> needs more trees, generalises better
    max_depth      3-8; deep trees in boosting overfit quickly

Lower the learning rate and raise the tree count TOGETHER."""),
  ("p", "<b>Bagging reduces variance; boosting reduces bias.</b> They are "
        "not two flavours of one idea but opposite responses to the two "
        "terms of Module 03's decomposition, and the model each starts from "
        "reflects that: bagging begins with a model that is too flexible "
        "and calms it down, boosting begins with models that are far too "
        "simple and accumulates them."),
  ("callout", "Why gradient-boosted trees win on tabular data",
   ["<b>Tabular features are heterogeneous</b> — different units, "
    "wildly different scales, a mixture of continuous, ordinal, and "
    "categorical types, with no meaningful notion of distance between rows. "
    "<b>Trees handle all of that natively; neural networks require it to "
    "be engineered away first.</b>",
    "<b>Relationships in tabular data are frequently piecewise and "
    "non-smooth</b> — thresholds, eligibility cut-offs, category "
    "effects, step changes at round numbers. <b>Trees represent a step "
    "exactly with one split</b>; a smooth function approximator spends "
    "capacity approximating it.",
    "<b>And the datasets are small by deep learning standards.</b> A few "
    "thousand to a few million rows, where boosting is extremely "
    "sample-efficient and networks are still in their data-hungry regime.",
    "<b>Most fundamentally, there is no useful inductive bias to "
    "exploit.</b> Convolution wins on images because it assumes spatial "
    "locality and translation invariance, both of which are true of images; "
    "attention wins on text because it assumes sequence structure. <b>A "
    "spreadsheet has neither property</b>, and column order is arbitrary "
    "— so the architectural advantage that makes deep learning "
    "dominant elsewhere simply does not apply. <b>This has been confirmed "
    "repeatedly in benchmark studies</b>, and it is the clearest available "
    "demonstration that architecture is about matching structure in the "
    "data rather than about capacity."]),

  ("h1", "4 &nbsp; Feature importance"),
  ("table", ["Method", "What it measures", "The trap"],
   [["<b>Impurity (Gini) importance</b>",
     "<b>Total impurity reduction attributable to splits on that "
     "feature.</b> The default, and nearly free.",
     "<b>Systematically biased toward high-cardinality features</b> "
     "— a continuous feature or an ID-like column offers many "
     "candidate splits and will score highly even when random. <b>Widely "
     "unknown and genuinely misleading.</b>"],
    ["<b>Permutation importance</b>",
     "<b>The drop in validation score when that feature's values are "
     "shuffled.</b> Measured on held-out data, so it reflects "
     "generalisation.",
     "<b>Correlated features share the credit and both look weak</b> "
     "— shuffling one leaves the other to carry the signal, so "
     "neither appears necessary."],
    ["<b>SHAP values</b>",
     "A per-prediction, additively fair attribution derived from "
     "cooperative game theory.",
     "<b>Expensive to compute</b>, and <b>still a statement about "
     "correlation within the model, not about causation</b> — which "
     "the presentation of SHAP plots tends to obscure."]],
   [0.22, 0.38, 0.40]),
  ("callout", "Importance is about the model, not the world",
   ["<b>Feature importance reports what the model used.</b> It does not "
    "report what causes the outcome, and the two are routinely conflated in "
    "exactly the settings where the distinction matters most.",
    "<b>A proxy will look important.</b> If postcode predicts income and "
    "income affects the outcome, postcode will score highly — and "
    "changing someone's postcode would do nothing. <b>The model is right "
    "about the correlation and the causal reading is wrong.</b>",
    "<b>And correlated features split the credit</b>, so two features "
    "carrying the same underlying signal each appear about half as "
    "important as that signal really is — which can make a genuinely "
    "important quantity look unimportant twice over.",
    "<b>So treat importance as a debugging tool rather than a finding.</b> "
    "<b>Its highest-value use is spotting leakage</b> (Module 12 "
    "&sect;1): <b>an implausibly dominant single feature is leakage far "
    "more often than it is a discovery</b>, and checking the top of the "
    "importance list is the cheapest leakage audit available. <b>Do not "
    "use it to make claims about the world</b> — that requires a "
    "causal design, which is a different subject."]),
 ],
 "resources": [
   ("Hastie et al. &mdash; The Elements of Statistical Learning, chapters "
    "9, 10 and 15 (free PDF)",
    "https://hastie.su.domains/ElemStatLearn/",
    "Trees, boosting, and random forests, with the bias-versus-variance "
    "framing of &sect;2 and &sect;3 made precise."),
   ("Friedman &mdash; Greedy Function Approximation: A Gradient Boosting "
    "Machine (free)",
    "https://projecteuclid.org/journals/annals-of-statistics/volume-29/issue-5/Greedy-function-approximation-A-gradient-boostingmachine/10.1214/aos/1013203451.full",
    "<b>The &sect;3 algorithm, from its author.</b> The gradient framing "
    "is what makes it general."),
   ("Grinsztajn, Oyallon & Varoquaux &mdash; Why do tree-based models "
    "still outperform deep learning on tabular data? (free)",
    "https://arxiv.org/abs/2207.08815",
    "<b>The &sect;3 callout, measured carefully</b> across many datasets, "
    "with the reasons isolated experimentally."),
   ("Strobl et al. &mdash; Bias in random forest variable importance "
    "measures (free)",
    "https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-8-25",
    "<b>The high-cardinality bias of &sect;4</b>, demonstrated. Read "
    "before reporting a Gini importance ranking."),
 ],
 "exercises": [
   "Implement a decision tree with Gini splitting from scratch.",
   "<b>Demonstrate instability:</b> change one training point and show the "
   "tree structure changes substantially.",
   "<b>Fit a tree to a diagonal boundary</b> and visualise the staircase. "
   "Measure how depth affects the approximation.",
   "Implement bagging and plot test error against the number of trees.",
   "<b>Add feature subsampling</b> and show the extra variance reduction.",
   "Compute out-of-bag error and compare it against a held-out estimate.",
   "Implement gradient boosting for squared loss from scratch.",
   "<b>Sweep learning rate against tree count</b> and plot the surface. "
   "Confirm the trade.",
   "<b>Compare boosted trees against a neural network</b> on a tabular "
   "dataset, at equal tuning effort.",
   "<b>Add a random high-cardinality ID column</b> and show it ranks "
   "highly in Gini importance and not in permutation importance.",
 ],
 "selfcheck": [
   "How is a tree grown, and why is it unstable?",
   "Give five things trees are good at and five they are bad at.",
   "What does bagging reduce, and what does feature subsampling add?",
   "What is out-of-bag error and why is it free?",
   "What does boosting reduce, and how does it differ from bagging?",
   "Name the three boosting knobs and the reliable tuning move.",
   "Give four reasons boosted trees win on tabular data.",
   "Compare three importance methods and the trap in each.",
   "Why is importance not causal, and what is it good for?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Kernels and Margins",
 "subtitle": "Infinite features without computing any of them.",
 "question": "How do you fit a nonlinear model with a linear method?",
 "outcomes": [
     "Explain the maximum margin principle.",
     "Explain the kernel trick and the representer theorem.",
     "Choose a kernel and explain its hyperparameters.",
     "Explain why SVMs lost ground and where they still fit.",
     "Connect kernels to the other methods in the course.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The margin",
   "blurb": "Of all separating lines, which one?"},

  {"t": "callout", "title": "Maximise the distance to the nearest point",
   "kind": "The principle",
   "body": ["<b>If the data is linearly separable, infinitely many lines "
            "separate it.</b> Logistic regression picks one by likelihood; "
            "the SVM picks one by geometry.",
            "<b>Choose the line maximising the distance to the nearest "
            "training point on either side</b> — the margin.",
            "<b>The intuition: a wide margin is a confident "
            "decision</b>, and leaves the most room for a new point to "
            "fall on the right side.",
            "<b>Only the closest points matter.</b> Those are the "
            "<i>support vectors</i>, and moving any other point changes "
            "nothing — which is both the method's name and its most "
            "distinctive property."]},

  {"t": "eq", "kicker": "Soft margin", "title": "Allowing violations",
   "eqs": [
     ("min  ½‖w‖² + C Σ ξᵢ",
      "Maximise the margin while penalising violations ξᵢ."),
     ("subject to  yᵢ(wᵀxᵢ + b) ≥ 1 − ξᵢ",
      "Each point should be on the right side by at least 1, or pay for "
      "the shortfall."),
     ("C large ⟹ few violations, narrow margin; C small ⟹ wide "
      "margin, more violations",
      "C is the regularisation dial, and it is the inverse of λ."),
   ],
   "caption": "<b>Real data is not separable</b>, so the hard margin is "
              "replaced by a penalty — and that penalty is "
              "Module 04's regularisation in a different costume.",
   "note": "Worth connecting C to lambda explicitly; students treat them "
           "as unrelated."},

  {"t": "section", "label": "Part 2", "title": "The kernel trick",
   "blurb": "The idea that made SVMs famous."},

  {"t": "code", "kicker": "The trick", "title": "Inner products are all you need",
   "lang": "text", "code": """
  THE OBSERVATION
      The SVM's solution depends on the data ONLY through inner
      products x_i . x_j -- never through individual x_i alone.

  SO: to fit in a richer feature space phi(x), you only need
      phi(x_i) . phi(x_j)
  and NOT phi(x) itself.

  A KERNEL is a function computing that inner product directly:
      K(x, z) = phi(x) . phi(z)

  POLYNOMIAL   K = (x.z + 1)^d
      phi expands to all monomials up to degree d.
      For d=5 and 100 features that is ~96 million terms.
      K costs ONE dot product and ONE power.

  RBF / GAUSSIAN  K = exp(-gamma ||x - z||^2)
      phi is INFINITE-DIMENSIONAL. You can never write it down.
      K is three operations.

  You are fitting a linear model in a space you never construct.
  That is the trick, and it is genuinely remarkable.
""",
   "caption": "<b>An infinite-dimensional feature space, at the cost of a "
              "distance and an exponential.</b>",
   "note": "The 96-million-terms figure makes the saving concrete."},

  {"t": "callout", "title": "The representer theorem is why this is legitimate",
   "kind": "The result underneath",
   "body": ["<b>For a broad class of regularised problems, the optimal "
            "solution is a weighted sum of kernel evaluations at the "
            "training points.</b>",
            "<b>So the solution lives in a space of dimension n — the "
            "number of training points — regardless of how "
            "high-dimensional the feature space is.</b>",
            "<b>Infinite features, n parameters.</b> That is why an "
            "infinite-dimensional model does not automatically overfit: "
            "the regularisation and the sample size bound it.",
            "<b>And it is why the cost scales with n, not d</b> — which "
            "is the method's strength on wide data and its fatal weakness "
            "on large data (Part 3)."]},

  {"t": "table", "kicker": "Kernels", "title": "The kernels worth knowing",
   "header": ["Kernel", "Form", "Character"],
   "widths": [2.5, 4.0, 5.6],
   "rows": [
     ["<b>Linear</b>", "x·z", "<b>Just a linear model. Try first</b>"],
     ["<b>RBF / Gaussian</b>", "<b>exp(−γ‖x−z‖&#178;)</b>", "<b>The default. γ sets locality</b>"],
     ["<b>Polynomial</b>", "(x·z + 1)^d", "<b>Explicit interactions; numerically awkward</b>"],
     ["Sigmoid", "tanh(κx·z + c)", "<b>Not always a valid kernel. Rarely used</b>"],
     ["<b>String, graph, custom</b>", "Domain-specific", "<b>Where kernels still genuinely shine</b>"],
   ],
   "footnote": "<b>γ and C must be tuned together</b> — they "
               "interact strongly, and a grid over both is one of the few "
               "places grid search is defensible.",
   "note": "The custom-kernel row is where SVMs remain genuinely "
           "competitive."},

  {"t": "section", "label": "Part 3", "title": "Where SVMs stand now",
   "blurb": "Honestly."},

  {"t": "callout", "title": "Why SVMs lost ground",
   "kind": "The honest assessment",
   "body": ["<b>Training is roughly O(n&#178;) to O(n&#179;)</b>, and "
            "prediction costs a kernel evaluation per support vector. "
            "<b>Past ~100,000 samples this is impractical.</b>",
            "<b>Boosted trees usually match or beat them on tabular "
            "data</b> (Module 06) with far less tuning and no scaling "
            "requirement.",
            "<b>And neural networks took the structured domains</b> "
            "— images, audio, text — where kernels were briefly "
            "competitive.",
            "<b>They remain excellent on small, wide, clean data</b> "
            "— a few thousand samples and many features, which describes "
            "a lot of bioinformatics — <b>and wherever a custom kernel "
            "encodes real domain structure.</b>"]},

  {"t": "callout", "title": "What kernels taught the rest of the field",
   "kind": "Why this module is still here",
   "body": ["<b>The margin idea became a loss function.</b> Hinge loss "
            "appears throughout deep learning.",
            "<b>The representer theorem explains why n-sample methods "
            "work</b> in high-dimensional spaces at all, which is a "
            "question deep learning still wrestles with.",
            "<b>'Make it linear in a transformed space' is the whole "
            "strategy of representation learning</b> — a deep network's "
            "final layer is a linear classifier on learned features "
            "(CSCE 636 M05).",
            "<b>So the difference is where the features come from:</b> "
            "<b>a kernel specifies them in advance; a network learns "
            "them.</b> That sentence is most of the history of the "
            "field."]},
 ],
 "takeaways": [
   "The SVM picks the separating boundary that maximises distance to the "
   "nearest point, and only those nearest points — the support vectors "
   "— affect the solution.",
   "The soft-margin penalty C is Module 04's regularisation dial in "
   "different notation, and it is the inverse of λ.",
   "The solution depends on data only through inner products, so a kernel "
   "can supply them for a feature space that is never constructed.",
   "The representer theorem puts the solution in an n-dimensional space "
   "regardless of feature dimension — infinite features, n parameters.",
   "That makes cost scale with sample count rather than feature count, "
   "which is the method's strength on wide data and its downfall on large "
   "data.",
   "A kernel specifies features in advance and a network learns them — "
   "which is most of the history of the field in one sentence.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The margin"),
  ("callout", "Maximise the distance to the nearest point",
   ["<b>If the data is linearly separable, infinitely many hyperplanes "
    "separate it</b>, and they are not equally good. Logistic regression "
    "selects one by maximising likelihood; the SVM selects one by a purely "
    "geometric criterion.",
    "<b>Choose the hyperplane that maximises the distance to the nearest "
    "training point on either side</b> — the margin. This is a "
    "well-posed optimisation with a unique solution.",
    "<b>The intuition is that a wide margin is a confident decision</b>, "
    "and leaves the greatest room for a new point drawn from the same "
    "distribution to fall on the correct side. There are generalisation "
    "bounds that formalise this, and they are loose, but the intuition "
    "survives.",
    "<b>Only the closest points affect the solution.</b> These are the "
    "<i>support vectors</i>, and <b>moving or deleting any other training "
    "point changes nothing at all</b> — which gives the method its "
    "name, makes the model compact (prediction needs only the support "
    "vectors), and is its most distinctive property. It also means the "
    "fit is robust to most of the data and exquisitely sensitive to a few "
    "points, which cuts both ways."]),
  ("eq", "min &nbsp; &frac12;&#8214;w&#8214;&#178; + C &Sigma; "
         "&xi;<sub>i</sub> &nbsp;&nbsp; s.t. &nbsp; "
         "y<sub>i</sub>(w<super>T</super>x<sub>i</sub> + b) &ge; 1 &minus; "
         "&xi;<sub>i</sub>"),
  ("p", "Real data is not separable, so the hard margin is replaced by a "
        "<i>soft</i> one: each point should be on the correct side by a "
        "margin of at least 1, and a slack variable &xi; pays for the "
        "shortfall. <b>Large C means violations are expensive, so the "
        "margin is narrow and the fit tight; small C means a wide margin "
        "and more violations tolerated.</b> <b>C is Module 04's "
        "regularisation dial in different notation — it is the inverse "
        "of &lambda;</b>, and noticing that the two are the same knob "
        "prevents treating SVM tuning as a separate skill."),

  ("h1", "2 &nbsp; The kernel trick"),
  ("code", """THE OBSERVATION
  the SVM's solution depends on the data ONLY through inner
  products  x_i . x_j  -- never through any x_i alone.

SO to fit in a richer feature space phi(x), you need only
  phi(x_i) . phi(x_j)    and NOT phi(x) itself.

A KERNEL computes that inner product directly:
  K(x, z) = phi(x) . phi(z)

POLYNOMIAL   K = (x.z + 1)^d
  phi expands to all monomials up to degree d.
  d=5 with 100 features is ~96 MILLION terms.
  K costs one dot product and one power.

RBF / GAUSSIAN   K = exp(-gamma ||x - z||^2)
  phi is INFINITE-dimensional -- it cannot be written down.
  K is three operations.

You fit a linear model in a space you never construct."""),
  ("callout", "The representer theorem is why this is legitimate",
   ["<b>For a broad class of regularised problems, the optimal solution can "
    "be written as a weighted sum of kernel evaluations at the training "
    "points</b> — f(x) = &Sigma; &alpha;<sub>i</sub> K(x<sub>i</sub>, "
    "x). This is a theorem, not a convenient restriction.",
    "<b>So the solution lives in a space whose dimension is n, the number "
    "of training points, regardless of how high-dimensional the feature "
    "space &phi; maps into.</b>",
    "<b>Infinite features, n parameters.</b> This is why an "
    "infinite-dimensional model does not automatically overfit: the "
    "effective capacity is bounded by the sample size and the "
    "regularisation, not by the nominal dimension — which is the "
    "same distinction Module 03 &sect;3 drew between parameter count and "
    "effective capacity.",
    "<b>And it is why the computational cost scales with n rather than "
    "with the feature dimension.</b> <b>That is the method's great "
    "strength on wide data</b> — ten thousand features cost nothing "
    "extra — <b>and its fatal weakness on large data</b>, since the "
    "kernel matrix alone is n&times;n (&sect;3)."]),
  ("table", ["Kernel", "Form", "Character"],
   [["<b>Linear</b>", "x&middot;z",
     "<b>An ordinary linear model.</b> Try it first — on wide data it "
     "frequently wins, and it is far faster."],
    ["<b>RBF (Gaussian)</b>",
     "<b>exp(&minus;&gamma;&#8214;x&minus;z&#8214;&#178;)</b>",
     "<b>The default.</b> &gamma; sets how local the influence of each "
     "point is: large &gamma; means a narrow bump and a wiggly boundary "
     "(high variance), small &gamma; approaches linear."],
    ["<b>Polynomial</b>", "(x&middot;z + 1)<super>d</super>",
     "<b>Explicit interactions up to degree d.</b> Numerically awkward "
     "— large d produces very large or very small values and the "
     "optimisation suffers."],
    ["<b>Sigmoid</b>", "tanh(&kappa; x&middot;z + c)",
     "<b>Not positive semidefinite for all parameters</b>, so it is not "
     "always a valid kernel. Rarely used, and historically motivated by an "
     "analogy to neural networks."],
    ["<b>String, graph, and custom kernels</b>",
     "Domain-specific similarity measures.",
     "<b>Where kernel methods still genuinely shine</b> — you can "
     "define a similarity between objects that have no natural vector "
     "representation at all, which is a capability nothing else offers so "
     "directly."]],
   [0.18, 0.28, 0.54]),
  ("p", "<b>&gamma; and C must be tuned together</b> — they interact "
        "strongly, since both control effective capacity by different "
        "routes, and tuning one at a time finds a poor optimum. <b>This is "
        "one of the few places where a grid over two parameters is "
        "genuinely defensible</b> (Module 04 &sect;3), because the "
        "interaction is exactly what you need to see."),

  ("break",),
  ("h1", "3 &nbsp; Where SVMs stand now"),
  ("callout", "Why SVMs lost ground",
   ["<b>Training is roughly O(n&#178;) to O(n&#179;)</b> — the kernel "
    "matrix alone has n&#178; entries — <b>and prediction requires a "
    "kernel evaluation against every support vector</b>, of which there may "
    "be thousands. <b>Past roughly 100,000 samples this is "
    "impractical</b>, and approximations (Nystr&ouml;m, random features) "
    "give up much of the advantage.",
    "<b>Gradient-boosted trees usually match or beat them on tabular "
    "data</b> (Module 06 &sect;3), with far less tuning, no feature "
    "scaling requirement, and native handling of categorical and missing "
    "values — all of which the SVM needs engineered.",
    "<b>And neural networks took the structured domains</b> — images, "
    "audio, text — where kernel methods had been briefly competitive, "
    "by learning the representation rather than specifying it.",
    "<b>They remain excellent on small, wide, clean data:</b> a few "
    "thousand samples and many features, which describes a great deal of "
    "bioinformatics and chemometrics. <b>And they remain the natural "
    "choice wherever a custom kernel encodes real domain structure</b> "
    "— comparing sequences, molecules, or graphs — because "
    "defining a similarity is sometimes far easier than defining a feature "
    "vector."]),
  ("callout", "What kernels taught the rest of the field",
   ["<b>The margin idea became a loss function.</b> Hinge loss and its "
    "relatives appear throughout deep learning, in metric learning, "
    "contrastive objectives, and ranking — the geometry outlived the "
    "algorithm.",
    "<b>The representer theorem explains how an n-sample method can work "
    "in a very high-dimensional space at all</b>, which is precisely the "
    "question deep learning still wrestles with (Module 03 &sect;4). The "
    "kernel answer — effective capacity is bounded by samples and "
    "regularisation, not by dimension — was the first clean statement "
    "of it.",
    "<b>And 'make the problem linear in a transformed space' is the entire "
    "strategy of representation learning.</b> <b>A deep network's final "
    "layer is a linear classifier operating on learned features</b> "
    "(CSCE 636 Module 05) — structurally the same arrangement as a "
    "kernel machine.",
    "<b>So the difference is where the features come from: a kernel "
    "specifies them in advance, and a network learns them from the "
    "data.</b> <b>That one sentence is most of the history of the field "
    "between about 1995 and 2015</b>, and it explains both why kernels won "
    "when data was scarce and why networks won when it was not — "
    "learning a representation requires enough examples to learn it "
    "from."]),
 ],
 "resources": [
   ("Stanford CS229 &mdash; support vector machines notes (free)",
    "https://cs229.stanford.edu/",
    "<b>The derivation of &sect;1 and &sect;2</b>, including the dual "
    "formulation that makes the kernel substitution visible."),
   ("Hastie et al. &mdash; The Elements of Statistical Learning, "
    "chapter 12 (free PDF)",
    "https://hastie.su.domains/ElemStatLearn/",
    "SVMs with the regularisation framing, which makes the C–&lambda; "
    "connection of &sect;1 explicit."),
   ("Sch&ouml;lkopf & Smola &mdash; Learning with Kernels",
    "https://mitpress.mit.edu/9780262536578/learning-with-kernels/",
    "The reference for the representer theorem and for constructing custom "
    "kernels (&sect;2). Library copy."),
   ("scikit-learn &mdash; SVM user guide and the kernel approximation "
    "module (free)",
    "https://scikit-learn.org/stable/modules/svm.html",
    "Practical tuning of C and &gamma;, and the Nystr&ouml;m and random "
    "feature approximations that address &sect;3's scaling problem."),
 ],
 "exercises": [
   "Fit a linear SVM on separable data and <b>identify the support "
   "vectors</b>. Move a non-support point and confirm nothing changes.",
   "Sweep C and plot the margin width and the violation count.",
   "<b>Verify that C is the inverse of &lambda;</b> by fitting an "
   "equivalent regularised linear model.",
   "<b>Compute a degree-3 polynomial kernel explicitly</b> and via the "
   "kernel function. Compare the results and the cost.",
   "Count how many explicit features a degree-5 polynomial kernel would "
   "need on your dataset.",
   "<b>Fit an RBF SVM and sweep &gamma;</b>, visualising the decision "
   "boundary at each value.",
   "<b>Tune &gamma; and C jointly on a grid</b> and plot the validation "
   "surface. Explain its shape.",
   "Measure training time against sample size from 1,000 to 100,000 and "
   "confirm the superlinear growth.",
   "<b>Compare an SVM against gradient-boosted trees</b> on a wide, small "
   "dataset and on a tall one. Report both.",
   "Define a custom kernel for a non-vector object (strings or sets) and "
   "verify it is positive semidefinite.",
 ],
 "selfcheck": [
   "What does the SVM maximise, and which points affect the solution?",
   "What does C control, and what is it the inverse of?",
   "State the kernel trick and say what makes it possible.",
   "Give two kernels and say what their feature spaces are.",
   "State the representer theorem and its two consequences.",
   "Why does SVM cost scale with n rather than d, and when is that good?",
   "Give three reasons SVMs lost ground and two places they still fit.",
   "What is the relationship between a kernel machine and a deep network?",
 ],
},

]
