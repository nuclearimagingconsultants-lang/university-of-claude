# -*- coding: utf-8 -*-
"""CSCE 678 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Distributed Data",
 "subtitle": "Splitting it up, and putting it back together.",
 "question": "How do you partition data, and transact across partitions?",
 "outcomes": [
     "Compare partitioning schemes and their rebalancing behaviour.",
     "Explain consistent hashing and virtual nodes.",
     "Explain two-phase commit and why it blocks.",
     "Explain sagas and compensating actions.",
     "Explain CRDTs and when they genuinely apply.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Partitioning",
   "blurb": "Deciding where each key lives."},

  {"t": "table", "kicker": "Schemes", "title": "How to split the keyspace",
   "header": ["Scheme", "How", "Problem"],
   "widths": [2.7, 4.3, 5.1],
   "rows": [
     ["<b>Range</b>", "Contiguous key ranges per node", "<b>Hot spots; sequential keys all land together</b>"],
     ["<b>Hash</b>", "<b>hash(key) mod n</b>", "<b>Changing n remaps nearly everything</b>"],
     ["<b>Consistent hashing</b>", "<b>Hash onto a ring; take the next node</b>", "<b>Only 1/n moves. Needs virtual nodes</b>"],
     ["Directory", "An explicit lookup table", "<b>Flexible; the directory is a SPOF</b>"],
     ["<b>By tenant</b>", "All of one customer together", "<b>Simple; one huge tenant breaks it</b>"],
   ],
   "footnote": "<b>hash(key) mod n is the trap:</b> going from 10 to 11 "
               "nodes moves roughly 10/11 of all keys, not 1/11.",
   "note": "That arithmetic is the whole motivation for consistent "
           "hashing."},

  {"t": "callout", "title": "Consistent hashing, and why virtual nodes are mandatory",
   "kind": "The standard solution",
   "body": ["<b>Hash both keys and nodes onto a ring.</b> A key belongs to "
            "the first node clockwise from it.",
            "<b>Adding a node steals keys only from its successor</b>, so "
            "roughly 1/n of the data moves instead of nearly all of it.",
            "<b>But with one point per node the load is badly "
            "uneven</b> — random placement gives some nodes far larger "
            "arcs than others.",
            "<b>So each physical node gets 100–200 virtual points on "
            "the ring.</b> The variance averages out, and removing a node "
            "spreads its load across many others rather than dumping it on "
            "one. <b>Without virtual nodes, consistent hashing does not "
            "work in practice.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Transactions across partitions",
   "blurb": "Atomicity when the data is in several places."},

  {"t": "code", "kicker": "2PC", "title": "Two-phase commit, and why it blocks",
   "lang": "text", "code": """
  PHASE 1 -- PREPARE
      coordinator -> all participants: "can you commit?"
      each participant does the work, makes it durable, and
      replies YES or NO. A YES is a PROMISE it cannot retract.

  PHASE 2 -- COMMIT or ABORT
      if all said YES: coordinator -> all: "commit"
      otherwise:       coordinator -> all: "abort"

  THE PROBLEM:
      a participant that voted YES and then hears nothing is
      STUCK. It cannot commit -- someone may have voted NO.
      It cannot abort -- it promised. It cannot ask the other
      participants, because they may not know either.

      It must HOLD ITS LOCKS AND WAIT for the coordinator.

  So the coordinator is a single point of failure that can
  block the system indefinitely. This is Module 01's timeout
  ambiguity, with locks held.

  THREE-PHASE COMMIT removes the blocking under a synchrony
  assumption that real networks do not satisfy. Modern systems
  instead make the COORDINATOR itself fault-tolerant, by
  running it on consensus (Module 06).
""",
   "caption": "<b>2PC is an atomicity protocol, not a fault-tolerance "
              "protocol.</b> Those are different problems and it only "
              "solves one.",
   "note": "The 'holds locks while stuck' detail is what makes blocking "
           "serious."},

  {"t": "callout", "title": "Sagas: give up atomicity, keep the outcome",
   "kind": "The practical alternative",
   "body": ["<b>Split the transaction into local transactions, each with "
            "a defined <i>compensating</i> action.</b>",
            "<b>Execute them in order; on failure, run the compensations "
            "backwards.</b> Book the flight, book the hotel; if the hotel "
            "fails, cancel the flight.",
            "<b>There is no isolation.</b> Intermediate states are "
            "visible — someone can see the flight booked before the "
            "hotel is.",
            "<b>And compensation is not rollback.</b> You cannot un-send "
            "an email; you send an apology. <b>The business decides what "
            "compensation means</b>, which is why sagas are a domain "
            "modelling exercise rather than an infrastructure one."]},

  {"t": "section", "label": "Part 3", "title": "CRDTs",
   "blurb": "Merging without choosing."},

  {"t": "callout", "title": "CRDTs converge without coordination, by construction",
   "kind": "The idea",
   "body": ["<b>If the merge operation is commutative, associative, and "
            "idempotent, replicas converge regardless of message order or "
            "duplication.</b>",
            "<b>So no coordination is needed at all</b> — no consensus, "
            "no locks, no conflict resolution, and no lost writes "
            "(Module 03 §4).",
            "<b>Examples: a grow-only counter (merge = max per "
            "replica), a grow-only set (merge = union), a last-writer "
            "register with a tiebreak, and sequence CRDTs for "
            "text.</b>",
            "<b>The cost is that not every datatype has one</b>, and "
            "metadata can grow — tombstones for deletions must be kept "
            "so a late-arriving add does not resurrect a removed element."]},

  {"t": "table", "kicker": "Fit", "title": "Where CRDTs apply, and where they do not",
   "header": ["Case", "Works?", "Why"],
   "widths": [3.3, 2.4, 6.4],
   "rows": [
     ["<b>Collaborative text</b>", "<b>Yes</b>", "<b>Sequence CRDTs. This is the flagship use</b>"],
     ["<b>Presence, sets, counters</b>", "<b>Yes</b>", "Natural merge semantics"],
     ["<b>Shopping cart</b>", "Mostly", "<b>Dynamo's example; deleted items can resurrect</b>"],
     ["<b>Bank balance</b>", "<b>No</b>", "<b>'Never go negative' is not mergeable</b>"],
     ["Unique username", "<b>No</b>", "Uniqueness is a global invariant"],
     ["<b>Game world state</b>", "<b>No</b>", "<b>Needs a referee, not convergence</b>"],
   ],
   "footnote": "<b>The rule: CRDTs handle invariants that are local, not "
               "global.</b> Anything requiring 'exactly one' or 'never "
               "below zero' needs coordination.",
   "note": "That local/global invariant distinction is the clean test."},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "The decision."},

  {"t": "bullets", "kicker": "Order", "title": "What to try, in order",
   "items": [
     "<b>1. Keep it on one node.</b> A partition boundary you do not "
     "have costs nothing.",
     "",
     "<b>2. Partition so that transactions stay within one "
     "partition.</b> Co-locate by tenant, by user, by game session.",
     "",
     "<b>3. Use a CRDT</b>, if the invariant is local.",
     "",
     "<b>4. Use a saga</b> with explicit compensations, if the business "
     "can define them.",
     "",
     "<b>5. Use 2PC over a consensus-backed coordinator</b> — correct, "
     "slow, and a real option.",
     "",
     "<b>6. Reconsider the requirement.</b> It is often negotiable and "
     "is rarely asked about.",
   ],
   "footnote": "<b>Step 2 is where the leverage is.</b> Most "
               "cross-partition transactions are an artifact of the "
               "partitioning choice, not of the domain."},
 ],
 "takeaways": [
   "hash(key) mod n remaps nearly everything when n changes; consistent "
   "hashing moves only 1/n, and needs 100–200 virtual nodes per "
   "machine to balance.",
   "Two-phase commit blocks: a participant that voted yes and lost the "
   "coordinator must hold its locks and wait.",
   "2PC is an atomicity protocol, not a fault-tolerance one — modern "
   "systems make the coordinator itself consensus-backed.",
   "Sagas trade isolation for progress, and compensation is not rollback: "
   "the business defines what undoing means.",
   "CRDTs converge without coordination when the merge is commutative, "
   "associative, and idempotent — which covers local invariants and "
   "not global ones.",
   "Most cross-partition transactions are an artifact of the partitioning "
   "choice rather than the domain.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Partitioning"),
  ("table", ["Scheme", "How it works", "The problem with it"],
   [["<b>Range partitioning</b>",
     "Each node owns a contiguous range of the key space.",
     "<b>Hot spots.</b> Sequential keys — timestamps, auto-increment "
     "IDs — all land on one node, so the newest and busiest data is "
     "never spread."],
    ["<b>Hash partitioning</b>", "<b>node = hash(key) mod n.</b>",
     "<b>Changing n remaps almost everything.</b> Going from 10 nodes to "
     "11 moves roughly 10/11 of all keys, not 1/11 — which makes "
     "adding capacity a full data migration."],
    ["<b>Consistent hashing</b>",
     "<b>Hash keys and nodes onto a ring; a key belongs to the first node "
     "clockwise.</b>",
     "<b>Only about 1/n of keys move when a node is added.</b> Requires "
     "virtual nodes to balance — see below."],
    ["<b>Directory</b>",
     "An explicit lookup table mapping key ranges to nodes.",
     "<b>Maximum flexibility</b> — you can move anything anywhere "
     "— <b>and the directory is a single point of failure</b> that "
     "must itself be replicated (Module 06)."],
    ["<b>By tenant</b>", "All of one customer's data on one node.",
     "<b>Simple, and transactions stay local</b>, which is a large "
     "advantage (&sect;4). <b>One enormous tenant breaks it</b>, and there "
     "is always one."]],
   [0.19, 0.33, 0.48]),
  ("callout", "Consistent hashing, and why virtual nodes are mandatory",
   ["<b>Hash both keys and node identifiers onto a ring</b>, and assign "
    "each key to the first node encountered clockwise from its position.",
    "<b>Adding a node takes keys only from its immediate successor on the "
    "ring</b>, so roughly 1/n of the data moves rather than nearly all of "
    "it. That is the entire point, and it is what makes elastic scaling "
    "possible at all.",
    "<b>But with one ring position per node the load is badly uneven.</b> "
    "Random placement of n points on a circle produces arcs of very "
    "different sizes — the largest is typically several times the "
    "average — so some nodes get far more data than others.",
    "<b>So each physical node is given 100 to 200 virtual positions on the "
    "ring.</b> The variance averages out, load becomes close to uniform, "
    "and <b>removing a node spreads its keys across many successors rather "
    "than dumping them all on one</b> — which matters enormously "
    "during a failure, since dumping one node's entire load onto its "
    "neighbour is how a single failure cascades. <b>Without virtual nodes, "
    "consistent hashing does not work in practice</b>, and this is "
    "frequently omitted from descriptions of it."]),

  ("h1", "2 &nbsp; Transactions across partitions"),
  ("code", """PHASE 1 -- PREPARE
    coordinator -> participants: "can you commit?"
    each does the work, makes it DURABLE, replies YES or NO.
    A YES is a PROMISE that cannot be retracted.

PHASE 2 -- COMMIT or ABORT
    all YES -> "commit";  any NO -> "abort"

THE PROBLEM
    a participant that voted YES and then hears nothing is STUCK:
      it cannot commit -- someone may have voted NO
      it cannot abort  -- it promised
      it cannot ask the others -- they may not know either
    so it HOLDS ITS LOCKS AND WAITS.

The coordinator is a single point of failure that can block
the system indefinitely -- Module 01's ambiguity, with locks held.

