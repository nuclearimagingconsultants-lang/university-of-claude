# -*- coding: utf-8 -*-
"""CSCE 671 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Perception",
 "subtitle": "What people see, which is not what is on the screen.",
 "question": "Why did they not notice it?",
 "outcomes": [
     "Explain the grouping principles and apply them to a "
     "layout.",
     "Explain contrast, colour, and their limits.",
     "Explain preattentive features and pop-out.",
     "Explain change blindness and its design consequences.",
     "Predict what will and will not be noticed.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Grouping",
   "blurb": "The visual system groups before you decide anything."},

  {"t": "code", "kicker": "Grouping", "title": "The principles, in rough order of strength",
   "lang": "text", "code": """
  PROXIMITY     things close together are one group.
                The strongest of these by a wide
                margin, and the cheapest to use.

  COMMON REGION a shared enclosure or background
                groups, and it overrides proximity.

  SIMILARITY    same colour, shape, or size groups.
                Weaker than proximity, and useful
                across distance.

  CONNECTEDNESS a visible link groups very strongly,
                and overrides similarity.

  CONTINUITY    aligned things read as a sequence,
                which is why alignment matters more
                than it looks.

  CLOSURE       the eye completes an implied shape.

  AND THE PRACTICAL CONSEQUENCE: if your spacing
  contradicts your intended grouping, the spacing
  wins. A label closer to the wrong field is attached
  to the wrong field, whatever the markup says.
""",
   "caption": "<b>If the spacing contradicts the intended grouping, "
              "the spacing wins</b> — which makes whitespace a "
              "functional rather than an aesthetic decision.",
   "note": "The spacing-wins rule is the module's most immediately "
           "usable finding."},

  {"t": "callout", "title": "Which makes whitespace structural rather than decorative",
   "kind": "The consequence worth internalising",
   "body": ["<b>Grouping by proximity is automatic and "
            "pre-conscious</b> — the user does not decide to group "
            "things, and cannot decide not to.",
            "<b>So the layout communicates a structure whether or not "
            "you intended one</b>, and <b>the commonest form-design "
            "defect is a label equidistant between two fields</b>, which "
            "attaches to neither reliably.",
            "<b>And the fix is free:</b> <b>reduce the space between "
            "related items and increase it between groups</b>, which "
            "costs nothing and requires no new elements.",
            "<b>Which is why a cluttered interface is not merely ugly "
            "but harder to use</b> — <b>uniform spacing conveys no "
            "structure</b>, so the user has to construct it from the "
            "content, which costs attention "
            "(Module 03)."]},

  {"t": "section", "label": "Part 2", "title": "Contrast and colour",
   "blurb": "Including the limits people design past."},

  {"t": "bullets", "kicker": "Colour", "title": "What colour can and cannot do",
   "items": [
     "<b>Colour is excellent for categorical "
     "distinction</b> — up to about five to seven categories, "
     "after which people cannot keep the mapping "
     "(Module 03 §2).",
     "",
     "<b>And poor for ordered quantities</b> unless the scale is "
     "designed for it — which is CSCE 679 §04's whole "
     "subject.",
     "",
     "<b>Luminance contrast carries the structure</b>, and hue "
     "does not — <b>which is why a design must work in "
     "greyscale</b> before colour is added.",
     "",
     "<b>And a substantial minority of people cannot distinguish "
     "some hue pairs</b> — so <b>colour must never be the only "
     "channel</b> (CSCE 632 §03).",
     "",
     "<b>Which makes 'redundant encoding' the rule:</b> colour "
     "<i>and</i> shape, colour <i>and</i> position, colour "
     "<i>and</i> a label.",
   ],
   "footnote": "<b>'Must work in greyscale' is the quickest available "
               "test</b> — and it catches the colour-only encoding, "
               "the insufficient contrast, and the "
               "hue-carrying-the-structure error at once."},

  {"t": "section", "label": "Part 3", "title": "Preattentive features",
   "blurb": "What is found without searching."},

  {"t": "callout", "title": "A few visual features are processed in parallel, so one item differing in them is found instantly",
   "kind": "The property that makes pop-out possible",
   "body": ["<b>Colour, size, orientation, motion, and a few "
            "others</b> — <b>a single item differing in one of these "
            "is located in constant time</b>, regardless of how many "
            "distractors there are.",
            "<b>Which is the basis of every effective visual "
            "highlight</b> — and <b>it only works for one "
            "feature.</b>",
            "<b>Because a <i>conjunction</i> of features requires "
            "serial search:</b> <b>finding the one red circle among red "
            "squares and blue circles takes time proportional to the "
            "number of items</b>, which is a measured and reliable "
            "result.",
            "<b>So the design rule is: highlight along exactly one "
            "dimension</b> — <b>and the more things you highlight, "
            "the less any of them pops out</b>, which is why an interface "
            "where everything is emphasised has no emphasis at all."]},

  {"t": "bullets", "kicker": "Application", "title": "And how to use it",
   "items": [
     "<b>Pick one feature for your most important "
     "distinction</b>, and do not reuse it for anything "
     "else.",
     "",
     "<b>Motion is the strongest and the most "
     "expensive</b> — it captures attention involuntarily, which "
     "is why an animated advertisement works and why "
     "it is intolerable.",
     "",
     "<b>And count your emphasis.</b> <b>If more than about three "
     "things on a screen are emphasised, none of them is</b> — "
     "which is a countable defect.",
     "",
     "<b>Reserve the strongest channel for the rarest and most "
     "important event</b>, which means errors rather than "
     "branding.",
     "",
     "<b>And test it by looking away and back</b> — whatever "
     "you see first is what is emphasised.",
   ],
   "footnote": "<b>'Look away and back' is a five-second test</b> "
               "— and what you see first is what the design actually "
               "emphasises, regardless of intent."},

  {"t": "section", "label": "Part 4", "title": "Change blindness",
   "blurb": "The finding with the largest design consequence."},

  {"t": "callout", "title": "People reliably fail to notice large changes outside their focus of attention",
   "kind": "And it is much stronger than intuition suggests",
   "body": ["<b>A substantial change to a scene, made during a "
            "saccade or a brief interruption, goes unnoticed by most "
            "observers</b> — including changes to the thing they were "
            "nominally looking for.",
            "<b>So a status message appearing in the corner is not "
            "feedback</b> — <b>the user was looking at the button "
            "they clicked, and the change happened elsewhere</b>, which "
            "is Module 01 §1's evaluation gap arriving "
            "perceptually.",
            "<b>Which means feedback has to appear where the attention "
            "already is</b> — at the point of interaction — "
            "<b>or move, which overrides the "
            "blindness.</b>",
            "<b>And it is why 'we showed a notification' is not a "
            "defence</b>: <b>showing is not the same as being "
            "perceived</b>, and the difference is measurable."]},

  {"t": "bullets", "kicker": "Prediction", "title": "Predicting what will be noticed",
   "items": [
     "<b>At the point of interaction, or moving:</b> noticed "
     "reliably.",
     "",
     "<b>In the periphery, static, and not differing "
     "preattentively:</b> <b>reliably missed</b>, however large.",
     "",
     "<b>In a position where something always appears:</b> <b>missed, "
     "because it is habituated</b> — which is why banner-position "
     "content is invisible.",
     "",
     "<b>And during a transition or a page change:</b> missed, "
     "because the change blindness window is exactly "
     "then.",
     "",
     "<b>So place feedback at the cursor, the field, or the "
     "control</b> — which is almost always possible and almost "
     "never done.",
   ],
   "footnote": "<b>Habituation to position is why anything in the "
               "advertising position is unseen</b> — including "
               "genuine content you put there, which is a mistake worth "
               "avoiding."},
 ],
 "takeaways": [
   "If the spacing contradicts the intended grouping, the spacing wins — "
   "which makes whitespace a functional decision.",
   "Uniform spacing conveys no structure, so a cluttered interface is "
   "harder to use rather than merely uglier.",
   "Luminance contrast carries the structure and hue does not, so a design "
   "must work in greyscale.",
   "A single differing feature is found in constant time and a conjunction "
   "requires serial search, so highlight along exactly one dimension.",
   "If more than about three things on a screen are emphasised, none of "
   "them is — which is a countable defect.",
   "People reliably miss large changes outside their attention, so a "
   "corner status message is not feedback.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Grouping"),
  ("code", """PROXIMITY     things close together are one group.
              The strongest of these by a wide margin,
              and the cheapest to use.

COMMON REGION a shared enclosure or background
              groups, and it overrides proximity.

SIMILARITY    same colour, shape, or size groups.
              Weaker than proximity, and useful
              across distance where proximity cannot
              reach.

CONNECTEDNESS a visible link groups very strongly,
              and overrides similarity.

CONTINUITY    aligned things read as a sequence,
              which is why alignment matters more
              than it appears to.

CLOSURE       the eye completes an implied shape, so
              a partial border still encloses.

