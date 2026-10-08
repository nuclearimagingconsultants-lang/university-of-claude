# -*- coding: utf-8 -*-
"""CSCE 711 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "TLS, as the Worked Example",
 "subtitle": "Every primitive so far, composed correctly.",
 "question": "What does a handshake actually establish, step by step?",
 "outcomes": [
     "Explain what each handshake step establishes.",
     "Explain what TLS 1.3 removed and why.",
     "Explain what TLS does and does not protect.",
     "Explain mutual authentication and when to use it.",
     "Read a real connection and assess it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The handshake",
   "blurb": "Four things, in order."},

  {"t": "code", "kicker": "Handshake", "title": "TLS 1.3, and what each step buys",
   "lang": "text", "code": """
  CLIENT HELLO
      supported versions, cipher suites, and an
      ephemeral key share (Module 06 section 4)
      -> establishes nothing yet; it is an offer

  SERVER HELLO
      chosen suite, its own ephemeral key share
      -> both sides can now derive a shared secret.
         Confidentiality, with SOMEBODY.

  SERVER CERTIFICATE + SIGNATURE
      the certificate chain, and a signature over the
      handshake transcript
      -> authentication. This is the step that says
         WHO, and it is why Module 07 exists.

  FINISHED (both sides)
      a MAC over the whole transcript
      -> integrity of the negotiation itself, so a
         downgrade or modification is detected.

  THEN application data, under an AEAD construction.
""",
   "caption": "<b>The transcript signature is the critical step</b> "
              "— it binds the authenticated identity to this "
              "specific exchange, defeating Module 06 §1's "
              "relay.",
   "note": "Walk the four steps in order; students conflate steps 2 "
           "and 3."},

  {"t": "callout", "title": "The signature is over the transcript, which is what defeats the relay",
   "kind": "The point most often missed",
   "body": ["<b>Signing the transcript binds the server's identity to "
            "<i>this exchange</i></b> — including the key shares "
            "that were actually sent.",
            "<b>So a relaying adversary cannot reuse it.</b> <b>The "
            "adversary's exchange has different key shares, so the "
            "transcript differs, so the captured signature does not "
            "verify</b> — and it cannot produce a new one without "
            "the private key.",
            "<b>Which is exactly the fix for Module 06 "
            "§1</b>: unauthenticated key exchange gives a "
            "secret with somebody, and a transcript signature names "
            "who.",
            "<b>And this is why 'sign the handshake' and 'sign a "
            "challenge' are different in strength</b> — a signature "
            "not bound to the session can be replayed into a different "
            "session."]},

  {"t": "section", "label": "Part 2", "title": "What 1.3 removed",
   "blurb": "A standard deleting options."},

  {"t": "table", "kicker": "Removed", "title": "What TLS 1.3 deleted, and the attack it closed",
   "header": ["Removed", "Why"],
   "widths": [4.4, 6.6],
   "rows": [
     ["<b>Non-ephemeral key exchange</b>", "<b>Forward secrecy is now mandatory (M06 §4)</b>"],
     ["<b>CBC mode and MAC-then-encrypt</b>", "<b>Padding oracles (M04 §2)</b>"],
     ["<b>RSA key transport</b>", "<b>Bleichenbacher's attack and descendants</b>"],
     ["<b>Renegotiation</b>", "<b>A family of injection attacks</b>"],
     ["<b>Compression</b>", "<b>Compression ratio leaks plaintext</b>"],
     ["<b>Custom DH groups</b>", "<b>Weak and backdoorable parameters (M06 §4)</b>"],
   ],
   "footnote": "<b>Every row is an option being deleted rather than "
               "deprecated</b> — because a negotiable weak option is "
               "a downgrade attack waiting to be found.",
   "note": "This table is the course's thesis in standards form."},

  {"t": "callout", "title": "Negotiable weakness is itself a vulnerability",
   "kind": "The design lesson worth generalising",
   "body": ["<b>If a protocol can negotiate a weak option, an "
            "adversary who can influence the negotiation will select "
            "it</b> — which turns every retained legacy option into "
            "an attack surface.",
            "<b>And this produced a decade of downgrade "
            "attacks</b> — version rollback, export-grade cipher "
            "revival, and protocol confusion, all of which exploited "
            "options kept for compatibility.",
            "<b>So TLS 1.3's approach was to remove rather than "
            "deprecate</b>, and to <b>authenticate the negotiation "
            "itself</b> so that tampering is detected "
            "(Part 1's Finished).",
            "<b>Which generalises beyond TLS:</b> <b>in any system "
            "you design, a configuration option that is unsafe will "
            "eventually be selected</b> — by a default, by a "
            "copied example, or by an adversary."]},

  {"t": "section", "label": "Part 3", "title": "What it protects",
   "blurb": "And the boundary people misjudge."},

  {"t": "bullets", "kicker": "Boundary", "title": "What TLS does and does not give you",
   "items": [
     "<b>It protects data in transit between two endpoints</b> "
     "— confidentiality, integrity, and server "
     "authentication.",
     "",
     "<b>It does not protect data at either endpoint.</b> <b>A "
     "compromised server sees plaintext</b>, which is where "
     "end-to-end designs differ (Module 10 §4).",
     "",
     "<b>It does not hide metadata.</b> <b>The destination address, "
     "the timing, and the traffic volume are visible</b>, and the "
     "server name was historically visible too "
     "(Module 01 §2).",
     "",
     "<b>It does not authenticate the client</b> unless you "
     "configure mutual TLS — so <b>server authentication is one "
     "direction only.</b>",
     "",
     "<b>And it says nothing about authorisation</b> — an "
     "authenticated connection from a party who should not be "
     "permitted is still a problem "
     "(CSCE 701 Module 03).",
   ],
   "footnote": "<b>'We use TLS' answers one question of "
               "four</b> — and the endpoint-compromise boundary is "
               "the one that matters most in practice."},

  {"t": "section", "label": "Part 4", "title": "Mutual TLS",
   "blurb": "And where it is the right tool."},

  {"t": "callout", "title": "Mutual TLS authenticates both ends with certificates",
   "kind": "Strong, and operationally demanding",
   "body": ["<b>The client presents a certificate too, and the server "
            "verifies it</b> — so <b>both ends are "
            "cryptographically identified</b> rather than one.",
            "<b>Which makes it excellent for service-to-service "
            "authentication</b>: no shared secrets to distribute, "
            "identity bound to a key, and it composes with "
            "CSCE 701 Module 04's segmentation.",
            "<b>And it is operationally demanding.</b> <b>Every "
            "client needs a certificate, which needs issuance, "
            "distribution, rotation, and revocation</b> — which is "
            "Module 07 §4's unsolved problem, now yours.",
            "<b>So the honest assessment:</b> <b>right for "
            "service-to-service inside infrastructure you operate, "
            "usually wrong for end users</b>, where the certificate "
            "lifecycle lands on people who cannot manage it."]},

  {"t": "bullets", "kicker": "Practice", "title": "Reading a connection, and what to check",
   "items": [
     "<b>The negotiated version and cipher suite.</b> <b>TLS 1.3 "
     "if possible, 1.2 with an AEAD suite at minimum</b>, and nothing "
     "older.",
     "",
     "<b>Whether the key exchange is ephemeral</b> — which "
     "determines forward secrecy and is visible in the suite "
     "name.",
     "",
     "<b>The certificate chain, its expiry, and its "
     "issuer</b> — and whether the name actually matches what you "
     "asked for (Module 07 §2).",
     "",
     "<b>Whether your client validates by default</b>, and whether "
     "anything in your codebase disables it.",
     "",
     "<b>And whether the server's configuration is current</b> "
     "— which is a patching question "
     "(CSCE 701 Module 08) rather than a cryptographic "
     "one.",
   ],
   "footnote": "<b>Run this against your own services.</b> <b>Most "
               "findings are configuration and currency rather than "
               "cryptography</b>, which is the course's second theme "
               "restated."},
 ],
 "takeaways": [
   "The handshake establishes confidentiality, then identity, then "
   "integrity of the negotiation — in that order, and the order "
   "matters.",
   "The server signs the transcript, not a challenge, which binds its "
   "identity to this exchange and defeats the relay from Module 06.",
   "TLS 1.3 deleted options rather than deprecating them, because a "
   "negotiable weak option is a downgrade attack waiting to be found.",
   "A configuration option that is unsafe will eventually be selected — "
   "by a default, a copied example, or an adversary.",
   "TLS protects data in transit between endpoints and protects nothing "
   "at either endpoint, which is the boundary most often misjudged.",
   "Mutual TLS is right for service-to-service and usually wrong for end "
   "users, because the certificate lifecycle lands on people.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The handshake"),
  ("code", """CLIENT HELLO
    supported versions, cipher suites, and an ephemeral
    key share (Module 06 section 4)
    -> establishes nothing yet; it is an offer

SERVER HELLO
    the chosen suite, and its own ephemeral key share
    -> both sides can now derive a shared secret.
       Confidentiality, with SOMEBODY.

SERVER CERTIFICATE + SIGNATURE
    the certificate chain, and a signature over the
    handshake transcript so far
    -> authentication. This is the step that says WHO,
       and it is the reason Module 07 exists.

FINISHED (both sides)
    a MAC over the entire transcript
    -> integrity of the negotiation itself, so a
       downgrade or any modification is detected.

