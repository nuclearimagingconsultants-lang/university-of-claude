# -*- coding: utf-8 -*-
"""UC LINA 600 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Vectors, Spans, and Bases",
 "subtitle": "What a coordinate actually is.",
 "question": "What do the numbers in a vector mean?",
 "outcomes": [
     "Explain a vector as an arrow and as a coordinate list.",
     "Define span and linear independence.",
     "Define a basis and explain why coordinates need one.",
     "Explain dimension.",
     "Recognise these objects in graphics contexts.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two readings",
   "blurb": "Which you have to be able to switch between."},

  {"t": "callout", "title": "A vector is an arrow, and its coordinates are instructions for building it from basis vectors",
   "kind": "The idea the whole course rests on",
   "body": ["<b>(3, 2) means 'three of the first basis vector plus "
            "two of the second'</b> — <b>so the numbers are relative "
            "to a choice somebody made</b>, and the arrow "
            "is not.",
            "<b>Which is why the same arrow has different "
            "coordinates in different bases</b> — <b>and why change of "
            "basis</b> (Module 04) <b>is the central operation rather "
            "than a technicality.</b>",
            "<b>And the arrow reading is the one to think in</b>, "
            "with the coordinates as bookkeeping — <b>which is the "
            "reverse of how it is usually taught</b> and is why "
            "3Blue1Brown is on the reading list "
            "first.",
            "<b>Plus the operations have geometric "
            "meanings:</b> <b>addition is tip-to-tail, scaling is "
            "stretching</b> — and <b>every algebraic rule is a "
            "statement about those pictures.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Span",
   "blurb": "Everything you can reach."},

  {"t": "bullets", "kicker": "Span", "title": "What a set of vectors reaches, and what it misses",
   "items": [
     "<b>The span is the set of all linear combinations</b> "
     "— <b>all the places you can get to by scaling and "
     "adding</b>.",
     "",
     "<b>One non-zero vector spans a line</b>; <b>two "
     "independent vectors span a plane</b>; <b>three independent ones "
     "in 3D span everything.</b>",
     "",
     "<b>And two vectors pointing the same way span only a "
     "line</b> — <b>which is linear dependence</b>, and is the "
     "failure this vocabulary exists to "
     "name.",
     "",
     "<b>So: vectors are linearly independent if none is in the "
     "span of the others</b> — <b>equivalently, if the only "
     "combination summing to zero is the all-zero "
     "one.</b>",
     "",
     "<b>Which matters in graphics immediately</b>: <b>three "
     "collinear points do not define a plane</b>, and a mesh face built "
     "from them has no normal "
     "(Module 06 §2).",
   ],
   "footnote": "<b>Three collinear points do not define a "
               "plane</b> — which is linear dependence, and is a "
               "degenerate triangle in every mesh you will ever "
               "load."},

  {"t": "section", "label": "Part 3", "title": "Basis",
   "blurb": "Which is what makes coordinates mean anything."},

  {"t": "callout", "title": "A basis is a set that is independent and spans — so every vector has exactly one coordinate list",
   "kind": "Why both conditions are needed",
   "body": ["<b>Spanning gives you at least one way to write every "
            "vector</b>; <b>independence gives you at most "
            "one</b> — <b>and together they give exactly one</b>, "
            "which is what a coordinate system "
            "is.",
            "<b>Too few vectors and some points are "
            "unreachable</b>; <b>too many and the coordinates are not "
            "unique</b> — so the basis is the Goldilocks "
            "condition.",
            "<b>And the dimension is the number of vectors in any "
            "basis</b> — <b>which is the same for every basis of a "
            "space</b>, and that invariance is a theorem rather than an "
            "observation.",
            "<b>So 'three-dimensional' means 'every basis has three "
            "vectors'</b> — <b>not 'the vectors have three "
            "numbers'</b>, which is a coordinate fact rather than a "
            "space fact."]},

  {"t": "section", "label": "Part 4", "title": "In graphics",
   "blurb": "Where every one of these shows up by week three."},

  {"t": "table", "kicker": "Graphics", "title": "These objects, in the places you will meet them",
   "header": ["Concept", "Where it appears", "What goes wrong"],
   "widths": [2.5, 4.3, 4.2],
   "rows": [
     ["<b>Basis</b>", "<b>Every coordinate frame: model, world, camera, tangent</b>", "<b>Mixing frames silently</b>"],
     ["<b>Span</b>", "<b>The plane of a triangle; a subspace of motion</b>", "<b>Degenerate faces</b>"],
     ["<b>Independence</b>", "<b>Whether three points define a plane</b>", "<b>Zero-length normals</b>"],
     ["<b>Linear combination</b>", "<b>Barycentric interpolation across a triangle</b>", "<b>Weights not summing to one</b>"],
     ["<b>Dimension</b>", "<b>Degrees of freedom in a rig or a spline</b>", "<b>Over-constrained solves</b>"],
   ],
   "footnote": "<b>Mixing frames silently is the characteristic bug "
               "of this whole subject</b> — the numbers are valid, "
               "the arrows are in the wrong space, and nothing "
               "errors.",
   "note": "Barycentric coordinates are the clearest everyday use of "
           "a linear combination."},

  {"t": "callout", "title": "And the habit this module asks for",
   "kind": "Closing",
   "body": ["<b>Label every vector with the space it lives "
            "in</b> — <b>in a comment, in a variable name, in your "
            "head</b> — <b>because the type system will not do it for "
            "you</b> and the numbers all look alike.",
            "<b>Which is the single cheapest defence against the "
            "characteristic bug of this subject</b> "
            "(Part 4), and costs a naming "
            "convention.",
            "<b>And it makes Module 04 easy</b>, because "
            "<b>a change of basis is then visibly a conversion between "
            "two labelled spaces</b> rather than a matrix appearing "
            "from nowhere.",
            "<b>So: <code>v_world</code>, "
            "<code>v_camera</code>, <code>n_tangent</code></b> — "
            "<b>and never a bare <code>v</code></b>, which is a "
            "convention Project 2 enforces."]},
 ],
 "takeaways": [
   "Coordinates are instructions for building an arrow from basis vectors, "
   "so they are relative to a choice somebody made.",
   "The arrow reading is the one to think in, with coordinates as "
   "bookkeeping.",
   "Three collinear points do not define a plane — linear dependence, "
   "and a degenerate triangle.",
   "Spanning gives at least one coordinate list and independence gives at "
   "most one; together, exactly one.",
   "'Three-dimensional' means every basis has three vectors, not that "
   "vectors have three numbers.",
   "Mixing frames silently is the characteristic bug of the subject, and "
   "labelling every vector is the cheapest defence.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two readings"),
  ("callout", "A vector is an arrow, and its coordinates are instructions for "
              "building it from basis vectors",
   ["<b>(3, 2) means 'three of the first basis vector, plus two of "
    "the second'</b> — <b>so the numbers are relative to a choice "
    "somebody made</b>, <b>and the arrow itself is not</b>. The arrow "
    "exists; the numbers describe it from a particular point of "
    "view.",
    "<b>Which is exactly why the same arrow has different "
    "coordinates in different bases</b> — and <b>why change of "
    "basis</b> (Module 04) <b>is the central operation of this "
    "course rather than a technicality buried in chapter "
    "nine</b>.",
    "<b>And the arrow reading is the one to think in</b>, with the "
    "coordinate list as bookkeeping — <b>which is the reverse of "
    "how the subject is usually taught</b>, and <b>is why the "
    "3Blue1Brown series is first on the reading list</b> rather than "
    "supplementary.",
    "<b>Plus the operations all have geometric meanings:</b> "
    "<b>addition is tip-to-tail, scaling is stretching (and reversing, "
    "for a negative scalar)</b> — and <b>every algebraic rule you "
    "will learn is a statement about those pictures</b>, which is how "
    "to check whether a rule you half-remember is right."]),

  ("h1", "2 &nbsp; Span"),
  ("ul", ["<b>The span of a set of vectors is the set of all their "
          "linear combinations</b> — <b>every place you can reach "
          "by scaling them and adding</b> — and it is always a "
          "line, a plane, a space, or (for the empty set) the "
          "origin.",
          "<b>One non-zero vector spans a line through the "
          "origin</b>; <b>two independent vectors span a plane</b>; "
          "<b>three independent vectors in three dimensions span "
          "everything.</b>",
          "<b>And two vectors pointing along the same line span only "
          "that line, however you scale them</b> — <b>which is "
          "linear dependence</b>, <b>and is the failure this vocabulary "
          "exists to name</b>.",
          "<b>So: a set is linearly independent if none of its "
          "members lies in the span of the others</b> — "
          "<b>equivalently, if the only linear combination summing to "
          "the zero vector is the one with all coefficients zero</b>, "
          "which is the form you actually compute with.",
          "<b>Which matters in graphics immediately</b>: <b>three "
          "collinear points do not define a plane</b>, <b>and a mesh "
          "face built from them has no well-defined normal</b> "
          "(Module 06 &sect;2's zero-length cross product) — "
          "<b>a degenerate triangle, which exists in every mesh you "
          "will ever load.</b>"]),

  ("break",),
  ("h1", "3 &nbsp; Basis"),
  ("callout", "A basis is a set that is independent and spans — so every "
              "vector has exactly one coordinate list",
   ["<b>Spanning gives you at least one way to write every "
    "vector</b>; <b>independence guarantees at most one</b> — "
    "<b>and the two together give exactly one</b>, <b>which is what a "
    "coordinate system is</b> and why both conditions appear in the "
    "definition.",
    "<b>Too few vectors and some points of the space are simply "
    "unreachable</b>; <b>too many and a vector has several different "
    "coordinate lists</b>, so 'the coordinates of v' stops naming "
    "anything — the basis is the condition that is just "
    "right.",
    "<b>And the dimension of a space is the number of vectors in "
    "any basis for it</b> — <b>which is the same number for every "
    "basis</b>, and <b>that invariance is a theorem rather than an "
    "observation</b>, and a non-trivial one.",
    "<b>So 'three-dimensional' means 'every basis has three "
    "vectors'</b> — <b>not 'the vectors are written with three "
    "numbers'</b>, which is a fact about a coordinate convention rather "
    "than about the space. The distinction matters as soon as you meet "
    "a two-dimensional subspace of a three-dimensional space, which in "
    "graphics is every triangle."]),

  ("h1", "4 &nbsp; In graphics"),
  ("table", ["Concept", "Where you will meet it", "What goes wrong"],
   [["<b>Basis</b>",
     "<b>Every coordinate frame: model, world, camera, tangent, "
     "light.</b>",
     "<b>Mixing frames silently</b> — see the note."],
    ["<b>Span</b>",
     "<b>The plane containing a triangle; the subspace a constrained "
     "joint can move in.</b>",
     "<b>Degenerate faces that span only a line.</b>"],
    ["<b>Linear independence</b>",
     "<b>Whether three points actually determine a plane.</b>",
     "<b>Zero-length normals, and the NaNs that follow when you "
     "normalise them.</b>"],
    ["<b>Linear combination</b>",
     "<b>Barycentric interpolation of colour, normals, and UVs "
     "across a triangle.</b>",
     "<b>Weights that do not sum to one</b>, which shifts everything "
     "subtly."],
    ["<b>Dimension</b>",
     "<b>Degrees of freedom in a rig, a spline, or a solver.</b>",
     "<b>Over-constrained systems with no solution</b> "
     "(Module 12)."]],
   [0.18, 0.40, 0.42]),
  ("p", "<b>Mixing frames silently is the characteristic bug of this "
        "whole subject</b> — <b>the numbers are valid, the arrows "
        "are in the wrong space, and nothing errors</b>: you get a "
        "picture, and it is wrong in a way that looks like an art "
        "problem. <b>Barycentric coordinates are the clearest everyday "
        "use of a linear combination</b>, and they are the reason "
        "anything varies smoothly across a triangle."),
  ("callout", "And the habit this module asks for",
   ["<b>Label every vector with the space it lives in</b> — "
    "<b>in a comment, in a variable name, or at minimum in your "
    "head</b> — <b>because the type system will not do it for "
    "you</b> and three floats look exactly like three other "
    "floats.",
    "<b>Which is the single cheapest defence against the "
    "characteristic bug of this subject</b> (&sect;4's note), and "
    "<b>it costs a naming convention and nothing else</b>.",
    "<b>And it makes Module 04 easy</b>, because <b>a change of "
    "basis is then visibly a conversion between two labelled "
    "spaces</b> — <code>M_world_from_camera</code> — <b>rather "
    "than a matrix appearing from nowhere</b> with an unmemorable "
    "name.",
    "<b>So: <code>v_world</code>, <code>v_camera</code>, "
    "<code>n_tangent</code></b> — <b>and never a bare "
    "<code>v</code></b>, <b>which is a convention Project 2 "
    "enforces</b> and which pays for itself the first time a shading "
    "bug turns out to be a frame mismatch."]),
 ],
 "resources": [
   ("3Blue1Brown, chapters 1 to 3 (free)",
    "https://www.3blue1brown.com/topics/linear-algebra",
    "<b>The whole module</b> — vectors, span, and basis, visually, "
    "and this is the right first exposure."),
   ("MIT 18.06, lectures 1 and 5 (free video)",
    "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
    "<b>&sect;&sect;2 and 3</b> — the column picture and independence, "
    "from Strang."),
   ("Immersive Math, chapters 2 and 3 (free)",
    "http://immersivemath.com/ila/",
    "<b>&sect;&sect;1 to 3</b> with manipulable figures — drag the "
    "basis vectors and watch the coordinates change, which is the "
    "point of &sect;1."),
   ("Gortler, chapter 2 (library copy)",
    "https://mitpress.mit.edu/9780262017350/",
    "<b>&sect;4's frames</b> — unusually careful about labelling "
    "which space a vector is in, which most graphics texts are "
    "not."),
 ],
 "exercises": [
   "<b>Draw ten vectors</b> and their sums, tip to tail.",
   "<b>Write one arrow's coordinates</b> in two different bases.",
   "<b>Find the span</b> of three given sets of vectors.",
   "<b>Determine independence</b> for five sets, by solving for a "
   "zero combination.",
   "<b>Construct three collinear points</b> and show they span only a "
   "line.",
   "<b>Verify that a basis gives unique coordinates</b>, by finding "
   "them two ways.",
   "<b>Find a set that spans but is dependent</b>, and one that is "
   "independent but does not span.",
   "<b>Compute barycentric coordinates</b> of a point in a "
   "triangle.",
   "<b>Interpolate a colour</b> across a triangle with them.",
   "<b>Adopt the naming convention</b> and apply it to any existing "
   "code you have.",
 ],
 "selfcheck": [
   "What do a vector's coordinates mean?",
   "Why does the same arrow have different coordinates in different "
   "bases?",
   "Define span, and say what one, two, and three vectors can "
   "span.",
   "Define linear independence, two equivalent ways.",
   "Give the graphics consequence of dependence.",
   "Define a basis and say what each condition buys.",
   "What is dimension, and why is it well-defined?",
   "What does 'three-dimensional' actually mean?",
   "Name five places these concepts appear in graphics.",
   "What is the characteristic bug, and what is the defence?",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Matrices as Linear Maps",
 "subtitle": "The columns are where the basis vectors land.",
 "question": "Why is matrix multiplication defined that way?",
 "outcomes": [
     "Read a matrix as a transformation.",
     "Explain why the columns are the images of basis vectors.",
     "Explain matrix multiplication as composition.",
     "Explain why multiplication is not commutative.",
     "Build the standard graphics transform matrices.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The one idea",
   "blurb": "Which makes everything else follow."},

  {"t": "callout", "title": "The columns of a matrix are where the basis vectors land — and that single fact derives everything",
   "kind": "The idea to internalise before anything else",
   "body": ["<b>A linear map is determined by what it does to the "
            "basis vectors</b>, because <b>everything else is a linear "
            "combination of them and the map preserves "
            "combinations.</b>",
            "<b>So write down where each basis vector goes, as "
            "columns, and you have the matrix</b> — <b>which is how "
            "you build every transform in this course</b>, rather than "
            "looking one up.",
            "<b>And then Mv is 'take v's coordinates as weights, and "
            "combine the columns'</b> — <b>which is what matrix-vector "
            "multiplication computes</b>, read "
            "correctly.",
            "<b>Which makes the definition inevitable rather than "
            "arbitrary</b> — and <b>anybody who finds matrix "
            "multiplication unmotivated has been shown the rule before "
            "the reason.</b>"]},

  {"t": "code", "kicker": "Building", "title": "Deriving a rotation matrix in ten seconds",
   "lang": "text", "code": """
  WHERE DO THE BASIS VECTORS GO under a rotation by
  theta in the plane?

      (1,0)  ->  (cos t,  sin t)
      (0,1)  ->  (-sin t, cos t)

  Those are the columns. So

      R = [ cos t   -sin t ]
          [ sin t    cos t ]

  AND THAT IS THE DERIVATION. No memorisation, and
  no risk of getting the signs backwards -- draw the
  two arrows and read off the answer.

  SAME METHOD, SCALE BY (a, b):
      (1,0) -> (a, 0),  (0,1) -> (0, b)
      S = [ a 0 ]
          [ 0 b ]

  SAME METHOD, SHEAR:
      (1,0) -> (1, 0),  (0,1) -> (k, 1)
      and you have it.

  EVERY MATRIX IN THIS COURSE IS BUILT THIS WAY.
