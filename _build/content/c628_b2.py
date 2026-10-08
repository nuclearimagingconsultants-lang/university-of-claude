# -*- coding: utf-8 -*-
"""CSCE 628 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Sequence Alignment",
 "subtitle": "Dynamic programming at its clearest.",
 "question": "How similar are two strings, and where?",
 "outcomes": [
     "Derive the global alignment recurrence.",
     "Derive local alignment and say when to use it.",
     "Explain affine gap penalties and implement them.",
     "Explain the space and time trade-offs.",
     "Implement and verify an alignment engine.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Global alignment",
   "blurb": "The recurrence, and what each term means biologically."},

  {"t": "eq", "kicker": "Needleman-Wunsch", "title": "The recurrence",
   "eqs": [
     ("F(i,j) = max of three terms, over prefixes of length i and j",
      "The best score for aligning the first i characters of one "
      "sequence with the first j of the other."),
     ("F(i−1,j−1) + s(xᵢ, yⱼ)   — align the two characters",
      "A match or a mismatch, scored by the substitution function s "
      "(Module 03 §1)."),
     ("F(i−1,j) + g   or   F(i,j−1) + g   — a gap in one sequence",
      "An insertion or a deletion, with gap penalty g. Three cases, "
      "one max, O(mn) time and O(mn) space with traceback."),
   ],
   "caption": "<b>Three cases, one max</b> — and the traceback "
              "pointer recovers the alignment itself rather than just "
              "the score.",
   "note": "This is the recurrence to be able to write from memory."},

  {"t": "callout", "title": "And each term corresponds to an evolutionary event, which is why the model is credible",
   "kind": "Why alignment scores mean anything at all",
   "body": ["<b>A match or mismatch is a position that was "
            "conserved or substituted</b>; <b>a gap is an insertion or "
            "a deletion</b> — so <b>the alignment is a hypothesis "
            "about what happened.</b>",
            "<b>Which means the scoring parameters are a model of "
            "evolution</b>, not arbitrary constants — <b>and "
            "Module 03 §1 derives them from observed substitution "
            "frequencies.</b>",
            "<b>And the optimal alignment is the most likely history "
            "under that model</b> — <b>not the true history</b>, "
            "which is unavailable (Module 01 §4).",
            "<b>So the thing to remember is: alignment is inference "
            "under a model</b> — <b>and the model's assumptions are "
            "where the disagreements between tools come "
            "from.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Local alignment",
   "blurb": "One change to the recurrence, and a different question."},

  {"t": "callout", "title": "Smith-Waterman adds zero to the max, which lets an alignment start anywhere",
   "kind": "The change, and why it matters more than it looks",
   "body": ["<b>Add 0 as a fourth case</b> — so a negative running "
            "score resets rather than persisting — <b>and start the "
            "traceback from the maximum cell rather than the "
            "corner.</b>",
            "<b>Which finds the best-matching <i>region</i> rather "
            "than the best whole-sequence correspondence</b> — "
            "<b>and that is almost always the biologically relevant "
            "question</b>, because conservation is domain-wise rather "
            "than whole-sequence.",
            "<b>So: global for sequences you believe are related "
            "along their whole length, local "
            "otherwise</b> — <b>and local is the default</b>, "
            "including for database search "
            "(Module 04).",
            "<b>And the scoring must allow negative "
            "scores</b> — <b>a matrix where every entry is positive "
            "makes local alignment degenerate into global</b>, which is "
            "a real implementation trap."]},

  {"t": "section", "label": "Part 3", "title": "Gaps",
   "blurb": "Where the simple model is clearly wrong."},

  {"t": "eq", "kicker": "Affine gaps", "title": "Why one gap of ten beats ten gaps of one",
   "eqs": [
     ("linear: cost of a gap of length k is k·g",
      "Simple, and biologically wrong: a single indel event of "
      "length 10 is far more likely than 10 separate events."),
     ("affine: cost is open + k·extend,  with open ≫ extend",
      "One expensive opening and cheap extension. This matches "
      "what is observed, and is what every real tool uses."),
     ("three matrices: M, I_x, I_y  — one per state",
      "Match state, gap-in-x state, gap-in-y state. Still O(mn), "
      "with three recurrences instead of one. Gotoh's algorithm."),
   ],
   "caption": "<b>Three state matrices, still O(mn)</b> — and "
              "the affine recurrence is where hand implementations "
              "usually break (Project 1).",
   "note": "The three-state formulation is the one to implement."},

  {"t": "section", "label": "Part 4", "title": "Space",
   "blurb": "And the trick that removes the quadratic memory."},

  {"t": "bullets", "kicker": "Engineering", "title": "The practical considerations",
   "items": [
     "<b>The score alone needs only two rows</b> — <b>O(min(m,n)) "
     "space</b> — because each cell depends only on the previous "
     "row and the current one.",
     "",
     "<b>But the traceback needs the whole matrix</b>, which is "
     "the quadratic cost — <b>and for two human chromosomes that "
     "is not available.</b>",
     "",
     "<b>Hirschberg's divide-and-conquer recovers the alignment "
     "in linear space</b> — <b>by finding the midpoint crossing "
     "with two linear-space passes and recursing</b> — <b>at "
     "twice the time.</b>",
     "",
     "<b>And banded alignment restricts to a diagonal "
     "band</b> — <b>correct only if the true alignment stays "
     "inside the band</b>, which is an assumption to "
     "state.",
     "",
     "<b>Which is the pattern:</b> <b>exact is quadratic, and "
     "everything faster assumes something</b> "
     "(Module 04).",
   ],
   "footnote": "<b>Exact alignment is quadratic, and everything "
               "faster assumes something</b> — which is the sentence "
               "that organises Modules 02 through "
               "05."},

  {"t": "callout", "title": "And the thing to carry forward",
   "kind": "Closing",
   "body": ["<b>This recurrence is the most reused idea in the "
            "field</b> — <b>Modules 07 and 08 are the same dynamic "
            "programming on richer state spaces</b>, and recognising "
            "that is most of the work.",
            "<b>Viterbi is alignment with probabilities instead of "
            "scores</b> (Module 07 §2) — <b>and the "
            "max-of-three structure is identical.</b>",
            "<b>And RNA folding is the same idea on "
            "intervals</b> (Module 08 §2) — <b>with a "
            "different decomposition and the same "
            "discipline.</b>",
            "<b>So implement this one carefully</b>, because "
            "<b>three later modules are variations on it</b> and the "
            "debugging habits transfer entirely."]},
 ],
 "takeaways": [
   "Three cases, one max — and the traceback pointer recovers the "
   "alignment rather than just the score.",
   "Each term corresponds to an evolutionary event, so the scoring "
   "parameters are a model rather than arbitrary constants.",
   "The optimal alignment is the most likely history under the model, not "
   "the true history.",
   "Smith-Waterman adds zero to the max and starts traceback from the "
   "maximum cell, which finds the best region.",
   "Affine gaps need three state matrices and are where hand "
   "implementations usually break.",
   "Exact alignment is quadratic, and everything faster assumes something.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Global alignment"),
  ("eq", "F(i,j) = max { F(i&minus;1,j&minus;1) + s(x<sub>i</sub>, "
         "y<sub>j</sub>),&nbsp; F(i&minus;1,j) + g,&nbsp; "
         "F(i,j&minus;1) + g }"),
  ("ul", ["<b>F(i,j) is the best score for aligning the first i "
          "characters of x with the first j of y</b> — which is the "
          "subproblem definition, and <b>stating it precisely is most of "
          "the derivation</b> (CSCE 629 Module 05's "
          "discipline).",
          "<b>The first term aligns the two characters</b> — a "
          "match or a mismatch, <b>scored by the substitution function "
          "s</b>, which Module 03 &sect;1 derives from observed "
          "data rather than choosing.",
          "<b>The second and third insert a gap in one sequence or "
          "the other</b> — <b>an insertion or a deletion, with "
          "penalty g</b> — and which of those it is depends on "
          "which sequence you call ancestral, which you usually "
          "cannot.",
          "<b>Three cases, one max</b>, <b>O(mn) time and O(mn) "
          "space with traceback</b> — and <b>the traceback pointer "
          "recovers the alignment itself rather than just the "
          "score</b>, which is the output anybody actually wants. "
          "<b>This is the recurrence to be able to write from "
          "memory</b>, because three later modules are variations on "
          "it."]),
  ("callout", "And each term corresponds to an evolutionary event, which is "
              "why the model is credible",
   ["<b>A match or mismatch is a position that was conserved or "
    "substituted</b>; <b>a gap is an insertion or a deletion</b> — "
    "so <b>the alignment is a hypothesis about what happened between "
    "the two sequences and their common ancestor.</b>",
    "<b>Which means the scoring parameters are a model of molecular "
    "evolution rather than arbitrary constants</b> — and "
    "<b>Module 03 &sect;1 derives them from observed substitution "
    "frequencies in curated alignments</b>, which is what makes the "
    "whole scheme more than a heuristic.",
    "<b>And the optimal alignment is the most likely history under "
    "that model</b> — <b>not the true history</b>, <b>which is "
    "unavailable</b> and in most cases unknowable (Module 01 "
    "&sect;4's no-ground-truth problem, in its first concrete "
    "instance).",
    "<b>So the thing to remember is: alignment is inference under a "
    "model</b> — and <b>the model's assumptions are exactly where "
    "the disagreements between different tools come from</b>, which is "
    "why Project 1 asks you to align the same pair under two "
    "substitution matrices and report the difference."]),

  ("h1", "2 &nbsp; Local alignment"),
  ("callout", "Smith-Waterman adds zero to the max, which lets an alignment "
              "start anywhere",
   ["<b>Add 0 as a fourth case in the max</b> — so a negative "
    "running score resets to zero rather than persisting — <b>and "
    "start the traceback from the maximum cell anywhere in the matrix "
    "rather than from the corner</b>, ending when a zero is "
    "reached.",
    "<b>Which finds the best-matching <i>region</i> rather than the "
    "best whole-sequence correspondence</b> — <b>and that is "
    "almost always the biologically relevant question</b>, because "
    "<b>conservation is domain-wise rather than whole-sequence</b>: two "
    "proteins may share one functional domain and nothing else.",
    "<b>So: global for sequences you believe are related along their "
    "entire length, local otherwise</b> — <b>and local is the "
    "default</b>, <b>including for database search</b> "
    "(Module 04), where you have no reason to think the query "
    "resembles the whole of any database entry.",
    "<b>And the scoring must allow negative scores</b> — "
    "<b>a substitution matrix in which every entry is positive makes "
    "local alignment degenerate into global</b>, since extending is "
    "never penalised — <b>which is a real and easily missed "
    "implementation trap</b>, and is why the expected score of a random "
    "pair must be negative (Module 03 &sect;1)."]),

  ("break",),
  ("h1", "3 &nbsp; Gaps"),
  ("eq", "linear: cost(k) = k&middot;g&nbsp;&nbsp;&nbsp;&nbsp; affine: "
         "cost(k) = open + k&middot;extend,&nbsp; with "
         "|open| &gt;&gt; |extend|"),
  ("ul", ["<b>The linear model is simple and biologically "
          "wrong</b>: <b>a single insertion or deletion event of length "
          "ten is far more likely than ten independent single-base "
          "events</b>, and the linear cost treats them identically.",
          "<b>Affine gives one expensive opening and cheap "
          "extension</b> — <b>which matches what is observed in "
          "curated alignments, and is what every real tool uses</b>, so "
          "an implementation without it will disagree with every "
          "reference.",
          "<b>The implementation needs three matrices</b>: "
          "<b>M (the last pair was aligned), I<sub>x</sub> (a gap in x), "
          "and I<sub>y</sub> (a gap in y)</b> — one per state, each "
          "with its own recurrence over the three predecessors — "
          "<b>which is Gotoh's algorithm, and it is still "
          "O(mn)</b>.",
          "<b>Three state matrices, still O(mn)</b> — and "
          "<b>the affine recurrence is where hand implementations "
          "usually break</b> (Project 1's second requirement), typically "
          "by allowing a transition that opens a gap and immediately "
          "opens another.",
          "<b>The three-state formulation is the one to "
          "implement</b>, rather than the various two-matrix "
          "simplifications, because it is the one whose correctness is "
          "obvious by inspection."]),

  ("h1", "4 &nbsp; Space"),
  ("ul", ["<b>The score alone needs only two rows</b> — "
          "<b>O(min(m,n)) space</b> — because <b>each cell depends "
          "only on the previous row and the current one</b>, which is "
          "the standard dynamic-programming space reduction "
          "(CSCE 629 Module 05).",
          "<b>But the traceback needs the whole matrix</b>, which is "
          "the quadratic memory cost — <b>and for two human "
          "chromosomes that is simply not available</b> on any "
          "machine.",
          "<b>Hirschberg's divide-and-conquer recovers the alignment "
          "in linear space</b> — <b>find where the optimal "
          "alignment crosses the middle column using two linear-space "
          "passes, then recurse on the two halves</b> — <b>at "
          "twice the time</b>, which is a very good trade.",
          "<b>And banded alignment restricts computation to a "
          "diagonal band</b> around the main diagonal — <b>correct "
          "only if the true optimal alignment stays inside the "
          "band</b>, <b>which is an assumption to state</b> rather than "
          "a safe optimisation, though it is usually fine for sequences "
          "of similar length.",
          "<b>Which is the pattern for the next three "
          "modules:</b> <b>exact alignment is quadratic, and everything "
          "faster assumes something</b> (Module 04's heuristics, "
          "Module 05's seeds) — <b>and the assumption is what "
          "should be reported.</b>"]),
  ("callout", "And the thing to carry forward",
   ["<b>This recurrence is the most reused idea in the whole "
    "field</b> — <b>Modules 07 and 08 are the same dynamic "
    "programming on richer state spaces</b>, <b>and recognising that is "
    "most of the work</b> of learning them.",
    "<b>Viterbi is alignment with probabilities instead of "
    "scores</b> (Module 07 &sect;2) — <b>and the max-of-three "
    "structure is identical</b>, with log-probabilities in place of "
    "substitution scores and transitions in place of gap "
    "penalties.",
    "<b>And RNA folding is the same idea on intervals rather than "
    "prefixes</b> (Module 08 &sect;2) — <b>with a different "
    "decomposition and exactly the same discipline</b> of stating the "
    "subproblem before writing the recurrence.",
    "<b>So implement this one carefully</b>, because <b>three later "
    "modules are variations on it</b> <b>and the debugging habits "
    "transfer entirely</b> — particularly the habit of checking "
    "the base cases and the traceback separately from the fill."]),
 ],
 "resources": [
   ("Durbin et al., chapter 2 (library copy)",
    "https://www.cambridge.org/9780521629713",
    "<b>The whole module</b> — alignment developed as probabilistic "
    "inference, which makes &sect;1's callout precise."),
   ("Needleman & Wunsch (1970), and Smith & Waterman (1981)",
    "https://pubmed.ncbi.nlm.nih.gov/5420325/",
    "<b>&sect;&sect;1 and 2 in the originals</b> — short, and the "
    "second is three pages."),
   ("Gotoh &mdash; An improved algorithm for matching biological "
    "sequences",
    "https://pubmed.ncbi.nlm.nih.gov/7166760/",
    "<b>&sect;3's three-state formulation</b> in the original."),
   ("Hirschberg &mdash; A linear space algorithm for computing "
    "maximal common subsequences",
    "https://dl.acm.org/doi/10.1145/360825.360861",
    "<b>&sect;4's divide and conquer</b> — and it predates its "
    "biological application entirely."),
 ],
 "exercises": [
   "<b>Write the global recurrence from memory</b>, with base "
   "cases.",
   "<b>Fill a 5 by 5 matrix by hand</b> and trace back.",
   "<b>Implement Needleman-Wunsch</b> with traceback.",
   "<b>Implement Smith-Waterman</b> and find the best local "
   "region.",
   "<b>Make every matrix entry positive</b> and observe local "
   "alignment degenerate.",
   "<b>Implement affine gaps</b> with three state matrices.",
   "<b>Compare linear and affine</b> on a pair with one long "
   "indel.",
   "<b>Reduce the score computation to two rows.</b>",
   "<b>Implement Hirschberg</b> and compare memory and time.",
   "<b>Band the alignment</b> and find a case where the band makes it "
   "wrong.",
 ],
 "selfcheck": [
   "State the global recurrence and define the subproblem.",
   "What does each of the three terms mean biologically?",
   "What is the optimal alignment, exactly?",
   "What single change gives local alignment, and what else changes?",
   "When is local the right choice, and why is it the default?",
   "Why must some matrix entries be negative?",
   "Why is a linear gap cost wrong?",
   "Describe the three-state affine formulation.",
   "Give the space costs and Hirschberg's trade.",
   "State the sentence that organises Modules 02 to 05.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Scores and Significance",
 "subtitle": "A number is not a finding until it has a null model.",
 "question": "The score is 412. Is that good?",
 "outcomes": [
     "Explain how substitution matrices are derived.",
     "Explain why a score needs a null distribution.",
     "Explain E-values and what they do and do not say.",
     "Explain the effect of database size on significance.",
     "Build an empirical null and use it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Substitution matrices",
   "blurb": "Which are log-odds ratios, and that is the whole idea."},

  {"t": "eq", "kicker": "Scoring", "title": "Where the numbers come from",
   "eqs": [
     ("s(a,b) = log [ p(a,b) / (q(a) · q(b)) ]",
      "The log-odds of seeing a aligned with b under relatedness, "
      "versus under independence. Positive means more likely than "
      "chance; negative means less."),
     ("PAM: estimated from closely related proteins, then extrapolated",
      "A model of evolution over time, with PAM250 being PAM1 "
      "applied 250 times. The extrapolation is the weak part."),
     ("BLOSUM62: counted directly from blocks at ≤62% identity",
      "No extrapolation — counted at the divergence you care "
      "about. Which is why it replaced PAM for most purposes."),
   ],
   "caption": "<b>A substitution score is a log-odds ratio</b>, so "
              "<b>adding scores along an alignment multiplies "
              "likelihood ratios</b> — which is why summing is the "
              "right operation.",
   "note": "The log-odds framing explains why scores are summed and "
           "why some must be negative."},

  {"t": "callout", "title": "And the matrix encodes an assumed divergence, so using the wrong one costs real accuracy",
   "kind": "Why there is more than one matrix",
   "body": ["<b>A matrix tuned for closely related sequences "
            "penalises substitutions heavily</b>; <b>one tuned for "
            "distant relatives tolerates them</b> — and the right "
            "choice depends on what you are looking "
            "for.",
            "<b>So using BLOSUM80 to find remote homologues finds "
            "fewer of them</b>, and <b>using BLOSUM45 for close "
            "matches gives noisier alignments</b> — both of which are "
            "measurable effects rather than preferences.",
            "<b>Which means the matrix is a stated assumption</b>, "
            "and <b>Project 1 asks you to align one pair under two and "
            "report the difference</b>, because the difference is "
            "frequently larger than expected.",
            "<b>And the expected score for a random pair must be "
            "negative</b> — <b>otherwise longer alignments always "
            "score higher</b> and local alignment is "
            "meaningless (Module 02 §2)."]},

  {"t": "section", "label": "Part 2", "title": "The null model",
   "blurb": "Without which a score means nothing."},

  {"t": "callout", "title": "A score is only interpretable against the distribution of scores from unrelated sequences",
   "kind": "The central methodological point of the module",
   "body": ["<b>412 is meaningless alone</b> — <b>the question is "
            "how often a pair of unrelated sequences of these lengths "
            "and compositions scores 412 or better.</b>",
            "<b>And that distribution is computable</b>: <b>for "
            "local alignment, optimal scores follow an extreme value "
            "(Gumbel) distribution</b>, which is where the E-value "
            "formula comes from.",
            "<b>Or it is measurable</b>: <b>shuffle one sequence a "
            "few thousand times, realign, and plot the "
            "scores</b> — which takes minutes and makes no "
            "distributional assumption.",
            "<b>Which is Project 1's requirement, and the habit this "
            "module is for</b> — <b>a score without a null is not "
            "a result</b>, in this field or any "
            "other (CSCE 658 §09)."]},

  {"t": "section", "label": "Part 3", "title": "E-values",
   "blurb": "What the number in a BLAST report actually means."},

  {"t": "code", "kicker": "E-values", "title": "Reading a database search result",
   "lang": "text", "code": """
  E = K · m · n · exp(-lambda · S)

      S     the alignment score
      m, n  query length and DATABASE length
      K, lambda  constants of the scoring system

  WHAT IT MEANS
      the expected NUMBER of alignments scoring at
      least S that would occur by chance in a
      database of this size.

  SO
      E = 10 means expect ten such hits by chance
      E = 1e-50 means essentially never by chance
      E depends on DATABASE SIZE: the same alignment
          has a worse E-value in a larger database,
          which is correct and surprises people

  AND NOTE
      E is not a p-value, though for small E they
      nearly coincide
      E says nothing about whether the hit is
          biologically meaningful (Part 4)
