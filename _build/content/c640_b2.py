# -*- coding: utf-8 -*-
"""CSCE 640 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "States and Measurement",
 "subtitle": "What a qubit holds, and what you are allowed to see.",
 "question": "Why can you not just read the amplitudes?",
 "outcomes": [
     "Write and manipulate single- and multi-qubit states.",
     "Explain the measurement rule and its consequences.",
     "Explain entanglement without mysticism.",
     "State the no-cloning result and why it matters.",
     "Write a state vector simulator.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The state",
   "blurb": "And the notation this course uses."},

  {"t": "eq", "kicker": "Notation", "title": "A qubit, and n of them",
   "eqs": [
     ("|psi> = a|0> + b|1>,   with |a|² + |b|² = 1",
      "A single qubit: two complex amplitudes, normalised. "
      "Not a probability pair — a and b may be negative or "
      "complex, and that is the point."),
     ("n qubits:  |psi> = Σ a_x |x>  over all x in {0,1}ⁿ",
      "2 to the n amplitudes, indexed by the classical bit strings. "
      "The state space is the tensor product of n copies, not n "
      "copies of a two-state space."),
     ("global phase: e^(iθ)|psi> is the same state as |psi>",
      "Unobservable, always. Relative phase between terms is "
      "observable and is where everything happens."),
   ],
   "caption": "<b>Relative phase is observable and global phase is "
              "not</b> — which is the distinction the whole subject "
              "turns on.",
   "note": "This course writes kets as |0> in ASCII throughout, for "
           "typographic reasons."},

  {"t": "callout", "title": "A superposition is not a probability distribution, and the difference is the negative numbers",
   "kind": "The distinction to get right before anything else",
   "body": ["<b>A probabilistic bit is 0 with probability p and 1 "
            "with probability 1 − p</b> — <b>and probabilities "
            "cannot cancel</b>, because they are "
            "non-negative.",
            "<b>A qubit's amplitudes can be negative or "
            "complex</b> — <b>so two paths to the same outcome can "
            "sum to zero</b>, which is the resource a randomised "
            "algorithm does not have "
            "(CSCE 658).",
            "<b>Which is why the right comparison is not 'quantum is "
            "random' but 'quantum is random with "
            "cancellation'</b> — and <b>the cancellation is the "
            "entire advantage</b> (Module 04).",
            "<b>And it is why a classical simulation is "
            "expensive</b>: <b>you cannot sample your way through "
            "it</b>, because the amplitudes that matter are the ones "
            "that will later cancel."]},

  {"t": "section", "label": "Part 2", "title": "Measurement",
   "blurb": "The rule, and the three things it costs you."},

  {"t": "bullets", "kicker": "Measurement", "title": "The rule, and what follows from it",
   "items": [
     "<b>Measuring in the computational basis returns x with "
     "probability |a_x|²</b>, and <b>leaves the state as |x></b> "
     "— everything else is gone.",
     "",
     "<b>So you get n bits per run, from 2 to the n "
     "amplitudes</b> — <b>which is the fundamental bottleneck of "
     "the whole subject</b>, and the reason algorithms must concentrate "
     "amplitude before measuring.",
     "",
     "<b>And the phases are invisible to measurement</b> — "
     "<b>|a_x|² discards them</b> — so <b>phase has to be "
     "converted into amplitude by interference first</b>, which is "
     "what every algorithm in this course "
     "does.",
     "",
     "<b>Measurement is irreversible</b>, unlike every other "
     "operation — which is why it comes last, and why intermediate "
     "measurement is a design decision rather than a "
     "convenience.",
     "",
     "<b>And repeating does not help directly</b>: <b>each run "
     "samples the same distribution</b>, so you learn the "
     "distribution, not the state.",
   ],
   "footnote": "<b>n bits out of 2 to the n amplitudes</b> — the "
               "whole art of quantum algorithm design is making those n "
               "bits worth having."},

  {"t": "section", "label": "Part 3", "title": "Entanglement",
   "blurb": "Which is a statement about factorisation."},

  {"t": "eq", "kicker": "Entanglement", "title": "The definition, which is unmysterious",
   "eqs": [
     ("product:     (|0> + |1>)(|0> + |1>)/2 = (|00>+|01>+|10>+|11>)/2",
      "A state that factors into a state per qubit. Measuring one "
      "tells you nothing about the other."),
     ("entangled:   (|00> + |11>)/√2",
      "Does not factor. Measuring the first qubit determines the "
      "second — and that is the whole content of the term."),
     ("test:  does the 2ⁿ-vector factor as a tensor product?",
      "If not, entangled. It is a linear-algebra property of the "
      "vector, not a physical influence travelling anywhere."),
   ],
   "caption": "<b>Entangled means the state vector does not "
              "factor</b> — it is a property of the vector, not a "
              "signal between qubits.",
   "note": "Defining entanglement as non-factorisability removes "
           "essentially all the mystery."},

  {"t": "callout", "title": "And no-cloning, which is a one-line consequence with large effects",
   "kind": "Why you cannot copy a state to look at it twice",
   "body": ["<b>There is no unitary that maps |psi>|0> to "
            "|psi>|psi> for every |psi></b> — <b>the proof is two "
            "lines from linearity</b>, and it is one of the few results "
            "in the subject you can derive on sight.",
            "<b>Which closes the obvious workaround to "
            "Part 2</b>: <b>you cannot copy the state a "
            "thousand times and measure each copy differently</b> to "
            "read the amplitudes out.",
            "<b>And it is what makes quantum key distribution "
            "possible</b> — <b>an eavesdropper cannot copy the "
            "channel</b> — which is the one quantum technology that is "
            "deployed rather than projected.",
            "<b>Plus it constrains error correction "
            "severely</b> — <b>the classical trick of storing three "
            "copies is unavailable</b>, which is why "
            "Module 10's codes are cleverer than "
            "repetition."]},

  {"t": "section", "label": "Part 4", "title": "Write the simulator",
   "blurb": "Which is forty lines and worth every one."},

  {"t": "code", "kicker": "Simulator", "title": "The whole thing, in outline",
   "lang": "python", "code": """
import numpy as np

# state: complex vector of length 2**n, index = bit string
def zero_state(n):
    v = np.zeros(2**n, dtype=complex); v[0] = 1.0
    return v

# apply a 2x2 gate U to qubit q of an n-qubit state
def apply1(v, U, q, n):
    v = v.reshape([2]*n)
    v = np.moveaxis(v, q, 0)
    v = np.tensordot(U, v, axes=([1], [0]))
    return np.moveaxis(v, 0, q).reshape(2**n)

# measure everything, once
def measure(v, rng):
    p = np.abs(v)**2
    return rng.choice(len(v), p=p / p.sum())
""",
   "caption": "<b>Controlled gates are the same idea with an index "
              "mask</b>, and that is the entire simulator — the "
              "amplitudes stop being abstract once you have written "
              "this.",
   "note": "Project 1 asks for exactly this, written rather than "
           "imported."},

  {"t": "callout", "title": "And the exponential cost is the point, not a limitation of your code",
   "kind": "Closing",
   "body": ["<b>The vector has 2 to the n entries, so 30 qubits is "
            "about 16 gigabytes in double-precision "
            "complex</b> — <b>which is why a laptop stops at around "
            "25 to 30.</b>",
            "<b>And that cost is exactly the reason the subject "
            "exists</b> — <b>Feynman's observation was that "
            "simulating quantum systems classically appears to be "
            "exponentially hard</b> (Module 09).",
            "<b>So your simulator's limit is informative rather than "
            "annoying</b>: <b>it is the same wall that makes quantum "
            "simulation worth doing on a quantum "
            "device.</b>",
            "<b>Though note the honest "
            "qualification</b> — <b>special structure (low "
            "entanglement, Clifford gates) simulates "
            "efficiently</b>, which Module 13 §3 shows is how "
            "several advantage claims got reduced."]},
 ],
 "takeaways": [
   "Relative phase is observable and global phase is not, which is the "
   "distinction the whole subject turns on.",
   "A superposition is not a probability distribution; the difference is "
   "that amplitudes can cancel.",
   "You get n bits per run out of 2 to the n amplitudes, which is the "
   "fundamental bottleneck of the subject.",
   "Phase is invisible to measurement, so it has to be converted into "
   "amplitude by interference first.",
   "Entangled means the state vector does not factor — a property of "
   "the vector, not a signal between qubits.",
   "No-cloning follows from linearity in two lines, and it rules out both "
   "reading amplitudes by copying and repetition-based error correction.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The state"),
  ("eq", "|psi&gt; = a|0&gt; + b|1&gt;,&nbsp;&nbsp; with "
         "|a|<super>2</super> + |b|<super>2</super> = 1"),
  ("ul", ["<b>A single qubit is two complex amplitudes, "
          "normalised</b> — and <b>it is not a probability "
          "pair</b>: <b>a and b may be negative or complex, and that is "
          "the entire point</b> (see the callout).",
          "<b>For n qubits, |psi&gt; = &Sigma; a<sub>x</sub> "
          "|x&gt;</b> over all x in {0,1}<super>n</super> — "
          "<b>2<sup>n</sup> amplitudes indexed by the classical bit "
          "strings</b>, and <b>the state space is the tensor product of "
          "n two-dimensional spaces</b> rather than n copies of one.",
          "<b>A global phase is unobservable:</b> "
          "<b>e<super>i&theta;</super>|psi&gt; is the same physical "
          "state as |psi&gt;</b>, always — <b>while the relative "
          "phase between terms is observable and is where everything "
          "happens</b> (Module 04 &sect;1).",
          "<b>This course writes kets as |0&gt; in ASCII "
          "throughout</b>, for typographic reasons: the conventional "
          "angle-bracket glyphs do not render reliably in the toolchain "
          "that produced these notes, and a visible notation is worth "
          "more than a conventional one."]),
  ("callout", "A superposition is not a probability distribution, and the "
              "difference is the negative numbers",
   ["<b>A probabilistic bit is 0 with probability p and 1 with "
    "probability 1 &minus; p</b> — <b>and probabilities cannot "
    "cancel</b>, because they are non-negative and sum to one.",
    "<b>A qubit's amplitudes can be negative or complex</b> — "
    "<b>so two computational paths arriving at the same outcome can sum "
    "to zero</b>, <b>which is a resource a randomised algorithm simply "
    "does not have</b> (CSCE 658's whole machinery is built without "
    "it).",
    "<b>Which is why the right comparison is not 'quantum is random' "
    "but 'quantum is random with cancellation'</b> — and <b>the "
    "cancellation is the entire advantage</b> (Module 04 states this "
    "as the course's central mechanism).",
    "<b>And it is also why a classical simulation is "
    "expensive</b>: <b>you cannot sample your way through it</b>, "
    "because <b>the amplitudes that matter are precisely the ones that "
    "will later cancel</b> — so a Monte Carlo approach that "
    "follows likely paths misses the interference."]),

  ("h1", "2 &nbsp; Measurement"),
  ("ul", ["<b>Measuring in the computational basis returns the string "
          "x with probability |a<sub>x</sub>|<super>2</super></b>, and "
          "<b>leaves the state as |x&gt;</b> — <b>everything "
          "else is gone irrecoverably.</b>",
          "<b>So you get n bits per run out of 2<sup>n</sup> "
          "amplitudes</b> — <b>which is the fundamental bottleneck "
          "of the whole subject</b>, and <b>the reason every algorithm "
          "must concentrate amplitude onto the answer before "
          "measuring.</b>",
          "<b>And the phases are invisible to measurement</b> "
          "— <b>|a<sub>x</sub>|<super>2</super> discards them "
          "entirely</b> — so <b>phase has to be converted into "
          "amplitude by interference first</b>, which is what every "
          "algorithm in Modules 05 through 08 is doing.",
          "<b>Measurement is irreversible</b>, unlike every other "
          "operation in the model — <b>which is why it comes last, "
          "and why measuring an intermediate qubit is a design decision "
          "with consequences</b> rather than a free diagnostic.",
          "<b>And repeating the whole computation does not help "
          "directly</b>: <b>each run samples the same "
          "distribution</b>, so <b>you learn the distribution, not the "
          "state</b> — and learning a distribution over "
          "2<sup>n</sup> outcomes takes exponentially many samples. "
          "<b>n bits out of 2<sup>n</sup> amplitudes</b>: <b>the whole "
          "art of quantum algorithm design is making those n bits worth "
          "having.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Entanglement"),
  ("eq", "product state:&nbsp; (|0&gt;+|1&gt;)(|0&gt;+|1&gt;)/2 = "
         "(|00&gt;+|01&gt;+|10&gt;+|11&gt;)/2"),
  ("eq", "entangled:&nbsp; (|00&gt; + |11&gt;)/&radic;2"),
  ("ul", ["<b>A product state factors into one state per "
          "qubit</b> — <b>measuring one qubit tells you nothing "
          "about the other</b>, and the description of the whole is just "
          "the descriptions of the parts.",
          "<b>An entangled state does not factor</b> — "
          "<b>measuring the first qubit of (|00&gt;+|11&gt;)/&radic;2 "
          "determines the second</b> — <b>and that correlation is "
          "the whole content of the term.</b>",
          "<b>So the test is: does the 2<sup>n</sup>-dimensional "
          "vector factor as a tensor product?</b> <b>If not, it is "
          "entangled.</b> <b>It is a linear-algebra property of the "
          "vector, not a physical influence travelling between "
          "qubits</b> — and nothing in the formalism moves.",
          "<b>Defining entanglement as non-factorisability removes "
          "essentially all the mystery</b>, and it also makes the "
          "computational role clear: <b>entanglement is how a circuit "
          "builds amplitudes that depend jointly on many qubits</b>, "
          "which is what makes the interference in Module 04 "
          "possible at all."]),
  ("callout", "And no-cloning, which is a one-line consequence with large "
              "effects",
   ["<b>There is no unitary U with U(|psi&gt;|0&gt;) = "
    "|psi&gt;|psi&gt; for every |psi&gt;</b> — <b>and the proof is "
    "two lines from linearity</b>: suppose it works for |0&gt; and for "
    "|1&gt;, then apply it to their superposition and compare. <b>It is "
    "one of the very few results in the subject you can derive on "
    "sight.</b>",
    "<b>Which closes the obvious workaround to &sect;2's "
    "bottleneck</b>: <b>you cannot copy the state a thousand times and "
    "measure each copy in a different basis</b> in order to read the "
    "amplitudes out.",
    "<b>And it is what makes quantum key distribution "
    "possible</b> — <b>an eavesdropper cannot copy the "
    "channel</b> — <b>which is the one quantum technology that is "
    "actually deployed</b> rather than projected, and is worth "
    "distinguishing from quantum computing when people conflate "
    "them.",
    "<b>Plus it constrains error correction severely</b> — "
    "<b>the classical trick of storing three copies and taking a "
    "majority is simply unavailable</b> — <b>which is why "
    "Module 10's codes are cleverer than repetition</b> and why "
    "fault tolerance took a decade to establish."]),

  ("h1", "4 &nbsp; Write the simulator"),
  ("code", """import numpy as np

