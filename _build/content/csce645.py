# -*- coding: utf-8 -*-
"""CSCE 645 Geometric Modeling — original course content."""

COURSE = {
    "code": "CSCE 645",
    "title": "Geometric Modeling",
    "tagline": "Curves, surfaces, meshes, and the discrete differential "
               "geometry that makes them computable",
    "term": "Semester 2 (with CSCE 611 and CSCE 606)",
    "prereqs": "CSCE 641 Computer Graphics; linear algebra; multivariable "
               "calculus helpful but developed as needed",
    "effort": "10–12 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A mesh processing library: half-edge structure, "
                   "curvature, smoothing, parameterisation, simplification, "
                   "and remeshing — all written by you",
    "description": [
        "CSCE 641 treated geometry as something that arrives in a vertex "
        "buffer. This course is about where that geometry comes from, how it "
        "is represented, and what you can compute from it.",
        "The central difficulty is that classical differential geometry is "
        "about smooth surfaces, and computers hold triangle meshes. A "
        "triangle mesh has zero curvature on every face and infinite "
        "curvature on every edge, so the classical definitions do not "
        "transfer. <b>Discrete differential geometry</b> is the discipline of "
        "finding discrete definitions that preserve the theorems rather than "
        "the formulas — and it turns out that insisting on the theorems "
        "is what produces algorithms that work.",
        "The course runs from the representation question through curves and "
        "spline surfaces, into subdivision, and then into the discrete "
        "operators — curvature, the Laplacian — that drive almost "
        "every modern geometry processing algorithm. Smoothing, "
        "parameterisation, simplification, and deformation all turn out to be "
        "the same small set of linear systems wearing different clothes.",
        "Everything is implemented. By the end you will have written a mesh "
        "library you understand completely, which is a far better foundation "
        "for engine work than familiarity with someone else's.",
    ],
    "outcomes": [
        "Choose a shape representation from the operations a task requires.",
        "Implement a half-edge mesh and its traversal operations.",
        "Evaluate Bézier and B-spline curves and reason about continuity.",
        "Implement Catmull–Clark and Loop subdivision.",
        "Compute discrete curvature and explain why the discrete definitions "
        "are chosen as they are.",
        "Build and solve the cotangent Laplacian for smoothing, "
        "parameterisation, and deformation.",
        "Implement quadric-error simplification with attribute preservation.",
        "Explain implicit representations and convert between them and "
        "meshes.",
    ],
    "materials": [
        ("Keenan Crane — Discrete Differential Geometry (free notes, "
         "video, and code)",
         "https://brickisland.net/ddg-web/",
         "Primary source. Complete lecture videos, a full set of course "
         "notes, and C++/JavaScript skeleton code. The best free resource on "
         "this subject by a wide margin."),
        ("libigl tutorial (free, with code)",
         "https://libigl.github.io/tutorial/",
         "A working geometry processing library with a tutorial that doubles "
         "as a survey of the field. Read the source for every algorithm you "
         "implement."),
        ("Polygon Mesh Processing — course slides (free)",
         "https://www.pmp-book.org/",
         "Slides and the companion open-source library. Strong on "
         "simplification, remeshing, and parameterisation."),
        ("GAMES101 Lectures 11–12 — Geometry",
         "https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html",
         "The condensed version you met in CSCE 641. Useful as revision "
         "before Module 03."),
        ("MIT 6.8410 Shape Analysis — Justin Solomon",
         "https://groups.csail.mit.edu/gdpgroup/6838_spring_2021.html",
         "A graduate course covering the same operators from a more "
         "analytical direction. Good second voice for Modules 07–09."),
        ("Inigo Quilez — articles on distance functions (free)",
         "https://iquilezles.org/articles/",
         "The practical reference for implicit surfaces and SDFs, with "
         "derivations and working shader code. Primary source for Module 11."),
    ],
    "tooling": [
        "<b>C++17</b> with <b>Eigen</b> for linear algebra. You will be "
        "solving sparse linear systems from Module 08 onward and writing your "
        "own solver is not the point of this course.",
        "<b>libigl</b> as a reference implementation and for mesh I/O. Write "
        "your own algorithms; use libigl to check them.",
        "<b>Polyscope</b> for visualisation — a few lines to display a "
        "mesh with per-vertex scalar fields, which you will want constantly.",
        "<b>A test mesh collection</b>: a sphere and torus (known curvature), "
        "a cube (sharp features), a scanned model (noise and holes), and a "
        "deliberately broken mesh (non-manifold edges).",
        "<b>A portfolio repository</b> with a rendered image for every "
        "algorithm.",
    ],
    "projects": [
        {"title": "A mesh processing library", "after": 8,
         "brief": "Build the half-edge structure and the operators that "
                  "everything later depends on. This is infrastructure, and "
                  "the rest of the course assumes it works.",
         "reqs": [
             "Half-edge data structure built from an indexed mesh, with "
             "detection and reporting of non-manifold input rather than "
             "silent failure.",
             "All one-ring traversals: faces around a vertex, vertices around "
             "a vertex, edges of a face, the face across an edge.",
             "Vertex normals by both uniform and area-weighted averaging, "
             "with a comparison.",
             "Discrete Gaussian and mean curvature, validated against a "
             "sphere and a torus where the analytic answer is known.",
             "The cotangent Laplacian as a sparse matrix, with explicit "
             "handling of boundary vertices.",
             "Explicit and implicit Laplacian smoothing.",
         ],
         "done": [
             "Gaussian curvature integrated over a closed genus-0 mesh equals "
             "4π to within floating-point tolerance. Report the number.",
             "The same integral over a torus equals 0. Report it.",
             "A noisy scanned mesh smoothed with both explicit and implicit "
             "schemes, with the time step at which explicit smoothing becomes "
             "unstable reported.",
         ]},
        {"title": "Simplify, parameterise, remesh", "after": 12,
         "brief": "Take a scanned model through a complete processing "
                  "pipeline and produce something an engine could actually "
                  "load.",
         "reqs": [
             "Quadric-error simplification with UV and normal seams "
             "preserved, producing a clean LOD chain.",
             "Least-squares conformal parameterisation of a mesh cut into "
             "charts, with the distortion measured and reported.",
             "Isotropic remeshing to a target edge length.",
             "A normal map baked from the high-resolution mesh onto the "
             "simplified one.",
             "Everything rendered in your CSCE 641 renderer.",
         ],
         "done": [
             "An LOD chain at 100%, 25%, and 5% of the original triangle "
             "count, shown side by side at matched screen size.",
             "A UV atlas image with distortion visualised as a per-triangle "
             "colour.",
             "The simplified mesh with the baked normal map rendered beside "
             "the original, at a distance where they should be "
             "indistinguishable.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Representing Shape",
 "subtitle": "Four ways to describe a surface, and what each one makes easy.",
 "question": "What is the right data structure for a shape?",
 "outcomes": [
     "Distinguish parametric, implicit, explicit, and volumetric "
     "representations.",
     "Predict which operations are cheap and which are hard in each.",
     "Explain why conversion between representations is lossy.",
     "Choose a representation from the operations a task requires.",
     "State what a manifold is and why the condition matters.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Four representations",
   "blurb": "The choice determines which questions are easy to answer."},

  {"t": "table", "kicker": "Representations", "title": "The four families",
   "header": ["Kind", "Form", "Example"],
   "widths": [2.8, 4.8, 4.5],
   "rows": [
     ["Parametric", "A map from parameters to points", "Bézier patch, NURBS, sphere by (θ,φ)"],
     ["Implicit", "f(x) = 0 defines the surface", "Signed distance field, metaball"],
     ["Explicit / discrete", "An enumerated set of elements", "Triangle mesh, point cloud"],
     ["Volumetric", "A sampled scalar field", "Voxel grid, MRI data, level set"],
   ],
   "note": "Students arrive thinking 'mesh' is the only answer. The point of "
           "the module is that the representation is a design decision."},

  {"t": "two", "kicker": "The trade", "title": "Parametric and implicit",
   "lh": "Parametric — S(u,v)",
   "l": ["<b>Easy:</b> generate points on the surface.",
         "<b>Easy:</b> tessellate, texture, march along the surface.",
         "<b>Hard:</b> is this point inside?",
         "<b>Hard:</b> union, intersection, difference.",
         ("Good for rendering and modelling by hand.", 1)],
   "rh": "Implicit — f(x) = 0",
   "r": ["<b>Easy:</b> is this point inside? Check the sign.",
         "<b>Easy:</b> booleans — min and max of two fields.",
         "<b>Easy:</b> blending, offsetting, smoothing.",
         "<b>Hard:</b> generate a point <i>on</i> the surface.",
         ("Good for CSG, collision, and procedural shape.", 1)],
   "note": "The inside/outside asymmetry is the cleanest way to see why both "
           "exist. Neither is better; they answer different questions."},

  {"t": "callout", "title": "The representation decides the algorithm",
   "kind": "Key idea",
   "body": ["Nearly every question in this course is easy in one "
            "representation and awkward in another.",
            "<b>'Is this point inside?'</b> — one subtraction and a sign "
            "test for an implicit surface; a ray cast and a parity count for "
            "a mesh.",
            "<b>'Give me a point on the surface'</b> — evaluate S(u,v) "
            "for a parametric surface; root-find along a ray for an implicit "
            "one.",
            "So the practical skill is not mastering one representation. It "
            "is recognising which one makes your actual question trivial, and "
            "knowing what the conversion costs."]},

  {"t": "section", "label": "Part 2", "title": "Why meshes won",
   "blurb": "Not because they are the best representation — because "
            "hardware rasterises triangles."},

  {"t": "bullets", "kicker": "Meshes", "title": "What a triangle mesh is good at",
   "items": [
     "<b>Rasterisation.</b> Hardware consumes triangles. Everything else must "
     "be converted first.",
     "<b>Arbitrary topology.</b> Any shape, any genus, no patch layout "
     "required.",
     "<b>Local editing.</b> Move one vertex without re-solving anything.",
     "<b>Adaptive detail.</b> Small triangles where needed.",
     "",
     "<b>And what it is bad at:</b>",
     ("No exact smoothness — curvature is zero on faces and undefined "
      "on edges.", 1),
     ("Booleans are difficult and numerically fragile.", 1),
     ("Resolution is baked in. Refining requires inventing detail.", 1),
   ],
   "note": "Framing the mesh as a pragmatic compromise rather than the "
           "natural choice sets up Module 07's whole problem."},

  {"t": "table", "kicker": "Operations", "title": "Cost by representation",
   "header": ["Operation", "Parametric", "Implicit", "Mesh"],
   "widths": [4.0, 2.7, 2.7, 2.7],
   "rows": [
     ["Point on surface", "<b>Trivial</b>", "Root-find", "<b>Trivial</b>"],
     ["Inside test", "Hard", "<b>Trivial</b>", "Ray parity"],
     ["Boolean ops", "Very hard", "<b>Trivial</b>", "Fragile"],
     ["Render", "Tessellate", "Ray march", "<b>Native</b>"],
     ["Exact normals", "<b>Analytic</b>", "<b>∇f</b>", "Approximate"],
     ["Arbitrary topology", "Hard", "<b>Free</b>", "<b>Free</b>"],
     ["Local edit", "Patch-wide", "Hard", "<b>Trivial</b>"],
   ],
   "note": "Have them keep this table. It is the practical content of the "
           "module."},

  {"t": "section", "label": "Part 3", "title": "Manifolds",
   "blurb": "The condition that makes a mesh well-behaved."},

  {"t": "bullets", "kicker": "Manifold", "title": "What the condition requires",
   "items": [
     "A surface is <b>manifold</b> if every point has a neighbourhood that "
     "looks like a flat disc.",
     "",
     "For a mesh, two concrete conditions:",
     ("Every edge is shared by exactly <b>two</b> faces (or one, at a "
      "boundary).", 1),
     ("The faces around every vertex form a single closed fan — not two "
      "cones meeting at a point.", 1),
     "",
     "Why it matters: half-edge structures, normals, curvature, and the "
     "Laplacian all assume it.",
     "",
     "<b>Real scanned and authored meshes routinely violate it.</b>",
   ],
   "note": "Setting the expectation now that real data is broken saves a lot "
           "of frustration in Project 1."},

  {"t": "callout", "title": "Euler's formula, and what it is for",
   "kind": "The one invariant worth knowing",
   "body": ["For a closed manifold mesh: <b>V − E + F = 2 − 2g</b>, "
            "where g is the genus — the number of handles.",
            "A sphere has g = 0 and V − E + F = 2. A torus has g = 1 and "
            "V − E + F = 0.",
            "This is a <b>topological invariant</b>: no amount of bending, "
            "stretching, or refining changes it. Only cutting or gluing does.",
            "Practical use: it is a cheap integrity check. Compute it on any "
            "mesh you load, and if it disagrees with the expected genus, your "
            "mesh has holes, duplicate vertices, or non-manifold edges "
            "— and you have found out in one line rather than three "
            "modules later."]},

  {"t": "eq", "kicker": "Consequence", "title": "A useful corollary",
   "eqs": [
     ("closed triangle mesh:  3F  =  2E",
      "Every face has 3 edges; every edge is shared by 2 faces."),
     ("⇒  F ≈ 2V,   E ≈ 3V",
      "Substituting into Euler's formula. Memorise this ratio."),
     ("⇒  average vertex valence  ≈  6",
      "Which is why regular triangle meshes look like hexagonal packings."),
   ],
   "caption": "Valence 6 is the 'natural' degree for a triangle mesh. "
              "Remeshing algorithms (Module 10) explicitly target it.",
   "note": "The valence-6 result reappears in subdivision and remeshing. "
           "Worth deriving once properly."},

  {"t": "bullets", "kicker": "Practice", "title": "Choosing a representation",
   "items": [
     "<b>Rendering a character?</b> Mesh. The hardware demands it.",
     "<b>CAD with exact booleans?</b> Implicit or B-rep with NURBS.",
     "<b>Procedural terrain or clouds?</b> Implicit — evaluate anywhere, "
     "any resolution.",
     "<b>Medical or simulation data?</b> Volumetric — that is how it was "
     "acquired.",
     "<b>Smooth authored surfaces?</b> Subdivision, which is Module 06's "
     "answer and converts to mesh on demand.",
     "",
     "Production pipelines use several and convert between them. The "
     "conversions are where the information is lost.",
   ]},
 ],
 "takeaways": [
   "Four families: parametric, implicit, explicit, volumetric. The choice "
   "determines which questions are cheap.",
   "Parametric makes 'give me a point' trivial; implicit makes 'is this "
   "inside' trivial. Neither is better.",
   "Meshes won because hardware rasterises triangles, not because they are "
   "the best representation — they have no exact smoothness and fragile "
   "booleans.",
   "Manifold means every edge has exactly two faces and every vertex has one "
   "closed fan. Nearly every algorithm assumes it, and real data violates it.",
   "V − E + F = 2 − 2g is a topological invariant and a one-line "
   "integrity check on any mesh you load.",
   "For a closed triangle mesh, F ≈ 2V and average valence ≈ 6. "
   "Remeshing targets that number deliberately.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Four ways to describe a surface"),
  ("p", "Before any algorithm, a decision: how is the shape stored? The "
        "answer determines which questions are one line of code and which are "
        "a research project."),
  ("table", ["Family", "Definition", "Examples", "Natural operation"],
   [["<b>Parametric</b>", "A function from a parameter domain to space: "
     "S(u,v) &rarr; &#8477;&#179;.",
     "B&eacute;zier and NURBS patches; a sphere by latitude and longitude.",
     "Generate points on the surface."],
    ["<b>Implicit</b>", "The zero set of a function: {x : f(x) = 0}.",
     "Signed distance fields, metaballs, algebraic surfaces.",
     "Test whether a point is inside."],
    ["<b>Explicit / discrete</b>", "An enumerated collection of primitives.",
     "Triangle meshes, point clouds.",
     "Render; edit locally."],
    ["<b>Volumetric</b>", "A scalar field sampled on a grid.",
     "Voxel grids, CT and MRI data, level sets.",
     "Represent interiors and topology change."]],
   [0.18, 0.28, 0.30, 0.24]),
  ("h2", "1.1 &nbsp; The fundamental asymmetry"),
  ("callout", "Each representation makes one question trivial and another hard",
   ["<b>'Give me a point on the surface.'</b> Parametric: evaluate S(u,v). "
    "Trivial. Implicit: you must solve f(x) = 0, which means root-finding "
    "along a ray.",
    "<b>'Is this point inside?'</b> Implicit: evaluate f and check the sign. "
    "Trivial. Parametric or mesh: cast a ray and count crossings, with all "
    "the degenerate cases that implies.",
    "<b>'Union these two shapes.'</b> Implicit: min(f&#8321;, f&#8322;). One "
    "line. Mesh: compute every intersection curve, re-triangulate both "
    "surfaces along it, and resolve numerical near-misses — a genuinely "
    "difficult problem that commercial kernels still get wrong.",
    "The skill is not mastering one representation. It is recognising which "
    "makes your actual question trivial, and knowing what conversion costs."]),

  ("h1", "2 &nbsp; Why triangle meshes dominate"),
  ("p", "Meshes are not the most expressive or the most mathematically "
        "convenient representation. They dominate for an engineering reason: "
        "graphics hardware rasterises triangles, and everything else must be "
        "converted to triangles before it can be drawn."),
  ("table", ["Strength", "Weakness"],
   [["Native to the rendering hardware (CSCE 641).",
     "No exact smoothness: curvature is zero on every face and undefined on "
     "every edge. Module 07 is about repairing this."],
    ["Arbitrary topology at no cost — any genus, no patch layout.",
     "Boolean operations are difficult and numerically fragile."],
    ["Local editing: move one vertex, nothing else changes.",
     "Resolution is baked in. Refining requires inventing detail that is not "
     "in the data (Module 06)."],
    ["Adaptive: small triangles where detail is needed.",
     "No compact analytic description — storage grows with detail."]],
   [0.44, 0.56]),

  ("h1", "3 &nbsp; The operation cost table"),
  ("table", ["Operation", "Parametric", "Implicit", "Triangle mesh"],
   [["Evaluate a point on the surface", "<b>Trivial</b>",
     "Root-find along a ray", "<b>Trivial</b>"],
    ["Inside/outside test", "Hard", "<b>Sign of f</b>",
     "Ray cast, count crossings"],
    ["Boolean operations", "Very hard", "<b>min / max of fields</b>",
     "Fragile; a real engineering problem"],
    ["Render", "Tessellate first", "Ray march or extract a mesh",
     "<b>Native</b>"],
    ["Exact normal", "<b>Cross product of partials</b>",
     "<b>&nabla;f, normalised</b>", "Averaged from faces — approximate"],
    ["Arbitrary topology", "Awkward — needs trimming and patch layout",
     "<b>Free</b>", "<b>Free</b>"],
    ["Local edit", "Affects a whole patch", "Hard to localise",
     "<b>Move one vertex</b>"],
    ["Offset by a distance", "Hard", "<b>f(x) &minus; d</b>",
     "Self-intersects"]],
   [0.25, 0.25, 0.25, 0.25]),
  ("p", "Keep this table. Almost every design decision in a geometry pipeline "
        "is a row of it, and most pipeline complexity comes from needing "
        "operations that live in different columns."),

  ("break",),
  ("h1", "4 &nbsp; Manifolds"),
  ("p", "Most algorithms in this course assume the mesh is <b>manifold</b>. "
        "The condition sounds abstract and has a concrete combinatorial "
        "meaning."),
  ("p", "A surface is manifold if every point has a neighbourhood "
        "homeomorphic to a disc — locally, it looks flat. For a "
        "triangle mesh this reduces to two checkable conditions:"),
  ("ol", ["<b>Every edge is shared by exactly two faces</b> (or by one, if it "
          "is a boundary edge). An edge with three incident faces is a "
          "non-manifold edge.",
          "<b>The faces around every vertex form a single closed fan.</b> Two "
          "cones meeting at a single shared vertex is non-manifold, even "
          "though every edge is fine."]),
  ("callout", "Real meshes violate this constantly",
   ["Scanned data has holes, duplicated vertices, and self-intersections. "
    "Authored data has T-junctions, zero-area triangles, and geometry "
    "intentionally built from intersecting parts. Exported data has "
    "duplicated vertices wherever a UV or normal seam occurs.",
    "A library that assumes manifold input and gets none will fail somewhere "
    "deep in a traversal, often silently producing wrong results rather than "
    "crashing.",
    "<b>Validate on load and report the specific violation.</b> This is "
    "required in Project 1, and it is the difference between a library you "
    "can trust and one you cannot."]),
  ("h2", "4.1 &nbsp; Euler's formula"),
  ("eq", "V &minus; E + F = 2 &minus; 2g"),
  ("p", "for a closed, connected, manifold surface of genus g — where "
        "the genus counts handles. A sphere has g = 0 so the alternating sum "
        "is 2; a torus has g = 1 so it is 0; a two-handled surface gives "
        "&minus;2."),
  ("p", "This is a <b>topological invariant</b>. Bending, stretching, and "
        "subdividing the mesh leave it unchanged; only cutting or gluing "
        "alters it. That makes it an excellent and extremely cheap integrity "
        "check: compute V &minus; E + F on any mesh you load, and if it does "
        "not match the expected genus you have holes, duplicated vertices, or "
        "non-manifold elements — discovered immediately rather than "
        "three algorithms later."),
  ("h2", "4.2 &nbsp; A corollary worth memorising"),
  ("p", "In a closed triangle mesh every face has three edges and every edge "
        "is shared by two faces, so 3F = 2E. Substituting into Euler's "
        "formula and taking V large:"),
  ("eq", "F &asymp; 2V &nbsp;&nbsp;&nbsp; E &asymp; 3V &nbsp;&nbsp;&nbsp; average valence &asymp; 6"),
  ("callout", "Why valence 6 keeps reappearing",
   ["The average vertex of a closed triangle mesh has six neighbours, "
    "regardless of the shape. This is forced by topology, not by any choice "
    "of the modeller.",
    "It is why a well-made triangle mesh looks locally like a hexagonal "
    "packing, why remeshing algorithms (Module 10) explicitly drive vertex "
    "valence toward 6, and why vertices of other valence are called "
    "<b>irregular</b> or <b>extraordinary</b> — a term that returns in "
    "Module 06, where subdivision surfaces lose a degree of smoothness "
    "precisely at those points.",
    "The analogous number for quad meshes is 4, which is why quad modelling "
    "guidelines are so insistent about avoiding poles."]),

  ("h1", "5 &nbsp; Choosing"),
  ("table", ["Task", "Representation", "Why"],
   [["Rendering a character or environment", "Triangle mesh",
     "The hardware requires it, and everything converts to it eventually."],
    ["CAD with exact booleans and offsets", "NURBS B-rep, or implicit",
     "Exactness and well-defined set operations matter more than rendering "
     "speed."],
    ["Procedural terrain, clouds, or effects", "Implicit",
     "Evaluate anywhere at any resolution; no storage proportional to detail."],
    ["Medical imaging, simulation output", "Volumetric",
     "It is how the data was acquired, and interiors matter."],
    ["Smooth authored organic surfaces", "Subdivision (Module 06)",
     "A coarse editable cage with a smooth limit surface, converting to mesh "
     "on demand."],
    ["Collision detection", "Implicit or BVH over a mesh",
     "Distance queries are what implicits are for."]],
   [0.28, 0.24, 0.48]),
  ("p", "Production pipelines use several representations and convert between "
        "them. The conversions are where information is lost and where most "
        "pipeline bugs live: a NURBS surface tessellated to a mesh has lost "
        "its exact parameterisation; a mesh converted to a distance field has "
        "lost its sharp edges unless they were specially handled. Knowing "
        "what each conversion discards is a large part of working with "
        "geometry professionally."),
 ],
 "resources": [
   ("Keenan Crane — DDG, Lecture 1 (Overview) and the Combinatorial "
    "Surfaces lecture",
    "https://brickisland.net/ddg-web/",
    "Representations, manifoldness, and Euler characteristic, with the "
    "topology done carefully."),
   ("libigl tutorial — Chapter 1 (Mesh representation)",
    "https://libigl.github.io/tutorial/",
    "How a real library stores meshes, and why it uses flat index matrices "
    "rather than pointer structures."),
   ("Inigo Quilez — 'Distance functions'",
    "https://iquilezles.org/articles/distfunctions/",
    "The implicit side, with working code. Read it now for contrast; it "
    "becomes the primary source in Module 11."),
   ("Polygon Mesh Processing slides — Chapter 1",
    "https://www.pmp-book.org/",
    "Representations compared with the operation-cost framing used here."),
 ],
 "exercises": [
   "Load several meshes and compute V, E, F, and the Euler characteristic for "
   "each. Verify a sphere gives 2 and a torus gives 0. Find or construct a "
   "mesh where it gives something unexpected and diagnose why.",
   "Write a validator that detects non-manifold edges (three or more incident "
   "faces), non-manifold vertices (more than one face fan), isolated "
   "vertices, and duplicate vertices. Run it on a scanned model and report "
   "what you find.",
   "Compute the average vertex valence for five different triangle meshes and "
   "confirm it approaches 6. Explain any deviation in terms of boundary "
   "vertices.",
   "Implement a sphere three ways: parametric by (&theta;, &phi;), implicit "
   "as |x|&minus;r, and as a triangle mesh. For each, write the code to "
   "answer 'is this point inside?' and 'give me a point on the surface'. "
   "Compare the effort.",
   "Implement the union of two spheres implicitly with min(f&#8321;, "
   "f&#8322;), and then attempt the same operation on two sphere meshes. Do "
   "not finish the mesh version — the point is to discover how much work "
   "it is.",
   "Take a NURBS or analytic surface, tessellate it at two resolutions, and "
   "describe precisely what information the conversion discarded.",
 ],
 "selfcheck": [
   "Name the four representation families and the operation each makes "
   "trivial.",
   "Why are boolean operations trivial for implicit surfaces and hard for "
   "meshes?",
   "Give the real reason triangle meshes dominate graphics, and two things "
   "they are genuinely bad at.",
   "State the two combinatorial conditions for a triangle mesh to be "
   "manifold.",
   "What is Euler's formula, why is it invariant, and what practical use does "
   "it have?",
   "Derive average valence &asymp; 6 for a closed triangle mesh, and say why "
   "the number matters later.",
 ],
},

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Meshes and Connectivity",
 "subtitle": "The data structure every later algorithm is built on.",
 "question": "How do you answer 'what is next to this?' in constant time?",
 "outcomes": [
     "Implement a half-edge structure from an indexed mesh.",
     "Write all the one-ring traversals.",
     "Handle boundaries correctly rather than by accident.",
     "Implement the basic topological operations: split, collapse, flip.",
     "Compute vertex normals and explain the weighting choice.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why indexed meshes are not enough",
   "blurb": "They store geometry. They do not store neighbourhood."},

  {"t": "bullets", "kicker": "The gap", "title": "What an indexed mesh cannot answer",
   "items": [
     "An indexed mesh is a vertex array and a triangle index array. Perfect "
     "for rendering.",
     "",
     "But: <b>which faces touch this vertex?</b>",
     ("Scan every face. O(F). Unusable inside a loop over vertices.", 1),
     "",
     "<b>Which face is across this edge?</b> <b>What are my neighbouring "
     "vertices, in order?</b>",
     ("Both require a full scan, or an auxiliary structure.", 1),
     "",
     "Every algorithm from Module 07 onward asks these questions per vertex, "
     "repeatedly.",
   ],
   "note": "Framing the half-edge as 'the structure that answers the "
           "questions the renderer never asks' makes it feel earned."},

  {"t": "code", "kicker": "Half-edge", "title": "The structure",
   "lang": "cpp", "code": """
struct HalfEdge {
    int next;      // next half-edge around the same face
    int twin;      // the opposite half-edge (-1 if boundary)
    int vertex;    // vertex this half-edge POINTS TO
    int face;      // face to the left (-1 if boundary)
};

struct Vertex { int halfedge; vec3 position; };  // any outgoing he
struct Face   { int halfedge; };                 // any he of this face
struct Edge   { int halfedge; };                 // one of the two

// Every edge becomes TWO directed half-edges, one per adjacent face.
// Four integers per half-edge, and every adjacency query becomes a walk.
""",
   "caption": "The invariant that makes everything work: "
              "<code>twin(twin(h)) == h</code> and following "
              "<code>next</code> cycles around a face.",
   "note": "Have them write the invariant checks as assertions. It catches "
           "construction bugs immediately."},

  {"t": "code", "kicker": "Traversal", "title": "The one-ring, which you will write once and use forever",
   "lang": "cpp", "code": """
// All faces around a vertex v.
// Pattern: twin then next, repeatedly, until you return to the start.
int h0 = vertex[v].halfedge, h = h0;
do {
    visit_face(he[h].face);
    h = he[he[h].twin].next;     // <- the move
} while (h != h0);

// All vertices of a face f: just follow next.
int h0 = face[f].halfedge, h = h0;
do { visit_vertex(he[h].vertex); h = he[h].next; } while (h != h0);

// The face across an edge: he[he[h].twin].face
""",
   "caption": "<code>twin</code> then <code>next</code> is the move that "
              "walks around a vertex. Writing it once correctly is most of "
              "the work in Project 1.",
   "note": "The twin-then-next idiom is worth drawing on a whiteboard. It is "
           "not obvious and it is used constantly."},

  {"t": "section", "label": "Part 2", "title": "Boundaries",
   "blurb": "The case that breaks naive implementations."},

  {"t": "callout", "title": "Two ways to handle boundaries",
   "kind": "Design decision",
   "body": ["<b>Option A: null twins.</b> A boundary half-edge has "
            "<code>twin = -1</code>. Simple to construct, and every traversal "
            "must now check for &minus;1 — which is exactly the check "
            "people forget.",
            "<b>Option B: a virtual boundary face.</b> Create one "
            "'imaginary' face per boundary loop, with real half-edges. Every "
            "half-edge then has a valid twin and the traversal code has no "
            "special cases.",
            "Option B costs a little construction complexity and removes an "
            "entire class of bugs. Most serious libraries use it, and this "
            "course recommends it.",
            "Either way, <b>decide deliberately</b>. Most mesh-library bugs "
            "are boundary bugs."]},

  {"t": "section", "label": "Part 3", "title": "Topological operations",
   "blurb": "Three local edits that everything later is built from."},

  {"t": "table", "kicker": "Operations", "title": "The three local edits",
   "header": ["Operation", "Does", "Used by"],
   "widths": [2.8, 4.8, 4.5],
   "rows": [
     ["Edge split", "Insert a vertex at an edge midpoint", "Subdivision, remeshing"],
     ["Edge collapse", "Merge an edge's two endpoints", "Simplification (Mod 10)"],
     ["Edge flip", "Rotate an edge within its two triangles", "Remeshing, Delaunay"],
   ],
   "note": "Everything in Modules 06 and 10 is a scheduled sequence of these "
           "three operations."},

  {"t": "callout", "title": "Edge collapse is the one with preconditions",
   "kind": "Where meshes break",
   "body": ["Collapsing an edge can silently create a non-manifold mesh, and "
            "the standard guard is the <b>link condition</b>.",
            "<b>Link condition:</b> the collapse is safe only if the vertices "
            "adjacent to <i>both</i> endpoints are exactly the two vertices "
            "opposite the edge.",
            "Violating it fuses parts of the surface that were not adjacent, "
            "producing a non-manifold vertex or a degenerate face. The result "
            "usually looks fine until some later algorithm fails confusingly.",
            "Also check: the collapse must not flip any adjacent face normal. "
            "Module 10 needs both tests."]},

  {"t": "section", "label": "Part 4", "title": "Normals",
   "blurb": "The first thing you compute, and the weighting matters."},

  {"t": "code", "kicker": "Normals", "title": "Three weightings",
   "lang": "cpp", "code": """
// Face normal: unambiguous.
vec3 fn = normalize(cross(p1 - p0, p2 - p0));

// Vertex normal: an average over incident faces. But weighted how?

// 1. UNIFORM -- simple, and biased toward whichever side has
//    more triangles, regardless of their size.
n = normalize(sum over faces of fn);

// 2. AREA-WEIGHTED -- a large triangle should count for more.
n = normalize(sum of area(f) * fn(f));

// 3. ANGLE-WEIGHTED -- weight by the face's angle AT THIS VERTEX.
//    Independent of tessellation: subdividing a face does not
//    change the result. Usually the right choice.
n = normalize(sum of theta_v(f) * fn(f));
""",
   "caption": "Angle weighting is tessellation-independent, which is the "
              "property you actually want — a normal should not change "
              "when you subdivide a neighbouring face.",
   "note": "Most engines use area weighting because it is cheaper. Angle "
           "weighting is better and worth knowing the argument for."},

  {"t": "bullets", "kicker": "Practice", "title": "Normals in a real pipeline",
   "items": [
     "<b>Smooth shading</b> needs one normal per vertex — average over "
     "all incident faces.",
     "<b>Sharp edges</b> need the vertex <b>split</b>: two copies with "
     "different normals.",
     ("Which is why exported meshes have more vertices than the half-edge "
      "structure does.", 1),
     "",
     "<b>Crease angle</b> thresholds decide automatically: split where the "
     "dihedral angle exceeds a threshold.",
     "",
     "Consequence for this course: the render mesh and the processing mesh "
     "are <b>different</b>. Process on the welded manifold; split for "
     "rendering.",
   ],
   "footnote": "This is why loading an OBJ and processing it directly usually "
               "fails — UV seams have already split the vertices."},

  {"t": "callout", "title": "Why your scanned mesh will not load",
   "kind": "Expect this",
   "body": ["<b>Duplicate vertices</b> at the same position, from seams or "
            "sloppy export. Weld with a spatial hash before building "
            "connectivity.",
            "<b>Non-manifold edges</b> where three faces meet. Detect and "
            "either cut or reject.",
            "<b>Inconsistent winding</b>, so face normals point in random "
            "directions. Propagate a consistent orientation by breadth-first "
            "traversal across shared edges.",
            "<b>Zero-area triangles</b> that make normals NaN. Remove them "
            "before anything else.",
            "Write all four repairs in Project 1. You will use them in every "
            "remaining module."]},
 ],
 "takeaways": [
   "An indexed mesh stores geometry but not neighbourhood. Every algorithm "
   "after Module 06 needs neighbourhood.",
   "A half-edge stores next, twin, vertex, and face. <code>twin</code> then "
   "<code>next</code> is the move that walks around a vertex.",
   "Handle boundaries with virtual boundary faces rather than null twins, and "
   "remove an entire class of bugs.",
   "Split, collapse, and flip are the three local edits. Everything in "
   "subdivision and simplification is a schedule of them.",
   "Edge collapse needs the link condition and a normal-flip test, or it "
   "silently produces non-manifold geometry.",
   "Angle-weighted vertex normals are tessellation-independent; the render "
   "mesh and the processing mesh are different objects.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What an indexed mesh cannot do"),
  ("p", "The rendering representation — a vertex array plus a triangle "
        "index array — is exactly right for the GPU and useless for "
        "geometry processing. It records <i>which vertices form each "
        "face</i> and nothing about neighbourhood."),
  ("table", ["Question", "Cost with an indexed mesh"],
   [["Which faces are incident to vertex v?",
     "Scan all F faces. O(F) per query, O(VF) for a loop over all vertices."],
    ["Which face lies across edge (a,b)?",
     "Scan, or build a hash from edges to faces."],
    ["What are v's neighbours, in rotational order?",
     "Scan, then sort — and the ordering is exactly what curvature and "
     "the Laplacian need."],
    ["Is this mesh manifold?", "Not directly answerable."]],
   [0.42, 0.58]),
  ("p", "From Module 07 onward, every algorithm iterates over vertices and "
        "asks for the one-ring neighbourhood of each. An O(F) query inside "
        "that loop is not viable, so a connectivity structure is required."),

  ("h1", "2 &nbsp; The half-edge structure"),
  ("p", "Represent each undirected edge as two directed <b>half-edges</b> "
        "pointing in opposite directions, one belonging to each adjacent "
        "face. Four references per half-edge suffice:"),
  ("code", """struct HalfEdge {
    int next;     // next half-edge around the same face
    int twin;     // the oppositely-directed half-edge of the same edge
    int vertex;   // the vertex this half-edge points TO
    int face;     // the face on its left
};

struct Vertex { int halfedge; vec3 position; };  // one outgoing half-edge
struct Face   { int halfedge; };                 // one half-edge of the face"""),
  ("p", "The invariants worth asserting during construction: "
        "<code>twin(twin(h)) == h</code>; following <code>next</code> from "
        "any half-edge returns to it after exactly the face's degree of "
        "steps; and <code>face(next(h)) == face(h)</code>. Checking these "
        "once at build time catches essentially every construction bug."),
  ("h2", "2.1 &nbsp; The traversals"),
  ("code", """// Faces around vertex v -- the one-ring.
int h0 = vertex[v].halfedge, h = h0;
do {
    visit(he[h].face);
    h = he[he[h].twin].next;        // twin, then next
} while (h != h0);

// Vertices of face f.
int h0 = face[f].halfedge, h = h0;
do { visit(he[h].vertex); h = he[h].next; } while (h != h0);

// The face across an edge.
int opposite = he[he[h].twin].face;"""),
  ("callout", "twin then next",
   ["This is the move that rotates around a vertex, and it is not obvious "
    "until you draw it. Starting from an outgoing half-edge, "
    "<code>twin</code> gives you the incoming half-edge of the neighbouring "
    "face, and <code>next</code> then gives you the next outgoing half-edge "
    "around the same vertex.",
    "Write it once, test it on a mesh where you know the answer, and never "
    "think about it again. Getting it wrong produces traversals that "
    "terminate but visit the wrong set — which is far harder to debug "
    "than an infinite loop."]),
  ("p", "With these, every adjacency query costs time proportional to the "
        "size of the answer, which is optimal."),

  ("h1", "3 &nbsp; Boundaries"),
  ("p", "A boundary edge has only one adjacent face, so one of its two "
        "half-edges has no face. There are two ways to represent this, and "
        "the choice has consequences."),
  ("table", ["Approach", "How", "Consequence"],
   [["<b>Null twins</b>", "A boundary half-edge has <code>twin = -1</code> "
     "and no second half-edge exists.",
     "Simple construction. <i>Every</i> traversal must test for &minus;1, and "
     "the one you forget is the bug you ship."],
    ["<b>Virtual boundary faces</b>",
     "Create one imaginary face per boundary loop, with genuine half-edges "
     "forming a cycle around the hole.",
     "Slightly more complex construction; every half-edge has a valid twin, "
     "so traversal code has no special cases. Boundary detection becomes "
     "<code>face &lt; 0</code> or a flag."]],
   [0.20, 0.38, 0.42]),
  ("callout", "Choose virtual boundary faces",
   ["The overwhelming majority of bugs in hand-written mesh libraries are "
    "boundary bugs, and most of them are a missing &minus;1 check in a "
    "traversal written weeks after the structure.",
    "Virtual boundary faces move the complexity into construction, where it "
    "is written once and tested once, instead of distributing it across every "
    "algorithm you will ever write.",
    "Whichever you choose, choose it deliberately and document it. Mixing the "
    "two conventions in one codebase is worse than either."]),

  ("break",),
  ("h1", "4 &nbsp; Topological operations"),
  ("p", "Three local edits generate essentially all of mesh processing."),
  ("table", ["Operation", "Effect", "Used in"],
   [["<b>Edge split</b>", "Insert a new vertex on an edge, splitting both "
     "adjacent triangles in two. Net: +1 vertex, +3 edges, +2 faces.",
     "Subdivision (Module 06), remeshing (Module 10)."],
    ["<b>Edge collapse</b>", "Merge the two endpoints into one, removing the "
     "edge and its two adjacent triangles. Net: &minus;1 vertex, &minus;3 "
     "edges, &minus;2 faces.",
     "Simplification (Module 10), LOD generation."],
    ["<b>Edge flip</b>", "Rotate an edge to connect the two opposite "
     "vertices of its adjacent triangles instead. Counts unchanged.",
     "Remeshing, Delaunay-ising, valence optimisation."]],
   [0.17, 0.46, 0.37]),
  ("h2", "4.1 &nbsp; The preconditions on edge collapse"),
  ("callout", "The link condition",
   ["Collapsing an edge (a, b) is topologically safe only when the "
    "intersection of a's one-ring neighbours and b's one-ring neighbours "
    "consists of exactly the two vertices opposite the edge.",
    "If they share a third neighbour, collapsing fuses two parts of the "
    "surface that were not adjacent, producing a non-manifold vertex or a "
    "degenerate face. The mesh often still renders, and fails much later in "
    "something unrelated.",
    "This is the standard guard and it is cheap: intersect two small sets."]),
  ("p", "A second precondition is geometric rather than topological: the "
        "collapse must not <b>flip</b> any adjacent face. Compute each "
        "affected face's normal before and after the proposed collapse and "
        "reject if any dot product goes negative. Without this check, "
        "simplification produces meshes with inverted triangles that shade "
        "black and self-intersect."),
  ("p", "Edge flips need a precondition too: the flip must not create a "
        "duplicate edge, which happens when the two opposite vertices are "
        "already connected."),

  ("h1", "5 &nbsp; Normals"),
  ("p", "A face normal is unambiguous: the normalised cross product of two "
        "edge vectors, with the sign determined by winding order (CSCE 641 "
        "Module 02). A <b>vertex</b> normal is an average over incident "
        "faces, and the weighting is a real choice."),
  ("table", ["Weighting", "Formula", "Behaviour"],
   [["Uniform", "&Sigma; n&#7523;",
     "Simple. Biased toward whichever side happens to have more triangles, "
     "regardless of their size — so it changes when you tessellate."],
    ["Area-weighted", "&Sigma; A&#7523; n&#7523;",
     "A large face contributes more. Better, and still tessellation-"
     "dependent: splitting one face into two does not change the total area "
     "but does change the sum if done unevenly."],
    ["Angle-weighted", "&Sigma; &theta;&#7523; n&#7523;",
     "Weight each face by its interior angle <i>at this vertex</i>. The "
     "angles around a vertex always sum to the same total regardless of how "
     "the faces are subdivided, so the result is <b>tessellation-"
     "independent</b>. Usually the right choice."]],
   [0.20, 0.18, 0.62]),
  ("p", "Tessellation independence is the property you actually want: "
        "subdividing a neighbouring face should not change a vertex's normal, "
        "because the surface did not change. Many engines use area weighting "
        "because it is marginally cheaper; angle weighting is better and the "
        "cost difference is negligible outside inner loops."),
  ("h2", "5.1 &nbsp; Render meshes and processing meshes are different"),
  ("callout", "This causes more confusion than any other practical issue",
   ["Smooth shading needs one normal per vertex. <b>Sharp</b> edges need the "
    "vertex duplicated, with each copy carrying a different normal — "
    "and the same applies at UV seams and material boundaries.",
    "So a mesh exported for rendering has <i>more vertices</i> than the "
    "underlying surface has, and those duplicates are not connected in the "
    "connectivity structure. Loading such a file and building a half-edge "
    "mesh directly yields a surface full of cracks, with wrong curvature "
    "everywhere near a seam.",
    "<b>Weld first.</b> Merge vertices by position (with a spatial hash and a "
    "tolerance), build connectivity on the welded manifold, process, and "
    "split again on export. Treating the render mesh and the processing mesh "
    "as separate objects is not pedantry — it is the only way this "
    "works."]),

  ("h1", "6 &nbsp; What real meshes will do to you"),
  ("table", ["Problem", "Symptom", "Repair"],
   [["Duplicate vertices", "Cracks; traversals that terminate early; wrong "
     "Euler characteristic.",
     "Weld by position with a spatial hash and an epsilon. Do this first, "
     "always."],
    ["Non-manifold edges", "Half-edge construction fails or produces a "
     "corrupt twin mapping.",
     "Detect edges with more than two incident faces. Either cut the surface "
     "along them or reject the mesh with a clear message."],
    ["Inconsistent winding", "Face normals point in random directions; "
     "lighting is patchy.",
     "Breadth-first traversal across shared edges, flipping faces to agree "
     "with their neighbour. Works on any orientable surface."],
    ["Zero-area triangles", "NaN normals that propagate everywhere.",
     "Remove degenerate faces before building connectivity. Check for NaN "
     "after every normal computation while developing."],
    ["Isolated vertices", "Euler characteristic wrong; vertices with no "
     "half-edge.", "Remove, or at least detect and report."]],
   [0.20, 0.38, 0.42]),
  ("p", "All five repairs are required in Project 1 because every subsequent "
        "module assumes clean input. Building them once, with tests, is the "
        "difference between a library you can rely on and one that fails "
        "mysteriously in Module 09."),
 ],
 "resources": [
   ("Keenan Crane — DDG, Combinatorial Surfaces and the half-edge "
    "lecture",
    "https://brickisland.net/ddg-web/",
    "The structure, the invariants, and the traversals, with the topology "
    "made precise."),
   ("libigl tutorial — adjacency and traversal",
    "https://libigl.github.io/tutorial/",
    "How a production library does this with flat index arrays rather than a "
    "pointer structure, and why."),
   ("OpenMesh documentation",
    "https://www.graphics.rwth-aachen.de/software/openmesh/",
    "A mature half-edge implementation. Read the handle and circulator design "
    "before writing your own API."),
   ("Max Wardetzky et al. — 'Discrete Laplace operators: no free lunch' "
    "(free)",
    "https://www.cs.columbia.edu/~keenan/Projects/Other/NoFreeLunch.pdf",
    "Not needed until Module 08, but the normal-weighting discussion here is "
    "the same kind of argument — worth seeing early."),
 ],
 "exercises": [
   "Implement a half-edge structure built from an indexed triangle mesh. "
   "Assert all three invariants after construction and verify on a cube, a "
   "sphere, and a mesh with boundary.",
   "Implement virtual boundary faces. Verify that a disc-topology mesh has "
   "exactly one boundary loop and that every half-edge has a valid twin.",
   "Write the one-ring traversal and verify it visits the correct number of "
   "faces for every vertex of a known mesh. Then verify the average count is "
   "about 6.",
   "Implement edge split, edge collapse, and edge flip, each with their "
   "preconditions. Write a test that performs a thousand random legal "
   "operations and re-validates the mesh afterwards.",
   "Deliberately perform a collapse that violates the link condition. "
   "Visualise the resulting non-manifold vertex and describe how you would "
   "detect it after the fact.",
   "Implement all three vertex normal weightings. Construct a mesh where "
   "uniform and angle weighting differ visibly, render all three, and explain "
   "which is correct and why.",
   "Write the five mesh repairs from &sect;6 and run them on a downloaded "
   "scanned model. Report what each one found.",
 ],
 "selfcheck": [
   "What question can an indexed mesh not answer efficiently, and why does it "
   "matter from Module 07 onward?",
   "List the four fields of a half-edge and state two invariants.",
   "What does the sequence twin-then-next accomplish?",
   "Give both boundary representations and say which this course recommends, "
   "with a reason.",
   "State the link condition and say what goes wrong without it.",
   "Why is angle weighting preferable to area weighting for vertex normals?",
   "Why must a mesh loaded from an OBJ file usually be welded before "
   "processing?",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Curves: Bézier and Continuity",
 "subtitle": "The one-dimensional case, where every idea is visible.",
 "question": "How do you define a smooth curve from a handful of points?",
 "outcomes": [
     "Evaluate Bézier curves by Bernstein basis and by de Casteljau.",
     "State and use the convex hull, affine invariance, and variation "
     "diminishing properties.",
     "Subdivide a curve and use it for adaptive tessellation.",
     "Distinguish parametric from geometric continuity and know which "
     "matters when.",
     "Explain why high-degree Bézier curves are impractical.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Definition",
   "blurb": "A weighted average of control points, with the weights chosen "
            "carefully."},

  {"t": "eq", "kicker": "Bézier", "title": "The Bernstein form",
   "eqs": [
     ("B(t)  =  Σᵢ  C(n,i) tⁱ (1−t)ⁿ⁻ⁱ Pᵢ,   t ∈ [0,1]",
      "The weights are the Bernstein polynomials of degree n."),
     ("Σᵢ C(n,i) tⁱ(1−t)ⁿ⁻ⁱ  =  1",
      "They sum to 1 for every t — the binomial theorem."),
     ("and each is ≥ 0 on [0,1]",
      "So B(t) is a <b>convex combination</b> of the control points."),
   ],
   "caption": "Non-negative weights summing to one is the entire source of "
              "the curve's good behaviour. Everything in Part 2 follows from "
              "those two facts.",
   "note": "Emphasise that the properties are consequences, not separate "
           "facts to memorise."},

  {"t": "code", "kicker": "de Casteljau", "title": "Evaluation by repeated interpolation",
   "lang": "cpp", "code": """
vec3 de_casteljau(vector<vec3> P, float t) {
    // Repeatedly lerp between adjacent points until one remains.
    while (P.size() > 1) {
        for (int i = 0; i + 1 < P.size(); i++)
            P[i] = lerp(P[i], P[i+1], t);
        P.pop_back();
    }
    return P[0];
}
// O(n^2), numerically stable, geometrically transparent --
// and it produces the subdivision for free (Part 3).
""",
   "caption": "Slower than evaluating the polynomial directly, and far better "
              "behaved. Direct evaluation of high-degree Bernstein "
              "polynomials loses precision badly.",
   "note": "The stability argument matters: the Bernstein coefficients are "
           "large and alternate in effect, so direct summation cancels."},

  {"t": "section", "label": "Part 2", "title": "Properties",
   "blurb": "Why Bézier curves are well behaved, derived rather than "
            "listed."},

  {"t": "table", "kicker": "Properties", "title": "What follows from convex combination",
   "header": ["Property", "Statement", "Why it is useful"],
   "widths": [3.0, 4.4, 4.7],
   "rows": [
     ["Endpoint interpolation", "B(0) = P₀, B(1) = Pₙ", "Joining segments is easy"],
     ["Convex hull", "The curve lies in the hull of the control points", "Conservative culling and bounds"],
     ["Affine invariance", "Transform the points, not the curve", "Transform n points, not 1000 samples"],
     ["Variation diminishing", "No line crosses the curve more often than the control polygon", "The curve does not wiggle more than you drew"],
     ["Tangents at ends", "B'(0) ∝ P₁−P₀", "Direct control of join smoothness"],
   ],
   "note": "Affine invariance is the one with the biggest practical payoff "
           "and the one students notice least."},

  {"t": "callout", "title": "Affine invariance is why curves are cheap to transform",
   "kind": "Practical consequence",
   "body": ["To transform a Bézier curve, transform its control points "
            "and re-evaluate. The result is exactly the transformed curve.",
            "So moving a curve costs <i>n</i> matrix multiplies, not one per "
            "sampled point. For a cubic that is four, regardless of how "
            "finely you later tessellate.",
            "This holds for affine transforms. It does <b>not</b> hold for "
            "perspective projection, which is why rational curves — "
            "NURBS, Module 04 — exist: adding weights makes the "
            "representation projectively invariant too."]},

  {"t": "section", "label": "Part 3", "title": "Subdivision",
   "blurb": "de Casteljau gives you the split for free."},

  {"t": "bullets", "kicker": "Subdivision", "title": "Splitting a curve at t",
   "items": [
     "Run de Casteljau at parameter t and keep the <b>intermediate</b> "
     "points, not just the final one.",
     "",
     "The first point of each level, in order, is the control polygon of the "
     "left half.",
     "The last point of each level, in reverse, is the control polygon of the "
     "right half.",
     "",
     "Both halves are exact Bézier curves of the same degree.",
     "",
     "<b>Use:</b> adaptive tessellation. Subdivide until the control polygon "
     "is flat enough, then draw it as a line.",
   ],
   "note": "This is the standard way curves are rendered, and it is the "
           "cleanest motivation for de Casteljau over direct evaluation."},

  {"t": "code", "kicker": "Tessellation", "title": "Adaptive flatness subdivision",
   "lang": "cpp", "code": """
void tessellate(Bezier c, float tol, vector<vec3>& out) {
    if (flat_enough(c, tol)) {           // control polygon close to a line?
        out.push_back(c.P[3]);
        return;
    }
    auto [left, right] = subdivide(c, 0.5f);
    tessellate(left,  tol, out);
    tessellate(right, tol, out);
}

// flat_enough: max distance from interior control points to the
// chord P0-P3. By the convex hull property, this BOUNDS the
// curve's deviation -- so the test is conservative and correct.
""",
   "caption": "The convex hull property is what makes the flatness test "
              "valid: it bounds the curve by its control polygon, so a flat "
              "polygon guarantees a flat curve.",
   "note": "Connecting the hull property to the correctness of the test is "
           "the satisfying part. The property is not decoration."},

  {"t": "section", "label": "Part 4", "title": "Continuity",
   "blurb": "Two notions, and they are not the same."},

  {"t": "table", "kicker": "Continuity", "title": "Parametric and geometric",
   "header": ["", "Cⁿ — parametric", "Gⁿ — geometric"],
   "widths": [2.4, 4.8, 4.9],
   "rows": [
     ["Requires", "Derivatives match as functions of t", "Derivative <i>directions</i> match"],
     ["C¹ vs G¹", "Same tangent vector", "Same tangent direction, any magnitude"],
     ["Governs", "Speed along the curve", "Apparent shape"],
     ["Matters for", "Animation, camera paths, tool paths", "Visual smoothness, silhouettes"],
     ["C² / G²", "Acceleration", "Curvature — visible in reflections"],
   ],
   "note": "C^n implies G^n but not conversely. The distinction is practical, "
           "not pedantic: a G1 camera path jolts."},

  {"t": "callout", "title": "Which one you need depends on what moves",
   "kind": "The practical rule",
   "body": ["<b>If something travels along the curve at a parameter-driven "
            "rate</b> — a camera, an animated object, a CNC tool "
            "— you need <b>C¹</b>. A G¹ join looks perfectly "
            "smooth and produces a visible jolt in speed.",
            "<b>If the curve is only a shape</b> — a silhouette, a "
            "profile, a font outline — <b>G¹</b> suffices and gives "
            "the designer more freedom.",
            "<b>If the surface will be shiny</b>, you need <b>G²</b>. "
            "Curvature discontinuities are invisible in silhouette and "
            "glaringly obvious in a reflection, which is why car body "
            "surfacing is specified in terms of G²."]},

  {"t": "bullets", "kicker": "Limits", "title": "Why high-degree Bézier curves fail",
   "items": [
     "Degree is tied to control point count: n+1 points gives degree n.",
     "",
     "<b>Global control.</b> Every control point affects every t. Moving one "
     "changes the whole curve.",
     "",
     "<b>Numerical trouble.</b> High-degree Bernstein evaluation loses "
     "precision.",
     "",
     "<b>Oscillation.</b> High-degree polynomials wiggle between control "
     "points.",
     "",
     "So: use <b>many low-degree segments</b> joined with continuity "
     "constraints — which, formalised, is the B-spline of Module 04.",
   ],
   "footnote": "Cubics (degree 3) are the near-universal choice: enough "
               "freedom for C² joins, little enough for stability."},
 ],
 "takeaways": [
   "A Bézier curve is a convex combination of control points. Every good "
   "property follows from the weights being non-negative and summing to one.",
   "de Casteljau is slower than direct evaluation and numerically stable, and "
   "it yields the subdivision for free.",
   "The convex hull property is what makes flatness-based adaptive "
   "tessellation correct, not merely plausible.",
   "Affine invariance means transforming n control points, not a thousand "
   "samples — and it fails under perspective, which is why NURBS exist.",
   "Cⁿ matches derivatives; Gⁿ matches directions. Anything "
   "travelling along the curve needs C¹; anything shiny needs G².",
   "High-degree Bézier curves have global control and oscillate. Use "
   "many cubic segments — formalised as B-splines.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Definition"),
  ("eq", "B(t) = &Sigma;<sub>i=0</sub><super>n</super> b<sub>i,n</sub>(t) P<sub>i</sub>, &nbsp;&nbsp; b<sub>i,n</sub>(t) = C(n,i) t<super>i</super>(1&minus;t)<super>n&minus;i</super>"),
  ("p", "The weights b<sub>i,n</sub> are the <b>Bernstein polynomials</b> of "
        "degree n. Two facts about them generate everything else:"),
  ("ul", ["They are non-negative on [0,1], since t and (1&minus;t) both are.",
          "They sum to 1 for every t — immediately, by the binomial "
          "theorem applied to (t + (1&minus;t))<super>n</super> = 1."]),
  ("callout", "The curve is a convex combination",
   ["Non-negative weights summing to one is precisely the definition of a "
    "convex combination, and CSCE 641 Module 02 noted that such a combination "
    "of <i>points</i> is well defined where a plain sum is not.",
    "Every property in &sect;2 is a consequence of this one observation. "
    "Treating them as a list to memorise obscures that they are all the same "
    "fact seen from different angles."]),
  ("h2", "1.1 &nbsp; de Casteljau's algorithm"),
  ("code", """vec3 de_casteljau(std::vector<vec3> P, float t) {
    while (P.size() > 1) {
        for (size_t i = 0; i + 1 < P.size(); ++i)
            P[i] = (1 - t) * P[i] + t * P[i + 1];
        P.pop_back();
    }
    return P[0];
}"""),
  ("p", "Repeated linear interpolation: interpolate between adjacent control "
        "points, then between the results, until one point remains. It is "
        "O(n&#178;) rather than the O(n) of Horner evaluation, and it is "
        "preferred anyway for two reasons."),
  ("ul", ["<b>Numerical stability.</b> Every intermediate value is a convex "
          "combination of points on the curve's hull, so no quantity grows. "
          "Direct evaluation of the Bernstein sum involves large binomial "
          "coefficients multiplying small powers, with substantial "
          "cancellation at high degree.",
          "<b>It produces the subdivision for free</b> (&sect;3), which is "
          "what you actually want for rendering."]),

  ("h1", "2 &nbsp; Properties"),
  ("table", ["Property", "Statement", "Consequence"],
   [["<b>Endpoint interpolation</b>", "B(0) = P&#8320; and B(1) = P&#8345;.",
     "Segments can be joined by sharing endpoints; the interior control "
     "points pull without being touched."],
    ["<b>Convex hull</b>", "The curve lies entirely within the convex hull of "
     "its control points.",
     "A bounding volume for free, without evaluating the curve. Makes "
     "conservative culling and the flatness test of &sect;3 valid."],
    ["<b>Affine invariance</b>", "Applying an affine map to the control "
     "points produces exactly the transformed curve.",
     "Transform n points rather than a thousand samples."],
    ["<b>Variation diminishing</b>", "No straight line intersects the curve "
     "more times than it intersects the control polygon.",
     "The curve cannot oscillate more than the polygon you drew — which "
     "is why B&eacute;zier curves feel predictable to designers."],
    ["<b>End tangents</b>", "B&prime;(0) = n(P&#8321; &minus; P&#8320;), "
     "B&prime;(1) = n(P&#8345; &minus; P&#8345;&#8331;&#8321;).",
     "The tangent direction at a join is controlled directly by the adjacent "
     "control point — the basis of continuity constraints in &sect;4."]],
   [0.21, 0.37, 0.42]),
  ("callout", "Affine invariance and its limit",
   ["Transforming the four control points of a cubic costs four matrix "
    "multiplies, and the resulting curve is exactly the transform of the "
    "original. No resampling is required.",
    "This holds for affine transformations — translation, rotation, "
    "scale, shear. It <b>fails</b> for perspective projection, because "
    "perspective involves a division and is therefore not affine.",
    "The repair is to use <i>rational</i> curves, where each control point "
    "carries a weight and the curve is a ratio of polynomials. These are "
    "invariant under projective transformations as well, and they are the "
    "reason NURBS exist. Module 04."]),

  ("break",),
  ("h1", "3 &nbsp; Subdivision and rendering"),
  ("p", "Running de Casteljau at parameter t and retaining the intermediate "
        "values produces the control polygons of the two halves:"),
  ("ul", ["The <b>first</b> point computed at each level, taken in order, is "
          "the control polygon of the curve on [0, t].",
          "The <b>last</b> point at each level, taken in reverse order, is "
          "the control polygon of the curve on [t, 1]."]),
  ("p", "Both halves are exact B&eacute;zier curves of the same degree — "
        "nothing is approximated. This gives the standard rendering "
        "algorithm:"),
  ("code", """void tessellate(const Bezier& c, float tol, std::vector<vec3>& out) {
    if (flat_enough(c, tol)) { out.push_back(c.P[3]); return; }
    auto [L, R] = subdivide(c, 0.5f);
    tessellate(L, tol, out);
    tessellate(R, tol, out);
}

// flat_enough: maximum distance from the interior control points
// to the chord P0-P3, compared against tol."""),
  ("callout", "Why the flatness test is correct and not just plausible",
   ["The convex hull property guarantees the curve lies within the hull of "
    "its control points. If all control points are within <i>tol</i> of the "
    "chord, the entire curve is too.",
    "So the test is <b>conservative</b>: it may subdivide more than strictly "
    "necessary, and it can never under-tessellate. That is exactly the "
    "guarantee you want from a renderer, and it depends on a property that "
    "would otherwise look like trivia.",
    "Adaptive subdivision also naturally produces more segments where "
    "curvature is high and fewer where the curve is nearly straight, which is "
    "the right distribution of effort."]),

  ("h1", "4 &nbsp; Continuity"),
  ("table", ["Order", "Parametric C&#8319;", "Geometric G&#8319;"],
   [["0", "Positions match.", "Identical to C&#8304;."],
    ["1", "First derivatives match <i>as vectors</i>: same direction "
     "<b>and</b> magnitude. The curve is traversed at a consistent speed "
     "through the join.",
     "Tangent <i>directions</i> match; magnitudes may differ. The join looks "
     "smooth; speed may jump."],
    ["2", "Second derivatives match: acceleration is continuous.",
     "Curvature matches. Reflections flow smoothly across the join."]],
   [0.08, 0.46, 0.46]),
  ("p", "C&#8319; implies G&#8319;, but not the reverse. A curve can be "
        "G&#185; and not C&#185;: the two segments meet with the same tangent "
        "direction but different tangent magnitudes."),
  ("callout", "Which you need depends on what is moving",
   ["<b>Something travels along the curve at a parameter-driven rate</b> "
    "— a camera on a spline path, an animated object, a CNC cutting "
    "head. You need <b>C&#185;</b>. A G&#185; join is visually smooth and "
    "produces a sudden change in speed, which reads as a jolt and is "
    "surprisingly noticeable.",
    "<b>The curve is purely a shape</b> — a font outline, a silhouette, "
    "a profile to be swept. <b>G&#185;</b> is sufficient, and it gives the "
    "designer an extra degree of freedom per join.",
    "<b>The resulting surface will be reflective.</b> You need "
    "<b>G&#178;</b>. A curvature discontinuity is invisible in the silhouette "
    "and unmistakable in a reflection, appearing as a crease in the reflected "
    "environment. This is why automotive surfacing standards are stated in "
    "terms of G&#178; and why 'zebra stripe' analysis exists."]),
  ("h2", "4.1 &nbsp; Joining two cubics"),
  ("p", "For two cubic segments with control points P&#8320;&hellip;P&#8323; "
        "and Q&#8320;&hellip;Q&#8323;:"),
  ("ul", ["<b>C&#8304;:</b> Q&#8320; = P&#8323;.",
          "<b>C&#185;:</b> additionally Q&#8321; &minus; Q&#8320; = "
          "P&#8323; &minus; P&#8322; — the three points "
          "P&#8322;, P&#8323;, Q&#8321; are collinear and evenly spaced.",
          "<b>G&#185;:</b> P&#8322;, P&#8323;, Q&#8321; collinear, with "
          "spacing unconstrained.",
          "<b>C&#178;:</b> a further condition on Q&#8322;, which uses up "
          "most of the second segment's freedom — which is exactly the "
          "problem B-splines solve by enforcing it automatically."]),

  ("h1", "5 &nbsp; Why not just raise the degree?"),
  ("p", "A B&eacute;zier curve's degree is tied to its control point count. "
        "Wanting more control means raising the degree, and that goes badly "
        "in three ways."),
  ("ol", ["<b>Global control.</b> Every Bernstein polynomial is non-zero "
          "throughout (0,1), so every control point influences every point of "
          "the curve. Moving one point to fix a local problem changes the "
          "whole curve, which makes editing a long curve impractical.",
          "<b>Numerical conditioning.</b> High-degree Bernstein coefficients "
          "become large while the basis functions become small, and direct "
          "evaluation suffers cancellation. de Casteljau helps but the "
          "underlying conditioning is still poor.",
          "<b>Oscillation.</b> High-degree polynomials tend to wiggle between "
          "their constraints — the same phenomenon as Runge's "
          "oscillation in polynomial interpolation."]),
  ("p", "The answer is to use many <b>low-degree segments</b> joined with "
        "explicit continuity constraints. Cubics are the near-universal "
        "choice: degree 3 provides enough freedom to achieve C&#178; joins "
        "while remaining numerically well behaved."),
  ("p", "Managing those constraints by hand across dozens of segments is "
        "tedious and error-prone. Module 04 introduces B-splines, which are "
        "exactly this construction with the continuity conditions built into "
        "the basis so that they hold automatically."),
 ],
 "resources": [
   ("Keenan Crane — DDG, the curves material",
    "https://brickisland.net/ddg-web/",
    "B&eacute;zier curves with the properties derived rather than asserted."),
   ("Freya Holmér — The Beauty of Bézier Curves (free video)",
    "https://www.youtube.com/watch?v=aVwxzDHniEw",
    "The clearest visual explanation of de Casteljau and the control "
    "properties available anywhere. Watch before reading."),
   ("A Primer on Bézier Curves (free, interactive)",
    "https://pomax.github.io/bezierinfo/",
    "Comprehensive, interactive, with derivations and working code for "
    "everything in this module including subdivision and offsetting."),
   ("GAMES101 Lecture 11 — Geometry 1 (Curves)",
    "https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html",
    "The condensed graphics-oriented treatment you met in CSCE 641."),
 ],
 "exercises": [
   "Implement B&eacute;zier evaluation both by direct Bernstein summation and "
   "by de Casteljau. Compare results at degree 3, 10, and 30, and quantify "
   "the numerical divergence.",
   "Implement subdivision at arbitrary t. Verify that evaluating the left "
   "half at parameter s gives the same point as evaluating the original at "
   "t&middot;s.",
   "Implement adaptive flatness-based tessellation. Render a curve at three "
   "tolerances and report the segment counts; confirm that segments cluster "
   "where curvature is high.",
   "Verify affine invariance numerically: transform the control points, "
   "evaluate, and compare against transforming evaluated points. Then do the "
   "same with a perspective matrix and show that it fails.",
   "Construct two cubic segments joined G&#185; but not C&#185;. Animate a "
   "point along the pair at constant parameter rate and make the speed "
   "discontinuity visible by plotting arc length against t.",
   "Construct a join that is G&#185; but not G&#178;. Sweep a surface along "
   "it, render with a mirror material and an environment map, and capture the "
   "crease in the reflection.",
   "Fit a single B&eacute;zier curve of degree 15 to a set of points and "
   "observe the oscillation. Then fit a chain of cubics and compare.",
 ],
 "selfcheck": [
   "What two facts about the Bernstein basis make a B&eacute;zier curve a "
   "convex combination, and why does that matter?",
   "Give two reasons to prefer de Casteljau over direct evaluation.",
   "Why is the convex hull property what makes flatness-based tessellation "
   "correct?",
   "What does affine invariance buy, and why does it fail under perspective?",
   "Distinguish C&#185; from G&#185; and give a situation where each is the "
   "one you need.",
   "Why does C&#178; matter for reflective surfaces but not for silhouettes?",
   "Give three reasons high-degree B&eacute;zier curves are impractical.",
 ],
},

]

# --- additional module batches ----------------------------------------------
for _b in ("c645_b2", "c645_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
