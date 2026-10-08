# -*- coding: utf-8 -*-
"""CSCE 632 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "The Range",
 "subtitle": "Permanent, temporary, situational — and the same "
             "requirement in all three.",
 "question": "How many people is this, really?",
 "outcomes": [
     "Explain the permanent-temporary-situational framing.",
     "State what is known about prevalence, and its limits.",
     "Describe the assistive technology landscape.",
     "Explain why the population is larger than it appears.",
     "Use the framing to argue for a requirement.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Three durations",
   "blurb": "One design requirement."},

  {"t": "table", "kicker": "Durations", "title": "The same constraint, three ways",
   "header": ["Constraint", "Permanent", "Temporary", "Situational"],
   "widths": [2.6, 2.6, 2.8, 2.8],
   "rows": [
     ["<b>One hand</b>", "<b>Amputation</b>", "<b>Broken arm</b>", "<b>Holding a child</b>"],
     ["<b>Cannot see it</b>", "<b>Blindness</b>", "<b>Dilated pupils</b>", "<b>Bright sunlight; driving</b>"],
     ["<b>Cannot hear it</b>", "<b>Deafness</b>", "<b>Ear infection</b>", "<b>Loud bar; no headphones</b>"],
     ["<b>Cannot speak</b>", "<b>Non-speaking</b>", "<b>Laryngitis</b>", "<b>Quiet office; a meeting</b>"],
     ["<b>Reduced attention</b>", "<b>ADHD</b>", "<b>Concussion</b>", "<b>Exhausted; distracted</b>"],
   ],
   "footnote": "<b>The design requirement is identical across each "
               "row</b> — which is the whole point of the framing, "
               "and is why it persuades people the compliance argument "
               "does not.",
   "note": "This table is the module's single most useful artefact."},

  {"t": "callout", "title": "Which means the situational column is the persuasive one and the permanent column is the obligatory one",
   "kind": "How to use the framing honestly",
   "body": ["<b>The situational cases make the requirement feel "
            "relevant</b> — <b>everybody has tried to use a phone "
            "one-handed in sunlight</b>, and that is a real design "
            "argument rather than a rhetorical trick.",
            "<b>And the permanent cases are why it is "
            "required</b> — <b>a situational constraint is an "
            "inconvenience and a permanent one is exclusion</b>, which "
            "are not the same thing.",
            "<b>So use the situational framing to get agreement and "
            "the permanent one to set the standard</b> — because "
            "<b>the situational case tolerates a workaround and the "
            "permanent one does not.</b>",
            "<b>Which is Module 01 §2's limit "
            "restated:</b> <b>the broad benefit is real and is not the "
            "justification</b>, and conflating them leads to dropping "
            "whatever lacks a mainstream beneficiary."]},

  {"t": "section", "label": "Part 2", "title": "Prevalence",
   "blurb": "What is known, and how uncertain it is."},

  {"t": "bullets", "kicker": "Numbers", "title": "What the figures say, and what they do not",
   "items": [
     "<b>Roughly one person in six lives with a significant "
     "disability</b>, by the usual international estimates — "
     "<b>which makes this the largest minority there is</b>, and it is "
     "one anybody can join.",
     "",
     "<b>But the figure depends entirely on the definition</b> "
     "— <b>self-report, functional assessment, and benefit "
     "eligibility give very different numbers</b>, and the three are "
     "measuring different things.",
     "",
     "<b>And it rises steeply with age</b>, which means <b>the "
     "population is growing wherever the population is "
     "ageing</b> — a demographic fact, not a "
     "projection.",
     "",
     "<b>Plus the undercount:</b> <b>people who have stopped "
     "trying to use an inaccessible system do not appear in its "
     "analytics</b>, which is a survivorship problem "
     "(CSCE 676 §08).",
     "",
     "<b>So the honest claim is 'a large minority, "
     "undercounted'</b> — and <b>the precise number is not the "
     "argument anyway.</b>",
   ],
   "footnote": "<b>People who gave up on an inaccessible system do "
               "not appear in its analytics</b> — so usage data "
               "systematically understates the population being "
               "excluded."},

  {"t": "callout", "title": "And the analytics argument is worth refusing explicitly",
   "kind": "A specific bad argument you will meet",
   "body": ["<b>'Our analytics show almost no screen reader "
            "users'</b> is offered as evidence that the work is not "
            "needed — and <b>it is evidence of the "
            "opposite.</b>",
            "<b>Because the measurement is conditional on being able "
            "to use the product</b> — <b>the excluded are absent from "
            "the data by construction</b>, which is exactly "
            "CSCE 676 §08's survivorship structure.",
            "<b>And screen reader use is frequently not detectable "
            "anyway</b> — <b>for good privacy reasons</b>, so the "
            "absence of a signal is not even weak evidence.",
            "<b>So the correct response is to name the sampling "
            "problem</b>, which is a technical objection rather than an "
            "ethical appeal — and technical objections carry further "
            "in engineering meetings."]},

  {"t": "section", "label": "Part 3", "title": "The technology",
   "blurb": "What is actually between the user and your interface."},

  {"t": "table", "kicker": "Assistive technology", "title": "What people use, and what it needs from you",
   "header": ["Technology", "What it does", "What it needs"],
   "widths": [2.9, 4.0, 4.3],
   "rows": [
     ["<b>Screen reader</b>", "<b>Speaks or brailles the interface</b>", "<b>Correct semantics (M08)</b>"],
     ["<b>Magnifier</b>", "<b>Enlarges a region of the screen</b>", "<b>Reflow; no distant dependencies</b>"],
     ["<b>Switch or scanning input</b>", "<b>One or two inputs, sequentially</b>", "<b>Few steps; no timeouts</b>"],
     ["<b>Voice control</b>", "<b>Operates by spoken command</b>", "<b>Visible, speakable names</b>"],
     ["<b>Alternative keyboards</b>", "<b>Different physical layouts</b>", "<b>Full keyboard operability</b>"],
     ["<b>Captions and transcripts</b>", "<b>Text for audio</b>", "<b>Accurate, synchronised text</b>"],
   ],
   "footnote": "<b>Every one of these consumes your semantics rather "
               "than your pixels</b> — which is why Module 08's "
               "accessibility tree is the mechanism the whole course "
               "depends on.",
   "note": "The semantics-not-pixels point is the bridge to "
           "Module 08."},

  {"t": "section", "label": "Part 4", "title": "Using the framing",
   "blurb": "To argue for a requirement, in practice."},

  {"t": "bullets", "kicker": "Practice", "title": "How to make the case",
   "items": [
     "<b>Name the capability, not the condition</b> "
     "(Module 01 §3) — which keeps it a design "
     "requirement rather than an accommodation "
     "request.",
     "",
     "<b>Give the situational case first</b>, because it is the "
     "one your audience has experienced.",
     "",
     "<b>Then the permanent case</b>, as the reason the "
     "workaround is not sufficient.",
     "",
     "<b>Then the test</b> — <b>which takes minutes and "
     "converts an argument into an observation</b>, and is the move "
     "this whole semester is built on.",
     "",
     "<b>And refuse the analytics argument by naming the "
     "sampling</b> (Part 2), not by appealing to "
     "fairness.",
   ],
   "footnote": "<b>Run the test in the meeting</b> — unplugging a "
               "mouse takes ten seconds and ends the discussion faster "
               "than any argument.",
   "note": "Converting the argument into an observation is the "
           "transferable skill here."},

  {"t": "callout", "title": "And the honest summary",
   "kind": "Closing",
   "body": ["<b>The population is large, undercounted, growing, and "
            "one anybody can join temporarily or "
            "permanently</b> — which is a reasonable thing to say and "
            "does not depend on a precise figure.",
            "<b>And the requirement does not actually depend on the "
            "count</b> — <b>an interface that excludes one user in a "
            "thousand is still defective</b>, and the count is a "
            "prioritisation input rather than a "
            "justification.",
            "<b>Which is worth being clear about</b>, because "
            "<b>arguing from the numbers invites arguing about the "
            "numbers</b>, and that is not the argument you "
            "want.",
            "<b>So the framing's real use is making the requirement "
            "legible</b> — <b>and then the capability test settles "
            "it</b>, which is the pattern for the next four "
            "modules."]},
 ],
 "takeaways": [
   "The same design requirement covers permanent, temporary, and "
   "situational versions of a constraint — which is the framing's "
   "whole point.",
   "Use the situational case to get agreement and the permanent case to set "
   "the standard, because only one of them tolerates a workaround.",
   "Roughly one person in six, but the figure depends entirely on the "
   "definition and is undercounted.",
   "People who gave up on an inaccessible system are absent from its "
   "analytics by construction, so usage data understates the exclusion.",
   "Refuse the analytics argument by naming the sampling problem, which is "
   "a technical objection rather than an ethical appeal.",
   "Every assistive technology consumes your semantics rather than your "
   "pixels.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Three durations"),
  ("table", ["The constraint", "Permanent", "Temporary", "Situational"],
   [["<b>Use of one hand only</b>", "<b>Amputation, hemiplegia</b>",
     "<b>A broken arm, a recent injury</b>",
     "<b>Holding a child, a bag, a handrail</b>"],
    ["<b>Cannot see the screen</b>", "<b>Blindness</b>",
     "<b>Dilated pupils after an eye examination</b>",
     "<b>Bright sunlight, a cracked display, driving</b>"],
    ["<b>Cannot hear the audio</b>", "<b>Deafness</b>",
     "<b>An ear infection</b>",
     "<b>A loud bar, a quiet library, no headphones</b>"],
    ["<b>Cannot speak</b>", "<b>Non-speaking, laryngectomy</b>",
     "<b>Laryngitis</b>",
     "<b>A quiet office, a meeting, a baby asleep</b>"],
    ["<b>Reduced attention or memory</b>",
     "<b>ADHD, some cognitive conditions</b>",
     "<b>Concussion, severe sleep deprivation, grief</b>",
     "<b>Exhausted, distracted, doing three things</b>"]],
   [0.22, 0.24, 0.26, 0.28]),
  ("p", "<b>The design requirement is identical across each row</b> "
        "— <b>which is the whole point of the framing</b>, and <b>is "
        "why it persuades people the compliance argument does not</b>: it "
        "connects the requirement to something the listener has "
        "experienced. <b>This table is the module's single most useful "
        "artefact</b>, and it is worth being able to produce a row of it "
        "for any constraint you are asked to justify."),
  ("callout", "Which means the situational column is the persuasive one and "
              "the permanent column is the obligatory one",
   ["<b>The situational cases make the requirement feel "
    "relevant</b> — <b>everybody has tried to use a phone "
    "one-handed in bright sunlight</b>, and <b>that is a real design "
    "argument rather than a rhetorical trick</b>, because the interface "
    "genuinely does fail in both cases for the same reason.",
    "<b>And the permanent cases are why the requirement is "
    "obligatory</b> — <b>a situational constraint is an "
    "inconvenience and a permanent one is exclusion</b>, <b>which are "
    "not the same thing</b> and should not be presented as though they "
    "were.",
    "<b>So use the situational framing to get agreement and the "
    "permanent one to set the standard</b> — because <b>the "
    "situational case tolerates a workaround ('wait until you are "
    "indoors') and the permanent one does not</b>, and a requirement "
    "argued only from the situational case will be met only to the "
    "situational standard.",
    "<b>Which is Module 01 &sect;2's limit restated</b>: <b>the "
    "broad benefit is real and is not the justification</b>, and "
    "<b>conflating them leads directly to dropping whatever lacks a "
    "mainstream beneficiary</b> — which is most of the screen "
    "reader requirements."]),

  ("h1", "2 &nbsp; Prevalence"),
  ("ul", ["<b>Roughly one person in six lives with a significant "
          "disability</b>, by the usual international "
          "estimates — <b>which makes this the largest minority "
          "there is</b>, and <b>it is one anybody can join</b>, which "
          "no other minority is.",
          "<b>But the figure depends entirely on the "
          "definition</b> — <b>self-report, functional assessment, "
          "and administrative benefit eligibility give very different "
          "numbers</b>, and <b>the three are measuring different "
          "things</b>: identity, capability, and entitlement.",
          "<b>And it rises steeply with age</b>, so <b>the "
          "population is growing wherever the population is "
          "ageing</b> — <b>which is a demographic fact rather than "
          "a projection</b>, and makes this a requirement that becomes "
          "more rather than less relevant over a career.",
          "<b>Plus the undercount:</b> <b>people who have stopped "
          "trying to use an inaccessible system do not appear in its "
          "analytics</b> — which is <b>CSCE 676 Module 08's "
          "survivorship structure</b> operating on your own usage "
          "data.",
          "<b>So the honest claim is 'a large minority, "
          "undercounted'</b> — and <b>the precise number is not "
          "the argument anyway</b> (&sect;4's closing callout)."]),
  ("callout", "And the analytics argument is worth refusing explicitly",
   ["<b>'Our analytics show almost no screen reader users'</b> is "
    "offered, in good faith and frequently, as evidence that the work is "
    "not needed — and <b>it is evidence of the opposite.</b>",
    "<b>Because the measurement is conditional on being able to use "
    "the product</b>: <b>the excluded are absent from the data by "
    "construction</b>, which is <b>exactly CSCE 676 Module 08's "
    "survivorship structure</b> — you are measuring the people who "
    "got through.",
    "<b>And screen reader use is frequently not detectable at "
    "all</b> — <b>for good privacy reasons</b>, since a detectable "
    "assistive technology is a disclosed disability — <b>so the "
    "absence of a signal is not even weak evidence</b> of absence.",
    "<b>So the correct response is to name the sampling "
    "problem</b>, <b>which is a technical objection rather than an "
    "ethical appeal</b> — and <b>technical objections carry "
    "further in engineering meetings</b>, which is a practical fact "
    "worth using."]),

  ("break",),
  ("h1", "3 &nbsp; The technology"),
  ("table", ["Technology", "What it does", "What it needs from your code"],
   [["<b>Screen reader</b>",
     "<b>Speaks the interface, or sends it to a refreshable braille "
     "display.</b>",
     "<b>Correct semantics: name, role, value, state</b> "
     "(Module 08)."],
    ["<b>Screen magnifier</b>",
     "<b>Enlarges a region, so only part of the screen is visible at "
     "once.</b>",
     "<b>Reflow at high zoom, and no dependency between distant parts "
     "of the screen.</b>"],
    ["<b>Switch access and scanning</b>",
     "<b>One or two physical inputs, selecting sequentially from a "
     "moving highlight.</b>",
     "<b>Few steps, no timeouts, and a sensible focus order</b> "
     "(Module 05 &sect;3)."],
    ["<b>Voice control</b>",
     "<b>Operates the interface by spoken command.</b>",
     "<b>Visible, speakable, matching names</b> — the label you "
     "show must be the name it responds to."],
    ["<b>Alternative keyboards and pointers</b>",
     "<b>Different physical layouts, head pointers, eye tracking.</b>",
     "<b>Full keyboard operability, and generous targets.</b>"],
    ["<b>Captions, transcripts, and sign interpretation</b>",
     "<b>Text or signed alternatives for audio content.</b>",
     "<b>Accurate, synchronised text</b> (Module 04)."]],
   [0.23, 0.36, 0.41]),
  ("p", "<b>Every one of these consumes your semantics rather than "
        "your pixels</b> — a screen reader reads a tree of roles and "
        "names, voice control matches spoken words against accessible "
        "names, and switch access walks a focus order — <b>which is "
        "why Module 08's accessibility tree is the mechanism the whole "
        "course depends on</b>. <b>The semantics-not-pixels point is the "
        "bridge to Module 08</b>, and it is the reason a visually "
        "perfect interface can be completely inoperable."),

  ("h1", "4 &nbsp; Using the framing"),
  ("ul", ["<b>Name the capability, not the condition</b> "
          "(Module 01 &sect;3) — <b>which keeps it a design "
          "requirement rather than an accommodation request</b>, and "
          "those are routed through different processes with very "
          "different outcomes.",
          "<b>Give the situational case first</b>, because <b>it is "
          "the one your audience has personally experienced</b> and "
          "therefore the one that gets agreement.",
          "<b>Then the permanent case</b>, <b>as the reason the "
          "workaround is not sufficient</b> — which is where the "
          "standard actually comes from (&sect;1's callout).",
          "<b>Then the test</b> — <b>which takes minutes and "
          "converts an argument into an observation</b>, and <b>is the "
          "move this whole semester is built on</b> (CSCE 671 "
          "Module 13 &sect;4, CSCE 679 Module 13 &sect;4).",
          "<b>And refuse the analytics argument by naming the "
          "sampling</b> (&sect;2), <b>not by appealing to "
          "fairness</b>. <b>Run the test in the meeting</b>: "
          "<b>unplugging a mouse takes ten seconds and ends the "
          "discussion faster than any argument</b> — <b>converting "
          "the argument into an observation is the transferable skill "
          "here.</b>"]),
  ("callout", "And the honest summary",
   ["<b>The population is large, undercounted, growing, and one "
    "anybody can join temporarily or permanently</b> — <b>which is "
    "a reasonable thing to say and does not depend on a precise "
    "figure</b>, and is therefore defensible.",
    "<b>And the requirement does not actually depend on the count at "
    "all</b> — <b>an interface that excludes one user in a thousand "
    "is still defective</b>, and <b>the count is a prioritisation input "
    "rather than a justification.</b>",
    "<b>Which is worth being clear about</b>, because <b>arguing "
    "from the numbers invites arguing about the numbers</b> — and "
    "<b>that is not the argument you want</b>, since the numbers are "
    "genuinely uncertain (&sect;2) and the requirement is not.",
    "<b>So the framing's real use is making the requirement "
    "legible</b> to people who have not thought about it — <b>and "
    "then the capability test settles it</b>, <b>which is the pattern "
    "for the next four modules</b>: a constraint, a requirement, and a "
    "test you can run today."]),
 ],
 "resources": [
   ("Microsoft Inclusive Design (free)",
    "https://inclusive.microsoft.com/",
    "<b>&sect;1's table in its original form</b> — and the version "
    "worth showing to somebody who is not convinced."),
   ("The WHO World Report on Disability (free)",
    "https://www.who.int/publications/i/item/9789241564182",
    "<b>&sect;2's figures</b>, with the definitional problems stated "
    "openly — which is the part to read."),
   ("The WebAIM screen reader user surveys (free)",
    "https://webaim.org/projects/screenreadersurvey/",
    "<b>&sect;3</b> — what people actually use, repeated over many "
    "years, and the only good public data on the question."),
   ("The W3C's How People with Disabilities Use the Web (free)",
    "https://www.w3.org/WAI/people-use-web/",
    "<b>&sect;3 with scenarios</b> — the technologies shown in use "
    "rather than described."),
 ],
 "exercises": [
   "<b>Add three rows to §1's table</b> for constraints it does not "
   "cover.",
   "<b>Take one requirement</b> and write its situational and permanent "
   "arguments separately.",
   "<b>Find three published prevalence figures</b> and account for the "
   "difference.",
   "<b>Write out the survivorship argument</b> against the analytics "
   "claim, in four sentences.",
   "<b>Install a screen reader</b> and complete one real task with "
   "it.",
   "<b>Try your platform's voice control</b> on one of your own "
   "interfaces.",
   "<b>Try switch or scanning access</b>, if your platform offers "
   "it.",
   "<b>Count the steps</b> required for one common task in your "
   "interface.",
   "<b>Check whether your visible labels match your accessible "
   "names.</b>",
   "<b>Make the case for one requirement</b> in four sentences, using "
   "§4's order.",
 ],
 "selfcheck": [
   "Give three rows of the durations table.",
   "Which column persuades, which obligates, and why distinguish them?",
   "What is the approximate prevalence, and why is the figure "
   "uncertain?",
   "Why is the population growing?",
   "State the undercount and its structure.",
   "Why is the analytics argument backwards, and how do you answer it?",
   "Name six assistive technologies and what each needs.",
   "What do they all consume, and what does that imply?",
   "Give the five steps for making the case.",
   "Why should the requirement not be argued from the count?",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Vision",
 "subtitle": "No sight, low sight, and colour — three different "
             "requirements.",
 "question": "What does your interface sound like?",
 "outcomes": [
     "Distinguish the three vision requirements.",
     "Explain the screen reader navigation model.",
     "State the colour and contrast requirements.",
     "Explain magnification, zoom, and reflow.",
     "Test an interface against all three.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Three requirements",
   "blurb": "Which are frequently confused and need different work."},

  {"t": "callout", "title": "No vision, low vision, and colour vision are three separate requirements with different fixes",
   "kind": "The distinction to get right first",
   "body": ["<b>No vision needs a non-visual "
            "representation</b> — <b>correct semantics, so a screen "
            "reader can convey structure, state, and "
            "change</b> (Part 2 and Module 08). <b>Visual "
            "design is irrelevant to it.</b>",
            "<b>Low vision needs the visual design to survive "
            "enlargement</b> — <b>magnification, zoom, reflow, and "
            "contrast</b> (Parts 3 and 4). <b>Semantics help and are "
            "not sufficient.</b>",
            "<b>Colour vision needs redundant encoding</b> — "
            "<b>colour must never be the only channel carrying "
            "information</b> (Part 3), which is a single rule and is "
            "widely broken.",
            "<b>And they are frequently conflated</b> — "
            "<b>'accessible for blind users' is used to mean all "
            "three</b>, and a fix for one does nothing for the others, "
            "which is how interfaces end up half-done."]},

  {"t": "section", "label": "Part 2", "title": "The screen reader model",
   "blurb": "Which you have to understand, not just accommodate."},

  {"t": "code", "kicker": "Navigation", "title": "How a screen reader user actually moves",
   "lang": "text", "code": """
  NOT linearly, usually. The common operations:

      jump by heading       the primary navigation,
                            which is why heading
                            structure IS navigation
      jump by landmark      main, nav, search
      list all links        then filter by typing
      list all headings     to get an outline
      tab through controls  focusable things only
      read continuously     when actually reading
      table navigation      cell by cell, with the
                            row and column headers
                            announced

  WHICH MEANS
      headings are a table of contents, not a font
          size
      a page with one heading has no navigation
      link text must make sense out of context,
          because it is heard out of context
      and "click here" x12 is a list of twelve
          identical items
