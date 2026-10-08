# -*- coding: utf-8 -*-
"""CSCE 638 Natural Language Processing — original course content."""

COURSE = {
    "code": "CSCE 638",
    "title": "Natural Language Processing",
    "tagline": "Computing over a signal that carries meaning and does "
               "not carry structure",
    "term": "Semester 10 (with CSCE 676 and CSCE 670)",
    "prereqs": "CSCE 633 Machine Learning and CSCE 636 Deep Learning, "
               "both assumed throughout; CSCE 605 Compiler Design for "
               "the parsing material; CSCE 670 runs in parallel and "
               "shares Module 11",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A working language system on a task you chose, with "
                   "a baseline it beats, an evaluation that measures the "
                   "thing you care about rather than the thing that is "
                   "easy, and a written account of the inputs on which "
                   "it fails",
    "description": [
        "<b>Language is a hard input because it is discrete, "
        "compositional, ambiguous at every level, and its structure is "
        "not given.</b> <b>Module 01 establishes those four properties "
        "properly</b>, because every technique in the course is a "
        "response to one of them — subword tokenisation to "
        "discreteness, attention to composition, context to ambiguity, "
        "and pretraining to the missing structure.",
        "<b>The course follows the actual historical arc, because the "
        "arc is the argument.</b> <b>Counting, then learned dense "
        "representations, then recurrence, then attention, then "
        "pretraining at scale</b> — and <b>each step removed a "
        "specific limitation that the previous step had made "
        "visible</b>, which is a more useful thing to understand than "
        "any single architecture.",
        "<b>The second theme is that evaluation is the hard part and "
        "is routinely the weakest part of a language system.</b> "
        "<b>Module 10 is about why the standard metrics mislead</b> "
        "— <b>a score that correlates poorly with the judgement you "
        "actually care about is worse than no score</b>, because it "
        "directs a year of work. This is CSCE 633 Module 12's "
        "argument, in the setting where it does the most damage.",
        "<b>The third is that these systems fail in ways that matter "
        "to people.</b> <b>Module 12 covers bias, distributional "
        "failure, and confident fabrication</b> — not as an "
        "appendix, but because <b>a system that produces fluent wrong "
        "answers is more dangerous than one that produces obviously "
        "wrong answers</b>, and fluency is exactly what these models "
        "optimise.",
        "<b>And the closing position is about what these systems "
        "do.</b> <b>Module 13 is about stating that honestly</b> "
        "— <b>a model that predicts the next token extremely well "
        "has demonstrated that, and nothing more</b>, and the gap "
        "between that claim and the claims commonly made about such "
        "models is where this course asks you to be careful.",
    ],
    "outcomes": [
        "Explain the four properties that make language hard.",
        "Tokenise and represent text, and explain what each choice "
        "costs.",
        "Build and evaluate a language model.",
        "Explain distributional word representations and their "
        "limits.",
        "Explain recurrence, its failure mode, and what attention "
        "fixed.",
        "Explain the transformer completely.",
        "Explain pretraining and why transfer works here.",
        "Adapt a pretrained model to a task under real "
        "constraints.",
        "Explain decoding and why the strategy changes the output.",
        "Evaluate a language system honestly.",
        "Build a retrieval-augmented system and explain its "
        "failures.",
        "Explain bias, distributional failure, and fabrication.",
        "State what a language model's performance establishes.",
    ],
    "materials": [
        ("Jurafsky & Martin — Speech and Language Processing, 3rd "
         "edition (free draft)",
         "https://web.stanford.edu/~jurafsky/slp3/",
         "<b>The primary text, free in full from the authors, and the "
         "best book in the field.</b> It covers the classical and the "
         "neural material with equal care, which is unusual and is "
         "exactly what this course needs."),
        ("Eisenstein — Introduction to Natural Language Processing "
         "(free draft)",
         "https://github.com/jacobeisenstein/gt-nlp-class",
         "<b>The rigorous companion.</b> Stronger on the learning "
         "theory and the structured prediction material, and free as a "
         "draft PDF."),
        ("Goldberg — Neural Network Methods for NLP",
         "https://link.springer.com/book/10.1007/978-3-031-02165-7",
         "<b>Modules 04 through 06.</b> Written before the "
         "transformer took over and consequently much clearer about "
         "<i>why</i> each architectural choice was made. Library "
         "copy."),
        ("The Illustrated Transformer, and The Annotated Transformer "
         "(free)",
         "https://jalammar.github.io/illustrated-transformer/",
         "<b>Module 06 twice over</b> — once as a diagram and once "
         "as working code. Read the illustrated version first, then "
         "implement from the annotated one."),
        ("Bender et al. and the model-documentation literature "
         "(free)",
         "https://dl.acm.org/doi/10.1145/3442188.3445922",
         "<b>Modules 12 and 13.</b> The paper that framed the "
         "scale-and-harm argument, plus the model card and datasheet "
         "practices that came out of it."),
        ("Hugging Face course and documentation (free)",
         "https://huggingface.co/learn/nlp-course",
         "<b>The practical toolchain for Modules 07 through 11</b> "
         "— free, current, and the implementations every exercise "
         "in the second half uses."),
    ],
    "tooling": [
        "<b>Python with PyTorch</b>, continuing from CSCE 636 "
        "— <b>and the exercises assume you can still write a "
        "training loop by hand</b>, because Module 05's "
        "gradient behaviour is only visible from inside one.",
        "<b>Hugging Face <code>transformers</code>, "
        "<code>tokenizers</code>, and <code>datasets</code></b> for "
        "Modules 07 onward. <b>Read the tokeniser library's output "
        "rather than trusting it</b>, which is Module 02 "
        "§4's exercise.",
        "<b><code>spaCy</code> or <code>stanza</code></b> for the "
        "classical pipeline in Modules 01 through 03 — "
        "<b>worth using once to see what a parser produces</b>, even "
        "though you will not build one.",
        "<b>A GPU, or free hosted notebooks.</b> <b>Every exercise "
        "is sized for a single modest GPU or a free tier</b>, and "
        "Module 08's parameter-efficient methods exist "
        "partly so that this is possible.",
        "<b>A small pretrained model you can fine-tune in "
        "minutes</b> — <b>the pedagogy requires iteration speed more "
        "than capability</b>, so prefer the smallest model that shows "
        "the effect.",
        "<b>And a held-out test set you look at once.</b> "
        "<b>Module 10 §1's discipline is the one habit from "
        "this course most worth keeping</b>, and it has to be set up "
        "before you start rather than after.",
    ],
    "projects": [
        {"title": "A language model, built and probed", "after": 6,
         "brief": "Build a language model from counting through to "
                  "attention, and measure what each step bought.",
         "reqs": [
             "<b>An n-gram model with smoothing</b>, evaluated by "
             "perplexity on held-out text "
             "(Module 03 §2).",
             "<b>A neural language model</b> with learned embeddings, "
             "compared on the same held-out set.",
             "<b>A recurrent model</b>, and <b>a demonstration of its "
             "long-range failure</b> (Module 05 §2) on a "
             "task you construct.",
             "<b>A single attention layer added</b>, and the same task "
             "re-measured.",
             "<b>A written account of what each step bought</b>, with "
             "the numbers and with the cases that changed.",
             "<b>And three inputs your best model handles badly</b>, "
             "with an explanation of why.",
         ],
         "done": [
             "<b>All four models evaluated on the identical held-out "
             "split</b>, which is the only way the comparison means "
             "anything.",
             "<b>The long-range failure demonstrated rather than "
             "asserted</b> — <b>you constructed a task that "
             "isolates it</b>, and that construction is graded "
             "hardest.",
             "<b>The improvements attributed correctly</b>, including "
             "where a step bought you nothing, which happens and should "
             "be reported.",
             "<b>And the three failures explained mechanically</b>, "
             "not as 'the model is imperfect'.",
         ]},
        {"title": "A language system, honestly evaluated", "after": 12,
         "brief": "Build a system for a task you care about, and "
                  "evaluate it as if somebody were going to rely on it.",
         "reqs": [
             "<b>A task and a stated decision it supports</b> — "
             "<b>what would someone do differently</b> given the "
             "output?",
             "<b>A baseline that is genuinely hard to "
             "beat</b> — <b>majority class, retrieval, or a "
             "well-tuned simple model</b>, not a strawman "
             "(Module 10 §2).",
             "<b>Your system, with the adaptation method justified</b> "
             "against its cost (Module 08).",
             "<b>An evaluation measuring the thing you care "
             "about</b>, with the metric's correlation to that thing "
             "argued rather than assumed.",
             "<b>An error analysis by category</b>, with at least "
             "twenty errors read individually.",
             "<b>And a failure and limitation statement</b> covering "
             "distribution shift, bias, and fabrication "
             "(Module 12).",
         ],
         "done": [
             "<b>The baseline strong</b> — <b>a system that beats a "
             "strawman has established nothing</b>, and this is graded "
             "first.",
             "<b>The metric justified against the decision</b>, which "
             "is the project's central requirement and the one most "
             "often skipped.",
             "<b>Twenty errors actually read</b> — the categories "
             "must come from the data rather than from your "
             "expectations.",
             "<b>And the limitation statement specific and "
             "non-empty</b>, in Module 13 §2's "
             "form. <b>A system reported without known failures has "
             "not been evaluated.</b>",
         ]},
    ],
    "map": [
        ("Jurafsky & Martin — Speech and Language Processing, 3rd "
         "edition (free)",
         "https://web.stanford.edu/~jurafsky/slp3/",
         "<b>Every module.</b> Read the corresponding chapter after "
         "each one; the book is better than any summary of it, "
         "including this course's."),
        ("Stanford CS224N — NLP with Deep Learning (free, with "
         "lectures)",
         "https://web.stanford.edu/class/cs224n/",
         "<b>Modules 04 through 09 as a lecture course</b>, with "
         "assignments, free. The best-paced presentation of the neural "
         "material available."),
        ("The Annotated Transformer (free)",
         "https://nlp.seas.harvard.edu/annotated-transformer/",
         "<b>Module 06 as working code</b> — implement from this "
         "once and the architecture stops being mysterious."),
        ("Hugging Face NLP course (free)",
         "https://huggingface.co/learn/nlp-course",
         "<b>Modules 07, 08, and 11 practically</b> — the "
         "toolchain, with the pitfalls flagged."),
        ("The ACL Anthology (free)",
         "https://aclanthology.org/",
         "<b>Every paper in the field, free.</b> Module 13's "
         "exercises use it; read the limitations sections, which are "
         "where the honest claims live."),
        ("Papers With Code and the benchmark leaderboards (free)",
         "https://paperswithcode.com/",
         "<b>Module 10's cautionary material</b> — useful for "
         "finding baselines, and read CSCE 633 Module 12 before "
         "trusting a leaderboard."),
    ],
}

MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "What Is Hard About Language",
 "subtitle": "Four properties, and the whole course as a response.",
 "question": "Why is text a harder input than an image?",
 "outcomes": [
     "Explain discreteness and what it costs.",
     "Explain compositionality and ambiguity.",
     "Explain why the structure is not given.",
     "Map each course technique to the property it addresses.",
     "Explain why some tasks are harder than their framing "
     "suggests.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Four properties",
   "blurb": "Each of which forces a technique."},

  {"t": "table", "kicker": "Properties", "title": "The four properties, and the response to each",
   "header": ["Property", "Why it is hard", "The response"],
   "widths": [2.6, 4.2, 5.1],
   "rows": [
     ["<b>Discrete</b>", "<b>No natural distance between words; the vocabulary is open</b>", "<b>Learned embeddings and subwords (M02, M04)</b>"],
     ["<b>Compositional</b>", "<b>Meaning depends on combination, not on the bag</b>", "<b>Sequence models and attention (M05, M06)</b>"],
     ["<b>Ambiguous</b>", "<b>At every level, and resolved by context</b>", "<b>Contextual representations (M07)</b>"],
     ["<b>Unstructured</b>", "<b>The syntax and semantics are latent, not labelled</b>", "<b>Pretraining on raw text (M07)</b>"],
   ],
   "footnote": "<b>This table is the course's outline.</b> Every "
               "technique in the remaining twelve modules is an answer to "
               "one of these four rows, which is worth checking as you "
               "go.",
   "note": "Returning to this table at each module is the course's "
           "organising device."},

  {"t": "callout", "title": "Discreteness is the one that shapes everything downstream",
   "kind": "Why the first problem is representation",
   "body": ["<b>Pixels have a natural metric</b> — two similar "
            "colours are numerically close, so a convolution over them "
            "means something (CSCE 636 §05). "
            "<b>Words do not.</b>",
            "<b>'Cat' and 'dog' are no closer than 'cat' and "
            "'thermodynamics' under any encoding you get for "
            "free</b> — and a one-hot vector makes every pair "
            "exactly equidistant, which discards all the structure you "
            "needed.",
            "<b>And the vocabulary is open.</b> <b>New words appear "
            "constantly, so a fixed vocabulary guarantees unknown "
            "tokens</b> at inference — which is "
            "Module 02's subword answer.",
            "<b>So the first problem in NLP is representation rather "
            "than modelling</b> — <b>and nearly all of the field's "
            "progress has come from better representations rather than "
            "better classifiers</b>, which is the single most useful "
            "generalisation about it."]},

  {"t": "section", "label": "Part 2", "title": "Ambiguity",
   "blurb": "At every level, simultaneously."},

  {"t": "code", "kicker": "Ambiguity", "title": "The levels, with an example at each",
   "lang": "text", "code": """
  LEXICAL     "bank" -- financial or riverside
  MORPHOLOGICAL
              "unlockable" -- cannot be locked, or
              able to be unlocked
  SYNTACTIC   "I saw the man with the telescope"
              -- who had it?
  SCOPE       "every student read a book" -- one book
              or one each?
  REFERENCE   "the trophy did not fit in the suitcase
              because it was too large" -- which?
  PRAGMATIC   "can you pass the salt?" -- not a
              question about ability

  AND THEY INTERACT. Resolving the syntax may require
  knowing the word sense; knowing the sense may require
  the syntax.

  WHICH IS WHY the pipeline architecture (tokenise,
  tag, parse, then interpret) loses to joint models:
  each stage needs information the later stages have.
""",
   "caption": "<b>The interaction is the real difficulty</b> — "
              "which is the argument against the classical pipeline and "
              "for end-to-end models.",
   "note": "The pipeline critique motivates everything from Module 05 "
           "onward."},

  {"t": "callout", "title": "Ambiguity is resolved by context, which is why context length matters",
   "kind": "The connection to the architectures",
   "body": ["<b>Nearly every ambiguity above is resolved by "
            "surrounding text</b> — sometimes a word away, sometimes "
            "a paragraph away, and sometimes by knowledge not in the text "
            "at all.",
            "<b>Which sets the architectural requirement:</b> <b>a "
            "representation of a word must depend on its "
            "context</b> — a fixed vector per word type cannot "
            "disambiguate 'bank' (Module 04 §4).",
            "<b>And it explains why context length is a headline "
            "number.</b> <b>A model that can only see five words cannot "
            "resolve a reference twenty words back</b>, however good its "
            "parameters.",
            "<b>So Module 04's static embeddings, "
            "Module 05's recurrence, and "
            "Module 06's attention are three successive "
            "answers to the same requirement</b> — which is why the "
            "course is ordered historically."]},

  {"t": "section", "label": "Part 3", "title": "The missing structure",
   "blurb": "And where the supervision comes from."},

  {"t": "callout", "title": "Language has rich structure and almost no labels",
   "kind": "The property that made pretraining inevitable",
   "body": ["<b>Syntax, semantics, discourse, and world knowledge are "
            "all present in text and none of them are "
            "annotated</b> — and <b>hand-annotating them is "
            "expensive, slow, and produces datasets of thousands rather "
            "than billions of examples.</b>",
            "<b>But the text itself is abundant.</b> <b>Which makes "
            "self-supervision the obvious move: construct a prediction "
            "task from the text alone, and the structure has to be "
            "learned to solve it.</b>",
            "<b>'Predict the next word' requires syntax, semantics, "
            "and a great deal of world knowledge</b> — so a model "
            "trained only on that acquires representations useful for "
            "tasks it never saw (Module 07).",
            "<b>Which is the single most consequential idea in modern "
            "NLP</b> — <b>and it follows directly from this "
            "property</b> rather than from any architectural insight."]},

  {"t": "section", "label": "Part 4", "title": "Harder than it looks",
   "blurb": "Tasks whose framing understates them."},

  {"t": "bullets", "kicker": "Tasks", "title": "Where a simple framing hides the difficulty",
   "items": [
     "<b>Sentiment classification sounds easy</b> and includes "
     "sarcasm, negation at a distance, mixed sentiment, and comparative "
     "statements — <b>each of which needs composition rather than "
     "keywords.</b>",
     "",
     "<b>Named entity recognition</b> requires knowing that a "
     "sequence of ordinary words is a title, which is "
     "world knowledge rather than a pattern.",
     "",
     "<b>Coreference</b> requires the physical and social "
     "reasoning of the trophy example — <b>which is not in the "
     "sentence.</b>",
     "",
     "<b>Translation</b> requires choices the source language did "
     "not make: grammatical gender, formality, and definiteness, all "
     "unspecified in the input.",
     "",
     "<b>And summarisation has no single correct answer</b>, which "
     "makes it an evaluation problem as much as a modelling one "
     "(Module 10 §3).",
   ],
   "footnote": "<b>The pattern is that each task needs information "
               "not present in its input</b> — which is why "
               "pretraining on everything helps more than task-specific "
               "architecture."},

  {"t": "callout", "title": "How to read this course",
   "kind": "Orientation",
   "body": ["<b>Modules 02 to 04 address representation</b> — "
            "tokenisation, counting, and learned dense vectors, which is "
            "the discreteness row.",
            "<b>Modules 05 to 07 address composition and "
            "context</b> — recurrence, attention, the transformer, "
            "and pretraining, which is the middle two rows and the "
            "fourth.",
            "<b>Modules 08 to 11 are practice</b> — adaptation, "
            "decoding, evaluation, and retrieval, which is where a real "
            "system is built.",
            "<b>And Modules 12 and 13 are about failure and about "
            "honest claims</b> — <b>which are not an "
            "appendix</b>, because a fluent wrong answer is the "
            "characteristic failure of everything built in this "
            "course."]},
 ],
 "takeaways": [
   "Language is discrete, compositional, ambiguous, and unstructured, and "
   "every technique in the course answers one of those four.",
   "Words have no natural metric and one-hot encoding makes every pair "
   "equidistant, which discards exactly the structure you needed.",
   "Nearly all of the field's progress came from better representations "
   "rather than better classifiers.",
   "Ambiguity levels interact, which is the argument against the classical "
   "pipeline and for joint, end-to-end models.",
   "Language has rich structure and almost no labels, which is why "
   "self-supervision was inevitable rather than clever.",
   "Each apparently simple task needs information not present in its "
   "input, which is why pretraining on everything beats task-specific "
   "architecture.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Four properties"),
  ("table", ["Property", "Why it makes language hard", "The response, and "
             "where"],
   [["<b>Discrete</b>",
     "<b>There is no natural distance between words, and the vocabulary "
     "is open-ended.</b>",
     "<b>Learned embeddings and subword tokenisation</b> "
     "(Modules 02 and 04)."],
    ["<b>Compositional</b>",
     "<b>Meaning depends on how the words combine, not on which words "
     "are present.</b>",
     "<b>Sequence models and attention</b> (Modules 05 and "
     "06)."],
    ["<b>Ambiguous</b>",
     "<b>At every level simultaneously, and resolved by context</b> "
     "(&sect;2).",
     "<b>Contextual representations</b> — a word's vector "
     "depending on its sentence (Module 07)."],
    ["<b>Unstructured</b>",
     "<b>The syntax, semantics, and world knowledge are latent rather "
     "than labelled</b> (&sect;3).",
     "<b>Self-supervised pretraining on raw text</b> "
     "(Module 07)."]],
   [0.18, 0.37, 0.45]),
  ("p", "<b>This table is the course's outline.</b> <b>Every technique "
        "in the remaining twelve modules is an answer to one of these four "
        "rows</b>, and checking which one as you go is the most useful "
        "orientation device available — it converts a sequence of "
        "architectures into a sequence of responses to stated problems, "
        "which is both easier to remember and more transferable."),
  ("callout", "Discreteness is the one that shapes everything downstream",
   ["<b>Pixels have a natural metric</b> — two similar colours are "
    "numerically close, which is exactly why a convolution over them means "
    "something (CSCE 636 Module 05's whole premise). <b>Words do "
    "not have this property at all.</b>",
    "<b>'Cat' and 'dog' are no closer than 'cat' and 'thermodynamics' "
    "under any encoding you get for free</b> — and <b>a one-hot "
    "vector makes every pair of words exactly equidistant</b>, which "
    "discards precisely the structure you needed and leaves the model to "
    "rediscover all of it from data.",
    "<b>And the vocabulary is open.</b> <b>New words, names, "
    "misspellings, and compounds appear constantly, so a fixed vocabulary "
    "guarantees unknown tokens at inference time</b> — which is the "
    "problem Module 02's subword tokenisation exists to solve, and "
    "which the classical approach handled by mapping everything unseen to "
    "a single uninformative symbol.",
    "<b>So the first problem in natural language processing is "
    "representation rather than modelling</b> — and <b>nearly all of "
    "the field's progress has come from better representations rather "
    "than better classifiers</b>, which is the single most useful "
    "generalisation available about its history and is worth holding "
    "onto through the next twelve modules."]),

  ("h1", "2 &nbsp; Ambiguity"),
  ("code", """LEXICAL     "bank" -- financial or riverside
MORPHOLOGICAL
            "unlockable" -- cannot be locked, or able
            to be unlocked
SYNTACTIC   "I saw the man with the telescope"
            -- who had the telescope?
SCOPE       "every student read a book" -- one book
            between them, or one each?
REFERENCE   "the trophy did not fit in the suitcase
            because it was too large" -- which one?
PRAGMATIC   "can you pass the salt?" -- not actually a
            question about your ability

AND THEY INTERACT. Resolving the syntax may require
knowing the word sense; knowing the sense may require
the syntax.

WHICH IS WHY the classical pipeline architecture
(tokenise, tag, parse, then interpret) loses to joint
models: each stage needs information that only the
later stages have."""),
  ("p", "<b>The interaction is the real difficulty</b>, rather than any "
        "individual level — <b>which is the argument against the "
        "classical pipeline and for end-to-end models</b>. A pipeline "
        "commits to a tokenisation, then to a tagging, then to a parse, "
        "and <b>each commitment is made without the information that would "
        "have resolved it</b>, with the errors compounding downstream. "
        "<b>This critique motivates everything from Module 05 onward</b>, "
        "and it is worth knowing that the pipeline was not abandoned "
        "because it was inelegant but because it was measurably worse."),
  ("callout", "Ambiguity is resolved by context, which is why context length "
              "matters",
   ["<b>Nearly every ambiguity in &sect;2 is resolved by surrounding "
    "text</b> — sometimes a word away, sometimes a paragraph away, "
    "and sometimes by knowledge that is not in the text at all (the "
    "trophy example requires knowing how physical containment works).",
    "<b>Which sets the architectural requirement directly:</b> <b>a "
    "representation of a word must depend on its context</b> — and "
    "<b>a single fixed vector per word type cannot possibly disambiguate "
    "'bank'</b>, because it has to represent both senses at once "
    "(Module 04 &sect;4's central limitation).",
    "<b>And it explains why context length is a headline number for "
    "these systems.</b> <b>A model that can only attend over five words "
    "cannot resolve a reference twenty words back</b>, however good its "
    "parameters are — the information is simply not available to "
    "it.",
    "<b>So Module 04's static embeddings, Module 05's "
    "recurrence, and Module 06's attention are three successive "
    "answers to the same requirement</b>, each handling more context "
    "more flexibly than the last — <b>which is why this course is "
    "ordered historically rather than by elegance.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; The missing structure"),
  ("callout", "Language has rich structure and almost no labels",
   ["<b>Syntax, semantics, discourse relations, and world knowledge are "
    "all present in text, and none of them are annotated</b> — and "
    "<b>hand-annotating them is expensive, slow, requires trained "
    "linguists, and produces datasets of thousands or at best hundreds of "
    "thousands of examples</b> rather than the billions that modern "
    "methods consume.",
    "<b>But the text itself is abundant and free.</b> <b>Which makes "
    "self-supervision the obvious move: construct a prediction task from "
    "the text alone, and arrange matters so that the structure must be "
    "learned in order to solve it.</b>",
    "<b>'Predict the next word' requires syntax (to know what part of "
    "speech comes next), semantics (to know which words make sense), and "
    "a very great deal of world knowledge (to complete 'the capital of "
    "France is')</b> — so <b>a model trained only on that objective "
    "acquires representations useful for tasks it never saw</b> "
    "(Module 07).",
    "<b>Which is the single most consequential idea in modern natural "
    "language processing</b> — and <b>it follows directly from this "
    "property of the data</b> rather than from any architectural insight, "
    "which is worth noticing: the transformer made it practical at scale, "
    "and the idea itself is a response to the absence of labels."]),

  ("h1", "4 &nbsp; Tasks that are harder than their framing"),
  ("ul", ["<b>Sentiment classification sounds easy</b> and includes "
          "sarcasm, negation at a distance ('not the worst film I have "
          "seen'), mixed sentiment about different aspects, and "
          "comparative statements — <b>each of which requires "
          "composition rather than keyword counting</b>, which is why the "
          "bag-of-words baseline plateaus where it does.",
          "<b>Named entity recognition</b> requires knowing that a "
          "particular sequence of entirely ordinary words is the title of "
          "something — <b>which is world knowledge rather than a "
          "surface pattern</b>, and is why the task benefits so much from "
          "pretraining.",
          "<b>Coreference resolution</b> requires the physical and "
          "social reasoning of the trophy example — <b>and that "
          "reasoning is not in the sentence</b>, which is what makes the "
          "Winograd-style examples a genuine test rather than a trick.",
          "<b>Translation</b> requires making choices the source "
          "language did not make: grammatical gender, levels of "
          "formality, definiteness, and number distinctions that are "
          "simply unspecified in the input — <b>so the model must "
          "infer or default, and both introduce error and bias</b> "
          "(Module 12 &sect;2).",
          "<b>And summarisation has no single correct answer</b>, which "
          "<b>makes it an evaluation problem at least as much as a "
          "modelling one</b> (Module 10 &sect;3). <b>The pattern "
          "across all five is that each task needs information not "
          "present in its input</b> — which is exactly why "
          "pretraining on everything helps more than designing a "
          "task-specific architecture, and is the empirical result that "
          "reorganised the field."]),
  ("callout", "How to read this course",
   ["<b>Modules 02 to 04 address representation</b> — "
    "tokenisation, counting-based models, and learned dense vectors, "
    "which is &sect;1's discreteness row and the foundation for "
    "everything else.",
    "<b>Modules 05 to 07 address composition and context</b> — "
    "recurrence, attention, the transformer, and pretraining, which "
    "covers the compositional, ambiguous, and unstructured rows "
    "together.",
    "<b>Modules 08 to 11 are practice</b> — adaptation under real "
    "constraints, decoding, evaluation, and retrieval augmentation, which "
    "is where an actual system gets built and where Project 2 lives.",
    "<b>And Modules 12 and 13 are about failure and about honest "
    "claims</b> — <b>which are not an appendix</b>, because <b>a "
    "fluent wrong answer is the characteristic failure of everything "
    "built in this course</b>, and fluency is precisely what these models "
    "are trained to produce."]),
 ],
 "resources": [
   ("Jurafsky & Martin, chapters 1 and 2 (free)",
    "https://web.stanford.edu/~jurafsky/slp3/",
    "<b>&sect;1 and &sect;2</b> — the properties and the ambiguity "
    "levels, with far more examples."),
   ("Bender & Koller &mdash; Climbing towards NLU (free)",
    "https://aclanthology.org/2020.acl-main.463/",
    "<b>&sect;3 and &sect;4 argued sharply</b> — what learning from "
    "form alone can and cannot provide. Read it again before "
    "Module 13."),
   ("Levesque et al. &mdash; The Winograd Schema Challenge (free)",
    "https://cdn.aaai.org/ocs/4492/4492-21843-1-PB.pdf",
    "<b>&sect;2's reference ambiguity as a designed test</b> — and "
    "the reasoning about why it resists surface statistics."),
   ("Stanford CS224N, lecture 1 (free)",
    "https://web.stanford.edu/class/cs224n/",
    "<b>&sect;1 as a lecture</b>, with the representation argument made "
    "carefully."),
 ],
 "exercises": [
   "<b>Write a sentence ambiguous at three of the six levels</b> "
   "simultaneously.",
   "<b>Find a real ambiguity</b> whose resolution requires knowledge "
   "outside the text.",
   "<b>Compute the cosine similarity</b> of one-hot vectors for 'cat', "
   "'dog', and 'thermodynamics'.",
   "<b>Explain what that result costs</b> a downstream classifier.",
   "<b>Estimate the unknown-token rate</b> of a 20,000-word vocabulary "
   "on held-out text.",
   "<b>Run a classical pipeline</b> on five sentences and find one "
   "compounding error.",
   "<b>Construct a sentiment example</b> that keyword counting gets "
   "wrong.",
   "<b>Find a translation choice</b> the source language leaves "
   "unspecified.",
   "<b>Write three summaries of one paragraph</b> and argue all three "
   "are acceptable.",
   "<b>Map each of the four properties</b> to a technique you expect to "
   "meet, and check your predictions at Module 07.",
 ],
 "selfcheck": [
   "Name the four properties and the response to each.",
   "Why does discreteness shape everything downstream?",
   "What does a one-hot encoding discard?",
   "Why does an open vocabulary guarantee unknown tokens?",
   "Name the six ambiguity levels with an example of each.",
   "Why do the levels interacting defeat a pipeline?",
   "Why must a word's representation depend on its context?",
   "Why was self-supervision inevitable here?",
   "What does 'predict the next word' require the model to learn?",
   "Give five tasks whose framing understates them, and the shared "
   "pattern.",
 ],
},

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Text as Data",
 "subtitle": "Tokenisation, and why it is not a solved detail.",
 "question": "What is a word, and does the question have an answer?",
 "outcomes": [
     "Explain why tokenisation is a modelling decision.",
     "Explain subword algorithms and what they buy.",
     "Explain the failure modes tokenisation causes.",
     "Explain normalisation and what it destroys.",
     "Inspect a tokeniser's actual output.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "There is no language-independent notion of a word."},

  {"t": "callout", "title": "Whitespace is not a word boundary, and a word is not a unit of meaning",
   "kind": "Why the obvious approach fails",
   "body": ["<b>Chinese and Japanese are written without spaces</b>, "
            "so whitespace splitting produces nothing — and <b>German "
            "compounds and Turkish agglutination produce single "
            "'words' carrying a sentence's worth of meaning.</b>",
            "<b>And even in English:</b> <b>'New York' is one "
            "concept in two words; 'don't' is two words in one; and "
            "'state-of-the-art' is anyone's guess.</b>",
            "<b>So the question 'what is a word' has no "
            "language-independent answer</b> — which means "
            "tokenisation is a <b>modelling decision with "
            "consequences</b> rather than a preprocessing "
            "detail.",
            "<b>And it is the decision made earliest and revisited "
            "least</b> — <b>every model in this course inherits its "
            "tokeniser's limitations</b>, and Part 3 covers "
            "what those turn out to be."]},

  {"t": "table", "kicker": "Options", "title": "The granularities, and what each trades",
   "header": ["Unit", "Advantage", "Cost"],
   "widths": [2.6, 4.2, 5.1],
   "rows": [
     ["<b>Characters</b>", "<b>No unknown tokens ever; tiny vocabulary</b>", "<b>Very long sequences; little meaning per unit</b>"],
     ["<b>Words</b>", "<b>Units carry meaning</b>", "<b>Huge vocabulary; unknown tokens guaranteed</b>"],
     ["<b>Subwords</b>", "<b>No unknowns, bounded vocabulary, frequent words intact</b>", "<b>Splits are statistical, not morphological</b>"],
     ["<b>Bytes</b>", "<b>Universal; handles any script and any encoding</b>", "<b>Longest sequences; no linguistic alignment</b>"],
   ],
   "footnote": "<b>Subwords won because they bound the vocabulary "
               "<i>and</i> eliminate unknown tokens</b> — which were "
               "previously a trade — and the cost is that the splits "
               "do not respect morphology.",
   "note": "The both-at-once property is why subwords took over."},

  {"t": "section", "label": "Part 2", "title": "Subword algorithms",
   "blurb": "How the vocabulary is learned."},

  {"t": "code", "kicker": "BPE", "title": "Byte-pair encoding, which is the one to understand",
   "lang": "text", "code": """
  TRAINING
      1. start with the vocabulary of single characters
      2. count every adjacent pair in the corpus
      3. merge the most frequent pair into one token
      4. record the merge; repeat to the target size

  INFERENCE
      apply the recorded merges in the same order

  SO: frequent sequences become single tokens, and rare
  ones remain split into pieces. "the" is one token;
  an unusual surname is five.

  THE VARIANTS
      WordPiece    merges by likelihood gain rather
                   than raw frequency
      Unigram      starts large and prunes, keeping
                   the most probable segmentation
      SentencePiece treats the input as raw bytes, so
                   no pre-tokenisation is needed

  AND FREQUENCY IS THE ONLY CRITERION -- which is
  Part 3's whole problem.
""",
   "caption": "<b>Frequency is the only criterion</b> — so the "
              "segmentation reflects the training corpus rather than the "
              "language's structure.",
   "note": "The frequency-only point is what produces every failure in "
           "Part 3."},

  {"t": "section", "label": "Part 3", "title": "What it breaks",
   "blurb": "Real failures traceable to tokenisation."},

  {"t": "bullets", "kicker": "Failures", "title": "The consequences, which are not minor",
   "items": [
     "<b>Arithmetic.</b> <b>Numbers split inconsistently</b> "
     "— '1234' may be one token or three, depending on frequency "
     "— <b>which makes digit-level reasoning hard for reasons that "
     "have nothing to do with arithmetic.</b>",
     "",
     "<b>Character-level tasks.</b> <b>A model that never sees "
     "individual letters struggles to count them or reverse a "
     "word</b>, which looks like a reasoning failure and is a "
     "representation failure.",
     "",
     "<b>Low-resource languages.</b> <b>A tokeniser trained mostly "
     "on English splits other scripts into many more tokens</b> "
     "— so the same meaning costs more context and more money "
     "(Module 12 §2).",
     "",
     "<b>Spelling and morphology</b> — related words get "
     "unrelated token sequences, so the model must learn the relation "
     "from scratch.",
     "",
     "<b>And prompt sensitivity</b> — <b>a trailing space "
     "changes the tokenisation and therefore the output.</b>",
   ],
   "footnote": "<b>The low-resource point is the one with the clearest "
               "equity consequence</b> — identical content costs "
               "several times more tokens in some languages than in "
               "English."},

  {"t": "callout", "title": "Which means some apparent reasoning failures are tokenisation failures",
   "kind": "A diagnostic habit worth having",
   "body": ["<b>When a model fails at counting characters, comparing "
            "numbers, or manipulating spelling, check the tokenisation "
            "before concluding anything about reasoning.</b>",
            "<b>Because the model may genuinely not have access to the "
            "information</b> — if '1234' is a single opaque token, "
            "the digits are not separately represented at all.",
            "<b>And the fix is frequently a representation change "
            "rather than a model change</b> — splitting digits "
            "individually, or restating the task.",
            "<b>Which is a specific instance of a general "
            "habit:</b> <b>before attributing a failure to the model's "
            "capability, check whether the input representation made the "
            "task possible</b> (Module 13 §1)."]},

  {"t": "section", "label": "Part 4", "title": "Normalisation",
   "blurb": "And what each step throws away."},

  {"t": "bullets", "kicker": "Normalisation", "title": "The steps, and what each destroys",
   "items": [
     "<b>Lowercasing</b> loses the distinction between 'Apple' and "
     "'apple', 'US' and 'us' — <b>which matters for entity "
     "recognition and barely at all for topic "
     "classification.</b>",
     "",
     "<b>Unicode normalisation</b> is nearly always right, since "
     "visually identical strings should be one thing — and it is "
     "the step most often omitted.",
     "",
     "<b>Stripping punctuation</b> loses sentence boundaries, "
     "negation cues, and the difference between a statement and a "
     "question.",
     "",
     "<b>Stemming and lemmatisation</b> conflate inflections, "
     "which <b>helps a sparse count-based model and is unnecessary "
     "for a model with learned subwords.</b>",
     "",
     "<b>And removing stopwords</b> destroys exactly the function "
     "words that carry syntax — <b>appropriate for retrieval, "
     "harmful for anything compositional.</b>",
   ],
   "footnote": "<b>Every step is lossy, and the right choice depends "
               "on the task</b> — which is why the classical "
               "preprocessing recipe is wrong for neural models and was "
               "right for the models it was designed for."},

  {"t": "callout", "title": "The practical instruction: read your tokeniser's output",
   "kind": "Closing",
   "body": ["<b>Print the tokens for twenty inputs from your actual "
            "data</b> — including the longest, the shortest, the "
            "numeric, the non-English, and the badly formatted "
            "ones.",
            "<b>You will find something surprising</b> — a word "
            "split into six pieces, a number tokenised "
            "inconsistently, an emoji consuming four tokens, or your "
            "domain's key term fragmented.",
            "<b>And that finding changes decisions:</b> <b>sequence "
            "length budgets, cost estimates, and whether a "
            "domain-specific vocabulary is worth training.</b>",
            "<b>Which is five minutes of work that nobody does</b> "
            "— and <b>it is the cheapest diagnostic in this "
            "course.</b>"]},
 ],
 "takeaways": [
   "There is no language-independent notion of a word, so tokenisation is a "
   "modelling decision rather than a preprocessing detail.",
   "Subwords won because they bound the vocabulary and eliminate unknown "
   "tokens at the same time, which was previously a trade.",
   "Frequency is BPE's only criterion, so the segmentation reflects the "
   "training corpus rather than the language's structure.",
   "Some apparent reasoning failures are tokenisation failures — "
   "check the representation before concluding anything about capability.",
   "A tokeniser trained mostly on English makes identical content cost "
   "several times more tokens in other languages.",
   "Every normalisation step is lossy, which is why the classical recipe "
   "is wrong for neural models and was right for count-based ones.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The problem"),
  ("callout", "Whitespace is not a word boundary, and a word is not a unit "
              "of meaning",
   ["<b>Chinese and Japanese are written without spaces between "
    "words</b>, so whitespace splitting produces a single enormous "
    "token — and <b>German compounding and Turkish agglutination "
    "produce single orthographic 'words' carrying what English would "
    "express in a clause.</b>",
    "<b>And even in English the notion does not hold "
    "together:</b> <b>'New York' is one concept written as two words; "
    "'don't' is two words written as one; 'state-of-the-art' is anyone's "
    "guess; and a URL or a chemical name is not a word at all.</b>",
    "<b>So the question 'what is a word' has no language-independent "
    "answer</b>, and arguably no answer within a single language "
    "either — which means <b>tokenisation is a modelling decision "
    "with downstream consequences</b> rather than a preprocessing "
    "detail to be handled by a utility function.",
    "<b>And it is the decision made earliest and revisited "
    "least.</b> <b>Every model in this course inherits its tokeniser's "
    "limitations</b> — and <b>&sect;3 covers what those turn out to "
    "be</b>, which is considerably more consequential than the topic's "
    "usual treatment suggests."]),
  ("table", ["Unit", "The advantage", "The cost"],
   [["<b>Characters</b>",
     "<b>No unknown tokens, ever; a vocabulary of a few hundred.</b>",
     "<b>Very long sequences, and very little meaning per unit</b> "
     "— the model must compose everything from scratch."],
    ["<b>Words</b>", "<b>The units carry meaning directly.</b>",
     "<b>An enormous vocabulary, and unknown tokens guaranteed</b> at "
     "inference (Module 01 &sect;1)."],
    ["<b>Subwords</b>",
     "<b>No unknown tokens, a bounded vocabulary, and frequent words "
     "kept intact.</b>",
     "<b>The splits are statistical rather than morphological</b> "
     "(&sect;2), which produces &sect;3's failures."],
    ["<b>Bytes</b>",
     "<b>Universal — handles any script, any encoding, any "
     "input.</b>",
     "<b>The longest sequences, and no linguistic alignment at all.</b>"]],
   [0.18, 0.37, 0.45]),
  ("p", "<b>Subwords won because they bound the vocabulary <i>and</i> "
        "eliminate unknown tokens</b> — <b>which were previously a "
        "trade-off between the first two rows</b>, and getting both at "
        "once is a genuine advance rather than a compromise. <b>The cost "
        "is that the splits do not respect morphology</b>, which is "
        "&sect;3's subject and is a real price rather than a theoretical "
        "one."),

  ("h1", "2 &nbsp; Subword algorithms"),
  ("code", """TRAINING
    1. start with the vocabulary of single characters
    2. count every adjacent pair in the corpus
    3. merge the most frequent pair into one token
    4. record the merge; repeat to the target size

INFERENCE
    apply the recorded merges, in the same order

SO: frequent sequences become single tokens, and rare
ones remain split into pieces. "the" is one token; an
unusual surname is five.

THE VARIANTS
    WordPiece     merges by likelihood gain rather
                  than by raw frequency
    Unigram       starts from a large vocabulary and
                  prunes, keeping the most probable
                  segmentation of the corpus
    SentencePiece treats the input as raw bytes, so no
                  language-specific pre-tokenisation
                  step is needed at all

AND FREQUENCY IS THE ONLY CRITERION -- which is
section 3's whole problem."""),
  ("p", "<b>Frequency is the only criterion</b>, in every variant "
        "— so <b>the segmentation reflects the training corpus "
        "rather than the language's structure</b>. A morpheme that is "
        "linguistically fundamental but rare in the corpus gets split; a "
        "meaningless character sequence that happens to be frequent "
        "becomes a single token. <b>This single property produces every "
        "failure in &sect;3</b>, which is why it is worth stating "
        "explicitly rather than treating the algorithms as "
        "interchangeable implementation details."),

  ("break",),
  ("h1", "3 &nbsp; What tokenisation breaks"),
  ("ul", ["<b>Arithmetic.</b> <b>Numbers are split "
          "inconsistently</b> — '1234' may be one token or three "
          "depending on how often that exact string appeared — "
          "<b>which makes digit-level reasoning hard for reasons that "
          "have nothing to do with arithmetic</b> and everything to do "
          "with whether the digits are separately represented at all.",
          "<b>Character-level tasks.</b> <b>A model that never sees "
          "individual letters struggles to count them, reverse a word, or "
          "reason about spelling</b> — <b>which looks like a "
          "reasoning failure and is a representation failure</b>, and the "
          "distinction matters for what you do about it.",
          "<b>Low-resource languages.</b> <b>A tokeniser trained "
          "predominantly on English splits other scripts into several "
          "times more tokens for the same content</b> — so the same "
          "meaning consumes more of a fixed context window and costs more "
          "money per request (Module 12 &sect;2). <b>This is the "
          "clearest equity consequence in the module.</b>",
          "<b>Spelling and morphology</b> — morphologically "
          "related words receive unrelated token sequences, so <b>the "
          "model must learn their relationship from scratch from "
          "co-occurrence</b> rather than getting it from the "
          "representation.",
          "<b>And prompt sensitivity</b> — <b>a trailing space or "
          "a different quotation mark changes the tokenisation and "
          "therefore the output</b>, which accounts for a surprising "
          "share of the apparent brittleness people attribute to model "
          "capriciousness."]),
  ("callout", "Which means some apparent reasoning failures are tokenisation "
              "failures",
   ["<b>When a model fails at counting characters, comparing numbers, "
    "or manipulating spelling, check the tokenisation before concluding "
    "anything at all about its reasoning.</b>",
    "<b>Because the model may genuinely not have access to the "
    "information.</b> <b>If '1234' is a single opaque token, the "
    "individual digits are not separately represented</b> — asking "
    "it to compare that against '987' is asking it to compare two "
    "arbitrary symbols, which is a task nobody could do.",
    "<b>And the fix is frequently a representation change rather than "
    "a model change</b> — splitting digits individually at "
    "tokenisation time, or restating the task so the required units are "
    "visible, both of which cost nothing.",
    "<b>Which is a specific instance of a general habit:</b> <b>before "
    "attributing a failure to the model's capability, check whether the "
    "input representation made the task possible at all</b> "
    "(Module 13 &sect;1) — and this habit transfers well beyond "
    "language."]),

  ("h1", "4 &nbsp; Normalisation"),
  ("ul", ["<b>Lowercasing</b> loses the distinction between 'Apple' "
          "and 'apple', 'US' and 'us', 'May' and 'may' — <b>which "
          "matters a great deal for entity recognition and barely at all "
          "for topic classification</b>, and that is the shape of every "
          "decision in this list.",
          "<b>Unicode normalisation</b> is nearly always correct, "
          "since visually identical strings ought to be the same "
          "thing — and <b>it is the step most often omitted</b>, "
          "which produces silent duplicate vocabulary entries and "
          "occasionally a security issue (CSCE 713 Module 04 "
          "&sect;2's encoding confusion).",
          "<b>Stripping punctuation</b> loses sentence boundaries, "
          "negation cues, and the difference between a statement and a "
          "question — all of which were load-bearing for the "
          "compositional tasks of Module 01 &sect;4.",
          "<b>Stemming and lemmatisation</b> conflate inflected forms, "
          "which <b>helps a sparse count-based model with limited data "
          "and is unnecessary for a model with learned subword "
          "embeddings</b> — the embeddings already place the forms "
          "near one another.",
          "<b>And removing stopwords</b> destroys exactly the function "
          "words that carry the syntax — <b>appropriate for "
          "retrieval, where they contribute little and cost index space "
          "(CSCE 670), and actively harmful for anything "
          "compositional.</b> <b>Every step is lossy, and the right "
          "choice depends on the task</b> — which is why the "
          "classical preprocessing recipe is wrong for neural models and "
          "was entirely right for the models it was designed for."]),
  ("callout", "The practical instruction: read your tokeniser's output",
   ["<b>Print the tokens for twenty inputs drawn from your actual "
    "data</b> — including the longest, the shortest, the numeric, "
    "the non-English, the badly formatted, and the one with your domain's "
    "key terminology in it.",
    "<b>You will find something surprising.</b> <b>A common word in "
    "your domain split into six pieces, numbers tokenised "
    "inconsistently, an emoji consuming four tokens, whitespace handled "
    "differently than you assumed, or your product's name "
    "fragmented</b> — and any of those changes what you should "
    "do.",
    "<b>And the finding changes real decisions:</b> <b>sequence length "
    "budgets, cost estimates per request, whether a domain-specific "
    "vocabulary is worth training, and whether a task is even expressible "
    "in this representation</b> (&sect;3).",
    "<b>Which is five minutes of work that essentially nobody "
    "does</b> — and <b>it is the cheapest diagnostic in this entire "
    "course.</b> <b>Project 2 requires it</b>, for exactly that "
    "reason."]),
 ],
 "resources": [
   ("Jurafsky & Martin, chapter 2 (free)",
    "https://web.stanford.edu/~jurafsky/slp3/",
    "<b>The whole module</b>, with the normalisation decisions and the "
    "regular-expression machinery."),
   ("Sennrich et al. &mdash; Neural Machine Translation of Rare Words "
    "with Subword Units (free)",
    "https://aclanthology.org/P16-1162/",
    "<b>&sect;2's algorithm in the original</b> — short, and the "
    "motivation is stated plainly."),
   ("Kudo & Richardson &mdash; SentencePiece (free)",
    "https://aclanthology.org/D18-2012/",
    "<b>&sect;2's variants</b>, and the argument for removing "
    "language-specific pre-tokenisation entirely."),
   ("The Hugging Face tokenizers documentation (free)",
    "https://huggingface.co/docs/tokenizers/",
    "<b>&sect;4's practical instruction</b>, with the inspection API "
    "— use it on your own data today."),
 ],
 "exercises": [
   "<b>Tokenise the same sentence</b> by character, word, subword, and "
   "byte, and compare the lengths.",
   "<b>Implement BPE training</b> on a small corpus, and print the first "
   "fifty merges.",
   "<b>Apply your merges</b> to held-out text and confirm there are no "
   "unknown tokens.",
   "<b>Tokenise fifty numbers</b> and report how inconsistent the "
   "splitting is.",
   "<b>Tokenise the same paragraph in English and in two other "
   "languages</b>, and compare the token counts.",
   "<b>Find a word in your domain</b> that your tokeniser splits "
   "badly.",
   "<b>Add and remove a trailing space</b> from a prompt and compare the "
   "tokenisation.",
   "<b>Take a task a model fails</b> and determine whether the "
   "tokenisation made it possible.",
   "<b>Apply the five normalisation steps</b> to one corpus and measure "
   "the vocabulary size after each.",
   "<b>Read your tokeniser's output on twenty real inputs</b> and write "
   "down what surprised you.",
 ],
 "selfcheck": [
   "Why is whitespace not a word boundary, and why is a word not a unit "
   "of meaning?",
   "Give four tokenisation granularities with their advantage and "
   "cost.",
   "Why did subwords win?",
   "Describe BPE training and inference.",
   "What is the only criterion, and what follows from that?",
   "Give five failures traceable to tokenisation.",
   "Which has the clearest equity consequence, and why?",
   "What should you check before concluding a reasoning failure?",
   "Give five normalisation steps and what each destroys.",
   "What is the cheapest diagnostic in the course?",
 ],
},

]

for _b in ("c638_b2", "c638_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
