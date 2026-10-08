# -*- coding: utf-8 -*-
"""CSCE 670 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "The Index",
 "subtitle": "The data structure that makes search possible.",
 "question": "How do you avoid reading every document?",
 "outcomes": [
     "Explain the inverted index and what it stores.",
     "Explain the preprocessing decisions and their costs.",
     "Explain postings compression and why it is worth it.",
     "Explain index construction at scale.",
     "Build an index and measure it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The structure",
   "blurb": "A map from term to the documents containing it."},

  {"t": "code", "kicker": "Structure", "title": "What an inverted index holds",
   "lang": "text", "code": """
  DICTIONARY        term -> (document frequency,
                    pointer into the postings)

  POSTINGS LIST     for each term, the documents
                    containing it, in increasing
                    document-id order:
                        doc_id, term_frequency,
                        [positions]

  AND THE CHOICES
      positions      needed for phrase and proximity
                     queries; they roughly triple the
                     index size
      frequencies    needed for any ranked retrieval
                     (Module 03)
      field info     which part of the document the
                     term appeared in, for Module 06's
                     features

  WHY SORTED BY DOCUMENT ID
      intersecting two sorted lists is linear in
      their lengths, and compression works far better
      on an increasing sequence (Part 3).
""",
   "caption": "<b>Sorted by document id is the decision everything "
              "else follows from</b> — it makes intersection linear "
              "and compression effective at once.",
   "note": "The sorted-order consequence is the structural insight."},

  {"t": "callout", "title": "The index trades space and build time for query time, which is the right trade",
   "kind": "Why this structure and not another",
   "body": ["<b>Scanning every document per query is O(collection) "
            "per query</b> — which is unaffordable at any "
            "scale, since queries are frequent and the collection is "
            "large.",
            "<b>An inverted index makes a query cost proportional to "
            "the length of the matching postings lists</b> — which "
            "for most terms is a tiny fraction of the collection.",
            "<b>And the cost is an index typically 10 to 40% of the "
            "collection size</b>, built once and updated "
            "incrementally.",
            "<b>Which is a good trade because queries vastly "
            "outnumber indexing operations</b> — and <b>recognising "
            "which side of a read/write asymmetry you are on is the "
            "general lesson</b>, applicable well beyond search."]},

  {"t": "section", "label": "Part 2", "title": "Preprocessing",
   "blurb": "Each decision is lossy, and the loss has to be chosen."},

  {"t": "bullets", "kicker": "Decisions", "title": "The decisions, and what each costs",
   "items": [
     "<b>Tokenisation.</b> <b>What counts as a term</b> — "
     "hyphenation, apostrophes, numbers, identifiers, and "
     "non-space-delimited scripts "
     "(CSCE 638 §02).",
     "",
     "<b>Case folding.</b> <b>Nearly always worth it, and it loses "
     "'US' versus 'us'</b> — which matters for named entities and "
     "not for topics.",
     "",
     "<b>Stemming.</b> <b>Improves recall and reduces "
     "precision</b> — and aggressive stemmers conflate unrelated "
     "words, which is why lighter ones are now "
     "preferred.",
     "",
     "<b>Stopword removal.</b> <b>Once essential for space, now "
     "mostly unnecessary</b> — and <b>it breaks phrase queries "
     "like 'to be or not to be'</b>.",
     "",
     "<b>And the index must do the same thing to queries as to "
     "documents</b> — <b>a mismatch here is a silent and complete "
     "failure</b> for the affected terms.",
   ],
   "footnote": "<b>The query-document symmetry requirement is the one "
               "that causes real bugs</b> — a stemmer applied at "
               "index time and not at query time makes a term class "
               "unfindable."},

  {"t": "section", "label": "Part 3", "title": "Compression",
   "blurb": "Which buys speed, not only space."},

  {"t": "code", "kicker": "Compression", "title": "The techniques, and why they are worth it",
   "lang": "text", "code": """
  GAP ENCODING
      store differences rather than absolute ids:
          17, 41, 42, 93  ->  17, 24, 1, 51
      Frequent terms give small gaps, which is
      exactly where the space goes.

  VARIABLE-BYTE
      one byte per 7 bits of value, with a
      continuation flag. Simple, fast to decode,
      byte-aligned.

  BIT-PACKED AND SIMD-FRIENDLY SCHEMES
      pack a block of gaps at the width the largest
      one needs. Much faster to decode than
      bit-by-bit codes, which is why they displaced
      Elias gamma and Golomb in practice.

  AND THE REASON IT BUYS SPEED
      the index is read from disk or from memory, and
      decoding is cheaper than the I/O saved. A
      smaller index is a faster index, which is the
      counterintuitive part.
""",
   "caption": "<b>A smaller index is a faster index</b> — because "
              "the bottleneck is data movement rather than "
              "decoding (CSCE 676 §01 §2).",
   "note": "The speed argument is why compression is not optional."},

  {"t": "callout", "title": "And skip pointers make intersection sublinear",
   "kind": "The other structural optimisation",
   "body": ["<b>Store occasional forward pointers into a postings "
            "list</b> — so that intersecting a short list with a "
            "long one can skip over the long one's irrelevant "
            "stretches.",
            "<b>Which matters because query term frequencies are "
            "wildly uneven</b>: <b>intersecting a rare term's hundred "
            "postings against a common term's ten million is the normal "
            "case</b>.",
            "<b>And the right skip interval is about √(list "
            "length)</b>, which balances the pointer overhead against "
            "the skipping gain.",
            "<b>But skips interact badly with "
            "compression</b> — <b>you cannot skip into the middle of "
            "a gap-encoded block without decoding it</b>, which is why "
            "real formats store skips at block boundaries."]},

  {"t": "section", "label": "Part 4", "title": "Building it",
   "blurb": "When the index does not fit in memory."},

  {"t": "bullets", "kicker": "Construction", "title": "The methods, in order of scale",
   "items": [
     "<b>In memory</b>, for a collection that fits — a "
     "dictionary of lists, then sorted and written "
     "out.",
     "",
     "<b>Blocked sort-based indexing</b>, for one that does "
     "not: <b>index blocks that fit, write each to disk, then merge "
     "the sorted runs</b> — which is external merge "
     "sort.",
     "",
     "<b>Single-pass in-memory indexing</b>, which avoids the "
     "global term-id mapping by writing dictionaries per block and "
     "merging them too.",
     "",
     "<b>Distributed</b>, which is a MapReduce by term "
     "(CSCE 676 §10) — and the shuffle is the "
     "cost.",
     "",
     "<b>And incremental updates</b>, usually by keeping a small "
     "in-memory index and merging periodically — because "
     "<b>rebuilding is cheaper than updating a compressed postings "
     "list in place.</b>",
   ],
   "footnote": "<b>The merge-rather-than-update conclusion recurs in "
               "storage engines generally</b> — a compressed, "
               "sorted structure is cheap to read and expensive to modify, "
               "so you write a new one."},

  {"t": "callout", "title": "And what to measure about an index",
   "kind": "Closing",
   "body": ["<b>Size against the raw collection</b>, with <b>the "
            "compression attributed per technique</b> rather than "
            "reported as a total — which is Project 1's "
            "requirement.",
            "<b>Build time, and whether it is "
            "parallelisable</b> — since a reindex is an operation you "
            "will perform repeatedly.",
            "<b>Query latency at the median and the 95th "
            "percentile</b>, because <b>the tail is what users "
            "experience as 'slow'</b>.",
            "<b>And the postings list length distribution</b>, which "
            "is heavy-tailed (CSCE 676 §07 §1) and "
            "determines which optimisations matter."]},
 ],
 "takeaways": [
   "Sorting postings by document id makes intersection linear and "
   "compression effective at the same time.",
   "The index trades space and build time for query time, which is right "
   "because queries vastly outnumber indexing operations.",
   "The index must do the same preprocessing to queries as to documents, "
   "and a mismatch is a silent complete failure.",
   "A smaller index is a faster index, because the bottleneck is data "
   "movement rather than decoding.",
   "Skip intervals of about the square root of the list length balance "
   "overhead against gain, and skips must sit at block boundaries.",
   "Merging a new index is cheaper than updating a compressed postings "
   "list in place, which recurs in storage engines generally.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The structure"),
  ("code", """DICTIONARY        term -> (document frequency,
                  pointer into the postings)

POSTINGS LIST     for each term, the documents
                  containing it, in increasing
                  document-id order:
                      doc_id, term_frequency,
                      [positions]

AND THE CHOICES
    positions      needed for phrase and proximity
                   queries; they roughly triple the
                   index size
    frequencies    needed for any ranked retrieval
                   at all (Module 03)
    field info     which part of the document the
                   term appeared in -- title, body,
                   anchor text -- for Module 06's
                   features

WHY SORTED BY DOCUMENT ID
    intersecting two sorted lists is linear in their
    lengths, and compression works far better on an
    increasing sequence (section 3)."""),
  ("p", "<b>Sorted by document id is the decision everything else "
        "follows from</b> — <b>it makes intersection linear and it "
        "makes compression effective, at the same time and for the same "
        "reason</b>. An index sorted by relevance or by frequency would "
        "support neither. <b>That structural insight is worth "
        "generalising</b>: choosing the order a structure is stored in "
        "frequently determines which operations are cheap, and it is a "
        "decision made once."),
  ("callout", "The index trades space and build time for query time, which "
              "is the right trade",
   ["<b>Scanning every document for every query is O(collection) per "
    "query</b> — which is unaffordable at any meaningful scale, "
    "since queries arrive constantly and the collection is large.",
    "<b>An inverted index makes a query cost proportional to the "
    "length of the matching postings lists</b> — <b>which for most "
    "terms is a tiny fraction of the collection</b>, and which is the "
    "entire point of the structure.",
    "<b>And the cost is an index typically 10 to 40% of the "
    "collection's size</b> (depending heavily on whether positions are "
    "stored), <b>built once and then updated incrementally</b> "
    "(&sect;4).",
    "<b>Which is a good trade precisely because queries vastly "
    "outnumber indexing operations</b> — and <b>recognising which "
    "side of a read/write asymmetry you are on is the general "
    "lesson</b>, applicable well beyond search: it is the same reasoning "
    "behind a database index, a materialised view, and a cache."]),

  ("h1", "2 &nbsp; Preprocessing"),
  ("ul", ["<b>Tokenisation.</b> <b>What counts as a term</b> — "
          "hyphenation, apostrophes, numbers, product identifiers, URLs, "
          "and non-space-delimited scripts (CSCE 638 Module 02's "
          "whole subject, and the same conclusion: it is a modelling "
          "decision rather than a detail).",
          "<b>Case folding.</b> <b>Nearly always worth doing, and it "
          "loses 'US' versus 'us' and 'May' versus 'may'</b> — which "
          "<b>matters considerably for named entity queries and barely at "
          "all for topical ones</b>, so the right answer depends on your "
          "query mix.",
          "<b>Stemming.</b> <b>Improves recall and reduces "
          "precision</b> — and <b>aggressive stemmers conflate "
          "unrelated words</b> ('organisation' and 'organ', 'university' "
          "and 'universe'), <b>which is why lighter stemmers and plain "
          "lemmatisation are now generally preferred.</b>",
          "<b>Stopword removal.</b> <b>Once essential for space, and "
          "now mostly unnecessary</b> since compression handles the "
          "common terms efficiently — and <b>it breaks phrase "
          "queries like 'to be or not to be'</b> entirely, which is a "
          "memorable and genuine failure.",
          "<b>And the index must apply the same transformations to "
          "queries as to documents</b> — <b>a mismatch here is a "
          "silent and complete failure for the affected terms</b>, not a "
          "degradation. <b>The query-document symmetry requirement is "
          "the one that causes real bugs:</b> a stemmer applied at index "
          "time and forgotten at query time makes an entire class of term "
          "unfindable, with no error anywhere."]),

  ("break",),
  ("h1", "3 &nbsp; Compression"),
  ("code", """GAP ENCODING
    store differences rather than absolute ids:
        17, 41, 42, 93  ->  17, 24, 1, 51
    Frequent terms give small gaps, which is exactly
    where the space is being spent.

VARIABLE-BYTE
    one byte per 7 bits of value, with a continuation
    flag in the top bit. Simple, fast to decode, and
    byte-aligned.

BIT-PACKED AND SIMD-FRIENDLY SCHEMES
    pack a block of gaps at whatever width the
    largest one in the block needs. Much faster to
    decode than bit-by-bit codes, which is why they
    displaced Elias gamma and Golomb coding in
    practice despite compressing slightly worse.

