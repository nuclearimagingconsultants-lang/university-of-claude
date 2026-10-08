# -*- coding: utf-8 -*-
"""CSCE 670 Information Retrieval — original course content."""

COURSE = {
    "code": "CSCE 670",
    "title": "Information Retrieval",
    "tagline": "Satisfying an information need, which is not the same as "
               "matching a query",
    "term": "Semester 10 (with CSCE 638 and CSCE 676)",
    "prereqs": "CSCE 629 Analysis of Algorithms and CSCE 633 Machine "
               "Learning; CSCE 638 runs in parallel and supplies the "
               "representation material; CSCE 676 Module 02 for the "
               "hashing used in Module 08",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A search system over a collection you care about "
                   "— with a hand-built relevance judgement set, a "
                   "lexical baseline it has to beat, an evaluation that "
                   "reflects how the results will be used, and a written "
                   "account of the queries it fails",
    "description": [
        "<b>Retrieval begins with a person who wants something and "
        "has typed an approximation of it.</b> <b>Module 01 "
        "establishes that gap properly</b>, because every technique in "
        "the course is an attempt to bridge it — <b>the query is "
        "evidence about a need rather than a specification of "
        "one</b>, and systems that treat it as a specification fail in "
        "predictable ways.",
        "<b>The course follows the engineering arc.</b> <b>An "
        "inverted index, a scoring function derived from stated "
        "assumptions, efficient query processing, then learned "
        "ranking, then dense representations</b> — and <b>each step "
        "is a response to a measured limitation of the previous "
        "one</b>, which is more useful to understand than any single "
        "component.",
        "<b>The second theme is that relevance is a human judgement "
        "and everything you measure is a proxy for it.</b> <b>Module "
        "05 is the course's centre</b>: the metrics, where they come "
        "from, what they assume about user behaviour, and <b>why a "
        "system tuned on one proxy can be worse for the people using "
        "it</b> — which is CSCE 676 Module 13's proxy problem in "
        "this course's form.",
        "<b>The third is that efficiency is a correctness "
        "concern.</b> <b>A ranking function you cannot evaluate within "
        "the latency budget is not a ranking function you have</b> "
        "— so Modules 04 and 08 are about making good ranking "
        "affordable, and the two-stage retrieve-then-rerank "
        "architecture that follows is the field's central practical "
        "idea.",
        "<b>And the closing position is about consequences and "
        "honest claims.</b> <b>Module 12 covers what a ranking does to "
        "the things being ranked</b> — exposure, feedback, and the "
        "people behind the documents — and <b>Module 13 is about "
        "what a retrieval evaluation establishes</b>, because <b>'our "
        "NDCG improved' is a claim about a judgement set</b>.",
    ],
    "outcomes": [
        "Distinguish an information need from a query and from a "
        "document.",
        "Build an inverted index and explain its compression.",
        "Derive and apply the standard scoring functions.",
        "Process queries efficiently with early termination.",
        "Evaluate a retrieval system and defend the metric.",
        "Train and deploy a learned ranker.",
        "Explain dense retrieval and when it helps.",
        "Search a large vector collection approximately.",
        "Understand and reformulate queries.",
        "Explain what web scale adds: crawling, spam, and links.",
        "Build a retrieval-augmented generative system.",
        "Explain exposure, feedback loops, and ranking's "
        "consequences.",
        "State what a retrieval result honestly establishes.",
    ],
    "materials": [
        ("Manning, Raghavan & Schütze — Introduction to Information "
         "Retrieval (free)",
         "https://nlp.stanford.edu/IR-book/",
         "<b>The primary text, free in full from the authors.</b> "
         "Modules 02 through 06 and 10 follow it closely, and its "
         "treatment of the index and the scoring derivations is still "
         "unmatched."),
        ("Croft, Metzler & Strohman — Search Engines: Information "
         "Retrieval in Practice (free PDF)",
         "https://ciir.cs.umass.edu/irbook/",
         "<b>The systems companion, also free.</b> Stronger on "
         "Modules 04, 09, and 10 — crawling, query processing, and "
         "what a production engine actually contains."),
        ("Lin, Nogueira & Yates — Pretrained Transformers for Text "
         "Ranking (free)",
         "https://arxiv.org/abs/2010.06467",
         "<b>Modules 06, 07, and 11, free.</b> The best available "
         "survey of the neural ranking material, and honest about "
         "which gains survived scrutiny."),
        ("Zobel & Moffat — Inverted files for text search engines "
         "(free)",
         "https://dl.acm.org/doi/10.1145/1132956.1132959",
         "<b>Module 02's reference.</b> Everything about index "
         "construction and compression, from the people who measured "
         "it."),
        ("Sanderson — Test Collection Based Evaluation of IR Systems "
         "(free)",
         "https://www.nowpublishers.com/article/Details/INR-009",
         "<b>Module 05's history and its critique</b> — how the "
         "evaluation methodology developed, and what it assumes that is "
         "not true."),
        ("The TREC proceedings, and BEIR (free)",
         "https://trec.nist.gov/",
         "<b>The field's evaluation infrastructure.</b> TREC for the "
         "methodology, BEIR for the zero-shot comparisons Module 07 "
         "relies on."),
    ],
    "tooling": [
        "<b>A lexical search engine you can inspect:</b> "
        "<b><code>Lucene</code> via PyLucene, or "
        "<code>Anserini</code>/<code>Pyserini</code></b>, which is "
        "built for reproducible retrieval experiments and is what "
        "Module 05's exercises use.",
        "<b>And your own inverted index first.</b> <b>Module 02 "
        "requires you to build one</b>, because the compression and the "
        "skip structure are invisible from behind a library "
        "interface.",
        "<b>Python with <code>sentence-transformers</code> and "
        "<code>faiss</code></b> for Modules 07 and 08 — and "
        "<b>read FAISS's index types rather than accepting the "
        "default</b>, which is Module 08 §4's exercise.",
        "<b><code>trec_eval</code>, or <code>ir_measures</code></b> "
        "for Module 05. <b>Use the standard implementation rather than "
        "writing your own metric</b>, because the edge cases are where "
        "the disagreements live.",
        "<b>A collection you care about and will judge "
        "yourself.</b> <b>Project 2 requires hand-made relevance "
        "judgements</b>, and making fifty of them teaches more about "
        "relevance than any reading.",
        "<b>And a latency budget you hold yourself to.</b> "
        "<b>Module 04's point is that a ranking you cannot compute in "
        "time does not exist</b> — so measure the latency from the "
        "first exercise onward.",
    ],
    "projects": [
        {"title": "An index and a ranker, built", "after": 6,
         "brief": "Build an inverted index and a BM25 ranker from "
                  "scratch, and measure both correctness and speed.",
         "reqs": [
             "<b>An inverted index you wrote</b>, with gap encoding "
             "and a compressed postings format "
             "(Module 02 §3).",
             "<b>BM25 implemented from the formula</b>, with the "
             "parameters' effect measured rather than defaulted "
             "(Module 03 §3).",
             "<b>Verified against a reference implementation</b> on "
             "the same collection — <b>the rankings should "
             "match</b>.",
             "<b>Query processing with early termination</b>, and the "
             "speedup measured against exhaustive scoring "
             "(Module 04 §3).",
             "<b>The index size reported</b> against the raw "
             "collection, with the compression attributed to each "
             "technique.",
             "<b>And a latency distribution</b>, at the median and "
             "the 95th percentile.",
         ],
         "done": [
             "<b>The rankings matching the reference</b> — which is "
             "binary, and is how you know the implementation is "
             "right.",
             "<b>The compression attributed per technique</b> rather "
             "than reported as a total, which is what demonstrates "
             "understanding.",
             "<b>The early termination verified safe</b>: <b>the top "
             "k must be identical to exhaustive scoring</b>, or the "
             "optimisation is a bug.",
             "<b>And the latency tail reported</b>, because <b>the "
             "median is not the number that determines whether a search "
             "system is usable.</b>",
         ]},
        {"title": "A search system, honestly evaluated", "after": 12,
         "brief": "Build a search system over a collection you care "
                  "about, and evaluate it as if people depended on it.",
         "reqs": [
             "<b>A collection, and at least thirty queries you wrote "
             "from real information needs</b> — not from the "
             "documents.",
             "<b>Relevance judgements you made yourself</b>, with "
             "your criteria written down before you judged "
             "(Module 05 §2).",
             "<b>A tuned BM25 baseline</b>, which the system has to "
             "beat (Module 05 §4).",
             "<b>Your system — learned ranking, dense "
             "retrieval, or hybrid — with the choice justified "
             "against its cost.</b>",
             "<b>An evaluation with the metric derived from how "
             "results will be used</b>, and the latency reported "
             "alongside.",
             "<b>And an analysis of the twenty worst queries</b>, "
             "with the failure categories drawn from them.",
         ],
         "done": [
             "<b>The queries written from needs rather than from "
             "documents</b> — <b>which is graded first, because a "
             "query derived from a document guarantees that document is "
             "retrievable</b> and the evaluation is then circular.",
             "<b>The judgement criteria written down in "
             "advance</b>, and applied consistently.",
             "<b>The baseline tuned</b>, with its parameters "
             "reported (CSCE 676 Module 13 §2).",
             "<b>And the twenty worst queries read individually</b>, "
             "with categories that came from the failures rather than "
             "from your expectations.",
         ]},
    ],
    "map": [
        ("Manning, Raghavan & Schütze — Introduction to Information "
         "Retrieval (free)",
         "https://nlp.stanford.edu/IR-book/",
         "<b>Modules 01 through 06 and 10.</b> Free in full, and the "
         "chapter order is close to this course's."),
        ("Croft, Metzler & Strohman — Search Engines (free PDF)",
         "https://ciir.cs.umass.edu/irbook/",
         "<b>Modules 04, 09, and 10</b> — the systems half, with "
         "the crawling and query-processing detail the other book "
         "leaves out."),
        ("Lin, Nogueira & Yates — Pretrained Transformers for Text "
         "Ranking (free)",
         "https://arxiv.org/abs/2010.06467",
         "<b>Modules 06, 07, and 11</b>, and the critical assessment "
         "of which reported gains replicated."),
        ("Pyserini and the BEIR benchmark (free)",
         "https://github.com/castorini/pyserini",
         "<b>Modules 05 and 07 practically</b> — reproducible "
         "baselines, which is exactly what Project 2 needs."),
        ("The TREC proceedings (free)",
         "https://trec.nist.gov/",
         "<b>Module 05's methodology in its original form</b>, and "
         "worth reading one track's overview paper end to end."),
        ("Stanford CS276 / CS224U materials (free)",
         "https://web.stanford.edu/class/cs276/",
         "<b>The course this one is shaped against</b>, with "
         "assignments."),
    ],
}

MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "The Information Need",
 "subtitle": "The query is evidence, not a specification.",
 "question": "What is the person actually trying to do?",
 "outcomes": [
     "Distinguish need, query, and document.",
     "Explain the vocabulary mismatch and its consequences.",
     "Explain the kinds of need and why they differ.",
     "Explain why relevance is not a property of a document.",
     "Set up a retrieval problem so it can be evaluated.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Three things",
   "blurb": "Routinely conflated, and the conflation causes the failures."},

  {"t": "table", "kicker": "Distinctions", "title": "Need, query, and document",
   "header": ["", "What it is", "What the system sees"],
   "widths": [2.6, 4.2, 4.6],
   "rows": [
     ["<b>Information need</b>", "<b>What the person wants to know or do</b>", "<b>Nothing — it is never observed</b>"],
     ["<b>Query</b>", "<b>Their attempt to express it in a few words</b>", "<b>This, and only this</b>"],
     ["<b>Document</b>", "<b>Text that may help</b>", "<b>Its words, and whatever else you indexed</b>"],
   ],
   "footnote": "<b>The need is never observed</b>, which is the "
               "governing fact of the field — every metric, every "
               "judgement, and every click is a proxy for something the "
               "system cannot see.",
   "note": "The never-observed point is what makes Module 05 hard."},

  {"t": "callout", "title": "So matching the query well and satisfying the need are different objectives",
   "kind": "The gap the whole course addresses",
   "body": ["<b>A system optimised to match query terms will return "
            "documents containing those terms</b> — which is not the "
            "same as documents that answer the question, and the "
            "divergence is where every failure lives.",
            "<b>And the person knows this, which changes their "
            "behaviour:</b> <b>they phrase queries for the system rather "
            "than for a person</b>, so the query is already a "
            "translation and frequently a bad one.",
            "<b>Which makes the query a noisy, truncated, "
            "strategically-chosen signal</b> — two or three words "
            "standing in for a paragraph of context the system never "
            "gets.",
            "<b>So every technique in this course is an attempt to "
            "recover information the query omitted</b> — from the "
            "collection, from the corpus statistics, from other users' "
            "behaviour, or from a language model."]},

  {"t": "section", "label": "Part 2", "title": "Vocabulary mismatch",
   "blurb": "The oldest problem, and still the central one."},

  {"t": "code", "kicker": "Mismatch", "title": "The forms it takes",
   "lang": "text", "code": """
  SYNONYMY
      the query says "car", the document says
      "automobile". A term match finds nothing.

  POLYSEMY
      the query says "jaguar". Three distinct needs,
      one string, and term matching cannot separate
      them.

  MORPHOLOGY
      "running" and "ran" and "runs". Stemming helps
      and over-stems ("university" -> "univers").

  SPECIFICITY MISMATCH
      the query says "dog illness", the document says
      "canine parvovirus". Neither term appears in
      the other.

  AND THE ASYMMETRY
      the searcher does not know the collection's
      vocabulary -- which is frequently WHY they are
      searching. Expecting them to guess the right
      term is expecting them to already know the
      answer.
""",
   "caption": "<b>The asymmetry is the point</b> — the person "
              "searching is the one least able to choose the right "
              "words.",
   "note": "The asymmetry argument motivates query expansion and dense "
           "retrieval both."},

  {"t": "callout", "title": "Every retrieval advance is an attack on vocabulary mismatch",
   "kind": "The organising view of the course",
   "body": ["<b>Stemming and normalisation</b> "
            "(Module 02) attack morphology, crudely and "
            "cheaply.",
            "<b>Query expansion and relevance "
            "feedback</b> (Module 09) add terms the searcher did "
            "not supply, from the collection or from their own "
            "behaviour.",
            "<b>Latent methods and dense "
            "retrieval</b> (Module 07) <b>represent meaning rather "
            "than words</b>, which addresses synonymy and specificity "
            "directly.",
            "<b>And learned ranking</b> (Module 06) <b>uses "
            "features correlated with relevance that have nothing to do "
            "with term overlap</b> — which is a different attack on "
            "the same problem."]},

  {"t": "section", "label": "Part 3", "title": "Kinds of need",
   "blurb": "Which require different systems."},

  {"t": "table", "kicker": "Intent", "title": "The query intent taxonomy, and what each needs",
   "header": ["Intent", "Example", "What success means"],
   "widths": [2.5, 3.7, 4.8],
   "rows": [
     ["<b>Navigational</b>", "<b>A specific site or document</b>", "<b>One correct result, at rank 1</b>"],
     ["<b>Informational</b>", "<b>Learn about a topic</b>", "<b>Several useful results; diversity helps</b>"],
     ["<b>Transactional</b>", "<b>Do something — buy, download</b>", "<b>A page where the action is possible</b>"],
     ["<b>Exploratory</b>", "<b>Understand a space you do not know</b>", "<b>Coverage and serendipity, over a session</b>"],
   ],
   "footnote": "<b>These need different metrics</b> — reciprocal "
               "rank for navigational, graded gain for informational, and "
               "session-level measures for exploratory, which "
               "Module 05 §3 develops.",
   "note": "Intent determining the metric is the practical "
           "consequence."},

  {"t": "callout", "title": "And relevance is a relation between a document and a need, not a property of the document",
   "kind": "The conceptual point that matters most",
   "body": ["<b>The same document is relevant to one person and "
            "useless to another</b> — depending on what they already "
            "know, what they are trying to do, and what else they have "
            "seen.",
            "<b>So it is contextual, graded, and "
            "dynamic:</b> <b>relevance depends on the session, declines "
            "with redundancy, and is not binary</b> — a partially "
            "useful document is common and is not captured by a "
            "yes/no label.",
            "<b>And it is not transitive or stable.</b> <b>A "
            "document's relevance changes once the user has read a "
            "similar one</b>, which means the relevance of a <i>list</i> "
            "is not the sum of its documents'.",
            "<b>Which is why Module 05 is hard</b> — <b>every "
            "evaluation methodology approximates this with a static, "
            "per-document label</b>, and the approximation is where the "
            "trouble starts."]},

  {"t": "section", "label": "Part 4", "title": "Setting it up",
   "blurb": "So that it can be evaluated at all."},

  {"t": "bullets", "kicker": "Setup", "title": "What to decide before building anything",
   "items": [
     "<b>Write the queries from needs, not from "
     "documents.</b> <b>A query derived from a document guarantees "
     "that document is retrievable</b>, and the evaluation is then "
     "circular (Project 2's first criterion).",
     "",
     "<b>Write down the relevance criteria before judging "
     "anything</b> — because <b>judging first and articulating "
     "afterwards produces criteria that match what you "
     "found.</b>",
     "",
     "<b>Decide how results will be used</b>, since that "
     "determines the metric (Part 3) — one result, ten, "
     "or a session.",
     "",
     "<b>Set the latency budget</b>, because it constrains the "
     "architecture (Module 04).",
     "",
     "<b>And identify the baseline you must beat</b>, which is "
     "BM25 and is harder than it sounds "
     "(Module 05 §4).",
   ],
   "footnote": "<b>Queries from needs rather than documents is the "
               "one that invalidates evaluations</b> — and it is the "
               "easiest mistake to make when building a test set "
               "quickly."},

  {"t": "callout", "title": "How to read this course",
   "kind": "Orientation",
   "body": ["<b>Modules 02 to 04 are the classical "
            "engine</b> — index, scoring, and efficient query "
            "processing, which is still the foundation of every "
            "production system.",
            "<b>Module 05 is the centre</b>, because every later "
            "claim depends on it.",
            "<b>Modules 06 to 09 are the learned and semantic "
            "layer</b> — learning to rank, dense retrieval, vector "
            "search at scale, and query understanding.",
            "<b>And Modules 10 to 13 are web scale, generative "
            "retrieval, consequences, and honest claims</b> — "
            "<b>with Module 12 about what a ranking does to the ranked</b>, "
            "which is not a side issue at scale."]},
 ],
 "takeaways": [
   "The information need is never observed, which is the governing fact of "
   "the field and why every measurement is a proxy.",
   "Matching the query well and satisfying the need are different "
   "objectives, and the divergence is where every failure lives.",
   "The person searching is the one least able to choose the right words, "
   "which is frequently why they are searching.",
   "Every retrieval advance is an attack on vocabulary mismatch, from "
   "stemming through to dense retrieval.",
   "Relevance is a relation between a document and a need rather than a "
   "property of the document, so it is contextual, graded, and dynamic.",
   "Write queries from needs rather than from documents, or the evaluation "
   "is circular.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Three things, routinely conflated"),
  ("table", ["", "What it is", "What the system actually sees"],
   [["<b>Information need</b>",
     "<b>What the person wants to know, or to be able to do.</b>",
     "<b>Nothing at all — it is never observed</b>, at any point, by "
     "any means. See the note."],
    ["<b>Query</b>",
     "<b>Their attempt to express that need in a few words, typed into a "
     "box.</b>",
     "<b>This, and only this</b> — plus whatever context the system "
     "separately holds."],
    ["<b>Document</b>", "<b>Text that may or may not help them.</b>",
     "<b>Its words, and whatever else you chose to index</b> — links, "
     "metadata, click history."]],
   [0.20, 0.38, 0.42]),
  ("p", "<b>The need is never observed</b>, and that is <b>the "
        "governing fact of the entire field</b> — <b>every metric, "
        "every relevance judgement, and every click is a proxy for "
        "something the system cannot see and never will.</b> <b>Which is "
        "what makes Module 05 genuinely hard</b> rather than merely "
        "technical, and is why CSCE 676 Module 13 &sect;3 identifies "
        "this course's proxy as a relevance label standing in for "
        "relevance to a person."),
  ("callout", "So matching the query well and satisfying the need are "
              "different objectives",
   ["<b>A system optimised to match query terms will return documents "
    "containing those terms</b> — which is <b>not the same thing as "
    "returning documents that answer the question</b>, and <b>the "
    "divergence between those two is where every retrieval failure "
    "lives.</b>",
    "<b>And the person knows this, which changes their behaviour:</b> "
    "<b>they phrase their queries for the system rather than for a "
    "person</b> — dropping function words, guessing at keywords, "
    "imitating what has worked before — <b>so the query is already "
    "a translation, and frequently a poor one.</b>",
    "<b>Which makes the query a noisy, truncated, "
    "strategically-chosen signal:</b> two or three words standing in for "
    "a paragraph of context that the system never receives and the user "
    "never thought to supply.",
    "<b>So every technique in this course is an attempt to recover "
    "information the query omitted</b> — <b>from the collection's "
    "statistics, from the corpus's vocabulary, from other users' "
    "behaviour, or from a language model's knowledge</b> — and that "
    "framing makes the course's sequence intelligible."]),

  ("h1", "2 &nbsp; Vocabulary mismatch"),
  ("code", """SYNONYMY
    the query says "car", the document says
    "automobile". A term match finds nothing at all.

POLYSEMY
    the query says "jaguar". Three distinct needs
    behind one string, and term matching cannot
    separate them.

MORPHOLOGY
    "running" and "ran" and "runs". Stemming helps,
    and over-stems ("university" -> "univers",
    "organisation" -> "organ").

SPECIFICITY MISMATCH
    the query says "dog illness", the document says
    "canine parvovirus". Neither term appears in the
    other, and both are correct.

AND THE ASYMMETRY
    the searcher does not know the collection's
    vocabulary -- which is frequently WHY they are
    searching. Expecting them to guess the right term
    is expecting them to already know the answer."""),
  ("p", "<b>The asymmetry is the point of the slide</b>, and it is "
        "worth stating plainly: <b>the person searching is the one least "
        "able to choose the right words</b>, because the words are in the "
        "material they have not read yet. <b>Which motivates query "
        "expansion (Module 09) and dense retrieval (Module 07) "
        "both</b>, and which explains why 'the user should have searched "
        "better' is never an acceptable diagnosis."),
  ("callout", "Every retrieval advance is an attack on vocabulary mismatch",
   ["<b>Stemming and normalisation</b> (Module 02 &sect;2) attack "
    "the morphology row, crudely and very cheaply — and the "
    "over-stemming cost is real, which is why the aggressive stemmers "
    "fell out of favour.",
    "<b>Query expansion and relevance feedback</b> (Module 09) "
    "<b>add terms the searcher did not supply</b>, drawn either from the "
    "collection's co-occurrence statistics or from the user's own "
    "interaction with the first results.",
    "<b>Latent methods and dense retrieval</b> (Module 07) "
    "<b>represent meaning rather than words</b>, which addresses "
    "synonymy and specificity mismatch directly rather than by "
    "substitution — and is the same distributional argument as "
    "CSCE 638 Module 04's.",
    "<b>And learning to rank</b> (Module 06) <b>uses features "
    "correlated with relevance that have nothing whatsoever to do with "
    "term overlap</b> — document quality, link structure, click "
    "history, recency — <b>which is a different attack on the same "
    "problem</b> and is why it was such a large advance."]),

  ("break",),
  ("h1", "3 &nbsp; Kinds of need"),
  ("table", ["Intent", "Example", "What success means"],
   [["<b>Navigational</b>",
     "<b>Find a specific site or document the user already knows "
     "exists.</b>",
     "<b>One correct result, at rank 1.</b> Anything else is a "
     "failure, which makes this the easiest intent to measure."],
    ["<b>Informational</b>", "<b>Learn about a topic.</b>",
     "<b>Several useful results; and diversity among them helps</b>, "
     "because redundancy is nearly worthless."],
    ["<b>Transactional</b>",
     "<b>Do something — buy, download, book, sign up.</b>",
     "<b>A page where the action is actually possible</b> — which is "
     "a property of the page rather than of its text."],
    ["<b>Exploratory</b>",
     "<b>Understand a space the user does not yet know the shape of.</b>",
     "<b>Coverage and serendipity, measured over a session</b> rather "
     "than over a single result list."]],
   [0.19, 0.30, 0.51]),
  ("p", "<b>These need different metrics</b> — reciprocal rank for "
        "navigational, graded cumulative gain for informational, and "
        "session-level measures for exploratory — <b>which "
        "Module 05 &sect;3 develops</b>. <b>Intent determining the "
        "metric is the practical consequence</b> of this taxonomy, and it "
        "is why a single system-wide metric averages over queries that "
        "should be judged by different standards."),
  ("callout", "And relevance is a relation between a document and a need, "
              "not a property of the document",
   ["<b>The same document is relevant to one person and useless to "
    "another</b> — depending on what they already know, what they "
    "are trying to accomplish, what reading level suits them, and what "
    "else they have already seen.",
    "<b>So it is contextual, graded, and dynamic:</b> <b>relevance "
    "depends on the session, declines sharply with redundancy, and is "
    "not binary</b> — <b>a partially useful document is the common "
    "case and is not captured by a yes/no label</b>, which is why graded "
    "judgements exist.",
    "<b>And it is neither transitive nor stable.</b> <b>A document's "
    "relevance changes once the user has read a similar one</b>, which "
    "means <b>the relevance of a <i>list</i> is not the sum of its "
    "documents' individual relevances</b> — a fact that nearly every "
    "metric assumes away (Module 05 &sect;3).",
    "<b>Which is precisely why Module 05 is hard</b> — <b>every "
    "evaluation methodology in the field approximates all of this with a "
    "static, per-document, query-independent-of-session label</b>, and "
    "<b>the approximation is where the trouble starts.</b>"]),

  ("h1", "4 &nbsp; Setting it up, and reading the course"),
  ("ul", ["<b>Write the queries from needs, not from "
          "documents.</b> <b>A query derived from a document guarantees "
          "that document is retrievable</b>, so the evaluation measures "
          "whether you can find the thing you wrote the query from "
          "— <b>which is circular</b>, and is <b>Project 2's first "
          "grading criterion</b> for exactly that reason.",
          "<b>Write down your relevance criteria before judging "
          "anything</b> — because <b>judging first and articulating "
          "the criteria afterwards produces criteria that match what you "
          "happened to find</b>, which is CSCE 676 Module 11's "
          "problem in a judgement setting.",
          "<b>Decide how the results will be used</b>, since that "
          "determines the metric (&sect;3) — one result, ten "
          "results, or a whole session, and each implies a different "
          "measure.",
          "<b>Set the latency budget</b>, because <b>it constrains the "
          "architecture</b> rather than merely the implementation "
          "(Module 04, and the two-stage design of "
          "Module 06 &sect;4).",
          "<b>And identify the baseline you have to beat</b>, which is "
          "a properly tuned BM25 and <b>is considerably harder than it "
          "sounds</b> (Module 05 &sect;4). <b>Queries from needs "
          "rather than documents is the one that invalidates "
          "evaluations</b>, and it is the easiest mistake to make when "
          "assembling a test set quickly."]),
  ("callout", "How to read this course",
   ["<b>Modules 02 to 04 are the classical engine</b> — the "
    "inverted index, the scoring functions and their derivations, and "
    "efficient query processing — <b>which is still the foundation "
    "of every production search system</b>, neural or otherwise.",
    "<b>Module 05 is the centre</b>, because <b>every later claim in "
    "the course depends on it</b>, and because the evaluation "
    "methodology is where the field's assumptions are concentrated.",
    "<b>Modules 06 to 09 are the learned and semantic layer</b> "
    "— learning to rank, dense retrieval, approximate vector search "
    "at scale, and query understanding — each attacking &sect;2's "
    "mismatch from a different direction.",
    "<b>And Modules 10 to 13 are web scale, generative retrieval, "
    "consequences, and honest claims</b> — <b>with Module 12 "
    "about what a ranking does to the things and people being "
    "ranked</b>, <b>which is not a side issue at scale</b> but a "
    "first-order property of a deployed ranking system."]),
 ],
 "resources": [
   ("Manning, Raghavan & Sch&uuml;tze, chapter 1 (free)",
    "https://nlp.stanford.edu/IR-book/",
    "<b>&sect;1 and &sect;2</b>, and the Boolean retrieval starting point "
    "that the rest of the course departs from."),
   ("Broder &mdash; A taxonomy of web search (free)",
    "https://dl.acm.org/doi/10.1145/792550.792552",
    "<b>&sect;3's taxonomy in the original</b> — short, and the "
    "navigational/informational/transactional split still "
    "organises practice."),
   ("Saracevic &mdash; Relevance: A review of the literature (free)",
    "https://onlinelibrary.wiley.com/doi/10.1002/asi.20682",
    "<b>&sect;3's callout, developed at length</b> — relevance as a "
    "relation, with the several decades of argument behind it."),
   ("Furnas et al. &mdash; The vocabulary problem (free)",
    "https://dl.acm.org/doi/10.1145/32206.32212",
    "<b>&sect;2 measured</b> — how rarely two people choose the same "
    "word for the same thing, which is the quantitative basis for the "
    "whole module."),
 ],
 "exercises": [
   "<b>Write five information needs as paragraphs</b>, then write the "
   "query you would type for each.",
   "<b>Compare the two</b> and list what the query omitted.",
   "<b>Ask two people to name one thing</b> and record how often they "
   "agree.",
   "<b>Find a document you need</b> whose vocabulary you had to guess "
   "at.",
   "<b>Classify twenty real queries</b> by intent, and note the ones "
   "that resist classification.",
   "<b>Find a document relevant to one person and useless to "
   "another</b>, and say why.",
   "<b>Judge the same document twice, a week apart</b>, and check "
   "whether you agreed with yourself.",
   "<b>Write your relevance criteria</b> for Project 2's collection, "
   "before judging anything.",
   "<b>Write thirty queries from needs</b> and verify none came from a "
   "document.",
   "<b>Set your latency budget</b> and record it.",
 ],
 "selfcheck": [
   "Distinguish need, query, and document, and say what the system "
   "sees.",
   "Why is the need never observed, and what follows?",
   "Why are matching the query and satisfying the need different?",
   "Name four forms of vocabulary mismatch and the asymmetry.",
   "How does each retrieval advance attack the mismatch?",
   "Name four query intents and what success means for each.",
   "Why does relevance belong to a relation rather than a document?",
   "Why is a list's relevance not the sum of its documents'?",
   "Give five setup decisions, and the one that invalidates "
   "evaluations.",
   "Why is Module 05 the centre of the course?",
 ],
},

]

for _b in ("c670_b2", "c670_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