""",
   "caption": "<b>Draw where the basis vectors go and read off the "
              "columns</b> — which removes every sign error from "
              "every transform in the "
              "course.",
   "note": "Project 1 requires every matrix built this way rather "
           "than looked up."},

  {"t": "section", "label": "Part 2", "title": "Composition",
   "blurb": "Which is what multiplication means."},

  {"t": "callout", "title": "Matrix multiplication is composition of maps, which is why it is associative and why it is not commutative",
   "kind": "Both properties, from one reading",
   "body": ["<b>AB means 'apply B, then apply A'</b> — <b>right to "
            "left</b>, which is backwards from reading order and is the "
            "source of endless confusion.",
            "<b>Associative because composing functions is "
            "associative</b> — <b>(AB)C and A(BC) are both 'do C, then "
            "B, then A'</b>, which is obviously the same "
            "thing.",
            "<b>And not commutative because the order you apply "
            "operations in matters</b> — <b>rotate then translate "
            "lands somewhere different from translate then "
            "rotate</b>, which you can check with a pen in ten "
            "seconds.",
            "<b>So the non-commutativity is not an algebraic "
            "quirk</b> — <b>it is a geometric fact that the algebra "
            "faithfully records</b>, and Project 1 asks you to "
            "demonstrate it."]},

  {"t": "section", "label": "Part 3", "title": "The standard transforms",
   "blurb": "All derivable, none worth memorising."},

  {"t": "table", "kicker": "Transforms", "title": "The ones you need, and what each does to the basis",
   "header": ["Transform", "Effect on basis vectors", "Notes"],
   "widths": [2.5, 4.4, 4.1],
   "rows": [
     ["<b>Scale</b>", "<b>Each stretched along its own axis</b>", "<b>Diagonal matrix</b>"],
     ["<b>Rotation</b>", "<b>Both turned by θ</b>", "<b>Columns are cos/sin; derive, do not recall</b>"],
     ["<b>Shear</b>", "<b>One fixed, one tilted</b>", "<b>Off-diagonal entry</b>"],
     ["<b>Reflection</b>", "<b>One negated</b>", "<b>Determinant −1 (M09)</b>"],
     ["<b>Projection</b>", "<b>Collapsed onto a subspace</b>", "<b>Not invertible; information lost</b>"],
     ["<b>Translation</b>", "<b>— not linear at all</b>", "<b>Needs M07's fourth coordinate</b>"],
   ],
   "footnote": "<b>Translation is not a linear map</b> — it moves "
               "the origin, and every linear map fixes the origin "
               "— which is precisely why homogeneous coordinates "
               "exist (Module 07).",
   "note": "The translation row is the one that motivates the whole "
           "of Module 07."},

  {"t": "section", "label": "Part 4", "title": "What linear means",
   "blurb": "Precisely, since it is doing real work."},

  {"t": "bullets", "kicker": "Linearity", "title": "The two conditions, and what they rule out",
   "items": [
     "<b>T(u + v) = T(u) + T(v)</b> and <b>T(cv) = cT(v)</b> "
     "— <b>which together mean the map preserves linear "
     "combinations</b>, and that is the whole "
     "definition.",
     "",
     "<b>Geometrically: lines stay lines, the origin stays "
     "put, and parallel lines stay parallel and evenly "
     "spaced</b>.",
     "",
     "<b>Which immediately rules out translation</b> "
     "(Part 3) — <b>it moves the origin</b> — and rules "
     "out anything with a squared term.",
     "",
     "<b>And it is why a linear map is determined by the "
     "basis</b> (Part 1): <b>knowing the images of a "
     "basis plus linearity determines everything</b>.",
     "",
     "<b>So the restriction buys the representation</b> — "
     "<b>linear maps are exactly the ones a matrix can "
     "express</b>, which is the trade.",
   ],
   "footnote": "<b>The restriction buys the representation</b> "
               "— linear maps are exactly the ones a matrix can "
               "express, which is why the definition is worth being "
               "exact about."},

  {"t": "callout", "title": "And the thing to carry forward",
   "kind": "Closing",
   "body": ["<b>Never look up a transform matrix</b> — <b>draw "
            "where the basis vectors go and read off the "
            "columns</b> (Part 1), which takes "
            "ten seconds and cannot be got "
            "backwards.",
            "<b>And always read a product right to left</b>, as "
            "composition — <b>which makes the model-view-projection "
            "chain readable</b> "
            "(Module 08).",
            "<b>Plus: translation is coming, and it does not "
            "fit</b> — <b>which is the one gap in this module and is "
            "Module 07's entire subject.</b>",
            "<b>Which is a good example of how the course is "
            "built:</b> <b>a restriction that buys something, then a "
            "trick that evades the restriction without giving the "
            "purchase back.</b>"]},
 ],
 "takeaways": [
   "The columns of a matrix are where the basis vectors land, and that "
   "single fact derives everything else.",
   "Mv means 'take v's coordinates as weights and combine the columns'.",
   "Draw where the basis vectors go and read off the columns — which "
   "removes every sign error.",
   "Matrix multiplication is composition, applied right to left, which is "
   "why it is associative and not commutative.",
   "Translation is not a linear map because it moves the origin, which is "
   "why homogeneous coordinates exist.",
   "The restriction buys the representation: linear maps are exactly the "
   "ones a matrix can express.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The one idea"),
  ("callout", "The columns of a matrix are where the basis vectors land "
              "— and that single fact derives everything",
   ["<b>A linear map is completely determined by what it does to the "
    "basis vectors</b>, <b>because every other vector is a linear "
    "combination of them and the map preserves linear "
    "combinations</b> (&sect;4's definition) — so there is nothing "
    "left to specify.",
    "<b>So write down where each basis vector goes, stack those "
    "images as columns, and you have the matrix</b> — <b>which is "
    "how you build every transform in this course</b>, <b>rather than "
    "looking one up and hoping the sign convention matches "
    "yours</b>.",
    "<b>And then Mv means 'take v's coordinates as weights, and "
    "combine the columns accordingly'</b> — <b>which is exactly "
    "what matrix-vector multiplication computes</b>, read "
    "correctly rather than as a row-by-column ritual.",
    "<b>Which makes the definition of the product inevitable rather "
    "than arbitrary</b> — and <b>anybody who finds matrix "
    "multiplication unmotivated has been shown the rule before the "
    "reason</b>, which is unfortunately the standard order."]),
  ("code", """WHERE DO THE BASIS VECTORS GO under a rotation by
