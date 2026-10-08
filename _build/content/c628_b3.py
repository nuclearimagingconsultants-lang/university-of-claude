# -*- coding: utf-8 -*-
"""CSCE 628 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "RNA Structure",
 "subtitle": "Dynamic programming on intervals, and a model that is "
             "honestly incomplete.",
 "question": "What shape does this sequence fold into?",
 "outcomes": [
     "Explain the folding problem and the base-pairing model.",
     "Derive the Nussinov recurrence.",
     "Explain energy minimisation and why it is better.",
     "Explain pseudoknots and why they are excluded.",
     "State what a predicted structure establishes.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "And why RNA structure is worth predicting."},

  {"t": "callout", "title": "RNA folds back on itself, and the shape determines what it does",
   "kind": "The setup",
   "body": ["<b>Complementary bases pair: A with U, G with C, and G "
            "with U more weakly</b> — <b>and a single strand pairs "
            "with itself</b>, producing stems, loops, and "
            "bulges.",
            "<b>Which matters because structure is "
            "function</b> — <b>for ribosomal and transfer RNA, for "
            "regulatory elements, and for the many non-coding RNAs "
            "whose role is structural.</b>",
            "<b>And structure is conserved where sequence is "
            "not</b> — <b>compensatory mutations preserve a pair while "
            "changing both bases</b>, which is evidence of function "
            "that sequence comparison misses.",
            "<b>So the computational problem is: given a sequence, "
            "predict the set of pairs</b> — <b>which is a "
            "combinatorial optimisation with a physically motivated "
            "objective.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Nussinov",
   "blurb": "The simplest version, and the recurrence worth deriving."},

  {"t": "eq", "kicker": "Nussinov", "title": "Maximise the number of pairs",
   "eqs": [
     ("N(i,j) = max over four cases, on the interval i..j",
      "The subproblem is an interval rather than a prefix — which "
      "is the structural difference from Module 02."),
     ("N(i+1,j),  N(i,j−1),  N(i+1,j−1) + δ(i,j)",
      "Leave i unpaired, leave j unpaired, or pair i with j "
      "(δ = 1 if they can pair)."),
     ("max over k of N(i,k) + N(k+1,j)   — bifurcation",
      "Split the interval in two. This case is what makes it "
      "O(n³) rather than O(n²), and it is the one people forget."),
   ],
   "caption": "<b>The bifurcation case is what makes it cubic</b>, "
              "and it is the case most often omitted in a first "
              "implementation.",
   "note": "Intervals rather than prefixes: that is the whole "
           "structural difference."},

  {"t": "callout", "title": "And maximising pair count is the wrong objective, which the next model fixes",
   "kind": "Why Nussinov is a teaching algorithm",
   "body": ["<b>Pairs do not contribute equally</b> — <b>stacked "
            "pairs in a helix are stabilising and isolated pairs are "
            "not</b> — so counting pairs rewards structures that do "
            "not form.",
            "<b>So Zuker's algorithm minimises free energy "
            "instead</b>, <b>with experimentally measured parameters "
            "for stacking, loops, and bulges</b> — same interval "
            "decomposition, better objective.",
            "<b>Which is a good example of the "
            "pattern:</b> <b>the algorithm was easy and the scoring "
            "function was the research</b> — exactly as in "
            "Module 03 §1.",
            "<b>And the energy parameters are measured, which makes "
            "the prediction physically grounded</b> — <b>within the "
            "model's assumptions</b>, which "
            "Part 3 names."]},

  {"t": "section", "label": "Part 3", "title": "What the model excludes",
   "blurb": "Explicitly, because the exclusion is load-bearing."},

  {"t": "bullets", "kicker": "Assumptions", "title": "The assumptions that make the recurrence work",
   "items": [
     "<b>No pseudoknots</b> — <b>pairs may not cross</b>, "
     "which is what makes the interval decomposition valid — and "
     "<b>pseudoknots exist and are functionally "
     "important</b>.",
     "",
     "<b>Allowing them makes the problem NP-hard</b> in general, "
     "so the exclusion is not laziness — and specialised heuristics "
     "handle restricted classes.",
     "",
     "<b>One sequence, one structure</b> — <b>whereas real "
     "RNA interconverts between conformations</b>, and some regulatory "
     "elements work precisely by switching.",
     "",
     "<b>No ligands, no proteins, no ions</b> — <b>and "
     "magnesium in particular stabilises structures the model cannot "
     "see</b>.",
     "",
     "<b>And the minimum free energy structure is frequently not "
     "the one that forms</b> — <b>which is why the partition "
     "function and base-pair probabilities are reported "
     "instead.</b>",
   ],
   "footnote": "<b>The minimum free energy structure is frequently "
               "not the one that forms</b> — so report base-pair "
               "probabilities from the partition function rather than a "
               "single structure."},

  {"t": "section", "label": "Part 4", "title": "Doing better",
   "blurb": "With comparative evidence."},

  {"t": "callout", "title": "Comparative folding beats single-sequence folding, because conservation is evidence the energy model is not",
   "kind": "Closing",
   "body": ["<b>If several related sequences fold to the same "
            "structure, and compensatory mutations preserve pairs, that "
            "is independent evidence</b> — <b>which the energy model "
            "does not provide.</b>",
            "<b>So the better methods fold an alignment rather than "
            "a sequence</b>, combining thermodynamics with covariation "
            "— and they are measurably more "
            "accurate.",
            "<b>Which is the same move as "
            "Module 07 §3's profiles</b>: <b>the family carries "
            "information no member does</b>, in a second "
            "setting.",
            "<b>And the honest claim is:</b> <b>'the minimum free "
            "energy structure under this parameter set, with these "
            "base-pair probabilities'</b> — <b>not 'the structure of "
            "this RNA'</b>, which requires an "
            "experiment."]},
 ],
 "takeaways": [
   "Structure is conserved where sequence is not, and compensatory "
   "mutations are evidence of function that sequence comparison misses.",
   "The subproblem is an interval rather than a prefix, which is the "
   "structural difference from alignment.",
   "The bifurcation case makes the recurrence cubic and is the one most "
   "often omitted.",
   "Maximising pair count is the wrong objective; the algorithm was easy "
   "and the scoring function was the research.",
   "No pseudoknots is what makes the decomposition valid, and allowing them "
   "makes the problem NP-hard.",
   "The minimum free energy structure is frequently not the one that forms, "
   "so report base-pair probabilities.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The problem"),
  ("callout", "RNA folds back on itself, and the shape determines what it "
              "does",
   ["<b>Complementary bases pair — A with U, G with C, and G "
    "with U more weakly</b> — <b>and a single strand pairs with "
    "itself</b>, producing stems (stacked pairs), hairpin loops, "
    "internal loops, and bulges.",
    "<b>Which matters because structure is function</b> — "
    "<b>for ribosomal and transfer RNA, for regulatory elements in "
    "untranslated regions, and for the many non-coding RNAs whose entire "
    "role is structural</b> rather than informational.",
    "<b>And structure is conserved where sequence is not</b> "
    "— <b>compensatory mutations preserve a pair while changing "
    "both of its bases</b> (a G-C becomes an A-U) — <b>which is "
    "evidence of function that plain sequence comparison misses "
    "entirely</b>, and which &sect;4 exploits.",
    "<b>So the computational problem is: given a sequence, predict "
    "the set of pairs</b> — <b>which is a combinatorial "
    "optimisation with a physically motivated objective</b>, and is "
    "therefore unusually well posed for this field."]),

  ("h1", "2 &nbsp; Nussinov"),
  ("eq", "N(i,j) = max { N(i+1,j),&nbsp; N(i,j&minus;1),&nbsp; "
         "N(i+1,j&minus;1) + &delta;(i,j),&nbsp; "
         "max<sub>k</sub> [ N(i,k) + N(k+1,j) ] }"),
  ("ul", ["<b>The subproblem is an interval i..j rather than a pair "
          "of prefixes</b> — <b>which is the structural difference "
          "from Module 02</b>, and is what makes the fill order "
          "by increasing interval length rather than by row.",
          "<b>The first three cases: leave i unpaired, leave j "
          "unpaired, or pair i with j</b> (with &delta; = 1 if those two "
          "bases can pair and 0 otherwise) — <b>which is the "
          "max-of-cases structure you already know.</b>",
          "<b>The fourth case is bifurcation: split the interval at "
          "some k and add the two halves' scores</b> — <b>which is "
          "what makes the algorithm O(n<sup>3</sup>) rather than "
          "O(n<sup>2</sup>)</b>, since it introduces a loop over "
          "k.",
          "<b>The bifurcation case is what makes it cubic, and it is "
          "the case most often omitted in a first "
          "implementation</b> — producing an algorithm that cannot "
          "represent two independent stems side by side, which is a "
          "quiet and plausible-looking failure. <b>Intervals rather "
          "than prefixes: that is the whole structural "
          "difference.</b>"]),
  ("callout", "And maximising pair count is the wrong objective, which the "
              "next model fixes",
   ["<b>Pairs do not contribute equally to stability</b> — "
    "<b>stacked pairs within a helix are strongly stabilising and "
    "isolated pairs are essentially not</b> — <b>so counting pairs "
    "rewards structures that would never form</b>, scattering single "
    "pairs across the molecule.",
    "<b>So Zuker's algorithm minimises free energy instead</b>, "
    "<b>with experimentally measured parameters for stacking, for loops "
    "of each type and size, and for bulges</b> — <b>the same "
    "interval decomposition with a much better objective</b>, and more "
    "cases to handle.",
    "<b>Which is a good example of the pattern this course keeps "
    "meeting:</b> <b>the algorithm was the easy part and the scoring "
    "function was the research</b> — <b>exactly as in "
    "Module 03 &sect;1</b>, where the recurrence was 1970 and the "
    "matrices were two decades of work.",
    "<b>And the energy parameters are measured in the laboratory, "
    "which makes the prediction physically grounded</b> rather than "
    "merely consistent — <b>within the model's assumptions</b>, "
    "<b>which &sect;3 names explicitly</b> because they are "
    "load-bearing."]),

  ("break",),
  ("h1", "3 &nbsp; What the model excludes"),
  ("ul", ["<b>No pseudoknots</b> — <b>pairs may not cross</b> "
          "(if i pairs with j and k with l, then either both of k,l lie "
          "inside i..j or both lie outside) — <b>which is exactly "
          "what makes the interval decomposition valid</b>, and "
          "<b>pseudoknots exist and are functionally important</b>, "
          "including in several viral elements.",
          "<b>Allowing them in general makes the problem "
          "NP-hard</b>, <b>so the exclusion is a real algorithmic "
          "constraint rather than laziness</b> — and specialised "
          "heuristics handle restricted pseudoknot classes at higher "
          "cost.",
          "<b>One sequence, one structure</b> — <b>whereas real "
          "RNA interconverts between conformations</b>, and <b>some "
          "regulatory elements work precisely by switching</b> between "
          "two structures in response to a ligand or a temperature "
          "change, which the model cannot represent at all.",
          "<b>No ligands, no proteins, no ions</b> — and "
          "<b>magnesium in particular stabilises tertiary structures "
          "that the model cannot see</b>, so predictions for structured "
          "RNAs in their biological context are systematically "
          "incomplete.",
          "<b>And the minimum free energy structure is frequently not "
          "the one that forms</b> — the energy landscape is "
          "shallow and folding is kinetic — <b>which is why the "
          "partition function and the resulting base-pair probabilities "
          "are the better thing to report</b> than a single structure "
          "(McCaskill's algorithm computes them with the same "
          "decomposition and sum in place of max, exactly as "
          "Module 07 &sect;1's forward relates to Viterbi)."]),

  ("h1", "4 &nbsp; Doing better"),
  ("callout", "Comparative folding beats single-sequence folding, because "
              "conservation is evidence the energy model is not",
   ["<b>If several related sequences fold to the same structure, and "
    "compensatory mutations preserve the pairs while changing the "
    "bases, that is independent evidence that the structure is "
    "real</b> — <b>which the thermodynamic model does not and "
    "cannot provide</b>, since it would predict a structure for random "
    "sequence too.",
    "<b>So the better methods fold an alignment rather than a single "
    "sequence</b>, combining thermodynamic scores with a covariation "
    "term — <b>and they are measurably more accurate</b> on "
    "benchmarks of known structures, by a wide margin for structured "
    "families.",
    "<b>Which is the same move as Module 07 &sect;3's profile "
    "HMMs</b>: <b>the family carries information that no individual "
    "member does</b> — <b>in a second setting</b>, and it is worth "
    "noticing as a general principle rather than two tricks.",
    "<b>And the honest claim is:</b> <b>'the minimum free energy "
    "structure under this parameter set, with these base-pair "
    "probabilities'</b> — <b>not 'the structure of this RNA'</b>, "
    "<b>which requires an experiment</b> (Module 01 &sect;4's "
    "no-ground-truth position, and Module 13's claim form)."]),
 ],
 "resources": [
   ("Durbin et al., chapter 10 (library copy)",
    "https://www.cambridge.org/9780521629713",
    "<b>&sect;&sect;2 and 4</b> — RNA structure, including stochastic "
    "context-free grammars, which is the unifying framing."),
   ("Zuker &mdash; Mfold web server for nucleic acid folding (free)",
    "https://academic.oup.com/nar/article/31/13/3406/2904101",
    "<b>&sect;2's energy minimisation</b> — and the server is worth "
    "running on a sequence you care about."),
   ("Lorenz et al. &mdash; ViennaRNA Package 2.0 (free)",
    "https://almob.biomedcentral.com/articles/10.1186/1748-7188-6-26",
    "<b>&sect;&sect;3 and 4</b> — partition function, base-pair "
    "probabilities, and comparative folding, as working "
    "software."),
   ("Mathews et al. &mdash; the nearest-neighbour energy parameters",
    "https://pubmed.ncbi.nlm.nih.gov/10329189/",
    "<b>&sect;2's measured parameters</b> — where the numbers come "
    "from, which is laboratory work rather than computation."),
 ],
 "exercises": [
   "<b>Pair a short sequence by hand</b> and draw the structure.",
   "<b>Write the Nussinov recurrence</b> with all four cases.",
   "<b>Implement it</b>, filling by increasing interval length.",
   "<b>Omit the bifurcation case</b> and find a sequence where it "
   "matters.",
   "<b>Compare Nussinov's output to an energy minimiser's</b> on the "
   "same sequence.",
   "<b>Construct a pseudoknot</b> and confirm the recurrence cannot "
   "represent it.",
   "<b>Fold a known tRNA</b> and compare to its published "
   "structure.",
   "<b>Compute base-pair probabilities</b> and compare to the single "
   "MFE structure.",
   "<b>Fold an alignment of a conserved family</b> and compare to "
   "folding one member.",
   "<b>Find a compensatory mutation</b> in that alignment.",
 ],
 "selfcheck": [
   "Why does RNA structure matter, and what is conserved?",
   "What is the subproblem, and how does that differ from alignment?",
   "Give the four cases, and say which makes it cubic.",
   "Why is maximising pairs the wrong objective?",
   "What replaced it, and where did its parameters come from?",
   "What general pattern does that illustrate?",
   "State five assumptions the model makes.",
   "Why are pseudoknots excluded?",
   "Why report base-pair probabilities?",
   "Why does comparative folding work better?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Protein Structure",
 "subtitle": "The problem that changed, and the parts that did not.",
 "question": "Does a predicted structure tell you what the protein "
             "does?",
 "outcomes": [
     "State the folding problem and why it was hard.",
     "Describe the classical approaches and their limits.",
     "Explain what learned predictors changed.",
     "State honestly what remains unsolved.",
     "Interpret a predicted structure and its confidence.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "And why it resisted for fifty years."},

  {"t": "callout", "title": "The sequence determines the structure, and the mapping was not computable",
   "kind": "The classical statement",
   "body": ["<b>Anfinsen's experiment showed a denatured protein "
            "refolds to the same structure</b> — <b>so the information "
            "is in the sequence</b>, which made prediction a "
            "well-posed goal.",
            "<b>And the search space is "
            "astronomical</b> — <b>Levinthal's point: random search "
            "would take longer than the universe's "
            "age</b>, yet folding takes "
            "milliseconds, so the landscape must be "
            "funnelled.",
            "<b>Physical simulation from first principles was "
            "attempted for decades</b> — <b>and the force fields were "
            "not accurate enough over the required timescales</b>, "
            "which is an honest summary.",
            "<b>So the field split:</b> <b>homology modelling where "
            "a related structure existed, and threading or fragment "
            "assembly where one did not</b> — both of which used "
            "known structures as the real "
            "information."]},

  {"t": "section", "label": "Part 2", "title": "What changed",
   "blurb": "And what the change actually consisted of."},

  {"t": "callout", "title": "Learned predictors reached experimental accuracy for many proteins, using coevolution as the key signal",
   "kind": "The result, stated carefully",
   "body": ["<b>Residues that contact each other coevolve</b> — "
            "<b>a substitution at one is compensated at the "
            "other</b> — so <b>a deep alignment of a family contains "
            "contact information</b>, which is "
            "Module 08 §4's covariation in three "
            "dimensions.",
            "<b>Extracting it required disentangling direct from "
            "indirect correlations</b>, which was the key methodological "
            "step before the learned models — and it worked before "
            "deep learning did.",
            "<b>And the deep models combined that signal with "
            "learned structural priors and end-to-end "
            "training</b> — <b>reaching accuracy comparable to "
            "experiment for a large fraction of "
            "targets</b>.",
            "<b>Which is a genuine and large "
            "result</b> — <b>and it is a result about structure "
            "prediction, which is narrower than 'the folding problem is "
            "solved'</b> (Part 3)."]},

  {"t": "section", "label": "Part 3", "title": "What remains",
   "blurb": "Which is more than the headlines suggested."},

  {"t": "bullets", "kicker": "Open", "title": "What a structure predictor does not give you",
   "items": [
     "<b>The folding <i>process</i></b> — <b>the predictors "
     "produce a structure without simulating how it is "
     "reached</b>, so misfolding and folding kinetics are "
     "untouched.",
     "",
     "<b>Proteins without deep alignments</b> — <b>accuracy "
     "depends on the family's depth</b>, so orphan sequences and "
     "designed proteins are much harder.",
     "",
     "<b>Disordered regions</b>, which have no single "
     "structure — <b>and the predictors flag them with low "
     "confidence, which is the right behaviour</b> and is often "
     "ignored.",
     "",
     "<b>Complexes, conformational change, and ligand-bound "
     "states</b> — <b>a protein's function frequently <i>is</i> "
     "its motion between states</b>.",
     "",
     "<b>And function</b> — <b>a structure is not a mechanism, "
     "and predicting the fold does not predict what it does</b> "
     "(Module 03 §4's chain).",
   ],
   "footnote": "<b>A structure is not a mechanism</b> — and the "
               "distance from a predicted fold to a biological claim is "
               "the same distance this course has been measuring "
               "throughout."},

  {"t": "section", "label": "Part 4", "title": "Reading a prediction",
   "blurb": "With its confidence attached."},

  {"t": "callout", "title": "A predicted structure comes with per-residue confidence, and using it without the confidence is the error",
   "kind": "Closing",
   "body": ["<b>The predictors emit a per-residue confidence "
            "score</b> — <b>and low-confidence regions are frequently "
            "disordered rather than merely uncertain</b>, which is "
            "information rather than a "
            "disclaimer.",
            "<b>So a figure showing the whole predicted structure at "
            "equal visual weight is misleading</b> — <b>colour by "
            "confidence, which the standard viewers "
            "do</b> (CSCE 679 §09).",
            "<b>And predicted structures are now in the "
            "databases</b>, alongside experimental ones — <b>so the "
            "predicted-versus-measured distinction has to travel with "
            "the identifier</b>, and it is "
            "Module 07 §4's problem at "
            "scale.",
            "<b>Which is this module's version of the "
            "rule:</b> <b>'the predicted structure, with this "
            "confidence, from this model version'</b> — <b>three "
            "things, and a citation usually gives "
            "none.</b>"]},
 ],
 "takeaways": [
   "Anfinsen showed the information is in the sequence; Levinthal showed "
   "the landscape must be funnelled.",
   "Physical simulation from first principles was attempted for decades and "
   "the force fields were not accurate enough.",
   "Residues in contact coevolve, so a deep family alignment contains "
   "contact information — covariation in three dimensions.",
   "Structure prediction reaching experimental accuracy is narrower than "
   "'the folding problem is solved'.",
   "Accuracy depends on alignment depth, so orphan and designed proteins "
   "remain hard.",
   "A structure is not a mechanism, and predicting the fold does not "
   "predict the function.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The problem"),
  ("callout", "The sequence determines the structure, and the mapping was not "
              "computable",
   ["<b>Anfinsen's experiment showed that a denatured protein "
    "refolds to the same structure without assistance</b> — <b>so "
    "the information required is present in the sequence</b>, <b>which "
    "made prediction a well-posed goal</b> rather than a hope, and is "
    "why the problem was stated so confidently so early.",
    "<b>And the search space is astronomical</b> — "
    "<b>Levinthal's point: a random search over conformations would take "
    "longer than the age of the universe</b>, <b>and yet folding takes "
    "milliseconds</b> — <b>so the energy landscape must be "
    "funnelled</b> toward the native state rather than flat.",
    "<b>Physical simulation from first principles was attempted for "
    "decades</b>, with enormous computational investment — <b>and "
    "the force fields were not accurate enough to remain correct over "
    "the required timescales</b>, with small errors accumulating, "
    "<b>which is an honest summary of why it did not work.</b>",
    "<b>So the field split in practice:</b> <b>homology modelling "
    "where a related structure had been solved experimentally, and "
    "threading or fragment assembly where one had not</b> — "
    "<b>both of which used the database of known structures as the "
    "actual source of information</b>, rather than physics."]),

  ("h1", "2 &nbsp; What changed"),
  ("callout", "Learned predictors reached experimental accuracy for many "
              "proteins, using coevolution as the key signal",
   ["<b>Residues that are in physical contact coevolve</b> — "
    "<b>a destabilising substitution at one position is compensated by a "
    "substitution at its partner</b> — so <b>a sufficiently deep "
    "alignment of a protein family contains information about which "
    "residues touch</b>, which is <b>Module 08 &sect;4's covariation "
    "argument in three dimensions.</b>",
    "<b>Extracting that signal required disentangling direct "
    "contacts from indirect correlations</b> (A correlates with C merely "
    "because both contact B) — <b>which was the key methodological "
    "step, and it produced usable contact predictions before deep "
    "learning was applied</b>, a piece of history worth "
    "keeping.",
    "<b>And the deep models combined that coevolutionary signal "
    "with learned structural priors and end-to-end training against "
    "known structures</b> — <b>reaching accuracy comparable to "
    "experimental determination for a large fraction of targets</b> in "
    "blind assessment, which is the strongest possible form of the "
    "claim.",
    "<b>Which is a genuine and large result</b> — one of the "
    "clearest successes of machine learning on a scientific "
    "problem — <b>and it is a result about structure prediction, "
    "which is narrower than 'the folding problem is solved'</b> "
    "(&sect;3 lists what it does not cover)."]),

  ("break",),
  ("h1", "3 &nbsp; What remains"),
  ("ul", ["<b>The folding <i>process</i></b> — <b>the "
          "predictors produce a final structure without simulating how "
          "it is reached</b> — so <b>misfolding, folding kinetics, "
          "chaperone dependence, and aggregation are untouched</b>, and "
          "those are where several diseases are.",
          "<b>Proteins without deep alignments</b> — "
          "<b>accuracy depends substantially on the depth of the "
          "available family alignment</b>, since that is where the "
          "coevolutionary signal comes from — so <b>orphan "
          "sequences, rapidly evolving proteins, and designed proteins "
          "are considerably harder.</b>",
          "<b>Intrinsically disordered regions</b>, which have no "
          "single native structure at all — <b>and the predictors "
          "flag them with low confidence, which is exactly the right "
          "behaviour</b> <b>and is frequently ignored by the people "
          "using the output</b> (&sect;4).",
          "<b>Complexes, conformational change, and ligand-bound "
          "states</b> — <b>a protein's function frequently "
          "<i>is</i> its motion between states</b>, and a single static "
          "prediction cannot express that however accurate it is.",
          "<b>And function</b> — <b>a structure is not a "
          "mechanism, and predicting the fold does not predict what the "
          "protein does</b> (Module 03 &sect;4's chain: structure is "
          "one more link, not the destination). <b>The distance from a "
          "predicted fold to a biological claim is the same distance "
          "this course has been measuring throughout.</b>"]),

  ("h1", "4 &nbsp; Reading a prediction"),
  ("callout", "A predicted structure comes with per-residue confidence, and "
              "using it without the confidence is the error",
   ["<b>The predictors emit a per-residue confidence score alongside "
    "the coordinates</b> — and <b>low-confidence regions are "
    "frequently genuinely disordered rather than merely "
    "uncertain</b>, <b>which makes the score information rather than a "
    "disclaimer</b> and is a point worth making to anyone using the "
    "output.",
    "<b>So a figure showing the whole predicted structure at equal "
    "visual weight is misleading</b> — <b>colour by confidence, "
    "which the standard viewers do by default</b> — and this is "
    "<b>CSCE 679 Module 09's uncertainty requirement</b> in a field "
    "where the uncertainty is supplied for free and discarded "
    "anyway.",
    "<b>And predicted structures are now deposited in public "
    "databases alongside experimentally determined ones</b> — "
    "<b>so the predicted-versus-measured distinction has to travel with "
    "the identifier</b>, <b>which is Module 07 &sect;4's "
    "predicted-annotation problem at a much larger scale</b> and with "
    "the same mechanism of loss.",
    "<b>Which is this module's version of the program's "
    "rule:</b> <b>'the predicted structure, at this confidence, from "
    "this model version'</b> — <b>three things</b>, <b>and a "
    "citation in a paper usually gives none of them.</b>"]),
 ],
 "resources": [
   ("Anfinsen &mdash; Principles that govern the folding of protein "
    "chains",
    "https://www.science.org/doi/10.1126/science.181.4096.223",
    "<b>&sect;1</b> — the experiment that made the problem well "
    "posed."),
   ("Marks et al. &mdash; Protein structure prediction from sequence "
    "variation (free)",
    "https://www.nature.com/articles/nbt.2419",
    "<b>&sect;2's coevolution signal</b>, before the deep models — "
    "and it is the conceptual core of what followed."),
   ("Jumper et al. &mdash; Highly accurate protein structure "
    "prediction with AlphaFold (free)",
    "https://www.nature.com/articles/s41586-021-03819-2",
    "<b>&sect;2</b> — the method paper, and its own limitations "
    "section is the model for &sect;3."),
   ("The CASP assessments (free)",
    "https://predictioncenter.org/",
    "<b>&sect;&sect;2 and 3</b> — blind assessment over three "
    "decades, which is how the claim was established and is the "
    "right evidence to cite."),
 ],
 "exercises": [
   "<b>State Anfinsen's result</b> and what it licensed.",
   "<b>State Levinthal's paradox</b> and its resolution.",
   "<b>Explain why physical simulation did not succeed.</b>",
   "<b>Explain coevolution as a contact signal</b> in four "
   "sentences.",
   "<b>Explain direct versus indirect correlation</b> with a "
   "three-residue example.",
   "<b>Fetch a predicted structure</b> and colour it by confidence.",
   "<b>Find a low-confidence region</b> and check whether it is "
   "predicted disordered.",
   "<b>Find a protein with a shallow alignment</b> and compare its "
   "prediction quality.",
   "<b>List five things a predicted structure does not tell "
   "you.</b>",
   "<b>Write a citation</b> that names the structure, the confidence, "
   "and the model version.",
 ],
 "selfcheck": [
   "What did Anfinsen show, and why did it matter?",
   "State Levinthal's paradox and what it implies about the "
   "landscape.",
   "Why did first-principles simulation fail?",
   "What did the field do instead?",
   "What is the coevolution signal, and what had to be disentangled?",
   "State the result carefully, and what it is narrower than.",
   "Name five things that remain open.",
   "Why is low confidence information rather than a disclaimer?",
   "What should a figure of a prediction do?",
   "What three things should a citation name?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Expression and Multiple Testing",
 "subtitle": "Where the computation is easy and the inference is "
             "where everything goes wrong.",
 "question": "You tested twenty thousand genes. How many are "
             "significant by chance?",
 "outcomes": [
     "Explain what expression data is and why normalisation matters.",
     "Explain the count model and the small-sample problem.",
     "Apply multiple testing correction and explain the choice.",
     "Explain batch effects and how to detect them.",
     "Analyse an expression dataset defensibly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The data",
   "blurb": "And why raw counts are not comparable."},

  {"t": "callout", "title": "A count depends on expression, on transcript length, and on how much was sequenced",
   "kind": "Why normalisation is mandatory rather than optional",
   "body": ["<b>Twice as many reads for a gene may mean twice the "
            "expression, a transcript twice as long, or a library "
            "sequenced twice as deeply</b> — and <b>the raw number "
            "does not distinguish them.</b>",
            "<b>So normalisation by library size is "
            "mandatory</b>, and <b>by length when comparing genes "
            "within a sample</b> — <b>not when comparing one gene "
            "across samples</b>, which is a distinction worth getting "
            "right.",
            "<b>And composition matters:</b> <b>if one gene "
            "dominates a sample, every other gene's share falls</b> "
            "— so <b>simple proportions mislead</b>, and the robust "
            "methods estimate a size factor "
            "instead.",
            "<b>Which is CSCE 679 §08 §3's normalisation "
            "argument</b> — <b>a count map is a population "
            "map</b> — <b>arriving in a field where the denominator "
            "is itself estimated.</b>"]},

  {"t": "section", "label": "Part 2", "title": "The model",
   "blurb": "And the problem of three replicates."},

  {"t": "bullets", "kicker": "Modelling", "title": "What differential expression analysis actually does",
   "items": [
     "<b>Counts are modelled as negative binomial</b> — "
     "<b>Poisson plus extra variance</b> — because biological "
     "replicates vary more than counting noise "
     "alone.",
     "",
     "<b>And the variance must be estimated per gene from "
     "three replicates</b>, which is hopeless on its own — so "
     "<b>the methods share information across genes</b>, shrinking each "
     "estimate toward a fitted trend.",
     "",
     "<b>Which is the key statistical idea in the "
     "field</b> — <b>borrowing strength across thousands of "
     "parallel tests</b> — and it works well and is an "
     "assumption.",
     "",
     "<b>Then a test per gene, and a p-value per "
     "gene</b> — twenty thousand of them, which is "
     "Part 3.",
     "",
     "<b>And the effect size matters as much as the "
     "p-value</b>: <b>a tiny fold change can be highly significant "
     "with enough samples</b>, and significance is not "
     "importance.",
   ],
   "footnote": "<b>Shrinking per-gene variance estimates toward a "
               "fitted trend is the key statistical idea here</b> "
               "— borrowing strength across thousands of parallel "
               "tests."},

  {"t": "section", "label": "Part 3", "title": "Multiple testing",
   "blurb": "The arithmetic, which is not optional."},

  {"t": "code", "kicker": "Correction", "title": "What twenty thousand tests costs you",
   "lang": "text", "code": """
  THE ARITHMETIC
      20,000 tests at alpha = 0.05
      => 1,000 expected false positives
      if you report 1,200 "significant" genes, most
      of your list is noise.

  BONFERRONI
      use alpha / m. Controls the probability of ANY
      false positive (family-wise error rate).
      Correct, and far too strict here: you will
      find almost nothing.

  BENJAMINI-HOCHBERG
      controls the FALSE DISCOVERY RATE: the
      expected PROPORTION of your reported list that
      is false. q = 0.05 means ~5% of your hits are
      expected to be wrong.
      Which is the right target for a screen whose
      output is a list for follow-up.

  AND THE COUNT OF TESTS MUST INCLUDE THE ONES YOU
  RAN AND DISCARDED. Everybody omits those.