3PC removes blocking under a synchrony assumption real networks
do not satisfy. Modern systems instead make the COORDINATOR
fault-tolerant by running it on consensus (Module 06)."""),
  ("p", "<b>Two-phase commit is an atomicity protocol, not a "
        "fault-tolerance protocol</b> — it ensures all participants "
        "reach the same decision, and says nothing about what happens when "
        "the decider fails. <b>Those are different problems</b>, and "
        "recognising that 2PC only solves the first explains both why it "
        "blocks and why the modern answer is to compose it with consensus "
        "rather than to replace it."),
  ("callout", "Sagas: give up atomicity, keep the outcome",
   ["<b>Split the distributed transaction into a sequence of local "
    "transactions, each paired with a defined <i>compensating</i> "
    "action</b> that semantically undoes it.",
    "<b>Execute them in order; on failure, run the compensations "
    "backwards.</b> Book the flight, then the hotel, then the car; if the "
    "car fails, cancel the hotel and cancel the flight.",
    "<b>There is no isolation.</b> Intermediate states are visible to "
    "everyone — another observer can see the flight booked while the "
    "hotel is still pending, and can act on that. <b>The application must "
    "be designed to tolerate its own intermediate states being seen</b>, "
    "which is a real constraint and the main reason sagas are harder than "
    "they look.",
    "<b>And compensation is not rollback.</b> You cannot un-send an email; "
    "you send a correction. You cannot un-charge a card; you issue a "
    "refund, which leaves two entries on the statement. <b>The business "
    "decides what compensation means</b> — which makes sagas a domain "
    "modelling exercise rather than an infrastructure one, and is why they "
    "cannot be provided by a library."]),

  ("break",),
  ("h1", "3 &nbsp; CRDTs"),
  ("callout", "Convergence without coordination, by construction",
   ["<b>If the merge operation is commutative, associative, and "
    "idempotent, then replicas converge to the same value regardless of "
    "the order in which updates arrive, how many times they arrive, or "
    "whether they arrive more than once.</b>",
    "<b>So no coordination is required at all</b> — no consensus, no "
    "locks, no conflict resolution rule to argue about, and <b>no silently "
    "lost writes</b> (Module 03 &sect;4). Updates can be applied in any "
    "order by any replica and the result is the same.",
    "<b>The standard examples:</b> a grow-only counter (each replica "
    "counts its own increments; merge takes the maximum per replica and "
    "sums); a grow-only set (merge is union); a two-phase set supporting "
    "removal via tombstones; a last-writer-wins register with a "
    "deterministic tiebreak; and sequence CRDTs for collaborative text.",
    "<b>The cost is that not every datatype has one</b>, and the metadata "
    "can grow without bound. <b>Deletions require tombstones</b> — a "
    "record that the element was removed — kept so that a "
    "late-arriving add does not resurrect it, and garbage-collecting "
    "tombstones safely requires knowing every replica has seen them, which "
    "is itself a coordination problem."]),
  ("table", ["Case", "Does a CRDT work?", "Why"],
   [["<b>Collaborative text editing</b>", "<b>Yes.</b>",
     "<b>Sequence CRDTs</b> — RGA, Logoot, Yjs, Automerge. <b>The "
     "flagship application</b>, and the one that drove most of the "
     "research."],
    ["<b>Presence, tag sets, counters</b>", "<b>Yes.</b>",
     "The merge semantics are natural: union, maximum, sum."],
    ["<b>Shopping cart</b>", "Mostly.",
     "<b>Dynamo's original example.</b> Merging by union never loses an "
     "add, <b>and a deleted item can reappear</b> if the delete and a "
     "concurrent add cross — which Amazon judged preferable to losing "
     "an add."],
    ["<b>Bank balance</b>", "<b>No.</b>",
     "<b>'The balance must never go below zero' is not a mergeable "
     "property.</b> Two replicas can each approve a withdrawal that is "
     "individually valid and jointly is not."],
    ["<b>Unique username</b>", "<b>No.</b>",
     "Uniqueness is a global invariant; convergence cannot establish it "
     "after the fact."],
    ["<b>Game world state</b>", "<b>No.</b>",
     "<b>A game needs a referee, not convergence</b> — who shot whom "
     "first is a decision, not a merge (Module 09)."]],
   [0.23, 0.17, 0.60]),
  ("p", "<b>The clean test: CRDTs handle invariants that are local, not "
        "global.</b> Anything requiring 'exactly one of these exists' or "
        "'this quantity never goes below zero' is a global invariant and "
        "needs coordination, because it is a statement about all replicas "
        "jointly that no replica can check alone."),

  ("h1", "4 &nbsp; Choosing"),
  ("ol", ["<b>Keep it on one node.</b> A partition boundary you do not "
          "have costs nothing to maintain, and single-node transactions "
          "are a solved problem (CSCE 608). This is Module 01 &sect;4's "
          "argument applied at the data layer.",
          "<b>Partition so that transactions stay within one "
          "partition.</b> Co-locate by tenant, by user, by order, by game "
          "session — whatever unit the transactions naturally fall "
          "within. <b>This is where the leverage is</b>, and most "
          "cross-partition transactions turn out to be an artifact of the "
          "partitioning choice rather than a property of the domain.",
          "<b>Use a CRDT</b>, if the invariant is local (&sect;3).",
          "<b>Use a saga</b> with explicitly defined compensating actions, "
          "if the business can say what undoing each step means "
          "(&sect;2).",
          "<b>Use two-phase commit over a consensus-backed "
          "coordinator.</b> Correct, slow, and <b>a genuinely available "
          "option</b> — Spanner does essentially this, and dismissing "
          "distributed transactions as impossible is out of date.",
          "<b>Reconsider the requirement.</b> <b>It is frequently "
          "negotiable and is rarely asked about</b> — 'must these two "
          "things be atomic, or must they merely both eventually happen?' "
          "has a different answer surprisingly often, and the second is "
          "far cheaper."]),
 ],
 "resources": [
   ("Kleppmann &mdash; Designing Data-Intensive Applications, chapters 6, "
    "7 and 9",
    "https://dataintensive.net/",
    "Partitioning, transactions, and 2PC, with the blocking problem of "
    "&sect;2 explained properly."),
   ("Karger et al. &mdash; Consistent Hashing and Random Trees (free)",
    "https://www.akamai.com/site/en/documents/research-paper/consistent-hashing-and-random-trees-distributed-caching-protocols-for-relieving-hot-spots-on-the-world-wide-web-technical-publication.pdf",
    "The &sect;1 algorithm, from the paper that introduced it and founded "
    "Akamai."),
   ("Shapiro, Pregui&ccedil;a, Baquero & Zawirski &mdash; A Comprehensive "
    "Study of Convergent and Commutative Replicated Data Types (free)",
    "https://inria.hal.science/inria-00555588/document",
    "<b>The CRDT reference.</b> Comprehensive, and the taxonomy in the "
    "first sections is the useful part."),
   ("Garcia-Molina & Salem &mdash; Sagas (free)",
    "https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf",
    "The &sect;2 alternative, from 1987 — long before microservices "
    "rediscovered it."),
 ],
 "exercises": [
   "<b>Measure how many keys move</b> under hash(key) mod n when n goes "
   "from 10 to 11. Compare against consistent hashing.",
   "Implement consistent hashing with one point per node and <b>plot the "
   "load distribution</b>.",
   "<b>Add 150 virtual nodes each</b> and plot it again. Report the "
   "variance in both cases.",
   "Remove a node from both and compare where its load goes.",
   "Implement two-phase commit.",
   "<b>Kill the coordinator after the prepare phase</b> and show a "
   "participant stuck holding locks.",
   "Run the coordinator on your Raft cluster from Module 06 and show the "
   "blocking is gone.",
   "<b>Implement a saga</b> with compensations for a three-step booking, "
   "and demonstrate a compensating rollback.",
   "Implement a grow-only counter and a two-phase set as CRDTs. Verify "
   "convergence under reordering and duplication.",
   "<b>Demonstrate the resurrected-item problem</b> in a cart CRDT and "
   "explain why Amazon accepted it.",
 ],
 "selfcheck": [
   "Compare five partitioning schemes and their failure modes.",
   "Why does hash mod n remap almost everything?",
   "Why are virtual nodes mandatory for consistent hashing?",
   "Describe 2PC and explain precisely why a participant blocks.",
   "Why is 2PC not a fault-tolerance protocol?",
   "What do sagas give up, and why is compensation not rollback?",
   "What three properties must a CRDT merge have?",
   "Give the test for whether a CRDT applies.",
   "Give the six-step order for choosing, and say where the leverage is.",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Netcode I: The Latency Problem",
 "subtitle": "Distributed systems with a 16 millisecond deadline.",
 "question": "How do you build a shared world when the network takes "
             "100 ms?",
 "outcomes": [
     "Compare netcode architectures and their failure modes.",
     "Explain the authority question and why it decides everything.",
     "Explain deterministic lockstep and its requirements.",
     "Explain state synchronisation and its bandwidth problem.",
     "Choose an architecture from the game's requirements.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The constraint",
   "blurb": "Why none of the previous eight modules applies directly."},

  {"t": "callout", "title": "A game is a distributed system with three extra constraints",
   "kind": "Why netcode looks different",
   "body": ["<b>A hard deadline.</b> 16.7 ms at 60 Hz, and a frame that "
            "misses it is visible. There is no option to wait.",
            "<b>An adversarial participant.</b> Every client runs on "
            "hardware the attacker owns (Module 01 §3). Byzantine, by "
            "default.",
            "<b>And continuous state.</b> Not a log of discrete "
            "operations but positions and velocities changing every "
            "tick.",
            "<b>So consensus is out</b> (Module 06 §4), <b>quorums are "
            "out, and CRDTs are out</b> (Module 08 §3). <b>What remains is "
            "a referee and a lot of educated guessing.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Architectures",
   "blurb": "Who decides what is true."},

  {"t": "table", "kicker": "Architectures", "title": "Four arrangements",
   "header": ["Architecture", "Authority", "Trade"],
   "widths": [2.8, 3.6, 5.7],
   "rows": [
     ["<b>Authoritative server</b>", "<b>The server, entirely</b>", "<b>Cheat-resistant; server cost; input latency</b>"],
     ["<b>Listen server</b>", "One player's machine", "<b>Free; that player has zero latency. Unfair</b>"],
     ["<b>Deterministic lockstep</b>", "<b>Everyone, by agreement</b>", "<b>Tiny bandwidth; input delay; desync risk</b>"],
     ["<b>Peer-to-peer trusted</b>", "Each client owns its objects", "<b>Trivially cheatable. Co-op only</b>"],
     ["Rollback (GGPO)", "<b>Lockstep + prediction</b>", "<b>Excellent feel; needs cheap rollback</b>"],
   ],
   "footnote": "<b>The authority question decides everything else</b> "
               "— bandwidth, cheat resistance, and how the game feels "
               "all follow from it.",
   "note": "Lead with authority; the rest are consequences."},

  {"t": "callout", "title": "The authority question comes first",
   "kind": "The decision everything follows from",
   "body": ["<b>Who decides whether the shot hit?</b> Whoever does is the "
            "authority, and everyone else is guessing.",
            "<b>If the client decides, it can lie</b> — and it will "
            "(Module 11). There is no cryptography that fixes this, "
            "because the client legitimately possesses everything it would "
            "need to lie convincingly.",
            "<b>If the server decides, the player waits a round trip to "
            "see the result</b> — unless the client predicts "
            "(Module 10).",
            "<b>So: server authority plus client prediction</b> is the "
            "answer for any competitive game, and the next module is "
            "entirely about making that feel instantaneous."]},

  {"t": "section", "label": "Part 3", "title": "Lockstep",
   "blurb": "Send inputs, simulate identically."},

  {"t": "code", "kicker": "Lockstep", "title": "Deterministic lockstep",
   "lang": "text", "code": """
  Send only INPUTS. Every client runs the identical simulation.

      tick N:  gather local input
               broadcast it
               WAIT for every other player's input for tick N
               simulate tick N with all inputs
               -> every client computes the identical world

  BANDWIDTH: a few bytes per player per tick, regardless of how
  many units exist. An RTS with 2000 units costs the same as one
  with 5. This is why RTS games use it.

  THE TWO PROBLEMS:

  1. INPUT DELAY. You cannot simulate tick N until everyone's
     input arrives, so every player waits for the SLOWEST.
     Mitigation: run tick N with inputs gathered at tick N-3,
     so there is slack. That is 3 ticks of input lag, always.

  2. DESYNC. Determinism must be EXACT and bit-identical.
     Float differences across compilers or CPUs, map iteration
     order, uninitialised memory, or one un-seeded random call
     diverge the simulations -- and the divergence COMPOUNDS.
     Detect with a periodic state checksum; the only recovery
     is to resynchronise or drop the player.
""",
   "caption": "<b>This is Module 06's replicated state machine</b> with "
              "no consensus layer — same determinism requirement, same "
              "failure when it is violated.",
   "note": "The compounding-divergence point explains why desync is "
           "catastrophic rather than cosmetic."},

  {"t": "section", "label": "Part 4", "title": "State synchronisation",
   "blurb": "Send the world, not the inputs."},

  {"t": "callout", "title": "State sync: the server sends what it decided",
   "kind": "The alternative",
   "body": ["<b>The server simulates authoritatively and sends snapshots "
            "of the world state.</b> Clients display what they are told.",
            "<b>No determinism requirement at all</b> — clients need not "
            "agree with each other, only receive updates.",
            "<b>And no waiting</b> — a client that misses a snapshot uses "
            "the next one. Loss degrades smoothly instead of stalling.",
            "<b>The cost is bandwidth</b>, which scales with the amount "
            "of state rather than the number of players. <b>Which is why "
            "shooters use state sync and strategy games use "
            "lockstep</b> — the state size differs by orders of "
            "magnitude."]},

  {"t": "bullets", "kicker": "Bandwidth", "title": "How state sync stays affordable",
   "items": [
     "<b>Relevance / interest management.</b> Send only what this client "
     "can see. <b>The largest single saving by far.</b>",
     "",
     "<b>Delta compression</b> against the last acknowledged snapshot "
     "— send what changed.",
     "",
     "<b>Quantisation.</b> A position does not need 32-bit floats; 16 "
     "bits over a bounded range is invisible.",
     "",
     "<b>Prioritisation</b> — nearby and recently-changed objects "
     "update more often than distant ones.",
     "",
     "<b>And it is unreliable UDP</b> (Module 02), so a lost snapshot "
     "costs nothing. <b>Delta compression must therefore be against an "
     "<i>acknowledged</i> baseline</b>, not the last one sent.",
   ],
   "footnote": "<b>That last point is the subtle one:</b> deltas against "
               "an unacknowledged baseline break permanently when a packet "
               "is lost."},

  {"t": "callout", "title": "Choosing",
   "kind": "The decision, with reasons",
   "body": ["<b>Few entities, many players, competitive: state sync with "
            "an authoritative server.</b> Shooters, MMOs, battle "
            "royales.",
            "<b>Many entities, few players, bandwidth-constrained: "
            "lockstep.</b> RTS, and anything with thousands of units.",
            "<b>Two players, frame-perfect input matters: rollback "
            "netcode.</b> Fighting games, and GGPO changed the genre.",
            "<b>Co-operative only, trust is acceptable: peer-to-peer.</b> "
            "<b>And be honest that it is cheatable</b> — which is fine "
            "when the only victim is a friend who chose to play with you."]},
 ],
 "takeaways": [
   "A game adds three constraints to distributed systems: a hard deadline, "
   "an adversarial participant, and continuous rather than discrete state.",
   "Consensus, quorums, and CRDTs are all unusable, leaving a referee and "
   "a lot of educated guessing.",
   "The authority question decides everything else — bandwidth, cheat "
   "resistance, and how the game feels all follow from it.",
   "Lockstep sends only inputs, so bandwidth is independent of entity "
   "count — at the cost of permanent input delay and catastrophic "
   "desync risk.",
   "State sync needs no determinism and degrades smoothly under loss, but "
   "bandwidth scales with world size.",
   "Delta compression must be against an acknowledged baseline, or one lost "
   "packet breaks it permanently.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The constraint"),
  ("callout", "Three extra constraints that change everything",
   ["<b>A hard deadline.</b> 16.7 ms at 60 Hz, and a frame that misses it "
    "is visible to the player as a stutter. <b>There is no option to "
    "wait</b> — which removes every technique in Modules 04 through 08 "
    "that involves a round trip before acting.",
    "<b>An adversarial participant.</b> Every client runs on hardware the "
    "attacker physically owns, with a debugger attached and the memory "
    "readable and writable. <b>Byzantine by default</b> (Module 01 "
    "&sect;3), and not occasionally but as the normal case.",
    "<b>And continuous state.</b> Not a log of discrete operations to be "
    "agreed upon but positions, velocities, and orientations changing every "
    "single tick — which is a poor fit for the replicated-log "
    "abstraction that Module 06 reduces everything to.",
    "<b>So consensus is out</b> (Module 06 &sect;4, on the arithmetic), "
    "<b>quorum replication is out</b> (no time for the round trip), and "
    "<b>CRDTs are out</b> (Module 08 &sect;3 — a game needs a referee, "
    "and 'who shot first' is a decision rather than a merge). <b>What "
    "remains is an authority and a great deal of educated guessing</b>, "
    "which is the subject of this module and the next two."]),

  ("h1", "2 &nbsp; Architectures"),
  ("table", ["Architecture", "Who has authority", "The trade"],
   [["<b>Authoritative dedicated server</b>",
     "<b>The server, entirely.</b> Clients send inputs and receive state.",
     "<b>Cheat-resistant</b> (Module 11), <b>costs server capacity</b>, and "
     "<b>introduces a round trip of input latency</b> unless the client "
     "predicts (Module 10)."],
    ["<b>Listen server</b>",
     "One player's machine, which also plays.",
     "<b>Free to operate</b>, and <b>that player has zero latency and "
     "perfect information while everyone else does not</b>. Structurally "
     "unfair, and common in casual games for cost reasons."],
    ["<b>Deterministic lockstep</b>",
     "<b>Everyone, by construction</b> — all clients compute the same "
     "world from the same inputs.",
     "<b>Minimal bandwidth</b>, <b>permanent input delay</b>, and "
     "<b>catastrophic failure on desync</b> (&sect;3)."],
    ["<b>Peer-to-peer with trusted clients</b>",
     "Each client is authoritative over its own objects.",
     "<b>Trivially cheatable</b> — a client simply declares it did not "
     "take damage. Acceptable for co-operative play only."],
    ["<b>Rollback (GGPO-style)</b>",
     "<b>Lockstep, with local prediction and re-simulation.</b>",
     "<b>Excellent responsiveness</b>, and requires a simulation cheap "
     "enough to re-run several ticks within one frame (Module 10 "
     "&sect;4)."]],
   [0.21, 0.33, 0.46]),
  ("callout", "The authority question comes first",
   ["<b>Who decides whether the shot hit?</b> Whoever decides is the "
    "authority; everyone else is displaying a guess. Answering this one "
    "question determines the bandwidth profile, the cheat resistance, and "
    "how the game feels.",
    "<b>If the client decides, it can lie</b>, and in any game with "
    "competition it will (Module 11). <b>No cryptography fixes this</b>, "
    "because the client legitimately possesses every key and every piece of "
    "code it would need to produce a perfectly well-formed false claim. "
    "This is a genuinely unsolvable problem, not a hard one.",
    "<b>If the server decides, the player must wait a full round trip to "
    "see the result of their own action</b> — which at 100 ms is "
    "unplayable for anything requiring aim or timing, <b>unless the client "
    "predicts</b> (Module 10).",
    "<b>So the answer for any competitive game is server authority plus "
    "client prediction</b>, and the whole of Module 10 is about making "
    "that combination feel instantaneous while remaining "
    "server-authoritative. <b>It is one of the more elegant pieces of "
    "engineering in this program</b>, and it is far less widely understood "
    "than it deserves to be."]),

  ("break",),
  ("h1", "3 &nbsp; Deterministic lockstep"),
  ("code", """Send only INPUTS. Every client runs the identical simulation.

  tick N:  gather local input
           broadcast it
           WAIT for every other player's input for tick N
           simulate tick N with all inputs
           -> every client computes an identical world

