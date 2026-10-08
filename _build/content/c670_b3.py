# -*- coding: utf-8 -*-
"""CSCE 670 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Vector Search at Scale",
 "subtitle": "Nearest neighbours when exact is impossible.",
 "question": "How do you search a billion vectors in milliseconds?",
 "outcomes": [
     "Explain why exact search does not scale.",
     "Explain the graph-based and partition-based "
     "approaches.",
     "Explain quantisation and what it costs.",
     "Explain the recall-latency-memory trade.",
     "Choose and tune an index against a stated requirement.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why approximate",
   "blurb": "Exact search is linear, and linear is too slow."},

  {"t": "callout", "title": "Exact nearest-neighbour search in high dimension is linear in the collection, with no better option",
   "kind": "The result that forces approximation",
   "body": ["<b>A brute-force scan computes every distance</b> "
            "— which is a few hundred million operations for a "
            "million 768-dimensional vectors, per query.",
            "<b>And the tree structures that work in low dimension "
            "fail here.</b> <b>A k-d tree degenerates to a full scan "
            "above roughly twenty dimensions</b>, because of "
            "CSCE 676 §05 §1's distance "
            "concentration.",
            "<b>So the honest position is that exact search is "
            "unavailable at scale</b> — and <b>approximate search "
            "with a measured recall is the only option</b>, not a "
            "shortcut.",
            "<b>Which makes recall the quantity to "
            "measure:</b> <b>what fraction of the true nearest "
            "neighbours did you actually return?</b> — and it is "
            "measurable by brute force on a sample, which is the "
            "exercise."]},

  {"t": "section", "label": "Part 2", "title": "The two families",
   "blurb": "Graphs and partitions."},

  {"t": "code", "kicker": "Families", "title": "How each one works",
   "lang": "text", "code": """
  GRAPH-BASED (HNSW)
      build a navigable graph: each vector links to
      some near neighbours, in layers of decreasing
      sparsity. Search greedily from the top layer
      down, following the closest link each time.
      Excellent recall at low latency; large memory;
      slow to build; awkward to delete from.

  PARTITION-BASED (IVF)
      cluster the vectors (k-means), store an
      inverted list per centroid. At query time,
      search only the nearest few lists.
      Compact, fast to build, and recall depends on
      how many lists you probe -- which is a dial.

  AND THE HASHING FAMILY (LSH)
      CSCE 676 Module 02's construction, applied to
      vectors. Strong guarantees, and beaten in
      practice by the two above, which have none.

  SO: HNSW for quality, IVF for memory and build
  time, and both are usually combined with Part 3.
""",
   "caption": "<b>The methods with guarantees lost to the methods "
              "without them</b> — which is worth noticing honestly, "
              "and is unusual.",
   "note": "The guarantee-versus-performance point is an honest "
           "observation about the field."},

  {"t": "callout", "title": "And the recall dial is what makes these usable",
   "kind": "The practical property",
   "body": ["<b>Both families expose a parameter that trades recall "
            "against latency</b> — the number of lists probed, or "
            "the size of the search frontier.",
            "<b>So you can set the operating point from a "
            "requirement</b> rather than accepting whatever the "
            "default gives — <b>which is the difference between "
            "engineering and configuration.</b>",
            "<b>And the curve is steep at the top:</b> <b>going from "
            "95% to 99% recall frequently costs several times the "
            "latency</b>, which is a decision worth making "
            "deliberately.",
            "<b>Which depends on the stage:</b> <b>a first-stage "
            "retriever feeding a reranker over 500 candidates needs "
            "recall at 500, not at 10</b> — and that is a much easier "
            "target (Module 06 §4)."]},

  {"t": "section", "label": "Part 3", "title": "Quantisation",
   "blurb": "Because the vectors themselves are the memory problem."},

  {"t": "code", "kicker": "Compression", "title": "Making the vectors smaller",
   "lang": "text", "code": """
  THE PROBLEM
      a billion 768-dimensional float32 vectors is
      about 3 TB. The index structure is a small
      fraction of that; the vectors are the cost.

  SCALAR QUANTISATION
      float32 -> int8. Four times smaller, small
      recall loss, and trivial to implement. Do this
      first.

  PRODUCT QUANTISATION
      split each vector into m subvectors, cluster
      each subspace separately, store m centroid
      ids. 768 floats -> 96 bytes is routine.
      Distances are computed from precomputed tables,
      which is also faster.

  BINARY QUANTISATION
      one bit per dimension. 32x smaller, and it
      needs a reranking pass over the full vectors
      to recover the lost precision.

  AND THE PATTERN: quantise for the search, then
  rerank the top candidates with exact distances.
""",
   "caption": "<b>Quantise to search, then rerank exactly</b> — "
              "the same two-stage logic as "
              "Module 06 §4, one level down.",
   "note": "The recurring two-stage pattern is worth naming "
           "explicitly."},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "Against a stated requirement."},

  {"t": "bullets", "kicker": "Choosing", "title": "How to pick and tune an index",
   "items": [
     "<b>State the requirement first:</b> <b>recall at k, the "
     "latency budget, the memory budget, and the update "
     "rate</b> — all four, because they conflict.",
     "",
     "<b>Measure recall by brute force on a sample</b> of a few "
     "thousand queries — <b>which is the only way to know, and "
     "it is cheap.</b>",
     "",
     "<b>Then: HNSW if memory permits and updates are "
     "rare</b>; IVF with product quantisation if memory is tight or "
     "the collection grows.",
     "",
     "<b>And tune the probe or frontier parameter against your "
     "latency budget</b>, reading the recall off the curve rather than "
     "accepting a default.",
     "",
     "<b>Beware of deletes.</b> <b>Graph indexes handle deletion "
     "badly</b>, usually by tombstoning and periodic rebuild — "
     "which is an operational cost.",
   ],
   "footnote": "<b>The update rate is the requirement most often "
               "forgotten</b> — and it is the one that rules out the "
               "highest-quality index."},

  {"t": "callout", "title": "And what this costs compared to a lexical index",
   "kind": "Closing",
   "body": ["<b>Memory, substantially:</b> <b>a dense index is "
            "typically much larger than an inverted index over the same "
            "collection</b>, even quantised.",
            "<b>Build time, substantially</b> — and <b>a full "
            "rebuild on every embedding model change</b> "
            "(Module 07 §4).",
            "<b>And operational complexity:</b> <b>the recall "
            "parameter is a quality knob that does not exist in a lexical "
            "system</b>, and a misconfigured one degrades results "
            "silently.",
            "<b>Which is worth stating because the comparison is "
            "usually made on quality alone</b> — <b>and the right "
            "comparison includes the memory, the rebuild, and the extra "
            "thing that can be set wrong.</b>"]},
 ],
 "takeaways": [
   "Exact nearest-neighbour search in high dimension is linear with no "
   "better option, because distance concentration defeats tree structures.",
   "The methods with strong guarantees lost in practice to the methods "
   "with none, which is unusual and worth noticing honestly.",
   "Both families expose a recall-latency dial, so you can set the "
   "operating point from a requirement rather than a default.",
   "A first-stage retriever feeding a reranker needs recall at 500 rather "
   "than at 10, which is a much easier target.",
   "The vectors rather than the index structure are the memory cost, which "
   "is why quantisation matters.",
   "Quantise to search then rerank exactly — the same two-stage logic "
   "one level down.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why approximate"),
  ("callout", "Exact nearest-neighbour search in high dimension is linear in "
              "the collection, with no better option",
   ["<b>A brute-force scan computes the distance to every "
    "vector</b> — which is a few hundred million floating-point "
    "operations for a million 768-dimensional vectors, <b>per query</b>, "
    "and scales linearly from there.",
    "<b>And the tree structures that work well in low dimension fail "
    "here.</b> <b>A k-d tree degenerates to something close to a full "
    "scan above roughly twenty dimensions</b>, because of <b>CSCE 676 "
    "Module 05 &sect;1's distance concentration</b>: the pruning "
    "bounds stop pruning when all the distances are similar.",
    "<b>So the honest position is that exact search is simply "
    "unavailable at scale</b> — and <b>approximate search with a "
    "measured recall is the only option rather than a shortcut</b>, which "
    "is <b>CSCE 676 Module 01 &sect;2's framing</b> arriving in this "
    "course.",
    "<b>Which makes recall the quantity to measure:</b> <b>what "
    "fraction of the true nearest neighbours did your index actually "
    "return?</b> — and <b>it is measurable by brute force on a "
    "sample of a few thousand queries</b>, which is cheap and is the "
    "exercise nobody runs."]),

  ("h1", "2 &nbsp; The two families"),
  ("code", """GRAPH-BASED (HNSW)
    build a navigable small-world graph: each vector
    links to some of its near neighbours, in layers
    of decreasing sparsity. Search greedily from the
    top layer down, following the closest link at
    each step.
    Excellent recall at low latency; large memory;
    slow to build; awkward to delete from.

PARTITION-BASED (IVF)
    cluster the vectors with k-means, and store an
    inverted list per centroid. At query time,
    search only the nearest few lists.
    Compact, fast to build, and the recall depends on
    how many lists you probe -- which is a dial.

AND THE HASHING FAMILY (LSH)
    CSCE 676 Module 02's construction, applied to
    vectors. Strong provable guarantees, and beaten
    in practice by the two above, which have none.

SO: HNSW for quality, IVF for memory and build time,
and both are usually combined with section 3."""),
  ("p", "<b>The methods with strong guarantees lost in practice to the "
        "methods without them</b> — <b>which is worth noticing "
        "honestly, and is unusual</b>. Locality-sensitive hashing has a "
        "provable recall bound and HNSW has none, and HNSW is what "
        "everybody deploys. <b>The guarantee-versus-performance "
        "observation is an honest one about this field</b>, and the lesson "
        "is that a guarantee is valuable when it is tight and a loose "
        "guarantee may be worth less than a measured empirical "
        "result (Module 05's measurement discipline applied to "
        "algorithms)."),
  ("callout", "And the recall dial is what makes these usable",
   ["<b>Both families expose a parameter that trades recall against "
    "latency</b> — the number of inverted lists probed in IVF, or "
    "the size of the search frontier in HNSW — and both are "
    "adjustable at query time without rebuilding.",
    "<b>So you can set the operating point from a requirement</b> "
    "rather than accepting whatever the library default happens to "
    "give — <b>which is the difference between engineering the "
    "system and configuring it</b>, and is Module 08 &sect;4's "
    "discipline.",
    "<b>And the curve is steep at the top:</b> <b>going from 95% to "
    "99% recall frequently costs several times the latency</b>, which is "
    "<b>a decision worth making deliberately</b> rather than by "
    "accepting a round number.",
    "<b>Which depends entirely on the stage you are serving:</b> <b>a "
    "first-stage retriever feeding a cross-encoder reranker over 500 "
    "candidates needs recall at 500, not recall at 10</b> — and "
    "<b>that is a very much easier target</b> (Module 06 &sect;4), "
    "which means the right operating point is far cheaper than it first "
    "appears."]),

  ("break",),
  ("h1", "3 &nbsp; Quantisation"),
  ("code", """THE PROBLEM
    a billion 768-dimensional float32 vectors is
    about 3 TB. The index structure is a small
    fraction of that; the VECTORS are the cost.

SCALAR QUANTISATION
    float32 -> int8. Four times smaller, a small
    recall loss, and trivial to implement. Do this
    first, before anything more sophisticated.

PRODUCT QUANTISATION
    split each vector into m subvectors, cluster each
    subspace separately, and store m centroid ids.
    768 floats -> 96 bytes is routine. Distances are
    computed from precomputed lookup tables, which
    is also faster than arithmetic on the originals.

BINARY QUANTISATION
    one bit per dimension. 32 times smaller, and it
    requires a reranking pass over the full vectors
    to recover the lost precision.

