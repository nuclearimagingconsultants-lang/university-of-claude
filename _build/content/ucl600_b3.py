# -*- coding: utf-8 -*-
"""UC LINA 600 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "The Pipeline as a Matrix Chain",
 "subtitle": "Where the course pays off, visibly.",
 "question": "Can you derive the projection matrix?",
 "outcomes": [
     "Derive the model and view matrices.",
     "Derive a perspective projection matrix.",
     "Explain the depth mapping and its precision problem.",
     "Explain the viewport transform.",
     "Assemble and verify the full chain.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Model and view",
   "blurb": "Both of which you can now build."},

  {"t": "callout", "title": "The model matrix composes the object's transforms and the view matrix is the camera frame inverted",
   "kind": "Two matrices, both already derived",
   "body": ["<b>Model: scale, then rotate, then translate</b> — "
            "<b>composed right to left as TRS</b>, which is the "
            "conventional order and gives the behaviour people "
            "expect (Module 03 §2).",
            "<b>And the order matters visibly</b>: <b>rotating "
            "after translating orbits the object around the "
            "origin</b>, which is sometimes what you want and is "
            "usually a bug.",
            "<b>View: build the camera's orthonormal frame and "
            "invert it</b> (Module 04 §3) — <b>which is a transpose "
            "plus a negated translation</b>, and is four "
            "lines.",
            "<b>So two of the four matrices are already yours</b>, "
            "from Modules 03 and 04 — <b>and the projection is the "
            "only new one.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Deriving the projection",
   "blurb": "From similar triangles, in four lines."},

  {"t": "code", "kicker": "Projection", "title": "Where the matrix comes from",
   "lang": "text", "code": """
  THE GEOMETRY: a point at depth z projects onto a
  screen plane at distance d by similar triangles:

      x_screen = d * x / (-z)      (z negative,
      y_screen = d * y / (-z)       camera looks -z)

  THAT IS A DIVISION, so we need w (Module 07):
  arrange for w = -z and let the hardware divide.

      [ d  0  0  0 ]   so x' = d*x
      [ 0  d  0  0 ]      y' = d*y
      [ 0  0  A  B ]      z' = A*z + B
      [ 0  0 -1  0 ]      w' = -z

  after the divide: x'/w' = -d*x/z.  Correct.

  AND A, B ARE CHOSEN to map the near and far planes
  to the depth range the hardware wants:
      z = -n  ->  z'/w' = -1   (or 0)
      z = -f  ->  z'/w' = +1
  two equations, two unknowns, and you solve them.

  THAT IS THE WHOLE DERIVATION.
""",
   "caption": "<b>Similar triangles, one row to put depth in w, and "
              "two equations for the depth range</b> — which is the "
              "whole projection "
              "matrix.",
   "note": "Project 2 requires this derived rather than copied."},

  {"t": "section", "label": "Part 3", "title": "Depth precision",
   "blurb": "Which follows from the derivation and surprises people."},

  {"t": "callout", "title": "Depth after the divide is non-linear in z, so almost all the precision sits near the near plane",
   "kind": "The consequence of the A and B row",
   "body": ["<b>z' / w' works out to something of the form "
            "a + b/z</b> — <b>a reciprocal</b> — <b>so equal steps in "
            "stored depth are not equal steps in "
            "distance.</b>",
            "<b>Which means a near plane at 0.01 and a far plane at "
            "10,000 spends most of its depth buffer on the first "
            "metre</b> — and the rest of the scene fights over what is "
            "left.",
            "<b>That is z-fighting</b>: <b>two distant surfaces "
            "rounding to the same depth value</b> and flickering — "
            "<b>and the fix is almost always to move the near plane "
            "out</b>, not the far plane in.",
            "<b>Which is a specific, common, and frequently "
            "misdiagnosed bug</b> — <b>and it falls directly out of "
            "Part 2's derivation</b>, which is why deriving "
            "rather than copying matters."]},

  {"t": "section", "label": "Part 4", "title": "Assembling and checking",
   "blurb": "The chain, and how to know it is right."},

  {"t": "bullets", "kicker": "Assembly", "title": "The full chain, and the checks at each stage",
   "items": [
     "<b>p_clip = Projection · View · Model · "
     "p_model</b> — <b>right to left</b>, and <b>the naming "
     "convention makes the composition "
     "checkable</b> (Module 04 §2).",
     "",
     "<b>Then the divide by w</b>, giving normalised device "
     "coordinates in a cube — and <b>anything outside that cube is "
     "clipped</b>.",
     "",
     "<b>Then the viewport transform</b>: <b>scale and shift the "
     "cube to pixel coordinates</b>, which is a trivial affine map "
     "and is where the y-flip usually hides.",
     "",
     "<b>And check each stage separately</b>: <b>a point you "
     "computed by hand, at every stage</b>, rather than looking at the "
     "final image (Module 13 §2).",
     "",
     "<b>Which is the only way to localise an error in a chain of "
     "four</b> — the image tells you something is wrong and never "
     "which matrix.",
   ],
   "footnote": "<b>The image tells you something is wrong and never "
               "which matrix</b> — so check each stage against a "
               "hand-computed point."},

  {"t": "callout", "title": "And the course's payoff is here",
   "kind": "Closing",
   "body": ["<b>Everything in Modules 02 through 07 was for "
            "this</b> — <b>bases, change of basis, linearity, and "
            "homogeneous coordinates</b>, all four used in one "
            "derivation.",
            "<b>And the derivation is about twenty lines "
            "total</b> — <b>which is why the course is four weeks "
            "rather than a semester</b>, and why skipping it costs more "
            "than it saves.",
            "<b>Plus: you can now debug it</b>, which was "
            "Module 01 §1's whole argument — <b>a "
            "copied matrix gives a picture and a derived one gives a "
            "diagnosis.</b>",
            "<b>So Project 2 asks for the derivations alongside the "
            "renderer</b> — <b>because the renderer alone does not "
            "demonstrate the thing the course was "
            "for.</b>"]},
 ],
 "takeaways": [
   "Model is TRS composed right to left; rotating after translating orbits "
   "the origin, which is usually a bug.",
   "The view matrix is the camera frame inverted — a transpose plus a "
   "negated translation.",
   "The projection matrix is similar triangles, one row to put depth in w, "
   "and two equations for the depth range.",
   "Depth after the divide is a reciprocal in z, so almost all precision "
   "sits near the near plane.",
   "Z-fighting is fixed by moving the near plane out, not the far plane "
   "in.",
   "The image tells you something is wrong and never which matrix, so check "
   "each stage against a hand-computed point.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Model and view"),
  ("callout", "The model matrix composes the object's transforms and the view "
              "matrix is the camera frame inverted",
   ["<b>Model: scale, then rotate, then translate</b> — "
    "<b>composed as T &middot; R &middot; S and applied right to "
    "left</b> (Module 03 &sect;2), <b>which is the conventional "
    "order and gives the behaviour people expect</b>: the object scales "
    "about its own origin, turns about its own origin, and then moves "
    "into place.",
    "<b>And the order matters visibly</b>: <b>rotating after "
    "translating makes the object orbit the world origin instead of "
    "spinning in place</b> — <b>which is occasionally what you "
    "want and is usually a bug</b>, and is instantly recognisable once "
    "you have seen it.",
    "<b>View: build the camera's orthonormal frame in world "
    "coordinates and invert it</b> (Module 04 &sect;3) — "
    "<b>which, because the frame is orthonormal, is a transpose plus a "
    "negated translation</b>, <b>and is about four lines of "
    "code</b>.",
    "<b>So two of the pipeline's four matrices are already "
    "yours</b>, from Modules 03 and 04 — <b>and the projection is "
    "the only genuinely new one</b>, which is &sect;2."]),

  ("h1", "2 &nbsp; Deriving the projection"),
  ("code", """THE GEOMETRY: a point at depth z projects onto a
screen plane at distance d by similar triangles:

    x_screen = d * x / (-z)      (z is negative;
    y_screen = d * y / (-z)       camera looks -z)

THAT IS A DIVISION, so we need w (Module 07):
arrange for w = -z and let the hardware divide.

    [ d  0  0  0 ]   so  x' = d*x
    [ 0  d  0  0 ]       y' = d*y
    [ 0  0  A  B ]       z' = A*z + B
    [ 0  0 -1  0 ]       w' = -z

after the divide: x'/w' = -d*x/z.  Correct.

AND A, B ARE CHOSEN to map the near and far planes
to whatever depth range the hardware wants:
    z = -n  ->  z'/w' = -1   (or 0)
    z = -f  ->  z'/w' = +1
two equations, two unknowns, and you solve them.

