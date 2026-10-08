# -*- coding: utf-8 -*-
"""CSCE 678 Distributed Systems and Cloud Computing — original content."""

COURSE = {
    "code": "CSCE 678",
    "title": "Distributed Systems and Cloud Computing",
    "tagline": "Consistency, consensus, and failure — with multiplayer "
               "netcode as the worked example",
    "term": "Semester 5 (with CSCE 620 and CSCE 605)",
    "prereqs": "CSCE 611 Operating Systems; CSCE 608 Database Systems; "
               "CSCE 735 Parallel Computing is helpful",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A replicated system that survives the failures you "
                   "inject into it, with a stated consistency model, "
                   "measured tail latency, and an honest account of what "
                   "it does when the network partitions",
    "description": [
        "Every other course in this program assumed one machine. The "
        "machine might have had many cores (CSCE 735) or a hostile "
        "scheduler (CSCE 611), but it was one machine: when it failed, "
        "everything failed together, and that turns out to have been an "
        "enormous simplification.",
        "<b>The organising fact of this course is partial failure.</b> In "
        "a distributed system, components fail independently and "
        "<i>the survivors cannot tell what happened</i>. A request that "
        "received no reply might have been lost on the way out, executed "
        "and lost on the way back, or be executing still. <b>Those three "
        "cases are indistinguishable from the caller</b>, they demand "
        "different responses, and essentially every difficulty in this "
        "subject traces back to that one ambiguity.",
        "The second theme is that <b>the impossibility results are real "
        "and are routinely misquoted</b>. CAP does not say pick two; FLP "
        "does not say consensus is impossible; eventual consistency is not "
        "a synonym for 'no guarantees'. <b>Module 05 states each result "
        "precisely</b> and says what it actually forbids, because the "
        "folklore versions lead to bad architecture.",
        "The worked example is <b>multiplayer netcode</b>, which is "
        "distributed systems under the hardest constraint in the subject: "
        "<b>a hard real-time deadline, an actively adversarial "
        "participant, and no option to make the user wait.</b> A database "
        "can block for 200 ms and nobody notices. A game cannot block for "
        "16. <b>Modules 09 through 11 show what you do instead</b>, and "
        "the answer — predict locally, reconcile against authority, "
        "and trust the client with nothing — is a genuinely elegant "
        "piece of engineering that is far less widely understood than it "
        "deserves to be.",
    ],
    "outcomes": [
        "Explain partial failure and why it is the central difficulty.",
        "Reason about latency, bandwidth, and protocol choice.",
        "Use logical clocks and explain why physical time is unreliable.",
        "Compare consistency models and choose one deliberately.",
        "State CAP, FLP, and PACELC precisely and say what each forbids.",
        "Explain Raft and implement leader election and log replication.",
        "Design failure detection and membership that tolerates false "
        "positives.",
        "Partition data and apply CRDTs where they fit.",
        "Implement client-side prediction and server reconciliation.",
        "Design for an adversarial client, and operate what you built.",
    ],
    "materials": [
        ("MIT 6.5840 — Distributed Systems (free lectures and labs)",
         "https://pdos.csail.mit.edu/6.824/",
         "<b>The primary source.</b> Complete video lectures, the paper "
         "list, and the Raft labs. The best free distributed systems "
         "course that exists, and the labs are the real value."),
        ("Martin Kleppmann — Designing Data-Intensive Applications",
         "https://dataintensive.net/",
         "<b>The reference for Modules 03 through 08.</b> Unusually "
         "careful about what the guarantees actually are. Library copy; "
         "the author's lecture series is free on YouTube."),
        ("van Steen & Tanenbaum — Distributed Systems (free book)",
         "https://www.distributed-systems.net/index.php/books/ds4/",
         "Free in full. Broader and more systematic than Kleppmann, "
         "stronger on naming, coordination, and the formal material."),
        ("Ongaro & Ousterhout — In Search of an Understandable "
         "Consensus Algorithm (free)",
         "https://raft.github.io/raft.pdf",
         "<b>The Raft paper, and the Module 06 project.</b> Deliberately "
         "written to be implementable, and the visualisation on the same "
         "site is excellent."),
        ("Gaffer On Games — networked physics and game networking "
         "(free)",
         "https://gafferongames.com/",
         "<b>The reference for Modules 09 through 11.</b> Glenn "
         "Fiedler's series on prediction, reconciliation, and snapshot "
         "interpolation is the clearest treatment of netcode available."),
        ("Google — Site Reliability Engineering and the SRE Workbook "
         "(free)",
         "https://sre.google/books/",
         "The Module 13 material: SLOs, error budgets, tail latency, and "
         "what operating a distributed system actually involves."),
    ],
    "tooling": [
        "<b>Go or Rust.</b> Both make concurrent network code tolerable, "
        "and the MIT labs are in Go. <b>Whatever you choose, you need "
        "good concurrency primitives</b>, because every module after the "
        "second is concurrent.",
        "<b>A network simulator or emulator</b> — <code>tc "
        "netem</code> on Linux, Clumsy on Windows, or your own in-process "
        "one. <b>You must be able to add latency, jitter, loss, and "
        "reordering on demand</b>; a system tested only on localhost has "
        "not been tested.",
        "<b>A deterministic test harness</b> that can run the whole "
        "system in one process with a controlled clock and a controlled "
        "scheduler. <b>Module 13 argues this is the only way to debug "
        "these systems</b>, and it must be designed in from the "
        "beginning.",
        "<b>Containers</b>, for running many nodes on one machine. Docker "
        "Compose is enough; a cluster is not required for any of this.",
        "<b>A way to plot latency distributions</b>, including the "
        "percentiles. <b>Means are useless here</b> and Module 13 explains "
        "why at length.",
        "<b>Wireshark or <code>tcpdump</code></b>, for Module 02. Looking "
        "at the actual packets once is worth a great deal.",
    ],
    "projects": [
        {"title": "Replicated state machine", "after": 7,
         "brief": "Implement Raft, or an equivalent consensus protocol, "
                  "and build a replicated key-value store on top of it "
                  "— then break it deliberately and show that it "
                  "survives.",
         "reqs": [
             "<b>Leader election with randomised timeouts</b>, surviving "
             "repeated leader failure.",
             "Log replication with the commit rule stated and tested.",
             "<b>Persistence across restart</b>, so a node that crashes "
             "and returns does not violate safety.",
             "<b>A fault injector:</b> drop messages, delay them, reorder "
             "them, partition the cluster, and kill and restart nodes.",
             "<b>A linearizability checker</b> over the operation history "
             "— Porcupine or Knossos, or your own.",
             "A deterministic replay harness for debugging.",
         ],
         "done": [
             "<b>The linearizability checker passes over thousands of "
             "randomised histories with faults injected throughout.</b> "
             "That is the deliverable, not a demo of it working.",
             "<b>A partition test:</b> split the cluster, show the "
             "minority stops accepting writes, heal it, show it catches "
             "up.",
             "<b>A bug you found with the fault injector</b>, with the "
             "trace that revealed it. If you found none, say how many "
             "histories you checked.",
             "Election latency measured as a distribution across many "
             "leader failures.",
         ]},
        {"title": "Netcode for a real-time simulation", "after": 12,
         "brief": "Take a simulation — ideally your CSCE 649 physics "
                  "project — and make it multiplayer over a hostile "
                  "network, with an authoritative server.",
         "reqs": [
             "<b>An authoritative server</b> that trusts the client for "
             "nothing except its own input.",
             "<b>Client-side prediction with server reconciliation</b>, "
             "including the replay of unacknowledged inputs.",
             "Entity interpolation for remote objects, with the buffer "
             "delay stated.",
             "<b>Measured behaviour at 50, 150, and 300 ms RTT, and at "
             "1%, 5%, and 10% packet loss</b>, with jitter.",
             "<b>A cheating attempt you implemented and your server "
             "defeated</b> — a speedhack, a teleport, or a fabricated "
             "hit.",
             "Bandwidth measured per client per second.",
         ],
         "done": [
             "<b>A video or frame sequence at each latency and loss "
             "setting</b>, so the degradation is visible rather than "
             "asserted.",
             "<b>A plot of reconciliation corrections against latency</b> "
             "— how often the server disagreed with the prediction, "
             "and by how much.",
             "<b>The cheat demonstrated and then shown to fail</b>, with "
             "the server-side check that caught it.",
             "<b>An honest statement of what still feels bad</b>, and at "
             "what latency your approach stops working. Every netcode has "
             "that point.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Partial Failure",
 "subtitle": "The thing that makes all of this hard.",
 "question": "Why is a distributed system not just a program on several "
             "machines?",
 "outcomes": [
     "Explain partial failure and why it has no single-machine analogue.",
     "Explain why a timeout cannot distinguish the cases it must.",
     "State the eight fallacies and give a consequence of each.",
     "Distinguish the failure models and say which to assume.",
     "Decide honestly whether to distribute at all.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The central difficulty",
   "blurb": "Components fail independently, and nobody can tell."},

  {"t": "callout", "title": "On one machine, everything fails together",
   "kind": "The simplification you are giving up",
   "body": ["<b>A function call either returns, or the process dies and "
            "the question is moot.</b> There is no third outcome.",
            "<b>So single-machine error handling has two cases</b>, and "
            "one of them you do not have to handle.",
            "<b>In a distributed system, components fail "
            "independently</b> — and the ones still running must continue "
            "without knowing what happened to the others.",
            "<b>That is partial failure, and it has no single-machine "
            "analogue at all.</b> It is not a harder version of a familiar "
            "problem; it is a new one."]},

  {"t": "code", "kicker": "The ambiguity", "title": "What a timeout actually tells you",
   "lang": "text", "code": """
  You send a request. The timeout expires. What happened?

    (a) the request was lost on the way out
            -> the server never saw it. Safe to retry.

    (b) the server received it, executed it, and the REPLY
        was lost on the way back
            -> already done. Retrying does it TWICE.

    (c) the server is still working on it
            -> retrying may run it CONCURRENTLY with itself.

    (d) the server is dead
            -> retry elsewhere, if there is an elsewhere.

    (e) the network is partitioned and the server is fine,
        serving other clients perfectly well
            -> you are the one who is cut off. Retrying
               achieves nothing until the partition heals.

  THESE ARE INDISTINGUISHABLE FROM THE CALLER. There is no
  measurement, no protocol, and no amount of waiting that
  separates them, because the evidence you need is on the
  other side of the thing that is broken.

  A longer timeout does not help. It only makes you slower
  to be wrong.
""",
   "caption": "<b>Every difficulty in this course descends from this "
              "slide.</b> Idempotence, consensus, and exactly-once are all "
              "responses to it.",
   "note": "Spend real time here. If this lands, the rest of the course "
           "is explanation."},

  {"t": "callout", "title": "The responses, and what each actually buys",
   "kind": "How the subject answers the ambiguity",
   "body": ["<b>Make operations idempotent.</b> Then (a) and (b) stop "
            "differing, because doing it twice equals doing it once. "
            "<b>The cheapest fix available, and it should be the "
            "default.</b>",
            "<b>Assign a unique request ID and deduplicate.</b> Idempotence "
            "for operations that are not naturally idempotent.",
            "<b>Use consensus to agree what happened</b> (Module 06) "
            "— expensive, and it makes the ambiguity someone else's "
            "problem.",
            "<b>Or accept it and reconcile later</b> — which is what "
            "eventual consistency (Module 04) and netcode (Module 10) both "
            "do. <b>'Exactly once' delivery does not exist;</b> at-least-"
            "once plus idempotence is what people mean by it."]},

  {"t": "section", "label": "Part 2", "title": "The fallacies",
   "blurb": "Eight assumptions that are all false."},

  {"t": "table", "kicker": "Fallacies", "title": "The eight fallacies of distributed computing",
   "header": ["Assumption", "Reality", "Consequence"],
   "widths": [2.8, 4.2, 5.1],
   "rows": [
     ["<b>The network is reliable</b>", "<b>Packets are lost routinely</b>", "<b>Every call needs a failure path</b>"],
     ["<b>Latency is zero</b>", "<b>Physics: ~100 ms round the world</b>", "<b>Chatty interfaces collapse</b>"],
     ["Bandwidth is infinite", "It is shared and metered", "Payload size is a design decision"],
     ["<b>The network is secure</b>", "<b>It is not, inside or out</b>", "<b>Authenticate; assume hostility</b>"],
     ["Topology does not change", "It changes constantly", "Discovery, not configuration"],
     ["<b>There is one administrator</b>", "There are many, uncoordinated", "<b>Version skew is permanent</b>"],
     ["Transport cost is zero", "<b>Serialisation and egress cost</b>", "<b>Cloud bills are mostly egress</b>"],
     ["<b>The network is homogeneous</b>", "Nothing is", "Protocols must negotiate"],
   ],
   "footnote": "<b>Deutsch and Gosling, 1994 and after.</b> Every one is "
               "still routinely assumed, usually implicitly.",
   "note": "The egress-cost row is the one that surprises people with a "
           "cloud bill."},

  {"t": "callout", "title": "Latency is a physics problem, and it does not improve",
   "kind": "The fallacy worth dwelling on",
   "body": ["<b>Light in fibre travels about 200,000 km/s.</b> New York "
            "to London and back is roughly 56 ms at best, and real routes "
            "are not great circles.",
            "<b>Bandwidth has improved by orders of magnitude; latency "
            "has not and cannot.</b> It is bounded by the speed of light "
            "and the route.",
            "<b>So a design that makes ten sequential round trips costs "
            "ten times the RTT</b>, no matter how fast the link is.",
            "<b>Batch, pipeline, and move computation to the data.</b> "
            "<b>This is the same argument as CSCE 735 Module 10's "
            "α + nβ model</b> — latency is per message and is "
            "paid regardless of size."]},

  {"t": "section", "label": "Part 3", "title": "Failure models",
   "blurb": "What you assume can go wrong."},

  {"t": "table", "kicker": "Models", "title": "What kind of failure are you tolerating?",
   "header": ["Model", "Nodes may", "Cost"],
   "widths": [2.9, 4.4, 4.8],
   "rows": [
     ["<b>Crash-stop</b>", "<b>Stop, and never come back</b>", "<b>Simplest. Often unrealistic</b>"],
     ["<b>Crash-recovery</b>", "<b>Stop and return, possibly amnesiac</b>", "<b>Needs durable state. The usual model</b>"],
     ["<b>Omission</b>", "Drop messages", "Covered by retries"],
     ["<b>Byzantine</b>", "<b>Behave arbitrarily, including maliciously</b>", "<b>Needs 3f+1 nodes, not 2f+1</b>"],
     ["Fail-stop", "Stop <i>detectably</i>", "<b>Convenient and rarely available</b>"],
   ],
   "footnote": "<b>Assume crash-recovery for internal systems</b>, and "
               "<b>Byzantine when a participant may be an adversary</b> "
               "— which in a game is every client (Module 11).",
   "note": "The game connection makes Byzantine concrete rather than "
           "exotic."},

  {"t": "section", "label": "Part 4", "title": "Whether to distribute",
   "blurb": "The question to answer first."},

  {"t": "callout", "title": "Distribution is a cost you pay for a specific benefit",
   "kind": "The decision",
   "body": ["<b>The legitimate reasons:</b> the data or the load exceeds "
            "one machine; the users are geographically spread and latency "
            "matters; or <b>the system must survive a machine failing</b>.",
            "<b>The illegitimate ones:</b> it seems more professional; "
            "microservices are the default; the team is large so the "
            "system should be too.",
            "<b>What it costs:</b> partial failure, no global clock, "
            "debugging that spans processes, and an operational burden "
            "that never goes away.",
            "<b>A single machine with 2 TB of RAM and 128 cores handles a "
            "great deal</b>, and this is the third time this program has "
            "made that argument — CSCE 608 M13 and CSCE 735 M10 both got "
            "there independently."]},

  {"t": "bullets", "kicker": "Setup", "title": "What to have working before Module 02",
   "items": [
     "<b>Go or Rust</b>, and a trivial TCP and UDP echo client and "
     "server in it.",
     "",
     "<b>A network impairment tool</b> — <code>tc netem</code>, Clumsy, "
     "or your own proxy. <b>Add 200 ms and 5% loss to your echo and watch "
     "it suffer.</b>",
     "",
     "<b>Wireshark</b>, and a capture of your own echo traffic. Look at "
     "the actual bytes once.",
     "",
     "<b>A latency plotting setup</b> that shows percentiles, not means.",
     "",
     "<b>And Docker Compose</b>, so you can run five nodes on one "
     "machine from the start.",
   ],
   "footnote": "<b>The impairment tool is the important one.</b> "
               "Everything in this course behaves differently on a real "
               "network, and localhost lies."},
 ],
 "takeaways": [
   "On one machine everything fails together; in a distributed system "
   "components fail independently and the survivors cannot tell what "
   "happened.",
   "A timeout cannot distinguish a lost request, a lost reply, a slow "
   "server, a dead server, or a partition — and no longer timeout "
   "helps.",
   "Idempotence is the cheapest response and should be the default; "
   "'exactly once' delivery does not exist.",
   "Latency is bounded by physics and has not improved like bandwidth has, "
   "so sequential round trips are the thing to design away.",
   "Assume crash-recovery for internal systems and Byzantine wherever a "
   "participant may be an adversary — which in a game is every client.",
   "Distribute for data size, geography, or fault tolerance; not for "
   "appearances. One large machine still goes a long way.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The central difficulty"),
  ("callout", "On one machine, everything fails together",
   ["<b>A function call either returns a result, or the process dies and "
    "the question of what it returned is moot.</b> There is no third "
    "outcome, and that fact is quietly load-bearing in every "
    "single-machine program ever written.",
    "<b>So single-machine error handling has two cases</b>, and one of them "
    "— the process dying — you do not have to handle, because "
    "there is nobody left to handle it.",
    "<b>In a distributed system, components fail independently</b>, and the "
    "components still running must carry on <i>without knowing what "
    "happened to the others</i>. Some of them are fine, some are gone, some "
    "are merely unreachable, and from the inside these look identical.",
    "<b>That is partial failure, and it has no single-machine "
    "analogue.</b> It is worth being precise about this: distribution is "
    "not a harder version of a problem you already know how to solve. "
    "<b>It introduces a failure mode that simply does not exist on one "
    "machine</b>, and essentially everything in this course is a response "
    "to it."]),
  ("code", """You send a request. The timeout expires. What happened?

  (a) the request was lost on the way out
          -> the server never saw it.  Safe to retry.
  (b) the server executed it and the REPLY was lost
          -> already done.  Retrying does it TWICE.
  (c) the server is still working on it
          -> retrying may run it CONCURRENTLY with itself.
  (d) the server is dead
          -> retry elsewhere, if there is an elsewhere.
  (e) the network is partitioned; the server is fine and is
      serving other clients perfectly well
          -> YOU are the one cut off.  Retrying achieves
             nothing until the partition heals.

THESE ARE INDISTINGUISHABLE FROM THE CALLER.  No measurement,
no protocol and no amount of waiting separates them, because
the evidence is on the far side of the thing that is broken.

A longer timeout only makes you slower to be wrong."""),
  ("p", "<b>Every difficulty in this course descends from that "
        "ambiguity.</b> Idempotence, deduplication, consensus, "
        "linearizability, leases, fencing tokens, and client-side "
        "prediction are all responses to it, and recognising them as such "
        "is most of what makes the subject coherent rather than a list of "
        "techniques."),
  ("callout", "The responses, and what each actually buys",
   ["<b>Make operations idempotent.</b> If applying an operation twice has "
    "the same effect as applying it once, then cases (a) and (b) stop "
    "differing and the caller can simply retry. <b>This is the cheapest "
    "fix available and it should be the default</b> — design the "
    "operation to be idempotent rather than designing the protocol to "
    "avoid duplicates.",
    "<b>Assign a unique request identifier and deduplicate at the "
    "server.</b> This is idempotence bolted onto operations that are not "
    "naturally idempotent (incrementing a counter, appending to a list), "
    "at the cost of the server remembering which identifiers it has seen "
    "— which is itself state that must be bounded and replicated.",
    "<b>Use consensus to agree on what happened</b> (Module 06). Correct, "
    "expensive, and it does not remove the ambiguity so much as move it "
    "into a subsystem built specifically to survive it.",
    "<b>Or accept the ambiguity and reconcile afterwards</b> — which "
    "is what eventual consistency (Module 04) and netcode reconciliation "
    "(Module 10) both do, in very different settings. <b>And note: "
    "'exactly once' message delivery does not exist.</b> It is provably "
    "impossible over an unreliable network. <b>What people mean by it is "
    "at-least-once delivery plus idempotent processing</b>, which produces "
    "exactly-once <i>effects</i> — a genuinely different and "
    "achievable thing, and worth insisting on the distinction when "
    "someone's design document claims the former."]),

  ("h1", "2 &nbsp; The eight fallacies"),
  ("table", ["The assumption", "The reality", "The consequence"],
   [["<b>The network is reliable.</b>",
     "<b>Packets are lost, duplicated, and reordered as a matter of "
     "routine</b>, not as an exception.",
     "<b>Every remote call needs a failure path</b>, and that path needs "
     "testing as much as the success path."],
    ["<b>Latency is zero.</b>",
     "<b>Physics puts a floor of roughly 100 ms on a round trip across the "
     "world</b>, and real routes are worse.",
     "<b>Chatty interfaces collapse.</b> See the callout below."],
    ["<b>Bandwidth is infinite.</b>",
     "It is shared, variable, and metered.",
     "Payload size is a design decision, not an implementation detail."],
    ["<b>The network is secure.</b>",
     "<b>It is not, and the inside of your datacentre is not either.</b>",
     "<b>Authenticate every hop and assume hostility</b> — which in "
     "a game means assuming the client is the attacker (Module 11)."],
    ["<b>Topology does not change.</b>",
     "Nodes come and go constantly; addresses change under you.",
     "Service discovery, not configuration files."],
    ["<b>There is one administrator.</b>",
     "There are many, and they are not coordinated.",
     "<b>Version skew is permanent</b>, so every protocol change must be "
     "compatible in both directions for a while."],
    ["<b>Transport cost is zero.</b>",
     "<b>Serialisation costs CPU and egress costs money.</b>",
     "<b>Cloud bills are substantially egress charges</b>, which surprises "
     "people who budgeted for compute (Module 12)."],
    ["<b>The network is homogeneous.</b>", "Nothing is.",
     "Protocols must negotiate rather than assume."]],
   [0.22, 0.36, 0.42]),
  ("callout", "Latency is a physics problem and it does not improve",
   ["<b>Light travels through optical fibre at roughly 200,000 km per "
    "second</b> — about two-thirds of its speed in vacuum, because of "
    "the refractive index of glass. New York to London and back is about "
    "56 ms at the theoretical best, and real fibre routes are not great "
    "circles.",
    "<b>Bandwidth has improved by orders of magnitude over four decades. "
    "Latency has not, and cannot.</b> It is bounded below by the speed of "
    "light and the physical route, and the remaining overhead is switching "
    "and queueing, which are already small.",
    "<b>So a design that makes ten sequential round trips costs ten times "
    "the RTT</b>, regardless of how fast the link is. Upgrading the "
    "connection does nothing; the requests are waiting on each other, not "
    "on the wire.",
    "<b>Batch requests, pipeline them, and move computation to the "
    "data.</b> <b>This is precisely CSCE 735 Module 10's "
    "&alpha; + n&beta; model</b> — the latency term is paid per "
    "message regardless of size, so fewer and larger is better. <b>The "
    "same conclusion, derived twice in two different courses</b>, which "
    "suggests it is a property of communication rather than of any "
    "particular system."]),

  ("break",),
  ("h1", "3 &nbsp; Failure models"),
  ("table", ["Model", "Nodes may", "What it costs to tolerate"],
   [["<b>Crash-stop</b>", "<b>Stop, and never return.</b>",
     "<b>The simplest model to reason about, and often unrealistic</b> "
     "— real machines reboot and come back."],
    ["<b>Crash-recovery</b>",
     "<b>Stop and later return, possibly having lost everything not "
     "written durably.</b>",
     "<b>Requires durable state and careful recovery</b>, because a "
     "returning node must not contradict what it promised before it "
     "crashed. <b>The right model for most internal systems.</b>"],
    ["<b>Omission</b>", "Drop messages, sent or received.",
     "Mostly covered by retries and idempotence (&sect;1)."],
    ["<b>Byzantine</b>",
     "<b>Behave arbitrarily, including lying, equivocating, and "
     "colluding.</b>",
     "<b>Requires 3f+1 nodes to tolerate f failures rather than 2f+1</b>, "
     "with substantially more messages and cryptographic signing. "
     "Expensive, and sometimes unavoidable."],
    ["<b>Fail-stop</b>",
     "Stop, <i>and the failure is reliably detectable by others</i>.",
     "<b>Extremely convenient and almost never actually available</b> "
     "— &sect;1 explains why detection is the hard part."]],
   [0.17, 0.35, 0.48]),
  ("p", "<b>Assume crash-recovery for systems you control</b>, and "
        "<b>Byzantine wherever a participant may be an adversary</b>. That "
        "second case is not exotic: <b>in a multiplayer game, every client "
        "is a potentially Byzantine node</b> running on hardware the "
        "attacker owns, with a debugger attached (Module 11). The game "
        "industry's answer — a single authoritative server that trusts "
        "no client — is a pragmatic alternative to Byzantine consensus "
        "that works because there is a natural trusted party."),

  ("h1", "4 &nbsp; Whether to distribute at all"),
  ("callout", "Distribution is a cost paid for a specific benefit",
   ["<b>The legitimate reasons are three.</b> The data or the load genuinely "
    "exceeds what one machine can hold or handle; the users are "
    "geographically distributed and latency to a single location would be "
    "unacceptable; or <b>the system must survive the failure of a "
    "machine</b>, which no single machine can do by definition.",
    "<b>The illegitimate ones are also three.</b> It seems more "
    "professional; microservices are what everyone does; the team is large "
    "so the architecture should be too (Conway's law applied "
    "backwards, as a justification rather than a warning).",
    "<b>What it costs:</b> partial failure in every code path, no global "
    "clock (Module 03), debugging that spans processes and machines, "
    "consistency decisions that must be made explicitly (Module 04), and "
    "<b>an operational burden that never goes away</b> (Module 13).",
    "<b>A single machine with two terabytes of memory and 128 cores "
    "handles a great deal.</b> <b>This is the third time this program has "
    "reached that conclusion</b> — CSCE 608 Module 13 argued it about "
    "databases and CSCE 735 Module 10 argued it about MPI — and three "
    "independent derivations of the same advice is reasonable evidence "
    "that the reflex to distribute is both strong and frequently "
    "unexamined."]),
  ("ul", ["<b>Go or Rust</b>, with a trivial TCP and UDP echo client and "
          "server working. Everything after Module 02 builds on this.",
          "<b>A network impairment tool</b> — <code>tc netem</code> on "
          "Linux, Clumsy on Windows, or a small proxy of your own that "
          "delays and drops. <b>Add 200 ms of latency and 5% loss to your "
          "echo and watch what happens</b>; it is the single most useful "
          "ten minutes in the course.",
          "<b>Wireshark</b>, and a capture of your own traffic. <b>Looking "
          "at the actual bytes once</b> makes Module 02 concrete in a way "
          "no description does.",
          "<b>A plotting setup that shows percentiles rather than "
          "means.</b> Module 13 explains at length why means are useless "
          "here, and it is easier to have built the right thing from the "
          "start.",
          "<b>Docker Compose</b>, so that running five nodes on one machine "
          "is one command. <b>A system you can only run as a single "
          "instance will not get tested as a distributed one</b>, and "
          "localhost without impairment lies about everything that "
          "matters."]),
 ],
 "resources": [
   ("MIT 6.5840 &mdash; lecture 1, introduction (free)",
    "https://pdos.csail.mit.edu/6.824/",
    "The &sect;1 framing and the course's overall shape. Watch it this "
    "week."),
   ("Deutsch & Gosling &mdash; The Eight Fallacies of Distributed "
    "Computing (free)",
    "https://nighthacks.com/jag/res/Fallacies.html",
    "The &sect;2 list, from the people who wrote it down. One page, and "
    "still entirely current."),
   ("Peter Bailis & Kyle Kingsbury &mdash; The Network Is Reliable (free)",
    "https://queue.acm.org/detail.cfm?id=2655736",
    "<b>Evidence for the first fallacy</b>, collected from real production "
    "incidents. Read it before deciding your network is fine."),
   ("Kleppmann &mdash; Designing Data-Intensive Applications, chapter 8 "
    "('The Trouble with Distributed Systems')",
    "https://dataintensive.net/",
    "<b>The best single treatment of &sect;1 and &sect;3</b>, including "
    "unreliable clocks and the process-pause problem."),
 ],
 "exercises": [
   "Write a TCP and a UDP echo client and server.",
   "<b>Add 200 ms latency and 5% loss</b> with an impairment tool and "
   "measure both. Report the difference in behaviour.",
   "<b>Construct each of the five timeout cases</b> from &sect;1 "
   "deliberately, and confirm your client cannot tell them apart.",
   "Implement a non-idempotent operation (increment a counter) and "
   "demonstrate a double-apply under retry.",
   "<b>Make it idempotent with a request ID and deduplication</b>, and "
   "show the double-apply is gone.",
   "Measure RTT to five servers around the world and compare against the "
   "speed-of-light floor for each distance.",
   "<b>Build an interface that makes ten sequential round trips</b>, then "
   "batch it into one. Measure both at 5 ms and at 200 ms RTT.",
   "Capture your echo traffic in Wireshark and identify the handshake, "
   "the data, and the teardown.",
   "Take a system you have built and <b>write down honestly whether it "
   "needs to be distributed</b>, against &sect;4's three legitimate "
   "reasons.",
   "Set up Docker Compose running five instances of your echo server.",
 ],
 "selfcheck": [
   "What is partial failure, and why does it have no single-machine "
   "analogue?",
   "Give the five things a timeout cannot distinguish, and say why a "
   "longer timeout does not help.",
   "Name four responses to the ambiguity and what each buys.",
   "Why does 'exactly once' delivery not exist, and what do people mean "
   "by it?",
   "State the eight fallacies with a consequence of each.",
   "Why has latency not improved the way bandwidth has?",
   "Name five failure models and say which to assume when.",
   "Why is every game client a potentially Byzantine node?",
   "Give three legitimate and three illegitimate reasons to distribute.",
 ],
},

]

for _b in ("c678_b2", "c678_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