""",
   "caption": "<b>Heading structure is navigation, not "
              "typography</b> — which is the single most useful "
              "thing to know about how screen readers are actually "
              "used.",
   "note": "Everything in Part 2 follows from the jump-by-heading "
           "operation."},

  {"t": "callout", "title": "And the thing to internalise is that it is a serial channel with a cursor",
   "kind": "Why the mechanism matters",
   "body": ["<b>Sight is parallel:</b> <b>you perceive layout, "
            "grouping, and emphasis simultaneously</b> and then attend "
            "to one part (CSCE 671 §02).",
            "<b>Speech is serial and has a cursor</b> — <b>one "
            "thing at a time, in an order, with a position</b> — so "
            "<b>everything your layout conveys spatially has to be "
            "conveyed some other way.</b>",
            "<b>Which is why grouping has to be semantic</b>: a "
            "visual box around three fields conveys nothing serially, "
            "and <b>a fieldset with a legend does.</b>",
            "<b>And why unannounced change is the characteristic "
            "defect</b> — <b>a visual user sees new content appear and "
            "a serial user does not know it happened</b>, which is "
            "Module 08 §4's live region problem."]},

  {"t": "section", "label": "Part 3", "title": "Colour and contrast",
   "blurb": "Two measurable requirements, and no judgement needed."},

  {"t": "callout", "title": "Colour must never be the only channel carrying information",
   "kind": "The requirement, and it is absolute",
   "body": ["<b>A substantial minority cannot distinguish certain hue "
            "pairs</b> — <b>red and green most commonly, at "
            "roughly one in twelve men and one in two hundred "
            "women</b> — so <b>a red-green status encoding is "
            "unreadable to them.</b>",
            "<b>So pair colour with a second channel</b>: "
            "<b>a shape, an icon, a position, a pattern, or a text "
            "label</b> — and the text label is the most "
            "reliable.",
            "<b>And the quickest test is greyscale</b>: <b>if the "
            "information survives desaturation, the colour was "
            "redundant</b> — which takes one screenshot and one "
            "filter.",
            "<b>Which is CSCE 679 Module 04's "
            "argument</b> — and <b>there it is a perceptual fact and "
            "here it is a requirement</b>, which is the same thing "
            "arriving from two directions."]},

  {"t": "table", "kicker": "Contrast", "title": "The contrast requirements, which are numeric",
   "header": ["What", "Minimum (AA)", "Enhanced (AAA)"],
   "widths": [4.4, 3.2, 3.4],
   "rows": [
     ["<b>Body text</b>", "<b>4.5:1</b>", "<b>7:1</b>"],
     ["<b>Large text (18pt, or 14pt bold)</b>", "<b>3:1</b>", "<b>4.5:1</b>"],
     ["<b>Interface components and their states</b>", "<b>3:1</b>", "<b>—</b>"],
     ["<b>Meaningful graphics and icons</b>", "<b>3:1</b>", "<b>—</b>"],
     ["<b>Decorative content, disabled controls</b>", "<b>No requirement</b>", "<b>—</b>"],
   ],
   "footnote": "<b>These are computed from the relative luminances, "
               "not judged</b> — so a contrast failure is a "
               "measurement rather than an opinion, and that is what "
               "makes it arguable in a design review.",
   "note": "The measured-not-judged property is why contrast "
           "requirements actually get met."},

  {"t": "section", "label": "Part 4", "title": "Magnification and zoom",
   "blurb": "Where most layouts break."},

  {"t": "bullets", "kicker": "Low vision", "title": "What enlargement requires, and what it breaks",
   "items": [
     "<b>Text must reach 200% without loss of content or "
     "function</b> — and <b>400% with reflow into a single "
     "column</b>, which is the criterion that breaks "
     "layouts.",
     "",
     "<b>Reflow means no two-dimensional scrolling</b> — "
     "<b>a magnifier user reading a line that requires horizontal "
     "scrolling loses their place every line</b>, which makes reading "
     "impossible rather than slow.",
     "",
     "<b>And a magnifier shows a small window</b>, so <b>anything "
     "that depends on two distant parts of the screen being seen "
     "together fails</b> — a tooltip far from its trigger, an "
     "error summary at the top.",
     "",
     "<b>Plus text has to be text</b> — <b>text in an image "
     "pixelates and cannot be restyled</b>, which is why that is a "
     "separate criterion.",
     "",
     "<b>And respect the user's font size</b>, which means "
     "relative units rather than fixed pixels.",
   ],
   "footnote": "<b>400% zoom with reflow breaks more layouts than "
               "anything else in this course</b> — and it takes "
               "thirty seconds to check."},

  {"t": "callout", "title": "And the three tests, which take about fifteen minutes together",
   "kind": "Closing",
   "body": ["<b>Turn on the screen reader and complete one task "
            "without looking</b> — which tests the no-vision "
            "requirement and is the one that teaches you most "
            "(Part 2).",
            "<b>Set the browser to 400% and check reflow</b>, then "
            "turn on operating system magnification and look for distant "
            "dependencies (Part 4).",
            "<b>Run the contrast checker and the greyscale "
            "filter</b> (Part 3) — which are numeric and take a "
            "minute each.",
            "<b>Which is three tests, fifteen minutes, and three "
            "distinct requirements</b> — <b>and no amount of visual "
            "inspection substitutes for any of them</b>, because the "
            "whole point is that your vision is not the one being "
            "tested."]},
 ],
 "takeaways": [
   "No vision, low vision, and colour vision are three separate "
   "requirements with different fixes, and conflating them leaves "
   "interfaces half-done.",
   "Heading structure is navigation rather than typography, because "
   "jumping by heading is the primary screen reader operation.",
   "Speech is a serial channel with a cursor, so everything your layout "
   "conveys spatially must be conveyed some other way.",
   "Colour must never be the only channel carrying information, and the "
   "greyscale test settles it in one screenshot.",
   "Contrast requirements are computed from relative luminance rather than "
   "judged, which is why they actually get met.",
   "400% zoom with reflow breaks more layouts than anything else in this "
   "course, and takes thirty seconds to check.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Three requirements"),
  ("callout", "No vision, low vision, and colour vision are three separate "
              "requirements with different fixes",
   ["<b>No vision needs a non-visual representation of the whole "
    "interface</b> — <b>correct semantics, so that a screen reader "
    "can convey structure, state, and change</b> (&sect;2 and "
    "Module 08). <b>Visual design is entirely irrelevant to it</b>: a "
    "beautiful interface and an ugly one are identical here.",
    "<b>Low vision needs the visual design to survive "
    "enlargement</b> — <b>magnification, browser zoom, reflow, and "
    "contrast</b> (&sect;&sect;3 and 4). <b>Semantics help and are not "
    "sufficient</b>, because the user is looking at the pixels.",
    "<b>Colour vision needs redundant encoding</b> — <b>colour "
    "must never be the only channel carrying information</b> "
    "(&sect;3) — <b>which is a single rule, is trivially testable, "
    "and is very widely broken.</b>",
    "<b>And the three are frequently conflated</b> — "
    "<b>'accessible for blind users' is used loosely to mean all "
    "three</b>, and <b>a fix for one does nothing at all for the "
    "others</b>: perfect semantics do not fix low contrast, and a "
    "contrast fix does not make anything announceable. <b>That "
    "conflation is how interfaces end up half-done</b> and reported as "
    "finished."]),

  ("h1", "2 &nbsp; The screen reader model"),
  ("code", """NOT linearly, usually. The common operations:

    jump by heading       the primary navigation,
                          which is why heading
                          structure IS navigation
    jump by landmark      main, nav, search, footer
    list all links        then filter by typing
    list all headings     to get an outline of the
                          page
    tab through controls  focusable things only
    read continuously     when actually reading prose
    table navigation      cell by cell, with the row
                          and column headers
                          announced for each cell

