# -*- coding: utf-8 -*-
"""CSCE 701 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Authentication",
 "subtitle": "Proving who you are, and the ways it actually fails.",
 "question": "How do you establish identity, and where does it go "
             "wrong?",
 "outcomes": [
     "Explain the three factors and what each resists.",
     "Explain password storage correctly and the reasoning behind "
     "it.",
     "Explain why the old password rules were wrong.",
     "Compare second factors by what attack each stops.",
     "Design account recovery, which is the hard part.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The factors",
   "blurb": "And what each actually resists."},

  {"t": "table", "kicker": "Factors", "title": "The three factors, by what they stop",
   "header": ["Factor", "Resists", "Fails to"],
   "widths": [2.6, 4.2, 5.2],
   "rows": [
     ["<b>Something you know</b>", "<b>Casual impersonation</b>", "<b>Phishing, reuse, database breach, keylogging</b>"],
     ["<b>Something you have</b>", "<b>Remote attacks entirely, if bound to the origin</b>", "<b>Theft, and SMS-based versions fail to SIM swap</b>"],
     ["<b>Something you are</b>", "<b>Casual access to a device</b>", "<b>Cannot be revoked; usually a local unlock, not authentication</b>"],
   ],
   "footnote": "<b>The biometric row is the one people get wrong:</b> "
               "<b>a fingerprint is a convenient local unlock and not a "
               "secret</b>, because you cannot change it and you leave "
               "copies everywhere.",
   "note": "The irrevocability of biometrics is the point to make."},

  {"t": "callout", "title": "Phishing resistance is the property that matters",
   "kind": "The sorting criterion for second factors",
   "body": ["<b>A second factor that the user can read out or type in "
            "can be relayed by a phishing site</b> — which asks for "
            "it and forwards it immediately.",
            "<b>So SMS codes, authenticator app codes, and push "
            "approvals are all phishable</b>, and real-time relay "
            "phishing kits are commodity tooling.",
            "<b>A factor cryptographically bound to the origin is "
            "not.</b> <b>WebAuthn and FIDO2 keys sign a challenge "
            "including the origin</b>, so a signature produced for the "
            "phishing site is useless at the real one.",
            "<b>Which is the single most important distinction in "
            "authentication</b> — <b>'two-factor' is not a security "
            "level, and origin-bound against relayable is the line that "
            "matters.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Password storage",
   "blurb": "The part with a correct answer."},

  {"t": "code", "kicker": "Password storage", "title": "What to do, and why each part is there",
   "lang": "text", "code": """
  STORE: a salted hash from a MEMORY-HARD algorithm.
      Argon2id, scrypt, or bcrypt. Not SHA-256.

  WHY EACH PIECE:
    HASH      so a database read does not yield passwords
    SALT      unique per user, so one table cannot crack
              many accounts at once, and identical
              passwords do not look identical
    SLOW      so guessing costs the attacker real time.
              SHA-256 is FAST, which is exactly wrong here:
              a GPU computes billions per second.
    MEMORY-   so specialised hardware (GPU, ASIC) loses its
    HARD      advantage, because memory bandwidth does not
              scale the way arithmetic does

  AND: a PEPPER (a secret key, stored separately from the
  database, mixed into the hash) means a database dump
  alone is not crackable at all. Underused, and cheap.

  WHAT NOT TO DO
    your own scheme, ever
    encryption instead of hashing -- a decryptable store
        means someone can decrypt it
    a single global salt, which is not a salt
    and truncating or normalising the password before
        hashing, which quietly reduces the space
""",
   "caption": "<b>Slowness is the feature</b> — which is the one "
              "place in this program where a fast algorithm is the wrong "
              "choice.",
   "note": "The 'SHA-256 is wrong because it is fast' point lands well."},

  {"t": "callout", "title": "The old password rules were wrong, and the evidence changed them",
   "kind": "A rare case of guidance being corrected",
   "body": ["<b>Complexity requirements and forced rotation produced "
            "predictable passwords</b> — <code>Password1!</code> "
            "becoming <code>Password2!</code> — and <b>drove reuse "
            "and writing-down.</b>",
            "<b>So the current guidance reverses them:</b> <b>long "
            "minimum, no composition rules, no forced expiry, and a "
            "check against known-breached password lists.</b>",
            "<b>Which is a human-factors result rather than a "
            "cryptographic one</b> (Module 11) — <b>the old rules "
            "maximised theoretical entropy and minimised actual "
            "entropy</b>, because people are predictable under "
            "constraint.",
            "<b>And it is worth knowing as an example of security "
            "guidance being corrected by measurement</b> — <b>which "
            "happens rarely and should happen more</b> "
            "(Module 12)."]},

  {"t": "section", "label": "Part 3", "title": "Sessions",
   "blurb": "Authentication happens once; authorisation happens "
            "constantly."},

  {"t": "bullets", "kicker": "Sessions", "title": "What a session must get right",
   "items": [
     "<b>A high-entropy, unpredictable identifier</b>, from a "
     "cryptographic source — <b>CSCE 658 §13 §2's "
     "weak-generator failure, in its most common form.</b>",
     "",
     "<b>Transmitted and stored safely:</b> <code>Secure</code>, "
     "<code>HttpOnly</code>, and <code>SameSite</code> on the cookie "
     "(Module 06 §3).",
     "",
     "<b>Rotated on privilege change</b> — <b>failing to issue a "
     "new identifier at login enables session fixation.</b>",
     "",
     "<b>Revocable server-side.</b> <b>A stateless token that cannot "
     "be revoked is a credential with a fixed lifetime</b>, which is a "
     "real trade and not a free one.",
     "",
     "<b>And bounded in lifetime</b>, with idle and absolute "
     "timeouts chosen from the threat model rather than from habit.",
   ],
   "footnote": "<b>The revocation point is the one that bites:</b> "
               "<b>a self-contained token is convenient and cannot be "
               "withdrawn</b>, so either keep the lifetime short or keep "
               "server-side state."},

  {"t": "section", "label": "Part 4", "title": "Recovery",
   "blurb": "The hardest part, and the usual way in."},

  {"t": "callout", "title": "Account recovery is the weakest link in most authentication systems",
   "kind": "And it is where attacks go",
   "body": ["<b>Strong authentication with weak recovery is weak "
            "authentication</b> — <b>the attacker simply uses the "
            "recovery path</b>, which is the whole point of "
            "Module 01's weakest-link observation.",
            "<b>And the classic failures are all recovery failures:</b> "
            "<b>security questions whose answers are public, SMS reset "
            "defeated by SIM swap, and support staff who can be "
            "socially engineered into a reset.</b>",
            "<b>So design it deliberately:</b> <b>multiple recovery "
            "factors, a delay with notification to the existing contact, "
            "and a documented support procedure that cannot be talked "
            "around.</b>",
            "<b>And accept that it is a trade against lockout.</b> "
            "<b>Stronger recovery means more users permanently locked "
            "out</b>, which is a real cost — <b>and the right point "
            "depends on what the account controls.</b>"]},

  {"t": "bullets", "kicker": "Practice", "title": "Authentication, in priority order",
   "items": [
     "<b>1 · Use a well-maintained identity provider or "
     "library.</b> <b>Do not implement authentication yourself</b> "
     "— the failure modes are numerous and known.",
     "",
     "<b>2 · Offer origin-bound second factors</b> (WebAuthn) "
     "<b>and prefer them in the flow</b> (Part 1).",
     "",
     "<b>3 · Store passwords correctly</b> (Part 2) <b>and check "
     "against breached lists.</b>",
     "",
     "<b>4 · Rate-limit and monitor</b> — credential "
     "stuffing is the most common attack and it is detectable "
     "(Module 09).",
     "",
     "<b>5 · And design recovery as carefully as login</b>, "
     "because that is where the attack will go.",
   ],
   "footnote": "<b>Credential stuffing is the attack to design "
               "against</b> — it uses passwords breached elsewhere, "
               "which is why the breached-list check and the "
               "origin-bound factor matter more than password "
               "complexity."},
 ],
 "takeaways": [
   "A biometric is a convenient local unlock rather than a secret, because "
   "it cannot be revoked and you leave copies everywhere.",
   "Phishing resistance is the property that sorts second factors: "
   "anything a user can read out can be relayed, and origin-bound keys "
   "cannot.",
   "Store passwords with a salted memory-hard hash, and slowness is the "
   "feature — SHA-256 is wrong precisely because it is fast.",
   "The old complexity-and-rotation rules maximised theoretical entropy "
   "and minimised actual entropy, and the guidance was corrected by "
   "measurement.",
   "A stateless token that cannot be revoked is a credential with a fixed "
   "lifetime, which is a real trade.",
   "Strong authentication with weak recovery is weak authentication, and "
   "recovery is where attacks go.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The factors"),
  ("table", ["Factor", "What it resists", "What it fails against"],
   [["<b>Something you know</b> (a password, a PIN)",
     "<b>Casual impersonation by someone who does not know it.</b>",
     "<b>Phishing, reuse across sites, database breach, keylogging, and "
     "shoulder-surfing.</b> Every one of which happens at scale."],
    ["<b>Something you have</b> (a security key, a device)",
     "<b>Remote attacks entirely, if the factor is cryptographically "
     "bound to the origin</b> — see the callout.",
     "<b>Physical theft, and the SMS-based version fails against SIM "
     "swapping</b>, which is a routine attack rather than an exotic "
     "one."],
    ["<b>Something you are</b> (a fingerprint, a face)",
     "<b>Casual access to an already-unlocked device.</b>",
     "<b>It cannot be revoked, and it is usually a local unlock rather "
     "than authentication to a remote service</b> — the device "
     "authenticates, and the biometric unlocks the device's key."]],
   [0.26, 0.34, 0.40]),
  ("p", "<b>The biometric row is the one that is most often "
        "misunderstood:</b> <b>a fingerprint is a convenient local unlock "
        "and not a secret</b>, because <b>you cannot change it after a "
        "compromise and you leave copies of it on every surface you "
        "touch.</b> <b>Which means it is a reasonable way to unlock a "
        "key stored in a device's secure element, and a poor thing to send "
        "to a server.</b> <b>The distinction between 'unlocks a local "
        "credential' and 'is a credential' is the one to hold.</b>"),
  ("callout", "Phishing resistance is the property that matters",
   ["<b>A second factor that the user can read out, type in, or approve "
    "can be relayed by a phishing site</b> — which asks the user for "
    "it and forwards it to the real service within seconds.",
    "<b>So SMS codes, authenticator app codes, and push approvals are "
    "all phishable</b>, and <b>real-time relay phishing toolkits are "
    "commodity</b> rather than bespoke — which means the attack is "
    "available to any adversary, not only a capable one.",
    "<b>A factor cryptographically bound to the origin is not "
    "phishable.</b> <b>WebAuthn and FIDO2 security keys sign a challenge "
    "that includes the origin the browser is actually talking to</b>, "
    "<b>so a signature produced for the phishing site is cryptographically "
    "useless at the real one</b> — the relay has nothing to relay.",
    "<b>Which is the single most important distinction in "
    "authentication.</b> <b>'Two-factor authentication' is not a "
    "security level</b>, and <b>origin-bound against relayable is the "
    "line that actually matters</b> — an account with SMS second "
    "factor and an account with a hardware key are protected against "
    "different adversaries, and only one of them is protected against the "
    "common one."]),

  ("h1", "2 &nbsp; Password storage"),
  ("code", """STORE: a salted hash produced by a MEMORY-HARD algorithm.
    Argon2id, scrypt, or bcrypt. NOT SHA-256.

WHY EACH PIECE IS THERE:
  HASH          so that reading the database does not yield
                the passwords themselves
  SALT          unique per user, so that one precomputed
                table cannot crack many accounts at once,
                and so that two users with the same
                password do not have the same stored value
  SLOW          so that guessing costs the attacker real
                time. SHA-256 is FAST, which is exactly
                wrong here: a GPU computes billions of
                SHA-256 hashes per second.
  MEMORY-HARD   so that specialised hardware (GPUs, FPGAs,
                ASICs) loses its advantage, because memory
                bandwidth does not scale the way raw
                arithmetic does

AND: a PEPPER -- a secret key held separately from the
database and mixed into the hash -- means that a database
dump ALONE is not crackable at all. Underused, and cheap.

