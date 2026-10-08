# -*- coding: utf-8 -*-
"""CSCE 608 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Query Optimisation",
 "subtitle": "Choosing a plan, and why the choice is often wrong.",
 "question": "How does a database decide how to run your query?",
 "outcomes": [
     "Explain the two stages of optimisation: rewriting and costing.",
     "Apply the standard algebraic rewrite rules.",
     "Explain selectivity estimation and why errors compound.",
     "Explain dynamic programming join enumeration.",
     "Diagnose a bad plan and identify the estimation error behind it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Rewriting",
   "blurb": "Transformations that are always good."},

  {"t": "table", "kicker": "Rewrites", "title": "Rules that need no cost model",
   "header": ["Rewrite", "Why it is always right"],
   "widths": [4.4, 7.7],
   "rows": [
     ["<b>Predicate pushdown</b>", "<b>Filter early; everything above does less work</b>"],
     ["Projection pushdown", "Drop unneeded columns as early as possible"],
     ["Constant folding", "<code>WHERE x &gt; 2+3</code> → <code>x &gt; 5</code>"],
     ["Subquery flattening", "<b>Turn a correlated subquery into a join</b>"],
     ["Join elimination", "Drop a join whose result is unused and provably 1:1"],
     ["<b>Predicate inference</b>", "<b>a=b and b=5 implies a=5 — now pushable to a's table</b>"],
   ],
   "footnote": "These are applied unconditionally because no plausible cost "
               "model prefers the unrewritten form.",
   "note": "Predicate inference is the one that surprises people — it can "
           "enable an index that was not obviously applicable."},

  {"t": "callout", "title": "Subquery flattening is the biggest single win",
   "kind": "Why it matters so much",
   "body": ["A correlated subquery is, naively, <b>executed once per outer "
            "row</b>. A million outer rows means a million executions.",
            "<b>Flattened into a join</b>, it executes once and the "
            "optimiser can choose a hash join over it.",
            "<b>This is often the difference between seconds and "
            "hours</b>, and it is invisible in the query text — the same "
            "SQL is fast on one system and slow on another depending on "
            "whether the optimiser flattens it.",
            "<b>Not every subquery can be flattened.</b> Ones involving "
            "<code>NOT EXISTS</code> with complex correlation, or "
            "aggregates with outer references, frequently cannot."]},

  {"t": "section", "label": "Part 2", "title": "Cost estimation",
   "blurb": "Where it all goes wrong."},

  {"t": "eq", "kicker": "Cardinality", "title": "The estimates and their assumptions",
   "eqs": [
     ("sel(a = c)  =  1 / distinct(a)",
      "Assumes UNIFORMITY — every value equally likely."),
     ("sel(p AND q)  =  sel(p) × sel(q)",
      "Assumes INDEPENDENCE — the two predicates are unrelated."),
     ("|R ⋈ S|  =  |R| × |S| / max(distinct_R, distinct_S)",
      "Assumes CONTAINMENT — the smaller key set is a subset of the "
      "larger."),
   ],
   "caption": "Three assumptions. Real data violates all three, "
              "routinely.",
   "note": "Naming the three assumptions explicitly is what lets students "
           "predict when the optimiser will be wrong."},

  {"t": "callout", "title": "Correlation is the assumption that breaks",
   "kind": "The classic example",
   "body": ["<code>WHERE city = 'Dallas' AND state = 'TX'</code>.",
            "<b>Independence says:</b> sel(city) × sel(state). If there "
            "are 10,000 cities and 50 states, that is 1/500,000.",
            "<b>Reality:</b> every row with city = Dallas already has state "
            "= TX. The true selectivity is 1/10,000 — <b>fifty times "
            "larger</b>.",
            "<b>So the optimiser expects 2 rows and gets 100</b>, chooses a "
            "nested loop, and the query is slow. <b>Extended statistics</b> "
            "on correlated column groups are the fix, and must be declared "
            "explicitly."]},

  {"t": "callout", "title": "Errors compound multiplicatively up the plan",
   "kind": "Why deep plans go badly wrong",
   "body": ["An error at a leaf feeds the estimate above it, which feeds the "
            "one above that.",
            "<b>A factor of 10 at each of four levels is a factor of "
            "10,000</b> at the top.",
            "<b>And underestimates are worse than overestimates</b>, "
            "because they lead to nested loops and undersized hash tables "
            "— both of which fail catastrophically rather than "
            "gracefully.",
            "<b>Leis et al.'s 'How Good Are Query Optimizers, Really?' "
            "measured this</b> and found estimates wrong by orders of "
            "magnitude on real schemas. It is the honest picture of the "
            "field."]},

  {"t": "bullets", "kicker": "Statistics", "title": "What the optimiser knows",
   "items": [
     "<b>Table and index row counts and page counts.</b> Cheap and usually "
     "accurate.",
     "",
     "<b>Histograms</b> per column — equi-depth is standard. Captures "
     "skew within a column.",
     "",
     "<b>Distinct value counts</b>, often estimated by HyperLogLog rather "
     "than computed exactly.",
     "",
     "<b>Most common values</b> with their frequencies, which handles the "
     "heavy-tail case histograms smooth over.",
     "",
     "<b>Correlation statistics</b> — only if you create them, in most "
     "systems. This is the gap.",
   ],
   "footnote": "Statistics are sampled and go stale. <code>ANALYZE</code> "
               "after a bulk load is not optional."},

  {"t": "section", "label": "Part 3", "title": "Plan enumeration",
   "blurb": "Searching a space that grows factorially."},

  {"t": "callout", "title": "System R's dynamic programming",
   "kind": "The 1979 algorithm still in use",
   "body": ["<b>The space is enormous:</b> n tables have "
            "(2n−2)!/(n−1)! join orders. At n=10 that is "
            "17 billion.",
            "<b>Build up by subset size:</b> find the best plan for every "
            "pair, then every triple using the best pairs, and so on. "
            "O(3&#8319;) rather than factorial.",
            "<b>Keep 'interesting orders' separately</b> — a more "
            "expensive plan that produces sorted output may win overall "
            "(Module 06).",
            "<b>Beyond 10–12 tables, switch to heuristics</b> "
            "— greedy, or genetic. Postgres switches at 12 by default."]},

  {"t": "two", "kicker": "Shapes", "title": "Left-deep and bushy plans",
   "lh": "Left-deep",
   "l": ["Each join's right input is a base table.",
         "<b>Fully pipelined</b> — one hash table at a time.",
         "Much smaller search space.",
         ("What System R considered, and most systems still do.", 1)],
   "rh": "Bushy",
   "r": ["Joins can take two join results as inputs.",
         "<b>Can be much better</b> for some schemas.",
         "<b>Far larger search space</b>, and more memory at once.",
         ("Analytical systems consider them; OLTP systems often do not.", 1)],
   "note": "The left-deep restriction is a real limitation that analytical "
           "workloads feel."},

  {"t": "section", "label": "Part 4", "title": "Diagnosis",
   "blurb": "What to do when the plan is bad."},

  {"t": "bullets", "kicker": "Method", "title": "Debugging a slow query, in order",
   "items": [
     "<b>1. EXPLAIN ANALYZE.</b> Compare estimated against actual rows at "
     "every node.",
     "<b>2. Find the deepest node with a large error.</b> Errors propagate "
     "upward, so fix the lowest one first.",
     "<b>3. Ask why that estimate is wrong.</b> Stale statistics? "
     "Correlation? A predicate the optimiser cannot estimate?",
     "<b>4. Fix the estimate.</b> ANALYZE, extended statistics, or rewrite "
     "the predicate.",
     "<b>5. Only then consider hints</b> — and know you are freezing a "
     "decision that will be wrong later.",
     "",
     "<b>Fix the estimate, not the plan.</b>",
   ],
   "note": "Step 2 is the one people skip. They fix the top-level symptom "
           "and the real error is three levels down."},

  {"t": "callout", "title": "Why optimisers are worse than you would hope",
   "kind": "An honest assessment",
   "body": ["<b>Cardinality estimation is the hard part</b>, and it has not "
            "been solved in fifty years of effort.",
            "<b>Cost models are approximations</b> of hardware they were "
            "calibrated against years ago, and SSDs changed the "
            "constants.",
            "<b>The search space is too large to explore exhaustively</b>, "
            "so heuristics cut it, and the heuristics are sometimes wrong.",
            "<b>Learned optimisers are an active research area</b> and are "
            "not yet dependable. <b>Meanwhile, the practical skill is "
            "reading plans and fixing estimates</b>, which is a skill rather "
            "than a workaround."]},
 ],
 "takeaways": [
   "Optimisation has two stages: rewrites that are always beneficial, and "
   "cost-based choice among plans that is not.",
   "Subquery flattening turns one-execution-per-outer-row into a join and is "
   "often the difference between seconds and hours.",
   "Estimation rests on uniformity, independence, and containment — and "
   "real data violates all three routinely.",
   "Correlated predicates are the classic failure: city and state look "
   "independent and are not, producing errors of fifty times or more.",
   "Errors compound multiplicatively up the plan, and underestimates are "
   "worse because they produce nested loops and undersized hash tables.",
   "Find the deepest node with a large estimation error and fix the "
   "estimate, not the plan. Hints freeze a decision that will later be "
   "wrong.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Rewriting"),
  ("p", "Optimisation has two distinct stages. The first applies "
        "transformations that are beneficial regardless of the data, so no "
        "cost model is consulted. The second chooses among alternatives "
        "whose relative cost depends on the data, and that is where the "
        "difficulty is."),
  ("table", ["Rewrite", "Example and justification"],
   [["<b>Predicate pushdown</b>",
     "Move filters as close to the base tables as the semantics allow. "
     "<b>Every operator above then processes fewer rows</b>, and no "
     "plausible cost model prefers the alternative."],
    ["<b>Projection pushdown</b>",
     "Drop columns as soon as they are no longer needed. Narrower tuples "
     "mean more rows per page and less memory in every breaker."],
    ["<b>Constant folding</b>",
     "<code>WHERE x &gt; 2 + 3</code> becomes <code>WHERE x &gt; 5</code>, "
     "so the arithmetic is done once rather than per row — and the "
     "constant can then be compared against a histogram."],
    ["<b>Subquery flattening</b>",
     "<b>Turn a correlated subquery into a join.</b> See below."],
    ["<b>Join elimination</b>",
     "If a join's result columns are unused and the join is provably "
     "one-to-one via a foreign key, the join can be removed entirely. "
     "Common with views and ORMs that join more than the query needs."],
    ["<b>Predicate inference</b>",
     "From <code>a = b</code> and <code>b = 5</code>, infer <code>a = "
     "5</code>. <b>The inferred predicate can then be pushed down to a's "
     "table and may enable an index that was not obviously applicable</b> "
     "— which surprises people and is genuinely valuable."]],
   [0.21, 0.79]),
  ("callout", "Subquery flattening is often the largest single win",
   ["A correlated subquery, executed naively, <b>runs once for every row of "
    "the outer query</b>. A million outer rows means a million executions of "
    "the inner query, each with its own setup and its own index lookups.",
    "<b>Flattened into a join, it executes once</b>, and the optimiser can "
    "then choose a hash join, reorder it with other joins, and push "
    "predicates through it.",
    "<b>This is routinely the difference between seconds and hours</b>, and "
    "it is entirely invisible in the query text. The same SQL can be fast on "
    "one system and pathological on another purely according to whether that "
    "system's optimiser recognises and flattens the pattern.",
    "<b>Not everything can be flattened.</b> <code>NOT EXISTS</code> with "
    "complex correlation, aggregates referencing outer columns, and "
    "subqueries in the SELECT list with side conditions frequently resist "
    "it. When performance matters and a subquery is hot, checking the plan "
    "for whether flattening occurred is worth the two minutes."]),

  ("h1", "2 &nbsp; Cost estimation"),
  ("p", "To compare plans the optimiser must estimate how many rows each "
        "operator will produce. <b>Cardinality estimation is the hard part "
        "of query optimisation</b>, and the rest of the machinery is "
        "comparatively straightforward."),
  ("table", ["Estimate", "Formula", "Assumption"],
   [["Equality selectivity", "1 / distinct(a)",
     "<b>Uniformity</b> — every distinct value occurs equally often."],
    ["Conjunction", "sel(p) &times; sel(q)",
     "<b>Independence</b> — the two predicates are statistically "
     "unrelated."],
    ["Join size",
     "|R| &times; |S| / max(distinct<sub>R</sub>, distinct<sub>S</sub>)",
     "<b>Containment</b> — the smaller key set is a subset of the "
     "larger."]],
   [0.22, 0.34, 0.44]),
  ("p", "<b>Real data violates all three, routinely.</b> Naming the "
        "assumptions explicitly is what lets you predict where the optimiser "
        "will go wrong, which is more useful than any individual tuning "
        "trick."),
  ("callout", "Correlation is the assumption that breaks most often",
   ["Consider <code>WHERE city = 'Dallas' AND state = 'TX'</code>.",
    "<b>The independence assumption computes</b> sel(city) &times; "
    "sel(state). With 10,000 distinct cities and 50 states, that is "
    "1/10,000 &times; 1/50 = 1/500,000.",
    "<b>The truth is that every row with city = Dallas already has state = "
    "TX.</b> The state predicate adds no selectivity at all, so the real "
    "figure is 1/10,000 — <b>fifty times larger than estimated</b>.",
    "<b>So the optimiser expects two rows and receives a hundred.</b> "
    "Expecting two, it chooses an index nested loop; receiving a hundred, "
    "that choice is fifty times more expensive than the hash join it "
    "rejected. <b>Extended statistics</b> — declared on correlated "
    "column groups — are the fix in PostgreSQL and SQL Server, and "
    "<b>they must be created explicitly</b>: no system discovers "
    "correlations on its own."]),
  ("callout", "Errors compound multiplicatively",
   ["An estimate at a leaf feeds the estimate of the operator above it, "
    "which feeds the one above that. The errors multiply rather than "
    "averaging out.",
    "<b>A factor of ten at each of four levels is a factor of ten thousand "
    "at the top of the plan.</b> This is why deep plans over many tables go "
    "wrong far more dramatically than simple ones.",
    "<b>And underestimates are considerably worse than "
    "overestimates.</b> An underestimate leads the optimiser to choose a "
    "nested loop (which is catastrophic at scale) and to size a hash table "
    "too small (which spills, per Module 06). An overestimate leads it to "
    "choose a hash join and allocate generously — wasteful, but it "
    "degrades gracefully.",
    "<b>Leis et al.'s 'How Good Are Query Optimizers, Really?' measured "
    "this on real schemas</b> and found estimates wrong by orders of "
    "magnitude as a routine matter, with errors growing sharply with the "
    "number of joins. It is the honest picture of where the field stands, "
    "and it is worth reading rather than assuming the textbook account "
    "describes practice."]),
  ("ul", ["<b>Table and index cardinalities and page counts.</b> Cheap to "
          "maintain and usually accurate.",
          "<b>Histograms</b>, typically equi-depth, capturing the "
          "distribution within a column. These handle skew that the "
          "uniformity assumption misses.",
          "<b>Distinct value counts</b>, frequently estimated with "
          "HyperLogLog rather than computed exactly, because an exact count "
          "requires a sort or a hash of the whole column.",
          "<b>Most common values and their frequencies</b>, stored "
          "separately from the histogram. This handles the heavy tail that "
          "equi-depth buckets smooth over — a value occurring in 30% of "
          "rows deserves its own entry.",
          "<b>Correlation statistics — only if you create them.</b> "
          "This is the gap in every system, and it is the gap that "
          "&sect;2's example falls into.",
          "<b>And all of it is sampled and goes stale.</b> Running "
          "<code>ANALYZE</code> after a bulk load is not optional; a table "
          "that the optimiser believes is empty will be planned as though it "
          "were."]),

  ("break",),
  ("h1", "3 &nbsp; Plan enumeration"),
  ("callout", "System R's dynamic programming, from 1979 and still in use",
   ["<b>The search space is enormous.</b> The number of join orders for n "
    "tables is (2n&minus;2)!/(n&minus;1)!. At n = 10 that is roughly 17 "
    "billion orderings, before considering which algorithm to use for each "
    "join or which access path for each table.",
    "<b>Dynamic programming builds up by subset size.</b> Find the best plan "
    "for every single table, then the best for every pair (using the "
    "single-table plans), then every triple (using the pair plans), and so "
    "on. <b>This is O(3&#8319;) rather than factorial</b> — still "
    "exponential, and vastly smaller.",
    "<b>Interesting orders are tracked separately.</b> A plan that is more "
    "expensive but produces output sorted on a useful column may win "
    "overall, because it saves a sort later (Module 06 &sect;2). So the "
    "algorithm keeps the cheapest plan for each distinct useful ordering, "
    "not just the cheapest plan overall. <b>This refinement is what makes "
    "sort-merge joins choosable at all.</b>",
    "<b>Beyond about 10 to 12 tables the exponential cost becomes "
    "unacceptable</b>, and systems switch to heuristics — greedy "
    "selection, or PostgreSQL's genetic algorithm, which kicks in at twelve "
    "tables by default."]),
  ("table", ["", "Left-deep plans", "Bushy plans"],
   [["Shape", "Every join's right input is a base table, so the tree leans "
     "entirely one way.",
     "A join may take two join results as its inputs."],
    ["Pipelining", "<b>Fully pipelined</b> — one hash table is built "
     "at a time, and the rest streams.",
     "Multiple hash tables may be live simultaneously, so memory "
     "consumption is higher."],
    ["Search space", "<b>Much smaller</b> — n! orderings rather than "
     "the full count.", "<b>Far larger.</b>"],
    ["Who considers them",
     "System R did, and most OLTP-oriented optimisers still restrict to "
     "them.",
     "<b>Analytical systems consider bushy plans</b>, because star and "
     "snowflake schemas have genuinely better bushy solutions. The "
     "left-deep restriction is a real limitation there."]],
   [0.15, 0.42, 0.43]),

  ("h1", "4 &nbsp; Diagnosing a bad plan"),
  ("ol", ["<b>Run <code>EXPLAIN ANALYZE</code></b> and compare estimated "
          "against actual row counts at every node. This single comparison "
          "resolves most investigations.",
          "<b>Find the <i>deepest</i> node with a large error.</b> Errors "
          "propagate upward, so a wildly wrong estimate at the root is often "
          "the consequence of a modest error three levels down. <b>This is "
          "the step people skip</b>, and fixing the top-level symptom while "
          "the real error remains is why tuning sessions go in circles.",
          "<b>Ask why that estimate is wrong.</b> Stale statistics? "
          "Correlated predicates? A predicate form the optimiser cannot "
          "estimate at all — a function call, a parameter it cannot "
          "see, a LIKE pattern?",
          "<b>Fix the estimate.</b> Run <code>ANALYZE</code>; create "
          "extended statistics on the correlated columns; rewrite the "
          "predicate into a form that can be estimated; or add the column to "
          "an index so its distribution is known.",
          "<b>Only then consider hints or plan pinning</b> — and "
          "understand that you are freezing a decision that is correct for "
          "today's data volume and distribution. <b>A bad estimate corrects "
          "itself when statistics are refreshed; a hint never does.</b>"]),
  ("p", "<b>Fix the estimate, not the plan.</b> This is the single most "
        "useful rule in query tuning, and it is the one most often "
        "violated."),
  ("callout", "Why optimisers are worse than you would hope",
   ["<b>Cardinality estimation is unsolved.</b> Fifty years of sustained "
    "effort have produced steady improvement and no general solution, "
    "because estimating the size of an arbitrary predicate's result over "
    "arbitrary correlated data is genuinely hard.",
    "<b>Cost models are approximations of hardware</b> — and often "
    "hardware they were calibrated against years ago. The default constants "
    "in several systems still encode assumptions about the relative cost of "
    "sequential and random I/O that SSDs invalidated.",
    "<b>The search space cannot be explored exhaustively</b> beyond a dozen "
    "tables, so heuristics prune it, and the heuristics are sometimes wrong "
    "in ways nothing detects.",
    "<b>Learned optimisers — using machine learning for cardinality "
    "estimation or plan selection — are an active research area</b> "
    "with promising results and are not yet dependable in production, "
    "particularly on queries unlike their training data.",
    "<b>So the practical skill is reading plans and fixing estimates</b>, "
    "and that is a genuine engineering skill rather than a workaround for "
    "an immature system. It will remain necessary."]),
 ],
 "resources": [
   ("CMU 15-445 &mdash; Lectures 15–16, Query Planning and Optimization",
    "https://15445.courses.cs.cmu.edu/",
    "Rewrites, cost estimation, and System R enumeration."),
   ("Selinger et al. &mdash; Access Path Selection in a Relational Database "
    "Management System (1979, free)",
    "https://people.csail.mit.edu/tdanford/6830papers/selinger-access-path.pdf",
    "The System R paper. Dynamic programming join enumeration and "
    "interesting orders, in the original. Still worth reading."),
   ("Leis et al. &mdash; How Good Are Query Optimizers, Really? (free)",
    "https://www.vldb.org/pvldb/vol9/p204-leis.pdf",
    "The measurement study behind &sect;2's honest assessment. Read it."),
   ("PostgreSQL &mdash; planner statistics and extended statistics",
    "https://www.postgresql.org/docs/current/planner-stats.html",
    "What the optimiser knows and how to give it more, including the "
    "correlation fix in &sect;2."),
   ("Use The Index, Luke &mdash; execution plan chapters",
    "https://use-the-index-luke.com/sql/explain-plan",
    "Reading plans across several database systems."),
 ],
 "exercises": [
   "Write a query with a filter above a join. Use <code>EXPLAIN</code> to "
   "confirm the optimiser pushes it below, and construct a case where it "
   "cannot.",
   "Write a correlated subquery over a large table. Check whether your "
   "system flattens it, and compare timings against the hand-written join.",
   "Construct the correlation example from &sect;2 with real data. Report "
   "estimated and actual rows, then add extended statistics and report "
   "again.",
   "Build a four-join query and record the estimation error at each level. "
   "Confirm the errors compound.",
   "Delete the statistics on a table and show how the plan changes. Then "
   "<code>ANALYZE</code> and show it change back.",
   "Count the join orders for 5, 10, and 15 tables, and confirm the "
   "factorial growth that motivates dynamic programming.",
   "Construct a query where a more expensive sorted plan wins overall "
   "because it avoids a later sort. Confirm with EXPLAIN.",
   "Force PostgreSQL to use its genetic optimiser by exceeding the join "
   "threshold, and compare plan quality and planning time against dynamic "
   "programming.",
   "<b>Take a genuinely slow query</b>, apply the five-step method of "
   "&sect;4, and document each step and what it revealed.",
   "Apply a hint to fix a plan, then change the data volume by 100&times; "
   "and show the hint is now wrong.",
 ],
 "selfcheck": [
   "Name the two stages of optimisation and say why only one needs a cost "
   "model.",
   "Give six algebraic rewrites and say why each is unconditionally "
   "applied.",
   "Why is subquery flattening so valuable, and when does it fail?",
   "State the three estimation assumptions and give a formula for each.",
   "Work through the city/state correlation example with numbers.",
   "Why do estimation errors compound, and why are underestimates worse?",
   "Name five kinds of statistics and say which one systems do not "
   "maintain automatically.",
   "Describe System R's enumeration and explain interesting orders.",
   "Compare left-deep and bushy plans on four axes.",
   "Give the five steps for diagnosing a bad plan, and the rule that "
   "summarises them.",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Transactions and Concurrency Control",
 "subtitle": "ACID, and what each letter actually costs.",
 "question": "What does a transaction guarantee, and how?",
 "outcomes": [
     "State the ACID properties precisely.",
     "Define conflict serializability and test for it.",
     "Implement two-phase locking and explain why it works.",
     "Explain deadlock detection and prevention.",
     "Name the anomalies each isolation level permits.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "ACID",
   "blurb": "Four properties, four different mechanisms."},

  {"t": "table", "kicker": "ACID", "title": "What each letter means and costs",
   "header": ["Property", "Guarantees", "Mechanism", "Module"],
   "widths": [2.3, 4.0, 3.2, 2.6],
   "rows": [
     ["<b>Atomicity</b>", "All or nothing", "<b>Logging, undo</b>", "11"],
     ["<b>Consistency</b>", "Constraints hold", "<b>The application's job</b>", "—"],
     ["<b>Isolation</b>", "As if run alone", "<b>Locking or MVCC</b>", "<b>09, 10</b>"],
     ["<b>Durability</b>", "Survives a crash", "<b>WAL, fsync</b>", "11"],
   ],
   "footnote": "<b>C is the odd one out.</b> It is largely the "
               "application's responsibility; the database enforces only "
               "declared constraints.",
   "note": "Worth saying plainly: C was arguably included to make the "
           "acronym work."},

  {"t": "callout", "title": "Consistency is not the database's job",
   "kind": "An honest note on the acronym",
   "body": ["<b>A, I, and D are implemented by specific mechanisms</b> you "
            "can point at: the log, the lock manager, fsync.",
            "<b>C is different.</b> The database enforces declared "
            "constraints — keys, foreign keys, checks — and nothing "
            "else.",
            "<b>'The balance must never be negative' is enforced only if "
            "you declare it.</b> Otherwise consistency means whatever the "
            "application maintains.",
            "<b>Härder and Reuter coined ACID in 1983</b>, and the C is "
            "widely regarded as having been included partly because the "
            "acronym needed it."]},

  {"t": "section", "label": "Part 2", "title": "Serializability",
   "blurb": "The correctness criterion."},

  {"t": "callout", "title": "Serializable means equivalent to <i>some</i> serial order",
   "kind": "The definition",
   "body": ["A concurrent schedule is <b>serializable</b> if its effect is "
            "the same as executing the transactions one after another in "
            "<i>some</i> order.",
            "<b>Not necessarily the order they arrived in.</b> Any serial "
            "order will do.",
            "<b>Conflict serializability</b> is the testable version: two "
            "operations conflict if they touch the same item and at least "
            "one is a write.",
            "<b>Build the conflict graph</b> — an edge from T₁ to T₂ when "
            "T₁ has an earlier conflicting operation. <b>Acyclic means "
            "serializable.</b>"]},

  {"t": "table", "kicker": "Anomalies", "title": "What goes wrong without isolation",
   "header": ["Anomaly", "What happens"],
   "widths": [3.4, 8.7],
   "rows": [
     ["<b>Dirty read</b>", "Read data another transaction wrote and then rolled back"],
     ["Non-repeatable read", "Read the same row twice; it changed in between"],
     ["<b>Phantom</b>", "<b>Re-run a range query; new rows appeared</b>"],
     ["Lost update", "Two read-modify-writes; one is silently overwritten"],
     ["<b>Write skew</b>", "<b>Each transaction's write is fine; together they break an invariant</b>"],
   ],
   "footnote": "Phantoms need predicate or range locks — locking the "
               "rows that exist is not enough.",
   "note": "Write skew is the one snapshot isolation permits and people do "
           "not expect."},

  {"t": "section", "label": "Part 3", "title": "Two-phase locking",
   "blurb": "The classical answer."},

  {"t": "code", "kicker": "2PL", "title": "The protocol",
   "lang": "text", "code": """
  GROWING PHASE:    may acquire locks, may NOT release any
  SHRINKING PHASE:  may release locks, may NOT acquire any

  Once a transaction releases its first lock, it may never
  acquire another. That single rule guarantees conflict
  serializability.

  STRICT 2PL:  hold ALL locks until commit or abort.
     Also prevents CASCADING ABORTS -- nobody can have read
     uncommitted data, because the writer held its lock.
     *** This is what real systems implement. ***

  Lock modes:         S (shared, read)   X (exclusive, write)
     S/S compatible.  Everything else conflicts.