# state: complex vector of length 2**n, index = bit string
def zero_state(n):
    v = np.zeros(2**n, dtype=complex); v[0] = 1.0
    return v

# apply a 2x2 gate U to qubit q of an n-qubit state
def apply1(v, U, q, n):
    v = v.reshape([2]*n)
    v = np.moveaxis(v, q, 0)
    v = np.tensordot(U, v, axes=([1], [0]))
    return np.moveaxis(v, 0, q).reshape(2**n)

# measure everything, once
def measure(v, rng):
    p = np.abs(v)**2
    return rng.choice(len(v), p=p / p.sum())"""),
  ("p", "<b>Controlled gates are the same idea with an index "
        "mask</b> — apply the gate only to the amplitudes whose "
        "control bit is 1 — <b>and that is the entire "
        "simulator</b>. <b>The amplitudes stop being abstract once you "
        "have written this</b>, which is why <b>Project 1 asks for "
        "exactly this, written rather than imported</b>. Verify it "
        "against a hand calculation on two qubits including an entangled "
        "state, because a simulator that handles product states "
        "correctly and entangled ones incorrectly looks right until it "
        "does not."),
  ("callout", "And the exponential cost is the point, not a limitation of "
              "your code",
   ["<b>The vector has 2<sup>n</sup> entries, so 30 qubits is about "
    "16 gigabytes in double-precision complex</b> — <b>which is why "
    "a laptop stops at around 25 to 30 qubits</b> of fully general "
    "state, and no amount of optimisation changes the exponent.",
    "<b>And that cost is exactly the reason the subject "
    "exists</b> — <b>Feynman's observation was that simulating "
    "quantum systems classically appears to be exponentially hard</b>, "
    "<b>so use a quantum system to do it</b> (Module 09, and "
    "Module 01 &sect;3's first item).",
    "<b>So your simulator's limit is informative rather than "
    "annoying</b>: <b>it is the same wall that makes quantum simulation "
    "worth doing on a quantum device</b>, encountered personally on a "
    "laptop, which is a better way to understand it than reading the "
    "claim.",
    "<b>Though note the honest qualification</b> — <b>states "
    "with special structure simulate efficiently</b>: <b>low "
    "entanglement (tensor-network methods), Clifford-only circuits (the "
    "Gottesman-Knill theorem), and shallow circuits</b> — <b>which "
    "Module 13 &sect;3 shows is precisely how several published "
    "advantage claims were reduced</b> after the fact."]),
 ],
 "resources": [
   ("Nielsen & Chuang, chapters 2 and 4 (library copy)",
    "https://www.cambridge.org/9781107002173",
    "<b>&sect;&sect;1 to 3</b> — the linear algebra and the "
    "measurement postulates, developed carefully."),
   ("Wootters & Zurek &mdash; A single quantum cannot be cloned",
    "https://www.nature.com/articles/299802a0",
    "<b>&sect;3's callout in the original</b> — one page, and the "
    "argument is the one you can reconstruct."),
   ("Watrous's notes, the early lectures (free)",
    "https://cs.uwaterloo.ca/~watrous/QC-notes/",
    "<b>&sect;&sect;1 and 2</b>, rigorous and short — and the "
    "measurement formalism is stated more generally than "
    "Nielsen-Chuang does at first."),
   ("Aaronson &mdash; Multilinear formulas and the Gottesman-Knill "
    "theorem, lecture notes (free)",
    "https://www.scottaaronson.com/qclec.pdf",
    "<b>&sect;4's qualification</b> — which circuit classes simulate "
    "classically, and why that matters for advantage claims."),
 ],
 "exercises": [
   "<b>Write three single-qubit states</b> and verify "
   "normalisation.",
   "<b>Show that a global phase changes no measurement "
   "probability.</b>",
   "<b>Construct two amplitudes that cancel</b>, and say what the "
   "probabilistic analogue would be.",
   "<b>Compute the measurement distribution</b> for a three-qubit "
   "state by hand.",
   "<b>Show that measurement discards relative phase.</b>",
   "<b>Factor three two-qubit states</b>, or show that they do not "
   "factor.",
   "<b>Prove no-cloning</b> from linearity, in your own words.",
   "<b>Write the simulator</b> from Part 4, and verify it on an "
   "entangled state by hand.",
   "<b>Find your simulator's qubit ceiling</b> on your own machine, "
   "and report the memory.",
   "<b>Simulate a Clifford-only circuit</b> and read about why it "
   "could have been done classically in polynomial time.",
 ],
 "selfcheck": [
   "Write a general n-qubit state and count its parameters.",
   "Which phase is observable, and which is not?",
   "Why is a superposition not a probability distribution?",
   "State the measurement rule and three consequences.",
   "How many bits per run, and why does that matter?",
   "Why must phase be converted to amplitude?",
   "Define entanglement, and say what it is not.",
   "Prove no-cloning, and give two of its effects.",
   "What is the memory cost of n qubits, and where is the ceiling?",
   "Name three classically simulable circuit classes.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Gates and Circuits",
 "subtitle": "The operations, and what counts as a cost.",
 "question": "What is the quantum equivalent of a NAND gate?",
 "outcomes": [
     "Use the standard single- and two-qubit gates.",
     "Explain universality and what it does and does not give.",
     "Explain reversibility and the cost of uncomputation.",
     "Build an oracle from a classical function.",
     "Count the resources of a circuit.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The gates",
   "blurb": "A small set, used constantly."},

  {"t": "table", "kicker": "Gates", "title": "The standard set, and what each is for",
   "header": ["Gate", "What it does", "Used for"],
   "widths": [2.0, 4.6, 4.4],
   "rows": [
     ["<b>X, Y, Z</b>", "<b>The Pauli operators; bit flip, phase flip</b>", "<b>Everything; the error basis (M10)</b>"],
     ["<b>H</b>", "<b>Hadamard: basis to superposition and back</b>", "<b>Creating and closing interference</b>"],
     ["<b>S, T</b>", "<b>Phase rotations by π/2 and π/4</b>", "<b>T is the expensive one (M10 §4)</b>"],
     ["<b>R_z(θ)</b>", "<b>Arbitrary phase rotation</b>", "<b>QFT (M07); variational circuits</b>"],
     ["<b>CNOT</b>", "<b>Flip target if control is 1</b>", "<b>Entangling; the two-qubit workhorse</b>"],
     ["<b>Toffoli</b>", "<b>Flip target if both controls are 1</b>", "<b>Classical logic, reversibly (§3)</b>"],
   ],
   "footnote": "<b>H and CNOT and T is a universal set</b>, and <b>T "
               "is by far the most expensive to make "
               "fault-tolerant</b> — so T-count is the resource "
               "metric that actually matters "
               "(Module 10 §4).",
   "note": "T-count, not gate count, is the number to quote."},

  {"t": "callout", "title": "Universality means approximating any unitary, and says nothing about efficiency",
   "kind": "A distinction worth being exact about",
   "body": ["<b>A small gate set can approximate any unitary on n "
            "qubits to any accuracy</b> — <b>which is the "
            "Solovay-Kitaev result</b> and is reassuring about "
            "expressiveness.",
            "<b>And it is silent about cost:</b> <b>almost all "
            "unitaries require exponentially many gates</b>, by a "
            "counting argument — <b>so universality does not mean "
            "'everything is cheap'.</b>",
            "<b>Which is the same structure as classical "
            "universality</b>: <b>NAND is universal and most Boolean "
            "functions still need exponential "
            "circuits</b> (CSCE 637 §02).",
            "<b>So the interesting question is never 'can it be "
            "expressed' but 'with how many gates and what "
            "depth'</b> — and <b>for most unitaries the answer is "
            "'too many', which is why algorithms are rare and "
            "precious.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Reversibility",
   "blurb": "Which is a constraint with a specific cost."},

  {"t": "callout", "title": "Every operation except measurement is reversible, so nothing can be thrown away",
   "kind": "The constraint and its consequence",
   "body": ["<b>A unitary is invertible, so no information is "
            "destroyed</b> — which means <b>a quantum circuit cannot "
            "overwrite a register the way classical code "
            "does.</b>",
            "<b>So intermediate results accumulate as "
            "garbage</b> — <b>and entangled garbage is worse than "
            "useless</b>: <b>it carries which-path information and "
            "therefore destroys the interference you "
            "needed.</b>",
            "<b>Which forces uncomputation:</b> <b>compute, copy "
            "the answer out with a CNOT, then run the computation "
            "backwards to clear the workspace</b> — the Bennett trick, "
            "and it roughly doubles the gate "
            "count.",
            "<b>And that is the real cost of reversibility</b>: "
            "<b>not the gate set, but the obligation to clean "
            "up</b> — which is the commonest source of a quantum "
            "algorithm that does not work."]},

  {"t": "section", "label": "Part 3", "title": "Oracles",
   "blurb": "How a classical function enters a quantum circuit."},

  {"t": "eq", "kicker": "Oracles", "title": "The two forms, and the conversion between them",
   "eqs": [
     ("bit oracle:    |x>|y>  →  |x>|y XOR f(x)>",
      "Reversible, and it is how any classical f is made available. "
      "Built from Toffoli gates mechanically."),
     ("phase oracle:  |x>  →  (−1)^f(x) |x>",
      "Puts the answer in the phase instead. Cleaner for "
      "interference-based algorithms."),
     ("conversion: set y = (|0> − |1>)/√2 in the bit oracle",
      "The target picks up the sign and is left unchanged — the "
      "phase kickback trick, used in Modules 05, 06 and 08."),
   ],
   "caption": "<b>Phase kickback converts a bit oracle into a phase "
              "oracle for free</b> — and it is the single most "
              "reused trick in the subject.",
   "note": "Every algorithm from here on uses phase kickback."},

  {"t": "bullets", "kicker": "Oracles", "title": "And the thing to be careful about",
   "items": [
     "<b>An oracle is a circuit you have to build</b>, not a "
     "free lookup — <b>and its cost counts</b>, which query-count "
     "results deliberately set aside.",
     "",
     "<b>So a query-efficient algorithm is not automatically "
     "time-efficient</b> — <b>and conflating the two is the "
     "commonest error in reading this literature</b> "
     "(Module 05 §4).",
     "",
     "<b>And the oracle must be unitary on <i>all</i> "
     "inputs</b>, including superpositions — <b>which is what "
     "'you may call it but not inspect it' actually means</b> for an "
     "implementation.",
     "",
     "<b>Building one from a classical circuit is "
     "mechanical</b> — Toffoli for AND, X for NOT, CNOT for "
     "copy — <b>plus uncomputation</b> "
     "(Part 2).",
     "",
     "<b>Which means the oracle usually dominates the gate "
     "count</b>, and a published circuit diagram that draws it as a box "
     "is hiding most of the work.",
   ],
   "footnote": "<b>A box labelled U_f in a circuit diagram is hiding "
               "most of the gate count</b> — which is fine for "
               "analysis and misleading for cost "
               "estimates."},

  {"t": "section", "label": "Part 4", "title": "Resources",
   "blurb": "What to count, and in what order."},

  {"t": "code", "kicker": "Counting", "title": "The resource metrics that matter",
   "lang": "text", "code": """
  QUBITS
      logical: what the algorithm needs
      physical: logical x overhead (M10 s4),
                which is 1000x or more

  DEPTH
      the longest path; it sets the wall-clock time
      and must fit inside the coherence time (M10)

  GATE COUNT
      total, and then by type

  T-COUNT  <-- the one that matters
      T gates need magic state distillation, which
      dominates the cost of a fault-tolerant circuit
      Clifford gates (H, S, CNOT, Paulis) are cheap

  QUERY COUNT
      oracle calls only; a theoretical measure that
      ignores the oracle's own cost (section 3)

  AND REPORT ALL FIVE, because a paper that reports
  only the ones that flatter the result is the norm.