""",
   "caption": "<b>The count of tests must include the ones you ran "
              "and discarded</b> — which everybody omits, and which "
              "is the honest part of the "
              "correction.",
   "note": "FDR for screens, FWER when a single false positive is "
           "costly."},

  {"t": "section", "label": "Part 4", "title": "Batch effects",
   "blurb": "The failure that produced a replication crisis."},

  {"t": "callout", "title": "If your cases and controls were processed on different days, you cannot separate biology from batch",
   "kind": "The most consequential design error in the field",
   "body": ["<b>Processing date, technician, reagent lot, and "
            "instrument all produce systematic differences</b> "
            "— <b>frequently larger than the biological effect you "
            "are looking for.</b>",
            "<b>And if batch is confounded with the condition, no "
            "statistical method can separate them</b> — <b>the "
            "information is not in the data</b>, which is "
            "Module 05 §3's kind of limit in a "
            "statistical setting.",
            "<b>So the fix is in the design:</b> <b>randomise or "
            "balance samples across batches</b>, and <b>record the "
            "batch metadata</b>, which is free and is often not "
            "done.",
            "<b>And the detection is cheap:</b> <b>cluster the "
            "samples and colour by batch</b> — <b>if they separate by "
            "batch rather than by condition, you have your "
            "answer</b> before any testing."]},

  {"t": "callout", "title": "And the general shape of this module",
   "kind": "Closing",
   "body": ["<b>The computation here is trivial and the inference is "
            "where everything fails</b> — <b>which is the opposite of "
            "Modules 02 to 09</b> and is why this module is placed "
            "after them.",
            "<b>And the failures are "
            "systematic:</b> <b>unnormalised counts, uncorrected "
            "testing, and confounded batches</b> — <b>three named "
            "errors that account for a large share of irreproducible "
            "findings.</b>",
            "<b>All three are detectable in an afternoon</b> by "
            "somebody who knows to look — which is the practical "
            "value of this module.",
            "<b>So: normalise, correct, and plot the samples "
            "coloured by batch before anything "
            "else</b> — <b>three steps, and Project 2 requires all "
            "three.</b>"]},
 ],
 "takeaways": [
   "A count depends on expression, transcript length, and sequencing depth, "
   "so normalisation is mandatory.",
   "Normalise by length when comparing genes within a sample, not when "
   "comparing one gene across samples.",
   "Shrinking per-gene variance toward a fitted trend borrows strength "
   "across thousands of parallel tests.",
   "20,000 tests at alpha 0.05 gives 1,000 expected false positives; FDR is "
   "the right target for a screen.",
   "The count of tests must include the ones you ran and discarded, which "
   "everybody omits.",
   "If batch is confounded with condition, no method can separate them "
   "— the information is not in the data.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The data"),
  ("callout", "A count depends on expression, on transcript length, and on "
              "how much was sequenced",
   ["<b>Twice as many reads assigned to a gene may mean twice the "
    "expression, a transcript twice as long, or a library that was "
    "sequenced twice as deeply</b> — and <b>the raw number does not "
    "distinguish between them</b>, which makes it uninterpretable on its "
    "own.",
    "<b>So normalisation by library size is mandatory</b>, and "
    "<b>normalisation by transcript length is needed when comparing "
    "different genes within one sample</b> — <b>but not when "
    "comparing the same gene across samples</b>, where the length is "
    "constant and dividing by it only adds noise. <b>That distinction "
    "is worth getting right</b> and is got wrong often.",
    "<b>And composition matters:</b> <b>if one gene dominates a "
    "sample, every other gene's <i>share</i> of the reads falls even "
    "though nothing about them changed</b> — so <b>simple "
    "proportions mislead</b>, and the robust methods estimate a per-"
    "sample size factor from the bulk of genes instead.",
    "<b>Which is CSCE 679 Module 08 &sect;3's normalisation "
    "argument</b> — <b>a map of counts is a map of "
    "population</b> — <b>arriving in a field where the denominator "
    "is itself estimated from the data</b> rather than known."]),

  ("h1", "2 &nbsp; The model"),
  ("ul", ["<b>Counts are modelled as negative binomial</b> — "
          "<b>Poisson counting noise plus extra variance</b> — "
          "<b>because biological replicates vary considerably more than "
          "counting noise alone would predict</b>, and a Poisson model "
          "therefore declares far too much significant.",
          "<b>And the per-gene variance must be estimated from "
          "perhaps three replicates</b>, <b>which is hopeless on its "
          "own</b> — so <b>the standard methods share information "
          "across genes</b>, fitting a mean-variance trend and shrinking "
          "each gene's estimate toward it.",
          "<b>Which is the key statistical idea in this "
          "field</b> — <b>borrowing strength across thousands of "
          "parallel tests</b> — <b>and it works well and is an "
          "assumption</b>: that genes with similar expression have "
          "similar variance, which is usually but not always "
          "true.",
          "<b>Then a test per gene, and a p-value per gene</b> "
          "— <b>twenty thousand of them</b>, <b>which is "
          "&sect;3's subject</b> and is where the list becomes a "
          "finding or does not.",
          "<b>And the effect size matters as much as the "
          "p-value</b>: <b>a tiny fold change can be highly significant "
          "given enough samples</b>, and <b>statistical significance is "
          "not biological importance</b> — which is why the "
          "standard practice reports both and filters on both."]),

  ("break",),
  ("h1", "3 &nbsp; Multiple testing"),
  ("code", """THE ARITHMETIC
    20,000 tests at alpha = 0.05
    => 1,000 expected false positives
    if you report 1,200 "significant" genes, most of
    your list is noise.