""",
   "caption": "Strict 2PL is universal in practice: plain 2PL permits "
              "cascading aborts, which are a much worse problem than holding "
              "locks slightly longer.",
   "note": "The cascading abort argument is why nobody implements basic "
           "2PL. Make it explicit."},

  {"t": "callout", "title": "Deadlock: detect or prevent",
   "kind": "Two strategies",
   "body": ["<b>Detection:</b> maintain a waits-for graph and look for "
            "cycles, periodically. On a cycle, abort a victim — usually "
            "the youngest, or the one with least work done.",
            "<b>Prevention by timestamp:</b> each transaction has an age. "
            "<b>Wait-die</b> — an older transaction waits, a younger one "
            "aborts. <b>Wound-wait</b> — an older one aborts the younger "
            "holder.",
            "<b>Both prevention schemes abort transactions that would not "
            "actually have deadlocked</b>, which is the cost of avoiding "
            "the graph.",
            "<b>Most systems detect</b>, because deadlocks are rare and "
            "needless aborts are not free. Timeouts are the crude "
            "fallback."]},

  {"t": "callout", "title": "Phantoms need more than row locks",
   "kind": "The subtle failure",
   "body": ["T₁ runs <code>SELECT count(*) WHERE age &gt; 30</code> and "
            "locks the rows it found.",
            "<b>T₂ inserts a new row with age 35.</b> It is not locked "
            "— it did not exist when T₁ looked.",
            "<b>T₁ re-runs the query and gets a different count.</b> Not "
            "serializable, and no row lock was violated.",
            "<b>The fixes:</b> predicate locks (correct, impractical), "
            "<b>index-range or next-key locks</b> (practical, what systems "
            "do), or table locks (correct and brutal)."]},

  {"t": "section", "label": "Part 4", "title": "Isolation levels",
   "blurb": "Weaker guarantees, traded for throughput."},

  {"t": "table", "kicker": "Levels", "title": "The SQL isolation levels",
   "header": ["Level", "Dirty read", "Non-repeatable", "Phantom"],
   "widths": [3.6, 2.8, 2.9, 2.8],
   "rows": [
     ["Read uncommitted", "<b>Possible</b>", "Possible", "Possible"],
     ["<b>Read committed</b>", "No", "<b>Possible</b>", "Possible"],
     ["Repeatable read", "No", "No", "<b>Possible</b>"],
     ["<b>Serializable</b>", "No", "No", "No"],
   ],
   "footnote": "<b>The standard defines levels by which anomalies they "
               "forbid</b>, which is a poor definition — it omits "
               "write skew entirely.",
   "note": "That the standard is defined by anomaly list rather than by "
           "guarantee is a real and consequential flaw."},

  {"t": "callout", "title": "The isolation levels are not what you think",
   "kind": "Three things that surprise people",
   "body": ["<b>The default is usually Read Committed</b>, not serializable "
            "— in PostgreSQL, Oracle, and SQL Server. Most applications "
            "have never run serializably.",
            "<b>Names differ from behaviour.</b> Oracle's 'serializable' is "
            "snapshot isolation, which is weaker and permits write skew.",
            "<b>The standard's definition is by anomaly list</b>, and the "
            "list is incomplete — Berenson et al.'s 'A Critique of ANSI "
            "SQL Isolation Levels' makes the case.",
            "<b>So: find out what your system actually provides</b>, by "
            "testing, rather than reading the level name."]},
 ],
 "takeaways": [
   "Atomicity, isolation, and durability have specific mechanisms. "
   "Consistency is largely the application's responsibility.",
   "Serializable means equivalent to <i>some</i> serial order, not the "
   "arrival order. Conflict serializability is testable by an acyclic "
   "conflict graph.",
   "Two-phase locking's single rule — never acquire after releasing "
   "— guarantees serializability; strict 2PL also prevents cascading "
   "aborts.",
   "Deadlock is detected with a waits-for graph or prevented by timestamp "
   "ordering; prevention aborts transactions that would not have "
   "deadlocked.",
   "Phantoms are not prevented by row locks, because the offending row did "
   "not exist. Index-range locks are the practical fix.",
   "The default isolation level is usually Read Committed, names differ from "
   "behaviour, and the standard's anomaly-list definition omits write skew.",
 ],
 "notes": [
  ("h1", "1 &nbsp; ACID"),
  ("table", ["Property", "Guarantee", "Mechanism"],
   [["<b>Atomicity</b>",
     "A transaction's effects are all applied or none are. A failure "
     "mid-transaction leaves no partial effect.",
     "<b>Logging and undo</b> (Module 11)."],
    ["<b>Consistency</b>",
     "The database moves from one valid state to another.",
     "<b>Largely the application's responsibility.</b> See below."],
    ["<b>Isolation</b>",
     "Concurrent transactions produce the same result as if they had run one "
     "at a time.",
     "<b>Locking (this module) or multi-versioning</b> (Module 10)."],
    ["<b>Durability</b>",
     "Once committed, the effects survive any subsequent crash.",
     "<b>Write-ahead logging and fsync</b> (Module 11)."]],
   [0.17, 0.48, 0.35]),
  ("callout", "Consistency is the odd one out",
   ["Atomicity, isolation, and durability are each implemented by a specific "
    "mechanism you can point to in the source: the log, the lock manager, "
    "the fsync call.",
    "<b>Consistency is not.</b> The database enforces the constraints you "
    "have <i>declared</i> — primary keys, foreign keys, uniqueness, "
    "check constraints — and nothing beyond them.",
    "<b>'An account balance must never be negative' is enforced only if you "
    "declare it as a check constraint.</b> Otherwise consistency means "
    "whatever invariants the application happens to maintain, and the "
    "database has no opinion.",
    "<b>H&auml;rder and Reuter coined the acronym in 1983</b>, building on "
    "Gray's earlier work, and the C is widely regarded as having been "
    "included partly because the acronym required a vowel. This is not a "
    "criticism of the concept — consistency matters enormously — "
    "but of its presentation as a database-provided guarantee alongside "
    "three that genuinely are."]),

  ("h1", "2 &nbsp; Serializability"),
  ("callout", "The correctness criterion",
   ["A concurrent schedule is <b>serializable</b> if its effect is "
    "equivalent to executing the same transactions one after another, in "
    "<i>some</i> serial order.",
    "<b>Not necessarily the order in which they arrived.</b> Any serial "
    "order counts, which is what makes the criterion achievable: we are not "
    "required to reproduce a particular outcome, only <i>an</i> outcome that "
    "could have arisen from running them one at a time.",
    "<b>Conflict serializability</b> is the practically testable version. "
    "Two operations <b>conflict</b> if they are from different transactions, "
    "touch the same data item, and at least one is a write. "
    "Read&ndash;read does not conflict; read&ndash;write, write&ndash;read, "
    "and write&ndash;write do.",
    "<b>Build the conflict graph:</b> a node per transaction, and an edge "
    "from T&#8321; to T&#8322; whenever T&#8321; has an operation that "
    "conflicts with and precedes one of T&#8322;'s. <b>The schedule is "
    "conflict serializable if and only if that graph is acyclic</b>, and a "
    "topological sort of it gives the equivalent serial order."]),
  ("table", ["Anomaly", "Scenario"],
   [["<b>Dirty read</b>",
     "T&#8321; writes a row, T&#8322; reads it, T&#8321; rolls back. "
     "T&#8322; has read a value that never existed."],
    ["<b>Non-repeatable read</b>",
     "T&#8321; reads a row, T&#8322; updates and commits, T&#8321; reads "
     "the same row again and sees different data."],
    ["<b>Phantom</b>",
     "<b>T&#8321; runs a range query, T&#8322; inserts a row matching the "
     "range, T&#8321; re-runs the query and sees an extra row.</b> &sect;3."],
    ["<b>Lost update</b>",
     "T&#8321; and T&#8322; both read a value, both compute a new one from "
     "it, both write. One update is silently overwritten — the classic "
     "'read-modify-write' bug."],
    ["<b>Write skew</b>",
     "<b>Each transaction reads a set, checks an invariant, and writes a "
     "different row. Each write is individually valid; together they violate "
     "the invariant.</b> The classic case: two doctors each check that at "
     "least one other doctor is on call, and both go off call. <b>Snapshot "
     "isolation permits this</b> (Module 10) and people do not expect it."]],
   [0.21, 0.79]),

  ("h1", "3 &nbsp; Two-phase locking"),
  ("code", """GROWING PHASE:    may acquire locks, may NOT release any
