# -*- coding: utf-8 -*-
"""CSCE 620 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Exact and Adaptive Predicates",
 "subtitle": "Exactness is affordable. Here is the bill.",
 "question": "How do you answer a predicate exactly, and quickly?",
 "outcomes": [
     "Explain why the predicates are integer problems in disguise.",
     "Use a floating-point filter with a correct error bound.",
     "Explain expansion arithmetic and adaptive evaluation.",
     "Implement the incircle predicate.",
     "Handle degeneracy by symbolic perturbation.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The filter",
   "blurb": "Fast path first, and it almost always takes it."},

  {"t": "callout", "title": "The predicate is a polynomial, so its sign is decidable",
   "kind": "Why exactness is possible at all",
   "body": ["<b>Orientation is a degree-2 polynomial in the "
            "coordinates</b>; incircle is degree 4. Both have integer "
            "coefficients.",
            "<b>And floating-point inputs are exact rationals</b> — a "
            "<code>double</code> is an integer times a power of two, "
            "exactly.",
            "<b>So the true value is an exactly representable "
            "rational</b>, and computing its sign is a finite, decidable "
            "problem.",
            "<b>There is no approximation anywhere in the statement of the "
            "problem.</b> The approximation came only from choosing to "
            "evaluate it in a fixed-width format."]},

  {"t": "code", "kicker": "The filter", "title": "Error-bounded fast path",
   "lang": "cpp", "code": """
double orient_filtered(P a, P b, P c) {
    double detleft  = (a.x - c.x) * (b.y - c.y);
    double detright = (a.y - c.y) * (b.x - c.x);
    double det      = detleft - detright;

    // Only when the two products have the SAME sign can cancellation
    // destroy the result. Opposite signs -> no cancellation -> trust it.
    double detsum;
    if (detleft > 0) {
        if (detright <= 0) return det;          // signs differ: exact enough
        else detsum = detleft + detright;
    } else if (detleft < 0) {
        if (detright >= 0) return det;
        else detsum = -detleft - detright;
    } else return det;                          // one factor is zero

    // Forward error bound: |computed - true| <= errbound * detsum.
    // If |det| exceeds that, the SIGN is certainly correct.
    double errbound = CCWERRBOUND_A * detsum;
    if (det >= errbound || -det >= errbound) return det;

    return orient_exact(a, b, c);               // slow path, <1% of calls
}
""",
   "caption": "<b>The bound is proven, not tuned.</b> It is derived from "
              "the floating-point model, which is what makes this correct "
              "rather than merely usually right.",
   "note": "Emphasise: this is not an epsilon. The bound certifies the "
           "sign; an epsilon guesses at it."},

  {"t": "callout", "title": "A filter is not an epsilon",
   "kind": "The distinction, restated precisely",
   "body": ["<b>An epsilon says 'this is close to zero, so call it "
            "zero'.</b> That is a guess, and it is wrong whenever the true "
            "value is small and nonzero.",
            "<b>A filter says 'the computed value exceeds the proven error "
            "bound, so its sign is certainly correct'.</b> That is a "
            "proof.",
            "<b>And when the filter cannot certify, it does not "
            "guess</b> — it escalates to exact evaluation.",
            "<b>So the answer is always exact.</b> The filter changes the "
            "cost, never the result. <b>Module 01's entire table of "
            "non-solutions is avoided by this one distinction.</b>"]},

  {"t": "section", "label": "Part 2", "title": "The exact path",
   "blurb": "Expansions, and why they are cheap."},

  {"t": "callout", "title": "Expansion arithmetic: exact sums of doubles",
   "kind": "The representation",
   "body": ["<b>Represent an exact value as a sum of several "
            "<code>double</code>s</b>, ordered by magnitude and "
            "non-overlapping in their significands.",
            "<b>Two-sum and two-product compute the exact result of an "
            "addition or multiplication</b> as a high part and a low part, "
            "in a handful of operations and no branches.",
            "<b>So exact arithmetic is ordinary floating-point arithmetic, "
            "carefully sequenced.</b> No bignum library, no allocation, no "
            "integer conversion.",
            "<b>Which is why it is fast enough to ship</b> — and why "
            "Shewchuk's 1997 paper changed practice rather than just the "
            "literature."]},

  {"t": "bullets", "kicker": "Adaptive", "title": "Adaptive evaluation: stop as soon as you are sure",
   "items": [
     "<b>Compute the cheapest approximation and its error bound.</b> "
     "Return if the sign is certain.",
     "",
     "<b>Otherwise refine</b> — add the next correction term, which "
     "tightens the bound.",
     "",
     "<b>Check again. Repeat.</b> Each stage costs more and is needed less "
     "often.",
     "",
     "<b>The last stage is fully exact</b> and is reached essentially "
     "never on real input.",
     "",
     "<b>Result: within ~2× of naive on average, and always correct.</b>",
   ],
   "footnote": "<b>The cost is paid in proportion to how close the input "
               "is to degenerate</b>, which is exactly the right billing.",
   "note": "The ~2x figure is the one that persuades people it is "
           "practical."},

  {"t": "eq", "kicker": "The second predicate", "title": "Incircle: is d inside the circle through a, b, c?",
   "eqs": [
     ("incircle(a,b,c,d) = sign of a 4×4 determinant",
      "Rows (aₓ, a_y, aₓ²+a_y², 1) for each of the four points, with a, b, "
      "c in counter-clockwise order."),
     ("Degree 4 in the coordinates",
      "So it cancels far worse than orientation, and the filter's error "
      "bound is correspondingly looser."),
     ("Zero ⟹ the four points are cocircular",
      "Which is the degeneracy that makes Delaunay non-unique "
      "(Module 09)."),
   ],
   "caption": "<b>Orientation and incircle are the two predicates this "
              "course needs.</b> Almost everything reduces to them.",
   "note": "Worth saying plainly: two predicates carry the whole course."},

  {"t": "section", "label": "Part 3", "title": "Degeneracy, decided",
   "blurb": "Making zero never happen."},

  {"t": "callout", "title": "Symbolic perturbation removes degeneracy by definition",
   "kind": "Simulation of Simplicity",
   "body": ["<b>Imagine perturbing each point by a distinct infinitesimal "
            "amount</b>, with the perturbations ordered so no two are "
            "comparable.",
            "<b>Then no predicate ever returns zero</b> — ties are broken "
            "consistently by the perturbation, and general position is "
            "guaranteed.",
            "<b>And you never actually perturb anything.</b> When the exact "
            "predicate returns zero, a deterministic tie-break rule — "
            "derived from the point indices — supplies the sign the "
            "perturbed input would have given.",
            "<b>So every degenerate case is handled by one rule</b> "
            "instead of by code in each algorithm. <b>The output is a valid "
            "structure for a nearby input</b>, which is usually what you "
            "want — and sometimes is not."]},

  {"t": "table", "kicker": "Choosing", "title": "Three ways to handle degeneracy",
   "header": ["Approach", "Cost", "When to use it"],
   "widths": [3.0, 4.2, 4.9],
   "rows": [
     ["<b>Handle each case explicitly</b>", "<b>Much more code; each case a bug risk</b>", "<b>When the degenerate answer is the point</b>"],
     ["<b>Symbolic perturbation</b>", "<b>One rule, applied everywhere</b>", "<b>Default. Structure for a nearby input</b>"],
     ["Reject degenerate input", "Trivial", "Never, for real data"],
   ],
   "footnote": "<b>Perturbation is the default</b> — but if the user asked "
               "'are these four points cocircular?', perturbing away the "
               "answer is wrong.",
   "note": "The caveat matters: perturbation answers a different question, "
           "and occasionally that question is not the one asked."},

  {"t": "callout", "title": "Use Shewchuk's code after this module",
   "kind": "The honest recommendation",
   "body": ["<b>Write the predicates once, to understand them.</b> The "
            "filter derivation in particular is worth doing by hand.",
            "<b>Then use <code>predicates.c</code>.</b> It is public "
            "domain, it is in CGAL and Triangle and countless shipped "
            "systems, and its error bounds are derived correctly.",
            "<b>Compiler flags can break it.</b> <code>-ffast-math</code>, "
            "x87 excess precision, and aggressive reassociation all "
            "invalidate the error analysis silently.",
            "<b>So pin the flags and test the predicate in the build you "
            "ship</b>, not only in a debug build. This is a real and "
            "frequently-encountered failure."]},
 ],
 "takeaways": [
   "Geometric predicates are integer-coefficient polynomials in exactly "
   "representable inputs, so their signs are decidable — exactness is "
   "possible, not merely desirable.",
   "A floating-point filter certifies the sign using a proven forward "
   "error bound, and escalates when it cannot; an epsilon guesses.",
   "Expansion arithmetic represents exact values as non-overlapping sums "
   "of doubles, so exactness needs no bignum library.",
   "Adaptive evaluation stops as soon as the sign is certain, costing "
   "roughly 2× naive on average and never being wrong.",
   "Orientation and incircle are the only two predicates this course needs.",
   "Symbolic perturbation makes every predicate nonzero by a consistent "
   "tie-break rule, replacing per-algorithm degeneracy code with one rule.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The filter"),
  ("callout", "The predicate is a polynomial, so its sign is decidable",
   ["<b>Orientation is a degree-2 polynomial in the input coordinates with "
    "integer coefficients</b>; the incircle predicate is degree 4. Neither "
    "involves division, square roots, or transcendental functions.",
    "<b>And a floating-point number is an exact rational.</b> An IEEE "
    "<code>double</code> is precisely an integer times a power of two "
    "— there is nothing approximate about the <i>input</i>.",
    "<b>So the true value of the predicate is an exactly representable "
    "rational number, and determining its sign is a finite, decidable "
    "problem.</b> It requires no approximation of any kind.",
    "<b>The approximation entered only when we chose to evaluate an exact "
    "expression in a fixed-width format.</b> That is worth stating plainly, "
    "because it reframes the whole difficulty: this was never an "
    "ill-conditioned problem in the numerical-analysis sense. It is an "
    "exactly answerable question that we chose to answer inexactly, and "
    "&sect;2 shows we can afford not to."]),
  ("code", """double orient_filtered(P a, P b, P c) {
    double detleft  = (a.x - c.x) * (b.y - c.y);
    double detright = (a.y - c.y) * (b.x - c.x);
    double det      = detleft - detright;
    double detsum;

    // Cancellation can only hurt when the two products share a sign.
    if      (detleft > 0) { if (detright <= 0) return det;
                            detsum =  detleft + detright; }
    else if (detleft < 0) { if (detright >= 0) return det;
                            detsum = -detleft - detright; }
    else return det;

    // PROVEN forward error bound, not a tuned constant.
    double errbound = CCWERRBOUND_A * detsum;
    if (det >= errbound || -det >= errbound) return det;
    return orient_exact(a, b, c);        // taken on <1% of real input
}"""),
  ("callout", "A filter is not an epsilon",
   ["<b>An epsilon says: 'the computed value is close to zero, so I will "
    "call it zero.'</b> That is a guess. It is wrong precisely when the "
    "true value is small and nonzero — which is exactly the case the "
    "epsilon was introduced to handle.",
    "<b>A filter says: 'the computed value exceeds the proven bound on the "
    "error, therefore its sign is certainly correct.'</b> That is a "
    "deduction from the floating-point model, and it either applies or it "
    "does not.",
    "<b>And when the filter cannot certify the sign, it does not "
    "guess.</b> It escalates to exact evaluation, which always terminates "
    "with the right answer.",
    "<b>So the answer is always exact. The filter changes only the "
    "cost.</b> <b>Module 01's entire table of non-solutions is avoided by "
    "this single distinction</b> — and the reason the distinction is "
    "not more widely understood is that the two look identical in the "
    "source code, differing only in whether the threshold was derived or "
    "chosen."]),

  ("h1", "2 &nbsp; The exact path"),
  ("callout", "Expansion arithmetic: exact values as sums of doubles",
   ["<b>Represent an exact value as a sum of several <code>double</code>s, "
    "ordered by magnitude and non-overlapping in their significands.</b> "
    "The sum of the components is the exact value; each component is an "
    "ordinary machine number.",
    "<b>The primitives are <code>two_sum</code> and "
    "<code>two_product</code></b>, which compute the exact result of a "
    "single addition or multiplication as a high part and a low part. Each "
    "takes a handful of floating-point operations and contains no branches "
    "and no memory allocation.",
    "<b>So exact arithmetic here is ordinary floating-point arithmetic, "
    "carefully sequenced.</b> There is no bignum library, no conversion to "
    "integers, no heap. The expansions live in a fixed-size stack array "
    "whose length is bounded by the degree of the polynomial.",
    "<b>Which is why it is fast enough to ship.</b> Exact geometric "
    "predicates existed long before Shewchuk's 1997 paper; what the paper "
    "contributed was making them cheap enough that there is no longer a "
    "reason to use anything else, which is why it changed practice rather "
    "than only the literature."]),
  ("ol", ["<b>Compute the cheapest approximation and its error bound.</b> "
          "If the bound certifies the sign, return immediately. On "
          "non-degenerate input this happens essentially always.",
          "<b>Otherwise refine:</b> compute the next correction term and "
          "add it, which both improves the estimate and tightens the error "
          "bound.",
          "<b>Check again, and repeat.</b> Each successive stage costs more "
          "than the last and is required less often — the stages are "
          "needed in inverse proportion to their cost.",
          "<b>The final stage is fully exact</b> and always determines the "
          "sign. On real input it is reached almost never; on deliberately "
          "degenerate input it is reached often, which is correct "
          "billing."]),
  ("p", "<b>The measured result is roughly twice the cost of the naive "
        "predicate on average, and always correct.</b> That figure is what "
        "settles the practical argument: a 2&times; cost on seven "
        "floating-point operations, in an algorithm that also does memory "
        "traffic and bookkeeping, is not a reason to accept wrong answers."),
  ("eq", "incircle(a,b,c,d) = sign of the 4&times;4 determinant with rows "
         "(p<sub>x</sub>, p<sub>y</sub>, p<sub>x</sub>&#178; + "
         "p<sub>y</sub>&#178;, 1)"),
  ("p", "for each of the four points, with <i>a</i>, <i>b</i>, <i>c</i> in "
        "counter-clockwise order. It is positive when <i>d</i> lies inside "
        "the circle through the other three, negative outside, and "
        "<b>zero when all four are cocircular</b> — the degeneracy "
        "that makes the Delaunay triangulation non-unique (Module 09). "
        "<b>It is degree 4, so it cancels considerably worse than "
        "orientation</b> and its filter bound is correspondingly looser, "
        "meaning the exact path is taken more often. <b>Orientation and "
        "incircle are the only two predicates this course needs</b>; "
        "nearly everything else reduces to them."),

  ("break",),
  ("h1", "3 &nbsp; Degeneracy, decided once"),
  ("callout", "Symbolic perturbation removes degeneracy by definition",
   ["<b>Imagine perturbing each input point by a distinct infinitesimal "
    "amount</b>, with the perturbations ordered so that no two are "
    "comparable in magnitude — formally, each point <i>i</i> is moved "
    "by a different power of an infinitesimal &epsilon;.",
    "<b>Under such a perturbation no predicate can return zero.</b> Any "
    "tie is broken by the perturbation, and the perturbed input is in "
    "general position by construction. <b>Degeneracy has been defined out "
    "of existence.</b>",
    "<b>And nothing is ever actually perturbed.</b> When the exact "
    "predicate returns zero, a deterministic tie-breaking rule derived from "
    "the point indices supplies the sign that the infinitesimally perturbed "
    "input would have produced. The rule is a small amount of index "
    "comparison, evaluated only on the degenerate path.",
    "<b>So every degenerate case in every algorithm is handled by one rule "
    "rather than by special-case code in each.</b> This is a large "
    "practical saving. <b>The output is a valid structure for an input "
    "infinitesimally close to yours</b> — which is usually exactly "
    "what is wanted, and occasionally is not, per the table below."]),
  ("table", ["Approach", "Cost", "When it is right"],
   [["<b>Handle every degenerate case explicitly.</b>",
     "<b>Substantially more code, and each special case is a fresh bug "
     "risk.</b> The combinatorial explosion is real — segment "
     "intersection alone has a dozen degenerate configurations.",
     "<b>When the degenerate answer is itself the point</b> — a CAD "
     "tool that must report coincident faces, or a validator."],
    ["<b>Symbolic perturbation.</b>",
     "<b>One rule, written once, applied everywhere.</b> Slight cost on the "
     "degenerate path only.",
     "<b>The default, and the right choice for almost all of this "
     "course.</b> You get a valid structure for a nearby input."],
    ["<b>Reject degenerate input.</b>", "Trivial to implement.",
     "<b>Never, for real data.</b> Module 01 &sect;4: real authored "
     "geometry is saturated with degeneracy, so this rejects most of your "
     "input."]],
   [0.26, 0.37, 0.37]),
  ("p", "<b>The caveat on perturbation is worth stating.</b> It answers a "
        "subtly different question from the one asked: not <i>what is the "
        "structure of this input?</i> but <i>what is the structure of an "
        "input infinitesimally near this one?</i> If a user asks whether "
        "four points are cocircular, perturbing the answer away is simply "
        "wrong. Know which question your caller is asking."),
  ("callout", "Use Shewchuk's code after this module",
   ["<b>Write the predicates once yourself, to understand them.</b> The "
    "filter's error-bound derivation in particular rewards doing by hand "
    "— it is the step that makes the difference between a filter and "
    "an epsilon concrete rather than verbal.",
    "<b>Then use <code>predicates.c</code>.</b> It is public domain, it is "
    "embedded in CGAL, Triangle, TetGen, and a great many shipped systems, "
    "its error bounds are derived correctly, and it has been exercised "
    "against more adversarial input than you will generate.",
    "<b>Compiler flags can silently invalidate it.</b> "
    "<code>-ffast-math</code> permits reassociation that breaks the error "
    "analysis; x87 excess precision on 32-bit x86 computes intermediates in "
    "80 bits and rounds unpredictably; aggressive optimisation can "
    "contract a multiply-add into an FMA with different rounding. <b>All of "
    "these produce a predicate that is wrong in exactly the cases it exists "
    "to handle.</b>",
    "<b>So pin the flags, and test the predicate in the configuration you "
    "ship</b> — not only in a debug build. This is a real failure mode "
    "that people hit, and the symptom is that the geometry works in debug "
    "and breaks in release, which sends everyone looking in the wrong "
    "place."]),
 ],
 "resources": [
   ("Shewchuk &mdash; Adaptive Precision Floating-Point Arithmetic and "
    "Fast Robust Geometric Predicates (free, with code)",
    "https://www.cs.cmu.edu/~quake/robust.html",
    "<b>The source for this entire module</b>, including "
    "<code>predicates.c</code>. The error-bound derivations are in the "
    "paper and are worth following once."),
   ("Edelsbrunner & M&uuml;cke &mdash; Simulation of Simplicity (free)",
    "https://arxiv.org/abs/math/9410209",
    "The &sect;3 technique, stated and proved by its authors."),
   ("Dekker; Knuth &mdash; two-sum and two-product",
    "https://en.wikipedia.org/wiki/2Sum",
    "The expansion primitives of &sect;2, with the correctness arguments."),
   ("CGAL &mdash; kernel and number type documentation (free)",
    "https://doc.cgal.org/latest/Kernel_23/",
    "How a production library packages exact predicates and inexact "
    "constructions, which is the Module 13 distinction."),
 ],
 "exercises": [
   "Implement <code>two_sum</code> and <code>two_product</code> and verify "
   "exactness against <code>Fraction</code> over many random inputs.",
   "<b>Derive the error bound</b> for the naive orientation expression "
   "from the IEEE model. Compare your constant against Shewchuk's.",
   "Implement the filtered orientation predicate with your bound.",
   "<b>Measure how often the slow path is taken</b> on uniform random "
   "input, on lattice input, and on your degenerate generator from "
   "Module 01. Explain the three numbers.",
   "Benchmark naive, filtered-adaptive, and fully exact orientation. "
   "Confirm the roughly 2&times; average figure.",
   "Implement the incircle predicate with a filter, and test on cocircular "
   "input.",
   "Re-run Module 01's cyclic-consistency check against the filtered "
   "predicate and confirm it now passes everywhere.",
   "<b>Implement symbolic perturbation</b> for orientation and verify it "
   "never returns zero.",
   "Compile your predicate with <code>-ffast-math</code> and find an input "
   "where it now gives the wrong sign.",
   "Compare your implementation against <code>predicates.c</code> on "
   "correctness and speed.",
 ],
 "selfcheck": [
   "Why is the sign of a geometric predicate a decidable problem?",
   "What does a floating-point filter certify, and how does that differ "
   "from an epsilon?",
   "What is an expansion, and why does exact arithmetic need no bignum "
   "library?",
   "Describe adaptive evaluation and its average cost.",
   "State the incircle predicate and say what its zero case means.",
   "Explain symbolic perturbation and what question it actually answers.",
   "Give three ways to handle degeneracy and when each is right.",
   "Name three compiler behaviours that break an exact predicate.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Convex Hulls",
 "subtitle": "The first real algorithm, and the first real degeneracy.",
 "question": "What is the smallest convex set containing these points?",
 "outcomes": [
     "Implement Graham scan and Andrew's monotone chain.",
     "Explain output-sensitive algorithms and the gift-wrapping bound.",
     "State and justify the lower bound for convex hull.",
     "Handle collinear and duplicate points deliberately.",
     "Extend to three dimensions and state what changes.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The planar algorithms",
   "blurb": "Sort, then sweep."},

  {"t": "code", "kicker": "Monotone chain", "title": "Andrew's algorithm, in full",
   "lang": "cpp", "code": """