AND THE REASON IT BUYS SPEED
    the index is read from disk or from memory, and
    decoding is cheaper than the I/O it saves. A
    smaller index is a FASTER index, which is the
    counterintuitive part."""),
  ("p", "<b>A smaller index is a faster index</b> — <b>because "
        "the bottleneck is data movement rather than decoding</b>, which "
        "is <b>CSCE 676 Module 01 &sect;2's cost model arriving in "
        "this course</b>. <b>The speed argument is why compression is "
        "not optional</b>: it is not a space-saving concession but a "
        "performance technique, and the schemes that won are the ones "
        "optimised for decode throughput rather than for compression "
        "ratio."),
  ("callout", "And skip pointers make intersection sublinear",
   ["<b>Store occasional forward pointers into a postings list</b> "
    "— so that <b>intersecting a short list against a long one can "
    "skip over the long list's irrelevant stretches</b> rather than "
    "walking them.",
    "<b>Which matters because query term frequencies are wildly "
    "uneven:</b> <b>intersecting a rare term's hundred postings against "
    "a common term's ten million is the normal case</b> rather than the "
    "exception, and the naive merge walks all ten million.",
    "<b>And the right skip interval is approximately the square root "
    "of the list length</b>, which balances the pointer storage overhead "
    "against the skipping gain — a classic square-root trade.",
    "<b>But skips interact badly with compression</b> — <b>you "
    "cannot skip into the middle of a gap-encoded block without decoding "
    "it from the start</b>, since each gap depends on the previous "
    "value — <b>which is exactly why real formats store skips at "
    "block boundaries</b> and why the block size is a tuning "
    "parameter."]),

  ("h1", "4 &nbsp; Building it"),
  ("ul", ["<b>In memory</b>, for a collection that fits — a "
          "dictionary of lists, accumulated, then sorted and written "
          "out. Simple, and the right answer more often than people "
          "assume (CSCE 676 Module 10 &sect;3).",
          "<b>Blocked sort-based indexing</b>, for a collection that "
          "does not fit: <b>index blocks that do fit, write each sorted "
          "block to disk, then merge the sorted runs</b> — <b>which "
          "is external merge sort</b>, and the merge is a single "
          "sequential pass.",
          "<b>Single-pass in-memory indexing</b>, which avoids needing "
          "a global term-to-id mapping by <b>writing a separate "
          "dictionary per block and merging the dictionaries too</b> "
          "— which matters when the vocabulary itself is too large to "
          "hold.",
          "<b>Distributed indexing</b>, which is a MapReduce "
          "partitioned by term (CSCE 676 Module 10) — <b>and "
          "the shuffle is the cost</b>, with the heavy-tailed term "
          "distribution producing exactly the skew that module "
          "warns about.",
          "<b>And incremental updates</b>, usually handled by "
          "<b>keeping a small in-memory index for recent changes and "
          "merging it into the main index periodically</b> — because "
          "<b>rebuilding a postings list is cheaper than updating a "
          "compressed one in place</b>. <b>The merge-rather-than-update "
          "conclusion recurs in storage engines generally</b>: a "
          "compressed sorted structure is cheap to read and expensive to "
          "modify, so you write a new one and merge."]),
  ("callout", "And what to measure about an index",
   ["<b>Size against the raw collection</b>, with <b>the compression "
    "attributed per technique</b> rather than reported as a single total "
    "— which is <b>Project 1's requirement</b> and is what "
    "demonstrates that you know which technique bought what.",
    "<b>Build time, and whether it parallelises</b> — since <b>a "
    "reindex is an operation you will perform repeatedly</b>, after every "
    "schema change and every preprocessing fix, and its cost determines "
    "how willing you are to experiment.",
    "<b>Query latency at the median and the 95th percentile</b>, "
    "because <b>the tail is what users actually experience as 'the "
    "search is slow'</b> — and a good median with a bad tail is the "
    "common and misleading shape (Module 04 &sect;4).",
    "<b>And the postings list length distribution</b>, which is "
    "heavy-tailed (CSCE 676 Module 07 &sect;1) and <b>determines "
    "which optimisations are worth implementing</b> — skips matter "
    "only because of that tail, and knowing its shape tells you how "
    "much."]),
 ],
 "resources": [
   ("Manning, Raghavan & Sch&uuml;tze, chapters 1 through 5 (free)",
    "https://nlp.stanford.edu/IR-book/",
    "<b>The whole module</b>, with the construction algorithms and the "
    "compression codes derived."),
   ("Zobel & Moffat &mdash; Inverted files for text search engines "
    "(free)",
    "https://dl.acm.org/doi/10.1145/1132956.1132959",
    "<b>&sect;3 and &sect;4 exhaustively</b> — the reference, with "
    "the measurements behind every recommendation."),
   ("Lemire & Boytsov &mdash; Decoding billions of integers per second "
    "(free)",
    "https://arxiv.org/abs/1209.2137",
    "<b>&sect;3's modern schemes</b> — why decode throughput beat "
    "compression ratio, with the numbers."),
   ("The Lucene index format documentation (free)",
    "https://lucene.apache.org/core/documentation.html",
    "<b>&sect;1 through &sect;4 as actually implemented</b> — read "
    "the postings format description against this module."),
 ],
 "exercises": [
   "<b>Build an inverted index</b> with frequencies, on a collection of "
   "at least 100,000 documents.",
   "<b>Add positions</b> and measure the size increase.",
   "<b>Apply case folding, stemming, and stopword removal</b> in turn, "
   "and measure the index size and the vocabulary after each.",
   "<b>Deliberately apply a stemmer at index time only</b> and find the "
   "queries that now fail.",
   "<b>Implement gap encoding</b> and measure the saving.",
   "<b>Implement variable-byte</b> and measure both size and decode "
   "speed.",
   "<b>Add skip pointers</b> at √n intervals and measure "
   "intersection speed on a rare-plus-common term pair.",
   "<b>Implement blocked sort-based indexing</b> on a collection larger "
   "than your memory.",
   "<b>Attribute your total compression</b> to each technique "
   "separately.",
   "<b>Report your query latency</b> at the median and the 95th "
   "percentile.",
 ],
 "selfcheck": [
   "What does an inverted index hold, and what are the storage "
   "choices?",
   "Why sorted by document id?",
   "What trade does the index make, and why is it the right one?",
   "Name five preprocessing decisions and the cost of each.",
   "Which preprocessing mistake is a silent failure?",
   "Name three compression techniques and why gap encoding works.",
   "Why does compression buy speed?",
   "What do skip pointers achieve, and what is the right interval?",
   "Why do skips conflict with compression?",
   "Name four construction methods and the merge-not-update "
   "conclusion.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Ranking",
 "subtitle": "Scoring functions, derived rather than asserted.",
 "question": "Why these formulas and not others?",
 "outcomes": [
     "Explain the vector space model and its weighting.",
     "Derive the components of TF-IDF from stated "
     "intuitions.",
     "Explain BM25 and what each parameter controls.",
     "Explain the language modelling approach.",
     "Tune and compare scoring functions.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Three intuitions",
   "blurb": "From which the formulas follow."},

  {"t": "callout", "title": "Term frequency, document frequency, and length: three intuitions that determine the formula",
   "kind": "Where the scoring functions come from",
   "body": ["<b>A document mentioning the term more is more likely "
            "relevant</b> — <b>but not proportionally</b>, since the "
            "tenth mention adds far less than the second. So "
            "<i>saturating</i> term frequency.",
            "<b>A term occurring in few documents is more "
            "discriminating</b> — 'the' tells you nothing and "
            "'parvovirus' tells you a great deal. So <i>inverse</i> "
            "document frequency.",
            "<b>And a long document matches more terms by "
            "chance</b> — so some normalisation by length, though "
            "<b>a long document may also genuinely cover more</b>, which "
            "is why the normalisation is partial.",
            "<b>Every scoring function in this module is a different "
            "way of combining those three</b> — which is why they "
            "perform similarly and why understanding the intuitions "
            "matters more than memorising the formulas."]},

  {"t": "eq", "kicker": "TF-IDF", "title": "The classical weighting",
   "eqs": [
     ("w(t,d) = (1 + log tf(t,d)) · log(N / df(t))",
      "Log-damped term frequency times inverse document frequency. "
      "The log on tf is the saturation."),
     ("score(q,d) = Σ over t in q of w(t,d) · w(t,q) / (|d| · |q|)",
      "Cosine similarity in the vector space, which is where the "
      "length normalisation comes from."),
     ("the cosine normalisation over-penalises long documents",
      "Which is the specific limitation BM25 addresses with a "
      "tunable normalisation (Part 3)."),
   ],
   "caption": "<b>The cosine's length normalisation is too "
              "aggressive</b> — which is the measured defect that "
              "motivated the next generation.",
   "note": "Naming the specific defect makes BM25's design "
           "intelligible."},

  {"t": "section", "label": "Part 2", "title": "The vector space",
   "blurb": "And what the geometry does and does not justify."},

  {"t": "bullets", "kicker": "Vector space", "title": "What the model gives, and its limits",
   "items": [
     "<b>Documents and queries as vectors over the "
     "vocabulary</b>, with cosine similarity as the score — which "
     "is intuitive and gives a total ordering.",
     "",
     "<b>And it handles partial matches naturally</b>, which "
     "Boolean retrieval cannot — a document with three of four "
     "query terms gets a score rather than a rejection.",
     "",
     "<b>But the geometry is a convenience rather than a "
     "justification.</b> <b>Nothing says relevance is a cosine</b>, and "
     "the model has no probabilistic interpretation.",
     "",
     "<b>And it assumes term independence</b>, which is plainly "
     "false — though <b>it is false in a way that happens not to "
     "hurt much</b>, which is worth noting honestly.",
     "",
     "<b>So it works well and explains nothing</b> — which is "
     "exactly what Part 3's probabilistic derivation "
     "fixes.",
   ],
   "footnote": "<b>'Works well and explains nothing' is a fair summary "
               "of the vector space model</b> — and the dissatisfaction "
               "with that is what produced the probabilistic "
               "models."},

  {"t": "section", "label": "Part 3", "title": "BM25",
   "blurb": "The default, and still hard to beat."},

  {"t": "eq", "kicker": "BM25", "title": "The formula, and what each part does",
   "eqs": [
     ("score = Σ IDF(t) · tf·(k₁+1) / (tf + k₁·(1 − b + b·|d|/avgdl))",
      "Saturating term frequency, inverse document frequency, and "
      "tunable length normalisation."),
     ("k₁ controls the saturation rate",
      "Low k₁ means tf saturates fast; k₁ → ∞ makes it linear. "
      "Typically 1.2 to 2.0."),
     ("b controls the length normalisation",
      "b = 0 is none at all; b = 1 is full. Typically 0.75, and it "
      "is worth tuning per collection."),
   ],
   "caption": "<b>The tunable b is the advance over cosine "
              "normalisation</b> — it lets the collection decide how "
              "much length should matter.",
   "note": "Emphasise that b and k1 should be tuned, not defaulted."},

  {"t": "callout", "title": "BM25 is a strong baseline that a decade of neural work struggled to beat",
   "kind": "Why it is the baseline to measure against",
   "body": ["<b>It is cheap, needs no training data, and transfers "
            "across collections without adaptation</b> — three "
            "properties no learned method has.",
            "<b>And the replication record is "
            "pointed:</b> <b>several waves of reported neural retrieval "
            "improvements did not survive comparison against a properly "
            "tuned BM25</b>, which is "
            "CSCE 676 Module 13's problem in this "
            "field.",
            "<b>The operative word is 'properly tuned':</b> <b>an "
            "untuned BM25 with default parameters is a weak baseline, and "
            "comparisons against it are not informative.</b>",
            "<b>So tune it, report its parameters, and treat beating "
            "it as the bar</b> — which is "
            "Module 05 §4's requirement and "
            "Project 2's."]},

  {"t": "section", "label": "Part 4", "title": "Language models",
   "blurb": "A different derivation, similar performance."},

  {"t": "callout", "title": "Query likelihood: rank documents by the probability their language model generates the query",
   "kind": "The probabilistic alternative",
   "body": ["<b>Estimate a language model from each document, then "
            "score by P(query | document model)</b> — which is a "
            "clean derivation from a stated generative "
            "assumption.",
            "<b>And smoothing is where the work happens.</b> <b>An "
            "unsmoothed document model gives probability zero to any "
            "unseen query term</b>, so the collection model is mixed "
            "in — Dirichlet or Jelinek-Mercer.",
            "<b>Which is the same role IDF plays</b>: <b>the "
            "smoothing weight makes common terms contribute "
            "less</b>, because they are well explained by the collection "
            "model.",
            "<b>So two independent derivations arrive at similar "
            "behaviour</b> — <b>which is evidence that the three "
            "intuitions of Part 1 are the content, and the "
            "formula is the packaging.</b>"]},

  {"t": "bullets", "kicker": "Practice", "title": "What to actually do",
   "items": [
     "<b>Use BM25, tuned on your collection</b>, as the baseline "
     "and frequently as the system.",
     "",
     "<b>Score fields separately and combine</b> — a term in "
     "the title means more than in the body, and BM25F is the standard "
     "extension.",
     "",
     "<b>Tune k₁ and b by grid search</b> on a held-out query "
     "set, and <b>report the values</b>, because an untuned "
     "comparison is uninformative.",
     "",
     "<b>And compare against query likelihood</b> once, to see "
     "how similar they are — which calibrates your expectations "
     "about scoring function choice.",
     "",
     "<b>Then spend your remaining effort on Modules 06 and "
     "07</b>, because the scoring function is not where the "
     "headroom is.",
   ],
   "footnote": "<b>The scoring function is not where the headroom "
               "is</b> — which is a useful thing to establish early, "
               "by measuring rather than by assumption."},
 ],
 "takeaways": [
   "Three intuitions — saturating term frequency, inverse document "
   "frequency, and partial length normalisation — determine every "
   "formula in the module.",
   "The cosine's length normalisation is too aggressive, which is the "
   "measured defect BM25's tunable b addresses.",
   "The vector space model works well and explains nothing, which is what "
   "the probabilistic derivations fix.",
   "BM25's k₁ controls saturation and b controls length "
   "normalisation, and both should be tuned per collection.",
   "An untuned BM25 is a weak baseline, and several waves of neural "
   "retrieval results did not survive a properly tuned one.",
   "Two independent derivations arrive at similar behaviour, which is "
   "evidence the intuitions are the content and the formula is the "
   "packaging.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Three intuitions"),
  ("callout", "Term frequency, document frequency, and length: three "
              "intuitions that determine the formula",
   ["<b>A document mentioning the query term more often is more likely "
    "to be relevant</b> — <b>but not proportionally so</b>, since "
    "the tenth mention adds far less evidence than the second did. "
    "<b>So the term frequency contribution must saturate.</b>",
    "<b>A term occurring in few documents is more discriminating</b> "
    "— 'the' tells you essentially nothing about which document you "
    "want and 'parvovirus' tells you a great deal. <b>So the weight "
    "should be inverse in document frequency.</b>",
    "<b>And a long document matches more query terms by chance "
    "alone</b> — so there must be some normalisation by "
    "length — <b>though a long document may also genuinely cover "
    "more material</b>, <b>which is why the normalisation should be "
    "partial rather than complete</b> (&sect;3's b parameter).",
    "<b>Every scoring function in this module is a different way of "
    "combining those three intuitions</b> — <b>which is why they "
    "all perform similarly, and why understanding the intuitions matters "
    "considerably more than memorising any particular formula.</b>"]),
  ("eq", "w(t,d) = (1 + log tf(t,d)) &middot; log(N / df(t))"),
  ("ul", ["<b>Log-damped term frequency times inverse document "
          "frequency.</b> <b>The logarithm on tf is the saturation</b> "
          "from &sect;1's first intuition, and the logarithm on N/df "
          "keeps the IDF from dominating entirely.",
          "<b>The document score is the cosine similarity between the "
          "query and document vectors</b> — which is where the "
          "length normalisation enters, as the division by the vector "
          "norms.",
          "<b>And the cosine normalisation over-penalises long "
          "documents</b> — <b>which is the specific, measured "
          "limitation that BM25 addresses with a tunable normalisation</b> "
          "(&sect;3).",
          "<b>Naming the specific defect makes BM25's design "
          "intelligible</b> rather than arbitrary: it is not a different "
          "idea but a correction to one parameter of this one, arrived at "
          "by measurement."]),

  ("h1", "2 &nbsp; The vector space model"),
  ("ul", ["<b>Documents and queries as vectors over the "
          "vocabulary</b>, with cosine similarity as the relevance score "
          "— which is intuitive, cheap, and gives a total ordering "
          "over the collection.",
          "<b>And it handles partial matches naturally</b>, which "
          "Boolean retrieval cannot — <b>a document containing three "
          "of four query terms receives a score rather than a "
          "rejection</b>, which was the advance that made ranked "
          "retrieval possible at all.",
          "<b>But the geometry is a convenience rather than a "
          "justification.</b> <b>Nothing says relevance is a cosine</b>, "
          "and <b>the model has no probabilistic interpretation</b> "
          "— so there is no principled way to extend it or to "
          "incorporate other evidence.",
          "<b>And it assumes term independence</b>, which is plainly "
          "false of language (CSCE 638 Module 01 &sect;1's "
          "compositionality) — <b>though it is false in a way that "
          "happens not to hurt retrieval much</b>, which is worth noting "
          "honestly rather than pretending the assumption holds.",
          "<b>So it works well and explains nothing</b> — which "
          "<b>is a fair summary</b>, and <b>the dissatisfaction with "
          "that is exactly what produced the probabilistic models</b> of "
          "&sect;3 and &sect;4. The field's progress here came from "
          "wanting a derivation rather than from wanting better "
          "numbers."]),

  ("break",),
  ("h1", "3 &nbsp; BM25"),
  ("eq", "score = &Sigma; IDF(t) &middot; tf&middot;(k<sub>1</sub>+1) / "
         "(tf + k<sub>1</sub>&middot;(1 &minus; b + b&middot;|d|/avgdl))"),
  ("ul", ["<b>Saturating term frequency, inverse document frequency, "
          "and a tunable length normalisation</b> — &sect;1's three "
          "intuitions, each with an explicit parameter.",
          "<b>k<sub>1</sub> controls the saturation rate.</b> <b>A low "
          "k<sub>1</sub> makes the term frequency contribution saturate "
          "quickly; k<sub>1</sub> &rarr; &infin; makes it linear.</b> "
          "Typically between 1.2 and 2.0.",
          "<b>b controls the length normalisation.</b> <b>b = 0 "
          "applies none at all; b = 1 applies it fully.</b> Typically "
          "around 0.75, <b>and it is worth tuning per collection</b> "
          "because the right amount depends on whether long documents in "
          "your collection genuinely cover more.",
          "<b>The tunable b is the advance over the cosine's fixed "
          "normalisation</b> — <b>it lets the collection decide how "
          "much document length should matter</b>, rather than imposing a "
          "single answer. <b>Both parameters should be tuned rather "
          "than defaulted</b>, and the tuning is a grid search over a "
          "held-out query set."]),
  ("callout", "BM25 is a strong baseline that a decade of neural work "
              "struggled to beat",
   ["<b>It is cheap to compute, requires no training data at all, and "
    "transfers across collections and domains without any "
    "adaptation</b> — <b>three properties that no learned method "
    "has</b>, and which make it the sensible default for a new "
    "collection.",
    "<b>And the replication record is pointed:</b> <b>several waves of "
    "reported neural retrieval improvements did not survive comparison "
    "against a properly tuned BM25</b>, particularly in the zero-shot "
    "and out-of-domain settings — <b>which is CSCE 676 "
    "Module 13's baseline problem arriving in this field</b> and is "
    "documented in the BEIR results.",
    "<b>The operative phrase is 'properly tuned':</b> <b>a BM25 run "
    "with library default parameters on a collection it was not tuned "
    "for is a weak baseline, and comparisons against it are not "
    "informative</b> — which is how a good deal of the overstated "
    "literature was produced.",
    "<b>So tune it, report its parameters, and treat beating it as the "
    "bar</b> — which is <b>Module 05 &sect;4's requirement and "
    "Project 2's third criterion.</b>"]),

  ("h1", "4 &nbsp; Language models, and what to do"),
  ("callout", "Query likelihood: rank documents by the probability their "
              "language model generates the query",
   ["<b>Estimate a language model from each document, then score each "
    "document by P(query | that document's model)</b> — which is a "
    "clean derivation from an explicitly stated generative assumption, "
    "and that is the point: the formula follows rather than being "
    "asserted.",
    "<b>And the smoothing is where all the work happens.</b> <b>An "
    "unsmoothed document model assigns probability zero to any query term "
    "the document does not contain</b>, which makes the whole score "
    "zero — so <b>the collection-wide model is mixed in</b>, by "
    "Dirichlet smoothing or Jelinek&ndash;Mercer interpolation.",
    "<b>Which turns out to play exactly the role IDF plays:</b> <b>the "
    "smoothing makes common terms contribute less to the score, because "
    "they are already well explained by the collection model</b> and "
    "therefore carry little document-specific evidence. <b>IDF emerges "
    "from the smoothing rather than being postulated</b>, which is the "
    "satisfying part of this derivation.",
    "<b>So two independent derivations arrive at similar "
    "behaviour</b> — <b>which is evidence that &sect;1's three "
    "intuitions are the actual content, and the formula is the "
    "packaging</b>, and it is why the practical advice in this module is "
    "to pick one and move on."]),
  ("ul", ["<b>Use BM25, tuned on your own collection</b>, as the "
          "baseline and frequently as the production system — it is "
          "still what many deployed search systems run.",
          "<b>Score fields separately and combine them</b> — a "
          "term appearing in the title means considerably more than the "
          "same term in the body, and <b>BM25F is the standard extension "
          "that handles this</b> without simply concatenating the fields "
          "(which breaks the length normalisation).",
          "<b>Tune k<sub>1</sub> and b by grid search</b> on a "
          "held-out query set, and <b>report the values you used</b>, "
          "because <b>an untuned comparison is uninformative</b> and a "
          "reader cannot assess it.",
          "<b>And compare against query likelihood once</b>, to see "
          "for yourself how similar they are — <b>which calibrates "
          "your expectations about how much the scoring function choice "
          "matters</b> before you spend time on it.",
          "<b>Then spend your remaining effort on Modules 06 and "
          "07</b>, because <b>the scoring function is not where the "
          "headroom is</b> — and <b>that is a useful thing to "
          "establish early, by measuring rather than by assumption</b>, "
          "which is what the comparison above is for."]),
 ],
 "resources": [
   ("Manning, Raghavan & Sch&uuml;tze, chapters 6, 11, and 12 (free)",
    "https://nlp.stanford.edu/IR-book/",
    "<b>&sect;1 through &sect;4</b>, with the probabilistic derivations "
    "done carefully."),
   ("Robertson & Zaragoza &mdash; The Probabilistic Relevance "
    "Framework (free)",
    "https://www.nowpublishers.com/article/Details/INR-019",
    "<b>&sect;3 in the original</b>, by its authors — including "
    "where BM25 came from and what it approximates."),
   ("Zhai & Lafferty &mdash; A study of smoothing methods (free)",
    "https://dl.acm.org/doi/10.1145/984321.984322",
    "<b>&sect;4's smoothing, measured</b> — and the IDF-emerges-from-"
    "smoothing argument."),
   ("Thakur et al. &mdash; BEIR (free)",
    "https://arxiv.org/abs/2104.08663",
    "<b>&sect;3's callout, with the numbers</b> — BM25 against neural "
    "methods across eighteen zero-shot collections."),
 ],
 "exercises": [
   "<b>State the three intuitions</b> and say which parameter of BM25 "
   "corresponds to each.",
   "<b>Implement TF-IDF with cosine</b> and inspect the top ten for five "
   "queries.",
   "<b>Find a case where the cosine over-penalises a long "
   "document.</b>",
   "<b>Implement BM25 from the formula</b> and verify against a "
   "reference implementation.",
   "<b>Sweep k₁ from 0.5 to 5</b> and plot the effect on your "
   "metric.",
   "<b>Sweep b from 0 to 1</b> and explain the shape of the curve.",
   "<b>Compare default and tuned BM25</b> and report the gap.",
   "<b>Implement query likelihood with Dirichlet smoothing</b> and "
   "compare against BM25.",
   "<b>Show that the smoothing weight behaves like IDF</b> on a common "
   "and a rare term.",
   "<b>Implement BM25F over title and body</b> and measure the "
   "improvement.",
 ],
 "selfcheck": [
   "State the three intuitions and why each is as it is.",
   "Why must term frequency saturate, and why is length normalisation "
   "partial?",
   "Give TF-IDF and say where the length normalisation comes from.",
   "What is the cosine's specific defect?",
   "What does the vector space model give, and what are its three "
   "limits?",
   "Give BM25 and say what k₁ and b each control.",
   "Why is BM25 a strong baseline, and what does 'properly tuned' "
   "mean?",
   "Describe query likelihood and why smoothing is necessary.",
   "How does IDF emerge from the smoothing?",
   "What does the agreement of two derivations suggest?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Query Processing",
 "subtitle": "Making good ranking affordable.",
 "question": "How do you get the top ten without scoring everything?",
 "outcomes": [
     "Explain term-at-a-time and document-at-a-time "
     "processing.",
     "Explain the safe early-termination strategies.",
     "Explain the unsafe ones and what they cost.",
     "Explain caching and index partitioning.",
     "Measure and meet a latency budget.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two orders",
   "blurb": "And they have different memory profiles."},

  {"t": "code", "kicker": "Orders", "title": "Term-at-a-time and document-at-a-time",
   "lang": "text", "code": """
  TERM-AT-A-TIME
      process one query term's whole postings list,
      accumulating partial scores in a hash table of
      candidate documents, then the next term.
      Memory: one accumulator per candidate document,
      which can be most of the collection.

  DOCUMENT-AT-A-TIME
      advance all the query terms' postings lists
      together in document order, completing each
      document's score before moving on.
      Memory: one heap of size k. Which is why it
      won.

  AND DOCUMENT-AT-A-TIME ENABLES EARLY TERMINATION
      because a document's score is final when you
      leave it, so you can compare against the
      current k-th best and stop when no remaining
      document could beat it (Part 2).

  TERM-AT-A-TIME CANNOT DO THIS, since no score is
  final until every term has been processed.