BANDWIDTH: a few bytes per player per tick, INDEPENDENT of how
many entities exist. 2000 units costs the same as 5. This is
why RTS games use it.

PROBLEM 1 -- INPUT DELAY
  cannot simulate tick N until everyone's input arrives, so
  everyone waits for the SLOWEST player.
  Mitigation: simulate tick N using inputs gathered at N-3.
  That is three ticks of input lag, permanently.

PROBLEM 2 -- DESYNC
  determinism must be EXACT and bit-identical. Float differences
  across compilers or CPUs, map iteration order, uninitialised
  memory, or one unseeded random call diverge the simulations --
  and the divergence COMPOUNDS from that tick onward.
  Detect with a periodic state checksum. Recovery is
  resynchronisation or dropping the player."""),
  ("p", "<b>This is exactly Module 06's replicated state machine with the "
        "consensus layer removed</b> — the same reduction (agree on "
        "the inputs, derive the state), the same absolute determinism "
        "requirement, and the same failure mode when it is violated. "
        "<b>The compounding is what makes desync catastrophic rather than "
        "cosmetic:</b> one unit's position differing by one bit at tick "
        "1000 changes what it collides with at tick 1001, which changes the "
        "whole battle by tick 1100. There is no partial recovery."),

  ("h1", "4 &nbsp; State synchronisation"),
  ("callout", "The server sends what it decided",
   ["<b>The server runs the authoritative simulation and sends snapshots "
    "of world state to each client.</b> Clients display what they are told "
    "and send only their inputs back.",
    "<b>There is no determinism requirement at all.</b> Clients need not "
    "agree with one another or reproduce the server's arithmetic — "
    "they only need to receive and render. <b>This removes the entire "
    "desync failure mode</b>, which is a very large practical advantage.",
    "<b>And there is no waiting.</b> A client that misses a snapshot "
    "simply uses the next one; packet loss degrades smoothly into slightly "
    "staler information rather than stalling everyone (Module 02 "
    "&sect;1).",
    "<b>The cost is bandwidth, which scales with the amount of state "
    "rather than with the number of players.</b> <b>Which is exactly why "
    "shooters use state sync and strategy games use lockstep</b>: a shooter "
    "has dozens of relevant entities and a dozen players, while an RTS has "
    "thousands of units and four players. <b>The architectures are not "
    "better or worse; they are matched to opposite ratios.</b>"]),
  ("ul", ["<b>Relevance or interest management.</b> Send each client only "
          "what it could plausibly perceive — what is nearby, visible, "
          "or audible. <b>By far the largest single saving</b>, often an "
          "order of magnitude, and it doubles as an anti-cheat measure "
          "(Module 11 &sect;3) since information not sent cannot be "
          "extracted.",
          "<b>Delta compression</b> against the last acknowledged "
          "snapshot — transmit only the fields that changed since the "
          "client last confirmed receipt.",
          "<b>Quantisation.</b> A position in a bounded world does not need "
          "three 32-bit floats; 16 bits per axis over the world extent is "
          "visually indistinguishable and halves the cost. The same applies "
          "to orientations (smallest-three quaternion encoding) and "
          "velocities.",
          "<b>Prioritisation.</b> Nearby, recently-changed, and "
          "player-relevant objects update every tick; distant scenery "
          "updates rarely. A per-object priority accumulator is the usual "
          "mechanism.",
          "<b>And all of it rides unreliable UDP</b> (Module 02 &sect;1), "
          "so a lost snapshot costs nothing — the next one supersedes "
          "it. <b>Which is precisely why delta compression must be against "
          "an <i>acknowledged</i> baseline rather than the last one "
          "sent:</b> if the client never received the baseline, every "
          "subsequent delta is meaningless, and the error persists forever "
          "rather than for one frame. <b>This is the subtle bug in naive "
          "implementations</b>, and it only appears under packet loss, "
          "which is why localhost testing misses it entirely."]),
  ("callout", "Choosing an architecture",
   ["<b>Few entities, many players, competitive:</b> <b>state "
    "synchronisation with an authoritative dedicated server.</b> Shooters, "
    "battle royales, and MMOs. The bandwidth is affordable because "
    "relevance filtering is effective, and the cheat resistance is "
    "essential.",
    "<b>Many entities, few players, bandwidth-constrained:</b> "
    "<b>deterministic lockstep.</b> Real-time strategy, and anything where "
    "the unit count makes state sync impossible. Accept the input delay "
    "and invest heavily in determinism testing.",
    "<b>Two players, frame-perfect input matters:</b> <b>rollback "
    "netcode.</b> Fighting games — and GGPO genuinely changed the "
    "genre, to the point that rollback support is now a purchasing "
    "consideration for players.",
    "<b>Co-operative only, where trust is acceptable:</b> peer-to-peer "
    "with client authority. <b>And be honest in the design document that "
    "it is cheatable</b> — which is entirely fine when the only person "
    "who can be cheated is a friend who chose to play with you, and is not "
    "fine the moment a leaderboard exists."]),
 ],
 "resources": [
   ("Glenn Fiedler &mdash; Networked Physics and the Gaffer On Games "
    "series (free)",
    "https://gafferongames.com/",
    "<b>The reference for this module and the next two.</b> Start with "
    "'What Every Programmer Needs To Know About Game Networking'."),
   ("Valve &mdash; Source Multiplayer Networking (free)",
    "https://developer.valvesoftware.com/wiki/Source_Multiplayer_Networking",
    "<b>A shipping architecture documented by its authors</b> — "
    "snapshots, interpolation, prediction, and lag compensation in one "
    "coherent description."),
   ("Bettner & Terrano &mdash; 1500 Archers on a 28.8: Network "
    "Programming in Age of Empires (free)",
    "https://www.gamedevs.org/uploads/1500-archers-on-a-288-network-programming-in-age-of-empires.pdf",
    "<b>The classic lockstep paper</b>, and still the clearest account of "
    "&sect;3's trade-offs and desync hunting."),
   ("Ruoyu Sun / GGPO &mdash; rollback networking documentation (free)",
    "https://github.com/pond3r/ggpo",
    "The rollback architecture, with source."),
 ],
 "exercises": [
   "<b>Measure your own input-to-display latency</b> locally, then add "
   "100 ms of network delay and measure the difference in feel.",
   "Implement a trivial two-player simulation with client authority and "
   "<b>cheat in it</b> to show how easy it is.",
   "Implement deterministic lockstep for a simple simulation.",
   "<b>Add a state checksum</b> and deliberately introduce a desync "
   "(an unseeded random call). Measure how many ticks before the worlds "
   "visibly differ.",
   "<b>Measure lockstep bandwidth against entity count</b> and confirm it "
   "is flat.",
   "Implement state synchronisation with full snapshots and measure the "
   "bandwidth.",
   "<b>Add relevance filtering</b> and measure the saving.",
   "Add delta compression against an acknowledged baseline.",
   "<b>Then delta against the last snapshot <i>sent</i> instead</b>, "
   "introduce 5% loss, and demonstrate the permanent corruption.",
   "Quantise positions to 16 bits per axis and verify the error is below "
   "a pixel at typical viewing distance.",
 ],
 "selfcheck": [
   "What three constraints does a game add, and which techniques do they "
   "rule out?",
   "Compare five netcode architectures on authority and trade.",
   "Why does the authority question come first?",
   "Why can cryptography not make a client trustworthy?",
   "Describe lockstep and give its two problems.",
   "Why does desync compound?",
   "What does state sync give up and what does it gain?",
   "Name five bandwidth reductions for state sync.",
   "Why must delta compression use an acknowledged baseline?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Netcode II: Prediction and Reconciliation",
 "subtitle": "Feeling instant while waiting for permission.",
 "question": "How do you hide a 100 millisecond round trip?",
 "outcomes": [
     "Implement client-side prediction.",
     "Implement server reconciliation with input replay.",
     "Implement entity interpolation and state the buffer trade.",
     "Explain rollback netcode and its requirements.",
     "Diagnose the characteristic artifacts of each.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Prediction",
   "blurb": "Act now, ask permission later."},

  {"t": "callout", "title": "The client simulates its own actions immediately",
   "kind": "The first half of the technique",
   "body": ["<b>Without prediction, pressing forward does nothing for a "
            "full round trip</b> — input to server, server simulates, "
            "state back. At 100 ms that is unplayable.",
            "<b>With prediction, the client applies the input to its own "
            "copy immediately</b> and simultaneously sends it to the "
            "server.",
            "<b>So movement feels instantaneous</b>, because locally it "
            "is.",
            "<b>And the client is usually right</b> — it runs the same "
            "movement code the server does, so in the absence of "
            "interaction with others the prediction matches. <b>The "
            "interesting case is when it does not.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Reconciliation",
   "blurb": "What happens when the server disagrees."},

  {"t": "code", "kicker": "Reconciliation", "title": "Replay the unacknowledged inputs",
   "lang": "text", "code": """
  CLIENT keeps a buffer of inputs it has sent but not yet seen
  acknowledged, each tagged with a sequence number.

      send input #42, #43, #44, #45 ...
      apply each locally as it is sent

  SERVER replies with authoritative state AND the last input
  sequence number it has processed:

      "here is the world, as of your input #43"

  CLIENT then:
      1. snap its own state to the server's authoritative state
      2. DISCARD inputs #43 and earlier from the buffer
      3. RE-APPLY inputs #44, #45 ... on top of that state
      4. the result is a corrected prediction that still
         includes everything the player has done since

  If the prediction was right, step 3 reproduces exactly what
  the client already had -- and NOTHING VISIBLY HAPPENS.
  If it was wrong, the error is corrected, and only the
  divergence since #43 is lost.
""",
   "caption": "<b>The replay is what makes correction invisible</b> when "
              "the prediction was right — which is almost always.",
   "note": "Students often snap without replaying, which throws away the "
           "player's recent input and feels terrible."},

  {"t": "callout", "title": "Smooth the correction, do not snap it",
   "kind": "The detail that decides how it feels",
   "body": ["<b>A visible snap is jarring</b>, and small corrections "
            "happen constantly from ordinary floating-point and timing "
            "differences.",
            "<b>So blend toward the corrected position over a few frames</b> "
            "rather than teleporting to it.",
            "<b>But large errors must snap.</b> Smoothing a two-metre "
            "correction means the player is wrong about where they are for "
            "half a second, which is worse.",
            "<b>So: threshold it.</b> Under ~10 cm, blend; over it, snap. "
            "<b>And log the large ones</b> — a rising rate of large "
            "corrections means a prediction bug or a cheater."]},

  {"t": "section", "label": "Part 3", "title": "Other players",
   "blurb": "You cannot predict what you cannot see."},

  {"t": "callout", "title": "Interpolate remote entities; do not predict them",
   "kind": "The asymmetry",
   "body": ["<b>You know your own input, so you can predict yourself. You "
            "do not know anyone else's</b>, so predicting them means "
            "extrapolating, and extrapolation is wrong whenever they "
            "change direction.",
            "<b>So render remote entities <i>in the past</i>:</b> buffer "
            "snapshots and display the interpolated state from 100 ms ago, "
            "between two snapshots you already have.",
            "<b>The result is perfectly smooth motion</b>, with no "
            "guessing and no correction artifacts.",
            "<b>The cost is that you see everyone else slightly "
            "late</b> — which is exactly the unfairness that lag "
            "compensation (Module 11) exists to address, and it creates "
            "problems of its own."]},

  {"t": "table", "kicker": "Artifacts", "title": "Each technique's characteristic failure",
   "header": ["Technique", "Artifact", "Seen as"],
   "widths": [3.0, 4.2, 4.9],
   "rows": [
     ["<b>Prediction</b>", "<b>Misprediction correction</b>", "<b>Rubber-banding; being pulled back</b>"],
     ["<b>No smoothing</b>", "Visible snap every correction", "Jitter on your own character"],
     ["<b>Over-smoothing</b>", "<b>Slow convergence</b>", "<b>Floaty, disconnected controls</b>"],
     ["<b>Interpolation</b>", "<b>Remote players are delayed</b>", "<b>Shots that look like hits and miss</b>"],
     ["Extrapolation", "Wrong on direction change", "<b>Warping; players snapping back</b>"],
     ["<b>Too small a buffer</b>", "Runs out of snapshots", "<b>Stuttering remote players</b>"],
   ],
   "footnote": "<b>Every one of these is a <i>correct</i> implementation "
               "showing its trade-off.</b> Recognising which you are "
               "looking at is the diagnostic skill.",
   "note": "Framing artifacts as trade-offs rather than bugs is the "
           "useful move."},

  {"t": "section", "label": "Part 4", "title": "Rollback",
   "blurb": "Prediction applied to everyone."},

  {"t": "callout", "title": "Rollback netcode predicts other players too",
   "kind": "The fighting-game answer",
   "body": ["<b>Assume the remote player's input is the same as last "
            "frame, and simulate forward immediately.</b> No waiting, no "
            "interpolation delay.",
            "<b>When the real input arrives and differs, roll the "
            "simulation back</b> to that frame and re-simulate everything "
            "since, with the correct input.",
            "<b>So both players see an instant response to their own "
            "input</b>, and occasional visual corrections of the other.",
            "<b>It requires the simulation to be deterministic, cheaply "
            "re-runnable, and fully snapshot-able</b> — several times per "
            "frame. <b>Easy for two fighters; infeasible for a large "
            "world.</b>"]},

  {"t": "callout", "title": "Why rollback beats input delay",
   "kind": "The empirical result",
   "body": ["<b>The alternative is adding input delay</b> until the "
            "remote input reliably arrives in time — so <i>both</i> "
            "players' controls become less responsive.",
            "<b>Rollback instead keeps local response instant and makes "
            "the <i>remote</i> character occasionally correct itself.</b>",
            "<b>Players tolerate the second far better than the "
            "first.</b> Your own character feeling sluggish is "
            "immediately noticeable; your opponent flickering occasionally "
            "is not.",
            "<b>This is a human-factors result, not a technical one</b> "
            "— and it is the same observation as CSCE 650's on VR "
            "latency: <b>the coupling between your own action and the "
            "response is what people detect.</b>"]},
 ],
 "takeaways": [
   "Client-side prediction applies input locally and immediately, so "
   "movement feels instant while the server remains authoritative.",
   "Reconciliation snaps to the server state and replays unacknowledged "
   "inputs, which makes correction invisible whenever the prediction was "
   "right.",
   "Smooth small corrections over a few frames and snap large ones; log "
   "the large ones, because a rising rate means a bug or a cheater.",
   "You can predict yourself because you know your input, and must "
   "interpolate others from the past because you do not.",
   "Every characteristic artifact — rubber-banding, warping, "
   "stuttering — is a correct implementation showing its trade-off.",
   "Rollback keeps local response instant and lets the remote character "
   "correct itself, which players tolerate far better than added input "
   "delay.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Client-side prediction"),
  ("callout", "The client simulates its own actions immediately",
   ["<b>Without prediction, pressing forward does nothing at all for a full "
    "round trip</b> — the input travels to the server, the server "
    "simulates, and the new state travels back. At 100 ms RTT that is a "
    "tenth of a second of complete unresponsiveness on every single input, "
    "which is unplayable for anything requiring precision.",
    "<b>With prediction, the client applies the input to its own copy of "
    "the world immediately</b>, using the same movement code the server "
    "will use, and sends the input to the server at the same time.",
    "<b>So movement feels instantaneous, because locally it is.</b> The "
    "player's own character responds on the same frame as the keypress, "
    "which is the only latency a player directly perceives.",
    "<b>And the client is usually right.</b> It runs the same deterministic "
    "movement code against the same input, so in the absence of interaction "
    "with other players or server-side events its prediction matches what "
    "the server will compute. <b>The interesting case is when it does "
    "not</b> — someone else shot you, a door closed, a grenade "
    "exploded — and &sect;2 is about handling that invisibly."]),

  ("h1", "2 &nbsp; Server reconciliation"),
  ("code", """CLIENT keeps a buffer of inputs sent but not yet acknowledged,
