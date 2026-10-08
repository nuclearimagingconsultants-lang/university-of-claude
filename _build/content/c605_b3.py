# -*- coding: utf-8 -*-
"""CSCE 605 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Dataflow Analysis",
 "subtitle": "Facts that hold at every program point, computed by "
             "iteration.",
 "question": "What is true here, on every path that reaches here?",
 "outcomes": [
     "Formulate an analysis as a lattice plus transfer functions.",
     "Explain why the iteration terminates and what it converges to.",
     "Implement liveness, reaching definitions, and available "
     "expressions.",
     "Distinguish forward from backward and may from must.",
     "Explain what static analysis fundamentally cannot do.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The framework",
   "blurb": "One algorithm, many analyses."},

  {"t": "callout", "title": "Every dataflow analysis is the same four things",
   "kind": "The framework",
   "body": ["<b>A lattice of facts</b> — the possible answers, with a "
            "partial order and a meet operation for combining them.",
            "<b>A transfer function per instruction</b> — how an "
            "instruction changes the facts.",
            "<b>A direction</b> — forward (facts flow with control) or "
            "backward (facts flow against it).",
            "<b>A meet operator</b> — intersection for <i>must</i> "
            "analyses, union for <i>may</i> analyses. <b>Choose these four "
            "and the algorithm is already written</b>, which is why this "
            "is called a framework rather than a technique."]},

  {"t": "code", "kicker": "The algorithm", "title": "Iterate to a fixpoint",
   "lang": "text", "code": """
  initialise every block's OUT to the lattice TOP
  worklist = all blocks

  while worklist not empty:
      b = worklist.pop()
      IN[b]  = MEET over all predecessors p of OUT[p]      # forward
      new    = TRANSFER(b, IN[b])
      if new != OUT[b]:
          OUT[b] = new
          worklist += successors(b)      # they must be redone

  WHY IT TERMINATES:
    * the lattice has finite height
    * transfer functions are MONOTONE: more input facts never
      produce fewer output facts
    * so each OUT only ever moves DOWN the lattice, and it
      cannot move down forever

  WHAT IT CONVERGES TO:
    the MAXIMAL FIXPOINT -- the most precise answer obtainable
    by this method. NOT necessarily the true answer (Part 4).

  Worklist order matters for SPEED, never for the RESULT.
""",
   "caption": "<b>Reverse postorder for forward analyses</b>, postorder "
              "for backward — typically a few times faster than "
              "arbitrary order.",
   "note": "Termination resting on monotonicity + finite height is the "
           "key theoretical point."},

  {"t": "section", "label": "Part 2", "title": "The classical analyses",
   "blurb": "Four, and what each enables."},

  {"t": "table", "kicker": "Catalogue", "title": "The four you must know",
   "header": ["Analysis", "Direction / meet", "Enables"],
   "widths": [3.0, 4.1, 5.0],
   "rows": [
     ["<b>Liveness</b>", "<b>Backward, union (may)</b>", "<b>Register allocation; dead store removal</b>"],
     ["<b>Reaching definitions</b>", "Forward, union (may)", "<b>Use-def chains; constant propagation</b>"],
     ["<b>Available expressions</b>", "<b>Forward, intersection (must)</b>", "<b>Common subexpression elimination</b>"],
     ["<b>Very busy expressions</b>", "Backward, intersection (must)", "Code hoisting; size reduction"],
     ["Constant propagation", "Forward, special lattice", "<b>Folding; branch elimination</b>"],
     ["Alias analysis", "Forward, may", "<b>Everything involving memory</b>"],
   ],
   "footnote": "<b>May analyses use union and are conservative by "
               "over-approximating; must analyses use intersection.</b> "
               "Getting this backwards produces unsound optimisation.",
   "note": "The may/must + union/intersection pairing is the thing to "
           "memorise."},

  {"t": "callout", "title": "Liveness is the one you cannot avoid",
   "kind": "Why it matters most",
   "body": ["<b>A variable is live at a point if its current value may be "
            "read before being overwritten.</b>",
            "<b>Backward, because liveness flows from uses back toward "
            "definitions.</b> Union at merges, because a value live on "
            "<i>any</i> successor path is live.",
            "<b>Register allocation is built on it</b> — two values can "
            "share a register exactly when they are never live "
            "simultaneously (Module 11).",
            "<b>And it finds dead stores directly:</b> a definition whose "
            "variable is not live immediately after it is dead and can be "
            "deleted."]},

  {"t": "section", "label": "Part 3", "title": "Precision",
   "blurb": "Where the cost goes."},

  {"t": "table", "kicker": "Precision", "title": "The axes you can pay along",
   "header": ["Axis", "Cheap version", "Precise version"],
   "widths": [2.8, 4.3, 5.0],
   "rows": [
     ["<b>Flow</b>", "<b>Flow-insensitive: one fact per variable</b>", "<b>Flow-sensitive: per program point</b>"],
     ["<b>Path</b>", "Path-insensitive: merge at joins", "<b>Path-sensitive: exponential</b>"],
     ["<b>Context</b>", "<b>One summary per function</b>", "<b>Per call site; exponential</b>"],
     ["Field", "Whole objects", "Per field"],
     ["<b>Heap</b>", "<b>One node per allocation site</b>", "Shape analysis; very expensive"],
   ],
   "footnote": "<b>Every axis trades precision against cost "
               "exponentially</b>, which is why production compilers stay "
               "near the cheap end and accept conservative answers.",
   "note": "The exponential blowup on each axis is why 'just be more "
           "precise' is not available."},

  {"t": "callout", "title": "Alias analysis is the one that limits everything else",
   "kind": "The practical bottleneck",
   "body": ["<b>'Can these two pointers refer to the same storage?'</b> If "
            "the answer is 'maybe', almost every memory optimisation is "
            "blocked.",
            "<b>And the answer is usually 'maybe'</b>, because proving "
            "otherwise requires reasoning about the whole program.",
            "<b>So a store through an unknown pointer invalidates every "
            "cached load</b>, and a value cannot be kept in a register "
            "across it.",
            "<b>This is exactly why shader languages forbid pointers</b> "
            "(Module 06 §4) and why <code>restrict</code>, Fortran's "
            "aliasing rules, and Rust's borrow checker all exist. <b>They "
            "are all the same answer to the same problem.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Limits",
   "blurb": "What no analysis can do."},

  {"t": "callout", "title": "Every static analysis is conservative by necessity",
   "kind": "Rice's theorem, again",
   "body": ["<b>Any non-trivial semantic property of programs is "
            "undecidable</b> (CSCE 627, and Module 06 §1).",
            "<b>So the analysis must err in a safe direction</b> — "
            "reporting that something <i>may</i> happen when it cannot, "
            "never that it cannot when it may.",
            "<b>Which direction is safe depends on the use.</b> For dead "
            "code elimination, over-estimating liveness is safe; "
            "under-estimating deletes live code.",
            "<b>Getting the direction wrong produces a miscompile</b> "
            "(Module 01 §4), not merely a missed optimisation. <b>This is "
            "the single most important thing to be careful about in this "
            "module.</b>"]},

  {"t": "callout", "title": "SSA makes several of these unnecessary",
   "kind": "The connection to Module 07",
   "body": ["<b>Reaching definitions is the question SSA answers by "
            "construction</b> — each use already names its definition, so "
            "the analysis is not needed at all.",
            "<b>Constant propagation becomes local</b>, or sparse "
            "conditional constant propagation over the SSA graph, which is "
            "both faster and <i>more</i> precise than the dataflow "
            "version.",
            "<b>Liveness is still needed</b>, and is cheaper to compute "
            "because def-use chains are explicit.",
            "<b>And memory analyses are unaffected</b> — SSA applies to "
            "registers, not to the heap, which is why alias analysis "
            "remains the bottleneck."]},
 ],
 "takeaways": [
   "Every dataflow analysis is a lattice, transfer functions, a direction, "
   "and a meet operator — choose those four and the algorithm is "
   "already written.",
   "Iteration terminates because the lattice has finite height and transfer "
   "functions are monotone, so facts only move one way.",
   "May analyses meet with union and must analyses with intersection; "
   "reversing this produces unsound optimisation.",
   "Liveness is backward and may, and register allocation is built directly "
   "on it.",
   "Alias analysis is the bottleneck — 'maybe' blocks nearly every "
   "memory optimisation, which is why restrict, Fortran's rules, and Rust's "
   "borrow checker all exist.",
   "SSA answers reaching definitions by construction, but leaves memory "
   "analysis exactly where it was.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The dataflow framework"),
  ("callout", "Every dataflow analysis is the same four things",
   ["<b>A lattice of facts.</b> The set of possible answers, equipped with "
    "a partial order (how precise one answer is relative to another) and a "
    "meet operation for combining answers arriving from different paths.",
    "<b>A transfer function per instruction</b>, describing how that "
    "instruction transforms the facts holding before it into the facts "
    "holding after it.",
    "<b>A direction.</b> <i>Forward</i> analyses propagate facts along "
    "control flow (what has happened already); <i>backward</i> analyses "
    "propagate against it (what will happen next).",
    "<b>A meet operator.</b> <b>Intersection for <i>must</i> analyses</b> "
    "(the fact holds on <i>all</i> paths) and <b>union for <i>may</i> "
    "analyses</b> (the fact holds on <i>some</i> path). <b>Choose those "
    "four and the algorithm is already written</b> — which is why "
    "this is called a framework: the iteration below is shared by every "
    "analysis in &sect;2."]),
  ("code", """initialise every block's OUT to lattice TOP
worklist = all blocks

while worklist not empty:
    b = worklist.pop()
    IN[b] = MEET over predecessors p of OUT[p]       # forward
    new   = TRANSFER(b, IN[b])
    if new != OUT[b]:
        OUT[b] = new
        worklist += successors(b)

TERMINATES because: the lattice has FINITE HEIGHT, and transfer
functions are MONOTONE -- more input facts never yield fewer
output facts -- so each OUT only moves DOWN, finitely often.

