# -*- coding: utf-8 -*-
"""CSCE 620 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Voronoi Diagrams",
 "subtitle": "Partitioning space by who is nearest.",
 "question": "Which site is closest to each point of the plane?",
 "outcomes": [
     "Define the Voronoi diagram and state its structural properties.",
     "Explain why it has linear complexity.",
     "Implement Fortune's sweep and explain the beach line.",
     "Apply the lifting map and connect it to convex hulls.",
     "Name the variants and what they are used for.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Structure",
   "blurb": "What the diagram is, and how big."},

  {"t": "callout", "title": "The definition, and three consequences",
   "kind": "What a Voronoi diagram is",
   "body": ["<b>Given n sites, the Voronoi cell of a site is the set of "
            "points closer to it than to any other site.</b>",
            "<b>Each cell is convex</b>, because it is an intersection of "
            "half-planes — one per other site, bounded by the "
            "perpendicular bisector.",
            "<b>Every cell is nonempty</b>, and the unbounded cells are "
            "exactly those of the convex hull vertices (Module 03).",
            "<b>And the whole diagram has only O(n) vertices and "
            "edges</b> — despite being an intersection of O(n&#178;) "
            "half-planes. <b>That is the non-obvious fact.</b>"]},

  {"t": "eq", "kicker": "Complexity", "title": "Why it is linear, not quadratic",
   "eqs": [
     ("The diagram is a planar straight-line graph",
      "Vertices, edges, and faces, with no crossings."),
     ("Euler: V − E + F = 2",
      "With F = n + 1 (n cells plus the outer face)."),
     ("Every Voronoi vertex has degree ≥ 3  ⟹  V ≤ 2n − 5,  E ≤ 3n − 6",
      "So the total size is linear in n. The quadratic half-plane count "
      "collapses."),
   ],
   "caption": "<b>Planarity is doing all the work.</b> The same argument "
              "bounds any planar subdivision.",
   "note": "Students find the linearity surprising; the Euler argument is "
           "short enough to do live."},

  {"t": "callout", "title": "A Voronoi vertex is equidistant from three sites",
   "kind": "The link to the incircle predicate",
   "body": ["<b>A vertex of the diagram is where three cells meet</b>, so "
            "it is equidistant from three sites — it is the "
            "circumcentre of their triangle.",
            "<b>And the circle through those three sites is empty</b> of "
            "all other sites, by definition of 'closest'.",
            "<b>So the predicate is incircle</b> (Module 02): is a fourth "
            "site inside the circle through these three?",
            "<b>Four cocircular sites give a degree-4 vertex</b>, which is "
            "the degeneracy — and it is exactly the case that makes the "
            "dual Delaunay triangulation non-unique (Module 09)."]},

  {"t": "section", "label": "Part 2", "title": "Fortune's algorithm",
   "blurb": "A sweep, with a curved status line."},

  {"t": "code", "kicker": "Fortune", "title": "Sweeping with a beach line",
   "lang": "text", "code": """
  THE PROBLEM with a straight sweep line: a Voronoi vertex can be
  discovered BEFORE the sweep reaches the site that created it.
  The output is not monotone in the sweep direction.

  THE FIX: sweep a line, but maintain the BEACH LINE -- the
  boundary of the region already determined. Each site behind
  the sweep contributes a PARABOLIC arc (equidistant from the
  site and the sweep line). The beach line is their lower envelope.

  STATUS:  the sequence of parabolic arcs, in x order
  EVENTS:  SITE events   -- the sweep reaches a new site
           CIRCLE events -- an arc shrinks to zero width

  SITE EVENT:    split the arc above the new site into two,
                 inserting a new arc between them
  CIRCLE EVENT:  an arc vanishes; its two neighbours become
                 adjacent and a VORONOI VERTEX is output there

  O(n log n), and it is optimal.
""",
   "caption": "<b>The beach line is the invention.</b> It makes the output "
              "monotone in the sweep direction, which is what a sweep "
              "requires.",
   "note": "Explain why a naive sweep fails first — the fix is only "
           "interesting once the problem is clear."},

  {"t": "callout", "title": "False circle events are normal, not a bug",
   "kind": "The implementation detail that confuses people",
   "body": ["<b>A circle event is queued when three consecutive arcs could "
            "converge.</b> But a later site event may split one of those "
            "arcs first.",
            "<b>The queued event is then invalid</b> and must not produce "
            "a vertex.",
            "<b>The standard handling is lazy deletion:</b> each arc holds "
            "a pointer to its pending circle event, and splitting the arc "
            "marks that event invalid.",
            "<b>Pop and discard invalid events.</b> This is not an error "
            "path — it happens constantly, and an implementation that "
            "treats it as exceptional will be wrong."]},

  {"t": "section", "label": "Part 3", "title": "The lifting map",
   "blurb": "Voronoi is a convex hull in disguise."},

  {"t": "eq", "kicker": "Lifting", "title": "Project onto a paraboloid",
   "eqs": [
     ("(x, y)  ↦  (x, y, x² + y²)",
      "Lift each site from the plane onto the paraboloid z = x² + y²."),
     ("Lower convex hull of the lifted points, projected down",
      "= the Delaunay triangulation of the original sites."),
     ("Voronoi = dual of Delaunay",
      "So one 3D convex hull gives you both diagrams."),
   ],
   "caption": "<b>Module 03's parabola trick, one dimension up.</b> The "
              "incircle predicate is exactly <code>orient3d</code> on the "
              "lifted points.",
   "note": "This unification is the most satisfying result in the course — "
           "give it room."},

  {"t": "callout", "title": "Why the lifting map matters practically",
   "kind": "Not merely elegant",
   "body": ["<b>It means Delaunay and Voronoi need no new algorithm</b> — "
            "a 3D convex hull code (Module 03) computes both.",
            "<b>It explains the incircle predicate.</b> 'Is d inside the "
            "circle through a, b, c?' becomes 'is the lifted d below the "
            "plane through the lifted a, b, c?' — which is "
            "<code>orient3d</code>.",
            "<b>And it generalises.</b> Voronoi in d dimensions is a "
            "convex hull in d + 1, so the same code handles every "
            "dimension.",
            "<b>It is also why <code>qhull</code> computes Delaunay "
            "triangulations</b> — it is a hull program being used exactly "
            "as this map suggests."]},

  {"t": "section", "label": "Part 4", "title": "Variants",
   "blurb": "The generalisations that get used."},

  {"t": "table", "kicker": "Variants", "title": "Voronoi variants and their uses",
   "header": ["Variant", "Change", "Used for"],
   "widths": [2.9, 4.1, 5.1],
   "rows": [
     ["<b>Power / Laguerre</b>", "<b>Weighted sites; cells by power distance</b>", "<b>Spheres of differing radii; molecules</b>"],
     ["<b>Centroidal (CVT)</b>", "<b>Site = centroid of its own cell</b>", "<b>Remeshing, stippling, sampling</b>"],
     ["Generalised", "Sites are segments or polygons", "Medial axis; toolpaths; NPC spacing"],
     ["<b>Higher-order</b>", "Cells by the k nearest sites", "k-nearest-neighbour queries"],
     ["<b>Farthest-point</b>", "<b>Cells by the <i>farthest</i> site</b>", "<b>Smallest enclosing circle</b>"],
     ["Manhattan / L∞", "Different metric", "Grid worlds; VLSI routing"],
   ],
   "footnote": "<b>Centroidal Voronoi via Lloyd's algorithm is the one "
               "that appears most in graphics</b> — it is how blue "
               "noise and good remeshes are produced.",
   "note": "CVT connects to CSCE 647's sampling material."},

  {"t": "callout", "title": "Where this shows up in an engine",
   "kind": "Applications",
   "body": ["<b>Fracture and destruction:</b> a Voronoi partition of a "
            "solid gives convincing shards, and the cells are convex so "
            "they are already collision-ready (Module 03).",
            "<b>Procedural texture and terrain:</b> Worley noise is a "
            "Voronoi distance field, used for cells, cracks, and "
            "scales.",
            "<b>Blue-noise sampling and stippling</b> via Lloyd relaxation "
            "— better than random for every sampling job (CSCE 647 M06).",
            "<b>Territory, influence maps, and NPC spacing</b>, and the "
            "medial axis for skeletons and for navmesh generation "
            "(Module 11)."]},
 ],
 "takeaways": [
   "A Voronoi cell is an intersection of half-planes and so is convex; the "
   "unbounded cells are exactly the convex hull vertices.",
   "Despite arising from O(n²) half-planes the diagram has only O(n) "
   "vertices and edges, by Euler's formula and planarity.",
   "A Voronoi vertex is the circumcentre of three sites with an empty "
   "circumcircle, so the predicate is incircle.",
   "A straight sweep fails because output is not monotone; Fortune's beach "
   "line of parabolic arcs fixes exactly that.",
   "False circle events are routine and are handled by lazy deletion, not "
   "treated as errors.",
   "Lifting to the paraboloid turns Delaunay into a 3D convex hull and "
   "incircle into orient3d — one algorithm serves both diagrams.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Structure"),
  ("callout", "The definition and three consequences",
   ["<b>Given n sites in the plane, the Voronoi cell of a site is the set "
    "of all points strictly closer to it than to any other site.</b> The "
    "cells partition the plane; the boundaries are the points equidistant "
    "from two or more sites.",
    "<b>Each cell is convex</b>, because it is the intersection of n "
    "&minus; 1 half-planes — one for each other site, bounded by the "
    "perpendicular bisector of the two. Convexity is immediate and it is "
    "what makes the cells useful downstream.",
    "<b>Every cell is nonempty</b> (a site is in its own cell), and <b>the "
    "unbounded cells are exactly those belonging to convex hull "
    "vertices</b> — a site has an unbounded cell if and only if it is "
    "on the hull (Module 03), which is a pleasing link between the two "
    "structures.",
    "<b>And the whole diagram has only O(n) vertices and edges</b>, despite "
    "each cell being defined as an intersection of O(n) half-planes and the "
    "total count of half-planes being quadratic. <b>That is the "
    "non-obvious structural fact</b>, and it is what makes the diagram "
    "computable in O(n log n)."]),
  ("eq", "V &minus; E + F = 2 &nbsp;&nbsp;&nbsp; F = n + 1 "
         "&nbsp;&nbsp;&nbsp; deg(v) &ge; 3 &nbsp;&rArr;&nbsp; "
         "V &le; 2n &minus; 5, &nbsp; E &le; 3n &minus; 6"),
  ("p", "The diagram is a planar straight-line graph, so Euler's formula "
        "applies with F = n + 1 — the n cells plus the unbounded outer "
        "face. Every Voronoi vertex has degree at least three (it is "
        "equidistant from at least three sites), and summing degrees gives "
        "2E &ge; 3V. Combining the two yields the linear bounds. <b>Planarity "
        "is doing all the work here</b>, and the same argument bounds the "
        "size of any planar subdivision — which is worth remembering, "
        "because it is the reason planar structures are tractable and their "
        "three-dimensional analogues frequently are not."),
  ("callout", "A Voronoi vertex is equidistant from three sites",
   ["<b>A vertex of the diagram is a point where three or more cells "
    "meet</b>, so it is equidistant from three sites — which makes it "
    "exactly the circumcentre of the triangle those sites form.",
    "<b>And the circle through those three sites contains no other "
    "site.</b> If it did, that site would be closer to the vertex than the "
    "three are, contradicting the vertex being on all three cell "
    "boundaries. <b>The empty circumcircle property is the definition in "
    "disguise.</b>",
    "<b>So the predicate needed is incircle</b> (Module 02 &sect;2): given "
    "three sites and a fourth, is the fourth inside their circumcircle? "
    "Every Voronoi and Delaunay algorithm is built on this one test.",
    "<b>Four cocircular sites produce a degree-4 vertex</b> instead of two "
    "degree-3 vertices joined by a zero-length edge. That is the "
    "degeneracy, it is why the incircle predicate must be exact, and it is "
    "exactly the configuration that makes the dual Delaunay triangulation "
    "non-unique (Module 09 &sect;1)."]),

  ("h1", "2 &nbsp; Fortune's algorithm"),
  ("code", """WHY A NAIVE SWEEP FAILS: a Voronoi vertex can be discovered
BEFORE the sweep line reaches the site that created it, so the
output is not monotone in the sweep direction.

THE FIX -- the BEACH LINE: each site already passed contributes a
PARABOLIC arc (points equidistant from that site and the sweep
line). The beach line is the lower envelope of those parabolas,
and everything above it IS already determined.

STATUS: the sequence of arcs, in x order
EVENTS: SITE   -- sweep reaches a new site: split the arc above it
        CIRCLE -- an arc shrinks to zero: its neighbours become
                  adjacent, and a VORONOI VERTEX is emitted there

