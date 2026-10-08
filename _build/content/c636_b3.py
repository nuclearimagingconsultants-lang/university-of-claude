# -*- coding: utf-8 -*-
"""CSCE 636 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Training at Scale",
 "subtitle": "When the model no longer fits.",
 "question": "What do you do when one GPU is not enough?",
 "outcomes": [
     "Explain data, tensor, and pipeline parallelism.",
     "Explain mixed precision and why loss scaling is needed.",
     "Apply gradient accumulation and checkpointing.",
     "Reason about the memory budget of a training run.",
     "Diagnose whether you are compute- or memory-bound.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The memory budget",
   "blurb": "Where the memory actually goes."},

  {"t": "code", "kicker": "Memory", "title": "What occupies the GPU during training",
   "lang": "text", "code": """
  For a model with P parameters, training in mixed precision
  with Adam:

    parameters        (fp16)   2P bytes
    gradients         (fp16)   2P
    Adam m            (fp32)   4P
    Adam v            (fp32)   4P
    fp32 master copy           4P
                             -----
                              16P bytes, before any activations

  A 7-BILLION-PARAMETER MODEL: ~112 GB of optimiser state alone.
  That does not fit on any single accelerator.

  ACTIVATIONS are stored for the backward pass and scale with
  batch size x sequence length x depth. For transformers at long
  context they frequently EXCEED the parameter memory.

  SO THE LEVERS, in the order you should reach for them:
    gradient accumulation   -- smaller batch, same effective batch
    activation checkpointing-- recompute instead of storing
    mixed precision         -- halve the activation memory
    optimiser sharding      -- split m, v, master across devices
    then actual model parallelism
""",
   "caption": "<b>The optimiser state is 12 bytes per parameter</b>, which "
              "is three-quarters of the budget and is usually the "
              "surprise.",
   "note": "The 16P figure is the one to remember; it drives everything."},

  {"t": "callout", "title": "Gradient accumulation and checkpointing come first",
   "kind": "The cheap fixes",
   "body": ["<b>Gradient accumulation:</b> run several small batches, sum "
            "the gradients, step once. <b>Identical result to a large "
            "batch</b>, at a fraction of the memory.",
            "<b>Activation checkpointing:</b> store only some layers' "
            "activations and recompute the rest during the backward pass. "
            "<b>Roughly √n memory for about 30% more compute.</b>",
            "<b>Both are a few lines and neither changes the "
            "mathematics</b>, so they should be exhausted before anything "
            "distributed.",
            "<b>And they compose.</b> Together they frequently turn a "
            "model that will not fit into one that trains comfortably, "
            "which is a better outcome than adding a second machine."]},

  {"t": "section", "label": "Part 2", "title": "Parallelism",
   "blurb": "Three axes, and the order to use them."},

  {"t": "table", "kicker": "Parallelism", "title": "The three kinds",
   "header": ["Kind", "Splits", "Communication"],
   "widths": [2.7, 4.3, 5.1],
   "rows": [
     ["<b>Data parallel</b>", "<b>The batch, across devices</b>", "<b>All-reduce the gradients each step</b>"],
     ["<b>ZeRO / FSDP</b>", "<b>Optimiser state and parameters too</b>", "<b>More communication; far less memory</b>"],
     ["<b>Tensor parallel</b>", "<b>Individual matrices, within a layer</b>", "<b>Every layer. Needs fast interconnect</b>"],
     ["<b>Pipeline parallel</b>", "Layers, across devices", "<b>Only at stage boundaries. Has a bubble</b>"],
     ["Expert parallel", "Experts in a mixture-of-experts", "Routed; sparse activation"],
   ],
   "footnote": "<b>Use data parallelism first, then ZeRO, then pipeline, "
               "then tensor</b> — in increasing order of "
               "communication demand and implementation pain.",
   "note": "That ordering is the practical takeaway."},

  {"t": "callout", "title": "Data parallelism is the all-reduce from CSCE 735",
   "kind": "The connection",
   "body": ["<b>Each device holds a full model copy and a slice of the "
            "batch</b>, computes gradients locally, and then they are "
            "averaged across all devices.",
            "<b>That average is exactly an all-reduce</b> "
            "(CSCE 735 M10 §2) — and ring all-reduce is what the "
            "libraries implement.",
            "<b>So the cost is the gradient size times the "
            "interconnect</b>, every step, and it is why NVLink and "
            "InfiniBand matter for training.",
            "<b>And it can be overlapped:</b> start reducing the last "
            "layer's gradients while the earlier layers are still "
            "computing theirs. <b>CSCE 735 Module 10's "
            "computation–communication overlap, applied here.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Mixed precision",
   "blurb": "Half the bits, most of the accuracy."},

  {"t": "callout", "title": "Why loss scaling is necessary",
   "kind": "The detail that makes it work",
   "body": ["<b>fp16 has a narrow range.</b> Gradients are often very "
            "small, and values below about 6×10⁻⁸ "
            "<b>flush to zero</b> — the gradient silently disappears.",
            "<b>So multiply the loss by a large constant before the "
            "backward pass</b>, which scales every gradient up into the "
            "representable range, then divide before the update.",
            "<b>Dynamic loss scaling adjusts the factor automatically</b> "
            "— raise it when no overflow occurs, halve it and skip the "
            "step when one does.",
            "<b>bf16 avoids the problem entirely</b> — same exponent "
            "range as fp32 with fewer mantissa bits — <b>which is why it "
            "is preferred wherever the hardware supports it.</b>"]},

  {"t": "table", "kicker": "Formats", "title": "The numeric formats",
   "header": ["Format", "Bits (sign/exp/mantissa)", "Character"],
   "widths": [2.3, 4.0, 5.8],
   "rows": [
     ["<b>fp32</b>", "1 / 8 / 23", "The baseline. Rarely needed throughout"],
     ["<b>fp16</b>", "<b>1 / 5 / 10</b>", "<b>Narrow range — needs loss scaling</b>"],
     ["<b>bf16</b>", "<b>1 / 8 / 7</b>", "<b>fp32's range, less precision. Preferred</b>"],
     ["<b>fp8</b>", "1 / 4 / 3 or 1 / 5 / 2", "<b>Inference, and increasingly training</b>"],
     ["int8", "Integer, with a scale", "<b>Inference only; Module 13</b>"],
   ],
   "footnote": "<b>bf16 trades mantissa for exponent</b>, which is the "
               "right trade for gradients — their magnitude varies "
               "far more than their precision matters.",
   "note": "That reasoning is why bf16 was designed and why it won."},

  {"t": "section", "label": "Part 4", "title": "Diagnosing",
   "blurb": "Where the time is going."},

  {"t": "bullets", "kicker": "Diagnosis", "title": "Is it compute, memory, or communication?",
   "items": [
     "<b>Measure the achieved FLOPs against the device peak.</b> Below "
     "~30% means you are not compute-bound.",
     "",
     "<b>Measure memory bandwidth utilisation.</b> High bandwidth and "
     "low FLOPs means memory-bound — CSCE 735's roofline, applied.",
     "",
     "<b>Measure the fraction of step time spent in communication.</b> "
     "If it is large, overlap it or reduce the gradient size.",
     "",
     "<b>Check the data loader.</b> <b>A GPU idle waiting for data is "
     "extremely common</b> and is invisible unless you look.",
     "",
     "<b>And profile before optimising</b> — CSCE 735 Module 07, "
     "unchanged.",
   ],
   "footnote": "<b>The data loader is the single most common "
               "bottleneck</b> in small-scale training and almost nobody "
               "checks it first."},
 ],
 "takeaways": [
   "Mixed-precision Adam costs about 16 bytes per parameter before any "
   "activations, and 12 of those are optimiser state.",
   "Gradient accumulation and activation checkpointing are a few lines "
   "each, change no mathematics, and should be exhausted before anything "
   "distributed.",
   "Data parallelism is an all-reduce of the gradients, which is "
   "CSCE 735's collective applied here — and it overlaps with the "
   "backward pass.",
   "fp16 gradients flush to zero, so loss scaling is required; bf16 has "
   "fp32's exponent range and avoids the problem.",
   "bf16 trades mantissa for exponent, which is the right trade because "
   "gradient magnitudes vary more than their precision matters.",
   "A GPU idle waiting on the data loader is the most common small-scale "
   "bottleneck and almost nobody checks it first.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The memory budget"),
  ("code", """For P parameters, mixed precision, Adam:

  parameters      (fp16)    2P bytes
  gradients       (fp16)    2P
  Adam m          (fp32)    4P
  Adam v          (fp32)    4P
  fp32 master copy          4P
                          -----
                           16P bytes, BEFORE any activations

A 7-BILLION-PARAMETER MODEL: ~112 GB of state alone. That does
not fit on any single accelerator.

ACTIVATIONS are retained for the backward pass and scale with
batch x sequence length x depth. At long context they frequently
EXCEED the parameter memory.

