# -*- coding: utf-8 -*-
"""CSCE 632 Accessible Computing — original course content."""

COURSE = {
    "code": "CSCE 632",
    "title": "Accessible Computing",
    "tagline": "Design for the constraint, and the design gets better for "
               "everybody",
    "term": "Semester 11 (with CSCE 671 and CSCE 679)",
    "prereqs": "CSCE 671 Human-Computer Interaction, particularly its "
               "Modules 02 and 09; CSCE 679 Data Visualization for "
               "Module 10; any course in which you built an interface "
               "somebody else used",
    "deliverable": "An accessibility repair of something you built "
                   "earlier — audited against the standard, tested "
                   "with the actual assistive technology, with the "
                   "automated tools' coverage measured rather than "
                   "assumed, and the remaining defects listed",
    "effort": "11–13 hours per week · 13 modules + 2 project weeks",
    "description": [
        "<b>This course takes a position in Module 01 and spends "
        "twelve modules making it operational.</b> <b>The position is "
        "that a disability is a mismatch between a body and an "
        "environment, and that software is part of the "
        "environment</b> — so <b>an interface a blind user cannot "
        "operate is a defect in the interface</b>, which is a "
        "statement about engineering rather than about "
        "accommodation.",
        "<b>The first half is the specific requirements, by "
        "capability rather than by diagnosis.</b> <b>Vision, hearing, "
        "motor control, and cognition each impose concrete "
        "constraints</b> (Modules 03 through 06) — and <b>each "
        "constraint has a test you can run in minutes</b>, which is "
        "what makes this checkable rather than aspirational.",
        "<b>The second theme is that the standard is a floor and not "
        "a design.</b> <b>Module 07 covers WCAG properly</b>, "
        "including <b>what a conformance claim does and does not "
        "establish</b> — because <b>a page can satisfy every "
        "automatically checkable criterion and still be unusable</b>, "
        "and Module 09 measures how large that gap actually is.",
        "<b>The third is that the mechanism matters more than the "
        "checklist.</b> <b>Module 08 is about the accessibility tree "
        "and the name-role-value model</b> — <b>because once you "
        "understand what an assistive technology actually "
        "receives</b>, most of the rules become derivable rather than "
        "memorised, which is the same move CSCE 671 Module 05 "
        "makes.",
        "<b>And the closing argument is the one that makes this a "
        "design course.</b> <b>Designing for a constraint improves the "
        "design for everybody</b> — captions are used most by people "
        "who can hear, and keyboard access is what power users "
        "want — so <b>Module 13's honest claim is a quality claim, "
        "and the accessibility argument does not need charity to "
        "work.</b>",
    ],
    "outcomes": [
        "State the social and medical models and what follows from "
        "each.",
        "Describe the range of disability, including temporary and "
        "situational.",
        "State and test the requirements that vision imposes.",
        "State and test the requirements for hearing and speech.",
        "State and test the requirements for motor control.",
        "State the cognitive and attentional requirements.",
        "Explain WCAG's structure and what conformance establishes.",
        "Explain the accessibility tree and the name-role-value "
        "model.",
        "Test accessibility, and state what each method catches.",
        "Make data and visual representations non-visually "
        "available.",
        "Address accessibility in games and real-time graphics.",
        "Explain why accessibility fails organisationally.",
        "Claim accessibility honestly, and say what you tested.",
    ],
    "materials": [
        ("The W3C WAI materials, including the tutorials and "
         "Understanding WCAG (free)",
         "https://www.w3.org/WAI/",
         "<b>The primary source for Modules 03 through 08</b>, free in "
         "full. The Understanding documents give the reason behind each "
         "criterion, which is the part worth reading — the criteria "
         "themselves are terse by design."),
        ("WCAG 2.2, with the quick reference (free)",
         "https://www.w3.org/WAI/WCAG22/quickref/",
         "<b>Module 07's object of study.</b> Read the structure "
         "first — principles, guidelines, criteria, levels — "
         "because the structure is what makes the document navigable."),
        ("The ARIA Authoring Practices Guide (free)",
         "https://www.w3.org/WAI/ARIA/apg/",
         "<b>Module 08.</b> Patterns with their keyboard interactions "
         "and their markup, and the first rule of ARIA is stated "
         "early and should be believed."),
        ("Microsoft's Inclusive Design toolkit (free)",
         "https://inclusive.microsoft.com/",
         "<b>Module 02's permanent, temporary, and situational "
         "framing</b> comes from here, and it is the most persuasive "
         "single page in the subject."),
        ("The Game Accessibility Guidelines (free)",
         "https://gameaccessibilityguidelines.com/",
         "<b>Module 11.</b> Organised by effort rather than by "
         "disability, which makes it unusually usable mid-project."),
        ("Lazar, Goldstein & Taylor — Ensuring Digital "
         "Accessibility through Process and Policy",
         "https://www.elsevier.com/books/ensuring-digital-accessibility-through-process-and-policy/lazar/978-0-12-800646-7",
         "<b>Module 12.</b> Why accessibility fails for "
         "organisational rather than technical reasons, which is the "
         "part engineering courses omit. Library copy."),
        ("The WebAIM Million annual report (free)",
         "https://webaim.org/projects/million/",
         "<b>Module 09's measurement.</b> An automated audit of a "
         "million home pages, repeated yearly — and the numbers are "
         "worse than anybody expects and are not improving "
         "quickly."),
    ],
    "tooling": [
        "<b>A screen reader, and you have to learn to use it</b> "
        "— <b>NVDA on Windows, VoiceOver on macOS and iOS, TalkBack "
        "on Android</b>, all free or built in. <b>Module 03 §2 is "
        "where you learn the navigation model</b>, and an hour spent "
        "there changes how you write markup permanently.",
        "<b>Your keyboard, with the mouse unplugged</b> — which is "
        "<b>the cheapest accessibility test that exists</b> and catches "
        "a large fraction of real defects "
        "(Module 05 §2).",
        "<b>An automated checker</b> — <b>axe, WAVE, or "
        "Lighthouse</b> — and <b>Module 09 §1 reports what "
        "fraction of criteria these can check at all</b>, which is the "
        "number to know before trusting a green result.",
        "<b>A contrast checker and a colour-vision simulator</b>, "
        "run on every figure and every interface "
        "(Modules 03 §3 and CSCE 679 Module 04).",
        "<b>Operating system magnification, at 400%</b>, and "
        "<b>browser zoom at 400% with reflow</b> — which breaks more "
        "layouts than anything else on this list.",
        "<b>And, where you can arrange it, somebody who uses "
        "assistive technology daily</b> — <b>which finds a class of "
        "problem no checklist contains</b>, and Module 09 §4 is about "
        "arranging that properly and paying for it.",
    ],
    "projects": [
        {"n": 1, "after": 6,
         "title": "Audit something you built",
         "brief": "Take your own earlier interface and find out what it "
                  "excludes.",
         "reqs": [
           "<b>Something you built and shipped or submitted "
           "earlier</b> — <b>your own work, because the exercise is "
           "about your habits</b> rather than about somebody else's "
           "code.",
           "<b>The keyboard-only pass first</b> "
           "(Module 05 §2), with every unreachable control "
           "listed.",
           "<b>A screen reader pass</b> (Module 03 §2), recording "
           "what is announced for each control and what is "
           "silent.",
           "<b>The contrast and colour-vision checks</b> "
           "(Module 03 §3), with the failures measured rather than "
           "judged.",
           "<b>An automated checker run</b>, and <b>the defects it "
           "missed that you found manually, counted</b>.",
           "<b>And each defect classified by the capability it "
           "excludes</b> rather than by the criterion number, which is "
           "what makes the list actionable.",
         ],
         "done": [
           "<b>The manual findings exceeding the automated "
           "ones</b> — <b>which they will, substantially</b>, and the "
           "ratio is the point of the exercise "
           "(Module 09 §1).",
           "<b>Every defect tied to a capability</b>, so that the "
           "repair is a design decision rather than a compliance "
           "edit.",
           "<b>The screen reader transcript included</b>, because "
           "<b>what is actually announced is frequently not what you "
           "assumed</b>.",
           "<b>And the honest total.</b> <b>A first audit of your own "
           "work finds more than you expect</b>, and reporting that "
           "accurately is the assessed behaviour.",
         ]},
        {"n": 2, "after": 12,
         "title": "Repair it, and prove the repair",
         "brief": "Fix what you found, test it with the technology, and "
                  "state what remains.",
         "reqs": [
           "<b>The defects from Project 1 repaired</b>, with "
           "<b>each repair justified from the mechanism</b> "
           "(Module 08) rather than from a rule.",
           "<b>Native elements preferred over ARIA</b> wherever "
           "possible, and <b>every ARIA use justified</b> "
           "(Module 08 §3's first rule).",
           "<b>Re-tested with the actual assistive technology</b>, "
           "not only with the checker — <b>and the transcripts "
           "before and after</b>.",
           "<b>The 400% zoom and reflow case handled</b>, which is "
           "where most layouts fail.",
           "<b>One non-visual representation of a figure or "
           "data</b> (Module 10), which is the hardest requirement "
           "here.",
           "<b>And a remaining-defects list that is specific and "
           "non-empty</b>, in Module 13 §2's form.",
         ],
         "done": [
           "<b>The repairs justified from the accessibility tree "
           "rather than from the criterion</b> — <b>which is the "
           "difference between understanding this and passing it</b> "
           "(Module 08).",
           "<b>Tested with the technology</b>, because <b>a checker "
           "pass is not evidence that anybody can use it</b> "
           "(Module 09 §1).",
           "<b>The remaining-defects list non-empty and "
           "specific</b> — <b>a claim of full accessibility fails "
           "this project</b>, for the reasons Module 13 §1 gives.",
           "<b>And at least one repair that improved the interface "
           "for everybody</b>, named as such. <b>That is the course's "
           "central claim</b>, and demonstrating it once on your own "
           "code is what makes it believable.",
         ]},
    ],
    "map": [
        ("The W3C WAI tutorials and Understanding WCAG (free)",
         "https://www.w3.org/WAI/tutorials/",
         "<b>Modules 03 through 08</b>, free in full — and the "
         "Understanding documents carry the reasons."),
        ("WCAG 2.2 quick reference (free)",
         "https://www.w3.org/WAI/WCAG22/quickref/",
         "<b>Module 07.</b> The criteria themselves, filterable by "
         "level and by technology."),
        ("The ARIA Authoring Practices Guide (free)",
         "https://www.w3.org/WAI/ARIA/apg/",
         "<b>Module 08.</b> The patterns, their keyboard models, and "
         "the first rule of ARIA."),
        ("Microsoft Inclusive Design (free)",
         "https://inclusive.microsoft.com/",
         "<b>Modules 01 and 02.</b> The permanent-temporary-situational "
         "framing, which is the persuasive version of this course's "
         "argument."),
        ("The Game Accessibility Guidelines (free)",
         "https://gameaccessibilityguidelines.com/",
         "<b>Module 11</b>, organised by implementation effort."),
        ("WebAIM's resources and the Million report (free)",
         "https://webaim.org/",
         "<b>Module 09.</b> The screen reader user surveys and the "
         "annual automated audit, which are the field's best public "
         "measurements."),
        ("Teach Access tutorials (free)",
         "https://teachaccess.org/resources/",
         "<b>A structured path through Modules 03 to 08</b>, aimed at "
         "exactly this course's audience."),
    ],
}

MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Disability as a Design Failure",
 "subtitle": "Where the problem is located, and why that decides "
             "everything else.",
 "question": "Who is the defect in?",
 "outcomes": [
     "State the medical and social models and their consequences.",
     "Explain why the location of the problem decides the "
     "engineering.",
     "State the curb-cut argument and its limits.",
     "Explain what this course means by a capability.",
     "Place this course relative to CSCE 671 and CSCE 679.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two models",
   "blurb": "Which locate the problem in different places."},

  {"t": "callout", "title": "The medical model locates disability in the person and the social model locates it in the mismatch",
   "kind": "The distinction this course is built on",
   "body": ["<b>The medical model says a person is disabled by their "
            "impairment</b> — so <b>the response is to treat the "
            "person, or to accommodate them as an "
            "exception.</b>",
            "<b>The social model says a person is disabled by an "
            "environment built for a narrower range of bodies than "
            "exists</b> — so <b>the response is to fix the "
            "environment.</b>",
            "<b>And software is environment</b>, almost entirely "
            "— <b>which puts the defect in the software</b> and "
            "makes it an engineering problem with an owner.",
            "<b>So this course takes the social model as its working "
            "position</b>, not as an ideological commitment but because "
            "<b>it is the one that generates testable "
            "requirements</b> — and a requirement you can test is what "
            "an engineering course needs."]},

  {"t": "bullets", "kicker": "Consequences", "title": "What follows from each, concretely",
   "items": [
     "<b>Under the medical model, an inaccessible interface is "
     "unfortunate</b>, and the response is a separate accessible "
     "version, requested and provided "
     "individually.",
     "",
     "<b>Under the social model it is a bug</b>, with a severity, "
     "an owner, and a regression test — <b>which is the framing "
     "that gets things fixed in practice.</b>",
     "",
     "<b>And the separate version always loses</b> — <b>it "
     "lags, it has fewer features, and it is the first thing cut</b>, "
     "which is an observed pattern rather than a "
     "prediction.",
     "",
     "<b>So the engineering consequence is: one artefact, built to "
     "work</b> — which is what the rest of this course is "
     "about.",
     "",
     "<b>And this is not a claim that impairments are not "
     "real</b>, which the social model is sometimes accused of; it is "
     "a claim about where the fixable part is.",
   ],
   "footnote": "<b>The separate accessible version always loses</b> "
               "— it lags, it has fewer features, and it is the "
               "first thing cut when the schedule "
               "tightens."},

  {"t": "section", "label": "Part 2", "title": "The curb cut",
   "blurb": "The argument, and an honest statement of its limit."},

  {"t": "callout", "title": "Designing for a constraint improves the design for everybody, and this is observed rather than hoped",
   "kind": "The course's central claim",
   "body": ["<b>Pavement ramps were built for wheelchairs and are "
            "used by anybody with a pushchair, a suitcase, a delivery "
            "trolley, or a bicycle</b> — which is the original "
            "case.",
            "<b>And the software cases are stronger:</b> "
            "<b>captions are used most by people who can hear</b>, "
            "<b>keyboard access is what power users ask for</b>, and "
            "<b>clear language helps everybody under time "
            "pressure.</b>",
            "<b>So the accessibility argument does not require "
            "charity</b> — <b>it is a quality argument</b>, and the "
            "quality argument is the one that survives a budget "
            "meeting.",
            "<b>But the honest limit:</b> <b>not every accessibility "
            "requirement benefits everybody</b> — <b>a screen reader "
            "label benefits exactly the people who need it</b>, and it "
            "is still required. <b>The curb-cut argument is a bonus, "
            "not the justification.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Capabilities",
   "blurb": "Which is how this course organises the requirements."},

  {"t": "callout", "title": "Design against capabilities, not against diagnoses",
   "kind": "Why the modules are organised the way they are",
   "body": ["<b>A diagnosis does not tell you what somebody can "
            "do</b> — <b>two people with the same condition may have "
            "entirely different interaction needs</b>, and the diagnosis "
            "is private information you have no right "
            "to.",
            "<b>A capability does:</b> <b>can this interface be "
            "operated without seeing it, without hearing it, without "
            "fine motor control, without holding several things in "
            "working memory?</b>",
            "<b>Which is testable</b>, by you, today — "
            "<b>unplug the mouse; turn on the screen reader; turn off "
            "the sound</b> — and that is why the course is organised "
            "this way.",
            "<b>And it generalises beyond disability</b>, which is "
            "Module 02's subject: <b>'cannot see the screen' covers "
            "blindness, bright sunlight, and driving</b>, and the "
            "requirement is identical in all three."]},

  {"t": "table", "kicker": "Scope", "title": "The capabilities, and where each is covered",
   "header": ["Capability", "The question", "Module"],
   "widths": [3.0, 5.0, 2.8],
   "rows": [
     ["<b>Vision</b>", "<b>Operable without seeing, or with low vision?</b>", "<b>03</b>"],
     ["<b>Hearing</b>", "<b>Is any information audio-only?</b>", "<b>04</b>"],
     ["<b>Motor</b>", "<b>Operable by keyboard, and without precision?</b>", "<b>05</b>"],
     ["<b>Cognition</b>", "<b>What does it demand of memory and attention?</b>", "<b>06</b>"],
     ["<b>Speech</b>", "<b>Is voice the only input?</b>", "<b>04 §4</b>"],
     ["<b>Photosensitivity</b>", "<b>Does anything flash or move unavoidably?</b>", "<b>11 §3</b>"],
   ],
   "footnote": "<b>Each of these has a test you can run in "
               "minutes</b> — which is what makes the list a working "
               "checklist rather than a statement of "
               "values.",
   "note": "Organising by capability rather than diagnosis is the "
           "structural decision of the course."},

  {"t": "section", "label": "Part 4", "title": "The semester",
   "blurb": "And where this course fits in it."},

  {"t": "callout", "title": "All three Semester 11 courses replace a judgement about taste with a measurement",
   "kind": "Closing",
   "body": ["<b>CSCE 671 replaces 'this feels intuitive' with five "
            "participants and a task</b>; <b>CSCE 679 replaces 'this "
            "chart looks good' with a measured channel ranking</b>; "
            "<b>and this course replaces 'this seems accessible' with "
            "the assistive technology and the standard.</b>",
            "<b>Which is the same move three times</b> — "
            "<b>applied to the interaction, the encoding, and the "
            "access</b> — and it is what makes these three "
            "engineering courses rather than criticism.",
            "<b>And all three correct the same error:</b> "
            "<b>designing for an imagined user who resembles the "
            "designer</b>, which is the failure mode every one of the "
            "three is organised against.",
            "<b>So the question this course keeps "
            "asking</b> — <b>'tested with whom, against "
            "what?'</b> — is CSCE 671's question with the population "
            "widened, and Module 13 is where it is answered "
            "properly."]},
 ],
 "takeaways": [
   "The medical model locates disability in the person and the social model "
   "in the mismatch; software is environment, which puts the defect in the "
   "software.",
   "Under the social model an inaccessible interface is a bug with an owner "
   "and a regression test, which is the framing that gets things fixed.",
   "The separate accessible version always loses: it lags, has fewer "
   "features, and is cut first.",
   "Designing for a constraint improves the design for everybody — but "
   "that is a bonus rather than the justification.",
   "Design against capabilities rather than diagnoses, because a capability "
   "is testable and a diagnosis is private information you have no right "
   "to.",
   "All three Semester 11 courses replace a judgement about taste with a "
   "measurement, and all three correct the same error.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two models"),
  ("callout", "The medical model locates disability in the person and the "
              "social model locates it in the mismatch",
   ["<b>The medical model says a person is disabled by their "
    "impairment</b> — the impairment is the problem and it is "
    "located in them — so <b>the response is to treat the person "
    "where that is possible, and otherwise to accommodate them as an "
    "exception</b> to a system that remains as it was.",
    "<b>The social model says a person is disabled by an environment "
    "built for a narrower range of bodies than actually exists</b> "
    "— the stairs disable the wheelchair user, not the wheelchair "
    "— so <b>the response is to fix the environment.</b>",
    "<b>And software is environment, almost entirely</b>: there is no "
    "physical constraint forcing a button to be unreachable by keyboard "
    "or an image to be unlabelled — <b>which puts the defect "
    "squarely in the software</b> and <b>makes it an engineering problem "
    "with an owner, a severity, and a fix.</b>",
    "<b>So this course takes the social model as its working "
    "position</b>, <b>not as an ideological commitment but because it is "
    "the one that generates testable requirements</b> — and <b>a "
    "requirement you can test is what an engineering course needs</b> "
    "(&sect;3's capability framing is the direct consequence)."]),
  ("ul", ["<b>Under the medical model, an inaccessible interface is "
          "unfortunate</b> — and <b>the response is a separate "
          "accessible version</b>, requested individually and provided as "
          "an accommodation.",
          "<b>Under the social model it is a bug</b>, with a severity, "
          "an owner, a ticket, and a regression test — <b>which is "
          "the framing that actually gets things fixed</b>, because it "
          "routes the work through the process that fixes things.",
          "<b>And the separate version always loses</b> — <b>it "
          "lags the main product, it has fewer features, and it is the "
          "first thing cut when the schedule tightens</b> — which is "
          "<b>an observed pattern across two decades of text-only "
          "alternatives</b> rather than a prediction.",
          "<b>So the engineering consequence is: one artefact, built "
          "to work</b> — which is what the remaining twelve modules "
          "are about, and is also considerably cheaper than maintaining "
          "two.",
          "<b>And none of this is a claim that impairments are not "
          "real</b>, which the social model is sometimes accused of; "
          "<b>it is a claim about where the fixable part is</b>, and the "
          "fixable part is the one an engineer is responsible for."]),

  ("h1", "2 &nbsp; The curb cut"),
  ("callout", "Designing for a constraint improves the design for everybody, "
              "and this is observed rather than hoped",
   ["<b>Pavement ramps were built for wheelchair users and are used "
    "by anybody with a pushchair, a suitcase, a delivery trolley, a "
    "bicycle, or a temporarily injured ankle</b> — which is the "
    "original case and is where the name comes from.",
    "<b>And the software cases are stronger than the original:</b> "
    "<b>captions are used most by people who can hear</b> (in noisy "
    "places, in quiet places, in a second language); <b>keyboard access "
    "is precisely what power users ask for</b>; and <b>clear, short "
    "language helps everybody who is tired or under time "
    "pressure</b> — which is everybody, sometimes.",
    "<b>So the accessibility argument does not require charity to "
    "work</b> — <b>it is a quality argument</b>, and <b>the quality "
    "argument is the one that survives a budget meeting</b>, which "
    "Module 12 &sect;2 treats as the practical fact it is.",
    "<b>But the honest limit, which this course states rather than "
    "eliding:</b> <b>not every accessibility requirement benefits "
    "everybody</b>. <b>A correct screen reader label on an icon benefits "
    "exactly the people who need it and nobody else</b>, and <b>it is "
    "still required</b>. <b>The curb-cut argument is a bonus, not the "
    "justification</b> — and treating it as the justification leads "
    "to dropping the requirements that lack a mainstream "
    "beneficiary."]),

  ("break",),
  ("h1", "3 &nbsp; Capabilities"),
  ("callout", "Design against capabilities, not against diagnoses",
   ["<b>A diagnosis does not tell you what somebody can do</b> — "
    "<b>two people with the same recorded condition may have entirely "
    "different interaction needs</b>, and in any case <b>a diagnosis is "
    "private information you have no right to and will not have.</b>",
    "<b>A capability does tell you:</b> <b>can this interface be "
    "operated without seeing it, without hearing it, without fine motor "
    "control, without holding several items in working memory, without "
    "speaking?</b> — which are questions about the interface rather "
    "than about any person.",
    "<b>Which makes them testable, by you, today</b> — "
    "<b>unplug the mouse; switch the screen reader on; mute the "
    "sound; set the zoom to 400%</b> — and <b>that is why the "
    "course is organised this way</b> rather than by condition.",
    "<b>And it generalises beyond disability</b>, which is "
    "<b>Module 02's subject</b>: <b>'cannot see the screen right now' "
    "covers blindness, bright sunlight, a cracked display, and "
    "driving</b> — and <b>the design requirement is identical in "
    "all four cases</b>, which is the most useful fact in this "
    "module."]),
  ("table", ["Capability", "The question to ask of the interface", "Module"],
   [["<b>Vision</b>",
     "<b>Can it be operated without seeing it, and is it usable with low "
     "vision or at 400% zoom?</b>", "<b>03</b>"],
    ["<b>Hearing</b>",
     "<b>Is any information available only as audio?</b>", "<b>04</b>"],
    ["<b>Motor control</b>",
     "<b>Is everything reachable by keyboard, and does anything require "
     "precision or speed?</b>", "<b>05</b>"],
    ["<b>Cognition and attention</b>",
     "<b>What does it demand of memory, attention, and reading?</b>",
     "<b>06</b>"],
    ["<b>Speech</b>",
     "<b>Is voice the only way in, anywhere?</b>", "<b>04 &sect;4</b>"],
    ["<b>Photosensitivity and vestibular</b>",
     "<b>Does anything flash, or move large areas, without a way to stop "
     "it?</b>", "<b>11 &sect;3</b>"]],
   [0.24, 0.60, 0.16]),
  ("p", "<b>Each of these has a test you can run in minutes</b> — "
        "<b>which is what makes the list a working checklist rather than a "
        "statement of values</b>, and is the difference between this "
        "course and an exhortation. <b>Organising by capability rather "
        "than by diagnosis is the structural decision of the course</b>, "
        "and it is also what lets Module 02 extend the same requirements "
        "to temporary and situational cases without changing any of "
        "them."),

  ("h1", "4 &nbsp; The semester"),
  ("callout", "All three Semester 11 courses replace a judgement about taste "
              "with a measurement",
   ["<b>CSCE 671 replaces 'this feels intuitive' with five "
    "participants and a task</b>; <b>CSCE 679 replaces 'this chart looks "
    "good' with a measured ranking of the visual channels</b>; <b>and "
    "this course replaces 'this seems accessible' with the actual "
    "assistive technology and a published standard.</b>",
    "<b>Which is the same move three times</b> — <b>applied to "
    "the interaction, to the encoding, and to the access</b> — and "
    "<b>it is what makes these three engineering courses rather than "
    "criticism</b>, which is the claim CSCE 671 Module 13 &sect;3 and "
    "CSCE 679 Module 13 &sect;3 both make from their own side.",
    "<b>And all three correct the same error:</b> <b>designing for "
    "an imagined user who resembles the designer</b> — which is "
    "<b>CSCE 671 Module 01 &sect;2's designer blindness</b>, and is "
    "the failure mode all three semesters' courses are organised "
    "against.",
    "<b>So the question this course keeps asking</b> — "
    "<b>'tested with whom, against what?'</b> — <b>is "
    "CSCE 671's question with the population widened</b>, and "
    "<b>Module 13 is where it gets answered properly</b>, including "
    "what a conformance claim does and does not establish."]),
 ],
 "resources": [
   ("Microsoft Inclusive Design (free)",
    "https://inclusive.microsoft.com/",
    "<b>&sect;2 and &sect;3</b> — the clearest short statement of the "
    "capability framing, and Module 02 builds directly on it."),
   ("Shakespeare &mdash; Disability Rights and Wrongs Revisited",
    "https://www.routledge.com/Disability-Rights-and-Wrongs-Revisited/Shakespeare/p/book/9780415527613",
    "<b>&sect;1 argued carefully, including the criticisms of the social "
    "model</b> — which are worth knowing. Library copy."),
   ("The W3C's Introduction to Web Accessibility (free)",
    "https://www.w3.org/WAI/fundamentals/accessibility-intro/",
    "<b>&sect;3's capabilities</b>, with the assistive technologies named "
    "and short videos of each in use."),
   ("Blackwell &mdash; The curb cut effect and its limits (free)",
    "https://ssir.org/articles/entry/the_curb_cut_effect",
    "<b>&sect;2's argument in its general form</b>, and useful for "
    "Module 12's organisational case."),
 ],
 "exercises": [
   "<b>State the two models</b> and what each implies about who owns a "
   "fix.",
   "<b>Find a product with a separate accessible version</b> and "
   "compare its feature set to the main one.",
   "<b>List four software curb cuts</b> you personally benefit from.",
   "<b>Then name two requirements with no mainstream beneficiary</b>, "
   "and say why they are still required.",
   "<b>Unplug your mouse for an hour</b> and record what you could not "
   "do.",
   "<b>Turn on your platform's screen reader</b> for ten minutes "
   "without looking at the screen.",
   "<b>Set your browser zoom to 400%</b> on three sites you use "
   "daily.",
   "<b>Rewrite one diagnosis-framed requirement</b> as a capability "
   "one.",
   "<b>For each capability in §3's table, name the situational "
   "version.</b>",
   "<b>State the measurement each Semester 11 course substitutes</b> "
   "for a judgement about taste.",
 ],
 "selfcheck": [
   "State both models and where each locates the problem.",
   "Why does the social model suit an engineering course?",
   "What follows under each model when an interface excludes somebody?",
   "Why does the separate version lose, and is that a prediction?",
   "State the curb-cut argument with three software examples.",
   "State its limit, and why the limit matters.",
   "Why design against capabilities rather than diagnoses?",
   "Name six capabilities and the test for each.",
   "How does the capability framing generalise beyond disability?",
   "What single error do all three Semester 11 courses correct?",
 ],
},

]

for _b in ("c632_b2", "c632_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
