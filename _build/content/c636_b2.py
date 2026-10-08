# -*- coding: utf-8 -*-
"""CSCE 636 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Backpropagation",
 "subtitle": "The chain rule, organised so it runs once.",
 "question": "How do you get gradients for millions of parameters?",
 "outcomes": [
     "Derive backpropagation as reverse-mode automatic "
     "differentiation.",
     "Explain why reverse mode and not forward mode.",
     "Implement an autodifferentiation engine.",
     "Verify gradients numerically.",
     "Diagnose vanishing and exploding gradients.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Reverse mode",
   "blurb": "Why the gradient costs about one forward pass."},

  {"t": "callout", "title": "Forward mode and reverse mode differ by which end you start",
   "kind": "The choice that decides the cost",
   "body": ["<b>Both compute exact derivatives by the chain rule.</b> "
            "Neither is numerical differentiation and neither is symbolic.",
            "<b>Forward mode propagates derivatives with respect to one "
            "<i>input</i> forward.</b> Cost: one pass per input. Good when "
            "there are few inputs and many outputs.",
            "<b>Reverse mode propagates derivatives of one <i>output</i> "
            "backward.</b> Cost: one pass per output.",
            "<b>A loss is one scalar output and a network has millions of "
            "parameters</b> — so reverse mode gives every gradient in a "
            "single backward pass. <b>That asymmetry is the whole reason "
            "training is affordable.</b>"]},

  {"t": "code", "kicker": "Autodiff", "title": "A complete engine, in principle",
   "lang": "python", "code": """
class Value:
    def __init__(self, data, parents=(), op=""):
        self.data, self.grad = data, 0.0
        self._parents, self._backward = parents, lambda: None

    def __mul__(self, other):
        out = Value(self.data * other.data, (self, other), "*")
        def _backward():
            # chain rule: accumulate, do not assign -- a value used
            # twice receives gradient from BOTH paths
            self.grad  += other.data * out.grad
            other.grad += self.data  * out.grad
        out._backward = _backward
        return out

def backward(root):
    topo, seen = [], set()
    def build(v):                      # topological order, so every
        if v in seen: return           # consumer is processed before
        seen.add(v)                    # its producer
        for p in v._parents: build(p)
        topo.append(v)
    build(root)
    root.grad = 1.0
    for v in reversed(topo):
        v._backward()
""",
   "caption": "<b>Two ideas: accumulate gradients, and process in reverse "
              "topological order.</b> Everything else is more operators.",
   "note": "The += rather than = is the bug people write first."},

  {"t": "callout", "title": "A computational graph, not a network",
   "kind": "The right abstraction",
   "body": ["<b>The engine knows nothing about layers, neurons, or "
            "networks.</b> It knows operations and their local "
            "derivatives.",
            "<b>So anything differentiable can be trained</b> — a "
            "renderer, a physics simulator (CSCE 649), a sorting "
            "relaxation, a protein folding model.",
            "<b>That generality is why the framework is a "
            "<i>differentiation</i> library with neural network utilities "
            "attached</b>, rather than a neural network library.",
            "<b>And it is why 'differentiable X' became a research "
            "programme</b> — once the gradient is free, the question is "
            "only whether X can be written differentiably."]},

  {"t": "section", "label": "Part 2", "title": "Checking it",
   "blurb": "The test that catches everything."},

  {"t": "code", "kicker": "Gradient check", "title": "Numerical verification",
   "lang": "python", "code": """
def grad_check(f, x, eps=1e-5):
    analytic = backward_gradient_of(f, x)
    for i in range(len(x)):
        xp, xm = x.copy(), x.copy()
        xp[i] += eps; xm[i] -= eps
        numeric = (f(xp) - f(xm)) / (2 * eps)    # CENTRAL difference,
                                                 # error O(eps^2)
        rel = abs(numeric - analytic[i]) / max(1e-8,
                  abs(numeric) + abs(analytic[i]))
        assert rel < 1e-5, f"component {i}: {numeric} vs {analytic[i]}"

# USE DOUBLE PRECISION. In float32 the subtraction cancels and the
# check fails on correct code -- a false alarm that wastes hours.
# Use RELATIVE error, not absolute: gradients span many orders.
# Check a SMALL random subset; checking all of them is too slow.
# And avoid points where the function is not differentiable:
# ReLU at exactly zero will fail the check legitimately.
""",
   "caption": "<b>Four caveats, each of which produces a false failure</b> "
              "— and a false failure on correct code costs more than "
              "no check at all.",
   "note": "The float32 cancellation issue is the one that wastes the most "
           "time."},

  {"t": "section", "label": "Part 3", "title": "Vanishing and exploding",
   "blurb": "Why deep stacks did not train."},

  {"t": "eq", "kicker": "The mechanism", "title": "Gradients multiply through depth",
   "eqs": [
     ("∂L/∂w₁ = ∂L/∂aₙ · ∂aₙ/∂aₙ₋₁ ⋯ ∂a₂/∂a₁ · ∂a₁/∂w₁",
      "The gradient at an early layer is a product of n Jacobians."),
     ("Each factor < 1 ⟹ the product → 0 exponentially",
      "Vanishing. Early layers receive no signal and do not learn."),
     ("Each factor > 1 ⟹ the product → ∞ exponentially",
      "Exploding. The update overshoots and the loss becomes NaN."),
   ],
   "caption": "<b>Sigmoid's derivative peaks at 0.25</b>, so ten sigmoid "
              "layers attenuate the gradient by about a million — "
              "which is why depth did not work.",
   "note": "The 0.25^10 figure makes it concrete."},

  {"t": "table", "kicker": "Fixes", "title": "What each fix addresses",
   "header": ["Fix", "Addresses", "How"],
   "widths": [2.8, 3.2, 6.1],
   "rows": [
     ["<b>ReLU</b>", "<b>Vanishing</b>", "<b>Derivative is exactly 1 when active — no attenuation</b>"],
     ["<b>He / Xavier init</b>", "<b>Both</b>", "<b>Scales weights so variance is preserved per layer</b>"],
     ["<b>Residual connections</b>", "<b>Vanishing</b>", "<b>An identity path gives gradient a route with factor 1</b>"],
     ["<b>Normalisation</b>", "Both", "Rescales activations each layer (M04)"],
     ["<b>Gradient clipping</b>", "<b>Exploding</b>", "<b>Caps the norm. Essential for RNNs</b>"],
     ["Careful gating", "Vanishing", "LSTM's cell path, same idea as residuals"],
   ],
   "footnote": "<b>Residual connections are the single most important "
               "architectural idea here</b> — they are why networks "
               "went from 20 layers to 1,000.",
   "note": "ResNet's contribution is best framed as a gradient-path fix."},

  {"t": "section", "label": "Part 4", "title": "Diagnosing it",
   "blurb": "What to look at."},

  {"t": "bullets", "kicker": "Diagnosis", "title": "Reading gradient pathology",
   "items": [
     "<b>Log the gradient norm per layer, every few steps.</b> A "
     "histogram across layers is the single best diagnostic here.",
     "",
     "<b>Vanishing looks like:</b> early layers' norms orders of "
     "magnitude below later ones; the loss plateaus above chance.",
     "",
     "<b>Exploding looks like:</b> a sudden spike then NaN, or a loss "
     "that oscillates wildly.",
     "",
     "<b>Dead ReLUs:</b> a unit whose output is zero for every input in "
     "the batch. Check the fraction; above ~40% is a problem.",
     "",
     "<b>And NaN propagates instantly</b> — find the first step it "
     "appears and look at the batch, not the architecture.",
   ],
   "footnote": "<b>Per-layer gradient norms cost almost nothing to log</b> "
               "and resolve most training mysteries in this course."},
 ],
 "takeaways": [
   "Reverse-mode autodifferentiation gives every parameter's gradient in "
   "one backward pass because the loss is a single scalar output.",
   "An autodiff engine is two ideas: accumulate gradients rather than "
   "assign, and process in reverse topological order.",
   "The engine knows nothing about networks, which is why anything "
   "differentiable — a renderer, a simulator — can be trained.",
   "Gradient checking needs double precision, relative error, a random "
   "subset, and avoidance of non-differentiable points.",
   "Gradients multiply through depth, so factors below one vanish "
   "exponentially and factors above one explode.",
   "Residual connections give the gradient an identity path, which is why "
   "networks went from twenty layers to a thousand.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Reverse-mode automatic differentiation"),
  ("callout", "Forward and reverse mode differ by which end you start from",
   ["<b>Both compute exact derivatives by systematic application of the "
    "chain rule.</b> Neither is finite differencing (which is approximate "
    "and unstable) nor symbolic differentiation (which produces "
    "expressions that explode in size). <b>Automatic differentiation is a "
    "third thing</b> and the distinction is worth being clear about.",
    "<b>Forward mode propagates the derivative with respect to one input "
    "forward through the graph.</b> One pass gives you the derivative of "
    "<i>every</i> output with respect to <i>that one</i> input, so the "
    "cost is one pass per input.",
    "<b>Reverse mode propagates the derivative of one output backward.</b> "
    "One backward pass gives the derivative of <i>that one</i> output with "
    "respect to <i>every</i> input, so the cost is one pass per output.",
    "<b>A loss is a single scalar output, and a network has millions of "
    "parameters.</b> So reverse mode delivers all the gradients in one "
    "backward pass costing roughly the same as the forward pass. <b>That "
    "asymmetry is the entire reason training large models is "
    "affordable</b> — with forward mode, each parameter would need "
    "its own pass, and training would be a million times more "
    "expensive."]),
  ("code", """class Value:
    def __init__(self, data, parents=(), op=""):
        self.data, self.grad = data, 0.0
        self._parents, self._backward = parents, lambda: None

    def __mul__(self, other):
        out = Value(self.data * other.data, (self, other), "*")
        def _backward():
            # ACCUMULATE, do not assign: a value used twice receives
            # gradient contributions from BOTH consumers.
            self.grad  += other.data * out.grad
            other.grad += self.data  * out.grad
        out._backward = _backward
        return out

def backward(root):
    topo, seen = [], set()
    def build(v):
        if v in seen: return
        seen.add(v)
        for p in v._parents: build(p)
        topo.append(v)
    build(root)
    root.grad = 1.0
    for v in reversed(topo):     # every consumer before its producer
        v._backward()"""),
  ("p", "<b>Two ideas carry the whole implementation: accumulate rather "
        "than assign, and process in reverse topological order.</b> The "
        "<code>+=</code> is the bug everyone writes as <code>=</code> the "
        "first time — and it only shows up when a value feeds more "
        "than one consumer, which in a simple test it may not. "
        "<b>Everything else is adding more operators.</b>"),
  ("callout", "It is a computational graph, not a network",
   ["<b>The engine above knows nothing about layers, neurons, activations, "
    "or networks.</b> It knows operations and their local derivatives, and "
    "how to compose them.",
    "<b>So anything differentiable can be trained by it</b> — a "
    "renderer (CSCE 647), a physics simulator (CSCE 649), a relaxed "
    "sorting operation, a protein structure predictor, an optimiser's own "
    "hyperparameters.",
    "<b>Which is why the major frameworks are differentiation libraries "
    "with neural network utilities attached</b>, rather than neural network "
    "libraries — a distinction visible in their API design, and one "
    "that becomes important the moment you want to differentiate through "
    "something that is not a standard layer.",
    "<b>And it is why 'differentiable X' became a research programme.</b> "
    "Differentiable rendering, differentiable physics, differentiable "
    "sorting, differentiable programming — <b>once the gradient is "
    "free, the only question is whether X can be written "
    "differentiably</b>, which turns the design problem into finding smooth "
    "relaxations of discrete operations. Module 11 is an instance of "
    "exactly this."]),

  ("h1", "2 &nbsp; Verifying it"),
  ("code", """def grad_check(f, x, eps=1e-5):
    analytic = backward_gradient_of(f, x)
    for i in random_subset(range(len(x))):
        xp, xm = x.copy(), x.copy()
        xp[i] += eps;  xm[i] -= eps
        numeric = (f(xp) - f(xm)) / (2*eps)      # CENTRAL difference
        rel = abs(numeric - analytic[i]) / max(1e-8,
                  abs(numeric) + abs(analytic[i]))
        assert rel < 1e-5