""",
   "caption": "<b>Document-at-a-time's bounded memory and its support "
              "for early termination are the same property</b> — "
              "scores complete as you go.",
   "note": "Connecting the two advantages to one cause is the "
           "insight."},

  {"t": "section", "label": "Part 2", "title": "Safe early termination",
   "blurb": "Identical results, less work."},

  {"t": "callout", "title": "WAND skips documents that provably cannot enter the top k",
   "kind": "The main technique, and it is exact",
   "body": ["<b>Precompute, per term, the maximum score it can "
            "contribute to any document</b> — its upper bound, which "
            "depends only on the term's IDF and the highest term "
            "frequency in its postings.",
            "<b>Then at each step, sum the upper bounds of the terms "
            "whose lists are positioned at or before the candidate "
            "document.</b> <b>If that sum is below the current k-th best "
            "score, no document there can qualify</b> — so skip "
            "ahead.",
            "<b>Which is <i>safe</i>: the top k is identical to "
            "exhaustive scoring</b>, because you only skipped documents "
            "that were provably ineligible.",
            "<b>And block-max variants tighten the bounds</b> by "
            "storing a maximum per postings block rather than per "
            "term — <b>a much tighter bound, and much more "
            "skipping.</b>"]},

  {"t": "bullets", "kicker": "Safety", "title": "Why safety matters, and how to verify it",
   "items": [
     "<b>A safe optimisation returns exactly the same top k</b>, "
     "so it can be deployed without re-evaluating "
     "quality.",
     "",
     "<b>And it can be verified mechanically:</b> <b>run both and "
     "compare the result lists</b> — which is "
     "Project 1's requirement and takes "
     "minutes.",
     "",
     "<b>An unsafe optimisation changes the results</b>, so it "
     "requires a new evaluation (Module 05) — and <b>a "
     "difference in a metric could be the optimisation or could be "
     "noise.</b>",
     "",
     "<b>Which makes safety a property worth paying for</b>, "
     "because it decouples performance work from quality "
     "work.",
     "",
     "<b>And an unverified 'safe' optimisation is a bug "
     "waiting</b> — the comparison is the only thing that "
     "establishes it.",
   ],
   "footnote": "<b>Safety decouples performance work from quality "
               "work</b>, which is worth a great deal "
               "organisationally — the team can optimise without "
               "re-running the evaluation."},

  {"t": "section", "label": "Part 3", "title": "Unsafe optimisations",
   "blurb": "Which are fine, if you measure them."},

  {"t": "bullets", "kicker": "Unsafe", "title": "The approximations, and what each costs",
   "items": [
     "<b>Static index pruning</b> — remove postings that "
     "could rarely matter, which shrinks the index permanently and may "
     "lose a rare but correct answer.",
     "",
     "<b>Tiering</b> — search a small high-quality tier "
     "first and fall back only if too few results, which works well "
     "and <b>systematically disadvantages the lower tier's "
     "documents</b> (Module 12).",
     "",
     "<b>Champion lists</b> — keep only each term's top "
     "scoring documents, and score only those.",
     "",
     "<b>A document-count cutoff</b> — stop after examining n "
     "documents, which bounds latency and is sensitive to the index "
     "order.",
     "",
     "<b>And all of them are legitimate</b> — <b>provided the "
     "quality cost is measured rather than assumed negligible.</b>",
   ],
   "footnote": "<b>Unsafe does not mean wrong</b> — it means the "
               "quality effect has to be measured, which is a "
               "requirement rather than an objection."},

  {"t": "section", "label": "Part 4", "title": "Systems",
   "blurb": "Caching, partitioning, and the latency tail."},

  {"t": "callout", "title": "Query distributions are heavy-tailed, which makes caching extremely effective",
   "kind": "The system-level win",
   "body": ["<b>A small number of queries account for a large "
            "fraction of traffic</b> — so <b>a result cache with a "
            "modest size serves a substantial share of requests at "
            "almost no cost.</b>",
            "<b>And there are two caches worth having:</b> <b>a "
            "result cache for whole queries, and a postings cache for "
            "frequently-accessed lists</b>, which helps the tail of "
            "unique queries.",
            "<b>With the invalidation question being the hard "
            "part:</b> <b>a cached result is stale as soon as the index "
            "changes</b>, and the right staleness depends on the "
            "application.",
            "<b>Which is the same heavy-tail-plus-caching pattern as "
            "everywhere else in systems</b> — and here the tail is in "
            "the query distribution rather than in the "
            "data."]},

  {"t": "bullets", "kicker": "Partitioning", "title": "And the two ways to split an index",
   "items": [
     "<b>Document partitioning:</b> <b>each machine holds a "
     "subset of documents and runs the whole query</b>, with results "
     "merged. <b>Simple, balanced, and the standard "
     "choice.</b>",
     "",
     "<b>Term partitioning:</b> <b>each machine holds a subset of "
     "terms' complete postings</b>, so a query touches only the "
     "relevant machines — less total work, and <b>badly "
     "imbalanced</b> by the term distribution.",
     "",
     "<b>So document partitioning wins in practice</b>, because "
     "<b>balance matters more than total work</b> when latency is set "
     "by the slowest machine.",
     "",
     "<b>Which is CSCE 676 §10 §2's skew "
     "argument</b>, arriving with a concrete design "
     "conclusion.",
     "",
     "<b>And it makes the tail latency the thing to "
     "measure</b>, since the query waits for every partition.",
   ],
   "footnote": "<b>With n partitions, the query latency is the maximum "
               "of n samples</b> — so the more you partition, the "
               "worse the tail, which is the fundamental tension in "
               "this design."},

  {"t": "callout", "title": "And the latency budget is a design input",
   "kind": "Closing",
   "body": ["<b>Decide the budget first</b>, because it determines "
            "the architecture — <b>how many candidates you can "
            "retrieve, how expensive a reranker you can afford</b> "
            "(Module 06 §4), and whether a neural model is "
            "usable at all.",
            "<b>Measure the distribution, not the mean.</b> <b>The "
            "95th and 99th percentiles are what users "
            "experience</b>, and the mean hides them.",
            "<b>And budget per stage:</b> <b>retrieval, reranking, "
            "and presentation each get a share</b>, which makes the "
            "trade-offs explicit rather than discovered.",
            "<b>Which is the module's practical conclusion:</b> <b>a "
            "ranking function you cannot evaluate in time is not a "
            "ranking function you have</b>, so the budget constrains the "
            "quality work rather than following it."]},
 ],
 "takeaways": [
   "Document-at-a-time processing needs only a heap of size k and enables "
   "early termination, and both follow from scores completing as you go.",
   "WAND skips documents that provably cannot enter the top k, and it is "
   "safe — the result is identical to exhaustive scoring.",
   "Safety decouples performance work from quality work, and it is "
   "verified by comparing result lists.",
   "Unsafe does not mean wrong; it means the quality cost has to be "
   "measured rather than assumed negligible.",
   "Query distributions are heavy-tailed, which makes a modest result "
   "cache serve a large share of traffic.",
   "With n partitions the latency is the maximum of n samples, so more "
   "partitioning means a worse tail.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two orders of processing"),
  ("code", """TERM-AT-A-TIME
    process one query term's entire postings list,
    accumulating partial scores in a hash table of
    candidate documents, then move to the next term.
    Memory: one accumulator per candidate document,
    which can be a large fraction of the collection.