WHICH MEANS
    headings are a table of contents, not a font size
    a page with one heading has no navigation
    link text must make sense out of context, because
        it is routinely heard out of context
    and "click here" twelve times is a list of twelve
        identical items"""),
  ("p", "<b>Heading structure is navigation, not typography</b> "
        "— <b>which is the single most useful thing to know about "
        "how screen readers are actually used</b>, and it reframes a "
        "whole class of markup decisions. A heading chosen for its size "
        "and a heading chosen for its level are different decisions, and "
        "<b>styling a <code>div</code> to look like a heading produces a "
        "page with no table of contents at all</b>. <b>Everything in "
        "this section follows from the jump-by-heading operation</b>, "
        "including why the link-text criterion exists."),
  ("callout", "And the thing to internalise is that it is a serial channel "
              "with a cursor",
   ["<b>Sight is parallel:</b> <b>you perceive layout, grouping, "
    "emphasis, and relative size simultaneously</b> and then attend to "
    "one part of it (CSCE 671 Module 02's preattentive "
    "material) — the structure arrives before you read anything.",
    "<b>Speech is serial and has a cursor</b> — <b>one thing at "
    "a time, in a definite order, with a current position</b> — so "
    "<b>everything your layout conveys spatially has to be conveyed some "
    "other way</b>, because there is no simultaneity to carry it.",
    "<b>Which is why grouping has to be semantic rather than "
    "visual</b>: <b>a visual box drawn around three related fields "
    "conveys nothing at all serially</b>, and <b>a "
    "<code>fieldset</code> with a <code>legend</code> does</b> — "
    "the group membership is announced with each field.",
    "<b>And it is why unannounced change is the characteristic "
    "defect of modern interfaces</b> — <b>a sighted user sees new "
    "content appear in the corner of their eye and a serial user does "
    "not know it happened at all</b> — which is <b>Module 08 "
    "&sect;4's live region problem</b> and the commonest failure in "
    "single-page applications."]),

  ("break",),
  ("h1", "3 &nbsp; Colour and contrast"),
  ("callout", "Colour must never be the only channel carrying information",
   ["<b>A substantial minority cannot distinguish certain hue "
    "pairs</b> — <b>red and green most commonly, at roughly one in "
    "twelve men and one in two hundred women of northern European "
    "descent</b> — so <b>a red-green status encoding is simply "
    "unreadable to them</b>, and red-green status encoding is "
    "everywhere.",
    "<b>So pair colour with a second channel</b>: <b>a shape, an "
    "icon, a position, a fill pattern, or a text label</b> — and "
    "<b>the text label is the most reliable</b>, because it also works "
    "for the screen reader case and for the greyscale print case.",
    "<b>And the quickest test is greyscale</b>: <b>if the "
    "information survives desaturation, the colour was "
    "redundant</b> — <b>which takes one screenshot and one "
    "filter</b> and is the test to run before shipping any figure or "
    "status display.",
    "<b>Which is CSCE 679 Module 04's argument</b> — and "
    "<b>there it is a perceptual fact about channel reliability and here "
    "it is a requirement with a conformance criterion attached</b>, "
    "<b>which is the same thing arriving from two directions</b> and is "
    "the clearest case of the two courses converging."]),
  ("table", ["What is being measured", "Minimum (level AA)",
             "Enhanced (level AAA)"],
   [["<b>Body text against its background</b>", "<b>4.5:1</b>",
     "<b>7:1</b>"],
    ["<b>Large text — 18pt, or 14pt bold</b>", "<b>3:1</b>",
     "<b>4.5:1</b>"],
    ["<b>Interface components, and the visible indication of their "
     "state</b>", "<b>3:1</b>", "<b>—</b>"],
    ["<b>Graphics and icons that carry meaning</b>", "<b>3:1</b>",
     "<b>—</b>"],
    ["<b>Purely decorative content, and disabled controls</b>",
     "<b>No requirement</b>", "<b>—</b>"]],
   [0.46, 0.27, 0.27]),
  ("p", "<b>These are computed from the relative luminances of the two "
        "colours, not judged by eye</b> — <b>so a contrast failure "
        "is a measurement rather than an opinion</b>, <b>and that is "
        "exactly what makes it arguable in a design review</b> where "
        "'it looks fine to me' otherwise wins. <b>The "
        "measured-not-judged property is why contrast requirements "
        "actually get met</b> while vaguer ones do not, which is a "
        "general lesson about writing requirements and is Module 07 "
        "&sect;2's point."),

  ("h1", "4 &nbsp; Magnification and zoom"),
  ("ul", ["<b>Text must reach 200% without loss of content or "
          "function</b> — and <b>400% with reflow into a single "
          "column</b>, <b>which is the criterion that breaks "
          "layouts</b> and is the one to test first.",
          "<b>Reflow means no two-dimensional scrolling</b> — "
          "<b>a magnifier user reading a line that requires horizontal "
          "scrolling loses their place at the end of every single "
          "line</b>, <b>which makes reading impossible rather than "
          "merely slow</b>, and is the reason the criterion is written "
          "the way it is.",
          "<b>And a magnifier shows a small window of the "
          "screen</b>, so <b>anything that depends on two distant parts "
          "being visible together fails</b> — <b>a tooltip far from "
          "its trigger, an error summary at the top of a long form, a "
          "status message in the opposite corner.</b>",
          "<b>Plus text has to actually be text</b> — <b>text "
          "rendered into an image pixelates on enlargement and cannot be "
          "restyled, recoloured, or read aloud</b> — which is why "
          "images of text are a separate criterion rather than a style "
          "preference.",
          "<b>And respect the user's chosen font size</b>, which "
          "means <b>relative units rather than fixed pixels</b> "
          "throughout. <b>400% zoom with reflow breaks more layouts "
          "than anything else in this course</b> — <b>and it takes "
          "thirty seconds to check</b>, which is the best "
          "effort-to-findings ratio available."]),
  ("callout", "And the three tests, which take about fifteen minutes together",
   ["<b>Turn on the screen reader and complete one real task without "
    "looking at the screen</b> — which tests the no-vision "
    "requirement, <b>and is the one that teaches you most</b> because "
    "the gap between what you assumed was announced and what is "
    "announced is large (&sect;2).",
    "<b>Set the browser to 400% and check for reflow</b>, then "
    "<b>turn on operating system magnification and look for distant "
    "dependencies</b> (&sect;4) — two minutes, and it finds layout "
    "defects that no other test does.",
    "<b>Run the contrast checker and the greyscale filter</b> "
    "(&sect;3) — <b>which are numeric and take about a minute "
    "each</b>, and give findings nobody can dispute.",
    "<b>Which is three tests, fifteen minutes, and three distinct "
    "requirements</b> — <b>and no amount of visual inspection "
    "substitutes for any of them</b>, <b>because the whole point is "
    "that your vision is not the one being tested</b> (Module 01 "
    "&sect;4's shared error)."]),
 ],
 "resources": [
   ("The WAI tutorials on page structure, images, and tables (free)",
    "https://www.w3.org/WAI/tutorials/",
    "<b>&sect;2</b> — the markup that produces correct screen reader "
    "behaviour, with examples of both the right and the wrong "
    "version."),
   ("WebAIM's screen reader keyboard shortcut references (free)",
    "https://webaim.org/resources/shortcuts/",
    "<b>&sect;2's operations</b> — keep this open the first few times "
    "you use a screen reader, because the model is not guessable."),
   ("Understanding WCAG 1.4.3 and 1.4.11 on contrast (free)",
    "https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum",
    "<b>&sect;3's table</b>, with the derivation of the ratios and the "
    "reasoning behind the exceptions."),
   ("Understanding WCAG 1.4.10 on reflow (free)",
    "https://www.w3.org/WAI/WCAG22/Understanding/reflow",
    "<b>&sect;4's hardest criterion</b> — and the explanation of why "
    "horizontal scrolling is disqualifying rather than merely "
    "awkward."),
 ],
 "exercises": [
   "<b>State the three vision requirements</b> and one fix that helps "
   "only one of them.",
   "<b>List the headings of one of your pages</b> and ask whether they "
   "form an outline.",
   "<b>List all the links</b> out of context and check each makes "
   "sense.",
   "<b>Complete one task with a screen reader, eyes closed</b>, and "
   "record where you got stuck.",
   "<b>Find one visually grouped set of fields</b> and check whether the "
   "grouping is semantic.",
   "<b>Find one unannounced change</b> in an interface you use.",
   "<b>Desaturate three interfaces</b> and list what information "
   "disappeared.",
   "<b>Measure the contrast</b> of every text colour in your own "
   "project.",
   "<b>Set 400% zoom</b> on your own project and record what breaks.",
   "<b>Find a distant dependency</b> that a magnifier window would "
   "split.",
 ],
 "selfcheck": [
   "Name the three vision requirements and the fix for each.",
   "Why does conflating them leave interfaces half-done?",
   "Give five screen reader navigation operations.",
   "Why is heading structure navigation?",
   "Why must link text work out of context?",
   "Contrast parallel and serial perception, and give one consequence.",
   "State the colour rule and the quickest test for it.",
   "Give the contrast ratios for body text, large text, and "
   "components.",
   "Why does the measured-not-judged property matter?",
   "What does reflow require, and why is horizontal scrolling "
   "disqualifying?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Hearing and Speech",
 "subtitle": "Audio alternatives, and not requiring a voice.",
 "question": "What does your interface say that it does not also "
             "write?",
 "outcomes": [
     "State the requirements for audio content.",
     "Distinguish captions, subtitles, and transcripts.",
     "Explain audio description and when it is needed.",
     "Explain why voice-only input excludes people.",
     "Test an interface with the sound off.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The requirement",
   "blurb": "Which is short to state."},

  {"t": "callout", "title": "No information may be available only as audio, and none only as video",
   "kind": "The whole requirement, in one sentence",
   "body": ["<b>Any information carried by sound needs a text or "
            "visual equivalent</b> — speech, alarms, status tones, "
            "and the audio track of video.",
            "<b>And symmetrically, any information carried only "
            "visually in a video needs an audio or text "
            "equivalent</b> — which is audio description "
            "(Part 3) and is the half people "
            "forget.",
            "<b>So the test is: turn the sound off, then look "
            "away</b> — <b>and anything you lose in either direction "
            "is a defect</b>, which is two minutes of "
            "work.",
            "<b>Plus the situational case is "
            "enormous</b> — <b>most video on the internet is watched "
            "without sound</b>, which makes this the clearest curb cut "
            "in the course (Module 02 §1)."]},

  {"t": "section", "label": "Part 2", "title": "Captions and transcripts",
   "blurb": "Which are different things for different purposes."},

  {"t": "table", "kicker": "Alternatives", "title": "The distinctions, which matter",
   "header": ["Thing", "What it is", "What it is for"],
   "widths": [2.7, 4.3, 4.2],
   "rows": [
     ["<b>Captions</b>", "<b>Synchronised text of all audio, incl. non-speech</b>", "<b>Watching without hearing</b>"],
     ["<b>Subtitles</b>", "<b>Synchronised translation of speech only</b>", "<b>Not an accessibility feature</b>"],
     ["<b>Transcript</b>", "<b>The full text, unsynchronised</b>", "<b>Reading, searching, skimming</b>"],
     ["<b>Audio description</b>", "<b>Narration of essential visual content</b>", "<b>Watching without seeing</b>"],
     ["<b>Sign interpretation</b>", "<b>A signed track</b>", "<b>Signing users; AAA-level</b>"],
   ],
   "footnote": "<b>Subtitles are not captions</b> — they omit "
               "speaker identification and non-speech audio, both of "
               "which are information, and a player labelling them "
               "interchangeably is a common "
               "defect.",
   "note": "The subtitles-are-not-captions distinction is the one "
           "most often got wrong."},

  {"t": "callout", "title": "And automatic captions are a draft, not a deliverable",
   "kind": "A specific and current problem",
   "body": ["<b>Automatic speech recognition has improved "
            "enormously and still fails on exactly the hard "
            "parts</b> — <b>names, technical terms, accents, "
            "overlapping speakers, and punctuation</b>.",
            "<b>Which means the errors are concentrated in the "
            "content words</b> — <b>the terms carrying the "
            "meaning</b> — and a caption track with the technical "
            "vocabulary wrong is worse than useless for a "
            "lecture.",
            "<b>And they do not caption non-speech audio</b>: no "
            "speaker identification, no '[alarm sounds]', no "
            "'[laughter]' — all of which is "
            "information.",
            "<b>So: generate automatically and correct "
            "manually</b> — <b>which is far cheaper than transcribing "
            "from nothing</b>, and is the honest workflow rather than a "
            "compromise."]},

  {"t": "section", "label": "Part 3", "title": "Audio description",
   "blurb": "The half that gets forgotten."},

  {"t": "bullets", "kicker": "Description", "title": "When visual-only content needs narrating",
   "items": [
     "<b>Whenever essential information appears visually without "
     "being spoken</b> — <b>on-screen text, a diagram, a "
     "demonstration, a gesture, a facial reaction that carries the "
     "meaning.</b>",
     "",
     "<b>Which is most instructional video</b> — <b>'as you "
     "can see here' followed by silence is the characteristic "
     "failure</b>, and it is extremely "
     "common.",
     "",
     "<b>And the cheapest fix is to not need it</b>: <b>narrate "
     "what you are doing as you do it</b>, which produces a video that "
     "needs no separate description track and is better "
     "anyway.",
     "",
     "<b>Which is the design-for-the-constraint move</b> "
     "(Module 01 §2) — <b>the accessible version is the "
     "better version here</b>, not an addition to "
     "it.",
     "",
     "<b>And a text transcript with the visual content described "
     "is frequently sufficient</b>, and much cheaper than a described "
     "audio track.",
   ],
   "footnote": "<b>'As you can see here' followed by silence</b> "
               "— the characteristic failure of instructional video, "
               "and it is fixed by narrating rather than by adding a "
               "track."},

  {"t": "section", "label": "Part 4", "title": "Speech as input",
   "blurb": "Which excludes people when it is the only way in."},

  {"t": "callout", "title": "A voice-only interface excludes anybody who does not speak the way it expects",
   "kind": "An increasingly important requirement",
   "body": ["<b>Non-speaking people, people with dysarthria or a "
            "stammer, people with atypical accents, and people who "
            "simply cannot speak aloud right now</b> are all excluded by "
            "a voice-only path.",
            "<b>And speech recognition accuracy varies "
            "systematically by accent and by speech pattern</b> — "
            "<b>which is CSCE 638 §12's measured disparity arriving "
            "as an access requirement.</b>",
            "<b>So voice must be an alternative input and never the "
            "only one</b> — <b>a text path, a keypad path, or a human "
            "path has to exist</b>, which is a specific requirement for "
            "phone systems and voice assistants.",
            "<b>And the situational case is universal:</b> <b>a "
            "quiet office, a meeting, a sleeping child, a crowded "
            "train</b> — which makes this another case where the "
            "requirement needs no charity."]},

  {"t": "callout", "title": "And the tests, which take five minutes",
   "kind": "Closing",
   "body": ["<b>Mute everything and use the interface</b> — <b>and "
            "list every notification, alarm, and status tone you "
            "missed.</b>",
            "<b>Play every video with the sound off and read the "
            "captions</b> — checking for speaker identification and "
            "non-speech audio, not only for accuracy.",
            "<b>Then play it with the screen off and listen</b> "
            "— which is the audio description test and the one nobody "
            "runs.",
            "<b>And find every path that requires speaking</b>, and "
            "check that an alternative exists. <b>Five minutes, four "
            "tests</b> — and this module's requirements are the "
            "cheapest to meet of any in the course."]},
 ],
 "takeaways": [
   "No information may be available only as audio, and none only as "
   "visual-in-video — and the second half is the one people forget.",
   "Subtitles are not captions: they omit speaker identification and "
   "non-speech audio, both of which are information.",
   "Automatic captions fail concentratedly on names, technical terms, and "
   "accents — the content words — so they are a draft.",
   "'As you can see here' followed by silence is the characteristic failure "
   "of instructional video.",
   "Narrating what you do as you do it removes the need for a description "
   "track and makes a better video.",
   "Speech recognition accuracy varies systematically by accent and speech "
   "pattern, so voice must never be the only input.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The requirement"),
  ("callout", "No information may be available only as audio, and none only "
              "as video",
   ["<b>Any information carried by sound needs a text or visual "
    "equivalent</b> — speech, alarms, status tones, error beeps, and "
    "the entire audio track of any video — which is the half of the "
    "requirement everybody knows.",
    "<b>And symmetrically, any information carried only visually "
    "within a video needs an audio or text equivalent</b> — "
    "<b>which is audio description</b> (&sect;3) <b>and is the half "
    "people forget</b>, including in otherwise careful "
    "organisations.",
    "<b>So the test is: turn the sound off, then look away</b> "
    "— <b>and anything you lose in either direction is a "
    "defect</b> — <b>which is about two minutes of work</b> and "
    "finds essentially everything in this module.",
    "<b>Plus the situational case here is enormous</b> — "
    "<b>most video on the internet is watched without sound</b>, in "
    "feeds, in offices, and on public transport — <b>which makes "
    "this the clearest curb cut in the course</b> (Module 02 "
    "&sect;1) and the easiest requirement to get agreement on."]),

  ("h1", "2 &nbsp; Captions and transcripts"),
  ("table", ["The thing", "What it actually is", "What it is for"],
   [["<b>Captions</b>",
     "<b>Synchronised text of all audio content, including speaker "
     "identification and significant non-speech sound.</b>",
     "<b>Watching without hearing</b> — the accessibility "
     "requirement."],
    ["<b>Subtitles</b>",
     "<b>Synchronised translation of the spoken dialogue only.</b>",
     "<b>Understanding a different language.</b> <b>Not an "
     "accessibility feature</b> — see the note."],
    ["<b>Transcript</b>",
     "<b>The full text of the audio, unsynchronised, as a "
     "document.</b>",
     "<b>Reading instead of watching, searching, skimming, and "
     "quoting</b> — and frequently what people prefer."],
    ["<b>Audio description</b>",
     "<b>Narration of the essential visual content, in the gaps or as "
     "an extended track.</b>",
     "<b>Watching without seeing</b> (&sect;3)."],
    ["<b>Sign language interpretation</b>",
     "<b>A signed track, by a human interpreter.</b>",
     "<b>Users whose first language is a signed one</b>; a AAA-level "
     "criterion."]],
   [0.20, 0.44, 0.36]),
  ("p", "<b>Subtitles are not captions</b> — <b>they omit speaker "
        "identification and non-speech audio, both of which are "
        "information</b> (who is talking; that an alarm is sounding; that "
        "the line went dead) — <b>and a player that labels the two "
        "interchangeably is a common and consequential defect</b>, "
        "because a user selecting 'subtitles' believing them to be "
        "captions gets a silently degraded experience. <b>The "
        "subtitles-are-not-captions distinction is the one most often got "
        "wrong</b>, including in procurement documents."),
  ("callout", "And automatic captions are a draft, not a deliverable",
   ["<b>Automatic speech recognition has improved enormously and "
    "still fails on exactly the hard parts</b> — <b>proper names, "
    "technical terminology, strong or less-represented accents, "
    "overlapping speakers, and punctuation.</b>",
    "<b>Which means the errors are concentrated in the content "
    "words</b> — <b>precisely the terms carrying the "
    "meaning</b> — <b>and a caption track with the technical "
    "vocabulary wrong is worse than useless for a lecture</b>, because "
    "it is confidently incorrect rather than obviously absent.",
    "<b>And they do not caption non-speech audio at all</b>: no "
    "speaker identification, no '[alarm sounds]', no '[laughter]', no "
    "'[the line disconnects]' — <b>all of which is "
    "information</b> and some of which is the point of the scene.",
    "<b>So: generate automatically and correct manually</b> — "
    "<b>which is far cheaper than transcribing from nothing</b>, takes a "
    "fraction of the media's duration, <b>and is the honest workflow "
    "rather than a compromise</b> (Module 12 &sect;3's cost "
    "argument)."]),

  ("break",),
  ("h1", "3 &nbsp; Audio description"),
  ("ul", ["<b>Whenever essential information appears visually without "
          "being spoken</b> — <b>on-screen text, a diagram, a "
          "demonstration, a pointed-at thing, a gesture, or a facial "
          "reaction that carries the meaning.</b>",
          "<b>Which is most instructional and demonstration "
          "video</b> — <b>'as you can see here' followed by silence "
          "is the characteristic failure</b>, <b>and it is extremely "
          "common</b> in exactly the material students are asked to "
          "learn from.",
          "<b>And the cheapest fix is to not need it:</b> <b>narrate "
          "what you are doing as you do it</b> — 'I'm opening the "
          "settings panel, and the third option is the one we want' "
          "— <b>which produces a video that needs no separate "
          "description track and is better anyway</b>, including for "
          "sighted viewers who looked away.",
          "<b>Which is the design-for-the-constraint move in its "
          "purest form</b> (Module 01 &sect;2) — <b>the "
          "accessible version is the better version here</b>, <b>not an "
          "addition to it</b>, and that is the strongest form the "
          "argument takes.",
          "<b>And a text transcript with the visual content "
          "described in it is frequently sufficient</b> for "
          "conformance and in practice, <b>and is much cheaper than a "
          "described audio track</b> — which matters when the "
          "alternative is nothing at all."]),

  ("h1", "4 &nbsp; Speech as input"),
  ("callout", "A voice-only interface excludes anybody who does not speak the "
              "way it expects",
   ["<b>Non-speaking people, people with dysarthria, a stammer, or a "
    "tracheostomy, people with atypical or less-represented accents, and "
    "people who simply cannot speak aloud right now</b> are all excluded "
    "by a voice-only path — which is a wider group than the design "
    "usually assumes.",
    "<b>And speech recognition accuracy varies systematically by "
    "accent and by speech pattern</b> — <b>which is CSCE 638 "
    "Module 12's measured disparity arriving here as an access "
    "requirement</b> rather than as a fairness finding, and is the same "
    "fact either way.",
    "<b>So voice must be an alternative input and never the only "
    "one</b> — <b>a text path, a keypad path, or a human path has "
    "to exist</b> — which is <b>a specific and frequently violated "
    "requirement for telephone systems, voice assistants, and in-car "
    "interfaces.</b>",
    "<b>And the situational case is universal:</b> <b>a quiet "
    "office, a meeting, a sleeping child, a crowded train, a sore "
    "throat</b> — <b>which makes this another case where the "
    "requirement needs no charity to be obvious</b>, only the "
    "observation that nobody wants to talk to their phone in a "
    "meeting."]),
  ("callout", "And the tests, which take five minutes",
   ["<b>Mute everything and use the interface normally</b> — "
    "<b>and list every notification, alarm, error, and status tone you "
    "missed</b>, which is usually more than you expected.",
    "<b>Play every video with the sound off and read the "
    "captions</b> — <b>checking for speaker identification and "
    "non-speech audio, not only for word accuracy</b>, since those are "
    "what automatic captions omit entirely (&sect;2).",
    "<b>Then play it with the screen off and listen</b> — "
    "<b>which is the audio description test and the one nobody "
    "runs</b>, and which finds the 'as you can see here' failures "
    "immediately.",
    "<b>And find every path that requires speaking</b>, and check "
    "that a non-speech alternative exists. <b>Five minutes, four "
    "tests</b> — and <b>this module's requirements are the cheapest "
    "to meet of any in the course</b>, which makes their frequent "
    "absence harder to explain than most."]),
 ],
 "resources": [
   ("The WAI media accessibility guide (free)",
    "https://www.w3.org/WAI/media/av/",
    "<b>The whole module</b>, free and well organised — with the "
    "captions, transcripts, and description requirements separated "
    "properly."),
   ("Understanding WCAG 1.2.x on time-based media (free)",
    "https://www.w3.org/WAI/WCAG22/Understanding/",
    "<b>&sect;&sect;1 to 3's criteria</b>, with the levels and the "
    "exceptions explained."),
   ("The DCMP Captioning Key (free)",
    "https://dcmp.org/learn/captioningkey",
    "<b>&sect;2 in practice</b> — how to caption well, including "
    "placement, timing, and non-speech conventions."),
   ("Koenecke et al. &mdash; Racial disparities in automated speech "
    "recognition (free)",
    "https://www.pnas.org/doi/10.1073/pnas.1915768117",
    "<b>&sect;4's disparity, measured</b> — and the same study "
    "CSCE 638 Module 12 uses."),
 ],
 "exercises": [
   "<b>Mute your machine for an hour</b> and list what you missed.",
   "<b>State the audio requirement in both directions</b> and give an "
   "example of each failure.",
   "<b>Compare a subtitle track and a caption track</b> for the same "
   "video.",
   "<b>Generate automatic captions</b> for a technical talk and count "
   "the content-word errors.",
   "<b>Correct them</b>, and record how long it took per minute of "
   "media.",
   "<b>Find three instructional videos</b> with 'as you can see here' "
   "failures.",
   "<b>Record a two-minute demonstration</b> narrating everything you "
   "do.",
   "<b>Write a transcript with the visual content described.</b>",
   "<b>Find a voice-only path</b> in a system you use, and look for the "
   "alternative.",
   "<b>Run all four tests from the closing callout</b> on your own "
   "project.",
 ],
 "selfcheck": [
   "State the requirement in both directions.",
   "Which half is forgotten, and what is it called?",
   "Give the five audio alternatives and what each is for.",
   "Why are subtitles not captions?",
   "Why do automatic caption errors concentrate in content words?",
   "What do automatic captions omit entirely?",
   "When is audio description needed, and what is the cheapest fix?",
   "Why is that fix the design-for-the-constraint move?",
   "Who does a voice-only interface exclude?",
   "Give the four tests and what each finds.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Motor Control",
 "subtitle": "Keyboard, targets, and time.",
 "question": "Can you use this without a mouse?",
 "outcomes": [
     "Explain the range of motor requirements.",
     "Explain keyboard operability and focus management.",
     "State the target size and pointer requirements.",
     "Explain why timing requirements exclude people.",
     "Test an interface with the mouse unplugged.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The range",
   "blurb": "Which is wider than wheelchairs."},

  {"t": "bullets", "kicker": "Requirements", "title": "What varies, and what each implies",
   "items": [
     "<b>Precision</b> — tremor, spasticity, or an unsteady "
     "pointer mean <b>a small target is unhittable</b>, which is "
     "Part 3's subject.",
     "",
     "<b>Range of motion</b> — a head pointer or a limited "
     "reach means <b>a target far from the current position is "
     "expensive</b> (CSCE 671 §05's Fitts's "
     "law).",
     "",
     "<b>Number of available inputs</b> — <b>switch access "
     "may have one</b>, so <b>every step costs</b>, and a "
     "twelve-step flow is not usable.",
     "",
     "<b>Speed and endurance</b> — <b>any timeout, any "
     "double-click interval, any drag is a barrier</b>, which is "
     "Part 4.",
     "",
     "<b>And whether a second simultaneous input is "
     "possible</b> — which rules out modifier chords and "
     "multi-point gestures as sole mechanisms.",
   ],
   "footnote": "<b>With switch access, every step has a cost</b> "
               "— which turns step count from a convenience metric "
               "into an accessibility one."},

  {"t": "section", "label": "Part 2", "title": "Keyboard operability",
   "blurb": "The single highest-value requirement in this course."},

  {"t": "code", "kicker": "Keyboard", "title": "What keyboard operability actually requires",
   "lang": "text", "code": """
  REACHABLE
      every interactive element receives focus
      in an order that matches the visual order
      with no element reachable only by mouse

  VISIBLE
      focus is always visible, with 3:1 contrast
      and never removed without a replacement
      (outline: none with nothing else is the
       single commonest defect in this module)

  OPERABLE
      every action available from the keyboard
      including drag, hover, and right-click paths

  ESCAPABLE
      no keyboard trap: you can always get out
      modals return focus where it came from

  SKIPPABLE
      a skip link, or landmarks, so repeated
      navigation can be bypassed