AND THE PATTERN: quantise for the search, then rerank
the top candidates with exact distances."""),
  ("p", "<b>Quantise to search, then rerank exactly</b> — which is "
        "<b>the same two-stage logic as Module 06 &sect;4, one level "
        "down</b>: use a cheap approximation to narrow the candidate set, "
        "then an expensive exact computation to order it. <b>The "
        "recurring two-stage pattern is worth naming explicitly</b>, "
        "because it appears at three levels in this course — retrieve "
        "then rerank, quantise then rerank, and chunk then expand "
        "(CSCE 638 Module 11 &sect;3) — and recognising it makes "
        "each instance easier to reason about."),

  ("h1", "4 &nbsp; Choosing and tuning"),
  ("ul", ["<b>State the requirement first:</b> <b>recall at k, the "
          "latency budget, the memory budget, and the update "
          "rate</b> — <b>all four, because they conflict</b> and "
          "because no index is best on all of them.",
          "<b>Measure recall by brute force on a sample</b> of a few "
          "thousand queries against the full collection — <b>which "
          "is the only way to actually know, and it is cheap</b> since it "
          "is done once offline.",
          "<b>Then: HNSW if memory permits and updates are "
          "rare</b>; <b>IVF with product quantisation if memory is tight "
          "or the collection grows continuously</b> — which covers "
          "most real decisions.",
          "<b>And tune the probe or frontier parameter against your "
          "latency budget</b>, <b>reading the recall off the measured "
          "curve rather than accepting a default</b> — the curve "
          "takes an afternoon to produce and is reusable.",
          "<b>Beware of deletes.</b> <b>Graph indexes handle deletion "
          "badly</b>, usually by marking tombstones and rebuilding "
          "periodically — <b>which is a real operational cost</b> "
          "that does not appear in any benchmark. <b>The update rate is "
          "the requirement most often forgotten</b>, and <b>it is the one "
          "that rules out the highest-quality index.</b>"]),
  ("callout", "And what this costs compared to a lexical index",
   ["<b>Memory, substantially:</b> <b>a dense index is typically very "
    "much larger than an inverted index over the same collection</b>, "
    "even after quantisation — because an inverted index stores only "
    "the terms that appear and a dense index stores a full vector per "
    "document.",
    "<b>Build time, substantially</b> — encoding every document "
    "through a transformer is far more expensive than tokenising "
    "it — and <b>a full rebuild is required on every embedding model "
    "change</b> (Module 07 &sect;4's commitment).",
    "<b>And operational complexity:</b> <b>the recall parameter is a "
    "quality knob that simply does not exist in a lexical system</b>, "
    "and <b>a misconfigured one degrades results silently</b> with no "
    "error and no obvious symptom.",
    "<b>Which is worth stating because the comparison between lexical "
    "and dense retrieval is usually made on quality alone</b> — and "
    "<b>the right comparison includes the memory, the rebuild cost, and "
    "the additional thing that can be set wrong</b>, all of which favour "
    "the lexical index and none of which appear in a benchmark "
    "table."]),
 ],
 "resources": [
   ("Malkov & Yashunin &mdash; HNSW (free)",
    "https://arxiv.org/abs/1603.09320",
    "<b>&sect;2's first family in the original</b> — the layered "
    "navigable graph, and why greedy search on it works."),
   ("J&eacute;gou, Douze & Schmid &mdash; Product Quantization (free)",
    "https://inria.hal.science/inria-00514462/",
    "<b>&sect;3's main technique</b> — the subspace decomposition and "
    "the lookup-table distance computation."),
   ("The FAISS documentation and wiki (free)",
    "https://github.com/facebookresearch/faiss/wiki",
    "<b>&sect;4 practically</b> — the index type guidance, which is "
    "the best available decision tree for this."),
   ("ANN-Benchmarks (free)",
    "https://ann-benchmarks.com/",
    "<b>&sect;2 and &sect;4 measured</b> — recall against latency "
    "across methods and datasets, which is how to compare them."),
 ],
 "exercises": [
   "<b>Time a brute-force scan</b> over a million vectors and "
   "extrapolate to a billion.",
   "<b>Build a k-d tree</b> and measure its pruning effectiveness at "
   "5, 20, and 100 dimensions.",
   "<b>Measure recall by brute force</b> for an approximate index on a "
   "thousand queries.",
   "<b>Build HNSW and IVF</b> on the same vectors and compare memory, "
   "build time, and the recall-latency curve.",
   "<b>Plot the recall-latency curve</b> and find the cost of going "
   "from 95% to 99%.",
   "<b>Measure recall at 10 and at 500</b> for the same index, and "
   "explain the difference.",
   "<b>Apply scalar quantisation</b> and measure the memory saving and "
   "recall loss.",
   "<b>Apply product quantisation</b> at two compression levels and "
   "compare.",
   "<b>Add an exact reranking pass</b> over the top 100 and measure the "
   "recall recovery.",
   "<b>Delete 10% of your HNSW index</b> and report what happens.",
 ],
 "selfcheck": [
   "Why is exact high-dimensional search linear, and why do trees "
   "fail?",
   "What quantity should you measure, and how?",
   "Describe HNSW and IVF, and the trade between them.",
   "What is unusual about which family won?",
   "What does the recall dial let you do, and why is the curve steep at "
   "the top?",
   "Why does the stage determine the recall target?",
   "Why are the vectors rather than the index the memory problem?",
   "Name three quantisation methods and the pattern they share.",
   "Give the four requirements to state, and which is most often "
   "forgotten?",
   "Name three costs of a dense index over a lexical one.",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Query Understanding",
 "subtitle": "Working out what was meant.",
 "question": "What can you do with the query before you search?",
 "outcomes": [
     "Explain spelling correction and its requirements.",
     "Explain query expansion and its risk.",
     "Explain relevance feedback, explicit and implicit.",
     "Explain query segmentation and intent "
     "classification.",
     "Build a query understanding pipeline and measure it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Correction",
   "blurb": "The highest-value preprocessing there is."},

  {"t": "callout", "title": "A misspelled query returns nothing useful, and a large fraction of queries are misspelled",
   "kind": "Why this comes first",
   "body": ["<b>Measured misspelling rates in real query logs are "
            "substantial</b> — and <b>a misspelled rare term "
            "matches no documents at all</b>, so the failure is total "
            "rather than degraded.",
            "<b>And the correction must use the collection and the "
            "query log, not a dictionary</b> — because <b>the right "
            "correction depends on what people search for and what "
            "documents exist</b>, which a dictionary does not "
            "know.",
            "<b>So the standard approach is a noisy channel "
            "model:</b> <b>choose the correction maximising P(intended) "
            "× P(typed | intended)</b>, with the prior from the "
            "query log and the error model from edit distance.",
            "<b>And the interface matters as much as the "
            "model:</b> <b>correct silently when confident, offer 'did "
            "you mean' when not, and always allow the original</b> "
            "— because a wrong confident correction is "
            "infuriating."]},

  {"t": "section", "label": "Part 2", "title": "Expansion",
   "blurb": "Adding terms, and the drift it risks."},

  {"t": "code", "kicker": "Expansion", "title": "The methods, and the danger",
   "lang": "text", "code": """
  PSEUDO-RELEVANCE FEEDBACK
      run the query, assume the top k results are
      relevant, extract their distinctive terms, add
      them, run again. Needs no user input and is
      the standard method.

  THESAURUS AND EMBEDDING EXPANSION
      add synonyms, or the nearest neighbours of the
      query terms in an embedding space
      (CSCE 638 Module 04).

  QUERY LOG EXPANSION
      add terms from queries that led to the same
      clicked documents. Often the best source,
      because it reflects actual intent.

  AND THE DANGER IS DRIFT
      if the top k were about the wrong topic, the
      expansion amplifies the error -- and the
      second query is now confidently wrong. Which
      is why expansion helps on average and can hurt
      badly on individual queries.

  SO: weight expansion terms below the original, and
  report the per-query distribution, not the mean.
""",
   "caption": "<b>Expansion helps on average and hurts badly on "
              "individual queries</b> — which is exactly why "
              "Module 05 §4's per-query reporting "
              "matters.",
   "note": "Query drift is the concrete case for per-query "
           "reporting."},

  {"t": "section", "label": "Part 3", "title": "Feedback",
   "blurb": "Using what the user does."},

  {"t": "bullets", "kicker": "Feedback", "title": "Explicit and implicit, and what each is worth",
   "items": [
     "<b>Explicit relevance feedback</b> — the user marks "
     "results as relevant and the query is reformulated. <b>It works "
     "very well and almost nobody will do it</b>, which is a usability "
     "finding rather than a technical one.",
     "",
     "<b>Rocchio's method is the classical "
     "formulation:</b> <b>move the query vector toward the relevant "
     "documents and away from the non-relevant</b> ones.",
     "",
     "<b>Implicit feedback</b> — clicks, dwell, "
     "reformulations, and abandonment. <b>Abundant, biased, and the "
     "only kind you will actually get</b> "
     "(Module 05 §4).",
     "",
     "<b>And session context is the strongest implicit "
     "signal:</b> <b>the previous query in a session usually "
     "disambiguates the current one</b>.",
     "",
     "<b>Which makes reformulation detection valuable</b> — a "
     "reformulated query is a reported failure of the previous "
     "one.",
   ],
   "footnote": "<b>A reformulation is a user telling you the last "
               "result was wrong</b> — which is a free, strong, and "
               "widely ignored quality signal."},

  {"t": "section", "label": "Part 4", "title": "Structure and intent",
   "blurb": "Understanding the query as more than a bag of words."},

  {"t": "bullets", "kicker": "Understanding", "title": "What else can be extracted",
   "items": [
     "<b>Segmentation</b> — which adjacent words form a "
     "phrase. <b>'New York hotel' is two units and not three "
     "words</b>, and treating it as three retrieves badly.",
     "",
     "<b>Entity recognition and linking</b> — identifying "
     "that a span names a specific known thing, which enables "
     "structured retrieval against a knowledge base.",
     "",
     "<b>Intent classification</b> "
     "(Module 01 §3) — which determines the result "
     "presentation as much as the ranking.",
     "",
     "<b>Attribute extraction</b> — 'red shoes under £50' "
     "contains a colour, a category, and a price filter, which should "
     "become structured constraints.",
     "",
     "<b>And none of it is free:</b> <b>each component adds "
     "latency and a failure mode</b>, so measure the end-to-end effect "
     "rather than the component's accuracy.",
   ],
   "footnote": "<b>Measure the end-to-end effect, not the component's "
               "accuracy</b> — a 95%-accurate intent classifier may "
               "hurt overall quality if the 5% are confidently "
               "misrouted."},

  {"t": "callout", "title": "And a language model changes what is available here",
   "kind": "The current shift, stated proportionately",
   "body": ["<b>Query rewriting, expansion, and reformulation are all "
            "things a language model does well</b> — and it can "
            "resolve a pronoun against a session, decompose a compound "
            "question, or generate a hypothetical answer to retrieve "
            "against.",
            "<b>Which is a real improvement over the classical "
            "methods</b> for conversational and complex "
            "queries (Module 11).",
            "<b>At a cost that is easy to understate:</b> <b>a model "
            "call before retrieval adds latency to every query and a "
            "failure mode that is hard to bound</b> "
            "(Module 04 §4).",
            "<b>So the honest position: use it where the query is "
            "genuinely hard, and not on the head of the "
            "distribution</b> — <b>where a cached classical pipeline "
            "is both faster and more predictable.</b>"]},
 ],
 "takeaways": [
   "A misspelled rare term matches no documents at all, so the failure is "
   "total rather than degraded.",
   "Spelling correction must use the collection and the query log rather "
   "than a dictionary, because the right correction depends on both.",
   "Query expansion helps on average and hurts badly on individual "
   "queries, which is why per-query reporting matters.",
   "Explicit relevance feedback works very well and almost nobody will do "
   "it, which is a usability finding rather than a technical one.",
   "A reformulation is a user telling you the last result was wrong — "
   "a free, strong, and widely ignored signal.",
   "Measure the end-to-end effect of a query understanding component "
   "rather than its own accuracy.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Spelling correction"),
  ("callout", "A misspelled query returns nothing useful, and a large "
              "fraction of queries are misspelled",
   ["<b>Measured misspelling rates in real query logs are "
    "substantial</b> — well into the double digits for some "
    "domains — and <b>a misspelled rare term matches no documents at "
    "all</b>, so <b>the failure is total rather than degraded</b>, which "
    "makes this the highest-value preprocessing step in the "
    "course.",
    "<b>And the correction must use the collection and the query log "
    "rather than a dictionary</b> — because <b>the right correction "
    "depends on what people actually search for and what documents "
    "actually exist</b>, which a dictionary has no information about. A "
    "dictionary will happily correct a correct product name into an "
    "English word.",
    "<b>So the standard approach is a noisy channel model:</b> "
    "<b>choose the candidate correction maximising P(intended) &times; "
    "P(typed | intended)</b>, with <b>the prior estimated from the query "
    "log and the error model from weighted edit distance</b> — which "
    "handles keyboard adjacency and common substitutions.",
    "<b>And the interface matters at least as much as the "
    "model:</b> <b>correct silently when the model is confident, offer "
    "'did you mean' when it is not, and always leave the original "
    "reachable</b> — because <b>a wrong confident correction is "
    "infuriating</b> and loses more trust than the correction gains "
    "(CSCE 701 Module 11's usability argument)."]),

  ("h1", "2 &nbsp; Expansion"),
  ("code", """PSEUDO-RELEVANCE FEEDBACK
    run the query, assume the top k results are
    relevant, extract their distinctive terms, add
    them to the query, and run it again. Needs no
    user input at all, and is the standard method.

THESAURUS AND EMBEDDING EXPANSION
    add synonyms from a thesaurus, or the nearest
    neighbours of the query terms in an embedding
    space (CSCE 638 Module 04).

QUERY LOG EXPANSION
    add terms from other queries that led to the same
    clicked documents. Frequently the best source,
    because it reflects actual expressed intent
    rather than semantic similarity.

AND THE DANGER IS DRIFT
    if the top k results were about the wrong topic,
    the expansion amplifies the error -- and the
    second query is now confidently wrong. Which is
    why expansion helps on average and can hurt badly
    on individual queries.

