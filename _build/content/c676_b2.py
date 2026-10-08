# -*- coding: utf-8 -*-
"""CSCE 676 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Similar Items at Scale",
 "subtitle": "The field's model result: exact becomes approximate, with a bound.",
 "question": "How do you find similar pairs without comparing all pairs?",
 "outcomes": [
     "Represent documents as sets and justify the choice.",
     "Explain minhashing and why it estimates Jaccard.",
     "Explain LSH and derive its S-curve.",
     "Choose LSH parameters from a target threshold.",
     "Verify the approximation bounds empirically.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Sets and shingles",
   "blurb": "Making documents comparable."},

  {"t": "callout", "title": "Represent a document as the set of its k-character shingles",
   "kind": "The representation, and why",
   "body": ["<b>A k-shingle is any contiguous substring of length "
            "k</b> — so a document becomes the set of all such "
            "substrings it contains, which <b>preserves local word "
            "order</b> unlike a bag of words.",
            "<b>And k matters:</b> <b>k = 5 suits short documents, "
            "k = 9 or 10 suits prose</b> — <b>too small and every "
            "document shares shingles by chance; too large and near-"
            "duplicates share none.</b>",
            "<b>Then hash the shingles to integers</b>, which bounds "
            "the space and makes the sets cheap to store and "
            "intersect.",
            "<b>So the similarity question becomes set "
            "similarity</b> — and <b>Jaccard similarity, the "
            "intersection over the union, is the measure that "
            "follows</b>, which is Part 2's subject."]},

  {"t": "eq", "kicker": "Jaccard", "title": "The measure, and the cost of computing it exactly",
   "eqs": [
     ("J(A, B) = |A ∩ B| / |A ∪ B|",
      "Between 0 and 1. Insensitive to document length, which is "
      "why it suits this."),
     ("all pairs: C(n,2) ≈ n²/2 comparisons",
      "At n = 10⁶ that is 5×10¹¹ set intersections. Infeasible, "
      "and it is only a million documents."),
     ("so: estimate J cheaply, then avoid most pairs entirely",
      "Two separate ideas — minhashing does the first, LSH does "
      "the second, and both are needed."),
   ],
   "caption": "<b>Two separate problems</b>: estimating the similarity "
              "cheaply, and avoiding the quadratic number of pairs. "
              "Confusing them is the usual error.",
   "note": "Separating the two ideas is what makes the module "
           "tractable."},

  {"t": "section", "label": "Part 2", "title": "Minhashing",
   "blurb": "An estimator with a provable property."},

  {"t": "callout", "title": "The probability that two sets have the same minhash is exactly their Jaccard similarity",
   "kind": "The result the whole technique rests on",
   "body": ["<b>Take a random permutation of the universe of "
            "shingles, and record for each set the first of its elements "
            "in that order.</b> <b>That single value is the "
            "set's minhash.</b>",
            "<b>And P[minhash(A) = minhash(B)] = J(A, B)</b>, "
            "<b>exactly</b> — because the first element of the union "
            "under a random permutation is equally likely to be any of "
            "them, and it is shared only if it lies in the "
            "intersection.",
            "<b>So averaging over many independent permutations "
            "estimates J</b> — <b>the fraction of agreeing minhashes "
            "is an unbiased estimator</b>, and its variance falls as "
            "1/k.",
            "<b>Which gives the signature:</b> <b>replace a set of "
            "any size with k integers</b>, typically 100 to 200, with "
            "the error around 1/√k — which is "
            "CSCE 658's concentration machinery doing the work."]},

  {"t": "code", "kicker": "Implementation", "title": "And how it is actually computed",
   "lang": "text", "code": """
  THE PROBLEM WITH REAL PERMUTATIONS
      a permutation of a billion shingles is a billion
      numbers, per permutation. Unaffordable.

  THE FIX: use hash functions as pseudo-permutations
      h_i(x) = (a_i * x + b_i) mod p
      with random a_i, b_i and p prime. Each h_i
      stands in for one permutation.

  ONE PASS OVER THE DATA
      for each set S:
        for each i in 1..k:
          sig[i] = min over x in S of h_i(x)

  SO the signature is k minima, computed in one pass,
  with no permutation ever materialised.

  AND THE ERROR
      the estimate is a mean of k Bernoulli trials, so
      the standard error is about sqrt(J(1-J)/k).
      k = 200 gives roughly 0.035 -- which Project 1
      asks you to verify rather than assume.
""",
   "caption": "<b>Hash functions standing in for permutations is the "
              "implementation trick</b> — and it is why the method "
              "is one pass and constant memory per set.",
   "note": "The pseudo-permutation substitution is the detail students "
           "miss."},

  {"t": "section", "label": "Part 3", "title": "LSH",
   "blurb": "Avoiding most pairs entirely."},

  {"t": "callout", "title": "Hash signatures into bands so that similar items collide and dissimilar ones mostly do not",
   "kind": "The construction",
   "body": ["<b>Split each k-element signature into b bands of r "
            "rows</b>, with br = k — and <b>hash each band "
            "separately into buckets.</b>",
            "<b>Two items are candidates if they land in the same "
            "bucket for <i>any</i> band</b> — so you only compare "
            "pairs that collided somewhere, which is a tiny fraction of "
            "all pairs.",
            "<b>And the probability of becoming a candidate is a "
            "function of similarity:</b> <b>1 − (1 − "
            "sᵣ)ᵇ</b>, which is an S-shaped "
            "curve.",
            "<b>Which means the threshold is "
            "tunable:</b> <b>the curve's steep region sits near "
            "(1/b)^(1/r)</b>, and choosing b and r places the "
            "threshold where you want it."]},

  {"t": "eq", "kicker": "The S-curve", "title": "What the parameters control",
   "eqs": [
     ("P(candidate | similarity s) = 1 − (1 − sʳ)ᵇ",
      "Both bands and rows appear. Increasing r sharpens; "
      "increasing b shifts the curve left."),
     ("threshold ≈ (1/b)^(1/r)",
      "The similarity at which the curve crosses the middle. Pick "
      "this from your requirement."),
     ("more bands ⟹ more candidates, higher recall, more work",
      "The trade is false positives against false negatives, and "
      "you choose where to sit on it."),
   ],
   "caption": "<b>Plot the curve before choosing parameters</b> "
              "— the trade is visible on it and invisible in the "
              "numbers.",
   "note": "Plotting the curve is Project 1's requirement for exactly "
           "this reason."},

  {"t": "section", "label": "Part 4", "title": "Beyond Jaccard",
   "blurb": "The same idea for other distances."},

  {"t": "bullets", "kicker": "Families", "title": "LSH families for other measures",
   "items": [
     "<b>Cosine similarity: random hyperplane "
     "hashing.</b> <b>Take the sign of the dot product with a random "
     "vector</b> — the collision probability is "
     "1 − θ/π.",
     "",
     "<b>Euclidean distance: random projection into "
     "buckets.</b> Project onto a random line and quantise, so "
     "nearby points usually share a bucket.",
     "",
     "<b>Hamming distance: sample random bit positions</b>, which "
     "is the simplest family and the easiest to analyse.",
     "",
     "<b>And the general requirement is "
     "the same:</b> <b>a hash family where the collision probability "
     "decreases with distance</b>, which is what makes amplification "
     "work.",
     "",
     "<b>Which is how approximate nearest-neighbour search "
     "works</b>, and is what CSCE 670 §08 builds on for "
     "dense retrieval.",
   ],
   "footnote": "<b>The abstraction is worth holding:</b> any distance "
               "with a locality-sensitive hash family gets the same "
               "banding construction and the same S-curve "
               "analysis."},

  {"t": "callout", "title": "And what to verify rather than assume",
   "kind": "Closing",
   "body": ["<b>Measure the minhash estimate against the exact "
            "Jaccard on a sample</b> — <b>and compare the observed "
            "error to √(J(1−J)/k)</b>, which is "
            "Project 1's central requirement.",
            "<b>Report both error rates.</b> <b>Recall alone hides "
            "the trade</b>, and the candidate count is what determines "
            "whether the method actually saved anything.",
            "<b>And check the hash functions.</b> <b>A poor hash "
            "family breaks the independence the bound assumes</b>, which "
            "shows up as correlated collisions rather than as an "
            "error.",
            "<b>Which is Module 01 §2's discipline in "
            "its first concrete instance:</b> <b>choose the "
            "approximation, state the bound, then measure whether it "
            "holds.</b>"]},
 ],
 "takeaways": [
   "Shingling preserves local word order, and k must be large enough that "
   "chance sharing is rare and small enough that near-duplicates still "
   "overlap.",
   "Estimating similarity cheaply and avoiding the quadratic pair count "
   "are two separate problems; minhashing solves the first and LSH the "
   "second.",
   "The probability two sets share a minhash is exactly their Jaccard "
   "similarity, which is why the estimator is unbiased.",
   "Hash functions stand in for permutations, which is what makes "
   "minhashing one pass and constant memory per set.",
   "The LSH S-curve's threshold is approximately (1/b)^(1/r), so plot the "
   "curve and derive the parameters from your requirement.",
   "Any distance with a locality-sensitive hash family gets the same "
   "banding construction and the same analysis.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Sets and shingles"),
  ("callout", "Represent a document as the set of its k-character shingles",
   ["<b>A k-shingle is any contiguous substring of length k</b> "
    "— so a document becomes the set of all such substrings it "
    "contains, and <b>this preserves local word order</b> in a way that a "
    "bag of words does not, which matters because reordered text is not a "
    "near-duplicate.",
    "<b>And k matters a good deal:</b> <b>k = 5 suits short documents "
    "and k = 9 or 10 suits ordinary prose</b> — <b>too small and "
    "every document shares shingles purely by chance, which destroys the "
    "signal; too large and genuine near-duplicates share none of "
    "them.</b> The rule of thumb is that the shingle space should be "
    "large enough that a typical document uses a tiny fraction of it.",
    "<b>Then hash the shingles to fixed-width integers</b>, which "
    "bounds the space, makes the sets cheap to store, and makes "
    "intersection a numeric operation — at the cost of occasional "
    "collisions, which are harmless at the rates involved.",
    "<b>So the similarity question becomes a set similarity "
    "question</b> — and <b>Jaccard similarity, the size of the "
    "intersection over the size of the union, is the measure that "
    "follows naturally</b>, because it is insensitive to document "
    "length."]),
  ("eq", "J(A, B) = |A &cap; B| / |A &cup; B|"),
  ("ul", ["<b>Between 0 and 1</b>, and <b>insensitive to document "
          "length</b> — which is why it suits near-duplicate "
          "detection, where one document may be a superset of another "
          "with boilerplate added.",
          "<b>Computing it for all pairs requires C(n,2) &approx; "
          "n&sup2;/2 comparisons.</b> <b>At n = 10<sup>6</sup> that is "
          "5&times;10<sup>11</sup> set intersections</b> — "
          "infeasible, <b>and that is only a million documents</b>, which "
          "is small by this course's standards.",
          "<b>So the approach is: estimate J cheaply, and then avoid "
          "most pairs entirely</b> — <b>two separate ideas</b>, "
          "which <b>minhashing and LSH address respectively</b>, and "
          "<b>both are necessary</b>: a cheap estimator still leaves you "
          "with n&sup2;/2 estimates to compute.",
          "<b>Confusing the two is the usual error</b>, and separating "
          "them is what makes this module tractable — so it is worth "
          "being able to state which problem each half solves."]),

  ("h1", "2 &nbsp; Minhashing"),
  ("callout", "The probability that two sets have the same minhash is "
              "exactly their Jaccard similarity",
   ["<b>Take a random permutation of the universe of possible "
    "shingles, and record, for each set, the first of its own elements in "
    "that order.</b> <b>That single value is the set's minhash under "
    "that permutation.</b>",
    "<b>And P[minhash(A) = minhash(B)] = J(A, B), exactly</b> — "
    "<b>because the first element of A &cup; B under a uniformly random "
    "permutation is equally likely to be any element of the union, and "
    "the two minhashes agree precisely when that element lies in the "
    "intersection</b>. The proof is one line and worth working "
    "through.",
    "<b>So averaging over many independent permutations estimates "
    "J</b> — <b>the fraction of positions at which two signatures "
    "agree is an unbiased estimator of their Jaccard "
    "similarity</b>, and its variance falls as 1/k in the number of "
    "permutations.",
    "<b>Which gives the signature:</b> <b>replace a set of any size "
    "with k integers</b>, typically 100 to 200, <b>with the standard "
    "error around 1/&radic;k</b> — and that is <b>CSCE 658's "
    "concentration machinery doing the work</b>, which is why this course "
    "requires it."]),
  ("code", """THE PROBLEM WITH REAL PERMUTATIONS
    a permutation of a billion shingles is a billion
    numbers, per permutation. Unaffordable, and you
    need hundreds of them.

THE FIX: use hash functions as pseudo-permutations
    h_i(x) = (a_i * x + b_i) mod p
    with random a_i, b_i and p a large prime. Each
    h_i stands in for one permutation.

ONE PASS OVER THE DATA
    for each set S:
      for each i in 1..k:
        sig[i] = min over x in S of h_i(x)

SO the signature is k minima, computed in a single
pass, with no permutation ever materialised.

