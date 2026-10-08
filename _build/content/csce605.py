# -*- coding: utf-8 -*-
"""CSCE 605 Compiler Design — original course content."""

COURSE = {
    "code": "CSCE 605",
    "title": "Compiler Design",
    "tagline": "Front end, intermediate representation, optimisation, and "
               "code generation — with the shader pipeline as the "
               "worked example",
    "term": "Semester 5 (with CSCE 620 and CSCE 678)",
    "prereqs": "CSCE 629 Analysis of Algorithms; CSCE 614 Computer "
               "Architecture; fluency in C, C++, or Rust",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A working compiler for a small language — lexer "
                   "through register allocation — with an SSA "
                   "intermediate representation, a measured optimisation "
                   "pipeline, and a differential test suite that proves it "
                   "does not miscompile",
    "description": [
        "A compiler is the program every other program depends on, and it "
        "is the one whose failures are hardest to see. <b>A miscompile is "
        "invisible from the source.</b> The code is right, the test is "
        "right, the output is wrong, and nothing in the program you wrote "
        "explains it — which is why compiler bugs cost so much more "
        "than their frequency suggests, and why this course treats "
        "correctness as the primary concern rather than a later one.",
        "The organising decision in any compiler is <b>the intermediate "
        "representation</b>. Everything upstream exists to produce it and "
        "everything downstream consumes it, so the IR determines which "
        "analyses are cheap, which optimisations are expressible, and which "
        "are effectively impossible. <b>Module 07 argues that static single "
        "assignment is the single most consequential idea in modern "
        "compilation</b> — not because it is clever, but because it "
        "makes the questions optimisation needs to ask into questions with "
        "O(1) answers.",
        "The second theme is that <b>optimisation is a search over a space "
        "with no reliable gradient</b>. Passes interact, the order matters, "
        "a pass that usually helps sometimes hurts, and the only honest way "
        "to settle any of it is measurement — which is CSCE 735's "
        "discipline applied to the compiler rather than to the program.",
        "The worked example throughout is <b>the shader pipeline</b>, "
        "because it is the compiler every graphics programmer already "
        "depends on and almost none can describe. HLSL and GLSL compile to "
        "SPIR-V, SPIR-V is consumed by a driver compiler, and the driver "
        "generates machine code for hardware whose instruction set is "
        "undocumented. <b>Module 13 explains shader compilation stutter "
        "properly</b>, which is worth the module on its own.",
    ],
    "outcomes": [
        "Explain the phases of a compiler and what each establishes.",
        "Build a lexer from regular expressions via NFA and DFA "
        "construction.",
        "Write recursive-descent and operator-precedence parsers.",
        "Explain LR parsing and diagnose shift-reduce and reduce-reduce "
        "conflicts.",
        "Implement scope resolution and type checking.",
        "Construct an SSA intermediate representation with dominance "
        "frontiers.",
        "Formulate and solve dataflow problems as fixpoints over a "
        "lattice.",
        "Implement the standard optimisations and measure which ones "
        "pay.",
        "Perform instruction selection, scheduling, and register "
        "allocation.",
        "Explain shader compilation, pipeline state objects, and why "
        "games stutter.",
    ],
    "materials": [
        ("Stanford CS143 — Compilers (free, self-paced)",
         "https://web.stanford.edu/class/cs143/",
         "<b>The primary source for Modules 02 through 06.</b> Complete "
         "lectures, assignments, and a full compiler project. Free and "
         "well paced."),
        ("Bob Nystrom — Crafting Interpreters (free book)",
         "https://craftinginterpreters.com/",
         "<b>The best free introduction in existence.</b> Two complete "
         "implementations, every line explained. Read the whole thing "
         "early — it makes the rest of the course concrete."),
        ("Cooper & Torczon — Engineering a Compiler",
         "https://www.elsevier.com/books/engineering-a-compiler/cooper/978-0-12-815412-0",
         "The reference for Modules 07 through 11. Stronger than the "
         "Dragon Book on SSA, dataflow, and register allocation. Library "
         "copy."),
        ("LLVM — the Kaleidoscope tutorial and the Language Reference "
         "(free)",
         "https://llvm.org/docs/tutorial/",
         "A working front end in a weekend, and then the IR specification "
         "that Module 07 is about. The Language Reference is worth reading "
         "as a document in its own right."),
        ("Khronos — the SPIR-V specification and SPIRV-Cross / "
         "DXC (free)",
         "https://registry.khronos.org/SPIR-V/",
         "<b>The Module 13 material.</b> SPIR-V is an SSA IR you can read, "
         "which makes it an unusually good teaching artifact as well as a "
         "shipping one."),
        ("Muchnick — Advanced Compiler Design and Implementation",
         "https://www.elsevier.com/books/advanced-compiler-design-implementation/muchnick/978-1-55860-320-2",
         "The exhaustive reference for Modules 08 and 09. Dense; use it to "
         "look things up rather than to read through."),
    ],
    "tooling": [
        "<b>A systems language</b> — C++17, Rust, or OCaml. You will "
        "write a great deal of tree and graph manipulation, and the "
        "language should make tagged unions pleasant.",
        "<b>No parser generator for Module 03.</b> Write the "
        "recursive-descent parser by hand; <b>use a generator in "
        "Module 04</b>, after you understand what it is doing.",
        "<b>LLVM installed</b>, for Modules 07 and 09. "
        "<code>opt -print-after-all</code> is the single most instructive "
        "command in this course.",
        "<b>A SPIR-V toolchain</b> — <code>glslangValidator</code> or "
        "DXC, plus <code>spirv-dis</code> and <code>spirv-opt</code>. All "
        "free, and Module 13 needs them.",
        "<b>A differential test harness and a random program generator.</b> "
        "<b>Module 13 argues this is the only testing that finds "
        "miscompiles</b>, and Csmith is the model.",
        "<b>A benchmark suite you can run in one command.</b> Every claim "
        "in Modules 09 through 11 is a measurement, and retuning must be "
        "cheap.",
    ],
    "projects": [
        {"title": "Front end to IR", "after": 7,
         "brief": "A complete front end for a small imperative language, "
                  "ending in a well-formed SSA intermediate "
                  "representation that you can print and inspect.",
         "reqs": [
             "A lexer, hand-written or generated, with <b>accurate source "
             "positions carried through every later phase</b>.",
             "A parser producing an AST, with <b>error recovery that "
             "reports more than one error per run</b>.",
             "Scope resolution and a symbol table handling shadowing, "
             "nested functions, and forward references.",
             "A type checker with <b>diagnostics that name the source "
             "location and explain the mismatch</b>.",
             "<b>SSA construction with correctly placed &phi; functions</b>, "
             "computed from dominance frontiers rather than guessed.",
             "A readable textual IR dump, and an IR verifier.",
         ],
         "done": [
             "<b>The IR verifier passes on every test program</b>, and the "
             "verifier checks dominance, not merely well-formedness.",
             "<b>A diagnostics gallery:</b> twenty ill-formed programs with "
             "the message each produces. <b>Quality of diagnostics is "
             "graded</b> — it is most of what users experience.",
             "An interpreter over your IR, so correctness is testable "
             "before any code generation exists.",
             "<b>A statement of what your language cannot express</b> and "
             "what that bought you.",
         ]},
        {"title": "Optimisation and code generation", "after": 12,
         "brief": "Take the IR to machine code, with every optimisation "
                  "measured individually — including the ones that "
                  "lose.",
         "reqs": [
             "<b>At least four optimisation passes</b> implemented over "
             "SSA: constant propagation, dead code elimination, common "
             "subexpression elimination or GVN, and one loop "
             "transformation.",
             "Instruction selection and a working backend for one real "
             "target, or emission of LLVM IR with a justification.",
             "<b>Register allocation by graph colouring or linear scan</b>, "
             "with spilling that works.",
             "<b>A differential test suite against an interpreter or "
             "another compiler</b>, run on generated programs.",
             "A benchmark suite with each pass's effect measured "
             "separately.",
         ],
         "done": [
             "<b>A table of every pass with its measured effect on each "
             "benchmark, including the negative results.</b> A pass that "
             "never helps is a finding, not a failure.",
             "<b>Evidence about pass ordering:</b> at least two orderings "
             "measured, with the difference explained.",
             "<b>A miscompile found and fixed</b>, with the reduced test "
             "case. If differential testing found none, say how many "
             "programs were tested — that is the actual claim.",
             "An honest comparison against <code>gcc -O0</code> and "
             "<code>-O2</code>, and a statement of where the gap is.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "What a Compiler Is",
 "subtitle": "A series of representations, each closer to the machine.",
 "question": "What does a compiler actually do, and in what order?",
 "outcomes": [
     "Name the phases and say what each one establishes.",
     "Explain why the intermediate representation is the central design "
     "decision.",
     "Distinguish compilation from interpretation, and locate the "
     "hybrids.",
     "Explain why a miscompile is uniquely expensive.",
     "Set up the toolchain this course needs.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The phases",
   "blurb": "Text to machine code, in stages."},

  {"t": "code", "kicker": "Pipeline", "title": "What each phase establishes",
   "lang": "text", "code": """
  SOURCE TEXT
     |  LEXING          -- characters become TOKENS
     |                     establishes: the vocabulary is valid
     |  PARSING         -- tokens become a SYNTAX TREE
     |                     establishes: the structure is valid
     |  SEMANTIC ANALYSIS -- names resolved, types checked
     |                     establishes: the program MEANS something
     |  ========= FRONT END ends here =========
     |  IR GENERATION    -- tree becomes INTERMEDIATE REPRESENTATION
     |                     establishes: machine-independent, analysable
     |  OPTIMISATION     -- IR becomes better IR
     |                     establishes: nothing. It preserves meaning.
     |  ========= BACK END begins here ========
     |  INSTRUCTION SELECTION -- IR becomes target instructions
     |  REGISTER ALLOCATION   -- virtual registers become real ones
     |  SCHEDULING            -- instructions are ordered for the pipeline
     v
  MACHINE CODE

  Each phase REJECTS a class of invalid program, except optimisation,
  which rejects nothing and must preserve everything.
""",
   "caption": "<b>Optimisation is the odd one out:</b> every other phase "
              "establishes a property, and optimisation must preserve all "
              "of them.",
   "note": "Framing phases by what they establish is more useful than "
           "listing them."},

  {"t": "callout", "title": "The front end / back end split is about reuse",
   "kind": "Why the pipeline has that shape",
   "body": ["<b>The front end depends on the language and not on the "
            "machine.</b> The back end depends on the machine and not on "
            "the language.",
            "<b>So m languages and n targets need m + n components, not "
            "m × n</b> — provided they meet at a common IR.",
            "<b>That is why LLVM exists</b>, and why Rust, Swift, Julia, "
            "and Clang share a back end despite having nothing else in "
            "common.",
            "<b>And it is why the IR is the real design decision.</b> It "
            "is the interface, and interfaces are harder to change than "
            "implementations."]},

  {"t": "section", "label": "Part 2", "title": "The IR",
   "blurb": "The decision everything else follows from."},

  {"t": "callout", "title": "The IR determines which optimisations are even expressible",
   "kind": "The central claim of the course",
   "body": ["<b>An optimisation is a question plus a rewrite.</b> 'Is this "
            "value constant everywhere it is used?' — then fold it.",
            "<b>How expensive the question is depends entirely on the "
            "representation.</b> In a syntax tree, 'where does this "
            "variable's value come from?' requires a search.",
            "<b>In SSA form it is a pointer dereference</b> — every value "
            "is assigned exactly once, so the definition is unique and "
            "immediate (Module 07).",
            "<b>So changing the IR does not make optimisations faster; it "
            "makes different optimisations <i>practical</i>.</b> That is a "
            "much stronger claim, and it is why SSA won."]},

  {"t": "table", "kicker": "Representations", "title": "The representations, and what each is good at",
   "header": ["Representation", "Good for", "Bad at"],
   "widths": [2.9, 4.4, 4.8],
   "rows": [
     ["<b>Syntax tree (AST)</b>", "<b>Source-level checks; refactoring; errors</b>", "<b>Dataflow — control flow is implicit</b>"],
     ["<b>Three-address code</b>", "Simple, close to machines", "No explicit def-use links"],
     ["<b>Control flow graph</b>", "<b>Control flow explicit; dataflow analysis</b>", "Values still need searching for"],
     ["<b>SSA</b>", "<b>Def-use is O(1); most modern optimisation</b>", "<b>Needs &phi; functions and a destruction pass</b>"],
     ["Stack machine", "Compact; easy to generate", "<b>Hard to analyse; JVM and WASM use it</b>"],
     ["Machine code", "Runs", "Target-specific; nearly unanalysable"],
   ],
   "footnote": "<b>Real compilers use several at once</b> and lower between "
               "them — Clang has an AST, LLVM IR, SelectionDAG, and "
               "MachineIR.",
   "note": "The multiple-IRs point surprises people who expect one."},

  {"t": "section", "label": "Part 3", "title": "Compile or interpret",
   "blurb": "A spectrum, not a dichotomy."},

  {"t": "table", "kicker": "Spectrum", "title": "Where the work happens",
   "header": ["Approach", "When translated", "Trade"],
   "widths": [2.9, 4.0, 5.2],
   "rows": [
     ["<b>Ahead-of-time</b>", "Before running", "<b>Best code; no runtime profile available</b>"],
     ["<b>Tree-walking interpreter</b>", "Never", "<b>Simplest; 10–100× slower</b>"],
     ["<b>Bytecode VM</b>", "To bytecode, then interpreted", "<b>Portable; the usual scripting choice</b>"],
     ["<b>JIT</b>", "<b>At runtime, hot code only</b>", "<b>Uses real profiles; pays warmup</b>"],
     ["Tiered JIT", "Progressively, by heat", "<b>Fast start and fast peak. V8, HotSpot</b>"],
     ["<b>Shader compilation</b>", "<b>Partly offline, partly in-driver</b>", "<b>Module 13. The cause of stutter</b>"],
   ],
   "footnote": "<b>A JIT can beat an AOT compiler</b>, because it knows "
               "which branch actually ran and what types actually "
               "occurred.",
   "note": "That a JIT can win is counterintuitive and worth stating."},

  {"t": "section", "label": "Part 4", "title": "Why correctness dominates",
   "blurb": "The failure mode that has no analogue."},

  {"t": "callout", "title": "A miscompile is invisible from the source",
   "kind": "Why this course leads with correctness",
   "body": ["<b>Every other program's bugs are explicable by reading "
            "it.</b> A compiler bug is not — the source is correct and "
            "the behaviour is wrong.",
            "<b>So the search goes everywhere except where the problem "
            "is.</b> Days are lost before anyone suspects the compiler, "
            "because suspecting it feels like arrogance.",
            "<b>And the blast radius is everything the compiler "
            "built.</b> One wrong optimisation silently corrupts every "
            "program that triggered it.",
            "<b>Which is why Module 13's differential testing is not an "
            "appendix.</b> <b>Csmith found over 400 bugs in GCC and "
            "LLVM</b> — production compilers, heavily tested, used by "
            "everyone."]},

  {"t": "callout", "title": "Undefined behaviour is where most of them live",
   "kind": "The specific hazard",
   "body": ["<b>A language specification says what <i>must</i> happen and "
            "leaves the rest undefined</b> — signed overflow, null "
            "dereference, data races, out-of-bounds access.",
            "<b>Optimisers exploit undefined behaviour aggressively</b>, "
            "because assuming it cannot happen licenses stronger "
            "transformations.",
            "<b>So a program with UB can change meaning under "
            "optimisation</b> — correctly, by the standard, and "
            "catastrophically in practice. The null check deleted after "
            "the pointer was already dereferenced is the classic case.",
            "<b>This is not a compiler bug</b>, and it is indistinguishable "
            "from one when you meet it. <b>Knowing the difference is part "
            "of what this course is for.</b>"]},

  {"t": "bullets", "kicker": "Setup", "title": "What to have working before Module 02",
   "items": [
     "<b>A language with good tagged unions</b> — Rust enums, C++ "
     "<code>std::variant</code>, or OCaml. You will build many trees.",
     "",
     "<b>LLVM installed</b>, and try "
     "<code>clang -S -emit-llvm</code> on something small.",
     "",
     "<b>Read Crafting Interpreters, part II.</b> A working interpreter "
     "in your head makes every later module concrete.",
     "",
     "<b>A SPIR-V toolchain</b> — <code>glslangValidator</code> and "
     "<code>spirv-dis</code>. Disassemble a shader you already have.",
     "",
     "<b>Pick your source language now</b> and keep it small. Scope creep "
     "in the language is the usual way this project fails.",
   ],
   "footnote": "<b>Disassembling one of your own shaders in week one</b> "
               "is the most motivating thing available here."},
 ],
 "takeaways": [
   "Each phase establishes a property — valid vocabulary, valid "
   "structure, valid meaning — except optimisation, which establishes "
   "nothing and must preserve everything.",
   "The front end/back end split turns m×n into m+n, which is why "
   "unrelated languages share a back end.",
   "The IR is the central design decision because it determines which "
   "optimisations are expressible, not merely how fast they run.",
   "Real compilers use several IRs at once and lower between them.",
   "Compilation and interpretation are a spectrum, and a JIT can beat an "
   "AOT compiler because it has a real profile.",
   "A miscompile is invisible from the source, which is why differential "
   "testing matters more here than anywhere else.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The phases"),
  ("table", ["Phase", "Transformation", "What it establishes"],
   [["<b>Lexical analysis</b>", "Characters &rarr; tokens.",
     "<b>The vocabulary is valid.</b> Every piece of the input is a "
     "recognisable word of the language."],
    ["<b>Parsing</b>", "Tokens &rarr; syntax tree.",
     "<b>The structure is valid.</b> The words are arranged into "
     "well-formed phrases."],
    ["<b>Semantic analysis</b>",
     "Tree &rarr; annotated tree; names resolved, types checked.",
     "<b>The program <i>means</i> something.</b> Every name refers to "
     "something, and every operation is applied to things it can apply to."],
    ["<b>IR generation</b>", "Tree &rarr; intermediate representation.",
     "A machine-independent, analysable form. <b>The front end ends "
     "here.</b>"],
    ["<b>Optimisation</b>", "IR &rarr; better IR.",
     "<b>Nothing.</b> It is the only phase that establishes no new "
     "property — its whole obligation is to <i>preserve</i> every "
     "property the earlier phases established, while changing the program."],
    ["<b>Instruction selection</b>", "IR &rarr; target instructions.",
     "The operations are ones the machine has. <b>The back end.</b>"],
    ["<b>Register allocation</b>",
     "Unbounded virtual registers &rarr; the machine's finite set.",
     "The program fits the register file, with spills where it does not "
     "(Module 11)."],
    ["<b>Scheduling</b>", "Instructions reordered.",
     "The order suits the pipeline (CSCE 614). Must not change meaning."]],
   [0.21, 0.31, 0.48]),
  ("p", "<b>Framing the phases by what each establishes is more useful "
        "than listing them in order</b>, because it explains why they are "
        "in that order: each depends on the guarantee the previous one "
        "made. And it isolates optimisation as the odd phase — <b>the "
        "only one whose correctness condition is that it changes nothing "
        "observable</b>, which is exactly why it is the hardest to get "
        "right and the source of the worst bugs (&sect;4)."),
  ("callout", "The front end / back end split is about reuse",
   ["<b>The front end depends on the source language and not on the target "
    "machine. The back end depends on the machine and not on the "
    "language.</b> Neither needs to know anything about the other's "
    "domain.",
    "<b>So m languages and n targets require m + n components rather than "
    "m &times; n</b>, provided they all meet at a common intermediate "
    "representation. With five languages and six targets that is eleven "
    "pieces instead of thirty.",
    "<b>That is the entire reason LLVM exists</b>, and it is why Rust, "
    "Swift, Julia, Clang, and a long list of others share a back end "
    "despite having almost nothing in common at the source level.",
    "<b>And it is why the IR is the real design decision.</b> It is the "
    "interface between the two halves, and interfaces are far harder to "
    "change than implementations — every consumer depends on them. "
    "LLVM IR has evolved, but its fundamental shape has not, because it "
    "cannot."]),

  ("h1", "2 &nbsp; The intermediate representation"),
  ("callout", "The IR determines which optimisations are expressible",
   ["<b>An optimisation is a question plus a rewrite.</b> 'Is this value "
    "the same constant at every use?' — then substitute it. 'Is this "
    "computation already available?' — then reuse it. 'Is this result "
    "ever used?' — then delete it.",
    "<b>How expensive the question is depends entirely on the "
    "representation.</b> In a syntax tree, 'where does this variable's "
    "value come from at this point?' requires searching backwards through "
    "the tree and reasoning about control flow that the tree only "
    "represents implicitly.",
    "<b>In SSA form the same question is a pointer dereference.</b> Every "
    "value is assigned exactly once, so each use names its unique "
    "definition directly (Module 07).",
    "<b>So changing the IR does not merely make optimisations faster; it "
    "makes different optimisations <i>practical</i>.</b> Analyses that "
    "would be quadratic searches become constant-time lookups, which moves "
    "them from 'theoretically possible' to 'run on every function'. "
    "<b>That is a much stronger claim than a constant-factor speedup, and "
    "it is why SSA displaced everything else.</b>"]),
  ("table", ["Representation", "Good for", "Bad at"],
   [["<b>Abstract syntax tree</b>",
     "<b>Source-level checks, refactoring tools, and error messages</b> "
     "— it still corresponds to what the user wrote.",
     "<b>Dataflow.</b> Control flow is implicit in the tree structure, so "
     "any question about what reaches what requires reconstructing it."],
    ["<b>Three-address code</b>",
     "Simple, linear, and close to what machines execute.",
     "No explicit link from a use back to its definition."],
    ["<b>Control flow graph</b>",
     "<b>Control flow is explicit</b>, which is the precondition for "
     "dataflow analysis (Module 08).",
     "Values still have to be searched for — the graph says where "
     "control goes, not where data comes from."],
    ["<b>SSA</b>",
     "<b>Def-use is O(1), which makes most modern optimisation "
     "practical.</b> The default for nearly every serious compiler.",
     "<b>Requires &phi; functions</b> at merge points and a destruction "
     "pass before code generation (Module 07, Module 11)."],
    ["<b>Stack machine code</b>",
     "Compact and very easy to generate from a tree.",
     "<b>Hard to analyse</b> — operands are implicit in stack "
     "position. The JVM and WebAssembly use it, and their optimisers "
     "reconstruct an SSA form internally."],
    ["<b>Machine code</b>", "It runs.",
     "Target-specific and nearly unanalysable — which is what makes "
     "decompilation hard."]],
   [0.19, 0.39, 0.42]),
  ("p", "<b>Real compilers use several of these simultaneously and lower "
        "between them.</b> Clang alone has an AST, LLVM IR, SelectionDAG, "
        "and MachineIR, each chosen because it suits a particular range of "
        "transformations. <b>The question is never 'which IR' but 'which "
        "IR for which phase'</b>, and the lowering points between them are "
        "themselves design decisions."),

  ("break",),
  ("h1", "3 &nbsp; Compilation and interpretation"),
  ("table", ["Approach", "When translation happens", "The trade"],
   [["<b>Ahead-of-time compilation</b>", "Entirely before running.",
     "<b>The best code, and no runtime information.</b> The compiler must "
     "guess which branch is hot and which types occur."],
    ["<b>Tree-walking interpreter</b>", "Never — the tree is walked.",
     "<b>By far the simplest to build</b>, and 10 to 100&times; slower "
     "than compiled code. Entirely adequate for configuration and for "
     "build scripts."],
    ["<b>Bytecode virtual machine</b>",
     "Source to bytecode once; bytecode interpreted.",
     "<b>Portable, compact, and much faster than tree walking.</b> The "
     "usual choice for an embedded scripting language (Module 12)."],
    ["<b>Just-in-time compilation</b>",
     "<b>At runtime, for hot code only.</b>",
     "<b>Uses real profiles</b> — actual branch frequencies and actual "
     "types — and pays a warmup cost plus the memory for the compiler "
     "itself."],
    ["<b>Tiered JIT</b>",
     "Progressively: interpret, then cheaply compile, then optimise hard.",
     "<b>Fast startup and fast peak performance.</b> What V8 and HotSpot "
     "do, and the reason both are enormous."],
    ["<b>Shader compilation</b>",
     "<b>Partly offline to SPIR-V, partly in the driver at load or draw "
     "time.</b>",
     "<b>Module 13</b>, and the direct cause of shader compilation "
     "stutter."]],
   [0.21, 0.31, 0.48]),
  ("p", "<b>A JIT can beat an ahead-of-time compiler</b>, which "
        "consistently surprises people. It knows which branch actually ran, "
        "which types actually occurred at a polymorphic call site, and "
        "which values turned out to be constant in practice — so it "
        "can specialise on facts that are true of this execution and are "
        "not provable in general. <b>It guards the assumption and "
        "deoptimises when it fails</b>, which is a trade an AOT compiler "
        "cannot make."),

  ("h1", "4 &nbsp; Why correctness dominates this course"),
  ("callout", "A miscompile is invisible from the source",
   ["<b>Every other program's bugs are explicable by reading it.</b> The "
    "behaviour follows from the code, so the code is where you look. A "
    "compiler bug breaks that assumption entirely: <b>the source is "
    "correct and the behaviour is wrong</b>, and nothing in the program "
    "accounts for it.",
    "<b>So the search goes everywhere except where the problem is.</b> "
    "Days are routinely lost before anyone seriously suspects the "
    "compiler, partly because the hypothesis feels like arrogance — "
    "the compiler is used by millions and your code is not.",
    "<b>And the blast radius is everything the compiler built.</b> A "
    "single wrong optimisation silently corrupts every program that "
    "happened to trigger it, across every project using that compiler "
    "version, with no error anywhere.",
    "<b>Which is why Module 13's differential testing is not an "
    "appendix.</b> <b>Csmith — a random C program generator — "
    "found over 400 bugs in GCC and LLVM</b>, production compilers that "
    "were already extremely heavily tested and used by essentially "
    "everyone. <b>Hand-written test suites did not find those bugs and "
    "would not have.</b>"]),
  ("callout", "Undefined behaviour is where most of them live",
   ["<b>A language specification says what <i>must</i> happen and "
    "deliberately leaves the rest undefined</b> — signed integer "
    "overflow, dereferencing null, data races, reading past an array, "
    "strict aliasing violations. Undefined means the standard imposes no "
    "requirement at all.",
    "<b>Optimisers exploit undefined behaviour aggressively</b>, because "
    "assuming it cannot occur licenses much stronger transformations. If "
    "signed overflow is undefined, the compiler may assume "
    "<code>x + 1 &gt; x</code> always holds and delete the check.",
    "<b>So a program containing undefined behaviour can change meaning "
    "under optimisation</b> — correctly, by the standard, and "
    "catastrophically in practice. <b>The canonical case is a null check "
    "deleted because the pointer was already dereferenced above it:</b> "
    "the dereference would be undefined if the pointer were null, so the "
    "compiler concludes it is not null, so the check is dead. Every step "
    "is valid; the result is a security hole.",
    "<b>This is not a compiler bug</b>, and <b>it is indistinguishable "
    "from one when you first meet it</b> — the symptom is the same: "
    "correct-looking source, wrong behaviour, appears only at -O2. "
    "<b>Learning to tell the two apart is part of what this course is "
    "for</b>, and the practical tools are the sanitisers (CSCE 735 "
    "Module 13) and bisecting the optimisation level."]),
  ("ul", ["<b>A language with good tagged unions</b> — Rust enums, "
          "C++ <code>std::variant</code> with a visitor, or OCaml. You "
          "will write a great deal of tree and graph manipulation, and the "
          "ergonomics of that one feature dominate the experience.",
          "<b>LLVM installed.</b> Run <code>clang -S -emit-llvm</code> on "
          "something small and read the output — <b>you are looking at "
          "the SSA form of Module 07</b>, and seeing it early makes that "
          "module land.",
          "<b>Read Crafting Interpreters, part II.</b> Having a complete "
          "working implementation in your head makes every later module "
          "concrete rather than abstract, and it is a weekend.",
          "<b>A SPIR-V toolchain</b> — <code>glslangValidator</code> "
          "and <code>spirv-dis</code>. <b>Disassemble one of your own "
          "shaders in week one</b>; it is the most motivating thing "
          "available in this course, and it is also an SSA IR you can "
          "read.",
          "<b>Pick your source language now and keep it deliberately "
          "small.</b> Integers, booleans, functions, control flow, and one "
          "aggregate type is plenty. <b>Scope creep in the source language "
          "is the usual way this project fails</b> — every feature "
          "added costs work in all eight phases."]),
 ],
 "resources": [
   ("Nystrom &mdash; Crafting Interpreters (free book)",
    "https://craftinginterpreters.com/",
    "<b>Read part II this week.</b> A complete tree-walking interpreter, "
    "then a complete bytecode VM, with every line explained."),
   ("Stanford CS143 &mdash; Compilers, lecture 1 (free)",
    "https://web.stanford.edu/class/cs143/",
    "The phase structure of &sect;1, with worked examples of what each one "
    "catches."),
   ("Chris Lattner &mdash; LLVM, in The Architecture of Open Source "
    "Applications (free)",
    "https://aosabook.org/en/v1/llvm.html",
    "<b>The &sect;1 reuse argument and the &sect;2 IR argument</b>, from "
    "the person who built the system that made both famous. Short."),
   ("Yang, Chen, Eide & Regehr &mdash; Finding and Understanding Bugs in C "
    "Compilers (free)",
    "https://www.flux.utah.edu/paper/yang-pldi11",
    "<b>The Csmith paper of &sect;4.</b> Read the results section now and "
    "the method in Module 13."),
   ("Regehr &mdash; A Guide to Undefined Behavior in C and C++ (free)",
    "https://blog.regehr.org/archives/213",
    "The &sect;4 hazard, with the deleted-null-check example worked "
    "through."),
 ],
 "exercises": [
   "Run <code>clang -S -emit-llvm</code> on a ten-line function and read "
   "the output. Identify the basic blocks.",
   "Compile the same function at <code>-O0</code> and <code>-O2</code> and "
   "diff the IR. Name three transformations you can see.",
   "<b>Disassemble one of your own shaders</b> with "
   "<code>spirv-dis</code> and find the entry point and the control flow.",
   "Write a tokeniser for arithmetic expressions by hand, with no "
   "libraries.",
   "Write a tree-walking interpreter for arithmetic with variables.",
   "<b>Measure it against compiled C</b> on the same computation and "
   "report the ratio.",
   "<b>Write a program with signed overflow</b> and show that it behaves "
   "differently at <code>-O0</code> and <code>-O2</code>.",
   "Reproduce the deleted-null-check example and inspect the generated "
   "code.",
   "Run the same program under UBSan and report what it says.",
   "<b>Specify your project language in one page</b> — grammar, "
   "types, and an explicit list of what it will not have.",
 ],
 "selfcheck": [
   "Name the eight phases and say what each establishes.",
   "Why is optimisation the odd phase out?",
   "What does the front end/back end split buy, and what does it cost?",
   "Why is the IR the central design decision?",
   "Compare six representations on what they are good and bad at.",
   "Give six points on the compile–interpret spectrum.",
   "Why can a JIT beat an ahead-of-time compiler?",
   "Why is a miscompile uniquely expensive to diagnose?",
   "What is undefined behaviour and why do optimisers exploit it?",
 ],
},

]

for _b in ("c605_b2", "c605_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