""",
   "caption": "<b><code>outline: none</code> with nothing to replace "
              "it is the single commonest defect in this "
              "module</b> — and it makes the interface unusable "
              "while looking tidier.",
   "note": "The five properties are reachable, visible, operable, "
           "escapable, skippable."},

  {"t": "callout", "title": "Because the keyboard is the substrate every other input sits on",
   "kind": "Why this one requirement carries so much",
   "body": ["<b>Switch access, voice control, head pointers, and "
            "alternative keyboards all ultimately drive the keyboard "
            "interface</b> — so <b>keyboard operability is a "
            "precondition for all of them.</b>",
            "<b>And screen reader navigation depends on focus "
            "order</b>, which means a broken focus order breaks the "
            "no-vision case too (Module 03 "
            "§2).",
            "<b>Which makes 'unplug the mouse' the highest-yield "
            "test in the course</b> — <b>it finds motor, vision, and "
            "switch-access defects simultaneously</b>, and costs ten "
            "seconds to start.",
            "<b>And power users want it anyway</b> — <b>the curb "
            "cut here is that keyboard shortcuts are a requested "
            "feature</b>, which makes this the easiest requirement to "
            "fund (Module 01 §2)."]},

  {"t": "section", "label": "Part 3", "title": "Targets and pointers",
   "blurb": "Size, spacing, and what must not be required."},

  {"t": "bullets", "kicker": "Pointer", "title": "The requirements, which are concrete",
   "items": [
     "<b>Targets at least 24 by 24 CSS pixels</b>, or spaced so "
     "that a 24-pixel circle around each does not overlap — and "
     "<b>44 is the usual platform guidance for touch</b>, which is "
     "better.",
     "",
     "<b>No path-dependent gesture as the only "
     "mechanism</b> — <b>a swipe, a drag, or a traced path needs "
     "a single-pointer alternative</b>, because tracing a path "
     "requires sustained control.",
     "",
     "<b>No multi-point gesture as the only "
     "mechanism</b> — pinch-to-zoom needs buttons too.",
     "",
     "<b>No hover-only content</b> — <b>because hover cannot "
     "be produced by touch, by keyboard, or reliably by a head "
     "pointer</b>, and hover content must be dismissible and "
     "hoverable.",
     "",
     "<b>And actions on down-event are a "
     "trap</b> — <b>commit on up, so a mistaken press can be "
     "aborted by moving away</b>, which is a specific and useful "
     "criterion.",
   ],
   "footnote": "<b>Commit on the up-event, not the down-event</b> "
               "— which lets a user who pressed the wrong thing "
               "abort by moving off it, and is free to "
               "implement."},

  {"t": "section", "label": "Part 4", "title": "Time",
   "blurb": "Which is the quietest exclusion in the course."},

  {"t": "callout", "title": "Any time limit excludes anybody who needs longer, and most time limits are arbitrary",
   "kind": "The requirement, and the common failures",
   "body": ["<b>A session timeout, a carousel that advances, a "
            "message that disappears, a double-click interval, a "
            "drag-and-hold</b> — <b>each assumes a speed, and the "
            "assumption is usually unexamined.</b>",
            "<b>So the rule is: adjustable, extendable, or "
            "absent</b> — <b>twenty seconds' warning and a way to "
            "extend</b>, except where the limit is essential (a live "
            "auction) or very long.",
            "<b>And the data-loss case is the serious "
            "one</b> — <b>a form that times out and discards what was "
            "typed</b> punishes slow entry specifically, which is "
            "exactly the wrong group.",
            "<b>Plus anything that moves, scrolls, or auto-updates "
            "needs a pause</b> — <b>which is also "
            "CSCE 671 §06's attention argument</b> and "
            "Module 06's cognitive one."]},

  {"t": "callout", "title": "And the test is the cheapest one that exists",
   "kind": "Closing",
   "body": ["<b>Unplug the mouse.</b> Then complete the three most "
            "important tasks in your interface using only the "
            "keyboard.",
            "<b>Watching for the five properties</b> — "
            "<b>reachable, visible, operable, escapable, "
            "skippable</b> (Part 2) — and recording every "
            "place you got stuck.",
            "<b>Then check the targets, the gestures, and the "
            "timeouts</b> (Parts 3 and 4), which is a "
            "read-through rather than a test.",
            "<b>Which finds more real defects per minute than "
            "anything else in this course</b> — <b>and is the first "
            "thing Project 1 asks for</b>, because it reframes how you "
            "think about every control you build afterwards."]},
 ],
 "takeaways": [
   "Precision, range, input count, speed, and simultaneity all vary, and "
   "each implies a different requirement.",
   "With switch access every step has a cost, which turns step count into "
   "an accessibility metric.",
   "Keyboard operability requires five properties: reachable, visible, "
   "operable, escapable, skippable.",
   "`outline: none` with nothing to replace it is the commonest defect in "
   "this module, and it makes the interface unusable while looking tidier.",
   "The keyboard is the substrate every other input sits on, which makes "
   "'unplug the mouse' the highest-yield test in the course.",
   "Commit on the up-event rather than the down-event, so a mistaken press "
   "can be aborted.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The range"),
  ("ul", ["<b>Precision</b> — tremor, spasticity, dystonia, or an "
          "inherently unsteady pointer such as a head tracker mean "
          "<b>a small target is unhittable rather than merely "
          "fiddly</b>, which is &sect;3's subject.",
          "<b>Range of motion</b> — a head pointer, a mouth "
          "stick, or a limited reach means <b>a target far from the "
          "current position is expensive in a way a hand on a mouse is "
          "not</b> (CSCE 671 Module 05's Fitts's law, where the "
          "distance term dominates).",
          "<b>The number of available inputs</b> — <b>switch "
          "access may have exactly one</b>, with a scanning highlight "
          "moving through the options, <b>so every step costs real "
          "seconds</b>, and <b>a twelve-step flow is not usable</b> "
          "regardless of how accessible each step is.",
          "<b>Speed and endurance</b> — <b>any timeout, any "
          "required double-click interval, any press-and-hold, and any "
          "drag is a barrier</b>, which is &sect;4.",
          "<b>And whether a second simultaneous input is possible at "
          "all</b> — which <b>rules out modifier chords and "
          "multi-point gestures as sole mechanisms</b> (&sect;3). "
          "<b>With switch access, every step has a cost</b> — "
          "<b>which turns step count from a convenience metric into an "
          "accessibility one</b>, and is a good reason to count the "
          "steps in your main flow."]),

  ("h1", "2 &nbsp; Keyboard operability"),
  ("code", """REACHABLE
    every interactive element receives focus
    in an order that matches the visual order
    with no element reachable only by mouse

