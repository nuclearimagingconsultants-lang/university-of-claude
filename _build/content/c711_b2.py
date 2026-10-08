# -*- coding: utf-8 -*-
"""CSCE 711 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Randomness",
 "subtitle": "The foundation everything else stands on.",
 "question": "Where do keys come from, and what if the answer is wrong?",
 "outcomes": [
     "Distinguish true, pseudo, and cryptographic randomness.",
     "Name the correct source on each platform.",
     "Explain the historical randomness failures and their cause.",
     "Explain why nonces and keys have different requirements.",
     "Audit code for randomness misuse.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Three kinds",
   "blurb": "Only one of which is acceptable for keys."},

  {"t": "table", "kicker": "Sources", "title": "The three kinds, and what each is for",
   "header": ["Kind", "Property", "Use"],
   "widths": [3.0, 4.2, 4.6],
   "rows": [
     ["<b>True / entropy source</b>", "<b>Physically unpredictable</b>", "<b>Seeding the CSPRNG</b>"],
     ["<b>Ordinary PRNG</b>", "<b>Statistically uniform, fully predictable from state</b>", "<b>Simulation, games — never keys</b>"],
     ["<b>CSPRNG</b>", "<b>Next output unpredictable even given all prior output</b>", "<b>Everything cryptographic</b>"],
   ],
   "footnote": "<b>The middle row is the trap:</b> a Mersenne Twister "
               "passes every statistical test and <b>its entire future "
               "is recoverable from 624 outputs</b> — statistical "
               "uniformity is not unpredictability.",
   "note": "The statistical-vs-unpredictable distinction is the whole "
           "module in one line."},

  {"t": "callout", "title": "The requirement is unpredictability, not uniformity",
   "kind": "And the distinction is not intuitive",
   "body": ["<b>An ordinary PRNG produces output that passes every "
            "statistical randomness test</b> — uniform, "
            "uncorrelated, high entropy by every measure — "
            "<b>and is completely predictable once you know its "
            "internal state.</b>",
            "<b>And the state is recoverable from the output.</b> "
            "<b>Observing enough outputs of a Mersenne Twister "
            "reconstructs its state exactly</b>, after which every past "
            "and future value is known.",
            "<b>A CSPRNG adds the property that matters:</b> "
            "<b>knowing all previous output gives no advantage in "
            "predicting the next bit</b>, which is exactly the "
            "indistinguishability framing of Module 01 §3.",
            "<b>So the test is never 'does it look random' — it "
            "is 'which function produced it'</b>, and that is a question "
            "about the code rather than about the output."]},

  {"t": "section", "label": "Part 2", "title": "The right source",
   "blurb": "Short list, memorise it."},

  {"t": "code", "kicker": "Sources", "title": "What to call, by platform",
   "lang": "text", "code": """
  CORRECT
      Linux/BSD    getrandom(2), or read /dev/urandom
      Windows      BCryptGenRandom
      macOS/iOS    SecRandomCopyBytes / arc4random_buf
      Python       secrets.*, or os.urandom
      Java         SecureRandom
      Go           crypto/rand
      Node         crypto.randomBytes
      libsodium    randombytes_buf

  NEVER FOR ANYTHING CRYPTOGRAPHIC
      rand(), random(), Math.random()
      java.util.Random
      Python's random module
      any PRNG you seeded yourself
      the current time, a PID, a counter, a UUIDv1

  AND /dev/random vs /dev/urandom: on modern Linux use
  urandom or getrandom. The folklore about urandom being
  weaker is obsolete.
""",
   "caption": "<b>The urandom folklore persists and is wrong</b> on "
              "every current kernel — blocking on /dev/random buys "
              "nothing and causes availability failures.",
   "note": "Students arrive believing the urandom myth; correct it "
           "explicitly."},

  {"t": "section", "label": "Part 3", "title": "How it fails",
   "blurb": "The historical record, which is instructive."},

  {"t": "bullets", "kicker": "Failures", "title": "The recurring failure modes",
   "items": [
     "<b>Seeding from a predictable value.</b> <b>Time, process "
     "ID, or a counter</b> — which reduces the key space to "
     "something searchable in seconds.",
     "",
     "<b>A patch that destroys the entropy pool.</b> <b>One "
     "distribution's removal of 'uninitialised memory' usage reduced "
     "its keys to a few tens of thousands of possibilities</b>, and the "
     "code still worked perfectly.",
     "",
     "<b>Generating keys at first boot</b>, before any entropy has "
     "accumulated — which produced large numbers of embedded "
     "devices sharing keys.",
     "",
     "<b>A broken hardware source trusted without "
     "mixing</b> — which is why platforms mix hardware output into "
     "a software pool rather than using it directly.",
     "",
     "<b>And forking:</b> <b>a process that forks after seeding "
     "gives both children the same stream</b> unless the library "
     "handles it.",
   ],
   "footnote": "<b>Every one of these produced working software.</b> "
               "<b>Randomness failures are silent</b> — the keys "
               "generate, the encryption works, and the key space is "
               "tiny."},

  {"t": "callout", "title": "Randomness failures are catastrophic, silent, and retroactive",
   "kind": "Why this module comes second",
   "body": ["<b>Catastrophic, because every key, nonce, and token "
            "derived from a weak source is weak</b> — the strength "
            "of the cipher is irrelevant.",
            "<b>Silent, because nothing fails.</b> <b>There is no "
            "error, no test failure, and no observable difference until "
            "someone exploits it</b>, which may be years later.",
            "<b>And retroactive:</b> <b>keys generated during the "
            "weak period remain weak after the bug is fixed</b>, so "
            "remediation means regenerating and rotating everything "
            "— which is why Module 10's rotation procedure matters.",
            "<b>So the correct posture is to use the platform source "
            "and never touch it again</b> — <b>this is the one "
            "place in cryptography where there is genuinely nothing to "
            "tune.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Nonces and keys",
   "blurb": "Different requirements, commonly confused."},

  {"t": "table", "kicker": "Requirements", "title": "What each value actually needs",
   "header": ["Value", "Requirement", "Consequence of failure"],
   "widths": [2.5, 4.2, 5.1],
   "rows": [
     ["<b>Key</b>", "<b>Unpredictable, secret</b>", "<b>Total loss of confidentiality</b>"],
     ["<b>Nonce / IV</b>", "<b>Unique per key — need not be secret</b>", "<b>Severe, mode-dependent (M11 §2)</b>"],
     ["<b>Salt</b>", "<b>Unique — need not be secret or unpredictable</b>", "<b>Precomputation becomes possible</b>"],
     ["<b>Session token</b>", "<b>Unpredictable</b>", "<b>Session hijacking</b>"],
     ["<b>Reset token</b>", "<b>Unpredictable, single-use, expiring</b>", "<b>Account takeover</b>"],
   ],
   "footnote": "<b>A nonce needs uniqueness and not secrecy</b>, which "
               "is why it ships in the clear — and why a counter is "
               "a valid nonce where you can guarantee the counter never "
               "repeats.",
   "note": "The uniqueness-not-secrecy point is the one that clarifies "
           "nonce handling."},

  {"t": "bullets", "kicker": "Audit", "title": "What to look for in review",
   "items": [
     "<b>Any import of a non-cryptographic random module</b> in a "
     "file that handles tokens, keys, or identifiers.",
     "",
     "<b>Any explicit seeding.</b> <b>A correct CSPRNG is never "
     "seeded by application code</b>, so a seed call is a defect "
     "signal.",
     "",
     "<b>Tokens built from a timestamp, a counter, a hash of "
     "predictable inputs, or a sequential identifier.</b>",
     "",
     "<b>UUID version 1 used as a secret</b> — it encodes a "
     "timestamp and a MAC address, and is designed to be unique rather "
     "than unguessable.",
     "",
     "<b>And key generation that happens at install or first "
     "boot</b>, which is the embedded-device failure from "
     "Part 3.",
   ],
   "footnote": "<b>'Unique' and 'unguessable' are different "
               "requirements</b>, and UUID conflates them in the mind of "
               "nearly every developer who reaches for one."},
 ],
 "takeaways": [
   "The requirement is unpredictability, not statistical uniformity — "
   "a Mersenne Twister passes every test and is fully recoverable from its "
   "output.",
   "Use the platform CSPRNG and never seed it yourself; an explicit seed "
   "call in application code is a defect signal.",
   "The /dev/random versus /dev/urandom folklore is obsolete; use urandom "
   "or getrandom on any current kernel.",
   "Randomness failures are catastrophic, silent, and retroactive — "
   "the software works perfectly while the key space is tiny.",
   "A nonce requires uniqueness and not secrecy, which is why it ships in "
   "the clear and why a guaranteed counter is valid.",
   "'Unique' and 'unguessable' are different requirements, and UUIDv1 "
   "provides only the first.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Three kinds of randomness"),
  ("table", ["Kind", "The property it has", "What it is for"],
   [["<b>True randomness / entropy source</b>",
     "<b>Physically unpredictable</b> — thermal noise, timing "
     "jitter, a hardware instruction.",
     "<b>Seeding the CSPRNG.</b> Rarely used directly, because it is "
     "slow and of variable quality."],
    ["<b>Ordinary PRNG</b>",
     "<b>Statistically uniform, and completely predictable from its "
     "internal state.</b>",
     "<b>Simulation, sampling, games, shuffling for fairness</b> "
     "— <b>never anything cryptographic.</b> See the note."],
    ["<b>CSPRNG</b>",
     "<b>The next output is unpredictable even to an adversary who has "
     "seen all previous output.</b>",
     "<b>Everything cryptographic</b> — keys, nonces, salts, "
     "tokens, identifiers that must not be guessable."]],
   [0.22, 0.38, 0.40]),
  ("p", "<b>The middle row is the trap, and it catches "
        "professionals.</b> <b>A Mersenne Twister passes every "
        "statistical randomness test that exists</b> — it is uniform, "
        "uncorrelated, and has an enormous period — <b>and its "
        "entire future and past output is recoverable from 624 consecutive "
        "outputs</b>, because that is exactly its state. <b>Statistical "
        "uniformity is not unpredictability</b>, and the tests that "
        "measure the first say nothing about the second."),
  ("callout", "The requirement is unpredictability, not uniformity",
   ["<b>An ordinary PRNG produces output that passes every statistical "
    "test of randomness</b> — uniform distribution, no "
    "autocorrelation, maximal entropy by every measure you can "
    "compute — <b>and is entirely predictable once its internal "
    "state is known.</b>",
    "<b>And the state is recoverable from the output.</b> <b>Observing "
    "sufficiently many outputs reconstructs the state exactly</b>, after "
    "which every past and future value is known with certainty — not "
    "estimated, known.",
    "<b>A CSPRNG adds precisely the property that matters:</b> "
    "<b>knowing all previous output gives an adversary no advantage in "
    "predicting the next bit</b>, which is exactly the "
    "indistinguishability framing of Module 01 &sect;3 applied to a "
    "generator rather than to a cipher.",
    "<b>So the test is never 'does this output look random' — it "
    "is 'which function produced it'</b>, and <b>that is a question "
    "about the source code rather than about the bytes</b>, which is why "
    "&sect;4's audit is a code review rather than a statistical "
    "analysis."]),

  ("h1", "2 &nbsp; The right source"),
  ("code", """CORRECT
    Linux/BSD    getrandom(2), or read /dev/urandom
    Windows      BCryptGenRandom
    macOS/iOS    SecRandomCopyBytes / arc4random_buf
    Python       secrets.*, or os.urandom
    Java         SecureRandom
    Go           crypto/rand
    Node         crypto.randomBytes
    libsodium    randombytes_buf

NEVER FOR ANYTHING CRYPTOGRAPHIC
    rand(), random(), Math.random()
    java.util.Random
    Python's random module
    any PRNG you seeded yourself
    the current time, a PID, a counter, a UUIDv1

