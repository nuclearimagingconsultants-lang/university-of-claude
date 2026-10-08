# -*- coding: utf-8 -*-
"""CSCE 640 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Phase Estimation and Shor",
 "subtitle": "The one dramatic result, assembled from parts you "
             "already have.",
 "question": "Why does factoring reduce to finding a period?",
 "outcomes": [
     "Derive phase estimation from the QFT.",
     "Explain the reduction from factoring to order finding.",
     "Assemble Shor's algorithm and state its cost.",
     "Explain what it does and does not break.",
     "State the resource reality for a useful instance.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Phase estimation",
   "blurb": "The QFT used backwards, and the subject's main tool."},

  {"t": "eq", "kicker": "Phase estimation", "title": "The problem and the circuit",
   "eqs": [
     ("given U and an eigenvector |u> with U|u> = e^(2πiφ)|u>, "
      "estimate φ",
      "The eigenvalue's phase is the thing you want. It is not "
      "directly measurable, so it must be moved into amplitudes."),
     ("apply controlled-U^(2^k) with control qubit k in superposition",
      "Phase kickback (Module 03 §3) writes the phase onto the "
      "control register, as e^(2πi·2ᵏφ)."),
     ("then the inverse QFT on the control register, and measure",
      "The control register now holds a periodic phase pattern; the "
      "inverse QFT turns it into a peak at φ, to m bits with m "
      "control qubits."),
   ],
   "caption": "<b>Phase estimation moves an eigenvalue's phase into "
              "a measurable register</b> — and almost every "
              "exponential-advantage algorithm is an instance of "
              "it.",
   "note": "Phase estimation is the general tool; Shor is one "
           "application of it."},

  {"t": "callout", "title": "And period finding is phase estimation on the shift operator",
   "kind": "Why the two are the same thing",
   "body": ["<b>Define U as multiplication by a modulo "
            "N</b> — <b>its eigenvalues have phases that are "
            "multiples of 1/r, where r is the order of a</b>, which is "
            "the period you want.",
            "<b>So estimating the phase estimates a multiple of "
            "1/r</b> — <b>one random multiple per run</b>, exactly "
            "as Simon's algorithm gave one random linear constraint "
            "(Module 05 §3).",
            "<b>And r is recovered by continued "
            "fractions</b> — <b>classical, cheap, and the step that "
            "makes the whole thing work</b> with a constant number of "
            "repetitions.",
            "<b>Which is why the chain QFT → phase estimation → "
            "period finding → factoring is worth seeing as one "
            "thing</b> — it is the subject's single route to "
            "superpolynomial advantage."]},

  {"t": "section", "label": "Part 2", "title": "Factoring reduces to order finding",
   "blurb": "And the reduction is entirely classical."},

  {"t": "code", "kicker": "Reduction", "title": "The classical part of Shor's algorithm",
   "lang": "text", "code": """
  TO FACTOR N:
    1  pick a random a < N
    2  if gcd(a, N) != 1, you are lucky: it is a
       factor. Return it.
    3  find r, the order of a mod N
       (THIS is the quantum part, Part 1)
    4  if r is odd, or a^(r/2) = -1 mod N, restart
    5  otherwise gcd(a^(r/2) - 1, N) is a nontrivial
       factor, with probability at least 1/2

  WHY STEP 5 WORKS
    a^r = 1 mod N, so N divides a^r - 1
        = (a^(r/2) - 1)(a^(r/2) + 1)
    N divides the product but neither factor
    (that is what step 4 ruled out), so it must
    share part of itself with each -- and gcd finds
    the shared part.

  EVERYTHING EXCEPT STEP 3 IS CLASSICAL, and the
  reduction was known before quantum computing.
""",
   "caption": "<b>Everything except order finding is classical, and "
              "the reduction predates quantum computing</b> — the "
              "quantum contribution is one subroutine.",
   "note": "Seeing how small the quantum part is clarifies what was "
           "actually contributed."},

  {"t": "section", "label": "Part 3", "title": "What it breaks",
   "blurb": "Precisely, and no more."},

  {"t": "table", "kicker": "Impact", "title": "What a large fault-tolerant machine would and would not break",
   "header": ["Primitive", "Status", "Why"],
   "widths": [3.3, 2.6, 5.1],
   "rows": [
     ["<b>RSA</b>", "<b>Broken</b>", "<b>Factoring, directly</b>"],
     ["<b>Diffie-Hellman, DSA</b>", "<b>Broken</b>", "<b>Discrete log, same machinery</b>"],
     ["<b>Elliptic curve crypto</b>", "<b>Broken</b>", "<b>Discrete log in a different group</b>"],
     ["<b>AES-256</b>", "<b>Weakened to ~128</b>", "<b>Grover only, and that is survivable</b>"],
     ["<b>SHA-256, SHA-3</b>", "<b>Weakened similarly</b>", "<b>Grover on preimages</b>"],
     ["<b>Lattice and hash signatures</b>", "<b>No known attack</b>", "<b>Which is why they are the replacements</b>"],
   ],
   "footnote": "<b>Symmetric cryptography survives with larger "
               "keys</b> — the break is specific to the "
               "number-theoretic public-key primitives, and the "
               "replacements already exist "
               "(CSCE 711 §13).",
   "note": "The asymmetric/symmetric distinction is the one people "
           "most often lose."},

  {"t": "callout", "title": "And the harvest-now-decrypt-later problem makes this urgent despite the machine not existing",
   "kind": "Why the timeline argument is not reassuring",
   "body": ["<b>Encrypted traffic recorded today can be decrypted "
            "whenever such a machine appears</b> — <b>so anything "
            "that must stay secret for twenty years is already "
            "exposed</b>, if it was sent under RSA or "
            "ECDH.",
            "<b>Which makes migration a present-tense engineering "
            "problem</b>, independent of whether the machine arrives in "
            "ten years or fifty or never.",
            "<b>And the standards exist</b>: "
            "<b>lattice-based key exchange and signatures are "
            "standardised and deployable now</b> "
            "(CSCE 711 §13).",
            "<b>So the honest position is:</b> <b>migrate for the "
            "recorded-traffic reason, not because the machine is "
            "imminent</b> — <b>and do not claim it is imminent in "
            "order to motivate the migration</b>, which has been done "
            "and damages the argument."]},

  {"t": "section", "label": "Part 4", "title": "The resource reality",
   "blurb": "Which is the part the headline omits."},

  {"t": "callout", "title": "Factoring a 2048-bit RSA key needs millions of physical qubits and hours of runtime, on a machine nobody has",
   "kind": "Closing",
   "body": ["<b>The careful published estimates are in the "
            "millions of physical qubits</b> — <b>a few thousand "
            "logical ones times Module 10 §4's "
            "overhead</b> — <b>running for hours</b>, with "
            "assumptions stated.",
            "<b>Against current devices of hundreds of noisy "
            "physical qubits with no error correction</b> — <b>which "
            "is a gap of three to four orders of magnitude</b>, not a "
            "matter of waiting a generation of "
            "hardware.",
            "<b>And the estimates have been falling as the "
            "algorithms and codes improve</b>, which is genuine "
            "progress and is still progress within those "
            "orders of magnitude.",
            "<b>So quote the number rather than the "
            "possibility</b> — <b>which is this course's practice and "
            "is Module 13's requirement</b>: a claim about capability "
            "needs a resource count attached."]},
 ],
 "takeaways": [
   "Phase estimation moves an eigenvalue's phase into a measurable "
   "register, and almost every exponential-advantage algorithm is an "
   "instance of it.",
   "Period finding is phase estimation on the modular multiplication "
   "operator, and r is recovered by continued fractions.",
   "Everything in Shor's algorithm except order finding is classical, and "
   "the reduction predates quantum computing.",
   "RSA, Diffie-Hellman, and elliptic curve cryptography break; symmetric "
   "ciphers and hashes survive with larger parameters.",
   "Harvest-now-decrypt-later makes migration a present-tense problem "
   "regardless of the machine's timeline.",
   "Factoring a 2048-bit key needs millions of physical qubits and hours "
   "— quote the number rather than the possibility.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Phase estimation"),
  ("eq", "given U and |u&gt; with U|u&gt; = "
         "e<super>2&pi;i&phi;</super>|u&gt;, estimate &phi;"),
  ("ul", ["<b>The eigenvalue's phase is the thing you want</b>, and "
          "<b>it is not directly measurable</b> — a global phase is "
          "invisible (Module 02 &sect;1) — <b>so it has to be "
          "moved into amplitudes of a separate register</b> before it "
          "can be read.",
          "<b>Apply controlled-U<super>2<sup>k</sup></super> with "
          "control qubit k held in superposition</b>: <b>phase kickback "
          "(Module 03 &sect;3) writes "
          "e<super>2&pi;i&middot;2<sup>k</sup>&phi;</super> onto that "
          "control qubit</b>, leaving the eigenvector untouched — "
          "which is why |u&gt; being an eigenvector is the whole "
          "trick.",
          "<b>The control register now holds a phase pattern that is "
          "periodic in &phi;</b> — <b>so the inverse QFT turns it "
          "into a peak</b>, and <b>measuring gives &phi; to m bits with "
          "m control qubits</b> (Module 07 &sect;1's "
          "period-becomes-peak, used in the direction that extracts the "
          "answer).",
          "<b>Phase estimation moves an eigenvalue's phase into a "
          "measurable register</b> — and <b>almost every "
          "exponential-advantage algorithm in the subject is an instance "
          "of it</b>, which is why it rather than Shor is the thing to "
          "learn. <b>Phase estimation is the general tool; Shor is one "
          "application of it.</b>"]),
  ("callout", "And period finding is phase estimation on the shift operator",
   ["<b>Define U as multiplication by a modulo N</b> — the map "
    "|x&gt; &rarr; |ax mod N&gt; — and <b>its eigenvalues have "
    "phases that are multiples of 1/r, where r is the multiplicative "
    "order of a</b>, <b>which is exactly the period you want</b>.",
    "<b>So estimating the phase estimates a multiple of 1/r</b> "
    "— <b>one random multiple per run</b> — <b>exactly as "
    "Simon's algorithm returned one random linear constraint per "
    "run</b> (Module 05 &sect;3), which is why Simon was worth "
    "studying first.",
    "<b>And r is recovered from that estimate by continued "
    "fractions</b> — <b>classical, cheap, and the step that makes "
    "the whole thing work</b> with only a constant expected number of "
    "repetitions rather than many.",
    "<b>Which is why the chain QFT &rarr; phase estimation &rarr; "
    "period finding &rarr; factoring is worth seeing as a single "
    "thing</b> rather than four topics — <b>it is the subject's one "
    "route to a superpolynomial advantage</b>, and everything else in "
    "Module 01 &sect;3's list is either simulation or "
    "quadratic."]),

  ("h1", "2 &nbsp; Factoring reduces to order finding"),
  ("code", """TO FACTOR N:
  1  pick a random a < N
  2  if gcd(a, N) != 1, you are lucky: it is a
     factor. Return it.
  3  find r, the multiplicative order of a mod N
     (THIS is the quantum part, section 1)
  4  if r is odd, or a^(r/2) = -1 mod N, restart
  5  otherwise gcd(a^(r/2) - 1, N) is a nontrivial
     factor, with probability at least 1/2

WHY STEP 5 WORKS
  a^r = 1 mod N, so N divides a^r - 1
      = (a^(r/2) - 1)(a^(r/2) + 1)
  N divides the product but neither factor
  (that is what step 4 ruled out), so N must share
  part of itself with each -- and gcd finds the
  shared part.

