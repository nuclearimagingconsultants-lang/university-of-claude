# -*- coding: utf-8 -*-
"""UC MATH 600 Mathematics for Computer Science — program prerequisite."""

COURSE = {
    "code": "UC MATH 600",
    "title": "Mathematics for Computer Science",
    "tagline": "Proof is a tool for being sure, and this is the course "
               "that makes the rest of the program readable",
    "term": "Prerequisite · take before Semester 1",
    "prereqs": "Secondary school algebra. Nothing else is assumed, and "
               "nothing in this course requires calculus",
    "deliverable": "A worked proof portfolio — thirty proofs you "
                   "wrote yourself, including at least five you got "
                   "wrong first and the record of what was wrong with "
                   "them",
    "effort": "8–10 hours per week · 13 modules + 2 project weeks",
    "description": [
        "<b>This is one of the two mathematics prerequisites, and "
        "skipping it is the single most common reason Semester 1 "
        "fails.</b> <b>CSCE 629 is unreadable without proof technique, "
        "induction, and asymptotic reasoning</b> — not difficult, "
        "<i>unreadable</i>, because its arguments are written in a "
        "language this course teaches.",
        "<b>The first third is proof itself.</b> <b>Module 01 argues "
        "that a proof is a tool rather than a ritual</b>, and "
        "<b>Modules 02 and 03 give you the three techniques that cover "
        "almost everything</b> — direct, contrapositive, contradiction, "
        "and then induction, which is the one computer science uses "
        "most and the one most often done badly.",
        "<b>The second third is the objects.</b> <b>Sets, functions, "
        "relations, modular arithmetic, counting, and graphs</b> "
        "(Modules 04 through 08) — <b>which are the vocabulary every "
        "later course assumes you already have</b>, and which it will "
        "not stop to define.",
        "<b>The third is the quantitative part.</b> <b>Asymptotics and "
        "recurrences</b> (Modules 09 and 10) are what CSCE 629 is "
        "actually about; <b>discrete probability and concentration</b> "
        "(Modules 11 and 12) are what CSCE 658 and every machine "
        "learning course rest on.",
        "<b>And the closing module is about honest claims</b>, which is "
        "the rule this whole program is built on. <b>A proof with a gap "
        "is not a short proof</b> — it is a different thing — and "
        "learning to see your own gaps is most of what this course is "
        "for.",
    ],
    "outcomes": [
        "Explain what a proof establishes and what it does not.",
        "Write direct, contrapositive, and contradiction proofs.",
        "Write induction proofs, including strong and structural.",
        "Work fluently with sets, functions, and relations.",
        "Use modular arithmetic and the division algorithm.",
        "Count correctly, including with overcounting corrections.",
        "Model problems as graphs and reason about them.",
        "Prove properties of trees and connectivity.",
        "Use asymptotic notation precisely.",
        "Solve recurrences, including by the master theorem.",
        "Compute discrete probabilities without the standard errors.",
        "Use expectation, linearity, and concentration bounds.",
        "State what you proved, and find your own gaps.",
    ],
    "materials": [
        ("Lehman, Leighton & Meyer — Mathematics for Computer "
         "Science (free book)",
         "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/",
         "<b>The primary text, free in full.</b> This course follows "
         "its development closely, and its exercises are the natural "
         "problem set. It is written for exactly this audience."),
        ("MIT 6.042J / 6.1200J Mathematics for Computer Science "
         "(OCW, full video)",
         "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/",
         "<b>The lectures, free.</b> Watch them alongside the "
         "modules — the recitation videos are where the proof "
         "technique is actually demonstrated."),
        ("Velleman — How to Prove It",
         "https://www.cambridge.org/9781108424189",
         "<b>Modules 01 through 03.</b> The best book on proof "
         "technique as a skill rather than a subject, and it is "
         "unusually patient. Library copy."),
        ("Rosen — Discrete Mathematics and Its Applications",
         "https://www.mheducation.com/highered/product/discrete-mathematics-applications-rosen/M9781259676512.html",
         "<b>Modules 04 through 08 as a reference.</b> Comprehensive "
         "and dry; good for looking something up, poor for reading "
         "straight through. Library copy."),
        ("Mitzenmacher & Upfal — Probability and Computing",
         "https://www.cambridge.org/9781107154889",
         "<b>Modules 11 and 12.</b> Where discrete probability is "
         "developed for computer scientists rather than for "
         "statisticians, and the direct prerequisite for CSCE 658. "
         "Library copy."),
        ("Cormen, Leiserson, Rivest & Stein, chapters 3 and 4",
         "https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/",
         "<b>Modules 09 and 10.</b> Asymptotics and recurrences in the "
         "form CSCE 629 will use them. Library copy."),
    ],
    "tooling": [
        "<b>Paper, and a great deal of it.</b> <b>This is the one "
        "course in the program with no code requirement</b>, and "
        "writing proofs by hand is not nostalgia — it is slower, which "
        "is the point.",
        "<b>A proof portfolio file</b>, kept from week one — "
        "<b>which is the deliverable</b>, and which is far easier to "
        "assemble continuously than retrospectively.",
        "<b>Python, for checking</b> — <b>a conjecture you can "
        "test on ten thousand cases before trying to prove it is a "
        "conjecture you waste much less time on</b>, and finding a "
        "counterexample in four lines is a legitimate "
        "result (Module 01 §3).",
        "<b>And somebody to read your proofs</b>, ideally — "
        "<b>because the gap you cannot see is the whole "
        "difficulty</b> (Module 13 §2). Failing that, read them aloud "
        "a day later, which catches a surprising amount.",
    ],
    "projects": [
        {"n": 1, "after": 6,
         "title": "Fifteen proofs, and five of them wrong",
         "brief": "Build the first half of the portfolio, and keep "
                  "the failures.",
         "reqs": [
           "<b>Fifteen proofs written out in full</b>, from "
           "Modules 02 through 06 — <b>at least three by each of "
           "direct, contrapositive, contradiction, and induction</b>.",
           "<b>Five of them attempted wrongly first</b>, with "
           "<b>the wrong version kept and the error named</b> — "
           "which is the part that teaches.",
           "<b>One conjecture tested computationally before "
           "proving</b>, with the test code included.",
           "<b>And one conjecture disproved by counterexample</b>, "
           "found rather than looked up.",
         ],
         "done": [
           "<b>The wrong versions kept and the errors named</b> "
           "— <b>which is the actual deliverable</b>; a portfolio "
           "of fifteen correct proofs with no history shows less.",
           "<b>Each proof stating what it assumes</b> at the top, "
           "which is the habit Module 13 asks for.",
           "<b>The induction proofs having an explicit base case "
           "and an explicit statement of the inductive "
           "hypothesis</b> — omitting either is the characteristic "
           "error (Module 03 §3).",
           "<b>And the counterexample genuinely found</b>, with the "
           "search described.",
         ]},
        {"n": 2, "after": 12,
         "title": "Fifteen more, and the asymptotic ones",
         "brief": "Finish the portfolio with the material CSCE 629 "
                  "will assume.",
         "reqs": [
           "<b>Fifteen further proofs</b> from Modules 07 "
           "through 12, <b>including at least three asymptotic "
           "bounds and three probability arguments</b>.",
           "<b>Three recurrences solved three ways</b> — by "
           "expansion, by the master theorem, and by "
           "substitution-and-induction — <b>with the three answers "
           "agreeing</b>.",
           "<b>One counting problem solved two ways</b>, with the "
           "two answers shown to be equal algebraically.",
           "<b>One graph result proved</b> and then verified "
           "computationally on a hundred random graphs.",
           "<b>And a self-audit</b>: <b>go back to Project 1's "
           "fifteen proofs and find at least two gaps you did not see "
           "at the time.</b>",
         ],
         "done": [
           "<b>The self-audit finding real gaps</b> — <b>which "
           "it will</b>, and <b>a self-audit reporting none is the one "
           "outcome that fails this project</b> "
           "(Module 13 §2).",
           "<b>The three recurrence methods agreeing</b>, with any "
           "disagreement tracked down rather than averaged.",
           "<b>The double-counting identity proved both ways</b>, "
           "which is the clearest demonstration that counting is "
           "reasoning rather than arithmetic.",
           "<b>And the asymptotic proofs using the definition</b> "
           "— <b>constants exhibited, threshold stated</b> — "
           "rather than appealing to intuition about growth "
           "(Module 09 §2).",
         ]},
    ],
    "map": [
        ("Lehman, Leighton & Meyer (free book)",
         "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/",
         "<b>Every module.</b> Free, complete, and written for this "
         "audience — the single best resource here."),
        ("MIT 6.042J lectures and recitations (free video)",
         "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/video_galleries/video-lectures/",
         "<b>Every module</b>, and the recitations are where the "
         "technique is demonstrated rather than stated."),
        ("Velleman &mdash; How to Prove It",
         "https://www.cambridge.org/9781108424189",
         "<b>Modules 01 to 03.</b> Proof as a skill. Library copy."),
        ("Mitzenmacher & Upfal (library copy)",
         "https://www.cambridge.org/9781107154889",
         "<b>Modules 11 and 12</b>, and the bridge to CSCE 658."),
        ("CLRS chapters 3 and 4 (library copy)",
         "https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/",
         "<b>Modules 09 and 10</b>, in the notation CSCE 629 uses."),
        ("Brilliant and Project Euler (free tiers)",
         "https://projecteuler.net/",
         "<b>Practice for Modules 05 and 06</b> — number theory and "
         "counting, with immediate feedback."),
    ],
}

MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "What a Proof Is For",
 "subtitle": "A tool for being sure, not a ritual for being graded.",
 "question": "Why write it out when you already believe it?",
 "outcomes": [
     "State what a proof establishes and what it does not.",
     "Distinguish a proof from an argument and from evidence.",
     "Explain the role of counterexamples and testing.",
     "Read a proof actively rather than passively.",
     "State why this course is a prerequisite.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What it is",
   "blurb": "And what the point of writing it down is."},

  {"t": "callout", "title": "A proof is a chain of steps each of which a reader can check, ending where you wanted to be",
   "kind": "The definition, and the whole purpose",
   "body": ["<b>Not a demonstration that you are clever</b>, and "
            "<b>not a ritual the grader requires</b> — <b>a device "
            "for transferring certainty from premises to a "
            "conclusion</b>, by steps.",
            "<b>And the reader it is written for is somebody who "
            "does not already believe you</b> — <b>which is what "
            "determines the level of detail</b>, and is the only "
            "question to ask when deciding what to "
            "include.",
            "<b>So 'obviously' is a warning sign</b> — <b>it marks "
            "the place where you stopped checking</b>, and in this "
            "program's experience it marks the place where the error "
            "is.",
            "<b>Which is why proofs are written at all:</b> "
            "<b>you are the reader most likely to be fooled by your own "
            "argument</b>, and writing it out is the cheapest available "
            "defence against that."]},

  {"t": "section", "label": "Part 2", "title": "Proof, argument, evidence",
   "blurb": "Three different things, and the differences matter."},

  {"t": "table", "kicker": "Kinds", "title": "What each establishes",
   "header": ["Kind", "What it gives you", "What it cannot do"],
   "widths": [2.5, 4.3, 4.2],
   "rows": [
     ["<b>Proof</b>", "<b>Certainty, given the premises</b>", "<b>Tell you the premises are true</b>"],
     ["<b>Argument</b>", "<b>Reason to believe</b>", "<b>Rule out the case you did not consider</b>"],
     ["<b>Evidence</b>", "<b>Cases where it held</b>", "<b>Cover the infinitely many you did not test</b>"],
     ["<b>Counterexample</b>", "<b>Certainty that it is false</b>", "<b>— it is complete on its own</b>"],
   ],
   "footnote": "<b>A single counterexample is complete and a million "
               "confirming cases are not</b> — which is the "
               "asymmetry that makes testing cheap and proving "
               "necessary.",
   "note": "The asymmetry between confirming and refuting is the "
           "module's practical content."},

  {"t": "callout", "title": "Which is why testing before proving is good practice rather than cheating",
   "kind": "How to use a computer in a mathematics course",
   "body": ["<b>Check your conjecture on ten thousand cases "
            "first</b> — <b>four lines of Python</b> — <b>and if it "
            "fails, you have saved a day and gained a "
            "counterexample.</b>",
            "<b>And if it holds, you have learned nothing about "
            "whether it is true</b> — <b>but you now know it is worth "
            "the effort of proving</b>, which is a real "
            "saving.",
            "<b>Plus the failures are informative</b>: <b>the "
            "smallest counterexample usually shows you which hypothesis "
            "you forgot</b>, and that frequently converts a false "
            "conjecture into a true one.",
            "<b>So the workflow is: conjecture, test, then "
            "prove</b> — <b>and Project 1 requires one of "
            "each</b>, including one conjecture you disproved rather "
            "than proved."]},

  {"t": "section", "label": "Part 3", "title": "Reading proofs",
   "blurb": "Which is a skill, and is not reading."},

  {"t": "bullets", "kicker": "Reading", "title": "How to read a proof so that you learn something",
   "items": [
     "<b>Read the statement first and try it yourself for ten "
     "minutes</b> — <b>which is the only way the proof's moves "
     "become visible as choices</b> rather than as inevitable "
     "steps.",
     "",
     "<b>Then read for the <i>idea</i>, not the steps</b> — "
     "<b>most proofs have one idea and a page of verification</b>, and "
     "the idea is usually a single sentence.",
     "",
     "<b>Then check every step</b>, including the ones that look "
     "routine — <b>which is where published errors actually "
     "live.</b>",
     "",
     "<b>Then ask where each hypothesis was used</b> — "
     "<b>a hypothesis that is never used is either unnecessary or the "
     "proof is wrong</b>, and finding out which teaches more than the "
     "proof did.",
     "",
     "<b>And then close the book and rewrite it</b>, which is the "
     "step that distinguishes having read a proof from being able to "
     "produce one.",
   ],
   "footnote": "<b>A hypothesis that is never used is either "
               "unnecessary or the proof is wrong</b> — and checking "
               "which is the single most useful question to ask of any "
               "proof."},

  {"t": "section", "label": "Part 4", "title": "Why this is a prerequisite",
   "blurb": "Stated concretely, because it determines whether you "
            "skip it."},

  {"t": "callout", "title": "CSCE 629 is written in this language and will not stop to translate",
   "kind": "Closing",
   "body": ["<b>'We proceed by induction on the number of "
            "edges'</b>; <b>'the recurrence solves to O(n log n) by "
            "the master theorem'</b>; <b>'with probability at least "
            "1 − 1/n'</b> — <b>three sentences from the first weeks of "
            "Semester 1</b>, none of which the course will "
            "explain.",
            "<b>And the failure mode is not confusion but slow "
            "attrition</b>: <b>you follow eighty per cent, fall further "
            "behind weekly, and conclude the subject is beyond "
            "you</b> — which it is not.",
            "<b>So the honest test is Module 13's "
            "self-check</b>, taken before Semester 1 rather than "
            "after — <b>and four to six weeks here is the stated "
            "cost of passing it.</b>",
            "<b>Which is a short time against two years</b>, and "
            "<b>it is the highest-return four weeks in the whole "
            "program</b> for anybody who needs it."]},
 ],
 "takeaways": [
   "A proof is a chain of steps a reader who does not already believe you "
   "can check.",
   "'Obviously' marks the place where you stopped checking, which is often "
   "where the error is.",
   "A single counterexample is complete; a million confirming cases are "
   "not.",
   "Test the conjecture before proving it — failure saves a day and "
   "gains a counterexample.",
   "A hypothesis that is never used means the hypothesis is unnecessary or "
   "the proof is wrong.",
   "The prerequisite failure mode is not confusion but slow attrition.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What a proof is"),
  ("callout", "A proof is a chain of steps each of which a reader can check, "
              "ending where you wanted to be",
   ["<b>Not a demonstration that you are clever</b>, and <b>not a "
    "ritual that a grader requires</b> — <b>a device for "
    "transferring certainty from premises to a conclusion, one checkable "
    "step at a time.</b>",
    "<b>And the reader it is written for is somebody who does not "
    "already believe you</b> — <b>which is what determines the "
    "level of detail</b>, <b>and is the only question to ask when "
    "deciding what to include</b>: would a sceptical reader accept this "
    "line without further argument?",
    "<b>So the word 'obviously' is a warning sign</b> — <b>it "
    "marks exactly the place where you stopped checking</b> — and "
    "<b>in this program's experience it marks the place where the error "
    "is</b>. Replace it with the reason, or delete the step.",
    "<b>Which is why proofs are written out at all:</b> <b>you are "
    "the reader most likely to be fooled by your own argument</b>, since "
    "you already believe the conclusion — <b>and writing it out in "
    "full is the cheapest available defence against that</b> "
    "(Module 13 &sect;2)."]),

  ("h1", "2 &nbsp; Proof, argument, evidence"),
  ("table", ["Kind", "What it gives you", "What it cannot do"],
   [["<b>Proof</b>", "<b>Certainty, conditional on the premises.</b>",
     "<b>Tell you the premises are true</b> — which is a separate "
     "question and frequently the harder one."],
    ["<b>Argument</b>", "<b>Reason to believe, and often the right "
     "intuition.</b>",
     "<b>Rule out the case you did not think of</b>, which is what "
     "the formal version is for."],
    ["<b>Evidence (testing)</b>",
     "<b>Confirmation on the cases you tried.</b>",
     "<b>Cover the infinitely many you did not try.</b>"],
    ["<b>Counterexample</b>",
     "<b>Certainty that the statement is false.</b>",
     "<b>— nothing; it is complete on its own.</b>"]],
   [0.20, 0.42, 0.38]),
  ("p", "<b>A single counterexample is complete and a million "
        "confirming cases are not</b> — <b>which is the asymmetry "
        "that makes testing cheap and proving necessary</b>, and which is "
        "the whole justification for &sect;2's callout. <b>The asymmetry "
        "between confirming and refuting is this module's practical "
        "content</b>, and it reappears in CSCE 629 as the difference "
        "between a correctness proof and a passing test suite."),
  ("callout", "Which is why testing before proving is good practice rather "
              "than cheating",
   ["<b>Check your conjecture on ten thousand cases first</b> "
    "— <b>four lines of Python</b> — <b>and if it fails, you "
    "have saved yourself a day and gained a counterexample</b>, which "
    "is itself a complete result (&sect;2's table).",
    "<b>And if it holds, you have learned nothing about whether it "
    "is true</b> — no amount of testing establishes a universal "
    "statement — <b>but you now know it is worth the effort of "
    "proving</b>, <b>which is a real saving</b> over discovering at the "
    "end of a long argument that the statement was false.",
    "<b>Plus the failures are informative</b>: <b>the smallest "
    "counterexample usually shows you precisely which hypothesis you "
    "forgot</b> — and that <b>frequently converts a false "
    "conjecture into a true one</b> with an extra condition attached, "
    "which is how most theorems actually get their hypotheses.",
    "<b>So the workflow is: conjecture, test, then prove</b> "
    "— and <b>Project 1 requires one of each</b>, <b>including one "
    "conjecture you disproved rather than proved</b>, because finding a "
    "counterexample is a skill with its own technique."]),

  ("break",),
  ("h1", "3 &nbsp; Reading proofs"),
  ("ul", ["<b>Read the statement first and try it yourself for ten "
          "minutes</b> — <b>which is the only way the proof's moves "
          "become visible as choices</b> rather than as inevitable "
          "steps, and ten minutes of failing is worth an hour of "
          "reading.",
          "<b>Then read for the <i>idea</i>, not the steps</b> "
          "— <b>most proofs have one idea and a page of "
          "verification</b>, <b>and the idea is usually expressible in "
          "a single sentence</b>. If you can state that sentence you "
          "have the proof; the rest you can reconstruct.",
          "<b>Then go back and check every step</b>, including and "
          "especially the ones that look routine — <b>which is "
          "where published errors actually live</b>, since nobody "
          "checks them.",
          "<b>Then ask where each hypothesis was used</b> — "
          "<b>a hypothesis that is never used is either unnecessary (so "
          "the theorem is stronger than stated) or the proof is "
          "wrong</b> — <b>and finding out which teaches more than "
          "the proof did</b>.",
          "<b>And then close the book and rewrite it from "
          "memory</b>, which is <b>the step that distinguishes having "
          "read a proof from being able to produce one</b>, and is the "
          "only part of this list that is uncomfortable."]),

  ("h1", "4 &nbsp; Why this is a prerequisite"),
  ("callout", "CSCE 629 is written in this language and will not stop to "
              "translate",
   ["<b>'We proceed by induction on the number of edges'</b>; "
    "<b>'the recurrence solves to O(n log n) by the master "
    "theorem'</b>; <b>'with probability at least 1 &minus; 1/n the "
    "algorithm succeeds'</b> — <b>three sentences from the first "
    "few weeks of Semester 1</b>, <b>none of which that course will "
    "stop to explain</b>, because it assumes this one.",
    "<b>And the failure mode is not confusion but slow "
    "attrition</b>: <b>you follow eighty per cent of each lecture, fall "
    "a little further behind every week, and eventually conclude that "
    "the subject is beyond you</b> — <b>which it is not</b>; the "
    "notation was.",
    "<b>So the honest test is Module 13's self-check, taken before "
    "Semester 1 rather than after</b> — if you can answer it, skip "
    "this course with a clear conscience — <b>and four to six "
    "weeks here is the stated cost of being able to</b>.",
    "<b>Which is a short time measured against a two-year "
    "program</b>, and <b>it is the highest-return four weeks in the "
    "whole thing</b> for anybody who needs it. It is also the easiest "
    "course here to convince yourself you do not need."]),
 ],
 "resources": [
   ("Lehman, Leighton & Meyer, chapter 1 (free)",
    "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/pages/readings/",
    "<b>&sect;&sect;1 and 2</b> — what a proof is, with the false "
    "proofs that make the point better than true ones do."),
   ("Velleman &mdash; How to Prove It, chapter 1",
    "https://www.cambridge.org/9781108424189",
    "<b>&sect;1</b> — proof as a transferable skill, patiently. "
    "Library copy."),
   ("Pólya &mdash; How to Solve It",
    "https://press.princeton.edu/books/paperback/9780691164076/how-to-solve-it",
    "<b>&sect;3</b> — how to approach a problem you cannot yet do, "
    "which is the actual difficulty. Library copy."),
   ("Project Euler (free)",
    "https://projecteuler.net/",
    "<b>&sect;2's workflow</b> — problems where testing a conjecture "
    "computationally is the natural first move."),
 ],
 "exercises": [
   "<b>Write out a proof you already believe</b> in full, and mark "
   "every step you had to think about.",
   "<b>Find three uses of 'obviously'</b> in any textbook and check "
   "whether each is.",
   "<b>State the difference</b> between a proof and evidence, in two "
   "sentences.",
   "<b>Find a statement true for n up to 40 and false after</b>, and "
   "say what that shows.",
   "<b>Write a four-line test</b> for a conjecture before proving "
   "it.",
   "<b>Disprove something by counterexample</b>, found by search.",
   "<b>Then add a hypothesis</b> that makes it true.",
   "<b>Read one proof and state its single idea</b> in a "
   "sentence.",
   "<b>Find a hypothesis in a proof</b> and locate exactly where it "
   "is used.",
   "<b>Take Module 13's self-check now</b>, and record your score "
   "honestly.",
 ],
 "selfcheck": [
   "What is a proof for, and who is it written for?",
   "Why is 'obviously' a warning sign?",
   "Why are you the reader most likely to be fooled?",
   "Contrast proof, argument, evidence, and counterexample.",
   "State the asymmetry between confirming and refuting.",
   "Why is testing before proving good practice?",
   "What does a failed test give you beyond a saved day?",
   "Give the five steps of reading a proof actively.",
   "What does an unused hypothesis tell you?",
   "What is the prerequisite failure mode, and why is it hard to "
   "notice?",
 ],
},

]

for _b in ("ucm600_b2", "ucm600_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
