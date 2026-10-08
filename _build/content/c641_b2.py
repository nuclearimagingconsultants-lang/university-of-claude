# -*- coding: utf-8 -*-
"""CSCE 641 — Modules 02-04."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Vectors, Frames, and Homogeneous Coordinates",
 "subtitle": "The algebra the whole pipeline is written in.",
 "question": "Why does a 3D renderer use 4D coordinates?",
 "outcomes": [
     "Distinguish points from vectors, and explain why the distinction is "
     "not pedantry.",
     "Build an orthonormal frame from an arbitrary direction.",
     "Explain what the fourth coordinate means and why translation requires "
     "it.",
     "Use dot and cross products fluently for projection, area, and "
     "orientation.",
     "Transform normals correctly, and say why the obvious method is wrong.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Points are not vectors",
   "blurb": "A distinction that costs nothing to maintain and a great deal "
            "to ignore."},

  {"t": "two", "kicker": "The distinction", "title": "Two different things with the same notation",
   "lh": "Point — a location",
   "l": ["Answers: <i>where</i>?",
         "Has no direction or length.",
         "Point &minus; point = vector.",
         "Point + vector = point.",
         ("Point + point is <b>meaningless</b>.", 1),
         "Affected by translation."],
   "rh": "Vector — a displacement",
   "r": ["Answers: <i>how far, which way</i>?",
         "Has direction and length, no location.",
         "Vector + vector = vector.",
         "Scalar &times; vector = vector.",
         ("All operations are well defined.", 1),
         "<b>Unaffected</b> by translation."],
   "note": "The practical payoff is immediate: if you translate a normal "
           "vector you have made an error, and the type system of homogeneous "
           "coordinates will catch it for you if you let it."},

  {"t": "callout", "title": "Why this matters in code", "kind": "Consequence",
   "body": ["Translating a direction is always a bug. A surface normal does "
            "not move when the object moves — it only rotates.",
            "Homogeneous coordinates encode this distinction in the data "
            "itself: <i>w</i> = 1 for a point, <i>w</i> = 0 for a vector. "
            "Multiply both by the same translation matrix and the vector is "
            "automatically left alone.",
            "The fourth coordinate is not a trick to make translation fit "
            "into a matrix. It is a type tag that happens to make translation "
            "fit into a matrix."]},

  {"t": "eq", "kicker": "Homogeneous coordinates", "title": "The fourth coordinate",
   "eqs": [
     ("point   =  (x, y, z, 1)",
      "Translation reaches it, because the translation column is scaled by w=1."),
     ("vector  =  (x, y, z, 0)",
      "Translation cannot reach it. Rotation and scale still apply normally."),
     ("(x, y, z, w)  ≡  (x/w, y/w, z/w, 1)   for w ≠ 0",
      "Scaling all four coordinates names the same point — this is what "
      "makes perspective possible."),
   ],
   "caption": "The third line is the one that earns the fourth coordinate. "
              "Module 03 uses it to make perspective a linear operation."},

  {"t": "section", "label": "Part 2", "title": "Products that do work",
   "blurb": "Two products, and almost everything geometric you will need."},

  {"t": "eq", "kicker": "Dot product", "title": "The dot product measures alignment",
   "eqs": [
     ("a · b  =  aₓbₓ + a_yb_y + a_zb_z  =  |a||b| cos θ",
      "Two definitions, one for computing and one for understanding."),
     ("a · b = 0   ⟺   perpendicular",
      "The visibility and backface tests reduce to this sign."),
     ("proj_b(a)  =  (a · b̂) b̂",
      "Projection onto a direction. Used in every lighting model and in "
      "Gram–Schmidt."),
   ],
   "note": "Stress that for unit vectors the dot product IS the cosine. "
           "Nearly every lighting equation in Module 06 is a clamped dot "
           "product."},

  {"t": "bullets", "kicker": "Dot product", "title": "Where you will actually use it",
   "items": [
     "<b>Lambert's cosine law</b> — diffuse shading is max(0, n · l).",
     "<b>Backface culling</b> — sign of n · v tells you which way a "
     "face points.",
     "<b>Specular highlights</b> — (n · h) raised to a power.",
     "<b>Frustum culling</b> — signed distance from a plane is a dot "
     "product with the plane normal.",
     "<b>Decomposing a vector</b> — splitting a velocity into components "
     "along and across a surface, which is the whole of collision response.",
   ]},

  {"t": "eq", "kicker": "Cross product", "title": "The cross product makes perpendiculars",
   "eqs": [
     ("a × b  =  (a_yb_z − a_zb_y,  a_zbₓ − aₓb_z,  aₓb_y − a_ybₓ)",
      "Perpendicular to both inputs, by the right-hand rule."),
     ("|a × b|  =  |a||b| sin θ  =  area of the parallelogram",
      "Half of this is the triangle area — which Module 04 turns into "
      "barycentric coordinates."),
     ("n  =  normalize((p₁ − p₀) × (p₂ − p₀))",
      "The face normal of a triangle. Winding order decides its sign."),
   ]},

  {"t": "section", "label": "Part 3", "title": "Frames",
   "blurb": "A coordinate system is three vectors and a point. Nothing more."},

  {"t": "bullets", "kicker": "Frames", "title": "What a coordinate frame is",
   "items": [
     "An origin (a point) plus three basis vectors (directions).",
     "Coordinates are <i>the amounts of each basis vector</i> you need.",
     "",
     "An <b>orthonormal</b> frame has basis vectors that are mutually "
     "perpendicular and unit length.",
     ("Its matrix inverse is its transpose — which is why view matrices "
      "are cheap to invert.", 1),
     ("Its determinant is +1 (right-handed) or −1 (left-handed, i.e. "
      "mirrored).", 1),
     "",
     "Every space in the pipeline — object, world, camera, tangent "
     "— is just a different frame.",
   ],
   "note": "Students often memorise 'the view matrix is the inverse of the "
           "camera transform' without knowing why it is cheap. Orthonormality "
           "is the reason."},

  {"t": "code", "kicker": "Frames", "title": "Building a frame from one direction",
   "lang": "cpp", "code": """
// Given a normal n, produce an orthonormal basis (t, b, n).
// Needed for tangent space (Module 08) and for sampling (Module 11).

void make_frame(const vec3& n, vec3& t, vec3& b) {
    // Pick any axis not nearly parallel to n, or the cross product
    // degenerates and you get NaNs in a few pixels only -- the worst
    // kind of bug, because it looks like noise.
    vec3 up = (fabs(n.z) < 0.999f) ? vec3(0,0,1) : vec3(1,0,0);

    t = normalize(cross(up, n));
    b = cross(n, t);            // already unit: n and t are orthonormal
}
""",
   "caption": "The guard on the `up` vector is not optional. Without it the "
              "cross product returns zero wherever n happens to align with "
              "the axis, and normalize() produces NaN.",
   "note": "This exact bug produces a handful of black or white pixels that "
           "move with the camera. It is worth showing once so they recognise "
           "it later."},

  {"t": "section", "label": "Part 4", "title": "Transforming normals",
   "blurb": "The one place where the obvious answer is wrong."},

  {"t": "callout", "title": "Normals do not transform like positions",
   "kind": "The classic error",
   "body": ["Apply a non-uniform scale to a surface and to its normal with "
            "the same matrix, and the normal stops being perpendicular to the "
            "surface.",
            "Stretch a sphere into an ellipsoid along X: the surface flattens, "
            "so its normals should tilt <i>toward</i> the Y axis. Scaling the "
            "normals by the same matrix tilts them the other way.",
            "The result is lighting that is subtly, confusingly wrong on every "
            "non-uniformly scaled object in your scene."]},

  {"t": "eq", "kicker": "The fix", "title": "The normal matrix",
   "eqs": [
     ("n'  =  (M⁻¹)ᵀ n",
      "Transform normals by the inverse transpose of the model matrix."),
     ("for rotation only:  (M⁻¹)ᵀ = M",
      "Orthonormal matrices are their own normal matrix — no extra work."),
     ("for uniform scale:  (M⁻¹)ᵀ ∝ M",
      "Direction is unchanged; only length, which normalize() removes anyway."),
   ],
   "caption": "So the inverse transpose only matters under non-uniform scale "
              "or shear — but that is common enough that you should "
              "simply always use it.",
   "note": "Derivation in the notes: it follows from requiring n·t = 0 to "
           "be preserved for every tangent t."},

  {"t": "code", "kicker": "In practice", "title": "Where the normal matrix goes",
   "lang": "glsl", "code": """
// CPU side, once per object -- not per vertex, and never per fragment.
mat3 normalMatrix = transpose(inverse(mat3(model)));

// Vertex shader
void main() {
    vWorldPos    = (model * vec4(aPos, 1.0)).xyz;
    vWorldNormal = normalMatrix * aNormal;   // NOT model * aNormal
    gl_Position  = proj * view * vec4(vWorldPos, 1.0);
}