""",
   "caption": "<b>The same alignment has a worse E-value in a larger "
              "database</b>, which is correct multiple-testing "
              "accounting and surprises people every "
              "time.",
   "note": "E-values are multiple testing, built into the tool."},

  {"t": "section", "label": "Part 4", "title": "Significant and meaningless",
   "blurb": "The two ways a good E-value misleads."},

  {"t": "bullets", "kicker": "Caveats", "title": "What a significant hit does not establish",
   "items": [
     "<b>Low-complexity regions produce spurious "
     "significance</b> — <b>a run of the same residue matches "
     "every other such run</b>, and the null model assumed "
     "composition that the sequence does not "
     "have.",
     "",
     "<b>Which is why filtering is on by "
     "default</b> — and why turning it off changes results "
     "dramatically.",
     "",
     "<b>And statistical significance is not homology</b> — "
     "<b>convergent evolution and shared short motifs both produce "
     "real matches without common ancestry.</b>",
     "",
     "<b>Nor is homology function</b> — <b>related sequences "
     "routinely do different things</b>, and <b>annotation transfer by "
     "similarity propagates errors through "
     "databases</b>.",
     "",
     "<b>So the chain is: score → significance → homology "
     "→ function</b>, and <b>each arrow is an inference somebody "
     "has to defend.</b>",
   ],
   "footnote": "<b>Annotation transfer by similarity propagates "
               "errors through databases</b> — a mislabelled entry "
               "becomes the evidence for the next "
               "one."},

  {"t": "callout", "title": "And the general lesson, which outlives the biology",
   "kind": "Closing",
   "body": ["<b>Every method in the rest of this course produces a "
            "score</b>, and <b>every one of them needs the same "
            "question asked:</b> <b>what would this look like if there "
            "were nothing there?</b>",
            "<b>Which is the empirical null, and it is almost always "
            "available</b> — <b>permute, shuffle, or "
            "randomise</b> — and costs a rerun "
            "(Module 01 §4).",
            "<b>And it is the one technique that catches errors in "
            "the parts of the pipeline you did not think "
            "about</b> — because it tests the whole thing rather than "
            "the model you have in mind.",
            "<b>So the habit: build the null before interpreting the "
            "score</b> — which is <b>CSCE 676 §13's framing and "
            "CSCE 658 §09's discipline</b>, and is the single most "
            "transferable thing in this course."]},
 ],
 "takeaways": [
   "A substitution score is a log-odds ratio, which is why scores are "
   "summed along an alignment.",
   "The expected score of a random pair must be negative, or longer "
   "alignments always score higher.",
   "A score is only interpretable against the distribution of scores from "
   "unrelated sequences.",
   "The same alignment has a worse E-value in a larger database, which is "
   "correct multiple-testing accounting.",
   "Statistical significance is not homology, and homology is not function "
   "— each arrow is a separate inference.",
   "Annotation transfer by similarity propagates errors through databases.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Substitution matrices"),
  ("eq", "s(a,b) = log [ p(a,b) / (q(a) &middot; q(b)) ]"),
  ("ul", ["<b>This is the log-odds of observing a aligned with b "
          "under a model of relatedness, versus under "
          "independence</b> — <b>positive means more likely than "
          "chance, negative means less</b>, and that is the entire "
          "interpretation.",
          "<b>PAM matrices are estimated from closely related "
          "proteins and then extrapolated</b> by matrix exponentiation: "
          "<b>PAM250 is the PAM1 model applied 250 times</b>, which "
          "makes it a model of evolution over time — <b>and the "
          "extrapolation is the weak part</b>, since the model's errors "
          "compound.",
          "<b>BLOSUM62 is counted directly from blocks of aligned "
          "sequences at no more than 62% identity</b> — <b>no "
          "extrapolation, counted at the divergence you actually care "
          "about</b> — <b>which is why it replaced PAM for most "
          "purposes</b> and is the usual default.",
          "<b>A substitution score is a log-odds ratio, so adding "
          "scores along an alignment multiplies likelihood "
          "ratios</b> — <b>which is why summing is the right "
          "operation</b> and not merely a convenient one. <b>The "
          "log-odds framing explains both why scores are summed and why "
          "some of them must be negative</b> (&sect;1's "
          "callout)."]),
  ("callout", "And the matrix encodes an assumed divergence, so using the "
              "wrong one costs real accuracy",
   ["<b>A matrix tuned for closely related sequences penalises "
    "substitutions heavily</b>; <b>one tuned for distant relatives "
    "tolerates them</b> — and <b>the right choice depends entirely "
    "on what you are looking for</b>, which you must decide before "
    "searching.",
    "<b>So using BLOSUM80 to find remote homologues finds fewer of "
    "them</b>, and <b>using BLOSUM45 for close matches gives noisier "
    "alignments with spurious extensions</b> — <b>both of which are "
    "measurable effects rather than matters of preference</b>, and both "
    "of which are easy to demonstrate.",
    "<b>Which means the matrix is a stated assumption</b>, and "
    "<b>Project 1 asks you to align one pair under two matrices and "
    "report the difference</b>, <b>because the difference is frequently "
    "larger than expected</b> — sometimes a different alignment "
    "entirely, not merely a different score.",
    "<b>And the expected score for a random pair must be "
    "negative</b> — <b>otherwise longer alignments always score "
    "higher simply by being longer</b>, <b>and local alignment becomes "
    "meaningless</b> (Module 02 &sect;2's trap). This is a "
    "constraint on how a matrix may be constructed, not an "
    "observation."]),

  ("h1", "2 &nbsp; The null model"),
  ("callout", "A score is only interpretable against the distribution of "
              "scores from unrelated sequences",
   ["<b>412 is meaningless on its own</b> — <b>the question is "
    "how often a pair of unrelated sequences of these lengths and these "
    "amino acid compositions would score 412 or better</b>, which is a "
    "question about a distribution rather than about this pair.",
    "<b>And that distribution is computable</b>: <b>for ungapped "
    "local alignment, the optimal scores follow an extreme value "
    "(Gumbel) distribution</b> — which is unsurprising, since an "
    "optimal local score is a maximum over many positions — and "
    "<b>that is where &sect;3's E-value formula comes from.</b>",
    "<b>Or it is simply measurable</b>: <b>shuffle one sequence a "
    "few thousand times, realign each shuffle, and plot the resulting "
    "scores</b> — <b>which takes minutes and makes no "
    "distributional assumption at all</b>, and which also accounts for "
    "composition automatically.",
    "<b>Which is Project 1's central requirement, and the habit this "
    "module exists to install</b> — <b>a score without a null is "
    "not a result</b>, <b>in this field or any other</b> (CSCE 658 "
    "Module 09's permutation testing, CSCE 676 Module 11's "
    "significance material)."]),

  ("break",),
  ("h1", "3 &nbsp; E-values"),
  ("code", """E = K * m * n * exp(-lambda * S)

    S     the alignment score
    m, n  query length and DATABASE length
    K, lambda  constants of the scoring system