AND THE ERROR
    the estimate is a mean of k Bernoulli trials, so
    the standard error is about sqrt(J(1-J)/k).
    k = 200 gives roughly 0.035 -- which Project 1
    asks you to verify rather than assume."""),
  ("p", "<b>Hash functions standing in for permutations is the "
        "implementation trick</b>, and <b>it is why the method is one "
        "pass and constant memory per set</b> — which is exactly "
        "Module 01 &sect;2's cost model being respected. <b>This is "
        "the detail students most often miss</b>, and it matters because "
        "the quality of the hash family determines whether the "
        "independence the bound assumes actually holds (&sect;4's last "
        "point)."),

  ("break",),
  ("h1", "3 &nbsp; Locality-sensitive hashing"),
  ("callout", "Hash signatures into bands so that similar items collide and "
              "dissimilar ones mostly do not",
   ["<b>Split each k-element signature into b bands of r rows "
    "each</b>, with br = k — and <b>hash each band separately into "
    "buckets</b>, so each item lands in b buckets.",
    "<b>Two items become candidates if they land in the same bucket "
    "for <i>any</i> band</b> — so <b>you only compute the actual "
    "similarity for pairs that collided somewhere</b>, which is a tiny "
    "fraction of all pairs and is where the quadratic cost "
    "disappears.",
    "<b>And the probability of becoming a candidate is a function of "
    "the true similarity:</b> <b>1 &minus; (1 &minus; "
    "s<sup>r</sup>)<sup>b</sup></b> — the probability of agreeing on "
    "all r rows of at least one of b bands — <b>which is an "
    "S-shaped curve in s.</b>",
    "<b>Which means the threshold is tunable rather than "
    "fixed:</b> <b>the curve's steep region sits near "
    "(1/b)<sup>1/r</sup></b>, so <b>choosing b and r places the "
    "threshold wherever your application needs it</b> — which is "
    "the design freedom the construction buys."]),
  ("eq", "P(candidate | s) = 1 &minus; (1 &minus; "
         "s<sup>r</sup>)<sup>b</sup> &nbsp;&nbsp; threshold &approx; "
         "(1/b)<sup>1/r</sup>"),
  ("ul", ["<b>Both parameters appear, and they do different "
          "things.</b> <b>Increasing r sharpens the curve</b> (a steeper "
          "transition), and <b>increasing b shifts it left</b> (a lower "
          "threshold, more candidates).",
          "<b>The threshold is the similarity at which the curve "
          "crosses the middle</b> — <b>pick this value from your "
          "application requirement</b>, then solve for b and r subject "
          "to br = k.",
          "<b>More bands means more candidates, higher recall, and "
          "more work</b> — <b>the trade is false positives against "
          "false negatives</b>, and the construction lets you choose "
          "where on it to sit rather than accepting a default.",
          "<b>Plot the curve before choosing parameters.</b> <b>The "
          "trade is visible on the plot and essentially invisible in the "
          "numbers</b> — which is why <b>Project 1 requires the plot "
          "rather than the parameters</b>, and why tuning by trial misses "
          "the structure."]),

  ("h1", "4 &nbsp; Beyond Jaccard"),
  ("ul", ["<b>Cosine similarity: random hyperplane hashing.</b> "
          "<b>Take the sign of the dot product with a random "
          "vector</b> — and <b>the collision probability is "
          "1 &minus; &theta;/&pi;</b>, where &theta; is the angle, which "
          "decreases with distance exactly as required.",
          "<b>Euclidean distance: random projection into "
          "buckets.</b> Project each point onto a random line and "
          "quantise the result, so that <b>nearby points usually fall in "
          "the same bucket</b> and distant ones usually do not.",
          "<b>Hamming distance: sample random bit positions.</b> "
          "<b>The simplest family and the easiest to analyse</b> — "
          "the collision probability is the fraction of agreeing bits "
          "raised to the number sampled.",
          "<b>And the general requirement is always the "
          "same:</b> <b>a hash family in which the collision probability "
          "decreases with distance</b> — <b>which is what makes the "
          "banding amplification work</b>, and is the definition of "
          "locality-sensitive.",
          "<b>Which is how approximate nearest-neighbour search "
          "works</b>, and is what <b>CSCE 670 Module 08 builds on for "
          "dense retrieval</b> at scale. <b>The abstraction is worth "
          "holding:</b> <b>any distance with a locality-sensitive hash "
          "family gets the same banding construction and the same S-curve "
          "analysis</b>, which means learning it once covers all of "
          "them."]),
  ("callout", "And what to verify rather than assume",
   ["<b>Measure the minhash estimate against the exact Jaccard "
    "similarity on a sample</b> — <b>and compare the observed error "
    "to &radic;(J(1&minus;J)/k)</b>, which is <b>Project 1's central "
    "requirement</b> and takes an hour.",
    "<b>Report both error rates.</b> <b>Recall alone hides the "
    "trade</b> — a parameter setting with excellent recall and a "
    "huge candidate count has not saved you anything — and <b>the "
    "candidate count is what determines whether the method actually "
    "helped.</b>",
    "<b>And check the hash functions.</b> <b>A poor hash family "
    "breaks the independence the bound assumes</b>, <b>which shows up as "
    "correlated collisions rather than as an obvious error</b> — so "
    "the estimates are biased in a way that looks like a property of the "
    "data.",
    "<b>Which is Module 01 &sect;2's discipline in its first "
    "concrete instance:</b> <b>choose the approximation, state the "
    "bound, then measure whether it holds on your data.</b> <b>Every "
    "remaining module in this course has a version of this "
    "paragraph.</b>"]),
 ],
 "resources": [
   ("Mining of Massive Datasets, chapter 3 (free)",
    "http://www.mmds.org/",
    "<b>The whole module, and the best treatment in print</b> — "
    "including the parameter selection worked through numerically."),
   ("Broder &mdash; On the resemblance and containment of documents "
    "(free)",
    "https://ieeexplore.ieee.org/document/666900",
    "<b>&sect;2 in the original</b> — minhashing as it was invented, "
    "for exactly this problem."),
   ("Indyk & Motwani &mdash; Approximate nearest neighbors (free)",
    "https://dl.acm.org/doi/10.1145/276698.276876",
    "<b>&sect;4's general framework</b> — where "
    "locality-sensitive hashing is defined properly."),
   ("Charikar &mdash; Similarity estimation from rounding algorithms "
    "(free)",
    "https://dl.acm.org/doi/10.1145/509907.509965",
    "<b>&sect;4's first row</b> — the random hyperplane family and "
    "its collision probability."),
 ],
 "exercises": [
   "<b>Shingle a document at k = 3, 5, and 10</b> and compare the set "
   "sizes.",
   "<b>Compute Jaccard similarity for ten document pairs</b> exactly.",
   "<b>Extrapolate the all-pairs cost</b> to a million and a billion "
   "documents.",
   "<b>Implement minhashing</b> with hash-based pseudo-permutations.",
   "<b>Verify that the agreement fraction estimates Jaccard</b> on "
   "pairs whose true similarity you know.",
   "<b>Plot the observed error against k</b> and compare to "
   "1/√k.",
   "<b>Implement banded LSH</b> and plot the S-curve for three (b, r) "
   "choices.",
   "<b>Derive b and r from a target threshold of 0.8</b> with "
   "k = 200.",
   "<b>Report candidate count, false positives, and false "
   "negatives</b> at your chosen parameters.",
   "<b>Implement random hyperplane hashing</b> for cosine similarity "
   "and verify its collision probability.",
 ],
 "selfcheck": [
   "What is a shingle, and how do you choose k?",
   "Why does Jaccard suit this problem?",
   "What are the two separate problems, and what solves each?",
   "State the minhash property and sketch why it holds.",
   "Why are hash functions used instead of permutations?",
   "Give the standard error of a k-permutation estimate.",
   "Describe the banding construction and the candidate condition.",
   "Give the S-curve formula and the approximate threshold.",
   "What do b and r each control?",
   "Name three other LSH families and the general requirement.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Frequent Patterns",
 "subtitle": "Co-occurrence, and the rules that do not mean what they look like.",
 "question": "Which items appear together more than they should?",
 "outcomes": [
     "Explain support, confidence, and lift.",
     "Explain the monotonicity property and the algorithms "
     "using it.",
     "Explain why confidence is misleading.",
     "Explain the multiplicity problem in this setting.",
     "Mine and assess a rule set.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The measures",
   "blurb": "Three, and only one of them is honest alone."},

  {"t": "eq", "kicker": "Measures", "title": "Support, confidence, and lift",
   "eqs": [
     ("support(X) = P(X)",
      "The fraction of transactions containing X. A frequency, and "
      "the thing the algorithms prune on."),
     ("confidence(X → Y) = P(Y | X)",
      "How often Y appears given X. Intuitive, and misleading on "
      "its own — Part 3."),
     ("lift(X → Y) = P(Y | X) / P(Y)",
      "Confidence relative to Y's base rate. Lift = 1 means no "
      "association at all."),
   ],
   "caption": "<b>Lift is the one that accounts for the base "
              "rate</b> — and confidence without it is the standard "
              "error in this material.",
   "note": "Lead with lift; confidence alone has caused real bad "
           "decisions."},

  {"t": "callout", "title": "High confidence can mean nothing at all, because Y may simply be common",
   "kind": "The error this module exists to prevent",
   "body": ["<b>If 80% of all transactions contain bread, then any "
            "rule X → bread has confidence near 0.8</b> "
            "— including rules where X is entirely unrelated to "
            "bread.",
            "<b>So the rule 'customers who buy caviar also buy bread, "
            "with 80% confidence' is true and "
            "uninformative</b> — its lift is 1.0, meaning caviar "
            "tells you nothing.",
            "<b>Which is why lift, or a comparable measure, is "
            "necessary</b> — <b>and why a rule list sorted by "
            "confidence is dominated by whatever is most popular.</b>",
            "<b>And lift has its own problem:</b> <b>it is unstable "
            "for rare items</b>, where a handful of co-occurrences "
            "produces an enormous ratio — so report support "
            "alongside it, always."]},

  {"t": "section", "label": "Part 2", "title": "The algorithms",
   "blurb": "All of which exploit one property."},

  {"t": "code", "kicker": "Monotonicity", "title": "The property, and the algorithms it enables",
   "lang": "text", "code": """
  THE DOWNWARD CLOSURE PROPERTY
      if an itemset is frequent, every subset of it is
      frequent. Equivalently: if a set is infrequent,
      every superset is infrequent.

  WHICH PRUNES ENORMOUSLY
      a candidate set with any infrequent subset can
      be discarded without counting it.

  APRIORI
      level by level: generate candidates of size k+1
      only from frequent sets of size k, then count.
      One pass per level. Simple, and many passes.

  FP-GROWTH
      build a compressed prefix tree of the
      transactions, then mine it recursively.
      Two passes total. Faster, more memory.

  PCY AND ITS VARIANTS
      use the spare memory in pass 1 to hash pairs
      into counters, so pass 2 skips pairs whose
      bucket was infrequent. A nice use of memory
      that was going to be idle anyway.
""",
   "caption": "<b>Pass count is the design axis</b>, which is "
              "Module 01 §2's cost model determining the "
              "algorithm.",
   "note": "Framing the algorithm family by pass count unifies it."},

  {"t": "section", "label": "Part 3", "title": "What the rules mean",
   "blurb": "Less than they appear to."},

  {"t": "bullets", "kicker": "Caveats", "title": "The specific limits of an association rule",
   "items": [
     "<b>It is not causal.</b> <b>X → Y and Y → X have "
     "the same support and different confidences</b>, and neither says "
     "which came first.",
     "",
     "<b>It may be a confound.</b> <b>Both items may be driven by "
     "a third factor</b> — a season, a promotion, a store "
     "location, or a customer segment.",
     "",
     "<b>It may be an artefact of how transactions were "
     "defined.</b> <b>Change the basket boundary and the rules "
     "change</b> — which is a data-collection decision, not a "
     "finding.",
     "",
     "<b>And the famous examples are mostly "
     "unverified.</b> <b>The beer-and-nappies story has no published "
     "source</b>, which is worth knowing given how often it is "
     "cited.",
     "",
     "<b>So a rule is a starting point for an investigation</b>, "
     "not a conclusion.",
   ],
   "footnote": "<b>'Change the basket boundary and the rules change' "
               "is the most practically important caveat</b> — "
               "because it means the finding is partly a property of your "
               "schema."},

  {"t": "callout", "title": "And the multiplicity problem is acute here",
   "kind": "Module 01 §3, in its worst setting",
   "body": ["<b>Mining itemsets over a thousand items considers an "
            "astronomical candidate space</b> — and reports every "
            "set that passes a threshold, which is a search of "
            "unprecedented breadth.",
            "<b>So the rules returned include whatever passed by "
            "chance</b> — and at a low support threshold on a large "
            "transaction set, that is many of them.",
            "<b>Which means the support threshold is doing "
            "statistical work it was not designed for</b>: it is a "
            "computational pruning parameter being used as a significance "
            "filter.",
            "<b>So test the surviving rules properly:</b> <b>a "
            "permutation test on held-out transactions, with a "
            "correction for the number of rules tested</b> "
            "(Module 11) — <b>which almost no published "
            "application does.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Using it",
   "blurb": "Where this is actually the right tool."},

  {"t": "bullets", "kicker": "Practice", "title": "Where frequent pattern mining earns its place",
   "items": [
     "<b>Exploratory data understanding</b> — finding out "
     "what co-occurs in a dataset you do not know, which is a "
     "legitimate and honest use.",
     "",
     "<b>Feature construction</b>, where a frequent combination "
     "becomes a feature for a supervised model that is then evaluated "
     "properly (CSCE 633).",
     "",
     "<b>Constraint and dependency discovery</b> in databases and "
     "logs, where the patterns are structural rather than "
     "behavioural.",
     "",
     "<b>And sequence and episode mining</b>, where the ordering "
     "constraint cuts the candidate space and makes the findings more "
     "interpretable.",
     "",
     "<b>But for prediction, use a supervised model</b> — "
     "<b>rules are interpretable and are not competitive</b>, and "
     "choosing them for accuracy is a mistake.",
   ],
   "footnote": "<b>The exploratory use is the honest one</b>, and "
               "framing the output as hypotheses rather than findings "
               "resolves most of this module's difficulties."},

  {"t": "callout", "title": "What to report",
   "kind": "Closing",
   "body": ["<b>Support, confidence, <i>and</i> lift for every "
            "rule</b> — because the three together are interpretable "
            "and any one alone is not.",
            "<b>The thresholds you used and how many rules "
            "passed</b> — <b>which is the hypothesis count</b> "
            "(Module 11 §1).",
            "<b>The transaction definition</b>, explicitly, since the "
            "rules depend on it (Part 3).",
            "<b>And validation on held-out transactions for any rule "
            "you intend to act on</b> — <b>which is the step that "
            "distinguishes a hypothesis from a finding.</b>"]},
 ],
 "takeaways": [
   "Lift accounts for the base rate and confidence does not, which is the "
   "standard error in this material.",
   "A rule list sorted by confidence is dominated by whatever item is most "
   "popular, regardless of any association.",
   "Downward closure is the property every algorithm exploits, and pass "
   "count is the axis along which they differ.",
   "Change the basket boundary and the rules change, which makes the "
   "finding partly a property of your schema.",
   "The support threshold is a computational pruning parameter being used "
   "as a significance filter, which it was not designed for.",
   "The exploratory use is the honest one — frame the output as "
   "hypotheses rather than findings.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The measures"),
  ("eq", "support(X) = P(X) &nbsp;&nbsp; conf(X&rarr;Y) = P(Y|X) "
         "&nbsp;&nbsp; lift(X&rarr;Y) = P(Y|X) / P(Y)"),
  ("ul", ["<b>Support is the fraction of transactions containing "
          "X</b> — a frequency, and <b>the quantity the algorithms "
          "prune on</b> (&sect;2), which makes it structurally central as "
          "well as descriptively useful.",
          "<b>Confidence is how often Y appears given X</b> — "
          "<b>intuitive, and misleading on its own</b>, which is "
          "&sect;1's callout and &sect;3's warning.",
          "<b>Lift is confidence relative to Y's base rate.</b> "
          "<b>Lift = 1 means no association at all</b>; above 1 means Y "
          "is more likely given X; below 1 means less likely.",
          "<b>Lift is the one that accounts for the base rate</b> "
          "— and <b>confidence without it is the standard error in "
          "this material</b>, which is why this module leads with lift "
          "rather than introducing it as a refinement."]),
  ("callout", "High confidence can mean nothing at all, because Y may simply "
              "be common",
   ["<b>If 80% of all transactions contain bread, then <i>any</i> rule "
    "of the form X &rarr; bread has confidence near 0.8</b> — "
    "<b>including rules where X is entirely unrelated to bread</b>, "
    "because confidence is just the conditional frequency.",
    "<b>So the rule 'customers who buy caviar also buy bread, with 80% "
    "confidence' is simultaneously true and completely "
    "uninformative</b> — <b>its lift is 1.0, which means knowing "
    "about the caviar tells you nothing whatsoever about the bread.</b>",
    "<b>Which is why lift, or a comparable base-rate-adjusted measure, "
    "is necessary rather than optional</b> — and <b>why a rule list "
    "sorted by confidence is dominated by whatever items are most "
    "popular</b>, which is both useless and reliably "
    "convincing-looking.",
    "<b>And lift has its own problem worth stating:</b> <b>it is "
    "unstable for rare items</b>, where a handful of co-occurrences "
    "produces an enormous ratio with no real support behind it — "
    "<b>so report support alongside it, always</b>, and treat a "
    "high-lift low-support rule as noise until shown otherwise."]),

  ("h1", "2 &nbsp; The algorithms"),
  ("code", """THE DOWNWARD CLOSURE PROPERTY
    if an itemset is frequent, every subset of it is
    frequent. Equivalently: if a set is infrequent,
    then every superset of it is infrequent too.

