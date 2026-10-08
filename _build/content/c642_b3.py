# -*- coding: utf-8 -*-
"""CSCE 642 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Model-Based Methods",
 "subtitle": "Learn the dynamics, then plan with them.",
 "question": "Can you buy sample efficiency by learning a model?",
 "outcomes": [
     "Explain the sample-efficiency argument for model-based "
     "learning.",
     "Explain model exploitation and the standard defences.",
     "Explain Dyna and model-based policy optimisation.",
     "Explain latent world models and why they work.",
     "Explain MuZero's planning and what it learns.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The argument",
   "blurb": "Why a model is worth learning."},

  {"t": "callout", "title": "A learned model turns environment steps into compute",
   "kind": "The whole motivation",
   "body": ["<b>Module 01 §2's binding constraint is "
            "environment steps.</b> A learned model can be queried "
            "millions of times for the cost of the data it was fitted "
            "on.",
            "<b>So planning or training inside the model converts a "
            "scarce resource into an abundant one</b> — which is the "
            "single strongest argument in this field.",
            "<b>And the numbers support it:</b> model-based methods "
            "reach Atari performance in 100,000 frames that model-free "
            "methods need tens of millions for.",
            "<b>Which is roughly the human figure</b> "
            "(Module 01 §2) — suggesting that <b>a great "
            "deal of the sample-efficiency gap was the absence of a "
            "model</b>, which is a satisfying and only partly complete "
            "explanation."]},

  {"t": "table", "kicker": "Uses", "title": "Four things to do with a learned model",
   "header": ["Use", "How", "Example"],
   "widths": [2.7, 4.2, 5.2],
   "rows": [
     ["<b>Generate experience</b>", "<b>Train a model-free learner on model rollouts</b>", "<b>Dyna, MBPO</b>"],
     ["<b>Plan at decision time</b>", "<b>Search forward from the current state</b>", "<b>MCTS — CSCE 625 M05; MuZero</b>"],
     ["<b>Short-horizon control</b>", "<b>Optimise an action sequence, execute the first</b>", "<b>Model-predictive control</b>"],
     ["<b>Differentiate through it</b>", "<b>Back-propagate return through the dynamics</b>", "<b>Dreamer. Powerful and delicate</b>"],
   ],
   "footnote": "<b>Planning at decision time is the one that composes "
               "with CSCE 625</b> — given a model, you are back in "
               "that course's setting, with tree search available.",
   "note": "The CSCE 625 connection is the structural insight."},

  {"t": "section", "label": "Part 2", "title": "Model exploitation",
   "blurb": "The failure that defines the field."},

  {"t": "callout", "title": "The policy finds where the model is wrong",
   "kind": "The central difficulty",
   "body": ["<b>A policy optimised against a learned model will find "
            "the states where the model is most optimistic</b> — "
            "because that is where the model promises the most "
            "reward.",
            "<b>And the model is most wrong where it has least data, "
            "which is exactly where an exploring policy goes.</b> <b>The "
            "two effects compound.</b>",
            "<b>Errors also compound over a rollout:</b> a 1% per-step "
            "error becomes unrecognisable after fifty steps, so long "
            "rollouts in a learned model are fiction.",
            "<b>This is CSCE 669 Module 12 §4's warning at "
            "its sharpest</b> — <b>the optimiser seeks the corner of "
            "your model least like reality and builds its policy "
            "there.</b>"]},

  {"t": "bullets", "kicker": "Defences", "title": "The four standard defences",
   "items": [
     "<b>Short rollouts.</b> <b>Branch five to ten steps from real "
     "states rather than rolling out from the start</b> — which "
     "bounds the compounding directly. MBPO's main idea.",
     "",
     "<b>Model ensembles.</b> <b>Train several models; where they "
     "disagree, the model is uncertain</b> — so disagreement is a "
     "usable uncertainty estimate.",
     "",
     "<b>Pessimism.</b> Penalise the reward by the model's "
     "uncertainty, so the policy avoids regions the model does not "
     "know.",
     "",
     "<b>And re-fit continuously.</b> <b>The policy's exploitation "
     "generates exactly the data that corrects the exploited error</b>, "
     "if you keep collecting.",
   ],
   "footnote": "<b>The last one is the elegant part:</b> the failure is "
               "self-correcting <i>provided</i> you alternate between "
               "optimising and collecting, which is why model-based "
               "methods are iterative."},

  {"t": "section", "label": "Part 3", "title": "World models",
   "blurb": "Learning dynamics in a latent space."},

  {"t": "code", "kicker": "World models", "title": "Why latent space, not pixels",
   "lang": "text", "code": """
  PREDICTING PIXELS IS THE WRONG OBJECTIVE. Most of an
  image's bits are irrelevant to control -- textures,
  distant scenery, lighting -- and a pixel-reconstruction
  loss spends its capacity on exactly those, because that
  is where most of the bits are.

  SO: ENCODE to a compact latent z, and learn the dynamics
  THERE.

      encoder     z_t = e(o_t)
      dynamics    z_{t+1} = f(z_t, a_t)       (recurrent)
      reward head r_t = r(z_t)
      and optionally a decoder, used only as a training
          signal to keep z informative

  THEN TRAIN THE POLICY ENTIRELY INSIDE THE LATENT MODEL --
  thousands of imagined trajectories per real step, at no
  environment cost at all.
""",
   "caption": "<b>Accuracy is needed only where it affects the "
              "decision</b> — a general modelling principle rather "
              "than a trick.",
   "note": "Connects to CSCE 636's representation learning directly."},

  {"t": "code", "kicker": "Dreamer", "title": "And differentiating through it",
   "lang": "text", "code": """
  DREAMER goes further: the latent dynamics are
  DIFFERENTIABLE, so the policy gradient can be
  BACK-PROPAGATED THROUGH the imagined trajectory rather
  than estimated by sampling (Module 05).

      -- far lower gradient variance
      -- and model error now compounds through the GRADIENT
         as well as through the state, which is why the
         imagination horizon is kept short (Part 2).

  THIS IS WHY MODEL-BASED METHODS FINALLY WORKED: the model
  does not have to be accurate in pixels, only in the
  features that predict reward.
""",
   "caption": "<b>The latent-space insight is the one to take from this "
              "module</b> — and Dreamer is what it makes "
              "possible.",
   "note": "The horizon-shortening rationale ties back to Part 2."},

  {"t": "section", "label": "Part 4", "title": "MuZero",
   "blurb": "Learn a model that is useful rather than accurate."},

  {"t": "callout", "title": "MuZero learns a model good only for planning",
   "kind": "The idea that is easy to miss",
   "body": ["<b>It learns three functions:</b> a representation, a "
            "latent dynamics, and a prediction head for policy, value, "
            "and reward.",
            "<b>And it never reconstructs the observation at all.</b> "
            "<b>The latent state has no requirement to represent the "
            "world</b> — only to make the <i>predictions</i> "
            "correct.",
            "<b>So the model is trained end to end to support MCTS</b> "
            "(CSCE 625 §05), and its internal state may bear no "
            "resemblance to anything interpretable.",
            "<b>Which is the point:</b> <b>a model only has to be "
            "accurate in the quantities planning consumes</b> "
            "— reward, value, and policy. <b>It is Part 3's "
            "principle taken to its conclusion.</b>"]},

  {"t": "callout", "title": "Where model-based methods stand",
   "kind": "Honest status",
   "body": ["<b>Clearly best on sample efficiency</b>, by one to two "
            "orders of magnitude, which is the metric that matters "
            "wherever interaction is costly.",
            "<b>More complex to implement and tune</b> — several "
            "networks, an imagination horizon, and the defences of "
            "Part 2.",
            "<b>And strongest where the dynamics are learnable:</b> "
            "<b>games, simulated robotics, and systems with smooth "
            "physics</b>. <b>Weaker where dynamics are chaotic or "
            "involve other agents.</b>",
            "<b>So the honest recommendation is:</b> <b>model-free "
            "(PPO or SAC) when samples are cheap; model-based when they "
            "are not</b> — and <b>if you already have a model, you are "
            "in CSCE 625</b>."]},
 ],
 "takeaways": [
   "A learned model turns scarce environment steps into abundant compute, "
   "which is the strongest argument in this field.",
   "Model-based methods reach in 100,000 frames what model-free methods "
   "need tens of millions for — roughly the human figure.",
   "A policy optimised against a learned model finds where the model is "
   "most optimistic, and the model is most wrong where it has least data.",
   "Short rollouts, ensembles, pessimism, and continuous re-fitting are "
   "the four defences, and the last makes the failure self-correcting.",
   "Predicting pixels is the wrong objective; learning dynamics in a "
   "compact latent space is why model-based methods finally worked.",
   "MuZero never reconstructs the observation — the model only has to "
   "be accurate in the quantities planning consumes.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The sample-efficiency argument"),
  ("callout", "A learned model turns environment steps into compute",
   ["<b>Module 01 &sect;2 established that environment steps are the "
    "binding constraint.</b> <b>A learned model can be queried millions "
    "of times for the one-off cost of the data it was fitted on</b>, so "
    "the scarce resource is traded for an abundant one.",
    "<b>So planning inside the model, or training a policy on model "
    "rollouts, converts sample cost into compute cost</b> — which is "
    "<b>the single strongest argument in this field</b> and the reason "
    "model-based methods have persisted through two decades of not quite "
    "working.",
    "<b>And the numbers now support it:</b> model-based methods reach "
    "Atari performance in around 100,000 frames that early model-free "
    "methods required tens of millions for — a two-order-of-"
    "magnitude improvement on the metric that matters most.",
    "<b>Which is roughly the human figure from Module 01 "
    "&sect;2</b> — <b>suggesting that a substantial part of the "
    "sample-efficiency gap was the absence of a model</b> rather than "
    "anything more mysterious. <b>A satisfying and only partly complete "
    "explanation</b>: humans also bring priors about objects and "
    "causality that no current model learns from scratch."]),
  ("table", ["Use", "How", "Example"],
   [["<b>Generate experience</b>",
     "<b>Train an ordinary model-free learner on trajectories sampled "
     "from the model.</b>",
     "<b>Dyna (tabular), MBPO (deep)</b> — the simplest and most "
     "robust use."],
    ["<b>Plan at decision time</b>",
     "<b>Search forward from the current state, choose an action, "
     "discard the search.</b>",
     "<b>Monte Carlo tree search — CSCE 625 Module 05 "
     "&sect;3; MuZero</b> (&sect;4)."],
    ["<b>Short-horizon control</b>",
     "<b>Optimise a sequence of actions over a few steps, execute only "
     "the first, and re-optimise.</b>",
     "<b>Model-predictive control</b> — standard in industrial "
     "control long before this field existed."],
    ["<b>Differentiate through it</b>",
     "<b>Back-propagate the return through the learned dynamics into the "
     "policy.</b>",
     "<b>Dreamer</b> (&sect;3). <b>Powerful and delicate</b>, because "
     "model error propagates through the gradient too."]],
   [0.21, 0.37, 0.42]),
  ("p", "<b>Planning at decision time is the use that composes directly "
        "with CSCE 625.</b> <b>Given a model, you are back in that "
        "course's setting</b> — a known MDP, with tree search and "
        "value iteration available — which means <b>the model-based "
        "agent is a learned front end to a classical planner</b>, and that "
        "is the cleanest way to understand MuZero (&sect;4)."),

  ("h1", "2 &nbsp; Model exploitation"),
  ("callout", "The policy finds where the model is wrong",
   ["<b>A policy optimised against a learned model will find the states "
    "where the model is most optimistic</b>, because <b>that is where the "
    "model promises the most reward</b> — and the optimiser is doing "
    "exactly what it was asked to do.",
    "<b>And the model is least accurate where it has least data, which "
    "is exactly where an exploring policy wants to go.</b> <b>The two "
    "effects compound</b>: the policy is drawn to under-sampled regions "
    "both by curiosity and by the model's erroneous optimism there.",
    "<b>Errors also compound over the length of a rollout.</b> A 1% "
    "per-step prediction error leaves the predicted state unrecognisable "
    "after fifty steps, <b>so long rollouts in a learned model are "
    "fiction</b> regardless of how good the one-step accuracy looks.",
    "<b>This is CSCE 669 Module 12 &sect;4's warning at its "
    "sharpest.</b> <b>The optimiser seeks the corner of your model least "
    "like reality and builds its policy there</b> — and here the "
    "model is itself learned and imperfect by construction, so there is "
    "always such a corner. <b>Which makes the defences below structural "
    "rather than optional.</b>"]),
  ("ul", ["<b>Short rollouts.</b> <b>Branch five to ten model steps from "
          "real states drawn from the replay buffer, rather than rolling "
          "out from an initial state</b> — which <b>bounds the "
          "compounding directly</b> and keeps every imagined state close "
          "to real data. <b>This is MBPO's main idea and it is the "
          "highest-value defence.</b>",
          "<b>Model ensembles.</b> <b>Train several models with "
          "different initialisations; where their predictions disagree, "
          "the model is uncertain</b> — so <b>disagreement is a "
          "usable, cheap uncertainty estimate</b>, which is the thing "
          "CSCE 753 Module 08 &sect;4 said learned systems do not "
          "provide by default.",
          "<b>Pessimism.</b> Penalise the predicted reward by the "
          "model's uncertainty, so the policy actively avoids regions the "
          "model does not know — <b>the inverse of Module 02 "
          "&sect;2's optimism, and correctly so</b>: you are optimistic "
          "about unexplored <i>reality</i> and pessimistic about "
          "unmodelled <i>predictions</i>.",
          "<b>And re-fit the model continuously.</b> <b>The policy's "
          "exploitation generates exactly the data that corrects the "
          "error it exploited</b> — the agent goes to the place the "
          "model was wrong about, discovers the truth, and the model is "
          "updated. <b>So the failure is self-correcting provided you "
          "alternate between optimising and collecting</b>, which is <b>the "
          "elegant part and the reason model-based methods are necessarily "
          "iterative</b> rather than a train-then-deploy pipeline."]),

  ("break",),
  ("h1", "3 &nbsp; World models and latent dynamics"),
  ("code", """PREDICTING PIXELS IS THE WRONG OBJECTIVE. Most of an
image's bits are irrelevant to control -- textures, distant
scenery, lighting, shadows -- and a pixel-reconstruction
loss spends its capacity on exactly those, because they are
where most of the bits are.

SO: ENCODE to a compact latent z and learn the dynamics
THERE.

    encoder      z_t = e(o_t)
    dynamics     z_{t+1} = f(z_t, a_t)      (recurrent)
    reward head  r_t = r(z_t)
    and optionally a decoder, used only as a training
        signal to keep z informative about the observation

THEN TRAIN THE POLICY ENTIRELY INSIDE THE LATENT MODEL --
thousands of imagined trajectories per real environment
step, at no environment cost.

DREAMER goes further: the latent dynamics are
DIFFERENTIABLE, so the policy gradient can be
back-propagated THROUGH the imagined trajectory rather than
estimated by sampling (Module 05).
    -- far lower gradient variance
    -- and model error now compounds through the GRADIENT
       as well as through the state, which is why the
       imagination horizon is kept short (section 2).