WHAT IT MEANS
    the expected NUMBER of alignments scoring at
    least S that would occur by chance in a database
    of this size.

SO
    E = 10 means expect ten such hits by chance
    E = 1e-50 means essentially never by chance
    E depends on DATABASE SIZE: the same alignment
        has a worse E-value in a larger database,
        which is correct and surprises people

AND NOTE
    E is not a p-value, though for small E the two
        nearly coincide
    E says nothing about whether the hit is
        biologically meaningful (section 4)"""),
  ("p", "<b>The same alignment has a worse E-value in a larger "
        "database</b>, <b>which is correct multiple-testing accounting "
        "and surprises people every time</b>: searching more sequences "
        "means more chances for a chance match, so the same score is less "
        "surprising. <b>E-values are multiple testing, built into the "
        "tool</b> — which is an unusually good piece of statistical "
        "design, and is worth noticing because Module 10 &sect;3 "
        "covers the case where nobody built it in for you."),

  ("h1", "4 &nbsp; Significant and meaningless"),
  ("ul", ["<b>Low-complexity regions produce spurious "
          "significance</b> — <b>a run of the same residue matches "
          "every other such run with a high score</b> — and <b>the "
          "null model assumed a composition that the sequence does not "
          "have</b>, so the E-value is computed under a false "
          "premise.",
          "<b>Which is why complexity filtering is on by default</b> "
          "in the standard tools — <b>and why turning it off "
          "changes results dramatically</b>, which is worth doing once "
          "deliberately to see the effect.",
          "<b>And statistical significance is not "
          "homology</b> — <b>convergent evolution and shared short "
          "functional motifs both produce genuinely significant matches "
          "without any common ancestry</b> — so the inference from "
          "one to the other is a judgement.",
          "<b>Nor is homology function</b> — <b>related "
          "sequences routinely do different things</b>, particularly "
          "after duplication — and <b>annotation transfer by "
          "similarity propagates errors through databases</b>: <b>a "
          "mislabelled entry becomes the evidence for the next one</b>, "
          "and the error compounds silently across releases.",
          "<b>So the chain is: score &rarr; significance &rarr; "
          "homology &rarr; function</b>, and <b>each arrow is an "
          "inference somebody has to defend</b> — which is "
          "Module 01 &sect;3's chain in its first concrete "
          "instance."]),
  ("callout", "And the general lesson, which outlives the biology",
   ["<b>Every method in the rest of this course produces a "
    "score</b> — an alignment score, a posterior probability, a "
    "fold energy, a test statistic — and <b>every one of them needs "
    "the same question asked:</b> <b>what would this look like if there "
    "were nothing there?</b>",
    "<b>Which is the empirical null, and it is almost always "
    "available</b> — <b>permute the labels, shuffle the sequence, "
    "randomise the assignment</b> — <b>and it costs one rerun</b> "
    "(Module 01 &sect;4).",
    "<b>And it is the one technique that catches errors in the "
    "parts of the pipeline you did not think about</b>, <b>because it "
    "tests the whole thing end to end rather than the model you have in "
    "your head</b> — a bug that inflates scores inflates the null "
    "too, and a bug that leaks labels shows up immediately.",
    "<b>So the habit: build the null before interpreting the "
    "score</b> — which is <b>CSCE 676 Module 13's framing and "
    "CSCE 658 Module 09's discipline</b>, and <b>is the single most "
    "transferable thing in this course.</b>"]),
 ],
 "resources": [
   ("Henikoff & Henikoff &mdash; Amino acid substitution matrices "
    "from protein blocks (free)",
    "https://www.pnas.org/doi/10.1073/pnas.89.22.10915",
    "<b>&sect;1's BLOSUM</b> in the original, with the construction "
    "explained."),
   ("Karlin & Altschul &mdash; Methods for assessing the statistical "
    "significance of molecular sequence features (free)",
    "https://www.pnas.org/doi/10.1073/pnas.87.6.2264",
    "<b>&sect;&sect;2 and 3</b> — where the E-value formula comes "
    "from, and the extreme-value argument."),
   ("The NCBI BLAST statistics documentation (free)",
    "https://www.ncbi.nlm.nih.gov/BLAST/tutorial/Altschul-1.html",
    "<b>&sect;3</b> — how to read a report, by the people who compute "
    "the numbers."),
   ("Wootton & Federhen &mdash; Statistics of local complexity in "
    "amino acid sequences",
    "https://pubmed.ncbi.nlm.nih.gov/8743706/",
    "<b>&sect;4's first caveat</b> — low complexity, and why filtering "
    "exists."),
 ],
 "exercises": [
   "<b>Derive the log-odds form</b> and explain why scores add.",
   "<b>Compare BLOSUM45, 62, and 80</b> on the same distant pair.",
   "<b>Check that a matrix's expected random score is "
   "negative.</b>",
   "<b>Construct a matrix with all positive entries</b> and watch "
   "local alignment degenerate.",
   "<b>Build an empirical null</b> by shuffling, with 5000 "
   "replicates.",
   "<b>Place a real score in it</b> and report the empirical "
   "p-value.",
   "<b>Compare that to the E-value</b> the formula gives.",
   "<b>Search the same query against two database sizes</b> and "
   "compare E-values.",
   "<b>Run one search with and without complexity filtering.</b>",
   "<b>Find one database entry whose annotation was transferred</b>, "
   "and trace it back.",
 ],
 "selfcheck": [
   "What is a substitution score, formally?",
   "Why are scores summed?",
   "Contrast PAM and BLOSUM construction.",
   "Why must the expected random score be negative?",
   "Why is a score alone uninterpretable?",
   "Give two ways to obtain a null distribution.",
   "Define an E-value, and say what m and n are.",
   "Why does database size change it, and is that right?",
   "Give four things a significant hit does not establish.",
   "State the general lesson and the technique.",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Search and Indexing",
 "subtitle": "When quadratic is too slow, and what you give up.",
 "question": "How do you align against forty billion bases?",
 "outcomes": [
     "Explain seed-and-extend heuristics.",
     "Explain what BLAST trades for its speed.",
     "Explain suffix structures and their space cost.",
     "Explain the BWT and the FM-index.",
     "Choose a search strategy from the requirement.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Seed and extend",
   "blurb": "The heuristic that made database search practical."},

  {"t": "code", "kicker": "BLAST", "title": "The idea, and the assumption inside it",
   "lang": "text", "code": """
  THE PROBLEM
      Smith-Waterman against a 40-billion-base
      database is O(query x database). Too slow.

  THE HEURISTIC
      1  break the query into short words (seeds)
      2  find exact (or near-exact) word matches in
         an index of the database
      3  extend each hit outward without gaps while
         the score improves
      4  keep the good ones, then do a full gapped
         alignment only on those

  THE ASSUMPTION
      a real alignment contains at least one exact
      word match of length w.

  WHICH IS USUALLY TRUE AND NOT ALWAYS. Raising w
  makes it faster and less sensitive; lowering w
  does the reverse. That dial IS the trade.
""",
   "caption": "<b>The word length is the sensitivity dial</b>, and "
              "the assumption — that a true alignment contains an "
              "exact word match — is what can "
              "fail.",
   "note": "Every fast search method has an assumption of this "
           "shape."},

  {"t": "callout", "title": "So a heuristic search can miss true alignments, and the miss rate is rarely reported",
   "kind": "The honest statement about every tool in this module",
   "body": ["<b>BLAST is not guaranteed to find the optimal local "
            "alignment</b> — <b>it finds alignments that contain a "
            "seed</b>, which is a different set.",
            "<b>And remote homologues are exactly the cases most "
            "likely to be missed</b>, because they are the ones least "
            "likely to contain a long exact match — <b>so the misses "
            "are not random.</b>",
            "<b>Which is why profile methods exist</b> "
            "(Module 07 §3) — <b>a profile uses the whole family's "
            "conservation pattern rather than one "
            "sequence</b>, and finds what pairwise "
            "search cannot.",
            "<b>So 'no significant hits' means 'this tool with these "
            "parameters found none'</b> — <b>which is a much weaker "
            "statement than it is usually taken to be</b>, and is "
            "Module 13's point in miniature."]},

  {"t": "section", "label": "Part 2", "title": "Suffix structures",
   "blurb": "Exact matching in linear time, at a price."},

  {"t": "table", "kicker": "Indexes", "title": "The exact-match structures and their costs",
   "header": ["Structure", "Query time", "Space"],
   "widths": [3.2, 3.5, 4.3],
   "rows": [
     ["<b>Suffix tree</b>", "<b>O(m) for a pattern of length m</b>", "<b>~20 bytes per base. Too much</b>"],
     ["<b>Suffix array</b>", "<b>O(m log n), or O(m) with extras</b>", "<b>~4-8 bytes per base</b>"],
     ["<b>FM-index (BWT)</b>", "<b>O(m), backward search</b>", "<b>Under 1 byte per base</b>"],
     ["<b>k-mer hash table</b>", "<b>O(1) per word</b>", "<b>Large, and fixed word length</b>"],
   ],
   "footnote": "<b>The FM-index is why read mapping onto a human "
               "genome fits in a few gigabytes</b> — the space "
               "reduction is what made Module 05 "
               "practical.",
   "note": "Space, not time, is what decided which structure won."},

  {"t": "section", "label": "Part 3", "title": "The BWT",
   "blurb": "A reversible permutation that happens to be searchable."},

  {"t": "code", "kicker": "BWT", "title": "How it works, in outline",
   "lang": "text", "code": """
  CONSTRUCTION
      take all rotations of the string (plus a
      terminator), sort them, and take the last
      column. That column is the BWT.

  WHY IT IS USEFUL
      identical characters cluster, so it compresses
      well -- which is why it was invented, for
      compression, not for biology.

  THE SEARCH PROPERTY (LF-mapping)
      the i-th occurrence of character c in the last
      column corresponds to the i-th occurrence of c
      in the first column. That correspondence lets
      you walk backwards through the text.

  SO BACKWARD SEARCH
      match the pattern right to left, maintaining
      the range of rows prefixed by the matched
      suffix. O(m), with a small index.

  AND IT IS REVERSIBLE: the original string is
  recoverable, which is what makes it an index
  rather than a lossy summary.