DOCUMENT-AT-A-TIME
    advance all the query terms' postings lists
    together in document order, completing each
    document's score before moving on.
    Memory: one heap of size k. Which is why it won.

AND DOCUMENT-AT-A-TIME ENABLES EARLY TERMINATION
    because a document's score is final when you leave
    it, so you can compare against the current k-th
    best and stop when no remaining document could
    possibly beat it (section 2).

TERM-AT-A-TIME CANNOT DO THIS, since no document's
score is final until every query term has been
processed."""),
  ("p", "<b>Document-at-a-time's bounded memory and its support for "
        "early termination are the same property</b> — <b>scores "
        "complete as you go</b>, which is what both lets you discard a "
        "document after scoring it and lets you reason about whether "
        "remaining documents could qualify. <b>Connecting the two "
        "advantages to one cause is the insight</b>, and it explains why "
        "the choice was not a close one once collections grew."),

  ("h1", "2 &nbsp; Safe early termination"),
  ("callout", "WAND skips documents that provably cannot enter the top k",
   ["<b>Precompute, for each term, the maximum score it could "
    "contribute to any document</b> — its upper bound, which depends "
    "only on the term's IDF and the largest term frequency anywhere in "
    "its postings list, and is computed once at index time.",
    "<b>Then at each step, sum the upper bounds of the terms whose "
    "postings lists are currently positioned at or before the candidate "
    "document.</b> <b>If that sum is below the current k-th best score, "
    "then no document at that position can possibly qualify</b> — so "
    "skip the lists forward past it.",
    "<b>Which makes it <i>safe</i>: the resulting top k is identical "
    "to what exhaustive scoring would produce</b>, because every "
    "document skipped was provably ineligible rather than merely "
    "unpromising.",
    "<b>And block-max variants tighten the bounds considerably</b> by "
    "<b>storing a maximum score per postings block rather than one per "
    "term</b> — <b>a much tighter bound, and therefore much more "
    "skipping</b>, which is what current implementations use."]),
  ("ul", ["<b>A safe optimisation returns exactly the same top k</b>, "
          "<b>so it can be deployed without re-evaluating the system's "
          "quality at all</b> — which is its organisational value as "
          "much as its technical one.",
          "<b>And it can be verified mechanically:</b> <b>run both the "
          "optimised and the exhaustive version and compare the result "
          "lists</b> — which is <b>Project 1's requirement</b> and "
          "takes minutes to set up.",
          "<b>An unsafe optimisation changes the results</b>, so it "
          "requires a fresh evaluation (Module 05) — and <b>a "
          "difference in the metric could be the optimisation's effect or "
          "could be noise</b>, which makes the assessment much "
          "harder.",
          "<b>Which makes safety a property worth paying for</b>, "
          "because <b>it decouples performance work from quality "
          "work</b> — the team can optimise freely without "
          "re-running the evaluation, which changes how quickly they can "
          "iterate.",
          "<b>And an unverified 'safe' optimisation is a bug "
          "waiting</b> — the bound arithmetic is easy to get subtly "
          "wrong, <b>and the comparison against exhaustive scoring is the "
          "only thing that establishes correctness</b>, which is why "
          "Project 1 grades it."]),

  ("break",),
  ("h1", "3 &nbsp; Unsafe optimisations"),
  ("ul", ["<b>Static index pruning</b> — remove postings that "
          "could rarely contribute to a top-k result, which <b>shrinks "
          "the index permanently</b> and <b>may lose a rare but entirely "
          "correct answer</b> for an unusual query.",
          "<b>Tiering</b> — search a small, high-quality tier "
          "first and fall back to the full index only if too few results "
          "are found, <b>which works well in practice</b> and "
          "<b>systematically disadvantages the lower tier's "
          "documents</b> in a way that compounds over time "
          "(Module 12 &sect;2's exposure argument).",
          "<b>Champion lists</b> — keep only each term's "
          "highest-scoring documents in a separate structure, and score "
          "only those for most queries.",
          "<b>A document-count cutoff</b> — simply stop after "
          "examining n documents, <b>which bounds the latency "
          "directly</b> and is <b>sensitive to the order documents appear "
          "in the index</b>, which makes the quality effect depend on "
          "something arbitrary.",
          "<b>And all of them are legitimate techniques</b> — "
          "<b>provided the quality cost is measured rather than assumed "
          "negligible</b>. <b>Unsafe does not mean wrong</b>: it means "
          "<b>the quality effect has to be measured</b>, which is a "
          "requirement rather than an objection, and the measurement is "
          "Module 05's apparatus."]),

  ("h1", "4 &nbsp; Systems"),
  ("callout", "Query distributions are heavy-tailed, which makes caching "
              "extremely effective",
   ["<b>A small number of distinct queries account for a large "
    "fraction of all traffic</b> — the same heavy tail as everywhere "
    "else in this semester — so <b>a result cache of quite modest "
    "size serves a substantial share of requests at almost no "
    "cost.</b>",
    "<b>And there are two caches worth having:</b> <b>a result cache "
    "keyed on the whole query, and a postings cache for "
    "frequently-accessed lists</b> — the second of which helps the "
    "long tail of unique queries, since even unique queries share common "
    "terms.",
    "<b>With the invalidation question being the genuinely hard "
    "part:</b> <b>a cached result is stale the moment the index "
    "changes</b>, and <b>the acceptable staleness depends entirely on "
    "the application</b> — a news search and a documentation search "
    "have very different answers.",
    "<b>Which is the same heavy-tail-plus-caching pattern as "
    "everywhere else in systems</b> — and here <b>the tail is in "
    "the query distribution rather than in the data</b>, which is worth "
    "noticing because it means the caching opportunity exists even when "
    "the collection is uniform."]),
  ("ul", ["<b>Document partitioning:</b> <b>each machine holds a "
          "subset of the documents and runs the complete query against "
          "its own shard</b>, with the results merged centrally. "
          "<b>Simple, naturally balanced, and the standard choice.</b>",
          "<b>Term partitioning:</b> <b>each machine holds the "
          "complete postings for a subset of terms</b>, so a query only "
          "touches the machines holding its terms — <b>less total "
          "work, and badly imbalanced</b> by the heavy-tailed term "
          "distribution, with the common terms' machines overwhelmed.",
          "<b>So document partitioning wins in practice</b>, because "
          "<b>balance matters more than total work when the latency is "
          "set by the slowest machine</b> — which is the whole "
          "argument.",
          "<b>Which is CSCE 676 Module 10 &sect;2's skew "
          "argument</b>, arriving here with a concrete and consequential "
          "design conclusion rather than as a general warning.",
          "<b>And it makes the tail latency the thing to measure</b>, "
          "since <b>the query cannot return until every partition has "
          "responded</b>. <b>With n partitions, the query latency is the "
          "maximum of n samples from the per-partition latency "
          "distribution</b> — so <b>the more you partition, the "
          "worse the tail gets</b>, which is the fundamental tension in "
          "this design and is why very large fan-outs need hedged "
          "requests."]),
  ("callout", "And the latency budget is a design input",
   ["<b>Decide the budget first</b>, because <b>it determines the "
    "architecture</b> — <b>how many candidates you can afford to "
    "retrieve, how expensive a reranker you can run over them</b> "
    "(Module 06 &sect;4), and <b>whether a neural model is usable at "
    "all</b> at your query volume.",
    "<b>Measure the distribution rather than the mean.</b> <b>The "
    "95th and 99th percentiles are what users experience as the system's "
    "speed</b>, and <b>the mean hides them entirely</b> — "
    "particularly with the partitioning fan-out above.",
    "<b>And budget per stage:</b> <b>retrieval, reranking, and "
    "presentation each receive an explicit share</b> — which makes "
    "the trade-offs visible and negotiable rather than discovered when "
    "something is too slow.",
    "<b>Which is the module's practical conclusion:</b> <b>a ranking "
    "function you cannot evaluate within the budget is not a ranking "
    "function you have</b> — <b>so the budget constrains the quality "
    "work rather than following it</b>, and that ordering is what "
    "Module 06 &sect;4's two-stage architecture exists to "
    "exploit."]),
 ],
 "resources": [
   ("Manning, Raghavan & Sch&uuml;tze, chapter 7 (free)",
    "https://nlp.stanford.edu/IR-book/",
    "<b>&sect;1 through &sect;3</b> — the processing orders and the "
    "inexact top-k strategies."),
   ("Broder et al. &mdash; Efficient query evaluation using a two-level "
    "retrieval process (free)",
    "https://dl.acm.org/doi/10.1145/956863.956944",
    "<b>&sect;2's WAND in the original</b> — short, and the bound "
    "argument is the whole paper."),
   ("Ding & Suel &mdash; Faster top-k document retrieval using "
    "block-max indexes (free)",
    "https://dl.acm.org/doi/10.1145/2009916.2010048",
    "<b>&sect;2's tightening</b> — block-max WAND, which is what "
    "current engines implement."),
   ("Dean & Barroso &mdash; The Tail at Scale (free)",
    "https://dl.acm.org/doi/10.1145/2408776.2408794",
    "<b>&sect;4's fan-out problem</b> — why partitioning worsens the "
    "tail, and what to do about it."),
 ],
 "exercises": [
   "<b>Implement both processing orders</b> and compare their peak "
   "memory.",
   "<b>Explain why term-at-a-time cannot terminate early.</b>",
   "<b>Compute per-term upper bounds</b> at index time.",
   "<b>Implement WAND</b> and measure the fraction of documents "
   "skipped.",
   "<b>Verify the top k matches exhaustive scoring exactly</b>, on a "
   "thousand queries.",
   "<b>Add block-max bounds</b> and remeasure the skipping.",
   "<b>Implement a document-count cutoff</b> and measure both the "
   "latency gain and the metric loss.",
   "<b>Measure your query distribution's skew</b> and compute the hit "
   "rate of a cache holding the top 10,000 queries.",
   "<b>Partition an index by document and by term</b>, and compare the "
   "load balance.",
   "<b>Report your latency at the median, 95th, and 99th "
   "percentiles.</b>",
 ],
 "selfcheck": [
   "Contrast the two processing orders on memory, and say why one "
   "won.",
   "Why does document-at-a-time enable early termination?",
   "Explain WAND's bound and why it is safe.",
   "What do block-max variants improve?",
   "Why does safety decouple performance from quality work?",
   "How do you verify a safe optimisation?",
   "Name four unsafe optimisations and what each costs.",
   "Why is caching so effective here, and what are the two caches?",
   "Contrast document and term partitioning, and say which wins and "
   "why.",
   "Why does partitioning worsen the latency tail?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Evaluation",
 "subtitle": "The course's centre: measuring a proxy for a judgement.",
 "question": "Is your system better, or is your test set different?",
 "outcomes": [
     "Explain the test collection methodology and its "
     "assumptions.",
     "Build relevance judgements and assess their "
     "reliability.",
     "Choose a metric from how results will be used.",
     "Explain what click data gives and what it biases.",
     "Run a comparison whose result means something.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The methodology",
   "blurb": "Collection, queries, judgements — and what each assumes."},

  {"t": "callout", "title": "A test collection is a collection, a query set, and relevance judgements — each with assumptions",
   "kind": "The apparatus, and where it is fragile",
   "body": ["<b>The collection must resemble the documents your system "
            "will face</b> — and a benchmark collection from a "
            "different domain measures transfer rather than "
            "quality.",
            "<b>The queries must come from real information "
            "needs</b> (Module 01 §4) — and <b>queries "
            "written from documents make the evaluation "
            "circular.</b>",
            "<b>The judgements assume relevance is per-document, "
            "static, and independent of the session</b> — <b>all "
            "three of which Module 01 §3 says are "
            "false</b>, and which the methodology accepts as a working "
            "approximation.",
            "<b>And completeness is unattainable:</b> <b>you cannot "
            "judge every document, so unjudged documents are treated as "
            "non-relevant</b> — which systematically penalises a "
            "system that finds something the pooling missed."]},

  {"t": "code", "kicker": "Pooling", "title": "How judgements are actually produced, and the bias it creates",
   "lang": "text", "code": """
  POOLING
      run many different systems on each query, take
      the top k from each, judge the union. Anything
      outside the pool is assumed non-relevant.

  WHY IT IS NECESSARY
      judging a million documents per query is
      impossible. The pool is a few hundred.

  AND THE BIAS IT CREATES
      a NEW system that retrieves a relevant document
      no pooled system found is scored as if that
      document were irrelevant. So the collection
      systematically favours systems resembling the
      ones that built the pool.

  WHICH MATTERED when dense retrieval arrived: it
  found documents lexical pools had missed, and old
  collections understated it.

  SO: check pool coverage for your system before
  trusting an old collection's verdict on it.