EVERYTHING EXCEPT STEP 3 IS CLASSICAL, and the
reduction was known before quantum computing."""),
  ("p", "<b>Everything except order finding is classical, and the "
        "reduction predates quantum computing</b> — <b>the quantum "
        "contribution is exactly one subroutine</b>. <b>Seeing how "
        "small the quantum part is clarifies what was actually "
        "contributed</b>: not a new way of thinking about factoring, but "
        "an efficient method for a single number-theoretic subproblem "
        "that was already known to suffice. It also shows why a fault in "
        "step 3 is detectable: the classical steps verify the answer in "
        "a few multiplications."),

  ("break",),
  ("h1", "3 &nbsp; What it breaks"),
  ("table", ["Primitive", "Status under a large fault-tolerant machine",
             "Why"],
   [["<b>RSA</b>", "<b>Broken.</b>", "<b>Factoring, directly.</b>"],
    ["<b>Diffie-Hellman and DSA</b>", "<b>Broken.</b>",
     "<b>Discrete logarithm, by the same phase-estimation "
     "machinery.</b>"],
    ["<b>Elliptic curve cryptography</b>", "<b>Broken.</b>",
     "<b>Discrete logarithm in a different group</b>, and with "
     "<i>smaller</i> resource requirements than RSA."],
    ["<b>AES-256</b>", "<b>Weakened to roughly 128-bit "
     "security.</b>",
     "<b>Grover only</b> (Module 06) — <b>and that is entirely "
     "survivable</b> by using larger keys."],
    ["<b>SHA-256 and SHA-3</b>", "<b>Weakened similarly.</b>",
     "<b>Grover on preimages; collision resistance is affected "
     "less.</b>"],
    ["<b>Lattice-based and hash-based signatures</b>",
     "<b>No known quantum attack.</b>",
     "<b>Which is precisely why they are the standardised "
     "replacements</b> (CSCE 711 Module 13)."]],
   [0.26, 0.30, 0.44]),
  ("p", "<b>Symmetric cryptography survives with larger "
        "keys</b> — <b>the break is specific to the "
        "number-theoretic public-key primitives</b>, <b>and the "
        "replacements already exist and are standardised</b>. <b>The "
        "asymmetric/symmetric distinction is the one people most often "
        "lose</b>, and 'quantum computers will break all encryption' is "
        "wrong in a way that matters: it suggests nothing can be done, "
        "when in fact the migration path is specified."),
  ("callout", "And the harvest-now-decrypt-later problem makes this urgent "
              "despite the machine not existing",
   ["<b>Encrypted traffic recorded today can be decrypted whenever "
    "such a machine appears</b> — <b>so anything that must stay "
    "secret for twenty years is already exposed</b>, if it was sent "
    "under RSA or ECDH key exchange, and recording is cheap.",
    "<b>Which makes migration a present-tense engineering "
    "problem</b>, <b>independent of whether the machine arrives in ten "
    "years, in fifty, or never</b> — and that independence is what "
    "makes the argument robust.",
    "<b>And the standards exist</b>: <b>lattice-based key "
    "encapsulation and both lattice- and hash-based signatures are "
    "standardised and deployable now</b> (CSCE 711 Module 13's "
    "post-quantum section), with hybrid deployments already "
    "common.",
    "<b>So the honest position is:</b> <b>migrate for the "
    "recorded-traffic reason, not because the machine is "
    "imminent</b> — and <b>do not claim it is imminent in order to "
    "motivate the migration</b>, <b>which has been done</b> and which "
    "damages the argument's credibility when the predicted date "
    "passes."]),

  ("h1", "4 &nbsp; The resource reality"),
  ("callout", "Factoring a 2048-bit RSA key needs millions of physical "
              "qubits and hours of runtime, on a machine nobody has",
   ["<b>The careful published estimates are in the millions of "
    "physical qubits</b> — <b>a few thousand logical qubits "
    "multiplied by Module 10 &sect;4's error-correction "
    "overhead</b> — <b>running for hours</b>, with the "
    "architectural assumptions stated explicitly, which is what makes "
    "those papers worth reading.",
    "<b>Against current devices of hundreds of noisy physical qubits "
    "with no useful error correction</b> — <b>which is a gap of "
    "three to four orders of magnitude in qubit count</b>, <b>not a "
    "matter of waiting one more hardware generation.</b>",
    "<b>And the estimates have been falling steadily as the "
    "algorithms, the codes, and the magic-state factories "
    "improve</b> — <b>which is genuine progress</b>, and <b>is "
    "still progress within those orders of magnitude</b> rather than "
    "across them.",
    "<b>So quote the number rather than the possibility</b> — "
    "<b>which is this course's practice throughout and is "
    "Module 13's explicit requirement</b>: <b>a claim about "
    "capability needs a resource count attached</b>, and a claim without "
    "one is not checkable."]),
 ],
 "resources": [
   ("Shor &mdash; Polynomial-time algorithms for prime factorization "
    "and discrete logarithms (free)",
    "https://arxiv.org/abs/quant-ph/9508027",
    "<b>&sect;&sect;1 and 2 in the original</b> — and it is "
    "readable, which is not true of every landmark paper."),
   ("Kitaev &mdash; Quantum measurements and the abelian stabilizer "
    "problem (free)",
    "https://arxiv.org/abs/quant-ph/9511026",
    "<b>&sect;1</b> — phase estimation in the framing that makes it "
    "the general tool rather than a step in Shor."),
   ("Gidney & Ekerå &mdash; How to factor 2048 bit RSA integers "
    "in 8 hours (free)",
    "https://quantum-journal.org/papers/q-2021-04-15-433/",
    "<b>&sect;4's numbers</b> — the careful estimate, with every "
    "assumption stated. This is the paper to cite."),
   ("NIST post-quantum cryptography standards (free)",
    "https://csrc.nist.gov/projects/post-quantum-cryptography",
    "<b>&sect;3's replacements</b> — the standardised algorithms and "
    "the migration guidance."),
 ],
 "exercises": [
   "<b>State the phase estimation problem</b> and its circuit.",
   "<b>Show where phase kickback enters</b>, explicitly.",
   "<b>Implement phase estimation</b> for a single-qubit U with known "
   "eigenvalue.",
   "<b>Verify the precision</b> against the number of control "
   "qubits.",
   "<b>Find the order of several a mod N</b> classically, and check "
   "the reduction's steps.",
   "<b>Prove step 5</b> of the reduction in your own words.",
   "<b>Run Shor's algorithm</b> on N = 15 and N = 21 in simulation.",
   "<b>Classify ten cryptographic primitives</b> as broken, weakened, "
   "or unaffected.",
   "<b>State the harvest-now argument</b> and its independence from "
   "the timeline.",
   "<b>Read the 2048-bit estimate</b> and list its three strongest "
   "assumptions.",
 ],
 "selfcheck": [
   "State the phase estimation problem and the three circuit steps.",
   "Why must the input be an eigenvector?",
   "How is period finding an instance of it?",
   "How is r recovered, and how many runs are needed?",
   "Give the factoring reduction, and say which step is quantum.",
   "Why does the gcd step produce a factor?",
   "Name three broken primitives and three that survive.",
   "What is the distinction people most often lose?",
   "State the harvest-now-decrypt-later argument.",
   "Give the resource estimate and the current gap.",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Quantum Simulation",
 "subtitle": "The original proposal, and the likeliest application.",
 "question": "What is a quantum computer actually for?",
 "outcomes": [
     "Explain why classical simulation of quantum systems is hard.",
     "Explain Hamiltonian simulation and Trotterisation.",
     "Explain the chemistry and materials applications.",
     "State the resource requirements honestly.",
     "Explain why this is the least speculative application.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The original argument",
   "blurb": "Which is the cleanest motivation in the subject."},

  {"t": "callout", "title": "Simulating a quantum system classically appears to cost exponentially, so use a quantum system",
   "kind": "Feynman's proposal, and it is still the best one",
   "body": ["<b>The state of m interacting particles needs "
            "exponentially many amplitudes</b> — <b>which is exactly "
            "the wall your simulator hit in "
            "Module 02 §4.</b>",
            "<b>So classical simulation of chemistry and materials "
            "is limited to small systems or to "
            "approximations</b> — <b>and the approximations fail "
            "precisely where the interesting physics is</b>, which is "
            "strong correlation.",
            "<b>And a quantum device has the same state space "
            "natively</b> — <b>so it represents the system without "
            "the exponential cost</b>, which is a structural fit rather "
            "than a clever algorithm.",
            "<b>Which is why this is the least speculative "
            "application</b>: <b>no problem structure had to be "
            "discovered, because the machine is the same kind of thing "
            "as the problem.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Hamiltonian simulation",
   "blurb": "How a physical evolution becomes a circuit."},

  {"t": "eq", "kicker": "Simulation", "title": "Evolution, and how to approximate it",
   "eqs": [
     ("goal: implement U(t) = e^(−iHt) for a given Hamiltonian H",
      "The time evolution operator. H is typically a sum of local "
      "terms — which is what makes this tractable."),
     ("Trotter: e^(−i(A+B)t) ≈ (e^(−iAt/n) e^(−iBt/n))ⁿ",
      "Exact as n grows; the error is O(t²/n) from the "
      "commutator of A and B. Each small factor is a short circuit."),
     ("newer methods: qubitisation, LCU, and QSP do better in n and ε",
      "Near-optimal scaling, at the cost of ancillas and complexity. "
      "This is an active and genuinely improving area."),
   ],
   "caption": "<b>Trotterisation turns a physical evolution into a "
              "product of short circuits</b>, and the error comes from "
              "the terms that do not commute.",
   "note": "Trotter is the simple method; qubitisation is what is "
           "actually used in current estimates."},

  {"t": "callout", "title": "And the locality of the Hamiltonian is what makes this possible at all",
   "kind": "Why not every unitary can be simulated",
   "body": ["<b>A physical Hamiltonian is a sum of terms each acting "
            "on a few particles</b> — <b>so each term's exponential "
            "is a small circuit</b>, and the product is "
            "polynomial.",
            "<b>Which is a special structure, not a general "
            "fact</b> — <b>a generic Hamiltonian on m particles has "
            "no short circuit</b> (Module 03 §1's "
            "counting argument again).",
            "<b>So 'quantum computers simulate quantum systems' is "
            "true for <i>local</i> Hamiltonians</b>, which happily is "
            "what physics provides.",
            "<b>And that is the pattern of this whole "
            "course:</b> <b>structure makes a circuit short, and the "
            "structure has to come from the problem</b> "
            "(Module 07 §2)."]},

  {"t": "section", "label": "Part 3", "title": "What it would be used for",
   "blurb": "Concretely, and with the caveats attached."},

  {"t": "bullets", "kicker": "Applications", "title": "The candidate problems, and what each needs",
   "items": [
     "<b>Ground state energies of molecules</b> — "
     "<b>catalysis, nitrogen fixation, battery chemistry</b> — "
     "<b>and the hard cases are strongly correlated systems where "
     "classical methods are least reliable.</b>",
     "",
     "<b>Which needs phase estimation</b> "
     "(Module 08 §1) <b>on the molecular "
     "Hamiltonian</b>, plus a good enough initial state — and "
     "<b>preparing one is itself hard</b>.",
     "",
     "<b>Materials: superconductivity, magnetism, correlated "
     "electron systems</b> — where the models are simple to "
     "state and intractable to solve.",
     "",
     "<b>And dynamics rather than ground "
     "states</b> — <b>reaction mechanisms and transport</b>, "
     "which is where Part 2's machinery applies most "
     "directly.",
     "",
     "<b>But note the honest comparison:</b> <b>classical methods "
     "have improved substantially too</b>, and the crossover point is "
     "contested (Module 13 §3).",
   ],
   "footnote": "<b>Preparing a good enough initial state is itself "
               "hard</b> — phase estimation needs overlap with the "
               "true ground state, and guaranteeing that is an open "
               "problem."},

  {"t": "section", "label": "Part 4", "title": "The resources",
   "blurb": "Which are large but smaller than Shor's."},

  {"t": "callout", "title": "Useful chemistry needs hundreds to thousands of logical qubits, which is still far away and closer than factoring",
   "kind": "Closing",
   "body": ["<b>Published estimates for industrially relevant "
            "molecules sit in the hundreds to low thousands of logical "
            "qubits</b>, with deep circuits — <b>and the estimates "
            "have fallen by orders of magnitude over a "
            "decade</b>.",
            "<b>Which is a smaller requirement than factoring</b> "
            "(Module 08 §4) — <b>so if anything "
            "useful runs first, this is "
            "it.</b>",
            "<b>And the value is scientific rather than "
            "cryptographic</b>: <b>a better catalyst is worth more "
            "than a broken cipher</b>, and does not require anybody to "
            "lose anything.",
            "<b>So when asked what quantum computers are for, this "
            "is the honest answer</b> — <b>and it is the one Feynman "
            "gave before the cryptographic application was "
            "found.</b>"]},
 ],
 "takeaways": [
   "Classical simulation of m interacting quantum particles costs "
   "exponentially, which is the wall your own simulator hit.",
   "A quantum device has the same state space natively, so this is a "
   "structural fit rather than a discovered algorithm.",
   "Trotterisation turns a physical evolution into a product of short "
   "circuits, with error from the non-commuting terms.",
   "Locality of the Hamiltonian is what makes the circuit short; a generic "
   "Hamiltonian has no short circuit.",
   "Preparing an initial state with enough overlap with the true ground "
   "state is itself hard and is an open problem.",
   "Useful chemistry needs hundreds to thousands of logical qubits — "
   "far away, and closer than factoring.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The original argument"),
  ("callout", "Simulating a quantum system classically appears to cost "
              "exponentially, so use a quantum system",
   ["<b>The state of m interacting quantum particles requires "
    "exponentially many amplitudes to write down</b> — <b>which is "
    "exactly the wall your own simulator hit in Module 02 "
    "&sect;4</b>, and meeting it personally on a laptop is the best "
    "preparation for this module.",
    "<b>So classical simulation of chemistry and materials is "
    "restricted to small systems or to approximations</b> — "
    "<b>and the approximations fail precisely where the interesting "
    "physics is</b>, <b>which is strong electron correlation</b>: the "
    "mean-field methods that work well are the ones that assume the "
    "correlation away.",
    "<b>And a quantum device has the same state space "
    "natively</b> — <b>so it represents the system without the "
    "exponential overhead</b> — <b>which is a structural fit "
    "rather than a clever algorithm</b>, and needs no hidden periodicity "
    "or engineered cancellation to work.",
    "<b>Which is why this is the least speculative application in "
    "the subject</b>: <b>no problem structure had to be discovered, "
    "because the machine is the same kind of thing as the problem</b> "
    "(Module 01 &sect;3's first item, now with its "
    "justification)."]),

  ("h1", "2 &nbsp; Hamiltonian simulation"),
  ("eq", "goal: implement U(t) = e<super>&minus;iHt</super> for a given "
         "Hamiltonian H"),
  ("ul", ["<b>U(t) is the time evolution operator</b>, and <b>H is "
          "typically a sum of local terms</b> — each acting on only "
          "a few particles — <b>which is what makes the whole thing "
          "tractable</b> (&sect;2's callout).",
          "<b>Trotter: e<super>&minus;i(A+B)t</super> &asymp; "
          "(e<super>&minus;iAt/n</super> "
          "e<super>&minus;iBt/n</super>)<sup>n</sup></b> — "
          "<b>exact in the limit of large n</b>, with <b>error of order "
          "t<super>2</super>/n arising from the commutator of A and "
          "B</b> — <b>and each small factor is a short "
          "circuit</b> because each term is local.",
          "<b>Newer methods — qubitisation, linear combination "
          "of unitaries, and quantum signal processing — achieve "
          "near-optimal scaling in both the simulation time and the "
          "accuracy</b>, <b>at the cost of ancilla qubits and "
          "considerable implementation complexity</b>. <b>This is an "
          "active and genuinely improving area</b>, which is unusual in "
          "a field where the headline algorithms are thirty years "
          "old.",
          "<b>Trotter is the simple method to understand; "
          "qubitisation is what is actually used in current resource "
          "estimates</b>, and the difference between them is a large "
          "part of why &sect;4's numbers have fallen."]),
  ("callout", "And the locality of the Hamiltonian is what makes this "
              "possible at all",
   ["<b>A physical Hamiltonian is a sum of terms each acting on a few "
    "particles</b> — nearest-neighbour couplings, two-electron "
    "integrals — <b>so each term's exponential is a small "
    "circuit</b>, <b>and the product of polynomially many small "
    "circuits is a polynomial-size circuit.</b>",
    "<b>Which is a special structure rather than a general "
    "fact</b> — <b>a generic Hamiltonian on m particles has no "
    "short circuit for its evolution</b> — <b>which is "
    "Module 03 &sect;1's counting argument arriving yet again</b>, "
    "in its third setting.",
    "<b>So the slogan 'quantum computers simulate quantum systems' "
    "is true for <i>local</i> Hamiltonians</b>, <b>which happily is "
    "what physics actually provides</b> — but the qualifier is "
    "doing real work and should be stated.",
    "<b>And that is the pattern of this entire course:</b> "
    "<b>structure makes a circuit short, and the structure has to come "
    "from the problem</b> (Module 07 &sect;2's factorisation point, "
    "Module 04 &sect;1's cancellation point) — three different "
    "modules, one observation."]),

  ("break",),
  ("h1", "3 &nbsp; What it would be used for"),
  ("ul", ["<b>Ground state energies of molecules</b> — "
          "<b>catalysis, nitrogen fixation, battery electrolytes, "
          "enzyme mechanisms</b> — <b>and the hard cases are "
          "precisely the strongly correlated systems where classical "
          "methods are least reliable</b>, which is the right place for "
          "a new tool to be useful.",
          "<b>Which needs phase estimation</b> (Module 08 "
          "&sect;1) <b>applied to the molecular Hamiltonian</b>, <b>plus "
          "an initial state with non-negligible overlap with the true "
          "ground state</b> — and <b>preparing one is itself "
          "hard</b>: <b>phase estimation needs that overlap, and "
          "guaranteeing it in general is an open problem</b> (the "
          "ground-state preparation problem is QMA-hard in general, "
          "which is a real obstacle rather than an engineering "
          "detail).",
          "<b>Materials: superconductivity, frustrated magnetism, "
          "correlated electron systems</b> — <b>where the models "
          "are simple to state and intractable to solve</b>, which is "
          "the clearest sign that the difficulty is computational rather "
          "than conceptual.",
          "<b>And dynamics rather than ground states</b> — "
          "<b>reaction mechanisms, transport, non-equilibrium "
          "behaviour</b> — <b>which is where &sect;2's machinery "
          "applies most directly</b>, since it is literally time "
          "evolution.",
          "<b>But note the honest comparison:</b> <b>classical "
          "methods (tensor networks, quantum Monte Carlo, modern density "
          "functional approaches) have improved substantially "
          "too</b>, <b>and the crossover point is genuinely "
          "contested</b> (Module 13 &sect;3) — which is a reason "
          "for specificity rather than for pessimism."]),

  ("h1", "4 &nbsp; The resources"),
  ("callout", "Useful chemistry needs hundreds to thousands of logical "
              "qubits, which is still far away and closer than factoring",
   ["<b>Published estimates for industrially relevant molecules sit "
    "in the hundreds to low thousands of logical qubits</b>, with deep "
    "circuits and long runtimes — <b>and the estimates have fallen "
    "by orders of magnitude over roughly a decade</b> as the simulation "
    "methods and the compilation improved.",
    "<b>Which is a materially smaller requirement than "
    "factoring</b> (Module 08 &sect;4's few thousand logical qubits "
    "with very deep circuits) — <b>so if anything useful runs "
    "first, this is it</b>, which is a reasonable prediction rather than "
    "a safe one.",
    "<b>And the value is scientific rather than "
    "cryptographic</b>: <b>a better catalyst for fertiliser production "
    "is worth more than a broken cipher</b>, <b>and it does not require "
    "anybody to lose anything</b> — which makes it a better thing "
    "to build a field's justification on.",
    "<b>So when asked what quantum computers are for, this is the "
    "honest answer</b> — <b>and it is the one Feynman gave in 1982, "
    "before the cryptographic application was found</b> and before the "
    "subject acquired its current framing."]),
 ],
 "resources": [
   ("Feynman &mdash; Simulating Physics with Computers",
    "https://link.springer.com/article/10.1007/BF02650179",
    "<b>&sect;1 in the original</b> — the proposal, and it is worth "
    "reading for how carefully he states the difficulty."),
   ("Lloyd &mdash; Universal quantum simulators",
    "https://www.science.org/doi/10.1126/science.273.5278.1073",
    "<b>&sect;2</b> — the Trotterisation argument that turned the "
    "proposal into an algorithm."),
   ("Low & Chuang &mdash; Hamiltonian simulation by qubitization "
    "(free)",
    "https://quantum-journal.org/papers/q-2019-07-12-163/",
    "<b>&sect;2's modern method</b> — near-optimal, and what current "
    "resource estimates assume."),
   ("Reiher et al. &mdash; Elucidating reaction mechanisms on quantum "
    "computers (free)",
    "https://www.pnas.org/doi/10.1073/pnas.1619152114",
    "<b>&sect;&sect;3 and 4</b> — a concrete application with a full "
    "resource estimate, which is the model for how this should be "
    "reported."),
 ],
 "exercises": [
   "<b>State the exponential-cost argument</b> and relate it to your "
   "own simulator's ceiling.",
   "<b>Explain where classical approximations fail</b>, and why that "
   "is the interesting region.",
   "<b>Derive the Trotter error</b> for two non-commuting terms.",
   "<b>Implement Trotterised evolution</b> for a two-qubit "
   "Hamiltonian.",
   "<b>Measure the error against n</b> and check the predicted "
   "scaling.",
   "<b>Find a Hamiltonian whose terms commute</b>, and say why Trotter "
   "is exact there.",
   "<b>Explain why locality matters</b>, using the counting "
   "argument.",
   "<b>Read one chemistry resource estimate</b> and list its "
   "assumptions.",
   "<b>State the state-preparation problem</b> and why it is not a "
   "detail.",
   "<b>Compare a classical method's current reach</b> to the quantum "
   "estimate for the same molecule.",
 ],
 "selfcheck": [
   "State Feynman's argument.",
   "Where do classical approximations fail, and why does that matter?",
   "Why is this the least speculative application?",
   "Give the Trotter formula and the source of its error.",
   "Name the newer methods and what they buy.",
   "Why does locality make the circuit short?",
   "What is the general pattern this illustrates?",
   "Name four application areas.",
   "State the state-preparation obstacle.",
   "Give the resource estimate, and compare to factoring.",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Noise and Error Correction",
 "subtitle": "Why this is hard, and why it is nonetheless possible.",
 "question": "You cannot copy a qubit. So how do you correct it?",
 "outcomes": [
     "Describe the error model and why it is continuous.",
     "Explain how a quantum code corrects without measuring data.",
     "State the threshold theorem and what it establishes.",
     "State the overhead, numerically.",
     "Read a resource estimate critically.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The error model",
   "blurb": "Which looks worse than it is."},

  {"t": "callout", "title": "Errors are continuous, but correcting the Pauli basis corrects everything",
   "kind": "The result that makes quantum error correction possible",
   "body": ["<b>A qubit can be rotated by any small "
            "angle</b> — <b>so the error set is continuous</b>, "
            "which appears to rule out the discrete correction that "
            "classical codes rely on.",
            "<b>But any single-qubit error decomposes into "
            "I, X, Y, Z</b> — <b>and the syndrome measurement "
            "projects the error onto that basis</b>, which "
            "<i>discretises</i> it.",
            "<b>So correcting bit flips (X) and phase flips (Z) "
            "corrects arbitrary single-qubit errors</b> — which is "
            "the central and genuinely surprising "
            "fact.",
            "<b>And phase flips are the new "
            "problem</b> — <b>classical codes have no analogue</b>, "
            "because classical bits have no phase; this is what the "
            "quantum codes had to invent."]},

  {"t": "section", "label": "Part 2", "title": "Correcting without looking",
   "blurb": "The trick that gets around no-cloning."},

  {"t": "code", "kicker": "Stabilisers", "title": "How a syndrome is measured without disturbing the data",
   "lang": "text", "code": """
  THE PROBLEM
      measuring the data destroys the superposition
      (Module 02), and no-cloning forbids copies.

  THE TRICK
      measure PARITIES, not values.
      "do qubits 1 and 2 agree?" is a question whose
      answer does not reveal what either one is.

  SO
      encode one logical qubit across many physical
      ones, in a subspace defined by a set of
      commuting parity operators (stabilisers)
      measure those operators repeatedly
      an error moves the state out of the subspace
      and the parity pattern (the syndrome) says
      which error, without ever naming the state

  THE SURFACE CODE
      stabilisers are local on a 2D grid, which is
      why hardware likes it. Distance d corrects
      (d-1)/2 errors and costs about d^2 physical
      qubits per logical one.