LEVERS, in the order to reach for them:
  gradient accumulation      smaller batch, same effective batch
  activation checkpointing   recompute rather than store
  mixed precision            halve the activation memory
  optimiser sharding (ZeRO)  split m, v and master across devices
  then actual model parallelism"""),
  ("p", "<b>The optimiser state is twelve of those sixteen bytes</b>, "
        "which is three-quarters of the budget and is reliably the "
        "surprise — people size their hardware against the parameter "
        "count and are short by a factor of eight. <b>It is also why ZeRO "
        "and FSDP exist</b>: sharding the optimiser state across devices "
        "attacks the largest term first."),
  ("callout", "Gradient accumulation and checkpointing come first",
   ["<b>Gradient accumulation:</b> run several small micro-batches, "
    "accumulate their gradients without stepping, then take one optimiser "
    "step. <b>The result is mathematically identical to a single large "
    "batch</b> (modulo batch normalisation, which is batch-dependent "
    "— Module 04 &sect;3), at a fraction of the activation memory.",
    "<b>Activation checkpointing:</b> store the activations of only some "
    "layers and recompute the rest during the backward pass. <b>Roughly "
    "&radic;n memory for about 30% additional compute</b> — an "
    "excellent trade whenever memory is the binding constraint, and a bad "
    "one when it is not.",
    "<b>Both are a few lines of code and neither changes the "
    "mathematics</b>, so they should be fully exhausted before anything "
    "distributed is attempted. Distribution brings communication, "
    "debugging across processes, and a class of bugs that single-device "
    "training does not have.",
    "<b>And they compose.</b> Together they frequently turn a model that "
    "will not fit into one that trains comfortably on the hardware you "
    "already have — <b>which is a better outcome than adding a second "
    "machine</b>, and is the same 'do you actually need to distribute?' "
    "question CSCE 678 Module 01 &sect;4 asked."]),

  ("h1", "2 &nbsp; Parallelism"),
  ("table", ["Kind", "What it splits", "Communication cost"],
   [["<b>Data parallel</b>",
     "<b>The batch, across devices.</b> Every device holds a complete model "
     "copy.",
     "<b>An all-reduce of the gradients every step</b> — see below. "
     "Simple, and the memory per device is unchanged."],
    ["<b>ZeRO / FSDP</b>",
     "<b>The optimiser state, the gradients, and eventually the parameters "
     "themselves</b>, across devices.",
     "<b>More communication, dramatically less memory.</b> Parameters are "
     "gathered just before use and released after, which trades bandwidth "
     "for capacity."],
    ["<b>Tensor parallel</b>",
     "<b>Individual weight matrices, within a layer</b> — each device "
     "computes part of one matrix multiply.",
     "<b>Communication at every layer</b>, so it <b>requires a very fast "
     "interconnect</b> (NVLink within a node) and does not work well across "
     "ordinary networks."],
    ["<b>Pipeline parallel</b>",
     "Consecutive layers, across devices.",
     "<b>Only at stage boundaries</b>, which is cheap — <b>but it "
     "introduces a pipeline bubble</b>, since the last stage idles until "
     "the first micro-batch reaches it. Micro-batching reduces but does not "
     "remove it."],
    ["<b>Expert parallel</b>",
     "The experts of a mixture-of-experts layer.",
     "Routed and sparse — only the selected experts activate, so "
     "parameters scale without proportional compute."]],
   [0.18, 0.38, 0.44]),
  ("p", "<b>Use data parallelism first, then ZeRO, then pipeline, then "
        "tensor</b> — in increasing order of communication demand and "
        "implementation pain. <b>Large training runs combine all of "
        "them</b> (3D parallelism), which is where the engineering "
        "genuinely becomes hard."),
  ("callout", "Data parallelism is the all-reduce from CSCE 735",
   ["<b>Each device holds a complete copy of the model and a slice of the "
    "batch</b>, computes gradients on its own slice, and then the gradients "
    "are averaged across all devices before the optimiser step.",
    "<b>That average is exactly an all-reduce</b> (CSCE 735 Module 10 "
    "&sect;2), and <b>ring all-reduce is what NCCL and the other "
    "collective libraries implement</b> — bandwidth-optimal, and it is "
    "the same algorithm the HPC community developed decades earlier.",
    "<b>So the cost is the gradient size divided by the interconnect "
    "bandwidth, every single step</b>, which is why NVLink within a node "
    "and InfiniBand between nodes matter so much for training throughput "
    "— and why gradient compression is an active area.",
    "<b>And it can be overlapped with computation:</b> start reducing the "
    "last layer's gradients as soon as they exist, while the earlier "
    "layers are still computing theirs. <b>This is exactly CSCE 735 "
    "Module 10 &sect;3's computation–communication overlap</b>, "
    "applied to a problem that course did not anticipate — and like "
    "there, <b>you must measure whether the overlap actually happened</b> "
    "rather than assuming the library arranged it."]),

  ("break",),
  ("h1", "3 &nbsp; Mixed precision"),
  ("callout", "Why loss scaling is necessary",
   ["<b>fp16 has a narrow exponent range.</b> Its smallest normal positive "
    "value is about 6&times;10<super>&minus;5</super>, and subnormals "
    "extend only to about 6&times;10<super>&minus;8</super>.",
    "<b>Gradients are frequently smaller than that</b>, particularly in "
    "early layers of deep networks — so they <b>flush to zero and the "
    "learning signal silently disappears</b>. The model trains, slowly and "
    "badly, with no error reported.",
    "<b>So multiply the loss by a large constant before the backward "
    "pass.</b> By the chain rule, every gradient is scaled by the same "
    "factor, lifting them into the representable range; divide the "
    "gradients by that factor before the optimiser step and the "
    "mathematics is unchanged. <b>Dynamic loss scaling adjusts the "
    "constant automatically</b> — raise it when no overflow has "
    "occurred for a while, halve it and skip the step when one does.",
    "<b>bf16 avoids the problem entirely.</b> It has the same eight-bit "
    "exponent as fp32 — hence the same range — with fewer "
    "mantissa bits. <b>No loss scaling is required at all</b>, which "
    "removes a whole class of bugs, <b>and it is why bf16 is preferred "
    "wherever the hardware supports it.</b>"]),
  ("table", ["Format", "sign / exponent / mantissa", "Character"],
   [["<b>fp32</b>", "1 / 8 / 23",
     "The baseline. Rarely needed throughout a training run; usually "
     "retained only for the master weights and the optimiser state."],
    ["<b>fp16</b>", "<b>1 / 5 / 10</b>",
     "<b>Narrow range, so it requires loss scaling</b> (above). More "
     "mantissa precision than bf16, which is almost never the binding "
     "concern."],
    ["<b>bf16</b>", "<b>1 / 8 / 7</b>",
     "<b>fp32's exponent range with much less precision.</b> <b>The "
     "preferred training format</b> — see below for why that trade is "
     "the right one."],
    ["<b>fp8</b>", "1 / 4 / 3, or 1 / 5 / 2",
     "<b>Inference, and increasingly training</b> on hardware that supports "
     "it, with per-tensor scaling factors."],
    ["<b>int8 and below</b>", "Integer plus a scale factor.",
     "<b>Inference only</b> — Module 13 &sect;2."]],
   [0.15, 0.33, 0.52]),
  ("p", "<b>bf16 trades mantissa bits for exponent bits, and that is the "
        "right trade for gradients:</b> their <i>magnitude</i> varies over "
        "many orders of magnitude between layers and over training, while "
        "their <i>precision</i> matters very little — the update is "
        "going to be averaged over a batch and scaled by a learning rate "
        "anyway. <b>Knowing why the format was designed that way makes the "
        "choice obvious rather than received.</b>"),

  ("h1", "4 &nbsp; Diagnosing a slow training run"),
  ("ul", ["<b>Measure the achieved FLOPs against the device's peak.</b> "
          "Below roughly 30% of peak means you are not compute-bound, and "
          "optimising the arithmetic will achieve nothing — which is "
          "CSCE 735 Module 07's roofline argument applied directly.",
          "<b>Measure memory bandwidth utilisation.</b> High bandwidth "
          "with low FLOPs means memory-bound, and the fix is fusion, better "
          "layout, or larger batches — not a faster kernel.",
          "<b>Measure the fraction of step time spent in "
          "communication.</b> If it is large, overlap it with computation "
          "(&sect;2), reduce the gradient size, or reconsider the "
          "parallelism strategy.",
          "<b>Check the data loader.</b> <b>A GPU sitting idle waiting for "
          "the next batch is extremely common and is completely invisible "
          "unless you look for it</b> — the training loop reports "
          "normal-looking step times and the accelerator is at 20% "
          "utilisation. <b>It is the single most common bottleneck in "
          "small-scale training and almost nobody checks it first.</b> More "
          "worker processes, prefetching, and doing augmentation on the GPU "
          "all help.",
          "<b>And profile before optimising</b> — CSCE 735 "
          "Module 07, entirely unchanged. The profiler names the limiting "
          "resource; guessing does not."]),
 ],
 "resources": [
   ("Rajbhandari et al. &mdash; ZeRO: Memory Optimizations Toward "
    "Training Trillion Parameter Models (free)",
    "https://arxiv.org/abs/1910.02054",
    "<b>The &sect;1 memory accounting and the &sect;2 sharding "
    "strategy</b>, with the three stages laid out clearly."),
   ("Micikevicius et al. &mdash; Mixed Precision Training (free)",
    "https://arxiv.org/abs/1710.03740",
    "<b>The &sect;3 loss-scaling argument</b>, including the gradient "
    "histograms that show the flush-to-zero problem."),
   ("Hugging Face &mdash; Performance and Scalability documentation "
    "(free)",
    "https://huggingface.co/docs/transformers/performance",
    "<b>The practical lever ordering of &sect;1</b>, with measured effects "
    "for each technique."),
   ("Chen et al. &mdash; Training Deep Nets with Sublinear Memory Cost "
    "(free)",
    "https://arxiv.org/abs/1604.06174",
    "Activation checkpointing and the &radic;n result."),
 ],
 "exercises": [
   "<b>Compute the memory budget</b> for a model you want to train, using "
   "the 16P formula, and compare against your hardware.",
   "<b>Measure actual GPU memory</b> during a training step and break it "
   "down by category.",
   "Implement gradient accumulation and verify the result matches a large "
   "batch exactly.",
   "<b>Enable activation checkpointing</b> and measure the memory saving "
   "and the compute cost.",
   "Train in fp32, fp16 with loss scaling, and bf16. Compare final loss "
   "and wall-clock time.",
   "<b>Disable loss scaling in fp16</b> and plot the fraction of gradients "
   "that flush to zero.",
   "Run data-parallel training on two devices and measure the all-reduce "
   "time per step.",
   "<b>Verify whether gradient reduction overlaps with the backward "
   "pass</b>, as CSCE 735 Module 10 required.",
   "<b>Profile your data loader</b> and report the fraction of step time "
   "the GPU spends idle.",
   "Place your training step on a roofline and state what limits it.",
 ],
 "selfcheck": [
   "Give the memory cost per parameter for mixed-precision Adam, broken "
   "down.",
   "What do gradient accumulation and checkpointing each cost and save?",
   "Compare five kinds of parallelism and give the order to use them.",
   "Why is data parallelism an all-reduce, and what can be overlapped?",
   "Why does fp16 need loss scaling, and how does dynamic scaling work?",
   "Why does bf16 avoid the problem, and why is its trade the right one?",
   "Give five things to measure when training is slow.",
   "What is the most common small-scale bottleneck?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Transfer and Representation Learning",
 "subtitle": "Reusing what a model already learned.",
 "question": "Why start from scratch?",
 "outcomes": [
     "Explain why pretrained features transfer.",
     "Choose between feature extraction and fine-tuning.",
     "Explain self-supervised pretraining and its objectives.",
     "Apply parameter-efficient fine-tuning.",
     "State when transfer fails.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why it works",
   "blurb": "The hierarchy from Module 05, exploited."},

  {"t": "callout", "title": "Early features are general; late features are task-specific",
   "kind": "The mechanism",
   "body": ["<b>Module 05 §2 found that early layers learn edges "
            "and colours, middle layers textures and parts, late layers "
            "objects.</b>",
            "<b>Edges are edges regardless of the task.</b> So the early "
            "layers of a model trained on anything visual are useful for "
            "everything visual.",
            "<b>Late layers encode the specific categories trained "
            "on</b>, and are what you replace.",
            "<b>So transfer is: keep the general part, replace the "
            "specific part, and optionally adjust the middle.</b> <b>The "
            "transferability declines smoothly with depth</b>, which is "
            "measurable and tells you how much to freeze."]},

  {"t": "table", "kicker": "Strategies", "title": "How much to adapt",
   "header": ["Strategy", "What changes", "Use when"],
   "widths": [2.8, 4.2, 5.1],
   "rows": [
     ["<b>Feature extraction</b>", "<b>Only a new head; backbone frozen</b>", "<b>Very little data; very different compute budget</b>"],
     ["<b>Fine-tune the last layers</b>", "Head plus the top block or two", "<b>Moderate data; similar domain</b>"],
     ["<b>Full fine-tuning</b>", "<b>Everything, at a low learning rate</b>", "<b>Plenty of data; domain shift</b>"],
     ["<b>LoRA / adapters</b>", "<b>Small added matrices only</b>", "<b>Large models; many tasks; limited memory</b>"],
     ["Prompting / in-context", "<b>Nothing — no training at all</b>", "Very large models; few examples"],
   ],
   "footnote": "<b>Use a much lower learning rate when fine-tuning</b> "
               "— typically 10 to 100&times; lower — or the "
               "first few steps destroy the pretrained features.",
   "note": "Catastrophic forgetting from too high an LR is the classic "
           "fine-tuning failure."},

  {"t": "section", "label": "Part 2", "title": "Self-supervision",
   "blurb": "Labels from the data itself."},

  {"t": "callout", "title": "The pretext task creates labels from structure",
   "kind": "The idea that removed the labelling bottleneck",
   "body": ["<b>Supervised pretraining needs labels, and labels are the "
            "expensive thing</b> (CSCE 633 M11 §4).",
            "<b>Self-supervision invents a task whose labels come from "
            "the data:</b> predict the next token, predict a masked "
            "patch, decide whether two crops come from the same image.",
            "<b>Solving it requires learning useful structure</b>, and "
            "the representation transfers even though nobody cares about "
            "the pretext task itself.",
            "<b>This is why language models scale:</b> <b>the internet is "
            "a labelled dataset if the label is 'the next word'</b> — "
            "which removed the constraint that had bounded every previous "
            "approach."]},

  {"t": "table", "kicker": "Objectives", "title": "The pretraining objectives that work",
   "header": ["Objective", "Signal", "Domain"],
   "widths": [2.8, 4.3, 5.0],
   "rows": [
     ["<b>Next-token prediction</b>", "<b>The next element of the sequence</b>", "<b>Text. The dominant one</b>"],
     ["<b>Masked prediction</b>", "Reconstruct hidden parts", "<b>Text (BERT), images (MAE)</b>"],
     ["<b>Contrastive</b>", "<b>Same image’s crops agree; others differ</b>", "<b>Images. SimCLR, MoCo</b>"],
     ["<b>Multimodal contrastive</b>", "<b>Image and its caption agree</b>", "<b>CLIP — and it changed everything</b>"],
     ["Denoising", "Reconstruct from a corrupted input", "<b>Generalises; the diffusion link (M10)</b>"],
   ],
   "footnote": "<b>CLIP's image–text alignment produced a "
               "representation usable without any task-specific "
               "training</b>, which was not expected.",
   "note": "CLIP is the one with the broadest downstream consequences."},

  {"t": "section", "label": "Part 3", "title": "Parameter-efficient tuning",
   "blurb": "Adapting a large model cheaply."},

  {"t": "code", "kicker": "LoRA", "title": "Low-rank adaptation",
   "lang": "text", "code": """
  OBSERVATION: the WEIGHT UPDATE during fine-tuning has low
  intrinsic rank -- the model does not need to move in many
  directions to adapt to a new task.

  SO instead of updating W (d x k), learn
      W' = W + BA        where B is d x r, A is r x k,  r << d

  PARAMETERS TRAINED: r(d + k)  instead of  dk
      d = k = 4096, r = 8  ->  65,536  instead of  16,777,216
      a 256x reduction

  PROPERTIES
    * W is FROZEN, so the pretrained knowledge cannot be destroyed
    * BA can be MERGED into W after training -- zero inference cost
    * many task-specific adapters can share one base model, which
      is the real deployment win
    * initialise B to ZERO so the adapted model starts identical
      to the base model

  Quality is typically within a point or two of full fine-tuning
  on most tasks, at a small fraction of the memory.