""",
   "caption": "<b>T-count dominates the cost of a fault-tolerant "
              "circuit</b>, and Clifford gates are comparatively "
              "free — which is why the metric is unusual."},

  {"t": "callout", "title": "And the circuit model is not the only model, which is worth knowing",
   "kind": "Closing",
   "body": ["<b>Measurement-based, adiabatic, and topological models "
            "are all polynomially equivalent to the circuit "
            "model</b> — <b>so nothing in this course's results "
            "depends on the choice.</b>",
            "<b>But they differ enormously in engineering "
            "difficulty</b>, which is why hardware efforts pick "
            "different ones — and <b>equivalence in theory is not "
            "equivalence in practice.</b>",
            "<b>And analogue or special-purpose devices are a "
            "separate question</b> — <b>a quantum annealer is not a "
            "universal quantum computer</b>, and conflating them has "
            "produced several confusing claims "
            "(Module 13 §3).",
            "<b>So this course uses the circuit model throughout and "
            "names it</b> — <b>because 'a quantum computer did X' "
            "needs the model stated</b> as part of "
            "Module 13's three requirements."]},
 ],
 "takeaways": [
   "H, CNOT, and T form a universal set, and T-count rather than gate count "
   "is the resource metric that matters.",
   "Universality means approximating any unitary and says nothing about "
   "efficiency; almost all unitaries need exponentially many gates.",
   "Everything but measurement is reversible, so intermediate results "
   "accumulate and entangled garbage destroys interference.",
   "Uncomputation — compute, copy out, run backwards — roughly "
   "doubles the gate count and is the real cost of reversibility.",
   "Phase kickback converts a bit oracle into a phase oracle for free and "
   "is the most reused trick in the subject.",
   "A box labelled U_f hides most of the gate count, so a query-efficient "
   "algorithm is not automatically time-efficient.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The gates"),
  ("table", ["Gate", "What it does", "What it is used for"],
   [["<b>X, Y, Z</b>",
     "<b>The Pauli operators: bit flip, bit-and-phase flip, phase "
     "flip.</b>",
     "<b>Everywhere</b> — and they are the error basis for "
     "Module 10, which is why they matter structurally."],
    ["<b>H</b>",
     "<b>Hadamard: maps basis states to even superpositions, and "
     "back.</b>",
     "<b>Creating interference, and closing it</b> — almost every "
     "algorithm opens and closes with a layer of H."],
    ["<b>S, T</b>",
     "<b>Phase rotations by &pi;/2 and &pi;/4.</b>",
     "<b>T is the expensive one</b> (Module 10 &sect;4) and the "
     "reason T-count is the metric."],
    ["<b>R<sub>z</sub>(&theta;)</b>",
     "<b>Arbitrary rotation about z; a relative phase "
     "e<super>i&theta;</super>.</b>",
     "<b>The quantum Fourier transform</b> (Module 07) <b>and "
     "variational circuits</b> (Module 11)."],
    ["<b>CNOT</b>",
     "<b>Flip the target if the control is 1.</b>",
     "<b>The entangling workhorse</b>, and the two-qubit gate most "
     "hardware implements natively."],
    ["<b>Toffoli (CCNOT)</b>",
     "<b>Flip the target if both controls are 1.</b>",
     "<b>Classical logic done reversibly</b> (&sect;3) — it is "
     "reversible AND."]],
   [0.14, 0.44, 0.42]),
  ("p", "<b>H and CNOT and T is a universal set</b>, and <b>T is by "
        "far the most expensive gate to implement "
        "fault-tolerantly</b> — it cannot be done transversally in "
        "the usual codes and requires magic state distillation — "
        "<b>so T-count is the resource metric that actually "
        "matters</b> (Module 10 &sect;4). <b>T-count, not gate count, "
        "is the number to quote</b>, and a resource estimate that reports "
        "only total gates is not telling you the cost."),
  ("callout", "Universality means approximating any unitary, and says "
              "nothing about efficiency",
   ["<b>A small finite gate set can approximate any unitary on n "
    "qubits to any desired accuracy</b> — <b>which is the "
    "Solovay-Kitaev result</b>, and it is genuinely reassuring about the "
    "model's expressiveness.",
    "<b>And it is entirely silent about cost:</b> <b>almost all "
    "unitaries require exponentially many gates</b>, by a straightforward "
    "counting argument (there are far more unitaries than short "
    "circuits) — <b>so universality does not mean 'everything is "
    "cheap'</b> and is sometimes read as though it did.",
    "<b>Which is exactly the same structure as classical "
    "universality</b>: <b>NAND is universal and most Boolean functions "
    "still require exponential-size circuits</b> (CSCE 637 "
    "Module 02's counting argument, which transfers "
    "unchanged).",
    "<b>So the interesting question is never 'can it be expressed' "
    "but 'with how many gates, and at what depth'</b> — and <b>for "
    "the overwhelming majority of unitaries the answer is 'far too "
    "many', which is why useful quantum algorithms are rare and "
    "precious</b> rather than waiting to be found in bulk."]),

  ("h1", "2 &nbsp; Reversibility"),
  ("callout", "Every operation except measurement is reversible, so nothing "
              "can be thrown away",
   ["<b>A unitary is invertible, so no information is destroyed by "
    "any gate</b> — which means <b>a quantum circuit cannot "
    "overwrite a register the way ordinary classical code does</b>, and "
    "cannot discard a temporary.",
    "<b>So intermediate results accumulate as garbage in ancillary "
    "qubits</b> — and <b>entangled garbage is considerably worse "
    "than merely wasteful</b>: <b>it carries which-path information, and "
    "therefore destroys the very interference the algorithm needed</b> "
    "(Module 04 &sect;3's decoherence argument, in miniature and "
    "self-inflicted).",
    "<b>Which forces uncomputation:</b> <b>compute the result, copy "
    "the answer out into a fresh register with a CNOT, then run the "
    "entire computation backwards to clear the workspace</b> — the "
    "Bennett trick — <b>and it roughly doubles the gate count.</b>",
    "<b>And that is the real cost of reversibility</b>: <b>not the "
    "restricted gate set, which costs little, but the obligation to "
    "clean up</b> — <b>which is the commonest single source of a "
    "hand-derived quantum algorithm that does not work</b>, and the "
    "first thing to check when a simulation gives the wrong "
    "distribution."]),

  ("break",),
  ("h1", "3 &nbsp; Oracles"),
  ("eq", "bit oracle:&nbsp; |x&gt;|y&gt; &rarr; |x&gt;|y &oplus; "
         "f(x)&gt;"),
  ("eq", "phase oracle:&nbsp; |x&gt; &rarr; "
         "(&minus;1)<super>f(x)</super> |x&gt;"),
  ("ul", ["<b>The bit oracle is reversible, and it is how any "
          "classical function f is made available to a quantum "
          "circuit</b> — <b>built from Toffoli, CNOT, and X gates "
          "mechanically</b> from any classical circuit for f.",
          "<b>The phase oracle puts the answer into the phase "
          "instead</b>, leaving the input register's basis states "
          "alone — <b>which is much cleaner for every "
          "interference-based algorithm</b> in this course.",
          "<b>And the conversion is free:</b> <b>set the target "
          "register to (|0&gt; &minus; |1&gt;)/&radic;2 before calling "
          "the bit oracle</b>, and <b>the target picks up the sign "
          "(&minus;1)<super>f(x)</super> while being left "
          "unchanged</b> — <b>the phase kickback trick</b>.",
          "<b>Phase kickback converts a bit oracle into a phase "
          "oracle for free</b>, and <b>it is the single most reused "
          "trick in the subject</b>: <b>every algorithm from "
          "Module 05 onwards uses it</b>, usually without "
          "comment.",
          "<b>Which is worth deriving once by hand</b>, because it "
          "then stops being a step to memorise and becomes the obvious "
          "thing to do."]),
  ("ul", ["<b>An oracle is a circuit you have to build</b>, not a "
          "free lookup table — <b>and its cost counts toward your "
          "total</b>, <b>which query-count results deliberately set "
          "aside</b> in order to prove clean lower bounds.",
          "<b>So a query-efficient algorithm is not automatically a "
          "time-efficient one</b> — <b>and conflating the two is "
          "the commonest error in reading this literature</b> "
          "(Module 05 &sect;4 makes this precise).",
          "<b>And the oracle must be unitary on <i>all</i> inputs, "
          "including superpositions</b> — <b>which is what 'you may "
          "call it but not inspect it' actually means for an "
          "implementation</b>: your simulator's oracle must act "
          "correctly on a superposed input, which is easy to get wrong "
          "by writing it as a classical if-statement.",
          "<b>Building one from a classical circuit is "
          "mechanical</b> — Toffoli for AND, X for NOT, CNOT for "
          "fan-out — <b>plus uncomputation of the intermediate "
          "wires</b> (&sect;2).",
          "<b>Which means the oracle usually dominates the gate "
          "count</b> of the whole algorithm. <b>A box labelled "
          "U<sub>f</sub> in a circuit diagram is hiding most of the gate "
          "count</b> — <b>which is fine for complexity analysis and "
          "actively misleading for a cost estimate.</b>"]),

  ("h1", "4 &nbsp; Resources"),
  ("code", """QUBITS
    logical: what the algorithm needs
    physical: logical x overhead (Module 10 s4),
              which is 1000x or more

DEPTH
    the longest path; it sets the wall-clock time
    and must fit inside the coherence time (M10)

GATE COUNT
    total, and then broken down by type

T-COUNT  <-- the one that matters
    T gates need magic state distillation, which
    dominates the cost of a fault-tolerant circuit
    Clifford gates (H, S, CNOT, Paulis) are cheap

QUERY COUNT
    oracle calls only; a theoretical measure that
    ignores the oracle's own cost (section 3)