// Sort by x, then y. Build the lower hull, then the upper.
std::sort(P.begin(), P.end());
P.erase(std::unique(P.begin(), P.end()), P.end());   // duplicates first

std::vector<Pt> h(2 * P.size());
int k = 0;

for (int i = 0; i < P.size(); i++) {                 // lower hull
    while (k >= 2 && orient(h[k-2], h[k-1], P[i]) <= 0) k--;
    h[k++] = P[i];
}
for (int i = P.size()-2, t = k+1; i >= 0; i--) {     // upper hull
    while (k >= t && orient(h[k-2], h[k-1], P[i]) <= 0) k--;
    h[k++] = P[i];
}
h.resize(k - 1);

// <= 0 DISCARDS collinear points. Use < 0 to KEEP them.
// This one character is a specification decision, not a style choice.
""",
   "caption": "O(n log n), dominated by the sort. <b>Twenty lines, one "
              "predicate, and one genuinely consequential comparison "
              "operator.</b>",
   "note": "The <=0 versus <0 choice is the whole degeneracy story for "
           "hulls. Dwell on it."},

  {"t": "callout", "title": "The collinear decision is a specification, not a detail",
   "kind": "The degeneracy that matters here",
   "body": ["<b>With <code>&lt;= 0</code>:</b> collinear points on a hull "
            "edge are discarded. You get the <i>minimal</i> set of vertices "
            "— the extreme points only.",
            "<b>With <code>&lt; 0</code>:</b> they are kept. You get every "
            "point lying on the boundary.",
            "<b>Both are correct hulls. They are different answers to "
            "different questions.</b>",
            "<b>And the caller cares.</b> A renderer wants the minimal "
            "set; a mesh-boundary extractor needs every boundary vertex. "
            "<b>Decide deliberately and document it</b> — this is the "
            "most common silent mismatch between a hull routine and its "
            "caller."]},

  {"t": "table", "kicker": "Algorithms", "title": "The planar hull algorithms",
   "header": ["Algorithm", "Cost", "Character"],
   "widths": [3.1, 2.7, 6.3],
   "rows": [
     ["<b>Monotone chain</b>", "O(n log n)", "<b>Simplest correct version. Use this</b>"],
     ["Graham scan", "O(n log n)", "Sorts by angle; more degenerate cases"],
     ["<b>Gift wrapping (Jarvis)</b>", "<b>O(nh)</b>", "<b>Output-sensitive; wins when h is tiny</b>"],
     ["QuickHull", "O(n log n) avg", "<b>O(n&#178;) worst case; excellent in practice</b>"],
     ["Divide and conquer", "O(n log n)", "Generalises to 3D; the usual 3D route"],
     ["<b>Chan's algorithm</b>", "<b>O(n log h)</b>", "<b>Optimal. Combines wrapping and D&amp;C</b>"],
   ],
   "footnote": "<b>h</b> is the number of hull vertices. For points on a "
               "disc h grows like n^(1/3); on a square, like log n.",
   "note": "The h growth rates explain why output-sensitivity matters in "
           "practice, not just theory."},

  {"t": "callout", "title": "Why Graham scan is the worse choice despite being the famous one",
   "kind": "A practical judgement",
   "body": ["<b>It sorts by angle about an extreme point</b>, which "
            "requires a pivot choice, and ties in angle must be broken by "
            "distance.",
            "<b>Points equal to the pivot, and points at identical angles, "
            "are both degenerate cases</b> the monotone chain simply does "
            "not have.",
            "<b>And angle comparison invites <code>atan2</code></b>, which "
            "is slow, and transcendental, and destroys exactness.",
            "<b>Monotone chain sorts lexicographically</b> — exact, "
            "total, no pivot, no ties to break. <b>Same bound, fewer ways "
            "to be wrong.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Lower bound and output sensitivity",
   "blurb": "Why n log n, and when you can beat it."},

  {"t": "eq", "kicker": "Lower bound", "title": "Hull is at least as hard as sorting",
   "eqs": [
     ("Given x₁ … xₙ, place pᵢ = (xᵢ, xᵢ²)",
      "Every point lies on a parabola, so every point is on the hull."),
     ("The hull, read in order, gives the xᵢ sorted",
      "So a hull algorithm sorts. Any sorting lower bound transfers."),
     ("⟹ Ω(n log n) in the comparison model",
      "And monotone chain matches it, so the planar problem is closed."),
   ],
   "caption": "<b>A reduction, in three lines.</b> The parabola trick is "
              "worth remembering — it recurs.",
   "note": "Ties back to CSCE 629's reduction material."},

  {"t": "callout", "title": "Output-sensitive algorithms charge by the answer",
   "kind": "Why O(nh) is sometimes the better bound",
   "body": ["<b>Gift wrapping is O(nh)</b> — it finds hull vertices one "
            "at a time, scanning all n points for each.",
            "<b>When h is small this beats O(n log n).</b> Ten thousand "
            "points whose hull is a triangle: 30,000 operations against "
            "130,000.",
            "<b>When h = n it is O(n&#178;)</b> and much worse. Points on a "
            "circle are the bad case.",
            "<b>Chan's algorithm achieves O(n log h)</b>, which is optimal "
            "and beats both — by running gift wrapping over "
            "divide-and-conquer hulls of groups, with a doubling guess for "
            "h. <b>Elegant, and rarely worth implementing.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Three dimensions",
   "blurb": "What stays and what changes."},

  {"t": "table", "kicker": "2D vs 3D", "title": "What changes in three dimensions",
   "header": ["Aspect", "2D", "3D"],
   "widths": [3.0, 4.0, 5.1],
   "rows": [
     ["Output size", "h vertices", "<b>O(n) faces by Euler; still linear</b>"],
     ["<b>Predicate</b>", "orient2d", "<b>orient3d — a 3×3 determinant</b>"],
     ["Structure", "A cycle", "<b>A polyhedron; needs half-edge or similar</b>"],
     ["<b>Degeneracy</b>", "Collinear", "<b>Coplanar — far more common and worse</b>"],
     ["Usual method", "Monotone chain", "<b>Incremental, or QuickHull3D</b>"],
     ["<b>In 4D+</b>", "—", "<b>Output can be O(n^(d/2)). Exponential in d</b>"],
   ],
   "footnote": "<b>Coplanar faces are the 3D robustness problem.</b> Four "
               "coplanar points have no well-defined face, and real meshes "
               "are full of them.",
   "note": "The dimension blowup is worth a sentence — it's why nobody "
           "computes 10D hulls."},

  {"t": "callout", "title": "The engine connection",
   "kind": "Why this module exists here",
   "body": ["<b>Collision detection runs on convex shapes</b> — GJK "
            "(Module 12) requires convexity and nothing else.",
            "<b>So concave meshes are decomposed into convex pieces "
            "offline</b>, and each piece's hull is its collision proxy.",
            "<b>Hulls also give bounding volumes, k-DOPs, and the "
            "separating-axis candidates</b> for SAT.",
            "<b>And in CSCE 649 you assumed all of this existed.</b> The "
            "collision geometry that course took for granted is built "
            "here."]},
 ],
 "takeaways": [
   "Andrew's monotone chain is twenty lines, runs in O(n log n), sorts "
   "lexicographically rather than by angle, and is the one to use.",
   "Whether to keep collinear boundary points is a specification decision "
   "the caller cares about — decide it deliberately and document it.",
   "Graham scan needs a pivot, angle ties, and often atan2, giving it "
   "degenerate cases the monotone chain does not have.",
   "Mapping xᵢ to (xᵢ, xᵢ²) reduces sorting to convex hull, so the problem "
   "is Ω(n log n) in the comparison model.",
   "Output-sensitive algorithms charge by the answer: gift wrapping is "
   "O(nh) and Chan's is the optimal O(n log h).",
   "In 3D the predicate becomes orient3d, the output is a polyhedron, and "
   "coplanarity replaces collinearity as the hard degeneracy.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The planar algorithms"),
  ("code", """std::sort(P.begin(), P.end());                      // lexicographic
P.erase(std::unique(P.begin(), P.end()), P.end()); // duplicates FIRST