VISIBLE
    focus is always visible, with 3:1 contrast
    and never removed without a replacement
    (outline: none with nothing else is the single
     commonest defect in this module)

OPERABLE
    every action available from the keyboard
    including drag, hover, and right-click paths

ESCAPABLE
    no keyboard trap: you can always get out
    modals return focus where it came from

SKIPPABLE
    a skip link, or landmarks, so that repeated
    navigation can be bypassed"""),
  ("p", "<b><code>outline: none</code> with nothing to replace it is "
        "the single commonest defect in this module</b> — <b>and it "
        "makes the interface unusable while looking tidier</b>, which is "
        "why it survives design review. A keyboard user with no visible "
        "focus indicator is navigating blind: the focus is somewhere, "
        "pressing Enter will do something, and there is no way to know "
        "what. <b>The five properties are reachable, visible, operable, "
        "escapable, skippable</b>, and they are worth memorising because "
        "they structure the whole test."),
  ("callout", "Because the keyboard is the substrate every other input sits "
              "on",
   ["<b>Switch access, voice control, head pointers, eye tracking, "
    "and alternative keyboards all ultimately drive the keyboard "
    "interface</b> — they synthesise focus moves and "
    "activations — so <b>keyboard operability is a precondition for "
    "every one of them</b> rather than one option among several.",
    "<b>And screen reader navigation depends on the focus order</b> "
    "and on focusability, which means <b>a broken focus order breaks the "
    "no-vision case too</b> (Module 03 &sect;2) — the two "
    "requirements are not independent.",
    "<b>Which makes 'unplug the mouse' the highest-yield test in the "
    "course</b> — <b>it finds motor defects, screen reader defects, "
    "and switch-access defects simultaneously</b>, <b>and costs ten "
    "seconds to start.</b>",
    "<b>And power users want it anyway</b> — <b>the curb cut "
    "here is that keyboard shortcuts and full keyboard operability are a "
    "requested feature</b> that people write in to ask for — "
    "<b>which makes this the easiest requirement in the course to "
    "fund</b> (Module 01 &sect;2, and Module 12 &sect;2's "
    "practical version)."]),

  ("break",),
  ("h1", "3 &nbsp; Targets and pointers"),
  ("ul", ["<b>Targets at least 24 by 24 CSS pixels</b>, or spaced so "
          "that a 24-pixel circle centred on each does not overlap a "
          "neighbour — and <b>44 is the usual platform guidance for "
          "touch</b>, <b>which is better</b> and is what to aim for "
          "rather than the floor.",
          "<b>No path-dependent gesture as the only "
          "mechanism</b> — <b>a swipe, a drag, or a traced path "
          "needs a single-pointer alternative</b>, <b>because tracing a "
          "path requires sustained directional control</b> that a tremor "
          "or a head pointer cannot provide.",
          "<b>No multi-point gesture as the only mechanism</b> "
          "— pinch-to-zoom needs buttons as well, since a one-finger "
          "or one-switch user cannot pinch.",
          "<b>No hover-only content</b> — <b>because hover "
          "cannot be produced by touch, by keyboard, or reliably by a "
          "head pointer</b> — and where hover content exists it must "
          "be <b>dismissible without moving the pointer, hoverable "
          "itself, and persistent</b> until dismissed.",
          "<b>And actions fired on the down-event are a trap</b> "
          "— <b>commit on up, so that a mistaken press can be "
          "aborted by moving away before releasing</b>, which is a "
          "specific criterion, is free to implement, and is what every "
          "native button already does. <b>Commit on the up-event, not "
          "the down-event.</b>"]),

  ("h1", "4 &nbsp; Time"),
  ("callout", "Any time limit excludes anybody who needs longer, and most "
              "time limits are arbitrary",
   ["<b>A session timeout, a carousel that advances on its own, a "
    "status message that disappears after three seconds, a required "
    "double-click interval, a drag-and-hold</b> — <b>each one "
    "assumes a speed, and the assumption is usually unexamined</b> and "
    "inherited from a default.",
    "<b>So the rule is: adjustable, extendable, or absent</b> "
    "— <b>at minimum twenty seconds' warning and a simple way to "
    "extend</b> — <b>except where the limit is genuinely essential "
    "(a live auction, a real-time event) or is already very long.</b>",
    "<b>And the data-loss case is the serious one</b>: <b>a form "
    "that times out and discards what was typed punishes slow entry "
    "specifically</b> — <b>which is exactly the wrong group</b>, "
    "since slow entry is what a motor or cognitive constraint produces. "
    "Preserve the data across re-authentication.",
    "<b>Plus anything that moves, scrolls, blinks, or auto-updates "
    "needs a pause control</b> — <b>which is also CSCE 671 "
    "Module 06's attention argument</b> (motion captures attention "
    "involuntarily) <b>and Module 06's cognitive one</b>, arriving at "
    "the same requirement from three directions."]),
  ("callout", "And the test is the cheapest one that exists",
   ["<b>Unplug the mouse.</b> Then complete the three most important "
    "tasks in your interface using only the keyboard — and resist "
    "the urge to touch the trackpad, which is harder than it sounds.",
    "<b>Watching for the five properties</b> — <b>reachable, "
    "visible, operable, escapable, skippable</b> (&sect;2) — and "
    "<b>recording every place you got stuck</b>, including the places "
    "where you only got through because you knew the layout.",
    "<b>Then check the targets, the gestures, and the timeouts</b> "
    "(&sect;&sect;3 and 4), <b>which is a read-through of the code "
    "rather than an interactive test</b> and takes about as long.",
    "<b>Which finds more real defects per minute than anything else "
    "in this course</b> — <b>and is the first thing Project 1 asks "
    "for</b>, <b>because it reframes how you think about every control "
    "you build afterwards</b>, which is a larger effect than the defect "
    "list itself."]),
 ],
 "resources": [
   ("The WAI keyboard and forms tutorials (free)",
    "https://www.w3.org/WAI/tutorials/forms/",
    "<b>&sect;2</b> — focus order, focus visibility, and the markup "
    "that produces them without effort."),
   ("Understanding WCAG 2.5.x on pointer input (free)",
    "https://www.w3.org/WAI/WCAG22/Understanding/",
    "<b>&sect;3's criteria</b> — target size, pointer gestures, "
    "pointer cancellation, and dragging movements, each with its "
    "reasoning."),
   ("Understanding WCAG 2.2.1 on timing adjustable (free)",
    "https://www.w3.org/WAI/WCAG22/Understanding/timing-adjustable",
    "<b>&sect;4</b> — including the exceptions, which are narrower "
    "than people assume."),
   ("The Inclusive Components patterns (free)",
    "https://inclusive-components.design/",
    "<b>&sect;&sect;2 and 3 as working components</b> — keyboard "
    "models and focus management, built up from the mechanism."),
 ],
 "exercises": [
   "<b>Name the five varying factors</b> and one requirement each "
   "implies.",
   "<b>Count the steps</b> in your interface's main flow, and halve "
   "them.",
   "<b>Unplug the mouse</b> and complete three tasks.",
   "<b>Check all five keyboard properties</b> and report which "
   "failed.",
   "<b>Grep your stylesheets for <code>outline</code></b> and audit "
   "every suppression.",
   "<b>Open and close a modal by keyboard</b> and check where focus "
   "goes.",
   "<b>Measure every target</b> in your interface against 24 and 44 "
   "pixels.",
   "<b>Find a hover-only, drag-only, or pinch-only mechanism</b> and "
   "add an alternative.",
   "<b>List every time limit</b> in something you built, and justify or "
   "remove each.",
   "<b>Check whether a timeout discards typed data</b>, and fix it if "
   "so.",
 ],
 "selfcheck": [
   "Name five varying motor factors and their implications.",
   "Why does step count matter for switch access?",
   "Give the five keyboard properties.",
   "What is the commonest defect, and why does it survive review?",
   "Why is the keyboard the substrate for other inputs?",
   "Why is unplugging the mouse the highest-yield test?",
   "State the target size requirement, both forms.",
   "Name three gesture requirements.",
   "Why commit on the up-event?",
   "State the timing rule, its exceptions, and the data-loss case.",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Cognition, Attention, and Language",
 "subtitle": "The largest group, and the least served.",
 "question": "How much does this ask you to hold in your head?",
 "outcomes": [
     "Explain why this area is the least well covered.",
     "State the memory and attention requirements.",
     "Explain language and reading requirements.",
     "Explain error prevention and recovery as access.",
     "Reduce the cognitive demand of an interface.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why this is underserved",
   "blurb": "Which is worth understanding, not just noting."},

  {"t": "callout", "title": "The cognitive requirements are the largest in population and the weakest in the standard",
   "kind": "An honest statement about a real gap",
   "body": ["<b>Cognitive, learning, and attention-related "
            "conditions are collectively the most common</b> — and "
            "<b>the standard's coverage of them is the thinnest and the "
            "most qualitative.</b>",
            "<b>Because the requirements resist the "
            "measured-not-judged property</b> that makes contrast work "
            "(Module 03 §3): <b>'is this simple enough' has no "
            "threshold</b>, and a criterion without a threshold is hard "
            "to enforce.",
            "<b>Which is a limitation of the standard rather than of "
            "the requirement</b> — <b>and Module 07 §4 is about what "
            "a standard can and cannot encode.</b>",
            "<b>So this module is more design guidance than "
            "checklist</b> — stated openly, because <b>pretending a "
            "qualitative requirement is a checkbox produces compliance "
            "without benefit.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Memory and attention",
   "blurb": "What the interface may assume."},

  {"t": "bullets", "kicker": "Demand", "title": "Reducing what has to be held",
   "items": [
     "<b>Do not require remembering across steps</b> — "
     "<b>show the reference code on the page that asks for it</b>, "
     "which is CSCE 671 §03's "
     "recognition-over-recall.",
     "",
     "<b>Do not require remembering across modes</b> — a "
     "modal that hides the information it asks about is the specific "
     "version of this.",
     "",
     "<b>Keep the sequence short and show the "
     "position</b> — <b>'step 2 of 4' costs nothing and removes "
     "a sustained uncertainty.</b>",
     "",
     "<b>Allow interruption and resumption</b> — <b>which is "
     "the requirement attention conditions most need and almost nothing "
     "provides</b>: save the partial state.",
     "",
     "<b>And remove involuntary attention capture</b> — "
     "<b>motion, autoplay, and sudden layout shift all take attention "
     "whether or not it can be spared</b> "
     "(CSCE 671 §06).",
   ],
   "footnote": "<b>Allowing interruption and resumption is the "
               "requirement attention conditions most need and almost "
               "nothing provides</b> — save the partial state, "
               "always."},

  {"t": "section", "label": "Part 3", "title": "Language",
   "blurb": "Which is a technical requirement, not a style one."},

  {"t": "callout", "title": "Write for the lowest reading demand the content allows, which is lower than you think",
   "kind": "The requirement, and why it is not dumbing down",
   "body": ["<b>Short sentences, common words, one idea at a time, "
            "and the point first</b> — which helps readers with "
            "dyslexia, with cognitive conditions, in a second language, "
            "and under time pressure.",
            "<b>And expand abbreviations and define jargon on first "
            "use</b> — <b>which is a mechanical requirement, not a "
            "judgement</b>, and is checkable.",
            "<b>Plus declare the language of the page and of any "
            "passage in another language</b>, <b>because a screen "
            "reader pronounces using that declaration</b> and gets it "
            "audibly wrong without it.",
            "<b>And this is not dumbing down:</b> <b>precise "
            "technical content can be written plainly</b>, and the "
            "difficulty of the prose is independent of the difficulty of "
            "the idea — which is a claim this program's own writing "
            "tries to honour."]},

  {"t": "section", "label": "Part 4", "title": "Errors",
   "blurb": "Where cognitive accessibility and good design are the "
            "same thing."},

  {"t": "code", "kicker": "Errors", "title": "Prevention, identification, and recovery",
   "lang": "text", "code": """
  PREVENT
      constrain the input instead of validating it
      format the field as the user types
      accept every reasonable form of the answer
      and do not ask for what you already know

  IDENTIFY
      say which field, in text, next to the field
      say what is wrong, specifically
      and not only in colour (Module 03 section 3)

  RECOVER
      say how to fix it, not only that it is wrong
      preserve everything already entered
      allow review before anything irreversible
      and allow reversal afterwards where possible

  WHICH IS CSCE 671 SECTION 05's error material,
  arriving as an access requirement -- because a
  recoverable error costs a moment and an
  unrecoverable one ends the task.