BONFERRONI
    use alpha / m. Controls the probability of ANY
    false positive (the family-wise error rate).
    Correct, and far too strict here: you will find
    almost nothing, and the true effects are small.

BENJAMINI-HOCHBERG
    controls the FALSE DISCOVERY RATE: the expected
    PROPORTION of your reported list that is false.
    q = 0.05 means about 5% of your hits are
    expected to be wrong.
    Which is the right target for a screen whose
    output is a list for experimental follow-up.

AND THE COUNT OF TESTS MUST INCLUDE THE ONES YOU RAN
AND DISCARDED. Everybody omits those."""),
  ("p", "<b>The count of tests must include the ones you ran and "
        "discarded</b> — the normalisations you tried, the "
        "covariate sets you fitted, the subgroups you looked at — "
        "<b>which everybody omits, and which is the honest part of the "
        "correction</b>. <b>FDR for screens, FWER when a single false "
        "positive is costly</b>: the choice follows from what the list is "
        "for, and should be stated along with the number m "
        "(CSCE 676 Module 11's multiplicity material, which is the "
        "general treatment)."),

  ("h1", "4 &nbsp; Batch effects"),
  ("callout", "If your cases and controls were processed on different days, "
              "you cannot separate biology from batch",
   ["<b>Processing date, technician, reagent lot, instrument, and "
    "position on a plate all produce systematic measurable "
    "differences</b> — <b>frequently larger than the biological "
    "effect you are looking for</b>, which is the uncomfortable part.",
    "<b>And if batch is confounded with the condition — all "
    "cases run in March, all controls in April — then no "
    "statistical method can separate them</b>: <b>the information is "
    "simply not in the data</b>, <b>which is Module 05 &sect;3's "
    "kind of limit arriving in a statistical setting</b> rather than a "
    "combinatorial one.",
    "<b>So the fix is in the experimental design:</b> <b>randomise "
    "or deliberately balance the samples across batches, and record the "
    "batch metadata</b> — <b>which is free and is very often not "
    "done</b>, leaving the analyst with an unanswerable question years "
    "later.",
    "<b>And the detection is cheap:</b> <b>cluster or project the "
    "samples and colour the points by batch</b> — <b>if they "
    "separate by batch rather than by condition, you have your answer "
    "before running a single test</b> (CSCE 679 Module 07 "
    "&sect;2's projection caveats apply, but the gross signal is "
    "unmistakable)."]),
  ("callout", "And the general shape of this module",
   ["<b>The computation here is trivial and the inference is where "
    "everything fails</b> — <b>which is the exact opposite of "
    "Modules 02 through 09</b>, <b>and is why this module is placed "
    "after them</b> rather than before.",
    "<b>And the failures are systematic and named:</b> "
    "<b>unnormalised counts, uncorrected multiple testing, and batch "
    "confounded with condition</b> — <b>three errors that account "
    "for a large share of the irreproducible findings in this "
    "literature</b> (Module 01's closing callout).",
    "<b>All three are detectable in an afternoon</b> by somebody who "
    "knows to look — which is <b>the practical value of this "
    "module</b> and the reason it is worth more than its algorithmic "
    "content suggests.",
    "<b>So: normalise, correct, and plot the samples coloured by "
    "batch before anything else</b> — <b>three steps, and "
    "Project 2 requires all three</b>, with the batch structure either "
    "examined or stated as unexaminable from the available "
    "metadata."]),
 ],
 "resources": [
   ("Love, Huber & Anders &mdash; Moderated estimation of fold change "
    "and dispersion (DESeq2) (free)",
    "https://genomebiology.biomedcentral.com/articles/10.1186/s13059-014-0550-8",
    "<b>&sect;&sect;1 and 2</b> — the shrinkage model, explained by "
    "its authors, and the software is the standard."),
   ("Benjamini & Hochberg &mdash; Controlling the false discovery "
    "rate",
    "https://rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1995.tb02031.x",
    "<b>&sect;3</b> — the original, and the idea is simpler than its "
    "reputation."),
   ("Leek et al. &mdash; Tackling the widespread and critical impact "
    "of batch effects (free)",
    "https://www.nature.com/articles/nrg2825",
    "<b>&sect;4</b> — with worked examples of published findings that "
    "were batch structure."),
   ("Conesa et al. &mdash; A survey of best practices for RNA-seq "
    "data analysis (free)",
    "https://genomebiology.biomedcentral.com/articles/10.1186/s13059-016-0881-8",
    "<b>The whole module</b>, as a practical checklist."),
 ],
 "exercises": [
   "<b>Take raw counts</b> and compute three normalisations; compare "
   "the gene rankings.",
   "<b>Show that length normalisation is wrong</b> for a "
   "within-gene-across-sample comparison.",
   "<b>Simulate a dominant gene</b> and show that proportions "
   "mislead.",
   "<b>Fit a Poisson and a negative binomial</b> to the same counts "
   "and compare the significance.",
   "<b>Estimate per-gene variance from n = 3</b> and compare to the "
   "shrunk estimate.",
   "<b>Run 20,000 tests on pure noise</b> and count the p-values below "
   "0.05.",
   "<b>Apply Bonferroni and BH</b> to the same p-values and compare "
   "the lists.",
   "<b>Count the tests you actually ran</b> in one analysis, including "
   "discarded ones.",
   "<b>Cluster samples and colour by batch</b> on a public "
   "dataset.",
   "<b>Find a published dataset</b> whose batch metadata is not "
   "available.",
 ],
 "selfcheck": [
   "Name three things a raw count depends on.",
   "When is length normalisation right, and when wrong?",
   "Why do proportions mislead, and what is used instead?",
   "Why negative binomial rather than Poisson?",
   "What is shrinkage doing, and what does it assume?",
   "Why is effect size needed alongside the p-value?",
   "Give the arithmetic of 20,000 tests.",
   "Contrast FWER and FDR, and say when each is right.",
   "Which tests must be counted?",
   "Why can confounded batch not be corrected, and how is it "
   "detected?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Association and Confounding",
 "subtitle": "Finding variants, and the structure that fakes them.",
 "question": "The variant is associated. Does it do anything?",
 "outcomes": [
     "Explain the association study design.",
     "Explain population structure as a confounder.",
     "Explain linkage disequilibrium and what it costs you.",
     "Explain effect sizes and missing heritability.",
     "State what an association establishes.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The design",
   "blurb": "Which is simple, and that is the problem."},

  {"t": "callout", "title": "Test every variant for association with the trait, which is a million tests and a correlational design",
   "kind": "The setup and its two structural weaknesses",
   "body": ["<b>Genotype many individuals at a million or more "
            "variant positions, and test each for association with the "
            "trait</b> — <b>which is Module 10 §3's multiple "
            "testing at a larger scale</b>, and is why the "
            "field uses a 5 × 10⁻⁸ "
            "threshold.",
            "<b>That threshold is a Bonferroni correction for about "
            "a million independent tests</b> — <b>derived rather than "
            "conventional</b>, which is a point in the field's "
            "favour.",
            "<b>And the design is observational</b> — <b>no "
            "intervention, so any association may be "
            "confounded</b> — which is "
            "Part 2.",
            "<b>Plus genotype is not randomised in the "
            "population</b> — <b>it is correlated with ancestry, which "
            "is correlated with environment</b>, and that is the "
            "specific confounder this field had to "
            "solve."]},

  {"t": "section", "label": "Part 2", "title": "Population structure",
   "blurb": "The confounder that produced famous false positives."},

  {"t": "code", "kicker": "Confounding", "title": "How ancestry fakes an association",
   "lang": "text", "code": """
  THE MECHANISM
      allele frequencies differ between ancestral
      populations
      so does almost every trait, for reasons of
      environment, diet, access, and history
      sample both populations unevenly across cases
      and controls, and EVERY differentiated variant
      associates with the trait

  THE CLASSIC ILLUSTRATION
      a variant common in one ancestry group
      "associates" with a trait more common in that
      group, with no causal relationship at all

  THE CORRECTIONS
      principal components of the genotype matrix,
          included as covariates
      linear mixed models with a relatedness matrix
      and these work well for broad structure and
          less well for fine-scale or recent
          structure

  WHICH IS WHY ANCESTRY MUST BE REPORTED, always.