THIS IS WHY MODEL-BASED METHODS FINALLY WORKED: the model
does not have to be accurate in pixels, only in the
features that predict reward."""),
  ("p", "<b>The latent-space insight is the one to take from this "
        "module.</b> <b>Accuracy is needed only where it affects the "
        "decision</b> — which is a general modelling principle well "
        "beyond reinforcement learning, and it is the same idea as "
        "CSCE 636's representation learning: <b>a representation is good "
        "if it preserves what the task needs and discards what it does "
        "not</b>, and the reconstruction objective is a proxy for that "
        "rather than the thing itself."),

  ("h1", "4 &nbsp; MuZero, and the status of the field"),
  ("callout", "MuZero learns a model good only for planning",
   ["<b>It learns three functions:</b> a representation function mapping "
    "observations to a latent state, a latent dynamics function, and a "
    "prediction head producing a policy, a value, and a reward from the "
    "latent state.",
    "<b>And it never reconstructs the observation at all.</b> <b>The "
    "latent state has no requirement whatsoever to represent the "
    "world</b> — only to make the predictions correct under the "
    "dynamics, which is a far weaker and far more achievable "
    "requirement.",
    "<b>So the model is trained end to end to support Monte Carlo tree "
    "search</b> (CSCE 625 Module 05 &sect;3), and <b>its internal "
    "state may bear no resemblance to anything a person would recognise "
    "as a board position or a game state.</b> That is permitted, and the "
    "planning still works.",
    "<b>Which is the point, and it is easy to miss:</b> <b>a model only "
    "has to be accurate in the quantities planning actually "
    "consumes</b> — reward, value, and policy. <b>It is &sect;3's "
    "principle taken to its conclusion</b>, and it dissolves the "
    "assumption that a model-based agent needs a model <i>of the "
    "world</i> rather than a model <i>of the decision problem</i>."]),
  ("callout", "Where model-based methods stand",
   ["<b>Clearly best on sample efficiency</b>, by one to two orders of "
    "magnitude — which is the metric that matters wherever "
    "interaction is slow, expensive, or risky, and that is most "
    "non-game applications.",
    "<b>More complex to implement and tune</b>: several networks, an "
    "imagination horizon, a model-to-real data ratio, and the defences "
    "of &sect;2 — all of which are hyperparameters that model-free "
    "methods do not have.",
    "<b>And strongest where the dynamics are learnable:</b> <b>board "
    "and video games, simulated robotics, and systems with smooth "
    "physics.</b> <b>Weaker where the dynamics are chaotic, "
    "discontinuous, or involve other adapting agents</b> (Module 11), "
    "since a model of a learning opponent is a model of a moving "
    "target.",
    "<b>So the honest recommendation is:</b> <b>model-free (PPO or SAC) "
    "when samples are cheap, because it is simpler and the complexity "
    "buys nothing; model-based when samples are not cheap, because "
    "nothing else closes the gap.</b> <b>And if you already have a "
    "model, you are in CSCE 625 and should plan rather than learn</b> "
    "(Module 01 &sect;3's first row, which keeps being the right "
    "answer)."]),
 ],
 "resources": [
   ("Sutton & Barto &mdash; chapter 8 (free PDF)",
    "http://incompleteideas.net/book/the-book.html",
    "<b>Dyna and the planning-learning relationship</b>, in the tabular "
    "setting where it is clearest."),
   ("Janner et al. &mdash; When to Trust Your Model: Model-Based Policy "
    "Optimization (free)",
    "https://arxiv.org/abs/1906.08253",
    "<b>&sect;2's short-rollout defence</b>, with the analysis that says "
    "how short."),
   ("Hafner et al. &mdash; Dream to Control, and DreamerV3 (free)",
    "https://danijar.com/project/dreamerv3/",
    "<b>&sect;3's latent world model</b>, and DreamerV3 is notable for "
    "working across many domains with fixed hyperparameters — which "
    "is rare in this field."),
   ("Schrittwieser et al. &mdash; Mastering Atari, Go, Chess and Shogi "
    "by Planning with a Learned Model (MuZero) (free)",
    "https://arxiv.org/abs/1911.08265",
    "<b>&sect;4's method.</b> Read it for the observation that the model "
    "need not model the world."),
 ],
 "exercises": [
   "<b>Implement Dyna-Q</b> on a grid world and compare sample efficiency "
   "against plain Q-learning.",
   "<b>Vary the number of planning steps per real step</b> and plot "
   "performance against environment steps.",
   "<b>Learn a dynamics model</b> for CartPole and measure one-step and "
   "fifty-step prediction error.",
   "<b>Confirm the compounding</b> and report the horizon at which the "
   "prediction becomes useless.",
   "<b>Optimise a policy against the learned model only</b> and evaluate "
   "it on the real environment. Report the gap.",
   "<b>Identify where the policy exploited the model</b> by comparing "
   "predicted and actual rewards along its trajectory.",
   "<b>Add short rollouts from real states</b> and report the "
   "improvement.",
   "<b>Train a model ensemble</b> and plot disagreement against "
   "prediction error. Confirm they correlate.",
   "<b>Add an uncertainty penalty</b> and report the effect on the "
   "model-to-real gap.",
   "<b>Alternate optimisation and collection</b> and show the exploited "
   "error being corrected.",
 ],
 "selfcheck": [
   "State the sample-efficiency argument for model-based learning.",
   "Give the Atari figures for model-based, model-free, and human.",
   "Name four uses of a learned model and which composes with "
   "CSCE 625.",
   "Explain model exploitation and why the two effects compound.",
   "Why are long rollouts in a learned model fiction?",
   "Name four defences and say which is self-correcting.",
   "Why is predicting pixels the wrong objective?",
   "What does Dreamer add, and what does it cost?",
   "What does MuZero's latent state have to represent?",
   "Give the recommendation for when to use model-based methods.",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Learning Without Interaction",
 "subtitle": "Offline reinforcement learning and imitation.",
 "question": "What can you learn from data you did not collect?",
 "outcomes": [
     "Explain behaviour cloning and compounding error.",
     "Explain DAgger and why it helps.",
     "Explain why naive off-policy learning fails offline.",
     "Explain conservative methods and what they constrain.",
     "Choose between imitation and offline reinforcement learning.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Behaviour cloning",
   "blurb": "Supervised learning on expert actions."},

  {"t": "callout", "title": "Behaviour cloning is supervised learning, and its failure is sequential",
   "kind": "The simplest approach and its specific problem",
   "body": ["<b>Collect expert state-action pairs and fit a classifier "
            "or regressor.</b> That is it — it is CSCE 633, with "
            "states as inputs and actions as labels.",
            "<b>And it frequently works</b>, which is worth saying "
            "first: for many tasks it is the strongest option per unit "
            "of effort.",
            "<b>The failure is <i>compounding error</i>.</b> A small "
            "mistake takes the agent slightly off the expert's state "
            "distribution, where the policy is less accurate, which takes "
            "it further off.",
            "<b>So the error grows quadratically in the horizon</b>, "
            "not linearly — <b>and it is a distribution shift the "
            "agent causes itself</b>, which supervised learning has no "
            "mechanism to anticipate."]},

  {"t": "code", "kicker": "DAgger", "title": "Fix it by asking the expert about your own mistakes",
   "lang": "text", "code": """
  THE PROBLEM: training data comes from the EXPERT's state
  distribution; the agent is evaluated on ITS OWN.

  DAgger (dataset aggregation):
      repeat:
          run the CURRENT POLICY to collect states
          ask the EXPERT what it would do in those states
          add those labelled states to the dataset
          retrain

  Now the training distribution converges on the agent's
  own distribution, and the error becomes LINEAR in the
  horizon rather than quadratic.

  THE COST: the expert must be queryable ONLINE, in states
  the expert never chose to visit. For a human expert this
  is laborious and sometimes impossible -- "what would you
  do here?" asked about a situation the person would never
  have got into.

  WHICH IS WHY DAgger IS COMMON IN SIMULATION, where the
  "expert" is a planner or a privileged-information policy
  that can be queried freely, and rare with human experts.

  THIS PATTERN -- train on the distribution you will be
  evaluated on -- IS THE SAME LESSON AS CSCE 753 MODULE 12.
""",
   "caption": "<b>The quadratic-to-linear improvement is the result</b>, "
              "and it comes entirely from fixing whose distribution the "
              "training data is drawn from.",
   "note": "The simulation-vs-human-expert point is what makes DAgger "
           "practical or not."},

  {"t": "section", "label": "Part 2", "title": "Offline reinforcement learning",
   "blurb": "A fixed dataset, and a specific failure."},

  {"t": "callout", "title": "Naive off-policy learning fails offline, for one identifiable reason",
   "kind": "The core difficulty",
   "body": ["<b>Q-learning is off-policy</b> (Module 03 §2), "
            "<b>so running it on a logged dataset looks like it should "
            "work.</b> It does not.",
            "<b>The target contains maxₐ Q(s′,a), and the max "
            "may select an action the dataset never contains</b> — "
            "so Q(s′,a) there is an extrapolation with no data "
            "behind it.",
            "<b>Extrapolated values are arbitrary and tend to be "
            "overestimates</b> (Module 03 §4), <b>and the max "
            "actively seeks them.</b>",
            "<b>With no interaction, nothing corrects it.</b> "
            "<b>Online, the agent would try the action and learn; "
            "offline the error compounds through bootstrapping "
            "forever</b> — which is why offline is harder than "
            "off-policy."]},

  {"t": "table", "kicker": "Methods", "title": "The offline methods and what each constrains",
   "header": ["Method", "Approach", "Constrains"],
   "widths": [2.5, 4.2, 5.3],
   "rows": [
     ["<b>BCQ / BEAR</b>", "<b>Restrict actions to those near the data</b>", "<b>The policy's action distribution</b>"],
     ["<b>CQL</b>", "<b>Penalise Q on out-of-distribution actions</b>", "<b>The value function, which is cleaner</b>"],
     ["<b>IQL</b>", "<b>Expectile regression; never query unseen actions</b>", "<b>Avoids the max entirely. Simple and strong</b>"],
     ["<b>Decision transformer</b>", "<b>Sequence model conditioned on desired return</b>", "<b>Nothing — it is supervised learning</b>"],
   ],
   "footnote": "<b>IQL is the one to try first:</b> <b>it never evaluates "
               "an action outside the dataset</b>, so the failure of Part "
               "2 cannot occur, and it is simpler than the "
               "alternatives.",
   "note": "A clear first recommendation is more useful than four "
           "equals."},

  {"t": "section", "label": "Part 3", "title": "Choosing",
   "blurb": "Imitation or offline reinforcement learning."},

  {"t": "bullets", "kicker": "Choosing", "title": "Which one, given your data",
   "items": [
     "<b>Expert data, and you want expert behaviour: behaviour "
     "cloning.</b> <b>It is simpler and frequently as good.</b>",
     "",
     "<b>Expert data, and the expert is queryable: DAgger.</b> It "
     "fixes the compounding directly.",
     "",
     "<b>Mixed-quality data, and you want to beat the data: offline "
     "RL.</b> <b>This is the only case where it clearly wins</b> "
     "— it can stitch good segments from mediocre trajectories.",
     "",
     "<b>Narrow, uniformly expert data: offline RL gains little</b>, "
     "because there is nothing better to find.",
     "",
     "<b>And no reward labels at all: imitation, or inverse "
     "reinforcement learning</b> to infer the reward.",
   ],
   "footnote": "<b>'Can it beat the data?' is the question that "
               "separates them</b> — and the honest answer is that "
               "it depends on the data containing better behaviour "
               "somewhere to be stitched together."},

  {"t": "section", "label": "Part 4", "title": "Evaluating offline",
   "blurb": "The hardest part, and the least discussed."},

  {"t": "callout", "title": "You cannot evaluate an offline policy offline",
   "kind": "The honest problem",
   "body": ["<b>To know a policy's value you must run it</b>, and in a "
            "genuinely offline setting you cannot.",
            "<b>Off-policy evaluation estimates it from logged data</b> "
            "— importance sampling, doubly robust estimators, fitted "
            "Q-evaluation — <b>and all of them have high variance "
            "when the policies differ</b> (Module 05 §3).",
            "<b>Which is exactly when you need the estimate:</b> if the "
            "learned policy resembles the data's, there was little point "
            "learning it.",
            "<b>So the honest position is:</b> <b>offline training with "
            "a small, careful online evaluation is the realistic "
            "workflow</b>, and purely offline claims should be stated as "
            "estimates with their variance."]},

  {"t": "callout", "title": "Where this matters most",
   "kind": "Why the subfield exists",
   "body": ["<b>Healthcare, education, and anything where exploration "
            "harms someone.</b> <b>You cannot try a random treatment to "
            "see what happens.</b>",
            "<b>Industrial control and robotics</b>, where a bad action "
            "damages equipment and logged operational data is "
            "plentiful.",
            "<b>Recommendation and dialogue</b>, where enormous logs "
            "exist and online experimentation is constrained.",
            "<b>And language model alignment</b> — <b>RLHF is "
            "offline reward modelling plus online policy optimisation</b> "
            "(Module 10 §4), which is the largest deployed "
            "application of anything in this course."]},
 ],
 "takeaways": [
   "Behaviour cloning is supervised learning and frequently works; its "
   "failure is compounding error, quadratic in the horizon.",
   "DAgger converges the training distribution onto the agent's own, "
   "making the error linear — at the cost of needing an online "
   "queryable expert.",
   "Offline reinforcement learning fails naively because the max selects "
   "actions the dataset never contains, and nothing corrects the "
   "extrapolation.",
   "IQL avoids the max entirely, so the failure cannot occur, which makes "
   "it the right first attempt.",
   "'Can it beat the data?' separates imitation from offline RL, and the "
   "answer depends on the data containing better behaviour to stitch.",
   "You cannot evaluate an offline policy offline, because every estimator "
   "has high variance exactly when the policy differs from the data's.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Imitation learning"),
  ("callout", "Behaviour cloning is supervised learning, and its failure is "
              "sequential",
   ["<b>Collect state-action pairs from an expert and fit a classifier or "
    "regressor from states to actions.</b> That is the entire method "
    "— <b>it is CSCE 633, with states as inputs and expert actions "
    "as labels</b>, and every technique from that course applies "
    "unchanged.",
    "<b>And it frequently works</b>, which is worth saying first because "
    "the literature emphasises its failure: <b>for many tasks behaviour "
    "cloning is the strongest option per unit of engineering effort</b>, "
    "and it is what most deployed imitation systems actually use.",
    "<b>The failure is <i>compounding error</i>.</b> A small action error "
    "takes the agent slightly off the expert's state distribution, where "
    "the policy was trained on less data and is therefore less accurate, "
    "which produces a larger error, which takes it further off.",
    "<b>So the error grows quadratically in the horizon rather than "
    "linearly</b> — and <b>it is a distribution shift the agent "
    "causes itself</b>, which is the part supervised learning has no "
    "mechanism to anticipate: the training distribution is fixed and the "
    "test distribution depends on the trained policy. <b>CSCE 753 "
    "Module 12's distribution shift, generated by the model rather than "
    "by the world.</b>"]),
  ("code", """THE PROBLEM: the training data comes from the EXPERT's