CAVEATS, each of which causes a FALSE failure:
  * use DOUBLE precision -- in float32 the subtraction cancels
  * use RELATIVE error -- gradients span many orders of magnitude
  * check a small RANDOM SUBSET -- checking all is too slow
  * avoid non-differentiable points -- ReLU at exactly 0 will
    legitimately fail"""),
  ("p", "<b>A false failure on correct code is worse than no check at "
        "all</b>, because it sends you looking for a bug that is not there. "
        "<b>The float32 cancellation is the one that wastes the most "
        "time:</b> the central difference subtracts two nearly equal "
        "numbers, which is exactly CSCE 620 Module 01's catastrophic "
        "cancellation, and in single precision the result can have no "
        "correct digits. <b>Run gradient checks in double.</b>"),

  ("break",),
  ("h1", "3 &nbsp; Vanishing and exploding gradients"),
  ("eq", "&part;L/&part;w<sub>1</sub> = &part;L/&part;a<sub>n</sub> "
         "&middot; &part;a<sub>n</sub>/&part;a<sub>n&minus;1</sub> "
         "&middot; &hellip; &middot; &part;a<sub>1</sub>/&part;w<sub>1</sub>"),
  ("p", "<b>The gradient reaching an early layer is a product of n "
        "Jacobians.</b> If each factor has magnitude consistently below "
        "one, the product decays exponentially in depth — "
        "<b>vanishing</b> — and the early layers receive essentially "
        "no learning signal. If each factor exceeds one, the product grows "
        "exponentially — <b>exploding</b> — and a single update "
        "overshoots catastrophically, usually producing NaN. <b>The "
        "sigmoid's derivative peaks at 0.25</b>, so ten sigmoid layers "
        "attenuate the gradient by a factor of roughly a million even in "
        "the best case. <b>That arithmetic is why depth did not work for "
        "twenty-five years</b>, and it is not subtle once stated."),
  ("table", ["Fix", "Addresses", "How"],
   [["<b>ReLU</b>", "<b>Vanishing.</b>",
     "<b>Its derivative is exactly 1 wherever the unit is active</b>, so "
     "the product does not attenuate through active paths. A one-line "
     "change with an enormous effect (Module 01 &sect;3)."],
    ["<b>He / Xavier initialisation</b>", "<b>Both.</b>",
     "<b>Scales the initial weights so that activation variance is "
     "preserved from layer to layer</b> — derived from the fan-in and "
     "fan-out, not tuned. Before this, deep networks frequently could not "
     "be trained at all."],
    ["<b>Residual connections</b>", "<b>Vanishing.</b>",
     "<b>An identity shortcut gives the gradient a path with factor "
     "exactly 1</b>, so it reaches early layers regardless of what the "
     "intervening blocks do. See below."],
    ["<b>Normalisation layers</b>", "Both.",
     "Rescale activations at each layer so neither the forward signal nor "
     "the backward gradient drifts in magnitude (Module 04)."],
    ["<b>Gradient clipping</b>", "<b>Exploding.</b>",
     "<b>Caps the gradient norm before the update.</b> Crude, effective, "
     "and essentially mandatory for recurrent networks (Module 06)."],
    ["<b>Gating (LSTM, GRU)</b>", "Vanishing.",
     "The cell state provides an additive path through time — <b>the "
     "same mechanism as a residual connection</b>, discovered earlier and "
     "in a different setting."]],
   [0.19, 0.20, 0.61]),
  ("p", "<b>Residual connections are the single most important "
        "architectural idea in this module.</b> By making each block "
        "compute x + f(x) rather than f(x), the gradient flows backward "
        "through the identity term unattenuated — <b>and that is why "
        "networks went from about twenty trainable layers to over a "
        "thousand</b>. It is also why the same pattern appears in "
        "transformers (Module 07), in U-Nets, and in diffusion models: "
        "<b>the trick is not about images, it is about gradient paths.</b>"),

  ("h1", "4 &nbsp; Diagnosing it"),
  ("ul", ["<b>Log the gradient norm per layer, every few hundred "
          "steps.</b> <b>A histogram of gradient magnitude across layers "
          "is the single best diagnostic available for this class of "
          "problem</b>, and it costs almost nothing.",
          "<b>Vanishing looks like:</b> early layers' gradient norms "
          "orders of magnitude smaller than later ones, and a loss that "
          "plateaus above chance while the last layer alone continues to "
          "improve.",
          "<b>Exploding looks like:</b> a sudden spike in the loss "
          "followed by NaN, or a loss that oscillates violently without "
          "settling. <b>The spike is usually one bad batch</b>, and "
          "clipping absorbs it.",
          "<b>Dead ReLUs:</b> units whose output is zero for every input "
          "in the batch, which receive no gradient and never recover. "
          "<b>Log the fraction of dead units per layer</b>; above roughly "
          "40% indicates the learning rate was too high at some point and "
          "the layer is now partly destroyed.",
          "<b>And NaN propagates instantly through everything.</b> <b>Find "
          "the <i>first</i> step at which it appears and inspect the input "
          "batch</b>, rather than the architecture — the cause is "
          "usually a specific input (a zero divisor, a log of zero, an "
          "extreme outlier) rather than a structural problem."]),
 ],
 "resources": [
   ("Karpathy &mdash; micrograd, and 'The spelled-out intro to neural "
    "networks and backpropagation' (free)",
    "https://github.com/karpathy/micrograd",
    "<b>The &sect;1 engine, built live on video in two hours.</b> The "
    "single best resource for this module."),
   ("Baydin, Pearlmutter, Radul & Siskind &mdash; Automatic "
    "Differentiation in Machine Learning: a Survey (free)",
    "https://jmlr.org/papers/v18/17-468.html",
    "<b>Forward versus reverse mode done properly</b>, and the "
    "distinction from symbolic and numerical differentiation."),
   ("He, Zhang, Ren & Sun &mdash; Deep Residual Learning (free)",
    "https://arxiv.org/abs/1512.03385",
    "<b>The &sect;3 fix.</b> Read the figure showing that a deeper plain "
    "network was <i>worse</i> on training error — which is what "
    "motivated it."),
   ("CS231n &mdash; backpropagation and gradient checking notes (free)",
    "https://cs231n.github.io/optimization-2/",
    "The &sect;2 caveats, each explained with the failure it causes."),
 ],
 "exercises": [
   "<b>Implement a scalar autodifferentiation engine</b> with add, "
   "multiply, power, and tanh.",
   "<b>Write <code>=</code> instead of <code>+=</code></b> in the backward "
   "pass and construct a graph where it gives the wrong answer.",
   "Extend the engine to tensors and train a two-layer network with it.",
   "<b>Implement gradient checking</b> and verify your engine.",
   "<b>Run the check in float32</b> and observe the false failures.",
   "Check the gradient of ReLU at exactly zero and explain the result.",
   "<b>Train a 15-layer network with sigmoid activations</b> and log "
   "per-layer gradient norms. Plot them.",
   "Switch to ReLU and plot again. Then add residual connections and plot "
   "a third time.",
   "<b>Make a network explode</b> with a high learning rate, then fix it "
   "with clipping.",
   "<b>Measure the dead ReLU fraction</b> per layer and relate it to the "
   "learning rate used.",
 ],
 "selfcheck": [
   "Distinguish forward and reverse mode, and say why reverse wins here.",
   "What two ideas does an autodiff engine need?",
   "Why must gradients be accumulated rather than assigned?",
   "Why can anything differentiable be trained?",
   "Give four caveats for gradient checking and the failure each causes.",
   "Explain vanishing and exploding gradients from the chain rule.",
   "Give six fixes and what each addresses.",
   "Why are residual connections so important?",
   "Name four gradient pathologies and how each looks in the logs.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Optimisation in Practice",
 "subtitle": "Making a non-convex surface cooperate.",
 "question": "Why does gradient descent work on a surface with no "
             "guarantees?",
 "outcomes": [
     "Compare SGD, momentum, and Adam and say when each wins.",
     "Choose a learning rate and a schedule with evidence.",
     "Explain why initialisation matters and how it is derived.",
     "Apply the standard debugging sequence to a failing run.",
     "Explain what is and is not understood about why this works.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The learning rate",
   "blurb": "The one hyperparameter that matters most."},

  {"t": "callout", "title": "Nothing else matters as much",
   "kind": "The practical hierarchy",
   "body": ["<b>Too high and the loss diverges or oscillates.</b> Too low "
            "and it converges so slowly you conclude the model cannot "
            "learn.",
            "<b>The gap between 'too high' and 'too low' is often less "
            "than an order of magnitude</b>, and the right value changes "
            "with batch size, architecture, and initialisation.",
            "<b>So find it by range test:</b> start very low, raise it "
            "exponentially each step, plot loss against learning rate, and "
            "take roughly an order of magnitude below the minimum.",
            "<b>Ten minutes of range test beats a day of guessing</b>, "
            "and it is the first thing to do with any new architecture or "
            "dataset."]},

  {"t": "code", "kicker": "Schedules", "title": "Why the rate should change during training",
   "lang": "text", "code": """
  WARMUP -- start small, ramp up over the first few hundred steps
      Early gradients are large and the parameters are random, so a
      full-size step at step 1 can destroy the initialisation.
      Essential for transformers and for large batches.

  THEN DECAY -- the main schedule
      step       drop by 10x at fixed epochs. Simple, dated.
      cosine     smooth decay to ~0 over the run. The default now.
      linear     to zero. Common for fine-tuning.
      one-cycle  up then down, with high peak. Fast convergence.

  WHY DECAY AT ALL
      A large rate explores -- the noise in SGD lets it escape poor
      regions. A small rate exploits -- it settles into whatever
      basin it is in. You want both, in that order.

      Decaying too early traps you in the first decent basin.
      Not decaying at all leaves you bouncing around the minimum
      and the final loss plateaus well above where it could be.

  RESTARTS -- jump the rate back up periodically. Sometimes finds
      a better basin; also gives you several usable checkpoints.
""",
   "caption": "<b>Explore then exploit</b> — and a decaying learning "
              "rate is how that is implemented.",
   "note": "The explore/exploit framing makes schedules make sense rather "
           "than being folklore."},

  {"t": "section", "label": "Part 2", "title": "Optimisers",
   "blurb": "What each adds, and what it costs."},

  {"t": "table", "kicker": "Optimisers", "title": "The ones worth knowing",
   "header": ["Optimiser", "Adds", "Character"],
   "widths": [2.6, 4.3, 5.2],
   "rows": [
     ["<b>SGD</b>", "<b>Nothing. The gradient, scaled</b>", "<b>Noisy, and the noise helps generalisation</b>"],
     ["<b>+ momentum</b>", "<b>A velocity term</b>", "<b>Damps oscillation; accelerates along consistent directions</b>"],
     ["<b>Adam</b>", "<b>Per-parameter adaptive step sizes</b>", "<b>Robust default; needs less tuning</b>"],
     ["<b>AdamW</b>", "<b>Decoupled weight decay</b>", "<b>Fixes a real bug in Adam. Use this one</b>"],
     ["RMSProp", "Adaptive scale only", "Adam's predecessor; still used in RL"],
     ["<b>LAMB / LARS</b>", "Layer-wise rate scaling", "<b>Very large batch training</b>"],
   ],
   "footnote": "<b>AdamW is the default for a reason</b> — Adam's "
               "original weight decay was implemented as an L2 penalty on "
               "the gradient, which the adaptive scaling then distorted.",
   "note": "The AdamW fix is a good example of a subtle bug in a very "
           "widely used method."},

  {"t": "callout", "title": "SGD sometimes generalises better than Adam",
   "kind": "The result that complicates the default",
   "body": ["<b>Adam converges faster and frequently reaches a worse "
            "test loss</b> than well-tuned SGD with momentum, "
            "particularly in vision.",
            "<b>The usual explanation is the noise.</b> SGD's gradient "
            "noise biases it toward flat minima, which appear to "
            "generalise better; Adam's adaptivity suppresses that noise.",
            "<b>The explanation is contested and the empirical pattern is "
            "reasonably robust.</b>",
            "<b>So: Adam or AdamW to get something working quickly; try "
            "tuned SGD with momentum if the last point of accuracy "
            "matters.</b> <b>And measure, because it does not hold "
            "everywhere</b> — transformers generally prefer Adam."]},

  {"t": "section", "label": "Part 3", "title": "Initialisation",
   "blurb": "Where the network starts decides whether it trains."},

  {"t": "eq", "kicker": "Scaling", "title": "Preserve the variance per layer",
   "eqs": [
     ("Var(output) = n_in · Var(w) · Var(input)",
      "For a linear layer with n_in inputs, assuming independence."),
     ("Xavier:  Var(w) = 2 / (n_in + n_out)",
      "Preserves variance in both directions. For tanh and sigmoid."),
     ("He:  Var(w) = 2 / n_in",
      "The factor of 2 compensates for ReLU zeroing half the "
      "activations."),
   ],
   "caption": "<b>These are derived, not tuned.</b> Getting the scale "
              "wrong by a factor of two per layer compounds "
              "exponentially with depth.",
   "note": "The He factor-of-2 derivation is a nice concrete payoff."},

  {"t": "callout", "title": "Zero initialisation does not work, and neither does large",
   "kind": "The two failures",
   "body": ["<b>All zeros: every unit in a layer computes the same thing "
            "and receives the same gradient</b>, so they remain identical "
            "forever. The layer has one effective unit. <b>Symmetry must "
            "be broken.</b>",
            "<b>Too large: activations saturate</b> (for bounded "
            "activations) <b>or explode</b> (for unbounded ones), and the "
            "gradients follow.",
            "<b>Biases are usually fine at zero</b>, since the weights "
            "already break symmetry.",
            "<b>And modern practice initialises residual branches near "
            "zero</b>, so that the network starts close to the identity "
            "and depth costs nothing at step one."]},

  {"t": "section", "label": "Part 4", "title": "Debugging a run",
   "blurb": "The sequence that finds it."},

  {"t": "bullets", "kicker": "Procedure", "title": "In this order, always",
   "items": [
     "<b>1. Overfit one batch.</b> Take 8 examples and drive the loss to "
     "near zero. <b>If you cannot, nothing else matters</b> — there is a "
     "bug, not a tuning problem.",
     "",
     "<b>2. Check the loss at initialisation.</b> For k balanced "
     "classes it should be about ln(k). If it is not, the output layer or "
     "the loss is wrong.",
     "",
     "<b>3. Run the learning rate range test</b> (Part 1).",
     "",
     "<b>4. Look at the data</b> — actually look at it, after "
     "augmentation, as the model sees it.",
     "",
     "<b>5. Then tune.</b> Everything before this is bug-finding; only "
     "now is it optimisation.",
   ],
   "footnote": "<b>Step 1 catches the overwhelming majority of "
               "problems</b> and takes under a minute. It is the single "
               "most valuable habit in this course."},

  {"t": "callout", "title": "Why this works at all is not fully understood",
   "kind": "The honest position",
   "body": ["<b>The loss surface is non-convex with enormous numbers of "
            "critical points</b>, and gradient descent has no guarantee "
            "of finding anything good.",
            "<b>It works anyway, reliably.</b> Current understanding: "
            "most critical points in high dimensions are saddles rather "
            "than bad minima, and the many minima that exist are mostly of "
            "similar quality.",
            "<b>And the optimiser appears to implicitly regularise</b> "
            "— of the many parameter settings that fit the training "
            "data, gradient descent finds low-complexity ones "
            "(CSCE 633 M03 §4).",
            "<b>This is an active research area, not settled "
            "knowledge.</b> <b>Be suspicious of confident mechanistic "
            "explanations</b>, including the two in this callout."]},
 ],
 "takeaways": [
   "The learning rate matters more than anything else, and a ten-minute "
   "range test beats a day of guessing.",
   "Decay implements explore-then-exploit: a large rate escapes poor "
   "regions and a small one settles into a basin.",
   "AdamW fixes a real bug in Adam's weight decay and is the sensible "
   "default; tuned SGD with momentum sometimes generalises better.",
   "Initialisation scales are derived to preserve variance per layer, and "
   "He's factor of two compensates for ReLU zeroing half the activations.",
   "Zero initialisation leaves every unit in a layer identical forever, so "
   "symmetry must be broken.",
   "Overfit one batch before anything else — if you cannot, there is a "
   "bug rather than a tuning problem.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The learning rate"),
  ("callout", "Nothing else matters as much",
   ["<b>Too high and the loss diverges, oscillates, or produces NaN. Too "
    "low and it converges so slowly that you conclude the architecture "
    "cannot learn the task.</b> Both failures look like model problems and "
    "neither is.",
    "<b>The window between the two is frequently less than an order of "
    "magnitude</b>, and the right value shifts with batch size, "
    "architecture, initialisation, and normalisation — so a value "
    "carried over from another project is a guess.",
    "<b>Find it by range test.</b> Start at a very small rate, multiply it "
    "by a constant factor each step, and plot the loss against the rate on "
    "a log axis. The loss falls, reaches a minimum, and then diverges; "
    "<b>take roughly an order of magnitude below the point of minimum "
    "loss</b> (or just past the steepest descent).",
    "<b>Ten minutes of range test beats a day of guessing</b>, and it "
    "should be the first thing done with any new architecture or dataset. "
    "It is also the cheapest possible intervention: one short run."]),
  ("code", """WARMUP -- start small, ramp up over the first few hundred steps
  early gradients are large and the parameters are random, so a
  full-size step at step 1 can destroy the initialisation.
  Essential for transformers and for large batches.