WHICH PRUNES ENORMOUSLY
    a candidate set with any infrequent subset can be
    discarded without ever being counted.

APRIORI
    level by level: generate candidates of size k+1
    only from the frequent sets of size k, then count
    them. One pass per level. Simple, and many passes.

FP-GROWTH
    build a compressed prefix tree of the transactions,
    then mine it recursively. Two passes in total.
    Faster, and much more memory.

PCY AND ITS VARIANTS
    use the spare memory during pass 1 to hash item
    pairs into counters, so that pass 2 can skip any
    pair whose bucket was infrequent. A nice use of
    memory that was going to sit idle anyway."""),
  ("p", "<b>Pass count is the design axis</b> along which this family "
        "varies — Apriori trades passes for memory, FP-growth trades "
        "memory for passes, and PCY recovers some passes using memory "
        "that was already free. <b>Which is Module 01 &sect;2's cost "
        "model determining the algorithm</b> rather than asymptotic "
        "operation counts, and it is the clearest example of that "
        "principle in the course."),

  ("break",),
  ("h1", "3 &nbsp; What the rules actually mean"),
  ("ul", ["<b>It is not causal.</b> <b>X &rarr; Y and Y &rarr; X have "
          "exactly the same support and different confidences</b>, and "
          "<b>neither of them says anything about which came first</b> "
          "— the arrow is notation, not a claim about direction.",
          "<b>It may be a confound.</b> <b>Both items may be driven "
          "by a third factor</b> — a season, a promotion that "
          "bundled them, a store location, or a customer segment that "
          "buys both for unrelated reasons.",
          "<b>It may be an artefact of how transactions were "
          "defined.</b> <b>Change the basket boundary — a visit, a "
          "day, a session, an order — and the rules change</b> "
          "— <b>which is a data-collection decision rather than a "
          "finding about behaviour.</b> <b>This is the most practically "
          "important caveat</b>, because it means the finding is partly a "
          "property of your schema.",
          "<b>And the famous examples are mostly unverified.</b> "
          "<b>The beer-and-nappies story, which appears in nearly every "
          "introduction to this topic, has no published source</b> and "
          "appears to be apocryphal — which is worth knowing given "
          "how often it is offered as evidence that the technique "
          "works.",
          "<b>So a rule is a starting point for an investigation "
          "rather than a conclusion</b> — which is &sect;4's framing "
          "and resolves most of the difficulty with this material."]),
  ("callout", "And the multiplicity problem is acute here",
   ["<b>Mining itemsets over a thousand items considers an "
    "astronomically large candidate space</b> — and reports every "
    "set that passes a support threshold, <b>which is a search of "
    "unprecedented breadth</b> conducted automatically.",
    "<b>So the rules returned include whatever passed by chance</b> "
    "— and <b>at a low support threshold on a large transaction set, "
    "that is a great many of them</b>, with the most striking-looking "
    "rules being disproportionately likely to be the chance ones.",
    "<b>Which means the support threshold is doing statistical work it "
    "was never designed for:</b> <b>it is a computational pruning "
    "parameter being used as a significance filter</b>, and the "
    "relationship between a support level and a false discovery rate is "
    "not one anybody computed.",
    "<b>So test the surviving rules properly:</b> <b>a permutation "
    "test on held-out transactions, with a correction for the number of "
    "rules examined</b> (Module 11) — <b>which almost no "
    "published application of this technique does</b>, and which is "
    "Project 2's requirement."]),

  ("h1", "4 &nbsp; Where this is the right tool"),
  ("ul", ["<b>Exploratory data understanding</b> — finding out "
          "what co-occurs in a dataset you do not yet know, <b>which is a "
          "legitimate and honest use</b> because the output is explicitly "
          "a set of leads rather than conclusions.",
          "<b>Feature construction</b>, where a frequent combination "
          "becomes a candidate feature for a supervised model that is "
          "<i>then</i> evaluated properly (CSCE 633) — which "
          "moves the validation to where it can be done well.",
          "<b>Constraint and dependency discovery</b> in databases and "
          "in logs, where <b>the patterns are structural rather than "
          "behavioural</b> — a functional dependency that holds in "
          "every one of ten million rows is a different kind of finding "
          "from a shopping correlation.",
          "<b>And sequence and episode mining</b>, where <b>the "
          "ordering constraint cuts the candidate space substantially and "
          "makes the findings more interpretable</b>, because a temporal "
          "ordering at least constrains the causal direction.",
          "<b>But for prediction, use a supervised model.</b> "
          "<b>Rules are interpretable and are not competitive on "
          "accuracy</b>, and choosing them for predictive performance is "
          "a mistake — choose them when the interpretability is the "
          "deliverable. <b>The exploratory use is the honest one</b>, "
          "and <b>framing the output as hypotheses rather than findings "
          "resolves most of this module's difficulties.</b>"]),
  ("callout", "What to report",
   ["<b>Support, confidence, <i>and</i> lift for every rule</b> "
    "— <b>because the three together are interpretable and any one "
    "of them alone is not</b> (&sect;1), and giving all three costs "
    "nothing.",
    "<b>The thresholds you used and how many rules passed "
    "them</b> — <b>which is the hypothesis count</b> "
    "(Module 11 &sect;1), and is the number that makes the rest "
    "interpretable.",
    "<b>The transaction definition, explicitly</b>, since the rules "
    "depend on it (&sect;3) — and a reader who does not know your "
    "basket boundary cannot assess your rules at all.",
    "<b>And validation on held-out transactions for any rule you "
    "intend to act on</b> — <b>which is the step that distinguishes "
    "a hypothesis from a finding</b>, and is the whole of this course's "
    "position in one sentence."]),
 ],
 "resources": [
   ("Tan et al. &mdash; Introduction to Data Mining, chapters 5 and 6",
    "https://www-users.cse.umn.edu/~kumar001/dmbook/index.php",
    "<b>The whole module</b>, with the interestingness measures treated "
    "more carefully than elsewhere."),
   ("Mining of Massive Datasets, chapter 6 (free)",
    "http://www.mmds.org/",
    "<b>&sect;2's algorithms with the memory analysis</b> — and PCY "
    "is explained better here than anywhere."),
   ("Agrawal & Srikant &mdash; Fast Algorithms for Mining Association "
    "Rules (free)",
    "https://www.vldb.org/conf/1994/P487.PDF",
    "<b>&sect;2's first algorithm in the original</b>, with the closure "
    "property stated as the key insight."),
   ("Han et al. &mdash; Mining Frequent Patterns without Candidate "
    "Generation (free)",
    "https://dl.acm.org/doi/10.1145/342009.335372",
    "<b>&sect;2's second algorithm</b> — FP-growth, and the "
    "pass-count argument for it."),
 ],
 "exercises": [
   "<b>Compute support, confidence, and lift</b> for ten rules on a "
   "transaction dataset.",
   "<b>Sort by confidence and by lift</b> and compare the top ten "
   "lists.",
   "<b>Construct a high-confidence rule with lift 1.0</b> and explain "
   "it.",
   "<b>Find a high-lift low-support rule</b> and argue it is noise.",
   "<b>Implement Apriori</b> and count the passes it makes.",
   "<b>Implement FP-growth</b> and compare runtime and memory.",
   "<b>Change your transaction definition</b> and report how the top "
   "rules change.",
   "<b>Count the rules that passed your threshold</b> — this is "
   "your hypothesis count.",
   "<b>Run a permutation test</b> on your top ten rules.",
   "<b>Validate one rule on held-out transactions</b> and report the "
   "result either way.",
 ],
 "selfcheck": [
   "Define support, confidence, and lift.",
   "Why can high confidence mean nothing?",
   "What does a confidence-sorted rule list return?",
   "What is lift's own weakness?",
   "State the downward closure property and what it prunes.",
   "Contrast Apriori, FP-growth, and PCY by pass count and memory.",
   "Give four reasons a rule means less than it appears to.",
   "Which caveat is most practically important, and why?",
   "Why is the support threshold doing the wrong job?",
   "Give four legitimate uses, and what to use instead for "
   "prediction.",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Clustering at Scale",
 "subtitle": "Groups you did not know about, and whether they exist.",
 "question": "Are there natural groups, and how would you know?",
 "outcomes": [
     "Explain the main families and what each assumes.",
     "Explain the algorithms that handle data exceeding memory.",
     "Explain why cluster evaluation is genuinely hard.",
     "Explain how to choose k, and why the question is "
     "sometimes wrong.",
     "Assess a clustering honestly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Families",
   "blurb": "Each of which defines 'cluster' differently."},

  {"t": "table", "kicker": "Families", "title": "What each method means by “cluster”",
   "header": ["Family", "A cluster is", "Fails when"],
   "widths": [2.7, 4.0, 5.1],
   "rows": [
     ["<b>k-means</b>", "<b>Points near a centroid</b>", "<b>Clusters are elongated, unequal, or non-convex</b>"],
     ["<b>Hierarchical</b>", "<b>A merge in a dendrogram</b>", "<b>n is large — it is O(n²) or worse</b>"],
     ["<b>Density (DBSCAN)</b>", "<b>A dense region, any shape</b>", "<b>Densities vary across the data</b>"],
     ["<b>Spectral</b>", "<b>A well-connected part of a graph</b>", "<b>The affinity matrix is too large</b>"],
     ["<b>Mixture models</b>", "<b>A component of a distribution</b>", "<b>The parametric form is wrong</b>"],
   ],
   "footnote": "<b>So 'are there clusters' is not well posed until you "
               "say what a cluster is</b> — and different definitions "
               "give genuinely different and equally valid answers on the "
               "same data.",
   "note": "The not-well-posed point is the module's honest core."},

  {"t": "callout", "title": "k-means minimises within-cluster variance, and that assumption is doing a lot of work",
   "kind": "What the objective implies",
   "body": ["<b>Minimising squared distance to centroids assumes "
            "clusters are roughly spherical, of similar size, and of "
            "similar density</b> — <b>none of which it checks and "
            "all of which it requires.</b>",
            "<b>So it will partition a single elongated cluster and "
            "merge two adjacent spherical ones</b>, confidently, with no "
            "indication that anything went wrong.",
            "<b>And it always returns k clusters</b>, whether or not "
            "the data has any structure — <b>which means a "
            "k-means result is not evidence that clusters "
            "exist.</b>",
            "<b>But it is fast, simple, and scales</b> — so it is "
            "the right first thing to run and the wrong only thing to "
            "run, which is the honest summary of its place."]},

  {"t": "section", "label": "Part 2", "title": "At scale",
   "blurb": "When the data exceeds memory."},

  {"t": "code", "kicker": "Scale", "title": "The algorithms for data that does not fit",
   "lang": "text", "code": """
  MINI-BATCH K-MEANS
      update centroids from a sample each iteration.
      Converges to a slightly worse optimum, far
      faster. Almost always the right default.

  BFR
      assumes clusters are axis-aligned Gaussians, so
      a cluster can be summarised by (count, sum,
      sum of squares) per dimension. One pass:
      assign points to summaries, keep only
      summaries. Memory independent of n.

  CURE
      represents each cluster by a sample of
      REPRESENTATIVE POINTS rather than a centroid,
      so non-spherical clusters survive. One pass,
      and it relaxes BFR's assumption.

  AND THE COMMON IDEA
      summarise, discard the points, keep the
      summaries. Which works exactly when the
      summary is sufficient for the model's
      assumptions -- and fails silently when it
      is not.