CONVERGES TO: the maximal fixpoint. The most precise answer this
method can give -- not necessarily the TRUE answer (section 4)."""),
  ("p", "<b>Worklist order affects speed, never the result.</b> Reverse "
        "postorder for forward analyses and postorder for backward ones "
        "typically converge several times faster than arbitrary order, "
        "because they tend to process a block after its predecessors have "
        "settled. <b>That the final answer is order-independent is the "
        "fixpoint property</b>, and it is worth asserting in tests: "
        "shuffling the worklist and getting a different answer means a "
        "non-monotone transfer function, which is a bug."),

  ("h1", "2 &nbsp; The classical analyses"),
  ("table", ["Analysis", "Direction and meet", "What it enables"],
   [["<b>Liveness</b>", "<b>Backward, union (may).</b>",
     "<b>Register allocation</b> (Module 11) and dead store elimination. "
     "See the callout below."],
    ["<b>Reaching definitions</b>", "Forward, union (may).",
     "<b>Use-def chains</b>, and hence constant propagation. <b>Made "
     "unnecessary by SSA</b> (&sect;4)."],
    ["<b>Available expressions</b>",
     "<b>Forward, intersection (must).</b>",
     "<b>Common subexpression elimination</b> — an expression already "
     "computed on <i>every</i> path reaching here need not be recomputed."],
    ["<b>Very busy expressions</b>", "Backward, intersection (must).",
     "Code hoisting, and hence code size reduction — an expression "
     "computed on every path <i>from</i> here can be computed once, now."],
    ["<b>Constant propagation</b>",
     "Forward, with a special three-level lattice (unknown / constant c / "
     "not constant).",
     "<b>Constant folding and branch elimination</b>, which together "
     "frequently unlock everything else."],
    ["<b>Alias analysis</b>", "Forward, may.",
     "<b>Everything that touches memory</b> — and it is the "
     "bottleneck (&sect;3)."]],
   [0.20, 0.33, 0.47]),
  ("p", "<b>The may/must and union/intersection pairing is the thing to "
        "memorise</b>, and getting it backwards is not a precision bug but "
        "a soundness bug: a <i>may</i> analysis that meets with "
        "intersection under-approximates, which licenses transformations "
        "that are not valid on all paths."),
  ("callout", "Liveness is the one you cannot avoid",
   ["<b>A variable is live at a program point if its current value may be "
    "read at some point in the future before being overwritten.</b> Note "
    "'may' — liveness along any single successor path is enough.",
    "<b>It is backward because liveness flows from uses back toward "
    "definitions</b>, and the meet is union because a value live on "
    "<i>any</i> successor path must be kept.",
    "<b>Register allocation is built directly on it:</b> two values can "
    "share a register exactly when they are never simultaneously live, "
    "which is what the interference graph of Module 11 encodes. <b>Without "
    "liveness there is no register allocation</b>, which is why this is the "
    "analysis every compiler has.",
    "<b>And it finds dead stores for free:</b> a definition whose variable "
    "is not live immediately after it can never be read, so the definition "
    "is dead and can be deleted — which in turn may make its operands "
    "dead, so the elimination iterates."]),

  ("break",),
  ("h1", "3 &nbsp; Precision, and what it costs"),
  ("table", ["Axis", "Cheap version", "Precise version"],
   [["<b>Flow sensitivity</b>",
     "<b>Flow-insensitive: one fact per variable for the whole "
     "function.</b> Very fast.",
     "<b>Flow-sensitive: a fact per variable per program point.</b> The "
     "framework above. Linear in program points, which is affordable."],
    ["<b>Path sensitivity</b>",
     "Path-insensitive: merge facts at every join, losing the correlation "
     "between branches.",
     "<b>Path-sensitive: track facts per path.</b> <b>Exponential in the "
     "number of branches</b>, so used only in bug-finding tools with "
     "aggressive path pruning."],
    ["<b>Context sensitivity</b>",
     "<b>One summary per function</b>, merging all call sites.",
     "<b>A separate analysis per call site</b>, or per call <i>string</i> "
     "— <b>exponential in call depth</b>. k-limiting is the usual "
     "compromise."],
    ["<b>Field sensitivity</b>",
     "Treat an object as one indivisible thing.",
     "Track each field separately. Affordable and usually worth it."],
    ["<b>Heap modelling</b>",
     "<b>One abstract node per allocation site</b>, so all objects from one "
     "<code>new</code> are conflated.",
     "Shape analysis, distinguishing individual heap cells. <b>Very "
     "expensive</b>, and mostly confined to verification tools."]],
   [0.19, 0.38, 0.43]),
  ("p", "<b>Every one of these axes trades precision against cost "
        "exponentially</b>, which is why production compilers sit near the "
        "cheap end on most of them and accept conservative answers. "
        "'Just be more precise' is not an available option, and a "
        "compiler that spent exponential time to find one more constant "
        "would not be used."),
  ("callout", "Alias analysis is what limits everything else",
   ["<b>The question is: can these two pointers refer to the same "
    "storage?</b> The possible answers are no, yes, and maybe — and "
    "<b>if the answer is 'maybe', almost every memory optimisation is "
    "blocked</b>.",
    "<b>And the answer is usually 'maybe'</b>, because proving two pointers "
    "distinct generally requires reasoning about the whole program, "
    "including code the compiler cannot see.",
    "<b>So a store through an unknown pointer invalidates every cached "
    "load</b>, a value cannot be held in a register across it, loops cannot "
    "be vectorised across it, and instructions cannot be reordered around "
    "it. The conservative assumption is correct and extremely expensive.",
    "<b>This is precisely why shader languages forbid pointers</b> "
    "(Module 06 &sect;4), why C has <code>restrict</code>, why Fortran's "
    "stricter aliasing rules let it beat C on numerical code for decades, "
    "and why Rust's borrow checker lets <code>rustc</code> emit "
    "<code>noalias</code> on essentially every reference. <b>Four "
    "apparently unrelated language features that are all the same answer to "
    "this one analysis problem</b> — which is a good illustration of "
    "how much language design is downstream of what the compiler can "
    "prove."]),

  ("h1", "4 &nbsp; Limits"),
  ("callout", "Every static analysis is conservative by necessity",
   ["<b>Any non-trivial semantic property of programs is undecidable</b> "
    "— Rice's theorem again (Module 06 &sect;1). No analysis can be "
    "exactly right about whether a variable is live, whether an expression "
    "is constant, or whether two pointers alias.",
    "<b>So the analysis must err in a <i>safe</i> direction</b> — "
    "reporting that something <i>may</i> happen when in fact it cannot, "
    "never that it cannot when in fact it may.",
    "<b>Which direction is safe depends entirely on how the result is "
    "used.</b> For dead code elimination, over-estimating liveness is safe "
    "(you keep code you could have deleted) and under-estimating is "
    "catastrophic (you delete live code). For a different client the "
    "safe direction may be the opposite.",
    "<b>Getting the direction wrong produces a miscompile</b> (Module 01 "
    "&sect;4), not a missed optimisation — and it will be found by a "
    "user, months later, in release builds only. <b>This is the single "
    "thing to be most careful about in this module</b>, and it should be "
    "stated explicitly in the comment above every transfer function you "
    "write."]),
  ("callout", "SSA makes several of these unnecessary",
   ["<b>Reaching definitions is the question SSA answers by "
    "construction</b> (Module 07 &sect;2). Each use already names its "
    "unique definition, so the analysis simply is not needed — the "
    "representation has the answer.",
    "<b>Constant propagation becomes local</b>, or better, <i>sparse "
    "conditional</i> constant propagation walking the SSA graph — "
    "which is both faster than the dataflow version and <b>strictly more "
    "precise</b>, because it can prove a branch never taken and ignore the "
    "values flowing along it.",
    "<b>Liveness is still required</b>, and is cheaper to compute in SSA "
    "because def-use chains are explicit and live ranges have a known "
    "structure.",
    "<b>And memory analyses are entirely unaffected.</b> <b>SSA applies to "
    "register-like values, not to the heap</b> — memory still has "
    "aliasing, still has unknown stores, and still blocks everything. "
    "<b>Which is why alias analysis remains the bottleneck no matter how "
    "good the IR is</b>, and why the language-level answers in &sect;3 "
    "matter more than any compiler improvement."]),
 ],
 "resources": [
   ("Cooper & Torczon &mdash; Engineering a Compiler, chapter 9",
    "https://www.elsevier.com/books/engineering-a-compiler/cooper/978-0-12-815412-0",
    "<b>The framework of &sect;1 and the analyses of &sect;2</b>, with the "
    "termination argument done properly."),
   ("Kildall; and Nielson, Nielson & Hankin &mdash; Principles of Program "
    "Analysis",
    "https://link.springer.com/book/10.1007/978-3-662-03811-6",
    "The lattice-theoretic foundations. Heavy going; useful for the "
    "monotonicity and fixpoint results."),
   ("Hind &mdash; Pointer Analysis: Haven't We Solved This Problem Yet? "
    "(free)",
    "https://dl.acm.org/doi/10.1145/379605.379665",
    "<b>The &sect;3 bottleneck, surveyed.</b> The title is the "
    "conclusion."),
   ("Wegman & Zadeck &mdash; Constant Propagation with Conditional "
    "Branches (free)",
    "https://dl.acm.org/doi/10.1145/103135.103136",
    "<b>Sparse conditional constant propagation</b> — the &sect;4 "
    "result that SSA makes an analysis both faster and more precise."),
 ],
 "exercises": [
   "Implement the generic worklist algorithm, parameterised on direction, "
   "meet, and transfer.",
   "Instantiate it for liveness and verify against hand-computed answers "
   "on a small CFG.",
   "<b>Shuffle the worklist order and confirm the answer is "
   "unchanged</b>, then confirm the iteration count changes.",
   "Implement reaching definitions and available expressions.",
   "<b>Write a non-monotone transfer function deliberately</b> and "
   "observe the iteration fail to converge or converge inconsistently.",
   "Implement dead store elimination from liveness and measure how many "
   "stores it removes on real code.",
   "Implement a flow-insensitive and a flow-sensitive version of one "
   "analysis. Compare precision and runtime.",
   "<b>Implement a simple alias analysis</b> (address-taken, then "
   "allocation-site-based) and measure how many loads each lets you "
   "cache.",
   "Add <code>restrict</code> to a C function and compare the generated "
   "code with and without.",
   "<b>Implement sparse conditional constant propagation</b> over SSA and "
   "find a case where it beats the dataflow version.",
 ],
 "selfcheck": [
   "Name the four components of a dataflow analysis.",
   "Why does the iteration terminate, and what does it converge to?",
   "Does worklist order affect the answer? What does it affect?",
   "Give six analyses with their direction and meet.",
   "Why do may analyses use union and must analyses intersection?",
   "Why is liveness unavoidable?",
   "Name five precision axes and the cost of each.",
   "Why is alias analysis the bottleneck, and name four language-level "
   "responses.",
   "Why must every analysis be conservative, and what happens if you err "
   "the wrong way?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Optimisation",
 "subtitle": "A search with no gradient, settled by measurement.",
 "question": "Which transformations actually make programs faster?",
 "outcomes": [
     "Implement the standard local and global optimisations.",
     "Explain loop optimisations and why loops dominate.",
     "Explain the phase-ordering problem.",
     "Explain inlining as the enabling transformation.",
     "Measure a pass honestly, including when it loses.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The catalogue",
   "blurb": "What the standard passes do."},

  {"t": "table", "kicker": "Passes", "title": "The standard optimisations",
   "header": ["Pass", "What it does", "Needs"],
   "widths": [3.2, 4.3, 4.6],
   "rows": [
     ["<b>Constant folding</b>", "Evaluate at compile time", "Nothing"],
     ["<b>Constant propagation</b>", "<b>Replace a variable by its known value</b>", "<b>SSA, or reaching definitions</b>"],
     ["<b>Dead code elimination</b>", "<b>Delete results nobody uses</b>", "<b>Liveness, or SSA use counts</b>"],
     ["<b>CSE / GVN</b>", "<b>Reuse an already-computed value</b>", "Available expressions, or SSA"],
     ["Copy propagation", "Replace a copy by its source", "SSA"],
     ["<b>Inlining</b>", "<b>Replace a call by the body</b>", "<b>Call graph. The enabler (Part 3)</b>"],
     ["Strength reduction", "<b>Multiply → add in loops</b>", "Loop structure"],
     ["<b>LICM</b>", "<b>Hoist loop-invariant work out</b>", "<b>Loop structure + dominance</b>"],
   ],
   "footnote": "<b>These interact.</b> Inlining enables constant "
               "propagation, which enables branch folding, which enables "
               "dead code elimination, which can enable more inlining.",
   "note": "The cascade is the real behaviour; individual passes are "
           "unimpressive alone."},

  {"t": "callout", "title": "Loops are where the time is, and where the wins are",
   "kind": "Why loop optimisation is a category",
   "body": ["<b>Programs spend nearly all their time in loops</b>, so a "
            "transformation inside a loop is multiplied by the trip "
            "count.",
            "<b>LICM hoists computations that do not change</b> out of the "
            "loop — one evaluation instead of n.",
            "<b>Strength reduction replaces a multiply by an add:</b> an "
            "induction variable <code>i*4</code> becomes a running sum.",
            "<b>Unrolling amortises the loop overhead</b> and exposes "
            "instruction-level parallelism (CSCE 614). <b>Vectorisation "
            "then uses the SIMD units</b> (CSCE 735 M02), and it is the "
            "single largest available win when it applies."]},

  {"t": "section", "label": "Part 2", "title": "Phase ordering",
   "blurb": "The problem with no clean answer."},

  {"t": "callout", "title": "Passes enable and disable each other",
   "kind": "The phase-ordering problem",
   "body": ["<b>Running A before B can expose opportunities for B</b> — "
            "or destroy them.",
            "<b>Inlining before constant propagation</b> lets arguments "
            "become constants. <b>After it</b>, that opportunity is "
            "missed.",
            "<b>But inlining increases code size</b>, which can hurt "
            "instruction cache behaviour and <i>reduce</i> performance "
            "(CSCE 614).",
            "<b>There is no ordering that is optimal for all "
            "programs</b>, and finding the optimal ordering for a given "
            "program is intractable. <b>So real compilers use a "
            "hand-tuned sequence, repeated</b> — LLVM's pipeline runs some "
            "passes several times for exactly this reason."]},

  {"t": "code", "kicker": "In practice", "title": "What a real pipeline looks like",
   "lang": "text", "code": """
  LLVM -O2, heavily abridged:

      SROA                   (promote memory to registers -- first,
                              because everything else needs SSA values)
      early CSE
      simplify CFG
      instcombine            (peephole over IR)
      inline                 (the enabler)
      ...
      SROA again             (inlining exposed more)
      instcombine again
      jump threading
      LICM
      loop unroll / vectorise
      GVN
      dead store elimination
      simplify CFG again
      ...

  Note SROA, instcombine, and simplify-CFG appear MULTIPLE times.
  Each pass creates opportunities for the ones before it, so the
  sequence is not a pipeline so much as a hand-tuned loop.

  `opt -print-after-all` shows every intermediate. Read it once.
""",
   "caption": "<b>The repetition is the admission</b> that the ordering "
              "problem has no clean solution.",
   "note": "Telling them to actually run print-after-all is the most "
           "valuable instruction in the module."},

  {"t": "section", "label": "Part 3", "title": "Inlining",
   "blurb": "The one that matters most."},

  {"t": "callout", "title": "Inlining is valuable for what it enables, not for the call",
   "kind": "The common misunderstanding",
   "body": ["<b>Removing the call overhead is a minor benefit</b> — a "
            "call is a few cycles and is well predicted.",
            "<b>The real value is that it makes the callee's body visible "
            "to every other optimisation</b>, with the caller's actual "
            "arguments substituted.",
            "<b>So a constant argument becomes a constant inside the "
            "body</b>, a branch on it folds, half the body becomes dead, "
            "and what remains may inline further.",
            "<b>Inlining is the transformation that unlocks the "
            "others</b>, which is why C++ templates and Rust generics are "
            "fast: monomorphisation is inlining with the types "
            "substituted too."]},

  {"t": "table", "kicker": "Heuristics", "title": "Deciding what to inline",
   "header": ["Signal", "Effect", "Note"],
   "widths": [3.0, 4.2, 4.9],
   "rows": [
     ["<b>Callee size</b>", "<b>Small ⇒ inline</b>", "<b>The dominant signal in practice</b>"],
     ["<b>Called once</b>", "<b>Always inline</b>", "<b>No size cost at all</b>"],
     ["Constant arguments", "Strongly favour", "<b>Because of what it enables</b>"],
     ["<b>In a loop</b>", "Favour", "Benefit is multiplied"],
     ["<b>Recursive</b>", "<b>Inline a bounded depth only</b>", "Or not at all"],
     ["Profile says cold", "<b>Do not inline</b>", "<b>Size costs i-cache everywhere</b>"],
   ],
   "footnote": "<b>Code size is a real cost</b>, not just a number — "
               "instruction cache misses are as expensive as the calls you "
               "removed.",
   "note": "The i-cache point is why aggressive inlining can lose."},

  {"t": "section", "label": "Part 4", "title": "Measuring",
   "blurb": "The only way to settle any of this."},

  {"t": "callout", "title": "Measure each pass separately, and report the losses",
   "kind": "The discipline",
   "body": ["<b>Enable one pass at a time against a fixed baseline</b>, "
            "over a benchmark suite that is not three microbenchmarks.",
            "<b>Some passes will lose on some programs.</b> That is "
            "normal, it is information, and hiding it is how compilers "
            "accumulate passes that do nothing.",
            "<b>Report the distribution, not the mean.</b> A pass that "
            "helps 10% on average by helping one benchmark 200% is a "
            "different thing from one that helps everything a little.",
            "<b>And measure code size and compile time too.</b> <b>A 2% "
            "speedup for 40% more compile time is usually a bad trade</b>, "
            "and nobody notices unless it is measured."]},

  {"t": "bullets", "kicker": "Pitfalls", "title": "How optimisation benchmarks lie",
   "items": [
     "<b>Dead code elimination removes the benchmark.</b> Consume the "
     "result or the loop vanishes entirely.",
     "",
     "<b>Constant folding evaluates the whole thing at compile time</b> "
     "if the inputs are literals.",
     "",
     "<b>Code layout changes</b> shift performance by several percent for "
     "reasons unrelated to the pass.",
     "",
     "<b>Three microbenchmarks is not a suite.</b> Passes are tuned to "
     "whatever you measure.",
     "",
     "<b>And compare against <code>-O2</code>, not <code>-O0</code></b> "
     "— CSCE 735's baseline rule, applied here.",
   ],
   "footnote": "<b>The layout effect is large and underappreciated:</b> "
               "aligning a hot loop differently can outweigh the "
               "optimisation you were measuring."},
 ],
 "takeaways": [
   "Individual passes are unimpressive alone; the value is in the cascade "
   "— inlining enables propagation, which enables folding, which "
   "enables elimination.",
   "Loops dominate runtime, so transformations inside them are multiplied "
   "by the trip count, and vectorisation is the largest available win.",
   "No pass ordering is optimal for all programs and finding the optimal "
   "one is intractable, so real pipelines repeat passes.",
   "Inlining is valuable for what it exposes to other passes, not for "
   "removing the call — which is why monomorphisation makes generics "
   "fast.",
   "Code size is a real cost: instruction cache misses can exceed the call "
   "overhead that inlining removed.",
   "Measure each pass separately against -O2, report the distribution and "
   "the losses, and track compile time and code size alongside speed.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The catalogue"),
  ("table", ["Pass", "What it does", "What it needs"],
   [["<b>Constant folding</b>",
     "Evaluate expressions over known constants at compile time.",
     "Nothing. The cheapest possible win, and it runs constantly."],
    ["<b>Constant propagation</b>",
     "<b>Replace a variable by its known constant value at each use.</b>",
     "<b>SSA</b> (Module 07) <b>or reaching definitions</b> (Module 08)."],
    ["<b>Dead code elimination</b>",
     "<b>Delete computations whose results are never used.</b> Iterates, "
     "because deleting one use can make its operands dead.",
     "Liveness, or in SSA simply a use count of zero."],
    ["<b>CSE and global value numbering</b>",
     "<b>Reuse a value already computed rather than recomputing it.</b> GVN "
     "is the SSA-based, stronger form.",
     "Available expressions, or SSA value numbering."],
    ["<b>Copy propagation</b>",
     "Replace uses of a copy with its source, so the copy becomes dead.",
     "SSA. Mostly cleanup after other passes."],
    ["<b>Inlining</b>",
     "<b>Replace a call with the callee's body.</b>",
     "<b>A call graph. The enabling transformation</b> — &sect;3."],
    ["<b>Strength reduction</b>",
     "<b>Replace an expensive operation with a cheaper equivalent</b> "
     "— a multiply by an induction variable becomes a running "
     "addition.",
     "Loop structure and induction variable recognition."],
    ["<b>Loop-invariant code motion</b>",
     "<b>Hoist computations that do not change out of the loop.</b>",
     "<b>Loop structure plus dominance</b> — the hoisted code must "
     "execute on every path that the loop body did."]],
   [0.22, 0.42, 0.36]),
  ("p", "<b>These interact, and the interaction is the whole point.</b> "
        "Inlining substitutes a constant argument, which lets constant "
        "propagation fire, which makes a branch condition constant, which "
        "lets the branch fold, which makes half the body unreachable, which "
        "dead code elimination removes — and the smaller remaining "
        "function may now itself be worth inlining somewhere else. "
        "<b>Individually these passes are unimpressive; the cascade is what "
        "produces the difference between -O0 and -O2.</b>"),
  ("callout", "Loops are where the time is",
   ["<b>Programs spend nearly all their time in loops</b> (CSCE 735 "
    "Module 07), so any transformation applied inside a loop is multiplied "
    "by the trip count. A one-instruction saving in a loop running a "
    "million times is a million instructions.",
    "<b>Loop-invariant code motion</b> hoists computations whose operands "
    "do not change within the loop — one evaluation instead of n. "
    "<b>The subtlety is that the hoisted code must be guaranteed to "
    "execute</b>, or you have introduced a computation (and possibly a "
    "fault) that the original program would not have performed.",
    "<b>Strength reduction</b> replaces an expensive operation with a "
    "cheaper one: an address computation <code>base + i*4</code> becomes a "
    "pointer incremented by 4 each iteration, turning a multiply into an "
    "add.",
    "<b>Unrolling amortises the loop overhead</b> — the increment, the "
    "compare, the branch — over several iterations, and exposes "
    "instruction-level parallelism for the out-of-order engine to exploit "
    "(CSCE 614). <b>Vectorisation then uses the SIMD units</b> "
    "(CSCE 735 Module 02), and when it applies it is the single largest "
    "win available — 4&times; to 16&times; on the arithmetic — "
    "which is why so much compiler engineering goes into making it apply."]),

  ("h1", "2 &nbsp; Phase ordering"),
  ("callout", "Passes enable and disable each other",
   ["<b>Running pass A before pass B can expose opportunities for B, or "
    "destroy them.</b> There is no general rule, and the effect is "
    "program-dependent.",
    "<b>Inlining before constant propagation</b> lets the caller's constant "
    "arguments become constants inside the body. <b>Running it after</b> "
    "misses that entirely — and it is the single most valuable "
    "interaction in the whole pipeline.",
    "<b>But inlining increases code size</b>, which can degrade "
    "instruction cache behaviour and make the program <i>slower</i> "
    "(CSCE 614) — so even a pass that is clearly beneficial in "
    "isolation has a cost that only shows up in interaction with the "
    "hardware.",
    "<b>There is no ordering optimal for all programs, and finding the "
    "optimal ordering for a single given program is intractable</b> "
    "— the space is the permutations of dozens of passes with "
    "repetition allowed. <b>So real compilers use a hand-tuned sequence "
    "with passes repeated</b>, arrived at empirically over years and "
    "defended by benchmark suites rather than by argument."]),
  ("code", """LLVM -O2, heavily abridged:

    SROA                (memory -> SSA registers; FIRST, because
                         everything downstream needs SSA values)
    early CSE
    simplify CFG
    instcombine         (peephole over IR)
    inline              (the enabler)
    SROA again          (inlining exposed more)
    instcombine again
    jump threading
    LICM
    loop unroll / vectorise
    GVN
    dead store elimination
    simplify CFG again

