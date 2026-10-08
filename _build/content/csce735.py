# -*- coding: utf-8 -*-
"""CSCE 735 Parallel Computing — original course content."""

COURSE = {
    "code": "CSCE 735",
    "title": "Parallel Computing",
    "tagline": "Multicore, SIMD, GPU, and distributed memory — with a "
               "performance mindset and honest measurement",
    "term": "Semester 4 (with CSCE 650 and CSCE 748)",
    "prereqs": "CSCE 629 Analysis of Algorithms; CSCE 614 Computer "
               "Architecture; fluency in C or C++",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A real workload parallelised three ways — threads, "
                   "GPU, and distributed — each with measured scaling, a "
                   "roofline placement, and an honest account of where the "
                   "speedup stopped",
    "description": [
        "Every other course in this program produced something that worked. "
        "This one is about making it fast, which turns out to be a different "
        "discipline with a different failure mode: <b>code that is correct, "
        "parallel, and no faster</b>.",
        "The organising fact is that <b>single-thread performance stopped "
        "improving</b> around 2005. Dennard scaling ended, clock speeds "
        "plateaued, and the transistors kept coming — so they went into "
        "more cores, wider vectors, and specialised units. Performance is "
        "still available and it is no longer free. Getting it requires "
        "restructuring the computation, and that is what this course "
        "teaches.",
        "The second fact is that <b>almost nothing is compute-bound</b>. "
        "The overwhelming majority of real workloads are limited by memory "
        "bandwidth, by synchronisation, or by load imbalance — and "
        "optimising the arithmetic in a bandwidth-bound loop achieves "
        "nothing. <b>Module 07's roofline model exists to tell you which "
        "problem you have</b> before you spend a week on the wrong one.",
        "Throughout, the discipline is measurement. Parallel programming is "
        "unusually rich in confident claims that do not survive a "
        "benchmark — superlinear speedups from cache effects, speedups "
        "measured against an unoptimised baseline, scaling curves that stop "
        "exactly where they would have bent. <b>This course measures "
        "everything and reports what it finds.</b>",
    ],
    "outcomes": [
        "Apply Amdahl's and Gustafson's laws and know which applies.",
        "Distinguish strong from weak scaling and measure both.",
        "Write correct shared-memory parallel code and reason about the "
        "memory model.",
        "Use atomics and lock-free techniques, and say when they are not "
        "worth it.",
        "Decompose a problem and balance the load dynamically.",
        "Build a roofline model and use it to decide what to optimise.",
        "Write and optimise CUDA kernels.",
        "Write distributed-memory programs with MPI and overlap "
        "communication.",
        "Implement the standard parallel primitives: scan, reduce, sort.",
        "Test concurrent code, and know what testing cannot establish.",
    ],
    "materials": [
        ("CMU 15-418 / Stanford CS149 — Parallel Computer Architecture "
         "and Programming (free)",
         "https://gfxcourses.stanford.edu/cs149/",
         "The primary source. Complete lectures, slides, and assignments. "
         "Kayvon Fatahalian's lectures are the best free treatment of the "
         "architecture-to-programming connection that exists."),
        ("CMU 15-418 course site (free)",
         "http://www.cs.cmu.edu/~418/",
         "The same course at CMU, with a different assignment set. Worth "
         "having both for the exercises."),
        ("NVIDIA CUDA C++ Programming Guide (free)",
         "https://web.archive.org/web/20260911074013/https://docs.nvidia.com/cuda/cuda-c-programming-guide/",
         "The reference for Modules 08 and 09. Dense, authoritative, and "
         "the Best Practices Guide alongside it is the practical companion."),
        ("OLCF CUDA Training Series (free video and exercises)",
         "https://www.olcf.ornl.gov/cuda-training-series/",
         "A structured, hands-on CUDA course from Oak Ridge. Good pacing, "
         "and the exercises run on hardware you have."),
        ("Herlihy & Shavit — The Art of Multiprocessor Programming",
         "https://www.sciencedirect.com/book/9780123973375/",
         "The reference for Modules 04 and 05. Library copy; the authors' "
         "lecture slides are free and cover the key material."),
        ("Victor Eijkhout — Introduction to High Performance Scientific "
         "Computing (free book)",
         "https://theartofhpc.com/",
         "Free, comprehensive, and strong on MPI and on the numerical "
         "side. The reference for Module 10."),
    ],
    "tooling": [
        "<b>C++17</b> with <b>OpenMP</b> and <b>std::thread</b>. The "
        "memory model work in Module 04 needs a language that has one.",
        "<b>A machine with at least 4 cores</b>, and preferably more. "
        "Scaling curves from a 2-core machine are not informative.",
        "<b>An NVIDIA GPU</b> for Modules 08 and 09. <b>A laptop GPU is "
        "sufficient</b> — the techniques are the same and the numbers are "
        "smaller. Cloud instances are an alternative.",
        "<b>A profiler you trust</b>: perf or VTune on CPU, Nsight Compute "
        "on GPU. <b>Performance claims without a profile are "
        "guesses</b>, and this course does not accept them.",
        "<b>MPI</b> — OpenMPI or MPICH. Multiple processes on one machine "
        "is adequate for correctness; borrowed nodes or a cloud cluster for "
        "the scaling study.",
        "<b>A plotting setup.</b> You will produce scaling curves and "
        "roofline plots constantly, and they are the deliverable.",
    ],
    "projects": [
        {"title": "Parallelise something real, on the CPU", "after": 7,
         "brief": "Take a genuine workload — ideally one of your own from "
                  "another course in this program — and make it fast on a "
                  "multicore machine. Measurement is the deliverable, not "
                  "the speedup.",
         "reqs": [
             "A profiled, optimised <i>serial</i> baseline. <b>Parallelising "
             "unoptimised code and reporting the speedup is the classic "
             "dishonesty</b> and is not accepted here.",
             "A threaded implementation with a stated decomposition and a "
             "stated synchronisation strategy.",
             "Strong scaling measured from 1 to the maximum available "
             "threads, plotted.",
             "Weak scaling measured over the same range, plotted "
             "separately.",
             "A roofline placement of the kernel, with the measured "
             "arithmetic intensity.",
             "A thread sanitiser run showing no data races.",
         ],
         "done": [
             "<b>Two scaling plots, strong and weak, with the point where "
             "each departs from ideal identified and explained.</b>",
             "A roofline plot with the kernel placed on it, and a statement "
             "of whether it is compute- or bandwidth-bound.",
             "<b>Speedup against the <i>optimised</i> serial baseline</b>, "
             "with that baseline's optimisation documented.",
             "<b>An honest account of where the parallelisation stopped "
             "helping and why.</b> Every workload has that point; finding it "
             "is the exercise.",
         ]},
        {"title": "GPU or distributed", "after": 12,
         "brief": "Take the same workload further. One platform, done "
                  "thoroughly, with the optimisation steps measured "
                  "individually.",
         "reqs": [
             "<b>Either</b> a CUDA implementation with at least three "
             "optimisation steps applied and measured separately — "
             "coalescing, shared memory tiling, occupancy tuning; <b>or</b> "
             "an MPI implementation with communication/computation overlap "
             "and a scaling study across nodes.",
             "A profiler report identifying the limiting resource at each "
             "stage.",
             "A roofline placement for the target platform.",
             "Correctness verified against the serial result, bitwise where "
             "the arithmetic permits and within tolerance where it does "
             "not.",
             "A comparison against a well-tuned library implementation if "
             "one exists.",
         ],
         "done": [
             "<b>A table of each optimisation step with its measured "
             "effect</b>, including any that made things worse.",
             "A profiler-supported statement of what limits the final "
             "version.",
             "<b>An honest comparison against cuBLAS, Thrust, or an "
             "equivalent library. You will probably lose.</b> Report by how "
             "much and explain where the gap is.",
             "A statement of the largest problem size the implementation "
             "handles and what fails beyond it.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Why Parallel, and What It Costs",
 "subtitle": "The free lunch ended, and the bill is restructuring.",
 "question": "Why is everything parallel now, and what does it buy?",
 "outcomes": [
     "Explain why single-thread performance stopped improving.",
     "State Amdahl's law and compute its consequences.",
     "State Gustafson's law and say when it applies instead.",
     "Distinguish strong from weak scaling.",
     "Measure and report speedup honestly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The end of the free lunch",
   "blurb": "Why the industry turned to cores."},

  {"t": "callout", "title": "Dennard scaling ended; Moore's law did not",
   "kind": "The two facts people conflate",
   "body": ["<b>Moore's law</b> — transistor count doubling — "
            "continued for a long time after the change, and is slowing now "
            "for different reasons.",
            "<b>Dennard scaling</b> — power density staying constant as "
            "transistors shrink — <b>broke around 2005</b>. Leakage "
            "current stopped falling with voltage.",
            "<b>So clock speeds stopped rising</b> while transistor budgets "
            "kept growing. The transistors had to go somewhere.",
            "<b>They went into cores, wider vector units, and specialised "
            "hardware</b> — all of which require the programmer to "
            "restructure the computation. <b>That is the bill.</b>"]},

  {"t": "table", "kicker": "Where they went", "title": "What the transistors bought",
   "header": ["Resource", "Scaling", "Requires"],
   "widths": [2.8, 4.2, 5.1],
   "rows": [
     ["Clock speed", "<b>Stopped ~2005</b>", "Nothing — it was free"],
     ["<b>Cores</b>", "<b>Still growing</b>", "<b>Explicit parallelism</b>"],
     ["<b>SIMD width</b>", "<b>Still growing</b>", "<b>Vectorisable loops</b>"],
     ["Cache", "Growing slowly", "Locality"],
     ["<b>Specialised units</b>", "<b>Growing fastest</b>", "<b>Using the right library</b>"],
   ],
   "footnote": "<b>Every row after the first requires the programmer to "
               "do something.</b> That is the entire reason this course "
               "exists.",
   "note": "The 'free versus earned' distinction in the last column is the "
           "framing worth keeping."},

  {"t": "section", "label": "Part 2", "title": "Amdahl's law",
   "blurb": "The serial fraction bounds everything."},

  {"t": "eq", "kicker": "Amdahl", "title": "The limit on speedup",
   "eqs": [
     ("S(n) = 1 / ( s + (1−s)/n )",
      "Speedup with n processors, where s is the fraction of the work that "
      "is inherently serial."),
     ("S(∞) = 1/s",
      "As n grows without bound, speedup approaches the reciprocal of the "
      "serial fraction. And nothing exceeds it."),
     ("s = 0.05  ⟹  S(∞) = 20",
      "Five percent serial caps you at 20×, no matter how many cores "
      "you buy."),
   ],
   "caption": "The bound depends only on the serial fraction, not on the "
              "hardware. This is why reducing s matters more than adding "
              "cores.",
   "note": "Have them compute S for s = 0.01, 0.05, 0.1 at n = 1000. The "
           "numbers are sobering."},

  {"t": "table", "kicker": "Amdahl", "title": "What the serial fraction costs",
   "header": ["Serial fraction", "Speedup at n=16", "Speedup at n=1024", "Ceiling"],
   "widths": [2.8, 2.8, 3.0, 3.5],
   "rows": [
     ["0.1%", "15.9", "<b>506</b>", "1000"],
     ["1%", "13.9", "<b>91</b>", "100"],
     ["<b>5%</b>", "<b>9.1</b>", "<b>19.6</b>", "<b>20</b>"],
     ["10%", "6.4", "<b>9.9</b>", "10"],
     ["50%", "1.9", "2.0", "<b>2</b>"],
   ],
   "footnote": "<b>At 5% serial, going from 16 to 1024 cores buys a factor "
               "of two.</b> Sixty-four times the hardware.",
   "note": "That row is the one to dwell on. It explains why large core "
           "counts are not a general solution."},

  {"t": "callout", "title": "The serial fraction is larger than you think",
   "kind": "What counts as serial",
   "body": ["<b>Not just the obviously sequential code.</b> Everything that "
            "does not scale counts.",
            "<b>Startup and teardown.</b> Reading input, allocating, "
            "building data structures, writing output.",
            "<b>Synchronisation.</b> Time at a barrier is time not spent "
            "computing.",
            "<b>Load imbalance.</b> If one thread takes twice as long, the "
            "others' idle time is effectively serial.",
            "<b>And the parallel overhead itself</b> — thread creation, "
            "communication, scheduling. <b>All of it lands in s.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Gustafson's law",
   "blurb": "The other half of the story."},

  {"t": "callout", "title": "Gustafson: problems grow with the machine",
   "kind": "Why supercomputers are useful",
   "body": ["<b>Amdahl assumes a fixed problem size</b> and asks how much "
            "faster you can solve it.",
            "<b>Gustafson observes that nobody buys a bigger machine to "
            "solve the same problem faster.</b> They solve a bigger "
            "problem.",
            "<b>And the serial fraction usually does not grow with problem "
            "size.</b> Reading a configuration file costs the same for a "
            "grid of any size.",
            "<b>So scaled speedup is nearly linear</b> — which is why "
            "machines with a hundred thousand cores are worth building, "
            "despite Amdahl."]},

  {"t": "two", "kicker": "Two laws", "title": "Strong and weak scaling",
   "lh": "Strong scaling (Amdahl)",
   "l": ["<b>Fixed total problem size</b>, more processors.",
         "Each processor gets less work.",
         "<b>Bounded by the serial fraction.</b>",
         ("Communication-to-computation ratio worsens.", 1),
         "Asks: how fast can I solve <i>this</i>?"],
   "rh": "Weak scaling (Gustafson)",
   "r": ["<b>Fixed work per processor</b>, more processors.",
         "Total problem size grows with n.",
         "<b>Can stay near linear.</b>",
         ("Ratio stays roughly constant.", 1),
         "Asks: how big a problem can I solve?"],
   "note": "Both are legitimate and they answer different questions. "
           "Reporting only the flattering one is the common dishonesty."},

  {"t": "callout", "title": "Report both, and say which you measured",
   "kind": "The honesty requirement",
   "body": ["<b>Weak scaling curves look better</b>, and a paper showing "
            "only weak scaling is making a weaker claim than it appears to.",
            "<b>Strong scaling is what most users care about</b> — they "
            "have a problem and want it solved sooner.",
            "<b>So measure and report both</b>, and label them "
            "unambiguously.",
            "<b>And state the baseline.</b> Speedup against an unoptimised "
            "serial version is the oldest trick in the field, and it is "
            "still common."]},

  {"t": "bullets", "kicker": "Honesty", "title": "How speedup is misreported",
   "items": [
     "<b>Against an unoptimised baseline.</b> Parallelise bad code and the "
     "speedup is flattering and meaningless.",
     "",
     "<b>Against a different algorithm.</b> Comparing your parallel method "
     "to a worse serial one.",
     "",
     "<b>Scaling plots that stop</b> exactly where the curve would have "
     "bent.",
     "",
     "<b>Superlinear speedup claimed as a triumph</b> — it is usually a "
     "cache effect and it means the baseline fitted poorly.",
     "",
     "<b>And best-of-many timings</b> rather than a distribution.",
   ],
   "footnote": "<b>All five are common in published work.</b> Reading for "
               "them is a skill.",
   "note": "Superlinear speedup deserves explanation rather than "
           "celebration — it usually indicates a baseline problem."},
 ],
 "takeaways": [
   "Dennard scaling ended around 2005, not Moore's law — so clocks "
   "stopped rising while transistor budgets grew, and the transistors went "
   "into cores and vector units.",
   "Every resource except clock speed requires the programmer to restructure "
   "the computation. Performance stopped being free.",
   "Amdahl: speedup is bounded by 1/s where s is the serial fraction. At 5% "
   "serial, going from 16 to 1024 cores buys a factor of two.",
   "The serial fraction includes startup, synchronisation, load imbalance, "
   "and parallel overhead — which makes it larger than it first looks.",
   "Gustafson: problems grow with the machine, and the serial part usually "
   "does not, so scaled speedup stays near linear.",
   "Strong scaling fixes the problem and adds processors; weak scaling fixes "
   "the work per processor. Report both and state the baseline.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why everything became parallel"),
  ("callout", "Dennard scaling ended; Moore's law did not",
   ["These are routinely conflated and they are different observations with "
    "different fates.",
    "<b>Moore's law</b> is the observation that transistor density doubles "
    "roughly every two years. It continued for well over a decade after the "
    "change described here, and is slowing now for reasons of physics and "
    "economics.",
    "<b>Dennard scaling</b> is the observation that as transistors shrink, "
    "power density stays constant — smaller transistors need less "
    "voltage and switch faster, so you get more, faster transistors for the "
    "same power. <b>This broke around 2005</b>, because leakage current "
    "stopped falling as voltage dropped, so reducing voltage further stopped "
    "saving power.",
    "<b>So clock speeds plateaued while transistor budgets kept "
    "growing.</b> The transistors still arrived and could no longer be spent "
    "on making one core faster. <b>They went into more cores, wider vector "
    "units, larger caches, and specialised accelerators</b> — every one "
    "of which requires the programmer to restructure the computation to "
    "benefit. <b>That restructuring is the bill</b>, and this course is "
    "about paying it."]),
  ("table", ["Resource", "Trend", "What it requires of you"],
   [["<b>Clock frequency</b>", "<b>Flat since about 2005.</b>",
     "<b>Nothing.</b> It was free, and it is over."],
    ["<b>Core count</b>", "Still growing; 64 to 128 cores is now ordinary "
     "in a server.",
     "<b>Explicit parallelism</b> — threads, tasks, processes "
     "(Modules 03, 06, 10)."],
    ["<b>SIMD width</b>", "Growing: 128 bits, then 256, then 512.",
     "<b>Vectorisable loops</b> — regular access patterns, no "
     "dependencies, no unpredictable branches (Module 02)."],
    ["<b>Cache capacity</b>", "Growing slowly.",
     "<b>Locality.</b> The algorithm must reuse data while it is still "
     "resident (CSCE 614)."],
    ["<b>Specialised units</b>", "<b>Growing fastest</b> — tensor "
     "cores, matrix engines, media accelerators.",
     "<b>Using the right library</b>, because hand-writing for them is "
     "rarely worthwhile."]],
   [0.18, 0.37, 0.45]),
  ("p", "<b>Every row after the first requires the programmer to do "
        "something</b>, and that is the whole reason this course exists. "
        "Before 2005 a program got faster by waiting; now it gets faster by "
        "being rewritten."),

  ("h1", "2 &nbsp; Amdahl's law"),
  ("eq", "S(n) = 1 / ( s + (1 &minus; s)/n ) &nbsp;&nbsp;&nbsp;&nbsp; "
         "S(&infin;) = 1/s"),
  ("p", "where s is the fraction of the total work that is inherently "
        "serial. <b>The bound depends only on s, not on the hardware</b> "
        "— which is why reducing the serial fraction matters far more "
        "than acquiring more cores."),
  ("table", ["Serial fraction s", "S at n=16", "S at n=256", "S at n=1024",
             "Ceiling"],
   [["0.1%", "15.9", "203", "<b>506</b>", "1000"],
    ["1%", "13.9", "72", "<b>91</b>", "100"],
    ["<b>5%</b>", "<b>9.1</b>", "<b>17.4</b>", "<b>19.6</b>", "<b>20</b>"],
    ["10%", "6.4", "9.7", "<b>9.9</b>", "10"],
    ["50%", "1.9", "2.0", "2.0", "<b>2</b>"]],
   [0.24, 0.17, 0.17, 0.19, 0.23]),
  ("p", "<b>Look at the 5% row.</b> Going from 16 cores to 1024 — "
        "sixty-four times the hardware — takes the speedup from 9.1 to "
        "19.6. <b>A factor of about two, for sixty-four times the "
        "machine.</b> This single row explains why large core counts are not "
        "a general-purpose solution and why so much effort goes into "
        "shrinking s."),
  ("callout", "The serial fraction is larger than it looks",
   ["<b>It is not only the obviously sequential code.</b> Everything that "
    "does not scale with the processor count lands in s, whether or not it "
    "looks serial.",
    "<b>Startup and teardown.</b> Reading the input file, allocating "
    "memory, building the data structure, writing the output. These often "
    "run on one thread and often take longer than anyone estimated.",
    "<b>Synchronisation.</b> Time spent waiting at a barrier is time not "
    "spent computing, and a barrier costs the <i>slowest</i> thread's time "
    "multiplied by the thread count.",
    "<b>Load imbalance.</b> If one thread's share takes twice as long as "
    "the others', every other thread's idle time is effectively serial "
    "(Module 06).",
    "<b>And the parallel overhead itself</b> — thread creation, task "
    "scheduling, communication, false sharing. <b>All of it lands in s</b>, "
    "which is why measured speedups fall short of Amdahl's prediction rather "
    "than matching it."]),

  ("h1", "3 &nbsp; Gustafson's law"),
  ("callout", "Problems grow with the machine",
   ["<b>Amdahl assumes a fixed problem size</b> and asks how much faster a "
    "larger machine can solve it. Under that assumption the answer is "
    "discouraging, and the law is frequently cited as a reason parallelism "
    "is futile.",
    "<b>Gustafson observed that the assumption is usually wrong.</b> "
    "Nobody acquires a machine with a hundred thousand cores in order to "
    "solve the same problem they were solving before, slightly faster. They "
    "solve a larger problem — a finer grid, more particles, a longer "
    "simulation, a bigger model.",
    "<b>And the serial portion usually does not grow with the problem "
    "size.</b> Parsing a configuration file, initialising, and writing a "
    "summary cost roughly the same for a grid of any resolution.",
    "<b>So the <i>scaled</i> speedup — work done per unit time as both "
    "the machine and the problem grow — stays close to linear.</b> "
    "This is why machines with enormous core counts are worth building, and "
    "it is not in conflict with Amdahl: the two laws answer different "
    "questions about different situations."]),
  ("table", ["", "Strong scaling (Amdahl)", "Weak scaling (Gustafson)"],
   [["Held fixed", "<b>The total problem size.</b>",
     "<b>The work per processor.</b>"],
    ["As n grows", "Each processor gets a smaller share.",
     "The total problem grows proportionally."],
    ["Bounded by", "<b>The serial fraction</b> — hard ceiling at "
     "1/s.", "<b>Can remain near linear.</b>"],
    ["Communication", "<b>Worsens</b> — less computation per "
     "processor against roughly the same communication, so the ratio "
     "degrades.",
     "Stays roughly constant, since both grow together."],
    ["Answers", "'How much faster can I solve <i>this</i> problem?'",
     "'How large a problem can I solve in a fixed time?'"]],
   [0.14, 0.43, 0.43]),
  ("callout", "Report both, and state the baseline",
   ["<b>Weak scaling curves look better</b>, nearly always. A result "
    "showing only weak scaling is making a substantially weaker claim than a "
    "casual reader will take it to be.",
    "<b>Strong scaling is what most users actually care about.</b> They "
    "have a problem of a particular size and want the answer sooner; the "
    "option of solving a bigger problem instead is not useful to them.",
    "<b>So measure and report both, clearly labelled.</b> The pair tells a "
    "complete story and either alone does not.",
    "<b>And state the serial baseline explicitly.</b> Speedup measured "
    "against an unoptimised serial implementation is the oldest trick in "
    "performance reporting and remains common — a poorly written serial "
    "version makes any parallel version look excellent, and the comparison "
    "measures the quality of the baseline rather than the parallelisation."]),
  ("ul", ["<b>Speedup against an unoptimised baseline.</b> Parallelising "
          "badly written serial code produces flattering numbers that mean "
          "nothing. <b>Project 1 requires a profiled, optimised serial "
          "baseline for exactly this reason.</b>",
          "<b>Speedup against a different algorithm.</b> Comparing a "
          "parallel implementation of a good algorithm against a serial "
          "implementation of a worse one.",
          "<b>Scaling plots that stop exactly where the curve would have "
          "bent.</b> If a plot ends at 16 cores on a 64-core machine, ask "
          "why.",
          "<b>Superlinear speedup presented as a triumph.</b> It is "
          "<i>possible</i> — n processors have n times the cache, so a "
          "working set that did not fit on one may fit when divided. But it "
          "usually indicates that the serial baseline was cache-thrashing, "
          "which means the baseline was poorly chosen. <b>It deserves an "
          "explanation, not a celebration.</b>",
          "<b>Best-of-many timings rather than a distribution.</b> Report "
          "the median and the spread; a minimum over twenty runs describes a "
          "machine with no other load, which is not the machine anyone "
          "has."]),
 ],
 "resources": [
   ("Stanford CS149 / CMU 15-418 &mdash; Lecture 1 and the scaling lectures "
    "(free)",
    "https://gfxcourses.stanford.edu/cs149/",
    "Why parallelism, Amdahl, and the architectural history. The primary "
    "source for this module."),
   ("Sutter &mdash; The Free Lunch Is Over (2005, free)",
    "http://www.gotw.ca/publications/concurrency-ddj.htm",
    "The essay that named the change in &sect;1, written as it was "
    "happening. Short and still accurate."),
   ("Gustafson &mdash; Reevaluating Amdahl's Law (1988, free)",
    "https://dl.acm.org/doi/10.1145/42411.42415",
    "Two pages, and it reframes the whole question. Read it immediately "
    "after Amdahl."),
   ("Hoefler & Belli &mdash; Scientific Benchmarking of Parallel Computing "
    "Systems (free)",
    "https://htor.inf.ethz.ch/publications/index.php?pub=222",
    "<b>How to measure and report honestly</b> — the material in "
    "&sect;3, made rigorous. Read it before producing any scaling plot."),
 ],
 "exercises": [
   "Compute Amdahl speedup for s = 0.001, 0.01, 0.05, 0.1 at n = 2, 16, 256, "
   "1024. Plot the curves on one figure.",
   "For a program you have written, estimate the serial fraction by timing "
   "the phases. Include startup and I/O.",
   "Instrument that program to measure time spent at barriers and add it to "
   "your serial fraction estimate.",
   "Compute the Gustafson scaled speedup for the same serial fractions and "
   "compare against Amdahl on one plot.",
   "Take any parallel program and measure both strong and weak scaling. Plot "
   "them separately and identify where each departs from ideal.",
   "<b>Deliberately construct a misleading speedup claim</b> using an "
   "unoptimised baseline, then correct it. Report both numbers.",
   "Construct a case exhibiting superlinear speedup from cache effects, and "
   "explain it.",
   "Run the same benchmark twenty times and plot the distribution of "
   "timings. Report median and interquartile range rather than the minimum.",
   "Find a published parallel computing result and check it against the five "
   "failure modes in &sect;3.",
 ],
 "selfcheck": [
   "Distinguish Moore's law from Dennard scaling and say which ended when.",
   "Name five resources transistors went into and what each requires of the "
   "programmer.",
   "State Amdahl's law and compute the speedup for s = 0.05 at n = 1024.",
   "Give five things that count toward the serial fraction.",
   "State Gustafson's law and explain why it does not contradict Amdahl.",
   "Distinguish strong from weak scaling on five axes.",
   "Why do weak scaling curves look better, and what should you report?",
   "Give five ways speedup is misreported.",
   "Why does superlinear speedup require explanation?",
 ],
},

]

# --- additional module batches ----------------------------------------------
for _b in ("c735_b2", "c735_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