WHAT NOT TO DO
  your own scheme, ever
  encryption instead of hashing -- a decryptable store
      means that someone, somewhere, can decrypt it
  a single global salt, which is not a salt
  and truncating or case-normalising the password before
      hashing, which quietly shrinks the search space"""),
  ("callout", "The old password rules were wrong, and the evidence changed "
              "them",
   ["<b>Composition requirements (one uppercase, one digit, one symbol) "
    "and forced periodic rotation produced predictable passwords</b> "
    "— <code>Password1!</code> becoming <code>Password2!</code> at "
    "the next rotation — and <b>drove reuse across sites and "
    "writing passwords down.</b>",
    "<b>So the current guidance reverses them:</b> <b>a long minimum "
    "length, no composition rules, no forced expiry without evidence of "
    "compromise, and a check of the proposed password against lists of "
    "known-breached passwords.</b> <b>NIST SP 800-63B says this "
    "explicitly.</b>",
    "<b>Which is a human-factors result rather than a cryptographic "
    "one</b> (Module 11) — <b>the old rules maximised theoretical "
    "entropy and minimised actual entropy</b>, because <b>people are "
    "highly predictable when constrained</b>, and the constraint "
    "collapsed the distribution rather than widening it.",
    "<b>And it is worth knowing as an example of security guidance being "
    "corrected by measurement</b> — <b>which happens rarely and "
    "should happen far more often</b> (Module 12's measurement "
    "problem). <b>The rules persisted for two decades on the strength of "
    "an argument that was never tested.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Sessions"),
  ("ul", ["<b>A high-entropy, unpredictable session identifier</b>, "
          "generated from a cryptographic random source — which is "
          "<b>CSCE 658 Module 13 &sect;2's weak-generator failure "
          "in its single most common real-world form</b>, and it has "
          "caused account-takeover vulnerabilities repeatedly.",
          "<b>Transmitted and stored safely:</b> the "
          "<code>Secure</code> flag so it is never sent over plaintext, "
          "<code>HttpOnly</code> so script cannot read it, and "
          "<code>SameSite</code> to limit cross-site submission "
          "(Module 06 &sect;3).",
          "<b>Rotated on any privilege change.</b> <b>Failing to issue "
          "a fresh identifier at login enables session fixation</b> "
          "— an attacker sets a known session identifier in the "
          "victim's browser, the victim logs in, and the attacker now "
          "holds an authenticated session.",
          "<b>Revocable server-side.</b> <b>A self-contained stateless "
          "token that cannot be revoked is a credential with a fixed "
          "lifetime</b>, which is <b>a real trade and not a free "
          "one</b> — convenient to validate, and impossible to "
          "withdraw when an account is compromised or an employee leaves. "
          "<b>So either keep the lifetime short or keep server-side "
          "state</b>, and decide which deliberately.",
          "<b>And bounded in lifetime</b>, with idle and absolute "
          "timeouts chosen from the threat model (a banking session and a "
          "news site's session are not the same problem) rather than from "
          "habit or from a framework default."]),

  ("h1", "4 &nbsp; Recovery"),
  ("callout", "Account recovery is the weakest link in most authentication "
              "systems",
   ["<b>Strong authentication with weak recovery is weak "
    "authentication</b> — <b>the attacker simply uses the recovery "
    "path instead of the login path</b>, which is precisely Module 01 "
    "&sect;1's weakest-link observation applied to the most commonly "
    "neglected component.",
    "<b>And the classic high-profile account takeovers are almost all "
    "recovery failures:</b> <b>security questions whose answers are "
    "public record or guessable, SMS-based reset defeated by SIM swapping, "
    "email-based reset where the email account was the weaker one, and "
    "support staff socially engineered into performing a manual "
    "reset.</b>",
    "<b>So design it deliberately rather than as an afterthought:</b> "
    "<b>require multiple recovery factors, impose a delay with "
    "notification to the existing contact addresses (so the legitimate "
    "owner can intervene), and give support staff a documented procedure "
    "they cannot be talked around.</b> <b>The notification-and-delay "
    "combination is the cheapest effective control.</b>",
    "<b>And accept that it is a genuine trade against lockout.</b> "
    "<b>Stronger recovery means more legitimate users permanently locked "
    "out of their accounts</b>, which is a real and sometimes severe cost "
    "— <b>and the right point on that trade depends entirely on what "
    "the account controls.</b> A cryptocurrency wallet and a recipe site "
    "should not make the same choice."]),
  ("ul", ["<b>1 &middot; Use a well-maintained identity provider or "
          "library.</b> <b>Do not implement authentication yourself</b> "
          "— the failure modes are numerous, known, and subtle, and "
          "there is no credit for a bespoke implementation.",
          "<b>2 &middot; Offer origin-bound second factors</b> "
          "(WebAuthn or passkeys) <b>and prefer them in the "
          "flow</b> — offering them and defaulting to SMS leaves "
          "the phishable path available (&sect;1).",
          "<b>3 &middot; Store passwords correctly</b> (&sect;2) "
          "<b>and check proposed passwords against breached-password "
          "lists</b>, which addresses the actual attack better than any "
          "composition rule.",
          "<b>4 &middot; Rate-limit and monitor.</b> <b>Credential "
          "stuffing is the most common attack against authentication and "
          "it is highly detectable</b> — many accounts, one source, "
          "high failure rate (Module 09).",
          "<b>5 &middot; And design recovery as carefully as you design "
          "login</b>, because that is where the attack will go once login "
          "is hard. <b>Credential stuffing is the attack to design "
          "against</b> — it uses passwords breached elsewhere, which "
          "is why the breached-list check and the origin-bound factor "
          "matter far more than password complexity rules ever did."]),
 ],
 "resources": [
   ("NIST SP 800-63B &mdash; Digital Identity Guidelines, "
    "Authentication (free)",
    "https://pages.nist.gov/800-63-3/sp800-63b.html",
    "<b>&sect;2's current guidance</b>, including the reversal of the "
    "composition and rotation rules, with the reasoning."),
   ("OWASP &mdash; Authentication, Password Storage, and Session "
    "Management Cheat Sheets (free)",
    "https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html",
    "<b>The working reference for every section of this module</b>, kept "
    "current."),
   ("The WebAuthn specification and passkeys documentation (free)",
    "https://www.w3.org/TR/webauthn-2/",
    "<b>&sect;1's origin-bound factor</b> — and the origin-binding "
    "mechanism is worth reading, because it is what makes the phishing "
    "resistance work."),
   ("Bonneau et al. &mdash; The Quest to Replace Passwords (free)",
    "https://www.cl.cam.ac.uk/~fms27/papers/2012-BonneauHerOorSta-password--oakland.pdf",
    "<b>A systematic comparison of authentication schemes on usability, "
    "deployability, and security</b> — and the framework explains why "
    "passwords persisted."),
 ],
 "exercises": [
   "<b>Classify the second factors</b> offered by five services you use "
   "as origin-bound or relayable.",
   "<b>Set up a hardware security key or passkey</b> on an account, and "
   "note the friction.",
   "<b>Hash a password with SHA-256 and with Argon2id</b> and compare the "
   "time per hash.",
   "<b>Estimate how many guesses per second</b> each permits on a GPU, "
   "and what that means for a weak password.",
   "<b>Implement salted memory-hard password storage</b> correctly, and "
   "then add a pepper.",
   "<b>Check a password list against a breached-password service</b> using "
   "its k-anonymity API.",
   "<b>Inspect the session cookie flags</b> on five sites and report which "
   "are missing.",
   "<b>Test whether a service rotates the session identifier at "
   "login</b> — on your own account.",
   "<b>Map the recovery paths</b> for your own most important account, and "
   "identify the weakest.",
   "<b>Design a recovery flow</b> for a system of yours, with the "
   "lockout trade stated explicitly.",
 ],
 "selfcheck": [
   "Name the three factors and what each resists and fails against.",
   "Why is a biometric not a secret?",
   "What property sorts second factors, and why is 'two-factor' not a "
   "security level?",
   "Give the four components of correct password storage and why each is "
   "there.",
   "Why is SHA-256 the wrong choice, and what is a pepper?",
   "Why were the old password rules wrong, and what replaced them?",
   "Name five requirements of a session, and the trade in stateless "
   "tokens.",
   "Why is recovery the weakest link, and what are the classic "
   "failures?",
   "What trade does stronger recovery make?",
   "Give the five-step priority order, and name the attack it is "
   "designed against.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Authorisation",
 "subtitle": "Deciding what an authenticated principal may do.",
 "question": "Who is allowed to do what, and how do you get that "
             "consistently right?",
 "outcomes": [
     "Distinguish authentication from authorisation precisely.",
     "Compare the access control models and choose one.",
     "Explain the confused deputy and the classes it generates.",
     "Explain why authorisation must be centralised and enforced "
     "server-side.",
     "Review an authorisation design for the standard failures.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The distinction",
   "blurb": "And why conflating them is a bug class."},

  {"t": "callout", "title": "Authentication happens once; authorisation happens on every request",
   "kind": "The distinction, and its consequence",
   "body": ["<b>Authentication establishes <i>who</i>. Authorisation "
            "decides <i>whether this principal may do this, to this "
            "object, now</i>.</b>",
            "<b>And the asymmetry in frequency is the "
            "consequence:</b> <b>authentication is one well-reviewed "
            "code path and authorisation is a decision at every "
            "endpoint</b> — so it is where the misses are.",
            "<b>Which is why missing authorisation is consistently "
            "near the top of every vulnerability-class ranking</b>, and "
            "<b>why it is a <i>coverage</i> problem rather than a design "
            "problem</b>.",
            "<b>So the goal is not a clever model but a design where "
            "forgetting the check is impossible</b> — "
            "<b>deny-by-default at a chokepoint, rather than an explicit "
            "check in every handler.</b>"]},

  {"t": "table", "kicker": "Models", "title": "The access control models",
   "header": ["Model", "Decides by", "Trade"],
   "widths": [2.5, 4.1, 5.4],
   "rows": [
     ["<b>ACL</b>", "<b>A list per object</b>", "<b>Precise; hard to audit 'what can Alice do?'</b>"],
     ["<b>RBAC</b>", "<b>Roles held by the principal</b>", "<b>Auditable; roles proliferate</b>"],
     ["<b>ABAC</b>", "<b>Attributes of subject, object, context</b>", "<b>Expressive; hard to reason about</b>"],
     ["<b>Capability</b>", "<b>Possession of an unforgeable token</b>", "<b>No ambient authority; revocation is harder</b>"],
     ["<b>ReBAC</b>", "<b>Relationships in a graph</b>", "<b>Fits sharing models; needs a service</b>"],
   ],
   "footnote": "<b>RBAC is the default and role proliferation is its "
               "characteristic failure</b> — a system with four "
               "hundred roles has an access control list with extra "
               "steps.",
   "note": "The role-proliferation failure is what pushes organisations "
           "to ABAC or ReBAC."},

  {"t": "section", "label": "Part 2", "title": "The confused deputy",
   "blurb": "One bug shape, many names."},

  {"t": "code", "kicker": "Confused deputy", "title": "The pattern 1/2: five classes, one shape",
   "lang": "text", "code": """
  A CONFUSED DEPUTY is a privileged component that acts on
  a request without checking whether the REQUESTER had the
  authority -- using its own authority instead.

  THE SAME SHAPE, UNDER MANY NAMES:

    CSRF             the browser attaches the user's cookie
                     to a request the attacker caused.
                     The server acts on the user's
                     authority. (Module 06)
    SSRF             your server fetches a URL supplied by
                     a user, from inside your network,
                     using its own network position.
    IDOR / missing   the handler looks up object 42 because
    object check     the request said 42, without asking
                     whether this user may see 42.
    PATH TRAVERSAL   the file server opens the path it was
                     given, with its own file permissions.
    SUDO/SETUID bugs the privileged binary acts on
                     attacker-controlled input.
""",
   "caption": "<b>Five names, one structure</b> — and recognising "
              "the shape means recognising five vulnerability classes at "
              "once.",
   "note": "The unification is the teaching value; students otherwise "
           "learn five unrelated acronyms."},

  {"t": "code", "kicker": "Confused deputy", "title": "The pattern 2/2: the fix, and the root cause",
   "lang": "text", "code": """
  THE FIX IS ALWAYS THE SAME SHAPE: the deputy must act on
  the REQUESTER's authority, not its own. Pass the
  authority along (a capability), or check it explicitly
  against the requester's identity.

  AMBIENT AUTHORITY is the underlying cause: the deputy has
  power merely by being itself, rather than by being handed
  it.

  WHICH IS WHY CAPABILITY SYSTEMS ARE STRUCTURALLY
  RESISTANT -- a capability names the object AND carries
  the right to it, so there is no authority to be confused
  about. You cannot ask a capability-based deputy to act on
  an object you were not able to hand it.

  AND IT IS WHY "pass the user's token through" is better
  advice than "add a check here": the check can be
  forgotten at the next call site, and the token cannot.
""",
   "caption": "<b>Ambient authority is the root cause</b>, which is why "
              "passing authority beats adding checks.",
   "note": "The capability argument is the structural answer rather "
           "than the procedural one."},

  {"t": "section", "label": "Part 3", "title": "Enforcement",
   "blurb": "Where the check must live."},

  {"t": "callout", "title": "Authorisation is enforced server-side, at a chokepoint, deny-by-default",
   "kind": "The three non-negotiables",
   "body": ["<b>Server-side, always.</b> <b>A hidden button, a "
            "disabled field, or a client-side role check is a user "
            "interface convenience and not a control</b> — the "
            "request can be made directly.",
            "<b>At a chokepoint.</b> <b>A check in every handler will "
            "be missed in some handler</b>, so put it in middleware, a "
            "policy layer, or the data access layer where it cannot "
            "be skipped.",
            "<b>Deny by default.</b> <b>A new endpoint should be "
            "inaccessible until explicitly permitted</b>, which turns "
            "'forgot the check' from a vulnerability into a bug report "
            "from a confused user.",
            "<b>And object-level, not just endpoint-level.</b> <b>'May "
            "this user call this endpoint' is not 'may this user access "
            "<i>this object</i>'</b> — and the second is the one that "
            "is missed."]},

  {"t": "bullets", "kicker": "Design", "title": "Making the check hard to forget",
   "items": [
     "<b>Scope queries by principal at the data layer.</b> <b>A "
     "query that cannot return another tenant's rows removes the class "
     "entirely</b> — the strongest available fix.",
     "",
     "<b>Use unguessable identifiers</b> as defence in depth, "
     "<b>not as the control</b> — obscurity is not "
     "authorisation (Module 01 §3).",
     "",
     "<b>Centralise the policy</b>, so it can be read, reviewed, and "
     "tested as a single artefact.",
     "",
     "<b>Test authorisation explicitly:</b> <b>for every endpoint, a "
     "test that the wrong user is refused</b> — which is the test "
     "suite nobody writes.",
     "",
     "<b>And log every denial</b>, because <b>a burst of denials is "
     "one of the clearest attack signals you will get</b> "
     "(Module 09).",
   ],
   "footnote": "<b>Scoping at the data layer is the structural fix</b> "
               "— every other item on this list is a way of "
               "catching a mistake, and this one prevents it."},

  {"t": "section", "label": "Part 4", "title": "Reviewing a design",
   "blurb": "The questions that find the failures."},

  {"t": "bullets", "kicker": "Review", "title": "What to ask of an authorisation design",
   "items": [
     "<b>Where is the decision made, and can any path reach the "
     "resource without passing it?</b> <b>Background jobs, admin "
     "tools, and internal APIs are where the second path lives.</b>",
     "",
     "<b>Is it object-level?</b> <b>Find an endpoint that checks the "
     "role and not the object</b> — there is usually one.",
     "",
     "<b>What happens on an error in the policy evaluation?</b> "
     "<b>Fail closed</b> (Module 01 §3).",
     "",
     "<b>How is a revocation propagated, and how fast?</b> <b>A "
     "cached decision is a stale decision</b>, and a departed employee "
     "is the test case.",
     "",
     "<b>And who can change the policy?</b> <b>Authorisation over the "
     "authorisation system is the part that is always "
     "forgotten.</b>",
   ],
   "footnote": "<b>The second-path question finds the most "
               "findings:</b> an application with correct authorisation "
               "and an unauthenticated internal admin endpoint is a "
               "common and severe pattern."},

  {"t": "callout", "title": "Multi-tenancy is the hardest case",
   "kind": "Where this gets genuinely difficult",
   "body": ["<b>In a shared system, every single query must be scoped "
            "to the tenant</b>, and <b>one unscoped query is a "
            "cross-tenant data exposure</b> — which is the most "
            "serious routine failure in software-as-a-service.",
            "<b>So enforce it structurally:</b> <b>row-level security "
            "in the database, a tenant-scoped connection, or an ORM layer "
            "that cannot emit an unscoped query</b> — rather than "
            "discipline.",
            "<b>And test it adversarially:</b> <b>a test suite that "
            "runs every endpoint as tenant A with tenant B's "
            "identifiers</b>, and expects a refusal every time.",
            "<b>Which is the one test suite worth building for its own "
            "sake</b> — <b>it is mechanical to generate, it covers the "
            "highest-severity class, and almost nobody has one.</b>"]},
 ],
 "takeaways": [
   "Authentication is one reviewed code path and authorisation is a "
   "decision at every endpoint, which makes it a coverage problem.",
   "So the goal is a design where forgetting the check is impossible, not "
   "a clever model.",
   "The confused deputy is one shape behind CSRF, SSRF, IDOR, path "
   "traversal, and setuid bugs — and ambient authority is the root "
   "cause.",
   "Authorisation must be server-side, at a chokepoint, deny-by-default, "
   "and object-level rather than endpoint-level.",
   "Scoping queries by principal at the data layer is the structural fix; "
   "everything else catches mistakes rather than preventing them.",
   "Multi-tenancy is the hardest case, and the cross-tenant test suite is "
   "mechanical to generate and almost nobody has one.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The distinction, and the models"),
  ("callout", "Authentication happens once; authorisation happens on every "
              "request",
   ["<b>Authentication establishes <i>who</i> is making the request. "
    "Authorisation decides <i>whether this principal may perform this "
    "action, on this object, now</i>.</b> Four parameters, and the third "
    "is the one that is dropped.",
    "<b>And the asymmetry in frequency is the operative "
    "consequence:</b> <b>authentication is a single, well-reviewed, "
    "heavily-tested code path, and authorisation is a decision that must "
    "be made correctly at every endpoint, in every background job, and in "
    "every internal tool</b> — so it is where the misses are.",
    "<b>Which is why missing or broken authorisation sits consistently "
    "near the top of every vulnerability-class ranking</b> (it is "
    "number one in the current OWASP Top Ten), and <b>why it is "
    "fundamentally a <i>coverage</i> problem rather than a design "
    "problem</b>: the design is usually fine and one handler forgot.",
    "<b>So the goal is not a clever access control model but a design in "
    "which forgetting the check is <i>impossible</i></b> — "
    "<b>deny-by-default enforcement at a chokepoint, rather than an "
    "explicit check written into every handler</b> (&sect;3). <b>That "
    "reframing from 'remember to check' to 'cannot fail to check' is the "
    "main content of this module.</b>"]),
  ("table", ["Model", "Decides by", "The trade"],
   [["<b>Access control lists</b>",
     "<b>A list of permitted principals attached to each object.</b>",
     "<b>Precise and fine-grained; very hard to answer 'what can Alice "
     "do?'</b>, which is the question an auditor asks."],
    ["<b>RBAC (role-based)</b>",
     "<b>Roles held by the principal, with permissions attached to "
     "roles.</b>",
     "<b>Auditable and comprehensible; roles proliferate</b> — see "
     "the note."],
    ["<b>ABAC (attribute-based)</b>",
     "<b>Attributes of the subject, the object, and the context "
     "(time, location, device).</b>",
     "<b>Very expressive; correspondingly hard to reason about and to "
     "test</b>, and a policy nobody understands is not a control."],
    ["<b>Capability-based</b>",
     "<b>Possession of an unforgeable token that designates both the "
     "object and the permitted operation.</b>",
     "<b>No ambient authority, so &sect;2's confused deputy is "
     "structurally prevented</b>; revocation and auditing are harder."],
    ["<b>ReBAC (relationship-based)</b>",
     "<b>Relationships in a graph — 'is a member of a group that "
     "owns the parent folder'.</b>",
     "<b>Fits real sharing models well</b> (it is what Google's Zanzibar "
     "implements); <b>needs a dedicated service</b> to answer queries at "
     "scale."]],
   [0.20, 0.38, 0.42]),
  ("p", "<b>RBAC is the sensible default and role proliferation is its "
        "characteristic failure</b> — <b>a system with four hundred "
        "roles, most held by one person each, has an access control list "
        "with extra steps</b> and none of ACL's precision. <b>Which is "
        "what pushes organisations toward ABAC or ReBAC</b>, and the honest "
        "answer is usually RBAC for coarse decisions plus "
        "relationship-based checks for object-level ones."),

  ("h1", "2 &nbsp; The confused deputy"),
  ("code", """A CONFUSED DEPUTY is a privileged component that acts on a