THAT IS THE WHOLE DERIVATION."""),
  ("p", "<b>Similar triangles, one row to put the depth into w, and "
        "two equations to fix the depth range</b> — <b>which is the "
        "whole projection matrix</b>, and takes about ten minutes the "
        "first time. <b>Project 2 requires this derived rather than "
        "copied</b>, because the derivation is what makes &sect;3's "
        "consequence visible, and because a copied matrix in the wrong "
        "depth convention produces a scene that is entirely black for "
        "reasons nothing explains."),

  ("h1", "3 &nbsp; Depth precision"),
  ("callout", "Depth after the divide is non-linear in z, so almost all the "
              "precision sits near the near plane",
   ["<b>z&prime;/w&prime; works out to something of the form "
    "a + b/z</b> — <b>a reciprocal in the depth</b> — <b>so "
    "equal steps in the stored depth value are emphatically not equal "
    "steps in actual distance</b>, and the relationship is "
    "steep.",
    "<b>Which means a near plane at 0.01 and a far plane at 10,000 "
    "spends the great majority of the depth buffer's precision on the "
    "first metre of the scene</b> — and everything beyond that "
    "fights over the few values left.",
    "<b>That is z-fighting</b>: <b>two distant surfaces rounding to "
    "the same stored depth and flickering between frames as the camera "
    "moves</b> — <b>and the fix is almost always to move the near "
    "plane further out</b>, not to pull the far plane in, because the "
    "ratio f/n is what governs the loss and n is the sensitive "
    "term.",
    "<b>Which is a specific, extremely common, and frequently "
    "misdiagnosed bug</b> — <b>and it falls directly out of "
    "&sect;2's derivation</b>, <b>which is precisely why deriving "
    "rather than copying matters</b> (Module 01 &sect;1's "
    "argument, now concrete)."]),

  ("h1", "4 &nbsp; Assembling and checking"),
  ("ul", ["<b>p_clip = Projection &middot; View &middot; Model "
          "&middot; p_model</b> — <b>applied right to left</b> "
          "— and <b>the from-naming convention makes the "
          "composition checkable by inspection</b> (Module 04 "
          "&sect;2: clip_from_camera &middot; camera_from_world &middot; "
          "world_from_model).",
          "<b>Then the divide by w</b>, which produces normalised "
          "device coordinates inside a cube — and <b>anything "
          "falling outside that cube is clipped</b> before "
          "rasterisation.",
          "<b>Then the viewport transform</b>: <b>scale and shift "
          "the cube to pixel coordinates</b>, which is a trivial affine "
          "map — <b>and is where the y-flip usually hides</b>, "
          "since screen y conventionally grows downward and device y "
          "grows upward.",
          "<b>And check each stage separately</b>: <b>take a point "
          "whose position you computed by hand, and verify it at every "
          "stage of the chain</b> rather than looking at the final image "
          "(Module 13 &sect;2's verification suite).",
          "<b>Which is the only practical way to localise an error "
          "in a chain of four matrices</b> — <b>the image tells "
          "you that something is wrong and never which matrix</b>, and "
          "bisecting the chain by hand is the whole technique."]),
  ("callout", "And the course's payoff is here",
   ["<b>Everything in Modules 02 through 07 was for this</b> "
    "— <b>bases, change of basis, linearity, and homogeneous "
    "coordinates</b> — <b>all four used in a single derivation</b>, "
    "which is a satisfying thing to notice.",
    "<b>And the whole derivation is about twenty lines</b> — "
    "<b>which is why this course is four weeks rather than a "
    "semester</b>, <b>and why skipping it costs more than it "
    "saves</b>.",
    "<b>Plus: you can now debug it</b>, <b>which was Module 01 "
    "&sect;1's entire argument</b> — <b>a copied matrix gives you "
    "a picture and a derived one gives you a diagnosis</b>, and "
    "&sect;3's z-fighting is the clearest example.",
    "<b>So Project 2 asks for the derivations alongside the working "
    "renderer</b> — <b>because the renderer alone does not "
    "demonstrate the thing this course was for</b>, and a renderer "
    "built from copied matrices looks identical to one built from "
    "understood ones until the first bug."]),
 ],
 "resources": [
   ("Scratchapixel, the perspective projection series (free)",
    "https://www.scratchapixel.com/lessons/3d-basic-rendering/perspective-and-orthographic-projection-matrix/",
    "<b>&sect;&sect;2 and 3</b> — the derivation done slowly and in "
    "full, free, with code."),
   ("Gortler, chapters 10 and 11 (library copy)",
    "https://mitpress.mit.edu/9780262017350/",
    "<b>&sect;&sect;1 and 2</b> — the pipeline with every frame "
    "named, which is the careful version."),
   ("Song Ho Ahn &mdash; OpenGL projection matrix (free)",
    "http://www.songho.ca/opengl/gl_projectionmatrix.html",
    "<b>&sect;2</b> — the standard derivation with every algebraic "
    "step shown, which is useful for checking yours."),
   ("Reversed-Z and depth precision writeups (free)",
    "https://developer.nvidia.com/content/depth-precision-visualized",
    "<b>&sect;3</b> — depth precision visualised, and the reversed-Z "
    "technique that largely solves it."),
 ],
 "exercises": [
   "<b>Build a model matrix</b> as TRS and verify the "
   "composition order.",
   "<b>Swap the order</b> and describe what the object does.",
   "<b>Build a view matrix</b> from a camera position and target.",
   "<b>Derive the projection matrix</b> from similar triangles, "
   "yourself.",
   "<b>Solve for A and B</b> given a near and far plane.",
   "<b>Plot stored depth against distance</b> and observe the "
   "reciprocal.",
   "<b>Produce z-fighting deliberately</b>, then fix it by moving "
   "the near plane.",
   "<b>Build the viewport transform</b>, including the y-flip.",
   "<b>Trace one point through all four stages</b> by hand.",
   "<b>Verify your implementation</b> against those hand "
   "numbers.",
 ],
 "selfcheck": [
   "Give the model matrix's composition order and why.",
   "What happens if you rotate after translating?",
   "How is the view matrix built, and why is it an inverse?",
   "Derive the projection matrix from similar triangles.",
   "What are A and B for, and how are they found?",
   "Why is stored depth non-linear in distance?",
   "What is z-fighting and what is the usual fix?",
   "Write the full chain, right to left.",
   "Where does the y-flip live?",
   "How do you localise an error in a four-matrix chain?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Determinants and Degeneracy",
 "subtitle": "One number that tells you volume, orientation, and "
             "invertibility.",
 "question": "What does the determinant measure?",
 "outcomes": [
     "Explain the determinant as a volume scale factor.",
     "Explain what a zero determinant means.",
     "Explain what a negative determinant means.",
     "Relate determinants to invertibility and solving.",
     "Use determinants in graphics contexts.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What it measures",
   "blurb": "A single geometric quantity, and the algebra follows."},

  {"t": "callout", "title": "The determinant is the factor by which the transform scales volume — and its sign says whether orientation flipped",
   "kind": "The definition worth having",
   "body": ["<b>Apply the transform to a unit cube</b>; <b>the "
            "determinant is the volume of what comes out</b> — which "
            "is the whole geometric content.",
            "<b>So det = 2 doubles volume, det = 1 preserves it</b> "
            "— <b>and every rotation has determinant 1</b>, which is "
            "one way to say that rotations do not distort.",
            "<b>Negative determinant means the orientation "
            "flipped</b> — <b>a reflection</b> — <b>and the cube came "
            "out inside-out</b>, which is "
            "Part 3's subject.",
            "<b>And zero means the cube was flattened</b> — "
            "<b>collapsed into a plane, a line, or a point</b> — which "
            "is Part 2 and is the case that matters "
            "most."]},

  {"t": "section", "label": "Part 2", "title": "Zero determinant",
   "blurb": "Which is the condition you actually test for."},

  {"t": "bullets", "kicker": "Degeneracy", "title": "What a zero determinant tells you, five ways",
   "items": [
     "<b>Volume collapsed to nothing</b> — the transform "
     "squashed space into a lower dimension.",
     "",
     "<b>The columns are linearly dependent</b> "
     "(Module 02 §2) — <b>they do not span</b>, so the image "
     "is a proper subspace.",
     "",
     "<b>The matrix is not invertible</b> — <b>information "
     "was destroyed and cannot be recovered</b>, since many inputs map "
     "to the same output.",
     "",
     "<b>The system Ax = b has either no solution or "
     "infinitely many</b> — never exactly one, which is the "
     "linear-systems consequence.",
     "",
     "<b>And in graphics: a degenerate triangle, a collapsed "
     "bone, a singular transform</b> — all of which produce NaNs "
     "downstream (Module 06 §2).",
   ],
   "footnote": "<b>Zero determinant means information was "
               "destroyed</b> — which is why it cannot be inverted, "
               "and why the five statements are all the same "
               "statement."},

  {"t": "section", "label": "Part 3", "title": "Sign and handedness",
   "blurb": "Which connects back to Module 06."},

  {"t": "callout", "title": "A negative determinant flips handedness, which is how a mirrored object turns its normals inside out",
   "kind": "The practical consequence",
   "body": ["<b>Mirror an object by scaling one axis by −1</b>, and "
            "<b>the determinant is −1</b> — <b>so the winding order "
            "effectively reverses</b> and every face now points "
            "inward.",
            "<b>Which is why a mirrored mesh renders inside-out</b> "
            "unless the renderer flips its culling — <b>and is a real "
            "and common asset-pipeline bug.</b>",
            "<b>And it is why a rotation has determinant exactly "
            "+1</b>: <b>rotations preserve both volume and "
            "handedness</b>, which is what distinguishes them from "
            "general orthogonal matrices.",
            "<b>So the test for 'is this a rotation' is: "
            "orthogonal, and determinant +1</b> — <b>two conditions, "
            "both cheap</b>, and Module 13 §2 uses them as a "
            "verification."]},

  {"t": "section", "label": "Part 4", "title": "Using it",
   "blurb": "And the one warning about computing it."},

  {"t": "table", "kicker": "Uses", "title": "Where determinants appear in graphics",
   "header": ["Use", "What the determinant does"],
   "widths": [4.2, 6.8],
   "rows": [
     ["<b>Triangle area and orientation</b>", "<b>2×2 determinant of the edge vectors</b>"],
     ["<b>Backface culling</b>", "<b>Sign of the signed area after projection</b>"],
     ["<b>Barycentric coordinates</b>", "<b>Ratios of sub-triangle determinants</b>"],
     ["<b>Ray-triangle intersection</b>", "<b>Cramer's rule on a 3×3 system</b>"],
     ["<b>Degenerate-transform detection</b>", "<b>Near-zero determinant before inverting</b>"],
     ["<b>Change of volume</b>", "<b>Jacobian determinant, for sampling (CSCE 647)</b>"],
   ],
   "footnote": "<b>Never test determinant == 0 in floating "
               "point</b> — test against a tolerance, and prefer a "
               "condition number when the decision actually "
               "matters.",
   "note": "The Jacobian row is what makes change of variables work "
           "in Monte Carlo integration."},

  {"t": "callout", "title": "And the computational warning",
   "kind": "Closing",
   "body": ["<b>Cofactor expansion is O(n!) and is unusable beyond "
            "about 4×4</b> — <b>which is fine for graphics and is "
            "a trap everywhere else.</b>",
            "<b>Real implementations use LU decomposition</b>, in "
            "O(n³) — <b>and that is what a library does when you ask "
            "for a determinant.</b>",
            "<b>And a tiny determinant does not mean nearly "
            "singular</b> — <b>scaling a matrix by 0.01 scales a 3×3 "
            "determinant by a millionth</b> without making it any harder "
            "to invert.",
            "<b>So for 'is this safe to invert', use the condition "
            "number rather than the determinant</b> — <b>which is the "
            "right tool and is what numerical libraries "
            "report.</b>"]},
 ],
 "takeaways": [
   "The determinant is the factor by which a transform scales volume, and "
   "its sign says whether orientation flipped.",
   "Zero determinant means information was destroyed, which is why the five "
   "consequences are all the same statement.",
   "A negative determinant flips handedness, which is why a mirrored mesh "
   "renders inside-out.",
   "A rotation is orthogonal with determinant +1 — two cheap "
   "conditions that together test for one.",
   "Never test determinant == 0 in floating point; test against a "
   "tolerance.",
   "A tiny determinant does not mean nearly singular — use the "
   "condition number instead.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What it measures"),
  ("callout", "The determinant is the factor by which the transform scales "
              "volume — and its sign says whether orientation flipped",
   ["<b>Apply the transform to a unit cube</b>; <b>the determinant "
    "is the signed volume of the parallelepiped that comes out</b> "
    "— <b>which is the whole geometric content</b>, and everything "
    "algebraic about determinants follows from it.",
    "<b>So a determinant of 2 doubles volume and a determinant of 1 "
    "preserves it</b> — <b>and every rotation has determinant "
    "exactly 1</b>, <b>which is one way of saying that rotations do not "
    "distort</b> (&sect;3).",
    "<b>A negative determinant means the orientation was "
    "flipped</b> — <b>a reflection is involved</b> — <b>and "
    "the cube came out inside-out</b>, which is &sect;3's subject and "
    "has direct consequences for normals.",
    "<b>And zero means the cube was flattened entirely</b> — "
    "<b>collapsed into a plane, a line, or a point</b> — <b>which "
    "is &sect;2, and is the case that matters most in practice</b> "
    "because it is the one you have to test for."]),

  ("h1", "2 &nbsp; Zero determinant"),
  ("ul", ["<b>The volume collapsed to nothing</b> — the "
          "transform squashed three-dimensional space into something "
          "lower-dimensional, and the output has no thickness.",
          "<b>The columns are linearly dependent</b> "
          "(Module 02 &sect;2) — <b>they do not span the "
          "space</b>, so the image of the transform is a proper "
          "subspace and most vectors are unreachable.",
          "<b>The matrix is not invertible</b> — "
          "<b>information was destroyed and cannot be recovered</b>, "
          "because many different inputs map to the same output and "
          "nothing can tell them apart afterwards.",
          "<b>The system Ax = b has either no solution or infinitely "
          "many</b> — <b>never exactly one</b> — which is the "
          "linear-systems consequence and the one a solver "
          "reports.",
          "<b>And in graphics: a degenerate triangle, a collapsed "
          "bone in a skeleton, a singular model transform</b> — "
          "<b>all of which produce NaNs downstream</b> (Module 06 "
          "&sect;2's zero-length normal). <b>Zero determinant means "
          "information was destroyed</b>, <b>which is why it cannot be "
          "inverted, and why all five statements are really the same "
          "statement.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Sign and handedness"),
  ("callout", "A negative determinant flips handedness, which is how a "
              "mirrored object turns its normals inside out",
   ["<b>Mirror an object by scaling one axis by &minus;1</b>, and "
    "<b>the determinant of that transform is &minus;1</b> — <b>so "
    "the effective winding order of every triangle reverses</b> and "
    "every face now points inward (Module 06 &sect;2).",
    "<b>Which is why a mirrored mesh renders inside-out</b> unless "
    "the renderer notices and flips its backface culling to "
    "match — <b>and is a real and common asset-pipeline bug</b>, "
    "usually appearing when somebody mirrors a character to make its "
    "other half.",
    "<b>And it is why a rotation has determinant exactly "
    "+1</b>: <b>rotations preserve both volume and handedness</b>, "
    "<b>which is what distinguishes them from general orthogonal "
    "matrices</b> (an orthogonal matrix with determinant &minus;1 is a "
    "reflection or a rotation-plus-reflection).",
    "<b>So the test for 'is this actually a rotation' is: "
    "orthogonal, and determinant +1</b> — <b>two conditions, both "
    "cheap to check</b> — and <b>Module 13 &sect;2 uses exactly "
    "these two as a verification</b> on any matrix claiming to be a "
    "rotation."]),

  ("h1", "4 &nbsp; Using it"),
  ("table", ["Use", "What the determinant does there"],
   [["<b>Triangle area and orientation</b>",
     "<b>The 2&times;2 determinant of the two edge vectors</b> gives "
     "twice the signed area."],
    ["<b>Backface culling after projection</b>",
     "<b>The sign of that signed area</b> says which way the triangle "
     "faces in screen space."],
    ["<b>Barycentric coordinates</b>",
     "<b>Ratios of sub-triangle determinants</b> — which is why "
     "they are cheap to compute during rasterisation."],
    ["<b>Ray-triangle intersection</b>",
     "<b>Cramer's rule on a 3&times;3 system</b>, which is the "
     "M&ouml;ller-Trumbore algorithm's core."],
    ["<b>Degenerate transform detection</b>",
     "<b>A near-zero determinant before attempting an inverse</b> "
     "— with the caveat in the closing callout."],
    ["<b>Change of volume under a map</b>",
     "<b>The Jacobian determinant</b>, which is how a change of "
     "variables rescales a probability density (CSCE 647)."]],
   [0.34, 0.66]),
  ("p", "<b>Never test <code>determinant == 0</code> in floating "
        "point</b> — <b>test against a tolerance</b>, and <b>prefer "
        "a condition number when the decision actually matters</b> (the "
        "closing callout). <b>The Jacobian row is what makes change of "
        "variables work in Monte Carlo integration</b>: when you sample "
        "in one parameterisation and need a density in another, the "
        "Jacobian determinant is the correction factor, and getting it "
        "wrong biases the whole estimate (CSCE 647 Module 07)."),
  ("callout", "And the computational warning",
   ["<b>Cofactor expansion is O(n!) and is unusable beyond about "
    "4&times;4</b> — <b>which is perfectly fine for graphics, where "
    "everything is 4&times;4</b>, <b>and is a trap in every other "
    "setting</b>, including anything in CSCE 633 or CSCE 669.",
    "<b>Real implementations use LU decomposition and multiply the "
    "diagonal</b>, in O(n<super>3</super>) — <b>and that is what a "
    "numerical library is doing when you ask it for a "
    "determinant</b>.",
    "<b>And a tiny determinant does not mean nearly "
    "singular</b>: <b>scaling a 3&times;3 matrix by 0.01 scales its "
    "determinant by a millionth</b> — <b>without making it any "
    "harder to invert at all</b>, since the inverse just scales "
    "back.",
    "<b>So for the question 'is this safe to invert', use the "
    "condition number rather than the determinant</b> — <b>which "
    "is the right tool for that question and is what numerical libraries "
    "report</b> when they warn you about a matrix."]),
 ],
 "resources": [
   ("3Blue1Brown, chapters 6 and 7 (free)",
    "https://www.3blue1brown.com/topics/linear-algebra",
    "<b>&sect;&sect;1 to 3</b> — the determinant as a volume factor, "
    "which is the framing this module uses throughout."),
   ("MIT 18.06, the determinant lectures (free video)",
    "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
    "<b>&sect;&sect;1 and 2</b> — the properties, and the connection "
    "to invertibility."),
   ("Möller & Trumbore &mdash; Fast ray-triangle intersection "
    "(free)",
    "https://cadxfem.org/inf/Fast%20MinimumStorage%20RayTriangle%20Intersection.pdf",
    "<b>&sect;4's fourth row</b> — determinants doing real work in a "
    "renderer's inner loop."),
   ("Trefethen & Bau &mdash; Numerical Linear Algebra",
    "https://epubs.siam.org/doi/book/10.1137/1.9780898719574",
    "<b>The closing callout</b> — condition numbers and why "
    "determinants are the wrong tool for conditioning. Library "
    "copy."),
 ],
 "exercises": [
   "<b>Compute the determinant</b> of five 2×2 and three "
   "3×3 matrices by hand.",
   "<b>Verify the volume interpretation</b> by transforming a unit "
   "cube.",
   "<b>Construct a transform with determinant 2</b> and confirm the "
   "volume.",
   "<b>Construct one with determinant 0</b> and show the columns are "
   "dependent.",
   "<b>Try to invert it</b> and observe what your library does.",
   "<b>Mirror a mesh</b> and observe the inside-out rendering.",
   "<b>Verify a rotation matrix</b> is orthogonal with determinant "
   "+1.",
   "<b>Compute a triangle's signed area</b> and use it for backface "
   "culling.",
   "<b>Scale a matrix by 0.01</b> and compare determinant to "
   "condition number.",
   "<b>Implement Cramer's rule</b> for ray-triangle "
   "intersection.",
 ],
 "selfcheck": [
   "What does the determinant measure, geometrically?",
   "What does its sign mean?",
   "Give five equivalent consequences of a zero determinant.",
   "Why are they all the same statement?",
   "Why does a mirrored mesh render inside-out?",
   "What two conditions test for a rotation?",
   "Name four graphics uses of determinants.",
   "Why should you never test for exact zero?",
   "Why is cofactor expansion unusable at scale?",
   "Why is a tiny determinant not the same as nearly singular?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Eigenvalues and Eigenvectors",
 "subtitle": "The directions a transform does not turn.",
 "question": "Which vectors come out pointing the same way they went "
             "in?",
 "outcomes": [
     "Define eigenvectors and eigenvalues geometrically.",
     "Compute them for small matrices.",
     "Explain diagonalisation and what it is for.",
     "Explain the symmetric case and why it is special.",
     "Recognise eigen-problems in the program ahead.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The definition",
   "blurb": "Which is geometric before it is algebraic."},

  {"t": "callout", "title": "An eigenvector is a direction the transform only stretches — it comes out along the same line",
   "kind": "The idea, before the characteristic polynomial",
   "body": ["<b>Most vectors get turned by a transform</b>; "
            "<b>eigenvectors do not</b> — <b>they come out as a scalar "
            "multiple of themselves</b>, and that scalar is the "
            "eigenvalue.",
            "<b>Av = λv</b> — <b>which says 'the transform acts on "
            "this direction like simple scaling'</b>, and that is the "
            "whole content.",
            "<b>So a rotation in the plane has no real "
            "eigenvectors</b> — <b>everything turns</b> — while <b>a "
            "3D rotation has exactly one: the axis</b>, with "
            "eigenvalue 1.",
            "<b>Which is a good first example</b>, because <b>'the "
            "axis of rotation is the eigenvector with eigenvalue 1' "
            "makes the definition concrete</b> and is directly useful "
            "(Module 11)."]},

  {"t": "section", "label": "Part 2", "title": "Computing them",
   "blurb": "And why this is the wrong method at scale."},

  {"t": "code", "kicker": "Computation", "title": "By hand, for a 2×2",
   "lang": "text", "code": """
  Av = lv  means  (A - lI)v = 0 for v nonzero,
  which needs A - lI to be SINGULAR, so

      det(A - lI) = 0

  -- the characteristic polynomial. Solve for l,
  then solve (A - lI)v = 0 for each root.

  EXAMPLE  A = [ 2 1 ]
               [ 1 2 ]
      det([2-l, 1], [1, 2-l]) = (2-l)^2 - 1
                              = l^2 - 4l + 3
                              = (l-1)(l-3)
      l = 1:  v = (1, -1)
      l = 3:  v = (1,  1)
  and both are perpendicular, because A is symmetric
  (section 4).

  BUT NOT AT SCALE: root-finding on a degree-n
  polynomial is numerically catastrophic. Real
  implementations use iterative methods (QR, power
  iteration). Use a library and know why.