""",
   "caption": "<b>The BWT was invented for compression and turned "
              "out to be searchable</b> — which is why the index is "
              "smaller than the text it "
              "indexes."},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "By what the task actually requires."},

  {"t": "bullets", "kicker": "Choosing", "title": "The questions that decide the method",
   "items": [
     "<b>Exact or approximate matching?</b> — <b>exact is "
     "solved and cheap; approximate is where all the difficulty "
     "is</b>, and every method handles mismatches by "
     "backtracking or by seeding.",
     "",
     "<b>One query or millions?</b> — <b>an index pays off "
     "across many queries</b> and is wasted on one "
     "(Module 05's read mapping is the "
     "many case).",
     "",
     "<b>Is the reference fixed?</b> — <b>if so, build the "
     "index once</b>; if the database changes constantly, indexing "
     "cost matters.",
     "",
     "<b>How sensitive must it be?</b> — <b>which sets the "
     "seed length, and should be chosen from the expected divergence "
     "rather than from the default.</b>",
     "",
     "<b>And what will you report when it finds "
     "nothing?</b> (Part 1) — which is the "
     "question this module most wants asked.",
   ],
   "footnote": "<b>'No significant hits' is a statement about a "
               "tool and its parameters</b>, not about the biology "
               "— and it is reported as though it were the "
               "latter."},

  {"t": "callout", "title": "And the pattern to carry forward",
   "kind": "Closing",
   "body": ["<b>Exact is quadratic, and everything faster assumes "
            "something</b> (Module 02 §4) — <b>here the "
            "assumption is that a true alignment contains an exact "
            "seed.</b>",
            "<b>And the assumption is usually "
            "reasonable</b> — <b>these tools work, and the field "
            "depends on them</b> — which is why it is so easy to stop "
            "noticing that it is an assumption.",
            "<b>So the discipline is to name it when reporting "
            "a negative</b> — <b>'BLASTP with default parameters "
            "found no significant hits' is checkable, and 'there is no "
            "homologue' is not.</b>",
            "<b>Which is the program's rule applied to a search "
            "tool</b>: <b>state what you ran, and do not promote the "
            "tool's output into a biological claim.</b>"]},
 ],
 "takeaways": [
   "Seed-and-extend assumes a true alignment contains an exact word match, "
   "and the word length is the sensitivity dial.",
   "A heuristic search can miss true alignments, and the misses are "
   "concentrated in remote homologues rather than random.",
   "'No significant hits' means this tool with these parameters found none, "
   "which is much weaker than it sounds.",
   "Space rather than time is what decided which index structure won.",
   "The BWT was invented for compression and turned out to be searchable, "
   "which is why the index is smaller than the text.",
   "An index pays off across many queries and is wasted on one.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Seed and extend"),
  ("code", """THE PROBLEM
    Smith-Waterman against a 40-billion-base
    database is O(query x database). Far too slow
    for interactive use.

THE HEURISTIC
    1  break the query into short words (seeds)
    2  find exact (or near-exact) word matches in a
       precomputed index of the database
    3  extend each hit outward without gaps while
       the score keeps improving
    4  keep the good ones, and do a full gapped
       alignment only on those

THE ASSUMPTION
    a real alignment contains at least one exact
    word match of length w.

WHICH IS USUALLY TRUE AND NOT ALWAYS. Raising w
makes the search faster and less sensitive; lowering
w does the reverse. That dial IS the trade."""),
  ("p", "<b>The word length is the sensitivity dial</b>, and <b>the "
        "assumption — that a true alignment contains an exact word "
        "match — is what can fail</b>. <b>Every fast search method "
        "in this course has an assumption of this shape</b>: a cheap "
        "filter that is applied first, and that is believed not to "
        "discard anything important. Naming the filter is how you reason "
        "about what a tool can miss."),
  ("callout", "So a heuristic search can miss true alignments, and the miss "
              "rate is rarely reported",
   ["<b>BLAST is not guaranteed to find the optimal local "
    "alignment</b> — <b>it finds alignments that contain a "
    "seed</b>, <b>which is a different set</b> from the set of "
    "high-scoring alignments, overlapping it heavily but not "
    "containing it.",
    "<b>And remote homologues are exactly the cases most likely to "
    "be missed</b>, because they are by definition the ones least likely "
    "to contain a long exact match — <b>so the misses are not "
    "random, they are concentrated precisely where the interesting "
    "biology is.</b>",
    "<b>Which is why profile methods exist</b> (Module 07 "
    "&sect;3) — <b>a profile uses a whole family's position-specific "
    "conservation pattern rather than a single sequence</b>, <b>and "
    "finds relationships that pairwise search cannot</b>, at the cost of "
    "needing the family first.",
    "<b>So 'no significant hits' means 'this tool, with these "
    "parameters, against this database version, found none'</b> — "
    "<b>which is a very much weaker statement than it is usually taken "
    "to be</b>, and <b>is Module 13's point in miniature</b>."]),

  ("h1", "2 &nbsp; Suffix structures"),
  ("table", ["Structure", "Query time", "Space"],
   [["<b>Suffix tree</b>", "<b>O(m) for a pattern of length m</b>",
     "<b>Roughly 20 bytes per base with pointers</b> — which for a "
     "human genome is tens of gigabytes. Too much."],
    ["<b>Suffix array</b>", "<b>O(m log n), or O(m) with extra "
     "tables</b>",
     "<b>Four to eight bytes per base</b> — better, and still "
     "large."],
    ["<b>FM-index (built on the BWT)</b>",
     "<b>O(m), by backward search</b> (&sect;3)",
     "<b>Under one byte per base</b> — the index is smaller than "
     "the text."],
    ["<b>k-mer hash table</b>", "<b>O(1) per word</b>",
     "<b>Large, and the word length is fixed at build time</b> — "
     "which is what &sect;1's tools use."]],
   [0.26, 0.34, 0.40]),
  ("p", "<b>The FM-index is why read mapping onto a human genome fits "
        "in a few gigabytes</b> — <b>the space reduction is what "
        "made Module 05 practical</b> on ordinary hardware, and it "
        "arrived at roughly the time short-read sequencing did, which is "
        "a fortunate coincidence. <b>Space, not time, is what decided "
        "which structure won</b>: suffix trees have been asymptotically "
        "optimal for query time since 1973 and are not what anybody "
        "uses."),

  ("break",),
  ("h1", "3 &nbsp; The BWT"),
  ("code", """CONSTRUCTION
    take all rotations of the string (plus a
    terminator character), sort them lexicographic-
    ally, and take the last column. That column is
    the Burrows-Wheeler transform.

WHY IT IS USEFUL
    identical characters cluster together, so it
    compresses well -- which is why it was invented,
    for compression, and not for biology.

THE SEARCH PROPERTY (LF-mapping)
    the i-th occurrence of character c in the last
    column corresponds to the i-th occurrence of c
    in the first column. That correspondence lets
    you walk backwards through the original text.

SO BACKWARD SEARCH
    match the pattern right to left, maintaining the
    range of sorted rows prefixed by the matched
    suffix. O(m), with a small index.