request without checking whether the REQUESTER had the
authority -- using its own authority instead.

THE SAME SHAPE, UNDER MANY NAMES:

  CSRF              the browser attaches the user's cookie
                    to a request the attacker caused. The
                    server acts on the user's authority.
                    (Module 06 section 3)
  SSRF              your server fetches a URL supplied by a
                    user, from inside your network, using
                    its own network position and identity.
  IDOR / missing    the handler looks up object 42 because
  object check      the request said 42, without ever
                    asking whether THIS user may see 42.
  PATH TRAVERSAL    the file server opens whatever path it
                    was given, with its own file
                    permissions.
  SETUID / SUDO     the privileged binary acts on
  BUGS              attacker-controlled input with root's
                    authority.

THE FIX IS ALWAYS THE SAME SHAPE: the deputy must act on
the REQUESTER's authority, not its own. Either pass the
authority along explicitly (a capability) or check it
against the requester's identity before acting.

AMBIENT AUTHORITY is the underlying cause: the deputy has
power merely by virtue of being itself, rather than by
having been handed it for this request. Which is exactly
why capability systems are structurally resistant."""),
  ("p", "<b>Ambient authority is the root cause</b>, and <b>recognising "
        "the shape means recognising five vulnerability classes at "
        "once</b> rather than learning five unrelated acronyms. <b>It "
        "also tells you what to look for in a code review:</b> any place "
        "where a privileged component takes an identifier, a path, or a "
        "URL from a less-privileged source and acts on it."),

  ("h1", "3 &nbsp; Enforcement"),
  ("callout", "Authorisation is enforced server-side, at a chokepoint, "
              "deny-by-default",
   ["<b>Server-side, always.</b> <b>A hidden button, a disabled form "
    "field, or a client-side role check is a user-interface convenience "
    "and not a control</b> — the request can be constructed and sent "
    "directly, and will be.",
    "<b>At a chokepoint.</b> <b>A check written into every handler will "
    "be omitted from some handler</b>, eventually, by someone in a hurry "
    "— so put it in middleware, a policy decision layer, or the data "
    "access layer, <b>where it cannot be skipped by accident.</b>",
    "<b>Deny by default.</b> <b>A newly added endpoint should be "
    "inaccessible until someone explicitly permits it</b>, which "
    "<b>converts 'forgot the authorisation check' from a security "
    "vulnerability into a bug report from a confused user</b> — a "
    "dramatically better failure mode, and Module 01 &sect;3's "
    "fail-closed principle applied to the development process rather than "
    "to runtime.",
    "<b>And object-level, not merely endpoint-level.</b> <b>'May this "
    "user call this endpoint' is a different question from 'may this user "
    "access <i>this particular object</i>'</b> — and <b>the second "
    "is the one that is missed</b>, because the first is what a route "
    "annotation naturally expresses."]),
  ("ul", ["<b>Scope queries by principal at the data layer.</b> <b>A "
          "query that structurally cannot return another tenant's or "
          "another user's rows removes the entire class</b> — "
          "<b>the strongest available fix</b>, and the only one on this "
          "list that prevents the mistake rather than catching it.",
          "<b>Use unguessable identifiers (UUIDs rather than sequential "
          "integers) as defence in depth</b>, <b>and not as the "
          "control</b> — obscurity is not authorisation "
          "(Module 01 &sect;3's open design), and identifiers leak "
          "through logs, referrers, and shared links.",
          "<b>Centralise the policy</b>, so that it can be read, "
          "reviewed, diffed, and tested as a single artefact rather than "
          "being distributed across a hundred route handlers.",
          "<b>Test authorisation explicitly:</b> <b>for every endpoint, "
          "a test asserting that the <i>wrong</i> user is refused</b> "
          "— <b>which is the test suite nobody writes</b>, because "
          "the positive tests feel like the real ones.",
          "<b>And log every authorisation denial</b>, because <b>a burst "
          "of denials from one principal is among the clearest attack "
          "signals you will ever get</b> (Module 09 &sect;2) — and "
          "it is free to collect."]),

  ("break",),
  ("h1", "4 &nbsp; Reviewing a design"),
  ("ul", ["<b>Where is the decision made, and can any code path reach "
          "the resource without passing through it?</b> <b>Background "
          "jobs, admin tools, internal APIs, batch exports, and support "
          "consoles are where the second path lives</b> — and <b>this "
          "question finds the most findings</b>: an application with "
          "impeccable authorisation and an unauthenticated internal admin "
          "endpoint is a common and severe pattern.",
          "<b>Is the check object-level?</b> <b>Find an endpoint that "
          "verifies the role and not the object</b> — there is "
          "usually at least one, and it is usually a report, an export, or "
          "a detail view added later.",
          "<b>What happens if the policy evaluation itself fails</b> "
          "— the policy service is unreachable, the attribute lookup "
          "times out? <b>Fail closed</b> (Module 01 &sect;3), and "
          "<b>test that it does</b>, because the default in most "
          "frameworks is not what you want.",
          "<b>How is a revocation propagated, and how quickly?</b> <b>A "
          "cached authorisation decision is a stale authorisation "
          "decision</b>, and <b>the departed employee is the test "
          "case</b>: how long after disabling the account can they still "
          "act?",
          "<b>And who can change the policy?</b> <b>Authorisation over "
          "the authorisation system is the part that is always "
          "forgotten</b>, and it is the highest-value target in the "
          "system — a principal who can grant themselves a role has "
          "every permission."]),
  ("callout", "Multi-tenancy is the hardest case",
   ["<b>In a system shared between tenants, every single query must be "
    "scoped to the requesting tenant</b>, and <b>one unscoped query is a "
    "cross-tenant data exposure</b> — <b>which is the most serious "
    "routine failure in software-as-a-service</b>, and it recurs because "
    "it requires perfect coverage (&sect;1).",
    "<b>So enforce it structurally rather than by discipline:</b> "
    "<b>row-level security in the database, a per-tenant connection or "
    "schema, or a data access layer that physically cannot emit an "
    "unscoped query</b> — because the discipline approach fails "
    "exactly once and that is enough.",
    "<b>And test it adversarially:</b> <b>a generated test suite that "
    "exercises every endpoint as tenant A using tenant B's object "
    "identifiers</b>, and <b>expects a refusal every single time.</b>",
    "<b>Which is the one test suite in this course worth building purely "
    "for its own sake</b> — <b>it is mechanical to generate from "
    "your route table, it covers the highest-severity vulnerability class "
    "in the system, and almost nobody has one.</b>"]),
 ],
 "resources": [
   ("OWASP &mdash; Authorization and Access Control Cheat Sheets, and "
    "the Top Ten A01 (free)",
    "https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html",
    "<b>The working reference for &sect;3 and &sect;4</b>, and A01 "
    "documents why this is the top-ranked class."),
   ("Hardy &mdash; The Confused Deputy (free)",
    "https://web.archive.org/web/20261002224639/http://cap-lore.com/CapTheory/ConfusedDeputy.html",
    "<b>&sect;2's pattern, named</b> — two pages, from 1988, and "
    "it explains five modern vulnerability classes."),
   ("Pang et al. &mdash; Zanzibar: Google's Consistent, Global "
    "Authorization System (free)",
    "https://research.google/pubs/pub48190/",
    "<b>&sect;1's ReBAC model at scale</b>, and a good illustration of "
    "the chokepoint principle implemented as a service."),
   ("Saltzer & Schroeder, and Miller's capability work (free)",
    "https://www.cs.virginia.edu/~evans/cs551/saltzer/",
    "<b>Least privilege and the capability alternative to ambient "
    "authority</b>, which is &sect;2's structural fix."),
 ],
 "exercises": [
   "<b>Classify your system's authorisation</b> as ACL, RBAC, ABAC, "
   "capability, or ReBAC, and name its characteristic failure.",
   "<b>Count your roles.</b> If there are more than twenty, report how "
   "many have exactly one holder.",
   "<b>Find an instance of each confused-deputy variant</b> in a "
   "deliberately vulnerable training application.",
   "<b>Identify every path to one resource</b> in your system, including "
   "jobs and admin tools, and check each passes the authorisation "
   "check.",
   "<b>Find an endpoint that checks the role and not the object</b> and "
   "fix it.",
   "<b>Make your policy evaluation fail</b> and confirm the system denies "
   "rather than permits.",
   "<b>Measure revocation latency:</b> disable an account and time how "
   "long until it can no longer act.",
   "<b>Scope one query at the data layer</b> instead of in the handler, "
   "and report what it prevented.",
   "<b>Generate a cross-tenant test suite</b> from your route table and "
   "run it. Report the failures.",
   "<b>Identify who can modify the authorisation policy</b> and whether "
   "that is itself controlled.",
 ],
 "selfcheck": [
   "Distinguish authentication from authorisation, and say why the "
   "second is a coverage problem.",
   "What should the goal be, rather than a clever model?",
   "Compare five access control models and name RBAC's characteristic "
   "failure.",
   "Define the confused deputy and name five vulnerability classes it "
   "covers.",
   "What is the root cause, and which model resists it structurally?",
   "Give the three non-negotiables of enforcement and the fourth "
   "distinction.",
   "Which design measure prevents rather than catches?",
   "Give five review questions, and say which finds the most.",
   "Why is multi-tenancy hardest, and what is the one test suite worth "
   "building?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Network Security",
 "subtitle": "What the network boundary buys, and what it does not.",
 "question": "What does securing the network actually accomplish?",
 "outcomes": [
     "Explain what TLS provides and what it does not.",
     "Explain certificate validation and its failure modes.",
     "Explain segmentation and what it contains.",
     "Explain why the perimeter model failed and what replaced it.",
     "Design network controls proportionate to a threat model.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Transport security",
   "blurb": "What TLS actually guarantees."},

  {"t": "callout", "title": "TLS gives you confidentiality, integrity, and server identity — and nothing else",
   "kind": "The scope, stated precisely",
   "body": ["<b>It protects data <i>in transit</i> between two "
            "endpoints</b> — against eavesdropping and modification "
            "by anyone on the path.",
            "<b>It authenticates the <i>server</i> you connected "
            "to</b>, by certificate — and <b>it says nothing about "
            "whether that server is trustworthy, correctly configured, or "
            "not compromised.</b>",
            "<b>It does not protect data at rest, data in the "
            "application, or data after the endpoint</b> — which is "
            "where most breaches occur.",
            "<b>And it does not hide <i>who</i> you talked to or how "
            "much</b> — <b>the destination address, the timing, and "
            "the volume are all visible</b>, which is enough to identify "
            "a great deal (and is why traffic analysis is a field)."]},

  {"t": "code", "kicker": "Certificates", "title": "What validation checks, and where it fails",
   "lang": "text", "code": """
  A CORRECT VALIDATION CHECKS, ALL OF THEM:
      the signature chains to a trusted root
      the certificate is within its validity window
      the HOSTNAME matches the certificate's subject or SAN
      the certificate is not revoked (OCSP, CRL, or stapled)
      the key usage permits this use

  THE HISTORIC FAILURES, EVERY ONE OF WHICH SHIPPED:
      chain validated, HOSTNAME NOT CHECKED  <- the classic
      validation disabled "temporarily" in development and
          left disabled
      a custom trust manager accepting everything
      revocation not checked, because it is slow and
          frequently unavailable

  THE HOSTNAME ONE IS WORTH DWELLING ON: a valid
  certificate for ANY domain then authenticates ANY
  server. The chain check passes and the connection is
  completely insecure.

  SO: USE THE PLATFORM'S VALIDATION. Do not write a trust
  manager. And if you must pin, pin to a CA or an
  intermediate rather than a leaf, and have a rotation
  plan -- pinning has caused more outages than it has
  prevented attacks.