""",
   "caption": "<b>The characteristic polynomial is for understanding "
              "and for 2×2</b> — real implementations iterate, "
              "because polynomial root-finding is numerically "
              "catastrophic."},

  {"t": "section", "label": "Part 3", "title": "Diagonalisation",
   "blurb": "What eigenvectors are actually for."},

  {"t": "callout", "title": "In its eigenvector basis a transform is diagonal — which is change of basis doing its job",
   "kind": "Why this matters beyond the definition",
   "body": ["<b>A = PDP⁻¹</b>, <b>where P's columns are the "
            "eigenvectors and D is diagonal</b> — <b>which reads as: "
            "change to the eigenbasis, scale each axis, change "
            "back</b> (Module 04).",
            "<b>And then Aⁿ = PDⁿP⁻¹</b>, <b>where Dⁿ is just each "
            "diagonal entry to the n</b> — <b>which turns repeated "
            "application into exponentiation of "
            "numbers.</b>",
            "<b>Which is why eigenvectors matter for anything "
            "iterated</b>: <b>stability of a simulation, convergence of "
            "an iterative method, long-run behaviour of a "
            "Markov chain.</b>",
            "<b>So the question 'does this simulation blow up' is "
            "'is the largest eigenvalue above 1'</b> — <b>which is "
            "CSCE 649's stability analysis</b> and is the most "
            "practical use in this track."]},

  {"t": "section", "label": "Part 4", "title": "The symmetric case",
   "blurb": "Which is the one you meet most, and is well behaved."},

  {"t": "bullets", "kicker": "Symmetric", "title": "Why symmetric matrices are the easy and common case",
   "items": [
     "<b>Real eigenvalues, always</b> — no complex "
     "numbers, which is not true in general.",
     "",
     "<b>And orthogonal eigenvectors</b> — <b>so P is "
     "orthonormal and P⁻¹ = Pᵀ</b> "
     "(Module 04 §2), making the diagonalisation free to "
     "invert.",
     "",
     "<b>Which is the spectral theorem</b>, and <b>it is why the "
     "symmetric case is the one every application arranges to be "
     "in</b>.",
     "",
     "<b>Inertia tensors are symmetric</b> — <b>so the "
     "principal axes are orthogonal</b>, which is why rigid body "
     "dynamics is tractable (CSCE 649).",
     "",
     "<b>And covariance matrices are symmetric</b> — "
     "<b>so principal component analysis is an eigendecomposition</b>, "
     "which is CSCE 633 and CSCE 753.",
   ],
   "footnote": "<b>Covariance matrices are symmetric, so PCA is an "
               "eigendecomposition</b> — which is the single most "
               "common use of this module outside "
               "graphics."},

  {"t": "callout", "title": "And where this appears in the program",
   "kind": "Closing",
   "body": ["<b>CSCE 649: inertia tensors, modal analysis, and "
            "stability of integrators</b> — <b>all eigenvalue "
            "problems</b>, and the last one decides whether your "
            "simulation explodes.",
            "<b>CSCE 753 and CSCE 633: principal components, "
            "spectral clustering</b> — <b>the covariance matrix's "
            "eigenvectors are the directions of greatest "
            "variance.</b>",
            "<b>CSCE 645: mesh smoothing and parameterisation "
            "use the Laplacian's spectrum</b>, which is the same "
            "machinery on a graph.",
            "<b>And Module 11's quaternions are the axis-angle "
            "representation</b> — <b>where the axis is the "
            "eigenvector with eigenvalue 1</b> "
            "(Part 1)."]},
 ],
 "takeaways": [
   "An eigenvector is a direction the transform only stretches; the scalar "
   "is the eigenvalue.",
   "A 3D rotation has exactly one real eigenvector: its axis, with "
   "eigenvalue 1.",
   "The characteristic polynomial is for understanding and for 2×2; "
   "real implementations iterate.",
   "In its eigenvector basis a transform is diagonal, which turns repeated "
   "application into exponentiation of numbers.",
   "'Does this simulation blow up' is 'is the largest eigenvalue above 1'.",
   "Symmetric matrices have real eigenvalues and orthogonal eigenvectors, "
   "which is why applications arrange to be symmetric.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The definition"),
  ("callout", "An eigenvector is a direction the transform only stretches "
              "— it comes out along the same line",
   ["<b>Most vectors get turned as well as stretched by a "
    "transform</b>; <b>eigenvectors do not</b> — <b>they come out "
    "as a scalar multiple of themselves, still on the same line through "
    "the origin</b> — <b>and that scalar is the "
    "eigenvalue</b>.",
    "<b>Av = &lambda;v</b> — <b>which says 'on this particular "
    "direction, the transform acts like simple scaling'</b>, and that "
    "is the entire content of the definition.",
    "<b>So a rotation in the plane has no real eigenvectors at "
    "all</b> — <b>everything turns</b> — while <b>a rotation "
    "in three dimensions has exactly one: its axis</b>, with eigenvalue "
    "1, since the axis is precisely the direction that does not "
    "move.",
    "<b>Which is a good first example to hold onto</b>, because "
    "<b>'the axis of rotation is the eigenvector with eigenvalue 1' "
    "makes the definition concrete</b> and <b>is directly useful</b> "
    "(Module 11's axis-angle representation is this fact, "
    "applied)."]),

  ("h1", "2 &nbsp; Computing them"),
  ("code", """Av = lv  means  (A - lI)v = 0 for some nonzero v,