THEN application data, under an AEAD construction
(Module 04), with keys derived from the exchange."""),
  ("callout", "The signature is over the transcript, which is what defeats "
              "the relay",
   ["<b>Signing the transcript binds the server's identity to <i>this "
    "particular exchange</i></b> — including the specific ephemeral "
    "key shares that were actually sent by both parties.",
    "<b>So a relaying adversary cannot reuse a captured "
    "signature.</b> <b>The adversary's own exchange with the client "
    "necessarily has different key shares, so the transcript differs, so "
    "the captured signature does not verify over it</b> — and the "
    "adversary cannot produce a fresh one without the server's private "
    "key.",
    "<b>Which is exactly the fix for Module 06 &sect;1:</b> "
    "<b>unauthenticated key exchange gives you a shared secret with "
    "somebody, and a transcript signature is what names who</b>. The "
    "two halves of the problem, solved by two different primitives, "
    "composed in this specific order.",
    "<b>And this is why 'sign the handshake' and 'sign a challenge' "
    "differ in strength</b> — <b>a signature not bound to the "
    "session can be replayed into a different session</b>, which is a "
    "mistake made regularly in custom authentication protocols and is one "
    "of the strongest arguments for Module 01 &sect;4's rule about "
    "assembling protocols."]),

  ("h1", "2 &nbsp; What TLS 1.3 removed"),
  ("table", ["What was removed", "The reason"],
   [["<b>Non-ephemeral (static) key exchange</b>",
     "<b>Forward secrecy is now mandatory rather than optional</b> "
     "(Module 06 &sect;4) — the option to omit it was itself the "
     "problem."],
    ["<b>CBC mode, and MAC-then-encrypt</b>",
     "<b>Padding oracle attacks</b> (Module 04 &sect;2 and "
     "&sect;4) — a long sequence of them, each patched and then "
     "re-found in a variant."],
    ["<b>RSA key transport</b>",
     "<b>Bleichenbacher's attack and its two decades of "
     "descendants</b> (Module 06 &sect;3), which kept returning "
     "because the construction was fragile."],
    ["<b>Renegotiation</b>",
     "<b>A family of injection attacks</b> in which an adversary's "
     "requests were prepended to an authenticated session."],
    ["<b>Compression</b>",
     "<b>The compression ratio leaks plaintext</b> — an adversary "
     "who can inject guesses observes whether they compressed well, "
     "recovering secrets byte by byte."],
    ["<b>Custom Diffie&ndash;Hellman groups</b>",
     "<b>Weak and potentially backdoorable parameters</b> "
     "(Module 06 &sect;4), and no way for a client to assess a group "
     "it was handed."]],
   [0.38, 0.62]),
  ("callout", "Negotiable weakness is itself a vulnerability",
   ["<b>If a protocol is able to negotiate a weak option, then an "
    "adversary who can influence the negotiation will cause it to be "
    "selected</b> — which turns every option retained for backwards "
    "compatibility into an active attack surface rather than a dormant "
    "one.",
    "<b>And this produced a full decade of downgrade attacks</b> "
    "— version rollback, the revival of deliberately weakened "
    "export-grade ciphers long after they were abandoned, cross-protocol "
    "confusion — <b>all of which exploited options kept for "
    "compatibility with systems nobody was still running.</b>",
    "<b>So TLS 1.3's approach was to remove rather than "
    "deprecate</b>, and additionally to <b>authenticate the negotiation "
    "itself</b> (&sect;1's Finished message) so that any tampering with "
    "what was offered or chosen is detected before application data "
    "flows.",
    "<b>Which generalises well beyond TLS:</b> <b>in any system you "
    "design, a configuration option that is unsafe will eventually be "
    "selected</b> — by an unfortunate default, by a copied "
    "Stack Overflow example, by a well-meaning compatibility fix, or by "
    "an adversary. <b>The only reliable remedy is for the unsafe option "
    "not to exist</b> (CSCE 701 Module 11 &sect;3's defaults "
    "argument, arriving from the other direction)."]),

  ("break",),
  ("h1", "3 &nbsp; What it protects"),
  ("ul", ["<b>It protects data in transit between two "
          "endpoints</b> — confidentiality, integrity, and "
          "authentication of the server. <b>Three of Module 01's four "
          "properties, for one hop.</b>",
          "<b>It does not protect data at either endpoint.</b> <b>A "
          "compromised server sees plaintext, because it must</b> — "
          "which is precisely where end-to-end encrypted designs differ, "
          "and is the architectural question of Module 10 &sect;4.",
          "<b>It does not hide metadata.</b> <b>The destination "
          "address, the connection timing, and the traffic volume are all "
          "visible to a network observer</b>, and <b>the requested "
          "server name was historically visible in the clear</b> as well "
          "(Module 01 &sect;2's first limitation).",
          "<b>It does not authenticate the client</b> unless you "
          "specifically configure mutual TLS (&sect;4) — so "
          "<b>authentication is one-directional by default</b>, and the "
          "application layer is left to identify the user.",
          "<b>And it says nothing whatsoever about "
          "authorisation</b> — <b>an authenticated connection from a "
          "party who should not be permitted to perform the requested "
          "action is still a vulnerability</b> (CSCE 701 "
          "Module 03). <b>'We use TLS' answers one question out of "
          "four</b>, and <b>the endpoint-compromise boundary is the one "
          "that matters most in practice</b>, because it is the one "
          "people genuinely misjudge when describing their system's "
          "guarantees to users."]),

  ("h1", "4 &nbsp; Mutual TLS, and reading a connection"),
  ("callout", "Mutual TLS authenticates both ends with certificates",
   ["<b>The client presents a certificate of its own, and the server "
    "validates it against a trusted issuer</b> — so <b>both ends "
    "are cryptographically identified</b> rather than only one, and the "
    "application layer need not re-establish who the caller is.",
    "<b>Which makes it excellent for service-to-service "
    "authentication:</b> <b>no shared secrets to distribute, identity "
    "bound to a key rather than to a bearer token that can be stolen and "
    "replayed, and it composes cleanly with CSCE 701 Module 04's "
    "segmentation and Module 03's authorisation.</b>",
    "<b>And it is operationally demanding.</b> <b>Every client needs "
    "a certificate, and every certificate needs issuance, secure "
    "distribution, rotation before expiry, and revocation when a client "
    "is decommissioned</b> — <b>which is Module 07 &sect;4's "
    "unsolved problem, now internal to your infrastructure.</b> A "
    "service mesh exists largely to automate exactly this.",
    "<b>So the honest assessment:</b> <b>right for service-to-service "
    "communication inside infrastructure you operate and can automate, "
    "and usually wrong for end users</b> — where the certificate "
    "lifecycle lands on people who cannot reasonably manage it, which is "
    "CSCE 701 Module 11 &sect;1's usability argument deciding a "
    "cryptographic question."]),
  ("ul", ["<b>The negotiated version and cipher suite.</b> <b>TLS 1.3 "
          "where possible, and TLS 1.2 with an AEAD suite as the "
          "minimum</b> — and nothing older, which is now a "
          "configuration question rather than a compatibility one.",
          "<b>Whether the key exchange is ephemeral</b>, which "
          "determines forward secrecy and is visible in the suite name "
          "itself (the ECDHE prefix).",
          "<b>The certificate chain, its expiry, and its "
          "issuer</b> — and critically <b>whether the name matches "
          "what you actually asked for</b> rather than what the "
          "certificate offers (Module 07 &sect;2's most-omitted "
          "check).",
          "<b>Whether your client library validates by default, and "
          "whether anything in your own codebase disables "
          "it</b> — which is a grep worth running across every "
          "repository you own.",
          "<b>And whether the server's TLS implementation is "
          "current</b>, which is a patching question (CSCE 701 "
          "Module 08) rather than a cryptographic one. <b>Run this "
          "against your own services:</b> <b>most findings turn out to "
          "be configuration and currency rather than "
          "cryptography</b> — which is this course's second theme, "
          "restated with evidence you gathered yourself."]),
 ],
 "resources": [
   ("RFC 8446 &mdash; TLS 1.3 (free)",
    "https://www.rfc-editor.org/rfc/rfc8446",
    "<b>&sect;1 and &sect;2 in the original</b> — and the handshake "
    "section is genuinely readable, which is unusual for an RFC."),
   ("Ristic &mdash; Bulletproof TLS and PKI",
    "https://www.feistyduck.com/books/bulletproof-tls-and-pki/",
    "<b>The whole module as the practical reference</b>, including the "
    "configuration guidance for &sect;4. Library copy."),
   ("The Illustrated TLS 1.3 Connection (free)",
    "https://tls13.xargs.org/",
    "<b>&sect;1 byte by byte</b>, annotated — the single best way to "
    "see the handshake concretely."),
   ("SSL Labs server test, and testssl.sh (free)",
    "https://www.ssllabs.com/ssltest/",
    "<b>&sect;4's checks, automated</b> — run against your own "
    "services, and read the explanations rather than only the grade."),
 ],
 "exercises": [
   "<b>Capture a TLS 1.3 handshake</b> and identify each of the four "
   "steps.",
   "<b>Say what each step established</b>, in your own words.",
   "<b>Explain why a captured transcript signature cannot be "
   "replayed</b> by a relay.",
   "<b>Contrast signing a transcript with signing a challenge</b>, and "
   "state which is stronger.",
   "<b>For each of the six removed features</b>, name the attack it "
   "enabled.",
   "<b>Find one unsafe configuration option</b> in a system you operate, "
   "and ask whether it could be deleted.",
   "<b>List what an observer learns</b> about your TLS traffic despite "
   "the encryption.",
   "<b>Test one of your own services</b> with a TLS scanner and read "
   "every finding.",
   "<b>Classify each finding</b> as cryptographic, configuration, or "
   "currency.",
   "<b>Decide whether mutual TLS is right</b> for one interface you "
   "operate, and justify it on lifecycle grounds.",
 ],
 "selfcheck": [
   "Give the four handshake steps and what each establishes.",
   "Why is the transcript signature the critical step?",
   "Why is signing a challenge weaker than signing a transcript?",
   "Name six things TLS 1.3 removed and the attack each closed.",
   "Why is a negotiable weak option a vulnerability?",
   "State the general design lesson and where else it applies.",
   "Give five things TLS does not provide.",
   "Which boundary is most often misjudged?",
   "When is mutual TLS right, and when wrong?",
   "What five things do you check when reading a connection?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Passwords and Key Derivation",
 "subtitle": "Where slow is the security property.",
 "question": "Why is a fast hash the wrong tool here?",
 "outcomes": [
     "Explain why password hashing differs from all other hashing.",
     "Explain salts, peppers, and what each prevents.",
     "Choose and parameterise a password hash.",
     "Distinguish password hashing from key derivation.",
     "Design a credential store and its migration.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why slow",
   "blurb": "The one place speed is a defect."},

  {"t": "callout", "title": "Passwords have far too little entropy to resist a fast hash",
   "kind": "The arithmetic",
   "body": ["<b>A human-chosen password carries perhaps 20 to 40 bits "
            "of real entropy</b> — not the 128 a key would "
            "have — <b>so the search space is small enough to "
            "enumerate.</b>",
            "<b>And a fast hash lets the adversary enumerate it.</b> "
            "<b>Commodity GPUs compute billions of SHA-256 hashes per "
            "second</b>, which exhausts a 40-bit space in minutes.",
            "<b>So the defence is to make each guess expensive.</b> "
            "<b>A hash taking 100 milliseconds reduces billions per "
            "second to ten per second per core</b> — a factor of "
            "roughly a hundred million.",
            "<b>Which is the only situation in cryptography where "
            "slowness is the security property</b> — and <b>why "
            "every hash from Module 05 §2's first group is "
            "exactly the wrong choice.</b>"]},

  {"t": "bullets", "kicker": "Mechanisms", "title": "Salt, pepper, and work factor",
   "items": [
     "<b>A salt is unique per password, stored alongside the "
     "hash</b>, and <b>need not be secret</b> "
     "(Module 02 §4).",
     "",
     "<b>It prevents precomputation and cross-user "
     "comparison</b> — <b>no rainbow tables, and two users with "
     "the same password get different hashes</b>, so a breach does not "
     "reveal that.",
     "",
     "<b>A pepper is a single secret added to every "
     "password</b>, stored separately from the database — <b>so a "
     "database-only breach yields unusable hashes.</b>",
     "",
     "<b>The work factor is the tunable cost</b>, and it must be "
     "raised over time as hardware improves.",
     "",
     "<b>And a memory cost is what resists GPUs</b> — which is "
     "the specific advance Argon2 and scrypt make over bcrypt.",
   ],
   "footnote": "<b>The memory-hardness point is the current "
               "state:</b> GPUs have enormous parallel compute and "
               "limited memory per core, so a memory-hard function "
               "narrows their advantage."},

  {"t": "section", "label": "Part 2", "title": "Choosing",
   "blurb": "And the parameters, which matter."},

  {"t": "code", "kicker": "Choice", "title": "What to use, and how to set it",
   "lang": "text", "code": """
  USE, IN ORDER OF PREFERENCE
      Argon2id    memory-hard, the current recommendation
      scrypt      memory-hard, older, well understood
      bcrypt      fine, widely available, no memory
                  hardness, and silently truncates input
                  at 72 bytes
      PBKDF2      acceptable only where a standard
                  requires it; weakest against GPUs

  NEVER
      SHA-256, SHA-3, BLAKE, MD5, or any fast hash
      a fast hash iterated by hand -- you will get the
          construction wrong, and it is still GPU-friendly

  SETTING PARAMETERS
      target 100-500 ms on YOUR production hardware,
      then raise it annually. Measure; do not copy a
      number from a blog post written for different
      hardware.
""",
   "caption": "<b>bcrypt's 72-byte truncation is a real trap</b> "
              "— a long passphrase is silently cut, so the extra "
              "length contributes nothing.",
   "note": "The measure-don't-copy instruction is the one that gets "
           "ignored."},

  {"t": "callout", "title": "The parameter is a budget decision, so state it that way",
   "kind": "How to argue for it",
   "body": ["<b>A higher work factor costs you CPU on every login and "
            "costs the adversary proportionally more per "
            "guess</b> — so the choice is a direct trade between "
            "your login capacity and the attacker's rate.",
            "<b>Which makes it quantifiable:</b> <b>at 100 ms and "
            "four cores you support about forty logins per second</b>, "
            "and you can say what doubling it costs in servers.",
            "<b>And the adversary's side is quantifiable too:</b> "
            "<b>state the guesses per second a GPU achieves at your "
            "parameters</b>, and how long a 30-bit password "
            "survives.",
            "<b>Which turns 'we should use stronger hashing' into a "
            "defensible number</b> — and is "
            "CSCE 701 §12's capability-metric argument "
            "applied to a parameter."]},

  {"t": "section", "label": "Part 3", "title": "Key derivation",
   "blurb": "A different problem, commonly conflated."},

  {"t": "table", "kicker": "Distinction", "title": "Password hashing versus key derivation",
   "header": ["", "Password hashing", "Key derivation (HKDF)"],
   "widths": [2.6, 4.2, 4.7],
   "rows": [
     ["<b>Input</b>", "<b>Low entropy, human-chosen</b>", "<b>High entropy already</b>"],
     ["<b>Goal</b>", "<b>Make guessing expensive</b>", "<b>Spread entropy into keys</b>"],
     ["<b>Speed</b>", "<b>Deliberately slow</b>", "<b>Fast is correct</b>"],
     ["<b>Output</b>", "<b>Stored for comparison</b>", "<b>Used as keys, never stored</b>"],
     ["<b>Use</b>", "<b>Argon2id</b>", "<b>HKDF</b>"],
   ],
   "footnote": "<b>Using HKDF on a password is a vulnerability, and "
               "using Argon2 to split a session secret is merely "
               "slow</b> — so the error is asymmetric and worth "
               "getting right.",
   "note": "The asymmetry makes the distinction memorable."},

  {"t": "bullets", "kicker": "HKDF", "title": "What HKDF is for",
   "items": [
     "<b>Deriving several independent keys from one shared "
     "secret</b> — which is exactly what TLS does after the "
     "handshake (Module 08 §1).",
     "",
     "<b>With a context label per key</b>, so that <b>the "
     "encryption key and the MAC key are independent and cannot be "
     "confused.</b>",
     "",
     "<b>Which removes a real hazard:</b> <b>using one key for two "
     "purposes has produced actual breaks</b>, and HKDF makes "
     "separation nearly free.",
     "",
     "<b>And it needs no slowness</b>, because the input already "
     "has full entropy — there is nothing to brute-force.",
     "",
     "<b>So: Argon2id for passwords, HKDF for everything derived "
     "from a real secret.</b>",
   ],
   "footnote": "<b>The per-purpose context label is the habit worth "
               "forming</b> — it costs one string and prevents key "
               "reuse across purposes."},

  {"t": "section", "label": "Part 4", "title": "The credential store",
   "blurb": "Including how to migrate it."},

  {"t": "callout", "title": "Migrating a credential store without knowing the passwords",
   "kind": "The problem everyone eventually has",
   "body": ["<b>You cannot rehash existing passwords, because you do "
            "not have them</b> — which is the point of hashing them "
            "in the first place.",
            "<b>So rehash on next successful login:</b> <b>verify "
            "against the old scheme, and if it passes, immediately "
            "compute and store the new hash</b> while you briefly hold "
            "the plaintext.",
            "<b>And record the scheme per record</b>, so both "
            "verification paths coexist — which means your stored "
            "format needs a scheme identifier from the start.",
            "<b>For accounts that never log in, eventually force a "
            "reset</b> — <b>and the migration is complete only when "
            "the old scheme is removed from the code</b>, which is the "
            "step usually left undone."]},

  {"t": "bullets", "kicker": "Store", "title": "What the store should look like",
   "items": [
     "<b>A scheme identifier, the parameters, the salt, and the "
     "hash</b> — all in one field, which is what the standard "
     "encoded formats give you.",
     "",
     "<b>Constant-time comparison of the result</b> "
     "(Module 04 §1), which the library's verify "
     "function already does.",
     "",
     "<b>Rate limiting and lockout on the login path</b>, because "
     "<b>a slow hash protects a stolen database and does nothing "
     "against online guessing</b> (CSCE 701 Module 02 "
     "§4).",
     "",
     "<b>No password length cap below something generous</b>, and "
     "no composition rules — which is the evidence-based "
     "guidance.",
     "",
     "<b>And a breached-password check</b>, which blocks the "
     "credentials that are actually used in attacks.",
   ],
   "footnote": "<b>The online-versus-offline distinction is "
               "essential:</b> hashing cost addresses an offline "
               "adversary with your database, and rate limiting "
               "addresses an online one."},
 ],
 "takeaways": [
   "Human-chosen passwords carry 20 to 40 bits of entropy, so a fast hash "
   "lets an adversary enumerate the whole space.",
   "This is the only place in cryptography where slowness is the security "
   "property, which is why every general-purpose hash is wrong.",
   "A salt prevents precomputation and cross-user comparison; a pepper "
   "stored separately makes a database-only breach useless.",
   "Memory hardness is what resists GPUs, since they have enormous "
   "parallel compute and little memory per core.",
   "Measure your work factor on your own production hardware rather than "
   "copying a number, and raise it annually.",
   "Migrate a credential store by rehashing on next successful login, and "
   "the migration ends when the old code path is deleted.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why slow"),
  ("callout", "Passwords have far too little entropy to resist a fast hash",
   ["<b>A human-chosen password carries perhaps 20 to 40 bits of real "
    "entropy</b> — not the 128 bits a generated key would have "
    "— because people choose from a small, heavily skewed "
    "distribution. <b>So the search space is small enough to enumerate "
    "exhaustively.</b>",
    "<b>And a fast hash is precisely what lets the adversary enumerate "
    "it.</b> <b>Commodity GPUs compute billions of SHA-256 hashes per "
    "second</b>, and purpose-built hardware does considerably better "
    "— which exhausts a 40-bit space in minutes and a 30-bit space "
    "instantly.",
    "<b>So the defence is to make each individual guess "
    "expensive.</b> <b>A hash that takes 100 milliseconds reduces "
    "billions per second to roughly ten per second per core</b> — a "
    "factor of about a hundred million, which converts minutes into "
    "centuries for the same password.",
    "<b>Which makes this the only situation in all of cryptography "
    "where slowness is the security property</b> — and <b>why every "
    "hash in Module 05 &sect;2's first group is exactly the wrong "
    "choice</b>, having been designed and optimised for the opposite "
    "goal."]),
  ("ul", ["<b>A salt is a unique random value per password, stored "
          "alongside the hash</b>, and <b>it need not be secret or even "
          "unpredictable</b> — only unique (Module 02 "
          "&sect;4).",
          "<b>It prevents precomputation and cross-user "
          "comparison:</b> <b>no precomputed table can cover all "
          "salts, and two users who chose the same password now have "
          "different stored hashes</b>, so a breach does not reveal which "
          "accounts share a password — which is itself valuable "
          "information to an attacker.",
          "<b>A pepper is a single secret value added to every "
          "password, stored separately from the database</b> — in a "
          "key management service or an environment secret (CSCE 701 "
          "Module 07) — <b>so that a database-only breach yields "
          "hashes that cannot be attacked at all.</b> <b>It is cheap and "
          "underused.</b>",
          "<b>The work factor is the tunable cost parameter</b>, and "
          "<b>it must be raised over time</b> as hardware improves "
          "— which means it is an operational commitment rather than "
          "a one-time decision.",
          "<b>And a memory cost is what actually resists GPUs</b>, "
          "which is the specific advance that Argon2 and scrypt make over "
          "bcrypt. <b>GPUs have enormous parallel compute and quite "
          "limited memory per execution unit</b>, so a function requiring "
          "substantial memory per evaluation narrows their advantage "
          "sharply — and that is the current state of the art."]),

  ("h1", "2 &nbsp; Choosing, and parameterising"),
  ("code", """USE, IN ORDER OF PREFERENCE
    Argon2id    memory-hard, the current recommendation
    scrypt      memory-hard, older, well understood
    bcrypt      fine, widely available, no memory
                hardness, and silently TRUNCATES its
                input at 72 bytes
    PBKDF2      acceptable only where a standard requires
                it; the weakest of these against GPUs