theta in the plane?

    (1,0)  ->  (cos t,  sin t)
    (0,1)  ->  (-sin t, cos t)

Those are the columns. So

    R = [ cos t   -sin t ]
        [ sin t    cos t ]

AND THAT IS THE DERIVATION. No memorisation, and no
risk of getting the signs backwards -- draw the two
arrows and read the answer off the picture.

SAME METHOD, SCALE BY (a, b):
    (1,0) -> (a, 0),  (0,1) -> (0, b)
    S = [ a 0 ]
        [ 0 b ]

SAME METHOD, SHEAR:
    (1,0) -> (1, 0),  (0,1) -> (k, 1)
    and you have it.

EVERY MATRIX IN THIS COURSE IS BUILT THIS WAY."""),
  ("p", "<b>Draw where the basis vectors go and read off the "
        "columns</b> — <b>which removes every sign error from every "
        "transform in the course</b>, and is why <b>Project 1 requires "
        "every matrix built this way rather than looked up</b>. The "
        "ten seconds spent drawing two arrows is reliably cheaper than "
        "the twenty minutes spent wondering why the object rotates the "
        "wrong way."),

  ("h1", "2 &nbsp; Composition"),
  ("callout", "Matrix multiplication is composition of maps, which is why it "
              "is associative and why it is not commutative",
   ["<b>AB means 'apply B first, then apply A'</b> — <b>right "
    "to left</b> — <b>which is backwards from reading order and is "
    "the source of endless confusion</b> about transform order, "
    "including in documentation.",
    "<b>It is associative because composing functions is "
    "associative</b>: <b>(AB)C and A(BC) both mean 'do C, then B, then "
    "A'</b>, <b>which is obviously the same thing</b> once you read the "
    "product as composition — and is a tedious computation if you "
    "read it as entries.",
    "<b>And it is not commutative because the order in which you "
    "apply operations matters</b> — <b>rotate then translate lands "
    "an object somewhere quite different from translate then "
    "rotate</b> — <b>which you can verify with a pen and a piece "
    "of paper in ten seconds</b>.",
    "<b>So the non-commutativity is not an algebraic quirk to be "
    "remembered</b> — <b>it is a geometric fact that the algebra "
    "faithfully records</b> — and <b>Project 1 asks you to "
    "demonstrate it and explain it</b> rather than merely observe "
    "it."]),

  ("break",),
  ("h1", "3 &nbsp; The standard transforms"),
  ("table", ["Transform", "What it does to the basis vectors", "Notes"],
   [["<b>Scale</b>", "<b>Each basis vector stretched along its own "
     "axis.</b>", "<b>A diagonal matrix.</b>"],
    ["<b>Rotation</b>", "<b>Both basis vectors turned by the same "
     "angle.</b>",
     "<b>Columns are cosines and sines</b> — <b>derive them, do "
     "not recall them</b> (&sect;1)."],
    ["<b>Shear</b>", "<b>One fixed, the other tilted.</b>",
     "<b>A single off-diagonal entry.</b>"],
    ["<b>Reflection</b>", "<b>One basis vector negated.</b>",
     "<b>Determinant &minus;1</b>, which flips handedness "
     "(Module 09 &sect;3)."],
    ["<b>Projection onto a subspace</b>",
     "<b>Collapsed onto a line or plane.</b>",
     "<b>Not invertible — information is destroyed</b>, and the "
     "determinant is zero."],
    ["<b>Translation</b>", "<b>&mdash; it is not a linear map at "
     "all.</b>",
     "<b>Needs Module 07's fourth coordinate</b> — see the "
     "note."]],
   [0.20, 0.42, 0.38]),
  ("p", "<b>Translation is not a linear map</b> — <b>it moves "
        "the origin, and every linear map necessarily fixes the "
        "origin</b> (set c = 0 in T(cv) = cT(v)) — <b>which is "
        "precisely why homogeneous coordinates exist</b> "
        "(Module 07). <b>The translation row is the one that motivates "
        "the whole of Module 07</b>, and noticing the gap here makes "
        "that module feel like a solution rather than a convention."),

  ("h1", "4 &nbsp; What linear means"),
  ("ul", ["<b>T(u + v) = T(u) + T(v)</b> and "
          "<b>T(cv) = c&middot;T(v)</b> — <b>which together mean "
          "the map preserves linear combinations</b>, <b>and that is "
          "the entire definition</b>; everything else in this module is "
          "a consequence.",
          "<b>Geometrically: straight lines stay straight, the "
          "origin stays where it is, and parallel evenly-spaced lines "
          "stay parallel and evenly spaced</b> — which is the "
          "picture to check a candidate map against.",
          "<b>Which immediately rules out translation</b> "
          "(&sect;3) — <b>it moves the origin</b> — and rules "
          "out anything involving a squared term, a sine of a "
          "coordinate, or a constant offset.",
          "<b>And it is exactly why a linear map is determined by "
          "its action on a basis</b> (&sect;1): <b>knowing the images "
          "of the basis vectors plus linearity determines the image of "
          "everything else</b>, by writing it as a combination.",
          "<b>So the restriction buys the representation</b> "
          "— <b>linear maps are precisely the maps a matrix can "
          "express</b> — <b>which is the trade, and is why the "
          "definition is worth being exact about</b> rather than "
          "treating 'linear' as a vague synonym for simple."]),
  ("callout", "And the thing to carry forward",
   ["<b>Never look up a transform matrix</b> — <b>draw where "
    "the basis vectors go and read off the columns</b> "
    "(&sect;1) — <b>which takes ten seconds and cannot be got "
    "backwards</b>, unlike a half-remembered formula.",
    "<b>And always read a matrix product right to left, as "
    "composition</b> — <b>which makes the model-view-projection "
    "chain readable</b> as a sentence (Module 08's "
    "<code>Viewport &middot; Project &middot; View &middot; Model</code> "
    "is 'model first, viewport last').",
    "<b>Plus: translation is coming, and it does not fit into this "
    "framework</b> — <b>which is the one gap in this module and is "
    "Module 07's entire subject.</b>",
    "<b>Which is a good example of how this course is built:</b> "
    "<b>a restriction that buys you something, and then a trick that "
    "evades the restriction without giving the purchase back</b> "
    "— homogeneous coordinates let you express translation as a "
    "linear map in one more dimension."]),
 ],
 "resources": [
   ("3Blue1Brown, chapters 3 to 5 (free)",
    "https://www.3blue1brown.com/topics/linear-algebra",
    "<b>&sect;&sect;1 and 2</b> — matrices as transformations and "
    "multiplication as composition, which is this module's entire "
    "thesis."),
   ("MIT 18.06, lectures 2 and 3 (free video)",
    "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
    "<b>&sect;&sect;1 and 4</b> — the column picture, which Strang "
    "builds the course on."),
   ("Immersive Math, chapter 6 (free)",
    "http://immersivemath.com/ila/",
    "<b>&sect;&sect;1 to 3</b> — drag a transform's basis images and "
    "watch the matrix change, which is &sect;1 made "
    "interactive."),
   ("Lengyel, chapters 2 and 3 (library copy)",
    "https://www.cengage.com/c/mathematics-for-3d-game-programming-and-computer-graphics-3e-lengyel/",
    "<b>&sect;3</b> — the graphics transforms in the conventions you "
    "will meet in an engine."),
 ],
 "exercises": [
   "<b>Derive the 2D rotation matrix</b> by drawing the basis "
   "images.",
   "<b>Derive scale, shear, and reflection</b> the same way.",
   "<b>Derive a 3D rotation about each axis.</b>",
   "<b>Verify Mv combines the columns</b>, on three examples.",
   "<b>Compose two transforms in both orders</b> and draw the "
   "results.",
   "<b>Explain the difference geometrically</b>, not just "
   "numerically.",
   "<b>Verify associativity</b> on a triple product.",
   "<b>Show that translation violates linearity</b>, explicitly.",
   "<b>Find a projection matrix</b> onto a line and show it is not "
   "invertible.",
   "<b>Check the two linearity conditions</b> for five candidate "
   "maps.",
 ],
 "selfcheck": [
   "What are the columns of a matrix?",
   "Why is a linear map determined by the basis?",
   "What does Mv compute, read correctly?",
   "Derive the rotation matrix.",
   "What does AB mean, and in what order?",
   "Why is multiplication associative? Why not commutative?",
   "Name six standard transforms and their effect on the basis.",
   "Why is translation not linear?",
   "State the two linearity conditions and their geometric "
   "meaning.",
   "What does the restriction buy?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Change of Basis",
 "subtitle": "The most useful idea in the course.",
 "question": "The same arrow, described from two places. How do you "
             "convert?",
 "outcomes": [
     "Explain what a change of basis does.",
     "Build a change of basis matrix from the basis vectors.",
     "Invert it, and explain the direction convention.",
     "Explain the view matrix as a change of basis.",
     "Avoid the standard direction confusion.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The setup",
   "blurb": "Two descriptions of one arrow."},

  {"t": "callout", "title": "The arrow does not change; only the numbers describing it do",
   "kind": "The idea, which is simpler than the notation suggests",
   "body": ["<b>A point in a room has one position</b>, and <b>two "
            "people with different coordinate systems assign it "
            "different numbers</b> — <b>neither is wrong</b> "
            "(Module 02 §1).",
            "<b>So a change of basis is a translation between two "
            "descriptions</b> — <b>a dictionary, not a "
            "movement</b> — and nothing in the world moves when you "
            "apply one.",
            "<b>Which is the distinction that causes all the "
            "trouble</b>: <b>rotating an object and rotating the frame "
            "you describe it in produce inverse matrices</b>, and look "
            "identical on screen.",
            "<b>And the view matrix is the second kind</b> — "
            "<b>the camera does not move the world; it re-describes "
            "it</b> — which is why Part 3 exists."]},

  {"t": "section", "label": "Part 2", "title": "Building the matrix",
   "blurb": "Which is one sentence, once you have Module 03."},

  {"t": "code", "kicker": "Construction", "title": "The matrix whose columns are the new basis vectors",
   "lang": "text", "code": """
  SUPPOSE a basis B has vectors b1, b2, b3, each
  written IN WORLD COORDINATES.

  BUILD  M = [ b1 | b2 | b3 ]   (as columns)

  THEN M takes B-coordinates TO world coordinates.
      v_world = M * v_B

  WHY: v_B = (x,y,z) means "x of b1 plus y of b2
  plus z of b3" -- and M*v_B combines the columns
  with exactly those weights (Module 03 section 1).
  So the construction is forced.

  AND THE OTHER DIRECTION is the inverse:
      v_B = M^-1 * v_world

  THE DIRECTION CONVENTION, which is worth fixing
  once and never rethinking:
      name it M_world_from_B.
      Then M_world_from_B * v_B = v_world
      reads as cancellation, and
      M_world_from_B * M_B_from_camera is obviously
      M_world_from_camera.