""",
   "caption": "<b>Summarise and discard is the pattern</b> — and "
              "the summary's sufficiency is exactly the model assumption "
              "being made.",
   "note": "BFR and CURE differ precisely in what they assume a "
           "summary can capture."},

  {"t": "section", "label": "Part 3", "title": "Evaluation",
   "blurb": "The genuinely hard part."},

  {"t": "callout", "title": "Internal measures reward the shape the algorithm was optimising for",
   "kind": "Why this is circular",
   "body": ["<b>Silhouette, Davies–Bouldin, and the "
            "within-cluster sum of squares all measure compactness and "
            "separation</b> — <b>which is what k-means "
            "optimises</b>, so k-means scores well on them by "
            "construction.",
            "<b>And DBSCAN's non-convex clusters score badly on the "
            "same measures</b> while being correct — so the measure "
            "selects the algorithm rather than evaluating "
            "it.",
            "<b>So internal measures compare parameter settings "
            "within one algorithm and cannot compare across "
            "families</b> — which is the limit to respect.",
            "<b>And external measures need labels</b>, which you do "
            "not have — if you did, you would be doing "
            "classification. <b>So the honest answer is stability plus "
            "inspection</b> (Part 4)."]},

  {"t": "bullets", "kicker": "Evaluation", "title": "What actually works",
   "items": [
     "<b>Stability under resampling.</b> <b>Cluster two "
     "subsamples and check whether the same structure "
     "appears</b> — a clustering that changes completely was "
     "fitting noise.",
     "",
     "<b>Stability under perturbation</b>, including a different "
     "random seed — <b>k-means with a different "
     "initialisation giving a different answer is "
     "informative.</b>",
     "",
     "<b>A null comparison.</b> <b>Cluster data with the same "
     "marginals and no structure</b>, and compare your "
     "score — which is the only way to know whether your "
     "silhouette is good.",
     "",
     "<b>Inspection.</b> <b>Read fifty members of each "
     "cluster</b> and ask whether the grouping means anything to "
     "someone who knows the domain.",
     "",
     "<b>And downstream utility</b>, if the clustering feeds a "
     "task — which is the only fully objective "
     "measure.",
   ],
   "footnote": "<b>The null comparison is the one people "
               "skip</b> — and a silhouette of 0.4 means nothing "
               "until you know what structureless data of the same shape "
               "scores."},

  {"t": "section", "label": "Part 4", "title": "Choosing k",
   "blurb": "And when the question is wrong."},

  {"t": "bullets", "kicker": "Choosing k", "title": "The methods, and their honest status",
   "items": [
     "<b>The elbow method</b> — plot the objective against k "
     "and look for the bend. <b>Frequently there is no bend</b>, and "
     "the choice is then arbitrary.",
     "",
     "<b>Silhouette against k</b>, which is less arbitrary and "
     "inherits Part 3's circularity.",
     "",
     "<b>The gap statistic</b>, which compares against a null "
     "reference — <b>the most principled of these</b> and the "
     "most computation.",
     "",
     "<b>Stability against k</b>, which asks at which k the "
     "structure reproduces — and is the one worth doing.",
     "",
     "<b>Or: use a method that does not need k</b> — DBSCAN "
     "takes a density instead, and hierarchical clustering defers the "
     "choice to the cut.",
   ],
   "footnote": "<b>Swapping the parameter is not escaping the "
               "problem:</b> DBSCAN's density parameters are as "
               "consequential as k and are harder to "
               "interpret."},

  {"t": "callout", "title": "And sometimes the data has no clusters",
   "kind": "Closing",
   "body": ["<b>Most real high-dimensional data is one connected mass "
            "with varying density</b>, not a set of separated "
            "groups — <b>and a clustering algorithm will "
            "partition it anyway.</b>",
            "<b>So 'the data has three clusters' is a claim that "
            "needs the null comparison</b> "
            "(Part 3) — <b>without it, it is a "
            "description of your algorithm's output.</b>",
            "<b>And a partition can be useful without being "
            "real</b> — <b>customer segments for operational "
            "purposes do not have to be natural kinds</b>, provided you "
            "say which you are claiming.",
            "<b>Which is the distinction to state:</b> <b>'a useful "
            "partition' and 'discovered natural groups' are different "
            "claims</b>, and conflating them is this module's "
            "characteristic overclaim (Module 13)."]},
 ],
 "takeaways": [
   "'Are there clusters' is not well posed until you say what a cluster is, "
   "and different definitions give equally valid different answers.",
   "k-means always returns k clusters whether or not the data has "
   "structure, so its output is not evidence that clusters exist.",
   "Summarise and discard is the scale pattern, and the summary's "
   "sufficiency is exactly the model assumption being made.",
   "Internal measures reward the shape the algorithm optimised for, so "
   "they compare settings within a family and not across families.",
   "The null comparison is the step people skip, and a silhouette means "
   "nothing without it.",
   "'A useful partition' and 'discovered natural groups' are different "
   "claims, and conflating them is this module's characteristic overclaim.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Families"),
  ("table", ["Family", "What a cluster <i>is</i>", "Where it fails"],
   [["<b>k-means and variants</b>", "<b>Points near a centroid.</b>",
     "<b>Clusters that are elongated, of unequal size, of unequal "
     "density, or non-convex.</b>"],
    ["<b>Hierarchical (agglomerative)</b>",
     "<b>A merge at some level of a dendrogram.</b>",
     "<b>Large n</b> — it is O(n&sup2;) in memory and O(n&sup2; log "
     "n) or worse in time."],
    ["<b>Density-based (DBSCAN, HDBSCAN)</b>",
     "<b>A dense region of any shape, with noise points left "
     "unassigned.</b>",
     "<b>Densities that vary substantially across the data</b> — one "
     "parameter cannot suit both regions."],
    ["<b>Spectral</b>",
     "<b>A well-connected component of a similarity graph.</b>",
     "<b>The affinity matrix is O(n&sup2;)</b>, so it does not scale "
     "without approximation."],
    ["<b>Mixture models (EM)</b>",
     "<b>A component of a probability distribution.</b>",
     "<b>The parametric form is wrong</b>, and it will fit it "
     "anyway."]],
   [0.20, 0.32, 0.48]),
  ("p", "<b>So 'are there clusters in this data' is not a well-posed "
        "question until you say what a cluster is</b> — and "
        "<b>different definitions give genuinely different and equally "
        "valid answers on the same data</b>, which is not a defect of the "
        "methods but a property of the question. <b>This is the module's "
        "honest core</b>, and it is why &sect;3's evaluation problem is "
        "hard rather than merely unsolved."),
  ("callout", "k-means minimises within-cluster variance, and that "
              "assumption is doing a lot of work",
   ["<b>Minimising the squared distance to centroids assumes clusters "
    "are roughly spherical, of similar size, and of similar "
    "density</b> — <b>none of which it checks, and all of which it "
    "requires</b> for the objective to correspond to anything you would "
    "recognise as a cluster.",
    "<b>So it will happily partition a single elongated cluster into "
    "three, and merge two adjacent spherical ones into one</b> — "
    "<b>confidently, with a good objective value, and with no indication "
    "at all that anything went wrong.</b>",
    "<b>And it always returns exactly k clusters</b>, whether or not "
    "the data has any group structure whatsoever — <b>which means a "
    "k-means result is not, by itself, evidence that clusters "
    "exist</b> (&sect;4's closing callout).",
    "<b>But it is fast, simple, well understood, and it "
    "scales</b> — so <b>it is the right first thing to run and the "
    "wrong only thing to run</b>, which is the honest summary of its "
    "place in practice and is not a criticism."]),

  ("h1", "2 &nbsp; At scale"),
  ("code", """MINI-BATCH K-MEANS
    update the centroids from a random sample each
    iteration. Converges to a slightly worse optimum,
    far faster. Almost always the right default at
    scale.

BFR
    assumes clusters are axis-aligned Gaussians, so a
    cluster can be summarised by (count, sum, sum of
    squares) per dimension. One pass: assign points
    to summaries, keep only the summaries. Memory
    independent of n.

CURE
    represents each cluster by a sample of
    REPRESENTATIVE POINTS rather than by a centroid,
    so non-spherical clusters survive the
    summarisation. One pass, and it relaxes BFR's
    assumption at some cost in memory.

