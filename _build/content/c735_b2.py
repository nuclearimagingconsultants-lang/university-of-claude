# -*- coding: utf-8 -*-
"""CSCE 735 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Parallel Architectures",
 "subtitle": "The machines you are writing for.",
 "question": "What hardware are you actually targeting?",
 "outcomes": [
     "Distinguish the forms of parallelism available in hardware.",
     "Explain SIMD and what makes a loop vectorisable.",
     "Explain NUMA and its consequences for data placement.",
     "Contrast latency-oriented and throughput-oriented cores.",
     "Choose a programming model from the hardware and the problem.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Forms of parallelism",
   "blurb": "Four kinds, exploited differently."},

  {"t": "table", "kicker": "Taxonomy", "title": "Parallelism in hardware",
   "header": ["Form", "Granularity", "Exploited by"],
   "widths": [3.0, 3.6, 5.5],
   "rows": [
     ["<b>ILP</b>", "Instructions", "<b>The hardware, automatically</b>"],
     ["<b>SIMD / vector</b>", "Elements within an instruction", "<b>The compiler, or intrinsics</b>"],
     ["<b>Thread / core</b>", "Independent instruction streams", "<b>You, explicitly</b>"],
     ["Node", "Separate machines", "<b>You, via messages</b>"],
   ],
   "footnote": "<b>Only the first is free.</b> Everything below it requires "
               "the program to be structured for it.",
   "note": "This table is the map for Modules 03 through 10 and is worth "
           "returning to."},

  {"t": "callout", "title": "Instruction-level parallelism is already spent",
   "kind": "Why the others matter",
   "body": ["<b>Out-of-order execution, speculation, and superscalar issue</b> "
            "extract parallelism from a serial instruction stream "
            "automatically (CSCE 614).",
            "<b>And they have reached diminishing returns.</b> The window "
            "of instructions that can be examined is limited by branch "
            "prediction accuracy and by the cost of the machinery.",
            "<b>So the hardware cannot find much more on its own.</b>",
            "<b>Which is precisely why the remaining forms require you.</b> "
            "The free parallelism has been extracted; what is left must be "
            "expressed."]},

  {"t": "section", "label": "Part 2", "title": "SIMD",
   "blurb": "The cheapest parallelism you are probably not using."},

  {"t": "callout", "title": "One instruction, several elements",
   "kind": "What SIMD is",
   "body": ["<b>A 512-bit vector register holds 16 single-precision "
            "floats.</b> One add instruction adds all sixteen.",
            "<b>So a vectorised loop can be 4 to 16 times faster</b> at "
            "identical clock speed and core count.",
            "<b>It is free in the sense that the hardware is already "
            "there</b> and idle if you do not use it.",
            "<b>And it is wasted by default.</b> Scalar code uses one lane "
            "of sixteen — a 94% waste of the vector unit on every "
            "arithmetic instruction."]},

  {"t": "code", "kicker": "Vectorisation", "title": "What stops a loop vectorising",
   "lang": "cpp", "code": """
// VECTORISES: independent, contiguous, no branches
for (int i = 0; i < n; i++)  c[i] = a[i] + b[i];

// NO: loop-carried dependence -- element i needs element i-1
for (int i = 1; i < n; i++)  a[i] = a[i-1] + b[i];

// NO (usually): the compiler cannot prove a and b do not overlap
void f(float* a, float* b, int n) { for (...) a[i] = b[i] * 2; }
//   fix: float* __restrict__ a

// POORLY: non-contiguous access needs gather/scatter
for (int i = 0; i < n; i++)  c[i] = a[idx[i]];

// POORLY: a divergent branch makes both sides execute, masked
for (int i = 0; i < n; i++)  if (a[i] > 0) c[i] = f(a[i]);

// *** Check: compile with -fopt-info-vec and READ THE OUTPUT. ***
""",
   "caption": "Four conditions: independent iterations, contiguous access, "
              "no aliasing, uniform control flow. Violate one and the "
              "compiler declines.",
   "note": "The __restrict__ case is the most common and the easiest to "
           "fix — worth demonstrating."},

  {"t": "bullets", "kicker": "Practice", "title": "Getting vectorisation",
   "items": [
     "<b>Read the compiler's vectorisation report.</b> It says what it did "
     "and, more usefully, why it refused.",
     "",
     "<b>Use <code>__restrict__</code></b> to promise pointers do not "
     "alias. The single most common blocker.",
     "",
     "<b>Structure of arrays, not array of structures.</b> SoA gives "
     "contiguous access per field; AoS gives strided.",
     "",
     "<b>Align data</b> to the vector width, and tell the compiler it is "
     "aligned.",
     "",
     "<b>Intrinsics as a last resort</b> — unportable, unreadable, and "
     "occasionally necessary.",
   ],
   "footnote": "<b>SoA versus AoS is frequently a 4–8&times; "
               "difference</b> and is a data layout decision, not an "
               "optimisation."},

  {"t": "section", "label": "Part 3", "title": "Memory",
   "blurb": "Where the time actually goes."},

  {"t": "callout", "title": "NUMA: not all memory is equally far away",
   "kind": "The multi-socket reality",
   "body": ["<b>On a multi-socket machine each socket has its own memory "
            "controller.</b> Accessing the other socket's memory crosses an "
            "interconnect.",
            "<b>Remote access is roughly 1.5–2× the latency</b> and has "
            "lower bandwidth.",
            "<b>And allocation is first-touch:</b> a page is placed on the "
            "socket of the thread that <i>first writes</i> it, not the one "
            "that allocated it.",
            "<b>So initialise data in parallel, with the same thread "
            "mapping you will compute with.</b> Serial initialisation puts "
            "everything on one socket and halves your bandwidth."]},

  {"t": "callout", "title": "False sharing: correctness is fine, performance is destroyed",
   "kind": "The bug that profiles like a mystery",
   "body": ["<b>Coherence operates on cache lines, not variables.</b> Two "
            "threads writing different variables in the same 64-byte line "
            "invalidate each other's copy on every write.",
            "<b>The program is correct</b> — no race, no wrong answer.",
            "<b>And it can be slower than serial</b>, because every write "
            "becomes a coherence transaction.",
            "<b>The fix is padding</b> — give each thread's counter its "
            "own cache line. <b>Per-thread accumulators combined at the end "
            "are the general pattern</b>, and they fix this for free."]},

  {"t": "section", "label": "Part 4", "title": "Two kinds of core",
   "blurb": "Latency machines and throughput machines."},

  {"t": "two", "kicker": "Design points", "title": "CPU and GPU",
   "lh": "CPU — latency oriented",
   "l": ["<b>Few, complex cores.</b> Large caches, deep out-of-order "
         "windows, aggressive branch prediction.",
         "<b>Goal: finish one thread as fast as possible.</b>",
         "Most transistors spent on hiding latency for one stream.",
         ("Good at: branches, irregular access, serial sections.", 1)],
   "rh": "GPU — throughput oriented",
   "r": ["<b>Many, simple cores.</b> Small caches, in-order, no "
         "speculation.",
         "<b>Goal: maximise total work per second.</b>",
         "<b>Latency hidden by switching between thousands of threads</b> "
         "rather than by prediction.",
         ("Good at: regular, data-parallel, arithmetic-heavy work.", 1)],
   "note": "The latency-hiding mechanism is the key difference and explains "
           "everything about GPU programming in Module 08."},

  {"t": "table", "kicker": "Choosing", "title": "Matching the model to the problem",
   "header": ["Problem", "Model"],
   "widths": [5.4, 6.7],
   "rows": [
     ["Regular, data-parallel, arithmetic-heavy", "<b>GPU</b>"],
     ["Irregular, branchy, pointer-chasing", "<b>CPU threads</b>"],
     ["Embarrassingly parallel, independent tasks", "Threads or processes"],
     ["<b>Data larger than one machine's memory</b>", "<b>MPI (Module 10)</b>"],
     ["Latency-critical, small", "<b>One thread; parallelism costs more than it saves</b>"],
   ],
   "footnote": "<b>The last row matters.</b> Parallelism has overhead, and "
               "for small work it loses.",
   "note": "The small-work case is real — thread creation costs "
           "microseconds and some work is not worth it."},
 ],
 "takeaways": [
   "Four forms of parallelism: instruction-level (free), SIMD (compiler), "
   "threads (you), and nodes (you, via messages).",
   "Instruction-level parallelism has reached diminishing returns, which is "
   "exactly why the others now require explicit effort.",
   "A 512-bit vector adds sixteen floats per instruction, so scalar code "
   "wastes 94% of the vector unit.",
   "A loop vectorises when iterations are independent, access is contiguous, "
   "pointers do not alias, and control flow is uniform.",
   "NUMA allocation is first-touch, so initialise data in parallel with the "
   "mapping you will compute with, or you halve your bandwidth.",
   "CPUs hide latency with caches and speculation; GPUs hide it by switching "
   "between thousands of threads — which explains everything in "
   "Module 08.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Forms of parallelism"),
  ("table", ["Form", "Granularity", "Who exploits it", "Covered in"],
   [["<b>Instruction-level (ILP)</b>",
     "Independent instructions within one stream.",
     "<b>The hardware, automatically</b> — out-of-order execution, "
     "superscalar issue, speculation (CSCE 614).", "—"],
    ["<b>SIMD / vector</b>",
     "Elements processed by a single instruction.",
     "<b>The compiler, if you let it</b> — or you, via intrinsics.",
     "This module"],
    ["<b>Thread and core</b>", "Independent instruction streams sharing "
     "memory.", "<b>You, explicitly.</b>", "Modules 03&ndash;07"],
    ["<b>Node</b>", "Separate machines with separate memory.",
     "<b>You, via explicit messages.</b>", "Module 10"]],
   [0.20, 0.26, 0.38, 0.16]),
  ("callout", "Instruction-level parallelism is already spent",
   ["<b>Out-of-order execution, speculative execution, and superscalar "
    "issue extract parallelism from a sequential instruction stream "
    "automatically</b>, with no cooperation from the programmer. This is the "
    "machinery CSCE 614 covered, and it is why a serial program runs far "
    "faster than its instruction count would suggest.",
    "<b>And it has reached diminishing returns.</b> The amount of "
    "parallelism extractable is bounded by how far ahead the processor can "
    "see, which is bounded by branch prediction accuracy — and by the "
    "quadratic cost of the scheduling hardware as the window grows.",
    "<b>So the hardware cannot find much more on its own.</b> Wider issue "
    "and deeper windows have stopped paying.",
    "<b>Which is precisely why the remaining forms require you.</b> The "
    "parallelism that could be extracted automatically has been extracted; "
    "what remains must be <i>expressed</i> in the structure of the program."]),

  ("h1", "2 &nbsp; SIMD"),
  ("callout", "One instruction, several elements",
   ["<b>A 512-bit vector register holds sixteen single-precision floats</b>, "
    "or eight doubles, or sixty-four bytes. <b>One vector add instruction "
    "adds all sixteen pairs.</b>",
    "<b>So a vectorised loop can run four to sixteen times faster</b> than "
    "the equivalent scalar loop, at identical clock speed and on a single "
    "core.",
    "<b>It is free in the sense that the hardware is already present</b> "
    "— you paid for the vector units when you bought the processor, and "
    "they sit idle if the code does not use them.",
    "<b>And they are idle by default.</b> Scalar code occupies one lane of "
    "sixteen, which is a 94% waste of the vector unit on every arithmetic "
    "instruction. <b>This is the cheapest available performance and the most "
    "commonly left unclaimed.</b>"]),
  ("code", """// VECTORISES: independent, contiguous, no branches
for (int i = 0; i < n; i++)  c[i] = a[i] + b[i];

// NO: loop-carried dependence
for (int i = 1; i < n; i++)  a[i] = a[i-1] + b[i];

// NO (usually): compiler cannot prove a and b do not overlap
void f(float* a, float* b, int n) { for (...) a[i] = b[i] * 2; }
//   fix: float* __restrict__ a

// POORLY: non-contiguous needs gather/scatter
for (int i = 0; i < n; i++)  c[i] = a[idx[i]];

