# -*- coding: utf-8 -*-
"""CSCE 638 — Modules 03-08."""

MODULES = [

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Language Models",
 "subtitle": "Predicting the next token, and why that is enough.",
 "question": "What does a model of P(next | context) give you?",
 "outcomes": [
     "Define a language model and state what it is for.",
     "Explain n-gram models, sparsity, and smoothing.",
     "Explain perplexity and its limitations.",
     "Explain why the neural formulation generalises.",
     "Build and evaluate both kinds.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The object",
   "blurb": "A distribution over continuations."},

  {"t": "eq", "kicker": "The model", "title": "What a language model computes",
   "eqs": [
     ("P(w₁ … wₙ) = ∏ᵢ P(wᵢ | w₁ … wᵢ₋₁)",
      "The chain rule. A distribution over sequences, factored into "
      "next-token predictions."),
     ("n-gram: P(wᵢ | w₁ … wᵢ₋₁) ≈ P(wᵢ | wᵢ₋ₖ … wᵢ₋₁)",
      "The Markov assumption: only the last k tokens matter. False, "
      "and tractable."),
     ("neural: P(wᵢ | context) = softmax(f(context))",
      "A learned function of the whole context, so no "
      "independence assumption is needed."),
   ],
   "caption": "<b>The factorisation is exact; the approximation is in "
              "how much context you condition on</b> — which is the "
              "whole difference between the two families.",
   "note": "Make clear that the chain rule is not the approximation."},

  {"t": "callout", "title": "A language model is a model of the data, and it turns out to be a model of the task",
   "kind": "Why this object is central",
   "body": ["<b>Nothing about predicting the next token mentions "
            "translation, summarisation, or question answering</b> "
            "— and yet <b>a sufficiently good next-token predictor "
            "can do all three</b>, because each can be phrased as a "
            "continuation.",
            "<b>Which is the observation the field was built on.</b> "
            "<b>'Translate to French: hello →' has a correct "
            "continuation</b>, so a model that predicts continuations "
            "well translates.",
            "<b>And the training signal is free</b> "
            "(Module 01 §3) — any text is a labelled "
            "example of 'what comes next', which is why these models "
            "scaled when supervised ones could not.",
            "<b>But it is worth being precise about what follows:</b> "
            "<b>the model is optimised for plausible continuation, not "
            "for correctness</b> — and that distinction is "
            "Module 12 §3's whole subject."]},

  {"t": "section", "label": "Part 2", "title": "Counting, and its limit",
   "blurb": "Why n-grams plateau."},

  {"t": "code", "kicker": "Sparsity", "title": "The problem that smoothing exists to manage",
   "lang": "text", "code": """
  P(w | context) = count(context, w) / count(context)

  AND MOST COUNTS ARE ZERO
      a 20,000-word vocabulary gives 8 x 10^12
      possible trigrams. No corpus covers them.
      So an unseen trigram gets probability 0, and
      the whole sequence gets probability 0.

  SMOOTHING, in increasing sophistication
      add-one         simple, and badly biased
      back-off        use the shorter context when
                      the longer one is unseen
      interpolation   mix all orders with learned
                      weights
      Kneser-Ney      back off by how many DISTINCT
                      contexts a word appears in,
                      not by its raw frequency

  KNESER-NEY'S INSIGHT: "Francisco" is frequent but
  appears almost only after "San", so it is a poor
  back-off candidate. Diversity of context beats
  frequency.
""",
   "caption": "<b>Kneser-Ney's insight is the best idea in classical "
              "language modelling</b> — and it is a statement about "
              "generalisation rather than about counting.",
   "note": "The Francisco example is what makes Kneser-Ney "
           "memorable."},

  {"t": "callout", "title": "The real limit is that counting cannot generalise across similar words",
   "kind": "Why neural models replaced this",
   "body": ["<b>Having seen 'the cat sat on the mat' a thousand times "
            "tells an n-gram model nothing about 'the dog sat on the "
            "rug'</b> — the contexts are different strings, so the "
            "counts are unrelated.",
            "<b>Which is Module 01 §1's discreteness "
            "arriving as a concrete modelling failure</b> — there is "
            "no notion of similarity between contexts, so every context "
            "must be observed.",
            "<b>And smoothing does not fix it.</b> <b>Smoothing "
            "redistributes probability mass to unseen events; it does not "
            "transfer what was learned about one word to a similar "
            "one.</b>",
            "<b>So the neural formulation's advantage is "
            "sharing:</b> <b>'cat' and 'dog' get nearby vectors, so "
            "evidence about one informs the other</b> — which is "
            "Module 04's subject and the reason for the whole "
            "architecture."]},

  {"t": "section", "label": "Part 3", "title": "Perplexity",
   "blurb": "The standard metric, and what it does not tell you."},

  {"t": "eq", "kicker": "Perplexity", "title": "The metric, and how to read it",
   "eqs": [
     ("PP = exp( −(1/N) Σᵢ log P(wᵢ | context) )",
      "The exponentiated average negative log likelihood per token "
      "on held-out text."),
     ("PP = 100  ⟺  as uncertain as choosing uniformly among 100",
      "The interpretation: an effective branching factor. Lower is "
      "better."),
     ("PP depends on the tokenisation",
      "So two models with different tokenisers are not comparable "
      "by perplexity at all (Module 02)."),
   ],
   "caption": "<b>The tokenisation dependence is the trap</b> — "
              "perplexity numbers are comparable only within a fixed "
              "vocabulary and a fixed test set.",
   "note": "The incomparability point is what people get wrong."},

  {"t": "bullets", "kicker": "Limits", "title": "And what perplexity does not measure",
   "items": [
     "<b>It does not measure usefulness.</b> <b>A model with "
     "lower perplexity can be worse at your task</b>, and the "
     "correlation is positive and far from perfect.",
     "",
     "<b>It is dominated by the frequent, easy tokens</b> — "
     "function words and punctuation — so <b>a large improvement "
     "there can mask no improvement on content.</b>",
     "",
     "<b>It is incomparable across tokenisers and across test "
     "sets</b>, which makes most published comparisons harder to read "
     "than they appear.",
     "",
     "<b>And it rewards hedging.</b> <b>A model that spreads "
     "probability broadly scores better than one that commits and is "
     "occasionally wrong</b>, which is not always what you "
     "want.",
     "",
     "<b>So use it for development and report task metrics for "
     "claims</b> (Module 10).",
   ],
   "footnote": "<b>'Dominated by the easy tokens' is the limitation "
               "that matters most</b> — it means perplexity "
               "improvements can be real and irrelevant at the same "
               "time."},

  {"t": "section", "label": "Part 4", "title": "The neural formulation",
   "blurb": "And what it fixed."},

  {"t": "code", "kicker": "Neural LM", "title": "The architecture, in its simplest form",
   "lang": "text", "code": """
  1. look up an embedding for each context token
  2. combine them somehow (concatenate, average, or
     a sequence model -- Modules 05 and 06)
  3. a hidden layer or several
  4. a softmax over the vocabulary

  WHAT THIS BUYS
      similar words share parameters, so evidence
          transfers between them
      the context can be arbitrarily long, in
          principle
      and the model size does not grow with the
          number of observed contexts

  WHAT IT COSTS
      the softmax over a large vocabulary is the
          expensive part -- which is why sampled
          softmax, hierarchical softmax, and
          subword vocabularies all exist
      and it needs much more computation per
          prediction than a table lookup
""",
   "caption": "<b>Parameter sharing between similar words is the whole "
              "gain</b> — everything else here is machinery to make "
              "it affordable.",
   "note": "Keep the focus on sharing rather than on depth."},

  {"t": "callout", "title": "And this is where the course's arc begins",
   "kind": "Closing",
   "body": ["<b>Module 04 asks where the embeddings come from</b>, "
            "and finds that they can be learned from co-occurrence "
            "alone.",
            "<b>Module 05 asks how to combine a variable-length "
            "context</b>, and finds that recurrence works and forgets.",
            "<b>Module 06 replaces recurrence with "
            "attention</b>, which fixes the forgetting and "
            "parallelises.",
            "<b>And Module 07 observes that the resulting model, "
            "trained at scale on this same objective, is useful for "
            "everything</b> — which is where the field "
            "is."]},
 ],
 "takeaways": [
   "The chain rule factorisation is exact; the approximation is in how much "
   "context you condition on.",
   "Nothing about next-token prediction mentions any task, and a "
   "sufficiently good predictor does all of them — which is the "
   "observation the field was built on.",
   "The model is optimised for plausible continuation rather than for "
   "correctness, which is the source of its characteristic failure.",
   "Counting cannot generalise across similar words, and smoothing "
   "redistributes mass rather than transferring evidence.",
   "Perplexity is dominated by frequent easy tokens and is incomparable "
   "across tokenisers, so improvements can be real and irrelevant.",
   "Parameter sharing between similar words is the entire gain of the "
   "neural formulation.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The object"),
  ("eq", "P(w<sub>1</sub> &hellip; w<sub>n</sub>) = &prod;<sub>i</sub> "
         "P(w<sub>i</sub> | w<sub>1</sub> &hellip; w<sub>i&minus;1</sub>)"),
  ("ul", ["<b>The chain rule factorisation is exact.</b> Any "
          "distribution over sequences can be written this way, so "
          "<b>nothing has been approximated yet.</b>",
          "<b>The n-gram approximation</b> replaces the full history "
          "with the last k tokens — a Markov assumption that is "
          "<b>plainly false about language and computationally "
          "tractable</b>, which was the right trade for decades.",
          "<b>The neural formulation</b> computes P(w<sub>i</sub> | "
          "context) as a softmax over a learned function of the whole "
          "context, <b>so no independence assumption is required at "
          "all</b> — the limit becomes architectural rather than "
          "statistical.",
          "<b>Which is the whole difference between the two "
          "families:</b> <b>the factorisation is shared and the amount "
          "of context conditioned upon is not</b>, and every advance from "
          "Module 05 onward is about conditioning on more of it more "
          "effectively."]),
  ("callout", "A language model is a model of the data, and it turns out to "
              "be a model of the task",
   ["<b>Nothing about predicting the next token mentions translation, "
    "summarisation, or question answering</b> — and yet <b>a "
    "sufficiently good next-token predictor can do all three</b>, because "
    "each of them can be phrased as a continuation of some prefix.",
    "<b>Which is the observation the entire field was built on.</b> "
    "<b>'Translate to French: hello &rarr;' has a correct "
    "continuation</b>, so a model that predicts continuations accurately "
    "translates — without ever having been trained to translate, "
    "which was a genuine surprise when it was first demonstrated at "
    "scale.",
    "<b>And the training signal is free</b> (Module 01 "
    "&sect;3) — <b>any text at all is a labelled example of 'what "
    "comes next'</b> — which is why these models scaled when "
    "supervised approaches could not, since supervision was the binding "
    "constraint.",
    "<b>But it is worth being precise about what follows from "
    "this:</b> <b>the model is optimised for <i>plausible continuation</i>, "
    "not for <i>correctness</i></b> — and <b>that distinction is "
    "Module 12 &sect;3's entire subject</b> and the origin of the "
    "confident-fabrication failure mode. A fluent false answer is a "
    "<i>successful</i> continuation by the training objective."]),

  ("h1", "2 &nbsp; Counting, and its limit"),
  ("code", """P(w | context) = count(context, w) / count(context)

AND MOST COUNTS ARE ZERO
    a 20,000-word vocabulary gives 8 x 10^12 possible
    trigrams. No corpus covers them. So an unseen
    trigram gets probability 0, and therefore the
    whole sequence gets probability 0.

SMOOTHING, in increasing sophistication
    add-one         simple, and badly biased
    back-off        use the shorter context when the
                    longer one is unseen
    interpolation   mix all orders together with
                    learned weights
    Kneser-Ney      back off by how many DISTINCT
                    contexts a word appears in, not
                    by its raw frequency

KNESER-NEY'S INSIGHT: "Francisco" is frequent but
appears almost only after "San", so it is a poor
back-off candidate. Diversity of context beats raw
frequency."""),
  ("p", "<b>Kneser-Ney's insight is the best idea in classical language "
        "modelling</b>, and it is worth stating as a principle: <b>what "
        "makes a word a good guess in an unfamiliar context is the variety "
        "of contexts it has appeared in, not how often it has "
        "appeared</b>. <b>Which is a statement about generalisation "
        "rather than about counting</b> — and it anticipates the "
        "distributional argument of Module 04 from inside the "
        "count-based paradigm."),
  ("callout", "The real limit is that counting cannot generalise across "
              "similar words",
   ["<b>Having observed 'the cat sat on the mat' a thousand times tells "
    "an n-gram model precisely nothing about 'the dog sat on the "
    "rug'</b> — the contexts are different strings, so the counts "
    "are entirely unrelated, and the model starts from zero.",
    "<b>Which is Module 01 &sect;1's discreteness arriving as a "
    "concrete modelling failure</b> — <b>there is no notion of "
    "similarity between contexts, so every context must be observed "
    "directly</b>, and the number of contexts grows exponentially with "
    "the order.",
    "<b>And smoothing does not fix this.</b> <b>Smoothing "
    "redistributes probability mass toward unseen events; it does not "
    "transfer what was learned about one word to a similar one</b> "
    "— which is a different operation entirely, and no amount of "
    "back-off sophistication achieves it.",
    "<b>So the neural formulation's real advantage is parameter "
    "sharing:</b> <b>'cat' and 'dog' receive nearby vectors, so evidence "
    "about one directly informs predictions about the other</b> — "
    "which is <b>Module 04's subject and the actual reason for the "
    "whole architecture</b>, rather than depth or nonlinearity."]),

  ("break",),
  ("h1", "3 &nbsp; Perplexity"),
  ("eq", "PP = exp( &minus;(1/N) &Sigma;<sub>i</sub> log P(w<sub>i</sub> | "
         "context) )"),
  ("ul", ["<b>The exponentiated average negative log likelihood per "
          "token</b>, computed on held-out text — so it is a direct "
          "function of how surprised the model was.",
          "<b>The interpretation is an effective branching "
          "factor:</b> <b>a perplexity of 100 means the model was as "
          "uncertain as if it were choosing uniformly among 100 "
          "options</b> at each step. Lower is better.",
          "<b>And it depends on the tokenisation</b> — <b>so two "
          "models with different tokenisers are not comparable by "
          "perplexity at all</b> (Module 02), since the same text is "
          "a different number of predictions. <b>This is the trap</b>, "
          "and it makes a good deal of published comparison harder to "
          "read than it looks.",
          "<b>Perplexity numbers are therefore comparable only within "
          "a fixed vocabulary and on a fixed test set</b> — which is "
          "why Project 1 requires all four models to be evaluated on the "
          "identical held-out split, and why that requirement is not "
          "pedantry."]),
  ("ul", ["<b>It does not measure usefulness.</b> <b>A model with "
          "lower perplexity can be worse at your actual task</b>, and "
          "while the correlation is positive it is far from perfect "
          "— which is CSCE 633 Module 12's "
          "choose-the-metric-from-the-use argument.",
          "<b>It is dominated by the frequent, easy tokens</b> — "
          "function words, punctuation, and predictable "
          "continuations — so <b>a large improvement there can mask "
          "no improvement at all on the content words you cared "
          "about</b>. <b>This is the limitation that matters most</b>, "
          "because it means <b>a perplexity gain can be entirely real "
          "and entirely irrelevant.</b>",
          "<b>It is incomparable across tokenisers and across test "
          "sets</b>, as above — and test sets differ in difficulty "
          "far more than is usually acknowledged.",
          "<b>And it rewards hedging.</b> <b>A model that spreads "
          "probability broadly scores better than one that commits and is "
          "occasionally wrong</b> — which is sometimes exactly what "
          "you want and sometimes the opposite (Module 09 &sect;2's "
          "decoding trade).",
          "<b>So use perplexity for development, where its cheapness "
          "and sensitivity are valuable, and report task metrics for any "
          "claim</b> (Module 10) — which is the division of "
          "labour that keeps it useful."]),

  ("h1", "4 &nbsp; The neural formulation"),
  ("code", """1. look up an embedding for each context token
2. combine them somehow (concatenate, average, or a
   sequence model -- Modules 05 and 06)
3. a hidden layer, or several
4. a softmax over the vocabulary

WHAT THIS BUYS
    similar words share parameters, so evidence
        transfers between them
    the context can be arbitrarily long, in principle
    and the model size does not grow with the number
        of observed contexts

WHAT IT COSTS
    the softmax over a large vocabulary is the
        expensive part -- which is why sampled
        softmax, hierarchical softmax, and subword
        vocabularies (Module 02) all exist
    and it needs far more computation per prediction
        than a table lookup does"""),
  ("p", "<b>Parameter sharing between similar words is the whole "
        "gain</b> — <b>everything else in that architecture is "
        "machinery to make the sharing affordable</b>, and keeping that "
        "straight prevents the common mistake of attributing the "
        "improvement to depth or to nonlinearity. <b>The original neural "
        "language model was shallow and still beat heavily tuned n-gram "
        "models</b>, because sharing was the thing that mattered."),
  ("callout", "And this is where the course's arc begins",
   ["<b>Module 04 asks where the embeddings in step 1 come "
    "from</b>, and finds that they can be learned from co-occurrence "
    "statistics alone — without any labels at all.",
    "<b>Module 05 asks how to combine a variable-length context in "
    "step 2</b>, and finds that recurrence works in principle and forgets "
    "in practice.",
    "<b>Module 06 replaces recurrence with attention</b>, which "
    "fixes the forgetting and parallelises the computation — two "
    "unrelated benefits from one change, which is why it won so "
    "decisively.",
    "<b>And Module 07 observes that the resulting model, trained at "
    "scale on this same free objective, turns out to be useful for "
    "essentially everything</b> — which is where the field "
    "currently is, and is &sect;1's callout vindicated at a scale nobody "
    "predicted."]),
 ],
 "resources": [
   ("Jurafsky & Martin, chapters 3 and 7 (free)",
    "https://web.stanford.edu/~jurafsky/slp3/",
    "<b>&sect;1 through &sect;4</b>, with the smoothing derivations and "
    "the perplexity discussion done properly."),
   ("Chen & Goodman &mdash; An Empirical Study of Smoothing Techniques "
    "(free)",
    "https://aclanthology.org/P96-1041/",
    "<b>&sect;2's comparison, settled empirically</b> — the study "
    "that established Kneser-Ney as the default."),
   ("Bengio et al. &mdash; A Neural Probabilistic Language Model (free)",
    "https://www.jmlr.org/papers/v3/bengio03a.html",
    "<b>&sect;4 in the original</b>, from 2003 — and the parameter "
    "sharing argument is made explicitly, which is why it is worth "
    "reading."),
   ("Jelinek &mdash; the history of statistical language modelling",
    "https://aclanthology.org/J09-4005/",
    "<b>&sect;1 and &sect;2 in context</b> — how the field arrived at "
    "the next-token formulation, by somebody who was there."),
 ],
 "exercises": [
   "<b>Write out the chain rule factorisation</b> and say which part is "
   "exact.",
   "<b>Build a trigram model</b> on a corpus and count how many of its "
   "possible trigrams were observed.",
   "<b>Evaluate it on held-out text</b> without smoothing, and report "
   "what happens.",
   "<b>Add back-off, then interpolation, then Kneser-Ney</b>, and "
   "compare perplexities.",
   "<b>Explain the Francisco example</b> in your own words.",
   "<b>Demonstrate the generalisation failure</b>: train on 'cat' "
   "contexts and test on 'dog' ones.",
   "<b>Compute perplexity with two different tokenisers</b> and show the "
   "numbers are incomparable.",
   "<b>Measure perplexity on function words and content words "
   "separately</b>, and report the gap.",
   "<b>Build a neural language model</b> with learned embeddings and "
   "compare on the same split.",
   "<b>Attribute the improvement</b> to sharing rather than to depth, "
   "by ablating the hidden layer.",
 ],
 "selfcheck": [
   "What does a language model compute, and which part is exact?",
   "Why does next-token prediction suffice for tasks it never saw?",
   "What is the model actually optimised for, and what follows?",
   "Why are most n-gram counts zero?",
   "Name four smoothing methods and state Kneser-Ney's insight.",
   "Why can counting not generalise, and why does smoothing not fix "
   "it?",
   "Define perplexity and give its interpretation.",
   "Why is perplexity incomparable across tokenisers?",
   "Give four things perplexity does not measure, and the worst of "
   "them.",
   "What is the whole gain of the neural formulation?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Word Representations",
 "subtitle": "Meaning from co-occurrence, and the limits of one vector.",
 "question": "Can you learn what a word means from the company it keeps?",
 "outcomes": [
     "State the distributional hypothesis and its scope.",
     "Explain how the embedding objectives work.",
     "Explain what the geometry does and does not encode.",
     "Explain why one vector per word is insufficient.",
     "Train and probe embeddings.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The hypothesis",
   "blurb": "An empirical claim that turned out to be productive."},

  {"t": "callout", "title": "Words appearing in similar contexts tend to have similar meanings",
   "kind": "The distributional hypothesis",
   "body": ["<b>It is an empirical claim rather than a definition</b> "
            "— and <b>it is true enough to be extremely "
            "useful</b>, which is the only standard that matters "
            "here.",
            "<b>So it converts an apparently semantic problem into a "
            "counting problem:</b> <b>represent a word by the "
            "distribution of contexts it occurs in, and similar words get "
            "similar representations.</b>",
            "<b>Which solves Module 03 §2's "
            "generalisation failure</b> — <b>'cat' and 'dog' now "
            "<i>are</i> close, so evidence transfers</b>, and it does so "
            "without any labelled data.",
            "<b>And the limit is in the word 'tend'.</b> "
            "<b>Antonyms occur in near-identical contexts</b>, so "
            "'hot' and 'cold' come out similar — which is correct "
            "distributionally and wrong semantically, and is "
            "Part 3's problem."]},

  {"t": "code", "kicker": "Objectives", "title": "The three ways to get there",
   "lang": "text", "code": """
  COUNT AND FACTORISE
      build a word x context count matrix, reweight
      it (PPMI), and reduce the dimension (SVD).
      Classical, interpretable, and it works.

  PREDICT (word2vec)
      skip-gram: given a word, predict its context
      CBOW:      given the context, predict the word
      trained with negative sampling, so the softmax
      over the vocabulary is avoided

  GLOBAL + LOCAL (GloVe)
      fit the vectors so that the dot product
      predicts the log co-occurrence count directly

  AND THEY ARE CLOSELY RELATED: skip-gram with
  negative sampling is implicitly factorising a
  shifted PMI matrix. The prediction framing and the
  counting framing are the same thing viewed
  differently.
""",
   "caption": "<b>The equivalence result matters</b> — it means "
              "the neural framing was a better optimiser rather than a "
              "different idea.",
   "note": "Levy and Goldberg's result is the one to cite here."},

  {"t": "section", "label": "Part 2", "title": "The geometry",
   "blurb": "What the space encodes."},

  {"t": "bullets", "kicker": "Structure", "title": "What you get, and what to be careful about",
   "items": [
     "<b>Nearest neighbours are genuinely "
     "meaningful</b> — the neighbours of 'Paris' are other "
     "cities, which is a real and useful result from counting "
     "alone.",
     "",
     "<b>Directions encode relations</b>, approximately — the "
     "vector offset between a country and its capital is roughly "
     "consistent across pairs.",
     "",
     "<b>And the analogy arithmetic works, with caveats:</b> "
     "<b>the standard evaluation excludes the three input words from "
     "the answer</b>, without which many analogies return an input "
     "instead.",
     "",
     "<b>So the structure is real and weaker than the famous "
     "demonstrations suggest</b> — which is worth knowing before "
     "building on it.",
     "",
     "<b>And the space has no notion of negation, "
     "quantification, or composition</b> — it is a similarity "
     "space, not a semantics.",
   ],
   "footnote": "<b>The excluded-inputs caveat is the honest "
               "footnote</b> on the most-cited result in the "
               "area — and it is routinely omitted."},

  {"t": "section", "label": "Part 3", "title": "What it gets wrong",
   "blurb": "Three failures, all structural."},

  {"t": "callout", "title": "One vector per word type cannot represent a word with two meanings",
   "kind": "The decisive limitation",
   "body": ["<b>'Bank' has a single vector, which must serve both the "
            "financial and the riverside sense</b> — so it ends up "
            "somewhere between them, representing neither.",
            "<b>Which is Module 01 §2's lexical "
            "ambiguity, unresolved</b> — and the resolution requires "
            "the representation to depend on the sentence rather than "
            "only on the word.",
            "<b>And the same applies to any word whose meaning shifts "
            "by domain</b> — 'cell', 'charge', 'model' — which "
            "is most interesting vocabulary.",
            "<b>So this is the limitation that forced contextual "
            "representations</b> (Module 07) — <b>and it is a "
            "limitation of the <i>object</i>, not of the training "
            "method</b>, so no better objective fixes it."]},

  {"t": "bullets", "kicker": "Failures", "title": "And the other two",
   "items": [
     "<b>Antonyms are distributionally similar.</b> <b>'Hot' and "
     "'cold' appear in nearly identical contexts</b>, so they are "
     "near neighbours — which is catastrophic for sentiment and "
     "for entailment.",
     "",
     "<b>And the embeddings encode the corpus's social "
     "biases</b>, measurably — occupational, gendered, and "
     "racial associations appear in the geometry because they appear in "
     "the text (Module 12 §2).",
     "",
     "<b>Which is not a bug in the method:</b> <b>the method "
     "faithfully represents the distribution it was given</b>, and the "
     "distribution contains the bias.",
     "",
     "<b>So debiasing the vectors treats a symptom</b> — and "
     "<b>the measured result is that it hides the association rather "
     "than removing it.</b>",
     "",
     "<b>Which is a general warning about post-hoc "
     "corrections.</b>",
   ],
   "footnote": "<b>'Faithfully represents the distribution it was "
               "given' is the sentence to remember</b> — it applies "
               "to every model in this course, not only to "
               "embeddings."},

  {"t": "section", "label": "Part 4", "title": "Using them",
   "blurb": "And when they are still the right tool."},

  {"t": "bullets", "kicker": "Practice", "title": "Where static embeddings still earn their place",
   "items": [
     "<b>When you need speed.</b> <b>A lookup table is "
     "approximately free</b>, and a contextual model is not — "
     "which matters at retrieval scale "
     "(CSCE 670).",
     "",
     "<b>When you have little data.</b> <b>Pretrained embeddings "
     "plus a simple classifier is a strong, cheap "
     "baseline</b> — and Module 10 §2 requires you "
     "to beat it.",
     "",
     "<b>For analysis.</b> <b>Measuring semantic change over time, "
     "or bias in a corpus, is easier with one vector per "
     "word</b> than with a contextual model.",
     "",
     "<b>And for initialisation</b>, which was their original "
     "role and is now largely superseded.",
     "",
     "<b>But for anything compositional or ambiguous, use "
     "contextual representations</b> (Module 07).",
   ],
   "footnote": "<b>The baseline role is the one to remember</b> "
               "— embeddings plus logistic regression is the "
               "baseline a great many published systems fail to "
               "beat convincingly."},
 ],
 "takeaways": [
   "The distributional hypothesis is an empirical claim that is true enough "
   "to be useful, which converts a semantic problem into a counting one.",
   "Skip-gram with negative sampling implicitly factorises a shifted PMI "
   "matrix, so the prediction and counting framings are the same thing.",
   "The analogy result requires excluding the three input words, and that "
   "caveat is routinely omitted.",
   "One vector per word type cannot represent two senses, and that is a "
   "limitation of the object rather than of the training method.",
   "Antonyms are distributionally similar, which is catastrophic for "
   "sentiment and entailment.",
   "The method faithfully represents the distribution it was given, which "
   "is why debiasing the vectors hides rather than removes the "
   "association.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The distributional hypothesis"),
  ("callout", "Words appearing in similar contexts tend to have similar "
              "meanings",
   ["<b>It is an empirical claim rather than a definition</b> — "
    "Firth's formulation, 'you shall know a word by the company it "
    "keeps' — and <b>it is true enough to be extremely useful</b>, "
    "which is the only standard that matters for this purpose.",
    "<b>So it converts an apparently semantic problem into a counting "
    "problem:</b> <b>represent a word by the distribution of contexts it "
    "occurs in, and similar words automatically receive similar "
    "representations.</b> No labels, no lexicon, no annotation.",
    "<b>Which solves Module 03 &sect;2's generalisation "
    "failure</b> — <b>'cat' and 'dog' now genuinely <i>are</i> "
    "close in the representation, so evidence about one transfers to the "
    "other</b> — and it does so from raw text alone, which is "
    "Module 01 &sect;3's argument delivering its first concrete "
    "result.",
    "<b>And the limitation is hiding in the word 'tend'.</b> "
    "<b>Antonyms occur in near-identical contexts</b> — anything you "
    "can say is hot you can say is cold — so <b>'hot' and 'cold' "
    "come out as close neighbours</b>, which is <b>entirely correct "
    "distributionally and badly wrong semantically</b>, and is "
    "&sect;3's problem."]),
  ("code", """COUNT AND FACTORISE
    build a word x context count matrix, reweight it
    (positive pointwise mutual information), and
    reduce the dimension (SVD). Classical,
    interpretable, and it works well.

PREDICT (word2vec)
    skip-gram: given a word, predict its context
    CBOW:      given the context, predict the word
    trained with negative sampling, so the expensive
    softmax over the vocabulary is avoided entirely

GLOBAL + LOCAL (GloVe)
    fit the vectors so that their dot product predicts
    the log co-occurrence count directly

AND THEY ARE CLOSELY RELATED: skip-gram with negative
sampling is implicitly factorising a shifted PMI
matrix. The prediction framing and the counting
framing are the same thing viewed differently."""),
  ("p", "<b>The equivalence result matters more than it is usually "
        "given credit for.</b> <b>Levy and Goldberg showed that "
        "skip-gram with negative sampling is implicitly factorising a "
        "shifted pointwise mutual information matrix</b> — which "
        "means <b>the neural framing was a better <i>optimiser</i> rather "
        "than a different <i>idea</i></b>. That is a useful corrective to "
        "the narrative that neural methods replaced counting: they "
        "computed the same thing more scalably, and the distributional "
        "hypothesis was doing the work in both."),

  ("h1", "2 &nbsp; The geometry"),
  ("ul", ["<b>Nearest neighbours are genuinely meaningful</b> — "
          "the neighbours of 'Paris' are other cities, the neighbours of "
          "'November' are other months — which is <b>a real and "
          "useful result obtained from counting alone</b>, and was "
          "surprising when first demonstrated.",
          "<b>Directions encode relations, approximately</b> — the "
          "vector offset between a country and its capital is roughly "
          "consistent across many such pairs, which means the space has "
          "learned something structural rather than only similarity.",
          "<b>And the analogy arithmetic works, with a caveat that "
          "matters:</b> <b>the standard evaluation excludes the three "
          "input words from the candidate answers</b>, and <b>without "
          "that exclusion a large share of analogies return one of the "
          "inputs</b> rather than the intended answer.",
          "<b>So the structure is real and considerably weaker than "
          "the famous demonstrations suggest</b> — which is worth "
          "knowing before building anything on vector arithmetic, and "
          "<b>the excluded-inputs caveat is the honest footnote on the "
          "most-cited result in the area</b> and is routinely omitted.",
          "<b>And the space has no notion of negation, "
          "quantification, or composition</b> — <b>it is a "
          "similarity space, not a semantics</b>. There is no vector "
          "operation corresponding to 'not', and averaging the words of a "
          "sentence loses the word order entirely, which is "
          "Module 01 &sect;1's compositionality row still "
          "unaddressed."]),

  ("break",),
  ("h1", "3 &nbsp; What it gets wrong"),
  ("callout", "One vector per word type cannot represent a word with two "
              "meanings",
   ["<b>'Bank' has a single vector, which must serve both the financial "
    "sense and the riverside sense</b> — so it ends up somewhere "
    "between the two, <b>representing neither one well</b> and being a "
    "poor neighbour for both 'money' and 'river'.",
    "<b>Which is Module 01 &sect;2's lexical ambiguity, entirely "
    "unresolved</b> — and <b>the resolution requires the "
    "representation to depend on the sentence</b> rather than only on the "
    "word identity, which no static method can provide.",
    "<b>And the same applies to any word whose meaning shifts by "
    "domain</b> — 'cell', 'charge', 'model', 'bias', 'significant' "
    "— <b>which is most of the interesting vocabulary in any "
    "technical field</b>, and is why domain adaptation mattered so much "
    "in the static era.",
    "<b>So this is the limitation that forced contextual "
    "representations</b> (Module 07) — and crucially, <b>it is a "
    "limitation of the <i>object</i> rather than of the training "
    "method</b>, so <b>no better objective fixes it</b>. You have to "
    "change what you are learning, not how you learn it."]),
  ("ul", ["<b>Antonyms are distributionally similar.</b> <b>'Hot' and "
          "'cold' appear in nearly identical contexts</b>, so they are "
          "near neighbours — <b>which is catastrophic for sentiment "
          "analysis and for entailment</b>, where the distinction is the "
          "entire task.",
          "<b>And the embeddings encode the corpus's social biases, "
          "measurably</b> — occupational, gendered, and racial "
          "associations appear directly in the geometry, and can be "
          "quantified with the same analogy arithmetic that produces the "
          "celebrated examples (Module 12 &sect;2).",
          "<b>Which is not a bug in the method:</b> <b>the method "
          "faithfully represents the distribution it was given</b>, and "
          "the distribution contains the bias because the text does. "
          "<b>That sentence is the one to remember</b> — it applies "
          "to every model in this course, not only to embeddings.",
          "<b>So debiasing the vectors treats a symptom</b> — and "
          "<b>the measured result is that the standard debiasing methods "
          "hide the association rather than removing it</b>: the clusters "
          "remain recoverable, and downstream behaviour changes less than "
          "the metric suggests.",
          "<b>Which is a general warning about post-hoc "
          "corrections</b>, and one worth carrying into Module 12: a "
          "correction that improves the measurement of a problem without "
          "improving the problem is <b>CSCE 701 Module 12</b>'s "
          "Goodhart failure, in a research setting."]),

  ("h1", "4 &nbsp; Where static embeddings still earn their place"),
  ("ul", ["<b>When you need speed.</b> <b>A lookup table is "
          "approximately free, and a contextual model is not</b> — "
          "which matters enormously at retrieval scale, where you may be "
          "embedding millions of documents (CSCE 670 Module 08).",
          "<b>When you have very little data.</b> <b>Pretrained "
          "embeddings plus a simple classifier is a strong and extremely "
          "cheap baseline</b> — and <b>Module 10 &sect;2 requires "
          "you to beat it</b>, which a surprising number of published "
          "systems do not do convincingly.",
          "<b>For analysis.</b> <b>Measuring semantic change over "
          "historical time, or quantifying bias in a corpus, is much "
          "easier with exactly one vector per word</b> than with a "
          "contextual model where there is no single vector to "
          "examine — so the limitation becomes an advantage.",
          "<b>And for initialisation</b>, which was their original role "
          "in neural pipelines and is now largely superseded by "
          "pretraining the whole model (Module 07).",
          "<b>But for anything compositional or ambiguous, use "
          "contextual representations</b> (Module 07) — which is "
          "most real tasks. <b>The baseline role is the one to "
          "remember:</b> embeddings plus logistic regression takes an "
          "hour, costs nothing, and is the number your expensive system "
          "has to beat before it has demonstrated anything."]),
 ],
 "resources": [
   ("Jurafsky & Martin, chapter 6 (free)",
    "https://web.stanford.edu/~jurafsky/slp3/",
    "<b>The whole module</b>, including the PPMI weighting and the "
    "evaluation caveats of &sect;2."),
   ("Mikolov et al., and Pennington et al. &mdash; word2vec and GloVe "
    "(free)",
    "https://arxiv.org/abs/1301.3781",
    "<b>&sect;1's objectives in the originals</b> — both short, and "
    "worth reading for how modest the claims were."),
   ("Levy & Goldberg &mdash; Neural Word Embedding as Implicit Matrix "
    "Factorization (free)",
    "https://papers.nips.cc/paper/5477-neural-word-embedding-as-implicit-matrix-factorization",
    "<b>&sect;1's equivalence result</b> — the paper that connected "
    "the two framings."),
   ("Bolukbasi et al., and Gonen & Goldberg (free)",
    "https://arxiv.org/abs/1607.06520",
    "<b>&sect;3's bias finding, and then the result that debiasing hides "
    "rather than removes it</b> — read both, in that order."),
 ],
 "exercises": [
   "<b>State the distributional hypothesis</b> and say what kind of "
   "claim it is.",
   "<b>Build a word-context count matrix</b>, apply PPMI, and reduce it "
   "with SVD.",
   "<b>Train skip-gram with negative sampling</b> on the same corpus and "
   "compare the neighbours.",
   "<b>Inspect the nearest neighbours</b> of ten words and report which "
   "are meaningful.",
   "<b>Run the analogy arithmetic with and without excluding the "
   "inputs</b>, and report the difference.",
   "<b>Find the vector for an ambiguous word</b> and show it is a poor "
   "neighbour for both senses.",
   "<b>Measure the similarity of five antonym pairs</b> and explain the "
   "result.",
   "<b>Measure one occupational association</b> in your embeddings.",
   "<b>Apply a debiasing method</b> and check whether the clusters are "
   "still recoverable.",
   "<b>Build the embeddings-plus-logistic-regression baseline</b> for "
   "your Project 2 task, and record the score.",
 ],
 "selfcheck": [
   "State the distributional hypothesis and where the limitation "
   "hides.",
   "How does it solve Module 03's generalisation failure?",
   "Name three ways to obtain embeddings and state the equivalence "
   "result.",
   "Why does the equivalence matter?",
   "What does the geometry encode, and what is the analogy caveat?",
   "What does the space have no notion of?",
   "Why can one vector not represent two senses, and why is no better "
   "objective enough?",
   "Why are antonyms similar, and what does that break?",
   "Why is encoded bias not a bug in the method?",
   "Give four places static embeddings still earn their place.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Sequence Models",
 "subtitle": "Recurrence, and the problem it could not solve.",
 "question": "How do you process a variable-length sequence?",
 "outcomes": [
     "Explain the recurrent formulation and its appeal.",
     "Explain vanishing gradients and why depth in time is "
     "different.",
     "Explain gating and what it buys.",
     "Explain the remaining limitations that attention fixed.",
     "Demonstrate a long-range failure experimentally.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Recurrence",
   "blurb": "The obvious idea, and it works."},

  {"t": "eq", "kicker": "RNN", "title": "The formulation",
   "eqs": [
     ("hₜ = σ(W_h hₜ₋₁ + W_x xₜ + b)",
      "One hidden state, updated by the same weights at every step. "
      "The state is the entire memory."),
     ("yₜ = g(W_y hₜ)",
      "Output from the current state, so a prediction is available "
      "at every position."),
     ("parameters independent of sequence length",
      "Which is the appeal: one set of weights handles any length, "
      "and shares statistical strength across positions."),
   ],
   "caption": "<b>Weight sharing across time is the point</b> — the "
              "same parameters apply at position 3 and position 300, "
              "which is what makes variable length tractable.",
   "note": "Connect to CSCE 636's convolution weight sharing — "
           "same idea, different axis."},

  {"t": "callout", "title": "The state is a fixed-size summary of an unbounded past, which is the whole problem",
   "kind": "Where the limitation comes from",
   "body": ["<b>Everything the model knows about the first 300 tokens "
            "must fit in one vector</b> — and that vector is "
            "overwritten, partially, at every step.",
            "<b>Which is a hard information bottleneck.</b> <b>A "
            "fixed-dimensional state cannot retain arbitrary amounts of "
            "detail about an arbitrarily long prefix</b>, so something "
            "must be discarded.",
            "<b>And the model has to learn <i>what</i> to "
            "discard</b> — which it does imperfectly, and which "
            "depends on information about the future it does not "
            "have.",
            "<b>So recurrence is theoretically sufficient and "
            "practically limited</b> — <b>a recurrent network is a "
            "universal sequence approximator and still cannot be trained "
            "to use its own capacity</b> (Part 2)."]},

  {"t": "section", "label": "Part 2", "title": "Vanishing gradients",
   "blurb": "Why depth in time is worse than depth in layers."},

  {"t": "code", "kicker": "The gradient", "title": "Why the signal dies",
   "lang": "text", "code": """
  Backpropagating from step t to step t-k multiplies
  by the recurrent Jacobian k times:

      dL/dh_{t-k} ~ (W_h)^k  x  (activation
                                 derivatives)^k

  SO
      largest eigenvalue < 1  ->  vanishes
      largest eigenvalue > 1  ->  explodes

  AND NEITHER IS A STABLE MIDDLE. The exponent is the
  distance in time, so a 100-step dependency needs 100
  multiplications to survive.

  THE PARTIAL FIXES
      gradient clipping          stops exploding
      careful initialisation     delays vanishing
      shorter truncation windows cheaper, and gives up
                                 the long range
      and gating (Part 3), which is the real one

  COMPARE CSCE 636 Module 04: a residual connection
  fixes depth in LAYERS by adding an identity path.
  Gating is the same move, along the time axis.
""",
   "caption": "<b>The exponent is the distance in time</b>, which is "
              "why this is qualitatively worse than ordinary depth.",
   "note": "The residual-connection parallel makes gating intuitive."},

  {"t": "section", "label": "Part 3", "title": "Gating",
   "blurb": "An additive path through time."},

  {"t": "callout", "title": "An LSTM adds a cell state the network can carry forward unchanged",
   "kind": "What the gates actually do",
   "body": ["<b>The forget gate decides what to drop from the cell "
            "state, the input gate what to add, and the output gate what "
            "to expose</b> — all learned, and all conditioned on the "
            "input and the previous state.",
            "<b>And the cell state's update is "
            "<i>additive</i></b> — <b>which gives the gradient a "
            "path with multiplier near one</b>, so it can travel far "
            "without vanishing.",
            "<b>Which is exactly the residual connection "
            "argument</b> (CSCE 636 §04) <b>applied along the "
            "time axis</b> — and recognising that is what makes "
            "gating memorable rather than arbitrary.",
            "<b>GRUs do the same with fewer gates</b> and perform "
            "comparably — <b>which suggests the additive path "
            "mattered and the specific gate arrangement mattered "
            "less.</b>"]},

  {"t": "bullets", "kicker": "Remaining", "title": "And what gating still did not fix",
   "items": [
     "<b>Sequential computation.</b> <b>Step t needs step "
     "t−1, so the sequence cannot be parallelised during "
     "training</b> — which caps the model and data size you can "
     "afford.",
     "",
     "<b>The bottleneck is relieved, not removed.</b> <b>Long "
     "dependencies still degrade</b>, just more slowly — and the "
     "degradation is gradual rather than cliff-edged, which makes it "
     "easy to miss.",
     "",
     "<b>And the path length between two positions is still "
     "O(distance)</b> — so the model must route information "
     "through every intervening step.",
     "",
     "<b>Which is the specific thing attention "
     "fixes</b> (Module 06): <b>a constant-length path "
     "between any two positions.</b>",
     "",
     "<b>And parallelism, as a second unrelated "
     "benefit.</b>",
   ],
   "footnote": "<b>The two benefits of attention are "
               "independent:</b> constant path length addresses quality, "
               "and parallelism addresses scale — and the second is "
               "arguably why it won."},

  {"t": "section", "label": "Part 4", "title": "Demonstrating it",
   "blurb": "Because you should see the failure yourself."},

  {"t": "code", "kicker": "Experiment", "title": "A task that isolates long-range dependence",
   "lang": "text", "code": """
  THE COPY TASK
      input:  a random sequence, a delimiter, then
              blanks
      target: reproduce the sequence after the
              delimiter
      vary the gap. Accuracy against gap length is the
      measurement.

  WHY IT ISOLATES THE PROPERTY
      nothing about the task is hard except carrying
      information across the gap. No syntax, no
      semantics, no ambiguity.

  WHAT YOU SHOULD SEE
      a plain RNN fails at modest gaps
      an LSTM succeeds much further and then degrades
      a single attention layer handles it flatly

  AND THIS IS PROJECT 1's REQUIREMENT -- construct
  the task, measure the curve, and report where each
  model breaks. Asserting the failure is not enough.
""",
   "caption": "<b>Isolating one property is what makes an experiment "
              "informative</b> — and it is a transferable "
              "experimental habit.",
   "note": "The copy task is the cleanest demonstration available."},

  {"t": "callout", "title": "And where recurrence still appears",
   "kind": "Closing",
   "body": ["<b>Streaming and online settings</b>, where you cannot "
            "see the whole sequence — recurrence is naturally "
            "incremental and attention is not.",
            "<b>Very long sequences</b>, where attention's quadratic "
            "cost is prohibitive — which is why the state-space and "
            "linear-attention families revived recurrent "
            "ideas.",
            "<b>Small models on constrained hardware</b>, where the "
            "parameter and memory cost matters more than the last "
            "increment of quality.",
            "<b>So the honest position is that attention replaced "
            "recurrence for the dominant case rather than for all "
            "cases</b> — and <b>the recurrent formulation is worth "
            "understanding because the arguments recur.</b>"]},
 ],
 "takeaways": [
   "Weight sharing across time is recurrence's appeal — one parameter "
   "set for any length, which is the same move as convolution on a "
   "different axis.",
   "The hidden state is a fixed-size summary of an unbounded past, which is "
   "a hard information bottleneck.",
   "The gradient's exponent is the distance in time, which makes depth in "
   "time qualitatively worse than depth in layers.",
   "Gating gives the gradient an additive path, which is the residual "
   "connection argument applied along the time axis.",
   "Attention's two benefits are independent: constant path length "
   "addresses quality, and parallelism addresses scale.",
   "Isolate one property in an experiment — the copy task is hard "
   "only in carrying information across a gap.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Recurrence"),
  ("eq", "h<sub>t</sub> = &sigma;(W<sub>h</sub> h<sub>t&minus;1</sub> + "
         "W<sub>x</sub> x<sub>t</sub> + b)"),
  ("ul", ["<b>One hidden state, updated by the same weights at every "
          "step</b> — and <b>the state is the entire memory</b> of "
          "everything seen so far, which is &sect;1's callout.",
          "<b>The output is computed from the current state</b>, so a "
          "prediction is available at every position, which makes the "
          "formulation natural for tagging and for language modelling "
          "alike.",
          "<b>And the parameters are independent of the sequence "
          "length</b> — <b>which is the appeal: one set of weights "
          "handles any length, and shares statistical strength across all "
          "positions</b> rather than learning each position "
          "separately.",
          "<b>Weight sharing across time is the point</b>, and it is "
          "worth connecting to <b>CSCE 636 Module 05's convolution, "
          "which shares weights across space</b> — <b>the same idea "
          "on a different axis</b>, with the same justification: the "
          "pattern you are looking for can occur anywhere, so the "
          "detector should not depend on position."]),
  ("callout", "The state is a fixed-size summary of an unbounded past, which "
              "is the whole problem",
   ["<b>Everything the model knows about the first three hundred tokens "
    "must fit into one vector</b> — and <b>that vector is "
    "overwritten, at least partially, at every single step</b>.",
    "<b>Which is a hard information bottleneck rather than a tuning "
    "issue.</b> <b>A fixed-dimensional state cannot retain arbitrary "
    "amounts of detail about an arbitrarily long prefix</b>, by counting, "
    "so something must be discarded at every step.",
    "<b>And the model has to learn <i>what</i> to discard</b> — "
    "which it does imperfectly, and which <b>depends on information "
    "about the future that it does not have</b>: whether a detail matters "
    "depends on what is asked later.",
    "<b>So recurrence is theoretically sufficient and practically "
    "limited.</b> <b>A recurrent network is a universal sequence "
    "approximator and still cannot be <i>trained</i> to use its own "
    "capacity</b> over long distances — and that gap between "
    "representational capacity and trainability is &sect;2's subject and "
    "one of the most instructive patterns in the whole of deep learning "
    "(CSCE 636 Module 04)."]),

  ("h1", "2 &nbsp; Vanishing gradients"),
  ("code", """Backpropagating from step t to step t-k multiplies by
the recurrent Jacobian k times:

    dL/dh_{t-k} ~ (W_h)^k  x  (activation
                               derivatives)^k

SO
    largest eigenvalue < 1  ->  the gradient vanishes
    largest eigenvalue > 1  ->  the gradient explodes

AND NEITHER IS A STABLE MIDDLE. The exponent is the
distance in time, so a 100-step dependency needs 100
multiplications for the signal to survive.

THE PARTIAL FIXES
    gradient clipping          stops exploding
    careful initialisation     delays vanishing
    shorter truncation windows cheaper, and gives up
                               the long range entirely
    and gating (section 3), which is the real one

COMPARE CSCE 636 Module 04: a residual connection
fixes depth in LAYERS by adding an identity path.
Gating is the same move, along the time axis."""),
  ("p", "<b>The exponent is the distance in time</b>, <b>which is why "
        "this is qualitatively worse than ordinary depth</b>: a fifty-layer "
        "network has a fixed and manageable depth, whereas a sequence model "
        "on a thousand-token input has an effective depth of a thousand, "
        "with the same multiplicative structure. <b>The problem scales "
        "with the input rather than with the architecture</b>, which is "
        "what makes it the binding constraint."),

  ("break",),
  ("h1", "3 &nbsp; Gating"),
  ("callout", "An LSTM adds a cell state the network can carry forward "
              "unchanged",
   ["<b>The forget gate decides what to drop from the cell state, the "
    "input gate decides what to add, and the output gate decides what to "
    "expose to the rest of the network</b> — all three learned, and "
    "all conditioned on the current input and the previous state.",
    "<b>And crucially, the cell state's update is "
    "<i>additive</i></b> — <b>which gives the gradient a path with "
    "a multiplier near one</b>, so <b>it can travel a long way without "
    "vanishing</b>, because adding does not shrink the signal the way "
    "repeated multiplication does.",
    "<b>Which is exactly the residual connection argument</b> "
    "(CSCE 636 Module 04) <b>applied along the time axis instead of "
    "the layer axis</b> — and <b>recognising that is what makes "
    "gating memorable rather than an arbitrary arrangement of "
    "sigmoids</b>. The LSTM predates ResNets by nearly two decades and "
    "contains the same insight.",
    "<b>GRUs achieve much the same with fewer gates</b> and perform "
    "comparably across most tasks — <b>which strongly suggests that "
    "the additive path was what mattered and that the specific gate "
    "arrangement mattered considerably less</b>, a conclusion the "
    "ablation literature supports."]),
  ("ul", ["<b>Sequential computation.</b> <b>Step t requires step "
          "t&minus;1, so the sequence cannot be parallelised during "
          "training</b> — which directly caps the model size and "
          "data volume you can afford, and was the binding constraint on "
          "scale before 2017.",
          "<b>The bottleneck is relieved rather than removed.</b> "
          "<b>Long dependencies still degrade</b>, merely more "
          "slowly — and <b>the degradation is gradual rather than "
          "cliff-edged, which makes it easy to miss</b> in aggregate "
          "metrics and is why &sect;4's constructed task matters.",
          "<b>And the path length between two positions remains "
          "O(distance)</b> — <b>so the model must route information "
          "through every single intervening step</b>, each of which can "
          "corrupt or discard it.",
          "<b>Which is the specific thing attention fixes</b> "
          "(Module 06): <b>a constant-length path between any two "
          "positions</b>, regardless of how far apart they are.",
          "<b>And parallelism, as a second and entirely unrelated "
          "benefit.</b> <b>The two benefits of attention are "
          "independent:</b> <b>constant path length addresses quality, "
          "and parallelism addresses scale</b> — and <b>the second "
          "is arguably why it won</b>, since it unlocked the data and "
          "parameter scales that Module 07 depends on."]),

  ("h1", "4 &nbsp; Demonstrating the failure"),
  ("code", """THE COPY TASK
    input:  a random sequence, a delimiter, then
            blanks
    target: reproduce the sequence after the delimiter
    vary the gap. Accuracy against gap length is the
    measurement.

WHY IT ISOLATES THE PROPERTY
    nothing about the task is hard except carrying
    information across the gap. No syntax, no
    semantics, no ambiguity, no world knowledge.

WHAT YOU SHOULD SEE
    a plain RNN fails at quite modest gaps
    an LSTM succeeds much further and then degrades
    a single attention layer handles it flatly

AND THIS IS PROJECT 1's REQUIREMENT -- construct the
task, measure the curve, and report where each model
breaks. Asserting the failure is not enough; the
construction is what is graded."""),
  ("callout", "And where recurrence still appears",
   ["<b>Streaming and online settings</b>, where you cannot see the "
    "whole sequence before producing output — <b>recurrence is "
    "naturally incremental and attention is not</b>, which matters for "
    "real-time transcription and for very low-latency applications.",
    "<b>Very long sequences</b>, where attention's quadratic cost in "
    "length becomes prohibitive — <b>which is precisely why the "
    "state-space and linear-attention model families revived recurrent "
    "ideas</b>, and did so with the gradient problem addressed by "
    "construction rather than by gating.",
    "<b>Small models on constrained hardware</b>, where the parameter "
    "count and the memory cost matter more than the last increment of "
    "quality — a recurrent model's memory does not grow with the "
    "sequence length, and attention's does.",
    "<b>So the honest position is that attention replaced recurrence "
    "for the dominant case rather than for all cases</b> — and "
    "<b>the recurrent formulation is worth understanding because the "
    "arguments recur</b>, literally: the bottleneck, the gradient path, "
    "and the parallelism trade all reappear whenever somebody proposes an "
    "alternative to attention."]),
 ],
 "resources": [
   ("Jurafsky & Martin, chapter 9 (free)",
    "https://web.stanford.edu/~jurafsky/slp3/",
    "<b>&sect;1 through &sect;3</b>, with the LSTM equations written out "
    "carefully."),
   ("Olah &mdash; Understanding LSTM Networks (free)",
    "https://colah.github.io/posts/2015-08-Understanding-LSTMs/",
    "<b>&sect;3 as the clearest available explanation</b> — the "
    "diagrams are what make the gates click."),
   ("Pascanu et al. &mdash; On the difficulty of training RNNs (free)",
    "https://arxiv.org/abs/1211.5063",
    "<b>&sect;2's analysis in the original</b>, including the clipping "
    "argument and the eigenvalue condition."),
   ("Hochreiter & Schmidhuber &mdash; Long Short-Term Memory (free)",
    "https://www.bioinf.jku.at/publications/older/2604.pdf",
    "<b>&sect;3 in the original</b>, from 1997 — and the "
    "constant-error-carousel framing is the additive path argument stated "
    "plainly."),
 ],
 "exercises": [
   "<b>Implement a plain RNN</b> and train it on a short sequence "
   "task.",
   "<b>Plot the gradient norm against time distance</b> and observe "
   "it.",
   "<b>Add gradient clipping</b> and report which problem it fixes and "
   "which it does not.",
   "<b>Implement an LSTM</b> and identify the additive path in your own "
   "code.",
   "<b>Explain the parallel to residual connections</b> in your own "
   "words.",
   "<b>Build the copy task</b> with a configurable gap.",
   "<b>Measure accuracy against gap length</b> for RNN, LSTM, and "
   "attention.",
   "<b>Report where each breaks</b>, with the curve.",
   "<b>Time one training epoch</b> for a recurrent and an attention "
   "model on the same data.",
   "<b>Explain why the recurrent one cannot be parallelised.</b>",
 ],
 "selfcheck": [
   "Give the recurrent formulation and say what its appeal is.",
   "What does recurrence share with convolution?",
   "Why is a fixed-size state a hard bottleneck?",
   "What is the gap between capacity and trainability?",
   "Why does the gradient vanish or explode, and what is the "
   "exponent?",
   "Why is depth in time worse than depth in layers?",
   "What do the three LSTM gates do, and which property matters most?",
   "What does gating share with residual connections?",
   "Name three things gating did not fix.",
   "Why does the copy task isolate the property, and where does "
   "recurrence still appear?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "The Transformer",
 "subtitle": "Attention, completely.",
 "question": "What does attention compute, and why did it win?",
 "outcomes": [
     "Explain attention as a differentiable lookup.",
     "Explain multi-head attention and what heads do.",
     "Explain positional encoding and why it is needed.",
     "Explain the full block and the training objectives.",
     "Implement the architecture.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Attention",
   "blurb": "A soft dictionary lookup."},

  {"t": "eq", "kicker": "Attention", "title": "The operation, in one line",
   "eqs": [
     ("Attention(Q, K, V) = softmax(QKᵀ / √d) V",
      "Each query is compared against every key; the softmax weights "
      "become a weighted average of the values."),
     ("the √d scaling",
      "Without it, large d makes the dot products large, the softmax "
      "saturates, and the gradient vanishes."),
     ("path length between any two positions: O(1)",
      "Which is Module 05 §3's limitation removed, and the "
      "quality half of the argument."),
   ],
   "caption": "<b>Read it as a lookup:</b> the query asks a question, "
              "the keys advertise what each position offers, and the "
              "values are what gets returned.",
   "note": "The dictionary framing is what makes Q, K, V stop being "
           "arbitrary."},

  {"t": "callout", "title": "Attention is a differentiable dictionary lookup, which is why Q, K, and V are three different things",
   "kind": "The framing that makes it intuitive",
   "body": ["<b>In a hard lookup you have a key and get one "
            "value.</b> <b>Here the query is compared to every key, "
            "producing a similarity distribution, and you get a weighted "
            "average of all the values.</b>",
            "<b>So the three projections have distinct jobs:</b> "
            "<b>the key advertises what information a position holds, the "
            "query expresses what the current position is looking for, "
            "and the value is what is actually transmitted.</b>",
            "<b>Which is why they are separate matrices</b> — "
            "what makes a position worth attending to is not the same as "
            "what you want from it once you do.",
            "<b>And self-attention is the case where all three come "
            "from the same sequence</b> — every position asks every "
            "other position a question, which is what makes it a general "
            "sequence operation."]},

  {"t": "section", "label": "Part 2", "title": "Multiple heads",
   "blurb": "And what they end up doing."},

  {"t": "bullets", "kicker": "Heads", "title": "Why more than one, and what is observed",
   "items": [
     "<b>One attention distribution can only express one "
     "relation</b> — and a position may need its syntactic head, "
     "its coreferent, and its topic simultaneously.",
     "",
     "<b>So run several in parallel on lower-dimensional "
     "projections, and concatenate</b> — which costs about the "
     "same as one full-dimensional head.",
     "",
     "<b>And the observed specialisation is real but "
     "loose:</b> <b>some heads attend to the previous token, some to "
     "syntactic dependents, some to matching brackets</b> — and "
     "many are not interpretable at all.",
     "",
     "<b>With substantial redundancy.</b> <b>A large fraction of "
     "heads can be pruned with little loss</b>, which is a caution "
     "against over-reading any single head.",
     "",
     "<b>So treat head interpretations as suggestive</b>, not as "
     "explanations (Module 13 §3).",
   ],
   "footnote": "<b>The prunability result is the honest "
               "caveat:</b> if most heads can be removed, the story that "
               "each one performs a specific linguistic function cannot "
               "be the whole picture."},

  {"t": "section", "label": "Part 3", "title": "Position",
   "blurb": "Which attention does not know about."},

  {"t": "callout", "title": "Attention is permutation-invariant, so position must be supplied explicitly",
   "kind": "An easy thing to miss and a fatal one to omit",
   "body": ["<b>The operation treats the input as a <i>set</i></b> "
            "— shuffle the positions and the output shuffles "
            "identically. <b>Which makes 'dog bites man' and 'man bites "
            "dog' indistinguishable</b> without extra information.",
            "<b>So position is injected:</b> <b>learned embeddings "
            "per index, fixed sinusoids, or a relative scheme that "
            "modifies the attention scores by distance.</b>",
            "<b>And the choice determines how the model handles "
            "longer inputs than it was trained on</b> — <b>absolute "
            "learned positions do not extrapolate at all</b>, which is "
            "why relative and rotary schemes displaced them.",
            "<b>Which is the practical consequence worth "
            "remembering:</b> <b>a model's usable context length is a "
            "property of its positional scheme as much as of its training "
            "data.</b>"]},

  {"t": "code", "kicker": "The block", "title": "The full architecture",
   "lang": "text", "code": """
  ONE BLOCK
      x = x + MultiHeadAttention(LayerNorm(x))
      x = x + FeedForward(LayerNorm(x))

  AND THAT IS ALL. Stack it N times.

  WHY EACH PIECE
      residual    the gradient path (CSCE 636 M04)
      layer norm  stabilises the scale; the pre-norm
                  placement shown trains more
                  reliably than post-norm
      feedforward per-position capacity; attention
                  mixes across positions and this
                  processes within one. It holds most
                  of the parameters.
      stacking    each layer attends over the previous
                  layer's contextual representations,
                  so the effective receptive
                  structure deepens

  THE MASK IS WHAT DISTINGUISHES THE VARIANTS
      causal mask     -> decoder; each position sees
                         only the past
      no mask         -> encoder; bidirectional
""",
   "caption": "<b>The mask is the only structural difference between "
              "an encoder and a decoder</b> — which is worth "
              "knowing, because the families are usually described as "
              "though they were different architectures.",
   "note": "The mask point collapses a lot of apparent complexity."},

  {"t": "section", "label": "Part 4", "title": "Why it won",
   "blurb": "Two reasons, and the second is bigger."},

  {"t": "bullets", "kicker": "Reasons", "title": "The honest accounting",
   "items": [
     "<b>Constant path length</b>, so long-range dependencies are "
     "learnable (Module 05 §3) — which is the "
     "quality argument.",
     "",
     "<b>And full parallelism across positions during "
     "training</b>, which is <b>the argument that actually "
     "mattered</b>: it made training on far more data with far more "
     "parameters affordable.",
     "",
     "<b>Because the scaling result is what produced the "
     "capability</b> (Module 07) — <b>and the architecture's "
     "contribution was making the scale reachable.</b>",
     "",
     "<b>The cost is quadratic attention</b> in sequence length, "
     "in both time and memory — which is the active research "
     "constraint.",
     "",
     "<b>And a large appetite for data</b>, since it has fewer "
     "built-in assumptions than a convolution or a recurrence does.",
   ],
   "footnote": "<b>Fewer built-in assumptions is a cost at small "
               "scale and an advantage at large scale</b> — which is "
               "the general shape of the inductive bias trade "
               "(CSCE 633 §03)."},

  {"t": "callout", "title": "And the implementation instruction",
   "kind": "Closing",
   "body": ["<b>Implement it once, from the equations, without "
            "copying</b> — single-head attention, then multi-head, "
            "then the block, then the stack.",
            "<b>Because the architecture is genuinely simple and "
            "reads as complicated</b> — and the gap closes entirely "
            "once you have written the four pieces yourself.",
            "<b>Check your implementation against a reference "
            "output</b>, since a transposed matrix or a misplaced mask "
            "produces something that trains badly rather than failing "
            "loudly.",
            "<b>Which is CSCE 711 Project 1's test-vector discipline, "
            "in a different subject</b> — <b>a construction that "
            "matches known outputs is correct in a way that one which "
            "merely runs is not.</b>"]},
 ],
 "takeaways": [
   "Attention is a differentiable dictionary lookup, which is why query, "
   "key, and value are three separate projections with distinct jobs.",
   "The square-root scaling exists because large dimensions would saturate "
   "the softmax and kill the gradient.",
   "Head specialisation is real and loose, and a large fraction of heads "
   "can be pruned — so treat head interpretations as suggestive.",
   "Attention is permutation-invariant, so a model's usable context length "
   "is a property of its positional scheme as much as its training data.",
   "The mask is the only structural difference between an encoder and a "
   "decoder.",
   "Parallelism rather than path length is the reason attention won, "
   "because it made the scale reachable.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Attention"),
  ("eq", "Attention(Q, K, V) = softmax(QK<sup>T</sup> / &radic;d) V"),
  ("ul", ["<b>Each query is compared against every key by dot "
          "product</b>; the softmax turns those similarities into "
          "weights, and <b>the output is a weighted average of the "
          "values.</b>",
          "<b>The &radic;d scaling is not cosmetic.</b> <b>Without "
          "it, a large dimension makes the dot products large, which "
          "saturates the softmax into a near-one-hot distribution and "
          "makes the gradient vanish</b> — so the model cannot "
          "learn to attend softly at all.",
          "<b>And the path length between any two positions is "
          "O(1)</b> — <b>which is Module 05 &sect;3's limitation "
          "removed outright</b>, and is the quality half of &sect;4's "
          "argument.",
          "<b>Read the whole operation as a lookup:</b> <b>the query "
          "asks a question, the keys advertise what each position has to "
          "offer, and the values are what actually gets returned</b> "
          "— which is the framing that makes Q, K, and V stop "
          "looking arbitrary."]),
  ("callout", "Attention is a differentiable dictionary lookup, which is why "
              "Q, K, and V are three different things",
   ["<b>In a hard dictionary lookup you have a key and you get exactly "
    "one value.</b> <b>Here the query is compared against every key, "
    "producing a similarity distribution, and you receive a weighted "
    "average of all the values</b> — which is what makes it "
    "differentiable and therefore learnable.",
    "<b>So the three projections have genuinely distinct jobs:</b> "
    "<b>the key advertises what information a position holds, the query "
    "expresses what the current position is looking for, and the value is "
    "what is actually transmitted when a match occurs.</b>",
    "<b>Which is precisely why they are three separate "
    "matrices</b> — <b>what makes a position worth attending to is "
    "not the same thing as what you want from it once you have decided "
    "to</b>. A position might advertise 'I am a verb' and transmit "
    "something quite different.",
    "<b>And self-attention is simply the case where all three are "
    "computed from the same sequence</b> — <b>every position asks "
    "every other position a question</b>, which is what makes it a "
    "general-purpose sequence operation rather than a mechanism for "
    "aligning two sequences, which is what it was originally invented "
    "for."]),

  ("h1", "2 &nbsp; Multiple heads"),
  ("ul", ["<b>One attention distribution can only express one "
          "relation</b> — and a given position may need its "
          "syntactic head, its coreferent, and its topical context all at "
          "once, which a single softmax cannot provide.",
          "<b>So run several attention operations in parallel on "
          "lower-dimensional projections, and concatenate the "
          "results</b> — which <b>costs approximately the same as "
          "one full-dimensional head</b>, since the dimensions are "
          "divided among them.",
          "<b>And the observed specialisation is real but loose:</b> "
          "<b>some heads reliably attend to the previous token, some to "
          "syntactic dependents, some to matching brackets or "
          "quotes</b> — and <b>many are not interpretable at "
          "all.</b>",
          "<b>With substantial redundancy.</b> <b>A large fraction of "
          "heads can be pruned after training with very little loss of "
          "performance</b>, which is <b>a serious caution against "
          "over-reading any individual head's behaviour.</b>",
          "<b>So treat head interpretations as suggestive rather than "
          "explanatory</b> (Module 13 &sect;3). <b>The prunability "
          "result is the honest caveat:</b> <b>if most heads can be "
          "removed, then the story in which each one performs a specific "
          "linguistic function cannot be the whole picture</b>, and the "
          "attractive attention-map visualisations should be read with "
          "that in mind."]),

  ("break",),
  ("h1", "3 &nbsp; Position"),
  ("callout", "Attention is permutation-invariant, so position must be "
              "supplied explicitly",
   ["<b>The operation treats its input as a <i>set</i></b> — "
    "shuffle the positions and the output shuffles identically, with no "
    "other change. <b>Which makes 'dog bites man' and 'man bites dog' "
    "entirely indistinguishable</b> without additional information, and "
    "is a fatal omission rather than a degradation.",
    "<b>So position is injected explicitly:</b> <b>learned embeddings "
    "indexed by position, fixed sinusoidal functions, or a relative "
    "scheme that modifies the attention scores according to the distance "
    "between positions</b> — with rotary embeddings being the "
    "current common choice.",
    "<b>And the choice determines how the model handles inputs longer "
    "than it was trained on</b> — <b>absolute learned positions do "
    "not extrapolate at all</b>, because position 5000 has no embedding "
    "if training never reached it, <b>which is why relative and rotary "
    "schemes displaced them.</b>",
    "<b>Which is the practical consequence worth remembering:</b> <b>a "
    "model's usable context length is a property of its positional scheme "
    "at least as much as of its training data</b> — so a claimed "
    "context window and a <i>usable</i> context window can differ "
    "substantially, and the difference is measurable (Module 10)."]),
  ("code", """ONE BLOCK
    x = x + MultiHeadAttention(LayerNorm(x))
    x = x + FeedForward(LayerNorm(x))

AND THAT IS ALL. Stack it N times.

WHY EACH PIECE
    residual    the gradient path (CSCE 636 M04)
    layer norm  stabilises the scale; the pre-norm
                placement shown here trains more
                reliably than post-norm does
    feedforward per-position capacity; attention mixes
                ACROSS positions and this processes
                WITHIN one. It holds most of the
                parameters in the model.
    stacking    each layer attends over the previous
                layer's contextual representations, so
                the representations become progressively
                more contextual

THE MASK IS WHAT DISTINGUISHES THE VARIANTS
    causal mask  -> decoder; each position sees only
                    the past, so it can generate
    no mask      -> encoder; fully bidirectional"""),
  ("p", "<b>The mask is the only structural difference between an "
        "encoder and a decoder</b> — which is genuinely worth "
        "knowing, <b>because the two families are usually described as "
        "though they were different architectures</b> when they differ by "
        "one boolean. <b>The attention-mixes-across and "
        "feedforward-processes-within division is the other thing to "
        "retain</b>: it explains why the feedforward layer holds most of "
        "the parameters and why it is the first place people look when "
        "trying to locate stored knowledge."),

  ("h1", "4 &nbsp; Why it won"),
  ("ul", ["<b>Constant path length</b>, so long-range dependencies "
          "are actually learnable (Module 05 &sect;3) — which is "
          "<b>the quality argument</b>, and it is real.",
          "<b>And full parallelism across positions during "
          "training</b>, which is <b>the argument that actually "
          "mattered</b>: <b>it made training on far more data with far "
          "more parameters affordable</b> at a time when recurrence was "
          "the binding constraint on both.",
          "<b>Because the scaling result is what produced the "
          "capability</b> (Module 07) — <b>and the "
          "architecture's real contribution was making the necessary "
          "scale reachable</b> rather than being a better model at "
          "equal scale, which is a more honest account of its "
          "importance.",
          "<b>The cost is quadratic attention</b> in sequence length, "
          "in both time and memory — <b>which is the active research "
          "constraint</b> and the reason for the whole efficient-attention "
          "literature (Module 05 &sect;4's note).",
          "<b>And a large appetite for data</b>, since it carries "
          "fewer built-in assumptions than a convolution's locality or a "
          "recurrence's sequentiality. <b>Fewer built-in assumptions is "
          "a cost at small scale and an advantage at large scale</b> "
          "— which is <b>the general shape of the inductive bias "
          "trade</b> (CSCE 633 Module 03) and explains why "
          "transformers lose to simpler models on small datasets."]),
  ("callout", "And the implementation instruction",
   ["<b>Implement it once, from the equations, without copying</b> "
    "— single-head attention, then multi-head, then one block, then "
    "the stack. Four steps, and a long afternoon.",
    "<b>Because the architecture is genuinely simple and reads as "
    "complicated</b> — and <b>the gap closes entirely once you have "
    "written the four pieces yourself</b>, which is the single most "
    "worthwhile exercise in this course.",
    "<b>Check your implementation against a reference output</b>, "
    "because <b>a transposed matrix or a misplaced mask produces "
    "something that trains badly rather than failing loudly</b> — "
    "the commonest outcome is a model that learns something, just worse, "
    "and you will not know why.",
    "<b>Which is CSCE 711 Project 1's test-vector discipline arriving "
    "in a different subject</b> — <b>a construction that matches "
    "known outputs is correct in a way that one which merely runs is "
    "not</b>, and the habit transfers to everything."]),
 ],
 "resources": [
   ("Vaswani et al. &mdash; Attention Is All You Need (free)",
    "https://arxiv.org/abs/1706.03762",
    "<b>The original.</b> Short, readable, and the ablations in it are "
    "more informative than the architecture diagram."),
   ("The Illustrated Transformer (free)",
    "https://jalammar.github.io/illustrated-transformer/",
    "<b>&sect;1 through &sect;3 visually</b> — read this first if the "
    "equations are not landing."),
   ("The Annotated Transformer (free)",
    "https://nlp.seas.harvard.edu/annotated-transformer/",
    "<b>&sect;4's implementation instruction, done for you</b> — use "
    "it to check your own version rather than to replace writing one."),
   ("Michel et al. &mdash; Are Sixteen Heads Really Better than One? "
    "(free)",
    "https://arxiv.org/abs/1905.10650",
    "<b>&sect;2's prunability result</b>, which is the honest caveat on "
    "head interpretation."),
 ],
 "exercises": [
   "<b>Implement single-head attention</b> from the equation and check "
   "it against a reference.",
   "<b>Remove the √d scaling</b> and observe what happens to the "
   "softmax and the gradient.",
   "<b>Explain the roles of Q, K, and V</b> in the lookup framing.",
   "<b>Implement multi-head attention</b> and confirm the parameter "
   "count matches one full head.",
   "<b>Visualise several heads</b> on a sentence, and find one that is "
   "interpretable and one that is not.",
   "<b>Prune half the heads</b> and measure the loss.",
   "<b>Shuffle the input positions</b> with positional encoding removed, "
   "and confirm the output is invariant.",
   "<b>Compare absolute and relative schemes</b> on inputs longer than "
   "training.",
   "<b>Build the full block and stack it</b>, then train on a small "
   "task.",
   "<b>Change only the mask</b> and confirm you have turned an encoder "
   "into a decoder.",
 ],
 "selfcheck": [
   "Write the attention equation and explain each factor.",
   "Why is the √d scaling necessary?",
   "Why are Q, K, and V three separate projections?",
   "Why use multiple heads, and what is actually observed?",
   "What does the prunability result imply about head "
   "interpretation?",
   "Why is positional information necessary, and what are the three "
   "schemes?",
   "What determines a model's usable context length?",
   "Give the block, and say why each piece is there.",
   "What is the only structural difference between an encoder and a "
   "decoder?",
   "Give the two reasons attention won, and say which mattered more.",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Pretraining and Transfer",
 "subtitle": "Why training on everything beats training on your task.",
 "question": "Why does a model trained on raw text help with your problem?",
 "outcomes": [
     "Explain the pretraining objectives and what each suits.",
     "Explain why transfer works unusually well here.",
     "Explain contextual representations and what they fixed.",
     "Explain scaling and what it does and does not deliver.",
     "Choose a pretrained model for a task.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The objectives",
   "blurb": "Three, and the choice determines the use."},

  {"t": "table", "kicker": "Objectives", "title": "The pretraining objectives",
   "header": ["Objective", "The task", "Suits"],
   "widths": [2.8, 4.2, 4.4],
   "rows": [
     ["<b>Causal LM</b>", "<b>Predict the next token from the left context</b>", "<b>Generation; decoder-only</b>"],
     ["<b>Masked LM</b>", "<b>Predict masked tokens from both sides</b>", "<b>Understanding; encoder-only</b>"],
     ["<b>Span corruption</b>", "<b>Reconstruct deleted spans</b>", "<b>Both; encoder-decoder</b>"],
   ],
   "footnote": "<b>Causal models can generate and see only the left "
               "context; masked models see both sides and cannot "
               "generate</b> — which is the trade, and span "
               "corruption is the attempt to have both.",
   "note": "The bidirectional-versus-generative trade is the "
           "organising fact."},

  {"t": "callout", "title": "The objective is a means, and the representations are the product",
   "kind": "What pretraining is actually for",
   "body": ["<b>Nobody wants a model that fills in masked words.</b> "
            "<b>The objective exists because solving it requires learning "
            "syntax, semantics, and world knowledge</b> "
            "(Module 01 §3).",
            "<b>So the useful output is the internal "
            "representations</b> — and the measure of a pretraining "
            "objective is how useful the representations it produces "
            "are, not how well the objective is solved.",
            "<b>Which explains why masked language modelling uses a "
            "15% masking rate</b> and similar apparently arbitrary "
            "choices: <b>they are tuned for representation quality, not "
            "for the proxy task.</b>",
            "<b>And it explains why causal models dominated:</b> "
            "<b>the objective is harder, uses every token as a "
            "prediction target, and the resulting model can also "
            "generate</b> — which turned out to matter more than "
            "bidirectionality."]},

  {"t": "section", "label": "Part 2", "title": "Contextual representations",
   "blurb": "Module 04's limitation, finally fixed."},

  {"t": "callout", "title": "A pretrained model gives a different vector for each occurrence of a word",
   "kind": "The decisive capability",
   "body": ["<b>'Bank' in a financial sentence and 'bank' by a river "
            "receive different representations</b> — because the "
            "representation is computed from the whole sentence rather "
            "than looked up by word identity.",
            "<b>Which is Module 04 §3's decisive "
            "limitation removed</b>, and it is why pretrained models "
            "improved essentially every task at once rather than one "
            "task at a time.",
            "<b>And the layers differ in what they encode:</b> "
            "<b>lower layers carry more surface and syntactic "
            "information, higher layers more semantic and task-relevant "
            "information</b> — which is a robust finding across "
            "probing studies.",
            "<b>So which layer to use is a real decision</b> — "
            "<b>and 'the last one' is frequently not the best answer</b> "
            "for a task that needs syntax."]},

  {"t": "section", "label": "Part 3", "title": "Why transfer works here",
   "blurb": "Better than in most of machine learning."},

  {"t": "bullets", "kicker": "Transfer", "title": "The reasons, which are specific to language",
   "items": [
     "<b>The pretraining data covers the target "
     "distribution.</b> <b>Nearly any text task involves text like "
     "the pretraining text</b> — which is unusually true here and "
     "is the main reason.",
     "",
     "<b>The required knowledge is shared.</b> <b>Syntax, word "
     "senses, and factual knowledge are needed by every task</b>, so "
     "learning them once serves all of them.",
     "",
     "<b>The objective is genuinely hard</b>, so it forces rich "
     "representations rather than shortcuts — which is not true "
     "of every self-supervised objective.",
     "",
     "<b>And the scale is available.</b> <b>Text is abundant in a "
     "way that labelled examples are not</b> "
     "(Module 01 §3).",
     "",
     "<b>So the gain is largest where labelled data is "
     "smallest</b> — which is most real applications.",
   ],
   "footnote": "<b>The distribution-coverage reason is the one that "
               "does not transfer to other domains</b> — which is "
               "why pretraining worked so much better in language than in "
               "tabular settings (CSCE 633)."},

  {"t": "callout", "title": "Scaling works, and it is worth being precise about what it delivers",
   "kind": "The honest account",
   "body": ["<b>Loss falls predictably with parameters, data, and "
            "compute</b> — a smooth power law over several orders of "
            "magnitude, which is an unusually clean empirical "
            "result.",
            "<b>And the compute-optimal allocation matters:</b> "
            "<b>early large models were substantially "
            "undertrained</b>, and training a smaller model on more data "
            "turned out to be better for the same budget.",
            "<b>What scaling delivers is lower loss, and capability "
            "follows imperfectly.</b> <b>Some abilities improve "
            "smoothly, and some appear to improve sharply</b> — "
            "though <b>the apparent sharpness depends substantially on "
            "the metric</b>, which is Module 10's concern.",
            "<b>And what it does not deliver is reliability.</b> "
            "<b>Larger models are more capable and still "
            "fabricate</b> (Module 12 §3) — so scale "
            "moves the average and not the worst case."]},

  {"t": "section", "label": "Part 4", "title": "Choosing one",
   "blurb": "Which is mostly a constraints question."},

  {"t": "bullets", "kicker": "Choosing", "title": "How to pick a pretrained model",
   "items": [
     "<b>Start from the task shape.</b> <b>Classification or "
     "extraction favours an encoder; generation requires a "
     "decoder</b>; sequence-to-sequence suits an "
     "encoder-decoder.",
     "",
     "<b>Then the domain.</b> <b>A model pretrained on text like "
     "yours beats a larger general one</b> on specialised vocabulary "
     "— clinical, legal, and code especially.",
     "",
     "<b>Then the constraints:</b> latency, memory, cost per "
     "request, and whether the data can leave your "
     "infrastructure.",
     "",
     "<b>Then the licence and the provenance</b>, which is a real "
     "constraint and is routinely discovered late.",
     "",
     "<b>And start with the smallest model that could work</b>, "
     "because <b>iteration speed matters more than capability while "
     "you are still learning what the task needs.</b>",
   ],
   "footnote": "<b>'Smallest model that could work' is the advice most "
               "often ignored</b> — and a fast feedback loop finds "
               "data problems that a slow one hides."},

  {"t": "callout", "title": "And what pretraining does not give you",
   "kind": "Closing",
   "body": ["<b>Knowledge of your specific data</b> — your "
            "schema, your customers, your product's terminology, and "
            "anything after the training cutoff "
            "(Module 11).",
            "<b>Reliable factuality.</b> <b>The model learned what "
            "text looks like, which includes what false text looks "
            "like</b>, and it has no mechanism separating the "
            "two.",
            "<b>Alignment with your task's definition.</b> <b>Your "
            "notion of a 'relevant' document or a 'serious' complaint is "
            "not in the pretraining data</b> — which is what "
            "Module 08 adapts.",
            "<b>And freedom from the corpus's biases</b>, which it "
            "represents faithfully (Module 04 §3's "
            "sentence, and Module 12 §2)."]},
 ],
 "takeaways": [
   "Causal models generate and see only the left context; masked models see "
   "both sides and cannot generate — that is the trade.",
   "The objective is a means and the representations are the product, which "
   "is why the hyperparameters are tuned for representation quality.",
   "A pretrained model gives a different vector per occurrence, which "
   "removes Module 04's decisive limitation.",
   "Lower layers carry surface and syntax, higher layers semantics — "
   "so 'the last layer' is often the wrong choice.",
   "Transfer works unusually well here mainly because the pretraining data "
   "covers the target distribution, which does not generalise to other "
   "domains.",
   "Scaling lowers loss predictably and does not deliver reliability — "
   "it moves the average rather than the worst case.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The objectives"),
  ("table", ["Objective", "The task", "What it suits"],
   [["<b>Causal language modelling</b>",
     "<b>Predict the next token from the left context only.</b>",
     "<b>Generation; decoder-only architectures</b> (Module 06 "
     "&sect;3's causal mask)."],
    ["<b>Masked language modelling</b>",
     "<b>Predict tokens that have been masked out, using the context on "
     "both sides.</b>",
     "<b>Understanding tasks; encoder-only architectures.</b>"],
    ["<b>Span corruption</b>",
     "<b>Reconstruct spans that have been deleted from the input.</b>",
     "<b>Both; encoder-decoder architectures</b> — the attempt to "
     "have bidirectionality and generation together."]],
   [0.22, 0.38, 0.40]),
  ("p", "<b>Causal models can generate and can see only the left "
        "context; masked models see both sides and cannot "
        "generate</b> — <b>which is the fundamental trade</b>, and "
        "span corruption is the attempt to have both at some cost in "
        "efficiency. <b>The bidirectional-versus-generative distinction "
        "is the organising fact of this table</b>, and it follows directly "
        "from Module 06 &sect;3's mask."),
  ("callout", "The objective is a means, and the representations are the "
              "product",
   ["<b>Nobody actually wants a model that fills in masked "
    "words.</b> <b>The objective exists because solving it requires "
    "learning syntax, semantics, and a great deal of world "
    "knowledge</b> — which is Module 01 &sect;3's argument, and "
    "the objective is the instrument rather than the goal.",
    "<b>So the useful output is the internal representations</b> "
    "— and <b>the measure of a pretraining objective is how useful "
    "the representations it produces turn out to be, not how well the "
    "objective itself is solved.</b> A model that solved masked "
    "prediction perfectly by some shortcut would be worthless.",
    "<b>Which explains the apparently arbitrary design choices:</b> "
    "<b>masked language modelling's 15% masking rate, the "
    "replace-with-random-token trick, and the span length "
    "distributions are all tuned for representation quality rather than "
    "for the proxy task's score.</b>",
    "<b>And it explains why causal models came to dominate:</b> <b>the "
    "objective is harder, every token serves as a prediction target "
    "rather than only the masked 15%, and the resulting model can also "
    "generate</b> — which turned out to matter more in practice than "
    "bidirectionality did, and was not obvious in advance."]),

  ("h1", "2 &nbsp; Contextual representations"),
  ("callout", "A pretrained model gives a different vector for each "
              "occurrence of a word",
   ["<b>'Bank' in a financial sentence and 'bank' beside a river "
    "receive genuinely different representations</b> — because <b>the "
    "representation is computed from the whole sentence rather than looked "
    "up by word identity</b>, which is the entire architectural point of "
    "Module 06's self-attention.",
    "<b>Which is Module 04 &sect;3's decisive limitation removed "
    "outright</b> — and <b>it is why pretrained models improved "
    "essentially every task at once</b> rather than one task at a time, "
    "which is what made the transition so abrupt.",
    "<b>And the layers differ systematically in what they "
    "encode:</b> <b>lower layers carry more surface and syntactic "
    "information, and higher layers more semantic and task-relevant "
    "information</b> — a finding that has held up robustly across "
    "many probing studies and several model families.",
    "<b>So which layer to use is a real decision</b> — and <b>'the "
    "last one' is frequently not the best answer</b> for a task that "
    "depends on syntax or on surface form, where a middle layer "
    "measurably outperforms it. <b>Concatenating several layers is "
    "often better still</b>, and costs nothing but memory."]),

  ("break",),
  ("h1", "3 &nbsp; Why transfer works unusually well here"),
  ("ul", ["<b>The pretraining data covers the target "
          "distribution.</b> <b>Nearly any text task involves text that "
          "resembles the pretraining text</b> — which is unusually "
          "true in language and is <b>the main reason transfer works so "
          "well here</b>, as opposed to in settings where the target data "
          "looks nothing like anything available at scale.",
          "<b>The required knowledge is genuinely shared.</b> "
          "<b>Syntax, word senses, and factual knowledge are needed by "
          "essentially every task</b>, so learning them once serves all "
          "of them — whereas in a narrower domain the useful "
          "knowledge may be task-specific.",
          "<b>The objective is genuinely hard</b>, so it forces rich "
          "representations rather than admitting a shortcut — <b>which "
          "is not true of every self-supervised objective</b>, several of "
          "which turned out to be solvable by exploiting a surface "
          "artefact.",
          "<b>And the scale is available.</b> <b>Text is abundant in "
          "a way that labelled examples simply are not</b> "
          "(Module 01 &sect;3), so the pretraining can be done at a "
          "scale the fine-tuning never could.",
          "<b>So the gain is largest where labelled data is "
          "smallest</b> — <b>which describes most real "
          "applications</b>, and is why this changed practice rather than "
          "only benchmarks. <b>The distribution-coverage reason is the "
          "one that does not transfer to other domains</b>, and is why "
          "pretraining has worked so much less dramatically in tabular "
          "settings (CSCE 633)."]),
  ("callout", "Scaling works, and it is worth being precise about what it "
              "delivers",
   ["<b>Loss falls predictably with parameters, data, and "
    "compute</b> — a smooth power law holding over several orders of "
    "magnitude, <b>which is an unusually clean empirical result</b> for "
    "machine learning and is what made large investments "
    "forecastable.",
    "<b>And the compute-optimal allocation matters a great "
    "deal:</b> <b>the early very large models were substantially "
    "undertrained</b>, and <b>training a smaller model on considerably "
    "more data turned out to be better for the same compute "
    "budget</b> — a correction that changed how models are sized.",
    "<b>What scaling delivers is lower loss, and capability follows "
    "imperfectly.</b> <b>Some abilities improve smoothly with scale, "
    "and some appear to improve sharply</b> — though <b>the apparent "
    "sharpness depends substantially on the choice of metric</b>, since a "
    "discontinuous metric over a continuously improving model produces an "
    "apparent jump (Module 10 &sect;1).",
    "<b>And what it does not deliver is reliability.</b> <b>Larger "
    "models are more capable and still fabricate</b> (Module 12 "
    "&sect;3) — <b>so scale moves the average and not the worst "
    "case</b>, which is the distinction that matters for anything "
    "deployed."]),

  ("h1", "4 &nbsp; Choosing one, and what it does not give you"),
  ("ul", ["<b>Start from the task shape.</b> <b>Classification or "
          "extraction favours an encoder; generation requires a decoder; "
          "sequence-to-sequence transformation suits an "
          "encoder-decoder</b> — and the mismatch is expensive "
          "rather than impossible.",
          "<b>Then the domain.</b> <b>A model pretrained on text like "
          "yours beats a larger general-purpose one</b> on specialised "
          "vocabulary — clinical, legal, and source code "
          "especially, where the tokenisation alone makes a large "
          "difference (Module 02 &sect;3).",
          "<b>Then the constraints:</b> latency budget, memory, cost "
          "per request at your expected volume, and <b>whether the data "
          "is permitted to leave your infrastructure</b> — which is "
          "frequently the binding constraint and is a governance question "
          "rather than a technical one.",
          "<b>Then the licence and the provenance</b>, which is a real "
          "constraint and <b>is routinely discovered late</b>, after the "
          "system is built — and which Module 13 treats as part of "
          "an honest claim.",
          "<b>And start with the smallest model that could possibly "
          "work</b>, because <b>iteration speed matters more than "
          "capability while you are still learning what the task "
          "needs</b>. <b>This is the advice most often ignored</b>, and "
          "<b>a fast feedback loop finds the data problems that a slow one "
          "hides</b> — which is where most of the real difficulty in "
          "these projects turns out to live."]),
  ("callout", "And what pretraining does not give you",
   ["<b>Knowledge of your specific data</b> — your schema, your "
    "customers, your product's terminology, your internal documents, and "
    "anything at all that happened after the training cutoff "
    "(Module 11's whole subject).",
    "<b>Reliable factuality.</b> <b>The model learned what text looks "
    "like, and that includes what <i>false</i> text looks like</b> "
    "— and <b>it has no mechanism that separates the two</b>, "
    "because the training objective did not distinguish them "
    "(Module 03 &sect;1's last point).",
    "<b>Alignment with your task's definition.</b> <b>Your notion of "
    "a 'relevant' document, a 'serious' complaint, or an 'acceptable' "
    "summary is not in the pretraining data</b> — which is exactly "
    "what Module 08's adaptation supplies, and why some adaptation is "
    "nearly always necessary.",
    "<b>And freedom from the corpus's biases</b>, which it represents "
    "faithfully — <b>Module 04 &sect;3's sentence applies "
    "unchanged at this scale</b>, and Module 12 &sect;2 is where the "
    "consequences are treated."]),
 ],
 "resources": [
   ("Devlin et al., and Radford et al. &mdash; BERT and the GPT series "
    "(free)",
    "https://arxiv.org/abs/1810.04805",
    "<b>&sect;1's two objectives in the originals</b> — read them "
    "together, because the contrast is the lesson."),
   ("Hoffmann et al. &mdash; Training Compute-Optimal Large Language "
    "Models (free)",
    "https://arxiv.org/abs/2203.15556",
    "<b>&sect;3's allocation correction</b> — the result that "
    "established the earlier models were undertrained."),
   ("Tenney et al. &mdash; BERT Rediscovers the Classical NLP Pipeline "
    "(free)",
    "https://aclanthology.org/P19-1452/",
    "<b>&sect;2's layer finding</b> — and a satisfying connection to "
    "Module 01 &sect;2's pipeline critique."),
   ("Schaeffer et al. &mdash; Are Emergent Abilities a Mirage? (free)",
    "https://arxiv.org/abs/2304.15004",
    "<b>&sect;3's sharpness caveat</b> — the argument that the metric "
    "produces the discontinuity. Read with Module 10."),
 ],
 "exercises": [
   "<b>State the three objectives</b> and what each architecture "
   "suits.",
   "<b>Explain why 15% masking</b> is a representation-quality decision "
   "rather than a task one.",
   "<b>Extract representations for an ambiguous word</b> in two "
   "sentences, and measure their distance.",
   "<b>Compare that to the static embedding distance</b> from "
   "Module 04.",
   "<b>Probe three layers</b> for a syntactic property and for a "
   "semantic one, and report which layer wins.",
   "<b>List the four reasons transfer works here</b> and say which does "
   "not generalise.",
   "<b>Find a scaling curve</b> and identify the power law region.",
   "<b>Construct a metric that makes smooth improvement look "
   "sharp.</b>",
   "<b>Choose a pretrained model for your Project 2 task</b> and justify "
   "it on all five criteria.",
   "<b>List four things pretraining did not give you</b> for that "
   "task.",
 ],
 "selfcheck": [
   "Name the three objectives and the trade between the first two.",
   "Why is the objective a means rather than the goal?",
   "Why did causal models come to dominate?",
   "What limitation do contextual representations remove?",
   "What do the layers differ in, and what follows for layer "
   "selection?",
   "Give four reasons transfer works here, and which is "
   "language-specific.",
   "What does scaling deliver predictably?",
   "Why might apparent sharp capability gains be a metric artefact?",
   "What does scale not deliver?",
   "Give five criteria for choosing a model, and four things "
   "pretraining omits.",
 ],
},

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Adaptation",
 "subtitle": "Getting a pretrained model to do your task.",
 "question": "Full fine-tuning, a prompt, or something between?",
 "outcomes": [
     "Explain the adaptation methods and their costs.",
     "Explain parameter-efficient fine-tuning.",
     "Explain in-context learning and its limits.",
     "Explain instruction tuning and preference training.",
     "Choose a method against real constraints.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The spectrum",
   "blurb": "From nothing to everything."},

  {"t": "table", "kicker": "Methods", "title": "The options, by cost",
   "header": ["Method", "What changes", "When it fits"],
   "widths": [2.7, 3.9, 5.3],
   "rows": [
     ["<b>Prompting</b>", "<b>Nothing — only the input</b>", "<b>No training data; fast iteration; prototyping</b>"],
     ["<b>Few-shot prompting</b>", "<b>Nothing; examples in the context</b>", "<b>A handful of examples; no training budget</b>"],
     ["<b>Linear probe</b>", "<b>A classifier on frozen features</b>", "<b>Small data; a strong cheap baseline</b>"],
     ["<b>Parameter-efficient (LoRA)</b>", "<b>A small added set of weights</b>", "<b>The usual answer — see Part 2</b>"],
     ["<b>Full fine-tuning</b>", "<b>Every weight</b>", "<b>Ample data and compute; a large domain shift</b>"],
     ["<b>Continued pretraining</b>", "<b>Every weight, on raw domain text</b>", "<b>A genuinely different domain, lots of text</b>"],
   ],
   "footnote": "<b>The linear probe row is the one to run "
               "first</b> — it is cheap, it is a legitimate "
               "baseline, and it tells you whether the pretrained "
               "features already contain what you need.",
   "note": "Running the probe first is the practical "
           "recommendation."},

  {"t": "callout", "title": "Run the cheapest method first, because it tells you what the task needs",
   "kind": "The ordering that saves time",
   "body": ["<b>A linear probe on frozen features takes "
            "minutes</b> — and <b>if it works, the pretrained "
            "representations already contain the signal and you are "
            "done.</b>",
            "<b>If it does not, that is informative</b>: either the "
            "task needs information the representations lack, or it needs "
            "a nonlinear decision boundary, and you can test "
            "which.",
            "<b>Whereas starting with full fine-tuning gives you a "
            "number and no diagnosis</b> — you do not know whether "
            "the gain came from the task adaptation or from the extra "
            "capacity.",
            "<b>Which is CSCE 633 Module 04's ablation "
            "discipline</b> — <b>the cheap method is both a baseline "
            "and an experiment</b>, and skipping it forfeits both."]},

  {"t": "section", "label": "Part 2", "title": "Parameter-efficient methods",
   "blurb": "Why they work, and they do."},

  {"t": "code", "kicker": "LoRA", "title": "Low-rank adaptation, which is the one to know",
   "lang": "text", "code": """
  INSTEAD OF updating W (d x d), learn
      W' = W + BA
  where B is d x r and A is r x d, with r << d.

  SO the trainable parameters go from d^2 to 2dr --
  frequently under 1% of the model.

  WHY IT WORKS
      the weight UPDATE needed for a task appears to
      be approximately low rank, even though the
      weights themselves are not. Adaptation is a
      small correction, not a new function.

  WHAT IT BUYS
      trains on much less memory, since optimiser
          state scales with trainable parameters
      many task adapters share one base model
      and it can be merged into W at inference, so
          there is no added latency

  AND THE QUALITY IS CLOSE TO FULL FINE-TUNING on
  most tasks -- which is the empirical result that
  made it the default.
""",
   "caption": "<b>The low-rank-update hypothesis is the "
              "insight</b> — and the merge-at-inference property is "
              "what makes it free in production.",
   "note": "The adapters-share-a-base-model property is what changed "
           "deployment."},

  {"t": "section", "label": "Part 3", "title": "In-context learning",
   "blurb": "Which is not learning, and is useful."},

  {"t": "callout", "title": "Few-shot prompting changes the model's behaviour without changing the model",
   "kind": "What is actually happening",
   "body": ["<b>Examples in the context condition the "
            "prediction</b> — the weights are unchanged, so nothing "
            "is retained between requests, which is why 'learning' is a "
            "misleading word for it.",
            "<b>And the examples do two things:</b> <b>they specify "
            "the task format, and they supply some information about the "
            "mapping</b> — and the evidence is that <b>the format "
            "contribution is the larger one.</b>",
            "<b>Which is why the results are sensitive to things that "
            "should not matter:</b> <b>example order, label wording, and "
            "formatting all move the output measurably.</b>",
            "<b>So treat it as a fast, high-variance method.</b> "
            "<b>Excellent for prototyping and for tasks with no training "
            "data, and a poor choice where consistency "
            "matters</b> — which Module 10 asks you to measure "
            "rather than assume."]},

  {"t": "bullets", "kicker": "Limits", "title": "And the specific limits",
   "items": [
     "<b>Context costs money and latency on every request</b>, "
     "forever — whereas fine-tuning pays once.",
     "",
     "<b>The examples consume the context window</b>, competing "
     "with the actual input and with retrieved "
     "material (Module 11).",
     "",
     "<b>It does not scale with data.</b> <b>Twenty examples help; "
     "two thousand do not fit</b>, and the method cannot use data you "
     "have.",
     "",
     "<b>And the sensitivity makes evaluation harder</b> — "
     "<b>a result from one prompt is a result about that prompt</b>, so "
     "report variance across several.",
     "",
     "<b>Which is a specific instance of "
     "Module 10 §1's single-number problem.</b>",
   ],
   "footnote": "<b>'A result from one prompt is a result about that "
               "prompt'</b> is the discipline to adopt — and "
               "reporting across several prompts is cheap and almost never "
               "done."},

  {"t": "section", "label": "Part 4", "title": "Instruction and preference tuning",
   "blurb": "How a predictor becomes an assistant."},

  {"t": "callout", "title": "Instruction tuning aligns the model's behaviour with the task framing, and preference training with human judgement",
   "kind": "The two stages after pretraining",
   "body": ["<b>Instruction tuning is supervised fine-tuning on "
            "(instruction, response) pairs across many "
            "tasks</b> — which teaches the model to treat an "
            "instruction as something to follow rather than as text to "
            "continue.",
            "<b>Preference training then optimises against human "
            "comparisons</b> — a reward model fitted to preferences, "
            "then reinforcement learning (CSCE 642), or a direct "
            "preference objective that skips the reward "
            "model.",
            "<b>And what this changes is behaviour rather than "
            "knowledge.</b> <b>The model does not learn new facts "
            "here</b>; it learns which of its possible continuations to "
            "produce.",
            "<b>Which is worth being clear about:</b> <b>preference "
            "training makes outputs more acceptable to raters, and "
            "acceptability is not accuracy</b> — <b>a confident wrong "
            "answer rates well</b>, which is "
            "Module 12 §3's mechanism."]},

  {"t": "bullets", "kicker": "Choosing", "title": "Choosing a method, concretely",
   "items": [
     "<b>No training data → prompting</b>, with the "
     "variance measured.",
     "",
     "<b>Tens of examples → few-shot prompting, or a linear "
     "probe</b> if you have features.",
     "",
     "<b>Hundreds to thousands → parameter-efficient "
     "fine-tuning</b>, which is the usual answer.",
     "",
     "<b>Tens of thousands and a domain shift → full "
     "fine-tuning</b>, if the compute is available.",
     "",
     "<b>And a genuinely different domain with abundant raw text "
     "→ continued pretraining first</b>, then one of the "
     "above.",
   ],
   "footnote": "<b>The middle row covers most real "
               "cases</b> — parameter-efficient fine-tuning on a few "
               "thousand examples is the modal correct answer, and it is "
               "cheap enough to do several times."},
 ],
 "takeaways": [
   "Run the linear probe first: it is a legitimate baseline and it "
   "diagnoses whether the pretrained features already contain the signal.",
   "LoRA works because the weight update needed for a task is "
   "approximately low rank even though the weights are not.",
   "LoRA merges into the base weights at inference, so there is no added "
   "latency, and many adapters share one base model.",
   "Few-shot examples mostly specify the format rather than the mapping, "
   "which is why order and wording move the output.",
   "A result from one prompt is a result about that prompt — report "
   "variance across several.",
   "Preference training makes outputs more acceptable to raters, and "
   "acceptability is not accuracy.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The spectrum"),
  ("table", ["Method", "What changes", "When it fits"],
   [["<b>Prompting</b>", "<b>Nothing — only the input text.</b>",
     "<b>No training data at all; fast iteration; prototyping.</b>"],
    ["<b>Few-shot prompting</b>",
     "<b>Nothing; examples are placed in the context</b> (&sect;3).",
     "<b>A handful of examples and no training budget.</b>"],
    ["<b>Linear probe</b>",
     "<b>A classifier trained on frozen features.</b>",
     "<b>Small data; and a strong, cheap baseline</b> — see the "
     "note."],
    ["<b>Parameter-efficient fine-tuning</b>",
     "<b>A small set of added or modified weights</b> (&sect;2).",
     "<b>The usual answer for most real tasks.</b>"],
    ["<b>Full fine-tuning</b>", "<b>Every weight in the model.</b>",
     "<b>Ample labelled data and compute, and a substantial domain "
     "shift.</b>"],
    ["<b>Continued pretraining</b>",
     "<b>Every weight, on raw domain text with the pretraining "
     "objective.</b>",
     "<b>A genuinely different domain with a lot of unlabelled "
     "text</b> — clinical or legal corpora, or code."]],
   [0.22, 0.32, 0.46]),
  ("callout", "Run the cheapest method first, because it tells you what the "
              "task needs",
   ["<b>A linear probe on frozen features takes minutes</b> — "
    "extract the representations once, fit logistic regression — and "
    "<b>if it works, the pretrained representations already contain the "
    "signal and you are finished.</b>",
    "<b>If it does not work, that is informative rather than "
    "disappointing:</b> either the task requires information the "
    "representations do not carry, or it requires a nonlinear decision "
    "boundary over them — and <b>you can distinguish those two by "
    "trying a small nonlinear head</b>, which takes another ten "
    "minutes.",
    "<b>Whereas starting with full fine-tuning gives you a number and "
    "no diagnosis</b> — <b>you do not know whether the gain came "
    "from task adaptation or simply from the additional effective "
    "capacity</b>, and you cannot tell what a cheaper method would have "
    "achieved.",
    "<b>Which is CSCE 633 Module 04's ablation discipline arriving "
    "as a practical workflow</b> — <b>the cheap method is "
    "simultaneously a baseline and an experiment</b>, and skipping it "
    "forfeits both. <b>Module 10 &sect;2 then requires the baseline "
    "anyway</b>, so running it first costs nothing."]),

  ("h1", "2 &nbsp; Parameter-efficient methods"),
  ("code", """INSTEAD OF updating W (d x d), learn
    W' = W + BA
where B is d x r and A is r x d, with r << d.

SO the trainable parameters go from d^2 to 2dr --
frequently under 1% of the model's total.

WHY IT WORKS
    the weight UPDATE needed for a task appears to be
    approximately low rank, even though the weights
    themselves are not. Adaptation is a small
    correction to an existing function, not the
    learning of a new one.

WHAT IT BUYS
    trains in much less memory, since the optimiser
        state scales with the TRAINABLE parameters
        rather than with the total
    many task adapters can share one base model in
        memory, which changed how these are deployed
    and BA can be merged into W at inference time, so
        there is no added latency at all

AND THE QUALITY IS CLOSE TO FULL FINE-TUNING on most
tasks -- which is the empirical result that made it
the default."""),
  ("p", "<b>The low-rank-update hypothesis is the actual "
        "insight</b>, and it is worth stating as a claim about "
        "adaptation: <b>a pretrained model already computes approximately "
        "the right function, and a task requires a small correction rather "
        "than a different function</b> — which is Module 07 "
        "&sect;3's transfer argument expressed in terms of weights. "
        "<b>And the merge-at-inference property is what makes it free in "
        "production</b>, while <b>the shared-base-model property is what "
        "changed deployment</b>: serving a hundred fine-tuned variants "
        "used to mean a hundred models."),

  ("break",),
  ("h1", "3 &nbsp; In-context learning"),
  ("callout", "Few-shot prompting changes the model's behaviour without "
              "changing the model",
   ["<b>Examples placed in the context condition the prediction</b> "
    "— <b>the weights are entirely unchanged, so nothing is retained "
    "between requests</b>, which is why 'learning' is a somewhat "
    "misleading word for what is happening.",
    "<b>And the examples do two distinct things:</b> <b>they specify "
    "the task format, and they supply some information about the "
    "input-output mapping</b> — and <b>the evidence is that the "
    "format contribution is substantially the larger of the two</b>, "
    "since replacing the labels with random ones degrades performance "
    "much less than removing the examples does.",
    "<b>Which is precisely why the results are sensitive to things "
    "that ought not to matter:</b> <b>the order of the examples, the "
    "exact wording of the labels, the formatting, and the presence of a "
    "trailing space all move the output measurably</b> "
    "(Module 02 &sect;3's tokenisation sensitivity "
    "contributing).",
    "<b>So treat it as a fast, high-variance method.</b> <b>Excellent "
    "for prototyping and for tasks where no training data exists, and a "
    "poor choice where consistency matters</b> — and "
    "<b>Module 10 asks you to measure that variance rather than assume "
    "it away.</b>"]),
  ("ul", ["<b>Context costs money and latency on every single "
          "request</b>, forever — <b>whereas fine-tuning pays the "
          "cost once</b>, which inverts the economics above a modest "
          "request volume.",
          "<b>The examples consume the context window</b>, competing "
          "directly with the actual input and with any retrieved material "
          "(Module 11) — so the method scales badly exactly where "
          "you also want retrieval.",
          "<b>It does not scale with data.</b> <b>Twenty examples "
          "help; two thousand do not fit in the context</b>, so <b>the "
          "method cannot make use of data you actually have</b>, which is "
          "the decisive argument for fine-tuning once you have "
          "collected any.",
          "<b>And the sensitivity makes evaluation harder</b> — "
          "<b>a result obtained from one prompt is a result about that "
          "prompt</b>, so you must report variance across several "
          "phrasings and orderings to claim anything about the method.",
          "<b>Which is a specific instance of Module 10 &sect;1's "
          "single-number problem.</b> <b>'A result from one prompt is a "
          "result about that prompt' is the discipline to adopt</b>, and "
          "<b>reporting across several prompts is cheap and almost never "
          "done</b> — which makes a great deal of published "
          "prompting comparison weaker than it appears."]),

  ("h1", "4 &nbsp; Instruction and preference tuning"),
  ("callout", "Instruction tuning aligns behaviour with the task framing, "
              "and preference training with human judgement",
   ["<b>Instruction tuning is supervised fine-tuning on (instruction, "
    "response) pairs across a great many tasks</b> — which teaches "
    "the model to treat an instruction as <i>something to follow</i> "
    "rather than as <i>text to continue</i>, and that reframing is most "
    "of what distinguishes a usable assistant from a raw language "
    "model.",
    "<b>Preference training then optimises against human "
    "comparisons</b> — either a reward model fitted to preference "
    "data followed by reinforcement learning (CSCE 642's "
    "machinery), or a direct preference objective that skips the explicit "
    "reward model and optimises the comparison directly.",
    "<b>And what this changes is behaviour rather than "
    "knowledge.</b> <b>The model does not learn new facts at this "
    "stage</b> — the data volume is far too small — <b>it "
    "learns which of its possible continuations to actually "
    "produce</b>, which is a selection among existing capabilities.",
    "<b>Which is worth being clear about, because it has a direct "
    "consequence:</b> <b>preference training makes outputs more "
    "acceptable to raters, and acceptability is not accuracy</b> — "
    "<b>a confident, fluent, well-formatted wrong answer rates "
    "well</b>, and <b>that is Module 12 &sect;3's mechanism</b> rather "
    "than an incidental flaw."]),
  ("ul", ["<b>No training data &rarr; prompting</b>, with the variance "
          "across phrasings measured and reported (&sect;3).",
          "<b>Tens of examples &rarr; few-shot prompting, or a linear "
          "probe</b> if you can extract features (&sect;1).",
          "<b>Hundreds to a few thousand &rarr; parameter-efficient "
          "fine-tuning</b> (&sect;2), <b>which is the usual answer</b> "
          "and is cheap enough to try several configurations.",
          "<b>Tens of thousands of examples and a real domain shift "
          "&rarr; full fine-tuning</b>, if the compute is available and "
          "the gain over the parameter-efficient version is measured "
          "rather than assumed.",
          "<b>And a genuinely different domain with abundant raw text "
          "&rarr; continued pretraining first</b>, then one of the above "
          "on top. <b>The middle row covers most real cases:</b> "
          "<b>parameter-efficient fine-tuning on a few thousand examples "
          "is the modal correct answer</b>, and it is cheap enough to do "
          "several times with different data, which is usually a better "
          "use of the budget than one larger run."]),
 ],
 "resources": [
   ("Hu et al. &mdash; LoRA (free)",
    "https://arxiv.org/abs/2106.09685",
    "<b>&sect;2 in the original</b> — including the rank ablations, "
    "which are the evidence for the low-rank hypothesis."),
   ("Min et al. &mdash; Rethinking the Role of Demonstrations (free)",
    "https://arxiv.org/abs/2202.12837",
    "<b>&sect;3's format-versus-mapping result</b> — the random-label "
    "experiment, which is the one to know."),
   ("Ouyang et al. &mdash; Training language models to follow "
    "instructions (free)",
    "https://arxiv.org/abs/2203.02155",
    "<b>&sect;4's two stages</b>, with the preference pipeline described "
    "concretely."),
   ("Rafailov et al. &mdash; Direct Preference Optimization (free)",
    "https://arxiv.org/abs/2305.18290",
    "<b>&sect;4's simpler alternative</b> — the same objective "
    "without the separate reward model."),
 ],
 "exercises": [
   "<b>Run a linear probe</b> on frozen features for your task, and "
   "record the score.",
   "<b>Try a small nonlinear head</b> and say what the difference tells "
   "you.",
   "<b>Implement LoRA</b> on a small model and count the trainable "
   "parameters.",
   "<b>Vary the rank</b> and plot quality against it.",
   "<b>Merge the adapter into the base weights</b> and confirm the "
   "outputs match.",
   "<b>Run the same few-shot task with five example orderings</b> and "
   "report the variance.",
   "<b>Replace the few-shot labels with random ones</b> and measure the "
   "drop.",
   "<b>Compute the per-request cost</b> of few-shot prompting versus "
   "fine-tuning at your expected volume.",
   "<b>Compare a base and an instruction-tuned model</b> on the same "
   "instruction.",
   "<b>Choose a method for Project 2</b> and justify it on data volume "
   "and constraints.",
 ],
 "selfcheck": [
   "Name six adaptation methods and what each changes.",
   "Why run the linear probe first, and what does its failure tell "
   "you?",
   "Explain LoRA and the hypothesis it rests on.",
   "What three things does LoRA buy?",
   "Why is 'in-context learning' a misleading name?",
   "What do few-shot examples mostly contribute, and what is the "
   "evidence?",
   "Give four limits of in-context learning.",
   "What discipline should you adopt about prompt results?",
   "What do instruction tuning and preference training each change?",
   "Why is acceptability not accuracy?",
 ],
},

]