AND THE COMMON IDEA
    summarise, discard the points, keep the summaries.
    Which works exactly when the summary is sufficient
    for the model's assumptions -- and fails silently
    when it is not."""),
  ("p", "<b>Summarise and discard is the pattern</b>, and <b>the "
        "summary's sufficiency is precisely the model assumption being "
        "made</b>. <b>BFR and CURE differ exactly in what they assume a "
        "summary can capture</b>: BFR's three moments are sufficient "
        "statistics for an axis-aligned Gaussian and lose everything else, "
        "whereas CURE's representative points retain shape at the cost of "
        "storing more. <b>Reading the summary as the assumption is the "
        "transferable idea</b>, and it recurs in Module 06's "
        "sketches."),

  ("break",),
  ("h1", "3 &nbsp; Evaluation"),
  ("callout", "Internal measures reward the shape the algorithm was "
              "optimising for",
   ["<b>Silhouette, Davies&ndash;Bouldin, and the within-cluster sum of "
    "squares all measure compactness and separation</b> — <b>which "
    "is exactly what k-means optimises</b>, so <b>k-means scores well on "
    "them by construction</b> rather than by being right.",
    "<b>And DBSCAN's correctly identified non-convex clusters score "
    "badly on the same measures</b> while being, by any reasonable "
    "reading, the better answer — so <b>the measure selects the "
    "algorithm rather than evaluating it.</b>",
    "<b>So internal measures can compare parameter settings within one "
    "algorithm and cannot compare across families</b> — which is the "
    "limit to respect, and is routinely violated in comparisons that "
    "report silhouette across methods.",
    "<b>And external measures need labels</b>, which you do not "
    "have — <b>if you did, you would be doing classification rather "
    "than clustering.</b> <b>So the honest answer is stability plus "
    "inspection plus a null comparison</b>, which is what follows."]),
  ("ul", ["<b>Stability under resampling.</b> <b>Cluster two disjoint "
          "subsamples and check whether the same structure appears in "
          "both</b> — <b>a clustering that changes completely was "
          "fitting noise</b>, and this is the single most informative "
          "check available.",
          "<b>Stability under perturbation</b>, including simply a "
          "different random seed — <b>k-means producing a "
          "substantially different answer from a different initialisation "
          "is informative</b> about whether the structure is there, and "
          "it costs one re-run.",
          "<b>A null comparison.</b> <b>Cluster data with the same "
          "marginal distributions and no group structure, and compare "
          "your score against it</b> — <b>which is the only way to "
          "know whether your silhouette of 0.4 is good</b>, since the "
          "scale has no absolute meaning.",
          "<b>Inspection.</b> <b>Read fifty members of each "
          "cluster</b> and ask whether the grouping means anything to "
          "somebody who knows the domain — which is slow, "
          "unglamorous, and finds things no statistic does.",
          "<b>And downstream utility</b>, if the clustering feeds a "
          "task with its own metric — <b>which is the only fully "
          "objective measure available</b> and should be preferred "
          "whenever it exists. <b>The null comparison is the one people "
          "skip</b>, and <b>a silhouette of 0.4 means nothing until you "
          "know what structureless data of the same shape scores</b>, "
          "which is frequently around 0.3."]),

  ("h1", "4 &nbsp; Choosing k"),
  ("ul", ["<b>The elbow method</b> — plot the objective against k "
          "and look for the bend. <b>Frequently there is no bend at "
          "all</b>, the curve being smooth, <b>and the choice is then "
          "arbitrary while appearing principled.</b>",
          "<b>Silhouette against k</b>, which is less arbitrary than "
          "the elbow and <b>inherits &sect;3's circularity</b> — it "
          "will prefer the k that produces the most spherical "
          "partition.",
          "<b>The gap statistic</b>, which compares the objective "
          "against a null reference distribution at each k — <b>the "
          "most principled of these methods</b> and <b>the most "
          "computation</b>, since it requires clustering the null data "
          "repeatedly.",
          "<b>Stability against k</b>, which asks at which k the "
          "structure reproduces across subsamples — <b>and is the "
          "one worth doing</b>, because it answers the question you "
          "actually care about rather than a proxy for it.",
          "<b>Or: use a method that does not require k</b> — "
          "DBSCAN takes density parameters instead, and hierarchical "
          "clustering defers the choice to where you cut the "
          "dendrogram. <b>But swapping the parameter is not escaping the "
          "problem:</b> <b>DBSCAN's density parameters are as "
          "consequential as k and are considerably harder to "
          "interpret</b>, so the decision has moved rather than "
          "disappeared."]),
  ("callout", "And sometimes the data has no clusters",
   ["<b>Most real high-dimensional data is one connected mass with "
    "varying density</b> rather than a set of well-separated "
    "groups — <b>and a clustering algorithm will partition it "
    "anyway</b>, returning exactly as many groups as you asked for.",
    "<b>So 'the data has three clusters' is a claim that requires the "
    "null comparison</b> (&sect;3) — <b>and without it, the "
    "statement is a description of your algorithm's output rather than a "
    "finding about the data.</b>",
    "<b>And a partition can be genuinely useful without being "
    "real</b> — <b>customer segments for operational purposes do not "
    "have to be natural kinds</b> to be worth having, provided you are "
    "clear about which claim you are making.",
    "<b>Which is the distinction to state explicitly:</b> <b>'a useful "
    "partition' and 'discovered natural groups' are different "
    "claims</b> with different evidential requirements, and "
    "<b>conflating them is this module's characteristic overclaim</b> "
    "(Module 13 &sect;1)."]),
 ],
 "resources": [
   ("Mining of Massive Datasets, chapter 7 (free)",
    "http://www.mmds.org/",
    "<b>&sect;2's scale algorithms</b> — BFR and CURE, with the "
    "assumptions stated clearly."),
   ("Tan et al., chapters 7 and 8",
    "https://www-users.cse.umn.edu/~kumar001/dmbook/index.php",
    "<b>&sect;1 and &sect;3</b> — and the cluster validity chapter is "
    "the best available treatment of the evaluation problem."),
   ("von Luxburg &mdash; A Tutorial on Spectral Clustering (free)",
    "https://arxiv.org/abs/0711.0189",
    "<b>&sect;1's fourth row, properly</b> — and the connection to "
    "graph cuts, which Module 07 uses."),
   ("Ben-David, von Luxburg & P&aacute;l &mdash; A Sober Look at "
    "Clustering Stability (free)",
    "https://link.springer.com/chapter/10.1007/11776420_4",
    "<b>&sect;3's stability measure, examined critically</b> — "
    "including when it does not work."),
 ],
 "exercises": [
   "<b>Cluster the same data with k-means, DBSCAN, and hierarchical</b>, "
   "and compare the partitions.",
   "<b>Construct data k-means gets wrong</b> — elongated, unequal, "
   "and non-convex.",
   "<b>Run k-means on uniform random data</b> and observe that it "
   "returns k clusters.",
   "<b>Implement BFR's summaries</b> and confirm memory is independent "
   "of n.",
   "<b>Show where BFR's assumption fails</b> and what CURE recovers.",
   "<b>Compute silhouette for k-means and DBSCAN</b> on non-convex data, "
   "and explain the ranking.",
   "<b>Run the null comparison</b> and report what structureless data "
   "scores.",
   "<b>Test stability across two subsamples</b> and quantify the "
   "agreement.",
   "<b>Plot elbow, silhouette, and stability against k</b> and compare "
   "what each suggests.",
   "<b>Read fifty members of one cluster</b> and say whether the "
   "grouping means anything.",
 ],
 "selfcheck": [
   "Name five families and what each means by 'cluster'.",
   "Why is 'are there clusters' not well posed?",
   "What does k-means assume, and what does it do when the assumption "
   "fails?",
   "Why is a k-means result not evidence that clusters exist?",
   "What is the common idea behind the scale algorithms?",
   "How do BFR and CURE differ?",
   "Why are internal measures circular?",
   "What can internal measures legitimately compare?",
   "Give five things that actually work for evaluation.",
   "State the distinction between a useful partition and natural "
   "groups.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Dimensionality Reduction",
 "subtitle": "Fewer dimensions, and what each method keeps.",
 "question": "Does the data lie near a simpler space?",
 "outcomes": [
     "Explain the curse of dimensionality concretely.",
     "Explain PCA and SVD and what they preserve.",
     "Explain random projection and its guarantee.",
     "Explain the nonlinear methods and their dangers.",
     "Choose a method by what must be preserved.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The curse",
   "blurb": "Specifically, and it is worse than it sounds."},

  {"t": "bullets", "kicker": "Consequences", "title": "What high dimension actually does",
   "items": [
     "<b>Distances concentrate.</b> <b>The ratio between the "
     "nearest and farthest neighbour approaches 1</b> — so "
     "<b>'nearest' stops being meaningful</b>, which breaks every "
     "distance-based method.",
     "",
     "<b>Volume moves to the corners.</b> <b>Almost all the volume "
     "of a high-dimensional ball is near its surface</b>, so "
     "intuitions from two dimensions mislead "
     "systematically.",
     "",
     "<b>Sampling density collapses.</b> <b>Covering a space to "
     "a fixed resolution needs exponentially many points</b> in the "
     "dimension.",
     "",
     "<b>And everything becomes orthogonal.</b> <b>Random vectors "
     "in high dimension are nearly perpendicular</b>, which is both a "
     "problem and the basis of random projection "
     "(Part 3).",
     "",
     "<b>So reduction is not only about cost</b> — it is "
     "frequently about making the problem meaningful at "
     "all.",
   ],
   "footnote": "<b>Distance concentration is the one with the widest "
               "consequences</b> — it is why nearest-neighbour "
               "methods, clustering, and anomaly detection all degrade "
               "in high dimension."},

  {"t": "callout", "title": "But real high-dimensional data usually has low intrinsic dimension",
   "kind": "Why reduction works at all",
   "body": ["<b>A thousand-pixel image of a rotating object varies "
            "along one parameter</b> — so the data lies on a "
            "one-dimensional curve in a thousand-dimensional space.",
            "<b>And this is typical.</b> <b>Correlated features, "
            "physical constraints, and generative structure all mean the "
            "data occupies a small part of its "
            "space.</b>",
            "<b>Which is what makes reduction possible rather than "
            "merely lossy</b> — <b>you are discarding dimensions the "
            "data does not use</b>, not compressing dimensions it "
            "does.",
            "<b>So the question for every method is: what structure "
            "does it preserve, and is that the structure you "
            "need?</b> — which is Part 4's framing and the "
            "module's organising question."]},

  {"t": "section", "label": "Part 2", "title": "Linear methods",
   "blurb": "PCA and SVD, which are the same thing."},

  {"t": "eq", "kicker": "SVD", "title": "The decomposition, and what the truncation gives",
   "eqs": [
     ("A = U Σ Vᵀ",
      "Any matrix. U and V orthogonal, Σ diagonal with the singular "
      "values in decreasing order."),
     ("Aₖ = Uₖ Σₖ Vₖᵀ",
      "Keep the top k. This is the best rank-k approximation in "
      "Frobenius norm — the Eckart–Young theorem."),
     ("PCA = SVD of the centred data",
      "So they are the same computation; PCA's covariance "
      "eigenvectors are the right singular vectors."),
   ],
   "caption": "<b>Best rank-k approximation is a theorem, not a "
              "heuristic</b> — which is what distinguishes these "
              "methods from the nonlinear ones.",
   "note": "Stating Eckart–Young explains why PCA is the "
           "default."},

  {"t": "bullets", "kicker": "Practice", "title": "And what to know in practice",
   "items": [
     "<b>Centre the data, and think about scaling.</b> <b>PCA on "
     "unscaled features is dominated by whichever has the largest "
     "units</b>, which is a measurement artefact rather than "
     "structure.",
     "",
     "<b>The explained variance ratio tells you how much you "
     "kept</b> — and <b>a scree plot is the honest way to choose "
     "k</b>, with the same elbow problem as "
     "Module 04 §4.",
     "",
     "<b>Components are orthogonal and are not "
     "interpretable</b> by default — <b>reading meaning into "
     "principal component two is a common and unjustified "
     "move.</b>",
     "",
     "<b>Truncated and randomised SVD scale to large "
     "matrices</b>, computing only the top k, which is what makes this "
     "usable at this course's scale.",
     "",
     "<b>And for sparse non-negative data, consider NMF</b>, "
     "whose components are additive and frequently more "
     "interpretable.",
   ],
   "footnote": "<b>The uninterpretability point is worth "
               "insisting on</b> — PCA maximises variance, and "
               "variance has no reason to align with anything "
               "meaningful."},

  {"t": "section", "label": "Part 3", "title": "Random projection",
   "blurb": "A guarantee that requires nothing from the data."},

  {"t": "callout", "title": "Projecting onto random directions preserves all pairwise distances, with high probability",
   "kind": "The Johnson–Lindenstrauss result",
   "body": ["<b>Any n points in any dimension can be projected into "
            "O(log n / ε²) dimensions with every pairwise "
            "distance preserved to within a factor "
            "(1 ± ε).</b>",
            "<b>And the target dimension depends on n and "
            "ε only</b> — <b>not on the original "
            "dimension at all</b>, which is the surprising part and is "
            "what makes it useful.",
            "<b>The projection is a random matrix</b>, so it costs "
            "nothing to construct, needs no pass over the data to fit, "
            "and is trivially parallel — unlike PCA.",
            "<b>So the trade against PCA is clear:</b> <b>PCA is "
            "optimal for the data and requires computing it; JL is "
            "data-oblivious and gives a distance guarantee "
            "instead</b> — and for distance-based methods, the "
            "guarantee is what you wanted."]},

  {"t": "section", "label": "Part 4", "title": "Nonlinear methods",
   "blurb": "Useful, and easy to over-read."},

  {"t": "table", "kicker": "Nonlinear", "title": "The methods, and what they preserve",
   "header": ["Method", "Preserves", "The danger"],
   "widths": [2.6, 3.9, 5.1],
   "rows": [
     ["<b>t-SNE</b>", "<b>Local neighbourhoods</b>", "<b>Cluster sizes and distances are meaningless</b>"],
     ["<b>UMAP</b>", "<b>Local, some global</b>", "<b>The same, slightly less so</b>"],
     ["<b>Isomap / MDS</b>", "<b>Geodesic or metric distances</b>", "<b>O(n²); sensitive to the neighbour graph</b>"],
     ["<b>Autoencoders</b>", "<b>Whatever the loss rewards</b>", "<b>No guarantee; needs training and tuning</b>"],
   ],
   "footnote": "<b>The t-SNE caution is the important one:</b> in a "
               "t-SNE plot, <b>the distance between two clusters and the "
               "relative size of clusters carry no information</b> "
               "— and both are routinely interpreted.",
   "note": "The t-SNE misreading is extremely common and worth "
           "attacking directly."},

  {"t": "callout", "title": "Choose by what must be preserved",
   "kind": "Closing",
   "body": ["<b>Variance and a reconstruction guarantee → "
            "PCA or truncated SVD</b>, which is also the right choice "
            "when you need to project new points cheaply.",
            "<b>Pairwise distances, with a bound, at scale → "
            "random projection</b>, especially as a preprocessing step "
            "before a distance-based method.",
            "<b>Visual exploration of local structure → "
            "t-SNE or UMAP</b>, <b>with the caveats stated on the "
            "figure</b>, which almost nobody does.",
            "<b>And a learned nonlinear representation for a "
            "downstream task → an autoencoder</b>, evaluated by "
            "the downstream task rather than by reconstruction "
            "loss."]},
 ],
 "takeaways": [
   "Distance concentration means 'nearest' stops being meaningful in high "
   "dimension, which is why distance-based methods degrade.",
   "Real high-dimensional data usually has low intrinsic dimension, which "
   "is what makes reduction possible rather than merely lossy.",
   "Truncated SVD gives the best rank-k approximation by theorem, which is "
   "what distinguishes it from the nonlinear methods.",
   "PCA components are orthogonal and not interpretable; reading meaning "
   "into a principal component is unjustified by default.",
   "Johnson–Lindenstrauss's target dimension depends on n and "
   "ε only, not on the original dimension.",
   "In a t-SNE plot, inter-cluster distance and relative cluster size "
   "carry no information, and both are routinely interpreted.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The curse of dimensionality"),
  ("ul", ["<b>Distances concentrate.</b> <b>The ratio between the "
          "distance to the nearest and the farthest neighbour approaches "
          "1 as the dimension grows</b> — so <b>'nearest' stops "
          "being a meaningful notion</b>, which breaks nearest-neighbour "
          "search, clustering (Module 04), and anomaly detection "
          "(Module 08) simultaneously.",
          "<b>Volume moves to the corners.</b> <b>Almost all the "
          "volume of a high-dimensional ball lies near its surface, and "
          "the ball occupies a vanishing fraction of its bounding "
          "cube</b> — so two-dimensional and three-dimensional "
          "intuitions mislead systematically rather than "
          "occasionally.",
          "<b>Sampling density collapses.</b> <b>Covering a space to "
          "a fixed resolution requires exponentially many points in the "
          "dimension</b>, which means any real dataset is extremely "
          "sparse in its own space.",
          "<b>And everything becomes orthogonal.</b> <b>Two random "
          "vectors in high dimension are nearly perpendicular with high "
          "probability</b> — which is <b>both a problem and the "
          "basis of random projection</b> (&sect;3), and that dual role "
          "is worth noticing.",
          "<b>So reduction is not only about computational cost</b> "
          "— <b>it is frequently about making the problem meaningful "
          "at all</b>. <b>Distance concentration is the consequence with "
          "the widest reach</b>, because so many of this course's methods "
          "are distance-based."]),
  ("callout", "But real high-dimensional data usually has low intrinsic "
              "dimension",
   ["<b>A thousand-pixel image of a single object rotating varies along "
    "exactly one parameter</b> — so <b>the data lies on a "
    "one-dimensional curve embedded in a thousand-dimensional "
    "space</b>, and 999 of those dimensions are unused.",
    "<b>And this is typical rather than contrived.</b> "
    "<b>Correlated features, physical constraints, and the generative "
    "process behind the data all mean that real data occupies a small "
    "part of its nominal space.</b>",
    "<b>Which is exactly what makes reduction possible rather than "
    "merely lossy</b> — <b>you are discarding dimensions the data "
    "does not use</b>, rather than compressing dimensions it does, and "
    "the distinction determines whether the reduction costs you "
    "anything.",
    "<b>So the question to ask of every method is: what structure does "
    "it preserve, and is that the structure you need?</b> — which "
    "is <b>&sect;4's framing and this module's organising "
    "question</b>, and it is a better way to choose than by "
    "popularity."]),

  ("h1", "2 &nbsp; Linear methods"),
  ("eq", "A = U &Sigma; V<sup>T</sup> &nbsp;&nbsp;&nbsp; "
         "A<sub>k</sub> = U<sub>k</sub> &Sigma;<sub>k</sub> "
         "V<sub>k</sub><sup>T</sup>"),
  ("ul", ["<b>Any matrix decomposes this way.</b> U and V are "
          "orthogonal, and &Sigma; is diagonal with the singular values "
          "in decreasing order — which is what makes truncation "
          "natural.",
          "<b>Keeping the top k gives the best rank-k approximation in "
          "Frobenius norm</b> — <b>the Eckart&ndash;Young "
          "theorem</b>, and <b>this is a theorem rather than a "
          "heuristic</b>, which is precisely what distinguishes these "
          "methods from the nonlinear ones in &sect;4.",
          "<b>And PCA is the SVD of the centred data</b> — so "
          "<b>they are the same computation</b>, with PCA's covariance "
          "eigenvectors being the right singular vectors. Knowing that "
          "saves learning two things.",
          "<b>Stating Eckart&ndash;Young explains why PCA is the "
          "default</b>: it is not merely a reasonable choice but the "
          "provably optimal linear one for reconstruction error, which is "
          "a strong position for a method this cheap."]),
  ("ul", ["<b>Centre the data, and think carefully about "
          "scaling.</b> <b>PCA on unscaled features is dominated by "
          "whichever feature has the largest units</b> — which is a "
          "measurement artefact rather than structure, and is the "
          "commonest mistake with the method.",
          "<b>The explained variance ratio tells you how much you "
          "kept</b> — and <b>a scree plot is the honest way to "
          "choose k</b>, with <b>exactly the same elbow problem as "
          "Module 04 &sect;4's</b>: frequently there is no bend.",
          "<b>Components are orthogonal and are not interpretable by "
          "default</b> — <b>reading meaning into principal component "
          "two is a common and unjustified move</b>. <b>PCA maximises "
          "variance, and variance has no reason at all to align with "
          "anything meaningful</b>, so interpretation requires separate "
          "evidence.",
          "<b>Truncated and randomised SVD scale to large "
          "matrices</b>, computing only the top k components without "
          "forming the full decomposition — <b>which is what makes "
          "this usable at this course's scale</b> and is worth knowing "
          "exists.",
          "<b>And for sparse non-negative data, consider "
          "non-negative matrix factorisation</b>, whose components are "
          "additive rather than signed and are <b>frequently genuinely "
          "more interpretable</b> — at the cost of losing the "
          "optimality guarantee."]),

  ("break",),
  ("h1", "3 &nbsp; Random projection"),
  ("callout", "Projecting onto random directions preserves all pairwise "
              "distances, with high probability",
   ["<b>Any n points in any dimension whatsoever can be projected into "
    "O(log n / &epsilon;&sup2;) dimensions with every pairwise distance "
    "preserved to within a factor of (1 &plusmn; &epsilon;)</b> — "
    "the Johnson&ndash;Lindenstrauss lemma.",
    "<b>And the target dimension depends on n and &epsilon; "
    "only</b> — <b>not on the original dimension at all</b>, which "
    "is the genuinely surprising part: a million-dimensional dataset and "
    "a thousand-dimensional one with the same number of points need the "
    "same target dimension.",
    "<b>The projection is simply a random matrix</b>, so <b>it costs "
    "nothing to construct, requires no pass over the data to fit, and is "
    "trivially parallel and streamable</b> — all of which are "
    "properties PCA lacks, since PCA must be computed from the data.",
    "<b>So the trade against PCA is clear:</b> <b>PCA is optimal for "
    "your specific data and requires computing it; "
    "Johnson&ndash;Lindenstrauss is data-oblivious and gives a distance "
    "guarantee instead</b> — and <b>for distance-based methods, the "
    "distance guarantee is precisely what you wanted</b> rather than a "
    "consolation. The proof is a concentration argument "
    "(CSCE 658 Module 03)."]),

  ("h1", "4 &nbsp; Nonlinear methods"),
  ("table", ["Method", "What it preserves", "The danger"],
   [["<b>t-SNE</b>",
     "<b>Local neighbourhoods — which points are near which.</b>",
     "<b>Cluster sizes and inter-cluster distances are "
     "meaningless</b> — see the note."],
    ["<b>UMAP</b>",
     "<b>Local structure, and somewhat more global structure than "
     "t-SNE.</b>",
     "<b>The same caution, slightly less severely</b> — and the "
     "hyperparameters change the picture substantially."],
    ["<b>Isomap and MDS</b>",
     "<b>Geodesic distances along a neighbour graph, or the metric "
     "directly.</b>",
     "<b>O(n&sup2;), and very sensitive to the neighbour graph's "
     "construction</b> — a single bad edge short-circuits the "
     "manifold."],
    ["<b>Autoencoders</b>",
     "<b>Whatever the loss function rewards.</b>",
     "<b>No guarantee of any kind; and it needs training, tuning, and "
     "its own evaluation</b> (CSCE 636)."]],
   [0.20, 0.32, 0.48]),
  ("p", "<b>The t-SNE caution is the important one, and it is worth "
        "attacking directly because the misreading is so "
        "common:</b> <b>in a t-SNE plot, the distance between two "
        "clusters and the relative sizes of the clusters carry no "
        "information at all</b> — the method optimises local "
        "neighbourhood preservation and explicitly does not preserve "
        "either — <b>and both are routinely interpreted in published "
        "figures</b>, usually as evidence of how distinct or how large a "
        "group is. <b>The perplexity parameter also changes the apparent "
        "number of clusters</b>, which means a t-SNE figure without its "
        "parameters is uninterpretable."),
  ("callout", "Choose by what must be preserved",
   ["<b>Variance and a reconstruction guarantee &rarr; PCA or truncated "
    "SVD</b> — which is also the right choice when you need to "
    "project new points cheaply, since the transformation is a fixed "
    "matrix.",
    "<b>Pairwise distances, with a stated bound, at scale &rarr; "
    "random projection</b> (&sect;3) — <b>especially as a "
    "preprocessing step before a distance-based method</b> such as LSH "
    "(Module 02) or clustering (Module 04).",
    "<b>Visual exploration of local structure &rarr; t-SNE or "
    "UMAP</b>, <b>with the caveats stated on the figure itself</b> "
    "— <b>which almost nobody does</b>, and which would prevent most "
    "of the misreading.",
    "<b>And a learned nonlinear representation for a downstream task "
    "&rarr; an autoencoder</b>, <b>evaluated by the downstream task "
    "rather than by its reconstruction loss</b> — since a low "
    "reconstruction error says nothing about whether the representation "
    "is useful for anything."]),
 ],
 "resources": [
   ("Tan et al., the dimensionality reduction appendix",
    "https://www-users.cse.umn.edu/~kumar001/dmbook/index.php",
    "<b>&sect;1 and &sect;2</b>, with the curse of dimensionality "
    "developed carefully."),
   ("Mining of Massive Datasets, chapter 11 (free)",
    "http://www.mmds.org/",
    "<b>&sect;2 and &sect;3</b> — SVD, CUR, and the scale "
    "considerations, free in full."),
   ("Wattenberg, Vi&eacute;gas & Johnson &mdash; How to Use t-SNE "
    "Effectively (free)",
    "https://distill.pub/2016/misread-tsne/",
    "<b>&sect;4's caution, demonstrated interactively</b> — the "
    "single best corrective to the common misreading."),
   ("Achlioptas &mdash; Database-friendly random projections (free)",
    "https://dl.acm.org/doi/10.1145/375551.375608",
    "<b>&sect;3 with a projection matrix you can compute "
    "cheaply</b> — the practical version of the lemma."),
 ],
 "exercises": [
   "<b>Measure the nearest-to-farthest distance ratio</b> as dimension "
   "grows from 2 to 1000.",
   "<b>Compute the fraction of a ball's volume</b> within 10% of its "
   "surface, by dimension.",
   "<b>Measure the angle between random vectors</b> at increasing "
   "dimension.",
   "<b>Estimate the intrinsic dimension</b> of a real dataset you "
   "have.",
   "<b>Run PCA with and without feature scaling</b> and compare the "
   "first component.",
   "<b>Plot a scree plot</b> and say whether there is an elbow.",
   "<b>Implement random projection</b> and measure the distance "
   "distortion against the bound.",
   "<b>Compare PCA and random projection</b> as preprocessing for "
   "nearest-neighbour search.",
   "<b>Run t-SNE at three perplexities</b> and compare the apparent "
   "cluster count.",
   "<b>Write the caveat</b> you would put on a t-SNE figure.",
 ],
 "selfcheck": [
   "Give four consequences of high dimension, and the one with widest "
   "reach.",
   "Why does real data usually have low intrinsic dimension?",
   "What makes reduction possible rather than merely lossy?",
   "State the SVD and what truncation gives you.",
   "What is the relationship between PCA and SVD?",
   "Why are PCA components not interpretable?",
   "State the Johnson–Lindenstrauss result and what is surprising "
   "about it.",
   "Give the trade between PCA and random projection.",
   "Name four nonlinear methods and what each preserves.",
   "What carries no information in a t-SNE plot?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Streams and Sketches",
 "subtitle": "One pass, bounded memory, a stated error.",
 "question": "What can you compute seeing each item once?",
 "outcomes": [
     "Explain the streaming model and its constraints.",
     "Explain reservoir sampling and why it is uniform.",
     "Explain the counting sketches and their guarantees.",
     "Explain cardinality estimation.",
     "Verify a sketch's error bound empirically.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The model",
   "blurb": "And why it is the realistic one."},

  {"t": "callout", "title": "One pass, memory sublinear in the stream length, and an answer with a stated error",
   "kind": "The constraints, and what they force",
   "body": ["<b>The stream is unbounded or too large to store</b>, "
            "each item is seen once, and the memory is "
            "polylogarithmic — <b>which rules out storing the data "
            "and therefore rules out exact answers for most "
            "questions.</b>",
            "<b>So every streaming result is a trade between memory, "
            "accuracy, and failure probability</b> — and <b>stating "
            "all three is what makes it a result rather than a "
            "heuristic.</b>",
            "<b>And this is the realistic model more often than it "
            "appears</b>: log processing, network monitoring, click "
            "streams, and sensor data all have this shape, and so does "
            "any dataset larger than memory read sequentially.",
            "<b>Which is Module 01 §2's cost model taken "
            "to its limit</b> — <b>one pass is the minimum, and "
            "several of these algorithms achieve it.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Sampling",
   "blurb": "A uniform sample from an unknown-length stream."},

  {"t": "code", "kicker": "Reservoir", "title": "Reservoir sampling, and why it is uniform",
   "lang": "text", "code": """
  KEEP k ITEMS. For the i-th item (i > k):
      with probability k/i, replace a uniformly
      chosen one of the k held items with it.

  THE CLAIM
      after n items, every item has probability k/n
      of being in the reservoir -- and this holds at
      every n, without knowing n in advance.

  WHY (sketch, for k = 1)
      item i is kept at step i with probability 1/i,
      and survives each later step j with
      probability (j-1)/j. The product telescopes:
          (1/i) * (i/(i+1)) * ... * ((n-1)/n) = 1/n

  WHICH IS THE WHOLE TRICK: the acceptance
  probability falls exactly as fast as the survival
  probability accumulates.

  AND FOR WEIGHTED OR SLIDING-WINDOW SAMPLING the
  construction changes; do not assume this version
  generalises.