AND THE PRACTICAL CONSEQUENCE: if your spacing
contradicts your intended grouping, the spacing wins.
A label closer to the wrong field is attached to the
wrong field, whatever the markup says."""),
  ("p", "<b>If the spacing contradicts the intended grouping, the "
        "spacing wins</b> — <b>which makes whitespace a functional "
        "rather than an aesthetic decision</b>, and is <b>the module's "
        "most immediately usable finding</b>. The ordering by strength "
        "matters too: when two principles conflict, the stronger one "
        "determines what the user perceives, which is why a shared "
        "background can hold together items that are not particularly "
        "close."),
  ("callout", "Which makes whitespace structural rather than decorative",
   ["<b>Grouping by proximity is automatic and pre-conscious</b> "
    "— <b>the user does not decide to group things, and cannot "
    "decide not to</b>, which means the layout is communicating whether "
    "or not you intended it to.",
    "<b>So the layout communicates a structure whether or not you "
    "designed one</b>, and <b>the commonest form-design defect is a "
    "label placed equidistant between two fields</b>, which <b>attaches "
    "to neither reliably</b> and produces errors that look like "
    "carelessness.",
    "<b>And the fix is free:</b> <b>reduce the space between related "
    "items and increase it between groups</b> — which costs nothing, "
    "requires no new elements, adds no visual weight, and is the "
    "highest-return edit available in most layouts.",
    "<b>Which is why a cluttered interface is not merely ugly but "
    "genuinely harder to use</b> — <b>uniform spacing conveys no "
    "structure at all</b>, so <b>the user has to construct the structure "
    "from the content</b>, which costs attention they could have spent on "
    "the task (Module 03 &sect;1)."]),

  ("h1", "2 &nbsp; Contrast and colour"),
  ("ul", ["<b>Colour is excellent for categorical distinction</b> "
          "— <b>up to about five to seven categories, after which "
          "people cannot hold the mapping</b> (Module 03 &sect;2's "
          "working memory limit) and have to consult the legend for every "
          "item, which defeats the purpose.",
          "<b>And it is poor for ordered quantities</b> unless the "
          "scale is specifically designed for perceptual uniformity "
          "— <b>which is CSCE 679 Module 04's whole "
          "subject</b>, and where the default rainbow scale does real "
          "damage.",
          "<b>Luminance contrast carries the structure, and hue does "
          "not</b> — the visual system's spatial acuity is largely "
          "driven by luminance — <b>which is why a design must work "
          "in greyscale</b> before any colour is added to it.",
          "<b>And a substantial minority of people cannot distinguish "
          "certain hue pairs</b>, red and green most commonly — so "
          "<b>colour must never be the only channel carrying "
          "information</b> (CSCE 632 Module 03's requirement, "
          "arriving here as a perceptual fact rather than a compliance "
          "one).",
          "<b>Which makes redundant encoding the rule:</b> colour "
          "<i>and</i> shape, colour <i>and</i> position, colour "
          "<i>and</i> a text label. <b>'Must work in greyscale' is the "
          "quickest available test</b>, and <b>it catches the "
          "colour-only encoding, the insufficient contrast, and the "
          "hue-carrying-the-structure error all at once</b> — which "
          "makes it worth running on every screen."]),

  ("break",),
  ("h1", "3 &nbsp; Preattentive features"),
  ("callout", "A few visual features are processed in parallel, so one item "
              "differing in them is found instantly",
   ["<b>Colour, size, orientation, motion, curvature, and a handful of "
    "others</b> — <b>a single item differing in one of these is "
    "located in approximately constant time</b>, <b>regardless of how "
    "many distractors are present</b>, which is a striking and "
    "well-replicated result.",
    "<b>Which is the basis of every effective visual highlight</b> in "
    "an interface or a chart — and critically, <b>it only works for "
    "one feature at a time.</b>",
    "<b>Because a <i>conjunction</i> of features requires serial "
    "search:</b> <b>finding the one red circle among red squares and "
    "blue circles takes time proportional to the number of items</b>, "
    "because no single channel distinguishes the target — which is a "
    "measured and reliable result and is the reason the one-dimension "
    "rule holds.",
    "<b>So the design rule is: highlight along exactly one "
    "dimension</b> — <b>and the more things you highlight, the less "
    "any of them pops out</b>, <b>which is why an interface where "
    "everything is emphasised has no emphasis at all</b> and is a "
    "countable rather than a stylistic defect."]),
  ("ul", ["<b>Pick one feature for your single most important "
          "distinction</b>, and <b>do not reuse that feature for "
          "anything else</b> — which is a discipline about the whole "
          "screen rather than about one element.",
          "<b>Motion is the strongest channel and the most "
          "expensive</b> — <b>it captures attention "
          "involuntarily</b>, which is simultaneously <b>why an animated "
          "advertisement works and why it is intolerable</b>, and is why "
          "it should be reserved for genuinely urgent things.",
          "<b>And count your emphasis.</b> <b>If more than about "
          "three things on a screen are emphasised, none of them is</b> "
          "— which makes this <b>a countable defect</b> you can check "
          "in a design review without any argument about taste.",
          "<b>Reserve the strongest available channel for the rarest "
          "and most important event</b>, <b>which means errors and "
          "destructive confirmations rather than branding and "
          "promotion</b> — a prioritisation that is frequently "
          "decided by whoever owns the page.",
          "<b>And test it by looking away and back</b> — "
          "<b>whatever you see first is what is actually "
          "emphasised</b>. <b>'Look away and back' is a five-second "
          "test</b>, and <b>what you see first is what the design "
          "emphasises regardless of intent</b>, which makes it a fast and "
          "unarguable check."]),

  ("h1", "4 &nbsp; Change blindness"),
  ("callout", "People reliably fail to notice large changes outside their "
              "focus of attention",
   ["<b>A substantial change to a scene, made during a saccade or a "
    "brief interruption, goes unnoticed by most observers</b> — "
    "<b>including changes to the very object they were nominally looking "
    "for</b>, which is the finding that makes the effect so much stronger "
    "than intuition suggests.",
    "<b>So a status message appearing in a corner is not "
    "feedback</b> — <b>the user was looking at the button they just "
    "clicked, and the change happened somewhere else entirely</b> — "
    "<b>which is Module 01 &sect;1's evaluation gap arriving as a "
    "perceptual mechanism</b> rather than as a design oversight.",
    "<b>Which means feedback has to appear where the attention "
    "already is</b> — at the point of interaction, on the control "
    "that was operated, at the cursor — <b>or it has to move, which "
    "overrides the blindness</b> because motion is preattentive "
    "(&sect;3).",
    "<b>And it is why 'we showed a notification' is not a "
    "defence</b>: <b>showing is not the same as being perceived</b>, and "
    "<b>the difference is measurable</b> — which is "
    "Module 01 &sect;2's non-reading argument in a perceptual "
    "register."]),
  ("ul", ["<b>At the point of interaction, or moving:</b> noticed "
          "reliably, which is the only combination you can depend on.",
          "<b>In the periphery, static, and not differing in a "
          "preattentive feature:</b> <b>reliably missed, however large "
          "it is</b> — size is not sufficient, which surprises "
          "people.",
          "<b>In a position where something always appears:</b> "
          "<b>missed, because the position has been habituated</b> — "
          "<b>which is why anything in a banner position is "
          "invisible</b>, and is a mistake worth avoiding when you put "
          "genuine content there.",
          "<b>And during a transition or a page change:</b> missed, "
          "<b>because the change blindness window is exactly then</b> "
          "— so a message that appears as part of a navigation is the "
          "worst available timing.",
          "<b>So place feedback at the cursor, at the field, or on "
          "the control that was operated</b> — <b>which is almost "
          "always technically possible and almost never done</b>, because "
          "a global notification area is easier to build. <b>Habituation "
          "to position is why anything in the advertising position is "
          "unseen</b>, including the genuine content you put there "
          "hoping it would be read."]),
 ],
 "resources": [
   ("Johnson &mdash; Designing with the Mind in Mind, chapters 1 "
    "through 5",
    "https://www.elsevier.com/books/designing-with-the-mind-in-mind/johnson/978-0-12-818202-4",
    "<b>The whole module</b>, with the research cited and the effect "
    "sizes given. Library copy."),
   ("Ware &mdash; Information Visualization: Perception for Design",
    "https://www.elsevier.com/books/information-visualization/ware/978-0-12-812875-6",
    "<b>&sect;2 and &sect;3 in depth</b> — the standard reference, "
    "and CSCE 679's primary text as well. Library copy."),
   ("Healey &mdash; Perception in Visualization (free)",
    "https://www.csc2.ncsu.edu/faculty/healey/PP/",
    "<b>&sect;3's preattentive features, with interactive "
    "demonstrations</b> — the conjunction search effect is worth "
    "experiencing rather than reading about."),
   ("Simons & Levin &mdash; Change blindness (free)",
    "https://www.sciencedirect.com/science/article/abs/pii/S1364661397010801",
    "<b>&sect;4 in the original</b> — and the magnitude of the effect "
    "is the part that changes how you design feedback."),
 ],
 "exercises": [
   "<b>Take a form you did not design</b> and identify where spacing "
   "contradicts the intended grouping.",
   "<b>Fix it with spacing alone</b> and compare.",
   "<b>Convert three interfaces to greyscale</b> and report what stops "
   "working.",
   "<b>Find a colour-only encoding</b> in software you use.",
   "<b>Build a pop-out search task</b> and measure your own time against "
   "the number of distractors.",
   "<b>Build the conjunction version</b> and measure again.",
   "<b>Count the emphasised elements</b> on three screens of your own "
   "software.",
   "<b>Look away and back</b> from a screen you designed, and note what "
   "you saw first.",
   "<b>Find a status message you have missed</b> and say where it should "
   "have appeared.",
   "<b>Move one piece of feedback to the point of interaction</b> and "
   "test whether it is noticed.",
 ],
 "selfcheck": [
   "Name the six grouping principles and say which is strongest.",
   "What happens when spacing contradicts intended grouping?",
   "Why is a cluttered interface harder to use rather than merely "
   "uglier?",
   "What is colour good and bad for, and how many categories?",
   "Why must a design work in greyscale?",
   "What are preattentive features, and what happens with a "
   "conjunction?",
   "State the one-dimension rule and the countable defect.",
   "What is the five-second emphasis test?",
   "State change blindness and why a corner message is not feedback.",
   "Give four cases and whether each will be noticed.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Attention, Memory, and Error",
 "subtitle": "Hard limits, and the error rates they imply.",
 "question": "What can you require a person to hold in mind?",
 "outcomes": [
     "Explain attention as a limited resource with a "
     "switching cost.",
     "Explain working memory's limit and its design "
     "consequences.",
     "Explain recognition against recall.",
     "Classify errors as slips or mistakes and fix each "
     "accordingly.",
     "Predict error rates from design properties.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Attention",
   "blurb": "Single-channel, with a switching cost."},

  {"t": "callout", "title": "Attention is a single channel, and switching it costs time and accuracy",
   "kind": "The resource being spent",
   "body": ["<b>People do not multitask; they switch</b> — and "
            "<b>every switch costs reorientation time and raises the "
            "error rate</b>, which is measured and substantial.",
            "<b>So an interruption is expensive in a way that its "
            "duration understates:</b> <b>a five-second notification can "
            "cost far more than five seconds of task progress</b>, "
            "because the state has to be rebuilt.",
            "<b>And the cost scales with the interrupted task's "
            "complexity</b> — which means interruptions are worst "
            "exactly when the user is doing something that "
            "matters.",
            "<b>Which gives a design rule:</b> <b>interrupt only for "
            "something more important than what the user is doing</b>, "
            "and <b>the system does not know what that is</b>, so the "
            "default should be not to."]},

  {"t": "bullets", "kicker": "Attention", "title": "And what follows for design",
   "items": [
     "<b>Batch notifications</b> rather than delivering them as "
     "they arrive — which converts many switches into "
     "one.",
     "",
     "<b>Make interruptions resumable:</b> <b>preserve the state, "
     "the scroll position, and the partially entered data</b> — "
     "because losing them makes the switch cost "
     "unbounded.",
     "",
     "<b>And do not steal focus.</b> <b>A dialogue that appears "
     "under the cursor mid-typing receives input intended for "
     "something else</b>, which is a destructive failure rather than an "
     "annoyance.",
     "",
     "<b>Reserve modal interruption for the irreversible</b>, "
     "which is almost nothing.",
     "",
     "<b>And note that this is the same argument as "
     "CSCE 701 §11's compliance "
     "budget</b> — attention is finite and everything spends from "
     "it.",
   ],
   "footnote": "<b>Focus stealing is the one that causes data "
               "loss</b> — and it is still common, which makes it "
               "worth naming as a defect rather than a "
               "preference."},

  {"t": "section", "label": "Part 2", "title": "Working memory",
   "blurb": "Very small, and the number is lower than the famous one."},

  {"t": "callout", "title": "Working memory holds about four chunks, not seven, and loses them in seconds",
   "kind": "The limit, corrected",
   "body": ["<b>The famous figure of seven plus or minus two is "
            "higher than the current estimate</b> — <b>the modern "
            "figure for unrehearsed capacity is around four "
            "chunks</b>, and it falls further under any concurrent "
            "task.",
            "<b>And a chunk is whatever the person has already "
            "learned as a unit</b> — so <b>an expert holds more of "
            "their domain because their chunks are larger</b>, not "
            "because their memory is.",
            "<b>Which means any design requiring a person to carry "
            "information between screens is requiring something they "
            "mostly cannot do</b> — a code from one page to another, "
            "a value to compare, a step in a sequence.",
            "<b>So the rule is: show it, do not ask them to remember "
            "it</b> — <b>which is almost always possible</b> and is the "
            "most frequently violated principle in "
            "the course."]},

  {"t": "bullets", "kicker": "Consequences", "title": "The specific design consequences",
   "items": [
     "<b>Keep the information needed for a decision visible at "
     "the moment of the decision</b> — not on a previous "
     "screen.",
     "",
     "<b>Avoid modal dialogues that hide the thing they ask "
     "about</b>, which is a common and self-defeating "
     "pattern.",
     "",
     "<b>Prefer recognition to recall</b> "
     "(Part 3) — show the options rather than "
     "requiring the name.",
     "",
     "<b>And do not require re-entry of anything the system "
     "already has</b>, which is both a memory demand and an error "
     "opportunity.",
     "",
     "<b>Which is why a wizard that forgets what you typed on step "
     "two is worse than a single long form.</b>",
   ],
   "footnote": "<b>'Show it, do not ask them to remember it' resolves "
               "most of this module's design questions</b> — and it "
               "is cheap, because the system already has the "
               "information."},

  {"t": "section", "label": "Part 3", "title": "Recognition and recall",
   "blurb": "A large asymmetry with an obvious consequence."},

  {"t": "callout", "title": "Recognising something is far easier than recalling it, which is why menus beat command lines for novices",
   "kind": "The asymmetry, and when each is right",
   "body": ["<b>Recognition requires only matching against what is "
            "present; recall requires generating from "
            "nothing</b> — and the difference in success rate is "
            "large.",
            "<b>So a visible list of options is usable "
            "immediately</b>, and a command requiring the exact name is "
            "not — which is why discoverability and menus go "
            "together.",
            "<b>But recall is faster once learned</b>, and <b>an "
            "expert using a command line outperforms the same person "
            "using menus</b> by a wide margin — so the asymmetry "
            "does not settle the design.",
            "<b>Which argues for both:</b> <b>a discoverable path for "
            "learning and a fast path for expertise</b>, with the fast "
            "path's existence signified in the slow one — a command "
            "palette showing its own shortcut."]},

  {"t": "section", "label": "Part 4", "title": "Error",
   "blurb": "Two kinds, needing different fixes."},

  {"t": "table", "kicker": "Error", "title": "Slips and mistakes",
   "header": ["", "Slip", "Mistake"],
   "widths": [2.5, 4.1, 4.8],
   "rows": [
     ["<b>What happened</b>", "<b>Right intention, wrong action</b>", "<b>Wrong intention, executed correctly</b>"],
     ["<b>Cause</b>", "<b>Attention, similarity, automaticity</b>", "<b>A wrong mental model (M04)</b>"],
     ["<b>Who makes them</b>", "<b>Experts, more than novices</b>", "<b>Novices, more than experts</b>"],
     ["<b>The fix</b>", "<b>Differentiate the controls; make it reversible</b>", "<b>Fix the conceptual model and its signifiers</b>"],
     ["<b>Example</b>", "<b>Clicked the adjacent menu item</b>", "<b>Believed 'archive' deleted it</b>"],
   ],
   "footnote": "<b>Experts make more slips because expertise is "
               "automaticity</b> — which means a design that is safe "
               "for novices may be dangerous for the people who use it "
               "most.",
   "note": "The experts-make-more-slips finding is the "
           "counter-intuitive one."},

  {"t": "callout", "title": "And the error rate is predictable from the design, which makes it an engineering quantity",
   "kind": "Closing",
   "body": ["<b>Adjacent destructive and benign controls produce "
            "slips at a rate you can measure</b> — and <b>separating "
            "them lowers it</b>, which is a design change with a "
            "predicted effect.",
            "<b>Similarly: a required value held across screens "
            "produces transcription errors; an unlabelled unit produces "
            "magnitude errors; a modal dialogue produces reflexive "
            "dismissal.</b>",
            "<b>So error is not a user property but a joint property "
            "of the person and the design</b> — which means it can be "
            "designed down, and the amount is "
            "measurable.",
            "<b>Which is Module 01 §4's reframing with a "
            "number attached</b> — <b>and is what turns a design "
            "argument into a prediction you can test</b> "
            "(Module 07)."]},
 ],
 "takeaways": [
   "People switch rather than multitask, and every switch costs "
   "reorientation time and raises the error rate.",
   "An interruption costs more than its duration, because the task state "
   "has to be rebuilt — and the cost scales with task complexity.",
   "Working memory holds about four chunks rather than seven, and falls "
   "further under any concurrent task.",
   "'Show it, do not ask them to remember it' is the most frequently "
   "violated principle in the course, and it is almost always possible.",
   "Recognition beats recall for novices and recall is faster once "
   "learned, which argues for both paths with the fast one signified.",
   "Experts make more slips than novices because expertise is "
   "automaticity, so a design safe for novices may be dangerous for heavy "
   "users.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Attention"),
  ("callout", "Attention is a single channel, and switching it costs time "
              "and accuracy",
   ["<b>People do not multitask; they switch between tasks</b> — "
    "and <b>every switch costs reorientation time and raises the "
    "subsequent error rate</b>, both of which are measured and "
    "substantial rather than marginal.",
    "<b>So an interruption is expensive in a way its duration badly "
    "understates:</b> <b>a five-second notification can cost far more "
    "than five seconds of task progress</b>, <b>because the mental state "
    "of the interrupted task has to be rebuilt</b> from whatever is still "
    "visible.",
    "<b>And the cost scales with the interrupted task's "
    "complexity</b> — <b>which means interruptions are worst "
    "precisely when the user is doing something that matters</b> and has "
    "the most state to lose.",
    "<b>Which gives a clear design rule:</b> <b>interrupt only for "
    "something more important than whatever the user is currently "
    "doing</b> — and <b>the system does not know what that is</b>, "
    "<b>so the default should be not to interrupt</b> and to let the user "
    "come to the information."]),
  ("ul", ["<b>Batch notifications</b> rather than delivering each one "
          "as it arrives — <b>which converts many switches into "
          "one</b> and is the single largest available improvement to a "
          "notification system.",
          "<b>Make interruptions resumable:</b> <b>preserve the "
          "state, the scroll position, the selection, and any partially "
          "entered data</b> — <b>because losing them makes the "
          "switching cost effectively unbounded</b> rather than merely "
          "high.",
          "<b>And do not steal focus.</b> <b>A dialogue that appears "
          "under the cursor while somebody is typing receives input that "
          "was intended for something else</b> — which is <b>a "
          "destructive failure rather than an annoyance</b>, since the "
          "keystroke may have dismissed it with a choice nobody made.",
          "<b>Reserve modal interruption for the genuinely "
          "irreversible</b>, which on inspection is almost "
          "nothing (&sect;4, and Module 01 &sect;4's undo "
          "preference).",
          "<b>And note that this is the same argument as CSCE 701 "
          "Module 11's compliance budget</b> — <b>attention is "
          "finite and everything spends from it</b>, so each interruption "
          "reduces the attention available for whatever you most wanted "
          "them to notice. <b>Focus stealing is the one that causes "
          "actual data loss</b>, and it is still common, which makes it "
          "worth naming as a defect rather than a preference."]),

  ("h1", "2 &nbsp; Working memory"),
  ("callout", "Working memory holds about four chunks, not seven, and loses "
              "them in seconds",
   ["<b>The famous figure of seven plus or minus two is higher than the "
    "current estimate</b> — <b>the modern figure for unrehearsed "
    "capacity is around four chunks</b>, and <b>it falls further under "
    "any concurrent task</b>, including the task of operating your "
    "interface.",
    "<b>And a chunk is whatever the person has already learned as a "
    "single unit</b> — so <b>an expert holds more of their own "
    "domain because their chunks are larger</b>, not because their memory "
    "capacity is greater, which is the finding that makes expertise "
    "intelligible.",
    "<b>Which means any design requiring a person to carry "
    "information between screens is requiring something they mostly "
    "cannot do</b> — a confirmation code from one page to another, a "
    "value to compare against, their position in a multi-step "
    "sequence.",
    "<b>So the rule is: show it, do not ask them to remember "
    "it</b> — <b>which is almost always technically possible</b> "
    "(the system has the information) and <b>is the most frequently "
    "violated principle in this course.</b>"]),
  ("ul", ["<b>Keep the information needed for a decision visible at "
          "the moment of the decision</b> — <b>not on a previous "
          "screen</b>, which is where it usually is because that is where "
          "it was collected.",
          "<b>Avoid modal dialogues that hide the thing they are "
          "asking about</b> — 'are you sure you want to delete this?' "
          "over the top of the thing being deleted is <b>a common and "
          "self-defeating pattern</b>.",
          "<b>Prefer recognition to recall</b> (&sect;3) — "
          "<b>show the available options rather than requiring the "
          "person to produce the name</b>, which converts a memory task "
          "into a matching task.",
          "<b>And do not require re-entry of anything the system "
          "already holds</b> — which is <b>both a memory demand and "
          "an error opportunity</b>, and is sometimes defended as "
          "verification when it is actually transcription.",
          "<b>Which is why a multi-step wizard that forgets what you "
          "typed on step two is worse than a single long form</b>: the "
          "form at least keeps everything visible. <b>'Show it, do not "
          "ask them to remember it' resolves most of this module's design "
          "questions</b>, and <b>it is cheap, because the system already "
          "has the information</b> — the only cost is layout."]),

  ("break",),
  ("h1", "3 &nbsp; Recognition and recall"),
  ("callout", "Recognising something is far easier than recalling it, which "
              "is why menus beat command lines for novices",
   ["<b>Recognition requires only matching against what is present; "
    "recall requires generating the answer from nothing</b> — and "
    "<b>the difference in success rate is large</b>, consistently, across "
    "every domain it has been measured in.",
    "<b>So a visible list of options is usable immediately</b>, and "
    "<b>a command requiring the exact name is not</b> — which is why "
    "<b>discoverability and menus go together</b>, and why a powerful "
    "tool with no visible surface has a learning cliff rather than a "
    "curve.",
    "<b>But recall is faster once it has been learned</b>, and <b>an "
    "expert using a command line outperforms the same person using menus "
    "by a wide margin</b> — <b>so the asymmetry does not by itself "
    "settle the design question</b>, which is the part usually left "
    "out.",
    "<b>Which argues for both:</b> <b>a discoverable path for "
    "learning and a fast path for expertise</b>, <b>with the fast path's "
    "existence signified within the slow one</b> — a menu item "
    "displaying its own keyboard shortcut, or a command palette that "
    "shows the shortcut for whatever you just ran. <b>This is the "
    "pattern that serves both populations without compromising "
    "either.</b>"]),

  ("h1", "4 &nbsp; Error"),
  ("table", ["", "Slip", "Mistake"],
   [["<b>What happened</b>",
     "<b>The right intention, executed with the wrong action.</b>",
     "<b>The wrong intention, executed perfectly correctly.</b>"],
    ["<b>The cause</b>",
     "<b>Attention, similarity between controls, and automaticity.</b>",
     "<b>A wrong mental model of the system</b> (Module 04)."],
    ["<b>Who makes them</b>",
     "<b>Experts, more than novices</b> — see the note.",
     "<b>Novices, more than experts.</b>"],
    ["<b>The fix</b>",
     "<b>Differentiate the controls, separate them spatially, and make "
     "the action reversible.</b>",
     "<b>Fix the conceptual model and the signifiers that convey it</b> "
     "(Module 04 &sect;3)."],
    ["<b>Example</b>",
     "<b>Clicked the menu item adjacent to the intended one.</b>",
     "<b>Believed that 'archive' deleted the message.</b>"]],
   [0.19, 0.37, 0.44]),
  ("p", "<b>Experts make more slips than novices because expertise "
        "<i>is</i> automaticity</b> — the expert is not attending to "
        "the individual actions, which is what makes them fast and what "
        "makes the occasional wrong one go uncaught. <b>Which means a "
        "design that is safe for novices may be dangerous for the people "
        "who use it most</b>, and <b>that is the counter-intuitive "
        "finding of the module</b>: the destructive control adjacent to a "
        "common one is a hazard specifically for your heaviest users."),
  ("callout", "And the error rate is predictable from the design, which "
              "makes it an engineering quantity",
   ["<b>Adjacent destructive and benign controls produce slips at a "
    "rate you can measure</b> — and <b>separating them lowers "
    "it</b> — <b>which is a design change with a predicted effect</b> "
    "rather than a matter of preference.",
    "<b>Similarly, and each with a predictable rate:</b> <b>a required "
    "value held across screens produces transcription errors; an "
    "unlabelled unit produces magnitude errors; a modal dialogue produces "
    "reflexive dismissal; two similar labels produce selection "
    "errors.</b>",
    "<b>So error is not a property of the user but a joint property of "
    "the person and the design</b> — <b>which means it can be "
    "designed down, and the amount by which is measurable</b> "
    "(Module 07's testing, and Module 08's experiment).",
    "<b>Which is Module 01 &sect;4's reframing with a number "
    "attached</b> — and <b>is what turns a design argument into a "
    "prediction you can test</b>, which is the move that makes this "
    "subject an engineering discipline rather than a critical one."]),
 ],
 "resources": [
   ("Johnson &mdash; Designing with the Mind in Mind, chapters 7 "
    "through 11",
    "https://www.elsevier.com/books/designing-with-the-mind-in-mind/johnson/978-0-12-818202-4",
    "<b>&sect;1 through &sect;3</b>, with the corrected memory figures and "
    "the sources. Library copy."),
   ("Cowan &mdash; The magical number 4 in short-term memory (free)",
    "https://pubmed.ncbi.nlm.nih.gov/11515286/",
    "<b>&sect;2's correction in the original</b> — why the figure is "
    "four rather than seven, and what a chunk is."),
   ("Norman &mdash; The Design of Everyday Things, chapter 5",
    "https://mitpress.mit.edu/9780262525671/",
    "<b>&sect;4's slip and mistake taxonomy</b>, with the sub-categories "
    "and the fixes."),
   ("Mark, Gudith & Klocke &mdash; The cost of interrupted work (free)",
    "https://dl.acm.org/doi/10.1145/1357054.1357072",
    "<b>&sect;1's switching cost, measured</b> — and the finding that "
    "people compensate by working faster, at a cost in stress."),
 ],
 "exercises": [
   "<b>Time yourself on a task with and without an interruption</b>, "
   "and measure the recovery.",
   "<b>Find a notification in your own software</b> that could be "
   "batched.",
   "<b>Find a focus-stealing dialogue</b> and reproduce the data loss it "
   "can cause.",
   "<b>Find a place in an interface</b> that requires carrying "
   "information between screens.",
   "<b>Fix it by showing the information</b> at the point of "
   "decision.",
   "<b>Count the chunks</b> a task in your software requires somebody to "
   "hold.",
   "<b>Find a modal dialogue that hides what it asks about.</b>",
   "<b>Add shortcut signifiers</b> to a menu, and check whether anybody "
   "learns them.",
   "<b>Classify ten errors you have made</b> as slips or mistakes.",
   "<b>Find adjacent destructive and benign controls</b> and predict the "
   "slip rate before measuring it.",
 ],
 "selfcheck": [
   "Why do people switch rather than multitask, and what does a switch "
   "cost?",
   "Why does an interruption cost more than its duration?",
   "Give five design consequences for attention, and the one that "
   "destroys data.",
   "State the working memory limit, and what a chunk is.",
   "What is the most frequently violated principle in the course?",
   "Give four consequences of the memory limit.",
   "State the recognition/recall asymmetry and why it does not settle "
   "the design.",
   "Contrast slips and mistakes on five dimensions.",
   "Why do experts make more slips, and what follows?",
   "Why is error an engineering quantity?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Mental Models",
 "subtitle": "What the user believes the system is.",
 "question": "What does the user think is happening?",
 "outcomes": [
     "Explain the three models and the gaps between them.",
     "Explain how mental models are formed.",
     "Elicit a user's mental model.",
     "Design a conceptual model and convey it.",
     "Diagnose mistakes as model mismatches.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Three models",
   "blurb": "And only one of them is visible to the user."},

  {"t": "table", "kicker": "Models", "title": "The design model, the system image, and the user's model",
   "header": ["Model", "Whose it is", "Where it lives"],
   "widths": [2.8, 3.8, 4.6],
   "rows": [
     ["<b>Design model</b>", "<b>The designer's</b>", "<b>In their head and the code</b>"],
     ["<b>System image</b>", "<b>Nobody's — it is the artefact</b>", "<b>The interface, docs, and behaviour</b>"],
     ["<b>User's model</b>", "<b>The user's</b>", "<b>Inferred entirely from the system image</b>"],
   ],
   "footnote": "<b>The designer communicates with the user only "
               "through the system image</b> — so <b>a correct design "
               "model conveyed by a poor system image produces a wrong "
               "user model</b>, and the design was still wrong.",
   "note": "The only-through-the-system-image point is the module's "
           "core."},

  {"t": "callout", "title": "The user will build a model whether or not you gave them one",
   "kind": "Why this is not optional",
   "body": ["<b>People do not operate a system without a theory of "
            "it</b> — they construct one from the interface, the "
            "vocabulary, the behaviour, and whatever analogy comes to "
            "hand.",
            "<b>So the question is not whether they have a model but "
            "whether it is the one you intended</b> — and <b>if you "
            "did not design one, they will build something from the "
            "accidents of your implementation.</b>",
            "<b>And a wrong model produces mistakes rather than "
            "slips</b> (Module 03 §4) — <b>confident, "
            "correctly-executed, wrong actions</b>, which are harder to "
            "catch than slips and more damaging.",
            "<b>Which means designing the conceptual model is a "
            "design activity in its own right</b> — <b>before the "
            "layout</b>, because the layout's job is to convey it "
            "(Part 3)."]},

  {"t": "section", "label": "Part 2", "title": "How models form",
   "blurb": "From analogy, from vocabulary, and from accidents."},

  {"t": "bullets", "kicker": "Sources", "title": "Where a user's model comes from",
   "items": [
     "<b>Analogy with something known</b> — a folder, a desk, "
     "a conversation, a document. <b>Powerful, and it imports the "
     "analogy's properties whether you wanted them or "
     "not.</b>",
     "",
     "<b>The vocabulary.</b> <b>Calling it 'archive' implies "
     "retrievability; 'remove' implies loss</b> — and <b>the word "
     "does more work than any help text.</b>",
     "",
     "<b>The observed behaviour</b>, including the timing and the "
     "errors — people theorise from what the system actually "
     "does.",
     "",
     "<b>And other systems' conventions</b>, which is why "
     "consistency with the platform is worth more than internal "
     "elegance.",
     "",
     "<b>So the vocabulary is the highest-leverage design "
     "decision</b>, and it is usually made in a hurry.",
   ],
   "footnote": "<b>The word does more work than any help "
               "text</b> — because it is present at the moment of "
               "decision and the help text is not "
               "(Module 01 §2)."},

  {"t": "callout", "title": "An analogy imports properties you did not choose",
   "kind": "The risk in the strongest tool here",
   "body": ["<b>A 'folder' implies that a file is in exactly one "
            "place</b> — so a tagging system presented as folders "
            "produces confusion at exactly the point where the analogy "
            "breaks.",
            "<b>And the breakage is worse than no analogy</b>, "
            "because <b>the user was confident until the moment it "
            "failed</b>, and now distrusts the parts that worked.",
            "<b>So choose the analogy for where it breaks, not only "
            "for where it fits</b> — and <b>signal the break "
            "explicitly</b> where it occurs.",
            "<b>Or choose a weaker analogy deliberately:</b> <b>a "
            "term with no strong prior implication forces the user to "
            "learn the actual model</b>, which is slower and more "
            "accurate."]},

  {"t": "section", "label": "Part 3", "title": "Conveying it",
   "blurb": "Making the system image carry the model."},

  {"t": "bullets", "kicker": "Conveying", "title": "How a system image communicates a model",
   "items": [
     "<b>Make the state visible.</b> <b>A system whose state is "
     "hidden cannot convey a model of its "
     "state</b> — which is most configuration systems "
     "(Module 10 §4).",
     "",
     "<b>Make the structure visible.</b> <b>If the data has a "
     "hierarchy, show the hierarchy</b> — and if it does not, do "
     "not imply one.",
     "",
     "<b>Make the consequences visible before the action</b>, not "
     "after — a preview is a model-communication device as much "
     "as a convenience.",
     "",
     "<b>And keep the vocabulary consistent and "
     "accurate</b> — one name per concept, and the name should be "
     "true.",
     "",
     "<b>Which together make the model inferable</b> — and "
     "<b>documentation is the fallback for when the system image "
     "failed.</b>",
   ],
   "footnote": "<b>Documentation is the fallback for a system image "
               "that failed</b> — which is not an argument against "
               "documentation and is an argument against relying on "
               "it."},

  {"t": "section", "label": "Part 4", "title": "Eliciting it",
   "blurb": "Finding out what they actually think."},

  {"t": "callout", "title": "Ask them to explain the system to you, and the mismatch is the finding",
   "kind": "The method",
   "body": ["<b>Ask a user to describe what happens when they do "
            "something, before they do it</b> — <b>and the "
            "difference between their account and the truth is a design "
            "defect with a location.</b>",
            "<b>And ask them to draw it</b>, which surfaces "
            "structural beliefs that verbal description "
            "omits — whether things are nested, shared, or "
            "copied.",
            "<b>Or ask them to predict:</b> <b>'what will happen if "
            "you click that' is the sharpest single question in this "
            "course</b>, because a wrong prediction is an unambiguous "
            "finding.",
            "<b>Which is Module 07's technique applied to beliefs "
            "rather than to actions</b> — and it finds the mistakes, "
            "where observing actions finds the slips."]},

  {"t": "bullets", "kicker": "Practice", "title": "And what to do with a mismatch",
   "items": [
     "<b>Change the vocabulary first</b>, because it is the "
     "cheapest change with the largest effect "
     "(Part 2).",
     "",
     "<b>Then make the relevant state or structure "
     "visible</b> (Part 3), so the model is inferable rather "
     "than taught.",
     "",
     "<b>Then consider changing the system</b> — <b>sometimes "
     "the user's model is better than yours</b>, and that is a "
     "legitimate outcome of the investigation.",
     "",
     "<b>And only then write documentation</b>, which is the "
     "weakest of the four and the one usually reached for "
     "first.",
     "",
     "<b>Which is the ordering that makes this module "
     "actionable.</b>",
   ],
   "footnote": "<b>'Sometimes the user's model is better than yours' "
               "is worth taking seriously</b> — a consistently wrong "
               "expectation across five users is evidence about the domain "
               "rather than about them."},
 ],
 "takeaways": [
   "The designer communicates with the user only through the system image, "
   "so a correct design model conveyed poorly produces a wrong user model.",
   "The user will build a model whether or not you designed one, and a "
   "wrong model produces mistakes rather than slips.",
   "The vocabulary does more work than any help text, because it is "
   "present at the moment of decision.",
   "An analogy imports properties you did not choose, so choose it for "
   "where it breaks rather than where it fits.",
   "'What will happen if you click that' is the sharpest single question "
   "in the course, because a wrong prediction is unambiguous.",
   "Sometimes the user's model is better than yours, and a consistently "
   "wrong expectation is evidence about the domain.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Three models"),
  ("table", ["Model", "Whose it is", "Where it lives"],
   [["<b>The design model</b>", "<b>The designer's.</b>",
     "<b>In their head, and in the code</b> — neither of which the "
     "user can inspect."],
    ["<b>The system image</b>",
     "<b>Nobody's — it is the artefact itself.</b>",
     "<b>The interface, the documentation, the vocabulary, and the "
     "observable behaviour.</b>"],
    ["<b>The user's model</b>", "<b>The user's.</b>",
     "<b>Inferred entirely from the system image</b>, plus whatever "
     "analogies and conventions they bring (&sect;2)."]],
   [0.22, 0.31, 0.47]),
  ("p", "<b>The designer communicates with the user only through the "
        "system image</b> — there is no other channel — so <b>a "
        "perfectly coherent design model conveyed by a poor system image "
        "produces a wrong user model, and the design was still wrong.</b> "
        "<b>The only-through-the-system-image point is this module's "
        "core</b>, and it is why 'but the model is coherent if you "
        "understand it' is not a defence."),
  ("callout", "The user will build a model whether or not you gave them one",
   ["<b>People do not operate a system without some theory of it</b> "
    "— they construct one from the interface, the vocabulary, the "
    "observed behaviour, and whatever analogy comes most readily to "
    "hand.",
    "<b>So the question is never whether they have a model but whether "
    "it is the one you intended</b> — and <b>if you did not design "
    "one, they will build something out of the accidents of your "
    "implementation</b>, which is reliably worse than anything you would "
    "have chosen.",
    "<b>And a wrong model produces mistakes rather than slips</b> "
    "(Module 03 &sect;4) — <b>confident, correctly-executed, "
    "wrong actions</b> — <b>which are harder to catch than slips and "
    "considerably more damaging</b>, because the user has no reason to "
    "check.",
    "<b>Which means designing the conceptual model is a design "
    "activity in its own right</b> — <b>and it comes before the "
    "layout</b>, because the layout's job is to convey it (&sect;3). A "
    "project that starts with screens has skipped this step and will "
    "convey whatever the screens happen to imply."]),

  ("h1", "2 &nbsp; How models form"),
  ("ul", ["<b>Analogy with something already known</b> — a "
          "folder, a desk, a conversation, a document, a queue. "
          "<b>Powerful, and it imports the analogy's properties whether "
          "you wanted them or not</b> (see the callout).",
          "<b>The vocabulary.</b> <b>Calling something 'archive' "
          "implies it remains retrievable; 'remove' implies it is "
          "gone</b> — and <b>the word does more work than any amount "
          "of help text</b>, because it is present at the moment of "
          "decision and the help text is not "
          "(Module 01 &sect;2).",
          "<b>The observed behaviour</b>, including the timing, the "
          "orderings, and the error cases — <b>people theorise from "
          "what the system actually does</b>, and they are quite good at "
          "it given enough exposure.",
          "<b>And other systems' conventions</b>, which <b>is why "
          "consistency with the platform is worth more than internal "
          "elegance</b>: the user arrives with a model already, and "
          "matching it is free.",
          "<b>So the vocabulary is the highest-leverage design "
          "decision in this module</b>, <b>and it is usually made in a "
          "hurry</b> by whoever wrote the first version of the code "
          "— which is worth correcting deliberately later, even "
          "though renaming is disruptive."]),
  ("callout", "An analogy imports properties you did not choose",
   ["<b>A 'folder' implies that a file is in exactly one place</b> "
    "— that is what folders are — <b>so a tagging system "
    "presented as folders produces confusion at exactly the point where "
    "the analogy breaks</b>: the moment something appears in two.",
    "<b>And the breakage is worse than having used no analogy at "
    "all</b>, because <b>the user was confident right up until the moment "
    "it failed</b>, and now <b>distrusts the parts of the analogy that "
    "were working</b> — which costs them everything they had "
    "learned.",
    "<b>So choose the analogy for where it breaks, not only for where "
    "it fits</b> — and <b>signal the break explicitly at the point "
    "where it occurs</b>, which is a design requirement rather than a "
    "documentation one.",
    "<b>Or choose a weaker analogy deliberately:</b> <b>a term with "
    "no strong prior implication forces the user to learn the actual "
    "model</b>, <b>which is slower and more accurate</b> — and is "
    "the right trade for a system whose behaviour genuinely does not "
    "match anything familiar."]),

  ("break",),
  ("h1", "3 &nbsp; Conveying it"),
  ("ul", ["<b>Make the state visible.</b> <b>A system whose state is "
          "hidden cannot convey a model of its state</b> — the user "
          "has nothing to infer from — <b>which describes most "
          "configuration systems</b> (Module 10 &sect;4) and most "
          "background processes.",
          "<b>Make the structure visible.</b> <b>If the data has a "
          "hierarchy, show the hierarchy</b>; <b>and if it does not, do "
          "not imply one</b> with indentation or nesting that the model "
          "does not support (&sect;2's folder problem).",
          "<b>Make the consequences visible before the action rather "
          "than after it</b> — <b>a preview is a model-communication "
          "device at least as much as a convenience</b>, because it shows "
          "what the system believes the action means.",
          "<b>And keep the vocabulary consistent and accurate</b> "
          "— <b>one name per concept, and the name should be "
          "true</b>: a 'save' that uploads, or a 'delete' that archives, "
          "teaches a wrong model very efficiently.",
          "<b>Which together make the model inferable</b> from the "
          "interface alone — and <b>documentation is the fallback for "
          "when the system image failed.</b> <b>That is not an argument "
          "against documentation and is an argument against relying on "
          "it</b>, since Module 01 &sect;2's non-reading finding "
          "applies."]),

  ("h1", "4 &nbsp; Eliciting it"),
  ("callout", "Ask them to explain the system to you, and the mismatch is "
              "the finding",
   ["<b>Ask a user to describe what happens when they do something, "
    "before they do it</b> — <b>and the difference between their "
    "account and the truth is a design defect with a location</b>, which "
    "is far more useful than a general impression of confusion.",
    "<b>And ask them to draw it</b>, which <b>surfaces structural "
    "beliefs that verbal description omits</b> — whether they think "
    "things are nested, shared, copied, or linked, which is exactly the "
    "class of belief that produces Module 03 &sect;4's mistakes.",
    "<b>Or ask them to predict:</b> <b>'what will happen if you click "
    "that' is the sharpest single question in this course</b>, <b>because "
    "a wrong prediction is an unambiguous finding</b> requiring no "
    "interpretation and admitting no argument.",
    "<b>Which is Module 07's technique applied to beliefs rather "
    "than to actions</b> — and <b>it finds the mistakes, where "
    "observing actions finds the slips</b>. A full study wants both, and "
    "the prediction question costs nothing to add."]),
  ("ul", ["<b>Change the vocabulary first</b>, <b>because it is the "
          "cheapest change with the largest effect</b> (&sect;2) — "
          "and because a wrong name actively teaches the wrong "
          "model.",
          "<b>Then make the relevant state or structure visible</b> "
          "(&sect;3), <b>so that the model is inferable rather than "
          "taught</b> — which is more robust, since it works for "
          "users who arrive later and read nothing.",
          "<b>Then consider changing the system itself</b> — "
          "<b>sometimes the user's model is better than yours</b>, and "
          "<b>that is a legitimate outcome of the investigation</b> "
          "rather than a failure of it.",
          "<b>And only then write documentation</b>, <b>which is the "
          "weakest of the four options and the one usually reached for "
          "first</b> — because it is the only one that does not "
          "require changing the product.",
          "<b>Which is the ordering that makes this module "
          "actionable.</b> <b>'Sometimes the user's model is better than "
          "yours' is worth taking seriously</b>: <b>a consistently wrong "
          "expectation across five users is evidence about the domain "
          "rather than about them</b>, and it has changed real product "
          "designs for the better."]),
 ],
 "resources": [
   ("Norman &mdash; The Design of Everyday Things, chapter 3",
    "https://mitpress.mit.edu/9780262525671/",
    "<b>The whole module</b> — the three models, the system image, and "
    "the knowledge-in-the-world argument."),
   ("Johnson-Laird &mdash; Mental Models",
    "https://www.hup.harvard.edu/catalog.php?isbn=9780674568822",
    "<b>&sect;1 and &sect;2's cognitive basis</b> — where the term "
    "comes from and what it is claimed to be. Library copy."),
   ("Kuang & Fabricant &mdash; User Friendly",
    "https://us.macmillan.com/books/9780374279752/userfriendly",
    "<b>&sect;2's analogies, historically</b> — how particular "
    "metaphors were chosen and what they cost later. Library copy."),
   ("Nielsen Norman Group on mental models (free)",
    "https://www.nngroup.com/articles/mental-models/",
    "<b>&sect;4's elicitation, practically</b> — with the interview "
    "protocols."),
 ],
 "exercises": [
   "<b>Write out the design model</b> for something you built, in a "
   "paragraph.",
   "<b>Ask somebody to explain the same system</b> and compare.",
   "<b>List everything your system image conveys</b> that you did not "
   "intend.",
   "<b>Find an analogy in software you use</b> and the exact point where "
   "it breaks.",
   "<b>Find a name in your own software</b> that implies something "
   "false.",
   "<b>Rename it</b> and note what else has to change.",
   "<b>Ask three people to draw how a system works</b>, and compare the "
   "drawings.",
   "<b>Ask five people to predict</b> what a button will do, before "
   "clicking.",
   "<b>Find a case where the users' shared wrong expectation</b> is "
   "better than your design.",
   "<b>Apply Part 4's four fixes in order</b> to one mismatch.",
 ],
 "selfcheck": [
   "Name the three models and where each lives.",
   "Why is the system image the only channel?",
   "Why will the user have a model regardless?",
   "What kind of error does a wrong model produce, and why is it "
   "worse?",
   "Name four sources of a user's model, and the highest-leverage "
   "one.",
   "Why is a broken analogy worse than none?",
   "Give four ways a system image conveys a model.",
   "What is documentation's role, honestly?",
   "Give three elicitation techniques and the sharpest question.",
   "Give the four fixes in order of preference.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Interaction Design Principles",
 "subtitle": "The rules, and what each one costs.",
 "question": "Which principles are real, and when do they conflict?",
 "outcomes": [
     "State the principles and the mechanism behind each.",
     "Explain where they conflict and how to decide.",
     "Explain visibility, feedback, and constraints "
     "concretely.",
     "Explain defaults and why they dominate.",
     "Apply the heuristics as a review method.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The principles",
   "blurb": "Each with a mechanism, not just an injunction."},

  {"t": "table", "kicker": "Principles", "title": "The principles and the mechanism each addresses",
   "header": ["Principle", "The mechanism", "Module"],
   "widths": [2.7, 4.6, 3.5],
   "rows": [
     ["<b>Visibility</b>", "<b>Closes the execution gap</b>", "<b>01 §1</b>"],
     ["<b>Feedback</b>", "<b>Closes the evaluation gap</b>", "<b>01 §1, 02 §4</b>"],
     ["<b>Consistency</b>", "<b>Preserves learning; cuts memory load</b>", "<b>01 §3, 03 §2</b>"],
     ["<b>Constraints</b>", "<b>Makes the error impossible</b>", "<b>01 §4</b>"],
     ["<b>Recognition over recall</b>", "<b>Exploits the memory asymmetry</b>", "<b>03 §3</b>"],
     ["<b>Reversibility</b>", "<b>Makes the error recoverable</b>", "<b>01 §4</b>"],
     ["<b>Good defaults</b>", "<b>Requires nothing of the user</b>", "<b>05 §3</b>"],
   ],
   "footnote": "<b>Each principle is a response to a named "
               "mechanism</b> — which is what makes them arguable and "
               "testable rather than a style guide, and is why this "
               "course states the mechanism alongside each "
               "one.",
   "note": "Tying each principle to its mechanism is the pedagogical "
           "move."},

  {"t": "callout", "title": "A principle without a mechanism is a preference, and a principle with one is a prediction",
   "kind": "Why the table has three columns",
   "body": ["<b>'Be consistent' as an injunction can be argued with "
            "indefinitely.</b> <b>'Inconsistency invalidates learned "
            "conventions and therefore raises the error rate' is a claim "
            "you can test</b> (Module 03 §4).",
            "<b>So stating the mechanism converts a design argument "
            "into an empirical question</b> — which is the only way "
            "such arguments get settled "
            "(Module 01 §2).",
            "<b>And it tells you when the principle does not "
            "apply.</b> <b>Consistency with a bad convention preserves "
            "the wrong learning</b>, so the mechanism tells you the "
            "exception.",
            "<b>Which is why this course states mechanisms rather than "
            "rules</b> — <b>a rule you know the reason for is one you "
            "can apply to a case nobody anticipated.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Conflicts",
   "blurb": "Because they do, and the resolution is not automatic."},

  {"t": "bullets", "kicker": "Conflicts", "title": "Where the principles pull against each other",
   "items": [
     "<b>Visibility against simplicity.</b> <b>Showing "
     "everything makes nothing visible</b> "
     "(Module 02 §3) — so visibility means <i>of what "
     "matters now</i>.",
     "",
     "<b>Consistency against local optimality.</b> <b>The locally "
     "better treatment breaks the convention</b>, and the convention is "
     "usually worth more (Module 01 §3).",
     "",
     "<b>Constraints against flexibility.</b> <b>Preventing the "
     "error prevents the legitimate unusual case</b> — which is "
     "the tension in every validation rule.",
     "",
     "<b>Efficiency for experts against learnability for "
     "novices</b> (Module 03 §3) — resolved by "
     "providing both paths rather than compromising.",
     "",
     "<b>And none of these resolves in general</b> — which is "
     "why Module 07's observation is the arbiter.",
   ],
   "footnote": "<b>The conflicts are the interesting part</b> — "
               "anybody can apply a principle in isolation, and design "
               "judgement is knowing which one yields."},

  {"t": "section", "label": "Part 3", "title": "Defaults",
   "blurb": "The principle with the largest effect."},

  {"t": "callout", "title": "The default is the setting almost everyone has, so it is the design",
   "kind": "Why this outranks the others",
   "body": ["<b>A small minority of users change any given "
            "setting</b> — so <b>the default is, in practice, the "
            "configuration of your system as used.</b>",
            "<b>Which makes it the only principle that requires "
            "nothing of the user at all</b> — no attention, no "
            "memory, no learning, and no reading.",
            "<b>And it is why CSCE 701 §11 §3 and "
            "CSCE 713 §10 §2 both arrive at the same "
            "conclusion from security</b>: the default is the "
            "intervention that works at population scale.",
            "<b>So choose defaults for the common case and the safe "
            "case</b> — <b>and when those conflict, say which you "
            "chose</b>, because an unsafe convenient default is a "
            "decision about other people's risk."]},

  {"t": "bullets", "kicker": "Defaults", "title": "And how to choose them",
   "items": [
     "<b>For the most common case</b>, which requires knowing what "
     "that is — and <b>guessing is where defaults usually go "
     "wrong.</b>",
     "",
     "<b>For the safe case where the stakes are "
     "asymmetric</b> — a destructive default is wrong even if it "
     "is what most people want most of the time.",
     "",
     "<b>Pre-fill rather than leave blank</b>, wherever the system "
     "knows the answer — which is "
     "Module 03 §2's show-it rule.",
     "",
     "<b>And make the default visible and changeable</b>, because "
     "<b>a hidden default is a decision the user cannot "
     "find</b>.",
     "",
     "<b>Then measure how often it is changed</b>, which tells you "
     "whether you chose correctly.",
   ],
   "footnote": "<b>Measuring how often a default is changed is the "
               "cheapest available evidence that you chose "
               "wrong</b> — and almost nobody instruments "
               "it."},

  {"t": "section", "label": "Part 4", "title": "Heuristic review",
   "blurb": "A method that is cheap and limited."},

  {"t": "callout", "title": "Heuristic evaluation finds many problems cheaply and misses the ones that matter most",
   "kind": "Stating its value honestly",
   "body": ["<b>Several reviewers independently walk the interface "
            "against a list of principles and record violations</b> "
            "— which takes hours rather than days and needs no "
            "participants.",
            "<b>And it finds a great deal:</b> <b>inconsistencies, "
            "missing feedback, poor error messages, and violated "
            "conventions</b>, all of which are real and worth "
            "fixing.",
            "<b>But it does not find what actual users will "
            "do.</b> <b>A reviewer knows what the interface is "
            "<i>for</i></b>, so they cannot discover that the task model "
            "is wrong — which is the expensive class of "
            "problem.",
            "<b>So: use it before testing, to remove the obvious "
            "problems so the test finds the interesting "
            "ones</b> — <b>and never instead of testing</b>, which is "
            "the substitution it invites."]},

  {"t": "bullets", "kicker": "Method", "title": "How to run one so it is worth doing",
   "items": [
     "<b>Use three to five reviewers independently</b>, then "
     "merge — <b>a single reviewer finds a minority of the "
     "problems</b>, and the overlap between reviewers is "
     "low.",
     "",
     "<b>Walk specific tasks</b>, not the interface as a "
     "catalogue — which keeps the review grounded in what "
     "somebody would be trying to do.",
     "",
     "<b>Record the violated principle and its mechanism</b> for "
     "each finding (Part 1), so each is "
     "actionable.",
     "",
     "<b>And rate severity by frequency times impact</b>, so that "
     "the list can be prioritised rather than merely "
     "produced.",
     "",
     "<b>Then fix the obvious ones and test</b> "
     "(Module 07).",
   ],
   "footnote": "<b>The low overlap between reviewers is the finding "
               "that makes three to five necessary</b> — one "
               "reviewer's list is not a subset of the "
               "problems."},
 ],
 "takeaways": [
   "Each principle is a response to a named mechanism, which makes it "
   "testable rather than a style preference.",
   "A principle with a stated mechanism tells you when it does not apply, "
   "which a rule does not.",
   "The principles conflict, and knowing which one yields is what design "
   "judgement consists of.",
   "The default is the configuration of your system as used, and it is the "
   "only principle requiring nothing of the user.",
   "Measuring how often a default is changed is the cheapest evidence that "
   "you chose wrong, and almost nobody instruments it.",
   "Heuristic review finds many problems cheaply and cannot find that the "
   "task model is wrong, which is the expensive class.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The principles"),
  ("table", ["Principle", "The mechanism it addresses", "Where that is "
             "established"],
   [["<b>Visibility</b>",
     "<b>Closes the gulf of execution</b> — the user can see what is "
     "possible.", "<b>Module 01 &sect;1</b>"],
    ["<b>Feedback</b>",
     "<b>Closes the gulf of evaluation</b>, and must overcome change "
     "blindness.", "<b>Module 01 &sect;1, Module 02 &sect;4</b>"],
    ["<b>Consistency</b>",
     "<b>Preserves learned conventions and reduces the memory load.</b>",
     "<b>Module 01 &sect;3, Module 03 &sect;2</b>"],
    ["<b>Constraints</b>",
     "<b>Makes the error impossible</b> — the strongest of the three "
     "error fixes.", "<b>Module 01 &sect;4</b>"],
    ["<b>Recognition over recall</b>",
     "<b>Exploits the memory asymmetry.</b>",
     "<b>Module 03 &sect;3</b>"],
    ["<b>Reversibility</b>",
     "<b>Makes the error recoverable, requiring nothing at the moment of "
     "the error.</b>", "<b>Module 01 &sect;4</b>"],
    ["<b>Good defaults</b>",
     "<b>Requires nothing of the user at all.</b>",
     "<b>Module 05 &sect;3</b>"]],
   [0.24, 0.52, 0.24]),
  ("callout", "A principle without a mechanism is a preference, and a "
              "principle with one is a prediction",
   ["<b>'Be consistent' as a bare injunction can be argued with "
    "indefinitely</b>, and frequently is. <b>'Inconsistency invalidates "
    "learned conventions and therefore raises the error rate' is a claim "
    "you can test</b> (Module 03 &sect;4's predictable rates).",
    "<b>So stating the mechanism converts a design argument into an "
    "empirical question</b> — <b>which is the only way such "
    "arguments actually get settled</b> (Module 01 &sect;2's designer "
    "blindness: neither party is a reliable witness).",
    "<b>And it tells you when the principle does not apply.</b> "
    "<b>Consistency with a bad convention preserves the wrong "
    "learning</b> — so <b>the mechanism tells you the exception</b>, "
    "where a rule would not.",
    "<b>Which is why this course states mechanisms rather than "
    "rules</b> — <b>a rule you know the reason for is one you can "
    "apply to a case nobody anticipated</b>, and interface design is "
    "mostly cases nobody anticipated."]),

  ("h1", "2 &nbsp; Conflicts"),
  ("ul", ["<b>Visibility against simplicity.</b> <b>Showing "
          "everything makes nothing visible</b> (Module 02 &sect;3's "
          "emphasis count) — so <b>visibility means visibility "
          "<i>of what matters now</i></b>, which requires knowing what "
          "that is.",
          "<b>Consistency against local optimality.</b> <b>The "
          "locally better treatment breaks the established "
          "convention</b>, and <b>the convention is usually worth "
          "more</b> (Module 01 &sect;3's invalidated learning) — "
          "but not always, and that is the judgement.",
          "<b>Constraints against flexibility.</b> <b>Preventing the "
          "error also prevents the legitimate unusual case</b> — "
          "which is the tension inside every validation rule, and is why "
          "over-strict validation produces workarounds (CSCE 701 "
          "Module 11 &sect;4).",
          "<b>Efficiency for experts against learnability for "
          "novices</b> (Module 03 &sect;3) — <b>resolved by "
          "providing both paths rather than by compromising between "
          "them</b>, which is the one conflict in this list with a clean "
          "answer.",
          "<b>And none of the others resolves in general</b> — "
          "<b>which is why Module 07's observation is the arbiter</b> "
          "rather than a stronger principle. <b>The conflicts are the "
          "interesting part of this material</b>: anybody can apply a "
          "principle in isolation, and <b>design judgement is knowing "
          "which one yields in a particular case.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Defaults"),
  ("callout", "The default is the setting almost everyone has, so it is the "
              "design",
   ["<b>A small minority of users change any given setting</b>, across "
    "essentially every system ever measured — so <b>the default is, "
    "in practice, the configuration of your system as it is actually "
    "used.</b>",
    "<b>Which makes it the only principle in &sect;1's table that "
    "requires nothing whatsoever of the user</b> — no attention, no "
    "memory, no learning, no reading, and no decision.",
    "<b>And it is why CSCE 701 Module 11 &sect;3 and CSCE 713 "
    "Module 10 &sect;2 both arrive at exactly the same conclusion from "
    "a security direction</b>: <b>the default is the intervention that "
    "works at population scale</b>, and three courses converging on it "
    "is worth noticing.",
    "<b>So choose defaults for the common case and for the safe "
    "case</b> — and <b>when those two conflict, say which you "
    "chose</b>, <b>because an unsafe but convenient default is a "
    "decision about other people's risk</b> taken on their behalf "
    "(Module 12)."]),
  ("ul", ["<b>For the most common case</b>, which requires actually "
          "knowing what that is — and <b>guessing is where defaults "
          "usually go wrong</b>, because the designer's own usage is not "
          "representative (Module 01 &sect;2).",
          "<b>For the safe case wherever the stakes are "
          "asymmetric</b> — <b>a destructive default is wrong even if "
          "it is what most people want most of the time</b>, because the "
          "cost of the minority case is not comparable.",
          "<b>Pre-fill rather than leave blank</b>, wherever the "
          "system already knows or can guess the answer — which is "
          "<b>Module 03 &sect;2's show-it rule</b> applied to input "
          "rather than to display.",
          "<b>And make the default visible and changeable</b>, "
          "because <b>a hidden default is a decision the user cannot "
          "find</b> and therefore cannot disagree with — which is a "
          "small-scale version of Module 12's concern.",
          "<b>Then measure how often it is changed</b>, which tells "
          "you directly whether you chose correctly. <b>Measuring how "
          "often a default is changed is the cheapest available evidence "
          "that you chose wrong</b> — <b>and almost nobody "
          "instruments it</b>, which leaves a free signal unused."]),

  ("h1", "4 &nbsp; Heuristic review"),
  ("callout", "Heuristic evaluation finds many problems cheaply and misses "
              "the ones that matter most",
   ["<b>Several reviewers independently walk the interface against a "
    "list of principles and record the violations they find</b> — "
    "which <b>takes hours rather than days and requires no participants "
    "at all</b>, making it the cheapest method in the course.",
    "<b>And it finds a great deal:</b> <b>inconsistencies, missing "
    "feedback, poor error messages, violated platform conventions, and "
    "unlabelled controls</b> — all of which are real problems worth "
    "fixing and all of which a usability test would also have found more "
    "expensively.",
    "<b>But it does not find what actual users will do.</b> <b>A "
    "reviewer knows what the interface is <i>for</i></b> "
    "(Module 01 &sect;2 again), <b>so they cannot discover that the "
    "task model itself is wrong</b> — that the user wants to do "
    "something the design never contemplated — <b>which is the "
    "expensive class of problem.</b>",
    "<b>So: use it before testing, to remove the obvious problems so "
    "that the test finds the interesting ones</b> — <b>and never "
    "instead of testing</b>, <b>which is the substitution it "
    "invites</b> because it is so much cheaper and produces such a "
    "satisfying list."]),
  ("ul", ["<b>Use three to five reviewers independently</b>, and then "
          "merge their lists — <b>a single reviewer finds only a "
          "minority of the problems</b>, and <b>the overlap between "
          "reviewers is surprisingly low</b>, which is the empirical "
          "finding that makes multiple reviewers necessary rather than "
          "merely better.",
          "<b>Walk specific tasks rather than reviewing the interface "
          "as a catalogue</b> — which <b>keeps the review grounded in "
          "what somebody would actually be trying to accomplish</b> and "
          "avoids a list of decontextualised nitpicks.",
          "<b>Record the violated principle and its mechanism</b> for "
          "each finding (&sect;1), <b>so that each one is actionable</b> "
          "and so that a disagreement about it is a disagreement about a "
          "mechanism rather than about taste.",
          "<b>And rate severity as frequency times impact</b>, so that "
          "<b>the list can be prioritised rather than merely "
          "produced</b> — an unprioritised list of forty findings "
          "gets ignored entire.",
          "<b>Then fix the obvious ones and test</b> "
          "(Module 07). <b>The low overlap between reviewers is the "
          "finding that makes three to five necessary</b> — <b>one "
          "reviewer's list is not a subset of the problems</b>, it is a "
          "fairly arbitrary sample of them."]),
 ],
 "resources": [
   ("Nielsen &mdash; Ten Usability Heuristics (free)",
    "https://www.nngroup.com/articles/ten-usability-heuristics/",
    "<b>&sect;1's list in its canonical form</b>, and the one most "
    "reviews are run against."),
   ("Norman &mdash; The Design of Everyday Things, chapters 4 and 7",
    "https://mitpress.mit.edu/9780262525671/",
    "<b>&sect;1's constraints and &sect;2's conflicts</b>, with the "
    "mechanisms developed properly."),
   ("Nielsen & Molich &mdash; Heuristic evaluation of user interfaces "
    "(free)",
    "https://dl.acm.org/doi/10.1145/97243.97281",
    "<b>&sect;4 in the original</b> — including the measured overlap "
    "between reviewers, which is the key number."),
   ("Thaler & Sunstein, and the default-effect literature",
    "https://web.archive.org/web/20260923132501/https://yalebooks.yale.edu/book/9780300122237/nudge/",
    "<b>&sect;3's effect outside software</b> — where the "
    "default-dominance finding was established."),
 ],
 "exercises": [
   "<b>For each of the seven principles</b>, state the mechanism "
   "without looking.",
   "<b>Find a case where consistency is wrong</b>, and justify breaking "
   "it from the mechanism.",
   "<b>Find each of the four conflicts</b> in an interface you use.",
   "<b>Resolve one of them</b> and say what you gave up.",
   "<b>List every default in your own software</b> and say whether it is "
   "the common case or the safe one.",
   "<b>Find a destructive default</b> somewhere and propose the "
   "change.",
   "<b>Instrument one default</b> and measure the change rate.",
   "<b>Run a heuristic review</b> of an interface, alone.",
   "<b>Have two other people do it independently</b> and measure the "
   "overlap.",
   "<b>Rate the merged findings by frequency times impact.</b>",
 ],
 "selfcheck": [
   "Name seven principles and the mechanism behind each.",
   "Why does stating the mechanism matter?",
   "How does a mechanism tell you the exception?",
   "Name four conflicts and which has a clean resolution.",
   "Why is the default the design?",
   "Why do three courses converge on defaults?",
   "Give five rules for choosing defaults.",
   "What is the cheapest evidence you chose a default wrong?",
   "What does heuristic review find, and what can it not find?",
   "Why are three to five reviewers necessary?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Prototyping",
 "subtitle": "Building the cheapest thing that answers the question.",
 "question": "What fidelity do you need?",
 "outcomes": [
     "Explain why low fidelity gets better feedback.",
     "Choose fidelity from the question being asked.",
     "Explain Wizard of Oz and when it is the right "
     "method.",
     "Explain what prototypes cannot test.",
     "Prototype at the right level for a stated question.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why low fidelity",
   "blurb": "A result about people, not about effort."},

  {"t": "callout", "title": "People critique a sketch and defer to a polished mock-up",
   "kind": "The finding that makes paper worth using",
   "body": ["<b>A hand-drawn prototype invites criticism</b> — it "
            "visibly cost nothing, so saying it is wrong costs the "
            "reviewer nothing either.",
            "<b>A polished one invites approval.</b> <b>It visibly "
            "took effort, and the feedback shifts toward colours and "
            "wording and away from whether the approach is "
            "right</b> — which is the feedback you needed.",
            "<b>And you are more willing to discard it</b>, which "
            "matters because <b>the sunk cost of a built prototype "
            "distorts your own judgement</b> as much as the "
            "reviewer's.",
            "<b>So the fidelity is a choice about what feedback you "
            "will get</b> — <b>not a budget constraint</b> — and "
            "low fidelity early is a method rather than a "
            "compromise."]},

  {"t": "section", "label": "Part 2", "title": "Choosing fidelity",
   "blurb": "From the question, in three dimensions."},

  {"t": "code", "kicker": "Fidelity", "title": "Three dimensions, varied independently",
   "lang": "text", "code": """
  VISUAL FIDELITY    how finished it looks
  FUNCTIONAL BREADTH how many features exist
  FUNCTIONAL DEPTH   how completely any one works

  AND YOU VARY THEM INDEPENDENTLY, which is the point:

  "Is the conceptual model right?"
      -> low visual, broad, no depth. A paper
         walkthrough of every screen.

  "Can people complete this task?"
      -> low visual, narrow, full depth. One path,
         working, ugly.

  "Does it feel responsive enough?"
      -> high visual, narrow, full depth, real
         timing. Nothing else matters.

  "Will people want it?"
      -> a prototype cannot answer this (Part 4).

  SO: name the question first, then build the least
  thing that answers it.