SO: weight the expansion terms below the originals,
and report the per-query distribution, not the mean."""),
  ("p", "<b>Expansion helps on average and hurts badly on individual "
        "queries</b> — <b>which is exactly why Module 05 "
        "&sect;4's per-query reporting matters</b>, and is the cleanest "
        "concrete case for it in the course. A mean NDCG improvement from "
        "expansion routinely conceals a subset of queries made much worse, "
        "and those queries are the ones users complain about. <b>Query "
        "drift is the concrete argument for per-query reporting</b>, and "
        "it generalises to every averaged improvement."),

  ("h1", "3 &nbsp; Feedback"),
  ("ul", ["<b>Explicit relevance feedback</b> — the user marks "
          "some results as relevant and the query is automatically "
          "reformulated. <b>It works very well and almost nobody will "
          "do it</b>, which is <b>a usability finding rather than a "
          "technical one</b> and is why the method is historically "
          "important and practically rare.",
          "<b>Rocchio's method is the classical formulation:</b> "
          "<b>move the query vector toward the centroid of the relevant "
          "documents and away from the centroid of the non-relevant "
          "ones</b>, with weights on each term — which is simple, "
          "effective, and interpretable.",
          "<b>Implicit feedback</b> — clicks, dwell time, query "
          "reformulations, and abandonment. <b>Abundant, biased, and the "
          "only kind you will actually get</b> at scale "
          "(Module 05 &sect;4's position bias).",
          "<b>And session context is the strongest implicit "
          "signal:</b> <b>the previous query in a session usually "
          "disambiguates the current one</b> — 'jaguar' after 'car "
          "reviews' is unambiguous — which is cheap to use and "
          "frequently neglected.",
          "<b>Which makes reformulation detection particularly "
          "valuable</b> — <b>a reformulated query is a reported "
          "failure of the previous one</b>, delivered voluntarily. <b>A "
          "reformulation is a user telling you the last result was "
          "wrong</b>, which is <b>a free, strong, and very widely ignored "
          "quality signal</b> — and aggregating reformulations is "
          "one of the best available sources of failing queries for "
          "Module 05 &sect;4's error analysis."]),

  ("break",),
  ("h1", "4 &nbsp; Structure and intent"),
  ("ul", ["<b>Segmentation</b> — working out which adjacent words "
          "form a single unit. <b>'New York hotel' is two units and not "
          "three words</b>, and <b>treating it as three retrieves "
          "badly</b> because it will match documents about York and about "
          "newness.",
          "<b>Entity recognition and linking</b> — identifying "
          "that a span of the query names a specific known entity, <b>which "
          "enables structured retrieval against a knowledge base</b> "
          "alongside the text search and is how most commercial engines "
          "handle entity queries.",
          "<b>Intent classification</b> (Module 01 &sect;3) — "
          "<b>which determines the result presentation at least as much "
          "as the ranking</b>: a navigational query wants one result, and "
          "a transactional one wants a filterable list.",
          "<b>Attribute extraction</b> — 'red shoes under "
          "&pound;50' contains a colour, a category, and a price "
          "constraint, <b>which should become structured filters rather "
          "than being matched as text</b> (and matching '50' as text is a "
          "characteristic failure).",
          "<b>And none of it is free:</b> <b>each component adds "
          "latency and its own failure mode</b>, so <b>measure the "
          "end-to-end effect rather than the component's accuracy</b>. "
          "<b>A 95%-accurate intent classifier may hurt overall quality "
          "if the 5% are confidently misrouted</b> to the wrong "
          "presentation, which is Module 05's measurement discipline "
          "applied to a pipeline stage."]),
  ("callout", "And a language model changes what is available here",
   ["<b>Query rewriting, expansion, decomposition, and reformulation "
    "are all things a language model does well</b> — and <b>it can "
    "resolve a pronoun against the session history, decompose a compound "
    "question into retrievable parts, or generate a hypothetical answer "
    "document to retrieve against</b>, none of which the classical "
    "methods do.",
    "<b>Which is a real improvement over the classical methods</b> for "
    "conversational and genuinely complex queries, and is the "
    "query-understanding half of Module 11's architecture.",
    "<b>At a cost that is easy to understate:</b> <b>a model call "
    "before retrieval adds latency to every single query and introduces "
    "a failure mode that is hard to bound</b> — a rewrite that "
    "changes the meaning is worse than no rewrite (Module 04 "
    "&sect;4's budget, and &sect;2's drift in a new form).",
    "<b>So the honest position: use it where the query is genuinely "
    "hard, and not on the head of the distribution</b> — <b>where a "
    "cached classical pipeline is both faster and considerably more "
    "predictable</b> (Module 04 &sect;4's caching). <b>Routing by "
    "query difficulty is the design that gets both</b>, and it requires "
    "a difficulty estimate, which is itself a query understanding "
    "problem."]),
 ],
 "resources": [
   ("Manning, Raghavan & Sch&uuml;tze, chapters 3 and 9 (free)",
    "https://nlp.stanford.edu/IR-book/",
    "<b>&sect;1's correction and &sect;2 and &sect;3's expansion and "
    "feedback</b>, with Rocchio derived."),
   ("Croft, Metzler & Strohman, chapter 6 (free PDF)",
    "https://ciir.cs.umass.edu/irbook/",
    "<b>&sect;4's query understanding</b> — segmentation, intent, and "
    "the production pipeline shape."),
   ("Cucerzan & Brill &mdash; Spelling correction as an iterative "
    "process (free)",
    "https://aclanthology.org/W04-3221/",
    "<b>&sect;1's log-based approach</b> — why the query log beats a "
    "dictionary, with the method."),
   ("Gao et al. &mdash; Precise Zero-Shot Dense Retrieval without "
    "Relevance Labels (free)",
    "https://arxiv.org/abs/2212.10496",
    "<b>&sect;4's callout</b> — generating a hypothetical document to "
    "retrieve against, which is the clearest instance of the shift."),
 ],
 "exercises": [
   "<b>Measure the misspelling rate</b> in any query log you can "
   "obtain.",
   "<b>Show that a misspelled rare term returns nothing</b> on your "
   "collection.",
   "<b>Build a noisy channel corrector</b> with a log-derived prior.",
   "<b>Find a case where a dictionary corrector is wrong</b> and a "
   "log-based one is right.",
   "<b>Implement pseudo-relevance feedback</b> and measure the mean "
   "improvement.",
   "<b>Plot the per-query change</b> and count the queries made "
   "worse.",
   "<b>Find a drifted query</b> and trace which expansion term caused "
   "it.",
   "<b>Implement Rocchio</b> and test it with judgements as explicit "
   "feedback.",
   "<b>Detect reformulations</b> in a session log and inspect the "
   "queries that preceded them.",
   "<b>Add an intent classifier</b> and measure the end-to-end effect "
   "rather than its accuracy.",
 ],
 "selfcheck": [
   "Why is a misspelled query a total rather than partial failure?",
   "Why must correction use the log rather than a dictionary?",
   "Give the noisy channel formulation and the interface rules.",
   "Name three expansion methods and the danger they share.",
   "Why does expansion require per-query reporting?",
   "Contrast explicit and implicit feedback, and say why one is rare.",
   "Describe Rocchio's method.",
   "Why is a reformulation a valuable signal?",
   "Name four things query understanding extracts.",
   "What should you measure about a query understanding component?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Web-Scale Retrieval",
 "subtitle": "What changes when the collection is adversarial.",
 "question": "What does the web add that a document collection does not?",
 "outcomes": [
     "Explain crawling and its politeness constraints.",
     "Explain duplicate detection at web scale.",
     "Explain link analysis and what it measures.",
     "Explain adversarial retrieval and spam.",
     "Explain the architecture of a web search system.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Crawling",
   "blurb": "An engineering problem with an etiquette constraint."},

  {"t": "code", "kicker": "Crawling", "title": "The requirements, and the ones people forget",
   "lang": "text", "code": """
  THE MECHANICS
      a frontier of URLs to fetch, prioritised
      politeness: a delay per host, robots.txt
          respected, and a contactable user agent
      duplicate URL detection before fetching
      and a recrawl policy by observed change rate

  THE PRIORITISATION PROBLEM
      you cannot fetch everything, so which pages
      first? Discovery order, link-based importance,
      and observed update frequency all contribute.

  THE TRAPS
      infinite URL spaces -- calendars, session ids,
          faceted navigation. A crawler without a
          depth and pattern limit will not escape.
      and soft 404s, which return 200 with an error
          page, so the crawler keeps the garbage

  AND POLITENESS IS NOT OPTIONAL. A crawler without a
  per-host rate limit is a denial of service, whatever
  was intended -- which is a professional constraint
  as much as a technical one.
""",
   "caption": "<b>A crawler without a per-host rate limit is a denial "
              "of service whatever was intended</b> — which is "
              "CSCE 701 Module 01 §4's constraint in this "
              "context.",
   "note": "The politeness-as-obligation framing belongs here."},

  {"t": "section", "label": "Part 2", "title": "Duplicates",
   "blurb": "Where CSCE 676's machinery earns its place."},

  {"t": "callout", "title": "A large fraction of the web is duplicate or near-duplicate, and indexing it wastes everything",
   "kind": "The scale of the problem",
   "body": ["<b>Mirrors, syndicated content, printer-friendly "
            "variants, session-id URLs, and templated pages</b> "
            "— <b>a very large share of fetched pages are "
            "substantially duplicates of others.</b>",
            "<b>Which costs on every axis:</b> <b>crawl bandwidth, "
            "index space, and result quality</b>, since a result page of "
            "ten near-identical documents is worth one.",
            "<b>So shingling, minhashing, and LSH</b> "
            "(CSCE 676 §02) <b>are deployed exactly "
            "here</b> — and <b>this is their original application</b>, "
            "which is why that module's examples are "
            "documents.",
            "<b>And canonicalisation is the other half:</b> <b>URL "
            "normalisation, and choosing one canonical version of a "
            "duplicate set</b> — which is a policy decision with "
            "consequences for whoever is not chosen "
            "(Module 12)."]},

  {"t": "section", "label": "Part 3", "title": "Links",
   "blurb": "Evidence from outside the document."},

  {"t": "callout", "title": "A link is an endorsement, which makes the link graph evidence the text does not contain",
   "kind": "Why link analysis mattered",
   "body": ["<b>A page's text is written by its author and its "
            "inbound links are written by others</b> — <b>which "
            "makes links the first large-scale source of evidence not "
            "under the document's own control.</b>",
            "<b>PageRank</b> (CSCE 676 §07 §2) "
            "<b>formalises this recursively</b>: an endorsement from a "
            "well-endorsed page counts for more.",
            "<b>And anchor text is at least as valuable:</b> <b>how "
            "others describe a page, which addresses "
            "Module 01 §2's vocabulary mismatch "
            "directly</b> — the describers use the searcher's words "
            "rather than the author's.",
            "<b>But the link graph became adversarial</b>, which is "
            "Part 4 — <b>and once a signal is known to "
            "matter, it is manufactured</b>, which is the general "
            "result."]},

  {"t": "bullets", "kicker": "Links", "title": "And what link analysis is worth now",
   "items": [
     "<b>As one feature among hundreds</b> in a learned ranker "
     "(Module 06 §3) — rather than as the ranking "
     "function, which it never quite was.",
     "",
     "<b>Anchor text remains valuable</b> and is harder to "
     "manufacture convincingly at scale than a link is.",
     "",
     "<b>And link-based spam detection</b> uses the graph's "
     "structure rather than its scores — unnatural link patterns "
     "are detectable as patterns.",
     "",
     "<b>While the raw score's value fell</b> as manipulation "
     "improved — which is a general lesson about any "
     "published ranking signal.",
     "",
     "<b>So: use it, weight it with everything else, and expect it "
     "to be attacked.</b>",
   ],
   "footnote": "<b>Once a signal is known to matter, it is "
               "manufactured</b> — which means a ranking signal's "
               "value decays after it becomes public, and is an argument "
               "for many weak signals over one strong one."},

  {"t": "section", "label": "Part 4", "title": "Adversarial retrieval",
   "blurb": "The property that distinguishes web search."},

  {"t": "callout", "title": "On the web, the documents are written by people who want to rank, which changes everything",
   "kind": "The structural difference from a document collection",
   "body": ["<b>In an ordinary collection the documents are "
            "indifferent to your ranking.</b> <b>On the web they are "
            "written specifically to influence it</b> — which makes "
            "retrieval an adversarial problem rather than a statistical "
            "one.",
            "<b>So every signal you use will be attacked:</b> "
            "<b>keyword stuffing, cloaking, link farms, generated "
            "content, and now generated content at "
            "scale.</b>",
            "<b>And the defences are the ones from "
            "CSCE 701:</b> <b>many weak signals rather than one "
            "strong one, detection rather than prevention, and "
            "signals that are expensive to fake</b> — behaviour, "
            "reputation over time, and editorial judgement.",
            "<b>Which makes web search a security problem with a "
            "ranking component</b> — and <b>it is why the signals "
            "are not published</b>, which is a defensive decision rather "
            "than a commercial one."]},

  {"t": "bullets", "kicker": "Architecture", "title": "And what a web search system contains",
   "items": [
     "<b>A crawler and a frontier</b> (Part 1), with "
     "duplicate detection (Part 2).",
     "",
     "<b>A document-partitioned index across many "
     "machines</b> (Module 04 §4), usually tiered by "
     "quality (Module 04 §3).",
     "",
     "<b>A cheap first-stage retrieval, then a learned "
     "ranker</b> (Module 06 §4), then presentation "
     "logic.",
     "",
     "<b>Query understanding in front</b> (Module 09), and "
     "caching at every layer.",
     "",
     "<b>And a spam and quality pipeline</b> running "
     "continuously beside all of it — which is as large as the "
     "retrieval system.",
   ],
   "footnote": "<b>The quality and anti-abuse pipeline is comparable "
               "in size to the retrieval system</b>, which is the fact "
               "most surprising to people who have only built "
               "retrieval."},
 ],
 "takeaways": [
   "A crawler without a per-host rate limit is a denial of service "
   "whatever was intended, which is a professional constraint.",
   "Infinite URL spaces from calendars and faceted navigation will trap a "
   "crawler without pattern and depth limits.",
   "A large share of the web is near-duplicate, which is the original "
   "application of shingling and LSH.",
   "Links and anchor text were the first large-scale evidence not under "
   "the document author's control.",
   "Once a signal is known to matter it is manufactured, which argues for "
   "many weak signals over one strong one.",
   "The quality and anti-abuse pipeline is comparable in size to the "
   "retrieval system itself.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Crawling"),
  ("code", """THE MECHANICS
    a frontier of URLs to fetch, prioritised
    politeness: a delay per host, robots.txt
        respected, and a contactable user agent
        string
    duplicate URL detection before fetching
    and a recrawl policy driven by observed change
        rate