""",
   "caption": "<b>The hostname check is the one that gets omitted</b>, "
              "and omitting it makes the rest of the validation "
              "worthless.",
   "note": "The pinning caveat is important; it is frequently "
           "overrecommended."},

  {"t": "section", "label": "Part 2", "title": "Segmentation",
   "blurb": "Containing a compromise rather than preventing one."},

  {"t": "callout", "title": "Segmentation limits lateral movement, which is its only job",
   "kind": "What it is for",
   "body": ["<b>Once an attacker has one host, the question is what "
            "else they can reach from it</b> — and <b>a flat network "
            "means everything.</b>",
            "<b>So segment by trust level and by function</b>, and "
            "<b>default-deny between segments</b> — which turns one "
            "compromised workstation into one compromised workstation "
            "rather than a domain compromise.",
            "<b>And it is a <i>consequence</i> control rather than a "
            "probability control</b> (Module 01 §3's least "
            "privilege, applied to the network).",
            "<b>Which means it earns its keep precisely when prevention "
            "has already failed</b> — <b>so it is the clearest "
            "instance of assume-breach design</b>, and the one most "
            "often deferred because its benefit is invisible until an "
            "incident."]},

  {"t": "table", "kicker": "Controls", "title": "The network controls and what each contains",
   "header": ["Control", "Contains", "Does not"],
   "widths": [2.6, 4.1, 5.3],
   "rows": [
     ["<b>Segmentation</b>", "<b>Lateral movement between zones</b>", "<b>Movement within a zone</b>"],
     ["<b>Egress filtering</b>", "<b>Exfiltration and callbacks</b>", "<b>Anything over an allowed channel</b>"],
     ["<b>Firewall / security group</b>", "<b>Unexpected inbound connections</b>", "<b>Attacks over an expected port</b>"],
     ["<b>VPN</b>", "<b>Transport exposure of internal services</b>", "<b>Anything once a client is on it</b>"],
     ["<b>mTLS between services</b>", "<b>Service impersonation</b>", "<b>A compromised service's own authority</b>"],
   ],
   "footnote": "<b>Egress filtering is the most underused control "
               "here</b> — most compromises need to call out, and "
               "most networks permit arbitrary outbound traffic.",
   "note": "The egress point is actionable and cheap and routinely "
           "skipped."},

  {"t": "section", "label": "Part 3", "title": "The perimeter's failure",
   "blurb": "And what replaced it."},

  {"t": "callout", "title": "The perimeter model assumed a boundary that no longer exists",
   "kind": "Why the architecture changed",
   "body": ["<b>'Inside is trusted, outside is not' worked when "
            "everything was in one building on one network.</b>",
            "<b>And then: remote work, cloud services, contractor "
            "access, mobile devices, and software-as-a-service.</b> "
            "<b>There is no inside.</b>",
            "<b>So the replacement is to authenticate and authorise "
            "every request regardless of origin</b> — no implicit "
            "trust from network position, which is the 'zero trust' "
            "idea stripped of the marketing.",
            "<b>Which is really Module 03's authorisation applied "
            "uniformly</b> — <b>the network stops being an "
            "authorisation input</b>, and <b>the device's posture and the "
            "principal's identity become the inputs instead.</b>"]},

  {"t": "bullets", "kicker": "In practice", "title": "What the replacement actually requires",
   "items": [
     "<b>Strong identity for every principal</b>, human and service "
     "— which is why Module 02 and Module 07 come first.",
     "",
     "<b>Authorisation on every request</b>, at a chokepoint "
     "(Module 03 §3), with the network position as at most one "
     "signal among several.",
     "",
     "<b>Device posture as a signal</b>, where you control the "
     "devices — and honestly, where you do not.",
     "",
     "<b>And segmentation anyway.</b> <b>Removing implicit network "
     "trust does not remove the value of containing a "
     "compromise</b> — the two are complementary.",
     "",
     "<b>Which makes it an expensive programme</b>, and <b>the "
     "honest sequencing is identity first, then authorisation, then "
     "the network</b>.",
   ],
   "footnote": "<b>'Zero trust' is not a product</b> — it is the "
               "consequence of getting identity and authorisation right, "
               "and a vendor selling it as a network appliance has "
               "inverted the dependency."},

  {"t": "section", "label": "Part 4", "title": "Proportionality",
   "blurb": "Matching the controls to the threat."},

  {"t": "callout", "title": "Network controls are frequently the wrong place to spend",
   "kind": "The honest assessment",
   "body": ["<b>Published incident data consistently shows "
            "credentials, unpatched software, and misconfiguration as the "
            "leading initial access vectors</b> — <b>none of which a "
            "firewall addresses.</b>",
            "<b>And network controls are visible, purchasable, and "
            "satisfying to deploy</b>, which makes them attractive "
            "relative to the less visible work of fixing authorisation "
            "and patching.",
            "<b>So the proportionate ordering is usually:</b> "
            "<b>identity and authentication, authorisation, patching, "
            "then segmentation and egress filtering, then "
            "everything else.</b>",
            "<b>With the exception that segmentation and egress "
            "filtering are cheap and high-value</b> — <b>so they are "
            "the network controls to do first and the ones most often "
            "skipped in favour of more expensive and less useful "
            "ones.</b>"]},

  {"t": "bullets", "kicker": "Checklist", "title": "The network review, briefly",
   "items": [
     "<b>Is TLS everywhere, including internal traffic?</b> "
     "<b>Internal plaintext assumes the network is trusted</b> "
     "(Part 3).",
     "",
     "<b>Is certificate validation on, everywhere, including in "
     "every client library?</b>",
     "",
     "<b>Can any host reach any other?</b> <b>If so, one compromise "
     "is a full compromise.</b>",
     "",
     "<b>Can hosts make arbitrary outbound connections?</b> <b>If so, "
     "exfiltration and command-and-control are unimpeded.</b>",
     "",
     "<b>And is the network a <i>sole</i> authorisation input "
     "anywhere?</b> <b>'Internal only' as a security control is the "
     "pattern to find and remove.</b>",
   ],
   "footnote": "<b>The last question finds the most severe findings:</b> "
               "an unauthenticated service protected only by being on the "
               "internal network is a compromise away from being "
               "public."},
 ],
 "takeaways": [
   "TLS protects data in transit and authenticates the server, and says "
   "nothing about whether that server is trustworthy or about data after "
   "the endpoint.",
   "It does not hide who you talked to, when, or how much — which is "
   "enough to identify a great deal.",
   "The hostname check is the validation step that gets omitted, and "
   "omitting it makes the rest worthless.",
   "Segmentation is a consequence control rather than a probability one, "
   "so it earns its keep exactly when prevention has already failed.",
   "Egress filtering is the most underused network control, because most "
   "compromises need to call out.",
   "Network controls are frequently the wrong place to spend — "
   "credentials, patching, and misconfiguration lead the incident data.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Transport security"),
  ("callout", "TLS gives you confidentiality, integrity, and server "
              "identity — and nothing else",
   ["<b>It protects data <i>in transit</i> between two endpoints</b> "
    "— against eavesdropping and against modification by anyone on "
    "the network path. That is a real and valuable guarantee.",
    "<b>It authenticates the <i>server</i> you connected to</b>, by "
    "means of a certificate — and <b>it says nothing whatsoever "
    "about whether that server is trustworthy, correctly configured, "
    "patched, or not currently compromised.</b> A padlock means you are "
    "talking privately to <i>someone</i> who holds a certificate for that "
    "name.",
    "<b>It does not protect data at rest, data inside the application, "
    "or data after it leaves the endpoint</b> — <b>which is where "
    "the overwhelming majority of breaches actually occur</b> "
    "(Module 12's incident data).",
    "<b>And it does not hide <i>who</i> you talked to, when, or how "
    "much.</b> <b>The destination address, the timing, and the volume "
    "are all visible to anyone on the path</b> — which is sufficient "
    "to infer a great deal, and is why traffic analysis is a research "
    "field rather than a footnote. <b>Encrypted DNS and encrypted "
    "client hello narrow this and do not close it.</b>"]),
  ("code", """A CORRECT VALIDATION CHECKS ALL OF THESE:
    the signature chains to a trusted root
    the certificate is within its validity window
    the HOSTNAME matches the subject or a SAN entry
    the certificate is not revoked (OCSP, CRL, or stapled)
    the key usage extension permits this use

THE HISTORIC FAILURES, EVERY ONE OF WHICH SHIPPED IN REAL
SOFTWARE:
    the chain was validated and the HOSTNAME WAS NOT
        CHECKED                            <- the classic
    validation disabled "temporarily" during development
        and left disabled in the release
    a custom trust manager written to accept everything,
        to get past a self-signed certificate once
    revocation not checked at all, because checking is slow
        and the responder is frequently unavailable

THE HOSTNAME ONE IS WORTH DWELLING ON: without it, a valid
certificate for ANY domain authenticates ANY server. The
chain check passes, the library reports success, and the
connection is completely insecure against anyone who can
obtain a certificate for any name at all.

SO: USE THE PLATFORM'S VALIDATION. Do not write a trust
manager. And if you must pin a certificate, pin to a CA or
an intermediate rather than to a leaf, and have a rotation
plan -- certificate pinning has caused considerably more
outages than it has prevented attacks."""),

  ("h1", "2 &nbsp; Segmentation"),
  ("callout", "Segmentation limits lateral movement, which is its only job",
   ["<b>Once an attacker controls one host, the operative question is "
    "what else they can reach from it</b> — and <b>a flat network "
    "means everything</b>, which is how a single phished workstation "
    "becomes a domain compromise.",
    "<b>So segment by trust level and by function</b> — user "
    "workstations, application servers, databases, build infrastructure, "
    "management interfaces — <b>and default-deny between "
    "segments</b>, which turns one compromised workstation into one "
    "compromised workstation.",
    "<b>And it is a <i>consequence</i> control rather than a "
    "<i>probability</i> control</b> — Module 01 &sect;3's least "
    "privilege, applied to the network rather than to a process.",
    "<b>Which means it earns its keep precisely when prevention has "
    "already failed.</b> <b>So it is the clearest instance of "
    "assume-breach design</b>, and <b>it is the control most often "
    "deferred, because its benefit is entirely invisible until there is an "
    "incident</b> — which is a budgeting problem rather than a "
    "technical one and is worth naming as such."]),
  ("table", ["Control", "What it contains", "What it does not"],
   [["<b>Segmentation</b>", "<b>Lateral movement between zones.</b>",
     "<b>Movement within a zone</b> — so zone granularity is the "
     "design decision."],
    ["<b>Egress filtering</b>",
     "<b>Data exfiltration and command-and-control callbacks.</b>",
     "<b>Anything carried over a channel you permit</b> — and HTTPS "
     "to a permitted cloud provider is a channel most networks permit."],
    ["<b>Firewall or security group</b>",
     "<b>Unexpected inbound connections to unexpected ports.</b>",
     "<b>An attack delivered over an expected port to an expected "
     "service</b>, which is how almost all of them arrive."],
    ["<b>VPN</b>",
     "<b>Transport-level exposure of internal services to the public "
     "internet.</b>",
     "<b>Anything at all, once a client is connected</b> — a VPN "
     "grants network position, which &sect;3 argues should not be an "
     "authorisation input."],
    ["<b>Mutual TLS between services</b>",
     "<b>Service impersonation and unauthenticated internal "
     "calls.</b>",
     "<b>A compromised service acting with its own legitimate "
     "authority</b>, which is why Module 03's authorisation is still "
     "needed."]],
   [0.21, 0.34, 0.45]),
  ("p", "<b>Egress filtering is the most underused control in this "
        "table.</b> <b>Most compromises need to call out</b> — to "
        "fetch a second stage, to receive commands, to exfiltrate "
        "data — <b>and most networks permit arbitrary outbound "
        "connections</b>, which makes restricting egress unusually "
        "high-value for its cost. <b>An allowlist of outbound "
        "destinations is tedious to maintain and it breaks a large class "
        "of attack entirely.</b>"),

  ("break",),
  ("h1", "3 &nbsp; The perimeter's failure"),
  ("callout", "The perimeter model assumed a boundary that no longer exists",
   ["<b>'Inside the network is trusted, outside is not' worked "
    "tolerably when everything was in one building, on one network, with "
    "one way in.</b>",
    "<b>And then: remote work, cloud infrastructure, contractor and "
    "vendor access, mobile devices, personal devices, and "
    "software-as-a-service holding your data.</b> <b>There is no inside "
    "any more</b> — the boundary is not weakened, it is absent.",
    "<b>So the replacement is to authenticate and authorise every "
    "request regardless of where it came from</b> — <b>no implicit "
    "trust derived from network position</b>, which is the 'zero trust' "
    "idea with the marketing removed.",
    "<b>Which is really Module 03's authorisation applied "
    "uniformly.</b> <b>The network stops being an authorisation "
    "input</b>, and <b>the principal's identity and the device's posture "
    "become the inputs instead</b> — so the architecture change is "
    "downstream of getting identity and authorisation right, which is why "
    "the sequencing below matters."]),
  ("ul", ["<b>Strong identity for every principal</b>, human and "
          "service — <b>which is why Module 02 and Module 07 "
          "come before this one</b>, and why an organisation without "
          "working identity management cannot do any of this.",
          "<b>Authorisation on every request</b>, at a chokepoint "
          "(Module 03 &sect;3), <b>with the network position as at "
          "most one signal among several</b> rather than as the "
          "decision.",
          "<b>Device posture as a signal</b> where you control the "
          "devices — patch level, disk encryption, management "
          "enrolment — <b>and honestly where you do not</b>, since a "
          "contractor's laptop cannot be assessed.",
          "<b>And segmentation anyway.</b> <b>Removing implicit network "
          "trust does not remove the value of containing a "
          "compromise</b> — the two are complementary rather than "
          "alternatives, and treating the new model as a reason to flatten "
          "the network is a misreading.",
          "<b>Which makes it an expensive, multi-year programme</b>, and "
          "<b>the honest sequencing is identity first, then "
          "authorisation, then the network</b>. <b>'Zero trust' is not a "
          "product</b> — it is the consequence of getting identity "
          "and authorisation right, <b>and a vendor selling it as a "
          "network appliance has inverted the dependency.</b>"]),

  ("h1", "4 &nbsp; Proportionality"),
  ("callout", "Network controls are frequently the wrong place to spend",
   ["<b>Published incident data consistently shows stolen or guessed "
    "credentials, unpatched software, and misconfiguration as the leading "
    "initial access vectors</b> — <b>none of which a firewall "
    "addresses at all.</b>",
    "<b>And network controls are visible, purchasable, and satisfying to "
    "deploy</b>, which makes them attractive relative to the far less "
    "visible work of fixing authorisation coverage, maintaining a patch "
    "cadence, and reviewing configurations — <b>which is an "
    "incentive problem rather than an engineering one</b> and is "
    "Module 12's subject.",
    "<b>So the proportionate ordering is usually:</b> <b>identity and "
    "authentication (Module 02), authorisation (Module 03), patching "
    "and dependency hygiene (Module 08), then segmentation and egress "
    "filtering, then everything else.</b>",
    "<b>With the important exception that segmentation and egress "
    "filtering are cheap and high-value</b> — <b>so they are the "
    "network controls to do first, and they are the ones most often "
    "skipped in favour of more expensive and considerably less useful "
    "ones.</b>"]),
  ("ul", ["<b>Is TLS used everywhere, including for traffic between "
          "internal services?</b> <b>Internal plaintext assumes the "
          "network is trusted</b>, which &sect;3 says it is not.",
          "<b>Is certificate validation enabled everywhere, including "
          "inside every client library and every service-to-service "
          "call?</b> <b>&sect;1's failures are all in client code.</b>",
          "<b>Can any host reach any other host?</b> <b>If so, one "
          "compromise is a full compromise</b>, and the fix is cheap "
          "relative to its value.",
          "<b>Can hosts make arbitrary outbound connections?</b> <b>If "
          "so, exfiltration and command-and-control are entirely "
          "unimpeded</b>, and the detection in Module 09 is your only "
          "line.",
          "<b>And is the network used as a <i>sole</i> authorisation "
          "input anywhere?</b> <b>'Internal only' as a security control "
          "is the pattern to find and remove</b> — <b>and this "
          "question finds the most severe findings</b>, because an "
          "unauthenticated service protected only by being on the internal "
          "network is exactly one compromise away from being public."]),
 ],
 "resources": [
   ("Anderson &mdash; Security Engineering, the networking chapters "
    "(free PDF)",
    "https://www.cl.cam.ac.uk/~rja14/book.html",
    "<b>&sect;1 and &sect;3 in context</b>, with the history of why the "
    "perimeter model was adopted and why it failed."),
   ("Georgiev et al. &mdash; The Most Dangerous Code in the World "
    "(free)",
    "https://crypto.stanford.edu/~dabo/pubs/abstracts/ssl-client-bugs.html",
    "<b>&sect;1's certificate validation failures, surveyed across real "
    "software</b> — and the title is not hyperbole. Required "
    "reading."),
   ("NIST SP 800-207 &mdash; Zero Trust Architecture (free)",
    "https://csrc.nist.gov/publications/detail/sp/800-207/final",
    "<b>&sect;3 without the marketing</b> — the architectural "
    "components and the sequencing."),
   ("Verizon Data Breach Investigations Report (free, annual)",
    "https://www.verizon.com/business/resources/reports/dbir/",
    "<b>&sect;4's incident data</b> — read the initial-access "
    "section each year, and compare it against where your budget "
    "goes."),
 ],
 "exercises": [
   "<b>Capture your own TLS traffic</b> and report what an observer on "
   "the path can still see.",
   "<b>Estimate what the destinations and volumes alone reveal</b> about "
   "a browsing session.",
   "<b>Write a client that validates the chain and not the hostname</b>, "
   "and demonstrate the consequence against your own test server.",
   "<b>Then fix it</b> by using the platform's validation.",
   "<b>Map your network's reachability</b>: can any host reach any "
   "other?",
   "<b>Implement egress filtering</b> on one host and report what broke "
   "and what it would have prevented.",
   "<b>Find a service in your environment protected only by being "
   "internal</b>, and add authentication.",
   "<b>Check certificate validation</b> in every client library your "
   "system uses.",
   "<b>Read the current breach report's initial-access section</b> and "
   "compare against your own control spending.",
   "<b>Write the proportionate ordering</b> for your own system, with "
   "reasons.",
 ],
 "selfcheck": [
   "What does TLS provide, and what does it explicitly not?",
   "What remains visible to an observer on the path?",
   "Name five certificate validation checks and the historic failures of "
   "each.",
   "Why is the hostname check the critical one?",
   "What is the caveat on certificate pinning?",
   "What does segmentation contain, and what kind of control is it?",
   "Name five network controls and what each does not contain.",
   "Why is egress filtering underused?",
   "Why did the perimeter model fail, and what does the replacement "
   "require?",
   "Give the proportionate ordering and the exception to it.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Platform and Isolation",
 "subtitle": "What the operating system and the runtime actually "
             "separate.",
 "question": "What stops one program from reading another's data?",
 "outcomes": [
     "Explain the isolation mechanisms and their boundaries.",
     "Compare processes, containers, and virtual machines as "
     "boundaries.",
     "Explain privilege separation and sandboxing.",
     "Explain the memory-safety classes at a defensive level.",
     "Choose an isolation boundary proportionate to the threat.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The boundaries",
   "blurb": "And what each is worth."},

  {"t": "table", "kicker": "Boundaries", "title": "Isolation mechanisms, by strength",
   "header": ["Boundary", "Enforced by", "Escapes via"],
   "widths": [2.6, 4.0, 5.4],
   "rows": [
     ["<b>Same process</b>", "<b>Nothing — language conventions only</b>", "<b>Any memory bug; not a boundary</b>"],
     ["<b>Process</b>", "<b>The MMU and the kernel</b>", "<b>Kernel vulnerabilities; shared files; IPC</b>"],
     ["<b>Container</b>", "<b>Namespaces and cgroups — one kernel</b>", "<b>Kernel vulnerabilities; misconfiguration</b>"],
     ["<b>Virtual machine</b>", "<b>The hypervisor — separate kernels</b>", "<b>Hypervisor vulnerabilities; side channels</b>"],
     ["<b>Separate machine</b>", "<b>Physics</b>", "<b>The network, and your authorisation</b>"],
   ],
   "footnote": "<b>Containers share a kernel and virtual machines do "
               "not</b>, which is the whole difference — and it is "
               "why multi-tenant isolation is usually at the VM level or "
               "stronger.",
   "note": "The shared-kernel point decides most real architecture "
           "questions."},

  {"t": "callout", "title": "A boundary is only as strong as what enforces it",
   "kind": "The reasoning to apply",
   "body": ["<b>'Isolated' means 'isolated by a specific mechanism "
            "against a specific class of attack'</b> — and <b>asking "
            "which mechanism is the whole analysis.</b>",
            "<b>So a container isolates a buggy process from another "
            "buggy process well</b>, and <b>isolates hostile code from "
            "your kernel much less well</b>, because they share one "
            "kernel and the kernel's attack surface is enormous.",
            "<b>Which is why running untrusted code requires a "
            "stronger boundary</b> — <b>a virtual machine, a "
            "microVM, or a language-level sandbox with a small "
            "interface.</b>",
            "<b>And why 'we run it in a container' is not an answer to "
            "'how do you isolate customer code'</b> — <b>it is an "
            "answer to 'how do you keep deployments from interfering', "
            "which is a different question.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Privilege separation",
   "blurb": "Splitting a program so a compromise yields less."},

  {"t": "code", "kicker": "Privilege separation", "title": "The design, and the canonical example",
   "lang": "text", "code": """
  THE IDEA: split a program so that the part handling
  untrusted input has the LEAST privilege, and the
  privileged part has the SMALLEST interface.

  THE CANONICAL EXAMPLE -- a network daemon:
      a small privileged parent: binds the port, opens
          log files, holds the host key, and answers a
          handful of specific requests
      an unprivileged child per connection: parses the
          protocol, handles the untrusted bytes, runs in
          a sandbox with no filesystem and no network
      they communicate over a NARROW, WELL-DEFINED channel

  SO A PARSER BUG YIELDS AN UNPRIVILEGED SANDBOXED
  PROCESS, not root.

  THE DESIGN RULES
    the privileged part must be SMALL enough to review
    the interface between them must be NARROW enough to
        reason about, and must validate everything
    the unprivileged part must hold NOTHING worth stealing
    and drop privileges EARLY and IRREVERSIBLY

  AND THE SAME SHAPE APPLIES ABOVE THE OS: a browser's
  renderer per site, a microservice per trust level, a
  separate process for untrusted media decoding.