""",
   "caption": "<b>The telescoping product is the proof</b>, and it is "
              "worth writing out once — it explains why the k/i "
              "probability is exactly right.",
   "note": "The telescoping argument makes this memorable rather than "
           "magical."},

  {"t": "section", "label": "Part 3", "title": "Counting sketches",
   "blurb": "Frequencies in sublinear space."},

  {"t": "table", "kicker": "Sketches", "title": "The sketches, and what each guarantees",
   "header": ["Sketch", "Answers", "Guarantee"],
   "widths": [2.7, 3.9, 5.2],
   "rows": [
     ["<b>Bloom filter</b>", "<b>Is x in the set?</b>", "<b>No false negatives; tunable false positives</b>"],
     ["<b>Count-Min</b>", "<b>How often did x occur?</b>", "<b>Never underestimates; bounded overestimate</b>"],
     ["<b>Count-Sketch</b>", "<b>The same</b>", "<b>Unbiased, with variance — can go either way</b>"],
     ["<b>HyperLogLog</b>", "<b>How many distinct items?</b>", "<b>~2% error in a few kilobytes</b>"],
     ["<b>Misra-Gries</b>", "<b>Which items are frequent?</b>", "<b>Finds all above a threshold; some extras</b>"],
   ],
   "footnote": "<b>'Never underestimates' is Count-Min's key "
               "property</b> — the error is one-sided, which makes "
               "it safe for threshold tests where a miss is worse than a "
               "false alarm.",
   "note": "The one-sidedness is what makes Count-Min usable in "
           "practice."},

  {"t": "callout", "title": "Count-Min works by taking the minimum over several independent hashes",
   "kind": "The mechanism, which explains the guarantee",
   "body": ["<b>Keep d rows of w counters. On each item, increment "
            "one counter per row, chosen by that row's hash.</b> <b>To "
            "query, take the minimum of the d counters.</b>",
            "<b>Each counter is at least the true count</b>, because "
            "collisions only add — <b>so every estimate is an "
            "overestimate, and the minimum is the tightest "
            "one.</b>",
            "<b>And the error is bounded by the total count over "
            "w</b>, with probability depending on d — so <b>width "
            "controls accuracy and depth controls "
            "confidence.</b>",
            "<b>Which means the heavy hitters are estimated "
            "accurately and the tail is not</b> — <b>the error is "
            "absolute rather than relative</b>, so a rare item's "
            "estimate can be wrong by a large multiple."]},

  {"t": "section", "label": "Part 4", "title": "Verifying",
   "blurb": "Because the bounds assume things."},

  {"t": "bullets", "kicker": "Verification", "title": "What to check on your own data",
   "items": [
     "<b>Measure the actual error against the exact answer</b> on "
     "a sample you can compute exactly — which is the whole "
     "verification, and it is cheap.",
     "",
     "<b>Compare it to the stated bound</b>, and <b>investigate if "
     "the observed error is <i>better</i> than the bound</b> too "
     "— which usually means the bound was loose and sometimes "
     "means a measurement error.",
     "",
     "<b>Check the hash independence</b>, because <b>the "
     "guarantees assume pairwise or k-wise independent hashes</b> and a "
     "fast non-cryptographic hash may not deliver it.",
     "",
     "<b>Check the tail specifically</b> — the error on rare "
     "items is where Count-Min's absolute bound hurts, and the average "
     "error hides it.",
     "",
     "<b>And measure the memory you actually used</b>, since the "
     "point of the exercise was the space.",
   ],
   "footnote": "<b>Checking the tail separately is the step that "
               "matters</b> — an aggregate error figure is dominated "
               "by the frequent items, which are the ones the sketch gets "
               "right."},

  {"t": "callout", "title": "And what streaming cannot do",
   "kind": "Closing",
   "body": ["<b>Exact distinct counts, exact medians, and exact "
            "quantiles all require memory linear in the "
            "distinct count</b> — these are proved lower bounds "
            "rather than missing algorithms.",
            "<b>Anything needing a second look at an earlier "
            "item</b> — so joins, sorting, and any iterative "
            "algorithm are out of the pure model.",
            "<b>And sliding windows are substantially harder than "
            "prefixes</b>, because expiry requires knowing what to "
            "forget, which the sketches above cannot do.",
            "<b>So the honest framing is:</b> <b>streaming gives you "
            "approximate answers to a specific set of questions in "
            "exchange for one pass</b> — and <b>knowing which "
            "questions is the content of the module.</b>"]},
 ],
 "takeaways": [
   "Streaming forces a trade between memory, accuracy, and failure "
   "probability, and stating all three is what makes it a result.",
   "Reservoir sampling's acceptance probability falls exactly as fast as "
   "the survival probability accumulates, which is why the telescoping "
   "product gives 1/n.",
   "Count-Min never underestimates, which makes its one-sided error safe "
   "for threshold tests.",
   "Count-Min's error is absolute rather than relative, so heavy hitters "
   "are accurate and the tail is not.",
   "Verify the bound on your own data, and check the tail separately "
   "because the aggregate error is dominated by frequent items.",
   "Exact distinct counts and exact quantiles require linear memory by "
   "proved lower bounds, not by missing algorithms.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The model"),
  ("callout", "One pass, memory sublinear in the stream length, and an "
              "answer with a stated error",
   ["<b>The stream is unbounded or simply too large to store</b>, each "
    "item is seen exactly once, and the memory available is "
    "polylogarithmic in the stream length — <b>which rules out "
    "storing the data and therefore rules out exact answers to most "
    "questions</b> (&sect;4's lower bounds).",
    "<b>So every streaming result is a trade between memory, accuracy, "
    "and failure probability</b> — and <b>stating all three is what "
    "makes it a result rather than a heuristic</b>, which is "
    "Module 01 &sect;2's discipline applied to this setting.",
    "<b>And this is the realistic model considerably more often than "
    "it appears:</b> log processing, network flow monitoring, click "
    "streams, and sensor data all have this shape, <b>and so does any "
    "dataset larger than memory being read sequentially</b> — which "
    "is most of this course's data.",
    "<b>Which is Module 01 &sect;2's cost model taken to its "
    "limit</b> — <b>one pass is the minimum possible, and several of "
    "these algorithms achieve it</b> while answering questions that look "
    "like they should need the whole dataset."]),

  ("h1", "2 &nbsp; Sampling"),
  ("code", """KEEP k ITEMS. For the i-th item (i > k):
    with probability k/i, replace a uniformly chosen
    one of the k held items with it.

