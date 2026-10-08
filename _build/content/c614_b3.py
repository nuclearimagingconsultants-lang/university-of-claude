# -*- coding: utf-8 -*-
"""CSCE 614 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Out-of-Order Execution",
 "subtitle": "Running instructions early while pretending you did not.",
 "question": "How does a processor keep working during a 250-cycle cache "
             "miss?",
 "outcomes": [
     "Explain register renaming and why it removes false dependences.",
     "Describe the reorder buffer and in-order retirement.",
     "Explain what limits instruction-level parallelism.",
     "Explain memory-level parallelism and why it matters more than ILP.",
     "Relate out-of-order behaviour to measured IPC.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The motivation",
   "blurb": "One stalled instruction should not stop everything."},

  {"t": "code", "kicker": "The problem", "title": "In-order stalls on the first miss",
   "lang": "asm", "code": """
    ld   r1, [r2]       ; CACHE MISS -- 250 cycles
    add  r3, r1, r4     ; depends on r1: must wait. Correct.
    mul  r5, r6, r7     ; INDEPENDENT -- why should this wait?
    sub  r8, r9, r10    ; also independent
    ...

In-order: everything behind the load stalls. 250 cycles of nothing.

Out-of-order: mul and sub execute DURING the miss. By the time r1
arrives, a great deal of useful work has already been done.
""",
   "caption": "The processor is not trying to be clever for its own sake. It "
              "is trying to find anything at all to do during a 250-cycle "
              "wait.",
   "note": "Frame OoO as latency hiding, not as reordering for its own sake. "
           "That makes every mechanism that follows feel necessary."},

  {"t": "section", "label": "Part 2", "title": "Register renaming",
   "blurb": "Removing the dependences that were never real."},

  {"t": "code", "kicker": "Renaming", "title": "False dependences, dissolved",
   "lang": "asm", "code": """
BEFORE renaming -- r1 reused, creating a WAW/WAR tangle:
    ld   r1, [r2]       ; writes r1   (slow)
    add  r3, r1, r4     ; reads  r1   -- TRUE dependence (RAW)
    ld   r1, [r5]       ; writes r1   -- FALSE (WAW) -- must it wait?
    add  r6, r1, r7     ; reads  r1

AFTER renaming to physical registers p40, p41, ...:
    ld   p40, [p12]
    add  p41, p40, p13  ; still waits -- RAW is real
    ld   p42, [p14]     ; INDEPENDENT -- different physical register
    add  p43, p42, p15  ;   -> can issue immediately

Two independent load chains, discovered automatically.
""",
   "caption": "Module 03 called WAR and WAW false dependences. Renaming is "
              "what makes that observation operational.",
   "note": "The payoff: both loads can be in flight simultaneously, which is "
           "memory-level parallelism — Part 4."},

  {"t": "bullets", "kicker": "Renaming", "title": "How it works",
   "items": [
     "The ISA exposes 16 architectural registers. The core has 150–400 "
     "<b>physical</b> ones.",
     "",
     "Each write to an architectural register allocates a fresh physical "
     "register.",
     "Reads are redirected to whichever physical register currently holds "
     "that architectural value.",
     "",
     "WAR and WAW vanish — they were artefacts of name reuse, and names "
     "are no longer reused.",
     "RAW remains, because it is a genuine flow of information.",
     "",
     "This is why Module 03's distinction between true and false dependences "
     "mattered.",
   ]},

  {"t": "section", "label": "Part 3", "title": "Keeping the illusion",
   "blurb": "Execute out of order; appear to execute in order."},

  {"t": "bullets", "kicker": "ROB", "title": "The reorder buffer",
   "items": [
     "Instructions <b>issue</b> out of order, as soon as their operands are "
     "ready.",
     "Instructions <b>retire</b> strictly in order, from the reorder buffer.",
     "",
     "Retirement is what makes a result architecturally visible.",
     "",
     "This gives two things at once:",
     ("<b>Precise exceptions</b> — a fault appears to occur exactly "
      "where the program says.", 1),
     ("<b>Speculation recovery</b> — mispredicted work is discarded "
      "before it ever becomes visible.", 1),
     "",
     "ROB size (300–500 entries) bounds how far ahead the core can look.",
   ],
   "note": "In-order retirement is the mechanism that makes the whole thing "
           "safe. Without it neither exceptions nor speculation would work."},

  {"t": "table", "kicker": "Window", "title": "What limits how far ahead it can see",
   "header": ["Resource", "Typical size", "Runs out when"],
   "widths": [3.4, 3.2, 5.5],
   "rows": [
     ["Reorder buffer", "~500 entries", "A long-latency miss blocks the head"],
     ["Physical registers", "~200–400", "Many values live at once"],
     ["Load/store queue", "~70–130", "Many memory ops in flight"],
     ["Scheduler entries", "~100–200", "Many waiting instructions"],
   ],
   "footnote": "When any one fills, the core stalls regardless of the others.",
   "note": "The ROB-head point is the key one: a miss at the head blocks "
           "retirement even though execution continues behind it."},

  {"t": "section", "label": "Part 4", "title": "What actually limits performance",
   "blurb": "Not instruction-level parallelism — memory-level "
            "parallelism."},

  {"t": "callout", "title": "MLP matters more than ILP", "kind": "Key idea",
   "body": ["Instruction-level parallelism is bounded: dependence chains in "
            "real code limit practical ILP to roughly 4–6, and wider "
            "cores show diminishing returns.",
            "<b>Memory-level parallelism</b> — how many cache misses are "
            "outstanding at once — matters far more.",
            "One miss at a time: 250 cycles each, serialised. Ten misses "
            "overlapped: still roughly 250 cycles total.",
            "So the real value of out-of-order execution is not executing "
            "arithmetic early. It is <b>discovering independent memory "
            "accesses and issuing them simultaneously</b>."]},

  {"t": "bullets", "kicker": "Consequences", "title": "What this means for your code",
   "items": [
     "<b>Independent loads are enormously valuable.</b> Multiple pointers, "
     "multiple arrays, multiple accumulators.",
     "",
     "<b>Pointer chasing is the worst case.</b> Each load depends on the "
     "last, so MLP is exactly 1.",
     ("A linked list cannot overlap any of its misses. This is the deepest "
      "reason it loses to an array.", 1),
     "",
     "<b>A long dependence chain through a miss is fatal</b> — the ROB "
     "fills and the core stalls.",
     "",
     "<b>Hyperthreading</b> exists to supply independent work when one thread "
     "stalls.",
   ],
   "note": "This completes the array-vs-list story begun in Module 02 and "
           "continued in 05. Three modules, one phenomenon, three levels of "
           "explanation."},

  {"t": "table", "kicker": "Reading IPC", "title": "Diagnosing from counters",
   "header": ["IPC", "Means", "Next step"],
   "widths": [2.2, 5.0, 4.9],
   "rows": [
     ["3–4", "Near peak — compute-bound", "Reduce work, or vectorise"],
     ["1–2", "Moderate stalling", "Check dependence chains, branches"],
     ["0.3–1", "Significant stalls", "Check cache misses"],
     ["&lt; 0.3", "Severely memory-bound", "Layout and access pattern (Mod 06)"],
   ],
   "note": "IPC is the first number to look at, and it narrows the search "
           "immediately."},
 ],
 "takeaways": [
   "Out-of-order execution exists to find work during long memory stalls, not "
   "to reorder arithmetic for its own sake.",
   "Register renaming maps 16 architectural registers onto hundreds of "
   "physical ones, dissolving the WAR and WAW dependences that were only "
   "naming artefacts.",
   "Instructions issue out of order and retire in order. In-order retirement "
   "is what gives precise exceptions and safe speculation.",
   "The reorder buffer bounds the lookahead window; a miss at its head blocks "
   "retirement and eventually stalls everything.",
   "Memory-level parallelism matters more than instruction-level "
   "parallelism — overlapping ten misses costs about the same as one.",
   "Pointer chasing has MLP of exactly 1, which is the deepest reason linked "
   "lists lose to arrays.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why execute out of order"),
  ("p", "An in-order pipeline stalls at the first instruction that cannot "
        "proceed, and everything behind it waits even if it is completely "
        "independent."),
  ("code", """    ld   r1, [r2]        ; cache miss: 250 cycles
    add  r3, r1, r4      ; depends on r1 -- must wait (correct)
    mul  r5, r6, r7      ; independent -- no reason to wait
    sub  r8, r9, r10     ; independent"""),
  ("p", "During a 250-cycle miss, a 4-wide core could have executed roughly a "
        "thousand instructions. An in-order machine executes none. The "
        "motivation for out-of-order execution is not elegance; it is that "
        "the alternative wastes an enormous fraction of the machine whenever "
        "memory is touched."),

  ("h1", "2 &nbsp; Register renaming"),
  ("p", "Module 03 distinguished true dependences (RAW — real "
        "information flow) from false ones (WAR and WAW — artefacts of "
        "two instructions happening to use the same register name). Renaming "
        "is the mechanism that acts on that distinction."),
  ("code", """Before renaming -- r1 is reused:
    ld   r1, [r2]        ; writes r1
    add  r3, r1, r4      ; reads  r1   -- RAW, genuine
    ld   r1, [r5]        ; writes r1   -- WAW with the first load
    add  r6, r1, r7      ; reads  r1

After renaming to physical registers:
    ld   p40, [p12]
    add  p41, p40, p13   ; still dependent -- RAW is real
    ld   p42, [p14]      ; now INDEPENDENT of the first load
    add  p43, p42, p15"""),
  ("p", "The processor maintains a far larger set of physical registers "
        "(150&ndash;400) than the ISA exposes (16 on x86-64), plus a mapping "
        "table. Every write to an architectural register allocates a fresh "
        "physical register; every read is redirected to whichever physical "
        "register currently holds that value."),
  ("callout", "What this buys",
   ["False dependences disappear entirely, because register names are never "
    "reused. True dependences remain, because they represent actual data "
    "flow and no amount of renaming can remove them.",
    "In the example, the two load chains become independent, so <b>both loads "
    "can be outstanding at the same time</b>. That is memory-level "
    "parallelism, and &sect;4 argues it is the single most valuable thing the "
    "mechanism provides."]),

  ("h1", "3 &nbsp; Keeping the illusion of sequential execution"),
  ("p", "Instructions <b>issue</b> and <b>execute</b> out of order, whenever "
        "their operands become available. They <b>retire</b> — commit "
        "their results to architectural state — strictly in program "
        "order, from the <b>reorder buffer</b>."),
  ("p", "In-order retirement is what makes the whole scheme safe, and it "
        "provides two essential properties:"),
  ("ul", ["<b>Precise exceptions.</b> If instruction 50 faults, instructions "
          "1&ndash;49 have retired and 51 onward have not, regardless of what "
          "order they actually executed in. The exception appears exactly "
          "where the program says it should, which is what makes debugging "
          "and signal handling possible at all.",
          "<b>Speculation recovery.</b> Work done down a mispredicted branch "
          "is sitting in the reorder buffer unretired. Discarding it is "
          "simply a matter of flushing those entries — nothing "
          "architecturally visible ever happened. This is precisely the "
          "mechanism Module 04 relied on."]),
  ("table", ["Resource", "Typical capacity", "Exhausted when"],
   [["Reorder buffer", "~500 entries",
     "A long-latency miss sits at the head and blocks retirement while "
     "execution continues behind it, filling the buffer."],
    ["Physical registers", "200&ndash;400",
     "Many values are simultaneously live."],
    ["Load/store queue", "70&ndash;130 entries",
     "Many memory operations are in flight."],
    ["Scheduler (reservation stations)", "100&ndash;200 entries",
     "Many instructions are waiting on operands."]],
   [0.26, 0.22, 0.52]),
  ("p", "The <b>instruction window</b> is bounded by whichever of these fills "
        "first. A cache miss at the head of the reorder buffer is the classic "
        "stall: the core continues executing younger instructions, but none "
        "can retire, and when the buffer fills, everything halts. This is why "
        "a single long-latency miss on the critical path can cost far more "
        "than its nominal latency."),

  ("break",),
  ("h1", "4 &nbsp; ILP, MLP, and which one matters"),
  ("p", "<b>Instruction-level parallelism</b> is how many independent "
        "instructions are available to execute simultaneously. Decades of "
        "research established that real code has limited ILP — "
        "dependence chains, branches, and memory ambiguity hold practical "
        "values to roughly 4&ndash;6, which is why core widths stopped "
        "growing aggressively."),
  ("callout", "Memory-level parallelism is the one that pays",
   ["<b>MLP</b> is how many cache misses are outstanding simultaneously.",
    "Serialised: ten misses, one at a time, 250 cycles each = 2,500 cycles.",
    "Overlapped: ten misses issued together = roughly 250 cycles total, "
    "because the memory system handles them concurrently.",
    "A factor of ten, from the same ten misses. No amount of arithmetic "
    "reordering comes close to that.",
    "So the real purpose of out-of-order execution is to look far enough "
    "ahead to <i>find independent memory accesses and issue them at the same "
    "time</i>. The arithmetic reordering is almost incidental."]),
  ("h2", "4.1 &nbsp; Consequences for code"),
  ("ul", ["<b>Independent loads are valuable.</b> Traversing four arrays at "
          "once, or using several independent pointers, allows several misses "
          "to overlap. Processing them one array at a time does not.",
          "<b>Pointer chasing has MLP of exactly 1.</b> The address of the "
          "next node is not known until the current load returns, so no two "
          "misses can ever overlap. This is the deepest level of the "
          "array-versus-linked-list story: Module 02 explained the "
          "dependence, Module 05 the cache lines, and this module the lost "
          "parallelism.",
          "<b>A dependence chain running through a miss is the worst "
          "case.</b> The reorder buffer fills with instructions that cannot "
          "retire, and the window collapses.",
          "<b>Hyperthreading exists for this.</b> When one thread stalls on "
          "memory, a second thread supplies genuinely independent work to "
          "keep the execution units busy. It helps most on memory-bound code "
          "and can hurt on code that already saturates the core."]),

  ("h1", "5 &nbsp; Reading IPC"),
  ("table", ["Measured IPC", "Interpretation", "Where to look next"],
   [["3&ndash;4", "Near the machine's peak issue rate. Compute-bound.",
     "Reduce the work itself, or vectorise it (Module 09). Memory "
     "optimisation will not help."],
    ["1&ndash;2", "Moderate stalling.",
     "Dependence chains, branch mispredictions, or partial memory stalls. "
     "Check branch-misses first since it is cheap to rule out."],
    ["0.3&ndash;1", "Substantial stalling.",
     "Almost certainly memory. Check L1, L2, and LLC miss rates."],
    ["Below 0.3", "Severely memory-bound.",
     "Data layout and access pattern (Module 06). Also check TLB misses "
     "(Module 07)."]],
   [0.17, 0.33, 0.50]),
  ("p", "IPC is the first number to obtain for any performance question "
        "because it immediately partitions the search space: either the core "
        "is working, in which case you must do less work, or it is waiting, "
        "in which case you must find out for what."),
 ],
 "resources": [
   ("Onur Mutlu — Out-of-Order Execution, Tomasulo's Algorithm",
    "https://safari.ethz.ch/architecture/",
    "Renaming, reservation stations, and the reorder buffer developed in "
    "full."),
   ("Agner Fog — The microarchitecture of Intel, AMD and VIA CPUs",
    "https://www.agner.org/optimize/",
    "Actual window sizes, physical register counts, and execution port "
    "layouts for every recent core."),
   ("Travis Downs — performance blog",
    "https://travisdowns.github.io/",
    "Careful microbenchmark-driven investigations of out-of-order behaviour. "
    "An excellent model of how to measure this material."),
   ("Intel — Top-Down Microarchitecture Analysis Method",
    "https://www.intel.com/content/www/us/en/docs/vtune-profiler/cookbook/current/top-down-microarchitecture-analysis-method.html",
    "A systematic method for attributing stalls to front end, back end, bad "
    "speculation, or retiring. The professional version of &sect;5."),
 ],
 "exercises": [
   "Write a loop with a long chain of dependent additions and one with the "
   "same number of independent additions. Measure IPC for both and explain "
   "the difference.",
   "Construct a memory-level parallelism experiment: traverse one pointer "
   "chain, then two, four, and eight independent chains simultaneously. Plot "
   "throughput against chain count and find where it saturates — that is "
   "your machine's MLP limit.",
   "Demonstrate the reorder-buffer limit: place a cache miss followed by "
   "increasing numbers of independent instructions, and find the point at "
   "which adding more stops helping.",
   "Measure the same memory-bound kernel with hyperthreading enabled and "
   "disabled. Then repeat with a compute-bound kernel. Explain both results.",
   "Use <code>perf stat</code> to compute IPC for five programs of your own, "
   "and classify each using the table in &sect;5. Verify your classification "
   "by checking the corresponding counter.",
   "Write a linked-list traversal and an equivalent array traversal with "
   "identical element counts and working-set size. Measure both and attribute "
   "the difference to MLP rather than to cache behaviour alone — you "
   "will need to control for line utilisation.",
 ],
 "selfcheck": [
   "What is out-of-order execution actually for?",
   "What does register renaming remove, and what can it not remove?",
   "Why must instructions retire in order when they execute out of order? "
   "Name the two properties this provides.",
   "What is the instruction window, and what exhausts it first during a cache "
   "miss?",
   "Define MLP and explain why it matters more than ILP.",
   "Why does pointer chasing have MLP of 1, and what are the three levels of "
   "explanation for why linked lists are slow?",
   "Your program shows IPC 0.2. What do you check next, and why?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "SIMD and Data-Level Parallelism",
 "subtitle": "One instruction, many elements.",
 "question": "How do you get 8× throughput without more cores?",
 "outcomes": [
     "Explain SIMD execution and its register widths.",
     "Identify loops that can and cannot vectorise.",
     "Diagnose why a compiler failed to auto-vectorise.",
     "Use intrinsics when auto-vectorisation is insufficient.",
     "Explain why SoA layout is a precondition for good vectorisation.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The idea",
   "blurb": "Amortise instruction overhead across many data elements."},

  {"t": "code", "kicker": "SIMD", "title": "Width is throughput",
   "lang": "c", "code": """