""",
   "caption": "<b>Name it <code>M_world_from_B</code></b> — then "
              "the subscripts cancel like units and you can never "
              "compose two of them "
              "backwards.",
   "note": "This naming convention eliminates the single most common "
           "error in the subject."},

  {"t": "callout", "title": "And for an orthonormal basis the inverse is just the transpose, which is why frames are built orthonormal",
   "kind": "The shortcut that makes this cheap",
   "body": ["<b>If the basis vectors are unit length and mutually "
            "perpendicular</b>, <b>the matrix is orthogonal and "
            "M⁻¹ = Mᵀ</b> — which is free to compute and numerically "
            "exact.",
            "<b>So camera frames, tangent frames, and bone frames "
            "are all built orthonormal deliberately</b> — <b>not for "
            "elegance but because inverting them is then a "
            "transpose.</b>",
            "<b>And it is why Gram-Schmidt matters</b> "
            "(Module 05 §4): <b>given any basis, it produces an "
            "orthonormal one spanning the "
            "same space.</b>",
            "<b>Plus the numerical point:</b> <b>a general inverse "
            "accumulates error and a transpose does "
            "not</b> — which matters in a loop running sixty times a "
            "second."]},

  {"t": "section", "label": "Part 3", "title": "The view matrix",
   "blurb": "Which is the whole idea, applied once."},

  {"t": "bullets", "kicker": "View matrix", "title": "Deriving it, rather than copying a lookAt function",
   "items": [
     "<b>Build the camera's frame in world coordinates</b>: "
     "<b>forward, right, and up, orthonormal</b> — which is "
     "Module 05's cross products and "
     "normalisation.",
     "",
     "<b>Those columns give M_world_from_camera</b> "
     "(Part 2) — the matrix that takes camera "
     "coordinates to world ones.",
     "",
     "<b>But you want the opposite</b>: <b>the view matrix is "
     "M_camera_from_world</b>, which is the inverse — <b>and "
     "because the frame is orthonormal, the transpose.</b>",
     "",
     "<b>Plus the translation</b>, which does not fit in a 3×3 "
     "and is Module 07's subject — <b>and inverts by "
     "negating</b>.",
     "",
     "<b>Which is the entire derivation of lookAt</b>, and it "
     "takes four lines once the convention is fixed.",
   ],
   "footnote": "<b>That is the entire derivation of lookAt</b> "
               "— four lines, and it explains why the function has "
               "a transpose and a negated translation in "
               "it."},

  {"t": "section", "label": "Part 4", "title": "The standard confusion",
   "blurb": "Named, so you can recognise it."},

  {"t": "callout", "title": "Rotating the object and rotating the frame are inverse operations that look identical",
   "kind": "Closing",
   "body": ["<b>Turning an object 30° left, and turning your head "
            "30° right, produce the same image</b> — <b>and the "
            "matrices are inverses of each other.</b>",
            "<b>So a sign error here does not crash</b>; <b>it "
            "produces a scene that moves the wrong way</b>, which is "
            "diagnosable only by knowing which operation you "
            "meant.",
            "<b>And the fix is the naming convention</b> "
            "(Part 2): <b>a matrix called "
            "<code>M_camera_from_world</code> cannot be applied in the "
            "wrong direction without the name looking "
            "wrong.</b>",
            "<b>Which is this module's practical "
            "deliverable</b> — <b>the idea is simple and the "
            "bookkeeping is where the time goes</b>, so fix the "
            "bookkeeping first."]},
 ],
 "takeaways": [
   "A change of basis is a dictionary, not a movement — nothing in the "
   "world moves.",
   "Build the matrix from the new basis vectors as columns; the "
   "construction is forced by what Mv means.",
   "Name it M_world_from_B, and the subscripts cancel like units.",
   "For an orthonormal basis the inverse is the transpose, which is why "
   "frames are built orthonormal deliberately.",
   "The view matrix is M_camera_from_world, which is the inverse of the "
   "camera's frame — and that is the whole derivation of lookAt.",
   "Rotating the object and rotating the frame are inverse operations that "
   "look identical on screen.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The setup"),
  ("callout", "The arrow does not change; only the numbers describing it do",
   ["<b>A point in a room has one position</b>, and <b>two people "
    "using different coordinate systems will assign it different "
    "numbers</b> — <b>and neither of them is wrong</b> "
    "(Module 02 &sect;1's two readings).",
    "<b>So a change of basis is a translation between two "
    "descriptions</b> — <b>a dictionary, not a movement</b> "
    "— and <b>nothing in the world moves when you apply one</b>, "
    "which is worth saying because the matrices look exactly like the "
    "ones that do move things.",
    "<b>Which is the distinction that causes all the trouble in "
    "this subject</b>: <b>rotating an object and rotating the frame you "
    "describe it in produce inverse matrices</b>, <b>and the two look "
    "identical on screen</b> (&sect;4).",
    "<b>And the view matrix is firmly the second kind</b> — "
    "<b>the camera does not move the world; it re-describes the world "
    "in its own coordinates</b> — <b>which is why &sect;3 exists "
    "and why <code>lookAt</code> contains an inverse.</b>"]),

  ("h1", "2 &nbsp; Building the matrix"),
  ("code", """SUPPOSE a basis B has vectors b1, b2, b3, each
written IN WORLD COORDINATES.

BUILD  M = [ b1 | b2 | b3 ]   (as columns)

THEN M takes B-coordinates TO world coordinates:
    v_world = M * v_B

WHY: v_B = (x,y,z) means "x of b1 plus y of b2 plus
z of b3" -- and M*v_B combines the columns with
exactly those weights (Module 03 section 1). So the
construction is forced; there is nothing to
remember.

AND THE OTHER DIRECTION is the inverse:
    v_B = M^-1 * v_world

THE DIRECTION CONVENTION, worth fixing once and
never rethinking:
    name the matrix M_world_from_B.
    Then M_world_from_B * v_B = v_world reads as
    cancellation, and
    M_world_from_B * M_B_from_camera is obviously
    M_world_from_camera."""),
  ("p", "<b>Name it <code>M_world_from_B</code></b> — <b>then "
        "the subscripts cancel like units and you can never compose two "
        "of them backwards</b>, because a mismatched pair is visible in "
        "the name before you run anything. <b>This naming convention "
        "eliminates the single most common error in the subject</b>, "
        "and it costs nothing but a habit. Gortler uses it; most "
        "graphics texts do not, which is why most graphics texts are "
        "confusing here."),
  ("callout", "And for an orthonormal basis the inverse is just the "
              "transpose, which is why frames are built orthonormal",
   ["<b>If the basis vectors are unit length and mutually "
    "perpendicular</b>, <b>the matrix is orthogonal and "
    "M<super>&minus;1</super> = M<super>T</super></b> — <b>which is "
    "free to compute and numerically exact</b>, with no division and no "
    "conditioning problem.",
    "<b>So camera frames, tangent frames, and skeleton bone frames "
    "are all built orthonormal deliberately</b> — <b>not for "
    "elegance, but because inverting them is then a transpose</b>, and "
    "inverting them is something you do constantly.",
    "<b>And it is exactly why Gram-Schmidt matters</b> "
    "(Module 05 &sect;4): <b>given any basis at all, it produces an "
    "orthonormal basis spanning the same space</b>, so you can always "
    "arrange to be in the easy case.",
    "<b>Plus the numerical point:</b> <b>a general matrix inverse "
    "accumulates floating-point error and a transpose does not</b> "
    "— <b>which matters in a loop running sixty times a "
    "second</b>, where drift compounds into visible skew."]),

  ("break",),
  ("h1", "3 &nbsp; The view matrix"),
  ("ul", ["<b>Build the camera's frame in world coordinates</b>: "
          "<b>a forward vector, a right vector, and an up vector, "
          "orthonormal</b> — <b>which is Module 05's cross "
          "products and normalisation</b>, and is where the handedness "
          "convention first bites (Module 06 &sect;3).",
          "<b>Those three vectors as columns give "
          "M_world_from_camera</b> (&sect;2) — the matrix taking "
          "camera-space coordinates to world-space ones.",
          "<b>But the pipeline wants the opposite</b>: <b>the view "
          "matrix is M_camera_from_world</b>, <b>which is the "
          "inverse</b> — <b>and because the frame is orthonormal, "
          "that inverse is simply the transpose</b> (&sect;2's "
          "callout).",
          "<b>Plus the translation</b>, which does not fit into a "
          "3&times;3 matrix at all and <b>is Module 07's "
          "subject</b> — <b>and which inverts by negating the "
          "camera's position, expressed in the rotated frame</b>.",
          "<b>Which is the entire derivation of <code>lookAt</code>, "
          "and it takes four lines once the convention is "
          "fixed</b> — <b>and it explains why every implementation "
          "of that function contains a transpose and a negated "
          "translation</b>, which is otherwise mysterious."]),

  ("h1", "4 &nbsp; The standard confusion"),
  ("callout", "Rotating the object and rotating the frame are inverse "
              "operations that look identical",
   ["<b>Turning an object thirty degrees to the left, and turning "
    "your head thirty degrees to the right, produce the same "
    "image</b> — <b>and the matrices that express them are "
    "inverses of one another.</b>",
    "<b>So a sign error here does not crash anything</b>; <b>it "
    "produces a scene that moves the wrong way when you drag the "
    "mouse</b>, <b>which is diagnosable only by knowing which of the "
    "two operations you meant to express</b> — and by then you are "
    "an hour in.",
    "<b>And the fix is the naming convention</b> "
    "(&sect;2): <b>a matrix called "
    "<code>M_camera_from_world</code> cannot be applied in the wrong "
    "direction without the name visibly disagreeing with the code "
    "around it</b>, which turns a runtime mystery into a reading "
    "error.",
    "<b>Which is this module's practical deliverable</b> — "
    "<b>the idea itself is simple and the bookkeeping is where all the "
    "time goes</b>, <b>so fix the bookkeeping first</b> and the idea "
    "stays simple."]),
 ],
 "resources": [
   ("3Blue1Brown, chapter 13 (free)",
    "https://www.3blue1brown.com/topics/linear-algebra",
    "<b>&sect;&sect;1 and 2</b> — change of basis, and the "
    "whose-coordinates question made visual."),
   ("Gortler, chapters 3 and 4 (library copy)",
    "https://mitpress.mit.edu/9780262017350/",
    "<b>The whole module</b> — and the frame-naming discipline of "
    "&sect;2 comes from here, which is why this book is "
    "recommended over the more popular ones."),
   ("MIT 18.06, the change of basis lecture (free video)",
    "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
    "<b>&sect;2</b> — the algebra, carefully."),
   ("Scratchapixel, the camera and lookAt articles (free)",
    "https://www.scratchapixel.com/",
    "<b>&sect;3</b> — the view matrix derived rather than presented, "
    "with code."),
 ],
 "exercises": [
   "<b>Write one arrow's coordinates</b> in two bases and convert "
   "between them.",
   "<b>Build a change of basis matrix</b> from three given "
   "vectors.",
   "<b>Verify v_world = M v_B</b> on several points.",
   "<b>Invert it</b> and check the round trip to tolerance.",
   "<b>Build an orthonormal basis</b> and confirm the inverse is the "
   "transpose.",
   "<b>Measure the error</b> of a general inverse versus a transpose "
   "over 10,000 compositions.",
   "<b>Adopt the from-naming convention</b> throughout your code.",
   "<b>Derive lookAt</b> from scratch, in four lines.",
   "<b>Compare yours</b> to a library implementation and account for "
   "every difference.",
   "<b>Deliberately invert the view matrix</b> and describe how the "
   "camera then behaves.",
 ],
 "selfcheck": [
   "What does a change of basis do, and what does it not do?",
   "Why do the two kinds of rotation look identical?",
   "How do you build the matrix, and why is the construction "
   "forced?",
   "State the naming convention and what it prevents.",
   "When is the inverse a transpose, and why does that matter?",
   "Why are frames built orthonormal?",
   "Derive the view matrix in four steps.",
   "Why does lookAt contain a transpose?",
   "What does a direction error here look like at runtime?",
   "What is this module's practical deliverable?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Dot Products and Projection",
 "subtitle": "The operation every shading calculation is made of.",
 "question": "Why does a dot product tell you about an angle?",
 "outcomes": [
     "Compute dot products and interpret them geometrically.",
     "Derive the projection formula.",
     "Explain orthogonality and orthonormal bases.",
     "Apply Gram-Schmidt.",
     "Recognise dot products in shading code.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Two definitions",
   "blurb": "Algebraic and geometric, and they agree."},

  {"t": "eq", "kicker": "Dot product", "title": "The same number, two ways",
   "eqs": [
     ("a · b = a₁b₁ + a₂b₂ + a₃b₃",
      "The algebraic definition: multiply componentwise and sum. "
      "Cheap, and tells you nothing by itself."),
     ("a · b = |a| |b| cos θ",
      "The geometric meaning. The equality of these two is the law "
      "of cosines, and it is worth proving once."),
     ("so for unit vectors, a · b IS the cosine",
      "Which is why normalised vectors are everywhere in shading: "
      "the dot product becomes the angle term directly."),
   ],
   "caption": "<b>For unit vectors the dot product is the "
              "cosine</b>, which is why shading code normalises "
              "everything before doing "
              "anything.",
   "note": "The agreement of the two definitions is the content; "
           "either alone is a formula."},

  {"t": "callout", "title": "And the sign alone answers the questions you ask most often",
   "kind": "Why this operation is everywhere",
   "body": ["<b>Positive means the angle is acute</b>; <b>zero means "
            "perpendicular</b>; <b>negative means obtuse</b> — and "
            "<b>you frequently need only that much.</b>",
            "<b>Is the light in front of this surface?</b> "
            "<b>n · l > 0.</b> <b>Is this face pointing toward the "
            "camera?</b> <b>n · v > 0</b> — which is backface "
            "culling.",
            "<b>Which is why the dot product appears in every "
            "shading model</b> — <b>Lambertian diffuse is literally "
            "max(0, n · l)</b>, and that is the whole "
            "formula.",
            "<b>And the clamp matters</b>: <b>a negative dot means "
            "the light is behind the surface</b>, and <b>without the "
            "max you get negative light</b>, which is the first bug "
            "everybody writes."]},

  {"t": "section", "label": "Part 2", "title": "Projection",
   "blurb": "Derived, not memorised."},

  {"t": "code", "kicker": "Projection", "title": "The shadow of one vector on another",
   "lang": "text", "code": """
  QUESTION: how much of a points along b?

  THE ANSWER has to be a multiple of b, say c*b,
  and the leftover (a - c*b) has to be perpendicular
  to b -- that is what "the component along b" means.

  SO IMPOSE IT:
      (a - c*b) . b = 0
      a.b - c (b.b) = 0
      c = (a . b) / (b . b)

  THEREFORE
      proj_b(a) = [ (a.b) / (b.b) ] * b

  AND IF b IS A UNIT VECTOR, b.b = 1, so
      proj_b(a) = (a . b) * b
  which is why everything gets normalised first.

  THE DERIVATION IS THREE LINES and it is worth
  redoing rather than recalling: the condition
  "leftover is perpendicular" IS the definition.
