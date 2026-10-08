# -*- coding: utf-8 -*-
"""CSCE 701 Cybersecurity — original course content."""

COURSE = {
    "code": "CSCE 701",
    "title": "Cybersecurity",
    "tagline": "Defending systems you did not design against adversaries "
               "who only need one way in",
    "term": "Semester 9 (with CSCE 711 and CSCE 713)",
    "prereqs": "CSCE 611 Operating Systems and CSCE 678 Distributed "
               "Systems; CSCE 606 Software Engineering for the process "
               "material; CSCE 711 runs in parallel and supplies the "
               "cryptography",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A threat model and security review of a system you "
                   "operate or built, with the controls mapped to the "
                   "threats, the residual risk stated, and a detection "
                   "plan you have tested",
    "description": [
        "<b>This is a defensive course.</b> It covers how systems fail "
        "so that you can build ones that do not, and <b>the governing "
        "asymmetry is that a defender must cover everything and an "
        "attacker needs one way in.</b> <b>Module 01 establishes that "
        "properly</b>, because every design decision in the course "
        "follows from it: defence in depth, least privilege, and "
        "assume-breach are all responses to the same arithmetic.",
        "<b>The second theme is that the interesting failures are "
        "almost never cryptographic.</b> <b>CSCE 711 covers the "
        "primitives and they are, in practice, the part that works</b> "
        "— real incidents come from misconfiguration, credential "
        "reuse, missing authorisation checks, unpatched dependencies, "
        "and people. <b>So this course spends its time where the "
        "failures are</b>, and the cryptography chapter is a short one "
        "about key management (Module 07).",
        "<b>The third is that detection matters as much as "
        "prevention.</b> <b>Assume a control will fail and ask how you "
        "would know</b> — which is Module 09, and it is the "
        "material most often missing from a security programme. "
        "<b>A system with perfect prevention and no logging cannot be "
        "investigated when the prevention turns out to have been "
        "imperfect.</b>",
        "<b>The fourth is that security is a property of a system in "
        "operation rather than of code.</b> <b>Modules 10 and 11 cover "
        "incident response and human factors</b>, because <b>a control "
        "that people route around is not a control</b>, and an "
        "organisation that cannot respond to an incident has not "
        "prepared for the one it will have.",
        "<b>And the closing position is about honest claims.</b> "
        "<b>Module 12 is about why security is hard to measure and which "
        "metrics actively mislead</b>, and <b>Module 13 is about what a "
        "security assessment can and cannot assert</b> — because "
        "'we are secure' is not a statement anyone can support, and "
        "'these threats are addressed by these controls, and these are "
        "accepted' is.",
    ],
    "outcomes": [
        "Build a threat model and defend its scope.",
        "Explain authentication's real failure modes and design "
        "around them.",
        "Design an authorisation scheme and reason about its "
        "weaknesses.",
        "Explain what transport security and network segmentation do "
        "and do not provide.",
        "Explain platform isolation mechanisms and their boundaries.",
        "Explain the browser security model and the standard "
        "vulnerability classes.",
        "Design key and secret management for a real system.",
        "Assess and harden a software supply chain.",
        "Design logging and detection that would catch a control "
        "failure.",
        "Run an incident response exercise and write a blameless "
        "post-mortem.",
        "Design controls that people will actually use.",
        "Explain why security metrics mislead and choose better "
        "ones.",
        "State what a security assessment honestly establishes.",
    ],
    "materials": [
        ("Anderson — Security Engineering, 3rd edition (free PDF)",
         "https://www.cl.cam.ac.uk/~rja14/book.html",
         "<b>The primary source, and free in full from the author.</b> "
         "The best book on this subject by a wide margin, and it is "
         "about systems and incentives rather than about tools. Modules "
         "01, 11, and 12 follow it closely."),
        ("Shostack — Threat Modeling: Designing for Security",
         "https://shostack.org/books/threat-modeling-book",
         "<b>Module 01's method.</b> The four-question framework used "
         "throughout this course comes from here. Library copy; the "
         "author's free materials cover the core."),
        ("OWASP — the Application Security Verification Standard "
         "and the Cheat Sheet Series (free)",
         "https://cheatsheetseries.owasp.org/",
         "<b>The practical reference for Modules 02–06</b> — "
         "specific, current, defensive, and maintained. The ASVS is the "
         "checklist to review a system against."),
        ("NIST SP 800-63 (digital identity) and SP 800-53 (controls) "
         "(free)",
         "https://pages.nist.gov/800-63-3/",
         "<b>Module 02's authentication guidance, free</b> — and "
         "notable for having reversed the industry's password advice on "
         "the basis of evidence, which is Module 11's point."),
        ("Google — Building Secure and Reliable Systems (free "
         "PDF)",
         "https://sre.google/books/building-secure-reliable-systems/",
         "<b>Free in full, and the reference for Modules 05, 09, and "
         "10</b> — security from the perspective of people "
         "operating large systems rather than auditing them."),
        ("Allspaw and the blameless post-mortem literature (free)",
         "https://www.etsy.com/codeascraft/blameless-postmortems-and-a-just-culture/",
         "<b>Module 10's practice.</b> Short, and it changed how the "
         "industry handles incidents — which is a human-factors "
         "result rather than a technical one."),
    ],
    "tooling": [
        "<b>A system you are authorised to examine.</b> <b>Your own "
        "machine, your own project, or a deliberately vulnerable "
        "training target</b> — and <b>nothing else, ever</b>, "
        "which is Module 01 §4's professional constraint and "
        "is not negotiable.",
        "<b>A deliberately vulnerable training environment:</b> OWASP "
        "Juice Shop, WebGoat, or a local Damn Vulnerable Web "
        "Application. <b>Free, legal, and designed for this.</b>",
        "<b>A dependency scanner</b> for Module 08 — "
        "<code>pip-audit</code>, <code>npm audit</code>, Dependabot, "
        "or Trivy. <b>Run it on your own projects and read the "
        "output.</b>",
        "<b>A log aggregator you can query</b>, even a local one, for "
        "Module 09. <b>Detection cannot be designed without somewhere "
        "to put the logs.</b>",
        "<b>A password manager and hardware security key</b>, used "
        "personally. <b>Module 02's material is far more convincing "
        "once you have lived with the controls</b>, including their "
        "friction.",
        "<b>And a written threat model template.</b> <b>The "
        "deliverable of this course is a document rather than "
        "code</b>, and the template is what makes it repeatable.",
    ],
    "projects": [
        {"title": "A threat model, defended", "after": 7,
         "brief": "Threat-model a real system you built or operate, and "
                  "map its controls to its threats.",
         "reqs": [
             "<b>A system diagram</b> with trust boundaries marked "
             "explicitly.",
             "<b>Assets, adversaries, and their capabilities</b>, "
             "written out — not a generic list.",
             "<b>At least fifteen threats</b> identified by a "
             "systematic method, not by brainstorming.",
             "<b>Each threat mapped to a control, or explicitly "
             "accepted</b>, with the acceptance justified.",
             "<b>The authentication and authorisation design reviewed "
             "against Modules 02–03.</b>",
             "<b>Three threats you cannot address</b>, with the reason "
             "and what you would need.",
         ],
         "done": [
             "<b>The trust boundaries correct</b> — which is where "
             "most threat models go wrong, and it is graded.",
             "<b>The adversary model specific</b>: a bored stranger, a "
             "motivated competitor, and an insider are different threat "
             "models with different controls.",
             "<b>Every threat either mitigated or accepted in "
             "writing</b> — an unaddressed threat that is not "
             "acknowledged is the failure mode.",
             "<b>And the three unaddressable threats stated "
             "honestly</b>, which is the part that demonstrates "
             "judgement.",
         ]},
        {"title": "Detection, and a response exercise", "after": 12,
         "brief": "Build detection for the controls you identified, "
                  "verify it fires, and run a response exercise.",
         "reqs": [
             "<b>Logging designed for three specific threats</b> from "
             "Project 1, with the fields justified.",
             "<b>A detection rule per threat</b>, with the expected "
             "false positive rate estimated.",
             "<b>A test that triggers each detection</b> — on your "
             "own system, safely.",
             "<b>The base rate computed</b> (Module 09 §3) and "
             "the alert volume predicted.",
             "<b>A tabletop incident exercise</b>, with the timeline "
             "and the decisions recorded.",
             "<b>A blameless post-mortem</b> of the exercise, in "
             "Module 10's form.",
         ],
         "done": [
             "<b>Every detection actually tested and seen to fire</b> "
             "— an untested detection is a hope, and this is the "
             "central requirement.",
             "<b>The false positive rate estimated and the alert volume "
             "computed</b>, because an alert nobody reads is not a "
             "detection (Module 09 §3).",
             "<b>The exercise surfacing at least one gap you did not "
             "anticipate</b> — which it will.",
             "<b>And the post-mortem genuinely blameless</b>, "
             "identifying system causes rather than decisions a person "
             "should have made differently.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Thinking About Security",
 "subtitle": "The asymmetry, and what follows from it.",
 "question": "What makes securing a system structurally different from "
             "building one?",
 "outcomes": [
     "State the defender's asymmetry and its consequences.",
     "Build a threat model by a systematic method.",
     "Specify an adversary rather than assuming one.",
     "Explain defence in depth, least privilege, and assume-breach "
     "as responses.",
     "State the professional and legal constraints on this work.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The asymmetry",
   "blurb": "One way in is enough."},

  {"t": "callout", "title": "The defender must cover everything; the attacker needs one way in",
   "kind": "The fact every design principle follows from",
   "body": ["<b>A system is secure only if every path is secure. It is "
            "compromised if any path is not.</b> <b>So the defender "
            "faces a conjunction and the attacker a disjunction</b>, and "
            "those are not symmetric problems.",
            "<b>Which means security does not compose like "
            "correctness.</b> <b>Two correct components compose into a "
            "correct system; two secure components can compose into an "
            "insecure one</b> — through their interaction, their "
            "shared state, or the trust each places in the other.",
            "<b>And it means the work is never finished</b>, because "
            "<b>the attacker's set of options grows as the system "
            "grows</b> while the defender's budget does not.",
            "<b>So the response is not 'be secure' but 'raise the cost, "
            "reduce the surface, and detect the failures'</b> — "
            "<b>which is what defence in depth, least privilege, and "
            "assume-breach each do</b> (Part 3)."]},

  {"t": "table", "kicker": "Consequences", "title": "What follows from the asymmetry",
   "header": ["Consequence", "Why", "What to do"],
   "widths": [2.7, 3.9, 5.4],
   "rows": [
     ["<b>Security does not compose</b>", "<b>Interactions create paths neither component has</b>", "<b>Model the system, not the parts</b>"],
     ["<b>Absence of evidence is weak</b>", "<b>You cannot test for the absence of a path</b>", "<b>Testing finds bugs, not security (CSCE 627 §07)</b>"],
     ["<b>Complexity is the enemy</b>", "<b>Surface grows faster than review capacity</b>", "<b>Reduce surface before adding controls</b>"],
     ["<b>The weakest link decides</b>", "<b>The attacker picks it</b>", "<b>Find yours before they do</b>"],
     ["<b>And prevention will fail</b>", "<b>Eventually, somewhere</b>", "<b>Design detection (M09)</b>"],
   ],
   "footnote": "<b>The second row is the most important:</b> <b>'we "
               "found no vulnerabilities' and 'there are no "
               "vulnerabilities' are completely different claims</b>, and "
               "it is CSCE 627's soundness distinction in a different "
               "setting.",
   "note": "The no-vulnerabilities-found distinction is the professional "
           "habit to instil."},

  {"t": "section", "label": "Part 2", "title": "Threat modelling",
   "blurb": "The four questions, and doing it systematically."},

  {"t": "code", "kicker": "Threat modelling", "title": "Four questions, in order",
   "lang": "text", "code": """
  1. WHAT ARE WE BUILDING?
         A diagram, with TRUST BOUNDARIES marked.
         Data flows crossing a boundary are where the
         threats are. Getting the boundaries wrong is the
         commonest failure.

  2. WHAT CAN GO WRONG?
         Enumerate systematically, not by brainstorming.
         STRIDE per data flow:
             Spoofing          -> authentication
             Tampering         -> integrity
             Repudiation       -> logging, signatures
             Information leak  -> confidentiality
             Denial of service -> availability
             Elevation         -> authorisation

  3. WHAT ARE WE GOING TO DO ABOUT IT?
         Mitigate, eliminate (remove the feature),
         transfer (insurance, a provider), or ACCEPT --
         and accepting IN WRITING is a legitimate answer.

  4. DID WE DO A GOOD JOB?
         Review it, test the mitigations, and revisit when
         the system changes.

  THE VALUE IS IN STEP 2 BEING SYSTEMATIC. A brainstorm
  finds the threats you already thought of; STRIDE per flow
  finds the ones you did not.
""",
   "caption": "<b>Systematic enumeration is the whole value</b> — "
              "and 'accept, in writing' is a real answer rather than a "
              "failure.",
   "note": "Insist on per-flow enumeration; brainstorming is the "
           "default and it misses things."},

  {"t": "callout", "title": "Specify the adversary, because different adversaries need different controls",
   "kind": "The step most often skipped",
   "body": ["<b>'An attacker' is not a threat model.</b> <b>A bored "
            "stranger with a scanner, a motivated competitor, a "
            "criminal group, a current employee, and a state actor have "
            "different capabilities, budgets, and goals.</b>",
            "<b>And the controls differ accordingly:</b> <b>rate "
            "limiting stops the first and not the last; an insider "
            "defeats your network boundary entirely</b> and requires "
            "authorisation and logging instead.",
            "<b>So write down, for each adversary: their goal, their "
            "capability, their budget, and what they already have "
            "access to.</b> <b>The last is the one that changes the "
            "model most.</b>",
            "<b>And be realistic.</b> <b>Most systems are not "
            "state-actor targets, and designing for one while leaving "
            "default credentials in place is the common failure</b> "
            "— <b>a threat model should be proportionate.</b>"]},

  {"t": "section", "label": "Part 3", "title": "The principles",
   "blurb": "Each a response to the asymmetry."},

  {"t": "bullets", "kicker": "Principles", "title": "The principles, and what each is for",
   "items": [
     "<b>Least privilege.</b> <b>Give every component the minimum "
     "access it needs</b> — so a compromise yields less. <b>It "
     "reduces the <i>consequence</i> rather than the probability.</b>",
     "",
     "<b>Defence in depth.</b> <b>Multiple independent controls, so "
     "one failure is not a compromise</b> — and <b>independence "
     "is the load-bearing word</b>: three controls sharing a flaw are "
     "one control.",
     "",
     "<b>Assume breach.</b> <b>Design for the case where an attacker "
     "is already inside</b> — which produces segmentation, "
     "short-lived credentials, and logging.",
     "",
     "<b>Fail closed.</b> <b>An error should deny rather than "
     "permit</b> — and <b>getting this wrong is a frequent and "
     "severe bug</b> (an authorisation check that errors and returns "
     "true).",
     "",
     "<b>And open design.</b> <b>Security must not depend on the "
     "design being secret</b>, because designs leak and keys can be "
     "rotated (CSCE 711 §01).",
   ],
   "footnote": "<b>Least privilege and defence in depth address "
               "different things</b> — consequence and probability "
               "— and a programme with only one of them is "
               "incomplete."},

  {"t": "section", "label": "Part 4", "title": "The constraints",
   "blurb": "What you may and may not do."},

  {"t": "callout", "title": "Authorisation is not optional, and it is the first thing",
   "kind": "The professional and legal position",
   "body": ["<b>Testing a system you are not authorised to test is "
            "unlawful in most jurisdictions</b>, regardless of intent, "
            "and <b>'I was only looking' is not a defence.</b>",
            "<b>So: your own systems, your employer's with written "
            "authorisation and a defined scope, or a deliberately "
            "vulnerable training target.</b> <b>Nothing else, "
            "ever.</b>",
            "<b>And if you find something unexpectedly</b> — in a "
            "product you use, by accident — <b>report it through a "
            "coordinated disclosure process and stop testing</b>, "
            "rather than investigating further.",
            "<b>This course teaches how systems fail so that you can "
            "build ones that do not.</b> <b>Every technique here has a "
            "defensive purpose, and the material is scoped to "
            "that</b> — which is the right scope for an engineer rather "
            "than a limitation."]},

  {"t": "callout", "title": "Where this course goes",
   "kind": "The shape of the semester",
   "body": ["<b>Modules 02–06: the controls.</b> "
            "Authentication, authorisation, network, platform, and web "
            "— <b>which is where the real failures are</b>, and the "
            "ordering is by how often each appears in an incident "
            "report.",
            "<b>Modules 07–08: secrets and supply "
            "chain.</b> <b>Key management is the hard part of "
            "cryptography</b> (CSCE 711 supplies the rest) <b>and "
            "dependencies are the fastest-growing attack surface.</b>",
            "<b>Modules 09–11: detection, response, "
            "and people.</b> <b>What you do when prevention "
            "fails</b> — and it will.",
            "<b>Modules 12–13: measurement and honest "
            "claims</b> — <b>which is harder here than in any other "
            "course in the program.</b>"]},
 ],
 "takeaways": [
   "The defender faces a conjunction and the attacker a disjunction, which "
   "is why security does not compose the way correctness does.",
   "'We found no vulnerabilities' and 'there are no vulnerabilities' are "
   "completely different claims.",
   "Threat modelling's value is in systematic enumeration — STRIDE "
   "per data flow finds the threats a brainstorm misses.",
   "'An attacker' is not a threat model: specify the goal, capability, "
   "budget, and existing access of each adversary.",
   "Least privilege reduces consequence and defence in depth reduces "
   "probability, so a programme needs both — and the controls must be "
   "independent.",
   "Authorisation is the first requirement for any security testing, and "
   "it is not negotiable.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The asymmetry"),
  ("callout", "The defender must cover everything; the attacker needs one "
              "way in",
   ["<b>A system is secure only if every path into it is secure. It is "
    "compromised if any single path is not.</b> <b>So the defender faces "
    "a conjunction over all paths and the attacker faces a disjunction</b> "
    "— and those are structurally different problems, with different "
    "effort profiles.",
    "<b>Which means security does not compose the way correctness "
    "does.</b> <b>Two correct components compose into a correct system; "
    "two secure components can compose into an insecure one</b> — "
    "through their interaction, through shared state, or through the trust "
    "each places in the other. <b>So a component-by-component review is "
    "not a system review</b>, which is why Module 01's threat model "
    "works on the system diagram.",
    "<b>And it means the work is never finished</b>, because <b>the "
    "attacker's set of available paths grows as the system grows</b> "
    "— every feature, dependency, integration, and configuration "
    "option adds to it — <b>while the defender's review budget does "
    "not.</b>",
    "<b>So the response is not 'be secure' but 'raise the attacker's "
    "cost, reduce the surface, and detect the failures'</b> — "
    "<b>which is precisely what defence in depth, least privilege, and "
    "assume-breach each do</b> (&sect;3). <b>Every principle in this "
    "course is a response to this one paragraph.</b>"]),
  ("table", ["Consequence", "Why it follows", "What to do about it"],
   [["<b>Security does not compose</b>",
     "<b>Component interactions create paths that neither component has "
     "on its own.</b>",
     "<b>Model the system and its trust boundaries, not the parts</b> "
     "(&sect;2)."],
    ["<b>Absence of evidence is weak evidence</b>",
     "<b>You cannot test for the absence of an attack path</b>, only for "
     "the presence of specific ones.",
     "<b>Testing finds bugs rather than establishing security</b> "
     "— CSCE 627 Module 07 &sect;3's testing asymmetry, and "
     "see the note."],
    ["<b>Complexity is the enemy</b>",
     "<b>Attack surface grows faster than review capacity</b>, and "
     "nobody reviews a configuration space.",
     "<b>Reduce the surface before adding controls</b> — removing a "
     "feature is the strongest mitigation available."],
    ["<b>The weakest link decides the outcome</b>",
     "<b>The attacker chooses which link to attack, and will choose the "
     "weakest.</b>",
     "<b>Find yours before they do</b>, which means looking at the "
     "boring parts rather than the interesting ones."],
    ["<b>And prevention will fail</b>",
     "<b>Eventually, somewhere, for reasons you did not anticipate.</b>",
     "<b>Design detection on the assumption that it has already "
     "happened</b> (Module 09)."]],
   [0.22, 0.33, 0.45]),
  ("p", "<b>The second row is the most important, and it is the "
        "professional habit to acquire:</b> <b>'we found no "
        "vulnerabilities' and 'there are no vulnerabilities' are "
        "completely different claims</b>, and only the first is ever "
        "supportable. <b>It is CSCE 627 Module 12's soundness "
        "distinction in a different setting</b> — a security review "
        "is an incomplete search, and reporting it as a clean bill of "
        "health is the error that makes assessments useless."),

  ("h1", "2 &nbsp; Threat modelling"),
  ("code", """1. WHAT ARE WE BUILDING?
       A diagram, with TRUST BOUNDARIES marked explicitly.
       Data flows that cross a boundary are where the
       threats are. Getting the boundaries wrong is the
       commonest failure in a threat model, and it is the
       graded part of this course's first project.

2. WHAT CAN GO WRONG?
       Enumerate SYSTEMATICALLY, not by brainstorming.
       STRIDE, applied to each data flow:
           Spoofing           -> authentication
           Tampering          -> integrity
           Repudiation        -> logging, signatures
           Information leak   -> confidentiality
           Denial of service  -> availability
           Elevation of priv. -> authorisation

3. WHAT ARE WE GOING TO DO ABOUT IT?
       Mitigate, eliminate (remove the feature entirely),
       transfer (to a provider or an insurer), or ACCEPT --
       and accepting IN WRITING is a legitimate answer.

4. DID WE DO A GOOD JOB?
       Review it, test that the mitigations work, and
       revisit it when the system changes.

THE VALUE IS IN STEP 2 BEING SYSTEMATIC. A brainstorm finds
the threats you had already thought of; STRIDE applied to
every flow finds the ones you had not."""),
  ("callout", "Specify the adversary, because different adversaries need "
              "different controls",
   ["<b>'An attacker' is not a threat model.</b> <b>A bored stranger "
    "running a scanner, a motivated competitor, an organised criminal "
    "group, a current employee, a departing employee, and a state actor "
    "have entirely different capabilities, budgets, patience, and "
    "goals.</b>",
    "<b>And the controls differ accordingly:</b> <b>rate limiting stops "
    "the first and not the last; an insider defeats your network boundary "
    "entirely</b> (Module 04 &sect;4) <b>and must be addressed by "
    "authorisation, separation of duties, and logging instead</b> "
    "(Module 03).",
    "<b>So write down, for each adversary you care about: their goal, "
    "their capability, their budget, and what access they already "
    "have.</b> <b>The last is the one that changes the model most</b> "
    "— an adversary who already holds a valid credential is a "
    "different problem from one who does not.",
    "<b>And be realistic about which adversaries apply.</b> <b>Most "
    "systems are not state-actor targets, and designing against one while "
    "leaving default credentials in place is the common and embarrassing "
    "failure</b> — <b>a threat model should be proportionate to the "
    "assets and the plausible adversaries</b>, and an implausible one "
    "consumes the budget that the plausible one needed."]),

  ("break",),
  ("h1", "3 &nbsp; The principles"),
  ("ul", ["<b>Least privilege.</b> <b>Give every component, process, "
          "and person the minimum access needed to do their job</b> "
          "— so that a compromise yields less. <b>It reduces the "
          "<i>consequence</i> of a breach rather than its "
          "probability</b>, which is worth being clear about because the "
          "two are frequently conflated.",
          "<b>Defence in depth.</b> <b>Multiple independent controls, "
          "so that one failing is not a compromise</b> — and "
          "<b>'independent' is the load-bearing word</b>: three controls "
          "that all depend on the same identity provider, or all share an "
          "implementation flaw, are one control wearing three hats.",
          "<b>Assume breach.</b> <b>Design for the case where an "
          "attacker is already inside the perimeter</b> — which "
          "produces network segmentation (Module 04 &sect;3), "
          "short-lived credentials (Module 07), and comprehensive "
          "logging (Module 09). <b>It is the principle that most "
          "changes an architecture.</b>",
          "<b>Fail closed.</b> <b>An error condition should deny "
          "access rather than permit it</b> — and <b>getting this "
          "wrong is a frequent and severe class of bug</b>: an "
          "authorisation check that throws an exception and is caught by a "
          "handler returning success, or a policy evaluation that defaults "
          "to allow when the policy service is unreachable.",
          "<b>And open design.</b> <b>Security must not depend on the "
          "design being secret</b>, because designs leak, are reverse "
          "engineered, and are discussed by former employees — "
          "<b>whereas keys can be rotated</b> (CSCE 711 Module 01 "
          "&sect;2's Kerckhoffs principle). <b>Least privilege and "
          "defence in depth address different things</b> — "
          "consequence and probability — <b>and a programme with "
          "only one of them is incomplete.</b>"]),

  ("h1", "4 &nbsp; The constraints"),
  ("callout", "Authorisation is not optional, and it is the first thing",
   ["<b>Testing a system you are not authorised to test is unlawful in "
    "most jurisdictions, regardless of your intent</b>, and <b>'I was "
    "only looking' is not a defence</b> — unauthorised access "
    "statutes generally turn on access rather than on harm.",
    "<b>So: your own systems; your employer's systems with written "
    "authorisation and a defined scope; a bug bounty programme within its "
    "published rules; or a deliberately vulnerable training target "
    "designed for the purpose.</b> <b>Nothing else, ever</b>, and the "
    "scope matters as much as the permission.",
    "<b>And if you find something unexpectedly</b> — in a product "
    "you use, by accident, in the course of normal work — "
    "<b>report it through a coordinated disclosure process and stop "
    "testing immediately</b> rather than investigating further to "
    "characterise it. <b>The instinct to confirm the finding is exactly "
    "the instinct to resist.</b>",
    "<b>This course teaches how systems fail so that you can build ones "
    "that do not.</b> <b>Every technique here has a defensive purpose, "
    "and the material is scoped to that</b> — which is the right "
    "scope for an engineer who will spend their career defending rather "
    "than attacking, and is not a limitation on what you can learn to "
    "do."]),
  ("callout", "Where this course goes",
   ["<b>Modules 02 through 06 are the controls.</b> Authentication, "
    "authorisation, network security, platform isolation, and web "
    "security — <b>which is where the real failures are</b>, and "
    "<b>the ordering is roughly by how often each appears as the root "
    "cause in a published incident report.</b>",
    "<b>Modules 07 and 08 are secrets and the supply chain.</b> <b>Key "
    "management is the genuinely hard part of applied cryptography</b> "
    "(CSCE 711 supplies the primitives, which work) <b>and "
    "dependencies are the fastest-growing attack surface in modern "
    "software.</b>",
    "<b>Modules 09 through 11 are detection, response, and people.</b> "
    "<b>What you do when prevention fails</b> — and it will, which "
    "is &sect;1's last row.",
    "<b>Modules 12 and 13 are measurement and honest claims</b> — "
    "<b>which is harder in this subject than in any other course in the "
    "program</b>, because the thing you want to measure is the absence of "
    "something and &sect;1's second row says you cannot."]),
 ],
 "resources": [
   ("Anderson &mdash; Security Engineering, chapters 1–3 (free "
    "PDF)",
    "https://www.cl.cam.ac.uk/~rja14/book.html",
    "<b>The asymmetry, the principles, and the economics</b> — free "
    "in full, and the first chapter is the best framing of this subject "
    "in print."),
   ("Shostack &mdash; Threat Modeling, and the free four-question "
    "materials",
    "https://shostack.org/books/threat-modeling-book",
    "<b>&sect;2's method</b>, including STRIDE per element and the "
    "trust-boundary guidance."),
   ("Saltzer & Schroeder &mdash; The Protection of Information in "
    "Computer Systems (free)",
    "https://www.cs.virginia.edu/~evans/cs551/saltzer/",
    "<b>&sect;3's principles, in the 1975 original</b> — least "
    "privilege, fail-safe defaults, and open design were all stated "
    "here, and the paper reads as current."),
   ("OWASP &mdash; Threat Modeling Cheat Sheet (free)",
    "https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html",
    "<b>&sect;2 as a working procedure</b>, with the common mistakes "
    "listed."),
 ],
 "exercises": [
   "<b>Diagram a system you built</b> and mark every trust boundary. "
   "Count the data flows crossing one.",
   "<b>Apply STRIDE to each crossing flow</b> and record every threat, "
   "however unlikely.",
   "<b>Compare against a list you produce by brainstorming</b> and report "
   "how many the systematic method found that the brainstorm did not.",
   "<b>Write adversary profiles</b> for three plausible adversaries of "
   "your system, with goal, capability, budget, and existing access.",
   "<b>Identify a control that stops one adversary and not another</b>, "
   "and say why.",
   "<b>For each threat, decide: mitigate, eliminate, transfer, or "
   "accept</b> — and write the acceptances down.",
   "<b>Find two of your controls that are not independent</b>, and say "
   "what they share.",
   "<b>Find a place where your system fails open</b> and fix it.",
   "<b>Look up the unauthorised-access law in your jurisdiction</b> and "
   "summarise what it prohibits.",
   "<b>Find the coordinated disclosure policy</b> for a product you use, "
   "and note whether one exists.",
 ],
 "selfcheck": [
   "State the asymmetry and explain why security does not compose.",
   "Why are 'found no vulnerabilities' and 'there are none' different "
   "claims?",
   "Give five consequences of the asymmetry.",
   "Give the four threat-modelling questions and the STRIDE "
   "categories.",
   "Why must enumeration be systematic?",
   "Why is 'an attacker' not a threat model, and what should you write "
   "instead?",
   "Name five principles and say what each addresses.",
   "Which reduce probability and which reduce consequence?",
   "What are the constraints on security testing, and what do you do on "
   "an accidental finding?",
 ],
},

]

for _b in ("c701_b2", "c701_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