AND /dev/random vs /dev/urandom: on any modern Linux
kernel, use urandom or getrandom. The folklore about
urandom being cryptographically weaker is obsolete."""),
  ("p", "<b>The urandom folklore persists and is wrong on every current "
        "kernel.</b> <b>Blocking on /dev/random buys no additional "
        "security and causes real availability failures</b> — "
        "services that hang at boot waiting for entropy that is already "
        "sufficient. <b>The one genuine edge case is a freshly "
        "provisioned virtual machine or embedded device generating "
        "long-term keys before any entropy has accumulated</b>, which is "
        "&sect;3's third failure and is addressed by "
        "<code>getrandom(2)</code> blocking only until the pool is "
        "initialised once."),

  ("break",),
  ("h1", "3 &nbsp; How it fails"),
  ("ul", ["<b>Seeding from a predictable value.</b> <b>The current "
          "time, a process identifier, or a counter</b> — which "
          "reduces an apparently 128-bit key space to something "
          "exhaustively searchable in seconds.",
          "<b>A patch that destroys the entropy pool.</b> <b>One "
          "distribution's well-intentioned removal of a line that used "
          "uninitialised memory reduced the effective key space to a few "
          "tens of thousands of possibilities</b> — and the code "
          "continued to work perfectly for two years.",
          "<b>Generating long-term keys at first boot</b>, before any "
          "entropy has accumulated — <b>which produced large "
          "populations of embedded devices and virtual machines sharing "
          "identical host keys</b>, discoverable by anyone who scanned "
          "for them.",
          "<b>A hardware source trusted without mixing.</b> <b>Which "
          "is exactly why every serious platform mixes hardware "
          "instruction output into a software pool rather than returning "
          "it directly</b> — a defective or backdoored hardware "
          "source then degrades rather than destroys the output.",
          "<b>And forking.</b> <b>A process that forks after seeding "
          "gives both children an identical stream</b> unless the library "
          "detects it — which produced duplicate session keys in "
          "more than one widely deployed server. <b>Every one of these "
          "produced working software</b>, which is the lesson: "
          "<b>randomness failures are silent, the keys generate, the "
          "encryption works, and the key space is tiny.</b>"]),
  ("callout", "Randomness failures are catastrophic, silent, and retroactive",
   ["<b>Catastrophic, because every key, nonce, salt, and token derived "
    "from a weak source is weak</b> — and <b>the strength of the "
    "cipher using it is entirely irrelevant.</b> AES-256 with a key "
    "drawn from 2<sup>16</sup> possibilities offers 16 bits of "
    "security.",
    "<b>Silent, because nothing fails.</b> <b>There is no error, no "
    "exception, no test failure, and no observable difference in "
    "behaviour</b> until somebody exploits it — which may be years "
    "after deployment, and which is how the historical examples in "
    "&sect;3 all went undetected for extended periods.",
    "<b>And retroactive:</b> <b>keys generated during the weak period "
    "remain weak after the bug is fixed</b>, so remediation means "
    "identifying, regenerating, and rotating every affected key and "
    "every artefact derived from one — <b>which is why "
    "Module 10's rotation procedure needs to exist before you need "
    "it</b> (and CSCE 701 Module 07 &sect;3).",
    "<b>So the correct posture is to use the platform source and never "
    "touch it again.</b> <b>This is the one place in all of "
    "cryptography where there is genuinely nothing to tune, nothing to "
    "optimise, and no legitimate reason to be clever</b> — which "
    "makes it the easiest rule in the course to follow and one of the "
    "most frequently broken."]),

  ("h1", "4 &nbsp; Nonces, keys, and what each needs"),
  ("table", ["Value", "What it actually requires", "Consequence of getting "
             "it wrong"],
   [["<b>Key</b>", "<b>Unpredictable and secret.</b>",
     "<b>Total loss of confidentiality and authenticity.</b>"],
    ["<b>Nonce / IV</b>",
     "<b>Unique per key. It need not be secret and, for most modes, "
     "need not be unpredictable.</b>",
     "<b>Severe and mode-dependent</b> — catastrophic for "
     "counter-mode constructions (Module 11 &sect;2)."],
    ["<b>Salt</b>",
     "<b>Unique. It need not be secret or unpredictable.</b>",
     "<b>Precomputation across users becomes possible</b> "
     "(Module 09)."],
    ["<b>Session token</b>", "<b>Unpredictable.</b>",
     "<b>Session hijacking</b> (CSCE 701 Module 02 &sect;3)."],
    ["<b>Password reset token</b>",
     "<b>Unpredictable, single-use, and expiring.</b>",
     "<b>Account takeover</b> — and the single-use requirement is "
     "the one usually omitted."]],
   [0.19, 0.40, 0.41]),
  ("p", "<b>A nonce requires uniqueness and not secrecy</b>, which is "
        "<b>why it ships in the clear alongside the ciphertext</b> and "
        "why <b>a counter is a perfectly valid nonce wherever you can "
        "genuinely guarantee the counter never repeats for a given "
        "key</b> — the difficulty being that distributed systems and "
        "restarts make that guarantee much harder than it sounds "
        "(CSCE 678 Module 05)."),
  ("ul", ["<b>Any import of a non-cryptographic random module</b> in a "
          "file that handles keys, tokens, or identifiers that must not be "
          "guessable. <b>This single grep finds real defects.</b>",
          "<b>Any explicit seeding call.</b> <b>A correct CSPRNG is "
          "never seeded by application code</b>, so the presence of a "
          "seed call is itself a defect signal regardless of what it "
          "seeds from.",
          "<b>Tokens constructed from a timestamp, a counter, a hash of "
          "predictable inputs, or a sequential database "
          "identifier</b> — all of which are unique and none of "
          "which are unguessable.",
          "<b>UUID version 1 used as a secret.</b> <b>It encodes a "
          "timestamp and a network address and is designed for "
          "uniqueness, not unguessability</b> — use version 4 from a "
          "CSPRNG, or better, <code>secrets.token_urlsafe</code>.",
          "<b>And key generation at install time or first boot</b>, "
          "which is &sect;3's embedded-device failure arriving in your "
          "own provisioning script. <b>'Unique' and 'unguessable' are "
          "different requirements</b>, and UUID conflates them in the "
          "mind of nearly every developer who reaches for one."]),
 ],
 "resources": [
   ("Aumasson &mdash; Serious Cryptography, chapter 2",
    "https://nostarch.com/serious-cryptography-2nd-edition",
    "<b>The whole module</b>, with more detail on the entropy pool "
    "design and the hardware source question."),
   ("Heninger et al. &mdash; Mining Your Ps and Qs (free)",
    "https://factorable.net/",
    "<b>&sect;3's third failure, measured at internet scale</b> — "
    "the study that found hundreds of thousands of devices with shared or "
    "factorable keys."),
   ("Myths about /dev/urandom (free)",
    "https://www.2uo.de/myths-about-urandom/",
    "<b>&sect;2's folklore, dismantled carefully</b> — read it once "
    "and stop worrying about this."),
   ("NIST SP 800-90A/B/C (free)",
    "https://csrc.nist.gov/publications/detail/sp/800-90a/rev-1/final",
    "<b>The standards for CSPRNG construction and entropy "
    "assessment</b> — reference rather than reading, but worth "
    "knowing exists."),
 ],
 "exercises": [
   "<b>Generate 1000 values from your language's default random "
   "module</b> and from its CSPRNG, and confirm both pass a basic "
   "statistical test.",
   "<b>Recover a Mersenne Twister's state</b> from its output, and "
   "predict the next value.",
   "<b>Explain why that is possible</b> for one and not the other.",
   "<b>Grep a codebase for non-cryptographic random imports</b> and "
   "classify each use as safe or not.",
   "<b>Find any explicit seeding</b> and determine what it seeds "
   "from.",
   "<b>Find how your platform's CSPRNG behaves at early boot</b>, and "
   "whether it blocks.",
   "<b>Write the five-row requirements table from memory</b> and check "
   "it.",
   "<b>Audit your own token generation</b> for every token type your "
   "system issues.",
   "<b>Check whether any of your tokens are single-use</b> and expiring "
   "where they should be.",
   "<b>Determine what your application would have to do</b> to rotate "
   "every key after a randomness failure.",
 ],
 "selfcheck": [
   "Name the three kinds and what each is for.",
   "Why is a Mersenne Twister dangerous despite passing every "
   "statistical test?",
   "What property does a CSPRNG add, and how does it relate to "
   "Module 01 §3?",
   "Name the correct source on three platforms, and four things never to "
   "use.",
   "What is the truth about /dev/random versus /dev/urandom?",
   "Give five historical randomness failures.",
   "Why are randomness failures silent, and why retroactive?",
   "What does a nonce require that a key does not, and vice versa?",
   "Why can a counter be a valid nonce, and what makes that hard?",
   "Why is UUIDv1 unsuitable as a secret?",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Symmetric Encryption",
 "subtitle": "Confidentiality, and the modes that provide it.",
 "question": "How do you turn a block cipher into something usable?",
 "outcomes": [
     "Explain what a block cipher is and is not.",
     "Explain why ECB is unacceptable and what it reveals.",
     "Explain CTR and CBC and their requirements.",
     "Explain stream ciphers and their single fatal misuse.",
     "Choose a mode, and explain why you should not have to.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The block cipher",
   "blurb": "A primitive, not a scheme."},

  {"t": "callout", "title": "A block cipher is a keyed permutation on fixed-size blocks, and nothing more",
   "kind": "What the primitive actually is",
   "body": ["<b>AES maps a 16-byte block to a 16-byte block, "
            "invertibly, under a key</b> — and <b>for each key it "
            "is a different permutation of the 2¹²⁸ possible "
            "blocks.</b>",
            "<b>The security goal is to be indistinguishable from a "
            "random permutation</b> — an adversary with "
            "encrypt-and-decrypt access cannot tell AES under an unknown "
            "key from a randomly chosen permutation.",
            "<b>But a single block is not a message.</b> <b>Encrypting "
            "a long message requires a <i>mode of operation</i>, and the "
            "mode is where the real design decisions and the real "
            "failures are.</b>",
            "<b>So AES is not an encryption scheme</b> — <b>it is "
            "a component of one</b>, and this distinction is the "
            "entire content of this module."]},

  {"t": "section", "label": "Part 2", "title": "ECB",
   "blurb": "The mode that teaches by failing."},

  {"t": "callout", "title": "Encrypting each block independently leaks every repetition",
   "kind": "ECB, and why it is in this course",
   "body": ["<b>ECB applies the block cipher to each block "
            "separately</b> — so <b>identical plaintext blocks "
            "produce identical ciphertext blocks</b>, always and "
            "visibly.",
            "<b>Which means structure survives encryption.</b> "
            "<b>The classic demonstration encrypts a bitmap and the "
            "image remains recognisable</b> — the shapes are "
            "preserved exactly, because the repetition pattern is.",
            "<b>And it fails the Module 01 §3 definition "
            "immediately:</b> <b>an adversary submits one plaintext of "
            "two identical blocks and one of two different blocks, and "
            "distinguishes them with certainty.</b>",
            "<b>So ECB is unacceptable for any message longer than one "
            "block</b> — and <b>it is worth knowing precisely why, "
            "because 'AES' in a system specification does not tell you "
            "the mode.</b>"]},

  {"t": "code", "kicker": "Modes", "title": "The modes, and what each needs",
   "lang": "text", "code": """
  ECB   block by block, independently.
        Needs: nothing. Leaks: all repetition. Never use.

  CBC   each plaintext block XORed with the previous
        ciphertext block before encryption.
        Needs: an unpredictable IV, and padding.
        Hazards: padding oracles; IV reuse leaks the
        first-block relationship; not parallelisable
        for encryption.

  CTR   encrypt a counter, XOR the result with the
        plaintext. Turns a block cipher into a stream
        cipher.
        Needs: a nonce that NEVER repeats per key.
        No padding. Parallelisable. Hazard: nonce
        reuse is catastrophic (Module 11).

  AND NONE OF THESE AUTHENTICATE ANYTHING. All three
  provide confidentiality only, which is why Module 04
  exists and why you should be using AEAD instead.
""",
   "caption": "<b>The last paragraph is the point of the slide</b> "
              "— every mode here is a confidentiality-only "
              "construction.",
   "note": "Students who learn modes without this caveat build "
           "unauthenticated systems."},

  {"t": "section", "label": "Part 3", "title": "Stream ciphers",
   "blurb": "And the one thing you must never do."},

  {"t": "eq", "kicker": "Stream cipher", "title": "The construction, and the misuse it invites",
   "eqs": [
     ("c = m ⊕ KS(k, n)",
      "The keystream KS depends only on the key and the nonce. XOR "
      "is the whole of the encryption."),
     ("c₁ ⊕ c₂ = m₁ ⊕ m₂    if the nonce n is reused",
      "The keystream cancels. The key has left the equation "
      "entirely, and the adversary did nothing clever."),
     ("two plaintexts XORed  ⟹  both usually recoverable",
      "A classical two-time-pad problem, solvable for any plaintext "
      "with structure — which is all real plaintext."),
   ],
   "caption": "<b>Nonce reuse in a stream cipher removes the key "
              "entirely</b> — the adversary is left with a classical "
              "two-time-pad problem, which is solvable.",
   "note": "This equation is the single most important one in the "
           "course."},

  {"t": "callout", "title": "ChaCha20 is the stream cipher to know",
   "kind": "And why it displaced the alternatives",
   "body": ["<b>It is fast in software without hardware "
            "acceleration</b> — which matters on mobile and embedded "
            "targets where AES instructions are absent.",
            "<b>It is structurally simple:</b> <b>additions, "
            "rotations, and XORs on a 512-bit state</b> — which "
            "makes constant-time implementation straightforward rather "
            "than delicate (Module 11 §1).",
            "<b>And it pairs with Poly1305 into an AEAD "
            "construction</b> (Module 04) that is the default choice "
            "wherever AES-GCM's hardware support is unavailable.",
            "<b>But it inherits the fatal requirement:</b> <b>the "
            "nonce must never repeat for a given key</b> — which "
            "is why the libsodium API generates it for you and does not "
            "offer the option."]},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "And why the answer is to not choose."},

  {"t": "bullets", "kicker": "Practice", "title": "What to actually do",
   "items": [
     "<b>Use an AEAD construction</b> (Module 04) — "
     "<b>AES-GCM, ChaCha20-Poly1305, or AES-GCM-SIV</b>. Not a "
     "confidentiality-only mode.",
     "",
     "<b>Use the library's one-call interface</b>, which handles the "
     "nonce, the tag, and the encoding together.",
     "",
     "<b>AES where hardware acceleration exists</b> (nearly all "
     "server and desktop CPUs); <b>ChaCha20 where it does "
     "not.</b>",
     "",
     "<b>And if you are selecting a mode by name, you have gone "
     "wrong somewhere</b> — which is Module 01 §4's "
     "IV test in a different form.",
     "",
     "<b>This module exists so that you can read an existing system "
     "and assess it</b>, not so that you can assemble a new one.",
   ],
   "footnote": "<b>The honest purpose of this module is "
               "diagnostic:</b> you will inherit systems specified as "
               "'AES-encrypted', and you now know that sentence is "
               "incomplete."},
 ],
 "takeaways": [
   "A block cipher is a keyed permutation on fixed-size blocks, not an "
   "encryption scheme — the mode of operation is where the design "
   "decisions and failures are.",
   "ECB leaks every repetition and fails the indistinguishability "
   "definition with a two-block message, which is why the encrypted bitmap "
   "stays recognisable.",
   "CBC needs an unpredictable IV and padding; CTR needs a nonce that "
   "never repeats and needs no padding.",
   "No confidentiality-only mode authenticates anything, which is why "
   "AEAD is the only acceptable default.",
   "Nonce reuse in a stream cipher cancels the key and leaves the "
   "adversary with two plaintexts XORed together.",
   "If you are selecting a mode by name, you have gone wrong — this "
   "module is for reading existing systems, not building new ones.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The block cipher"),
  ("callout", "A block cipher is a keyed permutation on fixed-size blocks, "
              "and nothing more",
   ["<b>AES maps a 16-byte block to a 16-byte block, invertibly, under "
    "a key</b> — and <b>for each distinct key it is a different "
    "permutation of the 2<sup>128</sup> possible blocks</b>, selected "
    "from an astronomically large family.",
    "<b>The security goal is indistinguishability from a random "
    "permutation:</b> an adversary permitted to encrypt and decrypt "
    "blocks of their choosing cannot tell AES under an unknown key from a "
    "permutation chosen uniformly at random — which is "
    "Module 01 &sect;3's framing applied to the primitive.",
    "<b>But a single block is not a message.</b> <b>Encrypting "
    "anything longer requires a <i>mode of operation</i>, and the mode is "
    "where the real design decisions and essentially all of the real "
    "failures live</b> — AES itself has no practical break after "
    "twenty-five years of attention.",
    "<b>So AES is not an encryption scheme.</b> <b>It is a component "
    "of one</b>, and this distinction is the entire content of this "
    "module — which is why 'we use AES-256' in a system "
    "specification conveys almost no information about the system's "
    "security."]),

  ("h1", "2 &nbsp; ECB, and what it teaches"),
  ("callout", "Encrypting each block independently leaks every repetition",
   ["<b>ECB mode applies the block cipher to each plaintext block "
    "separately and independently</b> — so <b>identical plaintext "
    "blocks produce identical ciphertext blocks</b>, always, visibly, and "
    "across the whole message.",
    "<b>Which means structure survives encryption intact.</b> <b>The "
    "classic demonstration encrypts a simple bitmap in ECB mode and the "
    "image remains plainly recognisable</b> — edges, shapes, and "
    "text all legible — because the repetition pattern of the "
    "plaintext is preserved exactly in the ciphertext.",
    "<b>And it fails the Module 01 &sect;3 definition "
    "immediately.</b> <b>An adversary submits one plaintext consisting "
    "of two identical blocks and one consisting of two different blocks, "
    "and distinguishes the ciphertexts with certainty</b> — "
    "advantage 1, which is as badly as a scheme can fail.",
    "<b>So ECB is unacceptable for any message longer than a single "
    "block</b> — and <b>it is worth knowing precisely why, because "
    "'AES' in a specification does not tell you the mode</b>, and ECB "
    "remains the default in more than one widely used library's "
    "lowest-level interface."]),
  ("code", """ECB   block by block, independently.
      Needs: nothing. Leaks: all repetition. Never use.