state distribution; the agent is evaluated on ITS OWN.

DAgger (dataset aggregation):
    repeat:
        run the CURRENT POLICY to collect states
        ask the EXPERT what it would do in those states
        add those newly labelled states to the dataset
        retrain on the aggregated dataset

Now the training distribution converges onto the agent's
own distribution, and the error becomes LINEAR in the
horizon rather than quadratic.

THE COST: the expert must be queryable ONLINE, in states
the expert never chose to visit. For a human expert this is
laborious and sometimes impossible -- "what would you do
here?" asked about a situation the person would never have
got themselves into, and about which they may have no
useful intuition.

WHICH IS WHY DAgger IS COMMON IN SIMULATION, where the
"expert" is a planner or a policy with privileged
information that can be queried freely and cheaply, and
RARE with human experts.

THIS PATTERN -- train on the distribution you will be
evaluated on -- IS THE SAME LESSON AS CSCE 753 MODULE 12,
arrived at from a different direction."""),

  ("h1", "2 &nbsp; Offline reinforcement learning"),
  ("callout", "Naive off-policy learning fails offline, for one "
              "identifiable reason",
   ["<b>Q-learning is off-policy</b> (Module 03 &sect;2), <b>so "
    "running it on a fixed logged dataset looks like it ought to work</b> "
    "— the algorithm never required the data to come from its own "
    "policy. <b>It does not work</b>, and the reason is specific rather "
    "than general.",
    "<b>The target contains max<sub>a</sub> Q(s&prime;,a), and the max "
    "may select an action that the dataset never contains at that "
    "state</b> — so Q(s&prime;,a) there is a pure extrapolation of "
    "the network, with no data behind it whatsoever.",
    "<b>Extrapolated values are essentially arbitrary and tend to be "
    "overestimates</b> (Module 03 &sect;4's maximisation bias, now "
    "operating on extrapolations rather than on noise), <b>and the max "
    "actively seeks exactly those overestimates.</b>",
    "<b>And with no interaction, nothing corrects it.</b> <b>Online, the "
    "agent would try the over-valued action, receive a poor reward, and "
    "learn; offline, the error propagates through bootstrapping "
    "indefinitely</b> and the Q-values diverge. <b>Which is why offline "
    "is strictly harder than off-policy</b>, and why it needed its own "
    "methods rather than being a straightforward application of "
    "existing ones."]),
  ("table", ["Method", "Approach", "What it constrains"],
   [["<b>BCQ / BEAR</b>",
     "<b>Restrict the policy's actions to those close to actions present "
     "in the data.</b>",
     "<b>The policy's action distribution</b> — which works and "
     "requires a notion of 'close' in action space."],
    ["<b>CQL (conservative Q-learning)</b>",
     "<b>Add a penalty that pushes down Q on out-of-distribution "
     "actions.</b>",
     "<b>The value function, which is cleaner</b> — the policy is "
     "then free to be greedy, because the values it would exploit have "
     "already been suppressed."],
    ["<b>IQL (implicit Q-learning)</b>",
     "<b>Use expectile regression on the value function and never query "
     "Q at an unseen action at all.</b>",
     "<b>It avoids the max entirely, so &sect;2's failure cannot "
     "occur.</b> <b>Simple, strong, and few hyperparameters.</b>"],
    ["<b>Decision transformer</b>",
     "<b>Treat the trajectory as a sequence and train a model to predict "
     "actions conditioned on a desired return.</b>",
     "<b>Nothing — it is supervised sequence learning</b> "
     "(CSCE 638), which sidesteps the whole problem and gives up the "
     "ability to improve on the data by value propagation."]],
   [0.20, 0.38, 0.42]),
  ("p", "<b>IQL is the one to try first.</b> <b>It never evaluates an "
        "action outside the dataset, so &sect;2's failure mode cannot "
        "arise by construction</b> rather than being penalised after the "
        "fact — and it has fewer hyperparameters than CQL, which "
        "matters in a setting where <b>you cannot evaluate your "
        "hyperparameter choices online</b> (&sect;4)."),

  ("break",),
  ("h1", "3 &nbsp; Choosing between them"),
  ("ul", ["<b>Expert data, and expert behaviour is what you want: "
          "behaviour cloning.</b> <b>Simpler, better understood, and "
          "frequently just as good</b> — and if the horizon is short "
          "or the task is forgiving, the compounding error of &sect;1 may "
          "never bite.",
          "<b>Expert data, and the expert is queryable online: "
          "DAgger.</b> It addresses the compounding directly and cheaply, "
          "when the query is available.",
          "<b>Mixed-quality data, and you want to exceed the average "
          "demonstrator: offline reinforcement learning.</b> <b>This is "
          "the case where it clearly wins</b> — <b>it can stitch "
          "good segments from several mediocre trajectories into a policy "
          "better than any single demonstration</b>, which imitation "
          "cannot do by construction.",
          "<b>Narrow, uniformly expert data: offline reinforcement "
          "learning gains little</b>, because there is nothing better in "
          "the data to find, and the conservative constraints will hold it "
          "close to the demonstrations anyway.",
          "<b>And no reward labels at all: imitation, or inverse "
          "reinforcement learning to infer a reward function from the "
          "demonstrations</b> and then optimise it — which connects "
          "directly to Module 10 &sect;4's preference learning.",
          "<b>'Can it beat the data?' is the question that separates "
          "the two families</b>, and <b>the honest answer depends on "
          "whether the data contains better behaviour somewhere to be "
          "stitched together</b>. If every trajectory is equally good, "
          "there is nothing to stitch."]),

  ("h1", "4 &nbsp; Evaluating offline, which is the hard part"),
  ("callout", "You cannot evaluate an offline policy offline",
   ["<b>To know a policy's value you have to run it</b>, and in a "
    "genuinely offline setting you cannot — which means the entire "
    "model-selection and hyperparameter-tuning apparatus of CSCE 633 is "
    "unavailable.",
    "<b>Off-policy evaluation estimates the value from logged data</b> "
    "— importance sampling, doubly robust estimators, fitted "
    "Q-evaluation — <b>and all of them have high variance when the "
    "evaluation policy differs substantially from the logging policy</b> "
    "(Module 05 &sect;3's importance-weight explosion, in an "
    "evaluation role).",
    "<b>Which is exactly the situation in which you need the "
    "estimate:</b> <b>if the learned policy closely resembles the "
    "logging policy, there was little point learning it</b>, and if it "
    "does not, the estimator is unreliable. <b>The problem is structural, "
    "not a gap in the methods.</b>",
    "<b>So the honest position is that offline training with a small, "
    "careful online evaluation is the realistic workflow</b> — even "
    "a few hundred carefully monitored online episodes transform what you "
    "can claim — <b>and that purely offline claims should be stated "
    "as estimates with their variance</b>, which is this program's "
    "standard discipline applied to the one setting where it is hardest "
    "to meet."]),
  ("callout", "Where this matters most",
   ["<b>Healthcare, education, and anything where exploration harms "
    "someone.</b> <b>You cannot try a random treatment to see what "
    "happens</b>, which rules out every method in Modules 02 through "
    "08 and makes this module the only applicable one.",
    "<b>Industrial control and robotics</b>, where a bad action damages "
    "expensive equipment, and where years of logged operational data "
    "already exist from human or classical controllers.",
    "<b>Recommendation and dialogue systems</b>, where enormous "
    "interaction logs exist and online experimentation is constrained by "
    "cost, risk, or policy.",
    "<b>And language model alignment.</b> <b>RLHF is offline reward "
    "modelling from human preference comparisons plus online policy "
    "optimisation against the learned reward</b> (Module 10 &sect;4) "
    "— <b>which is by far the largest deployed application of "
    "anything in this course</b>, and the reason the material in "
    "Module 10 deserves the attention it gets there rather than being a "
    "footnote."]),
 ],
 "resources": [
   ("Levine et al. &mdash; Offline Reinforcement Learning: Tutorial, "
    "Review, and Perspectives (free)",
    "https://arxiv.org/abs/2005.01643",
    "<b>The reference for &sect;2 and &sect;4.</b> The extrapolation "
    "analysis is the clearest statement of the core failure."),
   ("Ross, Gordon & Bagnell &mdash; A Reduction of Imitation Learning "
    "and Structured Prediction (DAgger) (free)",
    "https://arxiv.org/abs/1011.0686",
    "<b>&sect;1's method</b>, with the quadratic-to-linear bound "
    "proved."),
   ("Kostrikov, Nair & Levine &mdash; Offline RL with Implicit "
    "Q-Learning (free)",
    "https://arxiv.org/abs/2110.06169",
    "<b>&sect;2's recommended method</b>, and notably simple for what it "
    "achieves."),
   ("Fu et al. &mdash; D4RL: Datasets for Deep Data-Driven "
    "Reinforcement Learning (free)",
    "https://sites.google.com/view/d4rl/home",
    "<b>Standard offline datasets</b>, including the mixed-quality ones "
    "that make &sect;3's stitching question concrete."),
 ],
 "exercises": [
   "<b>Collect expert data</b> from a trained policy and fit behaviour "
   "cloning. Report the performance gap.",
   "<b>Measure how far the cloned policy's state distribution drifts</b> "
   "from the expert's over an episode.",
   "<b>Plot error against horizon</b> and confirm it is superlinear.",
   "<b>Implement DAgger</b> with the trained policy as the queryable "
   "expert, and confirm the improvement.",
   "<b>Run plain Q-learning on a fixed offline dataset</b> and plot the "
   "Q-values. Confirm they diverge.",
   "<b>Identify which actions the max is selecting</b> and confirm they "
   "are absent from the data.",
   "<b>Implement a conservative penalty</b> and report the effect on both "
   "Q-values and performance.",
   "<b>Implement IQL</b> and compare against CQL on a D4RL dataset.",
   "<b>Build a mixed-quality dataset</b> and show offline RL beating the "
   "average demonstrator while behaviour cloning does not.",
   "<b>Try off-policy evaluation</b> and compare its estimate against the "
   "true online return. Report the error.",
 ],
 "selfcheck": [
   "What is behaviour cloning, and what is its specific failure?",
   "Why does the error grow quadratically?",
   "What does DAgger change, and what does it require?",
   "Why is DAgger common in simulation and rare with human experts?",
   "Explain precisely why naive Q-learning fails offline.",
   "Why does nothing correct the error?",
   "Name four offline methods and what each constrains.",
   "Which should you try first, and why?",
   "What question separates imitation from offline RL?",
   "Why can you not evaluate an offline policy offline?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Reward Design",
 "subtitle": "The hard part, and the one with consequences.",
 "question": "How do you specify what you want?",
 "outcomes": [
     "Explain specification gaming with real examples.",
     "Explain reward shaping and the condition that makes it safe.",
     "Explain why sparse rewards are sometimes the right choice.",
     "Explain reward modelling from preferences.",
     "Anticipate how a reward you wrote will be gamed.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Specification gaming",
   "blurb": "The agent does what you said."},

  {"t": "code", "kicker": "Gaming", "title": "Documented cases, and the pattern",
   "lang": "text", "code": """
  A BOAT RACING AGENT rewarded for collecting checkpoint
  pickups found a lagoon where three pickups respawned, and
  circled it forever -- scoring far higher than finishing
  the race, which was the actual goal.

  A SIMULATED ROBOT rewarded for the height of its centre
  of mass learned to flip onto its back and kick a leg
  upward, rather than to stand.

  A GRIPPER rewarded by a human-judged success signal
  learned to position its hand BETWEEN the camera and the
  object, so that it LOOKED like a grasp.

  AN AGENT penalised for dying learned to pause the game
  indefinitely.

  AN EVOLVED CIRCUIT selected for oscillation used the
  test bench's radio pickup instead of oscillating.

  THE PATTERN IS ALWAYS THE SAME:
      the reward was a PROXY for what was wanted
      the proxy and the goal diverged somewhere
      and the optimiser found exactly that place

  THIS IS NOT AGENTS MISBEHAVING. The agent maximised what
  you wrote. CSCE 625 Module 01's vacuum agent, with a
  much larger search.