SROA, instcombine and simplify-CFG each appear SEVERAL times.
The repetition is the admission that ordering has no clean answer.

Run `opt -print-after-all` once and read the whole thing."""),

  ("break",),
  ("h1", "3 &nbsp; Inlining"),
  ("callout", "Inlining is valuable for what it enables",
   ["<b>Removing the call overhead is the minor benefit.</b> A direct call "
    "on a modern machine is a handful of cycles, perfectly predicted, and "
    "overlapped with other work. If that were all inlining bought, it would "
    "be a marginal pass.",
    "<b>The real value is that it makes the callee's body visible to every "
    "other optimisation, with the caller's actual arguments "
    "substituted.</b> The body stops being an opaque call and becomes "
    "ordinary code in context.",
    "<b>So a constant argument becomes a constant inside the body</b>, a "
    "branch on it folds away, half the body becomes unreachable and is "
    "deleted, loop bounds may become known, and the much smaller remainder "
    "may be worth inlining further up the chain.",
    "<b>Inlining is the transformation that unlocks the others</b>, and "
    "this explains several things at once: why C++ templates and Rust "
    "generics are fast (<b>monomorphisation is inlining with the types "
    "substituted too</b>, so the generic code specialises completely), why "
    "virtual calls are expensive beyond their direct cost (they cannot be "
    "inlined without devirtualisation), and why link-time optimisation "
    "exists (it extends inlining across translation units)."]),
  ("table", ["Signal", "Effect on the decision", "Note"],
   [["<b>Callee size</b>", "<b>Small bodies are inlined.</b>",
     "<b>The dominant signal in every real heuristic</b>, usually measured "
     "in IR instructions after a cheap simplification."],
    ["<b>Called exactly once</b>", "<b>Always inline.</b>",
     "<b>There is no size cost</b> — the original is deleted "
     "afterwards. Free."],
    ["<b>Constant arguments at the call site</b>", "Strongly favour.",
     "<b>Precisely because of what it enables</b>, per the callout above. "
     "LLVM estimates the simplification that would result."],
    ["<b>Call site is inside a loop</b>", "Favour.",
     "The benefit is multiplied by the trip count (&sect;1)."],
    ["<b>Recursive</b>",
     "<b>Inline to a bounded depth, or not at all.</b>",
     "Unbounded recursive inlining does not terminate."],
    ["<b>Profile says the call site is cold</b>", "<b>Do not inline.</b>",
     "<b>Code size costs instruction cache everywhere</b>, including in the "
     "hot code that has nothing to do with this call. <b>The cost is "
     "non-local, which is what makes this hard.</b>"]],
   [0.22, 0.32, 0.46]),

  ("h1", "4 &nbsp; Measuring"),
  ("callout", "Measure each pass separately, and report the losses",
   ["<b>Enable one pass at a time against a fixed baseline</b>, over a "
    "benchmark suite with real programs in it — not three "
    "microbenchmarks that happen to be in the repository.",
    "<b>Some passes will lose on some programs.</b> That is normal and it "
    "is information. <b>Hiding it is how compilers accumulate passes that "
    "do nothing</b> — a pass added for one benchmark in 2009, never "
    "re-measured, still running on every compile.",
    "<b>Report the distribution rather than the mean</b> (CSCE 735 "
    "Module 07). A pass that improves the average by 10% because it "
    "improves one benchmark by 200% and nothing else is a completely "
    "different thing from one that improves everything by 10%, and the "
    "mean cannot distinguish them.",
    "<b>And measure code size and compile time alongside speed.</b> <b>A "
    "2% speedup bought with 40% more compile time is usually a bad "
    "trade</b> — compile time is developer time, multiplied by every "
    "build — and nobody notices unless it is measured deliberately."]),
  ("ul", ["<b>Dead code elimination removes the benchmark.</b> If nothing "
          "consumes the result, the entire loop is deleted and you measure "
          "an empty function. Consume the result, or use a compiler barrier.",
          "<b>Constant folding evaluates the whole computation at compile "
          "time</b> if the inputs are literals, and you measure a return "
          "statement. Read the inputs from somewhere opaque.",
          "<b>Code layout changes shift performance by several percent</b> "
          "for reasons entirely unrelated to the pass being measured "
          "— a hot loop crossing a cache line boundary differently, or "
          "an alignment change. <b>This effect is large, "
          "underappreciated, and can exceed the optimisation you are "
          "measuring</b>; the published work on it (Mytkowicz et al.) "
          "showed link order alone moving results by more than the "
          "optimisations under study.",
          "<b>Three microbenchmarks is not a suite.</b> Passes get tuned to "
          "whatever is measured, so a small suite produces a compiler that "
          "is good at that suite.",
          "<b>And compare against <code>-O2</code>, never against "
          "<code>-O0</code></b> — CSCE 735 Module 07's optimised "
          "baseline rule, applied here. A speedup over unoptimised code is "
          "not a result."]),
 ],
 "resources": [
   ("Cooper & Torczon &mdash; Engineering a Compiler, chapters 8 and 10",
    "https://www.elsevier.com/books/engineering-a-compiler/cooper/978-0-12-815412-0",
    "The catalogue of &sect;1 with the correctness conditions for each "
    "transformation stated."),
   ("LLVM &mdash; passes documentation, and <code>opt "
    "-print-after-all</code> (free)",
    "https://llvm.org/docs/Passes.html",
    "<b>Run it on your own code this week.</b> Watching the IR change pass "
    "by pass is worth more than any description of the passes."),
   ("Chandler Carruth &mdash; talks on LLVM optimisation and benchmarking "
    "(free)",
    "https://www.youtube.com/results?search_query=chandler+carruth+llvm",
    "<b>Particularly the benchmarking material of &sect;4</b>, including "
    "how microbenchmarks mislead and what to do instead."),
   ("Mytkowicz, Diwan, Hauswirth & Sweeney &mdash; Producing Wrong Data "
    "Without Doing Anything Obviously Wrong (free)",
    "https://dl.acm.org/doi/10.1145/1508284.1508275",
    "<b>The code layout effect of &sect;4</b>, measured. Link order and "
    "environment size alone moved results more than the optimisations being "
    "studied."),
 ],
 "exercises": [
   "Implement constant folding, constant propagation, and dead code "
   "elimination over your SSA IR.",
   "Implement global value numbering and measure how many redundant "
   "computations it removes.",
   "Implement LICM. <b>Construct a case where naive hoisting introduces a "
   "fault</b> the original program would not have had.",
   "Implement inlining with a size-based heuristic.",
   "<b>Demonstrate the cascade:</b> show a function where inlining alone "
   "does little but inlining followed by three other passes transforms it.",
   "<b>Run your passes in two different orders</b> and measure the "
   "difference on each benchmark.",
   "Run <code>opt -print-after-all</code> on a C file and identify five "
   "transformations in the output.",
   "<b>Measure each of your passes separately</b> and produce the table, "
   "including the negative results.",
   "<b>Write a benchmark that dead code elimination deletes</b>, observe "
   "the impossible result, then fix the benchmark.",
   "Measure compile time and code size alongside speed, and find a pass "
   "whose trade is bad.",
 ],
 "selfcheck": [
   "Name eight optimisations and what each requires.",
   "Describe the cascade and give an example chain.",
   "Why do loops get their own category of optimisation?",
   "State the phase-ordering problem and how real compilers respond.",
   "Why is inlining valuable, and what does that explain about generics?",
   "Give six inlining signals and say why code size is a real cost.",
   "How should a pass be measured and reported?",
   "Name five ways optimisation benchmarks lie.",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Code Generation",
 "subtitle": "From IR to instructions the machine actually has.",
 "question": "How do you choose instructions, and in what order?",
 "outcomes": [
     "Explain instruction selection as tree tiling.",
     "Apply dynamic programming to select optimally over a tree.",
     "Explain list scheduling and what it is scheduling for.",
     "Explain calling conventions and why they are a contract.",
     "Explain what debug information must survive optimisation.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Instruction selection",
   "blurb": "Covering the IR with machine instructions."},

  {"t": "code", "kicker": "Tiling", "title": "Selection as tree covering",
   "lang": "text", "code": """
  The IR is a tree (or DAG). Each machine instruction is a TILE --
  a small tree pattern it can implement, with a cost.

  IR for   a[i] = x + 1     (a is a base pointer, i an index)

            store
            /    \\
         add      add
        /   \\    /   \\
       a   mul   x    1
          /   \\
         i     4

  TILES AVAILABLE on x86-64:
      add r, r              cost 1
      lea r, [r + r*4]      cost 1   <- covers THREE IR nodes
      mov [r + r*4], r      cost 1   <- covers FOUR
      imul r, imm           cost 3

  A naive one-node-per-instruction covering: 5 instructions.
  A good covering using the addressing mode: 2 instructions.

  So selection is: COVER THE TREE WITH TILES AT MINIMUM COST.
  Optimal over a TREE by dynamic programming, bottom-up, in
  linear time. NP-hard over a DAG -- so real compilers split
  DAGs into trees, or use heuristics.
""",
   "caption": "<b>x86 addressing modes are why this matters</b> — one "
              "instruction can absorb a multiply, two adds, and a memory "
              "access.",
   "note": "The lea example makes the value of good selection concrete."},

  {"t": "callout", "title": "Optimal on trees, intractable on graphs",
   "kind": "The complexity boundary",
   "body": ["<b>Over a tree, dynamic programming gives the optimal "
            "cover</b> in linear time: compute the best cost for each "
            "node bottom-up, then walk down choosing.",
            "<b>Over a DAG it is NP-hard</b>, because a shared subtree may "
            "want different tiles for its different parents.",
            "<b>Real IR is a DAG</b> — common subexpressions are shared "
            "by construction, especially after CSE.",
            "<b>So compilers split the DAG into trees and accept "
            "suboptimality</b>, or use heuristics, or use generated "
            "matchers. <b>LLVM's SelectionDAG does the first; its "
            "GlobalISel is a different bet.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Scheduling",
   "blurb": "Ordering for the pipeline."},

  {"t": "callout", "title": "Scheduling hides latency the hardware cannot",
   "kind": "What it is for",
   "body": ["<b>Instructions have latencies</b> — a load may take four "
            "cycles, a divide twenty. A dependent instruction must wait.",
            "<b>So reorder to put independent work between a producer and "
            "its consumer.</b> List scheduling does this greedily over the "
            "dependence DAG.",
            "<b>The priority is usually the critical path length</b> "
            "— schedule first whatever has the most work depending on "
            "it.",
            "<b>Out-of-order hardware already does this</b> (CSCE 614), "
            "which makes scheduling far less critical on big cores — and "
            "<b>still essential on in-order cores, VLIW, and GPUs</b>, "
            "which is most of the hardware in the world by count."]},

  {"t": "callout", "title": "Scheduling and register allocation fight",
   "kind": "The phase-ordering problem, concretely",
   "body": ["<b>Scheduling wants to spread computations apart</b> to hide "
            "latency — which lengthens live ranges.",
            "<b>Register allocation wants live ranges short</b>, so that "
            "fewer values are live at once and nothing spills.",
            "<b>So scheduling before allocation causes spills; allocating "
            "first constrains scheduling</b> with false dependences through "
            "reused registers.",
            "<b>The usual answer is to schedule, allocate, then schedule "
            "again</b> — which is a hack, is the standard practice, and is "
            "Module 09's phase-ordering problem in its most concrete "
            "form."]},

  {"t": "section", "label": "Part 3", "title": "Calling conventions",
   "blurb": "A contract that cannot be broken unilaterally."},

  {"t": "table", "kicker": "ABI", "title": "What a calling convention fixes",
   "header": ["Decision", "Example (System V x86-64)"],
   "widths": [4.2, 7.9],
   "rows": [
     ["<b>Argument registers, in order</b>", "<b>rdi, rsi, rdx, rcx, r8, r9; then the stack</b>"],
     ["<b>Return register</b>", "rax; rdx:rax for 128-bit"],
     ["<b>Caller-saved</b>", "<b>rax, rcx, rdx, rsi, rdi, r8–r11</b>"],
     ["<b>Callee-saved</b>", "<b>rbx, rbp, r12–r15 — must be restored</b>"],
     ["Stack alignment", "<b>16 bytes at the call instruction</b>"],
     ["<b>Struct passing</b>", "<b>By field class; the subtle part</b>"],
     ["Varargs", "al holds the vector register count"],
   ],
   "footnote": "<b>This is a contract between separately compiled code</b>, "
               "so it cannot be changed unilaterally — which is why "
               "ABIs outlive the hardware they were designed for.",
   "note": "Struct passing rules are where real ABI bugs live."},

  {"t": "callout", "title": "The ABI is why you cannot just change things",
   "kind": "Why this is a module and not a footnote",
   "body": ["<b>Separately compiled code must agree</b> — your compiler, "
            "the system libraries, and the operating system were built at "
            "different times by different people.",
            "<b>So a better convention cannot be adopted unilaterally.</b> "
            "Everything must change together, which in practice means "
            "nothing changes.",
            "<b>Which is why ABIs long outlive their hardware</b>, and why "
            "x86-64 still passes the first six integer arguments in "
            "registers chosen in 2000.",
            "<b>And it is why C is the universal interop layer</b> — not "
            "because the language is good for it, but because <b>the C ABI "
            "is the one everyone already implements.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Debug information",
   "blurb": "What has to survive all of this."},

  {"t": "callout", "title": "Optimisation destroys the correspondence to source",
   "kind": "The fundamental tension",
   "body": ["<b>A debugger needs to map a machine address to a source "
            "line, and a variable name to a location.</b>",
            "<b>Optimisation breaks both.</b> Instructions are reordered "
            "across lines, variables live in different registers at "
            "different points or are eliminated entirely, and inlined code "
            "comes from another file.",
            "<b>DWARF encodes this as location <i>lists</i></b> — a "
            "variable's location as a function of the program counter, "
            "plus inlining records.",
            "<b>'Optimised out' is the honest answer</b> when a variable "
            "genuinely does not exist at that point. <b>Carrying debug "
            "info correctly through every pass is substantial ongoing work "
            "that is easy to get silently wrong.</b>"]},

  {"t": "bullets", "kicker": "Rules", "title": "Debug info rules for a pass author",
   "items": [
     "<b>Preserve source locations</b> when moving an instruction; do not "
     "invent one.",
     "",
     "<b>Drop a location rather than attach a wrong one.</b> A wrong line "
     "number is worse than none.",
     "",
     "<b>Record inlining</b> — the inlined-at chain, so a stack trace can "
     "be reconstructed.",
     "",
     "<b>Never let debug info change codegen.</b> "
     "<code>-g</code> must not alter the generated instructions, or "
     "debugging changes the bug.",
     "",
     "<b>And test it</b> — debug info has no runtime behaviour, so "
     "nothing fails when it rots.",
   ],
   "footnote": "<b>The last point is why debug quality degrades "
               "silently</b> across compiler versions unless it is "
               "explicitly tested."},
 ],
 "takeaways": [
   "Instruction selection is covering the IR with machine instruction "
   "tiles at minimum cost; x86 addressing modes let one instruction absorb "
   "several IR nodes.",
   "Optimal tiling is linear-time dynamic programming over a tree and "
   "NP-hard over a DAG, so compilers split DAGs into trees.",
   "Scheduling hides latency by placing independent work between producer "
   "and consumer, and matters most on in-order cores, VLIW, and GPUs.",
   "Scheduling and register allocation have directly opposed goals, which "
   "is the phase-ordering problem in its most concrete form.",
   "A calling convention is a contract between separately compiled code, so "
   "it cannot change unilaterally — which is why ABIs outlive their "
   "hardware and why C is the interop layer.",
   "Optimisation destroys the source correspondence, so DWARF uses location "
   "lists, and debug info rots silently because nothing fails when it is "
   "wrong.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Instruction selection"),
  ("code", """IR for   a[i] = x + 1

          store
          /    \\
       add      add
      /   \\    /   \\
     a   mul   x    1
        /   \\
       i     4