CBC   each plaintext block XORed with the previous
      ciphertext block before encryption.
      Needs: an unpredictable IV, and padding.
      Hazards: padding oracles; IV reuse leaks the
      first-block relationship; not parallelisable
      for encryption.

CTR   encrypt a counter, XOR the result with the
      plaintext. Turns a block cipher into a stream
      cipher.
      Needs: a nonce that NEVER repeats per key.
      No padding. Parallelisable. Hazard: nonce
      reuse is catastrophic (Module 11).

AND NONE OF THESE AUTHENTICATE ANYTHING. All three
provide confidentiality only, which is why Module 04
exists and why you should be using AEAD instead."""),
  ("p", "<b>The last paragraph is the point of the slide.</b> <b>Every "
        "mode listed is a confidentiality-only construction</b>, and "
        "<b>students who learn the modes without that caveat go on to "
        "build unauthenticated systems</b> — which is the failure "
        "Module 01 &sect;1's callout describes and Module 04 "
        "exists to prevent. <b>CBC's padding oracle hazard is worth "
        "noting specifically</b>: a system that reports padding errors "
        "distinguishably from other errors can have its plaintext "
        "recovered without the key, which is a decryption failure arising "
        "entirely from error handling."),

  ("break",),
  ("h1", "3 &nbsp; Stream ciphers"),
  ("eq", "c = m &oplus; KS(k, n) &nbsp;&nbsp;&nbsp; so &nbsp;&nbsp; "
         "c<sub>1</sub> &oplus; c<sub>2</sub> = m<sub>1</sub> &oplus; "
         "m<sub>2</sub> &nbsp; if n is reused"),
  ("ul", ["<b>KS(k, n)</b> &mdash; a keystream of arbitrary length "
          "generated deterministically from the key and the nonce.",
          "<b>&oplus;</b> &mdash; bitwise XOR, which is the entirety "
          "of the encryption operation. The cipher's work is producing "
          "the keystream.",
          "<b>c<sub>1</sub> &oplus; c<sub>2</sub></b> &mdash; what an "
          "adversary computes directly from two ciphertexts if the nonce "
          "repeats under the same key.",
          "<b>The consequence</b> &mdash; <b>the keystream cancels "
          "and the key disappears from the equation entirely</b>, leaving "
          "the adversary with two plaintexts XORed together. <b>That is "
          "a classical two-time-pad problem and it is solvable</b> for "
          "any plaintexts with structure, which is all real "
          "plaintexts. <b>This is the single most important equation in "
          "the course</b>, and Module 11 &sect;2 returns to it."]),
  ("callout", "ChaCha20 is the stream cipher to know",
   ["<b>It is fast in software without hardware acceleration</b> — "
    "which matters on mobile, embedded, and older targets where AES "
    "instructions are absent and software AES is both slow and hard to "
    "make constant-time.",
    "<b>It is structurally simple:</b> <b>additions, rotations, and "
    "XORs on a 512-bit state, with no lookup tables</b> — which "
    "makes a constant-time implementation straightforward rather than "
    "delicate, because there are no data-dependent memory accesses to "
    "leak through the cache (Module 11 &sect;1).",
    "<b>And it pairs with the Poly1305 authenticator into an AEAD "
    "construction</b> (Module 04) <b>that is the default choice "
    "wherever AES-GCM's hardware support is unavailable</b> — and is "
    "specified in TLS 1.3 for exactly that reason (Module 08).",
    "<b>But it inherits the fatal requirement of every stream "
    "cipher:</b> <b>the nonce must never repeat for a given key</b> "
    "— which is why the libsodium interface generates the nonce "
    "itself and simply does not offer you the option of supplying "
    "one. <b>That API decision is Module 01 &sect;4's rule in "
    "concrete form.</b>"]),

  ("h1", "4 &nbsp; Choosing, and why you should not have to"),
  ("ul", ["<b>Use an AEAD construction</b> (Module 04) — "
          "<b>AES-GCM, ChaCha20-Poly1305, or AES-GCM-SIV</b>, and not "
          "any confidentiality-only mode from &sect;2 regardless of how "
          "carefully you intend to add authentication yourself.",
          "<b>Use the library's single-call interface</b>, which "
          "handles the nonce generation, the authentication tag, and the "
          "output encoding together as one operation that cannot be "
          "half-performed.",
          "<b>AES where hardware acceleration exists</b> — nearly "
          "every current server and desktop processor — <b>and "
          "ChaCha20 where it does not.</b> <b>This is the only "
          "legitimate choice in the module</b>, and most libraries will "
          "make it for you.",
          "<b>And if you find yourself selecting a mode by name, you "
          "have gone wrong somewhere</b> — which is Module 01 "
          "&sect;4's IV test in a slightly different form, and it applies "
          "equally.",
          "<b>This module exists so that you can read an existing "
          "system and assess it</b>, not so that you can assemble a new "
          "one. <b>The honest purpose is diagnostic:</b> you will "
          "inherit systems documented as 'AES-encrypted', and you now "
          "know that sentence is incomplete in at least three "
          "respects — mode, authentication, and key management."]),
 ],
 "resources": [
   ("Boneh & Shoup, chapters 3 through 5 (free)",
    "https://toc.cryptobook.us/",
    "<b>&sect;1 through &sect;3 rigorously</b> — including the "
    "proofs that CTR and CBC achieve the Module 01 &sect;3 "
    "definition given their requirements."),
   ("Aumasson &mdash; Serious Cryptography, chapters 4 and 5",
    "https://nostarch.com/serious-cryptography-2nd-edition",
    "<b>The modes and stream ciphers at engineering level</b>, with the "
    "practical hazards foregrounded."),
   ("RFC 8439 &mdash; ChaCha20 and Poly1305 (free)",
    "https://www.rfc-editor.org/rfc/rfc8439",
    "<b>&sect;3's specification</b>, and short enough to implement "
    "from — which is one of Project 1's options."),
   ("The ECB penguin, and why it persists (free)",
    "https://words.filippo.io/the-ecb-penguin/",
    "<b>&sect;2's demonstration, with the nuance</b> about what the "
    "image does and does not prove."),
 ],
 "exercises": [
   "<b>Encrypt a bitmap in ECB mode</b> and look at the result.",
   "<b>Construct the two-block distinguishing attack</b> on ECB and "
   "state the advantage you achieve.",
   "<b>Encrypt the same plaintext twice in CBC with the same IV</b> and "
   "compare the ciphertexts.",
   "<b>Do the same with CTR and the same nonce</b>, then XOR the two "
   "ciphertexts together.",
   "<b>Recover both plaintexts</b> from that XOR, given that one is "
   "English text.",
   "<b>Write out why the key vanished</b> from the equation.",
   "<b>Time software AES against ChaCha20</b> on a machine without AES "
   "instructions, if you have one.",
   "<b>Find a library whose lowest-level API defaults to ECB</b>, and "
   "read its documentation's warning.",
   "<b>Take one system you did not build</b> and determine its actual "
   "mode and whether it authenticates.",
   "<b>Rewrite one confidentiality-only use</b> as an AEAD call.",
 ],
 "selfcheck": [
   "What exactly is a block cipher, and what is its security goal?",
   "Why is AES not an encryption scheme?",
   "Why does ECB leave a bitmap recognisable?",
   "Give the two-block attack and the advantage it achieves.",
   "What does CBC need, and what are its three hazards?",
   "What does CTR need, and what does it not need?",
   "What do all three modes fail to provide?",
   "Write the stream cipher equation and say what happens on nonce "
   "reuse.",
   "Why did ChaCha20 displace the alternatives, and what does it "
   "inherit?",
   "What should you actually use, and what is this module really for?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Authenticated Encryption",
 "subtitle": "The only acceptable default.",
 "question": "Why is encryption without authentication a vulnerability?",
 "outcomes": [
     "Explain what a MAC provides and how to use one.",
     "Explain the composition orders and which is safe.",
     "Explain AEAD and associated data.",
     "Name the AEAD constructions and choose between them.",
     "Explain why verification must precede use.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The MAC",
   "blurb": "Integrity and authentication in one primitive."},

  {"t": "callout", "title": "A MAC is a keyed tag that only a keyholder can produce and verify",
   "kind": "The primitive",
   "body": ["<b>Given a key and a message it produces a short "
            "tag</b> — and <b>without the key, producing a valid "
            "tag for any new message is infeasible.</b>",
            "<b>So it provides integrity and authentication "
            "together</b> (Module 01 §1): a valid tag means "
            "the message was not modified <i>and</i> came from a "
            "keyholder.",
            "<b>HMAC is the construction to know</b> — built from "
            "any hash function, well understood, and not vulnerable to "
            "the length-extension problem the bare hash has "
            "(Module 05 §3).",
            "<b>And a hash is not a MAC.</b> <b>An unkeyed hash can "
            "be recomputed by anyone, so it detects accidental "
            "corruption and nothing adversarial</b> — which is the "
            "most common misuse of a hash function."]},

  {"t": "callout", "title": "Tag comparison must be constant-time",
   "kind": "A one-line defect with a real consequence",
   "body": ["<b>A normal string comparison returns as soon as it finds "
            "a difference</b> — so the time it takes reveals how "
            "many leading bytes matched.",
            "<b>Which lets an adversary forge a tag byte by "
            "byte.</b> <b>Guess the first byte 256 ways, keep the one "
            "that took longest, move to the second</b> — linear "
            "work instead of exponential.",
            "<b>So every library provides a constant-time "
            "comparison</b> — <code>hmac.compare_digest</code>, "
            "<code>sodium_memcmp</code>, "
            "<code>subtle.ConstantTimeCompare</code> — and "
            "<b>using <code>==</code> on a tag is a defect.</b>",
            "<b>This is Module 11 §1's whole subject "
            "appearing early</b>, because it is the one timing attack "
            "that shows up in ordinary application code rather than in a "
            "primitive."]},

  {"t": "section", "label": "Part 2", "title": "Composition",
   "blurb": "Three orders, one of them sound."},

  {"t": "table", "kicker": "Composition", "title": "Encrypt and MAC: the three orders",
   "header": ["Order", "What it does", "Verdict"],
   "widths": [2.8, 4.2, 4.8],
   "rows": [
     ["<b>Encrypt-then-MAC</b>", "<b>MAC the ciphertext</b>", "<b>Sound. Invalid ciphertext rejected before decryption</b>"],
     ["<b>MAC-then-encrypt</b>", "<b>MAC the plaintext, encrypt both</b>", "<b>Must decrypt to verify — hazardous</b>"],
     ["<b>Encrypt-and-MAC</b>", "<b>MAC the plaintext, send alongside</b>", "<b>Unsound — the tag can leak plaintext</b>"],
   ],
   "footnote": "<b>Encrypt-then-MAC is the only order that is "
               "generically secure</b>, and the reason is that it lets "
               "you reject a forged ciphertext without ever processing "
               "attacker-controlled plaintext.",
   "note": "The reject-before-decrypt property is the practical "
           "argument."},

  {"t": "callout", "title": "And the correct answer is to compose nothing",
   "kind": "Why AEAD exists",
   "body": ["<b>Encrypt-then-MAC is sound and still has to be built "
            "correctly:</b> <b>two keys, derived separately; the right "
            "byte ranges covered; the tag checked before any "
            "parsing.</b>",
            "<b>And each of those is a place to make a mistake that no "
            "test will catch</b> — a MAC over the ciphertext but not "
            "the IV, for instance, which has appeared in real "
            "systems.",
            "<b>So use an AEAD primitive, which performs the "
            "composition internally and exposes one call.</b> <b>There "
            "is no order to get wrong because there is no order to "
            "choose.</b>",
            "<b>Which is why Part 2 is diagnostic rather than "
            "instructional</b> — <b>you learn the orders so that you "
            "can audit an existing system, not so that you can build "
            "one.</b>"]},

  {"t": "section", "label": "Part 3", "title": "AEAD",
   "blurb": "And what associated data is for."},

  {"t": "code", "kicker": "AEAD", "title": "The interface, and the associated data",
   "lang": "text", "code": """
  encrypt(key, nonce, plaintext, associated_data)
      -> ciphertext_with_tag

  decrypt(key, nonce, ciphertext_with_tag, associated_data)
      -> plaintext, OR an error. Never both.

  ASSOCIATED DATA is authenticated but NOT encrypted. It
  is for the context that must not be tampered with and
  must stay readable:
      a record identifier, so a valid ciphertext cannot
          be moved to a different record
      a version or algorithm label, so it cannot be
          downgraded
      a recipient identifier, so a message cannot be
          replayed at someone else
      routing headers that intermediaries must read

  THE DECRYPTION CONTRACT: on tag failure you get an
  error and NO plaintext. Not partial output, not
  "probably fine". This is the property the whole
  construction exists to give you.