""",
   "caption": "<b>Zero inference cost after merging</b> is what makes this "
              "a deployment technique rather than only a training one.",
   "note": "The B=0 initialisation detail is the one people miss."},

  {"t": "section", "label": "Part 4", "title": "When it fails",
   "blurb": "The honest boundary."},

  {"t": "callout", "title": "Transfer fails when the domains genuinely differ",
   "kind": "The limits",
   "body": ["<b>Natural images to medical scans transfers "
            "poorly</b> — the low-level statistics differ, and studies "
            "find much of the benefit comes from the <i>scale</i> of the "
            "pretrained model rather than its features.",
            "<b>Natural images to satellite or microscopy:</b> different "
            "scale, different invariances, different noise.",
            "<b>And negative transfer is real</b> — a pretrained model "
            "can do worse than random initialisation when the source "
            "domain's biases actively mislead.",
            "<b>So measure it.</b> <b>Train from scratch as a baseline "
            "whenever transfer is used</b>, which is CSCE 633 Module 01's "
            "rule applied here and is routinely skipped."]},

  {"t": "bullets", "kicker": "Practice", "title": "Fine-tuning without breaking it",
   "items": [
     "<b>Use a much lower learning rate</b> — 10 to 100&times; below "
     "what you would use from scratch.",
     "",
     "<b>Warm up</b>, and consider freezing the backbone for the first "
     "epoch while the new head stabilises.",
     "",
     "<b>Discriminative learning rates</b> — lower for early layers, "
     "higher for late ones, matching how much each should move.",
     "",
     "<b>Watch for catastrophic forgetting</b> if the model must retain "
     "its original ability.",
     "",
     "<b>And evaluate on the original task too</b> when that matters — "
     "fine-tuning is lossy.",
   ],
   "footnote": "<b>A randomly initialised head producing large gradients "
               "into a pretrained backbone</b> is the usual cause of "
               "destroyed features in the first few steps."},
 ],
 "takeaways": [
   "Early layers learn general features and late layers task-specific ones, "
   "so transfer keeps the general part and replaces the specific part.",
   "Transferability declines smoothly with depth, which is measurable and "
   "tells you how much to freeze.",
   "Self-supervision invents a task whose labels come from the data's own "
   "structure, which removed the labelling bottleneck.",
   "The internet is a labelled dataset if the label is 'the next word' "
   "— which is why language models scale.",
   "LoRA exploits the low intrinsic rank of the fine-tuning update, trains "
   "hundreds of times fewer parameters, and merges to zero inference cost.",
   "Negative transfer is real, so train from scratch as a baseline whenever "
   "transfer is used.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why transfer works"),
  ("callout", "Early features are general; late features are specific",
   ["<b>Module 05 &sect;2 found that early layers learn edge and colour "
    "detectors, middle layers textures and parts, and late layers whole "
    "objects</b> — a hierarchy that emerged rather than being "
    "designed.",
    "<b>Edges are edges regardless of the task.</b> So the early layers of "
    "a model trained on <i>anything</i> visual are useful for <i>everything</i> "
    "visual, and there is no reason to learn them again from a thousand "
    "examples when they were learned once from a million.",
    "<b>Late layers encode the specific categories the model was trained "
    "on</b>, and those are exactly what you discard and replace with a head "
    "for the new task.",
    "<b>So transfer is: keep the general part, replace the specific part, "
    "and optionally adjust the middle.</b> <b>Transferability declines "
    "smoothly with depth</b> — which has been measured directly, layer "
    "by layer — <b>and the measurement tells you how much to "
    "freeze</b> rather than requiring a guess."]),
  ("table", ["Strategy", "What changes", "Use when"],
   [["<b>Feature extraction</b>",
     "<b>Only a new head; the backbone is frozen entirely.</b>",
     "<b>Very little data</b> (hundreds of examples), or a deployment "
     "budget that cannot afford to store a full model per task. Fast and "
     "nearly impossible to get wrong."],
    ["<b>Fine-tune the last layers</b>",
     "The head plus the top block or two.",
     "<b>Moderate data and a similar domain.</b> A sensible default."],
    ["<b>Full fine-tuning</b>",
     "<b>Every parameter, at a much lower learning rate.</b>",
     "<b>Plenty of data, or a genuine domain shift</b> that the early "
     "features do not cover."],
    ["<b>LoRA and adapters</b>",
     "<b>Only small added matrices; the base weights stay frozen.</b>",
     "<b>Large models, many tasks, or limited memory</b> — &sect;3."],
    ["<b>Prompting / in-context learning</b>",
     "<b>Nothing. No gradient step at all.</b>",
     "Very large models with a handful of examples, where the adaptation "
     "happens in the forward pass."]],
   [0.19, 0.36, 0.45]),

  ("h1", "2 &nbsp; Self-supervised pretraining"),
  ("callout", "The pretext task creates labels from structure",
   ["<b>Supervised pretraining needs labels, and labels are the expensive "
    "and rate-limiting resource</b> (CSCE 633 Module 11 &sect;4) — "
    "ImageNet's fourteen million labels took years and considerable money.",
    "<b>Self-supervision invents a task whose labels come from the data "
    "itself:</b> predict the next token in a sentence; reconstruct a masked "
    "patch of an image; decide whether two crops came from the same "
    "photograph. <b>No annotation is required at any point.</b>",
    "<b>Solving the pretext task requires learning genuinely useful "
    "structure</b> — you cannot predict the next word without "
    "representing syntax, semantics, and a good deal of world knowledge "
    "— <b>and that representation transfers</b>, even though nobody "
    "cares about the pretext task's output.",
    "<b>This is why language models scale as they do.</b> <b>The internet "
    "is a labelled dataset if the label is 'the next word'</b> — which "
    "removed, at a stroke, the data constraint that had bounded every "
    "previous approach. <b>The bottleneck moved from labelling to "
    "compute</b>, and compute was something that could be bought."]),
  ("table", ["Objective", "Where the signal comes from", "Domain"],
   [["<b>Next-token prediction</b>",
     "<b>The next element of the sequence, which the data already "
     "contains.</b>",
     "<b>Text, and the dominant objective by a wide margin.</b> Also audio "
     "and increasingly video."],
    ["<b>Masked prediction</b>",
     "Hide part of the input and reconstruct it from the rest.",
     "<b>Text (BERT) and images (masked autoencoders)</b>, where masking a "
     "large fraction of patches turns out to work remarkably well."],
    ["<b>Contrastive</b>",
     "<b>Two augmented crops of one image should agree; crops of different "
     "images should not.</b>",
     "<b>Images — SimCLR, MoCo.</b> Requires careful augmentation "
     "design, since the augmentations define what the model is told to be "
     "invariant to (Module 04 &sect;4)."],
    ["<b>Multimodal contrastive</b>",
     "<b>An image and its caption should agree; mismatched pairs should "
     "not.</b>",
     "<b>CLIP — and it changed a great deal.</b> See below."],
    ["<b>Denoising</b>",
     "Reconstruct a clean input from a corrupted one.",
     "<b>Generalises widely, and is the direct link to diffusion "
     "models</b> (Module 10 &sect;3)."]],
   [0.21, 0.38, 0.41]),
  ("p", "<b>CLIP's contribution was larger than a better representation.</b> "
        "By aligning images and text in one embedding space it produced a "
        "model that could classify into arbitrary categories specified in "
        "natural language, with no task-specific training at all — "
        "<b>zero-shot classification, which was not expected to work</b>. "
        "It also became the text-conditioning mechanism for image "
        "generation (Module 10), which is how a single pretraining "
        "objective ended up underneath most of generative vision."),

  ("break",),
  ("h1", "3 &nbsp; Parameter-efficient fine-tuning"),
  ("code", """OBSERVATION: the weight UPDATE during fine-tuning has low
intrinsic rank -- adapting to a new task does not require moving
in many directions.

SO instead of updating W (d x k), learn
    W' = W + BA      B is d x r,  A is r x k,  r << d

PARAMETERS TRAINED:  r(d+k)  instead of  dk
    d = k = 4096, r = 8  ->  65,536  rather than  16,777,216
    a 256x reduction

PROPERTIES
  * W is FROZEN, so pretrained knowledge cannot be destroyed
  * BA MERGES into W after training -- ZERO inference cost
  * many task adapters share one base model: the real
    deployment win
  * initialise B to ZERO so the adapted model starts EXACTLY
    equal to the base model

Quality is typically within a point or two of full fine-tuning,
at a small fraction of the memory."""),
  ("p", "<b>The zero-initialisation of B is the detail people miss.</b> It "
        "makes the product BA exactly zero at the start, so training begins "
        "from the pretrained model rather than from a perturbed version of "
        "it — which matters because the adapter's randomly initialised "
        "weights would otherwise inject noise into a model that was already "
        "good. <b>It is the same idea as initialising residual branches "
        "near zero</b> (Module 03 &sect;3)."),

  ("h1", "4 &nbsp; When transfer fails"),
  ("callout", "Transfer fails when the domains genuinely differ",
   ["<b>Natural images to medical imaging transfers poorly.</b> The "
    "low-level statistics are different, the relevant features are "
    "different, and <b>careful studies have found that much of the apparent "
    "benefit comes from the <i>scale</i> of the pretrained model and from "
    "better initialisation statistics rather than from the transferred "
    "features themselves</b> — a much weaker claim than 'ImageNet "
    "features help'.",
    "<b>Natural images to satellite imagery, to microscopy, to "
    "infrared:</b> different spatial scales, different invariances (a "
    "satellite image has no canonical 'up' for objects), different noise "
    "characteristics.",
    "<b>And negative transfer is real.</b> <b>A pretrained model can "
    "perform <i>worse</i> than random initialisation</b> when the source "
    "domain's biases actively mislead — the model arrives committed to "
    "features that are wrong for the target and must unlearn them.",
    "<b>So measure it.</b> <b>Train from scratch as a baseline whenever "
    "transfer is used</b>, on the same data and the same split. This is "
    "CSCE 633 Module 01 &sect;4's baseline rule applied to transfer, "
    "<b>and it is routinely skipped</b> because transfer is assumed to help "
    "— which it usually does, and not always, and the difference is "
    "one extra training run."]),
  ("ul", ["<b>Use a much lower learning rate</b> — typically 10 to "
          "100&times; below what you would use training from scratch. "
          "<b>Too high a rate destroys the pretrained features in the first "
          "few steps</b>, which is the classic fine-tuning failure and "
          "looks like 'transfer did not help'.",
          "<b>Warm up, and consider freezing the backbone for the first "
          "epoch</b> while the randomly initialised head stabilises. <b>A "
          "random head produces large gradients flowing into a good "
          "backbone</b>, which is precisely the mechanism that destroys "
          "it.",
          "<b>Discriminative learning rates:</b> lower for early layers, "
          "higher for late ones, matching &sect;1's finding about how much "
          "each layer should move.",
          "<b>Watch for catastrophic forgetting</b> if the model must "
          "retain its original capability — fine-tuning on a narrow "
          "task degrades performance on everything else, sometimes "
          "sharply.",
          "<b>And evaluate on the original task as well as the new one</b> "
          "when that matters. <b>Fine-tuning is lossy</b>, and the loss is "
          "invisible if you only measure the thing you tuned for."]),
 ],
 "resources": [
   ("Yosinski, Clune, Bengio & Lipson &mdash; How transferable are "
    "features in deep neural networks? (free)",
    "https://arxiv.org/abs/1411.1792",
    "<b>The &sect;1 measurement</b> — transferability layer by layer, "
    "including the negative transfer result."),
   ("Radford et al. &mdash; Learning Transferable Visual Models From "
    "Natural Language Supervision (CLIP) (free)",
    "https://arxiv.org/abs/2103.00020",
    "<b>The &sect;2 objective with the broadest consequences.</b> The "
    "zero-shot results section is the surprising part."),
   ("Hu et al. &mdash; LoRA: Low-Rank Adaptation of Large Language Models "
    "(free)",
    "https://arxiv.org/abs/2106.09685",
    "The &sect;3 method, including the intrinsic-rank evidence that "
    "motivates it."),
   ("Raghu et al. &mdash; Transfusion: Understanding Transfer Learning "
    "for Medical Imaging (free)",
    "https://arxiv.org/abs/1902.07208",
    "<b>The &sect;4 caution, measured carefully.</b> Required reading "
    "before claiming ImageNet pretraining helped."),
 ],
 "exercises": [
   "<b>Fine-tune a pretrained model</b> on your project and compare "
   "against training from scratch on the same split.",
   "<b>Measure transferability by depth:</b> freeze the first k layers for "
   "k from 0 to all, and plot accuracy against k.",
   "<b>Use too high a learning rate</b> when fine-tuning and demonstrate "
   "the destroyed features.",
   "Add warmup and backbone freezing for the first epoch, and compare.",
   "Implement a contrastive self-supervised objective and pretrain on "
   "unlabelled data.",
   "<b>Vary the augmentations</b> in that objective and show the "
   "representation changes accordingly.",
   "<b>Implement LoRA</b> and compare against full fine-tuning on quality, "
   "memory, and training time.",
   "<b>Initialise B randomly instead of zero</b> and report what "
   "happens.",
   "Merge the LoRA weights and verify inference is identical in cost to "
   "the base model.",
   "<b>Find a domain pair where transfer hurts</b> and document it.",
 ],
 "selfcheck": [
   "Why do pretrained features transfer, and how does transferability vary "
   "with depth?",
   "Compare five adaptation strategies and when each applies.",
   "What is a pretext task, and why did self-supervision matter so much?",
   "Give five pretraining objectives and their domains.",
   "What did CLIP make possible that was not expected?",
   "Explain LoRA's observation, its parameter saving, and its deployment "
   "advantage.",
   "Why initialise B to zero?",
   "Give three cases where transfer fails, and the baseline you must run.",
   "Give five practices for fine-tuning without destroying the model.",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Generative Models",
 "subtitle": "Learning a distribution instead of a mapping.",
 "question": "How do you learn to produce samples rather than "
             "predictions?",
 "outcomes": [
     "Distinguish the generative model families by what they optimise.",
     "Explain VAEs and the reparameterisation trick.",
     "Explain GANs and why they are hard to train.",
     "Explain diffusion models and why they won.",
     "Explain classifier-free guidance and conditioning.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "A different objective entirely."},

  {"t": "callout", "title": "Generative modelling learns p(x), not p(y|x)",
   "kind": "The shift",
   "body": ["<b>A discriminative model maps inputs to outputs.</b> A "
            "generative model learns the <i>distribution</i> the data came "
            "from, so it can produce new samples.",
            "<b>That is a much harder problem</b> — you must capture "
            "everything about the data, not only what distinguishes the "
            "classes.",
            "<b>And evaluation is genuinely hard.</b> There is no "
            "held-out accuracy; 'is this a good sample?' resists "
            "measurement, and the standard metrics are known to be "
            "flawed.",
            "<b>The families differ in how they make the problem "
            "tractable</b>, and each makes a different compromise between "
            "sample quality, diversity, and whether the likelihood is "
            "computable."]},

  {"t": "table", "kicker": "Families", "title": "The four approaches",
   "header": ["Family", "Optimises", "Trade"],
   "widths": [2.6, 4.3, 5.2],
   "rows": [
     ["<b>Autoregressive</b>", "<b>Exact likelihood, factorised</b>", "<b>Excellent quality; sequential, so slow to sample</b>"],
     ["<b>VAE</b>", "<b>A lower bound on the likelihood</b>", "<b>Fast, stable, and blurry</b>"],
     ["<b>GAN</b>", "<b>A minimax game against a critic</b>", "<b>Sharp; unstable; mode collapse</b>"],
     ["<b>Diffusion</b>", "<b>Denoising at many noise levels</b>", "<b>Best quality; stable; slow sampling</b>"],
     ["Normalising flows", "Exact likelihood via invertible maps", "<b>Exact; architecturally constrained</b>"],
   ],
   "footnote": "<b>Diffusion won image generation</b> because it has "
               "GAN-level quality with VAE-level training stability "
               "— which nothing else offered.",
   "note": "That one sentence explains the field's shift around 2021."},

  {"t": "section", "label": "Part 2", "title": "VAEs",
   "blurb": "A latent variable model, made trainable."},

  {"t": "callout", "title": "The reparameterisation trick makes sampling differentiable",
   "kind": "The idea that makes VAEs work",
   "body": ["<b>A VAE encodes an input to a <i>distribution</i> over "
            "latents, samples from it, and decodes.</b> The sampling step "
            "is the problem — you cannot backpropagate through a random "
            "draw.",
            "<b>So move the randomness outside the computation:</b> "
            "instead of sampling z ~ N(μ, σ²), compute "
            "z = μ + σ·ε with ε ~ N(0,1).",
            "<b>Now ε is an input, not an operation</b>, and the "
            "gradient flows through μ and σ normally.",
            "<b>That single restructuring is what made latent variable "
            "models trainable by gradient descent</b>, and the same trick "
            "appears throughout machine learning wherever a stochastic node "
            "must be differentiated."]},

  {"t": "callout", "title": "Why VAE samples are blurry",
   "kind": "The characteristic failure",
   "body": ["<b>The reconstruction loss is typically squared error</b>, "
            "which is maximum likelihood under Gaussian noise "
            "(CSCE 633 M10 §1).",
            "<b>Squared error is minimised by the <i>mean</i> of the "
            "plausible outputs.</b> If several sharp images are equally "
            "consistent with a latent, their average minimises the loss.",
            "<b>And the average of several sharp images is a blurry "
            "one.</b>",
            "<b>So the blur is the loss function working correctly</b>, "
            "not a capacity failure — which is why replacing the "
            "reconstruction loss (with a perceptual or adversarial one) is "
            "the fix, and adding parameters is not."]},

  {"t": "section", "label": "Part 3", "title": "Diffusion",
   "blurb": "The one that won."},

  {"t": "code", "kicker": "Diffusion", "title": "Destroy the data, then learn to undo it",
   "lang": "text", "code": """
  FORWARD PROCESS -- fixed, no learning at all
      repeatedly add a little Gaussian noise, T steps,
      until the image is indistinguishable from pure noise.
      Closed form: you can jump to any step t directly.

  REVERSE PROCESS -- learned
      train a network to predict the noise that was added at
      step t, given the noisy image and t.
      Loss: simple mean squared error on the predicted noise.

  SAMPLING
      start from pure noise, apply the learned denoiser
      repeatedly, stepping t down to 0.

  WHY THIS WORKS SO WELL
    * the training objective is a STABLE regression problem --
      no adversarial game, no balance to maintain
    * each step is an EASY problem (remove a little noise);
      the hard problem is decomposed into many easy ones
    * and the model sees every noise level, so it learns both
      coarse structure (high noise) and fine detail (low noise)

  THE COST: sampling needs many network evaluations. DDIM and
  distillation reduce 1000 steps to 20, or even to 1.