""",
   "caption": "<b>The parser is where untrusted input is handled, so "
              "the parser is what to isolate</b> — which is the "
              "single most transferable instance of this design.",
   "note": "The browser renderer parallel makes it concrete."},

  {"t": "section", "label": "Part 3", "title": "Memory safety",
   "blurb": "The classes, and the defensive response."},

  {"t": "callout", "title": "Memory-unsafe languages produce a predictable class of vulnerability",
   "kind": "The defensive view",
   "body": ["<b>Out-of-bounds access, use after free, double free, and "
            "integer overflow leading to a short allocation</b> — a "
            "small, well-understood set of root causes.",
            "<b>And they have accounted for the majority of severe "
            "vulnerabilities in large C and C++ codebases for "
            "decades</b>, which the major vendors' own published analyses "
            "agree on.",
            "<b>The mitigations help and do not solve it:</b> <b>stack "
            "canaries, address space randomisation, and "
            "non-executable memory each remove one technique and not the "
            "underlying bug.</b>",
            "<b>So the structural answers are a memory-safe "
            "language</b> (Rust, Go, Java, and anything managed) <b>for "
            "new code, and sanitisers and fuzzing for existing "
            "code</b> (CSCE 713's subject) — <b>and the "
            "language choice is the one with a large measured "
            "effect.</b>"]},

  {"t": "bullets", "kicker": "Mitigations", "title": "The platform mitigations, and what each costs the attacker",
   "items": [
     "<b>Non-executable data pages.</b> <b>Removes injecting code "
     "directly</b> — and reuse-of-existing-code techniques work "
     "around it.",
     "",
     "<b>Address space layout randomisation.</b> <b>Requires the "
     "attacker to learn an address first</b>, so it raises the cost "
     "and is defeated by any information leak.",
     "",
     "<b>Stack canaries.</b> <b>Detect sequential stack "
     "overwrites</b>, and not targeted writes or heap corruption.",
     "",
     "<b>Control-flow integrity and shadow stacks.</b> <b>Restrict "
     "where execution may be redirected</b> — currently the most "
     "effective of these.",
     "",
     "<b>And compiler hardening flags, which are free.</b> "
     "<b>Fortified library calls and bounds-checked containers cost "
     "almost nothing and are frequently off.</b>",
   ],
   "footnote": "<b>Turn on everything the toolchain offers and measure "
               "the cost</b> — it is usually a few percent, and the "
               "default-off ones are default-off for historical reasons "
               "rather than good ones."},

  {"t": "section", "label": "Part 4", "title": "Choosing a boundary",
   "blurb": "Proportionate to what you are isolating."},

  {"t": "table", "kicker": "Choosing", "title": "The boundary to use, by what you are running",
   "header": ["What you are running", "Use at least"],
   "widths": [5.3, 5.7],
   "rows": [
     ["<b>Your own code, separate services</b>", "<b>Processes, or containers for packaging</b>"],
     ["<b>Your own code handling untrusted input</b>", "<b>Privilege separation plus a sandbox (Part 2)</b>"],
     ["<b>A third-party library you cannot audit</b>", "<b>Process isolation; a sandbox if it parses</b>"],
     ["<b>Another tenant's code</b>", "<b>A virtual machine or microVM. Not a container</b>"],
     ["<b>Deliberately hostile code</b>", "<b>A VM, on separate hardware, with no network</b>"],
   ],
   "footnote": "<b>The fourth row is the one organisations get "
               "wrong</b> — container isolation between tenants has "
               "been the root cause of real multi-tenant escapes, and "
               "microVMs exist because of it.",
   "note": "The tenant row is where the real architectural decisions "
           "are."},

  {"t": "callout", "title": "And side channels cross every boundary in the table",
   "kind": "The caveat",
   "body": ["<b>Shared caches, shared branch predictors, shared memory "
            "bandwidth, and power consumption leak information across "
            "process, container, and VM boundaries.</b>",
            "<b>Which the Spectre and Meltdown family demonstrated at "
            "scale</b> — <b>architectural isolation was intact and "
            "microarchitectural state was shared.</b>",
            "<b>And the mitigations are expensive:</b> <b>cache "
            "partitioning, disabling shared predictors, and not "
            "co-scheduling different tenants on the same physical "
            "core</b> all cost real performance.",
            "<b>So the honest position is that if you share hardware "
            "with an adversary, some leakage is likely</b> — "
            "<b>which is why the highest-sensitivity workloads run on "
            "dedicated hardware</b>, and that is a proportionality "
            "judgement rather than paranoia."]},
 ],
 "takeaways": [
   "Same-process separation is not a boundary at all — nothing "
   "enforces it but convention.",
   "Containers share a kernel and virtual machines do not, which is the "
   "whole difference and decides multi-tenant architecture.",
   "'Isolated' means isolated by a specific mechanism against a specific "
   "attack class, and asking which is the whole analysis.",
   "Privilege separation puts the untrusted-input parser in the "
   "least-privileged part behind a narrow interface, so a parser bug "
   "yields a sandbox.",
   "Platform mitigations each remove one technique rather than the "
   "underlying bug; a memory-safe language is the change with a measured "
   "effect.",
   "Side channels cross every boundary, so sharing hardware with an "
   "adversary implies some leakage.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The boundaries"),
  ("table", ["Boundary", "Enforced by", "Escaped via"],
   [["<b>Same process, different modules</b>",
     "<b>Nothing — language and library conventions only.</b>",
     "<b>Any memory-safety bug, any reflection, any shared mutable "
     "state. This is not a security boundary</b> and should never be "
     "described as one."],
    ["<b>Separate processes</b>",
     "<b>The memory management unit and the kernel.</b>",
     "<b>Kernel vulnerabilities, shared files, shared sockets, "
     "permissive IPC, and the filesystem.</b> A real boundary, with a "
     "large surface."],
    ["<b>Container</b>",
     "<b>Kernel namespaces and control groups — <i>one shared "
     "kernel</i>.</b>",
     "<b>Kernel vulnerabilities (which are shared), and "
     "misconfiguration</b> — a privileged container, a mounted "
     "socket, or an over-broad capability set."],
    ["<b>Virtual machine</b>",
     "<b>The hypervisor — <i>separate kernels</i>.</b>",
     "<b>Hypervisor vulnerabilities (a far smaller surface than a "
     "kernel) and side channels</b> (&sect;4's callout)."],
    ["<b>Separate physical machine</b>", "<b>Physics.</b>",
     "<b>The network, and whatever authorisation you granted</b> "
     "(Modules 03 and 04)."]],
   [0.20, 0.34, 0.46]),
  ("callout", "A boundary is only as strong as what enforces it",
   ["<b>'Isolated' is not a property; it means 'isolated by a specific "
    "mechanism against a specific class of attack'</b> — and "
    "<b>asking which mechanism and which class is the whole "
    "analysis.</b>",
    "<b>So a container isolates a buggy process from another buggy "
    "process rather well</b>, and <b>isolates deliberately hostile code "
    "from your kernel considerably less well</b>, because <b>they share "
    "one kernel and a kernel's attack surface is enormous</b> — "
    "millions of lines, hundreds of system calls, and a steady stream of "
    "privilege escalation vulnerabilities.",
    "<b>Which is why running untrusted code requires a stronger "
    "boundary</b> — <b>a virtual machine, a microVM with a "
    "deliberately minimal device model, or a language-level sandbox with a "
    "small, auditable interface</b> (WebAssembly with a restricted host "
    "interface is the current example).",
    "<b>And it is why 'we run it in a container' is not an answer to "
    "'how do you isolate customer code'</b> — <b>it is an answer to "
    "'how do you stop deployments interfering with each other', which is a "
    "legitimate and completely different question.</b> <b>Conflating "
    "packaging isolation with security isolation is the commonest error in "
    "this module.</b>"]),

  ("h1", "2 &nbsp; Privilege separation"),
  ("code", """THE IDEA: split a program so that the part handling
untrusted input has the LEAST privilege, and the privileged
part has the SMALLEST interface.

THE CANONICAL EXAMPLE -- a network daemon:
    a small PRIVILEGED PARENT: binds the port, opens log
        files, holds the host key, and answers a handful of
        specific, well-defined requests
    an UNPRIVILEGED CHILD per connection: parses the
        protocol, handles all the untrusted bytes, runs in
        a sandbox with no filesystem and no network access
    they communicate over a NARROW, WELL-DEFINED channel

SO A PARSER BUG YIELDS AN UNPRIVILEGED SANDBOXED PROCESS,
rather than root.

THE DESIGN RULES
  the privileged part must be SMALL enough to review line
      by line
  the interface between the two must be NARROW enough to
      reason about completely, and must validate everything
      crossing it
  the unprivileged part must hold NOTHING worth stealing --
      no keys, no other users' data
  and privileges must be dropped EARLY and IRREVERSIBLY

