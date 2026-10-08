# -*- coding: utf-8 -*-
"""CSCE 608 Database Systems — original course content."""

COURSE = {
    "code": "CSCE 608",
    "title": "Database Systems",
    "tagline": "How a database is actually built — storage, indexing, "
               "query execution, concurrency, and recovery",
    "term": "Semester 3 (with CSCE 647 and CSCE 649)",
    "prereqs": "CSCE 629 Analysis of Algorithms; CSCE 611 Operating Systems "
               "helpful; fluency in one systems language",
    "effort": "10–12 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A working storage engine: buffer pool, B+tree, query "
                   "executor, concurrency control, and write-ahead logging "
                   "— with crash recovery you have tested by actually "
                   "killing the process",
    "description": [
        "Most courses teach you to <i>use</i> a database. This one teaches "
        "you to build one, which is a different subject and a more useful "
        "one — because once you know what happens underneath, the "
        "behaviour of a real system stops being folklore.",
        "The through-line is a single question: <b>how do you make a "
        "machine that loses power behave as though it did not?</b> Almost "
        "every design decision in a database descends from that. Durability "
        "is why there is a log; the log's cost is why there is a buffer "
        "pool; concurrent access to the buffer pool is why there is "
        "locking; and the cost of locking is why there is multi-version "
        "concurrency control.",
        "The second theme is that <b>the storage hierarchy dictates the "
        "algorithms</b>. A B+tree is not a better binary tree; it is the "
        "data structure you get when a random read costs ten thousand times "
        "a sequential one. Change that ratio — as SSDs did — and the "
        "right answers change with it, which is exactly what has happened to "
        "this field over the last fifteen years.",
        "Everything is implemented. By the end you will have a storage "
        "engine that survives <code>kill -9</code> in the middle of a "
        "transaction, and you will be able to explain exactly why.",
    ],
    "outcomes": [
        "Explain how a DBMS lays out data on disk and why.",
        "Implement a buffer pool with a replacement policy and pin counts.",
        "Implement a B+tree with correct splits, merges, and concurrent "
        "access.",
        "Explain the relational algebra behind SQL and the operators that "
        "implement it.",
        "Implement join algorithms and analyse their I/O cost.",
        "Explain cost-based query optimisation and why it goes wrong.",
        "State the ACID properties precisely and say what each costs.",
        "Implement two-phase locking and explain how MVCC avoids it.",
        "Implement write-ahead logging and ARIES-style recovery.",
        "Explain the trade-offs that distributed databases actually face.",
    ],
    "materials": [
        ("CMU 15-445/645 Database Systems — Andy Pavlo (free video, slides, "
         "projects)",
         "https://15445.courses.cs.cmu.edu/",
         "The primary source. Complete lectures, slides, and the BusTub "
         "project assignments. The best free database systems course that "
         "exists, by some margin."),
        ("CMU 15-721 Advanced Database Systems (free)",
         "https://15721.courses.cs.cmu.edu/",
         "Where modern in-memory and column-store systems are covered. Watch "
         "the relevant lectures after Modules 05 and 09."),
        ("MIT 6.5830 Database Systems (free)",
         "https://dsg.csail.mit.edu/6.5830/",
         "A second voice with a different emphasis — more on query "
         "processing theory and less on implementation detail."),
        ("The Red Book — Readings in Database Systems, 5th ed. (free)",
         "https://www.redbook.io/",
         "Curated classic papers with editorial commentary explaining why "
         "each mattered. Read the commentary even where you skip the paper."),
        ("Database Internals — Alex Petrov (sample chapters free)",
         "https://www.databass.dev/",
         "Strong on storage engines and on distributed systems. Good "
         "complement to the CMU material for Modules 02–04 and 13."),
        ("Architecture of a Database System — Hellerstein, Stonebraker & "
         "Hamilton (free)",
         "https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf",
         "A 100-page tour of how the components fit together. Read it in "
         "week one and again at the end."),
    ],
    "tooling": [
        "<b>C++17</b> or <b>Rust</b>. You are managing memory, page "
        "layouts, and latches; a garbage-collected language hides exactly "
        "what this course is about.",
        "<b>Raw files, not a filesystem abstraction.</b> You need control "
        "over when bytes reach the disk, which means <code>pwrite</code> "
        "and <code>fsync</code> and knowing what each guarantees.",
        "<b>SQLite installed as a reference.</b> Its source is famously "
        "readable and it implements almost everything in this course in "
        "about 150k lines.",
        "<b>PostgreSQL</b> for comparison, and for <code>EXPLAIN "
        "ANALYZE</code> — the single best tool for understanding query "
        "optimisation.",
        "<b>A crash-testing harness</b> that kills your process at a "
        "randomly chosen point and verifies recovery. Build it in "
        "Module 11; it is the only honest test of durability.",
        "<b>A benchmark</b>: YCSB or TPC-C style, so claims about "
        "performance are measured rather than asserted.",
    ],
    "projects": [
        {"title": "A storage engine", "after": 7,
         "brief": "The bottom half of a database. Everything after this "
                  "depends on it, so correctness matters more than speed "
                  "— though you will measure both.",
         "reqs": [
             "A page-based disk manager with a slotted page layout "
             "supporting variable-length records.",
             "A buffer pool with LRU-K or CLOCK replacement, pin counts, "
             "and dirty-page tracking.",
             "A B+tree index supporting insert, delete, point lookup, and "
             "range scan, with correct splits and merges.",
             "Latch-crabbing for concurrent B+tree access.",
             "A sequential scan and an index scan operator.",
             "Instrumentation: page reads, page writes, buffer hit rate, "
             "and tree height, all reported.",
         ],
         "done": [
             "<b>A million-key B+tree that survives a randomised workload "
             "of inserts, deletes, and range scans</b>, verified against an "
             "in-memory reference map after every operation.",
             "A buffer hit rate plot against pool size for a Zipfian "
             "workload. <b>Explain the shape of the curve.</b>",
             "Measured page I/O for a range scan against the analytic "
             "prediction from the tree height and fanout.",
             "<b>Eight threads hammering the tree concurrently with no "
             "corruption and no deadlock</b>, for ten million operations.",
         ]},
        {"title": "Transactions and recovery", "after": 12,
         "brief": "The top half. This is where a database stops being a "
                  "data structure and becomes a database.",
         "reqs": [
             "Two-phase locking with deadlock detection or prevention, and "
             "the deadlock rate reported.",
             "Write-ahead logging with log sequence numbers and the "
             "WAL protocol correctly enforced.",
             "ARIES-style recovery: analysis, redo, undo.",
             "Checkpointing, with the recovery time measured as a function "
             "of checkpoint interval.",
             "<b>Either</b> MVCC with snapshot isolation <b>or</b> "
             "serializable 2PL — with the isolation level you provide "
             "stated precisely and demonstrated.",
         ],
         "done": [
             "<b>A crash test that kills the process at a thousand random "
             "points during a transactional workload, and recovers to a "
             "consistent state every time.</b> Report the thousand results, "
             "not a representative one.",
             "A demonstration of each anomaly your isolation level permits "
             "and each one it prevents, with the SQL that exhibits it.",
             "Throughput against concurrency level, showing where lock "
             "contention begins to dominate.",
             "<b>An honest failure analysis:</b> name a crash point your "
             "recovery would not survive, or prove there is none.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "What a Database Is For",
 "subtitle": "The problems that justify a hundred thousand lines of code.",
 "question": "Why not just use files?",
 "outcomes": [
     "State the problems a DBMS solves that a filesystem does not.",
     "Explain data independence and why it matters.",
     "Describe the layered architecture of a DBMS.",
     "Explain the relational model's actual contribution.",
     "Situate the course's modules within the architecture.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The case for a database",
   "blurb": "Start with files and watch the requirements accumulate."},

  {"t": "bullets", "kicker": "Files", "title": "What goes wrong with files",
   "items": [
     "<b>No structure.</b> Every program must agree on the format, and "
     "changing it means changing every program.",
     "",
     "<b>No concurrent access.</b> Two writers corrupt the file. A reader "
     "sees half-written records.",
     "",
     "<b>No atomicity.</b> Crash mid-update and the file is in a state no "
     "program expects.",
     "",
     "<b>No query capability.</b> Every question needs new code; every "
     "access path is hand-written.",
     "",
     "<b>No scale beyond memory.</b> Sorting a file larger than RAM is a "
     "project in itself.",
   ],
   "note": "Framing it as requirements accumulating makes the architecture "
           "feel inevitable rather than arbitrary."},

  {"t": "callout", "title": "The hard problem is crash consistency",
   "kind": "The through-line of this course",
   "body": ["<b>How do you make a machine that loses power behave as "
            "though it did not?</b>",
            "Almost every design decision in a database descends from that "
            "question.",
            "<b>Durability needs a log.</b> The log's cost needs a buffer "
            "pool. Concurrent access to the buffer pool needs latching. The "
            "cost of locking needs MVCC.",
            "<b>Keep this chain in view.</b> Each module in this course adds "
            "one link, and the architecture stops looking arbitrary once you "
            "see it as a sequence of forced moves."]},

  {"t": "section", "label": "Part 2", "title": "Data independence",
   "blurb": "Codd's actual contribution, which was not tables."},

  {"t": "callout", "title": "The relational model's contribution was independence, not tables",
   "kind": "What 1970 actually changed",
   "body": ["Before Codd, programs navigated data structures "
            "<i>explicitly</i> — follow this pointer, traverse this "
            "chain. The access path was in the application.",
            "<b>So changing the physical layout meant rewriting every "
            "program</b> that touched the data.",
            "<b>Codd separated what you want from how to get it.</b> A query "
            "says which rows, not which pointers; the system chooses the "
            "access path.",
            "<b>That is the whole reason query optimisation exists</b> "
            "(Module 08) — and it is why a database can add an index and "
            "make every existing program faster without changing any of "
            "them."]},

  {"t": "table", "kicker": "Levels", "title": "Three levels of schema",
   "header": ["Level", "Describes", "Independence gained"],
   "widths": [2.6, 4.6, 4.9],
   "rows": [
     ["Physical", "Files, pages, indexes, layout", "—"],
     ["<b>Logical</b>", "Tables, columns, constraints", "<b>Physical independence</b>"],
     ["View / external", "What one application sees", "<b>Logical independence</b>"],
   ],
   "footnote": "<b>Physical independence</b> — reorganise storage "
               "without touching queries — is the one that was "
               "genuinely achieved.",
   "note": "Logical independence is the weaker claim; views only go so far. "
           "Worth being honest about."},

  {"t": "section", "label": "Part 3", "title": "The architecture",
   "blurb": "Where each module of this course sits."},

  {"t": "table", "kicker": "Layers", "title": "A DBMS from the top down",
   "header": ["Layer", "Does", "Module"],
   "widths": [3.2, 5.6, 3.3],
   "rows": [
     ["Parser, binder", "SQL text → logical plan", "05"],
     ["<b>Optimiser</b>", "Logical → physical plan by cost", "<b>08</b>"],
     ["Executor", "Runs operators over tuples", "06, 07"],
     ["<b>Access methods</b>", "B+trees, hash indexes, scans", "<b>03, 04</b>"],
     ["<b>Buffer pool</b>", "Memory, and what stays in it", "<b>02</b>"],
     ["Transactions", "Concurrency and isolation", "09, 10"],
     ["<b>Recovery</b>", "Logging, and surviving a crash", "<b>11</b>"],
     ["Disk manager", "Pages, files, and the hardware", "02"],
   ],
   "note": "Keep this table visible all semester. Students lose track of "
           "which layer they are in."},

  {"t": "callout", "title": "Read the architecture paper in week one",
   "kind": "A specific recommendation",
   "body": ["Hellerstein, Stonebraker, and Hamilton's <i>Architecture of a "
            "Database System</i> is about a hundred pages and free.",
            "<b>It is the map.</b> It explains how the components fit "
            "together before you understand any of them individually.",
            "<b>Read it now and again at the end of the course.</b> The "
            "second reading is a different document.",
            "This is unusually good advice for a survey paper, and it is "
            "why it appears in the required materials rather than as a "
            "module resource."]},

  {"t": "section", "label": "Part 4", "title": "What varies",
   "blurb": "Not every database makes the same choices."},

  {"t": "table", "kicker": "Design space", "title": "The axes systems differ on",
   "header": ["Axis", "Options", "Example"],
   "widths": [2.9, 4.4, 4.8],
   "rows": [
     ["Workload", "OLTP vs OLAP", "<b>Postgres vs Snowflake</b>"],
     ["<b>Layout</b>", "<b>Row vs column store</b>", "<b>MySQL vs DuckDB</b>"],
     ["Storage", "Disk-oriented vs in-memory", "Postgres vs Redis"],
     ["Index", "B+tree vs LSM tree", "<b>Postgres vs RocksDB</b>"],
     ["Concurrency", "Locking vs MVCC", "DB2 vs Postgres"],
     ["Scale", "Single node vs distributed", "SQLite vs Spanner"],
   ],
   "footnote": "<b>No option is universally right.</b> Each is correct for "
               "a workload, and the course covers both sides of every row.",
   "note": "This table also serves as a preview — every row is a later "
           "module."},

  {"t": "callout", "title": "Know when not to use a database",
   "kind": "An honest caveat",
   "body": ["<b>A file is fine</b> for configuration, logs, and anything "
            "one process writes and no one queries.",
            "<b>SQLite is fine</b> for an enormous range of applications, "
            "and it is the most widely deployed database in the world by "
            "several orders of magnitude.",
            "<b>A distributed database is rarely necessary.</b> A single "
            "machine with a modern NVMe drive handles workloads that "
            "required a cluster fifteen years ago.",
            "<b>The reflex to distribute is usually wrong</b>, and "
            "Module 13 makes the case precisely."]},
 ],
 "takeaways": [
   "Files fail on structure, concurrency, atomicity, querying, and scale "
   "— a DBMS exists because those failures compound.",
   "The organising question is: how do you make a machine that loses power "
   "behave as though it did not? Most of the architecture descends from it.",
   "Codd's contribution was data independence — separating what you "
   "want from how to get it — not tables.",
   "Physical independence is why query optimisation exists and why adding an "
   "index speeds up programs without changing them.",
   "The layers are parser, optimiser, executor, access methods, buffer pool, "
   "transactions, recovery, disk manager. Know which one you are in.",
   "Row versus column, B+tree versus LSM, locking versus MVCC — none "
   "is universally right, and the course covers both sides of each.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why not just use files?"),
  ("p", "The honest way to motivate a database is to start with files and "
        "watch the requirements accumulate until you have rebuilt one "
        "badly."),
  ("table", ["Problem", "What goes wrong"],
   [["<b>No structure</b>",
     "Every program that touches the file must agree on its format, and "
     "that agreement lives nowhere except in the programs. Changing the "
     "format means finding and changing all of them."],
    ["<b>No concurrent access</b>",
     "Two processes writing simultaneously interleave their writes and "
     "corrupt the file. A reader sees a record that is half old and half "
     "new. Neither is detectable after the fact."],
    ["<b>No atomicity</b>",
     "An update that touches three records can be interrupted after two. "
     "The file is now in a state no program was written to expect, and "
     "nothing records which operation was in flight."],
    ["<b>No query capability</b>",
     "Every new question requires new code, and every access path is "
     "hand-written. Finding records by a field nobody anticipated means a "
     "full scan or a new hand-built index."],
    ["<b>No scale beyond memory</b>",
     "Sorting or joining data larger than RAM is a substantial project in "
     "its own right (Module 06)."]],
   [0.23, 0.77]),
  ("callout", "The organising question of this course",
   ["<b>How do you make a machine that loses power behave as though it did "
    "not?</b>",
    "Nearly every structural decision in a database descends from that "
    "question, and the chain is worth holding in view:",
    "<b>Durability requires a log</b>, because you cannot update data in "
    "place and survive a crash halfway (Module 11). <b>The log's cost "
    "requires a buffer pool</b>, because writing every change to disk "
    "immediately is unaffordable (Module 02). <b>Concurrent access to the "
    "buffer pool requires latching</b> (Module 04). <b>The cost of locking "
    "requires multi-version concurrency control</b> (Module 10).",
    "<b>Each module adds one link.</b> The architecture stops looking like "
    "an arbitrary pile of components once you see it as a sequence of "
    "forced moves from a single requirement."]),

  ("h1", "2 &nbsp; Data independence"),
  ("callout", "Codd's contribution was independence, not tables",
   ["The relational model is usually described as 'data in tables', which "
    "misses what was actually new. Tables were not the point.",
    "<b>Before 1970, programs navigated data structures explicitly:</b> "
    "follow this pointer, traverse this chain, read the next record in this "
    "linked list. The access path was written into the application, in the "
    "application's own code.",
    "<b>So changing the physical organisation meant rewriting every "
    "program</b> that touched the data. Adding an index, reordering records, "
    "or splitting a file was a project across the whole codebase.",
    "<b>Codd separated what you want from how to obtain it.</b> A query "
    "states which rows satisfy a condition, not which pointers to follow. "
    "The system chooses the access path, at query time, from whatever "
    "structures currently exist.",
    "<b>This is the entire reason query optimisation exists</b> (Module 08). "
    "It is also why a database administrator can add an index and make every "
    "existing application faster without any of them being modified or even "
    "recompiled — which is a remarkable property and easy to take for "
    "granted."]),
  ("table", ["Level", "Describes", "Independence it provides"],
   [["<b>Physical schema</b>", "Files, pages, record layout, indexes, "
     "compression.", "—"],
    ["<b>Logical schema</b>", "Tables, columns, types, constraints, "
     "relationships.",
     "<b>Physical data independence:</b> the storage layout can be "
     "reorganised entirely without changing any query. <b>This is the one "
     "that was genuinely achieved</b>, and it is the foundation of the "
     "whole field."],
    ["<b>External schema (views)</b>",
     "What a particular application or user is shown.",
     "<b>Logical data independence:</b> the logical schema can change "
     "without breaking applications. Achieved only partially — views "
     "can hide added columns and renamings, and cannot hide a genuine "
     "restructuring."]],
   [0.20, 0.33, 0.47]),

  ("break",),
  ("h1", "3 &nbsp; The architecture"),
  ("table", ["Layer", "Responsibility", "Covered in"],
   [["<b>Parser and binder</b>",
     "SQL text to a validated logical plan: syntax, name resolution, type "
     "checking.", "Module 05"],
    ["<b>Optimiser</b>",
     "<b>Logical plan to physical plan</b>, choosing join order, join "
     "algorithms, and access paths by estimated cost.",
     "<b>Module 08</b>"],
    ["<b>Executor</b>",
     "Runs the physical plan: operators producing and consuming tuples.",
     "Modules 06, 07"],
    ["<b>Access methods</b>",
     "B+trees, hash indexes, sequential scans — the ways data can be "
     "reached.", "Modules 03, 04"],
    ["<b>Buffer pool</b>",
     "<b>Which pages are in memory and which are evicted.</b> The boundary "
     "between the database and the disk.", "<b>Module 02</b>"],
    ["<b>Transaction manager</b>",
     "Concurrency control and isolation.", "Modules 09, 10"],
    ["<b>Recovery manager</b>",
     "<b>Logging, checkpointing, and surviving a crash.</b>",
     "<b>Module 11</b>"],
    ["<b>Disk manager</b>",
     "Pages, files, and the storage hardware.", "Module 02"]],
   [0.20, 0.57, 0.23]),
  ("callout", "Read the architecture paper in week one",
   ["Hellerstein, Stonebraker and Hamilton's <i>Architecture of a Database "
    "System</i> is about a hundred pages, free, and the best overview of "
    "how these components relate.",
    "<b>Read it before you understand any of the pieces.</b> It is a map, "
    "and a map is most useful before you are lost.",
    "<b>Then read it again at the end of the course.</b> It will be a "
    "noticeably different document, because every sentence that was a bare "
    "assertion the first time will have an implementation behind it.",
    "This is unusually specific advice for a survey paper, which is why it "
    "is in the required materials rather than buried in a module's resource "
    "list."]),

  ("h1", "4 &nbsp; The design space"),
  ("table", ["Axis", "The choice", "Trade"],
   [["<b>Workload</b>", "OLTP (many small transactions) versus OLAP (few "
     "large analytical queries).",
     "Determines essentially every other choice on this list. Postgres "
     "versus Snowflake."],
    ["<b>Layout</b>", "<b>Row store versus column store.</b>",
     "Rows for reading whole records; columns for scanning one attribute "
     "across millions of records (Module 12). MySQL versus DuckDB."],
    ["<b>Storage</b>", "Disk-oriented versus in-memory.",
     "In-memory systems eliminate the buffer pool and change the cost model "
     "entirely. Postgres versus Redis or VoltDB."],
    ["<b>Index</b>", "<b>B+tree versus LSM tree.</b>",
     "B+trees favour reads, LSM trees favour writes (Module 04). Postgres "
     "versus RocksDB."],
    ["<b>Concurrency</b>", "Locking versus multi-version.",
     "Locking blocks readers against writers; MVCC does not, at the cost of "
     "storing old versions (Modules 09, 10)."],
    ["<b>Scale</b>", "Single node versus distributed.",
     "Distribution buys capacity and costs correctness guarantees, "
     "latency, and operational complexity (Module 13)."]],
   [0.14, 0.33, 0.53]),
  ("callout", "Know when not to use a database",
   ["<b>A plain file is entirely appropriate</b> for configuration, for "
    "append-only logs, and for anything that one process writes and nobody "
    "queries. Reaching for a database there adds a dependency and solves "
    "nothing.",
    "<b>SQLite is appropriate for an enormous range of applications.</b> It "
    "is an embedded library rather than a server, it implements most of this "
    "course in about 150,000 lines, and it is by a very wide margin the most "
    "widely deployed database in the world — it is in every phone, "
    "every browser, and most applications.",
    "<b>A distributed database is rarely necessary.</b> A single machine "
    "with a modern NVMe drive and a few hundred gigabytes of RAM handles "
    "workloads that genuinely required a cluster fifteen years ago, and it "
    "does so without giving up transactions, joins, or straightforward "
    "debugging.",
    "<b>The reflex to distribute is usually wrong</b>, and it is expensive "
    "in ways that are not obvious until you are committed. Module 13 makes "
    "the case precisely, with the trade-offs stated rather than gestured "
    "at."]),
 ],
 "resources": [
   ("CMU 15-445 &mdash; Lecture 1, Course Introduction and Relational Model",
    "https://15445.courses.cs.cmu.edu/",
    "Pavlo's opening lecture covers &sect;1 and &sect;2 with more history "
    "and more jokes. Watch it before reading these notes."),
   ("Hellerstein, Stonebraker & Hamilton &mdash; Architecture of a Database "
    "System (free)",
    "https://dsf.berkeley.edu/papers/fntdb07-architecture.pdf",
    "The map of &sect;3. Read it this week."),
   ("Codd &mdash; A Relational Model of Data for Large Shared Data Banks "
    "(1970, free)",
    "https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf",
    "The original paper. Short, and the data independence argument of "
    "&sect;2 is clearer in the original than in most retellings."),
   ("The Red Book &mdash; editorial introduction",
    "https://www.redbook.io/",
    "Stonebraker and Hellerstein's commentary on what has actually mattered "
    "in fifty years of the field. Opinionated and worth reading."),
 ],
 "exercises": [
   "Write a program that stores records in a flat file and supports lookup "
   "by key. Then add concurrent writers and demonstrate corruption.",
   "Add a crash point to the same program — kill it mid-update — "
   "and show that the file is left in an inconsistent state.",
   "Install SQLite and PostgreSQL. Create the same schema in both and "
   "compare what <code>EXPLAIN</code> tells you about the same query.",
   "Take a query against a table with no index, measure it, add an index, "
   "and measure again. Confirm that the query text did not change — "
   "this is physical data independence, demonstrated.",
   "Read the architecture paper and draw the layer diagram of &sect;3 from "
   "memory. Identify which layer each of this course's thirteen modules "
   "belongs to.",
   "For three systems you have used or heard of, place each on all six axes "
   "of &sect;4 and justify each placement.",
   "Find a project you know that uses a distributed database. Estimate "
   "whether a single machine would have sufficed, and state the numbers you "
   "based it on.",
 ],
 "selfcheck": [
   "Give five things a filesystem does not provide that a DBMS does.",
   "State the organising question of this course and the chain of "
   "consequences from it.",
   "What was Codd's actual contribution, and why is 'data in tables' a poor "
   "summary?",
   "Define physical and logical data independence, and say which was "
   "genuinely achieved.",
   "Why does query optimisation exist at all?",
   "Name the eight layers of a DBMS from the top down.",
   "Give six axes on which database systems differ, with an example of "
   "each.",
   "Give three situations where a full DBMS is the wrong choice.",
 ],
},

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Storage and the Buffer Pool",
 "subtitle": "Pages, and deciding what stays in memory.",
 "question": "How does a database decide what to keep in RAM?",
 "outcomes": [
     "Explain why databases are organised in fixed-size pages.",
     "Design a slotted page layout for variable-length records.",
     "Implement a buffer pool with pin counts and dirty tracking.",
     "Compare replacement policies and explain why LRU fails on scans.",
     "Explain why a DBMS bypasses the OS page cache.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Pages",
   "blurb": "The unit everything is built on."},

  {"t": "callout", "title": "The storage hierarchy dictates the design",
   "kind": "The constraint behind everything",
   "body": ["<b>Random read:</b> RAM ~100 ns. NVMe SSD ~100 μs. Spinning "
            "disk ~10 ms.",
            "<b>That is 1,000× and 100,000×.</b> No algorithm overcomes a "
            "five-order-of-magnitude gap; you design around it.",
            "<b>And sequential beats random</b> by 10–100× even on SSDs, "
            "because of prefetching and queue depth.",
            "<b>So: read in large fixed-size blocks, keep what you can in "
            "memory, and prefer sequential access.</b> Every structure in "
            "this course follows from those three."]},

  {"t": "table", "kicker": "Pages", "title": "Why fixed-size pages",
   "header": ["Reason", "Detail"],
   "widths": [3.4, 8.7],
   "rows": [
     ["Matches the hardware", "Disks transfer blocks, not bytes"],
     ["<b>Simple allocation</b>", "<b>No fragmentation of the page file</b>"],
     ["Addressable", "A page ID is an offset; no lookup table needed"],
     ["<b>Unit of I/O and caching</b>", "<b>The buffer pool deals in pages</b>"],
     ["Unit of recovery", "Log records reference pages (Module 11)"],
   ],
   "footnote": "4 KB to 16 KB is typical. Larger pages read more useful "
               "data per seek and waste more of it.",
   "note": "The page size trade is a recurring theme — bigger helps "
           "scans, hurts point lookups."},

  {"t": "code", "kicker": "Layout", "title": "The slotted page",
   "lang": "text", "code": """
 +--------------------------------------------------------------+
 | HEADER | slot0 | slot1 | slot2 | -->        free space    <-- |
 +--------------------------------------------------------------+
 |                                     | rec2 |  rec1  | rec0    |
 +--------------------------------------------------------------+

 Slot array grows FORWARD from the header.
 Records grow BACKWARD from the end of the page.
 They meet in the middle; the page is full when they touch.

 Each slot: (offset, length).  A record is addressed as (page, slot).

 WHY: a record can be moved within the page -- to compact free
 space -- WITHOUT changing its (page, slot) identity. So indexes
 pointing at it do not need updating. That indirection is the
 entire point of the design.
""",
   "caption": "The slot array is a level of indirection that makes records "
              "movable without invalidating every index that references "
              "them.",
   "note": "The movability argument is the thing to land. Without it the "
           "design looks needlessly complicated."},

  {"t": "bullets", "kicker": "Records", "title": "Complications the layout must handle",
   "items": [
     "<b>Variable-length fields.</b> Store fixed-length fields first, then "
     "offsets to the variable ones.",
     "",
     "<b>NULLs.</b> A bitmap in the record header; storing a sentinel value "
     "is wrong and eventually bites.",
     "",
     "<b>Records larger than a page.</b> Overflow pages, or out-of-line "
     "storage — Postgres calls it TOAST.",
     "",
     "<b>Updates that grow a record.</b> Either compact the page, or move "
     "the record and leave a forwarding pointer. Both are used.",
     "",
     "<b>Deletes.</b> Mark the slot free; actual reclamation is deferred "
     "(Module 10's garbage problem).",
   ],
   "note": "Forwarding pointers accumulate and degrade over time — this is "
           "why tables need periodic reorganisation."},

  {"t": "section", "label": "Part 2", "title": "The buffer pool",
   "blurb": "Memory, and who gets it."},

  {"t": "code", "kicker": "Buffer pool", "title": "The core data structure",
   "lang": "cpp", "code": """
struct Frame {
    page_id_t page_id;
    char      data[PAGE_SIZE];
    int       pin_count;   // > 0 means SOMEONE IS USING IT. Never evict.
    bool      is_dirty;    // modified since read; must be written back
};

Page* BufferPool::fetch(page_id_t id) {
    if (auto it = page_table.find(id); it != page_table.end()) {
        frames[it->second].pin_count++;       // hit
        replacer.pin(it->second);
        return &frames[it->second];
    }
    frame_id_t f;
    if (!free_list.empty())      f = pop_free();
    else if (!replacer.evict(&f)) return nullptr;   // ALL PINNED: fail
    else {
        if (frames[f].is_dirty) disk.write(frames[f].page_id, frames[f].data);
        page_table.erase(frames[f].page_id);
    }
    disk.read(id, frames[f].data);
    frames[f] = {id, ..., /*pin*/ 1, /*dirty*/ false};
    page_table[id] = f;
    return &frames[f];
}
""",
   "caption": "The pin count is the critical invariant: a pinned page is in "
              "use and must not move or be written out from under its "
              "user.",
   "note": "Returning nullptr when everything is pinned is correct and "
           "students always forget it. It is a real failure mode."},

  {"t": "callout", "title": "Pin counts are the invariant that matters",
   "kind": "Get this wrong and nothing works",
   "body": ["<b>A pinned page is in use.</b> Evicting it would hand a caller "
            "a pointer to a different page's data — which corrupts "
            "silently.",
            "<b>Every fetch must be matched by an unpin.</b> A leaked pin "
            "removes a frame from circulation permanently; enough leaks and "
            "the pool deadlocks with nothing evictable.",
            "<b>Use RAII or an equivalent.</b> Manual unpinning on every "
            "path, including error paths, is not reliably achievable.",
            "<b>And handle the all-pinned case explicitly</b> — it is a "
            "real condition, not an impossible one."]},

  {"t": "section", "label": "Part 3", "title": "Replacement",
   "blurb": "Choosing the victim."},

  {"t": "table", "kicker": "Policies", "title": "Replacement policies",
   "header": ["Policy", "Idea", "Weakness"],
   "widths": [2.6, 4.6, 4.9],
   "rows": [
     ["LRU", "Evict the least recently used", "<b>A single scan destroys it</b>"],
     ["<b>CLOCK</b>", "Approximate LRU with a reference bit", "<b>Cheap; nearly as good</b>"],
     ["<b>LRU-K</b>", "Use the K-th most recent access", "<b>Resists scan pollution</b>"],
     ["2Q / ARC", "Separate queues for once and twice accessed", "Adaptive; more state"],
     ["MRU", "Evict the <i>most</i> recent", "Correct for a sequential scan"],
   ],
   "footnote": "LRU-2 is the usual answer: one access is not evidence of "
               "value; two is.",
   "note": "MRU being right for scans surprises people and is a good way to "
           "show policy must match access pattern."},

  {"t": "callout", "title": "Sequential flooding: one scan evicts everything",
   "kind": "Why plain LRU is inadequate",
   "body": ["A full table scan touches every page exactly once, in order.",
            "<b>LRU dutifully caches all of them</b>, evicting the hot "
            "working set that thousands of queries were using — in "
            "exchange for pages that will never be touched again.",
            "<b>Performance collapses for every other query</b>, and "
            "recovers only slowly as the working set is read back in.",
            "<b>LRU-K fixes it</b> by requiring K accesses before a page is "
            "considered valuable. A scan touches each page once, so nothing "
            "it reads displaces anything."]},

  {"t": "section", "label": "Part 4", "title": "Fighting the OS",
   "blurb": "Why databases manage their own memory."},

  {"t": "bullets", "kicker": "Why not mmap", "title": "Why a DBMS does not just use mmap",
   "items": [
     "<b>No control over eviction.</b> The OS does not know which pages are "
     "hot <i>for your workload</i>, and it does not know about pin counts.",
     "",
     "<b>No control over write ordering</b> — and the WAL protocol "
     "(Module 11) <i>requires</i> specific ordering. This alone is "
     "disqualifying.",
     "",
     "<b>Unpredictable stalls.</b> A page fault blocks the thread in the "
     "kernel with no way to do anything else.",
     "",
     "<b>Transparent huge pages and readahead</b> interfere in ways you "
     "cannot disable per-file.",
     "",
     "<b>Double buffering</b> if the OS cache is also active, wasting half "
     "your memory.",
   ],
   "footnote": "'Are You Sure You Want to Use MMAP in Your DBMS?' is a real "
               "paper and the title is the abstract.",
   "note": "The write-ordering point is the decisive one. Everything else "
           "is an inconvenience; that is a correctness failure."},

  {"t": "callout", "title": "O_DIRECT and the fsync problem",
   "kind": "Two things to know",
   "body": ["<b>O_DIRECT</b> bypasses the OS page cache entirely, so the "
            "DBMS's buffer pool is the only cache. Avoids double buffering "
            "and gives predictable behaviour.",
            "<b>fsync is how you know a write reached durable storage</b> "
            "— and it is slow, which is why the log is designed to batch "
            "them (Module 11).",
            "<b>fsync can fail, and on some systems a failed fsync marks "
            "the error as consumed</b> — a retry returns success while the "
            "data is lost.",
            "<b>This is 'fsyncgate'</b>, it affected PostgreSQL for twenty "
            "years, and the resolution was to treat an fsync failure as "
            "unrecoverable and crash. Durability is harder than it looks."]},
 ],
 "takeaways": [
   "Random reads cost 1,000–100,000&times; a memory access, and "
   "sequential beats random by 10–100&times;. Every structure in this "
   "course follows from that.",
   "Fixed-size pages match the hardware, avoid fragmentation, and serve as "
   "the unit of I/O, caching, and recovery.",
   "A slotted page puts a slot array at one end and records at the other, so "
   "records can move within a page without changing their identity.",
   "The pin count is the buffer pool's critical invariant: a pinned page is "
   "in use and must never be evicted. Use RAII.",
   "Plain LRU collapses under sequential flooding — one scan evicts the "
   "whole working set. LRU-K requires two accesses before valuing a page.",
   "A DBMS manages its own memory because mmap offers no control over write "
   "ordering, which the WAL protocol requires.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Pages"),
  ("callout", "The storage hierarchy dictates the algorithms",
   ["<b>Approximate random-access latencies:</b> registers under a "
    "nanosecond; RAM around 100 ns; NVMe SSD around 100 &micro;s; a spinning "
    "disk around 10 ms.",
    "<b>Memory to SSD is a factor of a thousand; memory to disk is a factor "
    "of a hundred thousand.</b> No clever algorithm overcomes a gap of that "
    "size — you design around it, which means the algorithm's goal is "
    "to minimise the <i>number of I/Os</i> rather than the number of "
    "operations.",
    "<b>And sequential access beats random access</b> by ten to a hundred "
    "times even on SSDs, because of prefetching, request coalescing, and "
    "queue depth. On spinning disks the ratio is far larger still.",
    "<b>Three consequences, and they explain nearly everything:</b> read in "
    "large fixed-size blocks rather than individual records; keep as much as "
    "possible in memory; and prefer sequential access patterns even at the "
    "cost of reading more data than you need. A B+tree (Module 03) is what "
    "you get when you take these seriously."]),
  ("table", ["Why fixed-size pages", "Detail"],
   [["<b>Matches the hardware</b>",
     "Storage devices transfer blocks, not bytes. Reading one byte and "
     "reading four kilobytes cost the same."],
    ["<b>Simple allocation</b>",
     "Uniform size means a page file never fragments — any free page "
     "can hold any page's contents."],
    ["<b>Directly addressable</b>",
     "A page ID multiplied by the page size is a file offset. No lookup "
     "table is needed to find a page."],
    ["<b>The unit of I/O and of caching</b>",
     "The buffer pool deals exclusively in pages, which keeps it simple."],
    ["<b>The unit of recovery</b>",
     "Log records reference pages and their LSNs (Module 11)."]],
   [0.26, 0.74]),
  ("p", "<b>4 KB to 16 KB is typical.</b> A larger page reads more useful "
        "data per seek, which helps scans, and wastes more of the transfer "
        "when only one record is wanted, which hurts point lookups. The "
        "choice therefore depends on the workload, and this trade recurs "
        "throughout the course."),
  ("h2", "1.1 &nbsp; The slotted page"),
  ("code", """+-------------------------------------------------------------+
| HEADER | slot0 | slot1 | slot2 | -->     free space      <-- |
+-------------------------------------------------------------+
|                                    | rec2 |  rec1  |  rec0   |
+-------------------------------------------------------------+

slot array grows FORWARD    records grow BACKWARD
page is full when they meet
each slot = (offset, length);  record address = (page_id, slot_no)"""),
  ("callout", "The slot array exists so records can move",
   ["The design looks needlessly indirect until you ask what happens when a "
    "record is deleted and the resulting hole must be reclaimed.",
    "<b>With a slot array, a record can be relocated anywhere within its "
    "page — to compact free space — without changing its "
    "identity.</b> Its address is (page, slot number), and only the slot's "
    "offset field changes.",
    "<b>Which means every index entry pointing at that record remains "
    "valid.</b> Without the indirection, compacting a page would require "
    "finding and updating every index entry referencing every record that "
    "moved — which would make compaction impossible in practice.",
    "<b>That indirection is the entire point of the design</b>, and it is "
    "the answer to 'why not just store records end to end'."]),
  ("table", ["Complication", "Handling"],
   [["<b>Variable-length fields</b>",
     "Store all fixed-length fields first at known offsets, then an array of "
     "offsets to the variable-length ones. A field's position is then either "
     "a constant or one indirection."],
    ["<b>NULLs</b>",
     "A bitmap in the record header. <b>Using a sentinel value instead is "
     "wrong</b> and eventually collides with a legitimate value — the "
     "classic case being a date of 1900-01-01 meaning 'unknown'."],
    ["<b>Records larger than a page</b>",
     "Overflow pages chained from the main record, or out-of-line storage "
     "for large attributes. PostgreSQL's TOAST mechanism compresses and "
     "then, if still too large, stores out of line — transparently."],
    ["<b>An update that grows a record</b>",
     "Either compact the page to make room, or move the record to another "
     "page and leave a <b>forwarding pointer</b> in the original slot. Both "
     "approaches are used; forwarding pointers accumulate over time and "
     "turn one-page lookups into two, which is a significant reason tables "
     "need periodic reorganisation."],
    ["<b>Deletes</b>",
     "Mark the slot free. Actual reclamation is deferred, and under MVCC the "
     "record cannot be removed at all until no transaction can still see it "
     "(Module 10)."]],
   [0.26, 0.74]),

  ("h1", "2 &nbsp; The buffer pool"),
  ("p", "The buffer pool is the boundary between the database and the disk. "
        "It holds a fixed number of page-sized frames, a mapping from page "
        "IDs to frames, and the policy for deciding which page to evict when "
        "a frame is needed."),
  ("code", """struct Frame {
    page_id_t page_id;
    char      data[PAGE_SIZE];
    int       pin_count;    // > 0: in use, NEVER evict
    bool      is_dirty;     // modified; must be written before eviction
};"""),
  ("callout", "Pin counts are the invariant that matters",
   ["<b>A pinned page is one that some caller currently holds a pointer "
    "into.</b> Evicting it and loading a different page into that frame "
    "would leave the caller reading another page's bytes — and the "
    "corruption is silent, because the data looks like perfectly valid data "
    "of the wrong page.",
    "<b>Every fetch must be matched by exactly one unpin.</b> A leaked pin "
    "permanently removes a frame from circulation; enough leaks and the pool "
    "has nothing evictable and every subsequent fetch fails.",
    "<b>Use RAII, or your language's equivalent.</b> Unpinning manually on "
    "every control path — including every error path and every early "
    "return — is not something anyone achieves reliably, and the bug is "
    "invisible until the pool is under pressure.",
    "<b>Handle the all-pinned case explicitly.</b> Returning a failure when "
    "every frame is pinned is correct behaviour, not an impossible "
    "condition, and omitting it turns a recoverable situation into a crash "
    "or a corruption."]),

  ("break",),
  ("h1", "3 &nbsp; Replacement policies"),
  ("table", ["Policy", "Mechanism", "Assessment"],
   [["<b>LRU</b>", "Evict the page not accessed for longest.",
     "Intuitive and <b>fails badly on sequential scans</b> — see "
     "below."],
    ["<b>CLOCK</b>",
     "Approximate LRU: frames in a circular buffer, each with a reference "
     "bit. Sweep a hand, clear set bits, evict the first unset one.",
     "<b>Much cheaper than true LRU</b> (no list manipulation on every "
     "access) and nearly as effective. Very widely used."],
    ["<b>LRU-K</b>",
     "Track the time of the K-th most recent access, and evict by that "
     "rather than by the most recent.",
     "<b>Resists scan pollution</b>, because a page accessed only once has "
     "no K-th access and is evicted first. <b>LRU-2 is the usual choice:</b> "
     "one access is not evidence of value; two is."],
    ["<b>2Q, ARC</b>",
     "Separate queues for pages seen once and pages seen repeatedly, with "
     "adaptive sizing.",
     "Effective, with more bookkeeping. ARC's patent history pushed many "
     "systems toward alternatives."],
    ["<b>MRU</b>", "Evict the <i>most</i> recently used page.",
     "Sounds perverse and is <b>exactly right for a sequential scan</b>: "
     "the page just read will not be needed again, while older pages might. "
     "A good illustration that the correct policy depends on the access "
     "pattern, which is why some systems let the executor hint."]],
   [0.14, 0.40, 0.46]),
  ("callout", "Sequential flooding",
   ["A full table scan reads every page of a large table exactly once, in "
    "order.",
    "<b>LRU dutifully caches all of them.</b> Each newly read page is the "
    "most recently used, so it is the last candidate for eviction — "
    "and the pages being evicted to make room are the hot working set that "
    "thousands of other queries depend on.",
    "<b>The result is that one analytical query destroys the cache for "
    "every transactional query on the system</b>, in exchange for caching "
    "pages that will never be read again. Performance collapses, and "
    "recovers only slowly as the working set is faulted back in.",
    "<b>LRU-K fixes it directly.</b> A page needs K accesses before it is "
    "considered valuable; a scan touches each page once, so the scanned "
    "pages are the first evicted and the working set is untouched. This is "
    "the main reason real systems do not use plain LRU."]),

  ("h1", "4 &nbsp; Why not let the operating system do it?"),
  ("p", "The operating system already has a page cache and "
        "<code>mmap</code> already maps files into memory. The question of "
        "why a database reimplements all of this is a reasonable one, and "
        "the answer is instructive."),
  ("table", ["Problem with mmap", "Consequence"],
   [["<b>No control over eviction</b>",
     "The OS does not know which pages matter for this workload, and it "
     "knows nothing about pin counts. It can evict a page the DBMS is "
     "actively using."],
    ["<b>No control over write ordering</b>",
     "<b>Decisive.</b> The write-ahead logging protocol (Module 11) requires "
     "that specific writes reach durable storage before specific others. "
     "With mmap, the OS writes dirty pages whenever it chooses, in whatever "
     "order. <b>This is not an inconvenience — it makes durability "
     "unachievable.</b>"],
    ["<b>Unpredictable stalls</b>",
     "A page fault blocks the faulting thread inside the kernel. The DBMS "
     "cannot schedule other work, cannot issue the I/O asynchronously, and "
     "cannot even tell that it is waiting."],
    ["<b>Interference from OS features</b>",
     "Transparent huge pages, readahead heuristics, and NUMA migration all "
     "act on mapped memory in ways that cannot be disabled per file."],
    ["<b>Double buffering</b>",
     "If the DBMS has its own cache <i>and</i> the OS page cache is active, "
     "hot pages occupy memory twice."]],
   [0.25, 0.75]),
  ("p", "Crotty, Leis and Pavlo's paper <i>Are You Sure You Want to Use "
        "MMAP in Your DBMS?</i> makes this case in full; the title is "
        "effectively the abstract. Systems that tried it — MongoDB's "
        "original storage engine, among others — moved away."),
  ("callout", "O_DIRECT, fsync, and a twenty-year bug",
   ["<b>O_DIRECT</b> bypasses the OS page cache, so the DBMS's buffer pool "
    "is the only cache in the system. This eliminates double buffering and "
    "makes behaviour predictable, at the cost of losing the OS's readahead "
    "— which the DBMS must then implement itself, and can do better, "
    "because it knows what it is about to read.",
    "<b>fsync is how a program learns that a write has reached durable "
    "storage.</b> It is expensive, which is why the log batches writes and "
    "amortises the cost across transactions (Module 11).",
    "<b>And fsync can fail.</b> Worse: on Linux and several other systems, "
    "a failed fsync historically marked the error as <i>consumed</i>, so a "
    "subsequent retry returned success while the data was gone. A program "
    "that retried on failure would conclude it had succeeded.",
    "<b>This is 'fsyncgate'.</b> It affected PostgreSQL for roughly twenty "
    "years before being diagnosed in 2018, and the eventual resolution was "
    "to treat any fsync failure as unrecoverable and deliberately crash, so "
    "that recovery runs from the log. <b>Durability is substantially harder "
    "than it appears</b>, and this is the clearest illustration of why."]),
 ],
 "resources": [
   ("CMU 15-445 &mdash; Lectures 3–6, Storage and Buffer Pools",
    "https://15445.courses.cs.cmu.edu/",
    "Page layout, slotted pages, and the buffer pool with replacement "
    "policies. The primary source for this module."),
   ("Crotty, Leis & Pavlo &mdash; Are You Sure You Want to Use MMAP in Your "
    "DBMS? (free)",
    "https://db.cs.cmu.edu/mmap-cidr2022/",
    "The &sect;4 argument in full, with measurements."),
   ("O'Neil, O'Neil & Weikum &mdash; The LRU-K Page Replacement Algorithm "
    "(free)",
    "https://www.cs.cmu.edu/~christos/courses/721-resources/p297-o_neil.pdf",
    "The original LRU-K paper, including the sequential flooding analysis."),
   ("PostgreSQL fsync reliability discussion ('fsyncgate')",
    "https://wiki.postgresql.org/wiki/Fsync_Errors",
    "The &sect;4 story, documented by the people who found it. Worth reading "
    "as a case study in how durability assumptions fail."),
   ("Database Internals &mdash; chapters on storage engines",
    "https://www.databass.dev/",
    "Page layouts and buffer management from a different angle."),
 ],
 "exercises": [
   "Measure the latency of random and sequential reads on your own machine, "
   "at several block sizes. Plot it and compare against the figures in "
   "&sect;1.",
   "Implement a slotted page supporting insert, delete, and retrieval by "
   "slot number. Verify that compaction does not change any record's "
   "address.",
   "Add variable-length records and a NULL bitmap. Store a record "
   "containing a legitimate value that a sentinel scheme would have "
   "misread.",
   "Implement a buffer pool with pin counts and dirty tracking. Write a test "
   "that fails if a pin is leaked.",
   "Implement LRU and CLOCK replacement. Compare hit rates on a Zipfian "
   "workload at several pool sizes.",
   "<b>Demonstrate sequential flooding:</b> run a hot working set, then "
   "issue one full scan, and plot the hit rate before, during, and after.",
   "Implement LRU-2 and repeat. The hit rate should barely move during the "
   "scan.",
   "Produce the Project 1 hit-rate-against-pool-size plot and explain the "
   "shape of the curve — in particular where it flattens and why.",
   "Measure the cost of <code>fsync</code> on your machine, and the "
   "throughput difference between one fsync per write and one per hundred "
   "writes.",
 ],
 "selfcheck": [
   "Give the approximate latency of a random read from RAM, SSD, and disk, "
   "and the three design consequences.",
   "Give five reasons databases use fixed-size pages.",
   "Draw the slotted page layout and explain why the slot array exists.",
   "How are variable-length fields, NULLs, and oversized records handled?",
   "What is a pin count, what breaks without it, and why use RAII?",
   "Compare five replacement policies.",
   "Explain sequential flooding and how LRU-K prevents it.",
   "Give the decisive reason a DBMS does not use mmap.",
   "What was fsyncgate and what was the resolution?",
 ],
},

]

# --- additional module batches ----------------------------------------------
for _b in ("c608_b2", "c608_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