""",
   "caption": "<b>A recoverable error costs a moment and an "
              "unrecoverable one ends the task</b> — which is why "
              "error design is an access requirement rather than a "
              "nicety.",
   "note": "The prevent-identify-recover structure is worth "
           "memorising."},

  {"t": "callout", "title": "And the honest closing position",
   "kind": "Closing",
   "body": ["<b>Everything in this module benefits everybody, "
            "measurably and immediately</b> — <b>which makes it the "
            "strongest curb cut in the course</b> and also the reason it "
            "is treated as optional polish.",
            "<b>And the gap between the population and the standard's "
            "coverage is the largest in the subject</b>, which means "
            "<b>conformance is least informative here</b> "
            "(Module 07 §4).",
            "<b>So the test is not a checklist but a "
            "count:</b> <b>how many things must the user hold in mind, "
            "how many steps, how many words, how many unrecoverable "
            "actions</b> — and each is reducible.",
            "<b>Which is the one module where 'make it simpler' is "
            "the whole requirement</b> — <b>and where your own "
            "fluency with your own interface is the thing most likely to "
            "mislead you</b> (Module 01 §4)."]},
 ],
 "takeaways": [
   "The cognitive requirements are the largest in population and the "
   "thinnest in the standard, because they resist the measured-not-judged "
   "property.",
   "Pretending a qualitative requirement is a checkbox produces compliance "
   "without benefit.",
   "Allowing interruption and resumption is the requirement attention "
   "conditions most need and almost nothing provides.",
   "Declare the language of the page and of foreign passages, because a "
   "screen reader pronounces from that declaration.",
   "Plain writing is not dumbing down: the difficulty of the prose is "
   "independent of the difficulty of the idea.",
   "A recoverable error costs a moment and an unrecoverable one ends the "
   "task, which is why error design is an access requirement.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why this is underserved"),
  ("callout", "The cognitive requirements are the largest in population and "
              "the weakest in the standard",
   ["<b>Cognitive, learning, and attention-related conditions are "
    "collectively the most common category of disability</b> — and "
    "<b>the standard's coverage of them is the thinnest and the most "
    "qualitative</b> of any area it addresses, which is a mismatch worth "
    "naming.",
    "<b>Because the requirements resist the measured-not-judged "
    "property</b> that makes the contrast criterion so effective "
    "(Module 03 &sect;3): <b>'is this simple enough' has no "
    "threshold</b>, <b>and a criterion without a threshold is very hard "
    "to enforce</b> — so the standard either omits it or states it "
    "at a level nobody is required to meet.",
    "<b>Which is a limitation of the standard rather than of the "
    "requirement</b> — <b>and Module 07 &sect;4 is about exactly "
    "that distinction</b>: what a standard can encode, and what it "
    "therefore leaves to you.",
    "<b>So this module is more design guidance than checklist</b>, "
    "<b>stated openly</b>, because <b>pretending a qualitative "
    "requirement is a checkbox produces compliance without benefit</b> "
    "— which is the characteristic failure of accessibility "
    "programmes and Module 12 &sect;3's subject."]),

  ("h1", "2 &nbsp; Memory and attention"),
  ("ul", ["<b>Do not require remembering across steps</b> — "
          "<b>show the reference code on the page that asks for it</b>, "
          "show the email address on the page that asks you to confirm "
          "it — <b>which is CSCE 671 Module 03's "
          "recognition-over-recall principle</b> as an access "
          "requirement.",
          "<b>Do not require remembering across modes</b> — <b>a "
          "modal dialogue that covers the information it is asking about "
          "is the specific and extremely common version of this</b>, and "
          "it is a layout decision rather than a hard problem.",
          "<b>Keep the sequence short and show the position within "
          "it</b> — <b>'step 2 of 4' costs nothing and removes a "
          "sustained background uncertainty</b> about how much is left, "
          "which consumes attention continuously.",
          "<b>Allow interruption and resumption</b> — <b>which "
          "is the requirement attention conditions most need and almost "
          "nothing provides</b>: <b>save the partial state</b>, so that "
          "leaving and returning is not starting again. This is also "
          "&sect;4's data-preservation requirement.",
          "<b>And remove involuntary attention capture</b> — "
          "<b>motion, autoplay, carousels, notification badges, and "
          "sudden layout shift all take attention whether or not it can "
          "be spared</b> (CSCE 671 Module 06 and CSCE 679 "
          "Module 02 &sect;3's emphasis budget) — and the user "
          "cannot choose not to notice them."]),

  ("break",),
  ("h1", "3 &nbsp; Language"),
  ("callout", "Write for the lowest reading demand the content allows, which "
              "is lower than you think",
   ["<b>Short sentences, common words, one idea per sentence, and "
    "the point before the explanation</b> — <b>which helps readers "
    "with dyslexia, with cognitive conditions, reading in a second "
    "language, and anybody reading under time pressure</b>, which over a "
    "population is nearly everybody at some point.",
    "<b>And expand abbreviations and define jargon on first "
    "use</b> — <b>which is a mechanical requirement rather than a "
    "judgement</b>, <b>and is therefore checkable</b>, unlike most of "
    "this module.",
    "<b>Plus declare the language of the page and of any passage in "
    "another language</b> — <b>because a screen reader selects its "
    "pronunciation rules from that declaration</b> and <b>gets it "
    "audibly and sometimes incomprehensibly wrong without it</b>, which "
    "is a one-attribute fix for a total failure.",
    "<b>And this is not dumbing down</b>: <b>precise technical "
    "content can be written plainly</b>, <b>and the difficulty of the "
    "prose is independent of the difficulty of the idea</b> — which "
    "is a claim this program's own writing tries to honour, and which "
    "you are entitled to check on it."]),

  ("h1", "4 &nbsp; Errors"),
  ("code", """PREVENT
    constrain the input instead of validating it
    format the field as the user types
    accept every reasonable form of the answer
    and do not ask for what you already know