""",
   "caption": "<b>The corrections work well for broad structure and "
              "less well for fine-scale structure</b> — so residual "
              "confounding is expected rather than "
              "excluded.",
   "note": "Population structure is the field's canonical "
           "confounder, and the corrections are partial."},

  {"t": "section", "label": "Part 3", "title": "Linkage disequilibrium",
   "blurb": "Which is what makes the design work and what limits it."},

  {"t": "callout", "title": "Nearby variants are inherited together, so a tested variant stands in for its neighbours",
   "kind": "The double-edged property",
   "body": ["<b>Recombination is rare over short distances, so "
            "variants near each other are correlated across a "
            "population</b> — <b>which is linkage "
            "disequilibrium.</b>",
            "<b>Which is why genotyping a million variants covers a "
            "three-billion-base genome</b> — <b>each tested variant "
            "tags a block of its neighbours</b>, and that is what makes "
            "the design affordable.",
            "<b>And it means the associated variant is usually not "
            "the causal one</b> — <b>it is correlated with "
            "it</b> — so <b>fine-mapping to find the actual causal "
            "variant is a separate and difficult "
            "problem.</b>",
            "<b>Plus most associated variants are "
            "non-coding</b> — <b>regulatory rather than "
            "protein-altering</b> — which makes the mechanism harder "
            "to establish than the association."]},

  {"t": "section", "label": "Part 4", "title": "Effect sizes",
   "blurb": "Which are small, and that has consequences."},

  {"t": "bullets", "kicker": "Interpretation", "title": "What the results look like, and what follows",
   "items": [
     "<b>Individual effect sizes are tiny</b> — <b>odds "
     "ratios near one, explaining a fraction of a percent of "
     "variance</b> — so <b>no single variant predicts "
     "anything about an individual.</b>",
     "",
     "<b>Which is why enormous sample sizes are "
     "needed</b> — hundreds of thousands — and why the field "
     "consolidated into large consortia.",
     "",
     "<b>And polygenic scores aggregate many small "
     "effects</b> — <b>predictive at the population level, weakly "
     "so for individuals</b> — and <b>they transfer poorly across "
     "ancestries</b>, which is a direct consequence of "
     "Parts 2 and 3.",
     "",
     "<b>Plus missing heritability:</b> <b>known variants explain "
     "far less than twin studies suggest</b> — rare variants, "
     "interactions, and heritability estimates themselves are all "
     "candidate explanations.",
     "",
     "<b>And a heritability estimate is population- and "
     "environment-specific</b>, which is the most misunderstood "
     "statistic in biology.",
   ],
   "footnote": "<b>A heritability estimate is specific to a "
               "population and an environment</b> — it is not a "
               "property of a trait, and reading it as one is the "
               "characteristic error."},

  {"t": "callout", "title": "So what an association establishes",
   "kind": "Closing",
   "body": ["<b>'A variant in this region is statistically "
            "associated with this trait, in this cohort, after "
            "correcting for this much population structure'</b> — "
            "which is a real and useful "
            "finding.",
            "<b>And not: that this variant is causal</b> "
            "(Part 3), <b>that the mechanism is known, or "
            "that it predicts anything for a "
            "person</b> (Part 4).",
            "<b>The honest chain is: association → causal variant "
            "→ gene → mechanism → intervention</b>, and <b>each arrow "
            "is years of work</b> that the association does not "
            "do.",
            "<b>Which is Module 01 §3's chain at its "
            "longest</b> — <b>and the reason this field's results are "
            "so frequently overstated in reporting is that the first "
            "link is cheap and the rest are "
            "not.</b>"]},
 ],
 "takeaways": [
   "The genome-wide threshold is a Bonferroni correction for about a "
   "million independent tests, derived rather than conventional.",
   "Population structure fakes associations: differentiated variants "
   "associate with any trait that differs between groups.",
   "The corrections work for broad structure and less well for fine-scale, "
   "so residual confounding is expected.",
   "Linkage disequilibrium is what makes the design affordable and means "
   "the associated variant is usually not the causal one.",
   "Effect sizes are tiny, so no single variant predicts anything about an "
   "individual.",
   "A heritability estimate is specific to a population and an environment, "
   "not a property of a trait.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The design"),
  ("callout", "Test every variant for association with the trait, which is a "
              "million tests and a correlational design",
   ["<b>Genotype many individuals at a million or more variant "
    "positions, and test each position for association with the "
    "trait</b> — <b>which is Module 10 &sect;3's multiple "
    "testing problem at a considerably larger scale</b>, <b>and is why "
    "the field uses a genome-wide significance threshold of "
    "5 &times; 10<super>&minus;8</super>.</b>",
    "<b>That threshold is a Bonferroni correction for roughly a "
    "million effectively independent tests</b> — <b>derived rather "
    "than conventional</b> — <b>which is a real point in the "
    "field's favour</b>: it adopted a stringent, justified threshold "
    "early, and its replication record improved markedly as a "
    "result.",
    "<b>And the design is observational</b> — <b>there is no "
    "intervention, so any association found may be confounded</b> by "
    "anything correlated with both genotype and trait — which is "
    "<b>&sect;2's subject.</b>",
    "<b>Plus genotype is not randomised across the "
    "population</b> — <b>it is correlated with ancestry, which is "
    "correlated with geography, environment, diet, and access to "
    "healthcare</b> — <b>and that is the specific confounder this "
    "field had to solve</b> before any of its results could be "
    "believed."]),

  ("h1", "2 &nbsp; Population structure"),
  ("code", """THE MECHANISM
    allele frequencies differ between ancestral
    populations
    so does almost every trait, for reasons of
    environment, diet, access, and history
    sample both populations unevenly across cases and
    controls, and EVERY differentiated variant
    associates with the trait