// Fragment shader: renormalize. Interpolating unit vectors across a
// triangle does not preserve unit length.
vec3 N = normalize(vWorldNormal);
""",
   "caption": "Two separate requirements: the right matrix on the CPU, and "
              "renormalization after interpolation. Missing either one dims "
              "your lighting in a way that is easy to mistake for an art "
              "problem."},

  {"t": "table", "kicker": "Summary", "title": "What transforms how",
   "header": ["Quantity", "w", "Transform by", "Then"],
   "widths": [3.6, 1.0, 3.9, 3.6],
   "rows": [
     ["Position", "1", "M", "divide by w after projection"],
     ["Direction / tangent", "0", "M", "normalize if needed"],
     ["Normal", "0", "(M⁻¹)ᵀ", "always renormalize"],
     ["Plane (n, d)", "—", "(M⁻¹)ᵀ on the 4-vector",
      "renormalize n, rescale d"],
   ],
   "note": "Worth having students copy this into their renderer as a comment "
           "block. It prevents a whole family of bugs."},
 ],
 "takeaways": [
   "Points and vectors are different types. Homogeneous w = 1 and w = 0 "
   "encode the difference so the matrix does the right thing automatically.",
   "The fourth coordinate exists because scaling all four names the same "
   "point — that equivalence is what makes perspective linear.",
   "Dot product measures alignment and gives you projection; cross product "
   "makes perpendiculars and gives you area. Almost all of geometry is these "
   "two.",
   "An orthonormal frame's inverse is its transpose. This is why the view "
   "matrix is cheap.",
   "Normals transform by the inverse transpose, and must be renormalized "
   "after interpolation. Both halves are required.",
   "When building a frame from a single direction, guard the degenerate case "
   "or you will get NaN in a few pixels and never find them.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Points and vectors"),
  ("p", "Both are written as three numbers, which is why the distinction "
        "gets lost, and why losing it produces bugs that look like art "
        "problems rather than code problems. A <b>point</b> is a location: it "
        "answers <i>where</i>. A <b>vector</b> is a displacement: it answers "
        "<i>how far and in which direction</i>. A vector has no location at "
        "all — the same vector exists identically everywhere in space."),
  ("p", "The operations that are legal follow directly:"),
  ("table", ["Expression", "Result", "Meaning"],
   [["point &minus; point", "vector", "The displacement from one to the other."],
    ["point + vector", "point", "Move a location by a displacement."],
    ["vector &plusmn; vector", "vector", "Compose displacements."],
    ["scalar &times; vector", "vector", "Scale a displacement."],
    ["point + point", "<b>undefined</b>",
     "There is no meaningful sum of two locations. (A weighted average with "
     "weights summing to 1 <i>is</i> meaningful — that is exactly what "
     "barycentric interpolation is, and Module 04 relies on it.)"]],
   [0.22, 0.14, 0.64]),
  ("callout", "The practical consequence",
   ["Translation must affect points and must not affect vectors. A surface "
    "normal pointing up still points up after you move the object three "
    "metres to the left.",
    "Homogeneous coordinates make this automatic rather than something you "
    "have to remember."]),

  ("h1", "2 &nbsp; Homogeneous coordinates"),
  ("p", "Add a fourth coordinate <i>w</i>. Points get <i>w</i> = 1, "
        "directions get <i>w</i> = 0. Now consider a translation matrix:"),
  ("code", """    | 1  0  0  tx |   | x |     | x + tx*w |
    | 0  1  0  ty | * | y |  =  | y + ty*w |
    | 0  0  1  tz |   | z |     | z + tz*w |
    | 0  0  0   1 |   | w |     |    w     |""",
   "With w = 1 the translation applies. With w = 0 it vanishes. The same "
   "matrix does the correct thing to both types without a branch."),
  ("p", "That alone would be a convenience. The reason homogeneous "
        "coordinates are <i>necessary</i> rather than convenient is the "
        "equivalence relation they carry:"),
  ("eq", "(x, y, z, w) &nbsp;&equiv;&nbsp; (&lambda;x, &lambda;y, &lambda;z, &lambda;w) &nbsp; for any &lambda; &ne; 0"),
  ("p", "All of these name the same point, recovered as (x/w, y/w, z/w). "
        "This is what lets perspective projection — which is a division, "
        "and therefore not linear — be expressed as a linear matrix "
        "followed by a single divide at the end. The matrix arranges for "
        "<i>w</i> to come out equal to the view-space depth; the divide then "
        "produces the 1/z falloff that makes distant things small. Module 03 "
        "does this in full."),
  ("callout", "Points at infinity",
   ["A direction is a point with w = 0 — literally a point infinitely "
    "far away in that direction. This is not a metaphor; it is how "
    "projective geometry works, and it is why directional lights (the sun) "
    "are naturally expressed as w = 0 while point lights use w = 1.",
    "It also explains why parallel lines meet at the horizon in a perspective "
    "image: the horizon is where the w = 0 points land."]),

  ("h1", "3 &nbsp; The two products"),
  ("h2", "3.1 &nbsp; Dot product"),
  ("eq", "a &middot; b = a<sub>x</sub>b<sub>x</sub> + a<sub>y</sub>b<sub>y</sub> + a<sub>z</sub>b<sub>z</sub> = |a||b| cos&theta;"),
  ("p", "Two formulas for the same number: the first computes it, the second "
        "explains it. For unit vectors the dot product <i>is</i> the cosine "
        "of the angle between them, which is why so much of shading is "
        "clamped dot products. The sign alone answers 'are these pointing "
        "roughly the same way?', which is the whole of backface culling."),
  ("p", "Projection of <b>a</b> onto a <i>unit</i> direction <b>b</b> is "
        "(a &middot; b) b. Subtracting that projection leaves the "
        "perpendicular component. Splitting a vector into parallel and "
        "perpendicular parts this way is the core operation of "
        "Gram&ndash;Schmidt orthogonalisation, of collision response, and of "
        "reflecting a vector about a normal:"),
  ("eq", "reflect(d, n) = d &minus; 2(d &middot; n) n"),

  ("h2", "3.2 &nbsp; Cross product"),
  ("p", "Produces a vector perpendicular to both inputs, with length equal to "
        "the area of the parallelogram they span. Both halves are used "
        "constantly: the direction gives you normals and frames, the "
        "magnitude gives you areas, and the <i>sign</i> of the area in 2D "
        "gives you orientation — which is how Module 04 decides whether a "
        "point is inside a triangle."),
  ("p", "The cross product is anticommutative: a &times; b = &minus;(b &times; "
        "a). This is the entire content of 'winding order'. A triangle's "
        "normal depends on the order its vertices are listed in, and a "
        "renderer that disagrees with its asset pipeline about that "
        "convention renders everything inside out."),

  ("h1", "4 &nbsp; Coordinate frames"),
  ("p", "A frame is an origin and three basis vectors. A coordinate triple "
        "(x, y, z) means 'start at the origin, go x along the first basis "
        "vector, y along the second, z along the third'. Changing frames is "
        "re-expressing the same geometric object in different numbers, and "
        "the whole vertex pipeline is a sequence of exactly this."),
  ("p", "A frame whose basis vectors are mutually perpendicular and unit "
        "length is <b>orthonormal</b>, and orthonormal matrices have a "
        "property worth caring about:"),
  ("eq", "M&#8315;&#185; = M&#7488; &nbsp;&nbsp; (orthonormal only)"),
  ("p", "Inverting becomes transposing — nine memory moves instead of a "
        "general 4&times;4 inverse. This is precisely why the view matrix is "
        "cheap to build: the camera's orientation is orthonormal, so its "
        "inverse is free, and only the translation needs real work. Module 03 "
        "builds the view matrix on exactly this observation."),
  ("h2", "4.1 &nbsp; Building a frame from one vector"),
  ("p", "Tangent-space normal mapping (Module 08) and hemisphere sampling "
        "(Module 11) both need a full orthonormal frame given only a normal. "
        "The construction is three lines, and the guard is mandatory:"),
  ("code", """void make_frame(const vec3& n, vec3& t, vec3& b) {
    // If `up` is nearly parallel to n, cross(up, n) -> 0 and
    // normalize() returns NaN. This shows up as a few black or white
    // pixels that move with the camera -- almost impossible to find
    // if you do not already know to look for it.
    vec3 up = (fabs(n.z) < 0.999f) ? vec3(0,0,1) : vec3(1,0,0);
    t = normalize(cross(up, n));
    b = cross(n, t);
}"""),
  ("p", "Note that <b>b</b> needs no normalization: the cross product of two "
        "perpendicular unit vectors is already unit length. Small thing, but "
        "it runs per-fragment."),

  ("break",),
  ("h1", "5 &nbsp; Transforming normals correctly"),
  ("p", "This is the single most commonly botched piece of linear algebra in "
        "real-time graphics, and the symptom — lighting that is slightly "
        "wrong on stretched objects — is easy to blame on the artist."),
  ("h2", "5.1 &nbsp; Why the obvious method fails"),
  ("p", "Take a sphere and scale it by 2 along X, flattening it in Y and Z "
        "relatively. Consider a point on the surface at 45&deg;. The surface "
        "there becomes <i>shallower</i>, so its normal should rotate "
        "<i>toward</i> the Y axis. But applying the same scale to the normal "
        "stretches its X component, rotating it toward X — the opposite "
        "direction. The transformed vector is no longer perpendicular to the "
        "transformed surface."),
  ("h2", "5.2 &nbsp; The derivation"),
  ("p", "Let <b>t</b> be any tangent to the surface, so n &middot; t = 0. "
        "After transformation by M the tangent becomes Mt, and we want some "
        "matrix G such that the transformed normal Gn is still perpendicular "
        "to it:"),
  ("eq", "(Gn) &middot; (Mt) = 0 &nbsp;&nbsp;&rArr;&nbsp;&nbsp; (Gn)&#7488;(Mt) = 0 &nbsp;&nbsp;&rArr;&nbsp;&nbsp; n&#7488;(G&#7488;M)t = 0"),
  ("p", "We know n&#7488;t = 0 holds for every tangent t. So the equation is "
        "satisfied for all t precisely when G&#7488;M = I, which gives:"),
  ("eq", "G = (M&#8315;&#185;)&#7488;"),
  ("p", "This matrix is called the <b>normal matrix</b>. Two useful special "
        "cases: if M is a pure rotation then M is orthonormal and "
        "(M&#8315;&#185;)&#7488; = M, so nothing changes. If M is a uniform "
        "scale then (M&#8315;&#185;)&#7488; is proportional to M, which "
        "changes only length — and you normalize anyway. The inverse "
        "transpose therefore matters exactly when there is non-uniform scale "
        "or shear."),
  ("callout", "Two separate requirements",
   ["<b>1. Use the normal matrix.</b> Compute it once per object on the CPU; "
    "a 3&times;3 inverse per vertex would be absurd.",
    "<b>2. Renormalize after interpolation.</b> The rasterizer interpolates "
    "normals linearly across the triangle, and the linear interpolation of "
    "two unit vectors is not a unit vector — it is shorter, most so in "
    "the middle of the triangle. Skipping this darkens the centre of every "
    "large triangle, which looks exactly like a bad lightmap.",
    "Both are needed. Fixing one and not the other leaves you with a subtler "
    "version of the same bug."]),
  ("h2", "5.3 &nbsp; The cheat that is usually correct"),
  ("p", "Many engines upload only a 3&times;3 rotation and skip the inverse "
        "transpose, on the grounds that scene objects rarely carry "
        "non-uniform scale. This is a defensible engineering decision as long "
        "as it is <i>decided</i> rather than overlooked. If you take it, "
        "assert on non-uniform scale in your asset pipeline so that the day "
        "someone squashes a prop you get an error rather than a mystery."),

  ("h1", "6 &nbsp; Reference table"),
  ("table", ["Quantity", "w", "Transform by", "Post-step"],
   [["Position", "1", "M", "Divide by w after projection."],
    ["Direction, tangent, bitangent", "0", "M",
     "Normalize if length matters."],
    ["Normal", "0", "(M&#8315;&#185;)&#7488;",
     "Always renormalize, including after interpolation."],
    ["Plane (n<sub>x</sub>, n<sub>y</sub>, n<sub>z</sub>, d)", "&mdash;",
     "(M&#8315;&#185;)&#7488; applied to the full 4-vector",
     "Renormalize n and rescale d consistently."],
    ["Ray direction", "0", "M", "Do not normalize before intersection tests "
     "if the test assumes parametric t in object units."]],
   [0.26, 0.07, 0.34, 0.33]),
 ],
 "resources": [
   ("3Blue1Brown — Essence of Linear Algebra",
    "https://www.3blue1brown.com/topics/linear-algebra",
    "Chapters 1–9. The best available geometric intuition for bases, "
    "determinants, and change of basis. Watch before this module if linear "
    "algebra feels like symbol-pushing."),
   ("GAMES101 Lecture 02 — Review of Linear Algebra",
    "https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html",
    "The same material aimed specifically at graphics, including the "
    "geometric meaning of both products."),
   ("Scratchapixel — Geometry",
    "https://www.scratchapixel.com/lessons/mathematics-physics-for-computer-graphics/geometry/",
    "Written reference with the normal-matrix derivation in full."),
   ("Immersive Math — interactive linear algebra",
    "http://immersivemath.com/ila/",
    "Manipulable figures. Useful for building intuition about frames and "
    "projections."),
 ],
 "exercises": [
   "Implement a <code>vec3</code>, <code>vec4</code>, and <code>mat4</code> "
   "with the standard operations. Write them yourself even though GLM exists "
   "— you will reason about the pipeline better for having done it once.",
   "Write a unit test that constructs a non-uniform scale, transforms a "
   "normal with M and with (M&#8315;&#185;)&#7488;, and asserts that only the "
   "second remains perpendicular to a transformed tangent. This test will "
   "catch the bug permanently.",
   "Implement <code>make_frame</code> and verify numerically, over ten "
   "thousand random normals, that the resulting basis is orthonormal to "
   "within floating-point tolerance and never produces NaN. Deliberately "
   "remove the guard and find the inputs that break it.",
   "Given a triangle's three vertices, compute its face normal and its area "
   "using one cross product. Confirm that reversing two vertices negates the "
   "normal and leaves the area magnitude unchanged.",
   "Take two unit vectors 60&deg; apart, interpolate linearly halfway between "
   "them, and measure the result's length. Explain in one sentence why "
   "interpolated normals darken the middle of large triangles if you do not "
   "renormalize.",
 ],
 "selfcheck": [
   "Why is point + point undefined, while a weighted average of two points "
   "with weights summing to one is perfectly well defined?",
   "State the equivalence relation on homogeneous coordinates, and explain "
   "why it is what makes perspective projection expressible as a matrix.",
   "What does w = 0 mean geometrically? Why is a directional light naturally "
   "w = 0?",
   "Derive the normal matrix from the requirement that n &middot; t = 0 be "
   "preserved.",
   "Under what transformations is the inverse transpose unnecessary, and why?",
   "Give two distinct reasons a normal might need renormalizing in the "
   "fragment shader, and say what each one looks like if you skip it.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Transformations: Model, View, Projection",
 "subtitle": "Deriving every matrix in the vertex shader.",
 "question": "Where does each of the three matrices come from, and why that order?",
 "outcomes": [
     "Derive translation, rotation, and scale matrices in homogeneous form.",
     "Explain why matrix order matters and predict the result of swapping two.",
     "Construct a view matrix from a camera position and orientation.",
     "Derive the perspective projection matrix and explain each entry.",
     "Explain depth precision, why it is non-linear, and how to improve it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The model matrix",
   "blurb": "Placing an object in the world."},

  {"t": "eq", "kicker": "Primitives", "title": "The three basic transforms",
   "eqs": [
     ("T(t)  —  identity with the translation in the last column",
      "Only reaches points (w = 1), which is the point of homogeneous "
      "coordinates."),
     ("S(s)  —  diagonal (sₓ, s_y, s_z, 1)",
      "Non-uniform scale is what forces the normal matrix of Module 02."),
     ("R(θ)  —  orthonormal, determinant +1",
      "Inverse is the transpose. Composition of rotations is a rotation."),
   ],
   "caption": "Every model matrix in your scene is a product of these three."},

  {"t": "callout", "title": "Order is not a convention", "kind": "Watch out",
   "body": ["Matrix multiplication does not commute, and the two orders mean "
            "genuinely different things.",
            "<b>T · R</b> rotates the object about its own origin, then "
            "moves it. The object spins in place.",
            "<b>R · T</b> moves the object away from the origin, then "
            "rotates the whole displaced result. The object orbits.",
            "Both are useful. Neither is a bug. But you must know which one "
            "you wrote."]},

  {"t": "bullets", "kicker": "Reading order", "title": "How to read a matrix product",
   "items": [
     "With column vectors, matrices apply <b>right to left</b>.",
     ("<code>P * V * M * v</code> means: M first, then V, then P.", 1),
     "",
     "Read the product right to left as a sequence of operations on the "
     "<i>object</i>.",
     "Or read it left to right as a sequence of changes of <i>frame</i>.",
     ("Both readings are correct and they are inverses of each other. Pick "
      "one and stay with it, because mixing them is how people get lost.", 1),
     "",
     "Row-vector conventions (DirectX historically) reverse everything. "
     "Neither is better; both are in the wild.",
   ],
   "note": "The object-vs-frame duality trips up almost everyone once. Being "
           "explicit about it here saves hours later."},

  {"t": "section", "label": "Part 2", "title": "The view matrix",
   "blurb": "There is no camera. There is only moving the world."},

  {"t": "callout", "title": "The camera is a fiction", "kind": "Key idea",
   "body": ["The pipeline has no concept of a camera. It renders whatever "
            "ends up in the canonical view volume looking down −Z.",
            "So instead of moving a camera to the scene, we move the scene to "
            "a fixed camera. The view matrix is the <i>inverse</i> of the "
            "transform that would place the camera in the world.",
            "If this feels backwards, that is because it is. Everything after "
            "it is simpler as a result."]},

  {"t": "code", "kicker": "Construction", "title": "Building look-at directly",
   "lang": "cpp", "code": """