""",
   "caption": "<b>Measure parities, not values</b> — a parity "
              "answer carries no information about the individual "
              "amplitudes, so the superposition "
              "survives.",
   "note": "Parity-not-value is the single idea behind every "
           "quantum code."},

  {"t": "section", "label": "Part 3", "title": "The threshold theorem",
   "blurb": "The result the entire field rests on."},

  {"t": "callout", "title": "Below a threshold physical error rate, arbitrarily long computations are possible with polylogarithmic overhead",
   "kind": "Why this is a field and not a curiosity",
   "body": ["<b>Concatenate a code with itself and the logical error "
            "rate falls doubly exponentially while the overhead grows "
            "only exponentially</b> — <b>so below some "
            "rate, correction wins.</b>",
            "<b>Which establishes that noise is not a fundamental "
            "obstacle</b> — <b>it is an engineering "
            "one</b>, and before this result it was not clear which "
            "it was.",
            "<b>The threshold is roughly 1% for the surface code</b> "
            "under favourable assumptions — <b>and current hardware is "
            "at or near it</b>, which is the real progress of the last "
            "decade.",
            "<b>But 'above threshold' is the beginning rather than "
            "the end</b> — <b>the overhead at a rate just below "
            "threshold is enormous</b>, and that is "
            "Part 4."]},

  {"t": "section", "label": "Part 4", "title": "The overhead",
   "blurb": "The number that governs every resource estimate."},

  {"t": "bullets", "kicker": "Overhead", "title": "What error correction actually costs",
   "items": [
     "<b>Roughly a thousand physical qubits per logical "
     "qubit</b>, at plausible error rates with the surface "
     "code — <b>and it rises steeply as the physical rate "
     "approaches the threshold.</b>",
     "",
     "<b>Plus magic state distillation for T "
     "gates</b> (Module 03 §1) — <b>which "
     "frequently dominates the entire footprint</b>, and is why "
     "T-count is the metric.",
     "",
     "<b>And the syndrome must be measured continuously</b>, "
     "faster than errors accumulate — <b>so classical decoding "
     "throughput is itself a hard engineering "
     "requirement.</b>",
     "",
     "<b>Which is where Module 08 §4's millions of "
     "physical qubits come from</b>: thousands of logical, times a "
     "thousand, plus the distillation "
     "factories.",
     "",
     "<b>So every resource estimate is really an estimate about "
     "error correction</b> — and reading one means reading its "
     "assumed physical error rate first.",
   ],
   "footnote": "<b>Read the assumed physical error rate "
               "first</b> — it drives the overhead non-linearly, "
               "and it is the assumption that varies most between "
               "papers."},

  {"t": "callout", "title": "And this is where the honest optimism lives",
   "kind": "Closing",
   "body": ["<b>The threshold theorem is a real result and it is "
            "good news</b> — <b>it says the problem is solvable in "
            "principle</b>, which was genuinely open before it was "
            "proved.",
            "<b>And the experimental progress is real:</b> "
            "<b>error rates have fallen steadily, and logical qubits "
            "outperforming their physical constituents have been "
            "demonstrated</b>, which is the milestone that "
            "mattered.",
            "<b>While the gap to a useful machine remains three to "
            "four orders of magnitude in qubit "
            "count</b> (Module 08 §4) — <b>and both of those "
            "statements are true at once.</b>",
            "<b>Which is the posture this course "
            "asks for</b> — <b>neither 'it will never work' nor 'it "
            "is nearly here'</b>, both of which are claims made without "
            "the resource counts that would settle "
            "them."]},
 ],
 "takeaways": [
   "Errors are continuous, but the syndrome measurement projects them onto "
   "the Pauli basis, which discretises them.",
   "Phase flips are the new problem: classical codes have no analogue "
   "because classical bits have no phase.",
   "Measure parities, not values — a parity answer reveals nothing "
   "about the individual amplitudes, so the superposition survives.",
   "The threshold theorem establishes that noise is an engineering obstacle "
   "rather than a fundamental one.",
   "Roughly a thousand physical qubits per logical one, plus magic state "
   "distillation, which frequently dominates.",
   "Read a resource estimate's assumed physical error rate first; it drives "
   "the overhead non-linearly.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The error model"),
  ("callout", "Errors are continuous, but correcting the Pauli basis corrects "
              "everything",
   ["<b>A qubit can be rotated by any small angle, and can decohere "
    "partially</b> — <b>so the error set is a continuum</b>, "
    "<b>which appears to rule out the discrete correction that every "
    "classical code relies on</b>, and was the reason many people "
    "initially believed quantum error correction impossible.",
    "<b>But any single-qubit error decomposes into a combination of "
    "I, X, Y, and Z</b> — they span the space of single-qubit "
    "operators — <b>and the syndrome measurement projects the error "
    "onto that basis</b>, <b>which <i>discretises</i> it</b>: a small "
    "rotation becomes, with high probability, no error at all, and "
    "occasionally a full X or Z.",
    "<b>So correcting bit flips (X) and phase flips (Z) corrects "
    "arbitrary single-qubit errors</b> — <b>which is the central "
    "and genuinely surprising fact of this module</b>, and the one that "
    "made the field possible.",
    "<b>And phase flips are the new problem</b> — <b>classical "
    "codes have no analogue</b>, because classical bits have no "
    "phase — <b>which is what the quantum codes had to "
    "invent</b>, and why Shor's nine-qubit code and its successors look "
    "unlike classical repetition codes."]),

  ("h1", "2 &nbsp; Correcting without looking"),
  ("code", """THE PROBLEM
    measuring the data destroys the superposition
    (Module 02), and no-cloning forbids making
    copies to compare.

