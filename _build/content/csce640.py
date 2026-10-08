# -*- coding: utf-8 -*-
"""CSCE 640 Quantum Algorithms — original course content."""

COURSE = {
    "code": "CSCE 640",
    "title": "Quantum Algorithms",
    "tagline": "Interference is the resource, and the known advantages "
               "are few and specific",
    "term": "Semester 12 (with CSCE 628 and CSCE 717)",
    "prereqs": "Linear algebra over the complex numbers, properly; "
               "CSCE 629 Analysis of Algorithms; CSCE 637 Complexity "
               "Theory for Module 12; CSCE 658 Randomized Algorithms, "
               "whose amplitude-amplification analogy runs throughout",
    "deliverable": "A simulated implementation of one non-trivial "
                   "quantum algorithm, with its classical baseline "
                   "measured on the same instances, the advantage "
                   "stated as a function of problem size, and the "
                   "resource count that would be needed on hardware",
    "effort": "13–15 hours per week · 13 modules + 2 project weeks",
    "description": [
        "<b>This course is organised around a single honest "
        "claim:</b> <b>a quantum computer is a device that exploits "
        "interference among complex amplitudes, and the set of problems "
        "for which that is known to help is small, specific, and "
        "worth knowing exactly.</b> <b>Module 01 states the position "
        "and names the misconceptions</b>, because the subject is "
        "surrounded by claims that do not survive contact with the "
        "mathematics.",
        "<b>The first third builds the machinery.</b> <b>States, "
        "measurement, gates, and circuits</b> (Modules 02 and 03) "
        "— and then <b>Module 04 isolates where the advantage "
        "actually comes from</b>: <b>arranging for the wrong answers' "
        "amplitudes to cancel</b>, which is the one idea the whole "
        "subject rests on.",
        "<b>The second third is the algorithms that matter.</b> "
        "<b>The query model and Deutsch-Jozsa</b> (Module 05) for the "
        "cleanest separation; <b>Grover</b> (Module 06) with its "
        "<b>provably quadratic and no better</b> limit; <b>the quantum "
        "Fourier transform and phase estimation</b> (Modules 07 and "
        "08), <b>which is where Shor's algorithm comes from and is the "
        "one genuinely dramatic result.</b>",
        "<b>The third theme is the part the popular account "
        "omits.</b> <b>Noise, error correction, and the threshold "
        "theorem</b> (Module 10) determine whether any of this runs, "
        "and <b>the resource counts for useful instances are "
        "enormous</b> — so <b>Module 11 is about what the current "
        "generation of hardware can and cannot be expected to "
        "do</b>, stated carefully.",
        "<b>And the closing position is about claims.</b> "
        "<b>Module 12 covers BQP and, more usefully, what is not "
        "believed to be in it</b>, and <b>Module 13 is about what a "
        "demonstrated advantage establishes</b> — because <b>'a "
        "quantum computer solved this faster' is a claim about a "
        "specific problem, a specific classical baseline, and a "
        "specific machine</b>, and all three have to be named.",
    ],
    "outcomes": [
        "State what a quantum computer is, and refute the standard "
        "misconceptions.",
        "Work with quantum states, superposition, and measurement.",
        "Build and reason about quantum circuits.",
        "Explain interference as the source of every known "
        "advantage.",
        "Analyse algorithms in the query model.",
        "Derive Grover's algorithm and its optimality.",
        "Derive the quantum Fourier transform.",
        "Explain phase estimation and Shor's algorithm.",
        "Explain quantum simulation, the likeliest application.",
        "Explain noise, error correction, and the threshold "
        "theorem.",
        "Assess variational methods and near-term hardware claims.",
        "Place BQP, and state what it is not believed to contain.",
        "Claim a quantum advantage honestly.",
    ],
    "materials": [
        ("Nielsen & Chuang — Quantum Computation and Quantum "
         "Information",
         "https://www.cambridge.org/9781107002173",
         "<b>The primary text, and the standard one.</b> Modules 02 "
         "through 10 follow its development. Library copy; it is "
         "demanding and it is worth the demand."),
        ("Aaronson — Quantum Computing Since Democritus, and his "
         "lecture notes (free)",
         "https://www.scottaaronson.com/democritus/",
         "<b>Modules 01, 12, and 13.</b> The best available correction "
         "to the popular account, from somebody who works in the "
         "field and says plainly what is not known."),
        ("Kitaev, Shen & Vyalyi — Classical and Quantum Computation",
         "https://bookstore.ams.org/gsm-47/",
         "<b>Modules 07, 08, and 12.</b> The complexity-theoretic "
         "treatment, and the phase estimation development is "
         "especially clean. Library copy."),
        ("Preskill's lecture notes on quantum computation (free)",
         "http://theory.caltech.edu/~preskill/ph229/",
         "<b>Modules 04, 10, and 11, free in full.</b> The error "
         "correction and threshold material is the clearest written "
         "account, by the person who named the current era."),
        ("The Qiskit textbook and documentation (free)",
         "https://qiskit.org/",
         "<b>The implementation side</b>, Modules 03 onward — and "
         "simulating a circuit you derived on paper is the fastest way "
         "to find out you derived it wrong."),
        ("Gidney & Ekerå — How to factor 2048 bit RSA integers "
         "(free)",
         "https://quantum-journal.org/papers/q-2021-04-15-433/",
         "<b>Modules 10 and 13's resource counts.</b> A careful, "
         "specific estimate of what Shor's algorithm would actually "
         "cost in physical qubits and hours, which is the number to "
         "quote."),
    ],
    "tooling": [
        "<b>A simulator, and <code>numpy</code> is "
        "enough</b> — <b>a state of n qubits is a vector of 2 to the "
        "n complex amplitudes</b>, and <b>writing your own simulator in "
        "forty lines is the single most clarifying exercise in the "
        "course</b> (Module 02 §4).",
        "<b>Then Qiskit or Cirq</b>, for the circuit abstraction and "
        "the transpilation — <b>which makes the gate-count and "
        "connectivity constraints concrete</b> in a way a hand-rolled "
        "simulator hides.",
        "<b>And the honest ceiling:</b> <b>a laptop simulates "
        "roughly 25 to 30 qubits of general state</b>, which is "
        "<b>enough for every algorithm in this course and not enough "
        "for any useful instance of any of them</b> — a fact worth "
        "sitting with (Module 13 §1).",
        "<b>Real hardware is available free through cloud "
        "queues</b>, and <b>running a five-qubit circuit on it is "
        "worth doing once</b>, for Module 10's reason: <b>the output "
        "distribution will not be the one you "
        "derived.</b>",
        "<b>Pen and paper, unavoidably.</b> <b>Module 07's Fourier "
        "transform and Module 08's phase estimation have to be derived "
        "by hand</b> before any implementation makes sense.",
        "<b>And a classical baseline implementation for Project "
        "2</b>, measured on the same instances — because <b>an "
        "advantage claim without a measured baseline is not a "
        "claim</b> (Module 13 §2).",
    ],
    "projects": [
        {"n": 1, "after": 6,
         "title": "Write the simulator, then run Grover",
         "brief": "Build the state vector machinery yourself, and "
                  "measure what Grover actually buys.",
         "reqs": [
           "<b>A state vector simulator from scratch</b> — "
           "<b>state preparation, single-qubit and controlled gates, "
           "and measurement</b>, in whatever language, with no quantum "
           "library.",
           "<b>Verified against hand calculations</b> on one- and "
           "two-qubit circuits, including an entangled state.",
           "<b>Deutsch-Jozsa implemented</b> "
           "(Module 05), with the oracle as a black box your "
           "algorithm may call but not inspect.",
           "<b>Grover implemented</b> (Module 06), with "
           "<b>the success probability plotted against the number of "
           "iterations</b> — including past the optimum, where it "
           "goes back down.",
           "<b>The iteration count compared to the predicted "
           "π/4 · √N</b>, over several problem "
           "sizes.",
           "<b>And the classical baseline measured</b>: expected "
           "queries for random search, on the same instances.",
         ],
         "done": [
           "<b>The simulator written rather than imported</b> — "
           "<b>which is the point of the project</b>, because the "
           "amplitudes have to stop being abstract.",
           "<b>The success probability curve showing the "
           "decline</b> past the optimal iteration count — <b>which "
           "is the result that demonstrates you understand the "
           "rotation</b> rather than the recipe.",
           "<b>The quadratic speedup measured, not asserted</b>, "
           "with the constant factor reported.",
           "<b>And the entangled state verified by hand</b>, "
           "because <b>a simulator that gets product states right and "
           "entangled states wrong looks correct</b> until it does "
           "not.",
         ]},
        {"n": 2, "after": 12,
         "title": "One algorithm, honestly costed",
         "brief": "Implement something non-trivial, beat a real "
                  "baseline, and count the resources.",
         "reqs": [
           "<b>One algorithm from Modules 07 to 11</b> — phase "
           "estimation, a period-finding instance, a small simulation "
           "problem, or a variational method.",
           "<b>Derived by hand first</b>, with the derivation "
           "submitted — and <b>the implementation checked against "
           "it</b>.",
           "<b>A classical baseline implemented and measured</b> "
           "on the same instances — <b>the best classical method "
           "you can find, not a strawman</b>.",
           "<b>The scaling of both, measured over as many sizes as "
           "your simulator reaches</b>, with the fit stated.",
           "<b>A resource estimate for a useful instance</b>: "
           "<b>logical qubits, gate depth, and — using "
           "Module 10's overhead — physical qubits</b>.",
           "<b>And the honest claim</b> in Module 13 §2's form, "
           "including what your simulation could not reach.",
         ],
         "done": [
           "<b>The baseline being the best classical method rather "
           "than a convenient one</b> — <b>which is what makes the "
           "comparison mean anything</b>, and is where advantage "
           "claims most often fail (Module 13 §3).",
           "<b>The resource estimate carried through to physical "
           "qubits</b>, because <b>logical-qubit counts understate the "
           "cost by three or four orders of magnitude</b> "
           "(Module 10 §4).",
           "<b>The scaling measured over a range</b> rather than "
           "asserted from the asymptotic form.",
           "<b>And the honest claim naming the problem, the "
           "baseline, and the machine</b> — <b>all three</b>, which "
           "is the course's closing requirement and the thing most "
           "published advantage claims omit at least one of.",
         ]},
    ],
    "map": [
        ("Nielsen & Chuang (library copy)",
         "https://www.cambridge.org/9781107002173",
         "<b>Modules 02 through 10.</b> The standard development, and "
         "the exercises are the course's natural problem set."),
        ("Aaronson's lecture notes and essays (free)",
         "https://www.scottaaronson.com/",
         "<b>Modules 01, 12, and 13.</b> The honest account of what is "
         "known, what is believed, and what is marketing."),
        ("Preskill's Ph219 notes (free)",
         "http://theory.caltech.edu/~preskill/ph229/",
         "<b>Modules 04, 10, and 11, free in full</b> — and the "
         "clearest treatment of error correction anywhere."),
        ("The Qiskit textbook (free)",
         "https://qiskit.org/learn/",
         "<b>Modules 03 onward</b>, with runnable circuits for every "
         "algorithm in the course."),
        ("Watrous's lecture notes on quantum computation (free)",
         "https://cs.uwaterloo.ca/~watrous/QC-notes/",
         "<b>Modules 05, 07, 08, and 12</b> — rigorous, short, and "
         "the query-model treatment is excellent."),
        ("Quantum (the journal), open access",
         "https://quantum-journal.org/",
         "<b>Modules 11 and 13's primary literature</b>, free — and "
         "the resource-estimate papers are where the honest numbers "
         "are."),
    ],
}

MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "What a Quantum Computer Is",
 "subtitle": "And the four things it is not.",
 "question": "Does it try all the answers at once?",
 "outcomes": [
     "State what a quantum computer is, mechanically.",
     "Refute the four standard misconceptions.",
     "List the problems where an advantage is actually known.",
     "Explain why that list is short.",
     "State this course's position on advantage claims.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What it is",
   "blurb": "Mechanically, and without metaphor."},

  {"t": "callout", "title": "A quantum computer is a device that prepares a state, applies unitary operations, and measures — and interference is the only resource",
   "kind": "The whole subject, stated once",
   "body": ["<b>The state of n qubits is a unit vector of 2 to the n "
            "complex amplitudes</b> — <b>which is a lot of numbers, "
            "and is not a lot of accessible "
            "information.</b>",
            "<b>The operations are unitary</b>, meaning reversible "
            "and norm-preserving — <b>so the computation is a "
            "rotation of that vector</b>, nothing more "
            "exotic.",
            "<b>And the measurement returns one classical "
            "outcome</b>, with probability equal to the squared "
            "magnitude of its amplitude — <b>so you get one answer "
            "per run, not 2 to the n of them.</b>",
            "<b>Which locates the whole difficulty:</b> <b>the "
            "amplitudes are inaccessible and the algorithm's job is to "
            "arrange, before measuring, that the wrong answers' "
            "amplitudes cancel</b> — and <b>that is "
            "interference</b> (Module 04)."]},

  {"t": "section", "label": "Part 2", "title": "The four misconceptions",
   "blurb": "Each of which has a specific correction."},

  {"t": "table", "kicker": "Corrections", "title": "What people say, and what is true",
   "header": ["The claim", "The correction"],
   "widths": [4.2, 6.8],
   "rows": [
     ["<b>'It tries all answers at once'</b>", "<b>It holds all amplitudes and returns one outcome (§1)</b>"],
     ["<b>'It is exponentially faster'</b>", "<b>For a few specific problems; for most, not at all (§3)</b>"],
     ["<b>'It breaks encryption'</b>", "<b>RSA and discrete log, given a machine nobody has (M10 §4)</b>"],
     ["<b>'Quantum computers exist now'</b>", "<b>Devices exist; useful fault-tolerant ones do not (M11)</b>"],
   ],
   "footnote": "<b>'Tries all answers at once' is the one to unlearn "
               "first</b> — it predicts an exponential speedup for "
               "every search problem, which is false and provably so "
               "(Module 06 §4).",
   "note": "The tries-all-answers picture makes exactly the wrong "
           "prediction, which is why it must go first."},

  {"t": "callout", "title": "Because the tries-all-answers picture predicts something false",
   "kind": "Why this is worth being firm about",
   "body": ["<b>If the machine really evaluated every input and told "
            "you which succeeded, unstructured search would be "
            "constant-time</b> — <b>and it is provably not:</b> "
            "<b>Grover's quadratic improvement is optimal</b> "
            "(Module 06 §4).",
            "<b>So the metaphor is not an imprecise version of the "
            "truth; it is a model with a wrong consequence</b> — "
            "which is the only kind of wrongness worth correcting "
            "firmly.",
            "<b>And the correct picture makes the right "
            "prediction:</b> <b>you have one measurement, so you need "
            "the structure of the problem to make the right answer's "
            "amplitude large</b> — <b>and structure is exactly what "
            "unstructured search lacks.</b>",
            "<b>Which is why the known advantages all exploit "
            "structure</b> — <b>periodicity, in the case that "
            "matters</b> (Module 08) — and why the list in "
            "Part 3 is short rather than "
            "provisional."]},

  {"t": "section", "label": "Part 3", "title": "What is actually known",
   "blurb": "A short list, and it is worth memorising."},

  {"t": "bullets", "kicker": "Advantages", "title": "The known and believed separations, in decreasing confidence",
   "items": [
     "<b>Simulating quantum systems</b> — <b>which is the "
     "original proposal and the likeliest useful "
     "application</b> (Module 09), and the one where the advantage "
     "is least surprising: the machine is the same kind of thing as "
     "the problem.",
     "",
     "<b>Factoring and discrete logarithm</b> — <b>Shor, "
     "superpolynomial, and the one dramatic result</b> "
     "(Module 08). <b>It is a speedup over the best known "
     "classical method, not a proven separation</b>, which matters "
     "(Module 12 §3).",
     "",
     "<b>Unstructured search and its relatives</b> — "
     "<b>Grover, quadratic, provably optimal</b> "
     "(Module 06) — <b>and a quadratic speedup is frequently "
     "eaten by the overhead</b> (Module 10 §4).",
     "",
     "<b>Certain structured algebraic and query "
     "problems</b> — real, and narrow.",
     "",
     "<b>And for a great many problems, including NP-complete "
     "ones in general, no advantage is known or "
     "expected</b> (Module 12 §2).",
   ],
   "footnote": "<b>Quantum simulation is first on this list on "
               "purpose</b> — it is the original proposal, the "
               "least surprising advantage, and the most likely to "
               "matter in practice."},

  {"t": "section", "label": "Part 4", "title": "The position",
   "blurb": "Which this course holds throughout."},

  {"t": "callout", "title": "The mathematics is beautiful, the engineering is brutal, and the honest claims are narrow",
   "kind": "Closing",
   "body": ["<b>All three are true at once</b>, and the subject's "
            "public account usually keeps the first and drops the other "
            "two — which is how a field with real results acquires a "
            "credibility problem.",
            "<b>So this course states resource counts</b>: <b>the "
            "qubit and depth requirements for useful instances are "
            "enormous</b>, and <b>Module 10 §4 gives the numbers</b> "
            "rather than gesturing at them.",
            "<b>And it insists on baselines</b> — <b>'faster than "
            "what classical method, run by whom, on what "
            "instance'</b> — because <b>several published advantage "
            "claims have been reduced or eliminated by better classical "
            "algorithms</b> (Module 13 §3).",
            "<b>Which is the program's rule in this subject:</b> "
            "<b>an advantage is a claim about a problem, a baseline, "
            "and a machine</b>, and a claim that names fewer than all "
            "three is not yet a claim."]},
 ],
 "takeaways": [
   "A quantum computer prepares a state, applies unitary operations, and "
   "measures — and interference is the only resource.",
   "The amplitudes are inaccessible; the algorithm's job is to make the "
   "wrong answers cancel before the single measurement.",
   "'It tries all answers at once' predicts constant-time unstructured "
   "search, which is provably false.",
   "Every known advantage exploits structure, which is why the list is "
   "short rather than provisional.",
   "Quantum simulation is the original proposal and the likeliest useful "
   "application; factoring is the dramatic one.",
   "An advantage is a claim about a problem, a baseline, and a machine, and "
   "naming fewer than all three is not a claim.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What it is"),
  ("callout", "A quantum computer is a device that prepares a state, applies "
              "unitary operations, and measures — and interference is "
              "the only resource",
   ["<b>The state of n qubits is a unit vector of 2<sup>n</sup> "
    "complex amplitudes</b> — <b>which is a very large number of "
    "numbers, and is emphatically not a large amount of accessible "
    "information</b>, since you cannot read them (Module 02 "
    "&sect;3).",
    "<b>The operations are unitary</b>, meaning <b>reversible and "
    "norm-preserving</b> — <b>so the computation is a rotation of "
    "that vector in a complex inner-product space</b>, and nothing more "
    "exotic than that is going on.",
    "<b>And the measurement returns exactly one classical "
    "outcome</b>, with probability equal to the squared magnitude of "
    "that outcome's amplitude — <b>so you get one answer per run, "
    "not 2<sup>n</sup> of them</b>, and the state is destroyed in the "
    "process.",
    "<b>Which locates the whole difficulty of the subject:</b> "
    "<b>the amplitudes are inaccessible, and the algorithm's entire job "
    "is to arrange, before measuring, that the wrong answers' amplitudes "
    "cancel while the right one's reinforces</b> — and <b>that "
    "cancellation is interference</b> (Module 04, which isolates it "
    "properly)."]),

  ("h1", "2 &nbsp; The four misconceptions"),
  ("table", ["What is commonly said", "What is actually the case"],
   [["<b>'It tries all the answers at once.'</b>",
     "<b>It holds all the amplitudes simultaneously and returns exactly "
     "one outcome</b> (&sect;1) — which is a different thing with "
     "different consequences. See the callout."],
    ["<b>'It is exponentially faster than a classical computer.'</b>",
     "<b>For a few specific structured problems</b>; <b>for most "
     "problems, including most of the ones people care about, no "
     "advantage is known at all</b> (&sect;3)."],
    ["<b>'It breaks encryption.'</b>",
     "<b>RSA and discrete-log systems, yes — given a large "
     "fault-tolerant machine, which nobody has</b> (Module 10 "
     "&sect;4's resource counts). <b>Symmetric ciphers and hashes are "
     "only quadratically affected</b> (Module 06)."],
    ["<b>'Quantum computers exist now.'</b>",
     "<b>Devices exist, with tens to hundreds of noisy physical "
     "qubits</b>; <b>useful fault-tolerant ones do not</b>, and the gap "
     "is several orders of magnitude (Module 11)."]],
   [0.33, 0.67]),
  ("p", "<b>'Tries all answers at once' is the one to unlearn "
        "first</b> — <b>it predicts an exponential speedup for every "
        "search problem, which is false and provably so</b> "
        "(Module 06 &sect;4's optimality result). <b>The "
        "tries-all-answers picture makes exactly the wrong prediction, "
        "which is why it must go first</b>: a metaphor that is merely "
        "vague can be lived with, and one that entails a false theorem "
        "cannot."),
  ("callout", "Because the tries-all-answers picture predicts something false",
   ["<b>If the machine genuinely evaluated every input and then told "
    "you which one succeeded, unstructured search over N items would be "
    "constant-time</b> — <b>and it provably is not</b>: <b>Grover's "
    "quadratic improvement to &radic;N is optimal</b>, and the lower "
    "bound is a theorem (Module 06 &sect;4).",
    "<b>So the metaphor is not an imprecise version of the truth; it "
    "is a model with a wrong consequence</b> — <b>which is the only "
    "kind of wrongness worth correcting firmly</b>, and is why this "
    "module spends a section on it rather than a sentence.",
    "<b>And the correct picture makes the right prediction:</b> "
    "<b>you have exactly one measurement, so you need the structure of "
    "the problem in order to make the right answer's amplitude "
    "large</b> — <b>and structure is precisely what unstructured "
    "search, by definition, lacks.</b>",
    "<b>Which is why every known advantage exploits structure</b> "
    "— <b>periodicity, in the case that matters most</b> "
    "(Module 08's phase estimation) — and <b>why the list in "
    "&sect;3 is short rather than provisional</b>: it is short because "
    "structured problems with the right kind of structure are "
    "rare."]),

  ("break",),
  ("h1", "3 &nbsp; What is actually known"),
  ("ul", ["<b>Simulating quantum systems</b> — <b>which is "
          "Feynman's original proposal and the likeliest genuinely "
          "useful application</b> (Module 09), <b>and the one where "
          "the advantage is least surprising</b>: the machine is the "
          "same kind of thing as the problem, so no clever structure has "
          "to be found.",
          "<b>Factoring and discrete logarithm</b> — <b>Shor's "
          "algorithm, superpolynomial, and the one dramatic result in "
          "the subject</b> (Module 08). <b>It is a speedup over the "
          "best <i>known</i> classical method, not a proven "
          "separation</b> — <b>which matters</b>, because nobody has "
          "shown factoring is classically hard (Module 12 "
          "&sect;3).",
          "<b>Unstructured search and its relatives</b> — "
          "<b>Grover, quadratic, and provably optimal</b> "
          "(Module 06) — <b>and a quadratic speedup is frequently "
          "eaten entirely by the error-correction overhead</b> "
          "(Module 10 &sect;4), which is a sobering and "
          "under-reported point.",
          "<b>Certain structured algebraic and query problems</b> "
          "— hidden subgroup instances, some linear-algebraic "
          "routines with heavy caveats — <b>real, and narrow</b>.",
          "<b>And for a great many problems, including NP-complete "
          "problems in general, no advantage is known or "
          "expected</b> (Module 12 &sect;2) — which is the part "
          "of the list that does the most work. <b>Quantum simulation "
          "is first on this list on purpose</b>: <b>it is the original "
          "proposal, the least surprising advantage, and the most likely "
          "to matter in practice.</b>"]),

  ("h1", "4 &nbsp; The position"),
  ("callout", "The mathematics is beautiful, the engineering is brutal, and "
              "the honest claims are narrow",
   ["<b>All three of those are true at the same time</b>, and <b>the "
    "subject's public account usually keeps the first and quietly drops "
    "the other two</b> — <b>which is how a field with genuine, "
    "deep results acquires a credibility problem</b> it did not need.",
    "<b>So this course states resource counts</b>: <b>the qubit and "
    "circuit-depth requirements for useful instances are enormous</b>, "
    "and <b>Module 10 &sect;4 gives the actual numbers</b> from the "
    "published estimates rather than gesturing at 'many qubits'.",
    "<b>And it insists on baselines</b> — <b>'faster than what "
    "classical method, implemented by whom, on what problem "
    "instance'</b> — because <b>several published advantage claims "
    "have been substantially reduced or eliminated outright by better "
    "classical algorithms written in response</b> (Module 13 "
    "&sect;3), which is a healthy process and a reason for "
    "care.",
    "<b>Which is the program's closing rule arriving in this "
    "subject:</b> <b>an advantage is a claim about a problem, a "
    "baseline, and a machine</b> — and <b>a claim that names fewer "
    "than all three is not yet a claim</b>, which is Module 13's "
    "whole content."]),
 ],
 "resources": [
   ("Aaronson &mdash; The Limits of Quantum Computers, and related "
    "essays (free)",
    "https://www.scottaaronson.com/writings/",
    "<b>&sect;&sect;2 and 3</b> — the misconceptions corrected by "
    "somebody in the field, and the 'no, it does not try all answers' "
    "argument in its original form."),
   ("Nielsen & Chuang, chapter 1 (library copy)",
    "https://www.cambridge.org/9781107002173",
    "<b>&sect;1</b> — the model stated carefully, and the historical "
    "development of why it was proposed."),
   ("Feynman &mdash; Simulating Physics with Computers (free "
    "copies widely available)",
    "https://link.springer.com/article/10.1007/BF02650179",
    "<b>&sect;3's first item in the original</b> — the proposal that "
    "started the subject, and it is about simulation rather than about "
    "speed."),
   ("Preskill &mdash; Quantum Computing in the NISQ era and beyond "
    "(free)",
    "https://quantum-journal.org/papers/q-2018-08-06-79/",
    "<b>&sect;&sect;2 and 4</b> — the honest assessment of where the "
    "hardware is, from 2018 and still the right framing."),
 ],
 "exercises": [
   "<b>State the three-step model</b> — prepare, evolve, "
   "measure — and say what each step can and cannot do.",
   "<b>Count the amplitudes</b> for 10, 30, and 60 qubits.",
   "<b>Then say how many bits you get from one measurement.</b>",
   "<b>Refute each of the four misconceptions</b> in two sentences "
   "each.",
   "<b>Derive the false consequence</b> of the tries-all-answers "
   "picture.",
   "<b>List the known advantages</b> from memory, in order of "
   "confidence.",
   "<b>Explain why NP-complete problems are not on the list.</b>",
   "<b>Find three popular articles</b> and identify which "
   "misconceptions each repeats.",
   "<b>Find one published advantage claim</b> that was later reduced "
   "classically.",
   "<b>Write the three things an advantage claim must name.</b>",
 ],
 "selfcheck": [
   "Give the three-step model and the one resource.",
   "How many amplitudes, and how much information per measurement?",
   "Where does the difficulty of algorithm design therefore lie?",
   "State the four misconceptions and their corrections.",
   "What false consequence does 'tries all answers' have?",
   "Why is that the right reason to reject it firmly?",
   "Why do all known advantages exploit structure?",
   "List the known advantages in order of confidence.",
   "Why is Shor's result not a proven separation?",
   "What three things must an advantage claim name?",
 ],
},

]

for _b in ("c640_b2", "c640_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
