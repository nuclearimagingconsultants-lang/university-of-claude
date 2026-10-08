# -*- coding: utf-8 -*-
"""CSCE 606 Software Engineering — original course content."""

COURSE = {
    "code": "CSCE 606",
    "title": "Software Engineering",
    "tagline": "Building software that survives contact with other people "
               "and with time",
    "term": "Semester 2 (with CSCE 611 and CSCE 645)",
    "prereqs": "Fluency in at least one language; experience with a codebase "
               "large enough to have become difficult",
    "effort": "8–10 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A codebase you have deliberately made maintainable: "
                   "tested, reviewed, continuously integrated, instrumented, "
                   "and documented well enough for someone else to take over",
    "description": [
        "Every other course in this program is about making a program "
        "<i>work</i>. This one is about making it keep working — after "
        "you have forgotten how it works, after three other people have "
        "modified it, and after the requirements have changed twice.",
        "That sounds soft, and it is not. The economics are specific: most "
        "of the money spent on a piece of software is spent after it first "
        "ships, and most of that goes into understanding code before "
        "changing it. Every practice in this course is judged against that "
        "one measurement — does it reduce the cost of the next change?",
        "The hazard in a subject like this is that it becomes a list of "
        "received opinions. So every claim here comes with the reasoning "
        "behind it and, where the evidence is weak, that is stated. Some "
        "widely repeated advice is wrong, or right only in particular "
        "circumstances, and the course says which.",
        "This is also the course where the solo-study format is weakest, "
        "because several of its subjects — code review, collaboration, "
        "process — are inherently about working with other people. The "
        "projects are therefore built around open-source contribution, which "
        "supplies the other people.",
    ],
    "outcomes": [
        "Distinguish essential from accidental complexity and attack the "
        "right one.",
        "Elicit and specify requirements in a form that can be checked.",
        "Design modules with low coupling and high cohesion, and explain why "
        "that reduces change cost.",
        "Choose an architecture from the constraints that actually bind.",
        "Design a test suite that gives confidence proportionate to its cost.",
        "Refactor safely and reason about technical debt as a financial "
        "decision.",
        "Review code in a way that improves it without damaging the author.",
        "Build a pipeline that makes releasing boring.",
        "Instrument a system so that its behaviour in production is "
        "observable.",
    ],
    "materials": [
        ("Software Engineering at Google (free online)",
         "https://abseil.io/resources/swe-book",
         "The best single book on the subject, free from the authors. Its "
         "framing — engineering is programming integrated over time "
         "— is this course's framing."),
        ("MIT 6.031 Software Construction (free, complete)",
         "https://web.mit.edu/6.031/www/",
         "Excellent on specification, invariants, and testing. The readings "
         "are unusually precise."),
        ("Berkeley CS169 — Engineering Software as a Service (edX, free "
         "audit)",
         "https://www.edx.org/learn/software-engineering/university-of-california-berkeley-agile-development-using-ruby-on-rails-the-basics",
         "A full project-based course, with the SaaS context that most "
         "software now lives in."),
        ("Martin Fowler — refactoring.com and martinfowler.com",
         "https://martinfowler.com/",
         "The reference for refactoring, continuous integration, and "
         "architecture patterns. Catalogue-style and genuinely useful."),
        ("Google Testing Blog and the Test Sizes taxonomy",
         "https://testing.googleblog.com/",
         "Practical testing writing from people running it at scale."),
        ("Accelerate / DORA research (summaries free)",
         "https://dora.dev/",
         "The one body of empirical evidence about software delivery "
         "practices. Read it before believing anything else in this field."),
    ],
    "tooling": [
        "<b>Git</b>, used properly — interactive rebase, bisect, "
        "reflog, not just commit and push.",
        "<b>A CI service</b>: GitHub Actions is free for public "
        "repositories and sufficient for everything here.",
        "<b>A test framework</b> and a coverage tool for your language.",
        "<b>A linter and formatter</b>, configured once and then never "
        "argued about again.",
        "<b>A real open-source project</b> you will contribute to. Choose it "
        "in Module 01; it is the vehicle for both projects.",
    ],
    "projects": [
        {"title": "Make a codebase changeable", "after": 7,
         "brief": "Take a piece of your own code that has become hard to "
                  "modify — ideally something from CSCE 641 or 645 "
                  "— and make it changeable, measuring as you go.",
         "reqs": [
             "A written assessment of what makes it hard to change now, with "
             "specific examples rather than general complaints.",
             "A characterisation test suite covering current behaviour, "
             "written before any change.",
             "At least five refactorings, each a separate commit with a "
             "message explaining why.",
             "Coupling reduced demonstrably: a dependency diagram before and "
             "after.",
             "A written note on one refactoring you started and reverted, "
             "and why.",
         ],
         "done": [
             "A change that was previously difficult, now made in under an "
             "hour, with the before-and-after effort recorded.",
             "Test suite runs in under a minute and fails if you break "
             "behaviour. Demonstrate by introducing a deliberate bug.",
             "A dependency diagram showing a reduction in cycles or in "
             "fan-out.",
         ]},
        {"title": "Contribute to a real project", "after": 12,
         "brief": "Make a substantive contribution to an open-source project "
                  "you did not write. The point is working inside someone "
                  "else's constraints and surviving their review.",
         "reqs": [
             "A merged pull request of non-trivial size — not a typo "
             "fix. A bug fix with a regression test, or a small feature.",
             "Tests that match the project's existing conventions.",
             "A CI pipeline that passes, including any linting the project "
             "requires.",
             "The full review conversation, including every change requested.",
             "A written reflection on what the maintainers asked for that you "
             "had not anticipated.",
         ],
         "done": [
             "The pull request is merged, or has a documented reason it was "
             "not.",
             "A record of review comments received, categorised by kind: "
             "correctness, style, design, project convention.",
             "An honest account of the most useful criticism you received.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Why Software Engineering Exists",
 "subtitle": "Programming integrated over time.",
 "question": "What problem does software engineering solve that programming "
             "does not?",
 "outcomes": [
     "Distinguish programming from software engineering.",
     "Distinguish essential from accidental complexity.",
     "Explain why most software cost occurs after first release.",
     "Explain why adding people to a late project makes it later.",
     "Judge a practice by whether it reduces the cost of the next change.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The distinction",
   "blurb": "Not scale. Time."},

  {"t": "callout", "title": "Engineering is programming integrated over time",
   "kind": "The framing",
   "body": ["<b>Programming</b> produces a program that works now, for you, "
            "on this input.",
            "<b>Software engineering</b> produces a program that still works "
            "in three years, when you have forgotten it, when four other "
            "people have modified it, and when the requirements have changed "
            "twice.",
            "The difference is not size. A hundred-line script maintained for "
            "a decade is an engineering problem; a hundred-thousand-line "
            "program thrown away after one run is not.",
            "<b>Every practice in this course is judged by one question:</b> "
            "does it reduce the cost of the next change?"]},

  {"t": "table", "kicker": "Cost", "title": "Where the money actually goes",
   "header": ["Phase", "Share of total cost", "Note"],
   "widths": [3.6, 3.4, 5.1],
   "rows": [
     ["Initial development", "~20–40%", "The part everyone plans for"],
     ["Maintenance and evolution", "<b>~60–80%</b>", "The part nobody budgets"],
     ["— of which: reading code", "<b>Most of it</b>", "Understanding precedes changing"],
   ],
   "footnote": "Figures vary by study; the ordering never does.",
   "note": "The 'reading dominates' point is the one that justifies almost "
           "every practice in the course."},

  {"t": "callout", "title": "Code is read far more often than it is written",
   "kind": "The practical consequence",
   "body": ["A line of code is written once and read dozens of times — "
            "during review, during debugging, during every subsequent "
            "change, by people who were not there when it was written.",
            "So optimising for <i>writing</i> speed is optimising the wrong "
            "variable. Clever compression that saves two minutes of typing "
            "and costs ten minutes of comprehension, twenty times, is a "
            "large net loss.",
            "This single observation justifies naming conventions, explicit "
            "over implicit, boring over clever, and most of the rest of this "
            "course.",
            "<b>Write for the person who reads it next.</b> It is usually "
            "you, and you will have forgotten."]},

  {"t": "section", "label": "Part 2", "title": "Two kinds of complexity",
   "blurb": "One you can remove. One you cannot."},

  {"t": "two", "kicker": "Brooks", "title": "Essential and accidental",
   "lh": "Essential",
   "l": ["Inherent in the problem itself.",
         "Tax law is complicated. A payroll system must be.",
         "<b>Cannot be removed</b> — only relocated or exposed.",
         ("Hiding it does not reduce it.", 1),
         "Shrinks only if the requirements shrink."],
   "rh": "Accidental",
   "r": ["Introduced by how we build, not by what we build.",
         "Build systems, configuration, framework ceremony, duplication.",
         "<b>Can be removed</b>, and that is where engineering effort pays.",
         ("Most tooling progress attacks this.", 1),
         "Grows silently if nobody attacks it."],
   "note": "Brooks's argument that accidental complexity had already been "
           "largely conquered was wrong, and usefully so — we invented "
           "new kinds."},

  {"t": "callout", "title": "Diagnose before you simplify",
   "kind": "Why the distinction matters",
   "body": ["Effort spent removing essential complexity is wasted — the "
            "complexity reappears somewhere, usually somewhere worse.",
            "A system that hides genuine domain complexity behind a "
            "'simple' interface has not removed it; it has made it "
            "surprising.",
            "Effort spent removing accidental complexity compounds, because "
            "it reduces the cost of every future change.",
            "<b>So the first question about any messy system is which kind "
            "you are looking at.</b> 'This is complicated' is not a "
            "diagnosis."]},

  {"t": "section", "label": "Part 3", "title": "Brooks's law",
   "blurb": "The most quoted result in the field, and the most misquoted."},

  {"t": "eq", "kicker": "Communication", "title": "Why adding people does not scale",
   "eqs": [
     ("communication paths  =  n(n−1)/2",
      "Ten people have 45 pairwise channels. Twenty have 190."),
     ("work output  ∝  n  (at best)",
      "Linear, and only if the work partitions cleanly."),
     ("overhead  ∝  n²",
      "Quadratic. Eventually it dominates."),
   ],
   "caption": "<b>Adding people to a late software project makes it "
              "later</b> — because of ramp-up time plus quadratic "
              "communication cost.",
   "note": "Worth stressing the 'late' qualifier: adding people early to a "
           "partitionable project is fine."},

  {"t": "bullets", "kicker": "Brooks's law", "title": "What it does and does not say",
   "items": [
     "<b>Does say:</b> adding people to a <i>late</i> project makes it later. "
     "New people must be trained by the people doing the work.",
     "",
     "<b>Does not say</b> that teams cannot grow, or that large projects are "
     "impossible.",
     "",
     "<b>The real content:</b> communication cost is quadratic, so the way to "
     "scale is to <b>reduce the need to communicate</b>.",
     ("Which is what modularity, interfaces, and documentation are for.", 1),
     ("Conway's law is the same observation from the other side.", 1),
   ],
   "note": "Reframing Brooks's law as an argument for modularity rather than "
           "against hiring is the useful reading."},

  {"t": "callout", "title": "Conway's law", "kind": "The structural consequence",
   "body": ["<b>A system's architecture mirrors the communication structure "
            "of the organisation that built it.</b>",
            "Three teams will produce three components, with the awkward "
            "interfaces falling exactly on the team boundaries.",
            "This is an observation, not advice — but it can be used "
            "deliberately: choose the architecture you want, then organise "
            "teams to match. That is the <i>inverse Conway manoeuvre</i>.",
            "And it predicts failure: a team structure that does not match "
            "the intended architecture will reshape the architecture, not the "
            "other way round."]},

  {"t": "section", "label": "Part 4", "title": "Judging practices",
   "blurb": "This field has more opinion than evidence. Here is what the "
            "evidence says."},

  {"t": "table", "kicker": "Evidence", "title": "What is actually measured",
   "header": ["Claim", "Evidence"],
   "widths": [5.6, 6.5],
   "rows": [
     ["Small frequent deploys outperform large rare ones", "<b>Strong</b> — DORA, multi-year"],
     ["Version control and CI improve outcomes", "<b>Strong</b>"],
     ["Code review finds defects", "Good"],
     ["Specific language or framework matters most", "Weak"],
     ["TDD specifically improves quality", "<b>Mixed</b> — honestly contested"],
     ["Pair programming is worth the cost", "Mixed; context-dependent"],
   ],
   "note": "Being honest about TDD's contested evidence builds credibility "
           "for the claims that are well supported."},

  {"t": "bullets", "kicker": "This course", "title": "How to read the rest of it",
   "items": [
     "Where evidence is strong, it is cited.",
     "Where a practice is convention rather than evidence, that is said.",
     "Where reasonable practitioners disagree, both positions are given.",
     "",
     "<b>Be suspicious of confident advice in this field.</b> Much of it is "
     "one person's experience generalised past its warrant.",
     "",
     "The test is always the same: <i>does this reduce the cost of the next "
     "change, in my context?</i>",
   ],
   "footnote": "Including the advice in this course."},
 ],
 "takeaways": [
   "Software engineering is programming integrated over time. The "
   "distinguishing variable is duration, not size.",
   "Most of a system's cost is incurred after first release, and most of that "
   "is spent reading code before changing it.",
   "Write for the reader, not the writer. Cleverness that costs comprehension "
   "is a net loss.",
   "Essential complexity comes from the problem and cannot be removed; "
   "accidental complexity comes from our tools and can. Diagnose which.",
   "Communication cost is quadratic in team size, so the way to scale is to "
   "reduce the need to communicate — which is what modularity is for.",
   "Conway's law: architecture mirrors organisation. You can use this "
   "deliberately, and it will happen whether you do or not.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Programming and engineering"),
  ("callout", "The distinguishing variable is time",
   ["<b>Programming</b> produces code that works now, for the author, on the "
    "inputs at hand.",
    "<b>Software engineering</b> produces code that still works in three "
    "years — after the author has forgotten it, after several other "
    "people have modified it, after the requirements changed twice, and after "
    "a dependency released a breaking version.",
    "The difference is not scale. A two-hundred-line script that a team "
    "depends on for a decade is an engineering artefact. A hundred-thousand-"
    "line simulation run once for a paper is not.",
    "Every practice in this course should be judged against one question: "
    "<b>does it reduce the cost of the next change?</b> Practices that do not "
    "are ceremony, however widely they are recommended."]),
  ("h2", "1.1 &nbsp; Where the cost is"),
  ("table", ["Phase", "Approximate share", "Comment"],
   [["Initial development", "20&ndash;40%",
     "The part that gets estimated, scheduled, and budgeted."],
    ["Maintenance and evolution", "<b>60&ndash;80%</b>",
     "Bug fixes, new requirements, dependency updates, platform changes, "
     "performance work."],
    ["Within maintenance: understanding existing code",
     "<b>The majority of it</b>",
     "Before any change can be made safely, someone must work out what the "
     "current code does and why."]],
   [0.30, 0.22, 0.48]),
  ("p", "Specific percentages vary between studies and between domains. The "
        "ordering does not: post-release cost dominates, and comprehension "
        "dominates post-release cost."),
  ("callout", "Code is read far more often than written",
   ["A given line is typed once. It is then read during review, during "
    "debugging, during every subsequent change to the surrounding code, and "
    "by people who have no context on why it exists.",
    "Optimising for writing speed therefore optimises the wrong variable. A "
    "dense one-liner that saves two minutes of typing and costs five minutes "
    "of comprehension on each of twenty subsequent readings is a substantial "
    "net loss, even though it felt efficient at the time.",
    "This single observation underwrites most of the practices in this "
    "course: descriptive names, explicit over implicit, boring over clever, "
    "comments that explain <i>why</i>, and tests that document intent.",
    "<b>Write for whoever reads it next.</b> Statistically that is you, in "
    "six months, with no memory of this afternoon."]),

  ("h1", "2 &nbsp; Essential and accidental complexity"),
  ("p", "Fred Brooks drew the distinction in <i>No Silver Bullet</i> (1986), "
        "and it remains the most useful single analytical tool in the "
        "subject."),
  ("table", ["", "Essential", "Accidental"],
   [["Source", "The problem domain itself.",
     "The tools, languages, and processes used to build the solution."],
    ["Examples", "Tax rules are genuinely complicated; a payroll system "
     "cannot be simpler than the law it implements. Distributed consensus is "
     "hard because of physics, not because of our code.",
     "Build system configuration, boilerplate, framework ceremony, "
     "duplicated logic, awkward dependency management, four ways to do the "
     "same thing."],
    ["Can it be removed?", "<b>No.</b> It can be relocated, encapsulated, or "
     "made explicit — not eliminated.",
     "<b>Yes</b>, and this is where engineering effort compounds."],
    ["Trend over time", "Changes only if the requirements change.",
     "Grows silently unless someone actively attacks it."]],
   [0.17, 0.42, 0.41]),
  ("callout", "Diagnose before simplifying",
   ["Effort spent trying to remove essential complexity is wasted, and often "
    "harmful: the complexity does not disappear, it relocates somewhere less "
    "visible. A system that hides genuine domain complexity behind a "
    "deceptively simple interface has made it <i>surprising</i> rather than "
    "absent, and surprise is expensive.",
    "Effort spent removing accidental complexity compounds, because it "
    "reduces the cost of every future change, not just the current one.",
    "So the first question about any difficult system is which kind of "
    "complexity you are looking at. 'This is complicated' is a complaint; "
    "'this is accidentally complicated because the build system requires "
    "three files to add one module' is a diagnosis with a fix."]),
  ("p", "Brooks also argued that accidental complexity had already been "
        "largely conquered by high-level languages and that no future "
        "development would deliver an order-of-magnitude improvement. The "
        "first claim proved wrong in an interesting way — we invented "
        "entirely new categories of accidental complexity, in distributed "
        "systems, build tooling, and dependency management. The second claim "
        "has held up rather well."),

  ("h1", "3 &nbsp; Brooks's law"),
  ("eq", "communication paths = n(n &minus; 1) / 2"),
  ("table", ["Team size", "Pairwise channels"],
   [["3", "3"], ["5", "10"], ["10", "45"], ["20", "190"], ["50", "1,225"]],
   [0.3, 0.7]),
  ("p", "Output grows at best linearly with team size, and only when the work "
        "partitions cleanly. Communication overhead grows quadratically. "
        "There is therefore a point beyond which adding people reduces total "
        "output, and the point arrives sooner than intuition suggests."),
  ("callout", "What the law says, and what it does not",
   ["<b>It says:</b> adding people to a <i>late</i> project makes it later. "
    "New arrivals must be brought up to speed by exactly the people who are "
    "already behind, so throughput drops before it rises — and on a late "
    "project there is no time for it to rise.",
    "<b>It does not say</b> that teams cannot grow, that large projects are "
    "impossible, or that hiring is futile. Growing a team early, on work that "
    "partitions, is ordinary and effective.",
    "<b>The useful content is the diagnosis, not the prohibition.</b> "
    "Communication cost is quadratic, so scaling requires <i>reducing the "
    "need to communicate</i> — which is precisely what modular design, "
    "stable interfaces, and good documentation accomplish. Brooks's law is an "
    "argument for Module 03, not against hiring."]),
  ("callout", "Conway's law",
   ["<b>Organisations design systems that mirror their own communication "
    "structure.</b> (Conway, 1967.)",
    "Three teams will produce three components. The interfaces that are "
    "awkward will be the ones that fall on team boundaries, because those are "
    "the ones that required negotiation rather than a conversation.",
    "This is an empirical observation rather than advice, and it is "
    "remarkably robust. It can be exploited: decide the architecture you "
    "want, then structure teams to match it — the <i>inverse Conway "
    "manoeuvre</i>.",
    "It also predicts failure. If the team structure does not match the "
    "intended architecture, the architecture will drift to match the teams, "
    "not the other way round. Microservice migrations that keep a monolithic "
    "team structure reliably produce a distributed monolith."]),

  ("break",),
  ("h1", "4 &nbsp; On evidence"),
  ("p", "Software engineering has far more confident advice than it has "
        "evidence. Much of what is asserted is one practitioner's experience "
        "generalised well past its warrant, and some widely-repeated claims "
        "are simply untested."),
  ("table", ["Claim", "Evidence", "Source"],
   [["Small, frequent deployments outperform large, infrequent ones on both "
     "speed and stability.", "<b>Strong</b>",
     "DORA / <i>Accelerate</i>, multi-year survey research across thousands "
     "of organisations."],
    ["Version control, continuous integration, and automated deployment "
     "improve delivery outcomes.", "<b>Strong</b>", "Same."],
    ["Code review finds defects and spreads knowledge.", "Good",
     "Multiple industrial studies; effect size depends heavily on how review "
     "is conducted (Module 09)."],
    ["Choice of programming language or framework is the dominant factor in "
     "project outcome.", "Weak",
     "Repeatedly studied; effects are small relative to team and process "
     "factors."],
    ["Test-driven development specifically improves quality or "
     "productivity.", "<b>Mixed and genuinely contested</b>",
     "Studies disagree. Writing tests clearly helps; that the tests must come "
     "<i>first</i> is not well supported (Module 05)."],
    ["Pair programming justifies its cost.", "Mixed",
     "Benefits for knowledge transfer and for difficult problems; costs are "
     "real. Context-dependent."]],
   [0.32, 0.20, 0.48]),
  ("callout", "How to read the rest of this course",
   ["Where evidence is strong, it is cited. Where a practice is convention "
    "rather than demonstrated, that is stated. Where competent practitioners "
    "disagree, both positions are given rather than one being presented as "
    "settled.",
    "Be suspicious of confident advice in this field, including the advice "
    "here. The appropriate test is always the same: <i>does this reduce the "
    "cost of the next change, in my situation?</i>",
    "A practice that works for a team of two hundred on a ten-year product "
    "may be pure overhead for one person on a six-month project, and the "
    "reverse is also true. Context is not an excuse for sloppiness; it is "
    "part of the engineering judgement."]),
 ],
 "resources": [
   ("Software Engineering at Google — Chapters 1–3",
    "https://abseil.io/resources/swe-book",
    "'Programming over time', the distinction from programming, and the Beyoncé "
    "rule. This course's framing comes from here."),
   ("Fred Brooks — No Silver Bullet (1986, widely available free)",
    "https://www.cs.unc.edu/techreports/86-020.pdf",
    "Essential and accidental complexity. Forty years old and still the "
    "sharpest piece of analysis in the field."),
   ("Conway — How Do Committees Invent? (1968, free)",
    "https://www.melconway.com/Home/Committees_Paper.html",
    "The original paper. Short, and the argument is better than the "
    "slogan."),
   ("DORA — State of DevOps research",
    "https://dora.dev/",
    "The most substantial empirical evidence base in software delivery. Read "
    "the summaries before accepting any claim about process."),
 ],
 "exercises": [
   "Take a piece of code you wrote more than six months ago and did not "
   "document. Time how long it takes to understand it well enough to make a "
   "small change. Write down what would have made it faster.",
   "Choose the open-source project you will contribute to in Project 2. "
   "Criteria: active, has a contribution guide, has tests, and you can build "
   "it. Build it today and record how long that took and what went wrong.",
   "For that project, categorise five sources of difficulty you encountered "
   "as essential or accidental complexity. Be specific.",
   "Find a system you use whose architecture visibly reflects its "
   "organisation — inconsistent APIs across subsystems is the usual "
   "tell. Write a paragraph on what the organisation chart probably looks "
   "like.",
   "Pick one piece of software engineering advice you believe. Search for "
   "empirical evidence for it. Write down what you find, including if the "
   "answer is nothing.",
   "Estimate the lifetime cost split for a project you have worked on. How "
   "much went into initial development against subsequent change?",
 ],
 "selfcheck": [
   "What distinguishes software engineering from programming, and why is it "
   "not size?",
   "Where does most of a software system's cost occur, and what consumes most "
   "of that?",
   "Define essential and accidental complexity, and say why the distinction "
   "changes what you do.",
   "Why is adding people to a late project counterproductive, and what is the "
   "useful conclusion to draw from it?",
   "State Conway's law and give one way to use it deliberately.",
   "Name one software engineering claim with strong evidence and one that is "
   "genuinely contested.",
 ],
},

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Requirements and Specification",
 "subtitle": "Finding out what to build, and writing it down checkably.",
 "question": "Why is it so hard to find out what people actually want?",
 "outcomes": [
     "Explain why requirements elicitation is difficult rather than lazy.",
     "Distinguish functional from quality requirements.",
     "Write a specification precise enough to be checked.",
     "Use preconditions, postconditions, and invariants.",
     "Recognise when a requirement is actually a proposed solution.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why it is hard",
   "blurb": "Not because people are unhelpful."},

  {"t": "bullets", "kicker": "The difficulty", "title": "Five reasons requirements are hard",
   "items": [
     "<b>People do not know what they want</b> until they see something. "
     "Preferences form on contact.",
     "",
     "<b>They describe solutions, not problems.</b> 'Add a dropdown' is an "
     "answer to a question they did not state.",
     "",
     "<b>Tacit knowledge.</b> The important constraints are the ones so "
     "obvious to them that nobody mentions them.",
     "",
     "<b>Conflicting stakeholders.</b> Different people want incompatible "
     "things, and neither knows it.",
     "",
     "<b>Requirements change</b> because the world does, and because your "
     "system changes it.",
   ],
   "note": "The third point is the one that causes the worst failures — "
           "nobody mentions it because it is obvious."},

  {"t": "callout", "title": "A stated requirement is usually a proposed solution",
   "kind": "The most useful technique",
   "body": ["'We need a dropdown to pick the warehouse' is not a "
            "requirement. It is someone's design for an unstated problem.",
            "<b>Ask why.</b> Perhaps orders are being shipped from the wrong "
            "warehouse. That is the requirement, and a dropdown may be the "
            "worst available answer — the system might infer the "
            "warehouse, or validate afterwards, or make the error "
            "impossible.",
            "Keep asking until you reach something the user cares about "
            "independently of any implementation.",
            "<b>The requirement is the problem. Everything else is "
            "negotiable.</b>"]},

  {"t": "two", "kicker": "Kinds", "title": "Functional and quality requirements",
   "lh": "Functional",
   "l": ["What the system does.",
         "'A user can reset their password by email.'",
         "Usually easy to state and to test.",
         ("Mostly what gets written down.", 1)],
   "rh": "Quality (non-functional)",
   "r": ["How well it does it.",
         "Latency, availability, security, maintainability, accessibility.",
         "Harder to state and <b>much</b> harder to retrofit.",
         ("Mostly what gets forgotten — and what sinks projects.", 1)],
   "note": "Quality requirements drive architecture. Discovering one late is "
           "how rewrites happen."},

  {"t": "callout", "title": "Quality requirements decide the architecture",
   "kind": "Why they must come early",
   "body": ["A functional requirement discovered late usually costs a "
            "feature's worth of work.",
            "A quality requirement discovered late can cost a rewrite. "
            "'It must handle a thousand times this load' or 'it must be "
            "auditable' are not features — they are constraints that "
            "determine the structure.",
            "And they are the ones nobody volunteers, because they are "
            "assumed. Nobody says 'it should not lose data'.",
            "<b>So ask explicitly.</b> How fast? How available? How many "
            "users? What happens on failure? Who must not see what?"]},

  {"t": "section", "label": "Part 2", "title": "Writing it down",
   "blurb": "A specification is a claim that can be wrong."},

  {"t": "bullets", "kicker": "Specification", "title": "What makes a specification useful",
   "items": [
     "<b>Checkable.</b> You can tell whether the system satisfies it.",
     ("'Fast' is not checkable. '95th percentile under 200 ms at 1,000 "
      "requests per second' is.", 1),
     "",
     "<b>Complete enough</b> to cover the cases that will occur, including "
     "errors.",
     "",
     "<b>Unambiguous.</b> Two readers reach the same conclusion.",
     "",
     "<b>Minimal.</b> It constrains the behaviour that matters and leaves the "
     "implementer free elsewhere.",
   ],
   "footnote": "Over-specification is a real failure: it forbids "
               "improvements nobody needed to forbid."},

  {"t": "code", "kicker": "Contracts", "title": "Preconditions, postconditions, invariants",
   "lang": "python", "code": """
def withdraw(account, amount):
    \"\"\"Withdraw amount from account.

    PRECONDITION   amount > 0 and amount <= account.balance
                   -- the CALLER's obligation
    POSTCONDITION  account.balance decreases by exactly amount,
                   and a transaction record is appended
                   -- the IMPLEMENTATION's obligation
    INVARIANT      account.balance == sum(t.delta for t in
                                          account.transactions)
                   -- true before and after; may be broken DURING
    \"\"\"

# The contract divides responsibility. If the precondition is
# violated, the bug is in the caller. If the postcondition fails
# with the precondition met, the bug is here.
""",
   "caption": "The real value is the division of responsibility. Without it, "
              "every function defensively checks everything, and nobody knows "
              "whose bug it is.",
   "note": "The blame-assignment framing is more motivating than the formal "
           "one."},

  {"t": "callout", "title": "Strong preconditions or defensive checks?",
   "kind": "A real trade-off",
   "body": ["<b>Strong precondition:</b> 'the caller must pass a positive "
            "amount.' The function need not check, and is simpler and "
            "faster — and a violation is undefined behaviour.",
            "<b>Defensive check:</b> validate and raise. Safer, and every "
            "caller pays for the check, and the error path must be handled "
            "everywhere.",
            "<b>The practical rule:</b> validate at system boundaries — "
            "user input, network, files — where data is untrusted. "
            "Inside, rely on preconditions and assert them in debug builds.",
            "Checking the same thing at every layer is how codebases become "
            "mostly validation."]},

  {"t": "section", "label": "Part 3", "title": "Formats",
   "blurb": "Several, each useful for different things."},

  {"t": "table", "kicker": "Formats", "title": "Ways to record a requirement",
   "header": ["Format", "Good for", "Weakness"],
   "widths": [2.8, 4.4, 4.9],
   "rows": [
     ["User story", "Keeping the user's goal visible", "Imprecise; needs acceptance criteria"],
     ["Use case", "Flows with alternatives and errors", "Verbose"],
     ["Acceptance criteria", "<b>Checkable conditions</b>", "Can miss the why"],
     ["Executable spec (BDD)", "Spec and test are one artefact", "Tooling overhead; can rot"],
     ["Formal spec (TLA+, Alloy)", "Concurrency and protocols", "Expensive; specialist skill"],
   ],
   "note": "TLA+ is worth knowing about: AWS uses it on critical protocols "
           "and reports finding real bugs."},

  {"t": "code", "kicker": "User story", "title": "A story is a placeholder for a conversation",
   "lang": "text", "code": """
As a   warehouse manager
I want to see which orders are delayed
So that I can contact customers before they contact me

ACCEPTANCE CRITERIA  -- this is the part that matters
  - "Delayed" means promised date is in the past and status
    is not Shipped.
  - The list is sorted by how late, most late first.
  - Orders delayed by under 1 hour are excluded.
  - An empty list shows "No delayed orders", not an empty table.
  - Loads in under 2s with 10,000 open orders.

Without the criteria, the story is a conversation starter.
With them, it is checkable -- and it IS the test.
""",
   "caption": "The 'so that' clause is the actual requirement. It is what "
              "lets you propose something better than what was asked for.",
   "note": "The last two criteria — empty state and performance — "
           "are the ones always forgotten."},

  {"t": "bullets", "kicker": "Change", "title": "Requirements change; plan for it",
   "items": [
     "<b>Not a failure of elicitation.</b> The world changes, and shipping "
     "the system changes what people want.",
     "",
     "So: stop trying to get requirements complete up front, and build to "
     "<b>absorb change cheaply</b>.",
     ("Which is modularity — Module 03.", 1),
     "",
     "<b>Deliver early</b> so that feedback arrives while it is still cheap "
     "to act on.",
     "",
     "<b>Record decisions and their reasons</b>, so that revisiting one does "
     "not mean re-deriving it.",
   ],
   "footnote": "An architecture decision record costs ten minutes and saves "
               "an argument a year later."},
 ],
 "takeaways": [
   "People describe solutions, not problems. Ask why until you reach "
   "something they care about independently of implementation.",
   "The most important constraints are tacit — unstated because they "
   "seem obvious to everyone who has the context.",
   "Quality requirements determine architecture and are the ones nobody "
   "volunteers. Ask explicitly.",
   "A useful specification is checkable, complete enough, unambiguous, and "
   "minimal. Over-specification forbids improvements.",
   "Contracts divide responsibility: a precondition violation is the caller's "
   "bug, a postcondition failure is the implementation's.",
   "Validate at system boundaries; rely on preconditions within. Checking "
   "everywhere produces codebases that are mostly validation.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why requirements are hard"),
  ("p", "The difficulty is structural rather than a matter of people being "
        "unhelpful or analysts being lazy."),
  ("ol", ["<b>People do not know what they want until they see something.</b> "
          "Preferences are constructed on contact with a concrete artefact, "
          "not retrieved from storage. This is why prototypes elicit better "
          "requirements than interviews.",
          "<b>People describe solutions rather than problems.</b> A request "
          "arrives already shaped as a design, and the problem that motivated "
          "it is left unstated.",
          "<b>The important knowledge is tacit.</b> Experts cannot easily "
          "articulate what they know, and the constraints that matter most "
          "are the ones so obvious to everyone in the domain that nobody "
          "thinks to mention them. These are the requirements that are "
          "discovered at acceptance testing.",
          "<b>Stakeholders conflict.</b> Different people want incompatible "
          "things and frequently do not know it, because they have never had "
          "to state their assumptions side by side.",
          "<b>Requirements change</b> — because the business changes, "
          "because competitors change, and because deploying your system "
          "changes what people do and therefore what they need."]),
  ("callout", "The single most useful technique: ask why",
   ["'We need a dropdown to select the warehouse' is not a requirement. It is "
    "a design, proposed by someone who diagnosed a problem they did not "
    "state.",
    "Ask why. Perhaps orders are shipping from the wrong warehouse. <i>That</i> "
    "is the requirement, and once it is visible, a dropdown may be among the "
    "worse solutions — the system could infer the warehouse from the "
    "delivery address, or validate the choice afterwards, or make the wrong "
    "selection structurally impossible.",
    "Keep asking until you reach something the stakeholder values "
    "independently of any particular implementation. That is the requirement; "
    "everything above it is negotiable, and the negotiation is where "
    "engineering adds value."]),

  ("h1", "2 &nbsp; Two kinds of requirement"),
  ("table", ["", "Functional", "Quality (non-functional)"],
   [["Describes", "What the system does.", "How well it does it."],
    ["Example", "'A user can reset their password via an emailed link.'",
     "'The reset email arrives within 30 seconds for 99% of requests.'"],
    ["Stated?", "Usually, and explicitly.",
     "Rarely, because they are assumed."],
    ["Testable?", "Generally straightforward.",
     "Requires load, chaos, or security testing to verify."],
    ["Retrofittable?", "Usually, at the cost of a feature's work.",
     "<b>Often not.</b> They constrain the architecture."]],
   [0.15, 0.42, 0.43]),
  ("callout", "Quality requirements determine the architecture",
   ["A functional requirement discovered late typically costs the work of "
    "building that feature. A quality requirement discovered late can cost a "
    "rewrite.",
    "'It must sustain a thousand times current load', 'every change must be "
    "auditable', 'it must work offline', 'no customer data may leave the "
    "region' — none of these are features. Each is a constraint that "
    "determines how the system is structured, and retrofitting one means "
    "restructuring.",
    "They are also exactly the requirements nobody volunteers, because they "
    "feel too obvious to say. Nobody says 'the system should not lose data'.",
    "<b>So ask explicitly and in numbers.</b> How fast? Measured how, at what "
    "percentile, under what load? How available, and what does downtime cost? "
    "How many users in year three? What must happen when a dependency fails? "
    "Who must be prevented from seeing what?"]),

  ("h1", "3 &nbsp; Writing a specification"),
  ("p", "A specification is a claim about the system that can turn out to be "
        "false. If it cannot be false, it is not a specification."),
  ("table", ["Property", "Meaning", "Failure mode"],
   [["<b>Checkable</b>", "You can determine whether the system satisfies it.",
     "'The system shall be fast' — nobody can tell whether it complies. "
     "'95th-percentile response under 200 ms at 1,000 requests per second' "
     "— anyone can."],
    ["<b>Complete enough</b>", "Covers the situations that will arise, "
     "including failures.",
     "Specifying the happy path only, so error behaviour is invented "
     "independently by each implementer."],
    ["<b>Unambiguous</b>", "Two competent readers reach the same conclusion.",
     "'The system should handle invalid input gracefully' — handle how?"],
    ["<b>Minimal</b>", "Constrains what matters; leaves the rest free.",
     "<b>Over-specification.</b> Mandating an implementation detail forbids "
     "improvements nobody intended to forbid, and the constraint outlives the "
     "reason for it."]],
   [0.18, 0.34, 0.48]),
  ("h2", "3.1 &nbsp; Contracts"),
  ("code", """def withdraw(account, amount):
    \"\"\"Withdraw `amount` from `account`.

    PRECONDITION
        amount > 0 and amount <= account.balance
        (the CALLER must ensure this)

    POSTCONDITION
        account.balance is reduced by exactly `amount`;
        a transaction record is appended
        (the IMPLEMENTATION must ensure this)

    INVARIANT
        account.balance == sum(t.delta for t in account.transactions)
        (true before and after; may be temporarily false inside)
    \"\"\""""),
  ("callout", "The point of a contract is assigning responsibility",
   ["If the precondition is violated, the bug is in the <b>caller</b>. If the "
    "postcondition fails while the precondition held, the bug is in the "
    "<b>implementation</b>. The contract makes that determination mechanical "
    "rather than a matter of argument.",
    "Without contracts, every function defensively validates everything it "
    "receives, nobody is sure whose responsibility anything is, and a large "
    "fraction of the codebase becomes redundant checking — which is "
    "itself a source of bugs, because the checks disagree."]),
  ("callout", "Strong preconditions or defensive validation?",
   ["<b>A strong precondition</b> places the obligation on the caller. The "
    "function is simpler and faster, and a violation is undefined behaviour "
    "— potentially a security problem.",
    "<b>Defensive validation</b> checks and raises. Safer, and every caller "
    "pays the cost, and every caller must now handle an error that may be "
    "impossible in their situation.",
    "<b>The practical resolution is to validate at system boundaries.</b> "
    "Data arriving from a user, a network, a file, or another service is "
    "untrusted and must be checked once, thoroughly, at the point of entry. "
    "Within the system, rely on preconditions — and assert them in debug "
    "builds, which gives you the checking during development and the speed in "
    "production.",
    "Validating the same property at every layer is how codebases end up "
    "mostly validation, and it provides less safety than it appears to, "
    "because the layers eventually disagree about what is valid."]),

  ("break",),
  ("h1", "4 &nbsp; Formats"),
  ("table", ["Format", "Strength", "Weakness"],
   [["<b>User story</b>", "Keeps the user's goal visible and resists "
     "premature design.",
     "Imprecise on its own. Useless without acceptance criteria."],
    ["<b>Use case</b>", "Documents a complete flow including alternatives and "
     "error paths.", "Verbose; falls out of date."],
    ["<b>Acceptance criteria</b>", "<b>Checkable conditions.</b> The part "
     "that does the work.", "Can lose sight of why the feature exists."],
    ["<b>Executable specification</b> (Cucumber, BDD)",
     "The specification and the test are one artefact, so they cannot "
     "diverge.",
     "Substantial tooling overhead; the natural-language layer often adds "
     "cost without adding readers."],
    ["<b>Formal specification</b> (TLA+, Alloy)",
     "Can prove properties of concurrent and distributed protocols that "
     "testing cannot reach.",
     "Expensive and requires specialist skill. Worth it for a protocol whose "
     "failure is catastrophic — AWS uses TLA+ on core services and "
     "reports finding bugs that had survived extensive testing."]],
   [0.22, 0.39, 0.39]),
  ("code", """As a   warehouse manager
I want to see which orders are delayed
So that I can contact customers before they contact me

ACCEPTANCE CRITERIA
  - "Delayed" = promised date in the past AND status != Shipped.
  - Sorted by lateness, most late first.
  - Orders less than 1 hour late are excluded.
  - Empty result shows "No delayed orders", not a blank table.
  - Page loads in under 2 seconds with 10,000 open orders."""),
  ("p", "The <b>so that</b> clause carries the actual requirement. Knowing "
        "that the goal is contacting customers before they complain opens "
        "options the original request did not: perhaps the system should "
        "notify customers automatically, which serves the goal better than "
        "any list."),
  ("p", "The last two criteria are the ones habitually omitted. Empty-state "
        "behaviour and performance under realistic data volume are "
        "requirements, and discovering them after release is how a shipped "
        "feature becomes unusable."),

  ("h1", "5 &nbsp; Requirements change"),
  ("callout", "Change is not an elicitation failure",
   ["The instinct is to treat changing requirements as evidence that the "
    "analysis was inadequate. Usually it is not. The business environment "
    "changes, competitors act, regulations shift — and deploying the "
    "system changes what users do, which changes what they need next.",
    "So the goal is not to make requirements complete and final before "
    "building. It is to build something that <b>absorbs change cheaply</b>, "
    "which is a design property (Module 03) rather than a process one.",
    "Three things follow. <b>Deliver early</b>, so feedback arrives while "
    "acting on it is still cheap. <b>Keep modules loosely coupled</b>, so a "
    "change in requirements touches one place. <b>Record decisions and their "
    "reasons</b> — an architecture decision record costs ten minutes to "
    "write and saves re-deriving the argument a year later, usually in a "
    "meeting."]),
 ],
 "resources": [
   ("MIT 6.031 — Specifications, Designing Specifications",
    "https://web.mit.edu/6.031/www/",
    "The most precise free treatment of preconditions, postconditions, and "
    "specification strength. Read both readings."),
   ("Software Engineering at Google — Chapter 1 (and the 'what do we "
    "mean' framing)",
    "https://abseil.io/resources/swe-book",
    "On requirements that are discovered rather than stated."),
   ("Newcombe et al. — How Amazon Web Services Uses Formal Methods "
    "(free)",
    "https://cacm.acm.org/magazines/2015/4/184701-how-amazon-web-services-uses-formal-methods/fulltext",
    "An honest industrial account of where formal specification pays and "
    "where it does not."),
   ("Michael Nygard — Documenting Architecture Decisions",
    "https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions",
    "The ADR format. Two pages, and widely adopted for good reason."),
 ],
 "exercises": [
   "Take a feature request phrased as a solution — from your own "
   "project, or an open-source issue tracker — and work backwards to the "
   "underlying problem by asking why repeatedly. Propose two alternative "
   "solutions.",
   "Write acceptance criteria for a feature you have built. Include the empty "
   "state, the error cases, and a performance criterion. Then check your "
   "implementation against them and record what fails.",
   "Write preconditions, postconditions, and an invariant for three functions "
   "in an existing codebase. Assert them in a debug build and run the test "
   "suite. Report any that fire.",
   "Take a requirement written as 'the system shall be fast/secure/reliable' "
   "and rewrite it so that compliance can be determined.",
   "Find a quality requirement in a system you use that was clearly "
   "discovered late — bolted-on auditing, a pagination system added "
   "under duress. Describe the architectural damage.",
   "Write an architecture decision record for a decision you have already "
   "made, including the alternatives you rejected and why.",
   "For your Project 2 open-source target, read three closed issues and "
   "classify each as a well-specified requirement or a proposed solution.",
 ],
 "selfcheck": [
   "Give five structural reasons requirements elicitation is difficult.",
   "Why is a stated requirement usually a proposed solution, and what do you "
   "do about it?",
   "Distinguish functional from quality requirements, and say why the latter "
   "are harder to retrofit.",
   "Name the four properties of a useful specification, and give the failure "
   "mode of ignoring minimality.",
   "What does a contract accomplish beyond documentation?",
   "Where should you validate inputs, and what goes wrong if you validate "
   "everywhere?",
   "Why is changing requirements not a failure of analysis, and what does "
   "that imply for design?",
 ],
},

]

# --- additional module batches ----------------------------------------------
for _b in ("c606_b2", "c606_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