THE TRICK
    measure PARITIES, not values.
    "do qubits 1 and 2 agree?" is a question whose
    answer does not reveal what either one is.

SO
    encode one logical qubit across many physical
    ones, in a subspace defined by a set of
    commuting parity operators (stabilisers)
    measure those operators repeatedly
    an error moves the state out of the subspace
    and the parity pattern (the syndrome) says which
    error occurred, without ever naming the state

THE SURFACE CODE
    stabilisers are local on a 2D grid, which is why
    hardware likes it. Distance d corrects (d-1)/2
    errors and costs about d^2 physical qubits per
    logical one."""),
  ("p", "<b>Measure parities, not values</b> — <b>a parity "
        "answer carries no information about the individual amplitudes, "
        "so the superposition survives the measurement</b>. <b>This is "
        "the single idea behind every quantum code</b>, and it is worth "
        "checking by hand on the three-qubit bit-flip code: the parity of "
        "qubits 1 and 2, and of 2 and 3, together identify which qubit "
        "flipped, and neither parity says anything about whether the "
        "logical state was 0, 1, or a superposition. The surface code's "
        "locality is what makes it the hardware favourite: every "
        "stabiliser involves only neighbouring qubits on a grid."),

  ("break",),
  ("h1", "3 &nbsp; The threshold theorem"),
  ("callout", "Below a threshold physical error rate, arbitrarily long "
              "computations are possible with polylogarithmic overhead",
   ["<b>Concatenate a code with itself and the logical error rate "
    "falls doubly exponentially in the number of levels, while the "
    "overhead grows only exponentially</b> — <b>so below some "
    "physical error rate, correction wins</b>, and above it, each level "
    "of encoding makes things worse.",
    "<b>Which establishes that noise is not a fundamental "
    "obstacle</b> — <b>it is an engineering one</b> — and "
    "<b>before this result it was genuinely unclear which it was</b>, "
    "with serious people arguing that quantum computing was impossible "
    "in principle.",
    "<b>The threshold is roughly 1% for the surface code</b> under "
    "favourable assumptions about the noise model and the measurement "
    "speed — <b>and current hardware is at or near it</b>, <b>which "
    "is the real experimental progress of the last decade</b> and the "
    "thing worth tracking.",
    "<b>But 'above threshold' is the beginning rather than the "
    "end</b> — <b>the overhead at a physical rate only just below "
    "threshold is enormous</b>, because the code distance required grows "
    "rapidly as the margin shrinks — <b>and that is &sect;4.</b>"]),

  ("h1", "4 &nbsp; The overhead"),
  ("ul", ["<b>Roughly a thousand physical qubits per logical "
          "qubit</b>, at plausible near-term error rates with the "
          "surface code — <b>and it rises steeply as the physical "
          "rate approaches the threshold</b>, which is why a factor-of-"
          "two improvement in physical error rate can be worth far more "
          "than a factor of two in qubit count.",
          "<b>Plus magic state distillation for the T gates</b> "
          "(Module 03 &sect;1) — <b>which frequently dominates "
          "the entire footprint of a fault-tolerant circuit</b>, since "
          "T gates cannot be done transversally and each one consumes a "
          "distilled resource state — <b>and is why T-count rather "
          "than gate count is the metric.</b>",
          "<b>And the syndrome must be measured continuously and "
          "decoded faster than errors accumulate</b> — <b>so "
          "classical decoding throughput is itself a hard real-time "
          "engineering requirement</b>, and is an active research area "
          "in its own right.",
          "<b>Which is where Module 08 &sect;4's millions of "
          "physical qubits come from</b>: a few thousand logical qubits, "
          "times about a thousand, <b>plus the distillation "
          "factories</b>, which in some designs occupy most of the "
          "chip.",
          "<b>So every resource estimate is really an estimate about "
          "error correction</b> — and <b>reading one means reading "
          "its assumed physical error rate first</b>, <b>because that "
          "assumption drives the overhead non-linearly and is the "
          "parameter that varies most between papers.</b>"]),
  ("callout", "And this is where the honest optimism lives",
   ["<b>The threshold theorem is a real result and it is good "
    "news</b> — <b>it says the problem is solvable in "
    "principle</b>, <b>which was genuinely open before it was "
    "proved</b> and is the single most important theorem for the "
    "field's existence.",
    "<b>And the experimental progress is real:</b> <b>physical "
    "error rates have fallen steadily over two decades, and logical "
    "qubits that outperform their physical constituents have now been "
    "demonstrated</b> — <b>which is the milestone that actually "
    "mattered</b>, and it was not obvious it would arrive when it "
    "did.",
    "<b>While the gap to a useful machine remains three to four "
    "orders of magnitude in qubit count</b> (Module 08 &sect;4) "
    "— <b>and both of those statements are true at the same "
    "time</b>, which is the whole difficulty of describing this field "
    "accurately.",
    "<b>Which is the posture this course asks for</b> — "
    "<b>neither 'it will never work' nor 'it is nearly here'</b>, "
    "<b>both of which are claims made without the resource counts that "
    "would settle them</b> (Module 13)."]),
 ],
 "resources": [
   ("Shor &mdash; Scheme for reducing decoherence in quantum memory",
    "https://journals.aps.org/pra/abstract/10.1103/PhysRevA.52.R2493",
    "<b>&sect;&sect;1 and 2</b> — the first quantum code, and the "
    "phase-flip problem solved."),
   ("Fowler et al. &mdash; Surface codes: towards practical "
    "large-scale quantum computation (free)",
    "https://arxiv.org/abs/1208.0928",
    "<b>&sect;&sect;2 to 4</b> — the standard reference, with the "
    "overhead numbers and the decoding problem."),
   ("Preskill &mdash; Fault-tolerant quantum computation (free)",
    "https://arxiv.org/abs/quant-ph/9712048",
    "<b>&sect;3's threshold theorem</b>, explained rather than only "
    "proved."),
   ("Google Quantum AI &mdash; below-threshold surface code results "
    "(free)",
    "https://www.nature.com/articles/s41586-024-08449-y",
    "<b>&sect;&sect;3 and 4 experimentally</b> — a logical qubit "
    "outperforming its physical parts, which is the milestone to "
    "understand."),
 ],
 "exercises": [
   "<b>Show that I, X, Y, Z span</b> the single-qubit operator "
   "space.",
   "<b>Explain discretisation of errors</b> in your own words.",
   "<b>Say why phase flips have no classical analogue.</b>",
   "<b>Work the three-qubit bit-flip code</b> by hand, with both "
   "parities.",
   "<b>Confirm the parities reveal nothing</b> about the logical "
   "state.",
   "<b>Simulate the three-qubit code</b> with an injected error and "
   "correct it.",
   "<b>Try to correct a phase flip with it</b>, and see it fail.",
   "<b>State the threshold theorem</b> and what it established.",
   "<b>Compute the physical qubit count</b> for 1000 logical qubits at "
   "three overhead assumptions.",
   "<b>Read one resource estimate</b> and extract its assumed physical "
   "error rate.",
 ],
 "selfcheck": [
   "Why do continuous errors not prevent correction?",
   "Which errors must be corrected, and why does that suffice?",
   "What is new relative to classical codes?",
   "How is a syndrome measured without disturbing the data?",
   "Why is the surface code the hardware favourite?",
   "State the threshold theorem and what it established.",
   "What is the approximate threshold, and where is hardware?",
   "Give the overhead, and the two things that dominate it.",
   "Why does T-count matter so much?",
   "What should you read first in a resource estimate?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Near-Term Hardware",
 "subtitle": "What the current generation can and cannot be expected "
             "to do.",
 "question": "What can you do with a hundred noisy qubits?",
 "outcomes": [
     "Describe the current hardware landscape and its limits.",
     "Explain variational algorithms and their appeal.",
     "State the barren plateau problem.",
     "Explain the input and output problems.",
     "Assess a near-term application proposal.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What exists",
   "blurb": "Stated carefully, because it dates quickly."},

  {"t": "callout", "title": "Current devices have tens to hundreds of physical qubits, error rates near the threshold, and no useful error correction",
   "kind": "The landscape, as of this course's writing",
   "body": ["<b>Superconducting, trapped-ion, neutral-atom, and "
            "photonic platforms all exist</b>, with <b>different "
            "trade-offs between gate speed, coherence time, and "
            "connectivity</b> (Module 04 §3's "
            "tension).",
            "<b>Two-qubit gate error rates are around a "
            "fraction of a percent</b> on the best "
            "systems — <b>which bounds useful circuit depth to "
            "hundreds of gates</b>, not millions.",
            "<b>And connectivity is limited</b>: <b>a circuit "
            "assuming all-to-all coupling must be compiled with swap "
            "networks</b>, which multiplies the gate "
            "count.",
            "<b>So the honest statement is: these are real quantum "
            "devices and they are not fault-tolerant "
            "computers</b> — <b>Preskill's NISQ term names exactly "
            "this gap</b>, and the gap is the subject of this "
            "module."]},

  {"t": "section", "label": "Part 2", "title": "Variational algorithms",
   "blurb": "The near-term hope, and its structure."},

  {"t": "code", "kicker": "Variational", "title": "The hybrid loop",
   "lang": "text", "code": """
  THE IDEA
      keep the quantum circuit shallow, and let a
      classical optimiser do the hard work.

  THE LOOP
      1  prepare a parameterised state |psi(theta)>
         with a short circuit
      2  measure an expectation value, e.g. the
         energy of a Hamiltonian
      3  a CLASSICAL optimiser proposes new theta
      4  repeat until converged

  INSTANCES
      VQE     chemistry ground states (M09)
      QAOA    combinatorial optimisation

  WHY IT APPEALS
      shallow circuits fit inside the coherence time
      and some errors are absorbed by reoptimising
      the parameters

  WHY IT IS DIFFICULT
      see Part 3: the optimisation landscape