each tagged with a sequence number.

    send #42, #43, #44, #45 ...   and apply each locally

SERVER replies with authoritative state AND the last input it
processed:   "here is the world, as of your input #43"

CLIENT then:
    1. snap its own state to the server's state
    2. DISCARD inputs #43 and earlier from the buffer
    3. RE-APPLY #44, #45 ... on top of that state
    4. result: a corrected prediction that still contains
       everything the player has done since

If the prediction was right, step 3 reproduces exactly what the
client already had, and NOTHING VISIBLY HAPPENS.
If it was wrong, only the divergence since #43 is lost."""),
  ("p", "<b>The replay is what makes the correction invisible</b> in the "
        "overwhelmingly common case where the prediction was right. "
        "<b>Snapping to the server state without replaying is the classic "
        "implementation error:</b> it discards every input the player has "
        "made during the last round trip, so the character jerks backwards "
        "on every single update and the controls feel broken. The buffer "
        "and the replay are not an optimisation; they are the technique."),
  ("callout", "Smooth the correction, do not snap it",
   ["<b>A visible snap is jarring</b>, and small corrections happen "
    "constantly — from floating-point differences, from timing jitter, "
    "from a server tick landing slightly differently. If every one produced "
    "a visible jump, the character would shimmer permanently.",
    "<b>So blend toward the corrected position over a few frames</b> rather "
    "than teleporting to it. The player sees continuous motion and the "
    "error is absorbed.",
    "<b>But large errors must snap.</b> Smoothing a two-metre correction "
    "over half a second means the player spends half a second believing "
    "they are somewhere they are not — shooting from the wrong "
    "position, walking into a wall that is not where it appears. <b>Being "
    "wrong smoothly is worse than being corrected abruptly.</b>",
    "<b>So threshold it:</b> below roughly 10 cm, blend over a few frames; "
    "above it, snap immediately. <b>And log the large corrections as a "
    "metric</b> — a rising rate of large corrections means either a "
    "prediction bug (the client and server movement code have diverged) or "
    "a client attempting to move in ways the server rejects, which is "
    "Module 11's problem. <b>The same signal serves debugging and "
    "anti-cheat.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Other players"),
  ("callout", "Interpolate remote entities; do not predict them",
   ["<b>You know your own input, so you can predict yourself. You do not "
    "know anyone else's</b>, so predicting them means <i>extrapolating</i> "
    "from their last known velocity — which is correct while they move "
    "in a straight line and wrong the instant they change direction.",
    "<b>So render remote entities in the past.</b> Buffer incoming "
    "snapshots and display the state interpolated between two snapshots you "
    "have <i>already received</i>, typically 100 ms behind the newest. "
    "<b>You are interpolating between known facts rather than guessing "
    "beyond them.</b>",
    "<b>The result is perfectly smooth motion with no guessing and no "
    "correction artifacts</b> — remote players never warp, never snap, "
    "and never moonwalk, because nothing was ever predicted.",
    "<b>The cost is that you see everyone else slightly late.</b> You are "
    "aiming at where an opponent was 100 ms ago plus your own network "
    "delay. <b>That is exactly the unfairness lag compensation exists to "
    "address</b> (Module 11 &sect;2) — and the fix creates problems of "
    "its own, which is the subject of that module."]),
  ("table", ["Technique", "Characteristic artifact", "How it is perceived"],
   [["<b>Prediction</b>",
     "<b>Correction after a misprediction.</b>",
     "<b>Rubber-banding</b> — being pulled back to where the server "
     "says you were. Usually means genuine network trouble or a server "
     "disagreement."],
    ["<b>Prediction with no smoothing</b>",
     "A visible snap on every correction, however small.",
     "Constant jitter on your own character; controls feel unreliable."],
    ["<b>Prediction with too much smoothing</b>",
     "<b>Slow convergence to the authoritative state.</b>",
     "<b>Floaty, disconnected controls</b> — the character feels like "
     "it is being dragged rather than driven."],
    ["<b>Interpolation</b>",
     "<b>Remote players are rendered in the past.</b>",
     "<b>Shots that visually connect and are scored as misses</b> — "
     "the single most reported netcode complaint, and Module 11's subject."],
    ["<b>Extrapolation (dead reckoning)</b>",
     "Wrong whenever the extrapolated entity changes direction.",
     "<b>Warping and snapping back</b> — characters sliding past a "
     "corner and then jumping back to it."],
    ["<b>Too small an interpolation buffer</b>",
     "The buffer runs dry when a packet is late.",
     "<b>Stuttering remote players</b> — freeze, jump, freeze."]],
   [0.22, 0.34, 0.44]),
  ("p", "<b>Every one of these is a <i>correct</i> implementation "
        "displaying its trade-off, not a bug.</b> Recognising which "
        "artifact you are looking at tells you which parameter to move, and "
        "<b>that diagnostic skill is most of what netcode tuning "
        "actually is</b> — the implementations are not especially hard "
        "and the tuning is where the time goes."),

  ("h1", "4 &nbsp; Rollback"),
  ("callout", "Rollback netcode predicts the other player too",
   ["<b>Assume the remote player's input this frame is the same as their "
    "last frame's input, and simulate forward immediately.</b> No waiting "
    "for their input to arrive, and no interpolation delay — both "
    "characters respond on the current frame.",
    "<b>When the real input arrives and differs from the assumption, roll "
    "the simulation back</b> to the frame it applies to and re-simulate "
    "every frame since with the correct input. The display jumps to the "
    "corrected state.",
    "<b>So both players see an instant response to their own input</b>, "
    "and occasional visual corrections of the <i>other</i> character — "
    "which is the opposite allocation of the error from interpolation.",
    "<b>It requires the simulation to be deterministic, cheap enough to "
    "re-run several frames within one frame's budget, and fully "
    "snapshot-able</b> so that the rollback point can be restored. <b>Easy "
    "for two fighters on a small stage; infeasible for a large world with "
    "hundreds of entities</b>, which is why the technique is associated "
    "with one genre."]),
  ("callout", "Why rollback beats input delay",
   ["<b>The alternative is adding input delay</b> — holding your own "
    "input for a few frames so the remote input reliably arrives in time to "
    "simulate them together. <b>This makes <i>both</i> players' controls "
    "less responsive</b>, permanently, by the amount of the worst "
    "connection.",
    "<b>Rollback instead keeps local response instant and makes the remote "
    "character occasionally correct itself</b> — moving the entire "
    "cost of the network onto the visual representation of the opponent.",
    "<b>Players tolerate the second far better than the first.</b> Your own "
    "character feeling sluggish is immediately and continuously noticeable; "
    "your opponent's sprite flickering occasionally during a correction is "
    "barely registered, and in practice players report rollback connections "
    "as 'better' at latencies where delay-based netcode is reported as "
    "unplayable.",
    "<b>This is a human-factors result rather than a technical one</b>, and "
    "it is the same observation CSCE 650 Module 06 made about virtual "
    "reality: <b>what people detect is the coupling between their own "
    "action and the response to it</b>, far more sensitively than they "
    "detect inconsistency in the world around them. <b>Both fields "
    "arrived at the same conclusion independently</b>, which is reasonable "
    "evidence it is a fact about perception rather than about either "
    "medium."]),
 ],
 "resources": [
   ("Glenn Fiedler &mdash; Client-Side Prediction and Server "
    "Reconciliation (free)",
    "https://gafferongames.com/post/networked_physics_in_virtual_reality/",
    "<b>The &sect;1 and &sect;2 technique</b>, with code and with the "
    "smoothing detail of the second callout."),
   ("Gabriel Gambetta &mdash; Fast-Paced Multiplayer (free, interactive)",
    "https://www.gabrielgambetta.com/client-server-game-architecture.html",
    "<b>Interactive demonstrations of prediction, reconciliation, and "
    "interpolation</b>, with sliders for latency. <b>The single best way "
    "to build intuition for this module.</b>"),
   ("Valve &mdash; Latency Compensating Methods in Client/Server Protocol "
    "Design (free)",
    "https://developer.valvesoftware.com/wiki/Latency_Compensating_Methods_in_Client/Server_In-game_Protocol_Design_and_Optimization",
    "The original Half-Life paper. Covers &sect;3's interpolation and sets "
    "up Module 11."),
   ("Infil &mdash; The Fighting Game Glossary, and GGPO's documentation "
    "(free)",
    "https://github.com/pond3r/ggpo/blob/master/doc/README.md",
    "<b>Rollback explained from both the player's and the implementer's "
    "side</b> — the &sect;4 human-factors argument is clearest in the "
    "player-facing writing."),
 ],
 "exercises": [
   "<b>Build the no-prediction baseline</b> and play it at 100 ms. Record "
   "how it feels.",
   "Add client-side prediction and compare.",
   "<b>Implement reconciliation with input replay.</b>",
   "<b>Then remove the replay</b> (snap only) and demonstrate the "
   "character jerking backwards on every update.",
   "Add smoothing with a threshold. Tune the threshold and report what "
   "each value feels like.",
   "<b>Log correction magnitudes</b> and plot the distribution at 50, 150, "
   "and 300 ms.",
   "Implement entity interpolation with a 100 ms buffer.",
   "<b>Shrink the buffer until remote players stutter</b> and report the "
   "threshold against your jitter.",
   "Implement extrapolation instead and <b>demonstrate the warping on "
   "direction change</b>.",
   "<b>Implement rollback</b> for a two-player simulation and measure how "
   "many frames you can re-simulate within one frame's budget.",
 ],
 "selfcheck": [
   "What does client-side prediction do, and why is the client usually "
   "right?",
   "Describe reconciliation's four steps and say why the replay matters.",
   "What happens if you snap without replaying?",
   "When should a correction be smoothed and when snapped?",
   "Why can you predict yourself but not other players?",
   "What does interpolation cost, and what does it buy?",
   "Name six artifacts and the technique each comes from.",
   "Describe rollback and its three requirements.",
   "Why do players prefer rollback to input delay?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Trust, Cheating, and Fairness",
 "subtitle": "Byzantine participants, and a referee that cannot see "
             "everything.",
 "question": "What can you believe a client when it tells you?",
 "outcomes": [
     "Apply the authoritative-server principle consistently.",
     "Explain lag compensation and the unfairness it creates.",
     "Classify cheats by what they exploit.",
     "Explain why information hiding beats detection.",
     "Reason about anti-cheat trade-offs honestly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The principle",
   "blurb": "What a client may be permitted to decide."},

  {"t": "callout", "title": "The client may report intent, never outcome",
   "kind": "The one rule",
   "body": ["<b>'I am pressing forward' is intent.</b> The server decides "
            "whether that results in movement.",
            "<b>'I moved to (x, y, z)' is an outcome</b>, and accepting it "
            "is a teleport hack waiting to be written.",
            "<b>'I fired at this angle on tick 4821' is intent.</b> "
            "<b>'I hit the enemy for 40 damage' is an outcome</b>, and "
            "accepting it is an aimbot that does not even need to aim.",
            "<b>Every single exploit is this rule being broken "
            "somewhere</b> — usually for a good reason, under deadline, "
            "with a comment saying it will be fixed later."]},

  {"t": "bullets", "kicker": "Validation", "title": "What the server must check on every input",
   "items": [
     "<b>Is this movement physically possible</b> from the last known "
     "position in the elapsed time?",
     "",
     "<b>Is the action permitted</b> — is the weapon owned, the ability "
     "off cooldown, the player alive?",
     "",
     "<b>Is the rate plausible?</b> Inputs arriving faster than real time "
     "are a speedhack.",
     "",
     "<b>Is the target reachable</b> — line of sight, range, and not "
     "through a wall?",
     "",
     "<b>And is the tick number sane</b> — not in the future, not far in "
     "the past, not repeated.",
   ],
   "footnote": "<b>These checks are the entire security model.</b> "
               "Everything else is making them harder to work around."},

  {"t": "section", "label": "Part 2", "title": "Lag compensation",
   "blurb": "Fair for the shooter, unfair for the target."},

  {"t": "code", "kicker": "Rewind", "title": "Lag compensation, and its cost",
   "lang": "text", "code": """
  THE PROBLEM
      the shooter sees the target where it was
          (their latency) + (interpolation delay) ago
      so aiming at what they see and firing MISSES, because the
      server has since moved the target. Shots that visually
      connect are scored as misses.

  LAG COMPENSATION
      the server keeps a HISTORY of every player's position,
      one entry per tick, for ~1 second.
      when a shot arrives tagged with tick N:
          REWIND every other player to their tick-N position
          perform the hit test against that rewound world
          restore the present
      -> the shot hits what the shooter actually saw. Fair.

  THE COST -- "SHOT AROUND A CORNER"
      the target has, in the meantime, moved behind cover.
      On THEIR screen they are safe. They take damage anyway,
      because at tick N they were not safe.

  BOTH PLAYERS EXPERIENCED THE GAME CORRECTLY AND THEY
  DISAGREE. This is not a bug. It is the irreducible cost of
  a shared world with no shared present (Module 03).
""",
   "caption": "<b>You cannot have both.</b> Favouring the shooter or the "
              "target is a design decision, and it must be made "
              "deliberately.",
   "note": "That both players are right is the point. Say it plainly."},

  {"t": "callout", "title": "Who to favour is a design decision",
   "kind": "How games actually choose",
   "body": ["<b>Favour the shooter</b> — full lag compensation. Shots "
            "land where they looked. <b>Most competitive shooters choose "
            "this</b>, because aiming that does not work is intolerable.",
            "<b>Favour the target</b> — no compensation. Taking cover "
            "always works. <b>Shots feel unreliable</b>, which players "
            "blame on the game.",
            "<b>Bound the rewind</b> — compensate up to 200 ms and no "
            "further. <b>This is the usual compromise</b>, and it caps how "
            "much a high-latency player can exploit.",
            "<b>And some games favour the target for melee</b> and the "
            "shooter for ranged, because the perceptual expectations "
            "differ. <b>There is no correct answer, only a stated "
            "one.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Cheats",
   "blurb": "Classified by what they exploit."},

  {"t": "table", "kicker": "Taxonomy", "title": "What cheats exploit, and what stops them",
   "header": ["Cheat", "Exploits", "Defence"],
   "widths": [2.7, 4.3, 5.1],
   "rows": [
     ["<b>Speedhack</b>", "<b>Client-controlled timing</b>", "<b>Server validates input rate. Solved</b>"],
     ["<b>Teleport / fly</b>", "<b>Accepted position updates</b>", "<b>Server validates movement. Solved</b>"],
     ["<b>Aimbot</b>", "<b>Information the client has</b>", "<b>Not solvable; only detectable</b>"],
     ["<b>Wallhack / ESP</b>", "<b>State sent but not rendered</b>", "<b>DO NOT SEND IT. Mostly solvable</b>"],
     ["Macro / scripting", "Input is input", "<b>Undetectable in principle</b>"],
     ["<b>Lag switch</b>", "<b>Disconnection ambiguity</b>", "Rate limits; penalise the pattern"],
   ],
   "footnote": "<b>The split is sharp:</b> cheats that forge outcomes are "
               "solved by validation; cheats that exploit information or "
               "reflexes are not.",
   "note": "That clean split is the most useful thing in the module."},

  {"t": "callout", "title": "Information hiding beats detection",
   "kind": "The most effective defence available",
   "body": ["<b>A wallhack works because the client was sent the position "
            "of a player it cannot see.</b> The renderer hides them; the "
            "memory does not.",
            "<b>So do not send it.</b> Server-side visibility "
            "determination — the relevance filtering of Module 09 "
            "§4 — means the data is not there to extract.",
            "<b>This converts an arms race into an architecture "
            "decision</b>, which is a far better position to be in.",
            "<b>It costs server CPU</b>, it is imperfect (a player about "
            "to come into view must be sent slightly early), <b>and it is "
            "still the single most effective anti-cheat measure "
            "available.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Anti-cheat",
   "blurb": "What the remaining options cost."},

  {"t": "table", "kicker": "Approaches", "title": "Anti-cheat, honestly assessed",
   "header": ["Approach", "Catches", "Costs"],
   "widths": [2.8, 4.2, 5.1],
   "rows": [
     ["<b>Server validation</b>", "<b>All outcome forgery</b>", "<b>CPU. Non-negotiable; do this</b>"],
     ["<b>Information hiding</b>", "<b>Wallhacks, ESP</b>", "<b>CPU. Do this too</b>"],
     ["<b>Statistical detection</b>", "Aimbots, by behaviour", "<b>False positives ban real players</b>"],
     ["<b>Kernel anti-cheat</b>", "<b>Known client tampering</b>", "<b>Ring 0 on the user's machine</b>"],
     ["Player reporting", "<b>What humans notice</b>", "Brigading; abuse"],
     ["<b>Hardware bans</b>", "Repeat offenders", "<b>Spoofable; collateral damage</b>"],
   ],
   "footnote": "<b>Kernel anti-cheat is a genuine security and privacy "
               "cost imposed on every honest player</b>, and it should be "
               "argued for rather than assumed.",
   "note": "Be even-handed here; it's a real trade with real objections."},

  {"t": "callout", "title": "What is actually achievable",
   "kind": "The honest position",
   "body": ["<b>You can make outcome forgery impossible</b> — that is a "
            "solved problem and it is entirely within your control.",
            "<b>You can make information-based cheats much harder</b> by "
            "not sending the information.",
            "<b>You cannot stop a sufficiently motivated attacker</b> who "
            "controls the machine. An external aimbot reading the screen "
            "and moving the mouse is indistinguishable from a skilled "
            "player at the protocol level.",
            "<b>So the goal is to raise the cost above what most people "
            "will pay</b>, and to make the remainder detectable by "
            "behaviour. <b>'Unhackable' is not on offer, and claiming it "
            "is how trust gets lost.</b>"]},
 ],
 "takeaways": [
   "A client may report intent and never outcome; every exploit is that "
   "rule being broken somewhere.",
   "The server must validate movement plausibility, permissions, input "
   "rate, target reachability, and tick sanity — those checks are the "
   "security model.",
   "Lag compensation rewinds the world to the tick the shooter saw, which "
   "makes shots land and lets players be shot behind cover.",
   "Both players experienced the game correctly and they disagree — "
   "that is irreducible, and who to favour is a design decision.",
   "Cheats that forge outcomes are solved by validation; cheats that "
   "exploit information or reflexes are not.",
   "Not sending information the client cannot see converts an arms race "
   "into an architecture decision, and is the most effective measure "
   "available.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The authoritative server principle"),
  ("callout", "The client may report intent, never outcome",
   ["<b>'I am holding the forward key' is intent.</b> The server decides "
    "whether that produces movement, how much, and whether a wall "
    "intervenes.",
    "<b>'I have moved to position (x, y, z)' is an outcome</b>, and a "
    "server that accepts it has shipped a teleport hack — the client "
    "simply reports a different position.",
    "<b>'I fired at this angle on tick 4821' is intent.</b> <b>'I hit the "
    "enemy for 40 damage' is an outcome</b>, and accepting it is an aimbot "
    "that does not even need to aim — the cheat does not have to hit "
    "anything, only to claim it did.",
    "<b>Every single exploit in every game is this rule being broken "
    "somewhere</b> — and it is almost never broken out of ignorance. "
    "It is broken for a good reason, under a deadline, to fix a specific "
    "feel problem or save specific server CPU, with a comment saying it "
    "will be revisited. <b>So the useful discipline is not knowing the "
    "rule but auditing for where it has been relaxed</b>, which should be "
    "a recurring and deliberate exercise rather than a one-time design "
    "decision."]),
  ("ul", ["<b>Is this movement physically possible</b> from the last "
          "validated position within the elapsed time, given the player's "
          "speed, the terrain, and their current state? Catches teleporting "
          "and most flying.",
          "<b>Is the action permitted at all</b> — is the weapon "
          "actually owned, is the ability off cooldown, is the player "
          "alive, do they have the ammunition, are they in a state that "
          "allows it?",
          "<b>Is the input rate plausible?</b> Inputs arriving faster than "
          "real time are a speedhack, and the check is a simple comparison "
          "against the wall clock with a tolerance for jitter.",
          "<b>Is the target reachable</b> — line of sight, within "
          "range, and not through geometry? This requires a server-side "
          "world representation, which is a real cost and is the reason "
          "some games skip it.",
          "<b>And is the claimed tick number sane</b> — not in the "
          "future, not implausibly far in the past (which would exploit lag "
          "compensation, &sect;2), and not one already processed. <b>These "
          "checks collectively are the entire security model</b>; "
          "everything in &sect;4 is making them harder to circumvent rather "
          "than replacing them."]),

  ("h1", "2 &nbsp; Lag compensation"),
  ("code", """THE PROBLEM
  the shooter sees the target where it was (their latency plus
  interpolation delay) ago -- so aiming at what they SEE and
  firing MISSES, because the server has since moved the target.
  Shots that visually connect are scored as misses.

LAG COMPENSATION
  the server keeps a HISTORY of every player's position, one
  entry per tick, for about a second.
  when a shot arrives tagged with tick N:
      REWIND every other player to their tick-N position
      hit-test against that rewound world
      restore the present
  -> the shot hits what the shooter actually saw.

THE COST -- "SHOT AROUND A CORNER"
  the target has since moved behind cover. On THEIR screen they
  are safe. They take damage anyway, because at tick N they
  were not safe.

BOTH PLAYERS EXPERIENCED THE GAME CORRECTLY AND THEY DISAGREE."""),
  ("p", "<b>That last line is the point, and it is worth stating "
        "plainly.</b> Neither player is wrong, neither client is buggy, and "
        "no amount of engineering removes the disagreement. <b>It is the "
        "irreducible cost of a shared world with no shared present</b> "
        "(Module 03 &sect;1) — the same impossibility that made "
        "logical clocks necessary, surfacing here as a gameplay complaint "
        "rather than as a theorem."),
  ("callout", "Who to favour is a design decision",
   ["<b>Favour the shooter</b> — full lag compensation. Shots land "
    "where the player aimed, and victims are occasionally hit after "
    "reaching cover. <b>Most competitive shooters choose this</b>, because "
    "aiming that does not work is intolerable to players in a way that "
    "being hit unfairly is not.",
    "<b>Favour the target</b> — no compensation. Taking cover always "
    "works, and <b>shots feel unreliable</b>, which players attribute to "
    "the game being broken rather than to their own latency.",
    "<b>Bound the rewind</b> — compensate up to perhaps 200 ms and no "
    "further. <b>This is the usual compromise</b>: it covers the great "
    "majority of honest connections while capping how much advantage a "
    "deliberately high-latency player can extract (&sect;3's lag switch).",
    "<b>And some games choose differently per mechanic</b> — favour "
    "the shooter for ranged weapons and the target for melee, because the "
    "perceptual expectations genuinely differ: a bullet that misses feels "
    "like a bug, while a sword swing that misses feels like a dodge. "
    "<b>There is no correct answer, only a stated one</b>, and the games "
    "that handle this best document their choice to players rather than "
    "leaving them to infer it from frustration."]),

  ("break",),
  ("h1", "3 &nbsp; Cheats, classified"),
  ("table", ["Cheat", "What it exploits", "Defence"],
   [["<b>Speedhack</b>",
     "<b>Client-controlled timing</b> — the client claims more time "
     "has passed than has.",
     "<b>Server validates input rate against the wall clock. Solved "
     "completely.</b>"],
    ["<b>Teleport, fly, noclip</b>",
     "<b>A server that accepts client-reported positions.</b>",
     "<b>Server validates movement plausibility (&sect;1). Solved "
     "completely.</b>"],
    ["<b>Aimbot</b>",
     "<b>Information the client legitimately has</b> — it must know "
     "where visible enemies are in order to draw them.",
     "<b>Not solvable, only detectable.</b> The inputs are "
     "indistinguishable from a very good player's; only the statistical "
     "signature differs (&sect;4)."],
    ["<b>Wallhack and ESP</b>",
     "<b>State the server sent but the renderer chose not to draw.</b>",
     "<b>Do not send it</b> — see the callout. <b>Mostly solvable, and "
     "this is the highest-leverage defence available.</b>"],
    ["<b>Macros and scripting</b>",
     "Input is input; a recoil-control macro produces legitimate inputs.",
     "<b>Undetectable in principle</b> at the protocol level. Policy and "
     "statistical detection only."],
    ["<b>Lag switch</b>",
     "<b>The disconnection ambiguity</b> (Module 07 &sect;4) — "
     "deliberately inducing loss to exploit the grace period.",
     "Rate limits, bounded compensation (&sect;2), and penalising the "
     "pattern rather than the individual event."]],
   [0.19, 0.39, 0.42]),
  ("p", "<b>The split is sharp and is the most useful thing in this "
        "module: cheats that forge <i>outcomes</i> are completely solved by "
        "server validation, and cheats that exploit <i>information</i> or "
        "<i>reflexes</i> are not solvable at all.</b> Knowing which "
        "category a reported cheat falls into tells you immediately whether "
        "you have a bug to fix or a trade-off to manage."),
  ("callout", "Information hiding beats detection",
   ["<b>A wallhack works because the client was sent the position of a "
    "player it cannot see.</b> The renderer declines to draw them; the "
    "memory contains them regardless, and reading memory on a machine you "
    "own is not difficult.",
    "<b>So do not send it.</b> Server-side visibility determination "
    "— the relevance filtering of Module 09 &sect;4, applied as a "
    "security measure rather than a bandwidth one — means the data is "
    "simply not present on the client to be extracted.",
    "<b>This converts an arms race into an architecture decision</b>, which "
    "is an enormously better position: an arms race must be continuously "
    "funded forever, while an architecture decision is made once.",
    "<b>It costs server CPU</b> (visibility must now be computed "
    "per-client, authoritatively), <b>and it is imperfect</b> — a "
    "player about to round a corner must be sent slightly before they are "
    "visible, or they will pop in late, so a small amount of "
    "soon-to-be-visible information inevitably leaks. <b>And it remains "
    "the single most effective anti-cheat measure available</b>, "
    "substantially more so than anything in &sect;4, which is why it is "
    "worth the CPU."]),

  ("h1", "4 &nbsp; Anti-cheat, honestly assessed"),
  ("table", ["Approach", "What it catches", "What it costs"],
   [["<b>Server-side validation</b>", "<b>All outcome forgery</b> "
     "(&sect;1).",
     "<b>Server CPU. Non-negotiable — do this before anything "
     "else.</b>"],
    ["<b>Information hiding</b>", "<b>Wallhacks and ESP</b> (&sect;3).",
     "<b>More server CPU. Do this too</b>, and it pays for itself in "
     "bandwidth."],
    ["<b>Statistical behavioural detection</b>",
     "Aimbots and macros, by their signature — reaction times, "
     "snap angles, and consistency that humans do not produce.",
     "<b>False positives ban real players</b>, who are extremely difficult "
     "to re-acquire. Requires a human appeal path, which is an ongoing "
     "operational cost."],
    ["<b>Kernel-level anti-cheat</b>",
     "<b>Known client tampering, injected code, and debuggers.</b>",
     "<b>Ring 0 code on every honest player's machine</b> — a genuine "
     "security and privacy cost, a real crash and incompatibility risk, and "
     "a meaningful attack surface. <b>It should be argued for explicitly, "
     "not assumed</b>, and the objections to it are reasonable."],
    ["<b>Player reporting</b>",
     "<b>What humans notice</b>, which is a surprisingly good signal.",
     "Brigading and abuse; needs weighting by reporter reliability."],
    ["<b>Hardware bans</b>", "Repeat offenders, for a while.",
     "<b>Spoofable, and causes collateral damage</b> on shared or resold "
     "machines."]],
   [0.21, 0.36, 0.43]),
  ("callout", "What is actually achievable",
   ["<b>You can make outcome forgery impossible.</b> That is a solved "
    "problem, it is entirely within your control, and it requires no "
    "cooperation from the client. <b>Every game that is cheated by "
    "teleporting or by claimed damage has simply not done it.</b>",
    "<b>You can make information-based cheats dramatically harder</b> by "
    "not sending the information (&sect;3). Not perfectly, but enough to "
    "move the cheat from trivial to genuinely difficult.",
    "<b>You cannot stop a sufficiently motivated attacker who controls the "
    "machine.</b> An external aimbot that reads the screen with a capture "
    "card on a second computer and moves the mouse with a microcontroller "
    "<b>is indistinguishable from a skilled player at every level you have "
    "access to</b> — the inputs are real mouse movements from real "
    "hardware. This is not a gap to be closed; it is a consequence of the "
    "attacker owning the endpoint.",
    "<b>So the realistic goal is to raise the cost above what most people "
    "will pay, and to make what remains detectable by behaviour over "
    "time.</b> <b>'Unhackable' is not on offer</b>, and claiming it is how "
    "a studio loses its players' trust — which is worth more than the "
    "marketing. <b>This is the same honesty principle as every other "
    "'claiming honestly' section in this program:</b> state what you "
    "established and what you did not."]),
 ],
 "resources": [
   ("Valve &mdash; Latency Compensating Methods (free)",
    "https://developer.valvesoftware.com/wiki/Latency_Compensating_Methods_in_Client/Server_In-game_Protocol_Design_and_Optimization",
    "<b>The &sect;2 rewind technique</b>, documented by the people who "
    "popularised it, including the shot-around-a-corner consequence."),
   ("Glenn Fiedler &mdash; cheat prevention in networked games (free)",
    "https://gafferongames.com/post/what_every_programmer_needs_to_know_about_game_networking/",
    "The &sect;1 principle, stated as a design rule."),
   ("Riot Games &mdash; engineering blog on Valorant's netcode and "
    "anti-cheat (free)",
    "https://technology.riotgames.com/news/peeking-valorants-netcode",
    "<b>Server-side visibility (&sect;3) as a deliberate anti-cheat "
    "architecture</b>, with the CPU cost discussed openly. The best "
    "available account of the information-hiding argument."),
   ("Hoglund & McGraw &mdash; Exploiting Online Games",
    "https://www.pearson.com/en-us/subject-catalog/p/exploiting-online-games-cheating-massively-distributed-systems/P200000009238",
    "The attacker's perspective on &sect;3. Dated in specifics and "
    "accurate in structure."),
 ],
 "exercises": [
   "<b>Audit your Module 09 project for every place a client reports an "
   "outcome</b> rather than an intent. Fix them.",
   "Implement all five server-side validation checks.",
   "<b>Write a speedhack</b> against your own unvalidated server, then "
   "defeat it with rate validation.",
   "<b>Write a teleport hack</b>, then defeat it with movement "
   "validation.",
   "Implement lag compensation with a one-second position history.",
   "<b>Demonstrate the shot-around-a-corner case</b> from both players' "
   "points of view, and record both.",
   "Bound the rewind to 200 ms and show what a 400 ms player now "
   "experiences.",
   "<b>Implement server-side visibility determination</b> and verify that "
   "a hidden player's position is genuinely absent from the client's "
   "received packets.",
   "Measure the server CPU cost of that visibility determination against "
   "player count.",
   "<b>Write one page assessing your own game's cheat resistance "
   "honestly</b> — what is solved, what is mitigated, and what is not "
   "addressed.",
 ],
 "selfcheck": [
   "State the intent-versus-outcome rule and give two examples of each.",
   "Name five server-side validation checks.",
   "Explain lag compensation and the problem it solves.",
   "Why do both players experience the game correctly and still disagree?",
   "Give three ways to resolve who is favoured.",
   "Classify six cheats by what they exploit, and say which are solvable.",
   "Why does information hiding beat detection?",
   "Give six anti-cheat approaches and the cost of each.",
   "What is actually achievable, and what is not?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Cloud, Scaling, and Economics",
 "subtitle": "What it costs, and what the bill is actually for.",
 "question": "When does the cloud help, and what do you pay for it?",
 "outcomes": [
     "Explain elasticity and what it is worth.",
     "Compare the compute abstractions and their trade-offs.",
     "Explain data gravity and egress economics.",
     "Explain autoscaling and why it is harder than it looks.",
     "Decide honestly between cloud and owned hardware.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What you are buying",
   "blurb": "Elasticity, not cheap compute."},

  {"t": "callout", "title": "The cloud sells elasticity, and it is expensive per unit",
   "kind": "The economics, stated plainly",
   "body": ["<b>Rented compute costs several times owned compute</b>, "
            "amortised over three years. That is not a secret and it is "
            "not the point.",
            "<b>What you are buying is the ability to have zero servers "
            "on Monday and four hundred on Friday</b>, and to pay for "
            "neither when you do not need them.",
            "<b>So the cloud wins when load is variable, unpredictable, or "
            "growing</b> — a launch, a seasonal peak, an experiment, a "
            "startup that might fail.",
            "<b>And it loses when load is steady and known.</b> <b>A game "
            "with a stable player count running 24/7 is the textbook case "
            "for owned hardware</b>, and several large companies have "
            "repatriated for exactly this reason."]},

  {"t": "table", "kicker": "Abstractions", "title": "The compute options",
   "header": ["Abstraction", "You manage", "Suits"],
   "widths": [2.8, 4.2, 5.1],
   "rows": [
     ["<b>Bare metal</b>", "<b>Everything</b>", "<b>Steady load; latency-critical; GPUs</b>"],
     ["<b>VMs</b>", "OS and up", "The default; flexible"],
     ["<b>Containers</b>", "<b>The image; a scheduler runs it</b>", "<b>Most services. Kubernetes if you must</b>"],
     ["<b>Serverless</b>", "<b>A function</b>", "<b>Spiky, stateless, short. Cold starts</b>"],
     ["Managed services", "<b>Configuration only</b>", "<b>Databases, queues. Usually right</b>"],
   ],
   "footnote": "<b>Prefer managed services for stateful things.</b> "
               "Operating a database correctly is a specialism and the "
               "price is usually worth it.",
   "note": "The managed-database advice saves more pain than anything "
           "else here."},

  {"t": "section", "label": "Part 2", "title": "Where the bill comes from",
   "blurb": "Not where people expect."},

  {"t": "callout", "title": "Egress and data gravity",
   "kind": "The two things that dominate real bills",
   "body": ["<b>Ingress is usually free; egress is charged, and it adds "
            "up fast.</b> A game streaming state to a hundred thousand "
            "clients pays per byte, continuously.",
            "<b>And cross-zone and cross-region traffic is charged "
            "<i>inside</i> the cloud too</b> — a chatty microservice "
            "architecture spread across availability zones pays for its "
            "own internal chatter.",
            "<b>Data gravity: once a petabyte is in one provider, moving "
            "it costs more than leaving it.</b> The egress charge is the "
            "lock-in mechanism, whether or not it was designed as one.",
            "<b>So compute is portable and data is not.</b> <b>Architect "
            "for that</b> — and measure egress from the first week, "
            "because nobody budgets for it."]},

  {"t": "section", "label": "Part 3", "title": "Autoscaling",
   "blurb": "Harder than the marketing suggests."},

  {"t": "callout", "title": "Autoscaling reacts to a signal that lags the problem",
   "kind": "Why it is hard",
   "body": ["<b>By the time CPU is high, users are already waiting</b> "
            "— and a new instance takes 30 seconds to several minutes to "
            "be useful.",
            "<b>So scaling on a lagging metric is always late</b>, and "
            "scaling on a leading one (queue depth, request rate) requires "
            "knowing the relationship.",
            "<b>And it can oscillate.</b> Scale up, load per node falls, "
            "scale down, load rises, scale up — <b>hysteresis and "
            "cooldowns exist to prevent this</b> and must be tuned.",
            "<b>Worse: scaling can make things worse.</b> New instances "
            "with cold caches, or that all reconnect to the database at "
            "once, can deepen the incident they were meant to relieve."]},

  {"t": "bullets", "kicker": "Practice", "title": "What actually works",
   "items": [
     "<b>Scale on a leading indicator</b> — queue depth or request "
     "rate, not CPU.",
     "",
     "<b>Pre-warm for predictable peaks.</b> A game's evening peak is "
     "known; scale on the clock, not on the symptom.",
     "",
     "<b>Scale up fast, down slow.</b> The costs are asymmetric — "
     "being too small is an outage, being too large is a line item.",
     "",
     "<b>Set a maximum.</b> <b>A runaway autoscaler responding to a bug "
     "produces a very large bill</b>, and it has happened to many people.",
     "",
     "<b>And load-shed rather than collapse</b> — serving 90% of users "
     "beats serving none.",
   ],
   "footnote": "<b>The maximum is the one people skip</b> and then learn "
               "about from their invoice."},

  {"t": "section", "label": "Part 4", "title": "Game servers specifically",
   "blurb": "An unusual workload."},

  {"t": "table", "kicker": "Games", "title": "Why game hosting is different",
   "header": ["Property", "Consequence"],
   "widths": [3.6, 8.5],
   "rows": [
     ["<b>Stateful sessions</b>", "<b>Cannot move a match mid-game; no simple load balancing</b>"],
     ["<b>Latency-bound</b>", "<b>Must be near players — many regions, each small</b>"],
     ["<b>Sharply peaked</b>", "<b>Evenings and weekends; 5–10× the trough</b>"],
     ["Launch spikes", "<b>Day one can be 50× month two</b>"],
     ["<b>Long-lived processes</b>", "<b>Serverless does not fit at all</b>"],
     ["<b>CPU-bound simulation</b>", "Cores matter more than memory"],
   ],
   "footnote": "<b>Hybrid is the usual answer:</b> own the baseline "
               "capacity, burst to cloud for peaks and launches.",
   "note": "The hybrid conclusion is what most studios actually land on."},

  {"t": "callout", "title": "Deciding honestly",
   "kind": "The question to answer",
   "body": ["<b>What is the ratio of your peak to your trough?</b> Under "
            "2:1, owned hardware probably wins. Over 10:1, the cloud "
            "probably does.",
            "<b>How predictable is the peak?</b> Predictable peaks can be "
            "pre-provisioned either way.",
            "<b>How much data leaves?</b> Egress at scale can exceed the "
            "compute bill entirely.",
            "<b>And what is your team's time worth?</b> <b>Managed "
            "services buy back operational attention</b>, which for a small "
            "team is usually the dominant term — and is the argument "
            "least often made explicitly."]},
 ],
 "takeaways": [
   "The cloud sells elasticity at a premium per unit; it wins on variable "
   "or unpredictable load and loses on steady known load.",
   "Prefer managed services for stateful things — operating a database "
   "correctly is a specialism.",
   "Egress and cross-zone traffic dominate real bills, and the egress "
   "charge is the lock-in mechanism.",
   "Autoscaling reacts to a lagging signal, can oscillate, and can deepen "
   "the incident it was meant to relieve.",
   "Scale on a leading indicator, pre-warm predictable peaks, scale up fast "
   "and down slow, and always set a maximum.",
   "Game hosting is stateful, latency-bound, and sharply peaked, so hybrid "
   "— own the baseline, burst for peaks — is the usual answer.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What you are actually buying"),
  ("callout", "The cloud sells elasticity, and it is expensive per unit",
   ["<b>Rented compute costs several times what owned compute costs</b> "
    "when amortised over a three-year hardware life. This is not a secret, "
    "the providers do not dispute it, and it is not the point of the "
    "product.",
    "<b>What you are buying is the ability to have zero servers on Monday "
    "and four hundred on Friday</b>, provisioned in minutes, and to pay for "
    "neither at any other time. You are buying the removal of a capital "
    "decision and a lead time.",
    "<b>So the cloud wins when load is variable, unpredictable, or "
    "growing</b> — a product launch, a seasonal peak, an experiment "
    "that may be cancelled, a startup that may not exist in a year. "
    "<b>Optionality has real value and the premium buys it.</b>",
    "<b>And it loses when load is steady and known.</b> <b>A game with a "
    "stable player count running continuously is the textbook case for "
    "owned hardware</b> — and several large companies have "
    "repatriated workloads for exactly this reason, which is worth "
    "knowing because the default assumption now runs the other way."]),
  ("table", ["Abstraction", "What you manage", "What it suits"],
   [["<b>Bare metal</b>", "<b>Everything, including the hardware.</b>",
     "<b>Steady predictable load, latency-critical work, and GPU "
     "workloads</b> where virtualisation overhead or availability is a "
     "problem."],
    ["<b>Virtual machines</b>", "The operating system and everything above.",
     "The flexible default. Full control, and you own patching, "
     "monitoring, and configuration."],
    ["<b>Containers</b>",
     "<b>The image; a scheduler decides where it runs.</b>",
     "<b>Most stateless services.</b> Kubernetes if the scale genuinely "
     "warrants it — it is a substantial operational commitment and is "
     "frequently adopted well before it is needed."],
    ["<b>Serverless functions</b>", "<b>A function and its dependencies.</b>",
     "<b>Spiky, stateless, short-lived work.</b> <b>Cold starts</b> make it "
     "unsuitable for latency-sensitive paths, and the per-invocation "
     "pricing becomes expensive at sustained high volume."],
    ["<b>Managed services</b>", "<b>Configuration only.</b>",
     "<b>Databases, queues, caches, object storage.</b> <b>Usually the "
     "right choice</b> — operating a database correctly across "
     "backups, failover, upgrades, and replication is a genuine "
     "specialism, and the price premium is usually smaller than the cost of "
     "learning it badly."]],
   [0.17, 0.33, 0.50]),

  ("h1", "2 &nbsp; Where the bill comes from"),
  ("callout", "Egress and data gravity",
   ["<b>Ingress is typically free and egress is charged</b>, at rates that "
    "add up far faster than people expect. <b>A game streaming state to a "
    "hundred thousand concurrent clients pays per byte, continuously</b>, "
    "and that line can exceed the compute bill — which makes the "
    "bandwidth optimisations of Module 09 &sect;4 directly financial rather "
    "than merely technical.",
    "<b>And cross-zone and cross-region traffic is charged <i>inside</i> "
    "the cloud too.</b> A chatty microservice architecture spread across "
    "availability zones for resilience pays for every internal call that "
    "crosses a zone boundary — <b>so an architectural choice made for "
    "availability has a continuous and largely invisible cost</b>, and it "
    "is usually discovered during a cost review rather than a design "
    "review.",
    "<b>Data gravity: once a petabyte lives in one provider, moving it "
    "costs more than leaving it.</b> The egress charge on the full dataset "
    "may exceed a year of storage, so the data stays and the compute that "
    "uses it must stay with it. <b>The egress charge is the lock-in "
    "mechanism</b>, whether or not it was designed as one.",
    "<b>So compute is portable and data is not.</b> <b>Architect with that "
    "asymmetry in mind</b>, and <b>measure egress from the first week</b> "
    "— it is the line nobody budgets for and the one that produces "
    "surprises."]),

  ("break",),
  ("h1", "3 &nbsp; Autoscaling"),
  ("callout", "Autoscaling reacts to a signal that lags the problem",
   ["<b>By the time CPU utilisation is high, users are already waiting</b> "
    "— and a new instance takes anywhere from thirty seconds to "
    "several minutes to boot, warm up, pass health checks, and begin "
    "serving.",
    "<b>So scaling on a lagging metric is structurally always late.</b> "
    "Scaling on a leading indicator — queue depth, request arrival "
    "rate, connection count — is better, and requires understanding "
    "the relationship between that indicator and the capacity needed, which "
    "has to be measured rather than guessed.",
    "<b>And it can oscillate.</b> Scale up, per-node load falls below the "
    "scale-down threshold, scale down, load rises, scale up again. "
    "<b>Hysteresis and cooldown periods exist precisely to prevent this</b> "
    "and they have to be tuned against the actual startup time — "
    "which is the same flapping problem as Module 07 &sect;4, in a "
    "different domain.",
    "<b>Worse, scaling can deepen the incident it was meant to "
    "relieve.</b> New instances start with cold caches and serve slowly; "
    "they all open database connections simultaneously and exhaust the "
    "connection pool; they all fetch the same configuration at once. "
    "<b>A scaling event during an overload can be the thing that turns a "
    "degradation into an outage</b>, which is why scale-up needs to be "
    "rate-limited as well as fast."]),
  ("ul", ["<b>Scale on a leading indicator</b> — queue depth or "
          "request rate rather than CPU — and validate the "
          "relationship with a load test rather than assuming it.",
          "<b>Pre-warm for predictable peaks.</b> <b>A game's evening peak "
          "is known to the hour</b>, so scale on the clock rather than "
          "waiting for the symptom. Scheduled scaling is unglamorous and is "
          "usually better than reactive scaling.",
          "<b>Scale up fast and down slow.</b> The costs are deeply "
          "asymmetric: <b>being too small is an outage and being too large "
          "is a line item</b>, so the thresholds should not be symmetric "
          "either.",
          "<b>Set a maximum.</b> <b>A runaway autoscaler responding to a "
          "bug — an infinite retry loop, a queue that never drains "
          "— produces a very large bill very quickly</b>, and this has "
          "happened to a great many people. <b>The maximum is the control "
          "people skip</b> and then learn about from their invoice.",
          "<b>And load-shed rather than collapse.</b> <b>Serving 90% of "
          "users well beats serving 100% of them badly or none of them at "
          "all</b>, and that policy has to be designed in — a system "
          "that has no shedding mechanism will simply fall over."]),

  ("h1", "4 &nbsp; Game servers specifically"),
  ("table", ["Property", "Consequence"],
   [["<b>Sessions are stateful and long-lived.</b>",
     "<b>A match cannot be moved mid-game</b>, so ordinary load balancing "
     "does not apply — you place a session at start and live with the "
     "decision. Draining a node means waiting for matches to end."],
    ["<b>Latency-bound.</b>",
     "<b>Servers must be physically near players</b>, so you need many "
     "regions each running modest capacity — which is the opposite of "
     "the consolidation that makes capacity planning easy."],
    ["<b>Sharply peaked demand.</b>",
     "<b>Evenings and weekends run five to ten times the trough</b>, and "
     "the peak moves around the world with the timezone — which is "
     "either an opportunity (follow the sun with the same capacity) or a "
     "complication, depending on your architecture."],
    ["<b>Launch spikes.</b>",
     "<b>Day one can be fifty times month two.</b> Provisioning for launch "
     "and owning that hardware afterwards is wasteful; this is the clearest "
     "case for cloud bursting there is."],
    ["<b>Long-lived processes.</b>",
     "<b>Serverless does not fit at all</b> — the model assumes short "
     "stateless invocations and a game server is neither."],
    ["<b>CPU-bound simulation.</b>",
     "Core count and single-thread performance matter far more than memory "
     "or storage, which changes the instance selection."]],
   [0.28, 0.72]),
  ("callout", "Deciding honestly",
   ["<b>What is the ratio of your peak to your trough?</b> Below about 2:1, "
    "owned hardware probably wins on cost. Above about 10:1, the cloud "
    "probably does. <b>Compute that number before having the argument</b>, "
    "because it settles most of it.",
    "<b>How predictable is the peak?</b> A predictable peak can be "
    "pre-provisioned on either platform; an unpredictable one is exactly "
    "what elasticity is for, and is where the premium is worth paying.",
    "<b>How much data leaves?</b> <b>At scale, egress can exceed the "
    "compute bill entirely</b> (&sect;2), and it is the term most likely to "
    "be missing from the comparison spreadsheet.",
    "<b>And what is your team's time worth?</b> <b>Managed services buy "
    "back operational attention</b> — the hours not spent on backups, "
    "failover testing, and patching — and <b>for a small team that is "
    "usually the dominant term in the whole calculation</b>. It is also the "
    "argument least often made explicitly, because it is the hardest to put "
    "a number on, which is not a reason to leave it out."]),
 ],
 "resources": [
   ("Google &mdash; Site Reliability Engineering, chapters on capacity "
    "and load (free)",
    "https://sre.google/books/",
    "<b>The &sect;3 material</b>, including load shedding and the "
    "cascading-failure patterns that scaling can trigger."),
   ("Armbrust et al. &mdash; A View of Cloud Computing (free)",
    "https://www2.eecs.berkeley.edu/Pubs/TechRpts/2009/EECS-2009-28.pdf",
    "<b>The &sect;1 economics</b>, argued carefully. Old, and the argument "
    "is unchanged."),
   ("37signals &mdash; the cloud repatriation writeups (free)",
    "https://world.hey.com/dhh/why-we-re-leaving-the-cloud-3cc8ca24",
    "<b>The counter-case with real numbers.</b> Read alongside the "
    "Berkeley paper rather than instead of it."),
   ("Agones, and the major providers' game-server hosting documentation "
    "(free)",
    "https://agones.dev/",
    "The &sect;4 workload, handled by tooling built specifically for "
    "stateful session placement."),
 ],
 "exercises": [
   "<b>Price your Module 09 project</b> on owned hardware and on three "
   "cloud providers, at your expected scale.",
   "<b>Compute the egress cost</b> from your measured bandwidth per client "
   "per second, at 1,000 and at 100,000 concurrent players.",
   "Measure the cost of the bandwidth optimisations of Module 09 in "
   "currency rather than bytes.",
   "Deploy a service and <b>measure cold start time</b> for VMs, "
   "containers, and serverless.",
   "<b>Implement autoscaling on CPU</b>, then on queue depth, and compare "
   "how late each reacts to a load spike.",
   "<b>Make your autoscaler oscillate</b>, then fix it with hysteresis and "
   "a cooldown.",
   "Simulate a scale-up during overload where new instances exhaust the "
   "database connection pool.",
   "Implement load shedding and show it keeps 90% of users served under an "
   "overload that otherwise collapses.",
   "<b>Compute your peak-to-trough ratio</b> for a real or projected "
   "workload.",
   "<b>Write the honest comparison</b> for your project, including the "
   "team-time term.",
 ],
 "selfcheck": [
   "What does the cloud actually sell, and when does it lose?",
   "Compare five compute abstractions and what each suits.",
   "Why do egress and cross-zone traffic dominate bills?",
   "What is data gravity and how does it create lock-in?",
   "Why is autoscaling structurally late, and how can it oscillate?",
   "How can scaling deepen an incident?",
   "Give five autoscaling practices and say which is most often skipped.",
   "Name six ways game hosting differs, and the usual conclusion.",
   "What four questions decide cloud against owned?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Operating It",
 "subtitle": "Observability, failure, and what you can honestly promise.",
 "question": "How do you run a distributed system and know that it "
             "works?",
 "outcomes": [
     "Instrument a system with metrics, logs, and traces.",
     "Explain why tail latency dominates user experience.",
     "Define SLOs and error budgets and use them to decide.",
     "Explain cascading failure and the patterns that prevent it.",
     "State what a distributed system can honestly promise.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Observability",
   "blurb": "Three signals, and what each is for."},

  {"t": "table", "kicker": "Signals", "title": "Metrics, logs, and traces",
   "header": ["Signal", "Answers", "Cost"],
   "widths": [2.6, 4.5, 5.0],
   "rows": [
     ["<b>Metrics</b>", "<b>Is something wrong, and since when?</b>", "<b>Cheap; aggregated; low cardinality</b>"],
     ["<b>Logs</b>", "<b>What exactly happened to this request?</b>", "<b>Expensive at volume; sample them</b>"],
     ["<b>Traces</b>", "<b>Where did the time go across services?</b>", "<b>The one that actually finds latency</b>"],
     ["Profiles", "Where did the CPU go inside a service?", "Continuous profiling is now practical"],
   ],
   "footnote": "<b>Distributed tracing is the signal that distinguishes "
               "this from single-machine operations</b>, and it is the one "
               "most often missing.",
   "note": "If they add one thing: tracing."},

  {"t": "callout", "title": "Trace context must be propagated or tracing is useless",
   "kind": "The implementation detail that decides it",
   "body": ["<b>A trace works because every service passes along the trace "
            "ID it received</b> and attaches its own span to it.",
            "<b>One service that drops the header breaks the trace "
            "there</b>, and the remainder of the request becomes "
            "invisible — which is usually the part you needed.",
            "<b>So propagation must be in the shared framework</b>, not in "
            "each service's code, and it must cross queues and async "
            "boundaries too.",
            "<b>Use W3C Trace Context and OpenTelemetry</b> rather than a "
            "vendor format. <b>The standard exists precisely so that one "
            "service in a different language does not break the chain.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Tail latency",
   "blurb": "Why the average is the wrong number."},

  {"t": "callout", "title": "The tail is the experience, and fan-out amplifies it",
   "kind": "The arithmetic that changes how you measure",
   "body": ["<b>If one service call has a 1% chance of being slow, and a "
            "request makes 100 of them</b>, the chance that <i>none</i> is "
            "slow is 0.99¹⁰⁰ ≈ 37%.",
            "<b>So 63% of requests hit at least one slow call</b>, and the "
            "request is as slow as its slowest component.",
            "<b>The p99 of a component becomes the <i>median</i> of a "
            "fanned-out request.</b> That is the whole problem.",
            "<b>So measure p99 and p99.9, never the mean</b> — and the "
            "fixes are hedged requests, tied requests, and reducing "
            "fan-out. <b>This is CSCE 735's 'report the distribution' and "
            "CSCE 650's 'worst frame' argument, again.</b>"]},

  {"t": "callout", "title": "SLOs and error budgets",
   "kind": "Turning reliability into a decision",
   "body": ["<b>An SLO is a target: 99.9% of requests succeed in under "
            "200 ms, measured over 30 days.</b>",
            "<b>The error budget is what remains: 0.1%.</b> That is "
            "roughly 43 minutes a month of permitted failure.",
            "<b>Budget remaining ⟹ ship. Budget exhausted ⟹ "
            "stop shipping and fix reliability.</b> The argument about "
            "whether to prioritise features or stability becomes "
            "arithmetic.",
            "<b>And 100% is the wrong target.</b> It is unattainable, "
            "unaffordable, and the last nine costs more than it is worth. "
            "<b>An unused error budget means you are shipping too "
            "slowly.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Cascading failure",
   "blurb": "How a small problem becomes an outage."},

  {"t": "code", "kicker": "Cascade", "title": "The standard sequence",
   "lang": "text", "code": """
  1. one service slows down slightly
  2. its callers' requests take longer, so their threads and
     connections are held longer
  3. the callers' pools exhaust -- now THEY are slow, for
     requests that have nothing to do with the original service
  4. their callers exhaust, and so on upstream
  5. clients time out and RETRY, multiplying the load
  6. the original service, now receiving several times its
     normal traffic, fails completely
  7. it restarts with a cold cache and fails again immediately

  THE PATTERNS THAT BREAK THE CHAIN:
    TIMEOUTS        bound how long anything can be held
                    (and they must be SHORTER upstream than down)
    BULKHEADS       separate pools per dependency, so one slow
                    dependency cannot exhaust everything
    CIRCUIT BREAKER after N failures, fail FAST without calling
    BACKPRESSURE    reject early rather than queue forever
    LOAD SHEDDING   drop low-priority work to protect the rest
    JITTERED BACKOFF  so retries do not synchronise into a wave

  Retries without backoff and jitter CAUSE outages. The
  thundering herd is self-inflicted.
""",
   "caption": "<b>Step 5 is the one that turns a degradation into an "
              "outage</b>, and it is entirely self-inflicted.",
   "note": "The retry amplification point is the most actionable thing "
           "here."},

  {"t": "callout", "title": "Test the failures, because they will not test themselves",
   "kind": "The discipline",
   "body": ["<b>The failure paths are the least-exercised code in the "
            "system</b> and the most important. They are also, by "
            "definition, never run in normal operation.",
            "<b>So inject failures deliberately:</b> kill nodes, partition "
            "the network, add latency, exhaust disks, and do it in "
            "staging, continuously.",
            "<b>Deterministic simulation is better than chaos</b> where "
            "you can manage it — FoundationDB's approach runs the whole "
            "system in one process with a controlled clock and scheduler, "
            "so a failure is <i>reproducible</i>.",
            "<b>That reproducibility is the point.</b> <b>A distributed bug "
            "you cannot reproduce is a bug you cannot fix</b>, and most of "
            "them are not reproducible by default."]},

  {"t": "section", "label": "Part 4", "title": "Claiming honestly",
   "blurb": "The course, the semester, and the program, closed."},

  {"t": "bullets", "kicker": "Claims", "title": "What a distributed system can honestly promise",
   "items": [
     "<b>'Linearizable for single-key operations; causal across "
     "keys.'</b> Specific, and it tells a caller what they have.",
     "",
     "<b>'Tolerates f failures of 2f+1 nodes, assuming "
     "crash-recovery and no Byzantine behaviour.'</b> With the model "
     "stated.",
     "",
     "<b>'99.9% of reads under 50 ms, measured at the client over "
     "30 days.'</b> A percentile, a vantage point, and a window.",
     "",
     "<b>'Verified with a linearizability checker over 10,000 "
     "fault-injected histories.'</b> The evidence, not the hope.",
     "",
     "<b>And what you cannot say: 'highly available' or 'never loses "
     "data'.</b> Say the number, the model, and the assumptions.",
   ],
   "footnote": "<b>Every course in this program ended here</b>, and it is "
               "not a coincidence — it is the one habit that "
               "transfers everywhere."},

  {"t": "callout", "title": "Where this leaves you",
   "kind": "Closing the program",
   "body": ["You can reason about partial failure, choose a consistency "
            "model deliberately, implement consensus, and build netcode "
            "that feels instant while remaining authoritative.",
            "<b>And you know that the impossibility results are narrower "
            "than their reputations, that the ambiguity of a timeout is the "
            "root of nearly everything, and that most systems are "
            "distributed before they need to be.</b>",
            "<b>Semester 5 built what the degree assumed:</b> 620 the "
            "geometry, 605 the compiler, 678 the network.",
            "<b>Fifteen courses, 195 modules.</b> The thread running "
            "through all of them is the same: <b>measure it, state what you "
            "established, and do not claim more than you tested.</b>"]},
 ],
 "takeaways": [
   "Metrics say something is wrong, logs say what happened to one request, "
   "and traces say where the time went — tracing is the signal that "
   "distinguishes distributed operations.",
   "Trace context must be propagated by the shared framework, including "
   "across queues, or one service breaks the chain.",
   "With 100 calls at 1% slow each, 63% of requests hit a slow one — a "
   "component's p99 becomes a fanned-out request's median.",
   "An error budget turns the features-versus-stability argument into "
   "arithmetic, and an unused budget means you are shipping too slowly.",
   "Retries without backoff and jitter cause outages — the thundering "
   "herd is self-inflicted.",
   "Deterministic simulation beats chaos testing because a distributed bug "
   "you cannot reproduce is one you cannot fix.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Observability"),
  ("table", ["Signal", "The question it answers", "Cost and character"],
   [["<b>Metrics</b>",
     "<b>Is something wrong, and since when?</b> Aggregate counters, gauges, "
     "and histograms.",
     "<b>Cheap, because they are aggregated.</b> <b>Keep cardinality "
     "low</b> — a metric labelled by user ID is a time series per user "
     "and will bankrupt the monitoring system."],
    ["<b>Logs</b>",
     "<b>What exactly happened to this particular request?</b>",
     "<b>Expensive at volume.</b> Sample aggressively, log structured data "
     "rather than prose, and always include the trace ID."],
    ["<b>Traces</b>",
     "<b>Where did the time go, across all the services this request "
     "touched?</b>",
     "<b>The signal that actually finds latency problems</b> in a "
     "distributed system, and the one most often missing. See below."],
    ["<b>Continuous profiles</b>",
     "Where did the CPU or memory go <i>inside</i> a service?",
     "Now practical to run continuously in production at low overhead, and "
     "it closes the gap between a slow span and the reason for it."]],
   [0.16, 0.38, 0.46]),
  ("callout", "Trace context must be propagated or tracing is useless",
   ["<b>A distributed trace works because every service passes along the "
    "trace identifier it received</b> and attaches its own span to that "
    "same trace. The trace is assembled afterwards from independently "
    "reported spans that share an ID.",
    "<b>One service that drops the header breaks the trace at that "
    "point</b>, and everything downstream of it becomes invisible — "
    "which is reliably the part you needed to see, because the problem is "
    "usually further in than you expected.",
    "<b>So propagation belongs in the shared framework or middleware</b>, "
    "not in each service's own code where it will be forgotten. <b>And it "
    "must cross asynchronous boundaries too</b> — message queues, "
    "background jobs, and scheduled work are exactly where traces are "
    "usually lost, because the context does not flow naturally through a "
    "queue.",
    "<b>Use W3C Trace Context and OpenTelemetry rather than a vendor "
    "format.</b> <b>The standard exists precisely so that one service "
    "written in a different language with a different library does not "
    "break the chain</b>, which in a polyglot system is not a hypothetical "
    "concern."]),

  ("h1", "2 &nbsp; Tail latency"),
  ("callout", "The tail is the experience, and fan-out amplifies it",
   ["<b>Suppose one service call has a 1% chance of being unusually "
    "slow, and a single user request makes 100 such calls.</b> The "
    "probability that <i>none</i> of them is slow is "
    "0.99<super>100</super>, which is about 37%.",
    "<b>So 63% of requests encounter at least one slow call</b> — and "
    "a request that fans out is only as fast as its slowest component, "
    "because it cannot return until all of them have.",
    "<b>The p99 of a component becomes the <i>median</i> of a fanned-out "
    "request.</b> That single sentence is the whole problem, and it "
    "explains why a system whose every component looks healthy on average "
    "can deliver a consistently poor experience.",
    "<b>So measure p99 and p99.9, and never the mean.</b> The fixes are "
    "<b>hedged requests</b> (send to a second replica if the first is slow, "
    "take whichever answers), <b>tied requests</b> (send to two and cancel "
    "the loser), and <b>reducing fan-out</b> — which is the structural "
    "fix. <b>This is CSCE 735 Module 07's 'report the distribution' and "
    "CSCE 650 Module 06's 'the worst frame is the experience', arrived at "
    "a third time from a third direction</b>, which is reasonable evidence "
    "it is a general truth about systems people interact with."]),
  ("callout", "SLOs and error budgets",
   ["<b>A service level objective is a target with a measurement attached: "
    "99.9% of requests succeed in under 200 ms, measured at the client, "
    "over a rolling 30 days.</b> All four parts matter — the "
    "percentile, the threshold, the vantage point, and the window.",
    "<b>The error budget is what remains: 0.1%.</b> Over 30 days that is "
    "roughly 43 minutes of permitted failure, and <b>it is a budget to be "
    "spent, not a floor to be defended</b>.",
    "<b>Budget remaining means ship. Budget exhausted means stop shipping "
    "features and spend the time on reliability.</b> <b>The recurring "
    "argument between the people who want to ship and the people who want "
    "stability becomes arithmetic</b>, settled in advance by a number "
    "everyone agreed to — which is the real contribution of the idea, "
    "more than the measurement itself.",
    "<b>And 100% is the wrong target.</b> It is unattainable, the last "
    "nine costs more than all the preceding ones, and <b>an error budget "
    "that goes unused every month means you are shipping too "
    "cautiously</b> — you bought reliability you did not need with "
    "velocity you did."]),

  ("break",),
  ("h1", "3 &nbsp; Cascading failure"),
  ("code", """1. one service slows slightly
2. callers' requests take longer, holding threads and connections
3. callers' pools EXHAUST -- now THEY are slow, for requests
   unrelated to the original service
4. their callers exhaust, and so on upstream
5. clients time out and RETRY, MULTIPLYING the load
6. the original service, now at several times normal traffic,
   fails completely
7. it restarts with a cold cache and fails again immediately

PATTERNS THAT BREAK THE CHAIN
  TIMEOUTS          bound how long anything is held -- and they
                    must be SHORTER upstream than downstream
  BULKHEADS         separate pools per dependency
  CIRCUIT BREAKER   after N failures, fail FAST without calling
  BACKPRESSURE      reject early rather than queue forever
  LOAD SHEDDING     drop low-priority work to protect the rest
  JITTERED BACKOFF  so retries do not synchronise into a wave

Retries without backoff and jitter CAUSE outages."""),
  ("p", "<b>Step 5 is the one that converts a degradation into an "
        "outage, and it is entirely self-inflicted.</b> A client library "
        "that retries three times immediately turns a service running at "
        "its limit into one receiving four times its normal load at exactly "
        "the moment it can least handle it. <b>And unjittered backoff "
        "synchronises the retries into waves</b>, so the service recovers, "
        "is immediately flattened by the accumulated wave, and recovers "
        "again — the thundering herd, which is a problem the system "
        "creates for itself."),
  ("callout", "Test the failures, because they will not test themselves",
   ["<b>The failure-handling paths are the least-exercised code in the "
    "system and among the most important.</b> By definition they do not run "
    "in normal operation, so they rot silently — the same argument as "
    "CSCE 605 Module 10 made about debug information.",
    "<b>So inject failures deliberately and continuously:</b> kill "
    "processes, partition the network, add latency and jitter, fill disks, "
    "exhaust connection pools, and slow a dependency without failing it "
    "— which is the case that causes cascades and the one that chaos "
    "tooling often omits.",
    "<b>Deterministic simulation is better than chaos testing wherever you "
    "can manage it.</b> <b>FoundationDB's approach runs the entire system "
    "in a single process with a controlled clock and a controlled "
    "scheduler</b>, so every source of nondeterminism is under test "
    "control and a failing run is <i>reproducible from its seed</i>.",
    "<b>That reproducibility is the entire point.</b> <b>A distributed bug "
    "you cannot reproduce is a bug you cannot fix</b> — you can only "
    "guess, deploy the guess, and wait to see whether it recurs. <b>Most "
    "distributed bugs are not reproducible by default</b>, which is why "
    "building the deterministic harness early (as this course's tooling "
    "section asked) pays for itself many times over."]),

  ("h1", "4 &nbsp; Claiming honestly"),
  ("ul", ["<b>'Linearizable for single-key operations; causal "
          "consistency across keys.'</b> Specific, checkable, and it tells "
          "a caller exactly what they may rely on (Module 04).",
          "<b>'Tolerates f failures out of 2f+1 nodes, assuming "
          "crash-recovery failures and no Byzantine behaviour.'</b> <b>With "
          "the failure model stated</b> (Module 01 &sect;3), because the "
          "guarantee means nothing without it.",
          "<b>'99.9% of reads complete in under 50 ms, measured at the "
          "client, over a rolling 30 days.'</b> A percentile, a vantage "
          "point, and a window — not an average, and not measured on "
          "the server where the network is invisible.",
          "<b>'Verified with a linearizability checker over 10,000 "
          "fault-injected histories, with no violations found.'</b> "
          "<b>The evidence, and its extent</b> — which lets the reader "
          "judge the confidence rather than being asked to accept it.",
          "<b>And what you cannot honestly say: 'highly available', "
          "'never loses data', 'infinitely scalable'.</b> <b>Say the "
          "number, the model, and the assumptions.</b> <b>Every course in "
          "this program ended on this point</b> — CSCE 735 about "
          "speedups, CSCE 620 about robustness, CSCE 605 about "
          "miscompiles, and now this one — <b>and that is not a "
          "coincidence. It is the one habit that transfers to "
          "everything.</b>"]),
  ("callout", "Where this leaves you",
   ["<b>You can reason about partial failure, choose a consistency model "
    "deliberately rather than inheriting one, implement consensus and test "
    "it adversarially, and build netcode that feels instantaneous while "
    "remaining server-authoritative.</b>",
    "<b>And you know several things most practitioners do not:</b> that the "
    "impossibility results are considerably narrower than their "
    "reputations; that the ambiguity of a single timeout is the root of "
    "very nearly everything in the subject; that 'exactly once' does not "
    "exist; and that <b>most systems are distributed some time before they "
    "need to be</b>.",
    "<b>Semester 5 built what the degree had assumed.</b> <b>CSCE 620</b> "
    "supplied the geometry that CSCE 649's collisions and CSCE 647's "
    "acceleration structures had taken for granted. <b>CSCE 605</b> "
    "supplied the compiler behind every shader and every optimisation the "
    "program had relied on. <b>And CSCE 678 supplied the network</b> "
    "— because once the code is correct, fast, and compiled, the only "
    "remaining question is how more than one machine runs it together.",
    "<b>Fifteen courses and 195 modules.</b> The thread running through all "
    "of them is the same, and it is worth stating one final time: "
    "<b>measure it, state what you established, and never claim more than "
    "you tested.</b>"]),
 ],
 "resources": [
   ("Google &mdash; Site Reliability Engineering and the SRE Workbook "
    "(free)",
    "https://sre.google/books/",
    "<b>SLOs, error budgets, and cascading failure</b> — &sect;2 and "
    "&sect;3, from the organisation that formalised them. The "
    "'Addressing Cascading Failures' chapter is the one to read first."),
   ("Dean & Barroso &mdash; The Tail at Scale (free)",
    "https://research.google/pubs/pub40801/",
    "<b>The &sect;2 fan-out arithmetic</b>, with hedged and tied requests. "
    "Short, and among the most useful papers in systems."),
   ("OpenTelemetry and W3C Trace Context (free)",
    "https://opentelemetry.io/",
    "The &sect;1 standard, and the instrumentation libraries for every "
    "major language."),
   ("FoundationDB &mdash; Testing Distributed Systems with Deterministic "
    "Simulation (free)",
    "https://apple.github.io/foundationdb/testing.html",
    "<b>The &sect;3 approach</b>, which is the strongest testing "
    "methodology in this subject and is still not widely adopted."),
   ("Kyle Kingsbury &mdash; Jepsen (free)",
    "https://jepsen.io/analyses",
    "<b>Real distributed databases tested against their own claims</b>, "
    "with the results. The best available argument for &sect;4's "
    "discipline."),
 ],
 "exercises": [
   "Instrument your Module 06 cluster with metrics, structured logs, and "
   "traces.",
   "<b>Drop the trace header in one service</b> and observe what the trace "
   "looks like.",
   "Propagate trace context across a message queue.",
   "<b>Measure p50, p99, and p99.9</b> for your system and report how far "
   "apart they are.",
   "<b>Simulate the fan-out arithmetic:</b> 100 calls at 1% slow, and "
   "measure the fraction of requests affected. Compare against 0.99^100.",
   "Implement hedged requests and measure the effect on p99.",
   "Define an SLO for your project and compute the monthly error budget.",
   "<b>Reproduce a cascading failure</b> with no timeouts and immediate "
   "retries. Then add timeouts, circuit breakers, and jittered backoff, "
   "and show it no longer cascades.",
   "<b>Build a deterministic simulation harness</b> with a controlled "
   "clock and scheduler, and reproduce a failure from its seed.",
   "<b>Project 2 is now due.</b> Submit the netcode implementation, the "
   "measurements at each latency and loss setting, the reconciliation "
   "plot, the demonstrated and defeated cheat, and the honest statement of "
   "where it stops working.",
 ],
 "selfcheck": [
   "Name three observability signals and the question each answers.",
   "Why does trace context propagation decide whether tracing works?",
   "Explain the fan-out arithmetic and why a component's p99 becomes a "
   "request's median.",
   "Define an SLO and an error budget, and say what an unused budget "
   "means.",
   "Give the seven steps of a cascading failure.",
   "Name six patterns that break the chain.",
   "Why do retries cause outages?",
   "Why is deterministic simulation better than chaos testing?",
   "Give four honest claims and three things you cannot say.",
 ],
},

]