which requires A - lI to be SINGULAR, so

    det(A - lI) = 0

-- the characteristic polynomial (Module 09 gives
the determinant condition). Solve it for l, then
solve (A - lI)v = 0 for each root.

EXAMPLE  A = [ 2 1 ]
             [ 1 2 ]
    det([2-l, 1], [1, 2-l]) = (2-l)^2 - 1
                            = l^2 - 4l + 3
                            = (l-1)(l-3)
    l = 1:  v = (1, -1)
    l = 3:  v = (1,  1)
and the two are perpendicular, because A is
symmetric (section 4).

BUT NOT AT SCALE: root-finding on a degree-n
polynomial is numerically catastrophic -- the roots
are wildly sensitive to the coefficients. Real
implementations use iterative methods (QR
iteration, power iteration). Use a library, and
know why you are using it."""),
  ("p", "<b>The characteristic polynomial is for understanding and "
        "for 2&times;2 examples</b> — <b>real implementations "
        "iterate, because polynomial root-finding is numerically "
        "catastrophic</b> at any size (Wilkinson's famous example has "
        "roots that move enormously under tiny coefficient "
        "perturbations). This is a case where the textbook method and "
        "the production method are entirely different algorithms, and "
        "knowing that is part of knowing the subject."),

  ("break",),
  ("h1", "3 &nbsp; Diagonalisation"),
  ("callout", "In its eigenvector basis a transform is diagonal — which "
              "is change of basis doing its job",
   ["<b>A = PDP<super>&minus;1</super></b>, <b>where P's columns are "
    "the eigenvectors and D is the diagonal matrix of "
    "eigenvalues</b> — <b>which reads as: change into the "
    "eigenbasis, scale each axis independently, change back</b> "
    "(Module 04's change of basis, used for its intended "
    "purpose).",
    "<b>And then A<super>n</super> = "
    "PD<super>n</super>P<super>&minus;1</super></b>, <b>where "
    "D<super>n</super> is simply each diagonal entry raised to the "
    "n</b> — <b>which turns repeated application of a matrix into "
    "exponentiation of a few numbers</b>, and is the reason "
    "diagonalisation is worth doing at all.",
    "<b>Which is why eigenvectors matter for anything "
    "iterated</b>: <b>the stability of a simulation stepped thousands "
    "of times, the convergence rate of an iterative solver, the "
    "long-run behaviour of a Markov chain</b> (CSCE 658, "
    "CSCE 670's PageRank).",
    "<b>So the question 'does this simulation blow up' becomes 'is "
    "the largest eigenvalue greater than 1 in magnitude'</b> — "
    "<b>which is CSCE 649's stability analysis</b> and <b>is the most "
    "practically important use of this module within this track</b>: it "
    "is the difference between an integrator that works and one that "
    "explodes after four hundred frames."]),

  ("h1", "4 &nbsp; The symmetric case"),
  ("ul", ["<b>Real eigenvalues, always</b> — <b>no complex "
          "numbers appear</b>, which is emphatically not true for "
          "general matrices (a plane rotation has complex "
          "eigenvalues).",
          "<b>And mutually orthogonal eigenvectors</b> — <b>so "
          "P can be taken orthonormal and "
          "P<super>&minus;1</super> = P<super>T</super></b> "
          "(Module 04 &sect;2), <b>which makes the diagonalisation "
          "free to invert and numerically stable</b>.",
          "<b>Which together are the spectral theorem</b>, and "
          "<b>it is why the symmetric case is the one every application "
          "quietly arranges to be in</b> rather than a lucky "
          "coincidence.",
          "<b>Inertia tensors are symmetric</b> by "
          "construction — <b>so the principal axes of a rigid body "
          "are orthogonal</b>, <b>which is why rigid body dynamics is "
          "tractable at all</b> (CSCE 649: in the principal frame the "
          "inertia tensor is diagonal and the equations "
          "decouple).",
          "<b>And covariance matrices are symmetric</b> — "
          "<b>so principal component analysis is exactly an "
          "eigendecomposition</b>, with the eigenvectors giving the "
          "directions of greatest variance and the eigenvalues giving "
          "how much. <b>This is the single most common use of this "
          "module outside graphics</b> (CSCE 633, CSCE 753, "
          "CSCE 676)."]),
  ("callout", "And where this appears in the program",
   ["<b>CSCE 649: inertia tensors, modal analysis of deformable "
    "bodies, and the stability of numerical integrators</b> — "
    "<b>all eigenvalue problems</b>, and <b>the last one decides "
    "whether your simulation explodes</b> or settles.",
    "<b>CSCE 753 and CSCE 633: principal components and spectral "
    "clustering</b> — <b>the covariance matrix's eigenvectors are "
    "the directions of greatest variance</b>, and dimensionality "
    "reduction is keeping the largest few.",
    "<b>CSCE 645: mesh smoothing, parameterisation, and spectral "
    "mesh processing use the Laplacian's spectrum</b>, <b>which is this "
    "same machinery applied to a graph</b> rather than to a geometric "
    "transform.",
    "<b>And Module 11's quaternions encode the axis-angle "
    "representation of a rotation</b> — <b>where the axis is "
    "precisely the eigenvector with eigenvalue 1</b> (&sect;1), so this "
    "module is that one's prerequisite in a direct way."]),
 ],
 "resources": [
   ("3Blue1Brown, chapters 14 and 15 (free)",
    "https://www.3blue1brown.com/topics/linear-algebra",
    "<b>&sect;&sect;1 and 3</b> — eigenvectors geometrically, and the "
    "change-of-basis reading of diagonalisation."),
   ("MIT 18.06, the eigenvalue lectures (free video)",
    "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
    "<b>&sect;&sect;2 to 4</b> — including the spectral theorem and "
    "the applications to difference equations."),
   ("Trefethen & Bau, lectures 24 to 29",
    "https://epubs.siam.org/doi/book/10.1137/1.9780898719574",
    "<b>&sect;2's warning</b> — how eigenvalues are actually "
    "computed, and why not by the polynomial. Library copy."),
   ("Shlens &mdash; A Tutorial on Principal Component Analysis "
    "(free)",
    "https://arxiv.org/abs/1404.1100",
    "<b>&sect;4's last point</b> — PCA derived as an "
    "eigendecomposition, clearly, and free."),
 ],
 "exercises": [
   "<b>Find the eigenvectors</b> of five 2×2 matrices by "
   "hand.",
   "<b>Show a plane rotation has no real eigenvectors.</b>",
   "<b>Find the axis of a 3D rotation</b> as an eigenvector.",
   "<b>Verify Av = λv</b> numerically for each.",
   "<b>Diagonalise a matrix</b> and verify A = PDP⁻¹.",
   "<b>Compute A¹⁰⁰</b> two ways and compare the "
   "cost.",
   "<b>Find the largest eigenvalue</b> of a simple integrator and "
   "predict stability.",
   "<b>Then run the simulation</b> and confirm the prediction.",
   "<b>Verify a symmetric matrix</b> has real eigenvalues and "
   "orthogonal eigenvectors.",
   "<b>Compute the principal components</b> of a small point "
   "cloud.",
 ],
 "selfcheck": [
   "Define an eigenvector geometrically, then algebraically.",
   "Why does a plane rotation have none, and a 3D rotation one?",
   "How are they computed by hand, and why not at scale?",
   "State the diagonalisation and read it as three steps.",
   "Why does it make powers cheap?",
   "What question does the largest eigenvalue answer?",
   "What two properties do symmetric matrices have?",
   "What is that theorem called?",
   "Why are inertia tensors and covariance matrices convenient?",
   "Name four places eigenvectors appear in the program.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Quaternions",
 "subtitle": "How rotations are actually stored.",
 "question": "Why not just use three angles?",
 "outcomes": [
     "Explain what is wrong with Euler angles.",
     "State the quaternion representation of a rotation.",
     "Compose and apply rotations with quaternions.",
     "Interpolate rotations correctly.",
     "Choose a rotation representation for a purpose.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What is wrong with angles",
   "blurb": "Three specific problems, and the third is fatal."},

  {"t": "callout", "title": "Euler angles are order-dependent, interpolate badly, and lose a degree of freedom at certain orientations",
   "kind": "Why a more complicated representation is worth it",
   "body": ["<b>Order-dependent:</b> <b>'yaw 30, pitch 40' and "
            "'pitch 40, yaw 30' give different "
            "orientations</b> — <b>so the convention must be stated</b>, "
            "and there are a dozen in use.",
            "<b>Bad interpolation:</b> <b>interpolating the three "
            "angles separately does not give a smooth rotation</b> — it "
            "wobbles, and the path depends on the "
            "convention.",
            "<b>And gimbal lock:</b> <b>at certain orientations two "
            "of the three axes align and a degree of freedom is "
            "lost</b> — <b>which is not a bug in the implementation but "
            "a property of the representation.</b>",
            "<b>So Euler angles are fine for a user interface and "
            "poor for storage or interpolation</b> — <b>which is "
            "exactly the division of labour engines "
            "use.</b>"]},

  {"t": "section", "label": "Part 2", "title": "The representation",
   "blurb": "Four numbers, encoding an axis and an angle."},

  {"t": "eq", "kicker": "Quaternions", "title": "What the four numbers are",
   "eqs": [
     ("q = (cos(θ/2),  sin(θ/2)·axis)",
      "A scalar part and a vector part. The axis is the eigenvector "
      "with eigenvalue 1 (Module 10 §1), and the half-angle is the "
      "part that surprises people."),
     ("composition is quaternion multiplication, not commutative",
      "Which matches the fact that rotations do not commute "
      "(Module 03 §2) — the algebra records the geometry "
      "faithfully."),
     ("and q and −q are the same rotation",
      "The double cover. It matters for interpolation: pick the "
      "nearer of the two before interpolating or you take the long "
      "way around."),
   ],
   "caption": "<b>Half the angle, and q and −q are the same "
              "rotation</b> — two facts that account for most "
              "quaternion confusion and both of which "
              "matter.",
   "note": "Picking the nearer of q and −q before interpolating "
           "is the bug everybody writes "
           "once."},

  {"t": "section", "label": "Part 3", "title": "Why engines use them",
   "blurb": "Four concrete advantages."},

  {"t": "bullets", "kicker": "Advantages", "title": "What you get for the extra conceptual cost",
   "items": [
     "<b>No gimbal lock</b> — <b>every orientation is "
     "represented equally well</b>, with no degenerate "
     "configurations.",
     "",
     "<b>Smooth interpolation</b> — <b>spherical linear "
     "interpolation follows the shortest arc at constant angular "
     "speed</b>, which is what animation needs.",
     "",
     "<b>Cheap composition and cheap normalisation</b> — "
     "<b>four numbers rather than nine, and drift is corrected by one "
     "normalise</b> rather than by Gram-Schmidt "
     "(Module 05 §4).",
     "",
     "<b>And numerical stability under repeated "
     "composition</b> — <b>which matters in an animation system "
     "accumulating thousands of operations.</b>",
     "",
     "<b>At the cost of being hard to read</b> — <b>nobody "
     "can look at four numbers and picture the rotation</b>, which is "
     "why interfaces still show Euler angles.",
   ],
   "footnote": "<b>Nobody can look at four numbers and picture the "
               "rotation</b> — which is the one real cost, and is "
               "why engines store quaternions and display Euler "
               "angles."},

  {"t": "section", "label": "Part 4", "title": "Choosing",
   "blurb": "Three representations, three jobs."},

  {"t": "table", "kicker": "Choosing", "title": "Which representation for which job",
   "header": ["Representation", "Use it for", "Not for"],
   "widths": [2.8, 4.1, 4.1],
   "rows": [
     ["<b>Euler angles</b>", "<b>User interfaces, authoring, config files</b>", "<b>Storage, interpolation, composition</b>"],
     ["<b>Rotation matrix</b>", "<b>Applying to many vectors; the GPU wants one</b>", "<b>Storage; drift and nine numbers</b>"],
     ["<b>Quaternion</b>", "<b>Storage, interpolation, composition</b>", "<b>Being read by a human</b>"],
   ],
   "footnote": "<b>Convert at the boundaries</b> — author in "
               "Euler, store and interpolate as quaternion, upload as a "
               "matrix — which is what every engine actually "
               "does.",
   "note": "The three-representation workflow is the practical "
           "answer, not choosing one."},

  {"t": "callout", "title": "And the honest summary",
   "kind": "Closing",
   "body": ["<b>Quaternions are not mysterious; they are a "
            "half-angle axis encoding with a multiplication rule that "
            "composes rotations</b> — <b>and the half-angle is the "
            "only genuinely odd part.</b>",
            "<b>You do not need the algebra's derivation to use "
            "them</b> — <b>you need the construction, the composition "
            "rule, slerp, and the double-cover "
            "caveat.</b>",
            "<b>Which is four facts</b>, and "
            "<b>Project 2 accepts either a matrix or a quaternion "
            "camera provided you say which and why.</b>",
            "<b>And the axis is Module 10's "
            "eigenvector</b> — <b>which is a satisfying place for the "
            "two modules to meet</b>, and is worth verifying "
            "numerically once."]},
 ],
 "takeaways": [
   "Euler angles are order-dependent, interpolate badly, and lose a degree "
   "of freedom at gimbal lock.",
   "Gimbal lock is a property of the representation, not a bug in the "
   "implementation.",
   "A quaternion is cos(θ/2) and sin(θ/2) times the axis — "
   "and the axis is the eigenvector with eigenvalue 1.",
   "q and −q are the same rotation, and picking the nearer before "
   "interpolating is the bug everybody writes once.",
   "Nobody can look at four numbers and picture the rotation, which is the "
   "one real cost.",
   "Convert at the boundaries: author in Euler, store as quaternion, upload "
   "as a matrix.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What is wrong with angles"),
  ("callout", "Euler angles are order-dependent, interpolate badly, and lose "
              "a degree of freedom at certain orientations",
   ["<b>Order-dependent:</b> <b>'yaw 30 degrees then pitch 40' and "
    "'pitch 40 then yaw 30' produce different orientations</b> "
    "(Module 03 &sect;2's non-commutativity) — <b>so the "
    "convention has to be stated</b>, <b>and there are a dozen "
    "conventions in common use</b>, which is a genuine "
    "interoperability problem.",
    "<b>Bad interpolation:</b> <b>interpolating the three angles "
    "separately does not produce a smooth rotation</b> — the result "
    "wobbles, changes speed, and <b>takes a path that depends on the "
    "convention</b> rather than on the two endpoints.",
    "<b>And gimbal lock:</b> <b>at certain orientations two of the "
    "three rotation axes align, and a degree of freedom is lost</b> "
    "— the system can no longer rotate in one direction without a "
    "discontinuous jump — <b>which is not a bug in anybody's "
    "implementation but a property of the representation "
    "itself.</b>",
    "<b>So Euler angles are perfectly good for a user interface and "
    "poor for storage or interpolation</b> — <b>which is exactly "
    "the division of labour that engines use</b> (&sect;4), and is why "
    "the answer is not to pick one representation."]),

  ("h1", "2 &nbsp; The representation"),
  ("eq", "q = ( cos(&theta;/2),&nbsp; sin(&theta;/2) &middot; axis )"),
  ("ul", ["<b>A scalar part and a vector part, four numbers "
          "total</b>. <b>The axis is the eigenvector with eigenvalue "
          "1</b> (Module 10 &sect;1) — the direction the rotation "
          "leaves alone — <b>and the half-angle is the part that "
          "surprises everybody</b> and has to be remembered.",
          "<b>Composition is quaternion multiplication, and it is "
          "not commutative</b> — <b>which matches the fact that "
          "rotations do not commute</b> (Module 03 &sect;2) — "
          "<b>so the algebra records the geometry faithfully</b>, as it "
          "did for matrices.",
          "<b>And q and &minus;q represent the same rotation</b> "
          "— the double cover — which is harmless for applying "
          "a rotation and <b>matters a great deal for "
          "interpolation</b>: <b>pick whichever of the two is nearer to "
          "your starting quaternion before interpolating, or you take "
          "the long way around the sphere</b>.",
          "<b>Half the angle, and q and &minus;q are the same "
          "rotation</b> — <b>two facts that account for most "
          "quaternion confusion</b>, and <b>both of which "
          "matter</b>. <b>Picking the nearer of q and &minus;q before "
          "interpolating is the bug everybody writes once</b>, and it "
          "shows up as a character spinning 350 degrees the wrong way "
          "between two keyframes."]),

  ("break",),
  ("h1", "3 &nbsp; Why engines use them"),
  ("ul", ["<b>No gimbal lock</b> — <b>every orientation is "
          "represented equally well</b>, with no degenerate "
          "configurations anywhere on the sphere, which removes an "
          "entire class of bug.",
          "<b>Smooth interpolation</b> — <b>spherical linear "
          "interpolation (slerp) follows the shortest arc between two "
          "orientations at constant angular speed</b>, <b>which is "
          "exactly what animation needs</b> and what Euler interpolation "
          "fails to provide.",
          "<b>Cheap composition and cheap renormalisation</b> "
          "— <b>four numbers rather than nine</b>, and <b>drift "
          "from accumulated floating-point error is corrected by a "
          "single normalise</b> rather than by a Gram-Schmidt pass over "
          "a matrix (Module 05 &sect;4).",
          "<b>And numerical stability under repeated "
          "composition</b> — <b>which matters in an animation "
          "system accumulating thousands of operations per second per "
          "skeleton</b>, where a matrix would drift measurably away from "
          "orthogonality.",
          "<b>At the cost of being essentially unreadable</b> "
          "— <b>nobody can look at four numbers and picture the "
          "rotation they represent</b> — <b>which is the one real "
          "cost, and is why engines store quaternions internally and "
          "display Euler angles in the inspector</b>."]),

  ("h1", "4 &nbsp; Choosing"),
  ("table", ["Representation", "Use it for", "Do not use it for"],
   [["<b>Euler angles</b>",
     "<b>User interfaces, authoring tools, configuration files, "
     "anything a human types.</b>",
     "<b>Storage, interpolation, or composition</b> "
     "(&sect;1)."],
    ["<b>Rotation matrix</b>",
     "<b>Applying the rotation to many vectors, and uploading to the "
     "GPU, which wants a matrix.</b>",
     "<b>Long-term storage</b> — nine numbers, and it drifts out "
     "of orthogonality."],
    ["<b>Quaternion</b>",
     "<b>Storage, interpolation, and composition</b> "
     "(&sect;3).",
     "<b>Being read or edited by a human.</b>"]],
   [0.22, 0.40, 0.38]),
  ("p", "<b>Convert at the boundaries</b> — <b>author in Euler "
        "angles, store and interpolate as a quaternion, convert to a "
        "matrix when uploading to the GPU</b> — <b>which is what "
        "every engine actually does</b>, and is why all three "
        "conversions exist in every maths library. <b>The "
        "three-representation workflow is the practical answer, rather "
        "than choosing one and living with its weaknesses.</b>"),
  ("callout", "And the honest summary",
   ["<b>Quaternions are not mysterious</b>: <b>they are a "
    "half-angle axis-angle encoding together with a multiplication rule "
    "that happens to compose rotations correctly</b> — <b>and the "
    "half-angle is the only genuinely odd part</b> of the "
    "construction.",
    "<b>You do not need the algebra's full derivation to use "
    "them</b> — the relationship to complex numbers and to SU(2) "
    "is interesting and is not required — <b>you need the "
    "construction, the composition rule, slerp, and the double-cover "
    "caveat</b>.",
    "<b>Which is four facts</b>, and <b>Project 2 accepts either a "
    "rotation matrix or a quaternion for the orbiting camera, provided "
    "you say which you used and why</b> — the reasoning being the "
    "assessed part.",
    "<b>And the axis in &sect;2 is Module 10's "
    "eigenvector</b> — <b>which is a satisfying place for the two "
    "modules to meet</b>, <b>and is worth verifying numerically "
    "once</b>: build a rotation matrix, extract its eigenvector with "
    "eigenvalue 1, and compare it to the quaternion's vector part."]),
 ],
 "resources": [
   ("3Blue1Brown and Ben Eater &mdash; Visualizing quaternions "
    "(free, interactive)",
    "https://eater.net/quaternions",
    "<b>&sect;2</b> — the best explanation available, and it is "
    "interactive, which this topic needs more than most."),
   ("Shoemake &mdash; Animating rotation with quaternion curves",
    "https://dl.acm.org/doi/10.1145/325334.325242",
    "<b>&sect;3's slerp</b>, in the original paper that introduced it "
    "to graphics."),
   ("Lengyel, chapter 4 (library copy)",
    "https://www.cengage.com/c/mathematics-for-3d-game-programming-and-computer-graphics-3e-lengyel/",
    "<b>&sect;&sect;2 to 4</b> — quaternions in engine conventions, "
    "with the conversions worked."),
   ("Hanson &mdash; Visualizing Quaternions",
    "https://www.elsevier.com/books/visualizing-quaternions/hanson/978-0-12-088400-1",
    "<b>&sect;2 in depth</b> — far more than this course needs, and "
    "the right book if you want the full picture. Library "
    "copy."),
 ],
 "exercises": [
   "<b>Construct a gimbal lock configuration</b> and demonstrate the "
   "lost degree of freedom.",
   "<b>Interpolate two orientations with Euler angles</b> and "
   "observe the wobble.",
   "<b>Build a quaternion</b> from an axis and angle.",
   "<b>Verify the half-angle</b> by rotating a vector with it.",
   "<b>Compose two quaternions</b> and compare to composing the "
   "equivalent matrices.",
   "<b>Confirm q and −q rotate identically.</b>",
   "<b>Implement slerp</b>, and then omit the nearer-of-two check "
   "and watch it take the long way.",
   "<b>Convert quaternion to matrix and back</b>, and check the "
   "round trip.",
   "<b>Compose a thousand rotations</b> as matrices and as "
   "quaternions, and compare the drift.",
   "<b>Extract a rotation matrix's eigenvector</b> and compare it to "
   "the quaternion axis.",
 ],
 "selfcheck": [
   "Name the three problems with Euler angles.",
   "What is gimbal lock, and is it an implementation bug?",
   "Give the quaternion construction from axis and angle.",
   "What is the axis, in Module 10's terms?",
   "Why is composition non-commutative, and is that right?",
   "What is the double cover, and when does it matter?",
   "Name four advantages of quaternions.",
   "What is their one real cost?",
   "Give the three representations and the job of each.",
   "What four facts do you actually need to use them?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Least Squares",
 "subtitle": "What to do when there is no exact answer.",
 "question": "More equations than unknowns. Now what?",
 "outcomes": [
     "Explain why overdetermined systems have no solution.",
     "Derive the normal equations from projection.",
     "Fit a line and a plane to data.",
     "Explain conditioning and why QR is preferred.",
     "Recognise least squares in the program ahead.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The situation",
   "blurb": "Which is the usual one with measured data."},

  {"t": "callout", "title": "With more equations than unknowns there is usually no exact solution, so you settle for the closest thing",
   "kind": "The problem, and what 'closest' will mean",
   "body": ["<b>Fit a line to twenty noisy points</b>: <b>two "
            "unknowns, twenty equations</b> — <b>and no line passes "
            "through all twenty</b>, so Ax = b has no "
            "solution.",
            "<b>Which means b is not in the column space of "
            "A</b> (Module 02 §2) — <b>it is outside the set of "
            "things A can produce</b>, and that is "
            "the geometric statement.",
            "<b>So find the x making Ax as close to b as "
            "possible</b> — <b>minimising the length of the "
            "residual</b>, which is what 'least squares' "
            "names.",
            "<b>And 'closest' means the projection of b onto the "
            "column space</b> (Module 05 §2) — <b>which is why that "
            "module comes before this one</b> and makes the derivation "
            "three lines."]},

  {"t": "section", "label": "Part 2", "title": "The normal equations",
   "blurb": "Derived from perpendicularity, exactly as before."},

  {"t": "code", "kicker": "Derivation", "title": "Three lines, from Module 05",
   "lang": "text", "code": """
  WE WANT Ax as close to b as possible.
  The closest point in the column space is the
  PROJECTION of b onto it -- and the residual
  (b - Ax) must be perpendicular to that space
  (Module 05 section 2: same condition, bigger
  object).

  PERPENDICULAR TO THE COLUMN SPACE means
  perpendicular to every column, i.e.

      A^T (b - Ax) = 0
      A^T b - A^T A x = 0
      A^T A x = A^T b      <-- the normal equations

  AND THAT IS THE DERIVATION. Solve that square
  system and you have the least squares fit.

  FOR A LINE FIT y = mx + c, A has columns [x, 1],
  and the normal equations give the familiar
  formulas -- which are worth deriving once rather
  than memorising.