// Scalar: one add per instruction
for (i = 0; i < N; i++) c[i] = a[i] + b[i];

// SSE   (128-bit):  4 floats per instruction
// AVX2  (256-bit):  8 floats per instruction
// AVX-512 (512-bit): 16 floats per instruction

__m256 va = _mm256_load_ps(&a[i]);     // 8 floats
__m256 vb = _mm256_load_ps(&b[i]);
__m256 vc = _mm256_add_ps(va, vb);     // 8 additions, ONE instruction
_mm256_store_ps(&c[i], vc);
""",
   "caption": "Same execution unit count, eight times the arithmetic. The "
              "instruction fetch, decode, and loop overhead are amortised "
              "across all eight elements.",
   "note": "Worth noting that AVX-512 often downclocks the core, so 16-wide "
           "is not always 2x the 8-wide throughput."},

  {"t": "table", "kicker": "Widths", "title": "The instruction set families",
   "header": ["Extension", "Width", "Floats", "Notes"],
   "widths": [3.0, 2.4, 2.4, 4.3],
   "rows": [
     ["SSE / SSE2", "128-bit", "4", "Baseline on all x86-64"],
     ["AVX / AVX2", "256-bit", "8", "The practical default today"],
     ["AVX-512", "512-bit", "16", "Server; may reduce clock frequency"],
     ["NEON (ARM)", "128-bit", "4", "Baseline on all ARM64"],
     ["SVE (ARM)", "Scalable", "Varies", "Width-agnostic code"],
   ],
   "note": "SVE's width-agnostic model is the interesting design: the same "
           "binary adapts to whatever width the hardware has."},

  {"t": "section", "label": "Part 2", "title": "What blocks vectorisation",
   "blurb": "The compiler will do this for you — if you let it."},

  {"t": "table", "kicker": "Blockers", "title": "Why your loop did not vectorise",
   "header": ["Blocker", "Why", "Fix"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Pointer aliasing", "Compiler cannot prove a and b are disjoint",
      "<code>restrict</code>, or copy locally"],
     ["Loop-carried dependence", "Iteration i needs iteration i−1",
      "Restructure, or accept it"],
     ["FP reduction", "Reassociation changes the result",
      "<code>-ffast-math</code>, knowingly"],
     ["Branches in the body", "Divergent control flow",
      "Masking, or branchless arithmetic"],
     ["Non-unit stride", "Gathers are slow or unavailable",
      "<b>Change the layout</b> (Module 06)"],
     ["Function calls", "Cannot vectorise an opaque call", "Inline it"],
   ],
   "note": "Aliasing is by far the most common, and `restrict` is by far the "
           "cheapest fix."},

  {"t": "code", "kicker": "Aliasing", "title": "The most common blocker",
   "lang": "c", "code": """
void add(float* c, float* a, float* b, int n) {
    for (int i = 0; i < n; i++) c[i] = a[i] + b[i];
}
// Will NOT vectorise. The compiler must assume c may overlap a or b,
// in which case processing 8 at once would change the result.

void add(float* restrict c, float* restrict a,
         float* restrict b, int n) {
    for (int i = 0; i < n; i++) c[i] = a[i] + b[i];
}
// `restrict` promises no overlap. Vectorises immediately.
// NOTE: it is a PROMISE. Break it and you get silent corruption.
""",
   "caption": "One keyword, frequently an 8× difference. C++ has no "
              "standard <code>restrict</code>, but every major compiler "
              "offers <code>__restrict</code>.",
   "note": "Stress the 'promise' framing — restrict is unchecked and "
           "violating it is undefined behaviour."},

  {"t": "callout", "title": "Floating-point reductions and why they resist",
   "kind": "A real trade-off",
   "body": ["Vectorising <code>sum += a[i]</code> requires splitting the sum "
            "into 8 partial sums and combining at the end — which "
            "<i>reassociates</i> the additions.",
            "Floating-point addition is not associative: "
            "(a+b)+c ≠ a+(b+c) in general. So the vectorised result "
            "differs, usually in the last bits.",
            "The compiler will not do this without permission, because "
            "silently changing numerical results is not its decision to make.",
            "<code>-ffast-math</code> grants permission globally and enables "
            "much else besides; <code>#pragma omp simd reduction(+:sum)</code> "
            "grants it for one loop. Prefer the narrow version — and know "
            "that the vectorised sum is usually <i>more</i> accurate, since "
            "partial sums stay smaller."]},

  {"t": "section", "label": "Part 3", "title": "Layout and practice",
   "blurb": "Vectorisation is mostly a data layout problem."},

  {"t": "code", "kicker": "Layout", "title": "SoA is a precondition, not an optimisation",
   "lang": "c", "code": """
// AoS: x values are 32 bytes apart. A vector load needs a GATHER,
// which is slow, or 8 separate loads plus shuffles.
struct P { float x,y,z, vx,vy,vz; int id; float m; };
P p[N];
for (i...) p[i].x += p[i].vx * dt;        // poor vectorisation

// SoA: x values are contiguous. One aligned 256-bit load gets 8.
struct Ps { float x[N], ..., vx[N], ...; };
for (i...) P.x[i] += P.vx[i] * dt;        // vectorises perfectly
""",
   "caption": "Module 06 argued for SoA on cache grounds. Vectorisation is "
              "the second, independent argument, and often the larger one.",
   "note": "Two independent reasons converging on the same layout decision is "
           "worth pointing out explicitly."},

  {"t": "bullets", "kicker": "Method", "title": "How to approach vectorisation",
   "items": [
     "<b>1. Check whether it already vectorised.</b> Compiler reports "
     "(<code>-fopt-info-vec</code>) or read the assembly.",
     "",
     "<b>2. If not, find out why.</b> The compiler will usually tell you with "
     "<code>-fopt-info-vec-missed</code>.",
     "",
     "<b>3. Remove the blocker.</b> <code>restrict</code>, inlining, layout "
     "change, pragma.",
     "",
     "<b>4. Only then consider intrinsics.</b> They are unportable, verbose, "
     "and hard to maintain.",
     "",
     "<b>5. Measure.</b> If the loop is memory-bound, vectorising the "
     "arithmetic changes nothing.",
   ],
   "footnote": "Point 5 is the one people skip. 8× the arithmetic on a "
               "bandwidth-limited loop is 0× the speedup."},

  {"t": "callout", "title": "Vectorising a memory-bound loop does nothing",
   "kind": "The common disappointment",
   "body": ["SIMD multiplies <i>arithmetic</i> throughput. If the loop is "
            "waiting on memory, there was never an arithmetic shortage.",
            "<b>Check first:</b> compute the arithmetic intensity — "
            "operations per byte loaded. Below roughly 1 flop/byte you are "
            "almost certainly bandwidth-bound and SIMD will not help.",
            "This is why Module 06 comes before Module 09. Fix the memory "
            "behaviour, then vectorise what remains.",
            "The exception: SIMD loads also move more bytes per instruction, "
            "so there is sometimes a modest benefit even when bandwidth-"
            "bound. Modest, not 8×."]},

  {"t": "table", "kicker": "Perspective", "title": "SIMD and the courses around it",
   "header": ["Where", "Connection"],
   "widths": [3.6, 8.5],
   "rows": [
     ["CSCE 641", "Shaders are SIMD. A GPU warp is 32-wide SIMD with a nicer programming model"],
     ["CSCE 735", "SIMD is the finest-grained level of the parallelism hierarchy"],
     ["Module 10", "GPUs take this idea much further — next module"],
     ["Module 06", "SoA layout is required for both cache and vector efficiency"],
   ]},
 ],
 "takeaways": [
   "SIMD amortises instruction overhead across 4, 8, or 16 elements. AVX2 at "
   "256 bits is the practical default.",
   "Pointer aliasing is the most common vectorisation blocker, and "
   "<code>restrict</code> is an unchecked promise that fixes it.",
   "Floating-point reductions resist vectorisation because reassociation "
   "changes results. Grant permission per loop, not globally.",
   "Struct-of-arrays is a precondition for good vectorisation, not merely a "
   "cache optimisation — two independent arguments, same conclusion.",
   "Let the compiler vectorise; reach for intrinsics only after removing "
   "blockers and measuring.",
   "Vectorising a memory-bound loop achieves nothing. Check arithmetic "
   "intensity first.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Single instruction, multiple data"),
  ("p", "A scalar add instruction performs one addition and costs a fetch, a "
        "decode, and a slot in the execution pipeline. A vector add performs "
        "eight additions for the same overhead. The arithmetic units are "
        "wider, but the control overhead is unchanged — which is why "
        "SIMD is such an efficient way to add throughput."),
  ("table", ["Extension", "Register width", "Floats per op", "Availability"],
   [["SSE/SSE2", "128-bit", "4", "Every x86-64 processor. Baseline."],
    ["AVX / AVX2", "256-bit", "8",
     "Essentially universal since ~2013. The practical default target."],
    ["AVX-512", "512-bit", "16",
     "Server and some desktop parts. Historically triggered clock reduction, "
     "which could make it a net loss for short vectorised sections."],
    ["NEON", "128-bit", "4", "Every ARM64 processor. Baseline."],
    ["SVE / SVE2", "Scalable (128&ndash;2048)", "Varies",
     "ARM's width-agnostic design: the same binary adapts to the hardware's "
     "actual width, avoiding recompilation per target."]],
   [0.17, 0.22, 0.17, 0.44]),

  ("h1", "2 &nbsp; What prevents vectorisation"),
  ("p", "Compilers vectorise automatically and do it well. When they fail, "
        "there is almost always a specific, identifiable reason, and the "
        "compiler will usually tell you what it is."),
  ("table", ["Blocker", "Why it blocks", "Remedy"],
   [["<b>Pointer aliasing</b>",
     "The compiler cannot prove the output array does not overlap an input. "
     "If they overlapped, processing eight elements at once would produce a "
     "different result than processing them one at a time.",
     "<code>restrict</code> (C) or <code>__restrict</code> (C++). This is by "
     "far the most common blocker and the cheapest fix."],
    ["<b>Loop-carried dependence</b>",
     "Iteration i needs a value produced by iteration i&minus;1.",
     "Often unavoidable. Sometimes the loop can be restructured, or the "
     "dependence confined to a scalar prologue."],
    ["<b>Floating-point reduction</b>",
     "Vectorising requires reassociating additions, which changes the result.",
     "<code>#pragma omp simd reduction(+:sum)</code> for one loop, or "
     "<code>-ffast-math</code> globally. See &sect;2.2."],
    ["<b>Branches in the loop body</b>",
     "Different lanes would need different control flow.",
     "Convert to branchless arithmetic or masked operations, which modern "
     "compilers often do automatically."],
    ["<b>Non-unit stride</b>",
     "Elements are not contiguous, so a vector load would require a gather "
     "— slow where supported at all.",
     "<b>Change the data layout</b> (&sect;3). This is usually the real fix."],
    ["<b>Opaque function calls</b>",
     "The compiler cannot vectorise across a call it cannot see into.",
     "Make the definition visible so it can be inlined."]],
   [0.19, 0.40, 0.41]),
  ("h2", "2.1 &nbsp; Aliasing"),
  ("code", """// Does NOT vectorise: c might overlap a or b