// POORLY: divergent branch -- both sides execute, masked
for (int i = 0; i < n; i++)  if (a[i] > 0) c[i] = f(a[i]);"""),
  ("table", ["Requirement", "Why", "Fix when violated"],
   [["<b>Independent iterations</b>",
     "Element i cannot depend on element i&minus;1, since the vector "
     "computes them simultaneously.",
     "Restructure the algorithm — a scan (Module 11) is the standard "
     "answer for prefix dependencies."],
    ["<b>Contiguous access</b>",
     "A vector load reads consecutive memory. Scattered access requires "
     "gather instructions, which are far slower.",
     "<b>Structure of arrays rather than array of structures.</b>"],
    ["<b>No aliasing</b>",
     "If two pointers might refer to overlapping memory, the compiler must "
     "assume a write through one could affect a read through the other.",
     "<b><code>__restrict__</code></b>, which promises they do not overlap. "
     "<b>The most common blocker and the easiest fix.</b>"],
    ["<b>Uniform control flow</b>",
     "All lanes execute the same instruction. A branch that goes different "
     "ways in different lanes means both paths execute with masking.",
     "Make the branch uniform, or accept the cost, or use a branchless "
     "formulation."]],
   [0.20, 0.44, 0.36]),
  ("ul", ["<b>Read the compiler's vectorisation report.</b> "
          "<code>-fopt-info-vec</code> and <code>-fopt-info-vec-missed</code> "
          "on GCC, <code>-Rpass-analysis=loop-vectorize</code> on Clang. "
          "<b>It tells you what it vectorised and, far more usefully, why it "
          "declined</b> — and the reasons are specific and actionable.",
          "<b>Use <code>__restrict__</code> on pointer parameters</b> you "
          "know do not alias. This alone unlocks a great deal of "
          "vectorisation.",
          "<b>Structure of arrays, not array of structures.</b> An array of "
          "particle structs gives strided access when a loop touches one "
          "field; separate arrays per field give contiguous access. <b>This "
          "is frequently a four- to eightfold difference and it is a data "
          "layout decision rather than an optimisation</b> — which "
          "means it is expensive to change later.",
          "<b>Align data to the vector width</b> and tell the compiler it is "
          "aligned. Unaligned loads are supported and slower.",
          "<b>Intrinsics as a last resort.</b> They are unportable across "
          "instruction sets, unreadable, and occasionally the only way to "
          "express what you need. Write the portable version first and keep "
          "it."]),

  ("break",),
  ("h1", "3 &nbsp; Memory"),
  ("callout", "NUMA: not all memory is equally far away",
   ["<b>On a multi-socket machine, each socket has its own memory "
    "controller and its own attached memory.</b> A core accessing memory "
    "attached to its own socket goes directly; a core accessing the other "
    "socket's memory crosses an interconnect.",
    "<b>Remote access costs roughly 1.5 to 2 times the latency</b> and "
    "offers lower bandwidth. On a four-socket machine the disparity is "
    "larger.",
    "<b>And allocation is first-touch.</b> <code>malloc</code> reserves "
    "address space; the physical page is assigned when it is first written, "
    "<b>on the socket of the thread that writes it</b> — not the one "
    "that allocated it.",
    "<b>So initialise your data in parallel, using the same thread-to-data "
    "mapping you will use when computing.</b> A serial initialisation loop "
    "places every page on one socket, and every thread on the other socket "
    "then performs all its accesses remotely. <b>This can halve your "
    "effective bandwidth</b>, and it is invisible in the code — the "
    "initialisation loop looks harmless."]),
  ("callout", "False sharing destroys performance without affecting correctness",
   ["<b>Cache coherence operates on cache lines, typically 64 bytes, not on "
    "individual variables.</b> Two threads writing to <i>different</i> "
    "variables that happen to occupy the same cache line will invalidate "
    "each other's copy of that line on every single write.",
    "<b>The program is entirely correct.</b> There is no data race, no "
    "undefined behaviour, and the answer is right. Thread sanitisers report "
    "nothing.",
    "<b>And it can be slower than the serial version</b>, because every "
    "write turns into a coherence transaction across the interconnect "
    "instead of hitting in local cache. A per-thread counter array is the "
    "classic case: eight threads incrementing "
    "<code>counts[tid]</code> in an array of eight integers all share one "
    "cache line.",
    "<b>The fix is padding</b> — give each thread's data its own cache "
    "line, by padding the struct or over-allocating the array. <b>The "
    "general pattern is per-thread accumulators combined at the end</b>, "
    "which avoids both false sharing and contention, and is the right "
    "structure for almost all reductions anyway (Module 06)."]),

  ("h1", "4 &nbsp; Latency machines and throughput machines"),
  ("table", ["", "CPU — latency oriented", "GPU — throughput "
             "oriented"],
   [["Cores", "<b>Few and complex</b> — tens.",
     "<b>Many and simple</b> — thousands of lanes."],
    ["Per-core machinery", "Large caches, deep out-of-order windows, "
     "aggressive branch prediction, prefetchers.",
     "Small caches, in-order execution, no speculation."],
    ["Goal", "<b>Finish one thread as quickly as possible.</b>",
     "<b>Maximise total work completed per second</b>, with no concern for "
     "any individual thread's latency."],
    ["Latency hiding", "Caches, prefetching, and speculation — "
     "predict and avoid the stall.",
     "<b>Switch to another thread.</b> With thousands resident, there is "
     "always one ready, so the stall is covered by other work rather than "
     "avoided."],
    ["Good at", "Branches, irregular access, pointer chasing, serial "
     "sections, low-latency response.",
     "Regular, data-parallel, arithmetic-heavy work with predictable access "
     "patterns."]],
   [0.17, 0.41, 0.42]),
  ("p", "<b>The difference in latency-hiding mechanism is the key one</b>, "
        "and it explains essentially everything about GPU programming in "
        "Modules 08 and 09: why occupancy matters, why divergence is "
        "expensive, and why a GPU kernel with too few threads performs "
        "badly even when the arithmetic is trivial."),
  ("table", ["Problem characteristics", "Appropriate model"],
   [["Regular, data-parallel, arithmetic-heavy, predictable access.",
     "<b>GPU</b> (Modules 08, 09)."],
    ["Irregular, branchy, pointer-chasing, dependent on data values.",
     "<b>CPU threads</b> (Modules 03&ndash;06)."],
    ["Embarrassingly parallel — independent tasks with no shared "
     "state.",
     "Threads or processes; almost anything works."],
    ["<b>Data larger than one machine's memory.</b>",
     "<b>Distributed memory, MPI</b> (Module 10). This is frequently the "
     "actual reason for distribution rather than speed."],
    ["<b>Small, latency-critical work.</b>",
     "<b>One thread.</b> Thread creation costs microseconds and "
     "synchronisation costs more; <b>for small work, parallelism costs more "
     "than it saves</b>, and the correct decision is not to parallelise."]],
   [0.45, 0.55]),
 ],
 "resources": [
   ("Stanford CS149 &mdash; architecture lectures (free)",
    "https://gfxcourses.stanford.edu/cs149/",
    "The forms of parallelism, SIMD, and the latency/throughput distinction. "
    "The best free treatment of &sect;4."),
   ("Agner Fog &mdash; optimisation manuals (free)",
    "https://www.agner.org/optimize/",
    "Instruction tables, microarchitecture details, and vectorisation "
    "guidance. The reference for &sect;2, and exhaustively measured."),
   ("Ulrich Drepper &mdash; What Every Programmer Should Know About Memory "
    "(free)",
    "https://people.redhat.com/drepper/cpumemory.pdf",
    "NUMA, cache coherence, and false sharing (&sect;3), in far more detail "
    "than anywhere else. Long, and worth it."),
   ("Intel &mdash; Intrinsics Guide (free)",
    "https://www.intel.com/content/www/us/en/docs/intrinsics-guide/",
    "The reference when you reach the last resort in &sect;2."),
 ],
 "exercises": [
   "Write a vectorisable loop and compile with vectorisation reporting. Read "
   "the output.",
   "Introduce each of the four blockers in &sect;2 in turn and record what "
   "the compiler says about each.",
   "Fix the aliasing case with <code>__restrict__</code> and measure the "
   "speedup.",
   "Implement the same particle update with array-of-structures and "
   "structure-of-arrays layouts. Measure both and report the ratio.",
   "<b>Demonstrate false sharing:</b> have eight threads increment adjacent "
   "elements of an array, then pad to separate cache lines and measure "
   "again.",
   "On a multi-socket machine, initialise an array serially and then in "
   "parallel, and measure the bandwidth of a subsequent parallel loop over "
   "it.",
   "Measure memory bandwidth with a STREAM-style benchmark and compare "
   "against the hardware's specification.",
   "Time a trivial parallel region and find the problem size below which "
   "parallelisation loses.",
   "Profile a program and determine what fraction of its arithmetic "
   "instructions are vector instructions.",
 ],
 "selfcheck": [
   "Name four forms of hardware parallelism and who exploits each.",
   "Why has instruction-level parallelism reached diminishing returns?",
   "How much work does one 512-bit vector instruction do, and what does "
   "scalar code waste?",
   "Give four requirements for a loop to vectorise and the fix for each when "
   "violated.",
   "Why does structure-of-arrays beat array-of-structures?",
   "What is first-touch allocation and what must you do about it?",
   "What is false sharing, why is the program still correct, and what is the "
   "fix?",
   "Contrast CPU and GPU on cores, latency hiding, and what each is good at.",
   "Give a case where the right decision is not to parallelise.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Threads and Shared Memory",
 "subtitle": "Several instruction streams, one address space.",
 "question": "How do you write parallel code that is correct?",
 "outcomes": [
     "Distinguish a data race from a race condition.",
     "Use threads and OpenMP correctly.",
     "Explain why data races are undefined behaviour, not merely risky.",
     "Choose between thread and task parallelism.",
     "Detect races with tooling rather than reasoning.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two kinds of race",
   "blurb": "A distinction that is constantly conflated."},

  {"t": "two", "kicker": "Races", "title": "Data race and race condition",
   "lh": "Data race",
   "l": ["Two threads access the same location, at least one writes, with "
         "no synchronisation.",
         "<b>Undefined behaviour</b> in C++ — not merely a wrong answer.",
         "<b>Mechanically detectable</b> by a sanitiser.",
         ("Always a bug.", 1)],
   "rh": "Race condition",
   "r": ["The result depends on the <i>timing</i> of events.",
         "<b>A logic error</b>, not necessarily UB.",
         "<b>Not mechanically detectable</b> — it needs a specification.",
         ("Sometimes intentional.", 1)],
   "note": "The detectability difference is the practical point: one is "
           "found by tooling and the other by thinking."},

  {"t": "callout", "title": "A data race is undefined behaviour, not a wrong number",
   "kind": "Why this matters more than people think",
   "body": ["<b>The intuition is that a racy counter will be slightly "
            "wrong.</b> That is not what the standard says.",
            "<b>A data race is undefined behaviour</b>, so the compiler may "
            "assume it does not happen — and optimise accordingly.",
            "<b>So racy code can be transformed in ways that produce "
            "results no interleaving explains</b> — values that were "
            "never written, loops that do not terminate, branches both taken.",
            "<b>'It works in practice' is not a defence.</b> It works until "
            "the optimiser changes, which is a bad time to find out."]},

  {"t": "section", "label": "Part 2", "title": "Writing it",
   "blurb": "Threads, OpenMP, and tasks."},

  {"t": "code", "kicker": "OpenMP", "title": "The common cases",
   "lang": "cpp", "code": """
// Parallel loop. Iterations must be independent.
#pragma omp parallel for
for (int i = 0; i < n; i++)  c[i] = f(a[i], b[i]);

// Reduction. The compiler builds per-thread partials and combines.
double sum = 0.0;
#pragma omp parallel for reduction(+:sum)
for (int i = 0; i < n; i++)  sum += a[i];
//  ^ do NOT write this with a shared sum and a critical section:
//    it serialises, and it is slower than the serial loop.

// Scheduling: static is cheap; dynamic balances uneven work.
#pragma omp parallel for schedule(dynamic, 64)
for (int i = 0; i < n; i++)  variable_cost_work(i);

// Tasks: for recursion and irregular structure.
#pragma omp parallel
#pragma omp single
  quicksort(a, 0, n);        // which spawns #pragma omp task inside
""",
   "caption": "The reduction clause is the one to internalise — "
              "hand-rolling it with a critical section is a classic and "
              "costly mistake.",
   "note": "The critical-section reduction antipattern is extremely common "
           "and is slower than serial. Worth demonstrating."},

  {"t": "table", "kicker": "Scheduling", "title": "OpenMP loop schedules",
   "header": ["Schedule", "Behaviour", "Use when"],
   "widths": [2.6, 4.6, 4.9],
   "rows": [
     ["<b>static</b>", "Equal contiguous chunks, assigned up front", "<b>Uniform work per iteration</b>"],
     ["<b>dynamic</b>", "Threads take chunks from a queue as they finish", "<b>Variable work; some imbalance</b>"],
     ["guided", "Dynamic with shrinking chunk sizes", "Variable work; less queue overhead"],
     ["auto / runtime", "Compiler or environment decides", "When you want to tune without recompiling"],
   ],
   "footnote": "<b>static has no scheduling overhead and no load "
               "balancing.</b> dynamic has both. The chunk size is the dial "
               "between them.",
   "note": "The chunk size is the real parameter — too small and the "
           "queue dominates, too large and balance suffers."},

  {"t": "two", "kicker": "Models", "title": "Data parallelism and task parallelism",
   "lh": "Data parallel",
   "l": ["<b>The same operation on many elements.</b>",
         "A parallel for loop.",
         "<b>Load balancing by scheduling.</b>",
         ("Maps naturally onto SIMD and GPUs.", 1),
         "Most numerical work."],
   "rh": "Task parallel",
   "r": ["<b>Different operations, possibly dependent.</b>",
         "Spawned tasks with a dependency graph.",
         "<b>Load balancing by work stealing</b> (Module 06).",
         ("Natural for recursion and irregular structure.", 1),
         "Tree algorithms, pipelines, sparse problems."],
   "note": "Most real programs use both, at different levels."},

  {"t": "section", "label": "Part 3", "title": "Finding bugs",
   "blurb": "Why reasoning is insufficient."},

  {"t": "callout", "title": "Concurrency bugs do not reproduce",
   "kind": "The testing problem",
   "body": ["<b>A race may manifest in one run out of ten thousand</b>, on "
            "one machine, under one load, with one compiler version.",
            "<b>So the usual method — run it and see — "
            "fails.</b> Passing a thousand tests establishes very "
            "little.",
            "<b>And it will manifest in production</b>, under a load "
            "pattern your tests did not produce.",
            "<b>So use tools that detect the <i>possibility</i> of a race "
            "rather than its occurrence.</b> ThreadSanitizer instruments "
            "every access and checks the happens-before relation — it "
            "finds races that did not actually happen on that run."]},

  {"t": "bullets", "kicker": "Tools", "title": "What to use",
   "items": [
     "<b>ThreadSanitizer</b> — detects data races by tracking "
     "happens-before. ~10× slowdown and worth it. <b>Run your whole "
     "test suite under it.</b>",
     "",
     "<b>Helgrind / DRD</b> (Valgrind) — similar, slower, no "
     "recompilation needed.",
     "",
     "<b>Static analysis</b> with annotations — catches some classes at "
     "compile time.",
     "",
     "<b>Stress testing</b> with varied thread counts and deliberate delay "
     "injection.",
     "",
     "<b>And deterministic replay</b> where the framework supports it.",
   ],
   "footnote": "<b>Project 1 requires a clean ThreadSanitizer run</b>, "
               "which is the minimum honest standard."},

  {"t": "callout", "title": "The discipline that prevents most of this",
   "kind": "Design, not debugging",
   "body": ["<b>Share nothing by default.</b> Per-thread state combined at "
            "the end has no races to find.",
            "<b>Make shared data immutable.</b> Read-only sharing needs no "
            "synchronisation at all.",
            "<b>Where you must share mutable state, own it explicitly</b> "
            "— one lock, one clearly documented invariant, one place that "
            "touches it.",
            "<b>Most concurrency bugs are design failures</b>, not coding "
            "errors, and no amount of careful locking rescues a design that "
            "shares too much."]},
 ],
 "takeaways": [
   "A data race is two unsynchronised accesses with at least one write; a "
   "race condition is a timing-dependent result. One is detectable, the "
   "other needs a specification.",
   "A data race is undefined behaviour, so the compiler may optimise "
   "assuming it cannot happen — results need not correspond to any "
   "interleaving.",
   "Use OpenMP's reduction clause; hand-rolling a reduction with a critical "
   "section serialises and is slower than the serial loop.",
   "static scheduling has no overhead and no balancing; dynamic has both, "
   "and the chunk size is the dial between them.",
   "Concurrency bugs do not reproduce, so use tools that detect the "
   "possibility of a race rather than its occurrence.",
   "Share nothing by default, make shared data immutable, and own what must "
   "be mutable — most concurrency bugs are design failures.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two kinds of race"),
  ("table", ["", "Data race", "Race condition"],
   [["Definition", "Two threads access the same memory location, at least "
     "one of them writes, and there is no synchronisation ordering them.",
     "The program's result depends on the relative <i>timing</i> of "
     "events."],
    ["Status", "<b>Undefined behaviour</b> in C++ and most languages with a "
     "memory model.",
     "<b>A logic error</b> — the program is well-defined and does the "
     "wrong thing."],
    ["Detection", "<b>Mechanically detectable.</b> A sanitiser can find it "
     "without knowing what the program is supposed to do.",
     "<b>Not mechanically detectable</b>, because determining whether a "
     "timing dependence is wrong requires knowing the intended behaviour."],
    ["Always a bug?", "<b>Yes.</b>",
     "<b>No.</b> A work-stealing scheduler's outcome depends on timing by "
     "design."]],
   [0.15, 0.42, 0.43]),
  ("p", "<b>The two are constantly conflated</b>, including in otherwise "
        "careful writing. The practical consequence of the distinction is in "
        "the third row: one class of bug is found by running a tool, and the "
        "other requires thinking about what the program is for."),
  ("callout", "A data race is undefined behaviour, not a slightly wrong number",
   ["<b>The common intuition is that a racy counter will simply lose some "
    "increments</b> — that the answer will be a bit low but otherwise "
    "sensible. <b>That is not what the standard says</b>, and the difference "
    "matters.",
    "<b>A data race is undefined behaviour</b>, which means the compiler is "
    "entitled to assume it does not occur and to optimise on that "
    "assumption. It may hoist a load out of a loop, keep a value in a "
    "register across what you thought was a synchronisation point, or "
    "duplicate a read that you assumed happened once.",
    "<b>So racy code can produce results that no possible interleaving "
    "explains:</b> a variable holding a value that was never written to it, "
    "a loop that never terminates because the exit condition was hoisted, or "
    "both branches of an <code>if</code> taking effect.",
    "<b>'It works in practice' is not a defence.</b> It works with this "
    "compiler, at this optimisation level, on this architecture. It stops "
    "working when any of those changes — typically during a release "
    "build, in production, months later."]),

  ("h1", "2 &nbsp; Writing parallel code"),
  ("code", """#pragma omp parallel for                       // independent iterations