SHRINKING PHASE:  may release locks, may NOT acquire any

Once a transaction releases its first lock, it may never acquire
another. That one rule guarantees conflict serializability.

STRICT 2PL: hold ALL locks until commit or abort.
   Also prevents CASCADING ABORTS.   <-- what real systems do

Lock modes:  S (shared/read)   X (exclusive/write)
             S/S compatible; everything else conflicts."""),
  ("callout", "Why strict 2PL rather than basic 2PL",
   ["Basic two-phase locking is sufficient for serializability: the "
    "growing/shrinking rule alone guarantees an acyclic conflict graph.",
    "<b>But it permits cascading aborts.</b> If T&#8321; releases a lock "
    "after writing but before committing, T&#8322; can read that value. If "
    "T&#8321; then aborts, T&#8322; has read data that never existed and "
    "must abort too — along with anything that read from T&#8322;.",
    "<b>Strict 2PL holds every lock until commit or abort</b>, so no "
    "transaction can ever read uncommitted data and the cascade is "
    "impossible. It also makes recovery simpler, because an abort never "
    "requires undoing other transactions.",
    "<b>The cost is holding locks slightly longer</b>, which reduces "
    "concurrency. <b>Every real system accepts that trade</b>, because a "
    "cascading abort is a far worse problem than a marginally lower "
    "concurrency ceiling — it is unbounded in scope and arrives at "
    "unpredictable times."]),
  ("table", ["Deadlock strategy", "Mechanism", "Cost"],
   [["<b>Detection</b>",
     "Maintain a waits-for graph and search it for cycles periodically. On "
     "finding one, abort a victim — usually the youngest transaction, "
     "or the one that has done least work.",
     "<b>The usual choice.</b> Deadlocks are rare, so the periodic check is "
     "cheap and no transaction is aborted unnecessarily."],
    ["<b>Prevention: wait-die</b>",
     "Each transaction carries a timestamp. If an <i>older</i> transaction "
     "needs a lock held by a younger one, it waits. If a <i>younger</i> one "
     "needs a lock held by an older, it aborts immediately.",
     "<b>Aborts transactions that would not actually have deadlocked</b>, "
     "which is the price of never building the graph."],
    ["<b>Prevention: wound-wait</b>",
     "The reverse: an older transaction <i>aborts</i> the younger holder and "
     "takes the lock; a younger one waits.",
     "Same cost. Favours older transactions, so long transactions make "
     "progress — which wait-die does not guarantee as strongly."],
    ["<b>Timeout</b>",
     "Abort anything that has waited too long.",
     "Crude. Aborts transactions that were merely slow, and tuning the "
     "threshold is guesswork."]],
   [0.20, 0.44, 0.36]),
  ("callout", "Phantoms require more than locking the rows that exist",
   ["T&#8321; executes <code>SELECT count(*) FROM people WHERE age &gt; "
    "30</code> and takes a shared lock on every row it found.",
    "<b>T&#8322; inserts a new row with age 35.</b> That row was not locked "
    "— it did not exist when T&#8321; looked, so there was nothing to "
    "lock.",
    "<b>T&#8321; re-runs its query and gets a different count.</b> The "
    "schedule is not serializable, and yet no lock was violated. <b>The "
    "problem is that the lock protects rows, and the query's semantics are "
    "about a <i>predicate</i></b> — which covers rows that do not yet "
    "exist.",
    "<b>The fixes, in order of practicality:</b> <b>predicate locks</b>, "
    "which lock the condition itself, are correct and impractical — "
    "testing whether two arbitrary predicates overlap is undecidable in "
    "general. <b>Index-range or next-key locks</b> lock the gaps between "
    "index entries, preventing insertion into a scanned range; this is "
    "approximate, practical, and what real systems implement. <b>Table "
    "locks</b> are correct, simple, and destroy concurrency."]),

  ("break",),
  ("h1", "4 &nbsp; Isolation levels"),
  ("table", ["Level", "Dirty read", "Non-repeatable read", "Phantom"],
   [["<b>Read uncommitted</b>", "<b>Possible</b>", "Possible", "Possible"],
    ["<b>Read committed</b>", "Prevented", "<b>Possible</b>", "Possible"],
    ["<b>Repeatable read</b>", "Prevented", "Prevented", "<b>Possible</b>"],
    ["<b>Serializable</b>", "Prevented", "Prevented", "Prevented"]],
   [0.28, 0.24, 0.26, 0.22]),
  ("callout", "Three things about isolation levels that surprise people",
   ["<b>The default is almost never serializable.</b> PostgreSQL, Oracle, "
    "and SQL Server all default to Read Committed; MySQL's InnoDB defaults "
    "to Repeatable Read. <b>Most applications have never run under "
    "serializable isolation</b> and their developers are generally unaware "
    "of it.",
    "<b>The names do not reliably describe the behaviour.</b> Oracle's "
    "SERIALIZABLE is in fact snapshot isolation, which is strictly weaker "
    "and permits write skew (Module 10). PostgreSQL's REPEATABLE READ is "
    "also snapshot isolation. The level name is a historical label, not a "
    "specification.",
    "<b>The standard's definition is by anomaly list, and the list is "
    "incomplete.</b> Defining a level by which of three named anomalies it "
    "forbids says nothing about anomalies not on the list — and "
    "<b>write skew is not on the list</b>. Berenson, Bernstein, Gray, "
    "Melton, O'Neil and O'Neil's 'A Critique of ANSI SQL Isolation Levels' "
    "makes this case in detail and is worth reading.",
    "<b>So: determine empirically what your system provides</b>, by writing "
    "the transactions that would exhibit each anomaly and observing what "
    "happens. The level name will not tell you, and Project 2 asks for "
    "exactly this demonstration."]),
 ],
 "resources": [
   ("CMU 15-445 &mdash; Lectures 17–18, Transactions and Two-Phase "
    "Locking",
    "https://15445.courses.cs.cmu.edu/",
    "ACID, serializability theory, 2PL, and deadlock handling."),
   ("Berenson et al. &mdash; A Critique of ANSI SQL Isolation Levels (free)",
    "https://www.microsoft.com/en-us/research/publication/"
    "a-critique-of-ansi-sql-isolation-levels/",
    "The &sect;4 argument, from the people who built these systems. Short "
    "and important."),
   ("Gray & Reuter &mdash; Transaction Processing: Concepts and Techniques",
    "https://www.google.com/books/edition/_/VkUAQwAACAAJ",
    "The standard reference. Not free, and in most university libraries; "
    "Gray's individual papers are free and cover much of it."),
   ("Martin Kleppmann &mdash; Designing Data-Intensive Applications, "
    "chapter 7",
    "https://dataintensive.net/",
    "The clearest modern explanation of isolation levels and the anomalies, "
    "with real incident examples."),
   ("Jepsen &mdash; consistency model analyses (free)",
    "https://jepsen.io/consistency",
    "Empirical testing of what systems actually provide against what they "
    "claim. The practical counterpart to &sect;4's advice."),
 ],
 "exercises": [
   "Write schedules exhibiting each of the five anomalies in &sect;2 and "
   "reproduce each one in a real database at an appropriate isolation level.",
   "Build conflict graphs for five schedules by hand and determine "
   "serializability. Verify your answers by reasoning about the outcomes.",
   "Implement a lock manager with shared and exclusive modes and a wait "
   "queue.",
   "Implement strict 2PL on top of it. Demonstrate that it prevents each of "
   "the anomalies.",
   "Demonstrate a cascading abort under basic (non-strict) 2PL, then show "
   "strict 2PL preventing it.",
   "Implement deadlock detection with a waits-for graph. Construct a "
   "deadlock and confirm detection and victim selection.",
   "Implement wait-die and wound-wait. Measure the needless abort rate "
   "against detection on the same workload.",
   "<b>Demonstrate a phantom:</b> run a range query twice with an insert in "
   "between, under repeatable read. Then enable serializable and show it "
   "prevented.",
   "Determine your database's actual isolation behaviour by testing rather "
   "than reading the manual. Report any discrepancy with the level name.",
   "Measure throughput against concurrency level under 2PL and identify "
   "where lock contention begins to dominate.",
 ],
 "selfcheck": [
   "State the four ACID properties with their mechanisms, and say which is "
   "the odd one out and why.",
   "Define serializability and conflict serializability, and give the test.",
   "Name five anomalies and describe each.",
   "State the two-phase locking rule and say what it guarantees.",
   "Why do real systems use strict 2PL rather than basic 2PL?",
   "Compare deadlock detection with the two prevention schemes.",
   "Why do row locks not prevent phantoms, and what does?",
   "Name the four isolation levels and the anomalies each permits.",
   "Give three reasons the isolation level names are misleading.",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Multi-Version Concurrency Control",
 "subtitle": "Readers that never block, and the garbage they create.",
 "question": "How do you let readers and writers run at the same time?",
 "outcomes": [
     "Explain how MVCC makes readers non-blocking.",
     "Explain snapshot isolation and what it permits.",
     "Explain write skew and why snapshot isolation allows it.",
     "Explain version storage and garbage collection.",
     "Explain serializable snapshot isolation.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The idea",
   "blurb": "Keep old versions instead of blocking."},

  {"t": "callout", "title": "Readers do not block writers; writers do not block readers",
   "kind": "The central property",
   "body": ["Under 2PL, a long-running read holds shared locks and blocks "
            "every writer touching the same rows. <b>One analytical query "
            "can stall an entire OLTP system.</b>",
            "<b>MVCC keeps multiple versions of each row.</b> A writer "
            "creates a new version; readers continue to see the old one.",
            "<b>So no reader ever waits for a writer, and no writer ever "
            "waits for a reader.</b> Only writer-writer conflicts remain.",
            "<b>That single property is why MVCC won</b>, and it is why "
            "PostgreSQL, Oracle, MySQL InnoDB, and SQL Server's snapshot "
            "mode all use it."]},

  {"t": "code", "kicker": "Versions", "title": "How a version is identified",
   "lang": "text", "code": """
  Each ROW VERSION carries:
      xmin   -- the transaction that CREATED this version
      xmax   -- the transaction that DELETED it (or none)

  Each TRANSACTION carries a SNAPSHOT at its start:
      xmin_snapshot   -- oldest still-running transaction
      xmax_snapshot   -- next id to be assigned
      in_progress[]   -- ids running at snapshot time

  A VERSION IS VISIBLE to a transaction if:
      xmin committed BEFORE the snapshot was taken,  AND
      xmax is unset, or committed AFTER the snapshot

  So a transaction sees a consistent picture of the database
  as it was at one instant -- regardless of what has happened
  since, and without taking a single read lock.
""",
   "caption": "Visibility is computed per row from the snapshot. No locks "
              "are involved in reading at all.",
   "note": "This is PostgreSQL's scheme specifically. Others differ in "
           "where versions live, not in the principle."},

  {"t": "section", "label": "Part 2", "title": "Snapshot isolation",
   "blurb": "What MVCC naturally provides, and what it permits."},

  {"t": "callout", "title": "Snapshot isolation is not serializable",
   "kind": "The thing to understand",
   "body": ["Each transaction reads from a consistent snapshot and writes "
            "are checked for conflict at commit — first committer wins.",
            "<b>This prevents dirty reads, non-repeatable reads, phantoms, "
            "and lost updates.</b> Everything on the SQL standard's list.",
            "<b>And it is still not serializable</b>, because the standard's "
            "list is incomplete (Module 09).",
            "<b>It permits write skew</b>, which is not on the list and "
            "which real applications hit."]},

  {"t": "code", "kicker": "Write skew", "title": "The on-call example",
   "lang": "text", "code": """
  INVARIANT: at least one doctor must remain on call.
  Initially Alice and Bob are both on call.

  T1 (Alice):                      T2 (Bob):
    SELECT count(*) WHERE on_call    SELECT count(*) WHERE on_call
      -> 2, so it is safe to leave     -> 2, so it is safe to leave
    UPDATE alice SET on_call=false   UPDATE bob SET on_call=false
    COMMIT                           COMMIT

  Both snapshots saw 2. Neither wrote a row the other wrote,
  so there is NO WRITE-WRITE CONFLICT to detect.
  Both commit. Nobody is on call. The invariant is broken.

  *** No serial order produces this outcome. ***