void add(float* c, float* a, float* b, int n) {
    for (int i = 0; i < n; i++) c[i] = a[i] + b[i];
}

// Vectorises: restrict promises no overlap
void add(float* restrict c, float* restrict a,
         float* restrict b, int n) {
    for (int i = 0; i < n; i++) c[i] = a[i] + b[i];
}"""),
  ("callout", "restrict is an unchecked promise",
   ["The compiler does not verify it; it simply trusts you and optimises "
    "accordingly. If the pointers do overlap, the behaviour is undefined and "
    "the symptom is typically silent data corruption that depends on "
    "optimisation level.",
    "Use it where you genuinely know the arrays are distinct, which in "
    "practice is most numerical kernels. Do not scatter it hopefully."]),
  ("h2", "2.2 &nbsp; Floating-point reductions"),
  ("p", "Summing an array into a single accumulator is a loop-carried "
        "dependence. Vectorising it means keeping eight partial sums and "
        "combining them at the end, which reassociates the additions."),
  ("eq", "(a + b) + c &nbsp;&ne;&nbsp; a + (b + c) &nbsp;&nbsp; in floating point"),
  ("p", "The results differ, usually in the last bits. A compiler will not "
        "make that change without permission, because silently altering "
        "numerical output is not a decision it is entitled to make."),
  ("p", "Worth knowing: the vectorised sum is usually <i>more</i> accurate "
        "than the sequential one, because eight partial sums each stay "
        "smaller and therefore lose less precision when adding small values "
        "to a large running total. The compiler's caution is about "
        "<i>reproducibility</i>, not accuracy."),
  ("p", "Prefer the narrow grant — <code>#pragma omp simd "
        "reduction(+:sum)</code> on the specific loop — over "
        "<code>-ffast-math</code>, which also enables assuming no NaNs and no "
        "infinities, among other things that can break code in surprising "
        "ways."),

  ("break",),
  ("h1", "3 &nbsp; Layout determines vectorisability"),
  ("code", """// Array of structs: x values 32 bytes apart
struct P { float x,y,z, vx,vy,vz; int id; float m; };
P p[N];
for (i...) p[i].x += p[i].vx * dt;

// Struct of arrays: x values contiguous
struct Ps { float x[N], y[N], z[N], vx[N], vy[N], vz[N]; };
for (i...) P.x[i] += P.vx[i] * dt;"""),
  ("p", "In the AoS version, the eight <code>x</code> values a vector "
        "register needs are scattered 32 bytes apart. Loading them requires "
        "either a gather instruction — which is available on recent "
        "hardware but far slower than a contiguous load — or eight "
        "separate loads followed by shuffle instructions to assemble the "
        "register. Either way most of the benefit evaporates."),
  ("p", "In the SoA version a single aligned 256-bit load fetches all eight "
        "values. The loop vectorises cleanly and runs at close to the "
        "theoretical speedup."),
  ("callout", "Two independent arguments, one conclusion",
   ["Module 06 argued for struct-of-arrays on cache grounds: you fetch only "
    "the bytes you use.",
    "This module argues for it on vectorisation grounds: contiguous values "
    "load into vector registers in one instruction.",
    "These are genuinely independent arguments, and they compound. A loop "
    "converted from AoS to SoA frequently gains more than either effect alone "
    "would predict, which is a good reason to treat layout as the first thing "
    "to examine rather than the last."]),

  ("h1", "4 &nbsp; A working method"),
  ("ol", ["<b>Check whether it already vectorised.</b> "
          "<code>-fopt-info-vec</code> (GCC) or <code>-Rpass=loop-vectorize</code> "
          "(Clang) will report. Or read the assembly on Compiler Explorer and "
          "look for <code>ymm</code> registers.",
          "<b>If it did not, find out why.</b> "
          "<code>-fopt-info-vec-missed</code> usually names the reason "
          "directly — compilers are better at explaining this than most "
          "people expect.",
          "<b>Remove the blocker.</b> Add <code>restrict</code>, make "
          "functions inlinable, change the layout, or grant reduction "
          "permission.",
          "<b>Only then consider intrinsics.</b> They are unportable, verbose, "
          "and must be maintained against each instruction-set target. Modern "
          "auto-vectorisation is good; reach past it only when you have "
          "measured that it is not good enough here.",
          "<b>Measure.</b> Always."]),
  ("callout", "Why step 5 matters more than the others",
   ["SIMD multiplies <i>arithmetic</i> throughput. If the loop is waiting on "
    "memory, there was no arithmetic shortage to relieve.",
    "Compute the <b>arithmetic intensity</b>: floating-point operations per "
    "byte loaded from memory. Below roughly 1 flop/byte, the loop is almost "
    "certainly bandwidth-bound, and vectorising the arithmetic will produce "
    "no measurable change — a result that surprises people who have just "
    "spent a day writing intrinsics.",
    "This is precisely why Module 06 precedes Module 09. Fix memory "
    "behaviour first; vectorise what remains.",
    "The partial exception: vector loads also move more bytes per "
    "instruction, so there can be a modest gain even when bandwidth-bound. "
    "Modest meaning perhaps 10&ndash;20%, not 8&times;."]),

  ("h1", "5 &nbsp; Connections"),
  ("table", ["Elsewhere", "Relationship"],
   [["<b>CSCE 641</b>",
     "Fragment and vertex shaders are SIMD programs. A GPU warp is 32-wide "
     "SIMD with a programming model that hides the width — which is why "
     "divergent branches in a shader cost what they do."],
    ["<b>Module 10</b>",
     "GPUs take data-level parallelism much further, with thousands of "
     "concurrent threads in addition to width."],
    ["<b>CSCE 735</b>",
     "SIMD is the finest grain in the parallelism hierarchy: vector lanes, "
     "then cores, then sockets, then nodes. Each level has its own cost "
     "model."],
    ["<b>Module 06</b>",
     "SoA layout is required for both cache efficiency and vectorisability. "
     "Do it once, benefit twice."]],
   [0.17, 0.83]),
 ],
 "resources": [
   ("Agner Fog — Optimizing subroutines in assembly language",
    "https://www.agner.org/optimize/",
    "The reference for vector instruction selection, latencies, and "
    "throughputs."),
   ("Intel Intrinsics Guide",
    "https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html",
    "Searchable reference for every intrinsic, with latency and throughput "
    "per microarchitecture."),
   ("Onur Mutlu — SIMD Processing lectures",
    "https://safari.ethz.ch/architecture/",
    "Vector processors and SIMD from the architectural side, including the "
    "historical vector supercomputers."),
   ("Mike Acton — Data-Oriented Design and C++ (free video)",
    "https://www.youtube.com/watch?v=rX0ItVEVjHc",
    "Why layout decisions dominate, argued from shipped game engine "
    "experience."),
 ],
 "exercises": [
   "Write a simple elementwise loop without <code>restrict</code> and confirm "
   "with compiler reports that it does not vectorise. Add "
   "<code>restrict</code> and measure the speedup.",
   "Write a sum reduction and confirm it does not vectorise by default. "
   "Enable it with a pragma, then compare the numerical results against the "
   "scalar version and against a high-precision reference. Which is more "
   "accurate?",
   "Convert a particle update from AoS to SoA. Measure the speedup and "
   "determine how much comes from cache behaviour and how much from "
   "vectorisation, by testing an SoA version with vectorisation disabled.",
   "Compute the arithmetic intensity of three loops of your own. Predict "
   "which will benefit from vectorisation, then measure and check.",
   "Write a kernel with intrinsics and compare it against the "
   "auto-vectorised version. Report whether the extra effort paid.",
   "Write a loop with a data-dependent branch inside and examine whether the "
   "compiler vectorises it with masking. Compare against a branchless "
   "rewrite.",
 ],
 "selfcheck": [
   "What does SIMD amortise, and why does that make it efficient?",
   "Name four things that block auto-vectorisation.",
   "What does <code>restrict</code> promise, and what happens if you lie?",
   "Why will a compiler not vectorise a floating-point reduction by default, "
   "and is the vectorised result less accurate?",
   "Give both reasons SoA beats AoS, and say why they are independent.",
   "You vectorise a loop and nothing gets faster. What is the most likely "
   "explanation and how would you confirm it?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "GPUs as Throughput Machines",
 "subtitle": "A different answer to the same memory problem.",
 "question": "Why is a GPU fast at graphics and bad at pointer chasing?",
 "outcomes": [
     "Contrast latency-oriented and throughput-oriented design.",
     "Explain SIMT execution and warp divergence.",
     "Explain memory coalescing and its importance.",
     "Explain occupancy and what limits it.",
     "Decide whether a workload suits a GPU.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two philosophies",
   "blurb": "The same memory wall, answered in opposite ways."},

  {"t": "two", "kicker": "Design", "title": "Hide latency, or tolerate it",
   "lh": "CPU — latency oriented",
   "l": ["Make <b>one</b> thread fast.",
         "Large caches, deep out-of-order windows, branch prediction, "
         "speculation.",
         "Most of the die is control logic and cache.",
         ("Few cores, each enormous.", 1),
         ("Good at: everything, including irregular work.", 1)],
   "rh": "GPU — throughput oriented",
   "r": ["Make <b>many</b> threads collectively fast.",
         "Small caches, in-order, no speculation.",
         "Most of the die is arithmetic units.",
         ("Thousands of threads resident at once.", 1),
         ("Good at: regular, data-parallel work with high arithmetic "
          "intensity.", 1)],
   "note": "Same problem, opposite answers. The CPU avoids the wait; the GPU "
           "finds other work during it."},

  {"t": "callout", "title": "How a GPU hides memory latency",
   "kind": "Key idea",
   "body": ["A CPU hides a cache miss with out-of-order execution: find "
            "independent instructions <i>within one thread</i>. The window is "
            "a few hundred instructions.",
            "A GPU hides it by <b>switching threads</b>. When a warp stalls "
            "on memory, another resident warp issues in the very next cycle. "
            "With 64 warps resident, there is almost always something ready.",
            "Context switching is free because every thread's registers stay "
            "resident — that is what the enormous register file is for.",
            "The consequence: a GPU needs <b>many more threads than cores</b> "
            "to perform well. Under-occupancy is the most common reason GPU "
            "code disappoints."]},

  {"t": "section", "label": "Part 2", "title": "SIMT execution",
   "blurb": "SIMD with a thread-shaped programming model."},

  {"t": "bullets", "kicker": "SIMT", "title": "Warps: 32 threads in lockstep",
   "items": [
     "Threads are grouped into <b>warps</b> of 32 (NVIDIA) or waves of 32/64 "
     "(AMD).",
     "All threads in a warp execute the <b>same instruction</b> each cycle.",
     "",
     "You write scalar per-thread code; the hardware executes it 32 lanes "
     "wide.",
     ("This is SIMD with a far more pleasant programming model.", 1),
     "",
     "<b>Divergence:</b> if threads in a warp take different branches, both "
     "paths execute with inactive lanes masked off.",
     ("Worst case — all 32 take different paths — costs 32×.", 1),
   ],
   "note": "This is exactly Module 07 of CSCE 641. Same mechanism, explained "
           "from the hardware side."},

  {"t": "code", "kicker": "Divergence", "title": "What divergence costs",
   "lang": "c", "code": """
// BAD: threads within a warp diverge every time
if (threadIdx.x % 2 == 0) heavy_a();
else                      heavy_b();
// Both branches execute for the whole warp. Cost = a + b.

// GOOD: divergence occurs at warp granularity
if ((threadIdx.x / 32) % 2 == 0) heavy_a();
else                             heavy_b();
// Each warp takes one path. Cost = max(a, b) per warp.

// BEST: no divergence at all
result = select(cond, value_a, value_b);
""",
   "caption": "Divergence costs nothing if it happens at warp boundaries. "
              "Restructuring so that neighbouring threads agree is often the "
              "single largest GPU optimisation.",
   "note": "The 'divergence at warp granularity is free' point is the "
           "actionable one, and it is often missed."},

  {"t": "section", "label": "Part 3", "title": "Memory",
   "blurb": "Coalescing is the single most important GPU optimisation."},

  {"t": "code", "kicker": "Coalescing", "title": "Neighbouring threads must touch neighbouring addresses",
   "lang": "c", "code": """
// COALESCED: thread i reads element i.
// 32 consecutive floats = 128 bytes = ONE memory transaction.
float v = data[blockIdx.x * blockDim.x + threadIdx.x];

// UNCOALESCED: thread i reads element i*32.
// 32 separate transactions, each using 4 of 128 bytes fetched.
float v = data[(blockIdx.x * blockDim.x + threadIdx.x) * 32];
//  -> 32x the memory traffic for the same data