O(n log n), and optimal."""),
  ("p", "<b>The beach line is the invention</b>, and it is worth seeing "
        "what it buys: it makes the determined region monotone in the "
        "sweep direction, which is precisely the property a plane sweep "
        "(Module 04) requires and which the Voronoi diagram does not "
        "naturally have. Fortune's contribution was recognising that "
        "sweeping a <i>curve</i> rather than a line restores it."),
  ("callout", "False circle events are normal, not an error path",
   ["<b>A circle event is queued whenever three consecutive arcs on the "
    "beach line could converge to a point.</b> It records where a Voronoi "
    "vertex would appear if nothing intervenes.",
    "<b>But a later site event may split one of those three arcs "
    "first</b>, destroying the configuration. The queued event is then "
    "invalid and must not produce a vertex.",
    "<b>The standard handling is lazy deletion:</b> each arc holds a "
    "pointer to its pending circle event, and splitting or removing the arc "
    "marks that event invalid. Nothing is removed from the priority queue, "
    "which would cost a search.",
    "<b>Invalid events are popped and discarded.</b> <b>This happens "
    "constantly — it is not an exceptional case</b>, and an "
    "implementation that logs a warning or asserts on it will drown. This "
    "is the single most common source of confusion when implementing "
    "Fortune's algorithm, because the published descriptions tend to "
    "mention it in passing."]),

  ("break",),
  ("h1", "3 &nbsp; The lifting map"),
  ("eq", "(x, y) &rarr; (x, y, x&#178; + y&#178;)"),
  ("p", "Lift each site from the plane onto the paraboloid z = x&#178; + "
        "y&#178;. <b>The lower convex hull of the lifted points, projected "
        "back down, is exactly the Delaunay triangulation of the original "
        "sites</b> — and the Voronoi diagram is its dual. One "
        "three-dimensional convex hull therefore yields both diagrams. "
        "<b>This is Module 03's parabola reduction, one dimension up</b>, "
        "and it is the most satisfying result in the course."),
  ("callout", "Why the lifting map matters practically, not just aesthetically",
   ["<b>Delaunay and Voronoi require no new algorithm.</b> A working 3D "
    "convex hull implementation (Module 03 &sect;3) computes both, which is "
    "a substantial saving in code and in the number of things that can be "
    "wrong.",
    "<b>It explains where the incircle predicate comes from.</b> 'Is "
    "<i>d</i> inside the circle through <i>a</i>, <i>b</i>, <i>c</i>?' "
    "becomes 'is lifted <i>d</i> below the plane through lifted <i>a</i>, "
    "<i>b</i>, <i>c</i>?' — which is <code>orient3d</code> on the "
    "lifted points. <b>The 4&times;4 incircle determinant of Module 02 "
    "<i>is</i> the 3&times;3 orientation determinant after lifting</b>, "
    "which is why its rows contained x&#178; + y&#178;.",
    "<b>And it generalises to every dimension.</b> A Voronoi diagram in d "
    "dimensions is a convex hull in d + 1, so one piece of code handles all "
    "of them — subject to the output-size blowup of Module 03's last "
    "table.",
    "<b>It is also the reason <code>qhull</code> computes Delaunay "
    "triangulations</b> despite being a convex hull program: it is simply "
    "applying this map. Knowing that explains the otherwise-puzzling shape "
    "of its interface."]),

  ("h1", "4 &nbsp; Variants"),
  ("table", ["Variant", "What changes", "What it is used for"],
   [["<b>Power (Laguerre) diagram</b>",
     "<b>Sites carry weights</b>; distance becomes the power distance, so "
     "bisectors are still straight but shift toward the lighter site.",
     "<b>Spheres of differing radii</b> — molecular surfaces, packed "
     "particle systems, and weighted fracture."],
    ["<b>Centroidal Voronoi tessellation (CVT)</b>",
     "<b>Each site is required to be the centroid of its own cell.</b> "
     "Reached by Lloyd's algorithm: compute the diagram, move each site to "
     "its centroid, repeat.",
     "<b>Remeshing, stippling, and blue-noise sampling.</b> The cells "
     "become near-hexagonal and highly uniform. <b>The variant that "
     "appears most often in graphics</b>, and the link to CSCE 647's "
     "sampling material."],
    ["<b>Generalised Voronoi</b>",
     "Sites are line segments or polygons rather than points, so bisectors "
     "become parabolic arcs.",
     "<b>The medial axis</b> — skeletons, toolpath generation, and "
     "navmesh spine extraction (Module 11)."],
    ["<b>Order-k Voronoi</b>",
     "Cells defined by the <i>k</i> nearest sites rather than the single "
     "nearest.",
     "k-nearest-neighbour queries answered by point location (Module 10)."],
    ["<b>Farthest-point Voronoi</b>",
     "<b>Cells defined by the <i>farthest</i> site.</b> Only hull vertices "
     "get nonempty cells.",
     "<b>The smallest enclosing circle</b>, and other farthest-point "
     "problems."],
    ["<b>Manhattan or L<super>&infin;</super> metrics</b>",
     "A different distance function; bisectors become polylines.",
     "Grid-based worlds and VLSI routing, where the metric genuinely is "
     "not Euclidean."]],
   [0.19, 0.38, 0.43]),
  ("callout", "Where this shows up in an engine",
   ["<b>Fracture and destruction.</b> A Voronoi partition of a solid "
    "produces convincing shards, and because every cell is convex "
    "(&sect;1) the pieces are immediately usable as collision proxies with "
    "no decomposition step (Module 03 &sect;3, Module 12).",
    "<b>Procedural texture and terrain.</b> Worley noise is a Voronoi "
    "distance field evaluated per pixel, and it is the standard source of "
    "cells, cracks, scales, stones, and crystalline structure.",
    "<b>Blue-noise sampling and stippling</b> via Lloyd relaxation. The "
    "resulting point sets have far better spectral properties than uniform "
    "random ones, which matters for every sampling job in CSCE 647 "
    "Module 06 — from anti-aliasing to importance sampling to "
    "dithering.",
    "<b>Territory and influence maps, NPC spacing, and the medial axis</b> "
    "for skeleton extraction and navigation-mesh spine generation "
    "(Module 11). <b>Voronoi is one of the few structures in this course "
    "that is as useful for gameplay logic as for geometry.</b>"]),
 ],
 "resources": [
   ("de Berg et al. &mdash; Computational Geometry, chapter 7 (Voronoi "
    "diagrams)",
    "https://www.springer.com/gp/book/9783642096815",
    "Fortune's algorithm with the beach line and the circle-event handling "
    "of &sect;2, done in full."),
   ("Mount &mdash; CMSC 754, Voronoi and lifting lectures (free PDF)",
    "https://www.cs.umd.edu/class/spring2020/cmsc754/Lects/cmsc754-spring2020-lects.pdf",
    "<b>The lifting map of &sect;3</b>, derived rather than asserted."),
   ("Aurenhammer &mdash; Voronoi Diagrams: A Survey of a Fundamental "
    "Geometric Data Structure",
    "https://dl.acm.org/doi/10.1145/116873.116880",
    "The variants of &sect;4, comprehensively. Still the best single "
    "survey."),
   ("Du, Faber & Gunzburger &mdash; Centroidal Voronoi Tessellations "
    "(free)",
    "https://epubs.siam.org/doi/10.1137/S0036144599352836",
    "Lloyd's algorithm and CVT, with the convergence theory."),
 ],
 "exercises": [
   "Compute a Voronoi diagram by brute-force half-plane intersection, one "
   "cell at a time, and verify the linear total size.",
   "<b>Verify the Euler bound empirically</b> for many random site sets.",
   "Confirm that the unbounded cells are exactly the convex hull vertices.",
   "Implement Fortune's algorithm. <b>Count how many circle events turn "
   "out to be false</b> and report the fraction.",
   "Run Fortune's on cocircular sites and on collinear sites. Report what "
   "happens.",
   "<b>Implement the lifting map</b> and compute Delaunay via your 3D "
   "convex hull from Module 03. Compare against Fortune's output.",
   "Verify that incircle equals <code>orient3d</code> on lifted points.",
   "<b>Implement Lloyd's algorithm</b> and watch a random point set become "
   "blue noise. Plot the power spectrum before and after.",
   "Use a Voronoi partition to fracture a convex polygon and render the "
   "shards.",
   "Implement Worley noise from your diagram and texture a surface with "
   "it.",
 ],
 "selfcheck": [
   "Define the Voronoi diagram and give three structural consequences.",
   "Why is the diagram linear in size despite quadratically many "
   "half-planes?",
   "What is a Voronoi vertex geometrically, and which predicate decides "
   "it?",
   "Why does a straight sweep line fail, and what does the beach line fix?",
   "What is a false circle event and how is it handled?",
   "State the lifting map and give three practical consequences.",
   "Name six Voronoi variants and one use of each.",
   "Give four engine uses of Voronoi diagrams.",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Delaunay Triangulation and Meshing",
 "subtitle": "The triangulation you want, and how to force it to behave.",
 "question": "Of all triangulations of these points, which is best?",
 "outcomes": [
     "State the empty-circumcircle property and the max-min angle "
     "property.",
     "Implement incremental Delaunay with edge flipping.",
     "Explain constrained Delaunay and when it is needed.",
     "Apply Ruppert refinement for quality meshing.",
     "State what fails in three dimensions.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What makes it the right one",
   "blurb": "Several equivalent definitions, one good property."},

  {"t": "callout", "title": "Equivalent characterisations of Delaunay",
   "kind": "Four definitions of the same thing",
   "body": ["<b>Empty circumcircle:</b> no triangle's circumcircle "
            "contains any other site.",
            "<b>Max-min angle:</b> among all triangulations of the point "
            "set, Delaunay maximises the smallest angle. <b>This is why "
            "you want it.</b>",
            "<b>Dual of Voronoi:</b> connect sites whose cells share an "
            "edge (Module 08).",
            "<b>Lifted lower hull:</b> project the lower convex hull of "
            "the lifted points (Module 08 §3).",
            "<b>All four give the same triangulation</b> when the points "
            "are in general position."]},

  {"t": "callout", "title": "Max-min angle is the property that matters",
   "kind": "Why anyone cares",
   "body": ["<b>Thin slivers are bad for everything.</b> Interpolation "
            "across them is ill-conditioned, finite-element matrices "
            "become badly conditioned, and normals computed on them are "
            "numerically garbage.",
            "<b>Delaunay maximises the minimum angle over all possible "
            "triangulations</b> of the same points — it is optimal in "
            "that specific sense.",
            "<b>But it does not guarantee a good minimum angle.</b> If the "
            "points admit only bad triangles, Delaunay gives you the least "
            "bad ones.",
            "<b>Getting an actual quality guarantee requires adding "
            "points</b>, which is refinement — Part 3."]},

  {"t": "section", "label": "Part 2", "title": "Construction",
   "blurb": "Incremental, with flips."},

  {"t": "code", "kicker": "Incremental", "title": "Insert and flip",
   "lang": "text", "code": """
  Start with a large bounding triangle containing all sites.

  for each site p:
      t = triangle containing p          # point location
      split t into 3 triangles at p      # or 4 if p is on an edge
      LEGALISE each of the new edges

  LEGALISE(edge e, point p):
      let (p, a, b) and (a, b, d) be the two triangles on e
      if incircle(p, a, b, d) > 0:       # d is inside -> ILLEGAL
          flip e: replace a-b with p-d
          LEGALISE(p-a-d) and LEGALISE(p-d-b)   # recurse outward

  Each flip strictly increases the sorted angle vector, so the
  recursion TERMINATES.  Expected O(n log n) under random insertion
  order; O(n^2) worst case if you insert in sorted order.

  SO: shuffle the input. This is not optional.
""",
   "caption": "<b>Shuffling the insertion order is the difference between "
              "n log n and n&#178;</b>, and sorted input is extremely "
              "common.",
   "note": "The shuffle point is practical and frequently missed."},

  {"t": "callout", "title": "Why flipping terminates",
   "kind": "The correctness argument",
   "body": ["<b>Consider the vector of all angles in the triangulation, "
            "sorted ascending.</b>",
            "<b>Every legalising flip increases this vector "
            "lexicographically</b> — the flip replaces the worse diagonal "
            "with the better one.",
            "<b>There are finitely many triangulations</b>, so the process "
            "cannot cycle and must stop.",
            "<b>And it stops exactly at the Delaunay triangulation</b>, "
            "since a triangulation with no illegal edge satisfies the "
            "empty-circumcircle property everywhere. <b>Local optimality "
            "implies global optimality here</b>, which is unusual and is "
            "what makes flipping work."]},

  {"t": "section", "label": "Part 3", "title": "Constraints and quality",
   "blurb": "Forcing edges, and adding points."},

  {"t": "callout", "title": "Constrained Delaunay: when an edge must be present",
   "kind": "The practical necessity",
   "body": ["<b>A polygon boundary, a road, a crease, a hole edge — "
            "these must appear in the triangulation</b>, and plain "
            "Delaunay may not include them.",
            "<b>Constrained Delaunay forces them in</b>, then makes "
            "everything else as Delaunay as possible: a triangle's "
            "circumcircle may contain a site, but only if the constraint "
            "blocks visibility.",
            "<b>This is how you triangulate a polygon with holes</b> "
            "(Module 05 §4) without any bridging.",
            "<b>Conforming Delaunay is the alternative:</b> split the "
            "constraint edges by inserting points until they appear "
            "naturally. <b>More points, but genuinely Delaunay.</b>"]},

  {"t": "bullets", "kicker": "Ruppert", "title": "Refinement for guaranteed quality",
   "items": [
     "<b>Repeat: find a triangle with a bad angle, insert its "
     "circumcentre, re-triangulate.</b>",
     "",
     "<b>If the new point would land too close to a constraint "
     "segment, split the segment instead.</b> This is the whole "
     "subtlety.",
     "",
     "<b>Terminates with all angles above ~20.7°</b>, and with "
     "O(optimal) triangles.",
     "",
     "<b>Fails on input angles below ~60°</b> — two constraints meeting "
     "sharply cannot be fixed by adding points.",
     "",
     "<b>Chew's and Shewchuk's variants</b> improve the bound and handle "
     "small input angles better.",
   ],
   "footnote": "<b>Guaranteed-quality meshing is a solved problem in 2D "
               "and an open one in 3D.</b>",
   "note": "The small-input-angle limitation is fundamental, not a gap in "
           "the algorithm."},

  {"t": "section", "label": "Part 4", "title": "Three dimensions",
   "blurb": "Where the theory stops being kind."},

  {"t": "table", "kicker": "3D", "title": "What breaks in three dimensions",
   "header": ["Property", "2D", "3D"],
   "widths": [3.1, 3.7, 5.3],
   "rows": [
     ["Size", "O(n)", "<b>O(n&#178;) worst case — points on a moment curve</b>"],
     ["<b>Max-min angle</b>", "<b>Delaunay is optimal</b>", "<b>FALSE. No such guarantee</b>"],
     ["<b>Slivers</b>", "Excluded by the property", "<b>Allowed: 4 near-cocircular points, near-zero volume</b>"],
     ["Flipping", "Always converges", "<b>Can get stuck; flips are not always possible</b>"],
     ["<b>Polyhedra</b>", "Always triangulable", "<b>Schönhardt: some are NOT tetrahedralisable</b>"],
     ["Quality meshing", "Solved (Ruppert)", "<b>Open problem; heuristics in practice</b>"],
   ],
   "footnote": "<b>The Schönhardt polyhedron is the key fact:</b> a "
               "twisted triangular prism that cannot be split into "
               "tetrahedra without adding points.",
   "note": "This table is the module's sting — 2D intuition does not "
           "transfer."},

  {"t": "callout", "title": "Slivers: the 3D failure that has no 2D analogue",
   "kind": "Why 3D meshing is hard",
   "body": ["<b>A sliver is a tetrahedron whose four vertices lie almost "
            "on a circle</b> — nearly flat, near-zero volume, and yet it "
            "can satisfy the empty-circumsphere property perfectly.",
            "<b>So Delaunay does not exclude them.</b> The property that "
            "guarantees quality in 2D guarantees nothing in 3D.",
            "<b>And slivers destroy finite-element conditioning</b> and "
            "make gradient and normal computation meaningless.",
            "<b>Sliver removal is a separate post-process</b> — "
            "perturbation, exudation, or optimisation. <b>There is no "
            "clean guaranteed algorithm, which is why 3D meshing is a "
            "research area and 2D is not.</b>"]},
 ],
 "takeaways": [
   "Delaunay has four equivalent characterisations — empty "
   "circumcircle, max-min angle, Voronoi dual, and lifted lower hull.",
   "Max-min angle is why anyone wants it, but it only gives the least bad "
   "triangulation of those points; a quality guarantee requires adding "
   "points.",
   "Incremental insertion with edge flipping terminates because each flip "
   "lexicographically increases the sorted angle vector.",
   "Insertion order matters: shuffle, or sorted input gives O(n²).",
   "Constrained Delaunay forces required edges and is the clean way to "
   "triangulate polygons with holes.",
   "In 3D the max-min property is false, slivers satisfy the "
   "empty-circumsphere property, and some polyhedra cannot be "
   "tetrahedralised at all.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What makes it the right triangulation"),
  ("callout", "Four equivalent characterisations",
   ["<b>Empty circumcircle:</b> a triangulation is Delaunay when no "
    "triangle's circumcircle contains any other site in its interior. This "
    "is the definition that becomes the incircle predicate.",
    "<b>Max-min angle:</b> among all possible triangulations of the same "
    "point set, the Delaunay triangulation maximises the minimum angle "
    "— and in fact lexicographically maximises the whole sorted angle "
    "vector. <b>This is the reason anyone wants it.</b>",
    "<b>Dual of the Voronoi diagram:</b> connect two sites exactly when "
    "their Voronoi cells share an edge (Module 08 &sect;1).",
    "<b>Lifted lower hull:</b> project the lower convex hull of the points "
    "lifted onto the paraboloid (Module 08 &sect;3). <b>All four coincide "
    "when the points are in general position</b>, and all four fail to "
    "determine a unique answer when four points are cocircular — which "
    "is the one degeneracy this module must handle."]),
  ("callout", "Max-min angle is the property that matters, and what it does not promise",
   ["<b>Thin slivers are bad for everything downstream.</b> Barycentric "
    "interpolation across them is ill-conditioned; finite-element stiffness "
    "matrices built on them have terrible condition numbers; normals and "
    "gradients computed from them are numerically meaningless; and texture "
    "mapping across them stretches visibly.",
    "<b>Delaunay maximises the minimum angle over all triangulations of "
    "the same point set.</b> It is provably optimal in that specific and "
    "useful sense, which is a strong statement and is why it is the "
    "default choice everywhere.",
    "<b>But it does not guarantee that the minimum angle is good.</b> If "
    "the input points admit only bad triangles — four points in a very "
    "flat configuration, say — then Delaunay hands you the least bad "
    "of a set of bad options. <b>Optimal among the available is not the "
    "same as adequate.</b>",
    "<b>Obtaining an actual quality guarantee requires adding points</b>, "
    "which changes the problem from 'triangulate these points' to 'mesh "
    "this domain'. That is refinement, and it is &sect;3."]),

  ("h1", "2 &nbsp; Construction"),
  ("code", """Start with a bounding triangle containing all sites.