""",
   "caption": "<b>Decomposing a hard problem into many easy ones</b> is "
              "the whole idea, and it is why training is so much more "
              "stable than a GAN's.",
   "note": "The 'many easy problems' framing is the clearest way in."},

  {"t": "callout", "title": "Classifier-free guidance controls the quality/diversity trade",
   "kind": "The mechanism behind text-to-image",
   "body": ["<b>Train one model both conditionally and "
            "unconditionally</b>, by randomly dropping the condition "
            "during training.",
            "<b>At sampling, extrapolate away from the unconditional "
            "prediction</b> toward the conditional one, by a guidance "
            "scale.",
            "<b>High guidance means samples adhere closely to the prompt "
            "and are less diverse</b>; low guidance gives diversity and "
            "weaker adherence.",
            "<b>So one knob trades prompt fidelity against variety</b>, "
            "at sampling time with no retraining — which is most of why "
            "text-to-image systems feel controllable."]},

  {"t": "section", "label": "Part 4", "title": "Evaluation",
   "blurb": "The part that is not solved."},

  {"t": "bullets", "kicker": "Metrics", "title": "How generative models are scored, and the problems",
   "items": [
     "<b>FID</b> — distance between feature statistics of real and "
     "generated sets. <b>The standard, and it is sensitive to "
     "implementation details and to sample count.</b>",
     "",
     "<b>Inception Score</b> — older, and it cannot detect mode "
     "collapse within a class.",
     "",
     "<b>Precision and recall for generative models</b> — separates "
     "quality from coverage, which a single number cannot.",
     "",
     "<b>Human evaluation</b> — expensive, and still the only thing "
     "that measures what is actually wanted.",
     "",
     "<b>And likelihood, where it is available</b> — which "
     "correlates poorly with perceived sample quality.",
   ],
   "footnote": "<b>Report samples, including failures.</b> A metric in "
               "this area is a summary of something nobody has defined "
               "precisely."},
 ],
 "takeaways": [
   "Generative modelling learns the distribution rather than a mapping, "
   "which is harder and resists evaluation.",
   "Diffusion won image generation because it has GAN-level quality with "
   "VAE-level training stability.",
   "The reparameterisation trick moves randomness into an input so the "
   "gradient can flow through the distribution's parameters.",
   "VAE blur is the squared-error loss working correctly — it is "
   "minimised by the mean of plausible outputs.",
   "Diffusion decomposes one hard generation problem into many easy "
   "denoising problems, each a stable regression.",
   "Classifier-free guidance trades prompt adherence against diversity with "
   "one knob at sampling time.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The problem"),
  ("callout", "Generative modelling learns p(x), not p(y|x)",
   ["<b>A discriminative model learns a mapping from inputs to outputs.</b> "
    "A generative model learns the <i>distribution</i> the data was drawn "
    "from, well enough to produce new samples from it.",
    "<b>That is a substantially harder problem.</b> A classifier needs only "
    "to represent what distinguishes the classes and may ignore everything "
    "else; a generative model must capture everything about the data, "
    "including all the structure that no label ever referred to.",
    "<b>And evaluation is genuinely hard.</b> There is no held-out "
    "accuracy. <b>'Is this a good sample?' resists measurement</b>, the "
    "standard metrics are known to be flawed (&sect;4), and the thing you "
    "actually want — samples a person would judge good and varied "
    "— has no agreed formalisation.",
    "<b>The families differ in how they make the problem tractable</b>, and "
    "each makes a different compromise among sample quality, sample "
    "diversity, sampling speed, and whether the likelihood can be computed "
    "at all."]),
  ("table", ["Family", "What it optimises", "The trade"],
   [["<b>Autoregressive</b>",
     "<b>The exact likelihood, factorised as a product of "
     "conditionals.</b>",
     "<b>Excellent quality and a tractable likelihood</b>; <b>sampling is "
     "sequential and therefore slow</b>, element by element. The dominant "
     "approach for text (Module 07)."],
    ["<b>Variational autoencoder</b>",
     "<b>A lower bound on the likelihood</b> (the ELBO).",
     "<b>Fast to sample, stable to train, and blurry</b> — for the "
     "reason in &sect;2."],
    ["<b>GAN</b>",
     "<b>A minimax game between a generator and a discriminator.</b> No "
     "likelihood at all.",
     "<b>Sharp samples; notoriously unstable training; mode collapse</b>, "
     "where the generator produces a few outputs that fool the "
     "discriminator and abandons the rest of the distribution."],
    ["<b>Diffusion</b>",
     "<b>Denoising at many noise levels</b> — a simple regression "
     "objective.",
     "<b>Best sample quality, stable training, slow sampling</b> (many "
     "network evaluations), which distillation addresses."],
    ["<b>Normalising flows</b>",
     "Exact likelihood via a sequence of invertible transformations.",
     "<b>Exact and elegant</b>; the invertibility requirement heavily "
     "constrains the architecture, which limits capacity."]],
   [0.19, 0.37, 0.44]),
  ("p", "<b>Diffusion won image generation because it offered GAN-level "
        "sample quality with VAE-level training stability</b>, which "
        "nothing else did. <b>That single sentence explains the field's "
        "shift around 2021</b> — GANs had the quality and were "
        "miserable to train; VAEs trained easily and produced blur; "
        "diffusion took the good half of each."),

  ("h1", "2 &nbsp; Variational autoencoders"),
  ("callout", "The reparameterisation trick makes sampling differentiable",
   ["<b>A VAE encodes an input to a <i>distribution</i> over latent "
    "variables — a mean and a variance — samples a latent from "
    "it, and decodes that sample back to the input space.</b> <b>The "
    "sampling step is the problem:</b> you cannot backpropagate through a "
    "random draw, because the draw is not a differentiable function of its "
    "parameters.",
    "<b>So move the randomness outside the computation.</b> Instead of "
    "sampling z ~ N(&mu;, &sigma;&#178;) directly, sample &epsilon; ~ "
    "N(0, 1) and compute <b>z = &mu; + &sigma;&middot;&epsilon;</b>.",
    "<b>Now &epsilon; is an <i>input</i> to the graph rather than an "
    "operation within it</b>, and the gradient flows through &mu; and "
    "&sigma; by ordinary arithmetic — Module 02's machinery applies "
    "without modification.",
    "<b>That single restructuring is what made latent variable models "
    "trainable by gradient descent</b>, and <b>the same trick appears "
    "throughout machine learning</b> wherever a stochastic node must be "
    "differentiated through — in reinforcement learning, in "
    "variational inference generally, and in the Gumbel-softmax relaxation "
    "for discrete choices. <b>It is one of the most reusable ideas in this "
    "course.</b>"]),
  ("callout", "Why VAE samples are blurry",
   ["<b>The reconstruction term is typically squared error</b>, which is "
    "maximum likelihood under an assumption of Gaussian output noise "
    "(CSCE 633 Module 10 &sect;1) — an assumption nobody examined "
    "and which is doing a great deal of work.",
    "<b>Squared error is minimised by the <i>mean</i> of the plausible "
    "outputs.</b> If several different sharp images are equally consistent "
    "with a given latent code, the loss is lowest at their average rather "
    "than at any one of them.",
    "<b>And the average of several sharp images is a blurry image.</b> "
    "The model is not failing to represent sharpness; it is correctly "
    "declining to commit.",
    "<b>So the blur is the loss function working exactly as specified</b>, "
    "not a capacity failure — <b>which is why adding parameters does "
    "not fix it and changing the reconstruction loss does</b>. Perceptual "
    "losses, adversarial losses, and discrete latent spaces (VQ-VAE) are "
    "all attacks on this one issue, and the VQ-VAE route — a discrete "
    "latent plus an autoregressive prior — became the basis of several "
    "strong systems."]),

  ("break",),
  ("h1", "3 &nbsp; Diffusion"),
  ("code", """FORWARD PROCESS -- fixed, nothing learned
  repeatedly add a little Gaussian noise over T steps until the
  image is indistinguishable from pure noise.
  Closed form: you can jump directly to any step t.

REVERSE PROCESS -- learned
  train a network to predict the NOISE that was added at step t,
  given the noisy image and t.
  Loss: plain mean squared error on the predicted noise.

SAMPLING
  start from pure noise and apply the denoiser repeatedly,
  stepping t down to 0.

WHY IT WORKS SO WELL
  * the training objective is a STABLE regression -- no
    adversarial game and no balance to maintain
  * each step is an EASY problem (remove a little noise);
    one hard problem decomposed into many easy ones
  * the model sees every noise level, so it learns coarse
    structure (high noise) and fine detail (low noise)