mat4 look_at(vec3 eye, vec3 target, vec3 up) {
    vec3 f = normalize(eye - target);   // camera +Z (points BACKWARD)
    vec3 r = normalize(cross(up, f));   // camera +X (right)
    vec3 u = cross(f, r);               // camera +Y (true up)

    // Rotation part is orthonormal, so its inverse is its transpose:
    // write the basis vectors into the ROWS, not the columns.
    // Translation part is the negated, rotated eye position.
    return mat4(
        r.x,  r.y,  r.z, -dot(r, eye),
        u.x,  u.y,  u.z, -dot(u, eye),
        f.x,  f.y,  f.z, -dot(f, eye),
        0,    0,    0,    1);
}
""",
   "caption": "f points backward because OpenGL's camera looks down −Z. "
              "Getting this sign wrong gives you a camera that renders "
              "everything behind you — usually an empty screen.",
   "note": "Walk through why rows rather than columns: this IS the transpose, "
           "and the transpose IS the inverse. The -dot() terms are the "
           "rotated translation."},

  {"t": "section", "label": "Part 3", "title": "Projection",
   "blurb": "Making distant things small, without leaving linear algebra."},

  {"t": "bullets", "kicker": "The goal", "title": "What projection must achieve",
   "items": [
     "Map the view frustum — a truncated pyramid — onto the "
     "canonical cube [−1,1]³.",
     ("Clipping against a cube is trivial. Clipping against a pyramid is "
      "not. That is the real reason this stage exists.", 1),
     "",
     "Produce foreshortening: things further away must get smaller.",
     ("Screen position must scale as 1/z. Division is not linear.", 1),
     "",
     "<b>The trick:</b> arrange for the matrix to put view-space depth into "
     "<i>w</i>, then let the perspective divide do the division.",
   ]},

  {"t": "eq", "kicker": "Perspective", "title": "Similar triangles give the projection",
   "eqs": [
     ("x' = (n · x) / (−z)      y' = (n · y) / (−z)",
      "Pure similar triangles: project onto the plane at distance n from the eye."),
     ("so set  w_clip = −z_view",
      "Then the divide performs exactly that division, for free."),
     ("x_ndc = x_clip / w     y_ndc = y_clip / w     z_ndc = z_clip / w",
      "One divide, applied to all components, done by fixed-function hardware."),
   ],
   "caption": "The whole design is: make the matrix produce the right "
              "numerator and denominator, and let the hardware divide."},

  {"t": "code", "kicker": "Perspective", "title": "The perspective matrix, annotated",
   "lang": "cpp", "code": """