for each site p:                       # SHUFFLE the order first
    t = triangle containing p          # point location
    split t at p into 3 triangles
    LEGALISE each new edge

LEGALISE(edge ab, point p):
    let (p,a,b) and (a,b,d) share ab
    if incircle(p, a, b, d) > 0:       # d inside -> edge is ILLEGAL
        flip ab to pd
        LEGALISE(ad, p);  LEGALISE(db, p)      # recurse outward

Expected O(n log n) under RANDOM insertion order.
O(n^2) if you insert in sorted order -- so shuffle."""),
  ("p", "<b>Shuffling the insertion order is the difference between "
        "O(n log n) and O(n&#178;)</b>, and it is routinely omitted. The "
        "bad case is not adversarial or rare: <b>sorted input is extremely "
        "common</b>, because points frequently arrive from a scan, a grid "
        "traversal, or a previous sorted pass. Randomised incremental "
        "construction only has its expected bound if the randomisation "
        "actually happens."),
  ("callout", "Why flipping terminates",
   ["<b>Consider the vector of all angles in the current triangulation, "
    "sorted in ascending order.</b> This is a finite vector of real "
    "numbers, and triangulations of a fixed point set can be compared by it "
    "lexicographically.",
    "<b>Every legalising flip increases that vector lexicographically.</b> "
    "The flip replaces the worse of the two possible diagonals of a convex "
    "quadrilateral with the better one, and the six angles involved "
    "strictly improve in the lexicographic sense.",
    "<b>There are finitely many triangulations of a finite point set</b>, "
    "so a strictly increasing process over them cannot cycle and must "
    "terminate.",
    "<b>And it terminates exactly at the Delaunay triangulation</b>, "
    "because a triangulation in which no edge is illegal satisfies the "
    "empty-circumcircle property globally. <b>Local optimality implies "
    "global optimality here</b> — which is unusual, is not true of "
    "most optimisation problems, and is precisely what makes a purely local "
    "flipping procedure correct."]),

  ("break",),
  ("h1", "3 &nbsp; Constraints and quality"),
  ("callout", "Constrained Delaunay: when an edge must be present",
   ["<b>A polygon boundary, a road, a crease, a river, the edge of a hole "
    "— these must appear in the triangulation</b>, and the plain "
    "Delaunay triangulation of the vertices may simply not contain them.",
    "<b>The constrained Delaunay triangulation forces them in</b> and then "
    "makes everything else as Delaunay as possible: a triangle's "
    "circumcircle is permitted to contain a site, but only when a "
    "constraint edge blocks visibility between them. It is the Delaunay "
    "triangulation of the visibility-restricted problem.",
    "<b>This is the clean way to triangulate a polygon with holes</b> "
    "(Module 05 &sect;4) — insert the boundary and hole edges as "
    "constraints, triangulate, and discard the triangles outside. <b>No "
    "bridging, and none of the bridging degeneracies.</b>",
    "<b>Conforming Delaunay is the alternative:</b> rather than relaxing "
    "the property, split the constraint edges by inserting points until the "
    "pieces appear in the ordinary Delaunay triangulation. <b>The result is "
    "genuinely Delaunay and has more vertices</b>, which matters when the "
    "mesh is an input to simulation rather than a rendering artifact."]),
  ("ol", ["<b>Find a triangle whose smallest angle is below the target, or "
          "which is too large, and insert its circumcentre.</b> The "
          "circumcentre is, by the empty-circumcircle property, far from "
          "every existing vertex — which is why this does not produce "
          "new bad triangles near it.",
          "<b>If the proposed circumcentre would land inside the "
          "diametral circle of a constraint segment, split that segment at "
          "its midpoint instead</b>, and do not insert the circumcentre. "
          "<b>This single rule is the whole subtlety of Ruppert's "
          "algorithm</b> and the reason it terminates.",
          "<b>Repeat until no triangle is bad.</b> The algorithm "
          "terminates with every angle above roughly 20.7&deg;, and with a "
          "triangle count within a constant factor of the optimal mesh for "
          "that quality bound.",
          "<b>It fails when the input itself contains angles below about "
          "60&deg;</b> between two constraint segments. <b>This is "
          "fundamental, not a gap in the algorithm</b> — no amount of "
          "point insertion can improve the angle in the corner where two "
          "constraints meet sharply, because that angle is part of the "
          "specified domain.",
          "<b>Chew's variants and Shewchuk's terminator algorithm</b> "
          "improve the achievable angle bound and handle small input angles "
          "by grading the mesh into them rather than attempting to fix "
          "them."]),
  ("p", "<b>Guaranteed-quality meshing is a solved problem in two "
        "dimensions and an open one in three</b>, which is the single most "
        "useful thing to know about this area."),

  ("h1", "4 &nbsp; Three dimensions"),
  ("table", ["Property", "Two dimensions", "Three dimensions"],
   [["<b>Size of the triangulation</b>", "O(n), always.",
     "<b>O(n&#178;) in the worst case</b> — points on the moment curve "
     "achieve it. A tetrahedralisation can be quadratically larger than its "
     "input."],
    ["<b>Max-min angle optimality</b>",
     "<b>Delaunay is optimal</b> among all triangulations.",
     "<b>False.</b> There is no such guarantee in 3D, and this is the most "
     "important single fact in the table — the property that justifies "
     "using Delaunay at all simply does not transfer."],
    ["<b>Slivers</b>", "Excluded by the empty-circumcircle property.",
     "<b>Permitted.</b> Four nearly-cocircular points form a near-zero-"
     "volume tetrahedron that satisfies the empty-circumsphere property "
     "perfectly. See below."],
    ["<b>Flipping</b>", "Always converges to Delaunay.",
     "<b>Can get stuck.</b> The 2-to-3 and 3-to-2 flips are not always "
     "applicable, so a purely local flipping procedure may reach a "
     "non-Delaunay configuration with no legal move."],
    ["<b>Polyhedra</b>",
     "Every simple polygon can be triangulated (Module 05 &sect;1).",
     "<b>False in 3D.</b> <b>The Sch&ouml;nhardt polyhedron</b> — a "
     "triangular prism with its top face twisted — <b>cannot be "
     "decomposed into tetrahedra without adding interior points</b>, which "
     "destroys the entire induction of Module 05."],
    ["<b>Quality meshing</b>",
     "Solved: Ruppert refinement with proven bounds.",
     "<b>Open.</b> Heuristics, optimisation, and sliver exudation are used "
     "in practice, with no guarantee."]],
   [0.20, 0.29, 0.51]),
  ("callout", "Slivers: the 3D failure with no 2D analogue",
   ["<b>A sliver is a tetrahedron whose four vertices lie almost exactly "
    "on a common circle</b> — so it is nearly flat, has near-zero "
    "volume, and yet <b>its circumsphere can be perfectly empty</b>.",
    "<b>So the Delaunay property does not exclude slivers.</b> The "
    "criterion that guarantees good triangles in two dimensions guarantees "
    "nothing whatsoever in three, and a correctly computed 3D Delaunay "
    "tetrahedralisation of perfectly reasonable points can be full of them.",
    "<b>And slivers are destructive.</b> They ruin finite-element "
    "conditioning, make interpolated gradients and normals meaningless, and "
    "cause time-step restrictions in explicit simulation (CSCE 649) that "
    "can be orders of magnitude worse than the rest of the mesh requires.",
    "<b>Sliver removal is a separate post-process</b> — vertex "
    "perturbation, weight assignment (sliver exudation via a power diagram, "
    "Module 08 &sect;4), or direct optimisation. <b>None of these comes "
    "with a clean guarantee, which is precisely why three-dimensional "
    "meshing remains an active research area while the two-dimensional "
    "problem has been settled for thirty years.</b>"]),
 ],
 "resources": [
   ("Shewchuk &mdash; Triangle, and Delaunay Refinement Algorithms for "
    "Triangular Mesh Generation (free)",
    "https://www.cs.cmu.edu/~quake/triangle.html",
    "<b>The reference for &sect;3</b>, with working code. Shewchuk's "
    "writing on meshing is unusually clear."),
   ("de Berg et al. &mdash; Computational Geometry, chapter 9 (Delaunay "
    "triangulations)",
    "https://www.springer.com/gp/book/9783642096815",
    "Incremental construction, the flipping termination argument, and the "
    "randomisation analysis of &sect;2."),
   ("Shewchuk &mdash; What Is a Good Linear Finite Element? (free)",
    "https://people.eecs.berkeley.edu/~jrs/papers/elemj.pdf",
    "<b>Why angle quality matters</b>, derived from the interpolation "
    "error rather than asserted. The best answer to 'why not just use any "
    "triangulation'."),
   ("Cheng, Dey & Shewchuk &mdash; Delaunay Mesh Generation",
    "https://people.eecs.berkeley.edu/~jrs/meshbook.html",
    "The three-dimensional material of &sect;4, including slivers and the "
    "Sch&ouml;nhardt obstruction. Library copy."),
 ],
 "exercises": [
   "Implement incremental Delaunay with flipping and exact incircle.",
   "<b>Verify the four characterisations agree</b> on the same point set "
   "— compare against your Voronoi dual and your lifted hull.",
   "Insert in sorted order and in shuffled order. <b>Measure the "
   "difference and plot it against n.</b>",
   "Instrument the flip count per insertion and plot the distribution.",
   "Compare the minimum angle of Delaunay against several random "
   "triangulations of the same points.",
   "<b>Run on cocircular points</b> and report which triangulation you "
   "get and whether it is stable under reordering.",
   "Implement constrained Delaunay and use it to triangulate a polygon "
   "with three holes.",
   "<b>Implement Ruppert refinement</b> and plot the minimum angle "
   "against the number of inserted points.",
   "Construct an input with a 20° corner and show that refinement "
   "does not terminate at a high angle bound.",
   "Build a 3D Delaunay tetrahedralisation and <b>count the slivers</b>. "
   "Report the worst dihedral angle.",
 ],
 "selfcheck": [
   "Give four equivalent definitions of the Delaunay triangulation.",
   "What does max-min angle guarantee, and what does it not?",
   "Describe incremental insertion with legalisation.",
   "Prove that flipping terminates.",
   "Why does insertion order matter, and what should you do?",
   "What is constrained Delaunay, and how does it differ from conforming?",
   "Describe Ruppert refinement and its one subtle rule.",
   "Why does refinement fail on small input angles?",
   "Name six things that break in three dimensions.",
   "What is a sliver and why does Delaunay not exclude it?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Range Searching and Proximity",
 "subtitle": "Preprocessing, so the query is cheap.",
 "question": "What is near this point, and what is in this box?",
 "outcomes": [
     "Analyse the space–time trade-off in range searching.",
     "Build range trees and explain fractional cascading.",
     "Implement nearest-neighbour search with pruning.",
     "Explain approximate nearest neighbour and when to use it.",
     "Explain the curse of dimensionality concretely.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The trade",
   "blurb": "You can buy query time with space."},

  {"t": "table", "kicker": "2D orthogonal", "title": "The space–time trade-off, concretely",
   "header": ["Structure", "Space", "Query", "Build"],
   "widths": [3.0, 2.6, 3.3, 3.2],
   "rows": [
     ["<b>Linear scan</b>", "<b>O(n)</b>", "<b>O(n)</b>", "<b>O(1)</b>"],
     ["<b>k-d tree</b>", "<b>O(n)</b>", "<b>O(√n + m)</b>", "O(n log n)"],
     ["<b>Range tree</b>", "<b>O(n log n)</b>", "<b>O(log&#178;n + m)</b>", "O(n log n)"],
     ["<b>+ fractional cascading</b>", "O(n log n)", "<b>O(log n + m)</b>", "O(n log n)"],
     ["Full precomputation", "<b>O(n&#178;) or worse</b>", "O(1 + m)", "Expensive"],
   ],
   "footnote": "<b>m is the number of points reported</b>, and no structure "
               "can beat O(m) — you have to list them.",
   "note": "The k-d tree row is the practical default despite the worse "
           "bound; the constants and memory layout win."},

  {"t": "callout", "title": "A range tree is a tree of trees",
   "kind": "The construction",
   "body": ["<b>Build a balanced BST on x.</b> Each node covers a "
            "contiguous range of x values.",
            "<b>At every node, store a second BST on y</b> holding all "
            "points in that node's subtree.",
            "<b>A query splits into O(log n) canonical nodes</b> whose "
            "x-ranges exactly tile the query's x-interval — then search "
            "each one's y-tree.",
            "<b>O(log&#178;n + m).</b> The space is O(n log n) because each "
            "point appears in O(log n) secondary trees — which is the "
            "price of the better query."]},

  {"t": "callout", "title": "Fractional cascading removes one log factor",
   "kind": "A technique worth knowing generally",
   "body": ["<b>The O(log&#178;n) comes from doing a fresh binary search in "
            "each of O(log n) secondary trees</b> — searching for the "
            "same y value, repeatedly.",
            "<b>So link them.</b> Store with each element of a parent's "
            "list a pointer to the corresponding position in each child's "
            "list.",
            "<b>Then the first search costs log n and every subsequent one "
            "costs O(1)</b>, by following the pointer.",
            "<b>O(log n + m).</b> <b>The technique generalises far beyond "
            "range trees</b> — any time you repeat a search for the same "
            "key in related sorted lists, it applies."]},

  {"t": "section", "label": "Part 2", "title": "Nearest neighbour",
   "blurb": "Branch and bound on a spatial tree."},

  {"t": "code", "kicker": "k-NN", "title": "Nearest neighbour with pruning",
   "lang": "text", "code": """
  NEAREST(node, q, best):
      if node is a leaf:
          for each p in node: best = min(best, dist(q, p))
          return best

      # Descend the NEARER child first -- this is the whole trick.
      near, far = children ordered by which side q falls on
      best = NEAREST(near, q, best)

      # Only visit the far side if it could possibly contain
      # something closer than what we already have.
      if dist_to_plane(q, node.split) < best:
          best = NEAREST(far, q, best)
      return best

  Descending the near side first makes `best` small EARLY,
  which makes the far-side pruning test succeed more often.
  Reversing the order is correct and dramatically slower.

  For k nearest: keep a bounded max-heap of size k; prune
  against its largest element instead.