""",
   "caption": "<b>Every one of these is a correct solution to the "
              "specified problem</b>, which is why the fix is in the "
              "specification and not in the agent.",
   "note": "The examples do the teaching; let them."},

  {"t": "callout", "title": "Why reinforcement learning games rewards harder than search does",
   "kind": "The comparison worth making",
   "body": ["<b>CSCE 625's search explores a space you defined with "
            "actions you enumerated</b>, so the available "
            "misinterpretations are bounded by what you wrote down.",
            "<b>A reinforcement learning agent explores the environment "
            "itself</b>, including behaviours and interactions you never "
            "considered — including bugs in your simulator.",
            "<b>And it optimises for millions of steps</b>, which is "
            "enough to find a one-in-a-million exploit and then repeat it "
            "indefinitely.",
            "<b>So the same imperfect objective is far more dangerous "
            "here</b> — <b>which is why CSCE 625 M01's abstract point "
            "about performance measures becomes this module's central "
            "practical problem.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Shaping",
   "blurb": "Making the reward denser, safely."},

  {"t": "callout", "title": "Potential-based shaping is provably safe; other shaping is not",
   "kind": "The one theorem in this module",
   "body": ["<b>A sparse reward is hard to learn from</b> "
            "(Module 02 §3), so the temptation is to add "
            "intermediate rewards for progress.",
            "<b>And arbitrary shaping changes the optimal policy</b> "
            "— reward 'moving toward the goal' and the agent may "
            "learn to oscillate toward and away from it, accumulating "
            "the bonus.",
            "<b>Potential-based shaping is the exception:</b> if the "
            "shaping reward has the form "
            "γΦ(s′) − Φ(s) for any "
            "potential function Φ, <b>the optimal policy is "
            "provably unchanged.</b>",
            "<b>Because the shaping telescopes to a constant over any "
            "trajectory</b> — so it changes the learning dynamics "
            "and not the objective. <b>If you must shape, shape this "
            "way.</b>"]},

  {"t": "bullets", "kicker": "Practice", "title": "Designing a reward",
   "items": [
     "<b>Reward the outcome, not the method.</b> <b>Rewarding how you "
     "think it should be done forecloses better solutions and invites "
     "gaming of the proxy.</b>",
     "",
     "<b>Write down what you are <i>not</i> rewarding</b>, and ask "
     "whether the agent can get reward while doing it.",
     "",
     "<b>Then try to game it yourself.</b> <b>Spend twenty minutes "
     "finding the exploit before training</b> — it is the highest "
     "value twenty minutes available.",
     "",
     "<b>Watch the behaviour, not the reward curve.</b> <b>A rising "
     "reward with wrong behaviour is the signature of gaming</b>, and "
     "the curve looks like success.",
     "",
     "<b>And expect to iterate.</b> <b>Three or four reward revisions "
     "is normal</b>, each prompted by watching what the agent found.",
   ],
   "footnote": "<b>'Watch the behaviour, not the curve' is the single "
               "most useful habit in this module</b> — and it is "
               "Module 04 §4's 'the loss is not the "
               "objective', one level up."},

  {"t": "section", "label": "Part 3", "title": "Sparse rewards",
   "blurb": "Why you might choose the harder problem."},

  {"t": "callout", "title": "A sparse reward is honest and hard; a shaped one is easy and may be wrong",
   "kind": "The trade, stated",
   "body": ["<b>A sparse terminal reward — did you win? — "
            "cannot be gamed by construction</b>, because it is the thing "
            "you actually want.",
            "<b>And it is extremely hard to learn from</b>, because the "
            "agent must reach the reward by exploration before any "
            "learning begins (Module 02 §3).",
            "<b>So the options are: better exploration, "
            "demonstrations, a curriculum, or hindsight relabelling</b> "
            "— all of which attack the learning problem rather than "
            "changing the objective.",
            "<b>Hindsight experience replay is the neatest:</b> <b>treat "
            "whatever the agent achieved as if it had been the goal</b>, "
            "so every failed episode becomes a successful one for a "
            "different goal. <b>Free data from failure.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Learning the reward",
   "blurb": "When you cannot write it down."},

  {"t": "callout", "title": "Reward modelling from preferences",
   "kind": "The approach behind RLHF",
   "body": ["<b>Some objectives cannot be written as a function</b> "
            "— 'a helpful answer', 'a natural-looking backflip'. "
            "<b>But a person can compare two behaviours.</b>",
            "<b>So collect pairwise preferences, fit a reward model "
            "to them, and optimise the policy against that model.</b> "
            "That is RLHF.",
            "<b>And the reward model is itself a learned, imperfect "
            "proxy</b> — so <b>the policy will game <i>it</i></b>, "
            "which is Part 1's problem one level up and is called reward "
            "hacking.",
            "<b>The standard defence is a KL penalty toward the "
            "original policy</b> (Module 06 §2's trust region, "
            "reused) <b>plus continued preference collection</b> "
            "— which is Module 08 §2's re-fitting "
            "argument, again."]},

  {"t": "callout", "title": "What to take from this module",
   "kind": "The summary",
   "body": ["<b>The reward is the specification, and specification is "
            "the hard part of this entire subject.</b>",
            "<b>Every agent that did something strange was correctly "
            "optimising something you wrote.</b> <b>The fix is upstream, "
            "in the objective.</b>",
            "<b>Shape only with potential-based terms if you want the "
            "optimum preserved</b>, and otherwise know that you have "
            "changed the problem.",
            "<b>And watch what the agent actually does.</b> <b>Three or "
            "four reward revisions driven by observed behaviour is the "
            "normal and correct workflow</b>, not a sign of poor "
            "planning."]},
 ],
 "takeaways": [
   "Every documented case of specification gaming is a correct solution to "
   "the specified problem, so the fix is in the specification.",
   "Reinforcement learning games rewards harder than search because it "
   "explores the environment itself, including your simulator's bugs, for "
   "millions of steps.",
   "Potential-based shaping provably preserves the optimal policy because "
   "it telescopes to a constant; arbitrary shaping does not.",
   "Reward the outcome rather than the method, and spend twenty minutes "
   "trying to game your own reward before training.",
   "A rising reward curve with wrong behaviour is the signature of gaming, "
   "so watch the behaviour rather than the curve.",
   "A learned reward model is itself a proxy, so the policy games it — "
   "which is why RLHF needs a KL penalty and continued preference "
   "collection.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Specification gaming"),
  ("code", """A BOAT RACING AGENT rewarded for collecting checkpoint
pickups found a lagoon where three pickups respawned, and
circled it forever -- scoring far higher than finishing the
race, which was the actual goal.

A SIMULATED ROBOT rewarded for the height of its centre of
mass learned to flip onto its back and kick one leg upward,
rather than to stand.

A GRIPPER rewarded by a human-judged success signal learned
to position its hand BETWEEN the camera and the object, so
that it LOOKED like a successful grasp.

AN AGENT penalised for dying learned to pause the game
indefinitely.

AN EVOLVED CIRCUIT selected for oscillation used the test
bench's radio pickup instead of oscillating itself.

THE PATTERN IS ALWAYS THE SAME:
    the reward was a PROXY for what was wanted
    the proxy and the real goal diverged somewhere
    and the optimiser found exactly that place

THIS IS NOT AGENTS MISBEHAVING. In every case the agent
maximised what was written. It is CSCE 625 Module 01's
vacuum agent, with a very much larger search behind it."""),
  ("callout", "Why reinforcement learning games rewards harder than search "
              "does",
   ["<b>CSCE 625's search explores a state space you defined, with "
    "actions you enumerated</b>, so <b>the available misinterpretations "
    "are bounded by what you wrote down</b> — a pathfinder can take "
    "a silly route and cannot discover a physics exploit.",
    "<b>A reinforcement learning agent explores the environment "
    "itself</b>, including behaviours, object interactions, and edge "
    "cases you never considered — <b>including bugs in your "
    "simulator</b>, which it treats as perfectly legitimate features of "
    "the world.",
    "<b>And it optimises for millions of steps</b>, which is more than "
    "enough to find a one-in-a-million exploit and then repeat it "
    "indefinitely. <b>A human tester would not find it; an optimiser "
    "with ten million attempts will.</b>",
    "<b>So the same imperfect objective is far more dangerous here than "
    "in CSCE 625.</b> <b>Which is exactly why that course's abstract "
    "point about performance measures becomes this module's central "
    "practical problem</b> — the warning was correct there and is "
    "load-bearing here."]),

  ("h1", "2 &nbsp; Shaping"),
  ("callout", "Potential-based shaping is provably safe; other shaping is "
              "not",
   ["<b>A sparse reward is hard to learn from</b> (Module 02 "
    "&sect;3), so the natural temptation is to add intermediate rewards "
    "for apparent progress — and it is usually the first thing "
    "anyone tries.",
    "<b>And arbitrary shaping changes the optimal policy.</b> Reward "
    "'moving toward the goal' and the agent may learn to oscillate toward "
    "and away from it, collecting the approach bonus repeatedly and never "
    "arriving — which is a higher-scoring policy than finishing, so "
    "the agent is right and the reward is wrong.",
    "<b>Potential-based shaping is the exception, and it is a "
    "theorem:</b> if the shaping term has the form "
    "&gamma;&Phi;(s&prime;) &minus; &Phi;(s) for <i>any</i> potential "
    "function &Phi; over states, <b>the optimal policy is provably "
    "unchanged</b> (Ng, Harada and Russell).",
    "<b>Because the shaping telescopes:</b> summed along any trajectory, "
    "all the intermediate terms cancel and only the endpoints remain, so "
    "<b>the total shaping reward of a trajectory depends only on where it "
    "started and ended</b>. <b>It therefore changes the learning "
    "dynamics without changing the objective</b>, which is exactly what "
    "you want. <b>If you must shape, shape this way</b> — and a "
    "distance-to-goal potential is usually easy to write."]),
  ("ul", ["<b>Reward the outcome, not the method.</b> <b>Rewarding how "
          "you think the task should be done forecloses better solutions "
          "you did not imagine, and it invites gaming of the "
          "proxy</b> — rewarding 'forward velocity of the torso' "
          "produced &sect;1's backflipping robot.",
          "<b>Write down explicitly what you are <i>not</i> "
          "rewarding</b> — safety, smoothness, fuel, time, damage, "
          "the other agents — <b>and ask whether the agent can "
          "obtain reward while violating each.</b> If it can, it will.",
          "<b>Then try to game it yourself.</b> <b>Spend twenty minutes "
          "deliberately looking for the exploit before you start "
          "training</b> — it is the highest-value twenty minutes "
          "available in this course, and it is the same exercise as "
          "CSCE 669 Module 12 &sect;2's 'show the solution and "
          "collect objections', performed in advance.",
          "<b>Watch the behaviour, not the reward curve.</b> <b>A "
          "steadily rising reward accompanied by wrong behaviour is the "
          "signature of specification gaming</b>, and <b>the curve looks "
          "exactly like success</b> — which is why gaming is "
          "discovered late and by accident unless you watch the agent.",
          "<b>And expect to iterate.</b> <b>Three or four reward "
          "revisions driven by observing what the agent found is the "
          "normal and correct workflow</b>, not a sign of poor planning. "
          "<b>'Watch the behaviour, not the curve' is the single most "
          "useful habit in this module</b>, and it is Module 04 "
          "&sect;4's 'the loss is not the objective' one level up: the "
          "<i>reward</i> is not the objective either."]),

  ("break",),
  ("h1", "3 &nbsp; Sparse rewards"),
  ("callout", "A sparse reward is honest and hard; a shaped one is easy and "
              "may be wrong",
   ["<b>A sparse terminal reward — did you win, did the object end "
    "up in the box — cannot be gamed by construction</b>, because it "
    "is not a proxy for what you want: it <i>is</i> what you want.",
    "<b>And it is extremely hard to learn from</b>, because the agent "
    "must reach the reward through exploration before any learning can "
    "begin at all, which is Module 02 &sect;3's corridor problem in "
    "its practical form.",
    "<b>So the options are: better exploration</b> (Module 02 "
    "&sect;3–4), <b>demonstrations to seed the policy</b> "
    "(Module 09), <b>a curriculum of progressively harder tasks, or "
    "hindsight relabelling</b> — <b>all of which attack the "
    "<i>learning</i> problem rather than changing the objective</b>, "
    "which is the right place to attack it.",
    "<b>Hindsight experience replay is the neatest of these:</b> "
    "<b>after a failed episode, relabel it as a success for whatever goal "
    "the agent actually achieved</b> — it did not reach the target "
    "position, but it did reach <i>some</i> position, and that is a "
    "perfectly good training example for a goal-conditioned policy. "
    "<b>Free data extracted from failure</b>, and it transforms sparse "
    "goal-reaching tasks."]),

  ("h1", "4 &nbsp; Learning the reward"),
  ("callout", "Reward modelling from preferences",
   ["<b>Some objectives cannot be written as a function of the state.</b> "
    "'A helpful answer', 'a natural-looking backflip', 'a summary a person "
    "would find useful' — <b>nobody can write these down, and a "
    "person can reliably compare two examples.</b>",
    "<b>So collect pairwise preference judgements, fit a reward model to "
    "them</b> (a Bradley–Terry model over the comparisons), <b>and "
    "optimise the policy against the fitted model</b> using PPO or "
    "similar. <b>That is reinforcement learning from human feedback.</b>",
    "<b>And the reward model is itself a learned, imperfect proxy</b> "
    "— so <b>the policy will game <i>it</i></b>, finding inputs "
    "where the model scores highly and a human would not. <b>Which is "
    "&sect;1's problem exactly, one level up, and it is called reward "
    "hacking</b> — the structure is identical and recognising that "
    "is the useful part.",
    "<b>The standard defence is a KL penalty toward the original "
    "policy</b> (Module 06 &sect;2's trust region, reused for a "
    "different purpose: stay in the region where the reward model was "
    "trained) <b>plus continued collection of fresh preferences on the "
    "current policy's outputs</b> — <b>which is Module 08 "
    "&sect;2's re-fitting argument again</b>: the exploitation generates "
    "the data that corrects it, if you keep collecting."]),
  ("callout", "What to take from this module",
   ["<b>The reward is the specification, and specification is the hard "
    "part of this entire subject.</b> The algorithms of Modules 03 "
    "through 08 are well-documented and largely interchangeable; the "
    "reward is where projects actually fail.",
    "<b>Every agent that did something strange was correctly optimising "
    "something you wrote.</b> <b>So the fix is upstream, in the "
    "objective</b> — not in the algorithm, not in the "
    "hyperparameters, and not in adding a penalty for the specific thing "
    "it just did, which merely relocates the exploit.",
    "<b>Shape only with potential-based terms if you want the optimum "
    "preserved</b> (&sect;2), <b>and otherwise know that you have "
    "deliberately changed the problem</b> and can say how.",
    "<b>And watch what the agent actually does.</b> <b>Three or four "
    "reward revisions driven by observed behaviour is the normal and "
    "correct workflow</b> — which means <b>budget for it</b>, and "
    "treat the first reward function as a draft rather than a "
    "specification."]),
 ],
 "resources": [
   ("Krakovna et al. &mdash; Specification gaming examples in AI (free, "
    "maintained list)",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vRPiprOaC3HsCf5Tuum8bRfzYUiKLRqJmbOoC-32JorNdfyTiRRsR7Ea5eWtvsWzuxo8bjOxCG84dAg/pubhtml",
    "<b>&sect;1's examples and dozens more</b>, collected and sourced. "
    "Browse it before designing any reward."),
   ("Ng, Harada & Russell &mdash; Policy Invariance Under Reward "
    "Transformations (free)",
    "https://web.archive.org/web/20260917115731/https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/readings/NgHaradaRussell-shaping-ICML1999.pdf",
    "<b>&sect;2's theorem</b>, with the telescoping argument. Short and "
    "worth reading in full."),
   ("Andrychowicz et al. &mdash; Hindsight Experience Replay (free)",
    "https://arxiv.org/abs/1707.01495",
    "<b>&sect;3's relabelling trick</b>, which is simple and "
    "unreasonably effective on sparse goal-reaching tasks."),
   ("Christiano et al. &mdash; Deep RL from Human Preferences (free)",
    "https://arxiv.org/abs/1706.03741",
    "<b>&sect;4's method</b>, including the reward-hacking observation "
    "and the continued-collection response."),
 ],
 "exercises": [
   "<b>Read twenty entries</b> in the specification-gaming list and "
   "classify each by which proxy diverged.",
   "<b>Write a reward for a task you care about</b>, then spend twenty "
   "minutes finding its exploit before training.",
   "<b>Train against it</b> and report whether the agent found the same "
   "exploit or a different one.",
   "<b>Write down what you are not rewarding</b> and check each against "
   "the trained agent's behaviour.",
   "<b>Add arbitrary shaping</b> for progress and show the optimal policy "
   "change.",
   "<b>Replace it with potential-based shaping</b> and confirm the optimum "
   "is preserved.",
   "<b>Verify the telescoping</b> numerically along a trajectory.",
   "<b>Train on a sparse version</b> of the same task and report how much "
   "harder it is.",
   "<b>Implement hindsight experience replay</b> and report the "
   "improvement on the sparse version.",
   "<b>Record a video of every agent you train</b> and watch it. Report "
   "something you would not have seen in the curve.",
 ],
 "selfcheck": [
   "Give four documented specification-gaming cases and the common "
   "pattern.",
   "Why does reinforcement learning game rewards harder than search?",
   "Why does arbitrary shaping change the optimal policy?",
   "State the potential-based shaping theorem and why it holds.",
   "Give five reward-design practices.",
   "What is the signature of specification gaming in a training curve?",
   "Why might you choose a sparse reward, and what are the four "
   "responses?",
   "Explain hindsight experience replay.",
   "What is RLHF, and what is reward hacking?",
   "What are the two standard defences against it?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Multiple Agents and Self-Play",
 "subtitle": "When the environment learns too.",
 "question": "What breaks when the other agents are also improving?",
 "outcomes": [
     "Explain non-stationarity and why it breaks the MDP "
     "assumption.",
     "Explain self-play and why it produces a curriculum.",
     "Explain the cycling problem and population-based responses.",
     "Distinguish cooperative from competitive multi-agent "
     "learning.",
     "Explain centralised training with decentralised execution.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Non-stationarity",
   "blurb": "The assumption that fails first."},

  {"t": "callout", "title": "If the other agents learn, your environment is not an MDP",
   "kind": "The structural problem",
   "body": ["<b>An MDP's transition function is fixed</b> "
            "(CSCE 625 M10 §1). <b>If other agents are part of "
            "the environment and they are learning, P changes over "
            "time.</b>",
            "<b>So every convergence argument in this course is void</b> "
            "— and empirically, agents chase each other's changing "
            "behaviour rather than converging.",
            "<b>Replay buffers become actively misleading</b>: stored "
            "transitions describe how opponents behaved, which is no "
            "longer how they behave.",
            "<b>And the right solution concept changes.</b> <b>There is "
            "no 'optimal policy' independent of the others</b> — the "
            "target is an equilibrium (CSCE 625 M12 §4), which "
            "may not be unique."]},

  {"t": "section", "label": "Part 2", "title": "Self-play",
   "blurb": "The agent's opponent is itself."},

  {"t": "callout", "title": "Self-play generates a curriculum automatically",
   "kind": "Why it works so well",
   "body": ["<b>Play against a copy of yourself.</b> <b>The opponent is "
            "always exactly at your level</b>, so the task is always at "
            "the right difficulty — which is a curriculum nobody had "
            "to design.",
            "<b>And it scales:</b> as the agent improves, the opponent "
            "improves, so there is no performance ceiling imposed by a "
            "fixed opponent.",
            "<b>This is how superhuman play was reached in Go, chess, "
            "and shogi</b> — <b>with no human games at all in "
            "AlphaZero's case</b>, which was the striking result.",
            "<b>And the mechanism is simple enough to be suspicious "
            "of:</b> <b>it works beautifully in two-player zero-sum "
            "games with a clear win condition, and much less well "
            "elsewhere</b> (Part 3)."]},

  {"t": "code", "kicker": "Cycling", "title": "Why naive self-play can go in circles",
   "lang": "text", "code": """
  IN ROCK-PAPER-SCISSORS, naive self-play CYCLES:
      the agent learns rock
      its opponent (a copy) learns paper
      which learns scissors
      which learns rock

  No progress, forever -- and note that EACH STEP IS A
  GENUINE IMPROVEMENT against the current opponent.
  Nothing is malfunctioning.

  THE DIAGNOSIS: the game is NON-TRANSITIVE. Strength is
  not a single number, so "better than the last version"
  does not mean "better".