THE CLASSIC ILLUSTRATION
    a variant common in one ancestry group
    "associates" with a trait that is more common in
    that group, with no causal relationship at all

THE CORRECTIONS
    principal components of the genotype matrix,
        included as covariates in the model
    linear mixed models with a relatedness matrix
    and these work well for broad structure and less
        well for fine-scale or recent structure

WHICH IS WHY ANCESTRY MUST BE REPORTED, always."""),
  ("p", "<b>The corrections work well for broad structure and less "
        "well for fine-scale or recent structure</b> — <b>so "
        "residual confounding is expected rather than excluded</b>, and "
        "the right statement is 'after correcting for the first ten "
        "principal components' rather than 'after correcting for "
        "population structure'. <b>Population structure is the field's "
        "canonical confounder, and the corrections are partial</b> "
        "— which is a good example of a known confounder handled "
        "well enough to proceed and not well enough to forget."),

  ("break",),
  ("h1", "3 &nbsp; Linkage disequilibrium"),
  ("callout", "Nearby variants are inherited together, so a tested variant "
              "stands in for its neighbours",
   ["<b>Recombination is rare over short distances, so variants near "
    "one another on a chromosome are statistically correlated across a "
    "population</b> — <b>which is linkage disequilibrium</b>, and "
    "it decays with distance and with the number of generations since "
    "the variants arose.",
    "<b>Which is exactly why genotyping a million variants can cover "
    "a three-billion-base genome</b> — <b>each tested variant tags "
    "a block of its neighbours</b> — <b>and that is what makes the "
    "whole design affordable</b> rather than requiring full sequencing "
    "of everyone.",
    "<b>And it means the associated variant is usually not the "
    "causal one</b> — <b>it is merely correlated with it</b> "
    "— so <b>fine-mapping to identify the actual causal variant "
    "within an associated block is a separate and genuinely difficult "
    "problem</b>, often unresolved for years after the "
    "association.",
    "<b>Plus the great majority of associated variants are "
    "non-coding</b> — <b>regulatory rather than "
    "protein-altering</b> — <b>which makes establishing the "
    "mechanism substantially harder than establishing the "
    "association</b>, since you must identify not only the variant but "
    "the gene it regulates and the tissue in which it does so."]),

  ("h1", "4 &nbsp; Effect sizes"),
  ("ul", ["<b>Individual effect sizes are tiny</b> — <b>odds "
          "ratios close to one, each explaining a fraction of a percent "
          "of trait variance</b> — so <b>no single common variant "
          "predicts anything useful about an individual</b>, whatever a "
          "direct-to-consumer report may imply.",
          "<b>Which is why enormous sample sizes are "
          "required</b> — hundreds of thousands of participants to "
          "detect effects of that size — <b>and why the field "
          "consolidated into large international consortia and "
          "biobanks</b>, which has its own consequences for who is "
          "represented.",
          "<b>And polygenic scores aggregate many small effects into "
          "a single number</b> — <b>predictive at the population "
          "level and weakly so for individuals</b> — and <b>they "
          "transfer poorly to ancestries not represented in the training "
          "cohort</b>, <b>which is a direct consequence of &sect;&sect;2 "
          "and 3</b>: different allele frequencies and different linkage "
          "patterns mean the tag variants no longer tag the same "
          "thing.",
          "<b>Plus missing heritability:</b> <b>the known variants "
          "together explain far less of the variance than twin and "
          "family studies suggest is heritable</b> — and <b>rare "
          "variants, gene-gene and gene-environment interactions, and "
          "problems with the heritability estimates themselves are all "
          "live candidate explanations.</b>",
          "<b>And a heritability estimate is specific to a "
          "population and an environment</b>: it is the proportion of "
          "<i>observed variance in that setting</i> attributable to "
          "genetic variance there. <b>It is not a property of a "
          "trait</b>, <b>and reading it as one is the characteristic "
          "error</b> — a highly heritable trait in one environment "
          "can be barely heritable in another, with no genetics having "
          "changed."]),
  ("callout", "So what an association establishes",
   ["<b>'A variant in this region is statistically associated with "
    "this trait, in this cohort, after correcting for this much "
    "population structure, at this significance threshold'</b> — "
    "<b>which is a real and useful finding</b> and has repeatedly "
    "pointed to genuine biology.",
    "<b>And not: that this particular variant is causal</b> "
    "(&sect;3's linkage disequilibrium), <b>that the mechanism is "
    "known, or that it predicts anything actionable for an individual "
    "person</b> (&sect;4's effect sizes).",
    "<b>The honest chain is: association &rarr; causal variant "
    "&rarr; affected gene &rarr; mechanism &rarr; intervention</b>, and "
    "<b>each of those arrows is years of work</b> that the association "
    "itself does not perform.",
    "<b>Which is Module 01 &sect;3's inference chain at its "
    "longest</b> — and <b>the reason this field's results are so "
    "frequently overstated in reporting is structural: the first link is "
    "cheap and automatable, and every subsequent one is "
    "not.</b>"]),
 ],
 "resources": [
   ("Visscher et al. &mdash; 10 years of GWAS discovery (free)",
    "https://www.cell.com/ajhg/fulltext/S0002-9297(17)30240-9",
    "<b>The whole module</b> — an honest assessment by people in the "
    "field, including the overclaiming."),
   ("Price et al. &mdash; Principal components analysis corrects for "
    "stratification (free)",
    "https://www.nature.com/articles/ng1847",
    "<b>&sect;2's correction</b>, in the original."),
   ("Martin et al. &mdash; Clinical use of current polygenic risk "
    "scores may exacerbate health disparities (free)",
    "https://www.nature.com/articles/s41588-019-0379-x",
    "<b>&sect;4's transferability problem</b>, measured — and the "
    "consequences stated."),
   ("Manolio et al. &mdash; Finding the missing heritability of "
    "complex diseases (free)",
    "https://www.nature.com/articles/nature08494",
    "<b>&sect;4</b> — the problem stated, with the candidate "
    "explanations laid out."),
 ],
 "exercises": [
   "<b>Compute the Bonferroni threshold</b> for a million tests and "
   "compare to the field's.",
   "<b>Simulate two populations</b> with different allele frequencies "
   "and different trait rates.",
   "<b>Sample them unevenly</b> and count the spurious "
   "associations.",
   "<b>Correct with principal components</b> and recount.",
   "<b>Make the structure fine-scale</b> and watch the correction "
   "weaken.",
   "<b>Simulate linkage</b> and show a non-causal variant associating "
   "more strongly than the causal one.",
   "<b>Compute the variance explained</b> by a published effect "
   "size.",
   "<b>Apply a polygenic score</b> across two simulated "
   "ancestries.",
   "<b>Explain heritability</b> to somebody, correctly, in four "
   "sentences.",
   "<b>Find a news article</b> about a gene for a trait, and write the "
   "accurate version.",
 ],
 "selfcheck": [
   "Describe the design and its two structural weaknesses.",
   "Where does the genome-wide threshold come from?",
   "Explain how population structure fakes associations.",
   "Name two corrections, and state their limits.",
   "What is linkage disequilibrium, and what does it buy?",
   "What does it cost, and what is fine-mapping?",
   "Why are most associated variants hard to interpret?",
   "How large are effect sizes, and what follows?",
   "Why do polygenic scores transfer poorly?",
   "State what a heritability estimate is, and the common error.",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Pipelines and Reproducibility",
 "subtitle": "An unreproducible result is not a result.",
 "question": "Can you rerun your own analysis from last year?",
 "outcomes": [
     "Explain why computational biology is hard to reproduce.",
     "Explain reference and annotation versioning.",
     "Build a reproducible pipeline.",
     "Explain the silent failure modes.",
     "State what reproducibility does and does not guarantee.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why it fails",
   "blurb": "Specifically, because the causes are enumerable."},

  {"t": "bullets", "kicker": "Causes", "title": "What breaks a computational analysis over time",
   "items": [
     "<b>Tool versions</b> — <b>aligners and callers change "
     "their defaults and their algorithms between releases</b>, and the "
     "output changes with them.",
     "",
     "<b>Reference and annotation versions</b> — "
     "<b>coordinates from one genome build silently mean something else "
     "in another</b>, which is Part 2 and is the worst of "
     "these.",
     "",
     "<b>Undocumented manual steps</b> — <b>the file "
     "somebody edited once, the sample excluded for a reason nobody "
     "wrote down.</b>",
     "",
     "<b>Randomness without a seed</b> — clustering, "
     "subsampling, and any stochastic optimiser.",
     "",
     "<b>And the environment</b> — <b>library versions, "
     "locale settings, and floating-point differences across "
     "platforms</b>, which are small and occasionally "
     "decisive.",
   ],
   "footnote": "<b>'It worked last year' is the characteristic "
               "failure here</b> — the tools move faster than the "
               "papers, and nothing warns "
               "you."},

  {"t": "section", "label": "Part 2", "title": "References and coordinates",
   "blurb": "The specific failure worth its own section."},

  {"t": "callout", "title": "A genomic coordinate is meaningless without the assembly it refers to",
   "kind": "The error that produces wrong answers silently",
   "body": ["<b>Chromosome 7, position 117,120,017 is a different "
            "base in different genome builds</b> — <b>and nothing in "
            "the number says which build you "
            "meant.</b>",
            "<b>So mixing files from two builds produces plausible, "
            "wrong results</b> — <b>no error, no warning, and the "
            "genes are simply the wrong ones.</b>",
            "<b>And lifting coordinates between builds is "
            "lossy</b>: <b>some regions have no equivalent, and some "
            "map to multiple places</b> — so the conversion itself "
            "needs reporting.",
            "<b>Plus annotation versions move independently of "
            "assembly versions</b> — <b>so 'GRCh38' is not sufficient; "
            "the annotation release matters too</b>, which is "
            "Module 01 §1's check-first "
            "rule."]},

  {"t": "section", "label": "Part 3", "title": "Building one",
   "blurb": "What a reproducible pipeline actually requires."},

  {"t": "code", "kicker": "Pipeline", "title": "The requirements, in order of return",
   "lang": "text", "code": """
  1  VERSION CONTROL for the analysis code
         including the small scripts, which are
         where the undocumented decisions live

  2  PINNED ENVIRONMENT
         exact tool versions, in a lock file or a
         container. "conda install bwa" is not a
         version.

  3  NAMED REFERENCE AND ANNOTATION
         the build, the release, and the download
         URL or checksum

  4  A WORKFLOW MANAGER
         Snakemake or Nextflow: declares inputs,
         outputs, and dependencies, so a rerun is
         one command and a partial rerun is correct

  5  SEEDS for everything stochastic

  6  AND A TEST: run it on a tiny dataset in CI, so
         that breakage is found when it happens
         rather than at submission

  THE FIRST FOUR COST A DAY. THE LAST TWO COST AN
  HOUR AND ARE SKIPPED MOST OFTEN.