""",
   "caption": "<b>Near-side-first is not an optimisation detail</b> — it "
              "is what makes the pruning effective at all.",
   "note": "Students write this with arbitrary child order and then "
           "wonder why it's slow."},

  {"t": "section", "label": "Part 3", "title": "High dimensions",
   "blurb": "Where all of this stops working."},

  {"t": "callout", "title": "The curse of dimensionality, concretely",
   "kind": "Three facts that each break something",
   "body": ["<b>Distances concentrate.</b> In high dimensions the ratio of "
            "the farthest to the nearest point approaches 1, so 'nearest' "
            "stops being meaningful.",
            "<b>Volume moves to the corners.</b> The inscribed sphere of a "
            "unit cube has vanishing relative volume as d grows — so a "
            "ball-versus-box pruning test almost never prunes.",
            "<b>Everything is on the boundary.</b> Almost all the volume "
            "of a high-dimensional ball lies in a thin shell near its "
            "surface.",
            "<b>Together these mean exact nearest neighbour above ~20 "
            "dimensions costs more than a linear scan</b>, which has "
            "perfect locality and no branches."]},

  {"t": "table", "kicker": "Approximate", "title": "What replaces exact search",
   "header": ["Method", "Idea", "Character"],
   "widths": [2.9, 4.4, 4.8],
   "rows": [
     ["<b>LSH</b>", "<b>Hash so near points collide</b>", "<b>Provable guarantees; tunable</b>"],
     ["<b>HNSW</b>", "<b>Navigable small-world graph</b>", "<b>The practical default now</b>"],
     ["Product quantisation", "Compress vectors; search compressed", "<b>Huge memory savings</b>"],
     ["Random projection trees", "Split on random directions", "Simple; good baseline"],
     ["<b>IVF</b>", "Cluster, search nearest clusters", "<b>Scales; used with PQ</b>"],
   ],
   "footnote": "<b>Approximate is not a compromise here</b> — when "
               "distances concentrate, the exact answer is barely more "
               "meaningful than a good approximate one.",
   "note": "That reframing matters: approximation isn't settling, it's "
           "appropriate."},

  {"t": "section", "label": "Part 4", "title": "In practice",
   "blurb": "What an engine actually does."},

  {"t": "bullets", "kicker": "Engine", "title": "Proximity queries in a game engine",
   "items": [
     "<b>Broad-phase collision</b> — a uniform grid or sweep-and-prune, "
     "not a tree. O(1) updates matter more than query bounds "
     "(Module 07).",
     "",
     "<b>Audio and AI perception radius</b> — spatial hash, rebuilt or "
     "updated per frame.",
     "",
     "<b>Nearest navmesh polygon</b> — k-d tree or BVH over the navmesh "
     "(Module 11).",
     "",
     "<b>Photon and particle lookup</b> — k-d tree, built once per frame "
     "(CSCE 647).",
     "",
     "<b>Dynamic objects break every static structure</b>, which is why "
     "grids dominate despite worse asymptotics.",
   ],
   "footnote": "<b>The query bound is rarely what decides it.</b> Update "
               "cost, memory layout, and cache behaviour usually do."},
 ],
 "takeaways": [
   "Range searching is a space–time trade: k-d trees are O(n) space "
   "and O(√n + m) query; range trees buy O(log²n) query with "
   "O(n log n) space.",
   "A range tree is a BST on x where each node carries a secondary BST on "
   "y, so each point appears in O(log n) secondary structures.",
   "Fractional cascading links corresponding positions across related "
   "sorted lists, removing a log factor — and generalises well beyond "
   "range trees.",
   "Nearest-neighbour pruning works only if you descend the nearer child "
   "first, which makes the running best small early.",
   "In high dimensions distances concentrate, volume moves to the corners, "
   "and pruning stops pruning — so a linear scan wins above roughly 20 "
   "dimensions.",
   "In engines the query bound rarely decides the structure; update cost "
   "and cache behaviour do, which is why grids dominate.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The space–time trade-off"),
  ("table", ["Structure", "Space", "Query (2D orthogonal)", "Build"],
   [["<b>Linear scan</b>", "O(n)", "O(n)",
     "O(1). <b>Never dismiss it</b> — perfect locality, no branching, "
     "and it wins at small n and in high dimensions (&sect;3)."],
    ["<b>k-d tree</b>", "<b>O(n)</b>", "<b>O(&radic;n + m)</b>",
     "O(n log n). <b>The practical default</b> despite the worse bound, "
     "because the space is linear and the layout is cache-friendly."],
    ["<b>Range tree</b>", "<b>O(n log n)</b>", "<b>O(log&#178;n + m)</b>",
     "O(n log n). Buys query time with space — the clearest example "
     "of the trade in the subject."],
    ["<b>Range tree + fractional cascading</b>", "O(n log n)",
     "<b>O(log n + m)</b>", "O(n log n). One log factor removed, free."],
    ["<b>Full precomputation</b>", "<b>O(n&#178;) or worse</b>", "O(1 + m)",
     "Expensive. Included to mark the end of the spectrum."]],
   [0.25, 0.14, 0.21, 0.40]),
  ("p", "<b>m is the number of points reported</b>, and no structure can "
        "improve on the O(m) term — the answer has to be listed. "
        "Bounds of this shape are called <i>output-sensitive</i> "
        "(Module 03 &sect;2), and the right way to read the table is that "
        "the structures differ only in the additive search term."),
  ("callout", "A range tree is a tree of trees",
   ["<b>Build a balanced binary search tree on the x-coordinate.</b> Each "
    "node of this primary tree corresponds to a contiguous range of x "
    "values — the points in its subtree.",
    "<b>At every node of the primary tree, store a secondary balanced tree "
    "on the y-coordinate</b>, containing exactly the points in that node's "
    "subtree.",
    "<b>A query x-interval decomposes into O(log n) canonical nodes</b> "
    "whose x-ranges exactly tile the interval and are pairwise disjoint. "
    "Search each of their secondary y-trees for the query's y-interval and "
    "report what is found.",
    "<b>Total O(log&#178;n + m).</b> The space is O(n log n) rather than "
    "O(n) <b>because each point appears in the secondary tree of every "
    "ancestor</b> — O(log n) of them. That extra space is exactly what "
    "was bought, and it generalises: a d-dimensional range tree costs "
    "O(n log<super>d&minus;1</super>n) space for "
    "O(log<super>d</super>n + m) query."]),
  ("callout", "Fractional cascading removes one logarithm",
   ["<b>The O(log&#178;n) arises from performing a fresh binary search in "
    "each of O(log n) secondary trees</b> — and crucially, every one "
    "of those searches is for the <i>same</i> y value, in lists that are "
    "closely related (a parent's list is the merge of its children's).",
    "<b>So link them.</b> Store with each element of a node's sorted list a "
    "pointer to the position of the corresponding value in each child's "
    "list — that is, where that value would fall.",
    "<b>Then only the first search costs O(log n); every subsequent one is "
    "O(1)</b>, obtained by following the stored pointer and adjusting by at "
    "most one position.",
    "<b>The result is O(log n + m).</b> <b>The technique generalises far "
    "beyond range trees</b>: whenever an algorithm repeats a search for the "
    "same key across a family of related sorted lists, fractional cascading "
    "applies. It is one of the genuinely reusable ideas in this course, and "
    "it is worth recognising the pattern rather than only the "
    "application."]),

  ("h1", "2 &nbsp; Nearest neighbour"),
  ("code", """NEAREST(node, q, best):
    if leaf: return min over points in node

    # Descend the NEARER child first. This is the whole trick.
    near, far = children ordered by which side q lies on
    best = NEAREST(near, q, best)

    # Visit the far side only if it could hold something closer.
    if dist_to_split_plane(q, node) < best:
        best = NEAREST(far, q, best)
    return best