// fovy in radians, aspect = width/height, n and f are POSITIVE distances
mat4 perspective(float fovy, float aspect, float n, float f) {
    float t = 1.0f / tanf(fovy * 0.5f);   // cotangent of half-FOV

    return mat4(
      t/aspect, 0,  0,                 0,
      0,        t,  0,                 0,
      0,        0, -(f+n)/(f-n),  -2*f*n/(f-n),
      0,        0, -1,                 0);
    //            ^^ this -1 is what puts -z_view into w_clip.
}
""",
   "caption": "Row 3 maps the near plane to −1 and the far plane to +1. "
              "Row 4 is the entire perspective effect: it copies −z into "
              "w so the divide produces foreshortening.",
   "note": "Have them verify by hand: plug z = -n and z = -f into row 3 and "
           "divide by w = n and w = f respectively. They should get -1 and +1."},

  {"t": "two", "kicker": "Compare", "title": "Perspective and orthographic",
   "lh": "Perspective",
   "l": ["w varies per vertex (= −z).",
         "Parallel lines converge.",
         "Depth resolution is non-linear.",
         "Matches human vision and cameras.",
         ("Used for nearly all 3D scenes.", 1)],
   "rh": "Orthographic",
   "r": ["w = 1 for every vertex.",
         "Parallel lines stay parallel.",
         "Depth resolution is uniform.",
         "No foreshortening at all.",
         ("Used for CAD, 2D UI, and — importantly — directional "
          "light shadow maps (Module 10).", 1)],
   "note": "Flag the shadow-map connection now; it makes Module 10 land "
           "much faster."},

  {"t": "section", "label": "Part 4", "title": "Depth precision",
   "blurb": "Where z-fighting actually comes from."},

  {"t": "bullets", "kicker": "The problem", "title": "Why depth precision is uneven",
   "items": [
     "After the divide, z_ndc is a function of 1/z_view, not of z_view.",
     "So equal steps in the depth buffer are <b>not</b> equal steps in world "
     "distance.",
     "",
     "Precision concentrates near the near plane and thins out with distance.",
     ("Roughly: half of all depth buffer values describe the first few "
      "percent of your view distance.", 1),
     "",
     "Consequence: the <b>near plane</b> dominates precision, not the far "
     "plane.",
     ("Moving near from 0.01 to 0.1 helps enormously. Moving far from 1000 "
      "to 500 barely helps at all.", 1),
   ],
   "note": "This is counterintuitive and worth repeating. Students "
           "instinctively reach for the far plane."},

  {"t": "table", "kicker": "Fixes", "title": "What to do about z-fighting",
   "header": ["Fix", "How it works", "Cost"],
   "widths": [3.3, 5.6, 3.2],
   "rows": [
     ["Push the near plane out", "Directly attacks the dominant term",
      "Free; may clip close geometry"],
     ["Reversed-Z (far=0, near=1)", "Pairs 1/z with float's density near 0",
      "Free; needs GL_GREATER + clip control"],
     ["32-bit float depth", "More mantissa bits",
      "Bandwidth; often combined with reversed-Z"],
     ["Polygon offset", "Biases coplanar geometry apart",
      "Can cause peter-panning"],
     ["Just don't make it coplanar", "Fixes the asset, not the symptom",
      "Free, and usually correct"],
   ],
   "note": "Reversed-Z is close to a free win on modern hardware and is worth "
           "implementing in Project 2."},

  {"t": "code", "kicker": "Putting it together", "title": "The full chain, in order",
   "lang": "cpp", "code": """
// Once per frame
mat4 V = look_at(eye, target, up);
mat4 P = perspective(radians(60.0f), width/(float)height, 0.1f, 1000.0f);

// Once per object
mat4 M   = T(position) * R(rotation) * S(scale);   // read right to left:
                                                   // scale, rotate, place
mat4 MVP = P * V * M;
mat3 N   = transpose(inverse(mat3(M)));            // Module 02

// Per vertex (GPU)
vec4 clip = MVP * vec4(position, 1.0);
// -> hardware clips, divides by w, applies viewport. You are done.
""",
   "caption": "Three matrices, built at three different frequencies. Building "
              "any of them more often than necessary is a common and "
              "unnecessary cost."},
 ],
 "takeaways": [
   "Matrices apply right to left with column vectors. T·R spins in "
   "place; R·T orbits. Know which one you wrote.",
   "There is no camera. The view matrix is the inverse of the camera's world "
   "transform, and it is cheap because rotation is orthonormal.",
   "Projection exists to turn the frustum into a cube so clipping is trivial, "
   "and to put −z into w so the divide produces foreshortening.",
   "The perspective divide is the only non-linear step, and it is "
   "fixed-function. Everything else is a matrix multiply.",
   "Depth precision is a function of 1/z. The near plane dominates; pushing "
   "it out is the highest-value fix for z-fighting.",
   "Reversed-Z costs nothing and recovers most of the lost precision. Use it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Model: placing an object"),
  ("p", "The model matrix takes a vertex from the space the mesh was authored "
        "in to a shared world space. It is almost always a product of "
        "translation, rotation, and scale, and the order you multiply them in "
        "determines what the object does."),
  ("h2", "1.1 &nbsp; The three primitives"),
  ("code", """Translation T(tx,ty,tz)      Scale S(sx,sy,sz)     Rotation about Z, angle a