""",
   "caption": "<b>The residual is perpendicular to the column "
              "space</b> — the same condition as projecting onto a "
              "single vector, with a bigger "
              "target.",
   "note": "Module 05 §2's projection and this are the same "
           "derivation."},

  {"t": "section", "label": "Part 3", "title": "Conditioning",
   "blurb": "And why nobody solves the normal equations directly."},

  {"t": "callout", "title": "Forming AᵀA squares the condition number, which can destroy half your precision",
   "kind": "The numerical warning that matters here",
   "body": ["<b>The normal equations are correct and are a poor "
            "algorithm</b> — <b>computing AᵀA roughly squares the "
            "condition number</b>, so a mildly awkward problem becomes "
            "a badly conditioned one.",
            "<b>Which in double precision can cost you eight "
            "significant digits</b> — <b>on a problem that was "
            "perfectly solvable</b> before you formed the "
            "product.",
            "<b>So real implementations use QR "
            "decomposition</b> — <b>which solves the same problem "
            "without ever forming AᵀA</b> — or the SVD when the matrix "
            "may be rank-deficient.",
            "<b>And this is the general pattern:</b> <b>the "
            "derivation that explains the answer and the algorithm that "
            "computes it are frequently different</b> "
            "(Module 10 §2 again)."]},

  {"t": "section", "label": "Part 4", "title": "Where it appears",
   "blurb": "Which is almost everywhere there is data."},

  {"t": "bullets", "kicker": "Uses", "title": "Least squares across the program",
   "items": [
     "<b>CSCE 633: linear regression <i>is</i> least "
     "squares</b>, and <b>the normal equations are the closed-form "
     "solution</b> every course starts with.",
     "",
     "<b>CSCE 753: camera calibration, homography estimation, and "
     "bundle adjustment</b> — <b>all overdetermined systems from "
     "noisy measurements.</b>",
     "",
     "<b>CSCE 645: surface fitting and mesh "
     "parameterisation</b> — minimising a quadratic energy is a "
     "least squares problem.",
     "",
     "<b>CSCE 649: constraint solvers</b>, where more constraints "
     "than degrees of freedom is the normal "
     "situation.",
     "",
     "<b>And anywhere you fit anything to measurements</b> — "
     "<b>which is what makes this the most broadly applicable module in "
     "the course</b>.",
   ],
   "footnote": "<b>Linear regression is least squares</b> — so "
               "this module is a machine learning prerequisite as much "
               "as a graphics one."},

  {"t": "callout", "title": "And what it assumes, which is worth stating",
   "kind": "Closing",
   "body": ["<b>Least squares minimises squared error</b>, which "
            "<b>weights a single large outlier as heavily as many small "
            "errors</b> — <b>so one bad measurement can dominate the "
            "fit.</b>",
            "<b>Which is a modelling assumption rather than a "
            "mathematical necessity</b> — <b>it is the right answer "
            "under Gaussian noise and the wrong one under heavy "
            "tails.</b>",
            "<b>And robust alternatives exist</b> — <b>minimising "
            "absolute error, or RANSAC</b> — which CSCE 753 uses "
            "constantly because image correspondences contain gross "
            "outliers.",
            "<b>So the honest claim is: 'the least squares fit, "
            "which assumes the errors are independent and "
            "Gaussian'</b> — <b>which is the program's rule, in a "
            "prerequisite.</b>"]},
 ],
 "takeaways": [
   "With more equations than unknowns, b is not in the column space, so "
   "there is no exact solution.",
   "'Closest' means the projection of b onto the column space, which makes "
   "the derivation three lines.",
   "The residual is perpendicular to the column space — the same "
   "condition as Module 05's projection, with a bigger target.",
   "Forming AᵀA squares the condition number, which can cost eight "
   "significant digits.",
   "Real implementations use QR, so the explaining derivation and the "
   "computing algorithm are different.",
   "Least squares weights one large outlier as heavily as many small "
   "errors, which is a modelling assumption.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The situation"),
  ("callout", "With more equations than unknowns there is usually no exact "
              "solution, so you settle for the closest thing",
   ["<b>Fit a straight line to twenty noisy measured points</b>: "
    "<b>two unknowns (slope and intercept) and twenty equations</b> "
    "— <b>and no line passes through all twenty points</b>, so the "
    "system Ax = b simply has no solution.",
    "<b>Which means, geometrically, that b is not in the column "
    "space of A</b> (Module 02 &sect;2's span) — <b>it lies "
    "outside the set of vectors A is capable of producing</b> — and "
    "that is the precise statement of the difficulty.",
    "<b>So instead find the x that makes Ax as close to b as "
    "possible</b> — <b>minimising the length of the residual "
    "b &minus; Ax</b> — <b>which is what the name 'least squares' "
    "refers to</b>, since minimising a length means minimising a sum of "
    "squares.",
    "<b>And 'closest' means exactly the projection of b onto the "
    "column space</b> (Module 05 &sect;2) — <b>which is why that "
    "module comes before this one</b>, <b>and makes the whole "
    "derivation three lines</b> (&sect;2)."]),

  ("h1", "2 &nbsp; The normal equations"),
  ("code", """WE WANT Ax as close to b as possible.