NEVER
    SHA-256, SHA-3, BLAKE, MD5, or any fast hash
    a fast hash iterated by hand -- you will get the
        construction wrong, and it remains GPU-friendly
        even when you do not

SETTING PARAMETERS
    target 100-500 ms on YOUR production hardware, then
    raise it annually. Measure it; do not copy a number
    from a blog post written for different hardware."""),
  ("p", "<b>bcrypt's 72-byte truncation is a real and surprising "
        "trap.</b> <b>A long passphrase is silently cut at 72 bytes, so "
        "every character beyond that contributes exactly nothing</b> "
        "— and no error is raised, which means a user who carefully "
        "chose a 100-character passphrase has a 72-byte one. <b>And the "
        "measure-don't-copy instruction is the one most often "
        "ignored:</b> a parameter set appropriate for 2015 server "
        "hardware is substantially too weak now, and parameters copied "
        "from documentation are frequently the library's conservative "
        "minimum rather than a recommendation."),
  ("callout", "The parameter is a budget decision, so state it that way",
   ["<b>A higher work factor costs you CPU time on every single login "
    "and costs the adversary proportionally more per guess</b> — so "
    "<b>the choice is a direct, quantifiable trade between your login "
    "throughput and the attacker's guessing rate.</b>",
    "<b>Which makes your side measurable:</b> <b>at 100 ms per hash "
    "on four dedicated cores you support roughly forty logins per "
    "second</b>, and you can state precisely what doubling the work "
    "factor costs in additional capacity at your peak login rate.",
    "<b>And the adversary's side is measurable too:</b> <b>state the "
    "guesses per second a GPU achieves against your actual "
    "parameters</b>, and therefore how long a 30-bit password survives "
    "an offline attack on a stolen database. <b>Both numbers are "
    "obtainable in an afternoon.</b>",
    "<b>Which turns 'we should use stronger password hashing' from an "
    "opinion into a defensible number with a stated cost</b> — and "
    "is <b>CSCE 701 Module 12 &sect;2's capability-metric argument "
    "applied to a single parameter</b>, which is the form in which it is "
    "easiest to win."]),

  ("break",),
  ("h1", "3 &nbsp; Key derivation, which is a different problem"),
  ("table", ["", "Password hashing", "Key derivation (HKDF)"],
   [["<b>Input</b>",
     "<b>Low entropy, human-chosen</b> — 20 to 40 bits.",
     "<b>High entropy already</b> — a shared secret from a key "
     "exchange, or a random master key."],
    ["<b>Goal</b>", "<b>Make each guess expensive.</b>",
     "<b>Spread existing entropy into several independent keys.</b>"],
    ["<b>Speed</b>", "<b>Deliberately slow.</b>",
     "<b>Fast is correct</b> — there is nothing to brute-force."],
    ["<b>Output</b>",
     "<b>Stored, for later comparison against a login attempt.</b>",
     "<b>Used immediately as keys, and never stored.</b>"],
    ["<b>Use</b>", "<b>Argon2id.</b>", "<b>HKDF.</b>"]],
   [0.17, 0.38, 0.45]),
  ("p", "<b>The error is asymmetric, which is what makes the "
        "distinction worth remembering.</b> <b>Using HKDF on a password "
        "is a vulnerability</b> — fast derivation over a low-entropy "
        "input means the password is brute-forceable — whereas "
        "<b>using Argon2 to split a high-entropy session secret is merely "
        "slow and wasteful</b>. <b>So when in doubt, the slow choice is "
        "the safe mistake</b>, which is a useful asymmetry to carry."),
  ("ul", ["<b>Deriving several independent keys from a single shared "
          "secret</b> — which is exactly what TLS does after the "
          "handshake completes (Module 08 &sect;1), producing "
          "separate keys per direction and per purpose.",
          "<b>With a distinct context label for each key</b>, so that "
          "<b>the encryption key and the authentication key are "
          "independent and cannot be confused or interchanged.</b>",
          "<b>Which removes a genuine hazard:</b> <b>using a single "
          "key for two different purposes has produced real breaks</b>, "
          "because the security proofs of two constructions do not "
          "generally compose when they share a key — and <b>HKDF "
          "makes the separation nearly free</b>, so there is no reason "
          "not to.",
          "<b>And it needs no slowness at all</b>, because the input "
          "already carries full entropy and there is consequently nothing "
          "to brute-force — which is the whole content of the "
          "distinction above.",
          "<b>So: Argon2id for anything derived from a password, and "
          "HKDF for everything derived from a real secret.</b> <b>The "
          "per-purpose context label is the habit worth forming</b> "
          "— it costs one string literal and prevents an entire "
          "class of key-reuse error."]),

  ("h1", "4 &nbsp; The credential store"),
  ("callout", "Migrating a credential store without knowing the passwords",
   ["<b>You cannot simply rehash the existing passwords, because you do "
    "not have them</b> — which is, of course, the entire point of "
    "having hashed them. So a migration cannot be a batch job.",
    "<b>So rehash on next successful login:</b> <b>verify the "
    "submitted password against the old scheme, and if it verifies, "
    "immediately compute and store the new hash</b> while you briefly "
    "hold the plaintext in memory. <b>This is the standard technique and "
    "it works well.</b>",
    "<b>And record the scheme per record</b>, so that both "
    "verification paths coexist during the transition — <b>which "
    "means your stored format needs a scheme identifier from the very "
    "beginning</b>, and adding one retroactively is the painful version "
    "of this migration.",
    "<b>For accounts that never log in again, eventually force a "
    "reset</b> — and <b>the migration is complete only when the old "
    "scheme is removed from the code</b>, which is the step usually left "
    "undone, leaving a weak verification path available indefinitely. "
    "<b>An unfinished migration is a retained vulnerability</b>, and it "
    "belongs on the project plan with a date."]),
  ("ul", ["<b>A scheme identifier, the parameters used, the salt, and "
          "the hash</b> — all in a single field, which is exactly "
          "what the standard encoded formats (the modular crypt format, "
          "or PHC strings) give you for free. <b>Use the library's "
          "encoded output rather than splitting it into columns.</b>",
          "<b>Constant-time comparison of the result</b> "
          "(Module 04 &sect;1), which the library's own verify "
          "function already handles correctly — so use it rather "
          "than comparing hashes yourself.",
          "<b>Rate limiting and lockout on the login path</b>, "
          "because <b>a slow hash protects a stolen database and does "
          "essentially nothing against online guessing</b> — the "
          "online adversary is limited by your server, not by the hash "
          "cost (CSCE 701 Module 02 &sect;4).",
          "<b>No password length cap below something generous, and no "
          "composition rules</b> — which is the evidence-based "
          "guidance that NIST adopted after the composition rules were "
          "shown to reduce entropy by making choices predictable "
          "(CSCE 701 Module 11 &sect;1).",
          "<b>And a check against known-breached passwords</b>, which "
          "blocks the credentials actually used in credential stuffing "
          "— far more effective per unit of user friction than any "
          "composition rule. <b>The online-versus-offline distinction is "
          "essential throughout:</b> <b>hashing cost addresses an "
          "offline adversary holding your database, and rate limiting "
          "addresses an online one</b>, and you need both because they "
          "are different adversaries."]),
 ],
 "resources": [
   ("RFC 9106 &mdash; Argon2 (free)",
    "https://www.rfc-editor.org/rfc/rfc9106",
    "<b>&sect;2's recommendation in the original</b>, including the "
    "parameter selection guidance and the variant rationale."),
   ("OWASP &mdash; Password Storage Cheat Sheet (free)",
    "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html",
    "<b>&sect;2 and &sect;4 as current practice</b>, maintained and "
    "updated as hardware moves — which matters for the "
    "parameters."),
   ("RFC 5869 &mdash; HKDF (free)",
    "https://www.rfc-editor.org/rfc/rfc5869",
    "<b>&sect;3's construction</b>, short, with the extract-then-expand "
    "rationale clearly stated."),
   ("NIST SP 800-63B, the memorized secret section (free)",
    "https://pages.nist.gov/800-63-3/sp800-63b.html",
    "<b>&sect;4's evidence-based guidance</b> — and notable as a "
    "standard that reversed long-standing advice on the basis of "
    "measurement."),
 ],
 "exercises": [
   "<b>Estimate the entropy</b> of five passwords you have seen chosen "
   "in practice.",
   "<b>Measure your hardware's SHA-256 rate</b> and compute how long a "
   "35-bit space takes.",
   "<b>Measure Argon2id at your chosen parameters</b> and recompute.",
   "<b>Tune your parameters to 250 ms</b> on your actual production "
   "hardware.",
   "<b>Compute your login throughput</b> at those parameters, and at "
   "double.",
   "<b>Demonstrate bcrypt's 72-byte truncation</b> with two passwords "
   "differing only after byte 72.",
   "<b>Add a pepper</b> to a test credential store and verify a "
   "database-only copy is unusable.",
   "<b>Use HKDF to derive two labelled keys</b> from one secret, and "
   "confirm they differ.",
   "<b>Implement rehash-on-login</b> for a scheme migration, with a "
   "scheme identifier.",
   "<b>Write the plan for removing the old path</b>, with a date.",
 ],
 "selfcheck": [
   "Why can a fast hash not protect passwords? Give the arithmetic.",
   "Why is slowness the security property only here?",
   "What does a salt prevent, and does it need to be secret?",
   "What does a pepper add, and where is it stored?",
   "Why does memory hardness resist GPUs?",
   "Name four password hashes in order, and bcrypt's trap.",
   "How do you set the work factor, and how do you argue for it?",
   "Give five differences between password hashing and key "
   "derivation.",
   "Why is the error asymmetric?",
   "How do you migrate a credential store, and when is it done?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Key Management",
 "subtitle": "The real subject, and the one with no clean answer.",
 "question": "Where does the key live, and who can read it?",
 "outcomes": [
     "Explain the key lifecycle and each stage's failure.",
     "Design envelope encryption and explain why.",
     "Explain rotation and what it does and does not "
     "accomplish.",
     "Explain the architectural choice around end-to-end "
     "encryption.",
     "Specify a complete key management design.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The lifecycle",
   "blurb": "Six stages, each a place to fail."},

  {"t": "table", "kicker": "Lifecycle", "title": "The six stages and the failure at each",
   "header": ["Stage", "The requirement", "How it fails"],
   "widths": [2.4, 4.1, 5.4],
   "rows": [
     ["<b>Generate</b>", "<b>From a CSPRNG, at full length</b>", "<b>Weak randomness (M02 §3)</b>"],
     ["<b>Store</b>", "<b>Where only the user can read it</b>", "<b>In the repository, image, or config</b>"],
     ["<b>Distribute</b>", "<b>Over an authenticated channel</b>", "<b>Emailed, pasted into chat, in a ticket</b>"],
     ["<b>Use</b>", "<b>In memory only, for as long as needed</b>", "<b>Logged, in a crash dump, in a trace</b>"],
     ["<b>Rotate</b>", "<b>On a schedule, and on compromise</b>", "<b>Never, because it was never tested</b>"],
     ["<b>Destroy</b>", "<b>Verifiably, including backups</b>", "<b>Omitted entirely</b>"],
   ],
   "footnote": "<b>Destruction is the stage always omitted</b>, and it "
               "is the one that decides whether deleting data actually "
               "deletes it — which is Part 3's crypto-shredding.",
   "note": "Walking the six stages is the practical core of the "
           "module."},

  {"t": "callout", "title": "A key is only as protected as the weakest place it exists",
   "kind": "And it exists in more places than you listed",
   "body": ["<b>Enumerate every location:</b> <b>the key store, the "
            "running process's memory, the backup, the developer's "
            "laptop, the CI system, the log that captured it "
            "once.</b>",
            "<b>And the adversary needs only one of them</b> "
            "— which is CSCE 701 Module 01's "
            "asymmetry arriving as a key management requirement.",
            "<b>So the design question is not 'is the key store "
            "secure' but 'what is the complete list of places this key "
            "has ever been'</b> — and that list is usually longer "
            "than the architecture diagram shows.",
            "<b>Which is why the best answer is for the key never to "
            "be in your process at all</b> — a platform key service "
            "performs the operation and returns the result, so the key "
            "has one location."]},

  {"t": "section", "label": "Part 2", "title": "Envelope encryption",
   "blurb": "The pattern that makes rotation possible."},

  {"t": "code", "kicker": "Envelope", "title": "The construction, and what it buys",
   "lang": "text", "code": """
  ENCRYPT
      generate a fresh data key (random, per object)
      encrypt the data with it (AEAD, Module 04)
      encrypt the data key with the master key
      store: [encrypted data key] + [ciphertext]

  DECRYPT
      decrypt the data key using the master key
      decrypt the data with the data key
      discard the data key

  WHY
      the master key encrypts only small values, so it
          can live in a key service and never leave it
      rotating the master key means re-encrypting only
          the small data keys -- not the data
      a leaked data key exposes one object
      and destroying a data key destroys that object's
          plaintext permanently (crypto-shredding)