""",
   "caption": "<b>Name the question first, then build the least thing "
              "that answers it</b> — which is the whole method.",
   "note": "The three independent dimensions are what make this a "
           "method rather than a spectrum."},

  {"t": "callout", "title": "The commonest prototyping error is uniform fidelity",
   "kind": "What the three dimensions prevent",
   "body": ["<b>A prototype built to a uniform level of polish spends "
            "effort on the parts that are not in question</b> — "
            "which is most of the effort, and it buys nothing.",
            "<b>So deliberately leave things broken.</b> <b>A "
            "prototype with one working path and nine dead links tests "
            "the path, and the dead links cost nothing</b> provided the "
            "participant is told.",
            "<b>And conversely, do not under-build the thing in "
            "question.</b> <b>A latency question needs real latency; a "
            "typography question needs real type</b> — and a sketch "
            "cannot answer either.",
            "<b>Which is why the question has to come "
            "first</b> — <b>a prototype built before the question is "
            "named will be uniformly polished and will answer nothing in "
            "particular.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Wizard of Oz",
   "blurb": "Testing something you have not built."},

  {"t": "callout", "title": "A person behind the curtain lets you test an interaction before the system exists",
   "kind": "The method, and where it is uniquely useful",
   "body": ["<b>A human performs the system's function while the "
            "participant believes it is automated</b> — which tests "
            "the <i>interaction</i> without requiring the <i>capability</i> "
            "to exist.",
            "<b>Which is uniquely valuable for anything "
            "expensive:</b> <b>a speech interface, a recommendation, a "
            "generated response, or an automation</b> — all of which "
            "cost a great deal to build and may be the wrong "
            "design.",
            "<b>And it answers questions the built system "
            "cannot:</b> <b>what do people say to it, what do they "
            "expect it to handle, and how do they recover when it "
            "fails?</b> — which you need before choosing what to "
            "build.",
            "<b>With one ethical requirement:</b> <b>debrief "
            "afterwards</b> (Module 08 §4) — the deception "
            "is methodologically necessary and has to be undone."]},

  {"t": "bullets", "kicker": "Wizard", "title": "And how to run it well",
   "items": [
     "<b>Decide the wizard's rules in advance</b>, and follow "
     "them — because <b>a wizard who is cleverer than the real "
     "system would be gives you a misleading "
     "result.</b>",
     "",
     "<b>Include failures deliberately</b>, at the rate the real "
     "system would have — since <b>how people recover is "
     "frequently the design question.</b>",
     "",
     "<b>Record the inputs</b>, because <b>what people actually "
     "say or type is the most valuable output</b> and is your training "
     "and test data later.",
     "",
     "<b>Keep the latency realistic</b>, since response time "
     "changes behaviour substantially.",
     "",
     "<b>And debrief.</b> Always.",
   ],
   "footnote": "<b>'What people actually say to it' is the "
               "finding</b> — and it is routinely different from what "
               "the designers assumed, which is the whole reason to run "
               "this."},

  {"t": "section", "label": "Part 4", "title": "Limits",
   "blurb": "What a prototype cannot tell you."},

  {"t": "bullets", "kicker": "Limits", "title": "The questions prototypes do not answer",
   "items": [
     "<b>Whether people want it.</b> <b>A participant in a room "
     "will engage with anything</b>, and expressed interest predicts "
     "adoption poorly.",
     "",
     "<b>Long-term behaviour.</b> <b>Learnability, habituation, "
     "and whether the novelty wears off</b> all require time a "
     "prototype session does not have.",
     "",
     "<b>Performance at scale</b>, and anything depending on real "
     "data volume, real content, or real other users.",
     "",
     "<b>And social dynamics</b> — how a feature behaves when "
     "other people can see what you did with it.",
     "",
     "<b>So state what your prototype tested</b> and what it "
     "could not, which is Module 13 §2.",
   ],
   "footnote": "<b>Expressed interest predicts adoption "
               "poorly</b> — which is why 'would you use this' is "
               "nearly worthless as a question and 'show me how you do "
               "this now' is not."},

  {"t": "callout", "title": "And the discipline this module asks for",
   "kind": "Closing",
   "body": ["<b>Write the question before you build anything</b>, in "
            "one sentence — and <b>if you cannot, you are not ready "
            "to prototype.</b>",
            "<b>Build the least thing that answers it</b>, varying "
            "the three dimensions independently "
            "(Part 2).",
            "<b>Then test it with people</b> "
            "(Module 07) — <b>because a prototype nobody used is "
            "a drawing.</b>",
            "<b>And throw it away.</b> <b>A prototype that becomes "
            "the implementation carries every shortcut you took "
            "deliberately</b> — which is a real and common cost, and "
            "is worth naming before it happens."]},
 ],
 "takeaways": [
   "People critique a sketch and defer to a polished mock-up, so fidelity "
   "is a choice about what feedback you get.",
   "Visual fidelity, functional breadth, and functional depth vary "
   "independently, which is what makes this a method.",
   "The commonest prototyping error is uniform fidelity, which spends "
   "effort on the parts not in question.",
   "Wizard of Oz tests the interaction without requiring the capability, "
   "and what people actually say to it is the finding.",
   "Expressed interest predicts adoption poorly, so 'would you use this' "
   "is nearly worthless as a question.",
   "A prototype that becomes the implementation carries every shortcut you "
   "took deliberately.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why low fidelity"),
  ("callout", "People critique a sketch and defer to a polished mock-up",
   ["<b>A hand-drawn prototype invites criticism</b> — <b>it "
    "visibly cost nothing to produce, so saying it is wrong costs the "
    "reviewer nothing either</b>, socially or otherwise.",
    "<b>A polished one invites approval.</b> <b>It visibly took "
    "considerable effort, and the feedback shifts toward colours, "
    "wording, and alignment and away from whether the whole approach is "
    "right</b> — <b>which is precisely the feedback you needed and "
    "the only kind that is still cheap to act on.</b>",
    "<b>And you are more willing to discard a sketch</b>, which "
    "matters because <b>the sunk cost of a built prototype distorts your "
    "own judgement</b> at least as much as the reviewer's — and "
    "yours is the judgement that decides.",
    "<b>So the fidelity is a choice about what feedback you will "
    "get</b> — <b>not a budget constraint</b> — and <b>low "
    "fidelity early is a method rather than a compromise</b>, which is "
    "the reframing this module asks for."]),

  ("h1", "2 &nbsp; Choosing fidelity"),
  ("code", """VISUAL FIDELITY    how finished it looks