""",
   "caption": "<b>A workflow manager makes a rerun one command and "
              "a partial rerun correct</b> — which is what a shell "
              "script does not give you."},

  {"t": "section", "label": "Part 4", "title": "What it guarantees",
   "blurb": "And what it does not."},

  {"t": "callout", "title": "Reproducible means somebody gets the same answer from the same data, which is not the same as being right",
   "kind": "Closing",
   "body": ["<b>Computational reproducibility is the weakest of the "
            "three standards and the only one you fully "
            "control</b> — <b>same data, same code, same "
            "answer.</b>",
            "<b>Replication is stronger:</b> <b>new data, same "
            "question, same conclusion</b> — which is what the "
            "scientific claim actually "
            "requires.",
            "<b>And a reproducible pipeline can reproduce a "
            "confounded result perfectly</b> — <b>Module 10 "
            "§4's batch effect survives any amount of "
            "version pinning.</b>",
            "<b>So reproducibility is necessary and not "
            "sufficient</b> — <b>which is exactly the shape of "
            "CSCE 632 §07 §3's conformance claim</b>, and the "
            "right way to describe a floor."]},
 ],
 "takeaways": [
   "'It worked last year' is the characteristic failure: the tools move "
   "faster than the papers, and nothing warns you.",
   "A genomic coordinate is meaningless without the assembly it refers to, "
   "and mixing builds produces plausible wrong results silently.",
   "Annotation versions move independently of assembly versions, so naming "
   "the build is not sufficient.",
   "A workflow manager makes a rerun one command and a partial rerun "
   "correct, which a shell script does not.",
   "Seeds and a CI test cost an hour and are the most frequently skipped "
   "steps.",
   "A reproducible pipeline can reproduce a confounded result perfectly.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why it fails"),
  ("ul", ["<b>Tool versions</b> — <b>aligners, variant callers, "
          "and quantifiers change their default parameters and sometimes "
          "their algorithms between releases</b>, <b>and the output "
          "changes with them</b>, usually by a little and occasionally "
          "by a lot.",
          "<b>Reference and annotation versions</b> — "
          "<b>coordinates from one genome build silently mean something "
          "else in another</b> — <b>which is &sect;2's subject and "
          "is the worst of these failures</b>, because it produces no "
          "error at all.",
          "<b>Undocumented manual steps</b> — <b>the file "
          "somebody edited once by hand, the sample excluded for a "
          "reason nobody wrote down, the column renamed in a "
          "spreadsheet</b> — which are invisible in the code and "
          "decisive for the result.",
          "<b>Randomness without a recorded seed</b> — "
          "clustering initialisations, subsampling, bootstrap "
          "replicates, and any stochastic optimiser — all of which "
          "give different answers on every run.",
          "<b>And the environment</b> — <b>library versions, "
          "locale settings (which change sort order and therefore "
          "output), and floating-point differences across "
          "platforms</b> — <b>which are small and occasionally "
          "decisive</b> at a threshold. <b>'It worked last year' is the "
          "characteristic failure here</b>: <b>the tools move faster "
          "than the papers, and nothing warns you.</b>"]),

  ("h1", "2 &nbsp; References and coordinates"),
  ("callout", "A genomic coordinate is meaningless without the assembly it "
              "refers to",
   ["<b>Chromosome 7, position 117,120,017 is a different base in "
    "different genome builds</b> — the assembly shifted when gaps "
    "were closed and errors corrected — <b>and nothing in the "
    "number itself says which build you meant.</b>",
    "<b>So mixing files from two builds produces plausible, wrong "
    "results</b> — <b>no error, no warning, and the genes you "
    "report are simply the wrong ones</b>, <b>which is the worst "
    "possible failure mode</b> because nothing prompts you to check.",
    "<b>And lifting coordinates between builds is lossy</b>: "
    "<b>some regions have no equivalent in the other build, and some map "
    "to multiple places</b> — <b>so the conversion itself needs "
    "reporting</b>, including how many positions failed to lift.",
    "<b>Plus annotation versions move independently of assembly "
    "versions</b> — gene models are revised, added, and "
    "retired — <b>so naming 'GRCh38' is not sufficient; the "
    "annotation release matters too</b>, and a gene's extent can change "
    "without the assembly changing at all. <b>Which is Module 01 "
    "&sect;1's check-first rule</b>: always 'which version of which "
    "annotation'."]),

  ("break",),
  ("h1", "3 &nbsp; Building one"),
  ("code", """1  VERSION CONTROL for the analysis code
       including the small scripts, which are
       exactly where the undocumented decisions live

