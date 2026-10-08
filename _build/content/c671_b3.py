# -*- coding: utf-8 -*-
"""CSCE 671 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Controlled Experiments with People",
 "subtitle": "Measuring a difference, which needs a design.",
 "question": "Is design A actually better than design B?",
 "outcomes": [
     "Choose between within-subject and between-subject "
     "designs.",
     "Explain counterbalancing and why it is necessary.",
     "Explain the statistics for small human samples.",
     "Explain the specific threats to validity here.",
     "Design and analyse an experiment with people.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two designs",
   "blurb": "And the choice determines nearly everything else."},

  {"t": "table", "kicker": "Designs", "title": "Within-subject and between-subject",
   "header": ["", "Within-subject", "Between-subject"],
   "widths": [2.5, 4.1, 4.8],
   "rows": [
     ["<b>Each person</b>", "<b>Uses both designs</b>", "<b>Uses one design</b>"],
     ["<b>Controls for</b>", "<b>Individual differences — completely</b>", "<b>Nothing; relies on randomisation</b>"],
     ["<b>Needs</b>", "<b>Far fewer participants</b>", "<b>Many more</b>"],
     ["<b>Problem</b>", "<b>Order and learning effects</b>", "<b>Variance between people swamps the effect</b>"],
     ["<b>Use when</b>", "<b>The task can be repeated</b>", "<b>Exposure to one changes the other</b>"],
   ],
   "footnote": "<b>Individual variation between people is usually "
               "larger than the difference between two designs</b> "
               "— which is why within-subject is strongly preferred "
               "when it is available at all.",
   "note": "The variance argument is the reason, and it is worth "
           "stating numerically."},

  {"t": "callout", "title": "Individual differences are larger than design differences, which is the governing fact",
   "kind": "Why the design choice matters so much",
   "body": ["<b>The fastest and slowest participant on the same task "
            "with the same interface frequently differ by a factor of "
            "several</b> — and <b>the difference between two "
            "reasonable designs is usually much smaller than "
            "that.</b>",
            "<b>So a between-subject design has to detect a small "
            "effect against a large variance</b>, which requires many "
            "participants — frequently more than you can "
            "recruit.",
            "<b>While a within-subject design removes that variance "
            "entirely</b>, because each person is compared against "
            "themselves — <b>which is why it can work with a dozen "
            "people where between-subject needs a hundred.</b>",
            "<b>And it introduces order effects instead</b>, which "
            "are <b>manageable by counterbalancing</b> "
            "(Part 2) — a far better trade than needing "
            "ten times the participants."]},

  {"t": "section", "label": "Part 2", "title": "Counterbalancing",
   "blurb": "The necessary fix for order effects."},

  {"t": "code", "kicker": "Order effects", "title": "What they are, and the fix",
   "lang": "text", "code": """
  THE PROBLEM
      learning      the second design benefits from
                    the practice gained on the first
      fatigue       the second design suffers from
                    tiredness and boredom
      carryover     the first design's mental model
                    is applied to the second

  SO A -> B ORDER CONFOUNDS THE DESIGN WITH THE ORDER.

  THE FIX: COUNTERBALANCING
      half the participants see A then B, half see B
      then A. The order effect then applies equally
      to both conditions and cancels in the
      comparison.

  AND WITH MORE THAN TWO CONDITIONS
      a Latin square, so each condition appears in
      each position equally often.

  AND CARRYOVER IS THE ONE COUNTERBALANCING DOES NOT
  FIX -- if using A permanently changes how somebody
  thinks about B, go between-subject instead.
""",
   "caption": "<b>Carryover is the one counterbalancing does not "
              "fix</b> — and it is the condition that forces a "
              "between-subject design.",
   "note": "Distinguishing carryover from learning determines the "
           "design choice."},

  {"t": "section", "label": "Part 3", "title": "Statistics",
   "blurb": "For samples far smaller than the methods assume."},

  {"t": "bullets", "kicker": "Statistics", "title": "What applies at these sample sizes",
   "items": [
     "<b>Use a paired test for within-subject data</b>, which is "
     "where the design's power comes from — an unpaired test on "
     "paired data throws the advantage away.",
     "",
     "<b>Check the distribution, do not assume it.</b> <b>Task "
     "times are right-skewed, not normal</b> — so use a "
     "non-parametric test, or log-transform and say "
     "so.",
     "",
     "<b>Report the effect size and its confidence "
     "interval</b>, not only the p-value — which is "
     "CSCE 676 §11 §3's argument at the "
     "other extreme of n.",
     "",
     "<b>And count your comparisons.</b> <b>Three metrics times "
     "four tasks is twelve tests</b>, which needs a correction "
     "(CSCE 676 §11 §2).",
     "",
     "<b>While accepting that with twelve people you are "
     "estimating badly</b> — which is a limitation to state "
     "rather than to hide.",
   ],
   "footnote": "<b>The multiplicity problem is as real here as in "
               "CSCE 676 and is almost never corrected for</b> — a "
               "usability study reporting twelve tests at p &lt; 0.05 has "
               "found what you would expect by chance."},

  {"t": "section", "label": "Part 4", "title": "Validity and ethics",
   "blurb": "The threats specific to studies with people."},

  {"t": "bullets", "kicker": "Threats", "title": "The threats that matter here",
   "items": [
     "<b>Demand characteristics.</b> <b>Participants work out "
     "what you want and provide it</b> — so keep the hypothesis "
     "from them, and avoid signalling which design is "
     "yours.",
     "",
     "<b>The novelty effect.</b> <b>A new design performs well "
     "because it is new</b>, and the advantage disappears — which "
     "a single session cannot detect.",
     "",
     "<b>Sampling.</b> <b>Your participants are probably people "
     "like you</b>, and the population you are designing for is "
     "not (CSCE 632).",
     "",
     "<b>And the practice effect across the whole "
     "session</b>, which counterbalancing handles and which a "
     "single-condition study does not.",
     "",
     "<b>So state your sample's composition</b>, which is the "
     "limitation most often omitted.",
   ],
   "footnote": "<b>Your participants being people like you is the "
               "threat that is hardest to see</b> — convenience "
               "sampling in a university produces a very "
               "specific population."},

  {"t": "callout", "title": "And a study with people has obligations a study with data does not",
   "kind": "The ethics, briefly and non-negotiably",
   "body": ["<b>Informed consent:</b> <b>what you will do, what you "
            "will record, how it will be stored, and that they may stop "
            "at any time without giving a reason.</b>",
            "<b>Debrief any deception</b>, including a Wizard of Oz "
            "setup (Module 06 §3) — which is a requirement "
            "and not a courtesy.",
            "<b>Minimise and protect the data.</b> <b>A recording of "
            "somebody failing at a task is sensitive</b>, and "
            "CSCE 701's and CSCE 676 §12's handling obligations "
            "apply in full.",
            "<b>And never make the participant feel tested.</b> "
            "<b>It is both unkind and methodologically "
            "damaging</b> (Module 07 §1), which means the "
            "ethical and the practical point coincide here."]},
 ],
 "takeaways": [
   "Individual variation between people is usually larger than the "
   "difference between two designs, which is why within-subject is "
   "preferred.",
   "A within-subject design can work with a dozen people where "
   "between-subject needs a hundred.",
   "Counterbalancing cancels learning and fatigue effects and does not fix "
   "carryover, which is what forces a between-subject design.",
   "Task times are right-skewed rather than normal, so check the "
   "distribution rather than assuming it.",
   "Three metrics times four tasks is twelve tests, and a usability study "
   "reporting twelve at p < 0.05 has found what chance predicts.",
   "Your participants being people like you is the threat hardest to see, "
   "and the sample's composition is the limitation most often omitted.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two designs"),
  ("table", ["", "Within-subject", "Between-subject"],
   [["<b>Each person</b>", "<b>Uses both designs.</b>",
     "<b>Uses only one design.</b>"],
    ["<b>Controls for</b>",
     "<b>Individual differences — completely, since each person is "
     "their own control.</b>",
     "<b>Nothing directly; it relies on randomisation to balance the "
     "groups.</b>"],
    ["<b>Participants needed</b>", "<b>Far fewer.</b>",
     "<b>Many more</b> — see the callout for why."],
    ["<b>The problem</b>", "<b>Order and learning effects</b> "
     "(&sect;2).",
     "<b>Variance between people swamps the effect you are looking "
     "for.</b>"],
    ["<b>Use when</b>",
     "<b>The task can reasonably be repeated.</b>",
     "<b>Exposure to one design permanently changes how the other is "
     "approached</b> (&sect;2's carryover)."]],
   [0.19, 0.38, 0.43]),
  ("callout", "Individual differences are larger than design differences, "
              "which is the governing fact",
   ["<b>The fastest and the slowest participant on the same task with "
    "the same interface frequently differ by a factor of several</b> "
    "— and <b>the difference between two reasonable designs is "
    "usually very much smaller than that.</b>",
    "<b>So a between-subject design has to detect a small effect "
    "against a large variance</b>, <b>which requires many "
    "participants</b> — frequently more than you can realistically "
    "recruit, which means the study is underpowered and will find "
    "nothing whichever design is better.",
    "<b>While a within-subject design removes that variance "
    "entirely</b>, because each person is compared against "
    "themselves — <b>which is why it can work with a dozen people "
    "where a between-subject design would need a hundred.</b>",
    "<b>And it introduces order effects instead</b>, which are "
    "<b>manageable by counterbalancing</b> (&sect;2) — <b>a far "
    "better trade than needing ten times the participants</b>, and is "
    "why within-subject should be the default whenever the task can be "
    "repeated."]),

  ("h1", "2 &nbsp; Counterbalancing"),
  ("code", """THE PROBLEM
    learning      the second design benefits from the
                  practice gained on the first
    fatigue       the second design suffers from
                  tiredness and boredom
    carryover     the first design's mental model is
                  applied to the second

SO A -> B ORDER CONFOUNDS THE DESIGN WITH THE ORDER.

THE FIX: COUNTERBALANCING
    half the participants see A then B, and half see
    B then A. The order effect then applies equally
    to both conditions and cancels out in the
    comparison.

AND WITH MORE THAN TWO CONDITIONS
    a Latin square, so that each condition appears in
    each position equally often.