AND IT IS REVERSIBLE: the original string is
recoverable from the transform, which is what makes
it an index rather than a lossy summary."""),
  ("p", "<b>The BWT was invented for compression and turned out to be "
        "searchable</b> — <b>which is why the index can be smaller "
        "than the text it indexes</b>, a property that sounds impossible "
        "until you notice that the transform is the text, rearranged. "
        "Approximate matching is handled by backtracking the backward "
        "search: when a mismatch exhausts the range, try the other "
        "characters, which costs exponentially in the number of "
        "mismatches allowed and is why these tools permit only a "
        "few."),

  ("h1", "4 &nbsp; Choosing"),
  ("ul", ["<b>Exact or approximate matching?</b> — <b>exact "
          "matching is solved and cheap; approximate matching is where "
          "all the difficulty is</b>, and every method handles mismatches "
          "either by backtracking (&sect;3) or by seeding "
          "(&sect;1).",
          "<b>One query or millions?</b> — <b>an index pays "
          "off across many queries and is wasted on one</b> — and "
          "<b>Module 05's read mapping is emphatically the many "
          "case</b>, with hundreds of millions of queries against a "
          "fixed reference.",
          "<b>Is the reference fixed?</b> — <b>if so, build "
          "the index once and amortise it</b>; <b>if the database "
          "changes constantly, the indexing cost itself matters</b> and "
          "a hash table may win.",
          "<b>How sensitive must the search be?</b> — <b>which "
          "sets the seed length, and should be chosen from the expected "
          "divergence between query and target rather than from the "
          "tool's default</b>, which was chosen for someone else's "
          "problem.",
          "<b>And what will you report when it finds nothing?</b> "
          "(&sect;1's callout) — <b>which is the question this "
          "module most wants asked</b>. <b>'No significant hits' is a "
          "statement about a tool and its parameters, not about the "
          "biology</b> — <b>and it is reported as though it were "
          "the latter</b>, routinely."]),
  ("callout", "And the pattern to carry forward",
   ["<b>Exact is quadratic, and everything faster assumes "
    "something</b> (Module 02 &sect;4's organising sentence) — "
    "<b>and here the assumption is that a true alignment contains an "
    "exact seed of the chosen length.</b>",
    "<b>And the assumption is usually reasonable</b> — "
    "<b>these tools work, they are extremely well tested, and the whole "
    "field depends on them</b> — <b>which is exactly why it is so "
    "easy to stop noticing that it is an assumption</b> rather than a "
    "guarantee.",
    "<b>So the discipline is to name it when reporting a "
    "negative result</b> — <b>'BLASTP with default parameters "
    "against this database found no significant hits' is checkable, and "
    "'there is no homologue' is not</b>, and the two are routinely "
    "written as though they were the same sentence.",
    "<b>Which is the program's rule applied to a search "
    "tool</b>: <b>state what you ran, and do not promote the tool's "
    "output into a biological claim</b> (Module 13 &sect;1's "
    "chain)."]),
 ],
 "resources": [
   ("Altschul et al. &mdash; Basic local alignment search tool (free)",
    "https://pubmed.ncbi.nlm.nih.gov/2231712/",
    "<b>&sect;1 in the original</b> — and the heuristic's assumption "
    "is stated openly in it, which is worth seeing."),
   ("Burrows & Wheeler &mdash; A block-sorting lossless data "
    "compression algorithm",
    "https://www.hpl.hp.com/techreports/Compaq-DEC/SRC-RR-124.pdf",
    "<b>&sect;3 in the original</b>, where it is entirely about "
    "compression."),
   ("Ferragina & Manzini &mdash; Opportunistic data structures with "
    "applications",
    "https://ieeexplore.ieee.org/document/892127",
    "<b>&sect;3's FM-index</b> — the search property, and the space "
    "bound that made it matter."),
   ("Langmead & Salzberg &mdash; Fast gapped-read alignment with "
    "Bowtie 2 (free)",
    "https://www.nature.com/articles/nmeth.1923",
    "<b>&sect;&sect;3 and 4 applied</b> — and the bridge to "
    "Module 05."),
 ],
 "exercises": [
   "<b>Implement seed-and-extend</b> with a hash of k-mers.",
   "<b>Vary the word length</b> and measure speed against "
   "sensitivity.",
   "<b>Construct a pair</b> that a given seed length provably "
   "misses.",
   "<b>Compare BLAST's hits</b> to full Smith-Waterman on a small "
   "database.",
   "<b>Build a suffix array</b> for a short string and search it.",
   "<b>Compute a BWT by hand</b> for a ten-character string.",
   "<b>Verify LF-mapping</b> on it.",
   "<b>Implement backward search</b> and confirm it finds all "
   "occurrences.",
   "<b>Measure index sizes</b> for the same text, three ways.",
   "<b>Rewrite one 'there is no homologue' claim</b> as a checkable "
   "statement.",
 ],
 "selfcheck": [
   "Give the four steps of seed and extend.",
   "What is the assumption, and what is the dial?",
   "Why are the misses concentrated rather than random?",
   "Why do profile methods help?",
   "What does 'no significant hits' actually mean?",
   "Name four index structures with their time and space.",
   "Which won, and on what criterion?",
   "Describe the BWT's construction and its search property.",
   "Why is the index smaller than the text?",
   "Give the five questions that choose a search strategy.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Mapping and Assembly",
 "subtitle": "Reconstructing from fragments, and where repeats break "
             "everything.",
 "question": "Why can't you just put the pieces back together?",
 "outcomes": [
     "Explain read mapping and its error modes.",
     "Explain de Bruijn graph assembly.",
     "Explain why repeats are the fundamental obstacle.",
     "Explain coverage and why it must be uneven.",
     "Interpret assembly quality metrics critically.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Mapping",
   "blurb": "When you already have a reference."},

  {"t": "callout", "title": "Mapping places each read on a reference, and the hard cases are the ones that matter",
   "kind": "The task, and where it goes wrong",
   "body": ["<b>Hundreds of millions of short reads against a fixed "
            "reference</b> — <b>which is Module 04's many-queries "
            "case</b>, and is what the FM-index was "
            "adopted for.",
            "<b>And most reads map uniquely and "
            "easily</b> — <b>the problem is the minority that do "
            "not</b>: <b>reads from repeats, from regions absent in the "
            "reference, and from structural variants.</b>",
            "<b>A multi-mapping read is usually assigned "
            "arbitrarily or discarded</b> — <b>and both choices bias "
            "the result against repetitive regions</b>, "
            "systematically.",
            "<b>Plus reference bias:</b> <b>a read carrying a "
            "variant maps slightly worse than one matching the "
            "reference</b> — <b>so variants are systematically "
            "under-detected</b>, which is a measured effect and a "
            "serious one."]},

  {"t": "section", "label": "Part 2", "title": "Assembly",
   "blurb": "When you do not have a reference."},

  {"t": "code", "kicker": "de Bruijn", "title": "Assembly as a graph problem",
   "lang": "text", "code": """
  THE GRAPH
      nodes: every (k-1)-mer seen in the reads
      edges: every k-mer, joining its prefix to its
             suffix
      an assembly is a path using each edge --
      an Eulerian path, which is tractable
      (Hamiltonian, on the overlap graph, is not)

  WHY k MATTERS
      small k   more overlaps found, more false ones
                graph is tangled
      large k   cleaner graph, but needs higher
                coverage and loses low-coverage
                regions

  WHAT BREAKS IT
      sequencing errors create spurious nodes --
          removed by coverage thresholds
      repeats longer than k create ambiguous paths
          that NO amount of data resolves
      uneven coverage makes the threshold a guess

  SO THE OUTPUT IS CONTIGS, not a genome: pieces
  that could be ordered many ways.
""",
   "caption": "<b>The output is contigs, not a genome</b> — "
              "pieces that the data could order in many ways, and the "
              "ordering is a separate "
              "inference."},

  {"t": "section", "label": "Part 3", "title": "Repeats",
   "blurb": "The fundamental obstacle, and it is informational."},

  {"t": "callout", "title": "A repeat longer than your read length is not resolvable by more reads of that length",
   "kind": "Why this is not an engineering problem",
   "body": ["<b>If the same sequence appears twice and is longer "
            "than a read, no read spans from unique sequence through it "
            "to unique sequence</b> — <b>so the connection is "
            "absent from the data</b>, not merely "
            "hard to find.",
            "<b>Which is an information-theoretic limit rather than "
            "an algorithmic one</b> — <b>more coverage does not "
            "help</b>, and <b>this is the clearest such limit in the "
            "course.</b>",
            "<b>And roughly half of a human genome is "
            "repetitive</b>, which is why short-read assembly of "
            "mammalian genomes stayed poor for a "
            "decade.",
            "<b>So the fix is longer reads, or paired reads with "
            "known separation</b> — <b>changing the measurement rather "
            "than the algorithm</b>, which is this semester's recurring "
            "shape (CSCE 640 §13 §3)."]},

  {"t": "section", "label": "Part 4", "title": "Reading the metrics",
   "blurb": "Critically, because the usual one is gameable."},

  {"t": "bullets", "kicker": "Metrics", "title": "What assembly statistics say and hide",
   "items": [
     "<b>N50: the contig length such that half the assembly is "
     "in contigs at least that long</b> — <b>the standard metric, "
     "and it rewards aggressive joining</b> whether or not the joins "
     "are right.",
     "",
     "<b>So a wrong assembly can have a better N50 than a "
     "correct one</b> — <b>which makes it a proxy with the usual "
     "proxy problem</b> "
     "(CSCE 676 §13).",
     "",
     "<b>Total length against the expected genome "
     "size</b> — <b>too large means uncollapsed "
     "duplicates</b>, too small means collapsed "
     "repeats.",
     "",
     "<b>And completeness by conserved single-copy "
     "genes</b> — <b>which measures something you care about</b>, "
     "and is the metric to prefer.",
     "",
     "<b>Plus: does it agree with an independent "
     "measurement?</b> — optical maps, linkage, or a related "
     "species.",
   ],
   "footnote": "<b>A wrong assembly can have a better N50 than a "
               "correct one</b>, because N50 rewards joining — which "
               "is the proxy problem in its sharpest "
               "form."},

  {"t": "callout", "title": "And the honest summary",
   "kind": "Closing",
   "body": ["<b>A reference genome is an assembly</b>, with all of "
            "this behind it — <b>which is "
            "Module 01 §1's construct, now "
            "with the construction visible.</b>",
            "<b>And reference bias means your variant calls are "
            "biased toward the reference</b> "
            "(Part 1) — <b>which matters most for "
            "populations least represented in the reference</b>, and "
            "that is a known and consequential "
            "problem.",
            "<b>Which is why pangenome references exist</b>: "
            "<b>a graph rather than a single sequence</b>, which is the "
            "current direction and is harder "
            "computationally.",
            "<b>So the thing to carry: your coordinates refer to a "
            "particular assembly of a particular set of "
            "individuals</b> — <b>name it</b>, which is "
            "Module 12 §2's requirement."]},
 ],
 "takeaways": [
   "Most reads map easily; the problem is the minority from repeats, "
   "missing regions, and structural variants.",
   "Reference bias means a read carrying a variant maps slightly worse, so "
   "variants are systematically under-detected.",
   "Assembly output is contigs, not a genome — pieces the data could "
   "order many ways.",
   "A repeat longer than your read length is not resolvable by more reads "
   "of that length; the information is absent.",
   "The fix is longer reads or paired reads — changing the measurement "
   "rather than the algorithm.",
   "A wrong assembly can have a better N50 than a correct one, because N50 "
   "rewards joining.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Mapping"),
  ("callout", "Mapping places each read on a reference, and the hard cases "
              "are the ones that matter",
   ["<b>Hundreds of millions of short reads against a single fixed "
    "reference</b> — <b>which is Module 04's many-queries "
    "case</b> in its purest form, <b>and is exactly what the FM-index "
    "was adopted for</b> (Module 04 &sect;2).",
    "<b>And most reads map uniquely and easily</b> — <b>the "
    "problem is entirely the minority that do not</b>: <b>reads from "
    "repetitive regions, reads from sequence absent in the reference, "
    "and reads spanning structural variants</b>, all of which are the "
    "biologically interesting cases.",
    "<b>A multi-mapping read is usually either assigned arbitrarily "
    "among its best positions or discarded</b> — and <b>both "
    "choices bias the result against repetitive regions "
    "systematically</b>, so coverage appears low exactly where the "
    "mapping is hard.",
    "<b>Plus reference bias</b>: <b>a read carrying a genuine "
    "variant aligns slightly worse than one matching the reference</b>, "
    "so it is more likely to fall below a mapping quality threshold "
    "— <b>and variants are therefore systematically "
    "under-detected</b>, <b>which is a measured effect and a serious "
    "one</b>, especially for the alleles least represented in the "
    "reference (&sect;4's closing callout)."]),

  ("h1", "2 &nbsp; Assembly"),
  ("code", """THE GRAPH
    nodes: every (k-1)-mer seen in the reads
    edges: every k-mer, joining its prefix to its
           suffix
    an assembly is a path using each edge once --
    an Eulerian path, which is tractable
    (a Hamiltonian path on the overlap graph, the
     older formulation, is not)

WHY k MATTERS
    small k   more overlaps found, and more false
              ones; the graph is tangled
    large k   cleaner graph, but needs higher
              coverage and loses low-coverage
              regions entirely

WHAT BREAKS IT
    sequencing errors create spurious nodes --
        removed by coverage thresholds
    repeats longer than k create ambiguous paths
        that NO amount of data resolves (section 3)
    uneven coverage makes the error threshold a
        guess rather than a calculation

