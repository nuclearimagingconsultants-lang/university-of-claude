# -*- coding: utf-8 -*-
"""CSCE 614 Computer Architecture — original course content."""

COURSE = {
    "code": "CSCE 614",
    "title": "Computer Architecture",
    "tagline": "Why your code runs at the speed it does, from the pipeline to "
               "the memory hierarchy to the GPU",
    "term": "Semester 1 (with CSCE 629 and CSCE 641)",
    "prereqs": "Programming in C or C++; basic digital logic helpful but not "
               "assumed",
    "effort": "10–12 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A performance portfolio: a set of microbenchmarks that "
                   "measure your own machine's cache hierarchy, branch "
                   "predictor, and SIMD width, with every measured number "
                   "explained",
    "description": [
        "CSCE 629 analyses algorithms in a model where every memory access "
        "costs one unit and every instruction takes one step. That model is "
        "indispensable and it is also wrong by one to two orders of "
        "magnitude. This course is about the machine the model abstracts "
        "away.",
        "The organising fact is that processors have become very fast and "
        "memory has not. A modern core can execute several instructions per "
        "cycle; a main-memory access costs two to three hundred cycles. "
        "Essentially every architectural feature of the last forty years "
        "— caches, prefetchers, out-of-order execution, speculation, "
        "wide SIMD, many-threaded GPUs — exists to hide that gap or to "
        "find work to do while waiting.",
        "The course is built around measurement. Every mechanism is "
        "introduced, then measured on your own hardware with a benchmark you "
        "write. You will determine your machine's cache sizes without looking "
        "them up, observe the cost of a branch misprediction directly, and "
        "watch a loop get eight times faster when it vectorises. A number you "
        "measured and explained is worth more than a chapter you read.",
        "The aim is a working cost model: the ability to look at a loop and "
        "predict, roughly, what will make it slow. That skill transfers "
        "directly to CSCE 641, where frame time is decided by memory access "
        "patterns, and to CSCE 735, where it decides whether a parallel "
        "algorithm scales.",
    ],
    "outcomes": [
        "Measure performance correctly and explain why common methodologies "
        "mislead.",
        "Explain pipelining, the three hazard classes, and how each is "
        "resolved.",
        "Explain branch prediction and quantify the cost of a misprediction.",
        "Derive your machine's cache hierarchy from measurement alone.",
        "Restructure code for locality and predict the improvement before "
        "measuring it.",
        "Explain out-of-order execution and what limits instruction-level "
        "parallelism.",
        "Explain why GPUs are throughput machines and what follows for "
        "graphics and compute.",
        "Explain cache coherence, memory consistency, and why lock-free code "
        "is difficult.",
    ],
    "materials": [
        ("ETH Zürich — Onur Mutlu, Computer Architecture (full "
         "lecture videos, free)",
         "https://safari.ethz.ch/architecture/",
         "Primary lecture series. Graduate level, exceptionally thorough, "
         "and freely available in full with slides and assignments."),
        ("MIT 6.004 Computation Structures (OCW, Spring 2017)",
         "https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/",
         "The foundation course: from transistors to a working pipelined "
         "processor. Start here if digital logic is unfamiliar."),
        ("MITx 6.004.1x Computation Structures: Digital Circuits (edX)",
         "https://www.edx.org/learn/computer-programming/massachusetts-institute-of-technology-computation-structures-1-digital-circuits",
         "The same material in graded MOOC form, free to audit."),
        ("Nand2Tetris — build a computer from NAND gates (free)",
         "https://www.nand2tetris.org/",
         "If you have never built a processor, do the first six projects. "
         "The understanding it produces is disproportionate to the effort."),
        ("Ulrich Drepper — What Every Programmer Should Know About "
         "Memory (free)",
         "https://people.freebsd.org/~lstewart/articles/cpumemory.pdf",
         "The definitive practical treatment of the memory hierarchy. Long, "
         "dense, and worth every page. Core reading for Modules 05–07."),
        ("Agner Fog — Software optimization manuals (free)",
         "https://www.agner.org/optimize/",
         "Microarchitecture tables, instruction latencies, and optimisation "
         "guidance for every recent x86 core. The reference you will keep."),
    ],
    "tooling": [
        "<b>C or C++ with a good compiler.</b> You need to see generated "
        "assembly and control optimisation flags.",
        "<b>Compiler Explorer (godbolt.org)</b> — the fastest way to see "
        "what your source becomes. Used constantly from Module 02.",
        "<b>perf</b> (Linux) or <b>Intel VTune</b> / <b>AMD uProf</b> "
        "(Windows) for hardware performance counters: cache misses, branch "
        "mispredictions, IPC.",
        "<b>A timing harness</b> with proper warm-up, repeated trials, and "
        "median reporting — reuse the one from CSCE 629 Module 01.",
        "<b>A portfolio repository</b> with one directory per module, each "
        "containing the benchmark, the measured data, and a written "
        "explanation.",
    ],
    "projects": [
        {"title": "Measure your own machine", "after": 7,
         "brief": "Determine your machine's microarchitectural parameters by "
                  "measurement alone, without consulting a datasheet. Then "
                  "look them up and account for every discrepancy.",
         "reqs": [
             "Cache sizes at every level, derived from a pointer-chase "
             "latency curve against working-set size.",
             "Cache line size, derived from a strided access experiment.",
             "Cache associativity, derived from a conflict-miss experiment.",
             "TLB reach, derived from a page-stride experiment.",
             "Branch misprediction penalty, in cycles, derived from a "
             "random-versus-predictable branch benchmark.",
             "Memory bandwidth, sequential and random.",
         ],
         "done": [
             "A plot of access latency against working-set size with the "
             "cache levels visibly marked and labelled.",
             "A table comparing every measured value against the "
             "manufacturer's specification.",
             "A written explanation of each discrepancy. 'The prefetcher "
             "hid it' is a valid explanation; 'measurement noise' usually is "
             "not.",
         ]},
        {"title": "Make one loop ten times faster", "after": 12,
         "brief": "Take a memory-bound kernel and optimise it by a factor of "
                  "at least five, using only transformations justified by "
                  "this course. Every step must be predicted before it is "
                  "measured.",
         "reqs": [
             "Choose a kernel: dense matrix multiply, a stencil, an "
             "N-body step, or a histogram.",
             "A baseline implementation, honestly written.",
             "At least four optimisation steps, each with a <i>prediction</i> "
             "of the speedup written before measuring, and the measured "
             "result after.",
             "Techniques should include at minimum: loop interchange or "
             "blocking for locality, a data layout change (AoS to SoA), "
             "vectorisation, and one further transformation of your choice.",
             "Hardware counter data (cache misses, IPC) at each step.",
         ],
         "done": [
             "At least 5&times; end-to-end speedup, with the final version "
             "still producing identical output.",
             "A table of predicted versus measured speedup for each step.",
             "An honest account of at least one prediction that was wrong, "
             "and why.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Performance: What to Measure",
 "subtitle": "Why intuition about speed is usually wrong.",
 "question": "What does 'faster' actually mean, and how do you measure it "
             "honestly?",
 "outcomes": [
     "Decompose execution time into instruction count, CPI, and clock "
     "period.",
     "Explain why MIPS and clock speed are misleading metrics.",
     "Apply Amdahl's law and state what it implies for optimisation effort.",
     "Design a benchmark that measures what you intend it to.",
     "Read basic hardware performance counters.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The performance equation",
   "blurb": "Three factors, and every optimisation touches one of them."},

  {"t": "eq", "kicker": "The equation", "title": "Execution time, decomposed",
   "eqs": [
     ("time  =  instructions × CPI × clock period",
      "Every performance change is a change to one of these three."),
     ("instructions — the compiler and the algorithm",
      "Better algorithm, better codegen, fewer operations."),
     ("CPI — the microarchitecture meeting your code",
      "Cache misses, branch misses, dependencies. <b>This course.</b>"),
   ],
   "caption": "Clock period is largely out of your hands. Instruction count "
              "is CSCE 629's territory. CPI is where architecture lives.",
   "note": "Framing CPI as 'the microarchitecture meeting your code' sets up "
           "the whole course: CPI is not a property of the chip alone."},

  {"t": "callout", "title": "Why clock speed and MIPS mislead",
   "kind": "Bad metrics",
   "body": ["<b>Clock speed</b> ignores how much work happens per cycle. A "
            "3 GHz core with CPI 4 is slower than a 2 GHz core with CPI 1.",
            "<b>MIPS</b> rewards executing more instructions, which is "
            "backwards. A compiler that emits twice the instructions at the "
            "same speed scores better.",
            "<b>FLOPS</b> measures only floating-point work, and most real "
            "programs are limited by memory, not arithmetic.",
            "The only honest metric is <b>time to complete your actual "
            "workload</b>. Everything else is a proxy that someone is "
            "incentivised to game."]},

  {"t": "section", "label": "Part 2", "title": "Amdahl's law",
   "blurb": "The arithmetic that decides where to spend effort."},

  {"t": "eq", "kicker": "Amdahl", "title": "Speedup is bounded by what you did not improve",
   "eqs": [
     ("speedup  =  1 / ( (1−f) + f/s )",
      "f = fraction of time affected, s = how much faster that part becomes."),
     ("f = 0.9, s = ∞  ⇒  speedup = 10",
      "Making 90% of the work <i>free</i> gives only 10×."),
     ("f = 0.5, s = 10  ⇒  speedup = 1.8",
      "A tenfold improvement to half the program is worth less than 2×."),
   ],
   "caption": "The unimproved fraction dominates very quickly. This is why "
              "profiling before optimising is not advice but arithmetic.",
   "note": "Students nod at Amdahl and then optimise the wrong thing anyway. "
           "The f=0.9, s=infinity line usually lands."},

  {"t": "bullets", "kicker": "Consequence", "title": "What Amdahl's law actually tells you",
   "items": [
     "<b>Profile first.</b> Optimising 5% of the runtime caps your gain at "
     "5%, no matter how brilliant the optimisation.",
     "",
     "<b>Diminishing returns are structural,</b> not a failure of effort. "
     "Each optimisation shrinks f for the next one.",
     "",
     "<b>It bounds parallelism too</b> — the serial fraction caps "
     "speedup regardless of core count.",
     ("5% serial → at most 20×, with infinite cores.", 1),
     ("CSCE 735 takes this seriously.", 1),
     "",
     "Gustafson's counterpoint: with more machine, people solve bigger "
     "problems, so f is not fixed in practice.",
   ]},

  {"t": "section", "label": "Part 3", "title": "Measuring honestly",
   "blurb": "Most published benchmarks are wrong in at least one of these "
            "ways."},

  {"t": "table", "kicker": "Pitfalls", "title": "Ways to measure the wrong thing",
   "header": ["Mistake", "What you actually measured"],
   "widths": [4.4, 7.7],
   "rows": [
     ["No warm-up", "Cold caches, page faults, and JIT compilation"],
     ["Result unused", "Nothing — the optimiser deleted your loop"],
     ["Reporting the mean", "One scheduler preemption or thermal event"],
     ["Single input size", "A point, not a curve — no asymptotic information"],
     ["Timing inside the loop", "Mostly the cost of reading the clock"],
     ["Benchmarking in a VM", "The hypervisor's scheduling decisions"],
     ["Ignoring frequency scaling", "The CPU's thermal state, not your code"],
   ],
   "note": "Frequency scaling is worth dwelling on — a laptop under "
           "sustained load can drop 40% and make the last benchmark look "
           "better than the first."},

  {"t": "callout", "title": "Thermal throttling will lie to you",
   "kind": "Measure carefully",
   "body": ["Sustained load heats a chip, and modern processors respond by "
            "lowering the clock — on a laptop, often by 30–50%.",
            "Run benchmark A then benchmark B back to back, and B runs on a "
            "hotter, slower machine. The result is a systematic bias that "
            "looks exactly like a real difference.",
            "<b>Mitigations:</b> interleave the variants rather than running "
            "them in blocks; discard the first runs; monitor actual clock "
            "frequency during the benchmark; and treat any difference under "
            "about 10% on a laptop as unproven."]},

  {"t": "code", "kicker": "Practice", "title": "A harness that measures what you meant",
   "lang": "c", "code": """
double bench(void (*f)(void*), void* data, int trials) {
    f(data);                       // warm up: caches, branch predictor,
    f(data);                       //   page tables, frequency ramp

    double best = 1e30;
    for (int i = 0; i < trials; i++) {
        uint64_t t0 = rdtsc_serialized();
        f(data);
        uint64_t t1 = rdtsc_serialized();
        double t = (t1 - t0);
        if (t < best) best = t;    // MINIMUM, not mean: noise only adds
    }
    return best;
}

// And consume the result, or the optimiser removes the work entirely:
// asm volatile("" : : "r"(result) : "memory");
""",
   "caption": "Minimum rather than mean: interference only ever makes a run "
              "slower, so the fastest observed run is the closest estimate of "
              "the true cost.",
   "note": "The min-vs-median choice differs from CSCE 629's harness because "
           "here we want the machine's capability, not the typical experience."},

  {"t": "bullets", "kicker": "Counters", "title": "Hardware performance counters",
   "items": [
     "The processor counts microarchitectural events directly. Use them.",
     "",
     "<b>cycles, instructions</b> → IPC. Below ~1 means something is "
     "stalling.",
     "<b>cache-misses, LLC-load-misses</b> → memory-bound?",
     "<b>branch-misses</b> → control-flow problem?",
     "<b>stalled-cycles-frontend/backend</b> → which end is the problem?",
     "",
     "<code>perf stat ./program</code> on Linux; VTune or uProf on Windows.",
     "",
     "Counters turn 'it feels slow' into a diagnosis.",
   ],
   "footnote": "IPC alone answers the first question: is this compute-bound "
               "or stalled?"},

  {"t": "table", "kicker": "Orientation", "title": "The numbers to internalise",
   "header": ["Operation", "Cycles", "Relative"],
   "widths": [5.0, 3.2, 3.9],
   "rows": [
     ["Register access, simple ALU", "~1", "1×"],
     ["L1 cache hit", "~4", "4×"],
     ["L2 cache hit", "~12", "12×"],
     ["L3 cache hit", "~40", "40×"],
     ["Main memory", "~200–300", "~250×"],
     ["Branch misprediction", "~15–20", "~17×"],
     ["SSD read", "~10⁵", "100,000×"],
   ],
   "footnote": "The RAM model charges 1 for every row in this table.",
   "note": "This table is the course in miniature. Students should know these "
           "to within a factor of two by the end of week one."},
 ],
 "takeaways": [
   "time = instructions × CPI × clock period. CPI is where "
   "architecture meets your code, and it is this course's subject.",
   "Clock speed, MIPS, and FLOPS are all gameable proxies. Time on your real "
   "workload is the only honest metric.",
   "Amdahl's law: the fraction you do not improve dominates fast. Making 90% "
   "of a program free gives only 10×.",
   "Warm up, consume the result, take the minimum, vary the input size, and "
   "interleave variants to defeat thermal drift.",
   "Hardware counters turn 'it feels slow' into a diagnosis. Start with IPC.",
   "L1 is ~4 cycles and main memory is ~250. The RAM model charges 1 for "
   "both, and that gap is why this course exists.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The performance equation"),
  ("p", "Execution time factors into exactly three terms, and every "
        "performance change in existence modifies one of them."),
  ("eq", "time = instruction count &times; cycles per instruction &times; clock period"),
  ("table", ["Factor", "Determined by", "Who controls it"],
   [["Instruction count", "The algorithm and the compiler",
     "You, through algorithm choice (CSCE 629) and source structure."],
    ["CPI", "How the microarchitecture responds to <i>your</i> code: cache "
     "behaviour, branch predictability, dependency chains, available "
     "parallelism",
     "You, indirectly — and this is what the rest of this course is "
     "about."],
    ["Clock period", "Process technology, power and thermal limits",
     "Essentially nobody, any more. Clock frequency has been roughly flat "
     "since 2005 (Module 13)."]],
   [0.17, 0.48, 0.35]),
  ("callout", "CPI is not a property of the processor",
   ["It is a property of a <i>program running on</i> a processor. The same "
    "chip will deliver a CPI of 0.3 on one loop and 20 on another.",
    "That is the central idea of the course: the hardware provides "
    "mechanisms, and whether your code benefits from them or fights them "
    "decides performance far more than the clock on the box."]),
  ("h2", "1.1 &nbsp; Metrics that mislead"),
  ("table", ["Metric", "Why it misleads"],
   [["<b>Clock frequency</b>",
     "Says nothing about work per cycle. A 3 GHz core at CPI 4 is slower than "
     "a 2 GHz core at CPI 1. Marketing used this for two decades."],
    ["<b>MIPS</b>",
     "Rewards executing <i>more</i> instructions. A compiler that emits twice "
     "as many instructions in the same time scores twice as well, which is "
     "exactly backwards."],
    ["<b>FLOPS</b>",
     "Measures floating-point throughput only. Most real programs are limited "
     "by memory bandwidth or latency, so peak FLOPS is a number almost no "
     "application approaches."],
    ["<b>Synthetic benchmarks</b>",
     "Measure the benchmark. When a benchmark becomes commercially important, "
     "vendors optimise for it specifically, and it stops predicting anything "
     "else."]],
   [0.22, 0.78]),
  ("p", "The only trustworthy metric is wall-clock time on the workload you "
        "actually care about. Everything else is a proxy, and proxies get "
        "gamed."),

  ("h1", "2 &nbsp; Amdahl's law"),
  ("eq", "speedup = 1 / ( (1 &minus; f) + f/s )"),
  ("p", "where f is the fraction of original execution time affected by your "
        "optimisation and s is how much faster that fraction becomes."),
  ("table", ["f", "s", "Speedup", "Reading"],
   [["0.9", "&infin;", "10&times;",
     "Making 90% of the program take <i>zero time</i> yields only 10&times;."],
    ["0.5", "10", "1.82&times;",
     "A tenfold improvement to half the program is worth less than 2&times;."],
    ["0.05", "100", "1.05&times;",
     "A hundredfold improvement to 5% of the program is almost invisible."],
    ["0.99", "100", "50&times;",
     "To get large speedups you must improve nearly everything."]],
   [0.08, 0.08, 0.14, 0.70]),
  ("callout", "Why 'profile before optimising' is arithmetic, not advice",
   ["If a routine accounts for 5% of runtime, your maximum possible gain from "
    "optimising it is 5%. No amount of cleverness changes that ceiling.",
    "Programmers' intuitions about where time goes are famously unreliable "
    "— the hot spot is routinely somewhere nobody suspected. Measuring "
    "first is not diligence; it is the only way to know the ceiling exists "
    "before you spend a week under it."]),
  ("p", "Amdahl's law also bounds parallel speedup, with f as the "
        "parallelisable fraction. A 5% serial section limits you to 20&times; "
        "no matter how many cores you add, which is a central constraint in "
        "CSCE 735. <b>Gustafson's</b> counterargument is that in practice "
        "people given a bigger machine solve a bigger problem, so f grows "
        "with the machine rather than staying fixed — both observations "
        "are correct, and they apply to different situations."),

  ("break",),
  ("h1", "3 &nbsp; Measuring honestly"),
  ("p", "Most performance measurements are wrong, usually in one of a small "
        "number of recognisable ways."),
  ("table", ["Mistake", "What you measured instead", "Fix"],
   [["<b>No warm-up</b>",
     "Cold caches, page faults, lazy symbol binding, JIT compilation.",
     "Run the workload several times before timing."],
    ["<b>Result never used</b>",
     "Nothing. A compiler that can prove the result is unused will delete the "
     "computation entirely, and you will measure an empty loop.",
     "Consume the result: accumulate it, print a checksum, or use a compiler "
     "barrier."],
    ["<b>Reporting the mean</b>",
     "The worst interference you happened to encounter.",
     "Report the minimum (for machine capability) or the median (for typical "
     "experience). Never the mean."],
    ["<b>One input size</b>",
     "A single point, with no information about scaling or about which cache "
     "level you were in.",
     "Sweep sizes across several orders of magnitude."],
    ["<b>Timer inside the inner loop</b>",
     "Mostly the cost of reading the clock, which is substantial.",
     "Time a batch of iterations and divide."],
    ["<b>Thermal throttling</b>",
     "The chip's temperature, not your code.",
     "Interleave variants; monitor frequency; distrust small differences."]],
   [0.17, 0.46, 0.37]),
  ("callout", "Thermal throttling is the one that fools experienced people",
   ["Under sustained load a modern processor — especially in a laptop "
    "— reduces its clock frequency to stay within power and thermal "
    "limits. Reductions of 30&ndash;50% are routine.",
    "Run variant A for thirty seconds, then variant B, and B executes on a "
    "hotter and therefore slower machine. The resulting bias is systematic, "
    "reproducible, and looks exactly like a genuine difference.",
    "Interleave the variants (ABABAB rather than AAABBB), discard early runs, "
    "log the actual frequency, and treat differences below about 10% on a "
    "laptop as unproven."]),
  ("h2", "3.1 &nbsp; A defensible harness"),
  ("code", """double bench(void (*f)(void*), void* data, int trials) {
    f(data); f(data);              // warm caches, predictors, page tables

    double best = 1e30;
    for (int i = 0; i < trials; i++) {
        uint64_t t0 = rdtsc_serialized();
        f(data);
        uint64_t t1 = rdtsc_serialized();
        if ((double)(t1 - t0) < best) best = t1 - t0;
    }
    return best;                   // minimum: interference only adds time
}

// Prevent the optimiser from removing the work:
asm volatile("" : : "r"(result) : "memory");"""),
  ("p", "Taking the minimum is the right choice when you want to know what "
        "the machine is capable of: every source of interference — "
        "interrupts, other processes, migrations — only ever adds time, "
        "so the fastest observed run is the closest estimate of the "
        "underlying cost. When you instead want to characterise typical "
        "behaviour under real conditions, report a median and a tail "
        "percentile."),

  ("h1", "4 &nbsp; Hardware performance counters"),
  ("p", "Processors contain counters for microarchitectural events, and "
        "reading them converts guesswork into diagnosis."),
  ("table", ["Counter", "Tells you"],
   [["<code>cycles</code>, <code>instructions</code>",
     "IPC = instructions / cycles. Below about 1 means the core is stalling; "
     "modern cores can sustain 3&ndash;4 on good code."],
    ["<code>cache-misses</code>, <code>LLC-load-misses</code>",
     "Whether you are memory-bound. A high miss rate with low IPC is the "
     "classic memory-bound signature."],
    ["<code>branch-misses</code>",
     "Control-flow trouble. Compare against <code>branches</code> for a rate; "
     "above ~2% is worth investigating (Module 04)."],
    ["<code>stalled-cycles-frontend</code> / <code>-backend</code>",
     "Which end is the bottleneck: instruction supply, or execution and "
     "memory."],
    ["<code>page-faults</code>, <code>dTLB-load-misses</code>",
     "Virtual memory trouble (Module 07)."]],
   [0.33, 0.67]),
  ("p", "On Linux, <code>perf stat ./program</code> gives most of these in "
        "one line. On Windows, Intel VTune and AMD uProf provide equivalents. "
        "Learn to read IPC first: it answers the only question that matters "
        "at the start, which is whether the core is computing or waiting."),

  ("h1", "5 &nbsp; The numbers worth memorising"),
  ("table", ["Operation", "Approximate cycles", "Relative to an ALU op"],
   [["Register-to-register ALU operation", "1", "1&times;"],
    ["L1 data cache hit", "4", "4&times;"],
    ["L2 cache hit", "12", "12&times;"],
    ["L3 cache hit", "40", "40&times;"],
    ["Main memory (DRAM)", "200&ndash;300", "~250&times;"],
    ["Branch misprediction", "15&ndash;20", "~17&times;"],
    ["Integer division", "20&ndash;40", "~30&times;"],
    ["SSD read", "~100,000", "100,000&times;"],
    ["Network round trip (same datacentre)", "~500,000", "500,000&times;"]],
   [0.40, 0.26, 0.34]),
  ("callout", "The one comparison that organises the whole course",
   ["An L1 hit is 4 cycles. A main-memory access is around 250. That is a "
    "ratio of more than sixty.",
    "The RAM model of CSCE 629 charges <b>1</b> for both.",
    "Almost every architectural mechanism in the remaining twelve modules "
    "exists either to avoid paying the 250, or to find useful work to do "
    "while paying it. Caches, prefetchers, out-of-order execution, "
    "speculation, hyperthreading, and the entire design of GPUs are all "
    "responses to this one number."]),
 ],
 "resources": [
   ("Onur Mutlu — Computer Architecture, Lecture 1–2 (Introduction, "
    "Performance)",
    "https://safari.ethz.ch/architecture/",
    "The framing of the course and the performance equation, done "
    "thoroughly."),
   ("MIT 6.004 — Performance Measures",
    "https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/",
    "The equation and Amdahl's law at an accessible level."),
   ("Latency Numbers Every Programmer Should Know",
    "https://gist.github.com/jboner/2841832",
    "The table from &sect;5 with more entries. Memorise the orders of "
    "magnitude."),
   ("Brendan Gregg — perf Examples",
    "https://www.brendangregg.com/perf.html",
    "The practical reference for Linux performance counters. Bookmark it."),
   ("Agner Fog — Optimizing software in C++",
    "https://www.agner.org/optimize/",
    "Chapter 2 covers benchmarking methodology properly."),
 ],
 "exercises": [
   "Build the benchmarking harness from &sect;3.1. Verify it by timing an "
   "empty function and a function with a known cost, and confirm the overhead "
   "is small relative to what you intend to measure.",
   "Write a loop whose result is unused and confirm your compiler deletes it "
   "entirely at <code>-O2</code>. Inspect the assembly on Compiler Explorer "
   "to prove it. Then add a consume barrier and confirm the work returns.",
   "Measure the same kernel in blocks (AAABBB) and interleaved (ABABAB) under "
   "sustained load. Log CPU frequency throughout. Quantify the thermal bias.",
   "Compute the Amdahl speedup for your own code: profile a program you have "
   "written, identify the top function by time, and calculate the maximum "
   "possible gain from optimising it perfectly.",
   "Run <code>perf stat</code> (or VTune) on three programs: a tight "
   "arithmetic loop, a random-access memory loop, and a branchy loop. Record "
   "IPC, cache miss rate, and branch miss rate for each, and explain the "
   "pattern.",
   "Reproduce the latency table of &sect;5 for your own machine as far as you "
   "can with simple timing. You will complete this properly in Module 05.",
 ],
 "selfcheck": [
   "State the performance equation and say what determines each factor.",
   "Why is CPI a property of a program-processor pair rather than of the "
   "processor alone?",
   "Give two reasons MIPS is a bad metric.",
   "If an optimisation makes 80% of a program twice as fast, what is the "
   "overall speedup? What if that 80% became instantaneous?",
   "Name four ways a benchmark can measure something other than what was "
   "intended.",
   "Why take the minimum of several trials rather than the mean?",
   "How many times slower is a main-memory access than an L1 hit, and what "
   "does the RAM model charge for each?",
 ],
},

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Instruction Sets and the Hardware/Software Interface",
 "subtitle": "The contract between the compiler and the chip.",
 "question": "What does the hardware actually promise, and what is free to "
             "change underneath?",
 "outcomes": [
     "Explain what an ISA specifies and what it deliberately leaves open.",
     "Compare RISC and CISC design philosophies and their modern "
     "convergence.",
     "Read compiler-generated assembly well enough to diagnose performance.",
     "Explain addressing modes and the cost of each.",
     "Explain why the ISA is an abstraction boundary, and why that matters.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What an ISA is",
   "blurb": "A contract, deliberately silent about implementation."},

  {"t": "two", "kicker": "The contract", "title": "Specified, and deliberately not",
   "lh": "The ISA specifies",
   "l": ["The instructions and what each one does.",
         "Registers: how many, how wide.",
         "Memory addressing modes.",
         "Data types and their representations.",
         "Exception and interrupt behaviour.",
         ("Everything software can observe.", 1)],
   "rh": "The ISA says nothing about",
   "r": ["Pipeline depth.",
         "Cache sizes or organisation.",
         "Whether execution is in order.",
         "Branch prediction.",
         "How many instructions issue per cycle.",
         ("Everything this course is about.", 1)],
   "note": "The right column is the whole point: it is what lets one ISA "
           "survive thirty years of radically different implementations."},

  {"t": "callout", "title": "The ISA is why x86 is still here",
   "kind": "Why the boundary matters",
   "body": ["A 1985 program still runs on a 2026 processor, despite the two "
            "sharing essentially no implementation.",
            "The 2026 chip decodes those instructions into internal "
            "micro-operations, reorders them, executes them speculatively on "
            "a dozen functional units, and retires them in order to maintain "
            "the illusion of sequential execution.",
            "The ISA is the only thing held constant. Everything beneath it "
            "has been free to change completely, and has.",
            "This is an abstraction boundary doing an enormous amount of "
            "economic work — and like all abstraction boundaries, it "
            "leaks exactly where performance is concerned."]},

  {"t": "section", "label": "Part 2", "title": "RISC and CISC",
   "blurb": "An old argument whose resolution is more interesting than "
            "either side."},

  {"t": "table", "kicker": "Philosophies", "title": "The original positions",
   "header": ["", "CISC (x86, VAX)", "RISC (ARM, RISC-V, MIPS)"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["Instructions", "Many, complex, variable length", "Few, simple, fixed length"],
     ["Memory access", "Most instructions may touch memory", "Only load and store"],
     ["Registers", "Few (8 in 32-bit x86)", "Many (32 typical)"],
     ["Decoding", "Hard — variable length", "Easy — fixed width"],
     ["Rationale", "Small code; compilers were weak", "Simple hardware; pipelines cleanly"],
   ],
   "note": "The historical context matters: CISC made sense when memory was "
           "expensive and compilers were poor. Both changed."},

  {"t": "callout", "title": "How the argument actually resolved",
   "kind": "The interesting part",
   "body": ["Modern x86 decodes its complex instructions into simple internal "
            "<b>micro-operations</b> and executes those on a RISC-like core. "
            "The CISC instruction set survives as a compatibility "
            "<i>interface</i>, not as an implementation strategy.",
            "Meanwhile ARM and RISC-V have accumulated vector extensions, "
            "cryptography instructions, and other complex operations where "
            "they pay.",
            "So RISC won the argument about <i>how to build</i> a processor, "
            "and CISC won the market through compatibility. Both outcomes are "
            "real, and the apparent contradiction dissolves once you see the "
            "ISA as an interface rather than a design."]},

  {"t": "section", "label": "Part 3", "title": "Reading assembly",
   "blurb": "You do not need to write it. You do need to read it."},

  {"t": "code", "kicker": "Why read it", "title": "The compiler is doing more than you think",
   "lang": "asm", "code": """
// C source:                    int sum(int* a, int n) {
//                                  int s = 0;
//                                  for (int i = 0; i < n; i++) s += a[i];
//                                  return s;
//                              }

// x86-64 at -O3, abbreviated:
sum:
    test    esi, esi            ; n == 0?
    jle     .empty
    ...
.vector_loop:
    vpaddd  ymm0, ymm0, [rdi+rax*4]      ; EIGHT ints added per
    vpaddd  ymm1, ymm1, [rdi+rax*4+32]   ;   instruction, two
    add     rax, 16                      ;   accumulators to break
    cmp     rax, rdx                     ;   the dependency chain
    jb      .vector_loop
    ...                                  ; horizontal sum, then a
                                         ; scalar tail for leftovers
""",
   "caption": "The compiler vectorised the loop, unrolled it, used two "
              "accumulators to break the dependency chain, and generated a "
              "scalar tail. None of that is visible in the C.",
   "note": "Compiler Explorer is the single most useful tool introduced in "
           "this course. Get them using it in week two."},

  {"t": "bullets", "kicker": "What to look for", "title": "Reading assembly for performance",
   "items": [
     "<b>Did it vectorise?</b> Look for <code>ymm</code>/<code>zmm</code> "
     "registers and <code>v</code>-prefixed instructions.",
     "<b>Did it unroll?</b> Repeated instruction groups per iteration.",
     "<b>Is the loop body tight?</b> Spills to stack memory mean register "
     "pressure.",
     "<b>Are there branches inside?</b> Could they be made branchless "
     "(Module 04)?",
     "<b>Is there a division?</b> 20–40 cycles; often replaceable.",
     "<b>Function calls in the loop?</b> Not inlined means the compiler could "
     "not see enough.",
   ],
   "footnote": "You are not checking the compiler's work. You are finding out "
               "what it could not prove."},

  {"t": "table", "kicker": "Addressing", "title": "Addressing modes and their cost",
   "header": ["Mode", "Example", "Cost"],
   "widths": [3.3, 4.4, 4.4],
   "rows": [
     ["Register", "add rax, rbx", "Free"],
     ["Immediate", "add rax, 42", "Free"],
     ["Base + displacement", "mov rax, [rbp-8]", "One memory access"],
     ["Base + index×scale", "mov rax, [rdi+rsi*8]", "Same — computed in the AGU"],
     ["Indirect through pointer", "mov rax, [rax]", "Same, but <b>serialised</b>"],
   ],
   "note": "The last row is the important one: pointer chasing is not more "
           "expensive per access, it is less parallel, and that is worse."},

  {"t": "callout", "title": "Why pointer chasing is slow",
   "kind": "The thing to remember",
   "body": ["Address arithmetic is free — dedicated address generation "
            "units compute base + index×scale + displacement at no cost.",
            "What is expensive is a <b>dependent</b> load: "
            "<code>p = p->next</code> cannot begin until the previous load "
            "has returned. Each access serialises on the one before it.",
            "An array scan issues many independent loads that overlap, so the "
            "memory system works on several at once. A linked list issues one "
            "at a time and waits ~250 cycles for each.",
            "This is why the two data structures differ by 10–50× "
            "despite identical asymptotics — the point CSCE 629 Module "
            "01 could only assert."]},

  {"t": "bullets", "kicker": "Perspective", "title": "The ISA as a leaky abstraction",
   "items": [
     "The ISA promises <i>what</i> instructions do, not <i>how fast</i>.",
     "",
     "So two programs that are functionally identical can differ by 50× "
     "and both be correct ISA-level code.",
     "",
     "Performance lives entirely in the part the ISA does not specify.",
     ("Which is why you cannot reason about speed from the instruction set "
      "alone.", 1),
     ("And why the remaining eleven modules exist.", 1),
     "",
     "Speculative execution vulnerabilities (Spectre) were this abstraction "
     "leaking in a security-relevant direction.",
   ],
   "note": "The Spectre point lands well: the abstraction boundary was always "
           "leaky for performance, and it turned out to leak for "
           "confidentiality too."},
 ],
 "takeaways": [
   "An ISA specifies what software can observe and deliberately says nothing "
   "about pipeline, caches, or execution order — which is exactly what "
   "lets implementations change radically.",
   "RISC won the argument about how to build processors; CISC won the market "
   "through compatibility. Modern x86 decodes to RISC-like micro-operations.",
   "Read the generated assembly. The compiler vectorises, unrolls, and breaks "
   "dependency chains in ways invisible in the source.",
   "Address arithmetic is free; dependent loads are not. Pointer chasing is "
   "slow because it serialises, not because each access costs more.",
   "That serialisation is why arrays beat linked lists by 10–50× at "
   "identical asymptotic complexity.",
   "Performance lives entirely in what the ISA does not specify — which "
   "is the subject of the rest of this course.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The instruction set as a contract"),
  ("p", "An instruction set architecture is the interface between software "
        "and hardware: the complete specification of what a program can "
        "observe about the machine it runs on. Its most important property is "
        "what it deliberately omits."),
  ("table", ["The ISA specifies", "The ISA says nothing about"],
   [["The instruction repertoire and the semantics of each instruction",
     "How many cycles any instruction takes"],
    ["Architectural registers: count, width, naming",
     "How many physical registers exist, or register renaming"],
    ["Addressing modes and memory semantics",
     "Cache sizes, associativity, or whether caches exist at all"],
    ["Data types and their bit representations",
     "Pipeline depth, issue width, execution order"],
    ["Exception, interrupt, and privilege behaviour",
     "Branch prediction, speculation, prefetching"]],
   [0.5, 0.5]),
  ("callout", "This separation is doing serious economic work",
   ["Software compiled in 1985 still runs on a processor built in 2026, even "
    "though the two share essentially no implementation technique. The 2026 "
    "chip breaks those instructions into internal micro-operations, reorders "
    "them aggressively, executes them speculatively across a dozen functional "
    "units, and retires them in order so the program cannot tell.",
    "Only the ISA was held fixed. Everything underneath changed completely, "
    "repeatedly, and invisibly.",
    "Like every abstraction boundary, it leaks — and it leaks precisely "
    "where performance is concerned, which is why a course on what lies "
    "beneath it is necessary."]),

  ("h1", "2 &nbsp; RISC and CISC"),
  ("table", ["", "CISC (x86, VAX, 68000)", "RISC (ARM, RISC-V, MIPS, SPARC)"],
   [["Instruction count", "Hundreds, many specialised",
     "Tens to low hundreds, each simple"],
    ["Encoding", "Variable length (1&ndash;15 bytes on x86)",
     "Fixed width (typically 4 bytes)"],
    ["Memory operands", "Most instructions may access memory",
     "Load/store only — arithmetic works on registers"],
    ["Architectural registers", "Few (8 in 32-bit x86, 16 in x86-64)",
     "Many (32 is typical)"],
    ["Original rationale",
     "Memory was expensive, so dense code mattered; compilers were weak, so "
     "complex instructions were written by hand",
     "Simple instructions pipeline cleanly and decode trivially; let the "
     "compiler build complexity"]],
   [0.17, 0.42, 0.41]),
  ("p", "The RISC argument, made in the early 1980s, was that most of a "
        "complex instruction set goes unused, that variable-length decoding "
        "is a bottleneck, and that simple uniform instructions allow deeper "
        "pipelines and faster clocks. The argument was substantially "
        "correct."),
  ("callout", "How it actually resolved",
   ["Modern x86 processors decode their complex variable-length instructions "
    "into simple fixed-format internal <b>micro-operations</b>, and execute "
    "those on what is recognisably a RISC core with register renaming and "
    "out-of-order issue. The CISC instruction set persists as a compatibility "
    "interface, not as an implementation strategy.",
    "Meanwhile, RISC architectures have acquired vector extensions, "
    "cryptographic instructions, and other complex operations wherever they "
    "earn their silicon.",
    "<b>RISC won the engineering argument; CISC won the market through "
    "compatibility.</b> The contradiction is only apparent: once you see the "
    "ISA as an interface rather than a blueprint, both outcomes follow "
    "naturally. The decode cost x86 pays is real but has become a small "
    "fraction of a large core's power and area."]),

  ("break",),
  ("h1", "3 &nbsp; Reading assembly"),
  ("p", "You will not write assembly. You will read it, because it is the "
        "only way to find out what the compiler actually did — and the "
        "compiler does a great deal that is invisible in the source."),
  ("code", """// Source
int sum(int* a, int n) {
    int s = 0;
    for (int i = 0; i < n; i++) s += a[i];
    return s;
}

// x86-64, -O3, abbreviated
.vector_loop:
    vpaddd  ymm0, ymm0, [rdi+rax*4]        ; 8 ints per instruction
    vpaddd  ymm1, ymm1, [rdi+rax*4+32]     ; second accumulator breaks
    add     rax, 16                        ;   the dependency chain
    cmp     rax, rdx
    jb      .vector_loop"""),
  ("p", "From five lines of C the compiler produced a vectorised loop "
        "processing eight integers per instruction, unrolled by two, using "
        "two independent accumulators so that successive additions do not "
        "wait on each other, followed by a horizontal reduction and a scalar "
        "tail for the remaining elements. None of this is visible in the "
        "source, and all of it affects performance by large factors."),
  ("h2", "3.1 &nbsp; What to look for"),
  ("table", ["Question", "What to look for", "If absent"],
   [["Did it vectorise?", "<code>ymm</code>/<code>zmm</code> registers, "
     "<code>v</code>-prefixed instructions",
     "Something blocked it: aliasing, a branch, a reduction the compiler "
     "could not prove reassociable (Module 09)."],
    ["Did it unroll?", "The loop body repeated several times per branch",
     "Loop overhead may dominate a short body."],
    ["Register pressure?", "<code>mov</code> to and from "
     "<code>[rsp+...]</code> inside the loop",
     "Spilling to stack. Reduce live variables."],
    ["Branches in the loop?", "<code>j</code>* instructions in the body",
     "Possibly convertible to branchless (Module 04)."],
    ["Division present?", "<code>div</code>, <code>idiv</code>",
     "20&ndash;40 cycles. Often replaceable by multiplication or a shift."],
    ["Calls not inlined?", "<code>call</code> in the hot loop",
     "The compiler lacked visibility. Consider making the definition "
     "available."]],
   [0.20, 0.34, 0.46]),
  ("p", "<b>Compiler Explorer</b> (godbolt.org) shows source and generated "
        "assembly side by side with colour-coded correspondence, for any "
        "compiler and flags. It is the single most useful tool in this course "
        "and should become habitual."),

  ("h1", "4 &nbsp; Addressing modes and the real cost of memory"),
  ("table", ["Mode", "Example", "Cost"],
   [["Register", "<code>add rax, rbx</code>", "Free."],
    ["Immediate", "<code>add rax, 42</code>", "Free."],
    ["Base + displacement", "<code>mov rax, [rbp-8]</code>",
     "One memory access; the arithmetic is free."],
    ["Base + index&times;scale + disp", "<code>mov rax, [rdi+rsi*8+16]</code>",
     "Identical cost. A dedicated address generation unit computes this "
     "without consuming an arithmetic slot — array indexing is free."],
    ["Dependent indirection", "<code>mov rax, [rax]</code>",
     "Same nominal cost, but <b>serialised</b>: the next address is not known "
     "until this load returns."]],
   [0.21, 0.30, 0.49]),
  ("callout", "Pointer chasing: the mechanism behind a 50&times; difference",
   ["Address arithmetic costs nothing. What costs is a load whose address "
    "depends on a previous load's result.",
    "Scanning an array issues many <i>independent</i> loads. The memory "
    "system can have ten or more outstanding simultaneously, and the "
    "prefetcher can predict the pattern and fetch ahead, so the latencies "
    "overlap almost completely.",
    "Traversing a linked list issues one load, waits up to ~250 cycles for "
    "it, and only then knows where to look next. Nothing overlaps and nothing "
    "can be prefetched, because the address is unknowable in advance.",
    "This is the mechanism behind the 10&ndash;50&times; gap between arrays "
    "and linked lists at identical asymptotic complexity — the gap "
    "CSCE 629 Module 01 could only assert. It is not that each access is more "
    "expensive; it is that none of them overlap."]),

  ("h1", "5 &nbsp; The abstraction leaks"),
  ("p", "The ISA tells you what an instruction computes, never how long it "
        "takes. Two functionally identical programs can differ in running "
        "time by a factor of fifty while both being entirely correct at the "
        "ISA level."),
  ("p", "All of that difference lives in the part the ISA deliberately leaves "
        "unspecified: caches, pipelines, predictors, execution order. This is "
        "precisely why you cannot reason about performance from the "
        "instruction set, and why the remaining eleven modules are "
        "necessary."),
  ("callout", "Spectre: the abstraction leaking in a new direction",
   ["The Spectre and Meltdown vulnerabilities of 2018 exploited the fact that "
    "speculative execution leaves measurable traces in the cache even when "
    "the speculated instructions are architecturally discarded.",
    "The ISA guarantees that mis-speculated instructions have no "
    "<i>architectural</i> effect, and that guarantee held. It says nothing "
    "about microarchitectural state, and that is where the information "
    "escaped.",
    "The abstraction boundary had always leaked timing information. It turned "
    "out to leak confidentiality too — a reminder that an abstraction "
    "which is merely approximately true is a security property only by "
    "accident. Module 04 returns to this."]),
 ],
 "resources": [
   ("Onur Mutlu — ISA, RISC vs CISC lectures",
    "https://safari.ethz.ch/architecture/",
    "The design-space discussion done properly, including why the historical "
    "debate resolved as it did."),
   ("MIT 6.004 — Instruction Sets, Assembly Language",
    "https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/",
    "Builds an ISA from scratch and then a processor to run it. The best way "
    "to understand what an ISA is for."),
   ("Compiler Explorer",
    "https://godbolt.org/",
    "Source and assembly side by side for any compiler and flags. Use it in "
    "every remaining module."),
   ("Agner Fog — Instruction tables",
    "https://www.agner.org/optimize/",
    "Latency and throughput for every instruction on every recent x86 "
    "microarchitecture. The reference when you need an exact number."),
   ("RISC-V specifications (free)",
    "https://riscv.org/technical/specifications/",
    "A modern ISA designed in the open, and short enough to read. "
    "Instructive by contrast with x86."),
 ],
 "exercises": [
   "Compile a simple loop at <code>-O0</code>, <code>-O1</code>, "
   "<code>-O2</code>, and <code>-O3</code> on Compiler Explorer. Describe "
   "what changes at each level and measure the running time of each.",
   "Write a reduction loop and determine whether it vectorises. If it does "
   "not, find out why — floating-point reassociation and pointer "
   "aliasing are the usual culprits — and fix it with "
   "<code>restrict</code> or <code>-ffast-math</code>, noting the semantic "
   "cost.",
   "Measure array traversal against linked-list traversal over the same "
   "number of elements, with the list nodes allocated in order and then "
   "shuffled. Explain all three results.",
   "Write a loop with enough live variables to force register spilling. Find "
   "the threshold on your machine and observe it in the assembly.",
   "Replace an integer division by a constant with a multiply-and-shift. "
   "Verify your compiler already does this, and measure the case where it "
   "cannot (a runtime divisor).",
   "Compile the same C function for x86-64 and for ARM64 (AArch64) on "
   "Compiler Explorer. Compare instruction counts and comment on the "
   "RISC/CISC differences you can actually observe.",
 ],
 "selfcheck": [
   "Name four things an ISA specifies and four it deliberately does not.",
   "Why can a 1985 binary run on a 2026 processor that shares none of its "
   "implementation?",
   "How did the RISC/CISC debate resolve, and why is 'both won' not a "
   "contradiction?",
   "Give four things to look for when reading compiler output for "
   "performance.",
   "Is <code>[rdi + rsi*8 + 16]</code> more expensive than "
   "<code>[rdi]</code>? Explain.",
   "Explain precisely why pointer chasing is slow, in terms of dependence "
   "rather than cost per access.",
   "In what sense is the ISA a leaky abstraction, and what did Spectre "
   "demonstrate about that?",
 ],
},

]

# --- additional module batches ----------------------------------------------
for _b in ("c614_b2", "c614_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