AND CARRYOVER IS THE ONE COUNTERBALANCING DOES NOT
FIX -- if using A permanently changes how somebody
thinks about B, go between-subject instead."""),
  ("p", "<b>Carryover is the one counterbalancing does not fix</b>, and "
        "<b>it is the condition that forces a between-subject design</b> "
        "— so <b>distinguishing carryover from learning determines "
        "the design choice</b> and is worth thinking about before "
        "recruiting. Learning is symmetric and cancels; carryover is a "
        "permanent change to the participant and does not. A new "
        "conceptual model (Module 04) is the usual source of "
        "carryover: once somebody understands design A's model, they "
        "cannot approach B naively."),

  ("break",),
  ("h1", "3 &nbsp; Statistics at these sample sizes"),
  ("ul", ["<b>Use a paired test for within-subject data</b>, "
          "<b>which is where the design's statistical power actually "
          "comes from</b> — and <b>an unpaired test applied to "
          "paired data throws the entire advantage away</b>, which is a "
          "common and costly mistake.",
          "<b>Check the distribution rather than assuming it.</b> "
          "<b>Task completion times are right-skewed rather than "
          "normal</b> — a few very slow trials pull the tail — so "
          "<b>use a non-parametric test, or log-transform the times and "
          "say that you did.</b>",
          "<b>Report the effect size and its confidence interval, not "
          "only the p-value</b> — which is <b>CSCE 676 "
          "Module 11 &sect;3's argument arriving at the opposite "
          "extreme of n</b>: there, large n made everything significant; "
          "here, small n makes a real effect non-significant, and the "
          "effect size is informative either way.",
          "<b>And count your comparisons.</b> <b>Three metrics across "
          "four tasks is twelve statistical tests</b>, <b>which needs a "
          "correction</b> (CSCE 676 Module 11 &sect;2) and almost "
          "never receives one.",
          "<b>While accepting that with twelve participants you are "
          "estimating the effect badly</b> — the interval will be "
          "wide — <b>which is a limitation to state rather than to "
          "hide</b> (Module 13 &sect;2). <b>The multiplicity problem "
          "is as real here as in CSCE 676 and is almost never corrected "
          "for</b>: a usability study reporting twelve tests with one at "
          "p &lt; 0.05 has found exactly what you would expect by "
          "chance."]),

  ("h1", "4 &nbsp; Validity and ethics"),
  ("ul", ["<b>Demand characteristics.</b> <b>Participants work out "
          "what you are hoping for and helpfully provide it</b> — so "
          "<b>keep the hypothesis from them, and avoid signalling which "
          "of the two designs is yours</b>, which they will otherwise "
          "infer from your manner.",
          "<b>The novelty effect.</b> <b>A new design performs well "
          "partly because it is new and interesting</b>, and <b>the "
          "advantage disappears after a few weeks</b> — <b>which a "
          "single session cannot detect at all</b> (Module 06 "
          "&sect;4's long-term limit).",
          "<b>Sampling.</b> <b>Your participants are probably people "
          "quite like you</b> — colleagues, students, friends — "
          "<b>and the population you are designing for is not</b> "
          "(CSCE 632's whole argument).",
          "<b>And the practice effect across the session as a "
          "whole</b>, which counterbalancing handles within a study and "
          "which <b>a single-condition study does not</b>, making "
          "before/after comparisons across a session unreliable.",
          "<b>So state your sample's composition</b> — how many, "
          "recruited how, with what relevant experience — <b>which "
          "is the limitation most often omitted</b> and the easiest to "
          "supply. <b>Your participants being people like you is the "
          "threat that is hardest to see</b>, because <b>convenience "
          "sampling in a university produces a very specific "
          "population</b> that resembles nobody's user base."]),
  ("callout", "And a study with people has obligations a study with data "
              "does not",
   ["<b>Informed consent:</b> <b>what you will do, what you will "
    "record, how it will be stored and for how long, who will see it, and "
    "that they may stop at any point without giving a reason and without "
    "consequence.</b>",
    "<b>Debrief any deception</b>, including a Wizard of Oz setup "
    "(Module 06 &sect;3) — <b>which is a requirement and not a "
    "courtesy</b>, and which should be scripted in advance rather than "
    "improvised at the end of a long session.",
    "<b>Minimise and protect the data.</b> <b>A recording of "
    "somebody failing repeatedly at a task is sensitive material</b>, and "
    "<b>CSCE 701's handling obligations and CSCE 676 "
    "Module 12's privacy reasoning apply to it in full</b> — "
    "including the collect-less principle.",
    "<b>And never make the participant feel tested.</b> <b>It is both "
    "unkind and methodologically damaging</b> (Module 07 "
    "&sect;1) — <b>which means the ethical point and the practical "
    "point coincide here</b>, and that is a convenient and unusual "
    "alignment worth noticing."]),
 ],
 "resources": [
   ("Lazar, Feng & Hochheiser &mdash; Research Methods in HCI, "
    "chapters 2 through 5",
    "https://www.elsevier.com/books/research-methods-in-human-computer-interaction/lazar/978-0-12-805390-4",
    "<b>The whole module</b> — the designs, the statistics, and the "
    "ethics, treated properly. Library copy."),
   ("Cairns &mdash; Doing Better Statistics in Human-Computer "
    "Interaction",
    "https://www.cambridge.org/core/books/doing-better-statistics-in-humancomputer-interaction/",
    "<b>&sect;3 specifically</b> — and honest about how badly the "
    "field has historically done this. Library copy."),
   ("Dragicevic &mdash; Fair Statistical Communication in HCI (free)",
    "https://hal.science/hal-01377894",
    "<b>&sect;3's reporting recommendations</b> — effect sizes and "
    "intervals instead of significance, argued for this field."),
   ("The Belmont Report, and your institution's ethics guidance "
    "(free)",
    "https://www.hhs.gov/ohrp/regulatory-overview/index.html",
    "<b>&sect;4's obligations in their original framing</b> — and "
    "whatever local process applies to you."),
 ],
 "exercises": [
   "<b>Measure the spread of task times</b> across ten people on one "
   "interface.",
   "<b>Compare that spread</b> to the difference you expect between two "
   "designs.",
   "<b>Compute the sample size</b> a between-subject study would need "
   "for that effect.",
   "<b>Design a counterbalanced within-subject study</b> for two "
   "designs.",
   "<b>Identify whether your task has carryover</b>, and justify the "
   "design choice.",
   "<b>Plot your task times</b> and check whether they are normal.",
   "<b>Run a paired and an unpaired test</b> on the same data and "
   "compare the p-values.",
   "<b>Count the comparisons</b> in a usability study you have read, and "
   "check whether it corrected.",
   "<b>Describe your own likely sample</b> and how it differs from your "
   "users.",
   "<b>Write a consent script</b> and a debrief script.",
 ],
 "selfcheck": [
   "Contrast the two designs on five dimensions.",
   "Why are individual differences the governing fact?",
   "Why can within-subject work with a dozen people?",
   "Name the three order effects and what counterbalancing fixes.",
   "Which one does it not fix, and what follows?",
   "Give four statistical rules for small human samples.",
   "Why does an unpaired test on paired data waste the design?",
   "Name four threats to validity, and which is hardest to see.",
   "Give the four ethical obligations.",
   "Where do the ethical and practical points coincide?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Qualitative Methods",
 "subtitle": "Finding out what you did not know to ask.",
 "question": "What is actually going on, and why?",
 "outcomes": [
     "Explain what qualitative methods establish.",
     "Conduct an interview that produces usable data.",
     "Explain contextual inquiry and observation.",
     "Explain why what people say differs from what they "
     "do.",
     "Analyse qualitative data systematically.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What they are for",
   "blurb": "Discovery, not measurement."},

  {"t": "callout", "title": "Qualitative methods generate hypotheses and explain mechanisms; they do not measure rates",
   "kind": "The division of labour",
   "body": ["<b>An experiment can tell you that design A is faster; "
            "it cannot tell you why, or what else people were trying to "
            "do</b> — which is what qualitative work is "
            "for.",
            "<b>And it cannot tell you about the question you did not "
            "ask</b> — <b>which is the single largest risk in any "
            "study</b>, and the reason to look before you "
            "measure.",
            "<b>So the sequence is: observe to find out what matters, "
            "then measure the thing that mattered</b> — and "
            "<b>measuring first means measuring whatever you happened to "
            "think of.</b>",
            "<b>Which makes them complementary rather than "
            "competing:</b> <b>'eight of twelve people' from a "
            "qualitative study is not a rate and is a reason to go and "
            "measure one.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Interviews",
   "blurb": "Which are easy to run and easy to ruin."},

  {"t": "code", "kicker": "Interviews", "title": "The questions that work, and the ones that do not",
   "lang": "text", "code": """
  ASK ABOUT THE PAST AND THE CONCRETE
      "Tell me about the last time you did this."
      "Walk me through what you did yesterday."
      "Show me."

  DO NOT ASK ABOUT THE FUTURE OR THE HYPOTHETICAL
      "Would you use a feature that..."
      "How often do you think you would..."
      -- people are poor at predicting their own
      behaviour, and worse at predicting it to
      somebody who clearly wants a yes.

  AND DO NOT ASK FOR SOLUTIONS
      "What would you want here?" produces a feature
      request. "What were you trying to do?"
      produces a problem, which is what you can
      design against.

  THE RULE: ask for behaviour, not for opinion or
  prediction. And then ask "why" until it stops being
  informative.
""",
   "caption": "<b>Ask for behaviour, not for opinion or "
              "prediction</b> — which is the single rule that makes "
              "an interview worth running.",
   "note": "The past-and-concrete rule is the whole technique."},

  {"t": "callout", "title": "And a leading question gets the answer you led toward",
   "kind": "The commonest way an interview is wasted",
   "body": ["<b>'Was that confusing?' gets a yes; 'what were you "
            "thinking there?' gets a description</b> — and only the "
            "second is data.",
            "<b>And the participant wants to be helpful</b>, which "
            "means <b>they will agree with whatever you appear to "
            "believe</b> rather than contradict you "
            "(Module 08 §4's demand "
            "characteristics).",
            "<b>So keep your own hypothesis out of the room</b>, "
            "and <b>be willing to sit through silence</b>, which is "
            "where the unprompted material arrives.",
            "<b>Which is the same discipline as "
            "Module 07 §1's</b> — <b>the interviewer's job is "
            "to be uninteresting</b>, and it is equally difficult in both "
            "settings."]},

  {"t": "section", "label": "Part 3", "title": "Observation",
   "blurb": "Because what people say is not what they do."},

  {"t": "callout", "title": "People cannot accurately report their own behaviour, which is not dishonesty",
   "kind": "The finding that makes observation necessary",
   "body": ["<b>Self-reported frequencies are unreliable</b>, "
            "<b>workarounds are forgotten because they have become "
            "automatic</b>, and <b>the steps of a familiar task cannot "
            "be enumerated by the person who does "
            "them.</b>",
            "<b>So the workaround is the finding, and they will not "
            "mention it</b> — the spreadsheet beside the application, "
            "the note on the monitor, the re-typing of something that "
            "could be copied.",
            "<b>Which is why contextual inquiry exists:</b> <b>watch "
            "them do the real work in the real place, and ask about what "
            "you see rather than about what they "
            "recall.</b>",
            "<b>And the physical environment is data</b> — "
            "<b>what is written down, what is printed out, what is kept "
            "in a second window</b> all record something the software "
            "failed to provide."]},

  {"t": "bullets", "kicker": "Observation", "title": "How to observe usefully",
   "items": [
     "<b>Go where the work happens</b>, because the environment "
     "is half the data — interruptions, other people, and the "
     "second screen are all part of it.",
     "",
     "<b>Adopt the apprentice stance:</b> <b>'teach me to do "
     "this'</b>, which makes their expertise the subject and licenses "
     "you to ask obvious questions.",
     "",
     "<b>Record the artefacts</b> — the spreadsheets, the "
     "notes, the printouts — since <b>each one is a feature "
     "request nobody filed.</b>",
     "",
     "<b>Note the interruptions and the recovery</b>, which no "
     "laboratory study will show you "
     "(Module 03 §1).",
     "",
     "<b>And ask about the exceptions</b>, because the unusual "
     "case is where the design usually breaks.",
   ],
   "footnote": "<b>Every artefact beside the software is a feature "
               "request nobody filed</b> — which makes a desk the "
               "cheapest requirements document available."},

  {"t": "section", "label": "Part 4", "title": "Analysis",
   "blurb": "Making it systematic rather than anecdotal."},

  {"t": "bullets", "kicker": "Analysis", "title": "How to analyse without just picking quotations",
   "items": [
     "<b>Transcribe or at least index the sessions</b>, because "
     "<b>working from memory selects for whatever was memorable</b> "
     "rather than for whatever was common.",
     "",
     "<b>Code the data: label every segment with a category</b>, "
     "and <b>let the categories emerge from the material</b> rather "
     "than imposing them (CSCE 638 §10 §4).",
     "",
     "<b>Then count the codes</b>, so that you know what recurred "
     "— which is not a rate and is better than an "
     "impression.",
     "",
     "<b>Have a second person code a sample</b> and compare, "
     "because <b>a coding scheme only you can apply is not a "
     "finding.</b>",
     "",
     "<b>And look for the disconfirming case</b>, which is the "
     "discipline that separates analysis from illustration.",
   ],
   "footnote": "<b>Looking for the disconfirming case is what "
               "distinguishes analysis from illustration</b> — a "
               "report of five supporting quotations is a selection, "
               "not a finding."},

  {"t": "callout", "title": "And what a qualitative finding honestly supports",
   "kind": "Closing",
   "body": ["<b>'This mechanism exists and here is how it works' "
            "— which is a strong and useful claim</b>, and is the "
            "one these methods are for.",
            "<b>'Eight of our twelve participants did X' — "
            "which is a description of twelve people</b> and is not an "
            "estimate of a population.",
            "<b>And not 'X% of users do this'</b>, which requires a "
            "sample designed for it "
            "(Module 08).",
            "<b>So report the number of participants, how they were "
            "recruited, and the mechanism rather than the "
            "rate</b> — <b>which is Module 13's form and is what "
            "makes a qualitative study citable.</b>"]},
 ],
 "takeaways": [
   "Qualitative methods generate hypotheses and explain mechanisms; "
   "measuring first means measuring whatever you happened to think of.",
   "Ask for behaviour rather than opinion or prediction — the past and "
   "the concrete rather than the hypothetical.",
   "'What would you want here' produces a feature request and 'what were "
   "you trying to do' produces a problem.",
   "People cannot accurately report their own behaviour, and the "
   "workaround is the finding they will not mention.",
   "Every artefact beside the software is a feature request nobody filed, "
   "which makes a desk a cheap requirements document.",
   "Looking for the disconfirming case is what distinguishes analysis from "
   "illustration.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What qualitative methods are for"),
  ("callout", "Qualitative methods generate hypotheses and explain "
              "mechanisms; they do not measure rates",
   ["<b>An experiment can tell you that design A is faster than design "
    "B; it cannot tell you why, or what else the participants were "
    "actually trying to accomplish</b> — which is exactly what "
    "qualitative work is for, and is frequently the more useful "
    "finding.",
    "<b>And it cannot tell you anything about the question you did not "
    "think to ask</b> — <b>which is the single largest risk in any "
    "study</b>, and the reason to look before you measure.",
    "<b>So the sequence is: observe to find out what matters, then "
    "measure the thing that turned out to matter</b> — and "
    "<b>measuring first means measuring whatever you happened to think "
    "of</b>, which may not be the variable that explains anything.",
    "<b>Which makes the two kinds of method complementary rather than "
    "competing:</b> <b>'eight of twelve people did X' from a "
    "qualitative study is not a rate, and is an excellent reason to go "
    "and measure one</b> (&sect;4's closing callout)."]),

  ("h1", "2 &nbsp; Interviews"),
  ("code", """ASK ABOUT THE PAST AND THE CONCRETE
    "Tell me about the last time you did this."
    "Walk me through what you did yesterday."
    "Show me."

DO NOT ASK ABOUT THE FUTURE OR THE HYPOTHETICAL
    "Would you use a feature that..."
    "How often do you think you would..."
    -- people are poor at predicting their own
    behaviour, and worse at predicting it to
    somebody who clearly wants a yes.

AND DO NOT ASK FOR SOLUTIONS
    "What would you want here?" produces a feature
    request. "What were you trying to do?" produces a
    problem, which is the thing you can design
    against.

