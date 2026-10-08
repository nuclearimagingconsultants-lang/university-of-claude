# -*- coding: utf-8 -*-
"""CSCE 642 Deep Reinforcement Learning — original course content."""

COURSE = {
    "code": "CSCE 642",
    "title": "Deep Reinforcement Learning",
    "tagline": "The same Bellman equation as CSCE 625, with the model "
               "unknown and the table replaced by a network",
    "term": "Semester 7 (with CSCE 753 and CSCE 625)",
    "prereqs": "CSCE 625 Modules 09–10 for MDPs, CSCE 636 for "
               "deep networks, CSCE 669 Modules 05 and 08 for the "
               "optimisation; probability",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A working agent on a task you chose, trained across "
                   "at least five random seeds, reported with variance, "
                   "compared against a non-learned baseline, and "
                   "accompanied by an honest statement of whether "
                   "learning was the right approach",
    "description": [
        "<b>CSCE 625 Module 10 solved Markov decision processes by "
        "computation, with the model known and the value function in a "
        "table.</b> <b>This course removes both.</b> The agent does not "
        "know the transition probabilities or the rewards, and the state "
        "space is far too large to tabulate — <b>so it must learn "
        "from interaction and approximate with a network.</b>",
        "<b>Every difficulty in this course traces to one of those two "
        "substitutions</b>, which is the most useful organising fact "
        "available. <b>Not knowing the model causes sample "
        "inefficiency and makes exploration a problem</b> (Modules 02 "
        "and 08). <b>Replacing the table with an approximator causes "
        "instability and destroys the convergence guarantees</b> "
        "(Module 04).",
        "<b>The second theme is that reward specification is the hard "
        "part.</b> CSCE 625 Module 01 made the point in the abstract; "
        "<b>here it has teeth, because a reinforcement learning agent "
        "optimises its reward with far more ingenuity and less restraint "
        "than a search does</b>. <b>Module 10 is entirely about this</b>, "
        "and it is the module with the most practical consequence.",
        "<b>The third is that this field has a serious reproducibility "
        "problem, and the course does not soften it.</b> "
        "<b>Module 12 is about variance across random seeds, which in "
        "reinforcement learning is routinely larger than the differences "
        "between published methods</b> — a situation that makes most "
        "single-seed comparisons uninformative, and that you need to know "
        "before reading the literature.",
        "<b>And the closing position is scoped rather than "
        "enthusiastic.</b> <b>Module 13 states where reinforcement "
        "learning demonstrably works, where it does not, and how to tell "
        "which case you are in</b> — because <b>the honest answer is "
        "that CSCE 625's methods are the right choice far more often "
        "than this field's literature suggests</b>, and knowing when to "
        "use neither is part of knowing the subject.",
    ],
    "outcomes": [
        "State precisely what reinforcement learning adds to CSCE 625's "
        "MDP.",
        "Explain the exploration-exploitation trade and the standard "
        "strategies.",
        "Derive temporal-difference learning and distinguish on-policy "
        "from off-policy.",
        "Explain the deadly triad and the mechanisms that stabilise deep "
        "Q-learning.",
        "Derive the policy gradient and explain variance reduction.",
        "Explain trust-region methods and why PPO is the default.",
        "Choose an algorithm for continuous control and explain the "
        "entropy term.",
        "Explain model-based methods and their sample-efficiency "
        "argument.",
        "Explain offline reinforcement learning and why naive "
        "off-policy learning fails there.",
        "Design a reward and anticipate how it will be gamed.",
        "Evaluate an agent across seeds and report variance honestly.",
        "State whether reinforcement learning is the right approach for "
        "a given problem.",
    ],
    "materials": [
        ("Sutton & Barto — Reinforcement Learning: An "
         "Introduction, 2nd edition (free PDF)",
         "http://incompleteideas.net/book/the-book.html",
         "<b>The primary source, free from the authors.</b> Chapters 2, "
         "5–7, 9–13 are Modules 02–06; chapters 3–4 "
         "were CSCE 625 Module 10, which is why the two courses share "
         "one book."),
        ("OpenAI Spinning Up in Deep RL (free)",
         "https://spinningup.openai.com/",
         "<b>The best free practical introduction</b> — clean "
         "reference implementations of the Module 05–07 algorithms, "
         "with the derivations and an unusually honest discussion of what "
         "is hard."),
        ("Berkeley CS285 — Deep Reinforcement Learning (free "
         "lectures and homework)",
         "https://rail.eecs.berkeley.edu/deeprlcourse/",
         "<b>The graduate course this one follows most closely.</b> Full "
         "video lectures and assignments; Modules 05–09 track it."),
        ("Henderson et al. — Deep Reinforcement Learning That "
         "Matters (free)",
         "https://arxiv.org/abs/1709.06560",
         "<b>Module 12's source.</b> The seed-variance measurements that "
         "should change how you read every other paper in the field."),
        ("Agarwal et al. — Deep RL at the Edge of the Statistical "
         "Precipice (free)",
         "https://arxiv.org/abs/2108.13264",
         "<b>How to report reinforcement learning results properly</b> "
         "— Module 12's recommended practice, with the statistical "
         "argument and free tooling."),
        ("Gymnasium, Stable-Baselines3, and CleanRL (free)",
         "https://gymnasium.farama.org/",
         "<b>The working toolkit.</b> <b>CleanRL's single-file "
         "implementations are the ones to read</b> — every algorithm "
         "in one file, with the implementation details that papers "
         "omit."),
    ],
    "tooling": [
        "<b>Gymnasium for environments</b>, and <b>start with "
        "CartPole and a tabular grid world rather than Atari</b> "
        "— <b>a bug in your algorithm is diagnosable in five "
        "seconds on CartPole and invisible for six hours on Atari.</b>",
        "<b>CleanRL as a reference</b>, not a dependency. <b>Read its "
        "PPO implementation line by line</b>; the differences between it "
        "and the paper are the things that actually matter.",
        "<b>A 4 GB GPU is adequate for this entire course.</b> "
        "<b>Reinforcement learning is bottlenecked on environment "
        "steps, not on gradient computation</b> — which is good "
        "news for the hardware and bad news for the wall-clock time.",
        "<b>Seed control and logging from the first line of code.</b> "
        "<b>Module 12 requires five seeds per configuration and "
        "retrofitting that is painful</b>, so build it in at the "
        "start.",
        "<b>Weights and Biases or TensorBoard</b>, logging episode "
        "return, episode length, loss, gradient norm, and the entropy or "
        "exploration parameter. <b>All five, from the beginning.</b>",
        "<b>Patience, and a non-learned baseline.</b> <b>Every "
        "experiment in this course should be compared against the "
        "CSCE 625 method for the same task</b>, and sometimes the "
        "baseline wins.",
    ],
    "projects": [
        {"title": "Implement and diagnose", "after": 7,
         "brief": "Implement value-based and policy-gradient methods "
                  "from scratch, and diagnose them rather than merely "
                  "running them.",
         "reqs": [
             "<b>Tabular Q-learning and SARSA</b> on a grid world, with "
             "the on-policy/off-policy difference demonstrated on the "
             "cliff-walking task.",
             "<b>DQN from scratch</b> on CartPole, with replay and a "
             "target network, and an ablation of each.",
             "<b>REINFORCE with and without a baseline</b>, with the "
             "gradient variance measured.",
             "<b>PPO from scratch</b>, matching a reference "
             "implementation's performance.",
             "<b>Five seeds for every configuration</b>, with the "
             "spread plotted rather than the mean alone.",
             "<b>A learning curve that fails</b>, diagnosed to a "
             "specific cause.",
         ],
         "done": [
             "<b>The cliff-walking difference reproduced and "
             "explained</b> — it is the clearest demonstration of "
             "on-policy against off-policy that exists.",
             "<b>Each DQN ablation's effect measured</b>, not asserted.",
             "<b>Gradient variance reported with and without the "
             "baseline</b>, as numbers.",
             "<b>Five seeds everywhere, with the spread shown</b>, "
             "which is the graded discipline.",
         ]},
        {"title": "An agent on your own task", "after": 12,
         "brief": "Apply reinforcement learning to a problem you chose, "
                  "and establish honestly whether it was the right "
                  "approach.",
         "reqs": [
             "<b>A task you care about</b>, with the state, action, and "
             "reward design written out and justified.",
             "<b>A non-learned baseline</b> from CSCE 625 — "
             "scripted, planned, or searched.",
             "<b>At least five seeds</b>, reported with interquartile "
             "means and confidence intervals.",
             "<b>A reward-gaming attempt</b>: find a behaviour that "
             "scores well and is not what you wanted.",
             "<b>An evaluation under a changed environment</b>, not just "
             "the training one.",
             "<b>Sample count and wall-clock time</b> reported.",
         ],
         "done": [
             "<b>The baseline comparison honest, including if the "
             "baseline wins</b> — which is a complete and "
             "respectable result.",
             "<b>Seed variance reported properly</b>, by Module 12's "
             "standard.",
             "<b>At least one reward-gaming behaviour found and "
             "described</b>, because there is almost always one.",
             "<b>A written answer to 'was reinforcement learning the "
             "right tool here?'</b> — which is the graded part, and "
             "'no' is an acceptable answer with evidence.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "From Planning to Learning",
 "subtitle": "Two substitutions, and everything that follows.",
 "question": "What exactly changes when you do not know the model?",
 "outcomes": [
     "State the two differences from CSCE 625's MDP.",
     "Explain sample inefficiency and where it comes from.",
     "Distinguish model-free from model-based approaches.",
     "Classify reinforcement learning settings by what access you "
     "have.",
     "Decide whether a problem calls for learning at all.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The two substitutions",
   "blurb": "The same equation, two things removed."},

  {"t": "callout", "title": "Reinforcement learning is CSCE 625's MDP with two things taken away",
   "kind": "The framing for the whole course",
   "body": ["<b>The Bellman equation is unchanged.</b> "
            "V*(s) = maxₐ Σ P(s′|s,a)[R + "
            "γV*(s′)] is still the thing you are solving.",
            "<b>Substitution one: you do not know P or R.</b> So you "
            "cannot sum over s′ — you must <i>sample</i> it by "
            "acting and observing.",
            "<b>Substitution two: the state space is too large to "
            "tabulate.</b> So V or Q becomes a function approximator "
            "— a network (CSCE 636).",
            "<b>Every difficulty in this course traces to one of "
            "those.</b> <b>Sampling causes inefficiency and makes "
            "exploration a problem; approximation causes instability and "
            "removes the guarantees.</b> <b>Keep the attribution clear "
            "and the field becomes comprehensible.</b>"]},

  {"t": "table", "kicker": "Consequences", "title": "What each substitution costs",
   "header": ["", "No model (sampling)", "No table (approximation)"],
   "widths": [2.4, 4.4, 5.2],
   "rows": [
     ["<b>Causes</b>", "<b>Sample inefficiency; exploration is required</b>", "<b>Instability; generalisation across states</b>"],
     ["<b>Modules</b>", "<b>02, 03, 08</b>", "<b>04, 05, 06, 07</b>"],
     ["<b>Guarantees</b>", "<b>Convergence with enough visits</b>", "<b>None, in general</b>"],
     ["<b>Fix</b>", "<b>Better exploration; learn a model</b>", "<b>Replay, target networks, trust regions</b>"],
     ["<b>Residual problem</b>", "<b>Millions of steps</b>", "<b>Seed variance (M12)</b>"],
   ],
   "footnote": "<b>Note the second column has no guarantees row worth "
               "stating.</b> <b>Tabular reinforcement learning converges; "
               "deep reinforcement learning is an empirical discipline</b>, "
               "and the course says so throughout.",
   "note": "This table is the map of the whole course."},

  {"t": "section", "label": "Part 2", "title": "Sample inefficiency",
   "blurb": "The number that shapes everything."},

  {"t": "callout", "title": "The sample counts are the first thing to internalise",
   "kind": "Why this matters more than it sounds",
   "body": ["<b>Atari at human level: tens of millions of frames.</b> "
            "<b>A human reaches the same level in a couple of hours "
            "— roughly 100,000 frames.</b>",
            "<b>Continuous control: millions of steps for a task a "
            "scripted controller does immediately.</b>",
            "<b>So reinforcement learning is viable where samples are "
            "cheap</b> — a simulator — <b>and very difficult where "
            "they are not</b>, which is most of the physical world.",
            "<b>That single fact determines the field's shape:</b> "
            "<b>the successes are in games and simulation, and the "
            "robotics work is mostly about transferring from simulation "
            "or about learning a model</b> (Module 08)."]},

  {"t": "section", "label": "Part 3", "title": "The settings",
   "blurb": "What access you have decides the method."},

  {"t": "table", "kicker": "Settings", "title": "Classify your access first",
   "header": ["You have", "Setting", "Approach"],
   "widths": [3.4, 3.2, 4.4],
   "rows": [
     ["<b>The model</b>", "<b>Planning</b>", "<b>CSCE 625 M10. Not this course</b>"],
     ["<b>A fast simulator</b>", "<b>On-policy RL</b>", "<b>PPO. Modules 05–06</b>"],
     ["<b>Expensive interaction</b>", "<b>Off-policy RL</b>", "<b>SAC, or model-based (M07, M08)</b>"],
     ["<b>A fixed logged dataset</b>", "<b>Offline RL</b>", "<b>CQL, IQL. Module 09</b>"],
     ["<b>Expert demonstrations</b>", "<b>Imitation</b>", "<b>Behaviour cloning, DAgger. M09</b>"],
     ["<b>A reward you cannot write</b>", "<b>Preference learning</b>", "<b>RLHF. Module 10</b>"],
   ],
   "footnote": "<b>The first row is the one people skip.</b> <b>If you "
               "have or can build a model, computing is better than "
               "learning</b> — faster, guaranteed, and debuggable.",
   "note": "Putting the planning row first sets the honest tone."},

  {"t": "callout", "title": "Model-free and model-based, and why both exist",
   "kind": "The central architectural split",
   "body": ["<b>Model-free: learn a value function or a policy "
            "directly from experience</b>, with no explicit model of "
            "the dynamics. Simpler, and it is Modules 03–07.",
            "<b>Model-based: learn P and R, then plan with them</b> "
            "(CSCE 625 M10) <b>or use them to generate synthetic "
            "experience.</b> Module 08.",
            "<b>Model-based is far more sample-efficient</b>, because a "
            "learned model can be queried millions of times for the cost "
            "of one real step.",
            "<b>And it is harder, because model errors compound over a "
            "rollout</b> — <b>a policy optimised against a flawed "
            "model exploits the flaw</b>, which is CSCE 669 Module 12's "
            "warning in its sharpest form."]},

  {"t": "section", "label": "Part 4", "title": "Should you",
   "blurb": "The question to answer before Module 02."},

  {"t": "bullets", "kicker": "Decision", "title": "When reinforcement learning is the right tool",
   "items": [
     "<b>Yes:</b> sequential decisions, delayed consequences, a "
     "simulator, no good hand-written policy, and a reward you can "
     "actually specify.",
     "",
     "<b>No, if a scripted policy works.</b> <b>It will be faster, "
     "debuggable, and tunable</b> (CSCE 625 M01 §4).",
     "",
     "<b>No, if you have the model.</b> Plan instead. <b>Computing "
     "beats learning when you can compute.</b>",
     "",
     "<b>No, if decisions are independent.</b> <b>That is supervised "
     "learning</b>, which is far easier and better understood "
     "(CSCE 633).",
     "",
     "<b>And no, if you cannot specify the reward.</b> <b>Module 10 "
     "is about how badly that goes</b>, and it goes badly.",
   ],
   "footnote": "<b>'No' is a respectable answer and the project "
               "accepts it with evidence.</b> <b>Knowing when not to use "
               "a method is part of knowing it.</b>"},
 ],
 "takeaways": [
   "Reinforcement learning is CSCE 625's MDP with the model unknown and "
   "the table replaced by an approximator — and the Bellman equation "
   "is unchanged.",
   "Not knowing the model causes sample inefficiency and makes exploration "
   "necessary; approximation causes instability and removes the "
   "guarantees.",
   "Tabular reinforcement learning converges; deep reinforcement learning "
   "is an empirical discipline.",
   "Atari at human level takes tens of millions of frames against a "
   "human's hundred thousand, which determines the field's shape.",
   "Classify your access first — and if you have or can build a "
   "model, computing beats learning.",
   "Model-based methods are far more sample-efficient and harder, because "
   "a policy optimised against a flawed model exploits the flaw.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The two substitutions"),
  ("callout", "Reinforcement learning is CSCE 625's MDP with two things "
              "taken away",
   ["<b>The Bellman equation is unchanged.</b> V*(s) = "
    "max<sub>a</sub> &Sigma;<sub>s&prime;</sub> P(s&prime;|s,a)[R + "
    "&gamma;V*(s&prime;)] is still exactly the thing being solved, and "
    "<b>recognising that is the most useful single fact for navigating "
    "this course.</b>",
    "<b>Substitution one: you do not know P or R.</b> So <b>you cannot "
    "evaluate the sum over s&prime;</b> — you must estimate it by "
    "acting in the world and observing what happens, which means every "
    "update is based on samples rather than on the distribution.",
    "<b>Substitution two: the state space is far too large to "
    "tabulate.</b> So V or Q becomes a <i>function approximator</i> "
    "— in practice a neural network (CSCE 636) — which "
    "generalises across states it has never visited and, in doing so, "
    "introduces errors that feed back into its own targets.",
    "<b>Every difficulty in this course traces to one of those two "
    "substitutions.</b> <b>Sampling causes inefficiency and makes "
    "exploration an open problem; approximation causes instability and "
    "removes the convergence guarantees.</b> <b>Keeping the attribution "
    "clear is what makes the field comprehensible rather than a list of "
    "algorithms</b> — when a method is introduced, ask which "
    "substitution's damage it is repairing."]),
  ("table", ["", "No model (sampling)", "No table (approximation)"],
   [["<b>What it causes</b>",
     "<b>Sample inefficiency, and exploration becomes a problem that must "
     "be solved rather than assumed.</b>",
     "<b>Instability, and generalisation across states — which is "
     "both the benefit and the hazard.</b>"],
    ["<b>Modules addressing it</b>", "<b>02, 03, 08</b>",
     "<b>04, 05, 06, 07</b>"],
    ["<b>Guarantees</b>",
     "<b>Tabular methods converge given enough visits to every "
     "state-action pair</b> — a real theorem.",
     "<b>None, in general.</b> See the note below."],
    ["<b>The standard fixes</b>",
     "<b>Better exploration (Module 02); learn a model to reuse "
     "experience (Module 08).</b>",
     "<b>Experience replay, target networks, trust regions, and "
     "clipping</b> (Modules 04, 06)."],
    ["<b>What remains unfixed</b>",
     "<b>Millions of environment steps for tasks humans learn in "
     "minutes.</b>",
     "<b>Seed variance large enough to swamp method differences</b> "
     "(Module 12)."]],
   [0.17, 0.41, 0.42]),
  ("p", "<b>Note that the second column has no guarantees row worth "
        "stating.</b> <b>Tabular reinforcement learning converges and "
        "deep reinforcement learning is an empirical discipline</b>, and "
        "this course says so throughout rather than once. <b>It is not a "
        "criticism</b> — CSCE 636's deep networks have no "
        "guarantees either and are extremely useful — <b>but it does "
        "change what a result means and how it should be reported</b>, "
        "which is Module 12's subject."),

  ("h1", "2 &nbsp; Sample inefficiency"),
  ("callout", "The sample counts are the first thing to internalise",
   ["<b>Atari at human level: tens of millions of frames</b> for the "
    "original deep Q-network, and still millions for modern "
    "sample-efficient methods. <b>A human reaches comparable performance "
    "in a couple of hours — roughly a hundred thousand frames</b>, "
    "and brings priors about objects, gravity, and intent that the agent "
    "does not have.",
    "<b>Continuous control: millions of steps for tasks a hand-written "
    "controller performs immediately</b> — and the hand-written "
    "controller is frequently better, which Module 13 reports honestly.",
    "<b>So reinforcement learning is viable where samples are cheap</b> "
    "— a fast simulator, a game, a recommender with enormous traffic "
    "— <b>and very difficult where they are not</b>, which includes "
    "most of the physical world, most medical settings, and anything where "
    "a bad action has a real cost.",
    "<b>That single fact determines the field's shape.</b> <b>The "
    "well-known successes are in games and simulation; the robotics work "
    "is largely about transferring from simulation (domain randomisation) "
    "or about learning a model to reduce the real-sample requirement</b> "
    "(Module 08). <b>Reading the literature with the sample count in "
    "mind explains most of what the field chooses to work on.</b>"]),

  ("h1", "3 &nbsp; The settings"),
  ("table", ["What you have access to", "The setting", "The approach"],
   [["<b>The transition model and reward function</b>",
     "<b>Planning.</b>",
     "<b>CSCE 625 Module 10's value or policy iteration. Not this "
     "course.</b>"],
    ["<b>A fast simulator you can reset and query freely</b>",
     "<b>On-policy reinforcement learning.</b>",
     "<b>PPO is the default</b> (Modules 05–06)."],
    ["<b>Interaction that is slow or costly</b>",
     "<b>Off-policy reinforcement learning.</b>",
     "<b>SAC or TD3 for sample efficiency</b> (Module 07), <b>or "
     "model-based</b> (Module 08)."],
    ["<b>A fixed dataset of logged interactions and no further "
     "access</b>", "<b>Offline reinforcement learning.</b>",
     "<b>Conservative methods — CQL, IQL</b> (Module 09), <b>and "
     "naive off-policy learning fails here for a specific reason.</b>"],
    ["<b>Expert demonstrations</b>", "<b>Imitation learning.</b>",
     "<b>Behaviour cloning, DAgger, inverse reinforcement learning</b> "
     "(Module 09)."],
    ["<b>A notion of good behaviour you cannot write as a reward</b>",
     "<b>Preference-based learning.</b>",
     "<b>Learn a reward model from comparisons — RLHF</b> "
     "(Module 10)."]],
   [0.31, 0.25, 0.44]),
  ("p", "<b>The first row is the one people skip.</b> <b>If you have a "
        "model, or can build an approximate one, computing is better than "
        "learning</b> — it is faster, it has guarantees, it is "
        "debuggable, and it needs no samples at all. <b>And building an "
        "approximate model is frequently easier than people assume</b>, "
        "especially for engineered systems where the dynamics are "
        "documented. <b>Starting this course by naming the setting in "
        "which it does not apply is deliberate.</b>"),
  ("callout", "Model-free and model-based, and why both exist",
   ["<b>Model-free: learn a value function or a policy directly from "
    "experience</b>, with no explicit representation of the dynamics at "
    "all. Conceptually simpler, far more widely used, and the subject of "
    "Modules 03 through 07.",
    "<b>Model-based: learn P and R from experience, then either plan with "
    "them</b> (CSCE 625 Module 10, or Module 05's tree search in that "
    "course) <b>or use them to generate synthetic experience to train a "
    "model-free learner on.</b> Module 08.",
    "<b>Model-based is dramatically more sample-efficient</b>, because "
    "<b>a learned model can be queried millions of times for the cost of "
    "one real environment step</b> — and sample efficiency is "
    "&sect;2's binding constraint, so this is not a minor advantage.",
    "<b>And it is harder, because model errors compound over a "
    "rollout.</b> <b>A policy optimised against a flawed model exploits "
    "the flaw</b> — it finds the state where the model is most wrong "
    "and goes there, because that is where the model promises the most "
    "reward. <b>This is CSCE 669 Module 12 &sect;4's warning in its "
    "sharpest available form</b>, and it is why model-based reinforcement "
    "learning took so long to work: the obvious approach fails for a "
    "reason that is structural rather than incidental."]),

  ("break",),
  ("h1", "4 &nbsp; Should you use reinforcement learning at all"),
  ("ul", ["<b>Yes, when:</b> decisions are sequential, consequences are "
          "delayed, you have a simulator or cheap interaction, no good "
          "hand-written policy exists, <b>and you can actually specify a "
          "reward</b>. <b>All five, not three of five.</b>",
          "<b>No, if a scripted or searched policy works.</b> <b>It will "
          "be faster at runtime, debuggable, and tunable by a "
          "designer</b> — CSCE 625 Module 01 &sect;4's four "
          "properties, all of which matter more in production than the "
          "last few percent of performance.",
          "<b>No, if you have the model.</b> <b>Plan instead.</b> "
          "<b>Computing beats learning whenever you can compute</b>, and "
          "&sect;3's first row is there for this reason.",
          "<b>No, if the decisions are independent of each other.</b> "
          "<b>That is supervised learning</b>, which is far easier, far "
          "better understood, and has actual generalisation theory "
          "(CSCE 633). <b>A great deal of work framed as reinforcement "
          "learning is a contextual bandit at most</b>, and a bandit is "
          "much easier than a full MDP (Module 02 &sect;1).",
          "<b>And no, if you cannot specify the reward.</b> "
          "<b>Module 10 is about how badly that goes, and it goes "
          "badly</b> — an agent given an imperfect reward will find "
          "the imperfection, reliably and creatively.",
          "<b>'No' is a respectable answer, and this course's second "
          "project accepts it with evidence.</b> <b>Knowing when not to "
          "use a method is part of knowing the method</b>, and it is the "
          "part the literature is least helpful about."]),
 ],
 "resources": [
   ("Sutton & Barto &mdash; Reinforcement Learning, chapter 1 (free "
    "PDF)",
    "http://incompleteideas.net/book/the-book.html",
    "<b>The field's own framing</b>, and chapters 3–4 are the "
    "CSCE 625 Module 10 material this course builds on."),
   ("OpenAI Spinning Up &mdash; Introduction and Key Concepts (free)",
    "https://spinningup.openai.com/en/latest/spinningup/rl_intro.html",
    "<b>The clearest statement of &sect;1's framing available</b>, with "
    "the taxonomy of &sect;3's table."),
   ("Berkeley CS285 &mdash; lecture 1 and the course overview (free)",
    "https://rail.eecs.berkeley.edu/deeprlcourse/",
    "<b>The graduate framing</b>, including an honest treatment of "
    "&sect;2's sample-efficiency problem."),
   ("Tsividis et al. &mdash; Human Learning in Atari (free)",
    "https://arxiv.org/abs/1707.08602",
    "<b>The human comparison of &sect;2, measured</b> — and the "
    "analysis of which priors humans bring."),
 ],
 "exercises": [
   "<b>Write the Bellman equation</b> and mark which terms you do not "
   "have access to in the reinforcement learning setting.",
   "<b>Solve a small MDP by value iteration</b> (CSCE 625 M10), then "
   "<b>solve the same MDP by Q-learning</b> and report the sample count "
   "needed to match.",
   "<b>Report the ratio</b>, and explain which substitution it "
   "measures.",
   "<b>Classify three problems you care about</b> against &sect;3's "
   "table.",
   "<b>For each, answer &sect;4's five questions</b> and record whether "
   "reinforcement learning is appropriate.",
   "<b>Find a published reinforcement learning result</b> and locate its "
   "total environment step count. Report it.",
   "<b>Estimate how long that would take</b> at one step per second of "
   "real-world interaction.",
   "<b>Build a scripted baseline</b> for one of your tasks and record its "
   "performance before training anything.",
   "<b>Set up seed control and logging</b> for the five quantities in the "
   "tooling list, before Module 02.",
   "<b>Write down, now, what you expect reinforcement learning to be good "
   "at.</b> Keep it and revisit after Module 13.",
 ],
 "selfcheck": [
   "What two things does reinforcement learning remove from CSCE 625's "
   "MDP?",
   "What does each removal cause, and which modules address each?",
   "Which has convergence guarantees and which does not?",
   "Give the Atari sample counts for an agent and for a human.",
   "How does sample efficiency determine the field's shape?",
   "Name six settings and the approach for each.",
   "Why is the planning row first?",
   "Compare model-free and model-based, including the failure mode.",
   "Give five conditions for reinforcement learning being appropriate.",
 ],
},

]

for _b in ("c642_b2", "c642_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