TILES on x86-64:
    add  r, r              cost 1
    lea  r, [r + r*4]      cost 1   <- covers THREE IR nodes
    mov  [r + r*4], r      cost 1   <- covers FOUR
    imul r, imm            cost 3

Naive one-node-per-instruction:  5 instructions.
Good covering using addressing modes:  2 instructions.

Selection = COVER THE TREE WITH TILES AT MINIMUM COST."""),
  ("callout", "Optimal on trees, intractable on graphs",
   ["<b>Over a tree, dynamic programming produces the provably optimal "
    "cover in linear time.</b> Compute, bottom-up, the minimum cost to "
    "produce each node's value in each possible storage class; then walk "
    "back down selecting the tiles that achieved it. This is a clean and "
    "satisfying result.",
    "<b>Over a DAG the problem is NP-hard</b>, because a shared subtree may "
    "want to be covered by different tiles on behalf of its different "
    "parents, and the choices interact.",
    "<b>And real IR is a DAG.</b> Common subexpressions are shared by "
    "construction, and CSE and GVN (Module 09) deliberately create more "
    "sharing — so the easy case is exactly the one that does not "
    "occur.",
    "<b>So compilers split the DAG into trees at the shared nodes and "
    "accept suboptimality</b>, or use heuristic matchers, or generate a "
    "matcher from a machine description. <b>LLVM's SelectionDAG does "
    "roughly the first; GlobalISel is a different and ongoing bet</b> on a "
    "more incremental approach. That a production compiler is still "
    "replacing its instruction selector after twenty years is a reasonable "
    "indication of how unsettled this area is."]),

  ("h1", "2 &nbsp; Scheduling"),
  ("callout", "Scheduling hides latency the hardware cannot",
   ["<b>Instructions have latencies.</b> A load from L1 takes several "
    "cycles, from memory hundreds (CSCE 614); a divide takes tens. An "
    "instruction that consumes a result must wait for it.",
    "<b>So reorder to place independent work between a producer and its "
    "consumer.</b> <b>List scheduling</b> does this greedily: build the "
    "dependence DAG, repeatedly pick a ready instruction by some priority, "
    "and emit it.",
    "<b>The priority is usually critical path length</b> — schedule "
    "first whatever has the most dependent work behind it, since delaying "
    "it delays everything.",
    "<b>Out-of-order hardware already does this at runtime</b> "
    "(CSCE 614), which makes compile-time scheduling far less critical on "
    "large desktop and server cores — and <b>it remains essential on "
    "in-order cores, on VLIW machines where the compiler must fill the "
    "issue slots explicitly, and on GPUs</b> (CSCE 735 Module 08). "
    "<b>That is most of the processors in the world by count</b>, so "
    "scheduling has not become irrelevant; it has become "
    "target-dependent."]),
  ("callout", "Scheduling and register allocation have opposed goals",
   ["<b>Scheduling wants to spread dependent computations apart</b> so that "
    "independent work fills the latency — which necessarily lengthens "
    "the live ranges of the values involved.",
    "<b>Register allocation wants live ranges short</b>, so that fewer "
    "values are simultaneously live and the allocation fits the register "
    "file without spilling (Module 11).",
    "<b>So scheduling before allocation produces spills</b> that the "
    "scheduler's improvement does not pay for, while <b>allocating before "
    "scheduling constrains the scheduler</b> with false dependences through "
    "reused physical registers that were not in the original program at "
    "all.",
    "<b>The usual answer is to schedule, allocate, then schedule again</b> "
    "— a pre-pass scheduler, the allocator, and a post-pass scheduler "
    "to clean up. <b>It is a hack, it is standard practice in every "
    "production compiler, and it is Module 09's phase-ordering problem in "
    "its most concrete and least deniable form</b>: two phases whose "
    "optimal choices genuinely depend on each other, resolved by running "
    "one of them twice."]),

  ("break",),
  ("h1", "3 &nbsp; Calling conventions"),
  ("table", ["Decision", "System V AMD64 (Linux, macOS, BSD)"],
   [["<b>Integer argument registers, in order</b>",
     "<b>rdi, rsi, rdx, rcx, r8, r9</b>, then the stack right to left."],
    ["<b>Floating-point arguments</b>", "xmm0 through xmm7."],
    ["<b>Return value</b>",
     "rax; rdx:rax for 128-bit; xmm0 for floating point."],
    ["<b>Caller-saved (volatile)</b>",
     "<b>rax, rcx, rdx, rsi, rdi, r8–r11.</b> The caller must save "
     "these if it needs them across a call."],
    ["<b>Callee-saved (non-volatile)</b>",
     "<b>rbx, rbp, r12–r15.</b> The callee must restore them before "
     "returning — which interacts directly with register allocation "
     "(Module 11)."],
    ["<b>Stack alignment</b>",
     "<b>16 bytes at the point of the <code>call</code></b>, which means "
     "the callee sees the return address making it 8 mod 16. Getting this "
     "wrong produces crashes only in functions using aligned SIMD."],
    ["<b>Struct passing</b>",
     "<b>By classifying each eightbyte of the struct</b> as INTEGER, SSE, "
     "or MEMORY, with aggregates over 16 bytes passed in memory. <b>The "
     "subtle part, and where real ABI bugs live.</b>"],
    ["<b>Variadic functions</b>",
     "al must hold the number of vector registers used — an obscure "
     "rule that breaks <code>printf</code> when violated."]],
   [0.29, 0.71]),
  ("callout", "The ABI is why you cannot just change things",
   ["<b>Separately compiled code must agree on all of it.</b> Your "
    "compiler, the system C library, the operating system's syscall stubs, "
    "and every third-party binary were built at different times by "
    "different people and must interoperate exactly.",
    "<b>So a better calling convention cannot be adopted "
    "unilaterally.</b> Everything would have to change together, which in "
    "practice means nothing changes — the coordination cost exceeds "
    "any plausible benefit.",
    "<b>Which is why ABIs long outlive the hardware they were designed "
    "for.</b> The System V AMD64 register assignment was fixed around 2000 "
    "and is still what every Linux binary uses, on processors with "
    "completely different microarchitectural characteristics.",
    "<b>And it is why C is the universal interoperability layer.</b> Not "
    "because C is a good language for describing interfaces — it is "
    "not, having no modules, no ownership, and a weak type system — "
    "but because <b>the C ABI is the one that every language and every "
    "platform already implements.</b> Rust, Python, Go, and Swift all speak "
    "to each other in C, through a convention none of them would have "
    "chosen."]),

  ("h1", "4 &nbsp; Debug information"),
  ("callout", "Optimisation destroys the correspondence to source",
   ["<b>A debugger needs two mappings:</b> machine address to source line, "
    "and variable name to storage location. Both are straightforward in "
    "unoptimised code and both are destroyed by optimisation.",
    "<b>Instructions are reordered across source lines</b> (&sect;2), so "
    "stepping jumps backwards and forwards. <b>A variable lives in "
    "different registers at different points</b>, or in a register for part "
    "of its life and memory for another, or <b>is eliminated "
    "entirely</b>. <b>Inlined code comes from a different function and a "
    "different file</b>, so one address belongs to several source "
    "locations at once.",
    "<b>DWARF handles this with location <i>lists</i></b> — a "
    "variable's location expressed as a function of the program counter, "
    "rather than a single answer — plus explicit inlining records "
    "giving the inlined-at chain so a stack trace can be reconstructed.",
    "<b>'Optimised out' is the honest answer</b> when a variable genuinely "
    "has no storage at that point, and a debugger saying so is behaving "
    "correctly. <b>Carrying debug information accurately through every "
    "optimisation pass is substantial ongoing engineering work</b>, and it "
    "is easy to get silently wrong."]),
  ("ul", ["<b>Preserve the source location when moving an instruction</b>, "
          "and do not invent one for an instruction you created.",
          "<b>Drop a location rather than attach a plausible-looking wrong "
          "one.</b> A debugger that stops on the wrong line actively misleads; "
          "one that says it does not know is merely unhelpful.",
          "<b>Record inlining explicitly</b> — the inlined-at chain "
          "— so that a stack trace through inlined frames can be "
          "reconstructed. Without it, inlining makes profiles and crash "
          "reports unattributable.",
          "<b>Never let debug information change code generation.</b> "
          "Compiling with <code>-g</code> must produce byte-identical code "
          "to compiling without it. <b>If it does not, then debugging "
          "changes the bug</b>, which is the worst possible property for a "
          "debugging aid.",
          "<b>And test it.</b> <b>Debug information has no runtime "
          "behaviour, so nothing fails when it rots</b> — no test goes "
          "red, no benchmark regresses, and the quality degrades silently "
          "across releases until someone tries to debug an optimised build "
          "and finds every variable optimised out. This is why projects "
          "that care about it run dedicated debug-info test suites."]),
 ],
 "resources": [
   ("Appel &mdash; Modern Compiler Implementation, chapter 9 (instruction "
    "selection)",
    "https://www.cs.princeton.edu/~appel/modern/",
    "<b>Tree tiling and the dynamic programming algorithm of &sect;1</b>, "
    "presented clearly."),
   ("System V AMD64 ABI specification (free)",
     "https://gitlab.com/x86-psABIs/x86-64-ABI",
    "<b>The &sect;3 contract, normatively.</b> The struct classification "
    "section is the one worth reading carefully."),
   ("Cooper & Torczon &mdash; Engineering a Compiler, chapters 11 and 12",
    "https://www.elsevier.com/books/engineering-a-compiler/cooper/978-0-12-815412-0",
    "Selection and scheduling, with the DAG complexity result."),
   ("DWARF Debugging Standard (free)",
    "https://dwarfstd.org/",
    "Location lists and inlining records — the &sect;4 mechanism. "
    "Dense; read the introduction and the location-list chapter."),
 ],
 "exercises": [
   "Implement tree tiling with dynamic programming for a small "
   "instruction set.",
   "<b>Add x86 addressing-mode tiles</b> and measure the reduction in "
   "instruction count.",
   "Construct a DAG where tree splitting produces a suboptimal cover, and "
   "quantify the loss.",
   "Implement list scheduling with critical-path priority.",
   "<b>Measure scheduling's effect on an in-order target</b> and on an "
   "out-of-order one, and explain the difference.",
   "<b>Demonstrate the scheduling/allocation conflict:</b> schedule "
   "aggressively, then allocate, and count the spills.",
   "Implement the System V calling convention and call into C from your "
   "generated code.",
   "<b>Deliberately violate the stack alignment rule</b> and find a "
   "function that crashes because of it.",
   "Emit DWARF line information and step through your generated code in "
   "gdb.",
   "<b>Optimise a function and observe which variables become 'optimised "
   "out'.</b> Verify that <code>-g</code> did not change the code.",
 ],
 "selfcheck": [
   "Describe instruction selection as tiling and say why addressing modes "
   "matter.",
   "Why is tiling optimal on trees and NP-hard on DAGs, and why does that "
   "matter?",
   "What is scheduling for, and on which targets does it matter most?",
   "Why do scheduling and register allocation conflict, and how is it "
   "resolved?",
   "Name six things a calling convention fixes.",
   "Why can an ABI not be changed unilaterally, and what follows?",
   "How does optimisation break debugging, and what does DWARF do about "
   "it?",
   "Give five debug-info rules for a pass author.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Register Allocation",
 "subtitle": "Infinitely many values, sixteen registers.",
 "question": "Which values live in registers, and which spill?",
 "outcomes": [
     "Build an interference graph from liveness.",
     "Explain graph colouring allocation and Chaitin–Briggs.",
     "Implement linear scan and say when it is the right choice.",
     "Explain spilling, rematerialisation, and coalescing.",
     "Explain why SSA makes the problem easier.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The reduction",
   "blurb": "Allocation is graph colouring."},

  {"t": "callout", "title": "Interference, and the colouring reduction",
   "kind": "The classical formulation",
   "body": ["<b>Two values <i>interfere</i> if they are live at the same "
            "time</b>, so they cannot share a register.",
            "<b>Build a graph: a node per value, an edge per "
            "interference.</b> Liveness (Module 08) gives you exactly "
            "this.",
            "<b>Then assigning registers is colouring the graph with k "
            "colours</b>, where k is the number of registers.",
            "<b>Graph colouring is NP-complete</b>, and Chaitin's 1981 "
            "result showed every graph arises from some program — so the "
            "hardness is real, not an artifact. <b>Hence heuristics.</b>"]},

  {"t": "code", "kicker": "Chaitin–Briggs", "title": "Simplify, spill, select",
   "lang": "text", "code": """
  BUILD      interference graph from liveness
  COALESCE   merge copy-related nodes if it does not raise degree
             (conservative coalescing -- Briggs' contribution)
  SIMPLIFY   repeatedly remove any node with degree < k and push
             it on a stack.  Such a node is ALWAYS colourable:
             its neighbours use at most k-1 colours.
  SPILL      if every remaining node has degree >= k, pick one to
             spill by a cost heuristic and push it OPTIMISTICALLY
  SELECT     pop the stack, assigning each node a colour its
             neighbours do not use.  An optimistically pushed node
             may still find a colour -- its neighbours may share.
             If not, actually spill it and restart.

  CHAITIN spilled immediately on degree >= k.
  BRIGGS pushes optimistically and often finds a colour anyway.
  That one change is a large practical improvement.
""",
   "caption": "<b>Briggs' optimistic colouring is the difference</b> "
              "between the textbook algorithm and the one worth "
              "implementing.",
   "note": "The degree < k argument is the core insight; make sure it "
           "lands."},

  {"t": "section", "label": "Part 2", "title": "Spilling",
   "blurb": "When it does not fit."},

  {"t": "callout", "title": "Choose what to spill by cost, not by convenience",
   "kind": "The heuristic that matters",
   "body": ["<b>Spilling means storing a value to memory and reloading it "
            "at each use</b> — so the cost is the number of accesses, "
            "weighted by loop depth.",
            "<b>The standard metric is (uses + defs, weighted by 10^depth) "
            "divided by degree</b> — cheap to spill, and relieves a lot of "
            "pressure.",
            "<b>Rematerialisation is better when it applies:</b> if the "
            "value is a constant or a simple expression of still-live "
            "values, <b>recompute it instead of reloading</b>.",
            "<b>A constant is always cheaper to rematerialise than to "
            "spill</b>, and compilers that miss this spill constants to the "
            "stack, which is embarrassing and common in student "
            "allocators."]},

  {"t": "callout", "title": "Coalescing removes the copies SSA destruction made",
   "kind": "Why it belongs here",
   "body": ["<b>SSA destruction inserts copies at φ nodes</b> "
            "(Module 07 §4), and copy propagation leaves more.",
            "<b>If a copy's source and destination do not interfere, merge "
            "them</b> — same register, copy deleted.",
            "<b>But merging raises the merged node's degree</b>, which can "
            "make the graph uncolourable and cause a spill. <b>A spill "
            "costs far more than the copy saved.</b>",
            "<b>So coalesce conservatively</b> — Briggs' rule merges only "
            "if the result has fewer than k neighbours of significant "
            "degree. <b>Aggressive coalescing was the original approach and "
            "it was worse.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Linear scan",
   "blurb": "The fast alternative."},

  {"t": "table", "kicker": "Comparison", "title": "Graph colouring against linear scan",
   "header": ["", "Graph colouring", "Linear scan"],
   "widths": [2.6, 4.5, 5.0],
   "rows": [
     ["<b>Model</b>", "Interference graph", "<b>Live intervals on a linear order</b>"],
     ["<b>Cost</b>", "<b>Can be O(n&#178;) or worse</b>", "<b>O(n log n)</b>"],
     ["<b>Quality</b>", "<b>Better — 5–10% fewer spills typically</b>", "Good enough for most code"],
     ["<b>Used by</b>", "<b>GCC, LLVM (-O2+)</b>", "<b>JITs: HotSpot C1, V8 baseline</b>"],
     ["Incremental", "<b>No — rebuild on change</b>", "Easier"],
     ["<b>When</b>", "<b>Compile time is affordable</b>", "<b>Compile time is on the clock</b>"],
   ],
   "footnote": "<b>A JIT compiles while the user waits</b>, so an "
               "allocator that takes 10&times; longer to save 8% of spills "
               "is the wrong trade.",
   "note": "Framing it as a compile-time budget decision is the right "
           "way in."},

  {"t": "callout", "title": "Linear scan: intervals on a line",
   "kind": "The idea",
   "body": ["<b>Linearise the blocks, then give each value a live "
            "<i>interval</i></b> from its first definition to its last "
            "use.",
            "<b>Sweep by start position, maintaining the active "
            "set</b> — intervals overlapping the current point. Expire "
            "those that have ended.",
            "<b>Assign a free register, or spill the interval ending "
            "last</b> among the active ones plus the new one.",
            "<b>The approximation is that an interval is contiguous</b>, "
            "which over-states liveness across holes. <b>Interval splitting "
            "recovers most of the quality</b> and is what production JITs "
            "actually use."]},

  {"t": "section", "label": "Part 4", "title": "SSA",
   "blurb": "A genuinely surprising result."},

  {"t": "callout", "title": "SSA interference graphs are chordal",
   "kind": "Why the NP-hardness goes away",
   "body": ["<b>A chordal graph has no induced cycle longer than "
            "three</b>, and chordal graphs can be optimally coloured in "
            "<i>polynomial</i> time.",
            "<b>The interference graph of a program in SSA form is always "
            "chordal.</b> Live ranges in SSA are subtrees of the dominator "
            "tree, and intersection graphs of subtrees are chordal.",
            "<b>So the colouring that was NP-complete becomes "
            "tractable</b> — and the minimum number of registers needed "
            "equals the maximum number of values live at any point.",
            "<b>Chaitin's hardness result is not contradicted</b>; SSA "
            "simply does not produce the hard graphs. <b>The "
            "representation changed the problem's complexity</b>, which is "
            "Module 07's claim in its strongest form."]},

  {"t": "bullets", "kicker": "Caveat", "title": "Why this did not end the subject",
   "items": [
     "<b>Colouring becomes easy; <i>spilling</i> does not.</b> Deciding "
     "what to spill is still NP-hard, and spilling is where the cost is.",
     "",
     "<b>Destruction still inserts copies</b> (Module 07 §4), and "
     "coalescing them is still hard.",
     "",
     "<b>Register classes and constraints complicate it</b> — some "
     "instructions demand particular registers.",
     "",
     "<b>And callee-saved registers, ABI requirements, and precoloured "
     "nodes</b> all break the clean theory (Module 10 §3).",
     "",
     "<b>So SSA-based allocation is a real improvement, not a "
     "solution.</b>",
   ],
   "footnote": "<b>A good result that does not solve the whole problem is "
               "the normal shape of progress</b>, and worth saying "
               "plainly."},
 ],
 "takeaways": [
   "Two values interfere when simultaneously live; allocation is colouring "
   "the interference graph with k colours, and that is NP-complete in "
   "general.",
   "Chaitin–Briggs simplifies by removing nodes of degree below k, and "
   "Briggs' optimistic pushing is what makes it practical.",
   "Spill by cost per degree, weighted by loop depth — and "
   "rematerialise constants rather than spilling them.",
   "Coalescing must be conservative: a spill costs far more than the copy "
   "it would have saved.",
   "Linear scan is O(n log n) and slightly worse, which is the right trade "
   "when compile time is on the clock — which is why JITs use it.",
   "SSA interference graphs are chordal and therefore optimally colourable "
   "in polynomial time, but spilling and coalescing remain hard.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Allocation as graph colouring"),
  ("callout", "Interference, and the reduction",
   ["<b>Two values <i>interfere</i> if there is any point at which both are "
    "live</b> — if so, they cannot occupy the same register, because "
    "writing one would destroy the other.",
    "<b>Build a graph with a node per value and an edge per interfering "
    "pair.</b> Liveness analysis (Module 08 &sect;2) produces exactly the "
    "information needed, which is why liveness is the analysis no compiler "
    "can do without.",
    "<b>Then assigning registers <i>is</i> colouring that graph with k "
    "colours</b>, where k is the number of available physical registers "
    "— adjacent nodes must get different colours, exactly as "
    "interfering values must get different registers.",
    "<b>Graph colouring is NP-complete</b>, and <b>Chaitin showed in 1981 "
    "that every graph is the interference graph of some program</b> "
    "— so the hardness is genuine and not an artifact of the "
    "reduction. There is no special structure in real programs to exploit "
    "in general. <b>Hence heuristics</b>, and hence the &sect;4 result "
    "being so surprising when it arrived."]),
  ("code", """BUILD      interference graph from liveness
COALESCE   merge copy-related nodes if degree does not rise
SIMPLIFY   repeatedly remove a node of degree < k, push on a stack
           -- such a node is ALWAYS colourable, because its
              neighbours use at most k-1 colours between them
SPILL      if every node has degree >= k, pick one by cost and
           push it OPTIMISTICALLY
SELECT     pop the stack, colouring each node differently from
           its neighbours. An optimistically pushed node may STILL
           find a colour -- its high-degree neighbours may share
           colours. If not, really spill it and restart.

CHAITIN (1981): spill immediately at degree >= k.
BRIGGS  (1989): push optimistically; often a colour exists anyway."""),
  ("p", "<b>The degree-below-k argument is the core insight</b>, and it is "
        "worth stating carefully: a node with fewer than k neighbours can "
        "always be coloured, whatever happens to the rest of the graph, "
        "because its neighbours can collectively use at most k &minus; 1 "
        "colours and one is therefore left over. <b>Briggs' optimistic "
        "pushing is the difference between the textbook algorithm and the "
        "one worth implementing</b> — a node of degree k or more may "
        "still be colourable if several of its neighbours happen to share a "
        "colour, and simply trying costs nothing."),

  ("h1", "2 &nbsp; Spilling and coalescing"),
  ("callout", "Choose what to spill by cost, not by convenience",
   ["<b>Spilling a value means storing it to the stack and reloading it at "
    "each use</b>, so its cost is the number of definitions and uses, "
    "<b>weighted by loop depth</b> — a use inside a doubly nested loop "
    "is worth a hundred outside one.",
    "<b>The standard metric is cost divided by degree:</b> "
    "(uses + defs, each weighted by 10<super>loop depth</super>) / degree. "
    "<b>Spill what is cheap to spill and relieves the most pressure</b>, "
    "which is the right shape for the trade.",
    "<b>Rematerialisation is strictly better where it applies.</b> If the "
    "value is a constant, or a simple expression of values that are still "
    "live, <b>recompute it at each use rather than reloading it</b> "
    "— no store, no stack slot, and the recomputation is often a "
    "single instruction.",
    "<b>A constant is always cheaper to rematerialise than to spill</b>, "
    "and an allocator that misses this spills constants to the stack and "
    "reloads them — <b>which is both embarrassing and extremely "
    "common in hand-written allocators</b>. Check for it explicitly."]),
  ("callout", "Coalescing removes the copies SSA destruction created",
   ["<b>SSA destruction inserts copies at every &phi;</b> (Module 07 "
    "&sect;4), and copy propagation and instruction selection leave more. "
    "A function can easily have more copies than useful instructions after "
    "destruction.",
    "<b>If a copy's source and destination do not interfere, merge their "
    "nodes</b> — they get the same register and the copy is deleted "
    "entirely. This is the main reason naive &phi; destruction is "
    "acceptable.",
    "<b>But merging two nodes produces a node whose degree is the union of "
    "theirs</b>, which can push the graph over the colourability threshold "
    "and force a spill. <b>A spill costs far more than the copy it was "
    "meant to save</b> — a register-to-register move is a cycle or "
    "less on a modern machine, while a spill is a store, a reload, and "
    "possibly a cache miss.",
    "<b>So coalesce conservatively.</b> <b>Briggs' rule</b> merges only if "
    "the resulting node has fewer than k neighbours of significant degree; "
    "<b>George's rule</b> is a different sufficient condition and the two "
    "are usually applied together. <b>Aggressive coalescing — merging "
    "whenever possible — was the original approach and it was measurably "
    "worse</b>, which is a good small example of a locally obvious "
    "optimisation losing globally."]),

  ("break",),
  ("h1", "3 &nbsp; Linear scan"),
  ("table", ["", "Graph colouring", "Linear scan"],
   [["<b>Model</b>", "An interference graph over values.",
     "<b>Live intervals over a linearised instruction order.</b>"],
    ["<b>Cost</b>",
     "<b>Can be O(n&#178;) or worse</b> — graph construction alone is "
     "quadratic in the worst case, and spilling restarts the whole "
     "process.",
     "<b>O(n log n)</b>, dominated by sorting the intervals."],
    ["<b>Quality</b>",
     "<b>Better — typically 5 to 10% fewer spills</b>, more on "
     "register-starved targets.",
     "Good enough for the great majority of code."],
    ["<b>Used by</b>", "<b>GCC and LLVM at -O2 and above.</b>",
     "<b>JIT compilers: HotSpot's C1, V8's baseline tier</b>, and most "
     "first-tier JITs."],
    ["<b>Incremental</b>",
     "<b>No</b> — a change requires rebuilding the graph.",
     "Easier to update."],
    ["<b>When to use it</b>", "<b>When compile time is affordable.</b>",
     "<b>When compile time is on the clock</b> — see below."]],
   [0.16, 0.40, 0.44]),
  ("callout", "Linear scan: intervals on a line",
   ["<b>Linearise the basic blocks into a single instruction order, then "
    "give each value a live <i>interval</i></b> running from its first "
    "definition to its last use in that order.",
    "<b>Sweep through the intervals in order of start position, "
    "maintaining the <i>active</i> set</b> of intervals that overlap the "
    "current point. At each new interval, first expire every active "
    "interval that has already ended and free its register.",
    "<b>Then assign a free register if one exists; otherwise spill</b> "
    "— conventionally the interval among the active set and the new "
    "one that ends <i>last</i>, since it is occupying a register for the "
    "longest.",
    "<b>The approximation is that an interval is contiguous</b>, which "
    "over-states liveness across holes where the value is dead in the "
    "middle of its range — and those holes are common with loops and "
    "branches. <b>Interval splitting recovers most of the lost quality</b> "
    "by allowing a value to occupy different registers, or memory, in "
    "different parts of its range, and <b>that is what production JITs "
    "actually implement</b> rather than the textbook algorithm. "
    "<b>A JIT compiles while the user waits</b>, so an allocator taking "
    "ten times longer to remove 8% of spills is simply the wrong trade."]),

  ("h1", "4 &nbsp; The SSA result"),
  ("callout", "SSA interference graphs are chordal",
   ["<b>A <i>chordal</i> graph is one in which every cycle of four or more "
    "vertices has a chord</b> — equivalently, it has no induced cycle "
    "longer than a triangle. <b>Chordal graphs can be optimally coloured "
    "in polynomial time</b>, by a simple greedy algorithm over a perfect "
    "elimination ordering.",
    "<b>The interference graph of a program in SSA form is always "
    "chordal.</b> The reason is structural: in SSA, each value's live range "
    "is a <i>subtree</i> of the dominator tree, and the intersection graph "
    "of a family of subtrees of a tree is always chordal.",
    "<b>So the colouring problem that Chaitin proved NP-complete becomes "
    "tractable</b> — and better, the minimum number of registers "
    "required equals the maximum number of values simultaneously live at "
    "any program point, which is a quantity you can simply compute.",
    "<b>Chaitin's hardness result is not contradicted.</b> It says every "
    "graph arises from <i>some</i> program; SSA programs simply do not "
    "produce the hard graphs. <b>The representation changed the complexity "
    "of the problem</b> — which is Module 07 &sect;2's claim in its "
    "strongest possible form, and a genuinely striking result: changing how "
    "you write the program down moved a problem from NP-complete to "
    "polynomial."]),
  ("ul", ["<b>Colouring becomes easy; <i>spilling</i> does not.</b> "
          "Deciding which values to spill when the pressure exceeds k is "
          "still NP-hard, and <b>spilling is where essentially all the cost "
          "is</b>. The easy part got easier and the expensive part did not.",
          "<b>Destruction still inserts copies</b> (Module 07 &sect;4), and "
          "coalescing them optimally is still hard — so the copies "
          "that SSA created have to be removed by the machinery of "
          "&sect;2 regardless.",
          "<b>Register classes and instruction constraints complicate "
          "it.</b> Some instructions demand specific registers (x86 shifts "
          "want the count in cl; division uses rdx:rax), and some values "
          "must be in a floating-point class rather than an integer one. "
          "Neither fits the clean colouring model.",
          "<b>And callee-saved registers, ABI requirements, and "
          "precoloured nodes</b> (Module 10 &sect;3) all break the theory "
          "— an argument arriving in rdi is a node whose colour was "
          "decided before allocation began.",
          "<b>So SSA-based register allocation is a real improvement rather "
          "than a solution</b>, and it is used in production (LLVM and "
          "others exploit it) without having ended the subject. <b>A good "
          "result that does not solve the whole problem is the normal shape "
          "of progress</b>, and it is worth saying plainly rather than "
          "overselling the theorem."]),
 ],
 "resources": [
   ("Chaitin &mdash; Register allocation and spilling via graph colouring; "
    "Briggs et al. &mdash; Improvements to graph colouring (free)",
    "https://dl.acm.org/doi/10.1145/989393.989403",
    "<b>The two papers of &sect;1.</b> Briggs' optimistic colouring is the "
    "change worth understanding."),
   ("Poletto & Sarkar &mdash; Linear Scan Register Allocation (free)",
    "https://dl.acm.org/doi/10.1145/330249.330250",
    "<b>The &sect;3 algorithm</b>, from its authors. Short and clear."),
   ("Hack, Grund & Goos &mdash; Register Allocation for Programs in SSA "
    "Form (free)",
    "https://link.springer.com/chapter/10.1007/11688839_20",
    "<b>The chordality result of &sect;4</b>, with the subtree argument."),
   ("Wimmer & Franz &mdash; Linear Scan Register Allocation on SSA Form "
    "(free)",
    "https://dl.acm.org/doi/10.1145/1772954.1772979",
    "Interval splitting and the production JIT version of &sect;3."),
 ],
 "exercises": [
   "Build an interference graph from your liveness analysis and render it.",
   "<b>Implement Chaitin–Briggs</b> with simplify, optimistic spill, "
   "and select.",
   "<b>Disable optimistic pushing</b> (spill immediately at degree k) and "
   "measure the extra spills.",
   "Implement the spill cost heuristic with loop-depth weighting.",
   "<b>Add rematerialisation for constants</b> and measure how many spills "
   "it removes.",
   "Implement conservative coalescing. Then try aggressive coalescing and "
   "measure the resulting spills.",
   "Implement linear scan and compare spill counts and allocation time "
   "against graph colouring on the same functions.",
   "<b>Add interval splitting</b> and measure how much of the gap it "
   "closes.",
   "<b>Verify empirically that your SSA interference graphs are "
   "chordal</b> by testing for a perfect elimination ordering.",
   "Reduce k from 16 to 4 and plot spills against k for both allocators.",
 ],
 "selfcheck": [
   "Define interference and state the colouring reduction.",
   "Why is a node of degree below k always colourable?",
   "What did Briggs change, and why does it help?",
   "Give the spill cost heuristic and say when rematerialisation is "
   "better.",
   "Why must coalescing be conservative?",
   "Compare graph colouring and linear scan on six axes.",
   "What approximation does linear scan make, and what recovers it?",
   "Why are SSA interference graphs chordal, and what follows?",
   "Why did that result not end the subject?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Runtimes: Garbage Collection, JIT, and Scripting",
 "subtitle": "What runs alongside the code you generated.",
 "question": "What does a language need at runtime, and what does it "
             "cost?",
 "outcomes": [
     "Compare garbage collection algorithms on their real trade-offs.",
     "Explain generational collection and the generational "
     "hypothesis.",
     "Explain JIT tiering, deoptimisation, and inline caches.",
     "Design the embedding of a scripting language in an engine.",
     "Explain why GC pauses and frame budgets conflict.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Garbage collection",
   "blurb": "The algorithms, and what they actually trade."},

  {"t": "table", "kicker": "Collectors", "title": "The collection algorithms",
   "header": ["Algorithm", "Mechanism", "Trade"],
   "widths": [2.8, 4.2, 5.1],
   "rows": [
     ["<b>Reference counting</b>", "Count references; free at zero", "<b>Incremental; cycles leak; write cost</b>"],
     ["<b>Mark-sweep</b>", "Trace from roots; free the unmarked", "<b>Handles cycles; fragments; pauses</b>"],
     ["<b>Mark-compact</b>", "Mark, then slide survivors together", "<b>No fragmentation; moves objects</b>"],
     ["<b>Copying (semispace)</b>", "<b>Copy live to a new space</b>", "<b>Allocation is a pointer bump; 2× memory</b>"],
     ["<b>Generational</b>", "<b>Collect young objects often</b>", "<b>The big win. Needs a write barrier</b>"],
     ["Concurrent / incremental", "Collect alongside the program", "<b>Shorter pauses; lower throughput</b>"],
   ],
   "footnote": "<b>Nearly every production collector is generational</b>, "
               "with a copying young generation and a mark-compact old "
               "one.",
   "note": "The copying-allocation-is-a-pointer-bump point surprises "
           "people who assume GC is slow."},

  {"t": "callout", "title": "The generational hypothesis is why GC is affordable",
   "kind": "The empirical fact the design rests on",
   "body": ["<b>Most objects die young.</b> This is observed across almost "
            "every program in almost every language — temporaries, "
            "intermediate results, short-lived closures.",
            "<b>So collect the young generation frequently and "
            "cheaply.</b> A copying collector's cost is proportional to the "
            "<i>survivors</i>, not to the garbage.",
            "<b>If 95% dies, collecting is nearly free</b> — you copy 5% "
            "and reset a pointer.",
            "<b>The cost is a write barrier</b>: every pointer store must "
            "be recorded if it points from old to young. <b>A small tax on "
            "every write, to make collection cheap.</b>"]},

  {"t": "callout", "title": "Allocation in a copying collector is a pointer bump",
   "kind": "Why 'GC is slow' is too simple",
   "body": ["<b>Allocation is: add the size to a pointer, compare against "
            "the limit, return the old value.</b> Three instructions, no "
            "free list, no search.",
            "<b>That is faster than <code>malloc</code></b>, which must "
            "search a size class and manage metadata.",
            "<b>And survivors are copied into contiguous memory</b>, so "
            "related objects become adjacent — a locality benefit "
            "(CSCE 614).",
            "<b>The cost is not throughput; it is <i>pauses</i> and "
            "<i>memory</i>.</b> A GC'd program typically needs 2–5× the "
            "live-set size to perform well. <b>Those are the real "
            "trades.</b>"]},

  {"t": "section", "label": "Part 2", "title": "JIT compilation",
   "blurb": "Compiling with information you did not have."},

  {"t": "callout", "title": "Tiering: start fast, get fast",
   "kind": "The structure of a modern JIT",
   "body": ["<b>Tier 0: interpret.</b> Zero compile time, slow execution. "
            "Most code runs here and never leaves.",
            "<b>Tier 1: compile quickly with minimal optimisation</b>, "
            "while gathering profile data — types seen, branches taken, "
            "call targets.",
            "<b>Tier 2: compile the hot code hard</b>, using the profile "
            "to specialise aggressively.",
            "<b>And deoptimise when an assumption breaks.</b> The "
            "specialised code guards its assumptions; on failure it "
            "transfers control back to the interpreter <i>mid-function</i>, "
            "reconstructing the interpreter's state from the compiled "
            "frame. <b>That reconstruction is the hard part.</b>"]},

  {"t": "callout", "title": "Inline caches: speculating on types",
   "kind": "The technique that makes dynamic languages fast",
   "body": ["<b>In a dynamic language, <code>x.foo</code> requires a "
            "lookup</b> — the object's shape is not known statically.",
            "<b>But at a given site, the shape is usually the same every "
            "time.</b> So cache the result of the lookup, keyed on the "
            "shape.",
            "<b>Monomorphic sites — one shape ever — become a shape "
            "check and a fixed offset load.</b> Nearly as fast as a C "
            "struct field access.",
            "<b>Polymorphic caches hold a few shapes; megamorphic sites "
            "fall back to the full lookup.</b> <b>This single technique is "
            "most of why JavaScript is fast</b>, and it is why consistent "
            "object shapes matter for performance."]},

  {"t": "section", "label": "Part 3", "title": "Scripting in an engine",
   "blurb": "The design decisions that actually come up."},

  {"t": "table", "kicker": "Embedding", "title": "Choosing a scripting language",
   "header": ["Option", "Character", "Cost"],
   "widths": [2.7, 4.4, 5.0],
   "rows": [
     ["<b>Lua / LuaJIT</b>", "<b>Tiny, fast, designed to embed</b>", "<b>Small standard library</b>"],
     ["<b>C# (Mono / IL2CPP)</b>", "Full language and tooling", "<b>Large runtime; GC pauses</b>"],
     ["<b>Visual scripting</b>", "<b>Non-programmers can use it</b>", "<b>Diffs and merges are painful</b>"],
     ["WASM", "Any source language; sandboxed", "Host interop is awkward"],
     ["<b>Custom DSL</b>", "Exactly your domain", "<b>You own tooling forever</b>"],
     ["Native hot-reload", "<b>Full speed</b>", "<b>Crashes take the engine down</b>"],
   ],
   "footnote": "<b>The deciding question is who writes the scripts.</b> "
               "Designers, gameplay programmers, and modders want very "
               "different things.",
   "note": "That the answer is a people question, not a technical one, is "
           "the point."},

  {"t": "callout", "title": "GC pauses and frame budgets are in direct conflict",
   "kind": "The engine's specific problem",
   "body": ["<b>A 60 Hz frame budget is 16.7 ms, and most of it is already "
            "committed.</b> A 10 ms GC pause is a visible hitch; a 50 ms "
            "pause is a stutter everyone notices.",
            "<b>So engines fight the allocator rather than the "
            "collector:</b> pool objects, reuse buffers, avoid allocating "
            "in the per-frame path at all.",
            "<b>Unity's advice is essentially 'do not allocate during "
            "gameplay'</b>, which is a strong signal about where the "
            "problem lies.",
            "<b>Incremental and concurrent collectors trade throughput for "
            "pause time</b>, which is exactly the right trade here — "
            "<b>a frame budget cares about the worst case, not the "
            "mean</b> (CSCE 650 M06)."]},

  {"t": "section", "label": "Part 4", "title": "The interface",
   "blurb": "Where embedding actually goes wrong."},

  {"t": "bullets", "kicker": "Interop", "title": "What makes an embedding painful",
   "items": [
     "<b>Object lifetime across the boundary.</b> The script holds a "
     "reference to a native object the engine then destroys.",
     "",
     "<b>Two garbage collectors, or one GC and manual memory</b>, that "
     "cannot see each other's references — so cycles across the boundary "
     "leak.",
     "",
     "<b>Error propagation.</b> A script error must not crash the engine, "
     "and must still be reported usefully.",
     "",
     "<b>Threading.</b> Most script runtimes are single-threaded; the "
     "engine is not (CSCE 735).",
     "",
     "<b>And call overhead</b> — crossing the boundary per entity per "
     "frame is a real cost. <b>Batch it.</b>",
   ],
   "footnote": "<b>Design the boundary first.</b> It is much harder to "
               "narrow later, and it determines everything else."},
 ],
 "takeaways": [
   "Nearly every production collector is generational, with a copying young "
   "generation and a mark-compact old one.",
   "The generational hypothesis — most objects die young — is "
   "what makes GC affordable, because a copying collector's cost is "
   "proportional to survivors.",
   "Allocation in a copying collector is a pointer bump and is faster than "
   "malloc; the real costs are pause time and 2–5× memory.",
   "A tiered JIT interprets, then compiles cheaply while profiling, then "
   "compiles hot code hard — and deoptimisation must reconstruct "
   "interpreter state mid-function.",
   "Inline caches speculate that a call site sees one object shape, and are "
   "most of why JavaScript is fast.",
   "GC pauses conflict directly with frame budgets, so engines avoid "
   "allocating rather than tuning the collector.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Garbage collection"),
  ("table", ["Algorithm", "Mechanism", "Trade"],
   [["<b>Reference counting</b>",
     "Each object counts its references; freed when the count reaches zero.",
     "<b>Naturally incremental</b> with no pauses, and <b>cycles leak</b> "
     "unless a separate cycle collector runs. <b>Every pointer assignment "
     "costs</b> an increment and a decrement, which is a continuous "
     "throughput tax."],
    ["<b>Mark-sweep</b>",
     "Trace from the roots marking reachable objects, then free everything "
     "unmarked.",
     "<b>Handles cycles</b> correctly. <b>Fragments the heap</b> over time, "
     "and the trace is a pause."],
    ["<b>Mark-compact</b>",
     "Mark, then slide the survivors together to one end.",
     "<b>No fragmentation</b>, at the cost of <b>moving objects</b> "
     "— which means every pointer to them must be updated, so native "
     "code holding raw pointers must be accounted for."],
    ["<b>Copying (semispace)</b>",
     "<b>Copy live objects into a fresh space; the old space is then "
     "entirely free.</b>",
     "<b>Allocation becomes a pointer bump</b> (see below), and it costs "
     "<b>twice the memory</b> since half is always empty."],
    ["<b>Generational</b>",
     "<b>Segregate by age and collect young objects frequently.</b>",
     "<b>The single largest practical win</b>, and it <b>requires a write "
     "barrier</b> — see the callout."],
    ["<b>Concurrent / incremental</b>",
     "Collect alongside the running program, in small steps or on another "
     "thread.",
     "<b>Much shorter pauses, somewhat lower total throughput</b>, and "
     "considerably more implementation complexity."]],
   [0.19, 0.36, 0.45]),
  ("callout", "The generational hypothesis is why GC is affordable",
   ["<b>Most objects die young.</b> This is an empirical observation that "
    "holds across almost every program in almost every language — "
    "temporaries, intermediate results, short-lived closures, and iteration "
    "state vastly outnumber long-lived data.",
    "<b>So collect the young generation frequently and cheaply.</b> The "
    "key property is that <b>a copying collector's cost is proportional to "
    "the <i>survivors</i>, not to the garbage</b> — dead objects are "
    "never touched at all.",
    "<b>If 95% of the young generation is dead, a collection copies 5% and "
    "resets a pointer.</b> It is close to free, and it can therefore be run "
    "often enough that the young generation stays small and cache-resident.",
    "<b>The cost is a write barrier.</b> Because a young object may be "
    "referenced only from an old one, every pointer store must be checked "
    "and recorded if it creates an old-to-young reference, so the young "
    "collection knows its full root set without scanning the old "
    "generation. <b>A small tax on every pointer write, paid to make "
    "collection cheap</b> — and it is a trade that has won decisively, "
    "which is why essentially every production collector is generational."]),
  ("callout", "Allocation in a copying collector is a pointer bump",
   ["<b>Allocation is: add the object size to a pointer, compare against "
    "the limit, return the old pointer value.</b> Three instructions, no "
    "free list, no size classes, no search, and no metadata per object.",
    "<b>That is genuinely faster than <code>malloc</code></b>, which must "
    "find a suitable free block, maintain its own bookkeeping, and handle "
    "fragmentation. <b>'GC is slow' is too simple a claim</b>, and "
    "allocation-heavy code can be faster under a good collector than under "
    "manual management.",
    "<b>And survivors are copied into contiguous memory</b>, so objects "
    "that survive together end up adjacent — which improves locality "
    "(CSCE 614) in a way manual allocation does not naturally provide.",
    "<b>The real costs are pause time and memory.</b> <b>A garbage "
    "collected program typically needs two to five times its live-set size "
    "to perform well</b>, and performance degrades sharply below that "
    "because collections become frequent and survivor rates rise. "
    "<b>Pauses and memory are the honest trades</b>, not throughput "
    "— and pauses are what makes this a problem for engines "
    "(&sect;3)."]),

  ("h1", "2 &nbsp; JIT compilation"),
  ("callout", "Tiering: start fast, then get fast",
   ["<b>Tier 0 interprets.</b> Zero compilation cost, slow execution. "
    "<b>Most code runs here and never leaves</b>, which is the point "
    "— compiling code that runs twice is a waste.",
    "<b>Tier 1 compiles quickly with minimal optimisation</b>, while "
    "instrumenting the code to gather a profile: which types appear at each "
    "site, which branches are taken, which call targets occur.",
    "<b>Tier 2 compiles the hot code hard</b>, using that profile to "
    "specialise aggressively — assuming the observed types, inlining "
    "through the observed call targets, laying out the observed hot path "
    "straight.",
    "<b>And deoptimises when an assumption breaks.</b> The specialised code "
    "guards every assumption it made; when a guard fails it must transfer "
    "control back to the interpreter <b>mid-function</b>, <b>reconstructing "
    "the interpreter's entire state — locals, operand stack, program "
    "counter — from the optimised frame</b>, in which several of those "
    "values may be in registers, folded into constants, or eliminated "
    "entirely. <b>That reconstruction is the hard part of building a "
    "JIT</b>, and it is what the optimiser must preserve enough information "
    "to make possible — the same problem as Module 10 &sect;4's debug "
    "information, with correctness rather than convenience at stake."]),
  ("callout", "Inline caches: speculating on object shape",
   ["<b>In a dynamic language, <code>x.foo</code> requires a lookup</b> "
    "— the object's layout is not known statically, so the field's "
    "offset must be found at runtime, potentially through a prototype "
    "chain.",
    "<b>But at any given call site the object's shape is usually the same "
    "every single time.</b> The loop that processes a thousand particles "
    "sees a thousand objects with identical layout.",
    "<b>So cache the lookup's result at the site, keyed on the shape.</b> "
    "A <b>monomorphic</b> site — one shape ever observed — "
    "becomes a shape check and a load at a fixed offset, <b>nearly as fast "
    "as a C struct field access</b>.",
    "<b>Polymorphic caches hold a handful of shapes and check each; "
    "megamorphic sites give up and fall back to the full lookup.</b> "
    "<b>This single technique is most of the reason JavaScript is "
    "fast</b>, and it is the direct reason that keeping object shapes "
    "consistent — initialising all fields in the same order, not "
    "adding properties later — is standard JavaScript performance "
    "advice. The advice is about keeping sites monomorphic."]),

  ("break",),
  ("h1", "3 &nbsp; Scripting in an engine"),
  ("table", ["Option", "Character", "Cost"],
   [["<b>Lua or LuaJIT</b>",
     "<b>Tiny, fast, and designed from the start to be embedded.</b> "
     "LuaJIT's tracing JIT is remarkably good.",
     "<b>Small standard library</b>, and LuaJIT's language version is "
     "frozen at 5.1."],
    ["<b>C# via Mono or IL2CPP</b>",
     "A full language with real tooling, debuggers, and a large ecosystem.",
     "<b>A large runtime to ship and GC pauses to manage</b> — which "
     "is Unity's situation and the source of most of its performance "
     "guidance."],
    ["<b>Visual scripting</b>",
     "<b>Non-programmers can author behaviour</b>, which can be "
     "transformative for a content team.",
     "<b>Diffing and merging are painful</b> — graphs do not merge "
     "— and complex logic becomes unreadable. Version control pain is "
     "the usual complaint."],
    ["<b>WebAssembly</b>",
     "Any source language, sandboxed, with predictable performance.",
     "Host interop is awkward; passing structured data across the boundary "
     "requires marshalling."],
    ["<b>A custom DSL</b>",
     "Exactly fits your domain, and can be made safe and fast by "
     "construction.",
     "<b>You own the tooling forever</b> — editor support, debugger, "
     "error messages, documentation. Usually underestimated by a large "
     "factor."],
    ["<b>Native code with hot reload</b>", "<b>Full speed, no boundary.</b>",
     "<b>A script bug crashes the engine</b>, and reload has to handle "
     "state migration."]],
   [0.19, 0.40, 0.41]),
  ("p", "<b>The deciding question is who writes the scripts.</b> Designers, "
        "gameplay programmers, and external modders want substantially "
        "different things from this list, and <b>the answer is a people "
        "question rather than a technical one</b> — which is worth "
        "recognising before the benchmark comparison starts."),
  ("callout", "GC pauses and frame budgets are in direct conflict",
   ["<b>A 60 Hz frame budget is 16.7 milliseconds, and most of it is "
    "already committed</b> to simulation, animation, and rendering. <b>A "
    "10 ms GC pause is a visible hitch</b>; a 50 ms pause is a stutter "
    "every player notices.",
    "<b>So engines fight the allocator rather than tuning the "
    "collector:</b> pool objects, reuse buffers, preallocate at load time, "
    "and avoid allocating anything at all in the per-frame path.",
    "<b>Unity's performance guidance is essentially 'do not allocate during "
    "gameplay'</b>, which is a strong signal about where the problem "
    "actually lies — the recommended solution to having a garbage "
    "collector is to not generate garbage.",
    "<b>Incremental and concurrent collectors trade total throughput for "
    "shorter pauses, which is exactly the right trade here.</b> <b>A frame "
    "budget cares about the worst case, not the mean</b> — the same "
    "argument as CSCE 650 Module 06 made about VR latency, and CSCE 735 "
    "Module 07 made about reporting distributions rather than averages. "
    "<b>A collector that is 10% slower overall and never pauses for more "
    "than 1 ms is strictly better for an interactive application</b>, and "
    "that is not a judgement a throughput benchmark can make."]),

  ("h1", "4 &nbsp; The interface"),
  ("ul", ["<b>Object lifetime across the boundary.</b> A script holds a "
          "reference to a native object; the engine destroys it; the script "
          "uses it. <b>Handles with generation counters</b> rather than raw "
          "pointers are the standard answer, so a stale reference is "
          "detectable rather than catastrophic.",
          "<b>Two collectors, or one collector and manual memory, that "
          "cannot see each other's references.</b> A cycle spanning the "
          "boundary — a native object holding a script object holding "
          "the native object — <b>leaks permanently</b>, because "
          "neither side can prove the other's half unreachable.",
          "<b>Error propagation.</b> A script error must not take the "
          "engine down, must be caught at a defined boundary, and must "
          "still produce a useful message with a script-level stack trace "
          "— which means the embedding must map runtime errors back to "
          "script source locations (Module 10 &sect;4 again).",
          "<b>Threading.</b> Most script runtimes are single-threaded by "
          "design, while the engine is thoroughly parallel (CSCE 735). "
          "<b>Deciding where scripts may run, and what they may touch, is a "
          "design decision that cannot be deferred.</b>",
          "<b>And call overhead.</b> Crossing the boundary has a real "
          "cost — argument marshalling, stack setup, possibly a "
          "lock — and <b>calling into script once per entity per frame "
          "is a measurable fraction of the budget</b>. <b>Batch it</b>: one "
          "call processing a thousand entities beats a thousand calls. "
          "<b>Design the boundary first</b>, because it is much harder to "
          "narrow afterwards and it determines everything else."]),
 ],
 "resources": [
   ("Jones, Hosking & Moss &mdash; The Garbage Collection Handbook",
    "https://gchandbook.org/",
    "<b>The reference for &sect;1.</b> Library copy; the authors maintain a "
    "free bibliography and the first chapters set up the trade-offs well."),
   ("Nystrom &mdash; Crafting Interpreters, 'Garbage Collection' (free)",
    "https://craftinginterpreters.com/garbage-collection.html",
    "A complete mark-sweep collector implemented and explained, including "
    "the root-finding problems that make it tricky."),
   ("V8 and SpiderMonkey engineering blogs (free)",
    "https://v8.dev/blog",
    "<b>Tiering, inline caches, and deoptimisation</b> described by the "
    "people implementing them, with measurements. The best free source for "
    "&sect;2."),
   ("Roberto Ierusalimschy et al. &mdash; The Implementation of Lua 5.0 "
    "(free)",
    "https://www.lua.org/doc/jucs05.pdf",
    "<b>How a language designed for embedding is built</b> — the "
    "&sect;3 option, from its authors. Short and unusually clear."),
 ],
 "exercises": [
   "Implement mark-sweep collection for your interpreter.",
   "<b>Add a copying young generation</b> with a write barrier and "
   "measure allocation throughput before and after.",
   "<b>Measure the generational hypothesis directly</b>: instrument object "
   "lifetimes and plot the survival curve.",
   "Compare allocation cost against <code>malloc</code> for many small "
   "objects.",
   "Measure your collector's pause times and plot the distribution, not "
   "the mean.",
   "<b>Vary the heap size from 1× to 5× the live set</b> and "
   "plot throughput. Explain the shape.",
   "Implement a monomorphic inline cache for field access and measure it.",
   "<b>Make a call site polymorphic</b> and then megamorphic, and measure "
   "the degradation at each step.",
   "Embed Lua in a small program and expose a native type with handles and "
   "generation counters.",
   "<b>Measure the boundary crossing cost</b> and find the batch size at "
   "which it stops mattering.",
 ],
 "selfcheck": [
   "Name six collection algorithms and their trades.",
   "State the generational hypothesis and explain why it makes GC cheap.",
   "What is a write barrier and why is it needed?",
   "Why is allocation in a copying collector fast, and what are the real "
   "costs?",
   "Describe JIT tiering and say what deoptimisation must reconstruct.",
   "What is an inline cache, and what are monomorphic and megamorphic "
   "sites?",
   "Compare six scripting options and say what decides between them.",
   "Why do GC pauses conflict with frame budgets, and what do engines do?",
   "Name five things that make an embedding painful.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Shader Compilation, Testing, and Shipping",
 "subtitle": "The compiler you already depend on, and how to know yours "
             "is right.",
 "question": "Why do games stutter, and how do you test a compiler?",
 "outcomes": [
     "Explain the shader compilation pipeline end to end.",
     "Explain pipeline state objects and shader compilation stutter.",
     "Explain the shader permutation problem.",
     "Apply differential and randomised testing to a compiler.",
     "State what a compiler can honestly promise.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The shader pipeline",
   "blurb": "Where your shader actually goes."},

  {"t": "code", "kicker": "Pipeline", "title": "Source to silicon",
   "lang": "text", "code": """
  HLSL / GLSL source
      |  OFFLINE, at build time -- DXC or glslang
      |    lex, parse, type check, optimise      (Modules 02-09)
      v
  SPIR-V or DXIL           <- an SSA IR (Module 07) you can read
      |                       and ship inside your game package
      |
      |  AT RUNTIME, in the GRAPHICS DRIVER
      |    the driver contains a WHOLE SECOND COMPILER
      |    instruction selection, scheduling, register allocation
      |    for an ISA that is undocumented and changes per GPU
      v
  GPU machine code

  THE KEY FACTS:
    * the second compile happens on the USER'S machine
    * it happens when the PIPELINE STATE OBJECT is created
    * register allocation decides OCCUPANCY (CSCE 735 M08),
      so the driver's allocator decides your performance
    * you cannot see, profile, or control that compiler
""",
   "caption": "<b>Two compilers, and you control only the first.</b> The "
              "one that decides your occupancy runs on the user's machine.",
   "note": "The occupancy connection makes this concrete for anyone who "
           "took 735."},

  {"t": "callout", "title": "Why shader compilation stutter happens",
   "kind": "The explanation, properly",
   "body": ["<b>The driver compiles when a pipeline state object is "
            "created</b> — and a PSO bundles the shaders with the blend, "
            "depth, and raster state, because the driver specialises the "
            "code for all of it.",
            "<b>So a new material, a new effect, or a new state "
            "combination means a compile</b> — tens to hundreds of "
            "milliseconds, on the frame it is first needed.",
            "<b>That is the hitch.</b> It is a compiler running inside "
            "your frame.",
            "<b>The fixes: precompile every PSO at load</b> (so the wait is "
            "a loading screen), <b>ship a pipeline cache</b>, or "
            "<b>compile on a background thread and substitute a "
            "placeholder</b>. <b>All three are now standard, and all three "
            "are work the engine must do deliberately.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Permutations",
   "blurb": "The combinatorial problem underneath."},

  {"t": "callout", "title": "Shader permutations multiply",
   "kind": "The scaling problem",
   "body": ["<b>Shaders are specialised by preprocessor flags</b> — "
            "number of lights, shadows on or off, normal mapping, skinning, "
            "fog, instancing.",
            "<b>n independent boolean features means 2ⁿ "
            "variants.</b> Twenty features is a million shaders.",
            "<b>Specialisation is why they are fast</b> — no dynamic "
            "branching, no unused registers, maximum occupancy.",
            "<b>So the trade is compile time and package size against "
            "runtime speed</b>, and the responses are <b>uber-shaders with "
            "dynamic branching, on-demand compilation, and specialisation "
            "constants</b> (which SPIR-V supports directly, deferring the "
            "choice to pipeline creation)."]},

  {"t": "section", "label": "Part 3", "title": "Testing a compiler",
   "blurb": "The only way to find miscompiles."},

  {"t": "callout", "title": "Differential testing finds what test suites cannot",
   "kind": "The technique",
   "body": ["<b>Generate a random program, run it through two "
            "compilers</b> — or one compiler at two optimisation "
            "levels — and compare the output.",
            "<b>Any difference is a bug in one of them</b>, with no "
            "expected output needed. That is what makes it scale.",
            "<b>The generator must avoid undefined behaviour</b> "
            "(Module 01 §4), or every difference is a false positive. "
            "<b>This is the hard part of building one.</b>",
            "<b>Csmith found over 400 bugs in GCC and LLVM</b>, and "
            "<b>most were in the optimiser</b> — which is exactly where "
            "hand-written tests are weakest, because nobody writes tests "
            "for the interaction of three passes."]},

  {"t": "bullets", "kicker": "The suite", "title": "How to test a compiler",
   "items": [
     "<b>Differential testing against a reference</b>, on generated "
     "programs. The highest-yield technique by a wide margin.",
     "",
     "<b>Self-differential: compare <code>-O0</code> and "
     "<code>-O2</code>.</b> Needs no second compiler at all.",
     "",
     "<b>Metamorphic testing:</b> transform the program in a "
     "meaning-preserving way; the output must not change "
     "(CSCE 620 M13).",
     "",
     "<b>An IR verifier run after every pass</b> — catches a broken "
     "pass immediately rather than three passes later.",
     "",
     "<b>Test case reduction</b> (C-Reduce, <code>llvm-reduce</code>). "
     "<b>A 3,000-line failing case is useless; a 10-line one is a bug "
     "report.</b>",
   ],
   "footnote": "<b>The verifier-after-every-pass discipline is the "
               "cheapest of these</b> and finds the most bugs per hour "
               "spent."},

  {"t": "callout", "title": "Translation validation, and verified compilers",
   "kind": "The stronger options",
   "body": ["<b>Translation validation checks each compilation</b> — "
            "prove this output equivalent to this input, rather than "
            "proving the compiler correct in general. <b>Alive2 does this "
            "for LLVM passes and has found real bugs.</b>",
            "<b>A verified compiler proves the whole thing once.</b> "
            "<b>CompCert is proved correct in Coq</b>, and Csmith found "
            "<i>no</i> miscompiles in its verified parts — the only "
            "compiler tested of which that was true.",
            "<b>The cost is enormous</b> and the optimisation is weaker "
            "than GCC's.",
            "<b>So it is used where a miscompile is unacceptable</b> "
            "— avionics, medical devices, nuclear control. <b>A real "
            "answer, at a real price.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Claiming honestly",
   "blurb": "The course, and the semester, closed."},

  {"t": "bullets", "kicker": "Claims", "title": "What a compiler can honestly promise",
   "items": [
     "<b>'Conforms to this language subset, with these documented "
     "extensions and these known deviations.'</b>",
     "",
     "<b>'Tested differentially against GCC on 10 million generated "
     "programs; 3 miscompiles found and fixed.'</b> That is the claim "
     "— not 'correct'.",
     "",
     "<b>'This optimisation level makes these transformations and "
     "assumes no undefined behaviour.'</b>",
     "",
     "<b>'Debug information is accurate at -O0 and degrades "
     "predictably above it.'</b>",
     "",
     "<b>And what you cannot say: 'it generates correct code'.</b> "
     "<b>CompCert can say something close. You cannot.</b>",
   ],
   "footnote": "<b>Stating what was tested, and how much</b>, is the only "
               "honest form the claim can take."},

  {"t": "callout", "title": "Where this leaves you",
   "kind": "Closing",
   "body": ["You can build a compiler end to end, and you know which "
            "representation makes each phase possible.",
            "<b>And you understand the toolchain you already "
            "depended on</b> — what <code>-O2</code> is doing, why "
            "undefined behaviour is dangerous, why your shaders stutter, "
            "and what a driver is doing on the user's machine.",
            "<b>CSCE 614 described the machine this targets; 629 gave the "
            "algorithms; 735 explained what the generated code must "
            "exploit; 620 supplied the geometry.</b>",
            "<b>CSCE 678 finishes the semester</b> — once the code is "
            "compiled and correct, the remaining question is how more than "
            "one machine runs it together."]},
 ],
 "takeaways": [
   "A shader is compiled twice: offline to SPIR-V or DXIL, and again by the "
   "driver on the user's machine for an undocumented ISA you cannot "
   "profile.",
   "Stutter happens because the driver compiles when a pipeline state "
   "object is created, which is a compiler running inside your frame.",
   "n boolean shader features means 2ⁿ variants; specialisation is why "
   "shaders are fast and why the permutation count explodes.",
   "Differential testing on generated programs needs no expected output, "
   "which is what makes it scale — and the generator must avoid "
   "undefined behaviour.",
   "Running an IR verifier after every pass is the cheapest testing "
   "discipline and finds the most bugs per hour.",
   "You cannot claim a compiler generates correct code; you can state what "
   "was tested and how much.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The shader compilation pipeline"),
  ("code", """HLSL / GLSL source
   |  OFFLINE, at build time (DXC, glslang)
   |    lex, parse, type check, optimise      (Modules 02-09)
   v
SPIR-V or DXIL      <- an SSA IR (Module 07) you can disassemble
   |                   and that ships inside your game package
   |  AT RUNTIME, INSIDE THE GRAPHICS DRIVER
   |    a WHOLE SECOND COMPILER: instruction selection,
   |    scheduling, register allocation, for an ISA that is
   |    undocumented and differs per GPU generation
   v
GPU machine code

  * the second compile runs on the USER'S machine
  * it runs when a PIPELINE STATE OBJECT is created
  * its register allocation decides OCCUPANCY (CSCE 735 M08)
  * you cannot see, profile, or control it"""),
  ("p", "<b>Two compilers, and you control only the first.</b> The one that "
        "performs register allocation — and therefore determines "
        "occupancy, and therefore determines whether your shader achieves "
        "its memory latency hiding (CSCE 735 Module 08 &sect;3) — "
        "runs on the user's machine, is written by the GPU vendor, and "
        "changes with every driver release. <b>That is why shader "
        "performance can change without your code changing</b>, and why "
        "vendors ship game-specific driver optimisations."),
  ("callout", "Why shader compilation stutter happens",
   ["<b>The driver compiles when a pipeline state object is created</b>, "
    "not when the shader is loaded. <b>A PSO bundles the shaders together "
    "with the blend state, depth state, raster state, and render target "
    "formats</b>, because the driver specialises the generated code for all "
    "of them — fixed-function state that used to be hardware is now "
    "folded into the shader.",
    "<b>So a new material, a new effect, or merely a new combination of "
    "existing state means a fresh compile</b> — tens to hundreds of "
    "milliseconds — <b>on the frame it is first needed</b>, which is "
    "typically the frame the player first walks into a new area or fires a "
    "new weapon.",
    "<b>That is the hitch.</b> It is a compiler running inside your frame "
    "budget, and it is why the stutter correlates with new content rather "
    "than with load.",
    "<b>The three fixes are all now standard and all require deliberate "
    "engine work:</b> <b>precompile every PSO at load time</b> so the wait "
    "becomes a loading screen or a shader-compilation progress bar; "
    "<b>ship a pipeline cache</b> so the work is done once per machine "
    "rather than once per run; or <b>compile on a background thread and "
    "substitute a placeholder</b> material until it is ready. <b>Explicit "
    "APIs made this visible rather than causing it</b> — older APIs "
    "did the same compilation, less predictably, which was arguably "
    "worse."]),

  ("h1", "2 &nbsp; The permutation problem"),
  ("callout", "Shader permutations multiply",
   ["<b>Shaders are specialised by preprocessor flags</b> — the number "
    "of lights, whether shadows are enabled, normal mapping, skinning, fog, "
    "instancing, which lighting model, which tone curve.",
    "<b>n independent boolean features produce 2<super>n</super> "
    "variants.</b> Twenty features is a million shader programs, each of "
    "which must be compiled, stored, and shipped. Real engines have had "
    "hundreds of thousands.",
    "<b>Specialisation is exactly why they are fast.</b> A variant with "
    "shadows disabled contains no shadow code at all — no dynamic "
    "branch, no unused registers holding shadow parameters, and therefore "
    "<b>higher occupancy</b> (CSCE 735 Module 08). The alternative, one "
    "shader branching at runtime, pays register pressure for code it does "
    "not execute.",
    "<b>So the trade is compile time and package size against runtime "
    "speed</b>, and the standard responses are: <b>uber-shaders</b> with "
    "dynamic branching (fewer variants, lower peak performance), "
    "<b>on-demand compilation</b> of only the variants actually used, and "
    "<b>specialisation constants</b> — which SPIR-V supports directly, "
    "allowing one module to be specialised at pipeline creation time "
    "rather than at build time. <b>Specialisation constants are the "
    "principled answer</b>, and they move the combinatorial cost from your "
    "build to the user's PSO creation, which is &sect;1's problem again."]),

  ("break",),
  ("h1", "3 &nbsp; Testing a compiler"),
  ("callout", "Differential testing finds what test suites cannot",
   ["<b>Generate a random program, compile it with two different "
    "compilers</b> — or with the same compiler at two optimisation "
    "levels — run both, and compare the outputs.",
    "<b>Any difference is a bug in one of them</b>, and crucially <b>no "
    "expected output is needed</b>. That is what makes the technique scale "
    "to millions of programs: the oracle is the comparison itself.",
    "<b>The generator must avoid undefined behaviour</b> (Module 01 "
    "&sect;4), or every difference is a false positive — two compilers "
    "may legitimately produce different results for a program with signed "
    "overflow in it. <b>This is the genuinely hard part of building "
    "one</b>, and most of Csmith's engineering is in guaranteeing that its "
    "generated programs have defined behaviour.",
    "<b>Csmith found over 400 previously unknown bugs in GCC and LLVM</b>, "
    "and <b>the majority were in the optimiser</b> — which is exactly "
    "where hand-written test suites are weakest, because nobody writes a "
    "test for the interaction between three passes that only misbehaves "
    "when a loop is unrolled after being vectorised."]),
  ("ul", ["<b>Differential testing against a reference implementation</b>, "
          "on generated programs. <b>The highest-yield technique available "
          "by a wide margin</b>, and the one to build first.",
          "<b>Self-differential testing: compare <code>-O0</code> against "
          "<code>-O2</code>.</b> Requires no second compiler at all, and "
          "finds optimiser bugs specifically — which is where they "
          "are.",
          "<b>Metamorphic testing:</b> transform the source in a "
          "meaning-preserving way (rename variables, reorder independent "
          "statements, wrap in a function) and require the output to be "
          "unchanged. The same technique as CSCE 620 Module 13 &sect;2, and "
          "equally cheap here.",
          "<b>An IR verifier run after every pass</b>, checking "
          "well-formedness and dominance (Module 07 &sect;3). <b>This "
          "catches a broken pass immediately rather than three passes "
          "later</b>, when the symptom has become unrecognisable. <b>It is "
          "the cheapest item on this list and finds the most bugs per hour "
          "spent.</b>",
          "<b>Automatic test case reduction</b> — C-Reduce, "
          "<code>llvm-reduce</code>, or your own delta debugger. <b>A "
          "3,000-line failing program is useless; the same bug reduced to "
          "10 lines is an actionable bug report</b>, and reduction is "
          "mechanical enough to automate."]),
  ("callout", "Translation validation, and verified compilers",
   ["<b>Translation validation checks each individual compilation</b> "
    "rather than the compiler in general: prove that <i>this</i> output is "
    "equivalent to <i>this</i> input. It is a weaker guarantee that is "
    "vastly easier to obtain. <b>Alive2 does this for LLVM optimisation "
    "passes and has found real, long-standing bugs</b>, including in "
    "transformations that had been in the compiler for years.",
    "<b>A verified compiler proves the whole thing once, mechanically.</b> "
    "<b>CompCert is a C compiler proved correct in the Coq proof "
    "assistant</b>, with a machine-checked theorem that the generated "
    "assembly refines the source semantics.",
    "<b>Csmith found no miscompiles in CompCert's verified parts</b> "
    "— bugs were found only in its unverified front end. <b>It was "
    "the only compiler tested of which that was true</b>, which is about "
    "as strong an empirical endorsement as a formal method has ever "
    "received.",
    "<b>The cost is enormous</b> — person-decades of proof engineering "
    "— <b>and the generated code is slower than GCC's</b>, because "
    "every optimisation must be proved and the aggressive ones are hard to "
    "prove. <b>So it is used where a miscompile is unacceptable</b>: "
    "avionics, medical devices, nuclear control, and safety-critical "
    "automotive. <b>A real answer at a real price</b>, which is the correct "
    "way to think about formal verification generally."]),

  ("h1", "4 &nbsp; Claiming honestly"),
  ("ul", ["<b>'Conforms to this language subset, with these documented "
          "extensions and these known deviations.'</b> Every compiler has "
          "deviations; the honest ones list them.",
          "<b>'Tested differentially against GCC on ten million generated "
          "programs; three miscompiles found and fixed.'</b> <b>That is the "
          "claim</b> — the number of programs and the number of bugs "
          "— <b>not 'correct'</b>. It states the evidence and lets the "
          "reader judge the confidence.",
          "<b>'This optimisation level performs these transformations and "
          "assumes the absence of undefined behaviour.'</b> The second "
          "clause is the one users need and rarely get (Module 01 "
          "&sect;4).",
          "<b>'Debug information is accurate at <code>-O0</code> and "
          "degrades predictably above it.'</b> Rather than claiming it "
          "works, say how it fails (Module 10 &sect;4).",
          "<b>And what you cannot honestly say: 'it generates correct "
          "code'.</b> <b>CompCert can say something close to that, with a "
          "machine-checked proof and a stated set of assumptions. You "
          "cannot</b>, and the gap between 'extensively tested' and "
          "'proved' is exactly the gap that Module 01 &sect;4 said makes "
          "compiler bugs so expensive."]),
  ("callout", "Where this leaves you",
   ["<b>You can build a compiler end to end</b> — lexer, parser, "
    "resolver, type checker, SSA construction, dataflow analysis, "
    "optimisation, instruction selection, register allocation — "
    "<b>and you know which representation makes each phase possible</b>, "
    "which was the organising claim of Module 01.",
    "<b>And you understand the toolchain you were already depending "
    "on:</b> what <code>-O2</code> is actually doing, why undefined "
    "behaviour is dangerous rather than merely unspecified, why a debugger "
    "says 'optimised out', why your shaders stutter the first time an "
    "effect appears, and what the graphics driver is doing on the user's "
    "machine that you cannot see.",
    "<b>CSCE 614 described the machine this targets. CSCE 629 supplied the "
    "algorithms the optimiser applies. CSCE 735 explained what the "
    "generated code has to exploit to be fast, and CSCE 620 supplied the "
    "geometry the engine runs on.</b>",
    "<b>CSCE 678 finishes the semester.</b> Once the code is compiled and "
    "correct and fast, <b>the remaining question is how more than one "
    "machine runs it together</b> — which turns out to be a problem "
    "with its own impossibility results, its own failure modes, and its own "
    "reasons for being harder than it looks."]),
 ],
 "resources": [
   ("Khronos &mdash; SPIR-V specification, SPIRV-Cross, and SPIRV-Tools "
    "(free)",
    "https://registry.khronos.org/SPIR-V/",
    "<b>The &sect;1 pipeline.</b> <code>spirv-dis</code> and "
    "<code>spirv-opt</code> let you watch the offline half of it happen."),
   ("Yang, Chen, Eide & Regehr &mdash; Finding and Understanding Bugs in C "
    "Compilers (free)",
    "https://www.flux.utah.edu/paper/yang-pldi11",
    "<b>Csmith.</b> The method of &sect;3, the results, and the CompCert "
    "comparison. The most important paper in this course."),
   ("Lee, Hur, Nagarakatte et al. &mdash; Alive2 (free)",
    "https://github.com/AliveToolkit/alive2",
    "<b>Translation validation for LLVM passes</b>, usable on your own "
    "transformations."),
   ("Leroy &mdash; CompCert, and Formal Verification of a Realistic "
    "Compiler (free)",
    "https://compcert.org/",
    "The verified compiler of &sect;3, with the papers explaining what "
    "exactly is proved and what is assumed."),
   ("Microsoft &mdash; DirectX Shader Compiler; and the Vulkan pipeline "
    "cache documentation (free)",
    "https://github.com/microsoft/DirectXShaderCompiler",
    "The practical &sect;1 and &sect;2 material: PSO creation, pipeline "
    "caches, and specialisation constants."),
 ],
 "exercises": [
   "<b>Disassemble a shader to SPIR-V</b> and identify its basic blocks, "
   "φ instructions, and entry point.",
   "Run <code>spirv-opt</code> with and without optimisation and diff the "
   "result.",
   "<b>Measure PSO creation time</b> in a Vulkan or D3D12 application and "
   "report the distribution.",
   "Implement a pipeline cache and measure the second-run improvement.",
   "<b>Count the permutations</b> in a real shader system you have access "
   "to, and estimate the total compile time.",
   "Convert one permutation axis to a specialisation constant and compare "
   "variant count and performance.",
   "<b>Build a random program generator</b> for your language that avoids "
   "undefined behaviour.",
   "<b>Differentially test your compiler against itself</b> at two "
   "optimisation levels on a million programs. Report what you find.",
   "<b>Add an IR verifier and run it after every pass.</b> Report how many "
   "bugs it catches that your tests did not.",
   "Implement delta-debugging reduction and reduce a failing case to under "
   "twenty lines.",
   "<b>Project 2 is now due.</b> Submit the compiler, the per-pass "
   "measurements including negative results, the pass-ordering evidence, "
   "the differential testing results, and the honest comparison against "
   "<code>gcc -O2</code>.",
 ],
 "selfcheck": [
   "Describe the shader compilation pipeline and say where each compile "
   "happens.",
   "Why does the driver's register allocator determine your performance?",
   "Explain shader compilation stutter and give three fixes.",
   "Why do permutations multiply, and why is specialisation worth it?",
   "What are specialisation constants and what do they move?",
   "Describe differential testing and say why the generator is the hard "
   "part.",
   "Name five compiler testing techniques and say which is cheapest.",
   "Contrast translation validation with a verified compiler.",
   "Give four honest claims and one thing you cannot say.",
 ],
},

]
