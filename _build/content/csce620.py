# -*- coding: utf-8 -*-
"""CSCE 620 Computational Geometry — original course content."""

COURSE = {
    "code": "CSCE 620",
    "title": "Computational Geometry",
    "tagline": "Hulls, triangulations, subdivision, and proximity — with "
               "the robustness problem treated as the subject rather than "
               "an appendix",
    "term": "Semester 5 (with CSCE 605 and CSCE 678)",
    "prereqs": "CSCE 629 Analysis of Algorithms; CSCE 641 Computer "
               "Graphics; CSCE 645 Geometric Modeling is helpful but not "
               "required",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A geometry library whose predicates are exact, whose "
                   "degeneracies are handled by name, and whose test suite "
                   "is built from the cases that break naive "
                   "implementations",
    "description": [
        "Computational geometry is the one subject in this program where "
        "<b>a correct algorithm, correctly implemented, routinely produces "
        "a wrong answer</b>. Not slowly, not approximately — wrong, "
        "and often catastrophically: a convex hull that is not convex, a "
        "triangulation with a hole in it, a point-in-polygon test that says "
        "both yes and no depending on which edge you ask.",
        "The reason is that <b>geometric algorithms are built on "
        "predicates</b> — questions like <i>is this point left of that "
        "line?</i> — and the textbook proofs assume those predicates "
        "are answered exactly. Floating point does not answer them exactly. "
        "It answers them <i>nearly</i> exactly, which for a combinatorial "
        "algorithm is worse than useless: a single inconsistent answer can "
        "drive the algorithm into a state its correctness proof never "
        "contemplated, and from there it may loop forever, crash, or "
        "quietly emit nonsense.",
        "So this course teaches the algorithms and the robustness problem "
        "together, which is how practitioners actually have to hold them. "
        "<b>Module 02 builds exact predicates before any algorithm needs "
        "them</b>, and every module afterwards says what its degeneracies "
        "are and how they are handled.",
        "The emphasis throughout is on the geometry an engine needs. "
        "<b>Convex hulls and decomposition feed collision detection; "
        "triangulation and Delaunay feed meshing; BSP trees, quadtrees, and "
        "k-d trees feed culling and spatial queries; visibility and "
        "configuration space feed navigation.</b> CSCE 649 assumed "
        "collision geometry worked. This course is where it comes from.",
    ],
    "outcomes": [
        "Explain why floating-point predicates break combinatorial "
        "algorithms, and quantify when.",
        "Implement exact and adaptive-precision geometric predicates.",
        "Implement convex hulls in two and three dimensions.",
        "Apply the plane-sweep paradigm to intersection and related "
        "problems.",
        "Triangulate polygons and perform boolean operations on them.",
        "Build and query BSP trees, k-d trees, and quadtrees or octrees.",
        "Construct Voronoi diagrams and Delaunay triangulations and "
        "explain their duality.",
        "Answer range, proximity, and nearest-neighbour queries "
        "efficiently.",
        "Compute visibility and plan motion in configuration space.",
        "Choose between writing geometry and using a library, with "
        "reasons.",
    ],
    "materials": [
        ("David Mount — CMSC 754 Computational Geometry lecture notes "
         "(free PDF)",
         "https://www.cs.umd.edu/class/spring2020/cmsc754/Lects/cmsc754-spring2020-lects.pdf",
         "<b>The primary source.</b> A complete graduate course in one "
         "carefully written document, free, and better paced than most "
         "textbooks. Read alongside every module."),
        ("de Berg, Cheong, van Kreveld & Overmars — Computational "
         "Geometry: Algorithms and Applications",
         "https://www.springer.com/gp/book/9783642096815",
         "The standard text, and the source of the canonical treatments of "
         "sweep, Voronoi, and range searching. Library copy; the authors' "
         "course slides are free."),
        ("Jonathan Shewchuk — Adaptive Precision Floating-Point "
         "Arithmetic and Fast Robust Geometric Predicates (free)",
         "https://www.cs.cmu.edu/~quake/robust.html",
         "<b>The reference for Module 02</b>, with working code. The paper "
         "that made exact predicates practical rather than theoretical."),
        ("CGAL — the Computational Geometry Algorithms Library",
         "https://www.cgal.org/",
         "The reference implementation of nearly everything in this course. "
         "Its documentation is itself a good secondary source, and its "
         "kernel design is the subject of Module 13."),
        ("Christer Ericson — Real-Time Collision Detection",
         "https://realtimecollisiondetection.net/",
         "The engine-facing companion. Where this course gives the "
         "algorithm, Ericson gives the shipping version. Library copy; the "
         "author's errata and notes are free."),
        ("TU Eindhoven — Computational Geometry course materials "
         "(free)",
         "https://www.win.tue.nl/~kbuchin/teaching/",
         "Slides and exercises from one of the groups that wrote the "
         "standard text."),
    ],
    "tooling": [
        "<b>C++ or Rust</b>, because Module 02 needs control over "
        "floating-point evaluation and both give it to you. <b>A language "
        "that silently reassociates your arithmetic cannot do this "
        "course.</b>",
        "<b>Shewchuk's <code>predicates.c</code></b>, or your own "
        "implementation of it. Module 02 writes one; after that you may "
        "use his.",
        "<b>A way to draw what you computed.</b> SVG output is enough and "
        "takes an afternoon. <b>Geometric bugs are visible and almost "
        "nothing else about them is</b> — debugging a triangulation "
        "from printed coordinates is a waste of a week.",
        "<b>Exact rational arithmetic</b> available for testing — "
        "Python's <code>fractions.Fraction</code>, Boost.Multiprecision, "
        "or GMP. Used to produce ground truth, not to ship.",
        "<b>A degenerate-input generator.</b> Collinear points, duplicate "
        "points, cocircular points, coincident edges. <b>You will write "
        "this in Module 01 and use it in every module after.</b>",
        "<b>CGAL installed</b>, for Module 13's comparison and for "
        "checking your answers throughout.",
    ],
    "projects": [
        {"title": "A robust 2D geometry kernel", "after": 7,
         "brief": "Build the foundation layer: exact predicates, convex "
                  "hull, segment intersection, triangulation, and boolean "
                  "operations — each one tested against the "
                  "degeneracies that break it.",
         "reqs": [
             "<b>Exact orientation and incircle predicates</b>, with an "
             "adaptive fast path, tested against exact rational arithmetic "
             "on inputs chosen to be near-degenerate.",
             "A convex hull that is correct on <b>collinear points, "
             "duplicate points, and all-identical points</b>, not merely "
             "on random clouds.",
             "Bentley–Ottmann segment intersection handling "
             "<b>coincident endpoints and three-or-more segments through "
             "one point</b>.",
             "Polygon triangulation that handles <b>holes</b>.",
             "<b>A degenerate-input test suite</b>, written before the "
             "code it tests.",
             "SVG output for every structure, used in the report.",
         ],
         "done": [
             "<b>A test suite in which every test is a case that breaks a "
             "naive implementation</b>, with a note on each saying what it "
             "breaks and why.",
             "A demonstration, with figures, that your hull is correct on "
             "input where a <code>double</code>-based orientation test "
             "produces a non-convex result.",
             "<b>A measured comparison of the adaptive predicate against "
             "both the naive and the fully exact versions</b> — "
             "showing the fast path is actually fast.",
             "<b>An honest list of the degeneracies you did not handle</b>, "
             "which is a legitimate engineering outcome when stated.",
         ]},
        {"title": "Spatial structure, applied", "after": 12,
         "brief": "Take the kernel into three dimensions and into a "
                  "query-answering structure. One structure, built "
                  "properly, measured against the alternatives.",
         "reqs": [
             "<b>Either</b> a Delaunay triangulation with a constrained "
             "variant and a quality-meshing pass; <b>or</b> a 3D spatial "
             "structure (BVH, k-d tree, or octree) with range and "
             "nearest-neighbour queries; <b>or</b> a 3D convex hull with "
             "GJK collision queries on top.",
             "Construction and query cost both measured, over varying "
             "input size and distribution.",
             "<b>A comparison against CGAL or an equivalent library</b> on "
             "correctness and on speed.",
             "<b>A clustered or adversarial input distribution</b>, not "
             "only uniform random — uniform random hides almost every "
             "interesting failure.",
             "Degeneracy handling stated explicitly.",
         ],
         "done": [
             "<b>Construction and query timings against input size and "
             "distribution</b>, plotted, with the asymptotic prediction "
             "overlaid and any divergence explained.",
             "<b>An honest comparison against the library version</b>, "
             "covering both correctness and performance.",
             "A statement of which input distributions degrade your "
             "structure and by how much.",
             "<b>A rendered figure of the structure on real input</b>, "
             "because geometry that cannot be looked at has not been "
             "checked.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Geometry a Machine Can Believe",
 "subtitle": "The algorithms are correct. The arithmetic is not.",
 "question": "Why do correct geometric algorithms produce wrong answers?",
 "outcomes": [
     "Explain the structure of a geometric algorithm: predicates plus "
     "combinatorics.",
     "Demonstrate a floating-point predicate giving an inconsistent "
     "answer.",
     "Explain why inconsistency is worse than inaccuracy.",
     "Name the standard degeneracies and why they are not edge cases.",
     "Set up the tooling this course needs.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What a geometric algorithm is",
   "blurb": "Two layers, and only one of them is reliable."},

  {"t": "callout", "title": "Every geometric algorithm has two layers",
   "kind": "The structure that explains the whole course",
   "body": ["<b>A numerical layer: predicates.</b> Small questions with "
            "discrete answers — is this point left of, right of, or on "
            "that line? Is this point inside, outside, or on that circle?",
            "<b>A combinatorial layer: the algorithm.</b> It builds a "
            "structure — a hull, a triangulation, a subdivision — by "
            "asking predicates and branching on the answers.",
            "<b>The correctness proof assumes the predicates are "
            "exact.</b> Every textbook proof in this subject makes that "
            "assumption silently.",
            "<b>Floating point breaks the assumption</b>, and the "
            "combinatorial layer has no defence against it. <b>That gap is "
            "the subject of this course.</b>"]},

  {"t": "eq", "kicker": "The predicate", "title": "Orientation: the one you cannot avoid",
   "eqs": [
     ("orient(a, b, c) = sign((b−a) × (c−a))",
      "Positive if c is left of the directed line a→b, negative if right, "
      "zero if collinear."),
     ("= sign((bₓ−aₓ)(c_y−a_y) − (b_y−a_y)(cₓ−aₓ))",
      "Twice the signed area of the triangle. Four subtractions, two "
      "multiplications, one subtraction."),
     ("Convex hull, triangulation, intersection, point location",
      "All of them are this predicate plus bookkeeping. Get it wrong and "
      "every one of them fails."),
   ],
   "caption": "<b>Seven floating-point operations</b>, and the correctness "
              "of most of this course rests on their sign.",
   "note": "Students underestimate how much rests on this one expression. "
           "Say it explicitly."},

  {"t": "section", "label": "Part 2", "title": "How it fails",
   "blurb": "Not inaccuracy — inconsistency."},

  {"t": "callout", "title": "The failure is inconsistency, not error",
   "kind": "The distinction that matters most",
   "body": ["<b>If a predicate is merely <i>inaccurate</i>, you get a "
            "slightly wrong answer.</b> Numerical analysis handles that, "
            "and most of engineering tolerates it.",
            "<b>If a predicate is <i>inconsistent</i>, you get an "
            "impossible one.</b> The algorithm can be told that c is left "
            "of ab, and a is left of bc, and b is left of ca — a "
            "configuration no three real points can have.",
            "<b>The algorithm's invariants now describe a world that does "
            "not exist.</b> It may loop forever, index past an array, or "
            "produce a structure that is not a structure.",
            "<b>So a geometry bug is rarely 'off by a little'.</b> It is a "
            "crash, a hang, or a hull that is not convex. <b>Tolerances do "
            "not fix this</b> — see Part 3."]},

  {"t": "code", "kicker": "Demonstration", "title": "The same three points, two answers",
   "lang": "cpp", "code": """
// orient() computed naively in double precision.
double orient(P a, P b, P c) {
    return (b.x-a.x)*(c.y-a.y) - (b.y-a.y)*(c.x-a.x);
}

// Three points that are very nearly collinear.
P a{0.5, 0.5}, b{12.0, 12.0}, c{24.0, 24.0};

//  orient(a,b,c)  ->  0.0          "collinear"
//  orient(b,c,a)  ->  0.0          "collinear"
//  orient(c,a,b)  ->  0.0          "collinear"      consistent, fine.

// Now perturb c by one unit in the last place:
c.y = nextafter(c.y, 25.0);

//  orient(a,b,c)  ->  +7.1e-15     "left"
//  orient(b,c,a)  ->  -3.6e-15     "right"     <-- CONTRADICTION
//  orient(c,a,b)  ->   0.0         "collinear" <-- and a third answer

// The SAME three points, in three cyclic orders that must agree,
// give three different answers. No algorithm survives this.
""",
   "caption": "The predicate is not merely imprecise. It is "
              "<b>self-contradictory</b>, and cyclic symmetry is the "
              "easiest way to see it.",
   "note": "Have them run this. Believing it from a slide is not the same "
           "as watching it happen."},

  {"t": "callout", "title": "Why the error is unbounded in the worst case",
   "kind": "The arithmetic",
   "body": ["<b>The subtractions come first.</b> When the points are close "
            "together, <code>b−a</code> and <code>c−a</code> lose most of "
            "their significant digits to cancellation.",
            "<b>Then the products amplify what is left.</b> The two "
            "products are nearly equal and are subtracted — a second "
            "cancellation, on values that were already mostly noise.",
            "<b>So the computed result can have no correct digits at "
            "all</b>, including its sign. The relative error is not small; "
            "it is unbounded.",
            "<b>And the sign is the entire output.</b> A predicate returns "
            "one of three values, so losing the sign loses everything."]},

  {"t": "section", "label": "Part 3", "title": "Why the obvious fixes fail",
   "blurb": "Epsilon is not an answer."},

  {"t": "table", "kicker": "Non-solutions", "title": "What people try first",
   "header": ["Attempt", "Why it fails"],
   "widths": [3.6, 8.5],
   "rows": [
     ["<b>Compare against an epsilon</b>", "<b>Makes 'collinear' non-transitive; the inconsistency moves, it does not go</b>"],
     ["Use long double or float128", "<b>Buys digits, not exactness. The same failure, further out</b>"],
     ["Snap inputs to a grid", "Changes the problem; can create new degeneracies"],
     ["<b>Retry with jitter on failure</b>", "<b>Non-deterministic output. Unshippable</b>"],
     ["Catch the crash and skip", "<b>Silent wrong answers, which is worse</b>"],
   ],
   "footnote": "<b>Only exact predicates fix it</b>, and Module 02 shows "
               "they are affordable.",
   "note": "The epsilon row is the important one — nearly everyone reaches "
           "for it first and it actively makes things harder to reason "
           "about."},

  {"t": "callout", "title": "Epsilon makes 'equal' non-transitive",
   "kind": "The specific reason tolerances fail",
   "body": ["<b>With a tolerance, <i>a</i> may be collinear with "
            "<i>b</i>, and <i>b</i> with <i>c</i>, while <i>a</i> is not "
            "collinear with <i>c</i>.</b>",
            "<b>Algorithms rely on transitivity constantly</b> — to merge "
            "collinear runs, to classify a point once and reuse the "
            "classification, to sort.",
            "<b>A comparator built on an epsilon is not a valid strict "
            "weak ordering</b>, so <code>std::sort</code> on it is "
            "undefined behaviour and does in practice read out of bounds.",
            "<b>So the tolerance does not remove the inconsistency.</b> It "
            "relocates it to inputs that are harder to construct and "
            "therefore harder to test."]},

  {"t": "section", "label": "Part 4", "title": "Degeneracy",
   "blurb": "The cases that are not edge cases."},

  {"t": "bullets", "kicker": "The list", "title": "The standard degeneracies",
   "items": [
     "<b>Three or more collinear points</b> — hull and triangulation.",
     "",
     "<b>Four or more cocircular points</b> — Delaunay is then not "
     "unique.",
     "",
     "<b>Duplicate or coincident points</b> — and points differing by one "
     "ULP, which is worse.",
     "",
     "<b>Segments sharing an endpoint</b>, overlapping collinear segments, "
     "three segments through one point.",
     "",
     "<b>Vertical segments</b>, when the algorithm sorts by x.",
     "",
     "<b>Zero-area triangles, zero-length edges, empty polygons.</b>",
   ],
   "footnote": "<b>Real data is full of these</b> — CAD output, grids, and "
               "anything authored by a human are all highly degenerate.",
   "note": "The key reframing: degeneracy is the common case in real data, "
           "not the rare one. Random points are the unusual input."},

  {"t": "callout", "title": "Random input is the unrepresentative case",
   "kind": "Why testing on point clouds proves nothing",
   "body": ["<b>Uniform random points are almost surely in general "
            "position.</b> No three collinear, no four cocircular, no "
            "duplicates.",
            "<b>So a naive implementation passes every random test</b>, at "
            "every size, indefinitely.",
            "<b>And real input is the opposite.</b> CAD models, tile grids, "
            "terrain, and hand-authored geometry are saturated with right "
            "angles, shared vertices, and axis-aligned edges.",
            "<b>So test on grids, on lattices, on repeated points, and on "
            "the output of your own earlier passes</b> — which is where "
            "the degeneracies you created yourself come back."]},

  {"t": "bullets", "kicker": "Setup", "title": "What to have working before Module 02",
   "items": [
     "<b>A point and segment type</b>, and an <code>orient</code> you can "
     "swap implementations of behind one interface.",
     "",
     "<b>SVG output.</b> An afternoon's work, and it pays for itself in "
     "the first bug.",
     "",
     "<b>Exact rational arithmetic</b> for ground truth — "
     "<code>Fraction</code> in Python is enough to check against.",
     "",
     "<b>A degenerate-input generator:</b> lattice points, collinear runs, "
     "duplicates, cocircular sets, and near-misses at one ULP.",
     "",
     "<b>The cyclic-consistency check</b> from Part 2, as a test you can "
     "run against any predicate implementation.",
   ],
   "footnote": "<b>Build the generator now.</b> Every module after this "
               "one uses it, and writing it later means re-testing "
               "everything."},
 ],
 "takeaways": [
   "A geometric algorithm is a numerical predicate layer plus a "
   "combinatorial layer, and the correctness proofs assume the predicates "
   "are exact.",
   "Floating-point predicates fail by being inconsistent rather than "
   "inaccurate — they can report configurations no real points can "
   "have.",
   "Orientation suffers two successive cancellations, so its computed "
   "value can have no correct digits, including its sign.",
   "Epsilon tolerances make equality non-transitive, which breaks sorting "
   "and merging and relocates the bug rather than removing it.",
   "Degeneracies — collinear, cocircular, duplicate, coincident — "
   "are the common case in real authored data, not edge cases.",
   "Uniform random input is almost surely in general position, so passing "
   "random tests establishes nothing.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The structure of a geometric algorithm"),
  ("callout", "Every geometric algorithm has two layers",
   ["<b>A numerical layer: the predicates.</b> These are small questions "
    "with discrete answers — <i>is this point left of, right of, or "
    "exactly on that directed line?</i>, <i>is this point inside, outside, "
    "or exactly on that circle?</i> Each one reduces to the sign of a "
    "polynomial in the input coordinates.",
    "<b>A combinatorial layer: the algorithm proper.</b> It builds a "
    "structure — a convex hull, a triangulation, a planar subdivision "
    "— by asking predicates and branching on their answers, "
    "maintaining invariants as it goes.",
    "<b>The correctness proof assumes the predicates are answered "
    "exactly.</b> Every proof in every textbook on this subject makes that "
    "assumption, and almost none of them state it. The proof is about the "
    "combinatorial layer and it takes the numerical layer as given.",
    "<b>Floating point breaks the assumption, and the combinatorial layer "
    "has no defence.</b> It cannot detect that it was lied to, because the "
    "lie is indistinguishable from a legitimate answer. <b>That gap is the "
    "subject of this course</b>, and treating it as an implementation "
    "detail to be handled later is the single most common way geometric "
    "code fails."]),
  ("eq", "orient(a, b, c) = sign[ (b<sub>x</sub>&minus;a<sub>x</sub>)"
         "(c<sub>y</sub>&minus;a<sub>y</sub>) &minus; "
         "(b<sub>y</sub>&minus;a<sub>y</sub>)(c<sub>x</sub>&minus;"
         "a<sub>x</sub>) ]"),
  ("p", "This is twice the signed area of triangle <i>abc</i>: positive "
        "when <i>c</i> lies to the left of the directed line "
        "<i>a</i>&rarr;<i>b</i>, negative when it lies to the right, and "
        "zero when the three are collinear. <b>Four subtractions, two "
        "multiplications, and a final subtraction — seven "
        "floating-point operations on which the correctness of convex "
        "hulls, triangulations, segment intersection, and point location "
        "all rest.</b> It is worth pausing on how much weight that one "
        "expression carries."),

  ("h1", "2 &nbsp; How it fails"),
  ("callout", "The failure is inconsistency, not error",
   ["<b>If a predicate is merely <i>inaccurate</i>, the result is slightly "
    "wrong.</b> That is the familiar situation in numerical computing, it "
    "is what error analysis is for, and most engineering tolerates it "
    "comfortably.",
    "<b>If a predicate is <i>inconsistent</i>, the result is "
    "impossible.</b> The algorithm can be told that <i>c</i> is left of "
    "<i>ab</i>, that <i>a</i> is left of <i>bc</i>, and that <i>b</i> is "
    "left of <i>ca</i> — a configuration that no three points in the "
    "real plane can have.",
    "<b>The algorithm's invariants now describe a world that does not "
    "exist.</b> A hull-construction loop that pops vertices while they are "
    "non-convex may pop the entire stack and index past the bottom. A sweep "
    "that assumes an event ordering may process events in an order its "
    "state machine has no transition for. <b>The usual outcomes are an "
    "infinite loop, an out-of-bounds access, or a structure that violates "
    "its own definition.</b>",
    "<b>So a geometry bug is rarely 'off by a little'.</b> It is a hang, a "
    "crash, or a convex hull that is not convex — and the input that "
    "triggers it looks entirely ordinary. <b>Tolerances do not fix "
    "this</b>, for the reason in &sect;3."]),
  ("code", """double orient(P a, P b, P c) {        // naive, double precision
    return (b.x-a.x)*(c.y-a.y) - (b.y-a.y)*(c.x-a.x);
}

P a{0.5,0.5}, b{12.0,12.0}, c{24.0,24.0};
c.y = nextafter(c.y, 25.0);           // perturb by ONE ulp

orient(a,b,c)  ->  +7.1e-15   "left"
orient(b,c,a)  ->  -3.6e-15   "right"       <-- contradiction
orient(c,a,b)  ->   0.0       "collinear"   <-- and a third answer

// The same three points, in three cyclic orders that MUST agree,
// return three different answers."""),
  ("p", "<b>Run this before reading further.</b> The cyclic orders of three "
        "points describe the same triangle with the same orientation, so "
        "all three calls must return the same sign. Watching them disagree "
        "is more convincing than any argument about it, and the "
        "cyclic-consistency check makes a good permanent test for any "
        "predicate implementation."),
  ("callout", "Why the error is unbounded, not small",
   ["<b>The subtractions come first.</b> When the three points are close "
    "together relative to their distance from the origin, "
    "<code>b&minus;a</code> and <code>c&minus;a</code> lose most of their "
    "significant digits to catastrophic cancellation — the leading "
    "digits agree and cancel, leaving the trailing rounding noise promoted "
    "to the front.",
    "<b>Then the products amplify what remains.</b> The two products are "
    "nearly equal and are subtracted from one another, which is a second "
    "cancellation applied to values that were already mostly noise.",
    "<b>So the computed result can have no correct digits whatsoever, "
    "including its sign.</b> The relative error is not bounded by any small "
    "constant; in the worst case it is unbounded, and the computed value "
    "bears no relation to the true one.",
    "<b>And the sign <i>is</i> the entire output.</b> A predicate returns "
    "one of three discrete values. Losing a few digits of a magnitude is "
    "survivable; losing the sign loses the whole answer, and the caller "
    "cannot tell that it happened."]),

  ("break",),
  ("h1", "3 &nbsp; Why the obvious fixes fail"),
  ("table", ["Attempted fix", "Why it does not work"],
   [["<b>Compare against an epsilon:</b> treat |orient| &lt; &epsilon; as "
     "collinear.",
     "<b>Makes 'collinear' non-transitive</b>, which breaks sorting and "
     "merging — see the callout below. The inconsistency is relocated, "
     "not removed, and it moves to inputs that are harder to construct and "
     "therefore harder to test."],
    ["<b>Use <code>long double</code>, <code>float128</code>, or "
     "doubled-double.</b>",
     "<b>Buys digits, not exactness.</b> Every one of these has a finite "
     "precision and therefore a cancellation regime. The same failure "
     "occurs, on inputs slightly further out, and it is now much rarer "
     "— which makes it harder to find and no less fatal."],
    ["<b>Snap all inputs to a fixed grid.</b>",
     "<b>A real technique, but it changes the problem</b>, and naive "
     "snapping can create degeneracies that were not in the input (two "
     "distinct points snapping together) or move a point across a line it "
     "was on the other side of. Principled versions exist — snap "
     "rounding, Module 13."],
    ["<b>Detect failure and retry with a small random perturbation.</b>",
     "<b>Non-deterministic output.</b> The same input produces different "
     "results on different runs, which is unacceptable in a build pipeline "
     "or an asset tool, and makes bugs unreproducible."],
    ["<b>Catch the crash and skip the input.</b>",
     "<b>Converts loud failures into silent wrong answers</b>, which is "
     "strictly worse. The crash was the only thing telling you the output "
     "was invalid."]],
   [0.37, 0.63]),
  ("callout", "Epsilon makes equality non-transitive",
   ["<b>With a tolerance, <i>a</i> can be collinear with <i>b</i>, and "
    "<i>b</i> collinear with <i>c</i>, while <i>a</i> is not collinear with "
    "<i>c</i>.</b> Each pairwise test falls under the threshold; the "
    "endpoints together do not.",
    "<b>Algorithms rely on transitivity constantly</b> — to merge runs "
    "of collinear points into one edge, to classify a point once and reuse "
    "that classification elsewhere, and above all to sort.",
    "<b>A comparator built on an epsilon is not a valid strict weak "
    "ordering.</b> This is not a theoretical objection: passing such a "
    "comparator to <code>std::sort</code> is undefined behaviour, and the "
    "standard implementations do in practice run off the end of the "
    "sequence and corrupt memory. The crash appears inside the sort, which "
    "is nowhere near the geometry that caused it.",
    "<b>So the tolerance does not remove the inconsistency.</b> It moves it "
    "from inputs that differ by one ULP — which are at least easy to "
    "generate deliberately — to inputs that straddle the threshold, "
    "which are not. <b>Module 02 shows that exactness is affordable</b>, "
    "which makes this entire row of trade-offs unnecessary."]),

  ("h1", "4 &nbsp; Degeneracy"),
  ("ul", ["<b>Three or more collinear points.</b> Breaks convex hull "
          "(which vertices belong?) and triangulation (a zero-area "
          "triangle).",
          "<b>Four or more cocircular points.</b> The Delaunay "
          "triangulation is then <i>not unique</i> (Module 09), and an "
          "algorithm that assumes uniqueness has no defined behaviour.",
          "<b>Duplicate or coincident points</b> — and, worse, points "
          "that differ by one ULP, which are not equal but are closer "
          "together than any predicate can resolve.",
          "<b>Segments sharing an endpoint</b>, collinear overlapping "
          "segments, and three or more segments passing through a single "
          "point (Module 04).",
          "<b>Vertical segments</b>, whenever the algorithm sweeps or sorts "
          "by x and implicitly assumed distinct x-coordinates.",
          "<b>Zero-area triangles, zero-length edges, empty or "
          "self-intersecting polygons</b>, and polygons whose first and "
          "last vertices coincide."]),
  ("callout", "Random input is the unrepresentative case",
   ["<b>Uniform random points are, with probability one, in general "
    "position.</b> No three are collinear, no four cocircular, and no two "
    "coincide. This is a theorem, not an observation.",
    "<b>So a naive implementation passes every random test you write</b>, "
    "at every size, for as long as you care to run it. Random testing "
    "provides essentially no evidence about the robustness of geometric "
    "code, which is a genuinely counterintuitive fact given how well it "
    "works elsewhere.",
    "<b>And real input is the exact opposite.</b> CAD output, tile grids, "
    "terrain heightfields, architectural models, and anything authored by a "
    "human are saturated with right angles, shared vertices, axis-aligned "
    "edges, and repeated coordinates. <b>Degeneracy is the common case in "
    "real data.</b>",
    "<b>So test on lattices and grids, on deliberate collinear runs, on "
    "duplicated and one-ULP-apart points, on cocircular sets — and on "
    "the output of your own earlier passes</b>, which is where the "
    "degeneracies you generated yourself come back to be consumed by the "
    "next stage."]),
  ("ul", ["<b>A point and segment type, and an <code>orient</code> behind "
          "one interface</b> whose implementation you can swap. Modules 02 "
          "and 13 both replace it.",
          "<b>SVG output.</b> An afternoon's work, and it pays for itself "
          "during the first bug. <b>Geometric errors are obvious when drawn "
          "and nearly invisible otherwise</b> — debugging a "
          "triangulation from printed coordinates wastes days.",
          "<b>Exact rational arithmetic for ground truth.</b> Python's "
          "<code>fractions.Fraction</code> is enough; it is far too slow to "
          "ship and perfectly suited to deciding what the right answer was.",
          "<b>A degenerate-input generator:</b> lattice points, collinear "
          "runs, duplicates, cocircular sets, near-misses at one ULP, and "
          "axis-aligned configurations. <b>Build it now</b> — every "
          "module after this one uses it, and writing it later means "
          "re-testing everything you have already built.",
          "<b>The cyclic-consistency check from &sect;2</b>, as a permanent "
          "test applicable to any predicate implementation you write."]),
 ],
 "resources": [
   ("Mount &mdash; CMSC 754 lecture notes, Lecture 1 (free PDF)",
    "https://www.cs.umd.edu/class/spring2020/cmsc754/Lects/cmsc754-spring2020-lects.pdf",
    "The framing of &sect;1 and the orientation primitive, done "
    "carefully."),
   ("Shewchuk &mdash; Robust Adaptive Floating-Point Geometric Predicates "
    "(free)",
    "https://www.cs.cmu.edu/~quake/robust.html",
    "<b>The paper behind &sect;2 and &sect;3.</b> Section 1 alone is the "
    "best statement of the problem in print, and Module 02 builds its "
    "machinery."),
   ("Kettner, Mehlhorn, Pion, Schirra & Yap &mdash; Classroom Examples of "
    "Robustness Problems in Geometric Computations (free)",
    "https://web.archive.org/web/20240420100137/https://people.mpi-inf.mpg.de/~mehlhorn/ftp/ClassroomExamples.pdf",
    "<b>Worked failures with figures:</b> convex hulls that are not convex, "
    "produced by correct algorithms. Short, and it settles the matter for "
    "anyone still unconvinced."),
   ("Goldberg &mdash; What Every Computer Scientist Should Know About "
    "Floating-Point Arithmetic (free)",
    "https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html",
    "The cancellation analysis of &sect;2, from first principles."),
 ],
 "exercises": [
   "Implement the naive <code>orient</code> and the cyclic-consistency "
   "check. Find an input on which the three cyclic orders disagree.",
   "<b>Characterise the failure region:</b> fix <i>a</i> and <i>b</i>, "
   "sweep <i>c</i> over a fine grid near the line, and plot where the "
   "computed sign differs from the exact one.",
   "Repeat the above in <code>float</code>, <code>double</code>, and "
   "<code>long double</code>. Report how the failure region shrinks and "
   "confirm it does not vanish.",
   "Implement <code>orient</code> with <code>Fraction</code> and use it as "
   "ground truth for the previous two exercises.",
   "<b>Build an epsilon-based collinearity test and demonstrate "
   "non-transitivity</b> with three explicit points.",
   "Write a comparator using that epsilon test and sort with it. Report "
   "what happens, and at what input size.",
   "Implement SVG output for points, segments, and polygons.",
   "<b>Write the degenerate-input generator</b>: lattice points, collinear "
   "runs, duplicates, one-ULP pairs, cocircular sets, axis-aligned "
   "configurations.",
   "Generate 10,000 uniform random point sets and verify that none contain "
   "three collinear points. Explain the result.",
   "Take a mesh or CAD file you have and count its degeneracies: duplicate "
   "vertices, collinear triples, zero-area faces.",
 ],
 "selfcheck": [
   "What are the two layers of a geometric algorithm, and which does the "
   "correctness proof concern?",
   "Write the orientation predicate and say what its sign means.",
   "Distinguish an inaccurate predicate from an inconsistent one, and say "
   "why the second is worse.",
   "Why can the computed orientation have no correct digits at all?",
   "Give five attempted fixes and say why each fails.",
   "Why does an epsilon tolerance break <code>std::sort</code>?",
   "Name six standard degeneracies.",
   "Why does passing random tests establish nothing about robustness?",
 ],
},

]

for _b in ("c620_b2", "c620_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
