# -*- coding: utf-8 -*-
"""UC LINA 600 Linear Algebra for Graphics — program prerequisite."""

COURSE = {
    "code": "UC LINA 600",
    "title": "Linear Algebra for Graphics",
    "tagline": "The graphics pipeline is linear algebra, so this is "
               "not background — it is the subject",
    "term": "Prerequisite · take before Semester 1",
    "prereqs": "Secondary school algebra and trigonometry. UC MATH 600 "
               "is useful and is not required; the two can be taken in "
               "parallel",
    "deliverable": "A small software renderer that draws a shaded, "
                   "perspective-projected mesh — written with no "
                   "graphics API and no matrix library, so that every "
                   "transform in it is one you implemented",
    "effort": "8–10 hours per week · 13 modules + 2 project weeks",
    "description": [
        "<b>This is the second mathematics prerequisite, and it is "
        "less optional than it looks.</b> <b>The graphics pipeline "
        "<i>is</i> linear algebra</b> — <b>a vertex becomes a pixel by "
        "being multiplied by four matrices</b> — and CSCE 641 begins "
        "using bases, projections, and change of basis in week two "
        "without defining any of them.",
        "<b>The first third builds the objects.</b> <b>Vectors, "
        "spans, bases, and matrices as linear maps</b> (Modules 02 and "
        "03) — and <b>Module 04 on change of basis, which is the "
        "single most useful idea in the course</b> and the one that "
        "makes the pipeline comprehensible rather than "
        "memorised.",
        "<b>The second third is the geometry.</b> <b>Dot products, "
        "projection, cross products, normals, and orientation</b> "
        "(Modules 05 and 06) — <b>which is the vocabulary of every "
        "shading calculation</b> — and then <b>homogeneous coordinates "
        "and the pipeline itself</b> (Modules 07 and 08), where the "
        "course pays off visibly.",
        "<b>The third is the parts that matter later.</b> "
        "<b>Determinants and degeneracy</b> (Module 09) explain why "
        "transforms fail; <b>eigenvectors</b> (Module 10) are needed "
        "for CSCE 649 and CSCE 753; <b>quaternions</b> (Module 11) are "
        "how every engine actually stores a rotation; and <b>least "
        "squares</b> (Module 12) is the fitting procedure underneath "
        "half of CSCE 633.",
        "<b>And the closing module is about verification</b>, which "
        "is the program's rule in this subject. <b>A transform that "
        "looks right in one test scene is not a correct "
        "transform</b> — and the specific ways a wrong matrix looks "
        "right are worth knowing before you spend a weekend on "
        "one.",
    ],
    "outcomes": [
        "Explain why linear algebra is the graphics prerequisite.",
        "Work with vectors, spans, linear independence, and bases.",
        "Read a matrix as a linear map, and compose maps.",
        "Change basis, and explain why it is the central idea.",
        "Use dot products, projection, and orthogonality.",
        "Use cross products, normals, and orientation correctly.",
        "Explain homogeneous coordinates and affine transforms.",
        "Derive the model-view-projection chain.",
        "Use determinants to detect degeneracy and handedness.",
        "Compute and interpret eigenvectors.",
        "Use quaternions for rotation, and say why.",
        "Solve least squares problems and explain the normal "
        "equations.",
        "Verify a transform rather than eyeballing it.",
    ],
    "materials": [
        ("Strang — Introduction to Linear Algebra, with MIT 18.06 "
         "(OCW, full video)",
         "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
         "<b>The primary course, free in full.</b> The lectures are "
         "the standard introduction for good reason, and the "
         "column-space framing is exactly the one this course uses."),
        ("3Blue1Brown — Essence of Linear Algebra (free video)",
         "https://www.3blue1brown.com/topics/linear-algebra",
         "<b>Watch this first, all of it, before anything else.</b> "
         "Fifteen short videos that build the geometric intuition the "
         "algebra then formalises — and Modules 03, 04, and 09 are "
         "much easier afterwards."),
        ("Immersive Math — Interactive Linear Algebra (free)",
         "http://immersivemath.com/ila/",
         "<b>Modules 02 through 06, free.</b> Every figure is "
         "manipulable, which matters more here than in most "
         "subjects."),
        ("Lengyel — Mathematics for 3D Game Programming and Computer "
         "Graphics",
         "https://www.cengage.com/c/mathematics-for-3d-game-programming-and-computer-graphics-3e-lengyel/",
         "<b>Modules 06 through 11.</b> The graphics-specific "
         "treatment, including quaternions done properly. Library "
         "copy."),
        ("Gortler — Foundations of 3D Computer Graphics",
         "https://mitpress.mit.edu/9780262017350/",
         "<b>Modules 04, 07, and 08.</b> Unusually careful about "
         "frames and change of basis, which is exactly where graphics "
         "texts are usually sloppy. Library copy."),
        ("Shirley — Ray Tracing in One Weekend (free)",
         "https://raytracing.github.io/",
         "<b>Project 2's companion.</b> Free, short, and it exercises "
         "Modules 05, 06, and 09 on a real renderer."),
    ],
    "tooling": [
        "<b>Python with <code>numpy</code> for learning</b>, and "
        "<b>nothing but raw arrays for Project 2</b> — <b>because "
        "a matrix library will do the one thing you were supposed to "
        "understand</b>.",
        "<b>A plotting library</b> — <b>draw every vector and "
        "every basis you work with</b>, since <b>this is a subject "
        "where the picture is the understanding</b> and the algebra is "
        "the bookkeeping.",
        "<b>C++ for Project 2 if you intend to continue into "
        "CSCE 641</b>, which will want it — and the renderer "
        "transfers directly.",
        "<b>A right-handed convention, chosen once and written "
        "down</b> — <b>because handedness bugs are the single most "
        "common failure in this subject</b> and they are invisible "
        "until a normal points the wrong way "
        "(Module 06 §3).",
        "<b>And a test scene with known answers</b> — <b>a unit "
        "cube at the origin, a camera on an axis</b> — so that "
        "<b>every transform can be checked against a number you "
        "computed by hand</b> (Module 13 §2).",
    ],
    "projects": [
        {"n": 1, "after": 6,
         "title": "Transforms by hand",
         "brief": "Implement the operations, and verify them against "
                  "hand calculations.",
         "reqs": [
           "<b>Vector and matrix operations implemented from "
           "scratch</b> — add, scale, multiply, transpose — "
           "<b>with no library</b>.",
           "<b>Dot and cross products</b>, with <b>the geometric "
           "meaning verified</b>: angle from the dot, perpendicularity "
           "and area from the cross.",
           "<b>Rotation, scale, and shear matrices</b> built and "
           "<b>composed in both orders</b>, with the difference shown "
           "and explained.",
           "<b>A change of basis performed and inverted</b> "
           "(Module 04), with the round trip verified to numerical "
           "precision.",
           "<b>Every result checked against a hand "
           "calculation</b> on a case you worked on paper first.",
           "<b>And each transform drawn</b>, so that the picture "
           "and the numbers agree.",
         ],
         "done": [
           "<b>The hand calculations submitted alongside the "
           "code</b> — <b>which is the point</b>, because code that "
           "agrees with itself proves nothing.",
           "<b>The composition order difference demonstrated and "
           "explained</b>, not just observed — <b>matrix "
           "multiplication is not commutative and this is where that "
           "becomes real.</b>",
           "<b>The change of basis round trip exact</b> to "
           "floating-point tolerance, with the tolerance stated.",
           "<b>And the drawings included</b>, because <b>a transform "
           "you cannot picture is one you will misuse</b>.",
         ]},
        {"n": 2, "after": 12,
         "title": "A software renderer",
         "brief": "Draw a shaded perspective mesh with every matrix "
                  "your own.",
         "reqs": [
           "<b>A full model-view-projection chain</b> "
           "(Module 08), <b>each matrix derived rather than copied</b>, "
           "with the derivation submitted.",
           "<b>A triangle mesh loaded and transformed</b>, with "
           "<b>per-face normals computed by cross product</b> "
           "(Module 06).",
           "<b>Diffuse shading from a dot product</b> "
           "(Module 05), and <b>backface culling from the sign of a "
           "determinant or a dot</b> (Module 09).",
           "<b>Perspective divide and a viewport transform</b>, "
           "with <b>the near plane's behaviour explained</b>.",
           "<b>A camera that orbits</b>, using either a rotation "
           "matrix or a quaternion (Module 11) — and <b>say which "
           "and why</b>.",
           "<b>And the verification suite</b> of Module 13 §2: "
           "known points, known answers, checked automatically.",
         ],
         "done": [
           "<b>Every matrix derived rather than copied</b>, with "
           "the derivations submitted — <b>a correct projection "
           "matrix found online teaches nothing</b>, and this project "
           "is the one place in the program where that matters "
           "most.",
           "<b>The verification suite passing</b>, and <b>at least "
           "one bug found by it rather than by looking at the "
           "image</b> (Module 13 §1).",
           "<b>The handedness convention stated</b> and consistent "
           "throughout — which is the failure this project exists "
           "to inoculate against.",
           "<b>And the near-plane behaviour explained</b>, because "
           "<b>understanding why geometry explodes near it is "
           "understanding the projection matrix</b> "
           "(Module 08 §3).",
         ]},
    ],
    "map": [
        ("MIT 18.06 with Strang (OCW, free video)",
         "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
         "<b>Modules 02, 03, 09, 10, and 12.</b> The full course, "
         "free, and the standard reference."),
        ("3Blue1Brown, Essence of Linear Algebra (free)",
         "https://www.3blue1brown.com/topics/linear-algebra",
         "<b>Modules 02 to 04 and 09 to 10</b> — watch before "
         "reading, every time."),
        ("Immersive Math (free, interactive)",
         "http://immersivemath.com/ila/",
         "<b>Modules 02 to 06</b>, with manipulable figures."),
        ("Gortler &mdash; Foundations of 3D Computer Graphics",
         "https://mitpress.mit.edu/9780262017350/",
         "<b>Modules 04, 07, and 08</b> — frames and change of basis "
         "done carefully. Library copy."),
        ("Lengyel &mdash; Mathematics for 3D Game Programming",
         "https://www.cengage.com/c/mathematics-for-3d-game-programming-and-computer-graphics-3e-lengyel/",
         "<b>Modules 06, 09, and 11</b> — the graphics-specific "
         "material, including quaternions. Library copy."),
        ("Scratchapixel (free)",
         "https://www.scratchapixel.com/",
         "<b>Modules 07 and 08</b> — the pipeline derived step by "
         "step, free, with code."),
    ],
}

MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Why This Is the Graphics Prerequisite",
 "subtitle": "Because the pipeline is four matrix multiplications.",
 "question": "What actually happens to a vertex?",
 "outcomes": [
     "Trace a vertex through the pipeline at a high level.",
     "Name the four transforms and what each does.",
     "Explain why linear algebra is the subject rather than "
     "background.",
     "State what this course assumes and what it supplies.",
     "Decide whether you can skip it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What happens to a vertex",
   "blurb": "The whole pipeline, before any of the machinery."},

  {"t": "code", "kicker": "Pipeline", "title": "A point in a model becomes a pixel",
   "lang": "text", "code": """
  A VERTEX STARTS as three numbers in the space the
  artist modelled it in. It ends as a pixel. In
  between:

  1  MODEL MATRIX
         model space -> world space
         "where is this object placed in the scene"

  2  VIEW MATRIX
         world space -> camera space
         "what does this look like from the camera"
         -- which is a change of basis (Module 04)

  3  PROJECTION MATRIX
         camera space -> clip space
         "how does distance become smaller on screen"
         -- which needs homogeneous coords (M07)

  4  PERSPECTIVE DIVIDE and VIEWPORT
         clip space -> pixels

  SO: p_screen = Viewport * Project * View * Model * p

  FOUR MATRIX MULTIPLICATIONS. That is the pipeline,
  and this course is about what each one is.
""",
   "caption": "<b>Four matrix multiplications</b> — that is the "
              "pipeline, and the rest of the course is about what each "
              "one is and why it has the form it "
              "does.",
   "note": "Everything in Modules 02 through 08 serves this one "
           "line."},

  {"t": "callout", "title": "Which is why this is the subject rather than the background",
   "kind": "The argument for not skipping it",
   "body": ["<b>A graphics course that assumed no linear algebra "
            "would have to teach it anyway</b> — <b>there is nothing "
            "else there</b>, and CSCE 641 spends its time on the parts "
            "that are not matrices instead.",
            "<b>And the failure mode is specific:</b> <b>you can "
            "copy a projection matrix from a book and get a "
            "picture</b> — <b>and then be unable to debug it, extend "
            "it, or handle the case the book did not "
            "cover.</b>",
            "<b>Which happens constantly</b>, because the pipeline "
            "is forgiving of ignorance until it is not — <b>and the "
            "symptom is a scene that is almost right in a way you "
            "cannot name.</b>",
            "<b>So the test is Module 13's</b>: <b>can you derive "
            "the projection matrix rather than recall it</b> — and "
            "<b>deriving it is four lines once Module 07 is in "
            "place.</b>"]},

  {"t": "section", "label": "Part 2", "title": "The four transforms",
   "blurb": "And what kind of thing each one is."},

  {"t": "table", "kicker": "Transforms", "title": "What each matrix actually does",
   "header": ["Matrix", "What it is", "Covered in"],
   "widths": [2.5, 5.0, 3.5],
   "rows": [
     ["<b>Model</b>", "<b>Rotation, scale, translation composed</b>", "<b>Modules 03, 07</b>"],
     ["<b>View</b>", "<b>A change of basis to the camera's frame</b>", "<b>Module 04</b>"],
     ["<b>Projection</b>", "<b>A shear plus a divide, in disguise</b>", "<b>Modules 07, 08</b>"],
     ["<b>Normal matrix</b>", "<b>The inverse transpose — and why</b>", "<b>Modules 06, 09</b>"],
   ],
   "footnote": "<b>The view matrix is a change of basis and the "
               "projection is a shear</b> — two facts that make the "
               "pipeline comprehensible instead of "
               "memorised.",
   "note": "The normal matrix row is the one that surprises people, "
           "and Module 06 §4 explains it."},

  {"t": "section", "label": "Part 3", "title": "Beyond the pipeline",
   "blurb": "Where else the course pays off."},

  {"t": "bullets", "kicker": "Elsewhere", "title": "What the rest of the program needs from here",
   "items": [
     "<b>CSCE 645 Geometric Modeling</b> — <b>splines are "
     "linear combinations of basis functions</b>, which is "
     "Module 02's vocabulary applied to "
     "curves.",
     "",
     "<b>CSCE 647 Image Synthesis</b> — <b>every ray-surface "
     "intersection is a dot product and a solve</b>, and <b>importance "
     "sampling needs orthonormal frames</b> "
     "(Module 05).",
     "",
     "<b>CSCE 649 Physically-Based Modeling</b> — <b>inertia "
     "tensors are eigenvector problems</b> and rotations are "
     "quaternions (Modules 10, 11).",
     "",
     "<b>CSCE 633 and 636</b> — <b>least squares is the first "
     "fitting method</b> and <b>principal components are "
     "eigenvectors</b> (Modules 10, 12).",
     "",
     "<b>And CSCE 753 Computer Vision</b>, which is this course "
     "run backwards — <b>recovering the matrices from the "
     "images.</b>",
   ],
   "footnote": "<b>Computer vision is this course run "
               "backwards</b> — graphics computes the image from the "
               "transform, and vision recovers the transform from the "
               "image."},

  {"t": "section", "label": "Part 4", "title": "Can you skip it?",
   "blurb": "Honestly, with a specific test."},

  {"t": "callout", "title": "Five questions decide it, and they are the ones CSCE 641 assumes in week two",
   "kind": "Closing",
   "body": ["<b>Can you say what a basis is, and why a matrix column "
            "is where a basis vector lands?</b> "
            "(Modules 02, 03.)",
            "<b>Can you project one vector onto another, and derive "
            "the formula?</b> "
            "(Module 05 §2.)",
            "<b>Can you say why the cross product's direction "
            "depends on handedness?</b> "
            "(Module 06 §3.)",
            "<b>Can you explain what the fourth coordinate is "
            "for</b> (Module 07), and <b>why normals use the inverse "
            "transpose</b> (Module 06 §4)? <b>Five questions; answer "
            "them all and skip the course.</b>"]},
 ],
 "takeaways": [
   "Four matrix multiplications are the pipeline, and the rest of the "
   "course is what each one is.",
   "You can copy a projection matrix and get a picture, and then be unable "
   "to debug it — which is the specific failure mode.",
   "The view matrix is a change of basis and the projection is a shear, "
   "which makes the pipeline comprehensible instead of memorised.",
   "Computer vision is this course run backwards.",
   "The symptom of not knowing this is a scene that is almost right in a "
   "way you cannot name.",
   "Five questions decide whether you can skip it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What happens to a vertex"),
  ("code", """A VERTEX STARTS as three numbers in the space the
artist modelled it in. It ends as a pixel. In
between:

1  MODEL MATRIX
       model space -> world space
       "where is this object placed in the scene"

2  VIEW MATRIX
       world space -> camera space
       "what does this look like from the camera"
       -- which is a change of basis (Module 04)

3  PROJECTION MATRIX
       camera space -> clip space
       "how does distance become smaller on screen"
       -- which needs homogeneous coordinates (M07)

4  PERSPECTIVE DIVIDE and VIEWPORT TRANSFORM
       clip space -> normalised device coords
       -> pixels

SO: p_screen = Viewport * Project * View * Model * p

FOUR MATRIX MULTIPLICATIONS. That is the pipeline,
and this whole course is about what each one is."""),
  ("p", "<b>Four matrix multiplications</b> — <b>that is the "
        "pipeline</b>, and <b>the rest of the course is about what each "
        "one is and why it has the form it does</b>. <b>Everything in "
        "Modules 02 through 08 serves this one line</b>, and "
        "Module 08 returns to it with every matrix derived. It is "
        "worth copying this line somewhere and coming back to it as each "
        "module fills a piece in."),
  ("callout", "Which is why this is the subject rather than the background",
   ["<b>A graphics course that assumed no linear algebra would have "
    "to teach it anyway</b> — <b>there is nothing else in the "
    "pipeline</b> — <b>and CSCE 641 spends its time instead on "
    "the parts that are not matrices</b>: rasterisation, shading "
    "models, texturing, and the hardware.",
    "<b>And the failure mode is specific rather than "
    "general:</b> <b>you can copy a projection matrix out of a book "
    "and get a picture on the screen</b> — <b>and then be unable "
    "to debug it, extend it, or handle the case the book did not "
    "cover</b>, such as an off-axis frustum or a reversed depth "
    "buffer.",
    "<b>Which happens constantly</b>, because <b>the pipeline is "
    "forgiving of ignorance right up until it is not</b> — <b>and "
    "the symptom is a scene that is almost right in a way you cannot "
    "name</b>: shading slightly off, geometry subtly skewed, something "
    "inside out at one camera angle.",
    "<b>So the test is Module 13's and &sect;4's</b>: <b>can you "
    "derive the projection matrix rather than recall it?</b> — and "
    "<b>deriving it is about four lines once Module 07's homogeneous "
    "coordinates are in place</b>, which is the whole argument for "
    "spending the four weeks."]),

  ("h1", "2 &nbsp; The four transforms"),
  ("table", ["Matrix", "What it actually is", "Covered in"],
   [["<b>Model</b>",
     "<b>Rotation, scale, and translation composed into one "
     "matrix</b> — and the order matters.",
     "<b>Modules 03 and 07</b>"],
    ["<b>View</b>",
     "<b>A change of basis into the camera's frame</b> — not a "
     "movement of the camera, but a re-expression of the world.",
     "<b>Module 04</b>"],
    ["<b>Projection</b>",
     "<b>A shear plus a divide, in disguise</b> — the matrix sets "
     "up the divide and the hardware performs it.",
     "<b>Modules 07 and 08</b>"],
    ["<b>Normal matrix</b>",
     "<b>The inverse transpose of the model-view matrix</b> — and "
     "the reason is geometric, not algebraic.",
     "<b>Modules 06 and 09</b>"]],
   [0.18, 0.56, 0.26]),
  ("p", "<b>The view matrix is a change of basis and the projection "
        "is a shear</b> — <b>two facts that make the pipeline "
        "comprehensible instead of memorised</b>, and both are "
        "non-obvious until stated. <b>The normal matrix row is the one "
        "that surprises people</b>: normals do not transform like "
        "points, and <b>Module 06 &sect;4 explains why</b> in a way "
        "that makes the inverse transpose inevitable rather than "
        "arbitrary."),

  ("break",),
  ("h1", "3 &nbsp; Beyond the pipeline"),
  ("ul", ["<b>CSCE 645 Geometric Modeling</b> — <b>splines are "
          "linear combinations of basis functions</b>, <b>which is "
          "Module 02's vocabulary applied to curves rather than to "
          "arrows</b>, and the whole subject reads differently once you "
          "see that.",
          "<b>CSCE 647 Image Synthesis</b> — <b>every "
          "ray-surface intersection is a dot product and a linear "
          "solve</b>, and <b>importance sampling requires building an "
          "orthonormal frame around a normal</b> (Module 05 "
          "&sect;4), which is a Module 05 exercise.",
          "<b>CSCE 649 Physically-Based Modeling</b> — "
          "<b>inertia tensors are eigenvector problems</b> (the "
          "principal axes are the eigenvectors) <b>and orientations are "
          "quaternions</b> (Modules 10 and 11).",
          "<b>CSCE 633 and CSCE 636</b> — <b>least squares is "
          "the first fitting method you meet</b> and <b>principal "
          "component analysis is an eigenvector computation</b> "
          "(Modules 10 and 12), so two of this course's later modules "
          "are machine learning prerequisites as much as graphics "
          "ones.",
          "<b>And CSCE 753 Computer Vision, which is this course "
          "run backwards</b> — <b>graphics computes the image from "
          "the transform, and vision recovers the transform from the "
          "image</b> — which is why the camera matrix appears in "
          "both and means the same thing."]),

  ("h1", "4 &nbsp; Can you skip it?"),
  ("callout", "Five questions decide it, and they are the ones CSCE 641 "
              "assumes in week two",
   ["<b>Can you say what a basis is, and explain why the columns of "
    "a matrix are where the basis vectors land?</b> (Modules 02 and "
    "03 — and that second fact is the one that makes matrices stop "
    "being tables of numbers.)",
    "<b>Can you project one vector onto another, and derive the "
    "formula rather than recall it?</b> (Module 05 &sect;2 — "
    "and this is the operation every shading model uses.)",
    "<b>Can you say why the cross product's direction depends on a "
    "handedness convention, and which convention you use?</b> "
    "(Module 06 &sect;3 — and <b>handedness bugs are the "
    "commonest failure in this subject</b>.)",
    "<b>Can you explain what the fourth coordinate is for</b> "
    "(Module 07), and <b>why normals are transformed by the inverse "
    "transpose</b> (Module 06 &sect;4)? <b>Five questions; answer all "
    "five and skip the course with a clear conscience</b> — and if "
    "you cannot, the ones you missed name the modules that matter "
    "most."]),
 ],
 "resources": [
   ("3Blue1Brown &mdash; Essence of Linear Algebra (free)",
    "https://www.3blue1brown.com/topics/linear-algebra",
    "<b>Watch all fifteen before Module 02</b> — it is three hours "
    "and it changes how every later module reads."),
   ("Scratchapixel &mdash; the geometry and transform sections "
    "(free)",
    "https://www.scratchapixel.com/",
    "<b>&sect;1's pipeline</b>, derived step by step with code, and "
    "free."),
   ("MIT 18.06, lecture 1 (free video)",
    "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
    "<b>&sect;2</b> — Strang's opening, which frames the whole "
    "subject around the column picture."),
   ("Gortler, chapters 2 and 3 (library copy)",
    "https://mitpress.mit.edu/9780262017350/",
    "<b>&sect;&sect;1 and 2</b> — frames and transforms stated more "
    "carefully than most graphics books manage."),
 ],
 "exercises": [
   "<b>Write out the pipeline line</b> from memory, with all four "
   "transforms named.",
   "<b>For each transform, say what space it maps from and to.</b>",
   "<b>Find a projection matrix in a book</b> and list what you do "
   "not understand about it.",
   "<b>Describe a graphics bug</b> you have seen that was almost "
   "right.",
   "<b>Name which module covers each of the four matrices.</b>",
   "<b>Find three places in the program</b> outside graphics that "
   "need this course.",
   "<b>Explain why vision is graphics backwards</b>, in three "
   "sentences.",
   "<b>Take the five questions</b> in §4 now, and record your "
   "answers.",
   "<b>Watch the 3Blue1Brown series</b> end to end before "
   "Module 02.",
   "<b>Set up a test scene</b>: a unit cube, a camera on an axis, and "
   "a point whose screen position you can compute by hand.",
 ],
 "selfcheck": [
   "Name the four transforms and the spaces each maps between.",
   "Write the pipeline as one line.",
   "Why is linear algebra the subject rather than the background?",
   "What is the specific failure mode of copying a matrix?",
   "What is the view matrix, really?",
   "What is the projection matrix, really?",
   "Which transform surprises people, and why?",
   "Name four later courses that need this one, and what each "
   "needs.",
   "Why is computer vision this course backwards?",
   "Give the five skip-test questions.",
 ],
},

]

for _b in ("ucl600_b2", "ucl600_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