AND REPORT ALL FIVE, because a paper that reports
only the ones that flatter the result is the norm."""),
  ("callout", "And the circuit model is not the only model, which is worth "
              "knowing",
   ["<b>Measurement-based, adiabatic, and topological models are all "
    "polynomially equivalent to the circuit model</b> — <b>so "
    "nothing in this course's results depends on the choice</b>, and a "
    "result proved in one transfers.",
    "<b>But they differ enormously in engineering difficulty</b>, "
    "which is precisely why different hardware efforts pick different "
    "ones — and <b>equivalence in theory is not equivalence in "
    "practice</b>, which is a general lesson this program keeps meeting "
    "(CSCE 678 Module 03's consistency models, for one).",
    "<b>And analogue or special-purpose devices are a separate "
    "question entirely</b> — <b>a quantum annealer is not a "
    "universal quantum computer</b>, and does not run the algorithms in "
    "this course — <b>and conflating the two has produced several "
    "confusing public claims</b> (Module 13 &sect;3).",
    "<b>So this course uses the circuit model throughout and names "
    "it</b> — <b>because 'a quantum computer did X' needs the model "
    "stated</b> as part of <b>Module 13's three requirements</b>: the "
    "problem, the baseline, and the machine."]),
 ],
 "resources": [
   ("Nielsen & Chuang, chapter 4 (library copy)",
    "https://www.cambridge.org/9781107002173",
    "<b>&sect;&sect;1 and 2</b> — the gate set, universality, and "
    "the circuit constructions, with the Solovay-Kitaev discussion."),
   ("Bennett &mdash; Logical reversibility of computation",
    "https://ieeexplore.ieee.org/document/5391327",
    "<b>&sect;2's uncomputation trick in the original</b>, and it predates "
    "quantum computing entirely."),
   ("Amy et al. &mdash; T-count optimisation (free preprints)",
    "https://arxiv.org/abs/1206.0758",
    "<b>&sect;4's metric</b> — why T-count is the target, and how it "
    "is reduced in practice."),
   ("The Qiskit transpiler documentation (free)",
    "https://docs.quantum.ibm.com/",
    "<b>&sect;4 concretely</b> — run your circuit through it and watch "
    "the gate count grow as connectivity constraints are "
    "applied."),
 ],
 "exercises": [
   "<b>Write the matrices</b> for X, Z, H, S, T, and CNOT.",
   "<b>Verify H H = I</b> and that H X H = Z.",
   "<b>Count the unitaries versus the short circuits</b>, and state "
   "the consequence.",
   "<b>Build a reversible AND</b> from a Toffoli, and say what the "
   "ancilla costs.",
   "<b>Compute something, copy it out, and uncompute</b>, in your "
   "simulator.",
   "<b>Then skip the uncomputation</b> and observe the interference "
   "fail.",
   "<b>Derive phase kickback</b> by hand.",
   "<b>Build a bit oracle</b> for a three-bit Boolean function, from "
   "gates.",
   "<b>Count its gates</b>, and compare to the single box in the "
   "diagram.",
   "<b>Report all five resource metrics</b> for one circuit you have "
   "built.",
 ],
 "selfcheck": [
   "Name six standard gates and what each is for.",
   "Give a universal set, and say which gate is expensive and why.",
   "What does universality give you, and what does it not?",
   "What is the classical analogue of that distinction?",
   "Why can nothing be thrown away, and what is entangled garbage?",
   "Describe uncomputation and its cost.",
   "Give both oracle forms and the conversion.",
   "Why is a query-efficient algorithm not necessarily fast?",
   "Name the five resource metrics, and which dominates.",
   "Why does the model have to be named in a claim?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Interference",
 "subtitle": "The one resource, isolated.",
 "question": "Where does the speedup actually come from?",
 "outcomes": [
     "Explain interference as the source of every advantage.",
     "Trace the amplitude cancellation in a concrete circuit.",
     "Explain why which-path information destroys it.",
     "Relate decoherence to the loss of interference.",
     "Use the cancellation requirement as a design principle.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The mechanism",
   "blurb": "Stated in one sentence, then traced."},

  {"t": "callout", "title": "A quantum algorithm arranges many computational paths to the same outcome, with phases chosen so the wrong answers cancel",
   "kind": "The course's central mechanism",
   "body": ["<b>Each basis state's final amplitude is a sum over "
            "every path the circuit provides to it</b> — which is "
            "literally what matrix multiplication "
            "computes.",
            "<b>And the terms of that sum carry phases</b>, so "
            "<b>they can add constructively or destroy each "
            "other</b> — which a sum of probabilities cannot do "
            "(Module 02 §1).",
            "<b>So the design problem is: choose a circuit whose "
            "path phases make the unwanted outcomes' sums "
            "vanish</b> — <b>and that is all any quantum algorithm "
            "does.</b>",
            "<b>Which explains the shortness of "
            "Module 01 §3's list</b> — <b>you need problem "
            "structure that lets you engineer the phases</b>, and most "
            "problems do not have any."]},

  {"t": "eq", "kicker": "Trace", "title": "Two qubits, worked: where the cancellation happens",
   "eqs": [
     ("H|0> = (|0> + |1>)/√2;   H|1> = (|0> − |1>)/√2",
      "The minus sign is the whole resource. H is the gate that "
      "turns a basis state into paths, and a path pair back into a "
      "basis state."),
     ("H H |0> = |0>",
      "Two paths reach |1>: via |0> with sign +, and via |1> with "
      "sign −. They cancel exactly. The |0> paths reinforce."),
     ("H X H |0> = −|1>",
      "Insert anything that flips the relative sign and the "
      "cancellation moves. This is the whole trick, at the smallest "
      "possible scale."),
   ],
   "caption": "<b>H opens the interference and H closes it</b>, and "
              "whatever happens in between decides which outcome "
              "survives.",
   "note": "Trace this by hand; it is the smallest complete example "
           "of the mechanism."},

  {"t": "section", "label": "Part 2", "title": "Which-path information",
   "blurb": "Which destroys interference, every time."},

  {"t": "callout", "title": "If anything records which path was taken, the paths no longer interfere",
   "kind": "The constraint that explains both garbage and noise",
   "body": ["<b>Interference requires that the paths be "
            "indistinguishable at the point where they "
            "meet</b> — <b>if a leftover qubit is correlated with "
            "which path ran, the amplitudes add as probabilities "
            "instead.</b>",
            "<b>Which is exactly Module 03 §2's "
            "garbage problem</b> — <b>the uncomputed ancilla is a "
            "which-path record</b>, and leaving it is why the algorithm "
            "silently stops working.",
            "<b>And it is also what decoherence "
            "is</b> — <b>the environment records which path ran, "
            "accidentally</b> — so <b>noise and uncleaned garbage are "
            "the same failure</b> with different "
            "causes.",
            "<b>So the unifying design rule is: nothing outside the "
            "computation may learn which path was taken</b>, until the "
            "final measurement — <b>which is a single statement "
            "covering Module 03 §2 and all of "
            "Module 10.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Decoherence",
   "blurb": "The engineering consequence of Part 2."},

  {"t": "bullets", "kicker": "Decoherence", "title": "Why hardware is hard, in one argument",
   "items": [
     "<b>Any coupling to the environment leaks which-path "
     "information</b> — <b>so the qubit must be isolated</b>, and "
     "isolation conflicts directly with being able to control "
     "it.",
     "",
     "<b>Which is the central engineering tension:</b> "
     "<b>controllable means coupled, and coupled means "
     "decohering</b> — and every hardware platform is a position "
     "on that trade.",
     "",
     "<b>So coherence time bounds circuit depth</b> — "
     "<b>the computation must finish before the information "
     "leaks</b> (Module 03 §4's depth "
     "metric).",
     "",
     "<b>And it is not a matter of better "
     "shielding</b> — <b>the required isolation grows with the "
     "number of qubits and the depth</b>, which is why error "
     "correction rather than isolation is the "
     "answer (Module 10).",
     "",
     "<b>Which makes Module 10's threshold theorem the "
     "result the whole field depends on</b>: it says the problem is "
     "solvable in principle.",
   ],
   "footnote": "<b>Controllable means coupled, and coupled means "
               "decohering</b> — which is why this is hard in a way "
               "better engineering alone does not "
               "fix."},

  {"t": "section", "label": "Part 4", "title": "As a design principle",
   "blurb": "What to ask when designing or reading an algorithm."},

  {"t": "callout", "title": "The question to ask of any quantum algorithm is: what cancels, and why",
   "kind": "Closing",
   "body": ["<b>For Deutsch-Jozsa, the constant case's paths all "
            "reinforce on one outcome</b> "
            "(Module 05 §2) — <b>the cancellation does "
            "the deciding.</b>",
            "<b>For Grover, each iteration rotates amplitude toward "
            "the marked state</b> (Module 06 §2) — <b>and "
            "continues past it if you overshoot</b>, which is the "
            "clearest demonstration that this is "
            "geometry.",
            "<b>For Shor, the Fourier transform makes amplitudes at "
            "non-multiples of the period cancel</b> "
            "(Modules 07 and 08) — <b>which is the "
            "one case where the structure is "
            "obvious.</b>",
            "<b>So if you cannot say what cancels, you have not "
            "understood the algorithm</b> — <b>and if a proposed "
            "algorithm has no cancellation story, it has no "
            "advantage</b>, which is a useful filter on "
            "claims."]},
 ],
 "takeaways": [
   "A quantum algorithm arranges many paths to the same outcome with phases "
   "chosen so that the wrong answers cancel — and that is all any of "
   "them does.",
   "H opens the interference and H closes it, and whatever happens between "
   "decides which outcome survives.",
   "If anything records which path was taken, the paths no longer "
   "interfere.",
   "Uncleaned garbage and environmental decoherence are the same failure "
   "with different causes.",
   "Controllable means coupled and coupled means decohering, which is why "
   "better shielding alone does not fix the hardware problem.",
   "If you cannot say what cancels, you have not understood the algorithm; "
   "and no cancellation story means no advantage.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The mechanism"),
  ("callout", "A quantum algorithm arranges many computational paths to the "
              "same outcome, with phases chosen so the wrong answers cancel",
   ["<b>Each basis state's final amplitude is a sum over every path "
    "the circuit provides to reach it</b> — <b>which is literally "
    "what the matrix multiplication computes</b>, and is worth seeing as "
    "a path sum rather than as a vector update.",
    "<b>And the terms of that sum carry phases</b>, so <b>they can "
    "add constructively or destroy one another</b> — <b>which a sum "
    "of probabilities cannot do</b>, because probabilities are "
    "non-negative (Module 02 &sect;1).",
    "<b>So the entire design problem is: choose a circuit whose path "
    "phases make the unwanted outcomes' sums vanish</b>, leaving the "
    "amplitude concentrated where you want to measure — <b>and that "
    "is all any quantum algorithm does.</b>",
    "<b>Which immediately explains the shortness of Module 01 "
    "&sect;3's list</b> — <b>you need problem structure that lets "
    "you engineer the phases</b>, <b>and most problems do not have "
    "any</b>: for an unstructured problem there is nothing to build the "
    "cancellation out of (Module 06 &sect;4's lower bound is this "
    "intuition made rigorous)."]),
  ("eq", "H|0&gt; = (|0&gt; + |1&gt;)/&radic;2;&nbsp;&nbsp; "
         "H|1&gt; = (|0&gt; &minus; |1&gt;)/&radic;2"),
  ("ul", ["<b>The minus sign is the whole resource.</b> <b>H is the "
          "gate that turns a basis state into a pair of paths, and turns "
          "a pair of paths back into a basis state</b> — which is "
          "why nearly every algorithm opens and closes with a layer of "
          "it.",
          "<b>H H |0&gt; = |0&gt;</b>: <b>two paths reach "
          "|1&gt;</b> — via the |0&gt; branch with sign +, and via "
          "the |1&gt; branch with sign &minus; — <b>and they cancel "
          "exactly</b>, while <b>the two paths to |0&gt; "
          "reinforce.</b>",
          "<b>H X H |0&gt; = &minus;|1&gt;</b>: <b>insert anything "
          "that flips the relative sign between the paths and the "
          "cancellation moves to the other outcome</b> — <b>which "
          "is the whole trick of the subject, at the smallest possible "
          "scale.</b>",
          "<b>Trace this by hand</b>; <b>it is the smallest complete "
          "example of the mechanism</b>, and every algorithm in "
          "Modules 05 through 08 is this structure with more paths and "
          "cleverer phases."]),

  ("h1", "2 &nbsp; Which-path information"),
  ("callout", "If anything records which path was taken, the paths no longer "
              "interfere",
   ["<b>Interference requires that the paths be indistinguishable at "
    "the point where they meet</b> — <b>if any leftover qubit, "
    "anywhere, is correlated with which path ran, the amplitudes add as "
    "probabilities instead</b> and the cancellation does not "
    "happen.",
    "<b>Which is exactly Module 03 &sect;2's garbage "
    "problem</b> — <b>an uncomputed ancilla <i>is</i> a which-path "
    "record</b> — and <b>leaving it in place is why a correctly "
    "derived algorithm silently stops working</b> when implemented "
    "carelessly.",
    "<b>And it is also precisely what decoherence is</b> — "
    "<b>the environment records which path ran, accidentally and "
    "irreversibly</b> — so <b>noise and uncleaned garbage are the "
    "same failure</b> arising from different causes, which is a genuinely "
    "unifying observation.",
    "<b>So the design rule is a single statement: nothing outside "
    "the computation may learn which path was taken</b>, until the final "
    "measurement — <b>which covers Module 03 &sect;2 and the "
    "whole of Module 10 at once</b>, and is worth carrying as the "
    "subject's one safety property."]),

  ("break",),
  ("h1", "3 &nbsp; Decoherence"),
  ("ul", ["<b>Any coupling to the environment leaks which-path "
          "information</b> — <b>so the qubit must be "
          "isolated</b> — <b>and isolation conflicts directly with "
          "being able to control and read it</b>, which is where the "
          "difficulty lives.",
          "<b>Which is the central engineering tension of the whole "
          "field:</b> <b>controllable means coupled, and coupled means "
          "decohering</b> — and <b>every hardware platform "
          "(superconducting, trapped ion, photonic, neutral atom) is a "
          "particular position on that trade</b>, with different "
          "coherence times and different gate speeds.",
          "<b>So coherence time bounds circuit depth</b> — "
          "<b>the computation has to finish before the information "
          "leaks out</b> — which is why depth is one of "
          "Module 03 &sect;4's five metrics and not an "
          "afterthought.",
          "<b>And it is not a matter of better shielding</b> "
          "— <b>the required isolation grows with the number of "
          "qubits and with the depth</b>, so a fixed engineering "
          "improvement buys a fixed factor against an exponential "
          "need — <b>which is why error correction rather than "
          "isolation is the answer</b> (Module 10).",
          "<b>Which makes Module 10's threshold theorem the result "
          "the entire field depends on</b>: it says that below a certain "
          "physical error rate, arbitrarily long computations become "
          "possible — that the problem is solvable in principle, "
          "which was not obvious and is not cheap. <b>Controllable means "
          "coupled, and coupled means decohering</b> — <b>which is "
          "why this is hard in a way better engineering alone does not "
          "fix.</b>"]),

  ("h1", "4 &nbsp; As a design principle"),
  ("callout", "The question to ask of any quantum algorithm is: what "
              "cancels, and why",
   ["<b>For Deutsch-Jozsa, the constant case's paths all reinforce "
    "on the all-zeros outcome and the balanced case's cancel "
    "there</b> (Module 05 &sect;2) — <b>the cancellation does "
    "the deciding</b>, in a single query.",
    "<b>For Grover, each iteration rotates the state's amplitude "
    "toward the marked basis state by a fixed angle</b> (Module 06 "
    "&sect;2) — <b>and keeps rotating past it if you "
    "overshoot</b>, <b>which is the clearest available demonstration "
    "that this is geometry rather than accumulation</b> (and is what "
    "Project 1 asks you to plot).",
    "<b>For Shor, the Fourier transform makes the amplitudes at "
    "frequencies that are not multiples of the period cancel</b> "
    "(Modules 07 and 08) — <b>which is the one case where the "
    "structure being exploited is entirely obvious</b> once stated: "
    "periodicity is exactly what a Fourier transform detects.",
    "<b>So if you cannot say what cancels, you have not understood "
    "the algorithm</b> — and, more usefully, <b>if a proposed "
    "algorithm has no cancellation story, it has no advantage</b>, "
    "<b>which is a quick and effective filter on claims</b> "
    "(Module 13 &sect;2)."]),
 ],
 "resources": [
   ("Preskill's notes, the lectures on quantum information (free)",
    "http://theory.caltech.edu/~preskill/ph229/",
    "<b>&sect;&sect;2 and 3</b> — decoherence and which-path "
    "information, developed properly rather than by analogy."),
   ("Nielsen & Chuang, chapters 6 and 8 (library copy)",
    "https://www.cambridge.org/9781107002173",
    "<b>&sect;1's path view and &sect;3's open-system "
    "formalism</b>."),
   ("Zurek &mdash; Decoherence and the transition from quantum to "
    "classical (free)",
    "https://arxiv.org/abs/quant-ph/0306072",
    "<b>&sect;&sect;2 and 3</b> — the which-path account of "
    "decoherence from the person who developed it."),
   ("Aaronson &mdash; lecture notes on the source of quantum "
    "speedups (free)",
    "https://www.scottaaronson.com/qclec.pdf",
    "<b>&sect;&sect;1 and 4</b> — and the 'what cancels' question "
    "treated as the central one, which it is."),
 ],
 "exercises": [
   "<b>Write the amplitude of one outcome as a path sum</b> for a "
   "three-gate circuit.",
   "<b>Trace H H |0></b> by hand, naming both paths to each "
   "outcome.",
   "<b>Trace H X H |0></b>, and say which sign moved.",
   "<b>Build a circuit where the cancellation is exact</b>, and verify "
   "it in your simulator.",
   "<b>Then entangle an ancilla with the path</b>, and observe the "
   "interference disappear.",
   "<b>Explain why that ancilla is a which-path record.</b>",
   "<b>Relate that experiment to decoherence</b>, in four "
   "sentences.",
   "<b>State the isolation-versus-control tension</b> and give two "
   "hardware platforms' positions on it.",
   "<b>For each algorithm in Modules 05 to 08, say what cancels.</b>",
   "<b>Find a claimed quantum algorithm</b> and ask what its "
   "cancellation story is.",
 ],
 "selfcheck": [
   "State the mechanism in one sentence.",
   "Why can probabilities not do this?",
   "Why does the mechanism explain the shortness of the advantage "
   "list?",
   "Trace the two-qubit example and name the cancelling paths.",
   "What does H do, structurally?",
   "State the which-path rule.",
   "Why is uncomputed garbage a which-path record?",
   "How are garbage and decoherence the same failure?",
   "State the isolation-control tension and its consequence for "
   "depth.",
   "What is the question to ask of any quantum algorithm?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "The Query Model",
 "subtitle": "Where the separations are provable, and what that is "
             "worth.",
 "question": "One query, and you know the answer. What was the "
             "catch?",
 "outcomes": [
     "Explain the query model and why it is used.",
     "Derive the Deutsch-Jozsa algorithm.",
     "Explain Simon's problem as the bridge to Shor.",
     "Distinguish query complexity from time complexity.",
     "State what a query separation does and does not establish.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The model",
   "blurb": "And why almost every clean result lives in it."},

  {"t": "callout", "title": "In the query model you count oracle calls and ignore everything else, which is what makes lower bounds provable",
   "kind": "Why this model dominates the theory",
   "body": ["<b>The input is a function you may evaluate but not "
            "inspect</b> — <b>so the only resource is the number of "
            "evaluations</b>, and all other computation is "
            "free.",
            "<b>Which makes lower bounds tractable</b>: <b>you can "
            "prove that k queries cannot distinguish two cases</b>, "
            "which is a statement about information rather than about "
            "circuits.",
            "<b>And that is why the subject's provable separations "
            "are nearly all query separations</b> — <b>Deutsch-Jozsa, "
            "Simon, Grover's optimality</b> — while the results people "
            "care about (factoring) are not proven at "
            "all.",
            "<b>So the model is a tool for honest "
            "statements</b> — <b>and the honest statement about "
            "Part 4 is that a query separation is "
            "weaker than it sounds.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Deutsch-Jozsa",
   "blurb": "One query against exponentially many, and worth tracing "
            "fully."},

  {"t": "code", "kicker": "Deutsch-Jozsa", "title": "The algorithm, and what cancels",
   "lang": "text", "code": """
  PROBLEM
      f: {0,1}^n -> {0,1} is promised to be either
      constant or balanced. Which?

  CLASSICAL
      2^(n-1) + 1 queries in the worst case,
      deterministically. (Randomised: O(1) for high
      confidence -- which matters, see below.)

  QUANTUM, one query
      1  H on all n qubits:  uniform superposition
      2  phase oracle:  |x> -> (-1)^f(x)|x>
      3  H on all n qubits again
      4  measure

  WHY IT WORKS
      amplitude of |0...0> after step 3 is
          (1/2^n) * sum over x of (-1)^f(x)
      constant f  => that sum is +-1, so we measure
                     all zeros with certainty
      balanced f  => the sum is exactly 0: perfect
                     cancellation, so all zeros is
                     impossible