THE RULE: ask for behaviour, not for opinion or
prediction. And then ask "why" until it stops being
informative."""),
  ("p", "<b>Ask for behaviour, not for opinion or prediction</b> — "
        "<b>which is the single rule that makes an interview worth "
        "running</b>, and <b>the past-and-concrete formulation is the "
        "whole technique</b>. The reason the solution question fails is "
        "worth stating: <b>a feature request encodes the person's model of "
        "what is possible</b>, which is narrower than yours, whereas "
        "<b>a problem statement leaves the solution space open</b> "
        "(Module 04 &sect;4's 'sometimes the user's model is better' "
        "is the exception, and it is about the domain rather than about "
        "the interface)."),
  ("callout", "And a leading question gets the answer you led toward",
   ["<b>'Was that confusing?' gets a yes; 'what were you thinking "
    "there?' gets a description</b> — and <b>only the second one is "
    "data</b>, because the first supplied both the category and the "
    "valence.",
    "<b>And the participant wants to be helpful</b>, which means "
    "<b>they will agree with whatever you appear to believe</b> rather "
    "than contradict somebody who has given up an hour to talk to them "
    "(Module 08 &sect;4's demand characteristics, in a "
    "conversational setting where they are stronger).",
    "<b>So keep your own hypothesis out of the room</b> — do not "
    "state it, do not hint at it, and do not react differently to "
    "confirming and disconfirming answers — and <b>be willing to sit "
    "through silence</b>, <b>which is where the unprompted material "
    "arrives.</b>",
    "<b>Which is the same discipline as Module 07 &sect;1's</b> "
    "— <b>the interviewer's job, like the facilitator's, is to be "
    "uninteresting</b> — <b>and it is equally difficult in both "
    "settings</b> and for the same reason: the natural social instinct is "
    "to be responsive."]),

  ("break",),
  ("h1", "3 &nbsp; Observation"),
  ("callout", "People cannot accurately report their own behaviour, which is "
              "not dishonesty",
   ["<b>Self-reported frequencies are unreliable</b> in a measured and "
    "systematic way, <b>workarounds are forgotten because they have "
    "become automatic</b>, and <b>the steps of a familiar task cannot be "
    "enumerated by the person who performs them</b> — expertise is "
    "exactly the compiling-away of the steps "
    "(Module 03 &sect;4).",
    "<b>So the workaround is the finding, and they will not mention "
    "it</b> — the spreadsheet kept open beside the application, the "
    "note stuck to the monitor, the value re-typed because it cannot be "
    "copied, the report exported and fixed by hand every Monday.",
    "<b>Which is precisely why contextual inquiry exists:</b> "
    "<b>watch them do the real work in the real place, and ask about "
    "what you can see rather than about what they can recall.</b>",
    "<b>And the physical environment is itself data</b> — "
    "<b>what is written down, what is printed out, what is kept in a "
    "second window, what is on a sticky note</b> — <b>all of which "
    "record something the software failed to provide</b> and which "
    "nobody filed a bug about."]),
  ("ul", ["<b>Go where the work actually happens</b>, because <b>the "
          "environment is half the data</b> — the interruptions, the "
          "other people, the phone, the second screen, and the noise are "
          "all part of the conditions the design has to work in.",
          "<b>Adopt the apprentice stance:</b> <b>'teach me how to do "
          "this'</b> — <b>which makes their expertise the subject "
          "and licenses you to ask obvious questions</b> without either "
          "party being embarrassed, and is a far better frame than "
          "'evaluate this'.",
          "<b>Record the artefacts</b> — the spreadsheets, the "
          "handwritten notes, the printouts, the bookmarks — since "
          "<b>each one is a feature request nobody filed</b> and is "
          "concrete evidence rather than an opinion.",
          "<b>Note the interruptions and how they recover from "
          "them</b>, which <b>no laboratory study will ever show you</b> "
          "(Module 03 &sect;1) and which may dominate the real "
          "experience of using the software.",
          "<b>And ask about the exceptions</b> — the unusual "
          "customer, the month-end case, the thing that went wrong last "
          "week — <b>because the unusual case is where the design "
          "usually breaks</b> and where the workarounds "
          "concentrate. <b>Every artefact beside the software is a "
          "feature request nobody filed</b>, which makes <b>a desk the "
          "cheapest requirements document available.</b>"]),

  ("h1", "4 &nbsp; Analysis"),
  ("ul", ["<b>Transcribe, or at the very least index, the "
          "sessions</b>, because <b>working from memory selects for "
          "whatever was most memorable</b> — the vivid complaint, the "
          "articulate participant — <b>rather than for whatever was "
          "most common.</b>",
          "<b>Code the data: label every segment with a "
          "category</b>, and <b>let the categories emerge from the "
          "material rather than imposing a scheme you brought</b> "
          "(CSCE 638 Module 10 &sect;4's same requirement for error "
          "analysis).",
          "<b>Then count the codes</b>, so that you know what "
          "recurred and how often within your sample — <b>which is "
          "not a population rate and is considerably better than an "
          "impression</b>, and is reportable as what it is.",
          "<b>Have a second person code a sample independently and "
          "compare</b>, because <b>a coding scheme that only you can "
          "apply is not a finding</b> — it is an interpretation, and "
          "the agreement rate is the evidence that it is more than "
          "that.",
          "<b>And look specifically for the disconfirming case</b> "
          "— the participant who did not do the thing, the session "
          "that contradicts the pattern. <b>Looking for the "
          "disconfirming case is what distinguishes analysis from "
          "illustration</b>: <b>a report of five supporting quotations is "
          "a selection, not a finding</b>, and the reader cannot tell how "
          "many contradicting ones were available."]),
  ("callout", "And what a qualitative finding honestly supports",
   ["<b>'This mechanism exists and here is how it works'</b> — "
    "<b>which is a strong and genuinely useful claim</b>, and is the one "
    "these methods are designed to support. Establishing that something "
    "happens at all, and by what route, is valuable and does not require "
    "a sample.",
    "<b>'Eight of our twelve participants did X'</b> — <b>which "
    "is a description of twelve people</b> and <b>is not an estimate of "
    "a population</b>, however much it reads like one.",
    "<b>And not 'X% of users do this'</b>, which <b>requires a sample "
    "designed for the purpose</b> (Module 08) and a sampling frame "
    "you almost certainly do not have.",
    "<b>So report the number of participants, how they were "
    "recruited, and the mechanism rather than the rate</b> — "
    "<b>which is Module 13's claim form and is what makes a "
    "qualitative study citable</b> rather than merely suggestive."]),
 ],
 "resources": [
   ("Beyer & Holtzblatt &mdash; Contextual Design",
    "https://www.elsevier.com/books/contextual-design/holtzblatt/978-0-12-800894-2",
    "<b>&sect;3's method in full</b> — the apprentice stance and the "
    "artefact collection, from its originators. Library copy."),
   ("Portigal &mdash; Interviewing Users",
    "https://rosenfeldmedia.com/books/interviewing-users/",
    "<b>&sect;2 practically</b> — short, and the question-phrasing "
    "advice is the best available. Library copy."),
   ("Lazar, Feng & Hochheiser, the qualitative chapters",
    "https://www.elsevier.com/books/research-methods-in-human-computer-interaction/lazar/978-0-12-805390-4",
    "<b>&sect;4's analysis</b> — coding, agreement, and what the "
    "results support. Library copy."),
   ("Nisbett & Wilson &mdash; Telling more than we can know (free)",
    "https://psycnet.apa.org/record/1978-00295-001",
    "<b>&sect;3's finding in the original</b> — the classic result on "
    "the unreliability of introspective reports."),
 ],
 "exercises": [
   "<b>Write ten interview questions</b> and classify each as "
   "behavioural, hypothetical, or solution-seeking.",
   "<b>Rewrite the bad ones.</b>",
   "<b>Run one interview</b> and count your own leading questions "
   "afterwards.",
   "<b>Sit through ten seconds of silence</b> deliberately and note what "
   "arrives.",
   "<b>Watch somebody do real work</b> in their own environment for an "
   "hour.",
   "<b>Photograph every artefact</b> on their desk and classify each as "
   "a feature request.",
   "<b>Ask them to describe the task first</b>, then watch, and compare "
   "the two accounts.",
   "<b>Code one session</b> with categories drawn from the material.",
   "<b>Have somebody else code a sample</b> and compute your "
   "agreement.",
   "<b>Find a disconfirming case</b> for your main finding, and report "
   "it.",
 ],
 "selfcheck": [
   "What do qualitative methods establish, and what do they not?",
   "Why observe before measuring?",
   "Give the rule about interview questions, with examples of each "
   "kind.",
   "Why does asking for solutions fail?",
   "Why does a leading question waste a session?",
   "Why can people not report their own behaviour?",
   "What is the finding they will not mention?",
   "Give five rules for observation, and what the artefacts are.",
   "Give five rules for analysis, and which separates it from "
   "illustration?",
   "What does a qualitative finding support, and what does it not?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Interfaces for Programmers",
 "subtitle": "APIs, errors, and configuration are user interfaces.",
 "question": "Why is this library hard to use?",
 "outcomes": [
     "Apply the course's principles to an API.",
     "Write an error message that helps.",
     "Explain what makes documentation usable.",
     "Design configuration so its state is visible.",
     "Evaluate a developer tool with the same methods.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "An API is an interface",
   "blurb": "And every principle applies unchanged."},

  {"t": "table", "kicker": "Mapping", "title": "The principles, applied to an API",
   "header": ["Principle", "In an API", "Failure"],
   "widths": [2.5, 4.3, 4.7],
   "rows": [
     ["<b>Visibility</b>", "<b>Discoverable from the type signature</b>", "<b>A string parameter with undocumented values</b>"],
     ["<b>Feedback</b>", "<b>Errors that say what went wrong</b>", "<b>A null return, or a generic exception</b>"],
     ["<b>Consistency</b>", "<b>Argument order and naming throughout</b>", "<b>Two functions with reversed arguments</b>"],
     ["<b>Constraints</b>", "<b>Types that make misuse uncompilable</b>", "<b>Everything is a string or an int</b>"],
     ["<b>Good defaults</b>", "<b>The safe thing happens with no arguments</b>", "<b>Insecure or slow unless configured</b>"],
     ["<b>Reversibility</b>", "<b>Operations that can be undone or retried</b>", "<b>A partial write with no rollback</b>"],
   ],
   "footnote": "<b>The constraints row is where types earn their "
               "keep</b> — which is CSCE 713 §04 §4's "
               "parse-don't-validate argument arriving as a usability "
               "principle rather than a security one.",
   "note": "The direct mapping is the module's whole argument."},

  {"t": "callout", "title": "The signature is the documentation that is actually read",
   "kind": "Why naming and types carry the weight",
   "body": ["<b>A programmer reads the signature, the parameter "
            "names, and the autocompletion</b> — and <b>reaches the "
            "prose documentation only when those have failed</b>, which "
            "is Module 01 §2's non-reading finding in a new "
            "population.",
            "<b>So a well-named function with a precise type is "
            "better documentation than a paragraph</b>, because it is "
            "present at the point of use.",
            "<b>And a boolean parameter is a documentation "
            "failure:</b> <b>'process(data, true)' is unreadable at "
            "the call site</b>, where an enumerated value would have "
            "been self-describing.",
            "<b>Which gives a concrete rule:</b> <b>if the call site "
            "is not readable without consulting the definition, the "
            "signature is wrong</b> — and that is a check you can "
            "apply mechanically in review."]},

  {"t": "section", "label": "Part 2", "title": "Error messages",
   "blurb": "The most-read and least-designed text in software."},

  {"t": "code", "kicker": "Errors", "title": "What an error message needs",
   "lang": "text", "code": """
  WHAT HAPPENED
      specifically, in terms the caller recognises

  WHAT THE PROGRAM WAS DOING
      the operation and the input, not the internal
      function name

  WHY IT FAILED
      the actual condition, with the actual values

  AND WHAT TO DO ABOUT IT
      the next step, or where to look

  SO: "Configuration key 'timeout' must be a positive
  integer; got 'none' in config.yaml line 14. Use 0
  to disable."

  NOT: "Invalid configuration."
  NOT: "Error: NullPointerException"
  NOT: "Something went wrong. Try again."

  AND INCLUDE THE VALUE. An error that does not say
  what the offending input was forces the reader to
  reproduce it, which is the most expensive thing an
  error message can do.
""",
   "caption": "<b>Include the offending value</b> — an error that "
              "omits it forces a reproduction, which is the most "
              "expensive failure an error message has.",
   "note": "The include-the-value rule is the single highest-return "
           "change here."},

  {"t": "callout", "title": "And an error message is read at the worst possible moment",
   "kind": "Which is why brevity and specificity both matter",
   "body": ["<b>The reader is interrupted, frustrated, and under "
            "time pressure</b> — which is exactly the state in which "
            "attention is least available "
            "(Module 03 §1).",
            "<b>So it has to be scannable:</b> <b>the specific "
            "condition first, the detail after, and no apology</b> "
            "— 'oops, something went wrong' spends the reader's "
            "attention on nothing.",
            "<b>And it must not blame the user</b>, which is both "
            "Module 01 §4's framing and a practical matter: "
            "<b>'invalid input' when the input was reasonable teaches "
            "nothing.</b>",
            "<b>Which makes error messages worth reviewing as "
            "deliberately as any other interface text</b> — and "
            "<b>they are typically written last, by whoever hit the "
            "condition</b>, which is why they are poor."]},

  {"t": "section", "label": "Part 3", "title": "Documentation",
   "blurb": "What makes it usable rather than complete."},

  {"t": "bullets", "kicker": "Documentation", "title": "The four kinds, and why conflating them fails",
   "items": [
     "<b>A tutorial</b> gets a newcomer to a first success. "
     "<b>Its job is a working result, not coverage</b> — and "
     "completeness actively harms it.",
     "",
     "<b>A how-to guide</b> solves a specific stated problem for "
     "somebody who knows the system.",
     "",
     "<b>Reference</b> describes the surface exhaustively and "
     "makes no attempt to teach — which is correct, and is "
     "what generated docs are good at.",
     "",
     "<b>And explanation</b> conveys the conceptual model "
     "(Module 04) — which is the kind most often "
     "missing and the most valuable.",
     "",
     "<b>Conflating them produces documentation that teaches "
     "nobody and references nothing</b> — which describes most "
     "of it.",
   ],
   "footnote": "<b>Explanation is the kind most often missing</b> "
               "— and it is the one that conveys the conceptual "
               "model, without which the reference is a list of "
               "names."},

  {"t": "section", "label": "Part 4", "title": "Configuration",
   "blurb": "Where state invisibility does the most damage."},

  {"t": "callout", "title": "A configuration system whose effective state is invisible cannot be reasoned about",
   "kind": "The characteristic failure of this category",
   "body": ["<b>Values come from defaults, a file, an environment "
            "variable, a command-line flag, and a remote "
            "service</b> — and <b>no interface shows which one won "
            "for a given setting.</b>",
            "<b>So the user cannot tell why the system is behaving as "
            "it is</b>, which is Module 01 §1's evaluation "
            "gap in its most consequential form.",
            "<b>And the fix is a command that prints the effective "
            "configuration with each value's source</b> — which is "
            "an afternoon's work and transforms "
            "debuggability.",
            "<b>Plus: validate at start-up rather than on "
            "use</b> — <b>a typo in a setting should fail "
            "immediately and not three hours later</b>, which is "
            "Module 01 §4's make-it-visible applied to "
            "configuration."]},

  {"t": "bullets", "kicker": "Practice", "title": "And evaluating a developer tool",
   "items": [
     "<b>Use the same methods.</b> <b>Watch five programmers try "
     "to accomplish a task with your library</b>, without helping "
     "(Module 07) — which almost nobody does.",
     "",
     "<b>The findings are the same kinds:</b> <b>missing "
     "signifiers, absent feedback, model mismatches</b>, diagnosed with "
     "Module 01 §1's vocabulary.",
     "",
     "<b>Watch what they search for</b>, because <b>the search "
     "query is the vocabulary they expected</b> and your naming did "
     "not match it.",
     "",
     "<b>And read your own issue tracker as usability "
     "data</b> — a recurring question is a design finding, not a "
     "documentation gap.",
     "",
     "<b>Which makes this the most actionable module in the "
     "course</b> for most of this program's graduates.",
   ],
   "footnote": "<b>A recurring question in your issue tracker is a "
               "design finding</b> — answering it again is treating "
               "the symptom, and it is free data you already "
               "have."},
 ],
 "takeaways": [
   "Every interaction principle applies to an API unchanged, and the "
   "constraints row is where types earn their keep.",
   "The signature is the documentation that is actually read, so a "
   "well-named function with a precise type beats a paragraph.",
   "If the call site is not readable without consulting the definition, the "
   "signature is wrong.",
   "Include the offending value in an error message — omitting it "
   "forces a reproduction, which is the most expensive failure available.",
   "Tutorial, how-to, reference, and explanation are four different "
   "things, and explanation is the one most often missing.",
   "A recurring question in your issue tracker is a design finding, and it "
   "is free data you already have.",
 ],
 "notes": [
  ("h1", "1 &nbsp; An API is an interface"),
  ("table", ["Principle", "What it means in an API", "The characteristic "
             "failure"],
   [["<b>Visibility</b>",
     "<b>The available operations are discoverable from the type "
     "signature and the autocompletion.</b>",
     "<b>A string parameter with undocumented permitted values</b>, "
     "which is invisible by construction."],
    ["<b>Feedback</b>",
     "<b>Errors that say what went wrong and what to do</b> "
     "(&sect;2).",
     "<b>A null return, or a generic exception with no context.</b>"],
    ["<b>Consistency</b>",
     "<b>Argument order, naming, and error behaviour the same "
     "throughout.</b>",
     "<b>Two related functions with reversed argument orders</b> — "
     "which produces silent bugs."],
    ["<b>Constraints</b>",
     "<b>Types that make the misuse fail to compile.</b>",
     "<b>Everything is a string or an int</b>, so any value can be "
     "passed anywhere. See the note."],
    ["<b>Good defaults</b>",
     "<b>The safe and common thing happens with no arguments at "
     "all.</b>",
     "<b>Insecure or slow unless explicitly configured</b> "
     "(CSCE 701 Module 11 &sect;3)."],
    ["<b>Reversibility</b>",
     "<b>Operations that can be undone, or safely retried.</b>",
     "<b>A partial write with no rollback</b> and no way to tell what "
     "succeeded."]],
   [0.20, 0.38, 0.42]),
  ("p", "<b>The constraints row is where types earn their keep</b> "
        "— which is <b>CSCE 713 Module 04 &sect;4's "
        "parse-don't-validate argument arriving as a usability principle "
        "rather than a security one</b>, and the convergence is worth "
        "noticing: a type that makes the invalid state unrepresentable is "
        "simultaneously a security control and a usability feature, for "
        "the same reason. <b>The direct mapping is this module's whole "
        "argument</b>: nothing new is required, only the recognition that "
        "programmers are users."),
  ("callout", "The signature is the documentation that is actually read",
   ["<b>A programmer reads the signature, the parameter names, and the "
    "autocompletion list</b> — and <b>reaches the prose "
    "documentation only when those have failed</b>, <b>which is "
    "Module 01 &sect;2's non-reading finding appearing in a new "
    "population</b> that likes to think it is exempt.",
    "<b>So a well-named function with a precise type is better "
    "documentation than a paragraph</b>, <b>because it is present at the "
    "point of use</b> and the paragraph is in a browser tab that was "
    "never opened.",
    "<b>And a boolean parameter is a documentation failure:</b> "
    "<b><code>process(data, true)</code> is unreadable at the call "
    "site</b>, where an enumerated value — "
    "<code>process(data, Mode.Strict)</code> — would have been "
    "self-describing at no cost.",
    "<b>Which gives a concrete and mechanical rule:</b> <b>if the "
    "call site is not readable without consulting the definition, the "
    "signature is wrong</b> — and <b>that is a check you can apply "
    "in code review without any argument about taste</b>, which makes it "
    "unusually actionable for this subject."]),

  ("h1", "2 &nbsp; Error messages"),
  ("code", """WHAT HAPPENED
    specifically, in terms the caller recognises