for (int i = 0; i < n; i++)  c[i] = f(a[i], b[i]);

double sum = 0.0;
#pragma omp parallel for reduction(+:sum)     // per-thread partials
for (int i = 0; i < n; i++)  sum += a[i];

#pragma omp parallel for schedule(dynamic, 64) // uneven work
for (int i = 0; i < n; i++)  variable_cost_work(i);

#pragma omp parallel
#pragma omp single
  quicksort(a, 0, n);        // spawns #pragma omp task internally"""),
  ("callout", "Use the reduction clause; do not hand-roll it",
   ["The common mistake is to write a shared accumulator protected by a "
    "critical section or a lock:",
    "<pre>#pragma omp parallel for\nfor (...) { #pragma omp critical\n     "
    "       sum += a[i]; }</pre>",
    "<b>This serialises the entire loop.</b> Every iteration acquires a "
    "lock, so the threads execute the body one at a time — and they pay "
    "the lock overhead on top. <b>The result is reliably slower than the "
    "serial loop</b>, often by a large factor, while appearing to be "
    "parallel.",
    "<b>The reduction clause builds a private accumulator per thread and "
    "combines them once at the end</b>, which has no contention during the "
    "loop and one logarithmic or linear combination afterwards. <b>This is "
    "also the general pattern for any associative combination</b> "
    "(Module 06), and recognising it is worth more than the clause itself."]),
  ("table", ["Schedule", "Behaviour", "Appropriate when"],
   [["<b>static</b>",
     "The iteration space is divided into equal contiguous chunks and "
     "assigned to threads before the loop begins.",
     "<b>Work per iteration is uniform.</b> No scheduling overhead at all, "
     "and good locality since each thread touches a contiguous range."],
    ["<b>dynamic</b>",
     "Threads take chunks from a shared queue as they become free.",
     "<b>Work per iteration varies</b>, so static assignment would leave "
     "some threads idle. Costs a queue operation per chunk."],
    ["<b>guided</b>",
     "Dynamic, with chunk sizes starting large and shrinking.",
     "Variable work, with less queue overhead than dynamic — large "
     "early chunks amortise the cost, small late ones balance the tail."],
    ["<b>auto / runtime</b>", "Left to the compiler or set by an "
     "environment variable.",
     "When you want to tune the schedule without recompiling, which is "
     "genuinely useful during measurement."]],
   [0.15, 0.42, 0.43]),
  ("p", "<b>The chunk size is the real parameter.</b> Too small and the "
        "queue operations dominate; too large and the final chunks cause "
        "imbalance. It depends on the per-iteration cost and should be "
        "measured rather than assumed."),

  ("break",),
  ("h1", "3 &nbsp; Finding concurrency bugs"),
  ("callout", "Concurrency bugs do not reproduce",
   ["<b>A race may manifest in one run out of ten thousand</b>, on one "
    "machine, under one particular load, with one compiler version and one "
    "optimisation level. The window in which the interleaving goes wrong may "
    "be a few nanoseconds wide.",
    "<b>So the standard testing method — run it and see whether it "
    "works — fails.</b> Passing a thousand runs establishes very "
    "little about whether a race exists; it establishes that the window was "
    "not hit a thousand times.",
    "<b>And it will manifest in production</b>, under a concurrency pattern "
    "and a load that your tests did not produce — typically at the "
    "worst moment, and typically without reproducing when investigated.",
    "<b>So use tools that detect the <i>possibility</i> of a race rather "
    "than its occurrence.</b> ThreadSanitizer instruments every memory "
    "access and maintains the happens-before relation between threads; it "
    "reports a race when two accesses are unordered, <b>whether or not they "
    "actually raced on that particular run</b>. That is a fundamentally "
    "stronger result than testing, and it is why it should be used routinely "
    "rather than when a bug is suspected."]),
  ("ul", ["<b>ThreadSanitizer</b> — compile with "
          "<code>-fsanitize=thread</code>. Roughly a 10&times; slowdown and "
          "5&times; memory, and worth both. <b>Run your entire test suite "
          "under it</b>, not just a concurrency test. <b>Project 1 requires "
          "a clean run</b>, which is the minimum honest standard.",
          "<b>Helgrind and DRD</b> (Valgrind tools) — similar "
          "detection without recompilation, considerably slower, useful when "
          "you cannot rebuild.",
          "<b>Static analysis with annotations</b> — Clang's thread "
          "safety analysis lets you annotate which lock guards which data "
          "and checks it at compile time. Catches a real class of errors "
          "with no runtime cost.",
          "<b>Stress testing</b> with varied thread counts, oversubscription, "
          "and deliberate delay injection at suspicious points — which "
          "widens the windows and makes rare interleavings likelier.",
          "<b>Deterministic replay</b> where the framework supports it, so "
          "that a failure found once can be re-examined."]),
  ("callout", "The discipline that prevents most of this",
   ["<b>Share nothing by default.</b> Give each thread its own state and "
    "combine at the end. <b>Code with no shared mutable state has no data "
    "races to find</b>, which is a far stronger position than code with "
    "carefully placed locks.",
    "<b>Make shared data immutable.</b> Read-only sharing requires no "
    "synchronisation whatsoever — any number of threads may read the "
    "same data concurrently with no cost and no risk.",
    "<b>Where mutable sharing is genuinely necessary, own it "
    "explicitly:</b> one lock, one documented invariant, and one "
    "well-defined region of code permitted to touch it. Scattered "
    "synchronisation around data that many parts of the program modify is "
    "where the difficult bugs live.",
    "<b>Most concurrency bugs are design failures rather than coding "
    "errors.</b> No amount of careful locking rescues an architecture that "
    "shares too much mutable state, and the effort is better spent on the "
    "decomposition (Module 06) than on the locking."]),
 ],
 "resources": [
   ("Stanford CS149 &mdash; shared memory programming lectures (free)",
    "https://gfxcourses.stanford.edu/cs149/",
    "Threads, OpenMP, and the decomposition material."),
   ("OpenMP specification and examples (free)",
    "https://www.openmp.org/specifications/",
    "The examples document is unusually good and covers every construct in "
    "&sect;2 with working code."),
   ("Boehm &mdash; Threads Cannot Be Implemented as a Library (free)",
    "https://dl.acm.org/doi/10.1145/1065010.1065042",
    "<b>Why data races are undefined behaviour</b> and why a language needs "
    "a memory model. The argument in &sect;1, made properly."),
   ("ThreadSanitizer documentation (free)",
    "https://github.com/google/sanitizers/wiki/ThreadSanitizerCppManual",
    "How it works and how to use it. Read the happens-before explanation "
    "— it clarifies what the tool can and cannot find."),
 ],
 "exercises": [
   "Write a program with a data race on a counter. Run it a thousand times "
   "and report how often the answer is wrong.",
   "Compile the same program at -O0 and -O3 and compare the failure rates. "
   "Explain the difference.",
   "Run it under ThreadSanitizer and confirm the race is reported even on "
   "runs that produced the correct answer.",
   "Implement a reduction with a critical section and with the reduction "
   "clause. Measure both and compare against the serial loop.",
   "Construct a loop with highly variable per-iteration cost. Measure static "
   "and dynamic scheduling, and sweep the chunk size.",
   "Implement parallel quicksort with OpenMP tasks and compare against a "
   "parallel for over fixed partitions.",
   "Write a race condition that is not a data race — properly "
   "synchronised, and still timing-dependent and wrong. Confirm "
   "ThreadSanitizer does not report it.",
   "Run your Project 1 code under ThreadSanitizer and fix everything it "
   "reports.",
   "Take a shared-mutable-state design and restructure it to share nothing. "
   "Compare the amount of synchronisation required.",
 ],
 "selfcheck": [
   "Distinguish a data race from a race condition on four axes.",
   "Why is a data race undefined behaviour rather than merely a wrong "
   "answer, and what can a compiler do with that?",
   "Why is 'it works in practice' not a defence?",
   "Why is a critical-section reduction slower than the serial loop?",
   "Compare four OpenMP schedules and say what the chunk size trades.",
   "Distinguish data from task parallelism and give an example of each.",
   "Why does testing fail to find concurrency bugs, and what do sanitisers "
   "do instead?",
   "Give three design principles that prevent most concurrency bugs.",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Synchronisation and Memory Models",
 "subtitle": "What 'happens before' means when nothing is sequential.",
 "question": "Why does your correctly locked program still misbehave?",
 "outcomes": [
     "Use mutexes and condition variables correctly.",
     "Explain why a memory model is necessary.",
     "Use atomics with appropriate memory ordering.",
     "Explain sequential consistency and why hardware does not provide it.",
     "Recognise and avoid the common synchronisation errors.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Locks",
   "blurb": "The familiar primitive, and its failure modes."},

  {"t": "table", "kicker": "Primitives", "title": "Synchronisation primitives",
   "header": ["Primitive", "Provides", "Cost"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["<b>Mutex</b>", "Mutual exclusion", "<b>~20–100 ns uncontended; far more contended</b>"],
     ["Reader-writer lock", "Many readers or one writer", "<b>Only wins with many readers</b>"],
     ["<b>Condition variable</b>", "Wait for a predicate", "Requires a mutex; <b>must loop</b>"],
     ["<b>Atomic</b>", "Indivisible read-modify-write", "<b>Cheapest; limited to one word</b>"],
     ["Barrier", "All threads reach a point", "<b>Costs the slowest thread</b>"],
     ["Semaphore", "Counted resource", "General; easy to misuse"],
   ],
   "footnote": "<b>A reader-writer lock is more expensive than a mutex "
               "when uncontended</b> — it only pays when readers "
               "genuinely dominate.",
   "note": "The RW-lock caveat surprises people who reach for it by "
           "default."},

  {"t": "code", "kicker": "Condition variables", "title": "The loop is not optional",
   "lang": "cpp", "code": """
std::unique_lock<std::mutex> lk(m);
while (!ready)          // <-- WHILE, not IF
    cv.wait(lk);
// ... use the data

// WHY A LOOP:
//  * SPURIOUS WAKEUPS are permitted by the standard -- wait() may
//    return without any notify at all.
//  * Even without them, another thread may have consumed the
//    condition between the notify and this thread acquiring the lock.
//
// With `if`, the code proceeds with the predicate FALSE.
// This is the single most common condition variable bug.

cv.wait(lk, []{ return ready; });   // the predicate overload; same loop
""",
   "caption": "The predicate overload of wait() writes the loop for you, "
              "and is what you should use.",
   "note": "This is a bug students write once and never again, but they "
           "write it."},

  {"t": "callout", "title": "Lock ordering prevents deadlock",
   "kind": "The one rule",
   "body": ["<b>Deadlock requires a cycle in the wait-for graph.</b> Thread "
            "A holds lock 1 and wants 2; thread B holds 2 and wants 1.",
            "<b>A global acquisition order makes a cycle impossible</b> "
            "— if everyone takes locks in the same order, no cycle can "
            "form.",
            "<b>So define the order, document it, and never violate "
            "it.</b> <code>std::scoped_lock</code> takes several locks "
            "deadlock-free in one call.",
            "<b>And hold locks for as short a time as possible</b> — "
            "never across I/O, never across a callback into code you do not "
            "control."]},

  {"t": "section", "label": "Part 2", "title": "Memory models",
   "blurb": "Why your writes are not where you left them."},

  {"t": "callout", "title": "Nothing happens in the order you wrote it",
   "kind": "The uncomfortable fact",
   "body": ["<b>The compiler reorders</b> — it may hoist, sink, merge, or "
            "eliminate memory operations to optimise.",
            "<b>The processor reorders</b> — out-of-order execution and "
            "store buffers mean writes become visible in a different order "
            "than issued.",
            "<b>Both are legal</b>, because both preserve single-threaded "
            "semantics. Which is all the hardware ever promised.",
            "<b>So without synchronisation, another thread may observe your "
            "writes in any order</b> — and a memory model is the contract "
            "that says when it may not."]},

  {"t": "eq", "kicker": "Orderings", "title": "The C++ memory orderings",
   "eqs": [
     ("seq_cst  —  a single total order all threads agree on",
      "The default. Strongest, simplest to reason about, and the most "
      "expensive on weakly ordered hardware."),
     ("acquire / release  —  a one-way barrier each",
      "A release store synchronises with an acquire load of the same "
      "variable. Everything before the release is visible after the "
      "acquire."),
     ("relaxed  —  atomicity only, no ordering",
      "The operation is indivisible and nothing else is guaranteed. For "
      "counters nobody reads until the end."),
   ],
   "caption": "Acquire-release is sufficient for most lock-free code and "
              "measurably cheaper than sequential consistency on ARM.",
   "note": "On x86, acquire-release is nearly free and seq_cst costs a "
           "fence; on ARM the difference is larger."},

  {"t": "callout", "title": "Sequential consistency is what you assume and not what you get",
   "kind": "The gap",
   "body": ["<b>Sequential consistency means there is one global order of "
            "all memory operations</b> consistent with each thread's program "
            "order.",
            "<b>It is what everyone intuitively assumes</b>, and no "
            "mainstream processor provides it by default — it would cost "
            "too much performance.",
            "<b>x86 is relatively strong</b> (total store order); "
            "<b>ARM and POWER are weak</b> and reorder much more freely.",
            "<b>So code that works on x86 can fail on ARM</b>, which is now "
            "a mainstream target. <b>Use the language's model, not your "
            "mental model of a processor.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Atomics in practice",
   "blurb": "When they help and when they do not."},

  {"t": "bullets", "kicker": "Atomics", "title": "What atomics are for",
   "items": [
     "<b>Counters and flags</b> — where a lock would be absurd overhead "
     "for a single word.",
     "",
     "<b>Compare-and-swap loops</b> for small lock-free updates "
     "(Module 05).",
     "",
     "<b>And they are not free.</b> An atomic read-modify-write locks the "
     "cache line; under contention it is slower than a mutex.",
     "",
     "<b>Contended atomics serialise just as locks do</b>, with the "
     "additional cost of repeated failed attempts.",
     "",
     "<b>So per-thread accumulation beats both</b> whenever it is "
     "possible, which is most of the time.",
   ],
   "note": "The 'atomics are not a free lock' point is the one that "
           "surprises people — contention is the cost, not the primitive."},

  {"t": "callout", "title": "The mistakes that recur",
   "kind": "A checklist",
   "body": ["<b>Double-checked locking without atomics.</b> The classic "
            "broken idiom; correct only with proper ordering.",
            "<b><code>if</code> instead of <code>while</code></b> on a "
            "condition variable (Part 1).",
            "<b>Holding a lock across I/O or a callback</b> — "
            "unpredictable duration, and possible re-entry.",
            "<b>Assuming <code>volatile</code> means atomic.</b> It does "
            "not, in C or C++; it prevents some compiler optimisations and "
            "says nothing about the processor.",
            "<b>And lock-free code written without the memory model</b>, "
            "which works until the architecture changes."]},
 ],
 "takeaways": [
   "A mutex costs tens of nanoseconds uncontended and far more contended; a "
   "reader-writer lock is more expensive than a mutex unless readers "
   "dominate.",
   "Condition variables must be waited on in a loop — spurious wakeups "
   "are permitted and the predicate may be consumed by another thread.",
   "Deadlock requires a cycle, so a documented global lock acquisition order "
   "makes it impossible.",
   "Both the compiler and the processor reorder memory operations, legally, "
   "because both preserve single-threaded semantics.",
   "Acquire-release is sufficient for most lock-free code and cheaper than "
   "sequential consistency, especially on weakly ordered hardware.",
   "Atomics are not a cheap lock — contended atomics serialise too. "
   "Per-thread accumulation beats both when possible.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Locks"),
  ("table", ["Primitive", "Provides", "Cost and caveats"],
   [["<b>Mutex</b>", "Mutual exclusion over a critical section.",
     "Roughly 20&ndash;100 ns uncontended; <b>under contention, far more</b>, "
     "because threads block and the operating system is involved."],
    ["<b>Reader-writer lock</b>",
     "Many concurrent readers, or one exclusive writer.",
     "<b>More expensive than a plain mutex when uncontended</b>, because the "
     "bookkeeping is heavier. <b>It only pays when reads genuinely "
     "dominate</b> and are long enough to matter — which is less often "
     "than people assume when reaching for it."],
    ["<b>Condition variable</b>",
     "Wait efficiently until a predicate becomes true.",
     "Requires an associated mutex, and <b>must be waited on in a "
     "loop</b> — see below."],
    ["<b>Atomic</b>", "An indivisible read-modify-write on one word.",
     "<b>The cheapest primitive</b>, and limited to word-sized operations. "
     "&sect;3."],
    ["<b>Barrier</b>", "All participating threads reach a point before any "
     "proceeds.",
     "<b>Costs the slowest thread's time, multiplied by the thread "
     "count</b> — which is why load imbalance is so expensive "
     "(Module 06)."],
    ["<b>Semaphore</b>", "A counted resource.",
     "General and correspondingly easy to misuse. Prefer a more specific "
     "primitive when one fits."]],
   [0.17, 0.33, 0.50]),
  ("code", """std::unique_lock<std::mutex> lk(m);
while (!ready)          // WHILE, not IF
    cv.wait(lk);

// or, preferably, the predicate overload which writes the loop for you:
cv.wait(lk, []{ return ready; });"""),
  ("callout", "The loop is not optional",
   ["<b>Spurious wakeups are explicitly permitted by the standard.</b> "
    "<code>wait()</code> may return without any corresponding "
    "<code>notify</code> having occurred, because allowing this makes the "
    "implementation substantially simpler and faster on some platforms.",
    "<b>And even without spurious wakeups, the predicate may have been "
    "consumed.</b> Between the notifying thread's <code>notify</code> and "
    "this thread reacquiring the mutex, another waiting thread may have woken "
    "first and taken the item.",
    "<b>With <code>if</code> rather than <code>while</code>, the code "
    "proceeds with the predicate false</b> — dequeuing from an empty "
    "queue, or using data that is not ready.",
    "<b>This is the single most common condition variable bug</b>, and the "
    "predicate overload of <code>wait()</code> exists specifically to make "
    "it hard to write. Use it."]),
  ("callout", "Lock ordering prevents deadlock",
   ["<b>Deadlock requires a cycle in the wait-for graph.</b> Thread A holds "
    "lock 1 and waits for lock 2; thread B holds lock 2 and waits for lock "
    "1. Neither can proceed.",
    "<b>A global acquisition order makes a cycle impossible.</b> If every "
    "thread always acquires locks in the same defined order — by "
    "address, by a documented hierarchy, by any consistent rule — then "
    "a thread holding a lower-ordered lock never waits for a higher-ordered "
    "one held by a thread waiting on a lower, and no cycle can form.",
    "<b>So define the order, document it where the locks are declared, and "
    "never violate it.</b> <code>std::scoped_lock</code> acquires several "
    "locks at once using a deadlock-avoidance algorithm, which handles the "
    "cases where a fixed order is awkward.",
    "<b>And hold locks for as short a time as possible.</b> Never across "
    "I/O, which has unbounded duration; never across a callback into code "
    "you do not control, which may re-enter and attempt to acquire the same "
    "lock. Both are common sources of deadlock in otherwise careful code."]),

  ("h1", "2 &nbsp; Memory models"),
  ("callout", "Nothing happens in the order you wrote it",
   ["<b>The compiler reorders memory operations.</b> It hoists loads out of "
    "loops, sinks stores past branches, merges adjacent accesses, and "
    "eliminates operations it can prove are redundant.",
    "<b>The processor reorders memory operations.</b> Out-of-order execution "
    "issues instructions as their operands become available, and store "
    "buffers allow a write to be committed to the processor's own view long "
    "before it becomes visible to others.",
    "<b>Both are entirely legal</b>, because both preserve the semantics of "
    "a <i>single-threaded</i> program. That is the only guarantee the "
    "hardware ever offered, and it is sufficient for the overwhelming "
    "majority of code.",
    "<b>So without synchronisation, another thread may observe your writes "
    "in a different order than you performed them</b> — and may observe "
    "some and not others. <b>A memory model is the contract specifying "
    "exactly when that may not happen</b>, which is why a language needs one "
    "before it can support threads at all."]),
  ("table", ["Ordering", "Guarantee", "When to use"],
   [["<b>seq_cst</b> (sequential consistency)",
     "A single total order of all sequentially consistent operations, which "
     "every thread agrees on.",
     "<b>The default, and the right default.</b> Strongest and simplest to "
     "reason about. The most expensive on weakly ordered hardware, and "
     "nearly free on x86."],
    ["<b>acquire / release</b>",
     "A release store synchronises-with an acquire load of the same "
     "variable: everything sequenced before the release becomes visible to "
     "everything sequenced after the acquire. A one-way barrier in each "
     "direction.",
     "<b>Sufficient for most lock-free data structures</b>, and measurably "
     "cheaper than seq_cst on ARM and POWER. This is what a mutex does "
     "internally."],
    ["<b>relaxed</b>",
     "Atomicity only — the operation is indivisible. <b>No ordering "
     "guarantees whatsoever.</b>",
     "Counters that nobody reads until a later synchronisation point; "
     "statistics; reference counts on increment. <b>Easy to misuse.</b>"]],
   [0.20, 0.42, 0.38]),
  ("callout", "Sequential consistency is what you assume and not what you get",
   ["<b>Sequential consistency means there exists a single global ordering "
    "of all memory operations, consistent with each thread's program "
    "order.</b> It is the model everyone reasons with intuitively, and "
    "almost everyone assumes without realising they are assuming it.",
    "<b>No mainstream processor provides it by default</b>, because it would "
    "forbid store buffering and most memory-level parallelism, at a large "
    "performance cost.",
    "<b>x86 is comparatively strong</b> — total store order, which "
    "permits only store-load reordering. <b>ARM and POWER are weak</b> and "
    "reorder far more freely.",
    "<b>So code that works correctly on x86 can fail on ARM</b>, which is "
    "now a mainstream target in servers, laptops, and phones — and the "
    "failure appears as an impossible result, not a crash. <b>Reason using "
    "the language's memory model rather than your mental model of a "
    "particular processor</b>, and the code is portable by construction."]),

  ("break",),
  ("h1", "3 &nbsp; Atomics in practice"),
  ("ul", ["<b>Counters and flags.</b> A single word updated by many "
          "threads, where taking a mutex would be absurd overhead relative "
          "to the operation.",
          "<b>Compare-and-swap loops</b> for small lock-free updates "
          "(Module 05) — read the current value, compute the new one, "
          "and swap it in only if nothing changed meanwhile.",
          "<b>And they are not free.</b> An atomic read-modify-write "
          "acquires exclusive ownership of the cache line, so concurrent "
          "atomics on the same address serialise at the coherence layer. "
          "<b>Under heavy contention an atomic counter can be slower than a "
          "mutex</b>, because the mutex at least lets a thread sleep instead "
          "of spinning on a line it keeps losing.",
          "<b>Contended atomics serialise exactly as locks do</b>, with the "
          "additional cost of repeated failed CAS attempts whose work is "
          "discarded. <b>The primitive is cheap; the contention is "
          "not</b> — and it is the contention that costs.",
          "<b>So per-thread accumulation beats both</b> whenever the "
          "operation is associative and the combination can be deferred, "
          "which covers most reductions and most counters. This is the same "
          "conclusion as Module 03's reduction clause, reached from the "
          "hardware side."]),
  ("callout", "The mistakes that recur",
   ["<b>Double-checked locking without atomics.</b> Checking a flag, taking "
    "a lock, checking again, and initialising. <b>The classic broken "
    "idiom</b> — without proper memory ordering, another thread can see "
    "the flag set before the initialisation it guards is visible. Correct "
    "only with acquire-release or seq_cst atomics, and "
    "<code>std::call_once</code> or a function-local static is simpler and "
    "correct by construction.",
    "<b><code>if</code> instead of <code>while</code> on a condition "
    "variable</b> (&sect;1).",
    "<b>Holding a lock across I/O or across a callback.</b> I/O has "
    "unbounded duration, so the critical section does too; a callback may "
    "re-enter and attempt to acquire the same lock, which deadlocks "
    "immediately with a non-recursive mutex.",
    "<b>Assuming <code>volatile</code> means atomic.</b> <b>It does not</b>, "
    "in C or C++. It prevents certain compiler optimisations — which is "
    "why it works for memory-mapped hardware registers — and says "
    "nothing whatsoever about processor reordering or about atomicity. Java "
    "and C# give it different meanings, which is a substantial source of the "
    "confusion.",
    "<b>And lock-free code written without reference to the memory "
    "model</b>, which works on the machine it was tested on and fails when "
    "the architecture changes."]),
 ],
 "resources": [
   ("Herlihy & Shavit &mdash; The Art of Multiprocessor Programming",
    "https://www.sciencedirect.com/book/9780123973375/",
    "The reference for this module and Module 05. Library copy; the authors' "
    "slides are free and cover the core material."),
   ("Preshing on Programming &mdash; memory ordering articles (free)",
    "https://preshing.com/",
    "<b>The clearest free explanation of acquire-release and memory "
    "ordering</b>, with diagrams and runnable examples. Start here if "
    "&sect;2 is unfamiliar."),
   ("Sutter &mdash; atomic Weapons (free talks)",
    "https://herbsutter.com/2013/02/11/atomic-weapons-the-c-memory-model-and-modern-hardware/",
    "The C++ memory model in two talks, by someone who helped specify it."),
   ("Sorin, Hill & Wood &mdash; A Primer on Memory Consistency and Cache "
    "Coherence (free)",
    "https://link.springer.com/book/10.1007/978-3-031-01764-3",
    "The hardware side of &sect;2, rigorously. Free through many "
    "institutions."),
 ],
 "exercises": [
   "Measure uncontended and contended mutex cost on your machine, as a "
   "function of thread count.",
   "Measure a reader-writer lock against a mutex at several read/write "
   "ratios. Find the ratio at which it starts to win.",
   "Write a condition variable wait with <code>if</code> and construct a "
   "case where it fails. Then fix it.",
   "Construct a deadlock with two locks acquired in opposite orders, then "
   "fix it with a defined order and with <code>std::scoped_lock</code>.",
   "<b>Write a store-buffer litmus test</b> — two threads, each storing "
   "to one variable and loading the other — and run it millions of "
   "times. Confirm that both loads returning zero is observable on x86.",
   "Run the same test with seq_cst atomics and confirm the outcome "
   "disappears.",
   "Measure the cost of seq_cst against acquire-release on your hardware. "
   "Compare x86 and ARM if you have access to both.",
   "Implement an atomic counter and a per-thread accumulator. Measure both "
   "at 1, 4, and 32 threads and plot the crossover.",
   "Implement double-checked locking incorrectly, then correctly, then "
   "replace it with a function-local static.",
 ],
 "selfcheck": [
   "Name six synchronisation primitives with their costs, and say when a "
   "reader-writer lock pays.",
   "Why must a condition variable be waited on in a loop? Give two reasons.",
   "What does deadlock require, and what single rule prevents it?",
   "Why do the compiler and processor reorder memory operations, and why is "
   "it legal?",
   "Describe the three C++ memory orderings and when each is appropriate.",
   "What is sequential consistency, and why does hardware not provide it?",
   "Why are contended atomics not cheap, and what beats them?",
   "Name five recurring synchronisation mistakes.",
   "What does <code>volatile</code> actually mean in C++?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Lock-Free Programming",
 "subtitle": "Progress guarantees, and whether you need them.",
 "question": "When is lock-free worth the difficulty?",
 "outcomes": [
     "Define the progress guarantees precisely.",
     "Implement a compare-and-swap loop.",
     "Explain the ABA problem and its solutions.",
     "Explain safe memory reclamation.",
     "Judge honestly when lock-free is warranted.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Progress guarantees",
   "blurb": "Precise terms, usually used loosely."},

  {"t": "table", "kicker": "Guarantees", "title": "The hierarchy",
   "header": ["Guarantee", "Means", "Implies"],
   "widths": [2.8, 5.0, 4.3],
   "rows": [
     ["<b>Wait-free</b>", "<b>Every</b> thread completes in bounded steps", "<b>Strongest; rare</b>"],
     ["<b>Lock-free</b>", "<b>Some</b> thread makes progress", "System-wide progress"],
     ["Obstruction-free", "A thread running alone completes", "Weakest non-blocking"],
     ["<b>Blocking</b>", "A suspended thread can stall others", "<b>What a mutex gives</b>"],
   ],
   "footnote": "<b>Lock-free does not mean fast.</b> It is a progress "
               "guarantee, and it is frequently slower than a good mutex.",
   "note": "The name is the problem — 'lock-free' sounds like a "
           "performance claim and is a liveness claim."},

  {"t": "callout", "title": "Lock-free is a liveness property, not a speed claim",
   "kind": "The misunderstanding",
   "body": ["<b>Lock-free guarantees that <i>some</i> thread makes "
            "progress</b>, even if others are suspended arbitrarily.",
            "<b>It says nothing about throughput.</b> A lock-free structure "
            "under contention can perform worse than a mutex, because failed "
            "CAS attempts discard completed work.",
            "<b>Where it genuinely matters:</b> real-time systems where a "
            "priority-inverted thread cannot be tolerated; signal handlers; "
            "and code that may be interrupted by a thread that never "
            "resumes.",
            "<b>If you want speed, measure.</b> The answer is frequently "
            "that a mutex, or avoiding sharing entirely, wins."]},

  {"t": "section", "label": "Part 2", "title": "Compare and swap",
   "blurb": "The primitive everything is built on."},

  {"t": "code", "kicker": "CAS", "title": "The standard loop",
   "lang": "cpp", "code": """
// Atomically apply f to a shared value.
template <class F>
void atomic_update(std::atomic<int>& v, F f) {
    int old = v.load(std::memory_order_relaxed);
    int desired;
    do {
        desired = f(old);
    } while (!v.compare_exchange_weak(
                 old, desired,
                 std::memory_order_release,     // on success
                 std::memory_order_relaxed));   // on failure
    // NOTE: compare_exchange_weak UPDATES `old` on failure,
    // so the loop retries with the fresh value automatically.
}

// compare_exchange_WEAK may fail spuriously and is cheaper on
// LL/SC architectures (ARM, POWER). In a loop, always use weak.
// Outside a loop, use strong.
""",
   "caption": "The weak/strong distinction matters on ARM and POWER, where "
              "load-linked/store-conditional can fail without contention.",
   "note": "The weak-in-a-loop rule is a small thing that is consistently "
           "got wrong."},

  {"t": "callout", "title": "The ABA problem",
   "kind": "Why CAS is not enough",
   "body": ["<b>CAS checks that a value is unchanged, not that nothing "
            "happened.</b>",
            "<b>Thread 1 reads A. Threads 2 and 3 change it to B and back "
            "to A.</b> Thread 1's CAS succeeds, because the value matches.",
            "<b>But the world changed</b> — in a linked structure, the "
            "node at that address may have been freed and reallocated for "
            "something else entirely.",
            "<b>Solutions:</b> a tagged pointer with a version counter "
            "incremented on every change; double-width CAS; or a memory "
            "reclamation scheme that prevents reuse (Part 3)."]},

  {"t": "section", "label": "Part 3", "title": "Memory reclamation",
   "blurb": "The genuinely hard part."},

  {"t": "callout", "title": "You cannot free a node someone might still be reading",
   "kind": "The core difficulty of lock-free structures",
   "body": ["<b>With a lock, you know nobody else is in the structure.</b> "
            "Freeing is safe.",
            "<b>Without one, a thread may be holding a pointer to a node "
            "you have just unlinked</b> — and have no way to tell you.",
            "<b>Freeing it is a use-after-free</b>, which is the hardest "
            "class of bug to diagnose.",
            "<b>This, not the algorithm, is what makes lock-free data "
            "structures difficult.</b> Writing a lock-free stack is an "
            "afternoon; reclaiming its memory correctly is the project."]},

  {"t": "table", "kicker": "Reclamation", "title": "Safe reclamation schemes",
   "header": ["Scheme", "Idea", "Cost"],
   "widths": [3.0, 4.8, 4.3],
   "rows": [
     ["<b>Hazard pointers</b>", "Each thread publishes what it is reading", "<b>A store and fence per access</b>"],
     ["<b>Epoch-based (RCU)</b>", "Free only after all threads pass an epoch", "<b>Cheap reads; delayed frees</b>"],
     ["Reference counting", "Count readers atomically", "<b>Atomic per access; contended</b>"],
     ["Never free", "Leak, or use a pool", "<b>Viable more often than it sounds</b>"],
   ],
   "footnote": "<b>RCU is the standard answer where reads dominate</b> and "
               "is used throughout the Linux kernel.",
   "note": "The 'never free' option is genuinely reasonable for bounded "
           "structures and is underused."},

  {"t": "section", "label": "Part 4", "title": "Judgement",
   "blurb": "When to reach for this."},

  {"t": "bullets", "kicker": "Before you start", "title": "Questions to ask first",
   "items": [
     "<b>Can you avoid sharing?</b> Per-thread state and a final "
     "combination removes the problem entirely.",
     "",
     "<b>Can you shard?</b> Many locks over disjoint partitions scales "
     "nearly as well and is far simpler.",
     "",
     "<b>Have you measured the mutex?</b> It is frequently not the "
     "bottleneck you assumed.",
     "",
     "<b>Do you need the progress guarantee</b>, or do you want speed? "
     "They are different requirements.",
     "",
     "<b>Is there a library?</b> Use it. Correct lock-free structures are "
     "research contributions.",
   ],
   "note": "This list is the module's practical content. Most people "
           "reaching for lock-free should stop at line one."},

  {"t": "callout", "title": "Use a library",
   "kind": "The honest recommendation",
   "body": ["<b>Correct lock-free data structures are published as research "
            "papers</b>, and several well-known published ones had bugs "
            "found years later.",
            "<b>The memory model subtleties, the ABA cases, and the "
            "reclamation scheme each offer many ways to be subtly "
            "wrong</b> — and the failures are rare, non-reproducible, and "
            "catastrophic.",
            "<b>Use a tested implementation</b> — Boost.Lockfree, "
            "folly, libcds, or your platform's concurrent collections.",
            "<b>Write your own to understand them</b>, which is what this "
            "module is for. <b>Ship someone else's.</b>"]},
 ],
 "takeaways": [
   "Wait-free guarantees every thread completes in bounded steps; lock-free "
   "guarantees some thread progresses; blocking means a suspended thread can "
   "stall others.",
   "Lock-free is a liveness property, not a speed claim — under "
   "contention it is frequently slower than a mutex.",
   "The CAS loop is the basic primitive; use compare_exchange_weak inside a "
   "loop and strong outside one.",
   "ABA: CAS checks that a value is unchanged, not that nothing happened "
   "— the address may have been freed and reused.",
   "Safe memory reclamation, not the algorithm, is what makes lock-free "
   "structures hard. Writing the stack is an afternoon; freeing its nodes is "
   "the project.",
   "Ask first whether you can avoid sharing or shard the locks, and then use "
   "a library — correct lock-free structures are research "
   "contributions.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Progress guarantees"),
  ("table", ["Guarantee", "Definition", "Assessment"],
   [["<b>Wait-free</b>",
     "<b>Every</b> thread completes its operation in a bounded number of "
     "its own steps, regardless of what other threads do.",
     "<b>The strongest guarantee, and rare in practice.</b> Required in "
     "hard real-time systems. Wait-free versions of common structures exist "
     "and are substantially slower."],
    ["<b>Lock-free</b>",
     "<b>Some</b> thread makes progress in a bounded number of steps. An "
     "individual thread may retry indefinitely.",
     "System-wide progress is guaranteed; individual starvation is not "
     "excluded. <b>This is what most 'lock-free' structures provide.</b>"],
    ["<b>Obstruction-free</b>",
     "A thread running in isolation completes in a bounded number of steps.",
     "The weakest non-blocking guarantee. Permits livelock when threads "
     "contend; requires a contention manager in practice."],
    ["<b>Blocking</b>",
     "A thread suspended while holding a lock can prevent all others from "
     "progressing.",
     "<b>What a mutex provides.</b> Entirely adequate for most purposes."]],
   [0.17, 0.40, 0.43]),
  ("callout", "Lock-free is a liveness property, not a speed claim",
   ["<b>The name is the problem.</b> 'Lock-free' sounds like a performance "
    "claim and is a <i>liveness</i> claim: it guarantees that some thread "
    "makes progress even if others are suspended arbitrarily — "
    "descheduled, page-faulted, or terminated.",
    "<b>It says nothing about throughput.</b> A lock-free structure under "
    "heavy contention can perform considerably worse than a mutex-protected "
    "one, because every failed compare-and-swap discards work that was "
    "already done, and the retries add load that causes more failures.",
    "<b>Where the guarantee genuinely matters:</b> hard real-time systems "
    "where a priority-inverted thread holding a lock is unacceptable; signal "
    "handlers, which cannot safely take a lock that the interrupted code may "
    "hold; and any context where a thread might be stopped and never "
    "resumed.",
    "<b>If what you want is speed, measure.</b> The answer is frequently "
    "that a well-placed mutex wins, and more frequently still that "
    "restructuring to avoid the sharing wins by more than either "
    "(&sect;4)."]),

  ("h1", "2 &nbsp; Compare and swap"),
  ("code", """template <class F>
void atomic_update(std::atomic<int>& v, F f) {
    int old = v.load(std::memory_order_relaxed);
    int desired;
    do {
        desired = f(old);
    } while (!v.compare_exchange_weak(old, desired,
                 std::memory_order_release,     // success
                 std::memory_order_relaxed));   // failure
    // compare_exchange_weak UPDATES `old` on failure, so the loop
    // automatically retries against the fresh value.
}"""),
  ("p", "<b>Use <code>compare_exchange_weak</code> inside a loop and "
        "<code>compare_exchange_strong</code> outside one.</b> The weak form "
        "is permitted to fail spuriously — to report a mismatch when "
        "the values in fact matched — which allows a cheaper "
        "implementation on load-linked/store-conditional architectures such "
        "as ARM and POWER, where an intervening cache event can invalidate "
        "the reservation. Inside a loop a spurious failure simply causes "
        "another iteration, so the cheaper form is free; outside a loop it "
        "would be a bug."),
  ("callout", "The ABA problem",
   ["<b>Compare-and-swap checks that a value is unchanged. It does not "
    "check that nothing happened.</b>",
    "<b>Thread 1 reads the value A and is descheduled. Thread 2 changes it "
    "to B. Thread 3 changes it back to A. Thread 1 resumes and its CAS "
    "succeeds</b>, because the value it compares against does indeed equal "
    "A.",
    "<b>But the world has changed.</b> In a linked structure, where the "
    "value is a pointer, the node at that address may have been popped, "
    "freed, and the memory reallocated for something entirely different. "
    "Thread 1 proceeds on the assumption that its cached view of the "
    "structure is still valid, and it is not.",
    "<b>Solutions:</b> a <b>tagged pointer</b> that packs a version counter "
    "alongside the pointer and increments it on every modification, so the "
    "value never genuinely repeats; <b>double-width CAS</b>, which swaps "
    "pointer and counter atomically; or a <b>memory reclamation scheme</b> "
    "that prevents the address being reused while anyone might still be "
    "looking at it — which is &sect;3, and which is needed anyway."]),

  ("break",),
  ("h1", "3 &nbsp; Safe memory reclamation"),
  ("callout", "You cannot free a node someone might still be reading",
   ["<b>With a lock, reclamation is trivial.</b> Holding the lock means no "
    "other thread is inside the structure, so a node that has been unlinked "
    "can be freed immediately.",
    "<b>Without one, a thread may be holding a pointer to the node you have "
    "just unlinked</b> — it read the pointer before you removed it, and "
    "it has no way of telling you so and no obligation to check.",
    "<b>Freeing it is a use-after-free</b>, which is both a correctness "
    "catastrophe and a security vulnerability, and among the hardest classes "
    "of bug to diagnose because the symptom appears far from the cause.",
    "<b>This, rather than the algorithm, is what makes lock-free data "
    "structures difficult.</b> Writing a lock-free stack from the published "
    "algorithm is an afternoon's work. <b>Reclaiming its memory correctly is "
    "the project</b>, and it is where the published algorithms were found to "
    "have bugs."]),
  ("table", ["Scheme", "Mechanism", "Cost and use"],
   [["<b>Hazard pointers</b>",
     "Each thread publishes, in a globally visible slot, the pointers it is "
     "currently dereferencing. A thread wishing to free a node first checks "
     "that no hazard pointer references it.",
     "<b>A store and a memory fence on every access</b>, which is "
     "significant for read-heavy workloads. Bounded memory usage, which is "
     "its advantage."],
    ["<b>Epoch-based reclamation (RCU)</b>",
     "Threads announce entry to and exit from a read-side critical section. "
     "A node may be freed once every thread has passed through a quiescent "
     "point since it was unlinked.",
     "<b>Reads are extremely cheap</b> — essentially free in the kernel "
     "variant. Frees are deferred, so memory usage is unbounded if a thread "
     "stalls. <b>The standard answer where reads dominate</b>, and it is "
     "used pervasively in the Linux kernel."],
    ["<b>Reference counting</b>",
     "An atomic counter per node, incremented on acquisition.",
     "<b>An atomic operation per access, on shared data</b> — which is "
     "exactly the contention the structure was meant to avoid. Simple and "
     "frequently the slowest."],
    ["<b>Never free</b>",
     "Leak the nodes, or allocate from a fixed pool that is reused only when "
     "the structure is known to be quiescent.",
     "<b>More viable than it sounds</b>, and underused. For a bounded "
     "structure with a bounded lifetime, or one whose nodes are recycled "
     "through a type-stable pool, this removes the entire problem."]],
   [0.19, 0.40, 0.41]),

  ("h1", "4 &nbsp; Judgement"),
  ("ol", ["<b>Can you avoid sharing altogether?</b> Per-thread state with a "
          "final combination has no concurrency problem to solve "
          "(Modules 03, 04). <b>Most people reaching for lock-free should "
          "stop here.</b>",
          "<b>Can you shard the structure?</b> Many locks over disjoint "
          "partitions — a lock per hash bucket, a queue per thread "
          "— scales nearly as well as lock-free and is far simpler to "
          "get right.",
          "<b>Have you measured the mutex?</b> It is frequently not the "
          "bottleneck that was assumed. An uncontended mutex costs tens of "
          "nanoseconds, and if the critical section is longer than that the "
          "lock is not the problem.",
          "<b>Do you need the progress guarantee, or do you want speed?</b> "
          "These are different requirements with different answers, and "
          "conflating them is how people end up with slower, harder code.",
          "<b>Is there a tested library implementation?</b> There usually "
          "is."]),
  ("callout", "Use a library",
   ["<b>Correct lock-free data structures are published as research "
    "papers</b>, and <b>several well-known published algorithms had bugs "
    "discovered years after publication</b> — by people specifically "
    "looking, with model checkers.",
    "<b>The memory model subtleties, the ABA cases, and the reclamation "
    "scheme each admit many ways to be subtly wrong</b>, and the resulting "
    "failures share the worst possible combination of properties: rare, "
    "non-reproducible, architecture-dependent, and catastrophic.",
    "<b>Use a tested implementation.</b> Boost.Lockfree, Facebook's folly, "
    "libcds, Java's <code>java.util.concurrent</code>, or your platform's "
    "concurrent collections. These have been exercised by far more code than "
    "yours will be.",
    "<b>Write your own in order to understand them</b>, which is what this "
    "module and its exercises are for. <b>Ship someone else's.</b> That is "
    "not a lack of ambition; it is the correct engineering judgement for a "
    "component whose failure mode is silent corruption."]),
 ],
 "resources": [
   ("Herlihy & Shavit &mdash; The Art of Multiprocessor Programming",
    "https://www.sciencedirect.com/book/9780123973375/",
    "The standard text. Progress guarantees, CAS, and the classic lock-free "
    "structures, with proofs."),
   ("Michael &mdash; Hazard Pointers (free)",
    "https://www.cs.otago.ac.nz/cosc440/readings/hazard-pointers.pdf",
    "The reclamation scheme of &sect;3, in the original."),
   ("McKenney &mdash; Is Parallel Programming Hard, And, If So, What Can "
    "You Do About It? (free book)",
    "https://mirrors.edge.kernel.org/pub/linux/kernel/people/paulmck/perfbook/perfbook.html",
    "<b>Free, enormous, and excellent</b>, especially on RCU, which the "
    "author designed. The honest-judgement material in &sect;4 is "
    "throughout."),
   ("Fedor Pikus &mdash; talks on lock-free programming (free)",
    "https://www.youtube.com/results?search_query=fedor+pikus+lock+free",
    "Practical, measured, and unusually honest about when lock-free loses."),
 ],
 "exercises": [
   "Implement a lock-free stack with CAS. Verify it with a stress test and "
   "ThreadSanitizer.",
   "Measure it against a mutex-protected stack at 1, 2, 4, 8, and 32 "
   "threads. <b>Plot both and find where lock-free loses.</b>",
   "Measure both against per-thread stacks combined at the end.",
   "<b>Construct an ABA failure</b> deliberately, with a slow thread and a "
   "recycled node. This requires care and is instructive.",
   "Fix it with a tagged pointer and confirm the failure disappears.",
   "Implement hazard pointers for your stack and measure the read-side "
   "cost.",
   "Implement epoch-based reclamation and compare the read cost and the "
   "memory high-water mark against hazard pointers.",
   "Replace reclamation entirely with a type-stable pool and compare.",
   "Benchmark your implementation against Boost.Lockfree. Report the gap "
   "honestly.",
   "For a sharing problem in your Project 1 code, work through the five "
   "questions of &sect;4 and document the decision.",
 ],
 "selfcheck": [
   "Define wait-free, lock-free, obstruction-free, and blocking.",
   "Why is lock-free not a speed claim, and where does the guarantee "
   "genuinely matter?",
   "Write a CAS loop and say when to use weak rather than strong.",
   "Explain the ABA problem and give three solutions.",
   "Why can you not simply free an unlinked node, and why is this the hard "
   "part?",
   "Compare four reclamation schemes on mechanism and cost.",
   "Give the five questions to ask before writing lock-free code.",
   "Why is using a library the right recommendation?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Decomposition and Load Balancing",
 "subtitle": "Dividing the work so that nobody waits.",
 "question": "How do you split a problem so all the cores stay busy?",
 "outcomes": [
     "Choose a decomposition strategy for a problem.",
     "Explain granularity and its trade-off.",
     "Implement work stealing and explain why it balances.",
     "Recognise load imbalance in a profile.",
     "Apply the standard parallel patterns.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Decomposition",
   "blurb": "Four ways to divide a problem."},

  {"t": "table", "kicker": "Strategies", "title": "Decomposition strategies",
   "header": ["Strategy", "Divide by", "Suits"],
   "widths": [2.8, 4.4, 4.9],
   "rows": [
     ["<b>Data (domain)</b>", "Regions of the data", "<b>Arrays, grids, images</b>"],
     ["Task (functional)", "Different operations", "Pipelines, heterogeneous work"],
     ["<b>Recursive</b>", "Divide and conquer", "<b>Trees, sorts, spatial structures</b>"],
     ["Pipeline", "Stages of a sequence", "Streaming; bounded by the slowest stage"],
   ],
   "footnote": "<b>Data decomposition scales with the data; task "
               "decomposition scales with the number of distinct tasks</b>, "
               "which is usually small.",
   "note": "That task parallelism does not scale is the key practical "
           "limitation and is often missed."},

  {"t": "callout", "title": "Granularity is the central trade-off",
   "kind": "Too fine or too coarse",
   "body": ["<b>Too coarse:</b> few chunks, so load imbalance is severe and "
            "the tail dominates. With four chunks on four cores, one slow "
            "chunk wastes three cores.",
            "<b>Too fine:</b> scheduling overhead dominates the work. A task "
            "costing a microsecond does not justify a queue operation.",
            "<b>The rule of thumb: enough chunks that imbalance averages "
            "out</b> — typically several times the thread count — "
            "<b>each large enough to amortise the scheduling cost</b>.",
            "<b>And measure.</b> The right granularity depends on the "
            "per-item cost and the runtime, and it is easy to find "
            "empirically."]},

  {"t": "section", "label": "Part 2", "title": "Load balancing",
   "blurb": "Nobody finishes early."},

  {"t": "callout", "title": "A barrier costs the slowest thread's time, n times",
   "kind": "Why imbalance is so expensive",
   "body": ["<b>At a barrier, every thread waits for the last one.</b> So "
            "the cost of the phase is the maximum, not the average.",
            "<b>If one thread takes twice as long, every other thread idles "
            "for half the phase.</b> With 32 threads that is 31 cores doing "
            "nothing.",
            "<b>And this is invisible in total CPU time</b> — the idle "
            "threads are spinning or sleeping, not computing.",
            "<b>So imbalance goes straight into Amdahl's serial "
            "fraction</b> (Module 01), and it is frequently the largest "
            "contributor."]},

  {"t": "two", "kicker": "Two approaches", "title": "Static and dynamic balancing",
   "lh": "Static",
   "l": ["Assign work up front, equally.",
         "<b>No runtime overhead at all.</b>",
         "<b>Good locality</b> — each thread owns a contiguous region.",
         ("Requires the cost per item to be known and uniform.", 1),
         "Fails completely under skew."],
   "rh": "Dynamic",
   "r": ["Threads take work as they become free.",
         "<b>Balances automatically</b>, whatever the cost distribution.",
         "<b>Costs a queue operation per chunk</b>, and locality suffers.",
         ("Requires work to be divisible at runtime.", 1),
         "The general answer."],
   "note": "The locality cost of dynamic scheduling is real and is why "
           "static still wins for uniform work."},

  {"t": "code", "kicker": "Work stealing", "title": "The scheduler that balances itself",
   "lang": "text", "code": """
  Each worker has its OWN double-ended queue (deque).

  OWN work:    push and pop at the BOTTOM  -- LIFO
     -> the most recently pushed task is popped first
     -> that task's data is still in cache. GOOD LOCALITY.
     -> and it is the deepest in a recursion, so it is small.

  STEALING:    thieves take from the TOP of a victim's deque -- FIFO
     -> the OLDEST task, which is the LARGEST remaining subtree
     -> so one steal transfers a lot of work
     -> and the thief and victim touch opposite ends, so the
        common case needs no synchronisation at all

  Idle worker: pick a random victim and try to steal. Repeat.

  *** The LIFO-own / FIFO-steal asymmetry is the whole design. ***
""",
   "caption": "Local LIFO for cache locality, remote FIFO to steal large "
              "chunks, opposite ends to avoid contention. Three properties "
              "from one structure.",
   "note": "This is one of the most elegant designs in the course and is "
           "worth presenting as such."},

  {"t": "callout", "title": "Why work stealing is near-optimal",
   "kind": "The result",
   "body": ["<b>Blumofe and Leiserson proved</b> that randomised work "
            "stealing achieves expected time within a constant factor of "
            "optimal, with provably bounded space and communication.",
            "<b>It requires no knowledge of task costs</b>, which is what "
            "makes it practical — the costs are usually unknowable in "
            "advance.",
            "<b>It adapts to whatever the machine is doing</b>, including "
            "other processes competing for cores.",
            "<b>And it is what Cilk, TBB, OpenMP tasks, Go, Rust's rayon, "
            "and .NET's task scheduler all use.</b> The convergence is not "
            "coincidence."]},

  {"t": "section", "label": "Part 3", "title": "Patterns",
   "blurb": "The shapes that recur."},

  {"t": "table", "kicker": "Patterns", "title": "The standard parallel patterns",
   "header": ["Pattern", "Shape", "Parallelism"],
   "widths": [2.6, 4.8, 4.7],
   "rows": [
     ["<b>Map</b>", "Apply f to every element", "<b>Trivially parallel</b>"],
     ["<b>Reduce</b>", "Combine all elements with an associative op", "<b>Tree; O(log n) depth</b>"],
     ["<b>Scan</b>", "All prefix sums", "<b>Looks serial; is not</b> (Module 11)"],
     ["Stencil", "Each output from a neighbourhood", "Parallel with halo exchange"],
     ["Gather / scatter", "Indexed read / write", "<b>Scatter needs conflict handling</b>"],
     ["Partition", "Split by a predicate", "Scan over flags"],
   ],
   "footnote": "<b>Recognising the pattern gives you the parallel "
               "algorithm</b>, the complexity, and usually a library "
               "implementation.",
   "note": "Pattern recognition is the most practically useful skill here "
           "— most code is a composition of these six."},

  {"t": "callout", "title": "Associativity is what makes reduction parallel",
   "kind": "The requirement",
   "body": ["<b>A reduction can be computed as a tree only if the operator "
            "is associative</b> — (a⊕b)⊕c must equal "
            "a⊕(b⊕c).",
            "<b>Addition of integers is associative. Addition of floats is "
            "not.</b>",
            "<b>So a parallel float reduction gives a different answer than "
            "the serial one</b>, and a different answer for different thread "
            "counts.",
            "<b>This is not a bug, and it must be expected.</b> If "
            "bitwise reproducibility matters, fix the reduction order "
            "explicitly and accept the cost."]},
 ],
 "takeaways": [
   "Data decomposition scales with the data; task decomposition scales with "
   "the number of distinct tasks, which is usually small.",
   "Granularity trades load imbalance against scheduling overhead — "
   "enough chunks to average out imbalance, each large enough to amortise "
   "the queue.",
   "A barrier costs the slowest thread's time multiplied by the thread "
   "count, so imbalance goes straight into Amdahl's serial fraction.",
   "Work stealing uses LIFO locally for cache locality and FIFO remotely to "
   "steal large subtrees, with thief and victim at opposite ends.",
   "Randomised work stealing is provably near-optimal, requires no knowledge "
   "of task costs, and is what every modern task runtime uses.",
   "Floating-point addition is not associative, so a parallel reduction "
   "gives a different answer than the serial one — expect it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Decomposition"),
  ("table", ["Strategy", "Divides by", "Suits", "Scales with"],
   [["<b>Data (domain) decomposition</b>",
     "Regions of the data — rows, blocks, tiles, particles.",
     "<b>Arrays, grids, images, meshes.</b> The dominant strategy in "
     "numerical work.", "<b>The size of the data.</b>"],
    ["<b>Task (functional) decomposition</b>",
     "Different operations performed concurrently.",
     "Heterogeneous work, pipelines, programs with distinct phases.",
     "<b>The number of distinct tasks</b> — which is usually small and "
     "fixed, so <b>this does not scale</b>. A frequently missed limitation."],
    ["<b>Recursive decomposition</b>",
     "Divide and conquer — split, recurse, combine.",
     "<b>Trees, sorts, spatial structures, anything already recursive.</b>",
     "The depth of the recursion, which grows with the data."],
    ["<b>Pipeline</b>", "Stages of a sequential process, with data flowing "
     "through.",
     "Streaming workloads where each item passes through the same stages.",
     "The number of stages — and <b>throughput is bounded by the "
     "slowest stage</b>, so balancing the stages is the whole problem."]],
   [0.21, 0.26, 0.30, 0.23]),
  ("callout", "Granularity is the central trade-off",
   ["<b>Too coarse</b> and load imbalance dominates. With four chunks "
    "distributed over four cores, a single chunk that takes twice as long "
    "leaves three cores idle for half the phase, and no scheduler can "
    "recover — there is nothing left to redistribute.",
    "<b>Too fine</b> and scheduling overhead dominates the useful work. A "
    "task that takes one microsecond does not justify a queue push, a queue "
    "pop, and the cache traffic between them.",
    "<b>The rule of thumb: create enough chunks that imbalance averages "
    "out</b> — commonly several times the thread count, so that a slow "
    "chunk is absorbed by its neighbours — <b>while keeping each chunk "
    "large enough to amortise the scheduling cost</b>, which means tens of "
    "microseconds or more for a typical task runtime.",
    "<b>And measure.</b> The correct granularity depends on the "
    "per-item cost and the runtime's overhead, both of which are specific to "
    "your situation and both of which are easy to determine empirically by "
    "sweeping the chunk size."]),

  ("h1", "2 &nbsp; Load balancing"),
  ("callout", "A barrier costs the slowest thread's time, n times over",
   ["<b>At a barrier, every thread waits for the last one to arrive.</b> So "
    "the wall-clock cost of a parallel phase is the <i>maximum</i> thread's "
    "time, not the average.",
    "<b>If one thread's share takes twice as long as the others', every "
    "other thread idles for half the phase.</b> On 32 threads that is 31 "
    "cores doing nothing for half the time — a loss of nearly 50% of "
    "the machine, caused by one thread.",
    "<b>And it is invisible in total CPU time</b>, because the waiting "
    "threads are either spinning (which looks like full utilisation) or "
    "sleeping (which looks like idle time with no attributable cause). "
    "Neither tells you which thread was slow or why.",
    "<b>So load imbalance goes directly into Amdahl's serial fraction</b> "
    "(Module 01), and in practice it is frequently the largest single "
    "contributor to it — larger than the genuinely sequential code it "
    "is usually blamed on."]),
  ("table", ["", "Static balancing", "Dynamic balancing"],
   [["Assignment", "Decided before the computation begins, in equal "
     "shares.", "Threads take work as they become free."],
    ["Runtime overhead", "<b>None at all.</b>",
     "A queue operation per chunk, plus the cache traffic it causes."],
    ["Locality", "<b>Good</b> — each thread owns a contiguous region "
     "and touches it repeatedly, which also places NUMA pages correctly "
     "(Module 02).",
     "<b>Worse</b> — a thread may process chunks scattered through "
     "memory, and which chunks it gets varies between runs."],
    ["Requires", "The per-item cost to be known and roughly uniform.",
     "The work to be divisible into chunks at runtime."],
    ["Under skew", "<b>Fails completely.</b>",
     "<b>Balances automatically.</b>"]],
   [0.17, 0.41, 0.42]),
  ("code", """Each worker owns a double-ended queue (deque).

OWN work:   push and pop at the BOTTOM -- LIFO
   -> most recently pushed task popped first: its data is in cache
   -> and it is deepest in the recursion, so it is small

STEALING:   thieves take from the TOP -- FIFO
   -> the oldest task, which is the LARGEST remaining subtree
   -> so one steal transfers a lot of work
   -> thief and victim touch opposite ends: no contention

Idle worker: pick a random victim, try to steal, repeat."""),
  ("callout", "The LIFO-own / FIFO-steal asymmetry is the whole design",
   ["<b>Popping your own work LIFO gives cache locality.</b> The most "
    "recently pushed task operates on data you have just touched, so it is "
    "still resident. A FIFO local order would touch the oldest data first, "
    "which is the coldest.",
    "<b>Stealing FIFO transfers large chunks.</b> In a recursive "
    "decomposition, the oldest task on the deque is the one highest in the "
    "recursion tree — which represents the <i>largest</i> remaining "
    "subtree. So a single steal transfers a great deal of work, and steals "
    "are consequently rare.",
    "<b>And thief and victim access opposite ends of the deque</b>, so in "
    "the common case where the deque is not nearly empty, the two never "
    "touch the same memory and no synchronisation is needed at all. Only the "
    "nearly-empty case requires a CAS.",
    "<b>Three desirable properties fall out of one data structure "
    "choice</b>, which is why this design is used essentially universally "
    "and why it is worth studying as a piece of engineering rather than just "
    "learning the interface."]),
  ("callout", "Work stealing is provably near-optimal",
   ["<b>Blumofe and Leiserson proved</b> that randomised work stealing "
    "completes a computation in expected time within a constant factor of "
    "the optimal schedule, with provably bounded space usage and bounded "
    "communication. This is an unusually strong result for a scheduling "
    "heuristic.",
    "<b>It requires no advance knowledge of task costs</b>, which is what "
    "makes it practical — in real workloads those costs depend on the "
    "data and are generally unknowable before the work is done.",
    "<b>It adapts to whatever else the machine is doing.</b> If another "
    "process takes a core away, the remaining workers simply steal more, "
    "with no reconfiguration.",
    "<b>And it is what Cilk, Intel TBB, OpenMP tasks, Go's goroutine "
    "scheduler, Rust's rayon, Java's ForkJoinPool, and .NET's task scheduler "
    "all use.</b> The convergence of independent designs on the same "
    "algorithm is not coincidence."]),

  ("break",),
  ("h1", "3 &nbsp; Parallel patterns"),
  ("table", ["Pattern", "Shape", "Parallel structure"],
   [["<b>Map</b>", "Apply a function independently to every element.",
     "<b>Trivially parallel.</b> O(1) depth."],
    ["<b>Reduce</b>",
     "Combine all elements with an associative binary operator.",
     "<b>A tree</b> — O(log n) depth, O(n) work. Requires "
     "associativity; see below."],
    ["<b>Scan (prefix sum)</b>",
     "Produce all prefix reductions — output i is the reduction of "
     "inputs 0..i.",
     "<b>Appears inherently sequential and is not</b> — O(log n) "
     "depth. Module 11, and the most surprising result in the course."],
    ["<b>Stencil</b>",
     "Each output computed from a neighbourhood of inputs.",
     "Parallel over the interior; boundaries require a halo exchange "
     "(Module 10)."],
    ["<b>Gather / scatter</b>", "Indexed read / indexed write.",
     "Gather is parallel; <b>scatter requires conflict handling</b>, since "
     "two sources may write the same destination."],
    ["<b>Partition / filter</b>", "Split elements by a predicate.",
     "<b>A scan over the predicate flags</b> gives each surviving element "
     "its output position."]],
   [0.17, 0.41, 0.42]),
  ("p", "<b>Recognising the pattern gives you the parallel algorithm, its "
        "complexity, and usually a library implementation.</b> Most "
        "parallel code is a composition of these six, and pattern "
        "recognition is the most practically useful skill in this module."),
  ("callout", "Associativity is what makes reduction parallel",
   ["<b>A reduction can be computed as a tree only if the operator is "
    "associative</b> — that is, only if "
    "(a&oplus;b)&oplus;c = a&oplus;(b&oplus;c). The tree evaluates the "
    "combinations in a different order from the sequential loop, and "
    "associativity is exactly the guarantee that the order does not matter.",
    "<b>Integer addition is associative. Floating-point addition is "
    "not.</b> Rounding occurs after each operation, so "
    "(a+b)+c and a+(b+c) can differ in the last bits — and for values "
    "of widely differing magnitude they can differ substantially.",
    "<b>So a parallel floating-point reduction gives a different answer "
    "from the serial one</b>, and a <i>different</i> answer for different "
    "thread counts, and potentially a different answer between runs if the "
    "schedule varies (CSCE 649 Module 13 met the same problem from the "
    "determinism side).",
    "<b>This is not a bug and it must be expected.</b> If bitwise "
    "reproducibility is required — for regression testing, for "
    "debugging, or for a scientific result that must be replicable — "
    "then the reduction order must be fixed explicitly, which costs "
    "performance. <b>Decide which you need</b>, rather than discovering the "
    "variation later and treating it as a defect."]),
 ],
 "resources": [
   ("Blumofe & Leiserson &mdash; Scheduling Multithreaded Computations by "
    "Work Stealing (free)",
    "https://dl.acm.org/doi/10.1145/324133.324234",
    "The &sect;2 result, with the proof. The deque design is in the Cilk "
    "papers from the same group."),
   ("McCool, Robison & Reinders &mdash; Structured Parallel Programming",
    "https://www.elsevier.com/books/structured-parallel-programming/mccool/978-0-12-415993-8",
    "The pattern catalogue of &sect;3, systematically. Library copy; the "
    "pattern list is widely reproduced."),
   ("Intel TBB documentation (free)",
    "https://oneapi-src.github.io/oneTBB/",
    "A production work-stealing runtime, documented, including the "
    "granularity guidance in &sect;1."),
   ("Stanford CS149 &mdash; work distribution and scheduling lectures "
    "(free)",
    "https://gfxcourses.stanford.edu/cs149/",
    "Decomposition, granularity, and load balancing with worked "
    "measurements."),
 ],
 "exercises": [
   "Take a loop with uniform cost and one with highly variable cost. Measure "
   "static and dynamic scheduling on both and explain the four results.",
   "Sweep the chunk size over three orders of magnitude for a dynamic "
   "schedule and plot the time. Identify both failure modes.",
   "<b>Measure load imbalance directly:</b> instrument each thread's busy "
   "time within a phase and plot the distribution.",
   "Construct a workload where one thread takes twice as long and measure "
   "the wasted core-seconds.",
   "Implement a work-stealing deque with LIFO local and FIFO steal "
   "operations.",
   "Measure the steal rate for a balanced and a skewed workload, and confirm "
   "steals are rare in the balanced case.",
   "Implement your own LIFO-steal variant and measure how much worse it is. "
   "Explain the result.",
   "Implement map, reduce, and scan over an array and measure the scaling of "
   "each.",
   "<b>Demonstrate float non-associativity:</b> sum an array of mixed "
   "magnitudes serially and with 2, 4, and 8 threads. Report all the "
   "answers.",
   "Implement a deterministic parallel reduction with a fixed combination "
   "order and measure its cost against the unordered version.",
 ],
 "selfcheck": [
   "Name four decomposition strategies and say what each scales with.",
   "Why does task decomposition not scale?",
   "State the granularity trade-off and the rule of thumb.",
   "Why does a barrier cost the slowest thread's time n times, and why is it "
   "invisible in CPU time?",
   "Compare static and dynamic balancing on five axes.",
   "Explain the LIFO-own / FIFO-steal design and the three properties it "
   "provides.",
   "What did Blumofe and Leiserson prove, and why does it matter "
   "practically?",
   "Name six parallel patterns and the parallel structure of each.",
   "Why is a parallel float reduction not reproducible, and what are your "
   "options?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Performance Analysis",
 "subtitle": "Finding out what is actually slow.",
 "question": "What is limiting this code, and how would you know?",
 "outcomes": [
     "Build and read a roofline model.",
     "Compute arithmetic intensity for a kernel.",
     "Determine whether a kernel is compute- or bandwidth-bound.",
     "Use a profiler to identify the limiting resource.",
     "Measure and report performance honestly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The roofline model",
   "blurb": "One plot that tells you what to optimise."},

  {"t": "eq", "kicker": "Roofline", "title": "The model",
   "eqs": [
     ("I = FLOPs / bytes moved      (arithmetic intensity)",
      "How much arithmetic you do per byte fetched from memory. A property "
      "of the algorithm, not the machine."),
     ("P = min( P_peak , I × BW_peak )",
      "Attainable performance is the lesser of the machine's compute peak "
      "and what its memory bandwidth can feed."),
     ("I_ridge = P_peak / BW_peak",
      "The intensity at which the two are equal. Below it you are "
      "bandwidth-bound; above it, compute-bound."),
   ],
   "caption": "Two machine numbers, one kernel number, and the answer to "
              "'what should I optimise?'",
   "note": "The ridge point is the single most useful number — it tells "
           "you which side of the model your hardware sits on."},

  {"t": "table", "kicker": "Intensity", "title": "Arithmetic intensity of common kernels",
   "header": ["Kernel", "Intensity", "Bound by"],
   "widths": [3.4, 3.4, 5.3],
   "rows": [
     ["Vector add (a+b→c)", "<b>~0.08 FLOP/byte</b>", "<b>Bandwidth, badly</b>"],
     ["<b>SAXPY</b>", "~0.17", "<b>Bandwidth</b>"],
     ["Stencil (7-point)", "~0.5", "Bandwidth"],
     ["<b>Matrix multiply, naive</b>", "~0.25", "<b>Bandwidth</b>"],
     ["<b>Matrix multiply, tiled</b>", "<b>~O(tile size)</b>", "<b>Compute</b>"],
     ["FFT", "~O(log n)", "Depends on size"],
   ],
   "footnote": "<b>Tiling raises matrix multiply's intensity by the tile "
               "dimension</b>, which is the entire reason it is the "
               "canonical optimisation.",
   "note": "The naive-vs-tiled matmul contrast is the clearest "
           "demonstration that intensity is an algorithmic property."},

  {"t": "callout", "title": "Most real code is bandwidth-bound",
   "kind": "The conclusion that redirects effort",
   "body": ["<b>Typical ridge points are 5–20 FLOP per byte</b> on "
            "modern CPUs and GPUs, and rising — compute has grown faster "
            "than bandwidth for decades.",
            "<b>Most kernels have intensities well below 1.</b>",
            "<b>So optimising the arithmetic in a bandwidth-bound loop "
            "achieves nothing</b> — the processor is waiting for memory "
            "either way.",
            "<b>What helps instead:</b> raise the intensity through blocking "
            "and fusion, reduce the bytes moved through better layout and "
            "compression, and improve locality. <b>Not faster "
            "arithmetic.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Profiling",
   "blurb": "Measuring rather than guessing."},

  {"t": "bullets", "kicker": "Method", "title": "How to profile",
   "items": [
     "<b>Start with a timer</b> around phases. Coarse, free, and it "
     "usually identifies the right region immediately.",
     "",
     "<b>Then a sampling profiler</b> — perf, VTune, Instruments. Low "
     "overhead, and it tells you where the time is.",
     "",
     "<b>Then hardware counters</b> for <i>why</i>: cache misses, branch "
     "mispredictions, memory stalls, vector utilisation.",
     "",
     "<b>Measure bandwidth and FLOP rate</b> and place the kernel on the "
     "roofline.",
     "",
     "<b>And only then optimise</b> — against a measurement, not an "
     "intuition.",
   ],
   "note": "The ordering matters: people reach for hardware counters before "
           "they know which function is slow."},

  {"t": "table", "kicker": "Counters", "title": "What the counters tell you",
   "header": ["Symptom", "Likely cause"],
   "widths": [4.6, 7.5],
   "rows": [
     ["<b>High cache miss rate</b>", "<b>Poor locality; wrong data layout</b>"],
     ["High branch mispredictions", "Data-dependent branches; consider branchless"],
     ["<b>Low IPC, high memory stalls</b>", "<b>Bandwidth- or latency-bound</b>"],
     ["Low vector utilisation", "Not vectorising (Module 02)"],
     ["<b>High coherence traffic</b>", "<b>False sharing (Module 02)</b>"],
     ["Uneven per-thread cycles", "<b>Load imbalance (Module 06)</b>"],
   ],
   "footnote": "<b>A profile without counters tells you where; counters "
               "tell you why.</b> You need both.",
   "note": "The where/why split is the useful framing for choosing which "
           "tool to reach for."},

  {"t": "section", "label": "Part 3", "title": "Measuring honestly",
   "blurb": "The discipline, stated."},

  {"t": "callout", "title": "The measurement mistakes that recur",
   "kind": "A checklist",
   "body": ["<b>No warm-up.</b> The first iteration pays for cold caches, "
            "page faults, and lazy allocation.",
            "<b>Dead code elimination.</b> The compiler removes a benchmark "
            "whose result is unused, and you measure nothing.",
            "<b>Timing a single run.</b> Report a distribution; machines "
            "have other work.",
            "<b>Measuring at the wrong granularity</b> — a timer around "
            "a microsecond operation measures the timer.",
            "<b>And frequency scaling</b>, which makes the first seconds "
            "faster than the rest, or slower."]},

  {"t": "bullets", "kicker": "Reporting", "title": "What a performance claim must state",
   "items": [
     "<b>The hardware</b> — model, core count, memory configuration. "
     "'A modern CPU' is not a specification.",
     "",
     "<b>The compiler and flags.</b> A factor of two frequently lives "
     "here.",
     "",
     "<b>The baseline, and its optimisation state</b> (Module 01).",
     "",
     "<b>The distribution</b>, not the minimum — median and spread over "
     "many runs.",
     "",
     "<b>And the problem size</b>, because the answer frequently depends "
     "on whether it fits in cache.",
   ],
   "footnote": "<b>Project 1 and 2 require all five.</b> A result without "
               "them cannot be checked or reproduced."},

  {"t": "callout", "title": "Optimise in the right order",
   "kind": "The ordering that saves time",
   "body": ["<b>1. A better algorithm.</b> An O(n log n) method beats any "
            "amount of tuning of an O(n²) one.",
            "<b>2. Better data layout.</b> SoA, blocking, alignment "
            "— frequently a larger factor than parallelism.",
            "<b>3. Vectorisation.</b> 4–16× on one core (Module 02).",
            "<b>4. Parallelism.</b> Bounded by Amdahl and by the memory "
            "system.",
            "<b>5. Micro-optimisation.</b> Last, and usually unnecessary. "
            "<b>Doing these in the wrong order wastes most of the "
            "effort.</b>"]},
 ],
 "takeaways": [
   "Arithmetic intensity is FLOPs per byte moved — a property of the "
   "algorithm. Attainable performance is the lesser of compute peak and "
   "intensity times bandwidth.",
   "The ridge point separates bandwidth-bound from compute-bound, and modern "
   "ridge points are 5–20 FLOP per byte and rising.",
   "Most real kernels have intensity below 1, so they are bandwidth-bound "
   "and optimising the arithmetic achieves nothing.",
   "Raise intensity by blocking and fusion, and reduce bytes moved by better "
   "layout — that is what helps a bandwidth-bound kernel.",
   "Profile in order: timers for the region, sampling for where, hardware "
   "counters for why, then the roofline placement.",
   "Optimise in order: algorithm, data layout, vectorisation, parallelism, "
   "micro-optimisation. The wrong order wastes most of the effort.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The roofline model"),
  ("eq", "I = FLOPs / bytes &nbsp;&nbsp;&nbsp;&nbsp; "
         "P = min( P<sub>peak</sub>, I &times; BW<sub>peak</sub> ) "
         "&nbsp;&nbsp;&nbsp;&nbsp; I<sub>ridge</sub> = P<sub>peak</sub> / "
         "BW<sub>peak</sub>"),
  ("p", "<b>Arithmetic intensity</b> I is the number of floating-point "
        "operations performed per byte moved between memory and the "
        "processor. <b>It is a property of the algorithm and its data "
        "layout, not of the machine.</b> <b>Peak performance</b> and <b>peak "
        "bandwidth</b> are properties of the machine. The model says "
        "attainable performance is whichever of the two limits binds first."),
  ("table", ["Kernel", "Arithmetic intensity", "Consequence"],
   [["<b>Vector add: c[i] = a[i] + b[i]</b>",
     "<b>1 FLOP per 12 bytes &asymp; 0.08</b>",
     "<b>Severely bandwidth-bound.</b> The processor performs one addition "
     "while waiting for twelve bytes."],
    ["<b>SAXPY: y[i] = a&middot;x[i] + y[i]</b>", "2 FLOP / 12 bytes "
     "&asymp; 0.17", "Bandwidth-bound."],
    ["<b>7-point stencil</b>", "&asymp; 0.5, with good reuse",
     "Bandwidth-bound, and improvable by blocking."],
    ["<b>Matrix multiply, naive</b>", "&asymp; 0.25",
     "<b>Bandwidth-bound</b> — which surprises people, since matrix "
     "multiply is the canonical compute-heavy kernel."],
    ["<b>Matrix multiply, tiled</b>", "<b>O(tile dimension)</b>",
     "<b>Compute-bound.</b> Each tile loaded once serves many operations, "
     "so intensity rises with the tile size. <b>This is the entire reason "
     "tiling is the canonical optimisation</b>, and it is the clearest "
     "demonstration that intensity is algorithmic rather than fixed."],
    ["<b>FFT</b>", "O(log n)", "Depends on the transform size and the "
     "cache."]],
   [0.26, 0.26, 0.48]),
  ("callout", "Most real code is bandwidth-bound",
   ["<b>Typical ridge points on modern hardware are 5 to 20 FLOP per "
    "byte</b>, and they have been rising for decades — compute capacity "
    "has grown considerably faster than memory bandwidth, so the ridge moves "
    "right and more kernels fall on the bandwidth side.",
    "<b>Most real kernels have arithmetic intensities well below 1</b>, as "
    "the table above shows. They are nowhere near the ridge.",
    "<b>So optimising the arithmetic in a bandwidth-bound loop achieves "
    "nothing at all.</b> Making the floating-point operations faster, or "
    "fewer, does not help when the processor is idle waiting for data "
    "— and a great deal of optimisation effort is spent here.",
    "<b>What does help:</b> <b>raise the arithmetic intensity</b> through "
    "blocking and loop fusion, so that each byte fetched is used more times; "
    "<b>reduce the bytes moved</b> through better data layout, smaller data "
    "types, and compression; and <b>improve locality</b> so that fetches hit "
    "in cache. <b>Not faster arithmetic.</b> The roofline exists to tell you "
    "this before you spend a week on the wrong thing."]),

  ("h1", "2 &nbsp; Profiling"),
  ("ol", ["<b>Start with timers around phases.</b> Coarse, free, requires "
          "no tooling, and it usually identifies the right region "
          "immediately. A great deal of profiling effort is spent "
          "discovering something a <code>printf</code> of elapsed time would "
          "have revealed.",
          "<b>Then a sampling profiler</b> — perf, VTune, Instruments, "
          "or your platform's equivalent. Low overhead, no instrumentation, "
          "and it tells you <b>where</b> the time goes.",
          "<b>Then hardware performance counters</b> for <b>why</b>: cache "
          "misses at each level, branch mispredictions, memory stall cycles, "
          "vector instruction counts, coherence traffic.",
          "<b>Measure the achieved bandwidth and FLOP rate</b>, and place "
          "the kernel on the roofline. This tells you which ceiling you are "
          "near and therefore which optimisations can possibly help.",
          "<b>And only then optimise</b> — against a measurement "
          "rather than an intuition about what ought to be slow. <b>The "
          "ordering matters</b>, and people routinely reach for hardware "
          "counters before they know which function is responsible."]),
  ("table", ["Counter symptom", "Likely cause", "What to do"],
   [["<b>High cache miss rate</b>",
     "Poor locality, or a data layout that fetches unused bytes.",
     "Blocking, structure-of-arrays, smaller data types (Module 02)."],
    ["<b>High branch misprediction rate</b>",
     "Data-dependent branches that the predictor cannot learn.",
     "Branchless formulations, sorting the data, or predication."],
    ["<b>Low instructions-per-cycle with high memory stalls</b>",
     "<b>Bandwidth- or latency-bound.</b>",
     "Place it on the roofline; raise intensity or reduce bytes."],
    ["<b>Low vector instruction fraction</b>",
     "The loop is not vectorising.",
     "Read the vectorisation report (Module 02)."],
    ["<b>High coherence or snoop traffic</b>",
     "<b>False sharing</b>, or genuine heavy sharing.",
     "Pad to cache lines; use per-thread accumulators (Module 02)."],
    ["<b>Uneven cycle counts across threads</b>",
     "<b>Load imbalance.</b>",
     "Finer granularity or dynamic scheduling (Module 06)."]],
   [0.28, 0.32, 0.40]),

  ("break",),
  ("h1", "3 &nbsp; Measuring and reporting honestly"),
  ("callout", "The measurement mistakes that recur",
   ["<b>No warm-up.</b> The first iteration pays for cold caches, page "
    "faults on first touch, lazy allocation, and in a JIT-compiled language "
    "the compilation itself. Discard it, or run long enough that it does not "
    "matter.",
    "<b>Dead code elimination.</b> If a benchmark computes a result nothing "
    "uses, the compiler may remove the computation entirely and you measure "
    "an empty loop — which frequently appears as an implausibly "
    "excellent result. Consume the result, or use a compiler-specific "
    "<code>DoNotOptimize</code>.",
    "<b>Timing a single run.</b> The machine has other work, the scheduler "
    "moves threads, and frequency varies. <b>Report a distribution</b> "
    "— median and spread over many runs — rather than one number "
    "or a minimum.",
    "<b>Measuring at the wrong granularity.</b> A timer call around an "
    "operation taking a microsecond measures mostly the timer. Loop the "
    "operation and divide.",
    "<b>Frequency scaling.</b> Turbo makes the first seconds faster than "
    "the rest; thermal throttling makes the later minutes slower. <b>A "
    "benchmark of a few seconds and one of a few minutes measure different "
    "machines</b>, and which you want depends on the real workload."]),
  ("ul", ["<b>The hardware:</b> processor model, core count, memory "
          "configuration and speed, and for GPU work the exact device. "
          "<b>'A modern CPU' is not a specification</b> and makes a result "
          "uncheckable.",
          "<b>The compiler and its flags.</b> <b>A factor of two frequently "
          "lives here</b>, and a comparison between two implementations "
          "built with different flags is not a comparison of the "
          "implementations.",
          "<b>The baseline and its optimisation state</b> (Module 01 "
          "&sect;3). This is the one most often omitted and most often "
          "decisive.",
          "<b>The distribution rather than the minimum</b> — median, "
          "and some measure of spread, over enough runs to be meaningful.",
          "<b>The problem size</b>, because performance frequently depends "
          "on whether the working set fits in cache, and a result at one "
          "size may reverse at another. <b>Projects 1 and 2 require all "
          "five</b>, and a result lacking them cannot be checked or "
          "reproduced."]),
  ("callout", "Optimise in the right order",
   ["<b>1. A better algorithm.</b> An O(n log n) method beats any amount of "
    "tuning applied to an O(n&#178;) one, at sufficient scale, and the "
    "crossover is usually smaller than people expect. CSCE 629's content is "
    "the highest-leverage optimisation available.",
    "<b>2. Better data layout.</b> Structure-of-arrays, blocking for cache, "
    "alignment, smaller types. <b>Frequently a larger factor than "
    "parallelism</b>, and it compounds with everything after it — a "
    "bandwidth-bound kernel parallelises badly, and fixing the layout fixes "
    "the parallel version too.",
    "<b>3. Vectorisation.</b> Four to sixteen times on a single core, "
    "frequently for the cost of a compiler flag and a "
    "<code>__restrict__</code> (Module 02).",
    "<b>4. Parallelism.</b> Bounded above by Amdahl's law and, for most "
    "real kernels, by the memory system rather than the core count.",
    "<b>5. Micro-optimisation.</b> Last, and usually unnecessary once the "
    "first four are done. <b>Performing these in the wrong order wastes most "
    "of the effort</b> — hand-tuning the inner loop of an algorithm you "
    "are about to replace is the characteristic failure."]),
 ],
 "resources": [
   ("Williams, Waterman & Patterson &mdash; Roofline: An Insightful Visual "
    "Performance Model (free)",
    "https://dl.acm.org/doi/10.1145/1498765.1498785",
    "<b>The roofline paper.</b> Short, and the model has held up "
    "remarkably well. Read it before building your first roofline."),
   ("Brendan Gregg &mdash; systems performance resources (free)",
    "https://www.brendangregg.com/",
    "Profiling methodology, flame graphs, and the USE method. The practical "
    "side of &sect;2, and exhaustively documented."),
   ("Hoefler & Belli &mdash; Scientific Benchmarking of Parallel Computing "
    "Systems (free)",
    "https://htor.inf.ethz.ch/publications/index.php?pub=222",
    "<b>The reporting discipline of &sect;3, made rigorous.</b> Read it "
    "before producing any performance claim."),
   ("Intel &mdash; VTune and Advisor documentation (free)",
    "https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html",
    "Advisor generates roofline plots automatically, which is a "
    "considerable convenience."),
 ],
 "exercises": [
   "Measure your machine's peak FLOP rate and peak memory bandwidth, and "
   "compute the ridge point.",
   "Compute the arithmetic intensity of five kernels by hand and verify each "
   "against measured bytes and FLOPs.",
   "<b>Build a roofline plot for your machine</b> and place those five "
   "kernels on it.",
   "Implement naive and tiled matrix multiply. Measure the intensity and the "
   "performance of each and place both on the roofline.",
   "Sweep the tile size and plot performance against it. Explain the shape.",
   "Take a bandwidth-bound kernel and optimise its arithmetic. Confirm "
   "nothing happens.",
   "Then reduce its bytes moved — by changing layout or data type "
   "— and measure again.",
   "Profile a program with timers, then a sampling profiler, then hardware "
   "counters. Note what each step added.",
   "<b>Construct a benchmark that the compiler optimises away</b> and "
   "demonstrate the implausible result. Then fix it.",
   "Run a benchmark for 1 second and for 5 minutes on the same machine and "
   "compare, identifying frequency scaling effects.",
 ],
 "selfcheck": [
   "Define arithmetic intensity and say what it is a property of.",
   "State the roofline model and explain the ridge point.",
   "Why is naive matrix multiply bandwidth-bound and tiled matrix multiply "
   "not?",
   "Why is most real code bandwidth-bound, and what follows for "
   "optimisation?",
   "Give the four profiling steps in order and say what each provides.",
   "Give six counter symptoms and their likely causes.",
   "Name five recurring measurement mistakes.",
   "What five things must a performance claim state?",
   "Give the five optimisation steps in order and say what goes wrong if "
   "they are reordered.",
 ],
},

]