""",
   "caption": "<b>'The leftover is perpendicular' is the definition, "
              "and the formula follows in three lines</b> — which is "
              "why it never needs "
              "memorising.",
   "note": "This decomposition into parallel and perpendicular parts "
           "is used constantly in CSCE 649."},

  {"t": "section", "label": "Part 3", "title": "Orthogonality",
   "blurb": "And why orthonormal bases are worth the trouble."},

  {"t": "bullets", "kicker": "Orthonormal", "title": "What you get when the basis is orthonormal",
   "items": [
     "<b>Coordinates are just dot products</b> — "
     "<b>the i-th coordinate of v is v · eᵢ</b>, with no solve "
     "required, which is otherwise a linear system.",
     "",
     "<b>The inverse is the transpose</b> "
     "(Module 04 §2) — free, and numerically "
     "exact.",
     "",
     "<b>Lengths and angles are preserved</b> by the "
     "transform — <b>which is what makes a rotation a rotation</b> "
     "rather than a general linear map.",
     "",
     "<b>And decomposition is trivial</b>: <b>any vector is the "
     "sum of its projections onto the basis vectors</b>, which is "
     "Part 2 applied three times.",
     "",
     "<b>So the question is always: how do I get an orthonormal "
     "basis?</b> — and Gram-Schmidt is the "
     "answer.",
   ],
   "footnote": "<b>In an orthonormal basis, finding coordinates is "
               "three dot products instead of a linear solve</b> "
               "— which is the practical reason the condition is "
               "worth arranging."},

  {"t": "section", "label": "Part 4", "title": "Gram-Schmidt",
   "blurb": "Which is projection, applied repeatedly."},

  {"t": "callout", "title": "Take each vector, subtract its projections onto the ones already done, and normalise",
   "kind": "Closing",
   "body": ["<b>That is the entire algorithm</b> — <b>and each "
            "step is Part 2's projection</b>, so there is "
            "nothing new to learn.",
            "<b>Which gives you an orthonormal basis spanning the "
            "same space</b> — <b>so you can always arrange to be in "
            "Part 3's easy case.</b>",
            "<b>And the graphics use is constant:</b> <b>building a "
            "tangent frame around a surface normal for importance "
            "sampling</b> (CSCE 647 §07), or <b>re-orthonormalising a "
            "camera frame that has drifted.</b>",
            "<b>Plus the numerical caveat:</b> <b>the naive version "
            "loses orthogonality on nearly-dependent "
            "input</b> — <b>the modified version subtracts "
            "progressively and is what you should implement.</b>"]},
 ],
 "takeaways": [
   "For unit vectors the dot product is the cosine, which is why shading "
   "code normalises everything first.",
   "The sign alone answers most questions: in front, perpendicular, "
   "behind.",
   "Lambertian diffuse is literally max(0, n · l), and omitting the "
   "clamp gives negative light.",
   "'The leftover is perpendicular' is the definition of projection, and "
   "the formula follows in three lines.",
   "In an orthonormal basis, finding coordinates is three dot products "
   "instead of a linear solve.",
   "Gram-Schmidt is projection applied repeatedly, and the modified version "
   "is the one to implement.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Two definitions"),
  ("eq", "a &middot; b = a<sub>1</sub>b<sub>1</sub> + "
         "a<sub>2</sub>b<sub>2</sub> + a<sub>3</sub>b<sub>3</sub> "
         "&nbsp;&nbsp;=&nbsp;&nbsp; |a| |b| cos &theta;"),
  ("ul", ["<b>The algebraic definition is componentwise multiply and "
          "sum</b> — cheap to compute, and <b>it tells you nothing "
          "by itself</b> about what the number means.",
          "<b>The geometric meaning is |a||b|cos&theta;</b>, and "
          "<b>the equality of these two expressions is essentially the "
          "law of cosines</b> — <b>which is worth proving once</b>, "
          "because it is the bridge between the arrow picture and the "
          "coordinate arithmetic.",
          "<b>So for unit vectors, a &middot; b <i>is</i> the "
          "cosine of the angle between them</b> — <b>which is "
          "exactly why normalised vectors are everywhere in shading "
          "code</b>: the dot product becomes the angle term directly, "
          "with no trigonometry and no division.",
          "<b>The agreement of the two definitions is the content of "
          "this section; either one alone is just a formula</b>, and "
          "the whole usefulness of the operation comes from a cheap "
          "computation having a geometric meaning."]),
  ("callout", "And the sign alone answers the questions you ask most often",
   ["<b>Positive means the angle is acute</b>; <b>zero means exactly "
    "perpendicular</b>; <b>negative means obtuse</b> — and <b>you "
    "frequently need nothing more than that</b>, which makes the "
    "operation cheaper still.",
    "<b>Is the light in front of this surface?</b> "
    "<b>n &middot; l &gt; 0.</b> <b>Is this face pointing toward the "
    "camera?</b> <b>n &middot; v &gt; 0</b> — <b>which is backface "
    "culling</b>, and it is one dot product and one comparison per "
    "triangle.",
    "<b>Which is why the dot product appears in every shading "
    "model</b> — <b>Lambertian diffuse is literally "
    "max(0, n &middot; l) times the light colour</b>, <b>and that is "
    "the entire formula</b>, which surprises people who expected "
    "something more elaborate.",
    "<b>And the clamp matters</b>: <b>a negative dot product means "
    "the light is behind the surface</b>, and <b>without the max you "
    "get negative light</b> — which subtracts from other "
    "contributions and produces black rims. <b>This is the first bug "
    "everybody writes</b>, and it is worth writing once "
    "deliberately."]),

  ("h1", "2 &nbsp; Projection"),
  ("code", """QUESTION: how much of a points along b?

THE ANSWER has to be a multiple of b, say c*b, and
the leftover (a - c*b) has to be perpendicular to b
-- that is what "the component along b" means.

SO IMPOSE IT:
    (a - c*b) . b = 0
    a.b - c (b.b) = 0
    c = (a . b) / (b . b)

THEREFORE
    proj_b(a) = [ (a.b) / (b.b) ] * b

AND IF b IS A UNIT VECTOR, b.b = 1, so
    proj_b(a) = (a . b) * b
which is why everything gets normalised first.

