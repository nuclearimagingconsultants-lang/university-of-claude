# -*- coding: utf-8 -*-
"""CSCE 713 Software Security — original course content."""

COURSE = {
    "code": "CSCE 713",
    "title": "Software Security",
    "tagline": "Why code has vulnerabilities, and what actually finds "
               "them",
    "term": "Semester 9 (with CSCE 701 and CSCE 711)",
    "prereqs": "CSCE 611 Operating Systems for the memory model, "
               "CSCE 605 Compiler Design for the analysis material, and "
               "CSCE 627 Theory of Computability for what analysis "
               "cannot promise; CSCE 606 Software Engineering for the "
               "process",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A security assessment of a real codebase — a "
                   "fuzzing campaign with its coverage reported, a "
                   "static analysis run with its findings triaged, and "
                   "every defect you found fixed, with a written account "
                   "of what the tooling could not have found",
    "description": [
        "<b>This is a defensive course about defects.</b> It covers "
        "<b>why vulnerabilities exist, which classes account for the "
        "severe ones, and which techniques actually find them</b> "
        "— so that you can build software with fewer and find the "
        "ones you have. <b>The exercises are performed on your own "
        "code and on deliberately vulnerable training targets</b>, "
        "which Module 01 §4 states as a non-negotiable "
        "constraint.",
        "<b>The organising claim is that vulnerabilities are ordinary "
        "bugs with an adversary attached.</b> <b>A buffer overflow is "
        "a correctness defect that happens to be reachable by someone "
        "who wants it</b> — which means the techniques that find "
        "correctness defects find vulnerabilities, and the difference "
        "is in what you consider an input and who you imagine supplying "
        "it (Module 01 §2).",
        "<b>The second theme is that memory safety dominates the "
        "severe-defect data, and that it is a language property rather "
        "than a discipline problem.</b> <b>Decades of careful C "
        "produced a steady supply of the same defect classes</b> "
        "(Modules 02 and 03), which is <b>an argument about tools "
        "rather than about programmers</b>, and Module 12 covers what "
        "to do when rewriting is not available.",
        "<b>The third is that the tooling has hard theoretical limits "
        "and is still worth running.</b> <b>CSCE 627 established that "
        "non-trivial program properties are undecidable</b>, so every "
        "analyser must choose between false positives and false "
        "negatives — <b>and Modules 07 through 09 are about "
        "choosing deliberately and reading the output "
        "honestly.</b>",
        "<b>And the closing position is about honest claims.</b> "
        "<b>Module 13 is about what a fuzzing campaign, a static "
        "analysis run, and a code review each establish</b> — "
        "because <b>'the scanner found nothing' is a statement about "
        "the scanner</b>, and saying what you examined, with what, for "
        "how long, is the claim that can be checked.",
    ],
    "outcomes": [
        "Explain why vulnerabilities exist and what makes one "
        "severe.",
        "Explain the memory safety defect classes and their "
        "mechanisms.",
        "Explain integer and type confusion defects.",
        "Explain injection as a parsing problem and fix it "
        "structurally.",
        "Identify concurrency defects with security consequences.",
        "Explain deserialisation and trust boundary failures.",
        "Use static analysis and triage its output.",
        "Run a fuzzing campaign and measure it properly.",
        "Use sanitisers and runtime detection effectively.",
        "Integrate security into a development lifecycle.",
        "Review code for security with a systematic method.",
        "Explain exploit mitigations and what each costs.",
        "State what an assessment of code honestly establishes.",
    ],
    "materials": [
        ("Dowd, McDonald & Schuh — The Art of Software Security "
         "Assessment",
         "https://www.oreilly.com/library/view/the-art-of/0321444426/",
         "<b>The primary reference for Modules 02 through 06 and "
         "11.</b> Dated in its examples and unmatched in its treatment "
         "of how defects arise and how to find them by reading. Library "
         "copy."),
        ("Zeller et al. — The Fuzzing Book (free, interactive)",
         "https://www.fuzzingbook.org/",
         "<b>Module 08's primary source, free and executable.</b> "
         "Builds fuzzers from scratch in the browser, which is the right "
         "way to understand what coverage guidance actually does."),
        ("Møller & Schwartzbach — Static Program Analysis (free "
         "PDF)",
         "https://cs.au.dk/~amoeller/spa/",
         "<b>Module 07's theory, free.</b> The lattice and fixpoint "
         "material from CSCE 605 applied to defect detection, and "
         "honest about the precision limits."),
        ("Google — Building Secure and Reliable Systems, the "
         "development chapters (free PDF)",
         "https://sre.google/books/building-secure-reliable-systems/",
         "<b>Modules 10 and 12, free in full</b> — and notable for "
         "arguing that secure defaults in frameworks beat developer "
         "education, which is this course's position too."),
        ("The CWE and the OWASP Top Ten (free)",
         "https://cwe.mitre.org/",
         "<b>The shared vocabulary for Modules 02 through 06.</b> Use "
         "CWE identifiers when reporting; it makes a finding "
         "searchable and comparable."),
        ("Erickson — Hacking: The Art of Exploitation, 2nd edition",
         "https://nostarch.com/hacking2.htm",
         "<b>Optional, for Module 12's mitigations.</b> Understanding "
         "why a mitigation works requires understanding what it "
         "stops — <b>and the exercises are for your own machine "
         "and the book's own targets only.</b>"),
    ],
    "tooling": [
        "<b>Your own code, and deliberately vulnerable training "
        "targets.</b> <b>Nothing else, ever</b> — which is "
        "Module 01 §4's constraint, matches CSCE 701's, "
        "and is not negotiable.",
        "<b>A C or C++ toolchain with sanitisers:</b> "
        "<b><code>clang</code> with AddressSanitizer, "
        "UndefinedBehaviorSanitizer, and ThreadSanitizer</b> "
        "— free, and Module 09's whole subject.",
        "<b>A coverage-guided fuzzer:</b> <b>libFuzzer, AFL++, or "
        "cargo-fuzz</b> for Module 08, plus "
        "<code>atheris</code> or <code>jazzer</code> if you work in a "
        "managed language.",
        "<b>Static analysers:</b> <b>clang-tidy and the Clang Static "
        "Analyzer, plus CodeQL or Semgrep</b> for writing your own "
        "queries in Module 07 §4.",
        "<b>A deliberately vulnerable target set:</b> OWASP Juice "
        "Shop or WebGoat for the web classes, and "
        "<b><code>google/fuzzer-test-suite</code> for memory "
        "defects.</b> <b>Free, legal, and designed for exactly "
        "this.</b>",
        "<b>And a real open-source project you use</b>, to fuzz and "
        "analyse for Project 2. <b>Report what you find "
        "responsibly</b>, which Module 13 §2 covers as a "
        "professional obligation.",
    ],
    "projects": [
        {"title": "A defect class, understood completely", "after": 6,
         "brief": "Take one defect class, build a minimal vulnerable "
                  "program, and then make it impossible.",
         "reqs": [
             "<b>One class chosen from Modules 02 through 06</b>, with "
             "its CWE identifier and its mechanism explained in your own "
             "words.",
             "<b>A minimal program exhibiting it</b> — yours, "
             "under fifty lines, with the defect reachable from an "
             "input.",
             "<b>A demonstration that it is a defect</b>: a sanitiser "
             "report, a crash, or a wrong answer, captured.",
             "<b>Three fixes at different levels:</b> the local fix, "
             "the API-level fix that prevents recurrence, and the "
             "language or tooling fix that eliminates the class.",
             "<b>And the detection analysis:</b> which of static "
             "analysis, fuzzing, sanitisers, and review would have found "
             "it, and which would not, with each claim tested.",
         ],
         "done": [
             "<b>The mechanism explained correctly</b>, at the level of "
             "what the machine actually does.",
             "<b>Three fixes at genuinely different levels</b> — "
             "<b>the API-level fix is the one that demonstrates "
             "understanding</b>, and it is graded hardest.",
             "<b>The detection claims tested rather than "
             "asserted</b>: you ran the tools and reported what "
             "happened, including where your prediction was wrong.",
             "<b>And the class-elimination argument honest about its "
             "cost</b>, because 'rewrite it in a safe language' has a "
             "price that Module 12 asks you to state.",
         ]},
        {"title": "A real codebase, assessed", "after": 12,
         "brief": "Assess a real open-source project you use, with "
                  "fuzzing and static analysis, and fix what you find.",
         "reqs": [
             "<b>A fuzzing campaign with a harness you wrote</b>, run "
             "for a stated duration, <b>with coverage reported</b> "
             "(Module 08 §3).",
             "<b>A static analysis run with every finding "
             "triaged</b> — true positive, false positive, or "
             "undetermined, with reasons (Module 07 "
             "§3).",
             "<b>A manual review of the highest-risk component</b>, "
             "chosen and justified by Module 11's method.",
             "<b>Every genuine defect reported responsibly and fixed "
             "where you can</b>, with the patch offered upstream.",
             "<b>Coverage and limitation analysis:</b> what fraction "
             "of the code your fuzzing reached, and what your methods "
             "could not have found.",
             "<b>And an honest claim</b> in Module 13 §1's "
             "form.",
         ],
         "done": [
             "<b>The harness non-trivial</b> — it reaches real "
             "parsing logic rather than an input validation function, "
             "and the coverage figure demonstrates it.",
             "<b>Every static finding triaged with a reason</b>; "
             "<b>'probably a false positive' is not a "
             "triage</b> and is graded as an untriaged finding.",
             "<b>Anything found reported responsibly</b>, which is "
             "assessed as a professional obligation rather than a "
             "courtesy.",
             "<b>And the limitation analysis specific:</b> <b>naming "
             "the defect classes your campaign structurally could not "
             "have found is the deliverable</b>, and it is what separates "
             "an assessment from a tool run.",
         ]},
    ],
    "map": [
        ("The Fuzzing Book (free, interactive)",
         "https://www.fuzzingbook.org/",
         "<b>Module 08 in full, and the best free resource in this "
         "course.</b> Work the notebooks rather than reading them."),
        ("Møller & Schwartzbach — Static Program Analysis (free "
         "PDF)",
         "https://cs.au.dk/~amoeller/spa/",
         "<b>Module 07's theory</b> — read it against "
         "CSCE 605 Module 11, which built the same machinery for "
         "optimisation."),
        ("MIT 6.858 Computer Systems Security (free, OCW)",
         "https://css.csail.mit.edu/6.858/",
         "<b>Modules 02, 03, and 12 as lectures and labs</b>, free "
         "with assignments. The buffer overflow and mitigation labs are "
         "the best available."),
        ("The CWE Top 25, and the annual analyses (free)",
         "https://cwe.mitre.org/top25/",
         "<b>The evidence behind Modules 02 through 06's "
         "ordering</b> — reread it annually and check this course's "
         "emphasis against it."),
        ("Google's OSS-Fuzz, and its findings (free)",
         "https://google.github.io/oss-fuzz/",
         "<b>Module 08 at scale</b> — the infrastructure, the "
         "integration guide, and tens of thousands of real defects found "
         "by exactly the method the module teaches."),
        ("LLVM's sanitizer documentation (free)",
         "https://clang.llvm.org/docs/index.html",
         "<b>Module 09's reference</b> — what each sanitiser "
         "detects, what it costs, and which combinations are "
         "incompatible."),
    ],
}

MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Why Software Has Vulnerabilities",
 "subtitle": "Ordinary bugs with an adversary attached.",
 "question": "What makes a bug a vulnerability?",
 "outcomes": [
     "Explain what distinguishes a vulnerability from a bug.",
     "Explain the input and trust boundary framing.",
     "Explain what makes a defect severe.",
     "State the course's authorisation constraint.",
     "Assess a defect's exploitability honestly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The distinction",
   "blurb": "Which is about the adversary, not the code."},

  {"t": "callout", "title": "A vulnerability is a bug that an adversary can reach and benefit from",
   "kind": "The definition, and what follows from it",
   "body": ["<b>The code defect is the same.</b> <b>What makes it a "
            "vulnerability is that an untrusted party can influence the "
            "input that triggers it, and gains something when it "
            "fires.</b>",
            "<b>So three things are required:</b> <b>a defect, a path "
            "from attacker-controlled input to that defect, and a "
            "consequence the attacker wants.</b> Remove any one and you "
            "have a bug.",
            "<b>Which means the same defect differs in severity by "
            "context.</b> <b>A buffer overflow in a parser reading "
            "network data is critical; the identical code reading a "
            "compile-time constant is a latent defect.</b>",
            "<b>And it means the techniques that find correctness "
            "defects find vulnerabilities</b> — <b>the difference is "
            "in what you treat as an input and who you imagine supplying "
            "it</b>, which is the whole of Part 2."]},

  {"t": "bullets", "kicker": "Causes", "title": "Why defects exist at all, honestly",
   "items": [
     "<b>The language permits it.</b> <b>C and C++ make memory "
     "errors expressible, and a language that does not make them "
     "expressible does not have them</b> (Module 02 "
     "§4).",
     "",
     "<b>The interface invites it.</b> <b>An API that can be "
     "called wrongly will be</b> — which is "
     "CSCE 711 Module 01 §4's misuse-resistance "
     "argument, in a general form.",
     "",
     "<b>The assumption was undocumented.</b> <b>A function that "
     "requires its input to be validated, and does not say so, will "
     "eventually be called with unvalidated input.</b>",
     "",
     "<b>The composition was never considered.</b> <b>Two "
     "components each correct in isolation</b>, with incompatible "
     "assumptions at the seam.",
     "",
     "<b>And the code outlived its context</b> — written for a "
     "trusted caller, later exposed to a network.",
   ],
   "footnote": "<b>Note what is not on this list:</b> programmer "
               "carelessness. <b>The defect classes recur across "
               "decades and across highly capable teams</b>, which makes "
               "them a property of the tools."},

  {"t": "section", "label": "Part 2", "title": "Inputs and boundaries",
   "blurb": "The framing that finds defects."},

  {"t": "callout", "title": "Your input surface is larger than the parameters of your functions",
   "kind": "The enumeration that matters",
   "body": ["<b>Obvious inputs:</b> network requests, files, command "
            "arguments, environment variables, standard input.",
            "<b>Less obvious:</b> <b>filenames, file metadata, "
            "database contents, another service's response, a "
            "configuration file, a message queue, the system clock, and "
            "the contents of a directory.</b>",
            "<b>And the one most often missed:</b> <b>data your own "
            "system wrote earlier</b> — which is attacker-controlled "
            "if the attacker could influence what was stored, and is "
            "then trusted on read.",
            "<b>So the question for every piece of data is 'who could "
            "have influenced this, and what did we assume about "
            "it'</b> — which is CSCE 701 Module 01's trust "
            "boundary analysis, applied at function granularity."]},

  {"t": "code", "kicker": "Method", "title": "How to find the reachable defects",
   "lang": "text", "code": """
  1. ENUMERATE THE ENTRY POINTS
     everywhere untrusted data enters the program

  2. TRACE EACH ONE FORWARD
     where does it go? what parses it? what indexes
     with it? what allocates based on it? what is
     interpreted by something downstream?

  3. AT EVERY USE, ASK WHAT WAS ASSUMED
     a length that fits, a non-null pointer, a valid
     UTF-8 string, a number in range, a path without
     "..", a trusted serialised object

  4. THEN ASK WHETHER THE ASSUMPTION IS CHECKED
     and specifically, checked on THIS path -- a check
     on one call site does not protect another

  THIS IS TAINT ANALYSIS DONE BY HAND, and Module 07
  automates it imperfectly. Doing it manually first is
  what makes the tool's output readable.
""",
   "caption": "<b>Step 4's 'on this path' is where real defects "
              "hide</b> — the validation exists, and one caller "
              "bypasses it.",
   "note": "This four-step method is the course's core practical "
           "habit."},

  {"t": "section", "label": "Part 3", "title": "Severity",
   "blurb": "Which is not the same as interest."},

  {"t": "table", "kicker": "Severity", "title": "What actually determines severity",
   "header": ["Factor", "The question", "Why it matters"],
   "widths": [2.6, 4.2, 5.1],
   "rows": [
     ["<b>Reachability</b>", "<b>Can untrusted input get there?</b>", "<b>Unreachable means not a vulnerability</b>"],
     ["<b>Pre-authentication</b>", "<b>Before any login?</b>", "<b>The single largest severity multiplier</b>"],
     ["<b>Primitive gained</b>", "<b>Crash, read, write, or execution?</b>", "<b>A write is far worse than a read</b>"],
     ["<b>Privilege context</b>", "<b>What does the process hold?</b>", "<b>Least privilege bounds the damage</b>"],
     ["<b>Reliability</b>", "<b>Deterministic or racy?</b>", "<b>Affects practical exploitability</b>"],
   ],
   "footnote": "<b>Pre-authentication reachability is the factor that "
               "dominates</b> — a defect behind authentication "
               "requires an account first, which changes the adversary "
               "set entirely.",
   "note": "Students over-weight the primitive and under-weight "
           "reachability."},

  {"t": "callout", "title": "And be honest about exploitability in both directions",
   "kind": "The judgement to develop",
   "body": ["<b>Overclaiming wastes effort.</b> <b>A crash is not "
            "automatically code execution</b> — modern mitigations "
            "(Module 12) make many memory defects very hard to exploit, "
            "and treating every crash as critical exhausts the "
            "budget.",
            "<b>And underclaiming is worse.</b> <b>'Just a crash' has "
            "repeatedly turned out to be exploitable</b> once somebody "
            "capable spent a week on it, and 'not exploitable' is a "
            "claim requiring real analysis.",
            "<b>So the honest position is to state what you "
            "established:</b> <b>'reachable from unauthenticated input, "
            "causes an out-of-bounds write of attacker-controlled length, "
            "exploitability not analysed'.</b>",
            "<b>Which is the program's rule arriving in "
            "Module 01</b> — and <b>a defect report in that form "
            "is actionable, while 'critical RCE' and 'low, just a crash' "
            "both require the reader to redo your work.</b>"]},

  {"t": "section", "label": "Part 4", "title": "The constraint",
   "blurb": "Which is not negotiable."},

  {"t": "callout", "title": "Your own code, and deliberately vulnerable targets. Nothing else.",
   "kind": "The professional and legal constraint",
   "body": ["<b>Every exercise in this course is performed on code you "
            "own or on a training target built for the "
            "purpose</b> — Juice Shop, WebGoat, the fuzzer test "
            "suite, your own projects.",
            "<b>Testing systems you are not authorised to test is "
            "unlawful in most jurisdictions regardless of "
            "intent</b> — and the absence of harm is not a "
            "defence.",
            "<b>And when you find a defect in software you use, "
            "disclose it responsibly:</b> <b>report privately, allow "
            "time to fix, and coordinate publication</b> "
            "(Module 13 §2).",
            "<b>This constraint is the same one CSCE 701 states</b>, "
            "and <b>it applies to Project 2, where you will assess a real "
            "project</b> — fuzzing your own build of open-source "
            "software is fine, and probing somebody's deployment is "
            "not."]},

  {"t": "bullets", "kicker": "Orientation", "title": "What this course covers, and in what order",
   "items": [
     "<b>Modules 02–06: the defect classes</b> — "
     "<b>memory safety, integers and types, injection, concurrency, and "
     "deserialisation</b>, which together account for the severe-defect "
     "data.",
     "",
     "<b>Modules 07–09: the techniques</b> — static "
     "analysis, fuzzing, and sanitisers, <b>with their theoretical "
     "limits stated</b> (CSCE 627).",
     "",
     "<b>Modules 10–12: the practice</b> — lifecycle, "
     "review, and the mitigations you rely on when the defect is "
     "already shipped.",
     "",
     "<b>And Module 13: what an assessment establishes</b>, which is "
     "the course's closing position.",
     "",
     "<b>The ordering is deliberate:</b> <b>you cannot read a "
     "tool's output without knowing the classes it is looking "
     "for.</b>",
   ],
   "footnote": "<b>Defect classes before tooling</b> — because a "
               "static analyser's findings are unreadable to someone who "
               "does not already know what a use-after-free is."},
 ],
 "takeaways": [
   "A vulnerability requires three things: a defect, a path from "
   "attacker-controlled input, and a consequence the attacker wants.",
   "The same defect differs in severity by context, so a parser reading "
   "network data and one reading a constant are not comparable.",
   "Defects exist because languages permit them, interfaces invite them, "
   "assumptions go undocumented, and code outlives its context.",
   "Your input surface includes filenames, database contents, another "
   "service's response, and data your own system wrote earlier.",
   "Pre-authentication reachability is the single largest severity "
   "multiplier, and it is systematically under-weighted.",
   "State what you established — 'out-of-bounds write, "
   "exploitability not analysed' beats both 'critical RCE' and 'just a "
   "crash'.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The distinction"),
  ("callout", "A vulnerability is a bug that an adversary can reach and "
              "benefit from",
   ["<b>The code defect is exactly the same thing.</b> <b>What makes "
    "it a vulnerability is that an untrusted party can influence the "
    "input that triggers it, and gains something when it fires.</b> "
    "Nothing about the code changes.",
    "<b>So three things are required:</b> <b>a defect, a path from "
    "attacker-controlled input to that defect, and a consequence the "
    "attacker actually wants.</b> <b>Remove any one of the three and "
    "you have an ordinary bug</b> — which still deserves fixing, and "
    "on a different schedule.",
    "<b>Which means the identical defect differs enormously in "
    "severity by context.</b> <b>A buffer overflow in a parser reading "
    "network data is critical; byte-for-byte identical code reading a "
    "compile-time constant is a latent defect waiting for somebody to "
    "reuse the function.</b> <b>This is why severity cannot be read off "
    "the code alone</b> (&sect;3).",
    "<b>And it means the techniques that find correctness defects find "
    "vulnerabilities</b> — <b>the difference lies in what you treat "
    "as an input and who you imagine supplying it</b>, which is the whole "
    "of &sect;2 and is the single most transferable idea in the "
    "course. <b>A fuzzer is a test generator with a hostile "
    "imagination.</b>"]),
  ("ul", ["<b>The language permits it.</b> <b>C and C++ make memory "
          "errors expressible, and a language in which they are not "
          "expressible does not have them</b> (Module 02 "
          "&sect;4) — which is an observation about expressiveness "
          "rather than about programmers.",
          "<b>The interface invites it.</b> <b>An API that can be "
          "called incorrectly will eventually be called "
          "incorrectly</b> — which is CSCE 711 Module 01 "
          "&sect;4's misuse-resistance argument in its general form, and "
          "applies to every API rather than only to cryptographic "
          "ones.",
          "<b>The assumption was undocumented.</b> <b>A function that "
          "requires its input to have been validated, and does not say "
          "so, will eventually be called with unvalidated input</b> by "
          "somebody who had no way to know — frequently the original "
          "author, two years later.",
          "<b>The composition was never considered.</b> <b>Two "
          "components, each entirely correct in isolation</b>, with "
          "subtly incompatible assumptions at the seam between them "
          "— which is where a great many severe defects live and "
          "where no single-component analysis finds them.",
          "<b>And the code outlived its context</b> — written for "
          "a trusted local caller, later exposed to a network, with the "
          "original trust assumption still embedded and no longer "
          "true. <b>Note what is not on this list: programmer "
          "carelessness.</b> <b>These defect classes recur across "
          "decades, across languages, and across extremely capable "
          "teams</b>, which is precisely what makes them a property of "
          "the tools rather than of the people."]),

  ("h1", "2 &nbsp; Inputs and trust boundaries"),
  ("callout", "Your input surface is larger than the parameters of your "
              "functions",
   ["<b>The obvious inputs:</b> network requests, files, command-line "
    "arguments, environment variables, standard input. <b>Everyone "
    "enumerates these.</b>",
    "<b>The less obvious:</b> <b>filenames and file metadata, "
    "database contents, another service's response, a configuration "
    "file, a message from a queue, the system clock, the contents of a "
    "directory listing, an environment variable set by a parent "
    "process, and the terminal's own escape sequences.</b>",
    "<b>And the one most often missed entirely:</b> <b>data your own "
    "system wrote earlier</b> — which is attacker-controlled if the "
    "attacker could influence what was stored, and is then read back and "
    "trusted because 'it came from our database'. <b>This is the "
    "mechanism behind stored injection of every kind.</b>",
    "<b>So the question to ask of every piece of data is 'who could "
    "have influenced this, and what did we assume about it'</b> — "
    "which is <b>CSCE 701 Module 01's trust boundary analysis, "
    "applied at function granularity rather than at system "
    "granularity</b>, and is the same technique at a different "
    "scale."]),
  ("code", """1. ENUMERATE THE ENTRY POINTS
   everywhere untrusted data enters the program

2. TRACE EACH ONE FORWARD
   where does it go? what parses it? what indexes with
   it? what allocates based on it? what is it
   interpreted by, downstream?

3. AT EVERY USE, ASK WHAT WAS ASSUMED
   a length that fits, a non-null pointer, a valid
   UTF-8 string, a number in range, a path without
   "..", a trusted serialised object, a terminating
   null byte

4. THEN ASK WHETHER THE ASSUMPTION IS CHECKED
   and specifically, checked on THIS path -- a check at
   one call site does not protect another, and the
   defect is usually at the call site nobody listed

THIS IS TAINT ANALYSIS DONE BY HAND, and Module 07
automates it imperfectly. Doing it manually first is
what makes the tool's output readable."""),
  ("p", "<b>Step 4's 'on this path' qualifier is where the real defects "
        "hide.</b> <b>The validation exists, it is correct, and one "
        "caller bypasses it</b> — a refactor introduced a second "
        "entry point, an optimisation skipped the wrapper, a new feature "
        "called the internal function directly. <b>Which is why the "
        "question is never 'is this input validated' but 'is it validated "
        "on every path that reaches this use'</b>, and that is a question "
        "about the call graph."),

  ("break",),
  ("h1", "3 &nbsp; Severity"),
  ("table", ["Factor", "The question", "Why it matters"],
   [["<b>Reachability</b>",
     "<b>Can untrusted input actually get there?</b>",
     "<b>Unreachable means it is not a vulnerability</b> (&sect;1) "
     "— and this is where most triage effort belongs."],
    ["<b>Pre-authentication</b>",
     "<b>Is it reachable before any login?</b>",
     "<b>The single largest severity multiplier</b> — see the "
     "note."],
    ["<b>Primitive gained</b>",
     "<b>A crash, an out-of-bounds read, an out-of-bounds write, or "
     "control of execution?</b>",
     "<b>A write is far worse than a read</b>, and control of a "
     "function pointer worse again."],
    ["<b>Privilege context</b>",
     "<b>What does the affected process actually hold?</b>",
     "<b>Least privilege bounds the damage</b> (CSCE 701 "
     "Module 03) — which is why it is worth the trouble."],
    ["<b>Reliability</b>",
     "<b>Deterministic, or dependent on a race or a heap layout?</b>",
     "<b>Affects practical exploitability</b> and therefore the "
     "realistic urgency."]],
   [0.18, 0.34, 0.48]),
  ("p", "<b>Pre-authentication reachability is the factor that "
        "dominates, and it is systematically under-weighted.</b> <b>A "
        "defect behind authentication requires the attacker to obtain an "
        "account first</b>, which changes the adversary set from 'anyone "
        "on the internet' to 'anyone who can register or steal "
        "credentials' — a difference of several orders of magnitude "
        "in exposure. <b>Students reliably over-weight the primitive "
        "gained and under-weight how the input arrives.</b>"),
  ("callout", "And be honest about exploitability in both directions",
   ["<b>Overclaiming wastes effort.</b> <b>A crash is not "
    "automatically code execution</b> — modern mitigations "
    "(Module 12) make a great many memory defects genuinely hard to "
    "exploit, and <b>treating every crash as critical exhausts the "
    "remediation budget on the wrong things</b> (CSCE 701 "
    "Module 12's base rate problem, in a different setting).",
    "<b>And underclaiming is worse.</b> <b>'Just a crash' has "
    "repeatedly turned out to be fully exploitable</b> once somebody "
    "capable spent a week on it — so <b>'not exploitable' is a "
    "strong claim that requires real analysis</b>, and it is usually "
    "asserted without any.",
    "<b>So the honest position is to state precisely what you "
    "established:</b> <b>'reachable from unauthenticated input, causes "
    "an out-of-bounds write of attacker-controlled length at an "
    "attacker-influenced offset, exploitability not analysed'.</b> "
    "<b>Every clause is checkable.</b>",
    "<b>Which is the program's closing rule arriving in "
    "Module 01</b> — and <b>a defect report in that form is "
    "immediately actionable, while both 'critical RCE' and 'low, just a "
    "crash' require the reader to redo your analysis from "
    "scratch.</b> <b>Module 13 develops this into the course's closing "
    "position.</b>"]),

  ("h1", "4 &nbsp; The constraint, and the course"),
  ("callout", "Your own code, and deliberately vulnerable targets. Nothing "
              "else.",
   ["<b>Every exercise in this course is performed on code you own or "
    "on a training target built for the purpose</b> — OWASP Juice "
    "Shop, WebGoat, the fuzzer test suite, your own projects, your own "
    "build of open-source software.",
    "<b>Testing systems you are not authorised to test is unlawful in "
    "most jurisdictions regardless of your intent</b> — and <b>the "
    "absence of harm is not a defence</b>, nor is curiosity, nor is "
    "having found something real. This is settled and not a grey "
    "area.",
    "<b>And when you find a defect in software you use, disclose it "
    "responsibly:</b> <b>report privately to the maintainer, allow "
    "reasonable time for a fix, and coordinate publication</b> "
    "(Module 13 &sect;2, which treats this as a professional "
    "obligation rather than a courtesy).",
    "<b>This constraint is identical to the one CSCE 701 "
    "states</b>, and <b>it applies directly to Project 2, where you "
    "will assess a real project</b> — <b>fuzzing your own local "
    "build of open-source software is entirely fine, and probing "
    "somebody's running deployment of it is not</b>, and the distinction "
    "is the whole of the rule."]),
  ("ul", ["<b>Modules 02 through 06: the defect classes</b> — "
          "<b>memory safety, integers and type confusion, injection, "
          "concurrency, and deserialisation</b>, which together account "
          "for the great majority of severe defects in the published "
          "data.",
          "<b>Modules 07 through 09: the techniques</b> — static "
          "analysis, fuzzing, and dynamic sanitisers, <b>with their "
          "theoretical limits stated honestly</b> (CSCE 627's "
          "undecidability results, which bound what any tool can "
          "promise).",
          "<b>Modules 10 through 12: the practice</b> — the "
          "development lifecycle, systematic code review, and the "
          "exploit mitigations you rely on when the defect is already "
          "shipped and cannot be removed.",
          "<b>And Module 13: what an assessment actually "
          "establishes</b>, which is the course's closing position and "
          "the form of Project 2's final claim.",
          "<b>The ordering is deliberate:</b> <b>you cannot read a "
          "tool's output without already knowing the classes it is "
          "looking for.</b> <b>Defect classes before tooling</b> "
          "— because a static analyser's findings are genuinely "
          "unreadable to somebody who does not already know what a "
          "use-after-free is, and the commonest failure of static "
          "analysis adoption is handing the output to people who "
          "cannot triage it (Module 07 &sect;3)."]),
 ],
 "resources": [
   ("Dowd, McDonald & Schuh, chapters 1 and 2",
    "https://www.oreilly.com/library/view/the-art-of/0321444426/",
    "<b>&sect;1 and &sect;2's method</b> — the best treatment of "
    "reading code adversarially that exists. Library copy."),
   ("The CWE Top 25 and its methodology (free)",
    "https://cwe.mitre.org/top25/",
    "<b>&sect;3's severity factors and the evidence for Modules 02 "
    "through 06's ordering</b> — including how the ranking is "
    "computed, which is worth understanding."),
   ("CVSS specification (free)",
    "https://www.first.org/cvss/",
    "<b>&sect;3 as the industry's scoring system</b> — useful, "
    "widely required, and read CSCE 701 Module 12 on why a single "
    "number misleads."),
   ("MIT 6.858, the first lectures (free, OCW)",
    "https://css.csail.mit.edu/6.858/",
    "<b>&sect;1 and &sect;2 as lectures</b>, free, with the threat model "
    "framing developed carefully."),
 ],
 "exercises": [
   "<b>Take a bug you have fixed</b> and determine whether it was a "
   "vulnerability, using the three-part test.",
   "<b>Find a defect whose severity depends entirely on context</b>, and "
   "describe both contexts.",
   "<b>Enumerate every input</b> to a program you wrote — including "
   "the non-obvious ones.",
   "<b>Find one place you trust data your own system wrote.</b>",
   "<b>Run Part 2's four steps</b> on one entry point, by hand, and "
   "record what you assumed at each use.",
   "<b>Find one assumption that is checked on one path and not "
   "another.</b>",
   "<b>Rank five defects by Part 3's factors</b> and compare against "
   "your intuition.",
   "<b>Rewrite a severity claim</b> in the honest form.",
   "<b>Install a deliberately vulnerable target</b> and confirm it runs "
   "locally.",
   "<b>Write the authorisation constraint in your own words</b>, and "
   "keep it for Project 2.",
 ],
 "selfcheck": [
   "What three things does a vulnerability require?",
   "Why does the same defect differ in severity by context?",
   "Give five reasons defects exist, and say what is not on the list.",
   "Name five non-obvious inputs.",
   "Why is data your own system wrote an input?",
   "Give Part 2's four steps and say where defects hide.",
   "Name five severity factors and which dominates.",
   "Why is overclaiming bad, and why is underclaiming worse?",
   "Give the honest form of a defect report.",
   "State the authorisation constraint and how it applies to Project "
   "2.",
 ],
},

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Memory Safety",
 "subtitle": "The class that dominates the severe-defect data.",
 "question": "What exactly goes wrong, at the machine level?",
 "outcomes": [
     "Explain spatial and temporal safety violations.",
     "Explain each major class and its mechanism.",
     "Explain why the stack and heap cases differ.",
     "Explain what the safe languages actually guarantee.",
     "Find these defects in code you read.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two kinds",
   "blurb": "Spatial and temporal, which need different fixes."},

  {"t": "table", "kicker": "Taxonomy", "title": "The two kinds, and the classes under each",
   "header": ["Kind", "Violation", "Classes"],
   "widths": [2.6, 3.8, 5.5],
   "rows": [
     ["<b>Spatial</b>", "<b>Access outside the object's bounds</b>", "<b>Buffer overflow and underflow, OOB read/write</b>"],
     ["<b>Temporal</b>", "<b>Access outside the object's lifetime</b>", "<b>Use-after-free, double free, dangling pointer</b>"],
     ["<b>Initialisation</b>", "<b>Read before any write</b>", "<b>Uninitialised memory disclosure</b>"],
     ["<b>Type</b>", "<b>Access as the wrong type</b>", "<b>Type confusion (Module 03 §4)</b>"],
   ],
   "footnote": "<b>The distinction matters because the fixes "
               "differ:</b> <b>spatial safety needs bounds, and temporal "
               "safety needs ownership or lifetime tracking</b> — "
               "which is harder and is why it took longer to solve.",
   "note": "Spatial versus temporal is the organising distinction."},

  {"t": "callout", "title": "Temporal safety is the harder problem, which is why it was solved later",
   "kind": "Why these are not one topic",
   "body": ["<b>A bounds check is local.</b> <b>You need the object's "
            "size and the index, both available at the point of "
            "access</b> — so a compiler or a runtime can insert the "
            "check mechanically.",
            "<b>Lifetime is not local.</b> <b>Whether a pointer is "
            "still valid depends on what happened elsewhere in the "
            "program</b>, possibly in another thread, possibly through "
            "several aliases.",
            "<b>So temporal safety needs either a runtime cost "
            "(garbage collection, reference counting) or a static "
            "discipline (ownership and borrowing)</b> — and both "
            "are substantial design commitments.",
            "<b>Which is exactly why use-after-free is now the "
            "dominant class in mature C++ codebases</b> — the "
            "spatial defects were largely found by tooling, and the "
            "temporal ones were not."]},

  {"t": "section", "label": "Part 2", "title": "The classes",
   "blurb": "Mechanism by mechanism."},

  {"t": "code", "kicker": "Spatial", "title": "The spatial classes, and what each does",
   "lang": "text", "code": """
  BUFFER OVERFLOW (write past the end)
      overwrites whatever follows: other variables, a
      saved return address, heap metadata, a function
      pointer. The classic, and still common.

  OUT-OF-BOUNDS READ
      discloses adjacent memory -- which may be another
      user's data, a key, or a pointer that defeats
      address randomisation (Module 12)

  OFF-BY-ONE
      the single byte past the end. Enough to corrupt a
      length field, a null terminator, or the low byte
      of a pointer.

  UNDERFLOW / NEGATIVE INDEX
      a signed index that went below zero, usually from
      an integer defect (Module 03)

  AND THE COMMON CAUSES
      a length taken from the input and trusted
      a size computed with an overflow
      a string function with no bound
      and a check that used the wrong buffer's size
""",
   "caption": "<b>'A check that used the wrong buffer's size' is "
              "underrated</b> — it survives review because the check "
              "is visibly present.",
   "note": "The wrong-buffer case is the one reviewers miss."},

  {"t": "code", "kicker": "Temporal", "title": "The temporal classes, and why they are exploitable",
   "lang": "text", "code": """
  USE-AFTER-FREE
      the allocator may have reissued that memory to
      someone else. An attacker who controls an
      allocation between the free and the use controls
      what the stale pointer now points at.

  DOUBLE FREE
      corrupts allocator metadata, which is itself a
      write primitive in many allocators.

  DANGLING POINTER TO THE STACK
      returning a pointer to a local, or keeping one
      after the frame is gone. The memory is reused by
      the next call.

  AND THE PATTERNS THAT PRODUCE THEM
      an error path that frees and then continues
      two owners with unclear responsibility
      a cached pointer that outlives its object
      a container reallocating while a pointer into it
          is held -- iterator invalidation
      and a callback that fires after teardown
""",
   "caption": "<b>Iterator invalidation is the one that looks like "
              "ordinary code</b> — a push_back during iteration is a "
              "use-after-free with no free in sight.",
   "note": "Iterator invalidation makes the class feel less exotic."},

  {"t": "section", "label": "Part 3", "title": "Stack and heap",
   "blurb": "Different layouts, different consequences."},

  {"t": "bullets", "kicker": "Differences", "title": "Why the two regions behave differently",
   "items": [
     "<b>The stack holds return addresses and saved "
     "registers</b>, so an overflow there historically gave direct "
     "control of execution — which is why stack canaries exist "
     "(Module 12 §2).",
     "",
     "<b>The stack is also predictable in layout</b>, which made "
     "the classic attack reliable, and which address randomisation "
     "partly addresses.",
     "",
     "<b>The heap holds allocator metadata and other objects</b> "
     "— so a heap overflow corrupts a neighbour, and <b>the "
     "attacker's work is in arranging which neighbour</b>.",
     "",
     "<b>Which is why heap exploitation is about allocation "
     "control</b> rather than about the overflow itself — and why "
     "allocator hardening is a real mitigation.",
     "",
     "<b>And both are now substantially mitigated rather than "
     "fixed</b>, which Module 12 treats honestly.",
   ],
   "footnote": "<b>The shift from stack to heap defects over two "
               "decades was driven by mitigations</b> — the stack "
               "was hardened first, so the attention moved."},

  {"t": "section", "label": "Part 4", "title": "What safe languages give",
   "blurb": "Precisely, including the gaps."},

  {"t": "callout", "title": "A memory-safe language eliminates the class rather than reducing the defect rate",
   "kind": "The argument, stated accurately",
   "body": ["<b>Rust, Go, Java, Python, and C# do not have "
            "exploitable buffer overflows or use-after-free in safe "
            "code</b> — not fewer, but structurally none, because "
            "the error is not expressible.",
            "<b>And the evidence is strong:</b> <b>large projects "
            "report that memory safety accounted for the majority of "
            "their severe vulnerabilities, and that new code in a safe "
            "language contributes essentially none of them.</b>",
            "<b>But the gaps are real:</b> <b><code>unsafe</code> "
            "blocks, foreign function interfaces, the runtime itself, "
            "and logic defects which are entirely "
            "unaffected.</b>",
            "<b>So the honest claim is narrow and still "
            "large:</b> <b>'eliminates this class in safe code' "
            "— which is most of the severe-defect data and is not "
            "all of security.</b>"]},

  {"t": "bullets", "kicker": "Practice", "title": "And what to do in C and C++ meanwhile",
   "items": [
     "<b>Run the sanitisers in CI</b> "
     "(Module 09) — <b>AddressSanitizer finds most "
     "spatial and many temporal defects</b>, and it is the "
     "single highest-value change available.",
     "",
     "<b>Fuzz the parsers</b> (Module 08), because that is where "
     "attacker-controlled input meets manual memory "
     "handling.",
     "",
     "<b>Use the containers and smart pointers</b>, and treat raw "
     "pointer arithmetic as a review trigger.",
     "",
     "<b>Enable the compiler's hardening</b> — bounds-checked "
     "standard library modes, and the warnings as errors.",
     "",
     "<b>And write new components in a safe language where the "
     "interface permits</b>, which is the incremental version of the "
     "argument above.",
   ],
   "footnote": "<b>Sanitisers in CI plus fuzzing the parsers is the "
               "highest-yield pair</b> — and both are achievable "
               "without rewriting anything."},
 ],
 "takeaways": [
   "Spatial violations breach bounds and temporal ones breach lifetime, "
   "and the two need different fixes.",
   "A bounds check is local and a lifetime check is not, which is why "
   "temporal safety was solved later and why use-after-free now dominates.",
   "A check that used the wrong buffer's size survives review because the "
   "check is visibly present.",
   "Iterator invalidation is a use-after-free with no free in sight, which "
   "is why it looks like ordinary code.",
   "Heap exploitation is about controlling allocation rather than about "
   "the overflow, which is why allocator hardening matters.",
   "A safe language eliminates the class in safe code rather than reducing "
   "a rate — a narrow claim that covers most severe defects.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two kinds of violation"),
  ("table", ["Kind", "The violation", "The classes"],
   [["<b>Spatial</b>",
     "<b>Access outside the bounds of the intended object.</b>",
     "<b>Buffer overflow and underflow, out-of-bounds read and "
     "write, off-by-one.</b>"],
    ["<b>Temporal</b>",
     "<b>Access outside the lifetime of the intended object.</b>",
     "<b>Use-after-free, double free, dangling pointer to a dead "
     "stack frame.</b>"],
    ["<b>Initialisation</b>",
     "<b>Reading memory before anything was written to it.</b>",
     "<b>Uninitialised memory disclosure</b> — which leaks "
     "whatever the previous occupant left."],
    ["<b>Type</b>", "<b>Accessing memory as the wrong type.</b>",
     "<b>Type confusion</b> (Module 03 &sect;4), which is "
     "adjacent and worth separating."]],
   [0.18, 0.34, 0.48]),
  ("callout", "Temporal safety is the harder problem, which is why it was "
              "solved later",
   ["<b>A bounds check is local.</b> <b>You need the object's size and "
    "the index, and both are available right at the point of "
    "access</b> — so a compiler or a runtime can insert the check "
    "mechanically, which is exactly what every bounds-checked language "
    "does.",
    "<b>Lifetime is not local.</b> <b>Whether a pointer is still "
    "valid depends on what has happened elsewhere in the program</b> "
    "— possibly in a different function, possibly in another thread, "
    "possibly through any of several aliases to the same object, and the "
    "information simply is not present at the point of use.",
    "<b>So temporal safety requires either a runtime cost — "
    "garbage collection, or reference counting — or a static "
    "discipline such as ownership and borrowing</b>, and <b>both are "
    "substantial design commitments</b> that affect the whole language "
    "rather than one check.",
    "<b>Which is exactly why use-after-free is now the dominant class "
    "in mature C++ codebases</b>: <b>the spatial defects were largely "
    "found by tooling over the past two decades, and the temporal ones "
    "were not</b>, because detecting them requires knowing a lifetime "
    "the tool cannot see (Module 09 &sect;1 on what "
    "AddressSanitizer can and cannot catch)."]),

  ("h1", "2 &nbsp; The classes"),
  ("code", """BUFFER OVERFLOW (write past the end)
    overwrites whatever happens to follow: other
    variables, a saved return address, heap allocator
    metadata, a function pointer, a length field. The
    classic, and still common.

OUT-OF-BOUNDS READ
    discloses adjacent memory -- which may be another
    user's data, a cryptographic key, or a pointer
    value that defeats address randomisation
    (Module 12 section 2)

OFF-BY-ONE
    the single byte past the end. Enough to corrupt a
    length field, a null terminator, or the low byte of
    a pointer -- all of which have been exploited.

UNDERFLOW / NEGATIVE INDEX
    a signed index that went below zero, usually
    arriving from an integer defect (Module 03)

AND THE COMMON CAUSES
    a length taken from the input and trusted
    a size computed with an arithmetic overflow
    a string function with no bound argument
    and a check that used the WRONG buffer's size"""),
  ("p", "<b>'A check that used the wrong buffer's size' is badly "
        "underrated.</b> <b>It survives code review because the check is "
        "visibly present</b> — the reviewer sees a bounds comparison, "
        "ticks it, and moves on — and it survives testing because the "
        "two buffers are usually the same size in the common case. "
        "<b>Which makes it a defect that only careful reading or a "
        "sanitiser finds</b>, and it is worth looking for specifically "
        "whenever two buffers appear in one function."),
  ("code", """USE-AFTER-FREE
    the allocator may have reissued that memory to
    somebody else. An attacker who controls an
    allocation between the free and the use controls
    what the stale pointer now points at -- which turns
    a dangling read into a controlled read.

DOUBLE FREE
    corrupts allocator metadata, which is itself a write
    primitive in many allocator designs.

DANGLING POINTER TO THE STACK
    returning a pointer to a local, or retaining one
    after the frame is gone. The memory is reused by
    the very next call.

AND THE PATTERNS THAT PRODUCE THEM
    an error path that frees and then continues
    two owners with unclear responsibility
    a cached pointer that outlives its object
    a container reallocating while a pointer into it is
        still held -- iterator invalidation
    and a callback that fires after teardown"""),
  ("p", "<b>Iterator invalidation is the one that looks like entirely "
        "ordinary code.</b> <b>A <code>push_back</code> during iteration "
        "is a use-after-free with no <code>free</code> anywhere in "
        "sight</b> — the container reallocated and the held pointer "
        "or iterator now references the old buffer. <b>Which makes the "
        "class feel considerably less exotic</b>, and is the example worth "
        "leading with when explaining it to people who believe "
        "use-after-free is an exotic C problem."),

  ("break",),
  ("h1", "3 &nbsp; Stack and heap"),
  ("ul", ["<b>The stack holds return addresses and saved "
          "registers</b>, so an overflow there historically gave direct "
          "control of execution by overwriting where the function would "
          "return to — <b>which is precisely why stack canaries "
          "exist</b> (Module 12 &sect;2).",
          "<b>The stack is also highly predictable in layout</b>, "
          "which is what made the classic attack reliable — and "
          "which address space randomisation partly addresses by making "
          "the addresses unknown rather than the layout different.",
          "<b>The heap holds allocator metadata and other live "
          "objects</b> — so a heap overflow corrupts a neighbour, "
          "and <b>the attacker's real work is in arranging <i>which</i> "
          "neighbour it is</b>, by causing allocations and frees in a "
          "chosen order.",
          "<b>Which is why heap exploitation is fundamentally about "
          "allocation control rather than about the overflow itself</b> "
          "— and why allocator hardening (randomised placement, "
          "metadata separation, guard pages, quarantining freed memory) "
          "is a genuine mitigation rather than a cosmetic one.",
          "<b>And both regions are now substantially mitigated rather "
          "than fixed</b>, which Module 12 treats honestly. <b>The "
          "shift from predominantly stack defects to predominantly heap "
          "defects over two decades was driven by the "
          "mitigations</b> — the stack was hardened first, so the "
          "attention moved, which is a useful illustration of "
          "CSCE 701 Module 01's asymmetry operating over a long "
          "timescale."]),

  ("h1", "4 &nbsp; What safe languages actually give you"),
  ("callout", "A memory-safe language eliminates the class rather than "
              "reducing the defect rate",
   ["<b>Rust, Go, Java, Python, and C# do not have exploitable buffer "
    "overflows or use-after-free in safe code</b> — <b>not fewer of "
    "them, but structurally none</b>, because the error is not "
    "expressible in the language. <b>That is a categorical difference "
    "from a lower defect rate</b>, and it is the whole of the "
    "argument.",
    "<b>And the evidence is strong.</b> <b>Large projects with "
    "long-running security programmes report that memory safety "
    "accounted for the clear majority of their severe vulnerabilities, "
    "and that newly written code in a safe language contributes "
    "essentially none of them</b> — a result that has now been "
    "reported independently by several organisations with very different "
    "codebases.",
    "<b>But the gaps are real and worth naming:</b> "
    "<b><code>unsafe</code> blocks, foreign function interfaces to C "
    "libraries, the language runtime itself, and logic defects which are "
    "entirely unaffected</b> — an authorisation check you forgot is "
    "just as missing in Rust (CSCE 701 Module 03).",
    "<b>So the honest claim is narrow and still very "
    "large:</b> <b>'eliminates this class of defect in safe "
    "code'</b> — which is most of the severe-defect data and is "
    "<b>not all of security</b>, and stating it that way is both more "
    "defensible and more persuasive than the broader version "
    "(Module 13)."]),
  ("ul", ["<b>Run the sanitisers in continuous integration</b> "
          "(Module 09) — <b>AddressSanitizer finds most spatial "
          "defects and many temporal ones</b>, and it is <b>the single "
          "highest-value change available to an existing C or C++ "
          "codebase</b>, requiring no source changes at all.",
          "<b>Fuzz the parsers</b> (Module 08), because that is "
          "precisely where attacker-controlled input meets manual memory "
          "handling — and it is where the published defect data "
          "concentrates.",
          "<b>Use the containers and the smart pointers</b>, and "
          "<b>treat raw pointer arithmetic as a review trigger</b> rather "
          "than as ordinary code — which is a cheap cultural change "
          "with measurable effect.",
          "<b>Enable the compiler's hardening</b> — the "
          "bounds-checked standard library modes, the fortified string "
          "functions, and the relevant warnings promoted to errors "
          "(Module 12 &sect;2).",
          "<b>And write new components in a safe language wherever the "
          "interface boundary permits it</b>, which is the incremental "
          "version of the argument above and does not require anybody to "
          "approve a rewrite. <b>Sanitisers in CI plus fuzzing the "
          "parsers is the highest-yield pair</b>, and <b>both are "
          "achievable without rewriting anything</b>, which is why they "
          "are the recommendation rather than the language change."]),
 ],
 "resources": [
   ("Dowd, McDonald & Schuh, chapters 5 through 7",
    "https://www.oreilly.com/library/view/the-art-of/0321444426/",
    "<b>&sect;2 and &sect;3 in depth</b> — the mechanisms explained "
    "at the level of what the machine does. Library copy."),
   ("Szekeres et al. &mdash; SoK: Eternal War in Memory (free)",
    "https://web.archive.org/web/20260806120930/https://people.eecs.berkeley.edu/~dawnsong/papers/Oakland13-SoK-CR.pdf",
    "<b>&sect;1's taxonomy and &sect;3's mitigation history</b>, "
    "systematised — the single best overview of this material."),
   ("MIT 6.858's buffer overflow lab (free, OCW)",
    "https://css.csail.mit.edu/6.858/",
    "<b>&sect;2 and &sect;3 practically</b>, on targets built for the "
    "purpose — which is Module 01 &sect;4's constraint "
    "satisfied."),
   ("Google and Microsoft's memory safety reports (free)",
    "https://security.googleblog.com/2024/09/eliminating-memory-safety-vulnerabilities-Android.html",
    "<b>&sect;4's evidence</b> — measured proportions of severe "
    "defects attributable to memory safety, from codebases at scale."),
 ],
 "exercises": [
   "<b>Classify ten CVEs</b> as spatial, temporal, initialisation, or "
   "type.",
   "<b>Explain why a bounds check is local</b> and a lifetime check is "
   "not.",
   "<b>Write a minimal off-by-one</b> and observe what the extra byte "
   "corrupts.",
   "<b>Write a wrong-buffer-size check</b> and confirm review would miss "
   "it.",
   "<b>Trigger an iterator invalidation</b> and catch it with "
   "AddressSanitizer.",
   "<b>Write a use-after-free</b> and observe what the memory contains "
   "after reallocation.",
   "<b>Compare stack and heap overflow consequences</b> in two minimal "
   "programs.",
   "<b>Enable AddressSanitizer on an existing project</b> and report what "
   "it finds.",
   "<b>State the safe-language claim precisely</b>, including the four "
   "gaps.",
   "<b>Find one logic defect</b> that a safe language would not have "
   "prevented.",
 ],
 "selfcheck": [
   "Name the two kinds of violation and the classes under each.",
   "Why is temporal safety harder, and what are the two solutions?",
   "Why does use-after-free now dominate in mature C++ codebases?",
   "Name four spatial classes and four common causes.",
   "Why is the wrong-buffer-size check underrated?",
   "Name four patterns that produce temporal defects.",
   "Why does iterator invalidation look like ordinary code?",
   "Why is heap exploitation about allocation control?",
   "State precisely what a safe language gives, and the four gaps.",
   "What is the highest-yield pair for existing C and C++?",
 ],
},

]

for _b in ("c713_b2",):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