std::vector<Pt> h(2*P.size());  int k = 0;
for (int i = 0; i < P.size(); i++) {               // lower hull
    while (k >= 2 && orient(h[k-2], h[k-1], P[i]) <= 0) k--;
    h[k++] = P[i];
}
for (int i = P.size()-2, t = k+1; i >= 0; i--) {   // upper hull
    while (k >= t && orient(h[k-2], h[k-1], P[i]) <= 0) k--;
    h[k++] = P[i];
}
h.resize(k-1);"""),
  ("p", "<b>O(n log n), dominated entirely by the sort</b> — the two "
        "sweeps are linear, because each point is pushed once and popped at "
        "most once. Twenty lines, one predicate, and <b>one genuinely "
        "consequential comparison operator</b>."),
  ("callout", "The collinear decision is a specification, not a detail",
   ["<b>With <code>&lt;= 0</code>, collinear points lying on a hull edge "
    "are popped and discarded.</b> The result is the minimal set of "
    "vertices — the extreme points, and nothing else.",
    "<b>With <code>&lt; 0</code>, they are kept.</b> The result includes "
    "every input point lying anywhere on the hull boundary, including the "
    "interiors of edges.",
    "<b>Both are correct convex hulls.</b> They are different answers "
    "because they are answers to different questions, and neither is a bug.",
    "<b>And the caller cares which one it gets.</b> A renderer drawing the "
    "hull outline wants the minimal set. A mesh-boundary extractor that "
    "must map every input vertex to a boundary position needs all of them. "
    "A collision proxy generator wants the minimal set for fewer SAT axes. "
    "<b>This is the most common silent mismatch between a hull routine and "
    "its caller</b> — decide it deliberately, document it at the "
    "interface, and test both behaviours."]),
  ("table", ["Algorithm", "Cost", "Character"],
   [["<b>Andrew's monotone chain</b>", "O(n log n)",
     "<b>The simplest correct implementation, and the one to use.</b> "
     "Lexicographic sort, two linear sweeps, no pivot, no angles."],
    ["<b>Graham scan</b>", "O(n log n)",
     "Sorts by angle about an extreme point. Historically first, and it "
     "carries degenerate cases the monotone chain does not — see "
     "below."],
    ["<b>Gift wrapping (Jarvis march)</b>", "<b>O(nh)</b>",
     "<b>Output-sensitive.</b> Finds one hull vertex per pass over all n "
     "points. Excellent when h is small, quadratic when it is not."],
    ["<b>QuickHull</b>", "O(n log n) expected",
     "<b>O(n&#178;) worst case</b>, but very fast in practice and it "
     "generalises cleanly to 3D. The usual choice in graphics libraries."],
    ["<b>Divide and conquer</b>", "O(n log n)",
     "Split, recurse, merge by finding the two bridging tangents. "
     "<b>The route that generalises to three dimensions.</b>"],
    ["<b>Chan's algorithm</b>", "<b>O(n log h)</b>",
     "<b>Optimal.</b> Runs gift wrapping over the hulls of small groups, "
     "doubling a guess at h until it succeeds. Beautiful, and rarely worth "
     "the implementation effort."]],
   [0.21, 0.17, 0.62]),
  ("p", "<b>h</b> is the number of hull vertices, and its growth matters "
        "for the output-sensitive bounds: for points uniform in a disc, "
        "h grows like n<super>1/3</super>; for points uniform in a square, "
        "like log n; for points on a circle, h = n. <b>So the "
        "output-sensitive algorithms win on realistic input and lose on the "
        "adversarial case</b>, which is the usual shape of that trade."),
  ("callout", "Why Graham scan is the worse choice despite being the famous one",
   ["<b>It sorts by angle about an extreme point</b>, which requires "
    "choosing a pivot — and ties in angle must then be broken by "
    "distance from that pivot, in a direction that differs between the "
    "first and last edge.",
    "<b>Points coincident with the pivot, and multiple points at identical "
    "angles, are both degenerate cases that the monotone chain does not "
    "have at all.</b> They are not hard to handle; they are simply extra "
    "code and extra opportunities to be wrong.",
    "<b>And angle comparison invites <code>atan2</code></b>, which is slow, "
    "transcendental, and immediately destroys any exactness you established "
    "in Module 02. The correct implementation compares angles using "
    "<code>orient</code> instead — but the obvious implementation does "
    "not, and the obvious one is what gets written.",
    "<b>The monotone chain sorts lexicographically: exact, total, no pivot, "
    "no ties requiring geometric reasoning.</b> <b>Same asymptotic bound, "
    "strictly fewer ways to be wrong</b> — which is the right basis "
    "for choosing between two algorithms of equal complexity."]),

  ("break",),
  ("h1", "2 &nbsp; Lower bound and output sensitivity"),
  ("eq", "x<sub>i</sub> &rarr; p<sub>i</sub> = (x<sub>i</sub>, "
         "x<sub>i</sub>&#178;)"),
  ("p", "Every such point lies on the parabola y = x&#178;, which is "
        "strictly convex, <b>so every point is a hull vertex</b>. Reading "
        "the hull in order around its boundary therefore yields the "
        "x<sub>i</sub> in sorted order. <b>A convex hull algorithm sorts</b>, "
        "so the &Omega;(n log n) comparison-model lower bound for sorting "
        "transfers directly — and the monotone chain matches it, which "
        "closes the planar problem. <b>The parabola reduction is worth "
        "remembering</b>; it recurs in lower-bound arguments throughout "
        "computational geometry, and it is the same reduction technique "
        "CSCE 629 developed."),
  ("callout", "Output-sensitive algorithms charge by the answer",
   ["<b>Gift wrapping is O(nh)</b>: it finds hull vertices one at a time, "
    "scanning all n points to determine the next one, and so pays n per "
    "vertex produced.",
    "<b>When h is small this comfortably beats O(n log n).</b> Ten thousand "
    "points whose hull happens to be a triangle costs about 30,000 "
    "operations, against roughly 130,000 for the sort — and no sorting "
    "at all, which matters more than the operation count suggests because "
    "the memory traffic is sequential.",
    "<b>When h = n it degenerates to O(n&#178;)</b>, which is far worse. "
    "Points on a circle — a perfectly ordinary input, produced by any "
    "radial sampling — are the bad case.",
    "<b>Chan's algorithm achieves O(n log h), which is optimal</b> and "
    "dominates both. It partitions the points into groups of size m, hulls "
    "each group by divide and conquer, then gift-wraps over the group "
    "hulls; m is a guess at h, doubled (squared, in fact) until the wrap "
    "completes. <b>Genuinely elegant, and rarely worth implementing</b> "
    "— the constant factors and the code complexity usually lose to "
    "the monotone chain in practice."]),

  ("h1", "3 &nbsp; Three dimensions"),
  ("table", ["Aspect", "Two dimensions", "Three dimensions"],
   [["<b>Output size</b>", "h vertices, in a cycle.",
     "<b>O(n) vertices, edges, and faces</b> — Euler's formula "
     "V &minus; E + F = 2 keeps it linear, which is not obvious in advance."],
    ["<b>Predicate</b>", "<code>orient2d</code>, a 2&times;2 determinant.",
     "<b><code>orient3d</code>, a 3&times;3 determinant</b> — the "
     "signed volume of a tetrahedron. Same filtering treatment as "
     "Module 02."],
    ["<b>Structure</b>", "A cyclic sequence of vertices.",
     "<b>A polyhedron</b>, requiring a half-edge or winged-edge "
     "representation to navigate adjacency — the structure CSCE 645 "
     "built."],
    ["<b>Hard degeneracy</b>", "Collinear points.",
     "<b>Coplanar points</b>, which are far more common in real meshes and "
     "considerably worse: four coplanar points admit no unique face, so the "
     "algorithm must choose, and inconsistent choices produce a non-closed "
     "surface."],
    ["<b>Usual method</b>", "Monotone chain.",
     "<b>Incremental</b> (add points one at a time, delete visible faces, "
     "cone to the horizon) <b>or QuickHull3D</b>. Divide and conquer also "
     "works and is harder to implement."],
    ["<b>Four or more dimensions</b>", "—",
     "<b>Output size can be O(n<super>d/2</super>)</b> by the upper bound "
     "theorem — exponential in the dimension. This is why nobody "
     "computes hulls in high dimensions, and why the curse of "
     "dimensionality shows up again in Module 10."]],
   [0.17, 0.24, 0.59]),
  ("callout", "The engine connection",
   ["<b>Collision detection operates on convex shapes.</b> GJK "
    "(Module 12) requires convexity and essentially nothing else — "
    "no explicit face list, just a support function.",
    "<b>So concave meshes are decomposed into convex pieces offline</b>, "
    "and each piece's convex hull becomes its collision proxy. Approximate "
    "convex decomposition (V-HACD and relatives) is the standard asset-"
    "pipeline step, and it is built on repeated hull computation.",
    "<b>Hulls also give bounding volumes, k-DOPs, and the candidate "
    "separating axes</b> for the separating axis theorem — the face "
    "normals and edge cross-products of the hull are exactly the axes SAT "
    "must test.",
    "<b>And CSCE 649 assumed all of this already existed.</b> That course "
    "took collision geometry as given so it could get to the dynamics; "
    "<b>this is where the geometry it relied on actually comes from</b>, "
    "including the robustness properties that determine whether the "
    "simulation is stable."]),
 ],
 "resources": [
   ("Mount &mdash; CMSC 754, convex hull lectures (free PDF)",
    "https://www.cs.umd.edu/class/spring2020/cmsc754/Lects/cmsc754-spring2020-lects.pdf",
    "Monotone chain, gift wrapping, the lower bound, and Chan's algorithm, "
    "all done properly."),
   ("Barber, Dobkin & Huhdanpaa &mdash; The Quickhull Algorithm for Convex "
    "Hulls (free)",
    "http://www.qhull.org/",
    "The paper and the <code>qhull</code> implementation, which is what "
    "most software actually calls in 3D and higher."),
   ("Chan &mdash; Optimal output-sensitive convex hull algorithms (free)",
    "https://tmc.web.engr.illinois.edu/pub_hull.html",
    "The O(n log h) result of &sect;2, from its author. Short."),
   ("Ericson &mdash; Real-Time Collision Detection, chapters on convexity "
    "and bounding volumes",
    "https://realtimecollisiondetection.net/",
    "The &sect;3 engine connection, in shipping terms."),
 ],
 "exercises": [
   "Implement Andrew's monotone chain using your Module 02 predicate.",
   "<b>Implement both collinear policies</b> behind a flag, and produce an "
   "input where they differ. Draw both.",
   "Test on: all points identical, all collinear, a single point, two "
   "points, and the empty set. Fix what breaks.",
   "Implement gift wrapping and measure the crossover against monotone "
   "chain as h varies.",
   "<b>Measure h empirically</b> for points uniform in a disc and in a "
   "square, over several n. Compare against n^(1/3) and log n.",
   "Implement Graham scan and count how many degenerate cases it needs "
   "that the monotone chain does not.",
   "<b>Verify the parabola reduction</b> by sorting a list through your "
   "hull routine.",
   "Implement an incremental 3D convex hull with <code>orient3d</code>.",
   "<b>Feed it coplanar input</b> — a cube's vertices, a flat grid "
   "— and report what happens.",
   "Compare your 3D hull against <code>qhull</code> on correctness and "
   "speed.",
 ],
 "selfcheck": [
   "Write the monotone chain and state its cost and what dominates it.",
   "What does the collinear comparison decide, and who cares?",
   "Give three reasons to prefer monotone chain over Graham scan.",
   "State the lower bound reduction for convex hull.",
   "What is an output-sensitive bound? Give the gift-wrapping and Chan "
   "bounds.",
   "How does h grow for points in a disc, in a square, and on a circle?",
   "Name five things that change in three dimensions.",
   "Why is coplanarity worse than collinearity?",
   "How does a physics engine use convex hulls?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Plane Sweep and Segment Intersection",
 "subtitle": "One idea that solves a dozen problems.",
 "question": "How do you avoid comparing everything with everything?",
 "outcomes": [
     "Explain the plane-sweep paradigm and its two structures.",
     "Implement Bentley–Ottmann segment intersection.",
     "Analyse an output-sensitive sweep.",
     "Handle the sweep degeneracies by name.",
     "Recognise other problems the sweep solves.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The paradigm",
   "blurb": "A line moves; events happen; order is maintained."},

  {"t": "callout", "title": "Sweep reduces a 2D problem to a 1D one that changes",
   "kind": "The idea",
   "body": ["<b>Imagine a vertical line sweeping left to right across the "
            "plane.</b> At any moment it meets some subset of the input.",
            "<b>Maintain that subset in sorted order along the line</b> — "
            "the <i>status structure</i>, usually a balanced BST.",
            "<b>The order changes only at discrete events</b>, held in a "
            "priority queue: segment starts, segment ends, and "
            "intersections.",
            "<b>So the continuous sweep is simulated by jumping from event "
            "to event.</b> Nothing is examined between events, which is "
            "where all the savings come from."]},

  {"t": "callout", "title": "The key insight: intersections happen between neighbours",
   "kind": "Why the sweep finds them all",
   "body": ["<b>Two segments can only intersect if they become adjacent in "
            "the status order at some point before they cross.</b>",
            "<b>So you never test all pairs.</b> You test only pairs that "
            "become neighbours — and each adjacency change creates at "
            "most a constant number of new tests.",
            "<b>That reduces O(n&#178;) candidate pairs to O(n + k) actual "
            "tests</b>, where k is the number of intersections.",
            "<b>The proof is the whole algorithm.</b> Everything else is "
            "bookkeeping to keep the status order correct."]},

  {"t": "code", "kicker": "Bentley–Ottmann", "title": "The algorithm",
   "lang": "text", "code": """
  EVENT QUEUE Q: all segment endpoints, ordered by (x, then y)
  STATUS  T: segments crossing the sweep line, ordered by y

  while Q not empty:
      p = Q.pop()                        # leftmost unprocessed event

      LEFT ENDPOINT of s:
          insert s into T
          check s against its new neighbours above and below
          -> queue any intersection strictly right of p

      RIGHT ENDPOINT of s:
          remove s from T
          its former neighbours are now adjacent: check THAT pair

      INTERSECTION of s and t:
          report it
          swap s and t in T                  # their order reverses
          check each against its NEW outer neighbour

  O((n + k) log n).  The log is the BST and the queue.
