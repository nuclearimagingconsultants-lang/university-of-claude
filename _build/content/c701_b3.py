# -*- coding: utf-8 -*-
"""CSCE 701 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "The Supply Chain",
 "subtitle": "Securing what you did not write.",
 "question": "Your code is 5% yours. What about the other 95%?",
 "outcomes": [
     "Explain the dependency attack surface and its growth.",
     "Explain the build pipeline as a target.",
     "Explain provenance, signing, and reproducible builds.",
     "Assess a project's dependency risk.",
     "Design a response to a dependency advisory.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The surface",
   "blurb": "Transitive, and larger than you think."},

  {"t": "callout", "title": "Your dependency tree is code you run with your privileges and did not review",
   "kind": "The plain statement",
   "body": ["<b>A typical application has tens of direct dependencies "
            "and hundreds to thousands transitively</b> — and "
            "<b>every one of them runs with your process's "
            "privileges.</b>",
            "<b>So the trust decision is not 'do I trust this "
            "library' but 'do I trust the transitive closure, and "
            "everyone who can publish to it'</b> — which is a much "
            "larger and less answerable question.",
            "<b>And install-time code execution makes it worse</b>: "
            "<b>a package whose install script runs is code executing on "
            "your build machine before any review</b>, which is why "
            "install scripts are the highest-risk feature in a package "
            "manager.",
            "<b>Which means the first control is reducing the "
            "tree.</b> <b>A dependency you removed cannot be "
            "compromised</b>, and <b>Module 01 §1's "
            "reduce-the-surface principle applies here more directly "
            "than anywhere else.</b>"]},

  {"t": "table", "kicker": "Risks", "title": "The dependency risks, and what each needs",
   "header": ["Risk", "Mechanism", "Control"],
   "widths": [2.7, 4.1, 5.1],
   "rows": [
     ["<b>Known vulnerability</b>", "<b>A published advisory you have not acted on</b>", "<b>Scanning plus a patch cadence</b>"],
     ["<b>Abandoned package</b>", "<b>Nobody will fix the next one</b>", "<b>Check maintenance before adopting</b>"],
     ["<b>Maintainer handover</b>", "<b>A new publisher inherits your trust</b>", "<b>Pin, review diffs, watch ownership</b>"],
     ["<b>Typosquatting</b>", "<b>A near-name package installed by mistake</b>", "<b>Lockfiles; verify names on adoption</b>"],
     ["<b>Build-time execution</b>", "<b>Install scripts run before review</b>", "<b>Disable scripts; build in a sandbox</b>"],
   ],
   "footnote": "<b>The maintainer-handover row is the structurally "
               "hardest</b> — trust was placed in a person, and "
               "package managers mostly do not surface a change of "
               "publisher.",
   "note": "Handover is the risk with the fewest good controls."},

  {"t": "section", "label": "Part 2", "title": "The build",
   "blurb": "A privileged machine that touches everything."},

  {"t": "callout", "title": "The build system is the highest-value target in most organisations",
   "kind": "And it is usually the least hardened",
   "body": ["<b>It has credentials to the artefact registry, to "
            "production, and to the source repository</b> — and "
            "<b>its output is trusted and deployed without review.</b>",
            "<b>So compromising the build compromises everything it "
            "produces</b>, for as long as nobody notices — which is "
            "a far better position than compromising one server.",
            "<b>And it is typically less hardened than production</b>, "
            "because it is treated as developer infrastructure rather "
            "than as a production system holding production "
            "credentials.",
            "<b>So: treat the build as production.</b> <b>Least "
            "privilege on its credentials, ephemeral runners, no "
            "secrets in logs, review of pipeline changes, and "
            "segmentation from developer workstations</b> "
            "(Module 04 §2)."]},

  {"t": "code", "kicker": "Hardening", "title": "The build controls that matter most",
   "lang": "text", "code": """
  EPHEMERAL RUNNERS
      a fresh machine per build, destroyed after. A
      compromise does not persist into the next build.

  SCOPED, SHORT-LIVED CREDENTIALS
      the build gets a token for THIS artefact, valid for
      minutes -- not a standing deploy key.

  PINNED, VERIFIED INPUTS
      lockfiles with hashes, and pinned tool versions.
      "latest" means "whatever was published since you
      last looked".

  SEPARATE THE BUILD FROM THE RELEASE
      building is untrusted work on untrusted input;
      signing and publishing is privileged. Different
      stages, different credentials.

  AND REVIEW PIPELINE CHANGES LIKE CODE
      a pipeline definition is code with production
      credentials, and it is frequently exempt from review.
""",
   "caption": "<b>Separating build from release is the structural "
              "one</b> — it means compromising the build does not "
              "give you a signature.",
   "note": "The build/release split is the highest-leverage change."},

  {"t": "section", "label": "Part 3", "title": "Provenance",
   "blurb": "Knowing what you shipped and where it came from."},

  {"t": "bullets", "kicker": "Provenance", "title": "The mechanisms, and what each answers",
   "items": [
     "<b>A software bill of materials.</b> <b>Answers 'what is in "
     "this artefact'</b> — which is the question you cannot answer "
     "during an advisory response without one.",
     "",
     "<b>Artefact signing.</b> <b>Answers 'did this come from my "
     "build'</b> — and it is only as good as the key handling "
     "(Module 07).",
     "",
     "<b>Build attestation.</b> <b>Answers 'what source and what "
     "steps produced this'</b>, signed by the build platform rather "
     "than by a human.",
     "",
     "<b>Reproducible builds.</b> <b>Answers 'can anyone else get "
     "the same bytes from the same source'</b> — which makes a "
     "compromised build detectable by a third party.",
     "",
     "<b>And an artefact registry you control</b>, so that what you "
     "deploy is what you built rather than what a public registry "
     "currently serves.",
   ],
   "footnote": "<b>Reproducibility is the strongest of these</b> "
               "because it removes the need to trust the builder "
               "— and it is the hardest, because timestamps and "
               "paths leak into outputs."},

  {"t": "callout", "title": "The SBOM's value is entirely in the response, not the document",
   "kind": "Why it matters",
   "body": ["<b>An advisory lands on a library at 9am. The question "
            "is which of your hundred services contain it, at which "
            "version.</b>",
            "<b>Without an inventory that takes days of grep and "
            "guesswork</b>, during which you do not know your "
            "exposure — <b>which is exactly the position every "
            "organisation was in during the major logging-library "
            "advisory.</b>",
            "<b>With one it is a query.</b> <b>And the value is the "
            "<i>query time</i> rather than the compliance "
            "artefact</b>, which is why an SBOM generated and filed "
            "unread is wasted effort.",
            "<b>So the test is:</b> <b>can you answer 'where is "
            "version X of library Y deployed' in under five "
            "minutes?</b> <b>If not, the inventory does not work "
            "regardless of what documents exist.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Responding",
   "blurb": "What to do when an advisory lands."},

  {"t": "bullets", "kicker": "Response", "title": "The advisory response, in order",
   "items": [
     "<b>1 · Determine exposure.</b> <b>Which artefacts, which "
     "versions, which are reachable</b> — and 'present in the tree' "
     "is not 'reachable from your code'.",
     "",
     "<b>2 · Assess exploitability in <i>your</i> "
     "configuration.</b> <b>Most advisories do not apply to most "
     "users</b>, and triaging on the severity score alone wastes the "
     "budget.",
     "",
     "<b>3 · Mitigate if you cannot patch immediately</b> "
     "— configuration change, feature disable, or a filter in "
     "front.",
     "",
     "<b>4 · Patch, and verify the patched version is actually "
     "deployed</b> — which is where responses quietly fail.",
     "",
     "<b>5 · And record what you decided and why</b>, because "
     "the same library will have another advisory.",
   ],
   "footnote": "<b>Step 2 is where judgement earns its keep:</b> a "
               "programme that patches every advisory at the same "
               "urgency will exhaust itself and miss the one that "
               "mattered."},

  {"t": "callout", "title": "The honest assessment of dependency security",
   "kind": "Closing",
   "body": ["<b>You cannot review your dependency tree and you cannot "
            "do without it</b> — writing everything yourself trades "
            "a supply chain risk for a far larger quantity of your own "
            "bugs.",
            "<b>So the realistic programme is:</b> <b>reduce the tree, "
            "pin and verify, scan continuously, maintain an inventory "
            "you can query, harden the build, and respond with "
            "judgement.</b>",
            "<b>And accept residual risk explicitly</b> "
            "(Module 01 §2) — <b>'we depend on 1,400 "
            "packages and review none of them' is a true statement that "
            "belongs in the threat model.</b>",
            "<b>Which is more useful than a control nobody "
            "believes</b> — <b>an accepted risk gets revisited, and an "
            "unacknowledged one does not.</b>"]},
 ],
 "takeaways": [
   "Your dependency tree is code running with your privileges that you did "
   "not review, so the trust decision covers the transitive closure and "
   "everyone who can publish to it.",
   "Install-time script execution is the highest-risk package manager "
   "feature, because it runs before any review.",
   "The build system holds production credentials and produces trusted "
   "output, which makes it the highest-value target and usually the least "
   "hardened.",
   "Separating build from release is the structural control: compromising "
   "the build then does not yield a signature.",
   "An SBOM's value is the query time during an advisory, not the "
   "document — the test is whether you can locate a library version "
   "in five minutes.",
   "Most advisories do not apply to most users, so triaging on severity "
   "score alone exhausts the budget and misses the one that mattered.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The dependency surface"),
  ("callout", "Your dependency tree is code you run with your privileges "
              "and did not review",
   ["<b>A typical application has tens of direct dependencies and "
    "hundreds to several thousand transitively</b> — and <b>every "
    "one of them executes with your process's full privileges</b>, with "
    "access to your memory, your filesystem, and your network position.",
    "<b>So the trust decision is not 'do I trust this library' but 'do I "
    "trust the entire transitive closure, and every person who can "
    "publish an update to any part of it'</b> — which is a much "
    "larger and considerably less answerable question, and is not the "
    "question anyone asks when adding a package.",
    "<b>And install-time code execution makes it worse.</b> <b>A package "
    "whose install script runs is code executing on your build machine "
    "before any review, test, or human inspection</b> — which is why "
    "install scripts are the single highest-risk feature in a package "
    "manager, and why disabling them is a cheap and effective control.",
    "<b>Which means the first control is reducing the tree.</b> <b>A "
    "dependency you removed cannot be compromised</b>, and "
    "<b>Module 01 &sect;1's reduce-the-surface principle applies here "
    "more directly than anywhere else in the course</b> — the "
    "question 'do we need this package for the three functions we use' "
    "has a measurable security answer."]),
  ("table", ["Risk", "The mechanism", "The control"],
   [["<b>Known vulnerability</b>",
     "<b>A published advisory against a version you are running, which "
     "you have not acted on.</b>",
     "<b>Continuous scanning plus an actual patch cadence</b> — the "
     "scanning is easy and the cadence is the hard part."],
    ["<b>Abandoned package</b>",
     "<b>Nobody will fix the next vulnerability, because nobody is "
     "maintaining it.</b>",
     "<b>Check maintenance activity before adopting</b>, and treat "
     "abandonment as a reason to migrate rather than a neutral fact."],
    ["<b>Maintainer handover</b>",
     "<b>A new publisher inherits the trust you placed in the previous "
     "one</b>, including the right to push to every system that depends "
     "on it.",
     "<b>Pin versions, review diffs on upgrade, and watch for ownership "
     "changes</b> — see the note."],
    ["<b>Typosquatting and confusion</b>",
     "<b>A near-identical package name installed by mistake, or a public "
     "name shadowing an internal one.</b>",
     "<b>Lockfiles with hashes, scoped internal registries, and verifying "
     "the name on first adoption.</b>"],
    ["<b>Build-time execution</b>",
     "<b>Install and post-install scripts run on the build machine "
     "before anything is reviewed.</b>",
     "<b>Disable install scripts where the ecosystem allows, and build in "
     "an ephemeral sandbox</b> (&sect;2)."]],
   [0.22, 0.36, 0.42]),
  ("p", "<b>The maintainer-handover row is the structurally hardest.</b> "
        "<b>The trust was placed in a person and the package manager "
        "mostly does not surface a change of publisher</b> — so a "
        "transfer of a widely-depended-upon package to a new owner is "
        "invisible to the thousands of projects affected. <b>There is no "
        "good control available to a consumer beyond pinning and reading "
        "diffs</b>, which does not scale, and saying so is more useful "
        "than pretending otherwise."),

  ("h1", "2 &nbsp; The build"),
  ("callout", "The build system is the highest-value target in most "
              "organisations",
   ["<b>It holds credentials to the artefact registry, frequently to "
    "production, and to the source repository</b> — and <b>its "
    "output is trusted and deployed without further review</b>, which is "
    "the whole point of a build system.",
    "<b>So compromising the build compromises everything it "
    "produces</b>, for as long as nobody notices — <b>which is a "
    "far better position for an attacker than compromising any single "
    "server</b>, and is why this is where sophisticated attacks go.",
    "<b>And it is typically less hardened than production</b>, because "
    "<b>it is treated as developer infrastructure rather than as a "
    "production system that happens to hold production "
    "credentials</b> — which is a categorisation error with large "
    "consequences.",
    "<b>So: treat the build as production.</b> <b>Least privilege on "
    "its credentials, ephemeral runners, no secrets in build logs, review "
    "of pipeline changes, and network segmentation from developer "
    "workstations</b> (Module 04 &sect;2) — and the segmentation "
    "matters because a phished developer should not reach the builder."]),
  ("code", """EPHEMERAL RUNNERS
    a fresh machine or container per build, destroyed
    afterwards. A compromise does not persist into the
    next build, which removes the attacker's foothold.