""",
   "caption": "<b>Associated data binds the ciphertext to its "
              "context</b> — which prevents a whole class of "
              "valid-ciphertext-in-the-wrong-place attacks.",
   "note": "Associated data is underused; the record-identifier "
           "example is the one that lands."},

  {"t": "bullets", "kicker": "Constructions", "title": "The AEAD constructions, and when to use each",
   "items": [
     "<b>AES-GCM.</b> <b>The default where AES hardware "
     "acceleration exists</b> — fast, standardised, widely "
     "implemented. <b>Nonce reuse is catastrophic and also forfeits "
     "the authentication key.</b>",
     "",
     "<b>ChaCha20-Poly1305.</b> <b>The default without AES "
     "hardware</b> — fast in software, easy to implement in "
     "constant time (Module 03 §3).",
     "",
     "<b>AES-GCM-SIV.</b> <b>Nonce-misuse resistant</b>: a repeated "
     "nonce leaks only whether two plaintexts were equal, rather than "
     "everything. <b>Use it where you cannot guarantee "
     "uniqueness.</b>",
     "",
     "<b>XChaCha20-Poly1305.</b> <b>A 192-bit nonce, so a random "
     "nonce is safe indefinitely</b> — which removes the counter "
     "management problem entirely.",
     "",
     "<b>And libsodium's <code>crypto_secretbox</code></b>, which "
     "makes every one of these decisions for you.",
   ],
   "footnote": "<b>The misuse-resistant options are "
               "underused:</b> if your nonce discipline depends on "
               "distributed coordination, XChaCha20 or GCM-SIV removes "
               "the dependency."},

  {"t": "section", "label": "Part 4", "title": "The discipline",
   "blurb": "Verify before you use anything."},

  {"t": "callout", "title": "Verify the tag before you parse, decompress, or log anything",
   "kind": "The rule that makes AEAD worth having",
   "body": ["<b>The guarantee is only worth something if you act on "
            "it.</b> <b>Code that decrypts, parses the result, and "
            "<i>then</i> checks the tag has already processed "
            "attacker-controlled input.</b>",
            "<b>And the leak need not be the plaintext.</b> <b>An "
            "error message, a timing difference, a log line, or a "
            "distinguishable failure mode is enough to build a "
            "decryption oracle</b> — which is how padding oracle "
            "attacks work.",
            "<b>So: one error, indistinguishable, for every "
            "failure.</b> <b>Not 'bad padding' versus 'bad tag' "
            "versus 'bad length'</b> — the distinction is the "
            "vulnerability.",
            "<b>A proper AEAD library enforces this by returning "
            "nothing on failure</b> — <b>which is another case of "
            "the API preventing the mistake rather than the "
            "documentation warning about it.</b>"]},
 ],
 "takeaways": [
   "A MAC gives integrity and authentication together; an unkeyed hash "
   "gives neither, because anyone can recompute it.",
   "Tag comparison must be constant-time — a byte-at-a-time timing "
   "leak turns forgery from exponential to linear work.",
   "Encrypt-then-MAC is the only generically sound order, because it "
   "rejects forged ciphertext before decrypting it.",
   "The correct answer is to compose nothing and use an AEAD primitive, "
   "which has no order to get wrong.",
   "Associated data is authenticated but not encrypted, and binds a "
   "ciphertext to its record, version, or recipient.",
   "Verify the tag before parsing, decompressing, or logging — and "
   "report one indistinguishable error for every failure.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The MAC"),
  ("callout", "A MAC is a keyed tag that only a keyholder can produce or "
              "verify",
   ["<b>Given a key and a message it produces a short tag</b> — "
    "typically 16 or 32 bytes — and <b>without the key, producing a "
    "valid tag for any message the keyholder has not already tagged is "
    "computationally infeasible.</b>",
    "<b>So it provides integrity and authentication together</b> "
    "(Module 01 &sect;1): <b>a valid tag means the message was not "
    "modified <i>and</i> that it came from somebody holding the "
    "key</b> — two of the four properties, from one primitive.",
    "<b>HMAC is the construction to know.</b> <b>It is built from any "
    "hash function, is extremely well understood, and is specifically not "
    "vulnerable to the length-extension problem that a naive "
    "hash-the-key-and-message construction has</b> (Module 05 "
    "&sect;3) — which is exactly why HMAC's nested structure looks "
    "odd.",
    "<b>And a hash is not a MAC.</b> <b>An unkeyed hash can be "
    "recomputed by anyone, including the adversary who modified the "
    "message, so it detects accidental corruption and nothing "
    "adversarial whatsoever</b> — <b>which is the single most "
    "common misuse of a hash function</b> and appears in production "
    "systems as 'we hash it to make sure it wasn't tampered with'."]),
  ("callout", "Tag comparison must be constant-time",
   ["<b>A normal string or byte comparison returns as soon as it finds "
    "a difference</b> — that is what makes it fast — <b>so the "
    "time it takes reveals how many leading bytes matched.</b>",
    "<b>Which lets an adversary forge a tag one byte at a time.</b> "
    "<b>Guess the first byte in all 256 ways, keep whichever request "
    "took measurably longest, then move to the second byte</b> — "
    "<b>256 &times; 16 attempts instead of 2<sup>128</sup></b>, which is "
    "the difference between infeasible and an afternoon.",
    "<b>So every serious library provides a constant-time "
    "comparison</b> — <code>hmac.compare_digest</code> in Python, "
    "<code>sodium_memcmp</code>, Go's "
    "<code>subtle.ConstantTimeCompare</code> — and <b>using "
    "<code>==</code> or <code>memcmp</code> on an authentication tag is a "
    "defect</b>, however obviously correct it looks in review.",
    "<b>This is Module 11 &sect;1's whole subject appearing "
    "early</b>, because <b>it is the one timing attack that shows up in "
    "ordinary application code</b> rather than inside a primitive "
    "implementation — so it is the one you are personally likely to "
    "write."]),

  ("h1", "2 &nbsp; Composition"),
  ("table", ["Order", "What it does", "Verdict"],
   [["<b>Encrypt-then-MAC</b>",
     "<b>Encrypt the plaintext, then MAC the ciphertext (and the IV, and "
     "the header).</b>",
     "<b>Sound.</b> <b>An invalid ciphertext is rejected before "
     "decryption is attempted</b>, which is the practical property that "
     "matters."],
    ["<b>MAC-then-encrypt</b>",
     "<b>MAC the plaintext, then encrypt the plaintext and the tag "
     "together.</b>",
     "<b>You must decrypt in order to verify</b>, so you process "
     "attacker-controlled data before authenticating it — hazardous, "
     "and the source of several real attacks."],
    ["<b>Encrypt-and-MAC</b>",
     "<b>MAC the plaintext, encrypt the plaintext, send both.</b>",
     "<b>Unsound generically</b> — the tag is a deterministic "
     "function of the plaintext, so identical plaintexts produce "
     "identical tags, leaking equality."]],
   [0.22, 0.36, 0.42]),
  ("callout", "And the correct answer is to compose nothing",
   ["<b>Encrypt-then-MAC is sound and still has to be built "
    "correctly:</b> <b>two independent keys, properly derived rather "
    "than reused; the right byte ranges covered; the tag checked before "
    "any parsing takes place.</b>",
    "<b>And every one of those is a place to make a mistake that no "
    "functional test will catch</b> — <b>a MAC computed over the "
    "ciphertext but not over the IV</b>, for instance, which permits an "
    "adversary to change the IV and thereby the first plaintext block, "
    "and which has appeared in deployed systems more than once.",
    "<b>So use an AEAD primitive, which performs the composition "
    "internally and exposes a single call.</b> <b>There is no order to "
    "get wrong, because there is no order to choose</b> — the "
    "decision was made once, by people who prove things, and baked into "
    "the construction.",
    "<b>Which is why &sect;2 is diagnostic rather than "
    "instructional.</b> <b>You learn the three orders so that you can "
    "audit an existing system and recognise which one it implements</b>, "
    "not so that you can implement one yourself — and the same "
    "framing applies to Module 03 &sect;4."]),

  ("break",),
  ("h1", "3 &nbsp; AEAD"),
  ("code", """encrypt(key, nonce, plaintext, associated_data)
    -> ciphertext_with_tag

decrypt(key, nonce, ciphertext_with_tag, associated_data)
    -> plaintext, OR an error. Never both.

ASSOCIATED DATA is authenticated but NOT encrypted. It is
for context that must not be tampered with and must stay
readable:
    a record identifier, so a valid ciphertext cannot be
        moved to a different record
    a version or algorithm label, so it cannot be
        downgraded
    a recipient identifier, so a message cannot be
        replayed at someone else
    routing headers that intermediaries must read

THE DECRYPTION CONTRACT: on tag failure you receive an
error and NO plaintext. Not partial output, not a
"probably fine". This is the property the whole
construction exists to provide."""),
  ("p", "<b>Associated data binds the ciphertext to its context</b>, and "
        "<b>it is substantially underused.</b> <b>The record-identifier "
        "case is the one that lands:</b> without it, an adversary with "
        "write access to your database can move a validly encrypted, "
        "validly authenticated value from row 7 to row 9 — every "
        "cryptographic check passes, and the data is now wrong in a way "
        "your application will trust. <b>With the row identifier as "
        "associated data, that ciphertext fails to authenticate in its new "
        "position.</b>"),
  ("ul", ["<b>AES-GCM.</b> <b>The default wherever AES hardware "
          "acceleration exists</b> — fast, standardised, and "
          "implemented everywhere. <b>Nonce reuse is catastrophic and "
          "additionally forfeits the authentication key itself</b>, which "
          "is worse than for a plain stream cipher (Module 11 "
          "&sect;2).",
          "<b>ChaCha20-Poly1305.</b> <b>The default where AES "
          "hardware is absent</b> — fast in software and "
          "straightforward to implement in constant time (Module 03 "
          "&sect;3). Specified in TLS 1.3 for this reason.",
          "<b>AES-GCM-SIV.</b> <b>Nonce-misuse resistant:</b> a "
          "repeated nonce leaks only whether two plaintexts were "
          "identical, rather than destroying confidentiality and "
          "authenticity outright. <b>Use it wherever you cannot "
          "genuinely guarantee nonce uniqueness.</b>",
          "<b>XChaCha20-Poly1305.</b> <b>A 192-bit nonce, which makes "
          "a randomly generated nonce safe indefinitely</b> by the "
          "birthday bound — <b>removing the counter management "
          "problem entirely</b>, which is the right trade for most "
          "distributed systems.",
          "<b>And libsodium's <code>crypto_secretbox</code></b>, which "
          "makes every one of these decisions on your behalf. <b>The "
          "misuse-resistant options are underused:</b> if your nonce "
          "discipline depends on distributed coordination (CSCE 678 "
          "Module 05), XChaCha20 or GCM-SIV removes that dependency, "
          "which is worth more than the marginal performance."]),

  ("h1", "4 &nbsp; The discipline"),
  ("callout", "Verify the tag before you parse, decompress, or log anything",
   ["<b>The guarantee is only worth something if you act on it.</b> "
    "<b>Code that decrypts, parses the result, and <i>then</i> checks the "
    "tag has already processed attacker-controlled input</b> — "
    "through a parser, which is exactly where the memory-safety and "
    "injection bugs are (CSCE 713).",
    "<b>And the leak need not be the plaintext itself.</b> <b>A "
    "distinguishable error message, a measurable timing difference, a log "
    "line, or any observable difference between failure modes is enough "
    "to construct a decryption oracle</b> — which is precisely how "
    "padding oracle attacks recover plaintext without the key, using "
    "nothing but the server's error behaviour.",
    "<b>So: one error, indistinguishable, for every failure.</b> "
    "<b>Not 'bad padding' versus 'bad tag' versus 'malformed length' "
    "versus 'unknown key identifier'</b> — <b>the distinction is "
    "the vulnerability</b>, and the helpful error message is the "
    "defect. Log the detail internally; return one opaque failure.",
    "<b>A proper AEAD library enforces this by returning nothing at "
    "all on failure</b> — no partial plaintext, no diagnostic "
    "— <b>which is another case of the API preventing the mistake "
    "rather than the documentation warning about it</b>, and is the "
    "pattern Module 01 &sect;4 asks you to look for when choosing "
    "between libraries."]),
 ],
 "resources": [
   ("Boneh & Shoup, chapters 6 through 9 (free)",
    "https://toc.cryptobook.us/",
    "<b>MACs and authenticated encryption with the proofs</b> — "
    "including why encrypt-then-MAC is generically secure and the others "
    "are not."),
   ("Aumasson &mdash; Serious Cryptography, chapters 7 through 9",
    "https://nostarch.com/serious-cryptography-2nd-edition",
    "<b>&sect;1 through &sect;3 at engineering level</b>, with the "
    "construction comparisons laid out practically."),
   ("RFC 5116 and RFC 8452 (AEAD interface; AES-GCM-SIV) (free)",
    "https://www.rfc-editor.org/rfc/rfc5116",
    "<b>&sect;3's interface as standardised</b>, and the "
    "misuse-resistant construction's specification and rationale."),
   ("Rizzo & Duong on padding oracles (free)",
    "https://www.usenix.org/legacy/event/woot10/tech/full_papers/Rizzo.pdf",
    "<b>&sect;4's argument, demonstrated</b> — plaintext recovery "
    "from nothing but distinguishable error behaviour."),
 ],
 "exercises": [
   "<b>Write a MAC verification with <code>==</code></b> and measure the "
   "timing difference across first-byte guesses.",
   "<b>Replace it with the constant-time comparison</b> and measure "
   "again.",
   "<b>Find one place in code you have access to</b> where a hash is "
   "used where a MAC is needed.",
   "<b>Implement encrypt-then-MAC manually</b>, then list every detail "
   "you had to get right.",
   "<b>Deliberately omit the IV from the MAC</b> and show what an "
   "adversary can then change.",
   "<b>Replace the whole thing with one AEAD call</b> and compare the "
   "line counts.",
   "<b>Use associated data to bind a ciphertext to a record "
   "identifier</b>, then try moving it.",
   "<b>Confirm your AEAD library returns nothing on tag failure</b>, "
   "rather than partial plaintext.",
   "<b>Audit your error handling</b> for distinguishable decryption "
   "failures.",
   "<b>Pick between XChaCha20 and AES-GCM for your own system</b> and "
   "justify it on nonce management.",
 ],
 "selfcheck": [
   "What does a MAC provide, and why is a hash not one?",
   "Why does HMAC have its particular nested structure?",
   "Why must tag comparison be constant-time, and what is the attack's "
   "cost?",
   "Give the three composition orders and the verdict on each.",
   "Why is encrypt-then-MAC sound, in practical terms?",
   "Why should you compose nothing at all?",
   "What is associated data for, and give the record-identifier "
   "example.",
   "State the AEAD decryption contract.",
   "Name four AEAD constructions and when to use each.",
   "Why must every decryption failure look identical?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Hash Functions",
 "subtitle": "What they are for, and the three misuses.",
 "question": "What property do you actually need from a hash?",
 "outcomes": [
     "Name the three security properties and distinguish them.",
     "Choose a hash function for a stated purpose.",
     "Explain length extension and why HMAC avoids it.",
     "Name the three standard misuses.",
     "Explain Merkle trees and content addressing.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Three properties",
   "blurb": "Different strengths, different uses."},

  {"t": "table", "kicker": "Properties", "title": "The three properties, in increasing strength",
   "header": ["Property", "Infeasible to", "Security level"],
   "widths": [3.2, 4.6, 4.0],
   "rows": [
     ["<b>Preimage resistance</b>", "<b>Find m given H(m)</b>", "<b>2ⁿ for n-bit output</b>"],
     ["<b>Second preimage</b>", "<b>Find m′ ≠ m with H(m′) = H(m)</b>", "<b>2ⁿ</b>"],
     ["<b>Collision resistance</b>", "<b>Find any m, m′ colliding</b>", "<b>2ⁿᐟ² — the birthday bound</b>"],
   ],
   "footnote": "<b>Collision resistance is the weakest to break and "
               "the one that matters most</b> — SHA-256 gives 128 "
               "bits of collision resistance, not 256, which is why "
               "output length is doubled.",
   "note": "The birthday halving is the number students get wrong."},

  {"t": "callout", "title": "Collision resistance is what signatures depend on, and it is the first to fall",
   "kind": "Why the distinction is practical",
   "body": ["<b>A signature is computed over a hash, not over the "
            "message</b> (Module 07) — so <b>two messages with the "
            "same hash have the same valid signature.</b>",
            "<b>Which makes a collision directly exploitable:</b> "
            "<b>get a benign document signed, present the colliding "
            "malicious one with the same signature</b> — and both "
            "verify.",
            "<b>And this was not hypothetical.</b> <b>MD5 collisions "
            "were used to produce a fraudulent certificate authority "
            "certificate</b>, and SHA-1 collisions were later "
            "demonstrated for real document formats.",
            "<b>So the practical rule:</b> <b>MD5 and SHA-1 are "
            "broken for anything requiring collision resistance</b>, "
            "which includes every signature — <b>while remaining "
            "adequate for non-adversarial checksums.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Choosing",
   "blurb": "By purpose, not by reputation."},

  {"t": "code", "kicker": "Choice", "title": "Which hash, for what",
   "lang": "text", "code": """
  GENERAL CRYPTOGRAPHIC USE
      SHA-256 / SHA-512       the safe default
      SHA-3 / SHAKE           different internal
                              structure; no length
                              extension
      BLAKE2 / BLAKE3         faster, keyed mode built
                              in, no length extension

  PASSWORDS -- NONE OF THE ABOVE
      Argon2id, scrypt, bcrypt. A fast hash is exactly
      wrong here, and Module 09 explains why.

  NON-ADVERSARIAL CHECKSUMS
      CRC32, xxHash. Fast, not secure, and that is fine
      when nobody is attacking.

  BROKEN FOR COLLISION RESISTANCE
      MD5, SHA-1. Still fine as non-adversarial
      checksums; never in a signature.