The closest point in the column space is the
PROJECTION of b onto it -- and the residual
(b - Ax) must therefore be perpendicular to that
space (Module 05 section 2: the same condition,
applied to a bigger object).

PERPENDICULAR TO THE COLUMN SPACE means
perpendicular to every column of A, that is

    A^T (b - Ax) = 0
    A^T b - A^T A x = 0
    A^T A x = A^T b      <-- the normal equations

AND THAT IS THE DERIVATION. Solve that square
system and you have the least squares fit.

FOR A LINE FIT y = mx + c, A has columns [x, 1], and
the normal equations reduce to the familiar
slope-and-intercept formulas -- which are worth
deriving once rather than memorising."""),
  ("p", "<b>The residual is perpendicular to the column space</b> "
        "— <b>the same condition as projecting onto a single "
        "vector, with a bigger target</b> — which is why "
        "<b>Module 05 &sect;2's projection and this are "
        "fundamentally the same derivation</b>. If you can derive one "
        "you can derive the other, and neither needs memorising."),

  ("break",),
  ("h1", "3 &nbsp; Conditioning"),
  ("callout", "Forming AᵀA squares the condition number, which can "
              "destroy half your precision",
   ["<b>The normal equations are mathematically correct and are a "
    "poor numerical algorithm</b> — <b>computing "
    "A<super>T</super>A roughly squares the condition number of the "
    "problem</b>, so a mildly awkward system becomes a badly "
    "conditioned one before you have solved anything.",
    "<b>Which in double precision can cost you around eight "
    "significant digits</b> — <b>on a problem that was perfectly "
    "solvable</b> before you formed the product — and the loss is "
    "silent.",
    "<b>So real implementations use QR decomposition</b> "
    "(Gram-Schmidt's industrial relative, Module 05 &sect;4) — "
    "<b>which solves the identical problem without ever forming "
    "A<super>T</super>A</b> — <b>or the singular value "
    "decomposition when the matrix may be rank-deficient</b> and you "
    "need the minimum-norm solution.",
    "<b>And this is the general pattern of numerical "
    "work:</b> <b>the derivation that explains the answer and the "
    "algorithm that computes it are frequently different "
    "things</b> — <b>which is Module 10 &sect;2's characteristic "
    "polynomial point arriving a second time</b>, and is worth "
    "generalising from."]),

  ("h1", "4 &nbsp; Where it appears"),
  ("ul", ["<b>CSCE 633: linear regression <i>is</i> least "
          "squares</b>, and <b>the normal equations are the closed-form "
          "solution that every machine learning course opens with</b> "
          "before moving to iterative methods for larger "
          "problems.",
          "<b>CSCE 753: camera calibration, homography estimation, "
          "and bundle adjustment</b> — <b>all overdetermined "
          "systems built from noisy measurements</b>, and all solved by "
          "least squares or a robust variant of it.",
          "<b>CSCE 645: surface fitting and mesh "
          "parameterisation</b> — <b>minimising a quadratic energy "
          "over a mesh is a least squares problem</b>, usually a sparse "
          "one, and the Laplacian systems of that course are exactly "
          "this.",
          "<b>CSCE 649: constraint solvers</b>, where <b>more "
          "constraints than degrees of freedom is the normal "
          "situation</b> rather than an exception, and some constraints "
          "must be satisfied only approximately.",
          "<b>And anywhere at all that you fit something to "
          "measurements</b> — <b>which is what makes this the most "
          "broadly applicable module in the course</b>. <b>Linear "
          "regression is least squares</b>, so <b>this module is a "
          "machine learning prerequisite as much as a graphics "
          "one.</b>"]),
  ("callout", "And what it assumes, which is worth stating",
   ["<b>Least squares minimises the sum of squared errors</b>, which "
    "means <b>a single large outlier is weighted as heavily as many "
    "small errors combined</b> — <b>so one bad measurement can "
    "dominate the entire fit</b> and pull the line visibly away from "
    "the data.",
    "<b>Which is a modelling assumption rather than a mathematical "
    "necessity</b> — <b>squared error is the right choice under "
    "independent Gaussian noise</b> (it is the maximum likelihood "
    "estimate there) <b>and the wrong choice under heavy-tailed noise "
    "or gross outliers.</b>",
    "<b>And robust alternatives exist</b> — <b>minimising "
    "absolute error, Huber loss, or RANSAC</b> — <b>which "
    "CSCE 753 uses constantly</b>, because image feature "
    "correspondences contain not just noise but outright wrong "
    "matches.",
    "<b>So the honest claim is: 'the least squares fit, which "
    "assumes the errors are independent and approximately "
    "Gaussian'</b> — <b>which is this program's closing rule "
    "appearing in a prerequisite</b>, and is a good sign that the rule "
    "is not decoration."]),
 ],
 "resources": [
   ("MIT 18.06, the least squares lectures (free video)",
    "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
    "<b>&sect;&sect;1 and 2</b> — projection and the normal "
    "equations, with the column-space picture that makes it "
    "obvious."),
   ("3Blue1Brown, the projection material (free)",
    "https://www.3blue1brown.com/topics/linear-algebra",
    "<b>&sect;1</b> — the geometric picture of projecting onto a "
    "subspace."),
   ("Trefethen & Bau, lectures 11 and 18 to 20",
    "https://epubs.siam.org/doi/book/10.1137/1.9780898719574",
    "<b>&sect;3</b> — why QR rather than the normal equations, with "
    "the conditioning analysis. Library copy."),
   ("Hastie, Tibshirani & Friedman &mdash; Elements of Statistical "
    "Learning (free PDF)",
    "https://hastie.su.domains/ElemStatLearn/",
    "<b>&sect;4's first row</b> — regression as least squares, free, "
    "and the direct bridge to CSCE 633."),
 ],
 "exercises": [
   "<b>Set up an overdetermined system</b> and confirm it has no "
   "solution.",
   "<b>Show that b is outside the column space</b>, explicitly.",
   "<b>Derive the normal equations</b> from perpendicularity.",
   "<b>Fit a line to twenty noisy points</b>, by hand and by "
   "code.",
   "<b>Derive the slope and intercept formulas</b> from the normal "
   "equations.",
   "<b>Fit a plane to three-dimensional points.</b>",
   "<b>Construct an ill-conditioned problem</b> and compare normal "
   "equations to QR.",
   "<b>Measure the digits lost</b> in each.",
   "<b>Add one gross outlier</b> and watch the fit move.",
   "<b>Implement a robust alternative</b> and compare on the same "
   "data.",
 ],
 "selfcheck": [
   "Why does an overdetermined system usually have no solution?",
   "State that geometrically, in terms of the column space.",
   "What does 'closest' mean here?",
   "Derive the normal equations.",
   "Why is this the same derivation as projecting onto a vector?",
   "What is wrong with the normal equations numerically?",
   "What do real implementations use instead?",
   "State the general pattern this illustrates.",
   "Name four places least squares appears in the program.",
   "What does least squares assume, and what are the alternatives?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Claiming a Transform Is Correct",
 "subtitle": "Verification, rather than looking at the picture.",
 "question": "It looks right. Is it right?",
 "outcomes": [
     "Explain why visual inspection is insufficient.",
     "Build a verification suite for transforms.",
     "State the invariants worth checking.",
     "Assess whether you are ready for Semester 1.",
     "State the program's closing rule in this subject.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why looking is not enough",
   "blurb": "Five ways a wrong matrix looks right."},

  {"t": "table", "kicker": "Failures", "title": "Wrong transforms that produce plausible images",
   "header": ["The error", "What you see"],
   "widths": [4.6, 6.4],
   "rows": [
     ["<b>Transposed rotation</b>", "<b>Everything rotates the wrong way — looks deliberate</b>"],
     ["<b>Wrong handedness</b>", "<b>A mirrored scene, which reads as an art choice</b>"],
     ["<b>Normals not inverse-transposed</b>", "<b>Slightly wrong shading under non-uniform scale</b>"],
     ["<b>Unnormalised normals</b>", "<b>Too bright or too dark; reads as a lighting problem</b>"],
     ["<b>Composition order swapped</b>", "<b>Correct for symmetric test scenes only</b>"],
   ],
   "footnote": "<b>A symmetric test scene hides composition "
               "errors</b> — which is why the test scene should be "
               "deliberately asymmetric, at a known off-axis "
               "position.",
   "note": "Every row here is a bug that ships, because each one "
           "produces a picture."},

  {"t": "callout", "title": "Because a plausible image is the weakest possible evidence",
   "kind": "The argument for a test suite",
   "body": ["<b>The pipeline produces a picture from almost any "
            "matrices</b> — <b>so 'I see something' rules out only "
            "crashes</b>, and crashes were never the "
            "risk.",
            "<b>And you are the worst possible judge of your own "
            "scene</b> — <b>you know what it should look like, so you "
            "see what you expect</b> "
            "(CSCE 671 §01 §2, and UC MATH 600 "
            "§13 §2).",
            "<b>So the fix is numbers:</b> <b>a point whose screen "
            "position you computed by hand, checked "
            "automatically</b> — which cannot be "
            "talked out of a disagreement.",
            "<b>Which takes an hour to set up and saves "
            "days</b> — and <b>is the one engineering habit this "
            "course is trying to install.</b>"]},

  {"t": "section", "label": "Part 2", "title": "The verification suite",
   "blurb": "What to check, concretely."},

  {"t": "code", "kicker": "Tests", "title": "The checks, in order of how often they catch something",
   "lang": "text", "code": """
  1  KNOWN POINTS
         a unit cube at the origin, a camera on an
         axis, and screen positions you computed on
         paper. Assert them.

  2  ROUND TRIPS
         M * M^-1 == I to tolerance.
         world_from_camera * camera_from_world == I.

  3  INVARIANTS OF ROTATIONS
         orthogonal: R * R^T == I
         determinant == +1  (Module 09 section 3)
         lengths preserved: |Rv| == |v|
         -- three cheap checks that catch transposes
            and handedness errors

  4  DEGENERACY GUARDS
         |det| above tolerance before inverting
         |n| above tolerance before normalising

  5  AND A VISUAL CHECK LAST
         normals drawn as segments, axes drawn in
         colour -- useful, and not evidence.

  THE FIRST THREE WOULD CATCH EVERY ROW OF THE
  TABLE IN SECTION 1.