""",
   "caption": "Each transaction's write is individually valid. The conflict "
              "is between one transaction's <i>read</i> and the other's "
              "<i>write</i>, which snapshot isolation does not check.",
   "note": "This example is from the Berenson critique and is the clearest "
           "one. Students need to see that no serial order gives it."},

  {"t": "callout", "title": "Serializable snapshot isolation",
   "kind": "The fix",
   "body": ["Cahill et al., 2008. <b>Track read-write dependencies between "
            "concurrent transactions</b>, not just write-write.",
            "<b>Abort when a dangerous structure appears</b> — a "
            "particular pattern of two consecutive rw-dependencies that is "
            "necessary for a non-serializable cycle.",
            "<b>Optimistic:</b> no locks taken for reading, and the check "
            "happens at commit.",
            "<b>PostgreSQL implements this as SERIALIZABLE since 9.1.</b> "
            "It gives true serializability with MVCC's non-blocking reads, "
            "at the cost of some false-positive aborts."]},

  {"t": "section", "label": "Part 3", "title": "Versions and garbage",
   "blurb": "The cost side of MVCC."},

  {"t": "two", "kicker": "Storage", "title": "Where the old versions live",
   "lh": "Append-only (Postgres)",
   "l": ["New versions written into the table itself.",
         "<b>Old versions occupy table pages</b> until vacuumed.",
         "<b>Every index must point at every version</b> — writes are "
         "expensive.",
         ("Table bloat is the characteristic problem.", 1)],
   "rh": "Delta / rollback segment (Oracle, MySQL)",
   "r": ["Current version in place; <b>old versions in a separate undo "
         "area</b>.",
         "The table stays compact.",
         "<b>Reading an old version means following a chain</b> through the "
         "undo log.",
         ("'Snapshot too old' when undo space is exhausted.", 1)],
   "note": "Postgres's choice is why VACUUM exists and is the most "
           "operationally consequential design decision in it."},

  {"t": "callout", "title": "A long transaction holds back garbage collection",
   "kind": "The operational trap",
   "body": ["A version can only be removed once <b>no running transaction "
            "could still need to see it</b>.",
            "<b>So one transaction open for hours pins every version "
            "created since it started</b> — across the entire database, "
            "not just the tables it touched.",
            "<b>The table bloats, scans get slower, and nothing identifies "
            "the cause</b> except noticing the old transaction.",
            "<b>This is the single most common MVCC operational "
            "problem.</b> An idle-in-transaction connection — often an "
            "application that forgot to commit — is the usual culprit."]},

  {"t": "bullets", "kicker": "Cost", "title": "What MVCC costs",
   "items": [
     "<b>Space.</b> Multiple versions of everything, until collected.",
     "",
     "<b>Garbage collection.</b> VACUUM in Postgres, purge threads "
     "elsewhere. Real CPU and I/O.",
     "",
     "<b>Index bloat.</b> In an append-only design, every version needs "
     "index entries.",
     "",
     "<b>Visibility checks on every row read</b> — a small but "
     "unavoidable per-row cost.",
     "",
     "<b>Transaction ID wraparound</b> in systems with bounded ID space. "
     "Postgres's 32-bit counter must be managed or the database shuts "
     "down.",
   ],
   "note": "Wraparound is a genuine production hazard and worth naming."},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "When each approach is right."},

  {"t": "table", "kicker": "Comparison", "title": "2PL and MVCC",
   "header": ["", "Two-phase locking", "MVCC"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Readers", "<b>Block writers</b>", "<b>Never block anything</b>"],
     ["Space", "Minimal", "<b>Multiple versions</b>"],
     ["Long reads", "<b>Catastrophic for writers</b>", "Harmless to writers"],
     ["Write conflicts", "Detected by locking", "Detected at commit"],
     ["Default level", "Serializable achievable", "<b>Usually snapshot</b>"],
     ["Used by", "DB2, older systems", "<b>Postgres, Oracle, InnoDB</b>"],
   ],
   "footnote": "MVCC won for OLTP. The reason is entirely the first row.",
   "note": "Worth being direct: this is not close, and the reason is "
           "non-blocking reads."},

  {"t": "callout", "title": "Optimistic concurrency control",
   "kind": "The third option",
   "body": ["<b>Run without any locks</b>, record what was read and "
            "written, and validate at commit: did anything I read change?",
            "<b>Excellent when conflicts are rare</b> — no locking "
            "overhead at all, and no deadlocks.",
            "<b>Terrible when they are common</b> — work is done and then "
            "discarded, repeatedly, and throughput can collapse under "
            "contention.",
            "<b>Used in in-memory systems</b> where transactions are "
            "microseconds long, and in application-level patterns like "
            "version-column checks."]},
 ],
 "takeaways": [
   "MVCC keeps multiple row versions so readers never block writers and "
   "writers never block readers — which is why it won for OLTP.",
   "Visibility is computed per row from a transaction's snapshot, with no "
   "read locks taken at all.",
   "Snapshot isolation prevents every anomaly on the SQL standard's list and "
   "is still not serializable, because the list omits write skew.",
   "Write skew arises when each transaction's write is individually valid; "
   "the conflict is read-write, which snapshot isolation does not check.",
   "Serializable snapshot isolation tracks read-write dependencies and "
   "aborts on a dangerous structure — PostgreSQL's SERIALIZABLE.",
   "One long-running transaction pins every version created since it "
   "started, across the whole database. It is the commonest MVCC "
   "operational problem.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The idea"),
  ("callout", "Readers never block writers; writers never block readers",
   ["Under two-phase locking, a long-running read holds shared locks for its "
    "entire duration, and every writer touching those rows waits. <b>A "
    "single analytical query can stall an entire transactional "
    "workload</b>, which is intolerable for a system that must serve both.",
    "<b>MVCC keeps multiple versions of each row.</b> A writer does not "
    "overwrite; it creates a new version. Readers continue to see whichever "
    "version was current when they began.",
    "<b>So no reader ever waits for a writer, and no writer ever waits for a "
    "reader.</b> Only writer&ndash;writer conflicts need resolving, and "
    "those are comparatively rare.",
    "<b>That single property is why MVCC became dominant.</b> PostgreSQL, "
    "Oracle, MySQL's InnoDB, SQL Server's snapshot mode, and essentially "
    "every modern system use it — and the reason is this paragraph, not "
    "any subtler advantage."]),
  ("code", """Each ROW VERSION carries:
    xmin  -- transaction that CREATED this version
    xmax  -- transaction that DELETED it (or none)

Each TRANSACTION takes a SNAPSHOT at start:
    xmin_snapshot, xmax_snapshot, in_progress[]

A VERSION IS VISIBLE if:
    xmin committed BEFORE the snapshot was taken, AND
    xmax is unset, or committed AFTER the snapshot"""),
  ("p", "Visibility is therefore computed per row, from the reading "
        "transaction's snapshot, with <b>no locks taken for reading at "
        "all</b>. A transaction sees a consistent picture of the database as "
        "it was at one instant, regardless of everything that has happened "
        "since. (The scheme above is PostgreSQL's; other systems differ in "
        "where versions are stored, not in the principle.)"),

  ("h1", "2 &nbsp; Snapshot isolation"),
  ("callout", "Snapshot isolation is not serializability",
   ["What MVCC naturally provides is <b>snapshot isolation</b>: each "
    "transaction reads from a consistent snapshot taken at its start, and "
    "write&ndash;write conflicts are resolved at commit time by first "
    "committer wins.",
    "<b>This prevents every anomaly on the SQL standard's list</b> — "
    "dirty reads, non-repeatable reads, phantoms — and lost updates "
    "too.",
    "<b>And it is still not serializable</b>, because, as Module 09 "
    "established, the standard's list is incomplete.",
    "<b>It permits write skew</b>, which is not on the list, which real "
    "applications encounter, and which is the subject of the next page."]),
  ("code", """INVARIANT: at least one doctor must remain on call.
Initially Alice and Bob are both on call.

T1 (Alice):                       T2 (Bob):
  SELECT count(*) WHERE on_call     SELECT count(*) WHERE on_call
    -> 2, safe to leave               -> 2, safe to leave
  UPDATE alice SET on_call = false  UPDATE bob SET on_call = false
  COMMIT                            COMMIT

Both snapshots saw 2.  Neither wrote a row the other wrote,
so there is NO write-write conflict to detect.  Both commit.
Nobody is on call."""),
  ("callout", "Why snapshot isolation cannot catch this",
   ["<b>Each transaction's write is individually valid.</b> At the moment "
    "T&#8321; decided, two doctors were on call, so Alice leaving was "
    "correct. The same was true for T&#8322;.",
    "<b>And there is no write&ndash;write conflict.</b> T&#8321; wrote "
    "Alice's row; T&#8322; wrote Bob's. They touched disjoint data, so the "
    "first-committer-wins check finds nothing to complain about.",
    "<b>The conflict is between one transaction's <i>read</i> and the "
    "other's <i>write</i></b> — T&#8321; read Bob's row and T&#8322; "
    "wrote it, and vice versa. <b>Snapshot isolation does not track "
    "read&ndash;write dependencies at all</b>, so it cannot see the "
    "problem.",
    "<b>And no serial order produces this outcome.</b> Run T&#8321; first "
    "and T&#8322; sees one doctor on call and does not leave. Run T&#8322; "
    "first and the same. The concurrent execution produced a state that no "
    "sequential execution could, which is precisely the definition of "
    "non-serializable."]),
  ("callout", "Serializable snapshot isolation",
   ["Cahill, R&ouml;hm and Fekete, 2008. The insight is that a "
    "non-serializable execution under snapshot isolation always contains a "
    "particular structure: <b>two consecutive read&ndash;write "
    "dependencies</b> between concurrent transactions, forming part of a "
    "cycle.",
    "<b>So track read&ndash;write dependencies</b> — not just the "
    "write&ndash;write ones snapshot isolation already checks — and "
    "abort a transaction when this 'dangerous structure' appears.",
    "<b>It remains optimistic:</b> no locks are taken for reading, readers "
    "still never block, and the check happens at commit. The only cost is "
    "tracking the dependencies and some <b>false-positive aborts</b>, since "
    "the structure is necessary for a cycle but not sufficient.",
    "<b>PostgreSQL has implemented this as its SERIALIZABLE level since "
    "9.1.</b> It provides genuine serializability while keeping MVCC's "
    "non-blocking reads, which was widely assumed to be impossible, and it "
    "is one of the more satisfying results in the field."]),

  ("break",),
  ("h1", "3 &nbsp; Version storage and garbage"),
  ("table", ["", "Append-only (PostgreSQL)", "Delta / undo (Oracle, InnoDB)"],
   [["Where versions live", "New versions are written into the table's own "
     "pages.",
     "The current version stays in place; old versions go to a separate undo "
     "or rollback segment."],
    ["Table size", "<b>Grows with every update</b> until vacuumed. Table "
     "bloat is the characteristic problem.",
     "Stays compact."],
    ["Index maintenance",
     "<b>Every index must have an entry for every version</b>, so an update "
     "touching one column still writes to every index. Expensive. (HOT "
     "updates mitigate this when no indexed column changes.)",
     "Indexes point at the row's fixed location, so only indexes on changed "
     "columns are touched."],
    ["Reading an old version", "It is in the table; visibility is checked in "
     "place.",
     "<b>Follow a chain through the undo log</b>, applying deltas backwards. "
     "A long chain makes an old snapshot slow to read."],
    ["Characteristic failure", "<b>Bloat, and VACUUM not keeping up.</b>",
     "<b>'Snapshot too old'</b> when the undo segment is exhausted and old "
     "versions have been discarded."]],
   [0.16, 0.42, 0.42]),
  ("callout", "A long transaction pins every version in the database",
   ["A version can only be reclaimed once <b>no running transaction could "
    "still need to see it</b> — which means once the oldest active "
    "snapshot is newer than the version's deletion.",
    "<b>So a single transaction left open for hours prevents the collection "
    "of every version created since it began</b> — across the entire "
    "database, not merely the tables that transaction touched, because the "
    "collector cannot know what it might read next.",
    "<b>The table bloats, sequential scans read more pages, the buffer pool "
    "fills with dead rows, and nothing in the symptoms points at the "
    "cause.</b> Performance degrades gradually across the whole system.",
    "<b>This is the most common MVCC operational problem by a wide "
    "margin</b>, and the usual culprit is a connection sitting "
    "<code>idle in transaction</code> — an application that opened a "
    "transaction, did some work, and then went off to do something slow "
    "without committing. Monitoring for long-running transactions is not "
    "optional on an MVCC system."]),
  ("ul", ["<b>Space.</b> Multiple versions of everything, until collected.",
          "<b>Garbage collection.</b> PostgreSQL's VACUUM, InnoDB's purge "
          "threads. This is real CPU and I/O, competing with the workload, "
          "and it must be tuned.",
          "<b>Index bloat</b> in append-only designs, where every version "
          "needs index entries.",
          "<b>A visibility check on every row read.</b> Small per row, and "
          "unavoidable, and it adds up on a large scan.",
          "<b>Transaction ID wraparound.</b> PostgreSQL's transaction "
          "counter is 32 bits. Because visibility is determined by "
          "comparing IDs, the counter wrapping would make old rows appear to "
          "be in the future and vanish. VACUUM must 'freeze' old rows before "
          "this happens, and <b>if it falls far enough behind, PostgreSQL "
          "refuses new transactions to protect the data</b>. This is a real "
          "production hazard, it has taken down large sites, and it is a "
          "direct consequence of the design choice in this section."]),

  ("h1", "4 &nbsp; Choosing"),
  ("table", ["", "Two-phase locking", "MVCC"],
   [["<b>Readers</b>", "<b>Block writers</b> on the same rows.",
     "<b>Never block anything.</b>"],
    ["Space overhead", "Minimal — just the lock table.",
     "<b>Multiple versions of every updated row</b>, plus collection."],
    ["Long-running reads", "<b>Catastrophic</b> — they hold locks for "
     "their whole duration.",
     "Harmless to writers; harmful only through delayed garbage "
     "collection."],
    ["Write conflicts", "Detected when the lock is requested.",
     "Detected at commit — so work may be discarded."],
    ["Default isolation", "Serializable is achievable at reasonable cost.",
     "<b>Usually snapshot isolation</b>, with true serializability "
     "available at extra cost."],
    ["Used by", "DB2 and older systems.",
     "<b>PostgreSQL, Oracle, MySQL InnoDB, SQL Server snapshot mode.</b>"]],
   [0.16, 0.40, 0.44]),
  ("callout", "Optimistic concurrency control, the third option",
   ["<b>Run the transaction with no locks at all</b>, recording what was "
    "read and what was written. At commit, validate: has anything this "
    "transaction read been modified since it was read? If so, abort and "
    "retry; otherwise, commit.",
    "<b>Excellent when conflicts are rare.</b> No locking overhead, no lock "
    "table, no deadlock detection, and no blocking of any kind.",
    "<b>Terrible when conflicts are common.</b> Work is performed and then "
    "discarded, repeatedly, and under heavy contention throughput can "
    "collapse — transactions spend all their time doing work that is "
    "thrown away, and the situation is self-reinforcing because retries add "
    "load.",
    "<b>It is used in in-memory systems</b>, where transactions complete in "
    "microseconds so the conflict window is tiny, and in application-level "
    "patterns — the 'version column' check in ORMs is optimistic "
    "concurrency control under another name."]),
 ],
 "resources": [
   ("CMU 15-445 &mdash; Lecture 19, Multi-Version Concurrency Control",
    "https://15445.courses.cs.cmu.edu/",
    "Version storage, visibility, and garbage collection across real "
    "systems."),
   ("Wu et al. &mdash; An Empirical Evaluation of In-Memory MVCC (free)",
    "https://www.vldb.org/pvldb/vol10/p781-Wu.pdf",
    "A systematic comparison of version storage schemes and their costs. The "
    "source for &sect;3's table."),
   ("Cahill, R&ouml;hm & Fekete &mdash; Serializable Isolation for Snapshot "
    "Databases (free)",
    "https://dl.acm.org/doi/10.1145/1620585.1620587",
    "SSI, which became PostgreSQL's SERIALIZABLE. The dangerous-structure "
    "argument is clearer in the original."),
   ("PostgreSQL documentation &mdash; Concurrency Control and Routine "
    "Vacuuming",
    "https://www.postgresql.org/docs/current/mvcc.html",
    "The implementation in &sect;1 and &sect;3, including wraparound and "
    "what to monitor."),
   ("Kleppmann &mdash; Designing Data-Intensive Applications, chapter 7",
    "https://dataintensive.net/",
    "Write skew explained with more real examples, including ones that "
    "caused incidents."),
 ],
 "exercises": [
   "Implement MVCC visibility checking with xmin, xmax, and snapshots. "
   "Verify a reader sees a consistent snapshot while writers proceed.",
   "Demonstrate non-blocking reads: start a long read and confirm writers "
   "are not delayed. Repeat under 2PL and measure the difference.",
   "<b>Reproduce the write skew example</b> in PostgreSQL at REPEATABLE "
   "READ. Then set SERIALIZABLE and show one transaction aborts.",
   "Construct two more write skew scenarios from an application domain you "
   "know.",
   "Measure table bloat: update one column of a million-row table a hundred "
   "times and report the table size before VACUUM and after.",
   "Open a transaction and leave it idle. Run a heavy update workload and "
   "measure the bloat the idle transaction causes.",
   "Query <code>pg_stat_activity</code> for long-running transactions and "
   "write a monitoring query you would actually deploy.",
   "Measure the false-positive abort rate of SSI on a workload that is "
   "genuinely serializable.",
   "Implement optimistic concurrency control and measure throughput against "
   "contention level, identifying where it collapses.",
   "Compare 2PL, snapshot isolation, and SSI on the same workload: "
   "throughput, abort rate, and the anomalies each permits.",
 ],
 "selfcheck": [
   "What is MVCC's central property, and why did it win?",
   "How is version visibility determined, and what locks are involved in "
   "reading?",
   "What does snapshot isolation prevent, and why is it still not "
   "serializable?",
   "Work through the write skew example and explain why no conflict is "
   "detected.",
   "What does serializable snapshot isolation track, and what does it cost?",
   "Compare append-only and delta version storage on five axes.",
   "Why does one long transaction cause database-wide bloat?",
   "Give five costs of MVCC, including the one that can halt a database.",
   "When is optimistic concurrency control appropriate, and when does it "
   "collapse?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Logging and Recovery",
 "subtitle": "Surviving the crash, which is the whole point.",
 "question": "How do you survive losing power mid-transaction?",
 "outcomes": [
     "State the write-ahead logging protocol and both of its rules.",
     "Explain steal and force policies and why no-force/steal is chosen.",
     "Implement ARIES-style analysis, redo, and undo.",
     "Explain checkpointing and its trade-off.",
     "Test recovery honestly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Write-ahead logging",
   "blurb": "Two rules, and everything follows."},

  {"t": "callout", "title": "The WAL protocol",
   "kind": "Two rules",
   "body": ["<b>Rule 1 (undo rule):</b> before a modified page is written "
            "to disk, the log record describing that change must already be "
            "on disk.",
            "<b>Rule 2 (redo rule):</b> before a transaction is reported "
            "committed, all its log records must be on disk.",
            "<b>Rule 1 gives atomicity</b> — if we crash with a partial "
            "page write, the log tells us how to undo it.",
            "<b>Rule 2 gives durability</b> — if we crash after "
            "reporting commit, the log tells us how to redo it. <b>These "
            "two rules are the entire foundation.</b>"]},

  {"t": "callout", "title": "Why log instead of writing pages carefully",
   "kind": "The economics",
   "body": ["A transaction may modify pages scattered across the whole "
            "database. <b>Writing them is random I/O</b> and there is no "
            "way to make many random writes atomic.",
            "<b>The log is append-only</b>, so writing it is sequential "
            "— the fastest thing storage does.",
            "<b>So: write the log synchronously and the data pages "
            "lazily.</b> One sequential fsync per commit instead of many "
            "random writes.",
            "<b>And batch the fsyncs.</b> Group commit flushes one log "
            "write for many transactions, which is why throughput is far "
            "higher than one fsync per transaction would allow."]},

  {"t": "table", "kicker": "Policies", "title": "Steal and force",
   "header": ["Policy", "Means", "Consequence"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["<b>Steal</b>", "May write an uncommitted page to disk", "<b>Needs UNDO</b>"],
     ["No-steal", "Uncommitted pages stay in memory", "Pool must hold them all"],
     ["Force", "All pages written at commit", "<b>Slow commits; random I/O</b>"],
     ["<b>No-force</b>", "Pages written lazily", "<b>Needs REDO</b>"],
   ],
   "footnote": "<b>Everyone chooses steal + no-force</b>, which needs both "
               "undo and redo — the hardest combination and the "
               "fastest.",
   "note": "The point is that the hardest recovery combination is chosen "
           "deliberately, because the alternatives cost runtime."},

  {"t": "section", "label": "Part 2", "title": "ARIES",
   "blurb": "The algorithm everyone implements."},

  {"t": "code", "kicker": "Log records", "title": "What goes in the log",
   "lang": "text", "code": """
  Every log record:   LSN, transaction id, type, prev_LSN
  Update records also: page id, offset, BEFORE image, AFTER image

  Every PAGE stores the LSN of the last log record applied to it.
      -> so recovery can tell whether a change is already there.
         If page.LSN >= record.LSN, the change is present: SKIP IT.
         This is what makes redo IDEMPOTENT, which is what makes
         it safe to crash DURING recovery and run it again.

  CLR (Compensation Log Record): written when undoing.
      Records what the undo did, and points PAST the record it
      undid. So undo never gets redone, and a crash during undo
      resumes rather than restarting.