IDENTIFY
    say which field, in text, next to the field
    say what is wrong, specifically
    and not only in colour (Module 03 section 3)

RECOVER
    say how to fix it, not only that it is wrong
    preserve everything already entered
    allow review before anything irreversible
    and allow reversal afterwards where possible

WHICH IS CSCE 671 SECTION 05's error material,
arriving as an access requirement -- because a
recoverable error costs a moment and an unrecoverable
one ends the task."""),
  ("callout", "And the honest closing position",
   ["<b>Everything in this module benefits everybody, measurably and "
    "immediately</b> — <b>which makes it the strongest curb cut in "
    "the course</b> (Module 01 &sect;2) <b>and also, perversely, the "
    "reason it is treated as optional polish</b> rather than as an "
    "access requirement with a population behind it.",
    "<b>And the gap between the size of the population and the "
    "standard's coverage is the largest in the subject</b>, which means "
    "<b>a conformance claim is least informative here</b> "
    "(Module 07 &sect;4) — a fully conformant interface may still "
    "be cognitively unusable, and nothing in the claim says otherwise.",
    "<b>So the test is not a checklist but a count:</b> <b>how many "
    "things must the user hold in mind, how many steps are there, how "
    "many words, how many unrecoverable actions</b> — <b>and every "
    "one of those is reducible</b>, which makes the count actionable "
    "even without a threshold.",
    "<b>Which makes this the one module where 'make it simpler' is "
    "the whole requirement</b> — <b>and where your own fluency with "
    "your own interface is the thing most likely to mislead you</b>, "
    "because you cannot experience it as unfamiliar (Module 01 "
    "&sect;4's shared error, and CSCE 671 Module 01 &sect;2)."]),
 ],
 "resources": [
   ("The W3C Cognitive Accessibility materials (free)",
    "https://www.w3.org/WAI/cognitive/",
    "<b>The whole module</b> — the task force's guidance, which is "
    "more detailed than the standard itself and is the right source "
    "here."),
   ("Making Content Usable for People with Cognitive and Learning "
    "Disabilities (free)",
    "https://www.w3.org/TR/coga-usable/",
    "<b>&sect;&sect;2 to 4 in depth</b>, with patterns and the "
    "user-need statements behind them."),
   ("The UK Government Digital Service content guidance (free)",
    "https://www.gov.uk/guidance/content-design",
    "<b>&sect;3 as working practice</b> — plain writing applied to "
    "genuinely complex content, which is the proof that it is not "
    "dumbing down."),
   ("Understanding WCAG 3.3.x on input assistance (free)",
    "https://www.w3.org/WAI/WCAG22/Understanding/",
    "<b>&sect;4's criteria</b> — error identification, suggestion, "
    "and prevention for consequential actions."),
 ],
 "exercises": [
   "<b>State why this area resists the measured-not-judged "
   "property</b>, and what follows.",
   "<b>Find one place your interface requires remembering across "
   "steps</b>, and fix it.",
   "<b>Find a modal that hides what it asks about.</b>",
   "<b>Add a position indicator</b> to one multi-step flow.",
   "<b>Make one flow interruptible</b>, with its partial state "
   "saved.",
   "<b>List every involuntary attention capture</b> in one interface "
   "you use.",
   "<b>Rewrite one page of your own technical writing</b> for the "
   "lowest reading demand it allows.",
   "<b>Check the language declarations</b> on a multilingual page, and "
   "listen to it.",
   "<b>Audit one form against prevent-identify-recover</b>, all "
   "three.",
   "<b>Count the unrecoverable actions</b> in your interface, and make "
   "one reversible.",
 ],
 "selfcheck": [
   "Why is this area the largest and least covered?",
   "What property do these requirements resist, and why does that "
   "matter?",
   "What does pretending they are checkboxes produce?",
   "Give five ways to reduce memory and attention demand.",
   "Which is most needed and least provided?",
   "State the language requirements, including the technical one.",
   "Why is plain writing not dumbing down?",
   "Give the three error stages and two items under each.",
   "Why is error design an access requirement?",
   "What is the test here, if not a checklist?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "The Standard",
 "subtitle": "WCAG's structure, and what a conformance claim means.",
 "question": "What does 'AA conformant' actually tell you?",
 "outcomes": [
     "Explain WCAG's structure and the POUR principles.",
     "Explain the conformance levels and their basis.",
     "State what a conformance claim establishes.",
     "Explain what a standard can and cannot encode.",
     "Use the standard as a floor rather than a target.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The structure",
   "blurb": "Which is what makes the document usable."},

  {"t": "code", "kicker": "Structure", "title": "Four levels of nesting, and why",
   "lang": "text", "code": """
  4 PRINCIPLES -- POUR
      Perceivable    available to a sense you have
      Operable       usable with the inputs you have
      Understandable content and behaviour both
      Robust         works with assistive technology
                     now and later

  THEN GUIDELINES under each principle
      goals, not testable -- they organise

  THEN SUCCESS CRITERIA under each guideline
      testable statements, pass or fail
      each at level A, AA, or AAA
      technology-independent by design

  THEN TECHNIQUES, which are NOT normative
      sufficient techniques: one way to pass
      failures: known ways to fail
      and you may pass by other means

  SO: criteria are the requirement, techniques are
  advice. Confusing the two is the commonest error in
  using the document.
