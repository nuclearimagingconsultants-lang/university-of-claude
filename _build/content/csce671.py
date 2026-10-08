# -*- coding: utf-8 -*-
"""CSCE 671 Human-Computer Interaction — original course content."""

COURSE = {
    "code": "CSCE 671",
    "title": "Human-Computer Interaction",
    "tagline": "Designing for the person who will use it, who is not "
               "you",
    "term": "Semester 11 (with CSCE 679 and CSCE 632)",
    "prereqs": "CSCE 606 Software Engineering for the process material "
               "and CSCE 633 Machine Learning for the experimental "
               "design in Module 08; CSCE 679 and CSCE 632 run in "
               "parallel and extend Modules 02 and 05 respectively",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A redesign of an interface you did not design, "
                   "driven by observed failures rather than by opinion "
                   "— with users watched before and after, the "
                   "specific failures documented, and an honest account "
                   "of what your evaluation cannot establish",
    "description": [
        "<b>Interfaces fail for reasons that are predictable in "
        "advance and invisible to their designers.</b> <b>Module 01 "
        "establishes why: the designer knows the system's model and "
        "the user has only the interface</b>, so <b>every assumption "
        "the designer cannot see is one the user has to "
        "guess</b> — and the resulting failures look like user "
        "error from the inside and like bad design from outside.",
        "<b>The first third is about what people are actually "
        "like.</b> <b>Perception, attention, memory, and error are "
        "measured properties with hard limits</b> (Modules 02 and "
        "03) — and <b>a design that requires a person to notice "
        "something, remember something, or be careful will fail at a "
        "rate you can predict</b>, which turns a great deal of design "
        "argument into arithmetic.",
        "<b>The second third is method.</b> <b>Prototyping, usability "
        "evaluation, controlled experiments, and qualitative "
        "observation</b> (Modules 06 through 09) — <b>and the "
        "governing fact is that your opinion about your own interface "
        "is worth very little</b>, because you cannot un-know how it "
        "works. Watching five people use it is worth more than any "
        "amount of reasoning about it.",
        "<b>The third theme is that this course's subject includes "
        "the interfaces you build for other programmers.</b> <b>Module "
        "10 treats APIs, error messages, configuration, and tooling as "
        "user interfaces</b>, because they are — and because that is "
        "the interface design most of this program's graduates will "
        "actually do.",
        "<b>And the closing position is about honest claims and "
        "about consequences.</b> <b>Module 12 covers deliberately "
        "harmful design</b> — the techniques are the same ones, "
        "aimed differently — and <b>Module 13 is about what a "
        "usability study establishes</b>, because <b>'users liked it' "
        "is a statement about five people in a room.</b>",
    ],
    "outcomes": [
        "Explain why designers cannot see their own interfaces' "
        "failures.",
        "Apply what is known about perception to a layout.",
        "Predict error from attention and memory limits.",
        "Elicit and design against a user's mental model.",
        "Apply the interaction design principles and say what each "
        "costs.",
        "Prototype at the right fidelity for the question.",
        "Run a usability test and analyse it.",
        "Design a controlled experiment with human participants.",
        "Use qualitative methods and know what they establish.",
        "Design an API, an error message, and a configuration "
        "system.",
        "Explain input and output modalities and their "
        "constraints.",
        "Recognise and refuse manipulative design.",
        "State what a usability finding honestly establishes.",
    ],
    "materials": [
        ("Norman — The Design of Everyday Things, revised edition",
         "https://mitpress.mit.edu/9780262525671/",
         "<b>The primary text for Modules 01, 04, and 05.</b> The "
         "affordance, signifier, and conceptual model vocabulary this "
         "course uses comes from here, and the examples are still the "
         "best ones. Library copy."),
        ("Johnson — Designing with the Mind in Mind, 3rd edition",
         "https://www.elsevier.com/books/designing-with-the-mind-in-mind/johnson/978-0-12-818202-4",
         "<b>Modules 02 and 03.</b> The perceptual and cognitive "
         "research, written for designers and honest about effect "
         "sizes — which is unusual in this area. Library copy."),
        ("Krug — Don't Make Me Think, revisited",
         "https://sensible.com/dont-make-me-think/",
         "<b>Modules 05 and 07.</b> Short, practical, and its "
         "discount usability testing chapter is the best introduction "
         "to Module 07 there is."),
        ("Nielsen Norman Group articles, and the heuristics (free)",
         "https://www.nngroup.com/articles/",
         "<b>Modules 05 and 07's working reference</b> — the "
         "heuristics, the discount methods, and a large body of "
         "reported studies. Read the method sections, not only the "
         "conclusions."),
        ("Lazar, Feng & Hochheiser — Research Methods in "
         "Human-Computer Interaction, 2nd edition",
         "https://www.elsevier.com/books/research-methods-in-human-computer-interaction/lazar/978-0-12-805390-4",
         "<b>Modules 08 and 09.</b> The methods treated properly, "
         "including the ethics and the statistics. Library copy."),
        ("The CHI proceedings (free via the ACM OA programme)",
         "https://dl.acm.org/conference/chi",
         "<b>The field's primary literature.</b> Module 13's "
         "exercises use it; read the limitations sections, which is "
         "where the honest claims are."),
    ],
    "tooling": [
        "<b>Paper and a pen, first.</b> <b>Module 06 §1 "
        "argues that low-fidelity prototyping gets more and better "
        "feedback than a polished mock-up</b>, and the exercises "
        "require it before anything digital.",
        "<b>A screen recorder and a way to take notes while "
        "watching.</b> <b>Module 07's testing needs almost no "
        "tooling</b> — which is the point, and is why the barrier to "
        "doing it is not equipment.",
        "<b>Any prototyping tool you already know</b> for the "
        "higher-fidelity work. <b>The tool does not matter; the "
        "fidelity decision does</b> (Module 06 §2).",
        "<b>Python with <code>scipy.stats</code> and "
        "<code>statsmodels</code></b> for Module 08. <b>You will be "
        "analysing very small samples</b>, which is where the "
        "assumptions matter most.",
        "<b>Three to five people who will let you watch them use "
        "something.</b> <b>This is the real prerequisite</b>, and "
        "Module 07 §2 explains why five is the number.",
        "<b>And an interface you did not design, that you can "
        "change.</b> <b>Project 2 requires one</b> — your own code's "
        "interface is acceptable only if somebody else can be watched "
        "using it.",
    ],
    "projects": [
        {"title": "Watched, and diagnosed", "after": 6,
         "brief": "Watch people use an interface and diagnose the "
                  "failures mechanically rather than by opinion.",
         "reqs": [
             "<b>Five people observed</b> attempting the same three "
             "tasks, with the sessions recorded or carefully noted.",
             "<b>Every failure logged</b> with what the person "
             "expected, what happened, and what they did next.",
             "<b>Each failure attributed to a mechanism</b> from "
             "Modules 01 through 05 — <b>a missing signifier, an "
             "attention failure, a memory demand, a mental model "
             "mismatch</b> — not to 'confusing'.",
             "<b>A count by category</b>, so you know which mechanism "
             "accounts for most of the trouble.",
             "<b>Three things you predicted would fail and did "
             "not</b>, reported honestly.",
             "<b>And a redesign proposal per category</b>, with the "
             "mechanism it addresses named.",
         ],
         "done": [
             "<b>Failures attributed to mechanisms rather than "
             "described</b> — <b>which is the whole skill, and is "
             "graded hardest</b>. 'The button was confusing' is not a "
             "diagnosis.",
             "<b>Five people, not two</b>, and the sessions documented "
             "well enough that somebody else could count the same "
             "failures.",
             "<b>The wrong predictions reported</b>, because <b>a study "
             "in which you were right about everything was not a "
             "study.</b>",
             "<b>And the proposals tied to mechanisms</b>, so that "
             "each one is testable rather than a matter of taste.",
         ]},
        {"title": "Redesigned, and re-tested", "after": 12,
         "brief": "Implement the redesign and test whether it actually "
                  "helped.",
         "reqs": [
             "<b>The redesign built</b>, at whatever fidelity supports "
             "the test (Module 06 §2).",
             "<b>The same three tasks, with five new "
             "participants</b> — and <b>the same observation "
             "protocol</b>, so the comparison means something.",
             "<b>Task completion, time, and error counts</b> before "
             "and after, with the per-participant spread shown.",
             "<b>A qualitative account</b> of what changed in how "
             "people approached the tasks "
             "(Module 09).",
             "<b>The accessibility review</b> from CSCE 632's "
             "material, applied to your redesign.",
             "<b>And a limitation statement</b> in Module 13 "
             "§2's form.",
         ],
         "done": [
             "<b>New participants, not the same five</b>, because a "
             "second session with the same people measures learning "
             "rather than design.",
             "<b>The spread reported, not only the means</b> — "
             "<b>with five participants the mean is nearly "
             "uninformative</b> and the individual trajectories are the "
             "data.",
             "<b>Any regression reported</b>: <b>a redesign that fixed "
             "two things and broke a third is the normal outcome</b> and "
             "a complete project.",
             "<b>And the limitation statement specific:</b> <b>five "
             "people, one population, one set of tasks, in a room with "
             "you watching</b> — all four of which constrain the "
             "claim.",
         ]},
    ],
    "map": [
        ("Norman — The Design of Everyday Things",
         "https://mitpress.mit.edu/9780262525671/",
         "<b>Modules 01, 04, and 05.</b> Read it once in full; it is "
         "short and it reorganises how you see every object you "
         "touch."),
        ("Johnson — Designing with the Mind in Mind",
         "https://www.elsevier.com/books/designing-with-the-mind-in-mind/johnson/978-0-12-818202-4",
         "<b>Modules 02 and 03</b>, with the research cited so you "
         "can check it."),
        ("Nielsen Norman Group (free)",
         "https://www.nngroup.com/articles/",
         "<b>Modules 05, 06, and 07</b> — the practical reference, "
         "and the discount usability method in detail."),
        ("Lazar, Feng & Hochheiser — Research Methods in HCI",
         "https://www.elsevier.com/books/research-methods-in-human-computer-interaction/lazar/978-0-12-805390-4",
         "<b>Modules 08 and 09.</b> The methods, the statistics, and "
         "the ethics of studies with people."),
        ("Myers et al. — the API usability literature (free)",
         "https://www.cs.cmu.edu/~NatProg/",
         "<b>Module 10</b> — programmers as users, studied "
         "empirically, which is a small and unusually useful "
         "literature."),
        ("Brignull — Deceptive Patterns (free)",
         "https://www.deceptive.design/",
         "<b>Module 12's catalogue</b> — the techniques named and "
         "documented, which is what makes them recognisable."),
    ],
}

MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Why Interfaces Fail",
 "subtitle": "The gap between the system's model and the user's.",
 "question": "Why can you not see the problems in your own interface?",
 "outcomes": [
     "Explain the gulfs of execution and evaluation.",
     "Explain why designers are blind to their own designs.",
     "Explain affordances and signifiers and distinguish them.",
     "Explain why 'user error' is usually a design finding.",
     "Diagnose a failure mechanically rather than "
     "descriptively.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two gulfs",
   "blurb": "Doing, and understanding what happened."},

  {"t": "callout", "title": "The gulf of execution is not knowing what to do; the gulf of evaluation is not knowing what happened",
   "kind": "The two failures, and they need different fixes",
   "body": ["<b>The gulf of execution:</b> <b>the person has a goal "
            "and cannot work out which action achieves it</b> — "
            "which is a problem of what the interface <i>shows is "
            "possible</i>.",
            "<b>The gulf of evaluation:</b> <b>the person acted and "
            "cannot tell what the system did</b> — which is a problem "
            "of feedback, and is the one more often "
            "neglected.",
            "<b>And they fail differently.</b> <b>An execution gap "
            "produces hesitation and search; an evaluation gap produces "
            "repeated actions, undo, and eventually a wrong "
            "belief</b> about how the system works.",
            "<b>So the diagnosis matters:</b> <b>adding a label fixes "
            "an execution gap and does nothing for an evaluation "
            "gap</b> — and confusing the two is why interface fixes "
            "frequently do not help."]},

  {"t": "table", "kicker": "Diagnosis", "title": "The failure mechanisms this course names",
   "header": ["Mechanism", "What the user experiences", "Module"],
   "widths": [2.9, 4.4, 3.5],
   "rows": [
     ["<b>Missing signifier</b>", "<b>Does not know the action is possible</b>", "<b>01 §3</b>"],
     ["<b>Absent feedback</b>", "<b>Cannot tell what happened</b>", "<b>01 §1</b>"],
     ["<b>Perceptual failure</b>", "<b>Did not see it</b>", "<b>02</b>"],
     ["<b>Attention failure</b>", "<b>Saw it and did not process it</b>", "<b>03 §1</b>"],
     ["<b>Memory demand</b>", "<b>Had to hold something and did not</b>", "<b>03 §2</b>"],
     ["<b>Model mismatch</b>", "<b>Expected something else entirely</b>", "<b>04</b>"],
   ],
   "footnote": "<b>This table is the diagnostic vocabulary</b> — "
               "and <b>Project 1 requires every observed failure to be "
               "attributed to one of these rather than described as "
               "'confusing'.</b>",
   "note": "The vocabulary is the course's central practical tool."},

  {"t": "section", "label": "Part 2", "title": "Designer blindness",
   "blurb": "Which is structural, not a lack of care."},

  {"t": "callout", "title": "You cannot un-know how your own interface works, which makes your judgement of it nearly worthless",
   "kind": "The governing constraint on this whole subject",
   "body": ["<b>You know the conceptual model, the vocabulary, the "
            "state machine, and which of the three similar buttons does "
            "the thing</b> — <b>and none of that is available to the "
            "user.</b>",
            "<b>So the interface is legible to you by "
            "construction</b> — and <b>you cannot simulate not "
            "knowing</b>, which is a cognitive limit rather than a "
            "failure of imagination.",
            "<b>Which means your opinion about your own interface's "
            "usability is nearly worthless</b>, and the opinions of "
            "your colleagues who built it with you are no "
            "better.",
            "<b>And the only remedy is observation</b> "
            "(Module 07) — <b>watching five people struggle is "
            "worth more than any amount of reasoning</b>, and this is the "
            "single most important claim in the course."]},

  {"t": "bullets", "kicker": "Consequences", "title": "What follows from designer blindness",
   "items": [
     "<b>Design arguments cannot be settled by "
     "argument</b> — <b>two designers disagreeing about what is "
     "obvious are both unreliable witnesses</b>, and the resolution is "
     "to watch somebody.",
     "",
     "<b>Internal demos tell you nothing about usability.</b> "
     "<b>Everyone in the room knows the model</b>, so the demo tests "
     "the implementation and not the design.",
     "",
     "<b>And a user who 'does not read' is not the "
     "finding.</b> <b>Nobody reads</b> — it is a stable, measured "
     "property of people, and a design relying on reading has made an "
     "assumption it cannot support.",
     "",
     "<b>So 'the user should have…' is never a "
     "conclusion</b>, because the user is not available to be "
     "changed.",
     "",
     "<b>Which makes observation a method rather than a "
     "courtesy.</b>",
   ],
   "footnote": "<b>'The user should have read it' is the sentence that "
               "ends an investigation prematurely</b> — and the "
               "measured non-reading rate is the reason it is not a "
               "defence."},

  {"t": "section", "label": "Part 3", "title": "Affordances and signifiers",
   "blurb": "A distinction worth getting right."},

  {"t": "callout", "title": "An affordance is what an object permits; a signifier is what tells you so",
   "kind": "The distinction, and why it matters",
   "body": ["<b>A door affords pushing whether or not anything "
            "indicates it</b> — the affordance is a relation between "
            "the object and the person's capabilities, and it exists "
            "unperceived.",
            "<b>A flat plate is a signifier:</b> <b>it communicates "
            "that pushing is what to do</b> — and a handle on a push "
            "door is a signifier for the wrong affordance, which is why "
            "those doors fail.",
            "<b>So most interface failures are missing or misleading "
            "signifiers rather than missing affordances</b> — the "
            "action was possible and nothing said so, or something said "
            "the wrong thing.",
            "<b>Which is why the distinction is worth "
            "keeping:</b> <b>'add an affordance' is usually a confused "
            "request, and 'add a signifier' is an actionable "
            "one.</b>"]},

  {"t": "bullets", "kicker": "Signifiers", "title": "And where signifiers go wrong in software",
   "items": [
     "<b>Hidden gestures and shortcuts</b> — the affordance "
     "exists and nothing indicates it, so only people who were told "
     "will ever find it.",
     "",
     "<b>Elements that look clickable and are not</b>, and "
     "elements that are clickable and do not look it — both of "
     "which cost trust in every other element.",
     "",
     "<b>Disabled controls with no explanation</b>, which signify "
     "that something is possible while refusing it, with no path to "
     "making it possible.",
     "",
     "<b>And inconsistent signifiers within one "
     "system</b> — the same visual treatment meaning different "
     "things in different places, which destroys the learning the user "
     "did.",
     "",
     "<b>Which is why consistency is worth more than local "
     "optimality</b> (Module 05 §2).",
   ],
   "footnote": "<b>Inconsistency is expensive because it invalidates "
               "learning</b> — a user who learned your convention and "
               "then found an exception now trusts none of it."},

  {"t": "section", "label": "Part 4", "title": "User error",
   "blurb": "Which is a category to be suspicious of."},

  {"t": "callout", "title": "“User error” names a design finding you have decided not to investigate",
   "kind": "The reframing this course requires",
   "body": ["<b>People make mistakes at a predictable rate</b>, and "
            "<b>a design whose correct operation depends on their not "
            "doing so has made an assumption that does not "
            "hold.</b>",
            "<b>So the question is never 'why did they do that' but "
            "'why did the system permit it to matter'</b> — which is "
            "<b>exactly CSCE 701 §10 §4's blameless "
            "post-mortem framing</b>, arriving here first.",
            "<b>And the fixes are the same shape:</b> <b>make the "
            "error impossible, make it recoverable, or make it "
            "visible</b> — in that order of preference.",
            "<b>Which means confirmation dialogues are the weakest "
            "fix</b> — <b>they are read once and then dismissed "
            "reflexively</b> — and <b>undo is the strongest</b>, "
            "because it requires nothing of the user at the moment of "
            "the error."]},

  {"t": "bullets", "kicker": "Orientation", "title": "How to read this course",
   "items": [
     "<b>Modules 02 to 05 are what people are like</b>, and what "
     "follows for design — perception, attention, memory, mental "
     "models, and the principles.",
     "",
     "<b>Modules 06 to 09 are method</b> — prototyping, "
     "usability testing, controlled experiments, and qualitative "
     "observation.",
     "",
     "<b>Modules 10 and 11 are specific domains</b> — "
     "interfaces for programmers, and the input and output "
     "modalities.",
     "",
     "<b>And Modules 12 and 13 are consequences and honest "
     "claims</b> — manipulative design, and what a study "
     "establishes.",
     "",
     "<b>With Module 07 being the one to internalise</b>, because "
     "<b>everything else is argument and that is "
     "evidence.</b>",
   ],
   "footnote": "<b>If you take one thing from this course, take the "
               "habit of watching five people</b> — it is cheap, it "
               "is uncomfortable, and it is the only reliable source of "
               "information here."},
 ],
 "takeaways": [
   "An execution gap is not knowing what to do and an evaluation gap is not "
   "knowing what happened; they need different fixes.",
   "You cannot un-know how your own interface works, which makes your "
   "judgement of its usability nearly worthless.",
   "Two designers disagreeing about what is obvious are both unreliable "
   "witnesses, so the resolution is to watch somebody.",
   "An affordance is what an object permits and a signifier is what tells "
   "you so — most failures are missing signifiers.",
   "Inconsistency is expensive because it invalidates the learning the user "
   "already did.",
   "Make the error impossible, recoverable, or visible — in that "
   "order, which makes undo stronger than a confirmation dialogue.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two gulfs"),
  ("callout", "The gulf of execution is not knowing what to do; the gulf of "
              "evaluation is not knowing what happened",
   ["<b>The gulf of execution:</b> <b>the person has a goal and cannot "
    "work out which available action achieves it</b> — which is a "
    "problem of what the interface <i>shows is possible</i> (&sect;3's "
    "signifiers).",
    "<b>The gulf of evaluation:</b> <b>the person acted and cannot "
    "tell what the system actually did</b> — which is a problem of "
    "feedback, and <b>is the one more often neglected</b>, because "
    "feedback feels like a detail while the controls feel like the "
    "design.",
    "<b>And they fail differently, observably.</b> <b>An execution "
    "gap produces hesitation, hovering, and searching; an evaluation gap "
    "produces repeated actions, undo attempts, and eventually a settled "
    "wrong belief</b> about how the system works — which then causes "
    "further errors downstream.",
    "<b>So the diagnosis matters practically:</b> <b>adding a label "
    "fixes an execution gap and does nothing at all for an evaluation "
    "gap</b> — and <b>confusing the two is why interface fixes "
    "frequently fail to help</b>, which is a result you can observe in "
    "your own redesign in Project 2."]),
  ("table", ["Mechanism", "What the user experiences", "Where it is "
             "treated"],
   [["<b>Missing or misleading signifier</b>",
     "<b>Does not know the action is possible, or believes a different "
     "one is.</b>", "<b>Module 01 &sect;3</b>"],
    ["<b>Absent or ambiguous feedback</b>",
     "<b>Cannot tell what happened after acting.</b>",
     "<b>Module 01 &sect;1</b>"],
    ["<b>Perceptual failure</b>",
     "<b>Did not see it at all</b> — contrast, position, size, or "
     "grouping.", "<b>Module 02</b>"],
    ["<b>Attention failure</b>",
     "<b>Saw it and did not process it</b> — which is a different "
     "and more common failure.", "<b>Module 03 &sect;1</b>"],
    ["<b>Memory demand</b>",
     "<b>Had to hold something in mind across steps and did not.</b>",
     "<b>Module 03 &sect;2</b>"],
    ["<b>Mental model mismatch</b>",
     "<b>Expected the system to work in some other way entirely.</b>",
     "<b>Module 04</b>"]],
   [0.24, 0.52, 0.24]),
  ("p", "<b>This table is the diagnostic vocabulary of the course</b>, "
        "and <b>Project 1 requires every observed failure to be attributed "
        "to one of these mechanisms rather than described as "
        "'confusing'</b>. The reason is practical: <b>'confusing' admits "
        "no fix, and each of these six mechanisms has a known family of "
        "fixes</b> — so the attribution is what converts an "
        "observation into an action."),

  ("h1", "2 &nbsp; Designer blindness"),
  ("callout", "You cannot un-know how your own interface works, which makes "
              "your judgement of it nearly worthless",
   ["<b>You know the conceptual model, the vocabulary, the state "
    "machine, the intended order of operations, and which of the three "
    "similar-looking buttons does the thing</b> — and <b>none of "
    "that is available to the user</b>, who has only the pixels.",
    "<b>So the interface is legible to you by construction</b> "
    "— you built the legibility in by knowing it — and <b>you "
    "cannot simulate not knowing</b>, <b>which is a cognitive limit "
    "rather than a failure of imagination or empathy</b> and is why "
    "trying harder does not help.",
    "<b>Which means your opinion about your own interface's usability "
    "is nearly worthless</b>, and <b>the opinions of the colleagues who "
    "built it with you are no better</b> — they share the model, "
    "which is exactly the thing that disqualifies them.",
    "<b>And the only remedy is observation</b> (Module 07) — "
    "<b>watching five people struggle with it is worth more than any "
    "amount of reasoning about it</b>, and <b>this is the single most "
    "important claim in the course</b>. Everything in Modules 02 "
    "through 05 helps you predict and diagnose; only Module 07 "
    "tells you what actually happens."]),
  ("ul", ["<b>Design arguments cannot be settled by argument</b> "
          "— <b>two designers disagreeing about what is obvious are "
          "both unreliable witnesses</b>, and <b>the resolution is to "
          "watch somebody</b> rather than to escalate. This is "
          "liberating as well as humbling: it ends unresolvable "
          "meetings.",
          "<b>Internal demos tell you nothing about usability.</b> "
          "<b>Everybody in the room knows the model</b>, so <b>the demo "
          "tests the implementation and not the design</b> — which is "
          "a useful thing to do and is a different thing.",
          "<b>And a user who 'does not read' is not the "
          "finding.</b> <b>Nobody reads</b> — it is a stable, "
          "repeatedly measured property of how people use software "
          "(Module 03 &sect;1) — and <b>a design that relies on "
          "reading has made an assumption it cannot support.</b>",
          "<b>So 'the user should have…' is never a "
          "conclusion</b>, <b>because the user is not available to be "
          "changed</b> and the design is. This is the same move as "
          "CSCE 701 Module 11's compliance budget: the person is a "
          "fixed constraint and the system is the variable.",
          "<b>Which makes observation a method rather than a "
          "courtesy.</b> <b>'The user should have read it' is the "
          "sentence that ends an investigation prematurely</b> — and "
          "<b>the measured non-reading rate is the reason it is not a "
          "defence</b>, in design review or anywhere else."]),

  ("break",),
  ("h1", "3 &nbsp; Affordances and signifiers"),
  ("callout", "An affordance is what an object permits; a signifier is what "
              "tells you so",
   ["<b>A door affords pushing whether or not anything indicates "
    "it</b> — <b>the affordance is a relation between the object's "
    "properties and the person's capabilities, and it exists whether or "
    "not it is perceived.</b>",
    "<b>A flat plate is a signifier:</b> <b>it communicates that "
    "pushing is the thing to do</b> — and <b>a handle fitted to a "
    "push door is a signifier for the wrong affordance</b>, which is "
    "precisely why those doors fail and why they are the canonical "
    "example.",
    "<b>So most interface failures are missing or misleading "
    "signifiers rather than missing affordances</b> — the action was "
    "entirely possible and nothing indicated it, or something indicated "
    "something else.",
    "<b>Which is why the distinction is worth keeping "
    "straight:</b> <b>'add an affordance' is usually a confused request "
    "(the affordance is already there), and 'add a signifier' is an "
    "actionable one</b> — and the sloppy usage of 'affordance' to "
    "mean both has made a good deal of design discussion less precise "
    "than it could be."]),
  ("ul", ["<b>Hidden gestures and keyboard shortcuts</b> — the "
          "affordance exists and nothing indicates it, <b>so only people "
          "who were told will ever find it</b>, which makes the feature "
          "effectively private.",
          "<b>Elements that look clickable and are not, and elements "
          "that are clickable and do not look it</b> — <b>both of "
          "which cost trust in every other element</b> on the screen, "
          "because the user can no longer rely on appearance.",
          "<b>Disabled controls with no explanation</b>, which "
          "<b>signify that something is possible while refusing it, with "
          "no indication of what would make it possible</b> — a "
          "combined execution and evaluation gap, and one of the most "
          "frustrating patterns there is.",
          "<b>And inconsistent signifiers within a single system</b> "
          "— <b>the same visual treatment meaning different things in "
          "different places</b>, which <b>destroys the learning the user "
          "has already done.</b>",
          "<b>Which is why consistency is worth more than local "
          "optimality</b> (Module 05 &sect;2): a slightly worse "
          "treatment used everywhere beats a better one used "
          "inconsistently. <b>Inconsistency is expensive because it "
          "invalidates learning</b> — <b>a user who learned your "
          "convention and then found an exception now trusts none of "
          "it</b>, and has to check everything."]),

  ("h1", "4 &nbsp; User error"),
  ("callout", "“User error” names a design finding you have "
              "decided not to investigate",
   ["<b>People make mistakes at a predictable and well-measured "
    "rate</b> (Module 03 &sect;3), and <b>a design whose correct "
    "operation depends on their not doing so has made an assumption that "
    "does not hold</b> — which is a defect in the design rather than "
    "in the person.",
    "<b>So the question is never 'why did they do that' but 'why did "
    "the system permit it to matter'</b> — which is <b>exactly "
    "CSCE 701 Module 10 &sect;4's blameless post-mortem "
    "framing</b>, arriving in this course first chronologically and with "
    "the same justification: the first question produces a defensive "
    "answer and the second produces a list of fixes.",
    "<b>And the fixes are the same shape as there:</b> <b>make the "
    "error impossible, make it recoverable, or make it visible</b> "
    "— <b>in that order of preference</b>, because each requires "
    "less of the user than the last.",
    "<b>Which means confirmation dialogues are the weakest available "
    "fix</b> — <b>they are read once and then dismissed "
    "reflexively</b>, so they stop functioning after the second "
    "time — <b>and undo is the strongest</b>, <b>because it requires "
    "nothing of the user at the moment of the error</b>, which is "
    "precisely the moment they have no attention to spare."]),
  ("ul", ["<b>Modules 02 to 05 are what people are actually like</b>, "
          "and what follows for design — perception, attention, "
          "memory, error, mental models, and the interaction "
          "principles.",
          "<b>Modules 06 to 09 are method</b> — prototyping at "
          "the right fidelity, usability testing, controlled experiments "
          "with people, and qualitative observation.",
          "<b>Modules 10 and 11 are specific domains</b> — "
          "<b>interfaces for programmers</b> (which is the interface "
          "design most of this program's graduates will actually do), "
          "<b>and the input and output modalities.</b>",
          "<b>And Modules 12 and 13 are consequences and honest "
          "claims</b> — deliberately manipulative design, and what a "
          "usability study establishes.",
          "<b>With Module 07 being the one to internalise</b>, "
          "because <b>everything else in the course is argument and that "
          "is evidence</b>. <b>If you take one thing from this course, "
          "take the habit of watching five people</b> — it is cheap, "
          "it is uncomfortable, and it is <b>the only reliable source of "
          "information available in this subject.</b>"]),
 ],
 "resources": [
   ("Norman &mdash; The Design of Everyday Things, chapters 1 and 2",
    "https://mitpress.mit.edu/9780262525671/",
    "<b>&sect;1, &sect;3, and &sect;4</b> — the gulfs, the "
    "affordance/signifier distinction, and the human-error argument, from "
    "the source."),
   ("Nielsen &mdash; the usability heuristics, and the articles on "
    "scanning (free)",
    "https://www.nngroup.com/articles/ten-usability-heuristics/",
    "<b>&sect;2's non-reading finding and &sect;3's signifier "
    "problems</b>, with the studies behind them."),
   ("Norman &mdash; Affordances and Design (free)",
    "https://web.archive.org/web/20230307004923/https://jnd.org/affordances_and_design/",
    "<b>&sect;3's distinction, clarified by its author</b> — written "
    "specifically because the term had been misused."),
   ("Woods & Cook &mdash; on human error in complex systems",
    "https://www.taylorfrancis.com/books/mono/10.4324/9781315568003/behind-human-error",
    "<b>&sect;4's argument from safety engineering</b> — the "
    "intellectual source of the blameless framing. Library copy."),
 ],
 "exercises": [
   "<b>Find a door you have pushed when you should have pulled</b> and "
   "identify the misleading signifier.",
   "<b>Take one interface failure you have experienced</b> and classify "
   "it as an execution or an evaluation gap.",
   "<b>Classify ten failures</b> against Part 1's six "
   "mechanisms.",
   "<b>Explain a feature of your own software to someone unfamiliar</b> "
   "and note every piece of context you had to supply.",
   "<b>Watch one person use something you built</b>, without "
   "helping.",
   "<b>Count the things they did not read.</b>",
   "<b>Find a hidden affordance</b> in software you use daily.",
   "<b>Find an inconsistent signifier</b> within one application.",
   "<b>Find a confirmation dialogue you dismiss reflexively</b> and "
   "design the undo that would replace it.",
   "<b>Rewrite one 'user error' report</b> as a design finding.",
 ],
 "selfcheck": [
   "Distinguish the two gulfs and say how each fails observably.",
   "Why does the diagnosis determine whether a fix helps?",
   "Name the six failure mechanisms.",
   "Why is your judgement of your own interface unreliable?",
   "Why are internal demos uninformative about usability?",
   "Why is 'the user did not read' not a finding?",
   "Distinguish an affordance from a signifier, and say which is "
   "usually missing.",
   "Why is inconsistency expensive?",
   "Reframe 'user error', and give the three fixes in order.",
   "Why is a confirmation dialogue weak and undo strong?",
 ],
},

]

for _b in ("c671_b2", "c671_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