""",
   "caption": "Page LSNs make redo idempotent; CLRs make undo idempotent. "
              "Both exist so that crashing during recovery is survivable.",
   "note": "Crash-during-recovery is the case people forget, and it is "
           "exactly what these two mechanisms address."},

  {"t": "bullets", "kicker": "Three passes", "title": "ARIES recovery",
   "items": [
     "<b>1. ANALYSIS.</b> Scan forward from the last checkpoint. Rebuild "
     "the dirty page table and the transaction table. Determine which "
     "transactions were in flight.",
     "",
     "<b>2. REDO.</b> Scan forward from the oldest dirty page's LSN. "
     "<b>Repeat history</b> — reapply <i>every</i> change, including "
     "those of transactions that will be undone.",
     "",
     "<b>3. UNDO.</b> Scan backward, rolling back every transaction that "
     "did not commit, writing a CLR for each change undone.",
     "",
     "<b>Repeating history is the counterintuitive part</b> — redo work "
     "you are about to undo.",
   ],
   "note": "Repeating history is the key design decision and the one that "
           "needs justifying."},

  {"t": "callout", "title": "Why redo everything, including doomed transactions",
   "kind": "The design decision",
   "body": ["<b>It restores the database to its exact state at the moment of "
            "the crash</b>, whatever that state was.",
            "<b>Then undo operates on a known, consistent starting "
            "point</b> rather than on an unpredictable partial state.",
            "<b>This makes the algorithm far simpler and far easier to "
            "reason about</b> — there is one well-defined intermediate "
            "state rather than a combinatorial space of partial ones.",
            "<b>And it is what makes crash-during-recovery work.</b> "
            "Recovery restarted from the beginning reaches the same "
            "intermediate state and continues. Mohan et al., 1992."]},

  {"t": "section", "label": "Part 3", "title": "Checkpoints",
   "blurb": "Bounding how much log must be read."},

  {"t": "callout", "title": "Checkpoints trade runtime cost against recovery time",
   "kind": "The trade",
   "body": ["<b>Without checkpoints, recovery must scan the log from the "
            "beginning</b> — which could be weeks of it.",
            "<b>A checkpoint records which pages are dirty and which "
            "transactions are active</b>, so recovery can start there.",
            "<b>Frequent checkpoints mean fast recovery and more I/O "
            "during normal operation.</b> Infrequent means the reverse.",
            "<b>Fuzzy checkpoints</b> are what systems use: record the "
            "state without stopping the world, accepting that the recorded "
            "state is slightly inconsistent — which analysis then "
            "resolves."]},

  {"t": "bullets", "kicker": "Related", "title": "What else the log enables",
   "items": [
     "<b>Point-in-time recovery.</b> Restore a backup, then replay the log "
     "to any chosen moment. Recovers from a bad UPDATE, not just a crash.",
     "",
     "<b>Replication.</b> Ship the log to another machine and replay it "
     "— the standard mechanism for streaming replicas.",
     "",
     "<b>Change data capture.</b> Read the log to feed downstream systems "
     "without polling the tables.",
     "",
     "<b>Auditing.</b> The log is a complete record of every change.",
     "",
     "<b>The log turns out to be the most reusable structure in the "
     "system.</b>",
   ],
   "note": "The log-as-universal-primitive observation is worth drawing "
           "out — it is the basis of Kafka's design too."},

  {"t": "section", "label": "Part 4", "title": "Testing",
   "blurb": "The only part that actually establishes durability."},

  {"t": "callout", "title": "You have not tested recovery until you have killed the process",
   "kind": "The standard",
   "body": ["<b>Reasoning about recovery proves nothing.</b> Every system "
            "that lost data had a correctness argument.",
            "<b>Kill the process at a randomly chosen point</b>, during a "
            "transactional workload, and verify the recovered state against "
            "an independent model. Then do it a thousand times.",
            "<b>kill -9, not a clean shutdown</b> — a clean shutdown "
            "flushes everything and tests nothing.",
            "<b>And crash during recovery too.</b> That is the case the "
            "page LSNs and CLRs exist for, and it is the case nobody tests "
            "by accident."]},

  {"t": "bullets", "kicker": "Honesty", "title": "What a crash test must cover",
   "items": [
     "<b>Crash at random points</b>, not at convenient ones. Instrument the "
     "code to abort at a random log write.",
     "",
     "<b>Crash during recovery</b>, repeatedly.",
     "",
     "<b>Verify against an independent model</b>, not against the database's "
     "own opinion of its state.",
     "",
     "<b>Report the whole distribution</b> — a thousand runs, not a "
     "representative one.",
     "",
     "<b>Then name a crash point you would not survive</b>, or prove there "
     "is none. <b>Every system has assumptions.</b>",
   ],
   "footnote": "This is exactly what Project 2 requires, and the honesty "
               "requirement is the point of it."},
 ],
 "takeaways": [
   "WAL has two rules: the log record reaches disk before the page (undo "
   "rule), and before commit is reported (redo rule).",
   "Logging is chosen because the log is sequential and the data pages are "
   "scattered — one sequential fsync beats many random writes.",
   "Everyone chooses steal + no-force, which requires both undo and redo "
   "— the hardest recovery and the fastest runtime.",
   "Page LSNs make redo idempotent and CLRs make undo idempotent, which is "
   "what makes crashing during recovery survivable.",
   "ARIES is analysis, redo, undo — and redo repeats <i>all</i> "
   "history, so undo begins from a known state.",
   "You have not tested recovery until you have killed the process at "
   "random points a thousand times and verified against an independent "
   "model.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Write-ahead logging"),
  ("callout", "The two rules",
   ["<b>Rule 1, the undo rule:</b> before a modified page may be written to "
    "disk, the log record describing that modification must already be on "
    "disk.",
    "<b>Rule 2, the redo rule:</b> before a transaction may be reported to "
    "the client as committed, all of its log records must be on disk.",
    "<b>Rule 1 provides atomicity.</b> If we crash after a partially "
    "completed transaction's pages have reached disk, the log contains the "
    "before-images needed to undo them.",
    "<b>Rule 2 provides durability.</b> If we crash after telling the client "
    "the transaction committed, but before its pages reached disk, the log "
    "contains the after-images needed to redo them.",
    "<b>These two rules are the entire foundation of crash recovery</b>, and "
    "everything in this module is machinery for implementing them "
    "efficiently."]),
  ("callout", "Why log at all, instead of writing pages carefully",
   ["A single transaction may modify pages scattered anywhere across the "
    "database. <b>Writing those pages is random I/O</b> — the slow case "
    "from Module 02 — and, more fundamentally, <b>there is no way to "
    "make many separate random writes atomic</b>. A crash partway through "
    "leaves some applied and some not, with nothing recording which.",
    "<b>The log is append-only.</b> Writing it is a sequential append, which "
    "is the fastest thing storage does, and a single sequential write can be "
    "made durable with one fsync.",
    "<b>So: write the log synchronously, and the data pages lazily.</b> The "
    "commit path pays one sequential fsync; the scattered page writes happen "
    "later, in the background, coalesced and reordered for efficiency.",
    "<b>And batch the fsyncs.</b> <b>Group commit</b> collects the log "
    "records of many concurrent transactions and flushes them with a single "
    "fsync, so the per-transaction cost of durability falls by an order of "
    "magnitude. This is why a database can commit thousands of transactions "
    "per second on hardware that performs a few hundred fsyncs per second."]),
  ("table", ["Policy", "Definition", "Requires", "Runtime cost"],
   [["<b>Steal</b>", "The buffer pool may evict and write a page containing "
     "uncommitted changes.", "<b>UNDO logging</b>",
     "<b>None</b> — the pool evicts freely."],
    ["<b>No-steal</b>", "Pages with uncommitted changes must stay in memory "
     "until commit.", "No undo needed.",
     "<b>The buffer pool must hold every uncommitted page</b>, which bounds "
     "transaction size by memory."],
    ["<b>Force</b>", "All of a transaction's pages are written to disk "
     "before commit returns.", "No redo needed.",
     "<b>Commit performs scattered random writes</b> and is correspondingly "
     "slow."],
    ["<b>No-force</b>", "Pages are written lazily after commit.",
     "<b>REDO logging</b>", "<b>None</b> — commit writes only the "
     "log."]],
   [0.15, 0.37, 0.19, 0.29]),
  ("p", "<b>Every real system chooses steal and no-force</b>, which requires "
        "<i>both</i> undo and redo — the most complex recovery "
        "algorithm of the four combinations. <b>It is chosen because the "
        "alternatives pay at runtime</b>, continuously, while the complexity "
        "is paid once by the implementer and only exercised after a crash. "
        "That is a good trade, and recognising it is the point of the "
        "table."),

  ("h1", "2 &nbsp; ARIES"),
  ("code", """Every log record:  LSN, txn id, type, prev_LSN
Update records:    + page id, offset, BEFORE image, AFTER image

Every PAGE stores the LSN of the last record applied to it:
    if page.LSN >= record.LSN, the change is already there: SKIP
    -> this makes REDO IDEMPOTENT