""",
   "caption": "<b>Old test collections favour systems like the ones "
              "that built them</b> — which is a structural bias, not "
              "a flaw in any particular collection.",
   "note": "The pooling bias is the methodology's deepest "
           "limitation."},

  {"t": "section", "label": "Part 2", "title": "Judgements",
   "blurb": "Which you will have to make yourself."},

  {"t": "bullets", "kicker": "Judging", "title": "How to produce judgements you can defend",
   "items": [
     "<b>Write the criteria before judging anything</b> — "
     "because <b>criteria articulated afterwards describe what you "
     "happened to find</b> (Module 01 §4).",
     "",
     "<b>Use graded rather than binary labels.</b> <b>Partially "
     "useful is the common case</b> (Module 01 §3), and "
     "a binary label discards that.",
     "",
     "<b>Judge blind to the system</b> that retrieved the "
     "document, and in a randomised order.",
     "",
     "<b>Measure your agreement with yourself</b> by re-judging a "
     "sample after a week — <b>which is usually lower than "
     "people expect</b> and bounds what any metric can "
     "resolve.",
     "",
     "<b>And measure inter-judge agreement if you have two "
     "judges</b>, because <b>a metric difference smaller than the "
     "disagreement is not a finding.</b>",
   ],
   "footnote": "<b>Judge disagreement bounds the resolution of every "
               "comparison</b> — and the reassuring finding is that "
               "system <i>rankings</i> are fairly stable even when "
               "individual judgements are not."},

  {"t": "section", "label": "Part 3", "title": "Metrics",
   "blurb": "Each encoding a model of user behaviour."},

  {"t": "table", "kicker": "Metrics", "title": "The metrics, and the user they assume",
   "header": ["Metric", "Assumes the user", "Use when"],
   "widths": [2.5, 4.1, 4.8],
   "rows": [
     ["<b>Precision@k</b>", "<b>Looks at exactly k results</b>", "<b>A fixed-size result page</b>"],
     ["<b>Recall</b>", "<b>Needs everything relevant</b>", "<b>Legal, medical, patent search</b>"],
     ["<b>MRR</b>", "<b>Wants one answer, stops when found</b>", "<b>Navigational queries (M01 §3)</b>"],
     ["<b>MAP</b>", "<b>Reads down the whole list</b>", "<b>Binary judgements, full ranking</b>"],
     ["<b>NDCG</b>", "<b>Discounts by rank; gain is graded</b>", "<b>The general default</b>"],
   ],
   "footnote": "<b>Every metric encodes a model of how the user reads "
               "the list</b> — so <b>choosing a metric is choosing a "
               "user model</b>, and the choice should follow from "
               "Module 01 §3's intent.",
   "note": "The metric-as-user-model framing is the module's key "
           "idea."},

  {"t": "callout", "title": "And no standard metric accounts for redundancy",
   "kind": "The assumption they all share",
   "body": ["<b>Every metric above sums per-document gains</b> "
            "— so <b>ten identical relevant documents score as well "
            "as ten different ones</b>, which is plainly wrong for a "
            "person.",
            "<b>Which is Module 01 §3's point:</b> "
            "<b>a list's relevance is not the sum of its documents'</b>, "
            "and the standard metrics assume it is.",
            "<b>Diversity-aware metrics exist</b> — "
            "α-NDCG and the subtopic measures — <b>and they "
            "require subtopic judgements</b>, which are much more "
            "expensive to produce.",
            "<b>So the practical answer is to measure diversity "
            "separately</b> and report it alongside — which is "
            "cheap, and makes the limitation visible rather than "
            "hidden."]},

  {"t": "section", "label": "Part 4", "title": "Clicks, and comparing",
   "blurb": "Abundant data with a specific bias."},

  {"t": "callout", "title": "Clicks are abundant and position-biased, so they are relative evidence rather than absolute",
   "kind": "What click data can and cannot tell you",
   "body": ["<b>Users click higher results more, regardless of "
            "relevance</b> — so <b>a click rate is a measure of "
            "position as much as of quality</b>, and comparing absolute "
            "click rates across systems is invalid.",
            "<b>But a click on a lower result when a higher one was "
            "skipped is informative</b> — which is what the pairwise "
            "preference models extract, and it is "
            "position-corrected by construction.",
            "<b>And interleaving is the strong method:</b> <b>mix two "
            "systems' results into one list and see which system's "
            "contributions get clicked</b> — which controls for "
            "position directly and is far more sensitive than an A/B "
            "test.",
            "<b>With the caveat that clicks measure "
            "attractiveness</b> — <b>a misleading title gets "
            "clicked</b> — so pair them with a dwell or satisfaction "
            "signal."]},

  {"t": "bullets", "kicker": "Comparing", "title": "Making a comparison that means something",
   "items": [
     "<b>Tune the baseline with equal effort</b> — <b>a "
     "default-parameter BM25 against a tuned system is not a "
     "comparison</b> (Module 03 §3).",
     "",
     "<b>Use enough queries.</b> <b>Fifty is a minimum and the "
     "variance across queries is large</b> — so report a "
     "per-query significance test, paired.",
     "",
     "<b>Report the per-query distribution</b>, not only the "
     "mean — <b>a system that improves the average by hurting "
     "a third of queries is a different proposition.</b>",
     "",
     "<b>Report the latency alongside the "
     "quality</b> (Module 04 §4), because the two are "
     "traded.",
     "",
     "<b>And read the worst queries</b>, which is where the "
     "diagnosis is (Project 2).",
   ],
   "footnote": "<b>The per-query distribution is the report that "
               "changes decisions</b> — a mean improvement hiding "
               "widespread regressions is a common and important "
               "finding."},
 ],
 "takeaways": [
   "The judgements assume relevance is per-document, static, and "
   "session-independent, all of which are false and accepted as a working "
   "approximation.",
   "Pooling makes old test collections systematically favour systems "
   "resembling the ones that built the pool.",
   "Write relevance criteria before judging, because criteria articulated "
   "afterwards describe what you happened to find.",
   "Your agreement with yourself is lower than you expect, and it bounds "
   "the resolution of every comparison.",
   "Every metric encodes a model of how the user reads the list, so "
   "choosing a metric is choosing a user model.",
   "Clicks are position-biased, so they are relative evidence — and "
   "interleaving controls for position directly.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The methodology"),
  ("callout", "A test collection is a collection, a query set, and relevance "
              "judgements — each with assumptions",
   ["<b>The collection must resemble the documents your system will "
    "actually face</b> — and <b>a benchmark collection from a "
    "different domain measures transfer rather than quality</b>, which is "
    "a different and usually harder question than the one you asked.",
    "<b>The queries must come from real information needs</b> "
    "(Module 01 &sect;4) — and <b>queries written by reading "
    "documents make the evaluation circular</b>, because the document is "
    "guaranteed findable by construction.",
    "<b>The judgements assume relevance is per-document, static, and "
    "independent of the session</b> — <b>all three of which "
    "Module 01 &sect;3 establishes are false</b> — and <b>the "
    "methodology accepts them as a working approximation</b>, which is "
    "defensible and should be stated rather than forgotten.",
    "<b>And completeness is unattainable:</b> <b>you cannot judge "
    "every document in a large collection, so unjudged documents are "
    "treated as non-relevant</b> — <b>which systematically penalises "
    "a system that finds something the judging process missed</b>, and is "
    "the pooling bias below."]),
  ("code", """POOLING
    run many different systems on each query, take the
    top k from each, and judge the union. Anything
    outside the pool is assumed non-relevant.

WHY IT IS NECESSARY
    judging a million documents per query is simply
    impossible. The pool is a few hundred.

AND THE BIAS IT CREATES
    a NEW system that retrieves a relevant document
    that no pooled system found is scored as if that
    document were irrelevant. So the collection
    systematically favours systems that resemble the
    ones which built the pool.

WHICH MATTERED when dense retrieval arrived: it found
documents that lexical pools had missed, and the old
collections consequently understated it.