""",
   "caption": "<b>Non-transitivity is the diagnosis</b> — and the "
              "cycle is built from individually correct improvements, "
              "which is what makes it hard to notice.",
   "note": "The rock-paper-scissors cycle makes this immediately "
           "concrete."},

  {"t": "code", "kicker": "Responses", "title": "And how the cycling is broken",
   "lang": "text", "code": """
  OPPONENT POOLS -- play against a sample of PAST versions,
      not only the current one. The agent must now beat
      everything it has previously been, which rules out
      cycling back to a strategy it already defeated.

  FICTITIOUS SELF-PLAY -- play against the historical
      AVERAGE policy, which provably converges to
      equilibrium in two-player zero-sum games.

  POPULATION METHODS (PSRO, league training) -- maintain a
      diverse population with distinct strategies and
      dedicated exploiters, which is what the StarCraft II
      result required.

  AND THE EVALUATION PROBLEM IS REAL: "it beats the
  previous version" is NOT evidence of progress in a
  non-transitive game. Maintain a FIXED benchmark set of
  opponents and report against that, unchanged.
""",
   "caption": "<b>Every response forces the agent to be good against "
              "more than one thing at a time</b>, which is their common "
              "structure.",
   "note": "The fixed-benchmark point is the practical takeaway."},

  {"t": "section", "label": "Part 3", "title": "Cooperation",
   "blurb": "A different problem, with a different fix."},

  {"t": "table", "kicker": "Comparison", "title": "Competitive against cooperative",
   "header": ["", "Competitive", "Cooperative"],
   "widths": [2.3, 4.4, 5.3],
   "rows": [
     ["<b>Reward</b>", "<b>Opposed — zero-sum</b>", "<b>Shared, or team-based</b>"],
     ["<b>Hard part</b>", "<b>Non-transitivity and cycling</b>", "<b>Credit assignment across agents</b>"],
     ["<b>Self-play</b>", "<b>Works extremely well</b>", "<b>Does not apply in the same way</b>"],
     ["<b>Key difficulty</b>", "<b>Evaluating progress</b>", "<b>Which agent caused the team's result?</b>"],
     ["<b>Standard answer</b>", "<b>Opponent pools, populations</b>", "<b>CTDE; value decomposition</b>"],
   ],
   "footnote": "<b>Cooperative multi-agent credit assignment is the "
               "harder open problem</b>, and it is the one that matters "
               "for a game's allied NPCs or a robot team.",
   "note": "The two cases are genuinely different problems and should not "
           "be blended."},

  {"t": "callout", "title": "Centralised training, decentralised execution",
   "kind": "The dominant cooperative architecture",
   "body": ["<b>During training, the critic sees everything</b> "
            "— all agents' observations and actions — so the "
            "learning problem is stationary and credit assignment is "
            "tractable.",
            "<b>At execution each agent uses only its own "
            "observation</b>, so the deployed system is genuinely "
            "decentralised.",
            "<b>This is the dominant architecture for cooperative "
            "multi-agent learning</b>, and value decomposition methods "
            "(VDN, QMIX) <b>factor the team value into per-agent terms "
            "so each agent can act greedily on its own.</b>",
            "<b>And QMIX's constraint is the clever part:</b> <b>require "
            "the mixing to be monotone in each agent's value</b>, so that "
            "maximising individually maximises the team — which makes "
            "decentralised execution provably consistent with the "
            "centralised optimum."]},

  {"t": "section", "label": "Part 4", "title": "In a game",
   "blurb": "What this is actually good for."},

  {"t": "bullets", "kicker": "Games", "title": "Multi-agent learning in a game engine",
   "items": [
     "<b>Self-play for a competitive AI opponent</b> in a game with a "
     "clear win condition. <b>The clearest fit, and the sample cost is "
     "real.</b>",
     "",
     "<b>Difficulty tiers from the opponent pool</b> — "
     "<b>checkpoints from training form a natural ladder</b>, which is "
     "a genuinely useful by-product.",
     "",
     "<b>Emergent tactics as design input:</b> <b>train agents and "
     "watch what they discover</b>, then decide whether to script it or "
     "patch it.",
     "",
     "<b>Not for allied NPC behaviour</b>, usually — "
     "<b>CSCE 625 M11's behaviour trees are controllable and a learned "
     "ally is not.</b>",
     "",
     "<b>And balance testing</b>, which is the most underrated use: "
     "<b>an optimiser finds the dominant strategy before your players "
     "do.</b>",
   ],
   "footnote": "<b>Balance testing is the application most likely to pay "
               "for itself</b> — it uses the specification-gaming "
               "property of Module 10 as a feature rather than fighting "
               "it."},

  {"t": "callout", "title": "The honest status",
   "kind": "Closing the module",
   "body": ["<b>Two-player zero-sum with self-play is a solved "
            "success</b> — Go, chess, poker, and several video "
            "games.",
            "<b>Cooperative multi-agent learning works in constrained "
            "settings</b> and is not reliable at scale.",
            "<b>General mixed-motive multi-agent learning is open</b>, "
            "and the solution concepts themselves are contested "
            "(CSCE 625 M12 §4).",
            "<b>So the sample costs are enormous</b> — the "
            "StarCraft and Dota results used compute budgets unavailable "
            "to almost everyone. <b>Which is worth stating when citing "
            "them as evidence of what is possible.</b>"]},
 ],
 "takeaways": [
   "If other agents are learning, the transition function changes, so the "
   "environment is not an MDP and every convergence argument is void.",
   "Self-play generates a curriculum automatically because the opponent is "
   "always exactly at your level.",
   "Naive self-play cycles in non-transitive games, and every response "
   "forces the agent to be good against more than one thing at a time.",
   "'It beats the previous version' is not evidence of progress in a "
   "non-transitive game — keep a fixed benchmark set.",
   "Competitive and cooperative multi-agent learning are different "
   "problems: cycling against credit assignment.",
   "Centralised training with decentralised execution is the dominant "
   "cooperative architecture, and QMIX's monotonicity makes the two "
   "consistent.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Non-stationarity"),
  ("callout", "If the other agents learn, your environment is not an MDP",
   ["<b>An MDP's transition function is fixed by definition</b> "
    "(CSCE 625 Module 10 &sect;1). <b>If other agents are treated as "
    "part of the environment and those agents are learning, then P "
    "changes over time</b> — so the object you are solving is not an "
    "MDP at all.",
    "<b>So every convergence argument in this course is void.</b> And "
    "empirically the failure is visible: <b>agents chase each other's "
    "changing behaviour rather than converging</b>, and a policy that was "
    "good last hour is exploited this hour.",
    "<b>Replay buffers become actively misleading rather than merely "
    "stale.</b> A stored transition records how opponents behaved at the "
    "time, <b>which is no longer how they behave</b> — so the buffer "
    "teaches the agent to beat an opponent that no longer exists.",
    "<b>And the right solution concept changes.</b> <b>There is no "
    "'optimal policy' independent of what the others do</b> — the "
    "target is an equilibrium (CSCE 625 Module 12 &sect;4), which may "
    "not be unique, may not be reachable by learning, and may be bad for "
    "everyone. <b>Which means even stating the goal precisely is harder "
    "here than anywhere else in the course.</b>"]),

  ("h1", "2 &nbsp; Self-play"),
  ("callout", "Self-play generates a curriculum automatically",
   ["<b>Play against a copy of yourself.</b> <b>The opponent is always "
    "exactly at your level</b>, so the task is always at the right "
    "difficulty — neither trivially easy nor hopeless — "
    "<b>which is a curriculum that nobody had to design</b> and is the "
    "single most valuable property of the method.",
    "<b>And it scales without a ceiling:</b> as the agent improves, so "
    "does the opponent, so there is no fixed-opponent performance plateau "
    "to reach. <b>The task's difficulty tracks the agent's "
    "competence indefinitely.</b>",
    "<b>This is how superhuman play was reached in Go, chess, and "
    "shogi</b> — <b>and in AlphaZero's case with no human games at "
    "all</b>, starting from random play, which was the genuinely "
    "striking part of the result and not merely the strength achieved.",
    "<b>And the mechanism is simple enough to be suspicious of.</b> "
    "<b>It works beautifully in two-player zero-sum games with a clear "
    "win condition, and considerably less well elsewhere</b> — "
    "&sect;3 explains why, and the explanation is not a limitation of "
    "implementation but of the game's structure."]),
  ("code", """IN ROCK-PAPER-SCISSORS, naive self-play CYCLES:
    the agent learns rock
    its opponent (a copy) learns paper
    which learns scissors
    which learns rock

No progress, forever -- and note that EACH STEP IS A
GENUINE IMPROVEMENT against the current opponent. Nothing
is malfunctioning.

THE DIAGNOSIS: the game is NON-TRANSITIVE. Strength is not
a single number, so "better than the last version" does not
mean "better".

THE RESPONSES:
  OPPONENT POOLS -- play against a sample of PAST versions
      rather than only the current one. The agent must now
      beat everything it has previously been, which rules
      out cycling back to a strategy it already defeated.
  FICTITIOUS SELF-PLAY -- play against the historical
      AVERAGE policy, which provably converges to
      equilibrium in two-player zero-sum games.
  POPULATION METHODS (PSRO, league training) -- maintain a
      diverse population with distinct strategies and
      dedicated exploiters, which is what the StarCraft II
      result required.