THE PRIORITISATION PROBLEM
    you cannot fetch everything, so which pages
    first? Discovery order, link-based importance,
    and observed update frequency all contribute, and
    the policy determines what your index contains.

THE TRAPS
    infinite URL spaces -- calendars, session ids,
        faceted navigation with combinatorial
        filters. A crawler without a depth and
        pattern limit will not escape them.
    and soft 404s, which return status 200 with an
        error page, so the crawler happily keeps the
        garbage and indexes it

AND POLITENESS IS NOT OPTIONAL."""),
  ("p", "<b>A crawler without a per-host rate limit is a denial of "
        "service, whatever was intended</b> — which is <b>CSCE 701 "
        "Module 01 &sect;4's authorisation constraint arriving in this "
        "context</b>, and it is a professional and in some jurisdictions "
        "legal matter rather than a courtesy. <b>The politeness-as-"
        "obligation framing belongs here</b> rather than in a footnote: a "
        "student crawler that takes down a small site has caused real "
        "harm, and the mechanism is a missing three-line delay."),

  ("h1", "2 &nbsp; Duplicates"),
  ("callout", "A large fraction of the web is duplicate or near-duplicate, "
              "and indexing it wastes everything",
   ["<b>Mirrors, syndicated news content, printer-friendly variants, "
    "session-id URLs pointing at identical pages, and templated pages "
    "differing in one field</b> — <b>a very large share of fetched "
    "pages are substantially duplicates of others</b>, by every published "
    "measurement.",
    "<b>Which costs on every axis at once:</b> <b>crawl bandwidth "
    "spent fetching them, index space storing them, and result quality "
    "when they are returned</b> — since <b>a result page containing "
    "ten near-identical documents is worth approximately one</b> "
    "(Module 05 &sect;3's redundancy problem).",
    "<b>So shingling, minhashing, and locality-sensitive hashing</b> "
    "(CSCE 676 Module 02) <b>are deployed exactly here</b> — "
    "and <b>this is their original application</b>, which is why that "
    "module's worked examples are documents rather than something more "
    "abstract.",
    "<b>And canonicalisation is the other half of the problem:</b> "
    "<b>URL normalisation, and then choosing one canonical version from "
    "each duplicate set</b> — which is <b>a policy decision with "
    "real consequences for whoever is not chosen</b> (Module 12's "
    "exposure argument), and which site owners care about a great "
    "deal."]),

  ("h1", "3 &nbsp; Links"),
  ("callout", "A link is an endorsement, which makes the link graph evidence "
              "the text does not contain",
   ["<b>A page's own text is written by its author, and its inbound "
    "links are written by other people</b> — <b>which makes links "
    "the first large-scale source of retrieval evidence not under the "
    "document's own control</b>, and that independence was the whole "
    "insight.",
    "<b>PageRank</b> (CSCE 676 Module 07 &sect;2) <b>formalises "
    "this recursively:</b> an endorsement from a well-endorsed page "
    "counts for more than one from an obscure page, which is computed as "
    "a stationary distribution.",
    "<b>And anchor text is at least as valuable as the link "
    "itself:</b> <b>it is how other people describe a page</b>, which "
    "<b>addresses Module 01 &sect;2's vocabulary mismatch "
    "directly</b> — because <b>the describers use the searcher's "
    "words rather than the author's</b>, which is exactly the asymmetry "
    "that module identified.",
    "<b>But the link graph became adversarial</b>, which is "
    "&sect;4 — and the general result is worth stating: <b>once a "
    "signal is known to matter, it is manufactured.</b>"]),
  ("ul", ["<b>As one feature among hundreds</b> in a learned ranker "
          "(Module 06 &sect;3) — <b>rather than as the ranking "
          "function</b>, which it never quite was even in the systems "
          "most associated with it.",
          "<b>Anchor text remains valuable</b>, and <b>is harder to "
          "manufacture convincingly at scale than a link is</b>, because "
          "it requires producing plausible varied text on pages that look "
          "legitimate.",
          "<b>And link-based spam detection</b> uses the graph's "
          "<i>structure</i> rather than its scores — <b>unnatural "
          "link patterns are detectable as patterns</b> even when the "
          "individual links look fine, which is "
          "CSCE 676 Module 07's community detection put to a "
          "defensive use.",
          "<b>While the raw score's value fell</b> substantially as "
          "manipulation techniques improved — <b>which is a general "
          "lesson about any published ranking signal</b> rather than a "
          "fact about links.",
          "<b>So: use it, weight it alongside everything else, and "
          "expect it to be attacked.</b> <b>Once a signal is known to "
          "matter, it is manufactured</b> — which means <b>a ranking "
          "signal's value decays after it becomes public</b>, and <b>is "
          "an argument for many weak signals over one strong one</b> "
          "(&sect;4, and CSCE 701 Module 01's defence in depth)."]),

  ("break",),
  ("h1", "4 &nbsp; Adversarial retrieval"),
  ("callout", "On the web, the documents are written by people who want to "
              "rank, which changes everything",
   ["<b>In an ordinary document collection the documents are entirely "
    "indifferent to your ranking function.</b> <b>On the web they are "
    "written specifically to influence it</b> — <b>which makes "
    "retrieval an adversarial problem rather than a statistical one</b>, "
    "and that is the single structural difference from everything else in "
    "this course.",
    "<b>So every signal you use will be attacked:</b> <b>keyword "
    "stuffing, hidden text, cloaking (serving different content to the "
    "crawler), link farms, purchased links, and now generated content at "
    "scale</b> — each of which appeared within a short time of the "
    "corresponding signal becoming important.",
    "<b>And the defences are the ones from CSCE 701:</b> <b>many "
    "weak signals rather than one strong one, detection rather than "
    "prevention (Module 09 of that course), and a preference for "
    "signals that are expensive to fake</b> — user behaviour over "
    "time, reputation, and editorial judgement.",
    "<b>Which makes web search a security problem with a ranking "
    "component</b> rather than the reverse — and <b>it is why the "
    "ranking signals are not published</b>, <b>which is a defensive "
    "decision rather than a purely commercial one</b>, and is one of the "
    "few legitimate uses of obscurity (CSCE 701 Module 01 "
    "&sect;1)."]),
  ("ul", ["<b>A crawler and a frontier</b> (&sect;1), with "
          "duplicate detection and canonicalisation (&sect;2) in "
          "front of the index.",
          "<b>A document-partitioned index across many machines</b> "
          "(Module 04 &sect;4), usually <b>tiered by document "
          "quality</b> so that most queries are answered from a small "
          "high-quality tier (Module 04 &sect;3).",
          "<b>A cheap first-stage retrieval, then a learned ranker</b> "
          "(Module 06 &sect;4), <b>then presentation logic</b> that "
          "decides what kind of result page to build "
          "(Module 09 &sect;4's intent).",
          "<b>Query understanding in front of all of it</b> "
          "(Module 09), <b>and caching at every layer</b> "
          "(Module 04 &sect;4).",
          "<b>And a spam and quality pipeline running continuously "
          "beside the whole thing</b> — <b>which is as large as the "
          "retrieval system</b>. <b>The quality and anti-abuse pipeline "
          "being comparable in size to the retrieval system is the fact "
          "most surprising to people who have only built retrieval</b>, "
          "and it follows directly from &sect;4's callout."]),
 ],
 "resources": [
   ("Manning, Raghavan & Sch&uuml;tze, chapters 19 through 21 (free)",
    "https://nlp.stanford.edu/IR-book/",
    "<b>&sect;1 through &sect;3</b> — crawling, duplicate detection, "
    "and link analysis, with the algorithms."),
   ("Croft, Metzler & Strohman, chapters 3 and 9 (free PDF)",
    "https://ciir.cs.umass.edu/irbook/",
    "<b>&sect;1's mechanics and &sect;4's spam material</b>, in more "
    "practical detail."),
   ("Brin & Page &mdash; The Anatomy of a Large-Scale Hypertextual Web "
    "Search Engine (free)",
    "http://infolab.stanford.edu/~backrub/google.html",
    "<b>&sect;3 and &sect;4 in the original</b> — and worth reading "
    "for how much of the architecture survived."),
   ("Gy&ouml;ngyi & Garcia-Molina &mdash; Web Spam Taxonomy (free)",
    "http://ilpubs.stanford.edu:8090/771/",
    "<b>&sect;4's techniques, catalogued</b> — the defensive "
    "equivalent of CSCE 701's threat modelling."),
 ],
 "exercises": [
   "<b>Write a politely rate-limited crawler</b> for a site you own, "
   "and verify the delay.",
   "<b>Read a real robots.txt</b> and implement its rules.",
   "<b>Find an infinite URL space</b> on a site you own and construct "
   "the pattern limit that escapes it.",
   "<b>Detect soft 404s</b> by content rather than status code.",
   "<b>Run minhash near-duplicate detection</b> over your crawl and "
   "report the duplicate rate.",
   "<b>Choose canonical versions</b> and say what rule you used.",
   "<b>Compute PageRank</b> on a crawled subgraph.",
   "<b>Extract anchor text</b> and compare it against the target pages' "
   "own titles.",
   "<b>Find an unnatural link pattern</b> in a graph you have.",
   "<b>List the signals in your own system</b> and say how each could "
   "be manufactured.",
 ],
 "selfcheck": [
   "Give the crawling mechanics and the two traps.",
   "Why is politeness an obligation rather than a courtesy?",
   "Why does web duplication cost on every axis?",
   "Which CSCE 676 machinery applies, and why is this its original "
   "application?",
   "Why is a link evidence the text does not contain?",
   "Why is anchor text particularly valuable?",
   "State the general result about published signals.",
   "What is link analysis worth now, and in what role?",
   "What makes web retrieval adversarial, and what are the defences?",
   "Name six components of a web search system.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Generative Retrieval",
 "subtitle": "When the answer is written rather than found.",
 "question": "What changes when the system answers instead of listing?",
 "outcomes": [
     "Explain the architecture from the retrieval side.",
     "Explain what attribution requires.",
     "Explain how evaluation changes.",
     "Explain the effects on the documents and their "
     "authors.",
     "Build and evaluate an answering system.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The shift",
   "blurb": "From a list of documents to a written answer."},

  {"t": "callout", "title": "Returning an answer instead of a list moves the judgement from the user to the system",
   "kind": "What actually changes",
   "body": ["<b>A result list lets the user judge relevance "
            "themselves</b> — they see the titles, the sources, and "
            "the snippets, and choose. <b>An answer has already "
            "chosen.</b>",
            "<b>Which is better when the system is right and worse "
            "when it is wrong</b> — because the user has lost both "
            "the alternatives and the cues they used to "
            "judge.",
            "<b>And it changes the failure mode:</b> <b>a bad result "
            "list is visibly bad, and a fluent wrong answer is "
            "not</b> (CSCE 638 §12 §3).",
            "<b>So attribution is not a feature but the mechanism "
            "that restores the user's ability to judge</b> — which "
            "is why Part 2 treats it as a requirement rather "
            "than a nicety."]},

  {"t": "code", "kicker": "Architecture", "title": "The pipeline, from the retrieval side",
   "lang": "text", "code": """
  QUERY UNDERSTANDING (Module 09)
      rewrite, decompose, resolve against the session

  RETRIEVAL (Modules 03, 07, 08)
      hybrid, then rerank. THIS IS STILL THE
      BOTTLENECK -- a generator cannot answer from
      passages it was not given.

  SELECTION
      how many passages, which ones, in what order.
      Position effects are real, so put the best
      first (CSCE 638 Module 11 section 4).

  GENERATION
      answer FROM the passages, with citations, and
      abstain when they do not suffice

  AND THE RETRIEVAL HALF IS WHERE THE QUALITY IS.
  The generation step is largely solved and the
  retrieval step is not, which is the opposite of
  where the attention goes.