SO: check the pool coverage for your own system before
trusting an old collection's verdict on it."""),
  ("p", "<b>Old test collections favour systems like the ones that "
        "built them</b> — <b>which is a structural bias rather than a "
        "flaw in any particular collection</b>, and it is <b>the "
        "methodology's deepest limitation</b>. The practical check is "
        "cheap: take your system's top results that are unjudged, judge a "
        "sample of them yourself, and estimate how much the collection is "
        "understating you. <b>This is exactly the check that was missing "
        "during the early neural retrieval comparisons.</b>"),

  ("h1", "2 &nbsp; Judgements"),
  ("ul", ["<b>Write the criteria before judging anything</b> — "
          "because <b>criteria articulated afterwards describe what you "
          "happened to find</b> (Module 01 &sect;4, and CSCE 676 "
          "Module 11's forking paths in a judgement setting).",
          "<b>Use graded rather than binary labels.</b> <b>Partially "
          "useful is the common case</b> (Module 01 &sect;3), and <b>a "
          "binary label discards exactly the information that "
          "distinguishes a good ranking from an adequate one.</b>",
          "<b>Judge blind to which system retrieved the "
          "document</b>, and in a randomised order — both of which "
          "are easy to arrange and both of which are routinely "
          "neglected in small-scale evaluations.",
          "<b>Measure your agreement with yourself</b> by re-judging a "
          "sample a week later — <b>which is usually substantially "
          "lower than people expect</b>, and <b>bounds what any metric "
          "can resolve</b>: a difference smaller than your own "
          "inconsistency is not detectable.",
          "<b>And measure inter-judge agreement if you have two "
          "judges</b>, because <b>a metric difference smaller than the "
          "disagreement is not a finding</b>. <b>Judge disagreement "
          "bounds the resolution of every comparison</b> — and <b>the "
          "reassuring empirical finding is that system <i>rankings</i> "
          "are fairly stable even when individual judgements are "
          "not</b>, which is what makes the methodology workable at "
          "all."]),

  ("break",),
  ("h1", "3 &nbsp; Metrics"),
  ("table", ["Metric", "The user model it assumes", "Use it when"],
   [["<b>Precision@k</b>",
     "<b>The user looks at exactly k results and no further.</b>",
     "<b>There is a fixed-size result page.</b>"],
    ["<b>Recall</b>",
     "<b>The user needs everything relevant and will keep looking.</b>",
     "<b>Legal discovery, systematic review, patent search</b> — "
     "where a miss is the expensive error."],
    ["<b>Mean reciprocal rank</b>",
     "<b>The user wants one answer and stops as soon as it is "
     "found.</b>",
     "<b>Navigational queries</b> (Module 01 &sect;3)."],
    ["<b>Mean average precision</b>",
     "<b>The user reads down the whole list, caring about every "
     "relevant document's position.</b>",
     "<b>Binary judgements and a full ranking.</b>"],
    ["<b>NDCG</b>",
     "<b>Gain is graded, and discounted logarithmically by rank.</b>",
     "<b>The general default</b> — and the one to report unless you "
     "have a reason not to."]],
   [0.19, 0.35, 0.46]),
  ("p", "<b>Every metric encodes a model of how the user reads the "
        "list</b> — how far down they go, whether they stop, how much "
        "a lower position is worth — <b>so choosing a metric is "
        "choosing a user model</b>, and <b>the choice should follow from "
        "Module 01 &sect;3's intent taxonomy</b> rather than from "
        "convention. <b>The metric-as-user-model framing is this "
        "module's key idea</b>, and it makes the choice arguable rather "
        "than arbitrary."),
  ("callout", "And no standard metric accounts for redundancy",
   ["<b>Every metric in the table sums per-document gains</b> — so "
    "<b>ten identical relevant documents score exactly as well as ten "
    "different relevant ones</b>, which is plainly wrong from the point "
    "of view of a person reading the list.",
    "<b>Which is Module 01 &sect;3's point arriving as a concrete "
    "measurement failure:</b> <b>a list's relevance is not the sum of "
    "its documents' relevances</b>, and the standard metrics assume that "
    "it is because the assumption makes them computable.",
    "<b>Diversity-aware metrics do exist</b> — &alpha;-NDCG and "
    "the various subtopic measures — <b>and they require subtopic "
    "judgements</b>, which are considerably more expensive to produce "
    "than relevance judgements and are therefore rare.",
    "<b>So the practical answer is to measure diversity "
    "separately</b>, with a simple pairwise-similarity statistic over "
    "the result list, <b>and report it alongside the relevance "
    "metric</b> — which is cheap and <b>makes the limitation "
    "visible rather than hidden</b>, which is this course's general "
    "move."]),

  ("h1", "4 &nbsp; Clicks, and comparing"),
  ("callout", "Clicks are abundant and position-biased, so they are relative "
              "evidence rather than absolute",
   ["<b>Users click higher-ranked results more often regardless of "
    "their relevance</b> — the effect is large and well "
    "measured — so <b>a click-through rate is a measure of position "
    "as much as of quality</b>, and <b>comparing absolute click rates "
    "across differently-ordered systems is invalid.</b>",
    "<b>But a click on a lower result when a higher one was skipped "
    "<i>is</i> informative</b> — the user saw both and chose the "
    "lower — <b>which is what the pairwise preference models "
    "extract</b>, and it is position-corrected by construction rather "
    "than by modelling.",
    "<b>And interleaving is the strong method:</b> <b>mix two systems' "
    "results into a single list and observe which system's contributions "
    "receive the clicks</b> — <b>which controls for position "
    "directly and is far more sensitive than a conventional A/B "
    "test</b>, detecting differences with far less traffic.",
    "<b>With the important caveat that clicks measure "
    "attractiveness:</b> <b>a misleading title gets clicked</b> — so "
    "<b>pair the click signal with a dwell time or an explicit "
    "satisfaction signal</b>, or you will optimise for bait "
    "(Module 12 &sect;3's feedback argument)."]),
  ("ul", ["<b>Tune the baseline with equal effort</b> — <b>a "
          "default-parameter BM25 against a carefully tuned system is not "
          "a comparison</b> (Module 03 &sect;3's callout, and "
          "CSCE 676 Module 13 &sect;2).",
          "<b>Use enough queries.</b> <b>Fifty is a bare minimum and "
          "the variance across queries is large</b> — so <b>report a "
          "paired per-query significance test</b> rather than comparing "
          "two means.",
          "<b>Report the per-query distribution, not only the "
          "mean</b> — <b>a system that improves the average while "
          "hurting a third of the queries is a materially different "
          "proposition</b> from one that improves most queries slightly, "
          "and the mean cannot distinguish them.",
          "<b>Report the latency alongside the quality</b> "
          "(Module 04 &sect;4), <b>because the two are traded</b> and "
          "a quality claim without a latency figure is incomplete.",
          "<b>And read the worst queries</b>, which is where the "
          "diagnosis is (Project 2's last requirement, and CSCE 638 "
          "Module 10 &sect;4's error analysis). <b>The per-query "
          "distribution is the report that changes decisions</b> — a "
          "mean improvement concealing widespread regressions is a common "
          "and important finding, and it only shows up if you look."]),
 ],
 "resources": [
   ("Manning, Raghavan & Sch&uuml;tze, chapter 8 (free)",
    "https://nlp.stanford.edu/IR-book/",
    "<b>&sect;1 and &sect;3</b> — the metrics defined carefully, with "
    "the test collection methodology."),
   ("Sanderson &mdash; Test Collection Based Evaluation (free)",
    "https://www.nowpublishers.com/article/Details/INR-009",
    "<b>&sect;1 and &sect;2 critically</b> — the assumptions, the "
    "pooling bias, and the judge agreement literature."),
   ("Chapelle et al. &mdash; Large-scale validation of click models "
    "(free)",
    "https://dl.acm.org/doi/10.1145/1645953.1646033",
    "<b>&sect;4's position bias, measured</b> — and the models that "
    "correct for it."),
   ("Radlinski & Craswell &mdash; Comparing the sensitivity of "
    "information retrieval metrics (free)",
    "https://dl.acm.org/doi/10.1145/1835449.1835560",
    "<b>&sect;4's interleaving argument</b> — how much more sensitive "
    "it is, with the numbers."),
 ],
 "exercises": [
   "<b>State the three assumptions</b> the judgements make, and which "
   "Module 01 says are false.",
   "<b>Judge your system's unjudged top results</b> on an existing "
   "collection, and estimate the pooling bias against you.",
   "<b>Write your relevance criteria</b>, then judge fifty "
   "query-document pairs.",
   "<b>Re-judge ten of them a week later</b> and compute your agreement "
   "with yourself.",
   "<b>Compute all five metrics</b> on the same run and compare the "
   "system rankings they imply.",
   "<b>Construct a result list that scores well and is highly "
   "redundant.</b>",
   "<b>Measure diversity separately</b> and report it alongside NDCG.",
   "<b>Plot click rate against rank position</b> on any click log you "
   "can get.",
   "<b>Run a paired significance test</b> between two systems over fifty "
   "queries.",
   "<b>Plot the per-query difference</b> and report how many queries got "
   "worse.",
 ],
 "selfcheck": [
   "Name the three components of a test collection and an assumption "
   "each makes.",
   "What is pooling, why is it necessary, and what bias does it "
   "create?",
   "Why did the pooling bias matter for dense retrieval?",
   "Give five rules for producing defensible judgements.",
   "Why does judge disagreement bound every comparison?",
   "Name five metrics and the user model each assumes.",
   "What do all the standard metrics fail to account for?",
   "Why are clicks relative rather than absolute evidence?",
   "What does interleaving control for, and what do clicks still "
   "measure?",
   "Give five requirements for a meaningful comparison.",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Learning to Rank",
 "subtitle": "Ranking as a supervised problem.",
 "question": "How do you combine hundreds of relevance signals?",
 "outcomes": [
     "Explain why ranking is not classification or "
     "regression.",
     "Explain the three loss formulations.",
     "Explain the features that matter and where they come "
     "from.",
     "Explain the two-stage architecture and why it exists.",
     "Train and deploy a ranker.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why it is its own problem",
   "blurb": "The loss does not decompose over documents."},

  {"t": "callout", "title": "Ranking is not classification, because the loss depends on the other documents",
   "kind": "The structural difference",
   "body": ["<b>Classifying each document as relevant or not ignores "
            "that only the order matters</b> — and <b>getting the "
            "top result right matters far more than getting the "
            "hundredth right.</b>",
            "<b>So the loss does not decompose over documents:</b> "
            "<b>a document's contribution depends on where the other "
            "documents ended up</b>, which ordinary supervised learning "
            "assumes away.",
            "<b>And the metrics are not "
            "differentiable.</b> <b>NDCG depends on the sorted "
            "order</b>, so it is piecewise constant and has zero gradient "
            "almost everywhere.",
            "<b>Which is why there are three formulations</b> "
            "(Part 2) — <b>each a different way of getting a "
            "usable gradient out of a ranking objective</b>, and the "
            "differences between them are about that rather than about "
            "features."]},

  {"t": "table", "kicker": "Formulations", "title": "The three approaches",
   "header": ["Approach", "Learns", "Trade"],
   "widths": [2.5, 4.0, 4.9],
   "rows": [
     ["<b>Pointwise</b>", "<b>A relevance score per document</b>", "<b>Simplest; ignores rank entirely</b>"],
     ["<b>Pairwise</b>", "<b>Which of two documents ranks higher</b>", "<b>Natural from clicks; weights all pairs equally</b>"],
     ["<b>Listwise</b>", "<b>Optimises a metric over the whole list</b>", "<b>Matches the objective; harder to optimise</b>"],
   ],
   "footnote": "<b>LambdaMART is the practical answer</b> — a "
               "pairwise gradient weighted by how much swapping the pair "
               "would change NDCG, which is listwise in effect and "
               "pairwise in form.",
   "note": "LambdaMART's trick is the thing to understand here."},

  {"t": "section", "label": "Part 2", "title": "LambdaMART",
   "blurb": "Which is still the thing to beat on tabular features."},

  {"t": "callout", "title": "Weight each pairwise gradient by the NDCG change that swapping the pair would cause",
   "kind": "The idea that resolved the formulation problem",
   "body": ["<b>A pairwise model treats every misordered pair "
            "equally</b> — but <b>swapping positions 1 and 2 matters "
            "enormously and swapping 99 and 100 matters almost "
            "nothing.</b>",
            "<b>So multiply each pair's gradient by "
            "|ΔNDCG| from swapping them</b> — which makes "
            "the model concentrate its effort where the metric is "
            "sensitive.",
            "<b>Which gives a gradient that optimises a "
            "non-differentiable metric</b>, by construction rather than "
            "by approximating the metric itself.",
            "<b>Combined with gradient-boosted trees, this is "
            "LambdaMART</b> — and <b>it remains extremely strong on "
            "tabular ranking features</b>, which is why it is still "
            "deployed widely (CSCE 633 §07)."]},

  {"t": "section", "label": "Part 3", "title": "Features",
   "blurb": "Where most of the gain actually is."},

  {"t": "code", "kicker": "Features", "title": "What a production ranker uses",
   "lang": "text", "code": """
  QUERY-DOCUMENT MATCH
      BM25 per field (title, body, anchor), term
      proximity, coverage of query terms, and any
      semantic similarity score (Module 07)

  DOCUMENT QUALITY, independent of the query
      PageRank or another link score (Module 10),
      length, spam score, freshness, readability

  QUERY FEATURES
      length, rarity, detected intent (Module 09)

  BEHAVIOURAL
      historical click-through rate for this
      query-document pair, dwell time, and
      aggregate popularity

  AND THE BEHAVIOURAL FEATURES ARE THE STRONGEST and
  the most dangerous: they encode what was previously
  shown, which creates the feedback loop of
  Module 12 section 3, and they are unavailable for
  anything new.
""",
   "caption": "<b>Behavioural features are the strongest and the most "
              "dangerous</b> — they work very well and they entrench "
              "the previous ranking.",
   "note": "The strongest-and-most-dangerous framing is the honest "
           "one."},

  {"t": "bullets", "kicker": "Practice", "title": "And the practical findings about features",
   "items": [
     "<b>Feature engineering beat model sophistication</b> for "
     "most of this field's history — and <b>a good feature set "
     "with a simple model beats the reverse.</b>",
     "",
     "<b>Features must be computable within the latency "
     "budget</b>, for every candidate — which excludes a great "
     "deal (Module 04 §4).",
     "",
     "<b>And they must be available at serving time</b>, which "
     "excludes anything derived from the future or from the full "
     "session (CSCE 633 §11's leakage).",
     "",
     "<b>Watch for position bias leaking in through the "
     "behavioural features</b>, which encodes the old ranking into the "
     "new one.",
     "",
     "<b>And log the features as served</b>, not recomputed, "
     "because recomputation drifts and the training data becomes "
     "wrong.",
   ],
   "footnote": "<b>Logging features as served rather than recomputing "
               "them is the practice that prevents a slow, invisible "
               "training/serving skew.</b>"},

  {"t": "section", "label": "Part 4", "title": "Two stages",
   "blurb": "The field's central practical architecture."},

  {"t": "callout", "title": "Retrieve cheaply, then rerank expensively — because the budget is per query and not per document",
   "kind": "Why every real system has this shape",
   "body": ["<b>A good ranker is too expensive to run over a million "
            "documents</b> — but <b>running it over a hundred "
            "candidates is affordable</b>, and a hundred is enough if the "
            "right documents are among them.",
            "<b>So: a cheap, high-recall first stage</b> (BM25, or "
            "dense retrieval, or both) <b>followed by an expensive, "
            "high-precision reranker</b> over its top few "
            "hundred.",
            "<b>Which makes first-stage recall the binding "
            "constraint:</b> <b>the reranker cannot recover a document "
            "the retrieval missed</b> — exactly "
            "CSCE 638 §11 §2's point.",
            "<b>And the number of candidates is the dial</b> — "
            "<b>more candidates means better recall and a more expensive "
            "rerank</b>, which is where the latency budget enters the "
            "design."]},

  {"t": "bullets", "kicker": "Deployment", "title": "And what to watch in deployment",
   "items": [
     "<b>Measure recall at the first-stage cutoff</b>, separately "
     "from end-to-end quality — because <b>it bounds everything "
     "downstream.</b>",
     "",
     "<b>Measure the reranker's effect on the candidates it "
     "received</b>, which isolates its contribution.",
     "",
     "<b>Retrain on a schedule</b>, because the collection, the "
     "queries, and the behavioural features all drift "
     "(CSCE 633 §11).",
     "",
     "<b>And monitor the feature distributions</b>, since a "
     "silently broken feature degrades quality without any "
     "error.",
     "",
     "<b>Which is the commonest production failure in a learned "
     "ranker</b> — a feature pipeline breaks and the model keeps "
     "serving.",
   ],
   "footnote": "<b>A silently broken feature is the characteristic "
               "learned-ranker failure</b> — the model degrades "
               "gracefully and nothing alerts, which is why feature "
               "monitoring is the control that matters."},
 ],
 "takeaways": [
   "The ranking loss does not decompose over documents, and the metrics are "
   "not differentiable, which is why there are three formulations.",
   "LambdaMART weights each pairwise gradient by the NDCG change from "
   "swapping the pair, which optimises a non-differentiable metric by "
   "construction.",
   "Behavioural features are the strongest and the most dangerous — "
   "they entrench the previous ranking and are unavailable for anything "
   "new.",
   "Feature engineering beat model sophistication for most of this field's "
   "history.",
   "Retrieve cheaply then rerank expensively, because the budget is per "
   "query rather than per document.",
   "First-stage recall is the binding constraint, since the reranker "
   "cannot recover a document the retrieval missed.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why ranking is its own problem"),
  ("callout", "Ranking is not classification, because the loss depends on "
              "the other documents",
   ["<b>Classifying each document independently as relevant or not "
    "ignores the fact that only the <i>order</i> matters</b> — and "
    "<b>getting the top result right matters very much more than getting "
    "the hundredth right</b>, which a per-document loss cannot "
    "express.",
    "<b>So the loss does not decompose over documents:</b> <b>a "
    "document's contribution to the quality of the result depends on "
    "where all the other documents ended up</b>, <b>which ordinary "
    "supervised learning assumes away</b> entirely.",
    "<b>And the metrics are not differentiable.</b> <b>NDCG depends "
    "on the sorted order of the scores</b>, so it is piecewise constant "
    "as a function of the scores and <b>has zero gradient almost "
    "everywhere</b> — which means it cannot be optimised directly by "
    "gradient descent.",
    "<b>Which is exactly why there are three formulations</b> "
    "(&sect;1's table) — <b>each one a different way of getting a "
    "usable gradient out of a ranking objective</b> — and <b>the "
    "differences between them are about that rather than about "
    "features</b>, which is worth keeping straight."]),
  ("table", ["Approach", "What it learns", "The trade"],
   [["<b>Pointwise</b>",
     "<b>A relevance score for each document independently.</b>",
     "<b>Simplest, and it ignores rank entirely</b> — so it spends "
     "equal effort on position 1 and position 1000."],
    ["<b>Pairwise</b>",
     "<b>Which of two documents should rank higher.</b>",
     "<b>Natural to derive from clicks</b> (Module 05 &sect;4), "
     "<b>and it weights all pairs equally</b>, which is &sect;2's "
     "problem."],
    ["<b>Listwise</b>",
     "<b>Optimises a metric computed over the whole result list.</b>",
     "<b>Matches the actual objective, and is harder to optimise</b> "
     "because of the differentiability problem above."]],
   [0.19, 0.34, 0.47]),
  ("p", "<b>LambdaMART is the practical answer</b>, and it sits oddly "
        "across this taxonomy: <b>a pairwise gradient weighted by how much "
        "swapping the pair would change NDCG</b>, <b>which is listwise in "
        "effect and pairwise in form</b>. <b>Its trick is the thing to "
        "understand in this module</b>, because it is both the practical "
        "default and a genuinely clever resolution of a real "
        "difficulty."),

  ("h1", "2 &nbsp; LambdaMART"),
  ("callout", "Weight each pairwise gradient by the NDCG change that "
              "swapping the pair would cause",
   ["<b>A plain pairwise model treats every misordered pair as equally "
    "important</b> — but <b>swapping positions 1 and 2 matters "
    "enormously to the user and swapping positions 99 and 100 matters "
    "essentially not at all</b>, and the metric knows this while the loss "
    "does not.",
    "<b>So multiply each pair's gradient by the absolute change in "
    "NDCG that swapping them would produce</b> — which <b>makes the "
    "model concentrate its learning effort precisely where the metric is "
    "sensitive</b>, and costs almost nothing to compute.",
    "<b>Which yields a gradient that effectively optimises a "
    "non-differentiable metric</b> — <b>by construction rather than "
    "by constructing a differentiable approximation to the metric</b>, "
    "which is what the listwise methods attempt and which works less "
    "well.",
    "<b>Combined with gradient-boosted decision trees, this is "
    "LambdaMART</b> — and <b>it remains extremely strong on tabular "
    "ranking features</b> (CSCE 633 Module 07's finding that boosted "
    "trees dominate tabular problems, arriving here), <b>which is why it "
    "is still deployed very widely</b> in systems that also have neural "
    "components."]),

  ("break",),
  ("h1", "3 &nbsp; Features"),
  ("code", """QUERY-DOCUMENT MATCH
    BM25 per field (title, body, anchor text), term
    proximity, coverage of the query terms, and any
    semantic similarity score (Module 07)

DOCUMENT QUALITY, independent of the query
    PageRank or another link-based score
    (Module 10), length, spam score, freshness,
    readability, domain reputation

QUERY FEATURES
    length, rarity, detected intent (Module 09)

BEHAVIOURAL
    historical click-through rate for this
    query-document pair, dwell time, skip rate, and
    aggregate document popularity

AND THE BEHAVIOURAL FEATURES ARE THE STRONGEST and
also the most dangerous: they encode what was
previously shown, which creates the feedback loop of
Module 12 section 3, and they are entirely
unavailable for anything new."""),
  ("ul", ["<b>Feature engineering beat model sophistication</b> for "
          "most of this field's history — and <b>a good feature set "
          "with a simple model beats a sophisticated model with a poor "
          "feature set</b>, reliably, which is worth knowing before "
          "choosing where to spend effort.",
          "<b>Features must be computable within the latency "
          "budget</b>, <b>for every candidate document</b> — which "
          "<b>excludes a great deal</b> that would otherwise be useful "
          "(Module 04 &sect;4), and is why the two-stage architecture "
          "of &sect;4 matters so much.",
          "<b>And they must be available at serving time</b>, which "
          "excludes anything derived from the future or from the complete "
          "session — <b>which is CSCE 633 Module 11's leakage "
          "problem</b>, and it is easy to violate accidentally when "
          "training from logs.",
          "<b>Watch for position bias leaking in through the "
          "behavioural features</b> (Module 05 &sect;4), <b>which "
          "encodes the old ranking directly into the new one</b> and is "
          "the mechanism behind Module 12 &sect;3's feedback loop.",
          "<b>And log the features as served, rather than recomputing "
          "them for training</b> — because <b>recomputation drifts "
          "as the pipeline changes and the training data silently becomes "
          "wrong</b>. <b>Logging features as served is the practice that "
          "prevents a slow, invisible training/serving skew</b>, which is "
          "among the hardest production problems to diagnose after the "
          "fact."]),

  ("h1", "4 &nbsp; The two-stage architecture"),
  ("callout", "Retrieve cheaply, then rerank expensively — because the "
              "budget is per query and not per document",
   ["<b>A good ranker is far too expensive to run over a million "
    "documents</b> — but <b>running the same ranker over a hundred "
    "candidates is entirely affordable</b>, and <b>a hundred is enough "
    "<i>if</i> the right documents are among them.</b>",
    "<b>So: a cheap, high-recall first stage</b> — BM25, or dense "
    "retrieval, or both combined (Module 07 &sect;4) — "
    "<b>followed by an expensive, high-precision reranker over its top "
    "few hundred results.</b> This is the shape of essentially every "
    "production search system.",
    "<b>Which makes first-stage recall the binding "
    "constraint:</b> <b>the reranker cannot recover a document the "
    "retrieval stage missed</b> — which is exactly <b>CSCE 638 "
    "Module 11 &sect;2's point</b>, and is why &sect;4's first "
    "deployment measurement is first-stage recall.",
    "<b>And the number of candidates is the dial</b> — <b>more "
    "candidates means better recall and a more expensive reranking "
    "step</b> — <b>which is precisely where the latency budget "
    "enters the design</b> rather than being discovered afterwards "
    "(Module 04 &sect;4)."]),
  ("ul", ["<b>Measure recall at the first-stage cutoff</b>, separately "
          "from the end-to-end quality — because <b>it bounds "
          "everything downstream</b> and a system failing here cannot be "
          "fixed by improving the reranker.",
          "<b>Measure the reranker's effect on the candidates it "
          "actually received</b>, which <b>isolates its contribution</b> "
          "from the retrieval's and tells you which half to invest in.",
          "<b>Retrain on a schedule</b>, because <b>the collection, "
          "the query distribution, and the behavioural features all "
          "drift</b> (CSCE 633 Module 11) — and the behavioural "
          "features drift fastest, since they depend on what you have "
          "been showing.",
          "<b>And monitor the feature distributions</b>, since <b>a "
          "silently broken feature degrades quality without producing any "
          "error at all</b> — the model simply gets a constant or a "
          "default where it expected a signal, and keeps serving.",
          "<b>Which is the commonest production failure in a learned "
          "ranker</b>: a feature pipeline breaks upstream and <b>the "
          "model keeps serving, somewhat worse, indefinitely.</b> <b>A "
          "silently broken feature is the characteristic "
          "learned-ranker failure</b> — it degrades gracefully and "
          "nothing alerts — <b>which is why feature monitoring is "
          "the control that matters</b> rather than model monitoring."]),
 ],
 "resources": [
   ("Liu &mdash; Learning to Rank for Information Retrieval (free "
    "survey)",
    "https://www.nowpublishers.com/article/Details/INR-016",
    "<b>&sect;1's three formulations</b>, organised, with the theoretical "
    "relationships between them."),
   ("Burges &mdash; From RankNet to LambdaRank to LambdaMART (free)",
    "https://www.microsoft.com/en-us/research/publication/from-ranknet-to-lambdarank-to-lambdamart-an-overview/",
    "<b>&sect;2 by its author</b> — the clearest account of the "
    "lambda trick and why it works."),
   ("Qin et al. &mdash; Are Neural Rankers still Outperformed by "
    "Gradient Boosted Decision Trees? (free)",
    "https://openreview.net/forum?id=Ut1vF_q_vC",
    "<b>&sect;2's continued relevance, measured</b> — on tabular "
    "ranking features, which is the setting that matters here."),
   ("Joachims et al. &mdash; Unbiased Learning-to-Rank with Biased "
    "Feedback (free)",
    "https://arxiv.org/abs/1608.04468",
    "<b>&sect;3's position bias problem, with the correction</b> — "
    "inverse propensity weighting for click data."),
 ],
 "exercises": [
   "<b>Explain why a per-document loss is wrong</b> for ranking, with a "
   "concrete example.",
   "<b>Show that NDCG has zero gradient</b> almost everywhere.",
   "<b>Implement pointwise, pairwise, and listwise losses</b> and compare "
   "their NDCG.",
   "<b>Add the lambda weighting to your pairwise loss</b> and measure the "
   "improvement.",
   "<b>Build a feature set</b> with at least one feature from each of the "
   "four groups.",
   "<b>Train LambdaMART</b> and measure feature importance.",
   "<b>Remove the behavioural features</b> and report what you lose.",
   "<b>Build the two-stage architecture</b> and measure first-stage "
   "recall at 100 and 1000.",
   "<b>Measure the reranker's effect</b> on the candidates it "
   "received.",
   "<b>Break one feature deliberately</b> and measure how much quality "
   "falls before anything alerts.",
 ],
 "selfcheck": [
   "Why is ranking not classification?",
   "Why are the metrics not differentiable?",
   "Name the three formulations and the trade in each.",
   "Explain LambdaMART's weighting and what problem it solves.",
   "Name the four feature groups with an example from each.",
   "Why are behavioural features strongest and most dangerous?",
   "Give five practical findings about features.",
   "Why log features as served?",
   "State the two-stage argument and what the binding constraint is.",
   "Name the characteristic production failure and the control for it.",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Dense Retrieval",
 "subtitle": "Matching meaning, and when it helps.",
 "question": "Can you retrieve without sharing any terms?",
 "outcomes": [
     "Explain the bi-encoder and cross-encoder designs.",
     "Explain how a bi-encoder is trained.",
     "Explain where dense retrieval wins and where it loses.",
     "Explain hybrid retrieval and why it dominates.",
     "Build and evaluate a dense retriever.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two designs",
   "blurb": "And the difference is entirely about when you can "
            "precompute."},

  {"t": "table", "kicker": "Designs", "title": "Bi-encoder and cross-encoder",
   "header": ["", "Bi-encoder", "Cross-encoder"],
   "widths": [2.5, 4.1, 4.8],
   "rows": [
     ["<b>Input</b>", "<b>Query and document encoded separately</b>", "<b>Query and document encoded together</b>"],
     ["<b>Score</b>", "<b>Dot product of two vectors</b>", "<b>A model output over the pair</b>"],
     ["<b>Precompute</b>", "<b>All documents, offline</b>", "<b>Nothing — it needs the query</b>"],
     ["<b>Cost per query</b>", "<b>One encode, then vector search</b>", "<b>One model pass per candidate</b>"],
     ["<b>Quality</b>", "<b>Good</b>", "<b>Better — the terms interact</b>"],
     ["<b>Use as</b>", "<b>First-stage retrieval</b>", "<b>Reranker (M06 §4)</b>"],
   ],
   "footnote": "<b>The precompute row determines everything "
               "else</b> — a bi-encoder can index the collection in "
               "advance and a cross-encoder fundamentally cannot, which "
               "is why each has its stage.",
   "note": "The precompute argument explains the whole architecture."},

  {"t": "callout", "title": "A cross-encoder is better because the query and document terms can interact",
   "kind": "Why the quality difference exists",
   "body": ["<b>A bi-encoder must compress a document into one vector "
            "before it knows the query</b> — so <b>it has to "
            "anticipate every question anybody might ask</b>, which a "
            "fixed-size vector cannot do.",
            "<b>A cross-encoder sees both together</b>, so attention "
            "can match a query term against the specific part of the "
            "document that addresses it (CSCE 638 §06).",
            "<b>Which is a representational difference rather than a "
            "capacity one</b> — <b>a larger bi-encoder does not "
            "close the gap</b>, because the bottleneck is the single "
            "vector.",
            "<b>And it is the whole justification for the two-stage "
            "architecture</b> — <b>use the cheap one to narrow and "
            "the good one to order</b> "
            "(Module 06 §4)."]},

  {"t": "section", "label": "Part 2", "title": "Training",
   "blurb": "Where the negatives are the whole problem."},

  {"t": "code", "kicker": "Training", "title": "How a bi-encoder is trained",
   "lang": "text", "code": """
  THE OBJECTIVE
      contrastive: pull a query and its relevant
      document together, push the query and
      irrelevant documents apart.

  THE NEGATIVES ARE EVERYTHING
      random negatives     easy, and the model learns
                           only topical similarity
      in-batch negatives   free -- use the other
                           queries' documents in the
                           batch. Bigger batch, more
                           negatives, better model.
      hard negatives       documents retrieved by BM25
                           but not relevant. The ones
                           that teach the real
                           distinction.
      mined from the model itself, iteratively, which
                           is better again and risks
                           false negatives

  AND FALSE NEGATIVES ARE THE TRAP: an unlabelled
  relevant document used as a negative teaches the
  model exactly the wrong thing.
""",
   "caption": "<b>Hard negative mining is where the quality comes "
              "from</b>, and <b>false negatives are its characteristic "
              "failure.</b>",
   "note": "The negatives, not the architecture, determine dense "
           "retrieval quality."},

  {"t": "section", "label": "Part 3", "title": "Where it wins and loses",
   "blurb": "Specifically, and it is not uniform."},

  {"t": "bullets", "kicker": "Comparison", "title": "The honest comparison against BM25",
   "items": [
     "<b>Dense wins on paraphrase and vocabulary "
     "mismatch</b> — which is Module 01 §2's problem, "
     "and this is the first technique that attacks it "
     "directly.",
     "",
     "<b>And on short queries</b>, where there are too few terms "
     "for lexical matching to work with.",
     "",
     "<b>Lexical wins on exact terms:</b> <b>identifiers, product "
     "codes, names, numbers, and rare technical "
     "vocabulary</b> — which a fixed-dimension vector blurs "
     "together.",
     "",
     "<b>And on out-of-domain collections</b>, where <b>the dense "
     "model was trained somewhere else and BM25 needs no "
     "training</b> — which the zero-shot benchmarks "
     "showed clearly.",
     "",
     "<b>So the failure modes are complementary</b>, which is "
     "Part 4's argument.",
   ],
   "footnote": "<b>The out-of-domain result is the one that corrected "
               "the field's expectations</b> — dense retrievers "
               "transfer much less well than their in-domain numbers "
               "suggested."},

  {"t": "callout", "title": "And the single-vector bottleneck is the structural limit",
   "kind": "What no amount of training fixes",
   "body": ["<b>A document of two thousand words compressed to 768 "
            "numbers has lost most of itself</b> — and <b>which "
            "parts it kept were decided before the query was "
            "known.</b>",
            "<b>So a document covering several topics is represented "
            "as an average of them</b>, matching none well — which "
            "is why chunking matters so much in practice "
            "(CSCE 638 §11 §3).",
            "<b>The multi-vector designs address this</b> by storing "
            "a vector per token and matching them individually — "
            "<b>much better quality, and a much larger "
            "index.</b>",
            "<b>Which is the trade in this area:</b> <b>more vectors "
            "per document buys quality and costs storage and search "
            "time</b>, and the right point depends on your "
            "constraints."]},

  {"t": "section", "label": "Part 4", "title": "Hybrid",
   "blurb": "Which is the answer in practice."},

  {"t": "callout", "title": "Combine lexical and dense retrieval, because their failures are uncorrelated",
   "kind": "The practical conclusion",
   "body": ["<b>Run both and fuse the rankings</b> — <b>reciprocal "
            "rank fusion is the standard method and needs no "
            "tuning</b>, which makes it the right first "
            "attempt.",
            "<b>And the gain is real and consistent</b>, because "
            "<b>the two methods fail on different "
            "queries</b> (Part 3) rather than on the same "
            "ones.",
            "<b>With a learned combination doing better</b> if you "
            "have judgements — the scores become features for "
            "Module 06's ranker.",
            "<b>So the production shape is: hybrid first-stage "
            "retrieval, then a cross-encoder reranker</b> — "
            "<b>which is where this course's Modules 03, 06, and 07 "
            "converge</b>, and is the current standard "
            "architecture."]},

  {"t": "bullets", "kicker": "Practice", "title": "And what to measure",
   "items": [
     "<b>Recall at your first-stage cutoff</b>, for each method "
     "separately and for the fusion — which shows whether the "
     "hybrid is actually adding anything.",
     "",
     "<b>Performance on in-domain and out-of-domain "
     "queries</b> separately, because the gap is large "
     "(Part 3).",
     "",
     "<b>Performance on exact-match queries specifically</b> "
     "— identifiers and names — which is where a "
     "dense-only system fails embarrassingly.",
     "",
     "<b>The index size and the query latency</b>, since both are "
     "much larger than lexical (Module 08).",
     "",
     "<b>And the embedding model's version</b>, because <b>changing "
     "it invalidates the whole index</b> and that is an operational "
     "fact worth planning for.",
   ],
   "footnote": "<b>Changing the embedding model means reindexing "
               "everything</b> — which makes the model choice a "
               "commitment rather than a configuration."},
 ],
 "takeaways": [
   "The precompute row determines the architecture: a bi-encoder can index "
   "offline and a cross-encoder cannot, which is why each has its stage.",
   "A bi-encoder must compress a document before it knows the query, which "
   "is a representational limit a larger model does not close.",
   "The negatives rather than the architecture determine dense retrieval "
   "quality, and false negatives are the characteristic failure.",
   "Dense wins on paraphrase and short queries; lexical wins on exact "
   "terms and out of domain.",
   "The single-vector bottleneck is structural, and multi-vector designs "
   "trade index size for quality.",
   "Changing the embedding model invalidates the whole index, which makes "
   "the choice a commitment rather than a configuration.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two designs"),
  ("table", ["", "Bi-encoder", "Cross-encoder"],
   [["<b>Input</b>",
     "<b>Query and document encoded separately.</b>",
     "<b>Query and document encoded together, as one sequence.</b>"],
    ["<b>Score</b>", "<b>Dot product or cosine of the two vectors.</b>",
     "<b>A model output computed over the pair.</b>"],
    ["<b>Precompute</b>",
     "<b>All documents, offline, before any query arrives.</b>",
     "<b>Nothing — it fundamentally needs the query.</b>"],
    ["<b>Cost per query</b>",
     "<b>One query encode, then a vector search</b> "
     "(Module 08).",
     "<b>One full model pass per candidate document.</b>"],
    ["<b>Quality</b>", "<b>Good.</b>",
     "<b>Better — the query and document terms interact</b> (see the "
     "callout)."],
    ["<b>Use it as</b>", "<b>First-stage retrieval.</b>",
     "<b>A reranker</b> (Module 06 &sect;4)."]],
   [0.19, 0.38, 0.43]),
  ("p", "<b>The precompute row determines everything else in the "
        "table</b> — <b>a bi-encoder can index the entire collection "
        "in advance and a cross-encoder fundamentally cannot</b>, since "
        "its computation depends on the query — <b>which is why each "
        "design has its own stage</b> in the standard architecture. "
        "<b>The precompute argument explains the whole architecture</b>, "
        "and it is worth being able to derive the two-stage design from it "
        "rather than learning it as a convention."),
  ("callout", "A cross-encoder is better because the query and document "
              "terms can interact",
   ["<b>A bi-encoder must compress an entire document into a single "
    "fixed vector <i>before</i> it knows what the query will be</b> "
    "— so <b>it has to anticipate every question anybody might ever "
    "ask of that document</b>, which a fixed-size vector simply cannot "
    "do.",
    "<b>A cross-encoder sees both the query and the document "
    "together</b>, so <b>attention can match a specific query term "
    "against the specific part of the document that addresses it</b> "
    "(CSCE 638 Module 06 &sect;1's lookup framing, used for exactly "
    "this).",
    "<b>Which is a representational difference rather than a capacity "
    "one</b> — <b>a larger bi-encoder does not close the gap</b>, "
    "because <b>the bottleneck is the single vector</b> rather than the "
    "model's expressiveness, which is &sect;3's structural limit.",
    "<b>And it is the whole justification for the two-stage "
    "architecture</b> — <b>use the cheap design to narrow the "
    "candidate set and the good design to order it</b> (Module 06 "
    "&sect;4), which gets most of the cross-encoder's quality at a "
    "fraction of its cost."]),

  ("h1", "2 &nbsp; Training"),
  ("code", """THE OBJECTIVE
    contrastive: pull a query and its relevant
    document together in the embedding space, and
    push the query and irrelevant documents apart.

THE NEGATIVES ARE EVERYTHING
    random negatives     easy, and the model learns
                         only coarse topical
                         similarity from them
    in-batch negatives   free -- use the other
                         queries' documents in the
                         same batch. Bigger batch,
                         more negatives, better
                         model.
    hard negatives       documents retrieved by BM25
                         and judged not relevant.
                         The ones that teach the
                         actual distinction.
    mined from the model itself, iteratively, which
                         is better again and risks
                         false negatives

AND FALSE NEGATIVES ARE THE TRAP: an unlabelled but
genuinely relevant document used as a negative teaches
the model exactly the wrong thing."""),
  ("p", "<b>Hard negative mining is where the quality comes from</b> "
        "— the architecture is largely settled and <b>the negatives, "
        "not the architecture, determine dense retrieval quality</b>, "
        "which is a finding worth knowing before spending time on model "
        "variants. <b>And false negatives are its characteristic "
        "failure</b>: because relevance judgements are incomplete "
        "(Module 05 &sect;1's pooling), the hardest mined negatives "
        "are disproportionately likely to be unlabelled relevant "
        "documents, which actively damages the model."),

  ("break",),
  ("h1", "3 &nbsp; Where it wins and loses"),
  ("ul", ["<b>Dense retrieval wins on paraphrase and vocabulary "
          "mismatch</b> — which is <b>Module 01 &sect;2's central "
          "problem</b>, and <b>this is the first technique in the course "
          "that attacks it directly</b> rather than by term "
          "substitution.",
          "<b>And on short queries</b>, where <b>there are too few "
          "terms for lexical matching to work with</b> — a two-word "
          "query gives BM25 very little to compute with and gives an "
          "encoder enough to represent an intent.",
          "<b>Lexical retrieval wins on exact terms:</b> "
          "<b>identifiers, product codes, personal names, numbers, "
          "version strings, and rare technical vocabulary</b> — all "
          "of which <b>a fixed-dimension vector blurs together with its "
          "neighbours</b>, because that is what the embedding is for.",
          "<b>And on out-of-domain collections</b>, where <b>the dense "
          "model was trained on something else and BM25 requires no "
          "training at all</b> — <b>which the zero-shot benchmarks "
          "showed clearly</b> and which was not the expectation.",
          "<b>So the failure modes are complementary rather than "
          "overlapping</b>, which is &sect;4's entire argument. <b>The "
          "out-of-domain result is the one that corrected the field's "
          "expectations</b> — dense retrievers transfer considerably "
          "less well than their in-domain numbers had suggested, and "
          "BM25's training-free generality turned out to be worth more "
          "than it looked."]),
  ("callout", "And the single-vector bottleneck is the structural limit",
   ["<b>A document of two thousand words compressed into 768 numbers "
    "has lost the great majority of itself</b> — and critically, "
    "<b>which parts it kept were decided before the query was known</b> "
    "(&sect;1's callout).",
    "<b>So a document covering several distinct topics is represented "
    "as something like an average of them</b>, <b>matching none of them "
    "well</b> — which is exactly <b>why chunking matters so much in "
    "practice</b> (CSCE 638 Module 11 &sect;3's "
    "retrieve-small-generate-large pattern).",
    "<b>The multi-vector designs address this directly</b> by storing "
    "a vector per token and matching query tokens against document "
    "tokens individually — <b>much better quality, and a very much "
    "larger index</b>, which is the cost.",
    "<b>Which is the governing trade in this area:</b> <b>more vectors "
    "per document buys quality and costs storage and search time</b>, "
    "and <b>the right point on that curve depends entirely on your "
    "constraints</b> rather than on which is better in the abstract."]),

  ("h1", "4 &nbsp; Hybrid retrieval"),
  ("callout", "Combine lexical and dense retrieval, because their failures "
              "are uncorrelated",
   ["<b>Run both and fuse the rankings</b> — <b>reciprocal rank "
    "fusion is the standard method, needs no tuning, and requires no "
    "score calibration between the two systems</b>, which makes it the "
    "right first attempt and frequently the last one.",
    "<b>And the gain is real and consistent across collections</b>, "
    "because <b>the two methods fail on different queries</b> "
    "(&sect;3) rather than on the same ones — which is the "
    "condition under which combining two systems helps at all.",
    "<b>With a learned combination doing better still</b> if you have "
    "relevance judgements — <b>the two scores simply become "
    "features for Module 06's ranker</b>, alongside everything else, "
    "which is how production systems actually do it.",
    "<b>So the production shape is: hybrid first-stage retrieval, then "
    "a cross-encoder reranker</b> — <b>which is where this course's "
    "Modules 03, 06, and 07 converge</b>, and <b>is the current standard "
    "architecture</b> for a serious search system."]),
  ("ul", ["<b>Recall at your first-stage cutoff</b>, measured for each "
          "method separately and for the fusion — <b>which shows "
          "whether the hybrid is actually adding anything</b> or whether "
          "one method is doing all the work.",
          "<b>Performance on in-domain and out-of-domain queries "
          "separately</b>, because <b>the gap is large</b> (&sect;3) and "
          "an aggregate figure over a mixed query set tells you "
          "nothing useful about either.",
          "<b>Performance on exact-match queries specifically</b> "
          "— identifiers, product codes, personal names — which "
          "is <b>where a dense-only system fails embarrassingly</b> and "
          "where users notice immediately.",
          "<b>The index size and the query latency</b>, since <b>both "
          "are substantially larger than for a lexical index</b> "
          "(Module 08) and both are real operating costs.",
          "<b>And the embedding model's version</b>, because "
          "<b>changing it invalidates the entire index</b> — every "
          "document must be re-encoded — <b>and that is an "
          "operational fact worth planning for</b> rather than "
          "discovering. <b>Changing the embedding model means reindexing "
          "everything, which makes the model choice a commitment rather "
          "than a configuration.</b>"]),
 ],
 "resources": [
   ("Lin, Nogueira & Yates &mdash; Pretrained Transformers for Text "
    "Ranking (free)",
    "https://arxiv.org/abs/2010.06467",
    "<b>The whole module</b> — and the most careful available "
    "assessment of which results replicated."),
   ("Karpukhin et al. &mdash; Dense Passage Retrieval (free)",
    "https://aclanthology.org/2020.emnlp-main.550/",
    "<b>&sect;2's training in the original</b> — including the "
    "in-batch negatives finding."),
   ("Thakur et al. &mdash; BEIR (free)",
    "https://arxiv.org/abs/2104.08663",
    "<b>&sect;3's out-of-domain result</b> — the benchmark that showed "
    "how much less dense retrieval transfers."),
   ("Khattab & Zaharia &mdash; ColBERT (free)",
    "https://arxiv.org/abs/2004.12832",
    "<b>&sect;3's multi-vector answer</b> — late interaction, and the "
    "index size it costs."),
 ],
 "exercises": [
   "<b>Build a bi-encoder retriever</b> over your collection and measure "
   "recall at 100.",
   "<b>Add a cross-encoder reranker</b> and measure the NDCG "
   "improvement.",
   "<b>Measure the cross-encoder's latency per candidate</b> and compute "
   "the maximum candidates your budget allows.",
   "<b>Train with random negatives, then in-batch, then BM25 hard "
   "negatives</b>, and compare.",
   "<b>Find a false negative</b> among your mined hard negatives.",
   "<b>Compare dense and BM25 on paraphrase queries</b> and on "
   "identifier queries.",
   "<b>Evaluate your dense retriever on an out-of-domain "
   "collection</b> and report the gap.",
   "<b>Fuse the two rankings with reciprocal rank fusion</b> and measure "
   "the gain.",
   "<b>Measure recall for each method and the fusion</b> separately.",
   "<b>Time a full reindex</b> with a different embedding model.",
 ],
 "selfcheck": [
   "Contrast bi-encoder and cross-encoder on six dimensions.",
   "Which row determines the others, and why?",
   "Why is a cross-encoder better, and why does a bigger bi-encoder not "
   "close the gap?",
   "Describe the contrastive objective and the four kinds of "
   "negative.",
   "Why are the negatives the whole problem, and what is the trap?",
   "Where does dense retrieval win, and where does lexical?",
   "What was the out-of-domain finding?",
   "State the single-vector bottleneck and the multi-vector trade.",
   "Why does hybrid retrieval work, and what is the standard fusion "
   "method?",
   "Why is the embedding model choice a commitment?",
 ],
},

]