""",
   "caption": "<b>The first three checks would catch every failure "
              "in §1's table</b> — which is the argument for "
              "writing them, and they are about forty lines "
              "total.",
   "note": "Project 2 requires this suite and one bug found by it."},

  {"t": "section", "label": "Part 3", "title": "Are you ready?",
   "blurb": "The five questions, taken honestly."},

  {"t": "bullets", "kicker": "Readiness", "title": "Take these before Semester 1",
   "items": [
     "<b>Can you derive a rotation matrix</b> by drawing where "
     "the basis vectors go? "
     "(Module 03 §1.)",
     "",
     "<b>Can you derive the projection formula</b> from the "
     "perpendicularity condition? "
     "(Module 05 §2.)",
     "",
     "<b>Can you say why the view matrix is an inverse</b>, and "
     "why it is a transpose? "
     "(Module 04 §3.)",
     "",
     "<b>Can you explain what w is for</b>, both of its "
     "jobs? (Module 07.)",
     "",
     "<b>And can you derive the projection matrix</b> from "
     "similar triangles? (Module 08 §2.)",
   ],
   "footnote": "<b>Five questions.</b> Answer all five and start "
               "Semester 1; otherwise the ones you missed name the "
               "modules to revisit."},

  {"t": "section", "label": "Part 4", "title": "The rule",
   "blurb": "Which is the program's, in this subject's terms."},

  {"t": "callout", "title": "State what you verified, state what you assumed, and never claim more than you established",
   "kind": "Closing",
   "body": ["<b>In this subject it means:</b> <b>name the "
            "handedness convention, name the spaces each matrix maps "
            "between, and say what you tested</b> — three "
            "things.",
            "<b>'The transform is correct' means 'it passes these "
            "assertions under this convention'</b> — <b>which is a "
            "checkable claim</b>, unlike 'it looks "
            "right'.",
            "<b>And the convention is the one most often left "
            "unstated</b> — <b>which is why every handedness bug is "
            "somebody's unstated assumption meeting somebody else's "
            "unstated assumption.</b>",
            "<b>So: convention, spaces, tests</b> — <b>and that is "
            "the prerequisite done</b>, with the same rule the other "
            "thirty-six courses close on."]},
 ],
 "takeaways": [
   "Every wrong transform in §1's table produces a plausible picture, "
   "which is why they ship.",
   "A symmetric test scene hides composition errors, so make the test scene "
   "asymmetric and off-axis.",
   "You are the worst judge of your own scene, because you see what you "
   "expect.",
   "Three cheap checks — orthogonality, determinant +1, length "
   "preservation — catch transposes and handedness errors.",
   "The first three checks would catch every failure in the table, and are "
   "about forty lines total.",
   "'The transform is correct' means 'it passes these assertions under this "
   "convention'.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why looking is not enough"),
  ("table", ["The error", "What you actually see"],
   [["<b>Transposed rotation matrix</b>",
     "<b>Everything rotates the wrong way</b> — which looks "
     "deliberate, and reads as a control-direction preference."],
    ["<b>Wrong handedness convention</b> (Module 06 &sect;3)",
     "<b>A mirrored scene</b>, which reads as an art choice until "
     "somebody tries to read text in it."],
    ["<b>Normals transformed by M rather than the inverse "
     "transpose</b> (Module 06 &sect;4)",
     "<b>Slightly wrong shading, but only under non-uniform "
     "scale</b> — so it passes every uniformly-scaled test."],
    ["<b>Normals not renormalised after transforming</b>",
     "<b>Too bright or too dark</b> — which reads as a lighting "
     "parameter problem and gets 'fixed' by changing the light."],
    ["<b>Composition order swapped</b> (Module 03 &sect;2)",
     "<b>Correct results for symmetric test scenes only</b> — "
     "see the note."]],
   [0.40, 0.60]),
  ("p", "<b>A symmetric test scene hides composition errors</b> "
        "— a cube at the origin rotated about its own centre looks "
        "identical under several wrong orderings — <b>which is why "
        "the test scene should be deliberately asymmetric and at a known "
        "off-axis position</b>. <b>Every row in this table is a bug "
        "that ships</b>, <b>because each one produces a picture</b>, "
        "and a picture is what most people check against."),
  ("callout", "Because a plausible image is the weakest possible evidence",
   ["<b>The pipeline will produce a picture from almost any set of "
    "matrices</b> — <b>so 'I see something' rules out only crashes "
    "and all-black output</b>, <b>and crashes were never the "
    "risk</b>.",
    "<b>And you are the worst possible judge of your own "
    "scene</b> — <b>you know what it is supposed to look like, so "
    "you see what you expect to see</b> (CSCE 671 Module 01 "
    "&sect;2's designer blindness, and UC MATH 600 Module 13 "
    "&sect;2's inability to find gaps in your own argument — the "
    "same phenomenon twice).",
    "<b>So the fix is numbers:</b> <b>a point whose screen position "
    "you computed by hand on paper, asserted automatically</b> — "
    "<b>which cannot be talked out of a disagreement</b> and does not "
    "know what the scene is supposed to look like.",
    "<b>Which takes about an hour to set up and saves days</b> "
    "— and <b>is the one engineering habit this course is trying "
    "to install</b>, over and above the mathematics."]),

  ("h1", "2 &nbsp; The verification suite"),
  ("code", """1  KNOWN POINTS
       a unit cube at the origin, a camera on an
       axis, and screen positions you computed on
       paper. Assert them exactly.