""",
   "caption": "<b>The retrieval half is where the quality is</b> "
              "— and it is the half that gets the least attention in "
              "practice.",
   "note": "Framing this as a retrieval problem is this course's "
           "contribution."},

  {"t": "section", "label": "Part 2", "title": "Attribution",
   "blurb": "What a citation has to mean."},

  {"t": "callout", "title": "A citation must support the specific claim it is attached to, which is a stronger requirement than it looks",
   "kind": "The requirement, and why it fails",
   "body": ["<b>The weak version is that the cited document is "
            "topically related</b> — which is what a system produces "
            "if it retrieves passages and then generates freely, and it "
            "is nearly worthless.",
            "<b>The requirement is that the passage actually "
            "entails the sentence it is cited for</b> — <b>which "
            "has to be checked by reading, and frequently "
            "fails.</b>",
            "<b>And the characteristic failure is a plausible claim "
            "with a citation to a document that does not say "
            "it</b> — <b>which is worse than no citation, because "
            "the citation confers credibility.</b>",
            "<b>So measure attribution directly:</b> <b>sample "
            "sentences, read the cited passage, and record whether it "
            "supports the claim</b> — which is slow, unavoidable, and "
            "the only honest measurement."]},

  {"t": "bullets", "kicker": "Attribution", "title": "And what improves it",
   "items": [
     "<b>Generate per-sentence rather than per-answer "
     "citations</b>, so that each claim is individually "
     "traceable.",
     "",
     "<b>Instruct the model to quote before it paraphrases</b>, "
     "which makes the support checkable mechanically.",
     "",
     "<b>Verify with an entailment model</b> and drop or flag "
     "unsupported sentences — which is a second model and is "
     "worth it where the stakes are real.",
     "",
     "<b>And present the passage, not only the link</b>, so the "
     "user can check without leaving — which is the cheapest "
     "improvement available.",
     "",
     "<b>While accepting that none of these eliminate the "
     "problem</b> (CSCE 638 §12 §3) — it is "
     "structural.",
   ],
   "footnote": "<b>Presenting the supporting passage inline is the "
               "cheapest and most effective of these</b> — it "
               "restores the user's judgement, which is "
               "Part 1's argument."},

  {"t": "section", "label": "Part 3", "title": "Evaluation",
   "blurb": "Which has to change shape."},

  {"t": "bullets", "kicker": "Evaluation", "title": "What to measure, and it is not NDCG",
   "items": [
     "<b>Retrieval recall at the passage level</b>, separately "
     "— <b>because it bounds everything</b> and is the thing "
     "classical IR evaluation already measures "
     "well.",
     "",
     "<b>Answer correctness, by reading</b> — against a "
     "reference where one exists, and by judgement where one does "
     "not.",
     "",
     "<b>Attribution rate</b> (Part 2) — the "
     "fraction of claims genuinely supported by their "
     "citations.",
     "",
     "<b>Abstention rate on unanswerable questions</b>, measured "
     "by deliberately asking some (CSCE 638 §11 "
     "§4).",
     "",
     "<b>And the user-side measures:</b> <b>did they have to "
     "check? did they find the answer sufficient? did they "
     "reformulate?</b>",
   ],
   "footnote": "<b>Reformulation and checking behaviour are the "
               "strongest available signals</b> that an answer did not "
               "satisfy — and they are free "
               "(Module 09 §3)."},

  {"t": "section", "label": "Part 4", "title": "Consequences",
   "blurb": "For the documents, and the people who wrote them."},

  {"t": "callout", "title": "An answer that satisfies the user removes the visit the document's author depended on",
   "kind": "The consequence worth stating plainly",
   "body": ["<b>The web's documents were written under an implicit "
            "arrangement:</b> <b>search engines send visitors, and the "
            "visit is what the author receives in exchange for the "
            "content.</b>",
            "<b>An answered query breaks that</b> — the user is "
            "satisfied without visiting, so <b>the incentive to produce "
            "the content weakens</b>, and the system depends on that "
            "content existing.",
            "<b>Which is a genuine collective-action problem rather "
            "than a complaint</b>: <b>the answering system is more "
            "useful per query and degrades the corpus it needs</b>, and "
            "no individual system can resolve that.",
            "<b>So the honest position is to state it</b> — "
            "<b>along with what you do about it: prominent attribution, "
            "links that are actually followed, and licensing where it "
            "applies</b> (Module 12)."]},

  {"t": "bullets", "kicker": "Practice", "title": "And what to do when building one",
   "items": [
     "<b>Invest in retrieval first</b>, because that is where the "
     "quality is (Part 1) and where the attention is "
     "not.",
     "",
     "<b>Require and verify citations</b>, and present the "
     "supporting passage (Part 2).",
     "",
     "<b>Measure abstention deliberately</b>, by asking questions "
     "your corpus cannot answer.",
     "",
     "<b>Route by difficulty:</b> <b>answer directly where you are "
     "confident, and return a list where you are not</b> — which "
     "is the design that uses both modes well.",
     "",
     "<b>And state what you are not providing</b>, which is "
     "Module 13.",
   ],
   "footnote": "<b>Routing between answering and listing is the "
               "design most systems skip</b> — and it gets the "
               "benefit of both modes rather than committing to "
               "one."},
 ],
 "takeaways": [
   "Returning an answer moves the relevance judgement from the user to the "
   "system, which is better when right and worse when wrong.",
   "A bad result list is visibly bad and a fluent wrong answer is not, "
   "which is the changed failure mode.",
   "The retrieval half is where the quality is, and it is the half that "
   "gets the least attention.",
   "A citation must support the specific claim it is attached to, and the "
   "characteristic failure is a plausible claim cited to a document that "
   "does not say it.",
   "Presenting the supporting passage inline is the cheapest improvement, "
   "because it restores the user's ability to judge.",
   "An answered query removes the visit the document's author depended on, "
   "which is a collective-action problem rather than a complaint.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The shift"),
  ("callout", "Returning an answer instead of a list moves the judgement "
              "from the user to the system",
   ["<b>A result list lets the user judge relevance for "
    "themselves</b> — they see the titles, the source domains, and "
    "the snippets, and they choose which to trust. <b>An answer has "
    "already chosen on their behalf.</b>",
    "<b>Which is better when the system is right and considerably "
    "worse when it is wrong</b> — because <b>the user has lost both "
    "the alternatives and the cues they were using to judge</b> "
    "(Module 01 &sect;3's relevance-as-relation point: the user was "
    "doing work the system cannot do).",
    "<b>And it changes the failure mode entirely:</b> <b>a bad result "
    "list is visibly bad and a fluent wrong answer is not</b> "
    "(CSCE 638 Module 12 &sect;3's mechanism), which means the "
    "user cannot apply the scepticism that a poor list would have "
    "triggered.",
    "<b>So attribution is not a feature but the mechanism that "
    "restores the user's ability to judge</b> — <b>which is why "
    "&sect;2 treats it as a requirement rather than a nicety</b>, and why "
    "an answering system without working citations is a worse product "
    "than a list."]),
  ("code", """QUERY UNDERSTANDING (Module 09)
    rewrite, decompose, resolve against the session

RETRIEVAL (Modules 03, 07, 08)
    hybrid, then rerank. THIS IS STILL THE
    BOTTLENECK -- a generator cannot answer from
    passages it was not given.