// This is Module 06's stride problem, with a 32x penalty
// instead of a 16x one.
""",
   "caption": "The GPU fetches memory in wide transactions. If a warp's 32 "
              "threads touch 32 scattered addresses, you pay 32 transactions "
              "and use a fraction of each.",
   "note": "Coalescing is to GPUs what cache line utilisation is to CPUs — "
           "same principle, harsher penalty."},

  {"t": "table", "kicker": "Memory spaces", "title": "The GPU memory hierarchy",
   "header": ["Space", "Scope", "Latency", "Use for"],
   "widths": [2.6, 2.8, 2.6, 4.1],
   "rows": [
     ["Registers", "One thread", "~0", "Everything you can"],
     ["Shared / LDS", "Thread block", "~20 cyc", "Explicit tiling"],
     ["L1 / texture", "SM", "~30 cyc", "Automatic caching"],
     ["L2", "Device", "~200 cyc", "Automatic"],
     ["Global (VRAM)", "Device", "~400–600 cyc", "Bulk data"],
   ],
   "note": "Shared memory is the interesting one: a programmer-managed cache, "
           "which is how blocking (Module 06) is done explicitly on a GPU."},

  {"t": "bullets", "kicker": "Occupancy", "title": "Keeping enough warps resident",
   "items": [
     "<b>Occupancy</b> = resident warps / maximum possible.",
     "",
     "Limited by whichever runs out first:",
     ("<b>Registers</b> — a register-hungry kernel allows fewer "
      "threads.", 1),
     ("<b>Shared memory</b> — a block using a lot allows fewer blocks.", 1),
     ("<b>Block size</b> — too small wastes scheduling slots.", 1),
     "",
     "Higher occupancy means more warps available to hide latency.",
     "",
     "But <b>higher is not always better</b> — a kernel with high "
     "arithmetic intensity may do better with more registers and fewer warps.",
   ],
   "footnote": "Occupancy is a means to latency hiding, not a goal in itself."},

  {"t": "table", "kicker": "Judgement", "title": "Does this workload suit a GPU?",
   "header": ["Suits a GPU", "Suits a CPU"],
   "widths": [6.0, 6.1],
   "rows": [
     ["Thousands of independent work items", "Few threads, or heavy inter-dependence"],
     ["Regular, predictable memory access", "Pointer chasing, irregular structures"],
     ["High arithmetic intensity", "Low intensity — PCIe transfer dominates"],
     ["Little divergence", "Heavily data-dependent control flow"],
     ["Data already on the device", "Data must round-trip over PCIe"],
   ],
   "note": "The transfer cost is the one that kills otherwise-suitable "
           "workloads. Always count it."},

  {"t": "callout", "title": "Count the transfer", "kind": "The usual mistake",
   "body": ["PCIe gives roughly 16–32 GB/s. GPU memory gives 500–1000 "
            "GB/s.",
            "So moving data to the device and back can cost far more than the "
            "computation saves. A kernel that is 50× faster is worthless "
            "if the transfer takes 100× the kernel time.",
            "<b>Rule:</b> the arithmetic per byte transferred must be high, or "
            "the data must already live on the device and stay there.",
            "This is why graphics works so well: the vertex and texture data "
            "lives in VRAM permanently and is used every frame. It is also "
            "why many 'GPU-accelerated' library calls disappoint."]},
 ],
 "takeaways": [
   "CPUs hide latency within one thread; GPUs tolerate it by switching among "
   "thousands. Same memory wall, opposite answers.",
   "Context switching is free on a GPU because every resident thread's "
   "registers stay in place — hence the enormous register file.",
   "SIMT is SIMD with a per-thread programming model. Warp divergence "
   "executes both paths, costing up to 32×.",
   "Divergence at warp granularity is free. Restructuring so neighbouring "
   "threads agree is often the biggest win.",
   "Coalescing is Module 06's stride problem with a 32× penalty: "
   "neighbouring threads must touch neighbouring addresses.",
   "Count the PCIe transfer. A 50× kernel is worthless if moving the "
   "data costs more than the computation saves.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two answers to one problem"),
  ("p", "CPUs and GPUs face the same memory wall from Module 05 and respond "
        "in opposite ways. Understanding the two philosophies explains almost "
        "every difference between them."),
  ("table", ["", "CPU — latency oriented", "GPU — throughput oriented"],
   [["Goal", "Minimise the time for one thread to finish.",
     "Maximise total work completed per unit time."],
    ["Die area", "Mostly cache and control logic: branch predictors, "
     "schedulers, reorder buffers.",
     "Mostly arithmetic units and register file."],
    ["Latency strategy", "Avoid it (large caches) or hide it within one "
     "thread (out-of-order execution).",
     "Tolerate it by switching to another of thousands of resident threads."],
    ["Threads", "A handful per core.",
     "Thousands per SM; tens of thousands per device."],
    ["Strong at", "Anything, including irregular and branchy work.",
     "Regular data-parallel work with high arithmetic intensity."]],
   [0.14, 0.43, 0.43]),
  ("callout", "The mechanism that makes it work",
   ["When a GPU warp issues a memory request and stalls, the scheduler issues "
    "a different resident warp on the very next cycle. With 64 warps resident "
    "on a streaming multiprocessor, something is almost always ready.",
    "This is only possible because switching is <b>free</b>: every resident "
    "thread's registers remain allocated, so there is no state to save or "
    "restore. That is what the enormous register file — 256 KB per SM is "
    "typical — is for.",
    "The direct consequence is that a GPU requires <i>far more threads than "
    "it has cores</i> to perform well. Launching a kernel with too little "
    "parallelism leaves the latency unhidden and is the most common reason "
    "GPU code underperforms."]),

  ("h1", "2 &nbsp; SIMT"),
  ("p", "Threads are grouped into <b>warps</b> of 32 (NVIDIA terminology; AMD "
        "calls them waves and uses 32 or 64). Every thread in a warp executes "
        "the same instruction in the same cycle, on its own data."),
  ("p", "You write ordinary scalar code describing what one thread does, and "
        "the hardware executes 32 copies in lockstep. This is SIMD with a "
        "programming model that hides the vector width — considerably "
        "more pleasant to write than the intrinsics of Module 09, at the cost "
        "of a performance model that is less obvious."),
  ("h2", "2.1 &nbsp; Divergence"),
  ("p", "If threads within a warp take different branches, the hardware "
        "executes <i>both</i> paths, masking off the lanes that should not be "
        "active in each. The warp's cost is the sum of the paths, not the "
        "maximum."),
  ("code", """// Divergence within every warp: both paths run for all 32 lanes
if (threadIdx.x % 2 == 0) heavy_a();
else                      heavy_b();          // cost = a + b