""",
   "caption": "<b>The password row is the one that matters most</b> "
              "— using SHA-256 for passwords is a defect, not a "
              "weaker choice.",
   "note": "Separating 'broken' from 'broken for what' is the useful "
           "distinction."},

  {"t": "section", "label": "Part 3", "title": "Length extension",
   "blurb": "A structural property with a real consequence."},

  {"t": "callout", "title": "Given H(secret || m) you can compute H(secret || m || padding || m′) without the secret",
   "kind": "The Merkle–Damgård consequence",
   "body": ["<b>SHA-256 processes the message in blocks and its "
            "output <i>is</i> its internal state</b> — so knowing "
            "the hash means knowing the state and being able to continue "
            "hashing.",
            "<b>Which breaks the naive MAC.</b> <b>A system "
            "authenticating with H(key || message) can have data "
            "appended by an adversary who never learns the "
            "key</b> — and the resulting tag is valid.",
            "<b>This has produced real vulnerabilities</b> in "
            "signed-URL and signed-cookie schemes built from a bare hash "
            "rather than a MAC.",
            "<b>HMAC's nested structure exists precisely to prevent "
            "it</b> — <b>and SHA-3, BLAKE2, and BLAKE3 are not "
            "susceptible at all</b>, because their construction does not "
            "expose the full state."]},

  {"t": "eq", "kicker": "HMAC", "title": "Why the construction looks the way it does",
   "eqs": [
     ("HMAC(k, m) = H( (k ⊕ opad) || H( (k ⊕ ipad) || m ) )",
      "Two distinct padding constants make the inner and outer keys "
      "different."),
     ("inner hash  ⟹  a fixed-length digest",
      "So the outer hash's input has a fixed length that an "
      "adversary cannot extend."),
     ("outer hash re-keys  ⟹  no continuable state",
      "Length extension becomes impossible. The nesting is not "
      "arbitrary; it is exactly what buys this."),
   ],
   "caption": "<b>The nesting is not arbitrary</b> — it is exactly "
              "what removes the length-extension property.",
   "note": "Explaining the nesting makes HMAC memorable rather than "
           "mysterious."},

  {"t": "section", "label": "Part 4", "title": "Misuses and uses",
   "blurb": "The three errors, and the good constructions."},

  {"t": "bullets", "kicker": "Misuses", "title": "The three standard misuses",
   "items": [
     "<b>A hash as a MAC.</b> <b>Unkeyed, so anyone can "
     "recompute it</b> — it detects corruption and nothing "
     "adversarial (Module 04 §1).",
     "",
     "<b>A fast hash for passwords.</b> <b>Speed is the "
     "attacker's advantage</b>, and billions of guesses per second "
     "follow (Module 09).",
     "",
     "<b>A hash to hide a low-entropy value.</b> <b>Hashing an "
     "email address, a phone number, or a national identifier conceals "
     "nothing</b> — the space is small enough to enumerate "
     "completely.",
     "",
     "<b>And a fourth worth naming: truncating a hash without "
     "accounting for the birthday bound</b>, which halves again.",
     "",
     "<b>The third is the one that appears in privacy claims</b> "
     "— 'we only store hashed emails' is not "
     "de-identification.",
   ],
   "footnote": "<b>The low-entropy misuse is the most consequential "
               "outside engineering</b>, because it is routinely "
               "presented to regulators and users as anonymisation."},

  {"t": "callout", "title": "And the constructions worth knowing",
   "kind": "What hashes are genuinely good for",
   "body": ["<b>Content addressing.</b> <b>Name data by its "
            "hash</b> — and <b>the name then verifies the "
            "content</b>, which is how Git, container registries, and "
            "package lockfiles get their integrity.",
            "<b>Merkle trees.</b> <b>Hash pairs of hashes "
            "upward</b>; the root commits to everything beneath, and "
            "<b>a single branch proves membership in log n "
            "hashes</b>.",
            "<b>Which gives you efficient verification of a small "
            "part of a large structure</b> — the basis of "
            "certificate transparency logs, distributed version control, "
            "and block-chained ledgers.",
            "<b>And commitment:</b> <b>publish H(value) now, reveal "
            "the value later, and you cannot have changed it</b> "
            "— though <b>this requires the value to have enough "
            "entropy, or a random salt</b>, which is the third misuse "
            "again."]},
 ],
 "takeaways": [
   "Collision resistance is the weakest property to break — the "
   "birthday bound halves the security level, so SHA-256 gives 128 bits of "
   "it.",
   "Signatures are computed over hashes, so a collision yields two "
   "messages with one valid signature — which produced a fraudulent "
   "CA certificate from MD5.",
   "MD5 and SHA-1 are broken for collision resistance and remain adequate "
   "as non-adversarial checksums; the distinction is useful.",
   "Length extension means H(secret || m) lets an adversary append without "
   "the secret, which is why HMAC is nested and why SHA-3 and BLAKE are "
   "immune.",
   "The three misuses are a hash as a MAC, a fast hash for passwords, and "
   "a hash to hide a low-entropy value.",
   "'We only store hashed emails' is not de-identification, because the "
   "input space is enumerable.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The three properties"),
  ("table", ["Property", "What is infeasible", "Security level for an "
             "n-bit output"],
   [["<b>Preimage resistance</b>",
     "<b>Given H(m), find any m producing it.</b>",
     "<b>2<sup>n</sup></b> — the full output length."],
    ["<b>Second preimage resistance</b>",
     "<b>Given m, find a different m&prime; with the same hash.</b>",
     "<b>2<sup>n</sup></b>."],
    ["<b>Collision resistance</b>",
     "<b>Find <i>any</i> pair m, m&prime; with the same hash</b> — "
     "the adversary chooses both.",
     "<b>2<sup>n/2</sup></b> — the birthday bound, which is the "
     "number people get wrong."]],
   [0.24, 0.40, 0.36]),
  ("p", "<b>Collision resistance is the weakest of the three to break "
        "and the one that matters most in practice.</b> <b>SHA-256 "
        "provides 128 bits of collision resistance, not 256</b> — "
        "because the adversary gets to choose both messages, and the "
        "birthday paradox (CSCE 658 Module 02) halves the exponent. "
        "<b>This is exactly why output lengths are specified at double "
        "the intended security level</b>, and why a 128-bit hash offers "
        "only 64 bits against collisions, which is now reachable."),
  ("callout", "Collision resistance is what signatures depend on, and it is "
              "the first to fall",
   ["<b>A signature is computed over a hash of the message rather than "
    "over the message itself</b> (Module 07) — for both "
    "performance and structural reasons — <b>so two messages with "
    "the same hash have exactly the same valid signature.</b>",
    "<b>Which makes a collision directly exploitable:</b> <b>obtain a "
    "signature on a benign document, then present the colliding "
    "malicious document bearing that same signature</b> — and both "
    "verify correctly, because verification only ever sees the hash.",
    "<b>And this was never hypothetical.</b> <b>MD5 collisions were "
    "used to produce a fraudulent certificate authority certificate</b> "
    "that chained to a real root, and <b>SHA-1 collisions were later "
    "demonstrated for real document formats</b> where the colliding pair "
    "rendered as two different documents.",
    "<b>So the practical rule is stated by purpose:</b> <b>MD5 and "
    "SHA-1 are broken for anything requiring collision resistance</b>, "
    "which includes every signature and every commitment — <b>while "
    "remaining perfectly adequate for non-adversarial integrity "
    "checks</b> like detecting a corrupted download, where nobody is "
    "constructing the input."]),

  ("h1", "2 &nbsp; Choosing"),
  ("code", """GENERAL CRYPTOGRAPHIC USE
    SHA-256 / SHA-512       the safe default
    SHA-3 / SHAKE           different internal structure;
                            no length extension
    BLAKE2 / BLAKE3         faster, keyed mode built in,
                            no length extension

PASSWORDS -- NONE OF THE ABOVE
    Argon2id, scrypt, bcrypt. A fast hash is exactly
    wrong here, and Module 09 explains why at length.

NON-ADVERSARIAL CHECKSUMS
    CRC32, xxHash. Fast, not secure, and that is entirely
    fine when nobody is attacking the input.