THE DERIVATION IS THREE LINES and it is worth
redoing rather than recalling: the condition "the
leftover is perpendicular" IS the definition, and
everything else is algebra."""),
  ("p", "<b>'The leftover is perpendicular' is the definition, and "
        "the formula follows in three lines</b> — <b>which is why "
        "it never needs memorising</b>, and why getting it slightly "
        "wrong from memory is avoidable. <b>This decomposition of a "
        "vector into a part along b and a part perpendicular to it is "
        "used constantly in CSCE 649</b>: a collision response splits "
        "velocity into normal and tangential components and treats them "
        "differently, which is this formula twice."),

  ("break",),
  ("h1", "3 &nbsp; Orthogonality"),
  ("ul", ["<b>Coordinates become plain dot products</b> — "
          "<b>the i-th coordinate of v is v &middot; e<sub>i</sub></b>, "
          "<b>with no linear system to solve</b>, which in a general "
          "basis would require a solve or a stored inverse.",
          "<b>The inverse of the basis matrix is its transpose</b> "
          "(Module 04 &sect;2) — free to compute, and "
          "numerically exact rather than approximately "
          "correct.",
          "<b>Lengths and angles are preserved by the "
          "transform</b> — <b>which is precisely what makes a "
          "rotation a rotation</b> rather than a general invertible map, "
          "and is the property Module 09 &sect;3 detects with a "
          "determinant.",
          "<b>And decomposition becomes trivial</b>: <b>any vector "
          "is the sum of its projections onto the basis vectors</b>, "
          "<b>which is &sect;2 applied three times</b> and no more "
          "difficult than that.",
          "<b>So the question is always: how do I get an orthonormal "
          "basis in the first place?</b> — and <b>Gram-Schmidt is "
          "the answer</b> (&sect;4). <b>Finding coordinates in an "
          "orthonormal basis is three dot products instead of a linear "
          "solve</b>, which is the practical reason the condition is "
          "worth arranging deliberately."]),

  ("h1", "4 &nbsp; Gram-Schmidt"),
  ("callout", "Take each vector, subtract its projections onto the ones "
              "already done, and normalise",
   ["<b>That is the entire algorithm</b> — process the vectors "
    "in order, each time removing whatever part lies in the span of the "
    "ones already processed — <b>and each removal step is "
    "&sect;2's projection</b>, <b>so there is nothing new to "
    "learn</b>.",
    "<b>Which gives you an orthonormal basis spanning exactly the "
    "same space as the one you started with</b> — <b>so you can "
    "always arrange to be in &sect;3's easy case</b>, at the cost of a "
    "few dot products.",
    "<b>And the graphics use is constant:</b> <b>building a tangent "
    "frame around a surface normal for importance sampling</b> "
    "(CSCE 647 Module 07, where you need an orthonormal basis with "
    "the normal as one axis and do not care which two vectors fill out "
    "the rest), or <b>re-orthonormalising a camera or bone frame that "
    "has drifted from accumulated error</b> (Module 04 &sect;2's "
    "numerical point).",
    "<b>Plus the numerical caveat:</b> <b>the naive formulation "
    "loses orthogonality badly on nearly-dependent input</b>, because "
    "the subtractions are all computed against the original "
    "vectors — <b>the modified version subtracts progressively, "
    "updating as it goes, and is what you should actually "
    "implement</b>."]),
 ],
 "resources": [
   ("3Blue1Brown, chapter 9 (free)",
    "https://www.3blue1brown.com/topics/linear-algebra",
    "<b>&sect;1</b> — the dot product's two definitions and why they "
    "agree, made visual."),
   ("MIT 18.06, the orthogonality lectures (free video)",
    "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
    "<b>&sect;&sect;2 to 4</b> — projection, orthonormal bases, and "
    "Gram-Schmidt, with the least-squares connection previewed "
    "(Module 12)."),
   ("Immersive Math, chapter 4 (free)",
    "http://immersivemath.com/ila/",
    "<b>&sect;&sect;1 and 2</b> — drag the vectors and watch the "
    "projection follow."),
   ("Pharr, Jakob & Humphreys &mdash; PBRT, the sampling chapters "
    "(free online)",
    "https://pbr-book.org/",
    "<b>&sect;4's graphics use</b> — orthonormal frames around a "
    "normal, which is CSCE 647's version of this material."),
 ],
 "exercises": [
   "<b>Compute ten dot products</b> and predict each sign first.",
   "<b>Prove the two definitions agree</b>, via the law of "
   "cosines.",
   "<b>Implement backface culling</b> with a single dot product.",
   "<b>Implement Lambertian shading</b>, and then remove the clamp "
   "and look at the result.",
   "<b>Derive the projection formula</b> from the perpendicularity "
   "condition.",
   "<b>Decompose a vector</b> into parallel and perpendicular parts "
   "relative to another.",
   "<b>Find coordinates in an orthonormal basis</b> by dot "
   "products, and verify against a solve.",
   "<b>Implement Gram-Schmidt</b>, naive and modified.",
   "<b>Feed both nearly-dependent input</b> and measure the "
   "orthogonality loss.",
   "<b>Build a tangent frame</b> around an arbitrary normal.",
 ],
 "selfcheck": [
   "Give both definitions of the dot product and say why they "
   "agree.",
   "What is the dot product of two unit vectors?",
   "What does the sign tell you, and name two uses.",
   "Write the Lambertian formula and explain the clamp.",
   "Derive the projection formula from perpendicularity.",
   "What does it simplify to for a unit vector?",
   "Name four things an orthonormal basis buys you.",
   "How do you find coordinates in one?",
   "Describe Gram-Schmidt in one sentence.",
   "What is the numerical caveat, and what should you implement?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Cross Products and Normals",
 "subtitle": "Perpendicularity, area, and the handedness trap.",
 "question": "Which way does the normal point?",
 "outcomes": [
     "Compute cross products and interpret them.",
     "Compute face normals from a triangle.",
     "Explain handedness and winding order.",
     "Explain why normals transform by the inverse transpose.",
     "Debug a normal that points the wrong way.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What it gives you",
   "blurb": "Three things at once."},

  {"t": "callout", "title": "The cross product returns a vector perpendicular to both, with length equal to the parallelogram's area",
   "kind": "Three facts in one operation",
   "body": ["<b>Direction: perpendicular to both inputs</b> — which "
            "is what you want for a surface normal.",
            "<b>Magnitude: |a||b| sin θ</b> — <b>the area of the "
            "parallelogram they span</b>, and <b>half of it is the "
            "triangle's area</b>, which is how mesh "
            "areas get computed.",
            "<b>And it is zero exactly when the inputs are "
            "parallel</b> — <b>which is the degenerate-triangle "
            "test</b> (Module 02 §2) and is "
            "worth checking before "
            "normalising.",
            "<b>Plus: it is anticommutative</b>, "
            "<b>a × b = −(b × a)</b> — which is where handedness "
            "enters and is Part 3's subject."]},

  {"t": "section", "label": "Part 2", "title": "Face normals",
   "blurb": "The computation, and the two things that go wrong."},

  {"t": "code", "kicker": "Normals", "title": "From three vertices to a unit normal",
   "lang": "text", "code": """
  GIVEN a triangle with vertices p0, p1, p2:

      e1 = p1 - p0
      e2 = p2 - p0
      n  = cross(e1, e2)
      area = 0.5 * length(n)
      n  = normalize(n)

  TWO THINGS GO WRONG

  1  DEGENERATE TRIANGLE
         if p0, p1, p2 are collinear, n is the zero
         vector and normalize() divides by zero.
         CHECK length(n) before normalising -- this
         is not paranoia, real meshes contain these.

  2  WINDING ORDER
         cross(e1, e2) and cross(e2, e1) point
         opposite ways. Which one is "outward"
         depends on the order the vertices are
         listed in, which is a mesh convention.
         Counter-clockwise-is-front is the usual
         choice. PICK ONE AND WRITE IT DOWN.

  AND VERTEX NORMALS are the normalised average of
  the face normals around a vertex -- which is why
  a mesh with inconsistent winding shades wrongly.
""",
   "caption": "<b>Check the length before normalising</b> — real "
              "meshes contain degenerate triangles, and the NaN "
              "propagates silently through everything "
              "downstream.",
   "note": "Inconsistent winding is the usual cause of a mesh that "
           "shades in patches."},

  {"t": "section", "label": "Part 3", "title": "Handedness",
   "blurb": "The convention, and why it causes so much trouble."},

  {"t": "callout", "title": "The cross product's direction is a convention, and mixing conventions is the commonest bug in graphics",
   "kind": "The trap this module exists to prevent",
   "body": ["<b>Right-handed: point the fingers along a, curl toward "
            "b, and the thumb gives a × b.</b> <b>Left-handed systems "
            "reverse it</b> — and both are "
            "self-consistent.",
            "<b>And the conventions genuinely differ in "
            "practice</b>: <b>OpenGL and most mathematics are "
            "right-handed; DirectX and some engines are "
            "left-handed</b>, which is a historical accident you "
            "inherit.",
            "<b>So the bug is mixing them</b> — <b>importing a mesh "
            "built under one convention into a renderer using the "
            "other</b> — and <b>the symptom is normals inverted, or "
            "the scene mirrored.</b>",
            "<b>Which is why the rule is: choose once, write it "
            "down, and check it at every boundary</b> — <b>import, "
            "export, and any library call</b> — because nothing will "
            "warn you."]},

  {"t": "section", "label": "Part 4", "title": "Transforming normals",
   "blurb": "Which is not what you expect, and the reason is "
            "geometric."},

  {"t": "eq", "kicker": "Normal matrix", "title": "Why normals use the inverse transpose",
   "eqs": [
     ("a normal is defined by n · v = 0 for v in the surface",
      "It is perpendicular to the surface — which is a condition "
      "relating it to the tangent vectors, not an independent "
      "direction."),
     ("after transforming tangents by M, perpendicularity must survive",
      "We need n' · (Mv) = 0 whenever n · v = 0. Writing it "
      "out forces n' = (M⁻¹)ᵀ n."),
     ("and for a rotation, (M⁻¹)ᵀ = M — so nothing changes",
      "Which is why the issue only appears under non-uniform scale, "
      "and why it surprises people who only ever rotated things."),
   ],
   "caption": "<b>Under non-uniform scale, transforming a normal by "
              "M tilts it off the surface</b> — the inverse "
              "transpose is what keeps it "
              "perpendicular.",
   "note": "This is Module 01 §2's surprising row, and the "
           "explanation is geometric rather than "
           "algebraic."},

  {"t": "callout", "title": "And the debugging procedure for a wrong normal",
   "kind": "Closing",
   "body": ["<b>Draw it.</b> <b>Render the normals as short line "
            "segments</b> — <b>which turns an invisible bug into an "
            "obvious one</b>, and takes ten minutes to "
            "implement.",
            "<b>Then check, in order:</b> <b>winding order, "
            "handedness convention, whether you used the inverse "
            "transpose, and whether you normalised after "
            "transforming</b>.",
            "<b>That last one is easy to miss</b>: <b>a transform "
            "can change a unit normal's length</b>, and the shading will "
            "be subtly wrong rather than obviously "
            "broken.",
            "<b>Which is four causes</b>, and <b>in this program's "
            "experience it is nearly always one of them</b> — so the "
            "list is worth keeping."]},
 ],
 "takeaways": [
   "The cross product gives direction, area, and a degeneracy test in one "
   "operation.",
   "Check the length before normalising — real meshes contain "
   "degenerate triangles and the NaN propagates silently.",
   "Which way is 'outward' depends on winding order, which is a mesh "
   "convention you must pick and write down.",
   "Mixing handedness conventions is the commonest bug in graphics, and "
   "nothing warns you.",
   "Normals transform by the inverse transpose, because perpendicularity "
   "must survive the transform.",
   "Under a pure rotation the inverse transpose equals M, which is why the "
   "issue only appears with non-uniform scale.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What it gives you"),
  ("callout", "The cross product returns a vector perpendicular to both, with "
              "length equal to the parallelogram's area",
   ["<b>Direction: perpendicular to both inputs</b> — which is "
    "exactly what you want for a surface normal, and is the use that "
    "dominates in graphics.",
    "<b>Magnitude: |a||b| sin &theta;</b> — <b>the area of the "
    "parallelogram the two vectors span</b>, and <b>half of that is the "
    "triangle's area</b>, <b>which is how mesh surface areas and "
    "barycentric weights get computed</b> without any trigonometry.",
    "<b>And it is the zero vector exactly when the inputs are "
    "parallel</b> — <b>which is the degenerate-triangle test</b> "
    "(Module 02 &sect;2's linear dependence) and <b>is worth "
    "checking before you normalise</b> (&sect;2).",
    "<b>Plus it is anticommutative</b>: <b>a &times; b = "
    "&minus;(b &times; a)</b> — <b>which is where handedness "
    "enters</b> and is &sect;3's subject. Note it is also not "
    "associative, so parenthesise."]),

  ("h1", "2 &nbsp; Face normals"),
  ("code", """GIVEN a triangle with vertices p0, p1, p2:

    e1 = p1 - p0
    e2 = p2 - p0
    n  = cross(e1, e2)
    area = 0.5 * length(n)
    n  = normalize(n)

