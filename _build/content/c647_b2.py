# -*- coding: utf-8 -*-
"""CSCE 647 — Modules 03-07."""

MODULES = [

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Rays and Intersection",
 "subtitle": "The primitive operation, and the numerical trouble in it.",
 "question": "How do you intersect a ray with geometry without it breaking?",
 "outcomes": [
     "Derive ray-sphere and ray-triangle intersection.",
     "Explain what watertightness means and why it matters.",
     "Solve the self-intersection problem without a magic epsilon.",
     "Explain ray differentials and what they are for.",
     "Design the intersection interface a renderer actually needs.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The basic operation",
   "blurb": "A ray, a primitive, and the smallest positive root."},

  {"t": "eq", "kicker": "Setup", "title": "Rays",
   "eqs": [
     ("r(t)  =  o + t d,    t ∈ [tmin, tmax]",
      "Origin, direction, and a valid parameter interval. The interval is "
      "not optional — it is how shadow rays and epsilons are expressed."),
     ("‖d‖ = 1  is a choice, not a requirement",
      "Normalised directions make t a distance. Unnormalised directions let "
      "you transform a ray into object space without renormalising."),
   ],
   "caption": "Keep tmin and tmax in the ray. Almost every robustness fix in "
              "this module is expressed through them.",
   "note": "Students often store rays as just (o,d) and bolt the interval on "
           "later. Starting with it in the struct avoids a rewrite."},

  {"t": "eq", "kicker": "Sphere", "title": "Ray–sphere, and the subtraction that kills it",
   "eqs": [
     ("‖o + t d − c‖² = r²   ⟹   a t² + b t + c = 0",
      "Substitute and expand. A quadratic, solved the way everyone learns "
      "in school."),
     ("t = (−b ± √(b² − 4ac)) / 2a     ← catastrophic cancellation",
      "When b² ≫ 4ac, one root computes as the difference of two nearly "
      "equal numbers and loses most of its precision."),
     ("q = −½(b + sign(b)√(b²−4ac)),   t₁ = q/a,  t₂ = c/q",
      "The stable form. Same roots, no cancellation, three extra lines."),
   ],
   "caption": "This matters at grazing angles and for large spheres — "
              "exactly the planet-scale cases where the artefact is most "
              "visible.",
   "note": "A good first encounter with the theme: the textbook formula is "
           "correct in exact arithmetic and wrong in floating point."},

  {"t": "code", "kicker": "Triangle", "title": "Möller–Trumbore",
   "lang": "cpp", "code": """
// Solves o + t·d = (1-u-v)·v0 + u·v1 + v·v2 for (t, u, v).
// Cramer's rule on a 3x3 system; no precomputation, no plane stored.
bool intersect(const Ray& r, const Tri& T, Hit& h) {
    vec3 e1 = T.v1 - T.v0,  e2 = T.v2 - T.v0;
    vec3 pv = cross(r.d, e2);
    float det = dot(e1, pv);
    if (fabs(det) < 1e-12f) return false;      // ray parallel to triangle
    float inv = 1.0f / det;

    vec3  tv = r.o - T.v0;
    float u  = dot(tv, pv) * inv;
    if (u < 0 || u > 1) return false;

    vec3  qv = cross(tv, e1);
    float v  = dot(r.d, qv) * inv;
    if (v < 0 || u + v > 1) return false;

    float t = dot(e2, qv) * inv;
    if (t < r.tmin || t > r.tmax) return false;
    h = {t, u, v};                              // u,v are barycentrics
    return true;
}
""",
   "caption": "Returns barycentric coordinates for free, which you need for "
              "interpolating normals, UVs, and vertex colours.",
   "note": "Point out that the early-out ordering matters for performance: "
           "u before computing qv."},

  {"t": "section", "label": "Part 2", "title": "Watertightness",
   "blurb": "Why light leaks through a closed mesh."},

  {"t": "callout", "title": "Adjacent triangles can both miss the same ray",
   "kind": "The problem",
   "body": ["Two triangles share an edge exactly. A ray passes exactly "
            "through that edge.",
            "<b>Each triangle's test is performed in floating point, "
            "separately, with different rounding.</b> One rounds the ray "
            "just outside; the other does too.",
            "The ray passes through a solid object. In a path tracer this "
            "appears as isolated bright or black pixels on silhouettes and "
            "creases — and they <i>move</i> as the camera moves.",
            "<b>A watertight intersection test guarantees this cannot "
            "happen</b>: shared edges are evaluated identically from both "
            "sides."]},

  {"t": "bullets", "kicker": "Fix", "title": "How watertight tests work",
   "items": [
     "<b>Transform the ray to a canonical space</b> where its direction is "
     "(0,0,1), chosen by the largest-magnitude component.",
     "",
     "<b>Project vertices to 2D</b> and compute three edge functions.",
     "",
     "<b>Compute the edge functions in a canonical vertex order</b>, so both "
     "triangles sharing an edge compute bitwise identical values.",
     "",
     "<b>Fall back to double precision</b> when an edge function is exactly "
     "zero.",
     "",
     "Woop et al. 2013. PBRT implements it; cost is roughly 10%.",
   ],
   "footnote": "Ten percent to eliminate a class of artefact that is "
               "otherwise undebuggable.",
   "note": "The canonical ordering is the clever part — determinism is "
           "what buys watertightness, not extra precision."},

  {"t": "section", "label": "Part 3", "title": "Self-intersection",
   "blurb": "The most common bug in a first ray tracer."},

  {"t": "callout", "title": "Shadow acne is a floating-point problem",
   "kind": "Why it happens",
   "body": ["A path hits a surface at t, computes p = o + t·d, and spawns a "
            "new ray from p.",
            "<b>p is not exactly on the surface</b> — it is the nearest "
            "representable float, which may be slightly below it. The new "
            "ray immediately hits the surface it just left, at t ≈ 0.",
            "The result is dark speckle, worst where the surface is far from "
            "the origin — because float spacing grows with magnitude.",
            "<b>The usual fix, tmin = 1e-4, is wrong.</b> Too small and acne "
            "returns far from the origin; too large and contact shadows "
            "detach. There is no single correct value."]},

  {"t": "code", "kicker": "Fix", "title": "Offset in integers, not in floats",
   "lang": "cpp", "code": """
// Wachter & Binder 2019 (Ray Tracing Gems ch. 6).
// Scale the offset with the float spacing at p, automatically.
vec3 offset_ray(const vec3 p, const vec3 n) {
    constexpr float origin      = 1.0f / 32.0f;
    constexpr float float_scale = 1.0f / 65536.0f;
    constexpr float int_scale   = 256.0f;

    ivec3 of_i(int_scale*n.x, int_scale*n.y, int_scale*n.z);

    // Step p by N units in the LAST PLACE -- scale-invariant by construction.
    vec3 p_i(int_as_float(float_as_int(p.x) + (p.x < 0 ? -of_i.x : of_i.x)),
             int_as_float(float_as_int(p.y) + (p.y < 0 ? -of_i.y : of_i.y)),
             int_as_float(float_as_int(p.z) + (p.z < 0 ? -of_i.z : of_i.z)));

    // Near the origin, ULP steps are too small; fall back to a fixed offset.
    return vec3(fabs(p.x) < origin ? p.x + float_scale*n.x : p_i.x,
                fabs(p.y) < origin ? p.y + float_scale*n.y : p_i.y,
                fabs(p.z) < origin ? p.z + float_scale*n.z : p_i.z);
}
""",
   "caption": "Offsetting in units-in-the-last-place adapts to the local "
              "float spacing automatically. No scene-dependent epsilon.",
   "note": "This is the single most useful code on the slide deck. It "
           "eliminates a whole category of bug permanently."},

  {"t": "section", "label": "Part 4", "title": "Ray differentials",
   "blurb": "How a ray knows how wide it is."},

  {"t": "two", "kicker": "Why", "title": "The texture filtering problem, again",
   "lh": "Rasteriser",
   "l": ["Neighbouring pixels are shaded together.",
         "Hardware computes screen-space derivatives by differencing within "
         "a 2×2 quad.",
         ("Texture LOD comes free.", 1),
         "<b>You had this in CSCE 641 and never thought about it.</b>"],
   "rh": "Ray tracer",
   "r": ["Each ray is independent. There is no neighbour.",
         "Nothing tells you how much texture a ray covers.",
         ("Use the finest mip level and alias badly.", 1),
         "<b>Fix: carry two auxiliary rays, offset one pixel in x and y.</b>"],
   "note": "This is a good moment to show that a convenience of the "
           "rasteriser becomes explicit work here."},

  {"t": "callout", "title": "Differentials propagate, and degrade",
   "kind": "The practical limit",
   "body": ["Track ∂p/∂x and ∂p/∂y alongside the ray. At a hit, convert them "
            "into ∂u/∂x and ∂u/∂y and use those to choose a mip level.",
            "<b>They survive specular reflection and refraction</b>, with "
            "correction terms for surface curvature.",
            "<b>They do not survive diffuse bounces</b>, where the outgoing "
            "direction is random and the footprint is meaningless.",
            "So in practice: use differentials on camera rays and specular "
            "chains, and use <b>path-space filtering or a fixed blur</b> "
            "after the first diffuse bounce. Most production renderers do "
            "exactly this."]},

  {"t": "table", "kicker": "Interface", "title": "What intersection must return",
   "header": ["Field", "For", "Note"],
   "widths": [2.6, 4.8, 4.7],
   "rows": [
     ["t", "Ordering, ray interval", "The only field a shadow ray needs"],
     ["p", "Next ray origin", "<b>Offset it (Part 3)</b>"],
     ["ng", "Geometric normal", "<b>From the actual triangle</b> — for offsetting"],
     ["ns", "Shading normal", "Interpolated; may disagree with ng"],
     ["u, v", "Textures, derivatives", "Barycentric, free from Möller–Trumbore"],
     ["dpdu, dpdv", "Tangent frame", "Anisotropy, normal mapping"],
     ["prim", "Material lookup", "A pointer or index"],
   ],
   "note": "Keeping ng and ns separate is non-negotiable; conflating them "
           "produces light leaks and energy loss at silhouettes."},

  {"t": "callout", "title": "Geometric and shading normals are different things",
   "kind": "Keep both",
   "body": ["<b>ng</b> is perpendicular to the actual triangle. It defines "
            "which side you are on, and it is the correct normal to offset "
            "along.",
            "<b>ns</b> is interpolated from vertex normals, possibly "
            "perturbed by a normal map. It is what you shade with.",
            "They disagree near silhouettes, and the disagreement is the "
            "point of smooth shading.",
            "<b>If you use ns for offsetting</b>, rays can be offset to the "
            "wrong side of the surface. <b>If you use ng for shading</b>, "
            "your smooth meshes are faceted. Both bugs are common and both "
            "are avoided by storing both."]},

  {"t": "bullets", "kicker": "Shadow rays", "title": "A shadow ray is not a normal ray",
   "items": [
     "<b>It is a yes/no question</b>, so it can return at the first hit "
     "rather than the nearest.",
     "",
     "<b>It is typically 2–3× faster</b> for that reason. Implement a "
     "separate <code>occluded()</code> rather than calling "
     "<code>intersect()</code> and discarding.",
     "",
     "<b>Set tmax just short of the light</b> so the light's own geometry "
     "does not occlude it.",
     "",
     "<b>Offset at both ends</b> — the surface <i>and</i> the light.",
   ],
   "footnote": "Next-event estimation (Module 08) makes shadow rays the "
               "majority of all rays cast. The 2–3× is worth having."},
 ],
 "takeaways": [
   "Store tmin and tmax in the ray. Most robustness fixes are expressed "
   "through the interval.",
   "The textbook quadratic formula loses precision on ray-sphere "
   "intersection at grazing angles. Use the stable form.",
   "Möller–Trumbore gives t and barycentrics with no precomputation and no "
   "stored plane equation.",
   "Watertightness comes from evaluating shared edges identically from both "
   "sides — determinism, not extra precision. About 10% cost.",
   "Self-intersection is a float-spacing problem; offset in units-in-the-"
   "last-place rather than choosing a scene-dependent epsilon.",
   "Keep geometric and shading normals separate: offset along ng, shade with "
   "ns. Conflating them causes leaks or faceting.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Rays"),
  ("eq", "r(t) = o + t d, &nbsp;&nbsp; t &isin; [t<sub>min</sub>, "
         "t<sub>max</sub>]"),
  ("p", "The interval is part of the ray, not an afterthought. A shadow ray "
        "is a ray whose t<sub>max</sub> stops just short of the light; "
        "self-intersection avoidance historically used t<sub>min</sub>; and "
        "BVH traversal (Module 04) shrinks t<sub>max</sub> as closer hits are "
        "found, which is where much of its pruning power comes from. Put the "
        "interval in the struct from the beginning."),
  ("p", "Whether to normalise <b>d</b> is a genuine design choice. With a "
        "normalised direction, t is a distance, which is convenient. With an "
        "unnormalised direction, a ray can be transformed into an object's "
        "local space by a matrix multiply without renormalising, and t "
        "retains its meaning in that space — which matters for "
        "instancing. PBRT leaves directions unnormalised for this reason."),
  ("h2", "1.1 &nbsp; Ray&ndash;sphere, and a lesson in floating point"),
  ("p", "Substituting the ray into the implicit sphere equation gives a "
        "quadratic. The formula everyone learned at school is numerically "
        "poor:"),
  ("eq", "t = ( &minus;b &plusmn; &radic;(b&#178; &minus; 4ac) ) / 2a"),
  ("p", "When b&#178; is much larger than 4ac — which happens for "
        "grazing rays and for spheres large relative to their distance "
        "— the square root is very close to |b|, and one of the two "
        "roots is computed as the difference of two nearly equal numbers. "
        "This is <b>catastrophic cancellation</b>: the leading significant "
        "digits cancel and the result is dominated by rounding error."),
  ("eq", "q = &minus;&frac12;( b + sign(b) &radic;(b&#178; &minus; 4ac) ) "
         "&nbsp;&nbsp;&nbsp; t&#8321; = q / a, &nbsp; t&#8322; = c / q"),
  ("callout", "The textbook formula is correct and unusable",
   ["Both forms give the same roots in exact arithmetic. In floating point "
    "the second is accurate and the first is not, and the difference shows "
    "up precisely in the configurations that look most impressive: a "
    "planet-scale sphere, a grazing horizon ray, an atmosphere shell.",
    "The symptom is a band of noise or missing intersections near the "
    "silhouette that does not go away with more samples, because it is not "
    "noise — it is a deterministic precision failure.",
    "<b>This is the first instance of a theme that runs through the whole "
    "course:</b> the mathematically clean formulation and the numerically "
    "usable one are frequently different, and the difference matters most in "
    "the cases you most want to render."]),
  ("h2", "1.2 &nbsp; Ray&ndash;triangle"),
  ("p", "The M&ouml;ller&ndash;Trumbore algorithm solves for the "
        "intersection parameter and the barycentric coordinates "
        "simultaneously, by applying Cramer's rule to a 3&times;3 system. It "
        "requires no precomputation and stores no plane equation, which "
        "matters when a scene has a hundred million triangles and memory "
        "bandwidth is the binding constraint."),
  ("code", """vec3 e1 = v1 - v0, e2 = v2 - v0;
vec3 pv = cross(r.d, e2);
float det = dot(e1, pv);
if (fabs(det) < 1e-12f) return false;       // parallel
float inv = 1.0f / det;
vec3  tv = r.o - v0;
float u  = dot(tv, pv) * inv;   if (u < 0 || u > 1)     return false;
vec3  qv = cross(tv, e1);
float v  = dot(r.d, qv) * inv;  if (v < 0 || u+v > 1)   return false;
float t  = dot(e2, qv) * inv;   if (t < tmin || t > tmax) return false;"""),
  ("p", "The barycentric coordinates come out free, and you need them "
        "immediately: interpolating vertex normals, texture coordinates, "
        "tangents, and any other per-vertex attribute is a barycentric "
        "combination. The ordering of the early-outs is deliberate — "
        "testing u before computing <code>qv</code> saves a cross product on "
        "the majority of misses."),

  ("break",),
  ("h1", "2 &nbsp; Watertightness"),
  ("callout", "Two triangles sharing an edge can both miss the same ray",
   ["Consider two triangles that share an edge exactly, as every pair of "
    "adjacent triangles in a closed mesh does, and a ray that passes "
    "precisely through that shared edge.",
    "Each triangle's intersection test is evaluated independently, in "
    "floating point, using <i>different</i> vertex orderings and therefore "
    "different roundings. It is entirely possible for both tests to conclude "
    "that the ray passes just outside the triangle.",
    "<b>The ray passes through a closed solid.</b> In a path tracer, the "
    "escaped ray usually finds the environment light, so the artefact "
    "appears as isolated bright pixels scattered along silhouettes and "
    "creases — and they move as the camera moves, so they cannot be "
    "mistaken for texture.",
    "They are also nearly impossible to debug from the image, because the "
    "triangle that failed is not the one you would inspect."]),
  ("p", "A <b>watertight</b> intersection test guarantees this cannot occur. "
        "The approach of Woop, Benthin, and Wald (2013) is:"),
  ("ol", ["Transform the ray into a space where its direction is (0, 0, 1), "
          "choosing the permutation of axes by the largest-magnitude "
          "component of <b>d</b> so the transform is well conditioned.",
          "Project the three vertices into the plane perpendicular to the "
          "ray and compute three 2D edge functions.",
          "<b>Evaluate each edge function in a canonical order determined by "
          "the vertex positions themselves</b>, not by the triangle's "
          "winding. Two triangles sharing an edge then compute bitwise "
          "identical values for that edge.",
          "If an edge function evaluates to exactly zero, recompute it in "
          "double precision to break the tie consistently."]),
  ("callout", "Determinism, not precision, is what buys watertightness",
   ["Step 3 is the whole idea, and it is worth being clear about why it "
    "works. The test does not become more <i>accurate</i> — the edge "
    "function may still be computed with error.",
    "What changes is that both triangles compute the <i>same</i> value with "
    "the <i>same</i> error. So if one concludes the ray is outside, the "
    "other necessarily concludes it is inside. Exactly one of them "
    "reports a hit, which is precisely the guarantee required.",
    "This is a useful pattern beyond ray tracing: when two computations must "
    "agree, making them bitwise identical is often easier and more reliable "
    "than making them both accurate.",
    "<b>Cost is about 10%</b> over M&ouml;ller&ndash;Trumbore, which is a "
    "bargain for eliminating an entire class of artefact that is otherwise "
    "undiagnosable. PBRT uses it by default."]),

  ("h1", "3 &nbsp; Self-intersection"),
  ("callout", "Why shadow acne happens",
   ["A path hits a surface at parameter t and computes the hit point as "
    "p = o + t&middot;d. That computation rounds, so <b>p is not exactly on "
    "the surface</b> — it is at the nearest representable float, which "
    "may be slightly behind it.",
    "The next ray starts at p. If p is behind the surface, the new ray "
    "immediately intersects the surface it just left, at t very near zero. "
    "For a shadow ray this reports the point as being in its own shadow; for "
    "an indirect ray it produces a spurious short path.",
    "The resulting dark speckle is the classic 'shadow acne'. It is "
    "<b>worse far from the world origin</b>, because the spacing between "
    "representable floats grows with magnitude: at a coordinate of 10,000, "
    "consecutive floats are about a millimetre apart.",
    "This is why a scene imported with real-world coordinates often renders "
    "with acne that the same scene centred at the origin does not."]),
  ("p", "The usual response is a constant: reject hits with t below some "
        "epsilon, typically 10<super>&minus;4</super>. This does not work, "
        "and the reason it does not work is instructive. The required "
        "epsilon scales with the magnitude of the coordinates, so <b>no "
        "single value is correct across a scene</b>. Too small and acne "
        "reappears in the distant parts; too large and contact shadows "
        "detach from the objects casting them, so a chair appears to float."),
  ("callout", "Offset in units-in-the-last-place instead",
   ["The approach of W&auml;chter and Binder (Ray Tracing Gems, chapter 6) "
    "moves the ray origin along the <b>geometric</b> normal by a fixed "
    "number of representable floats — by reinterpreting the float's "
    "bits as an integer, adding a small constant, and reinterpreting back.",
    "Because the spacing of floats scales with magnitude automatically, "
    "<b>a fixed number of ULPs is a correctly scaled offset at every "
    "distance from the origin</b>, with no tuning and no scene dependence.",
    "Near the origin, where ULP steps become vanishingly small, it falls "
    "back to a small absolute offset. The combination is robust over the "
    "whole representable range.",
    "<b>Offset along the geometric normal, never the shading normal</b> "
    "(&sect;5). The shading normal can point to the wrong side of the actual "
    "triangle near a silhouette, and offsetting along it can push the origin "
    "<i>into</i> the surface, which makes the problem worse rather than "
    "better."]),

  ("h1", "4 &nbsp; Ray differentials"),
  ("table", ["", "Rasteriser", "Ray tracer"],
   [["How it filters textures",
     "Fragments are shaded in 2&times;2 quads, so hardware computes "
     "screen-space derivatives of the texture coordinates by differencing "
     "within the quad. Mip level selection is automatic.",
     "Each ray is independent. There is no neighbouring sample, so nothing "
     "indicates how much of the texture the ray covers."],
    ["Consequence",
     "You had correct texture filtering in CSCE 641 without thinking about "
     "it.",
     "<b>Without differentials, you must use the finest mip level</b> and "
     "accept severe aliasing on distant or grazing surfaces."]],
   [0.17, 0.42, 0.41]),
  ("p", "The fix is to carry two auxiliary rays alongside the main one, "
        "offset by one pixel in x and in y. At an intersection, the "
        "difference between where the three rays land gives "
        "&part;p/&part;x and &part;p/&part;y, which convert through the "
        "surface parameterisation into &part;u/&part;x and &part;u/&part;y "
        "— exactly the quantities a mip level requires."),
  ("callout", "Differentials survive specular bounces and die at diffuse ones",
   ["Through a mirror reflection or a refraction, the differentials can be "
    "propagated analytically, with correction terms accounting for the "
    "surface's curvature. A reflection in a convex mirror widens the "
    "footprint; a concave one narrows it. Igehy's 1999 derivation handles "
    "both.",
    "<b>At a diffuse bounce the concept breaks down.</b> The outgoing "
    "direction is sampled at random, so two adjacent camera rays scatter in "
    "completely unrelated directions and the 'footprint' of the bundle has "
    "no meaning.",
    "<b>What production renderers actually do:</b> use differentials for "
    "camera rays and specular chains, where they are correct and valuable, "
    "and after the first diffuse bounce switch to a heuristic — a "
    "fixed blur, a footprint that widens with path length, or path-space "
    "filtering.",
    "This is acceptable because indirect illumination is low frequency: an "
    "over-blurred texture lookup on a third bounce is invisible, while the "
    "same error on a camera ray would not be."]),

  ("h1", "5 &nbsp; The intersection interface"),
  ("table", ["Field", "Used for", "Notes"],
   [["<code>t</code>", "Ordering hits; updating the ray interval.",
     "The only field a shadow ray needs."],
    ["<code>p</code>", "Origin of the next ray.",
     "<b>Must be offset</b> per &sect;3 before reuse."],
    ["<code>ng</code>", "Which side of the surface you are on; the offset "
     "direction.", "<b>From the triangle itself</b>, by cross product of "
     "the edges."],
    ["<code>ns</code>", "Shading.",
     "Barycentric interpolation of vertex normals, possibly perturbed by a "
     "normal map."],
    ["<code>u, v</code>", "Texture lookup; derivative computation.",
     "Barycentrics, free from M&ouml;ller&ndash;Trumbore."],
    ["<code>dpdu, dpdv</code>", "Tangent frame.",
     "Needed for anisotropic BSDFs (Module 07) and normal mapping."],
    ["<code>prim</code>", "Material and light lookup.",
     "An index or pointer. Keep the hit record small — it is copied "
     "constantly."]],
   [0.16, 0.38, 0.46]),
  ("callout", "Geometric and shading normals must both be stored",
   ["<b>ng</b> is the true normal of the geometry you hit. It determines "
    "which side of the surface the ray is on, and it is the correct "
    "direction to offset along.",
    "<b>ns</b> is interpolated, and possibly perturbed by a normal map. It "
    "is what the BSDF is evaluated against, and the disagreement between it "
    "and ng is exactly what makes a coarse mesh look smooth.",
    "<b>Use ns to offset</b> and rays can be displaced to the wrong side of "
    "the actual triangle near silhouettes, producing light leaks and acne "
    "that no epsilon fixes.",
    "<b>Use ng to shade</b> and every smooth mesh is faceted — you "
    "have thrown away the vertex normals.",
    "Both mistakes are common in first renderers, and both disappear "
    "permanently if the hit record simply carries both. There is also a "
    "subtler issue: a sampled direction can be above the shading hemisphere "
    "and below the geometric one, which must be rejected explicitly or it "
    "produces energy from nowhere."]),
  ("h2", "5.1 &nbsp; Shadow rays are a different operation"),
  ("p", "A shadow ray asks a yes/no question: is anything between these two "
        "points? It does not need the nearest hit, only <i>any</i> hit, so "
        "it can return the instant one is found rather than continuing to "
        "search for a closer one."),
  ("ul", ["Implement a separate <code>occluded()</code> entry point. It is "
          "typically <b>2&ndash;3&times; faster</b> than a full intersection "
          "query, and after Module 08 introduces next-event estimation, "
          "shadow rays will be the majority of all rays cast.",
          "Set t<sub>max</sub> just short of the light sample so the light's "
          "own geometry does not register as an occluder — a classic "
          "cause of 'my area light is black'.",
          "Offset at <i>both</i> ends: the surface and the light. The light "
          "end has the same self-intersection problem."]),
 ],
 "resources": [
   ("PBRT 4th ed. &mdash; Chapter 6, Shapes",
    "https://pbr-book.org/4ed/Shapes",
    "Intersection for every primitive type, and &sect;6.8 on managing "
    "rounding error — the most careful free treatment of &sect;1 and "
    "&sect;3 anywhere."),
   ("Woop, Benthin & Wald &mdash; Watertight Ray/Triangle Intersection (free)",
    "https://jcgt.org/published/0002/01/05/",
    "The source for &sect;2. Short paper, complete algorithm, and the "
    "failure analysis is worth reading on its own."),
   ("Ray Tracing Gems &mdash; Chapter 6, A Fast and Robust Method for "
    "Avoiding Self-Intersection (free)",
    "https://www.realtimerendering.com/raytracinggems/",
    "The ULP-offset method of &sect;3, with the full code. The whole book is "
    "free."),
   ("Igehy &mdash; Tracing Ray Differentials (1999, free)",
    "https://graphics.stanford.edu/papers/trd/",
    "The original derivation of &sect;4, including propagation through "
    "reflection and refraction."),
   ("Ray Tracing in One Weekend",
    "https://raytracing.github.io/books/RayTracingInOneWeekend.html",
    "Work through this now if you have not. It gets an image on screen in a "
    "few hours and makes the rest of the course concrete."),
 ],
 "exercises": [
   "Implement ray&ndash;sphere intersection with the naive quadratic "
   "formula and with the stable form. Construct a case where they differ "
   "visibly and report the ratio of the errors.",
   "Implement M&ouml;ller&ndash;Trumbore and validate the barycentrics by "
   "interpolating a known linear function across the triangle and comparing "
   "against its analytic value.",
   "Build a closed cube from twelve triangles and fire ten million random "
   "rays at it from outside. Count how many escape. With a naive test the "
   "count should be small but non-zero; implement the watertight test and "
   "confirm it reaches exactly zero.",
   "Reproduce the self-intersection problem: place a plane at the origin and "
   "render it, then translate the whole scene by 10,000 units and render "
   "again with the same epsilon. Report the difference.",
   "Implement the ULP offset and repeat the previous exercise. Confirm the "
   "artefact is gone at both scales without changing any constant.",
   "Implement ray differentials for camera rays and use them to select mip "
   "levels. Render a textured ground plane extending to the horizon, with "
   "and without, and compare.",
   "Measure the speedup of a dedicated <code>occluded()</code> path against "
   "calling the full intersection routine, on a scene with significant "
   "occlusion. Report the ratio.",
   "Construct a case where the sampled direction is above the shading "
   "hemisphere but below the geometric one. Show what happens if it is not "
   "rejected.",
 ],
 "selfcheck": [
   "Why should the ray carry its own parameter interval?",
   "What is catastrophic cancellation, and where does it occur in "
   "ray&ndash;sphere intersection?",
   "What does M&ouml;ller&ndash;Trumbore return beyond t, and why do you "
   "need it?",
   "What does watertightness guarantee, and what mechanism provides it?",
   "Why is a fixed epsilon the wrong solution to self-intersection?",
   "How does a ULP-based offset adapt to scene scale automatically?",
   "What are ray differentials for, and at what point in a path do they stop "
   "being meaningful?",
   "Give the two distinct bugs that follow from conflating geometric and "
   "shading normals.",
   "Why is a shadow ray faster than a general intersection query?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Acceleration Structures",
 "subtitle": "Turning O(n) per ray into O(log n), and the heuristic that "
             "does it.",
 "question": "How do you avoid testing every triangle for every ray?",
 "outcomes": [
     "Explain the trade-off between spatial and object subdivision.",
     "Build a BVH with the surface area heuristic and justify every term.",
     "Implement efficient traversal with correct ordering and early exit.",
     "Explain why the SAH works, and what assumptions it makes.",
     "Measure and interpret traversal statistics.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "Linear search, a billion times."},

  {"t": "callout", "title": "The arithmetic that forces the issue",
   "kind": "Why this module exists",
   "body": ["A 1920×1080 image at 256 samples per pixel with 8 bounces is "
            "roughly <b>4 × 10&#185;&#8304; rays</b>.",
            "A modest scene has 10&#8310; triangles. Testing all of them per "
            "ray is 4 × 10&#185;&#8310; intersection tests.",
            "<b>At a billion tests per second that is 130,000 years.</b>",
            "With a BVH, each ray touches perhaps 100 nodes and 20 "
            "triangles. The same image is hours. <b>The acceleration "
            "structure is not an optimisation; it is what makes ray tracing "
            "possible.</b>"]},

  {"t": "two", "kicker": "Two families", "title": "Subdivide space, or subdivide objects",
   "lh": "Spatial — kd-tree, grid, octree",
   "l": ["Partition <b>space</b> into disjoint regions.",
         "A primitive may land in several regions.",
         "<b>Regions never overlap</b>, so traversal can stop at the first "
         "hit found in order.",
         ("Historically the fastest for static scenes.", 1),
         "Build is slow; refitting for animation is not possible."],
   "rh": "Object — BVH",
   "r": ["Partition the <b>primitives</b> into groups, bound each.",
         "Each primitive is in exactly one leaf.",
         "<b>Bounds may overlap</b>, so both children may need visiting.",
         ("Now the standard almost everywhere.", 1),
         "Fast to build, refittable, bounded memory."],
   "note": "The overlap/duplication trade is the heart of it. BVH won on "
           "build speed, predictable memory, and animation support."},

  {"t": "callout", "title": "Why BVH won",
   "kind": "The practical argument",
   "body": ["<b>Bounded memory:</b> n primitives give at most 2n−1 nodes. A "
            "kd-tree's size depends on how badly primitives straddle splits "
            "and cannot be predicted from n.",
            "<b>Fast to build:</b> seconds rather than minutes, which "
            "matters when you rebuild every frame of an animation.",
            "<b>Refittable:</b> for deforming geometry you can update the "
            "bounds without rebuilding the topology.",
            "<b>Hardware:</b> every ray tracing GPU implements BVH traversal "
            "in fixed-function silicon. That settled the question "
            "permanently."]},

  {"t": "section", "label": "Part 2", "title": "The surface area heuristic",
   "blurb": "The one idea in this module that generalises."},

  {"t": "eq", "kicker": "Geometric probability", "title": "The key fact",
   "eqs": [
     ("P(ray hits B | ray hits A)  =  SA(B) / SA(A)",
      "For a convex B inside a convex A, and uniformly distributed rays. "
      "A result from integral geometry."),
     ("cost(split) = Ct + (SA(L)/SA(P))·N(L)·Ci + (SA(R)/SA(P))·N(R)·Ci",
      "Expected cost of a node: traverse, plus each child's cost weighted by "
      "the probability of entering it."),
   ],
   "caption": "Surface area — not volume, not primitive count — is "
              "the right measure of how likely a box is to be hit.",
   "note": "The surface-area-not-volume point surprises people. It falls out "
           "of the geometry: a ray enters through the surface."},

  {"t": "callout", "title": "Minimise expected cost, not imbalance",
   "kind": "What the SAH actually says",
   "body": ["A median split balances the <i>tree</i>. The SAH balances the "
            "<i>expected work</i>, which is a different and better "
            "objective.",
            "<b>It will happily produce a lopsided tree</b> — 90% of "
            "primitives on one side — if that puts a tightly bounded "
            "cluster behind a small box that rays rarely enter.",
            "That is exactly right: a node rays never visit costs nothing, "
            "however many primitives it holds.",
            "<b>SAH typically beats median splitting by 2–3× in traversal "
            "cost.</b> It is the difference between a usable renderer and a "
            "slow one."]},

  {"t": "code", "kicker": "Build 1/2", "title": "Binned SAH — the accumulation pass",
   "lang": "cpp", "code": """
// Exact SAH needs a sort per axis. Binning gets ~99% of the quality
// for a fraction of the cost. 12-16 bins is standard everywhere.
Node* build(span<Prim> prims) {
    AABB bounds = union_of(prims);
    if (prims.size() <= 2) return make_leaf(prims, bounds);

    // Bin over the CENTROID bounds, not the full bounds: centroids are
    // what the split actually partitions.
    AABB centroids = union_of_centroids(prims);
    int  axis      = centroids.largest_extent();

    Bin bins[NBINS] = {};
    for (auto& p : prims) {                  // single pass, O(n)
        int b = bin_index(p.centroid, centroids, axis);
        bins[b].count++;
        bins[b].bounds.expand(p.bounds);
    }
    ...
""",
   "caption": "One linear pass over the primitives. Binning on centroid "
              "bounds rather than full bounds is what keeps the split "
              "candidates meaningful.",
   "note": "The centroid-bounds detail matters: binning over full bounds "
           "clusters everything into a few bins for large primitives."},

  {"t": "code", "kicker": "Build 2/2", "title": "Binned SAH — choosing the split",
   "lang": "cpp", "code": """
    // Prefix and suffix sweeps give EVERY candidate's cost in O(NBINS),
    // because each sweep accumulates bounds and counts incrementally.
    float best = FLT_MAX;  int split = -1;
    for (int i = 1; i < NBINS; i++) {
        auto [bl, nl] = prefix[i-1];         // everything left of plane i
        auto [br, nr] = suffix[i];           // everything right of it
        float c = C_TRAV
                + (bl.area()*nl + br.area()*nr) / bounds.area() * C_ISECT;
        if (c < best) { best = c; split = i; }
    }

    // THE TERMINATION TEST. Is the best split cheaper than not splitting?
    if (best >= prims.size() * C_ISECT)
        return make_leaf(prims, bounds);

    auto mid = partition(prims, [&](auto& p){ return bin_index(p) < split; });
    return make_inner(build(prims.first(mid)), build(prims.subspan(mid)));
}
""",
   "caption": "The termination test is three lines and is what stops the "
              "tree degenerating into one primitive per leaf.",
   "note": "The termination test is the part people omit, and then wonder "
           "why their tree has 200k nodes for 10k triangles."},

  {"t": "section", "label": "Part 3", "title": "Traversal",
   "blurb": "Where the time actually goes."},

  {"t": "code", "kicker": "Traversal", "title": "Ordered traversal with early exit",
   "lang": "cpp", "code": """
bool traverse(const BVH& bvh, Ray& r, Hit& h) {
    const Node* stack[64];  int sp = 0;
    const Node* node = &bvh.root;
    vec3 invd = 1.0f / r.d;                 // precompute once, not per node

    while (true) {
        if (node->is_leaf()) {
            for (auto& p : node->prims)
                if (intersect(r, p, h)) r.tmax = h.t;   // <-- shrink interval
        } else {
            float t0, t1;
            bool h0 = node->left ->bounds.hit(r, invd, t0);
            bool h1 = node->right->bounds.hit(r, invd, t1);
            if (h0 && h1) {
                // Visit the NEARER child first: its hit may cull the other.
                const Node* near = t0 < t1 ? node->left : node->right;
                const Node* far  = t0 < t1 ? node->right : node->left;
                stack[sp++] = far;  node = near;  continue;
            }
            if (h0) { node = node->left;  continue; }
            if (h1) { node = node->right; continue; }
        }
        if (sp == 0) return h.valid();
        node = stack[--sp];
        if (node->tenter > r.tmax) continue;  // <-- culled by a closer hit
    }
}
""",
   "caption": "Two lines do the work: shrinking tmax on every hit, and "
              "visiting the nearer child first so that shrinking happens as "
              "early as possible.",
   "note": "Without near-first ordering the structure still works and is "
           "roughly 2× slower. It is the cheapest optimisation here."},

  {"t": "table", "kicker": "Diagnosis", "title": "Statistics worth instrumenting",
   "header": ["Statistic", "Healthy", "If it is wrong"],
   "widths": [3.3, 3.2, 5.6],
   "rows": [
     ["Nodes visited / ray", "50–200", "<b>High: bad splits or overlap</b>"],
     ["Prims tested / ray", "10–50", "High: leaves too large"],
     ["Leaf size", "1–4", "Check the SAH termination test"],
     ["Tree depth", "~2 log&#8322;n", "Deep: degenerate splits"],
     ["Build time", "Seconds", "<b>Minutes: you are not binning</b>"],
   ],
   "footnote": "Instrument these in Module 04 and keep them. They are how "
               "you will diagnose every later performance problem.",
   "note": "Insist on the instrumentation. 'It feels slow' is not "
           "actionable; 'we test 400 prims per ray' is."},

  {"t": "section", "label": "Part 4", "title": "Beyond the basics",
   "blurb": "What production renderers add."},

  {"t": "bullets", "kicker": "Refinements", "title": "The improvements that matter",
   "items": [
     "<b>Spatial splits (SBVH).</b> Allow splitting a primitive across two "
     "nodes. Recovers much of the kd-tree advantage. ~30% faster on scenes "
     "with long thin triangles.",
     "",
     "<b>Wide BVHs (4- or 8-way).</b> Test four boxes at once with SIMD. "
     "Shallower tree, fewer stack operations.",
     "",
     "<b>Compressed nodes.</b> Quantise bounds to 8-bit offsets from the "
     "parent. Memory is the binding constraint at scale.",
     "",
     "<b>Two-level BVHs.</b> A BVH over instances, each holding a BVH. "
     "Essential for instanced geometry; standard in GPU APIs.",
     "",
     "<b>Ray reordering.</b> Sort incoherent rays by direction and origin to "
     "recover cache locality.",
   ],
   "note": "Two-level is the one students will meet first in practice — "
           "it is exactly what DXR/Vulkan expose as BLAS and TLAS."},

  {"t": "callout", "title": "Coherence is the real variable",
   "kind": "Why a path tracer is slower than it looks",
   "body": ["Primary rays are <b>coherent</b>: neighbouring rays follow "
            "almost identical paths through the tree, so the nodes they need "
            "are in cache.",
            "After one diffuse bounce, directions are random. Adjacent "
            "pixels' rays go to completely different parts of the tree.",
            "<b>The same BVH is several times slower for incoherent rays</b>, "
            "and the cause is memory, not arithmetic.",
            "This is why bounce 2 can cost more than bounce 1 despite fewer "
            "active paths, and why wavefront path tracers sort rays before "
            "tracing them."]},

  {"t": "callout", "title": "Do not write your own for production",
   "kind": "An honest note",
   "body": ["<b>You will write one in this course</b>, because understanding "
            "traversal cost is necessary to reason about everything that "
            "follows.",
            "For production, <b>Embree</b> (CPU) and the hardware BVH on any "
            "modern GPU are faster than anything you will write, by a "
            "factor of several.",
            "They have years of SIMD tuning, cache-aware layouts, and "
            "fixed-function silicon behind them.",
            "<b>Knowing what they are doing is still the point.</b> It is "
            "how you tell a traversal problem from a sampling problem when "
            "something is slow."]},
 ],
 "takeaways": [
   "Brute force is 10&#8309;&times; too slow. The acceleration structure is "
   "not an optimisation — it is what makes ray tracing feasible.",
   "Spatial subdivision gives disjoint regions and duplicated primitives; "
   "object subdivision gives overlapping bounds and unique primitives.",
   "BVH won on bounded memory, fast builds, refittability for animation, and "
   "hardware support.",
   "The SAH rests on P(hit B | hit A) = SA(B)/SA(A). Surface area, not "
   "volume, measures how likely a box is to be entered.",
   "The SAH minimises expected cost, not tree balance, and will produce "
   "lopsided trees on purpose. Worth 2–3&times; over median splitting.",
   "Traversal speed comes from shrinking tmax on every hit and visiting the "
   "nearer child first. Coherence, not arithmetic, dominates in practice.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The arithmetic that forces the issue"),
  ("p", "Consider a 1920&times;1080 image at 256 samples per pixel with a "
        "maximum path depth of 8. That is roughly 4 &times; "
        "10<super>10</super> rays, and next-event estimation (Module 08) "
        "will roughly double it."),
  ("p", "A modest production scene has 10<super>6</super> triangles. Testing "
        "every triangle against every ray is 4 &times; 10<super>16</super> "
        "intersection tests. At an optimistic 10<super>9</super> tests per "
        "second, that is about <b>1.3 million seconds per core</b> — "
        "call it 130,000 years on one core, or a few centuries on a large "
        "machine."),
  ("p", "With a well-built BVH, a ray visits on the order of 100 nodes and "
        "tests perhaps 20 triangles. The same image becomes hours. <b>This "
        "is not an optimisation; ray tracing does not exist without it.</b>"),

  ("h1", "2 &nbsp; Two families"),
  ("table", ["", "Spatial subdivision", "Object subdivision"],
   [["Examples", "kd-tree, uniform grid, octree, BSP.",
     "Bounding volume hierarchy (BVH)."],
    ["Partitions", "<b>Space</b>, into disjoint regions.",
     "<b>Primitives</b>, into disjoint groups, each with a bounding box."],
    ["Primitive placement",
     "A primitive straddling a boundary appears in <b>several</b> regions.",
     "Each primitive is in <b>exactly one</b> leaf."],
    ["Region overlap", "<b>None.</b> Regions are disjoint by construction.",
     "<b>Bounds may overlap</b>, so a ray may have to descend into both "
     "children."],
    ["Traversal consequence",
     "Can process regions in strict front-to-back order and stop at the "
     "first hit found.",
     "Must consider both children when their bounds overlap, though "
     "near-first ordering recovers most of the benefit."],
    ["Memory", "<b>Unbounded in n</b> — depends on how badly "
     "primitives straddle splits.",
     "<b>At most 2n &minus; 1 nodes.</b> Predictable."],
    ["Build time", "Minutes for large scenes.", "Seconds."],
    ["Animation", "Rebuild from scratch.",
     "<b>Refit bounds</b> without changing topology."]],
   [0.17, 0.41, 0.42]),
  ("callout", "Why the BVH won",
   ["For about fifteen years the kd-tree was understood to be faster for "
    "static scenes, and for static scenes it often still is.",
    "<b>It lost on everything else.</b> Memory consumption cannot be "
    "predicted from primitive count, which is intolerable when a scene must "
    "fit in a fixed budget. Build times of minutes are unacceptable when "
    "geometry deforms every frame. And there is no way to refit a kd-tree "
    "for animation — the splitting planes are tied to the geometry's "
    "positions.",
    "The BVH's bounded 2n &minus; 1 node count, second-scale builds, and "
    "refittability matched what production actually needed.",
    "<b>Then hardware settled it.</b> Every GPU with ray tracing support "
    "implements BVH traversal in fixed-function silicon. The question is no "
    "longer open."]),

  ("break",),
  ("h1", "3 &nbsp; The surface area heuristic"),
  ("p", "Given a set of primitives, which split is best? The surface area "
        "heuristic answers this by estimating the expected cost of each "
        "candidate, and it rests on one result from integral geometry."),
  ("eq", "P( ray hits B | ray hits A ) = SA(B) / SA(A)"),
  ("p", "For convex B contained in convex A, and rays drawn from a uniform "
        "distribution over directions and origins, the conditional "
        "probability of hitting the inner box given that you hit the outer "
        "one is the ratio of their <b>surface areas</b>."),
  ("callout", "Surface area, not volume",
   ["The intuition most people reach for is volume, and it is wrong. A ray "
    "is a line, not a point: it enters a box through its <i>surface</i>, and "
    "the measure of lines intersecting a convex body is proportional to that "
    "body's surface area.",
    "Consider a very flat box — a slab. Its volume is nearly zero, but "
    "it has substantial surface area and a great many rays pass through it. "
    "Any volume-based heuristic would consider it free, and it is not.",
    "<b>This is why the SAH is the surface <i>area</i> heuristic</b>, and "
    "getting that right is most of why it works as well as it does."]),
  ("eq", "cost = C<sub>trav</sub> + ( SA(L)&middot;N(L) + "
         "SA(R)&middot;N(R) ) &middot; C<sub>isect</sub> / SA(P)"),
  ("table", ["Term", "Meaning"],
   [["C<sub>trav</sub>", "Cost of visiting an interior node and testing two "
     "child boxes. Measured, not guessed — instrument your renderer."],
    ["C<sub>isect</sub>", "Cost of one primitive intersection test."],
    ["SA(L)/SA(P)", "Probability a ray entering the parent also enters the "
     "left child."],
    ["N(L)", "Number of primitives in the left child."]],
   [0.17, 0.83]),
  ("callout", "The SAH minimises expected cost, not tree balance",
   ["A median split divides primitives evenly and produces a balanced tree. "
    "That optimises the wrong thing.",
    "The SAH optimises <b>expected traversal work</b>, and the two "
    "objectives frequently disagree. The SAH will happily put 90% of the "
    "primitives on one side if doing so puts a tightly clustered group "
    "behind a <i>small</i> bounding box that few rays enter.",
    "<b>And that is correct.</b> A node that rays rarely visit contributes "
    "almost nothing to the expected cost, no matter how many primitives it "
    "contains. Balance is irrelevant; expected work is what you pay.",
    "<b>In practice the SAH beats median splitting by a factor of two to "
    "three in traversal cost.</b> That is the difference between a renderer "
    "you can iterate with and one you cannot."]),
  ("h2", "3.1 &nbsp; Binning"),
  ("p", "Evaluating every possible split exactly requires sorting the "
        "primitives along each axis, giving an O(n log&#178; n) build. "
        "<b>Binned SAH</b> instead divides the centroid bounds into a fixed "
        "number of bins — 12 to 16 is standard — accumulates each "
        "primitive into one bin in a single pass, and then evaluates only "
        "the bin boundaries as candidate splits, using prefix and suffix "
        "sweeps to make each candidate's cost O(1)."),
  ("p", "This gives roughly 99% of the quality of the exact SAH at a small "
        "fraction of the build cost, and it is what essentially every "
        "production builder does."),
  ("callout", "The termination test is not optional",
   ["<pre>if (best_cost &gt;= N * C_isect) return make_leaf(prims);</pre>",
    "This line compares the cost of the best available split against the "
    "cost of simply testing all the primitives in a leaf. If splitting does "
    "not pay, stop.",
    "<b>Omitting it is the most common BVH bug.</b> The builder keeps "
    "splitting until it reaches one primitive per leaf, producing a tree "
    "with far more nodes than necessary, higher memory traffic, and worse "
    "performance than a correctly terminated tree with leaves of two to four "
    "primitives.",
    "The symptom is a node count several times larger than expected and "
    "traversal statistics showing many nodes visited but few primitives "
    "tested."]),

  ("h1", "4 &nbsp; Traversal"),
  ("p", "Build quality sets the ceiling; traversal determines whether you "
        "reach it. Two details account for most of the difference between a "
        "fast traversal loop and a slow one."),
  ("ol", ["<b>Shrink t<sub>max</sub> on every hit.</b> Once a primitive has "
          "been hit at distance t, nothing beyond t can matter. Writing that "
          "into the ray immediately culls every subsequent node whose entry "
          "distance exceeds it.",
          "<b>Visit the nearer child first.</b> Compare the two children's "
          "box entry distances and descend into the closer one, pushing the "
          "farther onto the stack. A hit found in the near subtree often "
          "culls the far one entirely. <b>This is worth roughly 2&times;</b> "
          "and costs one comparison."]),
  ("p", "Beyond those: precompute the reciprocal of the ray direction once "
        "rather than dividing in every slab test; keep the stack small and "
        "on the actual stack; and check the stored entry distance when "
        "popping a node, since a closer hit may have been found since it was "
        "pushed."),
  ("table", ["Statistic", "Healthy range", "What a bad value indicates"],
   [["Nodes visited per ray", "50&ndash;200",
     "<b>High:</b> poor splits, or heavy bound overlap. Check the SAH "
     "implementation."],
    ["Primitives tested per ray", "10&ndash;50",
     "<b>High:</b> leaves are too large, or the termination test is too "
     "eager."],
    ["Average leaf size", "1&ndash;4 primitives",
     "<b>Large:</b> termination too aggressive. <b>All ones:</b> termination "
     "test missing."],
    ["Tree depth", "about 2 log&#8322;n",
     "<b>Much deeper:</b> degenerate splits — often all primitives "
     "sharing a centroid."],
    ["Build time", "Seconds for 10<super>6</super> primitives",
     "<b>Minutes:</b> you are not binning."]],
   [0.26, 0.24, 0.50]),
  ("p", "<b>Instrument these now and keep them.</b> Every performance "
        "question for the rest of the course is answered by looking at them "
        "first — a renderer that is slow because of traversal and one "
        "that is slow because of variance need completely different "
        "responses, and these numbers distinguish the two immediately."),

  ("h1", "5 &nbsp; Refinements"),
  ("table", ["Technique", "Idea", "Gain"],
   [["<b>Spatial splits (SBVH)</b>",
     "Allow a primitive to be split across two nodes, as a kd-tree does, "
     "when the SAH says it pays. Recovers most of the kd-tree's advantage "
     "while keeping the BVH's other properties.",
     "Up to ~30% on scenes with long thin triangles or widely varying "
     "primitive sizes. Memory is no longer strictly bounded."],
    ["<b>Wide BVHs</b>",
     "Four or eight children per node, with all child boxes tested "
     "simultaneously using SIMD.",
     "Shallower trees, fewer stack operations, better use of vector units. "
     "Standard in Embree."],
    ["<b>Compressed nodes</b>",
     "Quantise child bounds to 8-bit offsets relative to the parent's box.",
     "Several times less memory. At scale, memory bandwidth is the binding "
     "constraint, so this is often a speed win too."],
    ["<b>Two-level BVHs</b>",
     "A top-level BVH over instance transforms, each instance referencing a "
     "shared bottom-level BVH over its geometry.",
     "Essential for instancing — a forest of 10,000 identical trees "
     "stores one tree's BVH. <b>This is exactly the BLAS/TLAS structure the "
     "GPU ray tracing APIs expose.</b>"],
    ["<b>Ray reordering</b>",
     "Buffer up incoherent rays, sort them by origin and direction, then "
     "trace them in sorted order.",
     "Recovers cache locality for incoherent rays — see below."]],
   [0.18, 0.44, 0.38]),
  ("callout", "Coherence, not arithmetic, is the real variable",
   ["Primary rays from a pinhole camera are highly <b>coherent</b>: "
    "neighbouring pixels generate nearly parallel rays that descend through "
    "almost the same sequence of nodes. Those nodes are already in cache, so "
    "traversal is effectively free in memory terms.",
    "After a single diffuse bounce the directions are sampled at random. Two "
    "rays from adjacent pixels now travel to completely unrelated parts of "
    "the tree and touch disjoint memory.",
    "<b>The same BVH can be several times slower for incoherent rays than "
    "for coherent ones</b>, and the cause is cache behaviour, not "
    "instruction count. This is why bounce 2 sometimes costs more than "
    "bounce 1 despite having fewer active paths.",
    "It is also the reason GPU renderers use a <b>wavefront</b> "
    "architecture: rather than following each path to completion, they "
    "process all paths one bounce at a time, sorting rays between bounces to "
    "restore coherence. The sorting costs real time and still pays."]),
  ("callout", "Write one, then use someone else's",
   ["<b>You will implement a BVH in this course</b>, and you should. "
    "Understanding where traversal time goes is necessary for reasoning "
    "about everything downstream — when a render is slow, the first "
    "question is always whether it is traversal or variance, and you cannot "
    "answer it from outside.",
    "<b>For production, use Embree on the CPU or the hardware BVH on the "
    "GPU.</b> They will be several times faster than yours, and the gap "
    "comes from years of SIMD tuning, cache-conscious memory layouts, and in "
    "the GPU's case dedicated silicon that you cannot compete with in "
    "software.",
    "<b>This is not a reason to skip the implementation.</b> It is the "
    "difference between using a tool and being able to diagnose it."]),
 ],
 "resources": [
   ("PBRT 4th ed. &mdash; Chapter 7, Primitives and Intersection Acceleration",
    "https://pbr-book.org/4ed/Primitives_and_Intersection_Acceleration",
    "BVH construction including binned SAH, with complete code. The primary "
    "reading for this module."),
   ("Wald, Boulos & Shirley &mdash; Ray Tracing Deformable Scenes with "
    "Dynamic BVHs (free)",
    "https://www.sci.utah.edu/~wald/Publications/",
    "Where much of the modern BVH consensus comes from, including "
    "refitting and the case against kd-trees."),
   ("Stich, Friedrich & Dietrich &mdash; Spatial Splits in BVHs (SBVH, free)",
    "https://www.nvidia.com/docs/IO/77714/sbvh.pdf",
    "The spatial-split hybrid of &sect;5. Short and clearly argued."),
   ("Embree documentation and source",
    "https://www.embree.org/",
    "A production BVH you can read. Compare your traversal loop against "
    "theirs after you have written one."),
   ("Ray Tracing Gems &mdash; chapters on BVH traversal and compression "
    "(free)",
    "https://www.realtimerendering.com/raytracinggems/",
    "Practical implementation detail, especially for the GPU case."),
 ],
 "exercises": [
   "Implement a BVH with median splitting and one with binned SAH. Report "
   "nodes visited and primitives tested per ray for both on the same scene. "
   "The SAH should win by 2&ndash;3&times;.",
   "Measure C<sub>trav</sub> and C<sub>isect</sub> for your own renderer "
   "rather than using the textbook values, then rebuild with the measured "
   "constants and report the difference.",
   "Remove the SAH termination test and report the resulting node count, "
   "memory use, and render time. Then put it back.",
   "Implement near-first ordered traversal and measure the speedup against "
   "arbitrary ordering.",
   "Instrument the five statistics of &sect;4 and produce a heat-map image "
   "of nodes visited per pixel. The structure of the BVH will be visible in "
   "it, which is both useful and worth looking at.",
   "Measure the cost of primary rays against the cost of rays after one, "
   "two, and three diffuse bounces, with all other factors held constant. "
   "Explain the trend using &sect;5.",
   "Build a scene of 10,000 instances of the same mesh. Compare memory use "
   "and build time for a flat BVH against a two-level one.",
   "Benchmark your BVH against Embree on the same scene. Report the ratio "
   "honestly and identify where the difference comes from.",
 ],
 "selfcheck": [
   "Why is brute-force intersection infeasible? Give the order of magnitude.",
   "Give three differences between spatial and object subdivision.",
   "Give four reasons the BVH became standard despite the kd-tree often "
   "being faster for static scenes.",
   "State the geometric probability result the SAH rests on, and say why it "
   "involves surface area rather than volume.",
   "What does the SAH minimise, and why will it deliberately build an "
   "unbalanced tree?",
   "What does the SAH termination test do, and what happens without it?",
   "Name the two traversal details that account for most of the performance, "
   "and say why each works.",
   "What is ray coherence, why does it collapse after a diffuse bounce, and "
   "what do wavefront renderers do about it?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Monte Carlo Integration",
 "subtitle": "Estimating an integral with random numbers, and knowing how "
             "wrong you are.",
 "question": "How do you integrate something you cannot evaluate everywhere?",
 "outcomes": [
     "State the Monte Carlo estimator and prove it is unbiased.",
     "Derive the 1/&radic;N convergence rate and explain its consequences.",
     "Distinguish bias from variance, and consistency from unbiasedness.",
     "Explain why Monte Carlo beats quadrature in high dimensions.",
     "Build the validation suite you will use for the rest of the course.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The estimator",
   "blurb": "Three lines, and the whole of rendering follows."},

  {"t": "eq", "kicker": "The estimator", "title": "Monte Carlo integration",
   "eqs": [
     ("F  =  ∫ f(x) dx        want this",
      "An integral we cannot evaluate in closed form."),
     ("Fₙ  =  (1/N) Σ f(Xᵢ)/p(Xᵢ),   Xᵢ ~ p",
      "Draw N samples from any density p that is non-zero wherever f is, "
      "and average f/p."),
     ("E[Fₙ]  =  F     for every N",
      "Unbiased. Not approximately, not asymptotically — the expected "
      "value is exactly right, even for N = 1."),
   ],
   "caption": "The dividing by p is the whole trick: it corrects for having "
              "sampled some regions more often than others.",
   "note": "Students find it suspicious that N=1 is unbiased. It is — a "
           "single sample is an unbiased estimate with enormous variance."},

  {"t": "code", "kicker": "Proof", "title": "Unbiasedness, in three lines",
   "lang": "text", "code": """
E[Fₙ]  =  E[ (1/N) Σᵢ f(Xᵢ)/p(Xᵢ) ]

       =  (1/N) Σᵢ E[ f(Xᵢ)/p(Xᵢ) ]        linearity of expectation

       =  E[ f(X)/p(X) ]                   the terms are identically
                                           distributed

       =  ∫ (f(x)/p(x)) p(x) dx            definition of expectation

       =  ∫ f(x) dx   =  F                 the p cancels.  ∎

Requires only: p(x) > 0 wherever f(x) ≠ 0.
""",
   "caption": "The last cancellation is the entire argument. Everything "
              "else is bookkeeping.",
   "note": "Walk through this slowly. It is the only proof in the course "
           "students must be able to reproduce."},

  {"t": "callout", "title": "p can be almost anything, and that is the opportunity",
   "kind": "The consequence",
   "body": ["The proof requires only that p is positive wherever f is "
            "non-zero. <b>Any such density gives an unbiased estimator.</b>",
            "So the choice of p does not affect <i>correctness</i> at all. "
            "It affects only <b>variance</b> — how many samples you need "
            "before the answer is usable.",
            "A good p can reduce variance by orders of magnitude. A bad one "
            "produces an image that is correct in expectation and pure noise "
            "in practice.",
            "<b>Module 06 is entirely about choosing p.</b> This slide is "
            "why that module exists."]},

  {"t": "section", "label": "Part 2", "title": "Variance",
   "blurb": "How wrong you are, and how fast that improves."},

  {"t": "eq", "kicker": "Convergence", "title": "The 1/√N law",
   "eqs": [
     ("V[Fₙ]  =  V[f(X)/p(X)] / N",
      "Variance of the mean of N independent samples falls as 1/N."),
     ("σ[Fₙ]  ∝  1/√N",
      "So the standard deviation — the visible noise — falls as the "
      "square root. Independent of dimension."),
     ("4× the samples  ⟹  2× less noise",
      "The fact that governs every render time estimate you will ever make."),
   ],
   "caption": "To halve the noise, quadruple the samples. To get one more "
              "decimal digit, multiply by 100.",
   "note": "Make them feel this: 10,000× the compute for two extra digits. "
           "It is why variance reduction is the whole field."},

  {"t": "callout", "title": "Square-root convergence is brutal and is also the good news",
   "kind": "Both halves matter",
   "body": ["<b>The bad half:</b> halving noise costs 4× the time. Going "
            "from visibly noisy to clean is often 100×.",
            "<b>The good half:</b> 1/√N <i>regardless of dimension</i>. "
            "A trapezoid rule in d dimensions converges as "
            "N<sup>−2/d</sup> — at d = 20 that is "
            "N<sup>−0.1</sup>, which is hopeless.",
            "<b>A path of k bounces is an integral in about 2k "
            "dimensions</b>, and the series sums over all k.",
            "So Monte Carlo is not merely convenient here. <b>It is the only "
            "method whose convergence does not collapse</b>, which is why "
            "the field looks the way it does."]},

  {"t": "table", "kicker": "Vocabulary", "title": "Four words used precisely",
   "header": ["Term", "Means", "In rendering"],
   "widths": [2.5, 4.8, 4.8],
   "rows": [
     ["<b>Unbiased</b>", "E[estimate] = truth, for every N", "Path tracing"],
     ["<b>Consistent</b>", "Converges to truth as N → ∞", "Photon mapping"],
     ["<b>Biased</b>", "E[estimate] &ne; truth", "Any bounce limit"],
     ["<b>Variance</b>", "Spread of the estimate", "<b>Visible as noise</b>"],
   ],
   "footnote": "Unbiased implies consistent. The reverse does not hold: a "
               "consistent estimator may be wrong at every finite N.",
   "note": "Photon mapping is the standard example of consistent-but-biased "
           "— bias vanishes only as the photon count goes to infinity."},

  {"t": "two", "kicker": "Diagnosis", "title": "Telling bias from variance in an image",
   "lh": "Variance",
   "l": ["<b>Looks like noise.</b> Speckle, fireflies.",
         "Different per pixel, changes with the seed.",
         "<b>Decreases with more samples.</b>",
         ("Average many renders → converges to the right answer.", 1),
         "Ugly, and honest."],
   "rh": "Bias",
   "r": ["<b>Looks like a systematic error.</b> Too dark, blurred, missing "
         "an effect.",
         "Same every time; independent of the seed.",
         "<b>Does not decrease with more samples.</b>",
         ("Average many renders → converges to the wrong answer.", 1),
         "Often prettier, and wrong."],
   "note": "The averaging test is the practical diagnostic: render with ten "
           "seeds, average, compare to a long render."},

  {"t": "section", "label": "Part 3", "title": "Validation",
   "blurb": "Build this now and keep it all semester."},

  {"t": "callout", "title": "The white furnace test",
   "kind": "The single most useful test in rendering",
   "body": ["Put a white Lambertian object (albedo 1.0) inside a uniform "
            "environment of radiance 1.0.",
            "<b>Every pixel must be exactly 1.0.</b> The object becomes "
            "invisible — it reflects exactly as much as it receives, so "
            "it cannot be distinguished from the background.",
            "<b>It catches almost everything:</b> a missing cosine, a missing "
            "π, a wrong PDF, a non-conserving BRDF, a broken sampling "
            "routine, a bad hemisphere measure.",
            "And the failure is quantitative: the ratio to 1.0 usually names "
            "the bug. 0.5 is a cosine issue; π or 1/π is a normalisation "
            "issue."]},

  {"t": "bullets", "kicker": "Suite", "title": "The validation suite to build today",
   "items": [
     "<b>Hemisphere integrates to 2π.</b> Three lines. Catches the sin θ "
     "bug permanently.",
     "",
     "<b>White furnace test.</b> At several albedos and roughnesses, once "
     "Module 07 lands.",
     "",
     "<b>&chi;² test on every sampling routine.</b> Histogram the samples "
     "against the claimed PDF. Catches sampling/PDF mismatches, which are "
     "otherwise invisible.",
     "",
     "<b>Convergence plot script.</b> RMSE against sample count, log-log. "
     "The slope must be −0.5.",
     "",
     "<b>Reference comparison.</b> Same scene in PBRT; difference the "
     "images.",
   ],
   "footnote": "Every one of these has caught a real bug for every person "
               "who has written a renderer.",
   "note": "Insist they build this now. It is the difference between the "
           "project being a week of work and a month."},

  {"t": "callout", "title": "A convergence plot tells you what kind of problem you have",
   "kind": "Read the slope",
   "body": ["Plot RMSE against a converged reference, against sample count, "
            "on log-log axes.",
            "<b>Slope −0.5:</b> correct. Pure variance, converging as it "
            "should.",
            "<b>Slope −0.5 then flat:</b> <b>bias.</b> You are converging to "
            "the wrong answer. Look for a truncated path, a clamp, or a "
            "missing term.",
            "<b>Slope shallower than −0.5:</b> your samples are correlated "
            "— a bad RNG, or the same seed across pixels.",
            "<b>Steeper than −0.5:</b> you are using a low-discrepancy "
            "sequence (Module 06), which is legitimate and good."]},

  {"t": "bullets", "kicker": "Fireflies", "title": "The pathology you will meet first",
   "items": [
     "<b>A single extremely bright pixel</b>, from one sample with a huge "
     "f/p ratio — a near-zero PDF where f was large.",
     "",
     "<b>They do not average away quickly</b>, because they are rare and "
     "enormous. The variance is dominated by them.",
     "",
     "<b>Clamping removes them and introduces bias</b> — you are "
     "discarding real energy. Common in production, and it should be a "
     "decision, not an accident.",
     "",
     "<b>The honest fixes:</b> better importance sampling (Module 06), MIS "
     "(Module 08), and a denoiser with firefly rejection (Module 12).",
   ],
   "note": "Be explicit that clamping is a bias-for-variance trade. Most "
           "renderers do it; few say so."},
 ],
 "takeaways": [
   "The Monte Carlo estimator averages f(X)/p(X). Dividing by the density "
   "corrects for uneven sampling and makes it unbiased for every N.",
   "Any p positive wherever f is non-zero gives a correct answer. The choice "
   "of p affects only variance — which is why Module 06 exists.",
   "Noise falls as 1/&radic;N: four times the samples for half the noise, a "
   "hundred times for one more digit.",
   "That rate is dimension-independent, which is why Monte Carlo is the only "
   "viable method for an integral of unbounded dimension.",
   "Unbiased means right in expectation at every N; consistent means right "
   "only in the limit. Bias looks like a systematic error, variance like "
   "noise.",
   "Build the validation suite now: hemisphere = 2&pi;, white furnace, "
   "&chi;&#178; on every sampler, and a convergence plot whose slope must "
   "be −0.5.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The estimator"),
  ("p", "We want &int; f(x) dx over some domain, and we cannot do the "
        "integral analytically. Monte Carlo integration replaces it with an "
        "average of random evaluations."),
  ("eq", "F<sub>N</sub> = (1/N) &Sigma;<sub>i=1</sub><super>N</super> "
         "f(X<sub>i</sub>) / p(X<sub>i</sub>), &nbsp;&nbsp;&nbsp; "
         "X<sub>i</sub> ~ p"),
  ("p", "Draw N samples from a probability density p of your choosing, "
        "evaluate f at each, divide by the density there, and average. "
        "<b>The division is the entire trick</b>: regions sampled more often "
        "contribute proportionally less per sample, which exactly "
        "compensates for the uneven sampling."),
  ("h2", "1.1 &nbsp; Why it is unbiased"),
  ("code", """E[F_N] = E[ (1/N) SUM_i  f(X_i)/p(X_i) ]
       = (1/N) SUM_i  E[ f(X_i)/p(X_i) ]      linearity of expectation
       = E[ f(X)/p(X) ]                       identically distributed
       = INTEGRAL (f(x)/p(x)) p(x) dx         definition of expectation
       = INTEGRAL f(x) dx  =  F               the p cancels"""),
  ("p", "The requirement is only that p(x) &gt; 0 wherever f(x) &ne; 0. If p "
        "is zero somewhere f is not, that region is never sampled, its "
        "contribution is never counted, and the estimator is biased."),
  ("callout", "Unbiased at N = 1, which is worth sitting with",
   ["The derivation never assumed N was large. A <i>single</i> sample "
    "f(X)/p(X) is an unbiased estimate of the entire integral.",
    "That sounds absurd and is correct. One sample has the right expected "
    "value and enormous variance: run the single-sample estimator many times "
    "and the average of those runs converges to F, even though any "
    "individual run may be wildly off.",
    "<b>This separation is the central idea of the whole subject.</b> "
    "Correctness and usefulness are different properties. The estimator is "
    "correct from the first sample; making it <i>useful</i> is entirely a "
    "question of reducing variance, which is what Modules 06, 08, and 09 "
    "are about."]),
  ("callout", "The choice of p affects variance only, never correctness",
   ["The proof places almost no constraint on p. Any density positive where "
    "f is non-zero yields an unbiased estimator.",
    "So choosing p badly does not make your renderer <i>wrong</i>. It makes "
    "it <i>slow</i> — sometimes by factors of thousands, which is "
    "indistinguishable from wrong in practice, but the distinction matters "
    "for debugging: a noisy image and an incorrect image are different "
    "problems with different causes.",
    "<b>The ideal p is proportional to f</b>, which would give zero "
    "variance. That is unattainable — normalising it requires knowing "
    "&int;f, which is the problem we started with — but it is the "
    "target that importance sampling aims at.",
    "<b>Module 06 is entirely about choosing p well.</b> This result is why "
    "that effort is worthwhile and why it cannot break correctness."]),

  ("h1", "2 &nbsp; Variance and the convergence rate"),
  ("eq", "V[F<sub>N</sub>] = V[ f(X)/p(X) ] / N &nbsp;&nbsp;&nbsp;&rArr;"
         "&nbsp;&nbsp;&nbsp; &sigma;[F<sub>N</sub>] &prop; 1/&radic;N"),
  ("p", "The variance of the mean of N independent samples is the variance "
        "of one sample divided by N. The standard deviation — which is "
        "what the eye sees as noise — therefore falls as the square "
        "root of the sample count."),
  ("table", ["To achieve", "Multiply samples by", "Render time"],
   [["Half the noise", "4", "4&times;"],
    ["One quarter the noise", "16", "16&times;"],
    ["One tenth the noise", "100", "100&times;"],
    ["One more decimal digit", "100", "100&times;"],
    ["Two more decimal digits", "10,000", "<b>10,000&times;</b>"]],
   [0.33, 0.27, 0.40]),
  ("callout", "The rate is brutal, and the dimension-independence is why we accept it",
   ["<b>The discouraging half:</b> noise falls slowly. Going from 'visibly "
    "noisy' to 'clean' in a difficult scene is routinely a factor of a "
    "hundred in time, and no amount of engineering changes the exponent "
    "— only the constant.",
    "<b>The decisive half:</b> the rate is 1/&radic;N <i>independent of "
    "dimension</i>. Deterministic quadrature does not have this property. A "
    "trapezoid rule in d dimensions converges as N<super>&minus;2/d</super>: "
    "excellent at d = 1, useless at d = 20, where the exponent is "
    "&minus;0.1.",
    "<b>A path with k bounces is an integral over roughly 2k dimensions</b> "
    "— two angles per scattering event — and the Neumann series "
    "of Module 02 sums over all k, so the effective dimension is unbounded.",
    "Monte Carlo is therefore not a convenient choice here. It is the only "
    "method whose convergence does not collapse entirely, and that single "
    "fact determines the shape of the entire field: since the exponent "
    "cannot be improved, essentially all research effort goes into reducing "
    "the <i>constant</i> — the variance of a single sample."]),

  ("break",),
  ("h1", "3 &nbsp; Vocabulary, used precisely"),
  ("table", ["Term", "Definition", "Rendering example"],
   [["<b>Unbiased</b>", "E[estimate] = true value, for every N including "
     "N = 1.", "Path tracing with Russian roulette."],
    ["<b>Consistent</b>", "The estimate converges to the true value as "
     "N &rarr; &infin;.",
     "Photon mapping — biased at any finite photon count, converging "
     "only as the count grows without bound."],
    ["<b>Biased</b>", "E[estimate] &ne; true value.",
     "Any fixed bounce limit; any clamp on sample values; irradiance "
     "caching."],
    ["<b>Variance</b>", "Spread of the estimate about its mean.",
     "<b>Visible directly as image noise.</b>"]],
   [0.15, 0.40, 0.45]),
  ("p", "Unbiasedness implies consistency, but not the reverse: a consistent "
        "estimator can be wrong at every finite N and still converge "
        "eventually. In practice, 'biased but consistent' usually means "
        "<i>systematically wrong in a way that gets smaller as you work "
        "harder</i>, which is often an acceptable trade — provided it "
        "is a decision rather than an accident."),
  ("table", ["", "Variance", "Bias"],
   [["Appearance", "Noise: speckle, grain, isolated bright pixels.",
     "Systematic error: uniformly too dark, over-blurred, an effect missing "
     "entirely."],
    ["Per-pixel behaviour", "Different in every pixel; changes with the "
     "random seed.",
     "Identical every run; independent of the seed."],
    ["With more samples", "<b>Decreases as 1/&radic;N.</b>",
     "<b>Does not decrease.</b>"],
    ["Averaging many renders",
     "Converges to the correct answer.",
     "Converges to the <i>wrong</i> answer."],
    ["Aesthetics", "Ugly and honest.",
     "Frequently prettier than the truth, which is what makes it "
     "dangerous."]],
   [0.17, 0.40, 0.43]),
  ("p", "<b>The practical diagnostic</b> is the averaging test: render the "
        "same scene ten times with different seeds and average the results, "
        "then compare against a single very long render. If they agree, you "
        "have variance. If they differ, you have bias, and the difference "
        "image shows you where."),

  ("h1", "4 &nbsp; Build the validation suite now"),
  ("p", "This section is the most practically valuable in the module. Build "
        "these five tests today, before writing the integrator, and keep "
        "them running for the rest of the course."),
  ("callout", "The white furnace test",
   ["<b>Setup:</b> a white Lambertian object, albedo exactly 1.0, inside a "
    "uniform environment emitting radiance exactly 1.0 in all directions.",
    "<b>Expected result:</b> every pixel is exactly 1.0, and the object is "
    "<i>invisible</i> — it reflects precisely as much as it receives, "
    "so nothing distinguishes it from the background.",
    "<b>What it catches:</b> a missing or extra cosine factor; a missing "
    "&pi; or 1/&pi;; an incorrect PDF; a BRDF that does not conserve energy; "
    "a broken direction-sampling routine; an incorrect hemisphere measure. "
    "That is most of the ways a renderer can be wrong.",
    "<b>And the failure is diagnostic rather than merely alarming.</b> The "
    "ratio to 1.0 usually names the bug: a result of 0.5 points at the "
    "cosine; &pi; or 1/&pi; at a normalisation; a value that varies with "
    "surface orientation at the hemisphere measure. Run it at several "
    "albedos — the deviation should scale predictably."]),
  ("table", ["Test", "What it checks", "Cost to build"],
   [["<b>Hemisphere = 2&pi;</b>",
     "Your solid-angle measure and any uniform direction sampler.",
     "Three lines. There is no excuse for not having it."],
    ["<b>White furnace</b>", "Energy conservation end to end. See above.",
     "A scene file and an assertion."],
    ["<b>&chi;&#178; test on every sampler</b>",
     "That each sampling routine actually draws from the PDF it claims. "
     "Histogram a million samples and compare against the analytic density.",
     "An afternoon, and it will find a real bug. A sampler/PDF mismatch is "
     "<i>invisible</i> in an image — it produces a plausible, "
     "converged, wrong result."],
    ["<b>Convergence plot</b>",
     "RMSE against a converged reference, versus sample count, on log-log "
     "axes. See below.",
     "A script. Run it on every integrator you write."],
    ["<b>Reference comparison</b>",
     "The same scene rendered in PBRT, differenced against yours.",
     "Scene conversion, once. Then it is free forever."]],
   [0.21, 0.52, 0.27]),
  ("callout", "The slope of a convergence plot diagnoses the problem",
   ["<b>Slope &minus;0.5:</b> correct behaviour. Pure variance, converging "
    "at the theoretical rate.",
    "<b>Slope &minus;0.5, then flattening to horizontal:</b> <b>bias.</b> "
    "The estimator is converging, but not to the reference. Look for a "
    "truncated path depth, a clamp, a missing term, or a reference that is "
    "itself not converged.",
    "<b>Slope shallower than &minus;0.5:</b> your samples are not "
    "independent. The usual causes are a poor random number generator or the "
    "same seed used across pixels or frames.",
    "<b>Slope steeper than &minus;0.5:</b> you are using a low-discrepancy "
    "sequence, which genuinely does better than 1/&radic;N on "
    "sufficiently smooth integrands. This is legitimate, and Module 06 "
    "explains it."]),
  ("h2", "4.1 &nbsp; Fireflies"),
  ("p", "The first pathology you will meet is a single pixel, or a scattering "
        "of them, far brighter than everything around it."),
  ("ul", ["<b>Cause:</b> one sample with an enormous f/p ratio — a "
          "direction where the integrand was large but the sampling density "
          "happened to be near zero. The estimator divides by that tiny "
          "density and produces a huge value.",
          "<b>Why they persist:</b> they are rare and extreme, so they "
          "dominate the variance. Averaging many samples removes them only "
          "slowly, and a single firefly can survive thousands of samples.",
          "<b>Clamping</b> — capping sample values at some maximum "
          "— removes them instantly and <b>introduces bias</b>, "
          "because the energy discarded was real. Most production renderers "
          "clamp. <b>The problem is not that they clamp; it is that it is "
          "often an accident rather than a decision.</b> If you clamp, say "
          "so, and report the threshold.",
          "<b>The unbiased responses</b> are better importance sampling "
          "(Module 06), multiple importance sampling (Module 08), and "
          "firefly-aware denoising (Module 12). Each attacks the cause "
          "rather than the symptom."]),
 ],
 "resources": [
   ("PBRT 4th ed. &mdash; Chapter 2, Monte Carlo Integration",
    "https://pbr-book.org/4ed/Monte_Carlo_Integration",
    "The estimator, variance, and the sampling machinery, with proofs. The "
    "primary reading."),
   ("Veach thesis &mdash; Chapter 2, Monte Carlo Integration",
    "https://graphics.stanford.edu/papers/veach_thesis/",
    "More careful than most treatments on what unbiasedness does and does "
    "not guarantee."),
   ("TU Wien Rendering &mdash; Monte Carlo lectures",
    "https://www.youtube.com/playlist?list=PLujxSBD-JXgnGmsn7gEyN28P1DnRZG7qi",
    "The intuition for why dividing by the PDF works, built up slowly. Worth "
    "watching before reading PBRT."),
   ("PBRT &mdash; the &chi;&#178; test in the test suite",
    "https://github.com/mmp/pbrt-v4",
    "A working implementation of the sampler validation in &sect;4. Copy the "
    "approach."),
 ],
 "exercises": [
   "Estimate &pi; by Monte Carlo. Plot error against N on log-log axes and "
   "confirm the slope is &minus;0.5. Keep the plotting script — you "
   "will reuse it all semester.",
   "Integrate a function you know analytically, using three different "
   "densities p. Confirm all three converge to the same value and report "
   "their variances. This makes &sect;1's claim concrete.",
   "Deliberately choose a p that is zero where f is non-zero. Show the "
   "estimator converges confidently to the wrong answer.",
   "Implement the hemisphere test and the white furnace test. Then introduce "
   "each of these bugs in turn and record what the furnace test reports: "
   "drop the cosine; drop the 1/&pi;; use an albedo of 1.1; use the wrong "
   "PDF for cosine sampling.",
   "Write a &chi;&#178; test for a sampling routine. Then deliberately "
   "mismatch the sampler and its stated PDF by a constant factor and confirm "
   "the test catches it while the rendered image does not look obviously "
   "wrong.",
   "Produce a convergence plot with an artificial bias introduced — "
   "clamp all samples at 5.0 — and confirm the curve flattens.",
   "Create a scene that produces fireflies. Measure the variance with and "
   "without clamping, and measure the energy lost to the clamp. Report both "
   "numbers.",
   "Compare the variance of estimating a 10-dimensional integral by Monte "
   "Carlo against a tensor-product trapezoid rule with the same number of "
   "evaluations. Report both errors.",
 ],
 "selfcheck": [
   "State the Monte Carlo estimator and explain what the division by p is "
   "doing.",
   "Prove unbiasedness. What is the only condition on p?",
   "Why is a single-sample estimate unbiased, and what does that tell you "
   "about the relationship between correctness and usefulness?",
   "How does the choice of p affect the result, and what would the ideal p "
   "be?",
   "State the convergence rate. How many more samples for half the noise, "
   "and for one more digit?",
   "Why is dimension-independence decisive for rendering specifically?",
   "Distinguish unbiased, consistent, and biased, and give a rendering "
   "example of each.",
   "How do you tell bias from variance by looking at images?",
   "What is the white furnace test, and name four bugs it catches.",
   "What does a convergence plot that flattens out tell you?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Sampling and Variance Reduction",
 "subtitle": "Choosing where to look, which is the whole game.",
 "question": "How do you get the same answer with far fewer samples?",
 "outcomes": [
     "Derive and apply the inverse CDF method.",
     "Sample the hemisphere uniformly and proportionally to the cosine.",
     "Explain why importance sampling reduces variance and when it fails.",
     "Compare stratification, Latin hypercube, and low-discrepancy "
     "sequences.",
     "Apply Russian roulette without introducing bias.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Drawing from a distribution",
   "blurb": "You have uniform random numbers. You need something else."},

  {"t": "eq", "kicker": "Inversion", "title": "The inverse CDF method",
   "eqs": [
     ("P(x)  =  ∫₋∞ˣ p(t) dt",
      "The cumulative distribution function: the probability of drawing a "
      "value at most x. Monotonic, from 0 to 1."),
     ("X  =  P⁻¹(ξ),    ξ ~ Uniform[0,1)",
      "Invert it and feed in a uniform variate. The result is distributed "
      "according to p."),
   ],
   "caption": "Works whenever the CDF can be inverted in closed form, which "
              "covers most of what rendering needs.",
   "note": "The geometric intuition: the CDF stretches uniform density into "
           "the shape you want. Steep where p is large."},

  {"t": "code", "kicker": "Worked", "title": "Cosine-weighted hemisphere sampling",
   "lang": "cpp", "code": """
// Want: p(ω) = cos θ / π    (the cosine in the rendering equation)
//
// Malley's method: sample the unit DISK uniformly, project up.
//   Uniform on a disk, lifted to the hemisphere, IS cosine-distributed.
//   This is a one-line proof once you see it, and no trigonometry.

vec3 cosine_sample_hemisphere(float u1, float u2) {
    float r     = sqrtf(u1);          // NOT u1 -- that clusters at the centre
    float phi   = 2.0f * PI * u2;
    float x     = r * cosf(phi);
    float y     = r * sinf(phi);
    float z     = sqrtf(fmaxf(0.0f, 1.0f - u1));   // lift to the hemisphere
    return vec3(x, y, z);
}

float cosine_pdf(const vec3& w) { return w.z / PI; }   // w.z IS cos θ

// Why this matters: the estimator becomes
//      f(x)/p(x) = (albedo/π · cos θ) / (cos θ/π) = albedo
// The cosine and the π cancel exactly. CONSTANT. Zero variance
// from the cosine factor, for free.
""",
   "caption": "The √ in the radius is the whole correctness of the disk "
              "sample. Omitting it clusters samples at the centre.",
   "note": "The cancellation at the bottom is the payoff. Show it "
           "explicitly: a diffuse bounce costs one multiply."},

  {"t": "callout", "title": "Importance sampling, stated plainly",
   "kind": "The core idea",
   "body": ["Variance comes from the <i>ratio</i> f/p varying between "
            "samples. If f/p were constant, every sample would return the "
            "same value and the variance would be zero.",
            "<b>So choose p as close to proportional to f as you can "
            "manage.</b> Where f is large, sample often; where f is small, "
            "sample rarely.",
            "<b>The perfect p = f/∫f gives zero variance</b> — and is "
            "unobtainable, since the normalisation is the integral you are "
            "computing.",
            "But you can match <i>factors</i>: the cosine, the BRDF lobe, "
            "the light's emission. Each factor matched is variance "
            "removed."]},

  {"t": "table", "kicker": "Factors", "title": "The integrand is a product; match its factors",
   "header": ["Factor", "Sample it by", "Module"],
   "widths": [3.5, 5.3, 3.3],
   "rows": [
     ["cos θ", "Malley's method — free", "This one"],
     ["BRDF f", "Analytic inversion per model", "07"],
     ["Li (the lights)", "Sample light surfaces directly", "08, 09"],
     ["<b>Their product</b>", "<b>MIS combines strategies</b>", "<b>08</b>"],
   ],
   "footnote": "No single strategy matches the product. That is the whole "
               "reason MIS exists.",
   "note": "This table is the roadmap for the next three modules. Make the "
           "structure explicit."},

  {"t": "callout", "title": "Importance sampling can make things worse",
   "kind": "The failure mode",
   "body": ["If p is small where f is large, the ratio f/p <i>explodes</i> on "
            "the rare occasions that region is sampled.",
            "<b>That is a firefly</b> (Module 05), and a badly chosen p "
            "produces far more variance than uniform sampling would "
            "have.",
            "<b>The practical rule: never let p go to zero where f might "
            "not.</b> Mix in a small uniform component — 'defensive "
            "sampling' — if you are unsure.",
            "This is why the MIS weights of Module 08 are designed to be "
            "robust rather than optimal: a strategy that is excellent "
            "usually and catastrophic occasionally is worse than one that is "
            "merely good."]},

  {"t": "section", "label": "Part 2", "title": "Where the samples go",
   "blurb": "Not just how many, but how they are arranged."},

  {"t": "two", "kicker": "Arrangement", "title": "Random is not well spread",
   "lh": "Independent uniform",
   "l": ["Each sample drawn independently.",
         "<b>Clumps and gaps.</b> Random points are not evenly "
         "distributed — they only look that way in expectation.",
         ("Variance ∝ 1/N exactly.", 1),
         "The baseline."],
   "rh": "Stratified",
   "r": ["Divide the domain into N cells, one sample jittered in each.",
         "<b>Guaranteed coverage</b>, with randomness preserved inside each "
         "cell.",
         ("Variance never worse; often far better.", 1),
         "Costs nothing. <b>Always do this.</b>"],
   "note": "Stratification is free and strictly non-harmful. There is no "
           "argument against it."},

  {"t": "callout", "title": "Stratification breaks down in high dimensions",
   "kind": "The limitation",
   "body": ["Stratifying d dimensions with k divisions each needs "
            "k<sup>d</sup> samples. At d = 10 and k = 4 that is a "
            "million.",
            "<b>Latin hypercube</b> sidesteps it: stratify each dimension "
            "<i>separately</i> with N strata and shuffle. N samples, any "
            "d.",
            "It guarantees good 1D projections but says nothing about joint "
            "distribution.",
            "<b>Padded sampling</b> is the practical compromise: stratify "
            "well in the 2–4 dimensions that matter most — pixel "
            "position, lens, the first bounce — and use lower-quality "
            "samples deeper in the path, where the integrand is smoother."]},

  {"t": "table", "kicker": "Sequences", "title": "Low-discrepancy sequences",
   "header": ["Sequence", "Property", "Use"],
   "widths": [2.7, 5.2, 4.2],
   "rows": [
     ["Halton", "Radical inverse, different prime per dimension", "Good to ~10 dims"],
     ["Sobol", "Base-2, fast, scrambles well", "<b>The practical default</b>"],
     ["Hammersley", "Halton with one dimension from i/N", "<b>Needs N known</b>"],
     ["Blue noise", "Optimised for perceptual spectrum", "Low sample counts"],
   ],
   "footnote": "Convergence up to O(log&#8319;N / N) — better than "
               "1/&radic;N on smooth integrands.",
   "note": "The caveat is that the improved rate assumes bounded variation, "
           "which rendering integrands violate at discontinuities."},

  {"t": "callout", "title": "Why blue noise, when it converges no faster",
   "kind": "A perceptual argument",
   "body": ["Blue noise sampling does not reduce error. It <b>redistributes "
            "it into high spatial frequencies</b>.",
            "The human visual system is less sensitive to high-frequency "
            "noise than to low-frequency blotches, so an image with the same "
            "RMSE <i>looks</i> cleaner.",
            "<b>It is also what denoisers prefer</b>, because "
            "high-frequency noise is easier to separate from signal than "
            "low-frequency structure.",
            "A clear case where the right metric is perceptual rather than "
            "numerical — and where reporting RMSE alone would say the "
            "technique does nothing."]},

  {"t": "section", "label": "Part 3", "title": "Russian roulette",
   "blurb": "Terminating paths without biasing the result."},

  {"t": "eq", "kicker": "Roulette", "title": "Unbiased early termination",
   "eqs": [
     ("with probability q:  return 0",
      "Kill the path."),
     ("otherwise:           return F / (1 − q)",
      "Survive, but scale up to compensate for the paths that died."),
     ("E[F']  =  q·0 + (1−q)·F/(1−q)  =  F",
      "Unbiased. The expectation is untouched."),
   ],
   "caption": "You trade variance for speed: fewer, noisier samples in the "
              "same time. Usually a good trade.",
   "note": "The one-line proof is worth doing on the board. Students "
           "distrust roulette until they see the expectation is exact."},

  {"t": "callout", "title": "Choose the survival probability from throughput",
   "kind": "How to apply it",
   "body": ["<b>Set q from the path's accumulated throughput</b> — a path "
            "carrying little energy is cheap to lose and contributes little "
            "if it survives.",
            "<b>Never start before bounce 3 or 4.</b> Early bounces carry "
            "most of the energy; killing them is a large variance increase "
            "for a small time saving.",
            "<b>Clamp the survival probability</b> to something like 0.05 "
            "minimum, or the 1/(1−q) factor becomes enormous and "
            "manufactures fireflies.",
            "<b>Compare like for like:</b> roulette must be evaluated at "
            "equal <i>time</i>, not equal sample count. At equal samples it "
            "always looks worse."]},

  {"t": "bullets", "kicker": "Practice", "title": "The order to apply these",
   "items": [
     "<b>1. Stratify.</b> Free, never harmful, immediate benefit.",
     "<b>2. Importance sample the cosine.</b> Free via Malley; cancels a "
     "factor exactly.",
     "<b>3. Importance sample the BRDF</b> (Module 07). Essential for "
     "glossy.",
     "<b>4. Sample the lights</b> (Module 08). Essential for small lights.",
     "<b>5. Combine them with MIS</b> (Module 08). <b>The single biggest "
     "win.</b>",
     "<b>6. Low-discrepancy sequences.</b> A solid further factor.",
     "<b>7. Russian roulette.</b> Speed, at some variance cost.",
     "",
     "<b>Measure after each.</b> Equal-time RMSE, not intuition.",
   ],
   "footnote": "Done in this order, each step's benefit is visible in "
               "isolation.",
   "note": "Insist on measurement. Several of these interact, and some "
           "'obvious' optimisations lose at equal time."},
 ],
 "takeaways": [
   "The inverse CDF method turns uniform variates into any distribution "
   "whose CDF you can invert.",
   "Cosine-weighted hemisphere sampling via Malley's method makes the cosine "
   "and the &pi; cancel exactly — a diffuse bounce becomes a multiply "
   "by albedo.",
   "Variance comes from f/p varying. Make p proportional to f and it "
   "vanishes; match individual factors and it shrinks.",
   "A p that is small where f is large is worse than uniform — it "
   "manufactures fireflies. Never let p reach zero where f may not.",
   "Stratification is free and never harmful; it breaks down in high "
   "dimensions, where Latin hypercube and padded sampling take over.",
   "Russian roulette terminates paths without bias by scaling survivors. "
   "Judge it at equal time, never at equal sample count.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Drawing from a distribution"),
  ("p", "A random number generator gives uniform variates on [0,1). Every "
        "sampling routine in a renderer is a method for turning those into "
        "something else."),
  ("eq", "P(x) = &int;<sub>&minus;&infin;</sub><super>x</super> p(t) dt "
         "&nbsp;&nbsp;&nbsp;&nbsp; X = P<super>&minus;1</super>(&xi;), "
         "&nbsp; &xi; ~ U[0,1)"),
  ("p", "The cumulative distribution function is monotonic and runs from 0 "
        "to 1, so it can be inverted. Feeding a uniform variate into the "
        "inverse produces a sample distributed according to p. Geometrically, "
        "the CDF is steep where the density is high, so a uniform step in "
        "&xi; maps to a small step in x there — which is precisely "
        "concentrating samples where the density is large."),
  ("h2", "1.1 &nbsp; Cosine-weighted hemisphere sampling"),
  ("p", "The most useful instance in rendering. The rendering equation "
        "contains a cos&theta; factor, so sampling proportionally to the "
        "cosine removes it from the estimator entirely."),
  ("code", """vec3 cosine_sample_hemisphere(float u1, float u2) {
    float r   = sqrtf(u1);              // sqrt: uniform area on the disk
    float phi = 2.0f * PI * u2;
    float z   = sqrtf(fmaxf(0.0f, 1.0f - u1));
    return vec3(r*cosf(phi), r*sinf(phi), z);
}
float cosine_pdf(const vec3& w) { return w.z / PI; }"""),
  ("p", "This is <b>Malley's method</b>: sample a point uniformly on the "
        "unit disk and project it vertically onto the hemisphere. The result "
        "is exactly cosine-distributed, with no trigonometric inversion "
        "required. The &radic; in the radius is what makes the disk sample "
        "uniform by <i>area</i> — using u1 directly clusters samples "
        "near the centre, and it is the most common bug in this routine."),
  ("callout", "Why this particular density is worth the trouble",
   ["Take a Lambertian surface with albedo &rho;. The integrand is "
    "(&rho;/&pi;)&middot;L&middot;cos&theta;, and the cosine-weighted "
    "density is cos&theta;/&pi;. The estimator is their ratio:",
    "<b>f/p = (&rho;/&pi; &middot; L &middot; cos&theta;) / (cos&theta;/&pi;) "
    "= &rho; &middot; L</b>",
    "The cosine cancels and the &pi; cancels. A diffuse bounce reduces to "
    "multiplying the path throughput by the albedo — one multiply, no "
    "trigonometry, and <b>zero variance contributed by the cosine "
    "factor</b>.",
    "This is importance sampling working perfectly on one factor of the "
    "integrand, and it is free. It also explains why diffuse surfaces are "
    "the cheapest thing a path tracer renders."]),

  ("h1", "2 &nbsp; Importance sampling"),
  ("callout", "Variance comes from the ratio, not the function",
   ["The Monte Carlo estimator returns f(X)/p(X). Its variance is the "
    "variance of <i>that ratio</i> across samples.",
    "If f/p were constant, every sample would return the same number and the "
    "variance would be exactly zero — regardless of how complicated f "
    "itself is.",
    "<b>So the goal is to choose p proportional to f.</b> Where the "
    "integrand is large, sample often; where it is small, sample rarely; and "
    "the division by p undoes the bias this introduces.",
    "The ideal p = f/&int;f gives zero variance and is unobtainable, because "
    "normalising it requires the integral we set out to compute. <b>But the "
    "integrand is a product, and its factors can be matched "
    "individually.</b>"]),
  ("table", ["Factor of the integrand", "Sampled by", "Covered in"],
   [["cos&theta;<sub>i</sub>", "Malley's method. Exact, and free.",
     "This module."],
    ["The BRDF f", "Analytic inversion of each material's lobe — GGX "
     "has a closed-form visible-normal sampling routine.", "Module 07."],
    ["L<sub>i</sub>, the incoming radiance",
     "Sampling points on light sources directly, and building a 2D CDF over "
     "an environment map.", "Modules 08 and 09."],
    ["<b>Their product</b>",
     "<b>No single strategy.</b> Multiple importance sampling combines "
     "several strategies, each matching one factor, with weights that are "
     "robust to any one of them failing.", "<b>Module 08.</b>"]],
   [0.22, 0.52, 0.26]),
  ("callout", "A bad p is worse than no p at all",
   ["Importance sampling is not uniformly beneficial. If p is small in a "
    "region where f is large, then on the rare occasions a sample lands "
    "there, f/p is enormous.",
    "<b>That is exactly the firefly of Module 05</b>, and a badly chosen "
    "density can produce far higher variance than uniform sampling would "
    "have.",
    "<b>The rule: never let p approach zero where f might not be zero.</b> "
    "If in doubt, mix a small uniform component into the density — "
    "'defensive sampling'. The cost is a slight increase in variance "
    "everywhere; the benefit is removing an unbounded tail.",
    "This is also why the MIS weights of Module 08 are designed for "
    "<i>robustness</i> rather than optimality. A strategy that is excellent "
    "99% of the time and catastrophic 1% of the time is worse, in practice, "
    "than one that is merely good always."]),

  ("break",),
  ("h1", "3 &nbsp; Sample placement"),
  ("table", ["", "Independent uniform", "Stratified"],
   [["Method", "Draw each sample independently.",
     "Divide the domain into N equal cells; place one jittered sample in "
     "each."],
    ["Coverage", "<b>Clumps and gaps.</b> Random points are not evenly "
     "spread — they are even only in expectation, and any particular "
     "set is not.",
     "<b>Guaranteed</b>, with randomness retained within each cell so no "
     "aliasing is introduced."],
    ["Variance", "The 1/N baseline.",
     "<b>Never worse, usually better</b>, and dramatically better on "
     "integrands with structure."],
    ["Cost", "—", "<b>Nothing.</b> Index arithmetic."]],
   [0.12, 0.42, 0.46]),
  ("p", "<b>Always stratify.</b> It cannot hurt, it costs nothing, and the "
        "benefit on primary rays and light sampling is immediate and "
        "visible."),
  ("callout", "Stratification does not survive high dimensions",
   ["Stratifying d dimensions with k divisions in each requires "
    "k<super>d</super> samples. At d = 10 with a modest k = 4, that is over "
    "a million samples — for one pixel.",
    "<b>Latin hypercube sampling</b> avoids the explosion: stratify each "
    "dimension <i>independently</i> into N strata, then randomly permute the "
    "assignment across dimensions. N samples suffice for any d, and every 1D "
    "projection is perfectly stratified.",
    "The limitation is that it guarantees nothing about the <i>joint</i> "
    "distribution — the samples can still clump in 2D while being "
    "perfectly spread in each axis.",
    "<b>Padded sampling is the practical answer.</b> Stratify carefully in "
    "the two to four dimensions that matter most — pixel position, "
    "lens position, the first bounce direction, the first light sample "
    "— and use cheaper, lower-quality samples deeper in the path, where "
    "the integrand is smoother and errors are less visible. Every production "
    "renderer does something of this kind."]),
  ("h2", "3.1 &nbsp; Low-discrepancy sequences"),
  ("p", "Discrepancy measures how far a point set deviates from perfectly "
        "uniform coverage. Low-discrepancy sequences are deterministic "
        "constructions that achieve much better coverage than random points, "
        "and they are designed so that <i>any</i> prefix of the sequence is "
        "well distributed — which matters because you do not know in "
        "advance how many samples a pixel will need."),
  ("table", ["Sequence", "Construction", "In practice"],
   [["<b>Halton</b>", "Radical inverse in a different prime base per "
     "dimension.",
     "Good to about ten dimensions; the high primes correlate badly without "
     "scrambling."],
    ["<b>Sobol</b>", "Base 2 throughout, using direction numbers.",
     "<b>The practical default.</b> Fast to generate, scrambles well, and "
     "handles high dimensions better than Halton."],
    ["<b>Hammersley</b>", "Halton with the first dimension replaced by i/N.",
     "Slightly better, but <b>requires N to be fixed in advance</b>, which "
     "rules out adaptive sampling."],
    ["<b>Blue noise</b>", "Point sets optimised so the error spectrum has "
     "little low-frequency energy.", "See below."]],
   [0.16, 0.38, 0.46]),
  ("p", "On integrands of bounded variation these converge as "
        "O(log<super>d</super>N / N), which is asymptotically far better "
        "than 1/&radic;N. <b>The caveat matters:</b> rendering integrands "
        "are discontinuous at every visibility boundary and do not have "
        "bounded variation, so the theoretical rate is not achieved. The "
        "practical improvement is nonetheless real and typically worth a "
        "factor of two to four in equal-quality time."),
  ("callout", "Blue noise improves nothing measurable and is worth using",
   ["Blue noise sample placement does not reduce RMSE. It <b>redistributes "
    "the error into high spatial frequencies</b>, leaving the total "
    "unchanged.",
    "The human visual system is markedly less sensitive to high-frequency "
    "noise than to low-frequency blotching, so two images with identical "
    "RMSE can look very different — and the blue-noise one looks "
    "substantially cleaner.",
    "<b>Denoisers also prefer it</b>, for the related reason that "
    "high-frequency noise is easier to separate from the underlying signal "
    "than low-frequency structure is. A denoiser applied to blue-noise input "
    "produces a better result from the same sample count.",
    "<b>This is a case where RMSE is the wrong metric</b> and reporting it "
    "alone would conclude the technique does nothing. Perceptual metrics "
    "such as FLIP capture the difference; so does looking at the images."]),

  ("h1", "4 &nbsp; Russian roulette"),
  ("p", "Paths must terminate. Truncating at a fixed depth is biased "
        "(Module 02) — it simply discards the tail of the Neumann "
        "series. Russian roulette terminates paths <i>stochastically</i> "
        "while leaving the expectation exactly correct."),
  ("eq", "F&prime; = 0 with probability q; &nbsp;&nbsp; F / (1 &minus; q) "
         "otherwise"),
  ("eq", "E[F&prime;] = q &middot; 0 + (1 &minus; q) &middot; F / "
         "(1 &minus; q) = F"),
  ("p", "Paths are killed at random, and the survivors are scaled up by "
        "exactly the factor needed to compensate for those that died. The "
        "expected value is untouched; the variance increases, because some "
        "samples now return zero and others return more than they would "
        "have. <b>You are trading variance for speed</b>, which is usually a "
        "good trade because the time saved buys more samples."),
  ("callout", "How to choose the survival probability",
   ["<b>Base it on the path's accumulated throughput.</b> A path whose "
    "throughput has fallen to 0.01 can contribute little even if it survives, "
    "so it is cheap to terminate. A path still carrying 0.9 should be kept. "
    "Setting the survival probability to the throughput's maximum component "
    "is the standard choice.",
    "<b>Do not start before bounce three or four.</b> Early bounces carry "
    "most of the energy in the image, and killing them increases variance "
    "substantially while saving little time.",
    "<b>Clamp the survival probability from below</b> — 0.05 is a "
    "common floor. Otherwise the 1/(1&minus;q) factor on a surviving path "
    "becomes enormous, and roulette starts <i>manufacturing</i> fireflies, "
    "which is the opposite of what you wanted.",
    "<b>Evaluate it at equal time, not equal samples.</b> At a fixed sample "
    "count roulette always looks worse, because it is strictly adding "
    "variance. Its entire benefit is that each sample is cheaper, so you get "
    "more of them — which only shows up in an equal-time comparison. "
    "This mistake is extremely common."]),
  ("h1", "5 &nbsp; The order to apply these"),
  ("table", ["Step", "Technique", "Why in this position"],
   [["1", "<b>Stratification</b>", "Free, never harmful, immediately "
     "visible on primary rays."],
    ["2", "<b>Cosine-weighted sampling</b>", "Free via Malley, and cancels "
     "a factor of the integrand exactly."],
    ["3", "<b>BRDF sampling</b> (Module 07)",
     "Essential the moment any surface is glossy."],
    ["4", "<b>Light sampling</b> (Module 08)",
     "Essential the moment any light is small."],
    ["5", "<b>MIS</b> (Module 08)",
     "<b>The single largest win in the course.</b> Needs 3 and 4 first."],
    ["6", "<b>Low-discrepancy sequences</b>",
     "A further factor of two to four, once the strategy is right."],
    ["7", "<b>Russian roulette</b>",
     "Speed at some variance cost. Last, because it interacts with "
     "everything above."]],
   [0.07, 0.31, 0.62]),
  ("p", "<b>Measure after each step, at equal time.</b> Several of these "
        "interact, and intuition about which will help is unreliable "
        "— the point of the convergence-plot script from Module 05 is "
        "that you do not have to guess."),
 ],
 "resources": [
   ("PBRT 4th ed. &mdash; Chapter 2.2&ndash;2.4 and Chapter 8, Sampling and "
    "Reconstruction",
    "https://pbr-book.org/4ed/Sampling_and_Reconstruction",
    "Inversion, the standard sampling routines, stratification, and the "
    "Sobol sampler with complete code."),
   ("PBRT &mdash; A.5, Sampling Algorithms",
    "https://pbr-book.org/4ed/Sampling_Algorithms",
    "The reference list of how to sample every common distribution in "
    "rendering. Worth bookmarking."),
   ("Veach thesis &mdash; Chapter 2 on variance reduction",
    "https://graphics.stanford.edu/papers/veach_thesis/",
    "Careful treatment of importance sampling, including when it fails and "
    "why defensive sampling is sometimes necessary."),
   ("Christensen & Jarosz &mdash; The Path to Path-Traced Movies (free)",
    "https://graphics.pixar.com/library/",
    "What production renderers actually do about sampling, stratification, "
    "and roulette. Useful reality check on &sect;5."),
   ("Heitz &mdash; blue-noise sampling papers (free)",
    "https://eheitzresearch.wordpress.com/",
    "The perceptual argument of &sect;3 developed properly, with sample "
    "sets you can use."),
 ],
 "exercises": [
   "Implement the inverse CDF method for an exponential distribution and "
   "verify with a &chi;&#178; test against the analytic density.",
   "Implement uniform and cosine-weighted hemisphere sampling. Verify both "
   "with &chi;&#178; tests. Then render a diffuse scene with each and report "
   "the variance ratio.",
   "Deliberately use u1 instead of &radic;u1 in the disk radius. Plot the "
   "resulting sample distribution and explain what the furnace test "
   "reports.",
   "Construct a case where importance sampling increases variance: choose a "
   "p that is small where f is large. Report the variance against uniform "
   "sampling.",
   "Implement stratified sampling for pixel positions and measure the "
   "variance reduction on an edge-heavy scene against independent uniform "
   "sampling.",
   "Implement a Sobol sampler and produce a convergence plot against "
   "independent random sampling on the same scene. Report both slopes.",
   "Compare stratified, Latin hypercube, and Sobol sampling at 16, 64, and "
   "256 samples per pixel. Report RMSE for all nine combinations.",
   "Implement Russian roulette. Compare against a fixed bounce limit at "
   "<b>equal time</b>, and separately at equal sample count. Report both and "
   "explain the difference.",
   "Apply the seven steps of &sect;5 one at a time, measuring equal-time "
   "RMSE after each. Produce a single table. This is the most useful "
   "exercise in the module.",
 ],
 "selfcheck": [
   "State the inverse CDF method and explain geometrically why it works.",
   "Describe Malley's method and show that the cosine and &pi; cancel for a "
   "Lambertian surface.",
   "What causes variance in a Monte Carlo estimator, and what would the "
   "ideal density be?",
   "Why can the ideal density never be used, and what is matched instead?",
   "How can importance sampling make an estimator worse, and what is the "
   "defence?",
   "Why does stratification fail in high dimensions, and what two approaches "
   "replace it?",
   "What does a low-discrepancy sequence guarantee, and why is the "
   "theoretical rate not achieved in rendering?",
   "Why use blue noise if it does not reduce RMSE?",
   "Prove Russian roulette is unbiased, and give three rules for applying it "
   "well.",
   "Why must Russian roulette be evaluated at equal time rather than equal "
   "sample count?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "BSDFs and Microfacet Theory",
 "subtitle": "Where materials come from, and how to sample them.",
 "question": "What function describes a real surface, and how do you sample "
             "it?",
 "outcomes": [
     "Derive the microfacet BRDF and explain each of its three terms.",
     "Explain why GGX displaced Beckmann.",
     "Implement visible-normal sampling and its PDF.",
     "Handle specular surfaces correctly in a Monte Carlo renderer.",
     "Verify a BSDF for energy conservation and reciprocity.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The microfacet model",
   "blurb": "A rough surface is a field of tiny mirrors."},

  {"t": "callout", "title": "The modelling assumption",
   "kind": "Where the model comes from",
   "body": ["A surface that looks rough is, below the scale of a pixel, a "
            "field of <b>microfacets</b> — tiny perfectly specular "
            "mirrors with varying orientations.",
            "You cannot resolve them, so you see the <i>statistical "
            "aggregate</i> of their reflections.",
            "<b>Roughness is therefore a distribution of facet "
            "orientations</b>, not an arbitrary blur parameter.",
            "This is why microfacet models look right where ad-hoc models "
            "look like plastic: the lobe shape, the grazing-angle "
            "brightening, and the correlation between roughness and highlight "
            "size all follow from the geometry rather than being tuned."]},

  {"t": "eq", "kicker": "The model", "title": "The microfacet BRDF",
   "eqs": [
     ("f(ωi, ωo)  =  D(h) · F(ωo·h) · G(ωi, ωo)  /  (4 |n·ωi| |n·ωo|)",
      "Three physical terms over a geometric normalisation. h is the half "
      "vector, normalize(ωi + ωo)."),
     ("D(h)   — how many facets point along h",
      "The normal distribution function. This is what 'roughness' means."),
     ("F(ωo·h)  — how much those facets reflect",
      "Fresnel. Rises to 1 at grazing incidence for every material."),
     ("G(ωi, ωo)  — what fraction is not shadowed or masked",
      "Facets occlude each other at grazing angles. Without this, energy is "
      "created."),
   ],
   "caption": "Only facets whose normal is exactly h can reflect ωi into ωo. "
              "That constraint is the whole derivation.",
   "note": "The half-vector constraint is the key insight. Everything else "
           "is counting the facets that satisfy it."},

  {"t": "two", "kicker": "D", "title": "Why GGX replaced Beckmann",
   "lh": "Beckmann",
   "l": ["Gaussian surface-height statistics.",
         "Physically motivated; derived from surface metrology.",
         ("Falls off quickly away from the peak.", 1),
         "<b>Highlights end abruptly.</b> Measured materials have more "
         "energy in the tail than it predicts."],
   "rh": "GGX / Trowbridge–Reitz",
   "r": ["Heavier tails by construction.",
         "Originally an empirical fit.",
         ("Long, smooth falloff.", 1),
         "<b>Matches measured data far better</b>, especially the "
         "glow around a highlight. Universal since ~2012."],
   "note": "Good example of empirical fit beating physical derivation. "
           "Worth saying out loud."},

  {"t": "eq", "kicker": "GGX", "title": "The distribution and its shadowing term",
   "eqs": [
     ("D(h) = α² / ( π ((n·h)²(α²−1) + 1)² )",
      "The GGX normal distribution. α is roughness squared by convention, "
      "which makes the artist-facing parameter perceptually linear."),
     ("Λ(ω) = (−1 + √(1 + α² tan²θ)) / 2",
      "The Smith lambda function for GGX."),
     ("G₂(ωi,ωo) = 1 / (1 + Λ(ωi) + Λ(ωo))",
      "Height-correlated Smith masking-shadowing. Use this, not the "
      "separable G₁(ωi)·G₁(ωo)."),
   ],
   "caption": "Height-correlated G₂ is strictly more accurate than the "
              "separable form and costs nothing extra.",
   "note": "Many implementations still use the separable form out of habit. "
           "Flag it."},

  {"t": "callout", "title": "The single-scattering model loses energy",
   "kind": "A real limitation, honestly stated",
   "body": ["The standard model accounts for light bouncing off <b>one</b> "
            "microfacet.",
            "At high roughness, light genuinely bounces between facets "
            "several times before escaping. The model throws that energy "
            "away.",
            "<b>A rough white metal can lose over 50% of its energy</b> — "
            "it renders far too dark, and the error grows with roughness, so "
            "a roughness slider also darkens the material.",
            "<b>Fixes:</b> Kulla–Conty energy compensation (a small "
            "precomputed table, now standard) or a true multiple-scattering "
            "model. The furnace test at high roughness exposes this "
            "immediately."]},

  {"t": "section", "label": "Part 2", "title": "Sampling",
   "blurb": "Evaluating a BSDF is easy. Sampling it well is the work."},

  {"t": "callout", "title": "Sample visible normals, not all normals",
   "kind": "The important refinement",
   "body": ["The obvious approach samples D(h) directly and reflects about "
            "the chosen h.",
            "<b>But many of those facets are not visible from ωo</b> — "
            "they face away, or are masked. Samples that hit them are "
            "wasted, and the waste grows at grazing angles.",
            "<b>Visible-normal sampling (Heitz 2018)</b> draws from the "
            "distribution of normals <i>visible from the outgoing "
            "direction</i>. Every sample is usable.",
            "<b>Typically 2–3× less variance at grazing angles, for a few "
            "extra lines.</b> It is strictly better; there is no reason to "
            "use the older method."]},

  {"t": "code", "kicker": "Sampling", "title": "GGX visible-normal sampling",
   "lang": "cpp", "code": """
// Heitz 2018, "Sampling the GGX Distribution of Visible Normals".
vec3 sample_ggx_vndf(vec3 wo, float ax, float ay, float u1, float u2) {
    // 1. Warp to the hemisphere configuration (roughness -> 1).
    vec3 Vh = normalize(vec3(ax * wo.x, ay * wo.y, wo.z));

    // 2. Orthonormal basis around Vh, robust at Vh.z near -1.
    float lensq = Vh.x*Vh.x + Vh.y*Vh.y;
    vec3 T1 = lensq > 0 ? vec3(-Vh.y, Vh.x, 0) * rsqrt(lensq) : vec3(1,0,0);
    vec3 T2 = cross(Vh, T1);

    // 3. Uniform point on the projected disk, squashed for the hemisphere.
    float r = sqrtf(u1), phi = 2*PI*u2;
    float t1 = r*cosf(phi), t2 = r*sinf(phi);
    float s  = 0.5f * (1.0f + Vh.z);
    t2 = (1.0f - s)*sqrtf(1.0f - t1*t1) + s*t2;

    // 4. Project onto the hemisphere and unwarp.
    vec3 Nh = t1*T1 + t2*T2 + sqrtf(fmaxf(0.f, 1 - t1*t1 - t2*t2))*Vh;
    return normalize(vec3(ax*Nh.x, ay*Nh.y, fmaxf(0.f, Nh.z)));
}

// PDF of the sampled DIRECTION (not of the half vector):
//   pdf = D_visible(h) / (4 · |wo·h|)
// The 1/(4|wo·h|) is the Jacobian of the reflection operator.
""",
   "caption": "The Jacobian in the PDF is the most commonly omitted factor "
              "in a BSDF implementation. The χ² test catches it instantly.",
   "note": "Emphasise the Jacobian. An omitted 1/(4|wo·h|) gives a plausible "
           "but wrong image."},

  {"t": "callout", "title": "Specular surfaces need a separate path",
   "kind": "Delta distributions",
   "body": ["A perfect mirror's BRDF is a Dirac delta. It is infinite in one "
            "direction and zero everywhere else.",
            "<b>You cannot evaluate it</b> — the probability of sampling "
            "the exact reflected direction is zero. <b>You cannot "
            "importance sample it</b> with a finite PDF.",
            "<b>You must handle it as a special case:</b> choose the "
            "reflected direction deterministically and return the weight "
            "F(ωo·n) with a PDF of 1.",
            "<b>And flag it.</b> Next-event estimation (Module 08) must skip "
            "specular vertices, and MIS weights must treat them as having "
            "infinite density, or you double-count."]},

  {"t": "table", "kicker": "Interface", "title": "What a BSDF must provide",
   "header": ["Method", "Returns", "Note"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["<code>f(wo, wi)</code>", "BRDF value", "<b>Zero for specular</b>"],
     ["<code>sample(wo, u)</code>", "wi, f, pdf, flags", "One call: the three are coupled"],
     ["<code>pdf(wo, wi)</code>", "Density of that direction", "<b>Needed for MIS</b>"],
     ["<code>flags</code>", "specular / diffuse / glossy, R / T", "Drives integrator logic"],
   ],
   "footnote": "<code>pdf()</code> must be queryable independently of "
               "<code>sample()</code>. MIS needs the density of a direction "
               "the BSDF did not choose.",
   "note": "The independent pdf() is the design requirement students miss, "
           "and it forces a rewrite in Module 08 if omitted."},

  {"t": "section", "label": "Part 3", "title": "Beyond reflection",
   "blurb": "Transmission, layering, and what real materials need."},

  {"t": "bullets", "kicker": "Extensions", "title": "What a usable material system adds",
   "items": [
     "<b>Transmission (BTDF).</b> Snell's law, total internal reflection, "
     "and a non-symmetric Jacobian from the refractive index change.",
     "",
     "<b>Rough transmission.</b> The same microfacet machinery with the "
     "refraction half vector. Frosted glass.",
     "",
     "<b>Layered materials.</b> A coating over a base — car paint, "
     "varnished wood, skin. Correct treatment is expensive; most renderers "
     "approximate.",
     "",
     "<b>Anisotropy.</b> Separate roughness along the two tangent "
     "directions. Brushed metal, hair, fabric.",
     "",
     "<b>Measured BRDFs.</b> MERL and similar databases. Accurate, "
     "expensive to store and awkward to importance sample.",
   ],
   "note": "The non-symmetry of refraction is a classic source of bugs in "
           "bidirectional renderers — mention it now."},

  {"t": "callout", "title": "Test every BSDF three ways",
   "kind": "Non-negotiable",
   "body": ["<b>&chi;² test:</b> histogram the sampled directions against "
            "the PDF your <code>pdf()</code> reports. Catches sampler/PDF "
            "mismatch, which is invisible in an image.",
            "<b>White furnace test:</b> at albedo 1, integrate f·cos over "
            "the hemisphere. Must be ≤ 1, and ≈ 1 for a lossless "
            "material. <b>Run it at several roughnesses</b> — this is "
            "where the energy loss above shows up.",
            "<b>Reciprocity:</b> evaluate f with the arguments swapped over "
            "random pairs. Must match to floating-point tolerance.",
            "<b>A BSDF that passes all three is almost certainly correct. "
            "One that passes none can still look fine</b>, which is the "
            "problem."]},
 ],
 "takeaways": [
   "A microfacet model treats a rough surface as a statistical field of tiny "
   "mirrors; roughness is a distribution of facet orientations.",
   "f = D&middot;F&middot;G / (4|n&middot;&omega;i||n&middot;&omega;o|). Only "
   "facets whose normal is the half vector can reflect &omega;i into "
   "&omega;o.",
   "GGX displaced Beckmann because its heavier tails match measured "
   "materials better — an empirical fit beating a physical derivation.",
   "The single-scattering model loses substantial energy at high roughness. "
   "Use Kulla–Conty compensation and check with the furnace test.",
   "Sample visible normals, not all normals: every sample is usable, and it "
   "is 2–3&times; better at grazing angles for a few extra lines.",
   "Specular surfaces are delta distributions and need a separate code path, "
   "flagged so that NEE and MIS can handle them correctly.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Where the model comes from"),
  ("callout", "A rough surface is a field of tiny mirrors",
   ["The microfacet assumption is that a surface which appears rough is, at "
    "a scale below what a pixel can resolve, composed of many perfectly "
    "specular facets with varying orientations.",
    "You never see an individual facet. You see the <b>statistical "
    "aggregate</b> of their reflections, which is why a rough metal has a "
    "broad highlight and a polished one has a sharp reflection — the "
    "same physics, different orientation statistics.",
    "<b>So 'roughness' is a distribution of facet normals</b>, not a blur "
    "radius chosen to taste. This is the reason microfacet models look "
    "convincing where earlier ad-hoc models looked like plastic: the shape "
    "of the highlight, the brightening at grazing angles, and the "
    "relationship between roughness and highlight size all <i>follow</i> "
    "from the geometry rather than being independently tuned.",
    "It also explains why they generalise. A model derived from an "
    "assumption makes predictions in configurations it was never fitted to."]),
  ("eq", "f(&omega;<sub>i</sub>, &omega;<sub>o</sub>) = "
         "D(h) &middot; F(&omega;<sub>o</sub>&middot;h) &middot; "
         "G(&omega;<sub>i</sub>, &omega;<sub>o</sub>) / "
         "( 4 |n&middot;&omega;<sub>i</sub>| |n&middot;&omega;<sub>o</sub>| )"),
  ("p", "where h = normalize(&omega;<sub>i</sub> + &omega;<sub>o</sub>) is "
        "the <b>half vector</b>. The derivation rests on one observation: "
        "<b>only a facet whose normal is exactly h can reflect "
        "&omega;<sub>i</sub> into &omega;<sub>o</sub></b>. Everything else "
        "is counting how many such facets there are, how much they reflect, "
        "and how many of them are actually visible."),
  ("table", ["Term", "Answers", "Without it"],
   [["<b>D(h)</b> — normal distribution",
     "What fraction of facets are oriented along h?",
     "No concept of roughness. This term <i>is</i> the material's "
     "appearance."],
    ["<b>F(&omega;<sub>o</sub>&middot;h)</b> — Fresnel",
     "What fraction of light striking such a facet is reflected rather than "
     "transmitted or absorbed?",
     "No grazing-angle brightening. Every surface becomes mirror-like at "
     "glancing incidence in reality, and this term is why."],
    ["<b>G</b> — masking-shadowing",
     "What fraction of those facets is neither hidden from the light nor "
     "hidden from the viewer by neighbouring facets?",
     "<b>Energy is created</b> at grazing angles. The furnace test fails "
     "loudly, with values well above 1."],
    ["<b>4|n&middot;&omega;<sub>i</sub>||n&middot;&omega;<sub>o</sub>|</b>",
     "Normalisation from the change of variables between half-vector space "
     "and direction space.",
     "A constant factor error that varies with angle — the worst kind, "
     "because it cannot be scaled away."]],
   [0.21, 0.42, 0.37]),
  ("h2", "1.1 &nbsp; Why GGX displaced Beckmann"),
  ("table", ["", "Beckmann", "GGX / Trowbridge&ndash;Reitz"],
   [["Origin", "Derived from Gaussian surface-height statistics; physically "
     "motivated by surface metrology.",
     "Originally an empirical fit (Trowbridge&ndash;Reitz 1975), "
     "reintroduced to graphics by Walter et al. in 2007."],
    ["Tail behaviour", "Falls off quickly away from the peak.",
     "<b>Heavy tails</b> — significant energy far from the specular "
     "direction."],
    ["Against measured data",
     "Highlights terminate too abruptly; measured materials have more energy "
     "in the tail than it predicts.",
     "<b>Matches measurements substantially better</b>, particularly the "
     "soft glow surrounding a highlight."],
    ["Status", "Historical.",
     "<b>Universal since about 2012.</b> Every production renderer and "
     "every real-time engine."]],
   [0.14, 0.42, 0.44]),
  ("p", "This is a case worth noticing: the empirically fitted distribution "
        "beat the physically derived one, because the physical derivation's "
        "assumption — Gaussian height statistics — does not "
        "describe real machined and worn surfaces as well as the fit does. "
        "Deriving from first principles does not guarantee a better model "
        "than measuring."),
  ("eq", "D(h) = &alpha;&#178; / ( &pi; ( (n&middot;h)&#178; "
         "(&alpha;&#178; &minus; 1) + 1 )&#178; )"),
  ("p", "By convention &alpha; = roughness&#178;, where roughness is the "
        "parameter exposed to artists. The squaring makes the control "
        "perceptually linear — equal steps in the slider produce "
        "roughly equal perceived changes, which they do not if &alpha; is "
        "exposed directly."),
  ("eq", "&Lambda;(&omega;) = ( &minus;1 + &radic;(1 + &alpha;&#178; "
         "tan&#178;&theta;) ) / 2 &nbsp;&nbsp;&nbsp;&nbsp; "
         "G&#8322; = 1 / ( 1 + &Lambda;(&omega;<sub>i</sub>) + "
         "&Lambda;(&omega;<sub>o</sub>) )"),
  ("p", "This is the <b>height-correlated</b> Smith masking-shadowing "
        "function. The older separable form "
        "G&#8321;(&omega;<sub>i</sub>)&middot;G&#8321;(&omega;<sub>o</sub>) "
        "assumes masking and shadowing are independent, which they are not "
        "— a facet visible to the viewer is more likely to be visible "
        "to the light. The correlated form is more accurate and costs "
        "nothing additional. Many implementations still use the separable "
        "version out of habit."),
  ("callout", "The single-scattering model loses a great deal of energy",
   ["The standard microfacet BRDF accounts for light that strikes "
    "<b>one</b> facet and leaves. In reality, at high roughness, light "
    "frequently bounces between several facets before escaping the surface.",
    "<b>That energy is simply discarded.</b> For a rough white metal the "
    "loss can exceed 50% — the material renders far darker than it "
    "should, and because the loss grows with roughness, the roughness slider "
    "doubles as an unwanted brightness control.",
    "<b>The fix in production is Kulla&ndash;Conty energy compensation:</b> "
    "precompute the directional albedo of the single-scattering model as a "
    "function of roughness and viewing angle, store it in a small table, and "
    "add back the missing energy as an additional lobe. It is a few hundred "
    "lines and is now standard.",
    "<b>The furnace test at high roughness exposes this immediately</b>, "
    "which is why Module 05 insisted on running it at several roughness "
    "values rather than just one. A model that passes at roughness 0.1 and "
    "returns 0.45 at roughness 0.9 has exactly this problem."]),

  ("break",),
  ("h1", "2 &nbsp; Sampling a BSDF"),
  ("p", "Evaluating a BSDF is straightforward. Sampling it well — "
        "generating directions distributed approximately proportionally to "
        "it, and reporting the correct density — is where the "
        "engineering is."),
  ("callout", "Sample the visible normals, not all of them",
   ["The obvious approach samples the distribution D(h) directly, choosing a "
    "facet normal and reflecting &omega;<sub>o</sub> about it.",
    "<b>The problem is that many of those facets are not visible from "
    "&omega;<sub>o</sub></b> — they face away, or are masked by "
    "neighbouring facets. Samples that select them are wasted, and the "
    "proportion wasted grows sharply at grazing angles, which is exactly "
    "where microfacet surfaces are most interesting.",
    "<b>Visible-normal sampling</b> (Heitz, 2018) instead draws from the "
    "distribution of normals <i>visible from the outgoing direction</i>. "
    "Every sample selects a facet that can actually contribute.",
    "<b>The result is typically two to three times less variance at grazing "
    "angles</b>, for perhaps fifteen extra lines of code. It is strictly "
    "better than the older method in every configuration, and there is no "
    "longer a reason to implement sampling of D directly."]),
  ("p", "The PDF of the sampled <i>direction</i> — not of the half "
        "vector — is:"),
  ("eq", "pdf(&omega;<sub>i</sub>) = D<sub>visible</sub>(h) / "
         "( 4 |&omega;<sub>o</sub>&middot;h| )"),
  ("p", "The factor 1/(4|&omega;<sub>o</sub>&middot;h|) is the Jacobian of "
        "the reflection operator — the change of variables from the "
        "half-vector to the reflected direction. <b>It is the most commonly "
        "omitted term in a BSDF implementation.</b> Omitting it produces a "
        "plausible-looking, converged, wrong image, and no amount of staring "
        "at the render will reveal it. The &chi;&#178; test from Module 05 "
        "catches it on the first run."),
  ("callout", "Specular surfaces require a separate code path",
   ["A perfectly smooth mirror has a BRDF that is a Dirac delta: infinite in "
    "the single reflected direction, zero everywhere else.",
    "<b>It cannot be evaluated</b> — <code>f(wo, wi)</code> must "
    "return zero, because the probability that an independently chosen "
    "wi is exactly the mirror direction is zero. <b>It cannot be importance "
    "sampled</b> with a finite density, because no finite density can "
    "represent a delta.",
    "<b>Handle it explicitly:</b> <code>sample()</code> returns the "
    "reflected direction deterministically, the value F(&omega;<sub>o</sub>"
    "&middot;n), and a PDF of exactly 1 — representing a discrete "
    "choice rather than a density.",
    "<b>And set a flag.</b> Next-event estimation (Module 08) must skip "
    "specular vertices entirely, because the shadow ray's direction has zero "
    "probability of being the mirror direction. MIS must treat the specular "
    "strategy as having infinite density so its weight is 1 and the other "
    "strategy's is 0. <b>Getting this wrong double-counts energy</b>, and "
    "the symptom — mirrors that are too bright — is easy to "
    "misdiagnose as a Fresnel problem."]),
  ("table", ["Method", "Returns", "Requirements"],
   [["<code>f(wo, wi)</code>", "The BRDF value for a given pair of "
     "directions.", "<b>Must return zero for specular lobes.</b>"],
    ["<code>sample(wo, u)</code>",
     "A sampled direction, the BRDF value, the PDF, and the lobe flags.",
     "One call, because the three outputs are coupled and recomputing them "
     "separately is both slower and a source of inconsistency."],
    ["<code>pdf(wo, wi)</code>",
     "The density this BSDF would have assigned to a direction.",
     "<b>Must be queryable independently of sample().</b> MIS needs the "
     "density of a direction that the <i>light</i> sampler chose."],
    ["<code>flags</code>",
     "specular / diffuse / glossy; reflection / transmission.",
     "Drives integrator decisions: whether to do NEE, how to weight, whether "
     "the path is still 'specular' for caustic handling."]],
   [0.21, 0.38, 0.41]),
  ("p", "<b>The independently queryable <code>pdf()</code> is the design "
        "requirement most often missed</b>, and omitting it forces a rewrite "
        "in Module 08. Design for it now."),

  ("h1", "3 &nbsp; Beyond reflection"),
  ("table", ["Extension", "What it adds", "Difficulty"],
   [["<b>Transmission (BTDF)</b>",
     "Snell's law, total internal reflection, and the Fresnel split between "
     "reflected and transmitted energy.",
     "The Jacobian differs from the reflection case, and <b>the BTDF is "
     "not symmetric</b> when the refractive index changes — radiance "
     "is compressed or expanded by (&eta;<sub>o</sub>/&eta;<sub>i</sub>)"
     "&#178;. A classic source of bugs in bidirectional renderers."],
    ["<b>Rough transmission</b>",
     "The same microfacet machinery with a refraction half vector.",
     "Frosted glass. Walter et al. 2007 gives the complete derivation."],
    ["<b>Layered materials</b>",
     "A thin coating over a base: car paint, varnished wood, skin.",
     "Correct treatment requires simulating transport between the layers and "
     "is expensive. Most renderers approximate with a weighted sum of lobes, "
     "which loses energy and inter-reflection."],
    ["<b>Anisotropy</b>",
     "Independent roughness along the two tangent directions.",
     "Brushed metal, hair, satin. Requires a consistent tangent frame from "
     "the intersection (Module 03) — and a discontinuous tangent field "
     "produces visible seams."],
    ["<b>Measured BRDFs</b>",
     "Tabulated data from a gonioreflectometer (MERL, RGL databases).",
     "Maximally accurate and awkward: large to store, and importance "
     "sampling requires building a numerical CDF over the tabulated data."]],
   [0.17, 0.33, 0.50]),

  ("h1", "4 &nbsp; Testing a BSDF"),
  ("callout", "Three tests, all of them necessary",
   ["<b>&chi;&#178; test.</b> Generate a million samples with "
    "<code>sample()</code>, histogram them over the sphere, and compare "
    "against the density reported by <code>pdf()</code>. This catches any "
    "mismatch between the sampler and its stated density — including "
    "the missing Jacobian above. <b>Such a mismatch is completely invisible "
    "in a rendered image</b>, which converges confidently to a wrong answer.",
    "<b>White furnace test.</b> With albedo 1 and no absorption, integrate "
    "f&middot;cos&theta; over the hemisphere. It must not exceed 1 (or "
    "energy is created) and should be close to 1 for a lossless material. "
    "<b>Run it across the full roughness range</b> — that is where "
    "the single-scattering energy loss of &sect;1 appears, and a single "
    "test at low roughness will miss it entirely.",
    "<b>Reciprocity.</b> Evaluate f with the arguments exchanged over a "
    "thousand random direction pairs and confirm agreement to floating-point "
    "tolerance. Required for the bidirectional methods of Module 11.",
    "<b>A BSDF passing all three is almost certainly correct. A BSDF passing "
    "none can still produce an image that looks entirely reasonable</b>, "
    "which is precisely why these tests exist rather than relying on "
    "inspection."]),
 ],
 "resources": [
   ("PBRT 4th ed. &mdash; Chapters 9 and 14, Reflection Models and "
    "Sampling",
    "https://pbr-book.org/4ed/Reflection_Models",
    "The complete treatment with code: Fresnel, microfacet distributions, "
    "Smith masking, and the sampling routines."),
   ("Walter et al. &mdash; Microfacet Models for Refraction through Rough "
    "Surfaces (2007, free)",
    "https://www.graphics.cornell.edu/~bjw/microfacetbsdf.pdf",
    "The paper that brought GGX into graphics, including the rough "
    "transmission derivation of &sect;3."),
   ("Heitz &mdash; Sampling the GGX Distribution of Visible Normals (2018, "
    "free)",
    "https://jcgt.org/published/0007/04/01/",
    "The algorithm of &sect;2, with the derivation and complete code. Short "
    "paper, large practical payoff."),
   ("Heitz &mdash; Understanding the Masking-Shadowing Function (2014, free)",
    "https://jcgt.org/published/0003/02/03/",
    "Everything about G, including why the height-correlated form is the "
    "right default."),
   ("Kulla & Conty &mdash; Revisiting Physically Based Shading at Imageworks "
    "(free)",
    "https://blog.selfshadow.com/publications/",
    "The energy compensation of &sect;1, from the people who deployed it. "
    "The whole SIGGRAPH shading course archive is free and excellent."),
 ],
 "exercises": [
   "Implement GGX D, the Smith height-correlated G&#8322;, and Schlick's "
   "Fresnel approximation. Verify D integrates correctly over the "
   "hemisphere.",
   "Implement visible-normal sampling and verify it with a &chi;&#178; test. "
   "Deliberately omit the 1/(4|&omega;<sub>o</sub>&middot;h|) Jacobian and "
   "confirm the test catches what the image does not.",
   "Compare visible-normal sampling against sampling D directly. Report the "
   "variance ratio at normal incidence and at 80&deg;.",
   "Run the white furnace test across roughness from 0.05 to 1.0 in steps of "
   "0.05 and plot the result. The departure from 1.0 at high roughness is "
   "the energy loss of &sect;1 — report how much is lost.",
   "Implement Kulla&ndash;Conty energy compensation and repeat the previous "
   "exercise. The curve should flatten to approximately 1.",
   "Test your BSDF for reciprocity over a thousand random direction pairs "
   "and report the maximum relative asymmetry.",
   "Implement a smooth conductor as a delta BSDF. Confirm NEE skips it and "
   "that the resulting mirror has the correct brightness — compare "
   "against an analytic Fresnel calculation.",
   "Implement a rough dielectric with transmission. Render a glass sphere "
   "at roughness 0, 0.1, and 0.3 and verify total internal reflection "
   "appears where expected.",
   "Render a sphere grid: roughness across one axis, metallic across the "
   "other. This is the standard material validation image and belongs in "
   "your portfolio.",
 ],
 "selfcheck": [
   "State the microfacet assumption and explain why roughness is a "
   "distribution rather than a blur.",
   "Write the microfacet BRDF and say what each of D, F, and G contributes "
   "and what fails without it.",
   "Why can only facets whose normal is the half vector contribute?",
   "Why did GGX displace Beckmann, and what is notable about that outcome?",
   "What is the height-correlated Smith function, and why is it preferable "
   "to the separable form?",
   "Why does the single-scattering microfacet model lose energy, and how is "
   "it recovered in practice?",
   "What is visible-normal sampling, and why is it better at grazing "
   "angles?",
   "What is the Jacobian in the BSDF sampling PDF, and what happens if it is "
   "omitted?",
   "Why do specular surfaces need a separate path, and what two integrator "
   "behaviours depend on the flag?",
   "Name the three BSDF tests and say what each one catches.",
 ],
},

]