2  PINNED ENVIRONMENT
       exact tool versions, in a lock file or a
       container image. "conda install bwa" is not a
       version specification.

3  NAMED REFERENCE AND ANNOTATION
       the assembly build, the annotation release,
       and the download URL or a checksum

4  A WORKFLOW MANAGER
       Snakemake or Nextflow: declares inputs,
       outputs, and dependencies explicitly, so that
       a full rerun is one command and a partial
       rerun recomputes exactly what it should

5  SEEDS for everything stochastic, recorded

6  AND A TEST: run the whole pipeline on a tiny
       dataset in continuous integration, so that
       breakage is found when it happens rather than
       at submission

THE FIRST FOUR COST ABOUT A DAY. THE LAST TWO COST AN
HOUR AND ARE SKIPPED MOST OFTEN."""),
  ("p", "<b>A workflow manager makes a rerun one command and a "
        "partial rerun correct</b> — <b>which is precisely what a "
        "shell script does not give you</b>: a script reruns everything "
        "or whatever you remember to comment out, and the second of those "
        "is how stale intermediate files end up in published results. The "
        "dependency declaration is the point, not the parallelism."),

  ("h1", "4 &nbsp; What it guarantees"),
  ("callout", "Reproducible means somebody gets the same answer from the same "
              "data, which is not the same as being right",
   ["<b>Computational reproducibility is the weakest of the three "
    "standards and the only one you fully control</b> — <b>same "
    "data, same code, same answer</b> — and it is entirely within "
    "your power to deliver, which is why failing to is "
    "indefensible.",
    "<b>Replication is stronger:</b> <b>new data, the same question, "
    "the same conclusion</b> — <b>which is what the scientific "
    "claim actually requires</b> and what this field's crisis was "
    "about.",
    "<b>And a reproducible pipeline can reproduce a confounded "
    "result perfectly, forever</b> — <b>Module 10 &sect;4's "
    "batch effect survives any amount of version pinning</b>, and so "
    "does Module 11 &sect;2's residual population structure. "
    "Reproducibility fixes the plumbing, not the inference.",
    "<b>So reproducibility is necessary and not "
    "sufficient</b> — <b>which is exactly the shape of CSCE 632 "
    "Module 07 &sect;3's conformance claim</b> ('necessary, "
    "checkable, insufficient'), <b>and is the right way to describe a "
    "floor</b>: load-bearing, and not the building."]),
 ],
 "resources": [
   ("Sandve et al. &mdash; Ten simple rules for reproducible "
    "computational research (free)",
    "https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285",
    "<b>&sect;&sect;1 and 3</b> — two pages, and the rules are the "
    "right ones."),
   ("The Snakemake and Nextflow documentation (free)",
    "https://snakemake.readthedocs.io/",
    "<b>&sect;3's fourth item</b> — and the tutorials are short "
    "enough to do in an evening."),
   ("The UCSC and Ensembl genome build documentation (free)",
    "https://genome.ucsc.edu/FAQ/FAQreleases.html",
    "<b>&sect;2</b> — which builds exist, what changed, and how "
    "lifting works."),
   ("Nature's reporting and code availability policies (free)",
    "https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards",
    "<b>&sect;4</b> — what journals now require, which is a useful "
    "minimum checklist even when you are not submitting."),
 ],
 "exercises": [
   "<b>Try to rerun an analysis</b> you did more than six months "
   "ago.",
   "<b>List everything that broke</b>, and classify by §1's "
   "causes.",
   "<b>Take one coordinate</b> and look it up in two builds.",
   "<b>Lift a set of coordinates</b> and count how many fail.",
   "<b>Find two public files</b> that use different builds of the same "
   "genome.",
   "<b>Pin an environment</b> in a lock file or container.",
   "<b>Convert one shell script</b> into a workflow manager "
   "pipeline.",
   "<b>Delete one intermediate file</b> and confirm the partial rerun "
   "is correct.",
   "<b>Add seeds</b> to every stochastic step in one analysis.",
   "<b>Run the whole thing on a tiny dataset</b> in continuous "
   "integration.",
 ],
 "selfcheck": [
   "Name five causes of irreproducibility.",
   "Which is worst, and why?",
   "Why is a coordinate meaningless alone?",
   "What happens when builds are mixed?",
   "Why is lifting lossy, and what should be reported?",
   "Why is naming the build insufficient?",
   "Give the six pipeline requirements in order.",
   "What does a workflow manager give you that a script does not?",
   "Distinguish reproducibility and replication.",
   "What can a reproducible pipeline not fix?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Claiming a Biological Result",
 "subtitle": "What the analysis established, and what it did not.",
 "question": "You found a gene. What do you actually know?",
 "outcomes": [
     "State the inference chain behind a typical claim.",
     "Identify the standard overclaims.",
     "Explain why a negative control is required.",
     "Place this course in the semester and the program.",
     "Write an honest methods and claims section.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The chain",
   "blurb": "Which is long, and is reported as one step."},

  {"t": "callout", "title": "A computational biology result is a statistical statement about a model applied to a particular cohort's measurements",
   "kind": "The honest reading",
   "body": ["<b>The measurement</b> — <b>what the instrument "
            "emitted, with its biases</b> "
            "(Module 01 §2).",
            "<b>The processing</b> — <b>alignment, annotation "
            "version, normalisation, and filtering</b>, each of which "
            "has alternatives that change the result "
            "(Modules 04, 05, 10, 12).",
            "<b>The model and the test</b> — <b>with the number of "
            "tests and the correction</b> "
            "(Module 10 §3).",
            "<b>And the population</b> — <b>who was measured, and "
            "whether the batch and ancestry structure was examined or "
            "merely unexamined</b> (Modules 10 §4, 11 §2). "
            "<b>Five things, and a typical abstract names "
            "none.</b>"]},

  {"t": "table", "kicker": "Overclaims", "title": "The standard overclaims, corrected",
   "header": ["The claim", "The correction"],
   "widths": [4.2, 6.8],
   "rows": [
     ["<b>'We identified the gene for X'</b>", "<b>A variant in a region associated with X (M11 §3)</b>"],
     ["<b>'Gene Y is upregulated'</b>", "<b>Counts assigned to an annotation, normalised how? (M10 §1)</b>"],
     ["<b>'This protein functions as Z'</b>", "<b>Predicted structure, or measured activity? (M09 §3)</b>"],
     ["<b>'BLAST found no homologue'</b>", "<b>These parameters, this database version (M04 §1)</b>"],
     ["<b>'The tree shows that...'</b>", "<b>Under this model, with this support (M06 §4)</b>"],
     ["<b>'The results are reproducible'</b>", "<b>Same data, or new data? (M12 §4)</b>"],
   ],
   "footnote": "<b>'The gene for X' is the one to refuse "
               "hardest</b> — it asserts causality, specificity, "
               "and mechanism, and an association study establishes "
               "none of them.",
   "note": "Each correction names a step the claim skipped."},

  {"t": "section", "label": "Part 2", "title": "The negative control",
   "blurb": "Which is required, and why."},

  {"t": "callout", "title": "Run the analysis on data where the answer should be nothing, and report what it gives",
   "kind": "The cheapest and most informative check available",
   "body": ["<b>Permute the labels, shuffle the sequence, or use a "
            "comparison that should show no difference</b> — <b>and "
            "run the entire pipeline on it</b>, not a "
            "simplified version.",
            "<b>Because it tests the whole chain including the parts "
            "you did not think about</b> — <b>a leak, a filter applied "
            "after the split, an index built on the wrong "
            "file</b>.",
            "<b>And a pipeline that finds two hundred significant "
            "genes in permuted labels has told you something "
            "decisive</b> — <b>which no amount of careful reasoning "
            "would have.</b>",
            "<b>Which is Module 03 §2's empirical null, "
            "generalised to a pipeline</b> — <b>and it is why "
            "Project 2 fails without one</b>, whatever else it "
            "found."]},

  {"t": "section", "label": "Part 3", "title": "The honest write-up",
   "blurb": "What a methods section has to carry."},

  {"t": "code", "kicker": "Reporting", "title": "What to state, and the one extra thing",
   "lang": "text", "code": """
  THE DATA
      source, accession, and what was excluded and
      why

  THE PIPELINE
      tool versions, reference build AND annotation
      release, parameters that differ from defaults

  THE STATISTICS
      the model, the number of tests INCLUDING the
      discarded ones, the correction, and the
      effect sizes alongside the p-values

  THE CONTROLS
      the negative control and its result
      any positive control

  THE STRUCTURE
      batch and ancestry: examined, or stated as
      unexaminable from the available metadata

  AND THE ARTEFACT ACCOUNT
      "if this were batch structure it would look
       like X, and here is whether it does"
      which is the sentence that distinguishes an
      analysis from a result.
