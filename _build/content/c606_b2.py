# -*- coding: utf-8 -*-
"""CSCE 606 — Modules 03-07."""

MODULES = [

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Modularity: Coupling and Cohesion",
 "subtitle": "The one design idea that actually reduces change cost.",
 "question": "What makes a codebase easy to change?",
 "outcomes": [
     "Define coupling and cohesion and recognise each in code.",
     "Explain information hiding and what a module should hide.",
     "Distinguish deep modules from shallow ones.",
     "Recognise when abstraction adds cost rather than removing it.",
     "Judge a decomposition by the change it makes cheap.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The goal",
   "blurb": "Make the likely change touch one place."},

  {"t": "callout", "title": "Modularity is about change, not tidiness",
   "kind": "The framing",
   "body": ["A module boundary is a bet: <i>this will change "
            "independently of that</i>.",
            "A good decomposition means a likely change touches <b>one</b> "
            "module. A bad one means it touches seven, and you must "
            "understand all seven.",
            "So the question is never 'is this well organised?' but "
            "<b>'what change does this make cheap, and is that the change "
            "that will come?'</b>",
            "Which means decomposition depends on what you expect to change "
            "— and a decomposition that was right can stop being right."]},

  {"t": "two", "kicker": "The two measures", "title": "Coupling and cohesion",
   "lh": "Coupling — between modules",
   "l": ["How much one module depends on another's details.",
         "<b>Want: low.</b>",
         "High coupling means a change here forces a change there.",
         ("Measured by: what must I know about B to change A?", 1)],
   "rh": "Cohesion — within a module",
   "r": ["How closely the parts of one module belong together.",
         "<b>Want: high.</b>",
         "Low cohesion means the module has no single reason to exist.",
         ("Measured by: can I describe what it does in one sentence "
          "without 'and'?", 1)],
   "note": "The one-sentence test for cohesion is the most practical "
           "heuristic in the module."},

  {"t": "table", "kicker": "Coupling", "title": "Forms of coupling, worst last",
   "header": ["Kind", "What it means", "Severity"],
   "widths": [2.8, 5.0, 4.3],
   "rows": [
     ["Data", "Pass simple values", "<b>Best</b>"],
     ["Stamp", "Pass a structure, use part of it", "Fine"],
     ["Control", "Pass a flag that changes behaviour", "Suspicious"],
     ["Common", "Share global mutable state", "Bad"],
     ["Content", "Reach into another module's internals", "<b>Worst</b>"],
   ],
   "note": "Control coupling is the interesting one: a boolean parameter "
           "usually means the function should have been two functions."},

  {"t": "callout", "title": "A boolean parameter is usually two functions",
   "kind": "The control coupling smell",
   "body": ["<code>process(data, validate=True)</code> means the caller is "
            "selecting between two behaviours.",
            "The caller now has to know what the flag does — that is "
            "coupling to an internal decision.",
            "Usually better: <code>process(data)</code> and "
            "<code>process_unvalidated(data)</code>. Each has one "
            "behaviour, one name, and one reason to be called.",
            "<b>Exception:</b> a flag that configures genuinely orthogonal "
            "behaviour, where the alternative is combinatorial function "
            "names. Judgement, not a rule."]},

  {"t": "section", "label": "Part 2", "title": "Information hiding",
   "blurb": "Parnas, 1972, and still the central idea."},

  {"t": "bullets", "kicker": "Parnas", "title": "Decompose by what changes, not by what happens",
   "items": [
     "The obvious decomposition follows the <b>flowchart</b>: one module per "
     "processing step.",
     "",
     "Parnas's argument: decompose instead so that each module <b>hides a "
     "design decision likely to change</b>.",
     "",
     "A module's interface reveals what callers need. Its implementation "
     "hides the decision.",
     "",
     "<b>Test:</b> if that decision changes, how many modules change? One "
     "means the boundary was right.",
     "",
     "Fifty years old, and still the most useful thing written about "
     "software structure.",
   ],
   "note": "Parnas's 1972 paper is short and worth reading in full — it "
           "is genuinely still the best statement of this."},

  {"t": "code", "kicker": "Example", "title": "Two decompositions of the same program",
   "lang": "text", "code": """
BY PROCESSING STEP (follows the flowchart):
    read_input() -> tokenize() -> count() -> sort() -> print()

  Change the storage format for word counts?
  -> count, sort, and print all change. THREE modules.

BY HIDDEN DECISION (Parnas):
    InputSource        hides: where input comes from
    WordStore          hides: how counts are stored
    Formatter          hides: how output is arranged

  Change the storage format?
  -> WordStore changes. ONE module.

Same program. The second absorbs the likely change.
""",
   "caption": "Parnas's original example from 1972, and it still makes the "
              "point faster than any modern one.",
   "note": "Have students do this exercise on their own code. It usually "
           "lands hard."},

  {"t": "section", "label": "Part 3", "title": "Deep and shallow modules",
   "blurb": "Interface size against implementation size."},

  {"t": "two", "kicker": "Ousterhout", "title": "Depth is the measure that matters",
   "lh": "Deep module — good",
   "l": ["Small interface, substantial implementation.",
         "Hides a lot behind a little.",
         "<code>open/read/write/close</code> — five calls hiding a file "
         "system.",
         ("Each one you learn buys a lot of capability.", 1)],
   "rh": "Shallow module — costly",
   "r": ["Large interface, thin implementation.",
         "Hides almost nothing; adds a layer to learn.",
         "A class that wraps one call and renames it.",
         ("Each one you learn buys nothing.", 1)],
   "note": "Depth reframes 'too many small classes' as a measurable problem "
           "rather than a matter of taste."},

  {"t": "callout", "title": "More abstraction is not automatically better",
   "kind": "Against reflexive layering",
   "body": ["Every layer has a cost: it must be learned, navigated, and "
            "debugged through.",
            "A layer pays for itself if it hides more complexity than it "
            "adds. A layer that renames one call and forwards it has negative "
            "value.",
            "<b>Classitis</b> — the belief that smaller classes are "
            "always better — produces codebases where understanding one "
            "operation means opening nine files.",
            "The right question is not 'is this abstracted?' but <b>'does "
            "this abstraction hide more than it costs?'</b>"]},

  {"t": "table", "kicker": "Judgement", "title": "When an abstraction pays",
   "header": ["Pays", "Does not pay"],
   "widths": [6.0, 6.1],
   "rows": [
     ["Hides a decision that will change", "Wraps something stable"],
     ["Used from many places", "One caller"],
     ["Interface much smaller than implementation", "Interface as large as implementation"],
     ["Removes duplication of <i>knowledge</i>", "Removes duplication of <i>text</i>"],
     ["Lets you reason locally", "Forces you to read through it anyway"],
   ],
   "note": "The knowledge-vs-text distinction is the key to DRY being applied "
           "correctly."},

  {"t": "callout", "title": "DRY is about knowledge, not text",
   "kind": "A widely misapplied rule",
   "body": ["'Don't repeat yourself' means: <i>every piece of knowledge "
            "should have one authoritative representation.</i>",
            "It does not mean 'no two pieces of code may look alike'.",
            "Two functions that happen to have the same five lines, for "
            "unrelated reasons, are <b>not</b> duplication. Merging them "
            "couples two things that will diverge, and the merged function "
            "grows flags to serve both — control coupling, arriving by "
            "the front door.",
            "<b>Ask: if the requirement changes, must both change?</b> If "
            "yes, it is duplication. If no, it is coincidence."]},

  {"t": "bullets", "kicker": "Practice", "title": "Assessing a decomposition",
   "items": [
     "<b>Name the likely changes.</b> Then trace how many modules each one "
     "touches.",
     "",
     "<b>One-sentence test.</b> Describe each module without using 'and'. If "
     "you cannot, cohesion is low.",
     "",
     "<b>Draw the dependency graph.</b> Cycles are a hard signal; a module "
     "everything depends on is a bottleneck.",
     "",
     "<b>Count interface size against implementation size.</b> Shallow "
     "modules are candidates for inlining.",
     "",
     "<b>Look for shotgun surgery</b> — a change that always touches the "
     "same seven files. That is a missing module.",
   ],
   "footnote": "Shotgun surgery is the most reliable symptom of a wrong "
               "boundary."},
 ],
 "takeaways": [
   "A module boundary is a bet that two things change independently. Judge it "
   "by which change it makes cheap.",
   "Low coupling between, high cohesion within. The one-sentence test — "
   "describe it without 'and' — catches poor cohesion fast.",
   "A boolean parameter that selects behaviour is usually two functions "
   "wearing one name.",
   "Parnas: decompose by the design decision each module hides, not by "
   "processing step.",
   "Depth is the measure: small interface over substantial implementation. A "
   "shallow module costs more than it hides.",
   "DRY is about knowledge, not text. If a requirement change would not force "
   "both to change, it is coincidence, not duplication.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What modularity is for"),
  ("callout", "A module boundary is a bet about change",
   ["Drawing a boundary asserts that what is inside will change "
    "independently of what is outside. If that is true, changes stay local "
    "and cheap. If it is false, every change crosses the boundary and you "
    "have added ceremony without benefit.",
    "So the question is never whether code is 'well organised' in the "
    "abstract. It is: <b>which change does this structure make cheap, and is "
    "that the change that will actually come?</b>",
    "This also means a decomposition that was correct can become incorrect. "
    "When the axis of change shifts — a new platform, a new regulation, "
    "a new scale — the boundaries that absorbed the old changes may "
    "cut directly across the new ones. That is not a failure of the original "
    "design; it is information arriving."]),
  ("h2", "1.1 &nbsp; Coupling and cohesion"),
  ("table", ["", "Coupling", "Cohesion"],
   [["Scope", "Between modules.", "Within a module."],
    ["Measures", "How much one module must know about another's internals.",
     "How closely the parts of a module belong together."],
    ["Want", "<b>Low.</b>", "<b>High.</b>"],
    ["Symptom when wrong", "A change here forces a change there.",
     "The module has no single reason to exist, so every change touches it."],
    ["Practical test", "To change A, how much of B must I read?",
     "Can I describe what this module does in one sentence, with no 'and'?"]],
   [0.15, 0.43, 0.42]),
  ("table", ["Coupling type", "Description", "Verdict"],
   [["<b>Data</b>", "Modules communicate by passing simple values.",
     "<b>Best available.</b>"],
    ["<b>Stamp</b>", "A whole record is passed where only part is used.",
     "Acceptable. Mildly over-shares, which matters if the record changes."],
    ["<b>Control</b>", "One module passes a flag that selects the other's "
     "behaviour.",
     "<b>Suspicious.</b> The caller now knows about an internal decision."],
    ["<b>Common</b>", "Modules share global mutable state.",
     "Bad. Any module can change what any other sees, so reasoning is no "
     "longer local."],
    ["<b>Content</b>", "One module reaches into another's internal "
     "representation.",
     "<b>Worst.</b> The boundary exists only on paper."]],
   [0.15, 0.47, 0.38]),
  ("callout", "The boolean parameter smell",
   ["<code>process(data, validate=True)</code> requires the caller to know "
    "what <code>validate</code> changes — which is coupling to an "
    "internal decision, and the flag's meaning must be rediscovered at every "
    "call site.",
    "Two functions are usually better: <code>process(data)</code> and "
    "<code>process_unvalidated(data)</code>. Each has one behaviour, one "
    "name, and one documented contract.",
    "<b>The exception is real:</b> a flag configuring genuinely orthogonal "
    "behaviour, where splitting produces a combinatorial explosion of "
    "function names. This is judgement, not a rule — but a flag that "
    "makes the function do something <i>different</i>, rather than doing the "
    "same thing differently, is almost always two functions."]),

  ("h1", "2 &nbsp; Information hiding"),
  ("p", "David Parnas's 1972 paper <i>On the Criteria To Be Used in "
        "Decomposing Systems into Modules</i> is the most important piece of "
        "writing about software structure, and the argument is simple enough "
        "to state in a paragraph."),
  ("p", "The obvious decomposition follows the <b>processing sequence</b>: a "
        "module per step of the flowchart. Parnas proposed decomposing "
        "instead so that each module <b>hides a design decision that is "
        "likely to change</b>. The interface exposes what callers genuinely "
        "need; the implementation conceals the decision."),
  ("code", """BY PROCESSING STEP:
    read_input -> tokenize -> count -> sort -> print

  "Change how word counts are stored."
  -> count, sort, and print all break.  THREE modules change.

BY HIDDEN DECISION:
    InputSource   hides  where input comes from
    WordStore     hides  how counts are represented
    Formatter     hides  how output is arranged

  "Change how word counts are stored."
  -> WordStore changes.  ONE module."""),
  ("p", "Same program, same functionality, radically different change cost. "
        "The test for a boundary is therefore: <i>name a plausible change, "
        "and count the modules it touches</i>. One is the target."),

  ("break",),
  ("h1", "3 &nbsp; Deep and shallow modules"),
  ("p", "John Ousterhout's framing in <i>A Philosophy of Software Design</i> "
        "gives a measurable version of 'good abstraction': compare the size "
        "of the interface against the size of what it hides."),
  ("table", ["", "Deep module", "Shallow module"],
   [["Shape", "Small interface, substantial implementation.",
     "Large interface, thin implementation."],
    ["Example", "A file system: <code>open</code>, <code>read</code>, "
     "<code>write</code>, <code>close</code>, <code>seek</code> — five "
     "calls concealing allocation, caching, journaling, and device drivers.",
     "A class that wraps a single library call, renames its parameters, and "
     "forwards."],
    ["Value", "Each interface element learned buys a great deal of "
     "capability.",
     "Each element learned buys nothing; you must still understand what is "
     "underneath."],
    ["Verdict", "<b>What to aim for.</b>",
     "A candidate for removal."]],
   [0.13, 0.44, 0.43]),
  ("callout", "More abstraction is not automatically better",
   ["Every layer imposes a cost: it must be learned, navigated during "
    "debugging, and kept consistent with what it wraps.",
    "A layer is worth its cost only if it hides more complexity than it "
    "introduces. A class that renames one function and calls it has negative "
    "value — it adds a file, a name, and a hop, and conceals nothing.",
    "Ousterhout calls the reflexive multiplication of tiny classes "
    "<b>classitis</b>. Its symptom is that understanding one operation "
    "requires opening nine files, none of which contains any logic.",
    "The right question is not 'is this abstracted?' but <b>'does this "
    "abstraction hide more than it costs?'</b>"]),
  ("table", ["An abstraction pays when it…", "and does not when it…"],
   [["Hides a decision that is genuinely likely to change.",
     "Wraps something that has been stable for a decade."],
    ["Is used from many call sites.", "Has exactly one caller."],
    ["Has an interface much smaller than its implementation.",
     "Has an interface as large as its implementation."],
    ["Eliminates duplicated <i>knowledge</i>.",
     "Eliminates duplicated <i>text</i> that is coincidentally similar."],
    ["Lets a reader reason locally without looking inside.",
     "Must be read through anyway to understand the caller."]],
   [0.5, 0.5]),
  ("h2", "3.1 &nbsp; DRY, correctly understood"),
  ("callout", "DRY is about knowledge, not characters",
   ["The original formulation is that <i>every piece of knowledge should have "
    "a single authoritative representation in the system</i>. It is a claim "
    "about knowledge, not about textual similarity.",
    "Two functions that happen to contain the same five lines, for unrelated "
    "reasons, are not duplication. Merging them couples two things that will "
    "later need to diverge — and when they do, the merged function grows "
    "a flag to serve both callers, which is control coupling arriving by the "
    "front door.",
    "<b>The test: if the requirement changes, must both copies change?</b> If "
    "yes, it is genuine duplication and should be unified. If no, the "
    "similarity is coincidence and unifying it creates a dependency that did "
    "not exist.",
    "Premature deduplication is at least as common and at least as expensive "
    "as duplication, and it is harder to undo."]),

  ("h1", "4 &nbsp; Assessing a decomposition"),
  ("ol", ["<b>Name the likely changes</b> — three to five specific ones "
          "— and trace how many modules each touches. More than one is "
          "evidence the boundary is in the wrong place.",
          "<b>Apply the one-sentence test.</b> Describe each module's purpose "
          "in a sentence without using 'and'. Failure indicates low cohesion: "
          "the module is two modules.",
          "<b>Draw the dependency graph.</b> Cycles are a hard signal that "
          "two modules are really one. A module that everything depends on is "
          "a change bottleneck.",
          "<b>Compare interface size against implementation size</b> for each "
          "module. Shallow ones are candidates for inlining.",
          "<b>Look for shotgun surgery</b> — a category of change that "
          "reliably touches the same seven files. That pattern names a module "
          "that does not exist yet, and is the most dependable symptom of a "
          "misplaced boundary."]),
  ("p", "Note that items 1 and 5 are the same test from opposite directions: "
        "predict the change and count the files, or observe the files and "
        "infer the missing boundary. The second is more reliable, because it "
        "uses evidence rather than speculation — which is an argument "
        "for refactoring boundaries after you have seen the changes rather "
        "than guessing them in advance."),
 ],
 "resources": [
   ("Parnas — On the Criteria To Be Used in Decomposing Systems into "
    "Modules (1972, free)",
    "https://www.win.tue.nl/~wstomv/edu/2ip30/references/criteria_for_modularization.pdf",
    "Ten pages, fifty years old, and still the best thing written on this. "
    "Read it in full."),
   ("Ousterhout — A Philosophy of Software Design",
    "https://web.stanford.edu/~ouster/cgi-bin/book.php",
    "Deep modules, classitis, and complexity as a measurable property. Short "
    "and opinionated; the lecture video is free."),
   ("MIT 6.031 — Abstract Data Types, Abstraction Functions",
    "https://web.mit.edu/6.031/www/",
    "The formal side: representation invariants and what an abstraction "
    "boundary actually guarantees."),
   ("Martin Fowler — Refactoring catalogue (code smells)",
    "https://refactoring.com/catalog/",
    "Shotgun surgery, feature envy, and the rest, with the corresponding "
    "refactorings."),
 ],
 "exercises": [
   "Take a program of your own and list five plausible changes. For each, "
   "count the files that would need modifying. Identify the worst case and "
   "propose a boundary that would fix it.",
   "Apply the one-sentence test to every module in a codebase you know. "
   "Record which fail and what the second responsibility is.",
   "Do Parnas's exercise: take a small program structured by processing step "
   "and restructure it by hidden decision. Measure the change cost before and "
   "after on a specific modification.",
   "Draw the dependency graph for a project. Find the cycles, and the module "
   "with the highest fan-in. Propose a change to each.",
   "Find a shallow module in a real codebase — interface roughly the "
   "size of its implementation — and inline it. Judge whether the "
   "result is clearer.",
   "Find two pieces of similar-looking code and determine whether they are "
   "genuine duplication by the requirement-change test. If they are not, "
   "write down what would have gone wrong had you merged them.",
   "Use version control history to find shotgun surgery: files that are "
   "frequently modified together. <code>git log</code> with some scripting "
   "will do it. What missing module does the pattern name?",
 ],
 "selfcheck": [
   "What is a module boundary a bet about, and how do you judge one?",
   "Define coupling and cohesion, and give a practical test for each.",
   "Why is a boolean parameter that selects behaviour usually a smell, and "
   "what is the exception?",
   "State Parnas's criterion for decomposition and contrast it with the "
   "obvious alternative.",
   "What makes a module deep, and what is wrong with a shallow one?",
   "What does DRY actually claim, and what is the test for genuine "
   "duplication?",
   "What is shotgun surgery and what does it indicate?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Architecture",
 "subtitle": "The decisions that are expensive to reverse.",
 "question": "Which design decisions deserve to be made up front?",
 "outcomes": [
     "Explain what distinguishes architecture from design.",
     "Identify the quality attributes that drive architectural choice.",
     "Compare layered, hexagonal, and event-driven styles honestly.",
     "Explain the monolith/microservice trade without slogans.",
     "Defer decisions that can be deferred.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What architecture is",
   "blurb": "The subset of decisions that are hard to change later."},

  {"t": "callout", "title": "Architecture is the expensive-to-reverse part",
   "kind": "The definition that is useful",
   "body": ["Not 'the high-level design' — that is vague and invites "
            "diagram-drawing.",
            "<b>Architecture is the set of decisions that are expensive to "
            "change after the fact.</b>",
            "Which database? Synchronous or asynchronous? One deployable or "
            "many? Where does state live? What is the consistency model?",
            "The practical consequence: identify which decisions are "
            "genuinely expensive to reverse, think hard about <i>those</i>, "
            "and defer everything else. Most decisions are not "
            "architectural and should be made as late as possible."]},

  {"t": "bullets", "kicker": "Drivers", "title": "Quality attributes drive architecture",
   "items": [
     "Functional requirements rarely determine structure — almost any "
     "architecture can implement almost any feature.",
     "",
     "<b>Quality attributes do:</b>",
     ("<b>Scale</b> — how much, and growing how?", 1),
     ("<b>Latency</b> — what must be fast, and at which percentile?", 1),
     ("<b>Availability</b> — what does downtime cost?", 1),
     ("<b>Consistency</b> — can users see stale data?", 1),
     ("<b>Security</b> — what boundaries must hold?", 1),
     ("<b>Team structure</b> — Conway's law is a constraint.", 1),
     "",
     "Get these wrong and no amount of clean code rescues it.",
   ],
   "note": "Tying this to Module 02's quality requirements makes the "
           "dependency explicit."},

  {"t": "section", "label": "Part 2", "title": "Styles",
   "blurb": "Each solves a problem. Know which."},

  {"t": "table", "kicker": "Styles", "title": "Four common architectures",
   "header": ["Style", "Organises by", "Good when", "Weak when"],
   "widths": [2.4, 3.0, 3.4, 3.3],
   "rows": [
     ["Layered", "Abstraction level", "Clear direction of dependency", "Changes cut across layers"],
     ["Hexagonal", "Core vs adapters", "Domain logic must be testable", "Ceremony for simple apps"],
     ["Event-driven", "Messages", "Decoupling; async; audit", "<b>Hard to debug</b>"],
     ["Pipeline", "Stages", "Data transformation", "Interactive work"],
   ],
   "note": "Event-driven's debugging cost is routinely underestimated and "
           "worth stating plainly."},

  {"t": "callout", "title": "Hexagonal: the useful core of it",
   "kind": "Worth knowing",
   "body": ["Put the domain logic in the middle, with <b>no dependencies on "
            "anything external</b> — no database, no framework, no HTTP.",
            "Everything external is an <b>adapter</b> plugged into a port "
            "the core defines.",
            "<b>The payoff is testability:</b> the core can be tested with no "
            "database, no network, and no fixtures — so those tests are "
            "fast and they do not break when the framework changes.",
            "<b>The cost is indirection.</b> For a small CRUD application it "
            "is pure ceremony. For a system with real domain rules that will "
            "outlive three frameworks, it pays."]},

  {"t": "section", "label": "Part 3", "title": "Monolith and microservices",
   "blurb": "The argument that generates the most heat and the least light."},

  {"t": "table", "kicker": "Honest comparison", "title": "What each actually costs",
   "header": ["", "Monolith", "Microservices"],
   "widths": [2.6, 4.6, 4.9],
   "rows": [
     ["Deploy", "One unit — simple", "Many units — needs tooling"],
     ["Calls", "Function calls", "<b>Network calls that fail</b>"],
     ["Consistency", "Transactions work", "<b>Distributed, so they do not</b>"],
     ["Debug", "One stack trace", "Distributed tracing required"],
     ["Scale", "Whole app together", "Per service"],
     ["Teams", "Coordinate on one codebase", "<b>Deploy independently</b>"],
   ],
   "note": "The independent-deploy row is the only one that is reliably a "
           "microservice win — and it is an organisational benefit."},

  {"t": "callout", "title": "Microservices are an organisational solution",
   "kind": "The honest framing",
   "body": ["Nearly every technical column above favours the monolith. "
            "Function calls do not fail; transactions work; one stack trace "
            "tells you what happened.",
            "The genuine benefit is <b>independent deployment by independent "
            "teams</b>. Twelve teams sharing one deploy pipeline is a real "
            "coordination cost, and splitting removes it.",
            "That is a Conway's law argument, not a technical one. If you "
            "have one team, you are paying distributed systems costs "
            "(Module 12 of CSCE 611) to solve a problem you do not have.",
            "<b>Default: start with a well-modularised monolith.</b> Extract "
            "a service when a specific pressure — team coordination, or "
            "one component needing to scale separately — justifies it."]},

  {"t": "bullets", "kicker": "The trap", "title": "The distributed monolith",
   "items": [
     "Split into services <b>without</b> fixing the coupling, and you get the "
     "worst of both.",
     "",
     "Services that must be deployed together. Changes that span five "
     "repositories. Transactions that span services.",
     "",
     "Now you have monolith coupling <b>plus</b> network failure, latency, "
     "and distributed debugging.",
     "",
     "<b>The modular boundaries must exist first.</b> A service boundary is a "
     "module boundary with a network in it — and a network makes a bad "
     "boundary worse, not better.",
   ],
   "footnote": "If you cannot draw clean module boundaries in a monolith, "
               "splitting will not create them."},

  {"t": "section", "label": "Part 4", "title": "Deciding",
   "blurb": "And deferring."},

  {"t": "bullets", "kicker": "Method", "title": "How to make an architectural decision",
   "items": [
     "<b>1. Is it actually architectural?</b> Is it expensive to reverse? If "
     "not, defer it.",
     "",
     "<b>2. Which quality attribute drives it?</b> Name it, with a number.",
     "",
     "<b>3. What are the options,</b> and what does each cost?",
     "",
     "<b>4. What would change the answer?</b> Write it down — that is "
     "the revisit trigger.",
     "",
     "<b>5. Record it</b> as an ADR: context, decision, alternatives, "
     "consequences.",
   ],
   "note": "Step 4 is the one people skip and the one that makes the decision "
           "reviewable."},

  {"t": "callout", "title": "Defer what you can",
   "kind": "The underrated skill",
   "body": ["Every decision made early is made with the least information "
            "you will ever have.",
            "So the valuable skill is identifying which decisions can be "
            "<b>postponed without cost</b> — and structuring the system "
            "so that more of them can be.",
            "Keeping the database behind an interface defers the database "
            "choice. Keeping transport out of the domain defers REST versus "
            "gRPC.",
            "<b>But do not defer by ignoring.</b> An undeferred decision made "
            "implicitly — by whichever library someone imported first "
            "— is the worst case: expensive to reverse and nobody "
            "decided it."]},
 ],
 "takeaways": [
   "Architecture is the set of decisions expensive to reverse. Identify "
   "those, think hard about them, and defer everything else.",
   "Quality attributes drive architecture; functional requirements rarely do. "
   "Name them with numbers.",
   "Hexagonal architecture buys testability by keeping the domain free of "
   "external dependencies, and costs indirection.",
   "Nearly every technical comparison favours the monolith. Microservices "
   "solve an organisational problem — independent deployment.",
   "A distributed monolith is the worst outcome: monolith coupling plus "
   "network failure. Module boundaries must exist before service boundaries.",
   "Write down what would change the answer. That turns a decision into "
   "something reviewable rather than something to defend.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What architecture is"),
  ("callout", "The useful definition",
   ["Defining architecture as 'the high-level design' invites diagrams and "
    "settles nothing.",
    "<b>Architecture is the subset of design decisions that are expensive to "
    "change once made.</b> Which datastore. Synchronous or asynchronous "
    "communication. One deployable unit or many. Where state lives. What "
    "consistency model users experience. Where the trust boundaries fall.",
    "The practical value of this definition is that it tells you where to "
    "spend thought. A decision that can be reversed in an afternoon does not "
    "need a design review; a decision that would take six months to undo "
    "does.",
    "<b>Most decisions are not architectural</b> and should be made as late "
    "as possible, by the person doing the work."]),
  ("h2", "1.1 &nbsp; What drives it"),
  ("p", "Functional requirements rarely determine structure. Almost any "
        "architecture can be made to implement almost any feature; it is the "
        "<b>quality attributes</b> of Module 02 that constrain the shape."),
  ("table", ["Attribute", "The question to ask", "What it constrains"],
   [["<b>Scale</b>", "How much load, growing at what rate, in which "
     "dimension?",
     "Partitioning, statelessness, caching strategy."],
    ["<b>Latency</b>", "What must be fast, measured at which percentile?",
     "Synchronous versus asynchronous; how many network hops are permitted on "
     "the critical path."],
    ["<b>Availability</b>", "What does an hour of downtime cost?",
     "Redundancy, failover, how much of the system may share a failure "
     "domain."],
    ["<b>Consistency</b>", "May a user see stale data, and for how long?",
     "Whether distribution is viable at all for that data."],
    ["<b>Security</b>", "Which boundaries must hold, against whom?",
     "Process and network isolation, where secrets live (CSCE 611 "
     "Module 11)."],
    ["<b>Team structure</b>", "How many teams, and how independent must they "
     "be?",
     "Deployment units. Conway's law is a constraint, not a suggestion."]],
   [0.17, 0.40, 0.43]),

  ("h1", "2 &nbsp; Architectural styles"),
  ("table", ["Style", "Organising principle", "Suits", "Struggles with"],
   [["<b>Layered</b>", "Abstraction level; dependencies point one way.",
     "Systems with a clear stack of concerns. Easy to explain and to "
     "enforce.",
     "Changes that cut across layers — adding one field can require "
     "touching every layer, which is shotgun surgery by design."],
    ["<b>Hexagonal / ports and adapters</b>",
     "A dependency-free core surrounded by pluggable adapters.",
     "Systems with substantial domain logic that must outlive their "
     "frameworks and be testable in isolation.",
     "Simple CRUD applications, where it is ceremony without payoff."],
    ["<b>Event-driven</b>", "Components communicate by publishing and "
     "consuming events.",
     "Decoupling producers from consumers; asynchronous work; natural audit "
     "logs; adding consumers without touching producers.",
     "<b>Debugging.</b> There is no call stack. Understanding why something "
     "happened means reconstructing a causal chain across components, and "
     "ordering and duplicate handling become your problem."],
    ["<b>Pipeline</b>", "Stages transforming a stream.",
     "Data processing, compilers, media.",
     "Interactive systems and anything needing to go backwards."]],
   [0.17, 0.26, 0.29, 0.28]),
  ("callout", "Hexagonal architecture, and what it actually buys",
   ["Place the domain logic at the centre with <b>no dependencies on "
    "anything external</b> — no ORM, no web framework, no HTTP types, no "
    "database. The core defines <i>ports</i> (interfaces it needs); "
    "everything external is an <i>adapter</i> implementing one.",
    "<b>The payoff is testability.</b> The core can be tested with no "
    "database, no network, no fixtures, and no framework test harness. Those "
    "tests run in milliseconds and keep working when the framework is "
    "replaced — which it will be.",
    "<b>The cost is indirection.</b> Every external interaction goes through "
    "an interface and an implementation, which is real navigational overhead. "
    "For an application that is mostly forwarding HTTP requests to SQL, this "
    "is pure ceremony.",
    "The judgement is whether there is enough genuine domain logic to be "
    "worth protecting. If the answer is 'the domain logic is "
    "<code>INSERT</code>', there is not."]),

  ("break",),
  ("h1", "3 &nbsp; Monoliths and microservices"),
  ("table", ["", "Monolith", "Microservices"],
   [["Deployment", "One artefact. Simple.",
     "Many artefacts, needing orchestration, service discovery, and version "
     "compatibility management."],
    ["Inter-component calls", "Function calls. They do not fail.",
     "<b>Network calls, which fail</b>, time out, and may have executed "
     "despite failing (CSCE 611 Module 12)."],
    ["Consistency", "Database transactions work.",
     "<b>Transactions do not span services.</b> You get sagas, compensating "
     "actions, and eventual consistency."],
    ["Debugging", "One stack trace.",
     "Distributed tracing, correlation IDs, and log aggregation — all of "
     "which must be built before you need them."],
    ["Scaling", "The whole application scales together.",
     "Each service scales independently, which matters if one component is "
     "the bottleneck."],
    ["Team autonomy", "All teams coordinate on one codebase and one "
     "release.",
     "<b>Teams deploy independently.</b>"],
    ["Technology choice", "One stack.",
     "Per-service choice — a genuine benefit and a real fragmentation "
     "risk."]],
   [0.17, 0.39, 0.44]),
  ("callout", "Microservices solve an organisational problem",
   ["Read the table honestly: nearly every technical row favours the "
    "monolith. Function calls are faster and cannot fail halfway. "
    "Transactions work. One stack trace explains the whole request.",
    "The row that reliably favours microservices is <b>team autonomy</b>. "
    "Twelve teams sharing one deployment pipeline is a genuine and growing "
    "coordination cost: every release requires everyone's changes to be "
    "ready, and one team's bug blocks everyone.",
    "<b>That is a Conway's law argument, not a technical one.</b> If you have "
    "one team, or three, you are paying the full cost of distributed systems "
    "to solve a coordination problem you do not have.",
    "<b>Reasonable default:</b> start with a well-modularised monolith. "
    "Extract a service when a specific, identified pressure justifies it "
    "— a team that needs independent release cadence, or a component "
    "whose scaling profile differs sharply from the rest. Extracting one "
    "service for a reason is very different from decomposing everything on "
    "principle."]),
  ("callout", "The distributed monolith",
   ["Split a system into services without first fixing the coupling, and the "
    "result combines the disadvantages of both.",
    "The symptoms are unmistakable: services that must be deployed together "
    "in a particular order; a single feature requiring coordinated changes "
    "across five repositories; a shared database that every service writes "
    "to; transactions that span services and are implemented with hope.",
    "You now have the monolith's coupling <i>plus</i> network latency, "
    "partial failure, and distributed debugging. This is strictly worse than "
    "either alternative.",
    "<b>The modular boundaries must exist before the service boundaries.</b> "
    "A service boundary is a module boundary with a network in it, and "
    "putting a network inside a bad boundary makes it worse, not better. If "
    "you cannot draw clean module boundaries within a monolith, splitting "
    "into services will not create them — it will only make the mess "
    "harder to see."]),

  ("h1", "4 &nbsp; Making and deferring decisions"),
  ("ol", ["<b>Is this actually architectural?</b> Estimate the cost of "
          "reversing it in a year. If it is low, this is not an "
          "architectural decision and should be made by whoever is doing the "
          "work, now, without a meeting.",
          "<b>Which quality attribute drives it?</b> Name it, with a number. "
          "'We need it to scale' is not a driver; 'ten thousand concurrent "
          "users by Q3, 99th-percentile latency under 300 ms' is.",
          "<b>What are the realistic options, and what does each cost?</b> "
          "Including the option of doing nothing yet.",
          "<b>What would change the answer?</b> Write it down explicitly. "
          "This converts the decision from something to be defended into "
          "something to be reviewed when the trigger fires.",
          "<b>Record it</b> as an architecture decision record: context, "
          "decision, alternatives considered, consequences accepted. Ten "
          "minutes now; an avoided argument in a year."]),
  ("callout", "Deferring is a skill",
   ["Every decision made early is made with the least information you will "
    "ever have about the problem. The value of deferring is that the decision "
    "gets made with more.",
    "So part of the work is structuring the system so that <i>more</i> "
    "decisions can be deferred. Keeping persistence behind an interface "
    "defers the database choice. Keeping transport concerns out of the domain "
    "defers REST versus gRPC. Keeping the deployment unit singular defers the "
    "microservice question indefinitely.",
    "<b>But do not confuse deferring with ignoring.</b> A decision that is "
    "never consciously made still gets made — implicitly, by whichever "
    "library someone imported first on a Tuesday. That is the worst case: "
    "expensive to reverse, and nobody chose it or recorded why.",
    "Defer explicitly, write down that you are deferring, and name the "
    "trigger that will force the decision."]),
 ],
 "resources": [
   ("Martin Fowler — Software Architecture Guide",
    "https://martinfowler.com/architecture/",
    "Including 'Who needs an architect?' and the microservices material, "
    "which is unusually balanced for the topic."),
   ("Fowler — MonolithFirst and Microservice Premium",
    "https://martinfowler.com/bliki/MonolithFirst.html",
    "The argument for &sect;3's default, from someone who advocates "
    "microservices where they fit."),
   ("Alistair Cockburn — Hexagonal Architecture",
    "https://alistair.cockburn.us/hexagonal-architecture/",
    "The original description. Shorter and clearer than most of what has been "
    "written about it since."),
   ("Michael Nygard — Release It!",
    "https://pragprog.com/titles/mnee2/release-it-second-edition/",
    "Stability patterns and failure modes in production systems. The chapter "
    "on failure cascades is worth the book."),
 ],
 "exercises": [
   "List the architectural decisions in a system you have built. For each, "
   "estimate the cost of reversing it now. Identify which you made "
   "deliberately and which were made by default.",
   "Write an ADR for one of them, retrospectively: context, options, "
   "decision, consequences, and what would change the answer.",
   "Take a small application and restructure its core to have no dependency "
   "on its framework or database. Measure test suite runtime before and "
   "after.",
   "Find an open-source project that migrated to or from microservices. Read "
   "their write-up and identify which of the table's rows actually drove it.",
   "For a system you know, name the quality attribute that most constrains "
   "its architecture, and state it with a number.",
   "Identify a decision in your current project that is being made implicitly "
   "rather than deliberately. Write it down and decide it.",
   "Take a monolithic codebase and identify where you would cut a service, "
   "based on module boundaries and change-coupling data from version control "
   "history.",
 ],
 "selfcheck": [
   "What is the useful definition of architecture, and why does it help?",
   "Why do quality attributes drive architecture while functional "
   "requirements usually do not?",
   "What does hexagonal architecture buy, what does it cost, and when is it "
   "not worth it?",
   "Which column of the monolith/microservices comparison reliably favours "
   "microservices, and what kind of argument is that?",
   "What is a distributed monolith and why is it worse than either "
   "alternative?",
   "Name the five steps of an architectural decision, and say which is most "
   "often skipped.",
   "What is the difference between deferring a decision and ignoring it?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Testing",
 "subtitle": "Buying confidence, and deciding how much to pay.",
 "question": "What should you test, and how much is enough?",
 "outcomes": [
     "Explain what tests actually buy and what they do not.",
     "Distinguish test sizes and their different purposes.",
     "Explain why coverage is a poor target.",
     "Write tests that survive refactoring.",
     "Assess the honest evidence on TDD.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What tests are for",
   "blurb": "Not primarily finding bugs."},

  {"t": "callout", "title": "Tests buy the confidence to change things",
   "kind": "The real purpose",
   "body": ["The obvious answer — tests find bugs — is true and "
            "secondary.",
            "The primary value is that <b>a good test suite makes change "
            "safe</b>. Without one, every modification to unfamiliar code is "
            "a gamble, so people stop modifying it, and the codebase "
            "ossifies.",
            "A test suite is therefore not a quality gate bolted on at the "
            "end. It is the thing that keeps the cost of change from rising "
            "over time — which Module 01 identified as the whole point.",
            "Secondary benefits: tests document intent executably, and they "
            "pressure the design toward testability, which usually means "
            "lower coupling."]},

  {"t": "table", "kicker": "Sizes", "title": "Tests by scope, not by name",
   "header": ["Size", "Scope", "Speed", "Tells you"],
   "widths": [2.2, 3.6, 2.6, 3.7],
   "rows": [
     ["Small", "One process, no I/O, no clock", "<b>Milliseconds</b>", "This unit's logic is right"],
     ["Medium", "One machine, local DB, no network", "Seconds", "These components fit together"],
     ["Large", "Full system, real dependencies", "Minutes", "<b>It actually works</b>"],
   ],
   "footnote": "Google's taxonomy. Sizing by <i>what is allowed</i> is more "
               "useful than arguing about 'unit'.",
   "note": "The constraint-based definition sidesteps the endless "
           "unit-vs-integration terminology argument."},

  {"t": "bullets", "kicker": "The pyramid", "title": "Proportions, and the honest caveat",
   "items": [
     "<b>Many small, fewer medium, few large.</b> Fast tests run constantly; "
     "slow ones run rarely.",
     "",
     "<b>Why:</b> a small test failing points at one place. A large test "
     "failing says something somewhere broke.",
     "",
     "<b>The caveat:</b> small tests can all pass while the system is "
     "entirely broken, because the units do not fit together.",
     "",
     "So the pyramid is a guideline about cost, not about value. <b>Some "
     "end-to-end tests are mandatory</b> — they are the only ones that "
     "test what the user experiences.",
   ],
   "note": "Being honest about the pyramid's limitation is better than "
           "repeating it as doctrine."},

  {"t": "section", "label": "Part 2", "title": "Coverage",
   "blurb": "A useful diagnostic and a terrible target."},

  {"t": "callout", "title": "Coverage measures execution, not verification",
   "kind": "Why the number misleads",
   "body": ["Coverage tells you a line <i>ran</i> during the test suite. It "
            "says nothing about whether anything was checked.",
            "A test that calls every function and asserts nothing achieves "
            "100% coverage and verifies nothing at all.",
            "<b>Low coverage is informative:</b> code with none is "
            "definitely untested. <b>High coverage is not:</b> it may mean "
            "well tested, or it may mean assertion-free.",
            "<b>And as a target it is actively harmful</b> — Goodhart's "
            "law. Mandate 80% and you get tests written to raise the number, "
            "which are the least valuable tests and the most expensive to "
            "maintain."]},

  {"t": "bullets", "kicker": "Better questions", "title": "Instead of coverage",
   "items": [
     "<b>Mutation testing.</b> Introduce deliberate bugs; see how many the "
     "suite catches. Measures whether tests <i>verify</i>.",
     "",
     "<b>'Can I refactor this safely?'</b> If not, the suite is inadequate "
     "regardless of the number.",
     "",
     "<b>'Does every bug fix come with a regression test?'</b> A cheap and "
     "effective discipline.",
     "",
     "<b>'Which untested code would hurt most if wrong?'</b> Target that, not "
     "the percentage.",
   ],
   "footnote": "Mutation testing is slow and is the only direct measure of "
               "test quality."},

  {"t": "section", "label": "Part 3", "title": "Tests that last",
   "blurb": "Most bad test suites are bad in the same way."},

  {"t": "callout", "title": "Test behaviour, not implementation",
   "kind": "The one rule that matters",
   "body": ["A test coupled to <i>how</i> the code works breaks whenever the "
            "code is refactored — even though nothing the user cares "
            "about changed.",
            "That inverts the purpose: the suite was supposed to make "
            "refactoring safe, and now it punishes refactoring.",
            "<b>Symptom:</b> heavy mocking that asserts which internal "
            "methods were called in which order. That is a test of the "
            "implementation.",
            "<b>Test through the public interface.</b> If something is hard "
            "to test that way, the design usually has a problem — which "
            "is the useful signal."]},

  {"t": "code", "kicker": "Example", "title": "Brittle and durable versions of one test",
   "lang": "python", "code": """
# BRITTLE -- asserts HOW it works
def test_discount():
    repo, calc = Mock(), Mock()
    svc = OrderService(repo, calc)
    svc.apply_discount(order, "SAVE10")
    repo.find_by_code.assert_called_once_with("SAVE10")   # internals
    calc.compute.assert_called_once()                     # internals
# Rename a method or reorder two calls -> test fails.
# Behaviour unchanged.

# DURABLE -- asserts WHAT it does
def test_discount_reduces_total_by_ten_percent():
    order = Order(items=[Item(price=100)])
    result = apply_discount(order, discount_code("SAVE10"))
    assert result.total == 90
# Refactor freely. The test fails only if the discount is wrong.
""",
   "caption": "The second is shorter, clearer, documents the requirement, and "
              "survives refactoring. It is better on every axis.",
   "note": "The name of the second test states the requirement — worth "
           "pointing out."},

  {"t": "table", "kicker": "Properties", "title": "What a good test looks like",
   "header": ["Property", "Means", "Violated by"],
   "widths": [2.6, 4.6, 4.9],
   "rows": [
     ["Fast", "Runs in milliseconds", "Real I/O, sleeps, network"],
     ["Deterministic", "Same result every time", "<b>Clocks, randomness, ordering</b>"],
     ["Isolated", "Independent of other tests", "Shared mutable fixtures"],
     ["Readable", "The failure explains itself", "Assertions with no message"],
     ["Focused", "One reason to fail", "Twenty assertions"],
   ],
   "note": "Determinism is the one that matters most, because flaky tests "
           "destroy trust in the whole suite."},

  {"t": "callout", "title": "A flaky test is worse than no test",
   "kind": "The thing to fix immediately",
   "body": ["A test that fails intermittently teaches people to ignore "
            "failures.",
            "Once 'just re-run it' becomes normal, <b>real</b> failures are "
            "ignored too, and the entire suite's value collapses — not "
            "just that test's.",
            "<b>Causes:</b> real time, real randomness, test ordering "
            "dependence, shared state, real network, timing assumptions.",
            "<b>Response:</b> fix it or delete it, immediately. Quarantining "
            "flaky tests indefinitely is how suites die slowly."]},

  {"t": "section", "label": "Part 4", "title": "TDD, honestly",
   "blurb": "The evidence is weaker than the advocacy."},

  {"t": "two", "kicker": "TDD", "title": "What is and is not supported",
   "lh": "Well supported",
   "l": ["Writing tests helps.",
         "Writing a test before fixing a bug ensures it is really fixed.",
         "Thinking about testability improves design.",
         ("Hard to test usually means badly coupled.", 1)],
   "rh": "Not well supported",
   "r": ["That tests must come <b>first</b> specifically.",
         "That strict red-green-refactor beats test-after.",
         "That TDD measurably improves defect rates.",
         ("Studies conflict. Advocacy outruns evidence.", 1)],
   "note": "Students meet TDD as doctrine. An honest account is more useful "
           "and more credible."},

  {"t": "bullets", "kicker": "Defensible", "title": "What to actually do",
   "items": [
     "<b>Write a failing test before fixing any bug.</b> Proves the bug "
     "exists and that the fix works. Nearly free, and universally sensible.",
     "",
     "<b>Write tests before code when the interface is unclear</b> — the "
     "test forces you to use the API before building it.",
     "",
     "<b>Write tests after when the design is obvious</b> and you want to "
     "explore first.",
     "",
     "<b>Always write them.</b> The ordering is a working preference; "
     "<i>having</i> them is not.",
   ],
   "footnote": "Treating TDD as a tool rather than an identity makes it more "
               "useful."},
 ],
 "takeaways": [
   "Tests primarily buy the confidence to change code. Finding bugs is "
   "secondary.",
   "Size tests by what they are allowed to touch — process, machine, "
   "network — rather than arguing about 'unit'.",
   "The pyramid is about cost, not value. Small tests can all pass while the "
   "system is broken, so some end-to-end tests are mandatory.",
   "Coverage measures execution, not verification. Low coverage is "
   "informative; high coverage is not; as a target it is harmful.",
   "Test behaviour through the public interface. Tests coupled to "
   "implementation punish the refactoring they were meant to enable.",
   "A flaky test is worse than no test, because it teaches people to ignore "
   "failures. Fix or delete it immediately.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What tests are actually for"),
  ("callout", "Confidence to change, not defect detection",
   ["The standard answer is that tests find bugs. True, and it is the "
    "secondary benefit.",
    "The primary benefit is that a trustworthy test suite <b>makes change "
    "safe</b>. Without one, modifying unfamiliar code is a gamble, so people "
    "avoid it — they add new code beside the old rather than changing "
    "it, special-case around problems rather than fixing them, and eventually "
    "declare the system legacy and propose a rewrite.",
    "A test suite is therefore not a quality gate attached at the end of "
    "development. It is the mechanism that prevents the cost of change from "
    "rising over time, which Module 01 identified as the entire point of the "
    "discipline.",
    "Two secondary benefits are worth naming. Tests <b>document intent "
    "executably</b> — unlike comments, they cannot silently become "
    "false. And the requirement to be testable exerts <b>design pressure</b> "
    "toward lower coupling, because tightly coupled code is hard to test in "
    "isolation."]),
  ("h2", "1.1 &nbsp; Sizing tests"),
  ("p", "The terms 'unit test' and 'integration test' generate more argument "
        "than clarity. Google's taxonomy sizes tests by <i>what they are "
        "permitted to touch</i>, which is objective and useful."),
  ("table", ["Size", "May use", "May not use", "Typical runtime"],
   [["<b>Small</b>", "One process, one thread.",
     "No file system, no network, no database, no sleeping, no real clock, no "
     "randomness.", "Milliseconds. Run on every save."],
    ["<b>Medium</b>", "One machine; local database; multiple processes.",
     "No external network.", "Seconds. Run before every commit."],
    ["<b>Large</b>", "Anything, including real external services.",
     "—", "Minutes. Run in CI, or before release."]],
   [0.12, 0.30, 0.34, 0.24]),
  ("p", "The constraints make the categories enforceable — a test "
        "framework can prohibit network access in small tests — and "
        "they correlate directly with speed and with determinism, which are "
        "the properties that actually matter."),
  ("callout", "The pyramid, and its honest limitation",
   ["The usual advice is many small tests, fewer medium, few large. The "
    "reasoning is sound: fast tests can be run constantly and a failure "
    "localises the problem immediately, whereas a large test failure says "
    "only that something somewhere broke.",
    "<b>The limitation is real:</b> every small test can pass while the "
    "system is comprehensively broken, because the units work individually "
    "and do not fit together. Small tests verify the parts; only large tests "
    "verify the thing the user interacts with.",
    "So the pyramid is guidance about <i>cost distribution</i>, not about "
    "value. Some end-to-end tests are mandatory, however slow and awkward, "
    "because nothing else tests what was actually promised. The right number "
    "is small and it is not zero."]),

  ("h1", "2 &nbsp; Coverage"),
  ("callout", "Coverage measures execution, not verification",
   ["A coverage tool reports that a line was <i>executed</i> during the test "
    "run. It cannot report whether anything about the result was checked.",
    "A test suite that calls every function and asserts nothing achieves 100% "
    "line coverage and verifies nothing whatsoever. This is not a contrived "
    "example; suites written to satisfy a coverage mandate drift toward it "
    "naturally.",
    "<b>The asymmetry is what makes the metric usable at all.</b> Low "
    "coverage is genuinely informative: code never executed by any test is "
    "definitely untested. High coverage is uninformative: it is consistent "
    "with excellent testing and with no assertions at all.",
    "<b>As a target it is actively harmful</b> — a clean instance of "
    "Goodhart's law. Mandate 80% and the organisation produces exactly the "
    "tests that raise the number most cheaply, which are the least valuable "
    "tests in existence and which must then be maintained forever."]),
  ("table", ["Better question", "How to answer it"],
   [["Do my tests actually verify anything?",
     "<b>Mutation testing.</b> Automatically introduce small bugs — flip "
     "a comparison, change a constant — and measure how many the suite "
     "catches. Slow, and the only direct measure of test quality."],
    ["Can I refactor this safely?",
     "Attempt a refactoring. If you cannot tell whether you broke something, "
     "the suite is inadequate whatever the coverage number says."],
    ["Does every bug fix include a regression test?",
     "Check. This is a cheap, enforceable discipline that directly targets "
     "the code most likely to be wrong — code that has already been "
     "wrong once."],
    ["Which untested code would hurt most if it were wrong?",
     "Rank by consequence, not by percentage. Payment handling without tests "
     "matters more than a logging helper without tests."]],
   [0.34, 0.66]),

  ("break",),
  ("h1", "3 &nbsp; Tests that survive"),
  ("callout", "Test behaviour, not implementation",
   ["A test coupled to <i>how</i> code works fails whenever the code is "
    "restructured, even when the externally visible behaviour is identical.",
    "This inverts the purpose entirely. The suite existed to make refactoring "
    "safe; now refactoring breaks the suite, so people avoid refactoring, so "
    "the design degrades. The tests have become a cost rather than an asset.",
    "<b>The usual symptom is heavy mocking</b> with assertions about which "
    "internal methods were called, with which arguments, in which order. That "
    "is a test of the implementation, written in the vocabulary of the "
    "implementation.",
    "<b>Test through the public interface.</b> If something is genuinely hard "
    "to test that way, that is useful information about the design — "
    "usually that a responsibility is in the wrong place or that a dependency "
    "should be injected."]),
  ("code", """# BRITTLE -- asserts how it works
def test_discount():
    repo, calc = Mock(), Mock()
    svc = OrderService(repo, calc)
    svc.apply_discount(order, "SAVE10")
    repo.find_by_code.assert_called_once_with("SAVE10")
    calc.compute.assert_called_once()

# DURABLE -- asserts what it does
def test_discount_reduces_total_by_ten_percent():
    order = Order(items=[Item(price=100)])
    result = apply_discount(order, discount_code("SAVE10"))
    assert result.total == 90"""),
  ("p", "The second version is shorter, needs no mocking infrastructure, "
        "survives any internal restructuring, and — through its name "
        "— states the requirement. A reader learns what the system is "
        "supposed to do, which the first version never reveals."),
  ("table", ["Property", "Requirement", "Commonly broken by"],
   [["<b>Fast</b>", "Milliseconds for small tests.",
     "Real I/O, sleeps, network calls, spinning up containers."],
    ["<b>Deterministic</b>", "Identical result on every run.",
     "<b>Real clocks, real randomness, dependence on test ordering, "
     "concurrency.</b>"],
    ["<b>Isolated</b>", "Passes regardless of what else ran.",
     "Shared mutable fixtures, database state left behind, global "
     "configuration."],
    ["<b>Readable</b>", "A failure message explains the problem without "
     "opening the test.",
     "Bare assertions, obscure fixture setup, assertions on opaque values."],
    ["<b>Focused</b>", "One reason to fail.",
     "Twenty assertions, so the first failure hides the rest."]],
   [0.18, 0.38, 0.44]),
  ("callout", "A flaky test is worse than no test",
   ["A test that fails intermittently trains everyone to re-run the build "
    "rather than investigate. Once that reflex is established, it applies to "
    "<i>every</i> failure, including real ones.",
    "So one flaky test does not degrade the suite by one test's worth. It "
    "degrades trust in the whole suite, and a suite nobody trusts provides no "
    "confidence to change anything — which was the entire point.",
    "<b>The usual causes</b> are real time, real randomness, dependence on "
    "test execution order, shared mutable state, real network calls, and "
    "assumptions about timing in concurrent code.",
    "<b>The response is to fix it or delete it, now.</b> Quarantining flaky "
    "tests 'temporarily' is how suites die: the quarantine grows, nobody "
    "revisits it, and eventually most of the suite is not running."]),

  ("h1", "4 &nbsp; TDD, assessed honestly"),
  ("p", "Test-driven development is usually presented as settled best "
        "practice. The evidence is weaker than the advocacy, and saying so is "
        "more useful than repeating the doctrine."),
  ("table", ["Claim", "Support"],
   [["Writing tests improves outcomes.", "<b>Well supported.</b>"],
    ["Writing a failing test before fixing a bug is valuable.",
     "<b>Well supported</b>, and nearly free."],
    ["Designing for testability improves design.",
     "<b>Well supported.</b> Code that is hard to test in isolation is "
     "usually too coupled."],
    ["Writing tests <i>first</i>, specifically, produces better code than "
     "writing them shortly after.",
     "<b>Not well supported.</b> Studies conflict; effects, where found, are "
     "small and confounded with simply writing more tests."],
    ["Strict red-green-refactor measurably reduces defect rates.",
     "<b>Not well supported.</b>"]],
   [0.54, 0.46]),
  ("callout", "A defensible position",
   ["<b>Always write a failing test before fixing a bug.</b> It proves the "
    "bug is real and reproducible, proves the fix works, and leaves a "
    "regression test behind. This costs almost nothing and is sensible "
    "regardless of what you think about TDD.",
    "<b>Write tests first when the interface is unclear.</b> Writing the test "
    "forces you to be the first user of the API, which exposes awkwardness "
    "before you have built anything on top of it.",
    "<b>Write tests after when the design is obvious</b> and you would rather "
    "explore in code first. This is a legitimate working style, not a moral "
    "failure.",
    "<b>Always write them.</b> The ordering is a matter of working "
    "preference; whether the tests exist is not. Treating TDD as a tool with "
    "a domain of applicability, rather than as an identity, makes it more "
    "useful."]),
 ],
 "resources": [
   ("Software Engineering at Google — Chapters 11–14 (Testing "
    "Overview, Unit Testing, Test Doubles, Larger Testing)",
    "https://abseil.io/resources/swe-book",
    "The test-size taxonomy, the argument against mock-heavy testing, and the "
    "honest discussion of what large tests are for."),
   ("MIT 6.031 — Testing",
    "https://web.mit.edu/6.031/www/",
    "Partition-based test design and systematic case selection, which this "
    "module leaves to Module 06."),
   ("Google Testing Blog — flaky tests and test sizes",
    "https://testing.googleblog.com/",
    "Practical writing from people operating very large test suites."),
   ("Fucci et al. — An External Replication on the Effects of "
    "Test-driven Development (free)",
    "https://arxiv.org/abs/1611.05994",
    "One of the more careful empirical studies of TDD. Read it before "
    "accepting strong claims in either direction."),
 ],
 "exercises": [
   "Take an untested piece of your own code and write tests for it. Record "
   "what you had to change in the code to make it testable, and what that "
   "tells you about its coupling.",
   "Measure coverage on an existing project, then write a test that raises "
   "coverage substantially while asserting nothing. Confirm the number "
   "improves.",
   "Run a mutation testing tool on the same project. Compare the mutation "
   "score against the coverage number and explain the difference.",
   "Find a brittle test in a real codebase — one that asserts on mock "
   "call sequences — and rewrite it to assert behaviour. Then perform a "
   "refactoring and confirm the new test survives while the old one would "
   "not.",
   "Deliberately introduce a flaky test using a real clock. Run the suite "
   "fifty times and record the failure rate. Then fix it by injecting the "
   "clock.",
   "Take a bug from your own history. Write the failing test first, then fix "
   "it. Record how long each step took.",
   "Classify an existing test suite by size using the constraint-based "
   "definition. Plot the distribution and compare it against the pyramid.",
 ],
 "selfcheck": [
   "What do tests primarily buy, and why is defect detection secondary?",
   "How does the size taxonomy define small, medium, and large tests?",
   "What is the pyramid's honest limitation, and what follows for end-to-end "
   "tests?",
   "Why is high coverage uninformative while low coverage is informative?",
   "Why is coverage harmful as a target?",
   "What is the difference between testing behaviour and testing "
   "implementation, and how do you recognise the latter?",
   "Why is a flaky test worse than no test at all?",
   "Which claims about TDD are well supported and which are not?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Test Design",
 "subtitle": "Choosing which cases to write.",
 "question": "You cannot test everything. What do you test?",
 "outcomes": [
     "Use equivalence partitioning and boundary analysis.",
     "Write property-based tests and choose good properties.",
     "Use test doubles appropriately and know their costs.",
     "Test error paths and concurrency deliberately.",
     "Write characterisation tests for code you do not understand.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Choosing cases",
   "blurb": "The input space is infinite. Partition it."},

  {"t": "bullets", "kicker": "Partitioning", "title": "Equivalence classes",
   "items": [
     "Divide the input space into classes where you believe the code behaves "
     "<b>the same way</b> across the class.",
     "",
     "Test one value from each class. Testing a second adds little.",
     "",
     "For <code>withdraw(balance, amount)</code>:",
     ("amount &lt; 0 · amount = 0 · 0 &lt; amount &lt; balance "
      "· amount = balance · amount &gt; balance", 1),
     "",
     "Five tests cover the meaningful space far better than five hundred "
     "random values.",
   ],
   "note": "Partitioning is a hypothesis about the implementation, which is "
           "why it works and why it can miss."},

  {"t": "callout", "title": "Bugs live at boundaries",
   "kind": "Where to concentrate",
   "body": ["Off-by-one errors, wrong comparison operators, and overflow all "
            "occur at the <i>edges</i> of equivalence classes, not in the "
            "middle.",
            "So for every boundary, test <b>just below, exactly at, and just "
            "above</b>.",
            "Empty collection, one element, many. Zero, one, maximum. "
            "<code>INT_MAX</code> and <code>INT_MIN</code>. Empty string, one "
            "character, maximum length.",
            "<b>Boundary values are where to spend your test budget.</b> A "
            "value in the middle of a class rarely finds anything a "
            "boundary value would not."]},

  {"t": "section", "label": "Part 2", "title": "Property-based testing",
   "blurb": "State a property; let the machine find the counterexample."},

  {"t": "code", "kicker": "Properties", "title": "Testing a claim rather than a case",
   "lang": "python", "code": """
# EXAMPLE-BASED: three cases you thought of
def test_sort():
    assert sort([3,1,2]) == [1,2,3]
    assert sort([]) == []
    assert sort([1]) == [1]

# PROPERTY-BASED: a claim about ALL inputs
@given(lists(integers()))
def test_sort_is_ordered(xs):
    result = sort(xs)
    assert all(result[i] <= result[i+1] for i in range(len(result)-1))

@given(lists(integers()))
def test_sort_is_a_permutation(xs):
    assert Counter(sort(xs)) == Counter(xs)   # catches "return []"

# The framework generates hundreds of cases, including the
# nasty ones you would not have thought of -- and SHRINKS any
# failure to a minimal counterexample.
""",
   "caption": "The second property is essential. Without it, "
              "<code>return []</code> passes the first test.",
   "note": "Shrinking is the feature that makes property testing practical "
           "— a 200-element failure becomes a 2-element one."},

  {"t": "bullets", "kicker": "Properties", "title": "Properties worth looking for",
   "items": [
     "<b>Round trip:</b> <code>decode(encode(x)) == x</code>. The single most "
     "productive property.",
     "",
     "<b>Invariant:</b> something true of every output — sorted, "
     "balanced, non-negative.",
     "",
     "<b>Idempotence:</b> <code>f(f(x)) == f(x)</code>. True of normalise, "
     "sort, absolute value.",
     "",
     "<b>Oracle:</b> compare against a slow obviously-correct implementation.",
     "",
     "<b>Metamorphic:</b> a known relation between outputs — "
     "<code>sort(xs + ys)</code> contains everything in both.",
   ],
   "footnote": "Round-trip properties find serialisation bugs that examples "
               "almost never do."},

  {"t": "section", "label": "Part 3", "title": "Test doubles",
   "blurb": "Five kinds, routinely confused, with different costs."},

  {"t": "table", "kicker": "Doubles", "title": "The five kinds",
   "header": ["Kind", "Does", "Use when"],
   "widths": [2.4, 4.6, 5.1],
   "rows": [
     ["Dummy", "Fills a parameter; never used", "The argument is irrelevant"],
     ["Stub", "Returns canned answers", "You need a specific input"],
     ["Spy", "Records calls for later inspection", "The call itself is the effect"],
     ["Mock", "Asserts on calls made", "<b>Use sparingly</b>"],
     ["Fake", "A real working lightweight version", "<b>Usually best</b>"],
   ],
   "note": "The fake-over-mock recommendation is the practical content of "
           "the slide."},

  {"t": "callout", "title": "Prefer fakes to mocks",
   "kind": "The recommendation",
   "body": ["A <b>mock</b> asserts that specific calls were made — so "
            "the test is coupled to the implementation (Module 05), and it "
            "encodes your <i>belief</i> about how the dependency behaves, "
            "which may be wrong.",
            "A <b>fake</b> is a real, working, simplified implementation "
            "— an in-memory database, a map-backed repository. Tests "
            "using it exercise real behaviour and survive refactoring.",
            "<b>Best of all: use the real thing</b> when it is fast enough. "
            "An in-memory SQLite is a real database.",
            "The quality of a fake matters: a fake whose behaviour diverges "
            "from the real implementation gives false confidence. Ideally the "
            "fake is maintained by whoever owns the real one."]},

  {"t": "section", "label": "Part 4", "title": "Hard cases",
   "blurb": "Error paths, concurrency, and legacy code."},

  {"t": "bullets", "kicker": "Error paths", "title": "The least-tested, most-dangerous code",
   "items": [
     "Error handling is the code most likely to be wrong, because it is the "
     "code least often executed.",
     "",
     "<b>And it runs when things are already going badly.</b>",
     "",
     "<b>Force the errors:</b> inject failures, fill the disk, drop the "
     "network, exhaust memory, return malformed responses.",
     "",
     "<b>Fault injection</b> and chaos engineering are this idea applied to "
     "systems.",
     "",
     "A retry path that has never executed is a retry path that does not "
     "work.",
   ],
   "note": "The 'never executed therefore does not work' framing is blunt and "
           "accurate."},

  {"t": "callout", "title": "Concurrency cannot be tested into correctness",
   "kind": "Be honest about this",
   "body": ["A race condition requires a specific interleaving. Running the "
            "test a thousand times may never produce it, and then production "
            "does on the first day (CSCE 611 Module 04).",
            "<b>So testing is necessary and not sufficient.</b>",
            "<b>Use:</b> ThreadSanitizer, which reasons about happens-before "
            "rather than observed outcomes; stress tests with randomised "
            "scheduling; deterministic simulation that controls the "
            "interleaving.",
            "<b>And above all, reduce sharing.</b> Code with no shared "
            "mutable state has no races to find."]},

  {"t": "bullets", "kicker": "Legacy", "title": "Characterisation tests",
   "items": [
     "You must change code you do not understand and that has no tests. The "
     "usual situation.",
     "",
     "<b>Characterisation test:</b> write tests that capture what it "
     "<i>currently</i> does — not what it should do.",
     ("Run it, record the output, assert that output.", 1),
     "",
     "These are not correctness tests. They are a <b>safety net</b>: they "
     "tell you when you changed behaviour.",
     "",
     "Then refactor with confidence, and fix the bugs you find afterwards "
     "— deliberately, one at a time.",
   ],
   "footnote": "Feathers's technique, and the only workable approach to "
               "untested legacy code."},
 ],
 "takeaways": [
   "Partition the input space into equivalence classes and test one value "
   "from each. A second value from the same class adds little.",
   "Bugs cluster at boundaries. Test just below, at, and just above every "
   "edge — that is where the budget belongs.",
   "Property-based tests state a claim about all inputs; the framework finds "
   "and shrinks counterexamples you would not have thought of.",
   "Round trip, invariant, idempotence, oracle, metamorphic — five "
   "property patterns that cover most situations.",
   "Prefer fakes to mocks: a fake exercises real behaviour and survives "
   "refactoring, a mock encodes your beliefs about a dependency.",
   "Error paths are the least-executed and most-dangerous code. Force the "
   "failures; a retry path that never ran does not work.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Choosing cases"),
  ("p", "The input space of any non-trivial function is effectively infinite. "
        "Test design is the problem of choosing a small finite subset that "
        "finds most of the bugs."),
  ("h2", "1.1 &nbsp; Equivalence partitioning"),
  ("p", "Divide the input space into classes within which you expect the code "
        "to take the same path and behave the same way. Test one "
        "representative from each; a second representative from the same "
        "class exercises the same logic and adds little."),
  ("code", """withdraw(balance, amount):

    amount < 0                  -- invalid
    amount == 0                 -- boundary, possibly special
    0 < amount < balance        -- the ordinary case
    amount == balance           -- boundary, empties the account
    amount > balance            -- insufficient funds"""),
  ("p", "Five well-chosen tests cover the meaningful behaviour far better "
        "than five hundred random values, all but a handful of which land in "
        "the same class. Note that partitioning is a <b>hypothesis about the "
        "implementation</b> — which is why it is effective and why it "
        "can miss a class you did not anticipate."),
  ("callout", "Bugs cluster at boundaries",
   ["Off-by-one errors, incorrect comparison operators ( &lt; instead of "
    "&le; ), overflow, and empty-case handling all occur at the <i>edges</i> "
    "of equivalence classes rather than in their interiors.",
    "So for every boundary, test three values: just below, exactly at, and "
    "just above.",
    "The standard boundaries are worth memorising: empty collection, single "
    "element, many elements; zero, one, maximum; <code>INT_MAX</code> and "
    "<code>INT_MIN</code>; empty string, one character, maximum length; "
    "first element, last element; null or absent.",
    "<b>This is where to concentrate the test budget.</b> A value drawn from "
    "the middle of a class almost never finds a defect that the class's "
    "boundary values would not have found."]),

  ("h1", "2 &nbsp; Property-based testing"),
  ("p", "Example-based tests check the cases you thought of. Property-based "
        "tests state a claim that should hold for <i>all</i> inputs, and let "
        "a framework search for counterexamples."),
  ("code", """@given(lists(integers()))
def test_sort_is_ordered(xs):
    r = sort(xs)
    assert all(r[i] <= r[i+1] for i in range(len(r) - 1))

@given(lists(integers()))
def test_sort_is_a_permutation(xs):
    assert Counter(sort(xs)) == Counter(xs)"""),
  ("p", "The second property is not optional: without it, an implementation "
        "that simply returns the empty list satisfies the first. Properties "
        "usually come in pairs — one constraining the output's shape, "
        "one constraining its relationship to the input."),
  ("callout", "Shrinking is what makes this practical",
   ["When a property fails, the framework does not report the 200-element "
    "random list that triggered it. It automatically <b>shrinks</b> the "
    "counterexample, repeatedly simplifying while the failure persists, and "
    "reports something minimal — often two or three elements.",
    "A minimal counterexample is usually diagnostic on sight: "
    "<code>[0, -0.0]</code> or <code>['', ' ']</code> tells you immediately "
    "what you forgot.",
    "Without shrinking, property testing would produce failures too large to "
    "interpret. With it, the framework finds the edge case <i>and</i> "
    "explains it."]),
  ("table", ["Property pattern", "Form", "Finds"],
   [["<b>Round trip</b>", "<code>decode(encode(x)) == x</code>",
     "Serialisation, parsing, and encoding bugs. The single most productive "
     "pattern — these bugs are almost invisible to example tests."],
    ["<b>Invariant</b>", "Something true of every output.",
     "Output sorted, tree balanced, total non-negative, sum preserved."],
    ["<b>Idempotence</b>", "<code>f(f(x)) == f(x)</code>",
     "Normalisation, sorting, absolute value, deduplication, "
     "<code>abs</code>, <code>set</code>."],
    ["<b>Oracle</b>", "Compare against a slow, obviously-correct "
     "implementation.",
     "Optimised code. Test the fast version against the naive one on random "
     "inputs."],
    ["<b>Metamorphic</b>", "A known relation between two outputs.",
     "<code>sort(xs + ys)</code> contains exactly the elements of both; "
     "<code>f(2x) == 2f(x)</code> for a linear function."]],
   [0.17, 0.33, 0.50]),

  ("break",),
  ("h1", "3 &nbsp; Test doubles"),
  ("table", ["Kind", "Behaviour", "Appropriate when"],
   [["<b>Dummy</b>", "Satisfies a parameter; never actually used.",
     "The argument is irrelevant to the behaviour under test."],
    ["<b>Stub</b>", "Returns pre-arranged answers.",
     "You need the dependency to produce a particular input."],
    ["<b>Spy</b>", "A stub that records the calls it received, for later "
     "inspection.",
     "The call itself is the observable effect — 'did it send the "
     "email?'"],
    ["<b>Mock</b>", "Pre-programmed with expectations; fails if they are not "
     "met.",
     "<b>Sparingly.</b> See below."],
    ["<b>Fake</b>", "A genuine, working, simplified implementation.",
     "<b>Usually the best choice.</b> An in-memory repository, a map-backed "
     "cache."]],
   [0.14, 0.40, 0.46]),
  ("callout", "Prefer fakes to mocks",
   ["A <b>mock</b> asserts that particular calls were made with particular "
    "arguments. That couples the test to the implementation (Module 05), so "
    "refactoring breaks it. Worse, the mock encodes <i>your belief</i> about "
    "how the dependency behaves, and if that belief is wrong, the test passes "
    "while the system is broken.",
    "A <b>fake</b> is a working implementation with simplified internals "
    "— an in-memory version of a repository, a simple in-process queue. "
    "Tests against it exercise real behaviour, are readable, and survive "
    "restructuring.",
    "<b>Better still, use the real thing</b> where it is fast enough. An "
    "in-memory SQLite database is a real SQL database and runs in "
    "milliseconds. The best test double is often no double.",
    "<b>One caveat:</b> a fake whose behaviour diverges from the real "
    "implementation provides false confidence. Ideally the fake is written "
    "and maintained by whoever owns the real implementation, and is covered "
    "by a shared contract test suite that both must pass."]),

  ("h1", "4 &nbsp; The hard cases"),
  ("h2", "4.1 &nbsp; Error paths"),
  ("callout", "The least-executed code is the most dangerous",
   ["Error handling is simultaneously the code most likely to contain "
    "defects — because it is rarely executed and rarely reviewed with "
    "care — and the code that runs precisely when the system is already "
    "in trouble.",
    "A retry path that has never been executed is a retry path that does not "
    "work. A fallback that has never been exercised will fail on the day it "
    "is needed, and will do so while the primary path is also failing.",
    "<b>So force the errors.</b> Inject failures at dependency boundaries, "
    "fill the disk, sever the network, exhaust the connection pool, return "
    "malformed and truncated responses, return success after a timeout has "
    "already fired.",
    "<b>Fault injection</b> at the unit level and <b>chaos engineering</b> at "
    "the system level are the same idea at different scales: make the "
    "failure happen when you are watching, rather than at three in the "
    "morning."]),
  ("h2", "4.2 &nbsp; Concurrency"),
  ("callout", "Testing cannot establish concurrent correctness",
   ["A race condition manifests only under a particular interleaving. "
    "Running a test ten thousand times may never produce that interleaving, "
    "and production may produce it within an hour (CSCE 611 Module 04).",
    "Testing is therefore necessary and <b>not sufficient</b> for concurrent "
    "code, and this should be stated plainly rather than papered over.",
    "<b>What helps:</b> ThreadSanitizer and similar tools, which reason about "
    "happens-before relationships rather than observed outcomes and therefore "
    "find races on executions where nothing went wrong; stress testing with "
    "randomised scheduling and injected delays; deterministic simulation, "
    "where the test controls the interleaving explicitly and can replay a "
    "failure.",
    "<b>What helps most is reducing sharing.</b> Code with no shared mutable "
    "state has no races to find, and that is a design decision rather than a "
    "testing one."]),
  ("h2", "4.3 &nbsp; Characterisation tests"),
  ("p", "The common situation: you must modify code that has no tests, that "
        "you did not write, and whose correct behaviour nobody can state."),
  ("ol", ["Write tests that capture what the code <b>currently does</b> "
          "— not what it should do. Run it, observe the output, assert "
          "that output.",
          "Where the output is complex, assert on a serialisation or a hash "
          "of it.",
          "Build up enough of these to cover the paths your change will "
          "touch.",
          "Now refactor. The characterisation tests tell you when behaviour "
          "changed.",
          "<b>Afterwards</b>, examine the captured behaviour for bugs — "
          "there will be some — and fix them deliberately, one at a "
          "time, updating the corresponding test with a comment explaining "
          "why the expected value changed."]),
  ("p", "These are explicitly not correctness tests. They are a safety net "
        "that converts 'I hope I did not break anything' into 'I know exactly "
        "what I changed'. Michael Feathers's <i>Working Effectively with "
        "Legacy Code</i> develops the technique, and it is the only workable "
        "approach to untested code that must be changed."),
 ],
 "resources": [
   ("MIT 6.031 — Testing (partitioning and boundary analysis)",
    "https://web.mit.edu/6.031/www/",
    "The most systematic free treatment of choosing test cases."),
   ("Hypothesis documentation — 'What is property-based testing?'",
    "https://hypothesis.readthedocs.io/",
    "Excellent explanation plus a usable library. The equivalents in other "
    "languages (QuickCheck, fast-check, proptest) share the ideas."),
   ("Martin Fowler — Mocks Aren't Stubs",
    "https://martinfowler.com/articles/mocksArentStubs.html",
    "The taxonomy of doubles and the argument about classical versus "
    "mockist testing. Still the clearest statement of both positions."),
   ("Michael Feathers — Working Effectively with Legacy Code",
    "https://www.oreilly.com/library/view/working-effectively-with/0131177052/",
    "Characterisation tests and seam-finding. The standard reference for "
    "testing code that was not designed to be tested."),
 ],
 "exercises": [
   "Take a function with at least three parameters and derive its equivalence "
   "classes. Write one test per class, then add boundary tests. Compare the "
   "defect-finding power against twenty random inputs.",
   "Write property-based tests for a sorting function, including both the "
   "ordering and the permutation property. Then deliberately implement "
   "<code>sort</code> as <code>return []</code> and confirm which property "
   "catches it.",
   "Find a round-trip property in your own code — serialisation, "
   "parsing, encoding — and test it with generated inputs. Report "
   "whatever it finds.",
   "Write an oracle test: implement something the slow obvious way and the "
   "fast way, and compare them on random inputs.",
   "Replace a mock-heavy test with one using a fake. Then refactor the code "
   "under test and confirm the fake-based test survives while the mock-based "
   "one would not.",
   "Write a fault-injection test for an error path in your code that has "
   "never been executed. Report what you found.",
   "Take an undocumented function you did not write and build a "
   "characterisation test suite for it. Then refactor it and report whether "
   "any test caught a behaviour change.",
 ],
 "selfcheck": [
   "What is equivalence partitioning, and why does a second value from the "
   "same class add little?",
   "Why do bugs cluster at boundaries, and which three values do you test for "
   "each?",
   "What does a property-based test assert that an example-based test does "
   "not, and why is shrinking essential?",
   "Name five property patterns and give an example of each.",
   "Distinguish a mock from a fake, and give two reasons to prefer the fake.",
   "Why are error paths both the most dangerous and the least tested code?",
   "Why can testing not establish the correctness of concurrent code, and "
   "what helps instead?",
   "What is a characterisation test and what is it for?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Refactoring and Technical Debt",
 "subtitle": "Changing structure without changing behaviour, and deciding "
             "when to.",
 "question": "When is cleaning up code worth the time?",
 "outcomes": [
     "Define refactoring precisely and work in safe steps.",
     "Recognise common code smells and their corresponding refactorings.",
     "Treat technical debt as a financial decision, including deliberate "
     "debt.",
     "Decide when to refactor and when to leave it.",
     "Explain why rewrites usually fail.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The definition",
   "blurb": "Precise, and the precision matters."},

  {"t": "callout", "title": "Refactoring changes structure, not behaviour",
   "kind": "The definition",
   "body": ["<b>A refactoring is a change to the internal structure of code "
            "that does not change its observable behaviour.</b>",
            "If behaviour changes, it is not a refactoring — it is a "
            "change, and it needs testing as one.",
            "The precision matters because it licenses the technique: since "
            "behaviour is unchanged, a test suite that passed before must "
            "pass after. That is what makes the step <i>safe</i>.",
            "<b>Never refactor and change behaviour in the same commit.</b> "
            "When something breaks, you will not know which caused it."]},

  {"t": "bullets", "kicker": "Method", "title": "Small steps, tests between",
   "items": [
     "<b>1. Ensure tests exist</b> and pass. Characterisation tests if "
     "necessary (Module 06).",
     "",
     "<b>2. Make one small change.</b> Extract a function. Rename a variable.",
     "",
     "<b>3. Run the tests.</b> If they fail, undo — do not debug.",
     "",
     "<b>4. Commit.</b> Repeat.",
     "",
     "The discipline is the small steps. A large refactoring that breaks is "
     "unbisectable; fifty small ones are each trivially revertible.",
   ],
   "note": "'Undo, do not debug' is the hardest habit to instil and the most "
           "valuable."},

  {"t": "table", "kicker": "Smells", "title": "Smells and their refactorings",
   "header": ["Smell", "Means", "Refactoring"],
   "widths": [2.8, 4.4, 4.9],
   "rows": [
     ["Long function", "Several responsibilities", "Extract function"],
     ["Long parameter list", "Hidden structure", "Introduce parameter object"],
     ["Duplicated knowledge", "One fact in two places", "Extract and call"],
     ["Feature envy", "A method uses another class more than its own", "Move method"],
     ["Shotgun surgery", "<b>One change touches many files</b>", "A missing module (Mod 03)"],
     ["Primitive obsession", "Strings and ints for domain concepts", "Introduce a type"],
   ],
   "note": "A smell is a hypothesis, not a verdict — worth saying so."},

  {"t": "callout", "title": "A smell is a hypothesis, not a defect",
   "kind": "Judgement required",
   "body": ["A long function is <i>often</i> doing several things. "
            "Sometimes it is one long sequential process that is clearer "
            "written out than split into twelve one-line functions.",
            "A long parameter list is often hiding a missing type. Sometimes "
            "the function genuinely needs seven independent values.",
            "<b>Smells indicate where to look, not what to do.</b> Treating "
            "them as rules produces codebases that satisfy a linter and are "
            "harder to read.",
            "The test is always Module 01's: does this change reduce the cost "
            "of the next change?"]},

  {"t": "section", "label": "Part 2", "title": "Technical debt",
   "blurb": "A financial metaphor, and it is more precise than people "
            "realise."},

  {"t": "bullets", "kicker": "The metaphor", "title": "Ward Cunningham's original point",
   "items": [
     "Shipping imperfect code to learn sooner is like <b>borrowing</b>: you "
     "get value now and pay interest later.",
     "",
     "<b>Interest</b> = the extra cost of every future change made harder by "
     "the shortcut.",
     "",
     "<b>Principal</b> = the cost of fixing it properly.",
     "",
     "<b>Borrowing can be correct.</b> Shipping six months earlier may be "
     "worth years of interest.",
     "",
     "What is not correct is borrowing <i>without noticing</i>, and never "
     "checking the balance.",
   ],
   "note": "The original metaphor was about deliberate learning debt, not "
           "about sloppy code — worth correcting."},

  {"t": "table", "kicker": "Kinds", "title": "Four kinds of debt",
   "header": ["", "Deliberate", "Inadvertent"],
   "widths": [2.6, 4.8, 4.7],
   "rows": [
     ["Prudent", "'Ship now, fix after launch' — <b>fine</b>", "'Now we know how we should have done it'"],
     ["Reckless", "'No time for design' — <b>bad</b>", "'What's a module?' — ignorance"],
   ],
   "footnote": "Fowler's quadrant. Only the prudent-deliberate cell is a "
               "decision; the others are things that happened.",
   "note": "The quadrant usefully separates 'we chose this' from 'this "
           "happened to us'."},

  {"t": "callout", "title": "Debt you did not record is debt you will not repay",
   "kind": "The practical discipline",
   "body": ["Deliberate debt is a legitimate engineering decision. "
            "<b>Undocumented</b> deliberate debt is indistinguishable from "
            "incompetence six months later.",
            "So: when you take a shortcut deliberately, write down what you "
            "did, why, and what it will cost. A comment, an issue, an ADR.",
            "Then it can be reviewed, prioritised against other work, and "
            "repaid when the interest justifies it.",
            "<b>Without that record</b>, nobody knows whether the odd code is "
            "a deliberate trade or a mistake — so nobody dares change "
            "it, and the interest compounds forever."]},

  {"t": "section", "label": "Part 3", "title": "When to refactor",
   "blurb": "Not on a schedule."},

  {"t": "bullets", "kicker": "When", "title": "Good and bad times",
   "items": [
     "<b>Do:</b> immediately before changing code — make the change "
     "easy, then make the easy change.",
     "<b>Do:</b> immediately after, while you still understand it.",
     "<b>Do:</b> when the same awkwardness has cost you three times.",
     "",
     "<b>Do not:</b> on a 'cleanup sprint' with no specific change in view. "
     "You will refactor toward imagined requirements.",
     "<b>Do not:</b> code you are not going to change. Ugly stable code costs "
     "nothing.",
     "<b>Do not:</b> to satisfy a style preference.",
   ],
   "footnote": "'Make the change easy, then make the easy change' — "
               "Kent Beck."},

  {"t": "callout", "title": "Ugly code that nobody touches costs nothing",
   "kind": "The underrated judgement",
   "body": ["Technical debt accrues interest only on code that is "
            "<i>changed</i>. A module nobody has modified in four years is "
            "paying no interest, however unpleasant it looks.",
            "So prioritise refactoring by <b>change frequency</b>, not by "
            "ugliness. Version control history tells you which files change "
            "most, and that is where cleanup pays.",
            "The intersection of 'changes often' and 'is hard to change' is "
            "where all the value is. Everything else is aesthetics.",
            "This is also why 'the whole codebase needs cleaning up' is "
            "almost never the right plan."]},

  {"t": "section", "label": "Part 4", "title": "Rewrites",
   "blurb": "The most expensive mistake available."},

  {"t": "bullets", "kicker": "Rewrites", "title": "Why they usually fail",
   "items": [
     "<b>The old code encodes knowledge you have lost.</b> Every strange "
     "branch is a bug someone fixed.",
     "",
     "<b>You will reintroduce fixed bugs</b> — all of them, "
     "individually, over years.",
     "",
     "<b>You must hit a moving target:</b> the old system keeps changing "
     "while you rebuild.",
     "",
     "<b>No value until it is finished</b> — and the schedule will "
     "slip.",
     "",
     "<b>Alternative: strangler fig.</b> Build the new system around the old, "
     "divert traffic piece by piece, delete as you go.",
   ],
   "note": "Joel Spolsky's essay is the canonical statement and is worth "
           "assigning."},
 ],
 "takeaways": [
   "A refactoring changes structure without changing behaviour. That "
   "precision is what makes the existing test suite a safety net.",
   "Work in small steps, run tests between each, and undo rather than debug "
   "when they fail.",
   "A code smell is a hypothesis about where to look, not a rule about what "
   "to do.",
   "Technical debt is a real financial metaphor: deliberate prudent debt is a "
   "legitimate decision; undocumented debt will never be repaid.",
   "Refactor immediately before or after changing code, not on a cleanup "
   "schedule. Ugly stable code costs nothing.",
   "Prioritise by change frequency, not by ugliness. Version control history "
   "tells you where the interest is actually accruing.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What refactoring is"),
  ("callout", "The definition, and why precision matters",
   ["<b>A refactoring is a change to the internal structure of software that "
    "makes it easier to understand and cheaper to modify, without changing "
    "its observable behaviour.</b>",
    "If the observable behaviour changes, it is not a refactoring. It is a "
    "change, and it requires the testing and review that any behavioural "
    "change requires.",
    "The precision licenses the entire technique: because behaviour is "
    "unchanged by definition, a test suite that passed before the refactoring "
    "must pass after it. The tests become a mechanical check on the "
    "transformation.",
    "<b>Never combine a refactoring with a behavioural change in one "
    "commit.</b> When something breaks — and it will — you need to "
    "know which of the two caused it, and a mixed commit makes that "
    "impossible. It also makes review far harder: a reviewer can skim a pure "
    "rename and must read a behavioural change carefully."]),
  ("h2", "1.1 &nbsp; The method"),
  ("ol", ["<b>Ensure tests exist and pass.</b> If there are none, write "
          "characterisation tests first (Module 06).",
          "<b>Make one small change.</b> Extract a function. Rename a "
          "variable. Move a method. One transformation.",
          "<b>Run the tests.</b> If they fail, <b>undo</b> — do not "
          "debug. The step was too large or the transformation was wrong; "
          "either way, returning to a known-good state costs seconds and "
          "debugging costs hours.",
          "<b>Commit.</b> Then repeat."]),
  ("p", "The discipline is in the step size. A large refactoring that breaks "
        "leaves you with a working state and a broken state and no way to "
        "bisect between them. Fifty small refactorings leave fifty "
        "checkpoints, each trivially revertible, and <code>git bisect</code> "
        "will find the problem in six steps."),
  ("h2", "1.2 &nbsp; Smells"),
  ("table", ["Smell", "What it suggests", "Usual refactoring"],
   [["<b>Long function</b>", "Several responsibilities in one place.",
     "Extract function. Each extracted piece gets a name, which is most of "
     "the benefit."],
    ["<b>Long parameter list</b>", "A missing type — several parameters "
     "that always travel together.", "Introduce parameter object."],
    ["<b>Duplicated knowledge</b>", "One fact represented in two places "
     "(Module 03's DRY test).", "Extract and call."],
    ["<b>Feature envy</b>", "A method uses another class's data more than its "
     "own.", "Move method to where the data is."],
    ["<b>Shotgun surgery</b>", "<b>One conceptual change requires edits in "
     "many files.</b>",
     "A module is missing. This is Module 03's strongest signal."],
    ["<b>Primitive obsession</b>", "Domain concepts represented as strings "
     "and integers.",
     "Introduce a type. <code>EmailAddress</code> rather than "
     "<code>str</code> makes a class of bugs impossible."]],
   [0.20, 0.37, 0.43]),
  ("callout", "A smell is a hypothesis",
   ["A long function is often doing several things. It is sometimes a single "
    "sequential process that reads more clearly written out than split into "
    "twelve single-line functions, each of which must be located and read.",
    "A long parameter list often conceals a missing type. It sometimes "
    "reflects a function that genuinely requires seven independent values.",
    "<b>Smells tell you where to look, not what to do.</b> Treated as rules "
    "and enforced by tooling, they produce codebases that satisfy a linter "
    "and are harder to read than what they replaced — which is a real "
    "and common failure.",
    "The test is always Module 01's: <i>does this change reduce the cost of "
    "the next change?</i> If the answer is 'it satisfies a guideline', the "
    "answer is no."]),

  ("h1", "2 &nbsp; Technical debt"),
  ("p", "Ward Cunningham's metaphor is more precise than its common use "
        "suggests, and the original formulation is worth recovering."),
  ("callout", "The original argument",
   ["Shipping code that does not yet fully reflect your understanding of the "
    "problem is like <b>borrowing money</b>: you obtain value now — you "
    "ship, you learn from users — and you pay interest later in the form "
    "of harder changes.",
    "<b>Interest</b> is the additional cost imposed on every subsequent "
    "change by the shortcut. <b>Principal</b> is the cost of fixing it "
    "properly.",
    "<b>Borrowing is frequently correct.</b> Shipping six months earlier may "
    "be worth years of interest, particularly when shipping is how you "
    "discover whether the product should exist.",
    "Cunningham's point was specifically about <i>learning</i>: you write "
    "code reflecting your current understanding, that understanding improves, "
    "and the gap between the code and your improved understanding is the "
    "debt. It was never a licence for sloppiness, and it is frequently "
    "misquoted as one."]),
  ("table", ["", "Deliberate", "Inadvertent"],
   [["<b>Prudent</b>", "'We must ship now; we will fix this after launch.' "
     "<b>A legitimate decision</b>, provided it is recorded.",
     "'Now that it is built, we understand how it should have been done.' "
     "Unavoidable and healthy — this is Cunningham's original case."],
    ["<b>Reckless</b>", "'We do not have time for design.' A decision, and a "
     "bad one.",
     "'What is a module?' Debt incurred through ignorance, which is the only "
     "quadrant that is simply a problem."]],
   [0.14, 0.43, 0.43]),
  ("callout", "Record the debt or it will never be repaid",
   ["Deliberate prudent debt is good engineering. <b>Undocumented</b> "
    "deliberate debt is indistinguishable, six months later, from "
    "incompetence.",
    "When you take a shortcut knowingly, write down what you did, why, and "
    "what it will cost — a comment, an issue, an ADR. The form matters "
    "less than the existence.",
    "With that record, the debt can be reviewed, prioritised against feature "
    "work, and repaid when the accumulated interest justifies it. It becomes "
    "a managed liability.",
    "Without it, a future maintainer encountering the odd code cannot tell "
    "whether it is a deliberate trade-off or a mistake — so they will "
    "work around it rather than fix it, and the interest compounds "
    "indefinitely."]),

  ("break",),
  ("h1", "3 &nbsp; When to refactor"),
  ("table", ["Refactor", "Do not refactor"],
   [["<b>Immediately before changing code.</b> 'Make the change easy, then "
     "make the easy change' (Kent Beck). The restructuring is justified by a "
     "change you are definitely making.",
     "<b>On a scheduled cleanup sprint</b> with no specific change in view. "
     "You will restructure toward imagined future requirements, which is "
     "speculation, and speculation about requirements is usually wrong."],
    ["<b>Immediately after changing code</b>, while you still understand it "
     "and the context is loaded.",
     "<b>Code you are not going to change.</b> Ugly, stable, working code "
     "accrues no interest."],
    ["<b>When the same awkwardness has cost you three times.</b> Three is "
     "evidence; once is noise.",
     "<b>To satisfy a style preference</b> or to make a linter quieter."],
    ["<b>When a bug's root cause is structural</b> — fixing the "
     "structure prevents the next three bugs.",
     "<b>Across a whole codebase at once.</b> Large refactorings are "
     "unreviewable and conflict with everything in flight."]],
   [0.5, 0.5]),
  ("callout", "Prioritise by change frequency, not by ugliness",
   ["Technical debt accrues interest only on code that is actually modified. "
    "A module untouched for four years is paying no interest whatever it "
    "looks like, and refactoring it is pure cost.",
    "Version control history tells you exactly where the interest is: which "
    "files change most often, and which changes take longest. That data is "
    "free and nobody looks at it.",
    "<b>The intersection of 'changes frequently' and 'is hard to change' is "
    "where all the value is.</b> Everything outside that intersection is "
    "aesthetics with a cost attached.",
    "This is also why 'the whole codebase needs cleaning up' is almost never "
    "the right plan, and why it almost never gets approved — correctly."]),

  ("h1", "4 &nbsp; Rewrites"),
  ("p", "The strongest temptation in software engineering is to declare a "
        "system beyond saving and start again. It is usually a mistake, for "
        "reasons that are specific rather than merely cautionary."),
  ("ol", ["<b>The old code encodes knowledge you no longer have.</b> Every "
          "strange conditional is, in all likelihood, a bug somebody found "
          "and fixed. The code is ugly precisely because reality is, and the "
          "accumulated special cases are the record of five years of "
          "encounters with reality.",
          "<b>You will reintroduce every one of those bugs</b>, individually, "
          "and rediscover each over the following years — this time with "
          "users watching.",
          "<b>The target moves.</b> The old system does not stop evolving "
          "while you rebuild, so you are implementing a specification that is "
          "being rewritten as you work.",
          "<b>No value is delivered until it is complete</b>, and it will "
          "take substantially longer than estimated — so there is a long "
          "period during which two systems must be maintained and nothing has "
          "improved."]),
  ("callout", "The strangler fig",
   ["Martin Fowler's alternative, named after the plant that grows around a "
    "tree and gradually replaces it.",
    "Build the new system <i>around</i> the old one. Route all traffic "
    "through a facade. Implement one capability in the new system and divert "
    "that traffic to it. Delete the corresponding old code. Repeat.",
    "Every step delivers value, every step is revertible, and the system "
    "works throughout. There is never a big-bang cutover and never a period "
    "where nothing ships.",
    "It is slower in principle and faster in practice, and it is the "
    "difference between a migration that completes and one that is abandoned "
    "two years in with both systems running."]),
 ],
 "resources": [
   ("Martin Fowler — Refactoring catalogue",
    "https://refactoring.com/catalog/",
    "Every refactoring with its mechanics. The reference to keep open while "
    "working."),
   ("Fowler — Technical Debt Quadrant",
    "https://martinfowler.com/bliki/TechnicalDebtQuadrant.html",
    "The deliberate/inadvertent and prudent/reckless distinction of "
    "&sect;2."),
   ("Ward Cunningham — Debt Metaphor (free video)",
    "https://www.youtube.com/watch?v=pqeJFYwnkjE",
    "Cunningham explaining what he actually meant, and correcting the common "
    "misuse. Five minutes."),
   ("Joel Spolsky — Things You Should Never Do, Part I",
    "https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/",
    "The canonical argument against rewrites, with the Netscape case. Twenty "
    "years old and still correct."),
 ],
 "exercises": [
   "Take a long function and extract sub-functions in small steps, running "
   "tests between each. Commit after every step. Then review the commit "
   "history and judge whether each step was independently sensible.",
   "Use version control history to find the files in a project that change "
   "most frequently. Cross-reference against the files you find hardest to "
   "read. Refactor the intersection.",
   "Find a piece of deliberate technical debt in your own code. Write the "
   "record you should have written: what, why, what it costs, what would "
   "trigger repaying it.",
   "Take a function with primitive obsession — strings and integers "
   "standing in for domain concepts — and introduce types. Count the "
   "bugs that become impossible to express.",
   "Find an instance of shotgun surgery using commit history: files "
   "consistently changed together. Propose the module that is missing.",
   "Attempt a refactoring in one large step, break something, and experience "
   "the difficulty of locating the cause. Then revert and do it in small "
   "steps.",
   "Find a system you use that was rewritten from scratch. Research what "
   "happened and write a paragraph assessing it against &sect;4's four "
   "reasons.",
 ],
 "selfcheck": [
   "Define refactoring precisely, and say why the precision licenses the "
   "technique.",
   "Why should a refactoring never be combined with a behavioural change in "
   "one commit?",
   "Why undo rather than debug when tests fail mid-refactoring?",
   "Why is a code smell a hypothesis rather than a rule?",
   "What are interest and principal in the technical debt metaphor, and when "
   "is borrowing correct?",
   "Why does undocumented deliberate debt never get repaid?",
   "Give two times to refactor and two times not to.",
   "Give three specific reasons rewrites fail, and name the alternative.",
 ],
},

]