CLR (Compensation Log Record): written when undoing.
    Records what the undo did; points PAST the record it undid.
    -> undo is never redone, and a crash during undo RESUMES"""),
  ("callout", "Both mechanisms exist so that crashing during recovery is safe",
   ["<b>Page LSNs make redo idempotent.</b> Each page records the LSN of the "
    "last change applied to it, so redo can determine whether a given change "
    "is already present and skip it. Applying the redo pass twice produces "
    "the same result as applying it once.",
    "<b>Compensation log records make undo idempotent.</b> When undoing a "
    "change, ARIES writes a CLR describing the compensating action, and that "
    "CLR points <i>past</i> the record it undid. So a restarted undo pass "
    "skips work already done rather than undoing it twice.",
    "<b>Both exist for one reason: the machine can crash during "
    "recovery.</b> This is not a remote possibility — a machine that "
    "crashed once because of a failing power supply or a kernel bug is "
    "disproportionately likely to crash again during the recovery that "
    "follows.",
    "<b>It is also the case nobody tests by accident</b>, which is why "
    "&sect;4 requires it explicitly."]),
  ("ol", ["<b>ANALYSIS.</b> Scan forward from the most recent checkpoint. "
          "Rebuild the <b>dirty page table</b> (which pages had unwritten "
          "changes) and the <b>transaction table</b> (which transactions "
          "were active, and what their last LSN was). Determine which "
          "transactions were in flight at the crash and must be undone.",
          "<b>REDO.</b> Scan forward from the lowest LSN in the dirty page "
          "table, and <b>repeat history</b>: reapply <i>every</i> logged "
          "change whose page LSN shows it is not already present — "
          "<b>including changes made by transactions that will be undone in "
          "the next pass</b>.",
          "<b>UNDO.</b> Scan backward through the log, rolling back every "
          "transaction that was active at the crash, writing a CLR for each "
          "change undone, and following prev_LSN pointers to find each "
          "transaction's chain of changes."]),
  ("callout", "Why repeat history, including transactions you are about to undo",
   ["This is the counterintuitive part of ARIES, and the reason is worth "
    "stating clearly.",
    "<b>Repeating all of history restores the database to exactly the state "
    "it was in at the moment of the crash</b> — whatever that state "
    "was, including the partial effects of transactions that never "
    "committed.",
    "<b>Undo then operates from a known, well-defined starting point.</b> "
    "Without this, undo would have to cope with an unpredictable partial "
    "state in which some of a transaction's changes had reached disk and "
    "others had not, in an arbitrary combination.",
    "<b>So the algorithm becomes dramatically simpler to implement and to "
    "reason about</b>: there is one well-defined intermediate state rather "
    "than a combinatorial space of them. <b>And it is what makes "
    "crash-during-recovery work</b> — a restarted recovery repeats "
    "history again, reaches the same intermediate state, and continues from "
    "there. Mohan et al., 1992."]),

  ("break",),
  ("h1", "3 &nbsp; Checkpoints"),
  ("callout", "Checkpoints trade runtime I/O against recovery time",
   ["<b>Without checkpoints, recovery would have to scan the log from its "
    "beginning</b> — potentially weeks or months of it — because "
    "there would be no way to know which changes had already reached disk.",
    "<b>A checkpoint records the dirty page table and the active transaction "
    "table</b>, so recovery can begin its analysis there instead.",
    "<b>Frequent checkpoints mean fast recovery and more background I/O "
    "during normal operation.</b> Infrequent checkpoints mean the reverse. "
    "The setting is a direct trade between steady-state throughput and the "
    "recovery time objective, and it should be chosen from the latter.",
    "<b>Fuzzy checkpoints are what systems actually use.</b> A "
    "'sharp' checkpoint would quiesce the system, flush everything, and "
    "record a perfectly consistent state — which means stopping the "
    "world, which is unacceptable. A fuzzy checkpoint records the state "
    "while transactions continue, accepting that the recorded picture is "
    "slightly inconsistent, and leaves the analysis pass to resolve the "
    "discrepancy. ARIES is designed around this."]),
  ("ul", ["<b>Point-in-time recovery.</b> Restore a backup and replay the "
          "log up to any chosen instant. <b>This recovers from a mistaken "
          "<code>UPDATE</code> without a <code>WHERE</code> clause</b>, not "
          "just from a crash — which is the failure mode that actually "
          "happens.",
          "<b>Replication.</b> Ship the log to another machine and replay it "
          "there. This is how streaming replication works in essentially "
          "every system, and it is why a replica is a byte-for-byte copy "
          "rather than a logically equivalent one.",
          "<b>Change data capture.</b> Read the log to feed downstream "
          "systems — search indexes, caches, analytics — without "
          "polling tables or adding triggers. Debezium and similar tools do "
          "exactly this.",
          "<b>Auditing.</b> The log is a complete, ordered record of every "
          "change ever made.",
          "<b>The log turns out to be the most reusable structure in the "
          "system</b>, which is an observation with consequences well beyond "
          "databases — it is the central idea of Kafka and of "
          "event-sourced architectures generally."]),

  ("h1", "4 &nbsp; Testing recovery"),
  ("callout", "You have not tested recovery until you have killed the process",
   ["<b>Reasoning about recovery establishes nothing.</b> Every system that "
    "has ever lost data had a correctness argument, and the argument was "
    "wrong in a way nobody had thought of — fsyncgate (Module 02) being "
    "the clearest example.",
    "<b>Kill the process at a randomly chosen point</b> during a "
    "transactional workload, restart, run recovery, and verify the resulting "
    "state against an <i>independent</i> model of what should have "
    "survived. <b>Then do it a thousand times</b>, at a thousand different "
    "points.",
    "<b>Use <code>kill -9</code>, not a clean shutdown.</b> A clean "
    "shutdown flushes every buffer and runs the shutdown path; it tests "
    "nothing about recovery and will pass regardless.",
    "<b>And crash during recovery, repeatedly.</b> That is precisely the "
    "case the page LSNs and CLRs of &sect;2 exist to handle, and it is the "
    "case that is never exercised by accident."]),
  ("ul", ["<b>Crash at random points, not convenient ones.</b> Instrument "
          "the code to abort at a randomly selected log write or page "
          "flush, so the crash lands in the middle of operations rather "
          "than between them.",
          "<b>Crash during recovery</b>, and during the recovery of that "
          "recovery.",
          "<b>Verify against an independent model</b> — a separate "
          "record of which transactions were acknowledged as committed "
          "— rather than against the database's own account of its "
          "state. A corrupted database will happily report itself "
          "consistent.",
          "<b>Report the whole distribution.</b> A thousand runs and their "
          "outcomes, not a single representative success. One failure in a "
          "thousand is a durability bug, not noise.",
          "<b>Then name a crash point your implementation would not "
          "survive, or prove there is none.</b> <b>Every system rests on "
          "assumptions</b> — that fsync means what it says, that a "
          "sector write is atomic, that the disk does not reorder across a "
          "barrier. Stating yours is what distinguishes an engineer from "
          "someone who has not looked. <b>This is what Project 2 asks for, "
          "and the honesty requirement is the point of the exercise.</b>"]),
 ],
 "resources": [
   ("CMU 15-445 &mdash; Lectures 20–21, Crash Recovery",
    "https://15445.courses.cs.cmu.edu/",
    "WAL, steal/force policies, and the three ARIES passes."),
   ("Mohan et al. &mdash; ARIES (1992, free)",
    "https://cs.stanford.edu/people/chrismre/cs345/rl/aries.pdf",
    "The original paper. Long, and the repeating-history argument in "
    "&sect;2 is worth reading in full."),
   ("PostgreSQL documentation &mdash; Write-Ahead Logging and Reliability",
    "https://www.postgresql.org/docs/current/wal.html",
    "A production implementation, including group commit and the fsync "
    "settings that control durability."),
   ("Pillai et al. &mdash; All File Systems Are Not Created Equal (free)",
    "https://www.usenix.org/conference/osdi14/technical-sessions/"
    "presentation/pillai",
    "What filesystems actually guarantee about ordering and atomicity, and "
    "how many applications get it wrong. Sobering, and directly relevant to "
    "&sect;4."),
   ("Jepsen &mdash; database analyses",
    "https://jepsen.io/analyses",
    "Empirical crash and partition testing of real systems. The standard "
    "&sect;4 describes, applied professionally."),
 ],
 "exercises": [
   "Implement write-ahead logging with LSNs and before/after images. Verify "
   "both WAL rules are enforced by instrumenting every page write.",
   "Implement group commit and measure the throughput improvement against "
   "one fsync per transaction.",
   "Implement page LSNs and demonstrate redo idempotence: run the redo pass "
   "twice and confirm an identical result.",
   "Implement ARIES analysis, redo, and undo with CLRs.",
   "<b>Build the crash test harness:</b> kill the process at a randomly "
   "chosen log write, recover, and verify against an independent record of "
   "acknowledged commits.",
   "Run it a thousand times and report every outcome.",
   "Crash during recovery and confirm the restarted recovery completes "
   "correctly.",
   "Implement fuzzy checkpointing. Measure recovery time against checkpoint "
   "interval and plot it.",
   "Implement point-in-time recovery: restore a backup and replay to a "
   "chosen LSN.",
   "<b>Write the failure analysis:</b> name a crash point your "
   "implementation would not survive, and the assumption it rests on.",
 ],
 "selfcheck": [
   "State both WAL rules and say which ACID property each provides.",
   "Why log at all, rather than writing data pages carefully?",
   "Define steal and force, and say which combination everyone chooses and "
   "why.",
   "What makes redo idempotent, and what makes undo idempotent?",
   "Why do both of those mechanisms exist?",
   "Name the three ARIES passes and what each accomplishes.",
   "Why does redo repeat the history of transactions that will be undone?",
   "What do checkpoints trade, and what is a fuzzy checkpoint?",
   "Name four things the log enables besides crash recovery.",
   "What does an honest recovery test require?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Column Stores and Analytics",
 "subtitle": "A different workload needs a different system.",
 "question": "Why are analytical databases built differently?",
 "outcomes": [
     "Contrast OLTP and OLAP workloads.",
     "Explain why column storage suits analytics.",
     "Explain the compression schemes columns enable.",
     "Explain late materialisation and vectorised execution together.",
     "Explain why the two workloads ended up in separate systems.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two workloads",
   "blurb": "They want opposite things."},

  {"t": "table", "kicker": "Workloads", "title": "OLTP and OLAP",
   "header": ["", "OLTP", "OLAP"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Query shape", "Few rows, all columns", "<b>Many rows, few columns</b>"],
     ["Writes", "<b>Constant, small</b>", "Bulk load, rarely updated"],
     ["Concurrency", "<b>Thousands of users</b>", "Few, large queries"],
     ["Latency", "<b>Milliseconds</b>", "Seconds to minutes"],
     ["Data size", "Working set in memory", "<b>Far larger than memory</b>"],
     ["Indexes", "Many, selective", "<b>Few; scans dominate</b>"],
   ],
   "footnote": "Almost every design decision follows from the first row.",
   "note": "The first row really does drive everything else. Anchor on it."},

  {"t": "callout", "title": "Row storage reads columns you did not ask for",
   "kind": "The central inefficiency",
   "body": ["<code>SELECT avg(salary) FROM employees</code> on a table with "
            "fifty columns.",
            "<b>Row storage reads every one of them</b>, because a row is "
            "contiguous and the unit of I/O is a page.",
            "<b>You wanted 4 bytes per row and read 400.</b> Ninety-nine "
            "percent of the bandwidth is wasted.",
            "<b>Column storage keeps each column contiguously</b>, so the "
            "query reads only the salary column — a 100× reduction in "
            "bytes moved, before any compression."]},

  {"t": "section", "label": "Part 2", "title": "Compression",
   "blurb": "The second, larger advantage."},

  {"t": "callout", "title": "A column is a much better compression target",
   "kind": "Why columns compress well",
   "body": ["<b>A column holds values of one type with a similar "
            "distribution.</b> A row holds a name, a date, a float, and a "
            "boolean — nothing in common.",
            "<b>So column data is highly redundant</b>, and the schemes "
            "that exploit it are simple and fast.",
            "<b>10–30× compression is routine</b>, against perhaps 2–3× "
            "for row data.",
            "<b>And compression makes queries faster, not slower</b>, "
            "because the bottleneck is memory bandwidth (Module 07) — "
            "fewer bytes moved beats the decompression cost, often by a long "
            "way."]},

  {"t": "table", "kicker": "Schemes", "title": "Column compression schemes",
   "header": ["Scheme", "Works when", "Operate on directly?"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["<b>Run-length</b>", "Sorted or low cardinality", "<b>Yes — count without expanding</b>"],
     ["<b>Dictionary</b>", "Few distinct values", "<b>Yes — compare codes</b>"],
     ["Bit-packing", "Small value range", "<b>Yes — SIMD on packed ints</b>"],
     ["Delta", "Sorted numerics, timestamps", "Partly"],
     ["Frame of reference", "Clustered values", "Yes"],
   ],
   "footnote": "<b>Operating on compressed data directly is the real "
               "win</b> — not merely saving space.",
   "note": "Direct operation is the point. Decompressing and then operating "
           "gives up most of the benefit."},

  {"t": "callout", "title": "Operate on compressed data without decompressing",
   "kind": "The idea that makes it pay",
   "body": ["<b>Run-length encoded:</b> to count rows matching a value, sum "
            "the run lengths. The data is never expanded.",
            "<b>Dictionary encoded:</b> to filter on 'Texas', look up its "
            "code once and compare integers — faster than comparing "
            "strings, and on packed data.",
            "<b>Bit-packed:</b> SIMD operates on several packed values per "
            "instruction.",
            "<b>So compression is not a space/time trade here.</b> It saves "
            "space <i>and</i> time, which is unusual and is why column "
            "stores lean on it so heavily."]},

  {"t": "section", "label": "Part 3", "title": "Execution",
   "blurb": "What column storage enables."},

  {"t": "bullets", "kicker": "Late materialisation", "title": "Keep columns separate as long as possible",
   "items": [
     "<b>Early materialisation</b> reconstructs rows immediately after "
     "reading, then processes rows. Simple, and throws away the advantage.",
     "",
     "<b>Late materialisation</b> keeps columns separate through filters "
     "and joins, assembling rows only at the end.",
     "",
     "<b>Why it wins:</b> a filter on one column produces a bitmap, and "
     "other columns need only be read where the bitmap is set.",
     "",
     "<b>And compression survives longer</b>, so more of the plan operates "
     "on compressed data.",
     "",
     "<b>With vectorised execution (Module 07) this is the modern "
     "analytical engine.</b>",
   ],
   "note": "Column storage and vectorised execution are the same idea "
           "arriving from two directions."},

  {"t": "callout", "title": "Column stores and vectorisation belong together",
   "kind": "Why they co-evolved",
   "body": ["<b>Vectorised execution wants dense arrays of same-typed "
            "values</b> to loop over (Module 07).",
            "<b>Column storage supplies exactly that</b>, by construction.",
            "<b>So the two ideas reinforce each other</b>, and arriving at "
            "either tends to lead to the other — which is what happened "
            "historically with MonetDB and X100.",
            "<b>Together they account for most of the 10–100× that "
            "analytical systems achieve over row stores</b> on scan-heavy "
            "queries."]},

  {"t": "section", "label": "Part 4", "title": "Why separate systems",
   "blurb": "And whether they are converging."},

  {"t": "callout", "title": "The requirements are genuinely opposed",
   "kind": "Not a maturity gap",
   "body": ["<b>OLTP wants:</b> row storage, many indexes, fine-grained "
            "locking, small fast transactions.",
            "<b>OLAP wants:</b> column storage, few indexes, bulk loading, "
            "long scans, heavy compression.",
            "<b>A system optimised for one is poor at the other</b>, and "
            "this is structural rather than a matter of effort.",
            "<b>Hence the standard architecture:</b> an OLTP system of "
            "record, an ETL or CDC pipeline, and a separate analytical "
            "warehouse — which is operationally annoying and keeps being "
            "rediscovered."]},

  {"t": "bullets", "kicker": "Convergence", "title": "What is changing",
   "items": [
     "<b>HTAP systems</b> attempt both, often by keeping a row store for "
     "writes and a column store for reads, synchronised.",
     "",
     "<b>Column indexes</b> in row-store systems — SQL Server's "
     "clustered columnstore, Postgres extensions.",
     "",
     "<b>DuckDB</b> made embedded analytics trivial: a column store in a "
     "library, with no server.",
     "",
     "<b>Open formats</b> — Parquet and Arrow — decoupled storage from "
     "the engine, so many engines read the same files.",
     "",
     "<b>And the separation persists</b>, because the underlying conflict "
     "has not gone away.",
   ],
   "note": "Arrow and Parquet are the most consequential recent change — "
           "the format became the interface."},
 ],
 "takeaways": [
   "OLTP reads few rows and all columns; OLAP reads many rows and few "
   "columns. Nearly every design difference follows from that.",
   "Row storage reads every column because a row is contiguous — "
   "wasting 99% of the bandwidth on a single-column aggregate.",
   "A column holds one type with a similar distribution, so it compresses "
   "10–30&times; against 2–3&times; for rows.",
   "Compression makes analytical queries <i>faster</i>, because memory "
   "bandwidth is the bottleneck and compressed data can often be operated on "
   "directly.",
   "Late materialisation keeps columns separate through the plan, so filters "
   "produce bitmaps and other columns are read only where needed.",
   "Column storage and vectorised execution are the same idea from two "
   "directions, and together account for most of the 10–100&times;.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two workloads"),
  ("table", ["", "OLTP", "OLAP"],
   [["<b>Query shape</b>",
     "<b>Few rows, all columns.</b> 'Fetch order 12345.'",
     "<b>Many rows, few columns.</b> 'Average order value by region last "
     "quarter.'"],
    ["Writes", "<b>Constant and small</b> — individual inserts and "
     "updates from users.",
     "Bulk loads, infrequent updates. Often append-only."],
    ["Concurrency", "<b>Thousands of concurrent users.</b>",
     "A handful of large queries."],
    ["Latency target", "<b>Milliseconds.</b>", "Seconds to minutes."],
    ["Data size", "Working set usually fits in memory.",
     "<b>Far larger than memory.</b> Scans dominate."],
    ["Indexes", "Many, and selective.",
     "<b>Few</b> — a query touching 40% of rows gains nothing from an "
     "index (Module 03)."]],
   [0.15, 0.40, 0.45]),
  ("callout", "Row storage reads columns you did not ask for",
   ["Consider <code>SELECT avg(salary) FROM employees</code> on a table with "
    "fifty columns.",
    "<b>Row storage stores each row contiguously</b>, and the unit of I/O is "
    "a page, so reading any row's salary requires reading all fifty of its "
    "columns.",
    "<b>You wanted four bytes per row and you read four hundred.</b> "
    "Ninety-nine percent of the bandwidth — disk, memory, and cache "
    "— is spent on data the query does not reference.",
    "<b>Column storage keeps each column contiguously</b>, so the query "
    "reads the salary column and nothing else. <b>That is a hundredfold "
    "reduction in bytes moved before any compression is applied</b>, and it "
    "is the first of the two reasons column stores win."]),

  ("h1", "2 &nbsp; Compression"),
  ("callout", "A column is a far better compression target than a row",
   ["<b>A column contains values of a single type with a similar "
    "distribution</b> — a million timestamps, or a million country "
    "codes, or a million prices in a narrow range.",
    "<b>A row contains a name, a date, a floating-point number, and a "
    "boolean</b>, which have nothing in common and compress poorly together.",
    "<b>So column data is highly redundant</b>, and the schemes that exploit "
    "it are simple, fast, and specialised. <b>Ratios of 10 to 30 times are "
    "routine</b>, against perhaps 2 or 3 for row-oriented data with a "
    "general-purpose compressor.",
    "<b>And compression makes analytical queries faster rather than "
    "slower.</b> Module 07 established that <b>memory bandwidth, not CPU, is "
    "usually the limit</b> for scans. Moving a tenth as many bytes and "
    "spending a few cycles decompressing is a clear win — and often the "
    "decompression is not needed at all, per the next page."]),
  ("table", ["Scheme", "Effective when", "Direct operation"],
   [["<b>Run-length encoding</b>",
     "The column is sorted, or has low cardinality. Store (value, count) "
     "pairs.",
     "<b>Yes.</b> Counting rows matching a value is summing run lengths "
     "— the data is never expanded."],
    ["<b>Dictionary encoding</b>",
     "Few distinct values relative to row count. Store codes and a "
     "dictionary.",
     "<b>Yes.</b> Filtering on 'Texas' means looking up its code once and "
     "comparing small integers rather than strings."],
    ["<b>Bit-packing</b>",
     "Values span a small range. Store each in the minimum bits needed.",
     "<b>Yes.</b> SIMD instructions operate on several packed values at "
     "once."],
    ["<b>Delta encoding</b>",
     "Sorted numerics, timestamps, sequential identifiers. Store "
     "differences.", "Partly — sums and ranges, yes; equality, no."],
    ["<b>Frame of reference</b>",
     "Values clustered around a base. Store the base plus small offsets.",
     "Yes, for comparisons against the base."]],
   [0.21, 0.37, 0.42]),
  ("callout", "Operating on compressed data directly is the real win",
   ["Decompressing a column and then processing it captures only the I/O "
    "benefit. <b>Processing the compressed representation captures the CPU "
    "benefit too</b>, and that is where most of the advantage lies.",
    "<b>Run-length encoded:</b> <code>SELECT count(*) WHERE state = "
    "'TX'</code> is a sum over run lengths. The number of operations is "
    "proportional to the number of <i>runs</i>, not rows.",
    "<b>Dictionary encoded:</b> resolve the predicate value to its code "
    "once, then scan comparing fixed-width integers — which is both "
    "faster per comparison than string comparison and amenable to SIMD.",
    "<b>So compression here is not a space-for-time trade at all.</b> It "
    "saves space <i>and</i> time simultaneously, which is unusual enough to "
    "be worth noticing, and it is why analytical systems compress "
    "aggressively rather than treating it as an option."]),

  ("break",),
  ("h1", "3 &nbsp; Execution"),
  ("table", ["", "Early materialisation", "Late materialisation"],
   [["Approach", "Reconstruct rows immediately after reading the needed "
     "columns, then process rows as usual.",
     "<b>Keep columns separate through filters, aggregations, and joins</b>, "
     "assembling rows only at the very end."],
    ["Simplicity", "<b>Simple</b> — the rest of the engine is "
     "unchanged.", "More complex; operators work on column vectors."],
    ["Benefit retained", "<b>Only the I/O saving.</b> The CPU advantages "
     "are discarded at reconstruction.",
     "<b>A filter on one column produces a bitmap or selection vector, and "
     "other columns are read only where it is set.</b> Compression survives "
     "further into the plan, so more operators work on compressed data."]],
   [0.15, 0.40, 0.45]),
  ("callout", "Column storage and vectorised execution are the same idea",
   ["Module 07 established that <b>vectorised execution wants dense arrays "
    "of same-typed values</b> to loop over, so that dispatch is amortised "
    "and the compiler can emit SIMD.",
    "<b>Column storage produces exactly that, by construction.</b> A column "
    "<i>is</i> a dense array of same-typed values.",
    "<b>So the two ideas reinforce one another, and arriving at either tends "
    "to lead to the other.</b> This is what happened historically: MonetDB "
    "started from column storage and arrived at vectorised execution; the "
    "X100 work made the connection explicit.",
    "<b>Together they account for most of the 10 to 100 times that "
    "analytical systems achieve over row stores</b> on scan-heavy queries. "
    "Neither alone gets close, which is why systems that adopted only one "
    "saw disappointing results."]),

  ("h1", "4 &nbsp; Why they remain separate systems"),
  ("callout", "The requirements are genuinely opposed",
   ["<b>OLTP wants</b> row storage (a transaction touches whole rows), many "
    "selective indexes, fine-grained locking or MVCC, and short "
    "transactions with millisecond latency.",
    "<b>OLAP wants</b> column storage, few indexes, bulk loading, heavy "
    "compression, long scans, and large memory allocations per query.",
    "<b>A system optimised for one is structurally poor at the other.</b> "
    "This is not a maturity gap that will close with effort — the two "
    "sets of requirements conflict at the level of data layout, which is the "
    "most expensive thing to change.",
    "<b>Hence the standard architecture:</b> an OLTP system of record, an "
    "ETL or change-data-capture pipeline (Module 11), and a separate "
    "analytical warehouse. <b>It is operationally annoying</b> — two "
    "systems, a pipeline, and a replication lag to explain to users — "
    "<b>which is why it keeps being questioned and keeps being "
    "rediscovered.</b>"]),
  ("ul", ["<b>HTAP systems</b> attempt both workloads in one engine, "
          "typically by maintaining a row store for recent writes and a "
          "column store for historical reads, with background conversion "
          "between them. SingleStore, TiDB, and SAP HANA take variations of "
          "this approach. It works, and the complexity is real.",
          "<b>Column indexes within row-store systems.</b> SQL Server's "
          "clustered columnstore index and PostgreSQL extensions such as "
          "Citus Columnar bring columnar storage to specific tables inside a "
          "conventional system.",
          "<b>DuckDB</b> made embedded analytics trivial: a column store "
          "with vectorised execution, in a library, with no server to "
          "operate. It has substantially changed how local analytical work "
          "is done, in the way SQLite did for transactional work.",
          "<b>Open formats decoupled storage from the engine.</b> "
          "<b>Parquet</b> (on-disk columnar) and <b>Arrow</b> (in-memory "
          "columnar) are read and written by many independent engines, so "
          "the data no longer belongs to one system. <b>This is arguably the "
          "most consequential recent change</b> — the format became the "
          "interface, and the engine became replaceable.",
          "<b>And the separation persists</b>, because the conflict in "
          "&sect;4 has not gone away. The tooling around it has improved "
          "considerably; the underlying tension has not."]),
 ],
 "resources": [
   ("CMU 15-721 &mdash; Advanced Database Systems (free)",
    "https://15721.courses.cs.cmu.edu/",
    "Pavlo's graduate course, largely about the systems in this module. The "
    "column store and compression lectures are the primary source."),
   ("Abadi, Boncz & Harizopoulos &mdash; The Design and Implementation of "
    "Modern Column-Oriented Database Systems (free)",
    "https://stratos.seas.harvard.edu/publications/",
    "The definitive survey. Late materialisation, compression, and the "
    "execution model, with measurements."),
   ("Stonebraker et al. &mdash; C-Store (2005, free)",
    "https://www.vldb.org/archives/website/2005/program/paper/thu/p553-stonebraker.pdf",
    "The paper that established the modern column store, and the ancestor of "
    "Vertica."),
   ("Apache Arrow and Parquet documentation",
    "https://arrow.apache.org/",
    "The open formats of &sect;4. Worth understanding directly — they "
    "are increasingly the interface between systems."),
   ("DuckDB documentation and papers",
    "https://duckdb.org/",
    "A readable, modern column store you can install in one command and "
    "experiment with immediately."),
 ],
 "exercises": [
   "Store the same dataset row-wise and column-wise. Measure bytes read for "
   "a single-column aggregate over all rows.",
   "Measure the same query's wall-clock time for both layouts and attribute "
   "the difference.",
   "Implement run-length and dictionary encoding for a column. Report the "
   "compression ratio on real data of each kind.",
   "Implement a count query that operates on run-length encoded data without "
   "decompressing, and compare against decompress-then-count.",
   "Implement dictionary-encoded filtering by comparing codes. Compare "
   "against string comparison.",
   "Implement bit-packing and confirm the compiler vectorises operations on "
   "the packed representation.",
   "Implement early and late materialisation for a two-predicate query and "
   "measure the difference.",
   "Load the same data into PostgreSQL and DuckDB. Run five analytical "
   "queries on each and report the ratio.",
   "Write a Parquet file and read it from two different tools, confirming "
   "the format rather than the engine is the interface.",
   "Take an OLTP schema you know and design the analytical schema you would "
   "build from it, stating what the ETL would do.",
 ],
 "selfcheck": [
   "Give six differences between OLTP and OLAP workloads, and say which "
   "drives the rest.",
   "Why does row storage waste bandwidth on an analytical query? Give the "
   "ratio.",
   "Why does a column compress so much better than a row?",
   "Why does compression make analytical queries faster rather than slower?",
   "Name five column compression schemes and say which permit direct "
   "operation.",
   "What is late materialisation and why does it win?",
   "Why do column storage and vectorised execution belong together?",
   "Why are OLTP and OLAP in separate systems, and is that a maturity gap?",
   "Name four things that are changing, and say which is most "
   "consequential.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Distributed Databases",
 "subtitle": "What you gain, what you give up, and whether you need it.",
 "question": "What actually changes when the data is on many machines?",
 "outcomes": [
     "State CAP precisely and explain what it does not say.",
     "Explain PACELC and why it is the more useful framing.",
     "Explain two-phase commit and its blocking failure.",
     "Explain consensus and what Raft provides.",
     "Judge whether a workload needs distribution at all.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why distribute",
   "blurb": "Three reasons, and only some of them are good."},

  {"t": "table", "kicker": "Reasons", "title": "Why people distribute",
   "header": ["Reason", "Assessment"],
   "widths": [3.6, 8.5],
   "rows": [
     ["<b>Capacity</b>", "Data exceeds one machine. <b>Legitimate, and rarer than claimed</b>"],
     ["<b>Availability</b>", "Survive a machine failure. <b>Usually the real reason</b>"],
     ["<b>Geography</b>", "Serve users near them. <b>Legitimate and unavoidable</b>"],
     ["Throughput", "More machines, more queries. <b>Often a single machine suffices</b>"],
     ["Resume-driven", "<b>It happens</b>", "—"],
   ],
   "footnote": "A modern server handles a few terabytes in memory and tens "
               "of terabytes on NVMe. The bar is higher than most people "
               "assume.",
   "note": "Be direct about this. The reflex to distribute costs far more "
           "than people expect."},

  {"t": "callout", "title": "A single machine is bigger than you think",
   "kind": "Before distributing, check",
   "body": ["<b>A commodity server today:</b> 128 cores, 2 TB of RAM, and "
            "tens of terabytes of NVMe at millions of IOPS.",
            "<b>That handles workloads that genuinely required a cluster "
            "fifteen years ago</b>, and it does so with transactions, "
            "joins, and a single debugger.",
            "<b>Distribution costs:</b> no distributed joins worth the name, "
            "weaker transactions, network partitions as a routine event, and "
            "operational complexity that never goes away.",
            "<b>So measure first.</b> 'We might need to scale' is not a "
            "measurement, and the cost of being wrong in that direction is "
            "paid every day."]},

  {"t": "section", "label": "Part 2", "title": "CAP and PACELC",
   "blurb": "The theorem, and what it actually says."},

  {"t": "callout", "title": "CAP, stated precisely",
   "kind": "And what it does not say",
   "body": ["<b>In the presence of a network partition</b>, a system must "
            "choose between consistency (every read sees the latest write) "
            "and availability (every request gets a response).",
            "<b>It does not say 'pick two of three'.</b> Partitions are not "
            "a choice — they happen. The choice is what to do when one "
            "occurs.",
            "<b>And it is about one specific consistency model</b> "
            "(linearizability) and one specific availability definition. "
            "Both are stronger than most systems need.",
            "<b>'CP' and 'AP' labels are far less informative than they "
            "look</b>, and most marketing use of CAP is wrong."]},

  {"t": "callout", "title": "PACELC is the more useful framing",
   "kind": "Abadi, 2012",
   "body": ["<b>If there is a Partition, choose between Availability and "
            "Consistency. Else, choose between Latency and "
            "Consistency.</b>",
            "<b>The 'else' clause is the important addition</b>, because "
            "partitions are rare and the latency/consistency trade is paid "
            "<i>every single request</i>.",
            "<b>Strong consistency means coordination</b> — a round trip "
            "to a quorum, which costs milliseconds and far more across "
            "regions.",
            "<b>So the everyday cost of consistency is latency</b>, not "
            "availability. That is the trade you actually make, and CAP "
            "obscures it."]},

  {"t": "section", "label": "Part 3", "title": "Distributed transactions",
   "blurb": "Atomicity across machines."},

  {"t": "code", "kicker": "2PC", "title": "Two-phase commit",
   "lang": "text", "code": """
  PHASE 1 -- PREPARE
     coordinator -> all participants: "can you commit?"
     each participant: make the change durable but DO NOT commit;
                       reply YES (and now it is BOUND) or NO

  PHASE 2 -- COMMIT or ABORT
     if all said YES: coordinator -> "commit"
     else:            coordinator -> "abort"

  *** THE BLOCKING PROBLEM ***
  A participant that voted YES and then loses the coordinator
  CANNOT decide alone. It cannot commit (others may have voted
  NO) and cannot abort (others may already have committed).
  It holds its locks and waits. Possibly for a long time.
