# -*- coding: utf-8 -*-
"""CSCE 642 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Exploration",
 "subtitle": "You cannot learn about what you never try.",
 "question": "How should an agent balance using what it knows against "
             "finding out more?",
 "outcomes": [
     "Explain the bandit problem and why it is the right starting "
     "point.",
     "Compare the standard exploration strategies.",
     "Explain optimism in the face of uncertainty.",
     "Explain why deep exploration is harder than action noise.",
     "Explain intrinsic motivation and its failure mode.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Bandits",
   "blurb": "The problem with exploration and nothing else."},

  {"t": "callout", "title": "A bandit is reinforcement learning with the sequential part removed",
   "kind": "Why start here",
   "body": ["<b>k actions, each with an unknown reward distribution, no "
            "state, and no consequences.</b> Pull, observe, repeat.",
            "<b>So the <i>only</i> difficulty is exploration</b> "
            "— which makes it the right place to study exploration "
            "in isolation, with actual theory available.",
            "<b>The measure is <i>regret</i>:</b> the cumulative "
            "difference between what you got and what the best fixed "
            "action would have given.",
            "<b>And a great deal of real work is a bandit rather than "
            "an MDP</b> — which advert to show, which layout to "
            "serve. <b>If your actions have no lasting consequences, do "
            "not use an MDP</b> (M01 §4)."]},

  {"t": "table", "kicker": "Strategies", "title": "The standard exploration strategies",
   "header": ["Strategy", "How", "Property"],
   "widths": [2.6, 4.2, 5.2],
   "rows": [
     ["<b>ε-greedy</b>", "<b>Random with probability ε</b>", "<b>Linear regret at fixed ε; decay it</b>"],
     ["<b>Optimistic init</b>", "<b>Start every value too high</b>", "<b>Free, and surprisingly effective</b>"],
     ["<b>UCB</b>", "<b>Mean + c·√(ln N / n)</b>", "<b>Logarithmic regret — provably near-optimal</b>"],
     ["<b>Thompson sampling</b>", "<b>Sample from the posterior, act greedily</b>", "<b>Logarithmic regret; often best in practice</b>"],
     ["<b>Boltzmann</b>", "Sample proportional to exp(Q/τ)", "<b>Temperature is hard to set across scales</b>"],
   ],
   "footnote": "<b>UCB is the same formula as CSCE 625 "
               "§05's MCTS selection step</b> — the same "
               "problem, so the same solution, which is worth noticing "
               "rather than rediscovering.",
   "note": "The UCB/MCTS identity is the connection to make."},

  {"t": "section", "label": "Part 2", "title": "Optimism",
   "blurb": "The principle behind the good strategies."},

  {"t": "callout", "title": "Optimism in the face of uncertainty",
   "kind": "The one idea worth carrying",
   "body": ["<b>Act as though every uncertain option is as good as it "
            "plausibly could be.</b> Then either it is good (you gain) or "
            "you learn it is not (you gain information).",
            "<b>Either way the optimism is self-correcting</b>, and "
            "<b>the agent never persistently avoids something it has not "
            "tried</b> — which is &epsilon;-greedy's actual failure.",
            "<b>UCB implements it explicitly</b> through the "
            "confidence-width term: rarely-tried actions get a large "
            "bonus that shrinks as they are sampled.",
            "<b>And it is why optimistic initialisation works at all:</b> "
            "<b>a value function initialised too high makes every "
            "unvisited state attractive</b>, so exploration is driven by "
            "the value function rather than bolted on beside it."]},

  {"t": "section", "label": "Part 3", "title": "Deep exploration",
   "blurb": "Why random actions are not enough."},

  {"t": "code", "kicker": "Deep exploration", "title": "The corridor: what action noise cannot solve",
   "lang": "text", "code": """
  A CORRIDOR of length n. Reward only at the far end.
  Actions: left, right.

  WITH EPSILON-GREEDY from a zero-initialised Q:
      the agent performs a RANDOM WALK until it stumbles on
      the reward. Expected time is O(2^n) -- exponential in
      the corridor length.

  THE PROBLEM IS NOT INSUFFICIENT RANDOMNESS. It is that
  REACHING THE REWARD REQUIRES A LONG COHERENT SEQUENCE of
  the same choice, and independent per-step noise destroys
  coherence by construction. MORE NOISE MAKES IT WORSE.

  This is called DEEP EXPLORATION, and it is the open
  problem of the field.
""",
   "caption": "<b>Randomness must be coherent over time to explore "
              "deeply</b> — and per-step action noise is coherent "
              "over exactly one step.",
   "note": "The corridor example makes the exponential cost "
           "unmistakable."},

  {"t": "code", "kicker": "Partial answers", "title": "And what partly works",
   "lang": "text", "code": """
  BOOTSTRAPPED DQN / RANDOMISED VALUE FUNCTIONS
      sample a Q-function from an approximate posterior at
      the START OF EACH EPISODE and follow it greedily.
      The randomness is now PER-EPISODE, so behaviour is
      coherent within an episode. Thompson sampling,
      lifted to MDPs.

  PARAMETER-SPACE NOISE
      perturb the policy's WEIGHTS rather than its actions.
      One perturbation, one coherent behaviour.

  COUNT-BASED OR CURIOSITY BONUSES
      reward visiting rarely-seen states (Part 4), so
      exploration becomes DIRECTED rather than random.

  OPTIONS / TEMPORALLY EXTENDED ACTIONS
      make the coherent sequence a SINGLE action, so no
      coherence has to be maintained at all.

  AND NONE OF THEM SOLVES MONTEZUMA'S REVENGE WITHOUT
  DEMONSTRATIONS OR HAND-DESIGNED HELP, which is the
  honest status of the problem.
""",
   "caption": "<b>Every one of the four makes the randomness coherent "
              "over a longer span</b>, which is the common structure and "
              "the thing to remember.",
   "note": "Naming the common structure beats listing four methods."},

  {"t": "section", "label": "Part 4", "title": "Intrinsic motivation",
   "blurb": "Rewarding novelty, and what goes wrong."},

  {"t": "callout", "title": "Intrinsic reward, and the noisy-TV problem",
   "kind": "The approach and its characteristic failure",
   "body": ["<b>Add a bonus for visiting states that are novel</b> "
            "— measured by a visit count, a hash-based "
            "pseudo-count, or the prediction error of a learned "
            "model.",
            "<b>It works, and it is the best available answer for "
            "sparse-reward tasks</b> — curiosity-driven agents reach "
            "rewards that &epsilon;-greedy never finds.",
            "<b>And the failure is the noisy TV:</b> <b>a source of "
            "genuine randomness is permanently 'novel', because the "
            "prediction error never falls</b> — so the agent sits in "
            "front of it forever.",
            "<b>Random network distillation addresses it</b> by "
            "predicting a <i>fixed random network's</i> output, which is "
            "deterministic given the state — <b>so the error falls "
            "with familiarity and not with predictability.</b> <b>A "
            "neat fix for a specific, real failure.</b>"]},

  {"t": "bullets", "kicker": "Practice", "title": "Exploration in practice",
   "items": [
     "<b>Start with ε-greedy decayed to a small floor</b>, or "
     "with the entropy bonus of Module 07. <b>It is usually "
     "enough.</b>",
     "",
     "<b>Diagnose before escalating:</b> <b>plot state visitation</b>. "
     "<b>If the agent never reaches the rewarding region, exploration is "
     "the problem</b>; if it reaches it and does not learn, it is not.",
     "",
     "<b>Prefer fixing the reward over fixing the exploration.</b> "
     "<b>A denser reward is usually cheaper than a better explorer</b> "
     "— with Module 10's warning attached.",
     "",
     "<b>Then try per-episode coherent noise</b> before "
     "count-based bonuses, which add a hyperparameter and a failure "
     "mode.",
     "",
     "<b>And log the exploration parameter.</b> <b>A collapsed "
     "entropy or a decayed ε explains a plateau immediately.</b>",
   ],
   "footnote": "<b>The visitation plot is the diagnostic.</b> It "
               "separates 'cannot find the reward' from 'cannot learn "
               "from it', which call for completely different fixes."},
 ],
 "takeaways": [
   "A bandit is reinforcement learning with the sequential part removed, "
   "so exploration can be studied with actual theory — and a great "
   "deal of real work is a bandit.",
   "UCB's formula is identical to CSCE 625's MCTS selection step, because "
   "it is the same problem.",
   "Optimism in the face of uncertainty is self-correcting: the agent "
   "never persistently avoids what it has not tried.",
   "Deep exploration needs a long coherent action sequence, which "
   "independent per-step noise destroys by construction.",
   "So per-episode and parameter-space noise beat per-step action noise, "
   "and none of it solves the hardest sparse-reward tasks unaided.",
   "The noisy-TV problem is that genuine randomness is permanently novel, "
   "and random network distillation fixes it by predicting a fixed "
   "network.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Bandits"),
  ("callout", "A bandit is reinforcement learning with the sequential part "
              "removed",
   ["<b>k actions, each with an unknown reward distribution, no state, and "
    "no consequences carried forward.</b> Pull an arm, observe a reward, "
    "repeat — and nothing you did earlier changes what the actions "
    "now do.",
    "<b>So the <i>only</i> difficulty is exploration.</b> <b>Which makes "
    "the bandit the right place to study exploration in isolation</b>, "
    "and it is the one part of this subject with substantial theory and "
    "provably near-optimal algorithms.",
    "<b>The measure is <i>regret</i>:</b> the cumulative difference "
    "between the reward you obtained and the reward the single best fixed "
    "action would have given over the same horizon. <b>Logarithmic regret "
    "is the best achievable</b>, and &sect;1's table says which "
    "strategies attain it.",
    "<b>And a great deal of real applied work is a bandit rather than a "
    "full MDP</b> — which advert to show, which layout to serve, "
    "which of five treatments to assign. <b>If your actions have no "
    "lasting consequences for the environment's state, do not use an "
    "MDP</b> (Module 01 &sect;4): a contextual bandit is far easier, "
    "has theory, and will work."]),
  ("table", ["Strategy", "How it works", "Property"],
   [["<b>&epsilon;-greedy</b>",
     "<b>Act greedily, but take a uniformly random action with "
     "probability &epsilon;.</b>",
     "<b>Linear regret at a fixed &epsilon;</b> — because it keeps "
     "exploring forever at a constant rate. <b>Decay &epsilon;</b>, and "
     "the Robbins–Monro reasoning of CSCE 669 Module 08 "
     "&sect;2 applies to the schedule."],
    ["<b>Optimistic initialisation</b>",
     "<b>Initialise every action's estimated value well above any "
     "achievable reward.</b>",
     "<b>Free, requires no extra machinery, and is surprisingly "
     "effective</b> — see &sect;2's explanation of why."],
    ["<b>Upper confidence bound (UCB)</b>",
     "<b>Choose the action maximising mean + c&middot;&radic;(ln N / "
     "n)</b>, where n is that action's count and N the total.",
     "<b>Logarithmic regret — provably near-optimal.</b> <b>The "
     "same formula as CSCE 625 Module 05 &sect;3's MCTS selection "
     "step</b>, because it is the same problem."],
    ["<b>Thompson sampling</b>",
     "<b>Maintain a posterior over each action's value, sample one value "
     "from each, and act greedily on the samples.</b>",
     "<b>Logarithmic regret, and frequently the best in practice</b> "
     "— and it is the cleanest expression of &sect;2's principle."],
    ["<b>Boltzmann / softmax</b>",
     "Sample actions with probability proportional to exp(Q/&tau;).",
     "<b>The temperature &tau; is hard to set</b>, because the right "
     "value depends on the scale of Q, which changes during "
     "learning."]],
   [0.21, 0.38, 0.41]),

  ("h1", "2 &nbsp; Optimism"),
  ("callout", "Optimism in the face of uncertainty",
   ["<b>Act as though every uncertain option is as good as it plausibly "
    "could be.</b> Then one of two things happens: the option really is "
    "good, and you gain reward; or it is not, and you learn that, which "
    "is information you needed.",
    "<b>Either way the optimism is self-correcting</b> — an "
    "overestimate survives only until the action is tried enough times "
    "— <b>and the agent never persistently avoids something it has "
    "not tried</b>. <b>Which is exactly &epsilon;-greedy's real "
    "failure:</b> it explores uniformly at random, so it keeps retrying "
    "actions it has already established are bad, and gives a "
    "never-tried action no more attention than a known-bad one.",
    "<b>UCB implements the principle explicitly</b> through the "
    "confidence-width term: an action tried twice gets a large bonus and "
    "an action tried ten thousand times gets almost none, so the bonus is "
    "literally an uncertainty estimate.",
    "<b>And it explains why optimistic initialisation works at all.</b> "
    "<b>A value function initialised above every achievable value makes "
    "every unvisited state attractive</b>, so <b>exploration is driven by "
    "the value function itself rather than bolted on beside it</b> "
    "— which means the exploration is <i>directed</i> toward what "
    "has not been seen, rather than being uniform noise. <b>That "
    "distinction is the whole content of &sect;3.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Deep exploration"),
  ("code", """A CORRIDOR of length n. Reward only at the far end.
Actions: left, right.

WITH EPSILON-GREEDY from a zero-initialised Q:
    the agent performs a RANDOM WALK until it stumbles onto
    the reward. The expected time is O(2^n) -- exponential
    in the corridor length.

THE PROBLEM IS NOT INSUFFICIENT RANDOMNESS. It is that
REACHING THE REWARD REQUIRES A LONG COHERENT SEQUENCE of
the same choice, and INDEPENDENT PER-STEP NOISE DESTROYS
COHERENCE BY CONSTRUCTION. More noise makes it worse.

THIS IS CALLED DEEP EXPLORATION, and it is the open problem
of the field.

PARTIAL ANSWERS
  bootstrapped DQN / randomised value functions
      sample a Q-function from an approximate posterior at
      the START OF EACH EPISODE and follow it greedily. The
      randomness is now PER-EPISODE, so the behaviour is
      coherent within an episode and different between
      episodes. This is Thompson sampling, lifted to MDPs.
  parameter-space noise
      perturb the policy's WEIGHTS rather than its actions.
      Same reasoning: one perturbation produces one
      coherent behaviour.
  count-based or curiosity bonuses
      reward visiting rarely-seen states (section 4), so
      exploration becomes directed rather than random.
  options / temporally extended actions
      make the coherent sequence a SINGLE action, so no
      coherence has to be maintained at all.