TWO THINGS GO WRONG

1  DEGENERATE TRIANGLE
       if p0, p1, p2 are collinear then n is the
       zero vector and normalize() divides by zero.
       CHECK length(n) before normalising -- this is
       not paranoia, real meshes contain these, and
       the resulting NaN propagates silently into
       every lighting calculation downstream.

2  WINDING ORDER
       cross(e1, e2) and cross(e2, e1) point
       opposite ways. Which one counts as "outward"
       depends on the order the vertices are listed
       in, which is a mesh convention.
       Counter-clockwise-is-front is the usual
       choice. PICK ONE AND WRITE IT DOWN.

AND VERTEX NORMALS are the normalised average of the
face normals meeting at that vertex."""),
  ("p", "<b>Check the length before normalising</b> — <b>real "
        "meshes contain degenerate triangles</b> (exported from CAD, "
        "produced by decimation, or simply authored badly) <b>and the "
        "NaN propagates silently through everything downstream</b>, "
        "producing black or invisible geometry far from the actual "
        "fault. <b>Inconsistent winding is the usual cause of a mesh "
        "that shades in patches</b> — some faces lit and their "
        "neighbours dark — because the averaged vertex normals "
        "partially cancel."),

  ("break",),
  ("h1", "3 &nbsp; Handedness"),
  ("callout", "The cross product's direction is a convention, and mixing "
              "conventions is the commonest bug in graphics",
   ["<b>Right-handed: point the fingers of your right hand along a, "
    "curl them toward b, and your thumb gives the direction of "
    "a &times; b.</b> <b>Left-handed systems reverse it</b> — and "
    "<b>both are entirely self-consistent</b>, which is why neither can "
    "be called wrong.",
    "<b>And the conventions genuinely differ in practice</b>: "
    "<b>OpenGL and essentially all mathematics are right-handed; "
    "DirectX and several engines are left-handed</b> — <b>which is "
    "a historical accident that you inherit</b> and cannot "
    "avoid.",
    "<b>So the bug is mixing them</b> — <b>importing a mesh "
    "authored under one convention into a renderer that assumes the "
    "other</b>, or calling a library function that disagrees with your "
    "own code — and <b>the symptom is normals inverted, faces "
    "culled backwards, or the whole scene mirrored.</b>",
    "<b>Which is why the rule is: choose once, write it down "
    "somewhere visible, and check it at every boundary</b> — "
    "<b>every import, every export, and every library call</b> "
    "— <b>because nothing will warn you</b> and the numbers are "
    "valid either way."]),

  ("h1", "4 &nbsp; Transforming normals"),
  ("eq", "need n&prime; &middot; (Mv) = 0 whenever n &middot; v = 0 "
         "&nbsp;&rArr;&nbsp; n&prime; = "
         "(M<super>&minus;1</super>)<super>T</super> n"),
  ("ul", ["<b>A normal is not an independent direction</b>: <b>it is "
          "defined by being perpendicular to the surface</b>, which is a "
          "condition relating it to the tangent vectors rather than a "
          "property it carries on its own.",
          "<b>So after the tangent vectors are transformed by M, the "
          "perpendicularity must survive</b> — we need the "
          "transformed normal to be perpendicular to the transformed "
          "tangents — <b>and writing that condition out forces "
          "n&prime; = (M<super>&minus;1</super>)<super>T</super> n</b>, "
          "with no freedom in the matter.",
          "<b>And for a pure rotation, "
          "(M<super>&minus;1</super>)<super>T</super> = M</b> (since "
          "M<super>&minus;1</super> = M<super>T</super> for an "
          "orthogonal matrix, Module 04 &sect;2) — <b>so nothing "
          "changes</b>, <b>which is why the issue only appears under "
          "non-uniform scale</b> and <b>why it surprises people who have "
          "only ever rotated things.</b>",
          "<b>Under non-uniform scale, transforming a normal by M "
          "tilts it off the surface</b> — squash a sphere into an "
          "ellipsoid and the naively-transformed normals no longer point "
          "away from it — <b>and the inverse transpose is exactly "
          "what keeps it perpendicular</b>. <b>This is Module 01 "
          "&sect;2's surprising row, and the explanation is geometric "
          "rather than algebraic.</b>"]),
  ("callout", "And the debugging procedure for a wrong normal",
   ["<b>Draw it.</b> <b>Render the normals as short line segments "
    "from each vertex or face centre</b> — <b>which turns an "
    "invisible bug into an obvious one</b>, <b>and takes about ten "
    "minutes to implement</b> and pays for itself "
    "immediately.",
    "<b>Then check, in this order:</b> <b>the winding order "
    "(&sect;2), the handedness convention (&sect;3), whether you used "
    "the inverse transpose (&sect;4), and whether you normalised "
    "<i>after</i> transforming rather than before.</b>",
    "<b>That last one is easy to miss</b>: <b>a transform can "
    "change a unit normal's length</b> even when the direction is "
    "handled correctly, <b>and the shading will then be subtly wrong "
    "rather than obviously broken</b> — too bright or too dark in a "
    "way that reads as an art problem.",
    "<b>Which is four causes</b>, and <b>in this program's "
    "experience it is nearly always one of them</b> — <b>so the "
    "list is worth keeping</b> next to the renderer."]),
 ],
 "resources": [
   ("3Blue1Brown, chapters 10 and 11 (free)",
    "https://www.3blue1brown.com/topics/linear-algebra",
    "<b>&sect;1</b> — the cross product, including the determinant "
    "connection that Module 09 develops."),
   ("Lengyel, chapters 1 and 4 (library copy)",
    "https://www.cengage.com/c/mathematics-for-3d-game-programming-and-computer-graphics-3e-lengyel/",
    "<b>&sect;&sect;2 to 4</b> — normals, winding, and the normal "
    "matrix, in graphics conventions."),
   ("Scratchapixel, the normals and shading articles (free)",
    "https://www.scratchapixel.com/",
    "<b>&sect;&sect;2 and 4</b> — with the inverse transpose derived "
    "rather than asserted."),
   ("The OpenGL and DirectX coordinate system documentation (free)",
    "https://www.khronos.org/opengl/wiki/Viewing_and_Transformations",
    "<b>&sect;3</b> — the two conventions stated by their own "
    "specifications, which is the authoritative source when they "
    "disagree."),
 ],
 "exercises": [
   "<b>Compute five cross products</b> and verify perpendicularity by "
   "dot product.",
   "<b>Verify the area interpretation</b> against a known "
   "triangle.",
   "<b>Construct a degenerate triangle</b> and watch normalise "
   "produce NaN.",
   "<b>Add the length check</b> and handle it.",
   "<b>Reverse a triangle's winding</b> and observe the normal "
   "flip.",
   "<b>State your handedness convention</b> and find where your tools "
   "disagree.",
   "<b>Transform a normal by a non-uniform scale</b>, both ways, and "
   "compare.",
   "<b>Derive the inverse transpose</b> from the perpendicularity "
   "condition.",
   "<b>Implement normal visualisation</b> as line segments.",
   "<b>Introduce each of the four bugs deliberately</b> and learn "
   "what each looks like.",
 ],
 "selfcheck": [
   "What three things does a cross product give you?",
   "When is it zero, and what does that mean for a mesh?",
   "Give the face normal computation.",
   "Name the two things that go wrong, and the fix for each.",
   "What determines which way is outward?",
   "State the handedness conventions and who uses which.",
   "What does mixing them look like?",
   "Why do normals use the inverse transpose?",
   "When does it not matter, and why?",
   "Give the four-item debugging list.",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Homogeneous Coordinates",
 "subtitle": "A fourth number that makes translation linear.",
 "question": "Why does a 3D point have four coordinates?",
 "outcomes": [
     "Explain why translation needs an extra dimension.",
     "Use homogeneous coordinates for points and directions.",
     "Build affine transform matrices.",
     "Explain the perspective divide.",
     "Distinguish points from directions correctly.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "Translation does not fit, and that is a real obstacle."},

  {"t": "callout", "title": "Every linear map fixes the origin, so translation cannot be a matrix — in three dimensions",
   "kind": "The obstacle, and the shape of the trick",
   "body": ["<b>T(0) = T(0 · v) = 0 · T(v) = 0</b> — <b>so a "
            "linear map always sends the origin to the "
            "origin</b> (Module 03 §4), and translation does "
            "not.",
            "<b>Which would mean carrying transforms as a matrix "
            "<i>and</i> a vector</b>, composing them separately, "
            "forever — <b>workable, ugly, and error-prone.</b>",
            "<b>The trick: embed 3D space as the plane w = 1 inside "
            "4D</b> — <b>and a shear in 4D restricted to that plane is "
            "a translation in 3D.</b>",
            "<b>So translation <i>is</i> linear, one dimension "
            "up</b> — <b>which is a genuinely elegant move</b> and is "
            "why every graphics matrix is 4×4."]},

  {"t": "section", "label": "Part 2", "title": "Points and directions",
   "blurb": "The distinction the fourth coordinate encodes."},

  {"t": "code", "kicker": "w", "title": "What the fourth number means",
   "lang": "text", "code": """
  A POINT has w = 1.        (x, y, z, 1)
  A DIRECTION has w = 0.    (x, y, z, 0)

  AND THE ARITHMETIC THEN WORKS OUT CORRECTLY:
      point - point     = direction   (1-1 = 0)
      point + direction = point       (1+0 = 1)
      direction + direction = direction
      point + point     = w of 2 -- meaningless,
                          and the w tells you so

  WHY IT MATTERS FOR TRANSFORMS
      the translation column multiplies w.
      A point (w=1) gets translated.
      A direction (w=0) does NOT -- which is
      correct: translating a direction is
      meaningless, and the convention handles it
      automatically.

  SO LIGHT DIRECTIONS GET w = 0, and vertices
  get w = 1, and translation needs no branch.

  NORMALS ALSO TAKE w = 0, but that settles only
  translation. Their 3x3 part still needs the
  inverse transpose of Module 06 -- w = 0 does
  not rescue a normal under non-uniform scale.
