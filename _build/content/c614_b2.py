# -*- coding: utf-8 -*-
"""CSCE 614 — Modules 03-07."""

MODULES = [

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Pipelining and Hazards",
 "subtitle": "Overlapping instructions, and the three things that stop you.",
 "question": "How do you execute several instructions at once without "
             "breaking the program?",
 "outcomes": [
     "Explain the classic five-stage pipeline and why pipelining raises "
     "throughput, not latency.",
     "Identify structural, data, and control hazards.",
     "Explain forwarding and when it is insufficient.",
     "Explain why deeper pipelines increase misprediction cost.",
     "Relate pipeline behaviour to measurable CPI.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The idea",
   "blurb": "An assembly line for instructions."},

  {"t": "table", "kicker": "Stages", "title": "The classic five stages",
   "header": ["Stage", "Does", "Needs"],
   "widths": [2.6, 5.0, 4.5],
   "rows": [
     ["IF — fetch", "Read the instruction from memory", "Instruction cache, PC"],
     ["ID — decode", "Decode it; read registers", "Register file"],
     ["EX — execute", "Do the arithmetic; compute addresses", "ALU"],
     ["MEM — memory", "Load or store", "Data cache"],
     ["WB — write back", "Write the result to a register", "Register file"],
   ],
   "note": "Real pipelines are 14-20 stages, but the five-stage model "
           "exposes every concept and nothing extra."},

  {"t": "callout", "title": "Throughput, not latency", "kind": "Key idea",
   "body": ["Pipelining does <b>not</b> make any single instruction faster. "
            "An instruction still traverses all five stages.",
            "It makes the processor <i>finish</i> one instruction per cycle "
            "instead of one every five, by overlapping five instructions in "
            "different stages.",
            "Ideal speedup is the number of stages. In practice it is less, "
            "because of hazards — and because the pipeline registers "
            "between stages add real delay.",
            "This is the same throughput-versus-latency distinction as the "
            "graphics pipeline in CSCE 641, and for the same reason."]},

  {"t": "section", "label": "Part 2", "title": "Three hazards",
   "blurb": "Everything that prevents the next instruction starting on "
            "schedule."},

  {"t": "table", "kicker": "Hazards", "title": "The three classes",
   "header": ["Hazard", "Cause", "Fix"],
   "widths": [2.6, 4.8, 4.7],
   "rows": [
     ["Structural", "Two instructions need the same hardware",
      "Duplicate it, or stall"],
     ["Data", "An instruction needs a result not yet produced",
      "Forwarding; stall if still too early"],
     ["Control", "The next address is not yet known",
      "Predict and speculate (Module 04)"],
   ],
   "note": "Everything in the next ten modules is an elaboration of one of "
           "these three rows."},

  {"t": "code", "kicker": "Data hazard", "title": "Forwarding: the result before it is written",
   "lang": "asm", "code": """
    add  r1, r2, r3     ; r1 is produced in EX, written in WB
    sub  r4, r1, r5     ; needs r1 in its OWN EX -- one cycle later

Without forwarding: sub must wait until add reaches WB -> 3 stalls.

With forwarding: the ALU output of `add` is routed directly to the
ALU input of `sub`. Zero stalls.

BUT:
    ld   r1, 0(r2)      ; r1 available only after MEM
    add  r4, r1, r5     ; needs r1 in EX -- which is EARLIER

    -> the value does not exist yet. Forwarding cannot help.
    -> one unavoidable stall: the LOAD-USE HAZARD.
""",
   "caption": "Forwarding removes most data hazards. The load-use case is the "
              "one it cannot, which is why compilers schedule an independent "
              "instruction into that slot.",
   "note": "The load-use hazard is the one that survives into modern "
           "machines, and the reason instruction scheduling matters."},

  {"t": "bullets", "kicker": "Data hazards", "title": "Three kinds of dependence",
   "items": [
     "<b>RAW</b> (read after write) — a <i>true</i> dependence. Real "
     "information flow; cannot be removed.",
     "",
     "<b>WAR</b> (write after read) and <b>WAW</b> (write after write) "
     "— <i>false</i> dependences.",
     ("They exist only because two instructions happened to use the same "
      "register name.", 1),
     ("Removed by <b>register renaming</b> — Module 08.", 1),
     "",
     "Only RAW is fundamental. The other two are artefacts of having finitely "
     "many architectural register names.",
   ],
   "note": "Framing WAR/WAW as naming artefacts makes register renaming "
           "feel inevitable rather than clever."},

  {"t": "callout", "title": "Control hazards are the expensive ones",
   "kind": "The real problem",
   "body": ["After a branch, the processor does not know which instruction to "
            "fetch next until the branch resolves in EX.",
            "Stalling until then wastes several cycles on <b>every single "
            "branch</b> — and roughly one instruction in five is a "
            "branch.",
            "That is intolerable, so processors <i>guess</i> and execute "
            "speculatively. When the guess is right, nothing is lost; when "
            "wrong, the speculated work is discarded.",
            "The entire mechanism of Module 04 exists because of this one "
            "hazard."]},

  {"t": "section", "label": "Part 3", "title": "Depth and its costs",
   "blurb": "Why pipelines got deeper, and why that stopped."},

  {"t": "bullets", "kicker": "Depth", "title": "Deeper pipelines: the trade",
   "items": [
     "Less work per stage → shorter cycle → higher clock frequency.",
     "",
     "<b>But:</b> misprediction penalty is proportional to depth.",
     ("5 stages → ~3 cycles wasted. 20 stages → ~15–20.", 1),
     "",
     "Pentium 4 pushed to 31 stages chasing clock speed.",
     ("High frequency, poor performance per cycle, and enormous power. The "
      "design was abandoned.", 1),
     "",
     "Modern cores settle around 14–20 stages — the balance point.",
   ],
   "footnote": "An instructive case of a metric (clock speed) being optimised "
               "at the expense of the thing it was a proxy for."},

  {"t": "eq", "kicker": "Cost", "title": "What hazards do to CPI",
   "eqs": [
     ("CPI  =  1  +  stalls per instruction",
      "Ideal pipelined CPI is 1. Everything above that is a hazard."),
     ("branch stalls  =  frequency × misprediction rate × penalty",
      "20% branches × 5% mispredicted × 15 cycles = 0.15 CPI."),
     ("memory stalls  =  miss rate × miss penalty",
      "2% miss × 250 cycles = <b>5.0 CPI</b>. Memory dominates "
      "everything."),
   ],
   "caption": "Compare the last two lines. A 2% cache miss rate costs more "
              "than thirty times what a 5% branch misprediction rate does.",
   "note": "This comparison is the justification for spending Modules 5-7 on "
           "memory and only one module on branches."},

  {"t": "bullets", "kicker": "In practice", "title": "What this means for your code",
   "items": [
     "<b>Dependency chains limit speed.</b> A chain of dependent operations "
     "runs at one per latency, not one per cycle.",
     ("Use multiple accumulators to break chains — as the compiler did "
      "in Module 02.", 1),
     "",
     "<b>Loads early.</b> Issue a load several instructions before the value "
     "is needed.",
     "",
     "<b>Branches cost, but memory costs more.</b> Check IPC and cache "
     "misses before restructuring control flow.",
     "",
     "Compilers schedule for this automatically. Your job is to not block "
     "them — usually by avoiding aliasing and keeping loops simple.",
   ]},
 ],
 "takeaways": [
   "Pipelining raises throughput, not latency: an instruction still takes "
   "five stages, but one completes per cycle.",
   "Three hazards: structural (resource conflict), data (value not ready), "
   "control (next address unknown).",
   "Forwarding removes most data hazards. The load-use hazard survives, which "
   "is why instruction scheduling matters.",
   "Only RAW is a true dependence. WAR and WAW are artefacts of register "
   "naming, removed by renaming in Module 08.",
   "Misprediction penalty scales with pipeline depth, which is why the "
   "31-stage Pentium 4 failed and modern cores sit at 14–20.",
   "A 2% cache miss rate costs ~5.0 CPI; a 5% branch miss rate costs ~0.15. "
   "Memory dominates.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why pipeline"),
  ("p", "Executing an instruction takes several distinct steps, each using "
        "different hardware. Doing them strictly one instruction at a time "
        "leaves most of the processor idle most of the time."),
  ("table", ["Stage", "What happens", "Hardware used"],
   [["IF — instruction fetch", "Read the instruction at the program "
     "counter", "Instruction cache"],
    ["ID — decode", "Interpret the instruction; read source registers",
     "Decoder, register file"],
    ["EX — execute", "Perform arithmetic; compute memory addresses; "
     "resolve branches", "ALU"],
    ["MEM — memory", "Perform a load or store", "Data cache"],
    ["WB — write back", "Write the result into a register",
     "Register file"]],
   [0.26, 0.47, 0.27]),
  ("p", "Overlap them. While instruction 1 is in MEM, instruction 2 can be in "
        "EX, instruction 3 in ID, and instruction 4 in IF. All five units are "
        "busy and the processor completes one instruction per cycle instead "
        "of one every five."),
  ("callout", "Throughput, not latency",
   ["Pipelining makes no individual instruction faster. Each still passes "
    "through every stage, and the pipeline registers between stages add a "
    "little delay, so per-instruction latency actually increases slightly.",
    "What improves is the <i>rate</i> of completion. The ideal is one "
    "instruction per cycle regardless of how many stages there are — "
    "throughput equal to the stage count, latency unchanged.",
    "This is the same trade the graphics pipeline makes in CSCE 641 Module "
    "01, for the same reason, and it recurs throughout computer "
    "architecture."]),

  ("h1", "2 &nbsp; Hazards"),
  ("p", "A <b>hazard</b> is anything preventing the next instruction from "
        "beginning on schedule. There are exactly three kinds, and every "
        "mechanism in the rest of this course addresses one of them."),
  ("h2", "2.1 &nbsp; Structural hazards"),
  ("p", "Two instructions need the same hardware in the same cycle. If there "
        "is a single memory port, an instruction fetch in IF and a load in "
        "MEM collide. The solution is duplication: separate instruction and "
        "data caches, multiple ALUs, multiple register-file ports. Structural "
        "hazards are largely engineered away in modern designs — silicon "
        "is cheap enough to duplicate what matters."),
  ("h2", "2.2 &nbsp; Data hazards"),
  ("p", "An instruction needs a value that an earlier, still-executing "
        "instruction has not yet produced."),
  ("code", """    add  r1, r2, r3     ; r1 computed in EX, written in WB
    sub  r4, r1, r5     ; needs r1 in its own EX, one cycle later

Naively: sub stalls until add reaches WB -> three wasted cycles."""),
  ("p", "<b>Forwarding</b> (also called bypassing) fixes this: the value "
        "exists at the ALU output as soon as EX completes, so route it "
        "directly to the next instruction's ALU input rather than waiting for "
        "it to travel through MEM and WB. Most data hazards vanish at the "
        "cost of some wiring and multiplexers."),
  ("callout", "The load-use hazard: the one forwarding cannot fix",
   ["<code>ld r1, 0(r2)</code> followed immediately by "
    "<code>add r4, r1, r5</code>.",
    "The loaded value is not available until the end of MEM, but the "
    "<code>add</code> needs it in EX — which is <i>earlier</i>. "
    "Forwarding cannot send a value backwards in time, so at least one stall "
    "is unavoidable.",
    "This is why compilers schedule an independent instruction into the slot "
    "after a load, and why issuing loads well before their results are needed "
    "is a real optimisation. On modern out-of-order cores the hardware hides "
    "much of this (Module 08), but the principle persists."]),
  ("h2", "2.3 &nbsp; True and false dependences"),
  ("table", ["Type", "Pattern", "Nature"],
   [["<b>RAW</b> (read after write)", "B reads what A wrote",
     "<b>True dependence.</b> Real information flow. Cannot be removed by any "
     "means — the value genuinely must be computed first."],
    ["<b>WAR</b> (write after read)", "B overwrites what A reads",
     "<b>False.</b> Exists only because both instructions use the same "
     "register <i>name</i>."],
    ["<b>WAW</b> (write after write)", "B overwrites what A wrote",
     "<b>False.</b> Same cause."]],
   [0.26, 0.26, 0.48]),
  ("p", "The distinction matters a great deal. False dependences arise purely "
        "because an ISA offers finitely many register names, so unrelated "
        "computations are forced to reuse them. Supply more physical "
        "registers than architectural ones and rename on the fly, and the "
        "false dependences disappear entirely. That is <b>register "
        "renaming</b>, and Module 08 shows it is what makes out-of-order "
        "execution possible."),
  ("h2", "2.4 &nbsp; Control hazards"),
  ("p", "After a branch, which instruction should be fetched next? The answer "
        "is unknown until the branch condition is evaluated in EX. Stalling "
        "until then costs several cycles on every branch, and roughly one "
        "instruction in five is a branch."),
  ("p", "The resolution is to guess and proceed speculatively, discarding the "
        "work if the guess was wrong. Module 04 is entirely about making that "
        "guess well."),

  ("break",),
  ("h1", "3 &nbsp; Pipeline depth"),
  ("p", "Dividing the work into more, smaller stages shortens the critical "
        "path through each stage, which permits a higher clock frequency. "
        "This drove designs deeper through the 1990s."),
  ("callout", "Why it stopped",
   ["The misprediction penalty is roughly the pipeline depth: everything "
    "fetched after a mispredicted branch must be discarded. A five-stage "
    "pipeline loses about three cycles; a twenty-stage pipeline loses "
    "fifteen to twenty.",
    "The Pentium 4 took this to 31 stages in pursuit of headline clock "
    "speed. It achieved high frequencies, poor performance per cycle, and "
    "power consumption that proved unmanageable. Intel abandoned the "
    "architecture and returned to a shorter, wider design.",
    "Modern cores sit at 14&ndash;20 stages, which is roughly where the "
    "frequency gain and the misprediction cost balance. It is a good example "
    "of a proxy metric — clock speed — being optimised at the "
    "expense of the thing it was supposed to stand for."]),

  ("h1", "4 &nbsp; What hazards cost, quantitatively"),
  ("eq", "CPI = 1 + stalls per instruction"),
  ("p", "An ideal pipeline achieves CPI 1. Every stall adds to it, and the "
        "arithmetic is worth doing because the result is counterintuitive."),
  ("table", ["Source", "Calculation", "CPI contribution"],
   [["Branch mispredictions",
     "20% branches &times; 5% mispredicted &times; 15 cycles", "0.15"],
    ["L1 misses served by L2",
     "30% memory ops &times; 5% miss &times; 12 cycles", "0.18"],
    ["Misses to main memory",
     "30% memory ops &times; 2% miss &times; 250 cycles", "<b>1.50</b>"],
    ["Load-use stalls", "10% of instructions &times; 1 cycle", "0.10"]],
   [0.28, 0.46, 0.26]),
  ("callout", "Why this course spends three modules on memory and one on branches",
   ["Compare the rows. A 5% branch misprediction rate contributes 0.15 to "
    "CPI. A 2% main-memory miss rate contributes 1.50 — ten times more, "
    "from a far lower event rate.",
    "Memory is the dominant term in almost every real program's CPI, by a "
    "wide margin. That is why Modules 05 through 07 are about the memory "
    "hierarchy, and why 'is this memory-bound?' is the first question to ask "
    "of any slow code.",
    "It is also why the RAM model's assumption of uniform memory cost is not "
    "a small inaccuracy but the single largest error in the model."]),

  ("h1", "5 &nbsp; Consequences for code you write"),
  ("ul", ["<b>Dependency chains limit throughput.</b> A sequence of dependent "
          "operations proceeds at one per <i>latency</i>, not one per cycle. "
          "Summing an array into a single accumulator is limited by addition "
          "latency; using four accumulators and combining at the end is "
          "roughly four times faster. This is exactly what the compiler did "
          "in Module 02.",
          "<b>Issue loads early.</b> The further ahead of its use a load is "
          "issued, the more latency can be hidden behind other work.",
          "<b>Check memory before control flow.</b> Branch restructuring is "
          "visible and satisfying; it is usually not where the time is. "
          "Measure IPC and cache miss rate first.",
          "<b>Let the compiler schedule.</b> Modern compilers schedule "
          "instructions well. The useful contribution is usually to stop "
          "blocking them — avoid pointer aliasing, keep loop bodies "
          "simple, make functions inlinable."]),
 ],
 "resources": [
   ("Onur Mutlu — Pipelining, Pipeline Hazards lectures",
    "https://safari.ethz.ch/architecture/",
    "The full treatment including forwarding paths and the depth trade-off."),
   ("MIT 6.004 — Pipelined Processors",
    "https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/",
    "Builds a pipelined processor stage by stage. The best way to make "
    "forwarding concrete."),
   ("Nand2Tetris Projects 1–6",
    "https://www.nand2tetris.org/",
    "Build a CPU from gates. Not pipelined, but the understanding transfers."),
   ("Agner Fog — The microarchitecture of Intel, AMD and VIA CPUs",
    "https://www.agner.org/optimize/",
    "What real pipelines look like, core by core. Dense, and the definitive "
    "free reference."),
 ],
 "exercises": [
   "Write a loop summing an array into one accumulator, then into two, four, "
   "and eight. Measure all four and explain the curve in terms of dependency "
   "chains and addition latency. Find where it stops improving and say why.",
   "Construct a load-use hazard in C and inspect the generated assembly. Does "
   "the compiler schedule an independent instruction into the gap?",
   "Measure a loop with a long dependency chain against one with independent "
   "operations, matched for instruction count. Report IPC for both using "
   "<code>perf stat</code>.",
   "Compute the CPI contribution of branches and of memory for a program of "
   "your own, using hardware counters. Which dominates?",
   "Write two versions of a loop that differ only in whether consecutive "
   "iterations are dependent. Predict the ratio before measuring, then "
   "measure.",
   "Look up the pipeline depth of your own processor and compute the expected "
   "misprediction penalty. Compare with the value you will measure in Module "
   "04.",
 ],
 "selfcheck": [
   "Does pipelining reduce the latency of an instruction? What does it "
   "improve, and by how much ideally?",
   "Name the three hazard classes with a one-line cause for each.",
   "What does forwarding do, and give the specific case it cannot fix.",
   "Why are WAR and WAW called false dependences, and what removes them?",
   "Why did very deep pipelines fall out of favour?",
   "Compute the CPI contribution of a 2% miss rate to 250-cycle memory, with "
   "30% of instructions accessing memory. Compare it with a 5% branch "
   "misprediction rate at 15 cycles.",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Branch Prediction and Speculation",
 "subtitle": "Guessing the future, and the cost of being wrong.",
 "question": "How does a processor keep a deep pipeline full across a branch?",
 "outcomes": [
     "Explain why branch prediction is necessary rather than merely helpful.",
     "Describe static, bimodal, two-level, and modern predictors.",
     "Measure the misprediction penalty on your own machine.",
     "Write branchless code and judge when it is worth it.",
     "Explain speculative execution and its security consequences.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why guess at all",
   "blurb": "The arithmetic makes stalling impossible."},

  {"t": "eq", "kicker": "The arithmetic", "title": "Why you cannot simply stall",
   "eqs": [
     ("~20% of instructions are branches",
      "One in five. Conditionals, loops, calls, returns."),
     ("pipeline depth ~15–20 stages",
      "The branch resolves well after it was fetched."),
     ("stalling every branch  ⇒  CPI ≈ 1 + 0.2×15 = 4",
      "A fourfold slowdown. Completely unacceptable."),
   ],
   "caption": "So the processor guesses, and executes speculatively. "
              "Prediction is not an optimisation — deep pipelines are "
              "impossible without it.",
   "note": "Framing prediction as a precondition rather than a refinement "
           "is the right emphasis."},

  {"t": "bullets", "kicker": "Speculation", "title": "What speculative execution means",
   "items": [
     "Predict the branch outcome; fetch and execute down the predicted path "
     "immediately.",
     "Results are held <b>provisionally</b> — not committed to "
     "architectural state.",
     "",
     "<b>Right:</b> commit everything. Nothing was lost.",
     "<b>Wrong:</b> discard the speculated work and restart from the correct "
     "address.",
     ("Cost is the pipeline depth — everything in flight is thrown "
      "away.", 1),
     "",
     "At 95% accuracy this is overwhelmingly profitable.",
   ]},

  {"t": "section", "label": "Part 2", "title": "How prediction works",
   "blurb": "From one bit to neural-inspired, in four steps."},

  {"t": "table", "kicker": "Predictors", "title": "The evolution",
   "header": ["Predictor", "Mechanism", "Accuracy"],
   "widths": [3.0, 5.4, 3.7],
   "rows": [
     ["Static", "Always taken; or backward-taken, forward-not", "~60–70%"],
     ["1-bit", "Remember the last outcome for this branch", "~80%"],
     ["2-bit bimodal", "Saturating counter — needs two misses to flip", "~85–90%"],
     ["Two-level / gshare", "Index by branch address XOR global history", "~93–96%"],
     ["TAGE / perceptron", "Many history lengths, tagged, combined", "~98–99%"],
   ],
   "note": "The jump from bimodal to two-level is the conceptual one: "
           "correlation between branches is real and exploitable."},

  {"t": "callout", "title": "Why two bits rather than one",
   "kind": "The key refinement",
   "body": ["A 1-bit predictor mispredicts <b>twice</b> per loop: once on the "
            "final iteration (predicts taken, loop exits) and once on the "
            "first iteration of the next execution (now predicts not-taken).",
            "A 2-bit saturating counter requires two consecutive wrong "
            "outcomes before changing its prediction. A single anomalous "
            "outcome — like a loop exit — does not flip it.",
            "For a loop of n iterations, mispredictions drop from 2 per "
            "execution to 1. One extra bit of state, and roughly half the "
            "misses removed. The hysteresis is the whole idea."]},

  {"t": "bullets", "kicker": "Correlation", "title": "Why global history helps",
   "items": [
     "Branches are not independent. Later ones often depend on earlier ones.",
     "",
     "<code>if (x > 0) ... ; if (x > 10) ...</code>",
     ("The second is highly predictable <i>given</i> the first.", 1),
     "",
     "A <b>two-level</b> predictor indexes its table by branch address "
     "<i>combined with recent global outcomes</i>.",
     ("So the same branch gets different predictions in different "
      "contexts.", 1),
     "",
     "<b>gshare:</b> index = PC XOR global history register. Simple, and a "
     "large accuracy gain.",
   ],
   "note": "The correlation insight (Yeh & Patt) is one of the genuinely "
           "clever ideas in the field."},

  {"t": "bullets", "kicker": "Also predicted", "title": "Direction is not the only problem",
   "items": [
     "<b>Direction</b> — taken or not. The main predictor.",
     "<b>Target</b> — where to, for indirect branches. The Branch Target "
     "Buffer caches recent targets.",
     ("Virtual calls and switch statements are indirect, and harder.", 1),
     "<b>Returns</b> — a Return Address Stack, pushed on call and popped "
     "on return.",
     ("Almost perfectly accurate, since calls and returns nest.", 1),
     "",
     "Deep recursion can overflow the RAS, and accuracy collapses.",
   ],
   "footnote": "Virtual dispatch costs most when the target varies "
               "unpredictably — which is exactly when polymorphism is "
               "most useful."},

  {"t": "section", "label": "Part 3", "title": "Measuring and avoiding",
   "blurb": "What you can do about it."},

  {"t": "code", "kicker": "Measure", "title": "The classic experiment",
   "lang": "c", "code": """
// Fill an array with random values, then branch on them.
for (i = 0; i < N; i++) a[i] = rand() % 256;

uint64_t sum = 0;
for (rep = 0; rep < 1000; rep++)
    for (i = 0; i < N; i++)
        if (a[i] >= 128) sum += a[i];     // ~50% taken, UNPREDICTABLE

// Now SORT the array and run the identical loop again.
sort(a, N);
// Same instruction count. Same memory access pattern.
// Typically 3-6x FASTER -- the branch is now almost always
// correctly predicted.
""",
   "caption": "Identical work, identical data, identical memory traffic. The "
              "only difference is predictability. This is the single most "
              "convincing demonstration in the course.",
   "note": "Every student should run this. It makes branch prediction real in "
           "a way no diagram does."},

  {"t": "code", "kicker": "Avoid", "title": "Branchless: pay always, never mispredict",
   "lang": "c", "code": """
// Branchy: 0 or ~15 cycles, depending on prediction
if (a[i] >= 128) sum += a[i];

// Branchless: always ~1-2 cycles, never mispredicts
sum += a[i] * (a[i] >= 128);          // multiply by 0 or 1

// Or with a conditional move (often emitted automatically):
int t = (a[i] >= 128) ? a[i] : 0;
sum += t;
""",
   "caption": "Worth it when the branch is unpredictable. A <i>loss</i> when "
              "the branch predicts well, because you pay the work on every "
              "iteration instead of almost never.",
   "note": "The trade is the point: branchless is not strictly better, it is "
           "a different risk profile."},

  {"t": "table", "kicker": "Judgement", "title": "When to go branchless",
   "header": ["Situation", "Verdict"],
   "widths": [5.6, 6.5],
   "rows": [
     ["Branch is data-dependent and ~50/50", "<b>Yes</b> — the big win"],
     ["Branch is almost always one way", "<b>No</b> — prediction is already free"],
     ["Both sides are cheap", "Probably yes"],
     ["One side is expensive", "No — you would always pay it"],
     ["Inside a hot inner loop", "Measure. Do not guess."],
   ]},

  {"t": "callout", "title": "Spectre: speculation leaks", "kind": "Security",
   "body": ["Mis-speculated instructions are discarded architecturally "
            "— but they ran, and they left data in the cache.",
            "An attacker can induce speculation past a bounds check, cause a "
            "secret-dependent memory access, and then recover the secret by "
            "timing cache accesses. The architectural state was never wrong; "
            "the microarchitectural state carried the information out.",
            "The ISA guaranteed no architectural effect, and that guarantee "
            "held. It said nothing about timing, and timing was enough.",
            "Mitigations cost real performance. This is the Module 02 "
            "abstraction leak, in a form nobody designed for."]},
 ],
 "takeaways": [
   "With 20% branches and a 15-stage pipeline, stalling on every branch gives "
   "CPI 4. Prediction is a precondition for deep pipelines, not an "
   "optimisation.",
   "A 2-bit saturating counter needs two consecutive misses to change its "
   "mind, which halves loop mispredictions compared with 1 bit.",
   "Branches correlate. Two-level predictors index by address combined with "
   "global history, reaching 95%+; TAGE reaches 98–99%.",
   "Direction, target, and return address are predicted by separate "
   "mechanisms. Indirect calls are the hard case.",
   "Sorting an array makes an identical loop 3–6× faster purely by "
   "making one branch predictable.",
   "Branchless code is worth it only when the branch is genuinely "
   "unpredictable and both sides are cheap. Otherwise it is a loss.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why prediction is mandatory"),
  ("p", "Module 03 identified control hazards as the expensive case. The "
        "arithmetic shows why they cannot simply be tolerated."),
  ("ul", ["Roughly one instruction in five is a branch — conditionals, "
          "loop back-edges, calls, returns.",
          "A modern pipeline is 15&ndash;20 stages deep, and a branch is not "
          "resolved until well into it.",
          "Stalling on every branch therefore contributes about 0.2 &times; "
          "15 = 3 to CPI, taking an ideal CPI of 1 to roughly 4."]),
  ("p", "A fourfold slowdown is not acceptable, so processors guess which way "
        "each branch will go and continue executing immediately. Branch "
        "prediction is not a refinement that makes deep pipelines faster; it "
        "is the precondition that makes them possible at all."),
  ("h2", "1.1 &nbsp; Speculative execution"),
  ("p", "Having predicted, the processor fetches and executes down the "
        "predicted path, holding results provisionally rather than committing "
        "them to architectural state. If the prediction proves correct, the "
        "results commit and nothing was lost. If it proves wrong, all "
        "speculated work is discarded and fetching restarts at the correct "
        "address, costing roughly the pipeline depth."),
  ("p", "At 95% accuracy the expected cost per branch is about 0.05 &times; "
        "15 = 0.75 cycles instead of 15 — an overwhelming win, which is "
        "why the technique is universal despite its complexity and, as "
        "&sect;4 discusses, its security cost."),

  ("h1", "2 &nbsp; How predictors work"),
  ("table", ["Predictor", "Mechanism", "Typical accuracy"],
   [["<b>Static</b>", "A fixed rule: always predict taken, or predict "
     "backward branches taken and forward branches not taken (which "
     "approximates loops well).", "60&ndash;70%"],
    ["<b>1-bit dynamic</b>", "One bit per branch recording the last outcome; "
     "predict the same again.", "~80%"],
    ["<b>2-bit bimodal</b>", "A saturating counter per branch; two "
     "consecutive wrong outcomes are needed to change the prediction.",
     "85&ndash;90%"],
    ["<b>Two-level / gshare</b>", "Index a table of counters by the branch "
     "address combined with a global history of recent outcomes, capturing "
     "correlation between branches.", "93&ndash;96%"],
    ["<b>TAGE, perceptron</b>", "Several tables indexed by different history "
     "lengths, tagged to detect which applies, with the longest matching "
     "history winning.", "98&ndash;99%"]],
   [0.20, 0.57, 0.23]),
  ("callout", "The 2-bit counter, and why hysteresis matters",
   ["Consider a loop executing 100 iterations, repeatedly.",
    "A <b>1-bit</b> predictor mispredicts twice per execution: once on the "
    "final iteration (it predicts taken; the loop exits) and once on the "
    "first iteration of the next execution (it has now learned not-taken, but "
    "the loop is taken again).",
    "A <b>2-bit saturating counter</b> requires two consecutive wrong "
    "outcomes to flip. The single loop-exit misprediction moves the counter "
    "but does not change the prediction, so the next execution starts "
    "correctly. One misprediction per execution instead of two.",
    "One extra bit of state halves the misses. The idea — require "
    "corroboration before changing your mind — is simple and recurs "
    "throughout prediction and caching."]),
  ("h2", "2.1 &nbsp; Correlation and two-level prediction"),
  ("p", "Branches are not independent events. Consider:"),
  ("code", """if (x > 0)  { ... }        // branch A
if (x > 10) { ... }        // branch B -- highly correlated with A"""),
  ("p", "If A was not taken, B cannot be taken. A predictor that considers "
        "each branch in isolation cannot exploit this; one that considers "
        "<i>recent global history</i> can."),
  ("p", "A <b>two-level</b> predictor maintains a global history register of "
        "the last k branch outcomes and indexes its counter table by a "
        "combination of the branch address and that history. The same static "
        "branch then receives different predictions in different dynamic "
        "contexts. <b>gshare</b> uses the exclusive-or of the program counter "
        "and the global history as the index — simple to build, and a "
        "substantial accuracy improvement."),
  ("h2", "2.2 &nbsp; Three separate prediction problems"),
  ("table", ["Question", "Mechanism", "Difficulty"],
   [["Taken or not?", "The direction predictor described above.",
     "Largely solved: 98%+ on typical code."],
    ["Taken to <i>where</i>?", "Branch Target Buffer, caching recent targets "
     "by branch address.",
     "Easy for direct branches (the target is encoded). Hard for indirect "
     "branches — virtual calls, function pointers, switch tables — "
     "where the target varies at run time."],
    ["Where does this return go?",
     "Return Address Stack: push on call, pop on return.",
     "Nearly perfect, because calls and returns nest. Deep recursion can "
     "overflow it, at which point accuracy collapses."]],
   [0.22, 0.34, 0.44]),
  ("p", "The practical consequence is that virtual dispatch is cheap when the "
        "target is stable — the BTB predicts it correctly — and "
        "expensive when it genuinely varies, which is precisely the situation "
        "in which polymorphism is doing useful work. This is why devirtualisation "
        "and type-stability matter in hot loops."),

  ("break",),
  ("h1", "3 &nbsp; Measuring and avoiding"),
  ("h2", "3.1 &nbsp; The sorted-array experiment"),
  ("p", "The clearest demonstration of branch prediction's cost requires "
        "changing nothing except predictability."),
  ("code", """for (i = 0; i < N; i++) a[i] = rand() % 256;

// Loop 1: data is random
for (rep = 0; rep < 1000; rep++)
    for (i = 0; i < N; i++)
        if (a[i] >= 128) sum += a[i];

sort(a, N);

// Loop 2: identical code, identical data, now sorted"""),
  ("p", "The two loops execute the same instructions on the same values with "
        "the same memory access pattern. The second is typically three to six "
        "times faster. The only difference is that after sorting, the branch "
        "is not-taken for the first half of the array and taken for the "
        "second, so the predictor is wrong roughly once instead of half the "
        "time."),
  ("p", "Confirm it with <code>perf stat -e branch-misses</code>: the random "
        "version shows a miss rate near 50%, the sorted version near 0%."),
  ("h2", "3.2 &nbsp; Branchless code"),
  ("code", """// Branchy: 0 cycles when predicted, ~15 when not
if (a[i] >= 128) sum += a[i];

// Branchless: always 1-2 cycles, never mispredicts
sum += a[i] * (a[i] >= 128);

// Conditional move -- often generated automatically
int t = (a[i] >= 128) ? a[i] : 0;
sum += t;"""),
  ("callout", "Branchless is a different risk profile, not a strict improvement",
   ["A branch that predicts well is essentially free. Replacing it with "
    "arithmetic means paying a small cost on <i>every</i> iteration instead "
    "of a large cost almost never — which is a net loss.",
    "A branch that is genuinely unpredictable costs the full misprediction "
    "penalty about half the time. Replacing it is a large win.",
    "So the question is never 'is branchless faster?' but 'is this branch "
    "predictable?'. Measure the branch miss rate before deciding, and measure "
    "the result afterwards — compilers also convert branches to "
    "conditional moves on their own, sometimes wrongly."]),
  ("table", ["Situation", "Go branchless?"],
   [["Data-dependent branch, roughly 50/50", "<b>Yes</b> — the clearest win."],
    ["Branch taken 99% of the time", "<b>No</b> — prediction already costs nothing."],
    ["Both sides cheap and side-effect free", "Probably yes."],
    ["One side expensive", "<b>No</b> — you would execute it every time."],
    ["One side has side effects or may fault",
     "<b>No</b> — branchless evaluates both."],
    ["Hot inner loop", "Measure. This is not a case for intuition."]],
   [0.45, 0.55]),

  ("h1", "4 &nbsp; Speculation and security"),
  ("callout", "Spectre",
   ["Speculatively executed instructions are discarded architecturally when "
    "the prediction is wrong. But they <i>ran</i>, and their memory accesses "
    "left lines in the cache.",
    "An attacker trains the predictor so that a bounds check is speculatively "
    "bypassed, causing a read of out-of-bounds memory and then a second "
    "access indexed by the secret value. The architectural result is "
    "discarded; the cache state is not. Timing subsequent accesses reveals "
    "which line was loaded, and hence the secret.",
    "The ISA promised that mis-speculated instructions have no architectural "
    "effect, and that promise was kept. It said nothing about "
    "microarchitectural state or timing, and those were sufficient."]),
  ("p", "This is the abstraction leak of Module 02 in a form nobody designed "
        "for. Mitigations — speculation barriers, indirect branch "
        "restrictions, and various flushes — cost real performance, in "
        "some workloads 5&ndash;30%. The episode is a reminder that an "
        "abstraction which is only approximately true provides a security "
        "guarantee only by accident."),
 ],
 "resources": [
   ("Onur Mutlu — Branch Prediction lectures",
    "https://safari.ethz.ch/architecture/",
    "Static through TAGE, with the correlation insight developed properly."),
   ("Dan Luu — Branch prediction",
    "https://danluu.com/branch-prediction/",
    "A short, clear history of predictor designs with the intuition for each."),
   ("Stack Overflow — 'Why is processing a sorted array faster?'",
    "https://stackoverflow.com/questions/11227809/",
    "The canonical demonstration, with excellent answers. Run it yourself "
    "before reading."),
   ("Spectre Attacks: Exploiting Speculative Execution (free paper)",
    "https://spectreattack.com/spectre.pdf",
    "The original paper. Readable, and worth reading in full for how "
    "carefully the abstraction is picked apart."),
 ],
 "exercises": [
   "Run the sorted-array experiment. Measure both versions and confirm with "
   "<code>perf stat -e branches,branch-misses</code> that the difference is "
   "misprediction and not something else.",
   "Derive your machine's misprediction penalty in cycles: construct a loop "
   "with a perfectly predictable branch and one with a random branch, matched "
   "for instruction count, and solve for the penalty.",
   "Rewrite the branchy loop branchlessly. Measure it on random and on sorted "
   "data, and explain why it wins in one case and loses in the other.",
   "Write a loop whose branch pattern is periodic with period 4 (TNTN...). "
   "Measure the miss rate and explain why a modern predictor handles it "
   "nearly perfectly.",
   "Measure an indirect call through a function pointer that is stable, "
   "versus one that alternates between two targets, versus one chosen at "
   "random from eight. Explain the pattern in terms of the BTB.",
   "Write a deeply recursive function and measure where return prediction "
   "degrades. Relate the depth to the likely Return Address Stack size.",
 ],
 "selfcheck": [
   "Compute the CPI cost of stalling on every branch with 20% branches and a "
   "15-stage pipeline. Why does this make prediction mandatory?",
   "Why does a 2-bit predictor outperform a 1-bit predictor on loops? Be "
   "specific about which mispredictions it removes.",
   "What does global history let a predictor exploit that a per-branch "
   "predictor cannot?",
   "Name the three separate things that must be predicted at a branch, and "
   "which is hardest.",
   "Why is a sorted array faster to process, given identical instructions and "
   "identical memory traffic?",
   "Give two situations where branchless code is a loss.",
   "What exactly did Spectre exploit, and which guarantee was <i>not</i> "
   "violated?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Caches: The Memory Wall",
 "subtitle": "The gap that shapes every modern machine.",
 "question": "Why is memory 250 times slower than the processor, and what is "
             "done about it?",
 "outcomes": [
     "Explain the memory wall and its historical origin.",
     "Explain temporal and spatial locality and why caches work at all.",
     "Analyse direct-mapped, set-associative, and fully associative caches.",
     "Classify misses as compulsory, capacity, or conflict.",
     "Measure your own machine's cache hierarchy.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The wall",
   "blurb": "Two exponential curves with different exponents."},

  {"t": "callout", "title": "The memory wall", "kind": "The organising fact",
   "body": ["From roughly 1980 to 2005, processor speed improved about 50% "
            "per year. DRAM latency improved about 7% per year.",
            "Compounded over twenty-five years, the gap grew by more than two "
            "orders of magnitude. An access that once cost a few cycles now "
            "costs two to three hundred.",
            "DRAM <i>bandwidth</i> has improved far more than latency — "
            "you can get a great deal of data, but the first byte still takes "
            "a long time to arrive.",
            "Essentially every architectural mechanism from here on exists to "
            "avoid that latency or to find other work to do during it."]},

  {"t": "table", "kicker": "Hierarchy", "title": "A typical modern hierarchy",
   "header": ["Level", "Size", "Latency", "Notes"],
   "widths": [2.6, 2.8, 2.6, 4.1],
   "rows": [
     ["Registers", "~1 KB", "0", "Named by the ISA"],
     ["L1 data", "32–48 KB", "~4 cyc", "Per core; split from L1 instruction"],
     ["L2", "0.5–2 MB", "~12 cyc", "Per core, usually"],
     ["L3", "8–64 MB", "~40 cyc", "Shared across cores"],
     ["DRAM", "8–128 GB", "~250 cyc", "Shared, and far away"],
     ["SSD", "0.5–4 TB", "~10⁵ cyc", "A different world"],
   ],
   "note": "Each level is roughly 10x bigger and 3-5x slower than the one "
           "above. That geometric structure is not an accident."},

  {"t": "bullets", "kicker": "Why it works", "title": "Locality is the whole justification",
   "items": [
     "A cache only helps if future accesses are predictable from past ones. "
     "Real programs oblige.",
     "",
     "<b>Temporal locality</b> — a recently used item is likely to be "
     "used again.",
     ("Loop variables, hot functions, frequently traversed structures.", 1),
     "",
     "<b>Spatial locality</b> — items near a used item are likely to be "
     "used soon.",
     ("Array traversal, struct fields, sequential instruction fetch.", 1),
     "",
     "Caches exploit temporal locality by <b>keeping</b> and spatial locality "
     "by <b>fetching a whole line</b>.",
   ],
   "note": "Spatial locality is why the cache line exists, and the line is "
           "the unit everything else is measured in."},

  {"t": "section", "label": "Part 2", "title": "Organisation",
   "blurb": "Where can a line live, and how do you find it?"},

  {"t": "table", "kicker": "Placement", "title": "Three placement policies",
   "header": ["Policy", "A line may live", "Lookup", "Problem"],
   "widths": [2.8, 3.4, 2.8, 3.1],
   "rows": [
     ["Direct-mapped", "In exactly one set", "One tag compare", "Conflict misses"],
     ["N-way set associative", "In any of N ways of one set", "N compares", "Cost of N"],
     ["Fully associative", "Anywhere", "Compare all", "Impractical above tiny sizes"],
   ],
   "note": "8-way is the common compromise for L1. The TLB is often fully "
           "associative because it is small."},

  {"t": "code", "kicker": "Addressing", "title": "How an address is split",
   "lang": "text", "code": """
 63                        12 11        6 5        0
+-----------------------------+-----------+----------+
|            TAG              |   INDEX   |  OFFSET  |
+-----------------------------+-----------+----------+

OFFSET  which byte within the cache line      (64B line -> 6 bits)
INDEX   which set to look in                  (64 sets  -> 6 bits)
TAG     compared against stored tags to confirm a hit

A 32 KB, 8-way, 64-byte-line cache:
    32768 / 64 = 512 lines
    512 / 8 ways = 64 sets  -> 6 index bits

NOTE: the index comes from the MIDDLE bits, not the top.
Sequential addresses therefore spread across sets rather than
all landing in one -- which is the point.
""",
   "caption": "The middle-bit indexing is deliberate. Using the top bits "
              "would map an entire contiguous array to a single set.",
   "note": "Students rarely ask why the index is in the middle. Telling them "
           "makes the conflict-miss discussion land."},

  {"t": "section", "label": "Part 3", "title": "Misses",
   "blurb": "Three causes, and a different fix for each."},

  {"t": "table", "kicker": "The three Cs", "title": "Classify before you optimise",
   "header": ["Miss type", "Cause", "Fix"],
   "widths": [2.6, 4.6, 4.9],
   "rows": [
     ["Compulsory", "First ever reference to this line",
      "Prefetching; larger lines"],
     ["Capacity", "Working set exceeds the cache",
      "Blocking/tiling; shrink the data"],
     ["Conflict", "Too many lines map to one set",
      "Padding; change the stride; more associativity"],
   ],
   "note": "Conflict misses are the surprising ones: plenty of free cache, "
           "and still missing. Always suspect a power-of-two stride."},

  {"t": "callout", "title": "Why power-of-two strides are dangerous",
   "kind": "The classic trap",
   "body": ["The set index comes from middle address bits. A stride that is a "
            "large power of two leaves those bits unchanged, so every access "
            "lands in the <b>same set</b>.",
            "Walking a column of a 1024×1024 float matrix strides by "
            "4096 bytes. With 64 sets of 64-byte lines, every element maps to "
            "the same set. An 8-way cache holds 8 of them; the ninth evicts "
            "the first.",
            "You now miss on every access while using 8 lines out of 512. "
            "The cache is 98% empty and useless.",
            "<b>Fix:</b> pad the row length to a non-power-of-two — "
            "1024 → 1032 floats. A few kilobytes of waste for a large "
            "speedup."]},

  {"t": "code", "kicker": "Measure", "title": "Finding your cache sizes by pointer chase",
   "lang": "c", "code": """
// Build a pointer chain within a working set of `size` bytes,
// in RANDOM order so the prefetcher cannot help.
// Then time a long traversal.

for (size = 4*KB; size <= 256*MB; size *= 2) {
    build_random_chain(buf, size);
    t = time_chase(buf, ITERATIONS);
    printf("%8zu KB   %6.1f cycles/access\\n", size/1024, t);
}

// Output shows PLATEAUS with sharp steps between them:
//     32 KB      4.2     <- fits in L1
//     64 KB     12.1     <- spilled to L2
//    512 KB     13.0
//      2 MB     41.5     <- spilled to L3
//     32 MB    198.0     <- spilled to DRAM
//
// Each step marks a cache capacity. You just measured the
// hierarchy without reading a datasheet.
""",
   "caption": "Random order is essential — a sequential chase is "
              "perfectly prefetched and shows no steps at all.",
   "note": "This is Project 1's core experiment and the most satisfying "
           "measurement in the course."},

  {"t": "bullets", "kicker": "Policy", "title": "Replacement and writes",
   "items": [
     "<b>Replacement:</b> LRU is the ideal; true LRU is expensive above 2-way.",
     ("Real caches use pseudo-LRU, or tree-LRU, or random for high "
      "associativity.", 1),
     "",
     "<b>Write-through</b> — write to cache and memory together. Simple; "
     "high bandwidth.",
     "<b>Write-back</b> — write to cache, mark dirty, write out on "
     "eviction. Standard.",
     "",
     "<b>Write-allocate</b> — a write miss fetches the line first.",
     ("Which is why writing a large array you never read still consumes read "
      "bandwidth — unless you use non-temporal stores.", 1),
   ],
   "footnote": "Non-temporal stores bypass the cache. Useful for streaming "
               "output you will not re-read."},
 ],
 "takeaways": [
   "Processors improved ~50% per year and DRAM latency ~7%. The resulting "
   "memory wall shapes every modern design.",
   "Caches work only because of temporal and spatial locality. Keeping "
   "exploits the first; fetching a whole line exploits the second.",
   "The set index comes from middle address bits, so sequential data spreads "
   "across sets — and power-of-two strides collapse onto one.",
   "Three Cs: compulsory, capacity, conflict. Classify before optimising, "
   "because each has a different fix.",
   "A power-of-two row length in a 2D array can make a cache 98% useless. "
   "Padding fixes it for a few kilobytes.",
   "A random pointer chase across working-set sizes reveals your entire cache "
   "hierarchy as plateaus with sharp steps.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The memory wall"),
  ("p", "Between roughly 1980 and 2005, processor performance improved at "
        "about 50% per year while DRAM <i>latency</i> improved at about 7% "
        "per year. Two exponentials with different exponents diverge, and "
        "over twenty-five years this one diverged by more than two orders of "
        "magnitude."),
  ("p", "The result is the defining constraint of modern architecture: a "
        "processor capable of several operations per cycle, attached to a "
        "memory that takes two to three hundred cycles to answer. Note that "
        "DRAM <i>bandwidth</i> has improved much faster than latency — "
        "you can obtain a great deal of data per second, but the first byte "
        "is still slow to arrive. That asymmetry is why prefetching (Module "
        "06) is so valuable: it converts a latency problem into a bandwidth "
        "problem."),
  ("table", ["Level", "Typical size", "Latency", "Notes"],
   [["Registers", "~1 KB", "0 cycles", "Named directly by the ISA."],
    ["L1 data cache", "32&ndash;48 KB", "~4 cycles",
     "Per core, split from the L1 instruction cache."],
    ["L2 cache", "0.5&ndash;2 MB", "~12 cycles", "Usually per core."],
    ["L3 cache", "8&ndash;64 MB", "~40 cycles", "Shared between cores."],
    ["DRAM", "8&ndash;128 GB", "~250 cycles", "Shared, and physically far."],
    ["SSD", "0.5&ndash;4 TB", "~10&#8309; cycles", "A different regime."]],
   [0.20, 0.20, 0.17, 0.43]),
  ("p", "Each level is roughly ten times larger and three to five times "
        "slower than the one above it. That geometric structure is a "
        "deliberate design: it gives an average access time close to the "
        "fastest level while providing capacity close to the largest."),

  ("h1", "2 &nbsp; Why caching works at all"),
  ("p", "A cache is a bet that future accesses resemble past ones. The bet "
        "pays because real programs exhibit two forms of locality."),
  ("ul", ["<b>Temporal locality.</b> An item used recently is likely to be "
          "used again soon. Loop counters, hot function code, frequently "
          "traversed structures.",
          "<b>Spatial locality.</b> Items near a recently used item are "
          "likely to be used soon. Array traversal, struct fields accessed "
          "together, sequential instruction fetch."]),
  ("p", "Caches exploit temporal locality by <i>retaining</i> data, and "
        "spatial locality by fetching an entire <b>cache line</b> — "
        "typically 64 bytes — rather than a single word. The line is the "
        "unit of transfer, the unit of coherence (Module 11), and the unit in "
        "which you should think about data layout."),
  ("callout", "The consequence for data layout",
   ["Touching one byte brings in 64. If you use all 64, the fetch cost is "
    "amortised over 64 bytes of useful work. If you use 4 and skip the rest, "
    "you have wasted 94% of the bandwidth you paid for.",
    "This single observation justifies struct-of-arrays layouts, hot/cold "
    "field splitting, and most of Module 06."]),

  ("h1", "3 &nbsp; Cache organisation"),
  ("h2", "3.1 &nbsp; Address breakdown"),
  ("code", """ 63                        12 11        6 5        0
+-----------------------------+-----------+----------+
|            TAG              |   INDEX   |  OFFSET  |
+-----------------------------+-----------+----------+

OFFSET : byte within the line        (64B line  -> 6 bits)
INDEX  : which set to search         (64 sets   -> 6 bits)
TAG    : compared with stored tags to confirm a hit"""),
  ("p", "For a 32 KB, 8-way set-associative cache with 64-byte lines: "
        "32768/64 = 512 lines, divided into 512/8 = 64 sets, requiring 6 "
        "index bits."),
  ("callout", "Why the index comes from the middle",
   ["If the index were taken from the high-order bits, an entire contiguous "
    "array would map to a single set and the cache would be useless for "
    "exactly the access pattern it most needs to serve.",
    "Taking it from the middle means consecutive lines map to consecutive "
    "sets, so sequential data spreads evenly across the whole cache.",
    "The price is that addresses separated by (number of sets &times; line "
    "size) collide — which is the mechanism behind conflict misses, and "
    "the reason power-of-two strides are dangerous."]),
  ("h2", "3.2 &nbsp; Associativity"),
  ("table", ["Policy", "Placement", "Lookup cost", "Trade-off"],
   [["Direct-mapped", "Exactly one possible location", "One tag comparison",
     "Fastest and simplest; badly vulnerable to conflict misses."],
    ["N-way set associative", "Any of N ways within one set",
     "N comparisons in parallel",
     "The standard compromise. 8-way is typical for L1, 16-way for L3."],
    ["Fully associative", "Anywhere in the cache", "Compare every tag",
     "No conflict misses at all, but the comparison hardware limits this to "
     "very small caches — TLBs and victim caches."]],
   [0.20, 0.25, 0.22, 0.33]),

  ("break",),
  ("h1", "4 &nbsp; The three Cs"),
  ("table", ["Miss type", "Cause", "What helps"],
   [["<b>Compulsory</b>", "The first reference to a line — it could not "
     "possibly have been cached.",
     "Prefetching (Module 06); larger lines if spatial locality is good."],
    ["<b>Capacity</b>", "The working set is larger than the cache, so lines "
     "are evicted before reuse.",
     "Blocking or tiling to shrink the active working set; reduce the data "
     "itself."],
    ["<b>Conflict</b>", "Too many active lines map to the same set, so they "
     "evict each other despite free capacity elsewhere.",
     "Padding to change the stride; higher associativity; reorganising the "
     "access pattern."]],
   [0.17, 0.42, 0.41]),
  ("p", "Classifying a miss before trying to fix it saves a great deal of "
        "wasted effort, because the three have entirely different remedies. "
        "Conflict misses in particular are counterintuitive: the cache has "
        "ample free space and is still missing on every access."),
  ("h2", "4.1 &nbsp; The power-of-two stride trap"),
  ("p", "Consider traversing a column of a 1024 &times; 1024 array of "
        "4-byte floats. Successive elements are 4096 bytes apart."),
  ("p", "With 64-byte lines and 64 sets, the set index repeats every "
        "64 &times; 64 = 4096 bytes. Every element of the column therefore "
        "maps to the <i>same set</i>. An 8-way cache can hold eight of them; "
        "the ninth evicts the first, and by the time the traversal wraps "
        "around, nothing useful remains."),
  ("callout", "The cache is 98% empty and completely ineffective",
   ["You are using 8 lines out of 512 and missing on every single access, "
    "while the rest of the cache sits idle.",
    "<b>The fix is padding.</b> Allocate rows of 1032 floats instead of 1024 "
    "and use only the first 1024. The stride is no longer a power of two, "
    "successive column elements map to different sets, and the cache works as "
    "intended.",
    "The cost is about 0.8% extra memory for what can be a several-fold "
    "speedup. Any time a 2D array has a power-of-two row length and column "
    "access is slow, suspect this first."]),

  ("h1", "5 &nbsp; Measuring your own hierarchy"),
  ("p", "You can determine every cache size on your machine without consulting "
        "documentation, which is Project 1's central experiment."),
  ("code", """// Build a cyclic pointer chain through a buffer of `size` bytes,
// visiting lines in RANDOM order, then time a long traversal.
for (size = 4*KB; size <= 256*MB; size *= 2) {
    build_random_chain(buf, size);
    printf("%8zu KB  %6.1f cycles/access\\n",
           size/1024, time_chase(buf, ITERS));
}"""),
  ("p", "The output shows plateaus separated by sharp steps. Each plateau is "
        "a cache level, and each step marks the point where the working set "
        "exceeded that level's capacity:"),
  ("table", ["Working set", "Cycles per access", "Interpretation"],
   [["32 KB", "~4", "Fits in L1."],
    ["64 KB&ndash;512 KB", "~12", "Spilled to L2."],
    ["2 MB&ndash;16 MB", "~40", "Spilled to L3."],
    ["32 MB+", "~200", "Spilled to DRAM."]],
   [0.26, 0.26, 0.48]),
  ("callout", "Randomise the chain, or you will measure nothing",
   ["A sequential pointer chase is perfectly predicted by the hardware "
    "prefetcher, which fetches lines before they are requested. The latency "
    "is hidden entirely and the curve is flat at every size — you learn "
    "nothing about capacity.",
    "Randomising the order defeats the prefetcher, exposes the true latency "
    "of each level, and makes the steps appear. The fact that the sequential "
    "version is flat is itself the most convincing demonstration of what "
    "prefetching does, which is Module 06."]),

  ("h1", "6 &nbsp; Replacement and write policy"),
  ("ul", ["<b>Replacement.</b> LRU is close to optimal in practice but "
          "expensive to implement exactly above 2-way associativity. Real "
          "caches use pseudo-LRU approximations, tree-based schemes, or "
          "even random replacement at high associativity, where the "
          "difference is small.",
          "<b>Write-through</b> propagates every write to the next level "
          "immediately. Simple and keeps levels consistent, at the cost of "
          "substantial write bandwidth.",
          "<b>Write-back</b> writes only to the cache, marks the line dirty, "
          "and writes it out when evicted. Far less traffic, and the standard "
          "choice.",
          "<b>Write-allocate</b> fetches a line on a write miss before "
          "modifying it."]),
  ("callout", "Write-allocate has a cost people miss",
   ["Writing a large array you will never read still consumes <i>read</i> "
    "bandwidth, because every write miss first fetches the line it is about "
    "to overwrite completely.",
    "For streaming writes — clearing a buffer, writing output you will "
    "not revisit — <b>non-temporal stores</b> bypass the cache and skip "
    "the fetch, roughly halving memory traffic. They also avoid evicting "
    "useful data, which is often the larger benefit."]),
 ],
 "resources": [
   ("Ulrich Drepper — What Every Programmer Should Know About Memory",
    "https://people.freebsd.org/~lstewart/articles/cpumemory.pdf",
    "Sections 2–3 cover this module in far greater depth. The single "
    "most valuable free document on the subject."),
   ("Onur Mutlu — Memory Hierarchy and Caches lectures",
    "https://safari.ethz.ch/architecture/",
    "Organisation, the three Cs, and replacement policies."),
   ("MIT 6.004 — The Memory Hierarchy",
    "https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/",
    "A clean introduction to associativity and address breakdown."),
   ("Igor Ostrovsky — Gallery of Processor Cache Effects",
    "http://igoro.com/archive/gallery-of-processor-cache-effects/",
    "Nine short experiments, each isolating one cache behaviour. Run all of "
    "them — it takes an afternoon and is worth a week of reading."),
 ],
 "exercises": [
   "Implement the random pointer chase and plot cycles per access against "
   "working-set size on log axes. Identify L1, L2, L3, and DRAM, and compare "
   "with your processor's specification.",
   "Repeat with a <i>sequential</i> chain. Explain why the curve is nearly "
   "flat, and what that tells you about prefetching.",
   "Determine your cache line size: access an array with strides of 1, 2, 4, "
   "&hellip;, 256 bytes and find the stride beyond which time per access stops "
   "increasing.",
   "Determine associativity: access N addresses all mapping to the same set "
   "and find the N at which the time per access jumps.",
   "Reproduce the power-of-two stride trap: traverse the columns of a "
   "1024&times;1024 float matrix, then pad the row length to 1032 and repeat. "
   "Report the speedup and the cache-miss counts for both.",
   "Compare writing a 1 GB buffer with ordinary stores and with non-temporal "
   "stores. Measure total memory traffic for each and explain the difference.",
 ],
 "selfcheck": [
   "What is the memory wall, and what two divergent rates produced it?",
   "Define temporal and spatial locality, and say which cache mechanism "
   "exploits each.",
   "Why is the set index taken from the middle bits of an address rather than "
   "the top?",
   "Name the three Cs and give a distinct fix for each.",
   "Explain precisely why a 1024-float row length makes column traversal "
   "catastrophically slow, and why 1032 fixes it.",
   "Why must a pointer chase be randomised to measure cache capacity?",
   "Why does writing an array you never read still consume read bandwidth?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Cache Optimization and Prefetching",
 "subtitle": "Restructuring code and data so the hierarchy works for you.",
 "question": "How do you get a 10× speedup without changing the "
             "algorithm?",
 "outcomes": [
     "Apply loop interchange, blocking, and fusion for locality.",
     "Choose between array-of-structs and struct-of-arrays.",
     "Explain hardware prefetching and what defeats it.",
     "Use software prefetch intrinsics and know when not to.",
     "Predict a transformation's benefit before measuring it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Loop transformations",
   "blurb": "Same operations, different order, very different speed."},

  {"t": "code", "kicker": "Interchange", "title": "Loop order decides everything",
   "lang": "c", "code": """
// BAD: strides by N*sizeof(float) -- one useful float per 64B line
for (j = 0; j < N; j++)
    for (i = 0; i < N; i++)
        sum += a[i][j];

// GOOD: strides by 4 bytes -- 16 useful floats per line
for (i = 0; i < N; i++)
    for (j = 0; j < N; j++)
        sum += a[i][j];

// Identical arithmetic. Identical result. Typically 5-10x faster.
""",
   "caption": "The bad version fetches a 64-byte line and uses 4 bytes of it. "
              "16× the memory traffic for the same work.",
   "note": "Have them predict the ratio from line size before measuring. The "
           "prediction is usually close, which builds confidence in the "
           "model."},

  {"t": "code", "kicker": "Blocking", "title": "Tiling for the cache",
   "lang": "c", "code": """
// Naive matrix multiply: B is traversed column-wise N times.
for (i...) for (j...) for (k...) c[i][j] += a[i][k] * b[k][j];

// Blocked: work on tiles small enough to stay resident.
for (ii = 0; ii < N; ii += B)
 for (jj = 0; jj < N; jj += B)
  for (kk = 0; kk < N; kk += B)
   for (i = ii; i < ii+B; i++)
    for (j = jj; j < jj+B; j++) {
      float s = c[i][j];
      for (k = kk; k < kk+B; k++) s += a[i][k] * b[k][j];
      c[i][j] = s;
    }

// Choose B so that three B x B tiles fit in L1:
//    3 * B^2 * 4 bytes < 32 KB  ->  B ~ 50, so B = 32 or 48.
""",
   "caption": "Each tile is loaded once and reused B times. Misses drop by "
              "roughly a factor of B.",
   "note": "The sizing calculation is the point: blocking is not magic, it is "
           "arithmetic against a known cache size."},

  {"t": "table", "kicker": "Transformations", "title": "The standard set",
   "header": ["Transformation", "Does", "Helps when"],
   "widths": [2.9, 4.6, 4.6],
   "rows": [
     ["Interchange", "Reorder nested loops", "Access stride is wrong"],
     ["Blocking / tiling", "Work on sub-blocks", "Working set exceeds cache"],
     ["Fusion", "Merge loops over the same data", "Data re-read between loops"],
     ["Fission", "Split one loop into several", "Too many streams at once"],
     ["Unrolling", "Fewer iterations, bigger body", "Loop overhead dominates"],
   ],
   "note": "Fusion and fission oppose each other. Which one helps depends on "
           "whether you are limited by reuse or by stream count."},

  {"t": "section", "label": "Part 2", "title": "Data layout",
   "blurb": "Often a larger win than any loop transformation."},

  {"t": "code", "kicker": "AoS vs SoA", "title": "The layout decision",
   "lang": "c", "code": """
// ARRAY OF STRUCTS -- natural, and often wrong for bulk processing
struct Particle { float x,y,z, vx,vy,vz; int id; float mass; };
Particle p[N];                           // 32 bytes each

for (i...) p[i].x += p[i].vx * dt;       // uses 8 of every 32 bytes
                                         // -> 75% of fetched data wasted

// STRUCT OF ARRAYS -- awkward, and what the hardware wants
struct Particles {
    float x[N], y[N], z[N], vx[N], vy[N], vz[N];
};
for (i...) P.x[i] += P.vx[i] * dt;       // two dense streams
                                         // -> every byte used, and it
                                         //    vectorises cleanly
""",
   "caption": "AoS is better when you touch most fields of one object. SoA is "
              "better when you touch one field of many objects — which "
              "is what bulk processing does.",
   "note": "This is the single most valuable slide for a graphics student. "
           "Particle systems, vertex data, and ECS designs all turn on it."},

  {"t": "bullets", "kicker": "Layout", "title": "Other layout wins",
   "items": [
     "<b>Hot/cold splitting.</b> Separate frequently accessed fields from "
     "rarely accessed ones.",
     ("More hot objects per cache line.", 1),
     "",
     "<b>Alignment.</b> Align hot structures to 64 bytes so they do not "
     "straddle two lines.",
     "",
     "<b>Shrink the data.</b> float instead of double; 16-bit indices; "
     "quantised normals.",
     ("Half the bytes is often close to half the time when memory-bound.", 1),
     "",
     "<b>Avoid pointer chasing.</b> Flat arrays with indices beat node graphs "
     "(Module 02).",
   ]},

  {"t": "section", "label": "Part 3", "title": "Prefetching",
   "blurb": "Fetching before you ask — and what stops it."},

  {"t": "bullets", "kicker": "Hardware", "title": "What the prefetcher does for free",
   "items": [
     "Hardware detects access patterns and fetches ahead automatically.",
     "",
     "<b>Detected easily:</b> sequential forward, sequential backward, "
     "constant stride.",
     "<b>Not detected:</b> random access, pointer chasing, indirect "
     "<code>a[b[i]]</code>.",
     "",
     "A stream that is prefetched well turns a latency problem into a "
     "<b>bandwidth</b> problem — and bandwidth is plentiful.",
     "",
     "<b>Prefetchers stop at page boundaries</b> — they cannot risk "
     "faulting on an unmapped page.",
     ("Which is one argument for huge pages (Module 07).", 1),
   ],
   "note": "The latency-to-bandwidth conversion is the key framing, and it "
           "explains why sequential access is so much faster than its "
           "latency numbers suggest."},

  {"t": "code", "kicker": "Software", "title": "Explicit prefetch, used sparingly",
   "lang": "c", "code": """
for (i = 0; i < N; i++) {
    // Ask for data ~8 iterations ahead. The distance must be tuned:
    // too short and it has not arrived; too long and it is evicted
    // before use.
    __builtin_prefetch(&data[index[i + 8]], 0, 1);

    process(data[index[i]]);      // indirect: hardware CANNOT predict this
}
""",
   "caption": "Worth trying for indirect access, graph traversal, and hash "
              "probing. Almost never worth it for sequential access — "
              "the hardware already does it better.",
   "note": "Emphasise 'measure': software prefetch frequently makes things "
           "slower by adding instructions and polluting the cache."},

  {"t": "table", "kicker": "Method", "title": "An optimisation checklist, in order",
   "header": ["Step", "Ask", "Tool"],
   "widths": [1.6, 5.6, 4.9],
   "rows": [
     ["1", "Is it actually memory-bound?", "IPC and cache-miss counters"],
     ["2", "Which level is missing?", "L1/L2/LLC miss counters"],
     ["3", "Which of the three Cs?", "Vary size and stride"],
     ["4", "Fix layout first", "AoS→SoA, hot/cold, shrink"],
     ["5", "Then loop structure", "Interchange, block, fuse"],
     ["6", "Then prefetch", "Only for indirect patterns"],
   ],
   "footnote": "Layout before loops. A layout change often removes the need "
               "for the loop transformation entirely.",
   "note": "The ordering matters and is frequently got backwards — "
           "people tile first and then discover SoA would have sufficed."},
 ],
 "takeaways": [
   "Loop interchange can give 5–10× with identical arithmetic, "
   "because the wrong stride wastes 15 of every 16 bytes fetched.",
   "Blocking sizes the working set to the cache. Compute the tile size from "
   "the cache capacity; do not guess.",
   "AoS is right when you touch most fields of one object; SoA when you touch "
   "one field of many. Bulk processing wants SoA.",
   "Hardware prefetchers handle sequential and constant-stride access, and "
   "fail on random, pointer-chasing, and indirect patterns.",
   "Good prefetching converts a latency problem into a bandwidth problem, and "
   "bandwidth is the plentiful resource.",
   "Optimise in order: confirm memory-bound, classify the miss, fix layout, "
   "then loops, then prefetch.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Loop transformations"),
  ("h2", "1.1 &nbsp; Interchange"),
  ("p", "C stores arrays in row-major order, so <code>a[i][j]</code> and "
        "<code>a[i][j+1]</code> are adjacent in memory while "
        "<code>a[i][j]</code> and <code>a[i+1][j]</code> are N elements "
        "apart."),
  ("code", """// Column-major traversal: stride N*4 bytes
for (j = 0; j < N; j++)
    for (i = 0; i < N; i++)
        sum += a[i][j];

// Row-major traversal: stride 4 bytes
for (i = 0; i < N; i++)
    for (j = 0; j < N; j++)
        sum += a[i][j];"""),
  ("p", "Both perform exactly the same N&#178; additions and produce the same "
        "result. The first fetches a 64-byte line and uses 4 bytes of it "
        "before moving on; the second uses all 64. That is sixteen times the "
        "memory traffic for identical work, and the measured difference is "
        "typically 5&ndash;10&times; (less than 16 because bandwidth, not "
        "latency, becomes the limit)."),
  ("callout", "Predict before you measure",
   ["With a 64-byte line and 4-byte floats, the bad version uses 1/16 of each "
    "line, so you should expect roughly an order of magnitude.",
    "Making the prediction before running the benchmark is the habit this "
    "course is trying to build. When the prediction is right, your model of "
    "the machine is working; when it is wrong, you have learned something "
    "specific."]),
  ("h2", "1.2 &nbsp; Blocking"),
  ("p", "Naive matrix multiplication traverses B column-wise, once for every "
        "row of A. For large N, B has been entirely evicted between passes, "
        "so nothing is reused."),
  ("p", "<b>Blocking</b> (or tiling) restructures the computation to operate "
        "on sub-blocks small enough to remain resident while they are being "
        "reused."),
  ("code", """for (ii = 0; ii < N; ii += B)
 for (jj = 0; jj < N; jj += B)
  for (kk = 0; kk < N; kk += B)
   for (i = ii; i < ii+B; i++)
    for (j = jj; j < jj+B; j++) {
      float s = c[i][j];
      for (k = kk; k < kk+B; k++)
          s += a[i][k] * b[k][j];
      c[i][j] = s;
    }"""),
  ("p", "<b>Choosing B.</b> Three B&times;B tiles must fit in L1 "
        "simultaneously, so 3B&#178; &times; 4 bytes &lt; 32 KB, giving "
        "B &asymp; 52. In practice B = 32 or 48 works well, leaving room for "
        "other data. Each tile element is now loaded once and used B times, "
        "cutting misses by roughly a factor of B. On large matrices this is "
        "commonly a 3&ndash;5&times; speedup with no change to the "
        "arithmetic."),
  ("table", ["Transformation", "What it does", "Use when"],
   [["<b>Interchange</b>", "Reorders nested loops.",
     "The innermost loop has the wrong stride."],
    ["<b>Blocking / tiling</b>", "Operates on sub-blocks.",
     "The working set exceeds a cache level and there is reuse to capture."],
    ["<b>Fusion</b>", "Merges two loops over the same data.",
     "Data would otherwise be read, evicted, and read again."],
    ["<b>Fission</b>", "Splits one loop into several.",
     "The body touches too many independent streams for the prefetcher or the "
     "cache to track."],
    ["<b>Unrolling</b>", "Fewer iterations with a larger body.",
     "Loop overhead is significant, or you need to break a dependency chain "
     "(Module 03)."]],
   [0.20, 0.33, 0.47]),
  ("p", "Fusion and fission pull in opposite directions, which is a good "
        "reminder that these are not rules but responses to a measured "
        "diagnosis."),

  ("break",),
  ("h1", "2 &nbsp; Data layout"),
  ("p", "Layout changes are frequently larger wins than loop transformations, "
        "and should be considered first."),
  ("h2", "2.1 &nbsp; Array of structs versus struct of arrays"),
  ("code", """// Array of structs -- natural object-oriented layout
struct Particle { float x,y,z, vx,vy,vz; int id; float mass; };  // 32B
Particle p[N];

for (i...) p[i].x += p[i].vx * dt;    // touches 8 of every 32 bytes

// Struct of arrays -- what the hardware wants for bulk work
struct Particles { float x[N], y[N], z[N], vx[N], vy[N], vz[N]; };

for (i...) P.x[i] += P.vx[i] * dt;    // two dense sequential streams"""),
  ("table", ["", "Array of structs", "Struct of arrays"],
   [["Best when", "You touch most fields of one object at a time.",
     "You touch one or two fields across many objects."],
    ["Cache efficiency", "Poor for bulk processing — fetches fields you "
     "will not use.",
     "Excellent — every byte fetched is used."],
    ["Vectorisation", "Difficult: values are strided.",
     "Natural: consecutive values are contiguous (Module 09)."],
    ["Ergonomics", "Natural and readable.",
     "Awkward; often wrapped in an accessor layer."]],
   [0.17, 0.42, 0.41]),
  ("callout", "This is why entity-component systems exist",
   ["Game engines process thousands of objects by applying one operation to "
    "one field across all of them — integrate positions, cull bounds, "
    "update transforms. That is exactly the SoA access pattern.",
    "ECS architectures are, at the data level, an organised way of getting "
    "struct-of-arrays layout while retaining a usable programming model. The "
    "performance argument is this cache argument, and nothing more "
    "mysterious.",
    "The same reasoning governs vertex buffer layout in CSCE 641: interleaved "
    "attributes when the shader uses all of them, separate streams when "
    "different passes use different subsets."]),
  ("h2", "2.2 &nbsp; Other layout techniques"),
  ("ul", ["<b>Hot/cold splitting.</b> Move rarely accessed fields into a "
          "separate structure referenced by pointer. More hot objects fit per "
          "cache line.",
          "<b>Alignment.</b> Align frequently accessed structures to 64 bytes "
          "so a single object does not straddle two cache lines and cost two "
          "fetches.",
          "<b>Shrink the data.</b> <code>float</code> rather than "
          "<code>double</code>, 16-bit indices, quantised normals and "
          "colours. When memory-bound, halving the bytes often nearly halves "
          "the time — and this is usually easier than any loop "
          "transformation.",
          "<b>Replace pointers with indices.</b> A flat array indexed by "
          "32-bit integers is smaller than one of 64-bit pointers and, more "
          "importantly, avoids the serialised dependent loads of Module 02."]),

  ("h1", "3 &nbsp; Prefetching"),
  ("p", "Memory latency can be hidden entirely if the data is requested "
        "before it is needed. Processors attempt this automatically."),
  ("h2", "3.1 &nbsp; Hardware prefetchers"),
  ("table", ["Pattern", "Prefetched?", "Why"],
   [["Sequential forward or backward", "<b>Yes</b>",
     "Trivially detected; the common case."],
    ["Constant stride", "<b>Yes</b>",
     "Stride detectors handle regular strides well."],
    ["Multiple interleaved streams", "<b>Usually</b>",
     "Modern prefetchers track several streams at once, but there is a limit."],
    ["Random access", "<b>No</b>", "Nothing to detect."],
    ["Pointer chasing", "<b>No</b>",
     "The next address is unknown until the current load returns."],
    ["Indirect, <code>a[b[i]]</code>", "<b>No</b>",
     "The address depends on loaded data."]],
   [0.28, 0.17, 0.55]),
  ("callout", "What successful prefetching actually achieves",
   ["It converts a <b>latency</b> problem into a <b>bandwidth</b> problem.",
    "Instead of waiting 250 cycles for each line in turn, many requests are "
    "in flight simultaneously and the limit becomes how fast the memory "
    "system can deliver bytes — which is comparatively generous.",
    "This is why sequential access is vastly faster than the latency table "
    "alone would suggest, and why the random pointer chase of Module 05 had "
    "to be randomised to measure latency at all.",
    "Prefetchers stop at page boundaries, since prefetching into an unmapped "
    "page risks a spurious fault. This is one of the arguments for huge pages "
    "in Module 07."]),
  ("h2", "3.2 &nbsp; Software prefetch"),
  ("code", """for (i = 0; i < N; i++) {
    __builtin_prefetch(&data[index[i + DISTANCE]], 0, 1);
    process(data[index[i]]);     // indirect -- hardware cannot predict
}"""),
  ("p", "Explicit prefetch instructions are worth trying for exactly the "
        "patterns hardware cannot handle: indirect indexing, graph and tree "
        "traversal, hash table probing. The prefetch <i>distance</i> must be "
        "tuned — too short and the line has not arrived; too long and it "
        "is evicted before use — and the right value depends on the "
        "machine and on how much work each iteration does."),
  ("p", "For sequential access, software prefetch almost always makes things "
        "slightly worse: the hardware was already handling it, and you have "
        "added instructions and cache pressure. Measure, always."),

  ("h1", "4 &nbsp; A method"),
  ("table", ["Step", "Question", "How to answer it"],
   [["1", "Is this actually memory-bound?",
     "IPC below ~1 with a high cache-miss rate. If IPC is 3, memory is not "
     "your problem and none of this will help."],
    ["2", "Which level is missing?",
     "L1, L2, and LLC miss counters separately. An L1 miss served by L2 costs "
     "12 cycles; one served by DRAM costs 250."],
    ["3", "Which of the three Cs?",
     "Vary the working-set size (capacity) and the stride (conflict). "
     "Compulsory misses remain when neither changes anything."],
    ["4", "Fix the layout.",
     "AoS&rarr;SoA, hot/cold splitting, smaller types, indices instead of "
     "pointers."],
    ["5", "Then fix the loops.",
     "Interchange, block, fuse or split."],
    ["6", "Then consider prefetching.",
     "Only for patterns hardware cannot detect, and only with measurement."]],
   [0.07, 0.30, 0.63]),
  ("callout", "Layout before loops",
   ["The ordering in that table is deliberate and frequently got backwards. "
    "People reach for tiling first because it feels like the sophisticated "
    "answer.",
    "A layout change often removes the need for any loop transformation at "
    "all, is usually simpler, and compounds with everything else. Try it "
    "first."]),
 ],
 "resources": [
   ("Ulrich Drepper — What Every Programmer Should Know About Memory",
    "https://people.freebsd.org/~lstewart/articles/cpumemory.pdf",
    "Section 6 is a catalogue of exactly these optimisations with measured "
    "results. The core reading for this module."),
   ("Onur Mutlu — Prefetching lectures",
    "https://safari.ethz.ch/architecture/",
    "Hardware prefetcher designs and their limitations."),
   ("Igor Ostrovsky — Gallery of Processor Cache Effects",
    "http://igoro.com/archive/gallery-of-processor-cache-effects/",
    "Nine experiments isolating individual effects. Run every one."),
   ("Mike Acton — Data-Oriented Design and C++ (CppCon, free video)",
    "https://www.youtube.com/watch?v=rX0ItVEVjHc",
    "The practitioner's argument for layout-first thinking, from a game "
    "engine perspective. Directly relevant to CSCE 641."),
 ],
 "exercises": [
   "Measure row-major against column-major traversal of a large 2D array. "
   "Predict the ratio from the cache line size before measuring, then explain "
   "any discrepancy.",
   "Implement naive and blocked matrix multiplication. Compute the optimal "
   "tile size from your L1 capacity, then sweep B and confirm the optimum "
   "empirically.",
   "Convert a particle system from AoS to SoA. Measure an update that touches "
   "two fields of eight, and report both the speedup and the change in cache "
   "misses.",
   "Apply hot/cold splitting to a struct where one field is accessed in a hot "
   "loop and six are not. Measure.",
   "Compare a sequential array sum against a random-order sum of the same "
   "data. Then add software prefetch to the random version and report whether "
   "it helped.",
   "Take a loop with an indirect access pattern (<code>a[b[i]]</code>) and "
   "tune a software prefetch distance. Plot time against distance and find "
   "the optimum.",
   "Convert a <code>double</code> computation to <code>float</code> where "
   "precision permits. Measure, and determine whether you became "
   "compute-bound.",
 ],
 "selfcheck": [
   "Why is column-major traversal of a row-major array 5&ndash;10&times; "
   "slower, and why not exactly 16&times;?",
   "How do you compute the right tile size for blocked matrix multiplication?",
   "When is array-of-structs the right choice, and when is "
   "struct-of-arrays?",
   "Name three access patterns a hardware prefetcher cannot handle.",
   "What does successful prefetching convert a latency problem into, and why "
   "does that help?",
   "Why should layout changes be attempted before loop transformations?",
   "What is the first thing to check before applying any optimisation in this "
   "module?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Virtual Memory and the TLB",
 "subtitle": "The indirection under every memory access.",
 "question": "What happens between your pointer and a physical address?",
 "outcomes": [
     "Explain address translation and multi-level page tables.",
     "Explain the TLB and why it is on the critical path.",
     "Quantify TLB reach and recognise when it is exceeded.",
     "Explain huge pages and when they help.",
     "Explain page faults, swapping, and memory-mapped files.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why indirection",
   "blurb": "Four problems solved by one mechanism."},

  {"t": "bullets", "kicker": "Motivation", "title": "What virtual memory buys",
   "items": [
     "<b>Isolation</b> — a process cannot name another's memory. "
     "Security and robustness come free.",
     "<b>Relocation</b> — every program can believe it starts at the "
     "same address.",
     "<b>Over-subscription</b> — use more memory than exists, paging to "
     "disk.",
     "<b>Sharing</b> — one physical copy of a library mapped into many "
     "processes.",
     "",
     "All four come from one idea: programs use <b>virtual</b> addresses that "
     "hardware translates to <b>physical</b> ones.",
   ]},

  {"t": "code", "kicker": "Translation", "title": "Four-level page tables",
   "lang": "text", "code": """
Virtual address (x86-64, 48-bit):

 47   39 38   30 29   21 20   12 11        0
+-------+-------+-------+-------+-----------+
| PML4  | PDPT  |  PD   |  PT   |  OFFSET   |
+-------+-------+-------+-------+-----------+
   9       9       9       9         12 bits -> 4 KB pages

Each 9-bit field indexes one level of the page table.
A full walk = FOUR dependent memory accesses, before the
actual data access.

At ~250 cycles each if uncached, that is ~1000 cycles
to translate one address. Clearly unacceptable -- hence
the TLB.
""",
   "caption": "Multi-level tables keep the structure sparse: unused regions "
              "cost nothing. The price is four dependent lookups per "
              "translation.",
   "note": "Emphasise 'dependent' — the walk cannot be parallelised, "
           "exactly as in Module 02's pointer chasing."},

  {"t": "section", "label": "Part 2", "title": "The TLB",
   "blurb": "A cache for translations, and a hard limit you can hit."},

  {"t": "bullets", "kicker": "TLB", "title": "Caching the translation",
   "items": [
     "The <b>Translation Lookaside Buffer</b> caches recent virtual-to-"
     "physical mappings.",
     "",
     "Small and fast: typically 64 entries for L1 DTLB, 1500–2000 for "
     "L2 TLB.",
     "Often fully associative, because it is small enough to afford it.",
     "",
     "<b>Hit:</b> translation is essentially free, overlapped with cache "
     "access.",
     "<b>Miss:</b> a page walk — up to four dependent memory accesses.",
     "",
     "It is on the critical path of <b>every single memory access</b>.",
   ]},

  {"t": "eq", "kicker": "Reach", "title": "TLB reach — the number to know",
   "eqs": [
     ("reach  =  entries × page size",
      "How much memory can be addressed without a TLB miss."),
     ("1536 entries × 4 KB  =  6 MB",
      "Your L3 cache may be 32 MB. The TLB cannot reach it."),
     ("1536 entries × 2 MB  =  3 GB",
      "With huge pages, reach grows 512× for free."),
   ],
   "caption": "This is the mismatch that makes huge pages worth configuring: "
              "a working set that fits in cache may still thrash the TLB.",
   "note": "TLB reach being smaller than L3 is the surprising fact. Students "
           "assume the TLB covers whatever the cache covers."},

  {"t": "callout", "title": "You can fit in cache and still miss constantly",
   "kind": "The non-obvious failure",
   "body": ["A 20 MB working set fits comfortably in a 32 MB L3. But with 4 "
            "KB pages and 1536 TLB entries, the TLB reaches only 6 MB.",
            "Every access to the other 14 MB triggers a page walk — up "
            "to four dependent memory accesses — even though the data "
            "itself is in cache.",
            "The symptom is a program that is clearly not bandwidth-bound and "
            "clearly not missing in L3, yet runs far slower than it should. "
            "Check <code>dTLB-load-misses</code>.",
            "<b>Fix:</b> huge pages. 2 MB pages raise the reach from 6 MB to "
            "3 GB."]},

  {"t": "table", "kicker": "Huge pages", "title": "The trade",
   "header": ["", "Benefit", "Cost"],
   "widths": [2.6, 4.8, 4.7],
   "rows": [
     ["2 MB pages", "512× TLB reach; shorter page walks", "Internal fragmentation; harder to allocate"],
     ["1 GB pages", "Enormous reach", "Only for very large, long-lived regions"],
     ["Transparent HP", "Automatic, no code change", "Allocation stalls; unpredictable latency"],
   ],
   "note": "Transparent huge pages are on by default on many Linux systems "
           "and are a known cause of latency spikes in databases."},

  {"t": "section", "label": "Part 3", "title": "Faults and mapping",
   "blurb": "What happens when the page is not there."},

  {"t": "table", "kicker": "Page faults", "title": "Three kinds, very different costs",
   "header": ["Kind", "Cause", "Cost"],
   "widths": [2.8, 5.0, 4.3],
   "rows": [
     ["Minor", "Page is in memory, not mapped in this table", "~1 μs"],
     ["Major", "Page must be read from disk", "~100 μs (SSD)"],
     ["Invalid", "No valid mapping exists", "SIGSEGV — your bug"],
   ],
   "note": "Minor faults are routine and cheap: first touch of freshly "
           "allocated memory, copy-on-write after fork."},

  {"t": "bullets", "kicker": "Consequences", "title": "Things this explains",
   "items": [
     "<b>First touch is slow.</b> <code>malloc</code> reserves address space; "
     "physical pages arrive on first write.",
     ("Hence benchmark warm-up: the first pass pays the faults.", 1),
     "",
     "<b>fork() is cheap.</b> Pages are shared copy-on-write until written.",
     "",
     "<b>mmap on a file</b> turns file I/O into memory access, with the page "
     "cache doing the work.",
     "",
     "<b>NUMA first-touch:</b> on multi-socket machines, a page is allocated "
     "near whichever core first touches it.",
     ("So initialise data in parallel, with the thread that will use it.", 1),
   ],
   "footnote": "The NUMA point is a real and common performance bug in "
               "parallel code."},

  {"t": "callout", "title": "Why this module sits between caches and execution",
   "kind": "Perspective",
   "body": ["Every memory access in Modules 05 and 06 silently assumed a "
            "physical address. Obtaining one is itself a memory access "
            "problem, with its own cache (the TLB) and its own miss "
            "behaviour.",
            "The practical upshot is that there are <i>two</i> hierarchies to "
            "keep happy: the data cache hierarchy and the translation "
            "hierarchy. Code can be perfectly cache-friendly and still be "
            "destroyed by TLB misses.",
            "When a program is slow, has good cache behaviour, and is not "
            "bandwidth-bound, the TLB is the next thing to check."]},
 ],
 "takeaways": [
   "Virtual memory buys isolation, relocation, over-subscription, and "
   "sharing from one indirection.",
   "A four-level page walk is four <i>dependent</i> memory accesses, which is "
   "why the TLB exists.",
   "TLB reach = entries × page size. At 4 KB pages it is typically ~6 "
   "MB — smaller than your L3 cache.",
   "A working set that fits in cache can still thrash the TLB. Check "
   "dTLB-load-misses before concluding memory is fine.",
   "Huge pages raise reach 512× and shorten walks, at the cost of "
   "fragmentation and allocation stalls.",
   "First touch allocates the physical page — and on NUMA systems, "
   "allocates it near the touching core. Initialise in parallel.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why virtual memory"),
  ("p", "Programs do not use physical addresses. They use <b>virtual</b> "
        "addresses, translated by hardware into physical ones on every "
        "access. One indirection buys four distinct things:"),
  ("ul", ["<b>Isolation.</b> A process cannot even name memory belonging to "
          "another, because the translation simply does not exist. Memory "
          "protection is a consequence of the addressing scheme rather than a "
          "check bolted on top.",
          "<b>Relocation.</b> Every program can be compiled as though it "
          "starts at the same address, and be placed anywhere physically.",
          "<b>Over-subscription.</b> The sum of all processes' address spaces "
          "may exceed physical memory, with inactive pages evicted to disk.",
          "<b>Sharing.</b> A single physical copy of a shared library or a "
          "file can be mapped into many address spaces at once."]),
  ("h2", "1.1 &nbsp; Multi-level page tables"),
  ("code", """x86-64 virtual address (48 significant bits):

 47   39 38   30 29   21 20   12 11         0
+-------+-------+-------+-------+------------+
| PML4  | PDPT  |  PD   |  PT   |   OFFSET   |
+-------+-------+-------+-------+------------+
    9       9       9       9        12 bits"""),
  ("p", "A flat page table for a 48-bit address space with 4 KB pages would "
        "need 2&#179;&#8310; entries — hundreds of gigabytes per "
        "process. A multi-level table is sparse: a region of address space "
        "that is never used costs nothing because the corresponding "
        "upper-level entry is simply absent."),
  ("p", "The cost is that translating one address requires walking four "
        "levels, and each level's location depends on the previous level's "
        "contents. These are four <b>dependent</b> memory accesses — "
        "exactly the serialised pointer chasing of Module 02, and equally "
        "unamenable to overlapping. At 250 cycles each when uncached, a full "
        "walk approaches a thousand cycles, before the actual data access "
        "begins."),

  ("h1", "2 &nbsp; The TLB"),
  ("p", "A thousand cycles per access is obviously impossible, so "
        "translations are cached in the <b>Translation Lookaside Buffer</b>."),
  ("table", ["Property", "Typical value"],
   [["L1 data TLB entries", "64&ndash;100, often fully associative"],
    ["L2 (shared) TLB entries", "1,500&ndash;2,000"],
    ["Hit cost", "Effectively zero — overlapped with cache lookup"],
    ["Miss cost", "A page walk: up to four dependent memory accesses, "
     "partially cached in dedicated page-walk caches"]],
   [0.34, 0.66]),
  ("p", "The TLB sits on the critical path of every memory access, which is "
        "why it is kept small and fast, and why its capacity becomes a real "
        "constraint."),
  ("h2", "2.1 &nbsp; TLB reach"),
  ("eq", "reach = TLB entries &times; page size"),
  ("table", ["Entries", "Page size", "Reach"],
   [["1,536", "4 KB", "6 MB"],
    ["1,536", "2 MB", "3 GB"],
    ["1,536", "1 GB", "1.5 TB"]],
   [0.26, 0.26, 0.48]),
  ("callout", "The TLB does not reach as far as your cache",
   ["A modern L3 cache can be 32 MB or more. With 4 KB pages, the TLB reaches "
    "around 6 MB.",
    "So a 20 MB working set <i>fits in L3</i> and still incurs a page walk on "
    "most accesses outside the first 6 MB. The data is in cache; the "
    "<i>translation</i> is not.",
    "The symptom is distinctive and easily misdiagnosed: a program that is "
    "not bandwidth-bound, has a low L3 miss rate, and is nonetheless far "
    "slower than it should be. The counter to check is "
    "<code>dTLB-load-misses</code>.",
    "This is why there are effectively <b>two</b> hierarchies to satisfy: the "
    "data cache hierarchy and the translation hierarchy. Code can be perfect "
    "for one and hostile to the other."]),

  ("break",),
  ("h1", "3 &nbsp; Huge pages"),
  ("p", "Larger pages multiply TLB reach directly and shorten the page walk "
        "by removing a level."),
  ("table", ["Page size", "Benefit", "Cost"],
   [["<b>2 MB</b>", "512&times; the reach of 4 KB pages; one fewer level in "
     "the walk.",
     "Internal fragmentation: a mostly-empty 2 MB page wastes real memory. "
     "Harder to allocate once memory is fragmented."],
    ["<b>1 GB</b>", "Enormous reach; appropriate for very large data "
     "structures.",
     "Only sensible for large, long-lived, densely used regions. Usually "
     "reserved at boot."],
    ["<b>Transparent huge pages</b>", "Automatic promotion, no code changes.",
     "The allocator may stall trying to assemble a contiguous 2 MB region, "
     "producing unpredictable latency spikes. Several databases recommend "
     "disabling THP for this reason."]],
   [0.22, 0.38, 0.40]),
  ("p", "Hardware prefetchers also stop at page boundaries, since prefetching "
        "into an unmapped page risks a spurious fault. Larger pages therefore "
        "let prefetching run further uninterrupted — a secondary benefit "
        "that is easy to overlook."),

  ("h1", "4 &nbsp; Page faults"),
  ("table", ["Kind", "Cause", "Typical cost"],
   [["<b>Minor</b>", "The page is in physical memory but not mapped in this "
     "process's tables — first touch of newly allocated memory, "
     "copy-on-write, or a shared page already resident.",
     "~1 &mu;s. Routine."],
    ["<b>Major</b>", "The page must be read from storage.",
     "~100 &mu;s on SSD; ~10 ms on rotating disk. Visible to users."],
    ["<b>Invalid</b>", "No valid mapping exists for this address.",
     "SIGSEGV. This is a bug in your program, not a performance issue."]],
   [0.14, 0.56, 0.30]),
  ("h2", "4.1 &nbsp; Consequences worth knowing"),
  ("ul", ["<b>First touch is slow.</b> <code>malloc</code> reserves address "
          "space; physical pages are allocated lazily on first write. This is "
          "a large part of why benchmark warm-up matters (Module 01) — "
          "the first pass pays for every page.",
          "<b><code>fork()</code> is cheap.</b> The child shares the parent's "
          "pages copy-on-write; physical copying happens only for pages that "
          "are actually written.",
          "<b><code>mmap</code> turns file I/O into memory access.</b> The "
          "page cache handles reading on demand, and the same physical pages "
          "serve every process mapping the file.",
          "<b>NUMA first touch.</b> On multi-socket systems, a physical page "
          "is allocated in the memory attached to whichever core first "
          "touches it. Allocating and initialising a large array on one "
          "thread and then processing it on many places all of it on one "
          "socket, with every other socket paying remote-access latency. "
          "<b>Initialise in parallel, with the thread that will use the "
          "data.</b> This is a common and expensive bug in parallel code, and "
          "CSCE 735 returns to it."]),

  ("h1", "5 &nbsp; Where this fits"),
  ("callout", "Two hierarchies, not one",
   ["Modules 05 and 06 treated memory access as a question of cache "
    "behaviour, silently assuming a physical address was available. Obtaining "
    "that address is itself a memory access problem with its own cache and "
    "its own miss penalty.",
    "A program must satisfy both hierarchies. Cache-friendly code with a "
    "scattered page footprint will thrash the TLB; TLB-friendly code with a "
    "bad stride will thrash the cache.",
    "Diagnostic order: confirm it is memory-bound (low IPC), check cache miss "
    "rates, and if those look acceptable, check "
    "<code>dTLB-load-misses</code> before looking anywhere else."]),
 ],
 "resources": [
   ("Onur Mutlu — Virtual Memory lectures",
    "https://safari.ethz.ch/architecture/",
    "Translation, TLBs, and the interaction with caches."),
   ("Ulrich Drepper — What Every Programmer Should Know About Memory, "
    "section 4",
    "https://people.freebsd.org/~lstewart/articles/cpumemory.pdf",
    "Virtual memory and TLB behaviour with measurements."),
   ("OSTEP — Virtual Memory chapters (free book)",
    "https://pages.cs.wisc.edu/~remzi/OSTEP/",
    "The operating-system side: paging policy, replacement, swapping. "
    "Overlaps usefully with CSCE 611."),
   ("Linux kernel documentation — Transparent Hugepage Support",
    "https://docs.kernel.org/admin-guide/mm/transhuge.html",
    "How THP works in practice, and why some workloads disable it."),
 ],
 "exercises": [
   "Measure TLB reach: access one byte per page across a working set that "
   "grows from 1 MB to 1 GB, and find the size at which cost per access "
   "jumps. Compare with entries &times; 4 KB from your CPU's specification.",
   "Repeat the experiment with huge pages enabled "
   "(<code>madvise(MADV_HUGEPAGE)</code> or <code>mmap</code> with "
   "<code>MAP_HUGETLB</code>) and confirm the jump moves.",
   "Construct a workload with a 20 MB working set that fits in L3 but exceeds "
   "TLB reach. Show with hardware counters that L3 misses are low while TLB "
   "misses are high.",
   "Measure the cost of first touch: allocate 1 GB, time a first pass writing "
   "every page, then time a second pass. Explain the difference.",
   "Measure <code>fork()</code> on a process with a 1 GB heap, then measure "
   "it again after the child writes to every page. Explain both numbers.",
   "On a NUMA machine if you have access to one: initialise a large array "
   "from a single thread, then process it from all threads; then initialise "
   "in parallel and repeat. Report the difference.",
 ],
 "selfcheck": [
   "Name the four things virtual memory provides.",
   "Why are multi-level page tables used instead of a flat table, and what "
   "does the structure cost?",
   "Why is a page walk particularly expensive beyond simply being four "
   "accesses?",
   "Compute TLB reach for 1,536 entries at 4 KB and at 2 MB. Compare with a "
   "32 MB L3 cache.",
   "Describe a program that fits entirely in cache yet is limited by TLB "
   "misses. How would you detect it?",
   "Give two costs of huge pages.",
   "What is NUMA first touch, and what practice does it imply for parallel "
   "initialisation?",
 ],
},

]
