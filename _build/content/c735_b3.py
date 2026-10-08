# -*- coding: utf-8 -*-
"""CSCE 735 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "GPU Programming",
 "subtitle": "Thousands of threads, and a machine that only makes sense "
             "once.",
 "question": "How do you program a throughput processor?",
 "outcomes": [
     "Explain the CUDA execution model and map it to the hardware.",
     "Explain warps and why divergence costs.",
     "Explain the memory hierarchy and coalescing.",
     "Explain occupancy and what it is for.",
     "Write a correct kernel and launch it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The execution model",
   "blurb": "Threads, blocks, and grids."},

  {"t": "code", "kicker": "CUDA", "title": "The model, and the hardware under it",
   "lang": "text", "code": """
  SOFTWARE                      HARDWARE
  --------                      --------
  thread                 -->    one lane
  WARP (32 threads)      -->    executed in LOCKSTEP, always
  block (up to 1024)     -->    resident on ONE streaming multiprocessor
                                (shares that SM's shared memory)
  grid (many blocks)     -->    distributed across all SMs

  KEY FACTS:
   * A warp is the real unit of execution. Blocks are divided into
     warps and warps are scheduled; individual threads are not.
   * Threads in a block can synchronise (__syncthreads) and share
     memory. Threads in different blocks CANNOT, except via global
     memory and a kernel boundary.
   * Blocks must be independent -- they may run in any order, and
     any subset may run concurrently. This is what makes the model
     scale across devices with different SM counts.
""",
   "caption": "Blocks being independent is what lets the same binary run on "
              "a device with 4 SMs and one with 128.",
   "note": "Block independence is the design decision that makes CUDA "
           "portable across a decade of hardware."},

  {"t": "callout", "title": "The warp is the real unit, not the thread",
   "kind": "The fact that explains the rest",
   "body": ["<b>32 threads execute in lockstep</b>, issuing the same "
            "instruction each cycle. The hardware schedules warps, not "
            "threads.",
            "<b>So a block of 100 threads occupies four warps</b>, the last "
            "of which is 28/32 idle. <b>Always use multiples of 32.</b>",
            "<b>And a branch that goes different ways within a warp "
            "serialises</b> — both paths execute, with the inactive lanes "
            "masked off.",
            "<b>Everything about GPU performance follows from this.</b> "
            "Divergence, coalescing, and occupancy are all consequences of "
            "lockstep execution."]},

  {"t": "callout", "title": "Divergence: both branches execute",
   "kind": "The cost",
   "body": ["<b>If some lanes in a warp take the <code>if</code> and others "
            "the <code>else</code>, the warp executes both</b>, masking the "
            "inactive lanes each time.",
            "<b>So the cost is the sum of the branches, not the "
            "maximum.</b> A two-way branch costs twice.",
            "<b>Divergence <i>between</i> warps is free.</b> Warp 0 taking "
            "one path and warp 1 another costs nothing — they are "
            "scheduled independently.",
            "<b>So organise data so that threads in the same warp take the "
            "same path</b> — sort by branch condition, or pad, or "
            "restructure. This is frequently a large win."]},

  {"t": "section", "label": "Part 2", "title": "Memory",
   "blurb": "Where GPU performance is actually won."},

  {"t": "table", "kicker": "Hierarchy", "title": "The GPU memory hierarchy",
   "header": ["Space", "Scope", "Latency", "Note"],
   "widths": [2.4, 2.8, 2.4, 4.5],
   "rows": [
     ["Registers", "One thread", "~1 cycle", "<b>Plentiful; limits occupancy</b>"],
     ["<b>Shared</b>", "<b>One block</b>", "<b>~20 cycles</b>", "<b>Programmer-managed cache</b>"],
     ["L1 / L2", "SM / device", "~30/200", "Automatic"],
     ["<b>Global</b>", "Device", "<b>~400–800</b>", "<b>Large, slow, coalescing matters</b>"],
     ["Constant", "Device, read-only", "Cached", "Broadcast to a whole warp cheaply"],
     ["Local", "One thread", "<b>Global speed</b>", "<b>Register spills. Avoid</b>"],
   ],
   "footnote": "<b>Shared memory is the one you manage</b>, and using it "
               "well is most of GPU optimisation (Module 09).",
   "note": "'Local' memory being global-speed surprises people and spilling "
           "is a common silent performance bug."},

  {"t": "callout", "title": "Coalescing: the warp's accesses must be contiguous",
   "kind": "The single most important memory rule",
   "body": ["<b>The memory system serves a warp's 32 accesses as a small "
            "number of wide transactions.</b>",
            "<b>If the 32 threads read 32 consecutive floats</b>, that is "
            "one 128-byte transaction. <b>Perfect.</b>",
            "<b>If they read 32 scattered addresses</b>, that is up to 32 "
            "separate transactions — <b>32× the memory traffic</b> for "
            "the same data.",
            "<b>So thread <i>i</i> should access element <i>i</i></b>, and "
            "arrays should be structure-of-arrays. The same rule as "
            "Module 02, with a much steeper penalty."]},

  {"t": "code", "kicker": "Coalescing", "title": "The pattern that matters",
   "lang": "cpp", "code": """
// COALESCED: consecutive threads read consecutive addresses.
__global__ void good(float* a, float* b, float* c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) c[i] = a[i] + b[i];       // thread i -> element i
}

// NOT COALESCED: stride between consecutive threads.
__global__ void bad(float* a, float* c, int n, int stride) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i*stride < n) c[i] = a[i * stride];   // scattered
}

// NOT COALESCED: array of structures -- each thread wants one
// field, so the warp reads 32 widely separated words.
struct P { float x, y, z, w; };
__global__ void aos(P* p, float* out, int n) {
    int i = ...;  out[i] = p[i].x;       // reads 1 of every 4 floats
}
//  FIX: separate arrays for x, y, z, w (structure of arrays).
""",
   "caption": "The array-of-structures case is the one that appears in "
              "real code and silently costs 4×.",
   "note": "The AoS case is worth running — the measured difference is "
           "convincing in a way the explanation is not."},

  {"t": "section", "label": "Part 3", "title": "Occupancy",
   "blurb": "Having enough threads to hide latency."},

  {"t": "callout", "title": "Occupancy exists to hide memory latency",
   "kind": "What it is for",
   "body": ["<b>Global memory latency is 400 to 800 cycles.</b> A CPU "
            "hides this with caches and prediction; a GPU hides it by "
            "switching to another warp.",
            "<b>Occupancy is the fraction of the maximum resident warps "
            "that are actually resident.</b>",
            "<b>More resident warps means more candidates to switch to</b>, "
            "so more latency is covered.",
            "<b>It is limited by registers per thread, shared memory per "
            "block, and block size.</b> Using too many registers reduces the "
            "warps that fit — which is a real tuning trade-off."]},

  {"t": "callout", "title": "Maximum occupancy is not the goal",
   "kind": "The common misunderstanding",
   "body": ["<b>Occupancy is a means, not an end.</b> The goal is to "
            "saturate the limiting resource — usually memory bandwidth.",
            "<b>A kernel at 50% occupancy that saturates bandwidth is "
            "finished.</b> Raising occupancy achieves nothing.",
            "<b>And more registers per thread can beat more warps</b>, "
            "because instruction-level parallelism within a thread also "
            "hides latency.",
            "<b>Volkov's result:</b> several kernels run <i>faster</i> at "
            "lower occupancy with more work per thread. <b>Measure, do not "
            "maximise the metric.</b>"]},

  {"t": "bullets", "kicker": "Practice", "title": "Getting a kernel working",
   "items": [
     "<b>Check every error.</b> Kernel launches fail asynchronously; "
     "without checking you see a wrong answer, not an error.",
     "",
     "<b>Use <code>compute-sanitizer</code></b> — the CUDA memcheck and "
     "race detector. Catches out-of-bounds and races.",
     "",
     "<b>Verify against the CPU result</b> before optimising anything.",
     "",
     "<b>Guard the bounds.</b> Grid size rounds up, so some threads are "
     "past the end. <code>if (i &lt; n)</code> is not optional.",
     "",
     "<b>And profile with Nsight Compute</b>, which reports the limiting "
     "resource directly.",
   ],
   "footnote": "<b>Asynchronous launch failure</b> is the one that costs "
               "beginners the most time — the error surfaces at the "
               "next synchronisation, far from its cause."},
 ],
 "takeaways": [
   "A warp of 32 threads executes in lockstep and is the real unit of "
   "scheduling — everything about GPU performance follows from that.",
   "Blocks must be independent, which is what lets one binary scale across "
   "devices with very different SM counts.",
   "A divergent branch within a warp executes both paths with masking, so "
   "the cost is the sum; divergence between warps is free.",
   "Coalescing is the most important memory rule: thread i should access "
   "element i, or the warp costs up to 32 transactions instead of one.",
   "Occupancy exists to hide memory latency by providing warps to switch to, "
   "and is limited by registers and shared memory.",
   "Maximum occupancy is not the goal — several kernels run faster at "
   "lower occupancy with more work per thread.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The execution model"),
  ("table", ["Software abstraction", "Hardware reality"],
   [["<b>Thread</b>", "One lane of a SIMD unit."],
    ["<b>Warp</b> (32 threads)",
     "<b>The real unit of execution.</b> Executed in lockstep, issuing one "
     "instruction for all 32 lanes. The hardware schedules warps; it does "
     "not schedule threads."],
    ["<b>Block</b> (up to 1024 threads)",
     "Resident on <b>one</b> streaming multiprocessor for its entire "
     "lifetime, sharing that SM's shared memory and able to synchronise with "
     "<code>__syncthreads()</code>."],
    ["<b>Grid</b> (many blocks)",
     "Distributed across all SMs. <b>Blocks must be independent</b> — "
     "they may execute in any order, and any subset may be resident "
     "simultaneously."]],
   [0.26, 0.74]),
  ("p", "<b>Block independence is the design decision that makes CUDA "
        "portable.</b> Because blocks cannot communicate or depend on "
        "execution order, the same binary runs correctly on a device with "
        "four SMs and on one with a hundred and twenty-eight — the "
        "runtime simply schedules more or fewer blocks concurrently. "
        "Permitting inter-block dependencies would have tied every program "
        "to a particular device's resources."),
  ("callout", "The warp is the real unit, not the thread",
   ["<b>Thirty-two threads execute in lockstep</b>, issuing the same "
    "instruction on the same cycle across 32 lanes. This is SIMD hardware "
    "with a thread-shaped programming model layered over it.",
    "<b>So a block of 100 threads occupies four warps</b>, the fourth of "
    "which has 28 of its 32 lanes idle for the entire kernel. <b>Always use "
    "block sizes that are multiples of 32</b>, and 128 or 256 is the usual "
    "starting point.",
    "<b>And a branch that goes different ways within a warp serialises</b> "
    "— see below.",
    "<b>Essentially everything about GPU performance follows from "
    "this.</b> Divergence, coalescing, and occupancy are all direct "
    "consequences of 32 lanes executing together, and a model that treats "
    "GPU threads as independent will mispredict performance every time."]),
  ("callout", "Divergence: both branches execute",
   ["<b>If some lanes of a warp take the <code>if</code> branch and others "
    "take the <code>else</code>, the warp executes both</b> — first one "
    "with the other lanes masked off, then the other with the first set "
    "masked off.",
    "<b>So the cost is the sum of the two branches, not the maximum.</b> A "
    "two-way divergent branch costs twice what a uniform one would, and a "
    "switch with eight cases taken differently across a warp costs eight "
    "times.",
    "<b>Divergence <i>between</i> warps is entirely free.</b> If warp 0 "
    "takes one path and warp 1 takes the other, each executes only its own "
    "path — they are scheduled independently and never interact.",
    "<b>So organise data so that threads within a warp take the same "
    "path.</b> Sorting the input by the branch condition, padding, or "
    "restructuring the decomposition so that divergence falls on warp "
    "boundaries is frequently a large win — and it is a data layout "
    "decision rather than a code change."]),

  ("h1", "2 &nbsp; Memory"),
  ("table", ["Space", "Scope", "Latency", "Notes"],
   [["<b>Registers</b>", "One thread", "~1 cycle",
     "Plentiful, and <b>register usage per thread limits occupancy</b> "
     "(&sect;3)."],
    ["<b>Shared memory</b>", "<b>One block</b>", "~20 cycles",
     "<b>A programmer-managed cache.</b> Fast, small (tens of KB per SM), "
     "and explicitly loaded. <b>Using it well is most of GPU "
     "optimisation</b> (Module 09)."],
    ["<b>L1 / L2 cache</b>", "SM / whole device", "~30 / ~200 cycles",
     "Automatic. L1 shares hardware with shared memory on most "
     "architectures."],
    ["<b>Global memory</b>", "Whole device", "<b>400–800 cycles</b>",
     "Large (gigabytes), slow, and <b>coalescing determines whether you get "
     "its bandwidth</b>."],
    ["<b>Constant memory</b>", "Device, read-only", "Cached",
     "Broadcasts cheaply when a whole warp reads the same address — "
     "ideal for kernel parameters and lookup tables."],
    ["<b>Local memory</b>", "One thread", "<b>Global memory speed</b>",
     "<b>Despite the name, it lives in global memory.</b> Used for register "
     "spills and for arrays indexed dynamically. <b>A silent and severe "
     "performance bug</b> — check the compiler's register and spill "
     "report."]],
   [0.15, 0.17, 0.18, 0.50]),
  ("callout", "Coalescing is the most important memory rule",
   ["<b>The memory system serves a warp's 32 accesses as a small number of "
    "wide transactions</b>, typically 32 or 128 bytes each.",
    "<b>If the 32 threads read 32 consecutive floats, that is a single "
    "128-byte transaction.</b> One request, full bandwidth, nothing wasted.",
    "<b>If they read 32 scattered addresses, that is up to 32 separate "
    "transactions</b> — and each transaction still fetches a full "
    "cache line, so <b>the memory traffic can be 32 times larger</b> for "
    "exactly the same useful data.",
    "<b>So thread <i>i</i> should access element <i>i</i></b>, and data "
    "should be laid out structure-of-arrays rather than "
    "array-of-structures. <b>This is the same rule as Module 02's "
    "vectorisation guidance</b>, with a considerably steeper penalty for "
    "violating it — on a CPU a strided access is slower, and on a GPU "
    "it can cost an order of magnitude."]),
  ("code", """// COALESCED: consecutive threads, consecutive addresses
int i = blockIdx.x * blockDim.x + threadIdx.x;
if (i < n) c[i] = a[i] + b[i];

// NOT COALESCED: stride between consecutive threads
if (i*stride < n) c[i] = a[i * stride];