""",
   "caption": "<b>Three event types, and each does the same two things:</b> "
              "update the order, then test the adjacencies that changed.",
   "note": "Framing all three cases as 'update order, test new "
           "adjacencies' makes it memorable."},

  {"t": "section", "label": "Part 2", "title": "Cost",
   "blurb": "Output-sensitive, and when that is not enough."},

  {"t": "eq", "kicker": "Analysis", "title": "The bound and what it means",
   "eqs": [
     ("O((n + k) log n)",
      "n segments, k intersections. Each event costs a log for the queue "
      "and a log for the status tree."),
     ("Beats O(n²) when k is small",
      "Which it usually is — map data, floor plans, and polygon overlays "
      "have few crossings relative to n²."),
     ("Loses when k ≈ n²",
      "Then brute force wins, having no log factor and perfect locality."),
   ],
   "caption": "<b>Chazelle–Edelsbrunner achieves O(n log n + k)</b>, "
              "which is optimal and considerably harder to implement.",
   "note": "The 'brute force wins at high k' point is worth making — the "
           "sweep is not universally better."},

  {"t": "section", "label": "Part 3", "title": "Degeneracy",
   "blurb": "The sweep has a lot of it."},

  {"t": "table", "kicker": "Cases", "title": "Sweep degeneracies, and what each breaks",
   "header": ["Case", "What breaks", "Handling"],
   "widths": [3.1, 4.3, 4.7],
   "rows": [
     ["<b>Vertical segment</b>", "<b>No single x; status order undefined</b>", "<b>Tilt conceptually, or special-case</b>"],
     ["<b>Shared endpoint</b>", "Two events at one point", "<b>Process together as one event</b>"],
     ["<b>3+ through one point</b>", "<b>Pairwise swaps give wrong order</b>", "<b>Reverse the whole bundle at once</b>"],
     ["Overlapping collinear", "Intersection is a segment, not a point", "Define the output type for it"],
     ["<b>Endpoint on interior</b>", "Is it an intersection?", "<b>A specification question</b>"],
     ["Equal x coordinates", "Event order ambiguous", "Break ties by y, then by type"],
   ],
   "footnote": "<b>The three-segments-through-one-point case is the one "
               "that is genuinely hard</b> and the one random tests never "
               "produce.",
   "note": "This table is the practical heart of the module."},

  {"t": "callout", "title": "Why three-through-one-point is the hard case",
   "kind": "The degeneracy worth understanding",
   "body": ["<b>At a crossing of two segments, their order in the status "
            "reverses.</b> A swap handles it.",
            "<b>When m segments meet at one point, their entire order "
            "reverses</b> — the bundle flips as a block.",
            "<b>Processing that as a sequence of pairwise swaps gives the "
            "wrong final order</b>, and may report intersections that do "
            "not exist or miss ones that do.",
            "<b>So collect all events at the same point, reverse the "
            "bundle once, and test only the two outer boundaries.</b> "
            "<b>And note this case has probability zero under random "
            "input</b> — it appears only in real data, where it is "
            "common."]},

  {"t": "section", "label": "Part 4", "title": "The same idea elsewhere",
   "blurb": "What else is a sweep."},

  {"t": "bullets", "kicker": "Reuse", "title": "Problems the sweep paradigm solves",
   "items": [
     "<b>Closest pair</b> — maintain a strip; O(n log n).",
     "",
     "<b>Rectangle union area and the Klee measure</b> — sweep with a "
     "segment tree over y.",
     "",
     "<b>Trapezoidal decomposition</b> and point location (Module 07).",
     "",
     "<b>Voronoi diagrams</b> — Fortune's algorithm sweeps a beach line "
     "(Module 08).",
     "",
     "<b>Polygon triangulation</b> via monotone decomposition "
     "(Module 05).",
     "",
     "<b>Boolean operations on polygons</b> (Module 06) and "
     "visibility (Module 11).",
   ],
   "footnote": "<b>Six of the remaining modules are sweeps.</b> Learning "
               "the paradigm once pays for most of the course.",
   "note": "Good place to tell them the investment pays off repeatedly."},
 ],
 "takeaways": [
   "Plane sweep reduces a 2D problem to a changing 1D one: a status "
   "structure in sweep order and a priority queue of events.",
   "Two segments can only intersect if they first become neighbours in the "
   "status order, which is why O(n²) candidate pairs become O(n + k) "
   "tests.",
   "Every event type does the same two things — update the order, then "
   "test the adjacencies that changed.",
   "Bentley–Ottmann is O((n + k) log n), which loses to brute force "
   "when k approaches n².",
   "Three or more segments through one point reverses a whole bundle at "
   "once; pairwise swaps give the wrong order, and random input never "
   "produces the case.",
   "Six later modules are sweeps, so the paradigm is worth learning "
   "thoroughly once.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The paradigm"),
  ("callout", "Sweep reduces a 2D problem to a 1D problem that changes",
   ["<b>Imagine a vertical line sweeping continuously from left to right "
    "across the plane.</b> At any instant it meets some subset of the "
    "input, and that subset has a natural one-dimensional order along the "
    "line.",
    "<b>Maintain that subset in sorted order — the <i>status "
    "structure</i></b>, normally a balanced binary search tree supporting "
    "insert, delete, swap, and neighbour queries in logarithmic time.",
    "<b>The order changes only at discrete <i>events</i></b>, held in a "
    "priority queue ordered by sweep position: segment left endpoints, "
    "right endpoints, and — discovered during the sweep — "
    "intersections.",
    "<b>So the continuous sweep is simulated by jumping from event to "
    "event.</b> Nothing whatsoever is examined between events, and that is "
    "where every bit of the saving comes from. The geometry is reduced to "
    "maintaining an order."]),
  ("callout", "Intersections happen between neighbours",
   ["<b>Two segments can only intersect if they become adjacent in the "
    "status order at some moment before they cross.</b> Immediately before "
    "the crossing they are neighbours — nothing can lie between them "
    "— so the adjacency must have arisen at some earlier event.",
    "<b>So you never test all pairs.</b> You test only pairs that actually "
    "become neighbours, and each event changes only a constant number of "
    "adjacencies, generating a constant number of new tests.",
    "<b>That reduces O(n&#178;) candidate pairs to O(n + k) actual "
    "tests</b>, where k is the number of intersections reported.",
    "<b>The proof of that claim is essentially the whole algorithm.</b> "
    "Everything else — the three event handlers, the tie-breaking, the "
    "queue discipline — is bookkeeping in service of keeping the "
    "status order correct so that the adjacency argument remains valid."]),
  ("code", """EVENT QUEUE Q: endpoints ordered by (x, then y)
STATUS     T: segments crossing the sweep line, ordered by y

while Q not empty:
    p = Q.pop()

    LEFT ENDPOINT of s:
        insert s into T
        test s against its new neighbours above and below
        queue any intersection strictly right of p

    RIGHT ENDPOINT of s:
        remove s from T
        its two former neighbours are now adjacent: test THAT pair

    INTERSECTION of s and t:
        report it; swap s and t in T
        test each against its new OUTER neighbour

O((n + k) log n)"""),
  ("p", "<b>All three handlers do the same two things:</b> update the "
        "status order, then test exactly the adjacencies that the update "
        "created. Holding the algorithm in that form makes it far easier to "
        "reconstruct than memorising three separate cases."),

  ("h1", "2 &nbsp; Cost"),
  ("eq", "O((n + k) log n)"),
  ("p", "for n segments and k reported intersections. Each event costs one "
        "logarithmic operation on the priority queue and one on the status "
        "tree, and there are n + k events. <b>This beats O(n&#178;) "
        "whenever k is small</b>, which it usually is in practice — "
        "map data, floor plans, and polygon overlays all have far fewer "
        "crossings than the quadratic worst case. <b>But when k approaches "
        "n&#178;, brute force wins</b>: it has no logarithmic factor, no "
        "tree, and perfect memory locality. <b>Chazelle and Edelsbrunner "
        "achieved the optimal O(n log n + k)</b>, which separates the two "
        "terms, at a considerable cost in implementation complexity that is "
        "rarely repaid."),

  ("break",),
  ("h1", "3 &nbsp; Degeneracy in the sweep"),
  ("table", ["Degenerate case", "What it breaks", "How to handle it"],
   [["<b>A vertical segment.</b>",
     "It has no single x position, so its place in the status order is "
     "undefined and it generates two events at the same x.",
     "<b>Conceptually tilt the sweep line infinitesimally</b> (equivalently, "
     "order events by x then y), or special-case verticals explicitly. The "
     "tilt is cleaner and is symbolic perturbation (Module 02) again."],
    ["<b>Two segments sharing an endpoint.</b>",
     "Two events occur at exactly the same point.",
     "<b>Process all events at a given point together</b> as a single "
     "composite event, rather than one at a time."],
    ["<b>Three or more segments through one point.</b>",
     "<b>The pairwise swap is wrong</b> — see the callout below.",
     "<b>Reverse the entire bundle at once</b>, and test only the two "
     "outermost members against their new neighbours."],
    ["<b>Overlapping collinear segments.</b>",
     "The intersection is a segment, not a point, so the output type is "
     "wrong.",
     "Decide what the output means for this case and define it explicitly. "
     "There is no universally right answer."],
    ["<b>An endpoint lying on another segment's interior.</b>",
     "Is this an intersection or not?",
     "<b>A specification question, not a geometry question.</b> Both "
     "answers are defensible; the caller must be told which it gets."],
    ["<b>Several events at equal x.</b>",
     "The event order is ambiguous, and the wrong order corrupts the "
     "status.",
     "Break ties by y, then by event type — with a fixed, documented "
     "precedence among left endpoint, intersection, and right endpoint."]],
   [0.22, 0.34, 0.44]),
  ("callout", "Why three-through-one-point is the genuinely hard case",
   ["<b>At an ordinary crossing of two segments, their relative order in "
    "the status structure reverses</b>, and a single swap handles it "
    "correctly.",
    "<b>When m segments pass through a common point, the order of all m "
    "reverses</b> — the whole bundle flips as a block, so the segment "
    "that was topmost becomes bottommost.",
    "<b>Processing that as a sequence of pairwise swaps produces the wrong "
    "final order</b>, because the intermediate states are not valid "
    "configurations of the sweep. The consequences are reported "
    "intersections that do not exist, missed intersections that do, and in "
    "some implementations a corrupted tree.",
    "<b>So collect every event at the same point, reverse the bundle in one "
    "operation, and then test only the two outer boundaries of the bundle "
    "against their new neighbours.</b> <b>Note that this configuration has "
    "probability zero under random input</b> (Module 01 &sect;4) and is "
    "entirely routine in real data — any grid, any symmetric model, "
    "any CAD drawing. It is the single best illustration in this course of "
    "why random testing proves nothing."]),

  ("h1", "4 &nbsp; The same idea elsewhere"),
  ("ul", ["<b>Closest pair of points</b> — sweep while maintaining a "
          "strip of candidates within the current best distance. "
          "O(n log n).",
          "<b>Rectangle union area, and the Klee measure problem</b> "
          "— sweep in x with a segment tree over y tracking covered "
          "length.",
          "<b>Trapezoidal decomposition</b>, which underlies planar point "
          "location (Module 07).",
          "<b>Voronoi diagrams</b> — Fortune's algorithm sweeps a "
          "parabolic beach line rather than a straight status line "
          "(Module 08), which is the most inventive use of the paradigm "
          "here.",
          "<b>Polygon triangulation</b> by decomposition into monotone "
          "pieces (Module 05), where the sweep classifies vertices and adds "
          "diagonals.",
          "<b>Boolean operations on polygons</b> (Module 06) and "
          "<b>visibility computations</b> (Module 11), both of which are "
          "sweeps with different status contents."]),
  ("p", "<b>Six of the remaining modules in this course are plane "
        "sweeps.</b> The paradigm is worth learning once, thoroughly, "
        "because the investment is repaid repeatedly — and because "
        "recognising a problem as a sweep is most of the work of solving "
        "it."),
 ],
 "resources": [
   ("de Berg et al. &mdash; Computational Geometry, chapter 2 (line "
    "segment intersection)",
    "https://www.springer.com/gp/book/9783642096815",
    "The canonical treatment of Bentley&ndash;Ottmann, including the "
    "degeneracy handling of &sect;3."),
   ("Mount &mdash; CMSC 754, plane sweep lectures (free PDF)",
    "https://www.cs.umd.edu/class/spring2020/cmsc754/Lects/cmsc754-spring2020-lects.pdf",
    "The paradigm stated generally, then applied, which is the right order "
    "for it."),
   ("Bentley & Ottmann &mdash; Algorithms for reporting and counting "
    "geometric intersections",
    "https://ieeexplore.ieee.org/document/1675432",
    "The original. Short, and worth reading for how directly the adjacency "
    "argument is made."),
   ("CGAL &mdash; 2D Arrangements package documentation (free)",
    "https://doc.cgal.org/latest/Arrangement_on_surface_2/",
    "A production implementation that handles every degeneracy in "
    "&sect;3's table, and documents how."),
 ],
 "exercises": [
   "Implement brute-force segment intersection as a reference "
   "implementation.",
   "Implement Bentley–Ottmann and verify it against the reference on "
   "random input.",
   "<b>Then verify it on degenerate input</b> — and expect the "
   "reference to need fixing too.",
   "Construct each of the six cases in &sect;3's table explicitly and "
   "confirm your handling.",
   "<b>Build an input with ten segments through one point</b> and "
   "demonstrate that pairwise swapping gives the wrong order.",
   "Measure the crossover between brute force and the sweep as k varies "
   "from 0 to n².",
   "Plot the status structure size over the sweep for several inputs and "
   "explain the shapes.",
   "Implement closest pair by sweep and compare against divide and "
   "conquer.",
   "Implement rectangle union area by sweep.",
   "Draw every intermediate sweep state for a small input as SVG and check "
   "them by eye.",
 ],
 "selfcheck": [
   "Describe the sweep paradigm and name its two data structures.",
   "Why can intersections only occur between status neighbours?",
   "Give the three event types and say what each does.",
   "State the Bentley–Ottmann bound and say when brute force wins.",
   "Name six sweep degeneracies and their handling.",
   "Why does a pairwise swap fail when three segments meet at a point?",
   "Why does random input never produce that case?",
   "Name six other problems solved by sweeping.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Polygon Triangulation",
 "subtitle": "Turning a shape into triangles, which is what everything "
             "downstream wants.",
 "question": "How do you cut a polygon into triangles?",
 "outcomes": [
     "Prove that every simple polygon has a triangulation.",
     "Implement ear clipping and state its cost.",
     "Decompose a polygon into monotone pieces by sweep.",
     "Triangulate a monotone polygon in linear time.",
     "Handle holes, and explain the art gallery theorem.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Existence",
   "blurb": "Why there is always an answer."},

  {"t": "callout", "title": "Every simple polygon has a triangulation",
   "kind": "The theorem, and its proof is the algorithm",
   "body": ["<b>Claim: every simple polygon with n ≥ 4 vertices has a "
            "diagonal</b> — a segment between two vertices lying entirely "
            "inside.",
            "<b>Proof: take the leftmost vertex v, with neighbours u and "
            "w.</b> If uw is a diagonal, done. Otherwise some vertices lie "
            "inside triangle uvw; take the one farthest from line uw. "
            "<b>The segment from v to it is a diagonal.</b>",
            "<b>A diagonal splits the polygon into two smaller simple "
            "polygons.</b> Induct.",
            "<b>Every triangulation has exactly n − 2 triangles and "
            "n − 3 diagonals</b>, regardless of which one you find. "
            "<b>Useful as a correctness check.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Ear clipping",
   "blurb": "The one everyone implements."},

  {"t": "code", "kicker": "Ear clipping", "title": "Simple, quadratic, and usually fine",
   "lang": "text", "code": """
  An EAR is a vertex v whose neighbours u, w form a diagonal uw --
  equivalently, triangle uvw is inside the polygon and contains
  no other vertex.

  TWO EARS THEOREM: every simple polygon with n >= 4 has at
  least two non-overlapping ears. So the loop below never stalls.

  while polygon has more than 3 vertices:
      find an ear v
      emit triangle (prev(v), v, next(v))
      remove v from the polygon
      re-test ONLY prev(v) and next(v)      # the rest are unchanged
  emit the final triangle

  COST: O(n^2) -- finding an ear scans, and the point-in-triangle
  test is O(n) per candidate. Fine to n in the low thousands.

  REFLEX VERTEX CACHE: only reflex vertices can block an ear, so
  test candidate ears against those only. Large constant-factor win.