COST: sampling needs many network evaluations. DDIM and
distillation take 1000 steps down to 20, or to 1."""),
  ("callout", "Classifier-free guidance controls quality against diversity",
   ["<b>Train a single model both conditionally and unconditionally</b>, by "
    "randomly dropping the conditioning signal (the text embedding, the "
    "class label) on some fraction of training examples.",
    "<b>At sampling time, extrapolate away from the unconditional "
    "prediction toward the conditional one:</b> the guided prediction is "
    "the unconditional one plus a scale factor times the difference. "
    "<b>A scale of 1 is ordinary conditional sampling; higher scales "
    "exaggerate the conditioning.</b>",
    "<b>High guidance produces samples that adhere closely to the prompt "
    "and are less diverse</b> — and eventually over-saturated and "
    "artefact-laden. <b>Low guidance gives diversity and weaker "
    "adherence.</b>",
    "<b>So a single knob trades prompt fidelity against variety, at "
    "sampling time, with no retraining</b> — <b>which is most of why "
    "text-to-image systems feel controllable</b>, and it is a rare case of "
    "a technique that is both simple to implement and decisive for the "
    "user experience."]),

  ("h1", "4 &nbsp; Evaluation"),
  ("ul", ["<b>Fr&eacute;chet Inception Distance (FID).</b> The distance "
          "between Gaussian fits to the Inception features of real and "
          "generated sets. <b>The standard metric, and it is sensitive to "
          "the sample count, the resizing method, and the exact Inception "
          "implementation</b> — published FIDs are frequently not "
          "comparable across papers, which is a measurement problem of "
          "exactly the kind CSCE 633 Module 12 described.",
          "<b>Inception Score.</b> Older, and <b>it cannot detect mode "
          "collapse within a class</b> — a model producing one perfect "
          "image per class scores well.",
          "<b>Precision and recall for generative models.</b> Separates "
          "<i>quality</i> (are the samples realistic?) from <i>coverage</i> "
          "(do they span the distribution?), <b>which a single number "
          "cannot</b> — and the two fail in different ways, so "
          "reporting both is far more informative.",
          "<b>Human evaluation.</b> Expensive, slow, and <b>still the only "
          "thing that measures what is actually wanted</b> — with all "
          "the inter-annotator agreement caveats of CSCE 633 Module 11 "
          "&sect;4.",
          "<b>And likelihood, where the family provides it</b> — which "
          "<b>correlates surprisingly poorly with perceived sample "
          "quality</b>, a known and somewhat embarrassing result for the "
          "likelihood-based families. <b>Report samples, including "
          "failures</b>: in this area a metric is a summary of something "
          "nobody has defined precisely, and the pictures carry more "
          "information than the number."]),
 ],
 "resources": [
   ("Lilian Weng &mdash; What are Diffusion Models? (free)",
    "https://lilianweng.github.io/posts/2021-07-11-diffusion-models/",
    "<b>The clearest derivation of &sect;3 available</b>, including the "
    "connection to score matching."),
   ("Kingma & Welling &mdash; Auto-Encoding Variational Bayes (free)",
    "https://arxiv.org/abs/1312.6114",
    "<b>The &sect;2 reparameterisation trick</b>, from the paper that "
    "introduced it."),
   ("Ho, Jain & Abbeel &mdash; Denoising Diffusion Probabilistic Models "
    "(free)",
    "https://arxiv.org/abs/2006.11239",
    "The &sect;3 formulation that made diffusion practical, with the "
    "simplified objective."),
   ("Ho & Salimans &mdash; Classifier-Free Diffusion Guidance (free)",
    "https://arxiv.org/abs/2207.12598",
    "The &sect;3 guidance mechanism. Two pages of idea and it is behind "
    "every text-to-image system."),
 ],
 "exercises": [
   "Implement a VAE on a small image dataset and <b>sample from the "
   "prior</b>.",
   "<b>Implement sampling without the reparameterisation trick</b> and "
   "show the gradient does not flow.",
   "<b>Demonstrate the blur mechanism:</b> average several sharp images "
   "and compare against your VAE's samples.",
   "Replace the squared-error reconstruction with a perceptual loss and "
   "compare sharpness.",
   "<b>Implement a diffusion model</b> on small images, with the simple "
   "noise-prediction objective.",
   "<b>Visualise the reverse process</b> — show the sample at several "
   "steps from noise to image.",
   "Implement DDIM sampling and plot quality against step count.",
   "<b>Implement classifier-free guidance</b> and sweep the guidance "
   "scale. Show the quality–diversity trade.",
   "<b>Compute FID with two different implementations</b> and report "
   "whether they agree.",
   "Compute precision and recall for your generative model and show they "
   "say different things.",
 ],
 "selfcheck": [
   "How does generative modelling differ from discriminative, and why is "
   "evaluation hard?",
   "Compare five generative families on what each optimises.",
   "Why did diffusion win image generation?",
   "State the reparameterisation trick and say what problem it solves.",
   "Why are VAE samples blurry, and what fixes it?",
   "Describe the diffusion forward and reverse processes.",
   "Give three reasons diffusion trains stably.",
   "Explain classifier-free guidance and what it trades.",
   "Give five generative metrics and the problem with each.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Neural Rendering",
 "subtitle": "Where this course meets the graphics track.",
 "question": "What happens when the renderer is differentiable?",
 "outcomes": [
     "Explain differentiable rendering and what it enables.",
     "Explain NeRF and the volume rendering integral it learns.",
     "Explain Gaussian splatting and why it is faster.",
     "Connect learned denoising to CSCE 647.",
     "State what neural rendering does not yet do well.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Differentiable rendering",
   "blurb": "Inverting the forward process."},

  {"t": "callout", "title": "If rendering is differentiable, you can optimise the scene",
   "kind": "The idea",
   "body": ["<b>Rendering maps a scene to an image</b> (CSCE 647). "
            "<b>Inverse rendering wants the scene from images</b>, which "
            "is the hard direction.",
            "<b>If the renderer is differentiable, the inverse problem "
            "becomes gradient descent:</b> render, compare to the "
            "photograph, backpropagate into the scene parameters, repeat.",
            "<b>Module 02 §1 said anything differentiable can be "
            "trained.</b> This is the most consequential instance of that "
            "in the graphics track.",
            "<b>The difficulty is discontinuity.</b> Visibility, "
            "occlusion, and hard edges are not differentiable — <b>and "
            "the whole field is about smooth relaxations of those "
            "discontinuities.</b>"]},

  {"t": "section", "label": "Part 2", "title": "NeRF",
   "blurb": "A scene as a function, optimised from photographs."},

  {"t": "code", "kicker": "NeRF", "title": "The representation and the rendering",
   "lang": "text", "code": """
  THE SCENE IS A FUNCTION, stored as network weights:
      F(x, y, z, theta, phi)  ->  (colour, density)

  RENDERING a pixel: march a ray and integrate (CSCE 647 M10 --
  this is the volume rendering integral, unchanged):

      C = integral over t of  T(t) * sigma(t) * c(t) dt
      where T(t) = exp( -integral of sigma ) is transmittance

  Discretised as a weighted sum over samples along the ray.
  EVERY OPERATION IS DIFFERENTIABLE, so the loss between the
  rendered pixel and the photographed pixel backpropagates all
  the way into the network weights.

  TRAINING: photographs with known camera poses. Render each
  pixel, compare, descend. That is the entire algorithm.

  POSITIONAL ENCODING IS ESSENTIAL
      a plain MLP on raw (x,y,z) produces a blurry scene -- it
      has a strong bias toward low frequencies. Mapping the
      coordinates through sin/cos at many frequencies first
      lets it represent fine detail. WITHOUT IT, NeRF DOES NOT
      WORK, and that was the paper's key practical finding.
""",
   "caption": "<b>The volume rendering integral is from CSCE 647 "
              "Module 10</b> — unchanged. What is new is "
              "differentiating through it.",
   "note": "The positional encoding necessity is the surprising practical "
           "detail."},

  {"t": "callout", "title": "What NeRF traded",
   "kind": "The honest accounting",
   "body": ["<b>It produced photorealistic novel views from a few dozen "
            "photographs</b>, which the classical pipeline "
            "(CSCE 748 M09) could not match.",
            "<b>And it was extremely slow</b> — days to train one scene, "
            "seconds to render one frame — because every pixel requires "
            "hundreds of network evaluations.",
            "<b>The scene is also opaque.</b> It is network weights, not "
            "geometry — <b>you cannot edit it, relight it easily, or "
            "export it to an engine</b>.",
            "<b>Instant-NGP cut training to seconds</b> with a hash-grid "
            "encoding, which was a representation change rather than a "
            "better network. <b>The representation was the "
            "bottleneck.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Gaussian splatting",
   "blurb": "An explicit representation that rasterises."},

  {"t": "table", "kicker": "Comparison", "title": "NeRF against 3D Gaussian splatting",
   "header": ["", "NeRF", "Gaussian splatting"],
   "widths": [2.5, 4.5, 5.1],
   "rows": [
     ["<b>Scene is</b>", "<b>Implicit — network weights</b>", "<b>Explicit — millions of 3D Gaussians</b>"],
     ["<b>Rendering</b>", "<b>Ray marching; many network evals</b>", "<b>Rasterise and alpha-blend. No network</b>"],
     ["<b>Speed</b>", "Seconds per frame (originally)", "<b>Real time, 100+ fps</b>"],
     ["<b>Training</b>", "Hours to days", "<b>Minutes</b>"],
     ["<b>Editable</b>", "<b>Barely</b>", "<b>Yes — primitives can be moved and culled</b>"],
     ["Memory", "Compact (weights)", "<b>Large — millions of primitives</b>"],
   ],
   "footnote": "<b>Splatting is differentiable rasterisation</b> "
               "(CSCE 641) rather than differentiable ray marching "
               "— and rasterisation is what GPUs are built for.",
   "note": "The 'it went back to rasterisation' point is the key "
           "insight."},

  {"t": "callout", "title": "Splatting won by matching the hardware",
   "kind": "The lesson",
   "body": ["<b>A NeRF evaluates a network hundreds of times per "
            "pixel.</b> Splatting projects primitives and blends them "
            "— <b>which is the rasterisation pipeline from "
            "CSCE 641</b>, with gradients.",
            "<b>GPUs have been optimised for exactly that for thirty "
            "years.</b>",
            "<b>So the speedup came from changing the representation to "
            "one the hardware already executes well</b>, not from a better "
            "model.",
            "<b>This is CSCE 735's argument in a new domain:</b> "
            "<b>matching the computation to the machine beat improving the "
            "algorithm</b>, by two orders of magnitude."]},

  {"t": "section", "label": "Part 4", "title": "The rest of the pipeline",
   "blurb": "Where else learning entered graphics."},

  {"t": "bullets", "kicker": "Elsewhere", "title": "Learned components in a modern renderer",
   "items": [
     "<b>Denoising</b> (CSCE 647 M12) — a CNN on a noisy render "
     "plus geometry buffers. <b>Made path tracing interactive.</b>",
     "",
     "<b>Super-resolution and frame generation</b> — render fewer "
     "pixels and fewer frames, reconstruct the rest.",
     "",
     "<b>Neural materials and BRDFs</b> — a network replacing a "
     "measured or analytic model, evaluated per shading point.",
     "",
     "<b>Learned importance sampling</b> — guide paths toward "
     "light, reducing variance (CSCE 647 M06).",
     "",
     "<b>And texture and asset generation</b> (Module 10), which "
     "changed content production rather than rendering.",
   ],
   "footnote": "<b>Denoising is the one that mattered most.</b> It changed "
               "what sample counts are economically viable, which changed "
               "what is renderable in real time."},

  {"t": "callout", "title": "What neural rendering still does not do well",
   "kind": "The honest boundary",
   "body": ["<b>Relighting.</b> Most captured representations bake in the "
            "lighting they were photographed under; separating material "
            "from illumination remains hard.",
            "<b>Editing and animation.</b> These representations are not "
            "meshes with skeletons, so the entire content pipeline "
            "(CSCE 645) does not apply.",
            "<b>Dynamic scenes</b> — adding time multiplies the problem "
            "and the methods are young.",
            "<b>And generalisation.</b> <b>Most methods optimise one "
            "scene from scratch</b>; a feed-forward model that "
            "reconstructs any scene from a few images is an active area "
            "rather than a solved one."]},
 ],
 "takeaways": [
   "If the renderer is differentiable, inverse rendering becomes gradient "
   "descent — and the difficulty is relaxing visibility "
   "discontinuities.",
   "A NeRF stores a scene as network weights and renders with CSCE 647's "
   "volume rendering integral, differentiated.",
   "Positional encoding is essential because an MLP on raw coordinates is "
   "strongly biased toward low frequencies.",
   "Instant-NGP cut NeRF training from days to seconds by changing the "
   "representation, not the network — the representation was the "
   "bottleneck.",
   "Gaussian splatting is differentiable rasterisation, which is what GPUs "
   "have been built for, and that is where its two orders of magnitude came "
   "from.",
   "Learned denoising mattered most of all, because it changed which sample "
   "counts are economically viable.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Differentiable rendering"),
  ("callout", "If rendering is differentiable, you can optimise the scene",
   ["<b>Rendering maps a scene description to an image</b>, and CSCE 647 "
    "spent a semester on doing that accurately. <b>Inverse rendering wants "
    "the scene <i>from</i> the images</b>, which is the hard direction and "
    "was the subject of CSCE 748's reconstruction material.",
    "<b>If the renderer is differentiable, the inverse problem becomes "
    "gradient descent:</b> render the current scene estimate, compare it "
    "against the photographs, backpropagate the difference into the scene "
    "parameters, and repeat. <b>The forward model becomes the loss "
    "function.</b>",
    "<b>Module 02 &sect;1 observed that anything differentiable can be "
    "trained.</b> <b>This is the most consequential instance of that "
    "observation in the graphics track</b>, and it reframes a classical "
    "estimation problem as an optimisation one.",
    "<b>The central difficulty is discontinuity.</b> Visibility, occlusion, "
    "and silhouette edges are not differentiable functions of geometry "
    "— moving a triangle by an infinitesimal amount can change which "
    "surface is visible at a pixel, discontinuously. <b>Much of the field "
    "is about smooth relaxations of exactly those discontinuities</b>: soft "
    "rasterisation, edge sampling, and volumetric representations that have "
    "no hard boundaries at all — which is part of why NeRF's "
    "volumetric formulation worked so well."]),

  ("h1", "2 &nbsp; NeRF"),
  ("code", """THE SCENE IS A FUNCTION, stored as network weights:
    F(x, y, z, theta, phi)  ->  (colour, density)

RENDERING a pixel: march a ray and integrate. This is CSCE 647
Module 10's VOLUME RENDERING INTEGRAL, unchanged:

    C = integral  T(t) * sigma(t) * c(t) dt
    where T(t) = exp(-integral of sigma)  is transmittance

Discretised as a weighted sum over samples along the ray.
EVERY OPERATION IS DIFFERENTIABLE, so the loss between rendered
and photographed pixels backpropagates into the weights.

TRAINING: photographs with known camera poses. Render, compare,
descend. That is the whole algorithm.