SO THE OUTPUT IS CONTIGS, not a genome: pieces that
the data could order in many different ways."""),
  ("p", "<b>The output is contigs, not a genome</b> — <b>pieces "
        "that the data could order in many ways, and the ordering is a "
        "separate inference</b> requiring other evidence (paired reads, "
        "optical maps, linkage, synteny with a relative). The "
        "reformulation from Hamiltonian paths on an overlap graph to "
        "Eulerian paths on a de Bruijn graph is one of the genuinely "
        "elegant moves in the field: the same problem, restated so that a "
        "polynomial algorithm applies (CSCE 629 Module 11's "
        "reductions, used constructively)."),

  ("break",),
  ("h1", "3 &nbsp; Repeats"),
  ("callout", "A repeat longer than your read length is not resolvable by "
              "more reads of that length",
   ["<b>If the same sequence appears twice in the genome and is "
    "longer than a single read, then no read spans from unique sequence "
    "through the repeat into unique sequence on the other "
    "side</b> — <b>so the connection simply is not present in the "
    "data</b>, and no algorithm can recover it.",
    "<b>Which is an information-theoretic limit rather than an "
    "algorithmic one</b> — <b>more coverage does not help at "
    "all</b>, since every additional read has the same "
    "property — <b>and this is the clearest such limit in the "
    "course</b>, worth recognising as a type.",
    "<b>And roughly half of a human genome is repetitive</b> to "
    "some degree, <b>which is why short-read assembly of mammalian "
    "genomes remained poor for a decade</b> despite enormous "
    "improvements in cost and throughput: the throughput was not the "
    "binding constraint.",
    "<b>So the fix is longer reads, or paired reads with a known "
    "separation that spans the repeat</b> — <b>changing the "
    "measurement rather than the algorithm</b> — <b>which is this "
    "semester's recurring shape</b>: when the model comes from outside, "
    "the lever is frequently outside too (CSCE 640 Module 13 "
    "&sect;3's model-from-outside framing)."]),

  ("h1", "4 &nbsp; Reading the metrics"),
  ("ul", ["<b>N50: the contig length such that half the total "
          "assembly length lies in contigs at least that long</b> "
          "— <b>the standard reported metric, and it rewards "
          "aggressive joining</b> whether or not the joins are "
          "correct.",
          "<b>So a wrong assembly can have a better N50 than a "
          "correct one</b> — <b>which makes it a proxy with the "
          "usual proxy problem</b> (CSCE 676 Module 13, "
          "CSCE 671 Module 12 &sect;4): the metric is optimised, the "
          "thing it stood for is not.",
          "<b>Total assembly length compared against the expected "
          "genome size</b> — <b>substantially too large means "
          "uncollapsed duplicate haplotypes</b>, <b>too small means "
          "collapsed repeats</b> — and both are diagnosable.",
          "<b>And completeness measured by recovery of conserved "
          "single-copy genes</b> — <b>which measures something you "
          "actually care about</b>, namely whether the genes are "
          "there — <b>and is the metric to prefer</b> when "
          "reporting.",
          "<b>Plus the independent check: does the assembly agree "
          "with a measurement that did not go through it?</b> — "
          "optical maps, genetic linkage, or synteny with a related "
          "species. <b>A wrong assembly can have a better N50 than a "
          "correct one, because N50 rewards joining</b> — <b>which "
          "is the proxy problem in its sharpest form</b> and a good "
          "example to keep."]),
  ("callout", "And the honest summary",
   ["<b>A reference genome is an assembly</b>, with everything in "
    "this module behind it — <b>which is Module 01 &sect;1's "
    "'construct', now with the construction visible</b> and the sources "
    "of error nameable.",
    "<b>And reference bias means your variant calls are biased "
    "toward the reference</b> (&sect;1) — <b>which matters most for "
    "the populations least represented in the reference's source "
    "individuals</b>, <b>and that is a known, measured, and "
    "consequential problem</b> in medical genomics rather than a "
    "theoretical concern.",
    "<b>Which is why pangenome references exist</b>: <b>a graph "
    "representing variation rather than a single linear "
    "sequence</b> — <b>which is the current direction of the field "
    "and is substantially harder computationally</b>, since every "
    "algorithm in Modules 02 to 05 assumed a string.",
    "<b>So the thing to carry forward: your coordinates refer to a "
    "particular assembly of a particular set of individuals</b> — "
    "<b>name it</b>, <b>which is Module 12 &sect;2's requirement</b> "
    "and the single cheapest thing you can do for reproducibility."]),
 ],
 "resources": [
   ("Compeau, Pevzner & Tesler &mdash; How to apply de Bruijn graphs "
    "to genome assembly (free)",
    "https://www.nature.com/articles/nbt.2023",
    "<b>&sect;2</b> — four pages, and the clearest explanation of the "
    "reformulation."),
   ("Li & Durbin &mdash; Fast and accurate short read alignment with "
    "Burrows-Wheeler transform (free)",
    "https://academic.oup.com/bioinformatics/article/25/14/1754/225615",
    "<b>&sect;1</b> — the mapper most widely used, and its handling of "
    "the hard cases."),
   ("Nagarajan & Pop &mdash; Sequence assembly demystified (free)",
    "https://www.nature.com/articles/nrg3367",
    "<b>&sect;&sect;2 to 4</b> — including an honest treatment of the "
    "metrics."),
   ("The Human Pangenome Reference Consortium (free)",
    "https://humanpangenome.org/",
    "<b>&sect;4's closing callout</b> — what replaces a single linear "
    "reference, and why."),
 ],
 "exercises": [
   "<b>Map a small read set</b> to a small reference and count the "
   "multi-mappers.",
   "<b>Inject a variant</b> into simulated reads and measure the "
   "mapping rate difference.",
   "<b>Build a de Bruijn graph by hand</b> for a short string at two "
   "values of k.",
   "<b>Implement the graph</b> and find an Eulerian path.",
   "<b>Add a simulated repeat</b> longer than k and observe the "
   "ambiguity.",
   "<b>Add more coverage</b> and confirm it does not help.",
   "<b>Add errors</b> and find a coverage threshold that removes "
   "them.",
   "<b>Compute N50</b> for two assemblies, one deliberately "
   "over-joined.",
   "<b>Compute completeness</b> by a set of expected genes.",
   "<b>Find which reference build</b> a public variant file uses.",
 ],
 "selfcheck": [
   "What makes mapping easy, and which cases are hard?",
   "How are multi-mappers handled, and what does that bias?",
   "State reference bias and why it matters.",
   "Describe the de Bruijn construction and why it is tractable.",
   "What does k trade off?",
   "Name three things that break assembly.",
   "What is the output, actually?",
   "Why is a long repeat an information-theoretic limit?",
   "What is the fix, and what kind of fix is it?",
   "Why is N50 a poor metric, and what is better?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Multiple Alignment and Phylogeny",
 "subtitle": "Where error compounds, and the tree looks more certain "
             "than it is.",
 "question": "How confident is that branch?",
 "outcomes": [
     "Explain why exact multiple alignment is intractable.",
     "Explain progressive alignment and its error mode.",
     "Explain distance and character-based tree methods.",
     "Explain bootstrap support and what it measures.",
     "Build and critique a phylogeny.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Multiple alignment",
   "blurb": "Exponential in principle, heuristic in practice."},

  {"t": "callout", "title": "Exact multiple alignment is exponential in the number of sequences, so every tool is a heuristic",
   "kind": "The situation, stated plainly",
   "body": ["<b>The dynamic programming generalises to k sequences "
            "as a k-dimensional table</b> — <b>O(n to the k) time and "
            "space</b> — which is infeasible beyond three or "
            "four.",
            "<b>And the problem is NP-hard under the usual scoring "
            "schemes</b>, so no exact method is coming "
            "(CSCE 629 §12).",
            "<b>So progressive alignment is used:</b> <b>align the "
            "most similar pair, then add sequences one at a time in "
            "guide-tree order</b> — which is fast and is "
            "greedy.",
            "<b>And greedy means early errors are "
            "permanent</b> — <b>'once a gap, always a "
            "gap'</b> — which is the characteristic failure of every "
            "progressive aligner and is why iterative refinement "
            "exists."]},

  {"t": "section", "label": "Part 2", "title": "The circularity",
   "blurb": "Which is worth being explicit about."},

  {"t": "callout", "title": "The guide tree needs an alignment and the alignment needs a guide tree",
   "kind": "A genuine circularity, handled by iteration",
   "body": ["<b>Progressive alignment orders the sequences by a "
            "guide tree</b>, <b>which is built from pairwise "
            "distances</b> — <b>which are themselves alignment "
            "scores.</b>",
            "<b>So the alignment depends on a rough tree, and the "
            "final tree is built from the alignment</b> — <b>which "
            "means the tree is not independent evidence for the "
            "alignment.</b>",
            "<b>And iterative methods alternate between them</b> "
            "until stable — <b>which converges to something, not "
            "necessarily to the right thing</b> "
            "(CSCE 669 §04's local optima).",
            "<b>Which is a good example of a dependency that is easy "
            "to miss when reading a figure</b> — <b>the alignment and "
            "the tree in the same paper are not two independent "
            "results.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Building trees",
   "blurb": "Two families of method, with different failure modes."},

  {"t": "table", "kicker": "Methods", "title": "How trees are built, and what each assumes",
   "header": ["Method", "How", "Assumes"],
   "widths": [2.8, 4.2, 4.0],
   "rows": [
     ["<b>UPGMA</b>", "<b>Cluster by average distance</b>", "<b>A molecular clock. Usually false</b>"],
     ["<b>Neighbour-joining</b>", "<b>Minimise total branch length</b>", "<b>Additive distances. Fast, widely used</b>"],
     ["<b>Maximum parsimony</b>", "<b>Fewest character changes</b>", "<b>Changes are rare. Long-branch attraction</b>"],
     ["<b>Maximum likelihood</b>", "<b>Best tree under an evolutionary model</b>", "<b>The model. Slow, and principled</b>"],
     ["<b>Bayesian</b>", "<b>Posterior over trees</b>", "<b>The model and the prior. Gives intervals</b>"],
   ],
   "footnote": "<b>Every method assumes something that is not "
               "exactly true</b> — and the useful question is "
               "whether the assumption's failure would produce the tree "
               "you are looking at.",
   "note": "The assumption column is the one to read before "
           "believing a tree."},

  {"t": "section", "label": "Part 4", "title": "Support",
   "blurb": "And what a bootstrap value actually measures."},

  {"t": "bullets", "kicker": "Confidence", "title": "Reading the numbers on the branches",
   "items": [
     "<b>The bootstrap resamples alignment columns with "
     "replacement and rebuilds the tree</b> — <b>the support value "
     "is the fraction of replicates containing that "
     "branch.</b>",
     "",
     "<b>Which measures whether the <i>alignment</i> supports the "
     "branch consistently</b> — <b>not whether the branch is "
     "true</b>, and the two come apart when the model is "
     "wrong.",
     "",
     "<b>So systematic error gives high support for the wrong "
     "tree</b> — <b>long-branch attraction being the classic "
     "case</b>, where more data increases confidence in the "
     "error.",
     "",
     "<b>And the alignment's own uncertainty is excluded</b> "
     "(Part 1) — <b>the bootstrap resamples columns of "
     "a fixed alignment</b>, treating it as "
     "given.",
     "",
     "<b>Which means published support values are "
     "optimistic</b>, structurally, and should be read as a lower bound "
     "on uncertainty.",
   ],
   "footnote": "<b>The bootstrap treats the alignment as given</b>, "
               "so it excludes the largest source of uncertainty in the "
               "whole procedure."},

  {"t": "callout", "title": "And a tree is a hypothesis drawn with great confidence",
   "kind": "Closing",
   "body": ["<b>A phylogeny is rendered as a clean branching "
            "diagram</b> — <b>which is a visual claim of certainty "
            "that the underlying inference does not "
            "support</b> (CSCE 679 §09 §1).",
            "<b>And the errors compound along the "
            "pipeline:</b> <b>alignment error feeds tree error, and "
            "the tree is then used to interpret the "
            "alignment.</b>",
            "<b>So the honest presentation shows support values, "
            "states the model, and collapses poorly supported "
            "branches</b> — which is routine practice and is not "
            "universal.",
            "<b>Which is this module's version of the program's "
            "rule:</b> <b>draw the uncertainty, name the model, and do "
            "not let a tidy diagram do the claiming for "
            "you.</b>"]},
 ],
 "takeaways": [
   "Exact multiple alignment is exponential and NP-hard, so every tool is a "
   "heuristic.",
   "Progressive alignment is greedy, so early errors are permanent — "
   "once a gap, always a gap.",
   "The guide tree needs an alignment and the alignment needs a guide tree, "
   "so they are not independent evidence.",
   "Every tree method assumes something not exactly true; the question is "
   "whether the assumption's failure would produce this tree.",
   "A bootstrap value measures whether the alignment supports the branch "
   "consistently, not whether the branch is true.",
   "The bootstrap treats the alignment as given, excluding the largest "
   "source of uncertainty.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Multiple alignment"),
  ("callout", "Exact multiple alignment is exponential in the number of "
              "sequences, so every tool is a heuristic",
   ["<b>The dynamic programming of Module 02 generalises directly "
    "to k sequences as a k-dimensional table</b> — <b>O(n<sup>k</sup>) "
    "time and space</b> — <b>which is infeasible beyond three or "
    "four sequences</b> of any realistic length.",
    "<b>And the problem is NP-hard under the usual sum-of-pairs "
    "scoring schemes</b>, <b>so no exact method is coming</b> "
    "(CSCE 629 Module 12's framing: this is a settled question, not "
    "an open one).",
    "<b>So progressive alignment is what every tool "
    "does:</b> <b>align the most similar pair first, then add the "
    "remaining sequences one at a time in the order given by a guide "
    "tree</b> — <b>which is fast and is unavoidably greedy.</b>",
    "<b>And greedy means early errors are permanent</b> — "
    "<b>'once a gap, always a gap'</b>, because a gap introduced in an "
    "early pairwise step is carried through every subsequent "
    "addition — <b>which is the characteristic failure of every "
    "progressive aligner and is precisely why iterative refinement "
    "methods exist</b> (&sect;2)."]),

  ("h1", "2 &nbsp; The circularity"),
  ("callout", "The guide tree needs an alignment and the alignment needs a "
              "guide tree",
   ["<b>Progressive alignment orders the sequences by a guide "
    "tree</b>, <b>which is built from pairwise distances</b> — "
    "<b>which are themselves derived from pairwise alignment "
    "scores</b> (Module 03 &sect;1).",
    "<b>So the multiple alignment depends on a rough tree, and the "
    "final published tree is built from that alignment</b> — "
    "<b>which means the tree is not independent evidence for the "
    "alignment</b>, and the alignment is not independent evidence for "
    "the tree.",
    "<b>And iterative methods alternate between the two until the "
    "result is stable</b> — <b>which converges to something, and "
    "not necessarily to the right thing</b> (CSCE 669 Module 04's "
    "local optima: alternating optimisation has no global "
    "guarantee).",
    "<b>Which is a good example of a dependency that is easy to miss "
    "when reading a figure</b> — <b>the alignment and the tree "
    "presented in the same paper are not two independent results</b>, "
    "though they are frequently read as mutually corroborating."]),

  ("break",),
  ("h1", "3 &nbsp; Building trees"),
  ("table", ["Method", "How it works", "What it assumes"],
   [["<b>UPGMA</b>", "<b>Hierarchical clustering by average "
     "distance.</b>",
     "<b>A molecular clock — equal rates on all lineages</b>, "
     "<b>which is usually false</b> and produces characteristic "
     "errors."],
    ["<b>Neighbour-joining</b>",
     "<b>Greedily minimise total branch length.</b>",
     "<b>Additive distances.</b> <b>Fast, widely used</b>, and "
     "reasonable when divergence is moderate."],
    ["<b>Maximum parsimony</b>",
     "<b>The tree requiring the fewest character changes.</b>",
     "<b>That changes are rare.</b> <b>Susceptible to long-branch "
     "attraction</b> — see &sect;4."],
    ["<b>Maximum likelihood</b>",
     "<b>The tree maximising the probability of the data under an "
     "explicit evolutionary model.</b>",
     "<b>The model.</b> <b>Slow, and principled</b> — and the "
     "model choice is itself reportable."],
    ["<b>Bayesian inference</b>",
     "<b>Sample the posterior distribution over trees.</b>",
     "<b>The model and the prior.</b> <b>Gives credible intervals "
     "rather than a point estimate</b>, which is its main "
     "advantage."]],
   [0.20, 0.42, 0.38]),
  ("p", "<b>Every method assumes something that is not exactly "
        "true</b> — and <b>the useful question is not 'is the "
        "assumption true' but 'would its failure produce the tree I am "
        "looking at'</b>, which is answerable and specific. <b>The "
        "assumption column is the one to read before believing a "
        "tree</b>, and a paper that does not name its model has not told "
        "you enough to apply the question."),

  ("h1", "4 &nbsp; Support"),
  ("ul", ["<b>The bootstrap resamples the alignment's columns with "
          "replacement and rebuilds the tree from each "
          "replicate</b> — <b>the support value on a branch is the "
          "fraction of replicates in which that branch appears</b> "
          "(CSCE 658 Module 08's bootstrap, applied to trees).",
          "<b>Which measures whether the <i>alignment</i> supports "
          "the branch consistently across its columns</b> — "
          "<b>not whether the branch is true</b> — <b>and the two "
          "come apart whenever the evolutionary model is wrong</b> in a "
          "way that affects all columns similarly.",
          "<b>So systematic error produces high support for the "
          "wrong tree</b> — <b>long-branch attraction being the "
          "classic case</b>, where rapidly evolving lineages are grouped "
          "because of shared convergent changes, and <b>more data "
          "increases confidence in the error</b> rather than correcting "
          "it.",
          "<b>And the alignment's own uncertainty is excluded "
          "entirely</b> (&sect;1) — <b>the bootstrap resamples "
          "columns of a single fixed alignment</b>, <b>treating that "
          "alignment as given</b> when it is itself a heuristic output "
          "with its own error.",
          "<b>Which means published support values are optimistic, "
          "structurally</b>, <b>and should be read as a lower bound on "
          "the uncertainty</b> rather than as a calibrated probability. "
          "<b>The bootstrap treats the alignment as given, so it "
          "excludes the largest source of uncertainty in the whole "
          "procedure.</b>"]),
  ("callout", "And a tree is a hypothesis drawn with great confidence",
   ["<b>A phylogeny is rendered as a clean branching diagram with "
    "crisp bifurcations</b> — <b>which is a visual claim of "
    "certainty that the underlying inference does not support</b> "
    "(CSCE 679 Module 09 &sect;1: a point estimate drawn without its "
    "uncertainty invites a conclusion the data does not support, here in "
    "a discrete setting).",
    "<b>And the errors compound along the pipeline:</b> <b>alignment "
    "error feeds tree error, and the tree is then used to interpret the "
    "alignment</b> and sometimes to refine it — which is "
    "&sect;2's circularity with consequences.",
    "<b>So the honest presentation shows support values on every "
    "branch, states the evolutionary model and the software version, and "
    "collapses poorly supported branches into polytomies</b> — "
    "<b>which is routine good practice and is not universal</b>.",
    "<b>Which is this module's version of the program's rule:</b> "
    "<b>draw the uncertainty, name the model, and do not let a tidy "
    "diagram do the claiming for you</b> — because a reader looking "
    "at a tree sees a fact, not an inference."]),
 ],
 "resources": [
   ("Durbin et al., chapters 6 and 7 (library copy)",
    "https://www.cambridge.org/9780521629713",
    "<b>&sect;&sect;1 and 3</b> — multiple alignment and phylogeny, "
    "probabilistically."),
   ("Felsenstein &mdash; Inferring Phylogenies",
    "https://global.oup.com/academic/product/inferring-phylogenies-9780878931774",
    "<b>&sect;&sect;3 and 4</b> — the standard text, and the bootstrap "
    "is his. Library copy."),
   ("Edgar & Batzoglou &mdash; Multiple sequence alignment (free "
    "review)",
    "https://pubmed.ncbi.nlm.nih.gov/16843651/",
    "<b>&sect;&sect;1 and 2</b> — the heuristics compared, with their "
    "failure modes."),
   ("Felsenstein &mdash; Cases in which parsimony or compatibility "
    "will be positively misleading",
    "https://academic.oup.com/sysbio/article/27/4/401/1626946",
    "<b>&sect;4's long-branch attraction</b>, in the original — and "
    "the title says the finding."),
 ],
 "exercises": [
   "<b>Count the cells</b> in a k-dimensional alignment table for "
   "k = 5, n = 300.",
   "<b>Implement progressive alignment</b> for four short "
   "sequences.",
   "<b>Change the guide tree order</b> and compare the alignments.",
   "<b>Construct a case</b> where an early gap is clearly wrong and "
   "cannot be fixed.",
   "<b>Build trees by two methods</b> from the same alignment and "
   "compare.",
   "<b>Build a tree from two different alignments</b> of the same "
   "sequences.",
   "<b>Run a bootstrap</b> with 1000 replicates and report "
   "support.",
   "<b>Simulate long-branch attraction</b> and watch support rise for "
   "the wrong grouping.",
   "<b>Collapse branches below 70% support</b> and compare the two "
   "figures.",
   "<b>Find a published tree</b> with no support values, and say what "
   "is missing.",
 ],
 "selfcheck": [
   "Why is exact multiple alignment infeasible?",
   "Describe progressive alignment and its characteristic failure.",
   "State the circularity and how it is handled.",
   "Why are the alignment and the tree not independent?",
   "Name five tree methods and what each assumes.",
   "What is the useful question about an assumption?",
   "What does a bootstrap value measure?",
   "What does it not measure, and when do they diverge?",
   "What does the bootstrap exclude, and why does that matter?",
   "What does an honest tree figure contain?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Hidden Markov Models",
 "subtitle": "Alignment's recurrence, with probabilities and hidden "
             "state.",
 "question": "Which parts of this sequence are which?",
 "outcomes": [
     "Define an HMM and its three standard problems.",
     "Derive Viterbi and the forward algorithm.",
     "Explain profile HMMs and remote homology detection.",
     "Explain gene finding and its limits.",
     "Implement and apply an HMM.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The model",
   "blurb": "States you cannot see, emitting symbols you can."},

  {"t": "eq", "kicker": "Definition", "title": "An HMM, and the three questions",
   "eqs": [
     ("states S, transitions a(i,j), emissions e_i(x), start π",
      "A Markov chain over hidden states, each emitting an "
      "observable symbol. You see the symbols; the states are what "
      "you want."),
     ("decoding: argmax over paths of P(path | sequence)  — Viterbi",
      "The single most likely state path. Dynamic programming, with "
      "the max-of-predecessors structure of Module 02."),
     ("evaluation: P(sequence) summed over all paths  — forward",
      "Same recurrence with sum in place of max. Gives the "
      "likelihood, which is what scoring and comparison need."),
   ],
   "caption": "<b>Viterbi is max and forward is sum, over the same "
              "recurrence</b> — which is the whole relationship "
              "between the two.",
   "note": "If you can write Needleman-Wunsch you can write Viterbi."},

  {"t": "callout", "title": "And the third problem is learning the parameters, which is where it gets delicate",
   "kind": "Training, and its failure mode",
   "body": ["<b>Given sequences and no labels, Baum-Welch "
            "(expectation-maximisation) estimates the "
            "parameters</b> — <b>and converges to a local "
            "optimum</b> (CSCE 633 §07).",
            "<b>So initialisation matters, and different starts give "
            "different models</b> — <b>which should be reported and "
            "usually is not.</b>",
            "<b>And with labelled data it is just counting</b>, "
            "with pseudocounts to avoid zero probabilities — "
            "<b>which is far more reliable</b> and is what profile HMMs "
            "do.",
            "<b>Which is the general preference:</b> <b>estimate "
            "from labelled examples where you have them</b>, and treat "
            "unsupervised structure discovery as the weaker claim "
            "(CSCE 676 §05)."]},

  {"t": "section", "label": "Part 2", "title": "Viterbi",
   "blurb": "Which is Module 02's recurrence with a different "
            "alphabet of moves."},

  {"t": "code", "kicker": "Viterbi", "title": "The recurrence, and the two implementation rules",
   "lang": "text", "code": """
  v_k(i) = e_k(x_i) * max over j of [ v_j(i-1) * a(j,k) ]

      v_k(i)  best probability of any path ending in
              state k having emitted the first i
              symbols
      traceback pointer: which j achieved the max

  COMPARE Module 02:
      max over three predecessors -> max over states
      substitution score         -> emission prob
      gap penalty                -> transition prob
      SAME SHAPE.

  TWO RULES FOR IMPLEMENTING IT
      1  work in log space. Products of thousands of
         probabilities underflow to zero in double
         precision, silently.
      2  for the forward algorithm, summing in log
         space needs a log-sum-exp with the max
         factored out, or it overflows.

  THESE TWO BUGS ACCOUNT FOR MOST BROKEN HMM CODE.