""",
   "caption": "<b>Shallow circuit, classical optimiser</b> — "
              "which fits the hardware, and moves the difficulty into "
              "the optimisation."},

  {"t": "section", "label": "Part 3", "title": "Barren plateaus",
   "blurb": "The obstacle, and it is structural."},

  {"t": "callout", "title": "For random parameterised circuits, gradients vanish exponentially in the number of qubits",
   "kind": "Why the optimisation is the hard part",
   "body": ["<b>The expected gradient of the cost is zero and its "
            "variance shrinks exponentially with qubit "
            "count</b> — <b>so the landscape is flat almost "
            "everywhere</b>, and the optimiser has nothing to "
            "follow.",
            "<b>Which means the number of measurements needed to "
            "resolve a gradient grows exponentially</b> — "
            "<b>exactly the scaling the method was supposed to "
            "avoid.</b>",
            "<b>And it is not a tuning problem</b> — <b>it is a "
            "property of expressive random circuits</b>, and more "
            "expressive ansätze make it worse, which is an "
            "uncomfortable trade.",
            "<b>So the mitigations all restrict "
            "expressiveness</b> — <b>problem-informed ansätze, "
            "shallow local cost functions, layerwise "
            "training</b> — and <b>restricting expressiveness is in "
            "tension with capturing the physics</b>, which is the "
            "field's open question."]},

  {"t": "section", "label": "Part 4", "title": "Input and output",
   "blurb": "The two problems that undermine most proposals."},

  {"t": "bullets", "kicker": "The caveats", "title": "What to check in any near-term application proposal",
   "items": [
     "<b>The input problem</b> — <b>loading a classical "
     "dataset of size N into amplitudes generally costs O(N)</b>, "
     "which destroys a polynomial advantage before the algorithm "
     "starts (Module 07 §3).",
     "",
     "<b>The output problem</b> — <b>the result is a "
     "quantum state, and extracting more than a few numbers from it "
     "costs exponentially many measurements</b> "
     "(Module 02 §2).",
     "",
     "<b>The classical baseline</b> — <b>which must be the "
     "best known method, and frequently is not "
     "checked</b> (Module 13 §3).",
     "",
     "<b>The assumed hardware</b> — <b>error rate, "
     "connectivity, and whether error correction is assumed</b>, all "
     "three stated.",
     "",
     "<b>And the scaling claim</b> — <b>asserted "
     "asymptotically, or measured over a range?</b> Usually the "
     "former, on a range too short to fit.",
   ],
   "footnote": "<b>Input and output together eliminate most proposed "
               "quantum machine learning applications</b> — which is "
               "a strong claim and is the one the careful papers "
               "make."},

  {"t": "callout", "title": "And the honest near-term position",
   "kind": "Closing",
   "body": ["<b>No convincing demonstration of a near-term quantum "
            "advantage on a useful problem has been made</b>, as of this "
            "course's writing — <b>which is a factual statement "
            "rather than a prediction.</b>",
            "<b>And the sampling demonstrations are real "
            "results</b> — <b>a device sampling from a distribution "
            "classical simulation struggles with</b> — <b>on problems "
            "chosen to be hard to simulate rather than useful</b>, which "
            "is the point and is sometimes lost.",
            "<b>Several of those have been substantially reduced by "
            "improved classical simulation afterwards</b> "
            "(Module 13 §3) — <b>which is science working, not "
            "scandal.</b>",
            "<b>So the near-term honest answer to 'what can a "
            "hundred noisy qubits do' is: physics experiments, "
            "benchmarks, and algorithm development</b> — <b>which is "
            "a reasonable thing for a technology at this stage to "
            "be.</b>"]},
 ],
 "takeaways": [
   "Current devices are real quantum devices and are not fault-tolerant "
   "computers; NISQ names exactly that gap.",
   "Two-qubit error rates near a fraction of a percent bound useful circuit "
   "depth to hundreds of gates.",
   "Variational methods keep the circuit shallow and move the difficulty "
   "into a classical optimiser.",
   "Barren plateaus: gradients vanish exponentially in qubit count, so the "
   "measurements needed grow exponentially.",
   "Mitigations restrict expressiveness, which is in tension with capturing "
   "the physics.",
   "Input and output costs together eliminate most proposed quantum machine "
   "learning applications.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What exists"),
  ("callout", "Current devices have tens to hundreds of physical qubits, "
              "error rates near the threshold, and no useful error "
              "correction",
   ["<b>Superconducting circuits, trapped ions, neutral atoms, and "
    "photonic systems all exist as working platforms</b>, with <b>very "
    "different trade-offs between gate speed, coherence time, and "
    "qubit connectivity</b> — which is Module 04 &sect;3's "
    "isolation-versus-control tension resolved differently in each "
    "case.",
    "<b>Two-qubit gate error rates are around a fraction of a "
    "percent on the best systems</b> — <b>which bounds the useful "
    "circuit depth to hundreds of gates</b> before the output is noise, "
    "<b>not the millions that Module 08's algorithms require.</b>",
    "<b>And connectivity is limited</b>: <b>a circuit written "
    "assuming all-to-all coupling has to be compiled with swap "
    "networks</b>, <b>which multiplies the gate count</b> — run "
    "one of your own circuits through a transpiler and watch it happen "
    "(Module 03 &sect;4's exercise).",
    "<b>So the honest statement is: these are real quantum devices "
    "and they are not fault-tolerant computers</b> — <b>Preskill's "
    "'NISQ' term names exactly this gap</b>, and the gap rather than "
    "either side of it is what this module is about. Specific numbers "
    "date quickly; the structure of the limitation does not."]),

  ("h1", "2 &nbsp; Variational algorithms"),
  ("code", """THE IDEA
    keep the quantum circuit shallow, and let a
    classical optimiser do the hard work.

THE LOOP
    1  prepare a parameterised state |psi(theta)>
       with a short circuit
    2  measure an expectation value, for example the
       energy of a Hamiltonian
    3  a CLASSICAL optimiser proposes new theta
    4  repeat until converged

INSTANCES
    VQE     chemistry ground states (Module 09)
    QAOA    combinatorial optimisation

WHY IT APPEALS
    shallow circuits fit inside the coherence time,
    and some errors are partly absorbed by
    reoptimising the parameters