""",
   "caption": "<b>Constant reinforces on all-zeros and balanced "
              "cancels there exactly</b> — which is "
              "Module 04's mechanism in its clearest "
              "form.",
   "note": "Trace this fully; it is the model example of the whole "
           "course."},

  {"t": "callout", "title": "And the honest caveat, which is the reason this is a teaching example and not a result",
   "kind": "What the exponential separation actually requires",
   "body": ["<b>The exponential gap is against <i>deterministic</i> "
            "classical algorithms</b> — <b>a randomised classical "
            "algorithm answers with high confidence in a constant number "
            "of queries</b>, by sampling a few points.",
            "<b>So the dramatic separation needs exact "
            "classical</b>, which is an unusual thing to "
            "demand — and <b>stating it as 'exponentially faster' "
            "without that qualification is misleading.</b>",
            "<b>Which is why Simon's problem matters "
            "more</b> — <b>it is an exponential separation against "
            "<i>randomised</i> classical algorithms</b>, which is the "
            "meaningful comparison.",
            "<b>And Simon's structure is period-finding</b> — "
            "<b>a hidden XOR mask, found by interference</b> — which "
            "is the direct ancestor of Shor "
            "(Module 08)."]},

  {"t": "section", "label": "Part 3", "title": "Simon's problem",
   "blurb": "The real separation, and the bridge."},

  {"t": "eq", "kicker": "Simon", "title": "The problem and the mechanism",
   "eqs": [
     ("promise:  f(x) = f(y) iff y = x XOR s,  for a hidden s",
      "A two-to-one function with a hidden XOR period. Find s."),
     ("classical: Ω(2^(n/2)) queries, even randomised",
      "You must find a collision, and collisions are rare — a "
      "birthday argument. This is the meaningful lower bound."),
     ("quantum: O(n) queries, then classical linear algebra",
      "Each run yields a random y with y·s = 0 mod 2. Collect n−1 "
      "independent such y and solve for s."),
   ],
   "caption": "<b>Each quantum run returns a random linear "
              "constraint on s</b>, and n of them determine it — "
              "which is the same shape as Shor's "
              "algorithm.",
   "note": "Simon is the bridge: hidden periodicity, found by "
           "interference, then finished classically."},

  {"t": "section", "label": "Part 4", "title": "What it establishes",
   "blurb": "Which is less than a time separation."},

  {"t": "bullets", "kicker": "The claim", "title": "Query separations, read honestly",
   "items": [
     "<b>A query lower bound is a real theorem</b>, and <b>it is "
     "unconditional</b> — unlike almost everything in complexity "
     "theory (CSCE 637 §01).",
     "",
     "<b>But it is relative to an oracle</b>, and <b>an oracle "
     "separation does not imply a separation for explicitly given "
     "functions</b> — which is a known and important "
     "gap.",
     "",
     "<b>And it ignores the oracle's own cost</b> "
     "(Module 03 §3) — <b>so an O(1)-query algorithm calling a "
     "circuit of exponential size is not "
     "fast.</b>",
     "",
     "<b>Which is the trap:</b> <b>'exponentially fewer queries' "
     "is routinely reported as 'exponentially faster'</b>, and they are "
     "different claims.",
     "",
     "<b>So the model proves things and the things it proves are "
     "narrower than the headlines</b> — both halves of which are "
     "worth holding.",
   ],
   "footnote": "<b>'Exponentially fewer queries' is not "
               "'exponentially faster'</b> — and the substitution is "
               "made routinely, including in abstracts."},

  {"t": "callout", "title": "And what to carry forward",
   "kind": "Closing",
   "body": ["<b>The query model is where this subject's honest "
            "theorems live</b>, and <b>Grover's optimality "
            "(Module 06 §4) is the most important of "
            "them</b> — it bounds what search can ever "
            "buy.",
            "<b>Simon's structure is the one to "
            "remember</b> — <b>hidden periodicity, extracted by "
            "interference, finished by classical linear "
            "algebra</b> — because <b>Shor has exactly that "
            "shape.</b>",
            "<b>And the discipline is to state which complexity you "
            "are talking about</b> — <b>queries, gates, depth, or "
            "wall-clock</b> — which is "
            "Module 03 §4's five metrics as an honesty "
            "requirement.",
            "<b>Which is this module's version of the program's "
            "rule:</b> <b>name the resource you counted, because the "
            "separation is a statement about that resource and not about "
            "speed in general.</b>"]},
 ],
 "takeaways": [
   "In the query model you count oracle calls and ignore everything else, "
   "which is what makes lower bounds provable.",
   "Deutsch-Jozsa: constant f reinforces on all-zeros and balanced f "
   "cancels there exactly, in one query.",
   "Its exponential gap is against deterministic classical algorithms only; "
   "randomised classical solves it in constant queries.",
   "Simon's problem is the meaningful separation — exponential against "
   "randomised — and its structure is hidden periodicity.",
   "A query separation is relative to an oracle and ignores the oracle's "
   "own cost.",
   "'Exponentially fewer queries' is not 'exponentially faster', and the "
   "substitution is made routinely.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The model"),
  ("callout", "In the query model you count oracle calls and ignore "
              "everything else, which is what makes lower bounds provable",
   ["<b>The input is a function you may evaluate but not "
    "inspect</b> — <b>so the only resource counted is the number of "
    "evaluations</b>, and all other computation, however much, is "
    "free.",
    "<b>Which makes lower bounds tractable</b>: <b>you can prove "
    "that k queries cannot possibly distinguish two cases</b>, because "
    "<b>that is a statement about information rather than about "
    "circuits</b> — and circuit lower bounds are notoriously out of "
    "reach (CSCE 637 Module 09).",
    "<b>And that is precisely why this subject's provable "
    "separations are nearly all query separations</b> — "
    "<b>Deutsch-Jozsa, Simon, Bernstein-Vazirani, and Grover's "
    "optimality</b> — <b>while the result people actually care "
    "about, factoring, is not proven at all</b> (Module 12 "
    "&sect;3).",
    "<b>So the model is a tool for making honest "
    "statements</b> — <b>and the honest statement about it, in "
    "&sect;4, is that a query separation is weaker than it "
    "sounds</b>, which does not stop it from being a real theorem."]),

  ("h1", "2 &nbsp; Deutsch-Jozsa"),
  ("code", """PROBLEM
    f: {0,1}^n -> {0,1} is promised to be either
    constant or balanced. Which one?

CLASSICAL
    2^(n-1) + 1 queries in the worst case,
    deterministically. (Randomised: O(1) for high
    confidence -- which matters; see the callout.)

QUANTUM, one query
    1  H on all n qubits:  uniform superposition
    2  phase oracle:  |x> -> (-1)^f(x)|x>
    3  H on all n qubits again
    4  measure