BROKEN FOR COLLISION RESISTANCE
    MD5, SHA-1. Still acceptable as non-adversarial
    checksums; never in a signature or a commitment."""),
  ("p", "<b>The password row is the one that matters most.</b> <b>Using "
        "SHA-256 for password storage is a defect rather than a weaker "
        "choice</b> — the property you need there is slowness, which "
        "every hash in the first group is specifically designed not to "
        "have (Module 09 &sect;1). <b>And separating 'broken' from "
        "'broken for what' is the genuinely useful distinction</b>: it "
        "lets you assess an inherited system accurately rather than "
        "flagging every MD5 as critical."),

  ("break",),
  ("h1", "3 &nbsp; Length extension"),
  ("callout", "Given H(secret || m) you can compute H(secret || m || pad || "
              "m&prime;) without knowing the secret",
   ["<b>SHA-256 and SHA-1 process the message in fixed-size blocks, "
    "and the final output <i>is</i> the internal state</b> — the "
    "Merkle&ndash;Damg&aring;rd construction — <b>so knowing the "
    "hash means knowing the state, and knowing the state means being able "
    "to continue hashing from it.</b>",
    "<b>Which breaks the naive MAC completely.</b> <b>A system "
    "authenticating messages with H(key || message) can have arbitrary "
    "data appended by an adversary who never learns the key</b>, and "
    "<b>the resulting tag is valid</b> — the adversary needs only "
    "the original hash, the original message length, and the data to "
    "append.",
    "<b>This has produced real vulnerabilities</b>, particularly in "
    "signed-URL and signed-cookie schemes built from a bare hash rather "
    "than from a MAC — where appending <code>&amp;admin=true</code> "
    "to an authenticated query string was exactly the attack.",
    "<b>HMAC's nested structure exists precisely to prevent it</b> "
    "(see the equation) — <b>and SHA-3, BLAKE2, and BLAKE3 are not "
    "susceptible at all</b>, because their constructions do not expose "
    "the full internal state as output. <b>Which is a reason to prefer "
    "them where you have a free choice.</b>"]),
  ("eq", "HMAC(k, m) = H( (k &oplus; opad) || H( (k &oplus; ipad) "
         "|| m ) )"),
  ("ul", ["<b>ipad, opad</b> &mdash; two distinct fixed padding "
          "constants, which make the inner and outer keys different.",
          "<b>The inner hash</b> &mdash; produces a fixed-length "
          "digest, so <b>the outer hash's input has a fixed length that "
          "an adversary cannot extend.</b>",
          "<b>The outer hash</b> &mdash; re-keys over that digest, so "
          "<b>the output is not a continuable internal state for the "
          "message</b>, which is exactly what removes the extension "
          "property.",
          "<b>The result</b> &mdash; <b>length extension is "
          "impossible, and the security proof requires only modest "
          "assumptions about H</b> — notably, HMAC-MD5 remained "
          "unbroken as a MAC well after MD5's collision resistance "
          "fell, because a MAC does not depend on collision "
          "resistance. <b>The nesting is not arbitrary</b>, and "
          "explaining it is what makes HMAC memorable rather than "
          "mysterious."]),

  ("h1", "4 &nbsp; Misuses, and good uses"),
  ("ul", ["<b>A hash used as a MAC.</b> <b>It is unkeyed, so anybody "
          "including the adversary can recompute it</b> — it detects "
          "accidental corruption and nothing adversarial at all "
          "(Module 04 &sect;1).",
          "<b>A fast hash used for passwords.</b> <b>Speed is "
          "precisely the attacker's advantage</b>, and billions of "
          "guesses per second on commodity hardware follow directly "
          "(Module 09).",
          "<b>A hash used to hide a low-entropy value.</b> <b>Hashing "
          "an email address, a phone number, a date of birth, or a "
          "national identifier conceals essentially nothing</b> — the "
          "input space is small enough to enumerate exhaustively, so the "
          "hash is a reversible encoding in practice.",
          "<b>And a fourth worth naming: truncating a hash without "
          "accounting for the birthday bound</b>, which halves the "
          "collision security again — a 64-bit truncation offers 32 "
          "bits, which is trivially reachable.",
          "<b>The third misuse is the one that appears in privacy "
          "claims</b> — <b>'we only store hashed email addresses' is "
          "not de-identification</b>, and it is routinely presented to "
          "users and regulators as though it were. <b>This is the most "
          "consequential misuse outside engineering</b>, and a salted, "
          "slow construction is the minimum that changes the answer."]),
  ("callout", "And the constructions worth knowing",
   ["<b>Content addressing.</b> <b>Name the data by its hash</b> "
    "— and <b>the name then verifies the content</b>, so retrieval "
    "from an untrusted source is self-checking. This is how Git, "
    "container registries, and package lockfiles obtain their integrity "
    "(CSCE 701 Module 08 &sect;3).",
    "<b>Merkle trees.</b> <b>Hash pairs of hashes upward to a single "
    "root</b>; the root commits to every leaf beneath it, and <b>a single "
    "branch of the tree proves membership using only log n hashes</b> "
    "rather than the whole structure.",
    "<b>Which gives efficient verification of a small part of a very "
    "large structure</b> — the basis of certificate transparency "
    "logs (Module 07 &sect;4), distributed version control, "
    "block-chained ledgers, and verified file systems.",
    "<b>And commitment:</b> <b>publish H(value) now, reveal the value "
    "later, and you cannot have changed it in between</b> — binding "
    "and hiding from one primitive. <b>Though this requires the value "
    "to carry enough entropy, or to be accompanied by a random "
    "salt</b>, which is the third misuse arriving again in a different "
    "guise."]),
 ],
 "resources": [
   ("Aumasson &mdash; Serious Cryptography, chapters 6 and 7",
    "https://nostarch.com/serious-cryptography-2nd-edition",
    "<b>The whole module</b>, with the construction internals and the "
    "practical choice guidance."),
   ("Boneh & Shoup, chapters 8 and 14 (free)",
    "https://toc.cryptobook.us/",
    "<b>&sect;1's definitions and &sect;3's HMAC proof</b> — "
    "including why a MAC does not require collision resistance."),
   ("The SHAttered SHA-1 collision (free)",
    "https://shattered.io/",
    "<b>&sect;1's demonstration</b>, with the colliding PDF pair and the "
    "cost analysis."),
   ("Certificate Transparency (free)",
    "https://certificate.transparency.dev/",
    "<b>&sect;4's Merkle trees in production</b> — and the "
    "infrastructure Module 07 &sect;4 depends on."),
 ],
 "exercises": [
   "<b>State which of the three properties</b> each of five hash uses in "
   "your own code actually requires.",
   "<b>Compute the collision security</b> of a 256-bit hash truncated to "
   "128 bits, and to 64.",
   "<b>Explain why a signature forgery follows from a "
   "collision</b>, step by step.",
   "<b>Find an MD5 use you can safely leave alone</b> and justify "
   "it.",
   "<b>Demonstrate length extension</b> against H(secret || message) "
   "using a library that exposes the state.",
   "<b>Show that HMAC resists the same attempt.</b>",
   "<b>Explain the nesting</b> in your own words.",
   "<b>Enumerate a hashed low-entropy space</b> — hash 10,000 "
   "plausible phone numbers and match them.",
   "<b>Build a Merkle tree</b> over 1000 items and produce a membership "
   "proof.",
   "<b>Verify the proof without the other 999 items.</b>",
 ],
 "selfcheck": [
   "Name the three properties and the security level of each.",
   "Why is collision resistance only n/2 bits?",
   "Why does a collision break a signature scheme?",
   "What does 'broken' mean for MD5, and what remains acceptable?",
   "Which hash for general use, for passwords, and for checksums?",
   "State the length extension property and why it holds.",
   "What real vulnerability class did it produce?",
   "Explain HMAC's nesting and what it achieves.",
   "Name the three misuses, and the fourth.",
   "Explain content addressing, Merkle trees, and commitment.",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Key Exchange and Public Keys",
 "subtitle": "Establishing a shared secret with a stranger.",
 "question": "How do two parties who have never met agree on a key?",
 "outcomes": [
     "Explain Diffie–Hellman and what it does and does not "
     "provide.",
     "Explain the hardness assumptions and their relationship.",
     "Explain why public-key encryption is rarely used directly.",
     "Explain forward secrecy and why ephemeral keys matter.",
     "Choose between the curve and finite-field settings.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Diffie–Hellman",
   "blurb": "The idea that made the internet possible."},

  {"t": "eq", "kicker": "Key exchange", "title": "The exchange, in four lines",
   "eqs": [
     ("A → B: gᵃ          B → A: gᵇ",
      "Each party sends a public value. The private exponents a and "
      "b are never transmitted."),
     ("A computes (gᵇ)ᵃ,   B computes (gᵃ)ᵇ,   both get gᵃᵇ",
      "The same value from different inputs, which is the whole "
      "trick."),
     ("adversary sees g, gᵃ, gᵇ  and must find gᵃᵇ",
      "The computational Diffie–Hellman problem, believed hard "
      "and not proved so (Part 2)."),
   ],
   "caption": "<b>Both parties compute the same value and the "
              "eavesdropper cannot</b> — from public messages "
              "only.",
   "note": "Write this out by hand once; it is the most elegant result "
           "in the subject."},

  {"t": "callout", "title": "Diffie–Hellman gives you a shared secret with <i>somebody</i>",
   "kind": "The limitation that defines everything after it",
   "body": ["<b>Unauthenticated, it is wholly vulnerable to an active "
            "adversary.</b> <b>A machine in the middle runs the "
            "exchange separately with each party and relays "
            "everything</b> — two perfectly secure channels, both "
            "to the adversary.",
            "<b>And neither party can detect it from the exchange "
            "itself</b>, because every message is well-formed and the "
            "mathematics is correct.",
            "<b>So key exchange must be authenticated</b> — with "
            "a signature over the exchange "
            "(Module 07), a pre-shared key, or a "
            "password-authenticated variant.",
            "<b>Which is why Module 07 and the certificate problem "
            "exist</b>: <b>the hard part was never agreeing on a key, "
            "it was knowing who you agreed with.</b>"]},

  {"t": "section", "label": "Part 2", "title": "The assumptions",
   "blurb": "What the security actually rests on."},

  {"t": "table", "kicker": "Hardness", "title": "The assumptions, and what breaks if each falls",
   "header": ["Problem", "Statement", "Depends on it"],
   "widths": [2.7, 4.3, 4.6],
   "rows": [
     ["<b>Discrete log</b>", "<b>Given g, gᵃ, find a</b>", "<b>DH, DSA, ECDSA, Ed25519</b>"],
     ["<b>Computational DH</b>", "<b>Given gᵃ, gᵇ, find gᵃᵇ</b>", "<b>DH key exchange — weaker than DL</b>"],
     ["<b>Factoring</b>", "<b>Given n = pq, find p</b>", "<b>RSA</b>"],
     ["<b>Short vectors in lattices</b>", "<b>Find a short vector in a lattice</b>", "<b>The post-quantum schemes (M12)</b>"],
   ],
   "footnote": "<b>None of these is proved hard</b> — they are "
               "believed hard after long attention, and a proof would "
               "resolve questions CSCE 637 Module 13 explains are "
               "open.",
   "note": "The unproved-assumption point connects directly to the "
           "complexity course."},

  {"t": "callout", "title": "The security rests on unproved assumptions, and that is the honest position",
   "kind": "What this means practically",
   "body": ["<b>No one has proved that factoring or discrete log is "
            "hard.</b> <b>P ≠ NP would not even settle "
            "it</b>, since neither problem is known to be NP-hard "
            "(CSCE 637 §09).",
            "<b>What we have is decades of concentrated attention "
            "without a polynomial algorithm</b> — which is "
            "substantial evidence and is not proof.",
            "<b>And the assumptions are not independent of the "
            "computational model.</b> <b>A quantum computer breaks both "
            "factoring and discrete log in polynomial time</b> by "
            "Shor's algorithm, which is Module 12's subject.",
            "<b>So the honest claim is conditional:</b> <b>'secure "
            "assuming discrete log is hard in this group against a "
            "classical adversary'</b> — and Module 13 is about "
            "stating that rather than dropping the condition."]},

  {"t": "section", "label": "Part 3", "title": "Public-key encryption",
   "blurb": "And why you almost never use it directly."},

  {"t": "bullets", "kicker": "Hybrid", "title": "Why everything real is hybrid",
   "items": [
     "<b>Public-key operations are orders of magnitude slower</b> "
     "than symmetric ones, and the gap is large enough to matter at any "
     "scale.",
     "",
     "<b>And they encrypt only small messages</b> — RSA can "
     "encrypt less than its modulus size, so a long message does not "
     "fit at all.",
     "",
     "<b>So the universal pattern is hybrid:</b> <b>use public-key "
     "cryptography to establish or transport a symmetric key, then "
     "encrypt the data symmetrically</b> with AEAD "
     "(Module 04).",
     "",
     "<b>Which is what TLS does</b> (Module 08), <b>what encrypted "
     "email does, and what envelope encryption "
     "does</b> (Module 10 §2).",
     "",
     "<b>And raw RSA encryption is a hazard in itself</b> — "
     "<b>textbook RSA is deterministic and malleable</b>, so padding "
     "(OAEP) is mandatory and getting it wrong has produced real "
     "attacks.",
   ],
   "footnote": "<b>If you are calling an RSA encrypt function "
               "directly, stop</b> — the correct operation is a key "
               "encapsulation or a sealed-box API."},

  {"t": "section", "label": "Part 4", "title": "Forward secrecy",
   "blurb": "The property worth understanding properly."},

  {"t": "callout", "title": "Forward secrecy means a key compromised tomorrow does not decrypt today",
   "kind": "And it requires ephemeral keys",
   "body": ["<b>If a session key is derived from a long-term private "
            "key, then compromising that key later decrypts every "
            "recorded past session</b> — which is a realistic "
            "adversary model, since traffic is cheap to store.",
            "<b>So use an ephemeral exchange:</b> <b>generate a fresh "
            "Diffie–Hellman pair per session, authenticate it "
            "with the long-term key, and discard it afterwards.</b>",
            "<b>The long-term key then only ever signs, never "
            "decrypts</b> — so its later compromise permits "
            "impersonation going forward and reveals nothing "
            "retrospectively.",
            "<b>Which is why TLS 1.3 removed non-ephemeral key "
            "exchange entirely</b> (Module 08) — <b>a standard "
            "deleting an option rather than deprecating it, which is "
            "this course's thesis in action.</b>"]},

  {"t": "bullets", "kicker": "Choosing", "title": "Curves, fields, and what to use",
   "items": [
     "<b>Use X25519 for key exchange.</b> <b>Fast, 32-byte keys, "
     "no parameter choices, and no invalid-curve "
     "hazard</b> — every 32-byte string is a valid input.",
     "",
     "<b>Elliptic curves give equivalent security at much smaller "
     "sizes</b> — a 256-bit curve against a 3072-bit finite "
     "field, which is why they displaced the alternative.",
     "",
     "<b>Avoid implementing curve arithmetic</b>: <b>point "
     "validation, the identity element, and non-constant-time scalar "
     "multiplication have each produced real breaks.</b>",
     "",
     "<b>And avoid custom curves and custom groups</b> — "
     "parameter selection is where the subtle weaknesses "
     "hide.",
     "",
     "<b>Which is Module 01 §4 once more</b>, in the "
     "place where it has the strongest historical support.",
   ],
   "footnote": "<b>X25519 was designed so that misuse is "
               "difficult</b> — no invalid points, no cofactor "
               "subtleties exposed, no parameter choices. That design "
               "goal is why it is the recommendation."},
 ],
 "takeaways": [
   "Diffie–Hellman lets two parties compute a shared secret from "
   "public messages, which an eavesdropper cannot.",
   "Unauthenticated, it gives you a secure channel with somebody — "
   "possibly a machine in the middle, undetectably.",
   "The hardness assumptions are unproved and would not be settled by "
   "P ≠ NP, since neither factoring nor discrete log is known "
   "NP-hard.",
   "Everything real is hybrid: public-key cryptography establishes a "
   "symmetric key, and AEAD encrypts the data.",
   "Forward secrecy requires ephemeral keys, so that a long-term key's "
   "later compromise does not decrypt recorded traffic.",
   "Use X25519, which was designed so that misuse is difficult — no "
   "invalid points and no parameter choices.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Diffie&ndash;Hellman"),
  ("eq", "A &rarr; B: g<sup>a</sup> &nbsp;&nbsp;&nbsp; B &rarr; A: "
         "g<sup>b</sup> &nbsp;&nbsp;&nbsp; shared secret: g<sup>ab</sup>"),
  ("ul", ["<b>g</b> &mdash; a public generator of a group in which "
          "the discrete logarithm problem is believed hard. Public, "
          "fixed, and shared by everyone.",
          "<b>a, b</b> &mdash; each party's private value, generated "
          "fresh from a CSPRNG (Module 02) and <b>never "
          "transmitted.</b>",
          "<b>g<sup>ab</sup></b> &mdash; computed as "
          "(g<sup>b</sup>)<sup>a</sup> by A and as "
          "(g<sup>a</sup>)<sup>b</sup> by B. <b>The same value, from "
          "different inputs, which is the whole trick.</b>",
          "<b>The adversary</b> &mdash; sees g, g<sup>a</sup>, and "
          "g<sup>b</sup>, and must compute g<sup>ab</sup>, which is the "
          "computational Diffie&ndash;Hellman problem and is believed "
          "hard (&sect;2). <b>Write this out by hand once with small "
          "numbers</b> — it is the most elegant result in the "
          "subject and it takes five minutes."]),
  ("callout", "Diffie&ndash;Hellman gives you a shared secret with "
              "<i>somebody</i>",
   ["<b>Unauthenticated, it is wholly vulnerable to an active "
    "adversary.</b> <b>A machine in the middle runs the exchange "
    "separately with each party and relays the traffic between "
    "them</b> — producing two perfectly secure channels, both "
    "terminating at the adversary, who reads and may modify everything.",
    "<b>And neither party can detect this from the exchange "
    "itself</b>, because every message is correctly formed, the "
    "mathematics is valid, and both ends successfully derive a key that "
    "their peer also holds. <b>The cryptography worked exactly as "
    "specified.</b>",
    "<b>So key exchange must be authenticated</b> — by a signature "
    "over the exchange transcript (Module 07), by a pre-shared key, or "
    "by a password-authenticated key exchange where a low-entropy shared "
    "secret suffices without being brute-forceable.",
    "<b>Which is why Module 07 and the whole certificate problem "
    "exist:</b> <b>the hard part was never agreeing on a key — it "
    "was knowing who you agreed with</b>, and that turns out not to be a "
    "cryptographic problem at all (Module 01 &sect;2's third "
    "limitation)."]),

  ("h1", "2 &nbsp; The assumptions"),
  ("table", ["Problem", "The statement", "What depends on it"],
   [["<b>Discrete logarithm</b>",
     "<b>Given g and g<sup>a</sup>, find a.</b>",
     "<b>Diffie&ndash;Hellman, DSA, ECDSA, Ed25519.</b>"],
    ["<b>Computational Diffie&ndash;Hellman</b>",
     "<b>Given g<sup>a</sup> and g<sup>b</sup>, compute "
     "g<sup>ab</sup>.</b>",
     "<b>DH key exchange.</b> <b>A potentially weaker assumption than "
     "discrete log</b> — breaking DL breaks this, but not "
     "necessarily the reverse."],
    ["<b>Integer factoring</b>",
     "<b>Given n = pq for large primes, find p.</b>",
     "<b>RSA</b>, for both signing and encryption."],
    ["<b>Short vectors in lattices</b>",
     "<b>Find a short non-zero vector in a given lattice.</b>",
     "<b>The post-quantum schemes</b> (Module 12), which is why they "
     "rest on a different assumption rather than a better algorithm."]],
   [0.22, 0.36, 0.42]),
  ("callout", "The security rests on unproved assumptions, and that is the "
              "honest position",
   ["<b>Nobody has proved that factoring or discrete log is hard.</b> "
    "<b>Even P &ne; NP would not settle the question</b>, since neither "
    "problem is known to be NP-hard — both sit in the suspected gap "
    "between P and NP-complete (CSCE 637 Module 09), which is one "
    "reason that gap is interesting.",
    "<b>What we actually have is several decades of concentrated "
    "attention by capable people without a polynomial-time "
    "algorithm</b> — which is substantial evidence and is "
    "categorically not proof, and the distinction is worth keeping clear "
    "because the whole edifice rests on it.",
    "<b>And the assumptions are not independent of the computational "
    "model.</b> <b>A sufficiently large quantum computer breaks both "
    "factoring and discrete log in polynomial time</b> by Shor's "
    "algorithm — so the assumption was always 'hard for a classical "
    "adversary', which Module 12 addresses.",
    "<b>So the honest claim is conditional:</b> <b>'secure assuming "
    "the discrete logarithm problem is hard in this group against a "
    "classical adversary'</b> — and <b>Module 13 is about stating "
    "that condition rather than quietly dropping it</b>, which is the "
    "program's closing rule in this course's vocabulary."]),

  ("break",),
  ("h1", "3 &nbsp; Public-key encryption, and hybrid construction"),
  ("ul", ["<b>Public-key operations are orders of magnitude slower</b> "
          "than symmetric ones — a factor of hundreds to thousands "
          "— and the gap is large enough to dominate at any "
          "meaningful scale.",
          "<b>And they encrypt only small messages.</b> <b>RSA can "
          "encrypt a plaintext smaller than its modulus, less padding</b>, "
          "so a document does not fit at all and must be split or, "
          "correctly, handled differently.",
          "<b>So the universal pattern is hybrid:</b> <b>use "
          "public-key cryptography to establish or transport a symmetric "
          "key, then encrypt the actual data symmetrically</b> with an "
          "AEAD construction (Module 04).",
          "<b>Which is what TLS does</b> (Module 08), <b>what "
          "encrypted email and messaging do, and what envelope encryption "
          "does</b> (Module 10 &sect;2) — the pattern is so "
          "universal that the libraries expose it directly as a sealed-box "
          "or key-encapsulation operation.",
          "<b>And raw RSA encryption is a hazard in its own right.</b> "
          "<b>Textbook RSA is deterministic — so identical "
          "plaintexts give identical ciphertexts — and malleable, so "
          "an adversary can transform ciphertexts predictably.</b> "
          "<b>Padding (OAEP) is mandatory, and getting the padding "
          "validation wrong produced Bleichenbacher's attack and its "
          "many descendants.</b> <b>If you are calling an RSA encrypt "
          "function directly, stop</b> — the correct operation is a "
          "key encapsulation or a sealed box."]),

  ("h1", "4 &nbsp; Forward secrecy"),
  ("callout", "Forward secrecy means a key compromised tomorrow does not "
              "decrypt today's traffic",
   ["<b>If a session key is derived from a long-term private key, then "
    "compromising that key at any future point decrypts every past "
    "session that was recorded</b> — and <b>that is a realistic "
    "adversary model, because storing traffic is cheap and an adversary "
    "may obtain the key years later</b> by compromise, by legal process, "
    "or by the key outliving its protection.",
    "<b>So use an ephemeral exchange:</b> <b>generate a fresh "
    "Diffie&ndash;Hellman keypair for every session, authenticate it "
    "using the long-term key, derive the session key from the ephemeral "
    "exchange, and then discard the ephemeral private value.</b>",
    "<b>The long-term key then only ever signs and never "
    "decrypts</b> — so its later compromise permits impersonation "
    "going forward, which is serious, and reveals nothing about past "
    "sessions at all, which is the property being bought.",
    "<b>Which is why TLS 1.3 removed non-ephemeral key exchange "
    "entirely</b> (Module 08) rather than merely deprecating "
    "it — <b>a standards body deleting an option so that it cannot "
    "be selected</b>, which is this course's thesis appearing in "
    "standards form and is worth noticing as a design pattern."]),
  ("ul", ["<b>Use X25519 for key exchange.</b> <b>Fast, 32-byte keys, "
          "no parameter choices to make, and no invalid-curve "
          "hazard</b> — <b>every 32-byte string is a valid "
          "input</b>, which eliminates a whole validation step and the "
          "bugs in it.",
          "<b>Elliptic curves provide equivalent security at much "
          "smaller key sizes</b> — a 256-bit curve against roughly a "
          "3072-bit finite field — which is why they displaced the "
          "finite-field setting for new deployments.",
          "<b>Avoid implementing curve arithmetic yourself.</b> "
          "<b>Point validation, handling of the identity element, "
          "cofactor subtleties, and non-constant-time scalar "
          "multiplication have each produced real, exploited "
          "breaks</b> — this is among the least forgiving code in "
          "the field.",
          "<b>And avoid custom curves and custom groups</b> — "
          "<b>parameter selection is exactly where the subtle weaknesses "
          "hide</b>, and a group with a small subgroup or a special "
          "structure can be catastrophically weak while looking entirely "
          "ordinary.",
          "<b>Which is Module 01 &sect;4 once more</b>, arriving in "
          "the place where it has the strongest historical "
          "support. <b>X25519 was specifically designed so that misuse "
          "is difficult</b> — no invalid points, no exposed cofactor "
          "subtleties, no parameters — and <b>that design goal is "
          "the reason it is the recommendation</b>, rather than its "
          "performance."]),
 ],
 "resources": [
   ("Boneh & Shoup, chapters 10 through 12 (free)",
    "https://toc.cryptobook.us/",
    "<b>&sect;1 through &sect;3 rigorously</b> — the assumptions, "
    "their relationships, and what the reductions establish."),
   ("Aumasson &mdash; Serious Cryptography, chapters 10 through 12",
    "https://nostarch.com/serious-cryptography-2nd-edition",
    "<b>RSA, Diffie&ndash;Hellman, and elliptic curves at engineering "
    "level</b>, with the practical hazards foregrounded."),
   ("Bernstein &mdash; Curve25519, and the SafeCurves criteria (free)",
    "https://safecurves.cr.yp.to/",
    "<b>&sect;4's design argument</b> — what makes a curve hard to "
    "misuse, stated as explicit criteria."),
   ("Diffie & Hellman &mdash; New Directions in Cryptography (free)",
    "https://ee.stanford.edu/~hellman/publications/24.pdf",
    "<b>&sect;1 in the original, from 1976</b> — short, readable, "
    "and one of the genuinely pivotal papers in computing."),
 ],
 "exercises": [
   "<b>Perform a Diffie–Hellman exchange by hand</b> with small "
   "numbers, both sides.",
   "<b>Verify both parties compute the same value</b> and that you "
   "cannot get it from the public values alone.",
   "<b>Write out the machine-in-the-middle attack</b> on an "
   "unauthenticated exchange.",
   "<b>Explain why neither party can detect it</b> from the exchange.",
   "<b>State the four hardness assumptions</b> and what depends on "
   "each.",
   "<b>Explain why P ≠ NP would not settle the security of "
   "RSA.</b>",
   "<b>Measure RSA versus AES throughput</b> on the same machine.",
   "<b>Implement the hybrid pattern</b> with a sealed-box API.",
   "<b>Determine whether a TLS connection you use has forward "
   "secrecy</b>, and how you can tell.",
   "<b>Write the conditional security claim</b> for your own system's "
   "key exchange, with the assumption named.",
 ],
 "selfcheck": [
   "Give the Diffie–Hellman exchange and say what each party "
   "computes.",
   "What does unauthenticated DH actually give you?",
   "Why can the machine-in-the-middle not be detected from the "
   "exchange?",
   "Name four hardness assumptions and what rests on each.",
   "Why is CDH possibly weaker than discrete log?",
   "Why would P ≠ NP not settle these questions?",
   "Why is everything real hybrid, and give two reasons.",
   "Why is raw RSA encryption a hazard?",
   "Define forward secrecy and say what it requires.",
   "Why use X25519, and what was its design goal?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Signatures and Certificates",
 "subtitle": "Authenticity at scale, and the trust problem.",
 "question": "A signature proves a key signed it. Now what?",
 "outcomes": [
     "Explain signatures and how they differ from MACs.",
     "Name the schemes and choose between them.",
     "Explain what a certificate is and what it asserts.",
     "Explain the CA trust model and its weaknesses.",
     "Explain revocation and why it does not really work.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Signatures",
   "blurb": "And the property a MAC cannot give."},

  {"t": "table", "kicker": "Comparison", "title": "MAC versus signature",
   "header": ["", "MAC", "Signature"],
   "widths": [2.9, 4.1, 4.5],
   "rows": [
     ["<b>Keys</b>", "<b>One shared secret</b>", "<b>Private signs, public verifies</b>"],
     ["<b>Who can verify</b>", "<b>Only a keyholder</b>", "<b>Anyone</b>"],
     ["<b>Who can forge</b>", "<b>Any keyholder</b>", "<b>Only the private keyholder</b>"],
     ["<b>Non-repudiation</b>", "<b>No — either party could have made it</b>", "<b>Yes, cryptographically</b>"],
     ["<b>Speed</b>", "<b>Very fast</b>", "<b>Orders of magnitude slower</b>"],
   ],
   "footnote": "<b>Non-repudiation is the property only a signature "
               "provides</b> — and if you do not need public "
               "verification or non-repudiation, <b>use a MAC</b>, which "
               "is faster and simpler.",
   "note": "The default-to-MAC advice is the practical takeaway."},

  {"t": "bullets", "kicker": "Schemes", "title": "The schemes, and which to use",
   "items": [
     "<b>Ed25519.</b> <b>The default</b> — fast, small, "
     "deterministic (so no nonce to leak), and designed to be hard to "
     "misimplement.",
     "",
     "<b>ECDSA.</b> <b>Widely required by existing standards and "
     "genuinely hazardous</b>: <b>a repeated or biased nonce reveals "
     "the private key outright</b>, which has happened in production "
     "more than once.",
     "",
     "<b>RSA-PSS.</b> <b>Fine, with large keys</b> — 3072 "
     "bits for 128-bit security. Prefer it over the older PKCS#1 v1.5 "
     "padding.",
     "",
     "<b>And the post-quantum signature schemes</b> "
     "(Module 12), which are standardised and have much larger "
     "signatures.",
     "",
     "<b>Ed25519's determinism is the feature:</b> <b>no per-signature "
     "randomness means no randomness failure</b> "
     "(Module 02 §3).",
   ],
   "footnote": "<b>ECDSA's nonce requirement is the sharpest edge in "
               "deployed cryptography</b> — and it is why "
               "deterministic nonce generation (RFC 6979) and Ed25519 "
               "both exist."},

  {"t": "section", "label": "Part 2", "title": "Certificates",
   "blurb": "A signed statement binding a name to a key."},

  {"t": "callout", "title": "A certificate is a signature over the claim “this key belongs to this name”",
   "kind": "What it is, exactly",
   "body": ["<b>It contains a public key, a name, a validity period, "
            "and constraints — and a signature over all of it by "
            "an issuer.</b>",
            "<b>So verifying a certificate establishes that the issuer "
            "asserted the binding</b> — and <b>nothing about "
            "whether the assertion is true</b>, which is a different kind "
            "of question entirely.",
            "<b>And the chain terminates in a root you trust because "
            "it shipped with your operating system or browser</b> "
            "— which is the actual root of trust, and it is a "
            "business and governance arrangement rather than a "
            "cryptographic one.",
            "<b>Which is Module 01 §2's third "
            "limitation made concrete:</b> <b>cryptography moved the "
            "trust problem rather than solving it</b>, and the certificate "
            "system is where it now lives."]},

  {"t": "code", "kicker": "Validation", "title": "What validating a chain actually requires",
   "lang": "text", "code": """
  FOR EACH CERTIFICATE IN THE CHAIN:
      signature verifies under the issuer's public key
      the current time is within the validity period
      the issuer is permitted to issue (basic constraints
          CA:TRUE, and path length respected)
      key usage permits this purpose
      the algorithm is one you accept

  AND FOR THE LEAF, ADDITIONALLY:
      the name matches what you asked for -- the hostname
          you intended, not the one the certificate
          offers
      the chain terminates at a trusted root

  AND REVOCATION, if you can check it at all (Part 4).

  HISTORICAL FAILURES: missing the CA:TRUE check let any
  leaf certificate sign others. Skipping the name check
  accepted any valid certificate for any site. Both
  shipped widely.