""",
   "caption": "<b>Work in log space, and use log-sum-exp for the "
              "forward algorithm</b> — these two bugs account for "
              "most broken HMM implementations."},

  {"t": "section", "label": "Part 3", "title": "Profile HMMs",
   "blurb": "Which find what pairwise search cannot."},

  {"t": "callout", "title": "A profile HMM encodes a family's position-specific conservation, which is strictly more information than any one sequence",
   "kind": "Why this beats pairwise search for remote homology",
   "body": ["<b>Match, insert, and delete states per alignment "
            "column</b> — <b>with position-specific emission and gap "
            "probabilities</b> estimated from the family's "
            "alignment.",
            "<b>So a position that is absolutely conserved across "
            "the family scores a mismatch heavily, and a variable "
            "position barely at all</b> — <b>which a single "
            "substitution matrix cannot express</b> "
            "(Module 03 §1).",
            "<b>Which is why profile methods find remote homologues "
            "that BLAST misses</b> "
            "(Module 04 §1) — the information is in "
            "the family, not in any member.",
            "<b>And iterated search builds the profile as it "
            "goes</b> — <b>powerful, and it can drift</b>: <b>a false "
            "hit incorporated into the profile recruits more like "
            "itself</b>, which is a specific and known "
            "failure."]},

  {"t": "section", "label": "Part 4", "title": "Gene finding",
   "blurb": "The classic application, and what it does not do."},

  {"t": "bullets", "kicker": "Gene finding", "title": "What an HMM gene finder does and does not establish",
   "items": [
     "<b>States for coding, intron, intergenic, and the signal "
     "sites</b> — <b>and Viterbi labels every base</b>, which is a "
     "complete and plausible annotation of the whole "
     "sequence.",
     "",
     "<b>It is very good at this</b>, and it is how most genome "
     "annotation starts — <b>which is why the caveats "
     "matter.</b>",
     "",
     "<b>But Viterbi always returns a path</b> — <b>the most "
     "likely one, however unlikely</b> — so <b>it produces a gene "
     "model whether or not a gene is "
     "there.</b>",
     "",
     "<b>And a predicted gene is a hypothesis</b>, which is why "
     "annotations are flagged as predicted versus "
     "experimentally supported — and why that distinction gets "
     "lost downstream.",
     "",
     "<b>Which is Module 03 §4's chain again</b>: "
     "<b>prediction → annotation → cited fact</b>, with the "
     "qualifier dropped at each step.",
   ],
   "footnote": "<b>Viterbi always returns a path</b> — the most "
               "likely one, however unlikely — so the method cannot "
               "say 'there is nothing here' without being asked "
               "separately."},

  {"t": "callout", "title": "And the thing to carry forward",
   "kind": "Closing",
   "body": ["<b>HMMs are the clearest example in this course of a "
            "principled probabilistic model</b> — <b>the score is a "
            "likelihood, which means it composes and can be compared "
            "across models.</b>",
            "<b>And the recurrence is Module 02's</b>, which "
            "is why this module is short: <b>you already knew the "
            "algorithm</b>.",
            "<b>Plus the general caution:</b> <b>a model that always "
            "returns an answer needs a separate test for 'nothing "
            "here'</b> — <b>which is the null model "
            "question</b> (Module 03 §2) in a third "
            "setting.",
            "<b>So: log space, labelled training where possible, and "
            "a null to compare against</b> — three rules that cover "
            "most of what goes wrong."]},
 ],
 "takeaways": [
   "Viterbi is max and forward is sum, over the same recurrence — and "
   "that recurrence is Needleman-Wunsch's.",
   "Work in log space, and use log-sum-exp for the forward algorithm; these "
   "two bugs account for most broken HMM code.",
   "Baum-Welch converges to a local optimum, so initialisation matters and "
   "should be reported.",
   "A profile HMM encodes position-specific conservation, which a single "
   "substitution matrix cannot express.",
   "Iterated profile search can drift: a false hit incorporated into the "
   "profile recruits more like itself.",
   "Viterbi always returns a path, so a gene finder produces a model "
   "whether or not a gene is there.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The model"),
  ("eq", "states S, transitions a(i,j), emissions "
         "e<sub>i</sub>(x), initial distribution &pi;"),
  ("ul", ["<b>A Markov chain over hidden states, each of which emits "
          "an observable symbol</b> — <b>you see the symbols and "
          "the states are what you want</b>, which is the whole "
          "setup.",
          "<b>Decoding: find the single most likely state "
          "path</b> — <b>argmax over paths of P(path | "
          "sequence)</b> — <b>which is the Viterbi algorithm</b>, "
          "and is dynamic programming with exactly the "
          "max-over-predecessors structure of Module 02.",
          "<b>Evaluation: compute P(sequence), summed over all "
          "paths</b> — <b>the forward algorithm, which is the same "
          "recurrence with a sum in place of the max</b> — "
          "<b>and gives the likelihood, which is what scoring and model "
          "comparison need</b> (a single best path is not a "
          "likelihood).",
          "<b>Viterbi is max and forward is sum, over the same "
          "recurrence</b> — <b>which is the entire relationship "
          "between the two</b>, and once seen it cannot be unseen. "
          "<b>If you can write Needleman-Wunsch you can write "
          "Viterbi</b>, which is why this module is shorter than its "
          "importance suggests."]),
  ("callout", "And the third problem is learning the parameters, which is "
              "where it gets delicate",
   ["<b>Given sequences and no state labels, Baum-Welch (an instance "
    "of expectation-maximisation) estimates the transition and emission "
    "parameters</b> — <b>and converges to a local optimum</b> "
    "(CSCE 633 Module 07's EM material, with the same "
    "caveat).",
    "<b>So initialisation matters, and different starting points "
    "give genuinely different models</b> — <b>which should be "
    "reported and usually is not</b>, exactly as with any non-convex "
    "fit (CSCE 669 Module 04).",
    "<b>And with labelled data the estimation is just "
    "counting</b>, with pseudocounts added to avoid zero probabilities "
    "that would make unseen events impossible rather than "
    "rare — <b>which is far more reliable</b>, <b>and is what "
    "profile HMMs do</b> (&sect;3), since a curated family alignment "
    "supplies the labels.",
    "<b>Which is the general preference this program keeps "
    "arriving at:</b> <b>estimate from labelled examples wherever you "
    "have them</b>, <b>and treat unsupervised structure discovery as "
    "the weaker claim</b> (CSCE 676 Module 05's clustering "
    "caution)."]),

  ("h1", "2 &nbsp; Viterbi"),
  ("code", """v_k(i) = e_k(x_i) * max over j of [ v_j(i-1) * a(j,k) ]

    v_k(i)  the best probability of any path ending
            in state k having emitted the first i
            symbols
    traceback pointer: which j achieved the max