WHY IT WORKS
    amplitude of |0...0> after step 3 is
        (1/2^n) * sum over x of (-1)^f(x)
    constant f  => that sum is +-1, so we measure
                   all zeros with certainty
    balanced f  => the sum is exactly 0: perfect
                   cancellation, so all zeros is
                   impossible"""),
  ("p", "<b>Constant f reinforces on the all-zeros outcome and "
        "balanced f cancels there exactly</b> — <b>which is "
        "Module 04's mechanism in its clearest possible form</b>: the "
        "two cases are distinguished by whether a particular sum of "
        "&plusmn;1 terms is extremal or zero. <b>Trace this fully by "
        "hand; it is the model example of the whole course</b>, and the "
        "second layer of H gates is where the path sum is actually "
        "performed."),
  ("callout", "And the honest caveat, which is the reason this is a teaching "
              "example and not a result",
   ["<b>The exponential gap is against <i>deterministic</i> classical "
    "algorithms</b> — <b>a randomised classical algorithm answers "
    "with high confidence in a constant number of queries</b>, simply by "
    "sampling a few points and seeing whether they agree.",
    "<b>So the dramatic separation requires exact classical "
    "computation</b>, <b>which is an unusual thing to "
    "demand</b> — and <b>stating it as 'exponentially faster' "
    "without that qualification is misleading</b>, though it is "
    "frequently done in popular accounts.",
    "<b>Which is why Simon's problem matters considerably "
    "more</b> — <b>it is an exponential separation against "
    "<i>randomised</i> classical algorithms</b>, <b>which is the "
    "meaningful comparison</b> since nobody is restricted to "
    "deterministic methods (CSCE 658's whole premise).",
    "<b>And Simon's structure is period-finding</b> — <b>a "
    "hidden XOR mask, located by interference</b> — <b>which makes "
    "it the direct ancestor of Shor's algorithm</b> (Module 08), and "
    "is why it is worth more attention than its obscurity "
    "suggests."]),

  ("break",),
  ("h1", "3 &nbsp; Simon's problem"),
  ("eq", "promise:&nbsp; f(x) = f(y) iff y = x &oplus; s,&nbsp; for a "
         "hidden nonzero s"),
  ("ul", ["<b>f is two-to-one with a hidden XOR period s</b>, and the "
          "task is to find s — a promise problem, like "
          "Deutsch-Jozsa, but with an answer to extract rather than a "
          "bit to decide.",
          "<b>Classically it takes &Omega;(2<super>n/2</super>) "
          "queries, even with randomisation</b> — <b>because you "
          "must find a collision, and collisions are rare</b> until you "
          "have seen about the square root of the domain (a birthday "
          "argument, CSCE 658 Module 04). <b>This is the meaningful "
          "lower bound</b>, and it is the one Deutsch-Jozsa lacks.",
          "<b>Quantumly it takes O(n) queries, plus classical linear "
          "algebra</b>: <b>each run yields a uniformly random y "
          "satisfying y &middot; s = 0 (mod 2)</b> — the "
          "interference kills every y that does not satisfy it — and "
          "<b>n &minus; 1 independent such constraints determine s "
          "uniquely.</b>",
          "<b>Each quantum run returns a random linear constraint on "
          "s, and n of them determine it</b> — <b>which is exactly "
          "the same shape as Shor's algorithm</b>: a quantum subroutine "
          "that produces one random piece of information about a hidden "
          "period, called repeatedly, finished classically.",
          "<b>Simon is the bridge</b>: <b>hidden periodicity, found "
          "by interference, then finished classically</b> — and "
          "recognising that shape is what makes Module 08 feel "
          "inevitable rather than magical."]),

  ("h1", "4 &nbsp; What it establishes"),
  ("ul", ["<b>A query lower bound is a real theorem</b>, and <b>it is "
          "unconditional</b> — <b>unlike almost everything else in "
          "complexity theory</b>, which rests on unproven assumptions "
          "(CSCE 637 Module 01's framing). That is a genuine and "
          "unusual strength.",
          "<b>But it is relative to an oracle</b>, and <b>an oracle "
          "separation does not imply a separation for explicitly given "
          "functions</b> — <b>which is a known and important "
          "gap</b>, and the reason oracle results cannot settle "
          "questions like P versus NP (CSCE 637 Module 10's "
          "relativisation barrier).",
          "<b>And it ignores the oracle's own implementation "
          "cost</b> (Module 03 &sect;3) — <b>so an O(1)-query "
          "algorithm that calls a circuit of exponential size is not a "
          "fast algorithm</b>, and the query count says nothing about "
          "that.",
          "<b>Which is the trap:</b> <b>'exponentially fewer "
          "queries' is routinely reported as 'exponentially "
          "faster'</b>, <b>and they are different claims</b> — the "
          "substitution appears in abstracts, press releases, and "
          "occasionally in textbooks.",
          "<b>So the model proves real things, and the things it "
          "proves are narrower than the headlines</b> — <b>both "
          "halves of which are worth holding at once</b>, which is the "
          "general posture this course asks for."]),
  ("callout", "And what to carry forward",
   ["<b>The query model is where this subject's honest theorems "
    "live</b>, and <b>Grover's optimality (Module 06 &sect;4) is the "
    "most important of them</b> — <b>it bounds what unstructured "
    "search can ever buy</b>, for all time, which is a rare kind of "
    "knowledge.",
    "<b>Simon's structure is the one to remember</b> — "
    "<b>hidden periodicity, extracted by interference, finished by "
    "classical linear algebra</b> — because <b>Shor's algorithm "
    "has exactly that shape</b> with the XOR group replaced by the "
    "integers mod N.",
    "<b>And the discipline is to state which complexity you are "
    "talking about</b> — <b>queries, gate count, depth, T-count, or "
    "wall-clock</b> — <b>which is Module 03 &sect;4's five "
    "metrics restated as an honesty requirement</b> rather than an "
    "engineering one.",
    "<b>Which is this module's version of the program's rule:</b> "
    "<b>name the resource you counted</b>, <b>because the separation is "
    "a statement about that resource and not about speed in "
    "general</b>."]),
 ],
 "resources": [
   ("Deutsch & Jozsa &mdash; Rapid solution of problems by quantum "
    "computation",
    "https://royalsocietypublishing.org/doi/10.1098/rspa.1992.0167",
    "<b>&sect;2 in the original</b> — short, and the promise "
    "structure is stated clearly."),
   ("Simon &mdash; On the power of quantum computation",
    "https://epubs.siam.org/doi/10.1137/S0097539796298637",
    "<b>&sect;3 in the original</b> — and the paper Shor credits as "
    "the one that suggested the approach."),
   ("Watrous's notes on query complexity (free)",
    "https://cs.uwaterloo.ca/~watrous/QC-notes/",
    "<b>&sect;&sect;1 and 4</b> — the model stated rigorously, with "
    "the lower-bound methods."),
   ("Beals et al. &mdash; Quantum lower bounds by polynomials (free)",
    "https://arxiv.org/abs/quant-ph/9802049",
    "<b>&sect;4's technique</b> — the polynomial method, which is how "
    "most query lower bounds including Grover's are proved."),
 ],
 "exercises": [
   "<b>State the query model</b> and say why lower bounds are easier "
   "in it.",
   "<b>Trace Deutsch-Jozsa for n = 2</b>, all four f, by hand.",
   "<b>Compute the all-zeros amplitude</b> for a balanced f and verify "
   "it is zero.",
   "<b>Implement it</b> and confirm the certainty of both cases.",
   "<b>Give the randomised classical algorithm</b> and its query "
   "count.",
   "<b>State Simon's promise</b> and the classical lower bound's "
   "argument.",
   "<b>Implement Simon's algorithm</b> for n = 4 and recover s.",
   "<b>Count the runs needed</b> and compare to n − 1.",
   "<b>Explain the relativisation gap</b> in your own words.",
   "<b>Find a paper or article</b> that substitutes 'faster' for "
   "'fewer queries'.",
 ],
 "selfcheck": [
   "What is counted in the query model, and why use it?",
   "Why are query lower bounds provable when circuit ones are not?",
   "State Deutsch-Jozsa's promise and the quantum algorithm.",
   "What cancels, and in which case?",
   "State the caveat about the classical comparison.",
   "Why does Simon's problem matter more?",
   "Give Simon's promise, both bounds, and the mechanism.",
   "What shape does Simon share with Shor?",
   "Name three limits of a query separation.",
   "What is the routine substitution to watch for?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Grover's Algorithm",
 "subtitle": "Quadratic, optimal, and frequently not enough.",
 "question": "Why can't it be better than square root?",
 "outcomes": [
     "Derive Grover's algorithm as a rotation.",
     "Explain the iteration count and the overshoot.",
     "Generalise to amplitude amplification.",
     "State and explain the optimality lower bound.",
     "Assess when a quadratic speedup is worth having.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem and the idea",
   "blurb": "Search with no structure at all."},

  {"t": "callout", "title": "Given an oracle marking one of N items, find it — and the quantum algorithm is a rotation in a two-dimensional plane",
   "kind": "The setup and the key simplification",
   "body": ["<b>Classically this takes N/2 queries on "
            "average</b> and N in the worst case; <b>there is nothing "
            "to exploit, which is what 'unstructured' "
            "means.</b>",
            "<b>The quantum algorithm takes about π/4 times the "
            "square root of N</b> — <b>a quadratic "
            "improvement</b> — and the derivation is unusually "
            "clean.",
            "<b>Because the whole evolution stays in the plane "
            "spanned by two vectors</b>: <b>the marked state, and the "
            "uniform superposition over the unmarked "
            "ones</b>.",
            "<b>So the algorithm is a rotation in that "
            "plane</b> — <b>two reflections make a rotation</b>, and "
            "each Grover iteration is exactly two "
            "reflections."]},

  {"t": "section", "label": "Part 2", "title": "The iteration",
   "blurb": "Two reflections, and the angle."},

  {"t": "eq", "kicker": "Grover", "title": "The iteration, and the count",
   "eqs": [
     ("G = (reflect about uniform) · (reflect about unmarked)",
      "The phase oracle reflects about the unmarked subspace; the "
      "diffusion operator reflects about the uniform state. Two "
      "reflections compose to a rotation."),
     ("rotation angle θ with sin(θ/2) = 1/√N",
      "Each iteration rotates the state by θ toward the marked "
      "state. The start is almost perpendicular to it."),
     ("iterations ≈ (π/4)√N, and overshooting rotates past",
      "Success probability rises to near 1 and then falls again, "
      "periodically. It is geometry, not accumulation."),
   ],
   "caption": "<b>Overshooting rotates past the marked state and the "
              "success probability falls</b> — which is the result "
              "that proves this is a rotation.",
   "note": "Project 1 asks you to plot exactly this curve, including "
           "the decline."},

  {"t": "callout", "title": "And amplitude amplification is the same thing, generalised",
   "kind": "Why Grover is a template rather than one algorithm",
   "body": ["<b>Replace 'uniform superposition' with any state "
            "preparation A, and 'marked' with any verifiable "
            "property</b> — <b>and the same two reflections "
            "apply.</b>",
            "<b>Which turns any classical algorithm that succeeds "
            "with probability p into a quantum one with about 1 over "
            "the square root of p repetitions</b>, rather than 1 over "
            "p.",
            "<b>So it is a generic quadratic speedup over any "
            "Monte Carlo procedure</b> — <b>which is the broadest "
            "applicability of anything in this course</b> "
            "(CSCE 658's algorithms are all candidates).",
            "<b>And it composes</b>: <b>amplitude estimation gives "
            "a quadratic improvement in estimating p "
            "itself</b> — which is where several proposed "
            "applications come from, and where "
            "Part 4's caution applies hardest."]},

  {"t": "section", "label": "Part 3", "title": "Optimality",
   "blurb": "Why quadratic is the ceiling."},

  {"t": "callout", "title": "No quantum algorithm can search N unstructured items in fewer than order √N queries, and this is a theorem",
   "kind": "The most important negative result in the subject",
   "body": ["<b>The bound predates Grover's algorithm</b> — "
            "<b>Bennett, Bernstein, Brassard and Vazirani proved it "
            "first</b> — so the algorithm was known to be optimal "
            "when it appeared.",
            "<b>The argument is a hybrid or polynomial "
            "argument</b>: <b>each query can only change the state by a "
            "bounded amount</b>, so distinguishing N cases needs order "
            "√N of them.",
            "<b>Which rules out exponential speedup for "
            "NP-complete problems <i>by brute-force search</i></b> "
            "— <b>and brute-force search is what the "
            "tries-all-answers picture implicitly "
            "promised</b> (Module 01 §2).",
            "<b>And it does not rule out an exponential speedup via "
            "structure</b> — <b>it says only that search alone will "
            "not do it</b>, which is the precise and frequently "
            "misstated content of the result."]},

  {"t": "section", "label": "Part 4", "title": "Is quadratic worth it?",
   "blurb": "Honestly, and usually not."},

  {"t": "bullets", "kicker": "Assessment", "title": "What a quadratic speedup survives, and what eats it",
   "items": [
     "<b>The error-correction overhead is "
     "large</b> (Module 10 §4) — <b>and a quadratic speedup "
     "with a thousandfold constant-factor penalty needs an enormous N "
     "before it wins.</b>",
     "",
     "<b>Grover does not parallelise well</b> — <b>k "
     "machines give only a √k improvement</b>, while classical search "
     "parallelises linearly, which erodes the advantage "
     "further.",
     "",
     "<b>And the oracle must be built</b> "
     "(Module 03 §3) — <b>its circuit is evaluated "
     "coherently, which is more expensive than a classical "
     "evaluation.</b>",
     "",
     "<b>So the published analyses are "
     "pessimistic</b> — <b>for many proposed applications, "
     "classical hardware wins at every feasible problem "
     "size</b>.",
     "",
     "<b>Which does not make it useless</b>: <b>it halves "
     "symmetric key security exponents</b>, which is a real and "
     "already-accounted-for consequence.",
   ],
   "footnote": "<b>Grover parallelises poorly — k machines buy "
               "only √k</b> — which is a specific and "
               "under-reported reason the advantage erodes against "
               "classical clusters."},

  {"t": "callout", "title": "And the honest summary",
   "kind": "Closing",
   "body": ["<b>Grover is beautiful, general, provably optimal, and "
            "probably not where the value is</b> — all four at "
            "once.",
            "<b>Its real importance is the lower bound</b>, which "
            "<b>tells you where not to look</b>: <b>any claim of "
            "exponential advantage by searching is "
            "wrong</b>, immediately and provably.",
            "<b>And its secondary importance is amplitude "
            "amplification as a template</b> "
            "(Part 2) — <b>which is the thing to reach "
            "for when a classical randomised algorithm is the "
            "baseline.</b>",
            "<b>So the lesson is Module 01 §3's, "
            "sharpened:</b> <b>structure is what buys exponential "
            "advantage, and search is the absence of "
            "structure</b> — which is why Modules 07 and 08 are "
            "the important ones."]},
 ],
 "takeaways": [
   "Grover's evolution stays in a two-dimensional plane, so the algorithm "
   "is a rotation and two reflections make each iteration.",
   "Overshooting rotates past the marked state and the success probability "
   "falls, which proves it is geometry rather than accumulation.",
   "Amplitude amplification generalises it: any classical procedure "
   "succeeding with probability p needs about 1/√p repetitions.",
   "Order √N is a proven lower bound, and it predates the algorithm.",
   "The bound rules out exponential speedup for NP-complete problems by "
   "brute-force search, and nothing more than that.",
   "Grover parallelises poorly — k machines buy only √k — "
   "which erodes the advantage against classical clusters.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The problem and the idea"),
  ("callout", "Given an oracle marking one of N items, find it — and "
              "the quantum algorithm is a rotation in a two-dimensional "
              "plane",
   ["<b>Classically this takes N/2 queries on average and N in the "
    "worst case</b>, and <b>there is nothing whatever to exploit, which "
    "is exactly what 'unstructured' means</b> — the oracle is a "
    "black box with no pattern to find.",
    "<b>The quantum algorithm takes about (&pi;/4)&radic;N "
    "queries</b> — <b>a quadratic improvement</b> — and <b>the "
    "derivation is unusually clean</b> for this subject, which is why it "
    "is the algorithm everybody meets first.",
    "<b>Because the whole evolution stays within the plane spanned "
    "by two vectors</b>: <b>the marked basis state, and the uniform "
    "superposition over all the unmarked ones</b> — the circuit "
    "never leaves that two-dimensional subspace, so the "
    "2<sup>n</sup>-dimensional problem collapses to plane "
    "geometry.",
    "<b>So the algorithm is a rotation in that plane</b> — "
    "<b>and two reflections compose to a rotation</b>, by elementary "
    "geometry — <b>and each Grover iteration is exactly two "
    "reflections</b> (&sect;2)."]),

  ("h1", "2 &nbsp; The iteration"),
  ("eq", "G = (reflect about the uniform state) &middot; (reflect about "
         "the unmarked subspace)"),
  ("ul", ["<b>The phase oracle reflects about the unmarked "
          "subspace</b> (it negates the marked state's amplitude); "
          "<b>the diffusion operator reflects about the uniform "
          "state</b> — and <b>two reflections compose to a "
          "rotation</b> through twice the angle between the mirrors.",
          "<b>The rotation angle &theta; satisfies "
          "sin(&theta;/2) = 1/&radic;N</b> — <b>so each iteration "
          "rotates the state by &theta; toward the marked "
          "state</b>, and <b>the starting state is very nearly "
          "perpendicular to it</b>, which is why about "
          "(&pi;/2)/&theta; &asymp; (&pi;/4)&radic;N iterations are "
          "needed.",
          "<b>And overshooting rotates past the marked state</b>: "
          "<b>the success probability rises to near 1 and then falls "
          "again, periodically</b> — <b>it is geometry, not "
          "accumulation</b>, and a Grover loop run twice as long as it "
          "should be is worse than useless.",
          "<b>Overshooting rotates past the marked state and the "
          "success probability falls</b> — <b>which is the result "
          "that proves this is a rotation</b>, and is why "
          "<b>Project 1 asks you to plot exactly this curve, including "
          "the decline</b>: reproducing the decline demonstrates you "
          "understand the mechanism rather than the recipe.",
          "<b>With multiple marked items the angle changes</b> "
          "(sin(&theta;/2) = &radic;(M/N) for M marks), <b>so knowing M "
          "matters</b> — and not knowing it is handled by a "
          "randomised schedule."]),
  ("callout", "And amplitude amplification is the same thing, generalised",
   ["<b>Replace 'uniform superposition' with any state-preparation "
    "unitary A, and 'marked' with any efficiently verifiable "
    "property</b> — <b>and the same two reflections apply</b> "
    "unchanged, with the angle set by A's success amplitude.",
    "<b>Which turns any classical algorithm that succeeds with "
    "probability p into a quantum one needing about 1/&radic;p "
    "repetitions</b> rather than the classical 1/p — which is a "
    "quadratic improvement on the repetition count of any Monte Carlo "
    "procedure.",
    "<b>So it is a generic quadratic speedup over any Monte Carlo "
    "method</b> — <b>which is by far the broadest applicability of "
    "anything in this course</b>, and makes <b>every algorithm in "
    "CSCE 658 a candidate</b> in principle.",
    "<b>And it composes</b>: <b>amplitude estimation gives a "
    "quadratic improvement in estimating p itself</b> — which is "
    "where a number of proposed financial and physical-simulation "
    "applications come from, <b>and where &sect;4's caution applies "
    "hardest</b>, because those applications' N is not "
    "astronomical."]),

  ("break",),
  ("h1", "3 &nbsp; Optimality"),
  ("callout", "No quantum algorithm can search N unstructured items in fewer "
              "than order √N queries, and this is a theorem",
   ["<b>The bound predates Grover's algorithm</b> — "
    "<b>Bennett, Bernstein, Brassard and Vazirani proved it "
    "first</b> — <b>so the algorithm was known to be optimal at the "
    "moment it appeared</b>, which is a pleasing piece of history and an "
    "unusual one.",
    "<b>The argument is a hybrid argument, or equivalently a "
    "polynomial one</b>: <b>each query can only change the state by a "
    "bounded amount in the relevant norm</b>, so <b>distinguishing N "
    "possible marked positions requires order &radic;N of them</b>. The "
    "polynomial method (Beals et al.) gives it cleanly.",
    "<b>Which rules out an exponential speedup for NP-complete "
    "problems <i>by brute-force search</i></b> — and <b>brute-force "
    "search over all candidate solutions is exactly what the "
    "tries-all-answers picture implicitly promised</b> (Module 01 "
    "&sect;2's false consequence, now a theorem).",
    "<b>And it does not rule out an exponential speedup via "
    "structure</b> — <b>it says only that search alone will not "
    "achieve one</b> — <b>which is the precise and very frequently "
    "misstated content of the result</b>: 'quantum computers cannot "
    "solve NP-complete problems' is stronger than what is known "
    "(Module 12 &sect;2)."]),

  ("h1", "4 &nbsp; Is quadratic worth it?"),
  ("ul", ["<b>The error-correction overhead is large</b> "
          "(Module 10 &sect;4) — <b>and a quadratic speedup "
          "carrying a thousandfold constant-factor penalty needs an "
          "enormous N before it wins</b>, since &radic;N must beat "
          "1000-and-change times the classical constant.",
          "<b>Grover does not parallelise well</b> — <b>k "
          "independent machines give only a &radic;k improvement</b> "
          "(each searches N/k items in &radic;(N/k) time), <b>while "
          "classical search parallelises linearly</b> — <b>which "
          "erodes the advantage further against a classical cluster</b> "
          "and is a specific, under-reported point.",
          "<b>And the oracle must actually be built</b> "
          "(Module 03 &sect;3) — <b>its circuit is evaluated "
          "coherently and reversibly, which is materially more expensive "
          "than a classical evaluation of the same predicate.</b>",
          "<b>So the published analyses are pessimistic</b> — "
          "<b>for a good number of proposed applications, classical "
          "hardware wins at every feasible problem size</b>, which is a "
          "conclusion from careful resource accounting rather than "
          "scepticism.",
          "<b>Which does not make Grover useless</b>: <b>it halves "
          "the effective security exponent of symmetric keys and hash "
          "functions</b>, which is a real consequence and is <b>already "
          "accounted for in current key-size recommendations</b> "
          "(CSCE 711 Module 13's post-quantum discussion)."]),
  ("callout", "And the honest summary",
   ["<b>Grover's algorithm is beautiful, general, provably optimal, "
    "and probably not where the value is</b> — all four at once, "
    "and holding all four is the right posture.",
    "<b>Its real importance is the lower bound</b>, which <b>tells "
    "you where not to look</b>: <b>any claim of an exponential quantum "
    "advantage achieved by searching is wrong</b>, immediately and "
    "provably, which is a useful filter to be able to apply in "
    "seconds.",
    "<b>And its secondary importance is amplitude amplification as "
    "a template</b> (&sect;2's callout) — <b>which is the thing to "
    "reach for whenever a classical randomised algorithm is the "
    "baseline</b>, and is the most reusable tool in the course.",
    "<b>So the lesson is Module 01 &sect;3's, sharpened:</b> "
    "<b>structure is what buys exponential advantage, and search is "
    "precisely the absence of structure</b> — <b>which is why "
    "Modules 07 and 08 are the important ones</b> and why periodicity "
    "gets a whole module of machinery."]),
 ],
 "resources": [
   ("Grover &mdash; A fast quantum mechanical algorithm for database "
    "search (free)",
    "https://arxiv.org/abs/quant-ph/9605043",
    "<b>&sect;&sect;1 and 2 in the original</b> — four pages, and "
    "the geometric picture is not the one he used, which is "
    "instructive."),
   ("Bennett, Bernstein, Brassard & Vazirani &mdash; Strengths and "
    "weaknesses of quantum computing (free)",
    "https://arxiv.org/abs/quant-ph/9701001",
    "<b>&sect;3's lower bound</b> — and it is the paper that bounds "
    "the whole subject's search-based hopes."),
   ("Brassard, Høyer, Mosca & Tapp &mdash; Quantum amplitude "
    "amplification and estimation (free)",
    "https://arxiv.org/abs/quant-ph/0005055",
    "<b>&sect;2's generalisation</b> — the template, stated in full "
    "generality."),
   ("Babbush et al. &mdash; Focus beyond quadratic speedups (free)",
    "https://arxiv.org/abs/2011.04149",
    "<b>&sect;4's assessment</b>, from people building the hardware "
    "— and the conclusion is the honest one."),
 ],
 "exercises": [
   "<b>State the classical query cost</b> for unstructured search, "
   "average and worst case.",
   "<b>Show that the evolution stays in a two-dimensional "
   "plane.</b>",
   "<b>Derive the rotation angle</b> from the two reflections.",
   "<b>Implement Grover</b> and plot success probability against "
   "iteration count.",
   "<b>Run it past the optimum</b> and confirm the decline.",
   "<b>Modify it for M marked items</b> and verify the new angle.",
   "<b>Apply amplitude amplification</b> to a randomised algorithm you "
   "already have.",
   "<b>State the lower bound</b> and summarise its argument.",
   "<b>Compute the N at which a quadratic speedup with a 1000x "
   "constant wins.</b>",
   "<b>Work out the parallel scaling</b> for k machines, and compare "
   "to classical.",
 ],
 "selfcheck": [
   "State the problem and both costs.",
   "Why does the evolution stay in a plane?",
   "Give the two reflections and the resulting rotation.",
   "State the angle and the iteration count.",
   "What happens if you overshoot, and what does that prove?",
   "State amplitude amplification and its applicability.",
   "Give the lower bound and its date relative to the algorithm.",
   "What does the bound rule out, and what does it not?",
   "Name three things that erode a quadratic advantage.",
   "What is Grover's real importance?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "The Quantum Fourier Transform",
 "subtitle": "The one piece of machinery that buys an exponential "
             "advantage.",
 "question": "How can a Fourier transform on 2ⁿ points take n² "
             "gates?",
 "outcomes": [
     "Define the QFT and state what it does to a periodic state.",
     "Derive its efficient circuit.",
     "Explain why the exponential-size transform is cheap.",
     "Explain what the QFT does not give you.",
     "Implement and verify it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The transform",
   "blurb": "And why it is the right tool for periodicity."},

  {"t": "eq", "kicker": "Definition", "title": "The QFT, and its effect on a period",
   "eqs": [
     ("QFT: |x> → (1/√N) Σ_y ω^(xy) |y>,  ω = e^(2πi/N),  N = 2ⁿ",
      "The discrete Fourier transform, applied to the amplitude "
      "vector rather than to a list of data."),
     ("on a periodic state with period r, amplitude concentrates "
      "at y ≈ k·N/r",
      "Because the terms at other y have phases spread uniformly "
      "around the circle and sum to nearly zero — "
      "Module 04's cancellation, in its most useful instance."),
     ("so measuring y gives an estimate of a multiple of N/r",
      "One random multiple per run, from which r is recovered by "
      "continued fractions (Module 08)."),
   ],
   "caption": "<b>The QFT converts a period in the amplitudes into a "
              "peak in the outcome distribution</b> — which is the "
              "whole reason it matters.",
   "note": "Period becomes peak: that is the sentence to "
           "remember."},

  {"t": "callout", "title": "And the classical comparison is the thing to be careful about",
   "kind": "What the QFT is and is not faster than",
   "body": ["<b>The QFT acts on a vector of 2 to the n amplitudes "
            "using O(n²) gates</b> — <b>which looks like an "
            "exponential speedup over the classical FFT's "
            "O(N log N).</b>",
            "<b>And it is not one, in the usable sense:</b> <b>you "
            "cannot read out the transformed vector</b> — <b>one "
            "measurement gives one sample from "
            "it</b> (Module 02 §2).",
            "<b>So the QFT is not a faster Fourier "
            "transform</b> — <b>it is a device for making a period "
            "detectable in a single sample</b>, which is a narrower and "
            "genuinely useful thing.",
            "<b>Which is the most important caveat in the "
            "course</b>, because <b>'quantum computers do Fourier "
            "transforms exponentially faster' is a claim people build "
            "application proposals on</b> and it does not mean what it "
            "appears to."]},

  {"t": "section", "label": "Part 2", "title": "The circuit",
   "blurb": "Which is short, and derivable."},

  {"t": "code", "kicker": "Circuit", "title": "Why O(n²) gates suffice",
   "lang": "text", "code": """
  THE KEY FACTORISATION
      the QFT's output amplitude factorises across
      output qubits -- each output bit's state
      depends on the input through a product of
      phases. So the transform is a PRODUCT of
      single-qubit operations with phase
      corrections, not a general 2^n matrix.

  THE CIRCUIT, for qubit j from most significant
      1  H on qubit j
      2  controlled-R_k from each less significant
         qubit, k = 2, 3, ..., with phase 2 pi / 2^k
      3  move to the next qubit
      4  reverse the qubit order at the end

  GATE COUNT
      n Hadamards + n(n-1)/2 controlled rotations
      = O(n^2)

  AND THE SMALL ROTATIONS CAN BE DROPPED
      phases below the accuracy you need contribute
      negligibly: the approximate QFT uses
      O(n log n) gates, which matters a lot (M10)