""",
   "caption": "Two-phase commit is correct and blocking. The participant's "
              "locks are held until the coordinator returns.",
   "note": "The blocking failure is the whole reason 2PC has a bad "
           "reputation, and it is a real limitation, not an implementation "
           "flaw."},

  {"t": "callout", "title": "Three-phase commit does not fix it in practice",
   "kind": "An honest note",
   "body": ["3PC adds a round to make the outcome recoverable without the "
            "coordinator.",
            "<b>It assumes a synchronous network with bounded message "
            "delay</b>, which real networks do not provide.",
            "<b>Under an asynchronous network it is not correct</b>, and "
            "the extra round costs latency on every transaction.",
            "<b>So it is essentially unused.</b> The practical answer is to "
            "make the <i>coordinator</i> fault-tolerant with consensus "
            "(Part 4), which is what Spanner and its successors do."]},

  {"t": "section", "label": "Part 4", "title": "Consensus",
   "blurb": "Agreeing when machines fail."},

  {"t": "callout", "title": "What consensus provides",
   "kind": "Paxos and Raft",
   "body": ["<b>A set of machines agrees on a sequence of values</b>, "
            "surviving crashes and message loss, as long as a majority is "
            "reachable.",
            "<b>Used for the replicated log</b> (Module 11), so every "
            "replica applies the same changes in the same order.",
            "<b>Raft was designed for understandability</b> after Paxos "
            "proved notoriously hard to implement correctly — it "
            "separates leader election, log replication, and safety "
            "explicitly.",
            "<b>FLP says consensus is impossible with one faulty process in "
            "a fully asynchronous system</b>; real systems use timeouts and "
            "accept that liveness, not safety, is what can be lost."]},

  {"t": "table", "kicker": "Approaches", "title": "How real systems are built",
   "header": ["Approach", "Example", "Trade"],
   "widths": [3.0, 3.2, 5.9],
   "rows": [
     ["Single leader", "Postgres replicas", "<b>Simple; failover is the hard part</b>"],
     ["<b>Consensus replication</b>", "<b>Spanner, CockroachDB</b>", "<b>Strong consistency; coordination latency</b>"],
     ["Leaderless quorum", "Dynamo, Cassandra", "<b>Available; eventual consistency</b>"],
     ["Sharding", "Vitess, Citus", "Scales writes; <b>cross-shard queries are hard</b>"],
   ],
   "footnote": "Spanner uses synchronised clocks (TrueTime) to bound "
               "uncertainty and give external consistency — which "
               "needs atomic clocks and GPS.",
   "note": "TrueTime is worth mentioning: Google solved a software problem "
           "with hardware, which few others can."},

  {"t": "callout", "title": "What you give up, stated plainly",
   "kind": "The honest summary",
   "body": ["<b>Joins across shards</b> are either slow, restricted, or "
            "unsupported. Most systems restrict them.",
            "<b>Transactions across shards</b> cost a coordination round "
            "trip, and many systems do not offer them at all.",
            "<b>Secondary indexes</b> are either local to a shard (and so "
            "need scatter-gather) or global (and so need distributed "
            "updates).",
            "<b>Debugging</b> becomes distributed tracing, and a bug can "
            "live in the interaction rather than in any one machine.",
            "<b>And none of this gets easier later.</b> These are the "
            "permanent costs of the decision."]},
 ],
 "takeaways": [
   "The good reasons to distribute are availability and geography; capacity "
   "is rarer than claimed and throughput often does not require it.",
   "A commodity server with 2 TB of RAM and tens of terabytes of NVMe "
   "handles what needed a cluster fifteen years ago. Measure first.",
   "CAP says that <i>during a partition</i> you choose consistency or "
   "availability. It is not 'pick two of three', and it concerns one "
   "specific consistency model.",
   "PACELC adds the else clause: absent a partition, you choose latency or "
   "consistency — and that trade is paid on every request.",
   "Two-phase commit is correct and blocking: a participant that voted yes "
   "and lost the coordinator holds its locks and waits.",
   "Consensus makes the coordinator fault-tolerant. Raft was designed for "
   "understandability after Paxos proved hard to implement correctly.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why distribute"),
  ("table", ["Reason", "Assessment"],
   [["<b>Capacity</b> — the data does not fit on one machine.",
     "<b>Legitimate, and much rarer than claimed.</b> See below."],
    ["<b>Availability</b> — survive the loss of a machine.",
     "<b>Usually the real reason</b>, and a good one. Note that this needs "
     "<i>replication</i>, which is a far smaller step than sharding."],
    ["<b>Geography</b> — serve users from nearby.",
     "<b>Legitimate and unavoidable</b> when users are on several "
     "continents. The speed of light is not negotiable."],
    ["<b>Throughput</b> — more machines serving more queries.",
     "<b>Often a single machine suffices</b> once the obvious inefficiencies "
     "are addressed. Worth measuring before assuming."],
    ["<b>Resume-driven development</b>",
     "It happens, and it is worth being honest that it happens."]],
   [0.39, 0.61]),
  ("callout", "A single machine is larger than most people assume",
   ["<b>A commodity server available today</b> has on the order of 128 "
    "cores, 1 to 2 terabytes of RAM, and tens of terabytes of NVMe storage "
    "delivering millions of IOPS.",
    "<b>That configuration handles workloads that genuinely required a "
    "cluster fifteen years ago</b> — and handles them with full ACID "
    "transactions, arbitrary joins, a single process to profile, and a "
    "single machine to restart.",
    "<b>What distribution costs:</b> joins across shards become slow or "
    "unsupported; transactions across shards require coordination or are "
    "unavailable; network partitions become a routine operational event "
    "rather than a disaster; and the operational complexity is permanent "
    "— it does not diminish once the system is built.",
    "<b>So measure before distributing.</b> 'We might need to scale "
    "eventually' is not a measurement, and the cost of distributing "
    "unnecessarily is paid every day by everyone who works on the system, "
    "while the cost of distributing later is paid once by a team that by "
    "then understands the workload."]),

  ("h1", "2 &nbsp; CAP and PACELC"),
  ("callout", "CAP, stated precisely",
   ["<b>In the presence of a network partition, a distributed system must "
    "choose between consistency and availability.</b> That is the theorem.",
    "<b>It is not 'pick two of three'.</b> Partitions are not something you "
    "choose; they are something that happens to you. The theorem describes "
    "the choice you face <i>when one occurs</i>, which is a much narrower "
    "and more useful claim.",
    "<b>And the terms are specific.</b> 'Consistency' here means "
    "<b>linearizability</b> — every read returns the most recent write, "
    "as though there were a single copy. 'Availability' means <i>every</i> "
    "request to a non-failed node receives a response. Both are stronger "
    "than most real systems need or provide.",
    "<b>So the 'CP' and 'AP' labels convey far less than they appear to</b>, "
    "and most marketing use of CAP is either imprecise or wrong. Brewer "
    "himself wrote a retrospective saying as much."]),
  ("callout", "PACELC is the more useful framing",
   ["Daniel Abadi's formulation: <b>if there is a Partition, choose between "
    "Availability and Consistency; Else, choose between Latency and "
    "Consistency.</b>",
    "<b>The 'else' clause is the important addition.</b> Partitions are "
    "rare — perhaps a few times a year. <b>The latency/consistency "
    "trade is paid on every single request, forever.</b>",
    "<b>Strong consistency requires coordination:</b> a write must reach a "
    "quorum before it is acknowledged. Within a datacentre that is a "
    "millisecond or two; across regions it is tens to hundreds of "
    "milliseconds, bounded below by the speed of light.",
    "<b>So the everyday cost of consistency is latency, not "
    "availability.</b> That is the trade an architect actually makes, and "
    "CAP's focus on the rare case obscures it. PACELC's contribution is "
    "putting the common case in the name."]),

  ("break",),
  ("h1", "3 &nbsp; Distributed transactions"),
  ("code", """PHASE 1 -- PREPARE
   coordinator -> all participants: "can you commit?"
   each participant: make the change DURABLE but do not commit;
                     reply YES (now BOUND) or NO