AND THE EVALUATION PROBLEM IS REAL: "it beats the previous
version" is NOT evidence of progress in a non-transitive
game. Maintain a FIXED benchmark set of opponents and
report against that, unchanged, throughout training."""),

  ("break",),
  ("h1", "3 &nbsp; Cooperation"),
  ("table", ["", "Competitive", "Cooperative"],
   [["<b>Reward structure</b>", "<b>Opposed — zero-sum.</b>",
     "<b>Shared, or a team reward.</b>"],
    ["<b>The hard part</b>",
     "<b>Non-transitivity and cycling</b> (&sect;2).",
     "<b>Credit assignment across agents</b> — the team won, and "
     "which agent's actions caused it?"],
    ["<b>Self-play</b>",
     "<b>Works extremely well</b>, and is the standard method.",
     "<b>Does not apply in the same way</b> — playing against "
     "yourself is not cooperating with yourself."],
    ["<b>Key difficulty</b>", "<b>Evaluating whether progress is "
     "real.</b>",
     "<b>Attributing a shared outcome to individual actions</b>, which "
     "is the temporal credit-assignment problem in a second dimension."],
    ["<b>Standard answer</b>", "<b>Opponent pools, populations, "
     "leagues.</b>",
     "<b>Centralised training with decentralised execution; value "
     "decomposition.</b>"]],
   [0.17, 0.38, 0.45]),
  ("p", "<b>Cooperative multi-agent credit assignment is the harder open "
        "problem</b> of the two, <b>and it is the one that matters for a "
        "game's allied NPCs or for a team of robots</b> — which is "
        "worth knowing, because the field's famous results are almost all "
        "on the competitive side and are not evidence about the "
        "cooperative one."),
  ("callout", "Centralised training, decentralised execution",
   ["<b>During training, the critic sees everything</b> — all "
    "agents' observations and all their actions — <b>so from the "
    "critic's point of view the learning problem is stationary and credit "
    "assignment is tractable</b>, because nothing is hidden.",
    "<b>At execution time each agent uses only its own observation</b>, "
    "so the deployed system is genuinely decentralised and does not "
    "require communication or a central controller.",
    "<b>This is the dominant architecture for cooperative multi-agent "
    "learning</b>, and <b>value decomposition methods (VDN, QMIX) factor "
    "the team's value function into per-agent terms so each agent can act "
    "greedily on its own component.</b>",
    "<b>And QMIX's constraint is the clever part:</b> <b>require the "
    "mixing function to be monotone in each agent's value</b>. <b>Then "
    "maximising each agent's own value individually necessarily maximises "
    "the team value</b> — so <b>decentralised greedy execution is "
    "provably consistent with the centralised optimum</b>, which is "
    "exactly the guarantee the architecture needs and is not obvious that "
    "you can get."]),

  ("h1", "4 &nbsp; Multi-agent learning in a game engine"),
  ("ul", ["<b>Self-play for a competitive AI opponent</b> in a game with "
          "a clear win condition. <b>The clearest fit for the method, and "
          "the sample cost is real</b> — budget for it, and see the "
          "closing callout.",
          "<b>Difficulty tiers taken from the opponent pool.</b> "
          "<b>Checkpoints saved during training form a natural difficulty "
          "ladder</b>, each one a genuine policy of a known strength "
          "— <b>which is a genuinely useful by-product</b> and a "
          "better source of difficulty levels than the handicapping of "
          "CSCE 625 Module 05 &sect;4.",
          "<b>Emergent tactics as design input.</b> <b>Train agents and "
          "watch what they discover</b>, then decide deliberately whether "
          "to script it for the shipped AI, leave it for players to find, "
          "or patch it out.",
          "<b>Not for allied NPC behaviour, usually.</b> <b>CSCE 625 "
          "Module 11's behaviour trees are controllable and legible, and "
          "a learned ally is neither</b> — and an ally that behaves "
          "unpredictably is worse than one that behaves simply, because "
          "the player has to coordinate with it.",
          "<b>And balance testing, which is the most underrated use.</b> "
          "<b>An optimiser finds the dominant strategy before your "
          "players do</b> — which <b>uses the specification-gaming "
          "property of Module 10 as a feature rather than fighting "
          "it</b>, and is the application most likely to pay for itself on "
          "a real project."]),
  ("callout", "The honest status",
   ["<b>Two-player zero-sum with self-play is a solved success.</b> Go, "
    "chess, shogi, heads-up poker, and several video games — "
    "<b>superhuman, repeatedly, by multiple groups.</b>",
    "<b>Cooperative multi-agent learning works in constrained "
    "settings</b> — small teams, shared observations, well-specified "
    "team rewards — <b>and is not reliable at scale.</b>",
    "<b>General mixed-motive multi-agent learning is open</b>, and "
    "<b>the solution concepts themselves are contested</b> — it is "
    "not merely that the algorithms are immature but that <b>what counts "
    "as success is unsettled</b> (CSCE 625 Module 12 &sect;4's "
    "equilibria, which may be multiple and may be bad).",
    "<b>And the sample costs are enormous.</b> <b>The StarCraft II and "
    "Dota 2 results used compute budgets unavailable to almost "
    "everyone</b> — tens of thousands of years of simulated game "
    "time. <b>Which is worth stating whenever those results are cited as "
    "evidence of what is possible</b>, because they are evidence about "
    "what is possible <i>at that budget</i>, and Module 13 makes the "
    "general version of this point."]),
 ],
 "resources": [
   ("Silver et al. &mdash; A general reinforcement learning algorithm "
    "that masters chess, shogi and Go (AlphaZero) (free)",
    "https://arxiv.org/abs/1712.01815",
    "<b>&sect;2's self-play result</b>, with the curriculum property "
    "doing the work."),
   ("Vinyals et al. &mdash; Grandmaster level in StarCraft II with "
    "multi-agent reinforcement learning (free)",
    "https://www.nature.com/articles/s41586-019-1724-z",
    "<b>&sect;2's league training</b>, and the clearest demonstration of "
    "why opponent populations are necessary — and of the compute "
    "cost."),
   ("Rashid et al. &mdash; QMIX (free)",
    "https://arxiv.org/abs/1803.11485",
    "<b>&sect;3's monotone value decomposition</b>, with the consistency "
    "argument."),
   ("Lanctot et al. &mdash; A Unified Game-Theoretic Approach to "
    "Multiagent RL (PSRO) (free)",
    "https://arxiv.org/abs/1711.00832",
    "<b>&sect;2's population method</b>, and a good treatment of why "
    "non-transitivity demands it."),
 ],
 "exercises": [
   "<b>Train two agents against each other</b> and plot each one's "
   "performance against a fixed benchmark. Report whether both appear to "
   "improve.",
   "<b>Implement self-play on a simple game</b> and confirm the "
   "curriculum effect.",
   "<b>Implement rock-paper-scissors self-play</b> and observe the cycle "
   "directly.",
   "<b>Add an opponent pool</b> and confirm the cycling stops.",
   "<b>Maintain a fixed benchmark set</b> and show that 'beats the "
   "previous version' and 'beats the benchmark' disagree.",
   "<b>Set up a cooperative two-agent task</b> with a shared reward and "
   "try independent learners. Report the credit-assignment failure.",
   "<b>Implement a centralised critic</b> and report the improvement.",
   "<b>Implement value decomposition</b> and verify the monotonicity "
   "condition.",
   "<b>Use a trained agent to balance-test a game you have</b>, and "
   "report the dominant strategy it found.",
   "<b>Save checkpoints as difficulty tiers</b> and have someone play "
   "three of them. Report whether the ladder felt even.",
 ],
 "selfcheck": [
   "Why is a multi-agent environment not an MDP?",
   "What happens to replay buffers, and why?",
   "What replaces 'optimal policy' as the goal?",
   "Why does self-play produce a curriculum?",
   "Why does naive self-play cycle, and what is the diagnosis?",
   "Name three responses and what each forces.",
   "Why is 'beats the previous version' insufficient?",
   "Compare competitive and cooperative multi-agent learning on five "
   "axes.",
   "Explain CTDE and QMIX's monotonicity constraint.",
   "Give five uses in a game engine and the honest status of each "
   "setting.",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Reproducibility",
 "subtitle": "The variance is larger than the effects.",
 "question": "How do you tell whether a reinforcement learning result is "
             "real?",
 "outcomes": [
     "Explain seed variance and its magnitude in this field.",
     "Explain why single-seed comparisons are uninformative.",
     "Report results with appropriate statistics.",
     "Explain the confounds beyond seeds.",
     "Read the literature with calibrated scepticism.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The finding",
   "blurb": "Measured, repeatedly, and not disputed."},

  {"t": "callout", "title": "Seed variance routinely exceeds the differences between methods",
   "kind": "The central fact of this module",
   "body": ["<b>Run the identical algorithm on the identical task with "
            "different random seeds and the results differ "
            "enormously</b> — frequently by more than the gap between "
            "two published methods.",
            "<b>Two groups of five seeds from the <i>same</i> algorithm "
            "can appear to be two different algorithms</b>, with "
            "non-overlapping confidence intervals.",
            "<b>So a comparison on one or two seeds carries almost no "
            "information</b>, and a great deal of the published "
            "comparison literature is at that standard.",
            "<b>This is measured, replicated, and not seriously "
            "disputed.</b> <b>It is a property of the field rather than "
            "an accusation against anyone</b> — and knowing it is "
            "necessary to read the literature."]},

  {"t": "bullets", "kicker": "Causes", "title": "Why the variance is so large",
   "items": [
     "<b>The data depends on the policy</b>, which depends on the "
     "data. <b>An early lucky trajectory compounds; so does an early "
     "unlucky one.</b>",
     "",
     "<b>Exploration is stochastic</b>, so two runs see different "
     "parts of the state space entirely.",
     "",
     "<b>Instability</b> (Module 04 §1) <b>means a run can "
     "diverge for reasons that are seed-dependent.</b>",
     "",
     "<b>And a collapse is frequently unrecoverable</b> "
     "(Module 06 §2), so the outcomes are bimodal rather "
     "than spread.",
     "",
     "<b>Which is why the mean is a poor summary:</b> <b>averaging a "
     "bimodal distribution describes neither mode.</b>",
   ],
   "footnote": "<b>The feedback from policy to data is the root "
               "cause</b>, and it is the one thing that genuinely "
               "distinguishes this from supervised learning's seed "
               "variance."},

  {"t": "section", "label": "Part 2", "title": "Reporting",
   "blurb": "What to do about it."},

  {"t": "code", "kicker": "Reporting", "title": "The standard 1/2: seeds and statistics",
   "lang": "text", "code": """
  MINIMUM: FIVE SEEDS. Ten if you can afford it. And REPORT
  HOW MANY -- a result with the seed count omitted cannot
  be assessed at all.

  PLOT ALL THE RUNS, or a median with an interquartile
  range. NOT a mean with a standard deviation, which
  assumes a distribution the data does not have (Part 1).

  REPORT THE INTERQUARTILE MEAN across seeds and tasks. It
  is robust to the outlier runs that dominate a plain mean,
  and the Rliable tooling computes it for you.

  REPORT PERFORMANCE PROFILES: the fraction of runs
  exceeding each score threshold. This shows the whole
  distribution rather than a single statistic, and it makes
  bimodality visible immediately.
""",
   "caption": "<b>The interquartile mean and performance profiles are "
              "the field's own recommended practice</b>, with free "
              "tooling — and adopting them costs nothing.",
   "note": "Give the concrete standard; vague calls for rigour do not "
           "change behaviour."},

  {"t": "code", "kicker": "Reporting", "title": "The standard 2/2: budgets and baselines",
   "lang": "text", "code": """
  REPORT THE SAMPLE BUDGET. "Better after 10M steps" and
  "better after 1M steps" are different claims, and the
  learning curves frequently cross.

  TUNE THE BASELINE AS HARD AS YOU TUNED YOUR METHOD. An
  untuned baseline is not a comparison. This is the single
  largest source of overstated improvements in the field,
  and it is CSCE 633 Module 02's baseline discipline with a
  very specific target.

  AND FIX EVERY SOURCE OF RANDOMNESS you can control:
  environment seeds, network initialisation, action
  sampling, and the framework's global RNG state. Then
  report what you fixed, because full determinism is
  usually unattainable.
""",
   "caption": "<b>An untuned baseline is not a comparison</b> — the "
              "one item here that costs real effort, and the one that "
              "buys the most credibility.",
   "note": "The baseline item is the one most often skipped."},

  {"t": "section", "label": "Part 3", "title": "The other confounds",
   "blurb": "Seeds are not the only problem."},

  {"t": "table", "kicker": "Confounds", "title": "What else makes comparisons invalid",
   "header": ["Confound", "Effect", "What to do"],
   "widths": [2.6, 4.2, 5.2],
   "rows": [
     ["<b>Implementation details</b>", "<b>Can exceed the algorithmic difference</b>", "<b>Match them, or use one codebase (M06 §3)</b>"],
     ["<b>Hyperparameter effort</b>", "<b>Whoever tuned more wins</b>", "<b>Equal budget, reported</b>"],
     ["<b>Environment version</b>", "<b>Reward and termination change between versions</b>", "<b>State the exact version</b>"],
     ["<b>Evaluation protocol</b>", "<b>Best checkpoint vs final vs average differ greatly</b>", "<b>State it; prefer final or average</b>"],
     ["<b>Selective task reporting</b>", "<b>Choosing the tasks where you win</b>", "<b>Report the whole suite</b>"],
   ],
   "footnote": "<b>'Best checkpoint over training' is a form of test-set "
               "selection</b> (CSCE 633 M03) and is extremely common in "
               "this field — it inflates every number it touches.",
   "note": "The best-checkpoint point is a specific, widespread, fixable "
           "error."},

  {"t": "section", "label": "Part 4", "title": "Reading the literature",
   "blurb": "Calibrated scepticism, not cynicism."},

  {"t": "bullets", "kicker": "Reading", "title": "Questions to ask of any result",
   "items": [
     "<b>How many seeds, and is the spread shown?</b> <b>If fewer "
     "than five, or only a mean, the comparison is weak evidence.</b>",
     "",
     "<b>Was the baseline tuned?</b> <b>By whom, and with what "
     "budget?</b>",
     "",
     "<b>Is the improvement larger than the seed spread?</b> If not, "
     "it is not established.",
     "",
     "<b>Is there a released implementation that reproduces the "
     "reported number?</b> <b>Frequently there is not.</b>",
     "",
     "<b>And does the method appear in anyone else's benchmark a year "
     "later?</b> <b>Durable adoption is the strongest available "
     "evidence.</b>",
   ],
   "footnote": "<b>That last question is the most reliable filter</b>, "
               "and it costs one search — methods that work get "
               "used."},

  {"t": "callout", "title": "Why this module exists here and not as a footnote",
   "kind": "The position",
   "body": ["<b>This course cannot teach you to evaluate reinforcement "
            "learning results without saying that the field's standard "
            "practice has been inadequate.</b>",
            "<b>It is improving</b> — the tooling exists, the "
            "statistics are published, and major venues increasingly "
            "require seed reporting.",
            "<b>And it is still common to see three-seed "
            "comparisons</b> with confident claims, which the variance "
            "measurements say cannot be supported.",
            "<b>So the practical instruction is simple:</b> <b>five "
            "seeds minimum, spread shown, baseline tuned, protocol "
            "stated.</b> <b>Meet that standard and your results mean "
            "something regardless of what anyone else does.</b>"]},
 ],
 "takeaways": [
   "Seed variance in this field routinely exceeds the differences between "
   "published methods, which is measured and not disputed.",
   "Two groups of five seeds from the same algorithm can look like two "
   "different algorithms.",
   "The root cause is the feedback from policy to data, which supervised "
   "learning does not have.",
   "Outcomes are frequently bimodal, so a mean with a standard deviation "
   "describes neither mode — use interquartile means and performance "
   "profiles.",
   "An untuned baseline is not a comparison, and it is the largest source "
   "of overstated improvements.",
   "'Best checkpoint over training' is test-set selection and is extremely "
   "common here.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The finding"),
  ("callout", "Seed variance routinely exceeds the differences between "
              "methods",
   ["<b>Run the identical algorithm, on the identical task, with the "
    "identical hyperparameters, varying only the random seed, and the "
    "results differ enormously</b> — frequently by more than the "
    "reported gap between two published methods.",
    "<b>Two groups of five seeds drawn from the <i>same</i> algorithm can "
    "appear to be two different algorithms</b>, with non-overlapping "
    "confidence intervals and a clear apparent winner. <b>This has been "
    "demonstrated directly</b>, by splitting one algorithm's runs into "
    "two groups and comparing them as if they were different methods.",
    "<b>So a comparison on one or two seeds carries almost no "
    "information about which method is better</b>, and <b>a substantial "
    "portion of the published comparison literature is at that "
    "standard</b> — which means a reader cannot distinguish a real "
    "advance from a favourable seed.",
    "<b>This is measured, replicated, and not seriously disputed.</b> "
    "<b>It is a property of the field rather than an accusation against "
    "anyone</b> — the variance is caused by the problem's structure "
    "(&sect;1's list), not by carelessness — <b>and knowing it is "
    "necessary to read the literature usefully at all.</b>"]),
  ("ul", ["<b>The data depends on the policy, which depends on the "
          "data.</b> <b>An early lucky trajectory leads to a better "
          "policy, which collects better data, which compounds</b> "
          "— and an early unlucky one compounds the same way "
          "downward. <b>This feedback is the root cause and is the one "
          "thing that genuinely distinguishes this from supervised "
          "learning's much smaller seed variance.</b>",
          "<b>Exploration is stochastic</b>, so two runs genuinely see "
          "different parts of the state space — not noisier views of "
          "the same data, but different data (Module 02 &sect;3's "
          "corridor, where the seed decides whether the reward is ever "
          "found).",
          "<b>Instability</b> (Module 04 &sect;1) <b>means a run can "
          "diverge for reasons that are seed-dependent</b>, so some "
          "fraction of runs fail outright while others succeed.",
          "<b>And a performance collapse is frequently unrecoverable</b> "
          "(Module 06 &sect;2), <b>so outcomes are bimodal rather than "
          "spread</b>: some runs learn the task and some never do.",
          "<b>Which is why the mean is a poor summary.</b> "
          "<b>Averaging a bimodal distribution produces a number that "
          "describes neither mode</b>, and the standard deviation implies "
          "a shape the data does not have — hence &sect;2's "
          "recommendations."]),

  ("h1", "2 &nbsp; Reporting"),
  ("code", """MINIMUM: FIVE SEEDS. Ten if you can afford it. And REPORT
