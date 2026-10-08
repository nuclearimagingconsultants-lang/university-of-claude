# -*- coding: utf-8 -*-
"""CSCE 608 — Modules 03-07."""

MODULES = [

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "B+Trees",
 "subtitle": "The data structure the storage hierarchy forced into "
             "existence.",
 "question": "Why is every database index the same shape?",
 "outcomes": [
     "Explain why a B+tree rather than a binary tree.",
     "Implement insert with splits and delete with merges.",
     "Compute tree height from fanout and explain what it costs.",
     "Distinguish clustered from non-clustered indexes.",
     "Explain when an index helps and when it does not.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why not a binary tree",
   "blurb": "The answer is entirely about I/O."},

  {"t": "callout", "title": "Count I/Os, not comparisons",
   "kind": "The design driver",
   "body": ["A balanced binary tree over a million keys is about 20 levels "
            "deep. <b>Each level is a pointer chase to an arbitrary "
            "address</b> — a random read.",
            "<b>Twenty random reads at 100 μs is 2 ms</b> for one lookup. "
            "Unusable.",
            "<b>A page holds hundreds of keys</b>, so a node can have "
            "hundreds of children. With fanout 400, a million keys fit in "
            "<b>three levels</b>.",
            "<b>Three I/Os instead of twenty</b> — and the top two levels "
            "stay cached, so it is effectively one. The shape is forced by "
            "the hardware."]},

  {"t": "eq", "kicker": "Height", "title": "Fanout determines everything",
   "eqs": [
     ("height  =  ⌈log_f(N)⌉",
      "f is the fanout — how many children fit in a page. N is the key "
      "count."),
     ("f ≈ PAGE_SIZE / (key_size + pointer_size)",
      "A 16 KB page with 8-byte keys and 8-byte pointers gives f ≈ 1000."),
     ("10⁹ keys, f = 1000  ⟹  height 3",
      "A billion keys in three levels. Levels 0 and 1 are a few megabytes "
      "and stay in the buffer pool permanently."),
   ],
   "caption": "So a lookup in a billion-row table is usually one disk read. "
              "This is why B+trees are everywhere.",
   "note": "Have them compute this. The numbers are more persuasive than "
           "the argument."},

  {"t": "two", "kicker": "Variants", "title": "B-tree and B+tree",
   "lh": "B-tree",
   "l": ["Keys <b>and values</b> in every node.",
         "A lookup can terminate at an internal node.",
         ("Slightly fewer I/Os for a lucky point lookup.", 1),
         "<b>Lower fanout</b> — values take space in internal nodes.",
         "<b>Range scans are awkward</b> — must traverse the tree."],
   "rh": "B+tree",
   "r": ["Internal nodes hold <b>only keys</b>; all values in leaves.",
         "Every lookup goes to a leaf.",
         ("Predictable cost: always the height.", 1),
         "<b>Higher fanout</b>, so a shallower tree.",
         "<b>Leaves are linked</b> — a range scan is a sequential walk."],
   "note": "The linked leaves are the decisive advantage. Range scans are "
           "most of what a database does."},

  {"t": "section", "label": "Part 2", "title": "Operations",
   "blurb": "Splits going up, merges coming back."},

  {"t": "code", "kicker": "Insert", "title": "Insert, and splitting upward",
   "lang": "text", "code": """
INSERT(key, value):
  leaf = descend from root, choosing child by key range
  if leaf has room:
      insert in sorted position; done
  else:
      SPLIT:
        allocate a new leaf
        move the upper half of the entries into it
        link it into the leaf chain          <-- B+tree specific
        COPY the separator key up to the parent
        (B-tree would MOVE it; B+tree COPIES, because the
         key must remain in the leaf where its value lives)

      if the parent is now full, split the parent too,
      recursively, up to the root.

      If the ROOT splits, allocate a new root.
      *** This is the only way the tree grows taller. ***
""",
   "caption": "The tree grows at the root, not the leaves, which is why it "
              "stays perfectly balanced with no rebalancing logic.",
   "note": "Copy-up versus push-up is a classic exam question and a classic "
           "bug. Make the reason explicit."},

  {"t": "callout", "title": "Deletion is where implementations cheat",
   "kind": "An honest note",
   "body": ["<b>Textbook deletion</b> merges a node with a sibling when "
            "occupancy falls below half, or redistributes entries if the "
            "sibling is full enough.",
            "<b>Most real implementations do not.</b> They remove the entry "
            "and leave the node underfull.",
            "<b>Why:</b> merging is complex, requires locking more nodes "
            "(Module 04), and deletions are usually followed by insertions "
            "that refill the space anyway.",
            "<b>The cost is gradual degradation.</b> A tree subjected to "
            "many deletes becomes sparse and taller than necessary, which is "
            "why <code>REINDEX</code> and <code>VACUUM</code> exist."]},

  {"t": "bullets", "kicker": "Details", "title": "What real implementations add",
   "items": [
     "<b>Prefix compression.</b> Keys in a node share prefixes; store the "
     "prefix once. Raises fanout substantially on string keys.",
     "",
     "<b>Suffix truncation.</b> A separator key need only distinguish — "
     "it can be truncated to the shortest sufficient prefix.",
     "",
     "<b>Bulk loading.</b> Sort first, then build bottom-up. Far faster "
     "than repeated insertion, and produces a densely packed tree.",
     "",
     "<b>Variable-length keys</b> make 'half full' ambiguous and "
     "complicate splits considerably.",
     "",
     "<b>Duplicate keys</b> — either a list per key, or append the record "
     "ID to make keys unique. The second is simpler.",
   ],
   "footnote": "Prefix compression on a URL or name column can double the "
               "fanout, removing a level from the tree."},

  {"t": "section", "label": "Part 3", "title": "Using indexes",
   "blurb": "Clustered, covering, and when none of it helps."},

  {"t": "two", "kicker": "Clustering", "title": "Clustered and non-clustered",
   "lh": "Clustered",
   "l": ["<b>The table IS the index</b> — rows stored in leaves, in key "
         "order.",
         "<b>Range scans are sequential.</b> Excellent.",
         "<b>One per table</b>, necessarily.",
         ("Inserts in random key order fragment it.", 1),
         "MySQL InnoDB; SQL Server by default."],
   "rh": "Non-clustered",
   "r": ["Leaves hold <b>pointers</b> to rows stored elsewhere.",
         "<b>Range scan needs a random read per row.</b>",
         "<b>Many per table.</b>",
         ("Row location can change, needing indirection.", 1),
         "PostgreSQL's only kind."],
   "note": "PostgreSQL having no clustered index is a real and frequently "
           "underestimated difference."},

  {"t": "callout", "title": "A covering index avoids touching the table",
   "kind": "The biggest practical win",
   "body": ["If the index contains <i>every</i> column the query needs, "
            "<b>the base table is never read</b>.",
            "<b>This is an index-only scan</b>, and it can be an order of "
            "magnitude faster than an index scan that must fetch each row.",
            "The cost is a wider index: more space, slower writes, and lower "
            "fanout.",
            "<b>INCLUDE columns</b> let you add payload columns to a "
            "non-clustered index without making them part of the key — "
            "coverage without the key-size penalty. Supported by Postgres, "
            "SQL Server, and others."]},

  {"t": "table", "kicker": "When not", "title": "When an index does not help",
   "header": ["Situation", "Why"],
   "widths": [4.4, 7.7],
   "rows": [
     ["Query returns a large fraction of rows", "<b>A scan is cheaper than random reads</b>"],
     ["Low-cardinality column", "Few distinct values; each matches many rows"],
     ["Leading column not in the predicate", "<b>A composite index is ordered left to right</b>"],
     ["Function applied to the column", "<b>WHERE upper(x)='A' cannot use an index on x</b>"],
     ["Heavy write workload", "Every index must be updated on every write"],
   ],
   "footnote": "The crossover is often as low as 5–10% selectivity on "
               "spinning disks, higher on SSDs.",
   "note": "The leading-column rule is the one that costs people the most "
           "in practice."},

  {"t": "callout", "title": "Composite index order matters, and it is not symmetric",
   "kind": "The most common indexing mistake",
   "body": ["An index on <code>(a, b)</code> is sorted by a, then by b "
            "<i>within</i> each a.",
            "<b>It serves</b> <code>WHERE a = ?</code> and <code>WHERE a = ? "
            "AND b = ?</code>.",
            "<b>It does not serve</b> <code>WHERE b = ?</code> — the b "
            "values are scattered throughout, in as many groups as there are "
            "distinct a values.",
            "<b>So (a,b) and (b,a) are different indexes</b> and the right "
            "order depends on the queries. Equality columns first, then the "
            "range column, is the usual rule."]},
 ],
 "takeaways": [
   "B+trees exist because lookups are counted in I/Os, not comparisons; high "
   "fanout turns twenty random reads into three.",
   "Height is log_f(N) with f &asymp; page size over entry size. A billion "
   "keys at fanout 1000 is three levels, two of which stay cached.",
   "B+trees put all values in leaves and link the leaves, which raises "
   "fanout and makes range scans sequential — the decisive advantage.",
   "Splits propagate upward and the tree grows only at the root, which keeps "
   "it balanced with no rebalancing logic. Separators are copied, not moved.",
   "Most implementations skip merging on delete, accepting gradual sparsity "
   "— which is why REINDEX and VACUUM exist.",
   "A composite index on (a,b) does not serve a predicate on b alone, and a "
   "function applied to a column defeats the index on it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why not a binary tree"),
  ("callout", "The cost model is I/Os, not comparisons",
   ["A balanced binary search tree over a million keys has height about 20. "
    "In an in-memory setting that is excellent — twenty comparisons.",
    "<b>On disk, each level is a pointer chase to an arbitrary "
    "address</b>, which is a random read. Twenty random reads at 100 "
    "&micro;s each is 2 ms for a single lookup, and the comparisons "
    "themselves are free by comparison. <b>The cost model that matters is "
    "the number of I/Os.</b>",
    "<b>A page holds hundreds or thousands of keys</b>, and reading a page "
    "costs the same as reading a byte. So make each node a page, and let it "
    "have as many children as fit.",
    "<b>With fanout 400, a million keys fit in three levels.</b> Three I/Os "
    "rather than twenty — and because the root and the level below it "
    "are only a few megabytes, they stay resident in the buffer pool "
    "permanently, so a lookup is effectively <i>one</i> I/O. <b>The shape "
    "of the structure is forced by the hardware</b>, which is why every "
    "disk-based index is some variation on it."]),
  ("eq", "height = &lceil;log<sub>f</sub>(N)&rceil; &nbsp;&nbsp;&nbsp; "
         "f &asymp; PAGE_SIZE / (key_size + pointer_size)"),
  ("table", ["Page size", "Entry size", "Fanout f", "Keys at height 3"],
   [["4 KB", "16 bytes", "~250", "~1.5 &times; 10<super>7</super>"],
    ["16 KB", "16 bytes", "~1000", "<b>10<super>9</super></b>"],
    ["16 KB", "64 bytes (string keys)", "~250",
     "~1.5 &times; 10<super>7</super>"]],
   [0.17, 0.30, 0.18, 0.35]),
  ("p", "<b>A billion keys in three levels</b>, with the top two levels "
        "cached. This single calculation explains why B+trees displaced "
        "everything else for disk-resident indexing, and it is worth doing "
        "for your own page size and key type rather than taking it on "
        "trust."),
  ("table", ["", "B-tree", "B+tree"],
   [["Values stored", "In every node, internal and leaf.",
     "<b>Only in leaves.</b> Internal nodes hold keys and child pointers "
     "only."],
    ["Lookup", "May terminate early at an internal node.",
     "Always descends to a leaf. <b>Predictable cost</b>, always the "
     "height."],
    ["Fanout", "Lower — values consume space in internal nodes.",
     "<b>Higher</b>, so the tree is shallower for the same key count."],
    ["Range scan", "Awkward — requires in-order traversal back up and "
     "down the tree.",
     "<b>Leaves are linked in key order</b>, so a range scan finds the "
     "start and then walks sequentially. <b>This is the decisive "
     "advantage</b>, because range scans are a large fraction of what "
     "databases actually do."]],
   [0.13, 0.40, 0.47]),

  ("h1", "2 &nbsp; Operations"),
  ("code", """INSERT(key, value):
  leaf = descend from root, choosing child by key range
  if leaf has room: insert in sorted position; done
  else:
      allocate new leaf
      move upper half of entries into it
      link it into the leaf chain
      COPY the separator key up into the parent
      if parent now full, split it too (recursively)
      if the ROOT splits, allocate a new root  <-- the only way
                                                   the tree grows taller"""),
  ("callout", "The tree grows at the root, which is why it stays balanced",
   ["A B+tree never rebalances. There is no rotation, no colour, no "
    "rebalancing pass.",
    "<b>It stays perfectly balanced because it grows at the root rather "
    "than at the leaves.</b> Every leaf is at the same depth by "
    "construction: when a split propagates all the way up and the root "
    "itself splits, a new root is created above it and <i>every</i> path "
    "lengthens by one simultaneously.",
    "<b>Copy versus move is the detail people get wrong.</b> In a B+tree, "
    "the separator key pushed into the parent is <b>copied</b>, not moved "
    "— the key must remain in the leaf, because that is where its value "
    "lives. In a B-tree it is moved, because the value moves with it. "
    "Getting this backwards produces a tree that loses keys, and it is the "
    "classic implementation bug."]),
  ("callout", "Deletion is where real implementations cheat",
   ["<b>The textbook algorithm</b> merges a node with a sibling when its "
    "occupancy falls below half, or redistributes entries between them if "
    "the sibling has enough to spare, propagating merges upward as needed.",
    "<b>Most production implementations do not do this.</b> They remove the "
    "entry and leave the node underfull.",
    "<b>The reasons are practical:</b> merging is considerably more complex "
    "than splitting; it requires locking more nodes, which complicates "
    "concurrency (Module 04); and in most workloads deletions are followed "
    "by insertions that refill the space, so the work would be wasted.",
    "<b>The cost is gradual degradation.</b> A tree subjected to many "
    "deletions becomes sparse — more pages than the data requires, so "
    "more I/O per scan and sometimes a taller tree. <b>This is why "
    "<code>REINDEX</code> and <code>VACUUM FULL</code> exist</b>, and why "
    "they periodically need to be run on write-heavy tables."]),
  ("ul", ["<b>Prefix compression.</b> Keys within a node frequently share a "
          "prefix — URLs, names, timestamps. Storing the common prefix "
          "once per node and only the differing suffixes per entry can "
          "<b>double the fanout</b> on string keys, which removes a level "
          "from the tree.",
          "<b>Suffix truncation.</b> A separator key in an internal node "
          "only has to <i>distinguish</i> the two subtrees, not match any "
          "actual key. It can be truncated to the shortest prefix that "
          "separates them, which saves space in exactly the nodes where "
          "space buys the most.",
          "<b>Bulk loading.</b> Building a tree by repeated insertion is "
          "slow and produces a tree about 70% full. Sorting the data first "
          "and building bottom-up is far faster and produces a densely "
          "packed tree — which is what <code>CREATE INDEX</code> does.",
          "<b>Variable-length keys</b> make 'half full' ambiguous — "
          "half by entry count or half by bytes? — and complicate "
          "split-point selection.",
          "<b>Duplicate keys</b> are handled either by storing a list of "
          "record IDs per key, or by appending the record ID to the key to "
          "make every key unique. The second is simpler and is what most "
          "systems do."]),

  ("break",),
  ("h1", "3 &nbsp; Using indexes"),
  ("table", ["", "Clustered index", "Non-clustered index"],
   [["Structure", "<b>The table is the index.</b> Rows are stored in the "
     "leaves, in key order.",
     "Leaves hold keys and <b>pointers</b> to rows stored elsewhere."],
    ["Range scan", "<b>Sequential</b> — the rows are physically "
     "adjacent. Excellent.",
     "<b>One random read per row</b> to fetch it from the table. Can be "
     "slower than a full scan."],
    ["How many", "<b>One per table</b>, necessarily — rows can only "
     "be in one physical order.", "<b>As many as you like.</b>"],
    ["Insert cost", "Insertions in random key order fragment the table "
     "itself.", "The table is unaffected; only the index fragments."],
    ["Who uses it", "MySQL InnoDB (always, on the primary key); SQL Server "
     "by default.",
     "<b>PostgreSQL's only kind</b> — it has no clustered index at "
     "all, which is a real and frequently underestimated difference."]],
   [0.13, 0.42, 0.45]),
  ("callout", "A covering index avoids the table entirely",
   ["If an index contains <i>every</i> column a query references — "
    "both in the predicate and in the select list — then the query can "
    "be answered from the index alone and <b>the base table is never "
    "read</b>.",
    "<b>This is an index-only scan, and it is frequently an order of "
    "magnitude faster</b> than an index scan that must fetch each matching "
    "row, because it eliminates one random read per result row.",
    "<b>The cost is a wider index:</b> more disk space, more work on every "
    "write, and lower fanout, which can add a level to the tree.",
    "<b>INCLUDE columns are the refinement.</b> They let you add payload "
    "columns to an index without making them part of the sort key — "
    "you get coverage without paying for a wider key in every internal node. "
    "PostgreSQL, SQL Server, and others support them, and they are "
    "underused."]),
  ("table", ["An index does not help when", "Why"],
   [["<b>The query returns a large fraction of the table.</b>",
     "Each matching row costs a random read; past some selectivity a "
     "sequential scan of everything is cheaper. <b>The crossover is often "
     "as low as 5–10% on spinning disks</b>, and higher on SSDs where "
     "random reads are less punishing."],
    ["<b>The column has low cardinality.</b>",
     "An index on a boolean or a status column with four values points at "
     "huge row sets, so every lookup degenerates into the case above."],
    ["<b>The leading column is not in the predicate.</b>",
     "See below. The most common and most expensive indexing mistake."],
    ["<b>A function is applied to the column.</b>",
     "<code>WHERE upper(name) = 'SMITH'</code> cannot use an index on "
     "<code>name</code>, because the index is ordered by name and not by "
     "upper(name). <b>An expression index on upper(name) fixes it</b>, and "
     "so does not writing the query that way."],
    ["<b>The workload is write-heavy.</b>",
     "Every index must be updated on every insert, update, and delete that "
     "touches its columns. Indexes are not free; they move cost from reads "
     "to writes."]],
   [0.32, 0.68]),
  ("callout", "Composite index order is not symmetric",
   ["An index on <code>(a, b)</code> is sorted by a, and then by b "
    "<i>within</i> each distinct value of a. It is a single ordering, not "
    "two independent ones.",
    "<b>It serves</b> <code>WHERE a = ?</code>, and <code>WHERE a = ? AND "
    "b = ?</code>, and <code>WHERE a = ? AND b BETWEEN ? AND ?</code> "
    "— anything that fixes a prefix of the key.",
    "<b>It does not serve</b> <code>WHERE b = ?</code>. The rows with a "
    "given b value are scattered across the index in as many separate places "
    "as there are distinct values of a. The optimiser may still scan the "
    "whole index if it is narrower than the table, but that is a scan, not a "
    "seek.",
    "<b>So (a,b) and (b,a) are genuinely different indexes</b>, and which "
    "you want depends on the queries you run. <b>The usual rule: equality "
    "predicates first, then the range predicate, then any covering "
    "columns.</b> A range predicate on a column stops the index from being "
    "useful for anything after it."]),
 ],
 "resources": [
   ("CMU 15-445 &mdash; Lectures 7–8, Tree Indexes",
    "https://15445.courses.cs.cmu.edu/",
    "B+tree structure, splits, merges, and the design decisions in &sect;2. "
    "The project assignment is the implementation."),
   ("Graefe &mdash; Modern B-Tree Techniques (free)",
    "https://web.archive.org/web/20240920153314/https://w6113.github.io/files/papers/btreesurvey-graefe.pdf",
    "The definitive survey. Prefix compression, suffix truncation, bulk "
    "loading, and everything else in &sect;2's refinements list."),
   ("Use The Index, Luke (free online book)",
    "https://use-the-index-luke.com/",
    "The best free material on &sect;3 — when indexes help, composite "
    "ordering, and covering indexes, with examples in several dialects."),
   ("Database Internals &mdash; B-tree chapters",
    "https://www.databass.dev/",
    "A second treatment with more attention to on-disk layout details."),
 ],
 "exercises": [
   "Compute the fanout and height for your page size and key type, for "
   "10<super>6</super>, 10<super>9</super>, and 10<super>12</super> keys. "
   "Compare against a binary tree.",
   "Implement a B+tree with insert and point lookup. Verify against an "
   "in-memory map after every operation on a randomised workload.",
   "Implement splits correctly and demonstrate that the tree grows only at "
   "the root — assert that all leaves are at equal depth after every "
   "insert.",
   "Deliberately move the separator key up instead of copying it, and "
   "demonstrate the keys that are lost.",
   "Implement range scan over linked leaves. Measure pages read and compare "
   "against the analytic prediction.",
   "Implement delete without merging. Insert a million keys, delete 90% in "
   "random order, and report the resulting page count against the "
   "theoretical minimum.",
   "Implement bulk loading. Compare build time and resulting page count "
   "against repeated insertion of the same data.",
   "Implement prefix compression and report the fanout improvement on a "
   "column of URLs or file paths.",
   "In PostgreSQL, create a table with a composite index on (a,b). Use "
   "<code>EXPLAIN</code> to confirm which of four predicates use the index.",
   "Find the selectivity crossover on your own machine: at what fraction of "
   "rows returned does a sequential scan beat an index scan?",
 ],
 "selfcheck": [
   "Why is a binary tree unsuitable for a disk-based index?",
   "Write the height formula and compute it for a billion keys at fanout "
   "1000.",
   "Give four differences between a B-tree and a B+tree, and the decisive "
   "one.",
   "Why does a B+tree stay balanced without any rebalancing logic?",
   "Why is the separator key copied rather than moved?",
   "Why do most implementations skip merging on delete, and what is the "
   "cost?",
   "Compare clustered and non-clustered indexes on five axes.",
   "What is a covering index, what does it save, and what does INCLUDE add?",
   "Give five situations where an index does not help.",
   "Why does an index on (a,b) not serve a predicate on b alone?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Hash Indexes, LSM Trees, and Concurrent Access",
 "subtitle": "The alternatives, and making any of them thread-safe.",
 "question": "When is a B+tree the wrong answer?",
 "outcomes": [
     "Compare hash indexes with B+trees and say when each wins.",
     "Explain extendible and linear hashing.",
     "Explain the LSM tree and the read/write amplification trade.",
     "Implement latch crabbing for concurrent B+tree access.",
     "Distinguish a latch from a lock and explain why both exist.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Hash indexes",
   "blurb": "O(1) lookup, and no order at all."},

  {"t": "two", "kicker": "Comparison", "title": "Hash index and B+tree",
   "lh": "Hash index",
   "l": ["<b>O(1) point lookup</b> — one page read, in principle.",
         "<b>No ordering whatsoever.</b>",
         "<b>No range scans. No ORDER BY. No prefix matching.</b>",
         ("Resizing is disruptive unless done carefully.", 1),
         "Good for exact-match only, on a high-cardinality key."],
   "rh": "B+tree",
   "r": ["O(log_f N) — three I/Os, two of them cached.",
         "<b>Fully ordered.</b>",
         "<b>Ranges, ORDER BY, prefix matching, MIN/MAX.</b>",
         ("Grows gracefully.", 1),
         "<b>The default for a reason.</b>"],
   "note": "The practical conclusion is that hash indexes are rarer than "
           "their asymptotic advantage suggests."},

  {"t": "callout", "title": "Why hash indexes are rarer than you would expect",
   "kind": "The honest comparison",
   "body": ["<b>The B+tree's three I/Os are usually one</b>, because the "
            "top levels are cached. The asymptotic advantage mostly "
            "evaporates.",
            "<b>And the B+tree does far more:</b> ranges, ordering, prefix "
            "matching, min and max — all for free.",
            "<b>So the hash index wins only for exact-match lookup on a "
            "high-cardinality key</b>, where the key is large enough that "
            "fanout suffers.",
            "<b>PostgreSQL's hash indexes were not even crash-safe until "
            "version 10</b>, which tells you how much they were used."]},

  {"t": "bullets", "kicker": "Dynamic hashing", "title": "Growing a hash table without rehashing everything",
   "items": [
     "<b>Static hashing</b> needs the size up front, and resizing means "
     "rehashing every entry at once — unacceptable for a live database.",
     "",
     "<b>Extendible hashing:</b> a directory of pointers indexed by the top "
     "d bits. Splitting one overflowing bucket doubles the directory, not "
     "the data.",
     "",
     "<b>Linear hashing:</b> split one bucket at a time, in a fixed round "
     "robin, regardless of which bucket overflowed. No directory needed.",
     "",
     "<b>Both spread the resize cost</b> over many operations rather than "
     "stalling the system once.",
   ],
   "note": "Linear hashing's 'split a bucket that is not the full one' is "
           "counterintuitive and is what avoids the directory."},

  {"t": "section", "label": "Part 2", "title": "LSM trees",
   "blurb": "What you build when writes dominate."},

  {"t": "callout", "title": "B+trees write badly",
   "kind": "The motivation",
   "body": ["A single row insert into a B+tree <b>dirties a whole page</b>, "
            "which must eventually be written back.",
            "<b>Inserts in random key order touch random pages</b>, so the "
            "write pattern is random — the worst case for storage.",
            "<b>And writing a page to change 50 bytes is 300× write "
            "amplification</b> on a 16 KB page.",
            "<b>The LSM tree inverts this:</b> buffer writes in memory, "
            "flush them as sorted runs, and merge the runs in the "
            "background. Every disk write is sequential."]},

  {"t": "code", "kicker": "LSM", "title": "The structure",
   "lang": "text", "code": """
  WRITES -->  MEMTABLE (in memory, sorted; a skip list or B-tree)
                 |  when full, flush as an immutable sorted file
                 v
              L0:  [SST] [SST] [SST]        <- may overlap in key range
                 |  compaction merges and sorts
                 v
              L1:  [ SST ][ SST ][ SST ]    <- disjoint ranges
                 |
              L2:  ...  each level ~10x the previous

  READ: check memtable, then L0 (all of it), then one file per level.
        A Bloom filter per file skips the ones that cannot contain
        the key -- without them, reads would be hopeless.
""",
   "caption": "Every write to disk is a sequential write of a whole sorted "
              "file. Reads pay by having to check several places.",
   "note": "Bloom filters are not an optimisation here — LSM reads are "
           "impractical without them."},

  {"t": "table", "kicker": "Amplification", "title": "Three amplifications, and you choose two",
   "header": ["Kind", "Means", "B+tree", "LSM"],
   "widths": [2.5, 4.4, 2.6, 2.6],
   "rows": [
     ["Read", "Pages read per logical read", "<b>Low</b>", "High"],
     ["Write", "Bytes written per logical write", "High", "<b>Lower</b>"],
     ["Space", "Disk used per byte of data", "<b>Low</b>", "High"],
   ],
   "footnote": "<b>The RUM conjecture:</b> you can optimise any two of "
               "read, update, and memory — not all three.",
   "note": "The RUM framing is the clean way to present this. It is a "
           "genuine trade, not a maturity difference."},

  {"t": "section", "label": "Part 3", "title": "Concurrency",
   "blurb": "Many threads in one tree."},

  {"t": "callout", "title": "A latch is not a lock",
   "kind": "A distinction that confuses everyone",
   "body": ["<b>A latch protects a data structure</b> — a page, a node, a "
            "hash bucket. Held for microseconds, during one operation.",
            "<b>A lock protects data</b> — a row, a table. Held for the "
            "duration of a <i>transaction</i>, possibly seconds "
            "(Module 09).",
            "<b>Latches are not logged, not tracked, and deadlock is "
            "prevented by ordering.</b> Locks are tracked and deadlock is "
            "detected.",
            "<b>The literature uses the words inconsistently</b>, which is "
            "a genuine source of confusion. In this course: latch = "
            "structure, lock = data."]},

  {"t": "code", "kicker": "Crabbing", "title": "Latch crabbing for B+tree descent",
   "lang": "text", "code": """
SEARCH (read):
  latch root (shared)
  loop:
      latch child (shared)
      RELEASE parent latch        <-- safe: we never go back up
      descend

INSERT / DELETE (write):
  latch root (exclusive)
  loop:
      latch child (exclusive)
      if child is SAFE:
          release ALL ancestor latches
      descend

  SAFE means the operation cannot propagate past this node:
      insert -> the node is not full      (no split will reach the parent)
      delete -> the node is more than half full  (no merge will)

Named "crabbing" because you hold two levels at once and release
the upper one only after grabbing the lower -- like a crab's gait.
""",
   "caption": "The safety test is the whole idea: once a node absorbs the "
              "change, no ancestor can be affected, so their latches can be "
              "released.",
   "note": "Students find the safe-node condition unintuitive until they "
           "trace a split that propagates two levels."},

  {"t": "callout", "title": "Optimistic descent is what real systems do",
   "kind": "The refinement",
   "body": ["Pessimistic crabbing takes <b>exclusive</b> latches all the way "
            "down for every write, which serialises every writer at the "
            "root.",
            "<b>The root becomes a bottleneck</b> immediately — every "
            "operation touches it.",
            "<b>Optimistic descent:</b> take shared latches down to the "
            "leaf, assuming no split is needed. Take an exclusive latch on "
            "the leaf only.",
            "<b>If a split turns out to be necessary, restart the descent "
            "pessimistically.</b> Splits are rare, so the restart is rare, "
            "and the common case never contends at the root."]},

  {"t": "bullets", "kicker": "Further", "title": "What production systems add",
   "items": [
     "<b>Blink-trees:</b> each node has a right-sibling pointer, so a reader "
     "that arrives mid-split can follow it instead of blocking.",
     "",
     "<b>Lock-free and optimistic lock coupling</b> using version counters "
     "— read, then verify the version did not change.",
     "",
     "<b>Latch ordering</b> to prevent deadlock — always acquire top to "
     "bottom, left to right. Never violate it.",
     "",
     "<b>Reader-writer latches</b> so readers do not exclude one another.",
     "",
     "<b>Test with thread sanitizers and stress</b>, not by reasoning. "
     "Concurrency bugs here corrupt data silently.",
   ],
   "footnote": "Blink-trees are the classic solution and are still what "
               "most systems use."},
 ],
 "takeaways": [
   "Hash indexes give O(1) point lookup and no ordering at all; B+trees give "
   "three cached I/Os plus ranges, ordering, and prefix matching.",
   "Extendible and linear hashing grow a hash table incrementally so a "
   "resize never stalls the system.",
   "B+trees write badly — random page dirtying and large write "
   "amplification. LSM trees buffer in memory and write sorted runs "
   "sequentially.",
   "Bloom filters are not an optimisation for LSM reads; they are what makes "
   "them practical at all.",
   "RUM: you can optimise read, update, or memory — any two, not all "
   "three. B+tree and LSM pick different pairs.",
   "A latch protects a structure for microseconds; a lock protects data for "
   "a transaction. Crabbing releases ancestor latches once a node is safe.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Hash indexes"),
  ("table", ["", "Hash index", "B+tree"],
   [["Point lookup", "<b>O(1)</b> — one page read in principle.",
     "O(log<sub>f</sub> N) — three levels, of which two are normally "
     "cached, so <b>effectively one read</b>."],
    ["Ordering", "<b>None.</b> The hash deliberately destroys it.",
     "<b>Full.</b>"],
    ["Supports", "Exact match only.",
     "<b>Range scans, ORDER BY, prefix matching, MIN and MAX</b> — all "
     "for free from the ordering."],
    ["Growth", "Requires rehashing, unless the scheme is dynamic "
     "(&sect;1.1).", "Grows gracefully by splitting."],
    ["Use when", "Exact-match lookup on a high-cardinality key, where the "
     "key is large enough that B+tree fanout suffers.",
     "<b>Essentially everything else.</b>"]],
   [0.14, 0.42, 0.44]),
  ("callout", "The asymptotic advantage mostly evaporates in practice",
   ["O(1) against O(log N) looks decisive on paper. It is not, for a "
    "specific reason: <b>the B+tree's logarithm is three, and two of those "
    "three levels are permanently in the buffer pool</b> because they are "
    "only a few megabytes. So both structures do about one disk read.",
    "<b>And the B+tree does far more for that one read.</b> Range scans, "
    "ordered output, prefix matching, and MIN/MAX all come free from the "
    "ordering that hashing deliberately destroys.",
    "<b>So hash indexes win in a narrow band:</b> exact-match lookups on a "
    "high-cardinality key, particularly where the key is large enough that "
    "it would badly reduce B+tree fanout.",
    "<b>The practical evidence is telling:</b> PostgreSQL's hash indexes "
    "were not crash-safe — not replicated, not recoverable — "
    "until version 10, released in 2017. Nobody had noticed, because almost "
    "nobody used them."]),
  ("ul", ["<b>Static hashing</b> requires choosing the table size in "
          "advance, and growing means rehashing every entry at once. For a "
          "live database that is an unacceptable stall.",
          "<b>Extendible hashing</b> keeps a <i>directory</i> of pointers "
          "indexed by the top d bits of the hash. When a bucket overflows, "
          "it splits, and only the directory doubles — the other "
          "buckets are untouched and are simply pointed to twice. The cost "
          "of growth is paid on the directory, which is small.",
          "<b>Linear hashing</b> dispenses with the directory. When any "
          "bucket overflows, it splits <i>the next bucket in a fixed round "
          "robin</i> — which is usually not the one that overflowed. "
          "Overflow chains handle the interim. This is counterintuitive and "
          "is precisely what removes the need for a directory, because the "
          "split point is known rather than looked up.",
          "<b>Both schemes spread the cost of growth</b> across many "
          "operations rather than concentrating it in one stall, which is "
          "the property a live system requires."]),

  ("h1", "2 &nbsp; LSM trees"),
  ("callout", "B+trees write badly",
   ["Inserting a single small row into a B+tree <b>dirties an entire "
    "page</b>, which must eventually be written back to disk.",
    "<b>Inserts arriving in random key order touch random pages</b>, so the "
    "resulting write pattern is random — the access pattern storage "
    "devices handle worst, and the one the whole of Module 02 was about "
    "avoiding.",
    "<b>And the write amplification is severe:</b> writing a 16 KB page to "
    "record a 50-byte change is a factor of roughly 300. On SSDs this "
    "matters twice over, because flash has limited write endurance.",
    "<b>The LSM tree inverts the design.</b> Buffer writes in memory, flush "
    "them periodically as immutable sorted files, and merge those files in "
    "the background. <b>Every write that reaches disk is a large sequential "
    "write of a whole file</b>, which is the pattern storage handles best."]),
  ("code", """WRITES --> MEMTABLE (in memory, sorted: skip list or B-tree)
              | flush when full, as an immutable sorted file (SST)
              v
           L0: [SST] [SST] [SST]          key ranges may overlap
              | compaction merges and sorts
              v
           L1: [ SST ][ SST ][ SST ]      disjoint key ranges
              |
           L2: ...                        each level ~10x the previous

READ: memtable, then ALL of L0, then one file per level below.
      A Bloom filter per file skips files that cannot hold the key."""),
  ("p", "<b>Bloom filters are not an optimisation here.</b> Without them, a "
        "point lookup for a key that does not exist would have to read a "
        "file from every level to establish its absence. A Bloom filter "
        "answers 'definitely not present' in a few bytes of memory, so the "
        "read touches only the files that might actually contain the key. "
        "<b>LSM reads are impractical without them</b>, which is why every "
        "implementation has them."),
  ("table", ["Amplification", "Definition", "B+tree", "LSM tree"],
   [["<b>Read</b>", "Pages read per logical read.",
     "<b>Low</b> — one path down the tree.",
     "<b>High</b> — several files may need checking, mitigated by "
     "Bloom filters."],
    ["<b>Write</b>", "Bytes written to disk per logical byte written.",
     "<b>High</b> — a whole page per small change, randomly placed.",
     "<b>Lower, and sequential</b> — though compaction rewrites data "
     "several times as it moves down the levels."],
    ["<b>Space</b>", "Disk space used per byte of live data.",
     "<b>Low</b> — about 1.4&times; from partially full pages.",
     "<b>High</b> — superseded versions persist until compaction "
     "removes them."]],
   [0.16, 0.26, 0.29, 0.29]),
  ("callout", "The RUM conjecture",
   ["Athanassoulis et al. framed this as the <b>RUM conjecture</b>: for any "
    "access method you can optimise <b>R</b>ead cost, <b>U</b>pdate cost, "
    "and <b>M</b>emory (space) — but only two of the three.",
    "<b>B+trees take read and space.</b> <b>LSM trees take update and "
    "(partly) read, giving up space.</b> Neither is a more mature version "
    "of the other; they occupy different corners of a genuine trade-off.",
    "<b>So the choice follows the workload.</b> Read-heavy and "
    "range-scan-heavy favours B+trees — which is why relational "
    "databases use them. Write-heavy with mostly point lookups favours LSM "
    "— which is why RocksDB, Cassandra, and LevelDB use them, and why "
    "they sit underneath so much of the key-value infrastructure.",
    "<b>Recognising a trade-off as structural rather than circumstantial</b> "
    "is what stops the argument about which is 'better', and it is the "
    "useful content of this section."]),

  ("break",),
  ("h1", "3 &nbsp; Concurrent access"),
  ("callout", "A latch is not a lock",
   ["The terminology is genuinely confusing, and the literature is "
    "inconsistent. This course uses the database convention:",
    "<b>A latch protects a data structure</b> — a page, a B+tree node, "
    "a hash bucket. It is held for microseconds, for the duration of a "
    "single physical operation. It is not logged, not tracked in any table, "
    "and deadlock is prevented by imposing an acquisition <i>order</i> "
    "rather than by detection. In operating systems this is called a lock or "
    "a mutex.",
    "<b>A lock protects data</b> — a row, a range, a table. It is held "
    "for the duration of a <b>transaction</b>, which may be seconds. It is "
    "tracked in a lock table, it participates in deadlock detection, and it "
    "is the subject of Module 09.",
    "<b>Both exist and both are necessary</b>, and they operate at "
    "completely different timescales for completely different purposes. "
    "Confusing them is the main obstacle to reading the literature."]),
  ("code", """SEARCH (read):
  latch root (shared)
  loop: latch child (shared); RELEASE parent; descend

INSERT / DELETE (write):
  latch root (exclusive)
  loop: latch child (exclusive)
        if child is SAFE: release ALL ancestor latches
        descend

SAFE = the operation cannot propagate past this node:
   insert -> node is not full          (no split will reach the parent)
   delete -> node is more than half full  (no merge will)"""),
  ("p", "<b>The safety test is the whole idea.</b> Once a node can absorb "
        "the change without splitting or merging, no ancestor can possibly "
        "be affected by it, so every ancestor latch can be released "
        "immediately — which lets other threads descend behind you. "
        "The name 'crabbing' comes from holding two levels at once and "
        "releasing the upper only after acquiring the lower, like a crab's "
        "gait."),
  ("callout", "Optimistic descent is what production systems actually do",
   ["Pessimistic crabbing takes <b>exclusive</b> latches from the root "
    "downward on every insert and delete. <b>The root is therefore "
    "exclusively latched by every writer</b>, however briefly, which "
    "serialises all writers at a single point. On a multi-core machine this "
    "is immediately the bottleneck.",
    "<b>Optimistic descent assumes the common case:</b> take <i>shared</i> "
    "latches all the way down, on the assumption that no split will be "
    "needed, and take an exclusive latch only on the leaf.",
    "<b>If it turns out a split is required, release everything and restart "
    "the descent pessimistically.</b> Splits are rare — a node splits "
    "once per roughly f insertions — so the restart is rare, and the "
    "overwhelming majority of writes never contend at the root at all.",
    "<b>This is the standard approach</b>, and it is a good example of a "
    "general pattern: make the common case cheap and detect the rare case "
    "rather than defending against it everywhere."]),
  ("ul", ["<b>B<super>link</super>-trees</b> give each node a pointer to its "
          "right sibling. A reader that arrives at a node mid-split, and "
          "finds the key it wants is no longer there, follows the sibling "
          "pointer rather than blocking or restarting. This decouples "
          "readers from writers almost entirely, and it is still the basis "
          "of most production implementations — PostgreSQL's B-tree is "
          "a B<super>link</super>-tree.",
          "<b>Optimistic lock coupling</b> uses a version counter per node: "
          "read the version, read the node, re-read the version, and restart "
          "if it changed. No latch is taken for reading at all.",
          "<b>Latch ordering prevents deadlock.</b> Always acquire top to "
          "bottom and left to right, without exception. Any code path that "
          "violates the order can deadlock, and the deadlock will appear "
          "under load, in production, rarely.",
          "<b>Use reader-writer latches</b> so that concurrent readers do "
          "not exclude one another — which is the whole point, since "
          "reads dominate.",
          "<b>Test with thread sanitisers and sustained stress, not by "
          "reasoning.</b> Concurrency bugs in an index corrupt data "
          "<i>silently</i>: the tree remains structurally plausible and "
          "returns wrong answers. Project 1's requirement of eight threads "
          "and ten million operations verified against a reference map is "
          "the minimum honest test."]),
 ],
 "resources": [
   ("CMU 15-445 &mdash; Lectures 7 and 9, Hash Tables and Index Concurrency",
    "https://15445.courses.cs.cmu.edu/",
    "Extendible and linear hashing, and latch crabbing with the safe-node "
    "condition."),
   ("O'Neil et al. &mdash; The Log-Structured Merge-Tree (1996, free)",
    "https://www.cs.umb.edu/~poneil/lsmtree.pdf",
    "The original LSM paper. Short, and the amplification argument of "
    "&sect;2 is already in it."),
   ("Athanassoulis et al. &mdash; Designing Access Methods: The RUM "
    "Conjecture (free)",
    "https://stratos.seas.harvard.edu/publications/",
    "The framing in &sect;2 that makes the trade-off explicit."),
   ("Lehman & Yao &mdash; Efficient Locking for Concurrent Operations on "
    "B-Trees (1981, free)",
    "https://www.csd.uoc.gr/~hy460/pdf/p650-lehman.pdf",
    "The B<super>link</super>-tree of &sect;3. Still the basis of "
    "PostgreSQL's implementation."),
   ("RocksDB wiki",
    "https://github.com/facebook/rocksdb/wiki",
    "A production LSM engine, documented in detail by its maintainers. The "
    "compaction and tuning pages are the practical side of &sect;2."),
 ],
 "exercises": [
   "Implement extendible hashing with directory doubling. Verify that a "
   "bucket split touches only that bucket and the directory.",
   "Implement linear hashing and compare the worst-case latency of a single "
   "insert against static hashing with rehashing.",
   "Compare your hash index against your B+tree on point lookups and on "
   "range scans. Report both, and the key size at which hashing starts to "
   "win on point lookups.",
   "Implement a minimal LSM tree: memtable, flush to sorted files, and "
   "level-based compaction.",
   "Measure read, write, and space amplification for your LSM and for your "
   "B+tree on the same workload. Place both on the RUM triangle.",
   "Add Bloom filters and measure the reduction in files read per lookup for "
   "keys that are absent.",
   "Implement pessimistic latch crabbing. Measure throughput against thread "
   "count and show the root becoming the bottleneck.",
   "Implement optimistic descent and repeat. Report the scaling improvement "
   "and the restart rate.",
   "Run your concurrent B+tree under a thread sanitiser with eight threads "
   "and ten million mixed operations, verifying against a reference map.",
   "Deliberately violate latch ordering in one code path and construct a "
   "workload that deadlocks.",
 ],
 "selfcheck": [
   "Compare hash indexes and B+trees on five axes, and say when hashing "
   "wins.",
   "Why does the hash index's O(1) advantage mostly evaporate in practice?",
   "Explain extendible and linear hashing and what each avoids.",
   "Give two reasons B+trees write badly.",
   "Describe the LSM structure and explain why Bloom filters are essential "
   "rather than optional.",
   "State the RUM conjecture and say which two each of B+tree and LSM "
   "choose.",
   "Distinguish a latch from a lock on four axes.",
   "What is latch crabbing, and what is the safe-node condition?",
   "Why is pessimistic crabbing a bottleneck, and what does optimistic "
   "descent do instead?",
   "What is a B<super>link</super>-tree and what does the sibling pointer "
   "achieve?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Relational Algebra and SQL",
 "subtitle": "What a query means, before anyone decides how to run it.",
 "question": "What does a SQL query actually say?",
 "outcomes": [
     "Express queries in relational algebra.",
     "Explain the gap between SQL and the algebra.",
     "Explain three-valued logic and the problems NULL causes.",
     "Trace SQL's logical evaluation order.",
     "Explain why declarative querying requires an optimiser.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The algebra",
   "blurb": "Six operators, and everything else is sugar."},

  {"t": "table", "kicker": "Operators", "title": "Relational algebra",
   "header": ["Operator", "Symbol", "Does", "SQL"],
   "widths": [2.5, 1.6, 4.0, 4.0],
   "rows": [
     ["Select", "&sigma;", "Keep rows matching a predicate", "<code>WHERE</code>"],
     ["Project", "&pi;", "Keep columns; <b>remove duplicates</b>", "<code>SELECT DISTINCT</code>"],
     ["Union", "&cup;", "Rows in either", "<code>UNION</code>"],
     ["Difference", "&minus;", "Rows in one, not the other", "<code>EXCEPT</code>"],
     ["Product", "&times;", "Every pair", "<code>CROSS JOIN</code>"],
     ["Rename", "&rho;", "Rename a relation or attribute", "<code>AS</code>"],
   ],
   "footnote": "Join is &sigma; applied to &times; — derived, not "
               "primitive. Which is exactly why the optimiser can rewrite "
               "it.",
   "note": "That join is derived rather than primitive is the key fact for "
           "Module 08."},

  {"t": "callout", "title": "Closure is what makes composition work",
   "kind": "The property that matters",
   "body": ["<b>Every operator takes relations and returns a "
            "relation.</b>",
            "So operators compose arbitrarily — the output of one is a "
            "valid input to any other. Subqueries, views, and CTEs all "
            "follow from this.",
            "<b>And it means a query is a tree of operators</b>, which is "
            "exactly the structure an optimiser manipulates and an executor "
            "walks.",
            "<b>Without closure there would be no query plans</b>, no "
            "algebraic rewriting, and no optimisation. The whole "
            "architecture rests on this one property."]},

  {"t": "callout", "title": "SQL is not the relational algebra",
   "kind": "Three real differences",
   "body": ["<b>SQL has bags, not sets.</b> Duplicates persist unless you "
            "ask for DISTINCT. The algebra's relations are sets.",
            "<b>SQL has NULL</b>, which the algebra does not, and it brings "
            "three-valued logic with it (Part 2).",
            "<b>SQL has order</b> — ORDER BY, LIMIT, window functions. "
            "Relations are unordered by definition.",
            "<b>These are not pedantry.</b> Each one is a genuine source of "
            "bugs, and the NULL one in particular catches experienced people "
            "regularly."]},

  {"t": "section", "label": "Part 2", "title": "NULL",
   "blurb": "The feature Codd wanted and many regret."},

  {"t": "table", "kicker": "Three-valued logic", "title": "AND, OR, and UNKNOWN",
   "header": ["Expression", "Result"],
   "widths": [5.6, 6.5],
   "rows": [
     ["<code>NULL = NULL</code>", "<b>UNKNOWN</b> — not TRUE"],
     ["<code>NULL &lt;&gt; NULL</code>", "<b>UNKNOWN</b> — not TRUE either"],
     ["<code>TRUE OR NULL</code>", "TRUE"],
     ["<code>FALSE AND NULL</code>", "FALSE"],
     ["<code>TRUE AND NULL</code>", "UNKNOWN"],
     ["<code>WHERE &lt;UNKNOWN&gt;</code>", "<b>Row excluded</b> — only TRUE passes"],
   ],
   "footnote": "<code>IS NULL</code> is the only way to test for it. "
               "<code>= NULL</code> is always UNKNOWN and matches nothing.",
   "note": "The last row is the practical rule: WHERE needs TRUE, and "
           "UNKNOWN is not TRUE."},

  {"t": "callout", "title": "The NOT IN trap",
   "kind": "The bug that bites everyone once",
   "body": ["<code>WHERE x NOT IN (SELECT y FROM t)</code> returns "
            "<b>nothing at all</b> if any y is NULL.",
            "<b>Why:</b> <code>x NOT IN (1, 2, NULL)</code> expands to "
            "<code>x&lt;&gt;1 AND x&lt;&gt;2 AND x&lt;&gt;NULL</code>. The "
            "last conjunct is UNKNOWN, so the whole thing is UNKNOWN or "
            "FALSE — never TRUE.",
            "<b>The query is silently empty.</b> No error, no warning, and "
            "it worked yesterday before a NULL appeared in the data.",
            "<b>Use NOT EXISTS instead</b>, which is also usually faster. "
            "This is the single most costly NULL behaviour in practice."]},

  {"t": "bullets", "kicker": "More NULL", "title": "Other inconsistencies worth knowing",
   "items": [
     "<b>Aggregates skip NULLs.</b> <code>AVG(x)</code> ignores them, so "
     "the denominator is not the row count.",
     "",
     "<b>But COUNT(*) counts every row</b>, while "
     "<code>COUNT(x)</code> skips NULL x. Two different questions, one "
     "character apart.",
     "",
     "<b>GROUP BY treats NULLs as equal</b> and puts them in one group "
     "— even though <code>NULL = NULL</code> is UNKNOWN.",
     "",
     "<b>UNIQUE constraints permit multiple NULLs</b> in most systems, for "
     "the same reason — and the standard is ambiguous.",
     "",
     "<b>ORDER BY must decide</b> where NULLs sort. Systems differ; the "
     "standard allows either.",
   ],
   "note": "The GROUP BY inconsistency is the clearest illustration that "
           "NULL semantics were not designed as a whole."},

  {"t": "section", "label": "Part 3", "title": "Evaluation order",
   "blurb": "Not the order the clauses are written in."},

  {"t": "code", "kicker": "Order", "title": "SQL's logical evaluation order",
   "lang": "text", "code": """
  WRITTEN                      EVALUATED
  -------                      ---------
  SELECT    ...                1.  FROM / JOIN      build the row source
  FROM      ...                2.  WHERE            filter individual rows
  WHERE     ...                3.  GROUP BY         form groups
  GROUP BY  ...                4.  HAVING           filter GROUPS
  HAVING    ...                5.  SELECT           compute output columns
  ORDER BY  ...                6.  DISTINCT
  LIMIT     ...                7.  ORDER BY         sort the result
                               8.  LIMIT

  CONSEQUENCES:
   * WHERE cannot reference a SELECT alias -- it has not been computed.
   * ORDER BY CAN -- by then it has.
   * HAVING filters groups; WHERE filters rows. Not interchangeable.
   * An aggregate cannot appear in WHERE. It does not exist yet.
""",
   "caption": "This is the <i>logical</i> order. The optimiser may execute "
              "in any order that produces the same result.",
   "note": "Nearly every 'why can't I use my alias here' question is "
           "answered by this slide."},

  {"t": "callout", "title": "Declarative is the point, and it is why an optimiser exists",
   "kind": "Closing the loop with Module 01",
   "body": ["SQL says <i>what</i> rows you want. It says nothing about "
            "which index to use, which join algorithm, or what order to join "
            "in.",
            "<b>So something must decide</b> — and that is the optimiser "
            "(Module 08).",
            "<b>The benefit:</b> the same query gets faster when an index is "
            "added or statistics improve, with no change to the query.",
            "<b>The cost:</b> you cannot directly control execution, and "
            "when the optimiser chooses badly the query is slow for reasons "
            "the text does not reveal. This is the single most common "
            "practical frustration with SQL."]},
 ],
 "takeaways": [
   "Six primitive operators — select, project, union, difference, "
   "product, rename. Join is derived, which is why it can be rewritten.",
   "Closure means every operator returns a relation, so queries are trees of "
   "operators. Query plans and optimisation depend entirely on this.",
   "SQL differs from the algebra in three real ways: bags not sets, NULL, "
   "and order.",
   "NULL brings three-valued logic. WHERE passes only TRUE, so UNKNOWN "
   "excludes the row.",
   "NOT IN returns nothing if the subquery yields any NULL — silently. "
   "Use NOT EXISTS.",
   "Clauses are evaluated FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, "
   "LIMIT — which explains most alias and aggregate restrictions.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Relational algebra"),
  ("table", ["Operator", "Notation", "Meaning", "SQL"],
   [["<b>Selection</b>", "&sigma;<sub>cond</sub>(R)",
     "The rows of R satisfying a condition.", "<code>WHERE</code>"],
    ["<b>Projection</b>", "&pi;<sub>cols</sub>(R)",
     "The named columns, <b>with duplicates removed</b> — the result "
     "is a set.", "<code>SELECT DISTINCT</code>"],
    ["<b>Union</b>", "R &cup; S", "Rows in either, duplicates removed.",
     "<code>UNION</code>"],
    ["<b>Difference</b>", "R &minus; S", "Rows in R not in S.",
     "<code>EXCEPT</code>"],
    ["<b>Cartesian product</b>", "R &times; S", "Every row of R paired with "
     "every row of S.", "<code>CROSS JOIN</code>"],
    ["<b>Rename</b>", "&rho;<sub>a/b</sub>(R)", "Rename a relation or "
     "attribute.", "<code>AS</code>"]],
   [0.16, 0.17, 0.42, 0.25]),
  ("p", "<b>Join is not primitive.</b> A natural or equi-join is a selection "
        "applied to a Cartesian product: R &#8904; S = "
        "&sigma;<sub>cond</sub>(R &times; S). It is defined as a derived "
        "operator purely for convenience — and that derivation is "
        "exactly what licenses the optimiser to reorder joins and push "
        "predicates around (Module 08). An operator defined in terms of "
        "others can be re-expressed in terms of others."),
  ("callout", "Closure is the property everything depends on",
   ["<b>Every operator takes relations and returns a relation.</b> There is "
    "no operator that returns a scalar, or a list, or something that is not "
    "itself a valid input to every other operator.",
    "<b>So operators compose without restriction.</b> The output of a "
    "selection can be projected, joined, unioned, or selected again. "
    "Subqueries, views, and common table expressions are all direct "
    "consequences — a view is simply a named expression.",
    "<b>And a query is therefore a tree of operators</b>, which is precisely "
    "the structure an optimiser rewrites and an executor walks "
    "(Modules 07, 08).",
    "<b>Without closure there would be no query plans and no algebraic "
    "optimisation.</b> The entire architecture of a query processor rests on "
    "this one property, which is why it is worth naming explicitly rather "
    "than treating as obvious."]),
  ("table", ["SQL differs from the algebra", "Consequence"],
   [["<b>Bags, not sets.</b>",
     "SQL keeps duplicates unless <code>DISTINCT</code> is requested. This "
     "is a deliberate performance decision — eliminating duplicates "
     "requires a sort or a hash — and it means SQL's <code>UNION "
     "ALL</code> is cheaper than <code>UNION</code>, and that some algebraic "
     "identities do not hold."],
    ["<b>NULL exists.</b>",
     "The algebra has no such value. SQL's NULL brings three-valued logic "
     "with it, and a collection of special cases — &sect;2."],
    ["<b>Order exists.</b>",
     "<code>ORDER BY</code>, <code>LIMIT</code>, and window functions all "
     "depend on row order, which relations do not have. This is why "
     "<code>ORDER BY</code> is only meaningful at the outermost level, and "
     "why an <code>ORDER BY</code> inside a subquery or view is not "
     "guaranteed to survive."]],
   [0.26, 0.74]),

  ("h1", "2 &nbsp; NULL and three-valued logic"),
  ("p", "Codd introduced NULL to represent missing or inapplicable "
        "information, and later proposed distinguishing the two cases with "
        "separate markers. SQL adopted one NULL, and the resulting semantics "
        "are the most consistently criticised part of the language."),
  ("table", ["Expression", "Evaluates to", "Note"],
   [["<code>NULL = NULL</code>", "<b>UNKNOWN</b>",
     "Not TRUE. Two unknown values are not known to be equal."],
    ["<code>NULL &lt;&gt; NULL</code>", "<b>UNKNOWN</b>",
     "Not TRUE either. They are not known to be different."],
    ["<code>TRUE OR NULL</code>", "TRUE",
     "The truth of the left operand settles it."],
    ["<code>FALSE AND NULL</code>", "FALSE", "Likewise."],
    ["<code>TRUE AND NULL</code>", "UNKNOWN", "Undetermined."],
    ["<b>A WHERE clause</b>", "<b>Passes only TRUE</b>",
     "<b>UNKNOWN excludes the row, exactly as FALSE does.</b> This is the "
     "rule that explains almost every NULL surprise."]],
   [0.26, 0.17, 0.57]),
  ("callout", "The NOT IN trap",
   ["<code>WHERE x NOT IN (SELECT y FROM t)</code> <b>returns no rows at "
    "all</b> if any y in the subquery is NULL.",
    "<b>The expansion shows why.</b> <code>x NOT IN (1, 2, NULL)</code> "
    "means <code>x &lt;&gt; 1 AND x &lt;&gt; 2 AND x &lt;&gt; NULL</code>. "
    "The final conjunct is UNKNOWN for every x, so the conjunction is either "
    "FALSE (if x equals 1 or 2) or UNKNOWN (otherwise). <b>It is never "
    "TRUE</b>, so no row ever passes the WHERE clause.",
    "<b>The query silently returns nothing.</b> No error, no warning, and "
    "nothing in the text suggests a problem. It worked correctly yesterday, "
    "and then a single NULL appeared in the referenced column.",
    "<b>Use <code>NOT EXISTS</code> instead</b>, which uses existential "
    "semantics rather than a comparison chain and behaves as expected. It is "
    "also usually faster, because it can short-circuit. <b>This is the most "
    "expensive NULL behaviour in practice</b> and it catches experienced "
    "people, because the failure is silent and data-dependent."]),
  ("ul", ["<b>Aggregates skip NULLs.</b> <code>AVG(x)</code> divides by the "
          "number of non-NULL values, not by the row count. This is usually "
          "what you want and is worth knowing explicitly.",
          "<b><code>COUNT(*)</code> counts rows; <code>COUNT(x)</code> "
          "counts non-NULL x.</b> Two genuinely different questions, "
          "distinguished by one character.",
          "<b><code>GROUP BY</code> treats NULLs as equal</b> and collects "
          "them into a single group — even though <code>NULL = "
          "NULL</code> is UNKNOWN. This is a direct inconsistency, and it is "
          "the clearest evidence that NULL semantics were assembled "
          "piecemeal rather than designed.",
          "<b>UNIQUE constraints usually permit multiple NULLs</b>, on the "
          "grounds that two NULLs are not known to be equal. The SQL "
          "standard is ambiguous and systems differ.",
          "<b><code>ORDER BY</code> must place NULLs somewhere.</b> The "
          "standard permits first or last; PostgreSQL defaults to last for "
          "ascending, Oracle to last, MySQL to first. Specify <code>NULLS "
          "FIRST</code> or <code>NULLS LAST</code> if it matters."]),

  ("break",),
  ("h1", "3 &nbsp; Evaluation order"),
  ("code", """WRITTEN                 LOGICALLY EVALUATED
SELECT    ...           1. FROM / JOIN    build the row source
FROM      ...           2. WHERE          filter individual rows
WHERE     ...           3. GROUP BY       form groups
GROUP BY  ...           4. HAVING         filter GROUPS
HAVING    ...           5. SELECT         compute output expressions
ORDER BY  ...           6. DISTINCT
LIMIT     ...           7. ORDER BY       sort the result
                        8. LIMIT"""),
  ("table", ["Consequence", "Why"],
   [["<b>WHERE cannot reference a SELECT alias.</b>",
     "WHERE runs at step 2; the alias is not computed until step 5. (Some "
     "systems permit it as an extension; the standard does not.)"],
    ["<b>ORDER BY can reference a SELECT alias.</b>",
     "ORDER BY runs at step 7, after SELECT has computed it."],
    ["<b>HAVING and WHERE are not interchangeable.</b>",
     "<b>WHERE filters rows before grouping; HAVING filters groups "
     "after.</b> Moving a condition from HAVING to WHERE changes the "
     "result whenever it affects which rows form the groups — and "
     "moving a non-aggregate condition the other way is a common "
     "performance mistake, since filtering before grouping is cheaper."],
    ["<b>An aggregate cannot appear in WHERE.</b>",
     "Aggregates are computed during grouping at step 3. At step 2 they do "
     "not exist."]],
   [0.33, 0.67]),
  ("p", "<b>This is the <i>logical</i> order, not the execution order.</b> "
        "The optimiser is free to execute in any order that produces the "
        "same result — and routinely does, pushing filters below joins "
        "and evaluating aggregates during a scan. The logical order defines "
        "the <i>meaning</i>; Module 08 covers what is done with it."),
  ("callout", "Declarative querying is the point, and the optimiser is the cost",
   ["A SQL query specifies <i>which rows</i> you want. It says nothing "
    "about which index to use, which join algorithm to apply, or in what "
    "order to join four tables.",
    "<b>So something has to decide</b>, and that something is the optimiser "
    "(Module 08). This is Module 01's data independence, made concrete: the "
    "query is insulated from the physical structures beneath it.",
    "<b>The benefit is substantial.</b> Adding an index makes existing "
    "queries faster with no change to any of them. Updated statistics change "
    "the plan. A new release's better join algorithm improves queries "
    "written a decade earlier.",
    "<b>The cost is loss of control.</b> You cannot directly specify how a "
    "query runs, and when the optimiser chooses badly — which it "
    "does, for reasons Module 08 makes precise — the query is slow for "
    "reasons the text does not reveal. <b>This is the most common practical "
    "frustration with SQL</b>, and it is the direct price of the "
    "abstraction that makes everything else work."]),
 ],
 "resources": [
   ("CMU 15-445 &mdash; Lecture 2, Modern SQL",
    "https://15445.courses.cs.cmu.edu/",
    "SQL beyond the basics: window functions, CTEs, lateral joins, and the "
    "evaluation order of &sect;3."),
   ("Date &mdash; writings on NULL and three-valued logic",
    "https://www.dbdebunk.com/",
    "The case against NULL, argued at length by someone who worked with "
    "Codd. Opinionated, and the technical content in &sect;2 is correct."),
   ("Markus Winand &mdash; Modern SQL (free)",
    "https://modern-sql.com/",
    "Excellent free material on what SQL has gained since 1992, and on the "
    "evaluation order."),
   ("PostgreSQL documentation &mdash; Queries chapter",
    "https://www.postgresql.org/docs/current/queries.html",
    "Precise on evaluation order, NULL handling, and where the "
    "implementation differs from the standard."),
 ],
 "exercises": [
   "Express five queries of your own in relational algebra, then in SQL, and "
   "confirm they agree on real data.",
   "Demonstrate that join is derived: write an equi-join as a selection over "
   "a cross join and confirm identical results. Then compare the query "
   "plans.",
   "Construct a case where <code>UNION</code> and <code>UNION ALL</code> "
   "differ, and measure the cost difference.",
   "Build the full three-valued truth tables for AND, OR, and NOT by "
   "querying the database rather than by reading them.",
   "<b>Reproduce the NOT IN trap:</b> write a query that returns rows, then "
   "insert one NULL and show it returns none. Rewrite with NOT EXISTS.",
   "Demonstrate the GROUP BY inconsistency: show that NULLs group together "
   "while <code>NULL = NULL</code> is UNKNOWN.",
   "Compare <code>COUNT(*)</code> and <code>COUNT(column)</code> on a table "
   "with NULLs and explain the difference to someone who has not seen it.",
   "Write a query where moving a condition from HAVING to WHERE changes the "
   "result, and one where it does not but changes the cost.",
   "Test NULL sort order in two different database systems and report the "
   "difference.",
 ],
 "selfcheck": [
   "Name the six primitive relational operators and say why join is not one "
   "of them.",
   "What is closure, and what would be impossible without it?",
   "Give three ways SQL differs from the relational algebra.",
   "What does <code>NULL = NULL</code> evaluate to, and what does a WHERE "
   "clause do with it?",
   "Explain the NOT IN trap precisely and give the fix.",
   "Give four other NULL inconsistencies.",
   "State SQL's logical evaluation order and derive three of its "
   "consequences.",
   "Why can WHERE not reference a SELECT alias when ORDER BY can?",
   "What does declarative querying buy, and what does it cost?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Sorting and Joins",
 "subtitle": "The two operations that dominate query cost.",
 "question": "How do you sort or join data larger than memory?",
 "outcomes": [
     "Implement external merge sort and compute its I/O cost.",
     "Implement nested loop, sort-merge, and hash joins.",
     "Analyse each join's I/O cost and say when each wins.",
     "Explain why hash joins usually win and when they do not.",
     "Explain how joins degrade when memory is insufficient.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "External sorting",
   "blurb": "The foundation for everything else in this module."},

  {"t": "callout", "title": "Sort what does not fit",
   "kind": "The two-phase approach",
   "body": ["<b>Phase 1 — runs:</b> read B pages into memory, sort them "
            "in place, write the sorted run out. Repeat until the input is "
            "consumed. Produces N/B sorted runs.",
            "<b>Phase 2 — merge:</b> merge B−1 runs at a time, using one "
            "buffer page per run and one for output.",
            "<b>Both phases are purely sequential I/O.</b> No random "
            "access anywhere, which is the entire point.",
            "<b>With a reasonable buffer pool, one merge pass is almost "
            "always enough</b>, and the cost is effectively 'read twice, "
            "write twice'."]},

  {"t": "eq", "kicker": "Cost", "title": "The I/O cost of external sort",
   "eqs": [
     ("passes  =  1 + ⌈log_{B−1}(N/B)⌉",
      "One pass to create runs, then merging with fanout B−1."),
     ("I/O  =  2N × passes",
      "Each pass reads and writes the whole file."),
     ("N=10⁶ pages, B=1000  ⟹  2 passes, 4×10⁶ I/Os",
      "A gigabyte of buffer sorts a terabyte in two passes. The logarithm "
      "has a very large base."),
   ],
   "caption": "The base of the logarithm is the buffer size, which is why "
              "more memory helps so disproportionately here.",
   "note": "Have them compute the terabyte case. The base-1000 logarithm is "
           "the surprise."},

  {"t": "bullets", "kicker": "Refinements", "title": "What real sorts do",
   "items": [
     "<b>Replacement selection</b> produces runs averaging 2B rather than B, "
     "by maintaining a heap and writing out records as they become eligible.",
     "",
     "<b>Double buffering</b> overlaps I/O with comparison, so the CPU is "
     "not idle during reads.",
     "",
     "<b>Skip the sort entirely</b> if a B+tree already provides the order "
     "— scan the index instead.",
     "",
     "<b>Partial sorts for LIMIT:</b> a top-K heap beats a full sort when "
     "only the first few rows are wanted.",
     "",
     "<b>Normalised keys:</b> encode the sort key as a byte string so "
     "comparisons are memcmp. Large constant-factor win.",
   ],
   "footnote": "Normalised keys matter more than the asymptotics in "
               "practice — comparison cost dominates once I/O is "
               "sequential."},

  {"t": "section", "label": "Part 2", "title": "Joins",
   "blurb": "Three algorithms, three cost profiles."},

  {"t": "table", "kicker": "Nested loop", "title": "The three nested loop variants",
   "header": ["Variant", "Cost", "When"],
   "widths": [3.0, 4.4, 4.7],
   "rows": [
     ["Naive (tuple)", "M + (m &times; N)", "<b>Never. Pathological</b>"],
     ["Block", "M + (M &times; N)", "Small outer relation"],
     ["<b>Index</b>", "<b>M + (m &times; lookup)</b>", "<b>Inner side is indexed and outer is small</b>"],
   ],
   "footnote": "M, N = pages; m = rows in the outer. Index nested loop is "
               "the right choice far more often than its reputation "
               "suggests.",
   "note": "Index nested loop with a small outer is extremely common in "
           "OLTP and is often the plan you want."},

  {"t": "callout", "title": "Sort-merge join",
   "kind": "When order already exists or is wanted",
   "body": ["<b>Sort both inputs on the join key</b> (Part 1), then walk "
            "them together in one pass.",
            "<b>Cost:</b> the two sorts plus M + N for the merge.",
            "<b>Free if an input is already sorted</b> — because it came "
            "from a clustered index, or from an earlier sort-merge join.",
            "<b>And the output is sorted</b>, which may satisfy a later "
            "ORDER BY or GROUP BY for nothing. The optimiser accounts for "
            "this as an 'interesting order' (Module 08)."]},

  {"t": "code", "kicker": "Hash join", "title": "Grace hash join",
   "lang": "text", "code": """
PHASE 1 -- PARTITION both relations by hash(join_key) % P
    R -> R0 R1 R2 ... RP      S -> S0 S1 S2 ... SP
    Rows that could possibly join are now in the SAME partition index.
    Cost: read and write both relations once.

PHASE 2 -- JOIN partition by partition
    for i in 0..P:
        build an in-memory hash table on Ri   (the smaller side)
        probe it with every row of Si
    Each partition is sized to fit in memory, so this is one pass.
    Cost: read both relations once.

TOTAL: 3(M + N)   -- each relation read once, written once, read once.

*** Only works for EQUI-joins. A hash tells you nothing about < or >. ***
""",
   "caption": "Partitioning guarantees that matching rows land in the same "
              "partition, which is what makes the second phase a single "
              "pass.",
   "note": "The equi-join restriction is the key limitation and is why "
           "sort-merge survives."},

  {"t": "table", "kicker": "Comparison", "title": "Choosing a join",
   "header": ["Algorithm", "Cost", "Requires", "Best when"],
   "widths": [2.5, 2.4, 3.0, 4.2],
   "rows": [
     ["Index NL", "M + m&middot;lookup", "Index on inner", "<b>Small outer, indexed inner</b>"],
     ["Block NL", "M + M&middot;N", "Nothing", "Tiny outer; non-equi join"],
     ["Sort-merge", "sorts + M+N", "Sortable key", "<b>Already sorted; output order wanted</b>"],
     ["<b>Hash</b>", "<b>3(M+N)</b>", "<b>Equi-join</b>", "<b>Large unsorted inputs. The default</b>"],
   ],
   "footnote": "Hash join usually wins on large unsorted equi-joins, which "
               "is most analytical work.",
   "note": "The 'requires' column is what decides it as often as the cost "
           "column."},

  {"t": "section", "label": "Part 3", "title": "When memory runs out",
   "blurb": "The failure mode that explains most slow queries."},

  {"t": "callout", "title": "Spilling is a cliff, not a slope",
   "kind": "Why a query suddenly gets slow",
   "body": ["A hash join's build side is sized to fit in memory. <b>If the "
            "estimate was wrong</b> — and Module 08 explains why it often "
            "is — the hash table does not fit.",
            "<b>The join spills to disk</b>, and the cost jumps by an order "
            "of magnitude in one step.",
            "<b>This is why a query that was fast last week is slow "
            "today:</b> the table grew past the point where the estimate "
            "and the memory limit still matched.",
            "<b>Recursive partitioning</b> handles it — partition the "
            "oversized partition again — but skew can defeat even that, "
            "if one key value dominates."]},

  {"t": "bullets", "kicker": "Diagnosis", "title": "Reading a slow join",
   "items": [
     "<b>EXPLAIN ANALYZE shows estimated against actual row counts.</b> A "
     "large gap is the single most informative signal available.",
     "",
     "<b>Look for spills</b> — Postgres reports 'Batches: 4' or external "
     "sort disk usage. More than one batch means the estimate was wrong.",
     "",
     "<b>Check for a nested loop over a large outer.</b> Usually a "
     "cardinality underestimate.",
     "",
     "<b>Check for skew:</b> one key value matching millions of rows "
     "defeats hash partitioning entirely.",
     "",
     "<b>Then fix the estimate</b>, not the plan. Statistics first; hints "
     "last.",
   ],
   "footnote": "'Fix the estimate, not the plan' is the single most useful "
               "rule in query tuning."},
 ],
 "takeaways": [
   "External merge sort creates runs of B pages, then merges B−1 at a "
   "time. All I/O is sequential, and one merge pass is usually enough.",
   "Cost is 2N per pass with passes = 1 + log base (B−1). A gigabyte of "
   "buffer sorts a terabyte in two passes.",
   "Index nested loop wins when the outer is small and the inner is indexed "
   "— far more often than its reputation suggests.",
   "Sort-merge is free when an input is already sorted, and its sorted "
   "output may satisfy a later ORDER BY for nothing.",
   "Grace hash join partitions both inputs so matching rows share a "
   "partition, costing 3(M+N) — but only for equi-joins.",
   "Spilling is a cliff: when the memory estimate is wrong the cost jumps an "
   "order of magnitude. Fix the estimate, not the plan.",
 ],
 "notes": [
  ("h1", "1 &nbsp; External sorting"),
  ("p", "Sorting underlies ORDER BY, GROUP BY, DISTINCT, sort-merge join, "
        "and index construction. Doing it on data larger than memory is a "
        "foundational problem."),
  ("callout", "Two phases, both sequential",
   ["<b>Phase 1 — run generation.</b> Read B pages into the buffer "
    "pool, sort them in memory with any in-memory algorithm, and write the "
    "sorted result back out as a <i>run</i>. Repeat until the input is "
    "exhausted. This produces &lceil;N/B&rceil; sorted runs.",
    "<b>Phase 2 — merging.</b> Merge B&minus;1 runs simultaneously, "
    "using one buffer page as the input window for each run and one for "
    "output. When a run's buffer empties, read its next page. Repeat until "
    "one run remains.",
    "<b>Every I/O in both phases is sequential.</b> Runs are written "
    "sequentially and read sequentially; output is written sequentially. "
    "<b>This is the entire point</b> — Module 02 established that "
    "sequential access is 10 to 100 times faster, and this algorithm is "
    "constructed to use nothing else.",
    "<b>With a realistic buffer pool, one merge pass almost always "
    "suffices</b>, so the practical cost is 'read everything twice, write "
    "everything twice'."]),
  ("eq", "passes = 1 + &lceil;log<sub>B&minus;1</sub>(N/B)&rceil; "
         "&nbsp;&nbsp;&nbsp;&nbsp; total I/O = 2N &times; passes"),
  ("table", ["N (pages)", "B (buffer pages)", "Runs", "Passes", "Total I/O"],
   [["1,000", "100", "10", "2", "4,000"],
    ["10<super>6</super>", "1,000", "1,000", "2",
     "4 &times; 10<super>6</super>"],
    ["10<super>9</super>", "1,000", "10<super>6</super>", "3",
     "6 &times; 10<super>9</super>"],
    ["10<super>9</super>", "<b>10,000</b>", "10<super>5</super>",
     "<b>2</b>", "<b>4 &times; 10<super>9</super></b>"]],
   [0.20, 0.22, 0.18, 0.15, 0.25]),
  ("p", "<b>The base of the logarithm is the buffer size</b>, which is why "
        "memory helps so disproportionately here. At B = 1000 the logarithm "
        "has base 999, so sorting a terabyte takes two or three passes, not "
        "forty. Note the last two rows: ten times the memory removes an "
        "entire pass over a billion pages."),
  ("ul", ["<b>Replacement selection</b> generates runs averaging 2B pages "
          "rather than B, by keeping a heap in memory and emitting the "
          "smallest record still greater than the last one written. Fewer, "
          "longer runs mean a lower merge fanout requirement.",
          "<b>Double buffering</b> overlaps I/O with computation: while one "
          "buffer page is being merged, the next is being read. Without it "
          "the CPU idles through every read.",
          "<b>Skip the sort entirely</b> when a B+tree already provides the "
          "required order. Scanning an index is usually cheaper than sorting "
          "— and the optimiser must know this, which is Module 08's "
          "'interesting orders'.",
          "<b>Top-K for LIMIT.</b> <code>ORDER BY x LIMIT 10</code> does not "
          "need a sort; a bounded heap of ten elements over a single scan "
          "suffices, and the difference on a large table is enormous.",
          "<b>Normalised keys.</b> Encode the sort key as a byte string such "
          "that byte-wise comparison gives the correct order, then compare "
          "with <code>memcmp</code>. Once I/O is sequential, comparison cost "
          "dominates, and this is a large constant-factor win that the "
          "asymptotic analysis does not show."]),

  ("h1", "2 &nbsp; Joins"),
  ("table", ["Nested loop variant", "Cost", "Assessment"],
   [["<b>Naive (tuple-at-a-time)</b>",
     "M + (m &times; N) — scan the inner relation once per outer "
     "<i>row</i>.",
     "<b>Pathological.</b> Never correct; present only to motivate the "
     "others."],
    ["<b>Block nested loop</b>",
     "M + (M &times; N) — scan the inner once per outer <i>page</i>, "
     "or better, per block of buffer.",
     "Acceptable when the outer relation is small, and <b>the only option "
     "for a non-equi join</b> such as an inequality or a range overlap."],
    ["<b>Index nested loop</b>",
     "M + (m &times; cost of one index lookup).",
     "<b>Excellent when the outer relation is small and the inner is "
     "indexed on the join key.</b> This is the right plan far more often "
     "than its reputation suggests — it is the standard plan for OLTP "
     "queries that join a handful of rows to a large indexed table."]],
   [0.21, 0.35, 0.44]),
  ("callout", "Sort-merge join",
   ["Sort both inputs on the join key (&sect;1), then advance through them "
    "together in a single coordinated pass, emitting matches.",
    "<b>Cost is the two sorts plus M + N for the merge.</b> The sorts "
    "dominate.",
    "<b>Which makes it free when an input is already sorted</b> — "
    "because it arrived from a clustered index scan, or because an earlier "
    "sort-merge join in the same plan produced it in that order. The "
    "optimiser tracks this as an <b>interesting order</b> (Module 08), and "
    "it is why a plan may choose sort-merge over hash despite a higher "
    "local cost.",
    "<b>And the output is sorted</b>, which may satisfy a subsequent ORDER "
    "BY, GROUP BY, or merge join for nothing. Accounting for that benefit is "
    "one of the genuinely subtle parts of optimisation."]),
  ("code", """PHASE 1 -- PARTITION both relations by hash(join_key) % P
    R -> R0 R1 ... RP        S -> S0 S1 ... SP
    Matching rows now share a partition index.
    Cost: read and write both relations once.

PHASE 2 -- JOIN partition by partition
    for i in 0..P:
        build an in-memory hash table on Ri (the smaller side)
        probe it with every row of Si
    Cost: read both relations once.

TOTAL: 3(M + N)         EQUI-JOINS ONLY"""),
  ("p", "<b>Partitioning is what makes the second phase a single pass:</b> "
        "two rows can only join if their keys are equal, and equal keys hash "
        "to the same partition, so a row in R<sub>i</sub> can only match "
        "rows in S<sub>i</sub>. Each partition is sized to fit in memory, so "
        "each is joined with one in-memory hash table."),
  ("p", "<b>The restriction to equi-joins is fundamental.</b> A hash value "
        "tells you nothing about ordering, so hashing cannot help with "
        "<code>&lt;</code>, <code>&gt;</code>, or range overlap predicates. "
        "This is why sort-merge and block nested loop remain necessary."),
  ("table", ["Algorithm", "I/O cost", "Requires", "Best when"],
   [["<b>Index nested loop</b>", "M + m&middot;lookup",
     "An index on the inner join key.",
     "<b>Small outer, indexed inner.</b> The OLTP default."],
    ["<b>Block nested loop</b>", "M + M&middot;N", "Nothing.",
     "A very small outer relation, or a <b>non-equi join</b> where nothing "
     "else applies."],
    ["<b>Sort-merge</b>", "sorts + M + N", "An orderable join key.",
     "<b>An input is already sorted</b>, or the sorted output is wanted "
     "downstream."],
    ["<b>Hash</b>", "<b>3(M + N)</b>", "<b>An equi-join.</b>",
     "<b>Large unsorted inputs. The default for analytical work.</b>"]],
   [0.18, 0.16, 0.24, 0.42]),

  ("break",),
  ("h1", "3 &nbsp; When memory runs out"),
  ("callout", "Spilling is a cliff, not a slope",
   ["A hash join sizes its build-side hash table according to the "
    "optimiser's estimate of how many rows the build side will produce.",
    "<b>If that estimate is wrong — and Module 08 explains why it "
    "frequently is — the hash table does not fit in the memory "
    "allocated.</b> The join must then spill partitions to disk and process "
    "them in multiple batches.",
    "<b>The cost does not degrade smoothly. It jumps</b>, often by an order "
    "of magnitude, as soon as the threshold is crossed.",
    "<b>This is the usual explanation for a query that was fast last week "
    "and is slow today.</b> Nothing changed in the query; the table grew "
    "past the point where the estimate and the memory limit were still "
    "compatible, and the plan fell off the cliff.",
    "<b>Recursive partitioning handles the general case</b> — "
    "partition an oversized partition again — <b>but data skew can "
    "defeat it entirely.</b> If a single key value accounts for millions of "
    "rows, every one of them hashes to the same partition, and no amount of "
    "repartitioning separates them."]),
  ("ul", ["<b><code>EXPLAIN ANALYZE</code> shows estimated against actual "
          "row counts at every node.</b> A large discrepancy is the single "
          "most informative diagnostic available, and it is where every "
          "investigation should start.",
          "<b>Look for spills.</b> PostgreSQL reports <code>Batches: 4</code> "
          "on a hash join and disk usage on a sort. <b>More than one batch "
          "means the estimate was wrong</b> and the join is paying the "
          "cliff.",
          "<b>Look for a nested loop over a large outer relation.</b> This "
          "almost always indicates a cardinality underestimate — the "
          "optimiser chose nested loop because it expected a handful of "
          "rows.",
          "<b>Check for skew.</b> Query the distribution of the join key. "
          "One dominant value defeats hash partitioning and makes the "
          "estimated cost meaningless.",
          "<b>Then fix the estimate, not the plan.</b> Update statistics, "
          "add an extended statistics object for correlated columns, or "
          "rewrite the predicate so it can be estimated. <b>Hints are a last "
          "resort</b>, because they freeze a decision that was correct for "
          "today's data and will be wrong later — and unlike a bad "
          "estimate, a hint never corrects itself."]),
 ],
 "resources": [
   ("CMU 15-445 &mdash; Lectures 11–12, Sorting and Joins",
    "https://15445.courses.cs.cmu.edu/",
    "External sort, the three join families, and the cost analysis of "
    "&sect;2."),
   ("Graefe &mdash; Query Evaluation Techniques for Large Databases (free)",
    "https://dl.acm.org/doi/10.1145/152610.152611",
    "The comprehensive survey of sorting, hashing, and join processing. "
    "Dense, and still the reference."),
   ("Shapiro &mdash; Join Processing in Database Systems with Large Main "
    "Memories (free)",
    "https://dl.acm.org/doi/10.1145/6314.6315",
    "The Grace and hybrid hash join analysis of &sect;2."),
   ("PostgreSQL &mdash; Using EXPLAIN",
    "https://www.postgresql.org/docs/current/using-explain.html",
    "The diagnostic material in &sect;3, with worked examples. Read this "
    "before tuning anything."),
 ],
 "exercises": [
   "Implement external merge sort. Verify the I/O count against the formula "
   "for several values of N and B.",
   "Plot passes against buffer size for a fixed N and confirm the step "
   "structure predicted by the logarithm.",
   "Implement replacement selection and measure the average run length "
   "against the simple approach.",
   "Implement normalised keys for a multi-column sort and measure the "
   "speedup against comparator-based sorting.",
   "Implement block nested loop, index nested loop, sort-merge, and hash "
   "joins. Measure I/O for each on the same inputs.",
   "Find the crossover: at what outer-relation size does hash join overtake "
   "index nested loop on your data?",
   "Construct a non-equi join and confirm that only nested loop applies.",
   "<b>Demonstrate the spill cliff:</b> run a hash join with a work memory "
   "setting just large enough, then reduce it by 10% and measure the time "
   "difference.",
   "Construct a skewed join key where one value dominates, and show that "
   "recursive partitioning does not help.",
   "Take a slow query in PostgreSQL, read <code>EXPLAIN ANALYZE</code>, "
   "identify the estimation error, and fix it by improving statistics rather "
   "than by hinting.",
 ],
 "selfcheck": [
   "Describe the two phases of external merge sort and say why all I/O is "
   "sequential.",
   "Write the pass-count formula and explain why more memory helps so much.",
   "Name five refinements real sorts use.",
   "Give the three nested loop variants with their costs, and say when index "
   "nested loop wins.",
   "When is sort-merge join free, and what else does it provide?",
   "Explain Grace hash join and why partitioning makes phase 2 one pass.",
   "Why can hash join not handle inequality predicates?",
   "Why is spilling a cliff rather than a slope, and what causes it?",
   "What does skew do to a hash join, and why does repartitioning not help?",
   "What is the first thing to look at in EXPLAIN ANALYZE, and what should "
   "you fix?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Query Execution",
 "subtitle": "Turning a plan into rows, efficiently.",
 "question": "How does a query plan actually produce rows?",
 "outcomes": [
     "Explain the iterator model and its cost.",
     "Compare iterator, materialisation, and vectorised execution.",
     "Explain query compilation and when it pays.",
     "Explain pipeline breakers and why they matter.",
     "Reason about parallel query execution.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The iterator model",
   "blurb": "One interface, every operator."},

  {"t": "code", "kicker": "Volcano", "title": "Open, next, close",
   "lang": "cpp", "code": """
// Every operator implements the same three methods. A plan is a
// tree of them, and the root is pulled until it is exhausted.
struct Operator {
    virtual void  open()  = 0;
    virtual Tuple next()  = 0;   // returns one tuple, or EOF
    virtual void  close() = 0;
};

struct Filter : Operator {
    Operator* child;
    Expr*     pred;
    Tuple next() override {
        while (Tuple t = child->next())      // PULL from below
            if (pred->eval(t)) return t;
        return EOF;
    }
};

// while (Tuple t = root->next()) emit(t);
//
// Elegant, composable, and it makes ONE VIRTUAL CALL PER TUPLE
// PER OPERATOR. At a billion rows that is the dominant cost.
""",
   "caption": "The model is clean and the per-tuple virtual call is its "
              "undoing on analytical workloads.",
   "note": "Volcano's elegance is genuine. The criticism is purely about "
           "the constant factor at scale."},

  {"t": "callout", "title": "Pull-based execution has real advantages",
   "kind": "Why it lasted",
   "body": ["<b>Composable.</b> Any operator can be a child of any other, "
            "with no coordination.",
            "<b>Pipelined.</b> Tuples flow through without materialising "
            "intermediate results, so memory use is bounded.",
            "<b>Naturally lazy.</b> A LIMIT at the top simply stops pulling, "
            "and no operator below does unnecessary work.",
            "<b>And the per-tuple overhead is fine for OLTP</b>, where a "
            "query touches ten rows. <b>It is the analytical case — "
            "billions of rows — where it fails.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Beyond one tuple at a time",
   "blurb": "Two ways to amortise the overhead."},

  {"t": "table", "kicker": "Models", "title": "Three execution models",
   "header": ["Model", "Unit", "Good for", "Cost"],
   "widths": [2.6, 2.4, 3.6, 3.5],
   "rows": [
     ["<b>Iterator</b>", "One tuple", "<b>OLTP; low latency</b>", "Per-tuple call overhead"],
     ["Materialisation", "All tuples", "Small results; stored procs", "<b>Memory for everything</b>"],
     ["<b>Vectorised</b>", "<b>~1000 tuples</b>", "<b>OLAP; the modern default</b>", "Complexity; latency"],
   ],
   "footnote": "Vectorised is the standard choice for analytics and the "
               "reason column stores are fast.",
   "note": "Vectorisation is the single most important execution idea of "
           "the last twenty years."},

  {"t": "callout", "title": "Vectorised execution amortises everything",
   "kind": "Why batches of a thousand",
   "body": ["<b>One virtual call per thousand tuples</b> instead of per "
            "tuple. The dispatch cost effectively vanishes.",
            "<b>The inner loop becomes tight and branch-predictable</b>, and "
            "the compiler can auto-vectorise it into SIMD instructions.",
            "<b>A batch fits in L1 or L2 cache</b>, so the data is hot "
            "throughout the operation.",
            "<b>Typical speedups are 10–100× on analytical queries.</b> "
            "This is why column stores (Module 12) are fast, and the two "
            "ideas belong together."]},

  {"t": "callout", "title": "Compilation: generate code for the query",
   "kind": "The other approach",
   "body": ["Rather than interpreting a plan tree, <b>generate machine code "
            "specialised to this exact query</b> and run it.",
            "<b>No dispatch at all</b>, and the tuple layout is known at "
            "compile time, so field access is a constant offset.",
            "<b>The cost is compilation time</b> — milliseconds to tens of "
            "milliseconds, which is unacceptable for a query that runs in "
            "one.",
            "<b>So systems do both:</b> interpret short queries, compile "
            "long ones, and decide adaptively. HyPer compiles; DuckDB "
            "vectorises; several do both."]},

  {"t": "section", "label": "Part 3", "title": "Pipelines",
   "blurb": "Where the flow has to stop."},

  {"t": "callout", "title": "A pipeline breaker must see all its input",
   "kind": "The structural constraint",
   "body": ["<b>Pipelineable:</b> filter, projection, hash join probe side, "
            "index scan. A tuple goes in, a tuple comes out.",
            "<b>Breakers:</b> sort, aggregation, hash join <i>build</i> "
            "side, DISTINCT. <b>Nothing can be emitted until the last input "
            "tuple has arrived.</b>",
            "<b>Breakers determine memory use</b>, because they must "
            "accumulate. They are where spills happen (Module 06).",
            "<b>And they determine latency:</b> a plan with a sort at the "
            "top produces no rows at all until the sort completes, however "
            "small the LIMIT."]},

  {"t": "bullets", "kicker": "Consequences", "title": "What breakers imply for plans",
   "items": [
     "<b>Push breakers late.</b> A sort over fewer rows is cheaper; a filter "
     "below a sort is free.",
     "",
     "<b>A plan with no breakers streams</b> — constant memory, rows "
     "emitted immediately. The ideal for a LIMIT query.",
     "",
     "<b>The build side of a hash join is a breaker; the probe side is "
     "not.</b> This asymmetry is why the optimiser cares which input is "
     "which.",
     "",
     "<b>Top-K avoids the sort breaker</b> for LIMIT queries by keeping a "
     "bounded heap.",
     "",
     "<b>Count the breakers</b> to estimate a plan's memory and latency "
     "profile at a glance.",
   ],
   "note": "Build-versus-probe asymmetry is a good concrete reason the "
           "optimiser's join-order choice matters beyond cardinality."},

  {"t": "section", "label": "Part 4", "title": "Parallelism",
   "blurb": "Using more than one core."},

  {"t": "table", "kicker": "Kinds", "title": "Three kinds of parallelism",
   "header": ["Kind", "Means", "Note"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["<b>Intra-operator</b>", "Split data; run the same operator on each part", "<b>The important one</b>"],
     ["Inter-operator", "Different operators on different cores, pipelined", "Limited by pipeline depth"],
     ["Inter-query", "Different queries on different cores", "Trivial; always done"],
   ],
   "footnote": "Intra-operator parallelism is what makes a single large "
               "query fast; the others do not help one query much.",
   "note": "Students assume inter-operator is the main win. It is not — "
           "pipeline depth is small."},

  {"t": "callout", "title": "Morsel-driven parallelism",
   "kind": "The modern approach",
   "body": ["<b>Split the input into small chunks — morsels — and let "
            "worker threads pull them from a shared queue.</b>",
            "<b>Work-stealing handles skew automatically:</b> a thread that "
            "finishes early takes another morsel, so an uneven data "
            "distribution does not leave cores idle.",
            "<b>NUMA-aware:</b> prefer morsels whose data is local to the "
            "thread's socket.",
            "<b>It replaced static partitioning</b>, which divided work "
            "evenly in advance and therefore divided it badly whenever the "
            "data was skewed — which is always."]},

  {"t": "bullets", "kicker": "Limits", "title": "Why parallelism disappoints",
   "items": [
     "<b>Amdahl's law.</b> The serial fraction bounds the speedup, and "
     "there is always a serial fraction.",
     "",
     "<b>Memory bandwidth, not CPU, is usually the limit</b> for scans. "
     "More cores sharing the same bandwidth do not help.",
     "",
     "<b>Coordination costs</b> — exchanging tuples between threads is "
     "not free.",
     "",
     "<b>Skew</b> leaves cores idle, which is exactly what morsels fix.",
     "",
     "<b>And a parallel plan has startup cost</b>, so short queries are "
     "slower with it than without.",
   ],
   "footnote": "Memory bandwidth being the real limit is why column stores "
               "and compression matter so much (Module 12)."},
 ],
 "takeaways": [
   "The iterator model gives every operator open/next/close, which composes "
   "cleanly and costs one virtual call per tuple per operator.",
   "That overhead is fine for OLTP and fatal for analytics, where a query "
   "touches billions of rows.",
   "Vectorised execution processes batches of about a thousand tuples, "
   "amortising dispatch, enabling SIMD, and keeping data in cache — "
   "10–100&times; on analytics.",
   "Compilation generates code specialised to one query, eliminating "
   "dispatch entirely, at the cost of compile time that short queries cannot "
   "afford.",
   "Pipeline breakers — sort, aggregation, hash build — must see "
   "all input before emitting any, which determines a plan's memory and "
   "latency.",
   "Intra-operator parallelism is what speeds one query; morsel-driven "
   "scheduling with work stealing handles skew that static partitioning "
   "cannot.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The iterator model"),
  ("p", "The Volcano or iterator model, introduced by Graefe, gives every "
        "operator the same three-method interface. A query plan is a tree of "
        "such operators, and execution consists of repeatedly calling "
        "<code>next()</code> on the root."),
  ("code", """struct Operator {
    virtual void  open()  = 0;
    virtual Tuple next()  = 0;        // one tuple, or EOF
    virtual void  close() = 0;
};

struct Filter : Operator {
    Tuple next() override {
        while (Tuple t = child->next())      // PULL from below
            if (pred->eval(t)) return t;
        return EOF;
    }
};"""),
  ("callout", "Why the model lasted, and where it fails",
   ["<b>Composability.</b> Every operator presents the same interface, so "
    "any operator can be the child of any other with no coordination or "
    "special cases. New operators slot in without touching existing ones.",
    "<b>Pipelining.</b> Tuples flow from leaves to root without "
    "materialising intermediate results, so memory consumption is bounded "
    "by the plan's depth rather than by the data size.",
    "<b>Natural laziness.</b> A <code>LIMIT</code> at the top of the plan "
    "simply stops calling <code>next()</code>, and no operator below does "
    "any further work. Nothing special is required to make this happen.",
    "<b>And it makes one virtual call per tuple per operator.</b> For an "
    "OLTP query touching ten rows through four operators, that is forty "
    "calls — irrelevant. <b>For an analytical query over a billion "
    "rows it is four billion indirect calls</b>, each defeating branch "
    "prediction, and that becomes the dominant cost of the query."]),

  ("h1", "2 &nbsp; Beyond one tuple at a time"),
  ("table", ["Model", "Unit of work", "Suits", "Cost"],
   [["<b>Iterator (Volcano)</b>", "One tuple.",
     "<b>OLTP, and any query where latency to the first row matters.</b>",
     "One virtual call per tuple per operator."],
    ["<b>Materialisation</b>",
     "The entire output of each operator, computed at once.",
     "Small result sets; stored procedures; some embedded systems.",
     "<b>Every intermediate result must fit in memory.</b>"],
    ["<b>Vectorised</b>", "<b>A batch of roughly 1,000 tuples.</b>",
     "<b>OLAP. The modern default for analytics.</b>",
     "More complex operators; slightly worse latency to the first row."]],
   [0.18, 0.26, 0.31, 0.25]),
  ("callout", "Why batches of about a thousand",
   ["<b>Dispatch is amortised.</b> One virtual call per thousand tuples "
    "rather than per tuple reduces the overhead by three orders of "
    "magnitude, to the point where it no longer appears in a profile.",
    "<b>The inner loop becomes tight and predictable.</b> A loop over a "
    "thousand values of known type, with no indirect calls, is something the "
    "compiler can <b>auto-vectorise into SIMD instructions</b> — "
    "processing four, eight, or sixteen values per instruction.",
    "<b>A batch of a thousand values fits comfortably in L1 or L2 "
    "cache</b>, so the data stays hot through the whole operation. Larger "
    "batches would spill to a slower level and the benefit would reverse "
    "— which is why the number is around a thousand rather than a "
    "million.",
    "<b>The combined effect is 10 to 100 times on analytical queries.</b> "
    "This is the single most important execution idea of the last twenty "
    "years, and it is why column stores (Module 12) are fast: columnar "
    "storage supplies exactly the dense same-typed arrays that vectorised "
    "execution wants. <b>The two ideas belong together</b> and arriving at "
    "either tends to lead to the other."]),
  ("callout", "Compilation",
   ["The alternative is to stop interpreting the plan and instead "
    "<b>generate machine code specialised to this exact query</b>, then "
    "execute that.",
    "<b>There is no dispatch at all</b>, the tuple layout is known at code "
    "generation time so every field access is a constant offset, and the "
    "predicate is inlined rather than being an expression tree walked per "
    "row. The generated code resembles what a programmer would write by hand "
    "for this one query.",
    "<b>The cost is compilation time</b> — from a few milliseconds to "
    "tens of milliseconds depending on the approach. <b>For a query that "
    "would have run in one millisecond, that is a large regression.</b>",
    "<b>So systems do both and choose adaptively:</b> interpret short "
    "queries, compile long ones, and sometimes begin interpreting and switch "
    "to compiled code once the query proves to be long-running. HyPer "
    "compiles, DuckDB vectorises, and several systems combine the two."]),

  ("break",),
  ("h1", "3 &nbsp; Pipelines and breakers"),
  ("callout", "A pipeline breaker must consume all of its input first",
   ["<b>Pipelineable operators</b> — filter, projection, index scan, "
    "the probe side of a hash join — take a tuple and may produce a "
    "tuple. They hold essentially no state and pass data through.",
    "<b>Pipeline breakers</b> — sort, aggregation, DISTINCT, and the "
    "<i>build</i> side of a hash join — <b>cannot emit anything until "
    "they have seen their last input tuple.</b> A sort cannot know which row "
    "is first until it has seen all of them.",
    "<b>Breakers determine a plan's memory consumption</b>, because they "
    "must accumulate their entire input. They are therefore where spilling "
    "happens (Module 06 &sect;3), and where a cardinality misestimate turns "
    "into a cliff.",
    "<b>And they determine latency to the first row.</b> A plan with a sort "
    "near the top produces no output at all until the sort has completed, "
    "regardless of how small the LIMIT is — which is why a "
    "<code>LIMIT 10</code> query can take as long as the unlimited one."]),
  ("ul", ["<b>Push breakers as late as possible.</b> A sort over the output "
          "of a selective filter is far cheaper than a sort over the base "
          "table, so the optimiser pushes filters below sorts whenever "
          "semantics allow.",
          "<b>A plan with no breakers streams:</b> constant memory, and rows "
          "emitted as soon as they are found. This is the ideal shape for a "
          "LIMIT query and is worth recognising in an EXPLAIN output.",
          "<b>The build side of a hash join is a breaker and the probe side "
          "is not.</b> This asymmetry is a concrete reason the optimiser "
          "cares which relation is which, beyond their sizes — the "
          "choice determines where the plan stalls and how much memory it "
          "needs.",
          "<b>Top-K avoids the sort breaker.</b> <code>ORDER BY x LIMIT "
          "10</code> can be executed with a bounded ten-element heap over a "
          "single streaming pass, which is not a breaker in the memory "
          "sense and changes the plan's profile entirely.",
          "<b>Counting the breakers in a plan</b> gives you its memory and "
          "latency profile at a glance, which is a useful habit when reading "
          "EXPLAIN output."]),

  ("h1", "4 &nbsp; Parallelism"),
  ("table", ["Kind", "Mechanism", "Assessment"],
   [["<b>Intra-operator</b>",
     "Partition the data and run the same operator on each partition "
     "concurrently.",
     "<b>The one that matters.</b> This is what makes a single large query "
     "fast, and it scales with core count."],
    ["<b>Inter-operator</b>",
     "Run different operators of the same plan on different cores, passing "
     "tuples between them.",
     "<b>Limited by pipeline depth</b> — a plan has a handful of "
     "operators, so this caps out at a small speedup regardless of how many "
     "cores are available."],
    ["<b>Inter-query</b>", "Run different queries on different cores.",
     "Trivial, and every system does it. Does nothing for a single slow "
     "query."]],
   [0.17, 0.38, 0.45]),
  ("callout", "Morsel-driven parallelism",
   ["<b>Split the input into small chunks — morsels, typically tens of "
    "thousands of rows — and have worker threads pull them from a "
    "shared queue</b> as they become free.",
    "<b>Work stealing handles skew automatically.</b> A thread that finishes "
    "its morsel quickly simply takes another; a thread that gets an "
    "expensive morsel does not hold everyone up. No thread sits idle while "
    "another is still working.",
    "<b>It can be NUMA-aware:</b> prefer handing a thread a morsel whose "
    "data is resident on its own socket's memory, falling back to remote "
    "morsels only when local ones are exhausted.",
    "<b>It replaced static partitioning</b>, which divided the work evenly "
    "across threads in advance — and therefore divided it <i>badly</i> "
    "whenever the data was skewed, which is essentially always. The cost of "
    "a shared queue is far smaller than the cost of one thread doing three "
    "times its share."]),
  ("ul", ["<b>Amdahl's law bounds everything.</b> The serial fraction of a "
          "query — planning, final aggregation, result assembly "
          "— limits the achievable speedup regardless of core count, "
          "and there is always a serial fraction.",
          "<b>Memory bandwidth is usually the real limit for scans</b>, not "
          "CPU. Adding cores that share the same memory controller does not "
          "add bandwidth, so a scan-bound query stops improving well before "
          "the cores are saturated. <b>This is a large part of why column "
          "stores and compression matter so much</b> (Module 12): they "
          "reduce the bytes that must cross the bottleneck.",
          "<b>Coordination is not free.</b> Exchanging tuples between "
          "threads involves queues, synchronisation, and cache-line "
          "transfers between cores.",
          "<b>Skew leaves cores idle</b> under static partitioning, which is "
          "precisely what morsels address.",
          "<b>A parallel plan has startup cost</b> — launching workers, "
          "setting up exchanges — so short queries run <i>slower</i> "
          "in parallel. This is why systems have a cost threshold below "
          "which they do not parallelise at all."]),
 ],
 "resources": [
   ("CMU 15-445 &mdash; Lectures 13–14, Query Execution",
    "https://15445.courses.cs.cmu.edu/",
    "The iterator model, execution models, and parallelism. The primary "
    "source."),
   ("Graefe &mdash; Volcano, An Extensible and Parallel Query Evaluation "
    "System (free)",
    "https://dl.acm.org/doi/10.1109/69.273032",
    "The iterator model of &sect;1, in the original."),
   ("Boncz, Zukowski & Nes &mdash; MonetDB/X100: Hyper-Pipelining Query "
    "Execution (free)",
    "https://www.cidrdb.org/cidr2005/papers/P19.pdf",
    "The vectorised execution of &sect;2, and the paper that established "
    "it."),
   ("Neumann &mdash; Efficiently Compiling Efficient Query Plans for Modern "
    "Hardware (free)",
    "https://www.vldb.org/pvldb/vol4/p539-neumann.pdf",
    "Query compilation, from HyPer. The counterpoint to vectorisation."),
   ("Leis et al. &mdash; Morsel-Driven Parallelism (free)",
    "https://db.in.tum.de/~leis/papers/morsels.pdf",
    "The scheduling approach of &sect;4."),
 ],
 "exercises": [
   "Implement the iterator model with scan, filter, projection, and nested "
   "loop join operators. Run a query end to end.",
   "Profile it on a hundred million rows and measure what fraction of time "
   "is virtual dispatch.",
   "Implement vectorised versions of filter and projection operating on "
   "batches of 1024. Measure the speedup.",
   "Vary the batch size from 1 to 100,000 and plot throughput. Identify "
   "where cache effects take over.",
   "Confirm that the compiler auto-vectorises your batch filter by "
   "inspecting the generated assembly.",
   "Identify the pipeline breakers in five query plans from "
   "<code>EXPLAIN</code> and predict each plan's memory behaviour.",
   "Demonstrate the latency effect of a breaker: time to first row for a "
   "<code>LIMIT 1</code> query with and without an ORDER BY.",
   "Implement top-K for ORDER BY with LIMIT and compare against a full sort "
   "on a large table.",
   "Implement intra-operator parallelism for a scan with static "
   "partitioning. Then introduce skew and show cores going idle.",
   "Replace it with morsel-driven scheduling and show the skew handled.",
   "Measure scan throughput against thread count and identify where memory "
   "bandwidth becomes the limit.",
 ],
 "selfcheck": [
   "Describe the iterator interface and give three advantages of pull-based "
   "execution.",
   "Why does the iterator model fail on analytical workloads but not OLTP?",
   "Compare three execution models on unit of work, suitability, and cost.",
   "Give three reasons vectorised execution is faster, and say why the batch "
   "size is about a thousand.",
   "What does query compilation eliminate, what does it cost, and how do "
   "systems resolve that?",
   "What is a pipeline breaker? Give four examples and two consequences.",
   "Why is the build side of a hash join a breaker and the probe side not?",
   "Name three kinds of parallelism and say which matters for one slow "
   "query.",
   "What is morsel-driven parallelism and what does it fix?",
   "Give four reasons parallel query execution disappoints.",
 ],
},

]