""",
   "caption": "<b>Rotating the master key re-encrypts kilobytes rather "
              "than terabytes</b> — which is what makes rotation "
              "operationally possible at all.",
   "note": "The rotation economics are the reason this pattern is "
           "universal."},

  {"t": "section", "label": "Part 3", "title": "Rotation",
   "blurb": "What it does, and what it does not."},

  {"t": "callout", "title": "Rotation limits the damage window; it does not undo a compromise",
   "kind": "Stating it accurately",
   "body": ["<b>What it does:</b> <b>bounds how much data a single key "
            "protects, limits the window in which a leaked key is "
            "useful, and — critically — proves the procedure "
            "works.</b>",
            "<b>What it does not do:</b> <b>recover data already "
            "decrypted by an adversary, or protect anything encrypted "
            "under the old key if the adversary kept a copy of both the "
            "key and the ciphertext.</b>",
            "<b>And the real value is the tested procedure.</b> <b>An "
            "organisation that rotates quarterly can rotate in an hour "
            "during an incident</b>; one that never has cannot, which is "
            "when it matters.",
            "<b>So rotate on a schedule in order to be able to rotate "
            "on demand</b> — <b>which is "
            "CSCE 701 Module 07 §3's argument, "
            "and is the only reason scheduled rotation is worth "
            "the cost.</b>"]},

  {"t": "bullets", "kicker": "Rotation", "title": "Doing it without an outage",
   "items": [
     "<b>Support two keys at once:</b> <b>decrypt with either, "
     "encrypt with the new one</b> — which requires a key "
     "identifier stored with every ciphertext.",
     "",
     "<b>Which means the key identifier must be in the format from "
     "the start</b>, exactly as the scheme identifier was in "
     "Module 09 §4.",
     "",
     "<b>Then re-encrypt lazily on access, or in a background "
     "pass</b>, and <b>only remove the old key when nothing references "
     "it.</b>",
     "",
     "<b>And verify that by counting</b>, rather than by assuming "
     "— a query for ciphertexts under the old key identifier.",
     "",
     "<b>A rotation that cannot be verified complete is a rotation "
     "you will not finish</b>, which is the common outcome.",
   ],
   "footnote": "<b>The key identifier is the one design decision that "
               "makes everything else possible</b> — and it costs "
               "two bytes."},

  {"t": "section", "label": "Part 4", "title": "The architectural choice",
   "blurb": "Who holds the keys, and what that forecloses."},

  {"t": "callout", "title": "End-to-end encryption is an architectural decision with real costs",
   "kind": "Stated honestly, in both directions",
   "body": ["<b>If the server holds the keys, it can search, index, "
            "deduplicate, scan, recover accounts, and process the data "
            "— and it can be compelled or compromised into "
            "disclosure.</b>",
            "<b>If only the clients hold the keys, the server cannot "
            "read the data — and cannot provide search, "
            "server-side processing, or account recovery.</b>",
            "<b>And the lost-key problem is the hard part.</b> <b>True "
            "end-to-end means a user who loses their key loses their "
            "data</b>, so every real system adds a recovery mechanism "
            "— <b>which is then the weakest point.</b>",
            "<b>So the honest position is to state which you chose and "
            "what it forecloses</b> — <b>'end-to-end encrypted, "
            "with a recovery mechanism that can be compelled' is a "
            "complete claim, and 'end-to-end encrypted' alone is "
            "not.</b>"]},

  {"t": "bullets", "kicker": "Design", "title": "The specification to write",
   "items": [
     "<b>Every key in the system, with its purpose</b> — and "
     "nothing serving two purposes "
     "(Module 09 §3).",
     "",
     "<b>For each: where it is generated, stored, and used, and "
     "which components can read it.</b>",
     "",
     "<b>The rotation procedure, and the date it was last actually "
     "executed.</b>",
     "",
     "<b>What happens when each key is exposed</b> — the blast "
     "radius, per key, which is what makes the hierarchy worth "
     "designing.",
     "",
     "<b>And the destruction procedure, including backups</b> "
     "— <b>because 'we deleted it' is false if a backup holds the "
     "key and the ciphertext.</b>",
   ],
   "footnote": "<b>This specification is Project 2's deliverable</b>, "
               "and it is the artefact that distinguishes a design from "
               "an intention."},
 ],
 "takeaways": [
   "The six lifecycle stages each have a characteristic failure, and "
   "destruction is the one always omitted.",
   "A key is only as protected as the weakest place it exists, and that "
   "list is longer than the architecture diagram shows.",
   "Envelope encryption lets the master key encrypt only small values, so "
   "it can live in a key service and never leave it.",
   "Rotating the master key re-encrypts kilobytes rather than terabytes, "
   "which is what makes rotation operationally possible.",
   "Rotation's real value is the tested procedure — rotate on a "
   "schedule in order to be able to rotate on demand.",
   "'End-to-end encrypted, with a recovery mechanism that can be "
   "compelled' is a complete claim; 'end-to-end encrypted' alone is not.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The lifecycle"),
  ("table", ["Stage", "The requirement", "How it actually fails"],
   [["<b>Generate</b>",
     "<b>From a CSPRNG, at the full specified length.</b>",
     "<b>Weak or predictable randomness</b> (Module 02 &sect;3), "
     "which is silent and retroactive."],
    ["<b>Store</b>",
     "<b>Somewhere only the authorised user can read it.</b>",
     "<b>Committed to the repository, baked into a container image, "
     "left in a configuration file</b> (CSCE 701 Module 07)."],
    ["<b>Distribute</b>",
     "<b>Over an authenticated and confidential channel.</b>",
     "<b>Emailed, pasted into chat, attached to a ticket</b> — all "
     "of which retain it indefinitely and searchably."],
    ["<b>Use</b>",
     "<b>In memory only, for no longer than necessary.</b>",
     "<b>Logged, captured in a crash dump, included in a trace or an "
     "error report</b> — which is how keys reach third-party "
     "services."],
    ["<b>Rotate</b>",
     "<b>On a schedule, and immediately on suspected compromise.</b>",
     "<b>Never, because the procedure was never tested and nobody is "
     "willing to try it under pressure.</b>"],
    ["<b>Destroy</b>",
     "<b>Verifiably, including every backup and replica.</b>",
     "<b>Omitted entirely</b> — see the note."]],
   [0.16, 0.34, 0.50]),
  ("p", "<b>Destruction is the stage always omitted</b>, and it is the "
        "one that decides whether deleting data actually deletes it. "
        "<b>If you retain the key, you retain the plaintext</b> — so "
        "a deletion policy that leaves keys in a backup has not deleted "
        "anything, which matters legally as well as technically. "
        "<b>&sect;2's crypto-shredding is the mechanism that makes "
        "deletion real</b>, and it only works if the key destruction is "
        "genuinely complete."),
  ("callout", "A key is only as protected as the weakest place it exists",
   ["<b>Enumerate every location it has ever occupied:</b> <b>the key "
    "store, the running process's memory, the backup of that process's "
    "host, the developer's laptop where it was tested, the CI system that "
    "deployed it, the log line that captured it once eighteen months "
    "ago.</b>",
    "<b>And the adversary needs only one of them</b> — which is "
    "<b>CSCE 701 Module 01's defender's asymmetry arriving as a "
    "concrete key management requirement</b> rather than as a general "
    "principle.",
    "<b>So the design question is not 'is the key store secure' but "
    "'what is the complete list of places this key has ever "
    "existed'</b> — and <b>that list is reliably longer than the "
    "architecture diagram shows</b>, because the diagram records the "
    "intended flow rather than the historical one.",
    "<b>Which is why the best available answer is for the key never to "
    "be in your process at all.</b> <b>A platform key service performs "
    "the cryptographic operation and returns only the result</b>, so the "
    "key has exactly one location, never crosses a network in plaintext, "
    "and cannot be captured from your memory or your logs — and "
    "every use is audited for free (CSCE 701 Module 09 &sect;2)."]),

  ("h1", "2 &nbsp; Envelope encryption"),
  ("code", """ENCRYPT
    generate a fresh data key (random, per object)
    encrypt the data with it (AEAD, Module 04)
    encrypt the data key with the master key
    store: [encrypted data key] + [ciphertext]

DECRYPT
    decrypt the data key using the master key
    decrypt the data using the data key
    discard the data key from memory

WHY THIS PATTERN IS UNIVERSAL
    the master key encrypts only small values, so it can
        live inside a key service and never leave it
    rotating the master key means re-encrypting only the
        small data keys -- not the data itself
    a leaked data key exposes exactly one object
    and destroying a data key destroys that object's
        plaintext permanently (crypto-shredding), which
        is how deletion becomes verifiable"""),
  ("p", "<b>Rotating the master key re-encrypts kilobytes rather than "
        "terabytes</b> — which is <b>what makes rotation "
        "operationally possible at all</b>, and is the reason this pattern "
        "is universal in cloud key management. <b>A system that encrypts "
        "every object directly under one master key cannot rotate that key "
        "without rewriting all of its data</b>, which means in practice it "
        "will never rotate it, which means &sect;3's tested procedure does "
        "not exist."),

  ("break",),
  ("h1", "3 &nbsp; Rotation"),
  ("callout", "Rotation limits the damage window; it does not undo a "
              "compromise",
   ["<b>What it does:</b> <b>bounds how much data any single key "
    "protects, limits the window during which a leaked key remains "
    "useful, satisfies compliance requirements, and — "
    "critically — proves that the procedure actually works.</b>",
    "<b>What it does not do:</b> <b>recover data an adversary has "
    "already decrypted, or protect anything encrypted under the old key "
    "if the adversary retained a copy of both the key and the "
    "ciphertext.</b> <b>Rotation is forward-looking only</b>, and "
    "describing it otherwise is the common overclaim.",
    "<b>And the real value is the tested procedure.</b> <b>An "
    "organisation that rotates quarterly can rotate in an hour during an "
    "incident; one that has never rotated cannot</b> — and the "
    "incident is precisely when the capability is needed and when "
    "learning it is most expensive.",
    "<b>So rotate on a schedule in order to be able to rotate on "
    "demand</b> — <b>which is CSCE 701 Module 07 &sect;3's "
    "argument, and is genuinely the only reason scheduled rotation is "
    "worth its cost.</b> <b>The compliance requirement is a side "
    "effect; the capability is the point.</b>"]),
  ("ul", ["<b>Support two keys simultaneously:</b> <b>decrypt with "
          "either the old or the new key, and encrypt only with the "
          "new</b> — which <b>requires a key identifier stored "
          "alongside every ciphertext</b> so you know which to try.",
          "<b>Which means the key identifier must be in the stored "
          "format from the start</b>, exactly as the scheme identifier "
          "had to be in Module 09 &sect;4 — <b>the same design "
          "lesson, in a second place</b>, and adding either one "
          "retroactively is the painful migration.",
          "<b>Then re-encrypt lazily on access, or with a background "
          "pass over the data</b>, and <b>only remove the old key when "
          "nothing references it any longer.</b>",
          "<b>And verify that by counting rather than by "
          "assuming</b> — a query for ciphertexts still bearing the "
          "old key identifier, run to zero. <b>Which the key identifier "
          "makes a one-line query and which is otherwise "
          "impossible.</b>",
          "<b>A rotation that cannot be verified complete is a "
          "rotation you will not finish</b> — it will sit at "
          "'mostly done' indefinitely, with the old key retained "
          "just in case, which forfeits the entire benefit. <b>The key "
          "identifier is the one design decision that makes everything "
          "else possible, and it costs two bytes.</b>"]),

  ("h1", "4 &nbsp; The architectural choice"),
  ("callout", "End-to-end encryption is an architectural decision with real "
              "costs",
   ["<b>If the server holds the keys, it can search, index, "
    "deduplicate, scan for abuse, recover accounts, and process the data "
    "server-side — and it can be compelled by legal process or "
    "compromised into disclosure.</b> <b>Both halves of that are "
    "true</b>, and the capabilities are real product features rather than "
    "conveniences.",
    "<b>If only the clients hold the keys, the server cannot read the "
    "data at all — and therefore cannot provide server-side search, "
    "server-side processing, abuse detection on content, or account "
    "recovery.</b> <b>These are not implementation gaps; they are "
    "consequences.</b>",
    "<b>And the lost-key problem is the genuinely hard part.</b> "
    "<b>True end-to-end encryption means a user who loses their key "
    "loses their data permanently</b> — which is unacceptable to "
    "most users — <b>so every real system adds a recovery "
    "mechanism, and that mechanism is then the weakest point of the "
    "design</b> and the thing an adversary or a legal process targets.",
    "<b>So the honest position is to state which you chose and what it "
    "forecloses</b> — <b>'end-to-end encrypted, with a recovery "
    "mechanism that can be compelled' is a complete and honest claim, and "
    "'end-to-end encrypted' alone is not</b>. <b>Which is "
    "Module 13's practice, arriving in the place where the marketing "
    "pressure to overclaim is strongest.</b>"]),
  ("ul", ["<b>Every key in the system, with its single purpose</b> "
          "— and <b>nothing serving two purposes</b> "
          "(Module 09 &sect;3's context labels make this nearly "
          "free).",
          "<b>For each key: where it is generated, where it is "
          "stored, where it is used, and precisely which components and "
          "people can read it.</b>",
          "<b>The rotation procedure, and the date it was last "
          "actually executed</b> — not the date it was last "
          "documented, which is the number usually reported.",
          "<b>What happens when each key is exposed</b> — the "
          "blast radius, stated per key. <b>This is what makes designing "
          "a key hierarchy worth the effort</b>, because it is where you "
          "discover that one key's exposure compromises everything.",
          "<b>And the destruction procedure, including every "
          "backup</b> — <b>because 'we deleted the data' is simply "
          "false if a backup somewhere holds both the key and the "
          "ciphertext</b> (&sect;1's note). <b>This specification is "
          "Project 2's deliverable</b>, and <b>it is the artefact that "
          "distinguishes a design from an intention.</b>"]),
 ],
 "resources": [
   ("Google &mdash; Building Secure and Reliable Systems, the key "
    "management chapters (free PDF)",
    "https://sre.google/books/building-secure-reliable-systems/",
    "<b>&sect;1 through &sect;3 from operators</b> — and free in "
    "full. The strongest practical treatment available."),
   ("AWS KMS and Google Cloud KMS design documentation (free)",
    "https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html",
    "<b>&sect;2's pattern as implemented at scale</b> — read the "
    "envelope encryption and key hierarchy sections regardless of which "
    "platform you use."),
   ("Google Tink (free)",
    "https://developers.google.com/tink",
    "<b>&sect;2 and &sect;3 as a library</b> — keyset rotation and "
    "key identifiers are built in, which is the design argument made "
    "concrete."),
   ("NIST SP 800-57 &mdash; Key Management Recommendations (free)",
    "https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final",
    "<b>&sect;1's lifecycle, exhaustively</b> — reference rather "
    "than reading, and useful for the stages people skip."),
 ],
 "exercises": [
   "<b>Walk the six stages</b> for one key in a system you operate, and "
   "name the current failure.",
   "<b>Enumerate every location</b> one of your keys has ever "
   "existed.",
   "<b>Grep your logs and traces</b> for anything key-shaped.",
   "<b>Implement envelope encryption</b> with a data key per object.",
   "<b>Rotate the master key</b> and measure how much data you "
   "re-encrypted.",
   "<b>Add a key identifier</b> to a stored format that lacks one, and "
   "note the migration cost.",
   "<b>Execute a full rotation</b> and verify completion by counting.",
   "<b>Crypto-shred one object</b> by destroying its data key, and "
   "confirm the plaintext is unrecoverable.",
   "<b>Write the end-to-end trade-off</b> for your own system, with what "
   "each choice forecloses.",
   "<b>Write the complete key specification</b> — this is Project "
   "2.",
 ],
 "selfcheck": [
   "Name the six stages and the characteristic failure of each.",
   "Why is destruction the stage that decides whether deletion is "
   "real?",
   "Why is a key only as safe as its weakest location?",
   "Why is a platform key service the best answer?",
   "Describe envelope encryption and give four reasons for it.",
   "Why does it make rotation possible?",
   "State what rotation does and does not accomplish.",
   "Why rotate on a schedule at all?",
   "How do you rotate without an outage, and what must exist first?",
   "State the end-to-end trade-off and the honest form of the claim.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Implementation Hazards",
 "subtitle": "How correct designs fail in code.",
 "question": "The algorithm is right. Why is the system broken?",
 "outcomes": [
     "Explain timing side channels and constant-time "
     "programming.",
     "Explain nonce reuse consequences per construction.",
     "Explain what other side channels exist.",
     "Explain why error handling is a cryptographic concern.",
     "Review cryptographic code for these hazards.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Timing",
   "blurb": "The channel that defeats correct mathematics."},

  {"t": "callout", "title": "If execution time depends on secret data, the secret leaks",
   "kind": "The general principle",
   "body": ["<b>Any branch on a secret, any memory access at a "
            "secret-dependent index, and any loop whose count depends on "
            "a secret, leaks through timing.</b>",
            "<b>And the leak is exploitable remotely.</b> <b>Network "
            "noise averages out over enough samples</b>, and "
            "cache-timing attacks have recovered keys across process and "
            "virtual machine boundaries.",
            "<b>So constant-time means: the same operations in the "
            "same order regardless of the secret</b> — no early "
            "exit, no secret-indexed table lookup, no conditional "
            "branch.",
            "<b>Which is genuinely hard to write and harder to "
            "preserve</b> — <b>a compiler may reintroduce a branch "
            "while optimising code that was constant-time in "
            "source.</b>"]},

  {"t": "code", "kicker": "Constant time", "title": "The patterns, and what replaces them",
   "lang": "text", "code": """
  WRONG                    RIGHT
  if secret: a() else b()  compute both, select with a
                           mask
  memcmp(tag, expected)    constant-time compare
  table[secret_byte]       bitsliced or table-free
                           implementation
  while x: ...             a fixed iteration count
  return early on error    one exit, after all work

  SELECTION WITHOUT BRANCHING
      mask = -(condition)        // 0 or all ones
      result = (a & mask) | (b & ~mask)

  AND VERIFY IT HOLDS IN THE BINARY, not the source.
  Compilers reintroduce branches; a constant-time
  source file is not a constant-time program. Use
  dudect, ctgrind, or your platform's checker.