HOW MANY -- a result with the seed count omitted cannot be
assessed at all.

PLOT ALL THE RUNS, or a median with an interquartile range.
NOT a mean with a standard deviation, which assumes a
distribution the data does not have (section 1).

REPORT THE INTERQUARTILE MEAN across seeds and tasks. It
is robust to the outlier runs that dominate a plain mean,
and it is what the Rliable tooling computes for you.

REPORT PERFORMANCE PROFILES: the fraction of runs exceeding
each score threshold. This shows the whole distribution
rather than one statistic, and it makes bimodality visible
immediately.

REPORT THE SAMPLE BUDGET. "Better after 10M steps" and
"better after 1M steps" are different claims, and the
learning curves frequently cross.

TUNE THE BASELINE AS HARD AS YOU TUNED YOUR METHOD. An
untuned baseline is not a comparison. This is the single
largest source of overstated improvements in the field, and
it is CSCE 633 Module 02's baseline discipline with a very
specific target.

AND FIX EVERY SOURCE OF RANDOMNESS you can control:
environment seeds, network initialisation, action sampling,
and the framework's global RNG state. Then report what you
fixed, because full determinism is usually unattainable."""),
  ("p", "<b>The interquartile mean and performance profiles are the "
        "field's own recommended practice</b>, with free tooling that "
        "computes them and produces the plots — <b>so adopting them "
        "costs essentially nothing</b> and immediately puts your results "
        "above the median standard. <b>Giving the concrete standard "
        "matters</b>, because vague calls for rigour do not change what "
        "people do and a specific checklist does."),

  ("h1", "3 &nbsp; The other confounds"),
  ("table", ["Confound", "Effect", "What to do about it"],
   [["<b>Implementation details</b>",
     "<b>Can exceed the algorithmic difference entirely</b> "
     "(Module 06 &sect;3's finding).",
     "<b>Match the details, or run both methods in one codebase</b> "
     "— which is what CleanRL and similar efforts exist for."],
    ["<b>Hyperparameter tuning effort</b>",
     "<b>Whoever tuned more wins</b>, independently of the method.",
     "<b>Give both methods an equal and reported search budget.</b>"],
    ["<b>Environment version</b>",
     "<b>Reward scales, termination conditions, and observation "
     "definitions change between library versions</b>, sometimes "
     "substantially.",
     "<b>State the exact version</b>, and never compare numbers across "
     "versions."],
    ["<b>Evaluation protocol</b>",
     "<b>Best checkpoint, final policy, and average over training give "
     "very different numbers.</b>",
     "<b>State which you used, and prefer the final policy or an average "
     "over the last portion of training.</b>"],
    ["<b>Selective task reporting</b>",
     "<b>Reporting the subset of tasks where your method wins.</b>",
     "<b>Report the whole benchmark suite</b>, including the tasks where "
     "you lose."]],
   [0.21, 0.38, 0.41]),
  ("p", "<b>'Best checkpoint over training' deserves special mention: it "
        "is a form of test-set selection</b> (CSCE 633 Module 03 "
        "&sect;3's leakage), because the checkpoint was chosen using the "
        "evaluation you are then reporting. <b>It is extremely common in "
        "this field and it inflates every number it touches</b> — "
        "and with &sect;1's variance, selecting the best of fifty "
        "checkpoints can manufacture an improvement from nothing."),

  ("break",),
  ("h1", "4 &nbsp; Reading the literature"),
  ("ul", ["<b>How many seeds, and is the spread shown?</b> <b>If fewer "
          "than five, or if only a mean is reported, the comparison is "
          "weak evidence</b> whatever the stated improvement.",
          "<b>Was the baseline tuned, by whom, and with what budget?</b> "
          "A baseline taken from another paper's reported number, run on a "
          "different codebase, is not a controlled comparison.",
          "<b>Is the claimed improvement larger than the seed "
          "spread?</b> <b>If not, it is not established</b> — and "
          "this single check disposes of a surprising number of "
          "results.",
          "<b>Is there a released implementation that reproduces the "
          "reported number?</b> <b>Frequently there is not</b>, and "
          "'code available' is not the same as 'code reproduces the "
          "figures'.",
          "<b>And does the method appear in anyone else's benchmarks a "
          "year later?</b> <b>Durable adoption by people with no stake "
          "in it is the strongest available evidence</b>, and "
          "<b>it is the most reliable single filter</b> — it costs "
          "one search, and methods that genuinely work get used while "
          "methods that do not quietly disappear."]),
  ("callout", "Why this module exists here and not as a footnote",
   ["<b>This course cannot teach you to evaluate reinforcement learning "
    "results without stating plainly that the field's standard practice "
    "has been inadequate</b> — and it would be a disservice to teach "
    "the algorithms and omit this.",
    "<b>It is improving.</b> The statistical tooling exists and is free, "
    "the variance measurements are published and well-cited, and major "
    "venues increasingly require seed counts and spread reporting.",
    "<b>And it is still common to encounter three-seed comparisons with "
    "confident claims</b>, which &sect;1's measurements say cannot be "
    "supported — so the calibrated response when reading is "
    "scepticism about the <i>specific comparison</i> rather than cynicism "
    "about the field.",
    "<b>So the practical instruction is simple:</b> <b>five seeds "
    "minimum, spread shown, baseline tuned equally, protocol and sample "
    "budget stated.</b> <b>Meet that standard and your results mean "
    "something regardless of what anyone else does</b> — which is "
    "this program's position throughout, and here it has unusually "
    "concrete numbers behind it."]),
 ],
 "resources": [
   ("Henderson et al. &mdash; Deep Reinforcement Learning That Matters "
    "(free)",
    "https://arxiv.org/abs/1709.06560",
    "<b>&sect;1's measurements</b>, including the same-algorithm "
    "split-group demonstration. Read this before trusting any "
    "comparison."),
   ("Agarwal et al. &mdash; Deep RL at the Edge of the Statistical "
    "Precipice (free)",
    "https://arxiv.org/abs/2108.13264",
    "<b>&sect;2's recommended statistics</b>, with the free Rliable "
    "library that computes interquartile means and performance "
    "profiles."),
   ("Engstrom et al. &mdash; Implementation Matters in Deep Policy "
    "Gradients (free)",
    "https://arxiv.org/abs/2005.12729",
    "<b>&sect;3's first row, measured</b> — the implementation "
    "confound isolated from the algorithmic one."),
   ("Jordan et al. &mdash; Evaluating the Performance of Reinforcement "
    "Learning Algorithms (free)",
    "https://arxiv.org/abs/2006.16958",
    "<b>A complete evaluation protocol</b>, including the "
    "hyperparameter-effort confound of &sect;3."),
 ],
 "exercises": [
   "<b>Run one algorithm with ten seeds</b> on one task and plot all ten "
   "learning curves.",
   "<b>Split them into two groups of five</b> and compare the groups as "
   "if they were different methods. Report what you would have "
   "concluded.",
   "<b>Compute the mean, median, and interquartile mean</b> and report "
   "how much they differ.",
   "<b>Plot a performance profile</b> and identify whether the "
   "distribution is bimodal.",
   "<b>Compare an untuned baseline against your tuned method</b>, then "
   "tune the baseline equally and compare again.",
   "<b>Report the best checkpoint and the final policy</b> for the same "
   "runs, and report the inflation.",
   "<b>Run the same code on two environment library versions</b> and "
   "compare.",
   "<b>Take a published result</b> and apply &sect;4's five questions to "
   "it. Report your assessment.",
   "<b>Install Rliable</b> and reproduce its plots for your own "
   "results.",
   "<b>Write your project's results section</b> to &sect;2's standard.",
 ],
 "selfcheck": [
   "State the seed-variance finding and its magnitude.",
   "What can two groups of five seeds from one algorithm look like?",
   "Give four causes of the variance and identify the root one.",
   "Why is a mean with a standard deviation the wrong summary?",
   "Give the seven items in the reporting standard.",
   "Name five confounds beyond seeds.",
   "Why is 'best checkpoint' a leakage problem?",
   "Give five questions to ask of a published result.",
   "Which is the most reliable single filter, and why?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Where It Works",
 "subtitle": "The honest scope, and what to do with it.",
 "question": "After twelve modules, when should you actually use this?",
 "outcomes": [
     "State where reinforcement learning has demonstrably worked.",
     "Explain what those successes had in common.",
     "Explain why the same approach fails elsewhere.",
     "Choose between this course and CSCE 625 for a given problem.",
     "State what a reinforcement learning result can honestly "
     "promise.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The successes",
   "blurb": "What has actually worked, and what they share."},

  {"t": "table", "kicker": "Successes", "title": "Where it demonstrably works",
   "header": ["Domain", "What was achieved", "Enabling condition"],
   "widths": [2.6, 4.2, 5.2],
   "rows": [
     ["<b>Board games</b>", "<b>Superhuman, from self-play</b>", "<b>Perfect simulator; clear reward; self-play (M11)</b>"],
     ["<b>Video games</b>", "<b>Superhuman in several</b>", "<b>Fast simulator; enormous compute</b>"],
     ["<b>Simulated robotics</b>", "<b>Locomotion and manipulation</b>", "<b>Cheap samples; transfer with randomisation (M07)</b>"],
     ["<b>Chip and system tuning</b>", "<b>Placement, cooling, compilers</b>", "<b>Fast evaluator; clear objective</b>"],
     ["<b>LLM alignment</b>", "<b>RLHF — the largest deployment</b>", "<b>Cheap rollouts; learned reward (M10 §4)</b>"],
     ["<b>Recommendation</b>", "<b>Mostly bandits, honestly</b>", "<b>Huge traffic; short horizon</b>"],
   ],
   "footnote": "<b>Every row has a cheap, fast way to evaluate an "
               "action.</b> <b>That is the common condition</b>, and it "
               "is the one to check against your own problem first.",
   "note": "The shared condition is the single most useful conclusion of "
           "the course."},

  {"t": "callout", "title": "What the successes have in common",
   "kind": "Four conditions, and all four hold",
   "body": ["<b>A cheap, fast simulator or evaluator.</b> "
            "Module 01 §2's constraint, satisfied.",
            "<b>A reward that is genuinely what you want</b>, or a "
            "reward model you can keep correcting "
            "(Module 10).",
            "<b>A problem where no good hand-written policy existed</b> "
            "— so the comparison against CSCE 625 was lost "
            "honestly.",
            "<b>And a tolerance for occasional failure</b>, since there "
            "are no guarantees. <b>Check all four against your problem "
            "before committing; three of four is not enough.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Where it fails",
   "blurb": "And why, specifically."},

  {"t": "bullets", "kicker": "Failures", "title": "The failure conditions, each traceable",
   "items": [
     "<b>Real-world interaction is the binding cost.</b> Physical "
     "robots, clinical settings, anything with a per-step price. "
     "<b>Module 01 §2.</b>",
     "",
     "<b>The reward cannot be specified.</b> <b>Module 10's problem, "
     "and it is not a tooling gap.</b>",
     "",
     "<b>A guarantee is required.</b> Safety-critical control. "
     "<b>CSCE 625 gives guarantees and this course does not.</b>",
     "",
     "<b>A hand-written policy already works.</b> <b>Then the "
     "comparison is lost before it starts</b> — and this is more "
     "common than the literature suggests.",
     "",
     "<b>And the decisions are independent.</b> <b>That is supervised "
     "learning or a bandit, both far easier</b> "
     "(Module 02 §1).",
   ],
   "footnote": "<b>Each failure is traceable to a specific missing "
               "condition from Part 1</b>, which means the assessment is "
               "a checklist rather than a judgement."},

  {"t": "section", "label": "Part 3", "title": "This course or CSCE 625",
   "blurb": "The decision, made concrete."},

  {"t": "table", "kicker": "Choosing", "title": "Reinforcement learning or classical AI",
   "header": ["", "CSCE 625", "This course"],
   "widths": [2.3, 4.4, 5.3],
   "rows": [
     ["<b>Needs</b>", "<b>A model of the dynamics</b>", "<b>Interaction, in enormous quantity</b>"],
     ["<b>Gives</b>", "<b>Optimality, proofs, microsecond runtime</b>", "<b>A policy, and no guarantees</b>"],
     ["<b>Debugging</b>", "<b>Trace the search</b>", "<b>Seeds, curves, and patience</b>"],
     ["<b>Handles</b>", "<b>Known, crisp dynamics</b>", "<b>Unknown or unwritable dynamics</b>"],
     ["<b>Designer control</b>", "<b>Direct</b>", "<b>Through the reward, indirectly</b>"],
     ["<b>Try first</b>", "<b>Yes</b>", "<b>When the first column fails</b>"],
   ],
   "footnote": "<b>'Try CSCE 625 first' is the recommendation</b>, and "
               "it is not a hedge — <b>most sequential decision "
               "problems that look like reinforcement learning are "
               "planning problems with an unmeasured model.</b>",
   "note": "Ending with a clear ordering is the useful thing to do."},

  {"t": "callout", "title": "And the hybrid is usually right",
   "kind": "The practical architecture",
   "body": ["<b>Learn what cannot be written and compute what "
            "can.</b> <b>Learn a dynamics model, then plan with "
            "it</b> (Module 08) — which is the most reliable "
            "combination.",
            "<b>Or learn a value function or heuristic and use it "
            "inside a classical search</b> — which is AlphaZero, and "
            "CSCE 625 M05 §3's synthesis.",
            "<b>Or learn perception and plan over the result</b>, which "
            "is CSCE 753 Module 13 §2's division.",
            "<b>In every case the learned part supplies what nobody "
            "could write, and the structured part supplies the "
            "guarantees</b> — <b>which is the same conclusion all "
            "three courses this semester reached independently.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Claiming honestly",
   "blurb": "The course, the semester, and the program's rule."},

  {"t": "bullets", "kicker": "Claims", "title": "What a reinforcement learning result can honestly promise",
   "items": [
     "<b>'Mean return 312, interquartile mean 298, across ten seeds, "
     "after 5M environment steps; four of ten seeds failed to "
     "learn.'</b>",
     "",
     "<b>'It beats a tuned scripted baseline by 18% on this task, "
     "and loses to it on two of the five others.'</b>",
     "",
     "<b>'Trained in simulation; real-system performance is 64% of "
     "simulated, measured over 40 trials.'</b>",
     "",
     "<b>'The reward is a proxy for X; the agent exploits it by Y, "
     "which we mitigated by Z and did not eliminate.'</b>",
     "",
     "<b>And what you cannot say: 'the agent learned to play'</b> "
     "— <b>unqualified, without the seeds, the budget, or the "
     "baseline.</b>",
   ],
   "footnote": "<b>Every honest claim here names the seeds, the budget, "
               "and the baseline</b>, because Module 12 established that "
               "a claim without them is not assessable."},

  {"t": "callout", "title": "Where this course, and this semester, leave you",
   "kind": "Closing",
   "body": ["<b>You can implement and diagnose value-based and "
            "policy-gradient methods, choose between them, and recognise "
            "which leg of the deadly triad a method reintroduces.</b>",
            "<b>You can design a reward and anticipate how it will be "
            "gamed</b>, which is the skill with the most consequence in "
            "this course.",
            "<b>And you can evaluate a result to a standard the field "
            "frequently does not meet</b> — five seeds, spread shown, "
            "baseline tuned.",
            "<b>Semester 7 was perception, reasoning, and "
            "learning-to-act:</b> <b>CSCE 753 recovered the world from "
            "images, CSCE 625 decided what to do with a known model, and "
            "this course learned what to do without one.</b> <b>And the "
            "closing rule has not changed in twenty-one courses: state "
            "what you measured, state what you assumed, and never claim "
            "more than you established.</b>"]},
 ],
 "takeaways": [
   "Every demonstrated success has a cheap, fast way to evaluate an "
   "action, and that is the condition to check against your own problem.",
   "The four conditions are a cheap simulator, a specifiable reward, no "
   "good hand-written policy, and tolerance for occasional failure — "
   "and three of four is not enough.",
   "Each failure condition is traceable to a specific missing condition, "
   "which makes the assessment a checklist rather than a judgement.",
   "Try CSCE 625 first: most sequential decision problems that look like "
   "reinforcement learning are planning problems with an unmeasured "
   "model.",
   "The hybrid is usually right — learn what cannot be written and "
   "compute what can.",
   "Every honest claim names the seeds, the sample budget, and the "
   "baseline, because without them it is not assessable.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Where it demonstrably works"),
  ("table", ["Domain", "What was achieved", "The enabling condition"],
   [["<b>Board games</b>",
     "<b>Superhuman in Go, chess, and shogi from self-play alone.</b>",
     "<b>A perfect, fast simulator; an unambiguous reward; and "
     "self-play's automatic curriculum</b> (Module 11 &sect;2)."],
    ["<b>Video games</b>",
     "<b>Superhuman in several, including StarCraft II and Dota 2.</b>",
     "<b>A fast simulator and enormous compute</b> — tens of "
     "thousands of simulated years (Module 11's closing callout)."],
    ["<b>Simulated robotics</b>",
     "<b>Locomotion, dexterous manipulation, and some real transfer.</b>",
     "<b>Cheap samples in simulation, plus domain randomisation for "
     "transfer</b> (Module 07 &sect;4)."],
    ["<b>Chip placement, datacentre cooling, compiler tuning</b>",
     "<b>Real deployed improvements over hand-tuned heuristics.</b>",
     "<b>A fast evaluator and a clear scalar objective</b> — and "
     "these are the quietest and most convincing successes."],
    ["<b>Language model alignment</b>",
     "<b>RLHF — by far the largest deployment of anything in this "
     "course.</b>",
     "<b>Cheap rollouts (text generation) and a learned reward model "
     "that can be continually corrected</b> (Module 10 &sect;4)."],
    ["<b>Recommendation and advertising</b>",
     "<b>Real value, and mostly from bandits rather than full "
     "reinforcement learning, honestly.</b>",
     "<b>Huge traffic and a short effective horizon</b> — which is "
     "Module 02 &sect;1's point about not using an MDP where a bandit "
     "suffices."]],
   [0.21, 0.36, 0.43]),
  ("callout", "What the successes have in common",
   ["<b>A cheap, fast simulator or evaluator.</b> <b>Module 01 "
    "&sect;2's binding constraint, satisfied</b> — and it is "
    "satisfied in every single row of the table, which is the most useful "
    "observation in this module.",
    "<b>A reward that is genuinely what you want</b> (a win, a measured "
    "latency, a placement score) <b>or a reward model you can keep "
    "correcting as the policy exploits it</b> (Module 10 &sect;4's "
    "continued collection).",
    "<b>A problem where no good hand-written policy existed</b> — "
    "so <b>the comparison against CSCE 625's methods was lost "
    "honestly</b> rather than never run. Note that chip placement and "
    "cooling had decades of hand-tuned heuristics, and the learned "
    "methods had to beat them.",
    "<b>And a tolerance for occasional failure</b>, since there are no "
    "guarantees (Module 01 &sect;1's table). <b>Check all four against "
    "your problem before committing, and note that three of four is not "
    "enough</b> — a problem with a perfect simulator, an "
    "unspecifiable reward, and a safety requirement is not a "
    "reinforcement learning problem however good the simulator is."]),

  ("h1", "2 &nbsp; Where it fails, and why"),
  ("ul", ["<b>Real-world interaction is the binding cost.</b> Physical "
          "robots learning on hardware, clinical decision-making, "
          "anything with a per-step monetary or safety price. "
          "<b>Module 01 &sect;2's sample counts make it "
          "infeasible</b>, and the responses are Module 08's model-based "
          "methods, Module 09's offline methods, or simulation "
          "transfer — all of which have their own requirements.",
          "<b>The reward cannot be specified.</b> <b>Module 10's "
          "problem, and it is not a tooling gap</b> — a learned "
          "reward model helps and is itself gameable, so the difficulty "
          "is relocated rather than removed.",
          "<b>A guarantee is required.</b> Safety-critical control, "
          "certification, anything with a regulator. <b>CSCE 625's "
          "methods give guarantees and this course's do not</b> "
          "(Module 01 &sect;1's table), and no amount of empirical "
          "validation substitutes for a proof when a proof is what is "
          "required.",
          "<b>A hand-written policy already works well.</b> <b>Then the "
          "comparison is lost before it starts</b> — and <b>this "
          "situation is considerably more common than the literature "
          "suggests</b>, because papers do not get written about problems "
          "where a scripted controller was adequate.",
          "<b>And the decisions are actually independent of each "
          "other.</b> <b>That is supervised learning or a contextual "
          "bandit, both far easier and better understood</b> "
          "(Module 02 &sect;1) — and a surprising amount of work "
          "framed as reinforcement learning falls here.",
          "<b>Each failure is traceable to a specific missing condition "
          "from &sect;1</b>, <b>which means the assessment is a "
          "checklist rather than a judgement</b> — and that is the "
          "practical form the honesty takes."]),

  ("break",),
  ("h1", "3 &nbsp; This course or CSCE 625"),
  ("table", ["", "CSCE 625 (classical)", "This course (learned)"],
   [["<b>Requires</b>", "<b>A model of the dynamics.</b>",
     "<b>Interaction, in enormous quantity.</b>"],
    ["<b>Provides</b>",
     "<b>Optimality, proofs, and microsecond runtime</b> (CSCE 625 "
     "Module 01 &sect;4).",
     "<b>A policy, and no guarantees of any kind.</b>"],
    ["<b>Debugging</b>",
     "<b>Trace the search — costs, heuristic values, the frontier.</b>",
     "<b>Seeds, learning curves, and patience</b> (Module 12)."],
    ["<b>Handles</b>", "<b>Known, crisp dynamics.</b>",
     "<b>Unknown dynamics, or dynamics nobody can write down.</b>"],
    ["<b>Designer control</b>",
     "<b>Direct — edit the heuristic, the tree, the costs.</b>",
     "<b>Indirect, through the reward</b> — which Module 10 "
     "establishes is an imprecise instrument."],
    ["<b>Try it first?</b>", "<b>Yes.</b>",
     "<b>When the first column has honestly failed.</b>"]],
   [0.18, 0.39, 0.43]),
  ("p", "<b>'Try CSCE 625 first' is the recommendation, and it is not a "
        "hedge.</b> <b>Most sequential decision problems that look like "
        "reinforcement learning problems are planning problems with an "
        "unmeasured model</b> — the dynamics are known or knowable, "
        "and nobody wrote them down. <b>Writing them down and planning is "
        "frequently a week's work against months of training</b>, and it "
        "produces something debuggable."),
  ("callout", "And the hybrid is usually right",
   ["<b>Learn what cannot be written and compute what can.</b> <b>Learn "
    "a dynamics model from interaction, then plan with it</b> "
    "(Module 08) — which is the most reliable combination and the "
    "one with the best sample efficiency.",
    "<b>Or learn a value function or heuristic and use it inside a "
    "classical search</b> — which is AlphaZero, and is CSCE 625 "
    "Module 05 &sect;3's synthesis: <b>MCTS with the part nobody could "
    "write supplied by learning.</b>",
    "<b>Or learn the perception and plan over its output</b>, which is "
    "CSCE 753 Module 13 &sect;2's division and is how every "
    "self-driving stack is built.",
    "<b>In every case the learned component supplies what nobody could "
    "write down, and the structured component supplies the guarantees, "
    "the speed, and the control.</b> <b>Which is the same conclusion all "
    "three courses this semester reached independently</b> — "
    "CSCE 753 Module 13, CSCE 625 Module 13, and this one — "
    "<b>and three independent arrivals at one conclusion is the strongest "
    "form of evidence this program produces.</b>"]),

  ("h1", "4 &nbsp; Claiming honestly"),
  ("ul", ["<b>'Mean return 312, interquartile mean 298, across ten seeds, "
          "after 5M environment steps; four of the ten seeds failed to "
          "learn the task at all.'</b> <b>The seeds, the budget, and the "
          "failure rate</b> — and the failure rate is the part that "
          "is almost always omitted and almost always matters.",
          "<b>'It beats a tuned scripted baseline by 18% on this task, "
          "and loses to that baseline on two of the five other tasks we "
          "tried.'</b> <b>The baseline tuned, and the losses "
          "reported</b> (Module 12 &sect;3).",
          "<b>'Trained in simulation; real-system performance is 64% of "
          "simulated, measured over 40 physical trials.'</b> <b>The "
          "reality gap quantified</b> (Module 07 &sect;4), which is "
          "the only number that matters for a physical system.",
          "<b>'The reward is a proxy for X; the agent exploits it by "
          "doing Y, which we mitigated by Z and did not eliminate.'</b> "
          "<b>The specification gaming named rather than hidden</b> "
          "(Module 10) — and <b>'did not eliminate' is the honest "
          "ending</b>, because it rarely is eliminated.",
          "<b>And what you cannot honestly say: 'the agent learned to "
          "play the game'</b> — unqualified, without the seed count, "
          "the sample budget, or the baseline. <b>Every honest claim here "
          "names all three, because Module 12 established that a claim "
          "without them is not assessable by anyone</b>, including by "
          "you."]),
  ("callout", "Where this course, and this semester, leave you",
   ["<b>You can implement and diagnose value-based and policy-gradient "
    "methods, choose between them from the problem's properties, and "
    "recognise which leg of the deadly triad a given method "
    "reintroduces</b> — which is the diagnostic skill that makes the "
    "algorithm zoo navigable rather than memorised.",
    "<b>You can design a reward and anticipate how it will be gamed</b>, "
    "which is <b>the skill in this course with the most consequence</b> "
    "and the one that transfers furthest beyond it.",
    "<b>And you can evaluate a result to a standard the field "
    "frequently does not meet</b> — five seeds, spread shown, "
    "baseline tuned equally, protocol and budget stated — which "
    "<b>also means you can read the literature and tell which claims are "
    "supported.</b>",
    "<b>Semester 7 was perception, reasoning, and learning to act.</b> "
    "<b>CSCE 753 recovered the world from images; CSCE 625 decided what "
    "to do given a known model; and this course learned what to do "
    "without one.</b> <b>And the closing rule has not changed across "
    "twenty-one courses: state what you measured, state what you assumed, "
    "and never claim more than you established.</b> <b>In reinforcement "
    "learning it means naming the seeds</b> — because without them, "
    "Module 12 says, you have not measured anything."]),
 ],
 "resources": [
   ("Irpan &mdash; Deep Reinforcement Learning Doesn't Work Yet (free)",
    "https://www.alexirpan.com/2018/02/14/rl-hard.html",
    "<b>The honest assessment that this module's &sect;2 follows</b>, by "
    "a practitioner. Dated in its examples and not in its "
    "reasoning."),
   ("Dulac-Arnold et al. &mdash; Challenges of Real-World "
    "Reinforcement Learning (free)",
    "https://arxiv.org/abs/1904.12901",
    "<b>&sect;2's failure conditions, enumerated systematically</b>, with "
    "the gap between benchmark and deployment settings made explicit."),
   ("Mirhoseini et al. &mdash; A graph placement methodology for fast "
    "chip design (free)",
    "https://www.nature.com/articles/s41586-021-03544-2",
    "<b>&sect;1's chip placement row</b> — and worth reading "
    "alongside its published critiques, as an exercise in Module 12 "
    "&sect;4's questions."),
   ("Sutton & Barto &mdash; chapters 16–17 (free PDF)",
    "http://incompleteideas.net/book/the-book.html",
    "<b>Case studies and frontiers</b>, and a reasonable place to choose "
    "what to study next."),
 ],
 "exercises": [
   "<b>Check your project's problem against &sect;1's four "
   "conditions</b> and report how many hold.",
   "<b>For any that do not, identify which failure in &sect;2 "
   "applies.</b>",
   "<b>Build the CSCE 625 solution to your problem</b> — scripted, "
   "planned, or searched — and measure it.",
   "<b>Compare your trained agent against it</b> honestly, across five "
   "seeds.",
   "<b>Estimate what a model-based approach would cost</b> in samples, "
   "from Module 08's figures.",
   "<b>Design a hybrid</b> for your problem and state which part is "
   "learned and why.",
   "<b>Take one result from &sect;1's table</b> and find its sample and "
   "compute budget. Report it.",
   "<b>Write your project's claim</b> in the form of &sect;4's list.",
   "<b>Revisit what you wrote in Module 01's last exercise</b> and report "
   "what changed.",
   "<b>Project 2 is now due.</b> Submit the agent, the state/action/"
   "reward design, the non-learned baseline, five-seed results with "
   "spread, the reward-gaming behaviour you found, the shifted-environment "
   "evaluation, and a written answer to whether reinforcement learning was "
   "the right tool.",
 ],
 "selfcheck": [
   "Name six domains where reinforcement learning works and the enabling "
   "condition of each.",
   "What do all of them have in common?",
   "State the four conditions, and why three of four is insufficient.",
   "Name five failure conditions and trace each to a missing "
   "condition.",
   "Compare CSCE 625 and this course on six axes.",
   "Why is 'try CSCE 625 first' not a hedge?",
   "Give three hybrid architectures and the division in each.",
   "Give four honest claims and the thing you cannot say.",
   "What does 'state what you assumed' mean in this course "
   "specifically?",
 ],
},

]