2  ROUND TRIPS
       M * M^-1 == I to a stated tolerance.
       world_from_camera * camera_from_world == I.

3  INVARIANTS OF ROTATIONS
       orthogonal:   R * R^T == I
       determinant:  det(R) == +1
                     (Module 09 section 3)
       lengths:      |Rv| == |v|
       -- three cheap checks that between them catch
          transposes and handedness errors

4  DEGENERACY GUARDS
       |det| above tolerance before inverting
       |n| above tolerance before normalising
       (Module 06 section 2)

5  AND A VISUAL CHECK LAST
       normals drawn as segments, basis axes drawn
       in colour -- useful for orientation, and not
       evidence of correctness.

THE FIRST THREE WOULD CATCH EVERY ROW OF THE TABLE
IN SECTION 1."""),
  ("p", "<b>The first three checks would catch every failure in "
        "&sect;1's table</b> — <b>which is the argument for writing "
        "them</b>, <b>and they are about forty lines of code "
        "total</b>. <b>Project 2 requires this suite and at least one "
        "bug found by it rather than by looking at the image</b>, "
        "because finding one is the demonstration that the suite is "
        "doing work."),

  ("break",),
  ("h1", "3 &nbsp; Are you ready?"),
  ("ul", ["<b>Can you derive a rotation matrix by drawing where the "
          "basis vectors go</b>, rather than recalling the sign "
          "pattern? (Module 03 &sect;1.)",
          "<b>Can you derive the projection-onto-a-vector formula "
          "from the perpendicularity condition</b>, in three lines? "
          "(Module 05 &sect;2.)",
          "<b>Can you say why the view matrix is an inverse, and why "
          "for an orthonormal frame that inverse is a transpose?</b> "
          "(Module 04 &sect;3.)",
          "<b>Can you explain what the fourth coordinate is "
          "for</b> — <b>both of its jobs</b>, making translation "
          "linear and enabling the perspective divide? "
          "(Module 07.)",
          "<b>And can you derive the perspective projection matrix "
          "from similar triangles?</b> (Module 08 &sect;2.) <b>Five "
          "questions.</b> <b>Answer all five and start Semester 1</b>; "
          "<b>otherwise the ones you missed name exactly the modules to "
          "revisit</b>, which is more useful than a mark."]),

  ("h1", "4 &nbsp; The rule"),
  ("callout", "State what you verified, state what you assumed, and never "
              "claim more than you established",
   ["<b>In this subject it means three things:</b> <b>name the "
    "handedness convention, name the spaces each matrix maps between "
    "(Module 04 &sect;2's from-naming), and say what you actually "
    "tested.</b>",
    "<b>'The transform is correct' means 'it passes these "
    "assertions under this convention'</b> — <b>which is a "
    "checkable claim</b> — <b>unlike 'it looks right'</b>, which "
    "is a report about a person rather than about a matrix.",
    "<b>And the convention is the thing most often left "
    "unstated</b> — <b>which is why essentially every handedness "
    "bug is one person's unstated assumption meeting another person's "
    "unstated assumption</b>, usually across a file format "
    "boundary.",
    "<b>So: convention, spaces, tests</b> — <b>and that is the "
    "prerequisite done</b>, closing on <b>the same rule the other "
    "thirty-six courses close on</b>, which it turns out applies to a "
    "4&times;4 matrix as readily as to an experiment."]),
 ],
 "resources": [
   ("Gortler, the conventions appendix (library copy)",
    "https://mitpress.mit.edu/9780262017350/",
    "<b>&sect;4</b> — conventions stated explicitly, which is what "
    "this module is asking you to do."),
   ("Scratchapixel, the testing and debugging notes (free)",
    "https://www.scratchapixel.com/",
    "<b>&sect;2</b> — practical verification of a renderer, "
    "free."),
   ("Shirley &mdash; Ray Tracing in One Weekend (free)",
    "https://raytracing.github.io/",
    "<b>&sect;&sect;1 and 2</b> — a complete small renderer to test "
    "your understanding against, free and short."),
   ("The glTF specification, the coordinate conventions (free)",
    "https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html",
    "<b>&sect;4</b> — a format that states its conventions "
    "explicitly, which is why it interoperates."),
 ],
 "exercises": [
   "<b>Introduce each of §1's five errors</b> deliberately and "
   "look at the result.",
   "<b>Build an asymmetric test scene</b> and show it catches a "
   "composition error the symmetric one missed.",
   "<b>Compute one point's screen position by hand</b>, through all "
   "four stages.",
   "<b>Assert it</b> in a test.",
   "<b>Write the round-trip tests</b> for every matrix you "
   "build.",
   "<b>Write the three rotation invariant checks.</b>",
   "<b>Verify they catch a transposed rotation.</b>",
   "<b>Add the degeneracy guards</b> and feed them a degenerate "
   "triangle.",
   "<b>Take the five readiness questions</b> without reference.",
   "<b>Project 2 is now due.</b> Submit the renderer, the derivation "
   "of every matrix in it, the verification suite, at least one bug the "
   "suite found rather than your eyes, and a statement of the handedness "
   "convention you used.",
 ],
 "selfcheck": [
   "Name five wrong transforms that still produce a picture.",
   "Why does a symmetric test scene hide errors?",
   "Why are you the worst judge of your own scene?",
   "What is the fix, and why does it work?",
   "Give the five categories of check, in order.",
   "Which three would catch everything in the table?",
   "Give the three rotation invariants.",
   "What are the degeneracy guards for?",
   "Give the five readiness questions.",
   "State the closing rule in this subject's terms.",
 ],
},

]