THE CLAIM
    after n items, every item has probability k/n of
    being in the reservoir -- and this holds at every
    n, without ever knowing n in advance.

WHY (sketch, for k = 1)
    item i is kept at step i with probability 1/i, and
    survives each later step j with probability
    (j-1)/j. The product telescopes:
        (1/i) * (i/(i+1)) * ... * ((n-1)/n) = 1/n

WHICH IS THE WHOLE TRICK: the acceptance probability
falls exactly as fast as the survival probability
accumulates.

AND FOR WEIGHTED OR SLIDING-WINDOW SAMPLING the
construction changes; do not assume this version
generalises."""),
  ("p", "<b>The telescoping product is the proof</b>, and <b>it is "
        "worth writing out once</b> — <b>it explains why the k/i "
        "acceptance probability is exactly right rather than approximately "
        "right</b>, and it makes the algorithm memorable rather than "
        "magical. <b>The not-knowing-n property is what makes it useful "
        "in a stream</b>: a sample drawn with a fixed probability requires "
        "knowing the length, and this does not."),

  ("break",),
  ("h1", "3 &nbsp; Counting sketches"),
  ("table", ["Sketch", "What it answers", "The guarantee"],
   [["<b>Bloom filter</b>", "<b>Is x in the set?</b>",
     "<b>No false negatives, and a tunable false positive rate</b> "
     "— the asymmetry is the design."],
    ["<b>Count-Min</b>", "<b>How often did x occur?</b>",
     "<b>Never underestimates; a bounded overestimate</b> — see the "
     "callout."],
    ["<b>Count-Sketch</b>", "<b>The same question.</b>",
     "<b>Unbiased, with a variance bound</b> — the error can go "
     "either way, which suits different uses."],
    ["<b>HyperLogLog</b>", "<b>How many distinct items were there?</b>",
     "<b>About 2% relative error in a few kilobytes</b>, regardless of "
     "the cardinality — which is remarkable."],
    ["<b>Misra-Gries</b>", "<b>Which items are frequent?</b>",
     "<b>Finds every item above a frequency threshold, plus some "
     "extras</b> — so it is a candidate generator."]],
   [0.20, 0.30, 0.50]),
  ("p", "<b>'Never underestimates' is Count-Min's key property</b>, and "
        "it is worth dwelling on: <b>the error is one-sided, which makes "
        "the sketch safe for threshold tests where a miss would be worse "
        "than a false alarm</b> — if the estimate is below the "
        "threshold, the true count certainly is too. <b>That one-sidedness "
        "is what makes it usable in practice</b> for tasks like rate "
        "limiting and heavy-hitter detection."),
  ("callout", "Count-Min works by taking the minimum over several "
              "independent hashes",
   ["<b>Keep d rows of w counters each. On each arriving item, "
    "increment one counter per row, selected by that row's hash of the "
    "item.</b> <b>To query a count, take the minimum of the d counters "
    "the item hashes to.</b>",
    "<b>Each individual counter is at least the item's true count</b>, "
    "because collisions can only add to it and never subtract — "
    "<b>so every one of the d estimates is an overestimate, and the "
    "minimum is simply the tightest of them.</b> That is the whole "
    "argument for the one-sided guarantee.",
    "<b>And the error is bounded by the stream's total count divided "
    "by w</b>, with a failure probability that falls exponentially in "
    "d — so <b>the width controls the accuracy and the depth "
    "controls the confidence</b>, which are two separate dials.",
    "<b>Which means the heavy hitters are estimated accurately and the "
    "tail is not</b> — <b>the error is <i>absolute</i> rather than "
    "relative</b>, so <b>a rare item's estimate can be wrong by a large "
    "multiple</b> while the absolute error is within bound. This is "
    "&sect;4's tail check and is the practical limitation of the "
    "structure."]),

  ("h1", "4 &nbsp; Verifying, and what streaming cannot do"),
  ("ul", ["<b>Measure the actual error against the exact answer</b> on "
          "a sample small enough to compute exactly — <b>which is the "
          "whole verification, and it is cheap</b>, and it is "
          "Module 01 &sect;2's discipline in practice.",
          "<b>Compare the measured error to the stated bound</b>, and "
          "<b>investigate if the observed error is <i>better</i> than the "
          "bound as well</b> — which <b>usually means the bound was "
          "loose for your data and occasionally means you measured the "
          "wrong thing.</b>",
          "<b>Check the hash independence</b>, because <b>the "
          "guarantees assume pairwise or k-wise independent hash "
          "functions</b> and a fast non-cryptographic hash chosen for "
          "speed may not deliver it — which shows up as correlated "
          "collisions rather than as an obvious failure "
          "(Module 02 &sect;4's same warning).",
          "<b>Check the tail specifically</b> — the error on rare "
          "items is exactly where Count-Min's absolute bound hurts, and "
          "<b>an aggregate error figure is dominated by the frequent "
          "items, which are the ones the sketch gets right.</b> <b>This "
          "is the step that matters.</b>",
          "<b>And measure the memory you actually used</b>, since "
          "<b>the space was the entire point of the exercise</b> — a "
          "sketch using more memory than the exact structure would have is "
          "a result worth discovering in testing."]),
  ("callout", "And what streaming cannot do",
   ["<b>Exact distinct counts, exact medians, and exact quantiles all "
    "require memory linear in the number of distinct items</b> — and "
    "<b>these are proved lower bounds rather than missing "
    "algorithms</b>, which is worth knowing so you stop looking.",
    "<b>Anything that needs a second look at an earlier item</b> "
    "— so <b>joins, sorting, and any iterative algorithm are outside "
    "the pure streaming model</b>, and the practical systems of "
    "Module 10 exist partly to relax the one-pass constraint.",
    "<b>And sliding windows are substantially harder than "
    "prefixes</b>, because <b>expiry requires knowing what to forget</b>, "
    "which none of &sect;3's sketches can do — they accumulate "
    "monotonically. Windowed variants exist and cost more.",
    "<b>So the honest framing is:</b> <b>streaming gives you "
    "approximate answers to a specific and limited set of questions, in "
    "exchange for a single pass</b> — and <b>knowing which questions "
    "are on that list is the content of this module</b>, more than the "
    "individual algorithms are."]),
 ],
 "resources": [
   ("Mining of Massive Datasets, chapter 4 (free)",
    "http://www.mmds.org/",
    "<b>The whole module</b> — the streaming model, the sketches, and "
    "the sampling, with the analyses."),
   ("Cormode & Muthukrishnan &mdash; An improved data stream summary "
    "(free)",
    "https://web.archive.org/web/20260709152436/http://dimacs.rutgers.edu/~graham/pubs/papers/cm-full.pdf",
    "<b>&sect;3's Count-Min in the original</b>, with the bound derived "
    "— short and readable."),
   ("Flajolet et al. &mdash; HyperLogLog (free)",
    "http://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf",
    "<b>&sect;3's fourth row</b> — and the analysis is a genuinely "
    "elegant piece of work."),
   ("Cormode & Yi &mdash; Small Summaries for Big Data",
    "https://www.cambridge.org/core/books/small-summaries-for-big-data/",
    "<b>&sect;3 and &sect;4 comprehensively</b> — including the lower "
    "bounds and the windowed variants. Library copy."),
 ],
 "exercises": [
   "<b>Implement reservoir sampling</b> and verify uniformity "
   "empirically over many runs.",
   "<b>Write out the telescoping product</b> for k = 1.",
   "<b>Implement a Bloom filter</b> and measure the false positive rate "
   "against its prediction.",
   "<b>Implement Count-Min</b> and verify it never underestimates.",
   "<b>Measure its error for frequent and rare items separately.</b>",
   "<b>Vary the width and the depth</b> and confirm which controls "
   "accuracy and which confidence.",
   "<b>Implement HyperLogLog</b> and measure the relative error at three "
   "cardinalities.",
   "<b>Replace the hash with a deliberately poor one</b> and report what "
   "happens to the bounds.",
   "<b>Measure the memory used</b> against the exact structure.",
   "<b>Try to compute an exact median in one pass</b> and explain why "
   "you cannot.",
 ],
 "selfcheck": [
   "State the streaming model's three constraints.",
   "Why is every streaming result a three-way trade?",
   "Give reservoir sampling and the claim it satisfies.",
   "Explain why the telescoping product gives 1/n.",
   "Name five sketches and what each answers.",
   "What is Count-Min's key property, and why does it matter?",
   "Explain the mechanism and what width and depth each control.",
   "Why is the tail inaccurate?",
   "Give five verification steps and the one that matters most.",
   "Name three things streaming cannot do.",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Graph Mining",
 "subtitle": "Structure in relationships.",
 "question": "Who is central, and who belongs together?",
 "outcomes": [
     "Explain the properties real networks have.",
     "Explain centrality measures and what each means.",
     "Explain PageRank and its interpretation.",
     "Explain community detection and modularity's limits.",
     "Compute these at scale.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What real graphs look like",
   "blurb": "Which constrains every algorithm."},

  {"t": "bullets", "kicker": "Properties", "title": "The properties, and their consequences",
   "items": [
     "<b>Heavy-tailed degree distributions.</b> <b>A few nodes "
     "have enormous degree</b> — which breaks algorithms assuming "
     "bounded degree and dominates every average you "
     "compute.",
     "",
     "<b>Short paths.</b> <b>Diameter grows like log n or "
     "slower</b>, so a breadth-first search reaches everything in a few "
     "levels and the frontier explodes.",
     "",
     "<b>High clustering.</b> <b>Neighbours of a node are "
     "connected to each other far more than chance</b> — which is "
     "what makes communities exist at all.",
     "",
     "<b>Sparsity.</b> <b>The average degree is small even when n "
     "is huge</b>, so an adjacency matrix is unthinkable and an "
     "adjacency list is fine.",
     "",
     "<b>And the heavy tail is the one that breaks "
     "things</b> — <b>it causes load imbalance in every "
     "partitioning scheme</b> (Module 10).",
   ],
   "footnote": "<b>The heavy tail's consequence for distributed "
               "processing is the practical point:</b> partitioning a "
               "graph by node gives one machine the hub and the rest "
               "nothing to do."},

  {"t": "section", "label": "Part 2", "title": "Centrality",
   "blurb": "Four measures answering four different questions."},

  {"t": "table", "kicker": "Centrality", "title": "What each measure means",
   "header": ["Measure", "Means", "Use when"],
   "widths": [2.6, 4.2, 5.0],
   "rows": [
     ["<b>Degree</b>", "<b>Many direct connections</b>", "<b>Immediate influence matters; it is O(1)</b>"],
     ["<b>Betweenness</b>", "<b>On many shortest paths</b>", "<b>Flow and brokerage matter; it is expensive</b>"],
     ["<b>Closeness</b>", "<b>Short paths to everyone</b>", "<b>Reach matters; needs a connected graph</b>"],
     ["<b>Eigenvector / PageRank</b>", "<b>Connected to well-connected nodes</b>", "<b>Recursive importance; and it scales</b>"],
   ],
   "footnote": "<b>These disagree, and the disagreement is "
               "informative</b> — a node with high betweenness and "
               "low degree is a bridge, which is a different role from a "
               "hub.",
   "note": "The disagreement-is-informative framing beats arguing "
           "which is best."},

  {"t": "eq", "kicker": "PageRank", "title": "The definition, and how to read it",
   "eqs": [
     ("r = d Mᵀ r + (1−d)/n · 1",
      "A node's rank is the damped sum of ranks flowing in, plus a "
      "uniform teleport term."),
     ("interpretation: a random surfer's stationary distribution",
      "Follow a random link with probability d; jump to a random "
      "page with probability 1−d."),
     ("computed by power iteration",
      "Repeated multiplication converges; the teleport term is what "
      "guarantees it does."),
   ],
   "caption": "<b>The teleport term is not a hack</b> — it makes "
              "the chain irreducible and aperiodic, which is what "
              "guarantees a unique stationary distribution.",
   "note": "Explaining the teleport term mathematically prevents it "
           "looking arbitrary."},

  {"t": "section", "label": "Part 3", "title": "Communities",
   "blurb": "And modularity's specific failure."},

  {"t": "callout", "title": "Modularity compares edge density within groups against a random baseline",
   "kind": "The measure, and the problem with maximising it",
   "body": ["<b>It measures how many more edges fall inside the "
            "proposed communities than would in a random graph with the "
            "same degrees</b> — which is a reasonable definition and "
            "is cheap to compute.",
            "<b>And maximising it is the standard approach</b> "
            "— Louvain and Leiden do this greedily and scale to "
            "very large graphs.",
            "<b>But it has a resolution limit:</b> <b>modularity "
            "maximisation cannot find communities below a size that "
            "depends on the <i>total</i> graph size</b> — so small "
            "real communities are merged, and the effect worsens as the "
            "graph grows.",
            "<b>And it finds high-modularity partitions in random "
            "graphs</b> — <b>which is Module 01 §3 "
            "again</b>: a high modularity score is not evidence that "
            "communities exist, without a null comparison."]},

  {"t": "bullets", "kicker": "Community", "title": "The approaches, and how to assess the result",
   "items": [
     "<b>Louvain and Leiden</b> — greedy modularity, fast, "
     "and the practical default. <b>Leiden fixes a connectivity defect "
     "in Louvain's output</b>, so prefer it.",
     "",
     "<b>Label propagation</b> — near-linear, and "
     "unstable across runs, which is itself informative "
     "(Module 04 §3).",
     "",
     "<b>Spectral methods</b> — principled, connected to "
     "graph cuts, and limited by the eigenvector "
     "computation.",
     "",
     "<b>Overlapping methods</b>, because <b>real community "
     "membership is not a partition</b> — people belong to "
     "several.",
     "",
     "<b>And assess by stability and a null comparison</b>, not "
     "by the modularity score alone.",
   ],
   "footnote": "<b>'Real membership is not a partition' is worth "
               "stating</b> — most algorithms return one anyway, "
               "which is a modelling assumption rather than a "
               "finding."},

  {"t": "section", "label": "Part 4", "title": "At scale",
   "blurb": "Where graph algorithms get difficult."},

  {"t": "code", "kicker": "Scale", "title": "What changes on a large graph",
   "lang": "text", "code": """
  WHAT WORKS
      anything expressible as repeated local updates:
      PageRank, label propagation, connected
      components, single-source shortest paths.
      Pregel's "think like a vertex" model fits
      these, and so does sparse matrix multiply.

  WHAT DOES NOT
      betweenness centrality -- all-pairs shortest
          paths, so it is approximated by sampling
          source nodes instead
      exact triangle counting -- approximated
      anything needing the full adjacency matrix

  AND THE REAL PROBLEM IS PARTITIONING
      cutting a heavy-tailed graph across machines
      puts the hub somewhere, and that machine does
      most of the work. Edge-cut partitioning
      balances poorly; vertex-cut partitioning
      splits high-degree nodes instead, which is
      what the systems do.

  SO: communication dominates, not computation.