AND THE SAME SHAPE APPLIES WELL ABOVE THE OPERATING SYSTEM:
a browser's renderer process per site, a microservice per
trust level, a separate process for decoding untrusted
media."""),
  ("p", "<b>The parser is where untrusted input is handled, so the parser "
        "is what to isolate</b> — <b>which is the single most "
        "transferable instance of this design</b>, and it applies to image "
        "decoders, document parsers, protocol handlers, and template "
        "engines alike. <b>A browser's site-isolated renderer is exactly "
        "this pattern at a different scale</b>, and it is why a rendering "
        "engine vulnerability is now a sandbox escape chain rather than a "
        "single bug."),

  ("break",),
  ("h1", "3 &nbsp; Memory safety"),
  ("callout", "Memory-unsafe languages produce a predictable class of "
              "vulnerability",
   ["<b>Out-of-bounds read and write, use after free, double free, "
    "uninitialised memory, and integer overflow leading to a "
    "too-small allocation</b> — <b>a small and very "
    "well-understood set of root causes.</b>",
    "<b>And they have accounted for the substantial majority of severe "
    "vulnerabilities in large C and C++ codebases for decades</b>, which "
    "the major vendors' own published analyses agree on (Microsoft and "
    "Chromium have both reported around 70%).",
    "<b>The platform mitigations help and do not solve it:</b> <b>stack "
    "canaries, address space layout randomisation, and non-executable "
    "memory each remove one exploitation <i>technique</i> and leave the "
    "underlying bug in place</b> — which is why each was followed by "
    "a new technique rather than by the end of the class.",
    "<b>So the structural answers are a memory-safe language for new "
    "code</b> (Rust, Go, Java, C#, and anything managed) <b>and "
    "sanitisers plus fuzzing for existing code</b> (CSCE 713's "
    "subject) — <b>and the language choice is the intervention with a "
    "large, measured effect</b>, which is why national cybersecurity "
    "agencies now recommend it in writing."]),
  ("ul", ["<b>Non-executable data pages.</b> <b>Removes injecting and "
          "jumping to new code</b> — and reuse-of-existing-code "
          "techniques work around it entirely, which is why it was not the "
          "end of the problem.",
          "<b>Address space layout randomisation.</b> <b>Requires the "
          "attacker to learn an address before they can use one</b>, so it "
          "raises the cost — <b>and it is defeated by any information "
          "leak</b>, which is why leaks are now valuable in their own "
          "right.",
          "<b>Stack canaries.</b> <b>Detect sequential overwrites past "
          "a stack buffer</b>, and <b>not targeted writes, heap "
          "corruption, or anything that does not cross the canary.</b>",
          "<b>Control-flow integrity and hardware shadow stacks.</b> "
          "<b>Restrict where execution may be redirected to a set of "
          "legitimate targets</b> — <b>currently the most effective "
          "of these mitigations</b>, and the one with hardware support "
          "arriving.",
          "<b>And compiler hardening flags, which are close to "
          "free.</b> <b>Fortified standard library calls, bounds-checked "
          "containers in debug and release, integer overflow trapping, and "
          "stack protection cost a few percent and are frequently "
          "off</b> — <b>turn on everything the toolchain offers and "
          "measure the cost</b>, because the defaults are historical "
          "rather than considered."]),

  ("h1", "4 &nbsp; Choosing a boundary"),
  ("table", ["What you are running", "Use at least"],
   [["<b>Your own code, as separate services</b>",
     "<b>Separate processes; containers for packaging and resource "
     "limits.</b> The threat is bugs, not malice."],
    ["<b>Your own code handling untrusted input</b>",
     "<b>Privilege separation plus a sandbox for the parsing part</b> "
     "(&sect;2)."],
    ["<b>A third-party library you cannot audit</b>",
     "<b>Process isolation, and a sandbox if it parses anything</b> "
     "— which is Module 08's dependency risk made "
     "architectural."],
    ["<b>Another tenant's code</b>",
     "<b>A virtual machine or a microVM. <i>Not</i> a container.</b> "
     "See the note."],
    ["<b>Deliberately hostile code — malware analysis, untrusted "
     "submissions</b>",
     "<b>A virtual machine, on separate hardware, with no network "
     "access and a snapshot to revert to.</b>"]],
   [0.42, 0.58]),
  ("p", "<b>The fourth row is the one organisations get wrong.</b> "
        "<b>Container-level isolation between tenants has been the root "
        "cause of real multi-tenant escape incidents</b>, and "
        "<b>microVM technologies exist precisely because of it</b> — "
        "they provide VM-grade isolation at container-grade startup cost, "
        "which is what the workload actually needs."),
  ("callout", "And side channels cross every boundary in the table",
   ["<b>Shared caches, shared branch predictors, shared memory "
    "bandwidth, shared execution ports, and even power consumption leak "
    "information across process, container, and virtual machine "
    "boundaries</b> — because those resources are shared at a level "
    "below the one the boundary is enforced at.",
    "<b>Which the Spectre and Meltdown family demonstrated at "
    "scale</b> — <b>the architectural isolation was entirely intact "
    "and the microarchitectural state was shared</b>, and the boundary was "
    "defined over the former.",
    "<b>And the mitigations are expensive:</b> <b>cache partitioning, "
    "disabling or flushing shared predictors on context switch, and "
    "refusing to co-schedule different tenants on sibling hyperthreads of "
    "the same physical core</b> all cost real and sometimes substantial "
    "performance (CSCE 614's subject).",
    "<b>So the honest position is that if you share hardware with an "
    "adversary, some information leakage is likely</b> — <b>which is "
    "why the highest-sensitivity workloads run on dedicated hardware</b>, "
    "and <b>that is a proportionality judgement rather than paranoia</b> "
    "(Module 04 &sect;4's reasoning, applied to the platform)."]),
 ],
 "resources": [
   ("Google &mdash; Building Secure and Reliable Systems, the isolation "
    "chapters (free PDF)",
    "https://sre.google/books/building-secure-reliable-systems/",
    "<b>&sect;1 and &sect;2 from people operating this at scale</b>, "
    "free in full."),
   ("Provos, Friedl & Honeyman &mdash; Preventing Privilege Escalation "
    "(free)",
    "https://www.usenix.org/legacy/events/sec03/tech/full_papers/provos_et_al/provos_et_al.pdf",
    "<b>&sect;2's design, in the paper that introduced it to "
    "OpenSSH</b> — and the design rules are stated explicitly."),
   ("Szekeres et al. &mdash; SoK: Eternal War in Memory (free)",
    "https://users.ece.cmu.edu/~dbrumley/courses/18487-f14/readings/eternal_war.pdf",
    "<b>&sect;3's classes and mitigations, systematised</b> — which "
    "attack each mitigation stops and which it does not."),
   ("Kocher et al. &mdash; Spectre Attacks (free)",
    "https://spectreattack.com/spectre.pdf",
    "<b>&sect;4's callout</b> — and worth reading for the argument "
    "that the boundary was defined at the wrong level."),
 ],
 "exercises": [
   "<b>List every isolation boundary in a system you operate</b> and "
   "name what enforces each.",
   "<b>Find one described as a security boundary that is not one</b>, and "
   "say what it actually provides.",
   "<b>Inspect a container's capabilities and mounts</b> and identify "
   "what would weaken the boundary.",
   "<b>Privilege-separate a small program of your own</b> that parses "
   "input, and verify the parser cannot touch the filesystem.",
   "<b>Narrow the interface between the two parts</b> and document what "
   "crosses it.",
   "<b>Compile a C program with and without hardening flags</b> and "
   "measure the performance difference.",
   "<b>Check which mitigations are enabled</b> in a binary you ship.",
   "<b>Run a sanitiser over an existing C or C++ codebase</b> and report "
   "what it finds.",
   "<b>Classify five workloads</b> against §4's table and say "
   "whether the current boundary is adequate.",
   "<b>Read a side-channel paper</b> and state which boundary it "
   "crossed and what was shared.",
 ],
 "selfcheck": [
   "Name five isolation boundaries, what enforces each, and how each is "
   "escaped.",
   "What is the difference between a container and a VM, and what does "
   "it decide?",
   "Why is 'isolated' not a property?",
   "Why is 'we run it in a container' not an answer for customer code?",
   "Give the privilege separation design and its four rules.",
   "Why is the parser the thing to isolate?",
   "Name the memory-safety classes and what fraction of severe "
   "vulnerabilities they are.",
   "Name five mitigations and what each does not stop.",
   "Give the boundary to use for five workloads, and the row most often "
   "got wrong.",
   "Why do side channels cross every boundary, and what follows?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Web Security",
 "subtitle": "The browser's security model, and the classes it does and "
             "does not cover.",
 "question": "What is the browser actually protecting, and from what?",
 "outcomes": [
     "Explain the same-origin policy and what an origin is.",
     "Explain the injection classes and the one correct defence.",
     "Explain CSRF and the modern mitigations.",
     "Explain the security headers and what each does.",
     "Review a web application against the standard classes.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The origin",
   "blurb": "The unit the whole model is built on."},

  {"t": "callout", "title": "The same-origin policy is the browser's one security boundary",
   "kind": "And the origin is scheme, host, and port",
   "body": ["<b>An origin is the triple (scheme, host, port).</b> "
            "<b>Script from one origin cannot read responses from "
            "another</b> — which is the entire basis of web "
            "security.",
            "<b>Note what it does <i>not</i> prevent:</b> <b>a page can "
            "freely <i>send</i> requests cross-origin</b> — images, "
            "forms, and scripts all load cross-origin by design — "
            "<b>and it is only <i>reading the response</i> that is "
            "blocked.</b>",
            "<b>Which is exactly why CSRF exists</b> "
            "(Part 3): <b>the attacker's page can cause a request "
            "carrying your cookies, and cannot read the answer — "
            "and for a state-changing request, causing it is "
            "enough.</b>",
            "<b>And CORS <i>relaxes</i> the policy rather than "
            "enforcing it</b> — <b>a permissive CORS configuration "
            "is a hole you opened</b>, which is a common "
            "misconfiguration because the direction of the mechanism is "
            "counterintuitive."]},

  {"t": "section", "label": "Part 2", "title": "Injection",
   "blurb": "One cause, many names, one correct fix."},

  {"t": "code", "kicker": "Injection", "title": "Injection 1/2: one cause, many parsers",
   "lang": "text", "code": """
  THE CAUSE, EVERY TIME: data is concatenated into a string
  that is then PARSED as code by some interpreter. The
  parser cannot tell your data from your structure.

    SQL injection      -> the database's parser
    command injection  -> the shell's parser
    XSS                -> the browser's HTML/JS parser
    LDAP, XPath, NoSQL -> their respective parsers
    template injection -> the template engine's parser
    log injection      -> whatever reads the log

  THE DEFENCE THAT WORKS: never build the string. Use an
  interface that keeps data and structure SEPARATE.
      SQL     -> parameterised queries. Always.
      shell   -> pass an argument array, not a string;
                 better, do not invoke a shell at all
      HTML    -> contextual escaping by the template
                 engine, or a DOM API that takes text
      JSON    -> a serialiser, never string building
""",
   "caption": "<b>One cause and one correct defence</b> — keep data "
              "and structure separate, rather than trying to make the "
              "data safe.",
   "note": "The single-cause framing is what makes six acronyms one "
           "lesson."},

  {"t": "code", "kicker": "Injection", "title": "Injection 2/2: the defences that fail",
   "lang": "text", "code": """
  THE DEFENCES THAT DO NOT WORK RELIABLY

      blocklists -- you will miss an encoding, and the
          attacker only needs the one you missed

      input sanitisation at the boundary -- the right
          escaping depends on the DESTINATION context,
          which the boundary does not and cannot know.
          The same value is safe in HTML text and unsafe
          in an attribute, a URL, or a script block.

      escaping by hand -- correct until the context
          changes, and the context changes without the
          escaping being revisited

  SO: ESCAPE AT THE POINT OF USE, BY CONTEXT, USING THE
  INTERPRETER'S OWN PARAMETERISATION.
""",
   "caption": "<b>Escape at the point of use, by context</b> — "
              "because the correct escaping depends on where the value "
              "lands, which the input boundary cannot know.",
   "note": "The escape-at-use-not-at-input point is the one that "
           "changes behaviour."},

  {"t": "callout", "title": "Cross-site scripting is injection into the browser, and context is everything",
   "kind": "The one with the most contexts",
   "body": ["<b>The same value needs different escaping depending on "
            "where it lands:</b> <b>HTML text, an attribute value, "
            "inside a script, in a URL, or in CSS</b> — five "
            "different escaping rules.",
            "<b>Which is why a single <code>escapeHtml</code> function "
            "is insufficient</b> — <b>it is correct for element text "
            "and wrong inside an attribute without quotes, and dangerous "
            "inside a script block.</b>",
            "<b>So use a template engine that escapes by context "
            "automatically</b>, and <b>treat any manual escaping or "
            "<code>innerHTML</code> assignment as a finding to be "
            "justified.</b>",
            "<b>And Content Security Policy is the defence in "
            "depth</b> — <b>it does not fix the injection and it "
            "substantially limits what an injection can do</b> "
            "(Part 4)."]},

  {"t": "section", "label": "Part 3", "title": "CSRF",
   "blurb": "The confused deputy, in the browser."},

  {"t": "callout", "title": "CSRF: the browser attaches your credentials to a request the attacker caused",
   "kind": "And the modern mitigation is mostly free",
   "body": ["<b>An attacker's page submits a form to your site. The "
            "browser attaches your session cookie. Your server acts on "
            "your authority.</b> <b>Module 03 §2's confused "
            "deputy, exactly.</b>",
            "<b>The classical mitigation is a synchroniser token</b> "
            "— an unpredictable value tied to the session, required "
            "on every state-changing request, which the attacker's page "
            "cannot read (Part 1).",
            "<b>And the modern one is "
            "<code>SameSite</code> cookies</b> — "
            "<code>Lax</code> is now the browser default, which breaks "
            "the basic attack without any application change.",
            "<b>So the current position is:</b> <b>rely on SameSite, "
            "add tokens for anything sensitive, never use GET for a "
            "state change, and check the Origin header on state-changing "
            "requests.</b> <b>Defence in depth, because the cookie "
            "default can be overridden.</b>"]},

  {"t": "section", "label": "Part 4", "title": "The headers",
   "blurb": "What each actually does."},

  {"t": "table", "kicker": "Headers", "title": "The security headers worth setting",
   "header": ["Header", "What it does", "Note"],
   "widths": [2.9, 4.0, 5.1],
   "rows": [
     ["<b>Content-Security-Policy</b>", "<b>Restricts what sources may load and execute</b>", "<b>The highest-value one. Hard to deploy</b>"],
     ["<b>Strict-Transport-Security</b>", "<b>Forces HTTPS for this host, including the first visit after preload</b>", "<b>Cheap and effective</b>"],
     ["<b>X-Content-Type-Options</b>", "<b>Stops content-type sniffing</b>", "<b>One line; prevents a real class</b>"],
     ["<b>X-Frame-Options / frame-ancestors</b>", "<b>Prevents framing — clickjacking</b>", "<b>Use the CSP directive</b>"],
     ["<b>Referrer-Policy</b>", "<b>Limits URL leakage to third parties</b>", "<b>A privacy and a secrets-in-URLs control</b>"],
   ],
   "footnote": "<b>Content-Security-Policy is the one worth the effort "
               "and the one that is hard</b> — a strict policy "
               "requires eliminating inline script, which is a real "
               "refactor on an existing application.",
   "note": "Being honest that CSP is hard to adopt is more useful than "
           "recommending it flatly."},

  {"t": "bullets", "kicker": "Review", "title": "The web review, briefly",
   "items": [
     "<b>Is every query parameterised?</b> <b>Search the codebase for "
     "string concatenation into SQL</b> — it takes ten minutes and "
     "it finds things.",
     "",
     "<b>Is every template auto-escaping, and is every escape bypass "
     "justified?</b> <b><code>innerHTML</code>, "
     "<code>dangerouslySetInnerHTML</code>, and the equivalents are "
     "the list.</b>",
     "",
     "<b>Is every state change a POST with SameSite and a token?</b> "
     "<b>And is there no state-changing GET anywhere?</b>",
     "",
     "<b>Are the headers set?</b> <b>Check with a scanner, and check "
     "every response rather than the home page.</b>",
     "",
     "<b>And is CORS as narrow as it can be?</b> <b>A wildcard origin "
     "with credentials is the finding to look for.</b>",
   ],
   "footnote": "<b>The SQL concatenation search is the single "
               "highest-value ten minutes in a web review</b>, and it "
               "almost always finds at least one instance."},
 ],
 "takeaways": [
   "The same-origin policy blocks reading a cross-origin response and does "
   "not block sending a cross-origin request — which is exactly why "
   "CSRF exists.",
   "CORS relaxes the policy rather than enforcing it, so a permissive CORS "
   "configuration is a hole you opened.",
   "Every injection class has one cause: data concatenated into a string "
   "that an interpreter then parses.",
   "The fix is to escape at the point of use, by context, using the "
   "interpreter's own parameterisation — input sanitisation cannot "
   "know the destination context.",
   "CSRF is the confused deputy in the browser, and SameSite cookies now "
   "break the basic attack by default.",
   "Content-Security-Policy is the highest-value header and the hardest to "
   "deploy, because a strict policy requires eliminating inline script.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The origin"),
  ("callout", "The same-origin policy is the browser's one security "
              "boundary",
   ["<b>An origin is the triple (scheme, host, port).</b> <b>Script "
    "running in one origin cannot read responses from another</b> — "
    "<b>which is the entire basis of web security</b>, and everything "
    "else is a refinement of or an exception to it.",
    "<b>Note carefully what it does <i>not</i> prevent:</b> <b>a page "
    "can freely <i>send</i> requests to any origin</b> — images, "
    "stylesheets, scripts, and form submissions all load and post "
    "cross-origin by design, because the web was built on that — "
    "<b>and it is only <i>reading the response</i> that is blocked.</b>",
    "<b>Which is exactly why CSRF exists</b> (&sect;3): <b>the "
    "attacker's page can cause a request that carries your cookies, and "
    "cannot read the answer</b> — <b>and for a state-changing "
    "request, causing it is entirely sufficient.</b>",
    "<b>And CORS <i>relaxes</i> the policy rather than enforcing "
    "it.</b> <b>A permissive CORS configuration is a hole that you "
    "opened</b>, not a control that you added — which is a common "
    "and severe misconfiguration precisely because <b>the direction of "
    "the mechanism is counterintuitive</b>: developers add CORS headers to "
    "make something work and do not read them as granting access."]),

  ("h1", "2 &nbsp; Injection"),
  ("code", """THE CAUSE, EVERY TIME: data is concatenated into a string