FUNCTIONAL BREADTH how many features exist at all
FUNCTIONAL DEPTH   how completely any one of them
                   works

AND YOU VARY THEM INDEPENDENTLY, which is the point:

"Is the conceptual model right?"
    -> low visual, broad, no depth. A paper
       walkthrough of every screen, nothing working.

"Can people complete this task?"
    -> low visual, narrow, full depth. One path,
       genuinely working, and ugly.

"Does it feel responsive enough?"
    -> high visual, narrow, full depth, with real
       timing. Nothing else matters for this
       question.

"Will people want it?"
    -> a prototype cannot answer this (section 4).

SO: name the question first, then build the least
thing that answers it."""),
  ("callout", "The commonest prototyping error is uniform fidelity",
   ["<b>A prototype built to a uniform level of polish spends effort on "
    "the parts that are not in question</b> — <b>which is most of "
    "the effort, and it buys nothing</b> except a longer delay before you "
    "learn anything.",
    "<b>So deliberately leave things broken.</b> <b>A prototype with "
    "one working path and nine dead links tests the path perfectly well, "
    "and the dead links cost nothing</b> provided the participant is told "
    "in advance which parts are not built.",
    "<b>And conversely, do not under-build the thing that <i>is</i> in "
    "question.</b> <b>A latency question needs real latency; a "
    "typography question needs real type; a density question needs real "
    "content</b> — and a sketch cannot answer any of them, so a "
    "sketch is the wrong tool there.",
    "<b>Which is why the question has to come first</b> — <b>a "
    "prototype built before the question is named will be uniformly "
    "polished and will answer nothing in particular</b>, which describes "
    "a great many prototypes and explains why their reviews are "
    "unsatisfying."]),

  ("break",),
  ("h1", "3 &nbsp; Wizard of Oz"),
  ("callout", "A person behind the curtain lets you test an interaction "
              "before the system exists",
   ["<b>A human performs the system's function while the participant "
    "believes it is automated</b> — which <b>tests the "
    "<i>interaction</i> without requiring the <i>capability</i> to "
    "exist</b>, and is the only method in this course that can do "
    "that.",
    "<b>Which makes it uniquely valuable for anything expensive to "
    "build:</b> <b>a speech interface, a recommendation system, a "
    "generated response, or an automation</b> — all of which cost a "
    "great deal and <b>may turn out to be the wrong design</b>, which is "
    "an expensive thing to discover afterwards.",
    "<b>And it answers questions the built system cannot:</b> <b>what "
    "do people actually say to it, what do they expect it to handle, and "
    "how do they recover when it fails?</b> — <b>all of which you "
    "need before choosing what to build</b>, and none of which you can "
    "find out from a specification.",
    "<b>With one ethical requirement:</b> <b>debrief "
    "afterwards</b> (Module 08 &sect;4's ethics) — <b>the "
    "deception is methodologically necessary and has to be undone</b>, "
    "explicitly and before the participant leaves."]),
  ("ul", ["<b>Decide the wizard's rules in advance</b>, and follow "
          "them — because <b>a wizard who is cleverer than the real "
          "system could ever be gives you a misleading result</b>, and the "
          "temptation to be helpful is strong when a participant is "
          "struggling.",
          "<b>Include failures deliberately</b>, at approximately the "
          "rate the real system would have — since <b>how people "
          "recover from a failure is frequently the actual design "
          "question</b>, and a flawless wizard tests nothing about "
          "it.",
          "<b>Record the inputs</b>, because <b>what people actually "
          "say or type is the most valuable output of the whole "
          "exercise</b> — it is your training and test data later, "
          "and it is unobtainable any other way.",
          "<b>Keep the latency realistic</b>, since <b>response time "
          "changes behaviour substantially</b> — a wizard who "
          "responds instantly produces interaction patterns the real "
          "system will not see.",
          "<b>And debrief. Always.</b> <b>'What people actually say "
          "to it' is the finding</b>, and <b>it is routinely quite "
          "different from what the designers assumed</b> — which is "
          "the whole reason to run the study and the thing to write "
          "down first."]),

  ("h1", "4 &nbsp; Limits"),
  ("ul", ["<b>Whether people want it.</b> <b>A participant in a room "
          "will engage politely with almost anything</b>, and "
          "<b>expressed interest predicts actual adoption poorly</b> "
          "— which is a robust finding and a persistent "
          "temptation.",
          "<b>Long-term behaviour.</b> <b>Learnability over weeks, "
          "habituation, and whether the novelty wears off</b> all require "
          "time that a single prototype session does not have, and all of "
          "them can reverse a short-term result.",
          "<b>Performance at scale</b>, and anything depending on real "
          "data volume, real content quality, or the presence of real "
          "other users — a prototype's clean sample data hides a "
          "great deal.",
          "<b>And social dynamics</b> — how a feature behaves when "
          "other people can see what you did with it, which changes "
          "behaviour fundamentally and cannot be simulated in a room.",
          "<b>So state what your prototype tested and what it could "
          "not</b>, which is Module 13 &sect;2's requirement. "
          "<b>Expressed interest predicts adoption poorly</b> — "
          "which is why <b>'would you use this' is nearly worthless as a "
          "question</b> and <b>'show me how you do this now' is not</b>: "
          "the second asks about behaviour that already exists."]),
  ("callout", "And the discipline this module asks for",
   ["<b>Write the question before you build anything</b>, in a single "
    "sentence — and <b>if you cannot write it, you are not ready to "
    "prototype</b>, which is a useful and uncomfortable test.",
    "<b>Build the least thing that answers it</b>, varying the three "
    "dimensions independently (&sect;2) and <b>deliberately leaving the "
    "rest broken.</b>",
    "<b>Then test it with people</b> (Module 07) — <b>because "
    "a prototype nobody used is a drawing</b>, and a drawing you "
    "evaluated yourself is subject to Module 01 &sect;2 in full.",
    "<b>And throw it away.</b> <b>A prototype that becomes the "
    "implementation carries every shortcut you took deliberately</b> "
    "— the hardcoded values, the missing error handling, the one "
    "working path — <b>which is a real and very common cost, and is "
    "worth naming before it happens</b> rather than discovering it two "
    "years later (CSCE 606's technical debt, acquired on "
    "purpose)."]),
 ],
 "resources": [
   ("Buxton &mdash; Sketching User Experiences",
    "https://www.elsevier.com/books/sketching-user-experiences/buxton/978-0-12-374037-3",
    "<b>&sect;1's argument at length</b> — why sketching and "
    "prototyping are different activities. Library copy."),
   ("Snyder &mdash; Paper Prototyping",
    "https://www.elsevier.com/books/paper-prototyping/snyder/978-1-55860-870-2",
    "<b>&sect;1 and &sect;2 practically</b> — how to run a paper "
    "prototype session, in detail. Library copy."),
   ("Dahlb&auml;ck, J&ouml;nsson & Ahrenberg &mdash; Wizard of Oz "
    "studies (free)",
    "https://dl.acm.org/doi/10.1145/169891.169968",
    "<b>&sect;3's method and its pitfalls</b> — including the "
    "wizard-is-too-clever problem."),
   ("Nielsen Norman Group on prototyping fidelity (free)",
    "https://www.nngroup.com/articles/ux-prototype-hi-lo-fidelity/",
    "<b>&sect;2's decision, practically</b> — and the independent "
    "dimensions made explicit."),
 ],
 "exercises": [
   "<b>Sketch an interface on paper</b> and show it to three people.",
   "<b>Build the same thing polished</b> and show it to three "
   "others.",
   "<b>Compare the feedback</b> and classify it as structural or "
   "cosmetic.",
   "<b>Write four design questions</b> and specify the fidelity each "
   "needs on all three dimensions.",
   "<b>Build one of them</b> and deliberately leave the rest "
   "broken.",
   "<b>Run a Wizard of Oz study</b> for an interaction you have not "
   "built.",
   "<b>Record every input</b> and compare against what you expected "
   "people to say.",
   "<b>Include deliberate failures</b> and observe the recovery.",
   "<b>Ask 'would you use this' and 'show me how you do this now'</b>, "
   "and compare what you learn.",
   "<b>List what your prototype could not test.</b>",
 ],
 "selfcheck": [
   "Why do people critique a sketch and defer to a mock-up?",
   "Why is fidelity a choice about feedback rather than budget?",
   "Name the three dimensions of fidelity.",
   "Give the right fidelity for three different questions.",
   "What is the commonest prototyping error, and what prevents it?",
   "What does Wizard of Oz test that a built system cannot?",
   "Give five rules for running one, and the ethical requirement.",
   "Name four things a prototype cannot answer.",
   "Why is 'would you use this' nearly worthless?",
   "Why throw the prototype away?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Usability Testing",
 "subtitle": "The method that makes this subject empirical.",
 "question": "What happens when somebody actually tries it?",
 "outcomes": [
     "Run a think-aloud usability test.",
     "Explain why five participants is the right number.",
     "Write tasks that do not give away the answer.",
     "Avoid the ways a facilitator corrupts a session.",
     "Analyse a session into mechanisms and severities.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The method",
   "blurb": "Which is almost embarrassingly simple."},

  {"t": "code", "kicker": "Method", "title": "A usability test, in full",
   "lang": "text", "code": """
  1. WRITE 3-5 TASKS a real user would want to do,
     phrased as goals and not as instructions
     (Part 3).

  2. SIT SOMEBODY DOWN and ask them to attempt the
     first task, thinking aloud as they go.

  3. DO NOT HELP. This is the hard part and the whole
     method.

  4. WATCH AND NOTE: where they hesitate, what they
     try, what they expect, what they say, and where
     they succeed or give up.

  5. REPEAT with four more people.

  6. ANALYSE: every failure attributed to a mechanism
     (Module 01 Part 1) and rated by severity.

  THAT IS ALL. It takes a day, needs no equipment, and
  it is the only reliable source of information in
  this course (Module 01 section 2).