// NOT COALESCED: array of structures -- each thread wants one field,
// so the warp reads 32 widely separated words
struct P { float x, y, z, w; };
out[i] = p[i].x;          // reads 1 float of every 4
// FIX: separate arrays for x, y, z, w"""),

  ("break",),
  ("h1", "3 &nbsp; Occupancy"),
  ("callout", "Occupancy exists to hide memory latency",
   ["<b>Global memory latency is 400 to 800 cycles.</b> A CPU hides this "
    "with large caches, prefetching, and out-of-order execution — "
    "machinery that predicts and avoids the stall. <b>A GPU hides it by "
    "switching to a different warp</b> (Module 02 &sect;4).",
    "<b>Occupancy is the ratio of resident warps to the maximum the "
    "hardware supports</b> per streaming multiprocessor.",
    "<b>More resident warps means more candidates to switch to</b> when one "
    "stalls, so more of the latency is covered by useful work from other "
    "warps.",
    "<b>It is limited by three resources:</b> registers per thread "
    "(registers are a fixed pool per SM, so using more per thread means "
    "fewer resident threads), shared memory per block (same argument), and "
    "block size (which must divide the limits sensibly). <b>Using more "
    "registers to avoid recomputation reduces occupancy</b>, which is a real "
    "and frequently non-obvious trade-off."]),
  ("callout", "Maximum occupancy is not the goal",
   ["<b>Occupancy is a means, not an end.</b> The actual goal is to "
    "saturate whichever resource limits the kernel — usually memory "
    "bandwidth (Module 07).",
    "<b>A kernel running at 50% occupancy that already saturates memory "
    "bandwidth is finished.</b> Raising its occupancy to 100% achieves "
    "nothing whatsoever, because the bandwidth was already the constraint.",
    "<b>And more registers per thread can beat more warps.</b> "
    "Instruction-level parallelism <i>within</i> a thread also hides "
    "latency — several independent loads in flight from one thread "
    "cover a stall just as effectively as switching warps does, and the "
    "registers that make it possible reduce occupancy.",
    "<b>Volkov's result is the canonical demonstration:</b> several standard "
    "kernels run measurably <i>faster</i> at lower occupancy, with more work "
    "and more registers per thread. <b>Measure the kernel; do not maximise "
    "the metric</b> — which is a specific instance of a general rule "
    "worth carrying."]),
  ("ul", ["<b>Check every CUDA error.</b> Kernel launches are asynchronous "
          "and report failure at the next synchronisation point — so "
          "without explicit checking you observe a wrong answer rather than "
          "an error, far from where it occurred. <b>This costs beginners "
          "more time than anything else</b>; wrap every call in a checking "
          "macro from the first line of code.",
          "<b>Use <code>compute-sanitizer</code></b>, which provides "
          "out-of-bounds checking, race detection, and uninitialised memory "
          "detection for device code. The GPU equivalent of Module 03's "
          "ThreadSanitizer discipline.",
          "<b>Verify against a CPU implementation before optimising "
          "anything.</b> A fast wrong kernel is worth nothing, and "
          "optimisation frequently introduces subtle indexing errors.",
          "<b>Guard the bounds.</b> The grid size rounds up to a whole "
          "number of blocks, so the final block contains threads whose index "
          "exceeds the data. <b><code>if (i &lt; n)</code> is not "
          "optional</b>, and omitting it corrupts memory past the array.",
          "<b>Profile with Nsight Compute</b>, which reports the limiting "
          "resource, the achieved bandwidth, the occupancy, and the "
          "divergence directly — rather than requiring you to infer "
          "them."]),
 ],
 "resources": [
   ("NVIDIA &mdash; CUDA C++ Programming Guide (free)",
    "https://web.archive.org/web/20260911074013/https://docs.nvidia.com/cuda/cuda-c-programming-guide/",
    "The authoritative reference for the execution and memory models of "
    "&sect;1 and &sect;2."),
   ("NVIDIA &mdash; CUDA C++ Best Practices Guide (free)",
    "https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/",
    "The practical companion — coalescing, occupancy, and the "
    "optimisation ordering. Shorter and more immediately useful."),
   ("OLCF &mdash; CUDA Training Series (free)",
    "https://www.olcf.ornl.gov/cuda-training-series/",
    "Structured exercises with solutions, paced sensibly, and they run on "
    "modest hardware."),
   ("Volkov &mdash; Better Performance at Lower Occupancy (free)",
    "https://www.nvidia.com/content/gtc-2010/pdfs/2238_gtc2010.pdf",
    "<b>The &sect;3 result.</b> Short, measured, and it corrects a belief "
    "that is still widespread."),
 ],
 "exercises": [
   "Write, launch, and verify a vector addition kernel with full error "
   "checking and bounds guarding.",
   "Omit the error checking, introduce a launch failure, and observe what "
   "you see instead of an error.",
   "Measure the effect of block size on a simple kernel for sizes 32, 64, "
   "128, 256, 512, 1024, and for 100 and 200.",
   "<b>Measure divergence cost:</b> write a kernel whose branch depends on "
   "thread index modulo 2, and one where it depends on index divided by 32. "
   "Compare.",
   "Measure a coalesced and a strided access pattern, sweeping the stride "
   "from 1 to 32. Plot the achieved bandwidth.",
   "<b>Implement the array-of-structures case</b> and its "
   "structure-of-arrays equivalent, and report the measured ratio.",
   "Use the occupancy calculator or Nsight to find your kernel's occupancy "
   "and what limits it.",
   "Increase registers per thread deliberately and measure occupancy and "
   "performance together. Find a case where lower occupancy is faster.",
   "Run <code>compute-sanitizer</code> on a kernel with a deliberate "
   "out-of-bounds access.",
   "Place a kernel on the GPU's roofline (Module 07) and state what limits "
   "it.",
 ],
 "selfcheck": [
   "Map thread, warp, block, and grid onto the hardware.",
   "Why must blocks be independent, and what does that buy?",
   "Why is the warp the real unit of execution, and what follows for block "
   "size?",
   "What does a divergent branch cost within a warp, and between warps?",
   "Name six GPU memory spaces with their scope and latency.",
   "Why is 'local' memory a performance bug?",
   "Explain coalescing and the cost of violating it.",
   "What is occupancy for, and what three resources limit it?",
   "Why is maximum occupancy not the goal?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "GPU Optimisation",
 "subtitle": "Getting from working to fast.",
 "question": "How do you make a correct kernel a fast one?",
 "outcomes": [
     "Use shared memory for tiling and reuse.",
     "Explain and avoid bank conflicts.",
     "Overlap transfer with computation using streams.",
     "Identify the limiting resource from a profile.",
     "Judge when to use a library instead.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Shared memory",
   "blurb": "The programmer-managed cache."},

  {"t": "callout", "title": "Tiling turns a bandwidth problem into a compute problem",
   "kind": "The central GPU optimisation",
   "body": ["<b>Naive matrix multiply reads each element O(n) times from "
            "global memory.</b> Arithmetic intensity ~0.25 "
            "(Module 07): bandwidth-bound.",
            "<b>Tiled matrix multiply loads a tile into shared memory "
            "once</b> and every thread in the block reuses it.",
            "<b>Intensity rises with the tile dimension</b> — a 32×32 "
            "tile raises it by roughly 32×, which moves the kernel past "
            "the ridge point.",
            "<b>So the same arithmetic becomes compute-bound.</b> This is "
            "the clearest demonstration in the course that intensity is "
            "something you change, not something you have."]},

  {"t": "code", "kicker": "Tiling", "title": "Tiled matrix multiply",
   "lang": "cpp", "code": """
#define T 32
__global__ void matmul(float* A, float* B, float* C, int n) {
    __shared__ float As[T][T], Bs[T][T];

    int row = blockIdx.y*T + threadIdx.y;
    int col = blockIdx.x*T + threadIdx.x;
    float acc = 0.0f;

    for (int t = 0; t < n/T; t++) {
        // COOPERATIVE LOAD: each thread loads one element of each tile.
        As[threadIdx.y][threadIdx.x] = A[row*n + t*T + threadIdx.x];
        Bs[threadIdx.y][threadIdx.x] = B[(t*T + threadIdx.y)*n + col];
        __syncthreads();                 // tile is complete

        for (int k = 0; k < T; k++)      // every thread reuses the tile
            acc += As[threadIdx.y][k] * Bs[k][threadIdx.x];
        __syncthreads();                 // before overwriting it
    }
    C[row*n + col] = acc;
}
// TWO syncthreads: one after loading, one before the next overwrite.
// Omitting the second is a race that appears only under load.
""",
   "caption": "Each tile element is loaded once from global memory and used "
              "T times from shared. That ratio is the speedup.",
   "note": "The second __syncthreads is the one people omit, and the "
           "resulting race is intermittent."},

  {"t": "callout", "title": "Bank conflicts serialise shared memory",
   "kind": "The detail that costs 32×",
   "body": ["<b>Shared memory is divided into 32 banks</b>, each serving "
            "one access per cycle.",
            "<b>If 32 threads access 32 different banks, all are served "
            "simultaneously.</b> Full bandwidth.",
            "<b>If they all access the same bank, the accesses "
            "serialise</b> — 32 cycles instead of one.",
            "<b>Column access of a T×T tile is the classic case:</b> with "
            "T = 32, every thread in a column hits the same bank. <b>Pad the "
            "array to [T][T+1]</b> and the conflict disappears entirely. One "
            "character."]},

  {"t": "section", "label": "Part 2", "title": "Transfers and streams",
   "blurb": "The bus is slower than you think."},

  {"t": "callout", "title": "PCIe is the bottleneck nobody budgets for",
   "kind": "The arithmetic",
   "body": ["<b>GPU memory bandwidth is ~1000 GB/s. PCIe is "
            "~30 GB/s.</b> A factor of thirty.",
            "<b>So transferring data to the GPU can cost more than the "
            "computation</b>, and frequently does for a single kernel.",
            "<b>The rule: keep data resident on the device</b> and run many "
            "kernels on it rather than transferring per operation.",
            "<b>And overlap what you must transfer</b> with computation, "
            "using streams. <b>A kernel that is faster than the CPU but "
            "loses once transfer is counted is a common and dishonest "
            "result.</b>"]},

  {"t": "code", "kicker": "Streams", "title": "Overlapping transfer and compute",
   "lang": "cpp", "code": """
// Split the work into chunks and pipeline them across streams.
// While chunk i computes, chunk i+1 transfers.

const int NS = 4;
cudaStream_t s[NS];
for (int i = 0; i < NS; i++) cudaStreamCreate(&s[i]);

for (int i = 0; i < nchunks; i++) {
    int k = i % NS;
    cudaMemcpyAsync(d_in + off, h_in + off, bytes,
                    cudaMemcpyHostToDevice, s[k]);
    kernel<<<grid, block, 0, s[k]>>>(d_in + off, d_out + off, m);
    cudaMemcpyAsync(h_out + off, d_out + off, bytes,
                    cudaMemcpyDeviceToHost, s[k]);
}

// *** REQUIRES PINNED HOST MEMORY (cudaMallocHost). ***
// Pageable memory cannot be DMA'd directly, so the driver stages
// it through a pinned buffer -- which is synchronous, and your
// "async" copy silently is not.
""",
   "caption": "The pinned memory requirement is the detail that makes this "
              "work or silently not work.",
   "note": "Forgetting pinned memory produces code that looks overlapped "
           "and is not — and the profiler shows it immediately."},

  {"t": "section", "label": "Part 3", "title": "Finding the limit",
   "blurb": "What is actually constraining the kernel."},

  {"t": "table", "kicker": "Diagnosis", "title": "Reading a GPU profile",
   "header": ["Symptom", "Limit", "What helps"],
   "widths": [3.4, 2.8, 5.9],
   "rows": [
     ["High memory throughput, low compute", "<b>Bandwidth</b>", "<b>Tiling; fewer bytes; better layout</b>"],
     ["High compute, low memory", "Compute", "Better algorithm; lower precision"],
     ["<b>Both low</b>", "<b>Latency</b>", "<b>More occupancy or more ILP per thread</b>"],
     ["High divergence", "Control flow", "Reorganise data (Module 08)"],
     ["<b>Low achieved bandwidth</b>", "<b>Coalescing</b>", "<b>Fix the access pattern</b>"],
     ["Gaps between kernels", "Launch or transfer", "Streams; fuse kernels"],
   ],
   "footnote": "<b>'Both low' is the common beginner result</b> and means "
               "the GPU is waiting rather than working.",
   "note": "Nsight Compute names the limiter directly now, which makes "
           "this table a cross-check rather than a diagnosis procedure."},

  {"t": "bullets", "kicker": "Order", "title": "The GPU optimisation order",
   "items": [
     "<b>1. Correctness, verified against the CPU.</b>",
     "<b>2. Coalescing.</b> Usually the largest single factor "
     "(Module 08).",
     "<b>3. Shared memory tiling</b>, where there is reuse to exploit.",
     "<b>4. Occupancy</b>, if the profile says latency-bound.",
     "<b>5. Divergence</b>, if the profile says control flow.",
     "<b>6. Streams and transfer overlap.</b>",
     "<b>7. Instruction-level tuning.</b> Last, and rarely needed.",
     "",
     "<b>Measure after each.</b> Some steps interact and some lose.",
   ],
   "note": "This mirrors Module 07's CPU ordering and for the same "
           "reasons."},

  {"t": "callout", "title": "Use the library",
   "kind": "The honest recommendation",
   "body": ["<b>cuBLAS, cuFFT, cuDNN, Thrust, and CUB are written by people "
            "with the architecture documentation</b> and are tuned per "
            "device generation.",
            "<b>A hand-written matrix multiply reaching 60% of cuBLAS is a "
            "good result</b>, and it took you a week.",
            "<b>Write your own to understand the machine</b> — which is "
            "what this module is for, and it is genuinely necessary for "
            "reading a profile.",
            "<b>And then use theirs.</b> <b>Project 2 requires the "
            "comparison</b>, and reporting the gap honestly is the point of "
            "the exercise."]},
 ],
 "takeaways": [
   "Tiling loads a block into shared memory once and reuses it, raising "
   "arithmetic intensity by roughly the tile dimension — which moves "
   "the kernel past the ridge point.",
   "Shared memory has 32 banks; a column access of a 32&times;32 tile hits "
   "one bank and serialises. Padding to [T][T+1] fixes it.",
   "PCIe is roughly thirty times slower than GPU memory, so keep data "
   "resident and overlap what you must transfer.",
   "Asynchronous copies require pinned host memory — without it the "
   "copy is silently synchronous and nothing overlaps.",
   "Both compute and memory throughput low means latency-bound: the GPU is "
   "waiting rather than working.",
   "Optimise in order — correctness, coalescing, tiling, occupancy, "
   "divergence, streams — and then use the library anyway.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Shared memory and tiling"),
  ("callout", "Tiling turns a bandwidth problem into a compute problem",
   ["<b>Naive matrix multiply reads each element of A and B from global "
    "memory O(n) times.</b> Its arithmetic intensity is about 0.25 FLOP per "
    "byte (Module 07), which places it firmly on the bandwidth-bound side of "
    "the roofline — despite matrix multiply being the canonical "
    "arithmetic-heavy kernel.",
    "<b>Tiled matrix multiply loads a T&times;T tile of each operand into "
    "shared memory once</b>, and every thread in the block then reads it "
    "from shared memory, which is roughly twenty times faster and does not "
    "consume global bandwidth.",
    "<b>Arithmetic intensity rises with the tile dimension.</b> Each element "
    "loaded is used T times, so a 32&times;32 tile raises the intensity by "
    "roughly a factor of 32 — which carries the kernel well past the "
    "ridge point.",
    "<b>So exactly the same arithmetic becomes compute-bound.</b> <b>This is "
    "the clearest demonstration in the course that arithmetic intensity is "
    "something you change rather than something you have</b>, and it is why "
    "tiling is the canonical optimisation on every platform."]),
  ("code", """#define T 32
__shared__ float As[T][T], Bs[T][T];
float acc = 0.0f;
for (int t = 0; t < n/T; t++) {
    As[threadIdx.y][threadIdx.x] = A[row*n + t*T + threadIdx.x];
    Bs[threadIdx.y][threadIdx.x] = B[(t*T + threadIdx.y)*n + col];
    __syncthreads();                 // tile complete
    for (int k = 0; k < T; k++)
        acc += As[threadIdx.y][k] * Bs[k][threadIdx.x];
    __syncthreads();                 // before overwriting next iteration
}
C[row*n + col] = acc;"""),
  ("p", "<b>Both <code>__syncthreads()</code> calls are necessary.</b> The "
        "first ensures the tile is fully loaded before any thread reads it. "
        "<b>The second ensures every thread has finished reading before the "
        "next iteration overwrites it</b> — and this is the one that is "
        "routinely omitted, producing a race that appears only under load "
        "and only on some devices."),
  ("callout", "Bank conflicts serialise shared memory",
   ["<b>Shared memory is divided into 32 banks</b>, each of which can serve "
    "one access per cycle. Successive 32-bit words fall in successive banks.",
    "<b>If the 32 threads of a warp access 32 different banks, all are "
    "served in one cycle.</b> Full shared-memory bandwidth.",
    "<b>If they all access the same bank, the accesses serialise</b> "
    "— thirty-two cycles instead of one, for the same data. The "
    "hardware does this silently and the only symptom is that the kernel is "
    "slow.",
    "<b>Column-wise access of a T&times;T tile is the classic case.</b> "
    "With T = 32, elements of a column are 32 words apart, so every thread "
    "in a column maps to the same bank — a 32-way conflict on every "
    "access. <b>Declaring the array as [T][T+1] shifts each row by one "
    "word</b>, so a column spans all 32 banks and the conflict disappears "
    "entirely. <b>One character of padding, up to a 32&times; "
    "difference</b>, and it is worth measuring to believe."]),

  ("h1", "2 &nbsp; Transfers and streams"),
  ("callout", "PCIe is the bottleneck nobody budgets for",
   ["<b>GPU memory bandwidth is on the order of 1000 GB/s. PCIe is on the "
    "order of 30 GB/s.</b> A factor of roughly thirty, and the gap has "
    "widened over successive generations.",
    "<b>So transferring data to and from the device can cost more than the "
    "computation itself</b>, and for a single kernel over a modest dataset "
    "it frequently does. A kernel that is ten times faster than the CPU can "
    "lose outright once the round trip is counted.",
    "<b>The rule is to keep data resident on the device</b> and run many "
    "kernels against it, rather than transferring for each operation. "
    "Restructuring a pipeline so the data crosses PCIe once is usually worth "
    "more than any kernel optimisation.",
    "<b>And overlap what you genuinely must transfer</b> with computation, "
    "using streams. <b>A GPU result that beats the CPU on kernel time and "
    "loses once transfer is included is a common and dishonest claim</b>, "
    "and Project 2's comparison requirement exists partly to prevent it."]),
  ("code", """const int NS = 4;
for (int i = 0; i < nchunks; i++) {
    int k = i % NS;
    cudaMemcpyAsync(d_in+off, h_in+off, bytes, H2D, s[k]);
    kernel<<<grid, block, 0, s[k]>>>(d_in+off, d_out+off, m);
    cudaMemcpyAsync(h_out+off, d_out+off, bytes, D2H, s[k]);
}
// REQUIRES PINNED HOST MEMORY (cudaMallocHost)."""),
  ("callout", "Pinned memory is what makes asynchronous copies asynchronous",
   ["<b>Pageable host memory cannot be DMA'd directly</b>, because the "
    "operating system may move or swap the pages at any time.",
    "<b>So the driver stages the transfer through an internal pinned "
    "buffer</b> — copying from your pageable memory into its pinned "
    "buffer, then DMAing from there. <b>That staging copy is "
    "synchronous.</b>",
    "<b>Which means <code>cudaMemcpyAsync</code> from pageable memory is "
    "silently not asynchronous</b>, and a carefully constructed stream "
    "pipeline over pageable memory achieves no overlap at all while "
    "appearing correct.",
    "<b>Allocate host buffers with <code>cudaMallocHost</code></b> and the "
    "copies become genuine DMA transfers that overlap with computation. "
    "<b>The profiler shows the difference immediately</b> — the "
    "timeline either has overlapping bars or it does not — which is why "
    "profiling a stream pipeline is not optional."]),

  ("break",),
  ("h1", "3 &nbsp; Finding the limiting resource"),
  ("table", ["Profile symptom", "Limiting resource", "What helps"],
   [["<b>High memory throughput, low compute throughput</b>",
     "<b>Memory bandwidth.</b>",
     "<b>Tiling and shared memory</b> (&sect;1); reduce bytes moved; "
     "improve layout; use smaller data types."],
    ["<b>High compute, low memory</b>", "Compute.",
     "A better algorithm; lower precision where acceptable; tensor cores if "
     "the operation maps onto them."],
    ["<b>Both low</b>", "<b>Latency.</b>",
     "<b>The common beginner result</b> — the GPU is waiting rather "
     "than working. Raise occupancy, or increase instruction-level "
     "parallelism per thread (Module 08 &sect;3)."],
    ["<b>High warp divergence</b>", "Control flow.",
     "Reorganise the data so that warps are uniform (Module 08 &sect;1)."],
    ["<b>Low achieved bandwidth relative to peak</b>",
     "<b>Coalescing.</b>", "Fix the access pattern (Module 08 &sect;2)."],
    ["<b>Gaps between kernels on the timeline</b>",
     "Launch overhead or transfers.",
     "Fuse small kernels; use streams; check for implicit "
     "synchronisation."]],
   [0.30, 0.22, 0.48]),
  ("p", "Nsight Compute names the limiting resource directly in recent "
        "versions, which makes this table a cross-check rather than a "
        "diagnostic procedure — but knowing what the categories mean is "
        "still necessary to act on the report."),
  ("ol", ["<b>Correctness</b>, verified against a CPU implementation.",
          "<b>Coalescing.</b> Usually the single largest factor, and it is a "
          "data layout change rather than a code change (Module 08).",
          "<b>Shared memory tiling</b>, wherever there is data reuse to "
          "exploit (&sect;1).",
          "<b>Occupancy</b>, if and only if the profile indicates a "
          "latency-bound kernel.",
          "<b>Divergence</b>, if the profile indicates control flow is the "
          "limit.",
          "<b>Streams and transfer overlap</b> (&sect;2).",
          "<b>Instruction-level tuning</b> — last, and rarely "
          "necessary once the preceding six are done."]),
  ("p", "<b>Measure after each step.</b> Some interact — tiling changes "
        "the shared memory usage and therefore the occupancy — and some "
        "steps lose. <b>This mirrors Module 07's CPU ordering for the same "
        "reasons</b>, and performing the steps out of order wastes most of "
        "the effort."),
  ("callout", "Use the library",
   ["<b>cuBLAS, cuFFT, cuDNN, Thrust, and CUB are written by people with "
    "access to the architecture documentation</b>, and they are re-tuned for "
    "each device generation. Several of their kernels are generated by "
    "autotuners exploring configuration spaces no human would enumerate.",
    "<b>A hand-written tiled matrix multiply reaching 60% of cuBLAS is a "
    "good result</b> — and it took a week, and it will not be re-tuned "
    "when the next architecture ships.",
    "<b>Write your own in order to understand the machine.</b> This is "
    "genuinely necessary: you cannot read a profile or judge whether a "
    "library call is performing well without knowing what coalescing, "
    "occupancy, and divergence mean in practice. That is what this module "
    "is for.",
    "<b>And then use theirs.</b> <b>Project 2 requires the comparison "
    "precisely because reporting the gap honestly is the exercise</b> "
    "— the number is informative, and the instinct to present a "
    "hand-written kernel without the comparison is exactly what the "
    "requirement exists to prevent."]),
 ],
 "resources": [
   ("NVIDIA &mdash; CUDA C++ Best Practices Guide (free)",
    "https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/",
    "Coalescing, shared memory, bank conflicts, and streams, with the "
    "optimisation ordering of &sect;3."),
   ("NVIDIA &mdash; Nsight Compute documentation (free)",
    "https://docs.nvidia.com/nsight-compute/",
    "How to read the profile and what each metric means. The tool names the "
    "limiter; this explains it."),
   ("Mark Harris &mdash; Optimizing Parallel Reduction in CUDA (free)",
    "https://developer.download.nvidia.com/assets/cuda/files/reduction.pdf",
    "<b>Seven successive optimisations of one kernel, each measured.</b> "
    "The best worked example of &sect;3's methodology that exists, and it is "
    "thirty slides."),
   ("CUB and Thrust documentation (free)",
    "https://nvidia.github.io/cccl/",
    "The library primitives of &sect;3's recommendation, and the source is "
    "readable."),
 ],
 "exercises": [
   "Implement naive and tiled matrix multiply. Measure both, compute the "
   "arithmetic intensity of each, and place both on the roofline.",
   "Sweep the tile size from 8 to 32 and plot performance. Explain the "
   "shape, including the shared memory limit.",
   "<b>Produce a bank conflict</b> with a column access of a 32&times;32 "
   "tile, measure it, then pad to [32][33] and measure again.",
   "Omit the second <code>__syncthreads()</code> and construct a case where "
   "the result is wrong.",
   "Measure PCIe bandwidth in both directions, with pageable and with "
   "pinned host memory.",
   "Time a kernel with and without the transfer included and report both "
   "numbers for the same workload.",
   "Implement a four-stream pipeline and confirm the overlap in the "
   "profiler timeline. Then switch to pageable memory and confirm the "
   "overlap disappears.",
   "<b>Work through Mark Harris's reduction optimisations</b>, implementing "
   "and measuring each of the seven steps.",
   "Profile each version with Nsight Compute and record the limiting "
   "resource at each stage.",
   "<b>Benchmark your tiled matmul against cuBLAS</b> and report the "
   "percentage achieved.",
 ],
 "selfcheck": [
   "Why does tiling raise arithmetic intensity, and by roughly how much?",
   "Why are both <code>__syncthreads()</code> calls necessary?",
   "What is a bank conflict, what is the classic case, and what is the fix?",
   "Give the bandwidth ratio between GPU memory and PCIe, and the rule that "
   "follows.",
   "Why does an asynchronous copy require pinned memory?",
   "Give six profile symptoms and their limiting resources.",
   "What does 'both compute and memory low' indicate?",
   "Give the seven-step GPU optimisation order.",
   "Why write your own kernel, and why then use the library?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Distributed Memory and MPI",
 "subtitle": "When the data does not fit on one machine.",
 "question": "How do you compute across machines that share nothing?",
 "outcomes": [
     "Explain the message-passing model and when it is necessary.",
     "Use point-to-point and collective operations correctly.",
     "Model communication cost and reason about it.",
     "Overlap communication with computation.",
     "Decompose a domain with halo exchange.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The model",
   "blurb": "Separate address spaces, explicit messages."},

  {"t": "callout", "title": "Nothing is shared, which is a feature",
   "kind": "The model",
   "body": ["<b>Each process has its own memory.</b> There are no data "
            "races, because there is no shared data to race on.",
            "<b>All communication is explicit</b>, which means the "
            "communication cost is visible in the source rather than hidden "
            "in a cache miss.",
            "<b>That explicitness is why MPI programs often scale "
            "better</b> — you cannot accidentally communicate.",
            "<b>And it is the main reason to use it on one machine</b> "
            "too: the discipline of explicit data movement produces better "
            "decompositions than shared memory encourages."]},

  {"t": "table", "kicker": "When", "title": "When you actually need distributed memory",
   "header": ["Reason", "Assessment"],
   "widths": [4.0, 8.1],
   "rows": [
     ["<b>Data exceeds one machine's memory</b>", "<b>The legitimate reason. Not negotiable</b>"],
     ["Need more cores than one node has", "Legitimate, past a point"],
     ["<b>Fault tolerance</b>", "<b>Partly — MPI itself is not fault tolerant</b>"],
     ["Throughput on independent jobs", "<b>Use a job scheduler, not MPI</b>"],
     ["It seems more serious", "<b>No</b>"],
   ],
   "footnote": "<b>A single node with 2 TB of RAM and 128 cores handles a "
               "great deal</b> (CSCE 608 Module 13 made the same point).",
   "note": "The 'independent jobs' row matters — people write MPI for "
           "embarrassingly parallel work that a scheduler handles better."},

  {"t": "section", "label": "Part 2", "title": "Communication",
   "blurb": "Point to point, and collectives."},

  {"t": "code", "kicker": "MPI", "title": "The operations you need",
   "lang": "cpp", "code": """
MPI_Init(&argc, &argv);
MPI_Comm_rank(MPI_COMM_WORLD, &rank);
MPI_Comm_size(MPI_COMM_WORLD, &size);

// BLOCKING point to point. Simple, and it can deadlock:
//   if every rank MPI_Send's before any MPI_Recv's, and the
//   messages are too large to buffer, everyone blocks forever.
MPI_Send(buf, n, MPI_DOUBLE, dest, tag, MPI_COMM_WORLD);
MPI_Recv(buf, n, MPI_DOUBLE, src,  tag, MPI_COMM_WORLD, &status);

// NON-BLOCKING: post, compute, then wait. This is how you overlap.
MPI_Request req[2];
MPI_Irecv(ghost, n, MPI_DOUBLE, left,  0, comm, &req[0]);
MPI_Isend(edge,  n, MPI_DOUBLE, right, 0, comm, &req[1]);
compute_interior();                       // <-- overlapped
MPI_Waitall(2, req, MPI_STATUSES_IGNORE);
compute_boundary();                       // needs the ghost data

// COLLECTIVES: use these. They are optimised per topology.
MPI_Allreduce(&local, &global, 1, MPI_DOUBLE, MPI_SUM, comm);
""",
   "caption": "The non-blocking pattern — post, compute the interior, "
              "wait, compute the boundary — is the central idiom of "
              "the module.",
   "note": "This one code block contains most of what students need. The "
           "interior/boundary split is the key structure."},

  {"t": "callout", "title": "Use collectives rather than writing your own",
   "kind": "Why",
   "body": ["<b>A reduction implemented as a loop of point-to-point sends "
            "is O(n).</b> <code>MPI_Reduce</code> is O(log n) by tree.",
            "<b>And the implementation knows the network topology</b> "
            "— it uses different algorithms for shared memory, "
            "InfiniBand, and multi-rack, chosen at runtime.",
            "<b>Some use hardware offload</b> for reductions, which no "
            "hand-written version can reach.",
            "<b>So: Bcast, Reduce, Allreduce, Scatter, Gather, Alltoall, "
            "Barrier.</b> Learn them; they are almost always what you "
            "want."]},

  {"t": "eq", "kicker": "Cost", "title": "The communication cost model",
   "eqs": [
     ("T = α + n·β",
      "Latency plus bytes over bandwidth. α is per-message; β is "
      "per-byte."),
     ("α ≈ 1–10 μs,  1/β ≈ 10–200 GB/s",
      "Typical for a modern interconnect. The latency dominates for small "
      "messages."),
     ("n* = α / β  —  the message size where they are equal",
      "Below it you are latency-bound; above, bandwidth-bound. Usually a "
      "few kilobytes."),
   ],
   "caption": "<b>Send fewer, larger messages.</b> The latency term is paid "
              "per message regardless of size.",
   "note": "The crossover size is the practical number — it tells you "
           "when aggregation pays."},

  {"t": "section", "label": "Part 3", "title": "Domain decomposition",
   "blurb": "The standard structure."},

  {"t": "callout", "title": "Halo exchange: the surface-to-volume argument",
   "kind": "Why decomposition shape matters",
   "body": ["<b>Each process owns a subdomain and needs a layer of its "
            "neighbours' boundary values</b> — the halo, or ghost "
            "cells.",
            "<b>Computation scales with the volume; communication scales "
            "with the surface.</b>",
            "<b>So the ratio improves as the subdomain grows</b> — which "
            "is exactly why weak scaling works and strong scaling degrades "
            "(Module 01).",
            "<b>And it is why 3D decomposition beats 1D:</b> slicing a cube "
            "into slabs gives far more surface per process than cutting it "
            "into cubes. <b>For large process counts the difference is "
            "substantial.</b>"]},

  {"t": "table", "kicker": "Shape", "title": "Decomposition shape and communication volume",
   "header": ["Decomposition", "Surface per process", "At p=1000"],
   "widths": [3.2, 4.4, 4.5],
   "rows": [
     ["1D slabs", "2n²", "<b>Large — constant in p</b>"],
     ["2D columns", "4n²/√p", "Better"],
     ["<b>3D blocks</b>", "<b>6n²/p^(2/3)</b>", "<b>Best by a wide margin</b>"],
   ],
   "footnote": "<b>At 1000 processes on an n³ grid, 3D decomposition "
               "moves roughly an order of magnitude less data</b> than 1D.",
   "note": "The asymptotic difference is the reason production codes all "
           "use 3D decomposition despite the extra bookkeeping."},

  {"t": "callout", "title": "Overlap, and measure whether it worked",
   "kind": "The practical point",
   "body": ["<b>Post the non-blocking receives, compute the interior, wait, "
            "then compute the boundary.</b> The interior computation covers "
            "the communication.",
            "<b>But posting a non-blocking send does not mean progress is "
            "being made.</b> Many MPI implementations only advance the "
            "transfer inside MPI calls.",
            "<b>So the overlap may not happen</b>, and the code looks "
            "correct either way.",
            "<b>Measure it</b> — time the interior computation with and "
            "without the outstanding communication. If they are the same, "
            "nothing overlapped."]},
 ],
 "takeaways": [
   "Each process has its own memory and all communication is explicit, so "
   "there are no data races and the communication cost is visible in the "
   "source.",
   "The legitimate reason for distributed memory is data that exceeds one "
   "machine; independent jobs want a scheduler, not MPI.",
   "Blocking sends can deadlock when every rank sends before receiving and "
   "the messages are too large to buffer.",
   "Use collectives — they are O(log n), topology-aware, and sometimes "
   "hardware-offloaded.",
   "Communication costs &alpha; + n&beta;: send fewer, larger messages, "
   "because the latency term is paid per message.",
   "Computation scales with volume and communication with surface, which is "
   "why 3D decomposition beats 1D and why weak scaling works.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The message-passing model"),
  ("callout", "Nothing is shared, which is a feature",
   ["<b>Each process has its own private address space.</b> There are no "
    "data races, no memory model subtleties, and no false sharing, because "
    "there is no shared data at all — Modules 03 through 05 simply do "
    "not apply between processes.",
    "<b>All communication is explicit.</b> Every byte that moves between "
    "processes appears as a call in the source code, which makes the "
    "communication cost <i>visible</i> rather than hidden inside a cache "
    "miss or a coherence transaction.",
    "<b>That explicitness is a substantial part of why MPI programs "
    "frequently scale better than shared-memory ones</b> — you cannot "
    "accidentally communicate, so the decomposition has to be thought "
    "through before the program runs at all.",
    "<b>And it is a reasonable argument for using MPI on a single machine "
    "too.</b> The discipline of explicit data movement tends to produce "
    "better decompositions than shared memory encourages, where it is easy "
    "to share by default and discover the cost later."]),
  ("table", ["Reason given", "Assessment"],
   [["<b>The data does not fit in one machine's memory.</b>",
     "<b>The legitimate reason, and not negotiable.</b> If the working set "
     "is ten terabytes, no amount of single-node tuning helps."],
    ["<b>More cores are needed than one node provides.</b>",
     "Legitimate past a point — though a modern node has 128 cores and "
     "the Amdahl analysis of Module 01 should be done first."],
    ["<b>Fault tolerance.</b>",
     "<b>Partly, and be careful</b> — standard MPI is <i>not</i> fault "
     "tolerant. A single process failure aborts the job, and checkpointing "
     "is the usual answer rather than anything MPI provides."],
    ["<b>Throughput across many independent jobs.</b>",
     "<b>Use a job scheduler, not MPI.</b> Embarrassingly parallel work "
     "needs no communication, and writing it in MPI adds complexity for "
     "nothing. <b>This is a common mistake.</b>"],
    ["<b>It seems more serious.</b>", "<b>No.</b>"]],
   [0.33, 0.67]),
  ("p", "<b>A single node with two terabytes of memory and 128 cores "
        "handles a great deal</b>, and CSCE 608's Module 13 made exactly "
        "this argument about distributed databases. The reflex to distribute "
        "is costly and frequently unexamined."),

  ("h1", "2 &nbsp; Communication"),
  ("code", """// BLOCKING -- simple, and can deadlock if every rank sends first
MPI_Send(buf, n, MPI_DOUBLE, dest, tag, comm);
MPI_Recv(buf, n, MPI_DOUBLE, src,  tag, comm, &status);

// NON-BLOCKING -- post, compute, wait. This is how you overlap.
MPI_Irecv(ghost, n, MPI_DOUBLE, left,  0, comm, &req[0]);
MPI_Isend(edge,  n, MPI_DOUBLE, right, 0, comm, &req[1]);
compute_interior();                    // overlapped with the transfer
MPI_Waitall(2, req, MPI_STATUSES_IGNORE);
compute_boundary();                    // needs the ghost data

// COLLECTIVES -- use these
MPI_Allreduce(&local, &global, 1, MPI_DOUBLE, MPI_SUM, comm);"""),
  ("p", "<b>The blocking deadlock is worth understanding.</b> If every rank "
        "calls <code>MPI_Send</code> before any calls <code>MPI_Recv</code>, "
        "and the messages are large enough that the implementation cannot "
        "buffer them, every rank blocks waiting for a matching receive that "
        "nobody has posted. <b>It works for small messages and deadlocks for "
        "large ones</b>, which makes it a particularly unpleasant bug to "
        "encounter in production."),
  ("callout", "Use collectives rather than writing your own",
   ["<b>A reduction written as a loop of point-to-point sends to rank 0 is "
    "O(p).</b> <code>MPI_Reduce</code> is O(log p), using a tree.",
    "<b>And the implementation knows the network topology.</b> It selects "
    "between different algorithms at runtime depending on message size, "
    "process count, and whether the ranks are on the same node, the same "
    "switch, or across racks — decisions you cannot easily replicate "
    "and would have to revisit on every new machine.",
    "<b>Some interconnects offload reductions into the network hardware</b>, "
    "performing the combination in the switches as the data passes through. "
    "No hand-written implementation can reach that.",
    "<b>So learn the set:</b> <code>Bcast</code>, <code>Reduce</code>, "
    "<code>Allreduce</code>, <code>Scatter</code>, <code>Gather</code>, "
    "<code>Allgather</code>, <code>Alltoall</code>, <code>Barrier</code>, "
    "and the scan variants. <b>They are almost always what you want</b>, and "
    "recognising which collective a piece of communication is turns out to "
    "be most of the design work."]),
  ("eq", "T = &alpha; + n&beta; &nbsp;&nbsp;&nbsp;&nbsp; "
         "n* = &alpha;/&beta;"),
  ("p", "where &alpha; is the per-message latency and &beta; the per-byte "
        "cost. Typical modern figures are &alpha; of 1 to 10 microseconds "
        "and bandwidth of 10 to 200 GB/s. <b>The crossover message size "
        "n* — where latency and bandwidth contribute equally — is "
        "usually a few kilobytes.</b> Below it you are latency-bound and "
        "aggregating messages pays; above it you are bandwidth-bound and "
        "reducing bytes pays. <b>Send fewer, larger messages</b>, because "
        "&alpha; is charged per message regardless of size."),

  ("break",),
  ("h1", "3 &nbsp; Domain decomposition and halo exchange"),
  ("callout", "The surface-to-volume argument",
   ["<b>Each process owns a subdomain of the problem and needs a layer of "
    "its neighbours' boundary values</b> to compute its own boundary "
    "— the <b>halo</b> or ghost cells. Each timestep, the halos are "
    "exchanged.",
    "<b>Computation scales with the volume of the subdomain; communication "
    "scales with its surface.</b> This single observation governs the "
    "scaling behaviour of essentially every grid-based parallel "
    "application.",
    "<b>So the communication-to-computation ratio improves as the subdomain "
    "grows</b> — which is exactly why weak scaling works well "
    "(subdomains stay the same size) and strong scaling degrades (subdomains "
    "shrink, so surface comes to dominate volume). <b>Module 01's two laws, "
    "explained by geometry.</b>",
    "<b>And it is why the decomposition's shape matters.</b> Slicing a cube "
    "into flat slabs gives each process two large faces; cutting it into "
    "small cubes gives six small ones, with far less total area."]),
  ("table", ["Decomposition", "Surface area per process", "Behaviour at "
             "large p"],
   [["<b>1D slabs</b>", "2n&#178; — two faces, each the full cross "
     "section.",
     "<b>Constant in p.</b> The communication volume per process does not "
     "fall at all as processes are added, so it rapidly dominates."],
    ["<b>2D columns</b>", "4n&#178;/&radic;p",
     "Falls as p<super>&minus;1/2</super>. Considerably better."],
    ["<b>3D blocks</b>", "<b>6n&#178;/p<super>2/3</super></b>",
     "<b>Falls as p<super>&minus;2/3</super> — best by a wide "
     "margin.</b> At a thousand processes on an n&#179; grid this moves "
     "roughly an order of magnitude less data than 1D."]],
   [0.20, 0.36, 0.44]),
  ("p", "<b>This is why every production grid code uses 3D decomposition</b> "
        "despite the additional bookkeeping — twenty-six neighbours "
        "rather than two, and corner and edge halos as well as faces. The "
        "asymptotic difference is decisive at scale."),
  ("callout", "Overlap, and then measure whether it actually happened",
   ["<b>The standard idiom:</b> post the non-blocking receives and sends, "
    "compute the <i>interior</i> of the subdomain (which needs no halo "
    "data), wait for the transfers, then compute the <i>boundary</i>. The "
    "interior computation covers the communication latency.",
    "<b>But posting a non-blocking operation does not guarantee that "
    "progress is being made on it.</b> Many MPI implementations only advance "
    "transfers while inside an MPI call — there is no background thread "
    "— so a long stretch of pure computation may see no progress at "
    "all, and the entire transfer happens inside the <code>Waitall</code>.",
    "<b>So the overlap may simply not occur</b>, and the code is correct "
    "and well-structured either way. Nothing in the source distinguishes the "
    "two cases.",
    "<b>Measure it.</b> Time the interior computation with outstanding "
    "communication and without. <b>If the two are the same, nothing "
    "overlapped</b> — and the remedies are implementation-specific: "
    "enabling asynchronous progress threads, calling <code>MPI_Test</code> "
    "periodically during the computation, or accepting it."]),
 ],
 "resources": [
   ("Eijkhout &mdash; Parallel Programming in MPI and OpenMP (free book)",
    "https://theartofhpc.com/",
    "Free, thorough, and the best single reference for this module. The "
    "exercises are good."),
   ("MPI Standard and the MPICH / OpenMPI documentation (free)",
    "https://www.mpi-forum.org/",
    "The specification, plus two implementations' guides. The collectives "
    "chapter is worth reading in full."),
   ("Hoefler et al. &mdash; performance modelling and MPI work (free)",
    "https://htor.inf.ethz.ch/publications/",
    "The cost model of &sect;2 and measurement methodology, from a group "
    "that is unusually rigorous about both."),
   ("Grama, Gupta, Karypis & Kumar &mdash; Introduction to Parallel "
    "Computing",
    "https://www-users.cse.umn.edu/~karypis/parbook/",
    "The decomposition analysis of &sect;3, with the surface-to-volume "
    "derivations done properly."),
 ],
 "exercises": [
   "Write an MPI hello-world, then a ring communication, and confirm both "
   "run across multiple processes.",
   "<b>Construct the blocking deadlock:</b> have every rank send before "
   "receiving, and increase the message size until it hangs. Report the "
   "threshold.",
   "Implement a reduction with point-to-point messages and compare against "
   "<code>MPI_Reduce</code> at 4, 16, and 64 processes.",
   "Measure &alpha; and &beta; for your interconnect by timing messages of "
   "many sizes. Fit the model and compute n*.",
   "Implement 1D and 3D domain decomposition for a 3D stencil. Measure the "
   "communication volume per process for each at several process counts.",
   "Implement halo exchange with blocking and with non-blocking "
   "communication, and compare.",
   "<b>Measure whether your overlap actually occurred</b> by timing the "
   "interior computation with and without outstanding communication.",
   "Run a strong scaling study and a weak scaling study on the same stencil "
   "code and explain the difference using the surface-to-volume argument.",
   "Take a problem you solved with threads in Project 1 and estimate "
   "honestly whether MPI would help.",
 ],
 "selfcheck": [
   "What does the message-passing model provide, and what does its "
   "explicitness buy?",
   "Give five reasons people distribute and assess each.",
   "How does a blocking send deadlock, and why is it size-dependent?",
   "Give three reasons to use collectives rather than hand-written "
   "communication.",
   "State the communication cost model and the crossover message size.",
   "Explain the surface-to-volume argument and what it says about weak and "
   "strong scaling.",
   "Compare 1D, 2D, and 3D decomposition on communication volume.",
   "Describe the overlap idiom and say why it may not work.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Parallel Algorithms",
 "subtitle": "The primitives, and the one that surprises everyone.",
 "question": "What does a parallel algorithm look like?",
 "outcomes": [
     "Analyse an algorithm by work and depth.",
     "Implement parallel reduction and scan.",
     "Explain why scan is parallelisable despite appearing sequential.",
     "Implement parallel sorting.",
     "Explain the limits of the PRAM model.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Work and depth",
   "blurb": "The right complexity measures."},

  {"t": "eq", "kicker": "Analysis", "title": "Two measures, not one",
   "eqs": [
     ("W  —  work: total operations, over all processors",
      "What the serial algorithm would do. Should be close to the best "
      "serial complexity."),
     ("D  —  depth (span): the longest chain of dependencies",
      "The time on infinitely many processors. The fundamental limit on "
      "parallelism."),
     ("T_p  ≤  W/p + D        (Brent's theorem)",
      "Running time on p processors is bounded by the work divided among "
      "them, plus the depth."),
   ],
   "caption": "<b>W/D is the available parallelism.</b> A low-depth "
              "algorithm with high work may lose to a high-depth one with "
              "low work.",
   "note": "Work-efficiency matters as much as depth — an algorithm doing "
           "n log n work to achieve log n depth often loses in practice."},

  {"t": "callout", "title": "Work-efficiency matters as much as depth",
   "kind": "The trade people get wrong",
   "body": ["<b>An algorithm with O(log n) depth and O(n log n) work</b> "
            "does more total operations than the serial O(n) version.",
            "<b>So at modest processor counts it loses</b>, and the "
            "crossover may be beyond any machine you have.",
            "<b>A work-efficient parallel algorithm does O(n) work</b> and "
            "accepts somewhat more depth.",
            "<b>Both scan formulations below illustrate this</b> — "
            "Hillis–Steele is simpler and does O(n log n) work; "
            "Blelloch is work-efficient at twice the depth. <b>Blelloch "
            "usually wins.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Reduce and scan",
   "blurb": "Two primitives, one surprising."},

  {"t": "callout", "title": "Reduction is an obvious tree",
   "kind": "The easy case",
   "body": ["<b>Combine pairs, then pairs of results, recursively.</b> "
            "O(n) work, O(log n) depth.",
            "<b>Requires associativity</b> (Module 06) and nothing else.",
            "<b>In practice:</b> each thread reduces a contiguous chunk "
            "serially, then the per-thread results are combined by tree.",
            "<b>This two-level structure is what every real "
            "implementation does</b> — the serial phase has perfect "
            "locality and no synchronisation, and the tree phase is "
            "short."]},

  {"t": "code", "kicker": "Scan", "title": "The prefix sum, which looks sequential",
   "lang": "text", "code": """
  INPUT:    3  1  7  0  4  1  6  3
  OUTPUT:   3  4 11 11 15 16 22 25      (inclusive prefix sums)

  Each output DEPENDS ON ALL PREVIOUS INPUTS. It looks like the
  definition of a sequential computation. It is not.

  HILLIS-STEELE  (simple, O(n log n) work, O(log n) depth):
    for d = 1, 2, 4, 8, ...:
        in parallel: x[i] += x[i - d]      for i >= d
    After log n rounds every element has accumulated everything
    to its left. Each round doubles the reach.

  BLELLOCH  (work-efficient, O(n) work, 2 log n depth):
    UP-SWEEP:   build a reduction tree, storing partial sums
    DOWN-SWEEP: push prefixes back down the same tree
    Two passes over the tree, O(n) total operations.
""",
   "caption": "Hillis–Steele is easier to write; Blelloch does less "
              "work and usually wins in practice.",
   "note": "The doubling-reach intuition for Hillis-Steele is what makes "
           "the result believable."},

  {"t": "callout", "title": "Scan is the most useful primitive in parallel computing",
   "kind": "Why it matters so much",
   "body": ["<b>Stream compaction:</b> scan a 0/1 flag array, and each "
            "surviving element's prefix sum <i>is</i> its output index.",
            "<b>Sorting:</b> radix sort is a sequence of scans over "
            "digit-bucket flags.",
            "<b>Allocation:</b> variable-sized outputs — scan the sizes "
            "to get each thread's offset.",
            "<b>Sparse matrix formats, quicksort partitioning, run-length "
            "encoding, building acceleration structures</b> — all scans.",
            "<b>If a problem looks sequential because of a running "
            "total, it is probably a scan.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Sorting",
   "blurb": "The standard parallel sorts."},

  {"t": "table", "kicker": "Sorting", "title": "Parallel sorting algorithms",
   "header": ["Algorithm", "Approach", "Suits"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["<b>Sample sort</b>", "Sample to pick splitters, bucket, sort locally", "<b>Distributed memory</b>"],
     ["<b>Radix sort</b>", "Repeated scan over digit buckets", "<b>GPU — no comparisons, no divergence</b>"],
     ["Bitonic sort", "A fixed comparison network", "<b>Fixed structure; O(n log²n) work</b>"],
     ["Parallel merge sort", "Merge pairs in parallel", "Shared memory; merging is the hard part"],
     ["Parallel quicksort", "Partition by scan, recurse", "Good average case; pivot sensitivity"],
   ],
   "footnote": "<b>Radix sort dominates on GPUs</b> because it is a "
               "sequence of scans and has no data-dependent branching.",
   "note": "That radix sort is just repeated scan ties Part 3 back to "
           "Part 2 nicely."},

  {"t": "callout", "title": "Merging is harder to parallelise than sorting",
   "kind": "The non-obvious difficulty",
   "body": ["<b>Merging two sorted sequences looks trivially "
            "sequential</b> — compare the heads and advance.",
            "<b>The parallel version uses a co-rank computation:</b> for "
            "output position k, binary search to find how many elements come "
            "from each input.",
            "<b>Then each thread merges an independent segment</b>, with no "
            "communication at all.",
            "<b>So the merge becomes O(log n) depth</b> — and this is the "
            "step that makes parallel merge sort work."]},

  {"t": "section", "label": "Part 4", "title": "Models and reality",
   "blurb": "What the theory leaves out."},

  {"t": "callout", "title": "PRAM is a useful fiction",
   "kind": "The model and its limits",
   "body": ["<b>The PRAM model assumes p processors sharing memory with "
            "uniform unit-cost access.</b>",
            "<b>It is useful for reasoning about work and depth</b> and for "
            "proving lower bounds.",
            "<b>And it omits everything that matters in practice:</b> "
            "memory hierarchy, bandwidth limits, synchronisation cost, and "
            "communication latency.",
            "<b>So a PRAM-optimal algorithm may be a poor practical "
            "one.</b> Use work and depth as a guide and then measure "
            "— which is Module 07's discipline, applied to algorithms."]},

  {"t": "bullets", "kicker": "Better models", "title": "Models that account for the machine",
   "items": [
     "<b>External memory model:</b> counts block transfers between a fast "
     "and slow level. Predicts cache behaviour.",
     "",
     "<b>Cache-oblivious:</b> algorithms optimal at every level of a "
     "hierarchy without knowing the parameters. Elegant and real.",
     "",
     "<b>BSP:</b> supersteps of computation separated by communication and "
     "a barrier. Models distributed memory well.",
     "",
     "<b>LogP:</b> latency, overhead, gap, processors — a more detailed "
     "communication model.",
     "",
     "<b>And the roofline</b> (Module 07), which is the most practical of "
     "all of them.",
   ],
   "footnote": "<b>Each model exists because a simpler one mispredicted "
               "something.</b>"},
 ],
 "takeaways": [
   "Analyse by work (total operations) and depth (longest dependency chain); "
   "Brent's theorem bounds the time by W/p + D.",
   "Work-efficiency matters as much as depth — an O(n log n) work "
   "algorithm may never beat the serial one on a real machine.",
   "Reduction is a tree requiring only associativity; in practice each "
   "thread reduces a chunk serially and the results combine by tree.",
   "Scan looks inherently sequential and is not — Hillis–Steele "
   "doubles the reach each round; Blelloch is work-efficient at twice the "
   "depth.",
   "Scan is the most useful parallel primitive: compaction, radix sort, "
   "variable-size allocation, and sparse formats are all scans.",
   "PRAM is useful for work and depth and omits memory hierarchy, "
   "bandwidth, and communication — so a PRAM-optimal algorithm may be "
   "a poor practical one.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Work and depth"),
  ("table", ["Measure", "Definition", "Interpretation"],
   [["<b>Work, W</b>", "The total number of operations performed, summed "
     "over all processors.",
     "What the computation costs in total. <b>Should be close to the best "
     "serial complexity</b>, or the algorithm is wasting effort."],
    ["<b>Depth (span), D</b>",
     "The length of the longest chain of dependent operations.",
     "<b>The running time on infinitely many processors</b> — the "
     "fundamental limit on how much parallelism the algorithm admits."],
    ["<b>W/D</b>", "The ratio.",
     "<b>The available parallelism.</b> If W/D is 1000, there is no point "
     "using more than about 1000 processors."]],
   [0.17, 0.37, 0.46]),
  ("eq", "T<sub>p</sub> &le; W/p + D &nbsp;&nbsp;&nbsp;(Brent's theorem)"),
  ("p", "The running time on p processors is bounded by the work divided "
        "among them plus the depth. <b>The two terms correspond to the two "
        "ways an algorithm can fail to scale</b>: too much work, or too long "
        "a critical path."),
  ("callout", "Work-efficiency matters as much as depth",
   ["<b>An algorithm with O(log n) depth and O(n log n) work performs more "
    "total operations than the serial O(n) algorithm it replaces.</b> It is "
    "not work-efficient.",
    "<b>So at modest processor counts it loses to the serial version</b>, "
    "and the crossover point — where the parallelism outweighs the "
    "extra work — may lie beyond any machine you have access to.",
    "<b>A work-efficient parallel algorithm performs O(n) work</b>, "
    "asymptotically matching the serial version, and accepts somewhat "
    "greater depth in exchange.",
    "<b>The two scan formulations in &sect;2 illustrate this exactly.</b> "
    "Hillis&ndash;Steele is simpler and does O(n log n) work at O(log n) "
    "depth; Blelloch does O(n) work at twice the depth. <b>Blelloch usually "
    "wins in practice</b>, which is the opposite of what a depth-only "
    "analysis suggests, and it is why both measures are needed."]),

  ("h1", "2 &nbsp; Reduce and scan"),
  ("callout", "Reduction is an obvious tree",
   ["<b>Combine adjacent pairs, then pairs of those results, and so on.</b> "
    "O(n) work and O(log n) depth, which is optimal on both counts.",
    "<b>It requires only that the operator be associative</b> (Module 06 "
    "&sect;3), with the floating-point caveat that follows from that.",
    "<b>In practice, implementations are two-level:</b> each thread reduces "
    "a contiguous chunk serially, and then the per-thread results are "
    "combined by tree.",
    "<b>This structure is what every real implementation does</b>, and for "
    "good reasons: the serial phase has perfect cache locality, requires no "
    "synchronisation, and uses no atomics, while the tree phase is over only "
    "p elements and is correspondingly short. The pure tree is the "
    "theoretical form; the hybrid is the useful one."]),
  ("code", """INPUT:   3  1  7  0  4  1  6  3
OUTPUT:  3  4 11 11 15 16 22 25      (inclusive prefix sums)

HILLIS-STEELE  (simple; O(n log n) work, O(log n) depth):
  for d = 1, 2, 4, 8, ...:
      in parallel: x[i] += x[i-d]   for i >= d
  Each round DOUBLES the reach; after log n rounds every element
  has accumulated everything to its left.

BLELLOCH  (work-efficient; O(n) work, 2 log n depth):
  UP-SWEEP:   build a reduction tree, storing partial sums
  DOWN-SWEEP: push prefixes back down the same tree"""),
  ("p", "<b>Every output depends on all previous inputs</b>, which makes "
        "scan look like the definition of a sequential computation. <b>The "
        "doubling-reach intuition is what makes the parallel result "
        "believable:</b> after the first round each element holds the sum of "
        "itself and its neighbour; after the second, of four elements; after "
        "the third, of eight. Logarithmically many rounds suffice."),
  ("callout", "Scan is the most useful primitive in parallel computing",
   ["<b>Stream compaction.</b> Given a 0/1 flag per element, scan the "
    "flags — and each surviving element's exclusive prefix sum "
    "<i>is</i> its index in the compacted output. Filtering becomes a scan "
    "plus a scatter.",
    "<b>Radix sort.</b> Each pass is a scan over digit-bucket flags to "
    "compute destination offsets, followed by a scatter. <b>The whole sort "
    "is a sequence of scans</b> (&sect;3).",
    "<b>Variable-sized output allocation.</b> When each thread produces a "
    "different number of results, scan the counts to give every thread its "
    "output offset — with no atomics and no contention.",
    "<b>And a great deal more:</b> sparse matrix format construction, "
    "quicksort partitioning, run-length encoding and decoding, building "
    "acceleration structures (CSCE 647 Module 04), polynomial evaluation, "
    "and recurrence solving.",
    "<b>If a problem looks inherently sequential because of a running "
    "total, it is probably a scan.</b> That recognition is one of the most "
    "valuable things in this course."]),

  ("break",),
  ("h1", "3 &nbsp; Sorting"),
  ("table", ["Algorithm", "Approach", "Suits"],
   [["<b>Sample sort</b>",
     "Sample the data to choose splitters, bucket every element by splitter, "
     "then sort each bucket locally.",
     "<b>Distributed memory.</b> One all-to-all communication and then "
     "independent local sorts — which maps perfectly onto MPI."],
    ["<b>Radix sort</b>",
     "For each digit, scan the bucket flags to compute offsets and scatter.",
     "<b>GPUs.</b> No comparisons, no data-dependent branching, hence no "
     "divergence (Module 08), and it is built entirely from scans and "
     "scatters. <b>The dominant GPU sort.</b>"],
    ["<b>Bitonic sort</b>",
     "A fixed network of compare-exchange operations, independent of the "
     "data.",
     "Hardware and fixed-structure settings. <b>O(n log&#178;n) work</b> "
     "— not work-efficient — and its complete regularity is "
     "sometimes worth that."],
    ["<b>Parallel merge sort</b>",
     "Sort segments locally, then merge pairs in parallel.",
     "Shared memory. <b>The merge is the hard part</b> — see below."],
    ["<b>Parallel quicksort</b>",
     "Partition by scan, then recurse on both halves in parallel.",
     "Good average case; sensitive to pivot choice, as serially."]],
   [0.17, 0.38, 0.45]),
  ("callout", "Merging is harder to parallelise than sorting",
   ["<b>Merging two sorted sequences appears trivially sequential:</b> "
    "compare the heads, emit the smaller, advance. Each decision depends on "
    "the previous one.",
    "<b>The parallel formulation uses a co-rank computation.</b> For a "
    "given output position k, binary search to determine how many of the "
    "first k output elements come from sequence A and how many from B "
    "— which is determined by the data and can be found independently "
    "for any k.",
    "<b>Then each thread merges an independent segment</b>, from its "
    "computed starting positions in both inputs, with no communication and "
    "no dependence on any other thread.",
    "<b>So the merge becomes O(log n) depth</b> — the binary search "
    "— rather than O(n). <b>This is the step that makes parallel merge "
    "sort work</b>, and it is a good example of a problem whose sequential "
    "appearance conceals an independent-subproblem structure, exactly as "
    "scan does."]),

  ("h1", "4 &nbsp; Models and their limits"),
  ("callout", "PRAM is a useful fiction",
   ["<b>The PRAM model posits p processors sharing a single memory, with "
    "uniform unit-cost access and perfect synchrony.</b> Variants differ in "
    "whether concurrent reads and writes are permitted.",
    "<b>It is genuinely useful</b> for reasoning about work and depth, for "
    "proving lower bounds, and for establishing that a problem is "
    "parallelisable at all — the scan result of &sect;2 is a PRAM "
    "result.",
    "<b>And it omits essentially everything that determines practical "
    "performance:</b> the memory hierarchy, finite bandwidth, cache "
    "coherence traffic, synchronisation cost, communication latency, and "
    "load imbalance. Every one of those has been a module of this course.",
    "<b>So a PRAM-optimal algorithm may be a poor practical choice</b>, and "
    "frequently is. <b>Use work and depth as a guide, then measure</b> "
    "— which is Module 07's discipline applied at the level of "
    "algorithm selection rather than code tuning."]),
  ("ul", ["<b>The external memory model</b> counts block transfers between a "
          "fast small level and a slow large one. It predicts cache and I/O "
          "behaviour that PRAM cannot see, and it is why B-trees "
          "(CSCE 608 Module 03) have the shape they do.",
          "<b>Cache-oblivious algorithms</b> achieve optimal transfer counts "
          "at <i>every</i> level of a hierarchy without knowing any of its "
          "parameters — typically by recursive subdivision. Elegant, "
          "and genuinely practical.",
          "<b>BSP (bulk synchronous parallel)</b> structures a computation "
          "as supersteps of local computation separated by communication and "
          "a barrier, and assigns costs to each. <b>Models distributed "
          "memory well</b> and underlies several graph processing systems.",
          "<b>LogP</b> models communication with four parameters — "
          "latency, overhead, gap, and processor count — capturing the "
          "distinction between network latency and the per-message CPU cost, "
          "which &alpha;&beta; (Module 10) conflates.",
          "<b>And the roofline</b> (Module 07), which is the least "
          "theoretically ambitious and the most practically useful of all of "
          "them. <b>Each of these models exists because a simpler one "
          "mispredicted something important.</b>"]),
 ],
 "resources": [
   ("Blelloch &mdash; Prefix Sums and Their Applications (free)",
    "https://www.cs.cmu.edu/~guyb/papers/Ble93.pdf",
    "<b>The scan paper.</b> The work-efficient algorithm and a long list of "
    "applications. Read it — it changes how you see sequential-looking "
    "problems."),
   ("Harris, Sengupta & Owens &mdash; Parallel Prefix Sum (Scan) with CUDA "
    "(free)",
    "https://developer.nvidia.com/gpugems/gpugems3/part-vi-gpu-computing/chapter-39-parallel-prefix-sum-scan-cuda",
    "Both scan formulations implemented and measured on a GPU, including "
    "the bank conflict handling from Module 09."),
   ("Stanford CS149 &mdash; parallel algorithms lectures (free)",
    "https://gfxcourses.stanford.edu/cs149/",
    "Work and depth analysis with worked examples."),
   ("JaJa &mdash; An Introduction to Parallel Algorithms",
    "https://www.pearson.com/en-us/subject-catalog/p/introduction-to-parallel-algorithms-an/P200000003351",
    "The PRAM-theoretic treatment. Library copy; useful for the lower "
    "bounds and the formal analysis."),
 ],
 "exercises": [
   "Analyse three algorithms you know by work and depth, and compute the "
   "available parallelism of each.",
   "Implement a tree reduction and a two-level reduction. Measure both and "
   "explain the difference.",
   "Implement Hillis–Steele scan and count the operations. Confirm it "
   "is O(n log n).",
   "Implement Blelloch scan and confirm it is O(n). <b>Measure both at "
   "several sizes and thread counts and find where each wins.</b>",
   "<b>Implement stream compaction using scan</b> and compare against a "
   "serial filter.",
   "Implement variable-size output allocation with a scan, and compare "
   "against using an atomic counter.",
   "Implement radix sort as a sequence of scans and scatters.",
   "Implement parallel merge using co-rank and verify it against a serial "
   "merge.",
   "Benchmark your sort against <code>std::sort</code> and against a "
   "library parallel sort. Report both.",
   "Find a problem in your own code that looks sequential because of a "
   "running total, and reformulate it as a scan.",
 ],
 "selfcheck": [
   "Define work and depth, and state Brent's theorem.",
   "What is available parallelism, and why does work-efficiency matter as "
   "much as depth?",
   "Why is reduction a tree, and what do real implementations do instead?",
   "Why does scan look sequential, and what is the doubling-reach "
   "intuition?",
   "Compare Hillis–Steele and Blelloch on work and depth.",
   "Name five applications of scan.",
   "Name five parallel sorts and say what each suits.",
   "Why is merging hard to parallelise, and what is the co-rank trick?",
   "What does PRAM assume, what does it omit, and what follows?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Patterns, Frameworks, and Portability",
 "subtitle": "Writing it once and running it anywhere.",
 "question": "Can you write parallel code that outlives one machine?",
 "outcomes": [
     "Apply the standard parallel patterns as a design vocabulary.",
     "Compare the major portability frameworks.",
     "Explain what performance portability means and costs.",
     "Choose a framework from the constraints.",
     "Explain why parallel code ages badly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Patterns as vocabulary",
   "blurb": "Recognising the shape of a computation."},

  {"t": "callout", "title": "Most parallel code is a composition of six patterns",
   "kind": "Why this is useful",
   "body": ["<b>Map, reduce, scan, stencil, gather/scatter, and "
            "partition</b> (Module 06) cover the overwhelming majority of "
            "parallel computation.",
            "<b>Recognising the pattern gives you the algorithm</b>, the "
            "work and depth, the known pitfalls, and usually a library "
            "implementation.",
            "<b>And it gives you a vocabulary for design discussions</b> "
            "that is more precise than 'parallelise the loop'.",
            "<b>Composition is where the engineering is:</b> a fused "
            "map-reduce avoids materialising the intermediate, which for a "
            "bandwidth-bound kernel is the whole optimisation "
            "(Module 07)."]},

  {"t": "table", "kicker": "Composition", "title": "Compositions that matter",
   "header": ["Composition", "Why it is better than the parts"],
   "widths": [4.0, 8.1],
   "rows": [
     ["<b>map → reduce, fused</b>", "<b>No intermediate array; one pass over memory</b>"],
     ["<b>map → scan → scatter</b>", "<b>Stream compaction; the standard filter</b>"],
     ["stencil → stencil", "<b>Temporal blocking — fuse timesteps for locality</b>"],
     ["scan → segmented scan", "Operates on many sequences at once"],
     ["<b>reduce → broadcast</b>", "An allreduce (Module 10)"],
   ],
   "footnote": "<b>Fusion is the most valuable transformation</b> because "
               "it reduces bytes moved, which is what bandwidth-bound code "
               "needs.",
   "note": "Temporal blocking is the clever one and is underused — it "
           "trades redundant computation for locality."},

  {"t": "section", "label": "Part 2", "title": "Frameworks",
   "blurb": "Writing once for several machines."},

  {"t": "table", "kicker": "Options", "title": "The portability frameworks",
   "header": ["Framework", "Targets", "Character"],
   "widths": [2.6, 4.2, 5.3],
   "rows": [
     ["<b>OpenMP</b>", "CPU, and GPU via target", "<b>Pragmas; incremental; ubiquitous</b>"],
     ["<b>TBB</b>", "CPU", "<b>C++ tasks and work stealing</b>"],
     ["<b>Kokkos</b>", "CPU, CUDA, HIP, SYCL", "<b>C++ abstractions; US lab standard</b>"],
     ["SYCL", "CPU, GPU, FPGA", "Single-source C++; open standard"],
     ["<b>CUDA</b>", "<b>NVIDIA only</b>", "<b>Most mature; least portable</b>"],
     ["std::execution", "CPU, some GPU", "Standard C++; still maturing"],
   ],
   "footnote": "<b>Kokkos and SYCL exist because laboratories had to run "
               "the same code on NVIDIA, AMD, and Intel GPUs.</b>",
   "note": "The institutional driver is worth noting — portability "
           "frameworks came from people who were forced into them."},

  {"t": "callout", "title": "Portable is not the same as performance-portable",
   "kind": "The distinction that matters",
   "body": ["<b>Portable code compiles and runs everywhere.</b> That is "
            "the easy part.",
            "<b>Performance-portable code achieves a good fraction of each "
            "machine's peak</b> — which is much harder, because the "
            "machines want different things.",
            "<b>A GPU wants coalesced access and thousands of threads; a "
            "CPU wants cache blocking and vectorisation.</b> Sometimes the "
            "optimal data layouts conflict directly.",
            "<b>So frameworks provide abstractions for layout</b> — "
            "Kokkos views choose row- or column-major per architecture, from "
            "the same source. <b>That is the actual contribution.</b>"]},

  {"t": "callout", "title": "The layout problem, concretely",
   "kind": "Why one source cannot naively serve both",
   "body": ["<b>On a GPU, consecutive threads must read consecutive "
            "addresses</b> to coalesce (Module 08) — so the loop index "
            "should vary fastest in memory.",
            "<b>On a CPU, each thread wants a contiguous block</b> to "
            "stay in cache and to vectorise — so the loop index should "
            "vary slowest within a thread's range.",
            "<b>These are opposite layouts for the same array.</b>",
            "<b>A framework that parameterises layout resolves it</b> at "
            "compile time per target. <b>Writing the array type yourself "
            "does not.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Ageing",
   "blurb": "Why parallel code does not last."},

  {"t": "bullets", "kicker": "Why it ages", "title": "What changes under your code",
   "items": [
     "<b>Core counts rise</b>, so a granularity that balanced well becomes "
     "too coarse.",
     "",
     "<b>The memory-to-compute ratio falls</b>, so a compute-bound kernel "
     "becomes bandwidth-bound (Module 07).",
     "",
     "<b>Vector widths grow</b>, so hand-written intrinsics become "
     "obsolete.",
     "",
     "<b>New units appear</b> — tensor cores, matrix engines — that "
     "existing code cannot use.",
     "",
     "<b>And the tuned constants</b> — tile sizes, chunk sizes, thread "
     "counts — were tuned for a machine that no longer exists.",
   ],
   "note": "The tuned-constants point is the most actionable: parameterise "
           "them and retune rather than hard-coding."},

  {"t": "callout", "title": "Write for retuning, not for one machine",
   "kind": "The practical response",
   "body": ["<b>Parameterise the tuning constants</b> — tile size, chunk "
            "size, thread count, unroll factor — rather than hard-coding "
            "them.",
            "<b>Keep a correctness reference</b> that is obviously right "
            "and slow, so an optimisation can always be checked.",
            "<b>Keep the benchmark with the code</b>, so retuning on new "
            "hardware is running a script rather than a project.",
            "<b>And prefer libraries for the hot primitives</b>, because "
            "they are retuned for you — which is the whole argument of "
            "Modules 05 and 09, restated."]},

  {"t": "callout", "title": "Autotuning is the systematic version",
   "kind": "Where this goes",
   "body": ["<b>Search the parameter space automatically</b> on the target "
            "machine, rather than choosing constants by hand.",
            "<b>This is how ATLAS, FFTW, and cuBLAS achieve their "
            "performance</b> — they generate and measure many variants at "
            "build or first use.",
            "<b>The search space is large</b>, so the methods matter: "
            "pruning, modelling, and increasingly learned cost models.",
            "<b>And it is the honest conclusion of this course:</b> the "
            "machine changes faster than you can retune by hand, so build "
            "the retuning in."]},
 ],
 "takeaways": [
   "Map, reduce, scan, stencil, gather/scatter, and partition cover most "
   "parallel computation and give you algorithm, complexity, and pitfalls "
   "for free.",
   "Fusion is the most valuable composition because it reduces bytes moved, "
   "which is what bandwidth-bound code needs.",
   "Portable means it runs everywhere; performance-portable means it runs "
   "well everywhere, and that is much harder.",
   "A GPU wants coalesced access across threads and a CPU wants contiguous "
   "blocks per thread — opposite layouts for the same array.",
   "Parallel code ages because core counts, memory ratios, vector widths, "
   "and available units all change under it.",
   "Parameterise the tuning constants, keep the benchmark with the code, and "
   "use libraries for hot primitives — or autotune.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Patterns as a design vocabulary"),
  ("callout", "Most parallel code is a composition of six patterns",
   ["<b>Map, reduce, scan, stencil, gather/scatter, and partition</b> "
    "(Module 06 &sect;3) account for the overwhelming majority of parallel "
    "computation across every domain in this program — rendering, "
    "simulation, databases, and image processing alike.",
    "<b>Recognising which pattern a computation is gives you the parallel "
    "algorithm, its work and depth, the known pitfalls, and usually a tested "
    "library implementation</b> — all without further analysis.",
    "<b>And it supplies a vocabulary for design discussion</b> that is "
    "considerably more precise than 'parallelise the loop'. 'This is a "
    "segmented scan followed by a scatter' communicates the structure, the "
    "cost, and the likely bottleneck in one sentence.",
    "<b>The engineering is in the composition.</b> A fused map-reduce never "
    "materialises the intermediate array, so it makes one pass over memory "
    "instead of two — which for a bandwidth-bound kernel (Module 07) is "
    "the entire optimisation, and halves the runtime."]),
  ("table", ["Composition", "Why it beats the parts separately"],
   [["<b>map &rarr; reduce, fused</b>",
     "<b>No intermediate array is written or read.</b> One pass over memory "
     "rather than three. For a bandwidth-bound computation this is the "
     "dominant factor."],
    ["<b>map &rarr; scan &rarr; scatter</b>",
     "<b>Stream compaction</b> — the standard parallel filter "
     "(Module 11). Produces a densely packed output with no atomics and no "
     "contention."],
    ["<b>stencil &rarr; stencil (temporal blocking)</b>",
     "<b>Fuse several timesteps over a spatial block</b>, computing "
     "redundant halo values in exchange for keeping the block in cache "
     "across all of them. <b>Trades extra computation for locality</b>, "
     "which is the right trade on bandwidth-bound hardware — and it is "
     "underused."],
    ["<b>scan &rarr; segmented scan</b>",
     "Operate on many independent sequences in one pass, using flags to mark "
     "segment boundaries. Essential for sparse and irregular data."],
    ["<b>reduce &rarr; broadcast</b>",
     "An allreduce (Module 10) — and recognising it as such means using "
     "the optimised collective rather than two separate operations."]],
   [0.31, 0.69]),

  ("h1", "2 &nbsp; Portability frameworks"),
  ("table", ["Framework", "Targets", "Character"],
   [["<b>OpenMP</b>", "CPU; GPU via <code>target</code> offload.",
     "<b>Pragma-based and incremental</b> — you can parallelise one "
     "loop without restructuring. Ubiquitous and supported by every major "
     "compiler. The GPU offload support is improving and is not yet "
     "competitive with native."],
    ["<b>Intel TBB</b>", "CPU.",
     "C++ task-based with work stealing (Module 06). Excellent "
     "composability — nested parallelism does not oversubscribe."],
    ["<b>Kokkos</b>", "CPU, CUDA, HIP, SYCL.",
     "<b>C++ abstractions over execution and memory spaces</b>, with "
     "architecture-dependent data layouts. <b>The de facto standard in US "
     "national laboratories</b>, which is why it is well supported."],
    ["<b>SYCL</b>", "CPU, GPU, FPGA.",
     "Single-source C++ and an open Khronos standard. Intel's oneAPI is the "
     "most prominent implementation."],
    ["<b>CUDA</b>", "<b>NVIDIA only.</b>",
     "<b>The most mature tooling, libraries, and documentation, and the "
     "least portable.</b> A genuine trade rather than an oversight."],
    ["<b>std::execution</b> / C++ parallel algorithms", "CPU; some GPU.",
     "Standard C++ with no extra dependency. Still maturing, and the "
     "implementation quality varies considerably."]],
   [0.17, 0.23, 0.60]),
  ("p", "<b>Kokkos and SYCL exist because laboratories were forced into "
        "them.</b> Having procured machines with NVIDIA, AMD, and Intel GPUs "
        "in successive generations, and holding application codes with "
        "decades of accumulated physics, they could not rewrite for each. "
        "<b>The institutional pressure is why these frameworks are serious "
        "rather than academic.</b>"),
  ("callout", "Portable is not performance-portable",
   ["<b>Portable code compiles and runs on several architectures.</b> That "
    "is the straightforward part, and several frameworks achieve it.",
    "<b>Performance-portable code achieves a good fraction of each "
    "machine's attainable peak</b> — which is substantially harder, "
    "because the architectures want structurally different things.",
    "<b>A GPU wants coalesced access across threads, thousands of resident "
    "threads, and no divergence. A CPU wants cache blocking, vectorisable "
    "inner loops, and a thread count matching the core count.</b> These are "
    "not merely different tunings; <b>sometimes the optimal data layouts "
    "directly conflict</b>.",
    "<b>So the frameworks' real contribution is abstraction over "
    "layout.</b> A Kokkos <code>View</code> selects row-major or "
    "column-major ordering according to the target architecture, from "
    "identical source. <b>That is the actual engineering</b> — the "
    "parallel-for wrapper is the easy part."]),
  ("callout", "The layout conflict, concretely",
   ["<b>On a GPU, consecutive threads must access consecutive addresses</b> "
    "to coalesce (Module 08 &sect;2). If thread <i>i</i> handles column "
    "<i>i</i> of a matrix, the array must be stored so that moving between "
    "columns moves one element in memory.",
    "<b>On a CPU, each thread wants a contiguous block</b> so that it stays "
    "in its own cache lines, avoids false sharing (Module 02), and "
    "vectorises over its inner loop. That requires the opposite ordering.",
    "<b>These are opposite memory layouts for the same logical array</b>, "
    "and no single hard-coded choice serves both. A program written for one "
    "runs correctly and badly on the other.",
    "<b>A framework that parameterises the layout resolves this at compile "
    "time per target</b>, with the index expressions generated accordingly. "
    "<b>Declaring the array yourself as a raw pointer does not</b>, and this "
    "is the most concrete answer to 'why not just use OpenMP and CUDA "
    "separately'."]),

  ("break",),
  ("h1", "3 &nbsp; Why parallel code ages badly"),
  ("ul", ["<b>Core counts rise.</b> A granularity that balanced well across "
          "8 cores is too coarse for 128 (Module 06), and a chunk size tuned "
          "for one is wrong for the other.",
          "<b>The ratio of compute to memory bandwidth rises.</b> Compute "
          "capacity has grown faster than bandwidth for decades, so the "
          "roofline's ridge point moves right — and <b>a kernel that "
          "was compute-bound becomes bandwidth-bound</b> without a line "
          "changing (Module 07). The correct optimisation strategy inverts.",
          "<b>Vector widths grow.</b> Hand-written SSE intrinsics do not use "
          "AVX-512, and code written with them is frozen at the width it was "
          "written for — which is the strongest argument for letting "
          "the compiler vectorise (Module 02).",
          "<b>New functional units appear.</b> Tensor cores, matrix engines, "
          "and specialised accelerators cannot be used by existing code at "
          "all, and reaching them generally means a library call or a "
          "rewrite.",
          "<b>And the tuned constants were tuned for a machine that no "
          "longer exists.</b> Tile sizes, chunk sizes, thread counts, unroll "
          "factors, and block dimensions were all measured on specific "
          "hardware, and all of them are now wrong. <b>This is the most "
          "actionable item</b>, because it is the easiest to design for."]),
  ("callout", "Write for retuning rather than for one machine",
   ["<b>Parameterise the tuning constants.</b> Tile size, chunk size, thread "
    "count, unroll factor, and block dimension should be named constants or "
    "runtime parameters — never literals scattered through the kernel. "
    "<b>Retuning then becomes changing values rather than finding them.</b>",
    "<b>Keep a correctness reference implementation</b> that is obviously "
    "right and makes no attempt to be fast. Every optimisation is then "
    "checkable, and the reference does not rot because it is never "
    "optimised. CSCE 647 and 649 required this for the same reason.",
    "<b>Keep the benchmark with the code</b>, in the repository, runnable "
    "with one command. <b>Retuning on new hardware is then a script, not a "
    "project</b>, and it is far likelier to actually happen.",
    "<b>And prefer libraries for the hot primitives</b>, because somebody "
    "else retunes them for every architecture generation. <b>This is the "
    "argument of Modules 05 and 09 restated</b>, and it is the single most "
    "effective defence against ageing."]),
  ("callout", "Autotuning is the systematic version of this",
   ["<b>Rather than choosing tuning constants by hand, search the parameter "
    "space automatically on the target machine</b>, measuring each candidate "
    "and keeping the best.",
    "<b>This is how ATLAS, FFTW, and cuBLAS achieve their performance.</b> "
    "FFTW measures many transform decompositions at first use and caches the "
    "plan; ATLAS generates and benchmarks hundreds of matrix multiply "
    "variants at install time. <b>The library is fast on your machine "
    "because it measured your machine.</b>",
    "<b>The search space is large</b> — the product of several "
    "parameters, each with many values — so the search methods matter: "
    "pruning with analytical models, hill climbing, and increasingly learned "
    "cost models that predict performance without running the candidate.",
    "<b>And it is the honest conclusion of this course.</b> <b>The machine "
    "changes faster than anyone can retune by hand</b>, so the right "
    "engineering response is to build the retuning into the software rather "
    "than to tune harder."]),
 ],
 "resources": [
   ("McCool, Robison & Reinders &mdash; Structured Parallel Programming",
    "https://www.elsevier.com/books/structured-parallel-programming/mccool/978-0-12-415993-8",
    "The pattern catalogue and composition material of &sect;1."),
   ("Kokkos documentation and tutorials (free)",
    "https://kokkos.org/",
    "The performance-portability abstractions of &sect;2, including the "
    "layout handling that is the real contribution."),
   ("SYCL specification and oneAPI documentation (free)",
    "https://www.khronos.org/sycl/",
    "The open-standard alternative."),
   ("Frigo & Johnson &mdash; The Design and Implementation of FFTW3 (free)",
    "https://www.fftw.org/fftw-paper-ieee.pdf",
    "<b>Autotuning done properly</b>, by the people who did it. The "
    "planner description in &sect;3 is here in detail."),
 ],
 "exercises": [
   "Express five computations from earlier courses in this program as "
   "compositions of the six patterns.",
   "Implement a map followed by a reduce as two passes and as a fused "
   "operation. Measure the difference and relate it to the roofline.",
   "<b>Implement temporal blocking for a stencil</b> and measure the "
   "trade between redundant computation and improved locality.",
   "Write the same kernel in OpenMP and in CUDA. Count the lines that "
   "differ and classify each difference.",
   "Write it once in Kokkos and build for both targets. Compare performance "
   "against each native version and report the fraction achieved.",
   "<b>Demonstrate the layout conflict:</b> write a kernel with the "
   "GPU-optimal layout and measure it on a CPU, and vice versa.",
   "Take a kernel with hard-coded tile and block sizes and parameterise "
   "them. Sweep the parameters on your hardware and find the best.",
   "Write an autotuning script that searches that space automatically and "
   "caches the result.",
   "Find a piece of parallel code more than five years old and identify "
   "which of &sect;3's five changes have invalidated its assumptions.",
 ],
 "selfcheck": [
   "Name the six patterns and say what recognising one gives you.",
   "Give five compositions and say why fusion is the most valuable.",
   "Compare six portability frameworks on targets and character.",
   "Distinguish portable from performance-portable.",
   "Describe the layout conflict between CPU and GPU concretely.",
   "Give five reasons parallel code ages.",
   "Give four practices that make retuning feasible.",
   "What is autotuning, which libraries use it, and why is it the honest "
   "conclusion?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Correctness, Debugging, and Shipping",
 "subtitle": "The parts that determine whether any of it is usable.",
 "question": "How do you know parallel code is right?",
 "outcomes": [
     "Explain why testing establishes less for concurrent code.",
     "Use the tools that detect possible rather than observed failures.",
     "Achieve reproducibility and know what it costs.",
     "Debug a parallel program systematically.",
     "State what you can honestly claim about parallel code.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What testing establishes",
   "blurb": "Less than you would like."},

  {"t": "callout", "title": "Passing tests shows that one interleaving worked",
   "kind": "The fundamental limit",
   "body": ["<b>A serial program has one execution path for a given "
            "input.</b> Testing it establishes a great deal.",
            "<b>A concurrent program has exponentially many "
            "interleavings</b>, and a test exercises one of them — "
            "whichever the scheduler happened to produce.",
            "<b>So a thousand passing runs establish that a thousand "
            "interleavings worked</b>, out of a space you cannot enumerate.",
            "<b>And the untested ones are not random</b> — they are the "
            "ones that occur under production load, which is precisely when "
            "you will meet them."]},

  {"t": "table", "kicker": "Tools", "title": "Tools, by what they establish",
   "header": ["Tool", "Establishes", "Limit"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Testing", "<b>This interleaving worked</b>", "<b>Very weak</b>"],
     ["<b>ThreadSanitizer</b>", "<b>No race was possible on this path</b>", "Only paths executed"],
     ["<b>Model checking</b>", "<b>No interleaving fails</b>", "<b>Small models only</b>"],
     ["Static analysis", "A class of error is absent", "False positives; annotation burden"],
     ["<b>Formal proof</b>", "<b>Correct, given the model</b>", "<b>Expensive; the model may be wrong</b>"],
   ],
   "footnote": "<b>ThreadSanitizer is the practical sweet spot</b> "
               "— it detects races that did not occur, on the paths "
               "you exercise.",
   "note": "The 'detects what did not occur' property is what makes "
           "sanitisers qualitatively better than testing."},

  {"t": "callout", "title": "Model checking the small core",
   "kind": "Where exhaustive verification is feasible",
   "body": ["<b>Tools like SPIN and TLA+ explore every interleaving</b> of "
            "a model, exhaustively.",
            "<b>They cannot handle a whole program</b> — the state space "
            "explodes.",
            "<b>But a lock protocol, a queue, or a state machine is small "
            "enough</b>, and those are exactly where the hard bugs live.",
            "<b>So model the tricky core and test the rest.</b> Several "
            "published lock-free algorithms had bugs found this way "
            "(Module 05), which is the strongest available evidence that "
            "it works."]},

  {"t": "section", "label": "Part 2", "title": "Reproducibility",
   "blurb": "And why you usually do not have it."},

  {"t": "callout", "title": "Parallel results are not bitwise reproducible by default",
   "kind": "The expectation to correct",
   "body": ["<b>Floating-point addition is not associative</b> "
            "(Module 06), so a reduction's result depends on the "
            "combination order.",
            "<b>And the order depends on the thread count, the schedule, "
            "and the timing</b> — so two runs on the same machine can "
            "differ.",
            "<b>This is not a bug and it must be expected.</b> It is a "
            "consequence of the arithmetic, not of the implementation.",
            "<b>If you need bitwise reproducibility</b> — for regression "
            "tests, for debugging, or for a result someone must replicate "
            "— <b>you must fix the reduction order and pay for it.</b>"]},

  {"t": "bullets", "kicker": "Achieving it", "title": "Getting reproducibility when you need it",
   "items": [
     "<b>Fixed decomposition</b> independent of thread count — the same "
     "chunks combined in the same order every run.",
     "",
     "<b>Deterministic reduction trees</b> rather than whoever-finishes-"
     "first combination.",
     "",
     "<b>No atomics for accumulation</b>, because their order is "
     "non-deterministic.",
     "",
     "<b>Compensated summation</b> (Kahan) reduces the <i>error</i>, "
     "which is a different and also useful goal.",
     "",
     "<b>And it costs performance</b> — a fixed order forbids dynamic "
     "balancing.",
   ],
   "note": "The cost is real and worth stating: reproducibility and "
           "load balancing are in tension."},

  {"t": "section", "label": "Part 3", "title": "Debugging",
   "blurb": "A method, since intuition fails."},

  {"t": "bullets", "kicker": "Method", "title": "Debugging a parallel program",
   "items": [
     "<b>1. Reproduce it.</b> Record the thread count, the input, the "
     "schedule. Increase the thread count and add delays to widen windows.",
     "",
     "<b>2. Does it fail with one thread?</b> If so, it is not a "
     "concurrency bug and the whole problem is simpler.",
     "",
     "<b>3. Run the sanitisers.</b> They frequently name it immediately.",
     "",
     "<b>4. Reduce it.</b> Cut the program down until the bug disappears, "
     "and the last removal is the clue.",
     "",
     "<b>5. Then reason</b> — about the specific interleaving, with a "
     "small enough example to hold in your head.",
   ],
   "footnote": "<b>Step 2 is the one people skip</b>, and it resolves a "
               "surprising fraction of supposed concurrency bugs."},

  {"t": "callout", "title": "Heisenbugs: observation changes the schedule",
   "kind": "Why printf debugging fails here",
   "body": ["<b>Adding a print statement changes the timing</b>, which "
            "changes the interleaving, which hides the bug.",
            "<b>Running under a debugger does the same</b>, more "
            "dramatically.",
            "<b>So use low-overhead logging to a per-thread buffer</b>, "
            "dumped afterwards — no locks, no I/O, minimal timing "
            "disturbance.",
            "<b>And record timestamps and thread IDs</b>, so the "
            "interleaving can be reconstructed after the fact rather than "
            "observed during."]},

  {"t": "section", "label": "Part 4", "title": "Claiming honestly",
   "blurb": "The course, closed."},

  {"t": "bullets", "kicker": "Claims", "title": "What you can honestly say",
   "items": [
     "<b>'It is X times faster than the optimised serial baseline, on this "
     "hardware, at this problem size.'</b> With the distribution.",
     "",
     "<b>'It scales to N cores, with the departure from ideal here, for "
     "this reason.'</b>",
     "",
     "<b>'It is bandwidth-bound at this arithmetic intensity'</b> — "
     "with the roofline to support it.",
     "",
     "<b>'ThreadSanitizer reports no races on our test suite.'</b> Not "
     "'it is race-free'.",
     "",
     "<b>And what you cannot say: 'it is correct'.</b> You can say it "
     "passes, and what was checked.",
   ],
   "note": "The sanitiser phrasing is the model — state what was "
           "established, not what you hope follows."},

  {"t": "callout", "title": "Where this leaves you",
   "kind": "Closing",
   "body": ["You can take a working program and determine, with "
            "measurement, what limits it — and therefore what would help.",
            "You can write correct shared-memory, GPU, and distributed code, "
            "and you know which tools establish what about it.",
            "<b>And you know that most code is bandwidth-bound, most "
            "speedup claims are overstated, and most parallel bugs are "
            "design failures.</b>",
            "<b>CSCE 629</b> chose the algorithm; <b>CSCE 614</b> explained "
            "the machine; <b>647, 649, 608, 650, and 748</b> supplied the "
            "workloads. <b>This course made them fast, and honestly "
            "measured.</b>"]},
 ],
 "takeaways": [
   "A serial test exercises one path; a concurrent test exercises one "
   "interleaving out of exponentially many, so passing establishes far less.",
   "ThreadSanitizer detects races that did not occur on paths you did "
   "execute, which is qualitatively stronger than testing.",
   "Model checking explores every interleaving of a small model — so "
   "model the tricky core and test the rest.",
   "Parallel floating-point results are not bitwise reproducible by default, "
   "because addition is not associative and the order varies.",
   "Reproducibility requires a fixed decomposition and deterministic "
   "reduction order, and it costs dynamic load balancing.",
   "Say what was established — 'the sanitiser reports no races on our "
   "suite' — rather than what you hope follows.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What testing establishes"),
  ("callout", "Passing tests shows that one interleaving worked",
   ["<b>A serial program follows one execution path for a given input.</b> "
    "Running it with that input establishes what happens for that input, "
    "which is a great deal — and it is why testing works as well as it "
    "does for sequential code.",
    "<b>A concurrent program has exponentially many possible "
    "interleavings</b> of its threads' operations, and a single run "
    "exercises exactly one of them — whichever the scheduler, the cache "
    "state, and the ambient system load happened to produce.",
    "<b>So a thousand passing runs establish that a thousand interleavings "
    "worked</b>, drawn from a space you cannot enumerate and which is "
    "typically vastly larger.",
    "<b>And the untested interleavings are not randomly distributed.</b> "
    "They are the ones that arise under heavy load, on different hardware, "
    "with a different thread count — which is to say, in production. "
    "<b>Testing concentrates its sampling in precisely the conditions where "
    "the bugs are not.</b>"]),
  ("table", ["Technique", "What it establishes", "Limitation"],
   [["<b>Testing</b>", "<b>This particular interleaving produced the right "
     "answer.</b>", "<b>Very weak</b>, per the callout above."],
    ["<b>Dynamic race detection (ThreadSanitizer)</b>",
     "<b>No data race was <i>possible</i> on the paths executed</b> "
     "— it tracks the happens-before relation rather than observing "
     "failures, so it reports races that did not actually occur.",
     "Only covers code paths actually executed, so coverage still matters. "
     "<b>The practical sweet spot</b>, and the reason it should run over the "
     "whole test suite."],
    ["<b>Model checking (SPIN, TLA+)</b>",
     "<b>No interleaving of the model violates the specified "
     "properties.</b> Exhaustive.",
     "<b>Small models only</b> — the state space explodes. And the "
     "result applies to the model, not the code."],
    ["<b>Static analysis with annotations</b>",
     "A specific class of error is absent, at compile time.",
     "False positives, and the annotation burden is real."],
    ["<b>Formal proof</b>", "<b>The algorithm is correct, given the "
     "model.</b>",
     "<b>Expensive</b>, and the model may not match the hardware — "
     "several proofs assumed sequential consistency (Module 04)."]],
   [0.22, 0.42, 0.36]),
  ("callout", "Model check the small core",
   ["<b>Tools such as SPIN and TLA+ explore every possible interleaving of "
    "a model exhaustively</b>, and report a counterexample trace when a "
    "property fails — which is a qualitatively different kind of result "
    "from testing.",
    "<b>They cannot handle a whole program.</b> The state space grows "
    "combinatorially, and any realistic application exceeds it by many "
    "orders of magnitude.",
    "<b>But a lock protocol, a concurrent queue, a cache coherence "
    "handshake, or a state machine is small enough</b> — and those are "
    "exactly the components where the hard bugs live. The surrounding "
    "application code is usually straightforwardly sequential.",
    "<b>So model the tricky core and test the rest.</b> <b>Several published "
    "lock-free algorithms had bugs discovered this way</b> (Module 05), "
    "years after publication and peer review, which is the strongest "
    "available evidence that the technique finds things human review does "
    "not."]),

  ("h1", "2 &nbsp; Reproducibility"),
  ("callout", "Parallel results are not bitwise reproducible by default",
   ["<b>Floating-point addition is not associative</b> (Module 06 "
    "&sect;3), so the result of a reduction depends on the order in which "
    "the partial sums are combined.",
    "<b>And that order depends on the thread count, the schedule, and the "
    "timing.</b> With dynamic scheduling or atomic accumulation, two runs on "
    "the <i>same</i> machine with the <i>same</i> input can produce "
    "different results in the last bits.",
    "<b>This is not a bug and it must be expected.</b> It is a consequence "
    "of how floating-point arithmetic works combined with how parallel "
    "reduction works, and no implementation quality removes it.",
    "<b>If you need bitwise reproducibility</b> — for regression "
    "testing, for debugging (where a changing answer makes bisection "
    "impossible), or for a scientific result someone else must replicate "
    "— <b>you must fix the combination order and pay for it.</b> "
    "CSCE 649's Module 13 reached the same conclusion from the simulation "
    "side, and for the same underlying reason."]),
  ("ul", ["<b>A fixed decomposition independent of the thread count.</b> The "
          "same chunks, combined in the same order, regardless of how many "
          "threads execute them.",
          "<b>Deterministic reduction trees</b> — combine partial "
          "results in a predetermined pattern rather than in whatever order "
          "threads finish.",
          "<b>No atomics for accumulation</b>, since the order in which "
          "atomic updates land is non-deterministic by construction.",
          "<b>Compensated summation</b> (Kahan, or Neumaier) tracks and "
          "corrects the rounding error. <b>This reduces the error rather "
          "than fixing the order</b>, which is a different goal and often "
          "the more useful one — a more accurate answer may matter more "
          "than an identical one.",
          "<b>And it costs performance.</b> A fixed combination order "
          "forbids dynamic load balancing (Module 06), so a workload with "
          "variable per-item cost pays in imbalance. <b>Reproducibility and "
          "load balancing are in direct tension</b>, and which you need is a "
          "decision rather than a default."]),

  ("break",),
  ("h1", "3 &nbsp; Debugging"),
  ("ol", ["<b>Reproduce it.</b> Record the thread count, the input, and any "
          "relevant environment. <b>Then make it more likely:</b> increase "
          "the thread count beyond the core count, inject random delays at "
          "suspicious points, and run under load. All of these widen the "
          "windows in which the bad interleaving occurs.",
          "<b>Does it fail with one thread?</b> If it does, it is not a "
          "concurrency bug at all, and the entire problem becomes an "
          "ordinary sequential debugging exercise. <b>This is the step "
          "people skip, and it resolves a surprising fraction of supposed "
          "concurrency bugs</b> — an uninitialised variable or an "
          "off-by-one does not become a race because the program has "
          "threads.",
          "<b>Run the sanitisers.</b> ThreadSanitizer, AddressSanitizer, "
          "and <code>compute-sanitizer</code> for GPU code. They frequently "
          "identify the problem immediately, with both stack traces.",
          "<b>Reduce it.</b> Cut the program down — remove threads, "
          "remove phases, shrink the input — until the bug disappears. "
          "<b>The last thing you removed is the clue</b>, and a minimal "
          "reproducer is worth more than any amount of reasoning about the "
          "full program.",
          "<b>Then reason.</b> With a small enough example, the specific "
          "interleaving can be held in your head and the argument can be "
          "made properly. <b>Reasoning first, on the full program, is what "
          "wastes days.</b>"]),
  ("callout", "Heisenbugs: observing changes the schedule",
   ["<b>Adding a print statement changes the timing</b>, which changes the "
    "interleaving, which frequently hides the bug entirely — and then "
    "removing the print brings it back, which is a demoralising experience.",
    "<b>Running under a debugger does the same, more dramatically.</b> "
    "Single-stepping one thread serialises the execution completely, and "
    "breakpoints change the relative timing by orders of magnitude.",
    "<b>So use low-overhead logging into a per-thread ring buffer</b>, "
    "dumped after the failure. No locks, no I/O during the run, and minimal "
    "disturbance to timing — a few nanoseconds per entry rather than "
    "microseconds.",
    "<b>Record a timestamp and a thread identifier with every entry</b>, so "
    "the interleaving can be reconstructed afterwards from the merged logs. "
    "<b>Reconstructing the schedule after the fact is the technique</b>; "
    "observing it as it happens changes what you are observing."]),

  ("h1", "4 &nbsp; Claiming honestly"),
  ("ul", ["<b>'It is X times faster than the optimised serial baseline, on "
          "this hardware, at this problem size, with these compiler "
          "flags.'</b> With the distribution rather than the minimum "
          "(Module 07 &sect;3). Every one of those qualifiers is load "
          "bearing.",
          "<b>'It scales to N cores, departing from ideal at this point, "
          "for this reason.'</b> Naming the reason — bandwidth "
          "saturation, load imbalance, synchronisation — is what "
          "distinguishes a measurement from a graph.",
          "<b>'It is bandwidth-bound at an arithmetic intensity of "
          "I.'</b> With the roofline placement to support it (Module 07).",
          "<b>'ThreadSanitizer reports no data races over our test "
          "suite.'</b> <b>Not 'the code is race-free'</b> — the tool "
          "examined the paths your tests exercised, and that is exactly what "
          "the claim should say. <b>This phrasing is the model for all of "
          "them:</b> state what was established, not what you hope follows "
          "from it.",
          "<b>And what you cannot honestly say: 'it is correct'.</b> You can "
          "say what it passes, what was checked, and by what method. For "
          "concurrent code that gap is wider than for sequential code, and "
          "pretending otherwise is how the bugs reach production."]),
  ("callout", "Where this leaves you",
   ["<b>You can take a working program and determine, by measurement, what "
    "limits it</b> — and therefore which optimisations can possibly "
    "help and which cannot. That diagnostic ability is worth more than any "
    "individual technique in this course, because it is what prevents weeks "
    "spent on the wrong thing.",
    "<b>You can write correct shared-memory, GPU, and distributed-memory "
    "code</b>, and you know which tools establish what about its "
    "correctness — and how much less that is than you would like.",
    "<b>And you know the three things that reorient most people's "
    "expectations:</b> most real code is bandwidth-bound rather than "
    "compute-bound; most published speedup claims are overstated, usually "
    "through the baseline; and most parallel bugs are design failures rather "
    "than coding errors.",
    "<b>CSCE 629 chose the algorithm. CSCE 614 explained the machine. "
    "CSCE 647, 649, 608, 650, and 748 supplied the workloads that needed "
    "the speed.</b> <b>This course made them fast — and, more "
    "importantly, honestly measured</b>, which is the part that survives "
    "when the hardware changes."]),
 ],
 "resources": [
   ("Lamport &mdash; TLA+ and the Specifying Systems book (free)",
    "https://lamport.azurewebsites.net/tla/tla.html",
    "Model checking concurrent algorithms. The book is free and the "
    "video course is a reasonable entry point."),
   ("Holzmann &mdash; The SPIN Model Checker",
    "https://spinroot.com/",
    "The tool and its documentation, free. Well suited to the small-core "
    "modelling of &sect;1."),
   ("ThreadSanitizer and compute-sanitizer documentation (free)",
    "https://github.com/google/sanitizers/wiki",
    "What each tool establishes and what it does not — worth reading "
    "the limitations sections specifically."),
   ("Hoefler & Belli &mdash; Scientific Benchmarking of Parallel Computing "
    "Systems (free)",
    "https://htor.inf.ethz.ch/publications/index.php?pub=222",
    "<b>The reporting discipline of &sect;4</b>, made rigorous. The single "
    "most useful paper in this course for anyone who will publish "
    "performance results."),
   ("Demmel & Nguyen &mdash; reproducible floating-point summation (free)",
    "https://people.eecs.berkeley.edu/~demmel/",
    "The &sect;2 problem and the algorithms that address it."),
 ],
 "exercises": [
   "Take a concurrent data structure and run it a million times. Then run it "
   "under ThreadSanitizer and compare what each found.",
   "<b>Model a lock protocol or a bounded queue in TLA+ or SPIN</b> and "
   "check a safety property. Then introduce a bug and confirm it finds it.",
   "<b>Demonstrate non-reproducibility:</b> run a parallel float reduction "
   "twenty times at several thread counts and report every distinct answer.",
   "Implement a deterministic reduction and confirm bitwise reproducibility "
   "across thread counts. Measure the performance cost.",
   "Implement Kahan summation and compare the error against both the naive "
   "parallel and the serial result.",
   "Take a concurrency bug and apply the five-step method. Document what "
   "each step contributed.",
   "<b>Create a Heisenbug:</b> a race that disappears when a print statement "
   "is added. Then find it with a per-thread ring buffer.",
   "Write a per-thread logging buffer with timestamps and reconstruct an "
   "interleaving from it.",
   "Take a performance claim from a paper or a README and rewrite it to meet "
   "&sect;4's standard. Note what information is missing.",
   "<b>Project 2 is now due.</b> Submit the implementation, the measured "
   "optimisation steps including any that failed, the profiler evidence, the "
   "library comparison, and the statement of what limits the final version.",
 ],
 "selfcheck": [
   "Why does testing establish less for concurrent code than for sequential "
   "code?",
   "Compare five verification techniques on what each establishes and its "
   "limit.",
   "What makes dynamic race detection stronger than testing?",
   "What can model checking do, what can it not, and what follows?",
   "Why are parallel floating-point results not reproducible?",
   "Give four requirements for reproducibility and the cost.",
   "Give the five debugging steps and say which is most often skipped.",
   "What is a Heisenbug, and what technique replaces printf debugging?",
   "Give four honest performance claims and one thing you cannot say.",
 ],
},

]