PHASE 2 -- COMMIT or ABORT
   all YES -> coordinator broadcasts "commit"
   any NO  -> coordinator broadcasts "abort"

THE BLOCKING PROBLEM: a participant that voted YES and then loses
the coordinator CANNOT decide alone. It cannot commit (someone may
have voted NO) and cannot abort (others may already have committed).
It holds its locks and waits."""),
  ("callout", "Two-phase commit is correct and blocking",
   ["The protocol is correct: no execution results in some participants "
    "committing while others abort.",
    "<b>But a participant that has voted yes has surrendered its "
    "autonomy.</b> It has made its changes durable and promised to commit if "
    "asked; it cannot unilaterally abort, because others may have been told "
    "to commit, and it cannot unilaterally commit, because someone may have "
    "voted no.",
    "<b>So if the coordinator fails after collecting votes and before "
    "announcing the outcome, every prepared participant holds its locks and "
    "waits</b> — indefinitely, until the coordinator recovers and "
    "consults its log. Those locks block other transactions, so the failure "
    "of one machine stalls work on all the others.",
    "<b>This is the real limitation, and it is structural rather than an "
    "implementation flaw.</b> It is why distributed transactions have the "
    "reputation they do."]),
  ("callout", "Three-phase commit does not solve it in practice",
   ["3PC inserts an additional round — 'pre-commit' — so that a "
    "participant that loses the coordinator can determine the outcome by "
    "consulting its peers.",
    "<b>It assumes a synchronous network with a known bound on message "
    "delay</b>, so that the absence of a message within the bound proves "
    "failure.",
    "<b>Real networks are asynchronous</b> — a message may be "
    "arbitrarily delayed and then arrive — and under asynchrony 3PC is "
    "not correct. It can produce inconsistent outcomes when a slow node is "
    "mistaken for a failed one. The additional round also costs latency on "
    "every transaction, including the overwhelming majority that encounter "
    "no failure.",
    "<b>So it is essentially unused.</b> <b>The practical answer is to make "
    "the coordinator itself fault-tolerant using consensus</b> (&sect;4), so "
    "that it never becomes unavailable in the first place. This is what "
    "Spanner, CockroachDB, and their successors do, and it is why consensus "
    "and distributed transactions are studied together."]),

  ("h1", "4 &nbsp; Consensus"),
  ("callout", "What consensus provides, and its limit",
   ["<b>A set of machines agrees on a sequence of values</b>, tolerating "
    "crashes and lost or delayed messages, provided a majority remains "
    "reachable.",
    "<b>In a database it is used for the replicated log</b> (Module 11): if "
    "every replica agrees on the same log in the same order, every replica "
    "reaches the same state. The log, once again, turns out to be the right "
    "primitive.",
    "<b>Raft was designed explicitly for understandability</b>, after a "
    "decade in which Paxos proved notoriously difficult to implement "
    "correctly — the original paper leaves substantial gaps between the "
    "algorithm and a working system. Raft separates leader election, log "
    "replication, and the safety argument into distinct, individually "
    "comprehensible mechanisms. That is a legitimate and unusual design "
    "goal, and it worked: Raft implementations are widespread.",
    "<b>The FLP impossibility result</b> shows that consensus cannot be "
    "guaranteed in a fully asynchronous system with even one faulty process. "
    "<b>Real systems use timeouts</b> and thereby sacrifice guaranteed "
    "<i>liveness</i> — progress may stall — while preserving "
    "<i>safety</i>: they never produce an inconsistent result. Stalling is "
    "recoverable; inconsistency is not."]),
  ("table", ["Approach", "Examples", "Trade"],
   [["<b>Single leader with replicas</b>",
     "PostgreSQL streaming replication, MySQL.",
     "<b>Simple and well understood.</b> Failover is the hard part — "
     "deciding the leader is dead, and avoiding two leaders."],
    ["<b>Consensus replication</b>",
     "<b>Spanner, CockroachDB, TiDB, etcd.</b>",
     "<b>Strong consistency with automatic failover</b>, at the cost of a "
     "coordination round trip on every write."],
    ["<b>Leaderless quorum</b>", "Dynamo, Cassandra, Riak.",
     "<b>Highly available and eventually consistent.</b> Conflicts must be "
     "resolved by the application or by CRDTs."],
    ["<b>Sharding</b>", "Vitess, Citus, application-level sharding.",
     "Scales writes by partitioning the key space. <b>Cross-shard queries "
     "and transactions are the difficulty</b>, and the shard key choice is "
     "effectively permanent."]],
   [0.21, 0.30, 0.49]),
  ("p", "<b>Spanner's TrueTime</b> deserves a mention: Google bounded clock "
        "uncertainty using GPS receivers and atomic clocks in every "
        "datacentre, so a transaction can simply wait out the uncertainty "
        "interval and thereby achieve externally consistent global "
        "timestamps. <b>It is a software problem solved with hardware</b>, "
        "which few organisations can replicate — though cloud providers "
        "now expose bounded-uncertainty clocks, which is beginning to change "
        "that."),
  ("callout", "What you give up, stated plainly",
   ["<b>Joins across shards</b> are slow, restricted, or unsupported. Most "
    "systems require that joined tables be co-located by the shard key, "
    "which constrains the schema permanently.",
    "<b>Transactions across shards</b> require a coordination round trip at "
    "best, and many systems simply do not offer them — pushing the "
    "problem to the application, which solves it worse.",
    "<b>Secondary indexes</b> are either local to each shard, requiring a "
    "scatter-gather query across every shard to use them, or global, "
    "requiring a distributed update on every write. Neither is good.",
    "<b>Debugging becomes distributed tracing.</b> A bug can live in the "
    "<i>interaction</i> between machines rather than in any one of them, and "
    "it may be unreproducible because it depends on timing.",
    "<b>And none of this gets easier later.</b> These are the permanent "
    "costs of the decision, paid continuously — which is why &sect;1 "
    "argues for measuring before committing to them."]),
 ],
 "resources": [
   ("Kleppmann &mdash; Designing Data-Intensive Applications",
    "https://dataintensive.net/",
    "The best single book on this material. Chapters 5 through 9 cover "
    "everything in this module with more care and more examples."),
   ("Abadi &mdash; Consistency Tradeoffs in Modern Distributed Database "
    "System Design (PACELC, free)",
    "https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf",
    "The &sect;2 framing, in the original. Short."),
   ("Ongaro & Ousterhout &mdash; In Search of an Understandable Consensus "
    "Algorithm (Raft, free)",
    "https://raft.github.io/raft.pdf",
    "Raft. The paper is readable, and the site has an animated visualisation "
    "that makes leader election obvious."),
   ("Corbett et al. &mdash; Spanner (free)",
    "https://research.google/pubs/pub39966/",
    "TrueTime and externally consistent distributed transactions. Read it "
    "for the clock argument."),
   ("Jepsen &mdash; analyses of real distributed databases",
    "https://jepsen.io/analyses",
    "What systems actually do under partition, as opposed to what they "
    "claim. Essential reading before trusting any consistency claim."),
 ],
 "exercises": [
   "For a workload you know, estimate whether a single large machine would "
   "suffice. State the numbers: data size, write rate, query rate.",
   "Benchmark a single PostgreSQL instance on a modern machine and find its "
   "actual limits for your workload before assuming it needs distributing.",
   "State CAP precisely in your own words, then find three online claims "
   "about it that are wrong and say why.",
   "Classify five systems you know using PACELC and justify each "
   "classification.",
   "Implement two-phase commit across three processes. Then kill the "
   "coordinator after the prepare phase and observe the participants block.",
   "Measure how long participants hold locks in that scenario and what else "
   "it blocks.",
   "Implement Raft leader election. Kill the leader and verify a new one is "
   "elected within the expected time.",
   "Measure write latency for a single node, a three-node consensus group in "
   "one datacentre, and a simulated cross-region group.",
   "Set up a two-shard system and write a query requiring a cross-shard "
   "join. Implement it and measure the cost against the co-located version.",
   "Read one Jepsen analysis in full and write a page on what the system "
   "claimed, what it actually did, and why the gap existed.",
 ],
 "selfcheck": [
   "Give five reasons people distribute and assess each.",
   "What does a single modern server handle, and what does distribution "
   "cost?",
   "State CAP precisely and give two things it does not say.",
   "State PACELC and explain why the else clause matters more.",
   "Describe two-phase commit and explain the blocking problem exactly.",
   "Why does three-phase commit not solve it in practice?",
   "What does consensus provide, and what does Raft contribute over Paxos?",
   "What does FLP say, and what do real systems sacrifice?",
   "Compare four replication and partitioning approaches.",
   "Name four things you permanently give up by distributing.",
 ],
},

]