""",
   "caption": "<b>The artefact account is what distinguishes an "
              "analysis from a result</b> — say what the finding "
              "would look like if it were not "
              "real."},

  {"t": "section", "label": "Part 4", "title": "The semester and the program",
   "blurb": "Where this course sits."},

  {"t": "table", "kicker": "Semester 12", "title": "Three courses, one shape",
   "header": ["Course", "The external model", "What it costs you"],
   "widths": [2.3, 3.8, 4.9],
   "rows": [
     ["<b>CSCE 640</b>", "<b>Physics</b>", "<b>One measurement, and interference is the only resource</b>"],
     ["<b>CSCE 628</b>", "<b>Biology</b>", "<b>Noisy data, and no ground truth to check against</b>"],
     ["<b>CSCE 717</b>", "<b>Strategic agents</b>", "<b>Inputs chosen to benefit whoever sent them</b>"],
   ],
   "footnote": "<b>In all three the rules come from outside and are "
               "not negotiable</b> — and the first job in each is to "
               "state them accurately rather than to assume them "
               "away.",
   "note": "The model-from-outside framing is the semester's "
           "result."},

  {"t": "callout", "title": "Where this course leaves you",
   "kind": "Closing",
   "body": ["<b>You can derive and implement the core "
            "algorithms</b> — <b>alignment, Viterbi, "
            "folding</b> — and <b>recognise that they are three "
            "variations on one recurrence.</b>",
            "<b>You know where the scores come from and what a null "
            "model is for</b> (Module 03) — <b>which is the habit "
            "that transfers furthest beyond this "
            "subject.</b>",
            "<b>And you know the inference failures that actually "
            "sink findings</b> — <b>multiple testing, batch, "
            "confounding, and irreproducible "
            "pipelines</b> — which is the part a pure algorithms "
            "course omits.",
            "<b>The closing rule is the program's:</b> <b>state what "
            "you measured, state what you assumed, and never claim more "
            "than you established.</b> <b>Here it is the five-part "
            "methods section and the artefact account</b> — because "
            "<b>'we found a gene' is a claim about a pipeline.</b>"]},
 ],
 "takeaways": [
   "A result is a statistical statement about a model applied to a "
   "particular cohort's measurements — five things, and a typical "
   "abstract names none.",
   "'The gene for X' asserts causality, specificity, and mechanism, and an "
   "association study establishes none of them.",
   "A negative control tests the whole chain including the parts you did "
   "not think about.",
   "A pipeline that finds two hundred significant genes in permuted labels "
   "has told you something no reasoning would have.",
   "The artefact account — what the finding would look like if it were "
   "not real — distinguishes an analysis from a result.",
   "All three Semester 12 courses take their model from outside computer "
   "science, and the rules are not negotiable.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The chain"),
  ("callout", "A computational biology result is a statistical statement "
              "about a model applied to a particular cohort's measurements",
   ["<b>The measurement</b> — <b>what the instrument actually "
    "emitted, with its known biases</b>: counts or intensities, not "
    "biological quantities (Module 01 &sect;2).",
    "<b>The processing</b> — <b>alignment tool and parameters, "
    "reference build, annotation release, normalisation, and "
    "filtering</b> — <b>each of which has defensible alternatives "
    "that change the result</b> (Modules 04, 05, 10, and 12).",
    "<b>The model and the test</b> — <b>including the number of "
    "tests performed and the correction applied</b> (Module 10 "
    "&sect;3), and the effect sizes alongside the p-values.",
    "<b>And the population</b> — <b>who was measured, and "
    "whether the batch and ancestry structure was examined or merely "
    "left unexamined</b> (Module 10 &sect;4, Module 11 "
    "&sect;2). <b>Five things, and a typical abstract names none of "
    "them</b>, which is why the methods section is where the content "
    "is."]),
  ("table", ["The claim", "The correction"],
   [["<b>'We identified the gene for X.'</b>",
     "<b>A variant in a region statistically associated with X, in "
     "this cohort</b> — see the note (Module 11 &sect;3)."],
    ["<b>'Gene Y is upregulated in disease.'</b>",
     "<b>Reads assigned to an annotation and counted — normalised "
     "how, tested how, among how many tests?</b> (Module 10 "
     "&sect;&sect;1 and 3.)"],
    ["<b>'This protein functions as Z.'</b>",
     "<b>Predicted structure, inferred by homology, or measured "
     "activity?</b> Three very different claims (Module 09 "
     "&sect;3)."],
    ["<b>'BLAST found no homologue, so there is none.'</b>",
     "<b>These parameters, this database version, this seed "
     "length</b> (Module 04 &sect;1)."],
    ["<b>'The tree shows that A and B are sister taxa.'</b>",
     "<b>Under this evolutionary model, from this alignment, with this "
     "support value</b> (Module 06 &sect;4)."],
    ["<b>'The results are reproducible.'</b>",
     "<b>Same data and same code, or new data?</b> Those are different "
     "standards (Module 12 &sect;4)."]],
   [0.33, 0.67]),
  ("p", "<b>'The gene for X' is the one to refuse hardest</b> — "
        "<b>it asserts causality, specificity, and mechanism all at "
        "once</b>, <b>and an association study establishes none of "
        "them</b> (Module 11 &sect;4's closing chain). <b>Each "
        "correction above names a step the claim skipped</b>, which is "
        "why the corrections are specific rather than general scepticism: "
        "there is always an identifiable missing clause."),

  ("h1", "2 &nbsp; The negative control"),
  ("callout", "Run the analysis on data where the answer should be nothing, "
              "and report what it gives",
   ["<b>Permute the condition labels, shuffle the sequence, or use a "
    "comparison that should show no difference</b> — <b>and run the "
    "entire pipeline on it</b>, <b>not a simplified version</b>, because "
    "the point is to exercise the parts you are not thinking about.",
    "<b>Because it tests the whole chain including those "
    "parts</b> — <b>a label leak, a filter applied after the "
    "train-test split, an index built on the wrong file, a join on the "
    "wrong key</b> — all of which produce signal that no amount of "
    "reading the code reliably catches (CSCE 633 Module 12's "
    "leakage material, in a different setting).",
    "<b>And a pipeline that finds two hundred significant genes in "
    "permuted labels has told you something decisive</b> — "
    "<b>which no amount of careful reasoning would have</b>, and which "
    "takes one rerun to learn.",
    "<b>Which is Module 03 &sect;2's empirical null, generalised "
    "from a score to an entire pipeline</b> — and <b>it is why "
    "Project 2 fails without one</b>, <b>whatever else it found</b>, "
    "since an uncontrolled finding is not assessable."]),

  ("break",),
  ("h1", "3 &nbsp; The honest write-up"),
  ("code", """THE DATA
    source, accession number, and what was excluded
    and why

THE PIPELINE
    tool versions, reference build AND annotation
    release, and every parameter that differs from
    the defaults

THE STATISTICS
    the model, the number of tests INCLUDING the
    ones you ran and discarded, the correction, and
    the effect sizes alongside the p-values

THE CONTROLS
    the negative control and its result
    any positive control, and whether it was
    recovered

THE STRUCTURE
    batch and ancestry: examined, or explicitly
    stated as unexaminable from the available
    metadata

AND THE ARTEFACT ACCOUNT
    "if this were batch structure it would look like
     X, and here is whether it does"
    which is the sentence that distinguishes an
    analysis from a result."""),
  ("p", "<b>The artefact account is what distinguishes an analysis "
        "from a result</b> — <b>say what the finding would look "
        "like if it were not real, and then check</b>. It is the "
        "difference between presenting a number and having interrogated "
        "it, it is cheap, and it is the single most useful paragraph in a "
        "methods section. <b>Project 2 requires it</b>, and it is the "
        "analytical skill the whole course is aimed at."),

  ("h1", "4 &nbsp; The semester and the program"),
  ("table", ["Course", "The external model", "What it costs you"],
   [["<b>CSCE 640</b>", "<b>Physics.</b>",
     "<b>One measurement per run, and interference is the only "
     "resource</b> — the gate set and the noise are given."],
    ["<b>CSCE 628 (this one)</b>", "<b>Biology.</b>",
     "<b>Noisy data, and no ground truth to check the answer "
     "against</b> — so validation is by proxy and controls."],
    ["<b>CSCE 717</b>", "<b>Strategic agents.</b>",
     "<b>Inputs chosen to benefit whoever sent them</b> — so "
     "correctness must include the incentive to report honestly."]],
   [0.22, 0.26, 0.52]),
  ("p", "<b>In all three courses the rules come from outside computer "
        "science and are not negotiable</b> — <b>and the first job "
        "in each is to state them accurately rather than to assume them "
        "away</b>. That is a different discipline from the earlier "
        "semesters, where the machine, the data, and the inputs were all "
        "under your control. <b>The model-from-outside framing is "
        "Semester 12's result</b>, and this course's version of it is "
        "that the data was generated by an experiment you did not run and "
        "cannot repeat."),
  ("callout", "Where this course leaves you",
   ["<b>You can derive and implement the core algorithms</b> — "
    "<b>alignment, Viterbi, and RNA folding</b> — and, more "
    "usefully, <b>recognise that they are three variations on one "
    "recurrence</b> over different subproblem structures (Module 02 "
    "&sect;4's closing point).",
    "<b>You know where the scores come from and what a null model is "
    "for</b> (Module 03) — <b>which is the habit that transfers "
    "furthest beyond this subject</b>, and is the same move as "
    "CSCE 658's permutation tests and CSCE 676's significance "
    "material.",
    "<b>And you know the inference failures that actually sink "
    "findings</b> — <b>uncorrected multiple testing, confounded "
    "batches, population structure, and irreproducible "
    "pipelines</b> — <b>which is precisely the part a pure "
    "algorithms course omits</b> and the part that determines whether "
    "any of the algorithms were worth running.",
    "<b>The closing rule is the program's, unchanged across "
    "thirty-five courses:</b> <b>state what you measured, state what you "
    "assumed, and never claim more than you established.</b> <b>In this "
    "subject it is the five-part methods section and the artefact "
    "account</b> — because <b>'we found a gene' is a claim about a "
    "pipeline, and the pipeline is where the claim can be "
    "checked.</b>"]),
 ],
 "resources": [
   ("Ioannidis &mdash; Why most published research findings are false "
    "(free)",
    "https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.0020124",
    "<b>&sect;1</b> — the argument, which is about multiple testing "
    "and prior probability and applies directly."),
   ("Begley & Ioannidis &mdash; Reproducibility in science (free)",
    "https://www.ahajournals.org/doi/10.1161/CIRCRESAHA.114.303819",
    "<b>&sect;2</b> — what failed to replicate and what the "
    "successful analyses had in common."),
   ("The ARRIVE and MIAME-style reporting guidelines (free)",
    "https://arriveguidelines.org/",
    "<b>&sect;3</b> — structured reporting checklists, which are a "
    "good basis for your own methods section."),
   ("Leek & Peng &mdash; Statistics: P values are just the tip of the "
    "iceberg (free)",
    "https://www.nature.com/articles/520612a",
    "<b>&sect;&sect;1 and 3</b> — the pipeline, not the test, is "
    "where the inference happens."),
 ],
 "exercises": [
   "<b>Take one published abstract</b> and enumerate its five-part "
   "chain from the methods.",
   "<b>Find one that does not supply enough to do that.</b>",
   "<b>Correct six overclaims</b> in your own words.",
   "<b>Rewrite one 'the gene for X' headline</b> accurately.",
   "<b>Run a negative control</b> on an analysis you have already "
   "done.",
   "<b>Deliberately introduce a leak</b> and confirm the control "
   "catches it.",
   "<b>Write the six-part methods section</b> for your Project 2.",
   "<b>Write the artefact account</b>, specifically.",
   "<b>State each Semester 12 course's external model.</b>",
   "<b>Project 2 is now due.</b> Submit the reproducible pipeline, "
   "the multiple-testing accounting, the negative control and its result, "
   "the batch and confounding examination, and the honest claim with its "
   "artefact account.",
 ],
 "selfcheck": [
   "Give the five parts of the inference chain.",
   "Why does a typical abstract not supply them?",
   "Correct six standard overclaims.",
   "Why is 'the gene for X' the worst of them?",
   "What does a negative control test that reasoning does not?",
   "Why must it run the whole pipeline?",
   "Give the six parts of an honest write-up.",
   "What is the artefact account, and why does it matter?",
   "State each Semester 12 course's external model and its cost.",
   "State the closing rule in this subject's terms.",
 ],
},

]
