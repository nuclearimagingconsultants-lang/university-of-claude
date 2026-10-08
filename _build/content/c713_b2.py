# -*- coding: utf-8 -*-
"""CSCE 713 — Modules 03-08."""

MODULES = [

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Integers and Types",
 "subtitle": "Arithmetic that does not behave like arithmetic.",
 "question": "Why did the length check pass?",
 "outcomes": [
     "Explain overflow, truncation, and sign confusion.",
     "Explain integer promotion and its surprises.",
     "Explain why these become memory safety defects.",
     "Explain type confusion and its mechanism.",
     "Write arithmetic that cannot overflow silently.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Three failures",
   "blurb": "Each of which defeats a correct-looking check."},

  {"t": "table", "kicker": "Failures", "title": "The three integer failures",
   "header": ["Failure", "Mechanism", "Typical consequence"],
   "widths": [2.6, 4.2, 5.1],
   "rows": [
     ["<b>Overflow</b>", "<b>The result exceeds the type's range and wraps</b>", "<b>A small allocation for a large copy</b>"],
     ["<b>Truncation</b>", "<b>Assigned to a narrower type; high bits lost</b>", "<b>A large length becomes small</b>"],
     ["<b>Sign confusion</b>", "<b>Signed value reinterpreted as unsigned, or vice versa</b>", "<b>A negative length becomes enormous</b>"],
   ],
   "footnote": "<b>All three produce the same outcome:</b> <b>a length "
               "check that passes and a copy that does not fit</b> "
               "— which is why these appear in the memory safety "
               "data rather than as arithmetic bugs.",
   "note": "Tie all three to the same downstream consequence."},

  {"t": "code", "kicker": "Pattern", "title": "The canonical defect, in four lines",
   "lang": "text", "code": """
  size_t n = read_count_from_input();
  buf = malloc(n * sizeof(item));   // may overflow
  for (i = 0; i < n; i++)
      buf[i] = read_item();          // writes past end

  WHAT HAPPENS
      n is large enough that n * sizeof(item) wraps
      malloc succeeds with a SMALL allocation
      the loop writes n items into it

  AND THE CHECK THAT DOES NOT HELP
      if (n * sizeof(item) > LIMIT) return;
      -- the multiplication overflows BEFORE the
         comparison, so the check sees the wrapped
         value and passes

  THE FIX: check the operands, not the result.
      if (n > LIMIT / sizeof(item)) return;
      or use a checked-arithmetic helper.
""",
   "caption": "<b>'Check the operands, not the result' is the whole "
              "rule</b> — because the result has already been "
              "corrupted by the time you see it.",
   "note": "This slide is the module's single most useful artefact."},

  {"t": "section", "label": "Part 2", "title": "Promotion",
   "blurb": "The language rules that surprise people."},

  {"t": "callout", "title": "C promotes small types to int, and compares signed against unsigned by converting to unsigned",
   "kind": "The rules worth memorising",
   "body": ["<b>Any type smaller than <code>int</code> is promoted to "
            "<code>int</code> before arithmetic</b> — so "
            "<code>char</code> arithmetic happens at int width and "
            "overflows differently than you expect.",
            "<b>And in a comparison between a signed and an unsigned "
            "type of the same width, the signed value is converted to "
            "unsigned</b> — so <code>-1 &lt; 1u</code> is "
            "<b>false</b>.",
            "<b>Which breaks the obvious defensive check.</b> "
            "<b><code>if (len &lt; 0 || len &gt; max)</code> with an "
            "unsigned <code>len</code> has a first clause the compiler "
            "may remove entirely</b>, because it cannot be true.",
            "<b>And signed overflow is undefined behaviour</b>, so "
            "<b>the compiler may optimise on the assumption that it "
            "cannot happen</b> — which has removed real overflow "
            "checks from real code."]},

  {"t": "bullets", "kicker": "Practice", "title": "Writing arithmetic that cannot fail silently",
   "items": [
     "<b>Use checked arithmetic.</b> <b>Compiler builtins, "
     "<code>size_t</code>-safe helpers, or a safe-numerics "
     "library</b> — and in Rust, the checked and saturating "
     "methods rather than the bare operators.",
     "",
     "<b>Check the operands against the limit</b>, as in "
     "Part 1 — never the computed result.",
     "",
     "<b>Prefer unsigned for sizes and be consistent</b>, so there "
     "is no signed-unsigned comparison to get wrong.",
     "",
     "<b>Enable the sanitiser.</b> <b>UndefinedBehaviorSanitizer "
     "catches signed overflow at runtime</b>, and the unsigned "
     "overflow check can be enabled separately "
     "(Module 09 §2).",
     "",
     "<b>And treat every arithmetic operation on a value from input "
     "as a review trigger</b>, particularly multiplications feeding an "
     "allocation.",
   ],
   "footnote": "<b>Multiplication feeding an allocation is the single "
               "highest-yield pattern to grep for</b> — it is the "
               "shape of the canonical defect."},

  {"t": "section", "label": "Part 3", "title": "Why it becomes memory unsafety",
   "blurb": "The composition that makes it severe."},

  {"t": "callout", "title": "An integer defect is a vulnerability when the number becomes a size",
   "kind": "The connection",
   "body": ["<b>On its own, a wrapped integer is a wrong "
            "answer.</b> <b>It becomes a memory safety defect when the "
            "wrong answer is used as an allocation size, a copy length, "
            "or an index.</b>",
            "<b>So the dangerous sinks are specific and "
            "enumerable:</b> <b><code>malloc</code>, "
            "<code>memcpy</code>, array indexing, loop bounds, and "
            "pointer arithmetic.</b>",
            "<b>Which makes this a taint analysis with a short sink "
            "list</b> — from input, through arithmetic, to a size "
            "— and that is exactly what a static analyser does "
            "reasonably well (Module 07 §2).",
            "<b>And it is why integers get their own module rather "
            "than a paragraph</b>: <b>the arithmetic is where the check "
            "is defeated, and the memory defect is merely where it "
            "surfaces.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Type confusion",
   "blurb": "Accessing memory as the wrong shape."},

  {"t": "callout", "title": "Type confusion means the program interprets bytes as a type they are not",
   "kind": "The mechanism, and where it arises",
   "body": ["<b>A downcast to the wrong class, a union read through "
            "the wrong member, or a pointer cast that was never "
            "valid</b> — after which <b>field offsets, vtable "
            "pointers, and lengths are all read from the wrong "
            "places.</b>",
            "<b>Which is severe because a vtable pointer read from "
            "attacker-controlled data is control of execution</b>, and "
            "because a length field read from the wrong offset defeats "
            "every bounds check downstream.",
            "<b>And the common sources are:</b> <b>unchecked "
            "downcasts, tagged unions whose tag is not consulted, "
            "deserialisation producing an unexpected type "
            "(Module 06), and language runtimes with dynamic "
            "types.</b>",
            "<b>The fix is to make the invalid interpretation "
            "unrepresentable:</b> <b>checked casts, a sum type the "
            "compiler forces you to match on, and a parser that produces "
            "a validated type rather than a generic one.</b>"]},

  {"t": "bullets", "kicker": "Review", "title": "What to look for",
   "items": [
     "<b>Any multiplication or addition on an input-derived value "
     "that reaches an allocation</b> — the canonical "
     "pattern.",
     "",
     "<b>Any comparison mixing signed and unsigned</b>, and any "
     "<code>&lt; 0</code> check on an unsigned value.",
     "",
     "<b>Any assignment from a wider to a narrower integer "
     "type</b>, especially of a length.",
     "",
     "<b>Any cast between pointer types</b>, and any downcast "
     "without a check.",
     "",
     "<b>And any union or tagged variant whose tag is read in one "
     "place and not another.</b>",
   ],
   "footnote": "<b>All five are mechanically greppable</b>, and the "
               "compiler will warn about two of them if you let it "
               "— which is Module 12 §2's "
               "argument."},
 ],
 "takeaways": [
   "Overflow, truncation, and sign confusion all produce the same outcome: "
   "a length check that passes and a copy that does not fit.",
   "Check the operands against the limit, never the computed result, "
   "because the result has already been corrupted.",
   "In C, -1 < 1u is false, and an unsigned value's < 0 check may be "
   "removed by the compiler entirely.",
   "Signed overflow is undefined behaviour, so the compiler may optimise "
   "assuming it cannot happen — which has deleted real checks.",
   "An integer defect becomes a vulnerability when the wrong number is "
   "used as an allocation size, a copy length, or an index.",
   "Type confusion is severe because a vtable pointer read from "
   "attacker-controlled data is control of execution.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The three failures"),
  ("table", ["Failure", "The mechanism", "The typical consequence"],
   [["<b>Overflow</b>",
     "<b>The arithmetic result exceeds the type's range and wraps "
     "around.</b>",
     "<b>A small allocation followed by a large copy</b> — the "
     "canonical pattern below."],
    ["<b>Truncation</b>",
     "<b>A value assigned to a narrower type; the high bits are "
     "discarded.</b>",
     "<b>A large length silently becomes a small one</b>, after which "
     "the check on the small value passes."],
    ["<b>Sign confusion</b>",
     "<b>A signed value reinterpreted as unsigned, or the reverse.</b>",
     "<b>A negative length becomes an enormous positive one</b> — "
     "and negative lengths arrive from input more often than you would "
     "expect."]],
   [0.18, 0.37, 0.45]),
  ("code", """size_t n = read_count_from_input();
buf = malloc(n * sizeof(item));   // may overflow
for (i = 0; i < n; i++)
    buf[i] = read_item();          // writes past end

WHAT HAPPENS
    n is large enough that n * sizeof(item) wraps
    malloc succeeds with a SMALL allocation
    the loop then writes n items into it

AND THE CHECK THAT DOES NOT HELP
    if (n * sizeof(item) > LIMIT) return;
    -- the multiplication overflows BEFORE the
       comparison, so the check inspects the wrapped
       value and passes happily

THE FIX: check the operands, not the result.
    if (n > LIMIT / sizeof(item)) return;
    or use a checked-arithmetic helper that reports
    the overflow rather than wrapping."""),
  ("p", "<b>'Check the operands, not the result' is the whole "
        "rule</b> — <b>because by the time you can see the result, "
        "it has already been corrupted</b>, and no amount of validation "
        "applied to a wrapped value recovers the information that was "
        "lost. <b>This slide is the module's single most useful "
        "artefact</b>, and the pattern it describes accounts for a large "
        "share of the heap overflows in the published defect data."),

  ("h1", "2 &nbsp; Promotion, and the rules that surprise people"),
  ("callout", "C promotes small types to int, and compares signed against "
              "unsigned by converting to unsigned",
   ["<b>Any arithmetic type smaller than <code>int</code> is promoted "
    "to <code>int</code> before arithmetic is performed</b> — so "
    "<code>char</code> and <code>short</code> arithmetic actually happens "
    "at <code>int</code> width, and overflows at a different point than "
    "the declared type suggests.",
    "<b>And in a comparison between a signed and an unsigned type of "
    "the same width, the signed operand is converted to "
    "unsigned</b> — so <b><code>-1 &lt; 1u</code> evaluates to "
    "<i>false</i></b>, because &minus;1 becomes the largest unsigned "
    "value. This is correct per the standard and surprises nearly "
    "everybody.",
    "<b>Which breaks the obvious defensive check.</b> <b><code>if (len "
    "&lt; 0 || len &gt; max)</code> with an unsigned <code>len</code> has "
    "a first clause that can never be true, and which the compiler may "
    "therefore remove entirely</b> — frequently with a warning "
    "nobody read.",
    "<b>And signed overflow is undefined behaviour in C and "
    "C++</b>, which means <b>the compiler is permitted to optimise on "
    "the assumption that it cannot happen</b> — and <b>this has "
    "removed real overflow checks from real code</b>, because a check "
    "written as <code>if (a + b &lt; a)</code> is provably false under "
    "that assumption and gets deleted. <b>Which is why the checked "
    "builtins exist.</b>"]),
  ("ul", ["<b>Use checked arithmetic.</b> <b>The compiler builtins "
          "(<code>__builtin_mul_overflow</code> and relatives), a "
          "safe-numerics library, or in Rust the "
          "<code>checked_</code>/<code>saturating_</code> methods rather "
          "than the bare operators</b> — which make the overflow a "
          "value you must handle.",
          "<b>Check the operands against the limit</b>, as in "
          "&sect;1 — <b>never the computed result</b>, which is the "
          "defect.",
          "<b>Prefer unsigned types for sizes and be consistent about "
          "it</b>, so that there is no signed-unsigned comparison in the "
          "code to get wrong in the first place — consistency here "
          "is worth more than any individual choice.",
          "<b>Enable the sanitiser.</b> "
          "<b>UndefinedBehaviorSanitizer catches signed overflow at "
          "runtime</b>, and the unsigned overflow check can be enabled "
          "separately since unsigned wrapping is well-defined and "
          "sometimes intended (Module 09 &sect;2).",
          "<b>And treat every arithmetic operation on a value derived "
          "from input as a review trigger</b>, particularly a "
          "multiplication feeding an allocation. <b>Multiplication "
          "feeding an allocation is the single highest-yield pattern to "
          "grep for</b> — it is precisely the shape of the canonical "
          "defect, and the search takes minutes."]),

  ("break",),
  ("h1", "3 &nbsp; Why it becomes memory unsafety"),
  ("callout", "An integer defect is a vulnerability when the number becomes "
              "a size",
   ["<b>On its own, a wrapped integer is simply a wrong answer</b> "
    "— a counter that resets, a total that is negative, a display "
    "bug. <b>It becomes a memory safety defect when the wrong answer is "
    "used as an allocation size, a copy length, a loop bound, or an "
    "index.</b>",
    "<b>So the dangerous sinks are specific and enumerable:</b> "
    "<b><code>malloc</code> and friends, <code>memcpy</code> and the "
    "string functions, array indexing, loop bounds, and pointer "
    "arithmetic.</b> <b>Five sinks</b>, which is a short enough list to "
    "audit exhaustively in a medium codebase.",
    "<b>Which makes this a taint analysis with a short sink "
    "list</b> — from an input source, through arithmetic, to a size "
    "sink — and <b>that is exactly the shape of problem a static "
    "analyser handles reasonably well</b> (Module 07 &sect;2), which "
    "is why integer defects are among the classes tooling genuinely "
    "finds.",
    "<b>And it is why integers get a module rather than a "
    "paragraph:</b> <b>the arithmetic is where the check is defeated, "
    "and the memory defect is merely where it surfaces</b> — so "
    "fixing the overflow prevents the overflow, while fixing the "
    "<code>memcpy</code> treats the symptom and leaves the next sink "
    "exposed."]),

  ("h1", "4 &nbsp; Type confusion"),
  ("callout", "Type confusion means the program interprets bytes as a type "
              "they are not",
   ["<b>A downcast to the wrong class, a union read through the wrong "
    "member, a pointer cast that was never valid, or a deserialiser "
    "producing an unexpected concrete type</b> — after which "
    "<b>field offsets, virtual table pointers, and length fields are all "
    "read from the wrong places in memory.</b>",
    "<b>Which is severe for two specific reasons.</b> <b>A virtual "
    "table pointer read from attacker-controlled data is control of "
    "execution</b>, and <b>a length field read from the wrong offset "
    "defeats every bounds check downstream of it</b> — the checks "
    "run, and they compare against the wrong number.",
    "<b>And the common sources are:</b> <b>unchecked downcasts, "
    "tagged unions whose tag is consulted in some places and not others, "
    "deserialisation that produces whatever type the input names "
    "(Module 06), and language runtimes with dynamic typing where a "
    "JIT's type assumption can be violated.</b>",
    "<b>The fix is to make the invalid interpretation "
    "unrepresentable:</b> <b>checked casts that fail loudly, a sum type "
    "the compiler forces you to match exhaustively on, and a parser that "
    "produces a validated domain type rather than a generic "
    "map</b> — which is <b>the parse-don't-validate discipline of "
    "Module 04 &sect;4</b>, arriving here as a type safety "
    "measure."]),
  ("ul", ["<b>Any multiplication or addition on an input-derived value "
          "that reaches an allocation</b> — the canonical pattern "
          "from &sect;1, and the one to search for first.",
          "<b>Any comparison mixing signed and unsigned types</b>, and "
          "<b>any <code>&lt; 0</code> check applied to an unsigned "
          "value</b> — the compiler will warn about both if the "
          "warnings are enabled.",
          "<b>Any assignment from a wider to a narrower integer "
          "type</b>, especially of something that is a length or a count "
          "— which is truncation waiting to happen.",
          "<b>Any cast between pointer types</b>, and <b>any downcast "
          "performed without a check</b> — both of which are "
          "greppable and both of which are usually deliberate and "
          "occasionally wrong.",
          "<b>And any union or tagged variant whose tag is read in one "
          "place and not in another</b>, which is the pattern behind most "
          "union-based type confusion. <b>All five are mechanically "
          "greppable</b>, and <b>the compiler will warn about two of them "
          "if you let it</b> — which is Module 12 &sect;2's "
          "argument for turning the warnings on and treating them as "
          "errors."]),
 ],
 "resources": [
   ("Dowd, McDonald & Schuh, chapter 6",
    "https://www.oreilly.com/library/view/the-art-of/0321444426/",
    "<b>&sect;1 and &sect;2 exhaustively</b> — the best treatment of "
    "C's integer behaviour in a security context. Library copy."),
   ("Wang et al. &mdash; Undefined Behavior: What Happened to My Code? "
    "(free)",
    "https://pdos.csail.mit.edu/papers/ub:apsys12.pdf",
    "<b>&sect;2's last point, demonstrated</b> — real security "
    "checks deleted by real compilers, with the mechanism."),
   ("CERT C Coding Standard, the INT rules (free)",
    "https://wiki.sei.cmu.edu/confluence/display/c",
    "<b>&sect;2's practice as a rule set</b>, with compliant and "
    "non-compliant examples for each case."),
   ("CWE-190, CWE-680, CWE-843 (free)",
    "https://cwe.mitre.org/data/definitions/190.html",
    "<b>&sect;1 and &sect;4 with the shared vocabulary</b> — use "
    "these identifiers when reporting."),
 ],
 "exercises": [
   "<b>Write the canonical overflow defect</b> and confirm the small "
   "allocation with a debugger.",
   "<b>Add the result-based check</b> and show it still passes.",
   "<b>Replace it with the operand-based check</b> and show it "
   "rejects.",
   "<b>Print the value of <code>-1 &lt; 1u</code></b> and explain "
   "it.",
   "<b>Write a <code>&lt; 0</code> check on an unsigned value</b> and "
   "find the compiler warning.",
   "<b>Write an overflow check as <code>a + b &lt; a</code></b> on "
   "signed types, enable optimisation, and see whether it survives.",
   "<b>Enable UndefinedBehaviorSanitizer</b> on an existing project and "
   "report what it finds.",
   "<b>Grep a codebase for multiplications feeding allocations</b> and "
   "assess each.",
   "<b>Write a minimal type confusion</b> through a union, and observe "
   "the wrong field.",
   "<b>Replace it with a tagged sum type</b> the compiler checks.",
 ],
 "selfcheck": [
   "Name the three integer failures and the shared consequence.",
   "Give the canonical defect and the check that does not help.",
   "State the rule about operands and results, and why.",
   "What are C's promotion rules, and why is -1 < 1u false?",
   "Why might a <0 check on an unsigned value disappear?",
   "Why is signed overflow being undefined dangerous for checks?",
   "When does an integer defect become a memory safety defect?",
   "Name the five dangerous sinks.",
   "What is type confusion, and why is it severe?",
   "Give the five review checks.",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Injection and Parsing",
 "subtitle": "One cause, many names, one structural fix.",
 "question": "Why does escaping keep failing?",
 "outcomes": [
     "Explain injection as a parsing problem.",
     "Explain why parameterisation works and escaping is "
     "fragile.",
     "Explain path traversal and command injection.",
     "Explain parse-don't-validate.",
     "Fix an injection structurally rather than locally.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The cause",
   "blurb": "Data becoming structure."},

  {"t": "callout", "title": "Injection happens when data is concatenated into a string that is later parsed as code",
   "kind": "The single cause behind every variant",
   "body": ["<b>The interpreter downstream receives one string and "
            "cannot tell which parts you intended as data and which as "
            "structure</b> — because that information was destroyed "
            "by the concatenation.",
            "<b>So every variant is the same defect at a different "
            "parser:</b> <b>SQL at the database's parser, command "
            "injection at the shell's, XSS at the browser's, and "
            "template injection at the template engine's.</b>",
            "<b>And the reason escaping is fragile is that correct "
            "escaping depends on the destination context</b>, which the "
            "point of concatenation does not reliably know.",
            "<b>Which is why the structural fix is to never build the "
            "string</b> — <b>use an interface that carries data and "
            "structure separately, so the interpreter receives them "
            "distinguished.</b>"]},

  {"t": "code", "kicker": "Interfaces", "title": "The separating interface, per destination",
   "lang": "text", "code": """
  SQL        parameterised queries / prepared
             statements. Always. The query structure
             is fixed before any data is bound.

  SHELL      pass an argument ARRAY, not a string --
             execve-style. Better: do not invoke a
             shell at all.

  HTML       the template engine's contextual
             autoescaping, or a DOM API that takes
             text rather than markup.

  JSON/XML   a serialiser. Never string building.

  FILESYSTEM resolve the path, then verify the result
             is inside the intended directory. Do not
             filter for ".." (Part 3).

  LDAP/XPath the library's parameter binding.

  THE PRINCIPLE: the interface keeps data and structure
  in separate arguments, so no parser has to guess.
""",
   "caption": "<b>Every row is the same idea</b> — separate "
              "arguments rather than one string, so nothing has to be "
              "escaped at all.",
   "note": "Framing all six as one principle is the teaching value."},

  {"t": "section", "label": "Part 2", "title": "Why escaping fails",
   "blurb": "Not because it is wrong, but because it is positional."},

  {"t": "bullets", "kicker": "Escaping", "title": "The specific ways escaping goes wrong",
   "items": [
     "<b>The context changes and the escaping does not.</b> <b>A "
     "value safely escaped for HTML text is unsafe in an attribute, a "
     "URL, a script block, or a CSS value</b> — five contexts, five "
     "escapings.",
     "",
     "<b>Escaping at the input boundary cannot know the "
     "destination</b>, so it escapes for a guess — which is "
     "CSCE 701 Module 06's point.",
     "",
     "<b>Double-escaping and double-decoding</b> — a value "
     "escaped twice and decoded once, or the reverse, and the filter "
     "sees different bytes than the parser.",
     "",
     "<b>Encoding differences:</b> <b>a filter reading UTF-8 and a "
     "parser accepting overlong or alternate encodings</b> of the same "
     "character.",
     "",
     "<b>And a blocklist, which is always incomplete</b> — the "
     "attacker needs the one case you missed.",
   ],
   "footnote": "<b>Escaping is not wrong; it is "
               "<i>positional</i></b> — correct only relative to a "
               "destination, which is why it belongs at the point of use "
               "and in the template engine."},

  {"t": "section", "label": "Part 3", "title": "Paths and commands",
   "blurb": "Two cases with specific correct answers."},

  {"t": "callout", "title": "For paths, resolve first and then check containment",
   "kind": "Rather than filtering the input",
   "body": ["<b>Filtering for '..' fails</b> — because of "
            "encodings, symbolic links, alternate separators, and "
            "platform-specific path syntax, all of which produce a "
            "traversal without the literal sequence.",
            "<b>So: join the untrusted component to the base "
            "directory, canonicalise the result, and then verify the "
            "canonical path is still inside the base.</b>",
            "<b>Which handles symbolic links and encodings together</b> "
            "— because you are checking the <i>resolved</i> "
            "destination rather than predicting it from the "
            "input.",
            "<b>And beware the race:</b> <b>a check-then-open sequence "
            "can have the path replaced in between</b> "
            "(Module 05 §3) — so open first and verify "
            "the handle where the platform permits."]},

  {"t": "callout", "title": "For commands, pass an argument array and do not use a shell",
   "kind": "The one reliable answer",
   "body": ["<b>A shell parses its argument string</b> — for "
            "semicolons, pipes, backticks, substitutions, globs, and "
            "redirections — <b>so any untrusted content in that "
            "string is code.</b>",
            "<b>Passing an argument array bypasses the shell "
            "entirely</b>: the arguments reach the program as "
            "arguments, and no parsing occurs.",
            "<b>And the remaining hazard is argument injection</b> "
            "— <b>an untrusted value that begins with a dash "
            "becomes an option</b>, which has produced real "
            "vulnerabilities even without a shell.",
            "<b>So: argument array, and use <code>--</code> or "
            "validate against a list where the called program accepts "
            "options</b> — and better still, call a library rather "
            "than a program."]},

  {"t": "section", "label": "Part 4", "title": "Parse, don't validate",
   "blurb": "The discipline that prevents the whole family."},

  {"t": "callout", "title": "Parse input into a type that cannot be invalid, rather than checking it and passing it on",
   "kind": "The structural discipline",
   "body": ["<b>Validation checks a value and returns the same "
            "type</b> — so <b>the knowledge that it was checked "
            "lives only in the programmer's head, and the next function "
            "has to check again or assume.</b>",
            "<b>Parsing converts it into a type that can only hold "
            "valid values</b> — an <code>Email</code>, a "
            "<code>UserId</code>, a <code>SafePath</code> — <b>so "
            "the type system carries the guarantee.</b>",
            "<b>Which eliminates Module 01 §2's step-4 "
            "problem:</b> <b>'validated on this path but not that one' "
            "cannot arise, because the only way to obtain the type is "
            "through the parser.</b>",
            "<b>And it is why the injection fixes in "
            "Part 1 work:</b> <b>a prepared statement is a "
            "parsed query with holes, rather than a string hoped to be "
            "well-formed.</b>"]},

  {"t": "bullets", "kicker": "Practice", "title": "Applying it",
   "items": [
     "<b>Validate once, at the boundary, and return a distinct "
     "type</b> — not a string with a comment saying it is "
     "safe.",
     "",
     "<b>Make the unsafe constructor private or awkward</b>, so "
     "that the parsed type cannot be fabricated by accident.",
     "",
     "<b>Push the parse as early as possible</b>, so that the "
     "majority of the code never handles untrusted "
     "representations.",
     "",
     "<b>And accept the narrowest input you can:</b> <b>a "
     "restrictive allowlist beats any blocklist</b>, and it is a "
     "parsing decision rather than a filtering one.",
     "",
     "<b>Which composes with Module 03 §4's type "
     "confusion fix</b> — the same discipline, against a "
     "different failure.",
   ],
   "footnote": "<b>This is the most transferable idea in the "
               "module</b>, and it applies in every language with a type "
               "system worth the name."},
 ],
 "takeaways": [
   "Injection is one defect at many parsers: the concatenation destroyed "
   "the distinction between data and structure.",
   "Every correct fix is the same idea — an interface that carries "
   "data and structure in separate arguments.",
   "Escaping is not wrong but positional: correct only relative to a "
   "destination the input boundary cannot know.",
   "For paths, resolve and then check containment — filtering for "
   "'..' fails on encodings, symlinks, and alternate separators.",
   "For commands, pass an argument array and watch for argument injection "
   "from values beginning with a dash.",
   "Parse into a type that cannot be invalid, so the guarantee lives in "
   "the type system rather than in the programmer's head.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The cause"),
  ("callout", "Injection happens when data is concatenated into a string "
              "that is later parsed as code",
   ["<b>The interpreter downstream receives a single string and cannot "
    "possibly tell which parts you intended as data and which as "
    "structure</b> — because <b>that information was destroyed by "
    "the concatenation itself</b>, before the string ever reached the "
    "parser.",
    "<b>So every variant is the same defect at a different "
    "parser:</b> <b>SQL injection at the database's parser, command "
    "injection at the shell's, cross-site scripting at the browser's "
    "HTML and JavaScript parsers, template injection at the template "
    "engine's, and log injection at whatever reads the log.</b> <b>One "
    "cause, five names.</b>",
    "<b>And the reason escaping is fragile is that correct escaping "
    "depends entirely on the destination context</b> — which the "
    "point of concatenation does not reliably know and which changes "
    "when the code is refactored (&sect;2).",
    "<b>Which is why the structural fix is to never build the string "
    "at all</b> — <b>use an interface that carries data and "
    "structure in separate arguments, so that the interpreter receives "
    "them already distinguished and has nothing to guess.</b>"]),
  ("code", """SQL        parameterised queries / prepared statements.
           Always. The query structure is fixed before
           any data is bound to it.

SHELL      pass an argument ARRAY, not a string --
           execve-style. Better still: do not invoke a
           shell at all (section 3).

HTML       the template engine's contextual
           autoescaping, or a DOM API that takes text
           rather than markup.

JSON/XML   a serialiser. Never string building.

FILESYSTEM resolve the path, then verify the result is
           inside the intended directory. Do NOT filter
           for ".." (section 3).

LDAP/XPath the library's own parameter binding.

THE PRINCIPLE: the interface keeps data and structure in
separate arguments, so that no parser ever has to
guess which is which."""),
  ("p", "<b>Every row is the same idea</b> — <b>separate arguments "
        "rather than one concatenated string, so that nothing has to be "
        "escaped at all</b>. <b>Framing all six as a single principle is "
        "the teaching value of this module</b>, because students who learn "
        "them as six unrelated remedies apply each one only where they "
        "have seen it and miss the seventh parser."),

  ("h1", "2 &nbsp; Why escaping fails"),
  ("ul", ["<b>The context changes and the escaping does not.</b> <b>A "
          "value correctly escaped for HTML text is unsafe when placed in "
          "an attribute, a URL, a script block, or a CSS value</b> — "
          "five contexts with five different correct escapings, and a "
          "template change moves a value between them silently.",
          "<b>Escaping at the input boundary cannot know the "
          "destination</b>, so it escapes for a guess — which is "
          "<b>CSCE 701 Module 06's escape-at-the-point-of-use "
          "argument</b> and is why boundary sanitisation is the wrong "
          "architecture rather than merely an incomplete one.",
          "<b>Double-escaping and double-decoding</b> — a value "
          "escaped twice and decoded once, or the reverse, so that "
          "<b>the filter and the parser see different bytes</b>. This is "
          "the mechanism behind a long sequence of filter bypasses.",
          "<b>Encoding differences:</b> <b>a filter reading strict "
          "UTF-8 while the parser accepts overlong encodings, alternate "
          "representations, or a different character set</b> for the same "
          "character — so the dangerous character is present to one "
          "and absent to the other.",
          "<b>And a blocklist, which is always incomplete</b> — "
          "<b>the attacker needs only the one case you missed</b>, and "
          "the space of cases is defined by someone else's parser. "
          "<b>Escaping is not wrong; it is <i>positional</i></b> — "
          "correct only relative to a destination — <b>which is "
          "exactly why it belongs at the point of use and inside the "
          "template engine</b>, where the destination is known."]),

  ("break",),
  ("h1", "3 &nbsp; Paths and commands"),
  ("callout", "For paths, resolve first and then check containment",
   ["<b>Filtering the input for '..' fails</b> — because of "
    "percent-encodings, double encodings, symbolic links, alternate path "
    "separators, Windows short names, and platform-specific syntax, "
    "<b>all of which produce a traversal without the literal sequence "
    "ever appearing in the input.</b>",
    "<b>So the correct procedure is: join the untrusted component to "
    "the base directory, canonicalise the resulting path fully, and then "
    "verify that the canonical result is still inside the base "
    "directory.</b> <b>Three steps, in that order.</b>",
    "<b>Which handles symbolic links and encodings together</b> — "
    "<b>because you are checking the <i>resolved</i> destination rather "
    "than attempting to predict it from the input</b>, which is the "
    "distinction that makes this approach robust where filtering is "
    "not.",
    "<b>And beware the race:</b> <b>a check-then-open sequence can "
    "have the path replaced between the check and the open</b> — a "
    "time-of-check-to-time-of-use defect (Module 05 &sect;3) — "
    "<b>so open first and verify properties of the resulting handle "
    "where the platform permits it</b>, using the file descriptor rather "
    "than the name."]),
  ("callout", "For commands, pass an argument array and do not use a shell",
   ["<b>A shell parses its argument string</b> — for semicolons, "
    "pipes, backticks, command substitutions, globs, redirections, and "
    "variable expansions — <b>so any untrusted content anywhere in "
    "that string is code, not data.</b>",
    "<b>Passing an argument array bypasses the shell entirely:</b> the "
    "arguments reach the target program as discrete arguments, and "
    "<b>no parsing of the kind above occurs at any point.</b> This is "
    "the <code>execve</code> interface, and most languages expose it "
    "directly.",
    "<b>And the remaining hazard is argument injection</b> — "
    "<b>an untrusted value that begins with a dash is interpreted by the "
    "called program as an option rather than as data</b>, which has "
    "produced real vulnerabilities in programs invoked entirely without "
    "a shell. A filename of <code>--upload-file</code> is not a "
    "filename.",
    "<b>So: an argument array, and use the <code>--</code> separator "
    "or validate against an allowlist where the called program accepts "
    "options</b> — and <b>better still, call a library rather than a "
    "program</b>, which removes the whole interface."]),

  ("h1", "4 &nbsp; Parse, don't validate"),
  ("callout", "Parse input into a type that cannot be invalid, rather than "
              "checking it and passing it on",
   ["<b>Validation checks a value and returns the same type it was "
    "given</b> — a string goes in and a string comes out — so "
    "<b>the knowledge that it was checked exists only in the "
    "programmer's head, and every subsequent function must either check "
    "it again or assume somebody did.</b>",
    "<b>Parsing converts the value into a type that can only hold "
    "valid values</b> — an <code>Email</code>, a "
    "<code>UserId</code>, a <code>SafePath</code>, a "
    "<code>ValidatedQuery</code> — <b>so the type system itself "
    "carries the guarantee</b>, and a function requiring validated input "
    "says so in its signature.",
    "<b>Which eliminates Module 01 &sect;2's step-4 problem "
    "entirely:</b> <b>'validated on this path but not on that one' "
    "cannot arise, because the only way to obtain a value of the type is "
    "to go through the parser</b> — the call graph no longer needs "
    "auditing.",
    "<b>And it explains why the fixes in &sect;1 work:</b> <b>a "
    "prepared statement is a <i>parsed</i> query with typed holes, "
    "rather than a string that everybody hopes is well-formed</b> — "
    "the same discipline, applied by the database driver on your "
    "behalf."]),
  ("ul", ["<b>Validate once, at the boundary, and return a distinct "
          "type</b> — <b>not a string with a comment saying it is "
          "safe</b>, which is the pattern this discipline replaces.",
          "<b>Make the unsafe constructor private, or at least "
          "awkward</b>, so that a value of the parsed type cannot be "
          "fabricated by accident or by a hurried refactor — which "
          "is what makes the guarantee hold over time.",
          "<b>Push the parse as early as possible</b>, so that the "
          "great majority of the code never handles the untrusted "
          "representation at all — and so that the surface requiring "
          "security review shrinks to the parser.",
          "<b>And accept the narrowest input you can:</b> <b>a "
          "restrictive allowlist beats any blocklist</b> (&sect;2), and "
          "<b>it is a parsing decision rather than a filtering one</b> "
          "— you are defining the valid language, not enumerating "
          "the invalid strings.",
          "<b>Which composes with Module 03 &sect;4's type confusion "
          "fix</b> — the same discipline, applied against a "
          "different failure, which is why both modules converge on "
          "it. <b>This is the most transferable idea in the module</b>, "
          "and it applies in every language with a type system worth the "
          "name."]),
 ],
 "resources": [
   ("OWASP &mdash; the injection cheat sheets (free)",
    "https://cheatsheetseries.owasp.org/",
    "<b>&sect;1 through &sect;3 as current, specific guidance</b> per "
    "destination — maintained, and the right reference to hand a "
    "team."),
   ("King &mdash; Parse, Don't Validate (free)",
    "https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/",
    "<b>&sect;4 in the original</b> — short, and it reframes input "
    "handling permanently."),
   ("Dowd, McDonald & Schuh, chapters 8 and 17",
    "https://www.oreilly.com/library/view/the-art-of/0321444426/",
    "<b>&sect;2 and &sect;3's specifics</b> — encoding confusion and "
    "path handling, in more detail than anywhere else. Library copy."),
   ("Google's safe-by-construction libraries writeup (free)",
    "https://security.googleblog.com/2021/09/an-update-on-memory-safety-in-chrome.html",
    "<b>&sect;4 at scale</b> — types that make injection "
    "unrepresentable, deployed across a large codebase."),
 ],
 "exercises": [
   "<b>Write a SQL injection against your own test database</b> and then "
   "fix it with parameterisation.",
   "<b>Explain why the parameterised version cannot be injected</b>, "
   "mechanically.",
   "<b>Take one value and escape it correctly for five HTML "
   "contexts</b>, and note that all five differ.",
   "<b>Construct a double-decoding bypass</b> of a filter you wrote.",
   "<b>Write a path traversal that contains no '..'</b> — using "
   "encoding or a symlink.",
   "<b>Implement resolve-then-contain</b> and confirm it rejects "
   "both.",
   "<b>Invoke a program with a shell and with an argument array</b>, and "
   "compare what a semicolon does.",
   "<b>Demonstrate argument injection</b> with a value beginning with a "
   "dash.",
   "<b>Convert one validation function into a parser</b> returning a "
   "distinct type.",
   "<b>Make its unsafe constructor private</b> and fix whatever stops "
   "compiling.",
 ],
 "selfcheck": [
   "State the single cause of injection and name five parsers.",
   "Why can the downstream parser not tell data from structure?",
   "Give the separating interface for six destinations.",
   "Give five specific ways escaping fails.",
   "Why is escaping positional rather than wrong?",
   "Why does filtering for '..' fail, and what works?",
   "What is the remaining hazard after removing the shell?",
   "Contrast validation with parsing.",
   "Which problem from Module 01 does parsing eliminate?",
   "Why is a prepared statement an instance of parse-don't-validate?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Concurrency Defects",
 "subtitle": "Races with security consequences.",
 "question": "Which races are vulnerabilities?",
 "outcomes": [
     "Explain data races and their undefined behaviour.",
     "Explain atomicity violations above the data race "
     "level.",
     "Explain time-of-check-to-time-of-use.",
     "Explain why these are hard to find and to fix.",
     "Identify the security-relevant races in code.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Data races",
   "blurb": "The low-level case, and what it actually costs."},

  {"t": "callout", "title": "A data race is undefined behaviour, not merely a wrong value",
   "kind": "Why it is worse than it looks",
   "body": ["<b>Two threads accessing the same location "
            "concurrently, at least one writing, with no "
            "synchronisation</b> — and in C, C++, and Rust's "
            "unsafe subset this is <b>undefined behaviour rather than an "
            "unspecified result.</b>",
            "<b>So the compiler may assume it does not happen</b> "
            "— and <b>may cache a value in a register, reorder the "
            "accesses, or split a write into two</b>, none of which your "
            "reasoning accounted for.",
            "<b>Which means a torn pointer or a half-updated length is "
            "possible</b>, and that is immediately a memory safety "
            "problem (Module 02) rather than a logic one.",
            "<b>And the practical consequence is severity:</b> <b>a "
            "race on a size field, a reference count, or a state machine "
            "variable produces exactly the defects of "
            "Modules 02 and 03</b>, by a different route."]},

  {"t": "bullets", "kicker": "Patterns", "title": "The patterns that produce them",
   "items": [
     "<b>A reference count updated without atomics</b> — "
     "which produces double free or premature free, and is a classic "
     "source of use-after-free.",
     "",
     "<b>Lazy initialisation without synchronisation</b> — "
     "the double-checked locking pattern, which is wrong without the "
     "right memory ordering.",
     "",
     "<b>A shared cache or buffer reused across requests</b>, "
     "which leaks one user's data to another — a confidentiality "
     "defect from a concurrency bug.",
     "",
     "<b>Signal handlers touching non-atomic state</b>, which is a "
     "race with yourself.",
     "",
     "<b>And <code>fork</code> in a threaded program</b>, which "
     "inherits locks in arbitrary states.",
   ],
   "footnote": "<b>The shared-buffer case is the one with the most "
               "surprising impact</b> — it is a cross-user data "
               "disclosure that looks like a performance "
               "optimisation."},

  {"t": "section", "label": "Part 2", "title": "Atomicity violations",
   "blurb": "Correct locking, wrong granularity."},

  {"t": "callout", "title": "Every individual access can be synchronised and the sequence still be wrong",
   "kind": "The level above data races",
   "body": ["<b>Check the balance under a lock, release it, then "
            "deduct under the lock again</b> — <b>no data race, and "
            "the balance may have changed in between.</b>",
            "<b>So the invariant spans more than one "
            "operation</b>, and the lock has to span the invariant rather "
            "than each access — which is a design question that no "
            "race detector asks.",
            "<b>And this is the security-relevant case in managed "
            "languages</b>, where data races are prevented by the "
            "runtime and atomicity violations are not.",
            "<b>Which makes it the harder class to find:</b> "
            "<b>ThreadSanitizer finds data races and does not know what "
            "your invariant was</b> (Module 09 §3)."]},

  {"t": "code", "kicker": "Shapes", "title": "The shapes to recognise",
   "lang": "text", "code": """
  CHECK-THEN-ACT
      if (balance >= amount)     // lock held, released
          balance -= amount;     // lock taken again
      The gap is the defect.

  READ-MODIFY-WRITE
      x = get(); x++; set(x);
      Two updates interleave; one is lost.

  DOUBLE SPEND / DOUBLE REDEEM
      the same voucher, request, or token processed
      twice because the "already used" check and the
      marking are not atomic. Very common in web
      applications, and a direct financial defect.

  AND THE FIXES
      hold the lock across the whole invariant
      or use a single atomic operation (compare-and-swap)
      or make the operation idempotent, so a repeat is
          harmless (CSCE 678 Module 07)
      or enforce uniqueness in the database with a
          constraint, which is atomic for free
""",
   "caption": "<b>The database constraint is the underrated fix</b> "
              "— a unique index makes double redemption impossible "
              "without any application locking.",
   "note": "The constraint-based fix is the one practitioners "
           "forget."},

  {"t": "section", "label": "Part 3", "title": "TOCTTOU",
   "blurb": "The filesystem case, and the general one."},

  {"t": "callout", "title": "A property checked and then relied upon may change in between",
   "kind": "Time-of-check-to-time-of-use",
   "body": ["<b>Check that a path is not a symbolic link, then open "
            "it</b> — and an adversary who can replace the path "
            "between the two operations defeats the check "
            "entirely.",
            "<b>Which generalises beyond files:</b> <b>check a "
            "permission then act, check a quota then allocate, validate "
            "a URL then fetch it</b> — all the same shape.",
            "<b>And the fix is to make the check and the use one "
            "operation</b> — <b>open the file and then inspect the "
            "descriptor, use <code>openat</code> with the right flags, "
            "or hold a lock across both.</b>",
            "<b>The general principle: operate on the handle, not on "
            "the name</b> — <b>because the name is a lookup that can "
            "resolve differently next time, and the handle is the thing "
            "you actually checked.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Why they are hard",
   "blurb": "And what actually helps."},

  {"t": "bullets", "kicker": "Difficulty", "title": "Why these resist the usual methods",
   "items": [
     "<b>They are non-deterministic</b>, so a test that passes "
     "proves nothing and a failure may not reproduce.",
     "",
     "<b>They are timing-dependent</b>, so they appear under load "
     "and in production rather than on a developer's "
     "machine.",
     "",
     "<b>Fuzzing finds them poorly</b>, because the input space "
     "that matters is the <i>interleaving</i> rather than the data "
     "(Module 08 §4).",
     "",
     "<b>And static analysis finds them poorly</b>, because it "
     "requires reasoning about all interleavings, which is where "
     "CSCE 627's undecidability bites hardest.",
     "",
     "<b>What helps:</b> <b>ThreadSanitizer, stress testing with "
     "artificial delays, and reducing shared mutable state so there is "
     "less to get wrong.</b>",
   ],
   "footnote": "<b>Reducing shared mutable state is the structural "
               "answer</b> — message passing and immutability remove "
               "the class rather than detecting instances of it."},

  {"t": "callout", "title": "And what a safe language does and does not prevent",
   "kind": "Stating it precisely",
   "body": ["<b>Rust's ownership system prevents data races in safe "
            "code</b> — which is a real and unusual guarantee, and "
            "it covers Part 1 entirely.",
            "<b>It does not prevent atomicity violations, deadlocks, "
            "or TOCTTOU</b> — <b>those are logic defects, and the "
            "type system does not know your invariant.</b>",
            "<b>And managed languages prevent torn values</b> and "
            "therefore the memory-unsafe consequences, while leaving "
            "every logical race intact.",
            "<b>So the honest claim is 'no data races in safe code', "
            "and Parts 2 and 3 remain your "
            "problem</b> — which is the same shape of claim as "
            "Module 02 §4's and is worth stating with the "
            "same precision."]},
 ],
 "takeaways": [
   "A data race is undefined behaviour, so the compiler may cache, "
   "reorder, or split accesses — producing torn pointers and lengths.",
   "A race on a size field or a reference count produces the defects of "
   "Modules 02 and 03 by a different route.",
   "Every individual access can be synchronised and the sequence still be "
   "wrong, which is the atomicity violation level.",
   "A unique database constraint is the underrated fix for double "
   "redemption — atomic without any application locking.",
   "Operate on the handle rather than the name, because the name is a "
   "lookup that can resolve differently next time.",
   "Rust prevents data races in safe code and does not prevent atomicity "
   "violations, deadlocks, or TOCTTOU.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Data races"),
  ("callout", "A data race is undefined behaviour, not merely a wrong value",
   ["<b>Two threads accessing the same memory location concurrently, "
    "with at least one of them writing, and no synchronisation between "
    "them</b> — and in C, C++, and Rust's unsafe subset this is "
    "<b>undefined behaviour rather than merely an unspecified "
    "result.</b> The distinction matters enormously.",
    "<b>So the compiler is entitled to assume it does not "
    "happen</b> — and <b>may therefore cache a value in a register "
    "across what you believed was a synchronisation point, reorder the "
    "accesses, or split a single write into two instructions</b>, none of "
    "which your reasoning about the code accounted for.",
    "<b>Which means a torn pointer or a half-updated length field is "
    "entirely possible</b>, and <b>that is immediately a memory safety "
    "problem</b> (Module 02) rather than a logic one — a pointer "
    "half-written is a pointer to somewhere arbitrary.",
    "<b>And the practical consequence is severity:</b> <b>a race on a "
    "size field, a reference count, or a state machine variable produces "
    "exactly the defects of Modules 02 and 03, arriving by a different "
    "route</b> — which is why concurrency gets a module in a "
    "software security course rather than being left to the operating "
    "systems one."]),
  ("ul", ["<b>A reference count updated without atomic "
          "operations</b> — which produces either a double free or a "
          "premature free, and <b>is a classic source of "
          "use-after-free</b> in reference-counted C++ code.",
          "<b>Lazy initialisation without proper "
          "synchronisation</b> — the double-checked locking pattern, "
          "<b>which is simply wrong without the correct memory "
          "ordering</b> and was wrong in published textbooks for years "
          "before the memory models were formalised.",
          "<b>A shared cache or scratch buffer reused across "
          "requests</b>, which <b>leaks one user's data to "
          "another</b> — a confidentiality defect arising directly "
          "from a concurrency bug, and the one with the most surprising "
          "impact because <b>it looks like a performance "
          "optimisation</b> in review.",
          "<b>Signal handlers touching non-atomic state</b>, which is "
          "a race with yourself rather than with another thread — and "
          "which is why the set of functions safe to call from a handler "
          "is so small.",
          "<b>And <code>fork</code> in a threaded program</b>, which "
          "produces a child inheriting locks in arbitrary states, held by "
          "threads that no longer exist — a deadlock or a corrupted "
          "invariant at unpredictable times."]),

  ("h1", "2 &nbsp; Atomicity violations"),
  ("callout", "Every individual access can be synchronised and the sequence "
              "still be wrong",
   ["<b>Check the balance while holding a lock, release the lock, then "
    "deduct the amount while holding the lock again</b> — <b>there "
    "is no data race anywhere, every access is properly synchronised, "
    "and the balance may have changed in between the two.</b>",
    "<b>So the invariant spans more than one operation</b>, which "
    "means <b>the lock has to span the invariant rather than each "
    "individual access</b> — and that is a design question that no "
    "automated race detector can ask, because it does not know what the "
    "invariant was supposed to be.",
    "<b>And this is the security-relevant concurrency case in managed "
    "languages</b>, where <b>data races are prevented by the runtime and "
    "atomicity violations are not</b> — so a Java or Go service has "
    "no torn values and every double-spend defect available.",
    "<b>Which makes it the harder class to find:</b> "
    "<b>ThreadSanitizer finds data races very effectively and has no "
    "idea what your invariant was</b> (Module 09 &sect;3) — so "
    "this class is found by reasoning and by review (Module 11) "
    "rather than by tooling."]),
  ("code", """CHECK-THEN-ACT
    if (balance >= amount)     // lock held, released
        balance -= amount;     // lock taken again
    The gap between them is the defect.

READ-MODIFY-WRITE
    x = get(); x++; set(x);
    Two concurrent updates interleave; one is lost.

DOUBLE SPEND / DOUBLE REDEEM
    the same voucher, request, or token processed twice
    because the "already used" check and the marking as
    used are not atomic. Very common in web
    applications, and a direct financial defect.

AND THE FIXES
    hold the lock across the whole invariant
    or use a single atomic operation (compare-and-swap)
    or make the operation idempotent, so that a repeat
        is harmless (CSCE 678 Module 07)
    or enforce uniqueness in the database with a
        constraint, which is atomic for free"""),
  ("p", "<b>The database constraint is the underrated fix.</b> <b>A "
        "unique index on the redemption record makes double redemption "
        "impossible without any application-level locking at all</b> "
        "— the second insert fails, the transaction rolls back, and "
        "the invariant is enforced by the one component that is already "
        "designed to do exactly this. <b>Practitioners reliably reach for "
        "a lock and forget the constraint</b>, which is both more complex "
        "and less reliable across multiple application instances "
        "(CSCE 678 Module 04)."),

  ("break",),
  ("h1", "3 &nbsp; Time-of-check-to-time-of-use"),
  ("callout", "A property checked and then relied upon may change in between",
   ["<b>Check that a path is not a symbolic link, then open it</b> "
    "— and <b>an adversary who can replace the path between those "
    "two operations defeats the check entirely</b>, because the check "
    "examined a different object than the open received.",
    "<b>Which generalises well beyond the filesystem:</b> <b>check a "
    "permission then act on it, check a quota then allocate, validate a "
    "URL then fetch it, verify a file's hash then execute "
    "it</b> — all exactly the same shape, and all defeated by a "
    "change in between.",
    "<b>And the fix is to make the check and the use a single "
    "operation</b> — <b>open the file and then inspect the resulting "
    "descriptor, use <code>openat</code> with <code>O_NOFOLLOW</code> "
    "and the appropriate flags, or hold a lock across both "
    "operations</b> so that no change can intervene.",
    "<b>The general principle: operate on the handle, not on the "
    "name</b> — <b>because the name is a lookup that can resolve "
    "differently the next time it is performed, and the handle is the "
    "actual thing you checked.</b> <b>Which is the same reasoning as "
    "Module 04 &sect;3's resolve-then-contain</b>, and the two "
    "modules' advice composes: resolve, open, then verify the "
    "descriptor."]),

  ("h1", "4 &nbsp; Why they are hard, and what helps"),
  ("ul", ["<b>They are non-deterministic</b>, so <b>a test that passes "
          "proves nothing at all</b> and a failure may not reproduce on "
          "demand — which breaks the normal debugging loop "
          "entirely.",
          "<b>They are timing-dependent</b>, so they appear under "
          "production load and on different hardware rather than on a "
          "developer's machine — which means they are found by users "
          "and by incidents.",
          "<b>Fuzzing finds them poorly</b>, because <b>the input "
          "space that matters is the <i>interleaving</i> rather than the "
          "data</b> (Module 08 &sect;4), and a conventional fuzzer "
          "varies only the data.",
          "<b>And static analysis finds them poorly</b>, because it "
          "requires sound reasoning about all possible interleavings "
          "— <b>which is where CSCE 627's undecidability results "
          "bite hardest</b>, and why concurrency analysers have either "
          "very high false positive rates or very narrow scope.",
          "<b>What helps:</b> <b>ThreadSanitizer for the data races, "
          "stress testing with artificially injected delays at suspicious "
          "points, and reducing shared mutable state so that there is "
          "less to get wrong.</b> <b>Reducing shared mutable state is "
          "the structural answer</b> — message passing and "
          "immutability <b>remove the class rather than detecting "
          "instances of it</b>, which is the same move as "
          "Module 02 &sect;4's and is available in any language."]),
  ("callout", "And what a safe language does and does not prevent",
   ["<b>Rust's ownership and borrowing system prevents data races in "
    "safe code</b> — which is a real and genuinely unusual "
    "guarantee, not shared by the managed languages — and <b>it "
    "covers &sect;1 entirely.</b>",
    "<b>It does not prevent atomicity violations, deadlocks, or "
    "time-of-check-to-time-of-use defects</b> — <b>those are logic "
    "defects, and the type system does not know what your invariant "
    "was.</b> A Rust program can double-spend exactly as readily as a C "
    "one.",
    "<b>And the managed languages prevent torn values</b> and "
    "therefore the memory-unsafe consequences of &sect;1, <b>while "
    "leaving every logical race entirely intact</b> — which is a "
    "weaker guarantee than Rust's and still removes the severe "
    "cases.",
    "<b>So the honest claim is 'no data races in safe code', and "
    "&sect;2 and &sect;3 remain your problem</b> — <b>which is the "
    "same shape of claim as Module 02 &sect;4's and deserves the same "
    "precision</b>, because the broad version ('Rust is safe') leads "
    "teams to stop thinking about the classes that remain."]),
 ],
 "resources": [
   ("Boehm &mdash; Threads Cannot Be Implemented As a Library (free)",
    "https://www.hpl.hp.com/techreports/2004/HPL-2004-209.pdf",
    "<b>&sect;1's argument for why the memory model must be in the "
    "language</b> — and why a data race is undefined rather than "
    "merely unlucky."),
   ("Lu et al. &mdash; Learning from Mistakes: a study of real-world "
    "concurrency bugs (free)",
    "https://dl.acm.org/doi/10.1145/1346281.1346323",
    "<b>&sect;2's classification, measured</b> — the study that "
    "established atomicity violations as the dominant real-world "
    "class."),
   ("ThreadSanitizer documentation (free)",
    "https://clang.llvm.org/docs/ThreadSanitizer.html",
    "<b>&sect;4's primary tool</b> — what it detects, what it "
    "misses, and its cost."),
   ("CWE-362, CWE-367, CWE-416 (free)",
    "https://cwe.mitre.org/data/definitions/362.html",
    "<b>&sect;2 and &sect;3 with the shared vocabulary</b> — race "
    "condition, TOCTTOU, and use-after-free."),
 ],
 "exercises": [
   "<b>Write a non-atomic reference count</b> and produce a double free "
   "under load.",
   "<b>Catch it with ThreadSanitizer</b> and read the report.",
   "<b>Write a shared scratch buffer</b> and demonstrate cross-request "
   "data leakage.",
   "<b>Write a check-then-act double spend</b> and exploit it with "
   "concurrent requests.",
   "<b>Fix it four ways:</b> wider lock, compare-and-swap, idempotency, "
   "and a unique constraint.",
   "<b>Compare the four fixes</b> for complexity and for behaviour across "
   "multiple instances.",
   "<b>Write a TOCTTOU against your own test directory</b> using a "
   "symlink swap.",
   "<b>Fix it by operating on the descriptor.</b>",
   "<b>Try fuzzing a racy program</b> and report whether the race was "
   "found.",
   "<b>State precisely what Rust prevents</b> and what it does not.",
 ],
 "selfcheck": [
   "Why is a data race undefined behaviour, and what may the compiler "
   "do?",
   "How does a race become a memory safety defect?",
   "Name five patterns that produce data races.",
   "Why is the shared-buffer case surprising?",
   "What is an atomicity violation, and why does ThreadSanitizer miss "
   "it?",
   "Give three shapes and four fixes.",
   "Why is the database constraint underrated?",
   "Explain TOCTTOU and give the general principle.",
   "Give four reasons these defects resist the usual methods.",
   "State precisely what a safe language prevents here.",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Deserialisation and Trust Boundaries",
 "subtitle": "Reconstructing objects from hostile bytes.",
 "question": "What happens when you deserialise untrusted data?",
 "outcomes": [
     "Explain why native deserialisation is dangerous.",
     "Explain gadget chains conceptually.",
     "Explain the safe alternatives.",
     "Explain SSRF and the confused deputy at this layer.",
     "Audit a trust boundary crossing.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why it is dangerous",
   "blurb": "Because it is code, not data."},

  {"t": "callout", "title": "Native deserialisation lets the input choose which types to construct and which methods to run",
   "kind": "The mechanism",
   "body": ["<b>A native serialisation format encodes the class as "
            "well as the data</b> — so <b>the input decides what "
            "gets instantiated</b>, which is a very large amount of "
            "authority to hand to a byte stream.",
            "<b>And construction runs code.</b> <b>Constructors, "
            "setters, validation hooks, and finalisers all execute during "
            "deserialisation</b> — before your code has seen the "
            "resulting object or had any chance to check it.",
            "<b>So the attacker's problem reduces to finding a "
            "reachable class whose construction or disposal does "
            "something useful</b> — and in a large dependency tree, "
            "such classes exist (Part 2).",
            "<b>Which is why the rule is categorical:</b> <b>never "
            "deserialise untrusted data with a format that encodes "
            "types</b> — Java's native serialisation, Python's "
            "<code>pickle</code>, PHP's <code>unserialize</code>, .NET's "
            "<code>BinaryFormatter</code>, Ruby's Marshal."]},

  {"t": "bullets", "kicker": "Gadgets", "title": "Gadget chains, in concept",
   "items": [
     "<b>A 'gadget' is a class already present in the application "
     "or its dependencies whose deserialisation has a side "
     "effect</b> — it writes a file, makes a request, or invokes "
     "a method on another object.",
     "",
     "<b>A chain composes several</b>, so that the side effects "
     "add up to something the attacker wants — typically code "
     "execution.",
     "",
     "<b>And the attacker needs no vulnerability in your "
     "code.</b> <b>The gadgets are ordinary, correct classes behaving "
     "as designed</b>, assembled in an order their authors never "
     "considered.",
     "",
     "<b>Which is why the dependency tree matters here</b> "
     "— <b>adding a library adds gadgets</b> "
     "(CSCE 701 Module 08 §1).",
     "",
     "<b>And why an allowlist of permitted classes is the only "
     "mitigation that works</b>, if you cannot change the format.",
   ],
   "footnote": "<b>The key insight is that no component is "
               "buggy</b> — which is why this defect is invisible to "
               "any analysis that examines components "
               "individually."},

  {"t": "section", "label": "Part 2", "title": "The alternatives",
   "blurb": "What to use instead."},

  {"t": "code", "kicker": "Alternatives", "title": "Safe deserialisation, in order of preference",
   "lang": "text", "code": """
  BEST: A DATA-ONLY FORMAT, PARSED INTO A KNOWN TYPE
      JSON, Protocol Buffers, MessagePack, CBOR --
      formats that encode DATA and not TYPES.
      Then parse into a type you named in your own
      code (Module 04 section 4).

  ALSO FINE: A SCHEMA
      Protobuf or Avro with a declared schema. The
      shape is fixed by your code, not by the input.

  IF YOU CANNOT CHANGE THE FORMAT
      an allowlist of permitted classes, enforced
      during deserialisation -- not a blocklist of
      known gadgets, which is always incomplete

  AND IN EVERY CASE
      authenticate the data before deserialising it,
      if it crossed a boundary you control both ends
      of (CSCE 711 Module 04) -- a MAC makes the
      question of trust answerable
""",
   "caption": "<b>'Encodes data, not types' is the test</b> — and "
              "it immediately classifies every format you are likely to "
              "encounter.",
   "note": "The data-versus-types test is the portable version of the "
           "rule."},

  {"t": "callout", "title": "And a MAC turns untrusted data into data you can reason about",
   "kind": "Where you control both ends",
   "body": ["<b>If you serialised it and you will deserialise it, "
            "authenticate it</b> — a MAC over the serialised bytes, "
            "verified before any parsing "
            "(CSCE 711 Module 04 §4).",
            "<b>Which converts 'untrusted input' into 'input we "
            "produced'</b> — and that is a genuinely different "
            "trust category rather than a mitigation.",
            "<b>This is why signed cookies and signed tokens "
            "work</b>, and why the signature must be verified "
            "<i>before</i> the payload is parsed rather than "
            "after.",
            "<b>But it does not help where the data genuinely comes "
            "from elsewhere</b> — a third party, a user upload, a "
            "message from another organisation — where "
            "Part 2's format choice is the only "
            "answer."]},

  {"t": "section", "label": "Part 3", "title": "SSRF",
   "blurb": "The confused deputy at the network layer."},

  {"t": "callout", "title": "Server-side request forgery: your server fetches a URL the user chose",
   "kind": "Why it is severe",
   "body": ["<b>The request originates inside your network, from a "
            "host with your server's network position and "
            "credentials</b> — so it reaches internal services that "
            "are not exposed externally.",
            "<b>Which is the confused deputy pattern</b> "
            "(CSCE 701 Module 03 §2): <b>the server "
            "acts on its own authority on behalf of a requester who does "
            "not hold it.</b>",
            "<b>And the cloud metadata endpoint makes it "
            "worse</b> — a link-local address that returns "
            "credentials to any process that asks, which turns an SSRF "
            "into credential theft.",
            "<b>So the defences are:</b> <b>an allowlist of permitted "
            "destinations, resolution and validation of the resolved "
            "address rather than the hostname, blocking redirects, and "
            "egress filtering</b> "
            "(CSCE 701 Module 04 §2)."]},

  {"t": "bullets", "kicker": "SSRF", "title": "And the specific pitfalls",
   "items": [
     "<b>Validating the hostname rather than the resolved "
     "address</b> — DNS can return an internal address for a name "
     "you permitted.",
     "",
     "<b>And DNS rebinding:</b> <b>the name resolves to a "
     "permitted address when you check and an internal one when you "
     "connect</b> — which is Module 05 §3's "
     "TOCTTOU at the network layer.",
     "",
     "<b>Following redirects</b>, which lets the first response "
     "choose the second destination.",
     "",
     "<b>Alternative schemes</b> — <code>file:</code>, "
     "<code>gopher:</code>, and others, which reach things HTTP does "
     "not.",
     "",
     "<b>And IPv6, decimal, and octal address encodings</b>, which "
     "defeat textual filters.",
   ],
   "footnote": "<b>DNS rebinding is the pitfall that makes "
               "address-checking insufficient on its own</b> — the "
               "robust answer is to connect to a validated address "
               "directly, not to a name."},

  {"t": "section", "label": "Part 4", "title": "Auditing a boundary",
   "blurb": "The general method."},

  {"t": "bullets", "kicker": "Method", "title": "Questions to ask at every trust boundary crossing",
   "items": [
     "<b>What format is the data in, and does that format encode "
     "types or behaviour?</b>",
     "",
     "<b>Is it authenticated, and is the authentication verified "
     "before parsing?</b>",
     "",
     "<b>What type does it become, and was that type named by my "
     "code or by the input?</b>",
     "",
     "<b>What does the parsing itself do</b> — allocate based "
     "on a declared length, decompress, construct objects, resolve "
     "references?",
     "",
     "<b>And whose authority is used to act on it</b> — the "
     "requester's or the process's? (Part 3's confused "
     "deputy.)",
   ],
   "footnote": "<b>The last question generalises this whole "
               "module</b> — deserialisation and SSRF are both the "
               "same error: acting with your own authority on a "
               "requester's instruction."},
 ],
 "takeaways": [
   "Native serialisation encodes types, so the input chooses what to "
   "construct, and construction runs code before you see the object.",
   "A gadget chain uses ordinary, correct classes assembled in an order "
   "their authors never considered — no component is buggy.",
   "'Encodes data, not types' is the test that classifies every "
   "serialisation format you will meet.",
   "A MAC verified before parsing converts untrusted input into input you "
   "produced, which is a different trust category.",
   "SSRF is the confused deputy at the network layer, and the cloud "
   "metadata endpoint turns it into credential theft.",
   "DNS rebinding defeats address checking, so connect to a validated "
   "address rather than to a name.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why native deserialisation is dangerous"),
  ("callout", "Native deserialisation lets the input choose which types to "
              "construct and which methods to run",
   ["<b>A native serialisation format encodes the class as well as the "
    "data</b> — that is what makes it convenient — so <b>the "
    "input decides what gets instantiated</b>, which is an extraordinary "
    "amount of authority to hand to a byte stream from outside your "
    "system.",
    "<b>And construction runs code.</b> <b>Constructors, property "
    "setters, validation hooks, custom readObject methods, and finalisers "
    "all execute during deserialisation</b> — <b>before your code "
    "has seen the resulting object or had any opportunity to inspect "
    "it</b>, which means no amount of post-deserialisation validation "
    "helps.",
    "<b>So the attacker's problem reduces to finding a reachable class "
    "whose construction or disposal does something useful</b> — and "
    "<b>in a large dependency tree, such classes reliably exist</b> "
    "(&sect;1's gadget discussion below).",
    "<b>Which is why the rule is categorical rather than "
    "conditional:</b> <b>never deserialise untrusted data with a format "
    "that encodes types</b> — Java's native serialisation, Python's "
    "<code>pickle</code>, PHP's <code>unserialize</code>, .NET's "
    "<code>BinaryFormatter</code>, Ruby's <code>Marshal</code>. "
    "<b>Several of these are now deprecated by their own platforms for "
    "exactly this reason</b>, which is unusual and tells you how bad it "
    "is."]),
  ("ul", ["<b>A 'gadget' is a class already present in your "
          "application or its dependencies whose deserialisation has a "
          "side effect</b> — it writes a file, opens a network "
          "connection, invokes a method on another object it holds, or "
          "triggers a lookup.",
          "<b>A chain composes several of them</b>, so that the side "
          "effects compose into something the attacker wants — "
          "typically arbitrary code execution, reached through four or "
          "five entirely ordinary classes.",
          "<b>And the attacker needs no vulnerability in your code at "
          "all.</b> <b>The gadgets are ordinary, correct classes "
          "behaving exactly as designed</b>, assembled in an order and a "
          "combination their authors never considered and had no reason "
          "to.",
          "<b>Which is precisely why the dependency tree matters "
          "here</b> — <b>adding a library adds gadgets</b>, and the "
          "gadget surface grows with the transitive closure "
          "(CSCE 701 Module 08 &sect;1's trust argument, arriving "
          "with a specific consequence).",
          "<b>And why an allowlist of permitted classes is the only "
          "mitigation that works</b> if you cannot change the format "
          "— <b>a blocklist of known gadget classes is always "
          "incomplete</b>, because new chains are found in existing "
          "libraries regularly. <b>The key insight is that no component "
          "is buggy</b>, which is why <b>this defect is invisible to any "
          "analysis that examines components individually</b> — and "
          "is Module 01 &sect;1's composition cause in its purest "
          "form."]),

  ("h1", "2 &nbsp; The alternatives"),
  ("code", """BEST: A DATA-ONLY FORMAT, PARSED INTO A KNOWN TYPE
    JSON, Protocol Buffers, MessagePack, CBOR --
    formats that encode DATA and not TYPES.
    Then parse into a type you named in your own code
    (Module 04 section 4's discipline).

ALSO FINE: A SCHEMA
    Protobuf or Avro with a declared schema. The shape
    is fixed by your code rather than by the input.

IF YOU CANNOT CHANGE THE FORMAT
    an allowlist of permitted classes, enforced during
    deserialisation -- NOT a blocklist of known
    gadgets, which is always incomplete

AND IN EVERY CASE
    authenticate the data before deserialising it, if
    it crossed a boundary you control both ends of
    (CSCE 711 Module 04) -- a MAC makes the question
    of trust actually answerable"""),
  ("p", "<b>'Encodes data, not types' is the test</b>, and <b>it "
        "immediately classifies every serialisation format you are likely "
        "to encounter</b> — which makes it the portable version of "
        "the rule, usable in a language you have never written. <b>Note "
        "that a data-only format can still be misused</b>: a JSON "
        "document whose contents name a class your code then looks up and "
        "instantiates has reintroduced the whole problem, and this pattern "
        "appears in several real frameworks' polymorphic deserialisation "
        "features."),
  ("callout", "And a MAC turns untrusted data into data you can reason about",
   ["<b>If you serialised it and you are the one who will deserialise "
    "it, authenticate it</b> — a MAC computed over the serialised "
    "bytes, <b>verified before any parsing occurs</b> (CSCE 711 "
    "Module 04 &sect;4's ordering rule).",
    "<b>Which converts 'untrusted input' into 'input we "
    "produced'</b> — and <b>that is a genuinely different trust "
    "category rather than a mitigation applied to the same "
    "category.</b> The question 'can an attacker influence this' now has "
    "the answer 'no'.",
    "<b>This is exactly why signed cookies and signed tokens "
    "work</b>, and <b>why the signature must be verified before the "
    "payload is parsed rather than after</b> — a token whose claims "
    "are read first and verified second has already acted on "
    "attacker-controlled data.",
    "<b>But it does not help at all where the data genuinely "
    "originates elsewhere</b> — a third-party API, a user upload, a "
    "message from another organisation — <b>where &sect;2's format "
    "choice is the only available answer</b>, and where the temptation to "
    "use the convenient native format is strongest."]),

  ("break",),
  ("h1", "3 &nbsp; Server-side request forgery"),
  ("callout", "Server-side request forgery: your server fetches a URL the "
              "user chose",
   ["<b>The request originates inside your network, from a host "
    "holding your server's network position and its credentials</b> "
    "— so <b>it reaches internal services that are deliberately not "
    "exposed externally</b>, and those services frequently have weak or "
    "absent authentication precisely because they are internal "
    "(CSCE 701 Module 04 &sect;2).",
    "<b>Which is the confused deputy pattern</b> (CSCE 701 "
    "Module 03 &sect;2): <b>the server acts on its own authority on "
    "behalf of a requester who does not hold that authority</b> — "
    "the identical structure as CSRF, path traversal, and missing object "
    "checks, at the network layer.",
    "<b>And the cloud metadata endpoint makes it considerably "
    "worse</b> — <b>a link-local address that returns credentials "
    "to any process on the host that asks for them</b>, which turns a "
    "URL-fetching feature into credential theft and then into whatever "
    "those credentials permit.",
    "<b>So the defences are:</b> <b>an allowlist of permitted "
    "destinations, resolution of the hostname followed by validation of "
    "the <i>resolved address</i> rather than the name, refusing to follow "
    "redirects, and egress filtering at the network level</b> "
    "(CSCE 701 Module 04 &sect;2) — and the egress filtering is "
    "what limits the damage when the application-level checks are "
    "bypassed."]),
  ("ul", ["<b>Validating the hostname rather than the resolved "
          "address</b> — <b>DNS can return an internal address for a "
          "name you permitted</b>, and an attacker who controls a domain "
          "controls what it resolves to.",
          "<b>And DNS rebinding:</b> <b>the name resolves to a "
          "permitted external address when you check it and to an "
          "internal address when you connect</b> — which is "
          "<b>Module 05 &sect;3's TOCTTOU arriving at the network "
          "layer</b>, and is the pitfall that makes address-checking "
          "insufficient on its own.",
          "<b>Following redirects</b>, which lets the first response "
          "choose the second destination — so a permitted URL "
          "returns a 302 to the metadata endpoint, and your validation "
          "never saw it.",
          "<b>Alternative URL schemes</b> — <code>file:</code>, "
          "<code>gopher:</code>, <code>dict:</code> and others, which "
          "reach things HTTP does not and which a URL parser may accept "
          "while your validation only considered HTTP.",
          "<b>And IPv6, decimal, octal, and mixed address "
          "encodings</b>, which defeat textual filters looking for "
          "<code>127.0.0.1</code> or <code>169.254</code>. <b>The robust "
          "answer is to resolve the name once, validate the resulting "
          "address, and then connect to that address directly</b> rather "
          "than to the name — which closes the rebinding window and "
          "is Module 05 &sect;3's operate-on-the-handle principle "
          "again."]),

  ("h1", "4 &nbsp; Auditing a trust boundary"),
  ("ul", ["<b>What format is the data in, and does that format encode "
          "types or behaviour rather than only data?</b> (&sect;2's "
          "test.)",
          "<b>Is it authenticated, and is the authentication verified "
          "<i>before</i> parsing rather than after?</b> (&sect;2's "
          "callout.)",
          "<b>What type does it become, and was that type named by my "
          "code or chosen by the input?</b> — which is "
          "Module 04 &sect;4's parse-don't-validate question asked at "
          "a boundary.",
          "<b>What does the parsing itself do</b> — allocate "
          "based on a declared length (Module 03 &sect;1), "
          "decompress (which is where decompression bombs live), "
          "construct objects, resolve external references, or follow "
          "links?",
          "<b>And whose authority is used to act on it</b> — the "
          "requester's, or the process's? (&sect;3's confused deputy.) "
          "<b>The last question generalises this entire module</b>: "
          "<b>deserialisation and SSRF are both the same error — "
          "acting with your own authority on a requester's "
          "instruction</b>, which is why the fix in both cases is to "
          "constrain what the instruction may ask for rather than to "
          "filter the instruction."]),
 ],
 "resources": [
   ("Frohoff & Lawrence &mdash; Marshalling Pickles (free)",
    "https://frohoff.github.io/appseccali-marshalling-pickles/",
    "<b>&sect;1's gadget chains in the original</b> — the talk that "
    "made this class widely understood."),
   ("OWASP &mdash; Deserialization and SSRF cheat sheets (free)",
    "https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html",
    "<b>&sect;2 and &sect;3 as current, per-platform guidance</b>, "
    "maintained and specific."),
   ("Google &mdash; the Java serialization deprecation rationale (free)",
    "https://openjdk.org/jeps/154",
    "<b>&sect;1's severity, as judged by the platform's own "
    "maintainers</b> — a language feature deprecated for security "
    "reasons, which is rare."),
   ("CWE-502, CWE-918 (free)",
    "https://cwe.mitre.org/data/definitions/502.html",
    "<b>&sect;1 and &sect;3 with the shared vocabulary.</b>"),
 ],
 "exercises": [
   "<b>Deserialise a pickle you crafted</b> in your own sandbox and "
   "observe code running.",
   "<b>Explain why post-deserialisation validation cannot help.</b>",
   "<b>Find three classes in your dependency tree</b> whose construction "
   "has a side effect.",
   "<b>Convert one native serialisation use to JSON</b> parsed into a "
   "declared type.",
   "<b>Add a MAC to a serialised value</b> and verify it before "
   "parsing.",
   "<b>Show what happens if you verify after parsing instead.</b>",
   "<b>Write a URL-fetching endpoint</b> and then attack it from your own "
   "client with an internal address.",
   "<b>Implement resolve-then-validate-then-connect</b> and confirm it "
   "blocks rebinding.",
   "<b>Test your filter against decimal and IPv6 encodings</b> of a "
   "loopback address.",
   "<b>Run Part 4's five questions</b> at one real boundary in your own "
   "system.",
 ],
 "selfcheck": [
   "Why is native deserialisation dangerous — give both "
   "mechanisms?",
   "Why does post-deserialisation validation not help?",
   "Name five formats to avoid for untrusted data.",
   "What is a gadget chain, and why is no component buggy?",
   "State the format test and name three safe formats.",
   "What does a MAC change, and when does it not help?",
   "Why is SSRF severe, and what pattern is it?",
   "Give four SSRF defences and five pitfalls.",
   "Why is DNS rebinding the hardest pitfall?",
   "Give the five boundary questions and say which generalises the "
   "module.",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Static Analysis",
 "subtitle": "What it finds, and what it cannot.",
 "question": "Why does the analyser report things that are not bugs?",
 "outcomes": [
     "Explain the soundness and completeness trade.",
     "Explain taint analysis and its precision limits.",
     "Triage findings systematically.",
     "Write a custom query for a project-specific rule.",
     "Deploy analysis so that it is actually used.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The trade",
   "blurb": "Forced by undecidability."},

  {"t": "callout", "title": "Rice's theorem forces every analyser to choose which way to be wrong",
   "kind": "The theoretical foundation",
   "body": ["<b>CSCE 627 established that every non-trivial semantic "
            "property of programs is undecidable</b> — so no "
            "analyser can decide, for all programs, whether a given "
            "defect is present.",
            "<b>So each tool must choose:</b> <b>report everything "
            "possible and accept false positives (sound), or report only "
            "what it is confident about and accept false negatives "
            "(unsound).</b>",
            "<b>And in practice nearly every usable tool chooses "
            "unsound</b> — because <b>a sound analyser on real code "
            "produces more warnings than anyone will read</b>, which "
            "makes it unsound in effect.",
            "<b>So the honest framing is:</b> <b>a static analyser is "
            "a heuristic defect finder with a configurable "
            "precision</b> — not a verifier, and 'the analyser "
            "passed' establishes very little "
            "(Module 13)."]},

  {"t": "table", "kicker": "Trade", "title": "The two failure modes, and what each costs",
   "header": ["", "False positive", "False negative"],
   "widths": [2.6, 4.2, 4.7],
   "rows": [
     ["<b>Means</b>", "<b>Reported, not a defect</b>", "<b>A defect, not reported</b>"],
     ["<b>Cost</b>", "<b>Triage time, and lost credibility</b>", "<b>A shipped vulnerability</b>"],
     ["<b>Failure mode</b>", "<b>The tool gets ignored or disabled</b>", "<b>False confidence</b>"],
     ["<b>Tolerable rate</b>", "<b>Low — maybe one in five findings</b>", "<b>Unknown, which is the problem</b>"],
   ],
   "footnote": "<b>The asymmetry is that you can measure the false "
               "positive rate and cannot measure the false negative "
               "rate</b> — so the pressure is always toward quieter "
               "tools, regardless of whether that is correct.",
   "note": "The measurability asymmetry explains industry behaviour."},

  {"t": "section", "label": "Part 2", "title": "Taint analysis",
   "blurb": "The technique that maps onto this course's defects."},

  {"t": "code", "kicker": "Taint", "title": "The model, and where precision is lost",
   "lang": "text", "code": """
  SOURCES     where untrusted data enters
  SINKS       where it must not arrive unvalidated
  SANITISERS  what makes it safe in between

  The analyser propagates "tainted" from sources
  through assignments and calls, and reports any
  tainted value reaching a sink.

  WHERE PRECISION IS LOST
      aliasing      two names for one object; the
                    analyser must guess
      containers    taint one element, and most tools
                    taint the whole collection
      reflection    the call target is not statically
                    known
      callbacks     and function pointers, same problem
      cross-language and any boundary the tool cannot
                    follow

  WHICH IS WHY findings cluster in dynamic code, and
  why the sanitiser list needs project-specific
  configuration (Part 4).
""",
   "caption": "<b>Aliasing is the fundamental precision "
              "limit</b> — precise alias analysis is itself "
              "undecidable, so every tool approximates.",
   "note": "Connect directly to CSCE 605's dataflow machinery."},

  {"t": "callout", "title": "Which classes static analysis finds well, and which it does not",
   "kind": "Setting expectations correctly",
   "body": ["<b>Found well:</b> <b>integer defects with a short "
            "source-to-sink path (Module 03), injection with a "
            "recognisable sink (Module 04), use of a known-dangerous "
            "function, and missing error checks.</b>",
            "<b>Found poorly:</b> <b>use-after-free across "
            "functions, concurrency defects (Module 05 §4), "
            "and anything requiring the tool to know a project-specific "
            "invariant.</b>",
            "<b>Not found at all:</b> <b>missing authorisation, logic "
            "errors, and design flaws</b> — because <b>the tool does "
            "not know what the program was supposed to "
            "do.</b>",
            "<b>So pair it with fuzzing, which has the opposite "
            "profile</b> (Module 08) — <b>and with review, which "
            "is the only method that addresses the third "
            "category</b> (Module 11)."]},

  {"t": "section", "label": "Part 3", "title": "Triage",
   "blurb": "The work that determines whether this succeeds."},

  {"t": "bullets", "kicker": "Triage", "title": "How to triage without drowning",
   "items": [
     "<b>Start with one rule, not the whole ruleset.</b> <b>Enable "
     "the highest-confidence check, fix every instance, then add the "
     "next</b> — which is the only approach that works on an "
     "existing codebase.",
     "",
     "<b>Baseline the existing findings</b> and <b>fail the build "
     "only on new ones</b>, so the tool constrains new code "
     "immediately rather than after a cleanup project.",
     "",
     "<b>Record a reason for every dismissal</b>, in the code as a "
     "suppression with a comment — <b>'probably fine' is not a "
     "triage</b>.",
     "",
     "<b>And measure the per-rule true positive rate</b>, then "
     "disable the rules that never find anything "
     "(CSCE 701 Module 09 §3).",
     "",
     "<b>Which is the same discipline as alert "
     "tuning</b> — because it is the same problem.",
   ],
   "footnote": "<b>Baseline plus fail-on-new is the deployment pattern "
               "that works</b> — it avoids the cleanup project that "
               "kills most adoptions."},

  {"t": "section", "label": "Part 4", "title": "Custom queries",
   "blurb": "Where the real value is."},

  {"t": "callout", "title": "The highest-value rules are the ones only you can write",
   "kind": "Why custom queries matter more than the defaults",
   "body": ["<b>The built-in rules encode general knowledge, which "
            "every project shares</b> — so they find the general "
            "defects and have usually already been run by somebody "
            "else.",
            "<b>Your project-specific invariants are not in any "
            "ruleset:</b> <b>'every handler must call "
            "<code>check_permission</code> first', 'this function must "
            "never be called with a raw path', 'all queries go through "
            "this wrapper'.</b>",
            "<b>And those are exactly the rules that prevent the "
            "defect you just fixed from recurring</b> — which is "
            "the right trigger for writing one.",
            "<b>So the practice is:</b> <b>after fixing a defect, ask "
            "whether a query could have found it, and write that query "
            "into CI</b> — which converts an incident into a "
            "permanent guarantee."]},

  {"t": "bullets", "kicker": "Deployment", "title": "Making it stick",
   "items": [
     "<b>Run it in CI on every change</b>, and report findings on "
     "the diff rather than on the whole tree.",
     "",
     "<b>Report into the review</b>, where the author is already "
     "thinking about that code — rather than into a dashboard "
     "nobody opens.",
     "",
     "<b>Keep the run fast enough not to be skipped</b>, which "
     "frequently means a quick ruleset per change and the full one "
     "nightly.",
     "",
     "<b>And own the rules.</b> <b>A ruleset nobody is responsible "
     "for tuning degrades into noise</b> within a year.",
     "",
     "<b>Which is CSCE 701 Module 11's compliance budget</b> "
     "— the tool spends developer attention, and the budget is "
     "finite.",
   ],
   "footnote": "<b>Findings in the review rather than in a "
               "dashboard</b> is the single change that most improves "
               "whether static analysis has any effect."},
 ],
 "takeaways": [
   "Rice's theorem forces every analyser to choose between false positives "
   "and false negatives, and usable tools nearly all choose unsound.",
   "You can measure the false positive rate and cannot measure the false "
   "negative rate, so pressure always runs toward quieter tools.",
   "Aliasing is the fundamental precision limit, because precise alias "
   "analysis is itself undecidable.",
   "Static analysis finds short-path integer and injection defects well "
   "and finds missing authorisation not at all.",
   "Baseline the existing findings and fail the build only on new ones — "
   "the deployment pattern that avoids a cleanup project.",
   "The highest-value rules are your project-specific invariants, which "
   "are in no vendor's ruleset.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The trade"),
  ("callout", "Rice's theorem forces every analyser to choose which way to "
              "be wrong",
   ["<b>CSCE 627 established that every non-trivial semantic property "
    "of programs is undecidable</b> — so <b>no analyser can decide, "
    "for all programs, whether a given defect is present.</b> This is "
    "not an engineering limitation that better tools will overcome.",
    "<b>So each tool must choose:</b> <b>report everything that might "
    "be a defect and accept false positives (a sound analysis, which "
    "misses nothing), or report only what it is confident about and "
    "accept false negatives (an unsound analysis, which misses "
    "things).</b>",
    "<b>And in practice nearly every usable tool chooses "
    "unsound</b> — because <b>a sound analyser run on real code "
    "produces far more warnings than anybody will read</b>, <b>which "
    "makes it unsound in effect</b> once the team starts ignoring the "
    "output. The theoretically stronger choice is operationally "
    "weaker.",
    "<b>So the honest framing is:</b> <b>a static analyser is a "
    "heuristic defect finder with a configurable precision</b> — "
    "<b>not a verifier</b> — and therefore <b>'the analyser passed' "
    "establishes very little</b> about the code, which is "
    "Module 13's subject and the reason this framing matters."]),
  ("table", ["", "False positive", "False negative"],
   [["<b>What it means</b>",
     "<b>Reported, and not actually a defect.</b>",
     "<b>A real defect, and not reported.</b>"],
    ["<b>What it costs</b>",
     "<b>Triage time, and the tool's credibility.</b>",
     "<b>A shipped vulnerability.</b>"],
    ["<b>The failure mode</b>",
     "<b>The tool gets ignored, then disabled</b> — which forfeits "
     "the true positives too.",
     "<b>False confidence</b>, which is worse than no tool because it "
     "displaces other methods."],
    ["<b>Tolerable rate</b>",
     "<b>Low</b> — roughly one true positive in five findings is "
     "about the limit of what a team will sustain.",
     "<b>Unknown, which is precisely the problem.</b>"]],
   [0.20, 0.38, 0.42]),
  ("p", "<b>The asymmetry is that you can measure the false positive rate "
        "and cannot measure the false negative rate.</b> <b>So the "
        "commercial and organisational pressure is always toward quieter "
        "tools</b>, regardless of whether quieter is correct — a "
        "vendor is judged on noise and never on what was missed. "
        "<b>Which is CSCE 701 Module 12's measurement problem, in "
        "the tooling market</b>, and it is worth knowing when reading a "
        "product comparison."),

  ("h1", "2 &nbsp; Taint analysis"),
  ("code", """SOURCES     where untrusted data enters
SINKS       where it must not arrive unvalidated
SANITISERS  what makes it safe in between

The analyser propagates a "tainted" marking from
sources through assignments and calls, and reports any
tainted value that reaches a sink.

WHERE PRECISION IS LOST
    aliasing      two names for one object; the
                  analyser must guess
    containers    taint one element, and most tools
                  taint the whole collection
    reflection    the call target is not statically
                  known
    callbacks     and function pointers, same problem
    cross-language and any boundary the tool cannot
                  follow at all

WHICH IS WHY findings cluster in dynamic code, and why
the sanitiser list needs project-specific
configuration (section 4)."""),
  ("p", "<b>Aliasing is the fundamental precision limit</b> — "
        "<b>precise alias analysis is itself undecidable</b>, so every "
        "tool approximates, and the approximation is where both false "
        "positives and false negatives come from. <b>This is "
        "CSCE 605 Module 11's dataflow machinery applied to a "
        "different question</b>: the same lattices, the same fixpoint "
        "computation, the same soundness-precision trade, pointed at "
        "defects instead of at optimisations — which is worth "
        "noticing, because it means the theory transfers directly."),
  ("callout", "Which classes static analysis finds well, and which it does "
              "not",
   ["<b>Found well:</b> <b>integer defects with a short source-to-sink "
    "path (Module 03 &sect;3's five sinks), injection with a "
    "recognisable sink (Module 04), use of a known-dangerous library "
    "function, missing error checks, and simple resource leaks.</b>",
    "<b>Found poorly:</b> <b>use-after-free across function "
    "boundaries (Module 02 &sect;1's locality problem), concurrency "
    "defects (Module 05 &sect;4), and anything requiring the tool to "
    "know a project-specific invariant</b> — which is &sect;4's "
    "opportunity.",
    "<b>Not found at all:</b> <b>missing authorisation checks, logic "
    "errors, and design flaws</b> — because <b>the tool does not "
    "know what the program was supposed to do</b>, and no amount of "
    "analysis sophistication supplies that.",
    "<b>So pair it with fuzzing, which has close to the opposite "
    "profile</b> (Module 08) — <b>and with review, which is the "
    "only method that addresses the third category at all</b> "
    "(Module 11). <b>The three techniques are complementary rather "
    "than redundant</b>, which is why Project 2 requires two of them and "
    "Module 13 asks what all three together still miss."]),

  ("break",),
  ("h1", "3 &nbsp; Triage"),
  ("ul", ["<b>Start with one rule, not the whole ruleset.</b> "
          "<b>Enable the single highest-confidence check, fix every "
          "instance of it, then add the next</b> — which is <b>the "
          "only approach that works on an existing codebase</b>, because "
          "enabling everything produces thousands of findings and an "
          "immediate decision to ignore them.",
          "<b>Baseline the existing findings</b> and <b>fail the build "
          "only on new ones</b>, so that <b>the tool constrains new code "
          "from today</b> rather than after a cleanup project that will "
          "never be scheduled.",
          "<b>Record a reason for every dismissal</b>, in the code as "
          "a suppression with a comment explaining why — <b>'probably "
          "a false positive' is not a triage</b>, and Project 2 grades it "
          "as an untriaged finding.",
          "<b>And measure the per-rule true positive rate</b>, then "
          "<b>disable the rules that never find anything real</b> — "
          "which is CSCE 701 Module 09 &sect;3's rule retirement, "
          "applied to a different tool.",
          "<b>Which is the same discipline as security alert "
          "tuning</b> — <b>because it is the same problem</b>: a "
          "detector with a poor base rate, a finite human review budget, "
          "and a failure mode of being ignored. <b>Baseline plus "
          "fail-on-new is the deployment pattern that works</b>, and it "
          "avoids the cleanup project that kills most adoptions."]),

  ("h1", "4 &nbsp; Custom queries, and deployment"),
  ("callout", "The highest-value rules are the ones only you can write",
   ["<b>The built-in rules encode general knowledge, which every "
    "project shares</b> — so they find the general defects, and "
    "<b>somebody has usually already run a similar tool over your "
    "dependencies</b>, which means the marginal yield on a mature "
    "codebase is modest.",
    "<b>Your project-specific invariants are in no vendor's "
    "ruleset:</b> <b>'every request handler must call "
    "<code>check_permission</code> before touching the database', 'this "
    "function must never be called with a raw path', 'all queries go "
    "through this wrapper', 'no new call sites for this deprecated "
    "API'.</b>",
    "<b>And those are exactly the rules that prevent the defect you "
    "just fixed from recurring</b> — <b>which makes a completed "
    "fix the right trigger for writing one</b>, while the mechanism is "
    "still fresh and the cost of writing the query is lowest.",
    "<b>So the practice is:</b> <b>after fixing any defect, ask "
    "whether a query could have found it, and if so write that query into "
    "CI</b> — <b>which converts an incident into a permanent "
    "guarantee</b> and is the single highest-return use of a static "
    "analysis platform. <b>CodeQL and Semgrep both exist primarily for "
    "this</b>, and both are usable within a day."]),
  ("ul", ["<b>Run it in CI on every change</b>, and <b>report findings "
          "on the diff rather than on the whole tree</b> — which "
          "makes the output proportionate to what the author just "
          "did.",
          "<b>Report into the code review</b>, where the author is "
          "already thinking about that specific code — <b>rather "
          "than into a dashboard nobody opens</b>, which is where most "
          "static analysis output goes to be ignored.",
          "<b>Keep the run fast enough not to be skipped</b>, which "
          "frequently means a quick ruleset on every change and the full "
          "analysis nightly — a slow check gets bypassed under "
          "deadline pressure, every time.",
          "<b>And own the rules.</b> <b>A ruleset that nobody is "
          "responsible for tuning degrades into noise within about a "
          "year</b>, as the codebase changes around it and the "
          "suppressions accumulate unexamined.",
          "<b>Which is CSCE 701 Module 11 &sect;1's compliance "
          "budget</b> — <b>the tool spends developer attention, and "
          "that budget is finite and shared with every other process you "
          "impose.</b> <b>Findings in the review rather than in a "
          "dashboard is the single change that most improves whether "
          "static analysis has any effect at all.</b>"]),
 ],
 "resources": [
   ("M&oslash;ller & Schwartzbach &mdash; Static Program Analysis (free "
    "PDF)",
    "https://cs.au.dk/~amoeller/spa/",
    "<b>&sect;1 and &sect;2's theory</b> — free, rigorous, and "
    "explicit about the precision limits."),
   ("CodeQL documentation and the query examples (free)",
    "https://codeql.github.com/docs/",
    "<b>&sect;4's practice</b> — and the query language is worth "
    "learning for the project-specific rules alone."),
   ("Semgrep registry and rule-writing guide (free)",
    "https://semgrep.dev/docs/",
    "<b>&sect;4 with a much shallower learning curve</b> — the right "
    "starting point for a first custom rule."),
   ("Bessey et al. &mdash; A Few Billion Lines of Code Later (free)",
    "https://dl.acm.org/doi/10.1145/1646353.1646374",
    "<b>&sect;3's deployment reality</b>, from the people who "
    "commercialised it — honest about why adoption fails, and the "
    "best thing written on this."),
 ],
 "exercises": [
   "<b>State Rice's theorem</b> and explain what it forces on an "
   "analyser.",
   "<b>Run a sound and an unsound analyser</b> on the same code and "
   "compare the output volume.",
   "<b>Write a taint-flow defect</b> and confirm the analyser finds "
   "it.",
   "<b>Add an alias in between</b> and see whether it still does.",
   "<b>Put the tainted value in a container</b> and check again.",
   "<b>Classify ten findings</b> as true positive, false positive, or "
   "undetermined, with a reason for each.",
   "<b>Baseline a codebase</b> and configure fail-on-new.",
   "<b>Write one custom query</b> encoding a project-specific "
   "invariant.",
   "<b>Fix a defect, then write the query</b> that would have caught "
   "it.",
   "<b>Move your findings into code review</b> and report whether "
   "response changed.",
 ],
 "selfcheck": [
   "What does Rice's theorem force, and which choice do real tools "
   "make?",
   "Why is a sound analyser unsound in effect?",
   "Give the two failure modes and the asymmetry between them.",
   "Explain the source-sink-sanitiser model.",
   "Name five places taint analysis loses precision.",
   "Why is aliasing the fundamental limit?",
   "Which classes are found well, poorly, and not at all?",
   "Give four triage practices and the deployment pattern that works.",
   "Why are custom queries higher value than the defaults?",
   "What is the right trigger for writing one?",
 ],
},

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Fuzzing",
 "subtitle": "The technique that actually finds memory defects.",
 "question": "How do you generate inputs that reach the interesting code?",
 "outcomes": [
     "Explain coverage-guided fuzzing and why it works.",
     "Write an effective harness.",
     "Measure a campaign properly.",
     "Explain structure-aware fuzzing and when it is needed.",
     "Explain what fuzzing cannot find.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why coverage guidance works",
   "blurb": "The idea that made fuzzing effective."},

  {"t": "callout", "title": "Coverage feedback turns random mutation into a search",
   "kind": "The mechanism",
   "body": ["<b>Random inputs almost never reach deep code</b> "
            "— a parser rejects them at the first byte, so "
            "undirected fuzzing explores the error path and nothing "
            "else.",
            "<b>Coverage guidance fixes this:</b> <b>instrument the "
            "program, keep any input that reached a new edge, and mutate "
            "the kept inputs further</b> — so progress "
            "accumulates.",
            "<b>Which converts a random search into a hill-climb on "
            "coverage</b> — and <b>a magic number or a checksum is "
            "discovered byte by byte, because each correct byte opens a "
            "new edge.</b>",
            "<b>And it needs no specification.</b> <b>The oracle is "
            "simply 'did it crash', which is why this works on code "
            "nobody documented</b> — and why sanitisers multiply its "
            "power (Module 09)."]},

  {"t": "bullets", "kicker": "Oracles", "title": "What counts as a failure, which determines what you find",
   "items": [
     "<b>A crash or a hang</b> — the default, and the "
     "weakest, because many defects do not crash.",
     "",
     "<b>A sanitiser report</b> — <b>which is what makes "
     "fuzzing effective</b>: AddressSanitizer turns a silent "
     "out-of-bounds read into a loud failure "
     "(Module 09 §1).",
     "",
     "<b>An assertion</b> — your own invariants, checked on "
     "every input, which is the cheapest way to broaden the "
     "oracle.",
     "",
     "<b>A differential comparison</b> — two implementations "
     "disagreeing, which finds correctness defects with no "
     "crash.",
     "",
     "<b>And a round-trip property</b> — parse then serialise "
     "then parse, which must be stable.",
   ],
   "footnote": "<b>Fuzzing without sanitisers finds a fraction of what "
               "it should</b> — the pairing is not optional, and it "
               "is the most common omission."},

  {"t": "section", "label": "Part 2", "title": "The harness",
   "blurb": "Where campaigns succeed or fail."},

  {"t": "code", "kicker": "Harness", "title": "What a good harness looks like",
   "lang": "text", "code": """
  int LLVMFuzzerTestOneInput(const uint8_t *d, size_t n) {
      Parser p;
      p.parse(d, n);     // the real entry point
      return 0;
  }

  RULES
      target the REAL parsing entry point, not a
          validation wrapper
      be deterministic -- no time, no randomness, no
          network; seed any PRNG from the input
      be fast -- thousands of executions per second;
          a slow harness is a small campaign
      free everything, so leak detection is meaningful
      and do not catch the exceptions you want to find

  SEED CORPUS
      start from real, valid inputs -- a handful of
      genuine files beats a million random bytes,
      because coverage guidance needs somewhere to
      climb from
""",
   "caption": "<b>The seed corpus is the most underrated input to a "
              "campaign</b> — real files give the fuzzer the grammar "
              "for free.",
   "note": "Harness quality dominates campaign outcome; say so "
           "explicitly."},

  {"t": "section", "label": "Part 3", "title": "Measuring",
   "blurb": "Because 'we fuzzed it' is not a result."},

  {"t": "callout", "title": "Report coverage, not duration",
   "kind": "The measurement that means something",
   "body": ["<b>'We fuzzed for 48 hours' says nothing</b> — a "
            "harness that rejects every input at byte zero can run "
            "forever and test one function.",
            "<b>So report the coverage achieved:</b> <b>which "
            "functions and edges were reached, as a fraction of the "
            "target component</b> — which is both measurable and "
            "actionable.",
            "<b>And read the coverage to find the blocked "
            "paths.</b> <b>An unreached branch usually means a checksum, "
            "a magic value, a length field, or a decompression step the "
            "fuzzer cannot synthesise</b> — each of which has a "
            "specific fix.",
            "<b>Which makes coverage the campaign's steering "
            "signal</b> rather than a score — <b>a plateau means "
            "change the harness or the corpus, not run it "
            "longer.</b>"]},

  {"t": "bullets", "kicker": "Improving", "title": "What to do when coverage plateaus",
   "items": [
     "<b>Add seeds covering the formats and features you have "
     "not</b> — the cheapest intervention, and usually the most "
     "effective.",
     "",
     "<b>Disable checksum verification in the fuzz build</b>, so "
     "the fuzzer is not required to compute one — and keep it "
     "enabled in production.",
     "",
     "<b>Split one harness into several</b>, each targeting a "
     "different entry point, so the search is not diluted.",
     "",
     "<b>Use a dictionary of the format's tokens</b>, so the "
     "mutator inserts meaningful strings rather than discovering them "
     "byte by byte.",
     "",
     "<b>And go structure-aware</b> if the format is deeply "
     "structured (Part 4).",
   ],
   "footnote": "<b>Disabling checksums in the fuzz build is the "
               "highest-yield single change</b> for binary formats "
               "— and it is safe, because it is a build "
               "configuration."},

  {"t": "section", "label": "Part 4", "title": "Limits",
   "blurb": "What fuzzing structurally cannot find."},

  {"t": "callout", "title": "Fuzzing finds crashes, so it cannot find anything that does not crash",
   "kind": "The honest boundary",
   "body": ["<b>Not found:</b> <b>missing authorisation, business "
            "logic errors, weak cryptography, information disclosure "
            "without a crash, and anything where the wrong answer is "
            "still a well-formed answer.</b>",
            "<b>Found poorly:</b> <b>defects requiring a specific "
            "sequence of operations</b> rather than a single input, and "
            "<b>concurrency defects</b>, because the interleaving is not "
            "part of the input (Module 05 §4).",
            "<b>And deep state is hard</b> — a defect reachable "
            "only after authentication, a session, and three prior "
            "requests is not a single-input target.",
            "<b>So extend the oracle where you can:</b> "
            "<b>assertions, differential testing, and stateful "
            "harnesses that interpret the input as a sequence of "
            "operations</b> — which broadens it considerably."]},

  {"t": "bullets", "kicker": "Practice", "title": "Running it continuously",
   "items": [
     "<b>Fuzz in CI on every change</b>, briefly — a few "
     "minutes per harness catches regressions in code just "
     "written.",
     "",
     "<b>And run long campaigns continuously</b>, separately, "
     "because <b>the interesting findings arrive after hours rather "
     "than minutes.</b>",
     "",
     "<b>Keep the corpus</b> — it is the accumulated result "
     "of every previous campaign, and discarding it restarts the "
     "search.",
     "",
     "<b>Add every crash as a regression test</b>, minimised, so "
     "it cannot return.",
     "",
     "<b>And for open-source projects, OSS-Fuzz runs this "
     "infrastructure free</b>, which removes the main obstacle to doing "
     "it properly.",
   ],
   "footnote": "<b>Keeping the corpus is the practice most often "
               "skipped</b> — and it is what makes the next campaign "
               "start where the last one stopped."},
 ],
 "takeaways": [
   "Coverage guidance turns random mutation into a hill-climb, so a magic "
   "number is discovered byte by byte as each correct byte opens an edge.",
   "Fuzzing without sanitisers finds a fraction of what it should — "
   "the pairing is not optional.",
   "Target the real parsing entry point, be deterministic, and be fast; a "
   "slow harness is a small campaign.",
   "A handful of genuine input files beats a million random bytes, because "
   "coverage guidance needs somewhere to climb from.",
   "Report coverage rather than duration, and treat a plateau as a signal "
   "to change the harness rather than to run longer.",
   "Fuzzing finds crashes, so it cannot find missing authorisation, logic "
   "errors, or any wrong answer that is still well-formed.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why coverage guidance works"),
  ("callout", "Coverage feedback turns random mutation into a search",
   ["<b>Random inputs almost never reach deep code</b> — a parser "
    "rejects them at the first byte, so undirected random fuzzing "
    "explores the error-handling path exhaustively and the rest of the "
    "program not at all. <b>This is why fuzzing was considered a "
    "low-yield technique for years.</b>",
    "<b>Coverage guidance fixes it:</b> <b>instrument the program to "
    "report which edges executed, keep any input that reached a new edge, "
    "and mutate the kept inputs further</b> — so <b>progress "
    "accumulates rather than being rediscovered each time.</b>",
    "<b>Which converts a random search into a hill-climb on "
    "coverage</b> — and the consequence is striking: <b>a magic "
    "number or a format signature is discovered byte by byte, because "
    "each correct byte opens a new edge and the input is therefore "
    "kept.</b> The fuzzer reconstructs the format without being told "
    "it.",
    "<b>And it requires no specification whatsoever.</b> <b>The oracle "
    "is simply 'did it crash', which is why this works on code nobody "
    "documented and nobody understands</b> — and why <b>sanitisers "
    "multiply its power</b> (Module 09), since they convert silent "
    "corruption into a crash."]),
  ("ul", ["<b>A crash or a hang</b> — the default oracle, and the "
          "weakest one, <b>because a great many memory defects do not "
          "crash</b>: an out-of-bounds read returns whatever was there "
          "and execution continues.",
          "<b>A sanitiser report</b> — <b>which is what actually "
          "makes fuzzing effective</b>. <b>AddressSanitizer turns a "
          "silent one-byte out-of-bounds read into a loud, precisely "
          "located failure</b> (Module 09 &sect;1).",
          "<b>An assertion</b> — your own invariants, checked on "
          "every single input, <b>which is the cheapest available way to "
          "broaden the oracle</b> and finds logic defects a crash oracle "
          "never would.",
          "<b>A differential comparison</b> — two implementations "
          "of the same format or protocol disagreeing on an input, "
          "<b>which finds correctness defects with no crash at all</b> "
          "and is how a great many parser and cryptographic "
          "implementation bugs were found.",
          "<b>And a round-trip property</b> — parse, then "
          "serialise, then parse again, which must be stable. <b>Fuzzing "
          "without sanitisers finds a fraction of what it should</b>, and "
          "<b>the pairing is not optional</b> — it is the most common "
          "omission in campaigns that report disappointing results."]),

  ("h1", "2 &nbsp; The harness"),
  ("code", """int LLVMFuzzerTestOneInput(const uint8_t *d, size_t n) {
    Parser p;
    p.parse(d, n);     // the real entry point
    return 0;
}

RULES
    target the REAL parsing entry point, not a
        validation wrapper or a convenience API
    be deterministic -- no time, no randomness, no
        network, no filesystem; seed any PRNG from
        the input itself
    be fast -- thousands of executions per second; a
        slow harness is a small campaign, and the
        relationship is linear
    free everything, so that leak detection is
        meaningful
    and do NOT catch the exceptions you want to find

SEED CORPUS
    start from real, valid inputs -- a handful of
    genuine files beats a million random bytes,
    because coverage guidance needs somewhere to
    climb from"""),
  ("p", "<b>Harness quality dominates campaign outcome</b>, and it is "
        "worth saying explicitly because the instinct is to attribute a "
        "poor campaign to insufficient time. <b>The seed corpus is the "
        "most underrated input</b> — <b>real files give the fuzzer "
        "the format's grammar for free</b>, and a corpus of twenty genuine "
        "documents routinely outperforms a week of fuzzing from an empty "
        "corpus. <b>And targeting a validation wrapper rather than the "
        "real parser is the commonest harness defect</b>: the fuzzer "
        "spends its entire budget on the function that rejects malformed "
        "input, which is the one function you were not worried about."),

  ("break",),
  ("h1", "3 &nbsp; Measuring"),
  ("callout", "Report coverage, not duration",
   ["<b>'We fuzzed for 48 hours' says essentially nothing</b> — "
    "<b>a harness that rejects every input at byte zero can run forever "
    "and will have tested exactly one function.</b> Duration is an "
    "input to the process, not a result of it.",
    "<b>So report the coverage achieved:</b> <b>which functions and "
    "which edges were reached, as a fraction of the target "
    "component</b> — which is both measurable and, unlike duration, "
    "actionable.",
    "<b>And read the coverage specifically to find the blocked "
    "paths.</b> <b>An unreached branch usually means a checksum, a "
    "magic value, a length field, a decompression step, or a "
    "cryptographic check that the fuzzer cannot synthesise</b> — and "
    "<b>each of those has a specific fix</b> (&sect;3's list).",
    "<b>Which makes coverage the campaign's steering signal rather "
    "than a score</b> — <b>a plateau means change the harness or the "
    "corpus, not run it longer</b>, and recognising that distinction is "
    "what separates a productive campaign from an expensive one. "
    "<b>This is also what Project 2 grades</b>, and why it asks for the "
    "coverage figure."]),
  ("ul", ["<b>Add seeds covering the formats, versions, and features "
          "you have not reached</b> — <b>the cheapest intervention "
          "available, and usually the most effective</b> one.",
          "<b>Disable checksum verification in the fuzz build</b>, so "
          "that the fuzzer is not required to compute a valid checksum "
          "before reaching any parsing logic — <b>and keep it "
          "enabled in production</b>, since this is a build "
          "configuration rather than a code change.",
          "<b>Split one harness into several</b>, each targeting a "
          "different entry point or a different format, so that the "
          "search is not diluted across unrelated code.",
          "<b>Use a dictionary of the format's tokens and keywords</b>, "
          "so the mutator inserts meaningful strings directly rather than "
          "discovering each one byte by byte — which is nearly free "
          "and helps substantially on text formats.",
          "<b>And go structure-aware</b> if the format is deeply "
          "structured (&sect;4). <b>Disabling checksums in the fuzz "
          "build is the highest-yield single change for binary "
          "formats</b>, and it is entirely safe because it cannot affect "
          "the shipped artefact."]),

  ("h1", "4 &nbsp; Limits, and continuous operation"),
  ("callout", "Fuzzing finds crashes, so it cannot find anything that does "
              "not crash",
   ["<b>Not found at all:</b> <b>missing authorisation checks, "
    "business logic errors, weak cryptography, information disclosure "
    "without a crash, and anything at all where the wrong answer is "
    "still a well-formed answer</b> — which includes most of "
    "CSCE 701's subject matter.",
    "<b>Found poorly:</b> <b>defects requiring a specific sequence of "
    "operations</b> rather than a single input, <b>and concurrency "
    "defects</b>, because <b>the interleaving is not part of the "
    "input</b> and therefore not part of what the fuzzer varies "
    "(Module 05 &sect;4).",
    "<b>And deep state is genuinely hard</b> — a defect reachable "
    "only after authentication, a session setup, and three prior requests "
    "in a particular order is not a single-input target, and no amount of "
    "mutation on one buffer reaches it.",
    "<b>So extend the oracle where you can:</b> <b>assertions over "
    "your own invariants, differential testing against a second "
    "implementation, and stateful harnesses that interpret the input "
    "buffer as a <i>sequence of operations</i> rather than as one "
    "document</b> — which broadens the technique considerably and is "
    "how protocol implementations are fuzzed effectively."]),
  ("ul", ["<b>Fuzz in CI on every change, briefly</b> — a few "
          "minutes per harness, which catches regressions in code that "
          "was just written and is cheap enough nobody objects.",
          "<b>And run long campaigns continuously and separately</b>, "
          "because <b>the interesting findings arrive after hours or days "
          "rather than minutes</b> — the two uses have different "
          "purposes and different infrastructure.",
          "<b>Keep the corpus</b> — <b>it is the accumulated "
          "result of every previous campaign, and discarding it restarts "
          "the search from nothing</b>. This is <b>the practice most "
          "often skipped</b>, and keeping it is what makes the next "
          "campaign start where the last one stopped.",
          "<b>Add every crash as a minimised regression test</b>, so "
          "that the specific defect cannot return silently — and "
          "minimisation is automated by every modern fuzzer.",
          "<b>And for open-source projects, OSS-Fuzz runs this entire "
          "infrastructure free</b> — continuous fuzzing, corpus "
          "management, crash triage, and regression tracking — "
          "<b>which removes the main practical obstacle to doing this "
          "properly</b> and has found tens of thousands of real defects "
          "by exactly the method described here."]),
 ],
 "resources": [
   ("The Fuzzing Book (free, interactive)",
    "https://www.fuzzingbook.org/",
    "<b>The whole module, executable</b> — build a coverage-guided "
    "fuzzer yourself, which is the fastest route to understanding "
    "&sect;1."),
   ("libFuzzer and AFL++ documentation (free)",
    "https://llvm.org/docs/LibFuzzer.html",
    "<b>&sect;2 and &sect;3 in practice</b> — the harness rules and "
    "the coverage tooling, from the implementations."),
   ("OSS-Fuzz, and its ideal integration guide (free)",
    "https://google.github.io/oss-fuzz/",
    "<b>&sect;4's continuous operation</b>, plus the best available "
    "guidance on harness design at scale."),
   ("Klees et al. &mdash; Evaluating Fuzz Testing (free)",
    "https://arxiv.org/abs/1808.09700",
    "<b>&sect;3's argument, rigorously</b> — why duration and crash "
    "counts are poor measures, and what to report instead."),
 ],
 "exercises": [
   "<b>Write a coverage-guided fuzzer</b> for a toy parser, following "
   "The Fuzzing Book.",
   "<b>Show it discovering a four-byte magic number</b>, and explain "
   "why it can.",
   "<b>Fuzz a parser without sanitisers, then with them</b>, and compare "
   "the findings.",
   "<b>Write a harness that targets a validation wrapper</b>, then "
   "retarget it at the real parser and compare coverage.",
   "<b>Fuzz from an empty corpus and from twenty real files</b>, and "
   "compare.",
   "<b>Report coverage rather than duration</b> for one campaign.",
   "<b>Find one unreached branch</b> and determine what blocks it.",
   "<b>Disable a checksum in the fuzz build</b> and measure the coverage "
   "change.",
   "<b>Write a stateful harness</b> interpreting the input as an "
   "operation sequence.",
   "<b>List three defect classes your campaign could not have "
   "found.</b>",
 ],
 "selfcheck": [
   "Why do random inputs fail to reach deep code?",
   "How does coverage guidance change that, and how is a magic number "
   "found?",
   "Name five oracles and say which makes fuzzing effective.",
   "Give five harness rules and the commonest harness defect.",
   "Why does the seed corpus matter so much?",
   "Why is duration a poor measure, and what should you report?",
   "How do you read coverage to improve a campaign?",
   "Give five responses to a coverage plateau.",
   "What can fuzzing not find, and what does it find poorly?",
   "How do you extend the oracle, and why keep the corpus?",
 ],
},

]