""",
   "caption": "<b>It takes a day and needs no equipment</b> — "
              "which means the barrier to doing it is willingness rather "
              "than resources.",
   "note": "Emphasise the cheapness; the barrier is social, not "
           "technical."},

  {"t": "callout", "title": "Not helping is the whole method, and it is genuinely difficult",
   "kind": "The discipline the facilitator needs",
   "body": ["<b>Watching somebody struggle with something you built "
            "is uncomfortable</b> — and <b>every hint you give "
            "destroys the data you came for.</b>",
            "<b>So the responses are scripted:</b> <b>'what do you "
            "think you should do?', 'what did you expect to happen?', "
            "and silence</b> — which is the most useful of the "
            "three.",
            "<b>And the participant has to be told it is not a test "
            "of them</b>, repeatedly, because <b>they will apologise "
            "for your design's failures</b> and that discomfort "
            "suppresses what they say.",
            "<b>Which means the facilitator's job is to be boring and "
            "patient</b> — <b>and the commonest failure of a first "
            "study is a facilitator who could not stop "
            "helping.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Five participants",
   "blurb": "Why that number, and when it is wrong."},

  {"t": "callout", "title": "Five participants find most of the problems, because the problems are not independent",
   "kind": "The argument, and its limits",
   "body": ["<b>If each participant has roughly a one-in-three chance "
            "of hitting any given problem, five participants find a "
            "large majority of them</b> — which is the standard "
            "argument and is approximately right.",
            "<b>And the returns diminish sharply:</b> <b>the sixth "
            "participant mostly reproduces what the first five "
            "showed</b>, so the marginal information is low and the "
            "marginal cost is not.",
            "<b>So the efficient strategy is many small "
            "studies:</b> <b>five people, fix, five more</b> — "
            "rather than one study of twenty, which finds the same "
            "problems five times.",
            "<b>But the argument fails for distinct user "
            "populations:</b> <b>five of one group does not cover "
            "another</b> — so <b>five <i>per population</i></b>, which "
            "is CSCE 632's point and is where the number "
            "grows."]},

  {"t": "bullets", "kicker": "Limits", "title": "And where five is not enough",
   "items": [
     "<b>Distinct populations</b> — novices and experts, or "
     "different accessibility needs, encounter different problems "
     "entirely (CSCE 632).",
     "",
     "<b>Rare but severe problems</b>, which five people will "
     "probably miss — and which heuristic review "
     "(Module 05 §4) may catch instead.",
     "",
     "<b>Any quantitative claim.</b> <b>Five participants cannot "
     "support a claim about a rate or a mean</b>, which is "
     "Module 08's territory.",
     "",
     "<b>And comparison between two designs</b>, which needs "
     "more people or a within-subject design "
     "(Module 08 §2).",
     "",
     "<b>So five is right for finding problems and wrong for "
     "measuring anything.</b>",
   ],
   "footnote": "<b>Five is right for finding problems and wrong for "
               "measuring anything</b> — which is the distinction "
               "that keeps this method honest "
               "(Module 13)."},

  {"t": "section", "label": "Part 3", "title": "Tasks",
   "blurb": "Where a study is most easily ruined."},

  {"t": "bullets", "kicker": "Tasks", "title": "Writing tasks that test something",
   "items": [
     "<b>Phrase as a goal, not an instruction.</b> <b>'Find out "
     "how much you have spent this month' tests the design; 'click the "
     "Reports tab' tests nothing.</b>",
     "",
     "<b>Avoid the interface's own vocabulary</b>, because <b>using "
     "the label gives away the answer</b> — which is the single "
     "commonest way a task is ruined.",
     "",
     "<b>Make it realistic and specific</b>, with the context a "
     "real user would have — a task with no motivation produces "
     "aimless behaviour.",
     "",
     "<b>Ensure it is actually completable</b>, and know the "
     "intended path before you start.",
     "",
     "<b>And order them so an early task does not teach the "
     "later ones</b>, or accept that it will and account for "
     "it.",
   ],
   "footnote": "<b>Using the interface's own label in the task is the "
               "commonest way to ruin a study</b> — the participant "
               "then searches for the word rather than for the "
               "function."},

  {"t": "section", "label": "Part 4", "title": "Analysis",
   "blurb": "Turning observations into actions."},

  {"t": "callout", "title": "Attribute every failure to a mechanism, then rate it by frequency times impact",
   "kind": "The analysis that produces decisions",
   "body": ["<b>A list of things that went wrong is not "
            "actionable.</b> <b>A list attributed to "
            "Module 01 §1's six mechanisms is</b>, because each "
            "mechanism has a known family of fixes.",
            "<b>And rate severity as frequency times "
            "impact:</b> <b>a problem four of five people hit that "
            "stops the task outranks one person's cosmetic "
            "complaint</b>, however articulately expressed.",
            "<b>Beware of over-weighting what participants "
            "<i>said</i></b> — <b>what they did is the data and what "
            "they said is a hypothesis about it</b>, which is "
            "Module 09 §3's distinction.",
            "<b>And report the things you expected to fail and did "
            "not</b> — <b>because a study that confirmed everything "
            "you believed was probably run badly</b> "
            "(Project 1)."]},

  {"t": "bullets", "kicker": "Practice", "title": "And the habits that make it stick",
   "items": [
     "<b>Test early, when changing things is cheap</b> — a "
     "study on a finished product finds problems nobody will "
     "fix.",
     "",
     "<b>Have the people who will fix it watch</b>, because "
     "<b>watching one person struggle is more persuasive than any "
     "report</b> of the same session.",
     "",
     "<b>Keep it small and frequent</b>, which is "
     "Part 2's argument.",
     "",
     "<b>Fix something before the next round</b>, so that the "
     "studies compound.",
     "",
     "<b>And write down what you looked for and did not "
     "find</b>, which is what makes the claim checkable "
     "(Module 13).",
   ],
   "footnote": "<b>Having the implementers watch is the intervention "
               "that changes organisations</b> — a written finding is "
               "arguable and a recording of somebody failing is "
               "not."},
 ],
 "takeaways": [
   "A usability test takes a day and needs no equipment, so the barrier to "
   "doing it is willingness rather than resources.",
   "Not helping is the whole method, and the commonest failure of a first "
   "study is a facilitator who could not stop.",
   "Five participants find most problems because the problems are not "
   "independent, and the sixth mostly reproduces the first five.",
   "Five is right for finding problems and wrong for measuring anything, "
   "which is the distinction that keeps the method honest.",
   "Using the interface's own label in the task is the commonest way to "
   "ruin a study.",
   "What they did is the data and what they said is a hypothesis about it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The method"),
  ("code", """1. WRITE 3-5 TASKS a real user would want to do,
   phrased as goals and not as instructions
   (section 3).