WHAT THE PROGRAM WAS DOING
    the operation and the input, not the internal
    function name

WHY IT FAILED
    the actual condition, with the actual values

AND WHAT TO DO ABOUT IT
    the next step, or where to look

SO: "Configuration key 'timeout' must be a positive
integer; got 'none' in config.yaml line 14. Use 0 to
disable."

NOT: "Invalid configuration."
NOT: "Error: NullPointerException"
NOT: "Something went wrong. Try again."

AND INCLUDE THE VALUE. An error that does not say
what the offending input was forces the reader to
reproduce it, which is the most expensive thing an
error message can do."""),
  ("p", "<b>Include the offending value</b> — <b>an error that "
        "omits it forces the reader to reproduce the failure in order to "
        "find out what it was objecting to</b>, <b>which is the most "
        "expensive failure an error message can have</b> and is extremely "
        "common. <b>The include-the-value rule is the single "
        "highest-return change available here</b>, and it is a one-line "
        "edit per message. (With one exception worth stating: "
        "<b>do not include a secret</b> — CSCE 711 Module 09 "
        "&sect;4's logging rule applies, and the fix is to include the "
        "length or the shape rather than the value.)"),
  ("callout", "And an error message is read at the worst possible moment",
   ["<b>The reader is interrupted, frustrated, and under time "
    "pressure</b> — <b>which is exactly the state in which attention "
    "is least available</b> (Module 03 &sect;1) and in which a long "
    "message will not be read at all.",
    "<b>So it has to be scannable:</b> <b>the specific condition "
    "first, the supporting detail after, and no apology</b> — "
    "<b>'oops, something went wrong' spends the reader's attention on "
    "nothing</b> and delays the useful part.",
    "<b>And it must not blame the user</b>, which is both "
    "<b>Module 01 &sect;4's framing</b> and a practical matter: "
    "<b>'invalid input' when the input was entirely reasonable teaches "
    "nothing</b> and antagonises somebody who is already having a bad "
    "time.",
    "<b>Which makes error messages worth reviewing as deliberately as "
    "any other interface text</b> — and <b>they are typically "
    "written last, in a hurry, by whoever happened to hit the "
    "condition</b>, <b>which is exactly why they are poor</b> and why "
    "reviewing them is high-return."]),

  ("break",),
  ("h1", "3 &nbsp; Documentation"),
  ("ul", ["<b>A tutorial</b> gets a newcomer to a first working "
          "result. <b>Its job is a working result, not coverage</b> "
          "— and <b>completeness actively harms it</b>, because every "
          "additional option is a decision the newcomer cannot make "
          "yet.",
          "<b>A how-to guide</b> solves one specific stated problem "
          "for somebody who already understands the system — 'how do "
          "I do X' — and should assume the tutorial was read.",
          "<b>Reference</b> describes the surface exhaustively and "
          "<b>makes no attempt to teach</b> — <b>which is correct, "
          "and is what generated documentation is genuinely good at</b>, "
          "provided nobody mistakes it for the other three.",
          "<b>And explanation</b> conveys the conceptual model "
          "(Module 04) — why the system is organised as it is, "
          "what the central abstractions mean, and what it is not for. "
          "<b>Which is the kind most often missing and the most "
          "valuable</b>, because without it the reference is a list of "
          "names.",
          "<b>Conflating them produces documentation that teaches "
          "nobody and references nothing</b> — a tutorial interrupted "
          "by exhaustive option lists, or a reference that keeps trying to "
          "explain — <b>which describes most of the documentation "
          "that exists</b>. <b>Explanation is the kind most often "
          "missing</b>, and writing it is the thing a maintainer is "
          "uniquely positioned to do."]),

  ("h1", "4 &nbsp; Configuration, and evaluation"),
  ("callout", "A configuration system whose effective state is invisible "
              "cannot be reasoned about",
   ["<b>Values arrive from compiled-in defaults, a configuration file, "
    "an environment variable, a command-line flag, and sometimes a remote "
    "service</b> — and <b>no interface shows which one won for any "
    "given setting.</b>",
    "<b>So the user cannot tell why the system is behaving as it "
    "is</b>, <b>which is Module 01 &sect;1's gulf of evaluation in "
    "its most consequential form</b>: not 'what did my action do' but "
    "'what is this system's actual state', which is unanswerable.",
    "<b>And the fix is a single command that prints the effective "
    "configuration with each value's source</b> — <b>which is an "
    "afternoon's work and transforms the debuggability of the whole "
    "system</b>, and is still absent from a great deal of widely used "
    "software.",
    "<b>Plus: validate at start-up rather than at point of use</b> "
    "— <b>a typo in a setting should fail immediately and loudly, "
    "not three hours later when the relevant code path is first "
    "reached</b> — which is <b>Module 01 &sect;4's "
    "make-the-error-visible applied to configuration</b> and is "
    "CSCE 713 Module 04 &sect;4's parse-at-the-boundary in another "
    "guise."]),
  ("ul", ["<b>Use the same methods.</b> <b>Watch five programmers "
          "try to accomplish a task with your library, without "
          "helping</b> (Module 07) — <b>which almost nobody "
          "does</b>, despite it being exactly as cheap and exactly as "
          "informative as for any other interface.",
          "<b>The findings are the same kinds:</b> <b>missing "
          "signifiers (an operation they could not find), absent feedback "
          "(an error that told them nothing), and model mismatches (they "
          "expected it to work differently)</b> — all diagnosed with "
          "Module 01 &sect;1's vocabulary.",
          "<b>Watch what they search for</b>, because <b>the search "
          "query is the vocabulary they expected</b> and <b>your naming "
          "did not match it</b> — which is Module 04 &sect;2's "
          "vocabulary point and is immediately actionable.",
          "<b>And read your own issue tracker as usability data</b> "
          "— <b>a recurring question is a design finding rather than "
          "a documentation gap</b>, and the fifth time it is asked is "
          "evidence rather than coincidence.",
          "<b>Which makes this the most actionable module in the "
          "course for most of this program's graduates</b>, since the "
          "interfaces they will design are APIs, error messages, "
          "configuration files, and tools. <b>A recurring question in "
          "your issue tracker is a design finding</b>: <b>answering it "
          "again is treating the symptom</b>, and <b>it is free data you "
          "already have.</b>"]),
 ],
 "resources": [
   ("Myers & Stylos &mdash; Improving API usability (free)",
    "https://dl.acm.org/doi/10.1145/2962732",
    "<b>&sect;1 with the empirical studies</b> — programmers watched "
    "using APIs, and what the failures were."),
   ("Proch&aacute;zka &mdash; Di&aacute;taxis documentation framework "
    "(free)",
    "https://diataxis.fr/",
    "<b>&sect;3's four kinds</b> — the clearest statement of the "
    "distinction and why conflating them fails."),
   ("Rust's error message guidelines, and the Elm compiler's approach "
    "(free)",
    "https://rustc-dev-guide.rust-lang.org/diagnostics.html",
    "<b>&sect;2 done well, deliberately</b> — two projects that "
    "treated error messages as an interface and documented how."),
   ("Bloch &mdash; How to Design a Good API and Why it Matters (free "
    "talk)",
    "https://www.infoq.com/presentations/effective-api-design/",
    "<b>&sect;1 from a practitioner</b> — and much of it maps onto "
    "&sect;1's table without being framed that way."),
 ],
 "exercises": [
   "<b>Map all six principles</b> onto an API you maintain, and find "
   "a failure for each.",
   "<b>Find a boolean parameter</b> in your own code and replace it with "
   "an enumerated type.",
   "<b>Apply the call-site readability test</b> to twenty call sites.",
   "<b>Rewrite five error messages</b> to include all four "
   "components.",
   "<b>Check that each includes the offending value</b> and no "
   "secrets.",
   "<b>Classify your own documentation</b> into the four kinds, and find "
   "which is missing.",
   "<b>Write the explanation document</b> for something you maintain.",
   "<b>Add a command that prints the effective configuration</b> with "
   "sources.",
   "<b>Move your configuration validation to start-up</b> and see what "
   "it catches.",
   "<b>Watch five programmers use your library</b> and record what they "
   "searched for.",
 ],
 "selfcheck": [
   "Map the six principles onto an API, with a failure for each.",
   "Why does the constraints row connect to CSCE 713?",
   "Why is the signature the documentation that is read?",
   "Give the call-site readability rule.",
   "Name the four components of an error message.",
   "Why is including the value the highest-return change, and what is "
   "the exception?",
   "Why is an error message read at the worst moment, and what "
   "follows?",
   "Name the four kinds of documentation and which is most often "
   "missing.",
   "Why can an invisible configuration state not be reasoned about?",
   "How do you evaluate a developer tool, and what free data do you "
   "have?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Input and Output",
 "subtitle": "Modalities, and what each one is good for.",
 "question": "Why is this interaction awkward on this device?",
 "outcomes": [
     "Explain Fitts's law and what it predicts.",
     "Explain the input modalities and their error "
     "characteristics.",
     "Explain latency's effect on interaction.",
     "Explain modality appropriateness.",
     "Choose an interaction for a device and a context.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Pointing",
   "blurb": "Which has a quantitative law."},

  {"t": "eq", "kicker": "Fitts's law", "title": "The one quantitative law in interface design",
   "eqs": [
     ("T = a + b · log₂(D/W + 1)",
      "Time to acquire a target, from the distance to it and its "
      "width along the direction of travel."),
     ("so: bigger is faster, and nearer is faster",
      "Logarithmically in both, which means doubling the size helps "
      "less than halving the distance to a small target."),
     ("and an edge target has effectively infinite width",
      "Which is why a screen-edge menu bar is faster to hit than a "
      "floating one of the same size."),
   ],
   "caption": "<b>The edge consequence is the non-obvious one</b> "
              "— a target you cannot overshoot behaves as if it were "
              "much larger.",
   "note": "Fitts's law is the only genuinely predictive law here; use "
           "it."},

  {"t": "bullets", "kicker": "Consequences", "title": "What Fitts's law tells you to do",
   "items": [
     "<b>Make frequently-used targets larger</b>, and "
     "<b>dangerous ones smaller or further away</b> — which is "
     "Module 03 §4's slip prevention with a "
     "number.",
     "",
     "<b>Put things at the edges and corners</b>, which are "
     "effectively infinite targets — and <b>corners are the "
     "fastest points on a screen.</b>",
     "",
     "<b>Keep related controls near where the pointer already "
     "is</b>, which is why a context menu beats a toolbar for a "
     "selection-specific action.",
     "",
     "<b>And beware of adjacent targets</b>, since the law "
     "predicts the travel and not the accuracy — <b>adjacency is "
     "what produces slips.</b>",
     "",
     "<b>On touch, the minimum size is set by the "
     "finger</b> — roughly nine millimetres, which is much larger "
     "than a cursor needs.",
   ],
   "footnote": "<b>Dangerous targets should be smaller and further "
               "away</b> — which is the deliberate use of the law "
               "against itself, and is the right design for a destructive "
               "action."},

  {"t": "section", "label": "Part 2", "title": "Modalities",
   "blurb": "Each with a different error profile."},

  {"t": "table", "kicker": "Input", "title": "The input modalities, and what each is for",
   "header": ["Modality", "Good for", "Error profile"],
   "widths": [2.5, 3.9, 4.9],
   "rows": [
     ["<b>Keyboard</b>", "<b>Text, and fast expert commands</b>", "<b>Typos; discoverable only if signified</b>"],
     ["<b>Mouse</b>", "<b>Precise pointing and selection</b>", "<b>Slips on adjacent targets</b>"],
     ["<b>Touch</b>", "<b>Direct manipulation; mobile</b>", "<b>Occlusion by the hand; imprecision; no hover</b>"],
     ["<b>Speech</b>", "<b>Hands-free; eyes-free</b>", "<b>Recognition errors, and no undo in the channel</b>"],
     ["<b>Gaze</b>", "<b>Selection when nothing else is available</b>", "<b>Involuntary movement; no natural click</b>"],
   ],
   "footnote": "<b>'No hover' is the touch constraint most often "
               "forgotten</b> — every tooltip, every preview, and "
               "every disabled-state explanation that depended on hover "
               "is unavailable.",
   "note": "The no-hover consequence breaks a lot of desktop design "
           "patterns."},

  {"t": "callout", "title": "Speech has no cheap undo, which changes the whole interaction",
   "kind": "The constraint that is specific to it",
   "body": ["<b>A misrecognised word must be corrected by speaking "
            "again</b> — which is slower than the original input and "
            "may itself be misrecognised, so <b>errors compound rather "
            "than resolve.</b>",
            "<b>And there is no equivalent of pointing at the "
            "mistake:</b> <b>the channel is linear and has no "
            "spatial reference</b>, so 'no, the other one' is hard to "
            "express.",
            "<b>Which means a speech interface must be designed around "
            "confirmation and correction rather than around "
            "input</b> — and the confirmation cost is what makes long "
            "speech interactions unpleasant.",
            "<b>So speech suits short commands with clear "
            "confirmations, and suits dictation badly</b> unless "
            "a visual channel is available for correction — which is "
            "why dictation on a screen works and dictation to a speaker "
            "does not."]},

  {"t": "section", "label": "Part 3", "title": "Latency",
   "blurb": "Which changes behaviour, not only satisfaction."},

  {"t": "code", "kicker": "Latency", "title": "The thresholds, and what each one changes",
   "lang": "text", "code": """
  ~100 ms   feels instantaneous. The action and the
            result are one event.

  ~1 s      the flow of thought is preserved, and
            the delay is noticed. No feedback needed
            beyond the result.

  ~10 s     attention is lost. The user will switch
            to something else, and needs a progress
            indicator and an estimate to decide
            whether to wait.

  AND THE SECOND-ORDER EFFECTS
      people type more slowly when echo is delayed
      they click again when nothing happened
      they lose the causal connection between the
          action and the result, which breaks the
          evaluation gap (Module 01 section 1)
      and VARIABLE latency is worse than uniformly
          slow latency, because it defeats prediction