For k nearest: keep a bounded max-heap of size k and prune
against its largest element."""),
  ("p", "<b>Descending the nearer child first is not an optimisation "
        "detail — it is what makes the pruning work at all.</b> "
        "Visiting the near side first makes <code>best</code> small early, "
        "which makes the far-side test succeed far more often. Reversing "
        "the order yields a correct implementation that is dramatically "
        "slower, and this is the single most common performance bug in "
        "hand-written nearest-neighbour code."),

  ("break",),
  ("h1", "3 &nbsp; High dimensions"),
  ("callout", "The curse of dimensionality, concretely",
   ["<b>Distances concentrate.</b> As the dimension grows, the ratio "
    "between the distance to the farthest point and the distance to the "
    "nearest point approaches 1 for most natural distributions. <b>So "
    "'nearest neighbour' gradually stops being a meaningful notion</b> "
    "— everything is roughly equidistant, and which point is nearest "
    "is determined by noise.",
    "<b>Volume moves to the corners.</b> The ratio of the volume of the "
    "inscribed sphere to that of the unit cube goes to zero rapidly with "
    "dimension. <b>So a ball-versus-box pruning test — which is "
    "exactly the test in the code above — almost never prunes</b>, "
    "because the query ball overlaps essentially every box.",
    "<b>Almost everything is on the boundary.</b> Nearly all the volume of "
    "a high-dimensional ball lies in a thin shell just inside its surface, "
    "so there is no meaningful 'interior' to recurse away from.",
    "<b>Together these mean exact nearest-neighbour search above roughly "
    "twenty dimensions costs more than a linear scan</b>, which has perfect "
    "memory locality, no branch misprediction, and vectorises cleanly "
    "(CSCE 735 Module 02). <b>The tree is not merely no better; it is "
    "actively worse</b>, which is a result worth internalising before "
    "reaching for a spatial structure on embeddings."]),
  ("table", ["Method", "Idea", "Character"],
   [["<b>Locality-sensitive hashing (LSH)</b>",
     "<b>Hash with a family designed so that near points collide with high "
     "probability</b> and distant ones rarely do.",
     "<b>Provable approximation guarantees</b>, and the trade between "
     "recall and cost is explicitly tunable. The theoretically cleanest "
     "option."],
    ["<b>HNSW</b>",
     "<b>A navigable small-world graph</b> with long-range links in upper "
     "layers; greedy descent from a coarse layer to a fine one.",
     "<b>The practical default now</b> — excellent recall-versus-speed "
     "curves and the basis of most vector databases."],
    ["<b>Product quantisation</b>",
     "Split the vector into subvectors, quantise each against a small "
     "codebook, and compute distances on the codes.",
     "<b>Very large memory savings</b> — often 10 to 50&times; — "
     "which is what makes billion-scale search feasible at all."],
    ["<b>Random projection trees</b>",
     "Split on random directions rather than on axes.",
     "Simple, and a good baseline. Avoids the axis-alignment weakness of "
     "k-d trees."],
    ["<b>Inverted file (IVF)</b>",
     "Cluster the dataset, then search only the nearest few clusters.",
     "<b>Scales well and composes with product quantisation</b>, which is "
     "the standard industrial combination."]],
   [0.21, 0.38, 0.41]),
  ("p", "<b>Approximation is not a compromise in this setting.</b> When "
        "distances concentrate, the exact nearest neighbour is only "
        "marginally more meaningful than a good approximate one — the "
        "difference between them is frequently smaller than the noise in "
        "how the vectors were produced. <b>Insisting on exactness here is "
        "paying a large cost for a distinction the data does not "
        "support</b>, which is a useful reframing."),

  ("h1", "4 &nbsp; In practice"),
  ("ul", ["<b>Broad-phase collision detection:</b> a uniform grid or "
          "sweep-and-prune, not a tree. <b>Every object moves every "
          "frame</b>, so O(1) update cost dominates the query bound "
          "entirely (Module 07 &sect;4).",
          "<b>Audio sources and AI perception radii:</b> a spatial hash, "
          "rebuilt or incrementally updated each frame. The queries are "
          "small-radius and numerous.",
          "<b>Nearest navmesh polygon:</b> a k-d tree or BVH over the "
          "navmesh, which is static and so can afford a good structure "
          "(Module 11).",
          "<b>Photon lookup and particle neighbour finding:</b> a k-d tree "
          "built once per frame, which is the classic photon-mapping "
          "arrangement (CSCE 647) and the SPH neighbour search "
          "(CSCE 649 Module 12).",
          "<b>And dynamic objects break every static structure</b>, which "
          "is why grids and hashes dominate engine code despite having "
          "worse asymptotic bounds than the trees in this module. <b>The "
          "query bound is rarely what decides it</b> — update cost, "
          "memory layout, and cache behaviour usually do, which is "
          "CSCE 735's lesson applied to data structures."]),
 ],
 "resources": [
   ("de Berg et al. &mdash; Computational Geometry, chapters 5 and 10 "
    "(range searching)",
    "https://www.springer.com/gp/book/9783642096815",
    "Range trees and fractional cascading, with the analyses of &sect;1."),
   ("Mount &mdash; CMSC 754, range searching lectures (free PDF)",
    "https://www.cs.umd.edu/class/spring2020/cmsc754/Lects/cmsc754-spring2020-lects.pdf",
    "Clearer on the canonical-node decomposition than most treatments."),
   ("Malkov & Yashunin &mdash; Efficient and robust approximate nearest "
    "neighbor search using HNSW (free)",
    "https://arxiv.org/abs/1603.09320",
    "<b>The &sect;3 default method</b>, from its authors."),
   ("Facebook Research &mdash; FAISS (free)",
    "https://github.com/facebookresearch/faiss",
    "Production implementations of IVF, product quantisation, and HNSW, "
    "with benchmarks. The practical companion to &sect;3."),
 ],
 "exercises": [
   "Implement 2D orthogonal range search by linear scan, k-d tree, and "
   "range tree. Measure all three against n.",
   "<b>Confirm the √n and log²n query behaviours empirically</b> "
   "and compare against the predicted curves.",
   "Measure the actual memory of the range tree and confirm O(n log n).",
   "<b>Implement fractional cascading</b> and measure the improvement.",
   "Implement nearest neighbour with pruning. <b>Then reverse the child "
   "order and measure the slowdown.</b>",
   "Extend to k nearest with a bounded max-heap.",
   "<b>Measure the distance concentration ratio</b> — farthest over "
   "nearest — as dimension goes from 2 to 200. Plot it.",
   "Measure the inscribed-sphere volume ratio against dimension.",
   "Find the crossover dimension where a linear scan beats your k-d tree.",
   "Use FAISS or an HNSW implementation and plot recall against query "
   "time.",
 ],
 "selfcheck": [
   "Give the space and query bounds for four range-searching structures.",
   "Why can no structure beat the O(m) term?",
   "Describe a range tree and explain why its space is O(n log n).",
   "What is fractional cascading and what does it generalise to?",
   "Why must nearest-neighbour search descend the nearer child first?",
   "Give three concrete statements of the curse of dimensionality.",
   "Why does a linear scan win in high dimensions?",
   "Name five approximate methods and why approximation is appropriate.",
   "Why do engines use grids despite worse bounds?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Visibility and Motion Planning",
 "subtitle": "What can be seen, and how to get there.",
 "question": "What is visible from here, and how do I move without "
             "colliding?",
 "outcomes": [
     "Compute a visibility polygon by angular sweep.",
     "Build a visibility graph and use it for shortest paths.",
     "Explain configuration space and the Minkowski sum.",
     "Explain how a navigation mesh is built and why.",
     "Compare roadmap, sampling, and grid-based planners.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Visibility polygons",
   "blurb": "An angular sweep."},

  {"t": "callout", "title": "Visibility from a point is a rotational sweep",
   "kind": "The algorithm",
   "body": ["<b>Sort all obstacle vertices by angle about the "
            "viewpoint.</b> Sweep a ray through them in order.",
            "<b>Maintain the obstacle edges the ray currently crosses, "
            "ordered by distance</b> — the status structure "
            "(Module 04), now angular.",
            "<b>The nearest edge is what is visible in that "
            "direction.</b> When the nearest edge changes, emit a vertex "
            "of the visibility polygon.",
            "<b>O(n log n), dominated by the angular sort.</b> This is the "
            "basis of 2D field-of-view, line-of-sight, and 2D dynamic "
            "lighting."]},

  {"t": "callout", "title": "The degeneracies are the usual suspects",
   "kind": "What breaks it",
   "body": ["<b>Collinear vertices</b> — two obstacle corners at the same "
            "angle from the viewpoint. The sweep order between them is "
            "undefined.",
            "<b>The viewpoint exactly on an edge or at a vertex</b>, which "
            "is extremely common when the viewer is an agent standing "
            "against a wall.",
            "<b>Angle comparison invites <code>atan2</code></b>, which "
            "destroys exactness — compare with <code>orient</code> "
            "instead (Module 03 §1).",
            "<b>And the sweep wraps around at ±π</b>, so the "
            "comparator must be a cyclic one, which is a classic source of "
            "subtle bugs."]},

  {"t": "section", "label": "Part 2", "title": "Configuration space",
   "blurb": "The idea that makes planning tractable."},

  {"t": "callout", "title": "Shrink the robot to a point, grow the obstacles",
   "kind": "The central idea of motion planning",
   "body": ["<b>Planning for a shape is hard; planning for a point is "
            "easy.</b>",
            "<b>So transform the problem:</b> replace each obstacle O with "
            "the Minkowski sum O ⊕ (−R), where R is the robot. The "
            "robot becomes a single point.",
            "<b>A point path through the grown obstacles corresponds "
            "exactly to a collision-free motion of the original "
            "shape.</b>",
            "<b>For a translating convex robot the sum is convex and "
            "computable in O(n + m)</b> by merging edges in angular order "
            "— which is cheap. <b>Rotation adds a dimension and makes "
            "it much harder.</b>"]},

  {"t": "eq", "kicker": "Minkowski", "title": "The sum, and its one easy case",
   "eqs": [
     ("A ⊕ B = { a + b : a ∈ A, b ∈ B }",
      "Every point of A translated by every point of B."),
     ("Convex ⊕ convex: merge the edge vectors by angle",
      "O(n + m), and the result is convex with n + m edges."),
     ("Non-convex: O(n²m²) in the worst case",
      "Which is why decomposition into convex pieces (Module 03) comes "
      "first."),
   ],
   "caption": "<b>The convex case being linear is why convex decomposition "
              "is everywhere</b> in collision and planning.",
   "note": "This is the same reason GJK needs convexity (Module 12)."},

  {"t": "section", "label": "Part 3", "title": "Roadmaps",
   "blurb": "Precompute the connectivity."},

  {"t": "table", "kicker": "Planners", "title": "Four ways to plan a path",
   "header": ["Method", "Idea", "Character"],
   "widths": [2.8, 4.3, 5.0],
   "rows": [
     ["<b>Visibility graph</b>", "<b>Connect mutually visible vertices; shortest path</b>", "<b>Optimal path. O(n&#178;) graph</b>"],
     ["<b>Navigation mesh</b>", "<b>Convex cells covering walkable space</b>", "<b>What games use. Funnel for the path</b>"],
     ["<b>Grid / A*</b>", "Discretise; search", "<b>Simple; paths look discretised</b>"],
     ["<b>PRM</b>", "Sample configurations; connect", "<b>High dimensions; multi-query</b>"],
     ["RRT / RRT*", "Grow a tree toward random samples", "<b>Single-query; RRT* is optimal in the limit</b>"],
   ],
   "footnote": "<b>Visibility graphs give shortest paths; navmeshes give "
               "fast, natural-looking ones.</b> Games choose the second.",
   "note": "The optimal-vs-natural distinction is the key design point."},

  {"t": "callout", "title": "Why a navmesh beats a grid",
   "kind": "The engine's actual choice",
   "body": ["<b>A grid discretises space uniformly</b>, so a large open "
            "room costs as many cells as a cluttered corridor, and paths "
            "are constrained to grid directions.",
            "<b>A navmesh covers the walkable surface with convex "
            "polygons</b>, so one polygon can be an entire room and the "
            "cell count tracks the complexity of the geometry.",
            "<b>Convexity is the point:</b> within one cell, straight-line "
            "movement is guaranteed collision-free, so the path only needs "
            "cell-to-cell decisions.",
            "<b>Then the funnel algorithm pulls the path taut</b> through "
            "the sequence of shared edges, producing the shortest path "
            "within that corridor — which looks natural rather than "
            "stepped."]},

  {"t": "bullets", "kicker": "Building one", "title": "How a navmesh is generated",
   "items": [
     "<b>1. Voxelise the world geometry</b> and mark cells as solid or "
     "open.",
     "",
     "<b>2. Filter by walkability</b> — slope limit, step height, "
     "agent crouch height, ledge detection.",
     "",
     "<b>3. Extract the walkable surface</b> and build a distance field "
     "over it.",
     "",
     "<b>4. Watershed-partition into regions</b>, then trace region "
     "contours.",
     "",
     "<b>5. Simplify the contours and triangulate</b> (Module 05), then "
     "merge into convex polygons.",
     "",
     "<b>And erode by the agent radius</b> — which is the Minkowski sum "
     "of Part 2, applied.",
   ],
   "footnote": "<b>Recast does exactly this</b>, and it is the standard "
               "open implementation."},

  {"t": "section", "label": "Part 4", "title": "Sampling",
   "blurb": "When the configuration space is too big to build."},

  {"t": "callout", "title": "Sampling-based planning gives up completeness",
   "kind": "The trade",
   "body": ["<b>A robot arm with seven joints has a seven-dimensional "
            "configuration space.</b> Building it explicitly is "
            "hopeless.",
            "<b>So sample it:</b> pick random configurations, keep the "
            "collision-free ones, connect nearby pairs, and search the "
            "resulting graph.",
            "<b>This is <i>probabilistically</i> complete</b> — it finds "
            "a path if one exists, given enough samples. It cannot report "
            "that none exists.",
            "<b>And it struggles with narrow passages</b>, which have "
            "small volume and so are rarely sampled. <b>That is the "
            "characteristic failure mode</b>, and most of the literature is "
            "about mitigating it."]},
 ],
 "takeaways": [
   "A visibility polygon is an angular sweep maintaining edges ordered by "
   "distance; the nearest edge is what is visible.",
   "Configuration space shrinks the robot to a point and grows obstacles by "
   "the Minkowski sum, turning a shape-planning problem into a "
   "point-planning one.",
   "Minkowski sum of two convex polygons is O(n + m) by merging edge "
   "vectors in angular order — which is why convex decomposition comes "
   "first.",
   "Visibility graphs give optimal paths; navmeshes give fast "
   "natural-looking ones, which is what games choose.",
   "A navmesh's convex cells guarantee straight-line movement within a "
   "cell, and the funnel algorithm pulls the corridor path taut.",
   "Sampling-based planners are only probabilistically complete and fail "
   "characteristically on narrow passages.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Visibility polygons"),
  ("callout", "Visibility from a point is a rotational sweep",
   ["<b>Sort every obstacle vertex by its angle about the viewpoint</b>, "
    "and sweep a ray through them in that order. This is the plane sweep of "
    "Module 04 with an angular rather than a linear parameter.",
    "<b>Maintain the set of obstacle edges the ray currently crosses, "
    "ordered by distance from the viewpoint</b> — the status "
    "structure. Edges enter when the ray reaches their first endpoint and "
    "leave at their second.",
    "<b>The nearest edge in the status structure is what is visible in the "
    "current direction.</b> Whenever the nearest edge changes — "
    "because a closer edge was inserted, or the current nearest was removed "
    "— emit a vertex of the visibility polygon.",
    "<b>O(n log n), dominated by the angular sort.</b> This is the "
    "foundation of two-dimensional field-of-view cones, line-of-sight "
    "checks, guard coverage (Module 05 &sect;4), and 2D dynamic lighting "
    "and shadow casting."]),
  ("callout", "The degeneracies are the usual suspects",
   ["<b>Collinear vertices</b> — two obstacle corners at exactly the "
    "same angle from the viewpoint. The sweep order between them is "
    "undefined, and choosing wrongly inserts an edge before removing the "
    "one it should replace, corrupting the nearest-edge determination.",
    "<b>The viewpoint lying exactly on an obstacle edge or at a vertex.</b> "
    "<b>This is extremely common in practice</b>, because agents stand "
    "against walls and in doorways — it is the normal case, not an "
    "edge case, which is Module 01 &sect;4 in miniature.",
    "<b>Angle comparison invites <code>atan2</code></b>, which is "
    "transcendental and immediately destroys any exactness established in "
    "Module 02. <b>Compare angles with <code>orient</code> instead</b>, "
    "after bucketing by half-plane — the same correction as Module 03 "
    "&sect;1.",
    "<b>And the sweep wraps around at &plusmn;&pi;</b>, so the comparator "
    "must be cyclic rather than linear. <b>A classic source of subtle "
    "bugs:</b> the visibility polygon comes out correct except for one "
    "wrong vertex near the start angle, which is hard to spot and easy to "
    "misattribute."]),

  ("h1", "2 &nbsp; Configuration space"),
  ("callout", "Shrink the robot to a point, grow the obstacles",
   ["<b>Planning a collision-free motion for a shape is hard; planning for "
    "a point is easy.</b> The difficulty is entirely in the robot having "
    "extent, because then collision depends on the robot's whole footprint "
    "at every position along the path.",
    "<b>So transform the problem.</b> Replace each obstacle O with the "
    "Minkowski sum O &oplus; (&minus;R), where R is the robot shape taken "
    "about its reference point. <b>The robot becomes a single point</b> "
    "moving among the enlarged obstacles.",
    "<b>A point path through the grown obstacles corresponds exactly to a "
    "collision-free motion of the original shape</b> — the "
    "correspondence is exact, not approximate, which is what makes the "
    "transformation worth doing.",
    "<b>For a translating convex robot the sum is convex and computable in "
    "O(n + m)</b>, by merging the two polygons' edge vectors in angular "
    "order. That is remarkably cheap. <b>Rotation adds a dimension</b> "
    "— the configuration space becomes three-dimensional for a planar "
    "robot — <b>and the obstacles in it are no longer polygonal</b>, "
    "which is where the problem becomes genuinely hard."]),
  ("eq", "A &oplus; B = { a + b : a &isin; A, b &isin; B }"),
  ("p", "<b>Convex &oplus; convex is O(n + m)</b> by merging edge vectors "
        "in angular order, and the result is convex with at most n + m "
        "edges. <b>Non-convex &oplus; non-convex is O(n&#178;m&#178;) in "
        "the worst case</b> and the result may have holes. <b>This gap is "
        "why convex decomposition (Module 03 &sect;3) is everywhere in "
        "collision and planning</b> — it is the same reason GJK "
        "requires convexity (Module 12), and the same reason navmesh cells "
        "are convex (&sect;3)."),

  ("break",),
  ("h1", "3 &nbsp; Roadmaps and navigation meshes"),
  ("table", ["Method", "Idea", "Character"],
   [["<b>Visibility graph</b>",
     "<b>Connect every pair of mutually visible obstacle vertices</b>, then "
     "run a shortest-path search on the resulting graph.",
     "<b>Produces the genuinely shortest path</b> in the plane, because an "
     "optimal path bends only at obstacle vertices. <b>The graph is "
     "O(n&#178;)</b>, which limits it to modest scenes."],
    ["<b>Navigation mesh</b>",
     "<b>Cover the walkable surface with convex polygons</b>, search the "
     "adjacency graph, then smooth.",
     "<b>What games actually use.</b> Cell count tracks geometric "
     "complexity rather than area, and the funnel algorithm produces a "
     "natural path (below)."],
    ["<b>Grid with A*</b>",
     "Discretise the world uniformly and search.",
     "<b>Simple and robust</b>, and <b>paths look discretised</b> — "
     "diagonal stair-stepping that needs post-smoothing. Cost scales with "
     "area, not complexity."],
    ["<b>Probabilistic roadmap (PRM)</b>",
     "Sample random configurations, keep collision-free ones, connect "
     "nearby pairs.",
     "<b>Handles high-dimensional configuration spaces</b>, and amortises "
     "well over many queries in a static world."],
    ["<b>RRT and RRT*</b>",
     "Grow a tree from the start toward random samples.",
     "<b>Single-query and fast</b>; plain RRT gives poor paths, while "
     "<b>RRT* converges to optimal</b> given time."]],
   [0.20, 0.36, 0.44]),
  ("callout", "Why a navmesh beats a grid",
   ["<b>A grid discretises space uniformly</b>, so a large empty room costs "
    "exactly as many cells as an equally large cluttered one, and movement "
    "is constrained to the grid's directions — producing the "
    "characteristic stair-stepped path that needs a smoothing pass to look "
    "acceptable.",
    "<b>A navigation mesh covers the walkable surface with convex "
    "polygons</b>, so a single polygon can be an entire room. <b>The cell "
    "count tracks the complexity of the geometry rather than its area</b>, "
    "which is a very large saving in open environments.",
    "<b>Convexity is the whole point.</b> Within one convex cell, "
    "straight-line movement between any two points is guaranteed "
    "collision-free, so the path search only ever needs to make "
    "cell-to-cell decisions — the within-cell motion is free.",
    "<b>Then the funnel algorithm pulls the path taut</b> through the "
    "sequence of shared edges (the 'portals') between consecutive cells, "
    "producing the shortest path within that corridor in linear time. "
    "<b>The result looks natural rather than stepped</b>, and it is optimal "
    "given the corridor — though not necessarily globally, since the "
    "corridor itself came from a graph search."]),
  ("ol", ["<b>Voxelise the world geometry</b>, marking each voxel solid or "
          "open.",
          "<b>Filter by walkability:</b> apply a maximum slope, a maximum "
          "step height, the agent's required clearance height, and ledge "
          "detection. <b>This is where agent parameters enter</b>, which is "
          "why a navmesh is built per agent size.",
          "<b>Extract the walkable surface</b> — the top faces of the "
          "remaining spans — and build a distance field giving each "
          "cell's distance to the nearest obstacle or ledge.",
          "<b>Watershed-partition the distance field into regions</b>, so "
          "that region boundaries fall in corridors rather than across open "
          "space, then trace each region's contour.",
          "<b>Simplify the contours, triangulate them</b> (Module 05), and "
          "merge adjacent triangles into larger convex polygons wherever "
          "convexity is preserved.",
          "<b>And erode everything by the agent radius</b> — which is "
          "exactly the Minkowski sum of &sect;2, applied as a distance-"
          "field threshold rather than computed polygonally. <b>Recast does "
          "precisely this</b>, and it is the standard open implementation "
          "worth reading."]),

  ("h1", "4 &nbsp; Sampling-based planning"),
  ("callout", "Sampling gives up completeness, deliberately",
   ["<b>A robot arm with seven revolute joints has a seven-dimensional "
    "configuration space</b>, and the obstacles in it are the "
    "high-dimensional images of the physical obstacles under the forward "
    "kinematics. <b>Constructing that space explicitly is hopeless</b> "
    "— Module 10 &sect;3's volume arguments apply in full.",
    "<b>So sample it instead:</b> draw random configurations, discard those "
    "in collision (which only requires a collision <i>test</i>, never an "
    "explicit obstacle representation), connect nearby surviving samples "
    "with local paths, and search the resulting graph.",
    "<b>This is <i>probabilistically</i> complete</b> — the "
    "probability of finding a path approaches 1 as samples increase, if one "
    "exists. <b>It can never report that no path exists</b>, only fail to "
    "find one, which is a real limitation when the answer matters.",
    "<b>And it struggles with narrow passages.</b> A thin corridor in "
    "configuration space has small volume and is therefore rarely sampled, "
    "so the planner may run for a very long time on a problem whose "
    "solution is geometrically obvious. <b>That is the characteristic "
    "failure mode</b>, and a large fraction of the sampling-based planning "
    "literature is about mitigating it — bridge sampling, "
    "obstacle-based sampling, and medial-axis sampling (Module 08 "
    "&sect;4) all target exactly this."]),
 ],
 "resources": [
   ("LaValle &mdash; Planning Algorithms (free book)",
    "http://lavalle.pl/planning/",
    "<b>The reference for &sect;2 and &sect;4</b>, free in full. "
    "Configuration space, PRM, and RRT from the author of RRT."),
   ("de Berg et al. &mdash; Computational Geometry, chapters 13 and 15 "
    "(robot motion planning, visibility graphs)",
    "https://www.springer.com/gp/book/9783642096815",
    "Minkowski sums and visibility graphs, with the complexity analyses."),
   ("Mikko Mononen &mdash; Recast and Detour (free)",
    "https://github.com/recastnavigation/recastnavigation",
    "<b>The navmesh pipeline of &sect;3, implemented.</b> The standard "
    "open-source navigation toolkit; the source is the documentation."),
   ("Amit Patel &mdash; Red Blob Games, pathfinding and visibility (free)",
    "https://www.redblobgames.com/",
    "Interactive explanations of A*, the funnel algorithm, and 2D "
    "visibility. <b>Unusually good for building intuition</b> before "
    "reading the formal treatments."),
 ],
 "exercises": [
   "Implement a visibility polygon by angular sweep and render it.",
   "<b>Place the viewpoint exactly on a vertex and on an edge</b> and fix "
   "what breaks.",
   "Replace <code>atan2</code> comparison with <code>orient</code>-based "
   "comparison and verify the output is unchanged.",
   "Implement the Minkowski sum of two convex polygons in O(n + m).",
   "<b>Grow a set of obstacles by a disc robot</b> and verify that a "
   "point path through the grown obstacles is collision-free for the "
   "original.",
   "Build a visibility graph and find shortest paths. Compare the path "
   "length against A* on a grid.",
   "<b>Implement the funnel algorithm</b> over a sequence of navmesh "
   "portals and compare against the unsmoothed cell-centre path.",
   "Generate a navmesh from a simple scene by the six-step pipeline.",
   "Implement PRM and RRT for a 2D disc robot and compare path quality and "
   "time.",
   "<b>Construct a narrow-passage problem</b> and measure how sample count "
   "scales with the passage width.",
 ],
 "selfcheck": [
   "Describe the visibility sweep and what its status structure holds.",
   "Name four degeneracies in the visibility sweep.",
   "What is configuration space and what transformation builds it?",
   "State the Minkowski sum and give the convex and non-convex costs.",
   "Compare five planning methods on optimality and cost.",
   "Give three reasons a navmesh beats a grid.",
   "Why must navmesh cells be convex?",
   "What does the funnel algorithm do?",
   "What is probabilistic completeness, and what is the narrow-passage "
   "problem?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Geometry in Three Dimensions",
 "subtitle": "Collision queries, decomposition, and broken meshes.",
 "question": "How do you answer geometric queries on real 3D assets?",
 "outcomes": [
     "Implement GJK for convex distance and intersection.",
     "Explain EPA and why penetration depth needs it.",
     "Apply convex decomposition and say why it is needed.",
     "Diagnose and repair the standard mesh defects.",
     "Use the separating axis theorem where it fits.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "GJK",
   "blurb": "Convex intersection, without building anything."},

  {"t": "callout", "title": "GJK reduces intersection to a question about the origin",
   "kind": "The reframing that makes it work",
   "body": ["<b>Two convex shapes A and B intersect if and only if their "
            "Minkowski difference A ⊖ B contains the origin.</b>",
            "<b>So the problem becomes: is the origin inside this one "
            "convex set?</b> Two shapes have become one.",
            "<b>And the difference is never constructed.</b> GJK needs "
            "only a <i>support function</i> — given a direction, return "
            "the farthest point of the shape in it.",
            "<b>That is why GJK works on any convex shape</b>: polyhedra, "
            "spheres, capsules, cones, and their convex hulls, all behind "
            "one interface. <b>No face lists, no vertex counts.</b>"]},

  {"t": "code", "kicker": "GJK", "title": "The loop",
   "lang": "text", "code": """
  support(A, B, d) = farthest_point(A, d) - farthest_point(B, -d)

  simplex = [ support(A, B, any_direction) ]
  d = -simplex[0]                          # search toward the origin

  loop:
      p = support(A, B, d)
      if dot(p, d) < 0: return NO_INTERSECTION
          # the farthest point in direction d did not pass the origin,
          # so a separating plane exists. This is the early exit.

      simplex.add(p)
      if simplex contains the origin: return INTERSECTION
      d = direction from simplex toward the origin
      # and drop the simplex vertices that cannot help

  Converges in a handful of iterations for typical shapes.
  Returns DISTANCE for free if run to convergence when separated.