2. SIT SOMEBODY DOWN and ask them to attempt the
   first task, thinking aloud as they go.

3. DO NOT HELP. This is the hard part and it is the
   whole method.

4. WATCH AND NOTE: where they hesitate, what they
   try, what they expected to happen, what they say,
   and whether they succeed or give up.

5. REPEAT with four more people.

6. ANALYSE: every failure attributed to a mechanism
   (Module 01 section 1) and rated by severity.

THAT IS ALL. It takes a day, needs no equipment, and
it is the only reliable source of information in this
course (Module 01 section 2)."""),
  ("callout", "Not helping is the whole method, and it is genuinely "
              "difficult",
   ["<b>Watching somebody struggle with something you built is "
    "uncomfortable</b> — and <b>every hint you give destroys the "
    "data you came for</b>, because after the hint you are observing a "
    "person who has been told the answer.",
    "<b>So the facilitator's responses are scripted in "
    "advance:</b> <b>'what do you think you should do?', 'what did you "
    "expect to happen?', and silence</b> — <b>which is the most "
    "useful of the three</b> and the hardest to maintain.",
    "<b>And the participant has to be told that it is not a test of "
    "them</b>, repeatedly and at the start of each task, because "
    "<b>they will apologise for your design's failures</b> — and "
    "<b>that discomfort suppresses what they say</b>, which is the "
    "material you are there for.",
    "<b>Which means the facilitator's job is to be boring and "
    "patient</b> — and <b>the commonest failure of a first study is "
    "a facilitator who could not stop helping</b>, which produces a "
    "pleasant session and no findings."]),

  ("h1", "2 &nbsp; Five participants"),
  ("callout", "Five participants find most of the problems, because the "
              "problems are not independent",
   ["<b>If each participant has roughly a one-in-three chance of "
    "encountering any given problem, then five participants find a large "
    "majority of the problems present</b> — which is the standard "
    "argument, rests on an assumed detection rate, and is approximately "
    "right in practice.",
    "<b>And the returns diminish sharply:</b> <b>the sixth "
    "participant mostly reproduces what the first five already "
    "showed</b> — so <b>the marginal information is low and the "
    "marginal cost is not</b>, which is the actual argument for "
    "stopping.",
    "<b>So the efficient strategy is many small studies:</b> <b>five "
    "people, fix what you found, five more</b> — <b>rather than one "
    "study of twenty, which finds the same problems five times</b> and "
    "delays every fix until the end.",
    "<b>But the argument fails for genuinely distinct user "
    "populations:</b> <b>five participants from one group does not "
    "cover another</b> — so it is <b>five <i>per population</i></b>, "
    "<b>which is CSCE 632's point</b> and is where the number grows "
    "legitimately rather than by excessive caution."]),
  ("ul", ["<b>Distinct populations</b> — novices and experts, or "
          "people with different accessibility needs, <b>encounter "
          "entirely different problems</b> (CSCE 632) — so "
          "sampling one tells you nothing about the other.",
          "<b>Rare but severe problems</b>, which <b>five people will "
          "probably miss</b> — and which <b>heuristic review</b> "
          "(Module 05 &sect;4) <b>may catch instead</b>, which is one "
          "of the better arguments for running both methods.",
          "<b>Any quantitative claim.</b> <b>Five participants cannot "
          "support a claim about a rate, a mean, or a difference</b>, "
          "which is <b>Module 08's territory</b> and requires a "
          "different design and a larger sample.",
          "<b>And comparison between two designs</b>, which needs "
          "either more participants or a within-subject design with "
          "counterbalancing (Module 08 &sect;2).",
          "<b>So five is right for finding problems and wrong for "
          "measuring anything</b> — <b>which is the distinction that "
          "keeps this method honest</b> and is exactly what Module 13 "
          "asks you to state when reporting it."]),

  ("break",),
  ("h1", "3 &nbsp; Tasks"),
  ("ul", ["<b>Phrase the task as a goal, not an "
          "instruction.</b> <b>'Find out how much you have spent this "
          "month' tests the design; 'click the Reports tab and then "
          "select Monthly' tests nothing at all</b> except whether they "
          "can follow instructions.",
          "<b>Avoid the interface's own vocabulary</b>, because "
          "<b>using the label gives away the answer</b> — <b>which "
          "is the single commonest way a task is ruined</b>: the "
          "participant then searches for the word rather than for the "
          "function, and you learn nothing about whether the word was "
          "findable.",
          "<b>Make it realistic and specific, with the context a "
          "real user would have</b> — <b>a task with no motivation "
          "produces aimless behaviour</b>, and a participant who does not "
          "care about the outcome gives up differently than a real user "
          "would.",
          "<b>Ensure it is actually completable</b>, and <b>know the "
          "intended path before you start</b> — discovering "
          "mid-session that the task cannot be done wastes the "
          "participant and the slot.",
          "<b>And order the tasks so that an early one does not teach "
          "the later ones</b>, or <b>accept that it will and account for "
          "it in the analysis</b> — which is Module 08 &sect;2's "
          "ordering effect appearing in a qualitative method."]),

  ("h1", "4 &nbsp; Analysis"),
  ("callout", "Attribute every failure to a mechanism, then rate it by "
              "frequency times impact",
   ["<b>A list of things that went wrong is not actionable.</b> <b>A "
    "list attributed to Module 01 &sect;1's six mechanisms is</b>, "
    "<b>because each mechanism has a known family of fixes</b> — "
    "which is why that vocabulary was introduced in the first module and "
    "why Project 1 grades the attribution.",
    "<b>And rate severity as frequency times impact:</b> <b>a problem "
    "that four of five people hit and that stops the task outranks one "
    "person's cosmetic complaint</b>, <b>however articulately "
    "expressed</b> — and articulate complaints are "
    "over-weighted systematically.",
    "<b>Beware of over-weighting what participants <i>said</i></b> "
    "— <b>what they did is the data and what they said is a "
    "hypothesis about it</b>, which is <b>Module 09 &sect;3's "
    "distinction</b> and the single most important analytical discipline "
    "here.",
    "<b>And report the things you expected to fail and which did "
    "not</b> — <b>because a study that confirmed everything you "
    "already believed was probably run badly</b>, or analysed "
    "selectively (Project 1's fifth requirement)."]),
  ("ul", ["<b>Test early, when changing things is still cheap</b> "
          "— <b>a study on a finished product finds problems nobody "
          "will fix</b>, which wastes the study and discredits the "
          "method.",
          "<b>Have the people who will do the fixing watch the "
          "sessions</b>, because <b>watching one person struggle is more "
          "persuasive than any written report</b> of the same "
          "session — and the persuasion is what gets the fix "
          "scheduled.",
          "<b>Keep the studies small and frequent</b>, which is "
          "&sect;2's argument and makes the method sustainable rather "
          "than an event.",
          "<b>Fix something before the next round</b>, so that the "
          "studies compound rather than each one producing an independent "
          "list.",
          "<b>And write down what you looked for and did not find</b>, "
          "<b>which is what makes the claim checkable</b> "
          "(Module 13 &sect;2, and CSCE 713 Module 11 "
          "&sect;4's recording requirement). <b>Having the implementers "
          "watch is the intervention that changes organisations</b> "
          "— <b>a written finding is arguable and a recording of "
          "somebody failing is not.</b>"]),
 ],
 "resources": [
   ("Krug &mdash; Rocket Surgery Made Easy",
    "https://sensible.com/rocket-surgery-made-easy/",
    "<b>The whole module, practically</b> — the cheapest possible "
    "version of the method, argued for convincingly. Library copy."),
   ("Nielsen &mdash; Why You Only Need to Test with 5 Users (free)",
    "https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/",
    "<b>&sect;2's argument in its canonical form</b> — read it with "
    "the critiques, which are also linked there."),
   ("Dumas & Redish &mdash; A Practical Guide to Usability Testing",
    "https://www.intellectbooks.com/a-practical-guide-to-usability-testing",
    "<b>&sect;1, &sect;3, and &sect;4 thoroughly</b> — the task "
    "writing and the facilitation in detail. Library copy."),
   ("Nielsen Norman Group on think-aloud protocols (free)",
    "https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/",
    "<b>&sect;1's protocol</b>, with the facilitator scripts and the "
    "common mistakes."),
 ],
 "exercises": [
   "<b>Write five tasks</b> for an interface, phrased as goals.",
   "<b>Check each for the interface's own vocabulary</b> and rewrite "
   "any that leak it.",
   "<b>Run one session</b> and count how many times you wanted to "
   "help.",
   "<b>Run it again without helping</b> and compare what you "
   "learned.",
   "<b>Run five sessions</b> and record every failure.",
   "<b>Count how many new problems each participant added.</b>",
   "<b>Attribute every failure</b> to one of the six mechanisms.",
   "<b>Rate them by frequency times impact</b> and pick the top "
   "three.",
   "<b>Separate what participants did from what they said</b>, and note "
   "where they disagreed.",
   "<b>Have somebody who will fix it watch a session</b>, and record "
   "what changed afterwards.",
 ],
 "selfcheck": [
   "Give the six steps of a usability test.",
   "Why is not helping the whole method, and what are the three scripted "
   "responses?",
   "Why does a participant apologise, and what does it cost you?",
   "Give the five-participant argument and why returns diminish.",
   "Name four cases where five is not enough.",
   "What is five right for, and wrong for?",
   "Give five rules for writing tasks.",
   "What is the commonest way to ruin a study?",
   "How do you analyse a session into actions?",
   "Why report the things that did not fail?",
 ],
},

]