""",
   "caption": "<b>Variable latency is worse than uniformly slow "
              "latency</b> — because the user cannot form an "
              "expectation, and so cannot plan around it.",
   "note": "The variability finding is the one systems people need "
           "most."},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "By device, context, and what else is going on."},

  {"t": "bullets", "kicker": "Choosing", "title": "What determines the right interaction",
   "items": [
     "<b>What the hands and eyes are doing.</b> <b>Driving, "
     "cooking, and walking each remove a channel</b> — and a "
     "design assuming full visual attention fails in all "
     "three.",
     "",
     "<b>The precision available.</b> <b>A finger is not a "
     "cursor, and a controller is not either</b> — so target "
     "sizes and the whole layout change.",
     "",
     "<b>The environment.</b> <b>Noise defeats speech; sunlight "
     "defeats low contrast; gloves defeat capacitive "
     "touch</b> — all of which are design constraints rather than "
     "user problems.",
     "",
     "<b>And the social setting</b>, since <b>speech and gesture "
     "are public</b> in a way that typing is not.",
     "",
     "<b>So the modality follows from the context</b>, and "
     "<b>a context nobody specified gets a desktop "
     "design.</b>",
   ],
   "footnote": "<b>A context nobody specified gets a desktop "
               "design</b>, which is then deployed on a phone in "
               "sunlight to somebody holding a bag — and the "
               "failures are blamed on them."},

  {"t": "callout", "title": "And the accessibility connection",
   "kind": "Closing",
   "body": ["<b>Every constraint in this module is somebody's "
            "permanent condition</b> — <b>a design that works "
            "one-handed, eyes-free, or without fine motor control works "
            "for far more people than the situational cases "
            "suggest.</b>",
            "<b>Which is CSCE 632's argument, and it is an argument "
            "about design quality rather than about "
            "accommodation.</b>",
            "<b>And the situational framing is the persuasive "
            "one:</b> <b>'usable while holding a child' and 'usable "
            "one-handed permanently' are the same design "
            "requirement.</b>",
            "<b>So design for the constraint rather than for the "
            "population</b> — <b>which makes the requirement "
            "general and the benefit broad</b>, and is where this module "
            "hands over to CSCE 632."]},
 ],
 "takeaways": [
   "Fitts's law is the one genuinely predictive law here, and an edge "
   "target has effectively infinite width.",
   "Dangerous targets should be smaller and further away, which is the "
   "deliberate use of the law against itself.",
   "'No hover' is the touch constraint most often forgotten, and it breaks "
   "every tooltip and preview pattern.",
   "Speech has no cheap undo and no spatial reference, so errors compound "
   "rather than resolve.",
   "Variable latency is worse than uniformly slow latency, because the "
   "user cannot form an expectation.",
   "Every constraint in this module is somebody's permanent condition, "
   "which makes situational and permanent needs the same design "
   "requirement.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Pointing"),
  ("eq", "T = a + b &middot; log<sub>2</sub>(D/W + 1)"),
  ("ul", ["<b>The time to acquire a target</b>, from the distance to "
          "it and its width along the direction of travel — and it "
          "is <b>the one genuinely quantitative and predictive law in "
          "interface design</b>, which makes it worth knowing "
          "precisely.",
          "<b>So bigger is faster and nearer is faster</b>, "
          "<b>logarithmically in both</b> — <b>which means doubling a "
          "target's size helps less than halving the distance to a small "
          "one</b>, and the logarithm is why very large targets stop "
          "helping.",
          "<b>And an edge target has effectively infinite width</b> "
          "along the direction of travel, <b>because the pointer cannot "
          "overshoot it</b> — <b>which is why a screen-edge menu bar "
          "is measurably faster to hit than a floating one of the same "
          "visible size.</b>",
          "<b>The edge consequence is the non-obvious one</b>, and it "
          "is the most useful: <b>a target you cannot overshoot behaves "
          "as though it were much larger</b>, which is a free improvement "
          "available to any design that can place something at an edge or "
          "a corner."]),
  ("ul", ["<b>Make frequently-used targets larger</b>, and "
          "<b>dangerous ones smaller or further away</b> — which is "
          "<b>Module 03 &sect;4's slip prevention with a number "
          "attached</b> and is a quantitative design decision rather than "
          "a judgement.",
          "<b>Put things at the edges and the corners</b>, which are "
          "effectively infinite targets — and <b>corners are the "
          "fastest points on a screen</b>, being infinite in two "
          "directions at once.",
          "<b>Keep related controls near where the pointer already "
          "is</b>, which is <b>why a context menu beats a toolbar for a "
          "selection-specific action</b>: the distance is zero by "
          "construction.",
          "<b>And beware of adjacent targets</b>, since <b>the law "
          "predicts the travel time and says nothing about the "
          "accuracy</b> — <b>adjacency is what produces slips</b> "
          "(Module 03 &sect;4), so speed and safety pull apart here "
          "and have to be traded deliberately.",
          "<b>On touch, the minimum target size is set by the "
          "finger</b> rather than by the display — roughly nine "
          "millimetres regardless of resolution — <b>which is much "
          "larger than a cursor needs</b> and is why a dense desktop "
          "layout cannot simply be scaled. <b>Dangerous targets should "
          "be smaller and further away</b>, which is <b>the deliberate "
          "use of the law against itself</b> and is the right design for "
          "a destructive action."]),

  ("h1", "2 &nbsp; Modalities"),
  ("table", ["Modality", "What it is good for", "Its error profile"],
   [["<b>Keyboard</b>",
     "<b>Text entry, and fast expert command invocation.</b>",
     "<b>Typos; and the commands are discoverable only if signified</b> "
     "(Module 03 &sect;3)."],
    ["<b>Mouse or trackpad</b>",
     "<b>Precise pointing, selection, and dragging.</b>",
     "<b>Slips on adjacent targets</b> (&sect;1)."],
    ["<b>Touch</b>",
     "<b>Direct manipulation, and anything mobile.</b>",
     "<b>Occlusion by the hand, imprecision, and no hover state at "
     "all</b> — see the note."],
    ["<b>Speech</b>",
     "<b>Hands-free and eyes-free operation.</b>",
     "<b>Recognition errors, and no undo within the channel</b> (see "
     "the callout)."],
    ["<b>Gaze</b>",
     "<b>Selection when no other channel is available at all.</b>",
     "<b>Involuntary movement, and no natural equivalent of a "
     "click.</b>"]],
   [0.19, 0.33, 0.48]),
  ("p", "<b>'No hover' is the touch constraint most often "
        "forgotten</b> — <b>every tooltip, every preview, every "
        "hover-to-reveal control, and every disabled-state explanation "
        "that depended on hovering is simply unavailable</b>, and <b>the "
        "no-hover consequence breaks a great many desktop design "
        "patterns</b> that are otherwise portable. The usual response is "
        "to move the information into a tap, which costs a step; the "
        "better response is to make it unnecessary."),
  ("callout", "Speech has no cheap undo, which changes the whole interaction",
   ["<b>A misrecognised word must be corrected by speaking again</b> "
    "— <b>which is slower than the original input was and may itself "
    "be misrecognised</b>, so <b>errors compound rather than "
    "resolve</b>, which is a qualitatively different failure mode from "
    "any other modality's.",
    "<b>And there is no equivalent of pointing at the mistake:</b> "
    "<b>the channel is linear and has no spatial reference</b>, so 'no, "
    "the other one' is genuinely hard to express and 'the third item' "
    "requires the system to have numbered them.",
    "<b>Which means a speech interface has to be designed around "
    "confirmation and correction rather than around input</b> — and "
    "<b>the confirmation cost is exactly what makes long speech "
    "interactions unpleasant</b>, since every step needs one.",
    "<b>So speech suits short commands with clear confirmations, and "
    "suits dictation badly</b> unless a visual channel is available for "
    "correction — <b>which is why dictation onto a screen works well "
    "and dictation to a speaker does not</b>, and the difference is the "
    "correction channel rather than the recognition quality."]),

  ("break",),
  ("h1", "3 &nbsp; Latency"),
  ("code", """~100 ms   feels instantaneous. The action and the
          result are perceived as one event.

~1 s      the flow of thought is preserved, and the
          delay is noticed. No feedback needed beyond
          the result itself.

~10 s     attention is lost. The user will switch to
          something else, and needs a progress
          indicator and an estimate in order to
          decide whether to wait.

