# -*- coding: utf-8 -*-
"""CSCE 711 Applied Cryptography — original course content."""

COURSE = {
    "code": "CSCE 711",
    "title": "Applied Cryptography",
    "tagline": "The primitives work. Using them correctly is the whole "
               "problem",
    "term": "Semester 9 (with CSCE 701 and CSCE 713)",
    "prereqs": "CSCE 629 Analysis of Algorithms for the complexity "
               "arguments and CSCE 658 Randomized Algorithms for the "
               "probabilistic reasoning; CSCE 701 runs in parallel and "
               "supplies the operational context",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A reviewed cryptographic design for a real "
                   "requirement — the primitives chosen with "
                   "justification, the key lifecycle specified, the "
                   "failure modes named, and the properties you are "
                   "<i>not</i> providing stated explicitly",
    "description": [
        "<b>This course is about using cryptography correctly, not "
        "about breaking it.</b> <b>The primitives are the part of "
        "security that works</b> — AES and SHA-2 have resisted "
        "decades of concentrated academic attack — and <b>nearly "
        "every real cryptographic failure is a misuse</b>: a reused "
        "nonce, a missing authentication tag, an unvalidated "
        "certificate, a key in a repository. <b>So the course is "
        "organised around correct construction and the specific ways it "
        "goes wrong.</b>",
        "<b>The governing rule is stated in Module 01 and never "
        "relaxed: do not design your own primitives, and do not "
        "assemble your own protocols from primitives.</b> <b>Use a "
        "reviewed high-level library.</b> This is not timidity — "
        "<b>it is the consistent lesson of every published break of a "
        "deployed system</b>, and the course teaches you enough to "
        "understand <i>why</i> the rule holds, which is what lets you "
        "apply it with judgement rather than as superstition.",
        "<b>The second theme is that confidentiality is the easy half "
        "and is rarely what you actually needed.</b> <b>Integrity, "
        "authentication, and freshness are what most systems get wrong</b> "
        "— encryption without authentication is a vulnerability "
        "rather than a protection, which Module 04 establishes "
        "concretely and which the AEAD construction exists to prevent.",
        "<b>The third is that key management is the real "
        "subject.</b> <b>A perfect cipher with a key in a Git "
        "repository provides nothing</b> (CSCE 701 Module 07), and "
        "<b>the questions of where keys live, who can read them, how "
        "they rotate, and what happens when one is exposed are harder "
        "and more consequential than any algorithm choice.</b> "
        "Modules 09 and 10 are about this.",
        "<b>And the closing position is about honest claims.</b> "
        "<b>Module 12 covers the post-quantum transition without "
        "overstating its urgency</b>, and <b>Module 13 is about stating "
        "precisely which properties a construction provides and under "
        "which assumptions</b> — because <b>'it is encrypted' is not "
        "a security property</b>, and naming the adversary, the "
        "property, and the assumption is.",
    ],
    "outcomes": [
        "State what each primitive provides and what it does not.",
        "Explain why randomness is the foundation and how it fails.",
        "Choose and use symmetric encryption correctly.",
        "Explain why authenticated encryption is the only acceptable "
        "default.",
        "Use hash functions for the right purposes and not the wrong "
        "ones.",
        "Explain key exchange and what public-key cryptography is "
        "for.",
        "Explain signatures, certificates, and the trust problem they "
        "do not solve.",
        "Read a TLS handshake and say what each step establishes.",
        "Store passwords and derive keys correctly.",
        "Design envelope encryption and a key lifecycle.",
        "Identify the implementation hazards that break correct "
        "designs.",
        "Assess the post-quantum transition proportionately.",
        "State a cryptographic claim honestly and completely.",
    ],
    "materials": [
        ("Aumasson — Serious Cryptography, 2nd edition",
         "https://nostarch.com/serious-cryptography-2nd-edition",
         "<b>The primary text, and the right level for this "
         "course.</b> Written by a practising cryptographer for "
         "engineers who must use the primitives correctly, and it is "
         "consistently honest about what is and is not settled. "
         "Library copy."),
        ("Boneh & Shoup — A Graduate Course in Applied Cryptography "
         "(free PDF)",
         "https://toc.cryptobook.us/",
         "<b>Free in full, and the rigorous companion.</b> Where this "
         "course states a property informally, Boneh and Shoup give the "
         "definition and the proof. Modules 03 through 07 follow its "
         "structure."),
        ("Katz & Lindell — Introduction to Modern Cryptography",
         "https://www.cs.umd.edu/~jkatz/imc.html",
         "<b>The standard text on the definitional approach</b> — "
         "why security is defined as a game against an adversary, which "
         "is Module 01 §3 and is the idea that makes the "
         "rest rigorous. Library copy."),
        ("The libsodium documentation (free)",
         "https://doc.libsodium.org/",
         "<b>The course's reference implementation, and the "
         "embodiment of Module 01's rule.</b> A small, opinionated, "
         "misuse-resistant API — read it as a design argument "
         "rather than only as documentation."),
        ("Cryptographic Right Answers, current edition (free)",
         "https://www.latacora.com/blog/2018/04/03/cryptographic-right-answers/",
         "<b>A short list of what to use, maintained by practitioners "
         "who review real systems.</b> Read it after Module 04 and "
         "again after Module 11 — it will read differently."),
        ("RFC 8446 (TLS 1.3) and RFC 9106 (Argon2) (free)",
         "https://www.rfc-editor.org/rfc/rfc8446",
         "<b>Module 08's and Module 09's primary sources.</b> TLS 1.3 "
         "is worth reading as an example of a protocol deliberately "
         "simplified to remove misuse, which is this course's thesis in "
         "standards form."),
    ],
    "tooling": [
        "<b>A reviewed high-level library, and nothing lower.</b> "
        "<b>libsodium, Google Tink, or your platform's equivalent</b> "
        "— and <b>Module 01 §4's rule is that the "
        "exercises are done with these, not with raw block cipher "
        "APIs</b>, with one deliberate exception noted below.",
        "<b>Python with <code>cryptography</code> and "
        "<code>pynacl</code></b>, which cover every exercise in the "
        "course and are both well maintained.",
        "<b>One deliberate exception:</b> <b>Module 11's exercises use "
        "a low-level API specifically to observe a misuse "
        "failing</b> — on your own test vectors, to build the "
        "intuition for why the rule exists. <b>Nothing from that module "
        "goes into a real system.</b>",
        "<b>OpenSSL's command line</b>, for inspecting certificates and "
        "handshakes in Module 08. <b>Reading a real certificate chain is "
        "worth more than a diagram of one.</b>",
        "<b>A hardware security key and a password manager</b>, used "
        "personally — the same recommendation CSCE 701 makes, for "
        "the same reason: <b>the material is more convincing once you "
        "have lived with the controls.</b>",
        "<b>And published test vectors</b> for everything you "
        "implement. <b>A construction that passes the official vectors "
        "is correct in a way that one which merely round-trips is "
        "not</b>, and this is the course's single most useful habit.",
    ],
    "projects": [
        {"title": "A primitive, implemented and validated", "after": 7,
         "brief": "Implement one primitive from its specification, "
                  "validate it against published test vectors, and then "
                  "write the argument for never using it.",
         "reqs": [
             "<b>One primitive implemented from its specification</b> "
             "— ChaCha20, SHA-256, or HMAC. <b>From the spec, not "
             "from a reference implementation.</b>",
             "<b>Validated against the official published test "
             "vectors</b>, with the validation code included and every "
             "vector passing.",
             "<b>A written account of every specification detail you "
             "got wrong first</b>, and how the vectors caught it.",
             "<b>A timing analysis</b>: identify any place your "
             "implementation branches or indexes on secret data "
             "(Module 11 §1).",
             "<b>And the argument for not using your own "
             "implementation</b>, written in your own words and "
             "specific to what you found.",
         ],
         "done": [
             "<b>Every official test vector passes</b> — which is "
             "binary, and which is the point of the exercise.",
             "<b>The specification mistakes documented honestly</b>, "
             "including the ones that round-tripped correctly and were "
             "still wrong. <b>This is the most instructive part and it "
             "is graded.</b>",
             "<b>At least one timing hazard identified in your own "
             "code</b>, because there will be one.",
             "<b>And the never-use-this argument specific rather than "
             "generic</b>: what exactly would have to be true for your "
             "implementation to be safe, and why it is not.",
         ]},
        {"title": "A cryptographic design, reviewed", "after": 12,
         "brief": "Specify a complete cryptographic design for a real "
                  "requirement, including the key lifecycle and the "
                  "properties you are not providing.",
         "reqs": [
             "<b>A stated requirement</b> with the assets, the "
             "adversary, and the properties needed — <b>confidentiality, "
             "integrity, authentication, and freshness treated "
             "separately</b>.",
             "<b>Primitive choices with justification</b>, each one "
             "from a reviewed library, with the library's misuse "
             "resistance assessed.",
             "<b>The complete key lifecycle:</b> generation, storage, "
             "distribution, rotation, revocation, and destruction "
             "(Module 10).",
             "<b>A named failure mode per component</b>, and what "
             "happens to the rest of the system when it occurs.",
             "<b>An explicit statement of what you are not "
             "providing</b> — metadata protection, forward secrecy, "
             "deniability, or post-compromise security.",
             "<b>And a rotation procedure you have actually "
             "executed</b> against a test deployment.",
         ],
         "done": [
             "<b>The four properties treated separately</b> — "
             "<b>conflating confidentiality with integrity is the "
             "failure this project exists to prevent</b>, and it is "
             "graded first.",
             "<b>The key lifecycle complete</b>, including destruction, "
             "which is the step always omitted.",
             "<b>The rotation procedure executed rather than "
             "described</b> (CSCE 701 Module 07 §3's "
             "point).",
             "<b>And the not-providing list specific and "
             "non-empty.</b> <b>A design that claims to provide "
             "everything has not been understood</b>, and this list is "
             "what distinguishes a reviewed design from a hopeful "
             "one.",
         ]},
    ],
    "map": [
        ("Boneh & Shoup — A Graduate Course in Applied Cryptography",
         "https://toc.cryptobook.us/",
         "<b>Modules 03–07 and 09.</b> Free, rigorous, and the "
         "source for every definition this course states informally. "
         "Read the chapter after the module, not before."),
        ("Dan Boneh — Cryptography I, Stanford (free)",
         "https://www.coursera.org/learn/crypto",
         "<b>Modules 01–07 as lectures</b>, from one of the "
         "authors above. Free to audit, and the best-paced "
         "presentation of the symmetric material available."),
        ("The libsodium documentation and Tink's design docs (free)",
         "https://doc.libsodium.org/",
         "<b>Modules 04, 10, and 11.</b> Read these as arguments about "
         "API design — <b>what each library refuses to let you do is "
         "the lesson.</b>"),
        ("RFC 8446 (TLS 1.3) (free)",
         "https://www.rfc-editor.org/rfc/rfc8446",
         "<b>Module 08 in the original.</b> Long, but the handshake "
         "section is readable and repays the effort more than any "
         "summary of it."),
        ("NIST Post-Quantum Cryptography project (free)",
         "https://csrc.nist.gov/projects/post-quantum-cryptography",
         "<b>Module 12's primary source</b> — the standards, the "
         "selection rationale, and the migration guidance, all free and "
         "all more measured than the surrounding commentary."),
        ("Cryptopals (free)",
         "https://cryptopals.com/",
         "<b>Optional, and a genuinely good complement to Project "
         "1</b> — a sequence of exercises in which you break "
         "deliberately broken constructions you build yourself, which "
         "teaches why the rules exist. <b>On your own code only.</b>"),
    ],
}

MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "What Cryptography Provides",
 "subtitle": "And the rule that follows from it.",
 "question": "What problem does cryptography actually solve?",
 "outcomes": [
     "Name the four properties and distinguish them.",
     "State what cryptography does not provide.",
     "Explain how security is defined against an adversary.",
     "State the course's governing rule and why it holds.",
     "Identify which property a requirement actually needs.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Four properties",
   "blurb": "Routinely conflated, and genuinely different."},

  {"t": "table", "kicker": "Properties", "title": "The four properties, and what each means",
   "header": ["Property", "The guarantee", "Provided by"],
   "widths": [2.8, 4.4, 4.6],
   "rows": [
     ["<b>Confidentiality</b>", "<b>The adversary learns nothing about the content</b>", "<b>Encryption (M03)</b>"],
     ["<b>Integrity</b>", "<b>Modification is detected</b>", "<b>MAC or signature (M04, M07)</b>"],
     ["<b>Authentication</b>", "<b>The message came from who you think</b>", "<b>MAC or signature (M04, M07)</b>"],
     ["<b>Freshness</b>", "<b>This is not an old message replayed</b>", "<b>Nonces, counters, timestamps</b>"],
   ],
   "footnote": "<b>Integrity and authentication are nearly the same "
               "mechanism and are not the same property</b> — a MAC "
               "gives both, and a checksum gives neither.",
   "note": "Freshness is the one most often forgotten entirely."},

  {"t": "callout", "title": "Encryption alone provides none of the other three",
   "kind": "The misconception this course exists to remove",
   "body": ["<b>A ciphertext can be modified by an adversary, and "
            "unauthenticated decryption will happily produce "
            "<i>different plaintext</i> without complaint.</b>",
            "<b>With a stream cipher this is exact:</b> <b>flipping a "
            "ciphertext bit flips the corresponding plaintext "
            "bit</b> — so an adversary who knows the plaintext "
            "format can make targeted changes without the key.",
            "<b>So 'it is encrypted' says nothing about whether it has "
            "been tampered with</b>, and <b>a system that decrypts "
            "unauthenticated data is processing attacker-controlled "
            "input while believing it is trusted.</b>",
            "<b>Which is why authenticated encryption is the only "
            "acceptable default</b> (Module 04) — <b>and why this "
            "is Part 1 rather than a later refinement.</b>"]},

  {"t": "section", "label": "Part 2", "title": "What it does not do",
   "blurb": "The honest boundary."},

  {"t": "bullets", "kicker": "Limits", "title": "What cryptography does not provide",
   "items": [
     "<b>It does not protect metadata.</b> <b>Who talked to whom, "
     "when, how often, and how much</b> — all visible, and "
     "frequently more revealing than the content.",
     "",
     "<b>It does not protect data in use.</b> <b>The plaintext "
     "exists in memory in the process that handles it</b>, which is "
     "where a compromised server reads it.",
     "",
     "<b>It does not establish trust.</b> <b>A signature proves a "
     "key signed it, not that the keyholder is who they claim</b> "
     "— which is Module 07's certificate problem.",
     "",
     "<b>It does not fix authorisation.</b> <b>An authenticated "
     "request from a user who should not be permitted to make it is "
     "still a vulnerability</b> (CSCE 701 Module 03).",
     "",
     "<b>And it does not survive bad key management</b>, which is "
     "where real failures live (Module 10).",
   ],
   "footnote": "<b>The metadata point is the one most often "
               "missed:</b> encrypting message bodies while leaking the "
               "social graph protects very little against an adversary "
               "who wanted the graph."},

  {"t": "section", "label": "Part 3", "title": "Defining security",
   "blurb": "As a game, which is what makes it rigorous."},

  {"t": "callout", "title": "A scheme is secure when a specified adversary cannot win a specified game",
   "kind": "Why the definitional approach matters",
   "body": ["<b>'Secure' alone is not a claim.</b> <b>The definition "
            "names the adversary's capabilities, the adversary's goal, "
            "and the probability of success considered "
            "acceptable.</b>",
            "<b>So for encryption, the standard definition is "
            "indistinguishability:</b> <b>an adversary who chooses two "
            "plaintexts and receives the encryption of one cannot tell "
            "which</b>, better than guessing.",
            "<b>And that definition is stronger than it looks:</b> "
            "<b>it implies the adversary learns no partial information "
            "at all</b> — not one bit, not the length "
            "relationship, nothing beyond what the length itself "
            "leaks.",
            "<b>Which is why this framing is worth the "
            "effort:</b> <b>it converts 'seems hard to break' into a "
            "precise statement that can be proved relative to an "
            "assumption</b> — and the assumption is then the thing "
            "to examine."]},

  {"t": "eq", "kicker": "Indistinguishability", "title": "The advantage, which is what gets bounded",
   "eqs": [
     ("Adv(A) = | Pr[A(Enc(m₀)) = 0] − Pr[A(Enc(m₁)) = 0] |",
      "The adversary A picks two equal-length plaintexts, receives "
      "the encryption of one, and guesses which."),
     ("secure  ⟺  Adv(A) is negligible for every efficient A",
      "Both quantifiers matter: every efficient adversary, and "
      "negligible rather than merely small."),
     ("m₀, m₁ chosen by A, with full knowledge of the scheme",
      "The adversary knows everything except the key — which is "
      "the only assumption worth making."),
   ],
   "caption": "<b>Security is a bound on an advantage, not an absolute "
              "property</b> — and 'efficient' and 'negligible' are "
              "the two terms doing the real work.",
   "note": "The advantage formulation is what connects to CSCE 637's "
           "complexity assumptions."},

  {"t": "section", "label": "Part 4", "title": "The rule",
   "blurb": "And the reason it is not timidity."},

  {"t": "callout", "title": "Do not design primitives, and do not assemble protocols",
   "kind": "The course's governing rule",
   "body": ["<b>Use a reviewed high-level library.</b> <b>libsodium, "
            "Tink, or your platform's audited equivalent</b> — and "
            "<b>prefer the API that gives you the fewest "
            "choices.</b>",
            "<b>The reason is the historical record:</b> <b>nearly "
            "every published break of a deployed system was a "
            "composition error or an implementation flaw rather than a "
            "broken primitive</b> — a reused nonce, a padding "
            "oracle, a missing tag check, an unvalidated curve "
            "point.",
            "<b>And those errors are invisible to testing.</b> <b>A "
            "misused construction encrypts and decrypts correctly and "
            "passes every functional test</b>, which is why the defect "
            "survives to production.",
            "<b>So the rule holds — and this course teaches you "
            "why it holds</b>, because <b>a rule you understand you can "
            "apply with judgement, and one you have merely been told you "
            "will eventually break.</b>"]},

  {"t": "bullets", "kicker": "Practice", "title": "Which means, concretely",
   "items": [
     "<b>Choose the library, not the algorithm.</b> <b>A good "
     "library has already made the algorithm, mode, and parameter "
     "choices</b>, and each choice you make yourself is a chance to "
     "make it wrong.",
     "",
     "<b>Prefer misuse-resistant APIs</b> — <b>one that "
     "generates its own nonce cannot have its nonce "
     "reused</b> (Module 11 §2).",
     "",
     "<b>Treat every low-level API as a warning sign.</b> <b>If you "
     "are choosing an IV, you are in the wrong "
     "abstraction.</b>",
     "",
     "<b>And if your requirement genuinely has no library answer, "
     "that is a signal to re-examine the requirement</b> before it is "
     "a signal to build something.",
     "",
     "<b>Project 1 implements a primitive precisely so that you "
     "never need to again</b> — the deliverable includes the "
     "argument for not using it.",
   ],
   "footnote": "<b>'If you are choosing an IV, you are in the wrong "
               "abstraction' is the operational form of the rule</b> "
               "— and it is a reliable test."},
 ],
 "takeaways": [
   "Confidentiality, integrity, authentication, and freshness are four "
   "different properties, and encryption provides only the first.",
   "Flipping a ciphertext bit in a stream cipher flips the corresponding "
   "plaintext bit, so unauthenticated decryption yields "
   "attacker-controlled plaintext.",
   "Cryptography does not protect metadata, data in use, trust "
   "establishment, authorisation, or you from bad key management.",
   "Security is defined as a bound on an adversary's advantage in a "
   "specified game, which makes 'secure' a precise claim.",
   "Nearly every published break of a deployed system was a composition "
   "or implementation error rather than a broken primitive.",
   "If you are choosing an IV, you are in the wrong abstraction.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The four properties"),
  ("table", ["Property", "The guarantee", "Provided by"],
   [["<b>Confidentiality</b>",
     "<b>The adversary learns nothing about the content</b> beyond its "
     "length.",
     "<b>Encryption</b> (Module 03)."],
    ["<b>Integrity</b>",
     "<b>Any modification of the message is detected.</b>",
     "<b>A message authentication code or a signature</b> "
     "(Modules 04 and 07)."],
    ["<b>Authentication</b>",
     "<b>The message originated from the party you believe it "
     "did.</b>",
     "<b>The same mechanisms</b> — see the note."],
    ["<b>Freshness</b>",
     "<b>This is not a valid old message being replayed.</b>",
     "<b>Nonces, counters, timestamps, or a challenge</b> — and it "
     "requires protocol-level thought rather than a primitive."]],
   [0.21, 0.37, 0.42]),
  ("p", "<b>Integrity and authentication are nearly the same mechanism "
        "and are not the same property.</b> <b>A MAC gives you both at "
        "once</b>, which is why they are frequently conflated — but "
        "<b>a checksum or CRC gives you neither</b>, because an adversary "
        "who modifies the message simply recomputes it. <b>And freshness "
        "is the one most often forgotten entirely</b>: a correctly "
        "authenticated message, captured and replayed an hour later, is "
        "still valid unless the protocol was designed to reject it."),
  ("callout", "Encryption alone provides none of the other three",
   ["<b>A ciphertext can be modified by an adversary in transit, and "
    "unauthenticated decryption will happily produce <i>different "
    "plaintext</i> without any complaint</b> — the receiver has no "
    "way to tell.",
    "<b>With a stream cipher the relationship is exact:</b> "
    "<b>flipping a ciphertext bit flips exactly the corresponding "
    "plaintext bit</b>, because the ciphertext is the plaintext XORed "
    "with a keystream. <b>So an adversary who knows the plaintext "
    "format — which is usually public — can make targeted, "
    "predictable changes without possessing the key at all.</b>",
    "<b>So 'it is encrypted' says precisely nothing about whether the "
    "data has been tampered with</b>, and <b>a system that decrypts "
    "unauthenticated data is processing attacker-controlled input while "
    "believing it is processing its own trusted data</b> — which is "
    "a far worse position than processing input it knows to be "
    "untrusted.",
    "<b>Which is why authenticated encryption is the only acceptable "
    "default</b> (Module 04) — <b>and why this appears in &sect;1 "
    "rather than as a later refinement</b>, because every subsequent "
    "module assumes it."]),

  ("h1", "2 &nbsp; What cryptography does not provide"),
  ("ul", ["<b>It does not protect metadata.</b> <b>Who communicated "
          "with whom, at what times, how often, and in what "
          "volumes</b> — all of it visible, and <b>frequently more "
          "revealing than the content</b>. See the note.",
          "<b>It does not protect data in use.</b> <b>The plaintext "
          "exists in memory in whatever process handles it</b>, which is "
          "exactly where a compromised server reads it — so "
          "encryption at rest and in transit leaves the window where the "
          "data is actually being used.",
          "<b>It does not establish trust.</b> <b>A valid signature "
          "proves that a particular key signed the message, not that the "
          "holder of that key is who they claim to be</b> — which is "
          "Module 07's certificate problem and is not a cryptographic "
          "problem at all.",
          "<b>It does not fix authorisation.</b> <b>A correctly "
          "authenticated request from a user who should not be permitted "
          "to make it is still a vulnerability</b> (CSCE 701 "
          "Module 03) — authentication answers who, and "
          "authorisation answers whether.",
          "<b>And it does not survive bad key management</b>, which is "
          "where the overwhelming majority of real failures live "
          "(Module 10, and CSCE 701 Module 07). <b>The metadata "
          "point is the one most often missed:</b> a messaging system "
          "that encrypts every message body while leaking the complete "
          "social graph protects very little against an adversary whose "
          "objective was the graph."]),

  ("break",),
  ("h1", "3 &nbsp; Defining security"),
  ("callout", "A scheme is secure when a specified adversary cannot win a "
              "specified game",
   ["<b>'Secure' on its own is not a claim at all.</b> <b>A definition "
    "names three things: the adversary's capabilities, the adversary's "
    "goal, and the success probability considered acceptable.</b> "
    "Change any one and you have a different claim.",
    "<b>So for encryption, the standard definition is "
    "indistinguishability under chosen-plaintext attack:</b> <b>an "
    "adversary who chooses two equal-length plaintexts and receives the "
    "encryption of one of them cannot tell which, appreciably better "
    "than guessing.</b>",
    "<b>And that definition is considerably stronger than it first "
    "looks:</b> <b>it implies the adversary learns no partial "
    "information whatsoever</b> — not a single bit, not whether two "
    "ciphertexts encrypt the same message, nothing beyond what the "
    "length itself discloses. <b>Any scheme leaking even one bit of "
    "the plaintext fails it</b>, which is why the bar is set there.",
    "<b>Which is why the framing is worth the effort:</b> <b>it "
    "converts 'this seems hard to break' into a precise statement that "
    "can be proved relative to a stated computational "
    "assumption</b> — and <b>the assumption then becomes the thing "
    "to examine</b>, which is CSCE 637's territory and is where the "
    "post-quantum question lives (Module 12)."]),
  ("eq", "Adv(A) = | Pr[A(Enc(m<sub>0</sub>)) = 0] &minus; "
         "Pr[A(Enc(m<sub>1</sub>)) = 0] |"),
  ("ul", ["<b>A</b> &mdash; the adversary: any algorithm at all, "
          "within a stated bound on its running time.",
          "<b>m<sub>0</sub>, m<sub>1</sub></b> &mdash; two plaintexts "
          "of equal length, chosen by the adversary with full knowledge "
          "of the scheme.",
          "<b>Adv(A)</b> &mdash; the advantage: how much better than "
          "a coin flip the adversary distinguishes the two cases.",
          "<b>Secure</b> &mdash; Adv(A) is negligible for every "
          "efficient A. <b>Security is a bound on an advantage rather "
          "than an absolute property</b>, and <b>'efficient' and "
          "'negligible' are the two terms doing the real work</b> — "
          "they are what tie the definition to CSCE 637's complexity "
          "assumptions."]),

  ("h1", "4 &nbsp; The rule"),
  ("callout", "Do not design primitives, and do not assemble protocols from "
              "primitives",
   ["<b>Use a reviewed high-level library.</b> <b>libsodium, Google "
    "Tink, or your platform's audited equivalent</b> — and <b>prefer "
    "whichever API gives you the fewest choices to make</b>, because each "
    "choice is an opportunity to choose wrongly.",
    "<b>The reason is the historical record rather than caution:</b> "
    "<b>nearly every published break of a deployed system was a "
    "composition error or an implementation flaw rather than a broken "
    "primitive</b> — a reused nonce, a padding oracle, a missing tag "
    "verification, an unvalidated curve point, a timing leak. <b>AES "
    "and SHA-256 have withstood decades of concentrated attack; the "
    "systems built on them have not.</b>",
    "<b>And those errors are essentially invisible to testing.</b> "
    "<b>A misused construction encrypts and decrypts correctly, "
    "round-trips perfectly, and passes every functional test you would "
    "think to write</b> — which is precisely why the defect survives "
    "into production and is found by an adversary rather than by CI.",
    "<b>So the rule holds — and this course spends thirteen "
    "modules on why it holds</b>, because <b>a rule you understand you "
    "can apply with judgement at the edge cases, and a rule you have "
    "merely been handed you will eventually break while believing you "
    "are the exception.</b>"]),
  ("ul", ["<b>Choose the library, not the algorithm.</b> <b>A good "
          "library has already made the algorithm, mode, padding, and "
          "parameter decisions</b> on the basis of expert review, and "
          "every one of those you make yourself is a chance to get it "
          "wrong.",
          "<b>Prefer misuse-resistant APIs.</b> <b>An interface that "
          "generates its own nonce internally cannot have its nonce "
          "reused by its caller</b> (Module 11 &sect;2) — the "
          "whole class of failure is removed by the API shape rather than "
          "by discipline.",
          "<b>Treat every low-level API as a warning sign.</b> <b>If "
          "you are choosing an IV, selecting a padding mode, or calling "
          "a bare block cipher, you are in the wrong "
          "abstraction</b> — and this is a reliable test you can "
          "apply to code in review.",
          "<b>And if your requirement genuinely has no library answer, "
          "that is a signal to re-examine the requirement</b> before it "
          "is a signal to build something novel. <b>The requirement is "
          "usually the thing that is wrong.</b>",
          "<b>Project 1 has you implement a primitive precisely so "
          "that you never need to again</b> — and its deliverable "
          "explicitly includes the argument for not using what you "
          "built, written from what you found while building it."]),
 ],
 "resources": [
   ("Aumasson &mdash; Serious Cryptography, chapters 1 and 2",
    "https://nostarch.com/serious-cryptography-2nd-edition",
    "<b>&sect;1 and &sect;3 at this course's level</b>, and the "
    "treatment of what security definitions are for is the clearest "
    "available."),
   ("Boneh & Shoup &mdash; A Graduate Course in Applied Cryptography, "
    "chapter 2 (free)",
    "https://toc.cryptobook.us/",
    "<b>&sect;3 rigorously</b> — the definitions, the advantage "
    "formulation, and what a security proof actually establishes."),
   ("Cryptographic Right Answers (free)",
    "https://www.latacora.com/blog/2018/04/03/cryptographic-right-answers/",
    "<b>&sect;4 as a practical list</b>, maintained by people who "
    "review real systems for a living. Short, and worth rereading after "
    "Module 11."),
   ("The libsodium documentation (free)",
    "https://doc.libsodium.org/",
    "<b>&sect;4's rule embodied in an API</b> — read what it "
    "refuses to let you do, which is the design argument."),
 ],
 "exercises": [
   "<b>Take a system you use</b> and state which of the four properties "
   "it needs for each kind of data it handles.",
   "<b>Find one place where integrity matters and confidentiality does "
   "not</b>, and one where the reverse holds.",
   "<b>Encrypt a known plaintext with a stream cipher</b>, flip one "
   "ciphertext bit, decrypt, and observe the result.",
   "<b>Predict which plaintext bit will change before you run it</b>, "
   "and check.",
   "<b>List the metadata your own application leaks</b> even with "
   "perfect encryption.",
   "<b>Write the indistinguishability game</b> in your own words, "
   "naming the adversary's powers.",
   "<b>Explain why a scheme leaking one plaintext bit fails the "
   "definition</b>, and why that is the right bar.",
   "<b>Find three low-level cryptographic API calls</b> in code you have "
   "access to, and say what the high-level replacement would be.",
   "<b>Apply the IV test</b> to a piece of code and record the "
   "verdict.",
   "<b>Write the rule in your own words</b>, with the reason, and keep "
   "it for Module 13.",
 ],
 "selfcheck": [
   "Name the four properties and what each guarantees.",
   "Why are integrity and authentication distinct, and what gives "
   "neither?",
   "Why does encryption alone provide none of the other three?",
   "What exactly happens when you flip a stream cipher ciphertext "
   "bit?",
   "Give five things cryptography does not provide.",
   "Why is the metadata point the one most often missed?",
   "How is security defined, and what three things does a definition "
   "name?",
   "What does indistinguishability imply about partial information?",
   "State the course's rule and the historical reason for it.",
   "Why are misuse errors invisible to testing?",
 ],
},

]

for _b in ("c711_b2",):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