""",
   "caption": "<b>Verify in the binary</b> — the most common "
              "failure is a correct constant-time source that the "
              "compiler optimised into a branch.",
   "note": "The verify-the-binary point is what distinguishes real "
           "practice from the folklore."},

  {"t": "section", "label": "Part 2", "title": "Nonce reuse",
   "blurb": "Per construction, because it differs."},

  {"t": "table", "kicker": "Nonce reuse", "title": "What a repeated nonce costs you",
   "header": ["Construction", "Consequence of reuse"],
   "widths": [3.8, 7.2],
   "rows": [
     ["<b>CTR / stream cipher</b>", "<b>Plaintexts XORed; both usually recoverable (M03 §3)</b>"],
     ["<b>AES-GCM</b>", "<b>The above, plus the authentication key is recoverable — forgery follows</b>"],
     ["<b>CBC (IV reuse)</b>", "<b>Reveals whether two messages share a prefix</b>"],
     ["<b>AES-GCM-SIV</b>", "<b>Reveals only whether the plaintexts were equal</b>"],
     ["<b>ECDSA (nonce reuse)</b>", "<b>The private key is recoverable from two signatures (M07 §1)</b>"],
   ],
   "footnote": "<b>GCM is the worst case:</b> reuse costs you "
               "confidentiality <i>and</i> the ability to forge, which is "
               "why GCM-SIV and XChaCha20 exist.",
   "note": "Ranking the consequences is what makes the "
           "misuse-resistant choice obvious."},

  {"t": "callout", "title": "Uniqueness is harder than it sounds in a real system",
   "kind": "Why the misuse-resistant option is usually right",
   "body": ["<b>A counter is unique until the process restarts and "
            "loses it</b>, or until a snapshot is restored, or until the "
            "service is horizontally scaled.",
            "<b>And a random nonce is unique only probabilistically "
            "— at 96 bits, the birthday bound makes collision "
            "realistic after billions of messages</b> under one "
            "key.",
            "<b>So the practical answers are:</b> <b>a 192-bit random "
            "nonce (XChaCha20), or a misuse-resistant construction "
            "(GCM-SIV), or a fresh key per message</b> via envelope "
            "encryption (Module 10 §2).",
            "<b>Which is a design choice rather than a discipline "
            "problem</b> — <b>and choosing the construction that "
            "cannot fail this way is better than a procedure that must "
            "not.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Other channels",
   "blurb": "Briefly, and honestly about the threat model."},

  {"t": "bullets", "kicker": "Channels", "title": "The other side channels, and when to care",
   "items": [
     "<b>Cache timing</b> — which is Part 1, and is "
     "the one that matters for ordinary server software.",
     "",
     "<b>Power analysis and electromagnetic emission</b> — "
     "<b>relevant for smartcards and hardware you hand to an "
     "adversary</b>, and generally not for a server you operate.",
     "",
     "<b>Fault injection</b> — deliberately inducing errors "
     "to extract keys, which again requires physical access.",
     "",
     "<b>Speculative execution</b> — which crossed "
     "boundaries previously thought solid and is mitigated at the "
     "platform level (CSCE 701 Module 05).",
     "",
     "<b>And compression ratio</b> — <b>a logical channel "
     "rather than a physical one, and the reason TLS removed "
     "compression</b> (Module 08 §2).",
   ],
   "footnote": "<b>Be honest about your threat model here:</b> power "
               "analysis is a real attack and is almost certainly not "
               "<i>your</i> attack unless you ship hardware."},

  {"t": "section", "label": "Part 4", "title": "Errors",
   "blurb": "Which is where the design meets the oracle."},

  {"t": "callout", "title": "Distinguishable errors build a decryption oracle",
   "kind": "The hazard that lives in application code",
   "body": ["<b>If 'bad padding', 'bad tag', and 'bad length' are "
            "distinguishable — by message, by status code, or by "
            "timing — an adversary can use your system as a "
            "decryption service.</b>",
            "<b>Which is how padding oracle attacks recover "
            "plaintext</b> without the key, using nothing but the "
            "server's own error behaviour "
            "(Module 04 §4).",
            "<b>So: one opaque error for every cryptographic "
            "failure</b>, returned after the same amount of work, and "
            "<b>the detail logged internally where the adversary cannot "
            "read it.</b>",
            "<b>And this is the hazard most likely to be in code you "
            "personally write</b> — the primitives are in a "
            "library, and the error handling is in your request "
            "handler."]},

  {"t": "bullets", "kicker": "Review", "title": "What to look for in cryptographic code",
   "items": [
     "<b>Any <code>==</code> or <code>memcmp</code> on a tag, a "
     "token, or a hash</b> — the single most findable defect in "
     "this module.",
     "",
     "<b>Any nonce or IV supplied by application code</b>, and "
     "where it comes from.",
     "",
     "<b>Any distinguishable error path</b> after a decryption or "
     "verification failure.",
     "",
     "<b>Any key used for two purposes</b>, or derived without a "
     "context label (Module 09 §3).",
     "",
     "<b>And anything that parses, decompresses, or logs before "
     "verifying</b> — which is Module 04 §4's "
     "ordering rule.",
   ],
   "footnote": "<b>These five checks find most real defects</b>, and "
               "all five are mechanical enough to automate partially in "
               "a linter."},
 ],
 "takeaways": [
   "Any branch, memory index, or loop count that depends on a secret leaks "
   "it through timing, and the leak is remotely exploitable.",
   "Verify constant-time behaviour in the binary rather than the source, "
   "because compilers reintroduce branches while optimising.",
   "AES-GCM is the worst case for nonce reuse: it costs confidentiality "
   "and the authentication key, so forgery follows.",
   "Uniqueness is a design choice rather than a discipline problem — "
   "prefer a 192-bit nonce, a misuse-resistant construction, or a fresh "
   "key per message.",
   "Be honest about the threat model for physical side channels: power "
   "analysis is probably not your attack unless you ship hardware.",
   "Distinguishable decryption errors build an oracle, and this is the "
   "hazard most likely to be in code you personally wrote.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Timing"),
  ("callout", "If execution time depends on secret data, the secret leaks",
   ["<b>Any conditional branch on a secret value, any memory access at "
    "a secret-dependent index, and any loop whose iteration count depends "
    "on a secret, leaks information through timing.</b> <b>The "
    "mathematics being correct is irrelevant to this.</b>",
    "<b>And the leak is exploitable remotely, not merely in "
    "theory.</b> <b>Network jitter averages out over sufficiently many "
    "samples</b>, and <b>cache-timing attacks have recovered full keys "
    "across process boundaries and across virtual machine "
    "boundaries</b> on shared hardware — which is the ordinary "
    "deployment model for cloud computing.",
    "<b>So constant-time means precisely this: the same operations, in "
    "the same order, touching the same memory, regardless of the secret "
    "value</b> — no early exit, no secret-indexed table lookup, no "
    "conditional branch on secret data.",
    "<b>Which is genuinely hard to write and considerably harder to "
    "preserve</b> — <b>a compiler may reintroduce a branch while "
    "optimising code that was constant-time in its source form</b>, "
    "because the compiler is optimising for speed and knows nothing about "
    "your threat model. <b>This is the single strongest argument for "
    "Module 01 &sect;4's rule</b>: the people who maintain libsodium "
    "check the generated assembly, and you will not."]),
  ("code", """WRONG                    RIGHT
if secret: a() else b()  compute both, select with a mask
memcmp(tag, expected)    constant-time compare
table[secret_byte]       bitsliced or table-free
                         implementation
while x: ...             a fixed iteration count
return early on error    one exit, after all the work

SELECTION WITHOUT BRANCHING
    mask = -(condition)        // 0 or all ones
    result = (a & mask) | (b & ~mask)