""",
   "caption": "The two ears theorem is what guarantees the loop "
              "terminates — without it, ear clipping could get stuck.",
   "note": "Students often implement this without knowing why it can't "
           "stall. The theorem is the reason."},

  {"t": "callout", "title": "Ear clipping's real failure mode is robustness",
   "kind": "What goes wrong in practice",
   "body": ["<b>The ear test is an orientation predicate plus "
            "point-in-triangle tests</b> — both from Module 02, and both "
            "must be exact.",
            "<b>With inexact predicates the algorithm can find no ear at "
            "all</b>, which contradicts the theorem and means it loops "
            "forever or emits garbage.",
            "<b>That is the classic symptom:</b> a triangulator that hangs "
            "on one particular mesh and works on everything else.",
            "<b>And the usual 'fix' is to bail out after n iterations and "
            "emit a fan</b>, which produces overlapping triangles and "
            "moves the bug downstream. <b>Fix the predicate instead.</b>"]},

  {"t": "section", "label": "Part 3", "title": "The n log n route",
   "blurb": "Monotone decomposition, then linear triangulation."},

  {"t": "callout", "title": "A monotone polygon triangulates in linear time",
   "kind": "Why the two-phase approach works",
   "body": ["<b>A polygon is y-monotone if every horizontal line meets it "
            "in a single segment</b> — equivalently, walking from the top "
            "vertex to the bottom along either chain never goes back up.",
            "<b>Such a polygon triangulates with a single stack pass in "
            "O(n)</b>: merge the two chains by y, and greedily emit "
            "triangles whenever the stack top is convex.",
            "<b>And any simple polygon decomposes into monotone pieces by "
            "one plane sweep in O(n log n)</b> (Module 04).",
            "<b>So: O(n log n) total.</b> The sweep classifies each vertex "
            "as start, end, split, merge, or regular, and the split and "
            "merge vertices are exactly where diagonals must be added."]},

  {"t": "table", "kicker": "Vertex types", "title": "The five vertex types in the sweep",
   "header": ["Type", "Condition", "Action"],
   "widths": [2.5, 5.0, 4.6],
   "rows": [
     ["Start", "Both neighbours below; interior angle &lt; 180°", "Insert edge; set helper"],
     ["<b>Split</b>", "<b>Both below; interior angle &gt; 180°</b>", "<b>Add diagonal to helper</b>"],
     ["End", "Both neighbours above; angle &lt; 180°", "Remove edge"],
     ["<b>Merge</b>", "<b>Both above; angle &gt; 180°</b>", "<b>Mark helper; diagonal added later</b>"],
     ["Regular", "One above, one below", "Replace edge; update helper"],
   ],
   "footnote": "<b>Split and merge vertices are the only ones that break "
               "monotonicity</b>, and each gets exactly one diagonal.",
   "note": "The symmetry between split and merge is worth drawing — merge "
           "is split seen upside down."},

  {"t": "section", "label": "Part 4", "title": "Holes, and how many guards",
   "blurb": "Practical extension and a classic theorem."},

  {"t": "callout", "title": "Holes: join them to the outer boundary first",
   "kind": "The standard technique",
   "body": ["<b>A polygon with holes is not simple</b>, so neither ear "
            "clipping nor monotone decomposition applies directly.",
            "<b>Cut a bridge: find the hole's rightmost vertex, cast a ray "
            "right, and connect to the first edge hit</b> — or to a "
            "visible vertex of it.",
            "<b>The bridge is traversed twice, in opposite "
            "directions</b>, which merges hole and boundary into one "
            "simple polygon.",
            "<b>Repeat per hole.</b> <b>The degeneracies are nasty</b> — "
            "the ray may hit a vertex, two bridges may coincide, and holes "
            "may nest. <b>Delaunay with constraints (Module 09) is often "
            "the better route.</b>"]},

  {"t": "eq", "kicker": "Art gallery", "title": "How many guards does a gallery need?",
   "eqs": [
     ("⌊n/3⌋ guards always suffice, and are sometimes necessary",
      "For a simple polygon with n vertices. Chvátal's theorem."),
     ("Proof: triangulate, 3-colour the triangulation graph",
      "Every triangle gets all three colours; pick the least-used colour "
      "class."),
     ("The comb polygon needs exactly ⌊n/3⌋",
      "So the bound is tight. Each prong needs its own guard."),
   ],
   "caption": "<b>Fisk's proof is three lines and uses triangulation as a "
              "tool</b> rather than as a goal — a good example of why this "
              "module is foundational.",
   "note": "The 3-colouring proof is one of the prettiest in the subject."},

  {"t": "callout", "title": "Which one to use",
   "kind": "The practical recommendation",
   "body": ["<b>Under a few thousand vertices, no holes: ear clipping.</b> "
            "Simple, and the quadratic cost does not matter.",
            "<b>Large, or performance-sensitive: monotone "
            "decomposition.</b> O(n log n) and well understood.",
            "<b>Holes, or triangle quality matters: constrained "
            "Delaunay</b> (Module 09). Avoids the bridging degeneracies "
            "entirely and produces far better triangles.",
            "<b>Shipping: use a library.</b> <code>earcut</code>, "
            "<code>Triangle</code>, or CGAL. <b>All of them handle "
            "degeneracies you have not thought of</b>, which is the whole "
            "argument."]},
 ],
 "takeaways": [
   "Every simple polygon has a diagonal and therefore a triangulation, "
   "with exactly n − 2 triangles and n − 3 diagonals — a "
   "useful correctness check.",
   "The two ears theorem guarantees ear clipping never stalls; without it "
   "the loop has no termination argument.",
   "Ear clipping is O(n²) and its real failure mode is inexact "
   "predicates causing it to find no ear and hang.",
   "A y-monotone polygon triangulates in linear time with one stack pass, "
   "and any simple polygon decomposes into monotone pieces by one sweep.",
   "Split and merge vertices are the only ones that break monotonicity, and "
   "each receives exactly one diagonal.",
   "⌊n/3⌋ guards always suffice for a simple polygon, proved by "
   "triangulating and 3-colouring.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Existence"),
  ("callout", "Every simple polygon has a triangulation",
   ["<b>Claim: every simple polygon with n &ge; 4 vertices has a "
    "diagonal</b> — a segment joining two non-adjacent vertices and "
    "lying entirely in the interior.",
    "<b>Proof.</b> Take the leftmost vertex v (breaking ties by lowest y), "
    "with neighbours u and w. If the segment uw lies inside the polygon it "
    "is a diagonal and we are done. Otherwise at least one vertex lies "
    "inside triangle uvw; among those, take the vertex x farthest from the "
    "line uw. <b>The segment vx is then a diagonal</b> — no edge can "
    "cross it, because any edge doing so would have an endpoint inside uvw "
    "farther from uw than x.",
    "<b>A diagonal splits the polygon into two smaller simple polygons</b>, "
    "each with fewer vertices, so the result follows by induction. <b>The "
    "proof is constructive and is therefore also an algorithm</b>, though a "
    "slow one.",
    "<b>Every triangulation of a simple n-gon has exactly n &minus; 2 "
    "triangles and n &minus; 3 diagonals</b>, regardless of which "
    "triangulation is found — which follows from the same induction. "
    "<b>This is an excellent cheap correctness check</b> to assert in any "
    "triangulator you write."]),

  ("h1", "2 &nbsp; Ear clipping"),
  ("code", """An EAR is a vertex v whose neighbours u,w form a diagonal --
equivalently, triangle uvw lies inside and contains no other vertex.

TWO EARS THEOREM: every simple polygon with n >= 4 has at least
two non-overlapping ears.  This is why the loop cannot stall.

while polygon has > 3 vertices:
    find an ear v
    emit triangle (prev(v), v, next(v))
    remove v
    re-test ONLY prev(v) and next(v)
emit the final triangle

O(n^2).  Optimisation: only REFLEX vertices can block an ear,
so test candidates against the reflex set only."""),
  ("p", "<b>The two ears theorem is the termination argument</b>, and it is "
        "worth knowing that it exists. Many implementations are written "
        "without it and their authors cannot say why the loop must make "
        "progress — which matters, because when the loop <i>does</i> "
        "stall, the cause is never the polygon."),
  ("callout", "Ear clipping's real failure mode is robustness",
   ["<b>The ear test is an orientation predicate plus a sequence of "
    "point-in-triangle tests</b>, and point-in-triangle is itself three "
    "orientation tests. Everything rests on Module 02.",
    "<b>With inexact predicates the algorithm can find no ear at all</b> "
    "— a state the two ears theorem says is impossible, and which "
    "therefore has no handling. The polygon is lying to the algorithm about "
    "its own geometry.",
    "<b>That is the classic symptom:</b> a triangulator that hangs or "
    "produces garbage on one specific mesh out of ten thousand, and works "
    "perfectly on everything else. The mesh is almost always one with "
    "collinear or near-collinear vertices — which is to say, an "
    "ordinary authored mesh (Module 01 &sect;4).",
    "<b>And the usual field fix is to give up after n iterations and emit a "
    "triangle fan.</b> That produces overlapping and inverted triangles, "
    "which then corrupt the normals, the lighting, the collision mesh, and "
    "the physics — moving a loud bug downstream into several quiet "
    "ones. <b>Fix the predicate instead</b>; it is less work than debugging "
    "the consequences."]),

  ("break",),
  ("h1", "3 &nbsp; The O(n log n) route"),
  ("callout", "A monotone polygon triangulates in linear time",
   ["<b>A polygon is y-monotone if every horizontal line meets it in a "
    "single connected segment</b> — equivalently, walking from the "
    "topmost vertex to the bottommost along either boundary chain never "
    "moves back up.",
    "<b>Such a polygon triangulates with one stack pass in O(n).</b> Merge "
    "the two chains into a single y-ordered sequence, push vertices onto a "
    "stack, and whenever the new vertex makes the stack top convex, pop and "
    "emit a triangle. Each vertex is pushed once and popped at most once.",
    "<b>And any simple polygon decomposes into y-monotone pieces by a "
    "single plane sweep in O(n log n)</b>, using exactly the machinery of "
    "Module 04 — a status structure of edges ordered by x, and a "
    "priority queue of vertices ordered by y.",
    "<b>So the total is O(n log n)</b>, which is optimal for the "
    "decomposition-based approach. The sweep classifies every vertex into "
    "one of five types, and <b>the split and merge vertices are precisely "
    "the places where monotonicity fails</b> and a diagonal must be "
    "inserted."]),
  ("table", ["Vertex type", "Condition", "Sweep action"],
   [["<b>Start</b>",
     "Both neighbours lie below it, and the interior angle is less than "
     "180&deg;.",
     "Insert its left edge into the status structure and set that edge's "
     "<i>helper</i> to this vertex."],
    ["<b>Split</b>",
     "<b>Both neighbours below, interior angle greater than 180&deg;.</b> "
     "The interior splits here.",
     "<b>Add a diagonal to the helper of the edge immediately to the "
     "left</b>, then insert the new edge. This is one of the two places a "
     "diagonal is required."],
    ["<b>End</b>",
     "Both neighbours above, interior angle less than 180&deg;.",
     "Remove the edge; if its helper was a merge vertex, add that diagonal "
     "now."],
    ["<b>Merge</b>",
     "<b>Both neighbours above, interior angle greater than 180&deg;.</b> "
     "Two parts of the interior join here.",
     "<b>Mark it as the helper</b> of the edge to its left; the diagonal is "
     "added later, when that edge is removed or its helper replaced. The "
     "mirror image of a split."],
    ["<b>Regular</b>", "One neighbour above and one below.",
     "Replace the outgoing edge with the incoming one on the left side, or "
     "simply update the helper on the right side."]],
   [0.15, 0.37, 0.48]),
  ("p", "<b>Split and merge vertices are the only ones that break "
        "monotonicity</b>, and each receives exactly one diagonal. The "
        "symmetry between them is exact: a merge vertex is a split vertex "
        "seen upside down, which is why some implementations simply sweep "
        "twice in opposite directions and handle only splits."),

  ("h1", "4 &nbsp; Holes, and how many guards"),
  ("callout", "Holes: bridge them to the outer boundary",
   ["<b>A polygon with holes is not a simple polygon</b>, so neither ear "
    "clipping nor monotone decomposition applies to it directly — both "
    "assume a single closed boundary.",
    "<b>The standard technique is to cut a bridge.</b> Take the hole's "
    "rightmost vertex, cast a ray to the right, find the first boundary "
    "edge it hits, and connect to a visible vertex of that edge. This "
    "produces a single boundary that traverses the bridge in both "
    "directions.",
    "<b>The bridge is a degenerate zero-width corridor</b>, traversed once "
    "in each direction, which merges the hole's boundary into the outer "
    "boundary and restores simplicity. Repeat for each hole, processing "
    "them in right-to-left order.",
    "<b>The degeneracies here are genuinely nasty.</b> The ray may hit a "
    "vertex rather than an edge interior; two bridges may want the same "
    "connection; holes may be nested or may touch the boundary; and the "
    "resulting polygon has coincident edges that every downstream predicate "
    "must tolerate. <b>Constrained Delaunay triangulation (Module 09) "
    "handles holes natively and is usually the better route</b> when holes "
    "are present."]),
  ("eq", "&lfloor;n/3&rfloor; guards always suffice, and are sometimes "
         "necessary"),
  ("p", "<b>Chv&aacute;tal's art gallery theorem</b>, for a simple polygon "
        "with n vertices. <b>Fisk's proof is three lines and uses "
        "triangulation as a tool:</b> triangulate the polygon, then 3-colour "
        "the resulting triangulation graph — which is always possible, "
        "because the dual of a polygon triangulation is a tree, so a greedy "
        "colouring never gets stuck. Every triangle then has one vertex of "
        "each colour, so placing guards on the least-frequently-used colour "
        "class covers every triangle and therefore the whole polygon, using "
        "at most &lfloor;n/3&rfloor; guards. <b>The comb polygon — a "
        "row of prongs, each needing its own guard — shows the bound is "
        "tight.</b> It is a good demonstration that triangulation is "
        "foundational rather than merely useful: the theorem is about "
        "visibility and the proof is about triangles."),
  ("callout", "Which one to use",
   ["<b>Under a few thousand vertices and no holes: ear clipping.</b> It is "
    "simple enough to get right, and the quadratic cost is irrelevant at "
    "that size. Add the reflex-vertex cache and it is fast enough for most "
    "tools.",
    "<b>Large inputs, or performance-sensitive paths: monotone "
    "decomposition.</b> O(n log n), well understood, and the sweep is "
    "reusable machinery you will have built in Module 04 anyway.",
    "<b>Holes present, or triangle quality matters: constrained Delaunay</b> "
    "(Module 09). It handles holes without bridging, and it produces "
    "triangles with good aspect ratios — which matters enormously if "
    "the triangles will be used for finite elements, for physics, or for "
    "anything interpolated across.",
    "<b>Shipping anything: use a library.</b> <code>earcut</code> (small, "
    "fast, used in map rendering), <code>Triangle</code> (quality meshing), "
    "or CGAL (everything). <b>All of them handle degeneracies you have not "
    "thought of</b>, which is the entire argument — and triangulation "
    "is a solved problem that is nonetheless easy to get subtly wrong."]),
 ],
 "resources": [
   ("de Berg et al. &mdash; Computational Geometry, chapter 3 (polygon "
    "triangulation)",
    "https://www.springer.com/gp/book/9783642096815",
    "The monotone decomposition of &sect;3, with the five vertex types and "
    "the helper mechanism done precisely."),
   ("Mount &mdash; CMSC 754, triangulation and art gallery lectures (free "
    "PDF)",
    "https://www.cs.umd.edu/class/spring2020/cmsc754/Lects/cmsc754-spring2020-lects.pdf",
    "Includes Fisk's proof and the comb lower bound."),
   ("Mapbox &mdash; earcut (free, MIT)",
    "https://github.com/mapbox/earcut",
    "<b>A production ear clipper with hole support</b>, small enough to "
    "read in an afternoon. The best source for how the bridging of &sect;4 "
    "is actually done."),
   ("Shewchuk &mdash; Triangle (free)",
    "https://www.cs.cmu.edu/~quake/triangle.html",
    "Quality constrained Delaunay meshing, and the reference for the "
    "Module 09 route."),
 ],
 "exercises": [
   "Implement ear clipping with exact predicates. Assert the n − 2 "
   "triangle count.",
   "<b>Add the reflex-vertex cache</b> and measure the speedup.",
   "Build a polygon with many collinear vertices and run a "
   "<code>double</code>-based ear clipper on it. Report what happens.",
   "Implement the five-way vertex classification by sweep.",
   "Implement monotone decomposition and verify every piece is monotone.",
   "<b>Implement linear-time monotone triangulation</b> with the stack "
   "pass.",
   "Compare ear clipping and the two-phase method as n grows, and find the "
   "crossover.",
   "Implement hole bridging and construct three degenerate cases that "
   "break it.",
   "<b>3-colour a triangulation</b> and place art-gallery guards. Verify "
   "coverage by sampling.",
   "Construct the comb polygon and confirm it needs ⌊n/3⌋ "
   "guards.",
 ],
 "selfcheck": [
   "Prove that every simple polygon has a diagonal.",
   "How many triangles and diagonals does a triangulation of an n-gon "
   "have?",
   "State the two ears theorem and say what it guarantees.",
   "What is ear clipping's cost, and what is its real failure mode?",
   "Define y-monotone and say why it triangulates in linear time.",
   "Name the five vertex types and say which ones need diagonals.",
   "How are holes handled, and what goes wrong?",
   "State the art gallery theorem and sketch Fisk's proof.",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Polygon Boolean Operations",
 "subtitle": "Union, intersection, difference — and the hardest "
             "robustness problem in the course.",
 "question": "How do you combine two shapes?",
 "outcomes": [
     "Implement convex and general polygon clipping.",
     "Explain the Greiner–Hormann approach and its failure cases.",
     "Compute winding numbers and apply fill rules.",
     "Explain why boolean operations are the worst robustness case.",
     "Apply snap rounding and say what it costs.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The easy case",
   "blurb": "Clipping against a convex region."},

  {"t": "code", "kicker": "Sutherland–Hodgman", "title": "Clip a polygon against a convex region",
   "lang": "text", "code": """
  For each edge of the CONVEX clip region:
      output = []
      for each edge (prev -> curr) of the subject polygon:
          if curr is INSIDE:
              if prev is OUTSIDE: output += intersection(prev, curr)
              output += curr
          else:
              if prev is INSIDE:  output += intersection(prev, curr)
      subject = output

  Clip against one half-plane at a time; the result feeds the next.
  O(n * k) for n subject vertices and k clip edges.

  THE CATCH: if the SUBJECT is concave, the result may contain
  degenerate connecting edges -- a single output ring that visits
  the boundary and returns along the same line. Visually it looks
  right; topologically it is not a simple polygon.

  THE CLIP REGION MUST BE CONVEX. This is not a limitation that
  can be worked around; the half-plane decomposition requires it.