""",
   "caption": "<b>The approximate QFT drops the tiny rotations and "
              "uses O(n log n) gates</b> — which is what makes "
              "Shor's circuit depth tolerable."},

  {"t": "callout", "title": "Because the transform factorises, which is also why the classical FFT is fast",
   "kind": "The shared structure worth noticing",
   "body": ["<b>The classical FFT is fast for the same structural "
            "reason</b> — <b>the DFT matrix factors into sparse "
            "pieces</b> — and the quantum circuit is that same "
            "factorisation realised as gates.",
            "<b>Which is reassuring:</b> <b>no new mathematical "
            "magic is involved</b>, only the fact that a unitary with "
            "this structure has a short circuit.",
            "<b>And it is a general lesson:</b> <b>a unitary has an "
            "efficient circuit when it factorises</b>, which is rare "
            "(Module 03 §1's counting argument) and is "
            "why algorithms are scarce.",
            "<b>So the QFT is precious precisely because it is both "
            "cheap and useful</b> — <b>most unitaries are "
            "neither</b>, and this one underwrites the subject's one "
            "dramatic result."]},

  {"t": "section", "label": "Part 3", "title": "What it gives",
   "blurb": "And what it does not."},

  {"t": "bullets", "kicker": "Scope", "title": "The QFT's actual uses, and the non-uses",
   "items": [
     "<b>Period finding</b>, which is phase estimation, which is "
     "Shor — <b>the one chain in this subject that leads to a "
     "superpolynomial advantage</b> "
     "(Module 08).",
     "",
     "<b>The hidden subgroup problem over abelian "
     "groups</b> — which generalises it, and <b>whose "
     "non-abelian cases are open and would matter</b> (graph "
     "isomorphism, lattice problems).",
     "",
     "<b>And that is approximately the list</b> — which is "
     "worth stating plainly, because the QFT's prominence suggests a "
     "wider applicability than it has.",
     "",
     "<b>It does not give you signal processing</b>, because "
     "<b>you cannot read out the spectrum</b> "
     "(Part 1).",
     "",
     "<b>And it does not give you data analysis</b>, for the same "
     "reason plus the input problem: <b>loading classical data into "
     "amplitudes is itself expensive</b> "
     "(Module 11 §4).",
   ],
   "footnote": "<b>Loading classical data into amplitudes is itself "
               "expensive</b> — which is the input problem, and it "
               "undermines most proposed data-analysis "
               "applications."},

  {"t": "section", "label": "Part 4", "title": "Implementing it",
   "blurb": "And how to know it is right."},

  {"t": "callout", "title": "Verify the QFT on a known period before building anything on it",
   "kind": "Closing",
   "body": ["<b>Prepare a state periodic with a known r</b>, apply "
            "your QFT, and <b>check that the outcome distribution peaks "
            "at multiples of N/r</b> — which is a complete functional "
            "test.",
            "<b>And check the inverse</b>: <b>QFT followed by "
            "inverse QFT must be the identity</b>, which catches qubit "
            "ordering errors — <b>and the final bit-reversal is where "
            "they live.</b>",
            "<b>Then compare against the classical FFT of your "
            "amplitude vector</b> — <b>your simulator has the whole "
            "vector, so you can check it exactly</b>, which real "
            "hardware cannot.",
            "<b>Which is the practical value of having written "
            "Module 02 §4's simulator:</b> <b>you can see the "
            "amplitudes that the model says are "
            "unobservable</b> — and that is how to debug an algorithm "
            "before trusting it."]},
 ],
 "takeaways": [
   "The QFT converts a period in the amplitudes into a peak in the outcome "
   "distribution — period becomes peak.",
   "It is not a faster Fourier transform: you cannot read out the "
   "transformed vector, only sample from it.",
   "Its circuit is O(n²) because the transform factorises, which is the "
   "same reason the classical FFT is fast.",
   "The approximate QFT drops the tiny rotations and uses O(n log n) gates, "
   "which is what makes Shor's depth tolerable.",
   "A unitary has an efficient circuit when it factorises, which is rare "
   "— and is why useful algorithms are scarce.",
   "Loading classical data into amplitudes is itself expensive, which "
   "undermines most proposed data-analysis applications.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The transform"),
  ("eq", "QFT:&nbsp; |x&gt; &rarr; (1/&radic;N) &Sigma;<sub>y</sub> "
         "&omega;<super>xy</super> |y&gt;,&nbsp; with "
         "&omega; = e<super>2&pi;i/N</super>, N = 2<sup>n</sup>"),
  ("ul", ["<b>It is the ordinary discrete Fourier transform</b>, "
          "<b>applied to the vector of amplitudes rather than to a list "
          "of data values</b> — which is the distinction everything "
          "in &sect;1's callout turns on.",
          "<b>On a state whose amplitudes are periodic with period "
          "r, the transform concentrates amplitude near y &asymp; "
          "k&middot;N/r</b> — <b>because the terms at other y have "
          "phases spread roughly uniformly around the unit circle and "
          "sum to nearly zero</b> — <b>which is Module 04's "
          "cancellation in its single most useful instance.</b>",
          "<b>So measuring y gives an estimate of some random "
          "multiple of N/r</b> — <b>one multiple per run</b> "
          "— <b>from which r is recovered by continued "
          "fractions</b> (Module 08 &sect;3), exactly as Simon's "
          "algorithm recovered s from random linear constraints "
          "(Module 05 &sect;3).",
          "<b>Period becomes peak: that is the sentence to "
          "remember</b>, and it is the whole reason this transform "
          "appears in the one algorithm everybody has heard of."]),
  ("callout", "And the classical comparison is the thing to be careful about",
   ["<b>The QFT acts on a vector of 2<sup>n</sup> amplitudes using "
    "only O(n<super>2</super>) gates</b> — <b>which looks very much "
    "like an exponential speedup over the classical FFT's "
    "O(N log N)</b> on a vector of the same length.",
    "<b>And it is not one, in any usable sense:</b> <b>you cannot "
    "read out the transformed vector</b> — <b>one measurement gives "
    "you one sample drawn from it</b> (Module 02 &sect;2's "
    "bottleneck), and reconstructing the vector takes exponentially many "
    "samples.",
    "<b>So the QFT is not a faster Fourier transform</b> — "
    "<b>it is a device for making a period detectable in a single "
    "sample</b> — <b>which is a much narrower and genuinely useful "
    "thing</b>, and is all that Shor's algorithm needs.",
    "<b>Which is the most important caveat in the course</b>, "
    "because <b>'quantum computers do Fourier transforms exponentially "
    "faster' is a claim people build application proposals on</b>, "
    "<b>and it does not mean what it appears to mean</b> "
    "(Module 11 &sect;4 and Module 13 &sect;3 both return to "
    "this)."]),

  ("h1", "2 &nbsp; The circuit"),
  ("code", """THE KEY FACTORISATION
    the QFT's output amplitude factorises across the
    output qubits -- each output bit's state depends
    on the input through a product of phases. So the
    transform is a PRODUCT of single-qubit
    operations with phase corrections, not a general
    2^n by 2^n matrix.