| 1 0 0 tx |                 | sx 0  0  0 |        | cos -sin  0  0 |
| 0 1 0 ty |                 | 0  sy 0  0 |        | sin  cos  0  0 |
| 0 0 1 tz |                 | 0  0  sz 0 |        |  0    0   1  0 |
| 0 0 0 1  |                 | 0  0  0  1 |        |  0    0   0  1 |"""),
  ("p", "Translation lives entirely in the fourth column, which is why it "
        "only reaches vertices with w = 1. Scale is diagonal. Rotation is "
        "orthonormal with determinant +1 — a determinant of &minus;1 "
        "would be a reflection, which flips winding order and makes your "
        "meshes render inside out."),
  ("h2", "1.2 &nbsp; Order"),
  ("callout", "The two orders mean different things",
   ["<b>T &middot; R</b> &mdash; rotation applied first, in the object's own "
    "frame, then the result is translated. The object spins on its own axis "
    "and then moves. This is what you almost always want.",
    "<b>R &middot; T</b> &mdash; translation first, then the whole displaced "
    "object is rotated about the world origin. The object orbits. Useful for "
    "exactly that, and a bug everywhere else."]),
  ("p", "The conventional model matrix is <code>T * R * S</code>: scale the "
        "object in its own frame, orient it, then place it. Reading right to "
        "left gives the sequence of operations applied to the object; reading "
        "left to right gives the sequence of frame changes. Both readings are "
        "valid, they are inverses of each other, and mixing them within a "
        "single debugging session is a reliable way to waste an afternoon."),

  ("h1", "2 &nbsp; View: the camera that is not there"),
  ("p", "The hardware renders whatever lands in the canonical view volume, "
        "viewed from the origin looking down &minus;Z. It has no notion of a "
        "camera anywhere else. So rather than moving a camera to the scene, "
        "we transform the scene into the camera's frame."),
  ("eq", "V = (camera's world transform)&#8315;&#185;"),
  ("p", "If the camera's world transform is a rotation R followed by a "
        "translation to position <b>e</b>, then V = (T(e) &middot; R)&#8315;&#185; "
        "= R&#8315;&#185; &middot; T(&minus;e) = R&#7488; &middot; T(&minus;e), "
        "using orthonormality from Module 02. That identity is what makes the "
        "view matrix essentially free to construct — no general inverse "
        "is ever computed."),
  ("h2", "2.1 &nbsp; look-at"),
  ("p", "Given an eye position, a target, and an approximate up vector, build "
        "the camera's orthonormal basis and write it transposed:"),
  ("code", """mat4 look_at(vec3 eye, vec3 target, vec3 up) {
    vec3 f = normalize(eye - target);   // camera +Z points BACKWARD
    vec3 r = normalize(cross(up, f));   // camera +X, right
    vec3 u = cross(f, r);               // camera +Y, true up
                                        // (orthogonalises a sloppy `up`)
    return mat4(
        r.x, r.y, r.z, -dot(r, eye),    // basis vectors go in the ROWS:
        u.x, u.y, u.z, -dot(u, eye),    // that is the transpose,
        f.x, f.y, f.z, -dot(f, eye),    // which is the inverse.
        0,   0,   0,    1);
}"""),
  ("callout", "Two things that bite here",
   ["<b>f points backward.</b> OpenGL's camera looks down &minus;Z, so the "
    "camera's own +Z axis points behind it. Get this sign wrong and you "
    "render the world behind the camera — usually an empty screen, "
    "occasionally a confusing mirror image.",
    "<b>The supplied `up` need not be exact.</b> It only has to be "
    "non-parallel to f; the double cross product orthogonalises it. But if it "
    "<i>is</i> parallel — look straight up with up = (0,1,0) — the "
    "first cross product degenerates and the view matrix fills with NaN. This "
    "is the classic 'camera explodes at the poles' bug."]),

  ("h1", "3 &nbsp; Projection"),
  ("p", "Projection has two jobs, and the second is less obvious than the "
        "first."),
  ("ul", ["<b>Foreshortening.</b> Distant objects must appear smaller, which "
          "requires dividing by depth.",
          "<b>Normalising the clip volume.</b> Map the frustum — a "
          "truncated pyramid — onto the cube [&minus;1,1]&#179;, so that "
          "clipping becomes six comparisons against constants instead of six "
          "arbitrary plane tests. This is the job that actually justifies the "
          "stage."]),
  ("h2", "3.1 &nbsp; Deriving the perspective matrix"),
  ("p", "Place a projection plane at distance <i>n</i> in front of the eye. "
        "By similar triangles, a point at view-space (x, y, z) with z "
        "negative projects to:"),
  ("eq", "x&prime; = n&middot;x / (&minus;z) &nbsp;&nbsp;&nbsp; y&prime; = n&middot;y / (&minus;z)"),
  ("p", "Division is not a linear operation, so no 4&times;4 matrix can "
        "perform it. But homogeneous coordinates already <i>end</i> in a "
        "division — the perspective divide by w. So we do not need the "
        "matrix to divide; we need it to arrange the right numerator and "
        "denominator. Setting the last row to (0, 0, &minus;1, 0) makes "
        "w_clip = &minus;z_view, and the hardware divide does the rest."),
  ("p", "The remaining freedom is row 3, which maps depth into "
        "[&minus;1, 1]. Writing it as z_clip = Az + B and requiring "
        "z_ndc = &minus;1 at z = &minus;n and +1 at z = &minus;f gives:"),
  ("eq", "A = &minus;(f+n)/(f&minus;n) &nbsp;&nbsp;&nbsp; B = &minus;2fn/(f&minus;n)"),
  ("code", """mat4 perspective(float fovy, float aspect, float n, float f) {
    float t = 1.0f / tanf(fovy * 0.5f);
    return mat4(
      t/aspect, 0,  0,                0,
      0,        t,  0,                0,
      0,        0, -(f+n)/(f-n), -2*f*n/(f-n),
      0,        0, -1,                0);
}"""),
  ("p", "Verify it by hand once. Put z = &minus;n into row 3: z_clip = "
        "n(f+n)/(f&minus;n) &minus; 2fn/(f&minus;n) = n(n&minus;f)/(f&minus;n) "
        "= &minus;n. And w_clip = n. So z_ndc = &minus;1. The far plane "
        "checks out the same way. Doing this once removes all mystery from "
        "the matrix."),
  ("h2", "3.2 &nbsp; Orthographic"),
  ("p", "An orthographic projection has no divide — the last row stays "
        "(0,0,0,1), so w remains 1. It is a scale and offset mapping a box "
        "onto the cube. Parallel lines stay parallel, depth precision is "
        "uniform, and there is no foreshortening. Beyond CAD and 2D overlays, "
        "the important use is <b>directional-light shadow maps</b> in Module "
        "10: the sun is infinitely far away, so its 'camera' is orthographic."),

  ("break",),
  ("h1", "4 &nbsp; Depth precision and z-fighting"),
  ("p", "Having divided by w, the stored depth is a function of 1/z rather "
        "than z. Depth buffer values are therefore distributed hyperbolically "
        "through the scene: densely near the camera, sparsely far away. The "
        "distribution depends almost entirely on the ratio f/n."),
  ("table", ["Near", "Far", "f/n", "Fraction of depth range used by the "
             "nearest 10% of the view distance"],
   [["0.01", "1000", "100,000", "~91%"],
    ["0.1", "1000", "10,000", "~90%"],
    ["1.0", "1000", "1,000", "~82%"],
    ["1.0", "100", "100", "~53%"]],
   [0.12, 0.12, 0.16, 0.60],
   "Indicative figures for a standard [&minus;1,1] depth mapping. The "
   "qualitative point is what matters: the near plane dominates, and a small "
   "f/n ratio is worth far more than a large depth buffer."),
  ("callout", "The counterintuitive part",
   ["Everyone's instinct on seeing z-fighting is to pull the <i>far</i> plane "
    "in. It barely helps.",
    "Pushing the <i>near</i> plane out helps enormously. Going from "
    "n = 0.01 to n = 0.1 is a tenfold improvement in the f/n ratio for the "
    "cost of clipping geometry within 10cm of the camera — almost always "
    "an acceptable trade."]),
  ("h2", "4.1 &nbsp; Reversed-Z"),
  ("p", "A near-free improvement. Map the near plane to 1 and the far plane "
        "to 0, use a floating-point depth buffer, and set the depth test to "
        "GREATER. Floating-point numbers are dense near zero; 1/z is also "
        "dense near... the far plane, once reversed. The two non-uniformities "
        "cancel almost exactly, and depth precision becomes nearly uniform "
        "across the whole range."),
  ("ul", ["Use a 32-bit float depth buffer (<code>GL_DEPTH_COMPONENT32F</code>).",
          "Set <code>glClipControl(GL_LOWER_LEFT, GL_ZERO_TO_ONE)</code>.",
          "Swap near and far in the projection matrix.",
          "Clear depth to 0 and set <code>glDepthFunc(GL_GREATER)</code>.",
          "Remember that any code reading depth — shadow maps, "
          "reconstruction from depth, SSAO — must be updated to match."]),

  ("h1", "5 &nbsp; The chain, at the right frequency"),
  ("p", "Three matrices, built at three different rates. Building any of them "
        "more often than its natural frequency is a common and entirely "
        "avoidable cost."),
  ("table", ["Matrix", "Rebuild when", "Typical frequency"],
   [["Projection P", "Field of view, aspect ratio, or clip planes change",
     "On window resize. Often once per run."],
    ["View V", "The camera moves or turns", "Once per frame."],
    ["Model M", "The object moves", "Once per object per frame, at most."],
    ["Normal matrix", "M changes",
     "With M. Never per vertex, never per fragment."]],
   [0.20, 0.42, 0.38]),
  ("code", """// Per frame
mat4 V = look_at(eye, target, up);

// Per object
mat4 M   = T(position) * R(rotation) * S(scale);
mat4 MVP = P * V * M;
mat3 Nrm = transpose(inverse(mat3(M)));