""",
   "caption": "<b>Criteria are the requirement and techniques are "
              "advice</b> — confusing the two is the commonest error "
              "in using the document.",
   "note": "The criteria-versus-techniques distinction is the "
           "practical key to the standard."},

  {"t": "callout", "title": "And POUR is a good decomposition, which is worth saying because most acronyms are not",
   "kind": "Why the principles are useful rather than decorative",
   "body": ["<b>Perceivable, Operable, Understandable, Robust map "
            "onto genuinely different failure modes</b> — <b>can it "
            "reach your senses; can you drive it; can you follow it; "
            "does it survive your technology.</b>",
            "<b>And they are roughly ordered by "
            "consequence</b> — <b>an imperceptible interface is a "
            "total failure and an understandability problem is a partial "
            "one</b>, which is a useful triage "
            "order.",
            "<b>Plus Robust is the one people skip and is the one "
            "that ages</b> — <b>it is the semantics requirement</b>, "
            "and it is why Module 08 exists.",
            "<b>So the principles are worth using as a diagnostic "
            "frame</b>: given a defect, ask which letter it breaks, "
            "<b>which usually identifies the fix's "
            "category</b> immediately."]},

  {"t": "section", "label": "Part 2", "title": "The levels",
   "blurb": "And what A, AA, and AAA actually mean."},

  {"t": "table", "kicker": "Levels", "title": "The conformance levels, and their real basis",
   "header": ["Level", "What it means", "In practice"],
   "widths": [1.9, 4.6, 4.6],
   "rows": [
     ["<b>A</b>", "<b>Minimum; its absence blocks whole groups</b>", "<b>Not optional, and not sufficient</b>"],
     ["<b>AA</b>", "<b>Achievable across content types without redesign</b>", "<b>The usual legal and procurement target</b>"],
     ["<b>AAA</b>", "<b>Not achievable for all content</b>", "<b>Target where it applies; not claimable site-wide</b>"],
   ],
   "footnote": "<b>The levels are about achievability, not about "
               "importance</b> — a AAA criterion is not a nicety, it "
               "is one that cannot be required of every kind of "
               "content.",
   "note": "The achievability-not-importance point is widely "
           "misunderstood and changes how you read the "
           "levels."},

  {"t": "callout", "title": "And conformance is all-or-nothing per page, which has consequences",
   "kind": "How the claim is actually constructed",
   "body": ["<b>A page conforms at a level only if every criterion "
            "at that level and below is met</b> — <b>there is no "
            "partial credit</b>, and one failure fails the "
            "page.",
            "<b>And a process must conform end to end</b> — "
            "<b>a conformant checkout with one inaccessible step is a "
            "non-conformant checkout</b>, which is the "
            "full-pages-and-complete-processes requirement.",
            "<b>Which makes honest claims hard and dishonest ones "
            "easy</b> — <b>'AA conformant' is asserted far more often "
            "than it is true</b>, and Module 09 §1 explains how that "
            "happens without anybody lying.",
            "<b>So a claim should name what was tested, how, and "
            "when</b> — which is Module 13 §2's form and is what a "
            "serious accessibility statement contains."]},

  {"t": "section", "label": "Part 3", "title": "What it establishes",
   "blurb": "Which is less than the word 'conformant' suggests."},

  {"t": "bullets", "kicker": "The claim", "title": "What a conformance claim does and does not say",
   "items": [
     "<b>It says: these specific testable statements were "
     "checked and passed</b>, which is real information and is worth "
     "having.",
     "",
     "<b>It does not say the interface is usable</b> — "
     "<b>every criterion can pass while the task remains "
     "impractical</b>, which Module 09 §3 demonstrates with "
     "examples.",
     "",
     "<b>It does not cover cognitive accessibility "
     "adequately</b>, for Module 06 §1's "
     "reasons.",
     "",
     "<b>And it says nothing about whether anybody with a "
     "disability was involved</b> — <b>which is the question "
     "Module 09 §4 is about and the one that matters "
     "most.</b>",
     "",
     "<b>So treat it as a floor</b>: necessary, checkable, "
     "insufficient.",
   ],
   "footnote": "<b>Necessary, checkable, insufficient</b> — which "
               "is the honest three-word summary of what a conformance "
               "claim is worth."},

  {"t": "section", "label": "Part 4", "title": "What a standard can encode",
   "blurb": "A general point, arrived at here."},

  {"t": "callout", "title": "A standard can only require what can be tested the same way by two people",
   "kind": "Closing, and the general lesson",
   "body": ["<b>Which is why contrast has a number and simplicity "
            "does not</b> — <b>the testability requirement is what "
            "makes a standard enforceable, and it is also what "
            "determines its coverage.</b>",
            "<b>So the gaps are not oversights</b> — <b>they are "
            "the requirements that resisted operationalisation</b>, "
            "which is Module 06 §1's gap seen from the standard's "
            "side.",
            "<b>And this generalises:</b> <b>any metric-driven "
            "process is shaped by what is measurable rather than by what "
            "matters</b> — which is CSCE 671 §12 §4 and "
            "CSCE 676 §13's proxy problem, in a third "
            "setting.",
            "<b>So use the standard for what it is good "
            "at</b> — <b>the mechanical, checkable, arguable "
            "requirements</b> — <b>and do not mistake the covered set "
            "for the required set.</b>"]},
 ],
 "takeaways": [
   "Criteria are the requirement and techniques are advice; confusing them "
   "is the commonest error in using the document.",
   "POUR maps onto genuinely different failure modes and is roughly ordered "
   "by consequence.",
   "The conformance levels are about achievability, not importance — a "
   "AAA criterion is not a nicety.",
   "Conformance is all-or-nothing per page and per complete process, which "
   "makes honest claims hard and dishonest ones easy.",
   "A conformance claim is necessary, checkable, and insufficient.",
   "A standard can only require what two people can test the same way, "
   "which determines its coverage as well as its enforceability.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The structure"),
  ("code", """4 PRINCIPLES -- POUR
    Perceivable    available to a sense you have
    Operable       usable with the inputs you have
    Understandable content and behaviour both
    Robust         works with assistive technology,
                   now and in the future

THEN GUIDELINES under each principle
    goals, not testable -- they organise the criteria

THEN SUCCESS CRITERIA under each guideline
    testable statements, pass or fail
    each at level A, AA, or AAA
    technology-independent by design

THEN TECHNIQUES, which are NOT normative
    sufficient techniques: one way to pass
    failures: known ways to fail
    and you may pass by other means entirely

SO: criteria are the requirement, techniques are
advice. Confusing the two is the commonest error in
using the document."""),
  ("p", "<b>Criteria are the requirement and techniques are "
        "advice</b> — <b>confusing the two is the commonest error in "
        "using the document</b>, and it goes in both directions: people "
        "treat a sufficient technique as mandatory (it is one way, not "
        "the way) and people treat the absence of a technique as "
        "permission (the criterion still applies). <b>The "
        "criteria-versus-techniques distinction is the practical key to "
        "the standard</b>, and knowing it makes the document far less "
        "intimidating."),
  ("callout", "And POUR is a good decomposition, which is worth saying "
              "because most acronyms are not",
   ["<b>Perceivable, Operable, Understandable, Robust map onto "
    "genuinely different failure modes</b> — <b>can the information "
    "reach a sense you have; can you drive the interface with the inputs "
    "you have; can you follow the content and the behaviour; does it "
    "survive your particular assistive technology.</b>",
    "<b>And they are roughly ordered by consequence</b> — <b>an "
    "imperceptible interface is a total failure and an understandability "
    "problem is usually a partial one</b> — <b>which makes the "
    "order a useful triage sequence</b> when you have more defects than "
    "time.",
    "<b>Plus Robust is the one people skip and is the one that "
    "ages</b> — <b>it is the semantics requirement</b>: markup that "
    "correctly declares what things are keeps working with assistive "
    "technologies nobody has written yet. <b>It is why Module 08 "
    "exists</b>, and it is the principle with the longest shelf "
    "life.",
    "<b>So the principles are worth using as a diagnostic frame</b>: "
    "<b>given a defect, ask which letter it breaks</b>, <b>which usually "
    "identifies the fix's category immediately</b> — a Perceivable "
    "failure wants an alternative, an Operable one wants an input path, a "
    "Robust one wants semantics."]),

  ("h1", "2 &nbsp; The levels"),
  ("table", ["Level", "What it actually means", "In practice"],
   [["<b>A</b>",
     "<b>The minimum. Its absence blocks entire groups of users "
     "completely.</b>",
     "<b>Not optional, and not sufficient either</b> — an "
     "A-conformant page can still be very hard to use."],
    ["<b>AA</b>",
     "<b>Achievable across content types without a fundamental "
     "redesign or a change of medium.</b>",
     "<b>The usual legal and procurement target</b>, and the level "
     "almost every policy names."],
    ["<b>AAA</b>",
     "<b>Not achievable for all content</b> — some criteria are "
     "impossible for some media (sign interpretation of live audio, "
     "for instance).",
     "<b>Target it where it applies to your content; it is not "
     "claimable site-wide</b> and the standard says so."]],
   [0.12, 0.46, 0.42]),
  ("p", "<b>The levels are about achievability, not about "
        "importance</b> — <b>a AAA criterion is not a nicety, it is "
        "one that cannot reasonably be required of every kind of "
        "content</b>. The enhanced contrast ratio at AAA matters a great "
        "deal to the people who need it; it sits at AAA because requiring "
        "7:1 everywhere would constrain design more than the standard was "
        "willing to. <b>The achievability-not-importance point is widely "
        "misunderstood and changes how you read the levels</b>: AAA is a "
        "list of things to do where you can, not a list of things that "
        "barely matter."),
  ("callout", "And conformance is all-or-nothing per page, which has "
              "consequences",
   ["<b>A page conforms at a level only if every criterion at that "
    "level and every level below it is met</b> — <b>there is no "
    "partial credit</b>, and <b>one failure fails the page</b>, which is "
    "a stricter rule than most people assume.",
    "<b>And a complete process must conform end to end</b> — "
    "<b>a conformant checkout with one inaccessible step is a "
    "non-conformant checkout</b>, because the conformance unit is the "
    "whole process — <b>which is the full-pages-and-complete-"
    "processes requirement</b> and is the part most often ignored.",
    "<b>Which makes honest claims hard and dishonest ones easy</b> "
    "— <b>'AA conformant' is asserted very much more often than it "
    "is true</b>, <b>and Module 09 &sect;1 explains how that happens "
    "without anybody intending to lie</b>: an automated tool returns "
    "green, and green is read as conformant.",
    "<b>So a claim should name what was tested, how, and when</b> "
    "— <b>which is Module 13 &sect;2's form</b> and <b>is what a "
    "serious accessibility statement actually contains</b>, including the "
    "known exceptions."]),

  ("break",),
  ("h1", "3 &nbsp; What it establishes"),
  ("ul", ["<b>It says: these specific testable statements were checked "
          "and passed</b> — <b>which is real information and is "
          "genuinely worth having</b>, and is more than most software "
          "can say about any of its quality attributes.",
          "<b>It does not say the interface is usable</b> — "
          "<b>every single criterion can pass while the task remains "
          "impractical</b>, <b>which Module 09 &sect;3 demonstrates "
          "with concrete examples</b> (a conformant but unusable form, a "
          "correctly labelled but hopeless navigation).",
          "<b>It does not cover cognitive accessibility "
          "adequately</b>, for <b>Module 06 &sect;1's reasons</b> "
          "— so conformance is least informative for the largest "
          "population.",
          "<b>And it says nothing whatever about whether anybody with "
          "a disability was involved in the testing</b> — <b>which "
          "is the question Module 09 &sect;4 is about and the one that "
          "matters most</b>, and which no conformance level "
          "requires.",
          "<b>So treat it as a floor</b>: <b>necessary, checkable, "
          "insufficient</b> — <b>which is the honest three-word "
          "summary of what a conformance claim is worth</b>, and is not "
          "a dismissal: a floor is load-bearing."]),

  ("h1", "4 &nbsp; What a standard can encode"),
  ("callout", "A standard can only require what can be tested the same way by "
              "two people",
   ["<b>Which is why contrast has a number and simplicity does "
    "not</b> — <b>the inter-rater testability requirement is what "
    "makes a standard enforceable</b>, <b>and it is also what determines "
    "its coverage</b>: anything two careful people would score "
    "differently cannot be a criterion.",
    "<b>So the gaps are not oversights</b> — <b>they are "
    "precisely the requirements that resisted operationalisation</b>, "
    "<b>which is Module 06 &sect;1's gap seen from the standard's "
    "side</b> rather than from the population's.",
    "<b>And this generalises well beyond accessibility:</b> <b>any "
    "metric-driven process is shaped by what is measurable rather than by "
    "what matters</b> — which is <b>CSCE 671 Module 12 &sect;4's "
    "argument and CSCE 676 Module 13's proxy problem, arriving in a "
    "third setting</b> and with the same structure each time.",
    "<b>So use the standard for what it is good at</b> — <b>the "
    "mechanical, checkable, arguable requirements, which it encodes "
    "extremely well</b> — <b>and do not mistake the covered set for "
    "the required set</b>, which is the error the rest of this course is "
    "arranged to prevent."]),
 ],
 "resources": [
   ("WCAG 2.2, with the quick reference (free)",
    "https://www.w3.org/WAI/WCAG22/quickref/",
    "<b>The document itself</b> — and read the structure before any "
    "individual criterion, because the structure is the navigation."),
   ("Understanding WCAG 2.2 (free)",
    "https://www.w3.org/WAI/WCAG22/Understanding/",
    "<b>&sect;&sect;1 and 2</b> — the intent behind each criterion, "
    "which is where the reasoning lives and the part worth actually "
    "reading."),
   ("WCAG 2.2 conformance requirements (free)",
    "https://www.w3.org/TR/WCAG22/#conformance",
    "<b>&sect;2's callout</b> — the five conformance requirements, "
    "including full pages and complete processes."),
   ("The W3C's accessibility statement generator (free)",
    "https://www.w3.org/WAI/planning/statements/",
    "<b>&sect;2's honest claim</b> — what a statement should contain, "
    "including known exceptions and a contact route."),
 ],
 "exercises": [
   "<b>State POUR</b> and give one failure under each principle.",
   "<b>Classify ten defects</b> from Project 1 by principle.",
   "<b>Find a sufficient technique</b> and a different way of passing "
   "the same criterion.",
   "<b>Explain the levels to somebody</b> without saying that AAA is "
   "less important.",
   "<b>Find a AAA criterion</b> that matters greatly to the people who "
   "need it.",
   "<b>Take one multi-step process</b> and test every step, not only "
   "the main page.",
   "<b>Find a published 'AA conformant' claim</b> and test three "
   "criteria on it.",
   "<b>Write an honest accessibility statement</b> for something you "
   "built.",
   "<b>Name three requirements from Module 06</b> that no criterion "
   "encodes, and say why.",
   "<b>State the general lesson about standards</b> in your own "
   "words.",
 ],
 "selfcheck": [
   "Give WCAG's four structural levels.",
   "What is the difference between a criterion and a technique?",
   "State POUR, with a failure mode for each.",
   "Why is Robust the one that ages well?",
   "What do the conformance levels measure?",
   "Why is AAA not claimable site-wide?",
   "State the two all-or-nothing rules.",
   "What does a conformance claim establish, in three words?",
   "Name three things it does not establish.",
   "What can a standard require, and what follows about its gaps?",
 ],
},

]