""",
   "caption": "<b>The name check is the one most often omitted</b>, and "
              "omitting it accepts a valid certificate for an entirely "
              "different host.",
   "note": "Both historical failures are worth stating; they explain "
           "why libraries validate by default now."},

  {"t": "section", "label": "Part 3", "title": "The trust model",
   "blurb": "And its structural weakness."},

  {"t": "callout", "title": "Any CA can issue for any name, so the system is as strong as its weakest CA",
   "kind": "The structural problem",
   "body": ["<b>Your browser trusts on the order of a hundred root "
            "authorities, each able to delegate</b> — and <b>any "
            "one of them can issue a valid certificate for any domain in "
            "the world.</b>",
            "<b>So the security of every site is bounded by the least "
            "careful authority</b>, not by its own practices — "
            "which is an unusual and uncomfortable property for a "
            "security system.",
            "<b>And this has been exploited.</b> <b>Authorities have "
            "been compromised and have issued fraudulent certificates for "
            "major services</b>, which were used in real "
            "interception.",
            "<b>The mitigations are detection rather than "
            "prevention:</b> <b>Certificate Transparency logs every "
            "issued certificate publicly</b> "
            "(Module 05 §4), <b>so a fraudulent one can "
            "be noticed — after the fact.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Revocation",
   "blurb": "The part that does not work."},

  {"t": "bullets", "kicker": "Revocation", "title": "Why revocation is largely ineffective",
   "items": [
     "<b>Revocation lists grew too large to distribute</b> "
     "usefully, and were cached long enough to be stale when it "
     "mattered.",
     "",
     "<b>Online status checking introduced a privacy leak and an "
     "availability dependency</b> — the responder learns every "
     "site you visit, and an outage would break the web.",
     "",
     "<b>So clients fail <i>open</i>:</b> <b>if the status check "
     "fails, the connection proceeds</b> — which means an "
     "adversary who can block the check has defeated "
     "revocation.",
     "",
     "<b>Stapling helps by having the server supply its own signed "
     "status</b>, and depends on the server doing so.",
     "",
     "<b>And the actual answer was shorter lifetimes:</b> <b>a "
     "certificate valid for weeks needs less revocation than one valid "
     "for years</b>, which is why automated issuance mattered.",
   ],
   "footnote": "<b>Short lifetimes plus automation replaced revocation "
               "rather than fixing it</b> — an engineering answer to "
               "a problem that resisted a protocol answer."},

  {"t": "callout", "title": "What to take from this module",
   "kind": "Closing",
   "body": ["<b>Use Ed25519 unless a standard forces otherwise</b>, "
            "and <b>use a MAC when you do not need public verification "
            "— which is more often than people assume.</b>",
            "<b>Never implement certificate validation.</b> <b>Use "
            "your platform's validator and do not disable any check</b> "
            "— every historical failure in Part 2 was a "
            "skipped check, and 'verify=False' in a client library is a "
            "security decision.",
            "<b>Understand that the trust root is social rather than "
            "mathematical</b> — <b>which is why pinning, "
            "transparency logs, and short lifetimes exist</b>, and why "
            "none of them is cryptography.",
            "<b>And state the dependency when you make a "
            "claim:</b> <b>'authentic, assuming no trusted authority "
            "misissues'</b> is the honest form, which Module 13 "
            "develops."]},
 ],
 "takeaways": [
   "Only a signature provides non-repudiation and public verification; if "
   "you need neither, use a MAC, which is far faster.",
   "Ed25519 is deterministic, so there is no per-signature nonce to leak "
   "— while ECDSA reveals its private key from a repeated or biased "
   "nonce.",
   "A certificate proves an issuer asserted a name-to-key binding, not "
   "that the binding is true.",
   "The chain's root is trusted because it shipped with your OS, which "
   "makes the trust root a governance arrangement rather than a "
   "cryptographic one.",
   "Any CA can issue for any name, so every site's security is bounded by "
   "the least careful authority.",
   "Revocation largely does not work because clients fail open; short "
   "lifetimes plus automation replaced it rather than fixing it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Signatures"),
  ("table", ["", "MAC", "Signature"],
   [["<b>Keys</b>", "<b>One shared secret, held by both parties.</b>",
     "<b>A private key signs; the corresponding public key "
     "verifies.</b>"],
    ["<b>Who can verify</b>", "<b>Only someone holding the key.</b>",
     "<b>Anyone at all, including parties with no prior "
     "relationship.</b>"],
    ["<b>Who can forge</b>", "<b>Any keyholder</b> — which includes "
     "the verifier.",
     "<b>Only the holder of the private key.</b>"],
    ["<b>Non-repudiation</b>",
     "<b>No.</b> Either party could have produced the tag, so neither "
     "can prove the other did.",
     "<b>Yes, cryptographically</b> — the signer cannot credibly "
     "deny having signed."],
    ["<b>Speed</b>", "<b>Very fast</b> — a hash-rate operation.",
     "<b>Orders of magnitude slower</b>, which matters at volume."]],
   [0.21, 0.36, 0.43]),
  ("p", "<b>Non-repudiation is the property that only a signature "
        "provides</b>, and it follows directly from the asymmetry: since "
        "the verifier cannot produce the signature, its existence proves "
        "the signer did. <b>And the practical consequence is the useful "
        "one: if you do not need public verification or non-repudiation, "
        "use a MAC</b> — it is faster, simpler, has no key "
        "distribution problem beyond the shared secret, and is harder to "
        "misuse. <b>Signatures are reached for far more often than they "
        "are needed.</b>"),
  ("ul", ["<b>Ed25519.</b> <b>The default choice</b> — fast, "
          "64-byte signatures, 32-byte keys, <b>deterministic (so there "
          "is no per-signature nonce to leak)</b>, and specifically "
          "designed to be difficult to misimplement.",
          "<b>ECDSA.</b> <b>Widely required by existing standards and "
          "genuinely hazardous:</b> <b>a repeated nonce, or even a "
          "slightly biased one, reveals the private key "
          "outright</b> — recoverable from two signatures. <b>This "
          "has happened in production repeatedly</b>, including in a "
          "games console's code signing and in cryptocurrency wallets.",
          "<b>RSA-PSS.</b> <b>Entirely fine, with adequate key "
          "sizes</b> — 3072 bits for roughly 128-bit security. "
          "<b>Prefer PSS over the older PKCS#1 v1.5 padding</b>, whose "
          "signature verification has produced forgery bugs in multiple "
          "implementations.",
          "<b>And the post-quantum signature schemes</b> "
          "(Module 12) — now standardised, with substantially "
          "larger signatures and keys, which is the cost being "
          "weighed.",
          "<b>Ed25519's determinism is the feature rather than an "
          "incidental property:</b> <b>no per-signature randomness means "
          "no randomness failure</b> (Module 02 &sect;3), which "
          "removes the entire class of failure that makes ECDSA "
          "dangerous. <b>ECDSA's nonce requirement is the sharpest edge "
          "in deployed cryptography</b>, and it is why both deterministic "
          "nonce generation (RFC 6979) and Ed25519 exist."]),

  ("h1", "2 &nbsp; Certificates"),
  ("callout", "A certificate is a signature over the claim “this key "
              "belongs to this name”",
   ["<b>It contains a public key, a subject name, a validity period, "
    "and a set of constraints — and a signature over all of that by "
    "an issuer.</b> That is the whole structure.",
    "<b>So verifying a certificate establishes that the issuer asserted "
    "the binding</b> — and <b>establishes nothing whatsoever about "
    "whether the assertion is true</b>, which is a question about the "
    "issuer's verification procedures, its incentives, and its "
    "competence.",
    "<b>And the chain terminates in a root certificate you trust "
    "because it shipped with your operating system or your "
    "browser</b> — <b>which is the actual root of trust</b>, and it "
    "is a business, legal, and governance arrangement rather than a "
    "cryptographic one.",
    "<b>Which is Module 01 &sect;2's third limitation made entirely "
    "concrete:</b> <b>cryptography moved the trust problem rather than "
    "solving it</b>, and the certificate authority system is where it now "
    "lives — which is why &sect;3's weaknesses are structural rather "
    "than fixable with better algorithms."]),
  ("code", """FOR EACH CERTIFICATE IN THE CHAIN:
    signature verifies under the issuer's public key
    the current time is within the validity period
    the issuer is permitted to issue (basic constraints
        CA:TRUE, and the path length respected)
    key usage permits this purpose
    the signature algorithm is one you still accept