which is then PARSED AS CODE by some interpreter. The
parser cannot tell your data from your structure, because
by the time it sees them they are the same string.

  SQL injection       -> the database's SQL parser
  command injection   -> the shell's parser
  cross-site script.  -> the browser's HTML and JS parsers
  LDAP, XPath, NoSQL  -> their respective query parsers
  template injection  -> the template engine's parser
  log injection       -> whatever later reads the log

THE DEFENCE THAT WORKS: never build the string. Use an
interface that keeps data and structure SEPARATE all the
way down.
    SQL      -> parameterised queries. Always, everywhere.
    shell    -> pass an argument array rather than a
                string; better still, do not invoke a
                shell at all
    HTML     -> contextual escaping by the template engine,
                or a DOM API that takes text rather than
                markup
    JSON     -> a serialiser, never string building

THE DEFENCES THAT DO NOT WORK RELIABLY
    blocklists of dangerous characters -- you will miss an
        encoding, and there is always another encoding
    input sanitisation at the boundary -- the CORRECT
        escaping depends on the DESTINATION context, and
        the input boundary does not know the destination
    escaping by hand -- correct until someone changes the
        context around it, which nobody notices

SO: ESCAPE AT THE POINT OF USE, BY CONTEXT, USING THE
INTERPRETER'S OWN PARAMETERISATION."""),
  ("p", "<b>'Escape at the point of use, by context' is the sentence that "
        "changes behaviour</b>, and the reason is in the third "
        "non-defence: <b>the correct escaping depends on where the value "
        "lands, and the input boundary cannot know where that will "
        "be.</b> <b>Sanitising on input feels safer and is structurally "
        "unable to be correct</b>, which is why frameworks moved to "
        "contextual auto-escaping on output."),
  ("callout", "Cross-site scripting is injection into the browser, and "
              "context is everything",
   ["<b>The same value requires different escaping depending on where it "
    "lands:</b> <b>as HTML element text, as an attribute value (quoted or "
    "unquoted), inside a script block, inside a URL, or inside "
    "CSS</b> — <b>five different escaping rules</b>, and the wrong "
    "one is frequently worse than none because it looks safe.",
    "<b>Which is why a single <code>escapeHtml</code> function is "
    "insufficient</b> — <b>it is correct for element text, wrong "
    "inside an unquoted attribute, and actively dangerous inside a script "
    "block</b>, where HTML escaping does nothing useful and JavaScript "
    "string escaping is what is needed.",
    "<b>So use a template engine that escapes by context "
    "automatically</b> (which the major modern ones do), and <b>treat any "
    "manual escaping, any <code>innerHTML</code> assignment, and any "
    "escape-bypass directive as a finding that must be individually "
    "justified</b> — which makes the review tractable, because the "
    "list of bypasses is short and greppable.",
    "<b>And Content Security Policy is the defence in depth</b> "
    "(&sect;4) — <b>it does not fix the injection and it "
    "substantially limits what an injection can accomplish</b>, which is "
    "Module 01 &sect;3's layering applied to a specific class."]),

  ("break",),
  ("h1", "3 &nbsp; CSRF"),
  ("callout", "CSRF: the browser attaches your credentials to a request "
              "the attacker caused",
   ["<b>An attacker's page submits a form to your site, or loads an "
    "image whose URL is a state-changing endpoint. The browser attaches "
    "your session cookie, because that is what cookies do. Your server "
    "acts on your authority.</b> <b>Module 03 &sect;2's confused "
    "deputy, exactly — with the browser as the deputy.</b>",
    "<b>The classical mitigation is a synchroniser token</b>: an "
    "unpredictable value bound to the session, required on every "
    "state-changing request, <b>which the attacker's page cannot read "
    "because of the same-origin policy</b> (&sect;1) — so the "
    "defence rests on exactly the property the attack exploits the absence "
    "of.",
    "<b>And the modern mitigation is the <code>SameSite</code> cookie "
    "attribute</b> — <b><code>Lax</code> is now the default in major "
    "browsers</b>, which breaks the basic cross-site form submission "
    "without any application change at all.",
    "<b>So the current position is:</b> <b>rely on SameSite as the "
    "baseline, add synchroniser tokens for anything sensitive, never use "
    "GET for a state change (because GET requests are triggered by images "
    "and prefetching), and verify the Origin header on state-changing "
    "requests.</b> <b>Defence in depth, because the cookie default can be "
    "overridden by a developer who needed cross-site posting for something "
    "else.</b>"]),

  ("h1", "4 &nbsp; The headers, and the review"),
  ("table", ["Header", "What it does", "Note"],
   [["<b>Content-Security-Policy</b>",
     "<b>Restricts which sources may be loaded and which script may "
     "execute.</b>",
     "<b>The highest-value header, and genuinely hard to deploy</b> "
     "— see the note."],
    ["<b>Strict-Transport-Security</b>",
     "<b>Forces HTTPS for this host for a stated period, including the "
     "very first visit if preloaded.</b>",
     "<b>Cheap and effective</b> — it closes the downgrade window "
     "that Module 04's TLS cannot."],
    ["<b>X-Content-Type-Options: nosniff</b>",
     "<b>Stops the browser guessing a content type different from the "
     "declared one.</b>",
     "<b>One line, and it prevents a real vulnerability class</b> where "
     "an uploaded file is interpreted as script."],
    ["<b>X-Frame-Options, or CSP frame-ancestors</b>",
     "<b>Prevents your page being framed — which is "
     "clickjacking.</b>",
     "<b>Use the CSP directive</b>, which is the modern and more "
     "flexible form."],
    ["<b>Referrer-Policy</b>",
     "<b>Limits how much of your URL is sent to third parties.</b>",
     "<b>A privacy control and a mitigation for secrets accidentally "
     "placed in URLs</b> — which should not happen and does."]],
   [0.24, 0.34, 0.42]),
  ("p", "<b>Content-Security-Policy is the one worth the effort and the "
        "one that is hard.</b> <b>A strict policy requires eliminating "
        "inline script and inline event handlers</b>, which is a real "
        "refactor on an existing application — <b>so the honest "
        "advice is to deploy it in report-only mode first, read the "
        "reports for a month, and tighten incrementally</b>, rather than "
        "recommending it flatly and watching it be abandoned."),
  ("ul", ["<b>Is every database query parameterised?</b> <b>Search the "
          "codebase for string concatenation or interpolation into "
          "SQL</b> — <b>it takes ten minutes and it is the single "
          "highest-value ten minutes in a web review</b>, and it almost "
          "always finds at least one instance.",
          "<b>Is every template auto-escaping, and is every escape "
          "bypass individually justified?</b> <b><code>innerHTML</code>, "
          "<code>dangerouslySetInnerHTML</code>, <code>|safe</code>, "
          "<code>mark_safe</code>, and the equivalents are the complete "
          "greppable list.</b>",
          "<b>Is every state change a POST, with SameSite set and a "
          "token where it matters?</b> <b>And is there no state-changing "
          "GET endpoint anywhere</b> — including in admin tools and "
          "legacy routes?",
          "<b>Are the security headers set?</b> <b>Check with a "
          "scanner, and check <i>every</i> response rather than the home "
          "page</b> — API responses and error pages frequently lack "
          "them.",
          "<b>And is the CORS configuration as narrow as it can be?</b> "
          "<b>A wildcard origin combined with credentials is the specific "
          "finding to look for</b> (&sect;1), and it is a common result of "
          "making something work during development."]),
 ],
 "resources": [
   ("OWASP &mdash; the Cheat Sheet Series and the Top Ten (free)",
    "https://cheatsheetseries.owasp.org/",
    "<b>The working reference for this entire module</b> — "
    "specific, current, and defensive, with a sheet per class."),
   ("Zalewski &mdash; The Tangled Web",
    "https://nostarch.com/tangledweb",
    "<b>&sect;1's model, explained properly</b> — the best account "
    "of how the browser security model came to be what it is. Library "
    "copy; the author's Browser Security Handbook is free."),
   ("Google &mdash; CSP: A Successful Mess Between Hardening and "
    "Mitigation (free)",
    "https://research.google/pubs/pub45542/",
    "<b>&sect;4's honest assessment of CSP</b>, from people who deployed "
    "it at scale — including why strict policies are hard."),
   ("MDN &mdash; Same-origin policy, CORS, and SameSite cookies "
    "(free)",
    "https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy",
    "<b>The accurate current reference for &sect;1 and &sect;3</b>, "
    "which matters because the defaults have changed recently."),
 ],
 "exercises": [
   "<b>State the origin</b> of five URLs and say which pairs are "
   "same-origin.",
   "<b>Demonstrate that a cross-origin request can be sent and not "
   "read</b>, on your own test pages.",
   "<b>Find a permissive CORS configuration</b> in a training "
   "application and explain what it grants.",
   "<b>Find and fix a SQL injection</b> in a deliberately vulnerable "
   "application, using parameterisation.",
   "<b>Escape the same value for five different HTML contexts</b> and "
   "confirm the rules differ.",
   "<b>Demonstrate that HTML escaping inside a script block is "
   "insufficient.</b>",
   "<b>Build a CSRF demonstration</b> against your own test application, "
   "then fix it with SameSite and a token.",
   "<b>Set every header in §4's table</b> on an application of "
   "yours and verify with a scanner.",
   "<b>Deploy CSP in report-only mode</b> and read a week of reports.",
   "<b>Run §4's five-point review</b> on a web application you own "
   "and report the findings.",
 ],
 "selfcheck": [
   "Define an origin and state what the same-origin policy blocks and "
   "does not.",
   "Why does CSRF exist, given the policy?",
   "What does CORS do, and why is the direction counterintuitive?",
   "Give the single cause of every injection class and name six "
   "instances.",
   "What is the defence that works, and why do the other three fail?",
   "Why is input sanitisation structurally unable to be correct?",
   "Why is one escapeHtml function insufficient for XSS?",
   "Explain CSRF as a confused deputy and give the modern mitigations.",
   "Name five security headers and what each does.",
   "Why is CSP both the highest-value header and the hardest?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Secrets and Keys",
 "subtitle": "The hard part of applied cryptography.",
 "question": "Where do the keys live, and who can use them?",
 "outcomes": [
     "Explain why key management rather than cryptography is the "
     "failure point.",
     "Design secret storage for an application.",
     "Explain rotation and why it is the hard requirement.",
     "Explain the hardware-backed options and what each buys.",
     "Review a system for secret-handling failures.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Where it goes wrong",
   "blurb": "Not in the algorithms."},

  {"t": "callout", "title": "The primitives work; the key management does not",
   "kind": "The division of labour with CSCE 711",
   "body": ["<b>Modern authenticated encryption, signatures, and key "
            "agreement are, used correctly, not the weak point</b> "
            "— CSCE 711 covers them, and <b>the practical advice "
            "there is to use a high-level library and not to choose "
            "primitives.</b>",
            "<b>The failures are in the keys:</b> <b>committed to a "
            "repository, logged, baked into a container image, shared "
            "between environments, never rotated, or held by a service "
            "that did not need them.</b>",
            "<b>And they are mostly detectable.</b> <b>Secret scanning "
            "finds committed credentials, and the major platforms now do "
            "it by default</b> — which has turned a silent failure "
            "into a noisy one.",
            "<b>So this module is about plumbing</b> — <b>which is "
            "where the incidents are</b>, and <b>a course that spent its "
            "cryptography time on cipher modes rather than on key "
            "handling would be addressing the wrong problem.</b>"]},

  {"t": "table", "kicker": "Storage", "title": "Where to put a secret, worst to best",
   "header": ["Location", "Problem", "Verdict"],
   "widths": [2.8, 4.1, 5.1],
   "rows": [
     ["<b>In source code</b>", "<b>In every clone, forever, in history</b>", "<b>Never. And rotate, not just delete</b>"],
     ["<b>In a config file in the image</b>", "<b>In every registry copy; readable by anyone with the image</b>", "<b>Avoid</b>"],
     ["<b>In an environment variable</b>", "<b>Visible in process listings, crash dumps, and child processes</b>", "<b>Acceptable; not ideal</b>"],
     ["<b>In a mounted file, tmpfs</b>", "<b>Readable by the process; not in the image</b>", "<b>Good</b>"],
     ["<b>Fetched at runtime from a secret manager</b>", "<b>Requires an identity to fetch with</b>", "<b>Better — and rotation becomes possible</b>"],
     ["<b>Never leaves an HSM or KMS</b>", "<b>Operations go to the device; latency</b>", "<b>Best, for keys you can use remotely</b>"],
   ],
   "footnote": "<b>The last row is the real goal:</b> <b>a key that "
               "never exists in your process memory cannot be leaked by "
               "your process</b> — which converts a secrecy problem "
               "into an authorisation problem.",
   "note": "The never-leaves-the-HSM framing is the architectural "
           "insight."},

  {"t": "section", "label": "Part 2", "title": "The bootstrap problem",
   "blurb": "The secret you need to get the secrets."},

  {"t": "callout", "title": "Every secret management scheme has a bootstrap problem",
   "kind": "And the answer is an identity rather than a secret",
   "body": ["<b>To fetch a secret you must authenticate to the secret "
            "manager</b> — <b>which requires a credential, which is "
            "a secret, which must be stored somewhere.</b>",
            "<b>The wrong answer is a long-lived token in a config "
            "file</b>, which has moved the problem rather than solved "
            "it.",
            "<b>The right answer is a <i>platform-provided "
            "identity</i></b> — <b>a cloud instance role, a Kubernetes "
            "service account, a TPM-attested device identity</b> "
            "— <b>where the platform attests to who you are and no "
            "stored secret is involved.</b>",
            "<b>So the bootstrap is resolved by moving it into "
            "infrastructure that can attest</b> — <b>and if you have "
            "no such infrastructure, the bootstrap secret is the one you "
            "protect hardest and rotate most carefully.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Rotation",
   "blurb": "The requirement that shapes the design."},

  {"t": "code", "kicker": "Rotation", "title": "Why rotation is hard, and how to make it possible",
   "lang": "text", "code": """
  WHY YOU NEED IT
      a leaked key must be replaceable without an outage
      a departing employee's access must end
      and a key used for years accumulates exposure

  WHY IT IS HARD: everything that holds the key must learn
  the new one, and they do not all learn it at once. So
  there is a window where BOTH are in use.

  WHICH MEANS THE DESIGN MUST SUPPORT TWO VALID KEYS AT
  ONCE:
      verifiers accept old AND new
      signers/encryptors move to new
      then old is withdrawn
      -- a three-phase rollout, and the system must be
         built for it from the start

  SO: KEY IDENTIFIERS EVERYWHERE. Every ciphertext, token,
  and signature carries which key made it. Without that
  you cannot roll over; you can only cut over, with an
  outage.

  AND TEST THE ROTATION. An untested rotation procedure
  will be attempted for the first time during an incident,
  which is the worst possible time -- so rotate on a
  schedule even when nothing is wrong, which is the only
  way to know the procedure works.
""",
   "caption": "<b>Key identifiers in every artefact are the design "
              "decision that makes rotation possible</b> — retrofit "
              "them and you will have an outage.",
   "note": "The rotate-on-schedule-to-test-the-procedure point is the "
           "operational insight."},

  {"t": "section", "label": "Part 4", "title": "Reviewing",
   "blurb": "Where to look."},

  {"t": "bullets", "kicker": "Review", "title": "The secret-handling review",
   "items": [
     "<b>Scan the repository history</b>, not just the working tree. "
     "<b>A deleted secret is still in the history and must be "
     "rotated.</b>",
     "",
     "<b>Grep the logs for secret-shaped strings.</b> <b>Secrets in "
     "logs is a large and quiet class</b>, because logs are copied "
     "widely and retained long.",
     "",
     "<b>Check whether any secret is shared between "
     "environments.</b> <b>A production key in a staging system "
     "inherits staging's security.</b>",
     "",
     "<b>Ask when each secret was last rotated</b>, and whether the "
     "procedure has ever been executed.",
     "",
     "<b>And ask who can read each secret</b> — <b>'everyone in "
     "engineering' is the common and wrong answer</b> "
     "(Module 03).",
   ],
   "footnote": "<b>Rotate rather than delete:</b> once a secret has "
               "been committed, logged, or shared, it must be treated as "
               "compromised — removing the text does not "
               "un-disclose it."},

  {"t": "callout", "title": "The hardware-backed options, and what each buys",
   "kind": "When to use which",
   "body": ["<b>A cloud KMS:</b> <b>keys never leave the service, and "
            "you call it to encrypt, decrypt, or sign</b> — which "
            "turns key secrecy into an authorisation and audit problem, "
            "and both are tractable.",
            "<b>An HSM:</b> the same, with a hardware tamper boundary "
            "and a compliance story — <b>used where a regulator "
            "requires it or the key is extremely valuable.</b>",
            "<b>A TPM or secure element:</b> <b>binds a key to a "
            "specific device</b>, which is what makes device identity and "
            "disk encryption work.",
            "<b>And a hardware security key:</b> <b>binds a key to a "
            "physical object a person holds</b> — which is "
            "Module 02 §1's phishing resistance, and is the same "
            "mechanism at a different scale."]},
 ],
 "takeaways": [
   "The cryptographic primitives work; the failures are keys committed, "
   "logged, baked into images, shared between environments, or never "
   "rotated.",
   "A key that never leaves an HSM or KMS cannot be leaked by your "
   "process, which converts a secrecy problem into an authorisation "
   "problem.",
   "Every secret management scheme has a bootstrap problem, and the answer "
   "is a platform-provided identity rather than a stored secret.",
   "Rotation requires two keys valid at once, which requires key "
   "identifiers in every ciphertext, token, and signature.",
   "Rotate on a schedule even when nothing is wrong, because an untested "
   "procedure will first be attempted during an incident.",
   "Once a secret has been committed or logged it must be rotated — "
   "removing the text does not un-disclose it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Where it goes wrong"),
  ("callout", "The primitives work; the key management does not",
   ["<b>Modern authenticated encryption, digital signatures, and key "
    "agreement are, when used correctly, not the weak point of a "
    "system</b> — <b>CSCE 711 covers them, and the practical "
    "advice there is to use a high-level library and not to select "
    "primitives or modes yourself.</b>",
    "<b>The failures are in the keys:</b> <b>committed to a source "
    "repository, written to a log, baked into a container image, shared "
    "between production and staging, never rotated in five years, or held "
    "in the memory of a service that had no need of them.</b> Every one "
    "of those is a configuration or process failure rather than a "
    "mathematical one.",
    "<b>And they are mostly detectable.</b> <b>Secret scanning finds "
    "committed credentials reliably, and the major code-hosting platforms "
    "now scan by default and notify the issuing provider</b> — which "
    "has usefully converted a silent failure into a noisy one, and is one "
    "of the more effective interventions of the last decade.",
    "<b>So this module is about plumbing.</b> <b>Which is where the "
    "incidents are</b> — <b>and a course that spent its "
    "cryptography time on cipher modes rather than on key handling would "
    "be addressing the wrong problem</b>, which is why the division "
    "between this course and CSCE 711 falls where it does."]),
  ("table", ["Where the secret lives", "The problem", "Verdict"],
   [["<b>In source code</b>",
     "<b>It is in every clone, in the history, forever</b> — and in "
     "every fork and every backup.",
     "<b>Never. And when found, rotate rather than delete</b> (&sect;4's "
     "footnote)."],
    ["<b>In a configuration file inside the container image</b>",
     "<b>It is in every copy of the image in every registry, readable by "
     "anyone who can pull it.</b>",
     "<b>Avoid</b> — and note that image layers retain deleted "
     "files."],
    ["<b>In an environment variable</b>",
     "<b>Visible in process listings, inherited by every child process, "
     "and captured in crash dumps and error reporters.</b>",
     "<b>Acceptable and not ideal</b> — the crash-dump path is the "
     "one that surprises people."],
    ["<b>In a file mounted at runtime, on tmpfs</b>",
     "<b>Readable by the process and by anything that can read its "
     "filesystem; not present in the image.</b>", "<b>Good.</b>"],
    ["<b>Fetched at runtime from a secret manager</b>",
     "<b>Requires an identity to authenticate with</b> — which is "
     "&sect;2's bootstrap problem.",
     "<b>Better — and crucially, rotation becomes possible</b> "
     "(&sect;3)."],
    ["<b>Never leaves an HSM or KMS; operations are performed "
     "there</b>",
     "<b>Every cryptographic operation becomes a network call, with "
     "latency and an availability dependency.</b>",
     "<b>Best, for any key you can use remotely.</b>"]],
   [0.27, 0.38, 0.35]),
  ("p", "<b>The last row is the real goal and is worth stating as an "
        "architectural principle:</b> <b>a key that never exists in your "
        "process's memory cannot be leaked by your process</b> — not "
        "by a memory disclosure bug, not by a crash dump, not by a core "
        "file, and not by an attacker with code execution. <b>Which "
        "converts a secrecy problem into an authorisation and audit "
        "problem</b>, and <b>those are tractable with Module 03's "
        "machinery</b> while 'keep this value secret in a process an "
        "attacker may control' is not."),

  ("h1", "2 &nbsp; The bootstrap problem"),
  ("callout", "Every secret management scheme has a bootstrap problem",
   ["<b>To fetch a secret from a secret manager you must authenticate to "
    "the secret manager</b> — <b>which requires a credential, which "
    "is itself a secret, which must be stored somewhere.</b> The problem "
    "recurses.",
    "<b>The wrong answer is a long-lived token in a configuration "
    "file</b>, because that has <b>moved the problem rather than solved "
    "it</b> — you now have one secret in a file instead of twenty, "
    "which is an improvement in blast radius and not a solution.",
    "<b>The right answer is a <i>platform-provided identity</i></b> "
    "— <b>a cloud instance role, a Kubernetes service account token "
    "projected by the kubelet, a TPM-attested device identity, or a "
    "workload identity federated from the orchestrator</b> — "
    "<b>where the platform attests to who you are and no long-lived "
    "stored secret is involved at all.</b>",
    "<b>So the bootstrap is resolved by moving it into infrastructure "
    "that can attest to identity</b>, which is the one component "
    "positioned to do so. <b>And if you have no such "
    "infrastructure, then the bootstrap secret is the one you protect "
    "hardest, scope most narrowly, and rotate most carefully</b> — "
    "which is an honest answer rather than a good one."]),

  ("break",),
  ("h1", "3 &nbsp; Rotation"),
  ("code", """WHY YOU NEED IT
    a leaked key must be replaceable without an outage
    a departing employee's access must actually end
    and a key in use for years accumulates exposure --
        through backups, logs, and former staff

WHY IT IS HARD: everything that holds or verifies the key
must learn the new one, and they do not all learn it at the
same moment. So there is necessarily a window during which
BOTH keys are in use.

WHICH MEANS THE DESIGN MUST SUPPORT TWO VALID KEYS AT ONCE:
    phase 1: verifiers accept OLD and NEW
    phase 2: signers and encryptors switch to NEW
    phase 3: OLD is withdrawn
    -- a three-phase rollout, and the system has to be
       built for it from the beginning

SO: KEY IDENTIFIERS EVERYWHERE. Every ciphertext, every
token, and every signature carries an identifier saying
which key produced it. Without that you cannot roll over at
all; you can only cut over, with an outage and a window
during which old artefacts cannot be read.

AND TEST THE ROTATION. An untested rotation procedure will
be attempted for the first time during an incident, which
is the worst possible moment -- so rotate on a schedule
even when nothing is wrong, because that is the only way to
know the procedure works."""),
  ("p", "<b>Key identifiers in every artefact are the design decision "
        "that makes rotation possible</b>, and <b>retrofitting them "
        "produces an outage</b> — because existing artefacts carry no "
        "identifier, so you must either try every key or accept that old "
        "data becomes unreadable. <b>It costs a few bytes per artefact "
        "and it is the difference between a routine rotation and an "
        "incident</b>, which makes it one of the highest-value early "
        "design decisions in this course."),

  ("h1", "4 &nbsp; Reviewing, and the hardware options"),
  ("ul", ["<b>Scan the repository history, not merely the working "
          "tree.</b> <b>A secret that was committed and then deleted is "
          "still in the history, in every clone, and must be "
          "rotated</b> — and the tools for this are free.",
          "<b>Grep the logs for secret-shaped strings</b> — long "
          "base64 or hex values, known prefixes, authorisation headers. "
          "<b>Secrets in logs is a large and very quiet class</b>, because "
          "logs are copied to aggregators, retained for years, and readable "
          "by a wide audience.",
          "<b>Check whether any secret is shared between "
          "environments.</b> <b>A production key present in a staging "
          "system inherits staging's security posture</b>, which is "
          "invariably weaker — and staging is where the test data and "
          "the broad access are.",
          "<b>Ask when each secret was last rotated</b>, and more "
          "pointedly <b>whether the rotation procedure has ever been "
          "executed at all</b> (&sect;3).",
          "<b>And ask who can read each secret.</b> <b>'Everyone in "
          "engineering' is the common answer and the wrong one</b> "
          "(Module 03's least privilege). <b>Rotate rather than "
          "delete:</b> once a secret has been committed, logged, or shared, "
          "<b>it must be treated as compromised</b> — removing the "
          "text does not un-disclose it, and the cost of rotating is "
          "almost always less than the cost of being wrong."]),
  ("callout", "The hardware-backed options, and what each buys",
   ["<b>A cloud key management service:</b> <b>keys never leave the "
    "service, and you call it to encrypt, decrypt, or sign</b> — "
    "<b>which turns key secrecy into an authorisation and audit problem</b> "
    "(&sect;1's architectural point), and both are tractable. <b>The "
    "default choice for most systems.</b>",
    "<b>A hardware security module:</b> the same model, with a physical "
    "tamper boundary, a stronger attestation story, and a compliance "
    "certification — <b>used where a regulator requires it, or where "
    "the key is extremely valuable (a root signing key, a certificate "
    "authority).</b>",
    "<b>A TPM or a device secure element:</b> <b>binds a key to a "
    "specific physical device</b>, so the key cannot be copied to another "
    "machine — <b>which is what makes device identity, measured boot, "
    "and full-disk encryption work</b> (Module 04 &sect;3's device "
    "posture signal).",
    "<b>And a hardware security key:</b> <b>binds a key to a physical "
    "object a person holds</b> — <b>which is Module 02 "
    "&sect;1's phishing resistance</b>, and is <b>the same mechanism at "
    "a different scale</b>: the key cannot be exfiltrated because it "
    "cannot leave the device, and the signature is bound to the origin "
    "because the device enforces it."]),
 ],
 "resources": [
   ("OWASP &mdash; Secrets Management Cheat Sheet (free)",
    "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html",
    "<b>The working reference for &sect;1 and &sect;4</b>, including the "
    "storage hierarchy and the scanning guidance."),
   ("Google &mdash; Building Secure and Reliable Systems, the key "
    "management material (free PDF)",
    "https://sre.google/books/building-secure-reliable-systems/",
    "<b>&sect;2's bootstrap problem and &sect;3's rotation</b>, from "
    "people who operate it — and the identity-rather-than-secret "
    "framing is theirs."),
   ("Meli, McNiece & Reaves &mdash; How Bad Can It Git? (free)",
    "https://www.ndss-symposium.org/ndss-paper/how-bad-can-it-git-characterizing-secret-leakage-in-public-github-repositories/",
    "<b>&sect;1's committed-secret problem, measured</b> — the scale "
    "is larger than you would guess."),
   ("NIST SP 800-57 &mdash; Recommendation for Key Management (free)",
    "https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final",
    "<b>&sect;3's rotation and lifetime guidance</b>, and the key-state "
    "model is worth borrowing even if the document is long."),
 ],
 "exercises": [
   "<b>Run a secret scanner over your repository history</b> and report "
   "what it finds.",
   "<b>For anything found, write the rotation plan</b> rather than "
   "deleting the line.",
   "<b>Grep a month of your logs</b> for secret-shaped strings.",
   "<b>Move one secret from an environment variable to a mounted "
   "file</b>, and then to a secret manager.",
   "<b>Identify your bootstrap credential</b> and say whether it is a "
   "stored secret or a platform identity.",
   "<b>Add key identifiers</b> to a system that lacks them, and report "
   "what it took.",
   "<b>Execute a key rotation</b> on a non-critical key, and time it.",
   "<b>Write the rotation runbook</b> and have someone else follow it.",
   "<b>Move one signing operation into a KMS</b> so the key never enters "
   "your process.",
   "<b>Run §4's five-point review</b> on a system you operate.",
 ],
 "selfcheck": [
   "Why is key management rather than cryptography the failure point?",
   "Give the six storage locations, worst to best, and the problem with "
   "each.",
   "Why is 'never leaves the HSM' the architectural goal, and what does "
   "it convert the problem into?",
   "State the bootstrap problem and the right answer.",
   "Why is rotation hard, and what three phases does it require?",
   "What design decision makes rotation possible?",
   "Why rotate on a schedule when nothing is wrong?",
   "Give five review questions and the rotate-rather-than-delete "
   "rule.",
   "Name four hardware-backed options and what each binds a key to.",
 ],
},

]