""",
   "caption": "<b>Twelve lines, and it is the right answer for the "
              "viewport-clipping case</b> that graphics actually needs "
              "most often.",
   "note": "The degenerate-connecting-edge artifact is the thing people "
           "hit and cannot explain."},

  {"t": "callout", "title": "Convex clipping covers more cases than you expect",
   "kind": "When the easy case is enough",
   "body": ["<b>Viewport and scissor clipping</b> — a rectangle, which is "
            "convex.",
            "<b>Frustum clipping</b> — six half-spaces, the 3D version of "
            "exactly this algorithm.",
            "<b>Shadow volume and portal clipping</b>, and splitting "
            "against a BSP plane (Module 07).",
            "<b>So reach for Sutherland–Hodgman first</b> and only "
            "escalate to general boolean operations when the clip region "
            "genuinely is not convex. <b>The cost difference is enormous, "
            "and so is the robustness difference.</b>"]},

  {"t": "section", "label": "Part 2", "title": "The general case",
   "blurb": "Two arbitrary polygons."},

  {"t": "callout", "title": "Greiner–Hormann: walk the intersected boundaries",
   "kind": "The standard approach",
   "body": ["<b>1. Find all intersections</b> between the two boundaries "
            "and insert each as a vertex into both polygons' linked "
            "lists.",
            "<b>2. Classify each intersection as entry or exit</b> "
            "relative to the other polygon.",
            "<b>3. Walk:</b> traverse one boundary until an intersection, "
            "then jump to the other and continue — switching at every "
            "crossing.",
            "<b>4. The traversal rule selects the operation.</b> Union, "
            "intersection, and difference differ only in which direction "
            "you take after each jump. <b>One algorithm, three "
            "results.</b>"]},

  {"t": "table", "kicker": "Failure", "title": "Where Greiner–Hormann breaks",
   "header": ["Case", "What happens"],
   "widths": [4.0, 8.1],
   "rows": [
     ["<b>Vertex lies exactly on an edge</b>", "<b>Entry/exit classification is undefined</b>"],
     ["<b>Overlapping collinear edges</b>", "<b>Infinitely many intersections</b>"],
     ["Shared vertices", "Degenerate intersection; may be missed"],
     ["<b>Results touching at a point</b>", "<b>Output topology is ambiguous</b>"],
     ["Self-intersecting input", "Undefined; must be resolved first"],
   ],
   "footnote": "<b>The original 1998 paper handles none of these</b>; "
               "Foster's 2019 extension handles most. <b>Use the "
               "extension.</b>",
   "note": "Worth naming the versions — people implement the 1998 paper "
           "and then wonder why it fails."},

  {"t": "section", "label": "Part 3", "title": "Winding numbers",
   "blurb": "The cleaner formulation."},

  {"t": "eq", "kicker": "Winding", "title": "Fill rules from one integer",
   "eqs": [
     ("w(p) = number of signed crossings of a ray from p",
      "Counter-clockwise boundary crossings count +1, clockwise −1."),
     ("Non-zero rule: inside ⟺ w ≠ 0",
      "What most CAD and most renderers use. Holes need opposite "
      "winding."),
     ("Even–odd rule: inside ⟺ w is odd",
      "What PostScript and SVG default to. Self-overlap creates holes."),
   ],
   "caption": "<b>Union, intersection, and difference are arithmetic on "
              "winding numbers</b>, which is why this formulation is "
              "cleaner.",
   "note": "The even-odd vs nonzero difference explains a lot of real "
           "rendering bugs."},

  {"t": "callout", "title": "Booleans as winding arithmetic",
   "kind": "Why this view is better",
   "body": ["<b>Give polygon A winding contributions and polygon B "
            "its own.</b> Then for each output region, compute both.",
            "<b>Union: keep where w_A ≠ 0 or w_B ≠ 0. Intersection: "
            "and. Difference: w_A ≠ 0 and w_B = 0.</b>",
            "<b>So the algorithm is one arrangement computation plus a "
            "per-face predicate</b>, rather than three separate traversal "
            "rules.",
            "<b>And it extends to n polygons at once</b>, and to "
            "self-intersecting input, which the boundary-walk formulation "
            "does not. <b>This is what production libraries do.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Why this is the worst case",
   "blurb": "Robustness, at its hardest."},

  {"t": "callout", "title": "Booleans compute new points, and that is the problem",
   "kind": "The core difficulty of the module",
   "body": ["<b>Every algorithm so far only <i>classified</i> input "
            "points.</b> Exact predicates make classification exact, and "
            "Module 02 is sufficient.",
            "<b>Booleans <i>construct</i> new points</b> — the "
            "intersections — and a constructed point is generally not "
            "representable.",
            "<b>So the output of one boolean is approximate input to the "
            "next</b>, and error accumulates across a chain of operations.",
            "<b>Exact predicates do not solve this.</b> They make each "
            "classification right; they cannot make an unrepresentable "
            "coordinate representable. <b>This is the predicate/"
            "construction distinction, and it is the real lesson.</b>"]},

  {"t": "table", "kicker": "Responses", "title": "What can actually be done",
   "header": ["Strategy", "Cost", "Where used"],
   "widths": [2.9, 4.3, 4.9],
   "rows": [
     ["<b>Exact rational coordinates</b>", "<b>Denominators grow; unbounded</b>", "<b>CGAL exact kernels; CAD</b>"],
     ["<b>Snap rounding</b>", "<b>Moves points; can change topology</b>", "<b>Most robust practical systems</b>"],
     ["Integer coordinates only", "Must fix a grid up front", "Clipper; many 2D libraries"],
     ["<b>Interval + exact fallback</b>", "Fast path, exact when needed", "<b>CGAL lazy kernel</b>"],
     ["Tolerance-based merging", "<b>Unsound, but ubiquitous</b>", "Most mesh tools"],
   ],
   "footnote": "<b>Integer coordinates are the most underrated answer.</b> "
               "If your domain permits a fixed grid, the problem largely "
               "disappears.",
   "note": "Clipper's success is the evidence for the integer row."},

  {"t": "callout", "title": "Snap rounding, and its honest cost",
   "kind": "The practical compromise",
   "body": ["<b>Round every vertex and every computed intersection to a "
            "fixed grid</b>, then re-resolve any new intersections the "
            "rounding created.",
            "<b>The output is exactly representable</b>, so the next "
            "operation starts clean. Chains of booleans stop accumulating "
            "error.",
            "<b>But rounding can change topology:</b> a thin sliver can "
            "collapse, two components can merge, a point can cross an edge "
            "it was on the other side of.",
            "<b>So the output is a valid polygon near the true "
            "answer</b> — which is usually acceptable and must be "
            "documented. <b>Iterated snap rounding bounds the "
            "displacement</b>, which is the principled version."]},
 ],
 "takeaways": [
   "Sutherland–Hodgman clips against a convex region in O(nk), which "
   "covers viewport, frustum, portal, and BSP splitting — reach for it "
   "first.",
   "Greiner–Hormann walks intersected boundaries, and union, "
   "intersection and difference differ only in the traversal rule.",
   "The 1998 Greiner–Hormann paper handles no degeneracies; Foster's "
   "2019 extension handles most.",
   "Winding numbers turn booleans into per-face arithmetic, which extends "
   "to many polygons and to self-intersecting input.",
   "Booleans construct new points rather than only classifying existing "
   "ones, and a constructed intersection is generally not representable.",
   "Exact predicates cannot fix construction — snap rounding, exact "
   "rationals, or a fixed integer grid are the real options.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Clipping against a convex region"),
  ("code", """for each edge of the CONVEX clip region:
    output = []
    for each edge (prev -> curr) of the subject polygon:
        if curr is INSIDE:
            if prev is OUTSIDE: output += intersect(prev, curr)
            output += curr
        else:
            if prev is INSIDE:  output += intersect(prev, curr)
    subject = output