THE CIRCUIT, for qubit j from most significant
    1  H on qubit j
    2  controlled-R_k from each less significant
       qubit, k = 2, 3, ..., with phase 2 pi / 2^k
    3  move to the next qubit
    4  reverse the qubit order at the end

GATE COUNT
    n Hadamards + n(n-1)/2 controlled rotations
    = O(n^2)

AND THE SMALL ROTATIONS CAN BE DROPPED
    phases below the accuracy you need contribute
    negligibly: the approximate QFT uses
    O(n log n) gates, which matters a lot (M10)"""),
  ("p", "<b>The approximate QFT drops the tiny rotations and uses "
        "O(n log n) gates</b> — <b>which is what makes Shor's "
        "circuit depth tolerable</b> rather than merely polynomial, and "
        "is a good example of an approximation that costs nothing because "
        "the discarded terms are below the measurement's resolution "
        "anyway. The final bit-reversal is the step most often omitted in "
        "an implementation, and it is where ordering bugs live "
        "(&sect;4)."),
  ("callout", "Because the transform factorises, which is also why the "
              "classical FFT is fast",
   ["<b>The classical FFT is fast for the same structural "
    "reason</b> — <b>the DFT matrix factors into a product of "
    "sparse matrices</b> — and <b>the quantum circuit is that same "
    "factorisation realised as a sequence of gates</b> rather than as a "
    "recursion.",
    "<b>Which is reassuring</b>: <b>no new mathematical magic is "
    "involved</b>, only the fact that a unitary with this particular "
    "structure happens to have a short circuit — and the structure "
    "was known long before quantum computing.",
    "<b>And it is a general lesson worth extracting:</b> <b>a "
    "unitary has an efficient circuit when it factorises</b>, <b>which "
    "is rare</b> (Module 03 &sect;1's counting argument: there are "
    "vastly more unitaries than short circuits) <b>and is exactly why "
    "useful quantum algorithms are scarce</b> rather than abundant.",
    "<b>So the QFT is precious precisely because it is both cheap "
    "and useful</b> — <b>most unitaries are neither</b> — "
    "and <b>this single piece of machinery underwrites the subject's one "
    "dramatic result</b>, which is a lot of weight for one circuit to "
    "carry."]),

  ("break",),
  ("h1", "3 &nbsp; What it gives"),
  ("ul", ["<b>Period finding, which is phase estimation, which is "
          "Shor's algorithm</b> — <b>the one chain of reasoning in "
          "this subject that leads to a superpolynomial advantage</b> "
          "(Module 08), and it is worth seeing as a single chain "
          "rather than three topics.",
          "<b>The hidden subgroup problem over abelian "
          "groups</b> — which generalises period finding neatly, "
          "<b>and whose non-abelian cases are open and would matter a "
          "great deal</b> if solved: graph isomorphism and certain "
          "lattice problems are non-abelian HSP instances, and lattice "
          "problems are what post-quantum cryptography rests on "
          "(CSCE 711 Module 13).",
          "<b>And that is approximately the list</b> — <b>which "
          "is worth stating plainly</b>, because <b>the QFT's prominence "
          "in every introduction suggests a far wider applicability than "
          "it actually has.</b>",
          "<b>It does not give you signal processing</b>, because "
          "<b>you cannot read out the spectrum</b> (&sect;1's "
          "callout) — so 'quantum FFT for audio or images' is not a "
          "thing, however often it is proposed.",
          "<b>And it does not give you data analysis</b>, for that "
          "reason plus the input problem: <b>loading a classical dataset "
          "into amplitudes is itself expensive</b> — generally "
          "requiring time comparable to the data size, which destroys any "
          "polynomial advantage before the algorithm starts "
          "(Module 11 &sect;4). <b>The input problem undermines most "
          "proposed data-analysis applications</b>, and is the first "
          "question to ask of one."]),

  ("h1", "4 &nbsp; Implementing it"),
  ("callout", "Verify the QFT on a known period before building anything on "
              "it",
   ["<b>Prepare a state whose amplitudes are periodic with a known "
    "r</b>, apply your QFT, and <b>check that the outcome distribution "
    "peaks at multiples of N/r</b> — <b>which is a complete "
    "functional test</b> and takes a few minutes.",
    "<b>And check the inverse</b>: <b>QFT followed by inverse QFT "
    "must be the identity</b> — which catches qubit-ordering "
    "errors — <b>and the final bit-reversal step is where those "
    "errors live</b>, in essentially every first implementation.",
    "<b>Then compare directly against the classical FFT of your "
    "amplitude vector</b> — <b>your simulator has the whole vector, "
    "so you can check the transform exactly, amplitude by "
    "amplitude</b>, <b>which real hardware cannot</b> and which no "
    "amount of sampling would establish.",
    "<b>Which is the practical value of having written "
    "Module 02 &sect;4's simulator yourself:</b> <b>you can inspect "
    "the amplitudes that the model says are unobservable</b> — and "
    "<b>that is how to debug a quantum algorithm before trusting "
    "it</b>, which is the only debugging method available."]),
 ],
 "resources": [
   ("Nielsen & Chuang, chapter 5 (library copy)",
    "https://www.cambridge.org/9781107002173",
    "<b>&sect;&sect;1 and 2</b> — the QFT, its circuit, and phase "
    "estimation, in the standard development."),
   ("Coppersmith &mdash; An approximate Fourier transform useful in "
    "quantum factoring (free)",
    "https://arxiv.org/abs/quant-ph/0201067",
    "<b>&sect;2's approximate version in the original</b> — and the "
    "argument for dropping the small rotations."),
   ("Kitaev, Shen & Vyalyi, the phase estimation chapter",
    "https://bookstore.ams.org/gsm-47/",
    "<b>&sect;1 and Module 08</b> — the cleanest derivation, and "
    "the one that makes the eigenvalue framing central. Library "
    "copy."),
   ("Aaronson &mdash; Read the fine print (free)",
    "https://www.scottaaronson.com/papers/qml.pdf",
    "<b>&sect;3's input problem and non-uses</b> — the standard "
    "reference for what the caveats actually cost, and it should be read "
    "before any quantum machine learning proposal."),
 ],
 "exercises": [
   "<b>Write the QFT matrix</b> for N = 4 and verify it is "
   "unitary.",
   "<b>Apply it by hand</b> to a state with period 2.",
   "<b>State why it is not a faster FFT</b>, in three sentences.",
   "<b>Derive the factorisation</b> that makes the circuit short.",
   "<b>Implement the QFT circuit</b> and compare to the matrix.",
   "<b>Verify QFT then inverse QFT is the identity</b>, and find your "
   "ordering bug.",
   "<b>Implement the approximate QFT</b> and measure the fidelity "
   "loss.",
   "<b>Count gates for both</b> at n = 10, 20, 50.",
   "<b>Test your QFT on three known periods</b> and check the "
   "peaks.",
   "<b>Estimate the cost of loading a classical vector</b> into "
   "amplitudes, and state the consequence.",
 ],
 "selfcheck": [
   "Define the QFT and say what it does to a periodic state.",
   "What is the one sentence to remember?",
   "Why is it not a faster Fourier transform?",
   "Why is that the course's most important caveat?",
   "Why does O(n²) suffice?",
   "What does the approximate QFT drop, and what does it cost?",
   "When does a unitary have an efficient circuit, and why is that "
   "rare?",
   "List the QFT's actual uses.",
   "Why is signal processing not among them?",
   "State the input problem and its consequence.",
 ],
},

]