// Per vertex, on the GPU
gl_Position = MVP * vec4(aPos, 1.0);"""),
 ],
 "resources": [
   ("GAMES101 Lectures 03–04 — Transformation, Viewing",
    "https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html",
    "The clearest derivation of the perspective matrix available free, "
    "including the similar-triangles argument and the squish-then-ortho view."),
   ("Scratchapixel — The Perspective and Orthographic Projection Matrix",
    "https://www.scratchapixel.com/lessons/3d-basic-rendering/perspective-and-orthographic-projection-matrix/",
    "Full written derivation with every entry justified. The reference to "
    "reach for when a step in the derivation does not land."),
   ("LearnOpenGL — Coordinate Systems",
    "https://learnopengl.com/Getting-started/Coordinate-Systems",
    "The API mechanics: where each matrix goes and how to upload it."),
   ("NVIDIA — Depth Precision Visualized",
    "https://developer.nvidia.com/content/depth-precision-visualized",
    "The definitive treatment of depth precision and reversed-Z, with "
    "diagrams that make the 1/z distribution obvious."),
 ],
 "exercises": [
   "Implement <code>translate</code>, <code>scale</code>, "
   "<code>rotate_x/y/z</code>, <code>look_at</code>, <code>perspective</code>, "
   "and <code>orthographic</code>. Unit-test each by transforming known "
   "points and checking the results by hand.",
   "Verify the perspective matrix numerically: transform a point at "
   "z = &minus;n and one at z = &minus;f, divide by w, and assert that "
   "z_ndc is &minus;1 and +1 respectively.",
   "Build the same scene with <code>T*R</code> and with <code>R*T</code> and "
   "render both. Capture the two images and write one sentence explaining the "
   "difference to someone who has not taken this course.",
   "Plot depth-buffer value against world distance for f/n ratios of 100, "
   "1,000, and 100,000. Then implement reversed-Z and plot it on the same "
   "axes.",
   "Deliberately construct the degenerate look-at: camera looking straight "
   "down with up = (0,1,0). Observe the NaN, then fix it, and write down how "
   "you would detect this automatically.",
 ],
 "selfcheck": [
   "Why does the projection matrix map the frustum to a cube, when "
   "foreshortening alone would not require that?",
   "What specifically does the entry &minus;1 in the last row of the "
   "perspective matrix accomplish?",
   "The view matrix is described as 'the inverse of the camera transform'. "
   "Why is it cheap to compute despite being an inverse?",
   "Explain why depth precision depends far more on the near plane than on "
   "the far plane.",
   "How does reversed-Z recover precision? What two non-uniformities is it "
   "playing against each other?",
   "State in which order you would multiply T, R, and S for a conventional "
   "model matrix, and explain what each of the other orders would do.",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Rasterization: From Triangles to Fragments",
 "subtitle": "Deciding which pixels a triangle covers, and what they inherit.",
 "question": "How do you decide coverage without gaps, overlaps, or swimming textures?",
 "outcomes": [
     "Implement triangle coverage using edge functions.",
     "Apply a fill rule that makes shared edges neither doubled nor gapped.",
     "Derive barycentric coordinates and use them to interpolate attributes.",
     "Explain why screen-space linear interpolation is wrong, and correct it.",
     "Rasterize incrementally rather than re-evaluating per pixel.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Coverage",
   "blurb": "Is this sample inside this triangle?"},

  {"t": "eq", "kicker": "Edge functions", "title": "One function answers everything",
   "eqs": [
     ("E(p)  =  (pₓ − aₓ)(b_y − a_y) − (p_y − a_y)(bₓ − aₓ)",
      "The 2D cross product of edge ab with the vector from a to p."),
     ("E(p) > 0  →  p is left of edge ab",
      "The sign is the orientation. That is the entire inside test."),
     ("inside  ⟺  E₀(p), E₁(p), E₂(p) all share a sign",
      "Three edge functions, one sign comparison. No divisions, no branches."),
   ],
   "caption": "The same quantity is twice the signed area of triangle "
              "<i>abp</i> — which is why coverage and interpolation turn "
              "out to be the same computation.",
   "note": "Emphasise that this single expression gives coverage, winding, "
           "area, and barycentrics. It is the central object of the module."},

  {"t": "code", "kicker": "Coverage", "title": "The naive rasterizer",
   "lang": "cpp", "code": """
float edge(vec2 a, vec2 b, vec2 p) {
    return (p.x - a.x) * (b.y - a.y) - (p.y - a.y) * (b.x - a.x);
}

void raster(vec2 v0, vec2 v1, vec2 v2) {
    // Only visit pixels that could possibly be covered.
    int x0 = floor(min3(v0.x, v1.x, v2.x)), x1 = ceil(max3(...));
    int y0 = floor(min3(v0.y, v1.y, v2.y)), y1 = ceil(max3(...));

    for (int y = y0; y <= y1; ++y)
    for (int x = x0; x <= x1; ++x) {
        vec2 p = vec2(x + 0.5f, y + 0.5f);   // sample at pixel CENTRE
        float w0 = edge(v1, v2, p);
        float w1 = edge(v2, v0, p);
        float w2 = edge(v0, v1, p);
        if (w0 >= 0 && w1 >= 0 && w2 >= 0) emit_fragment(x, y, w0, w1, w2);
    }
}
""",
   "caption": "Sampling at the pixel centre, not the corner, is a convention "
              "— but it must be the same convention everywhere, or "
              "adjacent triangles disagree about their shared edge.",
   "note": "Note the bounding box: without it you test the whole screen per "
           "triangle. With it, cost is proportional to coverage."},

  {"t": "section", "label": "Part 2", "title": "Fill rules",
   "blurb": "What happens exactly on an edge decides whether your mesh has "
            "cracks."},

  {"t": "callout", "title": "The shared-edge problem", "kind": "Why this matters",
   "body": ["Two triangles share an edge. A sample lands exactly on it.",
            "If both triangles claim it, you get <b>double shading</b> "
            "— visible as a bright seam with transparency, and as "
            "wasted work always.",
            "If neither claims it, you get a <b>crack</b> — a one-pixel "
            "line of background showing through a solid mesh.",
            "Floating-point does not save you: the sample is exactly on the "
            "edge for both triangles, because they share the same vertices "
            "and therefore the same arithmetic."]},

  {"t": "bullets", "kicker": "The fix", "title": "The top-left rule",
   "items": [
     "A sample exactly on an edge belongs to the triangle if that edge is a "
     "<b>top</b> edge or a <b>left</b> edge.",
     ("<b>Top edge</b> — exactly horizontal, with the triangle below it.", 1),
     ("<b>Left edge</b> — going down, with the triangle to its right.", 1),
     "",
     "Each shared edge is a top-or-left edge of exactly one of the two "
     "triangles.",
     ("So exactly one claims it. No gaps, no overlaps, deterministic.", 1),
     "",
     "This is what GPUs implement. It is in the D3D and Vulkan specifications.",
   ],
   "note": "Students often skip this and then chase 'random sparkles' along "
           "mesh seams for days. Make them implement it in Project 1."},

  {"t": "code", "kicker": "The fix", "title": "Top-left as a bias",
   "lang": "cpp", "code": """
// Classify each edge once, before the pixel loop.
bool is_top_left(vec2 a, vec2 b) {
    bool top  = (a.y == b.y) && (b.x < a.x);   // horizontal, triangle below
    bool left = (b.y > a.y);                   // going down
    return top || left;
}

// Turn the rule into a constant bias so the inner loop stays branch-free:
// inclusive edges keep >= 0, exclusive edges effectively become > 0.
float bias0 = is_top_left(v1, v2) ? 0.0f : -EPS;
float bias1 = is_top_left(v2, v0) ? 0.0f : -EPS;
float bias2 = is_top_left(v0, v1) ? 0.0f : -EPS;

if (w0 + bias0 >= 0 && w1 + bias1 >= 0 && w2 + bias2 >= 0) { ... }
""",
   "caption": "With integer or fixed-point coordinates the bias is exactly "
              "−1 and the rule is exact. This is one of several reasons "
              "real GPUs rasterize in fixed point.",
   "note": "Good moment to mention sub-pixel precision: hardware typically "
           "uses 8 fractional bits, which is why very large triangles can "
           "show snapping artifacts."},

  {"t": "section", "label": "Part 3", "title": "Barycentric coordinates",
   "blurb": "Coverage and interpolation are the same computation."},

  {"t": "eq", "kicker": "Barycentrics", "title": "The edge functions were already the answer",
   "eqs": [
     ("λᵢ  =  Eᵢ(p) / (E₀ + E₁ + E₂)",
      "Normalize the three edge functions and you have barycentric weights."),
     ("λ₀ + λ₁ + λ₂  =  1,   all ≥ 0 inside",
      "An affine combination — legal for points, unlike a plain sum."),
     ("attr(p)  =  λ₀ a₀ + λ₁ a₁ + λ₂ a₂",
      "Interpolate anything: colour, normal, texcoord, depth, tangent."),
   ],
   "caption": "You computed the edge functions for the inside test. The "
              "weights come free — one reciprocal per fragment.",
   "note": "Connect back to Module 02: this is exactly the weighted average "
           "of points that IS well defined when weights sum to 1."},

  {"t": "section", "label": "Part 4", "title": "Perspective correction",
   "blurb": "The step whose absence produces swimming textures."},

  {"t": "callout", "title": "Linear in 3D is not linear on screen",
   "kind": "The problem",
   "body": ["A texture coordinate varies linearly across a triangle in "
            "<i>world</i> space. After perspective projection it does not "
            "vary linearly across the triangle in <i>screen</i> space.",
            "Projection divided by z, and division is not affine. Equal steps "
            "in screen space correspond to unequal steps on the surface "
            "— larger ones further away.",
            "Interpolate naively and the texture appears to slide, swim, or "
            "bend as the camera moves. It is most obvious on large floor "
            "polygons seen at a shallow angle, which is why it was so "
            "conspicuous in 1995-era console games."]},

  {"t": "eq", "kicker": "The correction", "title": "Interpolate attribute over w, then divide",
   "eqs": [
     ("1/w  is  affine in screen space",
      "The one quantity that survives projection linearly. Everything hangs "
      "off this."),
     ("interpolate  a/w  and  1/w  linearly",
      "Both are affine, so plain barycentric interpolation is correct for them."),
     ("a(p)  =  lerp(a/w) / lerp(1/w)",
      "One extra divide per fragment per attribute set. That is the whole cost."),
   ],
   "caption": "Hardware does this for you. In a software rasterizer you must "
              "do it yourself, and Project 1 requires it.",
   "note": "Note that depth z_ndc is already the result of a divide, so it IS "
           "screen-affine and must NOT be perspective-corrected. Getting this "
           "backwards is a common bug."},

  {"t": "code", "kicker": "The correction", "title": "Perspective-correct interpolation",
   "lang": "cpp", "code": """