THEN DECAY
  step       drop 10x at fixed epochs. Simple, dated.
  cosine     smooth decay toward 0. The current default.
  linear     to zero. Common for fine-tuning.
  one-cycle  up then down with a high peak. Fast.

WHY DECAY AT ALL
  a LARGE rate EXPLORES -- SGD's noise escapes poor regions
  a SMALL rate EXPLOITS -- it settles into the current basin
  you want both, in that order.

  decaying too early   -> trapped in the first decent basin
  never decaying       -> bouncing around the minimum forever,
                          final loss plateaus well above its floor"""),

  ("h1", "2 &nbsp; Optimisers"),
  ("table", ["Optimiser", "What it adds", "Character"],
   [["<b>SGD</b>", "<b>Nothing — the mini-batch gradient, scaled by "
     "the learning rate.</b>",
     "<b>Noisy, and the noise appears to help generalisation</b> "
     "(see below). Needs the most tuning."],
    ["<b>SGD with momentum</b>",
     "<b>A velocity term accumulating past gradients.</b>",
     "<b>Damps oscillation across narrow valleys and accelerates along "
     "consistently-signed directions</b> — the same thin-valley "
     "problem as CSCE 633 Module 02 &sect;2, addressed differently."],
    ["<b>Adam</b>",
     "<b>Per-parameter adaptive step sizes</b>, from running estimates of "
     "the gradient's first and second moments.",
     "<b>Robust, converges fast, and needs far less learning-rate "
     "tuning</b> — which is why it became the default."],
    ["<b>AdamW</b>", "<b>Decoupled weight decay.</b>",
     "<b>Fixes a genuine bug in Adam</b>: the original implemented weight "
     "decay as an L2 term added to the gradient, which the adaptive "
     "per-parameter scaling then distorted, so the effective decay differed "
     "per parameter. <b>Use AdamW.</b>"],
    ["<b>RMSProp</b>", "Adaptive scaling without the momentum term.",
     "Adam's predecessor; still common in reinforcement learning."],
    ["<b>LAMB, LARS</b>", "Layer-wise learning rate scaling.",
     "<b>For very large batch training</b> (Module 08), where a single "
     "global rate suits no layer well."]],
   [0.18, 0.37, 0.45]),
  ("callout", "SGD sometimes generalises better than Adam",
   ["<b>Adam converges faster in training loss and frequently reaches a "
    "<i>worse</i> test loss</b> than carefully tuned SGD with momentum "
    "— the effect is most consistently reported in computer vision.",
    "<b>The usual explanation appeals to the noise.</b> SGD's gradient "
    "noise is larger and less structured, which biases it toward wide flat "
    "minima; flat minima are argued to generalise better because small "
    "parameter perturbations change the loss little. <b>Adam's adaptivity "
    "suppresses exactly that noise.</b>",
    "<b>The explanation is contested</b> — the flatness measure is "
    "not reparameterisation-invariant, which is a real objection — "
    "<b>while the empirical pattern is reasonably robust.</b> It is worth "
    "holding the fact and the explanation separately.",
    "<b>So in practice: use AdamW to get something working quickly, and "
    "try tuned SGD with momentum if the last point of accuracy "
    "matters.</b> <b>And measure, because it does not hold "
    "everywhere</b> — transformers generally prefer Adam, and the "
    "reasons for that are also not fully settled."]),

  ("break",),
  ("h1", "3 &nbsp; Initialisation"),
  ("eq", "Var(out) = n<sub>in</sub> &middot; Var(w) &middot; Var(in) "
         "&nbsp;&rArr;&nbsp; Xavier: Var(w) = 2/(n<sub>in</sub>+"
         "n<sub>out</sub>) &nbsp;&nbsp; He: Var(w) = 2/n<sub>in</sub>"),
  ("p", "For a linear layer with n inputs, assuming independence, the "
        "output variance is the input variance times the fan-in times the "
        "weight variance. <b>Setting the weight variance to preserve "
        "activation variance across layers keeps the signal from growing or "
        "shrinking exponentially with depth</b> — which is Module 02 "
        "&sect;3's problem addressed at initialisation. <b>Xavier</b> "
        "balances the forward and backward directions, for symmetric "
        "activations. <b>He's extra factor of two compensates for ReLU "
        "zeroing half the activations</b>, which halves the variance — "
        "a derivation that takes two lines and makes the constant "
        "meaningful rather than magical. <b>These are derived, not "
        "tuned</b>, and getting the scale wrong by a factor of two per "
        "layer compounds exponentially."),
  ("callout", "Zero initialisation does not work, and neither does large",
   ["<b>All zeros is the symmetry failure:</b> every unit in a layer "
    "computes the identical function and therefore receives the identical "
    "gradient, so they update identically and remain identical forever. "
    "<b>The layer has exactly one effective unit regardless of its "
    "width</b>, and no amount of training fixes it. <b>Symmetry must be "
    "broken by randomness.</b>",
    "<b>Too large is the saturation failure:</b> activations are pushed "
    "into the flat regions of bounded functions (where the gradient is "
    "nearly zero) or grow without bound for unbounded ones — and the "
    "gradients follow in either case.",
    "<b>Biases are usually fine initialised at zero</b>, because the "
    "weights already break the symmetry. <b>The one common exception is "
    "initialising the final layer's bias to the base rate</b>, which saves "
    "the network from spending its first epochs learning the class "
    "prior — a small and genuinely useful trick on imbalanced "
    "problems.",
    "<b>And modern practice initialises the residual branch near zero</b> "
    "so that each block starts as approximately the identity. <b>The "
    "network then begins as a shallow one and deepens as training "
    "proceeds</b>, which means adding depth costs nothing at step one "
    "— an elegant resolution of the tension between depth and "
    "trainability."]),

  ("h1", "4 &nbsp; Debugging a failing run"),
  ("ol", ["<b>Overfit one batch.</b> Take eight examples and train until "
          "the loss is near zero. <b>If you cannot, there is a bug and "
          "nothing else matters</b> — a shape error, a detached "
          "gradient, a wrong loss, labels misaligned with inputs. "
          "<b>This takes under a minute and catches the overwhelming "
          "majority of problems</b>, and it is the single most valuable "
          "habit in this course.",
          "<b>Check the loss at initialisation.</b> For k balanced classes "
          "under cross-entropy it should be about ln(k) — 2.30 for "
          "ten classes. <b>If it is not, the output layer, the loss, or "
          "the label encoding is wrong</b>, and that is a thirty-second "
          "check for a bug that otherwise takes hours.",
          "<b>Run the learning rate range test</b> (&sect;1).",
          "<b>Look at the data.</b> Actually look at it — render the "
          "images after augmentation, print the tokenised text, listen to "
          "the audio, <b>as the model receives it</b>. Augmentation bugs "
          "and preprocessing bugs are invisible in the loss and obvious on "
          "screen.",
          "<b>Then tune.</b> <b>Everything before this step is "
          "bug-finding; only now is it optimisation</b>, and conflating the "
          "two is why people tune hyperparameters for a week against a "
          "shape error."]),
  ("callout", "Why this works at all is not fully understood",
   ["<b>The loss surface is non-convex, extremely high-dimensional, and "
    "has an enormous number of critical points.</b> Gradient descent has no "
    "theoretical guarantee of finding anything good, and Module 02 of "
    "CSCE 633 noted that convexity was what made the classical methods "
    "safe.",
    "<b>It works anyway, reliably, across architectures and datasets.</b> "
    "The current partial understanding: in very high dimensions most "
    "critical points are saddles rather than poor local minima (a bad "
    "minimum requires the Hessian to be positive in <i>every</i> direction, "
    "which becomes improbable), and the many minima that do exist appear to "
    "be of broadly similar quality.",
    "<b>And the optimiser appears to regularise implicitly</b> — among "
    "the many parameter settings that fit the training data exactly, "
    "gradient descent reliably finds low-complexity ones, which is the "
    "mechanism behind double descent (CSCE 633 Module 03 &sect;4).",
    "<b>This is an active research area rather than settled knowledge.</b> "
    "<b>Be suspicious of confident mechanistic explanations — "
    "including the two in this callout</b>, which are the current "
    "consensus and have both been challenged. <b>The honest position is "
    "that the practice is far ahead of the theory</b>, which is unusual in "
    "this program and worth noticing rather than papering over."]),
 ],
 "resources": [
   ("Smith &mdash; Cyclical Learning Rates and the LR range test (free)",
    "https://arxiv.org/abs/1506.01186",
    "<b>The &sect;1 range test</b>, from the paper that introduced it. "
    "Short and immediately applicable."),
   ("Loshchilov & Hutter &mdash; Decoupled Weight Decay Regularization "
    "(free)",
    "https://arxiv.org/abs/1711.05101",
    "<b>The AdamW fix of &sect;2</b>, with the explanation of what Adam's "
    "weight decay was actually doing."),
   ("He et al. &mdash; Delving Deep into Rectifiers (free)",
    "https://arxiv.org/abs/1502.01852",
    "<b>The &sect;3 initialisation derivation</b>, including the factor of "
    "two."),
   ("Karpathy &mdash; A Recipe for Training Neural Networks (free)",
    "https://karpathy.github.io/2019/04/25/recipe/",
    "<b>The &sect;4 procedure, in full.</b> The most practically useful "
    "single page in this course."),
 ],
 "exercises": [
   "<b>Run a learning rate range test</b> on your project and plot the "
   "curve. Choose a rate from it.",
   "Train with rates 10&times; above and below that choice, and plot all "
   "three curves.",
   "<b>Compare constant, step, and cosine schedules</b> at equal total "
   "steps.",
   "<b>Add warmup</b> to a transformer-style model and show what happens "
   "without it.",
   "Compare SGD, SGD+momentum, Adam, and AdamW on the same problem. "
   "<b>Report training and test loss for each.</b>",
   "<b>Derive He initialisation</b> for ReLU by hand.",
   "Initialise a network to all zeros and demonstrate that a layer has one "
   "effective unit.",
   "<b>Initialise residual branches near zero</b> and compare early "
   "training against standard initialisation.",
   "<b>Overfit a single batch of eight examples</b> on your project, and "
   "record how long it took to get working.",
   "Check your loss at initialisation against ln(k) and fix it if it "
   "disagrees.",
 ],
 "selfcheck": [
   "Why does the learning rate matter most, and how should it be found?",
   "Explain explore-then-exploit and why schedules decay.",
   "Compare six optimisers on what each adds.",
   "What bug does AdamW fix?",
   "Why might SGD generalise better than Adam, and how confident should "
   "you be?",
   "Derive the He initialisation factor.",
   "Why does zero initialisation fail?",
   "Give the five debugging steps in order and say which catches most "
   "bugs.",
   "What is and is not understood about why this works?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Regularisation and Normalisation",
 "subtitle": "Two different jobs that are routinely confused.",
 "question": "How do you stop it overfitting, and keep it trainable?",
 "outcomes": [
     "Apply dropout and explain what it actually does.",
     "Explain batch normalisation and why the original explanation "
     "was wrong.",
     "Choose between batch, layer, and group normalisation.",
     "Explain augmentation as the strongest regulariser available.",
     "Diagnose which problem you have.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two different problems",
   "blurb": "Regularisation and normalisation are not the same thing."},

  {"t": "callout", "title": "Normalisation makes it trainable; regularisation makes it generalise",
   "kind": "The distinction to hold onto",
   "body": ["<b>Normalisation addresses an <i>optimisation</i> "
            "problem:</b> activations drifting in scale through depth, "
            "which makes the loss surface badly conditioned "
            "(Module 02 §3).",
            "<b>Regularisation addresses a <i>generalisation</i> "
            "problem:</b> the gap between training and test error "
            "(CSCE 633 M03).",
            "<b>They are routinely conflated</b> because batch norm "
            "happens to do a bit of both, and because both are 'things you "
            "add to make it work'.",
            "<b>Diagnose first.</b> <b>A large train–test gap is a "
            "regularisation problem; a model that will not train at all is "
            "an optimisation problem</b>, and the remedies do not "
            "transfer."]},

  {"t": "section", "label": "Part 2", "title": "Dropout",
   "blurb": "Random deletion, and why it helps."},

  {"t": "code", "kicker": "Dropout", "title": "The mechanism, and the detail people get wrong",
   "lang": "text", "code": """
  TRAINING: zero each unit independently with probability p,
            then scale the survivors by 1/(1-p)

  INFERENCE: do nothing at all

  WHY THE SCALING ("inverted dropout")
      Without it, the expected activation at inference is 1/(1-p)
      times larger than during training, so every downstream layer
      sees a different input distribution than it was trained on.
      Scaling during training keeps the expectation matched and
      means inference needs no special case.

  WHY IT HELPS
      * no unit can rely on any specific other unit being present,
        so co-adapted detectors cannot form
      * it approximates training an ensemble of 2^n subnetworks
        that share weights, averaged at inference

  WHERE IT IS USED NOW
      Still standard in fully connected layers and in transformers.
      LARGELY ABANDONED in convolutional nets -- batch norm and
      augmentation regularise better, and dropout interacts badly
      with batch norm's statistics.