AND VERIFY IT HOLDS IN THE BINARY, not in the source.
Compilers reintroduce branches; a constant-time source
file is not a constant-time program. Use dudect,
ctgrind, or your platform's checker, and read the
generated assembly for the hot path."""),
  ("p", "<b>Verify in the binary</b> — <b>the most common failure "
        "in practice is a correctly written constant-time source file that "
        "the compiler optimised into a branch</b>, which no amount of "
        "source review will catch. <b>This is what distinguishes real "
        "practice from the folklore</b>, and it is why constant-time "
        "primitives are frequently written in assembly or in a restricted "
        "dialect with optimisation barriers."),

  ("h1", "2 &nbsp; Nonce reuse"),
  ("table", ["Construction", "The consequence of reusing a nonce"],
   [["<b>CTR mode / any stream cipher</b>",
     "<b>The two plaintexts XORed together, and both usually "
     "recoverable</b> (Module 03 &sect;3's equation)."],
    ["<b>AES-GCM</b>",
     "<b>All of the above, <i>plus</i> the authentication key becomes "
     "recoverable</b> — after which the adversary can forge valid "
     "ciphertexts at will. See the note."],
    ["<b>CBC (IV reuse)</b>",
     "<b>Reveals whether two messages share a common prefix</b>, and how "
     "long it is — less catastrophic, and still a leak."],
    ["<b>AES-GCM-SIV</b>",
     "<b>Reveals only whether the two plaintexts were identical</b> "
     "— which is the point of a misuse-resistant construction."],
    ["<b>ECDSA (nonce reuse or bias)</b>",
     "<b>The private signing key is recoverable from two "
     "signatures</b> (Module 07 &sect;1) — total "
     "compromise."]],
   [0.30, 0.70]),
  ("p", "<b>GCM is the worst case, and it is also the most widely "
        "deployed.</b> <b>A repeated nonce costs you confidentiality "
        "<i>and</i> the ability to detect forgery</b>, because the "
        "authentication key is derived in a way that two ciphertexts under "
        "one nonce expose — so the adversary moves from reading to "
        "writing. <b>Which is exactly why AES-GCM-SIV and XChaCha20 "
        "exist</b>, and <b>ranking the consequences this way is what "
        "makes the misuse-resistant choice obvious</b> rather than "
        "merely advisable."),
  ("callout", "Uniqueness is harder than it sounds in a real system",
   ["<b>A counter is unique until the process restarts and loses "
    "it</b>, or until a virtual machine snapshot is restored to an "
    "earlier state, or until the service is scaled horizontally and two "
    "instances hold the same counter — each of which has caused real "
    "nonce reuse.",
    "<b>And a random nonce is unique only probabilistically.</b> <b>At "
    "96 bits — which is AES-GCM's nonce size — the birthday "
    "bound makes a collision realistic after a few billion messages under "
    "a single key</b>, which large systems reach.",
    "<b>So the practical answers are structural:</b> <b>a 192-bit "
    "random nonce (XChaCha20-Poly1305), a misuse-resistant construction "
    "(AES-GCM-SIV), or a fresh key per message</b> via envelope "
    "encryption (Module 10 &sect;2) — any of which removes the "
    "requirement rather than managing it.",
    "<b>Which makes this a design choice rather than a discipline "
    "problem</b> — and <b>choosing a construction that cannot fail "
    "this way is strictly better than operating a procedure that must "
    "not</b>, because procedures are executed by systems under conditions "
    "their designers did not anticipate."]),

  ("break",),
  ("h1", "3 &nbsp; The other channels"),
  ("ul", ["<b>Cache timing</b> — which is &sect;1, and <b>is the "
          "one that genuinely matters for ordinary server software</b> "
          "running on shared hardware.",
          "<b>Power analysis and electromagnetic emission</b> — "
          "<b>relevant for smartcards, hardware tokens, and any device "
          "you hand to an adversary</b>, and generally not relevant for a "
          "server in a datacentre you control.",
          "<b>Fault injection</b> — deliberately inducing "
          "computational errors with voltage or clock glitching to "
          "extract keys, which again requires physical possession and is "
          "a hardware design concern.",
          "<b>Speculative execution</b> — which crossed isolation "
          "boundaries previously believed solid, and is mitigated at the "
          "platform and compiler level rather than by application code "
          "(CSCE 701 Module 05).",
          "<b>And compression ratio</b> — <b>a logical rather "
          "than a physical channel, and precisely the reason TLS removed "
          "compression</b> (Module 08 &sect;2). <b>Be honest about "
          "your threat model here:</b> <b>power analysis is a real and "
          "serious attack, and it is almost certainly not <i>your</i> "
          "attack unless you ship hardware</b> — and spending effort "
          "on it while leaving a <code>memcmp</code> on a tag is the "
          "wrong allocation."]),

  ("h1", "4 &nbsp; Errors, and review"),
  ("callout", "Distinguishable errors build a decryption oracle",
   ["<b>If 'bad padding', 'bad authentication tag', and 'malformed "
    "length' are distinguishable from one another — by error "
    "message, by HTTP status code, by response size, or by response "
    "timing — then an adversary can use your system as a decryption "
    "service.</b>",
    "<b>Which is exactly how padding oracle attacks recover "
    "plaintext</b> without ever obtaining the key, using nothing but the "
    "server's own error behaviour as the oracle (Module 04 "
    "&sect;4) — and the attack is efficient, requiring a few hundred "
    "queries per byte.",
    "<b>So: one opaque error for every cryptographic failure</b>, "
    "returned after performing the same amount of work in every case, and "
    "<b>with the diagnostic detail logged internally where the adversary "
    "cannot read it</b> (CSCE 701 Module 09 &sect;1).",
    "<b>And this is the hazard most likely to appear in code you "
    "personally wrote</b> — <b>the primitives are inside a library "
    "maintained by specialists, and the error handling is in your own "
    "request handler</b>, written while thinking about debuggability "
    "rather than about oracles. <b>Which makes it the highest-yield "
    "thing to look for in your own code.</b>"]),
  ("ul", ["<b>Any <code>==</code> or <code>memcmp</code> applied to a "
          "tag, a token, a hash, or a signature</b> — <b>the single "
          "most findable defect in this module</b>, and a grep away.",
          "<b>Any nonce or IV supplied by application code</b>, and "
          "specifically where that value comes from and whether its "
          "uniqueness survives a restart or a scale-out (&sect;2).",
          "<b>Any distinguishable error path</b> following a decryption "
          "or verification failure — including differences in "
          "logging, timing, and response shape rather than only in the "
          "message text.",
          "<b>Any key used for two purposes</b>, or any key derived "
          "without a per-purpose context label (Module 09 "
          "&sect;3) — which is cheap to fix and easy to miss.",
          "<b>And anything that parses, decompresses, deserialises, or "
          "logs before verifying</b> — which is Module 04 "
          "&sect;4's ordering rule, and is where cryptographic failure "
          "meets CSCE 713's memory-safety and injection material. "
          "<b>These five checks find most real defects</b>, and <b>all "
          "five are mechanical enough to automate at least partially in a "
          "linter</b>, which is a worthwhile afternoon."]),
 ],
 "resources": [
   ("Aumasson &mdash; Serious Cryptography, the implementation "
    "chapters",
    "https://nostarch.com/serious-cryptography-2nd-edition",
    "<b>&sect;1 and &sect;2 at engineering level</b>, with the "
    "constant-time patterns and the misuse consequences."),
   ("BearSSL &mdash; Constant-Time Cryptography (free)",
    "https://www.bearssl.org/constanttime.html",
    "<b>&sect;1's best single reference</b> — thorough, practical, "
    "and honest about what the compiler does to you."),
   ("Bernstein &mdash; Cache-timing attacks on AES (free)",
    "https://cr.yp.to/antiforgery/cachetiming-20050414.pdf",
    "<b>&sect;1's threat demonstrated</b> — and the paper that "
    "changed how AES is implemented in software."),
   ("Joux &mdash; Authentication failures in NIST GCM (free)",
    "https://csrc.nist.gov/csrc/media/projects/block-cipher-techniques/documents/bcm/comments/800-38-series-drafts/gcm/joux_comments.pdf",
    "<b>&sect;2's GCM row, in the original</b> — why nonce reuse "
    "costs the authentication key specifically."),
 ],
 "exercises": [
   "<b>Write a non-constant-time tag comparison</b> and measure the "
   "timing difference across guesses.",
   "<b>Implement branchless selection with a mask</b> and verify it "
   "produces the right answer.",
   "<b>Compile a constant-time function with optimisation on</b> and "
   "read the generated assembly.",
   "<b>Find whether the compiler reintroduced a branch</b>, and report "
   "what you found.",
   "<b>Reuse a nonce with AES-GCM</b> on your own test data and "
   "recover the two plaintexts.",
   "<b>Do the same with AES-GCM-SIV</b> and compare what you can "
   "extract.",
   "<b>Determine whether your nonce scheme survives</b> a process "
   "restart and a horizontal scale-out.",
   "<b>Switch one construction to XChaCha20</b> and note what "
   "requirement disappeared.",
   "<b>Audit one error path</b> for distinguishability in message, "
   "status, size, and timing.",
   "<b>Run Part 4's five checks</b> across a codebase and report the "
   "findings.",
 ],
 "selfcheck": [
   "State the timing principle and the three things that leak.",
   "Why is a timing leak remotely exploitable?",
   "Give five wrong patterns and their constant-time replacements.",
   "Why must you verify in the binary?",
   "Give the nonce reuse consequence for five constructions.",
   "Why is GCM the worst case?",
   "Why is uniqueness hard, and what are the three structural "
   "answers?",
   "Name five other side channels and say which matters to you.",
   "How does a distinguishable error build an oracle?",
   "Give the five review checks.",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Post-Quantum Cryptography",
 "subtitle": "Assessed proportionately.",
 "question": "What actually breaks, and when should you act?",
 "outcomes": [
     "State precisely what a quantum computer breaks.",
     "Explain why symmetric cryptography is largely fine.",
     "Explain the harvest-now-decrypt-later argument.",
     "Name the standardised schemes and their costs.",
     "Plan a migration proportionate to your threat model.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What breaks",
   "blurb": "Specifically, and not everything."},

  {"t": "table", "kicker": "Impact", "title": "What a large quantum computer does to each primitive",
   "header": ["Primitive", "Impact", "Response"],
   "widths": [3.0, 4.2, 4.6],
   "rows": [
     ["<b>RSA, DH, ECDH, ECDSA</b>", "<b>Broken — Shor's algorithm, polynomial time</b>", "<b>Replace (Part 3)</b>"],
     ["<b>AES-128</b>", "<b>Grover's: 2⁶⁴ work</b>", "<b>Use AES-256</b>"],
     ["<b>AES-256</b>", "<b>Grover's: 2¹²⁸ — still infeasible</b>", "<b>Nothing</b>"],
     ["<b>SHA-256</b>", "<b>Collision search improves modestly</b>", "<b>Nothing, or SHA-384</b>"],
     ["<b>HMAC, AEAD</b>", "<b>Inherit the above — essentially fine</b>", "<b>Nothing</b>"],
   ],
   "footnote": "<b>So it is a public-key problem, not a cryptography "
               "problem</b> — Grover's algorithm gives a square-root "
               "speedup, which doubling the key length answers "
               "completely.",
   "note": "Separating Shor from Grover is what makes this module "
           "proportionate."},

  {"t": "callout", "title": "Shor's algorithm breaks the structure; Grover's only searches faster",
   "kind": "The distinction that sets the response",
   "body": ["<b>Shor's algorithm factors integers and computes "
            "discrete logarithms in polynomial time</b> — which "
            "<b>destroys RSA and every elliptic-curve scheme "
            "completely</b>, not merely weakens them.",
            "<b>Grover's algorithm gives a square-root speedup on "
            "unstructured search</b> — so <b>an n-bit key gives "
            "n/2 bits of security</b>, which is answered entirely by "
            "doubling n.",
            "<b>So symmetric cryptography needs a parameter change and "
            "public-key cryptography needs replacement</b> — a "
            "qualitative difference, and the whole basis of a "
            "proportionate response.",
            "<b>And the post-quantum schemes rest on different "
            "problems rather than better algorithms</b> — lattices "
            "and codes, for which no quantum advantage is known "
            "(Module 06 §2's fourth row)."]},

  {"t": "section", "label": "Part 2", "title": "The timing question",
   "blurb": "And the one argument for acting now."},

  {"t": "callout", "title": "Harvest now, decrypt later is the argument that justifies action today",
   "kind": "And it applies to some data and not others",
   "body": ["<b>An adversary can record encrypted traffic now and "
            "decrypt it when a capable machine exists</b> — so "
            "<b>the relevant question is how long your data must stay "
            "confidential</b>, not when the machine arrives.",
            "<b>Which makes it a data-classification question.</b> "
            "<b>A session token expiring in an hour is unaffected; "
            "medical records, state secrets, and identity documents are "
            "not.</b>",
            "<b>And the honest position on timing is that nobody "
            "knows.</b> <b>Current machines are many orders of magnitude "
            "short</b>, and <b>the engineering gap is large and the "
            "progress is real</b> — both halves are true.",
            "<b>So: migrate key exchange first, because that is where "
            "harvesting applies</b> — and <b>signatures are less "
            "urgent, because a signature forged in 2040 on a 2026 "
            "document is a smaller problem.</b>"]},

  {"t": "bullets", "kicker": "Priority", "title": "Which to migrate, in order",
   "items": [
     "<b>1 · Key exchange protecting long-lived "
     "confidential data</b> — <b>this is the only genuinely "
     "urgent case</b>, and hybrid deployment addresses it now.",
     "",
     "<b>2 · Long-lived signing keys and root "
     "certificates</b>, whose validity extends decades — firmware "
     "signing keys especially.",
     "",
     "<b>3 · Ordinary TLS</b>, which your platform will "
     "migrate for you and where you mainly need to not "
     "obstruct it.",
     "",
     "<b>4 · Everything else</b>, on the normal upgrade "
     "cycle.",
     "",
     "<b>And cryptographic agility is the real deliverable:</b> "
     "<b>a system that can change algorithm without redesign</b>, which "
     "is Module 10 §3's key identifier applied to "
     "algorithms.",
   ],
   "footnote": "<b>Agility is worth more than any specific "
               "algorithm choice</b> — because the next transition "
               "will also happen, and the ability to make it is the "
               "durable asset."},

  {"t": "section", "label": "Part 3", "title": "The schemes",
   "blurb": "And what they cost."},

  {"t": "code", "kicker": "Standards", "title": "The standardised schemes and their trade",
   "lang": "text", "code": """
  KEY ENCAPSULATION
      ML-KEM (Kyber)     the standard choice.
          public key ~1.2 kB, ciphertext ~1.1 kB
          vs X25519's 32 bytes each.
          Fast, and the size is the cost.

  SIGNATURES
      ML-DSA (Dilithium) the general-purpose choice.
          signature ~2.4 kB vs Ed25519's 64 bytes.
      SLH-DSA (SPHINCS+) hash-based, very conservative
          assumptions, much larger and slower.
          For firmware and roots of trust.

  THE COST IS SIZE, NOT SPEED
      which matters for constrained links, embedded
      devices, certificate chains, and anything that
      must fit in one packet.

  AND DEPLOY HYBRID: classical + post-quantum together,
  secure if EITHER holds. The schemes are newer and have
  had less cryptanalysis.