AND FOR THE LEAF, ADDITIONALLY:
    the name matches what you asked for -- the hostname
        you INTENDED to reach, not the one the
        certificate happens to offer
    the chain terminates at a trusted root

AND REVOCATION, if you can check it at all (section 4).

HISTORICAL FAILURES: missing the CA:TRUE check let any
leaf certificate sign others. Skipping the name check
accepted any valid certificate for any site. Both
shipped widely, in major software."""),
  ("p", "<b>The name check is the one most often omitted</b>, and "
        "<b>omitting it accepts a perfectly valid certificate issued for "
        "an entirely different host</b> — so an adversary needs only "
        "a legitimate certificate for a domain they control. <b>Both "
        "historical failures are worth stating explicitly</b>, because "
        "they explain why every modern library validates by default and "
        "why disabling validation requires an explicit, conspicuous "
        "flag — and why that flag appearing in production code is a "
        "finding."),

  ("break",),
  ("h1", "3 &nbsp; The trust model"),
  ("callout", "Any CA can issue for any name, so the system is as strong as "
              "its weakest CA",
   ["<b>Your browser trusts on the order of a hundred root "
    "authorities, each able to delegate to intermediates</b> — and "
    "<b>any one of them can issue a technically valid certificate for "
    "any domain name in the world.</b> There is no partitioning by "
    "name.",
    "<b>So the security of every site is bounded by the least careful "
    "authority in the store</b>, rather than by that site's own "
    "practices — which is an unusual and genuinely uncomfortable "
    "property, and one that no amount of care by a site operator can "
    "improve.",
    "<b>And this has been exploited rather than merely "
    "theorised.</b> <b>Certificate authorities have been compromised "
    "and have issued fraudulent certificates for major services</b>, "
    "which were then used in real interception of real users' traffic at "
    "national scale.",
    "<b>The mitigations are detection rather than prevention:</b> "
    "<b>Certificate Transparency requires every issued certificate to be "
    "logged publicly in append-only Merkle logs</b> (Module 05 "
    "&sect;4), <b>so a fraudulent issuance can be noticed by the domain "
    "owner — after the fact.</b> <b>Which is CSCE 701 "
    "Module 09's argument arriving in a protocol:</b> when prevention "
    "is structurally unavailable, build detection."]),

  ("h1", "4 &nbsp; Revocation"),
  ("ul", ["<b>Revocation lists grew too large to distribute "
          "usefully</b>, and were cached for long enough that they were "
          "frequently stale at exactly the moment they mattered.",
          "<b>Online status checking introduced a privacy leak and an "
          "availability dependency</b> — <b>the responder learns "
          "every site every user visits</b>, and <b>a responder outage "
          "would break the web</b> if clients depended on it.",
          "<b>So clients fail <i>open</i>:</b> <b>if the status check "
          "cannot be completed, the connection proceeds anyway</b> — "
          "which means <b>an adversary who can block the status check "
          "has thereby defeated revocation entirely</b>, and an adversary "
          "positioned to use a stolen certificate is by definition "
          "positioned to block a check.",
          "<b>Stapling improves matters by having the server present "
          "its own recent signed status</b>, which removes the privacy "
          "leak and the per-client dependency — and depends entirely "
          "on the server choosing to do it.",
          "<b>And the actual answer turned out to be shorter "
          "lifetimes:</b> <b>a certificate valid for weeks needs far "
          "less revocation than one valid for years</b>, because the "
          "exposure window closes on its own. <b>Which is why automated "
          "issuance mattered so much</b> — it made short lifetimes "
          "operationally possible. <b>Short lifetimes plus automation "
          "replaced revocation rather than fixing it</b>: an engineering "
          "answer to a problem that resisted a protocol answer for two "
          "decades."]),
  ("callout", "What to take from this module",
   ["<b>Use Ed25519 unless an external standard forces otherwise</b>, "
    "and <b>use a MAC whenever you do not actually need public "
    "verification or non-repudiation — which is considerably more "
    "often than people assume</b> (&sect;1).",
    "<b>Never implement certificate validation yourself.</b> <b>Use "
    "your platform's validator, and do not disable any of its "
    "checks</b> — every historical failure in &sect;2 was a skipped "
    "check, and <b>a <code>verify=False</code> in a client library is a "
    "security decision being made without one being taken.</b>",
    "<b>Understand that the trust root is social rather than "
    "mathematical</b> — <b>which is why pinning, transparency logs, "
    "and short lifetimes all exist</b>, and why none of them is "
    "cryptography. The strongest cipher in the world sits behind a "
    "hundred organisations' issuance procedures.",
    "<b>And state the dependency when you make a claim:</b> "
    "<b>'authentic, assuming no trusted certificate authority "
    "misissues'</b> is the honest form — which Module 13 develops "
    "into the general practice, and which is the program's closing rule "
    "appearing here as a specific conditional."]),
 ],
 "resources": [
   ("Aumasson &mdash; Serious Cryptography, chapter 12",
    "https://nostarch.com/serious-cryptography-2nd-edition",
    "<b>&sect;1's schemes</b>, with the ECDSA nonce hazard explained "
    "properly."),
   ("Ristic &mdash; Bulletproof TLS and PKI",
    "https://www.feistyduck.com/books/bulletproof-tls-and-pki/",
    "<b>&sect;2 through &sect;4 as the practical reference</b> — the "
    "best single treatment of the certificate ecosystem. Library "
    "copy."),
   ("Certificate Transparency (free)",
    "https://certificate.transparency.dev/",
    "<b>&sect;3's mitigation</b>, and worth reading as a design response "
    "to an unfixable trust model."),
   ("RFC 6979 &mdash; Deterministic ECDSA (free)",
    "https://www.rfc-editor.org/rfc/rfc6979",
    "<b>&sect;1's fix for the sharpest edge</b> — and a good example "
    "of removing a failure mode rather than warning about it."),
 ],
 "exercises": [
   "<b>Decide for five uses in your own system</b> whether a MAC or a "
   "signature is correct, and justify each.",
   "<b>Sign the same message twice with Ed25519</b> and with ECDSA, and "
   "compare the outputs.",
   "<b>Explain why one is identical and one is not</b>, and what follows "
   "for randomness.",
   "<b>Dump a real certificate chain</b> with OpenSSL and read every "
   "field.",
   "<b>Walk the chain by hand</b> against Part 2's validation list.",
   "<b>Count the root authorities</b> your operating system trusts.",
   "<b>Pick three and look up who operates them</b> and under which "
   "jurisdiction.",
   "<b>Look up your own domain in a Certificate Transparency log</b> and "
   "check for anything unexpected.",
   "<b>Determine whether your client fails open</b> on a failed "
   "revocation check.",
   "<b>Find one <code>verify=False</code></b> in code you have access to, "
   "and assess it.",
 ],
 "selfcheck": [
   "Give five differences between a MAC and a signature.",
   "Which property is unique to signatures, and what follows "
   "practically?",
   "Name four signature schemes and say which to prefer.",
   "Why is ECDSA hazardous, and what are the two fixes?",
   "What exactly does a certificate assert?",
   "Why is the trust root not cryptographic?",
   "Give the chain validation checklist, and the two historical "
   "failures.",
   "State the structural weakness of the CA model.",
   "Why does revocation fail, and what replaced it?",
   "Give the honest form of a certificate-based authenticity claim.",
 ],
},

]