""",
   "caption": "<b>Communication dominates</b> — which is why graph "
              "processing is harder to distribute than most data "
              "parallel work (CSCE 678).",
   "note": "The vertex-cut answer to the heavy tail is the key "
           "systems insight."},

  {"t": "callout", "title": "And what to report about a graph finding",
   "kind": "Closing",
   "body": ["<b>How the graph was constructed</b> — <b>which "
            "edges you included is a modelling decision that determines "
            "every result</b>, and it is frequently unstated.",
            "<b>Which centrality you used, and why that "
            "question</b> — since the four measures disagree "
            "(Part 2).",
            "<b>The null comparison for any community "
            "finding</b> — <b>what a degree-preserving random graph "
            "scores</b>, which is the only way to read a modularity "
            "value.",
            "<b>And the stability across runs and subsamples</b>, "
            "because <b>several of these algorithms are "
            "non-deterministic</b> and the variation is the "
            "result."]},
 ],
 "takeaways": [
   "The heavy-tailed degree distribution is the property that breaks "
   "things, because it causes load imbalance in every partitioning scheme.",
   "The four centrality measures disagree, and the disagreement is "
   "informative — a bridge is a different role from a hub.",
   "PageRank's teleport term makes the chain irreducible and aperiodic, "
   "which is what guarantees a unique stationary distribution.",
   "Modularity has a resolution limit that depends on total graph size, so "
   "small real communities are merged and it worsens with scale.",
   "Modularity maximisation finds high-scoring partitions in random "
   "graphs, so the score is not evidence communities exist.",
   "At scale, communication dominates computation, and vertex-cut "
   "partitioning is the answer to the heavy tail.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What real graphs look like"),
  ("ul", ["<b>Heavy-tailed degree distributions.</b> <b>A few nodes "
          "have enormous degree while most have very little</b> — "
          "which <b>breaks algorithms that assume bounded degree and "
          "dominates every average you compute</b>, so the mean degree is "
          "a nearly useless summary.",
          "<b>Short paths.</b> <b>The diameter grows like log n or "
          "slower</b>, so a breadth-first search reaches essentially "
          "everything within a few levels — <b>and the frontier "
          "explodes</b>, which makes BFS expensive in memory rather than "
          "in depth.",
          "<b>High clustering.</b> <b>The neighbours of a node are "
          "connected to one another far more often than chance would "
          "predict</b> — which is <b>what makes communities exist at "
          "all</b> (&sect;3) and distinguishes real networks from random "
          "ones.",
          "<b>Sparsity.</b> <b>The average degree stays small even "
          "when n is enormous</b> — so an adjacency matrix is "
          "unthinkable at scale and an adjacency list is entirely "
          "manageable, which determines the representation.",
          "<b>And the heavy tail is the property that breaks "
          "things</b> — <b>it causes load imbalance in every "
          "partitioning scheme</b> (&sect;4, and Module 10). <b>The "
          "practical consequence is immediate:</b> partitioning a graph "
          "by node gives one machine the hub and leaves the others with "
          "very little to do."]),

  ("h1", "2 &nbsp; Centrality"),
  ("table", ["Measure", "What it means", "Use it when"],
   [["<b>Degree</b>", "<b>Many direct connections.</b>",
     "<b>Immediate influence is what matters</b>, and it costs O(1) per "
     "node."],
    ["<b>Betweenness</b>",
     "<b>Lies on many shortest paths between other nodes.</b>",
     "<b>Flow and brokerage matter</b> — and it is expensive "
     "(&sect;4)."],
    ["<b>Closeness</b>", "<b>Short paths to everybody else.</b>",
     "<b>Reach matters</b>; and it needs a connected graph, or a "
     "convention for disconnected pairs."],
    ["<b>Eigenvector and PageRank</b>",
     "<b>Connected to nodes that are themselves well connected.</b>",
     "<b>Recursive importance is the right notion</b> — and it "
     "scales (&sect;4)."]],
   [0.20, 0.32, 0.48]),
  ("p", "<b>These measures disagree, and the disagreement is "
        "informative rather than a problem to be resolved</b> — <b>a "
        "node with high betweenness and low degree is a bridge</b> "
        "connecting two otherwise separate regions, <b>which is a "
        "genuinely different structural role from a hub</b> with high "
        "degree and low betweenness. <b>That framing beats arguing about "
        "which measure is best</b>, which is not a well-posed question "
        "without saying what you want to know."),
  ("eq", "r = d M<sup>T</sup> r + ((1&minus;d)/n) &middot; 1"),
  ("ul", ["<b>A node's rank is the damped sum of the ranks flowing "
          "into it</b>, plus a uniform teleport term distributed over all "
          "nodes.",
          "<b>The interpretation is a random surfer's stationary "
          "distribution:</b> follow a random outgoing link with "
          "probability d, and jump to a uniformly random page with "
          "probability 1&minus;d — which makes the quantity "
          "interpretable rather than merely computable.",
          "<b>It is computed by power iteration</b> — repeated "
          "multiplication by the transition matrix, which converges, and "
          "which is the sort of repeated local update that distributes "
          "well (&sect;4).",
          "<b>And the teleport term is not a hack.</b> <b>It makes "
          "the Markov chain irreducible and aperiodic, which is exactly "
          "what guarantees a unique stationary distribution</b> that the "
          "iteration converges to — without it, dangling nodes and "
          "disconnected components break the whole thing. <b>Explaining "
          "it mathematically prevents it from looking arbitrary</b>, "
          "which it does in most presentations."]),

  ("break",),
  ("h1", "3 &nbsp; Communities"),
  ("callout", "Modularity compares edge density within groups against a "
              "random baseline",
   ["<b>It measures how many more edges fall inside the proposed "
    "communities than would be expected in a random graph with the same "
    "degree sequence</b> — which is a reasonable definition of "
    "community structure and is cheap to compute for a given "
    "partition.",
    "<b>And maximising it is the standard approach</b> — the "
    "Louvain and Leiden algorithms do this greedily and scale to graphs "
    "with billions of edges, which is why they are the practical "
    "default.",
    "<b>But it has a resolution limit:</b> <b>modularity maximisation "
    "cannot find communities below a size that depends on the <i>total</i> "
    "number of edges in the graph</b> — so <b>small but genuine "
    "communities get merged into larger ones, and the effect gets worse "
    "as the graph grows</b>, which is a bad property for a method used at "
    "scale.",
    "<b>And it finds high-modularity partitions in random "
    "graphs</b> — <b>which is Module 01 &sect;3 "
    "again</b>: <b>a high modularity score is not evidence that "
    "communities exist</b>, without a comparison against a "
    "degree-preserving null model (&sect;4's reporting "
    "requirement)."]),
  ("ul", ["<b>Louvain and Leiden</b> — greedy modularity "
          "optimisation, fast, and the practical default. <b>Leiden fixes "
          "a defect in Louvain by which the returned communities can be "
          "internally disconnected</b>, so prefer it.",
          "<b>Label propagation</b> — near-linear time, and "
          "<b>unstable across runs, which is itself informative</b> about "
          "whether the structure is real (Module 04 &sect;3's "
          "stability argument).",
          "<b>Spectral methods</b> — principled, directly "
          "connected to graph cut objectives, and limited in practice by "
          "the cost of the eigenvector computation (Module 05 "
          "&sect;2).",
          "<b>Overlapping community methods</b>, because <b>real "
          "community membership is not a partition</b> — people "
          "belong to several communities at once, and most algorithms "
          "return a partition anyway.",
          "<b>And assess the result by stability and by a null "
          "comparison</b>, not by the modularity score alone. <b>'Real "
          "membership is not a partition' is worth stating "
          "explicitly</b>, because <b>returning one is a modelling "
          "assumption rather than a finding</b> and is rarely flagged as "
          "such."]),

  ("h1", "4 &nbsp; At scale"),
  ("code", """WHAT WORKS
    anything expressible as repeated local updates:
    PageRank, label propagation, connected components,
    single-source shortest paths. Pregel's "think like
    a vertex" model fits these exactly, and so does
    sparse matrix multiplication.

WHAT DOES NOT
    betweenness centrality -- it needs all-pairs
        shortest paths, so it is approximated by
        sampling source nodes instead
    exact triangle counting -- approximated, usually
        by sampling or by a sketch
    anything needing the full adjacency matrix

AND THE REAL PROBLEM IS PARTITIONING
    cutting a heavy-tailed graph across machines puts
    the hub somewhere, and that machine then does most
    of the work. Edge-cut partitioning balances
    poorly; vertex-cut partitioning splits
    high-degree nodes across machines instead, which
    is what the real systems do.

SO: communication dominates, not computation."""),
  ("p", "<b>Communication dominates rather than computation</b> — "
        "<b>which is why graph processing is substantially harder to "
        "distribute than most data-parallel work</b> (CSCE 678 "
        "Module 11), where the partitions are independent. <b>The "
        "vertex-cut answer to the heavy tail is the key systems "
        "insight</b>: rather than trying to find a balanced edge cut in a "
        "graph where no balanced cut exists, split the problematic "
        "high-degree vertices themselves and reconcile their state."),
  ("callout", "And what to report about a graph finding",
   ["<b>How the graph was constructed</b> — <b>which edges you "
    "included is a modelling decision that determines every subsequent "
    "result</b>, and <b>it is frequently left unstated</b>. A "
    "co-authorship graph with and without single-author papers, or a "
    "social graph with and without reciprocity required, are different "
    "objects.",
    "<b>Which centrality measure you used, and why that was the right "
    "question</b> — since the four measures disagree (&sect;2) and "
    "reporting 'the most central nodes' without saying which measure is "
    "uninterpretable.",
    "<b>The null comparison for any community finding</b> — "
    "<b>what a degree-preserving random graph scores on the same "
    "measure</b>, which is <b>the only way to read a modularity value at "
    "all</b> (&sect;3).",
    "<b>And the stability across runs and across subsamples</b>, "
    "because <b>several of these algorithms are non-deterministic</b> and "
    "<b>the variation is itself the result</b> — a community "
    "structure that changes on every run has told you something, and it "
    "is not what the first run suggested."]),
 ],
 "resources": [
   ("Mining of Massive Datasets, chapters 5 and 10 (free)",
    "http://www.mmds.org/",
    "<b>&sect;2's PageRank and &sect;3's community detection</b>, with the "
    "scale considerations throughout."),
   ("Easley & Kleinberg &mdash; Networks, Crowds, and Markets (free "
    "PDF)",
    "https://www.cs.cornell.edu/home/kleinber/networks-book/",
    "<b>&sect;1 and &sect;2 in their social context</b>, free in full "
    "— and the clearest treatment of why these properties "
    "arise."),
   ("Fortunato & Barth&eacute;lemy &mdash; Resolution limit in "
    "community detection (free)",
    "https://www.pnas.org/doi/10.1073/pnas.0605965104",
    "<b>&sect;3's limitation, proved</b> — short, and it should be "
    "read by anybody using modularity."),
   ("Malewicz et al. &mdash; Pregel (free)",
    "https://dl.acm.org/doi/10.1145/1807167.1807184",
    "<b>&sect;4's programming model</b> — think-like-a-vertex, and "
    "why it fits this class of algorithm."),
 ],
 "exercises": [
   "<b>Plot the degree distribution</b> of a real graph on log-log "
   "axes.",
   "<b>Compute the mean and median degree</b> and say why the mean "
   "misleads.",
   "<b>Measure the diameter and the clustering coefficient</b>, and "
   "compare against a random graph with the same degrees.",
   "<b>Compute all four centralities</b> and find a node that is a "
   "bridge rather than a hub.",
   "<b>Implement PageRank by power iteration</b> and watch it "
   "converge.",
   "<b>Set the teleport term to zero</b> and report what breaks.",
   "<b>Run Louvain and Leiden</b> and compare the partitions.",
   "<b>Run community detection on a degree-preserving random "
   "graph</b> and report the modularity it achieves.",
   "<b>Run label propagation five times</b> and quantify the "
   "instability.",
   "<b>Partition a heavy-tailed graph by edge cut</b> and measure the "
   "load imbalance.",
 ],
 "selfcheck": [
   "Name four properties of real graphs and the consequence of each.",
   "Which property breaks things, and how?",
   "Name four centrality measures and what each means.",
   "Why is their disagreement informative?",
   "Give the PageRank equation and its random-surfer reading.",
   "Why is the teleport term necessary mathematically?",
   "What does modularity measure, and what is its resolution limit?",
   "Why is a high modularity score not evidence of communities?",
   "What kinds of graph algorithm distribute well, and which do not?",
   "Why does vertex-cut partitioning help?",
 ],
},

]
