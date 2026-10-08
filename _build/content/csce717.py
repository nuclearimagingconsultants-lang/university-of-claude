# -*- coding: utf-8 -*-
"""CSCE 717 Algorithmic Game Theory — original course content."""

COURSE = {
    "code": "CSCE 717",
    "title": "Algorithmic Game Theory",
    "tagline": "The input has interests, so correctness must include "
               "the incentive to report honestly",
    "term": "Semester 12 (with CSCE 640 and CSCE 628)",
    "prereqs": "CSCE 629 Analysis of Algorithms; CSCE 669 "
               "Computational Optimization for linear programming and "
               "duality; CSCE 637 Complexity Theory for Module 03; "
               "CSCE 642 Deep Reinforcement Learning is useful for "
               "Module 12 and is not required",
    "deliverable": "A mechanism for a resource allocation problem you "
                   "choose — with its incentive properties proved or "
                   "its failure of them demonstrated by a concrete "
                   "manipulation, its approximation ratio stated, and "
                   "its behaviour simulated against strategic rather "
                   "than honest agents",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "description": [
        "<b>Every algorithms course before this one assumed the "
        "input was given.</b> <b>Module 01 removes that "
        "assumption</b> — <b>the input is now reported by people who "
        "want particular outputs</b> — and <b>everything that follows "
        "is about what that changes</b>, which turns out to be the "
        "definition of correctness itself.",
        "<b>The first third is the analysis side.</b> <b>Games, "
        "equilibria, and what Nash's theorem does and does not "
        "promise</b> (Module 02); <b>the complexity of actually "
        "finding an equilibrium</b> (Module 03), <b>which is hard in "
        "a precise and interesting sense</b>; and <b>the price of "
        "anarchy</b> (Modules 04 and 05) — <b>the quantitative cost "
        "of letting agents choose for themselves.</b>",
        "<b>The second third is the design side, and it is the "
        "useful one.</b> <b>Mechanism design asks what outcomes can "
        "be implemented when truthful reporting has to be in each "
        "agent's interest</b> (Module 06) — and <b>auctions are "
        "where that theory is sharpest and most deployed</b> "
        "(Modules 07 and 08), with <b>matching and fair division "
        "covering the cases where money is unavailable</b> "
        "(Modules 09 and 11).",
        "<b>The third theme is the impossibility results, which are "
        "load-bearing rather than decorative.</b> <b>Arrow and "
        "Gibbard-Satterthwaite say that no voting rule has all the "
        "properties you want</b> (Module 10) — so <b>every real "
        "system is a choice about which property to give up</b>, and "
        "knowing which is the whole of being able to evaluate one.",
        "<b>And the closing position is about claims.</b> "
        "<b>Module 13 asks what it means to say a mechanism "
        "works</b> — because <b>'incentive compatible' is a statement "
        "about a model of the agents</b>, and <b>the agents are real "
        "people who may collude, misunderstand the rules, or care "
        "about things the model does not include.</b>",
    ],
    "outcomes": [
        "Explain why strategic inputs change what correctness "
        "means.",
        "Define games and equilibria, and state Nash's theorem "
        "precisely.",
        "Explain the complexity of computing equilibria.",
        "Define and compute the price of anarchy.",
        "Analyse routing and congestion games.",
        "State the mechanism design problem and incentive "
        "compatibility.",
        "Derive the second-price auction and revenue equivalence.",
        "Explain combinatorial auctions and their approximation.",
        "Design and analyse matching mechanisms.",
        "State the social choice impossibility results and what "
        "follows.",
        "Explain fair division and its fairness notions.",
        "Explain no-regret dynamics and what they converge to.",
        "Claim that a mechanism works, honestly.",
    ],
    "materials": [
        ("Nisan, Roughgarden, Tardos & Vazirani — Algorithmic Game "
         "Theory (free PDF from the authors)",
         "https://www.cs.cmu.edu/~sandholm/cs15-892F13/algorithmic-game-theory.pdf",
         "<b>The primary text, and it is free.</b> Modules 02 through "
         "11 follow its organisation, and the chapters are by the "
         "people who proved the results."),
        ("Roughgarden — Twenty Lectures on Algorithmic Game Theory, "
         "with the free video lectures and notes",
         "http://timroughgarden.org/notes.html",
         "<b>The best entry point, free in full.</b> Modules 01, 04, "
         "06, and 07 especially — and the lectures are worth watching "
         "rather than only reading."),
        ("Shoham & Leyton-Brown — Multiagent Systems (free PDF)",
         "http://www.masfoundations.org/",
         "<b>Modules 02, 10, and 12, free.</b> Broader than the "
         "algorithmic texts, and the social choice chapters are "
         "excellent."),
        ("Krishna — Auction Theory",
         "https://www.elsevier.com/books/auction-theory/krishna/978-0-12-374507-1",
         "<b>Module 07.</b> The economics treatment, where revenue "
         "equivalence is derived properly. Library copy."),
        ("Roth — Who Gets What and Why",
         "https://www.harpercollins.com/products/who-gets-what-and-why-alvin-e-roth",
         "<b>Module 09.</b> Matching markets as actually deployed — "
         "kidney exchange, school choice, medical residencies — by "
         "the person who built several of them."),
        ("Brandt, Conitzer, Endriss, Lang & Procaccia — Handbook of "
         "Computational Social Choice (free PDF)",
         "http://procaccia.info/wp-content/uploads/2020/03/comsoc.pdf",
         "<b>Modules 10 and 11, free.</b> The impossibility results "
         "and the fair division literature, rigorously."),
    ],
    "tooling": [
        "<b>Pen and paper for the proofs</b> — <b>most of this "
        "course is theorems</b>, and <b>Modules 06 and 07's arguments "
        "have to be worked by hand</b> before any implementation is "
        "meaningful.",
        "<b>A linear programming solver</b> — <b>any of them, and "
        "the duality from CSCE 669 §05 is used directly</b> in "
        "Modules 03 and 08.",
        "<b>Python for simulation</b>, because <b>the interesting "
        "question in Project 2 is what strategic agents do to your "
        "mechanism</b>, and that is answered by simulating them rather "
        "than by assuming they are honest.",
        "<b>Gambit or a similar game solver</b> for small normal-form "
        "games — useful in Module 02 and quickly outgrown, which is "
        "itself Module 03's point.",
        "<b>And a best-response or no-regret learner</b> "
        "(Module 12) — <b>the cheapest way to find out whether your "
        "mechanism survives agents who adapt</b>, which is Project 2's "
        "requirement.",
        "<b>Plus, for Project 2, a concrete manipulation</b> — "
        "<b>a specific misreport that makes a specific agent better "
        "off</b> — because <b>'it is manipulable' is a claim that "
        "needs an exhibit</b> (Module 13 §2).",
    ],
    "projects": [
        {"n": 1, "after": 6,
         "title": "Measure the price of anarchy",
         "brief": "Build a congestion game, find its equilibria, and "
                  "measure what selfish routing costs.",
         "reqs": [
           "<b>A routing or congestion game implemented</b>, with "
           "latency functions you choose and state.",
           "<b>The social optimum computed</b> — by "
           "optimisation, exactly — and <b>the equilibrium found by "
           "best-response dynamics</b>.",
           "<b>The ratio measured across many random "
           "instances</b>, with the distribution reported rather than "
           "the worst case alone.",
           "<b>Braess's paradox reproduced</b>: <b>an added edge "
           "that makes everybody worse off</b>, constructed and "
           "verified.",
           "<b>And the theoretical bound compared</b> to what you "
           "measured — with the gap explained.",
           "<b>Plus: does best-response dynamics always "
           "converge</b> in your game, and why?",
         ],
         "done": [
           "<b>Braess's paradox constructed and verified</b> "
           "— <b>which is the deliverable that shows you understand "
           "equilibrium rather than optimisation.</b>",
           "<b>The distribution of ratios reported</b>, not only "
           "the maximum — because <b>the worst case is a bound and "
           "the typical case is the engineering "
           "question</b>.",
           "<b>The convergence question answered with a "
           "reason</b> (a potential function, or a counterexample) "
           "rather than by observation.",
           "<b>And the latency functions stated</b>, since <b>the "
           "price of anarchy bound depends on the class of functions "
           "allowed</b> (Module 04 §3), which is the result's most "
           "misquoted condition.",
         ]},
        {"n": 2, "after": 12,
         "title": "Design a mechanism, then attack it",
         "brief": "Build an allocation mechanism and find out what "
                  "strategic agents do to it.",
         "reqs": [
           "<b>An allocation problem you choose</b> — "
           "scheduling, bandwidth, course seats, shared compute — "
           "<b>with the agents, their preferences, and the designer's "
           "objective stated precisely</b>.",
           "<b>A mechanism specified</b>: allocation rule and "
           "payment rule, or an ordinal rule if money is "
           "unavailable.",
           "<b>Its incentive properties proved, or its failure "
           "demonstrated by a concrete manipulation</b> — <b>a "
           "specific agent, specific true preferences, and a specific "
           "profitable misreport.</b>",
           "<b>The efficiency or approximation ratio stated</b>, "
           "with the benchmark named.",
           "<b>Simulated against strategic agents</b> "
           "(Module 12's learners), not honest ones — <b>and the "
           "outcome compared to the honest-agent "
           "case</b>.",
           "<b>And the honest claim</b> in Module 13 §3's form, "
           "including which impossibility result your design is choosing "
           "to live with.",
         ],
         "done": [
           "<b>The manipulation concrete</b> — <b>named agent, "
           "named misreport, computed gain</b> — because <b>'it is "
           "manipulable' without an exhibit is not a "
           "finding</b> (Module 13 §2).",
           "<b>The strategic simulation run</b> and compared to "
           "the honest baseline, which is the point of the "
           "project.",
           "<b>The impossibility named</b>: <b>every mechanism "
           "gives something up</b> (Modules 06 §4, 10 §3), and saying "
           "which is what makes a design defensible.",
           "<b>And the benchmark stated</b>, because <b>an "
           "approximation ratio against an unstated optimum is not a "
           "number</b> — which is CSCE 629's discipline in a new "
           "setting.",
         ]},
    ],
    "map": [
        ("Nisan, Roughgarden, Tardos & Vazirani (free PDF)",
         "https://www.cs.cmu.edu/~sandholm/cs15-892F13/algorithmic-game-theory.pdf",
         "<b>Modules 02 to 11</b>, free in full — the standard "
         "reference, chapter by chapter."),
        ("Roughgarden's lecture notes and videos (free)",
         "http://timroughgarden.org/notes.html",
         "<b>Modules 01, 04, 06, 07, and 12.</b> The clearest available "
         "presentation, and the problem sets are good."),
        ("Shoham & Leyton-Brown (free PDF)",
         "http://www.masfoundations.org/",
         "<b>Modules 02, 10, and 12</b>, free — with the social "
         "choice material developed carefully."),
        ("Handbook of Computational Social Choice (free PDF)",
         "http://procaccia.info/wp-content/uploads/2020/03/comsoc.pdf",
         "<b>Modules 10 and 11</b>, free — including the "
         "manipulation-complexity literature."),
        ("The ACM EC proceedings (free preprints)",
         "https://dl.acm.org/conference/ec",
         "<b>Modules 08, 12, and 13.</b> The current literature, and "
         "Module 13's exercises use it."),
        ("Roth's Nobel lecture and the matching literature (free)",
         "https://www.nobelprize.org/prizes/economic-sciences/2012/roth/lecture/",
         "<b>Module 09.</b> Theory deployed, with the practical "
         "obstacles described honestly."),
    ],
}

MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "When the Input Has Interests",
 "subtitle": "What changes when the data is reported rather than "
             "given.",
 "question": "Who gave you this input, and what do they want?",
 "outcomes": [
     "Explain why strategic inputs change correctness.",
     "Give concrete examples where the shift matters.",
     "Distinguish the analysis and design questions.",
     "State the two ways out of the problem.",
     "State this course's position on mechanism claims.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The shift",
   "blurb": "Which is one assumption, and it is load-bearing."},

  {"t": "callout", "title": "Every algorithms course before this one assumed the input was given; here it is reported by somebody with a preference over your output",
   "kind": "The assumption this course removes",
   "body": ["<b>A sorting algorithm's input does not care how it is "
            "sorted</b> — <b>a bidder's valuation does care who wins "
            "the item</b>, and will be reported accordingly if that "
            "helps.",
            "<b>So an algorithm that is correct on the reported "
            "input may be useless on the true one</b> — <b>and the "
            "true input is not observable</b>, which is the whole "
            "difficulty.",
            "<b>Which means correctness has to be "
            "redefined:</b> <b>a mechanism is correct if it produces "
            "the right outcome <i>given that agents will report "
            "strategically</i></b>, which is a stronger "
            "requirement.",
            "<b>And the cleanest way to get there is to make "
            "truthful reporting optimal for each agent</b> — "
            "<b>incentive compatibility</b> — so that the reported "
            "input <i>is</i> the true one (Module 06)."]},

  {"t": "section", "label": "Part 2", "title": "Where this bites",
   "blurb": "Concretely, because the abstraction is easy to dismiss."},

  {"t": "table", "kicker": "Examples", "title": "Systems where the input is reported by interested parties",
   "header": ["System", "The reported input", "The incentive"],
   "widths": [2.6, 4.0, 4.4],
   "rows": [
     ["<b>Ad auction</b>", "<b>Bids</b>", "<b>Pay less; win profitable slots</b>"],
     ["<b>Cloud scheduler</b>", "<b>Job priority, resource needs</b>", "<b>Overstate both, always</b>"],
     ["<b>Peer review</b>", "<b>Scores and bids on papers</b>", "<b>Advance one's own interests</b>"],
     ["<b>School choice</b>", "<b>Ranked preferences</b>", "<b>Game the ranking to get a better seat</b>"],
     ["<b>Routing protocol</b>", "<b>Advertised path costs</b>", "<b>Attract or avoid transit traffic</b>"],
     ["<b>Ranking signals</b>", "<b>Links, reviews, engagement</b>", "<b>Manufacture the signal (CSCE 670)</b>"],
   ],
   "footnote": "<b>Any shared resource allocated by reported need "
               "has this structure</b> — which includes most "
               "scheduling, most quotas, and every priority "
               "field.",
   "note": "The cloud scheduler row is the one most engineers have "
           "already met without naming it."},

  {"t": "callout", "title": "And the failure mode is familiar even where the theory is not",
   "kind": "Why this is an engineering subject",
   "body": ["<b>Every priority field that users set themselves ends "
            "up uniformly high</b> — <b>which is a mechanism design "
            "failure with a well understood "
            "cause</b>, and is usually patched by "
            "quota rather than by design.",
            "<b>And every ranking signal that can be manufactured "
            "eventually is</b> — <b>which is "
            "CSCE 670 §11's adversarial "
            "information retrieval</b>, and is the same problem with a "
            "different vocabulary.",
            "<b>So the subject is not exotic</b>: <b>it is the "
            "theory behind failures engineers meet constantly and "
            "usually treat as abuse rather than as a design "
            "defect.</b>",
            "<b>Which is the framing this course "
            "takes:</b> <b>if the rules reward misreporting, the "
            "misreporting is the system working as "
            "specified</b> — <b>and the fix is the rules</b>, not "
            "enforcement."]},

  {"t": "section", "label": "Part 3", "title": "Two questions",
   "blurb": "Analysis and design, which are different jobs."},

  {"t": "bullets", "kicker": "Structure", "title": "What this course actually asks",
   "items": [
     "<b>The analysis question: given these rules, what happens?</b> "
     "— <b>which needs a solution concept</b> "
     "(Module 02) and <b>a way to measure the damage</b> "
     "(Module 04's price of anarchy).",
     "",
     "<b>And the design question: given a desired outcome, what "
     "rules produce it?</b> — <b>which is mechanism design</b> "
     "(Module 06) and is the engineering half.",
     "",
     "<b>Analysis is Modules 02 to 05</b>, and it is largely "
     "bad news: <b>equilibria are hard to compute and worse than the "
     "optimum.</b>",
     "",
     "<b>Design is Modules 06 to 11</b>, and it is largely good "
     "news: <b>a great deal can be implemented</b>, with named "
     "exceptions.",
     "",
     "<b>And the exceptions are theorems</b> "
     "(Modules 06 §4, 10 §3) — <b>which tell you what to stop "
     "trying to build.</b>",
   ],
   "footnote": "<b>The impossibility results tell you what to stop "
               "trying to build</b> — which is the most practically "
               "valuable thing a negative theorem "
               "does."},

  {"t": "section", "label": "Part 4", "title": "The position",
   "blurb": "Which this course holds throughout."},

  {"t": "callout", "title": "A mechanism's guarantees hold under a model of the agents, and the agents are people",
   "kind": "Closing",
   "body": ["<b>'Truthful reporting is a dominant strategy' assumes "
            "agents know their own valuations, compute best responses, "
            "and do not collude</b> — <b>all three of which fail "
            "sometimes.</b>",
            "<b>And the second-price auction is the standard "
            "example:</b> <b>provably truthful, and bidders in "
            "practice still shade their bids</b>, because they do not "
            "believe the rule or do not understand it "
            "(Module 07 §4).",
            "<b>Which does not make the theory useless</b> — "
            "<b>it makes it a model whose assumptions should be stated "
            "with its conclusions</b>, exactly like every other model in "
            "this program.",
            "<b>So the rule here:</b> <b>name the solution concept, "
            "name the agent model, and name the impossibility you chose "
            "to live with</b> — <b>three things, and Module 13 is "
            "about all of them.</b>"]},
 ],
 "takeaways": [
   "A sorting algorithm's input does not care how it is sorted; a bidder's "
   "valuation does care who wins.",
   "Correctness becomes: the right outcome given that agents report "
   "strategically — which is a stronger requirement.",
   "Any shared resource allocated by reported need has this structure, "
   "including every user-set priority field.",
   "If the rules reward misreporting, the misreporting is the system "
   "working as specified, and the fix is the rules.",
   "Analysis is largely bad news and design is largely good news, with the "
   "exceptions being theorems.",
   "The impossibility results tell you what to stop trying to build.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The shift"),
  ("callout", "Every algorithms course before this one assumed the input was "
              "given; here it is reported by somebody with a preference over "
              "your output",
   ["<b>A sorting algorithm's input does not care how it is "
    "sorted</b> — <b>a bidder's valuation does care who wins the "
    "item</b>, <b>and will be reported accordingly if misreporting "
    "helps</b>, which is not dishonesty so much as rational "
    "participation.",
    "<b>So an algorithm that is provably correct on the reported "
    "input may be useless with respect to the true one</b> — "
    "<b>and the true input is not observable</b>, by anybody, ever, "
    "<b>which is the whole difficulty of the subject</b> and what "
    "distinguishes it from robustness or error tolerance.",
    "<b>Which means correctness has to be redefined:</b> <b>a "
    "mechanism is correct if it produces the right outcome <i>given "
    "that agents will report strategically</i></b> — <b>which is a "
    "strictly stronger requirement</b> than being correct on honest "
    "input, and is not implied by it.",
    "<b>And the cleanest route to it is to make truthful reporting "
    "optimal for each agent individually</b> — <b>incentive "
    "compatibility</b> — <b>so that the reported input simply "
    "<i>is</i> the true one</b> and the ordinary algorithmic analysis "
    "applies again (Module 06, and it is why that module is the "
    "course's centre)."]),

  ("h1", "2 &nbsp; Where this bites"),
  ("table", ["System", "The reported input", "The incentive to misreport"],
   [["<b>Advertising auction</b>", "<b>Bids.</b>",
     "<b>Pay less than your value; win the slots that are "
     "profitable.</b>"],
    ["<b>Cloud or cluster scheduler</b>",
     "<b>Job priority and declared resource requirements.</b>",
     "<b>Overstate both, always</b> — see the note."],
    ["<b>Peer review assignment</b>",
     "<b>Bids on papers, and review scores.</b>",
     "<b>Advance one's own work and collaborators; a real and "
     "studied problem.</b>"],
    ["<b>School choice and residency matching</b>",
     "<b>Ranked preference lists.</b>",
     "<b>Rank strategically rather than truly, to get a better "
     "assignment</b> (Module 09)."],
    ["<b>Inter-domain routing</b>",
     "<b>Advertised path costs and availability.</b>",
     "<b>Attract paying transit traffic, or avoid carrying it "
     "free.</b>"],
    ["<b>Search and recommendation signals</b>",
     "<b>Links, reviews, engagement.</b>",
     "<b>Manufacture the signal</b> — CSCE 670 Module 11's "
     "adversarial information retrieval."]],
   [0.22, 0.32, 0.46]),
  ("p", "<b>Any shared resource allocated by reported need has this "
        "structure</b> — <b>which includes most scheduling, most "
        "quota systems, and every priority field a user can set</b>. "
        "<b>The cloud scheduler row is the one most engineers have "
        "already met without naming it</b>: the priority field that is "
        "always 'high', the resource request that is always double what "
        "is used."),
  ("callout", "And the failure mode is familiar even where the theory is not",
   ["<b>Every priority field that users set for themselves ends up "
    "uniformly high</b> — <b>which is a mechanism design failure "
    "with a well understood cause</b>, <b>and is usually patched by "
    "imposing quotas rather than by redesigning the rule</b>, which "
    "works and is a different thing from solving it.",
    "<b>And every ranking signal that can be manufactured eventually "
    "is</b> — <b>which is CSCE 670 Module 11's adversarial "
    "information retrieval</b>, <b>and is exactly the same problem with "
    "a different vocabulary</b>: a metric that determines an allocation "
    "becomes a target (CSCE 676 Module 13's proxy problem).",
    "<b>So the subject is not exotic</b>: <b>it is the theory "
    "behind failures that engineers meet constantly and usually treat as "
    "abuse rather than as a design defect</b> — which matters, "
    "because the two framings lead to completely different "
    "responses.",
    "<b>Which is the framing this course takes:</b> <b>if the rules "
    "reward misreporting, then the misreporting is the system working as "
    "specified</b> — <b>and the fix is the rules</b>, not "
    "enforcement, not education, and not an appeal to good "
    "behaviour."]),

  ("break",),
  ("h1", "3 &nbsp; Two questions"),
  ("ul", ["<b>The analysis question: given these rules, what will "
          "happen?</b> — <b>which needs a solution concept to "
          "predict behaviour</b> (Module 02) <b>and a way to measure "
          "the damage relative to what a designer would have chosen</b> "
          "(Module 04's price of anarchy).",
          "<b>And the design question: given a desired outcome, what "
          "rules produce it?</b> — <b>which is mechanism "
          "design</b> (Module 06) <b>and is the engineering half of "
          "the subject</b>, and the half this course is ultimately "
          "for.",
          "<b>Analysis occupies Modules 02 through 05</b>, and it "
          "is largely bad news: <b>equilibria are hard to compute "
          "(Module 03) and are worse than the social optimum "
          "(Module 04)</b>, sometimes substantially.",
          "<b>Design occupies Modules 06 through 11</b>, and it is "
          "largely good news: <b>a great deal can be implemented "
          "truthfully</b>, including some things that look impossible "
          "at first, <b>with named exceptions.</b>",
          "<b>And the exceptions are theorems</b> (Module 06 "
          "&sect;4's Myerson-Satterthwaite, Module 10 &sect;3's "
          "Gibbard-Satterthwaite) — <b>which tell you what to stop "
          "trying to build</b>, <b>which is the most practically "
          "valuable thing a negative theorem does</b> and is worth the "
          "effort of understanding precisely."]),

  ("h1", "4 &nbsp; The position"),
  ("callout", "A mechanism's guarantees hold under a model of the agents, and "
              "the agents are people",
   ["<b>'Truthful reporting is a dominant strategy' assumes that "
    "agents know their own valuations, can compute best responses, and "
    "do not collude</b> — <b>all three of which fail "
    "sometimes</b>, and the first is less obvious than it sounds: "
    "people frequently do not know what something is worth to "
    "them.",
    "<b>And the second-price auction is the standard "
    "example:</b> <b>provably truthful under the model, and bidders in "
    "practice still shade their bids</b>, <b>because they do not "
    "believe the rule, do not understand it, or are optimising against "
    "a repeated interaction the single-shot model omits</b> "
    "(Module 07 &sect;4).",
    "<b>Which does not make the theory useless</b> — <b>it "
    "makes it a model whose assumptions should be stated alongside its "
    "conclusions</b>, <b>exactly like every other model in this "
    "program</b> (CSCE 640 Module 13's three things, CSCE 628 "
    "Module 13's five).",
    "<b>So the rule here:</b> <b>name the solution concept, name "
    "the agent model, and name the impossibility you chose to live "
    "with</b> — <b>three things, and Module 13 is about all "
    "three.</b>"]),
 ],
 "resources": [
   ("Roughgarden &mdash; Twenty Lectures, lecture 1 (free)",
    "http://timroughgarden.org/notes.html",
    "<b>&sect;&sect;1 and 3</b> — the framing, with the sponsored "
    "search example developed as the motivating case."),
   ("Nisan et al., chapter 1 (free PDF)",
    "https://www.cs.cmu.edu/~sandholm/cs15-892F13/algorithmic-game-theory.pdf",
    "<b>&sect;3's two questions</b>, and the book's organisation follows "
    "that division."),
   ("Roughgarden &mdash; Algorithmic Game Theory, CACM (free)",
    "https://cacm.acm.org/magazines/2010/7/95065-algorithmic-game-theory/fulltext",
    "<b>&sect;&sect;1 and 2</b> — a short argument for why computer "
    "scientists need this, aimed at exactly this course's "
    "audience."),
   ("Varian &mdash; Position auctions (free preprint)",
    "https://people.ischool.berkeley.edu/~hal/Papers/2006/position.pdf",
    "<b>&sect;2's first row</b> — the ad auction analysed, which is "
    "the deployment that made this field commercially "
    "serious."),
 ],
 "exercises": [
   "<b>State the assumption this course removes</b>, and what it "
   "changes about correctness.",
   "<b>Find three systems you use</b> whose input is reported by "
   "interested parties.",
   "<b>For each, name the incentive to misreport.</b>",
   "<b>Find a priority field</b> in a system you have access to, and "
   "look at its distribution.",
   "<b>Describe one case</b> where misreporting is treated as abuse "
   "rather than as a design defect.",
   "<b>Classify five questions</b> as analysis or design.",
   "<b>State what incentive compatibility would buy you</b>, in one "
   "sentence.",
   "<b>Find a quota that patches an incentive problem</b>, and say "
   "what the designed fix would be.",
   "<b>List the three assumptions</b> behind a dominant-strategy "
   "claim.",
   "<b>Find a case where one of them visibly fails.</b>",
 ],
 "selfcheck": [
   "What assumption does this course remove?",
   "Why does that change the definition of correctness?",
   "What is incentive compatibility for?",
   "Give four systems with strategic inputs and their incentives.",
   "Why is the priority-field failure a design defect?",
   "State the analysis question and what it needs.",
   "State the design question and which modules cover it.",
   "Which half is bad news, and why?",
   "What do the impossibility results give you?",
   "Name the three assumptions behind a truthfulness claim.",
 ],
},

]

for _b in ("c717_b2", "c717_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