POSITIONAL ENCODING IS ESSENTIAL
  a plain MLP on raw (x,y,z) produces a blurry scene -- MLPs
  have a strong bias toward LOW FREQUENCIES. Mapping coordinates
  through sin/cos at many frequencies first lets the network
  represent fine detail. WITHOUT IT NeRF DOES NOT WORK, and
  that was the paper's key practical finding."""),
  ("p", "<b>The low-frequency bias of MLPs is a real and general "
        "phenomenon</b> — networks fit smooth functions far more "
        "readily than oscillatory ones — and the positional encoding "
        "fix recurs well beyond NeRF, including in transformers "
        "(Module 07 &sect;2), where sinusoids at many frequencies serve a "
        "related purpose. <b>It is a good example of a practical detail "
        "that looks like an implementation trick and is actually the "
        "load-bearing idea.</b>"),
  ("callout", "What NeRF traded",
   ["<b>It produced photorealistic novel views from a few dozen "
    "photographs</b>, with view-dependent effects — specularity, "
    "translucency — that the classical structure-from-motion and "
    "multi-view stereo pipeline (CSCE 748 Module 09) could not match.",
    "<b>And it was extremely slow.</b> Days to train a single scene and "
    "seconds to render a single frame, <b>because every pixel requires "
    "hundreds of network evaluations</b> along its ray — the "
    "arithmetic is simply enormous.",
    "<b>The scene is also opaque.</b> It is a set of network weights "
    "rather than geometry, so <b>you cannot edit it, relight it easily, "
    "collide against it, or export it to an engine</b> — which is a "
    "serious practical limitation for the graphics track's purposes.",
    "<b>Instant-NGP reduced training from days to seconds</b> by replacing "
    "the positional encoding with a multiresolution hash grid of learnable "
    "features, so that a much smaller network sufficed. <b>That was a "
    "representation change rather than a better network or a better "
    "optimiser</b> — <b>the representation was the bottleneck all "
    "along</b>, which is a lesson that recurs in &sect;3."]),

  ("break",),
  ("h1", "3 &nbsp; Gaussian splatting"),
  ("table", ["", "NeRF", "3D Gaussian splatting"],
   [["<b>The scene is</b>", "<b>Implicit — network weights.</b>",
     "<b>Explicit — millions of anisotropic 3D Gaussians with "
     "position, covariance, opacity, and view-dependent colour.</b>"],
    ["<b>Rendering</b>",
     "<b>Ray marching with hundreds of network evaluations per pixel.</b>",
     "<b>Project each Gaussian to the image plane, sort by depth, and "
     "alpha-blend. No network evaluation at render time at all.</b>"],
    ["<b>Speed</b>", "Seconds per frame originally; still not real time "
     "for high quality.",
     "<b>Real time — over 100 frames per second at 1080p.</b>"],
    ["<b>Training</b>", "Hours to days (seconds with Instant-NGP).",
     "<b>Minutes</b>, including adaptive densification and pruning of the "
     "primitive set."],
    ["<b>Editable</b>",
     "<b>Barely</b> — the scene is entangled in the weights.",
     "<b>Yes</b> — primitives are explicit objects that can be "
     "selected, moved, culled, and composited."],
    ["<b>Memory</b>", "Compact — a few megabytes of weights.",
     "<b>Large</b> — millions of primitives, hundreds of megabytes, "
     "which is the main practical cost."]],
   [0.16, 0.38, 0.46]),
  ("callout", "Splatting won by matching the hardware",
   ["<b>A NeRF evaluates a neural network hundreds of times per pixel.</b> "
    "<b>Splatting projects primitives and alpha-blends them</b> — "
    "which is <b>the rasterisation pipeline from CSCE 641</b>, with "
    "gradients attached and with Gaussians instead of triangles.",
    "<b>GPUs have been optimised for exactly that operation for thirty "
    "years.</b> Projection, depth sorting, and blending are what the fixed "
    "and programmable pipeline exist to do, and the hardware is enormously "
    "good at them.",
    "<b>So the two-orders-of-magnitude speedup came from changing the "
    "representation to one the hardware already executes well</b>, not from "
    "a better model, a better optimiser, or more parameters. The quality is "
    "comparable; the execution is entirely different.",
    "<b>This is CSCE 735's central argument arriving in a new "
    "domain:</b> <b>matching the computation to the machine beat improving "
    "the algorithm</b>, by a factor of a hundred. <b>And it is the same "
    "lesson as Instant-NGP's</b> (&sect;2) — twice in one module, "
    "from two different directions, which suggests it is the governing "
    "consideration in this area rather than a coincidence."]),

  ("h1", "4 &nbsp; Learned components elsewhere in the pipeline"),
  ("ul", ["<b>Denoising</b> (CSCE 647 Module 12, CSCE 636 Module 05 "
          "&sect;4) — a convolutional network taking a sparsely "
          "sampled noisy render plus geometry buffers. <b>It made path "
          "tracing interactive</b>, and <b>it is the one that mattered "
          "most</b>: by making 1-to-4 samples per pixel usable, it changed "
          "which sample counts are economically viable, which changed what "
          "is renderable in real time at all.",
          "<b>Super-resolution and frame generation</b> — render at "
          "lower resolution and lower frame rate and reconstruct the rest. "
          "Now standard in shipping engines rather than experimental.",
          "<b>Neural materials and BRDFs</b> — a small network "
          "replacing a measured or analytic reflectance model (CSCE 647 "
          "Module 07), evaluated per shading point. Compact, and it can "
          "represent measured materials that no analytic model fits.",
          "<b>Learned importance sampling</b> — a network guiding path "
          "directions toward light-carrying regions, reducing variance "
          "(CSCE 647 Module 06). The variance reduction is real and the "
          "overhead per sample is the constraint.",
          "<b>And texture, material, and asset generation</b> "
          "(Module 10) — which changed content production rather "
          "than rendering, and is arguably the larger economic effect."]),
  ("callout", "What neural rendering still does not do well",
   ["<b>Relighting.</b> Most captured representations bake in the "
    "illumination present when the photographs were taken. <b>Separating "
    "material from lighting from geometry is the classical inverse "
    "rendering problem</b> and it remains underdetermined — neural "
    "methods have not resolved it, only sometimes sidestepped it.",
    "<b>Editing and animation.</b> These representations are not meshes "
    "with skeletons, UVs, and material graphs, <b>so the entire content "
    "pipeline of CSCE 645 and every tool built on it does not apply</b>. "
    "This is the single largest obstacle to production adoption, and it is "
    "a tooling problem rather than a quality one.",
    "<b>Dynamic scenes.</b> Adding a time dimension multiplies the problem "
    "and the methods are young — quality under motion, and capture "
    "requirements, are both substantially worse.",
    "<b>And generalisation.</b> <b>Most methods optimise a single scene "
    "from scratch</b> rather than learning a prior over scenes; a "
    "feed-forward model that reconstructs any scene from a handful of "
    "images is an active research area rather than a solved problem. "
    "<b>Which means the techniques are currently closer to a capture "
    "pipeline than to a learned model</b>, and that distinction matters "
    "for how they are deployed."]),
 ],
 "resources": [
   ("Mildenhall et al. &mdash; NeRF: Representing Scenes as Neural "
    "Radiance Fields (free)",
    "https://www.matthewtancik.com/nerf",
    "<b>The &sect;2 method.</b> The positional encoding ablation is the "
    "part to read closely."),
   ("Kerbl, Kopanas, Leimk&uuml;hler & Drettakis &mdash; 3D Gaussian "
    "Splatting for Real-Time Radiance Field Rendering (free)",
    "https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/",
    "<b>The &sect;3 method</b>, with the differentiable rasteriser "
    "described in enough detail to implement."),
   ("M&uuml;ller, Evans, Schied & Keller &mdash; Instant Neural Graphics "
    "Primitives (free)",
    "https://nvlabs.github.io/instant-ngp/",
    "<b>The &sect;2 representation change</b> — hash grids, and the "
    "seconds-not-days result."),
   ("Tewari et al. &mdash; Advances in Neural Rendering (free survey)",
    "https://arxiv.org/abs/2111.05849",
    "The landscape, including the &sect;4 limitations stated honestly by "
    "people working in it."),
 ],
 "exercises": [
   "<b>Implement a differentiable renderer</b> for a simple primitive and "
   "optimise its parameters to match a target image.",
   "<b>Demonstrate the visibility discontinuity:</b> move an occluder and "
   "plot the loss. Show it is not smooth.",
   "Implement a minimal NeRF on a small synthetic scene.",
   "<b>Remove the positional encoding</b> and show the result is blurry.",
   "<b>Sweep the number of encoding frequencies</b> and plot detail "
   "against frequency count.",
   "Verify that the volume rendering integral matches CSCE 647's "
   "formulation.",
   "<b>Implement or run Gaussian splatting</b> on your own photographs.",
   "<b>Measure frames per second and training time</b> for NeRF and "
   "splatting on the same scene.",
   "Count the primitives and the memory a splat scene requires.",
   "<b>Try to relight a captured scene</b> and document what fails.",
 ],
 "selfcheck": [
   "What does a differentiable renderer enable, and what is the central "
   "difficulty?",
   "What does a NeRF store, and what integral does it render with?",
   "Why is positional encoding essential?",
   "What did NeRF trade, and what did Instant-NGP change?",
   "Compare NeRF and Gaussian splatting on six axes.",
   "Why did splatting achieve its speedup, and what lesson does that "
   "repeat?",
   "Name five learned components in a modern renderer and say which "
   "mattered most.",
   "Give four things neural rendering does not yet do well.",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "What Networks Fail At",
 "subtitle": "The failure modes that do not show up in the test set.",
 "question": "What is the model actually doing?",
 "outcomes": [
     "Explain adversarial examples and what they reveal.",
     "Explain shortcut learning and how to detect it.",
     "Explain out-of-distribution failure and overconfidence.",
     "State the limits of attribution methods.",
     "Design evaluation that exposes these failures.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Adversarial examples",
   "blurb": "Imperceptible changes, confident errors."},

  {"t": "callout", "title": "A perturbation too small to see changes the answer completely",
   "kind": "The finding",
   "body": ["<b>Add a carefully chosen perturbation of magnitude "
            "invisible to a person, and a classifier's output changes to "
            "any target you choose</b>, with high confidence.",
            "<b>The perturbation is found by gradient ascent on the "
            "loss</b> — the same machinery that trained the model, "
            "pointed at its input instead of its weights.",
            "<b>And they transfer.</b> An example crafted against one "
            "model frequently fools a different model with a different "
            "architecture trained on different data.",
            "<b>Transfer is the important part.</b> <b>It means these are "
            "not quirks of one model but properties of the data and the "
            "learning procedure</b>, and it makes black-box attacks "
            "practical."]},

  {"t": "callout", "title": "They may be features, not bugs",
   "kind": "The interpretation that reframed it",
   "body": ["<b>The intuitive reading: the model is broken and should be "
            "fixed.</b>",
            "<b>An alternative with real evidence: the model is using "
            "<i>genuinely predictive</i> features that happen to be "
            "imperceptible to humans.</b>",
            "<b>The experiment:</b> build a dataset containing only "
            "adversarial perturbations with their target labels, train a "
            "fresh model on it, and <b>it generalises to the real test "
            "set</b>.",
            "<b>So the perturbations carry real signal.</b> <b>The "
            "mismatch is between which predictive features a human uses "
            "and which a network uses</b> — which is a much more "
            "uncomfortable finding than a bug."]},

  {"t": "section", "label": "Part 2", "title": "Shortcut learning",
   "blurb": "Solving the dataset instead of the task."},

  {"t": "table", "kicker": "Shortcuts", "title": "Documented cases",
   "header": ["Intended task", "What was learned", "Detection"],
   "widths": [3.0, 4.2, 4.9],
   "rows": [
     ["<b>Detect pneumonia</b>", "<b>Which hospital took the scan</b>", "<b>Test on a new hospital</b>"],
     ["<b>Classify animals</b>", "<b>Texture, not shape</b>", "<b>Texture–shape conflict images</b>"],
     ["Detect skin cancer", "<b>Whether a ruler is in frame</b>", "Remove the ruler"],
     ["<b>Answer questions</b>", "Dataset answer priors", "<b>Balanced counterfactual sets</b>"],
     ["<b>Detect tanks</b>", "<b>The weather that day</b>", "<b>The apocryphal original; still instructive</b>"],
   ],
   "footnote": "<b>Every one passed its own test set.</b> The shortcut was "
               "present in training and test alike, because both came from "
               "the same collection.",
   "note": "That the test set shares the shortcut is the whole problem."},

  {"t": "callout", "title": "The test set shares the shortcut",
   "kind": "Why this is invisible",
   "body": ["<b>Train and test are usually drawn from the same "
            "collection</b>, so any spurious correlation present in one is "
            "present in the other.",
            "<b>So the model scores well and has learned the wrong "
            "thing</b>, and no amount of held-out evaluation reveals it.",
            "<b>Detection requires a <i>distribution shift</i> you "
            "construct deliberately:</b> a different site, a different "
            "time, a counterfactual edit, a stress test.",
            "<b>This is CSCE 633 Module 12's leakage argument "
            "generalised</b> — <b>and the response is the same: be "
            "suspicious of good results and audit what the model is "
            "using.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Out of distribution",
   "blurb": "Confidently wrong on the unfamiliar."},

  {"t": "callout", "title": "Networks do not know what they do not know",
   "kind": "The deployment hazard",
   "body": ["<b>Presented with an input unlike anything in training, a "
            "classifier still produces a confident distribution</b> "
            "(CSCE 633 M10 §3) — the softmax must sum to one.",
            "<b>So a model trained on ten animal classes will confidently "
            "classify a photograph of a chair.</b> There is no 'none of "
            "these' output.",
            "<b>Detection methods exist</b> — ensemble disagreement, "
            "energy scores, Mahalanobis distance in feature space, "
            "conformal prediction — <b>and none is reliable across "
            "shifts.</b>",
            "<b>So the practical defence is to monitor the inputs</b> "
            "(CSCE 633 M13 §1) <b>and to design an abstain path</b>, "
            "rather than to trust the model's own confidence."]},

  {"t": "section", "label": "Part 4", "title": "Interpretability",
   "blurb": "What attribution does and does not tell you."},

  {"t": "callout", "title": "Saliency maps are not explanations",
   "kind": "The limitation that matters",
   "body": ["<b>Saliency highlights which input regions the output is "
            "sensitive to.</b> It does not say <i>why</i>, or what feature "
            "was used, or whether the reasoning was sound.",
            "<b>And several popular methods fail basic sanity checks:</b> "
            "randomising the model's weights leaves some saliency maps "
            "essentially unchanged — <b>they were reflecting the input, "
            "not the model.</b>",
            "<b>A plausible-looking heatmap is persuasive and weak "
            "evidence</b>, which is a dangerous combination.",
            "<b>Mechanistic interpretability</b> — identifying actual "
            "circuits and features inside the network — <b>is more "
            "promising and far more laborious</b>, and it does not yet "
            "scale to explaining a single production decision."]},

  {"t": "bullets", "kicker": "Design", "title": "Evaluation that exposes these failures",
   "items": [
     "<b>Test on a deliberately different distribution</b> — another "
     "site, another time, another device.",
     "",
     "<b>Construct counterfactuals</b> — change only the thing that "
     "should matter, and only the thing that should not.",
     "",
     "<b>Stress test:</b> corruptions, occlusions, rotations, "
     "compression artefacts.",
     "",
     "<b>Probe with adversarial examples</b>, even if robustness is not "
     "a goal — it tells you how brittle the decision boundary is.",
     "",
     "<b>And report by slice with counts</b> (CSCE 633 M12 §3), "
     "because the failures concentrate.",
   ],
   "footnote": "<b>None of this appears in a standard held-out "
               "evaluation</b>, which is exactly why it must be designed "
               "in deliberately."},
 ],
 "takeaways": [
   "An imperceptible perturbation found by gradient ascent changes a "
   "classifier's output to any target, and such examples transfer between "
   "models.",
   "Transfer means these are properties of the data and the learning "
   "procedure rather than quirks of one model.",
   "Adversarial perturbations carry genuinely predictive signal — a "
   "model trained only on them generalises to the real test set.",
   "Shortcut learning passes its own test set, because train and test share "
   "the spurious correlation.",
   "Networks have no 'none of these' output, so they are confidently wrong "
   "off-distribution and their confidence cannot be trusted.",
   "Several saliency methods fail the sanity check of randomising the "
   "model's weights — they reflected the input, not the model.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Adversarial examples"),
  ("callout", "A perturbation too small to see changes the answer completely",
   ["<b>Add a carefully chosen perturbation whose magnitude is below human "
    "perceptual threshold, and a classifier's output changes to any target "
    "class you nominate</b>, typically with very high confidence. The two "
    "images are visually identical.",
    "<b>The perturbation is found by gradient ascent on the loss with "
    "respect to the <i>input</i></b> — the same backpropagation "
    "machinery that trained the model (Module 02), pointed at the pixels "
    "rather than the weights. <b>The capability is a direct consequence of "
    "the model being differentiable.</b>",
    "<b>And they transfer.</b> An example crafted against one model "
    "frequently fools a different model, with a different architecture, "
    "trained on different data, by a different team.",
    "<b>Transfer is the important part.</b> <b>It means adversarial "
    "examples are not idiosyncratic quirks of a particular trained model "
    "but properties of the data and the learning procedure</b> — and "
    "practically, it makes black-box attacks feasible without any access "
    "to the target model at all."]),
  ("callout", "They may be features, not bugs",
   ["<b>The intuitive reading is that the model is broken</b> and that "
    "sufficient engineering would make it robust.",
    "<b>An alternative with real experimental support: the model is using "
    "genuinely predictive features that happen to be imperceptible to "
    "humans.</b> The features are real; they are just not the ones we "
    "would use.",
    "<b>The experiment is striking.</b> Construct a dataset consisting "
    "<i>only</i> of adversarially perturbed images labelled with their "
    "<i>target</i> classes — to a human, a set of mislabelled images. "
    "Train a fresh model on it. <b>It generalises to the real, unmodified "
    "test set.</b> The perturbations alone carried enough signal to learn "
    "the task.",
    "<b>So the perturbations are not noise; they are predictive "
    "features.</b> <b>The mismatch is between which predictive features a "
    "human uses and which a network uses</b> — both are real "
    "regularities in the data, and only one of them is robust to the "
    "distribution shifts humans care about. <b>That is a considerably more "
    "uncomfortable finding than a bug</b>, because it means robustness is "
    "a constraint we must impose rather than a property we are failing to "
    "achieve."]),

  ("h1", "2 &nbsp; Shortcut learning"),
  ("table", ["Intended task", "What was actually learned", "How to detect it"],
   [["<b>Detect pneumonia from chest radiographs</b>",
     "<b>Which hospital took the scan</b> — identifiable from a "
     "metadata token burned into the corner, or from scanner "
     "characteristics — combined with differing base rates between "
     "sites.",
     "<b>Evaluate on a hospital not in the training set.</b> Performance "
     "collapses."],
    ["<b>Classify animals</b>",
     "<b>Texture rather than shape.</b> ImageNet-trained CNNs are "
     "substantially texture-biased, contrary to the assumption that they "
     "learn shape.",
     "<b>Texture–shape conflict images</b> — a cat silhouette "
     "with elephant skin — which the model labels elephant."],
    ["<b>Detect skin cancer</b>",
     "<b>Whether a ruler appears in the frame</b>, because dermatologists "
     "photograph lesions they already suspect alongside a scale.",
     "Remove or add the ruler and observe the prediction change."],
    ["<b>Answer questions about images</b>",
     "Dataset answer priors — answering 'two' to 'how many' and "
     "'tennis' to 'what sport' without consulting the image.",
     "<b>Balanced counterfactual sets</b> where each question has multiple "
     "answers across images."],
    ["<b>Detect tanks in photographs</b>",
     "<b>The weather on the day each set was photographed.</b>",
     "<b>The apocryphal original story</b> — probably never happened "
     "as told, and it is still the clearest statement of the failure "
     "mode."]],
   [0.22, 0.42, 0.36]),
  ("callout", "The test set shares the shortcut",
   ["<b>Training and test splits are almost always drawn from the same "
    "collection</b>, by a random split of the same corpus. <b>So any "
    "spurious correlation present in the training data is present in the "
    "test data too.</b>",
    "<b>The model therefore scores well on its test set and has learned "
    "the wrong thing</b>, and <b>no amount of held-out evaluation reveals "
    "it</b> — the held-out set is testing the same shortcut.",
    "<b>Detection requires a distribution shift that you construct "
    "deliberately:</b> a different collection site, a different time "
    "period, a different device, a counterfactual edit that changes only "
    "the spurious feature, or a stress test.",
    "<b>This is CSCE 633 Module 12's leakage argument generalised</b> "
    "— there, a feature carried the label; here, a feature carries the "
    "label indirectly through the collection process. <b>And the response "
    "is identical: be suspicious of good results, and audit what the model "
    "is actually using rather than only what it scores.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Out-of-distribution failure"),
  ("callout", "Networks do not know what they do not know",
   ["<b>Presented with an input unlike anything in its training "
    "distribution, a classifier still produces a confident probability "
    "distribution over its known classes</b> (CSCE 633 Module 10 "
    "&sect;3) — because the softmax is constrained to sum to one and "
    "has no way to express 'none of these'.",
    "<b>So a model trained on ten animal species will confidently classify "
    "a photograph of a chair, a page of text, or pure noise</b> as one of "
    "its ten species. <b>The confidence is not merely misleading; it is "
    "frequently higher than on genuine in-distribution examples.</b>",
    "<b>Detection methods exist</b> — ensemble disagreement "
    "(Module 09), energy-based scores, Mahalanobis distance in feature "
    "space, conformal prediction (CSCE 633 Module 10 &sect;4) — "
    "<b>and none is reliable across the range of shifts encountered in "
    "practice</b>, which is an honest summary of a large literature.",
    "<b>So the practical defence is to monitor the <i>inputs</i></b> "
    "(CSCE 633 Module 13 &sect;1) <b>and to design an abstention path "
    "into the system</b> — a route by which a prediction can be "
    "deferred to a human or to a safer default — <b>rather than to "
    "trust the model's own confidence</b>, which is the one signal that "
    "demonstrably cannot be relied upon here."]),

  ("h1", "4 &nbsp; Interpretability"),
  ("callout", "Saliency maps are not explanations",
   ["<b>A saliency map highlights which input regions the output is "
    "sensitive to.</b> It does not say <i>why</i>, does not identify what "
    "feature was extracted, and does not indicate whether the reasoning was "
    "sound — it is a sensitivity analysis presented as a "
    "justification.",
    "<b>And several widely used methods fail basic sanity checks.</b> "
    "<b>Randomising the model's weights leaves some popular saliency maps "
    "essentially unchanged</b> — which means those maps were "
    "reflecting properties of the <i>input image</i> (edges, salient "
    "regions) rather than anything about the model at all. The check is "
    "simple and the result was widely replicated.",
    "<b>A plausible-looking heatmap is persuasive and weak evidence</b>, "
    "which is a dangerous combination — it is exactly the kind of "
    "artifact that satisfies a reviewer or a regulator without "
    "establishing anything.",
    "<b>Mechanistic interpretability</b> — identifying actual circuits "
    "and features within the network, and verifying them by intervention "
    "— <b>is considerably more promising and far more laborious</b>. "
    "<b>It does not yet scale to explaining a single production "
    "decision</b>, which is the thing that is usually wanted, so the "
    "honest position is that explaining a network's individual output "
    "remains unsolved."]),
  ("ul", ["<b>Test on a deliberately different distribution</b> — "
          "another collection site, another time period, another device, "
          "another demographic. <b>This single practice catches more "
          "shortcut learning than everything else combined.</b>",
          "<b>Construct counterfactuals:</b> change only the feature that "
          "should matter and verify the prediction changes; change only a "
          "feature that should not and verify it does not.",
          "<b>Stress test with corruptions</b> — blur, noise, "
          "compression artefacts, rotations, occlusions, weather effects. "
          "Standardised benchmarks exist (ImageNet-C and relatives) and "
          "they correlate with real deployment robustness.",
          "<b>Probe with adversarial examples even when robustness is not "
          "a stated goal</b> — the size of perturbation required tells "
          "you how brittle the decision boundary is, which is informative "
          "about the model regardless of whether an attacker exists.",
          "<b>And report by slice with counts</b> (CSCE 633 Module 12 "
          "&sect;3), <b>because these failures concentrate</b> rather than "
          "spreading evenly — an aggregate number hides exactly the "
          "subpopulation where the shortcut does not hold. <b>None of this "
          "appears in a standard held-out evaluation, which is precisely "
          "why it has to be designed in deliberately.</b>"]),
 ],
 "resources": [
   ("Ilyas et al. &mdash; Adversarial Examples Are Not Bugs, They Are "
    "Features (free)",
    "https://arxiv.org/abs/1905.02175",
    "<b>The &sect;1 reframing</b>, with the dataset experiment. One of the "
    "more genuinely surprising results in the field."),
   ("Geirhos et al. &mdash; Shortcut Learning in Deep Neural Networks "
    "(free)",
    "https://arxiv.org/abs/2004.07780",
    "<b>The &sect;2 survey</b> — the documented cases, the mechanism, "
    "and what to do about it."),
   ("Adebayo et al. &mdash; Sanity Checks for Saliency Maps (free)",
    "https://arxiv.org/abs/1810.03292",
    "<b>The &sect;4 result.</b> The weight-randomisation test, and which "
    "methods fail it."),
   ("Hendrycks & Dietterich &mdash; Benchmarking Neural Network Robustness "
    "to Common Corruptions (free)",
    "https://arxiv.org/abs/1903.12261",
    "The &sect;4 stress-test benchmark, and evidence that it predicts "
    "deployment behaviour."),
 ],
 "exercises": [
   "<b>Generate adversarial examples</b> against your model with FGSM and "
   "with PGD. Measure the perturbation size needed.",
   "<b>Test transfer:</b> apply examples crafted against one model to a "
   "different architecture.",
   "Plot accuracy against perturbation budget.",
   "<b>Construct a deliberate shortcut</b> — add a small marker "
   "correlated with the label — and show the model uses it and still "
   "passes its test set.",
   "<b>Then detect it</b> by evaluating on data without the marker.",
   "Test a pretrained classifier on texture–shape conflict images and "
   "report the bias.",
   "<b>Feed out-of-distribution inputs</b> and plot the confidence "
   "distribution against in-distribution inputs.",
   "Implement an OOD detector and measure its reliability across two "
   "different kinds of shift.",
   "<b>Run the saliency sanity check:</b> randomise the model weights and "
   "compare the saliency maps.",
   "<b>Design and run a stress test suite</b> for your project model and "
   "report by slice.",
 ],
 "selfcheck": [
   "How are adversarial examples found, and why does transfer matter?",
   "What does the 'features not bugs' experiment show?",
   "Give five shortcut learning cases and the detection for each.",
   "Why does a held-out test set not reveal a shortcut?",
   "Why are networks confidently wrong off-distribution?",
   "Name four OOD detection methods and say how reliable they are.",
   "What do saliency maps show, and what sanity check do several fail?",
   "Give five evaluation practices that expose these failures.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Shipping a Model",
 "subtitle": "Inference cost, and what you can honestly claim.",
 "question": "What does it take to run this in production?",
 "outcomes": [
     "Reason about the inference cost budget.",
     "Apply quantisation and measure the quality cost.",
     "Apply distillation and pruning.",
     "Explain serving considerations — batching, caching, "
     "latency.",
     "State what a trained model can honestly promise.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The cost",
   "blurb": "Training is once; inference is forever."},

  {"t": "callout", "title": "Inference dominates the lifetime cost",
   "kind": "The framing",
   "body": ["<b>Training happens once, or periodically. Inference happens "
            "on every request, forever.</b>",
            "<b>So a model that costs twice as much to train and half as "
            "much to serve is usually the better choice</b>, and the "
            "research literature optimises the wrong one of these.",
            "<b>And inference is frequently memory-bandwidth-bound, not "
            "compute-bound</b> — at batch size 1, every weight is read "
            "once per token and arithmetic intensity is terrible "
            "(CSCE 735 M07).",
            "<b>Which is why quantisation helps so much:</b> halving the "
            "bits halves the bytes moved, and <b>the speedup comes from "
            "bandwidth rather than arithmetic.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Making it smaller",
   "blurb": "Three techniques, with different trades."},

  {"t": "table", "kicker": "Compression", "title": "Quantisation, distillation, pruning",
   "header": ["Technique", "What it does", "Typical result"],
   "widths": [2.7, 4.3, 5.1],
   "rows": [
     ["<b>Post-training quantisation</b>", "<b>Cast weights to int8 or fp8 after training</b>", "<b>4× smaller, small quality loss, no retraining</b>"],
     ["<b>Quantisation-aware training</b>", "Simulate quantisation during training", "<b>Better quality at low bits; needs retraining</b>"],
     ["<b>Distillation</b>", "<b>Train a small model on a large one’s outputs</b>", "<b>Small model beats training it directly</b>"],
     ["<b>Structured pruning</b>", "Remove whole channels or heads", "<b>Real speedup; hardware-friendly</b>"],
     ["Unstructured pruning", "<b>Zero individual weights</b>", "<b>High sparsity, little real speedup</b>"],
   ],
   "footnote": "<b>Unstructured sparsity rarely translates into wall-clock "
               "gains</b> without hardware support — a sparse matrix "
               "multiply is slower per nonzero than a dense one.",
   "note": "That distinction between theoretical and achieved speedup "
           "matters."},

  {"t": "callout", "title": "Distillation transfers more than the labels",
   "kind": "Why it works better than it should",
   "body": ["<b>Train a small model to match a large one's output "
            "<i>distribution</i></b>, not just its top prediction.",
            "<b>The soft targets carry information the hard label does "
            "not</b> — that this image is 70% cat, 25% lynx, 5% dog tells "
            "the student about class similarity structure.",
            "<b>So the student frequently outperforms the same "
            "architecture trained directly on the hard labels</b>, with "
            "the same data.",
            "<b>'Dark knowledge' was the original name</b>, and the "
            "effect is robust — <b>which also means a distilled model "
            "inherits the teacher's biases and shortcuts</b> "
            "(Module 12)."]},

  {"t": "section", "label": "Part 3", "title": "Serving",
   "blurb": "The systems question."},

  {"t": "bullets", "kicker": "Serving", "title": "What determines throughput and latency",
   "items": [
     "<b>Batching</b> — the single largest lever. It converts a "
     "memory-bound problem into a compute-bound one, <b>and it adds "
     "latency</b>.",
     "",
     "<b>Continuous batching</b> for generation — admit new requests "
     "as others finish rather than waiting for a whole batch.",
     "",
     "<b>KV caching</b> — reuse attention keys and values across "
     "generated tokens. <b>Essential, and it is the memory "
     "bottleneck.</b>",
     "",
     "<b>Compilation</b> — kernel fusion and graph optimisation "
     "(CSCE 605 M13's shader argument, applied).",
     "",
     "<b>And measure p99, not the mean</b> (CSCE 678 M13).",
   ],
   "footnote": "<b>Batching trades latency for throughput</b>, which is "
               "the same trade CSCE 678 made about buffers and "
               "CSCE 650 about frame pacing."},

  {"t": "section", "label": "Part 4", "title": "Claiming honestly",
   "blurb": "The course, closed."},

  {"t": "bullets", "kicker": "Claims", "title": "What a trained model can honestly promise",
   "items": [
     "<b>'Top-1 82.3% on this benchmark, against a from-scratch "
     "baseline of 71.1%, with the split and date stated.'</b>",
     "",
     "<b>'Worst slice 64%, n = 290.'</b> And the slice named.",
     "",
     "<b>'Degrades to 61% under the standard corruption benchmark; "
     "fails on inputs outside the training distribution without "
     "signalling it.'</b>",
     "",
     "<b>'int8 quantised: 3.8&times; smaller, 2.1&times; faster, 0.6 "
     "points of accuracy.'</b>",
     "",
     "<b>And what you cannot say: 'human-level', 'understands', or "
     "'robust'.</b>",
   ],
   "footnote": "<b>Every course in this program ends here</b> — state "
               "what you measured, and what you did not."},

  {"t": "callout", "title": "Where this leaves you",
   "kind": "Closing",
   "body": ["You can build a network from autodifferentiation upward, "
            "diagnose why it will not train, choose an architecture from "
            "what the data looks like, and scale it when it does not fit.",
            "<b>And you know what these models fail at</b> — "
            "adversarially, through shortcuts, and off-distribution — "
            "which the benchmark number does not tell you.",
            "<b>CSCE 633 supplied the evaluation discipline; CSCE 669 "
            "supplies the optimisation theory</b>; and <b>Modules 10 and "
            "11 closed the loop back to CSCE 647 and 748.</b>",
            "<b>The discipline is the same as everywhere else in this "
            "program:</b> <b>baseline first, measure what you claim, "
            "report by slice, and never say more than you "
            "established.</b>"]},
 ],
 "takeaways": [
   "Training happens once and inference happens forever, so lifetime cost "
   "is dominated by serving — and the literature optimises the other "
   "one.",
   "Inference at small batch is memory-bandwidth-bound, which is why "
   "quantisation's speedup comes from moving fewer bytes rather than from "
   "arithmetic.",
   "Unstructured sparsity rarely produces wall-clock gains without hardware "
   "support; structured pruning does.",
   "Distillation transfers the output distribution, which carries class "
   "similarity information the hard label does not — and the teacher's "
   "biases with it.",
   "Batching is the largest serving lever and it trades latency for "
   "throughput.",
   "State the benchmark, the baseline, the split, the worst slice, and the "
   "degradation — and do not say 'human-level' or 'robust'.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The inference cost budget"),
  ("callout", "Inference dominates the lifetime cost",
   ["<b>Training happens once, or periodically on a retraining schedule. "
    "Inference happens on every single request, forever.</b> For any "
    "model with real traffic the integral over inference exceeds the "
    "training cost within weeks.",
    "<b>So a model that costs twice as much to train and half as much to "
    "serve is usually the better choice</b> — and <b>the research "
    "literature optimises the wrong one of these</b>, reporting training "
    "compute and benchmark accuracy while inference cost appears, if at "
    "all, as a footnote.",
    "<b>And inference is frequently memory-bandwidth-bound rather than "
    "compute-bound.</b> At batch size one, every weight is read from memory "
    "and used in exactly one multiply-accumulate — <b>arithmetic "
    "intensity is close to its worst possible value</b>, and the "
    "accelerator's arithmetic units are mostly idle (CSCE 735 Module 07's "
    "roofline, at the far left).",
    "<b>Which explains why quantisation helps as much as it does:</b> "
    "halving the bits per weight halves the bytes that must be moved, and "
    "<b>the speedup comes from bandwidth rather than from faster "
    "arithmetic</b> — which is why int8 inference can be close to "
    "4&times; faster even on hardware whose int8 arithmetic throughput is "
    "not 4&times; its fp32 throughput."]),

  ("h1", "2 &nbsp; Making it smaller"),
  ("table", ["Technique", "What it does", "Typical result"],
   [["<b>Post-training quantisation</b>",
     "<b>Cast the trained weights to int8 or fp8, with per-channel scale "
     "factors calibrated on a small sample.</b>",
     "<b>About 4&times; smaller, a small accuracy loss, and no retraining "
     "at all.</b> The first thing to try."],
    ["<b>Quantisation-aware training</b>",
     "Simulate the quantisation during training so the model adapts to it.",
     "<b>Noticeably better quality at low bit-widths</b>, at the cost of a "
     "retraining run."],
    ["<b>Distillation</b>",
     "<b>Train a small student model to match a large teacher's output "
     "distribution.</b>",
     "<b>The student frequently beats the same architecture trained "
     "directly on the labels</b> — see below."],
    ["<b>Structured pruning</b>",
     "Remove entire channels, attention heads (Module 07 &sect;2), or "
     "layers.",
     "<b>A real wall-clock speedup, because the resulting dense model is "
     "simply smaller</b> and the hardware is unchanged."],
    ["<b>Unstructured pruning</b>",
     "<b>Zero out individual weights wherever they are small.</b>",
     "<b>Very high sparsity is achievable and rarely translates into "
     "wall-clock gains</b> — a sparse matrix multiply costs more per "
     "nonzero than a dense one, so 90% sparsity can be slower than dense "
     "without specific hardware support. <b>A theoretical speedup is not "
     "an achieved one.</b>"]],
   [0.20, 0.38, 0.42]),
  ("callout", "Distillation transfers more than the labels",
   ["<b>Train a small model to match a large model's full output "
    "<i>distribution</i></b> — typically with a softened softmax "
    "— <b>rather than only its top prediction.</b>",
    "<b>The soft targets carry information the hard label does not.</b> "
    "That an image is rated 70% cat, 25% lynx, and 5% dog tells the student "
    "something about the similarity structure of the classes: that cats and "
    "lynxes are confusable in a way cats and dogs are not. A one-hot label "
    "contains none of that.",
    "<b>So the student frequently outperforms the identical architecture "
    "trained directly on the hard labels with the same data</b> — "
    "which is counterintuitive, since the teacher's outputs are strictly "
    "less accurate than the ground truth.",
    "<b>Hinton called it 'dark knowledge'</b> and the effect is robust "
    "across domains. <b>It also means a distilled model inherits the "
    "teacher's biases and shortcuts</b> (Module 12 &sect;2) — the "
    "student is learning to imitate the teacher, including where the "
    "teacher is wrong, and <b>evaluating the student only against the "
    "teacher will never reveal this.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Serving"),
  ("ul", ["<b>Batching is the single largest lever.</b> It amortises each "
          "weight read across many inputs, <b>converting a memory-bound "
          "problem into a compute-bound one</b> (&sect;1) — and it "
          "<b>adds latency</b>, because requests wait for the batch to "
          "fill. <b>The same latency-for-throughput trade as CSCE 678 "
          "Module 02's buffers and CSCE 650's frame pacing.</b>",
          "<b>Continuous (in-flight) batching for generation.</b> Admit new "
          "requests into the batch as earlier ones finish, rather than "
          "waiting for every sequence in a batch to complete — a large "
          "throughput gain for variable-length generation.",
          "<b>KV caching.</b> Reuse the attention keys and values computed "
          "for previous tokens rather than recomputing them each step. "
          "<b>Essential — without it generation is quadratic — "
          "and the cache becomes the memory bottleneck</b>, growing with "
          "batch size times sequence length, which is what PagedAttention "
          "and similar schemes manage.",
          "<b>Compilation.</b> Kernel fusion, graph-level optimisation, and "
          "target-specific code generation — <b>which is CSCE 605's "
          "subject applied here</b>, and the same argument as that course's "
          "Module 13 made about shader compilation, including the "
          "warm-up cost.",
          "<b>And measure the p99 rather than the mean</b> (CSCE 678 "
          "Module 13 &sect;2) — a serving system's tail is what users "
          "experience, and batching makes the tail worse in exchange for "
          "the throughput."]),

  ("h1", "4 &nbsp; Claiming honestly"),
  ("ul", ["<b>'Top-1 accuracy 82.3% on this benchmark, against a "
          "from-scratch baseline of 71.1%, split by subject, data "
          "collected in 2024.'</b> <b>The baseline, the split key, and the "
          "date are what make it a claim</b> (CSCE 633 Module 01 "
          "&sect;4).",
          "<b>'Worst-performing slice: 64%, n = 290, on the "
          "under-represented device type.'</b> <b>The slice named and "
          "counted</b> (CSCE 633 Module 12 &sect;3).",
          "<b>'Degrades to 61% under the standard corruption benchmark, "
          "and fails on inputs outside the training distribution without "
          "signalling that it has done so.'</b> <b>Stating the known "
          "failure mode is more useful than another point of "
          "accuracy</b> (Module 12).",
          "<b>'int8 quantised: 3.8&times; smaller, 2.1&times; faster at "
          "batch size 1, costing 0.6 points of top-1.'</b> The compression "
          "trade, measured in all three dimensions.",
          "<b>And what you cannot honestly say: 'human-level', "
          "'understands', or 'robust'.</b> <b>'Human-level' requires "
          "stating which humans, on which task, under which conditions, "
          "and with what inter-annotator agreement</b> (CSCE 633 "
          "Module 11 &sect;4) — usually it means 'exceeds the "
          "accuracy of the annotators who produced the labels', which is a "
          "statement about the labels. <b>Every course in this program ends "
          "on this point, and the repetition is the argument.</b>"]),
  ("callout", "Where this leaves you",
   ["<b>You can build a network from automatic differentiation upward, "
    "diagnose why it will not train, choose an architecture from what the "
    "data's structure actually is, scale it when it does not fit on one "
    "device, and compress it when it must be served.</b>",
    "<b>And you know what these models fail at</b> — adversarially, "
    "through shortcuts learned from the collection process, and "
    "confidently off-distribution — <b>none of which the benchmark "
    "number tells you</b>, and all of which decide whether a deployment "
    "works.",
    "<b>CSCE 633 supplied the evaluation discipline this course "
    "inherited</b> — baselines, slices, leakage, honest claims. "
    "<b>CSCE 669 supplies the optimisation theory underneath "
    "Module 03</b>, which is where the semester finishes. <b>And "
    "Modules 10 and 11 closed the loop back to CSCE 647's denoising and "
    "CSCE 748's reconstruction</b>, which is why this course sits in a "
    "graphics program at all.",
    "<b>The discipline does not change.</b> <b>Baseline first, measure "
    "what you claim, report by slice, and never say more than you "
    "established.</b> <b>That has now been the closing paragraph of eight "
    "consecutive courses</b>, and it is the part of this degree that will "
    "still be true when every architecture in it is obsolete."]),
 ],
 "resources": [
   ("Hinton, Vinyals & Dean &mdash; Distilling the Knowledge in a Neural "
    "Network (free)",
    "https://arxiv.org/abs/1503.02531",
    "<b>The &sect;2 'dark knowledge' argument</b>, from the paper that "
    "named it."),
   ("Jacob et al. &mdash; Quantization and Training of Neural Networks for "
    "Efficient Integer-Arithmetic-Only Inference (free)",
    "https://arxiv.org/abs/1712.05877",
    "The &sect;2 quantisation scheme, including quantisation-aware "
    "training."),
   ("Kwon et al. &mdash; Efficient Memory Management for Large Language "
    "Model Serving (PagedAttention / vLLM) (free)",
    "https://arxiv.org/abs/2309.06180",
    "<b>The &sect;3 KV cache problem</b>, and a solution borrowed directly "
    "from virtual memory (CSCE 611)."),
   ("Blalock et al. &mdash; What is the State of Neural Network Pruning? "
    "(free)",
    "https://arxiv.org/abs/2003.03033",
    "<b>The &sect;2 caution</b> — a survey finding that pruning "
    "results are frequently not comparable and that reported speedups are "
    "often theoretical."),
 ],
 "exercises": [
   "<b>Measure your model's inference latency and memory</b> at batch sizes "
   "1, 8, and 64.",
   "<b>Place inference on a roofline</b> and confirm it is memory-bound at "
   "batch 1.",
   "Apply post-training int8 quantisation and measure size, speed, and "
   "accuracy.",
   "<b>Apply quantisation-aware training</b> and compare at 8 and 4 bits.",
   "<b>Distil your model into one a quarter the size</b> and compare "
   "against training that architecture directly.",
   "<b>Check whether the student inherited a shortcut</b> from the teacher "
   "(Module 12).",
   "Apply structured and unstructured pruning at equal sparsity and "
   "<b>measure the actual wall-clock speedup of each</b>.",
   "Implement KV caching and measure the memory growth with sequence "
   "length.",
   "<b>Measure p50 and p99 latency under load</b>, with and without "
   "batching.",
   "<b>Project 2 is now due.</b> Submit the model, the training curves "
   "including failures, the baseline comparison, the cost measurements, "
   "the failure probe, and the honest claim.",
 ],
 "selfcheck": [
   "Why does inference dominate lifetime cost, and what does the "
   "literature optimise?",
   "Why is small-batch inference memory-bound, and what follows for "
   "quantisation?",
   "Compare five compression techniques and their real results.",
   "Why does unstructured sparsity rarely give a wall-clock speedup?",
   "Why does distillation beat direct training, and what does the student "
   "inherit?",
   "Name five serving considerations and the trade batching makes.",
   "Give four honest claims and three things you cannot say.",
 ],
},

]
