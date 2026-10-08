# -*- coding: utf-8 -*-
"""CSCE 628 Computational Biology — original course content."""

COURSE = {
    "code": "CSCE 628",
    "title": "Computational Biology",
    "tagline": "The data is noisy, the truth is often unavailable, and "
               "the algorithm has to say so",
    "term": "Semester 12 (with CSCE 640 and CSCE 717)",
    "prereqs": "CSCE 629 Analysis of Algorithms, especially dynamic "
               "programming; CSCE 633 Machine Learning and CSCE 676 "
               "Data Mining for Modules 10 and 11; no biology is "
               "assumed and Module 01 supplies what is needed",
    "deliverable": "A complete analysis of a public dataset you did "
                   "not generate — with the pipeline versioned and "
                   "reproducible, the multiple testing handled "
                   "explicitly, at least one negative control, and a "
                   "stated account of what the result would look like "
                   "if the finding were an artefact",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "description": [
        "<b>This is an algorithms course whose inputs come from an "
        "experiment somebody else ran.</b> <b>Module 01 establishes "
        "the biology you need and the position the course "
        "takes</b> — <b>which is that the hard part is rarely the "
        "algorithm and is almost always the gap between what was "
        "measured and what is being claimed.</b>",
        "<b>The first half is the classical algorithmic core, and "
        "it is genuinely beautiful.</b> <b>Alignment is dynamic "
        "programming at its clearest</b> (Modules 02 and 03); "
        "<b>indexing and read mapping are where the data volume "
        "forces real engineering</b> (Modules 04 and 05); and "
        "<b>hidden Markov models and RNA folding are dynamic "
        "programming on richer structures</b> (Modules 07 and "
        "08).",
        "<b>The second theme is that every one of these produces a "
        "score, and a score is not a finding.</b> <b>Module 03 is "
        "about what an alignment score means</b> — <b>which requires "
        "a null model</b> — and <b>that question recurs in every "
        "later module</b>, because the whole subject runs on "
        "statistics applied to measurements with structure the null "
        "model does not have.",
        "<b>The third is the one that distinguishes this from a "
        "pure algorithms course.</b> <b>Modules 10 and 11 are about "
        "multiple testing, batch effects, and "
        "confounding</b> — <b>where the computation is easy and the "
        "inference is where everything goes wrong</b> — and "
        "<b>Module 12 is about pipelines, because an unreproducible "
        "result is not a result.</b>",
        "<b>And the closing position is about claims.</b> "
        "<b>Module 13 asks what a computational biology result "
        "establishes</b> — because <b>'we identified a gene "
        "associated with the phenotype' is a statement about a "
        "statistical model applied to a particular cohort</b>, and the "
        "distance between that and the biological claim is the thing "
        "this course is trying to make visible.",
    ],
    "outcomes": [
        "State the biological objects and what is actually "
        "measured.",
        "Derive and implement sequence alignment algorithms.",
        "Explain alignment scores, null models, and significance.",
        "Explain indexing and heuristic database search.",
        "Explain read mapping and assembly, and where they fail.",
        "Build multiple alignments and phylogenies, with their "
        "error.",
        "Apply hidden Markov models to biological sequence.",
        "Predict RNA structure by dynamic programming.",
        "Explain protein structure prediction and what changed.",
        "Analyse expression data with multiple testing handled.",
        "Explain association studies and their confounders.",
        "Build a reproducible pipeline, and say why it matters.",
        "Claim a biological result honestly.",
    ],
    "materials": [
        ("Durbin, Eddy, Krogh & Mitchison — Biological Sequence "
         "Analysis",
         "https://www.cambridge.org/9780521629713",
         "<b>The primary text for Modules 02 through 08.</b> Probabilistic "
         "models of sequence, done properly, and the HMM chapters are "
         "the best treatment anywhere. Library copy."),
        ("Jones & Pevzner — An Introduction to Bioinformatics "
         "Algorithms",
         "https://mitpress.mit.edu/9780262101066/",
         "<b>Modules 02, 04, 05, and 08.</b> Algorithm-first, with the "
         "biology supplied as needed — which suits this course's "
         "audience exactly. Library copy."),
        ("Compeau & Pevzner — Bioinformatics Algorithms, with the "
         "free Rosalind problems",
         "https://rosalind.info/",
         "<b>The exercises for Modules 02 through 08, free.</b> "
         "Implementing these is the fastest way to find out whether you "
         "understood the recurrence."),
        ("Lander & Weinberg and the open genomics literature (free)",
         "https://www.ncbi.nlm.nih.gov/pmc/",
         "<b>Module 01's biology and Modules 10 to 13's practice.</b> "
         "PubMed Central is open access and is where the methods "
         "sections actually are."),
        ("Leek & Storey, and the batch effects literature (free)",
         "https://www.nature.com/articles/nrg2825",
         "<b>Module 10.</b> Why a large fraction of published "
         "expression findings were batch structure, and what to do "
         "about it."),
        ("The Bioconductor and Biopython documentation (free)",
         "https://bioconductor.org/",
         "<b>Modules 10 and 12.</b> The standard tooling, and "
         "Bioconductor's statistical packages encode a great deal of "
         "hard-won practice."),
    ],
    "tooling": [
        "<b>Python with <code>biopython</code>, or R with "
        "Bioconductor</b> — <b>and R for anything statistical</b>, "
        "because <b>the multiple-testing and differential-expression "
        "methods of Module 10 are implemented correctly "
        "there</b> and are easy to reimplement incorrectly.",
        "<b>But implement the core algorithms yourself "
        "first</b> — <b>Needleman-Wunsch, Viterbi, and Nussinov are "
        "each under fifty lines</b>, and <b>calling a library before "
        "writing one leaves the recurrence "
        "unlearned</b> (Project 1).",
        "<b>Public data, and plenty of it</b> — <b>NCBI, Ensembl, "
        "UniProt, GEO, and the 1000 Genomes data are all "
        "free</b> — and <b>Project 2 requires a dataset you did not "
        "generate</b>, which is the realistic case.",
        "<b>A workflow manager</b> — <b>Snakemake or "
        "Nextflow</b> — and <b>Module 12 §2 explains why a shell "
        "script is not sufficient</b> once a reference genome version "
        "is involved.",
        "<b>Containers, and a pinned environment</b>, because "
        "<b>'it worked last year' is the characteristic failure "
        "here</b> and the tools move faster than the papers.",
        "<b>And a negative control, always</b> — <b>permuted "
        "labels, a scrambled sequence, a known-null "
        "comparison</b> — which is <b>Module 13 §2's requirement and "
        "the cheapest insurance in the course.</b>",
    ],
    "projects": [
        {"n": 1, "after": 6,
         "title": "Write the alignment engine",
         "brief": "Implement the core algorithms, and find out what "
                  "the scores actually mean.",
         "reqs": [
           "<b>Global and local alignment implemented from the "
           "recurrence</b> — Needleman-Wunsch and "
           "Smith-Waterman — <b>with affine gap penalties</b>, and "
           "with traceback.",
           "<b>Verified against a library implementation</b> on "
           "the same inputs, with any disagreement explained rather "
           "than patched.",
           "<b>A substitution matrix used and its effect "
           "measured</b> (Module 03) — the same pair aligned under "
           "two matrices, and the difference "
           "reported.",
           "<b>An empirical null distribution</b>: <b>align "
           "shuffled sequences several thousand times and plot the "
           "score distribution</b>.",
           "<b>Then report where your real alignment's score falls "
           "in it</b>, as a measured rather than an assumed "
           "significance.",
           "<b>And the runtime measured against sequence length</b>, "
           "with the quadratic confirmed.",
         ],
         "done": [
           "<b>The empirical null built and used</b> — <b>which "
           "is the point of the project</b>, because <b>a score without "
           "a null is not interpretable</b> (Module 03 §2).",
           "<b>The affine gap recurrence correct</b>, which is "
           "where implementations usually break — and the three-"
           "matrix formulation is the one to get right.",
           "<b>The two substitution matrices giving different "
           "alignments</b>, reported as a finding about the method "
           "rather than as a nuisance.",
           "<b>And the disagreement with the library "
           "explained</b> — <b>usually it is a tie-breaking or a "
           "gap-at-the-end convention</b>, and tracking it down teaches "
           "more than agreement would.",
         ]},
        {"n": 2, "after": 12,
         "title": "A real dataset, honestly analysed",
         "brief": "Take public data you did not generate, and find "
                  "out what it will and will not support.",
         "reqs": [
           "<b>A public dataset you did not generate</b> — "
           "expression, variants, or sequence — <b>with its "
           "original paper read</b>, including the methods "
           "section.",
           "<b>A reproducible pipeline</b> (Module 12): "
           "<b>pinned versions, a named reference build, and a "
           "single command that reruns everything</b>.",
           "<b>Multiple testing handled explicitly</b> "
           "(Module 10 §3) — <b>with the number of tests "
           "stated and the correction named</b>.",
           "<b>At least one negative control</b>: <b>permuted "
           "labels, or a comparison that should produce "
           "nothing</b> — and its result reported whatever it "
           "is.",
           "<b>The batch and confounding structure examined</b> "
           "(Modules 10 §4, 11 §2) — or stated as "
           "unexaminable from the available metadata, which is a common "
           "and honest finding.",
           "<b>And the honest claim</b> in Module 13 §3's form, "
           "including what the result would look like if it were an "
           "artefact.",
         ],
         "done": [
           "<b>The negative control run and reported</b> — "
           "<b>a project with no negative control fails</b>, whatever it "
           "found, for Module 13 §2's reasons.",
           "<b>The pipeline rerunnable by somebody else</b>, from "
           "the repository, which is tested rather than "
           "asserted.",
           "<b>The multiple testing count honest</b> — "
           "<b>including the tests you ran and discarded</b>, which is "
           "the part everybody omits (Module 10 §3).",
           "<b>And the artefact account specific</b>: <b>'if this "
           "were batch structure it would look like X, and here is "
           "whether it does'</b> — which is the analytical skill "
           "the whole course is aimed at.",
         ]},
    ],
    "map": [
        ("Durbin et al. (library copy)",
         "https://www.cambridge.org/9780521629713",
         "<b>Modules 02, 03, 06, 07, and 08.</b> The probabilistic "
         "treatment, and the HMM chapters are definitive."),
        ("Rosalind problems (free)",
         "https://rosalind.info/problems/locations/",
         "<b>Modules 02 to 08's exercises</b>, free, with automatic "
         "checking — and the ordering is well designed."),
        ("NCBI handbooks and BLAST documentation (free)",
         "https://www.ncbi.nlm.nih.gov/books/NBK143764/",
         "<b>Modules 03 and 04.</b> What an E-value is, from the people "
         "who compute it."),
        ("The Bioconductor workflows (free)",
         "https://bioconductor.org/packages/release/BiocViews.html#___Workflow",
         "<b>Modules 10 and 12.</b> End-to-end analyses with the "
         "statistical reasoning included."),
        ("Nature Reviews Genetics, the methods reviews (library)",
         "https://www.nature.com/nrg/",
         "<b>Modules 09, 10, and 11.</b> The review literature is where "
         "the field's self-criticism is, and it is worth reading for "
         "that alone."),
        ("The Reproducibility literature in biology (free)",
         "https://www.nature.com/collections/prbfkwmwvz",
         "<b>Modules 12 and 13.</b> What failed to replicate, and the "
         "analyses of why."),
    ],
}

MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "What Is Actually Measured",
 "subtitle": "The biology you need, and the gap this course is about.",
 "question": "What did the machine actually produce?",
 "outcomes": [
     "State the molecular objects and the central dogma.",
     "Describe what the common measurement technologies output.",
     "Explain the gap between measurement and biological claim.",
     "Explain why ground truth is usually unavailable.",
     "State this course's position.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The objects",
   "blurb": "Four molecules and one flow of information."},

  {"t": "table", "kicker": "Objects", "title": "What the strings in this course represent",
   "header": ["Object", "Alphabet", "What it is"],
   "widths": [2.5, 2.6, 5.9],
   "rows": [
     ["<b>DNA</b>", "<b>A C G T</b>", "<b>The stored sequence; double-stranded and complementary</b>"],
     ["<b>RNA</b>", "<b>A C G U</b>", "<b>A transcribed copy; also folds and acts (M08)</b>"],
     ["<b>Protein</b>", "<b>20 amino acids</b>", "<b>Translated from RNA; folds into a shape (M09)</b>"],
     ["<b>Gene</b>", "<b>—</b>", "<b>A region that is transcribed; the definition is contested</b>"],
     ["<b>Genome</b>", "<b>—</b>", "<b>The whole sequence; 3 billion bases in a human</b>"],
   ],
   "footnote": "<b>DNA → RNA → protein is the central dogma</b>, "
               "and <b>every arrow has exceptions</b> — which is a "
               "good introduction to how biology's rules "
               "work.",
   "note": "The alphabet sizes are what make the algorithms behave "
           "as they do."},

  {"t": "callout", "title": "Which is enough biology to start, and the exceptions matter later",
   "kind": "What this course assumes and supplies",
   "body": ["<b>Most of this course is string algorithms and "
            "statistics</b> — <b>so the biology needed is the "
            "vocabulary and the measurement model</b>, both of which "
            "this module supplies.",
            "<b>But the exceptions are where the errors "
            "live:</b> <b>genes overlap, are spliced into multiple "
            "products, and are defined differently by different "
            "annotations</b> — so <b>'the gene' is frequently "
            "ambiguous.</b>",
            "<b>And the reference genome is a "
            "construct</b> — <b>assembled from a few individuals, "
            "revised repeatedly, and not any particular person's "
            "sequence</b> — which has consequences in "
            "Module 12 §2.",
            "<b>So the rule is to look up what you are assuming "
            "rather than to learn biology in advance</b> — and "
            "<b>the assumption to check first is always 'which version "
            "of which annotation'.</b>"]},

  {"t": "section", "label": "Part 2", "title": "What the instruments produce",
   "blurb": "Which is further from the biology than people assume."},

  {"t": "code", "kicker": "Measurement", "title": "The common technologies and their actual output",
   "lang": "text", "code": """
  SHORT-READ SEQUENCING
      output: millions of 100-300 base fragments,
      each with per-base quality scores, from random
      positions, with PCR duplicates and errors.
      NOT a genome. Assembly or mapping comes next
      (Module 05).

  LONG-READ SEQUENCING
      tens of kilobases, higher error rate, better
      across repeats. Different trade, same shape.

  RNA SEQUENCING
      reads from transcripts, counted per gene.
      The count depends on expression AND on length,
      AND on the library prep. Normalisation is not
      optional (Module 10).

  MICROARRAYS AND MASS SPEC
      intensities and spectra -- analogue signals
      with their own calibration problems.

  IN EVERY CASE THE OUTPUT IS COUNTS OR INTENSITIES,
  and the biological quantity is inferred from them.
""",
   "caption": "<b>In every case the output is counts or intensities, "
              "and the biological quantity is inferred</b> — which "
              "is the gap this course keeps "
              "returning to.",
   "note": "Knowing what the instrument emits prevents most "
           "interpretation errors."},

  {"t": "section", "label": "Part 3", "title": "The gap",
   "blurb": "Between the measurement and the claim."},

  {"t": "callout", "title": "Every result in this field is a chain of inferences, and the chain is usually reported as a single step",
   "kind": "The course's organising observation",
   "body": ["<b>'Gene X is upregulated in disease' "
            "means:</b> <b>reads mapped to an annotation, counted, "
            "normalised, modelled, and tested</b> — <b>five steps, "
            "each with choices, applied to tissue from a particular set "
            "of people.</b>",
            "<b>And each step has defensible alternatives that "
            "change the answer</b> — <b>different aligners, "
            "annotations, normalisations, and models give overlapping "
            "but different gene lists.</b>",
            "<b>Which is not a scandal</b> — <b>it is what analysis "
            "of noisy data looks like</b> — <b>and it is a reason to "
            "report the chain rather than the conclusion "
            "alone.</b>",
            "<b>So this course's habit is to name the chain</b>, "
            "every time — which is <b>CSCE 679 §13's five-clause "
            "caption</b> and <b>CSCE 676 §13's proxy problem</b>, "
            "arriving in a field where the stakes are "
            "medical."]},

  {"t": "section", "label": "Part 4", "title": "No ground truth",
   "blurb": "Which is the structural difficulty of the subject."},

  {"t": "bullets", "kicker": "Validation", "title": "Why you usually cannot check your answer",
   "items": [
     "<b>A sorting algorithm's output is checkable in linear "
     "time</b> — <b>an inferred gene function is not checkable at "
     "all without an experiment</b> that may take years.",
     "",
     "<b>So the field validates by proxy</b>: <b>agreement with "
     "other methods, known positive controls, held-out data, and "
     "eventual experimental follow-up</b> — each partial.",
     "",
     "<b>And agreement between methods is weak evidence</b> when "
     "<b>the methods share assumptions</b>, which they usually do "
     "(CSCE 676 §11's multiplicity "
     "problem).",
     "",
     "<b>Which makes negative controls disproportionately "
     "valuable</b> — <b>a permutation that should find nothing "
     "and does is the strongest cheap evidence "
     "available.</b>",
     "",
     "<b>And it is why Project 2 requires one</b>, and fails "
     "without it.",
   ],
   "footnote": "<b>A permutation that should find nothing and does "
               "find nothing is the strongest cheap evidence "
               "available</b> — and it costs one rerun with shuffled "
               "labels."},

  {"t": "callout", "title": "So the position this course takes",
   "kind": "Closing",
   "body": ["<b>The algorithms are the easy part and they are worth "
            "learning properly</b> — <b>Modules 02 to 09 are "
            "genuinely beautiful dynamic programming</b>, and this "
            "course does not short them.",
            "<b>And the inference is where the errors are</b> — "
            "<b>Modules 10 to 12 are about multiple testing, "
            "confounding, and reproducibility</b>, which is where "
            "published findings actually fail.",
            "<b>Plus the honest acknowledgement:</b> <b>large "
            "fractions of published findings in several subfields have "
            "failed to replicate</b>, and <b>the causes are "
            "statistical and procedural rather than "
            "biological.</b>",
            "<b>Which is why Module 13 exists</b> — <b>'we "
            "found an association' is a claim about a model and a "
            "cohort</b>, and the distance to the biological claim is "
            "what this course makes visible."]},
 ],
 "takeaways": [
   "DNA to RNA to protein is the central dogma, and every arrow has "
   "exceptions.",
   "The reference genome is a construct assembled from a few individuals, "
   "not any particular person's sequence.",
   "Sequencing outputs millions of short fragments with errors and "
   "duplicates — not a genome.",
   "In every technology the output is counts or intensities, and the "
   "biological quantity is inferred from them.",
   "Every result is a chain of inferences reported as a single step, and "
   "each step has defensible alternatives that change the answer.",
   "A permutation that should find nothing and does find nothing is the "
   "strongest cheap evidence available.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The objects"),
  ("table", ["Object", "Alphabet", "What it is"],
   [["<b>DNA</b>", "<b>A C G T</b>",
     "<b>The stored sequence</b>; double-stranded and complementary, so "
     "a read may come from either strand — which matters for every "
     "mapping algorithm."],
    ["<b>RNA</b>", "<b>A C G U</b>",
     "<b>A transcribed copy of a region</b>; <b>it also folds and acts "
     "catalytically or regulatorily</b> (Module 08)."],
    ["<b>Protein</b>", "<b>20 amino acids</b>",
     "<b>Translated from RNA in triplets</b>; <b>folds into a "
     "three-dimensional shape that determines what it does</b> "
     "(Module 09)."],
    ["<b>Gene</b>", "<b>&mdash;</b>",
     "<b>A region that is transcribed</b> — and <b>the definition "
     "is genuinely contested</b>, which has practical consequences "
     "(see the callout)."],
    ["<b>Genome</b>", "<b>&mdash;</b>",
     "<b>The whole sequence of an organism</b>; roughly three billion "
     "bases in a human, of which the protein-coding part is a small "
     "percentage."]],
   [0.16, 0.20, 0.64]),
  ("p", "<b>DNA &rarr; RNA &rarr; protein is the central dogma</b>, "
        "<b>and every arrow has exceptions</b> — reverse "
        "transcription, RNA that is never translated, proteins that "
        "modify other proteins — <b>which is a good introduction to "
        "how biology's rules work</b>: they are strong regularities with "
        "important exceptions, rather than axioms. <b>The alphabet sizes "
        "are what make the algorithms behave as they do</b>: a "
        "four-letter alphabet means random matches are common, which is "
        "Module 03's whole problem."),
  ("callout", "Which is enough biology to start, and the exceptions matter "
              "later",
   ["<b>Most of this course is string algorithms and "
    "statistics</b> — <b>so the biology you need is the vocabulary "
    "and the measurement model</b>, <b>both of which this module "
    "supplies</b>, and the rest can be looked up when a specific "
    "question arises.",
    "<b>But the exceptions are where the errors live:</b> <b>genes "
    "overlap, are spliced into multiple distinct products, sit inside "
    "the introns of other genes, and are defined differently by "
    "different annotation projects</b> — so <b>'the gene' is "
    "frequently ambiguous</b> and two analyses can disagree without "
    "either being wrong.",
    "<b>And the reference genome is a construct</b> — "
    "<b>assembled from a small number of individuals, revised "
    "repeatedly, and not any particular person's actual "
    "sequence</b> — <b>which has direct consequences in "
    "Module 12 &sect;2</b>, where coordinates from one build silently "
    "mean something else in another.",
    "<b>So the rule for this course is to look up what you are "
    "assuming rather than to learn biology in advance</b> — and "
    "<b>the assumption to check first is always 'which version of which "
    "annotation'</b>, which is the single most common source of a "
    "result that cannot be reproduced."]),

  ("h1", "2 &nbsp; What the instruments produce"),
  ("code", """SHORT-READ SEQUENCING
    output: millions of 100-300 base fragments, each
    with per-base quality scores, from roughly
    random positions, with PCR duplicates and
    errors. NOT a genome. Assembly or mapping comes
    next (Module 05).

LONG-READ SEQUENCING
    tens of kilobases per read, higher per-base
    error rate, far better across repeats.
    Different trade, same shape of output.

RNA SEQUENCING
    reads drawn from transcripts, counted per gene.
    The count depends on expression AND on transcript
    length AND on the library preparation.
    Normalisation is not optional (Module 10).

MICROARRAYS AND MASS SPECTROMETRY
    intensities and spectra -- analogue signals with
    their own calibration and saturation problems.

IN EVERY CASE THE OUTPUT IS COUNTS OR INTENSITIES,
and the biological quantity is inferred from them."""),
  ("p", "<b>In every case the output is counts or intensities, and "
        "the biological quantity is inferred</b> — <b>which is the "
        "gap this course keeps returning to</b> (&sect;3). <b>Knowing "
        "what the instrument actually emits prevents most interpretation "
        "errors</b>: an RNA-seq count is not a concentration, a read is "
        "not a position, and an intensity is not an amount. Each of "
        "those four-word corrections has a literature behind it."),

  ("break",),
  ("h1", "3 &nbsp; The gap"),
  ("callout", "Every result in this field is a chain of inferences, and the "
              "chain is usually reported as a single step",
   ["<b>'Gene X is upregulated in disease' means:</b> <b>reads were "
    "mapped to a particular annotation of a particular reference build, "
    "counted per feature, normalised by some method, modelled under some "
    "distributional assumption, and tested</b> — <b>five steps, "
    "each involving choices, applied to tissue from a particular set of "
    "people at a particular time.</b>",
    "<b>And each step has defensible alternatives that change the "
    "answer</b> — <b>different aligners, annotations, "
    "normalisation methods, and statistical models produce overlapping "
    "but genuinely different gene lists</b> from identical raw "
    "data.",
    "<b>Which is not a scandal</b> — <b>it is what analysis of "
    "noisy, high-dimensional data looks like</b> — <b>and it is a "
    "reason to report the chain rather than the conclusion alone</b>, so "
    "that a reader can tell which choices the finding depends on.",
    "<b>So this course's habit is to name the chain, every "
    "time</b> — which is <b>CSCE 679 Module 13's five-clause "
    "caption</b> and <b>CSCE 676 Module 13's proxy problem</b>, "
    "<b>arriving in a field where the stakes are medical</b> and the "
    "downstream reader is frequently not an analyst."]),

  ("h1", "4 &nbsp; No ground truth"),
  ("ul", ["<b>A sorting algorithm's output is checkable in linear "
          "time</b>; <b>an inferred gene function is not checkable at "
          "all without an experiment</b> that may take years and cost a "
          "great deal — which is a structural difference from every "
          "other algorithms course in this program.",
          "<b>So the field validates by proxy</b>: <b>agreement "
          "with other computational methods, recovery of known positive "
          "controls, performance on held-out data, and eventual "
          "experimental follow-up</b> — <b>each of which is "
          "partial</b> and none of which is the checkable answer.",
          "<b>And agreement between methods is weak evidence when "
          "the methods share assumptions</b>, <b>which they usually "
          "do</b> — two aligners built on the same scoring model "
          "agreeing tells you less than it appears to (CSCE 676 "
          "Module 11's multiplicity argument).",
          "<b>Which makes negative controls disproportionately "
          "valuable</b> — <b>a permutation that should find nothing "
          "and does find nothing is the strongest cheap evidence "
          "available</b>, because it tests the whole pipeline including "
          "the parts you did not think about.",
          "<b>And it is why Project 2 requires one and fails without "
          "it</b> — <b>it costs one rerun with shuffled "
          "labels</b>, and it catches a class of error that no amount of "
          "careful reasoning does (Module 13 &sect;2)."]),
  ("callout", "So the position this course takes",
   ["<b>The algorithms are the easy part, and they are worth "
    "learning properly</b> — <b>Modules 02 through 09 are "
    "genuinely beautiful dynamic programming and probabilistic "
    "modelling</b>, and <b>this course does not short them</b> or treat "
    "them as background to the statistics.",
    "<b>And the inference is where the errors are</b> — "
    "<b>Modules 10 through 12 are about multiple testing, confounding, "
    "batch structure, and reproducibility</b>, <b>which is where "
    "published findings actually fail</b> rather than where they are "
    "usually scrutinised.",
    "<b>Plus the honest acknowledgement:</b> <b>large fractions of "
    "published findings in several subfields have failed to "
    "replicate</b>, and <b>the causes are statistical and procedural "
    "rather than biological</b> — which is simultaneously "
    "discouraging and encouraging, since procedural causes are "
    "fixable.",
    "<b>Which is why Module 13 exists</b> — <b>'we found an "
    "association' is a claim about a statistical model applied to a "
    "particular cohort</b>, <b>and the distance between that and the "
    "biological claim is exactly what this course is trying to make "
    "visible.</b>"]),
 ],
 "resources": [
   ("The NCBI Science Primer and handbooks (free)",
    "https://www.ncbi.nlm.nih.gov/books/NBK143764/",
    "<b>&sect;1</b> — the biology vocabulary, at the level this "
    "course needs and no more."),
   ("Scitable and the open genetics primers (free)",
    "https://www.nature.com/scitable/topic/genetics-5/",
    "<b>&sect;1's exceptions</b> — splicing, overlapping genes, and "
    "why 'the gene' is contested."),
   ("Illumina and PacBio technology overviews (free)",
    "https://www.illumina.com/science/technology/next-generation-sequencing.html",
    "<b>&sect;2</b> — what the instruments do, from the "
    "manufacturers, read for the mechanism rather than the "
    "marketing."),
   ("Ioannidis &mdash; Why most published research findings are false "
    "(free)",
    "https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124",
    "<b>&sect;4 and the closing callout</b> — the argument, which is "
    "statistical and applies directly to Modules 10 and 11."),
 ],
 "exercises": [
   "<b>Write out the central dogma</b> and find one exception to each "
   "arrow.",
   "<b>Look up one gene in two annotation sources</b> and compare "
   "their coordinates.",
   "<b>Find out which reference build</b> a dataset you can access "
   "used.",
   "<b>Download a FASTQ file</b> and look at the quality scores.",
   "<b>Count the duplicate reads</b> in it.",
   "<b>Describe the output of three technologies</b> in your own "
   "words.",
   "<b>Take one published sentence of the form 'gene X is "
   "upregulated'</b> and enumerate the inference chain behind it.",
   "<b>Find two papers analysing the same public dataset</b> and "
   "compare their gene lists.",
   "<b>Design a negative control</b> for an analysis you might "
   "run.",
   "<b>State what this course assumes about biology</b>, and what it "
   "does not.",
 ],
 "selfcheck": [
   "Name the four objects and their alphabets.",
   "State the central dogma, and why its exceptions matter.",
   "Why is 'the gene' ambiguous, and what should you check first?",
   "What is the reference genome, actually?",
   "Describe what short-read sequencing outputs.",
   "Why is RNA-seq normalisation not optional?",
   "What is the one thing true of every technology's output?",
   "Enumerate the five steps behind an upregulation claim.",
   "Why is agreement between methods weak evidence?",
   "Why are negative controls disproportionately valuable?",
 ],
},

]

for _b in ("c628_b2", "c628_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