O(n*k).  THE CLIP REGION MUST BE CONVEX -- the half-plane
decomposition requires it and there is no way around that."""),
  ("p", "<b>The known artifact:</b> if the <i>subject</i> polygon is "
        "concave, the result may contain degenerate connecting edges "
        "— a single output ring that runs out to the boundary and back "
        "along the same line, joining what should be two separate pieces. "
        "<b>It renders correctly under most fill rules and is not a simple "
        "polygon</b>, so anything downstream that assumes simplicity "
        "(triangulation, offsetting, area computation by the shoelace "
        "formula) will misbehave. This is the artifact people encounter and "
        "cannot explain."),
  ("callout", "Convex clipping covers more cases than you expect",
   ["<b>Viewport and scissor clipping</b> — a rectangle, which is "
    "convex. This is the single most common clipping operation in "
    "graphics.",
    "<b>Frustum clipping</b> — six half-spaces, which is precisely "
    "this algorithm in three dimensions, and is what the hardware does "
    "between the vertex and fragment stages.",
    "<b>Shadow volume clipping, portal clipping, and splitting a polygon "
    "against a BSP plane</b> (Module 07) — all half-space operations.",
    "<b>So reach for Sutherland&ndash;Hodgman first</b>, and escalate to a "
    "general boolean only when the clip region genuinely is not convex. "
    "<b>The difference in cost is large and the difference in robustness is "
    "larger</b> — convex clipping constructs intersections too, but "
    "only against a known half-plane, which is a far better conditioned "
    "computation."]),

  ("h1", "2 &nbsp; The general case"),
  ("callout", "Greiner–Hormann: walk the intersected boundaries",
   ["<b>Find every intersection between the two boundaries and insert each "
    "as a new vertex</b> into both polygons' circular linked lists, with "
    "cross-links joining the two copies of each intersection.",
    "<b>Classify each intersection as an entry or an exit</b> with respect "
    "to the other polygon — determined by whether the boundary is "
    "crossing into or out of the other region at that point.",
    "<b>Then walk.</b> Traverse one boundary until reaching an "
    "intersection, jump through the cross-link to the other polygon, and "
    "continue — switching polygons at every crossing. Each closed walk "
    "produces one output ring; repeat until all intersections are visited.",
    "<b>The traversal rule selects the operation.</b> Union, intersection, "
    "and difference differ only in which direction you proceed after each "
    "jump and which intersections you start from. <b>One algorithm, three "
    "results</b>, which is the appeal of the formulation."]),
  ("table", ["Degenerate case", "What happens"],
   [["<b>A vertex of one polygon lies exactly on an edge of the other.</b>",
     "<b>The entry/exit classification is undefined</b> — the boundary "
     "touches without crossing, so it is neither entering nor exiting. The "
     "walk then takes a wrong turn and produces a malformed ring."],
    ["<b>Collinear overlapping edges.</b>",
     "<b>There are infinitely many intersection points</b>, so the "
     "intersection-insertion step has no well-defined output at all."],
    ["<b>The polygons share a vertex.</b>",
     "A degenerate intersection that a general segment-intersection routine "
     "may not report, so the walk never switches where it should."],
    ["<b>The result touches itself at a single point.</b>",
     "The output topology is genuinely ambiguous — one ring pinched at "
     "a point, or two rings meeting? Both are defensible and downstream "
     "code cares."],
    ["<b>Self-intersecting input.</b>",
     "Undefined behaviour; the input must be resolved into simple rings "
     "first, which is itself a boolean operation."]],
   [0.34, 0.66]),
  ("p", "<b>The original 1998 Greiner&ndash;Hormann paper handles none of "
        "these</b> and says so. <b>Foster, Overfelt and Hormann's 2019 "
        "extension handles most of them</b>, and is the version to "
        "implement. A great deal of broken polygon-clipping code in the "
        "world is a faithful implementation of the 1998 paper applied to "
        "degenerate input."),

  ("break",),
  ("h1", "3 &nbsp; Winding numbers"),
  ("eq", "w(p) = signed number of boundary crossings of any ray from p"),
  ("p", "Counting counter-clockwise crossings as +1 and clockwise as "
        "&minus;1. The value is independent of the ray chosen, which is "
        "what makes it well defined. <b>The non-zero rule</b> declares p "
        "inside when w(p) &ne; 0 — used by most CAD systems and most "
        "renderers, and it requires holes to be wound opposite to their "
        "enclosing boundary. <b>The even&ndash;odd rule</b> declares p "
        "inside when w(p) is odd — the PostScript and SVG default, "
        "under which a shape that overlaps itself develops a hole. "
        "<b>Mismatched fill rules between an authoring tool and a renderer "
        "explain a large fraction of real-world vector rendering bugs.</b>"),
  ("callout", "Booleans as winding arithmetic",
   ["<b>Compute the arrangement of both polygons' edges together</b>, then "
    "for each face of the arrangement compute two winding numbers: one with "
    "respect to A's edges and one with respect to B's.",
    "<b>Each operation is then a predicate on that pair.</b> Union keeps "
    "faces where w<sub>A</sub> &ne; 0 or w<sub>B</sub> &ne; 0; intersection "
    "where both are nonzero; difference where w<sub>A</sub> &ne; 0 and "
    "w<sub>B</sub> = 0; symmetric difference where exactly one is.",
    "<b>So the algorithm is one arrangement computation plus a per-face "
    "test</b>, rather than three distinct traversal rules with three sets "
    "of degenerate cases.",
    "<b>And it extends to many polygons at once, and to self-intersecting "
    "input</b>, neither of which the boundary-walk formulation handles. "
    "<b>This is what production libraries actually do</b> — Clipper, "
    "CGAL's Nef polyhedra, and the boolean operations in most CAD kernels "
    "are all arrangement-plus-predicate, not boundary walks."]),

  ("h1", "4 &nbsp; Why booleans are the worst robustness case"),
  ("callout", "Booleans construct new points, and that is the problem",
   ["<b>Every algorithm in this course so far only <i>classified</i> "
    "existing input points.</b> Convex hull decides which input vertices "
    "are extreme; triangulation decides which input vertices to join; the "
    "sweep decides orderings. Exact predicates (Module 02) make all of "
    "that exact, and nothing more is needed.",
    "<b>Boolean operations <i>construct</i> new points</b> — the "
    "intersections — and <b>the intersection of two segments with "
    "representable endpoints is in general not representable</b>. It is a "
    "rational number whose denominator is a determinant, and rounding it to "
    "the nearest <code>double</code> moves it off both lines.",
    "<b>So the output of one boolean is approximate input to the next.</b> "
    "A chain of operations — which is exactly what a CSG modelling "
    "session or a mesh-processing pipeline is — accumulates error, and "
    "the accumulated error eventually produces self-intersections, slivers, "
    "and non-manifold output.",
    "<b>Exact predicates do not solve this.</b> They make every "
    "classification correct; they cannot make an unrepresentable coordinate "
    "representable. <b>This predicate/construction distinction is the real "
    "lesson of the module</b>, and it is why CGAL's kernels are "
    "parameterised separately on predicate exactness and construction "
    "exactness — the two are genuinely different properties with "
    "genuinely different costs."]),
  ("table", ["Strategy", "Cost", "Where it is used"],
   [["<b>Exact rational coordinates.</b>",
     "<b>Denominators grow with each operation, without bound.</b> After a "
     "few hundred chained booleans the numbers are enormous and everything "
     "slows to a crawl.",
     "<b>CGAL's exact-construction kernels; high-end CAD.</b> Correct, and "
     "genuinely expensive."],
    ["<b>Snap rounding.</b>",
     "<b>Moves points, and can change topology</b> — see below.",
     "<b>Most robust practical systems.</b> The standard engineering "
     "answer."],
    ["<b>Integer coordinates throughout.</b>",
     "Requires fixing a grid resolution in advance and scaling all input "
     "onto it.",
     "<b>Clipper, and many 2D libraries.</b> If the domain permits it, the "
     "problem largely disappears — intersections still need rounding, "
     "but the inputs are exact and comparisons are trivially reliable. "
     "<b>The most underrated answer on this list.</b>"],
    ["<b>Interval arithmetic with exact fallback.</b>",
     "Fast path with a certified slow path, like Module 02's filter applied "
     "to constructions.",
     "CGAL's lazy kernel. Keeps exactness while usually paying floating "
     "point prices."],
    ["<b>Tolerance-based vertex merging.</b>",
     "<b>Unsound</b> — Module 01 &sect;3 applies in full.",
     "Nearly every mesh tool. It works most of the time and fails in ways "
     "nobody can reproduce."]],
   [0.22, 0.38, 0.40]),
  ("callout", "Snap rounding, and its honest cost",
   ["<b>Round every input vertex and every computed intersection to a fixed "
    "grid</b>, then re-resolve any <i>new</i> intersections that the "
    "rounding itself created — because moving points onto a grid can "
    "make previously disjoint edges cross.",
    "<b>The output is then exactly representable</b>, so the next operation "
    "in a chain starts from clean input and error stops accumulating. That "
    "property is what makes long CSG chains viable at all.",
    "<b>But rounding can change topology.</b> A thin sliver can collapse to "
    "nothing; two separate components can merge into one; a vertex can "
    "cross an edge it was formerly on the other side of. None of these is "
    "detectable from the output alone.",
    "<b>So the result is a valid polygon <i>near</i> the true answer</b>, "
    "which is normally acceptable and must be documented as what the "
    "function promises. <b>Iterated snap rounding and its variants bound "
    "the total displacement</b> of any point, which is the principled "
    "version and the one to cite when someone asks how wrong the answer "
    "can be."]),
 ],
 "resources": [
   ("Greiner & Hormann &mdash; Efficient Clipping of Arbitrary Polygons "
    "(free)",
    "https://www.inf.usi.ch/hormann/papers/Greiner.1998.ECO.pdf",
    "The 1998 original of &sect;2. Read it, then read the 2019 extension "
    "before implementing."),
   ("Foster, Overfelt & Hormann &mdash; Clipping simple polygons with "
    "degenerate intersections (free)",
    "https://www.inf.usi.ch/hormann/papers/Foster.2019.CSP.pdf",
    "<b>The degeneracy handling the original lacks.</b> This is the version "
    "to implement."),
   ("Angus Johnson &mdash; Clipper2 (free, Boost licence)",
    "https://github.com/AngusJohnson/Clipper2",
    "<b>The integer-coordinate strategy of &sect;4, shipped.</b> Widely "
    "used, readable, and the best evidence for that row of the table."),
   ("Hobby &mdash; Practical segment intersection with finite precision "
    "output; and CGAL's snap rounding package (free)",
    "https://doc.cgal.org/latest/Snap_rounding_2/",
    "Snap rounding, stated properly, with the displacement bounds."),
 ],
 "exercises": [
   "Implement Sutherland–Hodgman and clip a concave subject against a "
   "rectangle. <b>Produce the degenerate connecting edge and draw it.</b>",
   "Extend it to 3D frustum clipping against six planes.",
   "Implement Greiner–Hormann for union, intersection, and "
   "difference.",
   "<b>Construct all five degenerate cases</b> from &sect;2's table and "
   "report what your implementation does with each.",
   "Implement the 2019 degeneracy extension and re-run them.",
   "Implement winding-number computation and both fill rules. Find a "
   "polygon where they disagree and render both.",
   "<b>Implement booleans as arrangement plus per-face predicate</b> and "
   "compare robustness against the boundary walk.",
   "<b>Chain 100 random booleans</b> with <code>double</code> coordinates "
   "and measure how the error and the vertex count grow.",
   "Repeat with snap rounding and with integer coordinates. Compare.",
   "Find an input where snap rounding changes the topology, and "
   "characterise it.",
 ],
 "selfcheck": [
   "State Sutherland–Hodgman and its one hard requirement.",
   "What artifact appears when the subject polygon is concave?",
   "Name four uses of convex clipping.",
   "Describe the four steps of Greiner–Hormann.",
   "Give five degenerate cases that break it.",
   "Define the winding number and both fill rules.",
   "Why are booleans harder than everything before them?",
   "Distinguish predicates from constructions, and say why it matters.",
   "Give five robustness strategies and the cost of each.",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Spatial Subdivision",
 "subtitle": "BSP trees, k-d trees, quadtrees — the structures an "
             "engine is built on.",
 "question": "How do you organise space so queries are fast?",
 "outcomes": [
     "Build and query a BSP tree and explain painter's-algorithm "
     "ordering.",
     "Build a k-d tree and analyse its queries.",
     "Build quadtrees and octrees and explain balancing.",
     "Compare uniform grids against hierarchies.",
     "Choose a structure from the data and the query.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "BSP trees",
   "blurb": "Recursive half-space partition."},

  {"t": "callout", "title": "A BSP tree gives exact visibility ordering from any viewpoint",
   "kind": "The property that made it famous",
   "body": ["<b>Each internal node holds a splitting plane</b>; the two "
            "children hold what lies on each side. Geometry crossing the "
            "plane is split.",
            "<b>To render back-to-front from any viewpoint: at each node, "
            "recurse into the far side, draw the node, then the near "
            "side.</b>",
            "<b>The tree is built once, offline, and works for every "
            "viewpoint</b> — which is why Doom and Quake used it, and why "
            "it was the right answer before z-buffers were cheap.",
            "<b>The cost is splitting.</b> A poor plane choice fragments "
            "the geometry badly — <b>O(n&#178;) fragments in the worst "
            "case</b> — so plane selection is the whole engineering "
            "problem."]},

  {"t": "bullets", "kicker": "BSP today", "title": "What BSP trees are still used for",
   "items": [
     "<b>Solid modelling and CSG</b> — boolean operations on solids are "
     "clean in a BSP formulation (Module 06).",
     "",
     "<b>Collision geometry</b> — a point or sweep can be classified "
     "against a solid in O(depth).",
     "",
     "<b>Portal and PVS generation</b> — the offline visibility "
     "preprocessing step.",
     "",
     "<b>Convex decomposition</b> — the leaves of a solid BSP are convex "
     "cells (Modules 03 and 12).",
     "",
     "<b>Not for rendering order.</b> The z-buffer won that decisively.",
   ],
   "footnote": "<b>BSP survived by changing jobs</b>, which is a common "
               "pattern for good data structures."},

  {"t": "section", "label": "Part 2", "title": "k-d trees",
   "blurb": "Axis-aligned, alternating, point-based."},

  {"t": "code", "kicker": "k-d tree", "title": "Build and range query",
   "lang": "text", "code": """
  BUILD(points, depth):
      if |points| <= leaf_size: return Leaf(points)
      axis = depth mod k                    # cycle x, y, z, x, ...
      m    = median of points along axis    # nth_element: O(n)
      return Node(axis, m,
                  BUILD(points < m, depth+1),
                  BUILD(points > m, depth+1))

  Build: O(n log n) with linear-time median selection.
  Depth: O(log n) -- balanced by construction, because the median
  splits the COUNT, not the space.

  RANGE QUERY(node, box):
      if node's region is DISJOINT from box:  return       # prune
      if node's region is CONTAINED in box:   report all   # bulk
      otherwise recurse into both children                 # straddle

  Orthogonal range query: O(n^(1-1/k) + m) for m reported points.
  In 2D that is O(sqrt(n) + m) -- NOT logarithmic.