COMPARE Module 02:
    max over three predecessors -> max over states
    substitution score          -> emission prob
    gap penalty                 -> transition prob
    SAME SHAPE.

TWO RULES FOR IMPLEMENTING IT
    1  work in log space. Products of thousands of
       probabilities underflow to zero in double
       precision, silently and without warning.
    2  for the forward algorithm, summing in log
       space needs a log-sum-exp with the maximum
       factored out, or it overflows instead.

THESE TWO BUGS ACCOUNT FOR MOST BROKEN HMM CODE."""),
  ("p", "<b>Work in log space, and use log-sum-exp for the forward "
        "algorithm</b> — <b>these two bugs account for most broken "
        "HMM implementations</b>, and both fail silently: the underflow "
        "produces zeros that propagate, and the naive log-space sum "
        "produces infinities. Both are caught immediately by testing on a "
        "sequence long enough to underflow, which a toy example will "
        "not be."),

  ("break",),
  ("h1", "3 &nbsp; Profile HMMs"),
  ("callout", "A profile HMM encodes a family's position-specific "
              "conservation, which is strictly more information than any "
              "one sequence",
   ["<b>Match, insert, and delete states for each column of a family "
    "alignment</b> — <b>with position-specific emission "
    "probabilities and position-specific gap probabilities</b>, all "
    "estimated by counting from the alignment with pseudocounts.",
    "<b>So a position that is absolutely conserved across the "
    "family penalises a mismatch heavily, while a variable position "
    "penalises it barely at all</b> — <b>which a single global "
    "substitution matrix simply cannot express</b>, since it has one "
    "score per residue pair regardless of position (Module 03 "
    "&sect;1).",
    "<b>Which is why profile methods find remote homologues that "
    "pairwise BLAST misses</b> (Module 04 &sect;1's concentrated "
    "misses) — <b>the information is in the family, not in any "
    "individual member</b>, and no pairwise comparison can recover "
    "it.",
    "<b>And iterated search builds the profile as it goes</b>, "
    "adding each round's hits and re-searching — <b>which is "
    "powerful, and which can drift</b>: <b>a false hit incorporated "
    "into the profile recruits more sequences like itself</b>, and the "
    "profile walks away from the original family. <b>This is a "
    "specific, known, and still common failure</b>, and is why "
    "inclusion thresholds matter."]),

  ("h1", "4 &nbsp; Gene finding"),
  ("ul", ["<b>States for coding regions, introns, intergenic "
          "sequence, and the signal sites (start, stop, splice "
          "donors and acceptors)</b> — <b>and Viterbi labels every "
          "base of the input</b>, producing a complete and internally "
          "plausible annotation of the whole sequence.",
          "<b>It is very good at this</b>, and <b>it is how most "
          "genome annotation starts</b> — <b>which is exactly why "
          "the caveats matter</b>: a method this useful gets its output "
          "treated as data.",
          "<b>But Viterbi always returns a path</b> — <b>the "
          "most likely one, however unlikely in absolute terms</b> "
          "— so <b>it will produce a gene model whether or not "
          "there is a gene there</b>, and nothing in the output "
          "distinguishes the two cases without a separate likelihood "
          "comparison against a null model (Module 03 &sect;2).",
          "<b>And a predicted gene is a hypothesis</b>, which is "
          "<b>why annotation databases flag predicted versus "
          "experimentally supported entries</b> — <b>and why that "
          "distinction is routinely lost downstream</b>, when the "
          "identifier is cited without the flag.",
          "<b>Which is Module 03 &sect;4's chain "
          "again</b>: <b>prediction &rarr; database annotation &rarr; "
          "cited fact</b>, <b>with the qualifier dropped at each "
          "step</b> — and this is the same mechanism as annotation "
          "transfer by similarity, with a different first step."]),
  ("callout", "And the thing to carry forward",
   ["<b>HMMs are the clearest example in this course of a principled "
    "probabilistic model</b> — <b>the score is a likelihood, which "
    "means it composes, can be compared across models, and has a "
    "meaning independent of the scale somebody chose</b>, unlike an "
    "alignment score.",
    "<b>And the recurrence is Module 02's</b>, which is why this "
    "module is short relative to its importance: <b>you already knew the "
    "algorithm</b> and only had to learn what the quantities "
    "mean.",
    "<b>Plus the general caution:</b> <b>a model that always returns "
    "an answer needs a separate test for 'there is nothing here'</b> "
    "— <b>which is the null model question</b> (Module 03 "
    "&sect;2) <b>arriving in a third setting</b>, and will arrive again "
    "in Module 10.",
    "<b>So: log space, labelled training wherever possible, and a "
    "null to compare against</b> — <b>three rules that cover most "
    "of what goes wrong</b> with these models in practice."]),
 ],
 "resources": [
   ("Durbin et al., chapters 3 to 5 (library copy)",
    "https://www.cambridge.org/9780521629713",
    "<b>The whole module</b> — and the profile HMM chapters are the "
    "definitive treatment."),
   ("Rabiner &mdash; A tutorial on hidden Markov models (free copies "
    "widely available)",
    "https://ieeexplore.ieee.org/document/18626",
    "<b>&sect;&sect;1 and 2</b> — the three problems stated clearly, "
    "from speech recognition."),
   ("Eddy &mdash; What is a hidden Markov model? (free)",
    "https://www.nature.com/articles/nbt1004-1315",
    "<b>&sect;1</b> in two pages — the best short explanation "
    "there is."),
   ("The HMMER documentation and Pfam (free)",
    "http://hmmer.org/",
    "<b>&sect;3</b> — profile HMMs as working software, and Pfam is "
    "the family database built from them."),
 ],
 "exercises": [
   "<b>Define an HMM</b> for a two-state toy problem.",
   "<b>Run Viterbi by hand</b> on a five-symbol sequence.",
   "<b>Implement Viterbi</b> in log space.",
   "<b>Implement it without logs</b> and find the sequence length at "
   "which it underflows.",
   "<b>Implement the forward algorithm</b> with log-sum-exp.",
   "<b>Train with Baum-Welch</b> from three different "
   "initialisations.",
   "<b>Build a profile HMM</b> from a small aligned family.",
   "<b>Compare its hits</b> to BLAST's on the same database.",
   "<b>Run an iterated search</b> and watch for drift.",
   "<b>Run a gene finder on random sequence</b> and count the genes it "
   "predicts.",
 ],
 "selfcheck": [
   "Define an HMM's components.",
   "State the three standard problems.",
   "Give the Viterbi recurrence and map it onto Needleman-Wunsch.",
   "What is the relationship between Viterbi and forward?",
   "State the two implementation rules and what each bug looks like.",
   "Why does Baum-Welch need its initialisation reported?",
   "What does a profile HMM capture that a matrix cannot?",
   "Why do profiles find remote homologues, and how do they drift?",
   "What does a gene finder always do, and why is that a problem?",
   "State the three closing rules.",
 ],
},

]