// Divergence at warp granularity: each warp takes one path
if ((threadIdx.x / 32) % 2 == 0) heavy_a();
else                             heavy_b();   // cost = max(a, b)"""),
  ("callout", "Divergence at warp boundaries is free",
   ["A branch on which all 32 threads of a warp agree costs nothing — "
    "only one path executes.",
    "So the goal is not to eliminate branches but to arrange that "
    "<i>neighbouring threads agree</i>. Sorting work by branch outcome, or "
    "assigning work so that a warp handles a homogeneous group, routinely "
    "converts a 2&times; penalty into none.",
    "The worst case — all 32 threads taking different paths through a "
    "32-way switch — costs 32&times;. This is the hardware explanation "
    "for the shader branching guidance in CSCE 641 Module 07."]),

  ("break",),
  ("h1", "3 &nbsp; Memory coalescing"),
  ("p", "GPU memory is read in wide transactions — typically 128 bytes. "
        "If the 32 threads of a warp access 32 consecutive 4-byte elements, "
        "that is exactly one transaction, fully used."),
  ("code", """// Coalesced: thread i reads element i
float v = data[blockIdx.x * blockDim.x + threadIdx.x];
//  -> 32 consecutive floats = 128 bytes = one transaction

// Uncoalesced: thread i reads element 32i
float v = data[(blockIdx.x * blockDim.x + threadIdx.x) * 32];
//  -> 32 separate transactions, 4 useful bytes out of 128 each"""),
  ("p", "The uncoalesced version moves 32 times the memory traffic for the "
        "same data. This is Module 06's stride problem with a harsher "
        "penalty, and it is the single most important GPU optimisation: a "
        "kernel with uncoalesced access is frequently an order of magnitude "
        "below its potential, regardless of anything else."),
  ("p", "The practical rule is the same as on the CPU, stated differently: "
        "arrange that consecutive thread indices touch consecutive addresses. "
        "This is yet another argument for struct-of-arrays layout, and it is "
        "why GPU code is written that way almost without exception."),
  ("h2", "3.1 &nbsp; The memory spaces"),
  ("table", ["Space", "Scope", "Latency", "Managed by"],
   [["Registers", "One thread", "~0", "Compiler. Use as many as occupancy "
     "allows."],
    ["Shared memory / LDS", "A thread block", "~20 cycles",
     "<b>You.</b> A programmer-managed cache — this is how the blocking "
     "of Module 06 is done explicitly."],
    ["L1 / texture cache", "One SM", "~30 cycles", "Hardware."],
    ["L2", "The whole device", "~200 cycles", "Hardware."],
    ["Global memory (VRAM)", "The whole device", "400&ndash;600 cycles",
     "You, through allocation and access pattern."]],
   [0.20, 0.17, 0.17, 0.46]),
  ("p", "Shared memory is the distinctive one. It is a small, fast, "
        "explicitly managed scratchpad shared by a thread block, and using it "
        "well is essentially the blocking transformation of Module 06 "
        "performed by hand: load a tile cooperatively, synchronise, compute "
        "against the tile repeatedly, move on."),

  ("h1", "4 &nbsp; Occupancy"),
  ("eq", "occupancy = resident warps / maximum resident warps"),
  ("p", "Occupancy determines how many warps are available to hide latency. "
        "It is limited by whichever resource is exhausted first:"),
  ("ul", ["<b>Registers per thread.</b> A kernel using many registers allows "
          "fewer resident threads, since the register file is fixed.",
          "<b>Shared memory per block.</b> A block claiming a large "
          "allocation allows fewer blocks per SM.",
          "<b>Block size.</b> Blocks that are too small waste scheduling "
          "slots; typical good values are 128&ndash;256 threads."]),
  ("callout", "Higher occupancy is not automatically better",
   ["Occupancy is a means to latency hiding, not an end. A kernel with high "
    "arithmetic intensity and few memory accesses has little latency to hide, "
    "and may perform better with more registers per thread and lower "
    "occupancy.",
    "The quantity to optimise is throughput. Occupancy is one input to it, "
    "and tuning occupancy without measuring throughput is a classic way to "
    "spend a day for nothing."]),

  ("h1", "5 &nbsp; Is this workload a GPU workload?"),
  ("table", ["Favours GPU", "Favours CPU"],
   [["Thousands of independent work items",
     "Few threads, or heavy dependence between them"],
    ["Regular, predictable memory access",
     "Pointer chasing, trees, irregular graphs"],
    ["High arithmetic intensity (many ops per byte)",
     "Low intensity — transfer cost dominates"],
    ["Little or warp-aligned divergence",
     "Heavily data-dependent control flow"],
    ["Data already resident on the device",
     "Data must round-trip across PCIe for each call"]],
   [0.5, 0.5]),
  ("callout", "Always count the transfer",
   ["PCIe delivers roughly 16&ndash;32 GB/s. GPU memory delivers "
    "500&ndash;1000 GB/s. Moving data to the device and back is therefore "
    "slow relative to everything the device does once the data is there.",
    "A kernel that runs 50&times; faster than the CPU version is worthless if "
    "the transfer takes a hundred times the kernel's runtime. Many "
    "disappointing 'GPU-accelerated' library functions are exactly this.",
    "The requirement is that arithmetic per transferred byte be high, or that "
    "the data live on the device across many operations.",
    "This is precisely why real-time graphics suits GPUs so well: vertex "
    "buffers, textures, and render targets live in VRAM permanently and are "
    "used every frame. The transfer was paid once, at load time."]),
 ],
 "resources": [
   ("NVIDIA CUDA C++ Programming Guide",
    "https://web.archive.org/web/20260911074013/https://docs.nvidia.com/cuda/cuda-c-programming-guide/",
    "The authoritative reference. Chapters on the execution model and memory "
    "coalescing are the ones that matter here."),
   ("OLCF CUDA Training Series (free video + exercises)",
    "https://www.olcf.ornl.gov/cuda-training-series/",
    "A structured free course with hands-on labs. The best guided "
    "introduction available."),
   ("Onur Mutlu — GPUs and SIMT lectures",
    "https://safari.ethz.ch/architecture/",
    "The architectural view, with the latency-hiding argument developed "
    "properly."),
   ("CMU 15-418 / Stanford CS149 — GPU architecture lectures",
    "http://www.cs.cmu.edu/~418/",
    "Kayvon Fatahalian's treatment, which is unusually good at explaining "
    "<i>why</i> GPUs are shaped the way they are. Also the basis of "
    "CSCE 735."),
 ],
 "exercises": [
   "Write a CUDA (or OpenCL, or compute shader) kernel for vector addition "
   "and measure its bandwidth. Compare against the device's theoretical peak "
   "and account for the gap.",
   "Write coalesced and uncoalesced versions of the same kernel. Measure both "
   "and confirm the ratio is close to the transaction-size argument.",
   "Demonstrate warp divergence: write a kernel that branches on "
   "<code>threadIdx.x % 2</code> and one that branches on "
   "<code>threadIdx.x / 32</code>. Measure both.",
   "Implement tiled matrix multiplication using shared memory. Compare "
   "against the naive version, and relate the structure to the CPU blocking "
   "of Module 06.",
   "Vary registers per thread (via <code>__launch_bounds__</code> or just by "
   "adding live variables) and plot occupancy against achieved throughput. "
   "Find a case where lower occupancy is faster.",
   "Measure PCIe transfer bandwidth and compute, for a kernel of your choice, "
   "the minimum arithmetic intensity at which GPU execution beats CPU "
   "execution including transfer.",
 ],
 "selfcheck": [
   "How does a CPU hide memory latency, and how does a GPU? Why can the GPU "
   "switch threads for free?",
   "What is a warp, and what happens when threads in one diverge?",
   "Why is divergence at warp granularity free?",
   "What is memory coalescing, and what does uncoalesced access cost?",
   "What is shared memory for, and which CPU optimisation does using it "
   "correspond to?",
   "Why is higher occupancy not always better?",
   "Give the condition under which moving a computation to a GPU is worth the "
   "transfer cost.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Multicore and Cache Coherence",
 "subtitle": "Many caches, one memory, and the protocol that reconciles them.",
 "question": "How do several cores agree on what memory contains?",
 "outcomes": [
     "Explain why coherence is needed and what it guarantees.",
     "Describe the MESI protocol states and transitions.",
     "Explain false sharing and detect it.",
     "Explain why atomic operations cost what they do.",
     "Explain NUMA and its implications for data placement.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "Private caches plus shared memory equals disagreement."},

  {"t": "code", "kicker": "The problem", "title": "Two cores, two answers",
   "lang": "text", "code": """
Initially x = 0 in memory.

Core 0                      Core 1
  load x    -> cache has 0    load x    -> cache has 0
  x = 1     -> cache has 1
                              load x    -> still reads 0 from ITS cache

Core 1 is reading stale data. Without a protocol, nothing
prevents this -- each core's cache is private and neither
knows the other exists.

COHERENCE: a read must return the most recent write.
""",
   "caption": "Coherence is about a <i>single</i> location seen consistently. "
              "Consistency — the ordering of operations across several "
              "locations — is a separate and harder problem (Module 12).",
   "note": "Students conflate coherence and consistency constantly. "
           "Distinguish them early and repeat it."},

  {"t": "section", "label": "Part 2", "title": "MESI",
   "blurb": "Four states per cache line, and a protocol to move between them."},

  {"t": "table", "kicker": "MESI", "title": "The four states",
   "header": ["State", "Means", "Other caches", "Memory"],
   "widths": [2.4, 4.2, 2.8, 2.7],
   "rows": [
     ["<b>M</b>odified", "I have it and have changed it", "None have it", "Stale"],
     ["<b>E</b>xclusive", "I have it, unchanged, alone", "None have it", "Current"],
     ["<b>S</b>hared", "I have it, read-only", "Others may have it", "Current"],
     ["<b>I</b>nvalid", "I do not have it", "—", "—"],
   ],
   "note": "The E state is the useful optimisation: a write to an E line "
           "needs no bus traffic at all."},

  {"t": "bullets", "kicker": "MESI", "title": "How it behaves",
   "items": [
     "<b>Read miss:</b> fetch the line. If nobody else has it → "
     "<b>E</b>; if others do → <b>S</b> for everyone.",
     "",
     "<b>Write to S:</b> broadcast an invalidate; all other copies → "
     "<b>I</b>; mine → <b>M</b>.",
     "",
     "<b>Write to E:</b> silently → <b>M</b>. No traffic at all.",
     ("This is why E exists — private data is written without any bus "
      "transaction.", 1),
     "",
     "<b>Another core reads my M line:</b> I supply it and drop to <b>S</b>.",
     "",
     "Enforced by snooping on a bus, or by a directory at scale.",
   ]},

  {"t": "section", "label": "Part 3", "title": "False sharing",
   "blurb": "The most common and most invisible parallel performance bug."},

  {"t": "callout", "title": "Coherence operates on lines, not variables",
   "kind": "The bug",
   "body": ["Two threads write to two <i>different</i> variables that happen "
            "to occupy the <b>same 64-byte cache line</b>.",
            "Logically there is no sharing. The hardware cannot tell: it "
            "tracks lines, not variables. Every write invalidates the other "
            "core's copy.",
            "The line ping-pongs between cores on every write. Each access "
            "becomes a coherence miss costing hundreds of cycles.",
            "A parallel program can be <b>slower than the serial version</b> "
            "with perfect logical independence. Nothing in the source "
            "suggests a problem."]},

  {"t": "code", "kicker": "False sharing", "title": "The bug and the fix",
   "lang": "c", "code": """
// BAD: counters[0..7] share one or two cache lines
long counters[8];
// thread i:  counters[i]++;        <- ping-pongs constantly

// GOOD: pad each to its own line
struct alignas(64) Counter { long v; char pad[56]; };
Counter counters[8];
// thread i:  counters[i].v++;      <- no sharing at all

// BETTER: accumulate locally, combine at the end
long local = 0;
for (...) local++;                  // in a register
counters[tid].v = local;            // ONE write at the end
""",
   "caption": "The third version is usually best: it avoids both false "
              "sharing and the coherence traffic of frequent writes to "
              "shared lines.",
   "note": "The local-accumulation pattern generalises: minimise writes to "
           "any line another core touches."},

  {"t": "section", "label": "Part 4", "title": "Atomics and NUMA",
   "blurb": "What synchronisation costs, and where memory actually lives."},

  {"t": "bullets", "kicker": "Atomics", "title": "Why atomic operations are expensive",
   "items": [
     "An atomic read-modify-write must obtain the line in <b>M</b> state "
     "exclusively.",
     "",
     "Under contention, that line moves between cores constantly.",
     ("Uncontended atomic: ~20 cycles.", 1),
     ("Contended atomic: 100–500+ cycles, and worse with more cores.", 1),
     "",
     "<b>Atomics do not scale.</b> A single contended counter is a "
     "bottleneck at any core count.",
     "",
     "Fix: per-thread counters combined at the end — the same pattern as "
     "the false-sharing fix.",
   ],
   "note": "The scaling point matters: adding cores to a contended-atomic "
           "workload makes it slower, not faster."},

  {"t": "table", "kicker": "NUMA", "title": "Not all memory is equally far",
   "header": ["Access", "Latency", "Bandwidth"],
   "widths": [4.6, 3.6, 3.9],
   "rows": [
     ["Local socket memory", "~90 ns", "Full"],
     ["Remote socket memory", "~140 ns", "Reduced — crosses the interconnect"],
   ],
   "footnote": "Pages are allocated near whichever core first <b>touches</b> "
               "them — not where malloc was called.",
   "note": "First-touch is the practical consequence and the usual bug: "
           "serial initialisation puts everything on one node."},

  {"t": "bullets", "kicker": "Practice", "title": "Writing scalable parallel code",
   "items": [
     "<b>Minimise sharing.</b> Per-thread data combined at the end beats "
     "shared data protected by locks.",
     "<b>Pad shared structures</b> to 64-byte boundaries.",
     "<b>Avoid contended atomics.</b> Accumulate locally; combine once.",
     "<b>Initialise in parallel</b> so NUMA first-touch distributes pages.",
     "<b>Pin threads</b> when it matters, so the OS does not migrate them "
     "away from their data.",
     "",
     "Diagnose with cache-coherence counters, not with guesswork.",
   ],
   "footnote": "A parallel speedup well below the core count almost always "
               "means sharing, not insufficient parallelism."},
 ],
 "takeaways": [
   "Coherence guarantees a read returns the most recent write to <i>one</i> "
   "location. Consistency — ordering across locations — is Module "
   "12.",
   "MESI tracks four states per line. The Exclusive state exists so writes to "
   "private data generate no bus traffic.",
   "False sharing: two threads writing different variables in the same 64-byte "
   "line. Logically independent, physically contended, invisible in source.",
   "A contended atomic costs 100–500+ cycles and gets worse with more "
   "cores. Atomics do not scale.",
   "The fix for both is the same: accumulate per-thread, combine once.",
   "NUMA pages land near the core that first touches them, so parallel "
   "initialisation matters as much as parallel computation.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why coherence is needed"),
  ("p", "Each core has private L1 and usually private L2 caches. They share "
        "main memory. Without a protocol, two cores can hold different values "
        "for the same address and neither will know."),
  ("code", """Initially x = 0.

Core 0                        Core 1
  load  x   -> caches 0         load  x   -> caches 0
  store x=1 -> its cache: 1
                                load  x   -> reads 0 from its own cache"""),
  ("p", "<b>Cache coherence</b> is the guarantee that a read of a location "
        "returns the value of the most recent write to that location, "
        "regardless of which core performed it."),
  ("callout", "Coherence and consistency are different problems",
   ["<b>Coherence</b> concerns a single memory location: all cores must agree "
    "on the sequence of values it took.",
    "<b>Consistency</b> concerns the relative ordering of operations to "
    "<i>different</i> locations: if I write A then B, can another core "
    "observe B before A?",
    "Coherence is handled entirely by hardware and is essentially invisible "
    "except as performance. Consistency is visible, is <i>not</i> what most "
    "programmers assume, and is Module 12. Conflating them is the source of "
    "a great deal of confusion about concurrent code."]),

  ("h1", "2 &nbsp; MESI"),
  ("table", ["State", "Meaning", "Other caches may hold it", "Memory is"],
   [["<b>M</b>odified", "This cache has the only copy and has modified it.",
     "No", "Stale — this cache must write back on eviction."],
    ["<b>E</b>xclusive", "This cache has the only copy, unmodified.", "No",
     "Current."],
    ["<b>S</b>hared", "This cache has a read-only copy.", "Yes", "Current."],
    ["<b>I</b>nvalid", "This cache's copy is not usable.", "&mdash;",
     "&mdash;"]],
   [0.17, 0.35, 0.21, 0.27]),
  ("ul", ["<b>Read miss.</b> Fetch the line. If no other cache holds it, "
          "enter <b>E</b>; otherwise all copies become <b>S</b>.",
          "<b>Write to a Shared line.</b> Broadcast an invalidate; all other "
          "copies become <b>I</b>; this one becomes <b>M</b>.",
          "<b>Write to an Exclusive line.</b> Transition silently to "
          "<b>M</b> — <i>no bus traffic at all</i>.",
          "<b>Another core reads a Modified line.</b> This cache supplies the "
          "data and drops to <b>S</b>; memory is updated."]),
  ("callout", "Why the Exclusive state is worth having",
   ["Without E, a cache could not distinguish 'I am the only holder' from 'I "
    "share this'. Every write would have to broadcast an invalidate just in "
    "case.",
    "With E, writes to genuinely private data — which is most data in "
    "most programs — generate no coherence traffic whatsoever. The state "
    "exists purely as an optimisation for the common case, and it is a large "
    "one."]),
  ("p", "Coherence is enforced by <b>snooping</b> (every cache watches a "
        "shared bus) in small systems, and by a <b>directory</b> (a central "
        "record of which caches hold which lines) in larger ones, since "
        "broadcasting does not scale past a handful of cores."),

  ("break",),
  ("h1", "3 &nbsp; False sharing"),
  ("callout", "The defining property: coherence tracks lines, not variables",
   ["Two threads write to two entirely different variables. Those variables "
    "happen to lie within the same 64-byte cache line.",
    "There is no logical sharing whatsoever. The hardware has no way to know "
    "that — its unit of coherence is the line. Every write by one thread "
    "invalidates the other thread's copy of the line.",
    "The line now moves between cores on every single write, and each access "
    "becomes a coherence miss costing hundreds of cycles.",
    "The result is a parallel program that can be <b>slower than its serial "
    "equivalent</b> while being perfectly correct and perfectly independent "
    "in the source. Nothing in the code suggests a problem, which is what "
    "makes this the most insidious bug in parallel programming."]),
  ("code", """// BAD -- all eight counters occupy one or two cache lines
long counters[8];
// thread i: counters[i]++;

// PADDED -- each counter gets its own line
struct alignas(64) Counter { long v; char pad[56]; };
Counter counters[8];

// BEST -- accumulate in a register, write once
long local = 0;
for (...) local++;
counters[tid].v = local;"""),
  ("p", "The third form is generally preferable. Padding removes the false "
        "sharing but still writes to memory on every iteration; local "
        "accumulation keeps the hot variable in a register and touches shared "
        "memory exactly once. The general principle is to minimise writes to "
        "any line another core might touch."),
  ("p", "<b>Detection:</b> a parallel speedup far below the core count with "
        "no obvious lock contention. Confirm with hardware counters for "
        "coherence misses (<code>perf c2c</code> on Linux is purpose-built "
        "for this and will name the offending cache line)."),

  ("h1", "4 &nbsp; Atomics"),
  ("p", "An atomic read-modify-write must acquire the cache line in "
        "<b>Modified</b> state exclusively, perform the operation, and hold it "
        "until complete. Under contention, the line is pulled back and forth "
        "between cores continuously."),
  ("table", ["Situation", "Typical cost"],
   [["Uncontended atomic increment (line already M)", "~20 cycles"],
    ["Lightly contended (2&ndash;4 cores)", "100&ndash;200 cycles"],
    ["Heavily contended (many cores)", "500+ cycles, worsening with core "
     "count"]],
   [0.5, 0.5]),
  ("callout", "Atomics do not scale",
   ["A single contended counter is a serialisation point. Adding cores makes "
    "it <i>worse</i>, because more cores compete for the same line and each "
    "transfer costs more as the interconnect grows.",
    "This is one of the most common reasons a parallel program fails to scale "
    "while appearing to have ample parallelism.",
    "The remedy is the same as for false sharing: give each thread its own "
    "counter, accumulate locally, and combine once at the end. The cost drops "
    "from O(operations) coherence transfers to O(threads)."]),

  ("h1", "5 &nbsp; NUMA"),
  ("p", "On a multi-socket system, each processor has memory attached "
        "directly to it. Accessing another socket's memory traverses an "
        "interconnect."),
  ("table", ["Access", "Latency", "Bandwidth"],
   [["Local node", "~90 ns", "Full"],
    ["Remote node", "~140 ns", "Reduced, and shared with coherence traffic"]],
   [0.34, 0.33, 0.33]),
  ("p", "As Module 07 established, a physical page is allocated on the node "
        "of whichever core <b>first touches</b> it — not where "
        "<code>malloc</code> was called. The practical consequence is "
        "important and routinely missed:"),
  ("callout", "Initialise in parallel",
   ["Allocating a large array and initialising it from a single thread places "
    "every page on that thread's node. Processing it afterwards from all "
    "threads means every other socket pays remote latency for every access, "
    "and the interconnect becomes a bottleneck.",
    "Initialising the array <i>in parallel</i>, with each thread touching the "
    "region it will later process, distributes the pages correctly and can "
    "improve throughput substantially on multi-socket machines.",
    "Pinning threads to cores (<code>numactl</code>, "
    "<code>sched_setaffinity</code>) prevents the scheduler from later "
    "migrating a thread away from its data, which would reintroduce the "
    "problem."]),

  ("h1", "6 &nbsp; Writing code that scales"),
  ("ol", ["<b>Minimise sharing.</b> Per-thread state combined at the end "
          "beats shared state with locks, almost always.",
          "<b>Pad concurrently written structures</b> to 64-byte boundaries, "
          "or use <code>alignas(64)</code>.",
          "<b>Avoid contended atomics</b> in hot paths. Accumulate locally.",
          "<b>Initialise in parallel</b> so NUMA first touch distributes "
          "pages correctly.",
          "<b>Pin threads</b> when data placement matters.",
          "<b>Measure coherence traffic</b> rather than guessing. "
          "<code>perf c2c</code> identifies the exact line and the exact "
          "source locations involved."]),
  ("p", "A parallel speedup substantially below the core count, with no "
        "visible lock contention, is almost always sharing of some kind "
        "— false sharing, atomic contention, or NUMA placement. "
        "Insufficient parallelism is a much rarer explanation than people "
        "assume."),
 ],
 "resources": [
   ("Onur Mutlu — Cache Coherence, Multiprocessors lectures",
    "https://safari.ethz.ch/architecture/",
    "MESI and directory protocols developed properly, with the scaling "
    "arguments."),
   ("Ulrich Drepper — What Every Programmer Should Know About Memory, "
    "section 3.3",
    "https://people.freebsd.org/~lstewart/articles/cpumemory.pdf",
    "Coherence and false sharing with measurements."),
   ("Paul McKenney — Is Parallel Programming Hard? (free book)",
    "https://mirrors.edge.kernel.org/pub/linux/kernel/people/paulmck/perfbook/perfbook.html",
    "The practitioner's treatment of sharing, counters, and scalability. "
    "Chapter 5 on counting is directly relevant and unusually good."),
   ("perf c2c documentation",
    "https://man7.org/linux/man-pages/man1/perf-c2c.1.html",
    "The tool that finds false sharing by cache line and source line."),
 ],
 "exercises": [
   "Write a parallel counter with threads incrementing adjacent array "
   "elements. Measure scaling from 1 to 8 threads and observe it failing. "
   "Then pad to 64 bytes and measure again.",
   "Use <code>perf c2c</code> (or equivalent) to identify the false-sharing "
   "line in the unpadded version, and confirm it names the right source "
   "lines.",
   "Measure the cost of an uncontended atomic increment, then with 2, 4, and "
   "8 threads contending. Plot cost against thread count.",
   "Implement the same counting workload three ways: a single atomic counter, "
   "padded per-thread counters, and local accumulation with a final combine. "
   "Measure all three at several thread counts.",
   "Write a producer-consumer benchmark where producer and consumer write to "
   "adjacent variables, and show the effect of separating them onto different "
   "cache lines.",
   "On a NUMA machine if available: allocate and initialise a large array "
   "serially, then process it in parallel; then initialise in parallel and "
   "repeat. Report the difference and verify page placement with "
   "<code>numastat</code>.",
 ],
 "selfcheck": [
   "What does cache coherence guarantee, and how does it differ from memory "
   "consistency?",
   "Name the four MESI states. Why does the Exclusive state exist?",
   "Explain false sharing and why it is invisible in source code.",
   "Why does a contended atomic get <i>worse</i> as cores are added?",
   "Give the single pattern that fixes both false sharing and atomic "
   "contention.",
   "What is NUMA first touch, and what does it imply about how to initialise "
   "large arrays?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Memory Consistency and Synchronization",
 "subtitle": "Why your multithreaded code does not do what it says.",
 "question": "In what order do other cores see your memory operations?",
 "outcomes": [
     "Explain sequential consistency and why no hardware implements it.",
     "Explain store buffering and the reorderings real hardware permits.",
     "Use memory barriers and acquire/release semantics correctly.",
     "Explain why the compiler reorders too.",
     "Explain why lock-free programming is difficult.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The surprise",
   "blurb": "A program that cannot produce an outcome, producing it."},

  {"t": "code", "kicker": "Dekker", "title": "The result that should be impossible",
   "lang": "c", "code": """
// Initially: x = 0, y = 0

// Thread 1              // Thread 2
x = 1;                   y = 1;
r1 = y;                  r2 = x;

// Reason about all interleavings of a sequential execution:
//   both stores happen before at least one of the loads,
//   so at least one load must see 1.
//   r1 == 0 && r2 == 0 is IMPOSSIBLE.

// On real x86 hardware, r1 == 0 && r2 == 0 HAPPENS.
""",
   "caption": "Not a compiler bug and not a race in the usual sense. The "
              "hardware is behaving as specified — the specification is "
              "just not what you assumed.",
   "note": "Run this. Seeing it happen on real hardware is the only thing "
           "that makes the module stick."},

  {"t": "callout", "title": "Store buffers", "kind": "The explanation",
   "body": ["A store must obtain the cache line in Modified state, which can "
            "take hundreds of cycles. Stalling the core on every store would "
            "be ruinous.",
            "So stores go into a <b>store buffer</b> and the core proceeds "
            "immediately. The store becomes visible to other cores later.",
            "Meanwhile loads may read ahead, from cache or from the local "
            "store buffer.",
            "So Thread 1's store to x may still be sitting in its store "
            "buffer when Thread 2 loads x. Both threads see the old value. "
            "The hardware is correct; sequential reasoning was wrong."]},

  {"t": "section", "label": "Part 2", "title": "Consistency models",
   "blurb": "A contract about what reorderings are permitted."},

  {"t": "table", "kicker": "Models", "title": "What each model allows",
   "header": ["Model", "Reorders", "Found on"],
   "widths": [3.3, 4.6, 4.2],
   "rows": [
     ["Sequential (SC)", "Nothing", "No real hardware"],
     ["TSO", "Store→Load only", "x86-64"],
     ["Weak / relaxed", "Almost anything", "ARM, POWER, RISC-V"],
   ],
   "note": "x86's TSO is relatively strong, which is why code that works on "
           "x86 often breaks on ARM. Test on both."},

  {"t": "callout", "title": "Why weak code works on x86 and breaks on ARM",
   "kind": "A real portability trap",
   "body": ["x86 provides TSO: only store→load reordering is permitted. "
            "A great deal of incorrectly synchronised code happens to work.",
            "ARM and POWER permit store→store, load→load, and "
            "load→store reordering as well. The same code breaks.",
            "This is why a concurrency bug can lie dormant for years and then "
            "appear when a product ships on ARM.",
            "<b>Do not infer correctness from testing.</b> Reason from the "
            "memory model, use the language's atomics, and test on weakly "
            "ordered hardware as well."]},

  {"t": "section", "label": "Part 3", "title": "Barriers and ordering",
   "blurb": "Telling the hardware and the compiler what you require."},

  {"t": "table", "kicker": "Ordering", "title": "Acquire and release",
   "header": ["Operation", "Guarantees", "Use for"],
   "widths": [2.8, 5.2, 4.1],
   "rows": [
     ["acquire (load)", "Nothing after it moves before it", "Taking a lock; reading a flag"],
     ["release (store)", "Nothing before it moves after it", "Releasing a lock; setting a flag"],
     ["acq_rel", "Both", "Read-modify-write"],
     ["seq_cst", "A single global order of all seq_cst ops", "The safe default"],
     ["relaxed", "Atomicity only, no ordering", "Counters you only read at the end"],
   ],
   "note": "Acquire/release is the right mental model: release publishes "
           "everything written before it; acquire sees everything published."},

  {"t": "code", "kicker": "Pattern", "title": "The publish/subscribe idiom",
   "lang": "c", "code": """
// PRODUCER                         // CONSUMER
data = compute();                   while (!ready.load(acquire))
ready.store(true, release);             spin;
                                    use(data);     // guaranteed to see
                                                   // the compute() result

// The release store publishes everything written BEFORE it.
// The acquire load sees everything that was published.
// Together they create a happens-before edge across threads.

// With relaxed ordering, the consumer may see ready == true
// while `data` still holds its old value.
""",
   "caption": "This pairing is the foundation of almost all lock-free code. "
              "Release publishes; acquire subscribes.",
   "note": "If students remember one thing from this module, it should be "
           "this pattern."},

  {"t": "bullets", "kicker": "Compilers too", "title": "The compiler reorders as well",
   "items": [
     "Hardware reordering is only half the problem. Compilers reorder, cache "
     "values in registers, and delete 'redundant' loads.",
     "",
     "A spin loop on a non-atomic variable can be hoisted into an infinite "
     "loop.",
     ("The compiler proves nothing in the loop modifies it — which is "
      "true single-threaded.", 1),
     "",
     "<code>volatile</code> is <b>not</b> a synchronisation primitive in C "
     "or C++.",
     ("It prevents some compiler optimisations. It provides no hardware "
      "ordering and no atomicity.", 1),
     "",
     "Use <code>std::atomic</code> (or C11 <code>_Atomic</code>). It "
     "constrains both compiler and hardware.",
   ],
   "note": "The volatile misconception is extremely common and worth "
           "attacking directly."},

  {"t": "section", "label": "Part 4", "title": "Practice",
   "blurb": "What to actually do."},

  {"t": "table", "kicker": "Costs", "title": "Synchronisation, priced",
   "header": ["Mechanism", "Uncontended", "Contended"],
   "widths": [4.0, 4.0, 4.1],
   "rows": [
     ["Relaxed atomic load", "~1 cycle", "~1 cycle"],
     ["Acquire/release", "~1–20 cycles", "Coherence traffic"],
     ["seq_cst store (x86)", "~20–40 cycles", "Worse"],
     ["Uncontended mutex", "~20 cycles", "—"],
     ["Contended mutex", "—", "~1,000+ (syscall, context switch)"],
   ],
   "note": "An uncontended mutex is cheap. The cost is entirely in "
           "contention, which is an argument for reducing sharing rather "
           "than for avoiding locks."},

  {"t": "bullets", "kicker": "Advice", "title": "How to write correct concurrent code",
   "items": [
     "<b>Use a mutex</b> unless you have measured that it is the problem. "
     "Uncontended locks are cheap and obviously correct.",
     "",
     "<b>Prefer immutability and message passing</b> over shared mutable "
     "state.",
     "",
     "<b>If you must go lock-free:</b> use <code>std::atomic</code> with "
     "explicit ordering, document the reasoning, and test under a race "
     "detector and on ARM.",
     "",
     "<b>Never invent a synchronisation primitive</b> without a proof. This "
     "is one area where cleverness is reliably punished.",
     "",
     "<b>Use tools:</b> ThreadSanitizer, helgrind, stress tests on weak "
     "hardware.",
   ],
   "footnote": "Lock-free code that is subtly wrong usually passes every "
               "test you write for it."},
 ],
 "takeaways": [
   "Dekker's example produces an outcome that sequential reasoning says is "
   "impossible, because store buffers delay visibility.",
   "No real hardware implements sequential consistency. x86 gives TSO; ARM "
   "and POWER are much weaker.",
   "Code that is incorrectly synchronised often works on x86 and fails on "
   "ARM. Do not infer correctness from testing.",
   "Release publishes everything written before it; acquire sees everything "
   "published. That pairing underlies almost all lock-free code.",
   "The compiler reorders too, and <code>volatile</code> is not a "
   "synchronisation primitive. Use <code>std::atomic</code>.",
   "Uncontended mutexes are cheap. Reach for lock-free only after measuring, "
   "and never invent a primitive without a proof.",
 ],
 "notes": [
  ("h1", "1 &nbsp; A result that should be impossible"),
  ("code", """// Initially x = y = 0

// Thread 1          // Thread 2
x = 1;               y = 1;
r1 = y;              r2 = x;"""),
  ("p", "Enumerate the interleavings of a sequentially consistent execution. "
        "Whatever the order, both stores cannot follow both loads, so at "
        "least one load must observe a 1. The outcome r1 = 0 and r2 = 0 is "
        "impossible."),
  ("p", "On real x86 hardware it occurs, reproducibly, within seconds. This "
        "is not a compiler bug and not a data race in the sense a race "
        "detector would flag with proper atomics — the hardware is "
        "behaving exactly as specified. The specification is simply not what "
        "sequential intuition assumes."),
  ("callout", "Store buffers are the explanation",
   ["A store must acquire its cache line in Modified state, which may take "
    "hundreds of cycles under coherence (Module 11). Stalling the core on "
    "every store would be catastrophic for performance.",
    "So stores are placed in a <b>store buffer</b> and the core continues "
    "immediately. The store drains to cache later, becoming visible to other "
    "cores at that point. Meanwhile loads proceed, reading from cache or "
    "forwarding from the local store buffer.",
    "In the example, Thread 1's store to x may still be in its store buffer "
    "when Thread 2 loads x, and vice versa. Both read the old values. Each "
    "core sees its own stores immediately and other cores see them late "
    "— which is exactly the reordering that sequential reasoning does "
    "not permit."]),

  ("h1", "2 &nbsp; Consistency models"),
  ("p", "A <b>memory consistency model</b> is the contract specifying which "
        "reorderings a processor may perform. It is part of the ISA."),
  ("table", ["Model", "Permitted reorderings", "Hardware"],
   [["<b>Sequential consistency</b>", "None. Every core observes one global "
     "order consistent with program order.",
     "No commercially significant processor. Too slow."],
    ["<b>TSO</b> (total store order)",
     "Store&rarr;load only. Stores are not reordered with other stores, and "
     "loads are not reordered with other loads.",
     "x86-64. Relatively strong."],
    ["<b>Weak / relaxed</b>",
     "Store&rarr;store, load&rarr;load, load&rarr;store, store&rarr;load "
     "— nearly anything absent explicit barriers.",
     "ARM, POWER, RISC-V."]],
   [0.21, 0.46, 0.33]),
  ("callout", "The portability trap that bites real products",
   ["Because x86 only permits store&rarr;load reordering, a great deal of "
    "under-synchronised code <i>happens to work</i> on it.",
    "ARM and POWER permit far more. The identical code fails — "
    "intermittently, under load, in ways that do not reproduce in a debugger.",
    "This is why concurrency bugs have surfaced years after being written, "
    "when a product was ported to ARM. The code was always wrong; the "
    "hardware had been hiding it.",
    "<b>Correctness cannot be inferred from testing here.</b> Reason from the "
    "memory model, express intent with the language's atomics, and test on "
    "weakly ordered hardware as a matter of routine."]),

  ("break",),
  ("h1", "3 &nbsp; Ordering, expressed"),
  ("table", ["Ordering", "Guarantee", "Typical use"],
   [["<code>relaxed</code>", "Atomicity only. No ordering with respect to "
     "anything else.",
     "Statistics counters read only after all threads join."],
    ["<code>acquire</code> (loads)",
     "No read or write after this operation may be reordered before it.",
     "Acquiring a lock; reading a readiness flag."],
    ["<code>release</code> (stores)",
     "No read or write before this operation may be reordered after it.",
     "Releasing a lock; setting a readiness flag."],
    ["<code>acq_rel</code>", "Both, for a read-modify-write.",
     "Compare-and-swap in a lock-free structure."],
    ["<code>seq_cst</code>",
     "All seq_cst operations across all threads share one global order.",
     "The default, and the right choice unless you have measured a need for "
     "something weaker."]],
   [0.17, 0.44, 0.39]),
  ("h2", "3.1 &nbsp; The publish/subscribe pattern"),
  ("code", """// Producer                        // Consumer
data = compute();                  while (!ready.load(acquire))
ready.store(true, release);            /* spin */;
                                   use(data);"""),
  ("p", "The release store guarantees that everything written before it in "
        "program order is visible to any thread that performs an acquire load "
        "observing that store. The acquire load guarantees that nothing after "
        "it is reordered before it. Together they establish a "
        "<i>happens-before</i> relationship across the two threads, which is "
        "precisely what makes <code>data</code> safe to read."),
  ("p", "With relaxed ordering on either operation, the consumer may observe "
        "<code>ready == true</code> while <code>data</code> still holds its "
        "previous value — the stores can become visible out of order. "
        "This pairing is the foundation of nearly all lock-free code, and it "
        "is the single most useful thing to take from this module."),

  ("h1", "4 &nbsp; The compiler reorders too"),
  ("p", "Hardware reordering is only half the problem. Compilers reorder "
        "independent operations, keep values in registers across loop "
        "iterations, and eliminate loads they can prove are redundant "
        "— all entirely valid under single-threaded semantics."),
  ("code", """// This can become an infinite loop:
while (!done) { }         // `done` is a plain bool

// The compiler proves nothing in the loop writes `done`, hoists
// the load out, and generates:
//     if (!done) for (;;) { }"""),
  ("callout", "<code>volatile</code> is not a synchronisation primitive",
   ["In C and C++, <code>volatile</code> tells the compiler not to optimise "
    "away or cache accesses to a variable. That is <i>all</i> it does.",
    "It provides no atomicity: a volatile increment is still a non-atomic "
    "read-modify-write. It provides no hardware ordering: the processor may "
    "still reorder around it freely.",
    "It is intended for memory-mapped I/O registers, where every access must "
    "actually occur, not for inter-thread communication. (Java's "
    "<code>volatile</code> is a different keyword with different, stronger "
    "semantics — a persistent source of confusion.)",
    "Use <code>std::atomic</code> (C++) or <code>_Atomic</code> (C11). These "
    "constrain the compiler <i>and</i> emit the necessary hardware barriers."]),

  ("h1", "5 &nbsp; What synchronisation costs"),
  ("table", ["Mechanism", "Uncontended", "Contended"],
   [["Relaxed atomic load", "~1 cycle", "~1 cycle"],
    ["Acquire load / release store", "~1 cycle on x86 (free in the common "
     "case)", "Coherence traffic, hundreds of cycles"],
    ["<code>seq_cst</code> store on x86", "20&ndash;40 cycles (requires a "
     "fence)", "Worse"],
    ["Uncontended mutex lock/unlock", "~20 cycles",
     "&mdash;"],
    ["Contended mutex", "&mdash;",
     "1,000+ cycles: futex syscall, context switch, possible scheduler delay"]],
   [0.30, 0.35, 0.35]),
  ("p", "Note that an uncontended mutex is cheap — roughly the cost of "
        "one atomic operation. Essentially all of the cost of locking is the "
        "cost of <i>contention</i>, which means the productive response to "
        "slow locking is usually to reduce sharing rather than to abandon "
        "locks."),

  ("h1", "6 &nbsp; Advice"),
  ("ol", ["<b>Use a mutex</b> unless profiling shows it is the bottleneck. "
          "Uncontended locks are cheap and the code is obviously correct, "
          "which has enormous value.",
          "<b>Reduce sharing before optimising synchronisation.</b> Per-thread "
          "state combined at the end removes the problem rather than making "
          "it cheaper.",
          "<b>Prefer immutability and message passing.</b> Data that is never "
          "mutated after publication needs no synchronisation at all beyond "
          "the publication itself.",
          "<b>If you go lock-free, be explicit.</b> Use "
          "<code>std::atomic</code> with stated memory orderings, write down "
          "the happens-before argument in a comment, and treat the code as "
          "requiring review by someone who knows this material.",
          "<b>Never invent a synchronisation primitive</b> without a "
          "correctness argument. This is the area of systems programming where "
          "plausible reasoning is least reliable.",
          "<b>Use the tools.</b> ThreadSanitizer finds races that testing "
          "will not. Run stress tests on ARM as well as x86."]),
  ("callout", "Why this is genuinely hard",
   ["Lock-free code that is subtly wrong passes essentially every test you "
    "will write for it. The failure requires a specific interleaving, on "
    "specific hardware, under specific load, and may appear once a month in "
    "production.",
    "The discipline is therefore to reason formally rather than empirically: "
    "establish happens-before relationships explicitly, and treat a passing "
    "test suite as no evidence whatsoever of correctness."]),
 ],
 "resources": [
   ("Onur Mutlu — Memory Consistency lectures",
    "https://safari.ethz.ch/architecture/",
    "The hardware side: store buffers, consistency models, and fences."),
   ("Paul McKenney — Is Parallel Programming Hard? (free book)",
    "https://mirrors.edge.kernel.org/pub/linux/kernel/people/paulmck/perfbook/perfbook.html",
    "The definitive free treatment of memory ordering in practice, from the "
    "author of the Linux RCU implementation."),
   ("Jeff Preshing — blog on lock-free programming",
    "https://preshing.com/",
    "The clearest available explanations of acquire/release semantics, with "
    "worked examples and diagrams. Start with 'Memory Ordering at Compile "
    "Time'."),
   ("Russ Cox — Hardware and Programming Language Memory Models",
    "https://research.swtch.com/mm",
    "A three-part series covering both hardware and language models, "
    "unusually clearly."),
   ("cppreference — std::memory_order",
    "https://en.cppreference.com/w/cpp/atomic/memory_order",
    "The precise semantics, with examples. The reference to check before "
    "writing any atomic code."),
 ],
 "exercises": [
   "Implement Dekker's example and run it in a tight loop on x86 until you "
   "observe r1 == 0 && r2 == 0. Record how long it took.",
   "Add a <code>seq_cst</code> fence between the store and the load in each "
   "thread and confirm the outcome becomes impossible. Measure the cost of "
   "the fence.",
   "Implement the publish/subscribe pattern with acquire/release, then with "
   "relaxed ordering on both operations. Try to observe the consumer reading "
   "stale data — on x86 you may not, which is itself the lesson.",
   "Write a spin loop on a plain <code>bool</code> and confirm with the "
   "generated assembly that the compiler hoists the load. Fix it with "
   "<code>std::atomic</code> and compare.",
   "Measure uncontended and contended mutex cost, and compare against "
   "equivalent atomic operations, at 1, 2, 4, and 8 threads.",
   "If you have access to an ARM machine (including an Apple Silicon Mac or a "
   "Raspberry Pi), run the same experiments there and compare. This is the "
   "most instructive exercise in the module.",
   "Run any concurrent code you have written under ThreadSanitizer and report "
   "what it finds.",
 ],
 "selfcheck": [
   "Explain why r1 == 0 && r2 == 0 is possible in Dekker's example, in terms "
   "of store buffers.",
   "Why does no real hardware implement sequential consistency?",
   "What reordering does x86 TSO permit, and what additional ones do ARM and "
   "POWER permit?",
   "State precisely what acquire and release each guarantee, and how they "
   "combine.",
   "Why is <code>volatile</code> insufficient for inter-thread communication "
   "in C++?",
   "An uncontended mutex costs about 20 cycles. What does that suggest about "
   "when to replace locks with lock-free code?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Energy, Scaling, and Specialization",
 "subtitle": "Why the free lunch ended, and what replaced it.",
 "question": "Why did clock speeds stop rising, and where is performance "
             "coming from now?",
 "outcomes": [
     "Explain Dennard scaling and why its end changed everything.",
     "Explain dark silicon and the shift to multicore.",
     "Explain why specialised hardware is more efficient.",
     "Describe the current landscape of accelerators.",
     "Build a working cost model of a modern machine.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The free lunch",
   "blurb": "Thirty years of programs getting faster without being changed."},

  {"t": "eq", "kicker": "Dennard scaling", "title": "Why it worked",
   "eqs": [
     ("P  =  C · V² · f",
      "Dynamic power: capacitance, voltage squared, frequency."),
     ("shrink by k:  C ↓ k,  V ↓ k,  f ↑ k",
      "Dennard's observation: smaller transistors run at lower voltage."),
     ("power density stays constant",
      "More transistors, faster, <b>same power</b>. For thirty years."),
   ],
   "caption": "Moore's law gave more transistors; Dennard scaling let you use "
              "them for free. The second one is what actually ended.",
   "note": "Students conflate Moore's law ending with Dennard scaling ending. "
           "The distinction is the whole module."},

  {"t": "callout", "title": "Dennard scaling ended around 2005",
   "kind": "The turning point",
   "body": ["Voltage stopped scaling, because leakage current rises sharply "
            "as threshold voltage falls — a transistor that does not "
            "switch off cleanly wastes power continuously.",
            "With V fixed, shrinking transistors raises power <i>density</i>. "
            "Clock frequency became limited by heat rather than by "
            "switching speed.",
            "Clock speeds flattened at 3–4 GHz, where they remain "
            "twenty years later.",
            "Moore's law continued for some time — transistors kept "
            "getting smaller. What ended was the ability to use them all at "
            "full speed. That is <b>dark silicon</b>: a chip with more "
            "transistors than it can power simultaneously."]},

  {"t": "section", "label": "Part 2", "title": "The responses",
   "blurb": "Three strategies, in historical order."},

  {"t": "table", "kicker": "Responses", "title": "How the industry adapted",
   "header": ["Response", "Idea", "Cost to you"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Multicore", "Many simpler cores instead of one fast one",
      "<b>You must parallelise.</b> Amdahl applies"],
     ["Heterogeneity", "Big cores + little cores on one die",
      "Scheduling complexity; variable performance"],
     ["Specialisation", "Fixed-function units for specific work",
      "Only helps if your work matches"],
   ],
   "note": "Multicore was the first and bluntest response, and it transferred "
           "the burden to software. That transfer is why CSCE 735 exists."},

  {"t": "callout", "title": "The burden moved to software",
   "kind": "The consequence",
   "body": ["Before 2005, a program got faster every year by doing nothing. "
            "Clock speeds rose and single-thread performance rose with them.",
            "After 2005, performance came from <i>more cores</i>, which "
            "benefit only programs written to use them.",
            "Single-thread performance has improved maybe 2–3× in "
            "twenty years, from microarchitecture rather than frequency.",
            "This is why parallel programming stopped being specialised and "
            "became general. It is also why Amdahl's law from Module 01 is a "
            "practical constraint rather than a theoretical curiosity."]},

  {"t": "section", "label": "Part 3", "title": "Specialisation",
   "blurb": "Why fixed-function hardware wins by orders of magnitude."},

  {"t": "bullets", "kicker": "Why", "title": "Where a general-purpose core spends its energy",
   "items": [
     "A 32-bit integer add costs well under 1 pJ.",
     "<b>Fetching, decoding, renaming, scheduling, and retiring</b> the "
     "instruction that performs it costs far more.",
     "",
     "In a general-purpose core, the arithmetic is a small fraction of the "
     "energy.",
     "",
     "Fixed-function hardware removes the overhead entirely: no fetch, no "
     "decode, no scheduling, data flowing through dedicated logic.",
     "",
     "The result is routinely <b>10–1000×</b> better energy "
     "efficiency for the task it was built for.",
   ],
   "note": "The energy breakdown is the explanation people usually lack. "
           "Instruction overhead dominating arithmetic is the key fact."},

  {"t": "table", "kicker": "Accelerators", "title": "The current landscape",
   "header": ["Accelerator", "For", "Why it wins"],
   "widths": [3.0, 4.2, 4.9],
   "rows": [
     ["GPU", "Data-parallel throughput", "Area spent on ALUs, not control"],
     ["Video codec block", "H.264/H.265/AV1", "Fixed function; ~100× efficiency"],
     ["Tensor/matrix units", "Matrix multiply", "Systolic dataflow; minimal data movement"],
     ["Ray tracing units", "BVH traversal, intersection", "Fixed-function traversal"],
     ["DSP / NPU", "Signal processing, inference", "Specialised datapaths, low precision"],
   ],
   "note": "The RT cores row connects directly to CSCE 647: hardware "
           "acceleration changed what is feasible in real-time rendering."},

  {"t": "callout", "title": "Specialisation has a cost too",
   "kind": "The trade",
   "body": ["Fixed-function hardware does one thing. If the algorithm "
            "changes, the silicon is wasted — and silicon takes years to "
            "design and fabricate.",
            "A video block that decodes H.265 is useless for AV1. Tensor "
            "units tuned for one numeric format are poor for another.",
            "So specialisation is a bet that the workload is <i>stable</i>. "
            "It has paid off for video, graphics, and dense linear algebra, "
            "all of which have been stable for a decade or more.",
            "It is a worse bet for anything still changing rapidly — "
            "which is why programmable GPUs beat fixed-function graphics "
            "pipelines in the first place."]},

  {"t": "section", "label": "Part 4", "title": "A cost model",
   "blurb": "What this course was for."},

  {"t": "table", "kicker": "Synthesis", "title": "The questions to ask about any slow code",
   "header": ["Question", "Check", "Module"],
   "widths": [4.8, 3.6, 3.7],
   "rows": [
     ["Am I compute- or memory-bound?", "IPC", "01, 08"],
     ["Am I missing in cache?", "Miss rates by level", "05, 06"],
     ["Am I missing in the TLB?", "dTLB misses", "07"],
     ["Am I mispredicting branches?", "branch-miss rate", "04"],
     ["Am I vectorised?", "Assembly, vec reports", "09"],
     ["Am I sharing between cores?", "perf c2c", "11"],
     ["Would this suit a GPU?", "Arithmetic intensity", "10"],
   ],
   "note": "This table is the course's deliverable. Students should be able "
           "to work down it without prompting."},

  {"t": "bullets", "kicker": "The model", "title": "What you should now believe",
   "items": [
     "<b>Memory dominates.</b> A 2% miss rate costs more than a 5% branch "
     "misprediction rate by a factor of ten.",
     "<b>Latency is hidden, not removed.</b> Caches, prefetching, "
     "out-of-order, and multithreading are all latency hiding.",
     "<b>Parallelism is everywhere</b> — lanes, pipelines, cores, "
     "devices — and each level has a different cost.",
     "<b>Layout decides performance</b> more often than algorithms do, once "
     "the algorithm is reasonable.",
     "<b>Measure.</b> Every claim in this course is checkable on your own "
     "machine in an afternoon.",
   ]},

  {"t": "bullets", "kicker": "End", "title": "Where this course leaves you",
   "items": [
     "You can predict, roughly, what will make a loop slow — before "
     "running it.",
     "You can diagnose a slow program from counters rather than guesswork.",
     "You know why CSCE 629's model is wrong, and by how much.",
     "",
     "<b>CSCE 641</b> is where cache behaviour becomes frame time.",
     "<b>CSCE 735</b> takes the parallelism hierarchy seriously.",
     "<b>CSCE 611</b> explains the operating system on top of this hardware.",
   ]},
 ],
 "takeaways": [
   "Dennard scaling — not Moore's law — is what ended around 2005, "
   "when voltage stopped scaling because of leakage.",
   "Dark silicon: a chip can contain more transistors than it can power at "
   "once. Clock speeds have been flat at 3–4 GHz for twenty years.",
   "The response was multicore, which transferred the performance burden to "
   "software and made Amdahl's law a practical constraint.",
   "In a general-purpose core, instruction overhead dominates the arithmetic "
   "energy. Fixed-function hardware removes it, winning 10–1000×.",
   "Specialisation bets that the workload is stable. It has paid for video, "
   "graphics, and dense linear algebra.",
   "The deliverable of this course is a diagnostic checklist: IPC, cache "
   "misses, TLB, branches, vectorisation, sharing.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The free lunch, and why it ended"),
  ("p", "From roughly 1975 to 2005, programs became faster each year without "
        "being modified. Clock frequencies rose, and single-thread "
        "performance rose with them. Two separate trends made this possible, "
        "and they are routinely conflated."),
  ("table", ["", "Moore's law", "Dennard scaling"],
   [["Statement", "Transistor density doubles roughly every two years.",
     "As transistors shrink, voltage and current scale down proportionally, "
     "so power density stays constant."],
    ["Gives you", "More transistors.",
     "The ability to run them faster at the same power."],
    ["Status", "Slowed, but continued well past 2005.",
     "<b>Ended around 2005.</b>"]],
   [0.14, 0.40, 0.46]),
  ("eq", "P = C &middot; V&#178; &middot; f"),
  ("p", "Dynamic power depends on capacitance, the <i>square</i> of voltage, "
        "and frequency. Dennard's insight was that shrinking a transistor "
        "reduces C and permits a lower V, so frequency could rise with no net "
        "power increase. Smaller, faster, same power, for thirty years."),
  ("callout", "Why voltage stopped scaling",
   ["Lowering supply voltage requires lowering the transistor's threshold "
    "voltage. Below a certain point, transistors no longer switch off "
    "cleanly, and <b>leakage current</b> flows continuously even when "
    "nothing is switching.",
    "Leakage rises exponentially as threshold voltage falls, so beyond about "
    "2005 further voltage reduction cost more in static power than it saved "
    "in dynamic power.",
    "With V fixed and C still falling, power <i>density</i> rises as chips "
    "shrink. Frequency became limited by heat removal rather than by "
    "transistor switching speed. Clocks flattened at 3&ndash;4 GHz and have "
    "stayed there for two decades.",
    "<b>Dark silicon</b> is the consequence: a chip can contain more "
    "transistors than it can power simultaneously, so some fraction must "
    "always be idle or run slowly."]),

  ("h1", "2 &nbsp; Three responses"),
  ("table", ["Response", "What it does", "What it costs"],
   [["<b>Multicore</b>",
     "Use the transistor budget for several simpler cores instead of one "
     "larger one. Total throughput rises even though per-core speed does not.",
     "<b>The burden moves to software.</b> Only parallel programs benefit, "
     "and Amdahl's law (Module 01) caps the gain."],
    ["<b>Heterogeneity</b>",
     "Combine a few large high-performance cores with many small efficient "
     "ones, scheduling work according to need.",
     "Scheduling complexity and variable, less predictable performance. "
     "Benchmarking becomes harder."],
    ["<b>Specialisation</b>",
     "Dedicate silicon to specific tasks: video codecs, matrix units, "
     "cryptography, ray traversal.",
     "Only helps workloads that match. Inflexible, and obsolete if the "
     "algorithm changes."]],
   [0.17, 0.44, 0.39]),
  ("callout", "What this meant for programmers",
   ["Before 2005, performance was the hardware's problem. A program written "
    "in 1995 ran several times faster in 2000 with no changes.",
    "After 2005, additional performance came almost entirely from "
    "parallelism, and parallelism must be programmed. Single-thread "
    "performance has improved perhaps two to three times in twenty years, all "
    "of it from microarchitecture — wider issue, better prediction, "
    "larger caches — rather than frequency.",
    "This is why parallel programming moved from a specialist concern to a "
    "general one, and why Amdahl's law is now a practical constraint on "
    "ordinary software rather than a theoretical observation about "
    "supercomputers. CSCE 735 exists because of this transition."]),

  ("break",),
  ("h1", "3 &nbsp; Why specialisation wins"),
  ("p", "A fixed-function unit can be hundreds of times more energy-efficient "
        "than a general-purpose core performing the same computation. The "
        "reason is where the energy actually goes."),
  ("table", ["Operation", "Approximate energy"],
   [["32-bit integer add", "&lt; 1 pJ"],
    ["32-bit floating-point multiply-add", "a few pJ"],
    ["Reading a 32-bit value from a register file", "a few pJ"],
    ["Fetching, decoding, renaming, scheduling, and retiring one instruction",
     "<b>tens to hundreds of pJ</b>"],
    ["Reading 32 bits from DRAM", "<b>hundreds to thousands of pJ</b>"]],
   [0.6, 0.4]),
  ("callout", "The arithmetic is almost free; everything around it is not",
   ["In a general-purpose out-of-order core, the actual computation is a "
    "small fraction of the energy consumed. The majority goes to instruction "
    "supply, dependence tracking, scheduling, and data movement.",
    "Fixed-function hardware eliminates all of it. There is no instruction to "
    "fetch or decode, no renaming, no scheduling; data flows through "
    "dedicated logic laid out for the specific computation, with operands "
    "travelling minimal distances.",
    "That is the source of the 10&ndash;1000&times; efficiency advantage, and "
    "it explains why every phone contains a dozen accelerators: under a fixed "
    "power budget, specialisation is the only remaining way to increase "
    "useful work."]),
  ("table", ["Accelerator", "Workload", "Mechanism"],
   [["<b>GPU</b>", "Data-parallel throughput work",
     "Die area spent on arithmetic rather than control; latency hidden by "
     "thread switching (Module 10)."],
    ["<b>Video encode/decode block</b>", "H.264, H.265, AV1",
     "Entirely fixed function. Roughly 100&times; the efficiency of software "
     "decode, which is why phones play 4K video without heating up."],
    ["<b>Tensor / matrix units</b>", "Dense matrix multiplication",
     "Systolic arrays: operands flow between adjacent processing elements, "
     "minimising data movement — the dominant energy cost."],
    ["<b>Ray tracing units</b>", "BVH traversal and triangle intersection",
     "Fixed-function traversal and intersection test. This is what made "
     "real-time ray tracing viable, and it is directly relevant to "
     "CSCE 647."],
    ["<b>NPU / DSP</b>", "Inference, signal processing",
     "Specialised datapaths with reduced precision (int8, bf16), trading "
     "numerical range for efficiency."]],
   [0.20, 0.25, 0.55]),
  ("callout", "The bet specialisation makes",
   ["Fixed-function silicon does exactly one thing, takes years to design and "
    "fabricate, and is wasted if the algorithm changes. A decoder built for "
    "H.265 cannot decode AV1.",
    "So specialisation is a wager that the workload will remain stable long "
    "enough to repay the investment. It has paid handsomely for video "
    "compression, rasterised graphics, and dense linear algebra, all stable "
    "for a decade or more.",
    "It is a poor wager for anything evolving quickly — which is exactly "
    "why programmable shaders displaced fixed-function graphics pipelines in "
    "the first place, and a useful corrective to the assumption that "
    "specialisation is always the future."]),

  ("h1", "4 &nbsp; The cost model this course was for"),
  ("p", "The point of thirteen modules was not the mechanisms individually. "
        "It was to build a model good enough to predict and diagnose. When "
        "code is slow, work down this list:"),
  ("table", ["Question", "What to measure", "Module"],
   [["Is the core computing or waiting?", "IPC", "01, 08"],
    ["Is it missing in cache, and at which level?",
     "L1/L2/LLC miss rates", "05, 06"],
    ["Is it missing in the TLB?", "<code>dTLB-load-misses</code>", "07"],
    ["Is it mispredicting branches?", "<code>branch-misses</code> rate", "04"],
    ["Did the hot loop vectorise?",
     "Compiler reports; generated assembly", "09"],
    ["Are cores contending or falsely sharing?",
     "<code>perf c2c</code>; scaling curve", "11"],
    ["Is the synchronisation correct and cheap?",
     "ThreadSanitizer; contention counters", "12"],
    ["Would this workload suit a GPU?",
     "Arithmetic intensity; transfer volume", "10"]],
   [0.36, 0.40, 0.24]),
  ("h2", "4.1 &nbsp; What you should now believe"),
  ("ul", ["<b>Memory dominates.</b> A 2% main-memory miss rate contributes "
          "ten times more to CPI than a 5% branch misprediction rate. Check "
          "memory first, always.",
          "<b>Latency is hidden, not eliminated.</b> Caches, prefetchers, "
          "out-of-order execution, hyperthreading, and GPU thread switching "
          "are all the same idea applied at different scales: find something "
          "else to do while waiting.",
          "<b>Parallelism exists at every level</b> — vector lanes, "
          "pipeline stages, cores, sockets, devices — and each level has "
          "its own cost model and its own failure modes.",
          "<b>Data layout decides performance</b> more often than algorithm "
          "choice does, once the algorithm is asymptotically reasonable. This "
          "is the single most actionable conclusion of the course.",
          "<b>Everything here is measurable.</b> Every claim in these "
          "thirteen modules can be checked on your own machine in an "
          "afternoon, and you should distrust any you have not checked."]),
  ("callout", "Where this leaves you",
   ["You can look at a loop and predict, approximately, what will make it "
    "slow — before running it. You can take a slow program and diagnose "
    "it from hardware counters rather than by guessing. And you know "
    "precisely why CSCE 629's RAM model is wrong, in which direction, and by "
    "how much.",
    "<b>CSCE 641</b> is where this becomes frame time: a rendering loop is "
    "memory-bound far more often than it is arithmetic-bound, and the layout "
    "of vertex and texture data decides it. <b>CSCE 735</b> takes the "
    "parallelism hierarchy seriously and makes the scaling arguments "
    "quantitative. <b>CSCE 611</b> explains the operating system layered on "
    "top of all this hardware."]),
 ],
 "resources": [
   ("Onur Mutlu — Why Computer Architecture? and the closing lectures",
    "https://safari.ethz.ch/architecture/",
    "The scaling story and the case for specialisation, from someone who "
    "works on it."),
   ("Hennessy & Patterson — 'A New Golden Age for Computer "
    "Architecture' (Turing lecture, free)",
    "https://cacm.acm.org/research/a-new-golden-age-for-computer-architecture/",
    "The authors of the standard textbook on where architecture goes after "
    "Dennard scaling. Short, and the best single summary of this module's "
    "argument."),
   ("Herb Sutter — The Free Lunch Is Over (2005)",
    "http://www.gotw.ca/publications/concurrency-ddj.htm",
    "The essay that told the software industry the transition had happened. "
    "Worth reading as a historical document."),
   ("Mark Horowitz — Computing's Energy Problem (ISSCC keynote, free "
    "slides)",
    "https://ieeexplore.ieee.org/document/6757323",
    "Where the energy actually goes in a modern core. The source of the "
    "numbers in &sect;3."),
 ],
 "exercises": [
   "Measure your processor's clock frequency under sustained load versus "
   "idle. Relate the difference to the power equation and to the thermal "
   "throttling discussion of Module 01.",
   "Compare the energy consumed decoding a video in software versus using the "
   "hardware decoder, using battery drain or a power meter. Report the ratio.",
   "Measure parallel scaling of a workload from 1 to N threads. Fit Amdahl's "
   "law to the curve and estimate the serial fraction.",
   "Take a kernel and run it on CPU with SIMD, on CPU multithreaded, and on "
   "GPU. Report time and, if you can measure it, energy for each.",
   "Write the Module 4 diagnostic checklist as a script that runs "
   "<code>perf stat</code> with the right counters and prints an assessment. "
   "You will use it afterwards.",
   "<b>Project 2 is now due.</b> Complete the optimisation project described "
   "in the syllabus: a 5&times; speedup with predictions recorded before each "
   "measurement.",
   "Write a one-page summary of your own machine: cache sizes, TLB reach, "
   "misprediction penalty, SIMD width, core count, memory bandwidth. Every "
   "number measured by you.",
 ],
 "selfcheck": [
   "Distinguish Moore's law from Dennard scaling. Which one ended around "
   "2005, and why?",
   "Why did voltage stop scaling, and what is dark silicon?",
   "What did the shift to multicore transfer to software, and which earlier "
   "result became practically important as a result?",
   "Why is fixed-function hardware 10&ndash;1000&times; more energy "
   "efficient? Where does the energy go in a general-purpose core?",
   "What bet does specialisation make, and give one workload where it paid "
   "and one where programmability won.",
   "List the diagnostic questions you would ask, in order, about a slow "
   "program.",
   "Which costs more CPI: a 2% memory miss rate or a 5% branch misprediction "
   "rate? By roughly how much?",
 ],
},

]