""",
   "caption": "<b>Forgetting the train/inference distinction is the "
              "classic dropout bug</b> — and it produces a model that "
              "is quietly worse rather than visibly broken.",
   "note": "The variance-shift interaction with batch norm is real and "
           "worth flagging."},

  {"t": "section", "label": "Part 3", "title": "Normalisation",
   "blurb": "What it does, and the explanation that was wrong."},

  {"t": "callout", "title": "Batch norm's original explanation was wrong, and it still works",
   "kind": "An instructive piece of history",
   "body": ["<b>The original claim: it reduces 'internal covariate "
            "shift'</b> — the change in each layer's input distribution "
            "as earlier layers update.",
            "<b>That explanation was later tested and did not hold.</b> "
            "Injecting noise <i>after</i> batch norm restores the covariate "
            "shift and the benefit remains.",
            "<b>The current account is that it smooths the loss "
            "surface</b>, making gradients more predictive and permitting "
            "much larger learning rates.",
            "<b>So a technique with an incorrect justification became "
            "universal because it demonstrably worked.</b> <b>That is "
            "worth noting about this field</b> — the empirical result led "
            "and the explanation followed, and was wrong for three "
            "years."]},

  {"t": "table", "kicker": "Variants", "title": "Which normalisation, and why",
   "header": ["Type", "Normalises over", "Use when"],
   "widths": [2.6, 4.2, 5.3],
   "rows": [
     ["<b>Batch norm</b>", "<b>The batch, per channel</b>", "<b>CNNs with batch ≥ 32. Breaks at small batch</b>"],
     ["<b>Layer norm</b>", "<b>The features, per example</b>", "<b>Transformers, RNNs. Batch-independent</b>"],
     ["<b>Group norm</b>", "Groups of channels, per example", "<b>CNNs with small batches — detection, 3D</b>"],
     ["Instance norm", "Each channel, per example", "Style transfer; removes contrast"],
     ["<b>RMSNorm</b>", "<b>Scale only, no centring</b>", "<b>Cheaper; common in large language models</b>"],
   ],
   "footnote": "<b>Batch norm's batch dependence is its real "
               "weakness</b> — train and inference behave differently, "
               "and small batches give noisy statistics.",
   "note": "The batch-dependence problem is why layer norm took over in "
           "transformers."},

  {"t": "callout", "title": "Batch norm behaves differently at inference",
   "kind": "The source of real bugs",
   "body": ["<b>During training it uses the current batch's mean and "
            "variance. At inference it uses a running average</b> "
            "accumulated during training.",
            "<b>So the function computed differs between the two "
            "modes</b> — and forgetting to switch modes is among the most "
            "common bugs in deep learning.",
            "<b>If the running statistics have not converged, inference "
            "is wrong</b> even with correct code — which happens with "
            "short training runs or unusual data ordering.",
            "<b>And it makes the model's output depend on the other "
            "examples in its batch during training</b>, which is a "
            "genuinely strange property and the reason layer norm is "
            "preferred wherever batch size varies."]},

  {"t": "section", "label": "Part 4", "title": "Augmentation",
   "blurb": "The strongest regulariser, and the most domain-specific."},

  {"t": "callout", "title": "Augmentation encodes invariances you know about",
   "kind": "Why it works so well",
   "body": ["<b>A horizontally flipped cat is still a cat.</b> So "
            "training on flips tells the model an invariance it would "
            "otherwise have to learn from data.",
            "<b>That is the same mechanism as architecture</b> "
            "(Module 01 §2) — encoded prior knowledge substituting "
            "for examples — applied through the data rather than the "
            "model.",
            "<b>And it is usually the largest single win available</b> "
            "when data is limited, ahead of any amount of dropout or "
            "weight decay.",
            "<b>But the invariance must be true.</b> <b>A vertically "
            "flipped '6' is a '9'</b>, and a mirrored chest X-ray is "
            "dextrocardia. <b>A false augmentation teaches the model "
            "something wrong.</b>"]},

  {"t": "bullets", "kicker": "Diagnosis", "title": "Which problem do you have?",
   "items": [
     "<b>Will not train at all / loss stuck at initialisation:</b> "
     "optimisation. Normalisation, initialisation, learning rate "
     "(Module 03).",
     "",
     "<b>Trains, large train–test gap:</b> generalisation. "
     "Augmentation first, then weight decay, then dropout.",
     "",
     "<b>Trains, both errors high:</b> underfitting. More capacity or "
     "better features — <b>and remove regularisation</b>.",
     "",
     "<b>Unstable across runs:</b> learning rate or initialisation, not "
     "regularisation.",
     "",
     "<b>And add one thing at a time</b>, measuring each. Stacking four "
     "regularisers at once tells you nothing.",
   ],
   "footnote": "<b>Removing regularisation is a legitimate move</b> and is "
               "rarely considered when a model underfits."},
 ],
 "takeaways": [
   "Normalisation fixes an optimisation problem and regularisation fixes a "
   "generalisation problem — diagnose which you have before choosing.",
   "Inverted dropout scales during training so inference needs no special "
   "case; forgetting the mode switch is the classic bug.",
   "Batch norm's original internal-covariate-shift explanation was tested "
   "and did not hold; it appears to smooth the loss surface instead.",
   "Batch norm depends on the batch, behaves differently at inference, and "
   "makes one example's output depend on the others — which is why "
   "layer norm took over in transformers.",
   "Augmentation encodes invariances you already know, which is the same "
   "mechanism as architecture applied through the data.",
   "The invariance must actually be true — a vertically flipped six is "
   "a nine.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two different problems"),
  ("callout", "Normalisation makes it trainable; regularisation makes it generalise",
   ["<b>Normalisation addresses an <i>optimisation</i> problem:</b> "
    "activations drifting in scale as they propagate through depth, which "
    "makes the loss surface badly conditioned and the gradients unreliable "
    "(Module 02 &sect;3). It is about whether training works at all.",
    "<b>Regularisation addresses a <i>generalisation</i> problem:</b> the "
    "gap between training and test error (CSCE 633 Module 03 &sect;1). "
    "It is about whether a model that has trained successfully is any use.",
    "<b>The two are routinely conflated</b>, partly because batch "
    "normalisation happens to provide a little of both, and partly because "
    "in practice both are 'things you add to the model to make it work' and "
    "get reached for in the same mood.",
    "<b>Diagnose before prescribing.</b> <b>A large train–test gap is "
    "a regularisation problem; a model whose loss will not move at all is "
    "an optimisation problem</b>, and the remedies do not transfer. Adding "
    "dropout to a model that cannot train makes it worse, and adding batch "
    "norm to an overfitting model mostly does nothing for the gap."]),

  ("h1", "2 &nbsp; Dropout"),
  ("code", """TRAINING   zero each unit independently with probability p,
           then scale the survivors by 1/(1-p)
INFERENCE  do nothing

WHY THE SCALING ("inverted dropout")
  without it, the expected activation at inference is 1/(1-p)
  times larger than during training, so every downstream layer
  sees a different input distribution than it was trained on.
  Scaling during TRAINING keeps the expectation matched and
  leaves inference with no special case at all.

WHY IT HELPS
  * no unit can rely on a specific other unit being present, so
    fragile co-adapted detectors cannot form
  * it approximates averaging an ensemble of 2^n weight-sharing
    subnetworks