AND THE SECOND-ORDER EFFECTS
    people type more slowly when the echo is delayed
    they click again when nothing appeared to happen
    they lose the causal connection between the
        action and the result, which breaks the gulf
        of evaluation (Module 01 section 1)
    and VARIABLE latency is worse than uniformly slow
        latency, because it defeats prediction"""),
  ("p", "<b>Variable latency is worse than uniformly slow latency</b> "
        "— <b>because the user cannot form an expectation, and so "
        "cannot plan around it</b>: with a consistent two-second delay "
        "they learn to wait, and with a delay between 0.1 and four seconds "
        "they click again. <b>The variability finding is the one systems "
        "people need most</b>, because the usual optimisation target is "
        "the mean and <b>the tail is what determines the experience</b> "
        "(CSCE 670 Module 04 &sect;4's same point about "
        "percentiles)."),

  ("h1", "4 &nbsp; Choosing"),
  ("ul", ["<b>What the hands and the eyes are doing.</b> <b>Driving, "
          "cooking, carrying something, and walking each remove a "
          "channel</b> — and <b>a design assuming full visual and "
          "manual attention fails in all four</b>, which covers a large "
          "fraction of mobile use.",
          "<b>The precision available.</b> <b>A finger is not a "
          "cursor, and a game controller is not either</b> — so the "
          "target sizes and in fact the whole layout change, rather than "
          "scaling (&sect;1's nine millimetres).",
          "<b>The environment.</b> <b>Noise defeats speech; "
          "sunlight defeats low contrast; gloves defeat capacitive touch; "
          "cold defeats fine motor control</b> — <b>all of which are "
          "design constraints rather than user problems</b> "
          "(Module 01 &sect;2).",
          "<b>And the social setting</b>, since <b>speech and gesture "
          "are public in a way that typing is not</b> — which is why "
          "voice assistants are used far less in offices and on public "
          "transport than their designers expected.",
          "<b>So the modality follows from the context</b>, and <b>a "
          "context nobody specified gets a desktop design</b> — "
          "<b>which is then deployed on a phone, in sunlight, to somebody "
          "holding a bag, and the failures are blamed on them.</b> "
          "Specifying the context is therefore part of the design rather "
          "than a preliminary to it."]),
  ("callout", "And the accessibility connection",
   ["<b>Every constraint in this module is somebody's permanent "
    "condition</b> — <b>a design that works one-handed, eyes-free, "
    "or without fine motor control works for far more people than the "
    "situational cases alone would suggest</b>, because it works for both "
    "populations at once.",
    "<b>Which is CSCE 632's argument</b>, and <b>it is an argument "
    "about design quality rather than about accommodation</b> — the "
    "constraint produces a better design for everybody, which is a "
    "stronger claim than fairness and does not depend on it.",
    "<b>And the situational framing is the persuasive one:</b> "
    "<b>'usable while holding a child' and 'usable one-handed "
    "permanently' are precisely the same design requirement</b>, and the "
    "first is easier to get approved.",
    "<b>So design for the constraint rather than for the "
    "population</b> — <b>which makes the requirement general and the "
    "benefit broad</b> — and <b>is where this module hands over to "
    "CSCE 632</b>, which develops it properly."]),
 ],
 "resources": [
   ("MacKenzie &mdash; Fitts' law as a research and design tool (free)",
    "https://www.yorku.ca/mack/hci1992.html",
    "<b>&sect;1 in depth</b> — the formulations, the measurement "
    "method, and the two-dimensional extensions."),
   ("Card, Moran & Newell &mdash; The Psychology of Human-Computer "
    "Interaction",
    "https://www.taylorfrancis.com/books/mono/10.1201/9780203736166/",
    "<b>&sect;1 and &sect;3's foundations</b> — where the timing "
    "constants in this module come from. Library copy."),
   ("Nielsen &mdash; Response Times: The 3 Important Limits (free)",
    "https://www.nngroup.com/articles/response-times-3-important-limits/",
    "<b>&sect;3's thresholds</b>, with the sources and the behavioural "
    "consequences."),
   ("Material and Apple human interface guidelines (free)",
    "https://developer.apple.com/design/human-interface-guidelines/",
    "<b>&sect;2's touch constraints as platform guidance</b> — "
    "including the minimum target sizes and the reasons."),
 ],
 "exercises": [
   "<b>Measure your own Fitts's law constants</b> with a simple "
   "pointing task.",
   "<b>Time hitting a corner against a same-sized target in the "
   "middle.</b>",
   "<b>Find a destructive control adjacent to a common one</b> and move "
   "it.",
   "<b>Measure a touch target in your own interface</b> and compare "
   "against nine millimetres.",
   "<b>Find every hover-dependent element</b> in a desktop design and "
   "say what happens on touch.",
   "<b>Try correcting a speech recognition error by voice alone</b>, and "
   "count the attempts.",
   "<b>Add 300 ms of latency</b> to an interaction and observe your own "
   "behaviour.",
   "<b>Add variable latency between 50 ms and 2 s</b> and compare.",
   "<b>Use an interface one-handed</b> and list what fails.",
   "<b>Specify the context</b> for something you are designing, in three "
   "sentences.",
 ],
 "selfcheck": [
   "State Fitts's law and what it predicts.",
   "Why is an edge target effectively infinite, and why are corners "
   "fastest?",
   "Give five design consequences, including the deliberate inverse "
   "use.",
   "Name five input modalities with their error profiles.",
   "What is the touch constraint most often forgotten?",
   "Why does speech have no cheap undo, and what follows?",
   "Give the three latency thresholds and what changes at each.",
   "Why is variable latency worse than slow latency?",
   "Name four things that determine the right modality.",
   "State the accessibility connection and why it is a quality "
   "argument.",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Manipulative Design",
 "subtitle": "The same techniques, aimed at the user.",
 "question": "When does persuasion become manipulation?",
 "outcomes": [
     "Recognise the standard deceptive patterns.",
     "Explain the mechanism each one exploits.",
     "Distinguish persuasion from manipulation.",
     "Explain the professional position and its limits.",
     "Review a design for manipulative patterns.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The patterns",
   "blurb": "Named, because naming makes them visible."},

  {"t": "table", "kicker": "Patterns", "title": "The standard patterns and the mechanism each exploits",
   "header": ["Pattern", "What it does", "Exploits"],
   "widths": [2.7, 3.9, 5.1],
   "rows": [
     ["<b>Confirmshaming</b>", "<b>Makes declining feel shameful</b>", "<b>Social discomfort</b>"],
     ["<b>Roach motel</b>", "<b>Easy to enter, hard to leave</b>", "<b>Asymmetric effort tolerance</b>"],
     ["<b>Preselected opt-in</b>", "<b>Consent by default</b>", "<b>Default dominance (M05 §3)</b>"],
     ["<b>Misdirection</b>", "<b>Emphasises the choice you want</b>", "<b>Preattentive capture (M02 §3)</b>"],
     ["<b>Forced continuity</b>", "<b>Charges silently after a trial</b>", "<b>Forgetting and inattention</b>"],
     ["<b>Manufactured urgency</b>", "<b>False scarcity or countdowns</b>", "<b>Loss aversion</b>"],
     ["<b>Obstruction</b>", "<b>Many steps for one direction only</b>", "<b>Effort asymmetry</b>"],
   ],
   "footnote": "<b>Every mechanism in the right-hand column was "
               "introduced earlier in this course as a design "
               "constraint</b> — which is the module's "
               "point: the techniques are identical and the aim is "
               "reversed.",
   "note": "The same-mechanisms observation is what makes this module "
           "belong here."},

  {"t": "callout", "title": "These are the course's own findings, applied against the user",
   "kind": "Why this module is not an appendix",
   "body": ["<b>Default dominance</b> (Module 05 §3), "
            "<b>preattentive capture</b> (Module 02 §3), "
            "<b>limited attention</b> (Module 03 §1), and "
            "<b>the non-reading finding</b> "
            "(Module 01 §2) — <b>all of them are "
            "exploitable, and all of them are being "
            "exploited.</b>",
            "<b>Which means the knowledge in this course is "
            "dual-use</b> — <b>there is no version of it that helps "
            "you design well and does not also help you manipulate</b>, "
            "and pretending otherwise would be dishonest.",
            "<b>So the distinction has to be in the aim rather than "
            "in the technique</b> — which is Part 3's "
            "subject and is where the useful line is.",
            "<b>And recognising a pattern is most of resisting "
            "it</b>, which is why they are catalogued and named: a "
            "named pattern is arguable in a design "
            "review."]},

  {"t": "section", "label": "Part 2", "title": "Why they work",
   "blurb": "The mechanisms, which are the ones you already know."},

  {"t": "bullets", "kicker": "Mechanisms", "title": "The exploited properties, each from an earlier module",
   "items": [
     "<b>Defaults are not changed</b> "
     "(Module 05 §3) — so a preselected checkbox is "
     "consent from most people, which is the most "
     "effective pattern there is.",
     "",
     "<b>Emphasis captures attention preattentively</b> "
     "(Module 02 §3) — so making one button prominent and "
     "the other grey decides the outcome without "
     "lying.",
     "",
     "<b>Attention is finite and interruptions are "
     "costly</b> (Module 03 §1) — so a request at a "
     "moment of focus is accepted to be rid of "
     "it.",
     "",
     "<b>Nobody reads</b> "
     "(Module 01 §2) — so disclosure in prose is "
     "disclosure that did not happen.",
     "",
     "<b>And effort asymmetry works</b>: <b>people abandon a "
     "ten-step cancellation and complete a one-step "
     "signup.</b>",
   ],
   "footnote": "<b>The effort asymmetry is the one that needs no "
               "deception at all</b> — every step is honest, and the "
               "aggregate is a design that prevents people from leaving."},

  {"t": "section", "label": "Part 3", "title": "Persuasion and manipulation",
   "blurb": "A distinction worth being able to state."},

  {"t": "callout", "title": "Persuasion addresses the person's judgement; manipulation bypasses it",
   "kind": "The distinction, stated usably",
   "body": ["<b>Telling somebody a true, relevant fact so they can "
            "decide better is persuasion</b> — and <b>a good default "
            "chosen for their benefit and visibly changeable is "
            "too.</b>",
            "<b>Exploiting a known cognitive limitation to produce a "
            "choice they would not make on reflection is "
            "manipulation</b> — and the test is whether the "
            "technique survives being explained to "
            "them.",
            "<b>Which is the operative test:</b> <b>would you be "
            "comfortable telling the user exactly how this works?</b> "
            "<b>'We made the decline button grey because people click "
            "the prominent one' fails it.</b>",
            "<b>And it is a usable test precisely because it does not "
            "require agreeing on a theory of autonomy</b> — <b>it "
            "only requires imagining the explanation</b>, which anybody "
            "can do in a design review."]},

  {"t": "bullets", "kicker": "Edges", "title": "And the genuinely difficult cases",
   "items": [
     "<b>A safe default the user would not have chosen</b> "
     "— which is paternalistic and is frequently right "
     "(CSCE 701 §11 §3).",
     "",
     "<b>Friction on a destructive action</b>, which is "
     "obstruction aimed at the user's benefit — and is the same "
     "technique.",
     "",
     "<b>Genuine scarcity, honestly displayed</b>, which is "
     "indistinguishable at a glance from the manufactured "
     "kind.",
     "",
     "<b>And a design that is simply <i>better</i> at what it "
     "does</b>, which increases engagement without any "
     "intent.",
     "",
     "<b>So the test is the aim and the explainability</b>, not "
     "the technique — which is why a list of forbidden "
     "techniques is not the answer.",
   ],
   "footnote": "<b>A list of forbidden techniques is not the "
               "answer</b>, because every one of them has a legitimate "
               "use — which is why the explainability test does the "
               "work."},

  {"t": "section", "label": "Part 4", "title": "The professional position",
   "blurb": "What to do when asked."},

  {"t": "callout", "title": "You will be asked to build these, and the useful response is a measurement",
   "kind": "The practical position",
   "body": ["<b>The request usually arrives as a metric:</b> "
            "<b>'increase signups', 'reduce churn'</b> — and the "
            "manipulative implementation is frequently the cheapest way "
            "to move it.",
            "<b>So the effective counter is measuring the cost "
            "rather than objecting on principle:</b> <b>the support "
            "load, the refund rate, the complaint rate, and the "
            "retention of users who felt tricked.</b>",
            "<b>Because manipulated conversions are worse "
            "conversions</b> — <b>a subscription somebody did not "
            "mean to start is cancelled, charged back, or complained "
            "about</b>, and those costs land elsewhere in the "
            "organisation.",
            "<b>And where the measurement does not win, say so "
            "plainly and let the decision be made explicitly</b> — "
            "<b>which is a smaller thing than refusing and is usually "
            "available.</b>"]},

  {"t": "bullets", "kicker": "Review", "title": "Reviewing a design for these patterns",
   "items": [
     "<b>Compare the effort of the two directions</b> — "
     "signing up against cancelling, opting in against opting "
     "out.",
     "",
     "<b>Check the visual weight of the options</b>, and whether "
     "the recommended one is recommended for the user's "
     "benefit.",
     "",
     "<b>Check what is preselected</b>, and whether anybody chose "
     "it deliberately (Module 05 §3).",
     "",
     "<b>Apply the explainability test</b> to each persuasive "
     "element (Part 3).",
     "",
     "<b>And read the flow as somebody who wants to "
     "leave</b>, which is the perspective nobody designs "
     "for.",
   ],
   "footnote": "<b>Reading the flow as somebody who wants to leave is "
               "the review nobody runs</b> — and it finds the "
               "obstruction patterns immediately."},
 ],
 "takeaways": [
   "Every mechanism these patterns exploit was introduced earlier in the "
   "course as a design constraint — the techniques are identical and "
   "the aim is reversed.",
   "The knowledge in this course is dual-use, and there is no version that "
   "helps you design well without also helping you manipulate.",
   "Effort asymmetry needs no deception at all: every step is honest and "
   "the aggregate prevents people from leaving.",
   "The operative test is whether you would be comfortable telling the "
   "user exactly how the technique works.",
   "A list of forbidden techniques is not the answer, because every one "
   "has a legitimate use.",
   "Manipulated conversions are worse conversions, which makes measurement "
   "a more effective counter than objection.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The patterns"),
  ("table", ["Pattern", "What it does", "The mechanism it exploits"],
   [["<b>Confirmshaming</b>",
     "<b>Phrases the decline option so that choosing it feels "
     "shameful.</b>",
     "<b>Social discomfort</b> — 'No thanks, I don't want to save "
     "money'."],
    ["<b>Roach motel</b>",
     "<b>Easy to enter and disproportionately hard to leave.</b>",
     "<b>Asymmetric tolerance for effort</b> (&sect;2's last point)."],
    ["<b>Preselected opt-in</b>",
     "<b>Obtains consent by default rather than by choice.</b>",
     "<b>Default dominance</b> (Module 05 &sect;3) — the most "
     "effective of all of these."],
    ["<b>Visual misdirection</b>",
     "<b>Emphasises the option the designer wants chosen.</b>",
     "<b>Preattentive capture</b> (Module 02 &sect;3)."],
    ["<b>Forced continuity</b>",
     "<b>Begins charging silently when a free trial ends.</b>",
     "<b>Forgetting and inattention</b> (Module 03)."],
    ["<b>Manufactured urgency</b>",
     "<b>False scarcity, countdown timers, 'three others are viewing "
     "this'.</b>",
     "<b>Loss aversion</b>, which is a strong and well-measured "
     "effect."],
    ["<b>Obstruction</b>",
     "<b>Many steps required in one direction and one step in the "
     "other.</b>",
     "<b>Effort asymmetry</b> — see the note."]],
   [0.22, 0.33, 0.45]),
  ("callout", "These are the course's own findings, applied against the user",
   ["<b>Default dominance</b> (Module 05 &sect;3), "
    "<b>preattentive capture</b> (Module 02 &sect;3), <b>limited "
    "attention</b> (Module 03 &sect;1), and <b>the non-reading "
    "finding</b> (Module 01 &sect;2) — <b>all of them are "
    "exploitable, and all of them are being exploited commercially at "
    "scale.</b>",
    "<b>Which means the knowledge in this course is "
    "dual-use</b> — <b>there is no version of it that helps you "
    "design well and does not also help you manipulate</b> — and "
    "<b>pretending otherwise would be dishonest</b>, which is why this "
    "module is in the course rather than omitted from it.",
    "<b>So the distinction has to lie in the aim rather than in the "
    "technique</b> — which is &sect;3's subject and is where the "
    "only usable line can be drawn, since the techniques are "
    "identical.",
    "<b>And recognising a pattern is most of resisting it</b>, which "
    "is <b>precisely why they are catalogued and named</b>: <b>a named "
    "pattern is arguable in a design review</b>, where an unnamed "
    "discomfort is not and loses to a metric."]),

  ("h1", "2 &nbsp; Why they work"),
  ("ul", ["<b>Defaults are not changed</b> (Module 05 "
          "&sect;3) — so <b>a preselected checkbox is consent from "
          "most people</b>, and <b>it is the most effective pattern in "
          "the table</b> precisely because it exploits the strongest "
          "finding in the course.",
          "<b>Emphasis captures attention preattentively</b> "
          "(Module 02 &sect;3) — so <b>making one button "
          "prominent and the other grey decides the outcome without any "
          "false statement being made</b>, which is what makes it hard to "
          "object to on factual grounds.",
          "<b>Attention is finite and interruptions are costly</b> "
          "(Module 03 &sect;1) — so <b>a request made at a moment "
          "of focus is accepted simply to be rid of it</b>, which is why "
          "the timing of a prompt is part of the pattern.",
          "<b>Nobody reads</b> (Module 01 &sect;2) — so "
          "<b>disclosure in prose is disclosure that did not "
          "happen</b>, and a design can be simultaneously fully "
          "disclosed and fully deceptive.",
          "<b>And effort asymmetry works</b>: <b>people abandon a "
          "ten-step cancellation and complete a one-step "
          "signup.</b> <b>The effort asymmetry is the one that needs no "
          "deception at all</b> — <b>every individual step is "
          "honest, and the aggregate is a design that prevents people "
          "from leaving</b>, which is why it survives legal review and is "
          "the pattern to watch for most closely."]),

  ("break",),
  ("h1", "3 &nbsp; Persuasion and manipulation"),
  ("callout", "Persuasion addresses the person's judgement; manipulation "
              "bypasses it",
   ["<b>Telling somebody a true and relevant fact so that they can "
    "decide better is persuasion</b> — and <b>a good default chosen "
    "for their benefit and visibly changeable is persuasion too</b>, "
    "since it informs rather than circumvents.",
    "<b>Exploiting a known cognitive limitation in order to produce a "
    "choice they would not make on reflection is manipulation</b> — "
    "and <b>the test is whether the technique survives being explained "
    "to them.</b>",
    "<b>Which is the operative test:</b> <b>would you be comfortable "
    "telling the user exactly how this works?</b> <b>'We made the "
    "decline button grey because people click the prominent one' fails "
    "it</b> immediately and obviously, whereas 'we preselected the safe "
    "option' does not.",
    "<b>And it is a usable test precisely because it does not require "
    "agreeing on a theory of autonomy</b> — <b>it only requires "
    "imagining the explanation</b>, <b>which anybody can do in a design "
    "review</b> and which does not depend on anybody's philosophical "
    "commitments. That makes it the rare ethical criterion that is "
    "actually operable in a meeting."]),
  ("ul", ["<b>A safe default the user would not have chosen</b> "
          "— which <b>is paternalistic and is frequently right</b> "
          "(CSCE 701 Module 11 &sect;3's security defaults), and "
          "which passes the explainability test easily.",
          "<b>Friction deliberately added to a destructive "
          "action</b>, which <b>is obstruction aimed at the user's own "
          "benefit</b> — <b>and is exactly the same technique</b> as "
          "the roach motel, differing only in whose interest it "
          "serves.",
          "<b>Genuine scarcity, honestly displayed</b>, which <b>is "
          "indistinguishable at a glance from the manufactured kind</b> "
          "— and which the manufactured kind has made less credible "
          "for everybody, a collective cost.",
          "<b>And a design that is simply <i>better</i> at what it "
          "does</b>, which <b>increases engagement without any "
          "manipulative intent at all</b> — so engagement is not "
          "itself evidence of anything.",
          "<b>So the test is the aim and the explainability, not the "
          "technique</b> — <b>which is why a list of forbidden "
          "techniques is not the answer</b>: <b>every one of them has a "
          "legitimate use</b>, and a rule banning friction would forbid "
          "confirming a deletion."]),

  ("h1", "4 &nbsp; The professional position"),
  ("callout", "You will be asked to build these, and the useful response is "
              "a measurement",
   ["<b>The request usually arrives as a metric rather than as a "
    "design:</b> <b>'increase signups', 'reduce churn', 'improve "
    "consent rates'</b> — and <b>the manipulative implementation is "
    "frequently the cheapest available way to move it</b>, which is why "
    "it gets built.",
    "<b>So the effective counter is measuring the cost rather than "
    "objecting on principle:</b> <b>the support load, the refund and "
    "chargeback rate, the complaint rate, the app-store reviews, and the "
    "retention of users who felt tricked.</b>",
    "<b>Because manipulated conversions are worse conversions</b> "
    "— <b>a subscription somebody did not mean to start is "
    "cancelled, charged back, or complained about</b> — and <b>those "
    "costs land elsewhere in the organisation</b>, which is precisely why "
    "they are invisible to the person asking for the metric. <b>Making "
    "them visible is the intervention.</b>",
    "<b>And where the measurement does not win, say so plainly and "
    "let the decision be made explicitly</b> — <b>which is a much "
    "smaller thing than refusing and is usually available</b>: a recorded "
    "objection and a named decision-maker is a real outcome, and it is "
    "the one CSCE 701 Module 01 &sect;2's accepted-risk practice "
    "would recommend."]),
  ("ul", ["<b>Compare the effort required in the two "
          "directions</b> — signing up against cancelling, opting in "
          "against opting out, adding against removing — and count "
          "the steps for each.",
          "<b>Check the visual weight of the options</b>, and ask "
          "<b>whether the recommended one is recommended for the user's "
          "benefit</b> or for somebody else's (&sect;3's test).",
          "<b>Check what is preselected</b>, and <b>whether anybody "
          "chose it deliberately</b> or it is simply whatever the "
          "framework defaults to (Module 05 &sect;3) — both "
          "happen, and the second is fixable without an argument.",
          "<b>Apply the explainability test to each persuasive "
          "element</b> (&sect;3), one at a time rather than to the "
          "design as a whole.",
          "<b>And read the whole flow as somebody who wants to "
          "leave</b>, <b>which is the perspective nobody designs for</b> "
          "and which no other review covers. <b>Reading the flow as "
          "somebody who wants to leave is the review nobody runs</b> "
          "— and <b>it finds the obstruction patterns "
          "immediately</b>, because they were built on the assumption "
          "that nobody would look."]),
 ],
 "resources": [
   ("Brignull &mdash; Deceptive Patterns (free)",
    "https://www.deceptive.design/",
    "<b>&sect;1's catalogue</b> — the patterns named, with examples "
    "and the enforcement history."),
   ("Mathur et al. &mdash; Dark Patterns at Scale (free)",
    "https://arxiv.org/abs/1907.07032",
    "<b>&sect;1 measured</b> — an automated survey of eleven thousand "
    "shopping sites, with prevalence figures."),
   ("Thaler & Sunstein &mdash; Nudge, and its critics",
    "https://web.archive.org/web/20260923132501/https://yalebooks.yale.edu/book/9780300122237/nudge/",
    "<b>&sect;3's difficult cases</b> — the case for benign "
    "paternalism, and the objections to it. Library copy."),
   ("Susser, Roessler & Nissenbaum &mdash; Online Manipulation (free)",
    "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3306006",
    "<b>&sect;3's distinction, argued properly</b> — manipulation as "
    "bypassing rather than engaging deliberation."),
 ],
 "exercises": [
   "<b>Find each of the seven patterns</b> in software you use.",
   "<b>For each, name the mechanism</b> and the earlier module it came "
   "from.",
   "<b>Count the steps to cancel</b> three subscriptions you hold.",
   "<b>Compare against the steps to start them.</b>",
   "<b>Find a preselected checkbox</b> and determine whether anybody "
   "chose it.",
   "<b>Apply the explainability test</b> to five persuasive elements in "
   "your own work.",
   "<b>Find a legitimate use of obstruction</b> and justify it.",
   "<b>Estimate the support cost</b> of one manipulative pattern you "
   "have seen.",
   "<b>Read one of your own flows as somebody trying to leave</b>, and "
   "record what you find.",
   "<b>Write the measurement</b> you would bring to a request for a "
   "manipulative pattern.",
 ],
 "selfcheck": [
   "Name seven patterns and the mechanism each exploits.",
   "Where did each mechanism appear earlier in the course?",
   "Why is this knowledge dual-use, and what follows?",
   "Why is effort asymmetry the one needing no deception?",
   "State the persuasion/manipulation distinction and the operative "
   "test.",
   "Why is the test usable in a design review?",
   "Give four genuinely difficult cases.",
   "Why is a list of forbidden techniques not the answer?",
   "What is the effective professional response, and why does it "
   "work?",
   "Give five review checks, and the one nobody runs.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Claiming Usability Honestly",
 "subtitle": "What a study establishes.",
 "question": "You tested it. What do you know?",
 "outcomes": [
     "State what each method establishes.",
     "Identify the standard overclaims.",
     "Write a defensible usability claim.",
     "Place this course relative to CSCE 679 and CSCE 632.",
     "State a proportionate practice for real design work.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What each method establishes",
   "blurb": "Precisely, and the differences matter."},

  {"t": "table", "kicker": "Methods", "title": "What each method supports",
   "header": ["Method", "Establishes", "Does not establish"],
   "widths": [2.6, 4.2, 5.1],
   "rows": [
     ["<b>Heuristic review</b>", "<b>These principles are violated here</b>", "<b>That users will struggle (M05 §4)</b>"],
     ["<b>Usability test (n=5)</b>", "<b>These problems exist, and the mechanism</b>", "<b>Any rate or any comparison (M07 §2)</b>"],
     ["<b>Experiment</b>", "<b>A measured difference, in these conditions</b>", "<b>Long-term behaviour (M06 §4)</b>"],
     ["<b>Interview</b>", "<b>What they report and how they explain it</b>", "<b>What they actually do (M09 §3)</b>"],
     ["<b>Observation</b>", "<b>What they do, and the context</b>", "<b>Frequencies in a population</b>"],
     ["<b>Analytics</b>", "<b>What happened at scale</b>", "<b>Why — which needs M09</b>"],
   ],
   "footnote": "<b>The last two rows are complementary rather than "
               "redundant</b> — analytics tells you what and "
               "qualitative work tells you why, and neither substitutes "
               "for the other.",
   "note": "The does-not-establish column is the module."},

  {"t": "callout", "title": "“We tested it” is not a claim until you say which method and what it showed",
   "kind": "The substitution to refuse",
   "body": ["<b>Each row above supports a narrow, specific claim</b> "
            "— and <b>'we tested it and users liked it' names no "
            "method, no participants, and no measure.</b>",
            "<b>And 'users liked it' is the weakest possible "
            "finding</b>, because <b>a participant in a room will say "
            "they liked almost anything</b> "
            "(Module 06 §4).",
            "<b>So the honest form names the method, the number of "
            "participants, the tasks, and what happened</b> — four "
            "clauses, all cheap to supply.",
            "<b>Which is the same correction as CSCE 701 §13, "
            "CSCE 713 §13, and CSCE 670 §13 "
            "make</b> — <b>substituting an activity for a "
            "finding</b>, which this program has now identified in four "
            "different subjects."]},

  {"t": "section", "label": "Part 2", "title": "Overclaims and defensible claims",
   "blurb": "Both lists."},

  {"t": "table", "kicker": "Overclaims", "title": "The standard overclaims, corrected",
   "header": ["Claim", "Correction"],
   "widths": [4.4, 6.6],
   "rows": [
     ["<b>'Users liked it'</b>", "<b>How many, asked how, and compared to what?</b>"],
     ["<b>'It is intuitive'</b>", "<b>To whom? Intuition is prior exposure (M04 §2)</b>"],
     ["<b>'80% of users prefer it'</b>", "<b>From five participants? That is four people</b>"],
     ["<b>'The redesign improved usability'</b>", "<b>On which tasks, measured how, and what got worse?</b>"],
     ["<b>'It is accessible'</b>", "<b>Tested with whom, against what? (CSCE 632)</b>"],
     ["<b>'Best practice says'</b>", "<b>Which study, in which context, with what effect size?</b>"],
   ],
   "footnote": "<b>'It is intuitive' is the one to attack</b> — "
               "<b>intuition is prior exposure</b>, so the claim is "
               "always relative to a population and is usually relative "
               "to the designer's own.",
   "note": "The intuition correction is the most generally useful "
           "one."},

  {"t": "bullets", "kicker": "Honest", "title": "Claims you can defend",
   "items": [
     "<b>'Five participants attempted three tasks; four failed "
     "task two at the same step, which we attributed to a missing "
     "signifier.'</b> <b>Method, n, task, mechanism.</b>",
     "",
     "<b>'After the change, five new participants completed task "
     "two; one took notably longer and we do not know "
     "why.'</b> <b>Including the unexplained "
     "case.</b>",
     "",
     "<b>'In a counterbalanced within-subject study with twelve "
     "participants, design B was 18% faster (95% CI 4–32%) on "
     "this task.'</b>",
     "",
     "<b>'Our participants were twelve colleagues; our users are "
     "not twelve colleagues.'</b>",
     "",
     "<b>And: 'we have not tested with screen reader users, on "
     "mobile, or over more than one session.'</b>",
   ],
   "footnote": "<b>The last one is the limitation statement</b>, and "
               "it is Project 2's hardest-graded requirement — "
               "because it requires knowing what your method cannot "
               "reach."},

  {"t": "section", "label": "Part 3", "title": "The semester",
   "blurb": "Three courses about the person at the other end."},

  {"t": "table", "kicker": "Semester 11", "title": "Where this course sits",
   "header": ["Course", "Covers", "Its central correction"],
   "widths": [2.3, 3.6, 5.6],
   "rows": [
     ["<b>CSCE 671</b>", "<b>Interaction</b>", "<b>Your judgement of your own design is unreliable</b>"],
     ["<b>CSCE 679</b>", "<b>Visual representation</b>", "<b>The encoding determines what can be read</b>"],
     ["<b>CSCE 632</b>", "<b>Access</b>", "<b>Designing for a constraint improves it for everyone</b>"],
   ],
   "footnote": "<b>All three correct the same error:</b> <b>designing "
               "for an imagined user who resembles the designer</b> "
               "— and all three answer it with observation rather "
               "than with argument.",
   "note": "The shared correction is the semester's conclusion."},

  {"t": "section", "label": "Part 4", "title": "A proportionate practice",
   "blurb": "What to actually do."},

  {"t": "bullets", "kicker": "Practice", "title": "In order of return",
   "items": [
     "<b>1 · Watch five people</b> "
     "(Module 07) — <b>which costs a day and is the "
     "only reliable information available</b>, and almost nobody "
     "does it.",
     "",
     "<b>2 · Fix the errors mechanically</b> "
     "(Module 01 §1's six) — attributing before "
     "proposing.",
     "",
     "<b>3 · Check the defaults, the error messages, and the "
     "feedback placement</b> (Modules 05, 10, 02) — all cheap, "
     "all high-return.",
     "",
     "<b>4 · Run the accessibility review</b> "
     "(CSCE 632) — <b>which finds problems the five "
     "participants could not have.</b>",
     "",
     "<b>5 · And only then measure a difference</b> "
     "(Module 08), which is expensive and answers a narrower "
     "question.",
   ],
   "footnote": "<b>Step 1 before everything is the ordering that "
               "matters</b> — and it is the step that gets deferred "
               "because it is socially uncomfortable rather than because "
               "it is expensive."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can diagnose an interface failure "
            "mechanically</b> — a missing signifier, a perceptual "
            "failure, an attention failure, a memory demand, a model "
            "mismatch — rather than describing it as "
            "confusing.",
            "<b>You can watch five people without helping, and "
            "analyse what you saw</b> — <b>which is the skill that "
            "makes the rest of it evidence rather than "
            "argument.</b>",
            "<b>And you know that this applies to the interfaces you "
            "build for programmers</b> (Module 10), <b>which is most of "
            "what you will actually design.</b>",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it means naming the "
            "method, the participants, and the tasks</b> — because "
            "<b>'it is intuitive' names your own prior exposure and "
            "nothing else.</b>"]},
 ],
 "takeaways": [
   "Each method supports a narrow, specific claim, and the "
   "does-not-establish column is the content.",
   "Analytics tells you what happened and qualitative work tells you why; "
   "neither substitutes for the other.",
   "'Users liked it' is the weakest possible finding, because a "
   "participant in a room will say they liked almost anything.",
   "'It is intuitive' means 'intuitive to somebody with my prior "
   "exposure', which is usually the designer's own.",
   "All three Semester 11 courses correct the same error: designing for an "
   "imagined user who resembles the designer.",
   "Watching five people is deferred because it is socially uncomfortable "
   "rather than because it is expensive.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What each method establishes"),
  ("table", ["Method", "What it establishes", "What it does not"],
   [["<b>Heuristic review</b>",
     "<b>That these principles are violated in these places.</b>",
     "<b>That users will actually struggle</b> (Module 05 "
     "&sect;4)."],
    ["<b>Usability test, n = 5</b>",
     "<b>That these problems exist, and the mechanism behind each.</b>",
     "<b>Any rate, and any comparison between designs</b> "
     "(Module 07 &sect;2)."],
    ["<b>Controlled experiment</b>",
     "<b>A measured difference, under these conditions, with this "
     "interval.</b>",
     "<b>Long-term behaviour, or whether the novelty wears off</b> "
     "(Module 06 &sect;4, Module 08 &sect;4)."],
    ["<b>Interview</b>",
     "<b>What they report, and how they explain their own "
     "behaviour.</b>",
     "<b>What they actually do</b> (Module 09 &sect;3)."],
    ["<b>Observation</b>",
     "<b>What they do, and the context it happens in.</b>",
     "<b>Frequencies in a population.</b>"],
    ["<b>Analytics</b>",
     "<b>What happened, at scale, across real users.</b>",
     "<b>Why it happened</b> — which needs Module 09."]],
   [0.20, 0.36, 0.44]),
  ("p", "<b>The last two rows are complementary rather than "
        "redundant</b> — <b>analytics tells you <i>what</i> and "
        "qualitative work tells you <i>why</i></b>, and <b>neither "
        "substitutes for the other</b>: a drop-off at step three is a "
        "finding with no explanation, and five observed sessions explain a "
        "mechanism with no magnitude. <b>The does-not-establish column is "
        "this module's content</b>, and it is the one usually omitted from "
        "a methods summary."),
  ("callout", "“We tested it” is not a claim until you say which "
              "method and what it showed",
   ["<b>Each row above supports a narrow and specific claim</b> — "
    "and <b>'we tested it and users liked it' names no method, no number "
    "of participants, no tasks, and no measure</b>, which makes it "
    "unassessable.",
    "<b>And 'users liked it' is the weakest possible finding</b> in "
    "any case, because <b>a participant in a room with the designer will "
    "say they liked almost anything</b> (Module 06 &sect;4's "
    "expressed-interest problem, and Module 08 &sect;4's demand "
    "characteristics).",
    "<b>So the honest form names the method, the number of "
    "participants, the tasks, and what actually happened</b> — "
    "<b>four clauses, all of them cheap to supply</b> and all of them "
    "making the claim checkable.",
    "<b>Which is the same correction that CSCE 701 Module 13, "
    "CSCE 713 Module 13, and CSCE 670 Module 13 all make</b> "
    "— <b>substituting an activity for a finding</b> — and "
    "<b>this program has now identified it in four different "
    "subjects</b>, which suggests it is the general failure rather than a "
    "disciplinary quirk."]),

  ("h1", "2 &nbsp; Overclaims, and defensible claims"),
  ("table", ["The claim", "The correction"],
   [["<b>'Users liked it.'</b>",
     "<b>How many users, asked how, and compared against what?</b> And "
     "liking is not usability."],
    ["<b>'It is intuitive.'</b>",
     "<b>Intuitive to whom?</b> <b>Intuition is prior exposure</b> "
     "(Module 04 &sect;2) — see the note."],
    ["<b>'80% of users prefer it.'</b>",
     "<b>From five participants? That is four people</b>, and the "
     "percentage implies a precision the sample cannot carry."],
    ["<b>'The redesign improved usability.'</b>",
     "<b>On which tasks, measured how, and what got worse?</b> "
     "(Project 2's regression requirement.)"],
    ["<b>'It is accessible.'</b>",
     "<b>Tested with whom, against which standard, with what assistive "
     "technology?</b> (CSCE 632.)"],
    ["<b>'Best practice says&hellip;'</b>",
     "<b>Which study, in which context, with what effect size?</b> A "
     "great deal of 'best practice' is a single old study."]],
   [0.34, 0.66]),
  ("p", "<b>'It is intuitive' is the one to attack</b> — "
        "<b>intuition is prior exposure</b> (Module 04 &sect;2's "
        "conventions), <b>so the claim is always relative to a population "
        "and is usually relative to the designer's own</b>. Nothing is "
        "intuitive in the abstract: a scroll bar, a hamburger menu, and a "
        "pinch gesture all had to be learned. <b>The intuition correction "
        "is the most generally useful one in the table</b>, because the "
        "word is used constantly and is never qualified."),
  ("ul", ["<b>'Five participants attempted three tasks; four of them "
          "failed task two at the same step, which we attributed to a "
          "missing signifier on the filter control.'</b> <b>Method, "
          "number, task, step, and mechanism</b> — all five "
          "checkable.",
          "<b>'After the change, five new participants completed task "
          "two; one took notably longer and we do not know why.'</b> "
          "<b>Including the unexplained case</b>, which is what "
          "distinguishes a report from a success story.",
          "<b>'In a counterbalanced within-subject study with twelve "
          "participants, design B was 18% faster on this task (95% "
          "confidence interval 4 to 32%).'</b> <b>Design, n, effect "
          "size, and interval</b> (Module 08 &sect;3).",
          "<b>'Our participants were twelve colleagues; our users are "
          "not twelve colleagues.'</b> <b>The sampling limitation, "
          "stated rather than implied</b> (Module 08 &sect;4).",
          "<b>And: 'we have not tested with screen reader users, on "
          "mobile, or across more than one session.'</b> <b>The last one "
          "is the limitation statement</b>, and <b>it is Project 2's "
          "hardest-graded requirement</b> — <b>because it requires "
          "knowing what your method structurally cannot reach</b>, which "
          "is &sect;1's right-hand column applied to your own work."]),

  ("break",),
  ("h1", "3 &nbsp; The semester"),
  ("table", ["Course", "What it covers", "Its central correction"],
   [["<b>CSCE 671 (this one)</b>",
     "<b>Interaction — how people use what you built.</b>",
     "<b>Your judgement of your own design is unreliable</b>, so watch "
     "somebody (Module 01 &sect;2)."],
    ["<b>CSCE 679</b>",
     "<b>Visual representation of data.</b>",
     "<b>The encoding determines what can be read from a "
     "picture</b> — so the choice is not aesthetic."],
    ["<b>CSCE 632</b>", "<b>Access — who can use it at all.</b>",
     "<b>Designing for a constraint improves the design for "
     "everybody</b>, which is a quality argument rather than a fairness "
     "one."]],
   [0.22, 0.30, 0.48]),
  ("p", "<b>All three courses correct the same error:</b> <b>designing "
        "for an imagined user who resembles the designer</b> — in "
        "their knowledge (671), in their perception (679), and in their "
        "capabilities (632). <b>And all three answer it the same way, "
        "with observation rather than with argument</b>: watch somebody, "
        "test the encoding, try it with the assistive technology. "
        "<b>The shared correction is the semester's conclusion</b>, and "
        "it is more durable than any individual principle in it."),

  ("h1", "4 &nbsp; A proportionate practice"),
  ("ul", ["<b>1 &middot; Watch five people</b> (Module 07) — "
          "<b>which costs a day, needs no equipment, and is the only "
          "reliable source of information in this subject</b> "
          "(Module 01 &sect;2) — <b>and almost nobody does "
          "it.</b>",
          "<b>2 &middot; Fix the failures mechanically</b>, "
          "attributing each to one of Module 01 &sect;1's six "
          "mechanisms <b>before proposing anything</b>, so that each "
          "proposal is testable.",
          "<b>3 &middot; Check the defaults, the error messages, and "
          "the feedback placement</b> (Modules 05, 10, and 02) — "
          "<b>all three cheap, all three high-return</b>, and all three "
          "fixable without a redesign.",
          "<b>4 &middot; Run the accessibility review</b> "
          "(CSCE 632) — <b>which finds problems the five "
          "participants structurally could not have found</b>, and which "
          "is the single largest gap in a five-participant study.",
          "<b>5 &middot; And only then measure a difference</b> "
          "(Module 08), <b>which is expensive and answers a much "
          "narrower question</b> than the earlier steps do. <b>Step 1 "
          "before everything is the ordering that matters</b> — and "
          "<b>it is the step that gets deferred because it is socially "
          "uncomfortable rather than because it is expensive</b>, which "
          "is worth naming so that the discomfort can be acknowledged "
          "rather than rationalised."]),
  ("callout", "Where this course leaves you",
   ["<b>You can diagnose an interface failure mechanically</b> — a "
    "missing signifier, absent feedback, a perceptual failure, an "
    "attention failure, a memory demand, or a model mismatch — "
    "<b>rather than describing it as 'confusing'</b>, which is the "
    "difference between a finding and an impression.",
    "<b>You can watch five people without helping, and analyse what "
    "you saw into mechanisms and severities</b> — <b>which is the "
    "skill that makes the rest of the course evidence rather than "
    "argument</b> (Module 01 &sect;2's governing constraint).",
    "<b>And you know that all of this applies to the interfaces you "
    "build for other programmers</b> (Module 10) — <b>APIs, error "
    "messages, configuration, and tooling — which is most of what "
    "you will actually design</b> in a career in this field.",
    "<b>The closing rule is the program's, unchanged across thirty-one "
    "courses:</b> <b>state what you measured, state what you assumed, "
    "and never claim more than you established.</b> <b>In this subject "
    "it means naming the method, the participants, and the tasks</b> "
    "— because <b>'it is intuitive' names your own prior exposure "
    "and nothing else at all.</b>"]),
 ],
 "resources": [
   ("Lazar, Feng & Hochheiser, the reporting chapters",
    "https://www.elsevier.com/books/research-methods-in-human-computer-interaction/lazar/978-0-12-805390-4",
    "<b>&sect;1 and &sect;2</b> — what each method supports, and how to "
    "report it. Library copy."),
   ("Cockton &mdash; on the limits of usability claims (free via the "
    "CHI proceedings)",
    "https://dl.acm.org/conference/chi",
    "<b>&sect;2's overclaims, in the field's own literature</b> — and "
    "the limitations sections of CHI papers are the model to "
    "follow."),
   ("Greenberg & Buxton &mdash; Usability Evaluation Considered "
    "Harmful (free)",
    "https://dl.acm.org/doi/10.1145/1357054.1357074",
    "<b>&sect;1's first two rows argued sharply</b> — when evaluation "
    "is the wrong activity, which is a useful corrective."),
   ("Dragicevic &mdash; Fair Statistical Communication in HCI (free)",
    "https://hal.science/hal-01377894",
    "<b>&sect;2's third claim form</b> — intervals rather than "
    "significance, and why."),
 ],
 "exercises": [
   "<b>For each of the six methods</b>, write what it establishes and "
   "what it does not.",
   "<b>Find a usability claim</b> made about a product and assess it "
   "against §2's table.",
   "<b>Find 'intuitive' used without qualification</b> and supply the "
   "missing population.",
   "<b>Rewrite one of your own findings</b> in §2's claim form.",
   "<b>Write your limitation statement</b> for Project 2.",
   "<b>Name the correction</b> each of the three Semester 11 courses "
   "makes.",
   "<b>Audit your own practice</b> against §4's five steps.",
   "<b>Determine why step 1 has not happened</b>, honestly.",
   "<b>Revisit Module 01's last exercise</b> and compare.",
   "<b>Project 2 is now due.</b> Submit the redesign, the before and "
   "after sessions with different participants, the per-participant "
   "results, the qualitative account, the accessibility review, and the "
   "limitation statement.",
 ],
 "selfcheck": [
   "For six methods, state what each establishes and does not.",
   "Why are analytics and qualitative work complementary?",
   "Why is 'we tested it' not a claim?",
   "Why is 'users liked it' the weakest finding?",
   "Give six overclaims and the correction to each.",
   "Why is 'intuitive' the one to attack?",
   "Give four defensible claim forms.",
   "What error do all three Semester 11 courses correct, and how?",
   "Give the five-step practice in order.",
   "Why does step 1 get deferred?",
 ],
},

]