""",
   "caption": "<b>The early exit is the valuable part</b> — "
              "separated pairs are rejected in one or two iterations, and "
              "most pairs are separated.",
   "note": "Emphasise the support-function abstraction; it's the reusable "
           "idea."},

  {"t": "callout", "title": "EPA: GJK tells you that, not how much",
   "kind": "The companion algorithm",
   "body": ["<b>GJK returns a boolean when the shapes overlap</b>, and a "
            "physics solver needs the penetration depth and the contact "
            "normal to resolve it (CSCE 649 M06).",
            "<b>EPA — the Expanding Polytope Algorithm — starts from "
            "GJK's terminating simplex</b> and expands it toward the "
            "boundary of the Minkowski difference.",
            "<b>The nearest face when it stops gives the depth and the "
            "normal.</b>",
            "<b>EPA is slower and less numerically stable than GJK</b>, "
            "which is why engines avoid deep penetration in the first "
            "place — continuous collision detection and speculative "
            "contacts exist largely to keep EPA off the critical path."]},

  {"t": "section", "label": "Part 2", "title": "SAT",
   "blurb": "The alternative, and when it wins."},

  {"t": "table", "kicker": "Comparison", "title": "GJK against SAT",
   "header": ["", "GJK + EPA", "SAT"],
   "widths": [2.7, 4.6, 4.8],
   "rows": [
     ["<b>Shapes</b>", "<b>Any convex, via support function</b>", "Polyhedra with known faces"],
     ["<b>Axes tested</b>", "Iterative search", "<b>Face normals + edge cross products</b>"],
     ["Cost (boxes)", "Iterative", "<b>15 axes, fixed, branch-free</b>"],
     ["<b>Distance</b>", "<b>Free when separated</b>", "Not provided"],
     ["<b>Penetration</b>", "Needs EPA", "<b>Falls out directly</b>"],
     ["Curved shapes", "<b>Works</b>", "<b>Does not apply</b>"],
   ],
   "footnote": "<b>Use SAT for boxes and simple primitives; GJK for "
               "general convex shapes.</b> Most engines ship both.",
   "note": "The 15-axes figure for OBB-vs-OBB is worth stating — it's why "
           "SAT survives."},

  {"t": "section", "label": "Part 3", "title": "Convex decomposition",
   "blurb": "Because real assets are not convex."},

  {"t": "callout", "title": "Everything fast requires convexity, and nothing authored is convex",
   "kind": "The practical bind",
   "body": ["<b>GJK, SAT, and the Minkowski sum all require convex "
            "inputs</b> (Modules 11 and 12).",
            "<b>And no interesting asset is convex</b> — a chair, a "
            "weapon, a character, a piece of architecture.",
            "<b>Exact convex decomposition is expensive and produces far "
            "too many pieces</b> — a modestly concave mesh can yield "
            "hundreds.",
            "<b>So approximate convex decomposition is used:</b> allow "
            "each piece to be slightly non-convex, take its hull, and "
            "accept the small error. <b>V-HACD is the standard, and 20 to "
            "40 pieces is a typical budget.</b>"]},

  {"t": "bullets", "kicker": "Alternatives", "title": "What else is used for collision",
   "items": [
     "<b>Primitive fitting</b> — boxes, spheres, capsules placed by hand "
     "or fitted. Cheapest, and still extremely common.",
     "",
     "<b>Convex hull of the whole mesh</b> — one shape, crude, and fine "
     "for debris.",
     "",
     "<b>Triangle soup with a BVH</b> — exact, used for static level "
     "geometry only, because it has no inside.",
     "",
     "<b>Signed distance field</b> — sampled on a grid; excellent for "
     "deformation and for soft bodies.",
     "",
     "<b>Approximate convex decomposition</b> — the general answer for "
     "dynamic concave objects.",
   ],
   "footnote": "<b>Triangle soup cannot say 'inside'</b>, which is why "
               "dynamic objects never use it."},

  {"t": "section", "label": "Part 4", "title": "Broken meshes",
   "blurb": "What real assets are actually like."},

  {"t": "table", "kicker": "Defects", "title": "The standard mesh defects",
   "header": ["Defect", "What it breaks", "Repair"],
   "widths": [2.9, 4.3, 4.9],
   "rows": [
     ["<b>Duplicate vertices</b>", "<b>Adjacency; the mesh looks torn</b>", "<b>Weld within a tolerance</b>"],
     ["<b>Holes</b>", "<b>No inside/outside; SDF and CSG fail</b>", "<b>Fill by triangulating boundary loops</b>"],
     ["<b>Non-manifold edges</b>", "<b>&gt;2 faces per edge; half-edge impossible</b>", "Split or cut"],
     ["Inconsistent winding", "Normals point inward; backface culling wrong", "Flood-fill orientation"],
     ["<b>Self-intersection</b>", "<b>Volume undefined; booleans fail</b>", "<b>Hard. Often remesh instead</b>"],
     ["Degenerate faces", "Zero-area; normals undefined", "Collapse and remove"],
   ],
   "footnote": "<b>Self-intersection is the one with no cheap fix</b>, and "
               "it is extremely common in sculpted and scanned assets.",
   "note": "This table is what people actually spend their time on."},

  {"t": "callout", "title": "Watertight is the property that matters",
   "kind": "Why repair is not optional",
   "body": ["<b>A mesh is watertight when every edge has exactly two faces "
            "and the orientation is consistent.</b>",
            "<b>Only then is 'inside' defined</b> — and inside is what "
            "signed distance fields, booleans, volume, mass properties, "
            "and inertia tensors all need.",
            "<b>A mesh with one hole has no inside at all</b>, so every "
            "one of those computations silently produces nonsense rather "
            "than failing.",
            "<b>So validate before trusting.</b> <b>Check the Euler "
            "characteristic and the edge-to-face counts</b> — a few lines, "
            "and they catch most of the table above."]},
 ],
 "takeaways": [
   "GJK reduces convex intersection to whether the Minkowski difference "
   "contains the origin, and never constructs that difference.",
   "GJK needs only a support function, which is why it works uniformly on "
   "polyhedra, spheres, capsules, and cones.",
   "GJK's early exit rejects separated pairs in one or two iterations, "
   "which is the common case.",
   "EPA recovers penetration depth and contact normal, and is slower and "
   "less stable — which is why engines work to avoid deep penetration.",
   "Everything fast requires convexity and nothing authored is convex, so "
   "approximate convex decomposition is the standard asset-pipeline step.",
   "Watertightness is what makes 'inside' defined, and without it SDFs, "
   "booleans, volume and inertia silently produce nonsense.",
 ],
 "notes": [
  ("h1", "1 &nbsp; GJK and EPA"),
  ("callout", "GJK reduces intersection to a question about the origin",
   ["<b>Two convex shapes A and B intersect if and only if their Minkowski "
    "difference A &oplus; (&minus;B) contains the origin.</b> If some point "
    "is in both shapes, its difference with itself is zero; conversely, if "
    "the origin is in the difference, some pair of points coincides.",
    "<b>So the problem becomes: is the origin inside this one convex "
    "set?</b> Two shapes have become one, and a pairwise question has "
    "become a containment question — which is a considerably simpler "
    "thing to search for.",
    "<b>And the difference is never actually constructed.</b> GJK requires "
    "only a <i>support function</i>: given a direction, return the farthest "
    "point of the shape in that direction. The support function of the "
    "difference is the difference of the support functions, evaluated in "
    "opposite directions.",
    "<b>That abstraction is why GJK works on any convex shape</b> — "
    "polyhedra, spheres, capsules, cylinders, cones, ellipsoids, and the "
    "convex hull of any point set, all behind one interface, with no face "
    "lists and no vertex counts. <b>It is the most reusable idea in this "
    "module</b>, and it is why a single code path handles every collision "
    "primitive an engine ships."]),
  ("code", """support(A, B, d) = farthest(A, d) - farthest(B, -d)

simplex = [ support(A, B, arbitrary_direction) ]
d = -simplex[0]

loop:
    p = support(A, B, d)
    if dot(p, d) < 0: return SEPARATED     # EARLY EXIT: a separating
                                           # plane must exist
    simplex.add(p)
    if simplex contains the origin: return INTERSECTING
    d = direction from the simplex toward the origin
    drop simplex vertices that cannot contribute