WHERE IT IS USED NOW
  standard in fully connected layers and in transformers.
  LARGELY ABANDONED in CNNs -- batch norm and augmentation
  regularise better, and dropout interacts badly with batch
  norm's running statistics."""),
  ("p", "<b>The train/inference distinction is the classic dropout "
        "bug</b> — leaving dropout active at evaluation, or forgetting "
        "to call the framework's eval mode. <b>It produces a model that is "
        "quietly worse rather than visibly broken</b>, which is the worst "
        "kind of bug: the numbers are plausible and wrong. The "
        "batch-norm interaction is also real — dropout changes the "
        "variance of the activations between training and inference, which "
        "shifts the statistics batch norm accumulated, and the two together "
        "can underperform either alone."),

  ("h1", "3 &nbsp; Normalisation"),
  ("callout", "The original explanation was wrong, and it still works",
   ["<b>The original claim was that batch normalisation reduces 'internal "
    "covariate shift'</b> — the change in each layer's input "
    "distribution as the layers beneath it update during training. It is an "
    "intuitive story and it was accepted for several years.",
    "<b>It was later tested directly and did not hold.</b> Santurkar and "
    "colleagues injected deliberate noise <i>after</i> the batch norm "
    "layer, restoring and worsening the covariate shift — <b>and the "
    "benefit of batch norm remained</b>. The proposed mechanism was not the "
    "operative one.",
    "<b>The current account is that it smooths the loss surface</b>, "
    "reducing the Lipschitz constant of the loss and its gradient, which "
    "makes gradients more predictive over longer distances and permits "
    "much larger learning rates (Module 03 &sect;1). That account has "
    "better evidence and is not the final word either.",
    "<b>So a technique with an incorrect justification became universal "
    "because it demonstrably worked.</b> <b>That is worth noting about "
    "this field</b>: the empirical result led, the explanation followed, "
    "and the explanation was wrong for three years while the technique "
    "was in every network. <b>It is a reason to hold mechanistic stories "
    "loosely and measurements tightly</b> — which is Module 03 "
    "&sect;4's position too."]),
  ("table", ["Type", "Normalises over", "Use when"],
   [["<b>Batch norm</b>",
     "<b>The batch dimension, separately per channel.</b>",
     "<b>Convolutional networks with batch size 32 or more.</b> <b>Breaks "
     "down at small batch sizes</b>, where the statistics are noisy."],
    ["<b>Layer norm</b>",
     "<b>The feature dimension, separately per example.</b>",
     "<b>Transformers and recurrent networks.</b> <b>Batch-independent</b>, "
     "so training and inference are identical and batch size does not "
     "matter — which is why it took over."],
    ["<b>Group norm</b>",
     "Groups of channels, per example.",
     "<b>Convolutional networks that must use small batches</b> — "
     "object detection, segmentation, 3D volumes, anything memory-bound."],
    ["<b>Instance norm</b>", "Each channel separately, per example.",
     "Style transfer, where removing per-image contrast and colour "
     "statistics is exactly the desired effect."],
    ["<b>RMSNorm</b>",
     "<b>Scale only — no mean subtraction.</b>",
     "<b>Cheaper than layer norm and works about as well</b>; common in "
     "large language models where the saving is material."]],
   [0.17, 0.35, 0.48]),
  ("callout", "Batch norm behaves differently at inference",
   ["<b>During training it normalises using the current mini-batch's mean "
    "and variance. At inference it uses a running average</b> of those "
    "statistics, accumulated over training.",
    "<b>So the function computed is genuinely different in the two "
    "modes</b> — and forgetting to switch modes is among the most "
    "common bugs in deep learning, producing results that are wrong by a "
    "plausible-looking margin.",
    "<b>And if the running statistics have not converged, inference is "
    "wrong even with entirely correct code</b> — which happens with "
    "short training runs, with an unusual data ordering, or when the "
    "momentum on the running average is badly set.",
    "<b>More fundamentally, it makes a training example's output depend on "
    "the <i>other examples in its batch</i></b>, which is a genuinely "
    "strange property for a model to have: the prediction for one input is "
    "not a function of that input alone. <b>It is the deepest reason layer "
    "norm is preferred wherever batch size varies or batch composition is "
    "not controlled</b>, and it causes real difficulties in distributed "
    "training (Module 08) where the batch is split across devices."]),

  ("break",),
  ("h1", "4 &nbsp; Augmentation"),
  ("callout", "Augmentation encodes invariances you already know",
   ["<b>A horizontally flipped photograph of a cat is still a photograph of "
    "a cat.</b> Training on both the image and its flip tells the model an "
    "invariance it would otherwise have to infer from examples — and "
    "inferring it costs data.",
    "<b>That is precisely the mechanism of Module 01 &sect;2</b> — "
    "encoded prior knowledge substituting for examples — <b>applied "
    "through the data rather than through the architecture.</b> "
    "Convolution builds translation invariance into the model; "
    "augmentation builds other invariances into the training distribution, "
    "and the two are alternatives for the same job.",
    "<b>And it is usually the single largest win available when data is "
    "limited</b>, well ahead of any amount of dropout or weight decay. "
    "Modern augmentation policies — RandAugment, mixup, CutMix "
    "— are a substantial part of why vision models improved without "
    "architectural change.",
    "<b>But the invariance must actually be true.</b> <b>A vertically "
    "flipped '6' is a '9'</b>; a mirrored chest radiograph depicts "
    "dextrocardia, which is a real and rare condition; a colour-jittered "
    "image of a banana may no longer be ripe. <b>A false augmentation "
    "teaches the model something wrong</b>, and it does so invisibly, "
    "degrading exactly the cases where the invariance fails."]),
  ("ul", ["<b>The loss will not move from its initial value:</b> an "
          "optimisation problem. Check initialisation, learning rate, and "
          "normalisation (Module 03 &sect;4), and run the overfit-one-batch "
          "test before anything else.",
          "<b>Trains well, large train–test gap:</b> a generalisation "
          "problem. <b>Augmentation first</b> (it is usually the largest "
          "effect), then weight decay, then dropout, <b>and more data if it "
          "is available</b> (CSCE 633 Module 03 &sect;1).",
          "<b>Trains, and both errors are high:</b> underfitting. More "
          "capacity, better features, or longer training — <b>and "
          "<i>remove</i> regularisation</b>, which is a legitimate move "
          "that is rarely considered because adding things feels like "
          "progress.",
          "<b>Results vary wildly between runs with the same "
          "configuration:</b> a learning rate or initialisation problem, not "
          "a regularisation one. <b>Run the same config three times before "
          "concluding anything from a single run.</b>",
          "<b>And add one thing at a time, measuring each.</b> <b>Stacking "
          "four regularisers simultaneously tells you nothing about which "
          "helped</b> — and in this field the answer is frequently "
          "'none of them, and the fourth one hurt'."]),
 ],
 "resources": [
   ("Srivastava et al. &mdash; Dropout (free)",
    "https://jmlr.org/papers/v15/srivastava14a.html",
    "The &sect;2 method and the ensemble argument, from the original."),
   ("Santurkar, Tsipras, Ilyas & Madry &mdash; How Does Batch "
    "Normalization Help Optimization? (free)",
    "https://arxiv.org/abs/1805.11604",
    "<b>The &sect;3 correction.</b> The noise-injection experiment is the "
    "part to read — it is a model of how to test a mechanistic "
    "claim."),
   ("Wu & He &mdash; Group Normalization (free)",
    "https://arxiv.org/abs/1803.08494",
    "The small-batch problem of &sect;3, measured, with the alternative."),
   ("Cubuk et al. &mdash; RandAugment (free)",
    "https://arxiv.org/abs/1909.13719",
    "The &sect;4 practice at its current state, with the search space "
    "reduced to two hyperparameters."),
 ],
 "exercises": [
   "<b>Implement inverted dropout</b> and verify the expected activation "
   "matches between train and inference.",
   "<b>Leave dropout active at inference</b> and measure how much worse "
   "the model is.",
   "Implement batch norm from scratch, including the running statistics.",
   "<b>Evaluate without switching to eval mode</b> and report the "
   "difference.",
   "<b>Train with batch size 2</b> and compare batch norm against group "
   "norm.",
   "Compare batch, layer, and RMS normalisation on the same transformer "
   "block.",
   "<b>Measure the effect of augmentation alone</b> against dropout alone "
   "against weight decay alone, on the same train–test gap.",
   "<b>Apply a false augmentation</b> (vertical flip on digits) and "
   "measure the damage.",
   "Stack four regularisers at once, then ablate them one at a time, and "
   "report which actually helped.",
   "Run the same configuration three times and report the spread.",
 ],
 "selfcheck": [
   "Distinguish normalisation from regularisation and say how to diagnose "
   "which you need.",
   "Why does inverted dropout scale during training?",
   "Give two accounts of why dropout helps.",
   "What was batch norm's original explanation, and how was it refuted?",
   "Compare five normalisation variants.",
   "Give three problems caused by batch norm's batch dependence.",
   "Why does augmentation work, and what is the mechanism it shares with "
   "architecture?",
   "Give an example of a false augmentation.",
   "Give five diagnoses and the response to each.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Convolutional Networks",
 "subtitle": "The architecture that made the case.",
 "question": "Why does convolution work so well on images?",
 "outcomes": [
     "Explain convolution as weight sharing plus locality.",
     "Compute receptive fields and reason about depth.",
     "Explain the standard architectural moves and why each was "
     "introduced.",
     "Explain what the learned filters represent.",
     "Explain where CNNs have been displaced and where they persist.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The operation",
   "blurb": "What it is and what it assumes."},

  {"t": "callout", "title": "Convolution is weight sharing with a locality constraint",
   "kind": "The two ideas",
   "body": ["<b>Locality:</b> each output depends on a small spatial "
            "neighbourhood, not the whole image.",
            "<b>Weight sharing:</b> the same small filter is applied at "
            "every position — so a feature learned anywhere is detectable "
            "everywhere.",
            "<b>Together these cut the parameter count by orders of "
            "magnitude</b> and build in translation equivariance: shift "
            "the input and the feature map shifts with it.",
            "<b>Note equivariance, not invariance.</b> Pooling and "
            "striding add approximate invariance; convolution alone does "
            "not. <b>Conflating the two is a common and consequential "
            "error.</b>"]},

  {"t": "eq", "kicker": "Receptive field", "title": "How far back each output sees",
   "eqs": [
     ("r₀ = 1;  rₗ = rₗ₋₁ + (kₗ − 1)·∏ⱼ<ₗ sⱼ",
      "Receptive field grows linearly with depth and multiplicatively with "
      "stride."),
     ("Ten 3×3 layers, stride 1 ⟹ 21×21",
      "Linear growth. Slow, and every layer is cheap."),
     ("Add stride 2 every other layer ⟹ grows much faster",
      "Which is why downsampling is in every architecture."),
   ],
   "caption": "<b>A unit can only use what is in its receptive field.</b> "
              "If the object is larger than it, the network literally "
              "cannot see the object.",
   "note": "Receptive field arithmetic explains many architecture "
           "decisions directly."},

  {"t": "section", "label": "Part 2", "title": "The architectural moves",
   "blurb": "Each introduced to fix a specific problem."},

  {"t": "table", "kicker": "Moves", "title": "The standard ideas, and what each fixed",
   "header": ["Idea", "Fixed", "Note"],
   "widths": [2.8, 4.2, 5.1],
   "rows": [
     ["<b>Stacked 3×3</b>", "<b>Large filters are expensive</b>", "<b>Two 3×3 = one 5×5 receptive field, fewer params</b>"],
     ["<b>1×1 convolution</b>", "Channel count explosion", "<b>Mixes channels; a per-pixel linear layer</b>"],
     ["<b>Residual blocks</b>", "<b>Vanishing gradients at depth</b>", "<b>Enabled 100+ layers (M02 §3)</b>"],
     ["<b>Batch norm</b>", "Training instability", "Allowed much higher learning rates (M04)"],
     ["<b>Depthwise separable</b>", "<b>Parameter and compute cost</b>", "<b>MobileNet; ~8× cheaper for similar accuracy</b>"],
     ["Global average pooling", "<b>Huge fully connected head</b>", "Replaced millions of parameters with none"],
     ["<b>Dilated convolution</b>", "<b>Receptive field without downsampling</b>", "Segmentation, where resolution matters"],
   ],
   "footnote": "<b>Every one of these was a response to a measured "
               "problem</b>, not an aesthetic preference — which is "
               "how to read an architecture paper.",
   "note": "Framing architecture as accumulated fixes demystifies it."},

  {"t": "callout", "title": "What the filters learn, and why it matters",
   "kind": "The empirical finding",
   "body": ["<b>Early layers learn edge and colour detectors</b> that "
            "look strikingly like Gabor filters — and like the receptive "
            "fields measured in mammalian visual cortex.",
            "<b>Middle layers learn textures and parts</b> — fur, "
            "wheels, eyes.",
            "<b>Late layers respond to objects and configurations.</b>",
            "<b>This hierarchy was not designed; it emerged</b>, and it "
            "appears consistently across architectures and datasets. "
            "<b>It is also the basis of transfer learning</b> "
            "(Module 09): early features are general and are worth "
            "reusing."]},

  {"t": "section", "label": "Part 3", "title": "Where CNNs stand",
   "blurb": "After vision transformers."},

  {"t": "callout", "title": "Transformers displaced CNNs at scale, not everywhere",
   "kind": "The honest position",
   "body": ["<b>Vision transformers beat CNNs given enough data</b> "
            "— hundreds of millions of images — because the weaker "
            "inductive bias becomes an advantage once the data can supply "
            "what the bias would have assumed.",
            "<b>Below that scale, CNNs remain competitive or better</b>, "
            "which is Module 01 §2's argument: a correct prior "
            "substitutes for data, and the substitution stops mattering "
            "when data is abundant.",
            "<b>And modern CNNs narrowed the gap</b> — ConvNeXt applied "
            "transformer-era training recipes to a CNN and matched "
            "transformers.",
            "<b>So much of the reported advantage was training recipe, "
            "not architecture</b> — which is a recurring finding in this "
            "field and a reason to be careful when comparing "
            "architectures."]},

  {"t": "bullets", "kicker": "Still CNN", "title": "Where convolution still wins",
   "items": [
     "<b>Limited data</b> — the inductive bias is worth the "
     "constraint.",
     "",
     "<b>Limited compute or latency</b> — convolution is cheaper per "
     "unit of accuracy, and the hardware is optimised for it.",
     "",
     "<b>High resolution</b> — attention is quadratic in token count; "
     "convolution is linear in pixels.",
     "",
     "<b>Dense prediction</b> — segmentation and depth, where spatial "
     "structure is the output.",
     "",
     "<b>And on-device inference</b>, where depthwise separable "
     "convolutions and integer quantisation are mature.",
   ],
   "footnote": "<b>Most deployed vision models are still "
               "convolutional</b>, which the research literature does not "
               "reflect."},

  {"t": "section", "label": "Part 4", "title": "The graphics connection",
   "blurb": "Where this course's track meets it."},

  {"t": "callout", "title": "Convolution in the rendering pipeline",
   "kind": "Why this matters for the track",
   "body": ["<b>Learned denoising</b> (CSCE 647 M12) is a CNN "
            "operating on a noisy render plus auxiliary buffers — "
            "normals, albedo, depth. <b>It made path tracing "
            "interactive.</b>",
            "<b>Super-resolution and frame generation</b> — DLSS and "
            "its relatives are convolutional, and they are now part of the "
            "standard pipeline.",
            "<b>And both exploit exactly the locality assumption:</b> a "
            "pixel's correct value depends on its neighbourhood and on "
            "the geometry buffers, which is true of rendering in a way it "
            "is not of arbitrary data.",
            "<b>So the architecture matches the domain</b> — which is "
            "Module 01 §2, and the reason these worked almost "
            "immediately once tried."]},
 ],
 "takeaways": [
   "Convolution is locality plus weight sharing, which cuts parameters by "
   "orders of magnitude and builds in translation equivariance.",
   "Equivariance is not invariance — pooling and striding add the "
   "latter, and conflating them is a consequential error.",
   "A unit cannot use anything outside its receptive field, so receptive "
   "field arithmetic directly constrains architecture.",
   "Every standard architectural move was a response to a measured problem, "
   "which is how to read an architecture paper.",
   "The edge–texture–object hierarchy emerged rather than being "
   "designed, and it is the basis of transfer learning.",
   "Transformers beat CNNs given hundreds of millions of images; below that "
   "the inductive bias still pays, and much of the reported gap was "
   "training recipe.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The operation"),
  ("callout", "Convolution is weight sharing with a locality constraint",
   ["<b>Locality:</b> each output value depends only on a small spatial "
    "neighbourhood of the input, not on the whole image. This encodes the "
    "assumption that what matters about a pixel is determined nearby.",
    "<b>Weight sharing:</b> the same small filter is applied at every "
    "spatial position, so a feature learned at one location is detectable "
    "at all of them — and the parameters do not grow with image size.",
    "<b>Together these reduce the parameter count by orders of "
    "magnitude</b> relative to a fully connected layer and build in "
    "<i>translation equivariance</i>: translate the input and the feature "
    "map translates identically.",
    "<b>Note equivariance, not invariance.</b> The feature map <i>moves</i> "
    "with the input; it does not stay the same. Pooling, striding, and "
    "eventually global pooling introduce approximate invariance, and "
    "convolution alone does not. <b>Conflating the two is a common and "
    "consequential error</b> — it leads people to expect a CNN to be "
    "robust to translation when the architecture only guarantees that the "
    "representation shifts predictably, and the robustness actually comes "
    "from pooling and augmentation."]),
  ("eq", "r<sub>l</sub> = r<sub>l&minus;1</sub> + (k<sub>l</sub> &minus; 1) "
         "&middot; &prod;<sub>j&lt;l</sub> s<sub>j</sub>"),
  ("p", "The receptive field of a unit — the region of the input it "
        "can possibly depend on — <b>grows linearly with depth and "
        "multiplicatively with stride.</b> Ten 3&times;3 layers at stride 1 "
        "give a 21&times;21 receptive field, which is small for a "
        "224&times;224 image; <b>adding a stride-2 layer every other block "
        "makes it grow far faster, which is why downsampling appears in "
        "every architecture.</b> <b>A unit cannot use information outside "
        "its receptive field</b> — so if the object to be recognised "
        "is larger than the receptive field at the layer where the decision "
        "is made, <b>the network literally cannot see the object</b>, and "
        "no amount of training fixes it. Receptive field arithmetic is "
        "therefore a design constraint rather than an analysis, and it "
        "explains several architecture choices directly."),

  ("h1", "2 &nbsp; The architectural moves"),
  ("table", ["Idea", "What it fixed", "Note"],
   [["<b>Stacks of 3&times;3 filters</b>",
     "<b>Large filters are expensive</b> — a 7&times;7 filter has 49 "
     "parameters per channel pair.",
     "<b>Two stacked 3&times;3 layers have the same 5&times;5 receptive "
     "field with fewer parameters and an extra nonlinearity.</b> VGG's "
     "contribution, and it has stuck."],
    ["<b>1&times;1 convolution</b>",
     "Channel counts exploding as depth increases.",
     "<b>Mixes channels without touching space</b> — it is a per-pixel "
     "linear layer, and it makes bottleneck blocks possible."],
    ["<b>Residual blocks</b>", "<b>Vanishing gradients at depth.</b>",
     "<b>Enabled networks beyond a hundred layers</b> (Module 02 "
     "&sect;3). The most important single entry in this table."],
    ["<b>Batch normalisation</b>", "Training instability and slow "
     "convergence.",
     "Permitted much larger learning rates (Module 04 &sect;3)."],
    ["<b>Depthwise separable convolution</b>",
     "<b>Parameter and compute cost on mobile hardware.</b>",
     "<b>Factors a convolution into a per-channel spatial filter and a "
     "1&times;1 mixing step</b> — roughly 8&times; cheaper for "
     "comparable accuracy. MobileNet, and now widespread."],
    ["<b>Global average pooling</b>",
     "<b>An enormous fully connected head</b> — AlexNet's dense layers "
     "held most of its parameters.",
     "Averages each channel to a single number, replacing millions of "
     "parameters with none and improving generalisation."],
    ["<b>Dilated (atrous) convolution</b>",
     "<b>Growing the receptive field without losing resolution.</b>",
     "Segmentation and dense prediction, where downsampling destroys "
     "exactly what the output needs."]],
   [0.21, 0.36, 0.43]),
  ("callout", "What the filters learn, and why it matters",
   ["<b>Early layers learn oriented edge and colour-opponent detectors</b> "
    "that look strikingly like Gabor filters — and strikingly like the "
    "receptive fields measured in mammalian primary visual cortex decades "
    "earlier. <b>Nobody put them there.</b>",
    "<b>Middle layers respond to textures and object parts</b> — fur, "
    "mesh patterns, wheels, eyes — and late layers to whole objects "
    "and configurations.",
    "<b>This hierarchy was not designed; it emerged from the "
    "objective</b>, and it appears consistently across architectures, "
    "datasets, and training runs. It is one of the more genuinely "
    "surprising empirical results in the field.",
    "<b>And it is the basis of transfer learning</b> (Module 09): "
    "<b>early features are general</b> — edges are edges regardless of "
    "the task — <b>so they are worth reusing</b>, while late features "
    "are task-specific and are what fine-tuning replaces. The practical "
    "importance of this finding is hard to overstate; it is why a model "
    "trained on ImageNet is a useful starting point for medical imaging."]),

  ("break",),
  ("h1", "3 &nbsp; Where CNNs stand now"),
  ("callout", "Transformers displaced CNNs at scale, not everywhere",
   ["<b>Vision transformers outperform CNNs given enough data</b> — on "
    "the order of hundreds of millions of images — because attention's "
    "weaker inductive bias becomes an <i>advantage</i> once the data can "
    "supply what the bias would otherwise have assumed, and can discover "
    "relationships the bias would have excluded.",
    "<b>Below that scale, CNNs remain competitive or better.</b> This is "
    "exactly Module 01 &sect;2's argument: <b>a correct prior substitutes "
    "for data, and the substitution stops mattering when data is "
    "abundant</b> — so the crossover point is a data-quantity "
    "question, not an architectural one.",
    "<b>And modern CNNs substantially narrowed the gap.</b> ConvNeXt took "
    "a ResNet and applied the training recipe developed for transformers "
    "— the augmentation, the optimiser, the schedule, the "
    "normalisation choices — and matched transformer performance "
    "without changing the fundamental operation.",
    "<b>So much of the reported architectural advantage was training "
    "recipe rather than architecture.</b> <b>This is a recurring finding "
    "in this field</b>, and it is a strong reason to be sceptical of "
    "architecture comparisons where the training procedures differ — "
    "which they almost always do, because each paper tunes its own method "
    "and inherits the baseline's hyperparameters from an older paper."]),
  ("ul", ["<b>Limited data</b> — the inductive bias is worth the "
          "constraint, which covers most applied problems outside the "
          "largest labs.",
          "<b>Limited compute or tight latency</b> — convolution is "
          "cheaper per unit of accuracy, and a decade of hardware and "
          "compiler work has been aimed at it specifically (CSCE 735 "
          "Module 09).",
          "<b>High resolution</b> — <b>attention is quadratic in token "
          "count while convolution is linear in pixels</b>, so a "
          "4K image is a very different proposition for the two.",
          "<b>Dense prediction</b> — segmentation, depth estimation, "
          "optical flow, denoising — where the output has spatial "
          "structure and resolution must be preserved.",
          "<b>And on-device inference</b>, where depthwise separable "
          "convolutions, integer quantisation (Module 13), and dedicated "
          "accelerators are all mature for convolution and less so for "
          "attention. <b>Most deployed vision models are still "
          "convolutional</b>, which the research literature does not "
          "reflect and which is worth knowing when reading it."]),

  ("h1", "4 &nbsp; The graphics connection"),
  ("callout", "Convolution in the rendering pipeline",
   ["<b>Learned denoising</b> (CSCE 647 Module 12) is a convolutional "
    "network operating on a sparsely-sampled noisy render together with "
    "auxiliary geometry buffers — surface normals, albedo, depth, "
    "motion vectors. <b>It made path tracing interactive</b>, which a "
    "decade of sampling improvements had not.",
    "<b>Super-resolution and frame generation</b> — DLSS and its "
    "competitors — are likewise convolutional, and are now a standard "
    "part of the real-time pipeline rather than an experiment.",
    "<b>And both exploit precisely the locality assumption:</b> a pixel's "
    "correct value depends on its spatial neighbourhood and on the "
    "geometric buffers at that neighbourhood — <b>which is genuinely "
    "true of rendering in a way it is not true of arbitrary data</b>, "
    "because the rendering equation itself is local in screen space given "
    "the geometry.",
    "<b>So the architecture matches the domain</b>, which is Module 01 "
    "&sect;2 again, <b>and it is why these methods worked almost "
    "immediately once anyone tried them</b> — the prior was correct, "
    "the auxiliary buffers were already being computed, and the training "
    "data could be generated in unlimited quantity by rendering the same "
    "scene at high sample counts."]),
 ],
 "resources": [
   ("Stanford CS231n &mdash; convolutional networks notes (free)",
    "https://cs231n.github.io/convolutional-networks/",
    "<b>The reference for &sect;1 and &sect;2</b>, including the receptive "
    "field arithmetic and the architecture history."),
   ("He et al. &mdash; Deep Residual Learning; Howard et al. &mdash; "
    "MobileNets (free)",
    "https://arxiv.org/abs/1704.04861",
    "Two of &sect;2's rows, from their papers. The depthwise separable "
    "factorisation is worth deriving once."),
   ("Liu et al. &mdash; A ConvNet for the 2020s (ConvNeXt) (free)",
    "https://arxiv.org/abs/2201.03545",
    "<b>The &sect;3 result.</b> A step-by-step modernisation of a ResNet, "
    "with each change measured — which is also a model of how to "
    "ablate."),
   ("Chaitanya et al. &mdash; Interactive Reconstruction of Monte Carlo "
    "Image Sequences (free)",
    "https://research.nvidia.com/publication/interactive-reconstruction-monte-carlo-image-sequences-using-recurrent-denoising",
    "<b>The &sect;4 denoiser</b>, and the connection back to CSCE 647."),
 ],
 "exercises": [
   "Implement 2D convolution from scratch and verify against the "
   "framework.",
   "<b>Count the parameters</b> of a convolutional and a fully connected "
   "layer with identical input and output shapes.",
   "<b>Compute the receptive field</b> of each layer in a network you use, "
   "and compare against the object sizes in your data.",
   "<b>Demonstrate equivariance and the lack of invariance</b>: shift an "
   "input and compare the feature maps, then compare the final "
   "predictions.",
   "Replace one 5&times;5 layer with two 3&times;3 and compare parameters, "
   "compute, and accuracy.",
   "<b>Implement a depthwise separable convolution</b> and measure the "
   "saving.",
   "Replace a fully connected head with global average pooling and report "
   "the parameter reduction.",
   "<b>Visualise the first-layer filters</b> of a trained network.",
   "Visualise what maximally activates units at three different depths.",
   "<b>Train a CNN and a vision transformer</b> on the same small dataset "
   "and report which wins and why.",
 ],
 "selfcheck": [
   "What two ideas is convolution, and what does each buy?",
   "Distinguish equivariance from invariance and say where each comes "
   "from.",
   "Compute a receptive field and say why it constrains architecture.",
   "Give seven architectural moves and the problem each fixed.",
   "What do early, middle, and late filters learn, and why does that "
   "matter?",
   "When do transformers beat CNNs, and what explains the crossover?",
   "What did ConvNeXt show?",
   "Give five places convolution still wins.",
   "How is convolution used in the rendering pipeline?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Sequences and Attention",
 "subtitle": "Why recurrence lost.",
 "question": "How do you model data where order matters?",
 "outcomes": [
     "Explain recurrent networks and their two fatal problems.",
     "Explain LSTM gating and what it fixes.",
     "Derive attention and explain each term.",
     "Explain why attention replaced recurrence.",
     "State attention's cost and its consequences.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Recurrence",
   "blurb": "The obvious approach, and why it failed."},

  {"t": "callout", "title": "An RNN applies the same function at every step",
   "kind": "The idea",
   "body": ["<b>h_t = f(h_{t−1}, x_t)</b> — a hidden state carried "
            "forward, updated by the same learned function at every "
            "position.",
            "<b>So the parameter count is independent of sequence "
            "length</b>, and the same dynamics apply everywhere. That is "
            "the right inductive bias for a sequence (Module 01 §2).",
            "<b>Training is backpropagation through time</b> — unroll "
            "the recurrence and apply Module 02's machinery to the "
            "unrolled graph.",
            "<b>And the unrolled graph is as deep as the sequence is "
            "long</b>, which is where both of the problems come from."]},

  {"t": "table", "kicker": "Problems", "title": "The two that killed it",
   "header": ["Problem", "Cause", "Consequence"],
   "widths": [2.7, 4.3, 5.1],
   "rows": [
     ["<b>Vanishing gradients</b>", "<b>The same Jacobian multiplied T times</b>", "<b>Cannot learn long-range dependence</b>"],
     ["<b>No parallelism</b>", "<b>Step t needs step t−1</b>", "<b>Training time scales with sequence length</b>"],
   ],
   "footnote": "<b>LSTM and GRU largely fixed the first.</b> <b>Nothing "
               "fixes the second</b>, and on modern hardware that is "
               "decisive.",
   "note": "The parallelism point is the one that actually ended "
           "recurrence."},

  {"t": "callout", "title": "LSTM gating is the residual connection, in time",
   "kind": "The fix, and its limit",
   "body": ["<b>An LSTM carries a cell state updated additively</b>, "
            "with learned gates controlling what is written, forgotten, "
            "and read.",
            "<b>The additive path means the gradient can flow backward "
            "through many steps with factor near 1</b> — which is exactly "
            "the residual connection mechanism (Module 02 §3), "
            "discovered earlier in a different setting.",
            "<b>So long-range dependence became learnable</b>, and "
            "LSTMs dominated sequence modelling for roughly a decade.",
            "<b>But the sequential dependency remains.</b> <b>A GPU with "
            "thousands of cores sits idle while a sequence is processed one "
            "element at a time</b>, and that is what attention "
            "removed."]},

  {"t": "section", "label": "Part 2", "title": "Attention",
   "blurb": "Look at everything, weighted by relevance."},

  {"t": "eq", "kicker": "Attention", "title": "The operation",
   "eqs": [
     ("Attention(Q,K,V) = softmax(QKᵀ / √d_k) V",
      "Queries, keys, values. Each output is a weighted average of "
      "values."),
     ("QKᵀ gives the relevance of each key to each query",
      "A similarity score for every pair of positions."),
     ("The √d_k divisor keeps the softmax from saturating",
      "Dot products grow with dimension; without it the gradients "
      "vanish."),
   ],
   "caption": "<b>Every term has a reason.</b> The scaling factor in "
              "particular is not cosmetic — omit it and training "
              "fails at large d.",
   "note": "Students skip the scaling; it's a good concrete detail."},

  {"t": "code", "kicker": "Intuition", "title": "What Q, K, and V actually are",
   "lang": "text", "code": """
  A soft dictionary lookup.

    QUERY  "what am I looking for?"       -- from the current position
    KEY    "what do I offer?"             -- from every position
    VALUE  "what do I contribute if chosen?"

  A hard lookup would take the single best-matching key.
  Attention takes a WEIGHTED AVERAGE of all values, with weights
  from the query-key similarities. Soft, and differentiable.

  SELF-ATTENTION: Q, K, V all come from the same sequence, so
  every position attends to every other -- including itself.

  WHY IT BEAT RECURRENCE:
    * PATH LENGTH between any two positions is 1, not T.
      No multiplied Jacobians, so no vanishing over distance.
    * FULLY PARALLEL. All positions computed simultaneously --
      one big matrix multiply, which is exactly what GPUs do
      best (CSCE 735 M09).
    * The relationships are LEARNED, not fixed by architecture.

  THE COST: O(T^2) in time and memory. Attention is quadratic.
""",
   "caption": "<b>Constant path length and full parallelism</b> — "
              "either alone would have been significant; together they "
              "ended recurrence.",
   "note": "The dictionary metaphor is the one that actually helps."},

  {"t": "section", "label": "Part 3", "title": "The cost",
   "blurb": "Quadratic, and what follows from it."},

  {"t": "callout", "title": "Quadratic cost is the defining constraint",
   "kind": "What it determines",
   "body": ["<b>Every pair of positions is scored, so cost grows as "
            "T².</b> Doubling the context length quadruples the compute "
            "and the memory.",
            "<b>That is why context windows were small and why extending "
            "them is a research area</b> rather than a configuration "
            "change.",
            "<b>FlashAttention does not change the asymptotics</b> — it "
            "removes the materialisation of the T×T matrix by "
            "tiling, which is a memory-bandwidth win (CSCE 735 M09) "
            "and a very large practical one.",
            "<b>And the approximations — sparse, linear, sliding "
            "window — trade exactness for scale</b>, with mixed results. "
            "<b>Exact attention with better memory behaviour has mostly "
            "won.</b>"]},

  {"t": "section", "label": "Part 4", "title": "What attention assumes",
   "blurb": "Closing the inductive bias argument."},

  {"t": "callout", "title": "Attention is a weaker prior, deliberately",
   "kind": "The trade",
   "body": ["<b>Convolution asserts that nearby things relate.</b> "
            "Recurrence asserts that order matters and the dynamics are "
            "uniform.",
            "<b>Attention asserts only that <i>some</i> pairs relate, and "
            "learns which.</b> It imposes almost no structure — "
            "positional information has to be added back explicitly "
            "(Module 07).",
            "<b>So it needs more data and scales further</b>, which is "
            "Module 01 §2's trade at its sharpest.",
            "<b>And that is why the same architecture now works on text, "
            "images, audio, video, and proteins</b> — <b>a prior weak "
            "enough to be wrong about nothing is also general enough to "
            "apply to everything.</b>"]},
 ],
 "takeaways": [
   "An RNN applies the same function at each step, so the unrolled graph is "
   "as deep as the sequence is long — which causes both of its "
   "problems.",
   "LSTM gating gives the gradient an additive path through time, which is "
   "the residual connection mechanism discovered earlier.",
   "Gating fixed vanishing gradients; nothing fixes the lack of "
   "parallelism, and on modern hardware that was decisive.",
   "Attention is a soft differentiable dictionary lookup: queries match "
   "keys, and the output is a weighted average of values.",
   "Path length between any two positions is 1 rather than T, and all "
   "positions compute in parallel — either alone would have been "
   "significant.",
   "Attention is quadratic in sequence length, which is the defining "
   "constraint on context size, and it encodes almost no prior, which is "
   "why it generalises across domains.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Recurrence"),
  ("callout", "An RNN applies the same function at every step",
   ["<b>h<sub>t</sub> = f(h<sub>t&minus;1</sub>, x<sub>t</sub>)</b> — "
    "a hidden state carried forward through the sequence, updated by the "
    "same learned function at every position.",
    "<b>So the parameter count is independent of sequence length</b>, and "
    "the same dynamics are applied everywhere. <b>That is exactly the "
    "right inductive bias for a sequence</b> (Module 01 &sect;2), and it "
    "is why recurrence was the obvious and correct-seeming approach for "
    "decades.",
    "<b>Training is backpropagation through time:</b> unroll the "
    "recurrence into a feedforward graph with one copy of f per timestep, "
    "and apply Module 02's machinery to the unrolled graph.",
    "<b>And the unrolled graph is as deep as the sequence is long.</b> "
    "<b>Both of recurrence's fatal problems come from that single "
    "fact</b> — which is a good illustration of how an architectural "
    "choice determines a set of consequences that look unrelated."]),
  ("table", ["Problem", "Cause", "Consequence"],
   [["<b>Vanishing (and exploding) gradients</b>",
     "<b>The same Jacobian multiplied T times</b> — Module 02 "
     "&sect;3's product, with T in the hundreds or thousands.",
     "<b>Long-range dependence cannot be learned.</b> A word at position 5 "
     "cannot influence a prediction at position 500 because no gradient "
     "survives the journey."],
    ["<b>No parallelism</b>",
     "<b>Step t requires step t&minus;1</b>, by definition. The "
     "computation is inherently sequential.",
     "<b>Training time scales with sequence length</b>, and a GPU with "
     "thousands of cores processes one element at a time. <b>This is the "
     "one that actually ended recurrence.</b>"]],
   [0.24, 0.38, 0.38]),
  ("callout", "LSTM gating is the residual connection, in time",
   ["<b>An LSTM carries a cell state that is updated <i>additively</i></b>, "
    "with learned gates controlling what is written into it, what is "
    "forgotten from it, and what is read out.",
    "<b>The additive path means the gradient can flow backward across many "
    "timesteps with a multiplicative factor near one</b> — which is "
    "precisely the residual connection mechanism of Module 02 &sect;3, "
    "discovered years earlier in a different setting and for a different "
    "stated reason. <b>The same structural idea, arrived at twice.</b>",
    "<b>So long-range dependence became learnable</b>, and LSTMs and GRUs "
    "dominated sequence modelling for roughly a decade — machine "
    "translation, speech recognition, language modelling.",
    "<b>But the sequential dependency remains, and gating does nothing "
    "about it.</b> <b>A GPU with thousands of cores sits almost entirely "
    "idle while a sequence is processed one element at a time</b> "
    "(CSCE 735 Module 08) — the hardware got enormously wider and "
    "the architecture could not use it. <b>That is what attention "
    "removed, and it is why the replacement was so complete.</b>"]),

  ("h1", "2 &nbsp; Attention"),
  ("eq", "Attention(Q, K, V) = softmax(QK<super>T</super> / "
         "&radic;d<sub>k</sub>) V"),
  ("p", "<b>Every term has a reason.</b> QK<super>T</super> computes a "
        "relevance score between every query and every key. The softmax "
        "turns those scores into weights that sum to one. Multiplying by V "
        "produces a weighted average of the values. <b>And the "
        "&radic;d<sub>k</sub> divisor is not cosmetic:</b> dot products of "
        "random vectors grow in magnitude with the dimension, so without "
        "the scaling the softmax saturates at large d, its gradients vanish "
        "(Module 02 &sect;3), and training fails. <b>Omitting it is a "
        "real bug that only manifests at large model dimension</b>, which "
        "makes it hard to catch in a small test."),
  ("code", """A SOFT DICTIONARY LOOKUP

  QUERY  "what am I looking for?"        from the current position
  KEY    "what do I offer?"              from every position
  VALUE  "what do I contribute if chosen?"

A hard lookup takes the single best-matching key.
Attention takes a WEIGHTED AVERAGE of all values, weighted by
query-key similarity. Soft, and therefore differentiable.

SELF-ATTENTION: Q, K and V all come from the same sequence, so
every position attends to every other, including itself.

WHY IT BEAT RECURRENCE
  * PATH LENGTH between any two positions is 1, not T.
    No multiplied Jacobians, so no vanishing over distance.
  * FULLY PARALLEL -- all positions at once, as one large matrix
    multiply, which is exactly what GPUs do best (CSCE 735 M09).
  * relationships are LEARNED, not fixed by the architecture.

THE COST: O(T^2) in time and memory."""),

  ("break",),
  ("h1", "3 &nbsp; The quadratic cost"),
  ("callout", "Quadratic cost is the defining constraint",
   ["<b>Every pair of positions is scored, so the cost grows as "
    "T&#178;</b> in both time and memory. <b>Doubling the context length "
    "quadruples both.</b>",
    "<b>That is why context windows were historically small and why "
    "extending them is a research area rather than a configuration "
    "change</b> — the constraint is structural, not an implementation "
    "limit.",
    "<b>FlashAttention does not change the asymptotics.</b> It avoids ever "
    "materialising the full T&times;T attention matrix in memory, by tiling "
    "the computation and recomputing what it needs — <b>which is a "
    "memory-bandwidth optimisation</b> (CSCE 735 Module 09 &sect;1, "
    "exactly the tiling argument) <b>and a very large practical win</b>, "
    "enabling far longer contexts at the same hardware. It is still "
    "quadratic in arithmetic.",
    "<b>And the approximate variants — sparse attention, linear "
    "attention, sliding windows — trade exactness for scale</b>, with "
    "genuinely mixed results: many report strong benchmark numbers and "
    "underperform exact attention on careful comparison. <b>Exact "
    "attention with better memory behaviour has mostly won</b>, which is a "
    "recurring pattern (CSCE 735 Module 09: fix the memory traffic before "
    "changing the algorithm)."]),

  ("h1", "4 &nbsp; What attention assumes"),
  ("callout", "Attention is a weaker prior, deliberately",
   ["<b>Convolution asserts that nearby things relate and that position "
    "does not change meaning.</b> <b>Recurrence asserts that order matters "
    "and that the dynamics are uniform across the sequence.</b> Both are "
    "strong, specific claims about the data.",
    "<b>Attention asserts only that <i>some</i> pairs of positions relate, "
    "and learns which ones.</b> It imposes almost no structure — so "
    "little that <b>positional information has to be added back "
    "explicitly</b>, because the operation is otherwise entirely "
    "permutation-equivariant (Module 07 &sect;2).",
    "<b>So it needs more data and scales further</b>, which is Module 01 "
    "&sect;2's trade at its sharpest: the weakest useful prior, maximum "
    "data appetite, and the highest ceiling.",
    "<b>And that is why the same architecture now works on text, images, "
    "audio, video, point clouds, and protein sequences.</b> <b>A prior weak "
    "enough to be wrong about nothing is also general enough to apply to "
    "everything</b> — which is the single sentence that explains the "
    "transformer's spread across every domain in the space of a few years, "
    "and is the most important idea in this module."]),
 ],
 "resources": [
   ("Karpathy &mdash; 'Let's build GPT' (free)",
    "https://karpathy.ai/zero-to-hero.html",
    "<b>Attention built from scratch on video</b>, with every design choice "
    "explained as it is typed. The best resource for &sect;2."),
   ("Bahdanau, Cho & Bengio &mdash; Neural Machine Translation by Jointly "
    "Learning to Align and Translate (free)",
    "https://arxiv.org/abs/1409.0473",
    "<b>Attention's first appearance</b>, bolted onto an RNN. Worth "
    "reading to see the problem it was invented to solve."),
   ("Christopher Olah &mdash; Understanding LSTM Networks (free)",
    "https://colah.github.io/posts/2015-08-Understanding-LSTMs/",
    "The clearest explanation of &sect;1's gating that exists, with "
    "diagrams that actually help."),
   ("Dao et al. &mdash; FlashAttention (free)",
    "https://arxiv.org/abs/2205.14135",
    "<b>The &sect;3 memory argument</b> — and a direct application of "
    "CSCE 735 Module 09's tiling to a problem in this course."),
 ],
 "exercises": [
   "Implement a vanilla RNN and train it on a long-range dependency task.",
   "<b>Measure how far back it can learn</b> by varying the dependency "
   "distance.",
   "Implement an LSTM and repeat. Plot the achievable distance for each.",
   "<b>Measure training throughput against sequence length</b> for an RNN "
   "and for attention on the same hardware.",
   "Implement scaled dot-product attention from scratch.",
   "<b>Remove the &radic;d<sub>k</sub> scaling</b> and show training fails "
   "at large model dimension while succeeding at small.",
   "<b>Visualise the attention weights</b> on a real sequence and look for "
   "interpretable patterns.",
   "Measure attention's time and memory against sequence length and "
   "confirm the quadratic growth.",
   "<b>Implement a simple tiled attention</b> that avoids materialising "
   "the full matrix, and measure the memory saving.",
   "Compare a sliding-window approximation against exact attention on a "
   "task needing long-range dependence.",
 ],
 "selfcheck": [
   "State the RNN recurrence and say where both its problems come from.",
   "What does LSTM gating fix, and what mechanism does it share with "
   "residual connections?",
   "What does gating not fix, and why was that decisive?",
   "Write the attention equation and explain every term.",
   "What are queries, keys, and values?",
   "Give three reasons attention beat recurrence.",
   "Why is attention quadratic, and what does FlashAttention actually "
   "change?",
   "Why is attention a weaker prior, and what follows from that?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Transformers",
 "subtitle": "The architecture that absorbed every domain.",
 "question": "What is in a transformer block, and why each piece?",
 "outcomes": [
     "Explain every component of a transformer block.",
     "Explain multi-head attention and what the heads do.",
     "Explain positional encoding and compare the schemes.",
     "Distinguish encoder, decoder, and encoder–decoder uses.",
     "Explain scaling laws and what they predict.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The block",
   "blurb": "Four components, each with a job."},

  {"t": "code", "kicker": "The block", "title": "What is in it, and why",
   "lang": "text", "code": """
  x = x + MultiHeadAttention(LayerNorm(x))      # mix across positions
  x = x + FeedForward(LayerNorm(x))             # process each position

  FOUR COMPONENTS, FOUR JOBS:

  1. MULTI-HEAD ATTENTION  -- the only operation that moves
     information BETWEEN positions. Everything else is per-token.

  2. FEED-FORWARD  -- two linear layers with a nonlinearity,
     applied identically at every position, with an inner
     dimension typically 4x the model dimension.
     This holds MOST OF THE PARAMETERS. Attention mixes;
     the feed-forward does the computing.

  3. RESIDUAL CONNECTIONS  -- gradient highway (M02 section 3).
     Without them, deep transformers do not train.

  4. LAYER NORM  -- batch-independent, so sequence length and
     batch size do not affect it (M04 section 3).

  PRE-NORM (norm before the sublayer, as written above) trains
  far more stably than POST-NORM (the original paper's order),
  which needed careful warmup to train at all. Almost everything
  modern is pre-norm.
""",
   "caption": "<b>Attention mixes across positions; the feed-forward does "
              "the computation.</b> That division is the clearest way to "
              "read the block.",
   "note": "The pre-norm/post-norm detail is practically important and "
           "usually omitted."},

  {"t": "section", "label": "Part 2", "title": "Heads and positions",
   "blurb": "Two details that carry a lot of weight."},

  {"t": "callout", "title": "Multiple heads attend to different things",
   "kind": "Why not one big attention",
   "body": ["<b>Split the model dimension into h heads, attend "
            "independently in each, and concatenate.</b> Same total "
            "compute, different structure.",
            "<b>One attention distribution can only express one notion of "
            "relevance per position.</b> Several heads can attend by "
            "syntax, by coreference, by position, and by topic "
            "simultaneously.",
            "<b>And interpretable heads do appear</b> — previous-token "
            "heads, induction heads that complete repeated patterns, "
            "syntactic heads.",
            "<b>Though many heads are redundant.</b> A substantial "
            "fraction can be pruned with little loss, which is a recurring "
            "finding and the basis of several compression methods "
            "(Module 13)."]},

  {"t": "callout", "title": "Attention has no idea what order things are in",
   "kind": "The gap positional encoding fills",
   "body": ["<b>Self-attention is permutation-equivariant.</b> Shuffle "
            "the input tokens and the outputs shuffle identically — the "
            "operation sees a <i>set</i>, not a sequence.",
            "<b>So position must be injected explicitly</b>, or the model "
            "cannot distinguish 'dog bites man' from 'man bites dog'.",
            "<b>The schemes differ in how they extrapolate</b> beyond "
            "trained lengths, which is the practical question.",
            "<b>RoPE rotates the query and key vectors by an "
            "angle proportional to position</b>, so the attention score "
            "depends on <i>relative</i> position naturally. <b>It is the "
            "current default and extrapolates better than the "
            "alternatives.</b>"]},

  {"t": "table", "kicker": "Position", "title": "Positional encoding schemes",
   "header": ["Scheme", "How", "Extrapolates?"],
   "widths": [2.7, 4.4, 5.0],
   "rows": [
     ["<b>Sinusoidal</b>", "Fixed sin/cos at many frequencies", "<b>Somewhat; the original choice</b>"],
     ["<b>Learned absolute</b>", "<b>An embedding per position</b>", "<b>No — fails past trained length</b>"],
     ["<b>Relative</b>", "Bias based on position difference", "Better"],
     ["<b>RoPE</b>", "<b>Rotate Q and K by a position-dependent angle</b>", "<b>Well. The current default</b>"],
     ["ALiBi", "<b>Linear distance penalty on scores</b>", "<b>Very well; trivially simple</b>"],
   ],
   "footnote": "<b>Learned absolute encodings simply have no value for "
               "positions never seen</b>, which is why long-context work "
               "abandoned them.",
   "note": "ALiBi's simplicity relative to its effectiveness is "
           "striking."},

  {"t": "section", "label": "Part 3", "title": "Three configurations",
   "blurb": "The same block, arranged differently."},

  {"t": "table", "kicker": "Configurations", "title": "Encoder, decoder, and both",
   "header": ["Type", "Attention", "Used for"],
   "widths": [2.6, 4.3, 5.2],
   "rows": [
     ["<b>Encoder only</b>", "<b>Bidirectional — sees everything</b>", "<b>Classification, embeddings. BERT</b>"],
     ["<b>Decoder only</b>", "<b>Causal — masked to the past</b>", "<b>Generation. GPT, and most LLMs</b>"],
     ["<b>Encoder–decoder</b>", "Encoder bidirectional; decoder cross-attends", "<b>Translation, summarisation. T5</b>"],
   ],
   "footnote": "<b>The causal mask is the entire difference</b> between "
               "the first two — one upper-triangular mask on the "
               "attention scores.",
   "note": "That such a small change produces such different models is "
           "worth stating."},

  {"t": "section", "label": "Part 4", "title": "Scaling",
   "blurb": "The empirical regularity."},

  {"t": "callout", "title": "Scaling laws are smooth power laws, and they held",
   "kind": "The finding that shaped the field",
   "body": ["<b>Loss falls as a power law in parameters, data, and "
            "compute</b> — over many orders of magnitude, with "
            "remarkably little scatter.",
            "<b>So performance became <i>predictable</i> before "
            "training</b>, which turned model development into a budgeting "
            "exercise rather than an experiment.",
            "<b>Chinchilla corrected the ratio:</b> earlier large models "
            "were badly under-trained on data, and <b>parameters and "
            "tokens should scale together</b>, roughly 20 tokens per "
            "parameter.",
            "<b>And the laws describe the loss, not capability.</b> "
            "<b>Whether specific abilities appear smoothly or suddenly "
            "depends heavily on how you measure</b> — discontinuous "
            "metrics manufacture discontinuous-looking curves."]},

  {"t": "callout", "title": "Why the transformer absorbed everything",
   "kind": "Closing the architecture argument",
   "body": ["<b>Weak inductive bias</b> (Module 06 §4) — so it "
            "imposes nothing wrong on a new domain.",
            "<b>Excellent hardware fit</b> — dense matrix multiplication "
            "is what accelerators are built for (CSCE 735 M08).",
            "<b>Predictable scaling</b> — you can plan a model before "
            "building it.",
            "<b>And one implementation serves every modality</b>, so the "
            "engineering investment compounds instead of fragmenting. "
            "<b>That last point is underrated and may matter most.</b>"]},
 ],
 "takeaways": [
   "A transformer block is attention to mix across positions, a "
   "feed-forward to compute per position, residuals for gradient flow, and "
   "layer norm for batch independence.",
   "The feed-forward holds most of the parameters — attention mixes "
   "and the feed-forward does the computing.",
   "Pre-norm trains far more stably than the original post-norm ordering, "
   "and almost everything modern uses it.",
   "Self-attention is permutation-equivariant, so position must be injected "
   "explicitly or the model sees a set.",
   "The causal mask is the entire difference between an encoder and a "
   "decoder.",
   "Loss falls as a smooth power law in parameters, data, and compute, "
   "which made performance predictable before training.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The block"),
  ("code", """x = x + MultiHeadAttention(LayerNorm(x))   # mix ACROSS positions
x = x + FeedForward(LayerNorm(x))          # process EACH position

FOUR COMPONENTS, FOUR JOBS

1. MULTI-HEAD ATTENTION -- the ONLY operation that moves
   information between positions. Everything else is per-token.

2. FEED-FORWARD -- two linear layers and a nonlinearity, applied
   identically at every position, inner dimension typically 4x
   the model dimension. HOLDS MOST OF THE PARAMETERS.
   Attention mixes; the feed-forward computes.

3. RESIDUAL CONNECTIONS -- the gradient highway (M02 section 3).
   Without them deep transformers do not train.

4. LAYER NORM -- batch-independent, so batch size and sequence
   length do not affect it (M04 section 3).

PRE-NORM (as written) trains far more stably than POST-NORM
(the original paper's order), which needed careful warmup to
train at all."""),
  ("p", "<b>Attention mixes across positions and the feed-forward does the "
        "computation</b> — that division is the clearest way to read "
        "the block, and it explains the parameter distribution: the "
        "feed-forward's 4&times; inner dimension means it holds roughly "
        "two-thirds of a transformer's parameters, which surprises people "
        "who think of the transformer as 'the attention architecture'."),

  ("h1", "2 &nbsp; Heads and positions"),
  ("callout", "Multiple heads attend to different things",
   ["<b>Split the model dimension into h heads, run attention "
    "independently within each, and concatenate the results.</b> The total "
    "compute is essentially unchanged; what changes is the structure.",
    "<b>A single attention distribution can express only one notion of "
    "relevance per position.</b> Several heads can simultaneously attend by "
    "syntactic dependency, by coreference, by relative position, and by "
    "topic — which one softmax cannot.",
    "<b>And interpretable heads genuinely do appear.</b> Previous-token "
    "heads, induction heads that complete a repeated pattern (and which "
    "appear to underlie in-context learning), and heads tracking syntactic "
    "relations have all been identified in trained models.",
    "<b>Though many heads are redundant.</b> <b>A substantial fraction can "
    "be pruned with little loss of performance</b> — a finding "
    "replicated across models and the basis of several compression methods "
    "(Module 13). <b>The architecture is over-provisioned, and that "
    "appears to help training rather than inference</b>, which is a "
    "recurring theme."]),
  ("callout", "Attention has no idea what order things are in",
   ["<b>Self-attention is permutation-equivariant.</b> Shuffle the input "
    "tokens and the outputs shuffle identically — <b>the operation "
    "sees a <i>set</i> of vectors, not a sequence.</b> This is easy to "
    "verify and genuinely surprising the first time.",
    "<b>So positional information must be injected explicitly</b>, or the "
    "model cannot distinguish 'dog bites man' from 'man bites dog'. "
    "Position is not a detail of the architecture; it is a missing "
    "ingredient that must be supplied.",
    "<b>The schemes differ mainly in how they extrapolate beyond the "
    "lengths seen in training</b>, which is the practically important "
    "question — a model trained on 2,000 tokens that must handle "
    "8,000 needs an encoding whose meaning continues to make sense out "
    "there.",
    "<b>RoPE rotates the query and key vectors by an angle proportional "
    "to position</b>, so that the dot product between a query at position i "
    "and a key at position j depends on (i &minus; j) — <b>relative "
    "position emerges from the geometry rather than being added as a "
    "term.</b> <b>It is the current default</b> and extrapolates "
    "considerably better than learned absolute encodings, which have no "
    "value at all for positions never seen in training."]),
  ("table", ["Scheme", "How it works", "Extrapolates?"],
   [["<b>Sinusoidal</b>",
     "Fixed sine and cosine functions at a range of frequencies, added to "
     "the embeddings.",
     "<b>Somewhat.</b> The original choice, and the frequencies were "
     "designed so that relative offsets are expressible as linear "
     "functions."],
    ["<b>Learned absolute</b>",
     "<b>A separate learned embedding vector per position index.</b>",
     "<b>No.</b> There is no embedding for a position never seen, so the "
     "model simply fails past its trained length — which is why "
     "long-context work abandoned it."],
    ["<b>Relative position bias</b>",
     "A learned bias added to the attention score, indexed by the "
     "difference between positions.",
     "Better, and it generalises to unseen distances if the bias is "
     "bucketed."],
    ["<b>RoPE (rotary)</b>",
     "<b>Rotate Q and K by an angle proportional to position</b>, so "
     "relative position falls out of the dot product.",
     "<b>Well, and it is the current default</b> across most large "
     "models."],
    ["<b>ALiBi</b>",
     "<b>Subtract a penalty proportional to distance from the attention "
     "score.</b> No embeddings at all.",
     "<b>Very well, and it is trivially simple</b> — a striking "
     "ratio of effectiveness to complexity."]],
   [0.18, 0.40, 0.42]),

  ("break",),
  ("h1", "3 &nbsp; Three configurations"),
  ("table", ["Configuration", "Attention pattern", "Used for"],
   [["<b>Encoder only</b>",
     "<b>Bidirectional</b> — every position attends to every other, "
     "past and future.",
     "<b>Classification, sequence labelling, and embeddings.</b> BERT and "
     "its descendants. Cannot generate, because every position sees the "
     "answer."],
    ["<b>Decoder only</b>",
     "<b>Causal</b> — masked so that each position attends only to "
     "itself and earlier positions.",
     "<b>Generation, and essentially all modern large language "
     "models.</b> The mask lets every position be trained as a prediction "
     "target simultaneously, which is enormously efficient."],
    ["<b>Encoder–decoder</b>",
     "Bidirectional encoder; causal decoder that additionally "
     "cross-attends to the encoder output.",
     "<b>Translation and summarisation</b>, where the input and output are "
     "distinct sequences. T5, and the original transformer."]],
   [0.20, 0.36, 0.44]),
  ("p", "<b>The causal mask is the entire difference between the first "
        "two</b> — a single upper-triangular mask applied to the "
        "attention scores before the softmax. <b>That such a small change "
        "produces models with such different characters and uses is worth "
        "sitting with</b>, and it is a good illustration of how much of an "
        "architecture's behaviour comes from the training objective rather "
        "than the parameter arrangement."),

  ("h1", "4 &nbsp; Scaling"),
  ("callout", "Scaling laws are smooth power laws, and they held",
   ["<b>Loss falls as a power law in the number of parameters, the quantity "
    "of data, and the compute budget</b> — over many orders of "
    "magnitude, with remarkably little scatter around the fitted line.",
    "<b>So performance became <i>predictable before training</i></b>, "
    "which changed the character of the work: a laboratory could fit the "
    "curve on small models, extrapolate, and commit a large budget with a "
    "forecast rather than a hope. <b>Model development became a budgeting "
    "exercise.</b>",
    "<b>Chinchilla corrected the ratio.</b> The earlier large models were "
    "badly under-trained on data — too many parameters for the number "
    "of tokens they saw — and <b>parameters and training tokens should "
    "scale together</b>, at roughly twenty tokens per parameter for "
    "compute-optimal training. A smaller model trained on more data beat a "
    "larger one trained on less, at equal compute.",
    "<b>And the laws describe the <i>loss</i>, not capability.</b> "
    "<b>Whether a specific ability appears smoothly or suddenly depends "
    "heavily on how it is measured</b> — a metric that is "
    "discontinuous (exact string match, multiple-choice accuracy) "
    "manufactures a discontinuous-looking curve from an underlying smooth "
    "improvement. <b>Several reported 'emergent abilities' turn out to be "
    "artifacts of the metric</b>, which is a measurement lesson "
    "(CSCE 633 Module 12) rather than a fact about models."]),
  ("callout", "Why the transformer absorbed everything",
   ["<b>A weak inductive bias</b> (Module 06 &sect;4) — so applying "
    "it to a new modality imposes nothing <i>wrong</i>, which is the "
    "failure mode of a strong prior in the wrong place (Module 01 "
    "&sect;2).",
    "<b>An excellent hardware fit.</b> The computation is dominated by "
    "large dense matrix multiplications, which is precisely what GPUs and "
    "accelerators are built for (CSCE 735 Module 08) — and unlike "
    "recurrence, it parallelises across the sequence.",
    "<b>Predictable scaling</b> — you can plan and budget a model "
    "before building it, which no previous architecture offered.",
    "<b>And one implementation serves every modality.</b> <b>The "
    "engineering investment compounds rather than fragmenting</b>: every "
    "kernel optimisation, every distributed training improvement, every "
    "inference trick benefits text, vision, audio, and protein models "
    "simultaneously. <b>That last point is underrated and may matter "
    "most</b> — architectural convergence meant the entire field's "
    "systems work pointed in one direction, and the compounding has been "
    "substantial."]),
 ],
 "resources": [
   ("Vaswani et al. &mdash; Attention Is All You Need (free)",
    "https://arxiv.org/abs/1706.03762",
    "The original. Short, and the ablation table in section 6 is where the "
    "design justifications are."),
   ("Karpathy &mdash; nanoGPT and 'Let's build GPT' (free)",
    "https://github.com/karpathy/nanoGPT",
    "<b>A complete, readable, trainable implementation.</b> Read it "
    "alongside &sect;1 — it is about 300 lines."),
   ("Hoffmann et al. &mdash; Training Compute-Optimal Language Models "
    "(Chinchilla) (free)",
    "https://arxiv.org/abs/2203.15556",
    "<b>The &sect;4 correction</b>, with the parameter-to-token ratio "
    "derived from experiments."),
   ("Schaeffer, Miranda & Koyejo &mdash; Are Emergent Abilities of Large "
    "Language Models a Mirage? (free)",
    "https://arxiv.org/abs/2304.15004",
    "<b>The metric argument of &sect;4</b> — a careful demonstration "
    "that discontinuous metrics manufacture discontinuous curves."),
 ],
 "exercises": [
   "<b>Implement a transformer block from scratch</b> and train a small "
   "language model on a text corpus.",
   "<b>Count the parameters in attention and in the feed-forward</b> and "
   "report the ratio.",
   "<b>Compare pre-norm against post-norm</b> at twelve layers, with and "
   "without warmup.",
   "<b>Demonstrate permutation equivariance</b>: shuffle the input and "
   "show the outputs shuffle identically with positional encoding removed.",
   "Implement sinusoidal, learned, and rotary positional encodings and "
   "<b>compare extrapolation beyond the trained length</b>.",
   "<b>Visualise attention patterns per head</b> and try to characterise "
   "what each attends to.",
   "<b>Prune heads one at a time</b> and measure the loss increase for "
   "each. Report how many are removable.",
   "Convert a decoder to an encoder by removing the causal mask and "
   "observe what breaks.",
   "<b>Fit a scaling law</b> on your own small models across three sizes "
   "and extrapolate to a fourth. Then train it and check.",
   "Take a metric that is discontinuous and one that is smooth, and "
   "<b>plot the same models under both</b>.",
 ],
 "selfcheck": [
   "Name the four components of a transformer block and the job of each.",
   "Which component holds most of the parameters?",
   "What is the difference between pre-norm and post-norm, and which "
   "wins?",
   "Why use multiple heads rather than one?",
   "Why is positional encoding necessary at all?",
   "Compare five positional schemes on extrapolation.",
   "Distinguish encoder, decoder, and encoder–decoder, and say what "
   "the difference actually is.",
   "State the scaling laws and what Chinchilla corrected.",
   "Give four reasons the transformer spread across domains.",
 ],
},

]