// After the perspective divide, keep 1/w for every vertex.
float iw0 = 1.0f / c0.w, iw1 = 1.0f / c1.w, iw2 = 1.0f / c2.w;

// Per fragment, with screen-space barycentrics l0, l1, l2:
float iw = l0*iw0 + l1*iw1 + l2*iw2;          // affine: correct as-is

// Perspective-correct weights, computed once per fragment:
float p0 = l0 * iw0 / iw;
float p1 = l1 * iw1 / iw;
float p2 = l2 * iw2 / iw;

vec2 uv     = p0*uv0 + p1*uv1 + p2*uv2;       // CORRECTED
vec3 normal = p0*n0  + p1*n1  + p2*n2;        // CORRECTED

float depth = l0*z0 + l1*z1 + l2*z2;          // NOT corrected: z_ndc
                                              // is already screen-affine
""",
   "caption": "Compute the corrected weights once, then reuse them for every "
              "attribute. Correcting depth as well is a real and common bug.",
   "note": "Have students render with and without and diff the images. The "
           "difference on a floor plane is unmistakable."},

  {"t": "section", "label": "Part 5", "title": "Making it fast",
   "blurb": "The same answer, with far less arithmetic."},

  {"t": "bullets", "kicker": "Incremental", "title": "Edge functions are affine, so step them",
   "items": [
     "E(x+1, y) = E(x, y) + (b_y − a_y)",
     "E(x, y+1) = E(x, y) + (aₓ − bₓ)",
     "",
     "So: evaluate once per triangle at the bounding-box corner, then add "
     "per pixel.",
     ("Three multiplies and three subtractions per pixel become three "
      "additions.", 1),
     "",
     "Better still: evaluate a 2×2 or 8×8 block at once.",
     ("If all four corners of a block are outside the same edge, the whole "
      "block is outside — skip it.", 1),
     ("This is roughly what real hardware does, in a hierarchy.", 1),
   ],
   "note": "Connect to CSCE 735: this is also what makes rasterization "
           "SIMD-friendly, since the per-pixel work becomes a vector add."},

  {"t": "table", "kicker": "Diagnosis", "title": "Rasterization artifacts",
   "header": ["What you see", "Cause"],
   "widths": [5.0, 7.1],
   "rows": [
     ["One-pixel cracks along shared edges", "No fill rule, or inconsistent sample position"],
     ["Bright seams on transparent geometry", "Double-shaded shared edges — same cause"],
     ["Texture slides as camera moves", "Interpolation not perspective-corrected"],
     ["Texture correct, depth wrong", "Depth perspective-corrected when it should not be"],
     ["Triangles vanish at glancing angles", "Degenerate triangle: near-zero area, sign unstable"],
     ["Geometry snaps as it moves slowly", "Insufficient sub-pixel precision in fixed point"],
   ]},
 ],
 "takeaways": [
   "One edge function gives you coverage, winding, area, and barycentric "
   "weights. It is the whole module in a single expression.",
   "The top-left rule decides ties on shared edges so exactly one triangle "
   "claims each sample. Without it you get cracks or double shading.",
   "Barycentric weights are the normalized edge functions — free, once "
   "you have done the inside test.",
   "1/w is the quantity that stays affine under projection. Interpolate a/w "
   "and 1/w, then divide.",
   "Depth in NDC is already the result of a divide, so it must NOT be "
   "perspective-corrected. Attributes must.",
   "Edge functions are affine, so step them incrementally and reject whole "
   "blocks at once. That is what makes rasterization fast.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The coverage question"),
  ("p", "Rasterization asks one question repeatedly: does this sample point "
        "lie inside this triangle? Everything else in the stage — "
        "interpolation, fill rules, hierarchical traversal — is built "
        "from the machinery that answers it."),
  ("h2", "1.1 &nbsp; Edge functions"),
  ("p", "For a directed edge from <b>a</b> to <b>b</b> and a sample point "
        "<b>p</b>, define:"),
  ("eq", "E<sub>ab</sub>(p) = (p&#8339; &minus; a&#8339;)(b<sub>y</sub> &minus; a<sub>y</sub>) &minus; (p<sub>y</sub> &minus; a<sub>y</sub>)(b&#8339; &minus; a&#8339;)"),
  ("p", "This is the z-component of the cross product of (b &minus; a) with "
        "(p &minus; a) — the 2D cross product. Its sign tells you which "
        "side of the directed line <b>p</b> falls on, and its magnitude is "
        "twice the area of triangle <i>abp</i>. A point is inside the "
        "triangle exactly when the three edge functions, taken with "
        "consistent winding, all have the same sign."),
  ("callout", "One expression, four jobs",
   ["<b>Sign</b> &rarr; inside/outside test.",
    "<b>Sign of the sum</b> &rarr; winding order, hence backface culling.",
    "<b>Magnitude</b> &rarr; twice the sub-triangle area.",
    "<b>Normalized magnitude</b> &rarr; barycentric coordinates, hence "
    "attribute interpolation.",
    "This is why edge functions, rather than scanline algorithms, are how "
    "modern rasterization is done."]),
  ("h2", "1.2 &nbsp; Sample position"),
  ("p", "Pixels are areas, but we test points. The convention is to sample at "
        "the pixel <b>centre</b>: pixel (x, y) is tested at (x + 0.5, "
        "y + 0.5). The specific convention matters less than its "
        "<i>consistency</i>: if two triangles sharing an edge are tested at "
        "even slightly different points, the shared edge will leak."),

  ("h1", "2 &nbsp; Fill rules"),
  ("p", "Consider two triangles sharing an edge, and a sample that lands "
        "exactly on it. Both triangles compute E = 0 for that edge — "
        "not approximately zero, but exactly, because they share vertices and "
        "therefore perform identical arithmetic. Floating-point tolerance "
        "does not help; the values genuinely are equal."),
  ("p", "If the test is <code>&gt;= 0</code> for both, both triangles claim "
        "the sample. The fragment is shaded twice: wasted work always, and a "
        "visible bright seam wherever blending is enabled. If the test is "
        "<code>&gt; 0</code> for both, neither claims it, and a one-pixel "
        "crack of background shows through what should be a solid surface."),
  ("h2", "2.1 &nbsp; The top-left rule"),
  ("p", "Make the inclusion decision depend on the <i>edge</i>, not on the "
        "triangle. An on-edge sample belongs to the triangle if the edge in "
        "question is a top edge or a left edge:"),
  ("ul", ["<b>Top edge</b>: exactly horizontal, with the triangle's interior "
          "below it.",
          "<b>Left edge</b>: an edge that goes downward in screen space, with "
          "the interior to its right."]),
  ("p", "Because the two triangles traverse the shared edge in opposite "
        "directions, the edge is top-or-left for exactly one of them. Exactly "
        "one claims the sample. No gaps, no double shading, and the result is "
        "deterministic and order-independent. This rule is normative in both "
        "the Direct3D and Vulkan specifications; GPUs implement it in "
        "hardware."),
  ("code", """bool is_top_left(vec2 a, vec2 b) {
    bool top  = (a.y == b.y) && (b.x < a.x);   // horizontal, interior below
    bool left = (b.y > a.y);                   // descending edge
    return top || left;
}

// Classify once per triangle; apply as a bias so the inner loop
// stays branch-free. With integer coordinates EPS is exactly 1.
float b0 = is_top_left(v1, v2) ? 0 : -EPS;
float b1 = is_top_left(v2, v0) ? 0 : -EPS;
float b2 = is_top_left(v0, v1) ? 0 : -EPS;