AND NONE OF THEM SOLVES MONTEZUMA'S REVENGE WITHOUT
DEMONSTRATIONS OR HAND-DESIGNED HELP, which is the honest
status of the problem."""),
  ("p", "<b>Randomness must be coherent over time to explore deeply</b>, "
        "and that single observation explains why per-episode and "
        "parameter-space noise outperform per-step action noise despite "
        "being less random in total. <b>It also explains why "
        "&sect;2's optimism matters so much:</b> an optimistic value "
        "function produces coherent directed behaviour (go to the "
        "unexplored place, consistently) rather than noise, which is the "
        "property the corridor needs."),

  ("h1", "4 &nbsp; Intrinsic motivation"),
  ("callout", "Intrinsic reward, and the noisy-TV problem",
   ["<b>Add a bonus to the reward for visiting states that are "
    "novel</b> — measured by an explicit visit count in small "
    "domains, a hash-based pseudo-count in large ones, or the prediction "
    "error of a learned dynamics model, on the reasoning that error is "
    "high where experience is scarce.",
    "<b>It works, and it is the best available answer for "
    "sparse-reward tasks</b> — curiosity-driven agents reach rewards "
    "that &epsilon;-greedy provably never finds (&sect;3), and the "
    "improvement on hard exploration games is large.",
    "<b>And the characteristic failure is the noisy TV.</b> <b>A source "
    "of genuine, irreducible randomness in the environment — a "
    "static-filled screen, a random number display, leaves moving in wind "
    "— is permanently 'novel' under a prediction-error measure, "
    "because the prediction error never falls however long you "
    "watch.</b> <b>So the agent sits in front of it forever, maximally "
    "curious and entirely useless.</b>",
    "<b>Random network distillation addresses it neatly</b>: predict the "
    "output of a <i>fixed, randomly initialised</i> network applied to the "
    "state. <b>That target is deterministic given the state</b>, so the "
    "prediction error falls with <i>familiarity</i> and not with "
    "<i>predictability</i> — and a noisy TV becomes familiar even "
    "though it stays unpredictable. <b>A clean fix for a specific real "
    "failure</b>, and a good example of diagnosing a failure precisely "
    "enough that the remedy follows."]),
  ("ul", ["<b>Start with &epsilon;-greedy decayed to a small floor, or "
          "with the entropy bonus of Module 07 &sect;3.</b> <b>It is "
          "usually enough</b>, and the elaborate methods are for tasks "
          "that demonstrably need them.",
          "<b>Diagnose before escalating.</b> <b>Plot state "
          "visitation.</b> <b>If the agent never reaches the rewarding "
          "region at all, exploration is the problem; if it reaches it "
          "regularly and still does not improve, exploration is not the "
          "problem</b> and you are looking at a learning or credit-"
          "assignment failure (Module 04). <b>These two cases call for "
          "completely different fixes and are routinely confused.</b>",
          "<b>Prefer fixing the reward over fixing the explorer.</b> "
          "<b>A denser reward signal is usually far cheaper than a better "
          "exploration algorithm</b> — with <b>Module 10's warning "
          "firmly attached</b>, because reward shaping is how agents learn "
          "to do the wrong thing efficiently.",
          "<b>Then try per-episode coherent noise</b> (&sect;3) before "
          "count-based bonuses, which add a hyperparameter, a second "
          "network, and the failure mode above.",
          "<b>And log the exploration parameter every run.</b> <b>A "
          "collapsed policy entropy or a fully decayed &epsilon; explains "
          "a performance plateau immediately</b>, and is otherwise one of "
          "the hardest things to notice from a learning curve alone."]),
 ],
 "resources": [
   ("Sutton & Barto &mdash; chapter 2 (free PDF)",
    "http://incompleteideas.net/book/the-book.html",
    "<b>Bandits, &sect;1's strategies, and the regret framing</b>, with "
    "the experiments worth reproducing."),
   ("Lattimore & Szepesvári &mdash; Bandit Algorithms (free PDF)",
    "https://tor-lattimore.com/downloads/book/book.pdf",
    "<b>Free in full, and the reference for &sect;1 and &sect;2</b> "
    "— the UCB and Thompson sampling analyses done properly."),
   ("Osband et al. &mdash; Deep Exploration via Bootstrapped DQN "
    "(free)",
    "https://arxiv.org/abs/1602.04621",
    "<b>&sect;3's corridor argument and the per-episode randomisation "
    "answer</b>, from the paper that framed deep exploration clearly."),
   ("Burda et al. &mdash; Exploration by Random Network Distillation "
    "(free)",
    "https://arxiv.org/abs/1810.12894",
    "<b>&sect;4's fix for the noisy-TV problem</b>, with the diagnosis "
    "that motivates it."),
 ],
 "exercises": [
   "<b>Implement a 10-armed bandit</b> and compare all five strategies "
   "from &sect;1 over 2000 steps, averaged over 100 runs.",
   "<b>Plot cumulative regret</b> and confirm &epsilon;-greedy's is "
   "linear and UCB's logarithmic.",
   "<b>Implement optimistic initialisation</b> and report how long the "
   "optimism takes to wash out.",
   "<b>Implement Thompson sampling</b> and compare against UCB.",
   "<b>Build the corridor of &sect;3</b> at n = 5, 10, 20 and measure "
   "&epsilon;-greedy's steps to first reward.",
   "<b>Confirm the exponential scaling</b> and show that increasing "
   "&epsilon; makes it worse.",
   "<b>Implement per-episode randomised value functions</b> and report "
   "the improvement on the same corridor.",
   "<b>Add a count-based bonus</b> and compare.",
   "<b>Build a noisy TV</b> into an environment and confirm a "
   "prediction-error bonus traps the agent.",
   "<b>Implement random network distillation</b> and confirm it does "
   "not.",
 ],
 "selfcheck": [
   "What is a bandit, and why is it the right place to study "
   "exploration?",
   "Define regret and state the best achievable rate.",
   "Compare five exploration strategies.",
   "Where else in this program does UCB's formula appear?",
   "State the optimism principle and explain why it is "
   "self-correcting.",
   "What is &epsilon;-greedy's real failure?",
   "Why does per-step noise fail on the corridor, and what does the "
   "corridor cost?",
   "Name four partial answers to deep exploration.",
   "What is the noisy-TV problem and how does RND fix it?",
   "What does a state-visitation plot distinguish?",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Learning Values from Experience",
 "subtitle": "Temporal difference, and the on/off-policy distinction.",
 "question": "How do you improve a value estimate from a single "
             "transition?",
 "outcomes": [
     "Derive the temporal-difference update.",
     "Compare Monte Carlo and temporal-difference learning.",
     "Distinguish on-policy from off-policy and demonstrate the "
     "difference.",
     "Explain n-step returns and eligibility traces.",
     "Explain maximisation bias and double learning.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Temporal difference",
   "blurb": "Bootstrap from your own estimate."},

  {"t": "eq", "kicker": "TD", "title": "The update, and what is remarkable about it",
   "eqs": [
     ("V(s) ← V(s) + α [ r + γV(s′) − V(s) ]",
      "Move the estimate toward the observed reward plus the discounted "
      "estimate of where you landed."),
     ("The bracket is the TD ERROR",
      "The discrepancy between your prediction and a one-step-better "
      "prediction. Learning is driven by surprise."),
     ("It learns from ONE transition, without waiting for the episode "
      "to end",
      "Which is what makes it usable online, in continuing tasks, and "
      "in long episodes."),
   ],
   "caption": "<b>It updates a guess toward another guess</b>, which "
              "sounds unsound and converges — because the second "
              "guess is anchored by a real observed reward.",
   "note": "The 'guess toward a guess' framing is the thing students "
           "find strange and should."},

  {"t": "table", "kicker": "Comparison", "title": "Monte Carlo against temporal difference",
   "header": ["", "Monte Carlo", "Temporal difference"],
   "widths": [2.3, 4.5, 5.2],
   "rows": [
     ["<b>Target</b>", "<b>The actual return to the end of the episode</b>", "<b>r + γV(s′) — bootstrapped</b>"],
     ["<b>Bias</b>", "<b>Unbiased</b>", "<b>Biased while V is wrong</b>"],
     ["<b>Variance</b>", "<b>High — the whole episode's randomness</b>", "<b>Low — one step's randomness</b>"],
     ["<b>Needs</b>", "<b>Episodes to terminate</b>", "<b>Nothing. Works online and continually</b>"],
     ["<b>Markov</b>", "Does not rely on it", "<b>Relies on it</b>"],
   ],
   "footnote": "<b>It is a bias-variance trade</b> (CSCE 633 M03) "
               "<b>and n-step returns interpolate between the two</b> "
               "— with the best n almost always strictly between 1 "
               "and the episode length.",
   "note": "Framing n-step as the interpolation makes it obvious rather "
           "than arbitrary."},

  {"t": "section", "label": "Part 2", "title": "On-policy and off-policy",
   "blurb": "The distinction with the clearest demonstration in the "
            "field."},

  {"t": "code", "kicker": "SARSA and Q-learning", "title": "One character apart, and completely different",
   "lang": "text", "code": """
  SARSA (on-policy):
      Q(s,a) <- Q(s,a) + a[ r + g*Q(s',a') - Q(s,a) ]
      where a' is the action ACTUALLY TAKEN next

  Q-LEARNING (off-policy):
      Q(s,a) <- Q(s,a) + a[ r + g*max_a' Q(s',a') - Q(s,a) ]
      where the max is over ALL available actions

  SARSA learns the value of THE POLICY IT IS FOLLOWING,
  exploration included. Q-learning learns the value of THE
  OPTIMAL POLICY, regardless of what it is actually doing.
""",
   "caption": "<b>One term differs, and the two algorithms answer "
              "different questions</b> — which the next slide makes "
              "visible.",
   "note": "Hold the two updates side by side before interpreting "
           "them."},

  {"t": "code", "kicker": "Cliff walking", "title": "The demonstration worth reproducing",
   "lang": "text", "code": """
  A grid with a cliff along the bottom row. The shortest
  path runs right along the cliff edge. The agent behaves
  EPSILON-GREEDILY throughout.

  Q-LEARNING learns the cliff-edge path -- correctly, since
      it IS optimal for a greedy policy -- and then FALLS
      OFF THE CLIFF REGULARLY, because epsilon occasionally
      steps sideways.

  SARSA learns a path one row further from the cliff, which
      is SUBOPTIMAL for a greedy policy and BETTER for the
      epsilon-greedy policy it is actually running, because
      that policy sometimes steps randomly and SARSA has
      accounted for it.

  SARSA ACHIEVES HIGHER ONLINE REWARD.
  Q-LEARNING ENDS WITH THE BETTER FINAL GREEDY POLICY.

  This is the clearest demonstration of the distinction
  that exists. Reproduce it once and it is permanent.
""",
   "caption": "<b>Off-policy learning is what allows replay and offline "
              "data</b> (Modules 04, 09) — and it is also where "
              "instability comes from.",
   "note": "Insist students reproduce cliff walking; it is worth the "
           "hour."},

  {"t": "section", "label": "Part 3", "title": "Credit over time",
   "blurb": "n-step returns and traces."},

  {"t": "callout", "title": "n-step returns, and why eligibility traces exist",
   "kind": "Interpolating the trade",
   "body": ["<b>An n-step return uses n real rewards and then "
            "bootstraps</b> — so n = 1 is TD and n = ∞ is "
            "Monte Carlo.",
            "<b>The best n is almost always strictly between</b>, and "
            "n = 3 to 5 is a common default. <b>It is the single "
            "cheapest improvement to a value-based agent.</b>",
            "<b>Eligibility traces (TD(λ)) average over all n "
            "at once</b>, implemented backwards with a decaying "
            "eligibility per state — so the cost is one pass rather "
            "than n.",
            "<b>And traces are less used in deep reinforcement learning "
            "than they deserve</b>, partly because replay buffers make "
            "the backward view awkward — which is an engineering "
            "accident rather than a result."]},

  {"t": "section", "label": "Part 4", "title": "Maximisation bias",
   "blurb": "Why Q-learning overestimates, systematically."},

  {"t": "callout", "title": "The max of noisy estimates is biased upward",
   "kind": "A real and fixable problem",
   "body": ["<b>Q-learning's target contains maxₐ Q(s′,a), and "
            "the maximum of several noisy estimates exceeds the maximum "
            "of their true values in expectation.</b>",
            "<b>So the bias is <i>systematic</i>, not noise</b>, and it "
            "propagates: an overestimated value becomes another state's "
            "target.",
            "<b>Double Q-learning fixes it</b> by using one estimator to "
            "<i>select</i> the maximising action and another to "
            "<i>evaluate</i> it — so the selection noise and the "
            "evaluation noise are independent.",
            "<b>And the same fix becomes Double DQN</b> "
            "(Module 04 §3), where it is one of the few "
            "modifications with an unambiguous, measurable, and "
            "well-understood benefit."]},

  {"t": "bullets", "kicker": "Summary", "title": "What to use, tabularly",
   "items": [
     "<b>Q-learning with n-step returns and double estimation</b> is "
     "the sensible tabular default.",
     "",
     "<b>SARSA when online performance during learning matters</b> "
     "— a real robot, or a deployed system.",
     "",
     "<b>Monte Carlo when episodes are short and the Markov property "
     "is doubtful</b>, since it does not rely on it.",
     "",
     "<b>And expected SARSA</b> — average over the policy rather "
     "than sampling a′ — <b>which has lower variance than "
     "SARSA at no extra cost.</b>",
     "",
     "<b>Everything here converges, tabularly.</b> <b>Module 04 is "
     "where that stops being true.</b>",
   ],
   "footnote": "<b>Implement all of these tabularly before Module 04.</b> "
               "<b>Every deep method is one of them with a network, and "
               "the bugs are far easier to find here.</b>"},
 ],
 "takeaways": [
   "Temporal difference moves an estimate toward a reward plus another "
   "estimate — a guess toward a guess, anchored by a real observed "
   "reward.",
   "Monte Carlo is unbiased with high variance; temporal difference is "
   "biased with low variance, and n-step returns interpolate.",
   "SARSA learns the value of the policy it is following including its "
   "exploration; Q-learning learns the optimal policy's value regardless.",
   "Cliff walking is the clearest demonstration: SARSA takes the safer "
   "path and gets more online reward, Q-learning the optimal path and "
   "falls off.",
   "Off-policy learning is what allows replay and offline data, and it is "
   "also where instability comes from.",
   "The max of noisy estimates is biased upward systematically, and double "
   "estimation fixes it by separating selection from evaluation.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Temporal-difference learning"),
  ("eq", "V(s) &larr; V(s) + &alpha; [ r + &gamma;V(s&prime;) &minus; "
         "V(s) ]"),
  ("p", "<b>Move the estimate toward the observed reward plus the "
        "discounted estimate of the state you landed in.</b> <b>The "
        "bracketed quantity is the TD error</b> — the discrepancy "
        "between your current prediction and a prediction that "
        "incorporates one step of real information — so <b>learning "
        "is driven by surprise</b>, and an accurate predictor stops "
        "updating. <b>It learns from a single transition without waiting "
        "for the episode to end</b>, which is what makes it usable "
        "online, in continuing tasks with no terminal state, and in "
        "episodes too long to wait out. <b>And it updates a guess toward "
        "another guess, which sounds unsound and nevertheless "
        "converges</b> (tabularly, with a decaying step size) — "
        "<b>because the second guess contains a real observed reward, so "
        "genuine information enters the system at every step and "
        "propagates backwards.</b>"),
  ("table", ["", "Monte Carlo", "Temporal difference"],
   [["<b>Target</b>",
     "<b>The actual return accumulated to the end of the episode.</b>",
     "<b>r + &gamma;V(s&prime;) — bootstrapped from the current "
     "estimate.</b>"],
    ["<b>Bias</b>", "<b>Unbiased — it is a sample of the true "
     "return.</b>",
     "<b>Biased while V is wrong</b>, and the bias shrinks as V "
     "improves."],
    ["<b>Variance</b>",
     "<b>High — the target contains every random event in the rest "
     "of the episode.</b>",
     "<b>Low — the target contains one step's randomness.</b>"],
    ["<b>Requires</b>", "<b>Episodes that terminate.</b>",
     "<b>Nothing. Works online, incrementally, and in continuing "
     "tasks.</b>"],
    ["<b>The Markov property</b>",
     "Does not rely on it — the return is the return.",
     "<b>Relies on it</b>, because V(s&prime;) is only a valid summary of "
     "the future if the state is sufficient."]],
   [0.16, 0.40, 0.44]),
  ("p", "<b>It is a bias-variance trade</b> (CSCE 633 Module 03 "
        "&sect;2) <b>and n-step returns interpolate between the two "
        "endpoints</b> (&sect;3) — <b>with the best n almost always "
        "strictly between 1 and the episode length</b>, which is the "
        "practical consequence and is why pure TD and pure Monte Carlo "
        "are both suboptimal defaults."),

  ("h1", "2 &nbsp; On-policy and off-policy"),
  ("code", """SARSA (on-policy):
    Q(s,a) <- Q(s,a) + a[ r + g*Q(s',a') - Q(s,a) ]
    where a' is the action ACTUALLY TAKEN next

Q-LEARNING (off-policy):
    Q(s,a) <- Q(s,a) + a[ r + g*max_a' Q(s',a') - Q(s,a) ]
    where the max is over ALL available actions

SARSA learns the value of THE POLICY IT IS FOLLOWING,
exploration included. Q-learning learns the value of THE
OPTIMAL POLICY, regardless of what it is actually doing.

THE CLIFF-WALKING DEMONSTRATION:
    a grid world with a cliff along the bottom row. The
    shortest path runs right along the cliff edge. The
    agent behaves epsilon-greedily throughout.

    Q-LEARNING learns the cliff-edge path -- correctly,
        since it IS optimal for a greedy policy -- and then
        FALLS OFF THE CLIFF REGULARLY, because epsilon
        occasionally steps sideways.
    SARSA learns a path one row further from the cliff,
        which is SUBOPTIMAL for a greedy policy and BETTER
        for the epsilon-greedy policy it is actually
        running, because that policy sometimes steps
        randomly and SARSA has accounted for it.

    SARSA ACHIEVES HIGHER ONLINE REWARD. Q-learning ends
    with the better final greedy policy.

THIS IS THE CLEAREST DEMONSTRATION OF THE DISTINCTION THAT
EXISTS. Reproduce it once and it is permanent."""),
  ("p", "<b>Off-policy learning is what allows experience replay and "
        "offline datasets</b> (Modules 04 and 09) — if you can "
        "only learn from the policy you are currently running, you cannot "
        "reuse old experience at all, and sample efficiency becomes "
        "hopeless. <b>And it is also where instability comes from</b> "
        "(Module 04 &sect;1's deadly triad names off-policy learning as "
        "one of its three ingredients), <b>which is the trade the rest of "
        "the course negotiates.</b>"),

  ("break",),
  ("h1", "3 &nbsp; Credit assignment over time"),
  ("callout", "n-step returns, and why eligibility traces exist",
   ["<b>An n-step return uses n real observed rewards and then bootstraps "
    "from the estimate n steps ahead</b> — so <b>n = 1 is temporal "
    "difference and n equal to the episode length is Monte Carlo</b>, and "
    "intermediate n interpolates &sect;1's trade continuously.",
    "<b>The best n is almost always strictly between the endpoints</b>, "
    "and <b>n = 3 to 5 is a common and effective default</b>. <b>It is "
    "the single cheapest improvement available to a value-based agent</b> "
    "— a few lines of buffering, no new hyperparameter beyond n, and "
    "a reliable gain.",
    "<b>Eligibility traces (TD(&lambda;)) average over all n "
    "simultaneously</b>, with geometrically decaying weights, "
    "<b>implemented backwards by maintaining a decaying eligibility value "
    "per state</b> — so the computational cost is one pass per step "
    "rather than n, which is the elegant part.",
    "<b>And traces are less used in deep reinforcement learning than "
    "they deserve to be</b>, partly because <b>replay buffers make the "
    "backward view awkward</b> (the eligibility belongs to a trajectory "
    "and the buffer samples transitions independently) and partly because "
    "n-step returns capture most of the benefit with far less machinery. "
    "<b>Which is an engineering accident rather than a result</b>, and "
    "worth knowing in case your setting makes traces natural again."]),

  ("h1", "4 &nbsp; Maximisation bias"),
  ("callout", "The max of noisy estimates is biased upward",
   ["<b>Q-learning's target contains max<sub>a</sub> Q(s&prime;,a), and "
    "the maximum of several noisy estimates exceeds the maximum of their "
    "true values in expectation</b> — because the max selects "
    "whichever estimate happened to be most favourably perturbed. The "
    "effect requires no bias in the individual estimates at all; noise "
    "alone produces it.",
    "<b>So the bias is <i>systematic</i> rather than noise</b>, and it "
    "<b>propagates</b>: an overestimated value becomes the bootstrap "
    "target for its predecessors, which overestimate in turn. <b>The "
    "error does not average out; it accumulates along trajectories.</b>",
    "<b>Double Q-learning fixes it</b> by maintaining two estimators and "
    "<b>using one to <i>select</i> the maximising action and the other to "
    "<i>evaluate</i> it</b> — so <b>the noise that chose the action "
    "is independent of the noise that values it</b>, and the upward bias "
    "disappears.",
    "<b>And the same fix becomes Double DQN</b> (Module 04 &sect;3), "
    "where <b>it is one of the very few modifications in deep "
    "reinforcement learning with an unambiguous, measurable, and "
    "well-understood benefit</b> — which is worth saying because most "
    "of the field's reported improvements are neither unambiguous nor "
    "well-understood (Module 12)."]),
  ("ul", ["<b>Q-learning with n-step returns and double estimation</b> is "
          "the sensible tabular default, and it is what Module 04 scales "
          "up.",
          "<b>SARSA when online performance <i>during</i> learning "
          "matters</b> — a physical robot that must not fall off the "
          "cliff, or a deployed system whose exploration costs real money. "
          "<b>&sect;2's demonstration is exactly this situation.</b>",
          "<b>Monte Carlo when episodes are short and the Markov property "
          "is doubtful</b>, since it does not rely on the state being a "
          "sufficient summary (&sect;1's table) — which makes it "
          "surprisingly robust in partially observable settings.",
          "<b>And expected SARSA</b> — average over the policy's "
          "action distribution rather than sampling a&prime; — "
          "<b>which has strictly lower variance than SARSA at no extra "
          "cost when the action set is small</b>, and is underused.",
          "<b>Everything in this module converges, tabularly, with "
          "proofs.</b> <b>Module 04 is where that stops being "
          "true</b> — so <b>implement all of these tabularly "
          "first</b>, because every deep method is one of them with a "
          "network in place of the table, and <b>the bugs are far easier "
          "to find when the algorithm is the only thing that can be "
          "wrong.</b>"]),
 ],
 "resources": [
   ("Sutton & Barto &mdash; chapters 5–7 and 12 (free PDF)",
    "http://incompleteideas.net/book/the-book.html",
    "<b>Monte Carlo, temporal difference, n-step, and traces</b> — "
    "the reference for this whole module. <b>The cliff-walking example of "
    "&sect;2 is figure 6.5.</b>"),
   ("Watkins & Dayan &mdash; Q-learning (free)",
    "https://link.springer.com/article/10.1007/BF00992698",
    "<b>The original convergence result</b> — short, and worth "
    "reading for what the proof requires."),
   ("Hasselt &mdash; Double Q-learning (free)",
    "https://papers.nips.cc/paper/2010/hash/091d584fced301b442654dd8c23b3fc9-Abstract.html",
    "<b>&sect;4's analysis and fix</b>, with the bias demonstrated on a "
    "small example."),
   ("David Silver &mdash; Reinforcement Learning lectures 4–5 (free "
    "video)",
    "https://www.davidsilver.uk/teaching/",
    "<b>Model-free prediction and control</b>, and the clearest spoken "
    "explanation of &sect;2's distinction."),
 ],
 "exercises": [
   "<b>Implement TD(0) and Monte Carlo</b> on a random walk and compare "
   "the error against episodes, averaged over runs.",
   "<b>Measure the bias and variance of each target</b> empirically and "
   "confirm &sect;1's table.",
   "<b>Implement SARSA and Q-learning</b> on cliff walking and reproduce "
   "the two different paths.",
   "<b>Plot online reward for both</b> and confirm SARSA is higher.",
   "<b>Then plot the final greedy policy's performance</b> and confirm "
   "Q-learning is higher.",
   "<b>Sweep n in n-step returns</b> from 1 to 20 and plot performance. "
   "Report the best n.",
   "<b>Implement TD(λ)</b> with eligibility traces and compare "
   "against the best n-step.",
   "<b>Construct a maximisation-bias example</b> and measure the "
   "overestimate.",
   "<b>Implement double Q-learning</b> on it and confirm the bias "
   "disappears.",
   "<b>Implement expected SARSA</b> and compare its variance against "
   "SARSA's.",
 ],
 "selfcheck": [
   "Write the TD update and explain what the TD error is.",
   "Why does updating a guess toward a guess converge?",
   "Compare Monte Carlo and TD on five axes.",
   "Which relies on the Markov property, and why?",
   "Give the SARSA and Q-learning updates and state the difference "
   "precisely.",
   "Describe cliff walking and what each algorithm learns.",
   "What does off-policy learning enable, and what does it cost?",
   "What do n-step returns interpolate, and what is a good default?",
   "Explain maximisation bias and why it propagates.",
   "How does double learning fix it?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Deep Q-Networks",
 "subtitle": "What breaks when the table becomes a network, and why.",
 "question": "Why is replacing a table with a network so much harder than "
             "it sounds?",
 "outcomes": [
     "State the deadly triad and explain each ingredient's role.",
     "Explain experience replay and target networks as fixes.",
     "Explain the main DQN improvements and which are substantial.",
     "Diagnose a diverging value-based agent.",
     "State what DQN is and is not suitable for.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The deadly triad",
   "blurb": "Three things that are individually fine."},

  {"t": "callout", "title": "Function approximation, bootstrapping, and off-policy learning",
   "kind": "Any two are safe; all three can diverge",
   "body": ["<b>Function approximation</b> — a network generalises, "
            "so updating one state's value changes others', including "
            "ones it should not.",
            "<b>Bootstrapping</b> — the target depends on the "
            "current estimate (Module 03 §1), so an error "
            "feeds itself.",
            "<b>Off-policy learning</b> — the states you update are "
            "not distributed as the policy you are evaluating would visit "
            "them, so the errors are weighted wrongly.",
            "<b>Any two of the three is safe. All three can "
            "diverge</b>, provably, on examples smaller than ten states. "
            "<b>And DQN uses all three</b> — <b>so every stabilising "
            "mechanism in this module is damage control, not "
            "refinement.</b>"]},

  {"t": "code", "kicker": "Divergence", "title": "Baird's counterexample, in words",
   "lang": "text", "code": """
  A seven-state MDP with a linear value function whose
  features are deliberately chosen so that the states
  SHARE PARAMETERS.

  Run off-policy TD on it with a behaviour distribution
  that does not match the target policy's.

  THE WEIGHTS DIVERGE TO INFINITY. Not oscillate, not
  converge slowly -- diverge, monotonically, forever.

  WHY: updating one state's value, through the shared
  parameters, changes the BOOTSTRAP TARGET of another state
  in a direction that increases its error. The off-policy
  weighting means the correction never arrives, because the
  states that would correct it are rarely visited.

  SEVEN STATES. A LINEAR function approximator. No neural
  network, no noise, no deep anything.

  SO WHEN A DEEP Q-NETWORK DIVERGES, IT IS NOT A BUG IN
  YOUR CODE. It may be, but the algorithm diverges on
  seven states too, and the fixes in Part 2 exist because
  of this -- not because of implementation difficulty.
""",
   "caption": "<b>Knowing a seven-state example diverges changes how you "
              "debug</b> — you look for the triad before looking for "
              "a typo.",
   "note": "This reframes 'my DQN won't train' from a bug hunt to a "
           "design question."},

  {"t": "section", "label": "Part 2", "title": "The two fixes",
   "blurb": "Replay and target networks, and what each addresses."},

  {"t": "table", "kicker": "Fixes", "title": "What each mechanism actually does",
   "header": ["Mechanism", "Addresses", "Side effect"],
   "widths": [2.7, 4.3, 5.0],
   "rows": [
     ["<b>Experience replay</b>", "<b>Correlated consecutive samples; sample reuse</b>", "<b>Stale data from an old policy</b>"],
     ["<b>Target network</b>", "<b>The moving bootstrap target</b>", "<b>Slower propagation of value</b>"],
     ["<b>Reward clipping</b>", "<b>Loss scale varying between games</b>", "<b>Destroys reward magnitude information</b>"],
     ["<b>Huber loss</b>", "<b>Large TD errors dominating</b>", "<b>Slower learning on large errors</b>"],
     ["<b>Frame stacking</b>", "<b>Partial observability (velocity)</b>", "<b>4× the input size</b>"],
   ],
   "footnote": "<b>Every one has a side effect</b>, which is worth "
               "stating: these are not free improvements but trades, and "
               "reward clipping in particular loses real information.",
   "note": "Being explicit that the fixes cost something is unusual and "
           "honest."},

  {"t": "callout", "title": "Why a target network works",
   "kind": "The mechanism, precisely",
   "body": ["<b>Without one, the target r + γ·max Q(s′) uses "
            "the <i>same</i> network you are updating</b> — so each "
            "gradient step moves the target it was chasing.",
            "<b>That is a feedback loop, and it is the bootstrapping leg "
            "of the triad at its worst.</b>",
            "<b>Freeze a copy of the network and compute targets from "
            "it, updating the copy every few thousand steps.</b> The "
            "target is now stationary between updates.",
            "<b>So each phase is an ordinary supervised regression "
            "problem</b> (CSCE 636) — which is the right way to "
            "think about it. <b>The cost is that value propagates "
            "slowly</b>, which is why the update interval is a real "
            "hyperparameter."]},

  {"t": "section", "label": "Part 3", "title": "The improvements",
   "blurb": "Which of the many additions matter."},

  {"t": "bullets", "kicker": "Improvements", "title": "Ranked by how substantial they are",
   "items": [
     "<b>Double DQN.</b> <b>Fixes a real, understood bias</b> "
     "(Module 03 §4) <b>for one line of code.</b> Take it.",
     "",
     "<b>n-step returns.</b> <b>Cheap and reliably helps</b>, same as "
     "tabularly.",
     "",
     "<b>Prioritised replay.</b> Sample high-TD-error transitions more "
     "often. <b>Helps, and adds importance-weight bookkeeping that is "
     "easy to get wrong.</b>",
     "",
     "<b>Duelling architecture.</b> Separate value and advantage "
     "streams. <b>Modest and cheap.</b>",
     "",
     "<b>Distributional (C51, QR-DQN).</b> <b>Learn the return "
     "distribution rather than its mean. A large gain, and the "
     "explanation for why is still debated.</b>",
   ],
   "footnote": "<b>Rainbow combines them and is much better than "
               "DQN</b> — and the ablation shows prioritised replay "
               "and multi-step contribute most, which is worth knowing "
               "before adding all six."},

  {"t": "section", "label": "Part 4", "title": "Diagnosis",
   "blurb": "Reading a value-based agent that is not working."},

  {"t": "code", "kicker": "Diagnosis", "title": "Symptom to cause",
   "lang": "text", "code": """
  Q-VALUES GROWING WITHOUT BOUND
      the triad (Part 1). Check the target network is
      actually being used and updated; reduce the learning
      rate; add double Q-learning.

  Q-VALUES PLAUSIBLE, RETURN FLAT
      exploration, or the reward. Plot state visitation
      (Module 02 Part 4). If the reward is never reached,
      it is exploration.

  LEARNS THEN COLLAPSES
      classic. Usually the replay buffer filling with
      data from a changed policy, or the target network
      interval being too long relative to the policy's
      rate of change.

  WORKS ON ONE SEED, NOT OTHERS
      this is NORMAL (Module 12), not a bug. Run five
      seeds before concluding anything about anything.

  LOSS DECREASING, RETURN NOT IMPROVING
      the loss is NOT the objective. A TD loss can fall
      while the policy gets worse. NEVER judge an RL run
      by its loss curve -- judge it by episode return.

  THAT LAST ONE IS THE MOST COMMON MISTAKE BY PEOPLE
  ARRIVING FROM SUPERVISED LEARNING, where the loss IS
  a proxy for the thing you want.
""",
   "caption": "<b>The loss is not the objective</b> — which is the "
              "single most important habit to carry from CSCE 636 into "
              "this course, inverted.",
   "note": "The loss-curve mistake is universal and worth stating "
           "bluntly."},

  {"t": "callout", "title": "Where DQN belongs",
   "kind": "Honest scope",
   "body": ["<b>Discrete, small action spaces.</b> <b>The max over "
            "actions is enumerated</b>, so a large or continuous action "
            "space rules it out (Module 07).",
            "<b>Plenty of samples available.</b> Tens of millions, in "
            "practice.",
            "<b>And off-policy data worth reusing</b>, which is the "
            "actual advantage over policy gradients.",
            "<b>Not for continuous control</b> (Module 07), <b>not "
            "where samples are scarce</b> (Module 08), <b>and not where "
            "you need a stochastic policy</b> — which "
            "Module 05's methods give you natively."]},
 ],
 "takeaways": [
   "The deadly triad is function approximation, bootstrapping, and "
   "off-policy learning — any two are safe and all three can "
   "diverge.",
   "Baird's counterexample diverges on seven states with a linear "
   "approximator, so divergence is a property of the algorithm rather than "
   "your code.",
   "A target network makes each training phase an ordinary supervised "
   "regression, at the cost of slower value propagation.",
   "Every stabilising mechanism has a side effect — reward clipping "
   "in particular destroys magnitude information.",
   "Double DQN and n-step returns are the cheap reliable improvements; "
   "distributional methods help substantially and are not fully "
   "understood.",
   "The loss is not the objective: a TD loss can fall while the policy "
   "worsens, so judge a run by episode return.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The deadly triad"),
  ("callout", "Function approximation, bootstrapping, and off-policy "
              "learning",
   ["<b>Function approximation.</b> A network generalises, so updating "
    "one state's value necessarily changes other states' values — "
    "including states where the change is wrong. A table has no such "
    "coupling.",
    "<b>Bootstrapping.</b> The update target depends on the current "
    "estimate (Module 03 &sect;1), <b>so an error in the estimate feeds "
    "into its own target</b> and can amplify rather than correct.",
    "<b>Off-policy learning.</b> The states you update are not "
    "distributed as the policy being evaluated would visit them, <b>so the "
    "errors are weighted by the wrong distribution</b> and the states that "
    "would correct a growing error may be visited rarely or never.",
    "<b>Any two of the three is safe. All three together can "
    "diverge</b> — provably, on examples with fewer than ten states "
    "(&sect;1's code). <b>And DQN uses all three.</b> <b>So every "
    "stabilising mechanism in this module is damage control rather than "
    "refinement</b>, which is the right way to understand replay buffers "
    "and target networks: <b>they are not clever tricks that improve a "
    "sound algorithm; they are what makes an unsound combination usable.</b>"]),
  ("code", """BAIRD'S COUNTEREXAMPLE

A seven-state MDP with a LINEAR value function whose
features are deliberately chosen so that the states SHARE
PARAMETERS.

Run off-policy TD on it, with a behaviour distribution that
does not match the target policy's.

THE WEIGHTS DIVERGE TO INFINITY. Not oscillate; not
converge slowly -- diverge, monotonically, without bound.

WHY: updating one state's value, through the shared
parameters, changes the BOOTSTRAP TARGET of another state
in a direction that increases its error. And the off-policy
weighting means the correction never arrives, because the
states that would supply it are visited rarely.

SEVEN STATES. A LINEAR approximator. No neural network, no
stochasticity, no deep anything, no implementation bug.

SO WHEN A DEEP Q-NETWORK DIVERGES, IT IS NOT NECESSARILY A
BUG IN YOUR CODE. It may be -- but the algorithm diverges
on seven states too, and the mechanisms in section 2 exist
because of this, not because deep networks are fiddly."""),
  ("p", "<b>Knowing that a seven-state example diverges changes how you "
        "debug.</b> <b>You look for the triad before you look for a "
        "typo</b>: is the target network actually being used? Is it "
        "updated too rarely or too often? Is the learning rate too high "
        "for the bootstrap depth? <b>Which is a different and more "
        "productive first hour than reading your replay buffer "
        "indexing.</b>"),

  ("h1", "2 &nbsp; The two fixes"),
  ("table", ["Mechanism", "What it addresses", "Side effect"],
   [["<b>Experience replay</b>",
     "<b>Consecutive samples are highly correlated, which breaks the "
     "independence that stochastic gradient descent assumes</b> "
     "(CSCE 669 Module 08); <b>and it lets each sample be reused "
     "many times.</b>",
     "<b>The buffer contains data from older, worse policies</b> — "
     "which is the off-policy leg of the triad, deliberately accepted."],
    ["<b>Target network</b>", "<b>The bootstrap target moving as you "
     "update</b> — see the callout.",
     "<b>Value propagates more slowly</b>, so the update interval trades "
     "stability against speed."],
    ["<b>Reward clipping to [&minus;1, 1]</b>",
     "<b>The loss scale varying wildly between tasks</b>, which makes one "
     "learning rate work across games.",
     "<b>It destroys reward magnitude information</b> — a 1-point "
     "and a 1000-point event become identical, which is a real loss and is "
     "rarely acknowledged."],
    ["<b>Huber loss</b>",
     "<b>Large TD errors producing huge gradients</b> that destabilise "
     "the network.",
     "<b>Slower learning precisely where the error is largest</b>, which "
     "is sometimes where you need it fastest."],
    ["<b>Frame stacking</b>",
     "<b>Partial observability — a single frame does not reveal "
     "velocity</b>, so the state is not Markov (Module 03 &sect;1).",
     "<b>Four times the input size</b>, and it only fixes the short-range "
     "case; longer memory needs a recurrent or attention-based "
     "architecture."]],
   [0.19, 0.42, 0.39]),
  ("callout", "Why a target network works",
   ["<b>Without one, the target r + &gamma;&middot;max<sub>a</sub> "
    "Q(s&prime;,a) is computed with the <i>same</i> network you are "
    "updating</b> — so <b>each gradient step moves the target it was "
    "chasing</b>, in a direction correlated with the step itself.",
    "<b>That is a positive feedback loop, and it is the bootstrapping leg "
    "of the triad at its worst</b> — the estimate and its own target "
    "move together, so nothing anchors the scale.",
    "<b>Freeze a copy of the network, compute all targets from the "
    "frozen copy, and refresh the copy every few thousand steps.</b> "
    "<b>The target is now stationary between refreshes.</b>",
    "<b>So each phase between refreshes is an ordinary supervised "
    "regression problem</b> — fixed inputs, fixed targets, "
    "CSCE 636's entire toolkit applies — <b>which is the right way "
    "to think about what DQN is doing</b>. <b>The cost is that value "
    "information propagates one target-refresh per step of distance</b>, "
    "so <b>the refresh interval is a genuine hyperparameter</b>: too "
    "short and you reintroduce the feedback loop, too long and learning "
    "crawls."]),

  ("break",),
  ("h1", "3 &nbsp; The improvements, ranked"),
  ("ul", ["<b>Double DQN.</b> <b>Fixes a real, understood, systematic "
          "bias</b> (Module 03 &sect;4) <b>for approximately one line "
          "of code</b> — use the online network to select the action "
          "and the target network to evaluate it. <b>Take it "
          "unconditionally.</b>",
          "<b>n-step returns.</b> <b>Cheap and reliably helpful</b>, "
          "exactly as in the tabular case (Module 03 &sect;3). Three "
          "to five steps.",
          "<b>Prioritised experience replay.</b> Sample transitions with "
          "large TD error more often, on the reasoning that they carry "
          "more information. <b>It helps, and it adds importance-weight "
          "bookkeeping that is easy to get subtly wrong</b> — the "
          "correction for the non-uniform sampling is required, and "
          "omitting it introduces a bias that is hard to notice.",
          "<b>Duelling architecture.</b> Split the network into a state-"
          "value stream and an action-advantage stream and recombine "
          "them, so the value of a state can be learned without "
          "distinguishing actions. <b>Modest, cheap, and uncontroversial.</b>",
          "<b>Distributional reinforcement learning (C51, QR-DQN).</b> "
          "<b>Learn the full distribution of returns rather than its "
          "mean.</b> <b>A large and reliable gain — and the "
          "explanation for why is still debated</b>, since the policy only "
          "uses the mean. The leading guesses are a better-conditioned "
          "learning signal and an implicit auxiliary task; neither is "
          "settled, and saying so is more useful than picking one.",
          "<b>Rainbow combines all of these and is substantially better "
          "than DQN</b> — and <b>its ablation study shows "
          "prioritised replay and multi-step returns contribute most</b>, "
          "which is worth knowing before implementing all six."]),

  ("h1", "4 &nbsp; Diagnosis"),
  ("code", """Q-VALUES GROWING WITHOUT BOUND
    the triad (section 1). Check the target network is
    actually being used and is being refreshed; reduce the
    learning rate; add double Q-learning; check the reward
    scale.

Q-VALUES PLAUSIBLE, EPISODE RETURN FLAT
    exploration, or the reward itself. Plot state
    visitation (Module 02 section 4). If the rewarding
    region is never reached, it is exploration; if it is
    reached and nothing improves, it is not.

LEARNS, THEN COLLAPSES
    the classic failure. Usually the replay buffer filling
    with data from a policy that has since changed, or the
    target refresh interval being too long relative to how
    fast the policy is moving.

WORKS ON ONE SEED AND NOT OTHERS
    THIS IS NORMAL (Module 12), not a bug. Run five seeds
    before concluding anything about anything.

LOSS DECREASING, RETURN NOT IMPROVING
    THE LOSS IS NOT THE OBJECTIVE. A TD loss can fall
    steadily while the policy gets worse, because the
    network is becoming self-consistent rather than
    correct. NEVER judge a reinforcement learning run by
    its loss curve. Judge it by episode return."""),
  ("p", "<b>That last one is the most common mistake made by people "
        "arriving from supervised learning</b>, where the training loss "
        "genuinely is a proxy for the thing you want. <b>Here it is "
        "not:</b> the TD loss measures self-consistency between the "
        "network and its own bootstrap targets, and <b>a network can "
        "become perfectly self-consistent around a wrong value "
        "function</b>. <b>The only reliable signal is the episode "
        "return</b>, and the only reliable comparison is across seeds "
        "(Module 12)."),
  ("callout", "Where DQN belongs",
   ["<b>Discrete action spaces, and small ones.</b> <b>The max over "
    "actions in the target is computed by enumeration</b>, so a large "
    "discrete space is expensive and a continuous one is impossible "
    "(Module 07 exists for this reason).",
    "<b>Plenty of samples available.</b> Tens of millions in practice for "
    "anything visually complex — Module 01 &sect;2's figure, which "
    "means a fast simulator is a precondition.",
    "<b>And off-policy data worth reusing</b>, which is <b>the actual "
    "advantage over the policy-gradient methods of Module 05</b>: a "
    "replay buffer means each environment step contributes to many "
    "gradient steps, which is where the sample-efficiency advantage comes "
    "from.",
    "<b>Not for continuous control</b> (Module 07), <b>not where "
    "samples are scarce</b> (Module 08's model-based methods), <b>and "
    "not where you need a genuinely stochastic policy</b> — which "
    "Module 05's methods represent natively and a greedy value-based "
    "method does not. <b>Knowing the three exclusions is most of knowing "
    "when to reach for something else.</b>"]),
 ],
 "resources": [
   ("Mnih et al. &mdash; Human-level control through deep reinforcement "
    "learning (free)",
    "https://www.nature.com/articles/nature14236",
    "<b>The DQN paper.</b> The replay and target-network motivation of "
    "&sect;2 is stated here, and the engineering details matter."),
   ("Sutton & Barto &mdash; chapter 11 (free PDF)",
    "http://incompleteideas.net/book/the-book.html",
    "<b>The deadly triad and Baird's counterexample of &sect;1</b>, "
    "developed carefully. This chapter is the one to read slowly."),
   ("Hessel et al. &mdash; Rainbow: Combining Improvements in Deep "
    "Reinforcement Learning (free)",
    "https://arxiv.org/abs/1710.02298",
    "<b>&sect;3's list with the ablation study</b> that says which "
    "components actually contribute."),
   ("CleanRL &mdash; dqn.py and dqn_atari.py (free)",
    "https://docs.cleanrl.dev/",
    "<b>A readable single-file DQN</b> with every implementation detail "
    "visible — and the details are where the performance is."),
 ],
 "exercises": [
   "<b>Implement Baird's counterexample</b> and plot the weights "
   "diverging.",
   "<b>Remove one leg of the triad</b> (make it on-policy) and confirm it "
   "converges.",
   "<b>Implement DQN on CartPole</b> from scratch, with replay and a "
   "target network.",
   "<b>Ablate the replay buffer</b> and report what happens.",
   "<b>Ablate the target network</b> and report what happens.",
   "<b>Sweep the target refresh interval</b> and plot performance against "
   "it.",
   "<b>Add double Q-learning</b> and measure the change in Q-value "
   "magnitudes.",
   "<b>Add n-step returns</b> and report the improvement.",
   "<b>Plot the TD loss and the episode return on the same figure</b> for "
   "a run that fails, and confirm they disagree.",
   "<b>Run five seeds</b> of your best configuration and plot all five.",
 ],
 "selfcheck": [
   "Name the three legs of the deadly triad and what each contributes.",
   "What does Baird's counterexample establish, and with how many "
   "states?",
   "How should that change your debugging?",
   "What does experience replay address, and what is its side effect?",
   "Explain precisely why a target network helps, and what it costs.",
   "Which DQN improvements are cheap and reliable?",
   "Which is largest and least understood?",
   "Give five symptoms and their likely causes.",
   "Why is the loss not the objective?",
   "Name three situations where DQN is the wrong choice.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Policy Gradients",
 "subtitle": "Optimise the policy directly.",
 "question": "What if you skip the value function and differentiate the "
             "objective?",
 "outcomes": [
     "Derive the policy gradient theorem.",
     "Explain why the derivation needs no model of the environment.",
     "Explain baselines and variance reduction.",
     "Compare policy gradients against value-based methods.",
     "Explain why on-policy methods discard their data.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The derivation",
   "blurb": "The trick that makes it possible."},

  {"t": "eq", "kicker": "Policy gradient", "title": "The theorem, and the step that matters",
   "eqs": [
     ("∇J(θ) = E[ ∇log π(a|s;θ) · "
      "R ]",
      "The gradient of expected return is an expectation of the "
      "score function times the return."),
     ("The step: ∇p = p · ∇log p",
      "The log-derivative trick. It converts a gradient of an "
      "expectation into an expectation of a gradient."),
     ("Note what is ABSENT: any gradient of the environment",
      "No ∇P, no model. The environment's dynamics appear only "
      "inside the expectation, which you estimate by sampling."),
   ],
   "caption": "<b>That absence is the whole reason this works</b> "
              "— you are differentiating only your own policy, which "
              "you wrote and can differentiate.",
   "note": "Emphasising what is missing from the formula is the clearest "
           "way to teach it."},

  {"t": "callout", "title": "REINFORCE, and why it is so high-variance",
   "kind": "The simplest algorithm, and its problem",
   "body": ["<b>Run an episode, compute the return, and push up the "
            "log-probability of every action taken, in proportion to the "
            "return.</b> That is the whole algorithm.",
            "<b>It is unbiased</b> and it works on tiny problems.",
            "<b>The variance is enormous</b>, for two reasons: <b>the "
            "return is a Monte Carlo estimate</b> (Module 03 §1) "
            "<b>and every action in the episode is credited with the "
            "whole return</b>, including actions taken after the reward "
            "was earned.",
            "<b>So the gradient estimate is dominated by which episodes "
            "happened to go well</b>, rather than by which actions caused "
            "it. <b>Part 2 is entirely about fixing that.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Variance reduction",
   "blurb": "Three fixes, all necessary."},

  {"t": "code", "kicker": "Variance", "title": "Why a baseline is free, and what else helps",
   "lang": "text", "code": """
  SUBTRACT A BASELINE:
      grad = E[ grad log pi(a|s) * (R - b(s)) ]

  THIS DOES NOT CHANGE THE EXPECTATION, for any b that does
  not depend on the action:
      E[ grad log pi(a|s) * b(s) ] = b(s) * grad sum_a pi
                                   = b(s) * grad 1 = 0
  The subtracted term has expectation EXACTLY ZERO.

  SO THE BIAS IS UNCHANGED AND THE VARIANCE FALLS, often by
  an order of magnitude. It is as close to free as anything
  in this field gets.

  THE BEST SIMPLE BASELINE is V(s) -- the expected return
  from that state. Then (R - V(s)) is the ADVANTAGE: how
  much better this action turned out than average.
      -- and now you need a value function after all, which
         is Module 06's actor-critic.

  TWO MORE FIXES:
    CAUSALITY / reward-to-go -- credit an action only with
        rewards that came AFTER it. Actions cannot affect
        the past, so including earlier rewards is pure
        noise. Free, and always correct.
    NORMALISE the advantages within a batch -- subtract the
        mean, divide by the standard deviation. Technically
        introduces a bias; universally done; helps a lot.
""",
   "caption": "<b>The baseline proof is two lines and worth doing "
              "once</b> — it is the clearest example of reducing "
              "variance without touching bias.",
   "note": "Have students verify the zero-expectation step themselves."},

  {"t": "section", "label": "Part 3", "title": "Against value-based",
   "blurb": "What each is good for."},

  {"t": "table", "kicker": "Comparison", "title": "Policy gradients against value-based methods",
   "header": ["", "Policy gradient", "Value-based (DQN)"],
   "widths": [2.3, 4.5, 5.2],
   "rows": [
     ["<b>Learns</b>", "<b>The policy directly</b>", "<b>Q, then acts greedily</b>"],
     ["<b>Actions</b>", "<b>Continuous or discrete, natively</b>", "<b>Discrete, small</b>"],
     ["<b>Stochastic policies</b>", "<b>Natural — and sometimes optimal</b>", "<b>Awkward</b>"],
     ["<b>Sample efficiency</b>", "<b>Poor — on-policy, so data is discarded</b>", "<b>Better — replay reuses everything</b>"],
     ["<b>Stability</b>", "<b>Better — no bootstrapping leg</b>", "<b>Worse — the triad</b>"],
     ["<b>Converges to</b>", "<b>A local optimum, reliably</b>", "<b>Possibly nothing</b>"],
   ],
   "footnote": "<b>The trade is sample efficiency against stability</b>, "
               "and it is why both families persist — and why "
               "Module 06's actor-critic tries to have both.",
   "note": "Naming the trade explicitly prevents the 'which is better' "
           "question."},

  {"t": "callout", "title": "On-policy methods throw their data away",
   "kind": "The cost nobody mentions first",
   "body": ["<b>The policy gradient is an expectation under the "
            "<i>current</i> policy.</b> So experience from an older "
            "policy is not a valid sample for the current gradient.",
            "<b>Which means every batch is used once and "
            "discarded</b> — an enormous waste compared to a replay "
            "buffer that reuses each transition dozens of times.",
            "<b>Importance sampling can correct for the mismatch</b> "
            "— reweight by the ratio of action probabilities "
            "— <b>and the variance of the correction explodes as "
            "the policies diverge.</b>",
            "<b>Which is exactly what PPO's clipping manages</b> "
            "(Module 06 §3): <b>reuse a batch several times, but "
            "only while the policies remain close enough for the "
            "correction to be trustworthy.</b>"]},

  {"t": "section", "label": "Part 4", "title": "In practice",
   "blurb": "What to do and what to watch."},

  {"t": "bullets", "kicker": "Practice", "title": "Running a policy-gradient agent",
   "items": [
     "<b>Use reward-to-go and a learned value baseline.</b> <b>Plain "
     "REINFORCE is a teaching tool, not a method.</b>",
     "",
     "<b>Normalise advantages per batch</b>, and normalise "
     "observations too — <b>CSCE 633's feature scaling, which "
     "matters as much here.</b>",
     "",
     "<b>Log policy entropy.</b> <b>A collapsed entropy means the "
     "policy has become deterministic and stopped exploring</b>, which "
     "explains most plateaus.",
     "",
     "<b>Use large batches.</b> <b>The gradient is a noisy expectation "
     "and variance falls as 1/B</b> (CSCE 669 M08) — so batch "
     "size matters more here than in supervised learning.",
     "",
     "<b>And watch the gradient norm.</b> Clip it; spikes are "
     "real and destructive.",
   ],
   "footnote": "<b>Entropy and gradient norm are the two most "
               "informative logs</b>, and neither is the loss — "
               "which Module 04 §4 established is "
               "uninformative."},
 ],
 "takeaways": [
   "The log-derivative trick converts the gradient of an expectation into "
   "an expectation of a gradient, and no gradient of the environment "
   "appears.",
   "REINFORCE is unbiased and enormously high-variance, because every "
   "action is credited with the whole episode return.",
   "Subtracting any action-independent baseline leaves the expectation "
   "unchanged and reduces variance — as close to free as this field "
   "offers.",
   "Reward-to-go is always correct and free: an action cannot affect "
   "rewards that preceded it.",
   "Policy gradients handle continuous and stochastic policies natively "
   "and are more stable; value-based methods are more sample-efficient.",
   "On-policy methods discard every batch after one use, which is what "
   "PPO's clipping exists to partially recover.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The derivation"),
  ("eq", "&nabla;J(&theta;) = E[ &nabla; log &pi;(a|s;&theta;) &middot; "
         "R ]"),
  ("p", "<b>The gradient of the expected return equals the expectation of "
        "the score function times the return.</b> <b>The step that makes "
        "it possible is the log-derivative trick:</b> &nabla;p = p "
        "&middot; &nabla;log p, which <b>converts the gradient of an "
        "expectation (which you cannot compute, because it involves the "
        "environment's distribution) into an expectation of a gradient "
        "(which you can estimate by sampling).</b>"),
  ("p", "<b>Note carefully what is absent from the formula: any gradient "
        "of the environment.</b> <b>There is no &nabla;P and no model at "
        "all</b> — the dynamics appear only inside the expectation, "
        "which you estimate by running the policy and observing what "
        "happens. <b>That absence is the entire reason the method "
        "works</b>: <b>you are differentiating only your own policy, "
        "which you wrote in a framework that differentiates things.</b> "
        "<b>Teaching the derivation by pointing at what is missing is "
        "clearer than following the algebra</b>, because the algebra's "
        "purpose is precisely to eliminate that term."),
  ("callout", "REINFORCE, and why it is so high-variance",
   ["<b>Run an episode, compute its total return, and increase the "
    "log-probability of every action that was taken, in proportion to that "
    "return.</b> That is the whole algorithm, and it is four lines of "
    "code.",
    "<b>It is unbiased</b> — the estimate's expectation is the true "
    "gradient — and it does work on small problems, which makes it "
    "worth implementing once.",
    "<b>The variance is enormous, for two separable reasons.</b> "
    "<b>First, the return is a Monte Carlo estimate</b> and carries every "
    "random event in the episode (Module 03 &sect;1's table). "
    "<b>Second, every action in the episode is credited with the whole "
    "return</b> — including actions taken <i>after</i> the reward was "
    "earned, which cannot possibly have caused it.",
    "<b>So the gradient estimate is dominated by which episodes happened "
    "to go well rather than by which actions made them go well</b>, which "
    "is a credit-assignment failure rather than merely noise. <b>&sect;2 "
    "is entirely about fixing it</b>, and both of its main fixes attack "
    "one of the two reasons."]),

  ("h1", "2 &nbsp; Variance reduction"),
  ("code", """SUBTRACT A BASELINE:
    grad = E[ grad log pi(a|s) * (R - b(s)) ]

THIS DOES NOT CHANGE THE EXPECTATION, for any b that does
not depend on the action:
    E[ grad log pi(a|s) * b(s) ]
        = b(s) * sum_a pi(a|s) * grad log pi(a|s)
        = b(s) * grad sum_a pi(a|s)
        = b(s) * grad 1
        = 0
The subtracted term has expectation EXACTLY ZERO.

SO THE BIAS IS UNCHANGED AND THE VARIANCE FALLS, frequently
by an order of magnitude. It is as close to free as
anything in this field gets.

THE BEST SIMPLE BASELINE is V(s), the expected return from
that state. Then (R - V(s)) is the ADVANTAGE: how much
better this action turned out to be than average from here.
    -- and now you need a value function after all, which
       is Module 06's actor-critic.

TWO MORE FIXES:
  CAUSALITY / reward-to-go
      credit an action only with rewards that arrived AFTER
      it. An action cannot affect the past, so including
      earlier rewards adds variance and no signal. Free,
      always correct, and it is the fix for the SECOND
      reason in section 1's callout.
  NORMALISE the advantages within each batch -- subtract
      the mean, divide by the standard deviation.
      Technically this introduces a bias (the mean is
      estimated from the same batch); it is universally
      done; it helps substantially."""),
  ("p", "<b>The baseline proof is two lines and worth doing once by "
        "hand</b> — it is <b>the clearest example available of "
        "reducing variance without touching bias</b>, and the reason it "
        "works (the probabilities sum to one, so their gradient sums to "
        "zero) is the kind of fact that makes the rest of the field's "
        "variance-reduction tricks recognisable."),

  ("break",),
  ("h1", "3 &nbsp; Against value-based methods"),
  ("table", ["", "Policy gradient", "Value-based (DQN)"],
   [["<b>What it learns</b>", "<b>The policy directly.</b>",
     "<b>Q, and acts greedily with respect to it.</b>"],
    ["<b>Action spaces</b>",
     "<b>Continuous or discrete, natively</b> — the policy outputs a "
     "distribution of whatever shape you choose.",
     "<b>Discrete, and small</b>, because the target requires a max over "
     "actions (Module 04 &sect;4)."],
    ["<b>Stochastic policies</b>",
     "<b>Natural, and sometimes optimal</b> — CSCE 625 "
     "Module 12 &sect;4's mixed strategies, and necessary under "
     "partial observability.",
     "<b>Awkward</b> — a greedy policy is deterministic, and "
     "&epsilon;-greedy is a poor substitute for a learned "
     "distribution."],
    ["<b>Sample efficiency</b>",
     "<b>Poor — on-policy, so every batch is discarded after one "
     "use</b> (see the callout).",
     "<b>Better — a replay buffer reuses each transition many "
     "times.</b>"],
    ["<b>Stability</b>",
     "<b>Better — no bootstrapping leg, so no deadly triad</b> in "
     "the pure form.",
     "<b>Worse — all three legs of the triad</b> (Module 04 "
     "&sect;1)."],
    ["<b>Converges to</b>",
     "<b>A local optimum, reliably</b> — it is gradient ascent on a "
     "smooth objective (CSCE 669 Module 05).",
     "<b>Possibly nothing</b>, in the function-approximation case."]],
   [0.18, 0.40, 0.42]),
  ("callout", "On-policy methods throw their data away",
   ["<b>The policy gradient is an expectation under the <i>current</i> "
    "policy.</b> So experience collected under an older policy is not a "
    "valid sample for the current gradient — it answers a different "
    "question.",
    "<b>Which means every batch is used once and discarded.</b> <b>An "
    "enormous waste compared to a replay buffer that reuses each "
    "transition dozens of times</b>, and it is the direct cause of the "
    "sample-efficiency row in the table above.",
    "<b>Importance sampling can correct for the mismatch</b> — "
    "reweight each sample by the ratio of its action's probability under "
    "the new and old policies — <b>and the variance of that "
    "correction explodes as the two policies diverge</b>, because the "
    "ratios become extreme and a few samples dominate the estimate.",
    "<b>Which is exactly what PPO's clipping manages</b> (Module 06 "
    "&sect;3): <b>reuse a batch for several gradient steps, but only "
    "while the policies remain close enough for the importance correction "
    "to be trustworthy, and refuse to move further.</b> <b>Understanding "
    "PPO as 'partial data reuse under a trust constraint' rather than as a "
    "clipping heuristic is the thing to take from this callout.</b>"]),

  ("h1", "4 &nbsp; In practice"),
  ("ul", ["<b>Use reward-to-go and a learned value baseline.</b> "
          "<b>Plain REINFORCE is a teaching tool rather than a "
          "method</b>, and skipping both fixes wastes most of the "
          "sample budget on variance.",
          "<b>Normalise advantages per batch, and normalise observations "
          "too</b> — <b>CSCE 633 Module 02's feature scaling, "
          "which matters at least as much here</b>, because the "
          "observation scale feeds directly into the policy's "
          "conditioning (CSCE 669 Module 05 &sect;2).",
          "<b>Log policy entropy, every run.</b> <b>A collapsed entropy "
          "means the policy has become deterministic and has stopped "
          "exploring</b> — which explains most performance plateaus "
          "and is invisible in the return curve until it is too late. "
          "Module 07 &sect;3 makes entropy an explicit objective for "
          "exactly this reason.",
          "<b>Use large batches.</b> <b>The gradient is a noisy "
          "expectation and its variance falls as 1/B</b> (CSCE 669 "
          "Module 08 &sect;2), <b>so batch size matters considerably "
          "more here than in supervised learning</b> — and the "
          "practical consequence is that parallel environment collection "
          "is the standard engineering pattern.",
          "<b>And watch the gradient norm.</b> <b>Clip it</b>; spikes "
          "are real, they are caused by rare extreme advantages, and a "
          "single one can destroy a policy that took hours to train. "
          "<b>Entropy and gradient norm are the two most informative "
          "logs</b>, and <b>neither is the loss</b> — which "
          "Module 04 &sect;4 established is uninformative."]),
 ],
 "resources": [
   ("Sutton & Barto &mdash; chapter 13 (free PDF)",
    "http://incompleteideas.net/book/the-book.html",
    "<b>The policy gradient theorem and REINFORCE</b>, with the baseline "
    "derivation of &sect;2."),
   ("OpenAI Spinning Up &mdash; Intro to Policy Optimization (free)",
    "https://spinningup.openai.com/en/latest/spinningup/rl_intro3.html",
    "<b>The clearest available derivation of &sect;1</b>, including the "
    "reward-to-go and baseline arguments with the algebra shown."),
   ("Williams &mdash; Simple statistical gradient-following algorithms "
    "(free)",
    "https://link.springer.com/article/10.1007/BF00992696",
    "<b>The original REINFORCE paper</b>, and it is clearer than its "
    "reputation."),
   ("Schulman et al. &mdash; High-Dimensional Continuous Control Using "
    "Generalized Advantage Estimation (free)",
    "https://arxiv.org/abs/1506.02438",
    "<b>&sect;2's variance reduction taken properly</b> — GAE "
    "interpolates the bias-variance trade in the advantage, and it is what "
    "every modern implementation uses."),
 ],
 "exercises": [
   "<b>Derive the policy gradient</b> and identify the log-derivative "
   "step.",
   "<b>Verify the baseline's zero expectation</b> algebraically.",
   "<b>Implement REINFORCE on CartPole</b> and measure the gradient "
   "variance across batches.",
   "<b>Add reward-to-go</b> and report the variance change.",
   "<b>Add a learned value baseline</b> and report it again.",
   "<b>Add advantage normalisation</b> and report a third time.",
   "<b>Plot all four variances on one figure</b> and relate each to its "
   "fix.",
   "<b>Sweep batch size</b> from 256 to 8192 and plot performance and "
   "gradient variance.",
   "<b>Log policy entropy</b> and deliberately cause it to collapse. "
   "Observe the plateau.",
   "<b>Implement importance sampling to reuse a batch twice</b> and "
   "measure how the correction's variance grows.",
 ],
 "selfcheck": [
   "State the policy gradient theorem and the trick that derives it.",
   "What is absent from the formula, and why does that matter?",
   "Give the two reasons REINFORCE is high-variance.",
   "Prove that a baseline does not change the expectation.",
   "What is the advantage, and what does using V as a baseline "
   "require?",
   "Why is reward-to-go always correct?",
   "Compare policy gradients against value-based methods on six axes.",
   "Why do on-policy methods discard data, and what does PPO do about "
   "it?",
   "Name the two most informative things to log.",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Actor-Critic and Trust Regions",
 "subtitle": "Both halves, and the default algorithm.",
 "question": "How do you get a value function's efficiency and a policy "
             "gradient's stability?",
 "outcomes": [
     "Explain actor-critic and what each component contributes.",
     "Explain generalised advantage estimation.",
     "Explain why a trust region is needed and what TRPO computes.",
     "Explain PPO and why it became the default.",
     "Implement PPO correctly, including the details that matter.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Actor-critic",
   "blurb": "The baseline becomes a second network."},

  {"t": "callout", "title": "Actor-critic is a policy gradient with a learned baseline",
   "kind": "There is nothing more to it",
   "body": ["<b>The actor is the policy, updated by the policy "
            "gradient.</b> <b>The critic is a value function, used as the "
            "baseline</b> (Module 05 §2).",
            "<b>So the critic reduces the actor's gradient variance</b>, "
            "and the actor generates the data the critic learns from.",
            "<b>And the critic lets you bootstrap</b> — use "
            "r + γV(s′) instead of the full return — "
            "<b>which reduces variance further and introduces bias</b>, "
            "which is Module 03 §1's trade exactly.",
            "<b>So actor-critic reintroduces the bootstrapping leg of "
            "the triad</b> (Module 04 §1) — <b>which is why "
            "it is less stable than pure policy gradients and more "
            "sample-efficient. Nothing is free.</b>"]},

  {"t": "eq", "kicker": "GAE", "title": "Generalised advantage estimation",
   "eqs": [
     ("Â = Σ (γλ)ˡ δ_{t+l},   "
      "δ_t = r_t + γV(s_{t+1}) − V(s_t)",
      "An exponentially weighted average of n-step advantage "
      "estimates."),
     ("λ = 0 is one-step TD; λ = 1 is Monte Carlo",
      "So λ is the bias-variance dial, and it is continuous — "
      "Module 03 §3's n-step, made smooth."),
     ("λ ≈ 0.95 and γ ≈ 0.99 are the usual defaults",
      "And they are good defaults, which is unusual in this field."),
   ],
   "caption": "<b>GAE is the single most useful piece of machinery in "
              "modern policy optimisation</b> — it is in every "
              "implementation and it is three lines.",
   "note": "Note that lambda and gamma are separate dials; students "
           "conflate them."},

  {"t": "section", "label": "Part 2", "title": "Why a trust region",
   "blurb": "The problem a step size cannot solve."},

  {"t": "callout", "title": "A large policy update can be unrecoverable",
   "kind": "Why this is worse than in supervised learning",
   "body": ["<b>In supervised learning a bad step raises the loss and "
            "the next step corrects it.</b> The data is unchanged.",
            "<b>In reinforcement learning a bad step changes the policy, "
            "which changes the data distribution</b> — and the agent "
            "may now be collecting experience from a region where it "
            "cannot recover.",
            "<b>So performance collapse is not symmetric</b> and is "
            "frequently permanent within a training run. <b>This is the "
            "'learns then collapses' symptom</b> (Module 04 §4).",
            "<b>A fixed learning rate cannot prevent it</b>, because the "
            "same parameter step produces very different policy changes "
            "depending on where you are — <b>which is why the "
            "constraint has to be on the <i>policy</i>, not on the "
            "parameters.</b>"]},

  {"t": "code", "kicker": "TRPO and PPO", "title": "Constrain the policy change, two ways",
   "lang": "text", "code": """
  TRPO: maximise the surrogate objective subject to
            KL( pi_old || pi_new ) <= delta

      -- a constraint in POLICY space, not parameter space,
         which is the whole point: the same weight change
         means different things in different places.
      -- solved by a conjugate-gradient step using the
         Fisher information matrix (the natural gradient).
      -- Principled, provably monotone improvement under
         its assumptions, and a genuine pain to implement.

  PPO: approximate the same thing with CLIPPING.

      ratio r = pi_new(a|s) / pi_old(a|s)
      objective = min( r * A,  clip(r, 1-e, 1+e) * A )

      If the ratio moves beyond [1-e, 1+e] in the direction
      that would IMPROVE the objective, the gradient is
      CLIPPED TO ZERO. The update stops pushing.
      If it moves in the direction that makes things WORSE,
      it is NOT clipped -- so the policy can always be
      pulled back.

      THAT ASYMMETRY IS THE DESIGN. e = 0.2 typically.

  PPO IS THE DEFAULT because it is twenty lines, uses a
  first-order optimiser, allows several epochs per batch
  (Module 05 Part 3), and performs close to TRPO.
""",
   "caption": "<b>PPO's asymmetric clipping is the detail to "
              "understand</b> — it blocks over-improvement and "
              "permits correction, which is what makes it behave like a "
              "trust region.",
   "note": "Most explanations miss the asymmetry; it is the key."},

  {"t": "section", "label": "Part 3", "title": "Implementing PPO",
   "blurb": "The details that are not in the paper."},

  {"t": "bullets", "kicker": "Details", "title": "What actually determines PPO's performance",
   "items": [
     "<b>Observation and advantage normalisation.</b> <b>Running "
     "normalisation of observations is worth more than most algorithmic "
     "choices.</b>",
     "",
     "<b>Orthogonal initialisation, and a small final-layer gain for "
     "the policy head</b> — so the initial policy is close to "
     "uniform.",
     "",
     "<b>Learning rate annealing</b> to zero over training. "
     "<b>Consistently helps.</b>",
     "",
     "<b>Value loss clipping, gradient norm clipping at 0.5, and a "
     "small entropy bonus.</b>",
     "",
     "<b>And correct handling of episode boundaries in GAE</b> "
     "— <b>bootstrapping across a terminal state is a real bug "
     "that silently costs performance.</b>",
   ],
   "footnote": "<b>These details account for much of the reported "
               "difference between PPO implementations</b>, which is a "
               "finding about the field as much as about the algorithm "
               "(Module 12)."},

  {"t": "callout", "title": "The implementation-detail finding, stated plainly",
   "kind": "What it means for reading papers",
   "body": ["<b>Careful studies have found that PPO's performance "
            "depends heavily on implementation details not described in "
            "the paper</b>, and that some reported algorithmic advances "
            "disappear when the details are matched.",
            "<b>That is a serious finding about the field's evidential "
            "standards</b>, not a minor caveat — and Module 12 "
            "develops it.",
            "<b>The practical response is to compare against a strong "
            "tuned baseline</b> with the details present, rather than "
            "against a paper's reported number.",
            "<b>And to read a reference implementation rather than only "
            "the paper.</b> <b>CleanRL's single-file PPO is the right "
            "one</b>, because nothing is hidden behind a framework."]},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "When PPO, and when not."},

  {"t": "table", "kicker": "Choosing", "title": "PPO against the alternatives",
   "header": ["Situation", "Use", "Why"],
   "widths": [3.2, 3.2, 4.6],
   "rows": [
     ["<b>Fast simulator, parallel envs</b>", "<b>PPO</b>", "<b>Simple, robust, scales with parallelism</b>"],
     ["<b>Samples are expensive</b>", "<b>SAC (M07)</b>", "<b>Off-policy; reuses everything</b>"],
     ["<b>Discrete, small actions, many samples</b>", "<b>DQN variants</b>", "<b>Replay efficiency</b>"],
     ["<b>Very few samples available</b>", "<b>Model-based (M08)</b>", "<b>Orders of magnitude fewer steps</b>"],
     ["<b>A fixed dataset</b>", "<b>Offline RL (M09)</b>", "<b>PPO cannot use it at all</b>"],
   ],
   "footnote": "<b>PPO is the default because it is robust, not because "
               "it is best</b> — it rarely wins on sample efficiency "
               "and it rarely fails outright, which is the right trade "
               "when a simulator is cheap.",
   "note": "'Robust, not best' is the honest characterisation."},
 ],
 "takeaways": [
   "Actor-critic is a policy gradient with a learned baseline, and "
   "bootstrapping through the critic reintroduces the triad's third leg.",
   "GAE's λ is a continuous bias-variance dial separate from γ, "
   "and 0.95 with 0.99 are genuinely good defaults.",
   "A bad policy step changes the data distribution, so collapse is "
   "asymmetric and frequently permanent within a run.",
   "The constraint must be in policy space rather than parameter space, "
   "because the same weight change means different things in different "
   "places.",
   "PPO's clipping is asymmetric: it blocks over-improvement and permits "
   "correction, which is what makes it act as a trust region.",
   "PPO's performance depends heavily on implementation details absent "
   "from the paper, which is a finding about the field's evidential "
   "standards.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Actor-critic"),
  ("callout", "Actor-critic is a policy gradient with a learned baseline",
   ["<b>The actor is the policy, updated by the policy gradient of "
    "Module 05. The critic is a value function, used as the "
    "baseline</b> (Module 05 &sect;2). <b>There is nothing more to the "
    "idea than that</b>, and framing it this way avoids treating it as a "
    "third family of methods.",
    "<b>So the critic reduces the actor's gradient variance</b>, and the "
    "actor generates the on-policy data the critic learns from — a "
    "mutual dependence which is also why both can fail together.",
    "<b>And the critic enables bootstrapping</b> — using r + "
    "&gamma;V(s&prime;) in place of the full episode return — "
    "<b>which reduces variance further and introduces bias</b>, which is "
    "<b>Module 03 &sect;1's trade exactly</b>, now with the dial "
    "exposed as GAE's &lambda;.",
    "<b>So actor-critic reintroduces the bootstrapping leg of the deadly "
    "triad</b> (Module 04 &sect;1) that pure policy gradients did not "
    "have. <b>Which is precisely why it is less stable than REINFORCE "
    "and more sample-efficient than it.</b> <b>Nothing in this field is "
    "free, and tracking which leg of the triad a method reintroduces is "
    "the most reliable way to predict how it will fail.</b>"]),
  ("eq", "&Acirc;<sub>t</sub> = &Sigma;<sub>l</sub> "
         "(&gamma;&lambda;)<super>l</super> &delta;<sub>t+l</sub>, "
         "&nbsp;&nbsp; &delta;<sub>t</sub> = r<sub>t</sub> + "
         "&gamma;V(s<sub>t+1</sub>) &minus; V(s<sub>t</sub>)"),
  ("p", "<b>Generalised advantage estimation is an exponentially weighted "
        "average of every n-step advantage estimate at once.</b> "
        "<b>&lambda; = 0 gives the one-step TD advantage (low variance, "
        "biased) and &lambda; = 1 gives the Monte Carlo advantage "
        "(unbiased, high variance)</b> — so <b>&lambda; is the "
        "bias-variance dial and it is continuous</b>, which is "
        "Module 03 &sect;3's n-step returns made smooth and "
        "differentiable in the parameter. <b>&lambda; &asymp; 0.95 with "
        "&gamma; &asymp; 0.99 are the usual defaults and they are good "
        "ones</b>, which is unusual enough in this field to be worth "
        "noting. <b>And &lambda; and &gamma; are separate dials with "
        "separate jobs</b> — &gamma; sets the effective horizon of "
        "the problem (CSCE 625 Module 10 &sect;1) and &lambda; sets "
        "how much you trust the critic — <b>which students routinely "
        "conflate.</b>"),

  ("h1", "2 &nbsp; Why a trust region"),
  ("callout", "A large policy update can be unrecoverable",
   ["<b>In supervised learning a bad gradient step raises the loss and "
    "the next step corrects it.</b> The training data is unchanged by the "
    "mistake, so the correction is available.",
    "<b>In reinforcement learning a bad step changes the policy, which "
    "changes the data distribution the agent collects</b> — and the "
    "agent may now be gathering experience from a region of the state "
    "space from which it cannot find its way back. <b>The mistake has "
    "destroyed the data that would have corrected it.</b>",
    "<b>So performance collapse is not symmetric with improvement, and "
    "it is frequently permanent within a training run.</b> <b>This is the "
    "'learns, then collapses' symptom of Module 04 &sect;4</b>, and it "
    "is one of the two or three things that make deep reinforcement "
    "learning frustrating in a way supervised learning is not.",
    "<b>A fixed learning rate cannot prevent it</b>, because <b>the same "
    "step in parameter space produces very different changes in the "
    "policy depending on where in parameter space you are</b> — near "
    "a saturated softmax a small weight change barely moves the "
    "distribution, and elsewhere it moves it completely. <b>Which is why "
    "the constraint has to be on the <i>policy</i> rather than on the "
    "parameters</b>, and that single observation is the motivation for "
    "everything in &sect;2 and &sect;3."]),
  ("code", """TRPO: maximise the surrogate objective subject to
          KL( pi_old || pi_new ) <= delta

    -- a constraint in POLICY space, not parameter space,
       which is the entire point (see the callout).
    -- solved by a conjugate-gradient step using the Fisher
       information matrix, which is the natural gradient --
       CSCE 669 Module 07's second-order idea, with the
       metric supplied by the policy's own geometry.
    -- Principled, with provably monotone improvement under
       its assumptions, and a genuine pain to implement.

PPO: approximate the same thing with CLIPPING.

    ratio r = pi_new(a|s) / pi_old(a|s)
    objective = min( r * A,  clip(r, 1-e, 1+e) * A )

    If the ratio moves beyond [1-e, 1+e] in the direction
    that would IMPROVE the objective, the gradient is
    CLIPPED TO ZERO -- the update simply stops pushing
    further.
    If it moves in the direction that makes the objective
    WORSE, it is NOT clipped -- so the policy can always be
    pulled back from a bad place.

    THAT ASYMMETRY IS THE DESIGN, and most explanations
    omit it. e = 0.2 typically.

PPO IS THE DEFAULT because it is about twenty lines, uses
an ordinary first-order optimiser, allows several epochs of
updates per collected batch (Module 05 section 3's partial
data reuse), and performs close to TRPO on most tasks."""),

  ("break",),
  ("h1", "3 &nbsp; Implementing PPO"),
  ("ul", ["<b>Observation and advantage normalisation.</b> <b>Running "
          "normalisation of observations is worth more than most "
          "algorithmic choices</b> — CSCE 633 Module 02's feature "
          "scaling and CSCE 669 Module 05 &sect;2's conditioning "
          "argument, both arriving as the highest-value implementation "
          "detail in the algorithm.",
          "<b>Orthogonal weight initialisation, with a small gain on the "
          "policy head's final layer</b> — typically 0.01 — "
          "<b>so that the initial policy is close to uniform</b> rather "
          "than arbitrarily committed, which protects early exploration.",
          "<b>Learning rate annealing to zero over the course of "
          "training.</b> <b>Consistently helps</b>, and it is "
          "CSCE 669 Module 08 &sect;2's noise-floor argument: the "
          "step must shrink for the policy to settle.",
          "<b>Value loss clipping, gradient norm clipping at "
          "0.5, and a small entropy bonus</b> (Module 05 &sect;4, "
          "Module 07 &sect;3).",
          "<b>And correct handling of episode boundaries in the GAE "
          "computation.</b> <b>Bootstrapping V(s&prime;) across a "
          "terminal state is a real bug</b> — the value after "
          "termination is zero, not whatever the critic says — "
          "<b>and it silently costs performance without producing any "
          "error</b>. It is the single most common PPO implementation bug "
          "and it is worth checking first."]),
  ("callout", "The implementation-detail finding, stated plainly",
   ["<b>Careful replication studies have found that PPO's performance "
    "depends heavily on implementation details that are not described in "
    "the paper</b>, and that <b>some reported algorithmic advances over "
    "it disappear once those details are matched between the methods "
    "being compared.</b>",
    "<b>That is a serious finding about the field's evidential "
    "standards</b> rather than a minor caveat about one algorithm "
    "— it means a substantial fraction of the published comparison "
    "literature may be comparing implementations rather than ideas. "
    "<b>Module 12 develops this properly.</b>",
    "<b>The practical response is to compare against a strong, tuned "
    "baseline with the details present</b>, rather than against a number "
    "reported in a paper whose implementation you have not read. <b>This "
    "is CSCE 633 Module 02's baseline discipline with a specific and "
    "well-documented reason attached.</b>",
    "<b>And to read a reference implementation rather than only the "
    "paper.</b> <b>CleanRL's single-file PPO is the right one</b>, "
    "because nothing is hidden behind a framework abstraction and every "
    "detail in the list above is visible in sequence. <b>Reading it "
    "carefully once is worth more than reading three more papers.</b>"]),

  ("h1", "4 &nbsp; Choosing"),
  ("table", ["Situation", "Use", "Why"],
   [["<b>A fast simulator and many parallel environments</b>",
     "<b>PPO.</b>",
     "<b>Simple, robust, and it scales well with parallel collection</b> "
     "— which is what the large batches of Module 05 &sect;4 "
     "require."],
    ["<b>Samples are expensive</b>", "<b>SAC</b> (Module 07).",
     "<b>Off-policy, so a replay buffer reuses every transition</b> many "
     "times."],
    ["<b>Discrete, small action space, and many samples "
     "available</b>", "<b>DQN and its variants</b> (Module 04).",
     "<b>Replay efficiency, and the max over actions is cheap.</b>"],
    ["<b>Very few samples available at all</b>",
     "<b>Model-based methods</b> (Module 08).",
     "<b>Orders of magnitude fewer environment steps</b>, at the cost of "
     "model-exploitation risk."],
    ["<b>A fixed logged dataset and no interaction</b>",
     "<b>Offline reinforcement learning</b> (Module 09).",
     "<b>PPO cannot use it at all</b>, because it is on-policy and the "
     "data is not from its policy."]],
   [0.30, 0.25, 0.45]),
  ("p", "<b>PPO is the default because it is robust, not because it is "
        "best.</b> <b>It rarely wins on sample efficiency and it rarely "
        "fails outright</b> — which is the right trade when a "
        "simulator is cheap and your time is not, and it is the wrong "
        "trade when environment steps are the scarce resource. <b>Stating "
        "it as 'robust, not best' is the honest characterisation</b>, and "
        "it is how practitioners actually describe it."),
 ],
 "resources": [
   ("Schulman et al. &mdash; Proximal Policy Optimization Algorithms "
    "(free)",
    "https://arxiv.org/abs/1707.06347",
    "<b>PPO.</b> Short, and read it alongside &sect;3's detail list "
    "rather than alone."),
   ("Schulman et al. &mdash; Trust Region Policy Optimization (free)",
    "https://arxiv.org/abs/1502.05477",
    "<b>&sect;2's principled version</b>, with the monotone improvement "
    "argument that PPO approximates."),
   ("Engstrom et al. &mdash; Implementation Matters in Deep Policy "
    "Gradients (free)",
    "https://arxiv.org/abs/2005.12729",
    "<b>&sect;3's finding, measured</b> — and the paper that should "
    "change how you read comparisons in this field."),
   ("CleanRL &mdash; ppo.py and the PPO implementation-details blog "
    "(free)",
    "https://docs.cleanrl.dev/rl-algorithms/ppo/",
    "<b>Every detail from &sect;3, enumerated and benchmarked.</b> The "
    "single most useful page in this course."),
 ],
 "exercises": [
   "<b>Implement advantage actor-critic</b> and compare against "
   "REINFORCE with a baseline.",
   "<b>Implement GAE</b> and sweep λ from 0 to 1. Plot performance "
   "and advantage variance.",
   "<b>Confirm λ = 0 and λ = 1 reduce</b> to one-step TD and "
   "Monte Carlo.",
   "<b>Cause a policy collapse deliberately</b> with a large learning "
   "rate, and confirm it does not recover.",
   "<b>Implement PPO from scratch</b> and match CleanRL's CartPole "
   "performance.",
   "<b>Remove the clipping</b> and report what happens.",
   "<b>Remove the asymmetry</b> (clip both directions) and report the "
   "difference.",
   "<b>Ablate each of &sect;3's five details</b> and report the effect of "
   "each.",
   "<b>Introduce the terminal-state bootstrapping bug</b> and measure the "
   "performance cost.",
   "<b>Compare your PPO against a tuned reference</b> across five seeds, "
   "and report honestly.",
 ],
 "selfcheck": [
   "What is actor-critic, and which triad leg does it reintroduce?",
   "What does GAE's λ control, and how does it differ from "
   "γ?",
   "Why is a bad policy step worse than a bad supervised step?",
   "Why must the constraint be in policy space?",
   "What does TRPO compute, and what makes it hard?",
   "State PPO's objective and explain the asymmetry.",
   "Name five implementation details that determine PPO's performance.",
   "What is the implementation-detail finding, and what should you do "
   "about it?",
   "Give five situations and the algorithm for each.",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Continuous Control",
 "subtitle": "When you cannot enumerate the actions.",
 "question": "What changes when the action is a vector of real numbers?",
 "outcomes": [
     "Explain why value-based methods fail in continuous action "
     "spaces.",
     "Explain deterministic policy gradients and DDPG's structure.",
     "Explain TD3's three fixes and what each addresses.",
     "Explain maximum-entropy reinforcement learning and SAC.",
     "Choose an algorithm for a continuous control problem.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The obstruction",
   "blurb": "One max, and it is no longer computable."},

  {"t": "callout", "title": "The max over actions is the whole difficulty",
   "kind": "Why continuous control needs new algorithms",
   "body": ["<b>Q-learning's target contains maxₐ Q(s′,a)</b> "
            "(Module 03 §2). <b>With discrete actions you "
            "enumerate; with a real-valued action vector you cannot.</b>",
            "<b>And solving that maximisation at every step is an "
            "optimisation problem per transition</b> — which is "
            "CSCE 669's subject, run millions of times, inside the "
            "inner loop.",
            "<b>Two ways out.</b> <b>Policy gradients never needed the "
            "max</b> (Module 05) — a Gaussian policy outputs a mean "
            "and a spread, and that is continuous already.",
            "<b>Or learn a network that <i>outputs</i> the "
            "maximiser</b>, and train it by gradient ascent through "
            "Q — <b>which is the deterministic policy gradient, and "
            "it is a genuinely neat idea.</b>"]},

  {"t": "code", "kicker": "DDPG", "title": "Learn the argmax with a second network",
   "lang": "text", "code": """
  TWO NETWORKS:
      a CRITIC Q(s,a), trained by the usual TD error
      an ACTOR mu(s), trained to OUTPUT the action that
          maximises the critic

  THE ACTOR'S UPDATE IS JUST THE CHAIN RULE:
      grad_theta Q(s, mu(s)) = grad_a Q * grad_theta mu

  The critic is differentiable in the ACTION, so you can
  back-propagate through it into the actor. The actor
  becomes a learned argmax.
      -- which also means the actor is only as good as the
         critic's action-gradient, and a critic that is
         wrong in a region will confidently push the actor
         there.

  DDPG = this, plus a replay buffer and target networks
  (Module 04), plus exploration noise added to the actor's
  output since a deterministic policy does not explore.

  AND IT IS NOTORIOUSLY BRITTLE:
      very hyperparameter-sensitive
      the critic OVERESTIMATES (Module 03 Part 4) and the
          actor exploits exactly the overestimate
      results vary enormously across seeds (Module 12)

  So it is important historically and is not what you
  should use. Part 2 and Part 3 are.
""",
   "caption": "<b>The actor-exploits-the-critic's-error loop is the "
              "specific failure</b>, and both TD3 and SAC are "
              "principally responses to it.",
   "note": "Saying plainly that DDPG is not the recommendation is more "
           "useful than presenting it neutrally."},

  {"t": "section", "label": "Part 2", "title": "TD3",
   "blurb": "Three targeted fixes."},

  {"t": "table", "kicker": "TD3", "title": "Each fix, and what it addresses",
   "header": ["Fix", "Mechanism", "Addresses"],
   "widths": [2.8, 4.1, 5.1],
   "rows": [
     ["<b>Clipped double Q</b>", "<b>Two critics; use the MINIMUM in the target</b>", "<b>Overestimation (M03 §4), now deliberately pessimistic</b>"],
     ["<b>Delayed policy update</b>", "<b>Update the actor every d critic updates</b>", "<b>The actor chasing a critic that is still moving</b>"],
     ["<b>Target policy smoothing</b>", "<b>Add noise to the action in the target</b>", "<b>Sharp critic peaks the actor would exploit</b>"],
   ],
   "footnote": "<b>All three address the same underlying problem:</b> "
               "<b>the actor exploits the critic's errors</b>, so make "
               "the critic pessimistic, slow the actor down, and smooth "
               "the critic's peaks.",
   "note": "That all three attack one problem is the insight worth "
           "stating."},

  {"t": "section", "label": "Part 3", "title": "Soft actor-critic",
   "blurb": "Make entropy part of the objective."},

  {"t": "callout", "title": "Maximum-entropy reinforcement learning",
   "kind": "The reframing SAC is built on",
   "body": ["<b>Maximise expected return <i>plus</i> policy "
            "entropy:</b> J = E[Σ r + α·H(π(·|s))].",
            "<b>So the agent is rewarded for keeping its options "
            "open</b>, and exploration becomes part of the objective "
            "rather than a separate mechanism bolted beside it.",
            "<b>Which gives three things at once:</b> sustained "
            "exploration, robustness (a policy that must stay stochastic "
            "cannot depend on one narrow behaviour), and far less "
            "hyperparameter sensitivity than DDPG.",
            "<b>And α is auto-tuned</b> against a target entropy "
            "in modern SAC — <b>which removes the one hyperparameter "
            "the reframing introduced</b>, and is a large part of why SAC "
            "is pleasant to use."]},

  {"t": "table", "kicker": "Comparison", "title": "The continuous control options",
   "header": ["", "PPO", "TD3", "SAC"],
   "widths": [2.1, 3.1, 3.1, 3.0],
   "rows": [
     ["<b>Policy</b>", "<b>Stochastic</b>", "<b>Deterministic</b>", "<b>Stochastic</b>"],
     ["<b>Data</b>", "<b>On-policy</b>", "<b>Off-policy</b>", "<b>Off-policy</b>"],
     ["<b>Sample efficiency</b>", "<b>Low</b>", "<b>High</b>", "<b>High</b>"],
     ["<b>Robustness</b>", "<b>High</b>", "<b>Medium</b>", "<b>High</b>"],
     ["<b>Tuning needed</b>", "<b>Little</b>", "<b>Some</b>", "<b>Very little</b>"],
     ["<b>Best when</b>", "<b>Simulator is cheap</b>", "<b>Deterministic optimum</b>", "<b>The default</b>"],
   ],
   "footnote": "<b>SAC is the sensible default for continuous "
               "control</b>, and PPO is the default when you have "
               "massive parallel simulation and value robustness over "
               "sample efficiency.",
   "note": "Give a clear recommendation; students want one and it is "
           "defensible."},

  {"t": "section", "label": "Part 4", "title": "Practice",
   "blurb": "What matters in a continuous control task."},

  {"t": "bullets", "kicker": "Practice", "title": "Continuous control in practice",
   "items": [
     "<b>Normalise the action space to [−1, 1]</b> and scale "
     "outside the agent. <b>Mismatched action scales are a frequent, "
     "silent failure.</b>",
     "",
     "<b>Normalise observations with a running mean and variance</b> "
     "— the single most valuable implementation detail here too.",
     "",
     "<b>Use a squashed Gaussian policy</b> (tanh on a Gaussian "
     "sample) <b>and correct the log-probability for the squashing.</b> "
     "Forgetting the correction is a real bug.",
     "",
     "<b>Reward scale matters more than it should.</b> <b>A reward "
     "scaled by 1000 changes the effective learning rate</b> through the "
     "critic's targets.",
     "",
     "<b>And if your real system is a robot, read Module 08 and "
     "Module 09 first.</b>",
   ],
   "footnote": "<b>The action-scale and log-probability-correction bugs "
               "are both silent</b> — the agent trains, slowly and "
               "badly, with no error to find."},

  {"t": "callout", "title": "Simulation to reality",
   "kind": "The honest status for physical systems",
   "body": ["<b>Training on a real robot is usually infeasible</b> at "
            "the sample counts of Module 01 §2 — so you train "
            "in simulation and transfer.",
            "<b>And the simulation is wrong</b>, in friction, contact, "
            "latency, and actuator dynamics. <b>A policy trained on it "
            "exploits the inaccuracies</b>, which is CSCE 669 "
            "Module 12 §4 again.",
            "<b>Domain randomisation is the standard answer:</b> "
            "randomise the simulator's parameters so the policy must work "
            "across a range, including the real one.",
            "<b>It works, imperfectly, and it costs sample "
            "efficiency</b> — the policy becomes conservative. "
            "<b>Report the real-system performance, not the simulated "
            "one</b>, which is the only number that means anything."]},
 ],
 "takeaways": [
   "The max over actions is the whole difficulty: with a real-valued "
   "action vector it is an optimisation problem per transition.",
   "DDPG learns a network that outputs the maximiser and trains it by "
   "back-propagating through the critic — and the actor then exploits "
   "the critic's errors.",
   "TD3's three fixes all address that one problem: make the critic "
   "pessimistic, slow the actor, and smooth the critic's peaks.",
   "SAC adds policy entropy to the objective, so exploration is part of "
   "what is optimised rather than bolted beside it.",
   "SAC is the sensible default for continuous control, and PPO is the "
   "default when massive parallel simulation is available.",
   "Action-scale mismatch and a missing tanh log-probability correction "
   "are both silent bugs that merely make training bad.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The obstruction"),
  ("callout", "The max over actions is the whole difficulty",
   ["<b>Q-learning's target contains max<sub>a</sub> Q(s&prime;,a)</b> "
    "(Module 03 &sect;2). <b>With a small discrete action set you "
    "enumerate it; with a real-valued action vector you cannot.</b>",
    "<b>And solving that maximisation properly at every step is an "
    "optimisation problem per transition</b> — which is "
    "CSCE 669's entire subject, executed millions of times inside the "
    "inner loop of a training run. <b>Not impossible, and not "
    "affordable.</b>",
    "<b>There are two ways out.</b> <b>Policy gradients never needed "
    "the max at all</b> (Module 05) — a Gaussian policy outputs a "
    "mean and a standard deviation, which is a continuous action "
    "distribution by construction, and the gradient flows through the "
    "log-probability. <b>So PPO works on continuous control with no "
    "modification whatsoever</b>, which is worth noting before "
    "introducing anything new.",
    "<b>Or learn a network that <i>outputs</i> the maximiser</b>, and "
    "train that network by gradient ascent through the critic — "
    "<b>which is the deterministic policy gradient, and it is a genuinely "
    "neat idea</b>: the argmax becomes a learned function rather than a "
    "computation."]),
  ("code", """TWO NETWORKS:
    a CRITIC Q(s,a), trained by the usual TD error
    an ACTOR mu(s), trained to OUTPUT the action that
        maximises the critic

THE ACTOR'S UPDATE IS JUST THE CHAIN RULE:
    grad_theta Q(s, mu(s)) = grad_a Q * grad_theta mu

The critic is differentiable in the ACTION, so you can
back-propagate through it into the actor's parameters. The
actor becomes a learned argmax.
    -- which also means the actor is only as good as the
       critic's action-gradient, and A CRITIC THAT IS WRONG
       IN SOME REGION WILL CONFIDENTLY PUSH THE ACTOR
       THERE. That loop is the specific failure mode.

DDPG = this, plus a replay buffer and target networks
(Module 04), plus exploration noise added to the actor's
output -- because a deterministic policy does not explore
at all on its own.

AND IT IS NOTORIOUSLY BRITTLE:
    very sensitive to hyperparameters
    the critic OVERESTIMATES (Module 03 section 4) and
        the actor exploits exactly the overestimate, which
        is the worst possible interaction
    results vary enormously across random seeds
        (Module 12)

So DDPG is important historically and is NOT what you
should use. Sections 2 and 3 are."""),

  ("h1", "2 &nbsp; TD3"),
  ("table", ["Fix", "Mechanism", "What it addresses"],
   [["<b>Clipped double Q-learning</b>",
     "<b>Train two critics and use the <i>minimum</i> of the two in the "
     "target.</b>",
     "<b>Overestimation</b> (Module 03 &sect;4) — and note this "
     "goes beyond unbiasing: <b>it is deliberately pessimistic</b>, "
     "because an underestimate is far safer than an overestimate when the "
     "actor is going to exploit whichever way the error points."],
    ["<b>Delayed policy update</b>",
     "<b>Update the actor once every d critic updates</b> (d = 2 "
     "typically).",
     "<b>The actor chasing a critic that is still moving</b> — which "
     "is Module 06 &sect;2's moving-target problem inside the "
     "actor-critic loop."],
    ["<b>Target policy smoothing</b>",
     "<b>Add clipped noise to the action used in the target "
     "computation.</b>",
     "<b>Sharp spurious peaks in the critic that the actor would "
     "exploit</b> — averaging over a small action neighbourhood "
     "makes the critic's surface smoother and the peaks less "
     "attractive."]],
   [0.22, 0.33, 0.45]),
  ("p", "<b>All three fixes address the same underlying problem:</b> "
        "<b>the actor exploits the critic's errors.</b> So <b>make the "
        "critic pessimistic, slow the actor down relative to the critic, "
        "and smooth the critic's peaks</b> — three independent "
        "attacks on one failure mode. <b>Noticing that is more useful "
        "than memorising the three names</b>, and it is a good example of "
        "a method whose components look miscellaneous and are not."),

  ("break",),
  ("h1", "3 &nbsp; Soft actor-critic"),
  ("callout", "Maximum-entropy reinforcement learning",
   ["<b>Maximise expected return <i>plus</i> policy entropy:</b> "
    "J = E[&Sigma; r<sub>t</sub> + &alpha;&middot;H(&pi;(&middot;|"
    "s<sub>t</sub>))]. <b>The entropy term is in the objective, not "
    "added to the reward as a bonus.</b>",
    "<b>So the agent is rewarded for keeping its options open</b>, and "
    "<b>exploration becomes part of what is being optimised rather than a "
    "separate mechanism bolted on beside it</b> (Module 02's "
    "&epsilon;-greedy and noise injection are both bolted on).",
    "<b>Which gives three things at once:</b> sustained exploration "
    "without a schedule; <b>robustness, because a policy that must remain "
    "stochastic cannot depend on one narrow precisely-tuned behaviour</b>; "
    "and markedly less hyperparameter sensitivity than DDPG, which is the "
    "property practitioners actually notice first.",
    "<b>And &alpha; is auto-tuned against a target entropy in modern "
    "SAC</b>, by treating the entropy constraint as a dual problem "
    "(CSCE 669 Module 06's Lagrangian) — <b>which removes the one "
    "hyperparameter the reframing introduced</b>, and is a large part of "
    "why SAC is pleasant to use in a way its predecessors are not."]),
  ("table", ["", "PPO", "TD3", "SAC"],
   [["<b>Policy</b>", "<b>Stochastic.</b>", "<b>Deterministic.</b>",
     "<b>Stochastic, with entropy in the objective.</b>"],
    ["<b>Data</b>", "<b>On-policy</b> — discards batches.",
     "<b>Off-policy</b> — replay buffer.", "<b>Off-policy.</b>"],
    ["<b>Sample efficiency</b>", "<b>Low.</b>", "<b>High.</b>",
     "<b>High.</b>"],
    ["<b>Robustness</b>", "<b>High.</b>", "<b>Medium.</b>",
     "<b>High.</b>"],
    ["<b>Tuning required</b>", "<b>Little.</b>", "<b>Some.</b>",
     "<b>Very little.</b>"],
    ["<b>Best when</b>",
     "<b>The simulator is cheap and massively parallel.</b>",
     "<b>The optimal policy really is deterministic.</b>",
     "<b>The default choice.</b>"]],
   [0.17, 0.28, 0.27, 0.28]),
  ("p", "<b>SAC is the sensible default for continuous control</b>, and "
        "<b>PPO is the default when you have massive parallel simulation "
        "and value robustness over sample efficiency</b> — which is "
        "the situation in large-scale simulated robotics and in most game "
        "applications. <b>Giving a clear recommendation is defensible "
        "here</b>, which is not true of every choice in this course."),

  ("h1", "4 &nbsp; Practice"),
  ("ul", ["<b>Normalise the action space to [&minus;1, 1]</b> and scale "
          "to physical units outside the agent. <b>Mismatched action "
          "scales are a frequent and entirely silent failure</b> — "
          "an agent whose policy output saturates at a tenth of the usable "
          "range trains slowly and badly with nothing to indicate why.",
          "<b>Normalise observations with a running mean and "
          "variance</b>, updated online — <b>the single most "
          "valuable implementation detail here as in Module 06 "
          "&sect;3</b>, and for the same conditioning reason.",
          "<b>Use a squashed Gaussian policy</b> — sample from a "
          "Gaussian and apply tanh — <b>and correct the "
          "log-probability for the squashing</b> (the change-of-variables "
          "Jacobian). <b>Forgetting the correction is a real bug</b> that "
          "makes the entropy term wrong and the policy "
          "over-deterministic, and it produces no error message.",
          "<b>Reward scale matters more than it should.</b> <b>A reward "
          "scaled by a thousand changes the magnitude of the critic's "
          "targets and therefore the effective learning rate</b> — so "
          "normalise or scale rewards deliberately rather than inheriting "
          "whatever the environment emits.",
          "<b>And if your target is a real physical system, read "
          "Module 08 and Module 09 before starting</b>, because the "
          "sample counts in Module 01 &sect;2 make direct training "
          "infeasible and the alternatives have their own "
          "requirements."]),
  ("callout", "Simulation to reality",
   ["<b>Training on a real robot is usually infeasible</b> at the sample "
    "counts of Module 01 &sect;2 — millions of steps at one step "
    "per second is weeks of continuous operation, with wear and safety "
    "costs — <b>so you train in simulation and transfer.</b>",
    "<b>And the simulation is wrong.</b> Friction, contact dynamics, "
    "actuator latency, sensor noise, and compliance are all approximated, "
    "and <b>a policy trained on the simulator exploits the "
    "inaccuracies</b> — it finds the contact configuration the "
    "physics engine handles badly and builds its behaviour on it. <b>This "
    "is CSCE 669 Module 12 &sect;4 and Module 01 &sect;3's "
    "model-exploitation problem, in its most expensive form.</b>",
    "<b>Domain randomisation is the standard answer:</b> randomise the "
    "simulator's physical parameters across every episode so that <b>the "
    "policy must work across a range of dynamics, with the real system's "
    "parameters somewhere inside that range.</b> A policy that cannot "
    "rely on a specific friction coefficient cannot exploit a wrong one.",
    "<b>It works, imperfectly, and it costs sample efficiency</b> "
    "— the policy becomes conservative, because it must be robust to "
    "dynamics it is not currently experiencing. <b>And report the "
    "real-system performance rather than the simulated one</b>, which is "
    "<b>the only number that means anything</b> and is the one most "
    "frequently omitted."]),
 ],
 "resources": [
   ("Haarnoja et al. &mdash; Soft Actor-Critic (free)",
    "https://arxiv.org/abs/1801.01290",
    "<b>&sect;3's method</b>, with the maximum-entropy framing derived "
    "and the auto-tuned temperature in the follow-up paper."),
   ("Fujimoto et al. &mdash; Addressing Function Approximation Error in "
    "Actor-Critic Methods (TD3) (free)",
    "https://arxiv.org/abs/1802.09477",
    "<b>&sect;2's three fixes</b>, with the overestimation analysis that "
    "motivates all three."),
   ("Lillicrap et al. &mdash; Continuous control with deep "
    "reinforcement learning (DDPG) (free)",
    "https://arxiv.org/abs/1509.02971",
    "<b>&sect;1's deterministic policy gradient</b> — read for the "
    "idea, not as a recommendation."),
   ("Tobin et al. &mdash; Domain Randomization (free)",
    "https://arxiv.org/abs/1703.06907",
    "<b>&sect;4's transfer method</b>, and a clear statement of the "
    "reality-gap problem it addresses."),
 ],
 "exercises": [
   "<b>Try to run DQN on a continuous action space</b> and articulate "
   "exactly where it fails.",
   "<b>Run PPO on a continuous control task</b> with no modification, and "
   "confirm it works.",
   "<b>Implement DDPG</b> and run five seeds. Report the spread.",
   "<b>Plot the critic's Q-values over training</b> and look for "
   "overestimation.",
   "<b>Add clipped double Q</b> and report the change in Q-values and "
   "performance.",
   "<b>Add each of TD3's other two fixes</b> separately and report each "
   "effect.",
   "<b>Implement SAC</b> and compare sample efficiency against PPO on the "
   "same task.",
   "<b>Omit the tanh log-probability correction</b> and report what "
   "happens to the entropy.",
   "<b>Scale the reward by 1000</b> and report the effect on learning.",
   "<b>Randomise a simulator parameter</b> and compare the policy's "
   "robustness with and without.",
 ],
 "selfcheck": [
   "Why does the max over actions obstruct value-based methods?",
   "Name two ways around it.",
   "Explain the deterministic policy gradient and its chain rule.",
   "What is DDPG's specific failure loop?",
   "Name TD3's three fixes and the single problem they all address.",
   "State the maximum-entropy objective and the three things it buys.",
   "Why is α auto-tuned, and by what mechanism?",
   "Compare PPO, TD3, and SAC on six axes and give a default.",
   "Name two silent bugs specific to continuous control.",
   "What is domain randomisation, what does it cost, and what should you "
   "report?",
 ],
},

]