WHY IT IS DIFFICULT
    see section 3: the optimisation landscape"""),
  ("p", "<b>Shallow circuit, classical optimiser</b> — <b>which "
        "fits the hardware, and moves the difficulty into the "
        "optimisation</b>. That relocation is the whole design idea, and "
        "it is a reasonable one: the hardware constraint is depth, and a "
        "classical optimiser has no depth limit. Whether the relocated "
        "problem is easier is &sect;3's subject, and the answer is "
        "currently no (CSCE 669's non-convex optimisation material is "
        "the right background here)."),
  ("callout", "For random parameterised circuits, gradients vanish "
              "exponentially in the number of qubits",
   ["<b>The expected gradient of the cost function is zero and its "
    "variance shrinks exponentially with the qubit count</b> — "
    "<b>so the landscape is flat almost everywhere</b>, <b>and the "
    "optimiser has nothing to follow</b>: this is the barren plateau "
    "phenomenon.",
    "<b>Which means the number of measurements needed to resolve a "
    "gradient to useful precision grows exponentially</b> — "
    "<b>exactly the scaling the whole method was supposed to avoid</b>, "
    "and it arrives through the back door of the optimisation rather "
    "than through the circuit.",
    "<b>And it is not a hyperparameter tuning problem</b> — "
    "<b>it is a property of sufficiently expressive random "
    "circuits</b>, provable from the concentration of measure on the "
    "unitary group — <b>and more expressive ans&auml;tze make it "
    "worse</b>, which is an uncomfortable trade since expressiveness is "
    "what you wanted.",
    "<b>So the mitigations all restrict expressiveness in some "
    "way</b> — <b>problem-informed ans&auml;tze, shallow and local "
    "cost functions, layerwise training, careful "
    "initialisation</b> — and <b>restricting expressiveness is in "
    "direct tension with capturing the physics you came for</b>, "
    "<b>which is the field's central open question</b> rather than a "
    "known fix."]),

  ("break",),
  ("h1", "3 &nbsp; Input and output"),
  ("ul", ["<b>The input problem</b> — <b>loading a classical "
          "dataset of size N into quantum amplitudes generally costs "
          "O(N)</b> operations, <b>which destroys any polynomial "
          "advantage before the algorithm begins</b> "
          "(Module 07 &sect;3). Proposed fixes assume a 'QRAM' whose "
          "own cost is rarely accounted for.",
          "<b>The output problem</b> — <b>the result of the "
          "computation is a quantum state, and extracting more than a "
          "few numbers from it costs exponentially many "
          "measurements</b> (Module 02 &sect;2's bottleneck) — "
          "<b>so an algorithm that 'produces the solution vector' has "
          "not produced anything you can read.</b>",
          "<b>The classical baseline</b> — <b>which must be the "
          "best known classical method and frequently is not even "
          "checked</b> (Module 13 &sect;3), and the dequantisation "
          "literature exists precisely because this was skipped.",
          "<b>The assumed hardware</b> — <b>error rate, "
          "connectivity, and whether fault tolerance is assumed</b>, "
          "all three stated explicitly, because a result assuming "
          "error-free qubits is a mathematical result rather than an "
          "engineering one.",
          "<b>And the scaling claim</b> — <b>asserted "
          "asymptotically, or measured over a range?</b> <b>Usually the "
          "former, on a simulated range far too short to fit a trend "
          "to.</b> <b>Input and output together eliminate most proposed "
          "quantum machine learning applications</b> — which is a "
          "strong claim, and <b>is the one the careful papers in the "
          "area make</b> rather than an outsider's "
          "scepticism."]),

  ("h1", "4 &nbsp; The honest near-term position"),
  ("callout", "And the honest near-term position",
   ["<b>No convincing demonstration of a near-term quantum advantage "
    "on a useful problem has been made</b>, as of this course's "
    "writing — <b>which is a factual statement about the "
    "literature rather than a prediction about the future</b>, and "
    "should be re-checked rather than assumed.",
    "<b>And the random-circuit sampling demonstrations are real "
    "results</b> — <b>a device sampling from a distribution that "
    "classical simulation struggles to reproduce</b> — <b>on "
    "problems deliberately chosen to be hard to simulate rather than "
    "useful</b>, <b>which is the entire point of the experiment and is "
    "sometimes lost in the reporting.</b>",
    "<b>Several of those demonstrations have been substantially "
    "reduced by improved classical simulation published "
    "afterwards</b> (Module 13 &sect;3's pattern) — <b>which is "
    "science working rather than scandal</b>, and is the strongest "
    "argument for stating baselines carefully in the first place.",
    "<b>So the near-term honest answer to 'what can a hundred noisy "
    "qubits do' is: physics experiments, benchmarks, and algorithm "
    "development</b> — <b>which is a perfectly reasonable thing for "
    "a technology at this stage to be</b>, and is only disappointing "
    "against claims that should not have been made."]),
 ],
 "resources": [
   ("Preskill &mdash; Quantum Computing in the NISQ era and beyond "
    "(free)",
    "https://quantum-journal.org/papers/q-2018-08-06-79/",
    "<b>&sect;1</b> — the framing, from the person who named it, and "
    "it is admirably careful about what is and is not "
    "claimed."),
   ("Cerezo et al. &mdash; Variational quantum algorithms (free)",
    "https://www.nature.com/articles/s42254-021-00348-9",
    "<b>&sect;2</b> — the survey, with the obstacles stated "
    "alongside the hopes."),
   ("McClean et al. &mdash; Barren plateaus in quantum neural network "
    "training landscapes (free)",
    "https://www.nature.com/articles/s41467-018-07090-4",
    "<b>&sect;3 in the original</b> — and the result is cleaner and "
    "more damaging than its reception suggested."),
   ("Aaronson &mdash; Read the fine print (free)",
    "https://www.scottaaronson.com/papers/qml.pdf",
    "<b>&sect;4's checklist</b> — the input and output problems "
    "stated once and for all, and the right thing to hand somebody "
    "with a proposal."),
 ],
 "exercises": [
   "<b>Find the current best two-qubit error rate</b> and compute the "
   "usable depth.",
   "<b>Transpile one circuit</b> to a limited-connectivity device and "
   "compare gate counts.",
   "<b>Implement a small VQE</b> for a two-qubit Hamiltonian.",
   "<b>Plot its optimisation landscape</b> over two parameters.",
   "<b>Increase the qubit count</b> and watch the gradient variance "
   "shrink.",
   "<b>Try a problem-informed ansatz</b> and compare.",
   "<b>Estimate the cost of loading</b> a million-element vector into "
   "amplitudes.",
   "<b>Estimate the measurements needed</b> to read out a 2ⁿ-element "
   "solution vector.",
   "<b>Take one published near-term proposal</b> and run §4's five "
   "checks on it.",
   "<b>Find a sampling demonstration</b> and the classical simulation "
   "that followed it.",
 ],
 "selfcheck": [
   "Describe the current hardware landscape in three facts.",
   "What bounds the usable circuit depth?",
   "Why does connectivity matter?",
   "Describe the variational loop and its two instances.",
   "Why does it appeal, given the hardware?",
   "State the barren plateau result and its consequence.",
   "Why is it not a tuning problem?",
   "What do the mitigations cost?",
   "State the input and output problems.",
   "Give the five checks for a near-term proposal.",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "BQP and Its Neighbours",
 "subtitle": "What is known, what is believed, and the difference.",
 "question": "Can a quantum computer solve NP-complete problems?",
 "outcomes": [
     "Define BQP and state its basic properties.",
     "Place BQP relative to P, NP, and PSPACE.",
     "Explain why NP-complete problems are not expected to fall.",
     "Explain why factoring's hardness is unproven.",
     "State what is known versus believed, accurately.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The class",
   "blurb": "Defined, with its unusual robustness."},

  {"t": "callout", "title": "BQP is what a quantum computer solves efficiently with bounded error, and it is remarkably robust",
   "kind": "The definition and its properties",
   "body": ["<b>BQP: decidable by a polynomial-size quantum circuit "
            "with error at most 1/3</b> — <b>which is BPP's "
            "definition with quantum circuits</b> "
            "(CSCE 658 §02).",
            "<b>The error constant does not "
            "matter</b> — <b>repetition and majority vote amplify "
            "it</b>, exactly as classically, so 1/3 is a convention "
            "rather than a choice.",
            "<b>And the gate set does not matter</b> — "
            "<b>Solovay-Kitaev converts between universal sets with "
            "polylogarithmic overhead</b> "
            "(Module 03 §1).",
            "<b>Which makes BQP a robust class rather than a "
            "model-dependent one</b> — <b>the same robustness that "
            "makes P and BPP meaningful</b>, and it is why the class is "
            "worth studying at all."]},

  {"t": "section", "label": "Part 2", "title": "Where it sits",
   "blurb": "And what is actually proved."},

  {"t": "table", "kicker": "Containments", "title": "What is known, and what is believed",
   "header": ["Statement", "Status"],
   "widths": [5.2, 5.8],
   "rows": [
     ["<b>P ⊆ BPP ⊆ BQP</b>", "<b>Proved, and easy</b>"],
     ["<b>BQP ⊆ PSPACE</b>", "<b>Proved: sum the path amplitudes in small space</b>"],
     ["<b>BQP ≠ P</b>", "<b>Unproved. It would imply P ≠ PSPACE</b>"],
     ["<b>NP ⊆ BQP</b>", "<b>Believed false. No evidence for it</b>"],
     ["<b>BQP ⊆ NP</b>", "<b>Believed false. Oracle evidence against</b>"],
     ["<b>Factoring is not in P</b>", "<b>Unproved, and widely assumed</b>"],
   ],
   "footnote": "<b>BQP ≠ P is unproved, and proving it would "
               "separate P from PSPACE</b> — which is a famous open "
               "problem, so this one is not falling "
               "soon.",
   "note": "The BQP-vs-P separation implies P ≠ PSPACE, which is "
           "why nobody expects a proof."},

  {"t": "callout", "title": "Which means the subject's central claim is conditional, and that is worth saying plainly",
   "kind": "The honest statement of what is established",
   "body": ["<b>Nobody has proved that a quantum computer is faster "
            "than a classical one for any problem</b> — <b>in the "
            "non-relativised setting</b>, which is the setting that "
            "matters.",
            "<b>Shor's algorithm beats the best <i>known</i> "
            "classical factoring algorithm</b> — <b>and no one has "
            "shown that no better classical algorithm "
            "exists.</b>",
            "<b>So the field rests on the same kind of assumption "
            "cryptography does</b> — <b>that a well-studied problem is "
            "hard</b> — which is reasonable and is not a "
            "proof (CSCE 711 §02).",
            "<b>And that is normal for complexity "
            "theory</b> (CSCE 637 §01) — <b>what is not normal is "
            "how often the conditional is dropped</b> in accounts of "
            "this particular subject."]},

  {"t": "section", "label": "Part 3", "title": "NP-complete problems",
   "blurb": "Why nobody expects them to fall."},

  {"t": "bullets", "kicker": "NP", "title": "The reasons, which are evidential rather than proved",
   "items": [
     "<b>The only general-purpose tool is Grover</b>, and "
     "<b>Grover is provably quadratic</b> "
     "(Module 06 §4) — so brute force will not "
     "do it.",
     "",
     "<b>And NP-complete problems have no known structure of the "
     "kind the QFT exploits</b> — <b>no periodicity, no hidden "
     "subgroup</b> (Module 07 §3).",
     "",
     "<b>Plus there is oracle evidence against</b>: "
     "<b>relative to a random oracle, NP is not contained in "
     "BQP</b> — which is suggestive rather than "
     "conclusive.",
     "",
     "<b>So the belief is well-founded and unproved</b> — "
     "<b>and 'quantum computers cannot solve NP-complete problems' "
     "overstates what is known</b>, which this course does not "
     "do.",
     "",
     "<b>And the correct statement is: no approach is known, and "
     "the known approaches provably do not suffice.</b>",
   ],
   "footnote": "<b>No approach is known, and the known approaches "
               "provably do not suffice</b> — which is the precise "
               "form of the claim and is weaker than the usual "
               "paraphrase."},

  {"t": "section", "label": "Part 4", "title": "Reading the literature",
   "blurb": "With the conditionals intact."},

  {"t": "callout", "title": "Distinguish proved, believed with evidence, and assumed for convenience",
   "kind": "Closing",
   "body": ["<b>Proved:</b> <b>Grover's optimality; the query "
            "separations; BQP ⊆ PSPACE; the threshold "
            "theorem</b> — these are theorems and will not "
            "change.",
            "<b>Believed with evidence:</b> <b>NP is not in BQP; "
            "factoring is classically hard; BQP is strictly larger than "
            "P</b> — supported by oracles and by failure "
            "to find counterexamples.",
            "<b>Assumed for convenience:</b> <b>that a particular "
            "classical baseline is the best one</b> — <b>which is the "
            "assumption that has failed most often in "
            "practice</b> (Module 13 §3).",
            "<b>Which is the program's rule applied to a "
            "literature:</b> <b>state what you proved, state what you "
            "assumed, and keep the conditional attached when you report "
            "the result.</b>"]},
 ],
 "takeaways": [
   "BQP is BPP's definition with quantum circuits, and it is robust to both "
   "the error constant and the gate set.",
   "BQP ⊆ PSPACE is proved by summing path amplitudes in small space.",
   "BQP ≠ P is unproved, and proving it would separate P from PSPACE.",
   "Nobody has proved a quantum computer is faster than a classical one for "
   "any problem in the non-relativised setting.",
   "The known approaches provably do not solve NP-complete problems, which "
   "is weaker than saying quantum computers cannot.",
   "The assumption that has failed most often in practice is that a "
   "particular classical baseline is the best one.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The class"),
  ("callout", "BQP is what a quantum computer solves efficiently with "
              "bounded error, and it is remarkably robust",
   ["<b>BQP is the class of languages decidable by a uniform family "
    "of polynomial-size quantum circuits with error probability at most "
    "1/3</b> — <b>which is precisely BPP's definition with quantum "
    "circuits substituted</b> (CSCE 658 Module 02, CSCE 637 "
    "Module 06).",
    "<b>The error constant does not matter</b> — <b>repetition "
    "and a majority vote amplify any constant below 1/2 to exponentially "
    "small</b>, exactly as in the classical case — <b>so 1/3 is a "
    "convention rather than a meaningful choice.</b>",
    "<b>And the gate set does not matter</b> — "
    "<b>Solovay-Kitaev converts between any two universal gate sets "
    "with polylogarithmic overhead</b> (Module 03 &sect;1) — so "
    "the class is independent of the hardware's native operations.",
    "<b>Which makes BQP a robust class rather than a "
    "model-dependent artefact</b> — <b>the same robustness that "
    "makes P and BPP meaningful objects of study</b> — and <b>it is "
    "why the class is worth defining at all</b>, rather than talking "
    "about particular machines."]),

  ("h1", "2 &nbsp; Where it sits"),
  ("table", ["Statement", "Status"],
   [["<b>P &sube; BPP &sube; BQP</b>",
     "<b>Proved, and easy</b> — a quantum circuit can simulate a "
     "classical reversible one, and randomness is available."],
    ["<b>BQP &sube; PSPACE</b>",
     "<b>Proved</b> — sum the amplitudes over computational paths "
     "one at a time, reusing the space (Module 04 &sect;1's path "
     "view, used as a proof technique)."],
    ["<b>BQP &ne; P</b>",
     "<b>Unproved.</b> <b>Proving it would imply P &ne; PSPACE</b>, "
     "which is a famous open problem — see the note."],
    ["<b>NP &sube; BQP</b>",
     "<b>Believed false</b>, with oracle evidence against and no "
     "evidence for (&sect;3)."],
    ["<b>BQP &sube; NP</b>",
     "<b>Believed false</b> — there is oracle evidence that BQP "
     "contains problems outside NP, so the two are believed "
     "incomparable."],
    ["<b>Factoring is not in P</b>",
     "<b>Unproved, and widely assumed</b> — which is what the "
     "whole public-key infrastructure already rests on."]],
   [0.40, 0.60]),
  ("p", "<b>BQP &ne; P is unproved, and proving it would separate P "
        "from PSPACE</b> — <b>which is a famous open problem</b>, "
        "<b>so this one is not falling soon</b>. <b>The BQP-versus-P "
        "separation implies P &ne; PSPACE</b>, by the containment chain "
        "above: that is the structural reason nobody expects an "
        "unconditional proof that quantum computers are more powerful, "
        "and it is worth knowing because it explains why the field's "
        "central claim stays conditional."),
  ("callout", "Which means the subject's central claim is conditional, and "
              "that is worth saying plainly",
   ["<b>Nobody has proved that a quantum computer is faster than a "
    "classical one for any problem</b> — <b>in the non-relativised "
    "setting</b>, which is the setting that corresponds to actual "
    "computation (Module 05 &sect;4's relativisation gap).",
    "<b>Shor's algorithm beats the best <i>known</i> classical "
    "factoring algorithm</b> — the number field sieve, "
    "subexponential — <b>and no one has shown that no better "
    "classical algorithm exists</b>, nor is anybody close to showing "
    "it.",
    "<b>So the field rests on the same kind of assumption that "
    "cryptography does</b> — <b>that a well-studied problem is "
    "hard because many people have tried and failed</b> — <b>which "
    "is reasonable and is not a proof</b> (CSCE 711 Module 02's "
    "framing of exactly this).",
    "<b>And that is entirely normal for complexity theory</b> "
    "(CSCE 637 Module 01: almost everything is conditional) — "
    "<b>what is not normal is how often the conditional is dropped</b> "
    "in public accounts of this particular subject, where 'quantum "
    "computers are exponentially faster' is stated as fact."]),

  ("break",),
  ("h1", "3 &nbsp; NP-complete problems"),
  ("ul", ["<b>The only general-purpose tool is Grover's "
          "algorithm</b>, and <b>Grover is provably quadratic</b> "
          "(Module 06 &sect;4's lower bound) — <b>so brute-force "
          "search over candidate solutions will not do it</b>, and that "
          "part is a theorem rather than a belief.",
          "<b>And NP-complete problems have no known structure of "
          "the kind the QFT exploits</b> — <b>no periodicity, no "
          "hidden abelian subgroup</b> (Module 07 &sect;3) — "
          "which removes the only other route to an exponential "
          "advantage that anybody has found.",
          "<b>Plus there is oracle evidence against</b>: <b>relative "
          "to a random oracle, NP is not contained in BQP</b> — "
          "<b>which is suggestive rather than conclusive</b>, for the "
          "relativisation reasons of Module 05 &sect;4, but it is "
          "evidence pointing one way and none pointing the other.",
          "<b>So the belief is well-founded and unproved</b> — "
          "and <b>the flat statement 'quantum computers cannot solve "
          "NP-complete problems' overstates what is known</b>, <b>which "
          "this course does not do</b> even though the overstatement is "
          "on the side of caution.",
          "<b>The correct statement is: no approach is known, and the "
          "known approaches provably do not suffice</b> — <b>which "
          "is the precise form of the claim and is weaker than the usual "
          "paraphrase</b>, and is also more informative, because it says "
          "where a surprise would have to come from."]),

  ("h1", "4 &nbsp; Reading the literature"),
  ("callout", "Distinguish proved, believed with evidence, and assumed for "
              "convenience",
   ["<b>Proved:</b> <b>Grover's optimality; the query separations of "
    "Module 05; BQP &sube; PSPACE; the threshold theorem</b> — "
    "<b>these are theorems and will not change</b>, and they are the "
    "firm ground to reason from.",
    "<b>Believed with evidence:</b> <b>NP is not contained in BQP; "
    "factoring is classically hard; BQP is strictly larger than "
    "P</b> — <b>supported by oracle results and by sustained "
    "failure to find counterexamples</b>, which is real evidence of a "
    "kind, and is not proof.",
    "<b>Assumed for convenience:</b> <b>that a particular classical "
    "baseline is the best available one</b> — <b>which is the "
    "assumption that has failed most often in practice</b> "
    "(Module 13 &sect;3's pattern of advantage claims being reduced "
    "by better classical algorithms), and is the one most under the "
    "author's own control.",
    "<b>Which is the program's closing rule applied to a "
    "literature:</b> <b>state what you proved, state what you assumed, "
    "and keep the conditional attached when you report the "
    "result</b> — because the conditional is where the honest "
    "content is."]),
 ],
 "resources": [
   ("Bernstein & Vazirani &mdash; Quantum complexity theory",
    "https://epubs.siam.org/doi/10.1137/S0097539796300921",
    "<b>&sect;1</b> — where BQP is defined and its robustness "
    "established."),
   ("Aaronson &mdash; BQP and the Polynomial Hierarchy (free)",
    "https://arxiv.org/abs/0910.4698",
    "<b>&sect;2's containments</b> — and the oracle evidence for BQP "
    "containing things outside NP."),
   ("The Complexity Zoo (free)",
    "https://complexityzoo.net/Complexity_Zoo",
    "<b>&sect;2</b> — look up BQP and follow the containments, which "
    "is the fastest way to see the landscape."),
   ("Aaronson &mdash; The Limits of Quantum Computers (free)",
    "https://www.scottaaronson.com/writings/limitsqc-draft.pdf",
    "<b>&sect;3</b> — the NP question treated carefully and for a "
    "general audience, which is harder than it sounds."),
 ],
 "exercises": [
   "<b>Define BQP</b> and show the error constant is arbitrary.",
   "<b>Explain why the gate set does not matter.</b>",
   "<b>Prove P ⊆ BQP</b>, informally.",
   "<b>Sketch the BQP ⊆ PSPACE argument</b> as a path sum.",
   "<b>Explain why BQP ≠ P would separate P from PSPACE.</b>",
   "<b>State what Shor's algorithm actually establishes</b>, with the "
   "conditional.",
   "<b>Give three reasons NP-complete problems are not expected to "
   "fall.</b>",
   "<b>State the claim in its precise form</b>, and contrast with the "
   "usual paraphrase.",
   "<b>Classify ten claims</b> from this course as proved, believed, "
   "or assumed.",
   "<b>Find a paper that drops a conditional</b> in its abstract but "
   "keeps it in the body.",
 ],
 "selfcheck": [
   "Define BQP and give its two robustness properties.",
   "Which containments are proved?",
   "Why is BQP ≠ P hard to prove?",
   "What has nobody proved about quantum speedups?",
   "What does Shor's algorithm establish, exactly?",
   "What kind of assumption does the field rest on?",
   "Give three reasons NP-complete problems are not expected to fall.",
   "State the precise claim about NP-complete problems.",
   "Give the three epistemic categories with an example of each.",
   "Which category has failed most often in practice?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Claiming a Quantum Advantage",
 "subtitle": "The problem, the baseline, and the machine.",
 "question": "A quantum computer did it faster. Faster than what?",
 "outcomes": [
     "State what an advantage claim must specify.",
     "Identify the standard overclaims.",
     "Explain the dequantisation pattern.",
     "Place this course in the semester and the program.",
     "Assess a quantum computing claim in minutes.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What a claim must name",
   "blurb": "Three things, and most claims name one."},

  {"t": "callout", "title": "An advantage claim names a problem, a classical baseline, and a machine — and all three are load-bearing",
   "kind": "The honest reading",
   "body": ["<b>The problem</b> — <b>and whether anybody wants it "
            "solved</b>: <b>random circuit sampling is a real "
            "demonstration and is not a useful "
            "problem</b>, which the careful papers say and the "
            "coverage omits.",
            "<b>The classical baseline</b> — <b>which algorithm, "
            "on what hardware, with how much effort "
            "spent</b> — because <b>the baseline is the claim's other "
            "half and it is frequently a strawman</b> "
            "(Part 2).",
            "<b>The machine</b> — <b>qubit count, error rates, "
            "connectivity, and whether error correction was "
            "assumed</b> (Module 11 §1) — <b>since a result "
            "assuming error-free qubits is mathematics, not "
            "engineering.</b>",
            "<b>And the resource count for a useful "
            "instance</b> (Modules 08 §4, 10 §4) — "
            "<b>which converts a possibility into a "
            "number</b> that somebody can check."]},

  {"t": "table", "kicker": "Overclaims", "title": "The standard overclaims, corrected",
   "header": ["The claim", "The correction"],
   "widths": [4.3, 6.7],
   "rows": [
     ["<b>'Exponentially faster'</b>", "<b>At what? Than which classical method? (M05 §4)</b>"],
     ["<b>'Tries all answers at once'</b>", "<b>Predicts constant-time search, which is false (M01 §2)</b>"],
     ["<b>'Will break all encryption'</b>", "<b>Public-key, not symmetric; and not yet (M08 §3)</b>"],
     ["<b>'Quantum speedup for machine learning'</b>", "<b>Input and output costs, usually unaccounted (M11 §3)</b>"],
     ["<b>'Solved a problem in 200 seconds'</b>", "<b>Versus which classical implementation, run how long?</b>"],
     ["<b>'Quantum supremacy achieved'</b>", "<b>On a sampling task designed to be hard to simulate</b>"],
   ],
   "footnote": "<b>The baseline is the half of the claim nobody "
               "checks</b> — and it is the half that has moved most "
               "often after publication.",
   "note": "Every row's correction is about something the claim did "
           "not name."},

  {"t": "section", "label": "Part 2", "title": "Dequantisation",
   "blurb": "The pattern, which has recurred several times."},

  {"t": "callout", "title": "Several claimed advantages have been reduced or eliminated by better classical algorithms written afterwards",
   "kind": "A healthy pattern, and a warning",
   "body": ["<b>A quantum algorithm is published with an exponential "
            "speedup over the known classical method</b>, and "
            "<b>a classical algorithm matching it, or nearly, "
            "follows</b> — sometimes within months.",
            "<b>Because the quantum algorithm's assumptions "
            "frequently imply classical structure too</b> — "
            "<b>a sampling-access assumption that makes the quantum "
            "version work also enables a classical "
            "one</b>.",
            "<b>And several sampling demonstrations have had their "
            "claimed classical cost reduced by orders of magnitude</b> "
            "after the fact, by better simulation "
            "methods.",
            "<b>Which is science working</b> — <b>the claim "
            "provoked the effort that tested it</b> — and <b>it is a "
            "strong argument for stating the baseline precisely enough "
            "to be attacked.</b>"]},

  {"t": "section", "label": "Part 3", "title": "The semester",
   "blurb": "Three courses, one shape."},

  {"t": "table", "kicker": "Semester 12", "title": "Where this course sits",
   "header": ["Course", "Who sets the rules", "The consequence"],
   "widths": [2.3, 4.0, 4.7],
   "rows": [
     ["<b>CSCE 640</b>", "<b>Physics</b>", "<b>The gate set and the measurement rule are given</b>"],
     ["<b>CSCE 628</b>", "<b>Biology</b>", "<b>The data is noisy and the truth is not available</b>"],
     ["<b>CSCE 717</b>", "<b>Self-interested agents</b>", "<b>The inputs are chosen to benefit whoever sent them</b>"],
   ],
   "footnote": "<b>In all three, the model comes from outside "
               "computer science</b> — and designing against a model "
               "you did not choose is the semester's common "
               "skill.",
   "note": "The model-from-outside framing is Semester 12's "
           "result."},

  {"t": "section", "label": "Part 4", "title": "Assessing a claim",
   "blurb": "In about five minutes."},

  {"t": "bullets", "kicker": "Checklist", "title": "The questions, in order",
   "items": [
     "<b>What is the problem, and does anybody want it "
     "solved?</b> — which eliminates the sampling "
     "demonstrations from the 'useful' column "
     "immediately.",
     "",
     "<b>What is the classical baseline, and how hard did they "
     "try?</b> (Part 2) — <b>and is it the best known "
     "method or the obvious one?</b>",
     "",
     "<b>What machine, with what error rates, and is fault "
     "tolerance assumed?</b> "
     "(Module 11 §1).",
     "",
     "<b>What is the resource count for a useful "
     "instance?</b> (Modules 08 §4, "
     "10 §4) — in physical qubits, not "
     "logical.",
     "",
     "<b>And is the scaling measured or asserted?</b> "
     "(Module 11 §4) — <b>over what range, and does the "
     "range support the fit?</b>",
   ],
   "footnote": "<b>Five questions, five minutes</b> — and most "
               "claims fail on the second one, which is the baseline "
               "nobody checks."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You know the mechanism</b> — <b>interference, and "
            "what cancels</b> (Module 04) — <b>which is enough to "
            "evaluate whether a proposed algorithm could possibly "
            "work.</b>",
            "<b>You can derive the important "
            "algorithms</b> — <b>Grover as a rotation, Shor as phase "
            "estimation on a shift operator</b> — rather than recall "
            "them as recipes.",
            "<b>And you know the engineering reality and the "
            "complexity-theoretic status</b> (Modules 10 and 12) — "
            "<b>which is what separates assessing this field from "
            "admiring it.</b>",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it is the problem, the "
            "baseline, and the machine</b> — because <b>'a quantum "
            "computer did it faster' is not yet a "
            "claim.</b>"]},
 ],
 "takeaways": [
   "An advantage claim names a problem, a classical baseline, and a "
   "machine, and all three are load-bearing.",
   "The baseline is the half of the claim nobody checks, and it is the half "
   "that has moved most often after publication.",
   "Dequantisation recurs because the assumptions that make a quantum "
   "algorithm work often imply classical structure too.",
   "A result assuming error-free qubits is mathematics rather than "
   "engineering, so the machine must be named.",
   "Five questions, five minutes — and most claims fail on the "
   "baseline.",
   "All three Semester 12 courses take their model from outside computer "
   "science, and design against rules they did not choose.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What a claim must name"),
  ("callout", "An advantage claim names a problem, a classical baseline, and "
              "a machine — and all three are load-bearing",
   ["<b>The problem</b> — <b>and whether anybody wants it "
    "solved</b>: <b>random circuit sampling is a real and impressive "
    "demonstration and is not a useful problem</b>, <b>which the careful "
    "papers state plainly and the coverage routinely omits</b> "
    "(Module 11 &sect;4).",
    "<b>The classical baseline</b> — <b>which algorithm, "
    "running on what hardware, with how much engineering effort spent on "
    "it</b> — because <b>the baseline is the claim's other half, "
    "and it is frequently a strawman</b> or simply the first thing that "
    "came to hand (&sect;2).",
    "<b>The machine</b> — <b>qubit count, gate error rates, "
    "connectivity, and whether error correction was assumed rather than "
    "performed</b> (Module 11 &sect;1) — <b>since a result "
    "assuming error-free qubits is a mathematical result rather than an "
    "engineering one</b>, and both are legitimate but they are not the "
    "same.",
    "<b>And the resource count for a useful instance</b> "
    "(Module 08 &sect;4 and Module 10 &sect;4) — <b>which "
    "converts a possibility into a number</b> <b>that somebody else can "
    "check</b>, and is the single most useful thing a paper in this area "
    "can include."]),
  ("table", ["The claim", "The correction"],
   [["<b>'Exponentially faster.'</b>",
     "<b>At what task? Than which classical method?</b> And is it "
     "queries or time? (Module 05 &sect;4.)"],
    ["<b>'It tries all the answers at once.'</b>",
     "<b>Which predicts constant-time unstructured search, and that is "
     "provably false</b> (Module 01 &sect;2, Module 06 "
     "&sect;4)."],
    ["<b>'It will break all encryption.'</b>",
     "<b>Public-key number-theoretic primitives, not symmetric ones; "
     "and not on any machine that exists</b> (Module 08 "
     "&sect;3)."],
    ["<b>'Quantum speedup for machine learning.'</b>",
     "<b>Input and output costs, almost always unaccounted for</b> "
     "(Module 11 &sect;3)."],
    ["<b>'Solved in 200 seconds what would take 10,000 years.'</b>",
     "<b>Versus which classical implementation, run for how long, by "
     "people with what incentive to try?</b> (&sect;2.)"],
    ["<b>'Quantum supremacy achieved.'</b>",
     "<b>On a sampling task constructed specifically to be hard to "
     "simulate</b> — which is the experiment's design, not a "
     "criticism of it."]],
   [0.34, 0.66]),
  ("p", "<b>The baseline is the half of the claim nobody "
        "checks</b> — <b>and it is the half that has moved most "
        "often after publication</b> (&sect;2). <b>Every row's "
        "correction above is about something the claim did not "
        "name</b>, which is why &sect;4's checklist is a list of "
        "questions rather than a list of objections: the problem is "
        "almost never that a stated fact is wrong."),

  ("h1", "2 &nbsp; Dequantisation"),
  ("callout", "Several claimed advantages have been reduced or eliminated by "
              "better classical algorithms written afterwards",
   ["<b>A quantum algorithm is published with an apparent exponential "
    "speedup over the known classical method</b>, and <b>a classical "
    "algorithm matching it, or very nearly, follows</b> — sometimes "
    "within months, and in several well-known cases by a "
    "student.",
    "<b>Because the quantum algorithm's assumptions frequently imply "
    "classical structure as well</b> — <b>a sampling-access "
    "assumption strong enough to make the quantum version work often "
    "enables a classical sampling algorithm too</b>, which is the "
    "mechanism behind the quantum-machine-learning dequantisation "
    "results.",
    "<b>And several sampling demonstrations have had their claimed "
    "classical cost reduced by many orders of magnitude after the "
    "fact</b>, by better tensor-network simulation and by simply "
    "spending more compute on the classical side than the original "
    "comparison did.",
    "<b>Which is science working</b> — <b>the claim provoked "
    "exactly the effort that tested it</b> — and <b>it is a strong "
    "argument for stating the baseline precisely enough to be "
    "attacked</b>, rather than vaguely enough to be safe. A claim nobody "
    "can refute is a claim nobody can confirm."]),

  ("break",),
  ("h1", "3 &nbsp; The semester"),
  ("table", ["Course", "Who sets the rules", "The consequence"],
   [["<b>CSCE 640 (this one)</b>", "<b>Physics.</b>",
     "<b>The gate set, the measurement rule, and the noise are "
     "given</b> — you design within them and cannot negotiate."],
    ["<b>CSCE 628</b>", "<b>Biology.</b>",
     "<b>The data is noisy and the ground truth is frequently not "
     "available</b> — so the algorithm's output cannot be checked "
     "the way a sorting routine's can."],
    ["<b>CSCE 717</b>", "<b>Self-interested agents.</b>",
     "<b>The inputs are chosen to benefit whoever sent them</b> — "
     "so correctness has to include the incentive to report "
     "honestly."]],
   [0.22, 0.28, 0.50]),
  ("p", "<b>In all three courses the model comes from outside "
        "computer science</b> — <b>and designing against a model you "
        "did not choose is the semester's common skill</b>. It is a "
        "different discipline from the earlier semesters, where the "
        "machine, the data, and the inputs were all yours: here the rules "
        "are given, they are not negotiable, and the first job in each "
        "case is to state them accurately. <b>The model-from-outside "
        "framing is Semester 12's result</b>, and Module 01 &sect;4's "
        "insistence on resource counts is one instance of it."),

  ("h1", "4 &nbsp; Assessing a claim"),
  ("ul", ["<b>What is the problem, and does anybody want it "
          "solved?</b> — <b>which eliminates the sampling "
          "demonstrations from the 'useful' column immediately</b>, "
          "without diminishing them as experiments.",
          "<b>What is the classical baseline, and how hard did they "
          "try?</b> (&sect;2) — <b>and is it the best known method "
          "or merely the obvious one?</b> This is where most claims "
          "fail.",
          "<b>What machine, with what error rates and connectivity, "
          "and is fault tolerance assumed or achieved?</b> "
          "(Module 11 &sect;1.)",
          "<b>What is the resource count for a useful "
          "instance?</b> (Module 08 &sect;4, Module 10 "
          "&sect;4) — <b>in physical qubits, not logical ones</b>, "
          "since the two differ by three orders of magnitude.",
          "<b>And is the scaling measured or asserted?</b> "
          "(Module 11 &sect;4) — <b>over what range of problem "
          "sizes, and does that range actually support the fit?</b> "
          "<b>Five questions, five minutes</b> — and <b>most claims "
          "fail on the second one, which is the baseline nobody "
          "checks.</b>"]),
  ("callout", "Where this course leaves you",
   ["<b>You know the mechanism</b> — <b>interference, and the "
    "question of what cancels</b> (Module 04 &sect;4) — <b>which "
    "is enough to evaluate whether a proposed algorithm could possibly "
    "work</b>, and that filter alone resolves a great deal.",
    "<b>You can derive the important algorithms rather than recall "
    "them</b> — <b>Grover as a rotation built from two reflections, "
    "Shor as phase estimation on a modular multiplication "
    "operator</b> — which is the difference between understanding "
    "and remembering.",
    "<b>And you know the engineering reality and the "
    "complexity-theoretic status</b> (Modules 10 and 12) — "
    "<b>which is what separates assessing this field from admiring "
    "it</b>, and is the part that most popular accounts leave out "
    "entirely.",
    "<b>The closing rule is the program's, unchanged across "
    "thirty-four courses:</b> <b>state what you measured, state what you "
    "assumed, and never claim more than you established.</b> <b>In this "
    "subject it is the problem, the baseline, and the machine</b> "
    "— because <b>'a quantum computer did it faster' is not yet a "
    "claim</b>, and the three missing names are where the content "
    "is."]),
 ],
 "resources": [
   ("Aaronson &mdash; Read the fine print (free)",
    "https://www.scottaaronson.com/papers/qml.pdf",
    "<b>&sect;&sect;1 and 2</b> — the caveats, stated once and "
    "carefully, and the right thing to read before assessing any "
    "proposal."),
   ("Tang &mdash; A quantum-inspired classical algorithm for "
    "recommendation systems (free)",
    "https://arxiv.org/abs/1807.04271",
    "<b>&sect;2's dequantisation</b> — the paper that started the "
    "pattern, and it is short."),
   ("Pan, Chen & Zhang &mdash; classical simulation of random circuit "
    "sampling (free preprints)",
    "https://arxiv.org/abs/2111.03011",
    "<b>&sect;2's second kind</b> — a claimed classical cost reduced "
    "by orders of magnitude after the fact."),
   ("Quantum (the journal), the resource-estimate papers (free)",
    "https://quantum-journal.org/",
    "<b>&sect;&sect;1 and 4</b> — the papers that do state all three "
    "things, which are the model to imitate in Project 2."),
 ],
 "exercises": [
   "<b>State the three things a claim must name</b>, and why each "
   "matters.",
   "<b>Find three published claims</b> and check which of the three "
   "each names.",
   "<b>Correct six overclaims</b> in your own words.",
   "<b>Read one dequantisation paper</b> and state what assumption it "
   "exploited.",
   "<b>Find a sampling demonstration</b> and the classical response to "
   "it.",
   "<b>Write the baseline section</b> for your own Project 2.",
   "<b>Convert one logical-qubit estimate</b> to physical qubits, with "
   "the overhead stated.",
   "<b>State each Semester 12 course's model and who sets it.</b>",
   "<b>Run §4's five questions</b> on a current news story.",
   "<b>Project 2 is now due.</b> Submit the derivation, the "
   "implementation, the best-known classical baseline measured on the "
   "same instances, the measured scaling of both, the resource estimate "
   "in physical qubits, and the honest claim naming the problem, the "
   "baseline, and the machine.",
 ],
 "selfcheck": [
   "Name the three things an advantage claim must specify.",
   "What fourth thing converts a possibility into a number?",
   "Correct six standard overclaims.",
   "Which half of a claim is least checked?",
   "Describe the dequantisation pattern and its mechanism.",
   "Why is it science working rather than scandal?",
   "Give the five assessment questions in order.",
   "Which question do most claims fail?",
   "State each Semester 12 course's external model.",
   "State the closing rule in this subject's terms.",
 ],
},

]