Converges in a few iterations. Gives DISTANCE free when separated."""),
  ("p", "<b>The early exit is the valuable part in practice.</b> If the "
        "farthest point of the Minkowski difference in direction d does not "
        "reach past the origin, then no point of the difference does, so a "
        "separating plane exists and the shapes cannot intersect. "
        "<b>Separated pairs are rejected in one or two iterations</b>, and "
        "in a broad-phase-filtered narrow phase most pairs are separated "
        "— so the common case is the cheap one."),
  ("callout", "EPA: GJK tells you <i>that</i>, not <i>how much</i>",
   ["<b>GJK returns a boolean when the shapes overlap</b>, and that is not "
    "enough for a physics solver, which needs the penetration depth and the "
    "contact normal in order to compute an impulse or a positional "
    "correction (CSCE 649 Module 06).",
    "<b>EPA — the Expanding Polytope Algorithm — starts from the "
    "simplex GJK terminated with</b> (which encloses the origin) and "
    "repeatedly expands it toward the boundary of the Minkowski difference, "
    "by finding the face nearest the origin and pushing it outward with a "
    "new support point.",
    "<b>When no further expansion is possible, the nearest face gives the "
    "penetration depth and the contact normal</b> — the minimum "
    "translation that separates the shapes.",
    "<b>EPA is slower and markedly less numerically stable than GJK</b>, "
    "because it maintains and repeatedly modifies a polytope near a "
    "degenerate configuration. <b>This is why engines work hard to avoid "
    "deep penetration in the first place</b>: continuous collision "
    "detection, speculative contacts, and conservative advancement all "
    "exist in large part to keep EPA off the critical path, and to keep "
    "penetrations shallow enough that it converges quickly when it does "
    "run."]),

  ("h1", "2 &nbsp; The separating axis theorem"),
  ("table", ["", "GJK + EPA", "SAT"],
   [["<b>Applicable shapes</b>",
     "<b>Any convex shape, through its support function</b> — "
     "including curved ones.",
     "Polyhedra with explicitly known faces and edges."],
    ["<b>How axes are chosen</b>", "Iteratively, by search.",
     "<b>Enumerated:</b> both shapes' face normals, plus the cross products "
     "of all edge-direction pairs."],
    ["<b>Cost for two boxes</b>", "Iterative; a few support evaluations.",
     "<b>Exactly 15 axes</b> (3 + 3 face normals, 9 edge cross products), "
     "<b>fixed and branch-free</b> — which vectorises and pipelines "
     "beautifully."],
    ["<b>Distance when separated</b>",
     "<b>Free, if run to convergence.</b>", "Not provided."],
    ["<b>Penetration depth</b>", "Requires EPA.",
     "<b>Falls out directly</b> — the axis of minimum overlap is the "
     "answer."],
    ["<b>Curved shapes</b>", "<b>Works unchanged.</b>",
     "<b>Does not apply</b> — there is no finite axis set."]],
   [0.19, 0.38, 0.43]),
  ("p", "<b>Use SAT for boxes and simple primitives, and GJK for general "
        "convex shapes.</b> The fixed 15-axis test for two oriented "
        "bounding boxes is the reason SAT survives despite GJK's greater "
        "generality: it is predictable, branch-free, and fast, and "
        "box-versus-box is an extremely common query. <b>Most engines ship "
        "both</b>, with a dispatch table selecting the specialised routine "
        "when both shapes are primitives and falling back to GJK "
        "otherwise."),

  ("break",),
  ("h1", "3 &nbsp; Convex decomposition"),
  ("callout", "Everything fast requires convexity; nothing authored is convex",
   ["<b>GJK, SAT, and the Minkowski sum of Module 11 all require convex "
    "inputs.</b> So does the guarantee that straight-line motion within a "
    "navmesh cell is collision-free. Convexity is the precondition for "
    "essentially every fast geometric query in an engine.",
    "<b>And no interesting authored asset is convex</b> — a chair, a "
    "weapon, a character, a staircase, a piece of architecture. Concavity "
    "is what makes a shape recognisable.",
    "<b>Exact convex decomposition is expensive and produces far too many "
    "pieces.</b> A modestly concave mesh can decompose into hundreds of "
    "exactly convex parts, and the collision cost scales with the piece "
    "count — so an exact decomposition is frequently slower than the "
    "problem it solves.",
    "<b>So approximate convex decomposition is used instead:</b> partition "
    "the mesh into parts that are <i>nearly</i> convex, take the convex "
    "hull of each, and accept the small volume error where the hull bulges "
    "past the original surface. <b>V-HACD is the standard implementation, "
    "and 20 to 40 pieces is a typical budget</b> for a character or a prop "
    "— chosen by measuring, not by principle."]),
  ("ul", ["<b>Primitive fitting</b> — boxes, spheres, and capsules "
          "placed by hand or fitted automatically. <b>By far the cheapest, "
          "and still extremely common</b>, especially for characters, where "
          "a capsule is both fast and behaviourally better than an accurate "
          "shape.",
          "<b>Convex hull of the whole mesh</b> — one shape, crude, "
          "and entirely adequate for debris, pickups, and anything the "
          "player will not inspect closely.",
          "<b>Triangle soup with a BVH</b> — exact against the actual "
          "surface, and used for <b>static level geometry only</b>, because "
          "<b>a triangle soup has no inside</b>: it can answer 'does this "
          "ray hit the surface' but not 'is this point within the object', "
          "so a dynamic body can tunnel through or come to rest inside it.",
          "<b>Signed distance field</b> — sampled on a grid, giving "
          "cheap inside/outside and gradient queries. <b>Excellent for "
          "deformation, soft bodies, and destruction</b>, at the cost of "
          "memory and of resolution-limited sharp features.",
          "<b>Approximate convex decomposition</b> — the general "
          "answer for dynamic concave objects, and the only one that "
          "supports accurate contact against arbitrary authored shapes."]),

  ("h1", "4 &nbsp; Broken meshes"),
  ("table", ["Defect", "What it breaks", "Repair"],
   [["<b>Duplicate or near-duplicate vertices</b>",
     "<b>Adjacency is destroyed</b> — faces that should share an edge "
     "do not, so the mesh behaves as though torn even though it renders "
     "correctly.",
     "<b>Weld within a tolerance.</b> Note that this is the "
     "non-transitive-equality problem of Module 01 &sect;3, and the "
     "tolerance must be chosen with that in mind."],
    ["<b>Holes</b>",
     "<b>Inside and outside become undefined</b>, so signed distance "
     "fields, booleans, volume, and mass properties all fail — "
     "silently.",
     "Fill by identifying boundary loops and triangulating them "
     "(Module 05)."],
    ["<b>Non-manifold edges</b>",
     "<b>More than two faces share an edge</b>, so a half-edge "
     "representation cannot be built and 'the surface' is not a surface.",
     "Split the edge, or cut the mesh along it into manifold components."],
    ["<b>Inconsistent face winding</b>",
     "Normals point inward on some faces, so backface culling, lighting, "
     "and orientation tests are wrong.",
     "Flood-fill orientation from a seed face across the adjacency graph."],
    ["<b>Self-intersection</b>",
     "<b>Volume is undefined and booleans fail</b> (Module 06).",
     "<b>Genuinely hard, with no cheap fix.</b> Frequently the practical "
     "answer is to remesh — voxelise and re-extract — rather than "
     "repair. <b>Extremely common in sculpted and scanned assets.</b>"],
    ["<b>Degenerate faces</b>",
     "Zero area, so the normal is undefined and every downstream predicate "
     "is unreliable.",
     "Collapse the degenerate edge and remove the face."]],
   [0.20, 0.42, 0.38]),
  ("callout", "Watertight is the property that matters",
   ["<b>A mesh is watertight (closed and manifold) when every edge is "
    "shared by exactly two faces and the face orientations are "
    "consistent.</b>",
    "<b>Only then is 'inside' defined</b> — and inside is exactly what "
    "signed distance fields, boolean operations, volume, centre of mass, "
    "and the inertia tensor (CSCE 649 Module 07) all require.",
    "<b>A mesh with a single small hole has no inside at all</b>, in the "
    "strict sense. Every one of those computations will still run and will "
    "produce a number; the number will be meaningless. <b>Silent wrong "
    "answers, which Module 01 &sect;3 identified as the worst "
    "outcome.</b>",
    "<b>So validate before trusting.</b> <b>Check the Euler characteristic "
    "and the per-edge face counts</b> — a few lines of code that catch "
    "most of the table above, and which belong in the asset import path "
    "rather than in a debugging session six months later."]),
 ],
 "resources": [
   ("Ericson &mdash; Real-Time Collision Detection",
    "https://realtimecollisiondetection.net/",
    "<b>The reference for this whole module.</b> GJK, SAT, bounding "
    "volumes, and the practical choices of &sect;3. Library copy; the "
    "author's notes and errata are free."),
   ("Casey Muratori &mdash; Implementing GJK (free video)",
    "https://caseymuratori.com/blog_0003",
    "<b>The clearest explanation of &sect;1 available</b>, built up from "
    "the support-function idea rather than from the published pseudocode."),
   ("Mamou &mdash; V-HACD (free)",
    "https://github.com/kmammou/v-hacd",
    "The approximate convex decomposition of &sect;3, implemented and "
    "widely used."),
   ("Attene, Campen & Kobbelt &mdash; Polygon Mesh Repair: An Introduction "
    "(free)",
    "https://dl.acm.org/doi/10.1145/2431211.2431214",
    "<b>The &sect;4 defect taxonomy</b>, done systematically, with what "
    "can and cannot be repaired."),
 ],
 "exercises": [
   "Implement support functions for a point set, a sphere, and a capsule "
   "behind one interface.",
   "<b>Implement GJK</b> for intersection and verify against a brute-force "
   "separating-axis search.",
   "<b>Count GJK iterations</b> for separated, touching, and deeply "
   "overlapping pairs. Report the three distributions.",
   "Extend GJK to return the distance between separated shapes.",
   "Implement EPA and compare its stability at shallow and deep "
   "penetration.",
   "Implement SAT for two oriented boxes with all 15 axes. Benchmark "
   "against GJK on the same pairs.",
   "<b>Run V-HACD on a concave asset</b> at several piece budgets. Measure "
   "collision cost and volume error against piece count, and plot both.",
   "<b>Write a mesh validator</b> checking the Euler characteristic, "
   "edge-to-face counts, winding consistency, and degenerate faces.",
   "Run it on assets you have and report what fraction are watertight.",
   "Fill the holes in one and verify that its computed volume becomes "
   "meaningful.",
 ],
 "selfcheck": [
   "Why does the Minkowski difference containing the origin mean the "
   "shapes intersect?",
   "What is a support function, and why does it make GJK general?",
   "Explain GJK's early exit.",
   "What does EPA provide, and why do engines avoid needing it?",
   "Compare GJK and SAT on six axes.",
   "Why is exact convex decomposition impractical?",
   "Name five collision representations and when each is used.",
   "Why can a triangle soup not be used for dynamic objects?",
   "Name six mesh defects and what each breaks.",
   "Define watertight and say why it matters.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Shipping Geometric Code",
 "subtitle": "What to write, what to use, and what to promise.",
 "question": "How do you make geometric code that survives real input?",
 "outcomes": [
     "Choose a robustness strategy from the requirements.",
     "Separate predicates from constructions in an interface.",
     "Test geometric code in ways that actually find bugs.",
     "Judge when to use a library and which one.",
     "State what geometric code can honestly promise.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Choosing a strategy",
   "blurb": "The decision, made explicitly."},

  {"t": "table", "kicker": "Decision", "title": "Which robustness strategy",
   "header": ["If", "Then", "Because"],
   "widths": [3.3, 4.0, 4.8],
   "rows": [
     ["<b>Only predicates, no constructions</b>", "<b>Exact filtered predicates</b>", "<b>Module 02: ~2× cost, always right</b>"],
     ["<b>Constructions, bounded domain</b>", "<b>Fixed-point integer coordinates</b>", "<b>Exact inputs; simple reasoning</b>"],
     ["<b>Constructions, chained</b>", "<b>Snap rounding</b>", "<b>Stops error accumulating</b>"],
     ["Exact answers required", "Exact rational kernel", "<b>CAD; slow and correct</b>"],
     ["<b>Interactive, approximate OK</b>", "Filtered predicates + tolerant topology", "Fast; document the limits"],
   ],
   "footnote": "<b>The first row covers more cases than people expect</b> "
               "— hulls, triangulation, point location, and search all "
               "construct nothing.",
   "note": "Making the predicate/construction split the first question is "
           "the key move."},

  {"t": "callout", "title": "Separate predicates from constructions in the interface",
   "kind": "The design decision that matters most",
   "body": ["<b>Predicates can be made exact affordably.</b> "
            "Constructions cannot be made exact at all, in fixed "
            "precision (Module 06 §4).",
            "<b>So make the distinction visible in the API.</b> CGAL "
            "parameterises its kernels on exactly this — "
            "<code>Exact_predicates_inexact_constructions_kernel</code> is "
            "the most-used type in the library for a reason.",
            "<b>Then a caller knows what it is getting:</b> a correct "
            "<i>combinatorial</i> answer with approximate coordinates, or "
            "both exact at a cost.",
            "<b>And most callers want the first.</b> The topology must be "
            "right; the coordinates can be a few ULPs off."]},

  {"t": "section", "label": "Part 2", "title": "Testing",
   "blurb": "What actually finds geometric bugs."},

  {"t": "bullets", "kicker": "Testing", "title": "How to test geometric code",
   "items": [
     "<b>Property-based tests, not example-based.</b> The hull is convex; "
     "the triangulation has n − 2 triangles; the union area is at "
     "most the sum.",
     "",
     "<b>Degenerate generators</b> from Module 01 — lattices, collinear "
     "runs, duplicates, cocircular sets.",
     "",
     "<b>Exact rational ground truth</b> on small inputs.",
     "",
     "<b>Metamorphic tests:</b> translate, rotate, scale, and permute the "
     "input — the answer must transform correspondingly.",
     "",
     "<b>Differential testing</b> against CGAL or another "
     "implementation.",
     "",
     "<b>And render every failure.</b> You will see it in seconds.",
   ],
   "footnote": "<b>Metamorphic testing is the underused one</b> — "
               "permuting the input order finds degeneracy bugs "
               "immediately."},

  {"t": "callout", "title": "Why permuting the input is the best single test",
   "kind": "A cheap test that finds real bugs",
   "body": ["<b>The output of a geometric algorithm should not depend on "
            "the order the input was given in</b> — up to a documented "
            "tie-breaking rule.",
            "<b>So shuffle and re-run.</b> If the answer changes, you have "
            "found either a degeneracy that is not handled consistently or "
            "a predicate that is not exact.",
            "<b>It needs no ground truth</b>, no reference "
            "implementation, and no expected output — just two runs that "
            "must agree.",
            "<b>And it catches exactly the bugs that matter</b>, because "
            "inconsistent predicates are order-sensitive almost by "
            "definition (Module 01 §2)."]},

  {"t": "section", "label": "Part 3", "title": "Libraries",
   "blurb": "What to use, and when not to."},

  {"t": "table", "kicker": "Libraries", "title": "What to reach for",
   "header": ["Library", "Covers", "Character"],
   "widths": [2.6, 4.3, 5.2],
   "rows": [
     ["<b>CGAL</b>", "<b>Essentially everything in this course</b>", "<b>Exact, correct, heavy. GPL or commercial</b>"],
     ["<b>Clipper2</b>", "2D booleans and offsetting", "<b>Integer coordinates; robust; small</b>"],
     ["<b>Triangle / Shewchuk</b>", "2D quality meshing", "<b>The &sect;3 reference for Module 09</b>"],
     ["earcut", "Polygon triangulation", "<b>Tiny, fast, permissive</b>"],
     ["<b>qhull</b>", "Hulls, Delaunay, Voronoi in nD", "The lifting map (Module 08) applied"],
     ["<b>libigl / Open3D</b>", "Mesh processing and repair", "Research-oriented; good defaults"],
   ],
   "footnote": "<b>Check the licence before the features.</b> CGAL's "
               "GPL/commercial split has decided a great many "
               "architectural choices.",
   "note": "The licensing note is practical and genuinely shapes "
           "decisions."},

  {"t": "callout", "title": "When to write it yourself",
   "kind": "The honest answer",
   "body": ["<b>When the problem is small and the dependency is not "
            "worth it.</b> A convex hull is twenty lines (Module 03).",
            "<b>When you need a specific degeneracy policy</b> the "
            "library does not offer — the collinear-point decision, for "
            "instance.",
            "<b>When the data layout matters</b> and the library's types "
            "would force a conversion in a hot loop.",
            "<b>And to understand it.</b> <b>Which is the point of this "
            "course</b> — you cannot evaluate a library's guarantees "
            "without knowing what the guarantees could be."]},

  {"t": "section", "label": "Part 4", "title": "Claiming honestly",
   "blurb": "The course, closed."},

  {"t": "bullets", "kicker": "Claims", "title": "What geometric code can honestly promise",
   "items": [
     "<b>'Predicates are exact; constructions are rounded to double.'</b> "
     "Precise, and it tells the caller what they have.",
     "",
     "<b>'Degeneracies are resolved by symbolic perturbation'</b> — so "
     "the output is valid for an infinitesimally nearby input.",
     "",
     "<b>'Output is snap-rounded to a grid of size g; no point moves "
     "more than d.'</b>",
     "",
     "<b>'Tested against exact rational arithmetic on inputs up to "
     "n = 100, and differentially against CGAL above that.'</b>",
     "",
     "<b>And what you cannot say: 'it is robust'.</b> Say which inputs, "
     "which guarantees, and which cases are known to fail.",
   ],
   "footnote": "<b>'Robust' is the word that means nothing</b> in this "
               "field, and it is the one most often used."},

  {"t": "callout", "title": "Where this leaves you",
   "kind": "Closing",
   "body": ["You can implement the standard structures — hulls, "
            "triangulations, subdivisions, diagrams — and you know which "
            "predicate each rests on.",
            "<b>And you know the thing that most people working with "
            "geometry do not:</b> that the failures are about arithmetic "
            "rather than algorithms, and that they are fixable.",
            "<b>CSCE 629 gave the complexity analysis; 641 and 645 gave "
            "the representations; 649 assumed the collision geometry; "
            "647 assumed the acceleration structures.</b>",
            "<b>This course built what those assumed</b> — and the next "
            "two, CSCE 605 and CSCE 678, build the compiler and the "
            "network the rest of the engine needs."]},
 ],
 "takeaways": [
   "The first question is whether you construct new points or only "
   "classify existing ones — it determines the whole strategy.",
   "Make the predicate/construction distinction visible in the interface, "
   "as CGAL's kernel names do.",
   "Most callers want exact topology with approximate coordinates, which is "
   "the cheapest useful guarantee.",
   "Test by property, by degenerate generator, by exact rational ground "
   "truth, and metamorphically — not by examples.",
   "Permuting the input and requiring the same answer needs no ground "
   "truth and finds exactly the bugs that matter.",
   "'Robust' means nothing — state which inputs, which guarantees, and "
   "which cases are known to fail.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Choosing a strategy"),
  ("table", ["If your code...", "Then use...", "Because"],
   [["<b>only classifies existing points — no new coordinates are "
     "computed</b>",
     "<b>Exact filtered predicates</b> (Module 02).",
     "<b>Roughly 2&times; the cost of naive, and always correct.</b> "
     "<b>This row covers more than people expect:</b> convex hulls, "
     "triangulation, Delaunay, point location, range searching, and "
     "visibility all construct nothing."],
    ["<b>constructs points, within a bounded domain</b>",
     "<b>Fixed-point integer coordinates</b>, scaled onto a grid.",
     "<b>Inputs become exactly representable and comparisons become "
     "trivially reliable.</b> The most underrated option (Module 06 "
     "&sect;4), and what Clipper does."],
    ["<b>chains constructions — the output of one operation feeds the "
     "next</b>",
     "<b>Snap rounding.</b>",
     "<b>Stops error accumulating across the chain</b>, at the cost of "
     "possible topology change. Document the displacement bound."],
    ["<b>must produce provably exact answers</b>",
     "An exact rational kernel (CGAL).",
     "<b>Correct, and slow</b>, with coordinate size growing through the "
     "computation. CAD and verification need it; real-time does not."],
    ["<b>is interactive and can tolerate approximation</b>",
     "Filtered predicates with a tolerant topological layer.",
     "Fast, and the limits must be documented rather than discovered."]],
   [0.28, 0.26, 0.46]),
  ("callout", "Separate predicates from constructions in the interface",
   ["<b>Predicates can be made exact affordably</b> — Module 02 "
    "established that. <b>Constructions cannot be made exact at all in "
    "fixed precision</b>, because the result is simply not representable "
    "(Module 06 &sect;4). These are different problems with different "
    "costs, and conflating them is the most common design error in "
    "geometric libraries.",
    "<b>So make the distinction visible in the API.</b> CGAL parameterises "
    "its kernels on exactly this axis, and "
    "<code>Exact_predicates_inexact_constructions_kernel</code> is the "
    "most-used type in the library — a name that is both unwieldy and "
    "exactly right, because it states the guarantee.",
    "<b>Then a caller knows what it is getting:</b> either a correct "
    "<i>combinatorial</i> answer with coordinates rounded to "
    "<code>double</code>, or both exact at a substantial cost, and the "
    "choice is theirs to make with information.",
    "<b>And most callers want the first.</b> <b>The topology must be "
    "right</b> — the hull must be convex, the triangulation must "
    "cover, the mesh must be watertight — <b>while the coordinates "
    "can be a few ULPs off without anyone noticing or caring.</b> That is "
    "the cheapest useful guarantee in geometric computing, and recognising "
    "that it is usually sufficient is worth a great deal."]),

  ("h1", "2 &nbsp; Testing"),
  ("ul", ["<b>Property-based tests rather than example-based ones.</b> The "
          "hull is convex and contains every input point; the triangulation "
          "has exactly n &minus; 2 triangles and covers the polygon without "
          "overlap; the area of a union is at most the sum of the areas. "
          "<b>These hold for every input</b>, so they can be checked "
          "against generated data rather than hand-written cases.",
          "<b>Degenerate generators</b> from Module 01 &sect;4 — "
          "lattices, collinear runs, duplicates, one-ULP pairs, cocircular "
          "sets, axis-aligned configurations. <b>These are the tests; "
          "random points are not.</b>",
          "<b>Exact rational ground truth</b> on small inputs. Too slow to "
          "ship and ideal for deciding what the answer should have been.",
          "<b>Metamorphic tests:</b> translate, rotate, scale, reflect, and "
          "permute the input; the output must transform correspondingly or "
          "be unchanged. <b>No expected output is needed</b>, which is what "
          "makes them cheap to write.",
          "<b>Differential testing</b> against CGAL or another "
          "implementation on the same inputs, which catches disagreements "
          "neither side's own tests would find.",
          "<b>And render every failure.</b> A failed geometric test is "
          "nearly unreadable as numbers and obvious as a picture — "
          "which is why Module 01 asked for SVG output on day one."]),
  ("callout", "Permuting the input is the best single test",
   ["<b>The output of a geometric algorithm should not depend on the order "
    "in which the input was supplied</b> — up to a documented "
    "tie-breaking rule for genuine ties. A convex hull is a property of a "
    "point set, not of a list.",
    "<b>So shuffle the input and re-run.</b> If the answer changes, you "
    "have found either a degeneracy resolved inconsistently or a predicate "
    "that is not exact — and both are real bugs that will surface on "
    "real data.",
    "<b>It requires no ground truth, no reference implementation, and no "
    "expected output</b> — only two runs of your own code that must "
    "agree with each other. That makes it the cheapest useful test in the "
    "whole subject.",
    "<b>And it catches precisely the bugs that matter</b>, because an "
    "inconsistent predicate is order-sensitive almost by definition "
    "(Module 01 &sect;2): the same three points evaluated in different "
    "orders gave different answers, and a permuted input is exactly how "
    "that reaches the surface. <b>If you add one test to a geometry "
    "codebase, add this one.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Libraries"),
  ("table", ["Library", "What it covers", "Character"],
   [["<b>CGAL</b>",
     "<b>Essentially everything in this course</b>, and a great deal more.",
     "<b>Exact, correct, comprehensive, and heavy.</b> Deep template "
     "machinery and long compile times. <b>GPL or commercial licence</b>, "
     "which has decided a great many architectural choices in industry."],
    ["<b>Clipper2</b>", "2D boolean operations and polygon offsetting.",
     "<b>Integer coordinates, genuinely robust, small and readable.</b> "
     "Boost licence. The best demonstration of Module 06 &sect;4's integer "
     "strategy."],
    ["<b>Triangle</b> (Shewchuk)",
     "2D constrained Delaunay and quality meshing.",
     "<b>The reference implementation for Module 09 &sect;3.</b> Free for "
     "non-commercial use — check before shipping."],
    ["<b>earcut</b>", "Polygon triangulation with holes.",
     "<b>Tiny, fast, permissively licensed</b>, and readable in an "
     "afternoon. Used in map rendering at scale."],
    ["<b>qhull</b>",
     "Convex hulls, Delaunay, and Voronoi in arbitrary dimension.",
     "The lifting map of Module 08 &sect;3 applied. Mature and widely "
     "wrapped — it is what SciPy calls."],
    ["<b>libigl, Open3D, MeshLab</b>",
     "Mesh processing, repair, and analysis (Module 12 &sect;4).",
     "Research-oriented with good defaults. Excellent for pipelines and "
     "for one-off repair work."]],
   [0.17, 0.33, 0.50]),
  ("callout", "When to write it yourself",
   ["<b>When the problem is small and the dependency is not worth it.</b> "
    "A convex hull is twenty lines (Module 03 &sect;1); pulling in CGAL for "
    "it is not a sensible trade.",
    "<b>When you need a specific degeneracy policy the library does not "
    "offer.</b> The collinear-points decision of Module 03 &sect;1 is the "
    "clearest example — if you need every boundary point and the "
    "library returns only extreme ones, no amount of wrapping fixes it.",
    "<b>When the data layout matters.</b> If the library's point type "
    "forces a conversion inside a hot loop, the conversion can easily cost "
    "more than the algorithm (CSCE 735 Module 02).",
    "<b>And to understand it.</b> <b>Which is the point of this course</b> "
    "— you cannot evaluate a library's guarantees, read its kernel "
    "documentation, or diagnose its failure on your data without knowing "
    "what the guarantees could be and where they come from. <b>Writing it "
    "once is what makes using someone else's an informed decision rather "
    "than a hopeful one.</b>"]),

  ("h1", "4 &nbsp; Claiming honestly"),
  ("ul", ["<b>'Predicates are exact; constructions are rounded to "
          "<code>double</code>.'</b> Precise, honest, and it tells the "
          "caller exactly what they have — correct topology, "
          "approximate coordinates.",
          "<b>'Degeneracies are resolved by symbolic perturbation with "
          "index-based tie-breaking'</b> — which says that the output "
          "is a valid structure for an infinitesimally nearby input, and "
          "warns the caller who actually wanted to detect the degeneracy "
          "(Module 02 &sect;3).",
          "<b>'Output coordinates are snap-rounded to a grid of size g, "
          "and no point is displaced by more than d.'</b> A quantified "
          "promise rather than a vague one.",
          "<b>'Tested against exact rational arithmetic for n &le; 100, "
          "differentially against CGAL above that, and under permutation "
          "at every size.'</b> States the evidence, not the hope.",
          "<b>And what you cannot honestly say: 'it is robust'.</b> "
          "<b>'Robust' is the word in this field that means nothing</b>, "
          "and it is the one most frequently used. Say which inputs are "
          "handled, which guarantees hold, and which cases are known to "
          "fail — a documented limitation is engineering, and an "
          "undocumented one is a bug waiting for someone else to find."]),
  ("callout", "Where this leaves you",
   ["<b>You can implement the standard structures</b> — convex hulls, "
    "triangulations, planar subdivisions, Voronoi and Delaunay diagrams, "
    "spatial indices — <b>and for each one you know which predicate it "
    "rests on and which degeneracies attack it.</b>",
    "<b>And you know the thing most people working with geometry do "
    "not:</b> that geometric failures are overwhelmingly about arithmetic "
    "rather than about algorithms, that the distinction between a predicate "
    "and a construction determines what is possible, and that both are "
    "fixable by known means at known cost.",
    "<b>CSCE 629 supplied the complexity analysis. CSCE 641 and 645 "
    "supplied the representations. CSCE 649 assumed the collision geometry "
    "worked, and CSCE 647 assumed the acceleration structures did.</b>",
    "<b>This course built what those assumed.</b> And the two courses "
    "beside it in this semester build the rest of what an engine needs that "
    "the degree did not cover — <b>CSCE 605 the compiler that turns "
    "shaders and scripts into something the machine runs, and CSCE 678 the "
    "network that lets more than one person be in the world at once.</b>"]),
 ],
 "resources": [
   ("CGAL &mdash; kernel documentation and the robustness manual (free)",
    "https://doc.cgal.org/latest/Kernel_23/",
    "<b>The &sect;1 strategy table, as a working library's design.</b> The "
    "kernel-choice discussion is the best practical writing on this "
    "subject."),
   ("Kettner et al. &mdash; Classroom Examples of Robustness Problems "
    "(free)",
    "https://web.archive.org/web/20240420100137/https://people.mpi-inf.mpg.de/~mehlhorn/ftp/ClassroomExamples.pdf",
    "Worth re-reading now that you can fix everything in it."),
   ("Chen, Cheung, Xie, Zhang & Zhang &mdash; Metamorphic testing: a review "
    "(free)",
    "https://www.sciencedirect.com/science/article/pii/S0950584917300028",
    "The &sect;2 technique, generalised well beyond geometry."),
   ("Shewchuk &mdash; Lecture notes on geometric robustness (free)",
    "https://people.eecs.berkeley.edu/~jrs/",
    "The practitioner's summary, from the person who did most to make this "
    "tractable."),
 ],
 "exercises": [
   "Take each algorithm you built in this course and classify it as "
   "predicate-only or construction-involving.",
   "<b>Design an interface</b> that makes the predicate/construction "
   "distinction explicit, and implement two kernels behind it.",
   "Convert one construction-heavy algorithm to integer coordinates and "
   "measure the robustness difference.",
   "<b>Write property-based tests</b> for your hull, triangulation, and "
   "boolean implementations.",
   "<b>Add the permutation test</b> to every algorithm you have written. "
   "Report what it finds — it will find something.",
   "Add metamorphic tests for translation, rotation, and scaling.",
   "Build a differential test harness against CGAL and run it on your "
   "degenerate generator.",
   "Write the documentation paragraph for one of your routines, meeting "
   "&sect;4's standard.",
   "Find a geometry library's documentation that says 'robust' and "
   "determine what it actually guarantees.",
   "<b>Project 2 is now due.</b> Submit the implementation, the timing "
   "study across input distributions, the library comparison, the "
   "degeneracy statement, and the rendered figures.",
 ],
 "selfcheck": [
   "Give five situations and the robustness strategy each calls for.",
   "Why separate predicates from constructions in an interface?",
   "What is the cheapest useful guarantee, and why is it usually enough?",
   "Name six ways to test geometric code.",
   "Why is permuting the input the best single test?",
   "Name six libraries and what each covers.",
   "Give four reasons to write geometry yourself.",
   "Give four honest claims and one thing you cannot say.",
 ],
},

]