""",
   "caption": "<b>Hybrid is the right default during a "
              "transition</b> — it hedges against the new scheme "
              "being broken, which has already happened to several "
              "candidates.",
   "note": "The hybrid argument is the practical recommendation."},

  {"t": "section", "label": "Part 4", "title": "Proportionality",
   "blurb": "And what not to do."},

  {"t": "callout", "title": "What a proportionate response looks like",
   "kind": "Closing",
   "body": ["<b>Inventory where you use public-key "
            "cryptography</b> — which most organisations cannot "
            "currently answer, and which is the actual first step "
            "(CSCE 701 Module 08 §3).",
            "<b>Classify your data by how long it must stay "
            "confidential</b>, and <b>act on the long-lived "
            "portion.</b>",
            "<b>Enable hybrid key exchange where your platform offers "
            "it</b> — which is increasingly a configuration change "
            "rather than a project.",
            "<b>And build agility rather than switching "
            "algorithms:</b> <b>algorithm identifiers in stored formats, "
            "no hardcoded key sizes, and a tested procedure for "
            "changing</b> — which is what you will need "
            "again."]},

  {"t": "bullets", "kicker": "Avoid", "title": "And what not to do",
   "items": [
     "<b>Do not use a non-standardised scheme.</b> <b>Several "
     "candidates were broken during the selection process</b>, some "
     "spectacularly and late.",
     "",
     "<b>Do not abandon classical cryptography.</b> <b>Hybrid, "
     "not replacement</b> — the new schemes have had far less "
     "cryptanalysis than RSA has.",
     "",
     "<b>Do not treat it as urgent for short-lived data</b>, which "
     "is most data, and where the effort is better spent "
     "elsewhere.",
     "",
     "<b>Do not let it displace the work that matters.</b> <b>No "
     "organisation has been compromised by a quantum computer, and many "
     "by a leaked credential</b> (CSCE 701 Module 13 "
     "§4).",
     "",
     "<b>And do not claim quantum resistance you have not "
     "deployed</b> — which is Module 13.",
   ],
   "footnote": "<b>The last two are the honest proportionality "
               "point:</b> this is a real problem on a long timescale, "
               "and it is not your most likely cause of a breach this "
               "year."},
 ],
 "takeaways": [
   "Shor's algorithm destroys RSA and all elliptic-curve schemes; Grover's "
   "gives only a square-root speedup that doubling the key length answers.",
   "So this is a public-key problem rather than a cryptography problem, "
   "and AES-256 and SHA-256 need essentially nothing.",
   "Harvest-now-decrypt-later makes it a data-classification question: how "
   "long must this stay confidential?",
   "Migrate key exchange for long-lived confidential data first; "
   "signatures are less urgent.",
   "The post-quantum schemes cost size rather than speed, and hybrid "
   "deployment hedges against the newer scheme being broken.",
   "Cryptographic agility is worth more than any specific algorithm "
   "choice, because the next transition will also happen.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What actually breaks"),
  ("table", ["Primitive", "The impact", "The response"],
   [["<b>RSA, Diffie&ndash;Hellman, ECDH, ECDSA, Ed25519</b>",
     "<b>Broken</b> — Shor's algorithm solves factoring and "
     "discrete log in polynomial time.",
     "<b>Replace</b> (&sect;3)."],
    ["<b>AES-128</b>",
     "<b>Grover's algorithm: roughly 2<sup>64</sup> work rather than "
     "2<sup>128</sup>.</b>",
     "<b>Use AES-256.</b> A parameter change, not a redesign."],
    ["<b>AES-256</b>",
     "<b>Grover's: roughly 2<sup>128</sup></b> — which remains "
     "entirely infeasible.",
     "<b>Nothing.</b>"],
    ["<b>SHA-256</b>",
     "<b>Collision search improves modestly</b>, and not "
     "dramatically.",
     "<b>Nothing, or move to SHA-384 for very long-lived "
     "commitments.</b>"],
    ["<b>HMAC, AEAD constructions</b>",
     "<b>Inherit the symmetric situation above</b> — essentially "
     "fine.",
     "<b>Nothing.</b>"]],
   [0.26, 0.38, 0.36]),
  ("callout", "Shor's algorithm breaks the structure; Grover's only searches "
              "faster",
   ["<b>Shor's algorithm factors integers and computes discrete "
    "logarithms in polynomial time</b> — which <b>destroys RSA and "
    "every elliptic-curve scheme completely rather than merely weakening "
    "them</b>, because it exploits the algebraic structure those schemes "
    "are built on.",
    "<b>Grover's algorithm gives a square-root speedup on unstructured "
    "search</b> — so <b>an n-bit key provides about n/2 bits of "
    "security against it</b>, which is answered completely and cheaply by "
    "doubling n. <b>And the speedup does not parallelise well</b>, which "
    "makes even that estimate conservative.",
    "<b>So symmetric cryptography needs a parameter change and "
    "public-key cryptography needs replacement</b> — <b>a "
    "qualitative difference, and the entire basis of a proportionate "
    "response</b>. The common framing of 'quantum breaks encryption' "
    "collapses this distinction and produces badly allocated effort.",
    "<b>And the post-quantum schemes rest on different mathematical "
    "problems rather than on better algorithms</b> — lattice "
    "problems and error-correcting codes, for which <b>no quantum "
    "advantage is currently known</b> (Module 06 &sect;2's fourth "
    "row). <b>Which is a weaker guarantee than it sounds:</b> 'no known "
    "quantum algorithm' is the same kind of claim as 'no known classical "
    "algorithm' was for factoring, and &sect;4's hybrid recommendation "
    "follows from taking that seriously."]),

  ("h1", "2 &nbsp; The timing question"),
  ("callout", "Harvest now, decrypt later is the argument that justifies "
              "action today",
   ["<b>An adversary can record encrypted traffic today and decrypt it "
    "whenever a sufficiently capable machine exists</b> — storage is "
    "cheap and patience is free — so <b>the relevant question is how "
    "long your data must remain confidential</b>, rather than when the "
    "machine arrives.",
    "<b>Which makes this a data-classification question rather than a "
    "cryptography question.</b> <b>A session token that expires in an "
    "hour is entirely unaffected; medical records, genomic data, state "
    "secrets, and identity documents have confidentiality requirements "
    "measured in decades and are affected now.</b>",
    "<b>And the honest position on timing is that nobody knows.</b> "
    "<b>Current machines are many orders of magnitude short of what "
    "Shor's algorithm requires at cryptographic scale</b>, and <b>the "
    "remaining engineering gap is large while the progress is "
    "real</b> — both halves of that are true, and any confident "
    "date in either direction is not supported.",
    "<b>So: migrate key exchange first, because key exchange is "
    "precisely where harvesting applies</b> — and <b>signatures are "
    "considerably less urgent, because a signature forged in 2040 on a "
    "document from 2026 is a much smaller problem than that document's "
    "contents being read.</b> <b>That asymmetry is the single most "
    "useful planning insight in this module.</b>"]),
  ("ul", ["<b>1 &middot; Key exchange protecting long-lived "
          "confidential data</b> — <b>the only genuinely urgent "
          "case</b>, and hybrid deployment addresses it today with "
          "available software.",
          "<b>2 &middot; Long-lived signing keys and roots of "
          "trust</b>, whose validity extends over decades — "
          "<b>firmware signing keys especially</b>, since a device shipped "
          "now may be in service in twenty years and cannot have its root "
          "replaced.",
          "<b>3 &middot; Ordinary TLS</b>, which your platform and "
          "your browser vendors will migrate for you — and where "
          "<b>your main job is to not obstruct it</b> by pinning "
          "algorithms or inspecting traffic with middleboxes that cannot "
          "be updated.",
          "<b>4 &middot; Everything else</b>, on the normal upgrade "
          "cycle, as libraries and platforms deliver it.",
          "<b>And cryptographic agility is the real deliverable:</b> "
          "<b>a system that can change algorithm without being "
          "redesigned</b> — which is Module 10 &sect;3's key "
          "identifier argument applied to algorithm selection, and is the "
          "same design lesson for the third time. <b>Agility is worth "
          "more than any specific algorithm choice</b>, because <b>the "
          "next transition will also happen</b>, and the ability to make "
          "it is the durable asset."]),

  ("break",),
  ("h1", "3 &nbsp; The schemes"),
  ("code", """KEY ENCAPSULATION
    ML-KEM (Kyber)     the standard choice.
        public key ~1.2 kB, ciphertext ~1.1 kB,
        against X25519's 32 bytes each.
        Computationally fast; the size is the cost.

SIGNATURES
    ML-DSA (Dilithium) the general-purpose choice.
        signature ~2.4 kB against Ed25519's 64 bytes.
    SLH-DSA (SPHINCS+) hash-based, very conservative
        assumptions, substantially larger and slower.
        For firmware and roots of trust, where the
        conservatism is worth the cost.

THE COST IS SIZE, NOT SPEED
    which matters for constrained links, embedded
    devices, certificate chains, and anything that has
    to fit inside a single packet.