""",
   "caption": "<b>A direction has w = 0, so translation ignores "
              "it</b> — which is correct and automatic, and is why "
              "the convention is worth "
              "following.",
   "note": "Storing a direction with w = 1 is a real bug and it "
           "translates your light vectors."},

  {"t": "section", "label": "Part 3", "title": "Affine transforms",
   "blurb": "Linear plus translation, in one matrix."},

  {"t": "callout", "title": "The 4×4 is a 3×3 linear part, a translation column, and a bottom row that is usually (0,0,0,1)",
   "kind": "The structure to recognise",
   "body": ["<b>Top-left 3×3: rotation, scale, shear</b> — "
            "everything from Module 03.",
            "<b>Fourth column: the translation</b> — <b>which is "
            "where the object's position lives</b>, and is the first "
            "thing to read when inspecting an unfamiliar "
            "matrix.",
            "<b>Bottom row (0,0,0,1) means affine</b> — <b>parallel "
            "lines stay parallel</b> — and <b>anything else in that row "
            "is a projection</b>, which is "
            "Part 4.",
            "<b>So you can read a 4×4 at a glance</b>: <b>linear "
            "part, position, and whether it is affine or "
            "projective</b> — three things, from the "
            "layout."]},

  {"t": "section", "label": "Part 4", "title": "The perspective divide",
   "blurb": "Where w stops being 1 and starts doing work."},

  {"t": "bullets", "kicker": "Perspective", "title": "How division by depth becomes a matrix operation",
   "items": [
     "<b>Perspective means dividing by distance</b> — "
     "<b>things twice as far appear half as large</b> — and "
     "<b>division is not a linear operation</b>.",
     "",
     "<b>But a matrix can put the depth into w</b> — <b>a "
     "bottom row of (0,0,−1,0) copies −z into w</b> — and then "
     "the divide happens afterwards.",
     "",
     "<b>So the projection matrix does not project</b>: "
     "<b>it sets up a division that the hardware performs "
     "next</b>, which is why the operation is called the perspective "
     "divide and is a separate stage.",
     "",
     "<b>Which is the piece people find mysterious</b>, and it is "
     "one row of one matrix plus one division.",
     "",
     "<b>And it explains the near plane</b>: <b>as z approaches "
     "zero, w approaches zero, and the divide explodes</b> — "
     "which is why there is a near clip plane at all.",
   ],
   "footnote": "<b>The projection matrix does not project; it sets "
               "up a division</b> — which is the sentence that makes "
               "Module 08 straightforward."},

  {"t": "callout", "title": "And this is the idea the whole pipeline depends on",
   "kind": "Closing",
   "body": ["<b>One extra coordinate makes translation linear and "
            "makes perspective expressible</b> — <b>two problems, one "
            "trick</b>, which is why it is worth understanding rather "
            "than accepting.",
            "<b>And it is the reason every transform in graphics is "
            "4×4</b>, including the ones that are obviously "
            "3D.",
            "<b>Plus the practical rule:</b> <b>w = 1 for points, "
            "w = 0 for directions, and check it whenever something is "
            "translated that should not have been.</b>",
            "<b>Which is Module 08's prerequisite</b> — "
            "<b>that module derives the projection matrix, and this is "
            "the machinery it needs.</b>"]},
 ],
 "takeaways": [
   "Every linear map fixes the origin, so translation cannot be a matrix in "
   "three dimensions.",
   "Embed 3D as the plane w = 1 in 4D, and a 4D shear becomes a 3D "
   "translation.",
   "A point has w = 1 and a direction has w = 0, so translation ignores "
   "directions automatically.",
   "A 4×4 reads as: linear part, translation column, and a bottom row "
   "saying affine or projective.",
   "The projection matrix does not project; it sets up a division the "
   "hardware performs next.",
   "As z approaches zero w approaches zero and the divide explodes, which "
   "is why there is a near clip plane.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The problem"),
  ("callout", "Every linear map fixes the origin, so translation cannot be a "
              "matrix — in three dimensions",
   ["<b>T(0) = T(0 &middot; v) = 0 &middot; T(v) = 0</b> — "
    "<b>so a linear map always sends the origin to the origin</b> "
    "(Module 03 &sect;4), <b>and translation manifestly does "
    "not</b>. This is a proof, not an inconvenience.",
    "<b>Which would mean carrying every transform as a matrix "
    "<i>and</i> a separate vector</b>, composing the two parts by "
    "different rules, forever — <b>workable, ugly, and "
    "error-prone</b>, and it is what you have to do in systems that "
    "lack this trick.",
    "<b>The trick: embed three-dimensional space as the plane "
    "w = 1 inside a four-dimensional space</b> — <b>and a shear in "
    "4D, restricted to that plane, is exactly a translation in "
    "3D</b>.",
    "<b>So translation <i>is</i> a linear map, one dimension "
    "up</b> — <b>which is a genuinely elegant move</b> rather than "
    "a bookkeeping convenience, <b>and is why every graphics transform "
    "matrix is 4&times;4</b> even though the geometry is "
    "three-dimensional."]),

  ("h1", "2 &nbsp; Points and directions"),
  ("code", """A POINT has w = 1.        (x, y, z, 1)
A DIRECTION has w = 0.    (x, y, z, 0)

AND THE ARITHMETIC THEN WORKS OUT CORRECTLY:
    point - point     = direction   (1 - 1 = 0)
    point + direction = point       (1 + 0 = 1)
    direction + direction = direction
    point + point     = w of 2 -- which is
                        meaningless, and the w
                        tells you so

WHY IT MATTERS FOR TRANSFORMS
    the translation column of the matrix multiplies
    w. A point (w=1) therefore gets translated. A
    direction (w=0) does NOT -- which is correct,
    since translating a direction is meaningless,
    and the convention handles it automatically
    with no special case.

SO LIGHT DIRECTIONS GET w = 0, and vertices get
w = 1, and translation needs no branch.

NORMALS ALSO TAKE w = 0, but that settles only
translation. Their 3x3 part still needs the
inverse transpose of Module 06 -- w = 0 does
not rescue a normal under non-uniform scale."""),
  ("p", "<b>A direction has w = 0, so translation ignores it</b> "
        "— <b>which is correct and automatic, and is why the "
        "convention is worth following</b> rather than storing "
        "everything as w = 1 and remembering which is which. <b>Storing "
        "a direction with w = 1 is a real bug and it translates your "
        "light vectors</b>: the lighting then changes as the object "
        "moves, which looks like an entirely different problem."),

  ("break",),
  ("h1", "3 &nbsp; Affine transforms"),
  ("callout", "The 4&times;4 is a 3&times;3 linear part, a translation "
              "column, and a bottom row that is usually (0,0,0,1)",
   ["<b>The top-left 3&times;3 block is rotation, scale, and "
    "shear</b> — everything from Module 03, unchanged and "
    "composing as before.",
    "<b>The fourth column is the translation</b> — <b>which is "
    "where the object's position lives</b>, <b>and is the first thing "
    "to read when inspecting an unfamiliar matrix in a debugger</b>: if "
    "the object is in the wrong place, look there first.",
    "<b>A bottom row of (0, 0, 0, 1) means the transform is "
    "affine</b> — <b>parallel lines stay parallel, and w is left "
    "alone</b> — <b>and anything else in that row makes it a "
    "projective transform</b>, which is &sect;4.",
    "<b>So you can read a 4&times;4 at a glance</b>: <b>the linear "
    "part, the position, and whether it is affine or "
    "projective</b> — <b>three things, directly from the "
    "layout</b>, which makes matrix debugging far less opaque than it "
    "first appears."]),

  ("h1", "4 &nbsp; The perspective divide"),
  ("ul", ["<b>Perspective means dividing by distance</b> — "
          "<b>something twice as far away appears half as large</b> "
          "— and <b>division is not a linear operation</b>, so no "
          "matrix can perform it.",
          "<b>But a matrix can arrange for the depth to end up in "
          "the w component</b> — <b>a bottom row of "
          "(0, 0, &minus;1, 0) copies &minus;z into w</b> — and "
          "<b>the division then happens as a separate step "
          "afterwards</b>, dividing x, y, and z by w.",
          "<b>So the projection matrix does not project</b>: "
          "<b>it sets up a division that the hardware performs in the "
          "next stage</b> — <b>which is why that stage is called "
          "the perspective divide and is listed separately in every "
          "pipeline diagram.</b>",
          "<b>Which is the piece of the pipeline people find most "
          "mysterious</b>, and it is <b>one row of one matrix plus one "
          "division</b>, which is considerably less than its reputation "
          "suggests.",
          "<b>And it explains the near clip plane</b>: <b>as z "
          "approaches zero, w approaches zero, and the divide "
          "explodes</b> — <b>which is why there is a near plane at "
          "all</b>, and why putting it very close to the camera "
          "destroys depth precision (Module 08 &sect;3). <b>'The "
          "projection matrix does not project; it sets up a division' is "
          "the sentence that makes Module 08 straightforward.</b>"]),
  ("callout", "And this is the idea the whole pipeline depends on",
   ["<b>One extra coordinate makes translation linear and makes "
    "perspective expressible</b> — <b>two separate problems solved "
    "by one trick</b>, <b>which is why it is worth understanding rather "
    "than accepting as a convention</b>.",
    "<b>And it is the reason every transform matrix in graphics is "
    "4&times;4</b>, including the ones that are doing nothing but "
    "rotating something in three dimensions.",
    "<b>Plus the practical rule:</b> <b>w = 1 for points, w = 0 for "
    "directions, and check it whenever something gets translated that "
    "should not have been</b> — which is a two-second diagnosis "
    "for a class of bug that otherwise looks mysterious.",
    "<b>Which is Module 08's prerequisite</b> — <b>that module "
    "derives the projection matrix from scratch, and this is the entire "
    "machinery it needs.</b>"]),
 ],
 "resources": [
   ("Gortler, chapters 3 and 11 (library copy)",
    "https://mitpress.mit.edu/9780262017350/",
    "<b>&sect;&sect;1 to 3</b> — points versus directions treated "
    "properly, which most texts blur."),
   ("Scratchapixel, the homogeneous coordinates article (free)",
    "https://www.scratchapixel.com/",
    "<b>&sect;&sect;1 and 4</b> — free, with the perspective divide "
    "derived step by step."),
   ("Lengyel, chapter 4 (library copy)",
    "https://www.cengage.com/c/mathematics-for-3d-game-programming-and-computer-graphics-3e-lengyel/",
    "<b>&sect;3</b> — the 4&times;4 structure in engine "
    "conventions."),
   ("Hartley & Zisserman, chapter 2 (library copy)",
    "https://www.robots.ox.ac.uk/~vgg/hzbook/",
    "<b>&sect;4 rigorously</b> — projective geometry properly, which "
    "is what CSCE 753 will want."),
 ],
 "exercises": [
   "<b>Prove that a linear map fixes the origin.</b>",
   "<b>Show that no 3×3 matrix can translate.</b>",
   "<b>Build a 4×4 translation matrix</b> and verify it on "
   "points.",
   "<b>Apply it to a direction (w = 0)</b> and confirm nothing "
   "happens.",
   "<b>Store a direction as w = 1 deliberately</b> and watch the "
   "lighting change as the object moves.",
   "<b>Read three unfamiliar 4×4 matrices</b> and state the "
   "linear part, position, and type of each.",
   "<b>Build a matrix that copies −z into w.</b>",
   "<b>Apply it and perform the divide by hand</b> on several "
   "points.",
   "<b>Plot apparent size against distance</b> and confirm the "
   "reciprocal.",
   "<b>Move the near plane very close</b> and observe what happens to "
   "depth precision.",
 ],
 "selfcheck": [
   "Why can translation not be a 3×3 matrix?",
   "What is the trick, stated geometrically?",
   "What do w = 1 and w = 0 mean?",
   "Why does point minus point give a direction?",
   "Why does translation ignore directions automatically?",
   "Describe the four parts of a 4×4 affine matrix.",
   "What does the bottom row tell you?",
   "Why is perspective not a linear operation?",
   "What does the projection matrix actually do?",
   "Why is there a near clip plane?",
 ],
},

]
