# -*- coding: utf-8 -*-
"""CSCE 636 Deep Learning — original course content."""

COURSE = {
    "code": "CSCE 636",
    "title": "Deep Learning",
    "tagline": "Learned representations — backpropagation, "
               "architecture as inductive bias, and what the resulting "
               "models cannot do",
    "term": "Semester 6 (with CSCE 633 and CSCE 669)",
    "prereqs": "CSCE 633 Machine Learning; CSCE 735 Parallel Computing "
               "(Modules 08–09 especially); linear algebra and "
               "calculus",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A trained network you built and debugged yourself, "
                   "with the training curves that show what went wrong "
                   "first, a measured comparison against a non-deep "
                   "baseline, and an account of what it fails on",
    "description": [
        "CSCE 633 ended with a module on feature engineering — on "
        "deciding, by hand, what to show the model. <b>Deep learning is "
        "the proposal that the representation should be learned "
        "too</b>, and that given enough data and enough compute, learned "
        "features beat designed ones by a wide margin in any domain with "
        "exploitable structure.",
        "<b>That proposal turned out to be correct, and the reasons are "
        "not what was predicted.</b> It was not that deeper networks "
        "approximate more functions — a two-layer network already "
        "approximates anything. <b>It was that architecture encodes an "
        "assumption about the data</b>, and that gradient descent on an "
        "enormously overparameterised non-convex surface works far better "
        "than any theory anticipated. <b>Module 03 is honest that nobody "
        "fully knows why</b>, which is an uncomfortable thing to teach and "
        "the truth.",
        "The second theme is that <b>almost all of the difficulty is "
        "engineering</b>. The mathematics of backpropagation is a week; "
        "making a network actually train is the rest of the course. "
        "<b>Module 02 derives the gradients, and Modules 03, 04, and 08 "
        "are about initialisation, normalisation, learning rates, "
        "precision, and memory</b> — the things that decide whether "
        "the derivation ever produces a working model.",
        "The payoff for this program is <b>Modules 10 and 11</b>. "
        "Generative models and neural rendering are where deep learning "
        "has changed graphics directly: <b>learned denoising made path "
        "tracing interactive</b> (CSCE 647 Module 12), <b>and neural "
        "radiance fields and Gaussian splatting replaced the "
        "reconstruction pipeline of CSCE 748 outright.</b> This course "
        "closes those loops.",
    ],
    "outcomes": [
        "Explain why depth helps, and why the universal approximation "
        "theorem does not.",
        "Derive backpropagation and implement reverse-mode "
        "autodifferentiation.",
        "Diagnose vanishing and exploding gradients from evidence.",
        "Choose an optimiser, a schedule, and an initialisation with "
        "reasons.",
        "Explain batch normalisation, dropout, and what each actually "
        "does.",
        "Explain convolution and attention as inductive biases.",
        "Implement a transformer and explain each component's purpose.",
        "Apply transfer learning and say when it fails.",
        "Explain diffusion models and neural rendering.",
        "State what networks reliably fail at, and report honestly.",
    ],
    "materials": [
        ("Andrej Karpathy — Neural Networks: Zero to Hero (free)",
         "https://karpathy.ai/zero-to-hero.html",
         "<b>The primary source for Modules 02, 06, and 07.</b> Builds "
         "autodifferentiation and then a transformer from nothing, on "
         "video, with every line typed. <b>Do this before anything "
         "else.</b>"),
        ("Zhang, Lipton, Li & Smola — Dive into Deep Learning "
         "(free interactive book)",
         "https://d2l.ai/",
         "<b>Free, complete, and runnable.</b> Every chapter has working "
         "code in several frameworks. The reference for Modules 04, 05, "
         "and 08."),
        ("Stanford CS231n — Convolutional Neural Networks (free notes "
         "and lectures)",
         "https://cs231n.github.io/",
         "<b>The Module 05 reference</b>, and the best free treatment of "
         "the practical training material in Modules 03 and 04."),
        ("Goodfellow, Bengio & Courville — Deep Learning (free book)",
         "https://www.deeplearningbook.org/",
         "Free in full. The theoretical grounding; dated on "
         "architectures and still correct on the fundamentals."),
        ("Lilian Weng — Lil'Log (free)",
         "https://lilianweng.github.io/",
         "<b>The reference for Module 10.</b> Her posts on diffusion "
         "models and on attention are clearer than most papers on the same "
         "subjects."),
        ("Papers with Code, and the original architecture papers (free)",
         "https://paperswithcode.com/",
         "<b>Read the primary papers for the architectures you use.</b> "
         "They are shorter than expected and the ablation tables are where "
         "the actual knowledge is."),
    ],
    "tooling": [
        "<b>PyTorch.</b> <b>Write your own autodifferentiation engine "
        "first</b> (Module 02) and then use the framework — the same "
        "pattern this program has used throughout.",
        "<b>A GPU, or a free hosted notebook.</b> <b>A modest laptop GPU "
        "is sufficient for every exercise here</b>; the point is "
        "understanding, not scale, and CSCE 735 Module 08 already covered "
        "the hardware.",
        "<b>Experiment tracking</b> — Weights &amp; Biases, MLflow, "
        "or a disciplined spreadsheet. <b>You will run hundreds of "
        "configurations and will not remember them.</b>",
        "<b>A fixed seed and a deterministic flag</b>, and the knowledge "
        "that <b>full determinism on a GPU costs performance and is "
        "sometimes unavailable</b> (CSCE 735 Module 13).",
        "<b>A tiny dataset you can overfit in seconds.</b> <b>The single "
        "most useful debugging tool in this course</b> — Module 03 "
        "explains why.",
        "<b>A non-deep baseline from CSCE 633</b>, kept and reported "
        "alongside every result.",
    ],
    "projects": [
        {"title": "Build it from scratch, then make it train", "after": 7,
         "brief": "Implement reverse-mode autodifferentiation and a small "
                  "network on top of it, then train a real architecture "
                  "and document everything that went wrong.",
         "reqs": [
             "<b>A working autodifferentiation engine</b> — scalar or "
             "tensor — with gradients verified numerically.",
             "A network trained on a real dataset, from your engine or "
             "from PyTorch.",
             "<b>The overfit-one-batch test passed</b> before any full "
             "training run.",
             "<b>Training curves for every run, including the failures</b>, "
             "with the diagnosis written on each.",
             "A learning rate sweep, plotted.",
             "<b>A comparison against your CSCE 633 baseline</b> on the "
             "same data and the same split.",
         ],
         "done": [
             "<b>Gradient checking passes to within numerical "
             "tolerance.</b>",
             "<b>A gallery of failed training runs with the cause "
             "identified</b> — diverged, plateaued, overfitted, dead "
             "units. <b>This is graded; a clean first run means you did "
             "not try hard enough.</b>",
             "<b>The non-deep baseline's score next to yours.</b> If it "
             "wins, that is a legitimate and reportable result.",
             "A statement of how much compute the whole thing consumed.",
         ]},
        {"title": "Transfer, generate, or render", "after": 12,
         "brief": "Take one of the later modules further — fine-tune "
                  "a pretrained model, train a generative model, or "
                  "implement a neural rendering method.",
         "reqs": [
             "<b>One of:</b> a fine-tuned pretrained model with a "
             "from-scratch comparison; a diffusion or VAE model with "
             "samples; or a NeRF or Gaussian splatting implementation on "
             "your own captures.",
             "<b>Measured inference cost</b> — latency, memory, and "
             "energy if you can.",
             "<b>An adversarial or out-of-distribution probe</b> showing "
             "where it breaks.",
             "A quantised or distilled version, with the quality cost "
             "measured.",
             "<b>Honest failure cases, shown rather than described.</b>",
         ],
         "done": [
             "<b>Qualitative results that are shown, not claimed</b> "
             "— images, renders, or samples, including the bad ones.",
             "<b>A quality-against-cost curve</b> for the quantised or "
             "distilled variants.",
             "<b>A documented failure mode you found yourself</b>, with "
             "the input that triggers it.",
             "<b>A statement of what this model should not be used "
             "for</b>, and why.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Why Depth",
 "subtitle": "Learning the representation instead of designing it.",
 "question": "What changed, and why did it work?",
 "outcomes": [
     "Explain why universal approximation does not justify depth.",
     "Explain architecture as encoded assumption.",
     "Explain what actually changed around 2012.",
     "State when deep learning is the wrong choice.",
     "Set up the tooling and the baseline.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The proposal",
   "blurb": "Stop designing features."},

  {"t": "callout", "title": "The pipeline collapsed into one optimisation",
   "kind": "What deep learning actually proposed",
   "body": ["<b>The classical pipeline: hand-designed features, then a "
            "simple model.</b> SIFT then an SVM; MFCCs then a mixture "
            "model; n-grams then logistic regression.",
            "<b>Each stage was tuned separately</b>, by domain experts, "
            "against a proxy objective that was not the final task.",
            "<b>Deep learning replaces the whole pipeline with one "
            "function trained end to end</b> on the actual objective.",
            "<b>So the features are optimised for the task rather than "
            "for a human's notion of what should matter</b> — and that "
            "turns out to be worth more than decades of feature design, "
            "wherever there is enough data to learn from."]},

  {"t": "callout", "title": "Universal approximation does not explain any of this",
   "kind": "The theorem people cite incorrectly",
   "body": ["<b>A network with one hidden layer can approximate any "
            "continuous function on a compact set, to any accuracy.</b> "
            "That is the theorem.",
            "<b>It says nothing about how many units are needed</b> "
            "— which may be exponential — <b>nor whether gradient "
            "descent will find them</b>, nor whether the result "
            "generalises.",
            "<b>So it does not justify depth at all.</b> It says shallow "
            "networks are already universal.",
            "<b>What depth buys is <i>efficiency</i> of representation:</b> "
            "functions expressible compactly by a deep network can require "
            "exponentially many units when shallow. <b>Expressivity was "
            "never the constraint; learnability was.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Architecture as assumption",
   "blurb": "The actual mechanism."},

  {"t": "table", "kicker": "Inductive bias", "title": "What each architecture assumes about the data",
   "header": ["Architecture", "Assumes", "So it suits"],
   "widths": [2.7, 4.5, 4.9],
   "rows": [
     ["<b>Fully connected</b>", "<b>Nothing. Every input relates to every other</b>", "<b>Tabular — where it loses to trees</b>"],
     ["<b>Convolution</b>", "<b>Locality and translation invariance</b>", "<b>Images, audio, anything gridded</b>"],
     ["<b>Recurrence</b>", "Sequential dependence; shared dynamics", "Sequences — superseded by attention"],
     ["<b>Attention</b>", "<b>Any element may relate to any other, learned</b>", "<b>Text, and increasingly everything</b>"],
     ["Graph networks", "Relations given by an explicit graph", "Molecules, meshes, social networks"],
     ["<b>Equivariant nets</b>", "<b>A known symmetry group</b>", "Physics, chemistry, 3D"],
   ],
   "footnote": "<b>Architecture is a prior.</b> It is how you tell the "
               "model what you know about the data before it sees any.",
   "note": "This table is the module's central idea; everything else "
           "supports it."},

  {"t": "callout", "title": "A matched inductive bias is worth enormous amounts of data",
   "kind": "Why convolution won images",
   "body": ["<b>A fully connected layer on a 224×224 image has 50,000 "
            "inputs and no notion that nearby pixels are related.</b> It "
            "must learn that from examples.",
            "<b>A convolution builds it in:</b> weights are shared across "
            "positions, so a feature learned anywhere is available "
            "everywhere, and the parameter count drops by orders of "
            "magnitude.",
            "<b>That is not merely efficient — it is a correct "
            "assumption about images</b>, and a correct assumption "
            "substitutes for data.",
            "<b>Which is also why the same architecture loses on "
            "tabular data</b> (CSCE 633 M06): <b>column order is "
            "arbitrary, so locality is false</b>, and the bias is wrong "
            "rather than merely absent."]},

  {"t": "section", "label": "Part 3", "title": "What changed",
   "blurb": "Why 2012 and not 1989."},

  {"t": "table", "kicker": "History", "title": "The ingredients, and when each arrived",
   "header": ["Ingredient", "When", "Why it mattered"],
   "widths": [2.7, 2.6, 6.8],
   "rows": [
     ["Backpropagation", "1986", "<b>The mathematics was never the bottleneck</b>"],
     ["Convolutional nets", "1989", "LeCun's digit recognition worked, at small scale"],
     ["<b>GPUs</b>", "<b>~2007–12</b>", "<b>Two orders of magnitude of throughput (CSCE 735 M08)</b>"],
     ["<b>Large labelled data</b>", "<b>ImageNet, 2009</b>", "<b>14M images — enough to learn representations</b>"],
     ["<b>ReLU</b>", "~2011", "<b>Fixed vanishing gradients in deep stacks (M02)</b>"],
     ["Better initialisation", "2010–15", "Xavier, He — made depth trainable at all"],
     ["<b>Normalisation</b>", "2015", "<b>Batch norm made training robust to the learning rate</b>"],
   ],
   "footnote": "<b>The idea waited twenty-five years for the compute and "
               "the data</b>, plus a handful of small engineering fixes "
               "that mattered enormously.",
   "note": "That ReLU and initialisation were decisive is a good "
           "corrective to 'it was just compute'."},

  {"t": "section", "label": "Part 4", "title": "When not to",
   "blurb": "The honest boundary."},

  {"t": "bullets", "kicker": "Not this", "title": "When deep learning is the wrong choice",
   "items": [
     "<b>Tabular data.</b> Gradient-boosted trees usually win "
     "(CSCE 633 M06), with less tuning and no GPU.",
     "",
     "<b>Small data.</b> Under a few thousand examples with no "
     "pretrained model available, there is nothing to learn a "
     "representation from.",
     "",
     "<b>You need to explain the decision.</b> Attribution methods are "
     "not explanations (M12).",
     "",
     "<b>Inference cost matters more than accuracy</b> — on a "
     "microcontroller, in a 16 ms frame budget.",
     "",
     "<b>Or a classical method already solves it</b> — which is the "
     "most common case and the least often checked.",
   ],
   "footnote": "<b>Fit the CSCE 633 baseline first and keep it.</b> It is "
               "the number every result in this course is relative to."},
 ],
 "takeaways": [
   "Deep learning replaces a hand-designed feature pipeline with one "
   "function trained end to end on the actual objective.",
   "Universal approximation says shallow networks are already universal, "
   "so it does not justify depth — depth buys efficiency of "
   "representation, not expressivity.",
   "Architecture is a prior: it encodes what you already know about the "
   "data's structure before the model sees any.",
   "A correct inductive bias substitutes for data, which is why convolution "
   "won images and why it loses on tabular data where locality is false.",
   "The mathematics was ready in 1986; GPUs, ImageNet, ReLU, "
   "initialisation, and normalisation were what arrived later.",
   "Deep learning is the wrong choice for tabular data, small data, "
   "explainability, and tight inference budgets.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The proposal"),
  ("callout", "The pipeline collapsed into one optimisation",
   ["<b>The classical pipeline had two stages: hand-designed features, "
    "then a simple model.</b> SIFT or HOG descriptors feeding a support "
    "vector machine; MFCCs feeding a Gaussian mixture; n-gram counts "
    "feeding logistic regression. <b>The feature stage was where the "
    "domain expertise lived</b>, and it was the product of years of "
    "careful work.",
    "<b>Each stage was designed and tuned separately</b>, by different "
    "people, against proxy objectives that were not the final task — "
    "a descriptor was evaluated on whether it was distinctive and "
    "repeatable, not on whether it helped the classifier.",
    "<b>Deep learning replaces the entire pipeline with a single function "
    "trained end to end on the actual objective.</b> The early layers "
    "learn whatever representation serves the final loss, and there is no "
    "intermediate target to approximate.",
    "<b>So the features are optimised for the task rather than for a "
    "human's theory of what should matter</b> — and that turns out to "
    "be worth more than decades of hand design, <b>wherever there is "
    "enough data to learn the representation from</b>. That qualifier "
    "carries the whole argument, and &sect;4 is about where it fails."]),
  ("callout", "Universal approximation does not explain any of this",
   ["<b>The theorem: a feedforward network with a single hidden layer and "
    "a non-polynomial activation can approximate any continuous function "
    "on a compact set to arbitrary accuracy.</b> It is true and it is "
    "cited constantly as a justification for neural networks.",
    "<b>It says nothing about how many hidden units are required</b> "
    "— which can be exponential in the input dimension — "
    "<b>nothing about whether gradient descent will find those "
    "weights</b>, and <b>nothing about whether the result generalises to "
    "new data</b>. All three are the questions that matter.",
    "<b>And it does not justify <i>depth</i> at all.</b> It is a statement "
    "about shallow networks: one hidden layer already suffices. If the "
    "theorem were the reason deep learning works, deep learning would not "
    "need to be deep.",
    "<b>What depth actually buys is efficiency of representation.</b> "
    "There are functions a deep network expresses with a modest number of "
    "units that require exponentially many units to express with one hidden "
    "layer — compositional and hierarchical functions especially. "
    "<b>Expressivity was never the binding constraint; learnability "
    "was</b>, and that is an optimisation question (Module 03) rather than "
    "an approximation-theoretic one."]),

  ("h1", "2 &nbsp; Architecture as encoded assumption"),
  ("table", ["Architecture", "What it assumes about the data", "So it "
             "suits"],
   [["<b>Fully connected</b>",
     "<b>Nothing at all.</b> Every input may relate to every other, with "
     "no structure assumed.",
     "<b>Tabular data — where it loses to gradient-boosted trees</b> "
     "(CSCE 633 Module 06 &sect;3), because assuming nothing means "
     "learning everything from examples."],
    ["<b>Convolution</b>",
     "<b>Locality and translation invariance</b> — nearby inputs "
     "relate, and a pattern means the same thing wherever it appears.",
     "<b>Images, audio spectrograms, and anything on a regular grid</b> "
     "where both assumptions genuinely hold."],
    ["<b>Recurrence</b>",
     "Sequential dependence, with the same dynamics applied at every step.",
     "Sequences — <b>and largely superseded by attention</b> "
     "(Module 06)."],
    ["<b>Attention</b>",
     "<b>Any element may relate to any other, and which ones do is "
     "learned</b> rather than fixed by the architecture.",
     "<b>Text, and increasingly images, audio, and proteins</b> — a "
     "weaker prior that needs more data and scales further (Module 07)."],
    ["<b>Graph networks</b>",
     "The relations are given explicitly by a graph the data comes with.",
     "Molecules, meshes (CSCE 645), social networks, scene graphs."],
    ["<b>Equivariant networks</b>",
     "<b>A known symmetry group</b> — rotation, permutation, "
     "translation — under which outputs should transform predictably.",
     "Physics, chemistry, 3D geometry, where the symmetry is a known fact "
     "rather than a guess."]],
   [0.17, 0.40, 0.43]),
  ("callout", "A matched inductive bias is worth enormous amounts of data",
   ["<b>A fully connected layer applied to a 224&times;224 colour image "
    "has 150,000 inputs and no notion whatsoever that adjacent pixels are "
    "related.</b> It must discover locality from examples — and it "
    "can, given enough of them, which is the expensive part.",
    "<b>A convolution builds that knowledge in.</b> Weights are shared "
    "across spatial positions, so a feature learned at one location is "
    "available at every location, and the parameter count drops by orders "
    "of magnitude for the same expressive power on the functions that "
    "matter.",
    "<b>That is not merely a computational efficiency — it is a "
    "<i>correct assumption</i> about images</b>, and a correct assumption "
    "substitutes directly for data. The model does not need to spend "
    "examples learning something it was told.",
    "<b>Which is exactly why the same architecture loses on tabular "
    "data.</b> <b>Column order in a spreadsheet is arbitrary, so locality "
    "is false</b>, and a convolution over columns encodes an assumption "
    "that is not merely absent but <i>wrong</i>. <b>Architecture is a "
    "prior, and a wrong prior is worse than a weak one</b> — which is "
    "the cleanest way to understand CSCE 633 Module 06's result about "
    "trees."]),

  ("break",),
  ("h1", "3 &nbsp; What actually changed"),
  ("table", ["Ingredient", "When", "Why it mattered"],
   [["<b>Backpropagation</b>", "1986 (popularised)",
     "<b>The mathematics was never the bottleneck.</b> It was available "
     "for twenty-five years before the results arrived."],
    ["<b>Convolutional networks</b>", "1989",
     "LeCun's digit recognition worked and was deployed on cheques — "
     "at a scale that did not generalise to harder problems."],
    ["<b>GPUs</b>", "<b>roughly 2007–2012</b>",
     "<b>Two orders of magnitude of arithmetic throughput</b>, and the "
     "workload is almost entirely matrix multiplication (CSCE 735 "
     "Module 08). <b>The single largest factor.</b>"],
    ["<b>Large labelled datasets</b>", "<b>ImageNet, 2009</b>",
     "<b>Fourteen million labelled images</b> — enough to learn a "
     "representation rather than merely fit a classifier."],
    ["<b>ReLU</b>", "~2011",
     "<b>Fixed vanishing gradients in deep stacks</b> (Module 02 "
     "&sect;4). A one-line change with disproportionate effect."],
    ["<b>Principled initialisation</b>", "2010–2015",
     "Xavier and He initialisation. <b>Made networks beyond a few layers "
     "trainable at all</b>, which they previously were not."],
    ["<b>Normalisation layers</b>", "2015",
     "<b>Batch normalisation made training robust to the learning rate</b> "
     "and much faster to converge (Module 04)."]],
   [0.20, 0.20, 0.60]),
  ("p", "<b>The idea waited twenty-five years for the compute and the "
        "data</b> — and also for a handful of small engineering fixes "
        "that mattered enormously. <b>It is a useful corrective to the "
        "'it was just compute' story</b> that ReLU, initialisation, and "
        "normalisation were each decisive, each simple, and each took years "
        "to find. <b>Most of this course is about that kind of "
        "fix</b>, which is why Modules 03 and 04 are longer than "
        "Module 02."),

  ("h1", "4 &nbsp; When deep learning is the wrong choice"),
  ("ul", ["<b>Tabular data.</b> Gradient-boosted trees usually win "
          "(CSCE 633 Module 06 &sect;3), with far less tuning, no GPU, "
          "and native handling of missing values and categoricals. "
          "<b>&sect;2 explains why</b>: there is no structure for an "
          "architecture to exploit.",
          "<b>Small data.</b> Below a few thousand examples with no "
          "suitable pretrained model available, <b>there is nothing to "
          "learn a representation from</b> — and the whole proposal of "
          "&sect;1 depends on there being.",
          "<b>You need to explain the decision.</b> <b>Attribution methods "
          "are not explanations</b> (Module 12 &sect;4), and in regulated "
          "settings a linear model with readable coefficients may be "
          "required rather than merely preferable.",
          "<b>Inference cost matters more than accuracy</b> — on a "
          "microcontroller, inside a 16 ms frame budget (CSCE 650), or at "
          "a scale where energy is the binding constraint. Module 13 covers "
          "what can be recovered by quantisation and distillation, and it "
          "is not unlimited.",
          "<b>Or a classical method already solves the problem</b> — "
          "<b>the most common case and the least often checked</b>. "
          "<b>Fit the CSCE 633 baseline first and keep it</b>; it is the "
          "number every result in this course is reported relative to, and "
          "occasionally it wins."]),
 ],
 "resources": [
   ("Karpathy &mdash; Neural Networks: Zero to Hero, lecture 1 (free)",
    "https://karpathy.ai/zero-to-hero.html",
    "<b>Start here this week.</b> Builds autodifferentiation from nothing "
    "on video; Module 02 assumes you have watched it."),
   ("Goodfellow, Bengio & Courville &mdash; Deep Learning, chapters 1 and "
    "6 (free)",
    "https://www.deeplearningbook.org/",
    "The &sect;1 framing and the universal approximation discussion, "
    "stated carefully rather than as a slogan."),
   ("Krizhevsky, Sutskever & Hinton &mdash; ImageNet Classification with "
    "Deep CNNs (free)",
    "https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html",
    "<b>The 2012 result of &sect;3.</b> Read it for the engineering "
    "detail — the architectural choices are all justified by "
    "ablations."),
   ("Battaglia et al. &mdash; Relational inductive biases, deep learning, "
    "and graph networks (free)",
    "https://arxiv.org/abs/1806.01261",
    "<b>The &sect;2 framing, stated as a general principle.</b> The "
    "clearest available treatment of architecture as prior."),
 ],
 "exercises": [
   "<b>Fit the CSCE 633 baseline</b> on the dataset you will use all "
   "semester and record it.",
   "Train a fully connected network on tabular data and compare against "
   "gradient boosting. <b>Report which wins.</b>",
   "<b>Train the same network on images with the pixels randomly "
   "permuted</b> (a fixed permutation). Compare against a CNN on the "
   "unpermuted images, and against a CNN on the permuted ones.",
   "Explain the three results using &sect;2's argument.",
   "<b>Count the parameters</b> of a fully connected layer and a "
   "convolutional layer with the same input and output sizes.",
   "Train a network with sigmoid activations and with ReLU at eight "
   "layers deep. Report what happens.",
   "<b>Train with and without a principled initialisation</b> at ten "
   "layers.",
   "Measure the wall-clock difference between CPU and GPU training for one "
   "epoch.",
   "Find a problem where a classical method beats a network, and document "
   "it.",
   "Set up experiment tracking and a tiny overfittable dataset before "
   "Module 02.",
 ],
 "selfcheck": [
   "What does deep learning propose, and what does it replace?",
   "State the universal approximation theorem and three things it does "
   "not say.",
   "What does depth actually buy?",
   "Give six architectures and the assumption each encodes.",
   "Why does a correct inductive bias substitute for data?",
   "Why does convolution lose on tabular data?",
   "Name seven ingredients and say which was the largest factor.",
   "Give five cases where deep learning is the wrong choice.",
 ],
},

]

for _b in ("c636_b2", "c636_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
