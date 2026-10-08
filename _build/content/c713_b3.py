# -*- coding: utf-8 -*-
"""CSCE 713 — Modules 09-13."""

MODULES = [

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Sanitisers and Runtime Detection",
 "subtitle": "Making silent corruption loud.",
 "question": "The test passed. Was the program actually correct?",
 "outcomes": [
     "Explain what each sanitiser detects and how.",
     "Explain the cost and the incompatibilities.",
     "Explain why sanitisers and fuzzing are a pair.",
     "Explain what sanitisers cannot detect.",
     "Deploy them in a real build and test pipeline.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "AddressSanitizer",
   "blurb": "The highest-value tool in this course."},

  {"t": "callout", "title": "AddressSanitizer makes out-of-bounds and use-after-free loud instead of silent",
   "kind": "The mechanism, which explains the limits",
   "body": ["<b>It places poisoned 'redzones' around every allocation "
            "and checks every memory access against a shadow map</b> "
            "— so an access into a redzone is reported immediately, "
            "with the allocation and the access both located.",
            "<b>And it quarantines freed memory rather than reusing "
            "it</b>, so a use-after-free hits poisoned memory instead of "
            "somebody else's live object.",
            "<b>Which is why its limits are what they are:</b> <b>an "
            "overflow that lands <i>inside another valid object</i> is "
            "not detected</b>, because that memory is legitimately "
            "mapped — <b>so a large jump past the redzone can be "
            "missed.</b>",
            "<b>But it detects the overwhelming majority of real "
            "defects</b> — <b>and it requires no source changes at "
            "all</b>, which makes enabling it the single "
            "highest-value action available to a C or C++ project."]},

  {"t": "table", "kicker": "Sanitisers", "title": "The sanitisers, and what each costs",
   "header": ["Sanitiser", "Detects", "Cost"],
   "widths": [2.8, 4.4, 4.4],
   "rows": [
     ["<b>AddressSanitizer</b>", "<b>OOB, use-after-free, double free, leaks</b>", "<b>~2× time, ~3× memory</b>"],
     ["<b>UndefinedBehavior</b>", "<b>Signed overflow, bad shifts, misalignment</b>", "<b>Low — often under 20%</b>"],
     ["<b>ThreadSanitizer</b>", "<b>Data races</b>", "<b>~5–15× time</b>"],
     ["<b>MemorySanitizer</b>", "<b>Uninitialised reads</b>", "<b>~3×, and needs all deps instrumented</b>"],
     ["<b>HWASan</b>", "<b>Like ASan, lower memory, on ARM</b>", "<b>Low enough for production use</b>"],
   ],
   "footnote": "<b>ASan and TSan are mutually incompatible</b> and must "
               "be separate builds — and <b>UBSan's cost is low "
               "enough that parts of it ship in production</b> in some "
               "projects.",
   "note": "The incompatibility and the UBSan cost are the two "
           "practical facts."},

  {"t": "section", "label": "Part 2", "title": "UBSan",
   "blurb": "The cheap one, which catches Module 03."},

  {"t": "bullets", "kicker": "UBSan", "title": "What it catches, and why it matters here",
   "items": [
     "<b>Signed integer overflow</b> — which is "
     "Module 03's canonical defect and is otherwise "
     "entirely silent.",
     "",
     "<b>Shifts by more than the width</b>, which is undefined and "
     "produces platform-dependent nonsense.",
     "",
     "<b>Misaligned and null pointer dereferences</b>, and "
     "<b>invalid casts</b> — which is Module 03 "
     "§4's type confusion.",
     "",
     "<b>Array bounds where the size is statically known</b>, and "
     "invalid enum or boolean values.",
     "",
     "<b>And it can be configured to trap rather than report</b>, "
     "which turns undefined behaviour into a deterministic abort "
     "— a hardening measure rather than a debugging one "
     "(Module 12 §2).",
   ],
   "footnote": "<b>The trap mode is the underused "
               "feature:</b> <b>-fsanitize-trap converts a class of "
               "exploitable undefined behaviour into a crash</b>, at "
               "almost no cost."},

  {"t": "section", "label": "Part 3", "title": "The pairing",
   "blurb": "Why these two techniques multiply."},

  {"t": "callout", "title": "Fuzzing generates the inputs and sanitisers supply the oracle",
   "kind": "Why neither is as good alone",
   "body": ["<b>Fuzzing without a sanitiser only detects defects that "
            "crash</b> — and <b>a one-byte out-of-bounds read does "
            "not crash</b>, so the input that triggered it is discarded "
            "as uninteresting.",
            "<b>A sanitiser without fuzzing only checks the inputs "
            "your tests happen to use</b> — which are the valid, "
            "expected ones, and are precisely not where the defects "
            "are.",
            "<b>Together, the fuzzer explores the input space and the "
            "sanitiser reports every violation it reaches</b> — "
            "which is why <b>this pairing found most of the memory "
            "defects fixed in major open-source projects over the past "
            "decade.</b>",
            "<b>So the recommendation is a single pipeline:</b> "
            "<b>sanitiser-instrumented build, coverage-guided fuzzer, "
            "persistent corpus, crashes as regression "
            "tests</b> (Module 08 §4)."]},

  {"t": "bullets", "kicker": "Pipeline", "title": "And the same build serves your ordinary tests",
   "items": [
     "<b>Run the existing test suite under AddressSanitizer</b> "
     "— <b>which frequently finds defects on day one</b>, in "
     "code that has passed its tests for years.",
     "",
     "<b>Because a test asserts the output and a sanitiser asserts "
     "the execution</b> — so a test can pass while the program "
     "corrupts memory.",
     "",
     "<b>Add UBSan to the same build</b>, since the costs are "
     "compatible and the overlap is small.",
     "",
     "<b>Run a separate ThreadSanitizer build</b> over the "
     "concurrency tests (Module 05 §1).",
     "",
     "<b>And treat any sanitiser report as a build "
     "failure</b>, not a warning — otherwise the reports "
     "accumulate.",
   ],
   "footnote": "<b>'A test asserts the output; a sanitiser asserts the "
               "execution' is the sentence that persuades "
               "people</b> — it explains why a green suite proves "
               "less than it appears to."},

  {"t": "section", "label": "Part 4", "title": "Limits",
   "blurb": "Stated precisely."},

  {"t": "callout", "title": "A sanitiser only reports what the execution actually did",
   "kind": "The honest boundary",
   "body": ["<b>It is a dynamic technique</b>, so <b>it finds defects "
            "on the paths you executed and says nothing about the paths "
            "you did not</b> — which is why coverage "
            "(Module 08 §3) is the thing to "
            "measure.",
            "<b>And it is not a verifier.</b> <b>'The suite passes "
            "under ASan' means 'these inputs caused no detected "
            "violation'</b> — a statement about your inputs rather "
            "than about your program.",
            "<b>Which is the opposite failure mode to static "
            "analysis</b> (Module 07 §1): <b>a sanitiser "
            "has essentially no false positives and a large number of "
            "false negatives.</b>",
            "<b>So the three techniques are complementary:</b> "
            "<b>static analysis reasons about all paths imprecisely, "
            "sanitisers observe some paths precisely, and review "
            "addresses what neither can</b> "
            "(Module 11)."]},

  {"t": "bullets", "kicker": "Production", "title": "And running detection in production",
   "items": [
     "<b>The heavy sanitisers are too expensive for "
     "production</b>, but <b>hardware-assisted ASan and "
     "pointer-tagging on ARM are cheap enough</b> to deploy on a "
     "fraction of traffic.",
     "",
     "<b>A hardened allocator is the cheaper option</b> — "
     "randomised placement, guard pages, and freed-memory quarantine, "
     "at single-digit overhead.",
     "",
     "<b>UBSan's trap mode for the checks you can afford</b>, "
     "which converts undefined behaviour into a clean "
     "abort.",
     "",
     "<b>And crash reporting that you actually read</b>, because "
     "<b>a repeated crash in a parser is a defect report from a "
     "stranger</b> (CSCE 701 Module 09).",
     "",
     "<b>Which is the detection-over-prevention argument</b>, "
     "applied to memory safety.",
   ],
   "footnote": "<b>Reading your crash reports is free detection</b> "
               "— and a cluster of crashes at one parser offset is "
               "frequently somebody probing."},
 ],
 "takeaways": [
   "AddressSanitizer poisons redzones and quarantines freed memory, which "
   "is why an overflow landing inside another valid object is missed.",
   "ASan and ThreadSanitizer are incompatible and need separate builds; "
   "UBSan is cheap enough that parts of it can ship.",
   "UBSan's trap mode converts exploitable undefined behaviour into a "
   "deterministic abort at almost no cost.",
   "Fuzzing supplies the inputs and sanitisers supply the oracle — "
   "neither is nearly as effective alone.",
   "A test asserts the output and a sanitiser asserts the execution, which "
   "is why a green suite proves less than it appears to.",
   "Sanitisers have almost no false positives and many false negatives, "
   "which is the opposite profile to static analysis.",
 ],
 "notes": [
  ("h1", "1 &nbsp; AddressSanitizer"),
  ("callout", "AddressSanitizer makes out-of-bounds and use-after-free loud "
              "instead of silent",
   ["<b>It places poisoned 'redzones' around every allocation and "
    "checks every memory access against a shadow map that records which "
    "bytes are valid</b> — so <b>an access into a redzone is "
    "reported immediately, with both the allocation site and the access "
    "site located precisely</b>, which is what makes the reports "
    "actionable.",
    "<b>And it quarantines freed memory rather than returning it to "
    "the allocator for immediate reuse</b>, so <b>a use-after-free hits "
    "poisoned memory and is reported, instead of silently reading or "
    "writing somebody else's live object</b> (Module 02 &sect;2).",
    "<b>Which is precisely why its limits are what they are:</b> "
    "<b>an overflow that lands <i>inside another valid object</i> is not "
    "detected</b>, because that memory is legitimately mapped and "
    "unpoisoned — <b>so a large jump past the redzone, or an index "
    "far out of range, can be missed entirely</b> while a one-byte "
    "overflow is caught.",
    "<b>But it detects the overwhelming majority of real defects</b>, "
    "because real defects are mostly small overshoots — <b>and it "
    "requires no source changes at all</b>, only a compiler flag, which "
    "makes <b>enabling it the single highest-value action available to "
    "an existing C or C++ project</b> and the thing to do before "
    "anything else in this course."]),
  ("table", ["Sanitiser", "What it detects", "What it costs"],
   [["<b>AddressSanitizer (ASan)</b>",
     "<b>Out-of-bounds read and write, use-after-free, double free, "
     "use-after-return, and leaks.</b>",
     "<b>Roughly 2&times; time and 3&times; memory</b> — "
     "acceptable for testing, generally not for production."],
    ["<b>UndefinedBehaviorSanitizer (UBSan)</b>",
     "<b>Signed overflow, invalid shifts, misalignment, invalid casts, "
     "null dereference.</b>",
     "<b>Low — frequently under 20%</b>, and see the note."],
    ["<b>ThreadSanitizer (TSan)</b>",
     "<b>Data races</b> (Module 05 &sect;1).",
     "<b>Roughly 5 to 15&times; time</b> and substantial memory — "
     "run it over the concurrency tests specifically."],
    ["<b>MemorySanitizer (MSan)</b>",
     "<b>Reads of uninitialised memory.</b>",
     "<b>Roughly 3&times;, and it requires every dependency to be "
     "instrumented</b> — which is the practical obstacle."],
    ["<b>Hardware-assisted ASan (HWASan)</b>",
     "<b>Much the same as ASan, using pointer tagging.</b>",
     "<b>Low enough for production use on ARM</b>, which is &sect;4's "
     "opportunity."]],
   [0.24, 0.38, 0.38]),
  ("p", "<b>ASan and TSan are mutually incompatible and must be separate "
        "builds</b> — they both instrument memory access and their "
        "runtimes conflict — which means a complete pipeline has at "
        "least two instrumented configurations. <b>And UBSan's cost is "
        "low enough that parts of it ship in production in some "
        "projects</b>, which makes it a hardening measure as well as a "
        "debugging one (&sect;2)."),

  ("h1", "2 &nbsp; UndefinedBehaviorSanitizer"),
  ("ul", ["<b>Signed integer overflow</b> — which is "
          "<b>Module 03 &sect;1's canonical defect and is otherwise "
          "entirely silent</b>, since the wrapped value is a perfectly "
          "ordinary number as far as the program is concerned.",
          "<b>Shifts by more than the operand width</b>, which is "
          "undefined and produces platform-dependent nonsense — and "
          "which appears regularly in bit-manipulation code written "
          "against one compiler.",
          "<b>Misaligned and null pointer dereferences</b>, and "
          "<b>invalid casts between pointer types</b> — which is "
          "<b>Module 03 &sect;4's type confusion</b>, caught at the "
          "moment the invalid interpretation occurs.",
          "<b>Array bounds where the size is statically known</b>, and "
          "<b>invalid enum or boolean values</b> — a boolean holding "
          "something other than 0 or 1, which arises from uninitialised "
          "memory or a bad cast and then breaks every branch on it.",
          "<b>And it can be configured to trap rather than to "
          "report</b>, which <b>turns undefined behaviour into a "
          "deterministic abort</b> — a hardening measure rather than "
          "a debugging one (Module 12 &sect;2). <b>The trap mode is "
          "the underused feature:</b> "
          "<b><code>-fsanitize-trap</code> converts a class of "
          "exploitable undefined behaviour into a clean crash, at almost "
          "no runtime cost</b>, and is deployed in production by several "
          "major projects."]),

  ("break",),
  ("h1", "3 &nbsp; The pairing"),
  ("callout", "Fuzzing generates the inputs and sanitisers supply the oracle",
   ["<b>Fuzzing without a sanitiser only detects defects that actually "
    "crash</b> — and <b>a one-byte out-of-bounds read does not "
    "crash</b>, it returns whatever was there, <b>so the input that "
    "triggered it is discarded as uninteresting</b> and the defect is "
    "never found however long the campaign runs.",
    "<b>A sanitiser without fuzzing only checks the inputs your tests "
    "happen to supply</b> — which are the valid, expected, "
    "well-formed ones, <b>and are precisely not where the defects "
    "are</b> (Module 01 &sect;2's input framing).",
    "<b>Together, the fuzzer explores the input space while the "
    "sanitiser reports every violation on every path it reaches</b> "
    "— which is why <b>this specific pairing found most of the "
    "memory safety defects fixed in major open-source projects over the "
    "past decade</b>, through OSS-Fuzz and equivalent infrastructure.",
    "<b>So the recommendation is a single pipeline:</b> <b>a "
    "sanitiser-instrumented build, a coverage-guided fuzzer, a persistent "
    "corpus, and every crash minimised into a regression test</b> "
    "(Module 08 &sect;4) — four components, all free, and the "
    "combination is the state of the practice."]),
  ("ul", ["<b>Run the existing test suite under AddressSanitizer</b> "
          "— <b>which frequently finds defects on the first day</b>, "
          "in code that has passed those same tests for years without "
          "complaint.",
          "<b>Because a test asserts the <i>output</i> and a sanitiser "
          "asserts the <i>execution</i></b> — <b>so a test can pass "
          "while the program corrupts memory</b>, provided the corruption "
          "did not happen to change the answer on that input.",
          "<b>Add UBSan to the same build</b>, since the runtime costs "
          "are compatible and the detection overlap is small — so the "
          "marginal cost of the second sanitiser is close to nothing.",
          "<b>Run a separate ThreadSanitizer build</b> over the "
          "concurrency tests specifically (Module 05 &sect;1), since "
          "it cannot share a build with ASan and its cost is high enough "
          "to want targeting.",
          "<b>And treat any sanitiser report as a build failure rather "
          "than a warning</b> — <b>otherwise the reports "
          "accumulate</b> and the output becomes exactly the ignored "
          "dashboard of Module 07 &sect;4. <b>'A test asserts the "
          "output; a sanitiser asserts the execution' is the sentence that "
          "persuades people</b>, because it explains concisely why a "
          "green test suite proves considerably less than it appears "
          "to."]),

  ("h1", "4 &nbsp; Limits, and production"),
  ("callout", "A sanitiser only reports what the execution actually did",
   ["<b>It is a dynamic technique</b>, so <b>it finds defects on the "
    "paths you actually executed and says precisely nothing about the "
    "paths you did not</b> — which is exactly why <b>coverage</b> "
    "(Module 08 &sect;3) <b>is the thing to measure and to "
    "report.</b>",
    "<b>And it is emphatically not a verifier.</b> <b>'The test suite "
    "passes under AddressSanitizer' means 'these particular inputs caused "
    "no detected violation'</b> — which is a statement about your "
    "inputs rather than about your program, and Module 13 is about "
    "stating it that way.",
    "<b>Which is the opposite failure mode to static analysis</b> "
    "(Module 07 &sect;1): <b>a sanitiser has essentially no false "
    "positives — a report is a real defect — and a very large "
    "number of false negatives.</b> <b>Static analysis is the "
    "reverse.</b>",
    "<b>So the three techniques are genuinely complementary rather "
    "than redundant:</b> <b>static analysis reasons about all paths "
    "imprecisely, sanitisers observe some paths precisely, and code "
    "review addresses the design and authorisation defects that neither "
    "can see</b> (Module 11) — which is why Project 2 requires "
    "all three and Module 13 asks what the three together still "
    "miss."]),
  ("ul", ["<b>The heavy sanitisers are too expensive for production</b> "
          "at their stated costs, <b>but hardware-assisted ASan and "
          "pointer-tagging on ARM are cheap enough to deploy on a "
          "fraction of traffic</b> — which several large mobile "
          "platforms now do, and which finds defects that no test "
          "reached.",
          "<b>A hardened allocator is the cheaper and more portable "
          "option</b> — randomised placement, guard pages, "
          "freed-memory quarantine, and metadata separation, at "
          "single-digit percentage overhead (Module 02 &sect;3's "
          "allocator argument).",
          "<b>UBSan's trap mode for whichever checks you can "
          "afford</b>, which converts undefined behaviour into a clean "
          "abort rather than into exploitable behaviour (&sect;2).",
          "<b>And crash reporting that you actually read</b>, because "
          "<b>a repeated crash in a parser is a defect report from a "
          "stranger</b> — and a cluster of crashes at one parser "
          "offset is frequently somebody probing (CSCE 701 "
          "Module 09 &sect;2).",
          "<b>Which is the detection-over-prevention argument</b> "
          "(CSCE 701 Module 01 &sect;1's last row) <b>applied to "
          "memory safety</b>: you will ship defects, so arrange to hear "
          "about them. <b>Reading your crash reports is free "
          "detection</b>, and it is routinely ignored."]),
 ],
 "resources": [
   ("LLVM sanitizer documentation (free)",
    "https://clang.llvm.org/docs/AddressSanitizer.html",
    "<b>&sect;1 and &sect;2's reference</b> — what each detects, what "
    "it costs, and which combinations are incompatible."),
   ("Serebryany et al. &mdash; AddressSanitizer (free)",
    "https://www.usenix.org/conference/atc12/technical-sessions/presentation/serebryany",
    "<b>&sect;1's mechanism in the original</b> — the shadow memory "
    "design, which explains the limits."),
   ("OSS-Fuzz architecture documentation (free)",
    "https://google.github.io/oss-fuzz/architecture/",
    "<b>&sect;3's pipeline as deployed</b> — the sanitiser and fuzzer "
    "combination at scale."),
   ("Android's HWASan and memory tagging writeups (free)",
    "https://source.android.com/docs/security/test/hwasan",
    "<b>&sect;4's production detection</b> — the cost figures and the "
    "deployment strategy."),
 ],
 "exercises": [
   "<b>Enable AddressSanitizer on an existing project</b> and run its "
   "test suite.",
   "<b>Report what it found</b> in code that was passing its tests.",
   "<b>Write an overflow that ASan catches</b> and one that lands inside "
   "another object and is missed.",
   "<b>Explain the difference</b> in terms of the shadow map.",
   "<b>Enable UBSan</b> and find a signed overflow in real code.",
   "<b>Try the trap mode</b> and confirm the abort is deterministic.",
   "<b>Try to enable ASan and TSan together</b> and report what "
   "happens.",
   "<b>Fuzz a parser with and without sanitisers</b>, and compare the "
   "defect counts.",
   "<b>Make a sanitiser report fail your build</b>, and verify it "
   "does.",
   "<b>Measure the overhead</b> of each sanitiser on your own workload.",
 ],
 "selfcheck": [
   "How does AddressSanitizer work, and what follows about its "
   "limits?",
   "Name five sanitisers, what each detects, and the rough cost.",
   "Which two are incompatible, and which can ship in production?",
   "Name five things UBSan catches, and what trap mode achieves.",
   "Why does fuzzing without sanitisers miss defects?",
   "Why does a sanitiser without fuzzing miss defects?",
   "What does a test assert, and what does a sanitiser assert?",
   "What does 'the suite passes under ASan' actually mean?",
   "Contrast the false positive and negative profiles with static "
   "analysis.",
   "Give four ways to run detection in production.",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "The Secure Development Lifecycle",
 "subtitle": "Process that changes outcomes, and process that does not.",
 "question": "Which practices actually reduce defects?",
 "outcomes": [
     "Explain where in the lifecycle each practice belongs.",
     "Explain why secure defaults beat developer education.",
     "Design a security gate that does not get bypassed.",
     "Explain what to do with a vulnerability report.",
     "Assess a development process honestly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Where things belong",
   "blurb": "Earlier is cheaper, and the slogan is not the point."},

  {"t": "table", "kicker": "Lifecycle", "title": "The practice that fits each stage",
   "header": ["Stage", "The practice", "What it catches"],
   "widths": [2.4, 4.1, 5.4],
   "rows": [
     ["<b>Design</b>", "<b>Threat modelling (CSCE 701 M01)</b>", "<b>Design flaws — which no tool finds</b>"],
     ["<b>Dependency</b>", "<b>Selection and scanning (701 M08)</b>", "<b>Inherited defects and gadgets</b>"],
     ["<b>Code</b>", "<b>Safe libraries and types (M04 §4)</b>", "<b>Whole classes, by construction</b>"],
     ["<b>Commit</b>", "<b>Static analysis on the diff (M07 §4)</b>", "<b>Pattern defects, before merge</b>"],
     ["<b>Build</b>", "<b>Sanitisers and fuzzing (M08, M09)</b>", "<b>Memory and parsing defects</b>"],
     ["<b>Review</b>", "<b>Security review of risky changes (M11)</b>", "<b>Logic and authorisation defects</b>"],
     ["<b>Operate</b>", "<b>Detection and response (701 M09–10)</b>", "<b>Everything above that got through</b>"],
   ],
   "footnote": "<b>The design row is the one with no automated "
               "substitute</b> — and it is the one most often "
               "skipped, because it produces a document rather than a "
               "passing check.",
   "note": "This table is the module's practical artefact."},

  {"t": "callout", "title": "“Shift left” is right about cost and wrong as a strategy",
   "kind": "Stating it carefully",
   "body": ["<b>The cost claim is true:</b> <b>a design flaw found at "
            "design time costs a conversation, and the same flaw found "
            "after release costs a redesign plus an incident.</b>",
            "<b>But 'shift left' is frequently implemented as moving "
            "work onto developers</b> — more training, more "
            "checklists, more tools in the pipeline — <b>which "
            "spends the compliance budget</b> "
            "(CSCE 701 Module 11 §1).",
            "<b>And the practices that actually scale are the ones "
            "that require no developer effort:</b> <b>a safe default, a "
            "type that cannot be misused, a framework that escapes "
            "automatically.</b>",
            "<b>So the honest version is: move the <i>guarantee</i> "
            "left, not the <i>work</i></b> — <b>which is the "
            "distinction that separates a programme that holds from one "
            "that decays after the first deadline.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Defaults over education",
   "blurb": "The strongest result in this module."},

  {"t": "callout", "title": "A framework that makes the defect unexpressible beats any amount of training",
   "kind": "The evidence",
   "body": ["<b>Training decays, turns over with staff, and competes "
            "with everything else for attention</b> — and <b>its "
            "measured effect on defect rates is modest.</b>",
            "<b>A template engine with contextual autoescaping on by "
            "default eliminates the whole XSS class for every developer, "
            "including the one who has never heard of "
            "it</b> (Module 04).",
            "<b>And the pattern generalises:</b> <b>a query builder "
            "that cannot concatenate, a path type that cannot escape its "
            "root, an HTTP client that cannot reach internal addresses, "
            "a serialiser that cannot name a class.</b>",
            "<b>Which is CSCE 701 Module 11 §3's "
            "defaults argument, and CSCE 711 Module 01 §4's "
            "misuse-resistant API argument</b> — <b>three courses "
            "converging on one conclusion, which is worth "
            "noticing.</b>"]},

  {"t": "bullets", "kicker": "Building it", "title": "How to build a safe-by-default layer",
   "items": [
     "<b>Find the defect class you keep fixing</b>, and ask what "
     "interface would make it unexpressible.",
     "",
     "<b>Provide that interface, and make it the easiest "
     "path</b> — because <b>a safe API that is harder to use "
     "than the unsafe one loses</b>.",
     "",
     "<b>Then make the unsafe path hard to reach:</b> a lint rule "
     "banning it, a private constructor, or a deprecation with a "
     "migration.",
     "",
     "<b>And add a static analysis rule to prevent new call "
     "sites</b> (Module 07 §4), which is what makes "
     "the migration finish.",
     "",
     "<b>Which converts one fix into a permanent property of the "
     "codebase.</b>",
   ],
   "footnote": "<b>'Make it the easiest path' is the step that "
               "decides it</b> — and it is a usability requirement "
               "rather than a security one."},

  {"t": "section", "label": "Part 3", "title": "Gates",
   "blurb": "Which get bypassed unless designed not to be."},

  {"t": "bullets", "kicker": "Gates", "title": "Designing a gate that survives a deadline",
   "items": [
     "<b>Fast.</b> <b>A check that adds twenty minutes to every "
     "change will be skipped</b> — which is "
     "CSCE 701 Module 11 §4's friction "
     "question.",
     "",
     "<b>Scoped to new code.</b> <b>Baseline the existing "
     "findings</b> (Module 07 §3), so the gate never "
     "demands a cleanup project.",
     "",
     "<b>Specific.</b> <b>A finding that names the line and the "
     "fix gets fixed</b>; one that names a risk category gets "
     "dismissed.",
     "",
     "<b>With a documented, auditable override</b> — because "
     "<b>a gate with no override gets removed entirely the first time "
     "it blocks something urgent.</b>",
     "",
     "<b>And owned</b>, so that the false positives get fixed "
     "rather than suppressed.",
   ],
   "footnote": "<b>The override is counter-intuitive and "
               "essential:</b> an override that is logged and reviewed "
               "preserves the gate, and no override destroys it."},

  {"t": "section", "label": "Part 4", "title": "Receiving reports",
   "blurb": "Which is a process, not an inbox."},

  {"t": "callout", "title": "Make it easy to report a vulnerability to you",
   "kind": "The obligation and the self-interest",
   "body": ["<b>Publish a security contact and a policy</b> — "
            "<b><code>security.txt</code>, or a documented address</b> "
            "— because a researcher who cannot find where to report "
            "will publish instead, or give up.",
            "<b>Acknowledge quickly, and state a timeline you will "
            "meet</b> — <b>the commonest complaint from reporters "
            "is silence</b>, not disagreement.",
            "<b>Fix it, credit the reporter, and publish an "
            "advisory</b> with enough detail for your users to assess "
            "their exposure (CSCE 701 Module 08 "
            "§4).",
            "<b>And never threaten a good-faith reporter</b> — "
            "<b>which has repeatedly converted a private report into a "
            "public incident</b>, and is the single worst available "
            "response."]},

  {"t": "bullets", "kicker": "Disclosing", "title": "And when you are the reporter",
   "items": [
     "<b>Report privately first</b>, with enough detail to "
     "reproduce, and a clear statement of impact.",
     "",
     "<b>Offer a reasonable timeline</b> — ninety days is the "
     "common norm — and <b>say what you will do when it "
     "expires.</b>",
     "",
     "<b>Coordinate publication</b>, so users have a fix available "
     "when they learn of the problem.",
     "",
     "<b>And never test against systems you do not own</b> "
     "(Module 01 §4), which is where good intentions "
     "become unlawful.",
     "",
     "<b>This is Project 2's professional requirement</b>, and it "
     "is graded.",
   ],
   "footnote": "<b>'Report privately, with a timeline, and "
               "coordinate'</b> is the whole of responsible disclosure "
               "— and the timeline is what makes it responsible "
               "rather than indefinite."},
 ],
 "takeaways": [
   "The design stage is the one with no automated substitute, and the one "
   "most often skipped because it produces a document.",
   "'Shift left' is right about cost and wrong as a strategy — move "
   "the guarantee left, not the work.",
   "A template engine with autoescaping on by default eliminates XSS for "
   "every developer, including one who has never heard of it.",
   "A safe API that is harder to use than the unsafe one loses, so making "
   "it the easiest path is the deciding step.",
   "A gate with no override gets removed entirely the first time it blocks "
   "something urgent.",
   "The commonest complaint from vulnerability reporters is silence, not "
   "disagreement.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Where each practice belongs"),
  ("table", ["Stage", "The practice", "What it catches"],
   [["<b>Design</b>",
     "<b>Threat modelling</b> (CSCE 701 Module 01).",
     "<b>Design flaws — which no tool finds</b>, because a tool does "
     "not know what the system was for. See the note."],
    ["<b>Dependency selection</b>",
     "<b>Adoption review and continuous scanning</b> (CSCE 701 "
     "Module 08).",
     "<b>Inherited defects, and deserialisation gadgets</b> "
     "(Module 06 &sect;1)."],
    ["<b>Writing code</b>",
     "<b>Safe libraries and parse-don't-validate types</b> "
     "(Module 04 &sect;4).",
     "<b>Whole classes, by construction</b> — which is &sect;2's "
     "argument and the highest-leverage row."],
    ["<b>Commit</b>",
     "<b>Static analysis on the diff</b> (Module 07 &sect;4).",
     "<b>Pattern-matchable defects, before merge</b>, where the author "
     "is still thinking about the code."],
    ["<b>Build and test</b>",
     "<b>Sanitisers and fuzzing</b> (Modules 08 and 09).",
     "<b>Memory safety and parsing defects</b> — the pairing of "
     "Module 09 &sect;3."],
    ["<b>Review</b>",
     "<b>Security review of the risky changes</b> (Module 11).",
     "<b>Logic and authorisation defects</b>, which are exactly what "
     "the tooling cannot see."],
    ["<b>Operate</b>",
     "<b>Detection and incident response</b> (CSCE 701 "
     "Modules 09 and 10).",
     "<b>Everything above that got through</b> — and some "
     "always does."]],
   [0.16, 0.34, 0.50]),
  ("p", "<b>The design row is the one with no automated "
        "substitute</b> — and <b>it is the one most often skipped, "
        "because it produces a document rather than a passing check</b>, "
        "which makes it invisible in every dashboard. <b>Which is "
        "CSCE 701 Module 12's measurement problem deciding a process "
        "question</b>: the practice with the highest value is the one "
        "hardest to show credit for."),
  ("callout", "“Shift left” is right about cost and wrong as a "
              "strategy",
   ["<b>The cost claim is simply true:</b> <b>a design flaw found at "
    "design time costs a conversation, and the same flaw found after "
    "release costs a redesign, a migration, and possibly an "
    "incident.</b> Nobody disputes this.",
    "<b>But 'shift left' is frequently implemented as moving work onto "
    "developers</b> — more training, more checklists, more tools in "
    "the pipeline, more questionnaires — <b>which spends the "
    "compliance budget</b> (CSCE 701 Module 11 &sect;1) <b>and "
    "therefore reduces compliance with whatever mattered most.</b>",
    "<b>And the practices that actually scale are precisely the ones "
    "that require no developer effort at all:</b> <b>a safe default, a "
    "type that cannot be misused, a framework that escapes "
    "automatically</b> (&sect;2) — none of which appear in a "
    "training completion metric.",
    "<b>So the honest version is: move the <i>guarantee</i> left, not "
    "the <i>work</i></b> — <b>which is the distinction that "
    "separates a security programme that holds up from one that decays "
    "quietly after the first serious deadline</b>, and it is worth "
    "stating in exactly those words when the programme is being "
    "designed."]),

  ("h1", "2 &nbsp; Defaults over education"),
  ("callout", "A framework that makes the defect unexpressible beats any "
              "amount of training",
   ["<b>Training decays, turns over with staff, and competes with "
    "everything else for attention</b> — and <b>its measured effect "
    "on defect rates is modest</b>, which is an uncomfortable finding "
    "that the industry has largely declined to act on "
    "(CSCE 701 Module 11 &sect;2's parallel with phishing "
    "training).",
    "<b>A template engine with contextual autoescaping enabled by "
    "default eliminates the entire cross-site scripting class for every "
    "developer on the team, including the one who has never heard of "
    "it</b> (Module 04) — and it keeps working when that "
    "developer leaves.",
    "<b>And the pattern generalises widely:</b> <b>a query builder "
    "that cannot concatenate strings into SQL, a path type that cannot "
    "escape its root directory, an HTTP client that refuses internal "
    "addresses (Module 06 &sect;3), a serialiser that cannot name a "
    "class to construct (Module 06 &sect;1).</b>",
    "<b>Which is CSCE 701 Module 11 &sect;3's defaults argument "
    "and CSCE 711 Module 01 &sect;4's misuse-resistant API "
    "argument</b> — <b>three courses in one semester converging "
    "independently on the same conclusion, which is worth noticing</b> "
    "and is the strongest single result in this semester."]),
  ("ul", ["<b>Find the defect class you keep fixing</b> — which "
          "your own incident and review history already tells you — "
          "<b>and ask what interface would make it unexpressible.</b>",
          "<b>Provide that interface, and make it the easiest "
          "path</b> — because <b>a safe API that is harder to use "
          "than the unsafe one loses</b>, every time, under deadline. "
          "<b>This is the step that decides the outcome</b>, and <b>it "
          "is a usability requirement rather than a security one.</b>",
          "<b>Then make the unsafe path hard to reach:</b> a lint rule "
          "banning it, a private constructor, a deprecation warning with "
          "a documented migration, or removal from the public API "
          "surface.",
          "<b>And add a static analysis rule preventing new call "
          "sites</b> (Module 07 &sect;4) — <b>which is what makes "
          "the migration actually finish</b>, rather than stalling at "
          "ninety percent with the remaining call sites permanently "
          "exempt.",
          "<b>Which converts one fix into a permanent property of the "
          "codebase</b> — and is the mechanism by which a security "
          "programme accumulates rather than merely maintaining. "
          "<b>Every defect you fix is an opportunity to do this once, "
          "and the opportunity expires when attention moves on.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Gates"),
  ("ul", ["<b>Fast.</b> <b>A check that adds twenty minutes to every "
          "change will be skipped</b>, worked around, or disabled — "
          "which is CSCE 701 Module 11 &sect;4's friction question, "
          "and the answer is measured in seconds rather than "
          "principles.",
          "<b>Scoped to new code.</b> <b>Baseline the existing "
          "findings</b> (Module 07 &sect;3), <b>so the gate never "
          "demands a cleanup project as the price of enabling it</b> "
          "— which is the single commonest reason a gate is never "
          "turned on.",
          "<b>Specific.</b> <b>A finding that names the line and the "
          "fix gets fixed</b>; <b>one that names a risk category gets "
          "dismissed</b>, because the author cannot act on it and has "
          "other work.",
          "<b>With a documented, auditable override</b> — because "
          "<b>a gate with no override gets removed entirely the first "
          "time it blocks something genuinely urgent</b>, and then you "
          "have neither the gate nor the override.",
          "<b>And owned</b>, so that false positives get fixed in the "
          "rule rather than suppressed in the code — which is the "
          "difference between a gate that improves and one that decays "
          "(Module 07 &sect;4). <b>The override is "
          "counter-intuitive and essential:</b> <b>an override that is "
          "logged and periodically reviewed preserves the gate, and no "
          "override destroys it</b>, which is a general lesson about "
          "controls and people."]),

  ("h1", "4 &nbsp; Receiving and making reports"),
  ("callout", "Make it easy to report a vulnerability to you",
   ["<b>Publish a security contact and a disclosure policy</b> — "
    "<b>a <code>security.txt</code> file, or a documented address on your "
    "site</b> — because <b>a researcher who cannot find where to "
    "report will publish instead, or give up</b>, and neither outcome is "
    "one you wanted.",
    "<b>Acknowledge quickly, and state a timeline you will actually "
    "meet</b> — <b>the commonest complaint from reporters is "
    "silence</b>, not disagreement about severity, and silence is what "
    "converts a cooperative reporter into an adversarial one.",
    "<b>Fix it, credit the reporter, and publish an advisory</b> with "
    "enough detail for your users to assess their own exposure "
    "(CSCE 701 Module 08 &sect;4's advisory response depends on "
    "somebody having written one).",
    "<b>And never threaten a good-faith reporter</b> — <b>which "
    "has repeatedly converted a quiet private report into a public "
    "incident with far worse coverage than the vulnerability "
    "warranted</b>, and is the single worst available response. It is "
    "also, on the record, ineffective at suppressing anything."]),
  ("ul", ["<b>Report privately first</b>, with enough detail to "
          "reproduce reliably, and a clear statement of the impact you "
          "established (Module 01 &sect;3's honest form).",
          "<b>Offer a reasonable timeline</b> — ninety days is the "
          "common norm — and <b>say what you will do when it "
          "expires</b>, so the maintainer can plan rather than guess.",
          "<b>Coordinate publication</b>, so that users have a fix "
          "available at the moment they learn there is a problem — "
          "which is the entire point of coordination.",
          "<b>And never test against systems you do not own</b> "
          "(Module 01 &sect;4) — <b>which is precisely where good "
          "intentions become unlawful</b>, and where a finding you cannot "
          "lawfully have obtained becomes a finding you cannot report.",
          "<b>This is Project 2's professional requirement, and it is "
          "graded</b> as an obligation rather than a courtesy. "
          "<b>'Report privately, with a timeline, and coordinate "
          "publication' is the whole of responsible disclosure</b> — "
          "and <b>the timeline is what makes it responsible rather than "
          "indefinite</b>, since a report with no deadline can be ignored "
          "forever at the users' expense."]),
 ],
 "resources": [
   ("Google &mdash; Building Secure and Reliable Systems, the "
    "development chapters (free PDF)",
    "https://sre.google/books/building-secure-reliable-systems/",
    "<b>&sect;1 and &sect;2, free in full</b> — and the "
    "safe-by-construction argument is made better here than anywhere "
    "else."),
   ("Microsoft SDL, and the SAMM maturity model (free)",
    "https://www.microsoft.com/en-us/securityengineering/sdl/",
    "<b>&sect;1 as published frameworks</b> — useful for structure, "
    "and read &sect;1's callout before adopting wholesale."),
   ("security.txt (RFC 9116) (free)",
    "https://securitytxt.org/",
    "<b>&sect;4's first step</b>, which takes ten minutes and is still "
    "missing from most sites."),
   ("CERT Guide to Coordinated Vulnerability Disclosure (free)",
    "https://certcc.github.io/CERT-Guide-to-CVD/",
    "<b>&sect;4 from both sides</b> — the obligations of reporter and "
    "maintainer, with the hard cases discussed."),
 ],
 "exercises": [
   "<b>Map your own project's practices</b> onto Part 1's seven "
   "stages, and find the empty rows.",
   "<b>Determine whether you threat model at all</b>, and what replaced "
   "it if not.",
   "<b>Distinguish three practices that move work left</b> from three "
   "that move the guarantee left.",
   "<b>Find the defect class you keep fixing</b>, from your own history.",
   "<b>Design the interface</b> that would make it unexpressible.",
   "<b>Make the unsafe path harder to reach</b>, and add the lint "
   "rule.",
   "<b>Time your slowest security gate</b> and decide whether it will be "
   "skipped.",
   "<b>Add an auditable override</b> to a gate that lacks one.",
   "<b>Publish a <code>security.txt</code></b> for a project you "
   "maintain.",
   "<b>Write the report</b> you would send for a defect you found, in "
   "full.",
 ],
 "selfcheck": [
   "Give the seven stages and the practice at each.",
   "Which row has no automated substitute, and why is it skipped?",
   "What is right and wrong about 'shift left'?",
   "State the honest version in one sentence.",
   "Why do defaults beat training, and give four examples.",
   "Give the four steps to build a safe-by-default layer.",
   "Which step decides the outcome, and what kind of requirement is "
   "it?",
   "Give five properties of a gate that survives, and why the override "
   "matters.",
   "Give four things to do when receiving a report.",
   "Give the three elements of responsible disclosure.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Code Review for Security",
 "subtitle": "The only method that finds design and logic defects.",
 "question": "What do you read, and in what order?",
 "outcomes": [
     "Choose what to review, by risk.",
     "Apply a systematic reading method.",
     "Explain what review finds that tooling cannot.",
     "Review a diff for security specifically.",
     "Write a finding that gets fixed.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Choosing",
   "blurb": "Because you cannot read everything."},

  {"t": "bullets", "kicker": "Priority", "title": "What to review, in order of yield",
   "items": [
     "<b>Anything that parses untrusted input</b> — the "
     "highest concentration of memory and logic defects in any "
     "codebase.",
     "",
     "<b>Authentication and authorisation code</b>, and <b>every "
     "place that decides whether an action is permitted</b> "
     "(CSCE 701 Module 03) — because tooling finds none of "
     "this.",
     "",
     "<b>Anything that runs with elevated privilege</b>, or "
     "crosses a trust boundary "
     "(Module 06 §4).",
     "",
     "<b>Cryptographic use</b>, against "
     "CSCE 711 Module 11's five checks — which are "
     "mechanical and high-yield.",
     "",
     "<b>And the code nobody understands</b> — old, "
     "undocumented, and still reachable, which is where the assumptions "
     "have rotted (Module 01 §1).",
   ],
   "footnote": "<b>'Parses untrusted input' and 'decides whether an "
               "action is permitted' are the two highest-yield "
               "categories</b>, and they fail in completely different "
               "ways."},

  {"t": "callout", "title": "Review what tooling cannot see, and let tooling have the rest",
   "kind": "How to allocate the attention",
   "body": ["<b>A reviewer spending time on patterns a linter "
            "finds is wasting the scarcest resource in the "
            "process</b> — and will be less careful by the time they "
            "reach the part that needed them.",
            "<b>So automate the mechanical checks</b> "
            "(Module 07) <b>and spend review on the three things only a "
            "person can assess:</b>",
            "<b>Is the design right? Is the authorisation complete? "
            "And does this code do what it claims?</b> — <b>none of "
            "which a tool can evaluate</b>, because none is expressible "
            "without knowing the intent.",
            "<b>Which makes review the complement rather than the "
            "backstop</b> — and is why Project 2 requires it "
            "alongside the tooling rather than after it."]},

  {"t": "section", "label": "Part 2", "title": "Reading",
   "blurb": "A method, rather than scanning."},

  {"t": "code", "kicker": "Method", "title": "How to read a component adversarially",
   "lang": "text", "code": """
  1. UNDERSTAND THE INTENDED BEHAVIOUR FIRST
     you cannot spot a deviation from a specification
     you do not have. If none exists, reconstruct it.

  2. FIND THE ENTRY POINTS
     and rank them by who can reach them

  3. FOR EACH, TRACE TO THE DANGEROUS OPERATIONS
     allocation, indexing, copying, interpretation,
     privilege decisions (Module 01 section 2)

  4. AT EVERY STEP, ASK "WHAT IS ASSUMED HERE"
     and then whether it is guaranteed on THIS path

  5. THEN READ THE ERROR PATHS SPECIFICALLY
     they are less tested, less reviewed, and they free
     things, skip checks, and return early

  6. AND READ THE DIFF'S CONTEXT, NOT JUST THE DIFF
     a correct change can break a caller's assumption
""",
   "caption": "<b>Step 5 is the highest-yield single habit</b> — "
              "error paths hold a disproportionate share of defects "
              "because nothing exercises them.",
   "note": "Error paths are where the leaks, double frees, and skipped "
           "checks live."},

  {"t": "bullets", "kicker": "Questions", "title": "The questions that find real defects",
   "items": [
     "<b>'What happens if this is zero, negative, empty, maximal, "
     "or absent?'</b> — five cases, and one of them is usually "
     "unhandled.",
     "",
     "<b>'Who checked this, and can this function be called "
     "without that check?'</b> — which is "
     "Module 01 §2's step 4.",
     "",
     "<b>'What happens if this fails?'</b> — and whether the "
     "caller can distinguish failure from success.",
     "",
     "<b>'Who owns this memory, and when is it freed?'</b> "
     "— asked of every pointer that crosses a function "
     "boundary.",
     "",
     "<b>And 'is this check in the right place?'</b> — a "
     "check in the client is not a check "
     "(CSCE 701 Module 03 §3).",
   ],
   "footnote": "<b>The zero-negative-empty-maximal-absent question is "
               "mechanical and finds a great deal</b> — it is worth "
               "asking of every numeric and every collection "
               "parameter."},

  {"t": "section", "label": "Part 3", "title": "What only review finds",
   "blurb": "The three categories."},

  {"t": "table", "kicker": "Coverage", "title": "The three techniques, and what each sees",
   "header": ["Defect kind", "Static", "Fuzzing", "Review"],
   "widths": [4.0, 2.2, 2.2, 2.4],
   "rows": [
     ["<b>Memory safety</b>", "<b>Partly</b>", "<b>Yes</b>", "<b>Partly</b>"],
     ["<b>Injection</b>", "<b>Yes</b>", "<b>Sometimes</b>", "<b>Yes</b>"],
     ["<b>Integer defects</b>", "<b>Yes</b>", "<b>Yes</b>", "<b>Partly</b>"],
     ["<b>Concurrency</b>", "<b>Poorly</b>", "<b>Poorly</b>", "<b>Partly</b>"],
     ["<b>Missing authorisation</b>", "<b>No</b>", "<b>No</b>", "<b>Yes</b>"],
     ["<b>Logic and design flaws</b>", "<b>No</b>", "<b>No</b>", "<b>Yes</b>"],
   ],
   "footnote": "<b>The last two rows are why review cannot be "
               "replaced</b> — and they are not minor categories; "
               "missing authorisation is among the most common severe "
               "findings in real assessments.",
   "note": "This table justifies the whole module."},

  {"t": "section", "label": "Part 4", "title": "Writing it up",
   "blurb": "So that it gets fixed."},

  {"t": "callout", "title": "A finding gets fixed when it is specific, reachable, and actionable",
   "kind": "The form to use",
   "body": ["<b>The location, precisely</b> — file and line, and "
            "the specific condition rather than 'input "
            "validation is weak here'.",
            "<b>The path from untrusted input</b>, concretely "
            "— <b>because a finding whose reachability is "
            "unestablished will be disputed and deferred</b>, "
            "correctly.",
            "<b>The impact you actually established</b>, in "
            "Module 01 §3's honest form — not the "
            "worst case you can imagine.",
            "<b>And a suggested fix</b>, ideally at the level that "
            "prevents recurrence (Module 10 §2) rather than "
            "only this instance."]},

  {"t": "bullets", "kicker": "Practice", "title": "And the review culture that makes this work",
   "items": [
     "<b>Review the change, not the author</b> — which is "
     "CSCE 701 Module 10 §4's blamelessness, before "
     "the incident.",
     "",
     "<b>Ask questions rather than assert defects</b> when you are "
     "unsure, because <b>you are reading without the context the "
     "author has.</b>",
     "",
     "<b>And accept that you will miss things.</b> <b>Review "
     "finds a fraction of what is there</b>, and a programme that "
     "treats it as a guarantee has misplaced its confidence "
     "(Module 13).",
     "",
     "<b>Record what you looked for</b>, so the next reviewer does "
     "not repeat it and the claim is checkable.",
     "",
     "<b>Which is what makes a review an assessment rather than an "
     "opinion.</b>",
   ],
   "footnote": "<b>Recording what you looked for is the practice that "
               "turns review into evidence</b> — and it is what "
               "Module 13 §1 asks you to report."},
 ],
 "takeaways": [
   "'Parses untrusted input' and 'decides whether an action is permitted' "
   "are the two highest-yield review categories.",
   "Review what tooling cannot see — design, authorisation "
   "completeness, and whether the code does what it claims.",
   "Understand the intended behaviour first, because you cannot spot a "
   "deviation from a specification you do not have.",
   "Read the error paths specifically: they are less tested, less "
   "reviewed, and they free things and return early.",
   "Missing authorisation and logic flaws are found by review and by "
   "neither static analysis nor fuzzing.",
   "A finding whose reachability is unestablished will be disputed and "
   "deferred, correctly.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Choosing what to review"),
  ("ul", ["<b>Anything that parses untrusted input</b> — <b>the "
          "highest concentration of both memory and logic defects in any "
          "codebase</b>, and the place where Modules 02 through 06 all "
          "apply at once.",
          "<b>Authentication and authorisation code</b>, and <b>every "
          "place that decides whether an action is permitted</b> "
          "(CSCE 701 Module 03) — <b>because the tooling finds "
          "none of this</b> (&sect;3's table), so review is not a "
          "second opinion here but the only opinion.",
          "<b>Anything that runs with elevated privilege</b>, or that "
          "crosses a trust boundary (Module 06 &sect;4) — where "
          "the consequence of a defect is multiplied by the context "
          "(Module 01 &sect;3).",
          "<b>Cryptographic use</b>, against CSCE 711 "
          "Module 11's five mechanical checks — a non-constant-time "
          "comparison, a caller-supplied nonce, a distinguishable error, "
          "a doubled-purpose key, and parsing before verification. "
          "<b>Five greps, and high yield.</b>",
          "<b>And the code nobody understands</b> — old, "
          "undocumented, written for a different context, and still "
          "reachable — <b>which is where the assumptions have "
          "rotted</b> (Module 01 &sect;1's last cause). <b>'Parses "
          "untrusted input' and 'decides whether an action is permitted' "
          "are the two highest-yield categories</b>, and they <b>fail in "
          "completely different ways</b>, which is why a reviewer needs "
          "both halves of this course."]),
  ("callout", "Review what tooling cannot see, and let tooling have the rest",
   ["<b>A reviewer spending their attention on patterns a linter finds "
    "is wasting the scarcest resource in the entire process</b> — "
    "and <b>will be measurably less careful by the time they reach the "
    "part that actually needed a person</b>, because attention is "
    "finite within a single review.",
    "<b>So automate the mechanical checks</b> (Module 07) <b>and "
    "spend the review on the three things only a person can "
    "assess:</b>",
    "<b>Is the design right? Is the authorisation complete? And does "
    "this code do what it claims to do?</b> — <b>none of which a "
    "tool can evaluate</b>, because none of the three is expressible "
    "without knowing the intent, and intent is not in the source.",
    "<b>Which makes review the <i>complement</i> to tooling rather "
    "than its backstop</b> — and is precisely why Project 2 requires "
    "review alongside the automated techniques rather than as a final "
    "pass over whatever they flagged."]),

  ("h1", "2 &nbsp; Reading"),
  ("code", """1. UNDERSTAND THE INTENDED BEHAVIOUR FIRST
   you cannot spot a deviation from a specification you
   do not have. If none exists, reconstruct one from
   the tests and the callers before reading further.

2. FIND THE ENTRY POINTS
   and rank them by who can reach them (pre-auth
   first -- Module 01 section 3)

3. FOR EACH, TRACE TO THE DANGEROUS OPERATIONS
   allocation, indexing, copying, interpretation by
   something downstream, and privilege decisions
   (Module 01 section 2's four-step method)

4. AT EVERY STEP, ASK "WHAT IS ASSUMED HERE"
   and then whether it is guaranteed on THIS path

5. THEN READ THE ERROR PATHS SPECIFICALLY
   they are less tested, less reviewed, and they free
   things, skip checks, and return early

6. AND READ THE DIFF'S CONTEXT, NOT JUST THE DIFF
   a locally correct change can break a caller's
   assumption that is not visible in the diff"""),
  ("p", "<b>Step 5 is the highest-yield single habit in this "
        "module.</b> <b>Error paths hold a disproportionate share of "
        "defects because essentially nothing exercises them</b> — "
        "they are rarely unit tested, rarely hit in integration, almost "
        "never fuzzed into, and they perform exactly the operations that "
        "go wrong: freeing partially constructed objects, returning before "
        "a check, leaving a lock held, logging the thing that should not be "
        "logged. <b>Reading only the error paths of a component is a "
        "productive half-hour.</b>"),
  ("ul", ["<b>'What happens if this is zero, negative, empty, maximal, "
          "or absent?'</b> — <b>five cases, and one of them is "
          "usually unhandled.</b> Mechanical, and it finds a great "
          "deal.",
          "<b>'Who checked this, and can this function be called "
          "without that check?'</b> — which is <b>Module 01 "
          "&sect;2's step 4</b>, and the answer requires looking at the "
          "call graph rather than at the function.",
          "<b>'What happens if this fails?'</b> — and "
          "specifically <b>whether the caller can distinguish failure "
          "from success</b>, since an ignored error return is how a great "
          "many security checks come to be skipped.",
          "<b>'Who owns this memory, and when is it freed?'</b> "
          "— asked of every pointer that crosses a function boundary "
          "(Module 02 &sect;2's unclear-ownership pattern).",
          "<b>And 'is this check in the right place?'</b> — "
          "because <b>a check in the client is not a check</b> "
          "(CSCE 701 Module 03 &sect;3's chokepoint argument), and a "
          "check in the wrong layer is a check an attacker simply does not "
          "execute. <b>The zero-negative-empty-maximal-absent question "
          "is worth asking of every numeric and every collection "
          "parameter you encounter.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; What only review finds"),
  ("table", ["Defect kind", "Static analysis", "Fuzzing", "Review"],
   [["<b>Memory safety</b>", "<b>Partly</b> (Module 07 &sect;2)",
     "<b>Yes</b> — with sanitisers (Module 09 &sect;3)",
     "<b>Partly</b>"],
    ["<b>Injection</b>", "<b>Yes</b>", "<b>Sometimes</b>", "<b>Yes</b>"],
    ["<b>Integer defects</b>", "<b>Yes</b>", "<b>Yes</b>",
     "<b>Partly</b>"],
    ["<b>Concurrency</b>", "<b>Poorly</b>", "<b>Poorly</b>",
     "<b>Partly</b> — and it is the best of the three "
     "(Module 05 &sect;4)"],
    ["<b>Missing authorisation</b>", "<b>No</b>", "<b>No</b>",
     "<b>Yes</b>"],
    ["<b>Logic and design flaws</b>", "<b>No</b>", "<b>No</b>",
     "<b>Yes</b>"]],
   [0.34, 0.21, 0.21, 0.24]),
  ("p", "<b>The last two rows are why review cannot be "
        "replaced</b> — and <b>they are not minor categories</b>. "
        "<b>Missing authorisation is among the most common severe findings "
        "in real assessments</b>, and a design flaw can make a system "
        "insecure while every line of its code is individually "
        "correct. <b>So a programme consisting entirely of tooling has a "
        "structural blind spot covering two of the six rows</b>, and no "
        "amount of additional tooling closes it — which is this "
        "table's argument and the justification for the module."),

  ("h1", "4 &nbsp; Writing up a finding"),
  ("callout", "A finding gets fixed when it is specific, reachable, and "
              "actionable",
   ["<b>The location, precisely</b> — file and line, and the "
    "specific condition under which the defect occurs, <b>rather than "
    "'input validation is weak in this module'</b>, which cannot be acted "
    "on and will not be.",
    "<b>The path from untrusted input</b>, stated concretely — "
    "<b>because a finding whose reachability is unestablished will be "
    "disputed and deferred</b>, and <b>that is the correct response to "
    "it</b> (Module 01 &sect;1's three requirements). Establishing "
    "reachability is your job, not the maintainer's.",
    "<b>The impact you actually established</b>, in Module 01 "
    "&sect;3's honest form — <b>not the worst case you can "
    "imagine</b>, which costs you credibility on the next finding and "
    "misdirects the triage.",
    "<b>And a suggested fix</b>, ideally <b>at the level that prevents "
    "recurrence</b> (Module 10 &sect;2's interface change) <b>rather "
    "than only this instance</b> — which is what turns a finding "
    "into a durable improvement and is what Project 1's three-level fix "
    "exercise was training."]),
  ("ul", ["<b>Review the change, not the author</b> — which is "
          "<b>CSCE 701 Module 10 &sect;4's blamelessness applied "
          "before the incident rather than after it</b>, and it has the "
          "same justification: a blaming review process produces "
          "defensive authors and smaller, less honest changes.",
          "<b>Ask questions rather than assert defects when you are "
          "unsure</b>, because <b>you are reading without the context the "
          "author has</b> — and a question costs nothing while a "
          "wrong assertion costs credibility you will need later.",
          "<b>And accept that you will miss things.</b> <b>Review "
          "finds a fraction of what is present</b> — the measured "
          "rates are sobering — and <b>a programme that treats it as "
          "a guarantee has misplaced its confidence</b> "
          "(Module 13).",
          "<b>Record what you looked for</b>, so that the next reviewer "
          "does not repeat the same pass and so that <b>the claim about "
          "what was reviewed is checkable</b> by somebody else.",
          "<b>Which is what makes a review an assessment rather than an "
          "opinion.</b> <b>Recording what you looked for is the practice "
          "that turns review into evidence</b> — and it is exactly "
          "what Module 13 &sect;1 asks you to report, and what "
          "Project 2 grades."]),
 ],
 "resources": [
   ("Dowd, McDonald & Schuh, chapters 1 through 4",
    "https://www.oreilly.com/library/view/the-art-of/0321444426/",
    "<b>&sect;1 and &sect;2's method</b> — the most complete "
    "treatment of adversarial code reading in print. Library copy."),
   ("Google's code review developer guide (free)",
    "https://google.github.io/eng-practices/review/",
    "<b>&sect;4's culture</b>, from a very large practice — not "
    "security-specific, and the right foundation for it."),
   ("OWASP Code Review Guide (free)",
    "https://owasp.org/www-project-code-review-guide/",
    "<b>&sect;1 and &sect;2 as a checklist</b> — useful for "
    "completeness, and no substitute for &sect;2's method."),
   ("Mozilla and Chromium security review notes (free)",
    "https://chromium.googlesource.com/chromium/src/+/main/docs/security/",
    "<b>&sect;1's prioritisation in practice</b> — how large "
    "projects decide what gets a security review at all."),
 ],
 "exercises": [
   "<b>Rank five components of your own project</b> by Part 1's "
   "yield order.",
   "<b>List the mechanical checks</b> you should automate rather than "
   "review.",
   "<b>Reconstruct the intended behaviour</b> of an undocumented "
   "component.",
   "<b>Apply Part 2's six steps</b> to one parser, and record what "
   "you found.",
   "<b>Read only the error paths</b> of one component, and report the "
   "yield.",
   "<b>Ask the five-case question</b> of every parameter in one "
   "module.",
   "<b>Find one check that can be bypassed</b> by a different call "
   "path.",
   "<b>Find one check in the client</b> that is not enforced on the "
   "server.",
   "<b>Write up one finding</b> in Part 4's form.",
   "<b>Record what you looked for and did not find</b>, for Project "
   "2.",
 ],
 "selfcheck": [
   "Give the five review priorities and the two highest-yield "
   "categories.",
   "Why should a reviewer not check what a linter checks?",
   "What three things can only a person assess?",
   "Give Part 2's six steps, and say which habit yields most.",
   "Why are error paths disproportionately defective?",
   "Give the five questions that find real defects.",
   "Why is a check in the client not a check?",
   "Which defect kinds are found only by review?",
   "Give the four components of a finding that gets fixed.",
   "Why record what you looked for?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Exploit Mitigations",
 "subtitle": "What to do when the defect is already shipped.",
 "question": "The bug exists. Why is it hard to exploit?",
 "outcomes": [
     "Explain each mitigation and what it stops.",
     "Explain how each has been bypassed.",
     "Explain the cost of each.",
     "Explain compiler hardening you should already enable.",
     "Assess a binary's mitigations.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The strategy",
   "blurb": "Raise the cost, since the defects remain."},

  {"t": "callout", "title": "Mitigations do not fix defects; they make exploitation expensive and unreliable",
   "kind": "The honest framing",
   "body": ["<b>Every mitigation in this module leaves the defect "
            "present</b> — the overflow still overflows — "
            "<b>and makes the step from defect to control of execution "
            "harder.</b>",
            "<b>Which is worth a great deal.</b> <b>An exploit that "
            "requires an information leak, works one time in ten, and "
            "breaks on the next release is a very different "
            "proposition</b> from one that works reliably.",
            "<b>And it is worth being clear about the "
            "arithmetic:</b> <b>mitigations shift effort from the "
            "defender to the attacker</b>, which is the opposite "
            "direction to most of CSCE 701 Module 01's "
            "asymmetry.",
            "<b>But none of them is a substitute for not having the "
            "defect</b> — <b>and every one has been bypassed</b>, "
            "which Part 2 covers rather than omits."]},

  {"t": "section", "label": "Part 2", "title": "The mitigations",
   "blurb": "What each stops, and how each is bypassed."},

  {"t": "table", "kicker": "Mitigations", "title": "The standard set",
   "header": ["Mitigation", "Stops", "Bypassed by"],
   "widths": [2.8, 3.9, 4.9],
   "rows": [
     ["<b>Stack canary</b>", "<b>Sequential stack overflow reaching the return address</b>", "<b>Leaking the canary; non-sequential writes</b>"],
     ["<b>Non-executable memory</b>", "<b>Executing injected shellcode</b>", "<b>Reusing existing code (ROP)</b>"],
     ["<b>ASLR</b>", "<b>Knowing where anything is</b>", "<b>An address leak; low entropy; partial overwrite</b>"],
     ["<b>CFI</b>", "<b>Indirect calls to unintended targets</b>", "<b>Targets within the permitted set; data-only attacks</b>"],
     ["<b>Shadow stack</b>", "<b>Return address corruption</b>", "<b>Forward-edge attacks, which it does not cover</b>"],
     ["<b>Allocator hardening</b>", "<b>Reliable heap layout control</b>", "<b>Patience, and leaks</b>"],
   ],
   "footnote": "<b>The pattern is that each mitigation removes one "
               "technique and the attacker moves to the next</b> — "
               "which is why they are deployed in combination rather than "
               "chosen between.",
   "note": "The stops/bypassed pairing is what makes this honest."},

  {"t": "callout", "title": "The historical sequence is instructive",
   "kind": "Each mitigation created the next technique",
   "body": ["<b>Non-executable memory made injected shellcode "
            "useless</b> — so attackers reused code already present "
            "in the process, which is return-oriented "
            "programming.",
            "<b>ASLR made the addresses of that code "
            "unknown</b> — so attackers added an information leak as "
            "a first stage, which is why an out-of-bounds <i>read</i> is "
            "now valuable (Module 02 §2).",
            "<b>Control-flow integrity constrained indirect "
            "calls</b> — so attackers moved to data-only attacks, "
            "corrupting values rather than pointers.",
            "<b>Which is CSCE 701 Module 01's asymmetry running in "
            "reverse</b> — <b>each defence closed a technique and "
            "the attacker needed only one remaining one</b>, and the "
            "cost went up each time."]},

  {"t": "section", "label": "Part 3", "title": "Hardening you should already have",
   "blurb": "Free, and frequently off."},

  {"t": "code", "kicker": "Flags", "title": "The build configuration to adopt",
   "lang": "text", "code": """
  -D_FORTIFY_SOURCE=3        bounds-checked string and
                             memory functions where the
                             size is known
  -fstack-protector-strong   stack canaries
  -fstack-clash-protection   stack probing
  -Wl,-z,relro,-z,now        read-only relocations
  -fPIE -pie                 position independent, so
                             ASLR applies to the main
                             binary too
  -fcf-protection            hardware CFI on x86
  -D_GLIBCXX_ASSERTIONS      bounds-checked C++
                             containers

  AND THE WARNINGS AS ERRORS
      -Wall -Wextra -Werror
      -Wformat=2 -Wconversion

  CHECK WHAT YOU SHIPPED, not what you configured --
  use checksec or hardening-check on the artefact.
""",
   "caption": "<b>Check the artefact rather than the build "
              "configuration</b> — a flag in one makefile and a "
              "library built without it is the common case.",
   "note": "Verifying the binary is the step people skip."},

  {"t": "bullets", "kicker": "Costs", "title": "And what each costs, honestly",
   "items": [
     "<b>Most of the list above costs under a few percent</b>, and "
     "<b>several cost nothing measurable</b> — which makes "
     "leaving them off a decision rather than a trade-off.",
     "",
     "<b>FORTIFY_SOURCE and container assertions can cost "
     "more</b> in allocation-heavy or string-heavy code, so "
     "measure.",
     "",
     "<b>CFI costs real performance and code size</b>, and "
     "requires whole-program or link-time visibility.",
     "",
     "<b>And PIE historically cost a little on 32-bit x86</b> and "
     "costs essentially nothing now.",
     "",
     "<b>So the honest position:</b> <b>enable the cheap set "
     "unconditionally, and measure the rest against your own "
     "workload.</b>",
   ],
   "footnote": "<b>The cheap set is free security and is off by "
               "default in a great many build systems</b> — which "
               "makes checking it a high-yield afternoon."},

  {"t": "section", "label": "Part 4", "title": "Perspective",
   "blurb": "What mitigations are and are not for."},

  {"t": "callout", "title": "Mitigations buy time; safe languages and tooling remove the class",
   "kind": "Closing",
   "body": ["<b>Enable every mitigation you can afford</b> — it is "
            "cheap, it applies to code you cannot change, and it "
            "degrades the reliability of exploits against defects you do "
            "not know about.",
            "<b>And do not mistake that for a solution.</b> <b>The "
            "defect is still there, and a sufficiently motivated "
            "adversary gets through</b> — the published record is "
            "unambiguous on this.",
            "<b>So the ordering is:</b> <b>eliminate the class where "
            "you can (Module 02 §4), find the instances "
            "with tooling (Modules 07–09), and mitigate what "
            "remains.</b>",
            "<b>Which is the proportionate position</b> — "
            "<b>mitigations are the last layer rather than the "
            "strategy</b>, and a programme that consists only of "
            "hardening flags has not started."]},
 ],
 "takeaways": [
   "Mitigations leave the defect present and make the step from defect to "
   "execution control harder, which is worth a great deal and is not a "
   "fix.",
   "Each mitigation removes one technique and the attacker moves to the "
   "next, which is why they are deployed in combination.",
   "Non-executable memory produced ROP, ASLR made information leaks "
   "valuable, and CFI produced data-only attacks.",
   "Check what you shipped rather than what you configured — a flag "
   "in one makefile and a library built without it is the common case.",
   "Most hardening flags cost under a few percent and several cost "
   "nothing, so leaving them off is a decision rather than a trade-off.",
   "Mitigations are the last layer rather than the strategy, and a "
   "programme consisting only of hardening flags has not started.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The strategy"),
  ("callout", "Mitigations do not fix defects; they make exploitation "
              "expensive and unreliable",
   ["<b>Every mitigation in this module leaves the defect entirely "
    "present</b> — the overflow still overflows, the stale pointer "
    "is still stale — <b>and makes the step from having a defect to "
    "having control of execution substantially harder.</b>",
    "<b>Which is worth a great deal in practice.</b> <b>An exploit "
    "that requires a separate information leak as a first stage, works "
    "one time in ten, and breaks on the next compiler release is a "
    "fundamentally different proposition</b> from one that works "
    "reliably and indefinitely — both economically and "
    "operationally.",
    "<b>And it is worth being explicit about the arithmetic:</b> "
    "<b>mitigations shift effort from the defender to the attacker</b>, "
    "which is <b>the opposite direction to most of CSCE 701 "
    "Module 01's asymmetry</b> and is why they have been worth the "
    "investment despite every one being bypassable.",
    "<b>But none of them is a substitute for not having the "
    "defect</b> — <b>and every single one has been bypassed in "
    "practice</b>, which &sect;2 covers explicitly rather than omitting, "
    "because a mitigation whose bypass you do not know is a mitigation "
    "you will over-trust."]),

  ("h1", "2 &nbsp; The mitigations"),
  ("table", ["Mitigation", "What it stops", "How it has been bypassed"],
   [["<b>Stack canary</b>",
     "<b>A sequential stack overflow reaching the saved return "
     "address.</b>",
     "<b>Leaking the canary value first; writing non-sequentially past "
     "it; overwriting a local pointer instead of the return "
     "address.</b>"],
    ["<b>Non-executable memory (NX/DEP)</b>",
     "<b>Executing shellcode the attacker injected as data.</b>",
     "<b>Reusing code already present in the process</b> — "
     "return-oriented programming."],
    ["<b>Address space layout randomisation</b>",
     "<b>Knowing the address of anything.</b>",
     "<b>An information leak; insufficient entropy on 32-bit; partial "
     "pointer overwrite; a non-PIE binary left at a fixed "
     "address.</b>"],
    ["<b>Control-flow integrity</b>",
     "<b>Indirect calls and jumps to unintended targets.</b>",
     "<b>Choosing a target within the permitted set; data-only attacks "
     "that corrupt values rather than pointers.</b>"],
    ["<b>Shadow stack / return address protection</b>",
     "<b>Corruption of the return address specifically.</b>",
     "<b>Forward-edge attacks, which it does not cover at all</b> "
     "— so it pairs with CFI rather than replacing it."],
    ["<b>Allocator hardening</b>",
     "<b>Reliable control of heap layout</b> (Module 02 "
     "&sect;3).",
     "<b>Patience, repeated attempts, and information leaks</b> — it "
     "reduces reliability rather than preventing the technique."]],
   [0.24, 0.33, 0.43]),
  ("callout", "The historical sequence is instructive",
   ["<b>Non-executable memory made injected shellcode useless</b> "
    "— so attackers stopped injecting code and started reusing code "
    "already present in the process, chaining short sequences ending in "
    "a return. <b>Return-oriented programming exists because of "
    "NX.</b>",
    "<b>ASLR then made the addresses of that existing code "
    "unknown</b> — so attackers added an information leak as a "
    "mandatory first stage, <b>which is precisely why an out-of-bounds "
    "<i>read</i> is now a valuable primitive rather than a minor "
    "disclosure</b> (Module 02 &sect;2's second row, and "
    "Module 01 &sect;3's severity reasoning).",
    "<b>Control-flow integrity then constrained indirect calls to "
    "plausible targets</b> — so attackers moved to data-only "
    "attacks, corrupting a privilege flag, a length field, or a file path "
    "rather than any pointer, which CFI does not address because no "
    "control flow is violated.",
    "<b>Which is CSCE 701 Module 01's asymmetry running in "
    "reverse</b> — <b>each defence closed off one technique and the "
    "attacker needed only one remaining technique</b> — <b>and the "
    "cost went up substantially at each step</b>, which is the whole "
    "justification for the sequence. <b>The defender did not win and "
    "the price rose by orders of magnitude</b>, and that is a real "
    "result."]),

  ("break",),
  ("h1", "3 &nbsp; Hardening you should already have"),
  ("code", """-D_FORTIFY_SOURCE=3        bounds-checked string and
                           memory functions wherever the
                           size is known at compile time
-fstack-protector-strong   stack canaries
-fstack-clash-protection   stack probing
-Wl,-z,relro,-z,now        read-only relocations, so the
                           GOT is not writable
-fPIE -pie                 position independent, so that
                           ASLR applies to the main
                           binary and not only libraries
-fcf-protection            hardware CFI on x86
-D_GLIBCXX_ASSERTIONS      bounds-checked C++ containers

AND THE WARNINGS AS ERRORS
    -Wall -Wextra -Werror
    -Wformat=2 -Wconversion   (the last catches
                               Module 03's truncations)

CHECK WHAT YOU SHIPPED, not what you configured --
run checksec or hardening-check on the actual
artefact."""),
  ("p", "<b>Check the artefact rather than the build "
        "configuration.</b> <b>A flag set in one makefile, and a "
        "vendored library or a third-party dependency built without "
        "it, is the common case</b> — and the resulting binary has "
        "the mitigation on some objects and not others, which for ASLR "
        "and RELRO means effectively not at all. <b>Verifying the binary "
        "is the step people skip</b>, and it takes one command."),
  ("ul", ["<b>Most of the list above costs under a few percent</b>, "
          "and <b>several cost nothing measurable at all</b> — which "
          "makes <b>leaving them off a decision rather than a "
          "trade-off</b>, and usually a decision nobody made "
          "deliberately.",
          "<b>FORTIFY_SOURCE and the container assertions can cost "
          "more</b> in allocation-heavy or string-heavy code, <b>so "
          "measure on your own workload</b> rather than accepting either "
          "the published figure or the folklore.",
          "<b>Control-flow integrity costs real performance and code "
          "size</b>, and <b>requires whole-program or link-time "
          "visibility</b> — which makes it a genuine engineering "
          "decision rather than a free flag.",
          "<b>And PIE historically cost a little on 32-bit x86</b>, "
          "because of register pressure, <b>and costs essentially nothing "
          "now</b> — so the objection you may read in older material "
          "no longer applies.",
          "<b>So the honest position:</b> <b>enable the cheap set "
          "unconditionally, and measure the rest against your own "
          "workload.</b> <b>The cheap set is free security and is off by "
          "default in a great many build systems</b> — which makes "
          "checking your own build a high-yield afternoon and one of the "
          "few genuinely easy wins in this course."]),

  ("h1", "4 &nbsp; Perspective"),
  ("callout", "Mitigations buy time; safe languages and tooling remove the "
              "class",
   ["<b>Enable every mitigation you can afford</b> — <b>it is "
    "cheap, it applies to code you cannot change or do not control, and "
    "it degrades the reliability of exploits against defects you do not "
    "yet know you have</b>, which is the only defence that has that "
    "property.",
    "<b>And do not mistake that for a solution.</b> <b>The defect is "
    "still present, and a sufficiently motivated and resourced adversary "
    "gets through</b> — <b>the published record on this is "
    "unambiguous</b>, and &sect;2's third column is the evidence.",
    "<b>So the ordering is clear:</b> <b>eliminate the class where you "
    "can (Module 02 &sect;4's safe languages, Module 10 "
    "&sect;2's safe-by-default interfaces), find the instances with "
    "tooling (Modules 07 through 09), and mitigate whatever "
    "remains.</b> <b>Three layers, in that order of preference.</b>",
    "<b>Which is the proportionate position</b> — "
    "<b>mitigations are the last layer rather than the strategy</b>, and "
    "<b>a programme that consists only of hardening flags has not "
    "started</b>. Equally, a programme that has rewritten nothing and "
    "also not enabled the free flags has left money on the table, which "
    "is the more common failure."]),
 ],
 "resources": [
   ("Szekeres et al. &mdash; SoK: Eternal War in Memory (free)",
    "https://web.archive.org/web/20260806120930/https://people.eecs.berkeley.edu/~dawnsong/papers/Oakland13-SoK-CR.pdf",
    "<b>&sect;1 and &sect;2 systematised</b> — every mitigation, "
    "what it stops, and what bypasses it, in one paper."),
   ("Shacham &mdash; The Geometry of Innocent Flesh on the Bone (free)",
    "https://hovav.net/ucsd/dist/geometry.pdf",
    "<b>&sect;2's first bypass in the original</b> — the paper that "
    "introduced return-oriented programming."),
   ("Debian and Red Hat hardening guides, and checksec (free)",
    "https://wiki.debian.org/Hardening",
    "<b>&sect;3's flags with the distribution's rationale</b>, plus the "
    "tool to verify the artefact."),
   ("MIT 6.858's mitigation labs (free, OCW)",
    "https://css.csail.mit.edu/6.858/",
    "<b>&sect;2 practically</b>, on targets built for it — which is "
    "Module 01 &sect;4's constraint satisfied."),
 ],
 "exercises": [
   "<b>State what each of six mitigations stops</b> and how each has "
   "been bypassed.",
   "<b>Explain why NX produced ROP</b>, and why ASLR made OOB reads "
   "valuable.",
   "<b>Explain what a data-only attack is</b> and why CFI does not stop "
   "it.",
   "<b>Run <code>checksec</code> on a binary you ship</b> and report "
   "what is missing.",
   "<b>Run it on your dependencies' libraries</b> and compare.",
   "<b>Enable the cheap hardening set</b> and verify it on the "
   "artefact.",
   "<b>Measure the performance cost</b> on your own workload.",
   "<b>Enable <code>-Wconversion</code></b> and report how many "
   "Module 03 truncations it finds.",
   "<b>Demonstrate a stack canary stopping an overflow</b> on your own "
   "test program.",
   "<b>Write your three-layer plan:</b> eliminate, find, mitigate.",
 ],
 "selfcheck": [
   "What do mitigations do and not do?",
   "Why is an unreliable exploit meaningfully different?",
   "Name six mitigations, what each stops, and a bypass for each.",
   "Why are they deployed in combination?",
   "Give the historical sequence NX → ROP → ASLR → leak "
   "→ CFI → data-only.",
   "Why is an out-of-bounds read now valuable?",
   "Name six hardening flags and what each provides.",
   "Why check the artefact rather than the configuration?",
   "Which flags are free and which cost real performance?",
   "Give the three-layer ordering and the proportionate position.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Claiming Code Security Honestly",
 "subtitle": "What an assessment of code establishes.",
 "question": "The tools found nothing. What does that tell anyone?",
 "outcomes": [
     "State what each technique establishes.",
     "Identify the standard overclaims.",
     "Write a checkable assessment claim.",
     "Place this course relative to CSCE 701 and CSCE 711.",
     "State a proportionate programme for a real codebase.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What each establishes",
   "blurb": "Precisely, and it is less than it sounds."},

  {"t": "table", "kicker": "Claims", "title": "What each technique actually supports",
   "header": ["Technique", "Establishes", "Does not establish"],
   "widths": [2.6, 4.2, 5.1],
   "rows": [
     ["<b>Static analysis</b>", "<b>These rules found these things</b>", "<b>Absence — it is unsound by design (M07 §1)</b>"],
     ["<b>Fuzzing</b>", "<b>This coverage, no crashes, this long</b>", "<b>Anything on unreached code (M08 §3)</b>"],
     ["<b>Sanitisers</b>", "<b>These executions had no violation</b>", "<b>Anything about other inputs (M09 §4)</b>"],
     ["<b>Review</b>", "<b>A person looked for these things</b>", "<b>That they would have seen them (M11 §4)</b>"],
     ["<b>A test suite</b>", "<b>These behaviours are as expected</b>", "<b>Anything adversarial</b>"],
   ],
   "footnote": "<b>Not one of these establishes absence</b>, and the "
               "middle column is always a statement about <i>what you "
               "did</i> rather than about the program.",
   "note": "The does-not-establish column is the module."},

  {"t": "callout", "title": "“The scanner found nothing” is a statement about the scanner",
   "kind": "The substitution to refuse",
   "body": ["<b>It says that these rules, on this code, produced no "
            "findings</b> — which is information about the rules' "
            "coverage as much as about the code.",
            "<b>And it is routinely reported as 'the code is "
            "clean'</b>, which is a different claim entirely and is not "
            "supported by the evidence.",
            "<b>The honest form names the method and its "
            "scope:</b> <b>'this ruleset, on these files, found no "
            "instances of these classes'</b> — all four clauses "
            "checkable.",
            "<b>Which is the same correction "
            "CSCE 701 Module 13 §1 makes about a "
            "penetration test and CSCE 711 Module 13 "
            "§3 makes about a proof</b> — three "
            "courses, one error."]},

  {"t": "section", "label": "Part 2", "title": "Overclaims",
   "blurb": "The specific ones to avoid."},

  {"t": "table", "kicker": "Overclaims", "title": "The standard overclaims, corrected",
   "header": ["Claim", "Correction"],
   "widths": [4.4, 6.6],
   "rows": [
     ["<b>'The code is secure'</b>", "<b>Not supportable. Against which adversary, for which classes?</b>"],
     ["<b>'We fuzzed it'</b>", "<b>With what coverage, for how long, with which oracle?</b>"],
     ["<b>'Static analysis is clean'</b>", "<b>Which rules, and what is the known false negative profile?</b>"],
     ["<b>'It passed security review'</b>", "<b>Who looked, at what, for what, and for how long?</b>"],
     ["<b>'Memory safe'</b>", "<b>In safe code — name the unsafe blocks and the FFI (M02 §4)</b>"],
     ["<b>'100% test coverage'</b>", "<b>Line coverage says nothing about adversarial inputs</b>"],
   ],
   "footnote": "<b>The coverage row is the most seductive</b> — a "
               "complete-sounding number that measures lines executed by "
               "friendly inputs, and says nothing at all about hostile "
               "ones.",
   "note": "The 100% coverage overclaim is the one engineers believe "
           "most."},

  {"t": "bullets", "kicker": "Honest", "title": "Claims you can defend",
   "items": [
     "<b>'We fuzzed the parser for 400 CPU-hours under ASan and "
     "UBSan, reaching 78% of its edges, with no findings in the last "
     "300 hours.'</b> <b>Every clause checkable.</b>",
     "",
     "<b>'These twelve rules run on every change; the eight "
     "findings to date are triaged in the repository.'</b>",
     "",
     "<b>'The authorisation layer was reviewed by two people "
     "against this checklist; the three findings are fixed.'</b>",
     "",
     "<b>'Memory safe except for these four <code>unsafe</code> "
     "blocks and the FFI boundary, which were reviewed "
     "individually.'</b>",
     "",
     "<b>And the limitation statement:</b> <b>'we have no coverage "
     "of concurrency defects or authorisation logic outside this "
     "layer.'</b>",
   ],
   "footnote": "<b>The limitation statement is the one that "
               "distinguishes an assessment from a tool run</b> — "
               "and it is Project 2's hardest-graded "
               "requirement."},

  {"t": "section", "label": "Part 3", "title": "The semester",
   "blurb": "Three courses, divided by failure source."},

  {"t": "table", "kicker": "Semester 9", "title": "Where each course sits",
   "header": ["Course", "Covers", "Honest summary"],
   "widths": [2.3, 3.8, 5.4],
   "rows": [
     ["<b>CSCE 701</b>", "<b>Systems, operations, people</b>", "<b>Where the incidents are</b>"],
     ["<b>CSCE 711</b>", "<b>Primitives and their use</b>", "<b>The part that works — misused</b>"],
     ["<b>CSCE 713</b>", "<b>Defects in code</b>", "<b>Where the severe ones are, and where the tooling has limits</b>"],
   ],
   "footnote": "<b>And all three converge on one conclusion:</b> "
               "<b>make the defect unexpressible rather than training "
               "people not to write it</b> — defaults, "
               "misuse-resistant APIs, and safe types, from three "
               "directions.",
   "note": "The convergence is the semester's result."},

  {"t": "section", "label": "Part 4", "title": "A proportionate programme",
   "blurb": "In order, with a finite budget."},

  {"t": "bullets", "kicker": "Programme", "title": "What to do, in order",
   "items": [
     "<b>1 · Sanitisers in CI</b> "
     "(Module 09) — <b>no source changes, finds "
     "defects on day one</b>, and it is the cheapest real "
     "improvement available.",
     "",
     "<b>2 · Fuzz the parsers</b> (Module 08) — "
     "<b>where untrusted input meets manual memory handling</b>, with "
     "coverage reported.",
     "",
     "<b>3 · Hardening flags</b> "
     "(Module 12 §3) — free, and verify them on "
     "the artefact.",
     "",
     "<b>4 · Static analysis on new code only</b> "
     "(Module 07 §3), with your own rules for your own "
     "invariants.",
     "",
     "<b>5 · Then review the authorisation and parsing "
     "code</b> (Module 11), <b>and make the recurring defect "
     "unexpressible</b> (Module 10 §2).",
   ],
   "footnote": "<b>Steps 1 to 3 are a week's work and change the "
               "defect profile measurably</b> — and step 5 is where "
               "the durable improvement is, which is why it is last "
               "rather than unimportant."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can explain why vulnerabilities exist, name the "
            "classes that account for the severe ones, and recognise each "
            "in code you are reading</b> — which is the practical "
            "skill and transfers to any language.",
            "<b>You can run the techniques and read their output "
            "honestly:</b> <b>a fuzzing campaign measured by coverage, "
            "static analysis triaged with reasons, sanitisers as the "
            "oracle, and review aimed at what tooling cannot "
            "see.</b>",
            "<b>And you know the limits are theoretical rather than "
            "temporary</b> — <b>CSCE 627's undecidability means no "
            "tool will ever decide this</b>, so the choice is always "
            "which way to be wrong.",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it means naming the "
            "technique, its coverage, and its blind spots</b> — "
            "because <b>'the tools found nothing' states none of the "
            "three.</b>"]},
 ],
 "takeaways": [
   "Not one technique in this course establishes absence — each "
   "supports a statement about what you did rather than about the program.",
   "'The scanner found nothing' is a statement about the scanner, and it "
   "is routinely reported as 'the code is clean'.",
   "'100% test coverage' is the most seductive overclaim: it measures "
   "lines executed by friendly inputs.",
   "The limitation statement is what distinguishes an assessment from a "
   "tool run.",
   "All three Semester 9 courses converge on making the defect "
   "unexpressible rather than training people not to write it.",
   "Sanitisers, fuzzing, and hardening flags are about a week's work and "
   "change the defect profile measurably.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What each technique establishes"),
  ("table", ["Technique", "What it establishes", "What it does not "
             "establish"],
   [["<b>Static analysis</b>",
     "<b>That these rules, run on this code, produced these "
     "findings.</b>",
     "<b>Absence of defects</b> — it is unsound by design "
     "(Module 07 &sect;1), so silence carries very little "
     "information."],
    ["<b>Fuzzing</b>",
     "<b>That this coverage was achieved, over this duration, with no "
     "crashes under this oracle.</b>",
     "<b>Anything at all about unreached code</b> (Module 08 "
     "&sect;3) — which is why coverage is the number that "
     "matters."],
    ["<b>Sanitisers</b>",
     "<b>That these executions, on these inputs, contained no detected "
     "violation.</b>",
     "<b>Anything about any other input</b> (Module 09 "
     "&sect;4)."],
    ["<b>Code review</b>",
     "<b>That a person looked at this code for these specific "
     "things.</b>",
     "<b>That they would have recognised the defect if it were "
     "there</b> (Module 11 &sect;4)."],
    ["<b>A test suite</b>",
     "<b>That these behaviours are as the tests expect.</b>",
     "<b>Anything adversarial</b> — the tests encode the expected "
     "cases, which are precisely not the interesting ones."]],
   [0.18, 0.37, 0.45]),
  ("p", "<b>Not one of these establishes absence</b>, and <b>the middle "
        "column is in every case a statement about <i>what you did</i> "
        "rather than about the program</b> — which is the whole "
        "content of this module and the reason the right-hand column is "
        "worth memorising. <b>The asymmetry is fundamental rather than a "
        "limitation of current tools</b> (CSCE 627, and "
        "Module 07 &sect;1)."),
  ("callout", "“The scanner found nothing” is a statement about "
              "the scanner",
   ["<b>It says that these particular rules, applied to this code, "
    "produced no findings</b> — <b>which is information about the "
    "rules' coverage at least as much as about the code's quality.</b> A "
    "scanner with no rules finds nothing on any input.",
    "<b>And it is routinely reported as 'the code is clean'</b>, which "
    "is <b>a different claim entirely and is not supported by the "
    "evidence</b> — and the substitution happens silently, usually "
    "between the engineer and the summary slide.",
    "<b>The honest form names the method and its scope:</b> <b>'this "
    "ruleset, on these files, found no instances of these "
    "classes'</b> — <b>all four clauses checkable by somebody "
    "else</b>, which is the test of a real claim.",
    "<b>Which is exactly the same correction CSCE 701 "
    "Module 13 &sect;1 makes about a penetration test, and "
    "CSCE 711 Module 13 &sect;3 makes about a security "
    "proof</b> — <b>three courses in one semester identifying the "
    "same error</b>: substituting the absence of a finding for the "
    "presence of a property."]),

  ("h1", "2 &nbsp; Overclaims, and defensible claims"),
  ("table", ["The claim", "The correction"],
   [["<b>'The code is secure.'</b>",
     "<b>Not a supportable statement.</b> Against which adversary, for "
     "which defect classes, in which components?"],
    ["<b>'We fuzzed it.'</b>",
     "<b>With what coverage, for how long, with which oracle, and from "
     "what corpus?</b> (Module 08 &sect;3.)"],
    ["<b>'Static analysis is clean.'</b>",
     "<b>Which rules, and what is the known false negative profile of "
     "those rules?</b> (Module 07 &sect;1.)"],
    ["<b>'It passed security review.'</b>",
     "<b>Who looked, at what, for what, and for how long?</b> "
     "(Module 11 &sect;4's recording requirement.)"],
    ["<b>'It is memory safe.'</b>",
     "<b>In safe code</b> — <b>name the <code>unsafe</code> blocks "
     "and the foreign function boundary</b> (Module 02 &sect;4)."],
    ["<b>'We have 100% test coverage.'</b>",
     "<b>Line coverage says nothing whatsoever about adversarial "
     "inputs.</b> See the note."]],
   [0.34, 0.66]),
  ("p", "<b>The coverage row is the most seductive of these</b> — "
        "<b>a complete-sounding number that measures which lines were "
        "executed by friendly inputs, and says nothing at all about "
        "hostile ones.</b> <b>A function with 100% line coverage can "
        "have an unhandled integer overflow on every path</b>, because the "
        "tests supplied reasonable values. <b>This is the overclaim "
        "engineers believe most readily</b>, because it is quantitative "
        "and it is their own number."),
  ("ul", ["<b>'We fuzzed the parser for 400 CPU-hours under "
          "AddressSanitizer and UBSan, reaching 78% of its edges, with no "
          "findings in the final 300 hours.'</b> <b>Every clause "
          "checkable, and the plateau is itself informative.</b>",
          "<b>'These twelve static analysis rules run on every change; "
          "the eight findings to date are triaged in the repository with "
          "reasons.'</b> (Module 07 &sect;3.)",
          "<b>'The authorisation layer was reviewed by two engineers "
          "against this written checklist; the three findings are fixed "
          "and the checklist is in the repository.'</b> "
          "(Module 11 &sect;4.)",
          "<b>'Memory safe except for these four <code>unsafe</code> "
          "blocks and the FFI boundary, each of which was reviewed "
          "individually.'</b> — the narrow claim of Module 02 "
          "&sect;4, made precisely.",
          "<b>And the limitation statement:</b> <b>'we have no "
          "coverage of concurrency defects, and no coverage of "
          "authorisation logic outside this layer.'</b> <b>The limitation "
          "statement is the one thing that distinguishes an assessment "
          "from a tool run</b> — and it is <b>Project 2's "
          "hardest-graded requirement</b>, because it requires knowing "
          "what your methods structurally cannot see."]),

  ("break",),
  ("h1", "3 &nbsp; The semester"),
  ("table", ["Course", "What it covers", "The honest summary"],
   [["<b>CSCE 701</b>",
     "<b>Systems, operations, architecture, and people.</b>",
     "<b>Where the incidents are</b> — credentials, "
     "misconfiguration, missing authorisation, unpatched dependencies, "
     "phishing."],
    ["<b>CSCE 711</b>",
     "<b>The cryptographic primitives and their correct use.</b>",
     "<b>The part that works — misused</b>: nonces, keys, error "
     "handling, composition."],
    ["<b>CSCE 713 (this one)</b>",
     "<b>Defects in code, and the techniques that find them.</b>",
     "<b>Where the severe ones are, and where the tooling has "
     "theoretical limits</b> rather than merely practical ones."]],
   [0.22, 0.34, 0.44]),
  ("p", "<b>And all three courses converge on a single "
        "conclusion:</b> <b>make the defect unexpressible rather than "
        "training people not to write it.</b> <b>CSCE 701 "
        "Module 11 &sect;3 reached it through defaults and the "
        "compliance budget; CSCE 711 Module 01 &sect;4 reached it "
        "through misuse-resistant APIs and the historical record of "
        "cryptographic failures; this course reached it through "
        "Module 02 &sect;4's safe languages and Module 10 "
        "&sect;2's safe-by-construction interfaces.</b> <b>Three "
        "independent routes to the same place is the semester's "
        "result</b>, and it is worth more than any individual technique in "
        "it."),

  ("h1", "4 &nbsp; A proportionate programme"),
  ("ul", ["<b>1 &middot; Sanitisers in continuous integration</b> "
          "(Module 09) — <b>no source changes required, and it "
          "finds defects on the first day</b> in code that has passed its "
          "tests for years. <b>The cheapest real improvement "
          "available.</b>",
          "<b>2 &middot; Fuzz the parsers</b> (Module 08) — "
          "<b>where untrusted input meets manual memory handling</b>, "
          "with <b>coverage reported rather than duration</b>, and the "
          "corpus kept.",
          "<b>3 &middot; Hardening flags</b> (Module 12 "
          "&sect;3) — <b>free, and verify them on the artefact "
          "rather than in the makefile.</b>",
          "<b>4 &middot; Static analysis, on new code only</b> "
          "(Module 07 &sect;3's baseline), <b>with your own rules "
          "encoding your own invariants</b> (Module 07 &sect;4), "
          "which is where the real yield is.",
          "<b>5 &middot; Then review the authorisation and parsing "
          "code</b> (Module 11 &sect;1's two highest-yield "
          "categories), <b>and make the recurring defect "
          "unexpressible</b> (Module 10 &sect;2). <b>Steps 1 to 3 are "
          "about a week's work and change the defect profile "
          "measurably</b> — and <b>step 5 is where the durable "
          "improvement is, which is why it is last rather than "
          "unimportant</b>: it requires knowing which defect recurs, and "
          "steps 1 to 4 are how you find out."]),
  ("callout", "Where this course leaves you",
   ["<b>You can explain why vulnerabilities exist, name the classes "
    "that account for the severe ones, and recognise each of them in code "
    "you are reading</b> — which is the practical skill, and it "
    "transfers across languages because the classes do.",
    "<b>You can run the techniques and read their output "
    "honestly:</b> <b>a fuzzing campaign measured by coverage rather "
    "than duration, static analysis triaged with written reasons, "
    "sanitisers used as the oracle rather than as a debugger, and review "
    "aimed specifically at what the tooling structurally cannot "
    "see.</b>",
    "<b>And you know that the limits are theoretical rather than "
    "temporary</b> — <b>CSCE 627's undecidability results mean no "
    "tool will ever decide these properties</b>, so <b>the choice is "
    "always which way to be wrong</b>, and a vendor promising otherwise "
    "is selling something.",
    "<b>The closing rule is the program's, unchanged across "
    "twenty-seven courses:</b> <b>state what you measured, state what "
    "you assumed, and never claim more than you established.</b> <b>In "
    "software security it means naming the technique, its coverage, and "
    "its blind spots</b> — because <b>'the tools found nothing' "
    "states none of the three</b>, and &sect;2's table is what happens "
    "when it is accepted as though it did."]),
 ],
 "resources": [
   ("Klees et al. &mdash; Evaluating Fuzz Testing (free)",
    "https://arxiv.org/abs/1808.09700",
    "<b>&sect;1's fuzzing row, rigorously</b> — what a campaign "
    "establishes and what is routinely claimed instead."),
   ("Bessey et al. &mdash; A Few Billion Lines of Code Later (free)",
    "https://dl.acm.org/doi/10.1145/1646353.1646374",
    "<b>&sect;1's static analysis row, from the field</b> — honest "
    "about what the tools find and what customers believe they find."),
   ("Google &mdash; Building Secure and Reliable Systems, the "
    "concluding chapters (free PDF)",
    "https://sre.google/books/building-secure-reliable-systems/",
    "<b>&sect;3's convergence and &sect;4's ordering</b>, argued from "
    "operating experience."),
   ("The CWE Top 25, current edition (free)",
    "https://cwe.mitre.org/top25/",
    "<b>&sect;4's evidence</b> — reread it annually and check your "
    "own programme's emphasis against it."),
 ],
 "exercises": [
   "<b>For each of the five techniques</b>, write what it establishes "
   "and what it does not.",
   "<b>Find a security claim made about software you use</b> and assess "
   "it against §2's table.",
   "<b>Rewrite 'the scanner found nothing'</b> in the four-clause "
   "form.",
   "<b>Take your own test coverage figure</b> and say what it does not "
   "measure.",
   "<b>Write the honest claim</b> for your own fuzzing campaign.",
   "<b>Write your limitation statement</b> — the classes your "
   "methods cannot see.",
   "<b>Identify where the three courses converge</b>, in your own "
   "words.",
   "<b>Compare your own programme</b> against §4's five steps and "
   "report the gaps.",
   "<b>Revisit Module 01's last exercise</b> and compare.",
   "<b>Project 2 is now due.</b> Submit the fuzzing campaign with "
   "coverage, the triaged static analysis, the manual review of the "
   "highest-risk component, the fixes offered upstream, and the "
   "limitation analysis.",
 ],
 "selfcheck": [
   "For five techniques, what does each establish and not establish?",
   "What do all five have in common?",
   "Why is 'the scanner found nothing' a statement about the scanner?",
   "Give the four-clause honest form.",
   "Give six overclaims and the correction to each.",
   "Why is the coverage overclaim the most seductive?",
   "Give three defensible claims.",
   "What distinguishes an assessment from a tool run?",
   "How does the semester divide, and where do the three courses "
   "converge?",
   "Give the five-step programme and say where the durable improvement "
   "is.",
 ],
},

]