if (w0 + b0 >= 0 && w1 + b1 >= 0 && w2 + b2 >= 0)
    emit_fragment(...);"""),
  ("callout", "Why hardware rasterizes in fixed point",
   ["With floating-point coordinates the 'exactly on the edge' case is "
    "fragile and the bias is a fudge. With fixed-point coordinates — "
    "typically 8 sub-pixel fractional bits — the comparison is exact and "
    "the rule is watertight.",
    "The cost is a bound on coordinate range, which is why extremely large "
    "triangles can show vertex snapping. This is a real constraint in "
    "engines, not a curiosity."]),

  ("break",),
  ("h1", "3 &nbsp; Barycentric coordinates"),
  ("p", "Having computed the three edge functions for the coverage test, "
        "normalize them:"),
  ("eq", "&lambda;&#7522; = E&#7522;(p) / (E&#8320; + E&#8321; + E&#8322;)"),
  ("p", "The denominator is twice the full triangle area and is constant per "
        "triangle, so this costs one reciprocal per triangle and one multiply "
        "per weight. The resulting weights are non-negative inside the "
        "triangle and sum to one — which, as Module 02 noted, is exactly "
        "the condition under which a weighted sum of <i>points</i> is "
        "meaningful."),
  ("p", "Any per-vertex attribute now interpolates as "
        "&lambda;&#8320;a&#8320; + &lambda;&#8321;a&#8321; + "
        "&lambda;&#8322;a&#8322;. Colour, normal, texture coordinate, "
        "tangent, depth — all the same operation. Coverage and "
        "interpolation turn out to be a single computation, which is the "
        "elegant fact at the centre of this module."),

  ("h1", "4 &nbsp; Perspective-correct interpolation"),
  ("h2", "4.1 &nbsp; Why naive interpolation fails"),
  ("p", "A texture coordinate varies linearly over the triangle's surface in "
        "3D. Projection divided every coordinate by w, and division is not an "
        "affine map, so linear variation in 3D does not survive as linear "
        "variation in 2D. Walking across the triangle in equal screen-space "
        "steps corresponds to unequal steps across the actual surface "
        "— larger steps where the surface is further away."),
  ("p", "Interpolating linearly in screen space therefore stretches the "
        "texture incorrectly, and because the error depends on the camera, it "
        "changes as you move: the texture appears to swim or slide over the "
        "geometry. Shallow-angle floors show it most, and splitting the "
        "polygon into many small triangles reduces it — which is why "
        "some early software renderers subdivided geometry as a workaround."),
  ("h2", "4.2 &nbsp; The correction"),
  ("p", "One quantity does survive projection as an affine function of screen "
        "position: 1/w. So interpolate <i>a</i>/w and 1/w linearly, both of "
        "which is valid, and divide at the end:"),
  ("eq", "a(p) = [ &Sigma; &lambda;&#7522; (a&#7522;/w&#7522;) ] / [ &Sigma; &lambda;&#7522; (1/w&#7522;) ]"),
  ("code", """float iw0 = 1.0f/c0.w, iw1 = 1.0f/c1.w, iw2 = 1.0f/c2.w;

// per fragment
float iw = l0*iw0 + l1*iw1 + l2*iw2;
float p0 = l0*iw0/iw, p1 = l1*iw1/iw, p2 = l2*iw2/iw;

uv     = p0*uv0 + p1*uv1 + p2*uv2;   // corrected
normal = p0*n0  + p1*n1  + p2*n2;    // corrected
depth  = l0*z0  + l1*z1  + l2*z2;    // NOT corrected""",
   "Compute the corrected weights once per fragment and reuse them for every "
   "attribute. Interpolating depth with the corrected weights is a real and "
   "frequent bug."),
  ("callout", "Depth is the exception",
   ["z_ndc is already the output of the perspective divide. It is therefore "
    "<i>already</i> an affine function of screen position, and interpolating "
    "it with plain screen-space barycentrics is correct.",
    "Apply the perspective correction to depth and you get subtly wrong "
    "occlusion, which looks like mild z-fighting and sends people hunting in "
    "entirely the wrong place.",
    "Rule: anything that was linear <i>in 3D</i> needs correction; anything "
    "that is already a post-divide screen quantity does not."]),

  ("h1", "5 &nbsp; Making it fast"),
  ("p", "The edge function is affine in screen position, so its value at the "
        "next pixel differs from the current one by a constant:"),
  ("eq", "E(x+1, y) = E(x, y) + (b<sub>y</sub> &minus; a<sub>y</sub>) &nbsp;&nbsp;&nbsp; E(x, y+1) = E(x, y) + (a&#8339; &minus; b&#8339;)"),
  ("p", "Evaluate the three edge functions once at a corner of the bounding "
        "box, then add constants as you walk. Three multiplies and three "
        "subtractions per pixel collapse into three additions, and the inner "
        "loop vectorises trivially across four or eight pixels at once."),
  ("p", "The larger win is hierarchical. Test a block of pixels — "
        "8&times;8, say — by evaluating the edge functions at its "
        "corners. If all four corners lie outside the same edge, every pixel "
        "in the block is outside, and the block is skipped without touching a "
        "single pixel. If all four are inside all three edges, the block is "
        "entirely covered and the inside test can be skipped per pixel. Only "
        "partially covered blocks need per-pixel work, and those are a small "
        "fraction of a typical triangle's area. Real GPUs do this in a "
        "multi-level hierarchy, and it is a large part of why rasterization "
        "is so fast."),

  ("h1", "6 &nbsp; Artifact table"),
  ("table", ["What you see", "Cause", "Fix"],
   [["One-pixel cracks along shared edges",
     "No fill rule, or sample positions differ between triangles.",
     "Implement top-left; sample consistently at pixel centres."],
    ["Bright seams on alpha-blended geometry",
     "Shared-edge samples shaded twice.",
     "Same fix. The seam is the double-blend."],
    ["Textures swim or slide with camera motion",
     "Screen-space linear interpolation of attributes.",
     "Perspective-correct: interpolate a/w and 1/w, then divide."],
    ["Occlusion subtly wrong, mild z-fighting",
     "Depth perspective-corrected when it should not be.",
     "Interpolate z_ndc with plain screen-space barycentrics."],
    ["Thin triangles flicker or disappear",
     "Near-degenerate area; the edge-function sum approaches zero and its "
     "sign becomes unstable.",
     "Cull triangles below an area threshold before rasterizing."],
    ["Vertices snap as geometry moves slowly",
     "Sub-pixel precision exhausted in fixed point.",
     "Reduce triangle size, or increase fractional bits."]],
   [0.26, 0.42, 0.32]),
 ],
 "resources": [
   ("GAMES101 Lectures 05–06 — Rasterization",
    "https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html",
    "Coverage, the inside test, and the introduction to sampling that sets "
    "up Module 09."),
   ("Fabian Giesen — 'A trip through the Graphics Pipeline' and the "
    "rasterization series",
    "https://fgiesen.wordpress.com/2011/07/09/a-trip-through-the-graphics-pipeline-2011-index/",
    "The best free writing on how real hardware rasterizes: fill rules, "
    "fixed point, hierarchical traversal. Essential reading for this module."),
   ("Scratchapixel — Rasterization: a Practical Implementation",
    "https://www.scratchapixel.com/lessons/3d-basic-rendering/rasterization-practical-implementation/",
    "Full working code including the perspective-correction derivation."),
   ("CMU 15-462 — Drawing a Triangle / Sampling",
    "https://15462.courses.cs.cmu.edu/",
    "Frames coverage as a sampling problem, which is the framing Module 09 "
    "builds on."),
 ],
 "exercises": [
   "Implement the edge-function rasterizer with a bounding box. Render a "
   "single large triangle and confirm the coverage is exact at the edges.",
   "Implement the top-left fill rule. Render two triangles sharing an edge, "
   "each in a different colour with 50% alpha, and verify at 8&times; "
   "magnification that the shared edge is neither doubled nor cracked. "
   "Capture before and after.",
   "Implement barycentric interpolation and render a triangle with the three "
   "vertices coloured red, green, and blue. The result should be a smooth "
   "gradient with no banding.",
   "Implement perspective-correct interpolation. Render a large textured "
   "floor plane at a shallow angle, with and without correction, and capture "
   "both. This is a required deliverable of Project 1.",
   "Convert the inner loop to incremental edge stepping and measure the "
   "speedup on a 5,000-triangle mesh. Then add 8&times;8 block rejection and "
   "measure again.",
   "Deliberately apply the perspective correction to depth as well. Describe "
   "precisely what goes wrong and why it is easy to misdiagnose.",
 ],
 "selfcheck": [
   "Write the edge function from memory and state four distinct things its "
   "value tells you.",
   "Why does floating-point tolerance not solve the shared-edge problem?",
   "State the top-left rule and explain why it guarantees exactly one "
   "triangle claims each on-edge sample.",
   "How are barycentric coordinates obtained from the edge functions, and why "
   "is this essentially free?",
   "Explain why screen-space linear interpolation of texture coordinates is "
   "wrong, and name the one quantity that is affine in screen space.",
   "Which interpolated quantity must <i>not</i> be perspective-corrected, and "
   "why?",
   "Describe how block-based hierarchical rasterization reduces per-pixel "
   "work, and what determines how much it helps.",
 ],
},

]