SCOPED, SHORT-LIVED CREDENTIALS
    the build receives a token for THIS artefact, valid
    for minutes -- not a standing deploy key with broad
    rights (Module 07 section 2's platform identity).

PINNED, VERIFIED INPUTS
    lockfiles with content hashes, and pinned versions of
    the tools themselves. "latest" means "whatever was
    published since you last looked".

SEPARATE THE BUILD FROM THE RELEASE
    building is untrusted work on untrusted input;
    signing and publishing is privileged. Different
    stages, different credentials, different machines.

AND REVIEW PIPELINE CHANGES LIKE CODE
    a pipeline definition is code with production
    credentials, and it is frequently exempt from the
    review that ordinary code requires."""),
  ("p", "<b>Separating build from release is the structural one.</b> "
        "<b>It means that compromising the build machine does not yield a "
        "signature</b> — the attacker can produce a malicious "
        "artefact and cannot get it signed, so the signature verification "
        "at deploy time catches it. <b>Which converts a total compromise "
        "into a detected attempt</b>, and it is the highest-leverage "
        "change in this list."),

  ("break",),
  ("h1", "3 &nbsp; Provenance"),
  ("ul", ["<b>A software bill of materials.</b> <b>Answers 'what is "
          "actually in this artefact'</b> — which is precisely the "
          "question you cannot answer during an advisory response without "
          "one (see the callout).",
          "<b>Artefact signing.</b> <b>Answers 'did this come from my "
          "build'</b> — and <b>it is only as good as the key "
          "handling</b> (Module 07), so a signing key on the build "
          "machine provides much less than it appears to (&sect;2).",
          "<b>Build attestation.</b> <b>Answers 'what source revision "
          "and what build steps produced this artefact'</b>, signed by the "
          "build platform rather than by a human — which is what "
          "SLSA and similar frameworks specify.",
          "<b>Reproducible builds.</b> <b>Answers 'can an independent "
          "party obtain byte-identical output from the same "
          "source'</b> — <b>which makes a compromised build "
          "detectable by a third party rather than only by the "
          "builder.</b>",
          "<b>And an artefact registry you control</b>, so that what "
          "you deploy is what you built and verified rather than whatever "
          "a public registry currently serves under that name. "
          "<b>Reproducibility is the strongest of these, because it "
          "removes the need to trust the builder at all</b> — and it "
          "is the hardest, because timestamps, build paths, parallelism, "
          "and locale all leak into outputs and each has to be hunted "
          "down."]),
  ("callout", "The SBOM's value is entirely in the response, not the "
              "document",
   ["<b>An advisory lands on a widely-used library at nine in the "
    "morning. The question you must answer is which of your hundred "
    "services contain it, at which version, and which of those are "
    "exposed.</b>",
    "<b>Without an inventory, that takes days of grepping and "
    "guesswork</b>, during which <b>you do not know your own "
    "exposure</b> — <b>which is exactly the position nearly every "
    "organisation found itself in during the major logging-library "
    "advisory</b>, and the inventory gap was the story rather than the "
    "vulnerability.",
    "<b>With one, it is a query.</b> <b>And the value is the <i>query "
    "time</i> rather than the compliance artefact</b> — which is why "
    "an SBOM generated at build time, filed, and never read is wasted "
    "effort that satisfies an auditor and helps nobody.",
    "<b>So the test is simple:</b> <b>can you answer 'where is version "
    "X of library Y deployed right now' in under five minutes?</b> "
    "<b>If not, your inventory does not work, regardless of what "
    "documents exist</b> — and that is the thing to measure rather "
    "than SBOM coverage."]),

  ("h1", "4 &nbsp; Responding to an advisory"),
  ("ul", ["<b>1 &middot; Determine exposure.</b> <b>Which artefacts, "
          "which versions, and which of those are actually "
          "reachable</b> — and <b>'present in the dependency tree' "
          "is not the same as 'reachable from your code'</b>, which is "
          "what reachability analysis tools exist to distinguish.",
          "<b>2 &middot; Assess exploitability in <i>your</i> "
          "configuration.</b> <b>Most advisories do not apply to most "
          "users</b> — the vulnerable feature is not enabled, the "
          "input is not attacker-controlled, the component is not "
          "network-reachable — and <b>triaging on the published "
          "severity score alone wastes the budget</b>.",
          "<b>3 &middot; Mitigate if you cannot patch immediately</b> "
          "— a configuration change, disabling the affected feature, "
          "or a filter in front of the vulnerable path. <b>A mitigation "
          "today beats a patch next week.</b>",
          "<b>4 &middot; Patch, and then verify that the patched version "
          "is actually deployed everywhere</b> — <b>which is where "
          "responses quietly fail</b>: the fix is merged, one service is "
          "not redeployed, and the inventory still shows the old version "
          "six months later.",
          "<b>5 &middot; And record what you decided and why</b>, "
          "because <b>the same library will have another advisory</b> and "
          "the analysis of whether the feature is enabled is reusable. "
          "<b>Step 2 is where judgement earns its keep:</b> a programme "
          "that patches every advisory at the same urgency will exhaust "
          "itself and miss the one that mattered."]),
  ("callout", "The honest assessment of dependency security",
   ["<b>You cannot review your dependency tree, and you cannot do "
    "without it</b> — writing everything yourself trades a supply "
    "chain risk for a far larger quantity of your own bugs, which is a "
    "worse trade in almost every case.",
    "<b>So the realistic programme is:</b> <b>reduce the tree where you "
    "can, pin and verify, scan continuously, maintain an inventory you "
    "can actually query, harden the build (&sect;2), and respond with "
    "judgement rather than by severity score (&sect;4).</b>",
    "<b>And accept the residual risk explicitly</b> (Module 01 "
    "&sect;2's fourth option) — <b>'we depend on 1,400 packages "
    "and review none of them' is a true statement that belongs in the "
    "threat model</b> rather than being left unsaid.",
    "<b>Which is more useful than a control nobody believes in.</b> "
    "<b>An accepted risk gets revisited when circumstances change, and an "
    "unacknowledged one does not</b> — which is the whole argument "
    "for writing acceptances down."]),
 ],
 "resources": [
   ("SLSA &mdash; Supply-chain Levels for Software Artifacts (free)",
    "https://slsa.dev/",
    "<b>&sect;2 and &sect;3 as a graded framework</b> — the levels "
    "are a usable roadmap rather than a checklist, and the build/release "
    "separation is explicit."),
   ("Ohm et al. &mdash; Backstabber's Knife Collection (free)",
    "https://arxiv.org/abs/2005.09535",
    "<b>&sect;1's risks, from real incidents</b> — a systematic "
    "study of malicious package attacks and the mechanisms they used."),
   ("The Reproducible Builds project (free)",
    "https://reproducible-builds.org/",
    "<b>&sect;3's strongest mechanism</b>, with the practical guidance on "
    "the sources of non-determinism."),
   ("OpenSSF &mdash; Scorecard and the Concise Guides (free)",
    "https://openssf.org/",
    "<b>&sect;1's adoption checks, automated</b> — maintenance "
    "activity, review practices, and signing, scored per dependency."),
 ],
 "exercises": [
   "<b>Count your transitive dependencies</b> and compare against your "
   "direct ones.",
   "<b>Find the three largest</b> and ask what fraction of each you "
   "actually use.",
   "<b>List every package whose install scripts run</b> during your "
   "build.",
   "<b>Disable install scripts</b> and report what breaks.",
   "<b>Enumerate what credentials your build system holds</b>, and what "
   "each can reach.",
   "<b>Check whether your build runs on ephemeral or persistent "
   "machines.</b>",
   "<b>Generate an SBOM</b> and then time yourself answering 'where is "
   "library Y version X deployed'.",
   "<b>Pick a past advisory</b> and run §4's five steps against your "
   "own system retrospectively.",
   "<b>Find one advisory that does not apply to you</b> and write down "
   "why.",
   "<b>Write your dependency risk acceptance</b> for the threat "
   "model.",
 ],
 "selfcheck": [
   "Why is a dependency tree a security concern, and what is the trust "
   "decision really about?",
   "Why are install scripts the highest-risk feature?",
   "Name five dependency risks and the control for each.",
   "Which risk has the fewest good controls, and why?",
   "Why is the build system the highest-value target?",
   "Name five build controls and say which is structural.",
   "Name five provenance mechanisms and what each answers.",
   "Why is reproducibility the strongest, and why is it hardest?",
   "What is the real test of an SBOM?",
   "Give the five-step advisory response and say where judgement "
   "matters.",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Detection",
 "subtitle": "How you would know.",
 "question": "A control has failed. What tells you?",
 "outcomes": [
     "Design logging that answers security questions.",
     "Explain the base rate problem and its consequence for "
     "alerting.",
     "Build detections for specific threats and test them.",
     "Explain what to centralise and what to retain.",
     "Explain why most detection programmes fail.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Logging",
   "blurb": "Designed backwards, from the question."},

  {"t": "callout", "title": "Log what you would need to answer the question, not what is convenient to emit",
   "kind": "The design direction",
   "body": ["<b>Most logging is written forwards — emit what the "
            "code knows at that point</b> — and is then useless "
            "during an investigation.",
            "<b>So design backwards:</b> <b>write the questions you "
            "will need to answer, and then the fields required to answer "
            "them.</b> 'Which accounts did this address touch?' needs "
            "both in every event.",
            "<b>The security-relevant events are a short list:</b> "
            "<b>authentication attempts, authorisation denials "
            "(Module 03 §3), privilege changes, configuration "
            "changes, secret access, and administrative actions.</b>",
            "<b>And every event needs: who, what, when, from where, "
            "and the outcome</b> — <b>the outcome field is the one "
            "most often missing</b>, and a log of attempts without "
            "results cannot distinguish a successful attack from a "
            "failed one."]},

  {"t": "code", "kicker": "Events", "title": "The fields that make a log usable",
   "lang": "text", "code": """
  EVERY SECURITY EVENT:
      who      the authenticated principal, and the real
               one -- not the service account acting on
               their behalf
      what     the action and the specific object
      when     a synchronised timestamp, with timezone
      where    source address, and the request identifier
      outcome  permitted, denied, or errored

  AND A CORRELATION IDENTIFIER threaded through every
  service, so one user action is one searchable trace
  (CSCE 678 Module 09).

  WHAT NOT TO LOG
      secrets, tokens, and passwords -- including in
          error messages and request dumps
          (Module 07 section 4)
      personal data beyond what is needed, because logs
          are copied widely and retained long
      and whole request bodies, for the same reason
""",
   "caption": "<b>The 'who' field must be the real principal</b> "
              "— a log showing a service account for every action "
              "is unusable for an insider investigation.",
   "note": "The real-principal point is the one that bites during "
           "investigations."},

  {"t": "section", "label": "Part 2", "title": "Detection",
   "blurb": "From threats, and tested."},

  {"t": "bullets", "kicker": "Detections", "title": "The detections with the best signal",
   "items": [
     "<b>Authorisation denials in bursts</b> "
     "(Module 03 §3) — <b>one principal, many "
     "refusals, is among the clearest signals available</b> and is "
     "free to collect.",
     "",
     "<b>Authentication failures across many accounts from one "
     "source</b> — credential stuffing "
     "(Module 02 §4), and it has a distinctive shape.",
     "",
     "<b>A successful login from a new location immediately after "
     "failures</b>, which is the stuffing success signal.",
     "",
     "<b>New outbound destinations</b> "
     "(Module 04 §2) — <b>exfiltration and callbacks "
     "need a channel</b>, and a host contacting something it never "
     "has is worth a look.",
     "",
     "<b>And privilege grants, secret reads, and configuration "
     "changes</b> — low volume, high value, and they should be "
     "reviewed rather than merely stored.",
   ],
   "footnote": "<b>Low-volume high-value events are the best "
               "detections</b> because they can be reviewed by a person "
               "— and most programmes over-invest in high-volume "
               "signals instead."},

  {"t": "callout", "title": "An untested detection is a hope",
   "kind": "The requirement",
   "body": ["<b>A detection rule that has never fired may be working "
            "perfectly or may be broken</b> — and <b>the two look "
            "identical from the outside.</b>",
            "<b>So trigger each one deliberately, on your own system, "
            "and confirm the alert arrives</b> — including that it "
            "reaches a person who knows what to do with it.",
            "<b>And re-test after changes</b>, because <b>a log format "
            "change, a field rename, or a library upgrade silently "
            "breaks parsing</b> and the rule then matches nothing "
            "forever.",
            "<b>Which makes detection testing a continuous requirement "
            "rather than a one-off</b> — and <b>the mature version is "
            "automated: synthetic attack traffic on a schedule, with the "
            "alert as the assertion.</b>"]},

  {"t": "section", "label": "Part 3", "title": "The base rate",
   "blurb": "Why good detectors produce useless alerts."},

  {"t": "callout", "title": "A 99%-accurate detector on rare events produces mostly false positives",
   "kind": "The arithmetic that kills alerting programmes",
   "body": ["<b>Ten million events a day, one attack, a detector with "
            "a 1% false positive rate.</b> <b>That is 100,000 false "
            "alerts and one true one.</b>",
            "<b>So the precision is 1 in 100,001</b>, and <b>no team "
            "can review that</b> — which is CSCE 633 "
            "§12 §2's base rate problem, in the setting "
            "where it does the most damage.",
            "<b>And the failure mode is predictable:</b> <b>the alerts "
            "are ignored, then muted, then deleted</b> — so the "
            "detector's effective sensitivity becomes zero while the "
            "dashboard still shows it enabled.",
            "<b>So the response is to raise the base rate rather than "
            "the accuracy:</b> <b>alert on rare, high-value events "
            "(Part 2), correlate several weak signals, and scope rules "
            "narrowly</b> — <b>and compute the expected volume before "
            "deploying a rule.</b>"]},

  {"t": "bullets", "kicker": "Volume", "title": "Managing alert volume honestly",
   "items": [
     "<b>Compute the expected daily volume before enabling a "
     "rule.</b> <b>If it exceeds what a person can review, the rule is "
     "not ready</b> — and enabling it anyway is worse than not "
     "having it.",
     "",
     "<b>Separate 'alert' from 'record'.</b> <b>Most signals should "
     "be searchable during an investigation and should not "
     "page anyone.</b>",
     "",
     "<b>Correlate.</b> <b>Three weak signals on one principal is a "
     "far better detection than any one of them</b>, and the base rate "
     "improves multiplicatively.",
     "",
     "<b>And measure the false positive rate per rule</b>, then "
     "retire the rules that never produce a true positive.",
     "",
     "<b>Which almost nobody does</b> — rules accumulate and are "
     "never removed, and the noise is the result.",
   ],
   "footnote": "<b>Retiring rules is the maintenance nobody "
               "performs</b>, and it is why a mature detection stack is "
               "noisier than a new one."},

  {"t": "section", "label": "Part 4", "title": "Why programmes fail",
   "blurb": "The honest list."},

  {"t": "callout", "title": "Most detection programmes fail for operational reasons, not technical ones",
   "kind": "Closing",
   "body": ["<b>Alert fatigue</b> (Part 3) — <b>the volume "
            "exceeds the capacity, so nothing is read.</b>",
            "<b>Untested rules</b> (Part 2) — <b>a parsing change "
            "silently disabled half the detections and nobody "
            "noticed.</b>",
            "<b>No response path.</b> <b>An alert reaching someone who "
            "does not know what to do with it is not a detection</b> "
            "— which is Module 10's subject.",
            "<b>And logging the wrong things</b> (Part 1) — "
            "<b>the investigation needs a field nobody emitted</b>, "
            "which is discovered during the incident and cannot be "
            "fixed retroactively."]},

  {"t": "bullets", "kicker": "Programme", "title": "A detection programme that works",
   "items": [
     "<b>Start from the threat model</b> (Module 01 §2) "
     "— <b>three threats, logged and detected properly, beats "
     "thirty rules from a vendor list.</b>",
     "",
     "<b>Log the short list</b> (Part 1) <b>with the five fields and "
     "a correlation identifier.</b>",
     "",
     "<b>Centralise, so logs survive the compromise of the host that "
     "produced them</b> — an attacker's first act is frequently to "
     "clear local logs.",
     "",
     "<b>Retain long enough to investigate.</b> <b>Intrusions are "
     "frequently discovered months later</b>, and 30 days of retention "
     "answers nothing.",
     "",
     "<b>And test every detection, on a schedule.</b>",
   ],
   "footnote": "<b>Centralisation and retention are the two "
               "unglamorous controls that decide whether an "
               "investigation is possible at all</b> — and both are "
               "budget decisions rather than technical ones."},
 ],
 "takeaways": [
   "Design logging backwards from the questions you will need to answer, "
   "not forwards from what the code happens to know.",
   "Every security event needs who, what, when, where, and outcome — "
   "and the outcome field is the one most often missing.",
   "The 'who' must be the real principal rather than the service account "
   "acting for them, or insider investigation is impossible.",
   "A 99%-accurate detector on rare events produces overwhelmingly false "
   "positives, so raise the base rate rather than the accuracy.",
   "An untested detection is a hope, and a log format change silently "
   "breaks parsing forever.",
   "Centralisation and retention decide whether an investigation is "
   "possible at all, and both are budget decisions.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Logging"),
  ("callout", "Log what you would need to answer the question, not what is "
              "convenient to emit",
   ["<b>Most logging is written forwards — emit whatever the code "
    "happens to know at that point in execution</b> — and is then "
    "largely useless during an investigation, because the field that "
    "matters was in a different function.",
    "<b>So design backwards:</b> <b>write down the questions you will "
    "need to answer, and then derive the fields required to answer "
    "them.</b> 'Which accounts did this source address touch in the last "
    "week?' requires both the address and the account in every single "
    "event, which forwards-designed logging rarely achieves.",
    "<b>The security-relevant event types are a short list:</b> "
    "<b>authentication attempts, authorisation denials</b> (Module 03 "
    "&sect;3), <b>privilege and role changes, configuration changes, "
    "secret access</b> (Module 07), <b>and administrative actions.</b> "
    "<b>Six categories, and getting those right beats logging "
    "everything.</b>",
    "<b>And every event needs who, what, when, from where, and the "
    "outcome</b> — <b>the outcome field is the one most often "
    "missing</b>, and <b>a log of attempts without results cannot "
    "distinguish a successful attack from a failed one</b>, which is the "
    "central question in every investigation."]),
  ("code", """EVERY SECURITY EVENT:
    who      the authenticated principal -- and the REAL
             one, not the service account acting on their
             behalf
    what     the action, and the specific object
    when     a synchronised timestamp, with timezone
    where    source address, and the request identifier
    outcome  permitted, denied, or errored

AND A CORRELATION IDENTIFIER threaded through every
service, so that one user action is one searchable trace
across the whole system (CSCE 678 Module 09).

WHAT NOT TO LOG
    secrets, tokens, and passwords -- including inside
        error messages and request dumps, which is how
        they usually get there (Module 07 section 4)
    personal data beyond what is needed, because logs are
        copied to aggregators, read widely, and retained
        for years
    and whole request bodies, for the same reason"""),
  ("p", "<b>The 'who' field must be the real principal.</b> <b>A log "
        "showing a service account as the actor for every action is "
        "unusable for an insider investigation</b> — which is "
        "Module 01 &sect;2's adversary model arriving as a concrete "
        "logging requirement, and it is a common architectural mistake in "
        "systems where a middle tier acts on users' behalf."),

  ("h1", "2 &nbsp; Detection"),
  ("ul", ["<b>Authorisation denials in bursts</b> (Module 03 "
          "&sect;3) — <b>one principal generating many refusals is "
          "among the clearest signals available</b>, it is free to "
          "collect, and legitimate use produces very few of them.",
          "<b>Authentication failures across many accounts from a "
          "single source</b> — credential stuffing (Module 02 "
          "&sect;4), <b>and it has a distinctive shape</b>: many "
          "usernames, one or few passwords, one origin.",
          "<b>A successful login from a new location immediately "
          "following a run of failures</b>, which is the signal that the "
          "stuffing <i>worked</i> — and is far more actionable than "
          "the failures alone.",
          "<b>New outbound destinations</b> (Module 04 "
          "&sect;2) — <b>exfiltration and command-and-control both "
          "need a channel</b>, and a host contacting an address it has "
          "never contacted before is worth a look.",
          "<b>And privilege grants, secret reads, and configuration "
          "changes</b> — <b>low volume, high value, and they should "
          "be <i>reviewed</i> rather than merely stored.</b> "
          "<b>Low-volume high-value events are the best detections "
          "available</b>, precisely because a person can actually read "
          "them — and <b>most programmes over-invest in "
          "high-volume signals instead</b>, for reasons &sect;3 "
          "explains."]),
  ("callout", "An untested detection is a hope",
   ["<b>A detection rule that has never fired may be working perfectly "
    "in a quiet environment, or may be completely broken</b> — and "
    "<b>the two states look identical from the outside.</b>",
    "<b>So trigger each rule deliberately, on your own system, and "
    "confirm the alert arrives</b> — <b>including that it reaches a "
    "person who knows what to do with it</b>, which is the part usually "
    "left untested.",
    "<b>And re-test after changes</b>, because <b>a log format change, "
    "a field rename, a library upgrade, or a new service version silently "
    "breaks parsing</b> — and <b>the rule then matches nothing, "
    "forever, while continuing to appear enabled.</b>",
    "<b>Which makes detection testing a continuous requirement rather "
    "than a one-off exercise</b> — and <b>the mature version is "
    "automated: synthetic attack traffic generated on a schedule, with "
    "the arrival of the alert as the test assertion.</b> <b>Which is "
    "CSCE 606's testing discipline applied to security controls, and "
    "it is this course's single most valuable operational practice.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; The base rate problem"),
  ("callout", "A 99%-accurate detector on rare events produces mostly false "
              "positives",
   ["<b>Ten million events a day, one genuine attack among them, and a "
    "detector with a 1% false positive rate.</b> <b>That is one hundred "
    "thousand false alerts and one true one.</b>",
    "<b>So the precision is one in 100,001</b>, and <b>no team on earth "
    "can review that</b> — which is <b>CSCE 633 Module 12 "
    "&sect;2's base rate problem, arriving in the setting where it does "
    "the most practical damage.</b>",
    "<b>And the failure mode is entirely predictable:</b> <b>the alerts "
    "are ignored, then filtered, then muted, then deleted</b> — "
    "<b>so the detector's effective sensitivity becomes zero while the "
    "dashboard continues to show it enabled</b>, which is worse than not "
    "having deployed it because it occupies the budget.",
    "<b>So the response is to raise the base rate rather than the "
    "accuracy:</b> <b>alert on rare, high-value events (&sect;2), "
    "correlate several weak signals into one strong one, and scope rules "
    "narrowly to specific assets</b> — <b>and compute the expected "
    "alert volume before deploying any rule</b>, which takes an hour and "
    "prevents the whole failure."]),
  ("ul", ["<b>Compute the expected daily volume before enabling a "
          "rule.</b> <b>If it exceeds what a person can actually review, "
          "the rule is not ready</b> — and <b>enabling it anyway is "
          "worse than not having it</b>, because it degrades every other "
          "alert's credibility.",
          "<b>Separate 'alert' from 'record'.</b> <b>Most signals "
          "should be searchable during an investigation and should not "
          "page anybody</b> — and conflating the two is the "
          "commonest cause of excessive volume.",
          "<b>Correlate.</b> <b>Three weak signals on the same "
          "principal within an hour is a far better detection than any one "
          "of them individually</b>, and <b>the base rate improves "
          "multiplicatively</b> while the sensitivity falls only "
          "slightly.",
          "<b>And measure the false positive rate per rule</b>, then "
          "<b>retire the rules that have never produced a true "
          "positive</b> — which is a one-line query against your "
          "alert history and an uncomfortable conversation.",
          "<b>Which almost nobody does.</b> <b>Rules accumulate and "
          "are never removed</b>, which is <b>why a mature detection "
          "stack is routinely noisier than a new one</b> — and "
          "<b>retiring rules is the maintenance nobody performs.</b>"]),

  ("h1", "4 &nbsp; Why programmes fail, and what works"),
  ("callout", "Most detection programmes fail for operational reasons, not "
              "technical ones",
   ["<b>Alert fatigue</b> (&sect;3) — <b>the volume exceeds the "
    "review capacity, so nothing is read</b>, and this is the single "
    "largest cause.",
    "<b>Untested rules</b> (&sect;2) — <b>a log parsing change "
    "silently disabled half the detections eighteen months ago and nobody "
    "noticed, because a detection that does not fire looks exactly like a "
    "quiet environment.</b>",
    "<b>No response path.</b> <b>An alert that reaches someone who does "
    "not know what to do with it is not a detection</b> — it is a "
    "notification — <b>which is Module 10's subject and is the "
    "half of the problem that is not technical at all.</b>",
    "<b>And logging the wrong things</b> (&sect;1) — <b>the "
    "investigation needs a field that nobody emitted</b>, <b>which is "
    "discovered during the incident and cannot be fixed "
    "retroactively</b>. <b>That last one is why &sect;1 designs "
    "backwards from the questions.</b>"]),
  ("ul", ["<b>Start from the threat model</b> (Module 01 "
          "&sect;2) — <b>three specific threats, logged and "
          "detected properly and tested, beats thirty rules taken from a "
          "vendor's default list</b>, because the three will fire "
          "meaningfully and the thirty will produce noise.",
          "<b>Log the short list</b> (&sect;1's six categories) <b>with "
          "the five fields and a correlation identifier.</b>",
          "<b>Centralise, so that logs survive the compromise of the "
          "host that produced them</b> — <b>clearing local logs is "
          "frequently an attacker's first action</b>, and a log that can "
          "be deleted by the compromised machine is not evidence.",
          "<b>Retain long enough to investigate.</b> <b>Intrusions are "
          "frequently discovered months after the initial access</b>, and "
          "<b>thirty days of retention answers nothing at all</b> — "
          "which makes retention length a direct determinant of whether "
          "an investigation can succeed.",
          "<b>And test every detection, on a schedule</b> "
          "(&sect;2). <b>Centralisation and retention are the two "
          "unglamorous controls that decide whether an investigation is "
          "possible at all</b> — and <b>both are budget decisions "
          "rather than technical ones</b>, which is why they are the ones "
          "to argue for first."]),
 ],
 "resources": [
   ("Google &mdash; Building Secure and Reliable Systems, the detection "
    "chapters (free PDF)",
    "https://sre.google/books/building-secure-reliable-systems/",
    "<b>&sect;1 and &sect;4 from operators</b> — including the "
    "logging-design-backwards argument."),
   ("Axelsson &mdash; The Base-Rate Fallacy and Intrusion Detection "
    "(free)",
    "https://dl.acm.org/doi/10.1145/357830.357849",
    "<b>&sect;3, with the arithmetic</b> — the paper that should "
    "have settled how alerting is designed and did not."),
   ("MITRE ATT&amp;CK (free)",
    "https://attack.mitre.org/",
    "<b>A catalogue of adversary techniques with detection guidance "
    "per technique</b> — useful for &sect;2's rule design, and best "
    "used threat-model-first rather than as a checklist."),
   ("Atomic Red Team (free)",
    "https://atomicredteam.io/",
    "<b>&sect;2's detection testing, automated</b> — small, safe "
    "tests that trigger specific detections, for use on your own "
    "systems."),
 ],
 "exercises": [
   "<b>Write five questions</b> you would need to answer during an "
   "incident, then check whether your logs can answer them.",
   "<b>Add the missing fields</b> and re-check.",
   "<b>Verify your logs record the real principal</b> rather than a "
   "service account.",
   "<b>Grep your logs for secrets</b> and fix whatever you find "
   "(Module 07 §4).",
   "<b>Build a detection for authorisation denial bursts</b> and trigger "
   "it on your own system.",
   "<b>Compute the expected daily alert volume</b> for three rules before "
   "enabling them.",
   "<b>Deliberately break a log field name</b> and confirm your detection "
   "silently stops matching.",
   "<b>Measure the false positive rate per rule</b> over a month, and "
   "identify rules to retire.",
   "<b>Check your log retention period</b> and compare against typical "
   "intrusion discovery times.",
   "<b>Confirm your logs survive compromise of the host</b> that emits "
   "them.",
 ],
 "selfcheck": [
   "Why design logging backwards, and what are the six event "
   "categories?",
   "Name the five required fields and say which is most often "
   "missing.",
   "Why must the 'who' be the real principal?",
   "Name five high-signal detections, and say why low-volume ones are "
   "best.",
   "Why is an untested detection a hope, and what breaks rules "
   "silently?",
   "Give the base rate arithmetic and the predictable failure mode.",
   "How do you raise the base rate rather than the accuracy?",
   "Give four ways to manage volume, and the one nobody does.",
   "Name four reasons detection programmes fail.",
   "Which two controls decide whether investigation is possible?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Incident Response",
 "subtitle": "What you do, decided before you need it.",
 "question": "It has happened. What now?",
 "outcomes": [
     "Explain the phases and what each requires in advance.",
     "Explain the containment trade and decide it.",
     "Explain evidence handling and why it constrains action.",
     "Run a tabletop exercise.",
     "Write a blameless post-mortem that produces change.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The phases",
   "blurb": "And the one that matters is the first."},

  {"t": "table", "kicker": "Phases", "title": "The phases, and what each needs ready",
   "header": ["Phase", "The work", "Prepared in advance"],
   "widths": [2.4, 4.0, 5.5],
   "rows": [
     ["<b>Prepare</b>", "<b>Everything below, before you need it</b>", "<b>The only phase you control the timing of</b>"],
     ["<b>Detect</b>", "<b>Notice it</b>", "<b>Module 09, and a reporting channel for people</b>"],
     ["<b>Contain</b>", "<b>Stop it spreading</b>", "<b>Authority to act, and the means (Part 2)</b>"],
     ["<b>Eradicate</b>", "<b>Remove the access</b>", "<b>Credential rotation that works (M07 §3)</b>"],
     ["<b>Recover</b>", "<b>Restore service, verify it is clean</b>", "<b>Tested restores, known-good images</b>"],
     ["<b>Learn</b>", "<b>Change the system</b>", "<b>A blameless process (Part 4)</b>"],
   ],
   "footnote": "<b>Preparation is the only phase whose timing you "
               "choose</b> — and every other phase's quality is "
               "determined by how much of it was done.",
   "note": "The preparation framing is what makes the phase list "
           "actionable."},

  {"t": "callout", "title": "What must exist before the incident",
   "kind": "The preparation list",
   "body": ["<b>A named person who decides</b>, and an escalation path "
            "that works at 3am on a Sunday — <b>including who may "
            "authorise taking production down.</b>",
            "<b>Out-of-band communication.</b> <b>If the incident is "
            "in your email or chat, you cannot coordinate in it</b>, and "
            "deciding this during the incident is too late.",
            "<b>Access to act:</b> <b>can the responder actually "
            "isolate a host, revoke a credential, and pull logs</b> "
            "— or do they need someone who is asleep?",
            "<b>And the contact list:</b> legal, communications, "
            "insurance, your regulator if you have one, and law "
            "enforcement. <b>Assembled calmly beforehand, not "
            "searched for during.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Containment",
   "blurb": "The decision under pressure."},

  {"t": "callout", "title": "Containment trades evidence and intelligence against further damage",
   "kind": "The real decision",
   "body": ["<b>Isolate immediately and you stop the damage, lose "
            "visibility into what the attacker was doing, and tell them "
            "they are detected.</b>",
            "<b>Watch and wait and you learn the scope, the method, and "
            "the other footholds — while the damage "
            "continues.</b>",
            "<b>And the right answer depends on what is at stake:</b> "
            "<b>active data exfiltration or destructive activity means "
            "contain now</b>, and <b>a single reconnaissance foothold may "
            "be worth observing briefly.</b>",
            "<b>But decide it deliberately, with the decision "
            "recorded</b> — <b>and the default under uncertainty "
            "should be to contain</b>, because the downside of waiting is "
            "unbounded and the downside of containing is "
            "inconvenience."]},

  {"t": "code", "kicker": "Containment", "title": "The actions, roughly in order of reach",
   "lang": "text", "code": """
  ISOLATE   network-isolate the host, do not power it off
            -- powering off destroys memory evidence and
            may trigger destructive logic

  REVOKE    sessions, tokens, and keys for the affected
            principals. This is where Module 07 section 3's
            tested rotation procedure pays for itself.

  BLOCK     the attacker's known infrastructure at the
            egress boundary (Module 04 section 2)

  DISABLE   the affected feature or integration, if that
            closes the path

  AND PRESERVE as you go: snapshot before you change
  anything, and record every action with a timestamp.
  The timeline is the deliverable.
""",
   "caption": "<b>Isolate rather than power off</b> — memory holds "
              "the evidence, and shutdown destroys it.",
   "note": "The do-not-power-off instruction is the one people get "
           "wrong under pressure."},

  {"t": "section", "label": "Part 3", "title": "Evidence",
   "blurb": "Which constrains how you act."},

  {"t": "bullets", "kicker": "Evidence", "title": "Handling it so it remains usable",
   "items": [
     "<b>Snapshot before changing.</b> <b>Disk and memory images, "
     "taken before remediation</b> — because remediation destroys "
     "the record of what happened.",
     "",
     "<b>Record the order of volatility:</b> memory, network state, "
     "running processes, then disk. <b>The most volatile first.</b>",
     "",
     "<b>Keep a contemporaneous timeline</b> of every action taken, "
     "by whom, at what time — <b>which is also the post-mortem's "
     "raw material.</b>",
     "",
     "<b>Preserve logs beyond the retention window</b> explicitly, "
     "before they rotate out from under the investigation.",
     "",
     "<b>And get legal advice early</b> if the incident may involve "
     "personal data, a regulator, or litigation — <b>because the "
     "notification clocks start without waiting for you.</b>",
   ],
   "footnote": "<b>The notification deadlines are the surprise:</b> "
               "several regimes require reporting within 72 hours of "
               "becoming aware, which is a decision to have made in "
               "advance."},

  {"t": "section", "label": "Part 4", "title": "Learning",
   "blurb": "The phase that determines whether it recurs."},

  {"t": "callout", "title": "A blameless post-mortem asks what made the mistake possible",
   "kind": "And the framing is the whole technique",
   "body": ["<b>'Why did the engineer click the link' produces a "
            "defensive answer and no change.</b> <b>'Why did clicking a "
            "link lead to a domain compromise' produces a list of "
            "controls.</b>",
            "<b>So the rule is to treat human error as a <i>symptom</i> "
            "of system design</b> — <b>people will make mistakes, so "
            "the question is why the mistake had that "
            "consequence.</b>",
            "<b>And blamelessness is instrumental rather than "
            "kind:</b> <b>a blaming process produces incidents that are "
            "not reported</b>, which is the worst possible outcome and "
            "the reason the practice exists.",
            "<b>The deliverable is a short list of specific changes "
            "with owners and dates</b> — <b>and a post-mortem whose "
            "actions are not tracked to completion was an exercise in "
            "writing.</b>"]},

  {"t": "bullets", "kicker": "Exercising", "title": "Tabletop exercises, which are cheap and uncomfortable",
   "items": [
     "<b>Take a scenario from your threat model</b> and walk through "
     "it with the people who would actually respond.",
     "",
     "<b>Ask who decides, who is called, and what they can "
     "do</b> — and <b>stop when someone cannot answer</b>, because "
     "that is the finding.",
     "",
     "<b>Expect to discover a missing authority, a missing access, "
     "or a missing contact</b> — every exercise finds at least "
     "one.",
     "",
     "<b>It costs two hours and no production risk</b>, which makes "
     "it the highest-value security exercise available.",
     "",
     "<b>And run it before you need it.</b> <b>The alternative is "
     "discovering the gaps during the incident</b>, which is the same "
     "discovery at a far worse price.",
   ],
   "footnote": "<b>Two hours, no risk, and it always finds "
               "something</b> — there is no cheaper security "
               "activity in this course."},
 ],
 "takeaways": [
   "Preparation is the only phase whose timing you choose, and every other "
   "phase's quality is determined by how much of it was done.",
   "Out-of-band communication must be arranged in advance, because if the "
   "incident is in your chat you cannot coordinate in it.",
   "Containment trades evidence and intelligence against further damage, "
   "and the default under uncertainty is to contain.",
   "Isolate rather than power off — memory holds the evidence and "
   "shutdown destroys it.",
   "Blamelessness is instrumental rather than kind: a blaming process "
   "produces incidents that are not reported.",
   "A tabletop exercise costs two hours and no production risk and always "
   "finds a missing authority, access, or contact.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The phases"),
  ("table", ["Phase", "The work", "What must be prepared in advance"],
   [["<b>Prepare</b>", "<b>Everything in the rows below, before you need "
     "it.</b>",
     "<b>The only phase whose timing you control</b> — see the "
     "note."],
    ["<b>Detect</b>", "<b>Notice that it is happening.</b>",
     "<b>Module 09's logging and detection, and a reporting channel "
     "that a person can use</b> — many incidents are first reported "
     "by a customer or an employee."],
    ["<b>Contain</b>", "<b>Stop it spreading.</b>",
     "<b>The authority to act and the technical means to do so</b> "
     "(&sect;2)."],
    ["<b>Eradicate</b>", "<b>Remove the attacker's access.</b>",
     "<b>A credential rotation procedure that has actually been "
     "executed before</b> (Module 07 &sect;3)."],
    ["<b>Recover</b>",
     "<b>Restore service, and verify that what you restored is "
     "clean.</b>",
     "<b>Tested restores and known-good images</b> — an untested "
     "backup is a hope, and restoring a compromised image reinstates the "
     "attacker."],
    ["<b>Learn</b>", "<b>Change the system so it does not recur.</b>",
     "<b>A blameless process that produces tracked actions</b> "
     "(&sect;4)."]],
   [0.17, 0.33, 0.50]),
  ("callout", "What must exist before the incident",
   ["<b>A named person who decides</b>, and an escalation path that "
    "functions at three in the morning on a Sunday — <b>including an "
    "explicit answer to who may authorise taking production down</b>, "
    "because that decision will be needed and nobody wants to make it "
    "unilaterally.",
    "<b>Out-of-band communication.</b> <b>If the incident is in your "
    "email or your chat system, you cannot coordinate the response "
    "inside it</b> — the attacker is reading it — and "
    "<b>deciding this during the incident is far too late</b>. A "
    "pre-arranged alternative channel, with the numbers written down "
    "somewhere not on the compromised system.",
    "<b>Access to act:</b> <b>can the person responding actually "
    "isolate a host, revoke a credential, and retrieve logs</b> — or "
    "do they have to wake somebody who holds the permission? "
    "<b>Module 03's least privilege and the need to respond are in "
    "genuine tension, and the resolution is break-glass access that is "
    "logged and alerted rather than absent.</b>",
    "<b>And the contact list:</b> legal counsel, communications, the "
    "insurer, your regulator if you have one, and law enforcement. "
    "<b>Assembled calmly beforehand, rather than searched for during</b> "
    "— and the legal contact matters most, for &sect;3's reasons."]),

  ("h1", "2 &nbsp; Containment"),
  ("callout", "Containment trades evidence and intelligence against further "
              "damage",
   ["<b>Isolate immediately and you stop the damage, lose visibility "
    "into what the attacker was doing, and inform them that they have been "
    "detected</b> — after which they may change tactics, or act "
    "destructively.",
    "<b>Watch and wait and you learn the scope, the method, and the "
    "other footholds you had not found</b> — <b>while the damage "
    "continues</b>, and while your knowledge of the damage grows.",
    "<b>And the right answer depends entirely on what is at stake:</b> "
    "<b>active data exfiltration or any destructive activity means "
    "contain now</b>, without deliberation; <b>a single reconnaissance "
    "foothold with no evidence of movement may be worth observing "
    "briefly</b>, if you have the capability to observe it.",
    "<b>But decide it deliberately, and record the decision and the "
    "reasoning</b> — <b>and the default under uncertainty should be "
    "to contain</b>, because <b>the downside of waiting is unbounded and "
    "the downside of containing is inconvenience.</b> <b>Organisations "
    "that chose to observe and regretted it outnumber those that contained "
    "and regretted it.</b>"]),
  ("code", """ISOLATE   network-isolate the host. DO NOT POWER IT OFF --
          powering off destroys memory evidence and may
          trigger destructive logic on shutdown.

REVOKE    sessions, tokens, and keys for every affected
          principal. This is where Module 07 section 3's
          tested rotation procedure pays for itself, and
          where an untested one fails.

BLOCK     the attacker's known infrastructure at the
          egress boundary (Module 04 section 2) -- which
          is also why egress filtering was worth having
          before the incident.

DISABLE   the affected feature or integration, if doing so
          closes the path. Removing capability is faster
          than fixing it.

AND PRESERVE AS YOU GO: snapshot before you change
anything, and record every action with a timestamp. The
timeline is the deliverable."""),

  ("break",),
  ("h1", "3 &nbsp; Evidence"),
  ("ul", ["<b>Snapshot before changing anything.</b> <b>Disk and "
          "memory images, taken before remediation begins</b> — "
          "<b>because remediation destroys the record of what "
          "happened</b>, and the pressure to fix it immediately is "
          "exactly what causes the evidence to be lost.",
          "<b>Respect the order of volatility:</b> memory first, then "
          "network state and connections, then running processes, then "
          "disk. <b>The most volatile evidence first</b>, because it is "
          "gone in minutes and the disk will still be there in an hour.",
          "<b>Keep a contemporaneous timeline</b> of every action "
          "taken, by whom, at what time, and why — <b>which is also "
          "the post-mortem's raw material</b> (&sect;4) and is "
          "impossible to reconstruct afterwards.",
          "<b>Preserve logs beyond the retention window explicitly</b>, "
          "before they rotate out from under the investigation — "
          "which happens during long investigations and is "
          "irrecoverable.",
          "<b>And get legal advice early</b> if the incident may involve "
          "personal data, a regulator, a contract, or litigation — "
          "<b>because the notification clocks start running without "
          "waiting for you</b>. <b>Several regimes require reporting "
          "within 72 hours of becoming aware</b>, which is <b>a decision "
          "to have made in advance</b> rather than researched on the "
          "second day."]),

  ("h1", "4 &nbsp; Learning"),
  ("callout", "A blameless post-mortem asks what made the mistake possible",
   ["<b>'Why did the engineer click the link' produces a defensive "
    "answer, an apology, and no change.</b> <b>'Why did clicking a link "
    "lead to a domain compromise' produces a list of missing "
    "controls</b> — no second factor, excessive standing privilege, "
    "flat network, no egress filtering. <b>The second framing is "
    "actionable and the first is not.</b>",
    "<b>So the rule is to treat human error as a <i>symptom</i> of "
    "system design</b> — <b>people will make mistakes at a "
    "predictable rate, so the operative question is why that mistake had "
    "that consequence</b> (Module 11's subject).",
    "<b>And blamelessness is instrumental rather than kind.</b> <b>A "
    "blaming process produces incidents that are not reported</b> — "
    "people conceal mistakes, near-misses go unexamined, and you lose the "
    "information you most need. <b>Which is the actual reason the "
    "practice exists</b>, and it is worth stating because 'blameless' "
    "sounds like a cultural nicety and is an information-gathering "
    "requirement.",
    "<b>The deliverable is a short list of specific changes with named "
    "owners and dates</b> — <b>and a post-mortem whose action items "
    "are not tracked to completion was an exercise in writing</b>, which "
    "is the commonest way the learning phase fails."]),
  ("ul", ["<b>Take a scenario directly from your threat model</b> "
          "(Module 01 &sect;2) <b>and walk through it with the people "
          "who would actually respond</b> — not with a committee.",
          "<b>Ask who decides, who is called, and what they are able to "
          "do</b> — and <b>stop when somebody cannot answer, because "
          "that is the finding</b> rather than an interruption.",
          "<b>Expect to discover a missing authority, a missing access, "
          "or a missing contact</b> — <b>every exercise finds at "
          "least one</b>, and the first one typically finds several.",
          "<b>It costs two hours and carries no production risk "
          "whatsoever</b>, which makes it <b>the highest-value security "
          "exercise available to most organisations.</b>",
          "<b>And run it before you need it.</b> <b>The alternative is "
          "discovering the same gaps during a real incident</b>, which is "
          "the identical discovery at a vastly worse price. <b>Two hours, "
          "no risk, and it always finds something</b> — there is no "
          "cheaper security activity in this course."]),
 ],
 "resources": [
   ("NIST SP 800-61 &mdash; Computer Security Incident Handling Guide "
    "(free)",
    "https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final",
    "<b>&sect;1's phases, in detail</b>, with the preparation checklists "
    "worth borrowing."),
   ("Allspaw &mdash; Blameless PostMortems and a Just Culture (free)",
    "https://www.etsy.com/codeascraft/blameless-postmortems-and-a-just-culture/",
    "<b>&sect;4's practice</b>, short, and it changed how the industry "
    "handles incidents."),
   ("Dekker &mdash; The Field Guide to Understanding Human Error",
   "https://www.routledge.com/The-Field-Guide-to-Understanding-Human-Error/Dekker/p/book/9781472439055",
    "<b>&sect;4's framing, from safety engineering</b> — where the "
    "human-error-as-symptom argument originates. Library copy."),
   ("Google SRE Book &mdash; the incident management chapters (free)",
    "https://sre.google/sre-book/managing-incidents/",
    "<b>&sect;1's roles and command structure</b>, free in full — "
    "and the incident-commander model is worth adopting."),
 ],
 "exercises": [
   "<b>Write your preparation list</b> and identify which items do not "
   "yet exist.",
   "<b>Determine who may authorise taking production down</b>, and "
   "whether that person knows.",
   "<b>Arrange an out-of-band channel</b> and record the numbers "
   "somewhere off the primary systems.",
   "<b>Check whether a responder can isolate a host and revoke a "
   "credential</b> without waking anyone.",
   "<b>Write the containment decision criteria</b> for your own system, "
   "in advance.",
   "<b>Practise taking a memory image</b> of a machine you own.",
   "<b>Find out your notification obligations</b> and the deadline.",
   "<b>Run a two-hour tabletop</b> on a threat from your model, and "
   "record every question nobody could answer.",
   "<b>Write a blameless post-mortem</b> of the exercise.",
   "<b>Track the resulting actions to completion</b>, and report how "
   "many closed.",
 ],
 "selfcheck": [
   "Name the six phases and what each needs prepared.",
   "Why is preparation the only phase whose timing you choose?",
   "Give four things that must exist before an incident.",
   "Why does out-of-band communication have to be arranged in "
   "advance?",
   "State the containment trade and the default under uncertainty.",
   "Why isolate rather than power off?",
   "Give the order of volatility and why snapshots come first.",
   "What is the surprise about notification deadlines?",
   "Contrast the two post-mortem framings, and say why blamelessness is "
   "instrumental.",
   "Why is a tabletop the highest-value exercise?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Human Factors",
 "subtitle": "A control people route around is not a control.",
 "question": "Why do correct security designs fail in practice?",
 "outcomes": [
     "Explain why usability is a security property.",
     "Explain the compliance budget and its consequences.",
     "Design phishing defences that do not rely on vigilance.",
     "Explain secure defaults and why they dominate.",
     "Review a control for the ways people will avoid it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Usability is security",
   "blurb": "Not a trade against it."},

  {"t": "callout", "title": "An unusable control is not a strong control — it is an absent one",
   "kind": "The central claim",
   "body": ["<b>A password policy people satisfy by writing passwords "
            "down has reduced security</b> "
            "(Module 02 §2) — <b>and the policy looks "
            "stronger on paper.</b>",
            "<b>So usability and security are not opposed</b> — "
            "<b>the usability of a control determines whether it is "
            "actually in place</b>, which makes it a component of the "
            "control's strength rather than a cost against it.",
            "<b>And the evidence is that people are rational.</b> "
            "<b>They route around controls whose cost exceeds the "
            "benefit they perceive</b>, which is a sensible response to a "
            "poorly-designed control.",
            "<b>So the design question is 'what will people actually "
            "do'</b> rather than 'what should they do' — <b>which "
            "is the same empirical turn as CSCE 671's, and is the "
            "reason the two courses share an argument.</b>"]},

  {"t": "callout", "title": "The compliance budget is finite and you are spending it",
   "kind": "The idea that reframes the problem",
   "body": ["<b>Each person has a limited willingness to absorb "
            "security friction</b> — and <b>every control spends from "
            "the same budget.</b>",
            "<b>So a mandatory training module, a complex password "
            "rule, a VPN that drops, and a slow approval process compete "
            "with each other</b> — and <b>spending the budget on "
            "low-value controls means the high-value one is "
            "ignored.</b>",
            "<b>Which explains a common pattern:</b> <b>an "
            "organisation with many controls and poor security</b>, "
            "because the budget was exhausted before anything important "
            "was asked.",
            "<b>So remove controls deliberately.</b> <b>Dropping three "
            "low-value requirements to buy compliance with one "
            "high-value one is a net gain</b> — and it is a decision "
            "almost nobody makes because removing a control looks like "
            "weakening security."]},

  {"t": "section", "label": "Part 2", "title": "Phishing",
   "blurb": "And why training is not the answer."},

  {"t": "callout", "title": "Design so that being phished does not matter",
   "kind": "The only reliable approach",
   "body": ["<b>Phishing training reduces click rates and does not "
            "eliminate them</b> — and <b>a sufficiently good lure "
            "will catch a careful person on a bad day.</b>",
            "<b>So the goal is not a zero click rate but a harmless "
            "click.</b> <b>Origin-bound second factors mean a phished "
            "credential is unusable</b> "
            "(Module 02 §1) — which removes the entire "
            "attack rather than reducing its frequency.",
            "<b>And the supporting controls are all "
            "consequence-reducing:</b> <b>least privilege, so the stolen "
            "account yields little; segmentation, so it does not spread; "
            "and detection, so the use is noticed.</b>",
            "<b>Which means phishing is an authentication and "
            "architecture problem rather than a training problem</b> "
            "— <b>and treating it as a training problem puts the "
            "burden on the person least able to carry it.</b>"]},

  {"t": "bullets", "kicker": "Reporting", "title": "And make reporting easy and safe",
   "items": [
     "<b>A one-click report button</b> that reaches someone who "
     "acts — <b>because a reported phish lets you find everyone "
     "else who received it.</b>",
     "",
     "<b>Thank the reporter, always</b>, including for false alarms "
     "— <b>the cost of a false report is a minute and the cost of "
     "a silent one is an incident.</b>",
     "",
     "<b>And never penalise clicking.</b> <b>A person who clicked and "
     "is afraid to say so is the worst outcome</b>, and it is exactly "
     "what a punitive simulated-phishing programme produces.",
     "",
     "<b>Which is Module 10 §4's blamelessness, applied "
     "before the incident rather than after it.</b>",
     "",
     "<b>And the metric should be reporting rate, not click "
     "rate</b> — the first is what you want to increase.",
   ],
   "footnote": "<b>Measuring click rate incentivises punishing "
               "clickers, which suppresses reporting</b> — so the "
               "metric choice determines the programme's effect "
               "(Module 12)."},

  {"t": "section", "label": "Part 3", "title": "Defaults",
   "blurb": "The control that needs no cooperation."},

  {"t": "callout", "title": "The default is the setting almost everyone has",
   "kind": "Why defaults dominate everything else",
   "body": ["<b>A small minority of users change any given "
            "setting</b> — so <b>the default is, in practice, the "
            "configuration of your system.</b>",
            "<b>Which makes secure-by-default worth more than any "
            "amount of documentation, guidance, or hardening "
            "guide</b> — and it is the one intervention that requires "
            "no user action at all.",
            "<b>And the examples are large:</b> <b>HTTPS by default, "
            "SameSite cookies by default</b> "
            "(Module 06 §3), <b>automatic updates, and "
            "encrypted disks by default each eliminated a class at "
            "scale.</b>",
            "<b>So if you ship software, the highest-leverage security "
            "work available is changing a default</b> — <b>and the "
            "cost is usually a compatibility argument rather than an "
            "engineering one.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Reviewing",
   "blurb": "For the ways people will avoid it."},

  {"t": "bullets", "kicker": "Review", "title": "Questions to ask of a control",
   "items": [
     "<b>What is the cheapest way to avoid this?</b> <b>Someone will "
     "find it</b> — a shared account, a personal device, an "
     "exception request, a screenshot.",
     "",
     "<b>How often must a person comply, and what does it cost "
     "them?</b> <b>Daily friction is spent from the budget</b> "
     "(Part 1) and is remembered.",
     "",
     "<b>What happens when it fails?</b> <b>If a failure blocks "
     "work, there will be a documented workaround within a "
     "month</b> — and the workaround becomes the real process.",
     "",
     "<b>Does it require vigilance?</b> <b>If the control is "
     "'notice something unusual', it will fail</b>, because sustained "
     "vigilance is not available.",
     "",
     "<b>And could a default, an architecture change, or a tool do "
     "this instead of a person?</b>",
   ],
   "footnote": "<b>The last question is the one to ask first</b> "
               "— a control a person must perform is the weakest "
               "kind, and moving it into the system is almost always "
               "possible."},

  {"t": "callout", "title": "What this module adds to the rest of the course",
   "kind": "Closing",
   "body": ["<b>Every control in Modules 02 through 09 is implemented "
            "by people and avoided by people</b> — so <b>a design "
            "that ignores that is incomplete rather than merely "
            "optimistic.</b>",
            "<b>And the direction of the fix is consistent:</b> "
            "<b>move the control into the system, the default, or the "
            "architecture, and away from a person's attention.</b>",
            "<b>Which is also the most reliable way to make security "
            "cheaper</b> — <b>a control that requires no ongoing "
            "human effort has no ongoing cost</b> and does not degrade.",
            "<b>So the question 'who has to do something for this to "
            "work, and how often' is the most useful single question to "
            "ask of a security design</b> — and the best answer is "
            "'nobody, never'."]},
 ],
 "takeaways": [
   "An unusable control is an absent control, so usability is a component "
   "of a control's strength rather than a cost against it.",
   "The compliance budget is finite and every control spends from it, "
   "which explains organisations with many controls and poor security.",
   "Removing three low-value controls to buy compliance with one "
   "high-value one is a net gain, and almost nobody does it.",
   "Phishing is an authentication and architecture problem rather than a "
   "training problem — design so that being phished does not matter.",
   "Measure reporting rate rather than click rate, because measuring "
   "clicks incentivises punishing clickers and suppresses reporting.",
   "The default is the configuration of your system, which makes changing "
   "a default the highest-leverage security work available to a vendor.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Usability is a security property"),
  ("callout", "An unusable control is not a strong control — it is an "
              "absent one",
   ["<b>A password policy that people satisfy by writing their passwords "
    "on a note has <i>reduced</i> security</b> (Module 02 &sect;2) "
    "— <b>and the policy looks stronger on paper than the one it "
    "replaced.</b>",
    "<b>So usability and security are not opposed quantities.</b> "
    "<b>The usability of a control determines whether it is actually in "
    "place</b>, which makes it <b>a component of the control's strength "
    "rather than a cost to be traded against it</b> — and that "
    "reframing is the whole content of this module.",
    "<b>And the evidence is that people behave rationally.</b> <b>They "
    "route around controls whose cost to them exceeds the benefit they "
    "perceive</b>, which is a sensible response to a badly-designed "
    "control rather than a failure of discipline — and treating it as "
    "a discipline problem guarantees the design is not fixed.",
    "<b>So the design question is 'what will people actually do' rather "
    "than 'what should they do'</b> — <b>which is the same empirical "
    "turn as CSCE 671's</b>, and is the reason these two courses share "
    "an argument despite being in different semesters."]),
  ("callout", "The compliance budget is finite and you are spending it",
   ["<b>Each person has a limited willingness to absorb security "
    "friction</b> — Beautement, Sasse and Wonham's compliance budget "
    "— and <b>every control you impose spends from the same "
    "budget.</b>",
    "<b>So a mandatory annual training module, a complex password rule, a "
    "VPN that drops twice a day, and a three-day access approval process "
    "all compete with one another</b> — and <b>spending the budget "
    "on low-value controls means the high-value one is the one that gets "
    "ignored</b>, because by then there is nothing left.",
    "<b>Which explains a pattern that is otherwise puzzling:</b> <b>an "
    "organisation with a great many controls and demonstrably poor "
    "security</b>, because the budget was exhausted long before anything "
    "important was asked of anyone.",
    "<b>So remove controls deliberately.</b> <b>Dropping three "
    "low-value requirements in order to buy genuine compliance with one "
    "high-value one is a net gain</b> — <b>and it is a decision "
    "almost nobody makes, because removing a control looks like weakening "
    "security and is hard to defend in an audit.</b> <b>Which is a "
    "measurement problem</b> (Module 12) <b>rather than a disagreement "
    "about the facts.</b>"]),

  ("h1", "2 &nbsp; Phishing"),
  ("callout", "Design so that being phished does not matter",
   ["<b>Phishing awareness training reduces click rates and does not "
    "eliminate them</b> — the measured effect is real and modest "
    "— and <b>a sufficiently well-crafted lure will catch a careful "
    "person on a bad day</b>, which is not a training deficiency.",
    "<b>So the goal is not a zero click rate but a <i>harmless</i> "
    "click.</b> <b>Origin-bound second factors mean a phished credential "
    "is simply unusable by the attacker</b> (Module 02 &sect;1) "
    "— <b>which removes the entire attack rather than reducing its "
    "frequency</b>, and is the single most effective anti-phishing control "
    "available.",
    "<b>And the supporting controls are all consequence-reducing:</b> "
    "<b>least privilege, so that a stolen account yields little; "
    "segmentation, so that it does not spread</b> (Module 04 "
    "&sect;2); <b>and detection, so that its use is noticed</b> "
    "(Module 09 &sect;2).",
    "<b>Which means phishing is an authentication and architecture "
    "problem rather than a training problem</b> — <b>and treating it "
    "as a training problem places the burden on the person least able to "
    "carry it</b>, while leaving the architecture that made the "
    "consequence severe entirely unchanged."]),
  ("ul", ["<b>A one-click report button</b> that reaches someone who "
          "acts on it — <b>because a single reported phish lets you "
          "find every other recipient and pull the message</b>, which is "
          "worth far more than the one person's caution.",
          "<b>Thank the reporter, every time, including for false "
          "alarms</b> — <b>the cost of a false report is one "
          "minute of someone's time and the cost of a silent true one is "
          "an incident.</b> The asymmetry is enormous and the incentive "
          "should reflect it.",
          "<b>And never penalise clicking.</b> <b>A person who clicked "
          "and is afraid to say so is the worst possible outcome</b>, "
          "because the attacker now has hours of undetected access — "
          "<b>and it is exactly what a punitive simulated-phishing "
          "programme produces.</b>",
          "<b>Which is Module 10 &sect;4's blamelessness, applied "
          "before the incident rather than after it</b> — the same "
          "information-gathering argument, at a different point in the "
          "timeline.",
          "<b>And the metric should be the reporting rate rather than "
          "the click rate</b> — <b>the first is the thing you want "
          "to increase</b>, and <b>measuring clicks incentivises punishing "
          "clickers, which suppresses reporting</b> and makes the "
          "organisation less safe while the metric improves "
          "(Module 12's subject exactly)."]),

  ("break",),
  ("h1", "3 &nbsp; Defaults"),
  ("callout", "The default is the setting almost everyone has",
   ["<b>Only a small minority of users change any given setting</b>, "
    "across essentially every system ever measured — so <b>the "
    "default is, in practice, the configuration of your system as "
    "deployed.</b>",
    "<b>Which makes secure-by-default worth more than any amount of "
    "documentation, guidance, hardening guide, or training</b> — and "
    "<b>it is the one intervention that requires no user action "
    "whatsoever</b>, so it spends nothing from &sect;1's compliance "
    "budget.",
    "<b>And the historical examples are large:</b> <b>HTTPS by default "
    "and then HTTPS-preferred in browsers, SameSite cookies defaulting to "
    "Lax</b> (Module 06 &sect;3), <b>automatic updates, full-disk "
    "encryption on by default on phones, and randomised hash seeds in "
    "language runtimes</b> (Module 01 &sect;1) — <b>each "
    "eliminated a vulnerability class at population scale without asking "
    "anyone to do anything.</b>",
    "<b>So if you ship software, the highest-leverage security work "
    "available to you is changing a default</b> — <b>and the cost is "
    "usually a backwards-compatibility argument rather than an engineering "
    "one</b>, which means the obstacle is organisational and the fix is "
    "available."]),

  ("h1", "4 &nbsp; Reviewing a control"),
  ("ul", ["<b>What is the cheapest way to avoid this?</b> <b>Somebody "
          "will find it</b> — a shared account, a personal device, a "
          "standing exception, a screenshot of the data, an export to a "
          "spreadsheet — <b>and the avoidance path becomes the real "
          "process</b> while the control remains on the diagram.",
          "<b>How often must a person comply, and what does it cost "
          "them each time?</b> <b>Daily friction is spent from the "
          "compliance budget</b> (&sect;1) <b>and is remembered and "
          "resented</b>; an annual cost is nearly free by comparison.",
          "<b>What happens when it fails?</b> <b>If a failure blocks "
          "work, there will be a documented workaround within a "
          "month</b> — and <b>the workaround will not be "
          "reviewed</b>, which makes it a worse control than the one it "
          "replaced.",
          "<b>Does it require sustained vigilance?</b> <b>If the "
          "control is 'notice something unusual', it will fail</b>, "
          "because <b>sustained vigilance is not a human capability</b> "
          "and designing around the assumption that it is guarantees the "
          "failure.",
          "<b>And could a default, an architecture change, or a tool "
          "perform this instead of a person?</b> <b>This is the question "
          "to ask first</b> — <b>a control that a person must "
          "perform is the weakest kind, and moving it into the system is "
          "almost always possible</b> and almost never attempted."]),
  ("callout", "What this module adds to the rest of the course",
   ["<b>Every control in Modules 02 through 09 is implemented by people "
    "and avoided by people</b> — so <b>a design that ignores that is "
    "incomplete rather than merely optimistic</b>, and the incompleteness "
    "is predictable in advance from &sect;4's questions.",
    "<b>And the direction of the fix is consistent across every "
    "case:</b> <b>move the control into the system, into the default, or "
    "into the architecture, and away from a person's ongoing "
    "attention.</b>",
    "<b>Which is also the most reliable way to make security "
    "cheaper</b> — <b>a control that requires no ongoing human "
    "effort has no ongoing cost and does not degrade over time</b>, "
    "whereas one that depends on attention degrades from the day it is "
    "introduced.",
    "<b>So 'who has to do something for this to work, and how often' is "
    "the most useful single question to ask of a security "
    "design</b> — and <b>the best available answer is 'nobody, "
    "never'.</b>"]),
 ],
 "resources": [
   ("Anderson &mdash; Security Engineering, the psychology and usability "
    "chapters (free PDF)",
    "https://www.cl.cam.ac.uk/~rja14/book.html",
    "<b>&sect;1 and &sect;2 with the evidence</b> — free in full, "
    "and the strongest treatment of this material anywhere."),
   ("Beautement, Sasse & Wonham &mdash; The Compliance Budget (free)",
    "https://discovery.ucl.ac.uk/id/eprint/1445307/",
    "<b>&sect;1's second callout, in the original</b> — and the "
    "framing is more useful than any individual finding."),
   ("Adams & Sasse &mdash; Users Are Not the Enemy (free)",
    "https://dl.acm.org/doi/10.1145/322796.322806",
    "<b>&sect;1's argument, from 1999</b>, and the title is the "
    "thesis. It took the industry twenty years to act on it."),
   ("Thaler & Sunstein &mdash; Nudge; and the default-effect "
    "literature",
    "https://web.archive.org/web/20260923132501/https://yalebooks.yale.edu/book/9780300122237/nudge/",
    "<b>&sect;3's effect, outside security</b> — where the "
    "default-dominance finding was established, and it transfers "
    "directly."),
 ],
 "exercises": [
   "<b>Find a control in your organisation that people route "
   "around</b>, and document how.",
   "<b>Estimate the daily friction</b> your controls impose on one "
   "person.",
   "<b>Identify three low-value controls</b> you could remove to buy "
   "compliance with one high-value one.",
   "<b>Check whether your organisation uses origin-bound second "
   "factors</b>, and what the obstacle is if not.",
   "<b>Find your phishing reporting path</b> and time how long it takes "
   "to use.",
   "<b>Determine whether your programme measures clicks or reports</b>, "
   "and what it does to clickers.",
   "<b>List the security-relevant defaults</b> in software you ship, and "
   "whether each is the safe one.",
   "<b>Change one default to the safe value</b> and note the "
   "compatibility objection.",
   "<b>Run §4's five questions</b> against one of your controls.",
   "<b>Find a control that requires vigilance</b> and replace it with "
   "one that does not.",
 ],
 "selfcheck": [
   "Why is an unusable control an absent one?",
   "Why is routing around a control rational?",
   "State the compliance budget and what it explains.",
   "Why is removing a control sometimes a net gain, and why is it "
   "rare?",
   "Why is phishing not a training problem, and what is the effective "
   "control?",
   "Why measure reporting rate rather than click rate?",
   "Why do defaults dominate, and give four historical examples.",
   "Give five questions to ask of a control, and which comes first.",
   "What is the consistent direction of the fix, and the best answer to "
   "'who has to do something'?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Measuring Security",
 "subtitle": "Why it is hard, and which metrics mislead.",
 "question": "How do you know whether you are more secure than last "
             "year?",
 "outcomes": [
     "Explain why security resists measurement.",
     "Identify metrics that mislead and say how.",
     "Choose metrics that drive useful behaviour.",
     "Explain risk quantification and its limits.",
     "Explain the incentive problems around security spending.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why it is hard",
   "blurb": "You are measuring an absence."},

  {"t": "callout", "title": "The thing you want to measure is the absence of something",
   "kind": "The structural difficulty",
   "body": ["<b>'Secure' means 'no successful attack occurred'</b> "
            "— and <b>a quiet year is consistent with excellent "
            "security and with being undetected</b> "
            "(Module 01 §1).",
            "<b>So the outcome is unobservable in the good case</b>, "
            "which is unlike almost every other engineering "
            "property.",
            "<b>And the base rate is low:</b> <b>severe incidents are "
            "rare for any single organisation</b>, so there is no "
            "statistical signal in your own history.",
            "<b>Which leaves process and control metrics as "
            "proxies</b> — <b>and a proxy that is managed becomes a "
            "target</b>, which is Part 2 and is the central hazard."]},

  {"t": "table", "kicker": "Misleading", "title": "Metrics that mislead, and how",
   "header": ["Metric", "What it rewards", "The distortion"],
   "widths": [2.7, 3.9, 5.3],
   "rows": [
     ["<b>Vulnerability count</b>", "<b>Not looking</b>", "<b>Scanning less improves the number</b>"],
     ["<b>Patch compliance %</b>", "<b>Patching the easy fleet</b>", "<b>The hard 5% is where the risk is</b>"],
     ["<b>Training completion %</b>", "<b>Clicking through</b>", "<b>Measures attendance, not behaviour</b>"],
     ["<b>Phishing click rate</b>", "<b>Punishing clickers</b>", "<b>Suppresses reporting (M11 §2)</b>"],
     ["<b>Number of controls</b>", "<b>Adding controls</b>", "<b>Spends the compliance budget (M11 §1)</b>"],
     ["<b>Alerts handled</b>", "<b>Noisy rules</b>", "<b>Rewards the volume problem (M09 §3)</b>"],
   ],
   "footnote": "<b>Every row is Goodhart's law:</b> a measure used as a "
               "target stops measuring what it measured — and these "
               "are the specific distortions each one produces.",
   "note": "This table is the practically useful artefact of the "
           "module."},

  {"t": "section", "label": "Part 2", "title": "Better metrics",
   "blurb": "Which drive behaviour you want."},

  {"t": "bullets", "kicker": "Better", "title": "Metrics worth tracking",
   "items": [
     "<b>Time from advisory to patched in production</b>, at the "
     "median and the 95th percentile — <b>the tail is where the "
     "risk is</b> (Module 08 §4).",
     "",
     "<b>Mean time to detect, measured against injected test "
     "events</b> — <b>which is measurable without waiting for a "
     "real incident</b> (Module 09 §2).",
     "",
     "<b>Percentage of accounts on origin-bound second "
     "factors</b> — a specific, high-value, countable control "
     "(Module 02 §1).",
     "",
     "<b>Inventory query time</b> — <b>'can you locate a library "
     "version in five minutes' is a real capability "
     "test</b> (Module 08 §3).",
     "",
     "<b>And tabletop findings closed</b>, which measures whether "
     "learning turns into change (Module 10 §4).",
   ],
   "footnote": "<b>Each of these measures a capability rather than a "
               "count</b>, and each is hard to improve without actually "
               "improving."},

  {"t": "callout", "title": "Prefer metrics you cannot improve without improving",
   "kind": "The selection criterion",
   "body": ["<b>Ask of every candidate metric: what is the cheapest way "
            "to improve this number without improving security?</b>",
            "<b>If there is one, the metric will be gamed</b> — not "
            "through dishonesty, but because <b>people optimise what is "
            "measured and that is what you asked for.</b>",
            "<b>And prefer measured capabilities over counted "
            "artefacts:</b> <b>'we detected the injected event in 4 "
            "minutes' cannot be faked</b> and 'we have 40 detection "
            "rules' can.",
            "<b>Which is CSCE 633 §12's metric-choice "
            "discipline and CSCE 642 §12's honest "
            "reporting, in the subject where the incentive to look good "
            "is strongest.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Risk",
   "blurb": "Quantification, and its honest limits."},

  {"t": "callout", "title": "Risk quantification is useful for comparison and not for absolute numbers",
   "kind": "The honest position",
   "body": ["<b>Expected loss is probability times impact</b> — and "
            "<b>for a rare event you have no data on the "
            "probability.</b>",
            "<b>So an absolute figure is a guess with decimal "
            "places</b>, and presenting it as a measurement is "
            "misleading in a way that a stated range is not.",
            "<b>But <i>comparative</i> estimates are genuinely "
            "useful:</b> <b>'this risk is roughly ten times that one' is "
            "defensible and is enough to order a budget</b>, which is "
            "what the exercise is actually for.",
            "<b>And the discipline of estimating is valuable even when "
            "the number is not</b> — <b>it forces explicit assumptions, "
            "which can then be argued with</b> "
            "(CSCE 669 §12 §4's sensitivity "
            "analysis)."]},

  {"t": "section", "label": "Part 4", "title": "Incentives",
   "blurb": "Why the spending goes where it does."},

  {"t": "bullets", "kicker": "Incentives", "title": "The incentive problems, named",
   "items": [
     "<b>Security spending is invisible when it works</b>, so it "
     "competes badly against features that are visible.",
     "",
     "<b>The person who bears the cost is frequently not the person "
     "who bears the risk</b> — which is the externality at the "
     "centre of Anderson's economics argument.",
     "",
     "<b>Compliance is measurable and security is not</b>, so "
     "<b>budgets flow to compliance</b> — and a compliant system "
     "can be insecure.",
     "",
     "<b>And a prevented incident produces no evidence</b>, so the "
     "team that prevents them looks idle next to the team that responds "
     "well.",
     "",
     "<b>Which is why Part 2's capability metrics matter</b> "
     "— they give the invisible work something visible to point "
     "at.",
   ],
   "footnote": "<b>The externality is the deepest of these:</b> a "
               "vendor's insecure default costs its users and not the "
               "vendor, which is why Module 11 §3's defaults "
               "needed regulation to change in some cases."},

  {"t": "callout", "title": "What to do about measurement",
   "kind": "Closing",
   "body": ["<b>Pick a small number of capability metrics</b> "
            "(Part 2) <b>and track them over time</b> — five is "
            "better than fifty.",
            "<b>State explicitly what they do not measure</b>, so the "
            "dashboard is not mistaken for coverage.",
            "<b>Test capabilities rather than counting "
            "artefacts</b> — <b>injected events, tabletop exercises, "
            "and timed queries</b>, all of which resist gaming.",
            "<b>And report the threats you have accepted</b> "
            "(Module 01 §2) <b>alongside the controls you "
            "have</b> — <b>which is the one piece of reporting that "
            "conveys the actual position.</b>"]},
 ],
 "takeaways": [
   "Security's outcome is unobservable in the good case, and a quiet year "
   "is consistent with excellence and with being undetected.",
   "Every common security metric is a Goodhart's law instance, and the "
   "table names the specific distortion each produces.",
   "Vulnerability count rewards not looking, and patch compliance "
   "percentage rewards ignoring the hard tail where the risk is.",
   "Prefer metrics you cannot improve without improving — measured "
   "capabilities resist gaming and counted artefacts do not.",
   "Risk quantification is defensible for comparison and not for absolute "
   "figures, and the estimating discipline is worth more than the number.",
   "The deepest incentive problem is the externality: a vendor's insecure "
   "default costs its users rather than the vendor.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why security resists measurement"),
  ("callout", "The thing you want to measure is the absence of something",
   ["<b>'Secure' means 'no successful attack has occurred'</b> — "
    "and <b>a quiet year is entirely consistent with excellent security "
    "and with having been compromised and not noticed</b> (Module 01 "
    "&sect;1's second row, and Module 09's whole subject).",
    "<b>So the outcome you care about is unobservable in the good "
    "case</b>, which is unlike almost every other engineering property: "
    "performance, availability, and correctness all produce observable "
    "evidence when they are good.",
    "<b>And the base rate is low.</b> <b>Severe incidents are rare for "
    "any single organisation</b>, so <b>there is no statistical signal "
    "available in your own history</b> — two good years tells you "
    "almost nothing, and the sample will never grow large enough.",
    "<b>Which leaves process and control metrics as proxies</b> — "
    "and <b>a proxy that is managed becomes a target</b>, which is "
    "&sect;2's table and is <b>the central hazard of this module</b>: "
    "the measurement does not merely fail to capture security, it actively "
    "distorts the behaviour it is meant to assess."]),
  ("table", ["Metric", "What it actually rewards", "The distortion"],
   [["<b>Number of open vulnerabilities</b>", "<b>Not looking.</b>",
     "<b>Scanning less, or scanning fewer systems, improves the "
     "number</b> — and so does classifying findings as "
     "informational."],
    ["<b>Patch compliance percentage</b>",
     "<b>Patching the easy majority of the fleet.</b>",
     "<b>The hard 5% is precisely where the risk lives</b> — the "
     "legacy system nobody can reboot — and 95% compliance is "
     "compatible with total exposure."],
    ["<b>Training completion percentage</b>",
     "<b>Clicking through the module.</b>",
     "<b>It measures attendance rather than behaviour</b>, and the "
     "correlation between the two is weak (Module 11 &sect;2)."],
    ["<b>Phishing simulation click rate</b>",
     "<b>Punishing the people who click.</b>",
     "<b>Which suppresses reporting</b> (Module 11 &sect;2) <b>and "
     "makes the organisation less safe while the metric "
     "improves.</b>"],
    ["<b>Number of security controls deployed</b>",
     "<b>Adding controls.</b>",
     "<b>Which spends the compliance budget</b> (Module 11 "
     "&sect;1) <b>and can reduce actual compliance with the controls "
     "that matter.</b>"],
    ["<b>Alerts handled per analyst</b>", "<b>Noisy detection rules.</b>",
     "<b>It rewards exactly the volume problem</b> that makes detection "
     "programmes fail (Module 09 &sect;3)."]],
   [0.24, 0.30, 0.46]),
  ("p", "<b>Every row is an instance of Goodhart's law</b> — a "
        "measure adopted as a target ceases to measure what it "
        "measured — <b>and the value of the table is that it names "
        "the <i>specific</i> distortion each metric produces</b>, which is "
        "what lets you predict the behaviour before you deploy the metric "
        "rather than after."),

  ("h1", "2 &nbsp; Better metrics"),
  ("ul", ["<b>Time from advisory publication to patched in "
          "production</b>, reported at the median <i>and</i> the 95th "
          "percentile — <b>the tail is where the risk is</b> "
          "(Module 08 &sect;4), and a good median with a terrible tail "
          "is the common and dangerous shape.",
          "<b>Mean time to detect, measured against deliberately "
          "injected test events</b> — <b>which is measurable "
          "continuously without waiting for a real incident</b>, and it "
          "tests the whole chain from log to alert to person "
          "(Module 09 &sect;2).",
          "<b>Percentage of accounts on origin-bound second "
          "factors</b> — <b>a specific, high-value, countable "
          "control</b> whose improvement is genuinely an improvement "
          "(Module 02 &sect;1), unlike a count of controls in "
          "general.",
          "<b>Inventory query time</b> — <b>'can you locate every "
          "deployment of a given library version in under five minutes' is "
          "a real capability test</b> (Module 08 &sect;3) and is the "
          "metric that would have distinguished organisations during the "
          "major logging advisory.",
          "<b>And tabletop exercise findings closed</b>, which measures "
          "whether learning turns into change (Module 10 &sect;4) "
          "rather than into documents. <b>Each of these measures a "
          "<i>capability</i> rather than a count</b>, and <b>each is hard "
          "to improve without actually improving.</b>"]),
  ("callout", "Prefer metrics you cannot improve without improving",
   ["<b>Ask of every candidate metric: what is the cheapest way to "
    "improve this number <i>without</i> improving security?</b> <b>Five "
    "minutes of adversarial thinking per metric.</b>",
    "<b>If there is a cheap way, the metric will be gamed</b> — "
    "<b>not through dishonesty, but because people reasonably optimise "
    "what is measured and rewarded, and that is what you asked for.</b> "
    "Treating the resulting behaviour as a failure of integrity is a "
    "misdiagnosis.",
    "<b>And prefer measured capabilities over counted "
    "artefacts:</b> <b>'we detected the injected event in four minutes' "
    "cannot meaningfully be faked</b>, and <b>'we have forty detection "
    "rules' can be improved by writing a forty-first that fires on "
    "nothing.</b>",
    "<b>Which is CSCE 633 Module 12's choose-the-metric-from-the-use "
    "discipline and CSCE 642 Module 12's honest reporting</b>, "
    "<b>arriving in the subject where the incentive to look good is "
    "strongest</b> (&sect;4) and the ability to check is weakest "
    "(&sect;1)."]),

  ("break",),
  ("h1", "3 &nbsp; Risk"),
  ("callout", "Risk quantification is useful for comparison and not for "
              "absolute numbers",
   ["<b>Expected loss is probability times impact</b> — and <b>for "
    "a rare event you have essentially no data on the probability</b>, so "
    "the first factor is an estimate with very wide uncertainty.",
    "<b>So an absolute figure is a guess with decimal places attached</b>, "
    "and <b>presenting it as a measurement is misleading in a way that a "
    "stated range with its assumptions is not</b> — the number "
    "acquires authority it has not earned the moment it enters a "
    "spreadsheet.",
    "<b>But <i>comparative</i> estimates are genuinely useful:</b> "
    "<b>'this risk is roughly ten times that one' is defensible from far "
    "weaker evidence, and it is enough to order a budget</b> — which "
    "is what the exercise is actually for. <b>Ordering does not require "
    "calibration; magnitude does.</b>",
    "<b>And the discipline of estimating is valuable even when the "
    "resulting number is not</b> — <b>it forces the assumptions to "
    "be written down explicitly, and an explicit assumption can be argued "
    "with and tested</b> (CSCE 669 Module 12 &sect;4's sensitivity "
    "analysis, which is the right follow-up to any risk figure)."]),

  ("h1", "4 &nbsp; Incentives"),
  ("ul", ["<b>Security spending is invisible when it works</b>, so it "
          "<b>competes badly against features, which are visible</b> "
          "— and the competition is for the same budget and the same "
          "engineering time.",
          "<b>The person who bears the cost of a control is frequently "
          "not the person who bears the risk of its absence</b> — "
          "<b>which is the externality at the centre of Anderson's "
          "security-economics argument</b>, and it explains a great deal "
          "that looks like irrationality.",
          "<b>Compliance is measurable and security is not</b> "
          "(&sect;1), so <b>budgets flow to compliance</b> — and "
          "<b>a fully compliant system can be insecure</b>, which is not a "
          "criticism of any particular standard but a consequence of what "
          "can be audited.",
          "<b>And a prevented incident produces no evidence at "
          "all</b>, so <b>the team that quietly prevents incidents looks "
          "idle beside the team that responds visibly and well to "
          "them</b> — which is a career incentive pointing the wrong "
          "way.",
          "<b>Which is precisely why &sect;2's capability metrics "
          "matter</b> — <b>they give the invisible work something "
          "visible to point at</b>, which is their organisational function "
          "quite apart from their measurement value. <b>The externality is "
          "the deepest of these problems:</b> a vendor's insecure default "
          "costs its users and not the vendor, <b>which is why "
          "Module 11 &sect;3's defaults needed regulation to change in "
          "several cases</b> rather than changing on their own."]),
  ("callout", "What to do about measurement",
   ["<b>Pick a small number of capability metrics</b> (&sect;2) <b>and "
    "track them over time</b> — <b>five is better than fifty</b>, "
    "because fifty cannot be acted on and will include several from "
    "&sect;1's table.",
    "<b>State explicitly what they do not measure</b>, so that <b>the "
    "dashboard is not mistaken for coverage</b> — which is the "
    "specific failure of a security dashboard: it makes the measured "
    "portion look like the whole.",
    "<b>Test capabilities rather than counting artefacts</b> — "
    "<b>injected detection events, tabletop exercises, timed inventory "
    "queries, and executed credential rotations</b>, all of which resist "
    "gaming because the only way to pass is to work.",
    "<b>And report the threats you have accepted</b> (Module 01 "
    "&sect;2's fourth option) <b>alongside the controls you have "
    "implemented</b> — <b>which is the single piece of reporting "
    "that conveys the actual position</b>, and it is the one almost never "
    "included, because a list of accepted risks reads as an admission "
    "rather than as a decision."]),
 ],
 "resources": [
   ("Anderson &mdash; Security Engineering, the economics chapter (free "
    "PDF)",
    "https://www.cl.cam.ac.uk/~rja14/book.html",
    "<b>&sect;4's incentive problems, developed properly</b> — and "
    "the externality argument is the most important idea in this "
    "module."),
   ("Hubbard & Seiersen &mdash; How to Measure Anything in "
    "Cybersecurity Risk",
    "https://web.archive.org/web/20221020051430/http://www.wiley.com/en-us/How+to+Measure+Anything+in+Cybersecurity+Risk-p-9781119085294",
    "<b>&sect;3's case for quantification</b>, argued at length — "
    "read alongside this module's caveat about absolute figures. Library "
    "copy."),
   ("Verizon DBIR and the Cyentia reports (free)",
    "https://www.verizon.com/business/resources/reports/dbir/",
    "<b>The nearest thing to population-level data</b> — which is "
    "what individual organisations lack (&sect;1)."),
   ("Goodhart, and Muller &mdash; The Tyranny of Metrics",
    "https://press.princeton.edu/books/hardcover/9780691174952/the-tyranny-of-metrics",
    "<b>&sect;1's table as a general phenomenon</b> — the same "
    "distortion documented across medicine, education, and policing."),
 ],
 "exercises": [
   "<b>List the security metrics your organisation reports</b> and "
   "classify each against §1's table.",
   "<b>For each, name the cheapest way to improve it without improving "
   "security.</b>",
   "<b>Propose five capability metrics</b> from §2 and say what each "
   "would cost to collect.",
   "<b>Measure your time to detect</b> with an injected event.",
   "<b>Measure your inventory query time</b> for a specific library "
   "version.",
   "<b>Measure your patch time at the median and the 95th "
   "percentile</b>, and report the gap.",
   "<b>Produce a comparative risk ranking</b> for five threats, with the "
   "assumptions written down.",
   "<b>Vary your least-confident assumption</b> and report whether the "
   "ranking changes.",
   "<b>Identify one externality</b> in your own system — a cost you "
   "impose on someone else.",
   "<b>Write your accepted-risk list</b> and put it next to your control "
   "list.",
 ],
 "selfcheck": [
   "Why does security resist measurement, and what does a quiet year "
   "mean?",
   "Why is there no statistical signal in your own history?",
   "Give six misleading metrics and the distortion each produces.",
   "What law are they all instances of?",
   "Give five better metrics and what they have in common.",
   "State the selection criterion for a metric.",
   "What is risk quantification good for, and not good for?",
   "Why is the estimating discipline worth more than the number?",
   "Name four incentive problems and say which is deepest.",
   "Give four things to do about measurement.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Claiming Security Honestly",
 "subtitle": "What an assessment establishes.",
 "question": "What can you actually say about a system's security?",
 "outcomes": [
     "State what a security assessment does and does not "
     "establish.",
     "Avoid the standard overclaims.",
     "Write a security position that is checkable.",
     "Place this course relative to CSCE 711 and CSCE 713.",
     "State the programme that is proportionate for a real system.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What an assessment is",
   "blurb": "An incomplete search."},

  {"t": "callout", "title": "Every assessment is a bounded search, and the bound is the finding",
   "kind": "The honest framing",
   "body": ["<b>A penetration test, a code review, and a scan are all "
            "searches with a time budget, a scope, and a method</b> "
            "— and <b>each finds what its method finds.</b>",
            "<b>So 'no findings' means 'this method, in this time, on "
            "this scope, found nothing'</b> — which is useful and is "
            "not a clean bill of health "
            "(Module 01 §1).",
            "<b>And the scope is where the real limitation "
            "usually is:</b> <b>an assessment that excluded the admin "
            "interface, the mobile client, or the third-party "
            "integration has excluded where the finding was.</b>",
            "<b>So report the scope, the method, the time spent, and "
            "what was not examined</b> — <b>which makes the report a "
            "measurement rather than a verdict</b>, and is the difference "
            "between a useful assessment and a reassuring one."]},

  {"t": "table", "kicker": "Overclaims", "title": "The standard overclaims, corrected",
   "header": ["Claim", "Correction"],
   "widths": [4.6, 6.4],
   "rows": [
     ["<b>'The system is secure'</b>", "<b>Not a supportable statement. Against which adversary, for which assets?</b>"],
     ["<b>'We passed the penetration test'</b>", "<b>A bounded search found nothing in scope in the time available</b>"],
     ["<b>'We are compliant, so we are secure'</b>", "<b>Compliance is auditable and security is not (M12 §4)</b>"],
     ["<b>'We use encryption'</b>", "<b>Which data, at rest or in transit, with keys held where? (M07)</b>"],
     ["<b>'Military-grade encryption'</b>", "<b>Meaningless. The primitive was never the weak point (M07 §1)</b>"],
     ["<b>'No breaches to date'</b>", "<b>Consistent with no detection capability (M09)</b>"],
   ],
   "footnote": "<b>The last row is the one to internalise:</b> an "
               "organisation with no detection has no breaches by "
               "construction, and its clean record is evidence of "
               "nothing.",
   "note": "The no-breaches row is both the most common claim and the "
           "emptiest."},

  {"t": "section", "label": "Part 2", "title": "The honest position",
   "blurb": "What a security statement should contain."},

  {"t": "bullets", "kicker": "Claims", "title": "What you can honestly assert",
   "items": [
     "<b>'Our threat model covers these adversaries; these threats "
     "are mitigated by these controls; these are accepted, with "
     "reasons.'</b> <b>The whole position, in one sentence.</b>",
     "",
     "<b>'An external assessment of this scope, over ten days, "
     "found three issues, all remediated; it excluded the mobile "
     "client.'</b> <b>Bounded and checkable.</b>",
     "",
     "<b>'94% of accounts use origin-bound second factors; the "
     "remaining 6% are service accounts with scoped "
     "credentials.'</b> <b>A measured control.</b>",
     "",
     "<b>'We detect injected test events in a median of 4 minutes "
     "and a 95th percentile of 40.'</b> <b>A tested "
     "capability</b> (M12 §2).",
     "",
     "<b>And what you cannot say: 'we are secure'</b> — "
     "<b>unqualified, against no stated adversary.</b>",
   ],
   "footnote": "<b>The first form is the one to aim for:</b> controls "
               "mapped to threats, with the acceptances stated — "
               "which is the deliverable of this entire course."},

  {"t": "section", "label": "Part 3", "title": "The semester",
   "blurb": "Three courses, one subject."},

  {"t": "table", "kicker": "Semester 9", "title": "What each course covers",
   "header": ["Course", "Covers", "The honest summary"],
   "widths": [2.3, 3.8, 5.4],
   "rows": [
     ["<b>CSCE 701</b>", "<b>Systems, operations, people</b>", "<b>Where the incidents are</b>"],
     ["<b>CSCE 711</b>", "<b>Cryptographic primitives and protocols</b>", "<b>The part that works, used correctly</b>"],
     ["<b>CSCE 713</b>", "<b>Finding and preventing code defects</b>", "<b>Where the severe bugs are</b>"],
   ],
   "footnote": "<b>The division is by where the failures come from:</b> "
               "<b>operations and configuration, then code defects, and "
               "rarely the cryptography</b> — which is the ordering "
               "the incident data supports.",
   "note": "Framing the three by failure source is the honest "
           "organisation."},

  {"t": "section", "label": "Part 4", "title": "A proportionate programme",
   "blurb": "For a real system, in order."},

  {"t": "bullets", "kicker": "Programme", "title": "What to do, in order, with a finite budget",
   "items": [
     "<b>1 · Threat model</b> (M01) — <b>two days, and it "
     "determines everything after.</b>",
     "",
     "<b>2 · Authentication and authorisation</b> "
     "(M02–03) — <b>origin-bound factors and chokepoint "
     "authorisation. The highest-value controls there are.</b>",
     "",
     "<b>3 · Patch and inventory</b> (M08) — <b>unglamorous "
     "and consistently among the top initial-access vectors.</b>",
     "",
     "<b>4 · Logging, detection, and a tested response "
     "plan</b> (M09–10) — <b>because the above will "
     "fail.</b>",
     "",
     "<b>5 · Then segmentation, egress filtering, and the "
     "rest</b> (M04–06), <b>and remove controls people route "
     "around</b> (M11).",
   ],
   "footnote": "<b>Steps 1 to 4 are where the evidence says the value "
               "is</b>, and step 5 is where most programmes start "
               "— which is the single most useful reordering in this "
               "course."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can build a threat model with correct trust "
            "boundaries, map controls to threats, and state what you have "
            "accepted.</b>",
            "<b>You can review authentication, authorisation, platform "
            "isolation, web, secrets, and the supply chain against the "
            "failures that actually occur</b> — which is the practical "
            "skill.",
            "<b>You can design detection that would catch a control "
            "failure, test it, and run a response exercise</b> — and "
            "<b>you know that most programmes fail operationally rather "
            "than technically.</b>",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it means naming the "
            "adversary and the scope</b> — because <b>'secure' without "
            "those is not a claim at all.</b>"]},
 ],
 "takeaways": [
   "Every assessment is a bounded search, and the scope and method are the "
   "finding as much as the issues are.",
   "'No findings' means this method, in this time, on this scope, found "
   "nothing — which is useful and is not a clean bill of health.",
   "'No breaches to date' is consistent with having no detection "
   "capability, which makes a clean record evidence of nothing.",
   "The honest position is controls mapped to threats with the acceptances "
   "stated, which is this course's deliverable.",
   "The three security courses divide by where failures come from: "
   "operations, then code defects, and rarely the cryptography.",
   "Threat model, identity, patching, and detection are where the evidence "
   "says the value is — and step five is where most programmes "
   "start.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What an assessment is"),
  ("callout", "Every assessment is a bounded search, and the bound is the "
              "finding",
   ["<b>A penetration test, a code review, a dependency scan, and a "
    "configuration audit are all searches with a time budget, a defined "
    "scope, and a particular method</b> — and <b>each finds what its "
    "method is capable of finding, within the time it had.</b>",
    "<b>So 'no findings' means 'this method, in this time, on this scope, "
    "found nothing'</b> — <b>which is genuinely useful information "
    "and is not a clean bill of health</b> (Module 01 &sect;1's second "
    "consequence, which is the governing fact of this module).",
    "<b>And the scope is where the real limitation usually sits:</b> "
    "<b>an assessment that excluded the administrative interface, the "
    "mobile client, the third-party integration, or the build pipeline has "
    "excluded exactly where the finding was</b> — and scope "
    "exclusions are negotiated for cost and schedule reasons rather than "
    "security ones.",
    "<b>So report the scope, the method, the time spent, and explicitly "
    "what was <i>not</i> examined</b> — <b>which makes the report a "
    "measurement rather than a verdict</b>, and <b>is the difference "
    "between a useful assessment and a reassuring one.</b> <b>A report "
    "without a stated exclusion list is incomplete regardless of its "
    "findings.</b>"]),
  ("table", ["The claim", "The correction"],
   [["<b>'The system is secure.'</b>",
     "<b>Not a supportable statement in any form.</b> Secure against "
     "which adversary (Module 01 &sect;2), for which assets, under "
     "which assumptions?"],
    ["<b>'We passed the penetration test.'</b>",
     "<b>A bounded search found nothing in scope in the time "
     "available</b> — and the scope and the time are the "
     "information."],
    ["<b>'We are compliant, therefore we are secure.'</b>",
     "<b>Compliance is auditable and security is not</b> (Module 12 "
     "&sect;4), <b>so budgets flow to compliance</b> — and a fully "
     "compliant system can be insecure."],
    ["<b>'We use encryption.'</b>",
     "<b>Which data, at rest or in transit, with the keys held where and "
     "accessible to whom?</b> (Module 07). The sentence conveys "
     "nothing without those."],
    ["<b>'Military-grade encryption.'</b>",
     "<b>Meaningless as a phrase, and misdirected as a claim</b> — "
     "<b>the primitive was never the weak point</b> (Module 07 "
     "&sect;1)."],
    ["<b>'No breaches to date.'</b>",
     "<b>Entirely consistent with having no detection capability</b> "
     "(Module 09). See the note."]],
   [0.38, 0.62]),
  ("p", "<b>The last row is the one to internalise.</b> <b>An "
        "organisation with no detection capability has no breaches by "
        "construction</b>, and <b>its clean record is evidence of "
        "nothing whatsoever</b> — which means <b>the claim is "
        "strongest from organisations least able to make it and weakest "
        "from those best able to</b>. <b>So the useful question is never "
        "'have you been breached' but 'how would you know', and the answer "
        "to the second tells you what the first is worth.</b>"),

  ("h1", "2 &nbsp; The honest position"),
  ("ul", ["<b>'Our threat model covers these adversaries and these "
          "assets; these threats are mitigated by these controls; these "
          "threats are accepted, for these reasons.'</b> <b>The whole "
          "position, in one sentence</b>, and it is checkable by "
          "someone else.",
          "<b>'An external assessment of this defined scope, over ten "
          "days, found three issues, all since remediated and retested; "
          "the scope excluded the mobile client and the payment "
          "integration.'</b> <b>Bounded, dated, and checkable</b> "
          "(&sect;1).",
          "<b>'94% of employee accounts use origin-bound second "
          "factors; the remaining 6% are service accounts using scoped "
          "short-lived credentials.'</b> <b>A measured, specific, "
          "high-value control</b> (Module 12 &sect;2).",
          "<b>'We detect injected test events at a median of four "
          "minutes and a 95th percentile of forty minutes, measured "
          "weekly.'</b> <b>A tested capability rather than a counted "
          "artefact</b> — the strongest form of security claim "
          "available.",
          "<b>And what you cannot honestly say: 'we are "
          "secure'</b> — unqualified, against no stated adversary, "
          "with no scope. <b>The first form is the one to aim for:</b> "
          "<b>controls mapped to threats with the acceptances "
          "stated</b> — <b>which is the deliverable of this entire "
          "course</b> and of both its projects."]),

  ("break",),
  ("h1", "3 &nbsp; The semester"),
  ("table", ["Course", "What it covers", "The honest summary"],
   [["<b>CSCE 701 (this one)</b>",
     "<b>Systems, operations, architecture, and people.</b>",
     "<b>Where the incidents are</b> — credentials, "
     "misconfiguration, missing authorisation, unpatched dependencies, and "
     "phishing."],
    ["<b>CSCE 711</b>",
     "<b>Cryptographic primitives, protocols, and their correct "
     "use.</b>",
     "<b>The part that works, when used correctly</b> — and the "
     "part whose failures are nearly all in key management, which is "
     "Module 07."],
    ["<b>CSCE 713</b>",
     "<b>Finding and preventing defects in code — memory safety, "
     "fuzzing, static analysis, secure development.</b>",
     "<b>Where the severe bugs are</b> — and where "
     "CSCE 627's undecidability constrains the tooling."]],
   [0.22, 0.34, 0.44]),
  ("p", "<b>The division is by where the failures come from:</b> "
        "<b>operations and configuration first, then code defects, and "
        "only rarely the cryptography</b> — <b>which is the ordering "
        "the published incident data supports</b> (Module 12's reports), "
        "and it is deliberately not the ordering a cryptography-first "
        "curriculum would imply."),

  ("h1", "4 &nbsp; A proportionate programme"),
  ("ul", ["<b>1 &middot; Threat model</b> (Module 01) — <b>two "
          "days of work, and it determines the value of everything "
          "after</b>, because a control not tied to a threat is a guess.",
          "<b>2 &middot; Authentication and authorisation</b> "
          "(Modules 02 and 03) — <b>origin-bound second factors "
          "and chokepoint deny-by-default authorisation</b>. <b>The "
          "highest-value controls available</b>, and the two that address "
          "the leading initial-access and privilege-escalation "
          "vectors.",
          "<b>3 &middot; Patching and inventory</b> (Module 08) "
          "— <b>unglamorous, consistently near the top of the "
          "initial-access data</b>, and the inventory is what makes an "
          "advisory response possible at all.",
          "<b>4 &middot; Logging, detection, and a tested response "
          "plan</b> (Modules 09 and 10) — <b>because everything "
          "above will eventually fail</b> (Module 01 &sect;1's last "
          "row), and the difference between a contained incident and a "
          "catastrophic one is made here.",
          "<b>5 &middot; Then segmentation, egress filtering, platform "
          "hardening, and the web controls</b> (Modules 04 to 06), "
          "<b>and remove the controls people route around</b> "
          "(Module 11 &sect;1). <b>Steps 1 to 4 are where the "
          "evidence says the value is</b>, and <b>step 5 is where most "
          "programmes start</b> — <b>which is the single most useful "
          "reordering in this course.</b>"]),
  ("callout", "Where this course leaves you",
   ["<b>You can build a threat model with correct trust boundaries, "
    "enumerate threats systematically, map controls to them, and state "
    "explicitly what you have accepted</b> — which is the artefact "
    "the whole course is organised around.",
    "<b>You can review authentication, authorisation, platform "
    "isolation, the web surface, secret handling, and the supply chain "
    "against the failures that actually occur</b> rather than against a "
    "generic checklist — <b>which is the practical skill, and it "
    "transfers to systems you did not design.</b>",
    "<b>You can design detection that would catch a specific control "
    "failing, test that it fires, and run a response exercise that finds "
    "the gaps</b> — and <b>you know that most security programmes "
    "fail operationally rather than technically</b> (Module 09 "
    "&sect;4, Module 11), which is the knowledge that stops you "
    "building one that does.",
    "<b>The closing rule is the program's, unchanged across twenty-five "
    "courses:</b> <b>state what you measured, state what you assumed, "
    "and never claim more than you established.</b> <b>In security it "
    "means naming the adversary and the scope</b> — because "
    "<b>'secure' without those is not a claim at all</b>, and the whole "
    "of &sect;1's table is what happens when it is made anyway."]),
 ],
 "resources": [
   ("Anderson &mdash; Security Engineering, the concluding chapters "
    "(free PDF)",
    "https://www.cl.cam.ac.uk/~rja14/book.html",
    "<b>&sect;3 and &sect;4 in context</b>, and the best available "
    "account of why programmes are ordered the way they are rather than "
    "the way they should be."),
   ("OWASP &mdash; Application Security Verification Standard (free)",
    "https://owasp.org/www-project-application-security-verification-standard/",
    "<b>A levelled checklist to review a system against</b>, with the "
    "levels making the proportionality of &sect;4 explicit."),
   ("CIS Critical Security Controls (free)",
    "https://www.cisecurity.org/controls",
    "<b>&sect;4's ordering, as a published prioritisation</b> — and "
    "the implementation groups are a proportionality framework worth "
    "borrowing."),
   ("Verizon DBIR, the initial-access section (free, annual)",
    "https://www.verizon.com/business/resources/reports/dbir/",
    "<b>The evidence behind &sect;4's ordering</b> — reread it "
    "annually and check your programme against it."),
 ],
 "exercises": [
   "<b>Take a security claim your organisation makes publicly</b> and "
   "assess it against §1's table.",
   "<b>Find the scope exclusions</b> in a past assessment report, and "
   "say what they excluded.",
   "<b>Rewrite one claim</b> in §2's first form.",
   "<b>Answer 'how would you know' </b> for a breach of your own "
   "system.",
   "<b>Write the one-sentence position</b> for your system: adversaries, "
   "controls, acceptances.",
   "<b>Compare your actual control spending</b> against §4's "
   "ordering and report the mismatch.",
   "<b>Identify which step you are weakest on</b> and what the next "
   "action is.",
   "<b>Read the current breach report's initial-access section</b> and "
   "check §4's ordering against it.",
   "<b>Revisit what you wrote in Module 01's last exercise.</b>",
   "<b>Project 2 is now due.</b> Submit the logging design, the tested "
   "detections with their predicted alert volumes, the tabletop timeline, "
   "and the blameless post-mortem.",
 ],
 "selfcheck": [
   "Why is every assessment a bounded search, and what should a report "
   "contain?",
   "Where is the real limitation usually found?",
   "Give six overclaims and the correction to each.",
   "Why is 'no breaches to date' the emptiest claim?",
   "Give four honest claim forms and the one you cannot use.",
   "Which form is the course's deliverable?",
   "How do the three security courses divide, and by what principle?",
   "Give the five-step proportionate programme.",
   "Which steps hold the value, and where do most programmes start?",
   "In this course, what does 'state what you assumed' mean?",
 ],
},

]