SELECTION
    how many passages, which ones, and in what order.
    Position effects within the context are real, so
    put the best first (CSCE 638 Module 11
    section 4's lost-in-the-middle row).

GENERATION
    answer FROM the passages, with citations, and
    abstain when they do not suffice

AND THE RETRIEVAL HALF IS WHERE THE QUALITY IS. The
generation step is largely solved and the retrieval
step is not, which is the opposite of where the
attention usually goes."""),
  ("p", "<b>The retrieval half is where the quality is</b> — and "
        "<b>it is the half that gets the least attention in practice</b>, "
        "because the prompt is the most visible and most easily modified "
        "component (CSCE 638 Module 11 &sect;2's same observation). "
        "<b>Framing this as a retrieval problem rather than a generation "
        "problem is this course's contribution to the topic</b>, and it is "
        "the right framing: everything in Modules 02 through 09 applies "
        "unchanged, and the generation step is a presentation layer over "
        "it."),

  ("h1", "2 &nbsp; Attribution"),
  ("callout", "A citation must support the specific claim it is attached to, "
              "which is a stronger requirement than it looks",
   ["<b>The weak version of attribution is that the cited document is "
    "topically related to the answer</b> — which is what a system "
    "produces by default if it retrieves passages and then generates "
    "freely while listing its sources, <b>and it is nearly "
    "worthless</b> as a verification aid.",
    "<b>The actual requirement is that the cited passage entails the "
    "specific sentence it is attached to</b> — <b>which has to be "
    "checked by reading, and frequently fails</b> even when the retrieval "
    "was good and the answer is broadly correct.",
    "<b>And the characteristic failure is a plausible claim with a "
    "citation to a document that does not actually say it</b> — "
    "<b>which is worse than no citation at all, because the citation "
    "confers credibility the claim has not earned</b> and discourages "
    "the checking it appears to invite.",
    "<b>So measure attribution directly:</b> <b>sample sentences from "
    "generated answers, read the cited passage, and record whether it "
    "supports the claim</b> — which is slow, unavoidable, and <b>the "
    "only honest measurement</b> available (CSCE 638 Module 11 "
    "&sect;4's fourth evaluation)."]),
  ("ul", ["<b>Generate per-sentence rather than per-answer "
          "citations</b>, so that <b>each individual claim is "
          "traceable</b> rather than the answer as a whole being "
          "attributed to a set of sources.",
          "<b>Instruct the model to quote before it paraphrases</b>, "
          "<b>which makes the support checkable mechanically</b> — a "
          "quoted span either appears in the cited passage or it does "
          "not, and that check is a string search.",
          "<b>Verify with an entailment model</b> and drop or flag the "
          "unsupported sentences — <b>which is a second model and is "
          "worth it where the stakes are real</b>, and which is how the "
          "better production systems handle this.",
          "<b>And present the passage itself, not only a link to "
          "it</b>, so that the user can check without navigating "
          "away — <b>which is the cheapest improvement "
          "available</b> and the most effective.",
          "<b>While accepting that none of these eliminate the "
          "problem</b> (CSCE 638 Module 12 &sect;3) — <b>it is "
          "structural</b>, and a system that claims to have solved it "
          "has not measured it. <b>Presenting the supporting passage "
          "inline is the cheapest and most effective of these</b>, "
          "<b>because it restores the user's judgement</b>, which is "
          "&sect;1's argument."]),

  ("break",),
  ("h1", "3 &nbsp; Evaluation"),
  ("ul", ["<b>Retrieval recall at the passage level</b>, measured "
          "separately — <b>because it bounds everything "
          "downstream</b> and <b>is the thing classical IR evaluation "
          "already measures well</b> (Module 05), so there is no "
          "excuse for omitting it.",
          "<b>Answer correctness, established by reading</b> — "
          "against a reference answer where one exists, and by judgement "
          "where one does not (which is most interesting cases, and is "
          "CSCE 638 Module 10 &sect;3's unsolved problem).",
          "<b>The attribution rate</b> (&sect;2) — <b>the "
          "fraction of claims genuinely supported by the citations "
          "attached to them</b>, sampled and read.",
          "<b>The abstention rate on unanswerable questions</b>, "
          "measured by <b>deliberately asking some that your corpus "
          "cannot answer</b> (CSCE 638 Module 11 &sect;4) — "
          "which takes an hour to set up and is almost never done.",
          "<b>And the user-side measures:</b> <b>did they have to "
          "check the sources? did they find the answer sufficient? did "
          "they reformulate?</b> <b>Reformulation and checking behaviour "
          "are the strongest available signals that an answer did not "
          "satisfy</b> — <b>and they are free</b>, arriving in the "
          "logs (Module 09 &sect;3's reformulation signal)."]),

  ("h1", "4 &nbsp; Consequences"),
  ("callout", "An answer that satisfies the user removes the visit the "
              "document's author depended on",
   ["<b>The web's documents were written under an implicit "
    "arrangement:</b> <b>search engines send visitors, and the visit is "
    "what the author receives in exchange for having produced the "
    "content</b> — through advertising, subscriptions, reputation, or "
    "sales.",
    "<b>An answered query breaks that arrangement</b> — the user "
    "is satisfied without visiting, so <b>the incentive to produce the "
    "content weakens</b>, and <b>the answering system depends entirely on "
    "that content continuing to exist.</b>",
    "<b>Which is a genuine collective-action problem rather than a "
    "complaint about business models:</b> <b>the answering system is "
    "more useful per query and simultaneously degrades the corpus it "
    "requires</b>, and <b>no individual system can resolve that</b> by "
    "behaving better, because the benefit of defecting accrues to "
    "whoever defects.",
    "<b>So the honest position is to state it</b> — <b>along with "
    "what you actually do about it: prominent attribution, links that "
    "are genuinely followed rather than decorative, and licensing "
    "arrangements where they apply</b> (Module 12). <b>Stating the "
    "problem and your response is the available honesty</b>, and it is "
    "more than most systems offer."]),
  ("ul", ["<b>Invest in retrieval first</b>, because <b>that is where "
          "the quality is</b> (&sect;1) <b>and where the attention is "
          "not</b> — which makes it the highest-return work "
          "available.",
          "<b>Require and verify citations, and present the supporting "
          "passage</b> (&sect;2) — the verification being the part "
          "that distinguishes a system with citations from a system with "
          "attribution.",
          "<b>Measure abstention deliberately</b>, by constructing "
          "questions your corpus cannot answer and recording what happens "
          "(&sect;3).",
          "<b>Route by difficulty:</b> <b>answer directly where you "
          "are confident, and return a result list where you are "
          "not</b> — <b>which is the design that uses both modes "
          "well</b> rather than committing to one, and which requires a "
          "confidence estimate.",
          "<b>And state what you are not providing</b>, which is "
          "Module 13's subject. <b>Routing between answering and "
          "listing is the design most systems skip</b>, and <b>it gets "
          "the benefit of both modes</b> — the convenience of an "
          "answer where it is warranted, and the user's own judgement "
          "where it is not."]),
 ],
 "resources": [
   ("Lewis et al. &mdash; Retrieval-Augmented Generation (free)",
    "https://arxiv.org/abs/2005.11401",
    "<b>&sect;1's architecture in the original</b> — read it against "
    "CSCE 638 Module 11, which covers the generation side."),
   ("Rashkin et al. &mdash; Measuring Attribution in NLG (free)",
    "https://aclanthology.org/2023.tacl-1.10/",
    "<b>&sect;2's requirement, formalised</b> — what it means for a "
    "citation to support a claim, and how to judge it."),
   ("Liu, Zhang & Liang &mdash; Evaluating Verifiability in Generative "
    "Search Engines (free)",
    "https://arxiv.org/abs/2304.09848",
    "<b>&sect;2 and &sect;3 measured on deployed systems</b> — and the "
    "attribution rates are sobering."),
   ("Nakano et al. &mdash; WebGPT (free)",
    "https://arxiv.org/abs/2112.09332",
    "<b>&sect;1's pipeline with retrieval in the loop</b> — and the "
    "honest discussion of what the citations did and did not "
    "establish."),
 ],
 "exercises": [
   "<b>Build the answering pipeline</b> over your Project 2 "
   "collection.",
   "<b>Measure passage-level retrieval recall</b> separately from answer "
   "quality.",
   "<b>Generate per-sentence citations</b> and sample twenty for "
   "reading.",
   "<b>Record the attribution rate</b> — the fraction genuinely "
   "supported.",
   "<b>Instruct the model to quote first</b> and measure the attribution "
   "rate again.",
   "<b>Add an entailment check</b> and report what it drops.",
   "<b>Construct ten unanswerable questions</b> and measure the "
   "abstention rate.",
   "<b>Reorder the passages worst-first</b> and measure the quality "
   "change.",
   "<b>Compare answering against listing</b> on the same queries, by "
   "user judgement.",
   "<b>Implement difficulty routing</b> between the two modes.",
 ],
 "selfcheck": [
   "What does returning an answer move, and what does the user lose?",
   "How does the failure mode change?",
   "Give the pipeline stages, and say which is the bottleneck.",
   "Contrast weak and strong attribution.",
   "What is the characteristic attribution failure, and why is it worse "
   "than no citation?",
   "Give four ways to improve attribution, and the cheapest.",
   "Name five things to measure, and the free signals.",
   "State the consequence for document authors.",
   "Why is it a collective-action problem?",
   "What is the design most systems skip?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Exposure and Consequences",
 "subtitle": "What a ranking does to the things being ranked.",
 "question": "Who does your ranking affect, and how?",
 "outcomes": [
     "Explain exposure and why rank position is the resource "
     "being allocated.",
     "Explain feedback loops in deployed rankers.",
     "Explain the fairness formulations and their "
     "disagreements.",
     "Explain filter bubbles honestly, including the "
     "evidence.",
     "Assess a ranking system's consequences.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Exposure",
   "blurb": "The resource a ranking allocates."},

  {"t": "callout", "title": "Attention falls steeply with rank, so a ranking allocates a scarce resource",
   "kind": "The fact that makes this a consequential system",
   "body": ["<b>Click-through falls sharply with position</b> "
            "(Module 05 §4) — so <b>rank 1 receives "
            "many times the attention of rank 10, and rank 11 receives "
            "almost none.</b>",
            "<b>Which means a ranking is not a neutral ordering but "
            "an allocation of attention</b> — and attention is "
            "revenue, reach, and opportunity for whoever produced the "
            "document.",
            "<b>And the allocation is extremely "
            "unequal:</b> <b>a small difference in score produces a "
            "large difference in exposure</b>, because the "
            "position-to-attention curve is so steep.",
            "<b>So two documents of nearly equal relevance receive "
            "wildly unequal outcomes</b> — <b>which is a property of "
            "the presentation rather than of the ranking function</b>, "
            "and is where the fairness question starts."]},

  {"t": "bullets", "kicker": "Exposure", "title": "And what follows from it",
   "items": [
     "<b>Ties should be broken randomly, or rotated</b>, because "
     "<b>a deterministic tiebreak gives one document all the exposure "
     "permanently.</b>",
     "",
     "<b>Randomised ranking spreads exposure</b> at a small "
     "quality cost — and it also produces unbiased click data, "
     "which is a second benefit "
     "(Module 05 §4).",
     "",
     "<b>Exposure can be measured and reported</b>: the "
     "distribution of impressions across the catalogue, which is "
     "CSCE 676 §09 §4's coverage "
     "metric.",
     "",
     "<b>And it can be constrained</b>, by an explicit amortised "
     "exposure target — which is a policy decision rather than a "
     "technical one.",
     "",
     "<b>But all of it costs relevance</b>, which has to be stated "
     "rather than hidden.",
   ],
   "footnote": "<b>Randomisation buys two things at once</b> — "
               "fairer exposure and unbiased training data — which "
               "makes it a better deal than it first appears."},

  {"t": "section", "label": "Part 2", "title": "Feedback",
   "blurb": "Why a deployed ranker shapes its own training data."},

  {"t": "callout", "title": "Your training data is the output of your previous ranker",
   "kind": "The loop, and it is not avoidable",
   "body": ["<b>Clicks are only observed on documents you "
            "showed</b> — so <b>the data records what you ranked "
            "highly, not what was best</b> "
            "(CSCE 676 §09 §3).",
            "<b>So a document ranked low gets no clicks, so it looks "
            "unpopular, so it stays ranked low</b> — a "
            "self-fulfilling loop that no amount of model improvement "
            "escapes.",
            "<b>Which means the system converges to its own early "
            "judgements</b>, and a document's initial placement matters "
            "more than its quality.",
            "<b>And the corrections are all forms of "
            "exploration:</b> <b>randomisation, inverse propensity "
            "weighting, and deliberate exposure of new "
            "items</b> — all of which cost short-term "
            "relevance and buy long-term correctness."]},

  {"t": "section", "label": "Part 3", "title": "Fairness",
   "blurb": "Several formulations, and they conflict."},

  {"t": "table", "kicker": "Formulations", "title": "What different fairness criteria require",
   "header": ["Criterion", "Requires", "Tension"],
   "widths": [2.7, 4.0, 5.1],
   "rows": [
     ["<b>Demographic parity of exposure</b>", "<b>Groups get exposure proportional to their share</b>", "<b>Ignores relevance differences</b>"],
     ["<b>Exposure proportional to relevance</b>", "<b>Equal relevance gets equal exposure</b>", "<b>Requires relevance to be measured fairly</b>"],
     ["<b>Individual fairness</b>", "<b>Similar documents ranked similarly</b>", "<b>Requires a similarity metric nobody has</b>"],
     ["<b>Amortised fairness</b>", "<b>Equal exposure over many queries, not one</b>", "<b>Practical, and needs a session concept</b>"],
   ],
   "footnote": "<b>These are mutually incompatible in general</b> "
               "— so <b>choosing a fairness criterion is a value "
               "judgement</b> and cannot be derived from the data, which "
               "is the honest position.",
   "note": "The incompatibility is the point; do not let it be a "
           "technical question."},

  {"t": "callout", "title": "And the two-sided market makes it harder",
   "kind": "Why this is not a single-objective problem",
   "body": ["<b>A ranking serves searchers and also allocates "
            "outcomes to document providers</b> — <b>and the two "
            "have different interests</b>, which a single relevance "
            "objective does not represent.",
            "<b>So 'optimal' is underdetermined:</b> <b>the ranking "
            "best for searchers in aggregate may starve a provider whose "
            "content is good and slightly less popular</b>, which "
            "degrades the catalogue over time.",
            "<b>Which connects to Part 2:</b> <b>provider "
            "starvation is a feedback loop, and the catalogue the system "
            "depends on erodes.</b>",
            "<b>So the honest framing is a multi-objective one with "
            "the weights stated</b> — <b>rather than a single "
            "relevance objective with the other effects "
            "unmeasured.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Filter bubbles",
   "blurb": "Stated with the evidence, which is mixed."},

  {"t": "callout", "title": "The filter bubble argument is plausible and the evidence is more mixed than the discussion suggests",
   "kind": "The honest account",
   "body": ["<b>The mechanism is real:</b> <b>personalisation shows "
            "you more of what you engaged with, which narrows what you "
            "see</b>, and the feedback loop of Part 2 "
            "reinforces it.",
            "<b>And the measured effects are smaller and more "
            "complicated than the argument predicts:</b> <b>several "
            "studies find that algorithmic feeds expose people to more "
            "diverse sources than their own choices "
            "would</b>, because self-selection is also narrowing.",
            "<b>So the honest position is that both the mechanism and "
            "the counter-evidence are real</b> — <b>and that the "
            "effect depends heavily on the platform, the domain, and the "
            "measure</b>, which is why the literature "
            "disagrees.",
            "<b>What follows practically is measurable regardless of "
            "the debate:</b> <b>measure the diversity of what you serve, "
            "report it, and give users control over "
            "personalisation</b> — which is defensible on its own "
            "terms."]},

  {"t": "bullets", "kicker": "Assessment", "title": "And what to assess about a ranking system",
   "items": [
     "<b>The exposure distribution across the catalogue</b>, "
     "reported rather than assumed uniform.",
     "",
     "<b>Whether new items can ever surface</b>, which tests the "
     "feedback loop directly (Part 2).",
     "",
     "<b>The diversity of a typical result list</b>, and of what a "
     "typical user sees over time.",
     "",
     "<b>Which fairness criterion you chose</b> and why — "
     "<b>stated as a value judgement rather than derived</b> "
     "(Part 3).",
     "",
     "<b>And who is affected besides the searcher</b>, which is "
     "the question that is usually not asked at all.",
   ],
   "footnote": "<b>'Who is affected besides the searcher' is the "
               "question this module exists to make askable</b> — and "
               "it has an answer in every deployed ranking "
               "system."},
 ],
 "takeaways": [
   "Attention falls steeply with rank, so a ranking allocates a scarce "
   "resource rather than merely ordering documents.",
   "A small score difference produces a large exposure difference, which "
   "is a property of the presentation rather than the ranking function.",
   "Randomisation buys fairer exposure and unbiased training data at once, "
   "which makes it a better deal than it appears.",
   "A document ranked low gets no clicks, looks unpopular, and stays "
   "ranked low — a loop no model improvement escapes.",
   "The fairness criteria are mutually incompatible in general, so "
   "choosing one is a value judgement and cannot be derived from data.",
   "The filter bubble mechanism is real and the measured effects are more "
   "mixed than the discussion suggests.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Exposure"),
  ("callout", "Attention falls steeply with rank, so a ranking allocates a "
              "scarce resource",
   ["<b>Click-through rate falls sharply with position</b> "
    "(Module 05 &sect;4's position bias) — so <b>rank 1 receives "
    "many times the attention of rank 10, and rank 11, below the fold, "
    "receives almost none at all.</b>",
    "<b>Which means a ranking is not a neutral ordering but an "
    "allocation of attention</b> — and <b>attention is revenue, "
    "reach, and opportunity for whoever produced the document</b>, which "
    "makes the ranking a consequential decision about people rather than "
    "a presentation choice.",
    "<b>And the allocation is extremely unequal:</b> <b>a very small "
    "difference in relevance score produces a very large difference in "
    "exposure</b>, because the position-to-attention curve is so steep "
    "near the top.",
    "<b>So two documents of nearly equal relevance receive wildly "
    "unequal outcomes</b> — <b>which is a property of the "
    "presentation rather than of the ranking function</b>, and <b>is "
    "where the fairness question starts</b> (&sect;3): nothing in the "
    "scoring is unfair, and the outcome is."]),
  ("ul", ["<b>Ties should be broken randomly, or rotated across "
          "impressions</b>, because <b>a deterministic tiebreak gives one "
          "document all of the exposure permanently</b> — and "
          "document id order is a common and entirely arbitrary "
          "tiebreak.",
          "<b>Randomised ranking spreads exposure</b> at a small "
          "quality cost — <b>and it also produces unbiased click "
          "data, which is a second and substantial benefit</b> "
          "(Module 05 &sect;4, and &sect;2's loop).",
          "<b>Exposure can be measured and reported</b>: the "
          "distribution of impressions across the catalogue, <b>which is "
          "CSCE 676 Module 09 &sect;4's coverage metric</b> arriving "
          "here as a fairness measurement.",
          "<b>And it can be constrained</b>, by an explicit amortised "
          "exposure target across queries — <b>which is a policy "
          "decision rather than a technical one</b> and should be made "
          "and stated as such.",
          "<b>But all of it costs relevance</b>, which has to be "
          "stated rather than hidden — there is no free fairness "
          "intervention here. <b>Randomisation buys two things at "
          "once</b> — fairer exposure and unbiased training "
          "data — <b>which makes it a considerably better deal than "
          "it first appears</b> and is the intervention to reach for "
          "first."]),

  ("h1", "2 &nbsp; Feedback"),
  ("callout", "Your training data is the output of your previous ranker",
   ["<b>Clicks are only ever observed on documents you actually "
    "showed</b> — so <b>the data records what you ranked highly "
    "rather than what was best</b> (CSCE 676 Module 09 &sect;3's "
    "feedback loop, in its original setting).",
    "<b>So a document ranked low receives no clicks, therefore looks "
    "unpopular, therefore stays ranked low</b> — <b>a "
    "self-fulfilling loop that no amount of model improvement "
    "escapes</b>, because the model is learning from data the previous "
    "model generated.",
    "<b>Which means the system converges toward its own early "
    "judgements</b>, and <b>a document's initial placement matters more "
    "than its actual quality</b> — which is a striking and "
    "uncomfortable property of a system that looks purely "
    "meritocratic.",
    "<b>And the corrections are all forms of exploration:</b> "
    "<b>randomisation (&sect;1), inverse propensity weighting of the "
    "click data, and deliberate exposure of new items</b> — <b>all "
    "of which cost short-term relevance and buy long-term "
    "correctness</b>, which is a trade worth making explicitly rather "
    "than by default."]),

  ("break",),
  ("h1", "3 &nbsp; Fairness"),
  ("table", ["Criterion", "What it requires", "The tension"],
   [["<b>Demographic parity of exposure</b>",
     "<b>Groups receive exposure proportional to their share of the "
     "catalogue.</b>",
     "<b>It ignores genuine relevance differences</b>, so it can require "
     "showing worse results."],
    ["<b>Exposure proportional to relevance</b>",
     "<b>Documents of equal relevance receive equal exposure.</b>",
     "<b>It requires relevance to have been measured fairly</b>, which "
     "&sect;2's loop undermines."],
    ["<b>Individual fairness</b>",
     "<b>Similar documents are ranked similarly.</b>",
     "<b>It requires a similarity metric that nobody has</b>, and the "
     "metric choice carries the whole decision."],
    ["<b>Amortised fairness</b>",
     "<b>Equal exposure across many queries rather than within one "
     "result list.</b>",
     "<b>Practical and implementable, and it needs a session or time "
     "window concept</b> to amortise over."]],
   [0.22, 0.34, 0.44]),
  ("p", "<b>These criteria are mutually incompatible in general</b> "
        "— satisfying one can require violating another, which is a "
        "formal result rather than an engineering difficulty — <b>so "
        "choosing a fairness criterion is a value judgement and cannot be "
        "derived from the data</b>. <b>That is the honest position</b>, "
        "and <b>the incompatibility is the point: it should not be "
        "allowed to become a technical question</b> with a technical "
        "answer, because it does not have one."),
  ("callout", "And the two-sided market makes it harder",
   ["<b>A ranking serves searchers and simultaneously allocates "
    "outcomes to document providers</b> — sellers, publishers, "
    "authors, creators — <b>and the two sides have different "
    "interests</b>, which <b>a single relevance objective does not "
    "represent at all.</b>",
    "<b>So 'optimal' is underdetermined:</b> <b>the ranking that is "
    "best for searchers in aggregate may starve a provider whose content "
    "is good and only slightly less popular</b>, which <b>degrades the "
    "catalogue over time</b> as that provider leaves.",
    "<b>Which connects directly to &sect;2:</b> <b>provider "
    "starvation is itself a feedback loop, and the catalogue the system "
    "depends on erodes</b> — the same structure as Module 11 "
    "&sect;4's collective-action problem, at a different level.",
    "<b>So the honest framing is a multi-objective one with the "
    "weights stated</b> — <b>rather than a single relevance "
    "objective with all the other effects left unmeasured</b>, which is "
    "the default and is the thing this module asks you to notice."]),

  ("h1", "4 &nbsp; Filter bubbles, and assessment"),
  ("callout", "The filter bubble argument is plausible and the evidence is "
              "more mixed than the discussion suggests",
   ["<b>The mechanism is real:</b> <b>personalisation shows you more "
    "of what you previously engaged with, which narrows the range of what "
    "you see</b>, and <b>&sect;2's feedback loop reinforces it</b> at the "
    "system level.",
    "<b>And the measured effects are smaller and more complicated than "
    "the argument predicts:</b> <b>several careful studies find that "
    "algorithmic feeds expose people to <i>more</i> diverse sources than "
    "their own unaided choices would</b>, because <b>self-selection is "
    "also strongly narrowing</b> and the comparison baseline matters.",
    "<b>So the honest position is that both the mechanism and the "
    "counter-evidence are real</b> — <b>and that the effect depends "
    "heavily on the platform, the domain, the measure of diversity, and "
    "the comparison chosen</b>, which is precisely why the literature "
    "disagrees rather than one side being mistaken.",
    "<b>What follows practically is measurable regardless of how the "
    "debate resolves:</b> <b>measure the diversity of what you serve, "
    "report it, and give users control over personalisation</b> — "
    "<b>which is defensible on its own terms</b> and does not require "
    "settling the empirical question first."]),
  ("ul", ["<b>The exposure distribution across the catalogue</b>, "
          "<b>reported rather than assumed uniform</b> — which is one "
          "query against your impression logs.",
          "<b>Whether new items can ever surface</b>, which <b>tests "
          "the feedback loop directly</b> (&sect;2) and is answerable by "
          "tracking a cohort of newly added documents.",
          "<b>The diversity of a typical result list</b>, and "
          "separately <b>the diversity of what a typical user sees over "
          "time</b> — which are different questions and &sect;4's "
          "debate is about the second.",
          "<b>Which fairness criterion you chose and why</b> — "
          "<b>stated as a value judgement rather than presented as "
          "derived</b> (&sect;3), because presenting a value judgement as "
          "a technical result is the characteristic dishonesty in this "
          "area.",
          "<b>And who is affected besides the searcher</b>, which is "
          "<b>the question that is usually not asked at all</b>. <b>'Who "
          "is affected besides the searcher' is the question this module "
          "exists to make askable</b> — and <b>it has an answer in "
          "every deployed ranking system</b>, whether or not anybody has "
          "looked for it."]),
 ],
 "resources": [
   ("Singh & Joachims &mdash; Fairness of Exposure in Rankings (free)",
    "https://arxiv.org/abs/1802.07281",
    "<b>&sect;1 and &sect;3 formalised</b> — exposure as the allocated "
    "resource, with the optimisation framework."),
   ("Biega, Gummadi & Weikum &mdash; Equity of Attention (free)",
    "https://arxiv.org/abs/1805.01788",
    "<b>&sect;3's fourth row</b> — amortised fairness, which is the "
    "most implementable of the criteria."),
   ("Joachims et al. &mdash; Unbiased Learning-to-Rank with Biased "
    "Feedback (free)",
    "https://arxiv.org/abs/1608.04468",
    "<b>&sect;2's correction</b> — inverse propensity weighting, and "
    "what it requires to work."),
   ("Bakshy, Messing & Adamic, and the subsequent debate (free)",
    "https://www.science.org/doi/10.1126/science.aaa1160",
    "<b>&sect;4's counter-evidence and its critics</b> — read the "
    "paper and at least one critique, since the disagreement is the "
    "lesson."),
 ],
 "exercises": [
   "<b>Measure click-through by position</b> on any log you have, and "
   "plot the curve.",
   "<b>Compute the exposure a one-position improvement buys.</b>",
   "<b>Find a deterministic tiebreak</b> in your system and make it "
   "random.",
   "<b>Measure the exposure distribution</b> across your catalogue.",
   "<b>Track a cohort of new documents</b> and report whether any "
   "surfaced.",
   "<b>Simulate the feedback loop</b>: train on your own rankings' "
   "clicks for several rounds and measure coverage.",
   "<b>Implement two fairness criteria</b> and show a case where they "
   "disagree.",
   "<b>Measure the relevance cost</b> of your chosen criterion.",
   "<b>Measure result-list diversity</b> and per-user diversity over "
   "time.",
   "<b>List who besides the searcher</b> is affected by your ranking, "
   "and how.",
 ],
 "selfcheck": [
   "Why is a ranking an allocation rather than an ordering?",
   "Why do near-equal documents get unequal outcomes?",
   "Give four consequences of the exposure curve, and what "
   "randomisation buys.",
   "State the feedback loop and why model improvement does not escape "
   "it.",
   "Name three corrections and what they cost.",
   "Name four fairness criteria and the tension in each.",
   "Why can a fairness criterion not be derived from data?",
   "Why does a two-sided market make 'optimal' underdetermined?",
   "State the filter bubble position honestly, with both sides.",
   "Give five things to assess, and the question this module makes "
   "askable.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Claiming Relevance Honestly",
 "subtitle": "What a retrieval evaluation establishes.",
 "question": "Your NDCG improved. What follows?",
 "outcomes": [
     "State what a retrieval result establishes.",
     "Identify the standard overclaims.",
     "Write a defensible system claim.",
     "Place this course relative to CSCE 638 and CSCE 676.",
     "State a proportionate practice for building search.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What a result establishes",
   "blurb": "Precisely, and it is about the judgement set."},

  {"t": "callout", "title": "A metric improvement is a statement about a judgement set, a metric, and a query sample",
   "kind": "The honest reading",
   "body": ["<b>It establishes that on these queries, under these "
            "judgements, by this metric, the new system scored "
            "higher</b> — four clauses, and the judgements are the "
            "one people treat as objective.",
            "<b>And the judgements encode a user model</b> "
            "(Module 05 §3) — so <b>a different metric can "
            "reverse the ranking of two systems</b>, which is not rare "
            "and is worth checking.",
            "<b>It does not establish that users will be better "
            "served</b>, because <b>relevance judgements are a proxy "
            "for a need the judge did not have</b> "
            "(Module 01 §1).",
            "<b>And on an old collection, it may partly reflect "
            "pooling</b> (Module 05 §1) — <b>so a gain "
            "from a method unlike the pool's builders is "
            "understated</b>, and one from a similar method is "
            "flattered."]},

  {"t": "table", "kicker": "Overclaims", "title": "The standard overclaims, corrected",
   "header": ["Claim", "Correction"],
   "widths": [4.4, 6.6],
   "rows": [
     ["<b>'Our system is better'</b>", "<b>On these queries, by this metric, against which baseline? (M05 §4)</b>"],
     ["<b>'NDCG improved 3%'</b>", "<b>Mean or median? How many queries got worse? (M05 §4)</b>"],
     ["<b>'Semantic search beats keyword search'</b>", "<b>In domain. Out of domain it loses (M07 §3)</b>"],
     ["<b>'We beat BM25'</b>", "<b>Tuned, or default? (M03 §3)</b>"],
     ["<b>'The answer is cited'</b>", "<b>Does the citation support the claim? (M11 §2)</b>"],
     ["<b>'The ranking is neutral'</b>", "<b>It allocates attention. Neutral by which criterion? (M12)</b>"],
   ],
   "footnote": "<b>The last row is the one with consequences outside "
               "the system</b> — 'neutral' is not a property a "
               "ranking can have, because any ordering allocates and "
               "every allocation implements some criterion.",
   "note": "The neutrality overclaim is the one worth attacking "
           "hardest."},

  {"t": "section", "label": "Part 2", "title": "Claims you can defend",
   "blurb": "With the proxy disclosed."},

  {"t": "bullets", "kicker": "Honest", "title": "Defensible claims",
   "items": [
     "<b>'On 50 queries we wrote from real needs, with judgements "
     "we made against written criteria, NDCG@10 is 0.61 against a tuned "
     "BM25's 0.54; 38 queries improved and 7 got "
     "worse.'</b>",
     "",
     "<b>'First-stage recall at 500 is 0.89; the reranker "
     "contributes 0.04 NDCG over that candidate "
     "set.'</b> <b>Stage-attributed</b> "
     "(Module 06 §4).",
     "",
     "<b>'Median latency 40 ms, 95th percentile 180 ms, at "
     "recall 0.95'</b> — <b>quality and cost "
     "together</b> (Module 04 §4).",
     "",
     "<b>'Of 20 sampled answer sentences, 14 were supported by "
     "their citations.'</b> <b>A measured attribution "
     "rate</b> (Module 11 §2).",
     "",
     "<b>And: 'we have not evaluated on identifier queries, or on "
     "any collection but this one.'</b>",
   ],
   "footnote": "<b>The limitation statement is Project 2's "
               "hardest-graded requirement</b>, and the "
               "queries-got-worse count is the clause that most changes "
               "how a result is read."},

  {"t": "section", "label": "Part 3", "title": "The semester",
   "blurb": "Three proxies, one discipline."},

  {"t": "table", "kicker": "Semester 10", "title": "Where this course sits",
   "header": ["Course", "Its proxy", "What the proxy omits"],
   "widths": [2.3, 3.6, 5.6],
   "rows": [
     ["<b>CSCE 638</b>", "<b>A metric for a quality judgement</b>", "<b>Factuality, and whether anyone is helped</b>"],
     ["<b>CSCE 676</b>", "<b>A score for a pattern being real</b>", "<b>How hard you looked</b>"],
     ["<b>CSCE 670</b>", "<b>A label for relevance to a person</b>", "<b>The need, the session, and redundancy</b>"],
   ],
   "footnote": "<b>And the shared discipline is the "
               "same:</b> <b>name the proxy, state what it omits, and "
               "report the distribution rather than the mean</b> — "
               "which is CSCE 633 Module 12's argument, three "
               "ways.",
   "note": "The three-proxies framing is the semester's "
           "conclusion."},

  {"t": "section", "label": "Part 4", "title": "A proportionate practice",
   "blurb": "What to actually do, in order."},

  {"t": "bullets", "kicker": "Practice", "title": "Building search, in order of return",
   "items": [
     "<b>1 · Tuned BM25 with good "
     "preprocessing</b> (Modules 02–03) — <b>which gets "
     "you most of the way and is cheap</b>, and is where a "
     "surprising number of systems should stop.",
     "",
     "<b>2 · Spelling correction</b> "
     "(Module 09 §1) — <b>the highest-value single "
     "addition</b>, because its failures are total.",
     "",
     "<b>3 · A judgement set and an evaluation</b> "
     "(Module 05) — <b>before any further "
     "improvement</b>, because otherwise you cannot tell.",
     "",
     "<b>4 · Hybrid retrieval and a reranker</b> "
     "(Modules 06–07), with the latency "
     "measured.",
     "",
     "<b>5 · And then the consequences:</b> exposure, "
     "feedback, and diversity "
     "(Module 12) — <b>which should not wait for "
     "scale.</b>",
   ],
   "footnote": "<b>Step 3 before step 4 is the ordering people get "
               "wrong</b> — building the neural system before the "
               "evaluation means never knowing whether it "
               "helped."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can build a search engine:</b> <b>an index with "
            "compression and skips, a derived scoring function, efficient "
            "query processing with safe early termination, and a learned "
            "or hybrid ranker in two stages.</b>",
            "<b>You can evaluate one honestly</b> — <b>a judgement "
            "set you made, a metric chosen from the use, a tuned "
            "baseline, and the per-query distribution</b> — which is "
            "the half that most systems omit.",
            "<b>And you know that a ranking allocates "
            "attention</b> (Module 12), so <b>the question 'who else is "
            "affected' is one you now ask.</b>",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it means naming the "
            "judgement set, the metric, and the baseline</b> — "
            "because <b>'relevant' is a relation and the system never "
            "saw one side of it.</b>"]},
 ],
 "takeaways": [
   "A metric improvement is a statement about a judgement set, a metric, "
   "and a query sample — and the judgements are the clause people "
   "treat as objective.",
   "A different metric can reverse the ranking of two systems, which is "
   "not rare and is worth checking.",
   "'We beat BM25' requires saying whether it was tuned, and 'semantic "
   "beats keyword' holds in domain and fails out of it.",
   "'Neutral' is not a property a ranking can have, because any ordering "
   "allocates attention.",
   "Build the evaluation before the neural system, or you will never know "
   "whether it helped.",
   "The three Semester 10 courses share one discipline: name the proxy, "
   "state what it omits, and report the distribution.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What a result establishes"),
  ("callout", "A metric improvement is a statement about a judgement set, a "
              "metric, and a query sample",
   ["<b>It establishes that on these particular queries, under these "
    "particular judgements, by this particular metric, the new system "
    "scored higher</b> — <b>four clauses, and the judgements are the "
    "one people routinely treat as objective</b> when they are the most "
    "contestable.",
    "<b>And the judgements encode a user model</b> (Module 05 "
    "&sect;3's metric-as-user-model point) — so <b>a different "
    "metric can reverse the ranking of two systems</b>, <b>which is not "
    "rare and is worth checking</b> before reporting a single number.",
    "<b>It does not establish that users will be better served</b>, "
    "because <b>relevance judgements are a proxy for an information need "
    "that the judge did not actually have</b> (Module 01 &sect;1's "
    "governing fact) — which is the gap the whole course has been "
    "working within.",
    "<b>And on an older test collection, the improvement may partly "
    "reflect pooling</b> (Module 05 &sect;1) — <b>so a gain from "
    "a method unlike the pool's original builders is systematically "
    "understated, and a gain from a similar method is flattered</b>, "
    "which is a bias in a specific and predictable direction."]),
  ("table", ["The claim", "The correction"],
   [["<b>'Our system is better.'</b>",
     "<b>On which queries, by which metric, against which "
     "baseline?</b> (Module 05 &sect;4.)"],
    ["<b>'NDCG improved by 3%.'</b>",
     "<b>Mean or median? And how many queries got worse?</b> "
     "(Module 05 &sect;4's per-query distribution.)"],
    ["<b>'Semantic search beats keyword search.'</b>",
     "<b>In domain. Out of domain it loses</b> (Module 07 "
     "&sect;3), and on identifier queries it loses badly."],
    ["<b>'We beat BM25.'</b>",
     "<b>Tuned, or library default?</b> (Module 03 &sect;3's "
     "callout.) The two are different claims."],
    ["<b>'The answer is cited.'</b>",
     "<b>Does the citation actually support the claim?</b> "
     "(Module 11 &sect;2.)"],
    ["<b>'The ranking is neutral.'</b>",
     "<b>It allocates attention</b> (Module 12 &sect;1). <b>Neutral "
     "by which criterion?</b> See the note."]],
   [0.34, 0.66]),
  ("p", "<b>The last row is the one with consequences outside the "
        "system</b>, and it is worth attacking hardest: <b>'neutral' is "
        "not a property a ranking can have</b>, <b>because any ordering "
        "allocates attention and every allocation implements some "
        "criterion</b> — including the criterion of whatever the "
        "scoring function happened to optimise. <b>A system cannot "
        "decline to choose</b>; it can only decline to say which choice it "
        "made (Module 12 &sect;3's value judgement)."),

  ("h1", "2 &nbsp; Claims you can defend"),
  ("ul", ["<b>'On 50 queries written from real information needs, with "
          "relevance judgements we made against written criteria, NDCG@10 "
          "is 0.61 against a tuned BM25's 0.54; 38 queries improved and 7 "
          "got worse.'</b> <b>Every clause checkable, and the "
          "got-worse count is the one that changes how it reads.</b>",
          "<b>'First-stage recall at 500 is 0.89; the cross-encoder "
          "reranker contributes 0.04 NDCG over that candidate "
          "set.'</b> <b>Stage-attributed</b> (Module 06 &sect;4), "
          "which tells a reader which half to invest in.",
          "<b>'Median latency 40 ms, 95th percentile 180 ms, at an "
          "approximate-search recall of 0.95.'</b> <b>Quality and cost "
          "reported together</b> (Module 04 &sect;4, Module 08 "
          "&sect;4), which is the only way either is meaningful.",
          "<b>'Of 20 sampled answer sentences, 14 were genuinely "
          "supported by the passages cited for them.'</b> <b>A measured "
          "attribution rate</b> (Module 11 &sect;2) rather than a "
          "claim that the system cites its sources.",
          "<b>And: 'we have not evaluated on identifier or "
          "exact-match queries, or on any collection other than this "
          "one.'</b> <b>The limitation statement is Project 2's "
          "hardest-graded requirement</b>, and <b>the queries-got-worse "
          "count is the clause that most changes how a result is "
          "read</b> — which is why both are required."]),

  ("break",),
  ("h1", "3 &nbsp; The semester"),
  ("table", ["Course", "Its proxy", "What the proxy omits"],
   [["<b>CSCE 638</b>",
     "<b>A metric standing in for a quality judgement</b> — BLEU, "
     "ROUGE, a judge model.",
     "<b>Factuality, and whether anybody was actually helped</b> "
     "(its Module 10 &sect;3)."],
    ["<b>CSCE 676</b>",
     "<b>A score standing in for a pattern being real</b> — "
     "modularity, silhouette, support.",
     "<b>How hard you looked</b> (its Module 11) — the search is "
     "invisible in the score."],
    ["<b>CSCE 670 (this one)</b>",
     "<b>A relevance label standing in for relevance to a person</b>.",
     "<b>The need itself, the session, and redundancy within a list</b> "
     "(Module 01 &sect;3, Module 05 &sect;3)."]],
   [0.20, 0.34, 0.46]),
  ("p", "<b>And the shared discipline is the same in all "
        "three:</b> <b>name the proxy, state what it omits, and report "
        "the distribution rather than the mean</b> — which is "
        "<b>CSCE 633 Module 12's choose-the-metric-from-the-use "
        "argument, arriving three separate ways in one semester</b>. "
        "<b>The three-proxies framing is the semester's conclusion</b>, "
        "and it is worth more than any individual technique in it, because "
        "it transfers to every measurement problem."),

  ("h1", "4 &nbsp; A proportionate practice"),
  ("ul", ["<b>1 &middot; A tuned BM25 with good preprocessing</b> "
          "(Modules 02 and 03) — <b>which gets you most of the "
          "way and is cheap</b>, and <b>is where a surprising number of "
          "systems should simply stop</b>, having met their "
          "requirement.",
          "<b>2 &middot; Spelling correction</b> (Module 09 "
          "&sect;1) — <b>the highest-value single addition</b>, "
          "<b>because its failures are total rather than degraded</b> and "
          "a substantial fraction of queries are affected.",
          "<b>3 &middot; A judgement set and a working "
          "evaluation</b> (Module 05) — <b>before any further "
          "improvement</b>, <b>because otherwise you cannot tell whether "
          "anything you do next helps.</b>",
          "<b>4 &middot; Hybrid retrieval and a cross-encoder "
          "reranker</b> (Modules 06 and 07), <b>with the latency "
          "measured at the tail</b> and the stages attributed "
          "separately.",
          "<b>5 &middot; And then the consequences:</b> exposure, the "
          "feedback loop, and diversity (Module 12) — <b>which "
          "should not wait for scale</b>, since the feedback loop starts "
          "with the first deployment. <b>Step 3 before step 4 is the "
          "ordering people get wrong</b>: <b>building the neural system "
          "before the evaluation means never knowing whether it "
          "helped</b>, and that is the commonest way effort is wasted in "
          "this field."]),
  ("callout", "Where this course leaves you",
   ["<b>You can build a search engine:</b> <b>an inverted index with "
    "compression and skip pointers, a scoring function you can derive "
    "rather than recite, efficient query processing with safe early "
    "termination, and a learned or hybrid ranker in two stages.</b>",
    "<b>You can evaluate one honestly</b> — <b>a judgement set "
    "you made against criteria you wrote first, a metric chosen from how "
    "the results will be used, a properly tuned baseline, and the "
    "per-query distribution rather than the mean</b> — <b>which is "
    "the half that most systems omit</b> and the half this course spent "
    "its centre on.",
    "<b>And you know that a ranking allocates attention rather than "
    "merely ordering documents</b> (Module 12), so <b>the question "
    "'who else is affected by this' is one you now ask</b> as a matter of "
    "course rather than when prompted.",
    "<b>The closing rule is the program's, unchanged across thirty "
    "courses:</b> <b>state what you measured, state what you assumed, "
    "and never claim more than you established.</b> <b>In this subject "
    "it means naming the judgement set, the metric, and the "
    "baseline</b> — because <b>'relevant' is a relation and the "
    "system never saw one side of it</b> (Module 01 &sect;1), which is "
    "where the course began and is what every claim in it has to "
    "respect."]),
 ],
 "resources": [
   ("Armstrong et al. &mdash; Improvements that don't add up (free)",
    "https://dl.acm.org/doi/10.1145/1645953.1646031",
    "<b>&sect;1's problem, measured across a decade of papers</b> — "
    "weak baselines producing apparent cumulative progress that was not "
    "there."),
   ("Lin &mdash; The Neural Hype and Comparisons Against Weak Baselines "
    "(free)",
    "https://sigir.org/wp-content/uploads/2019/01/p040.pdf",
    "<b>&sect;1's fourth row</b> — the tuned-baseline argument, stated "
    "directly."),
   ("Fuhr &mdash; Some Common Mistakes In IR Evaluation (free)",
    "https://sigir.org/wp-content/uploads/2017/06/p032.pdf",
    "<b>&sect;1 and &sect;2</b> — a short, pointed list, and worth "
    "checking your own work against."),
   ("Sakai &mdash; Statistical Reform in Information Retrieval? (free)",
    "https://sigir.org/wp-content/uploads/2017/06/p003.pdf",
    "<b>&sect;2's reporting requirements</b> — significance testing, "
    "effect sizes, and the per-query distribution."),
 ],
 "exercises": [
   "<b>Take a published retrieval result</b> and assess it against "
   "§1's table.",
   "<b>Check whether its baseline was tuned.</b>",
   "<b>Compute two metrics on the same two systems</b> and find a case "
   "where they disagree.",
   "<b>Count the queries your system made worse</b>, and report it.",
   "<b>Write the defensible claim</b> for your Project 2 system, in "
   "§2's form.",
   "<b>Write its limitation statement.</b>",
   "<b>Name the proxy</b> in each of the three Semester 10 courses, and "
   "what each omits.",
   "<b>Audit your own build order</b> against §4's five steps.",
   "<b>Revisit Module 01's last exercise</b> and compare.",
   "<b>Project 2 is now due.</b> Submit the collection, the thirty "
   "need-derived queries, your judgements and criteria, the tuned "
   "baseline, your system, the evaluation with latency, and the "
   "twenty-worst-query analysis.",
 ],
 "selfcheck": [
   "What four clauses does a metric improvement require?",
   "Why can a different metric reverse two systems' order?",
   "What does a metric improvement not establish?",
   "How does pooling bias an improvement, and in which direction?",
   "Give six overclaims and the correction to each.",
   "Why can a ranking not be neutral?",
   "Give four defensible claim forms.",
   "Name the proxy in each Semester 10 course and what it omits.",
   "Give the five-step build order, and which ordering people get "
   "wrong.",
   "In this course, what does 'never claim more than you established' "
   "mean?",
 ],
},

]