AND DEPLOY HYBRID: classical plus post-quantum together,
secure if EITHER holds. The new schemes are newer and
have had far less cryptanalysis."""),
  ("p", "<b>Hybrid is the right default during a transition.</b> <b>It "
        "hedges against the new scheme being broken, which has already "
        "happened to several candidates</b> — including some that "
        "reached late rounds of the standardisation process and were then "
        "broken by classical attacks, in one case on a laptop in under an "
        "hour. <b>That history is the strongest argument for hybrid</b>, "
        "and it costs only bandwidth."),

  ("h1", "4 &nbsp; Proportionality"),
  ("callout", "What a proportionate response looks like",
   ["<b>Inventory where you use public-key cryptography</b> — "
    "<b>which most organisations cannot currently answer</b>, and which "
    "is therefore the actual first step rather than any algorithm "
    "decision (CSCE 701 Module 08 &sect;3's inventory argument, "
    "arriving in a second context).",
    "<b>Classify your data by how long it must remain "
    "confidential</b>, and <b>act on the long-lived portion</b> — "
    "which for most organisations is a small and identifiable fraction of "
    "everything they hold.",
    "<b>Enable hybrid key exchange where your platform offers "
    "it</b> — which is increasingly a configuration change rather "
    "than a project, and is already deployed by default in several major "
    "browsers and TLS libraries.",
    "<b>And build agility rather than merely switching "
    "algorithms:</b> <b>algorithm identifiers in every stored format, no "
    "hardcoded key or signature sizes, no assumptions that a public key "
    "fits in 32 bytes, and a procedure for changing that you have "
    "actually executed</b> — which is what you will need again, for "
    "the transition after this one."]),
  ("ul", ["<b>Do not use a non-standardised scheme.</b> <b>Several "
          "candidates were broken during the selection process</b>, some "
          "spectacularly and some very late — which is exactly what "
          "a standardisation process is for.",
          "<b>Do not abandon classical cryptography.</b> <b>Hybrid, "
          "not replacement</b> — the post-quantum schemes have had a "
          "small fraction of the cryptanalytic attention that RSA and "
          "elliptic curves have absorbed over forty years.",
          "<b>Do not treat it as urgent for short-lived data</b>, "
          "which is the great majority of data, and where the same effort "
          "spent on &sect;4's inventory or on CSCE 701's identity "
          "controls buys considerably more security.",
          "<b>Do not let it displace the work that actually "
          "matters.</b> <b>No organisation has yet been compromised by a "
          "quantum computer, and a great many have been compromised by a "
          "leaked credential or an unpatched dependency</b> "
          "(CSCE 701 Module 13 &sect;4's ordering).",
          "<b>And do not claim quantum resistance you have not "
          "deployed</b> — which is Module 13's subject and is "
          "already a common marketing overclaim. <b>The last two points "
          "are the honest proportionality position:</b> <b>this is a real "
          "problem on a long timescale, and it is not your most likely "
          "cause of a breach this year</b> — and holding both of "
          "those at once is the judgement this module is trying to "
          "develop."]),
 ],
 "resources": [
   ("NIST Post-Quantum Cryptography project (free)",
    "https://csrc.nist.gov/projects/post-quantum-cryptography",
    "<b>&sect;3's standards and the selection rationale</b> — free, "
    "and considerably more measured than most commentary on the "
    "subject."),
   ("NSA CNSA 2.0 and the NIST migration guidance (free)",
    "https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/3148990/",
    "<b>&sect;2's timelines as published by parties who must plan "
    "them</b> — useful as a datum rather than a prediction."),
   ("Bernstein & Lange &mdash; Post-quantum cryptography (free)",
    "https://pqcrypto.org/",
    "<b>&sect;1 and &sect;3 from researchers in the field</b>, including "
    "candid assessment of the assumptions."),
   ("Open Quantum Safe (free)",
    "https://openquantumsafe.org/",
    "<b>&sect;3 and &sect;4 as working code</b> — hybrid TLS you can "
    "actually deploy and measure."),
 ],
 "exercises": [
   "<b>State precisely what Shor's and Grover's algorithms each do</b>, "
   "and the response to each.",
   "<b>Explain why AES-256 needs nothing</b> while RSA needs "
   "replacement.",
   "<b>Classify your own data</b> by required confidentiality "
   "lifetime.",
   "<b>Identify which of it is affected</b> by harvest-now-decrypt-later, "
   "and which is not.",
   "<b>Inventory every use of public-key cryptography</b> in a system you "
   "operate.",
   "<b>Measure ML-KEM against X25519</b> for key size, ciphertext size, "
   "and time.",
   "<b>Compute the added bytes per handshake</b> and what that costs on a "
   "constrained link.",
   "<b>Enable a hybrid key exchange</b> somewhere and verify it "
   "negotiated.",
   "<b>Audit one stored format</b> for hardcoded key sizes and missing "
   "algorithm identifiers.",
   "<b>Write your proportionate plan</b>, with what you are explicitly "
   "not doing and why.",
 ],
 "selfcheck": [
   "What does Shor's algorithm break, and what does Grover's do?",
   "Why is this a public-key problem rather than a cryptography "
   "problem?",
   "Which primitives need nothing at all?",
   "State the harvest-now-decrypt-later argument and what it makes this "
   "into.",
   "What is the honest position on timing?",
   "Why is key exchange more urgent than signatures?",
   "Name the standardised schemes and state their cost.",
   "Why deploy hybrid rather than replacing?",
   "Give the four steps of a proportionate response.",
   "Give five things not to do.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Claiming Cryptographic Security Honestly",
 "subtitle": "Which properties, against whom, assuming what.",
 "question": "What does “it is encrypted” actually tell anyone?",
 "outcomes": [
     "State a cryptographic claim completely.",
     "Identify the standard overclaims.",
     "Explain what a security proof does and does not "
     "establish.",
     "Place this course relative to CSCE 701 and CSCE 713.",
     "State the course's rule in your own words.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The complete claim",
   "blurb": "Four components, all required."},

  {"t": "callout", "title": "A complete claim names the property, the adversary, the assumption, and the scope",
   "kind": "The form to use",
   "body": ["<b>The property:</b> <b>which of Module 01 "
            "§1's four, specifically</b> — "
            "confidentiality, integrity, authentication, freshness. "
            "<b>Not 'secure'.</b>",
            "<b>The adversary:</b> <b>a network observer, a "
            "compromised server, a malicious client, a cloud operator, "
            "an insider</b> — because the answer differs for "
            "each.",
            "<b>The assumption:</b> <b>which hardness assumption, and "
            "what key management is presumed correct</b> "
            "(Module 06 §2, Module 10).",
            "<b>And the scope:</b> <b>which data, at which "
            "points in its lifetime</b> — in transit, at rest, in "
            "use, in backups, in logs."]},

  {"t": "table", "kicker": "Overclaims", "title": "The standard overclaims, corrected",
   "header": ["Claim", "Correction"],
   "widths": [4.4, 6.6],
   "rows": [
     ["<b>'It is encrypted'</b>", "<b>Which property? Against whom? Keys held where?</b>"],
     ["<b>'Military-grade encryption'</b>", "<b>Meaningless. The primitive was never the weak point</b>"],
     ["<b>'256-bit encryption'</b>", "<b>A key length, not a security property (M03 §1)</b>"],
     ["<b>'End-to-end encrypted'</b>", "<b>Incomplete without the recovery mechanism (M10 §4)</b>"],
     ["<b>'Provably secure'</b>", "<b>Proved relative to an assumption and a model (Part 3)</b>"],
     ["<b>'Quantum-safe'</b>", "<b>Only if deployed, and hybrid is the honest form (M12)</b>"],
     ["<b>'Zero-knowledge'</b>", "<b>A specific technical property, not a marketing synonym</b>"],
   ],
   "footnote": "<b>'256-bit encryption' is the most revealing of "
               "these</b> — it describes a parameter and implies a "
               "guarantee, which is exactly the substitution this module "
               "exists to prevent.",
   "note": "This table is the practically useful artefact."},

  {"t": "section", "label": "Part 2", "title": "Honest claims",
   "blurb": "What the good form looks like."},

  {"t": "bullets", "kicker": "Examples", "title": "Claims you can actually defend",
   "items": [
     "<b>'Message contents are confidential and authenticated "
     "against a network observer, using ChaCha20-Poly1305 with keys "
     "exchanged by X25519, assuming discrete log is hard "
     "classically.'</b>",
     "",
     "<b>'The server can read message contents. It is not "
     "end-to-end encrypted.'</b> <b>Which is an honest "
     "statement of an architecture</b> "
     "(Module 10 §4).",
     "",
     "<b>'Data at rest is encrypted with per-object keys under a "
     "master key in a key service; a compromise of the application "
     "process exposes the objects it decrypts.'</b>",
     "",
     "<b>'Passwords are stored with Argon2id at these parameters, "
     "which resists offline attack at roughly this rate.'</b>",
     "",
     "<b>And: 'we do not protect metadata'</b> — <b>stated "
     "rather than omitted</b> (Module 01 §2).",
   ],
   "footnote": "<b>Every one of these is longer than the overclaim it "
               "replaces, and every one is checkable</b> — which is "
               "the trade this module is asking you to make."},

  {"t": "section", "label": "Part 3", "title": "What a proof means",
   "blurb": "And what it does not cover."},

  {"t": "callout", "title": "A security proof is a reduction, and it is only as good as its assumptions and its model",
   "kind": "Stating it accurately",
   "body": ["<b>What it establishes:</b> <b>if an adversary breaks "
            "this scheme, then it solves the underlying hard "
            "problem</b> — so the scheme is at least as hard as the "
            "problem.",
            "<b>Which is genuinely valuable</b> — it rules out "
            "entire classes of attack and replaces 'nobody has broken "
            "it' with a structural argument.",
            "<b>What it does not cover:</b> <b>the implementation "
            "(Module 11), the key management (Module 10), side channels, "
            "the protocol it is embedded in, and anything outside the "
            "model.</b>",
            "<b>So 'provably secure' is not a claim about a "
            "system</b> — <b>it is a claim about a scheme in a "
            "model, and nearly every real break happened outside the "
            "model.</b>"]},

  {"t": "section", "label": "Part 4", "title": "The semester",
   "blurb": "Three courses, and where this one sits."},

  {"t": "table", "kicker": "Semester 9", "title": "The three courses, by failure source",
   "header": ["Course", "Covers", "Honest summary"],
   "widths": [2.3, 3.8, 5.4],
   "rows": [
     ["<b>CSCE 701</b>", "<b>Systems, operations, people</b>", "<b>Where the incidents are</b>"],
     ["<b>CSCE 711</b>", "<b>Primitives and their correct use</b>", "<b>The part that works — misused</b>"],
     ["<b>CSCE 713</b>", "<b>Code defects</b>", "<b>Where the severe bugs are</b>"],
   ],
   "footnote": "<b>This course's honest summary is the "
               "uncomfortable one:</b> the mathematics is sound, and "
               "the failures are yours — nonces, keys, error "
               "handling, and composition.",
   "note": "Framing 711 as 'the part that works, misused' is the "
           "course's own thesis."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can state what each primitive provides, choose "
            "correctly from a library, and recognise the compositions "
            "that are unsound</b> — which is the practical skill, "
            "and it transfers to systems you did not design.",
            "<b>You can design a key lifecycle, specify envelope "
            "encryption, and execute a rotation</b> — <b>which is "
            "the subject that actually decides whether the cryptography "
            "helps.</b>",
            "<b>You can find the implementation hazards:</b> <b>a "
            "non-constant-time comparison, a reused nonce, a "
            "distinguishable error, a key with two purposes.</b>",
            "<b>And the closing rule is the program's:</b> <b>state "
            "what you measured, state what you assumed, and never claim "
            "more than you established.</b> <b>Here it means naming the "
            "property, the adversary, and the assumption</b> — "
            "because <b>'it is encrypted' assumes all three and states "
            "none.</b>"]},
 ],
 "takeaways": [
   "A complete claim names the property, the adversary, the assumption, "
   "and the scope — and 'secure' names none of them.",
   "'256-bit encryption' describes a parameter and implies a guarantee, "
   "which is exactly the substitution to avoid.",
   "'End-to-end encrypted' is incomplete without the recovery mechanism, "
   "which is the weakest point of such a design.",
   "A security proof is a reduction: it shows breaking the scheme solves a "
   "hard problem, relative to an assumption and inside a model.",
   "Nearly every real break happened outside the model — in the "
   "implementation, the key management, or the surrounding protocol.",
   "This course's honest summary is that the mathematics is sound and the "
   "failures are yours: nonces, keys, error handling, and composition.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The complete claim"),
  ("callout", "A complete claim names the property, the adversary, the "
              "assumption, and the scope",
   ["<b>The property:</b> <b>which of Module 01 &sect;1's four, "
    "specifically</b> — confidentiality, integrity, authentication, "
    "or freshness, named individually because a system may provide some "
    "and not others. <b>Not 'secure', which names none of them.</b>",
    "<b>The adversary:</b> <b>a passive network observer, an active "
    "network attacker, a compromised server, a malicious client, the "
    "cloud operator, a legal process, an insider</b> — <b>because "
    "the answer is genuinely different for each</b>, and a claim that "
    "does not say which is not falsifiable.",
    "<b>The assumption:</b> <b>which hardness assumption the scheme "
    "rests on, and what key management is being presumed correct</b> "
    "(Module 06 &sect;2, Module 10) — the second being the "
    "one always left implicit and most often wrong.",
    "<b>And the scope:</b> <b>which data, at which points in its "
    "lifetime</b> — in transit, at rest, in use in process memory, "
    "in backups, in logs, in the analytics pipeline. <b>'Encrypted at "
    "rest' says nothing about the other five.</b>"]),
  ("table", ["The claim", "The correction"],
   [["<b>'It is encrypted.'</b>",
     "<b>Which property? Against which adversary? With the keys held "
     "where and readable by whom?</b> The sentence conveys almost "
     "nothing."],
    ["<b>'Military-grade encryption.'</b>",
     "<b>Meaningless as a phrase, and misdirected as a claim</b> — "
     "<b>the primitive was never the weak point</b> (Module 01 "
     "&sect;4)."],
    ["<b>'256-bit encryption.'</b>",
     "<b>A key length, not a security property</b> (Module 03 "
     "&sect;1) — see the note."],
    ["<b>'End-to-end encrypted.'</b>",
     "<b>Incomplete without the recovery mechanism</b>, which is the "
     "weakest point of the design (Module 10 &sect;4)."],
    ["<b>'Provably secure.'</b>",
     "<b>Proved relative to a stated assumption, inside a stated "
     "model</b> — and almost every real break was outside the model "
     "(&sect;3)."],
    ["<b>'Quantum-safe.'</b>",
     "<b>Only if actually deployed, and hybrid is the honest form</b> "
     "(Module 12 &sect;4)."],
    ["<b>'Zero-knowledge.'</b>",
     "<b>A specific technical property with a formal definition, not a "
     "marketing synonym for 'we cannot see your data'.</b>"]],
   [0.34, 0.66]),
  ("p", "<b>'256-bit encryption' is the most revealing of these.</b> "
        "<b>It describes a parameter and implies a guarantee</b> — "
        "and it is perfectly compatible with ECB mode, a hardcoded key, no "
        "authentication, and a nonce that repeats. <b>Which is exactly "
        "the substitution this module exists to prevent:</b> quoting a "
        "number that sounds large in place of stating a property that can "
        "be checked."),

  ("h1", "2 &nbsp; Claims you can defend"),
  ("ul", ["<b>'Message contents are confidential and authenticated "
          "against a network observer, using ChaCha20-Poly1305 with keys "
          "exchanged by X25519, assuming the discrete logarithm problem is "
          "hard against a classical adversary.'</b> <b>Property, "
          "adversary, construction, assumption.</b>",
          "<b>'The server can read message contents. This is not an "
          "end-to-end encrypted system.'</b> <b>Which is an honest "
          "statement of an architecture rather than an admission</b> "
          "(Module 10 &sect;4) — and is far more useful to a user "
          "than a vague reassurance.",
          "<b>'Data at rest is encrypted with per-object data keys "
          "under a master key held in a key service. A compromise of the "
          "application process exposes the objects that process "
          "decrypts.'</b> <b>Scope, construction, and blast "
          "radius.</b>",
          "<b>'Passwords are stored using Argon2id at these specific "
          "parameters, which resists offline attack at approximately this "
          "rate on current hardware.'</b> <b>A measured capability "
          "rather than an assertion</b> (Module 09 &sect;2).",
          "<b>And: 'we do not protect metadata — who communicates "
          "with whom, when, and how much is visible to us and to a "
          "network observer.'</b> <b>Stated rather than "
          "omitted</b> (Module 01 &sect;2). <b>Every one of these is "
          "longer than the overclaim it replaces, and every one is "
          "checkable by somebody else</b> — which is precisely the "
          "trade this module is asking you to make."]),

  ("break",),
  ("h1", "3 &nbsp; What a proof means"),
  ("callout", "A security proof is a reduction, and it is only as good as "
              "its assumptions and its model",
   ["<b>What it establishes:</b> <b>if an adversary breaks this "
    "scheme, then that adversary can be used to solve the underlying hard "
    "problem</b> — so the scheme is at least as hard to break as the "
    "problem is to solve. <b>A reduction, exactly in CSCE 637's "
    "sense.</b>",
    "<b>Which is genuinely valuable and should not be "
    "undersold:</b> <b>it rules out entire classes of attack at once, "
    "and replaces 'nobody has managed to break it yet' with a structural "
    "argument that will remain true</b> as long as the assumption "
    "holds.",
    "<b>What it does not cover:</b> <b>the implementation "
    "(Module 11), the key management (Module 10), side channels of "
    "any kind, the protocol the scheme is embedded in, the error handling "
    "around it, and anything at all outside the model's "
    "definition.</b> <b>A proof in the random oracle model assumes "
    "something no real hash function is.</b>",
    "<b>So 'provably secure' is not a claim about a system.</b> <b>It "
    "is a claim about a scheme inside a model — and nearly every "
    "real-world break happened outside the model</b>, in exactly the "
    "places the proof said nothing about. <b>Which is Module 01 "
    "&sect;4's historical record and this module's thesis, meeting.</b>"]),

  ("h1", "4 &nbsp; The semester, and where this leaves you"),
  ("table", ["Course", "What it covers", "The honest summary"],
   [["<b>CSCE 701</b>",
     "<b>Systems, operations, architecture, and people.</b>",
     "<b>Where the incidents are</b> — credentials, "
     "misconfiguration, missing authorisation, unpatched dependencies."],
    ["<b>CSCE 711 (this one)</b>",
     "<b>The primitives, and their correct use and composition.</b>",
     "<b>The part that works — misused</b>. See the note."],
    ["<b>CSCE 713</b>",
     "<b>Finding and preventing defects in code.</b>",
     "<b>Where the severe bugs are</b>, and where CSCE 627's "
     "undecidability bounds what tooling can promise."]],
   [0.22, 0.34, 0.44]),
  ("p", "<b>This course's honest summary is the uncomfortable one:</b> "
        "<b>the mathematics is sound, and the failures are yours</b> "
        "— reused nonces, keys in repositories, distinguishable "
        "errors, unauthenticated encryption, keys serving two purposes, and "
        "comparisons that are not constant-time. <b>Which is why this "
        "course spent more time on Modules 10 and 11 than on the "
        "primitives themselves</b>, and why Module 01 &sect;4's rule was "
        "stated at the beginning rather than derived at the end."),
  ("callout", "Where this course leaves you",
   ["<b>You can state what each primitive provides, choose correctly "
    "from a reviewed library, and recognise the compositions that are "
    "unsound</b> — which is the practical skill, and <b>it transfers "
    "to systems you did not design and cannot rewrite</b>, which is most "
    "of them.",
    "<b>You can design a key lifecycle, specify envelope encryption, "
    "and execute a rotation you have actually tested</b> — <b>which "
    "is the subject that genuinely decides whether any of the "
    "cryptography helps</b>, and which is the half most courses leave "
    "out.",
    "<b>You can find the implementation hazards:</b> <b>a "
    "non-constant-time comparison, a nonce whose uniqueness does not "
    "survive a restart, a distinguishable decryption error, a key serving "
    "two purposes, a parser running before verification.</b> <b>Five "
    "checks, mechanically applicable.</b>",
    "<b>And the closing rule is the program's, unchanged across "
    "twenty-six courses:</b> <b>state what you measured, state what you "
    "assumed, and never claim more than you established.</b> <b>In "
    "cryptography it means naming the property, the adversary, and the "
    "assumption</b> — because <b>'it is encrypted' assumes all three "
    "and states none of them</b>, and the whole of &sect;1's table is "
    "what happens when that substitution goes unchallenged."]),
 ],
 "resources": [
   ("Boneh & Shoup, the introduction and chapter 2 (free)",
    "https://toc.cryptobook.us/",
    "<b>&sect;3's account of what a proof establishes</b>, from the "
    "people who write them — and notably careful about the "
    "limits."),
   ("Koblitz & Menezes &mdash; Another Look at “Provable "
    "Security” (free)",
    "https://eprint.iacr.org/2004/152",
    "<b>&sect;3's caveats argued forcefully</b> — a useful "
    "corrective, and contested, which is itself instructive."),
   ("Green &mdash; A Few Thoughts on Cryptographic Engineering (free)",
    "https://blog.cryptographyengineering.com/",
    "<b>&sect;1 and &sect;2 in practice</b> — consistently good at "
    "separating what a system claims from what it provides."),
   ("Anderson &mdash; Security Engineering, the cryptography chapter "
    "(free PDF)",
    "https://www.cl.cam.ac.uk/~rja14/book.html",
    "<b>&sect;4's placement of this subject within security as a "
    "whole</b>, and consistent with this course's ordering."),
 ],
 "exercises": [
   "<b>Take a cryptographic claim made publicly</b> by a product you use "
   "and assess it against §1's table.",
   "<b>Rewrite it</b> in the four-component form.",
   "<b>Write the complete claim for your own system</b> — property, "
   "adversary, assumption, scope.",
   "<b>State what you do not protect</b>, explicitly.",
   "<b>Find a 'provably secure' claim</b> and identify what its model "
   "excludes.",
   "<b>List the places a break could occur outside the model</b> for one "
   "scheme you use.",
   "<b>Compare your actual effort allocation</b> against the three "
   "courses' failure sources.",
   "<b>Revisit Module 01's last exercise</b> and compare what you wrote "
   "then.",
   "<b>Run Module 11's five checks</b> once more, on your own project.",
   "<b>Project 2 is now due.</b> Submit the requirement, the primitive "
   "choices with justification, the complete key lifecycle, the executed "
   "rotation, and the explicit list of properties you are not "
   "providing.",
 ],
 "selfcheck": [
   "Name the four components of a complete claim.",
   "Why does the adversary have to be named?",
   "Give seven overclaims and the correction to each.",
   "Why is '256-bit encryption' the most revealing?",
   "Give three claims you could actually defend.",
   "What does a security proof establish, and as a what?",
   "What does a proof not cover — give five things.",
   "Why is 'provably secure' not a claim about a system?",
   "How do the three security courses divide?",
   "In this course, what does 'never claim more than you established' "
   "mean?",
 ],
},

]