""",
   "caption": "<b>The median split is what guarantees balance</b>, and it "
              "is the difference between a k-d tree and a quadtree.",
   "note": "The sqrt(n) range query bound surprises people who expect "
           "log n."},

  {"t": "callout", "title": "k-d trees degrade with dimension, and sooner than expected",
   "kind": "The limitation to know",
   "body": ["<b>Range query is O(n^(1−1/k))</b> — √n in 2D, n^(2/3) in "
            "3D, and approaching linear as k grows.",
            "<b>Nearest-neighbour search degrades similarly.</b> Above "
            "roughly 20 dimensions a k-d tree examines most of the data "
            "and loses to a linear scan.",
            "<b>The reason is that a bounding box in high dimensions "
            "touches almost everything</b> — the volume concentrates in "
            "the corners, so pruning stops pruning.",
            "<b>For graphics this is fine</b> — k is 2 or 3. <b>For "
            "feature vectors it is not</b>, and approximate methods take "
            "over (Module 10)."]},

  {"t": "section", "label": "Part 3", "title": "Quadtrees and grids",
   "blurb": "Splitting space rather than data."},

  {"t": "table", "kicker": "Comparison", "title": "Three ways to subdivide",
   "header": ["Structure", "Splits", "Consequence"],
   "widths": [2.7, 3.7, 5.7],
   "rows": [
     ["<b>k-d tree</b>", "<b>The data, at the median</b>", "<b>Always balanced; depth O(log n)</b>"],
     ["<b>Quadtree / octree</b>", "<b>Space, at the midpoint</b>", "<b>Depth depends on clustering; can be deep</b>"],
     ["<b>Uniform grid</b>", "Space, uniformly", "<b>O(1) lookup; fails on non-uniform data</b>"],
     ["BVH", "The data, by bounding volume", "<b>Overlapping nodes; best for ray tracing</b>"],
     ["BSP", "Space, by arbitrary plane", "Fits geometry; requires splitting"],
   ],
   "footnote": "<b>Splitting data gives balance; splitting space gives "
               "simple addressing and locational codes.</b> That is the "
               "whole trade.",
   "note": "This table is the module's organising idea — data vs space."},

  {"t": "callout", "title": "Quadtrees: implicit addressing is the real advantage",
   "kind": "Why split space instead of data",
   "body": ["<b>A quadtree cell's position is determined by its path from "
            "the root</b>, so it can be encoded as an integer — the "
            "Morton or Z-order code, formed by interleaving the coordinate "
            "bits.",
            "<b>So cells can be stored in a hash table or a sorted array "
            "with no pointers at all</b>, and neighbours found by bit "
            "arithmetic.",
            "<b>And it sorts into a cache-coherent order</b> — Morton "
            "order has good spatial locality, which matters more than the "
            "asymptotics on real hardware.",
            "<b>The cost is that depth depends on the data.</b> A million "
            "points in one cell means a very deep tree, and <b>duplicate "
            "points mean infinite depth</b> unless you cap it."]},

  {"t": "callout", "title": "Balanced quadtrees, and why meshing needs them",
   "kind": "The 2:1 constraint",
   "body": ["<b>A quadtree is balanced if adjacent leaves differ by at "
            "most one level</b> — the 2:1 rule.",
            "<b>Unbalanced trees produce hanging nodes</b> when converted "
            "to a mesh: a large cell's edge meets two small cells' edges, "
            "so the vertex in the middle belongs to one side only.",
            "<b>That produces cracks in a rendered surface and invalid "
            "elements in a simulation</b> — the classic LOD seam, "
            "and the reason terrain systems care.",
            "<b>Balancing costs only a constant factor in cell count</b>, "
            "which is a very cheap fix for a very visible problem."]},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "The decision, with reasons."},

  {"t": "bullets", "kicker": "Decision", "title": "Which structure, and why",
   "items": [
     "<b>Ray tracing against static geometry: BVH.</b> Overlapping nodes "
     "are fine; SAH construction is the standard (CSCE 647 M04).",
     "",
     "<b>Nearest neighbour on points, low dimension: k-d tree.</b>",
     "",
     "<b>Uniformly distributed, dynamic, many updates: uniform grid.</b> "
     "O(1) insert and remove beats any hierarchy.",
     "",
     "<b>Clustered and dynamic: loose octree or hierarchical hash grid.</b>",
     "",
     "<b>Solid classification and CSG: BSP.</b>",
     "",
     "<b>Terrain and LOD: balanced quadtree.</b>",
   ],
   "footnote": "<b>Measure on your data.</b> The constant factors and the "
               "memory layout usually decide this, not the asymptotics."},
 ],
 "takeaways": [
   "A BSP tree gives exact back-to-front ordering from any viewpoint from "
   "one offline build, at the cost of splitting geometry.",
   "BSP survived by changing jobs — solid classification, CSG, convex "
   "decomposition and PVS, not rendering order.",
   "A k-d tree splits the data at the median, so it is balanced by "
   "construction with depth O(log n).",
   "Orthogonal range query in a k-d tree is O(n^(1−1/k)), which is "
   "√n in 2D — not logarithmic — and degrades badly with "
   "dimension.",
   "Splitting data buys balance; splitting space buys implicit addressing "
   "via Morton codes and cache-coherent ordering.",
   "The 2:1 balance constraint on a quadtree prevents hanging nodes, which "
   "are the cause of LOD cracks and invalid simulation elements.",
 ],
 "notes": [
  ("h1", "1 &nbsp; BSP trees"),
  ("callout", "Exact visibility ordering from any viewpoint",
   ["<b>Each internal node stores a splitting plane</b>, and its two "
    "children store the geometry lying on each side. Geometry that crosses "
    "the plane is <i>split</i> into two pieces, one for each side — "
    "which is where the cost comes from.",
    "<b>To render back-to-front from any viewpoint:</b> at each node, "
    "determine which side the viewpoint is on, recurse into the far side, "
    "draw the node's own geometry, then recurse into the near side. "
    "<b>This yields an exact painter's-algorithm ordering with no "
    "per-frame sorting.</b>",
    "<b>The tree is built once, offline, and is correct for every "
    "viewpoint.</b> That is the remarkable property, and it is why Doom and "
    "Quake were built on BSP trees — before depth buffers were cheap "
    "in hardware, this was the only way to get correct occlusion at "
    "interactive rates.",
    "<b>The cost is splitting.</b> Every plane choice fragments the "
    "geometry that crosses it, and a poor sequence of choices can produce "
    "<b>O(n&#178;) fragments</b> from n input polygons. Plane selection "
    "— typically a scored heuristic trading balance against split "
    "count, evaluated over a random sample of candidate planes — is "
    "essentially the whole engineering problem."]),
  ("ul", ["<b>Solid modelling and CSG.</b> Boolean operations on solids "
          "are clean in a BSP formulation: each operation is a tree merge "
          "with classification at the leaves, and it sidesteps much of "
          "Module 06's boundary-walk difficulty.",
          "<b>Collision geometry.</b> A point, ray, or swept volume can be "
          "classified inside or outside a solid in O(depth), which is what "
          "the <code>.bsp</code> collision hulls in id-lineage engines "
          "do.",
          "<b>Portal and potentially-visible-set generation.</b> The leaves "
          "of a solid BSP are the convex cells between which portals are "
          "computed, in the offline visibility preprocessing step.",
          "<b>Convex decomposition.</b> The leaves of a solid BSP are "
          "convex by construction, which connects directly to Module 03 and "
          "Module 12's collision proxies.",
          "<b>Not for rendering order any more.</b> The z-buffer won that "
          "argument decisively, on cost and on simplicity. <b>BSP survived "
          "by changing jobs</b>, which is a common and underappreciated "
          "pattern for good data structures."]),

  ("h1", "2 &nbsp; k-d trees"),
  ("code", """BUILD(points, depth):
    if |points| <= leaf_size: return Leaf(points)
    axis = depth mod k                  # cycle x, y, z, x, ...
    m    = median along axis            # nth_element: linear time
    return Node(axis, m, BUILD(left, depth+1), BUILD(right, depth+1))

Build O(n log n); depth O(log n), BALANCED BY CONSTRUCTION
because the median splits the COUNT, not the space.

RANGE QUERY(node, box):
    if region DISJOINT from box:   return          # prune
    if region CONTAINED in box:    report all      # bulk report
    else recurse into both children                # straddle

O(n^(1-1/k) + m).  In 2D: O(sqrt(n) + m).  NOT logarithmic."""),
  ("callout", "k-d trees degrade with dimension, sooner than expected",
   ["<b>Orthogonal range query costs O(n<super>1&minus;1/k</super> + m)</b> "
    "for m reported points — &radic;n in two dimensions, "
    "n<super>2/3</super> in three, and approaching linear as k grows. "
    "<b>The square-root term surprises people who expect a tree to give "
    "logarithmic queries</b>; it arises because the query box boundary "
    "straddles many cells, and every straddled cell must be visited.",
    "<b>Nearest-neighbour search degrades similarly.</b> Above roughly "
    "twenty dimensions a k-d tree examines most of the data and is beaten "
    "outright by a linear scan, which has perfect memory locality and no "
    "branching.",
    "<b>The underlying reason is that a bounding box in high dimensions "
    "touches almost everything.</b> The volume of a high-dimensional box "
    "concentrates in its corners, the ratio of the inscribed sphere to the "
    "box vanishes, and so the pruning test almost never prunes. This is the "
    "curse of dimensionality in its most concrete form.",
    "<b>For graphics none of this matters</b> — k is 2 or 3 and the "
    "bounds are good. <b>For feature vectors and embeddings it matters "
    "enormously</b>, and approximate methods take over (Module 10)."]),

  ("break",),
  ("h1", "3 &nbsp; Quadtrees, octrees, and grids"),
  ("table", ["Structure", "What it splits", "Consequence"],
   [["<b>k-d tree</b>", "<b>The data, at the median.</b>",
     "<b>Always balanced; depth O(log n) regardless of distribution.</b> "
     "Cell positions must be stored explicitly."],
    ["<b>Quadtree / octree</b>", "<b>Space, at the midpoint.</b>",
     "<b>Depth depends entirely on how clustered the data is</b>, and can "
     "be unbounded with duplicate points. In exchange, cell position is "
     "implicit — see below."],
    ["<b>Uniform grid</b>", "Space, uniformly, with no hierarchy.",
     "<b>O(1) lookup and O(1) insert and remove</b>, which no hierarchy "
     "matches. <b>Fails badly on non-uniform data</b> — either the "
     "cells are too large to prune or there are too many of them."],
    ["<b>BVH</b>", "The data, by bounding volume.",
     "<b>Nodes may overlap</b>, so a query can descend both children. The "
     "best structure for ray tracing against static geometry (CSCE 647 "
     "Module 04)."],
    ["<b>BSP</b>", "Space, by an arbitrary plane.",
     "Fits the geometry rather than the axes, at the cost of splitting it."]],
   [0.18, 0.26, 0.56]),
  ("p", "<b>Splitting the data buys balance; splitting space buys implicit "
        "addressing.</b> That single trade organises this entire table, and "
        "knowing which side of it you need usually determines the choice."),
  ("callout", "Implicit addressing is the quadtree's real advantage",
   ["<b>A quadtree cell's position is fully determined by its path from the "
    "root</b>, so it can be encoded as a single integer — the Morton "
    "or Z-order code, formed by interleaving the bits of the coordinates.",
    "<b>So cells can live in a hash table or a sorted array with no "
    "pointers at all</b>, a parent or child code is obtained by shifting, "
    "and neighbours are found by bit arithmetic on the code. The tree "
    "structure is never materialised.",
    "<b>And Morton order is cache-coherent.</b> Points sorted by Morton "
    "code are spatially local in memory, so traversals and range queries "
    "get good locality for free — <b>which matters more on real "
    "hardware than the asymptotic difference from a k-d tree does</b>, and "
    "is why GPU spatial structures are overwhelmingly Morton-based.",
    "<b>The cost is that depth depends on the data.</b> A million points "
    "in one small region produces a very deep tree with mostly-empty nodes, "
    "and <b>exactly duplicated points produce infinite depth</b> unless the "
    "recursion is capped — which every implementation must do, and "
    "which is the first bug people hit."]),
  ("callout", "Balanced quadtrees and the 2:1 constraint",
   ["<b>A quadtree is <i>balanced</i> when adjacent leaf cells differ by at "
    "most one level of subdivision</b> — the 2:1 rule, so no cell is "
    "more than twice the size of its neighbour.",
    "<b>Unbalanced trees produce hanging nodes</b> when converted to a "
    "mesh: a large cell's single edge meets two smaller cells' edges, so "
    "the vertex at the midpoint belongs to the small side only and the "
    "large side knows nothing about it.",
    "<b>That produces visible cracks in a rendered surface and invalid "
    "elements in a simulation.</b> It is exactly the classic terrain LOD "
    "seam — a gap of background visible between two adjacent terrain "
    "patches at different detail levels — and it is why every terrain "
    "system has either a balance constraint or an explicit skirt or "
    "stitching pass.",
    "<b>Balancing costs only a constant factor in the number of cells</b> "
    "(the refinement propagates, but geometrically decreasing), <b>which is "
    "a very cheap fix for a very visible problem</b> and should essentially "
    "always be applied."]),

  ("h1", "4 &nbsp; Choosing"),
  ("ul", ["<b>Ray tracing against static geometry: BVH.</b> Overlapping "
          "nodes are acceptable because rays are tested against bounds "
          "cheaply, and SAH-guided construction is the standard (CSCE 647 "
          "Module 04).",
          "<b>Nearest neighbour on points in two or three dimensions: k-d "
          "tree.</b> Balanced, simple, and the bounds are good at low k.",
          "<b>Uniformly distributed, dynamic, many insertions and "
          "removals: uniform grid.</b> O(1) update beats any hierarchy, and "
          "particle systems and broad-phase collision are exactly this "
          "case.",
          "<b>Clustered and dynamic: loose octree or a hierarchical hash "
          "grid.</b> The looseness avoids objects straddling cell "
          "boundaries being pushed to the root.",
          "<b>Solid classification, CSG, and convex decomposition: "
          "BSP.</b>",
          "<b>Terrain, LOD, and anything with a view-dependent detail "
          "requirement: balanced quadtree.</b>",
          "<b>And measure on your own data.</b> At realistic sizes the "
          "constant factors and the memory layout usually decide this "
          "rather than the asymptotics — a flat Morton-sorted array "
          "frequently beats a pointer-based tree with better bounds."]),
 ],
 "resources": [
   ("de Berg et al. &mdash; Computational Geometry, chapters 5, 12, 14 "
    "(range searching, BSP, quadtrees)",
    "https://www.springer.com/gp/book/9783642096815",
    "The analyses behind &sect;2 and &sect;3, including the range-query "
    "bound and the quadtree balancing argument."),
   ("Samet &mdash; Foundations of Multidimensional and Metric Data "
    "Structures",
    "https://www.cs.umd.edu/~hjs/",
    "The exhaustive reference for everything in &sect;3. The author's "
    "course slides are free and are a good substitute."),
   ("Ericson &mdash; Real-Time Collision Detection, chapters 6–8",
    "https://realtimecollisiondetection.net/",
    "<b>The engine-facing treatment</b> — grids, hierarchies, loose "
    "octrees, and the practical choices of &sect;4."),
   ("Fabian Giesen &mdash; Morton codes and Z-order (free)",
    "https://fgiesen.wordpress.com/2009/12/13/decoding-morton-codes/",
    "The bit arithmetic behind &sect;3's implicit addressing, clearly "
    "explained."),
 ],
 "exercises": [
   "Build a BSP tree from a set of polygons and render back-to-front from "
   "several viewpoints.",
   "<b>Measure the fragment count</b> under random plane selection and "
   "under a balance-versus-splits heuristic. Report both.",
   "Use a solid BSP to classify points inside and outside a concave "
   "shape.",
   "Implement a k-d tree with median splitting and verify the depth is "
   "O(log n).",
   "<b>Measure range query cost against n</b> and confirm the √n "
   "behaviour in 2D.",
   "Measure nearest-neighbour cost as dimension rises from 2 to 50, "
   "against a linear scan. Find the crossover.",
   "Implement a quadtree with Morton codes and no pointers.",
   "<b>Implement 2:1 balancing</b>, and render a terrain patch with and "
   "without it to show the cracks.",
   "Compare a uniform grid, a quadtree, and a k-d tree on uniform and on "
   "heavily clustered data.",
   "Profile all three for cache behaviour and relate the result to "
   "CSCE 614 and CSCE 735.",
 ],
 "selfcheck": [
   "How does a BSP tree give viewpoint-independent ordering, and what does "
   "it cost?",
   "Name four current uses of BSP trees.",
   "Why is a k-d tree balanced by construction?",
   "State the range query bound and say why it is not logarithmic.",
   "Why do k-d trees fail in high dimensions?",
   "Contrast splitting data with splitting space.",
   "What is a Morton code and what two advantages does it give?",
   "What is the 2:1 constraint, what does it prevent, and what does it "
   "cost?",
 ],
},

]
