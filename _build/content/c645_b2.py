# -*- coding: utf-8 -*-
"""CSCE 645 — Modules 04-08."""

MODULES = [

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "B-Splines and NURBS",
 "subtitle": "Local control, automatic continuity, and exact circles.",
 "question": "How do you build a long smooth curve you can actually edit?",
 "outcomes": [
     "Explain local support and why it is the decisive property.",
     "Read a knot vector and predict the curve's behaviour from it.",
     "Explain how knot multiplicity controls continuity.",
     "Explain what weights add and why NURBS can represent conics exactly.",
     "Choose between Bézier, B-spline, and NURBS for a task.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem with Bézier",
   "blurb": "Degree tied to control count, and every point affects "
            "everything."},

  {"t": "callout", "title": "What B-splines fix", "kind": "The motivation",
   "body": ["<b>Degree is decoupled from control point count.</b> You can "
            "have fifty control points and still a cubic curve.",
            "<b>Local support.</b> Each control point influences only a few "
            "spans. Moving one changes the curve nearby and nowhere else.",
            "<b>Continuity is automatic.</b> A degree-p B-spline is "
            "C^(p−1) at every internal join, by construction — no "
            "constraints to maintain by hand.",
            "The cost is a new object to understand: the <b>knot vector</b>, "
            "which is where all the subtlety lives."]},

  {"t": "eq", "kicker": "Definition", "title": "The same shape, a different basis",
   "eqs": [
     ("C(t)  =  Σᵢ  Nᵢ,ₚ(t) Pᵢ",
      "Still a weighted sum of control points. Only the basis changed."),
     ("Nᵢ,ₚ has support on [uᵢ, uᵢ₊ₚ₊₁]",
      "<b>Local</b>: non-zero over only p+1 knot spans."),
     ("Σᵢ Nᵢ,ₚ(t)  =  1,   Nᵢ,ₚ ≥ 0",
      "Still a convex combination — so the hull property survives."),
   ],
   "caption": "Everything good about Bézier curves is retained because "
              "the basis is still non-negative and sums to one. Only the "
              "support changed.",
   "note": "Framing B-splines as 'Bézier with a better basis' rather "
           "than a new object makes the properties transfer for free."},

  {"t": "section", "label": "Part 2", "title": "Knot vectors",
   "blurb": "The part everyone finds confusing, and the part that does the "
            "work."},

  {"t": "bullets", "kicker": "Knots", "title": "What a knot vector is",
   "items": [
     "A non-decreasing list of parameter values: U = {u₀, u₁, "
     "…, uₘ}.",
     "",
     "It partitions the parameter domain into <b>spans</b>, and says where "
     "one polynomial piece ends and the next begins.",
     "",
     "<b>m = n + p + 1</b> — knots = control points + degree + 1.",
     ("Get this wrong and nothing works. Check it first when debugging.", 1),
     "",
     "<b>Uniform</b> knots — evenly spaced. <b>Clamped</b> — the "
     "first and last repeated p+1 times, so the curve touches its endpoints.",
   ],
   "note": "The m = n + p + 1 relation is the single most useful debugging "
           "check in spline code."},

  {"t": "table", "kicker": "Multiplicity", "title": "Repeating a knot reduces continuity",
   "header": ["Multiplicity k", "Continuity there", "Effect"],
   "widths": [3.0, 3.8, 5.3],
   "rows": [
     ["1", "C^(p−1)", "A normal smooth join"],
     ["2", "C^(p−2)", "Less smooth; curvature may break"],
     ["p", "C⁰", "A visible <b>corner</b>"],
     ["p+1", "Discontinuous", "The curve splits; used at the ends to clamp"],
   ],
   "footnote": "General rule: continuity at a knot is C^(p−k).",
   "note": "This is the elegant bit: one mechanism gives you both smooth "
           "joins and deliberate corners."},

  {"t": "callout", "title": "Multiplicity is how you put a corner in a smooth curve",
   "kind": "The useful consequence",
   "body": ["A designer wants a curve that is smooth everywhere except at one "
            "deliberate sharp point. With Bézier segments you would "
            "break the curve into two objects and manage the join yourself.",
            "With a B-spline you repeat one interior knot p times. The curve "
            "remains a single object with a single control polygon, and it "
            "has a corner exactly there.",
            "Clamping is the same mechanism applied at the ends: repeating "
            "the first and last knots p+1 times makes the curve interpolate "
            "P₀ and Pₙ, recovering Bézier's endpoint "
            "behaviour.",
            "<b>A Bézier curve is a B-spline</b> with no interior knots "
            "and clamped ends. The general object contains the special one."]},

  {"t": "code", "kicker": "Evaluation", "title": "de Boor — de Casteljau's generalisation",
   "lang": "cpp", "code": """
vec3 de_boor(int k, float t, const vector<float>& U,
             vector<vec3> P, int p) {
    // k = the knot span containing t: U[k] <= t < U[k+1]
    // Only p+1 control points matter -- LOCAL SUPPORT in action.
    vector<vec3> d(P.begin() + k - p, P.begin() + k + 1);

    for (int r = 1; r <= p; r++)
        for (int j = p; j >= r; j--) {
            float a = (t - U[j + k - p]) /
                      (U[j + 1 + k - r] - U[j + k - p]);
            d[j] = (1 - a) * d[j - 1] + a * d[j];   // repeated lerp again
        }
    return d[p];
}
""",
   "caption": "Repeated linear interpolation, exactly as in de Casteljau "
              "— but the interpolation parameters come from the knots "
              "rather than being t itself.",
   "note": "Point out that only p+1 control points are touched. That IS local "
           "support, visible in the code."},

  {"t": "section", "label": "Part 3", "title": "NURBS",
   "blurb": "Weights, and the one thing polynomials cannot do."},

  {"t": "eq", "kicker": "NURBS", "title": "Rational: a ratio of polynomials",
   "eqs": [
     ("C(t)  =  Σ wᵢ Nᵢ,ₚ(t) Pᵢ  /  Σ wᵢ Nᵢ,ₚ(t)",
      "Each control point gains a weight wᵢ > 0."),
     ("wᵢ = 1 for all i  ⇒  an ordinary B-spline",
      "The denominator becomes 1. NURBS strictly generalise B-splines."),
     ("wᵢ ↑  ⇒  the curve is pulled toward Pᵢ",
      "A direct, intuitive handle for designers."),
   ],
   "caption": "The division is the whole point: it makes the curve a "
              "<i>rational</i> function, and rational functions can do things "
              "polynomials cannot.",
   "note": "Connect to CSCE 641's homogeneous coordinates — same idea, "
           "same division, same payoff."},

  {"t": "two", "kicker": "Why rational", "title": "The two things weights buy",
   "lh": "Exact conics",
   "l": ["No polynomial curve is exactly a circular arc.",
         "A quadratic NURBS with the right weights <b>is</b>, exactly.",
         ("w = cos(θ/2) at the middle control point.", 1),
         "Which is why CAD is built on NURBS: a cylinder must be a cylinder, "
         "not an approximation."],
   "rh": "Projective invariance",
   "r": ["Affine invariance was Module 03's property.",
         "Rational curves are invariant under <b>perspective</b> too.",
         ("Transform the weighted control points; the projected curve is "
          "exact.", 1),
         "Exactly the homogeneous-coordinate trick from CSCE 641 Module 02."]},

  {"t": "table", "kicker": "Choosing", "title": "Which representation",
   "header": ["Use", "When", "Why"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Bézier", "Short segments, font outlines, animation keys", "Simple; direct endpoint control"],
     ["B-spline", "Long editable curves, camera paths", "Local control; automatic C^(p−1)"],
     ["NURBS", "CAD, exact conics, surfaces of revolution", "Exactness; the industry standard"],
     ["Subdivision", "Organic models, arbitrary topology", "Module 06 — no patch layout needed"],
   ],
   "note": "The honest summary: NURBS dominate engineering, subdivision "
           "dominates entertainment, and the reason is topology."},

  {"t": "callout", "title": "Why games do not use NURBS",
   "kind": "Honest assessment",
   "body": ["NURBS are superb for engineered shapes and poor for organic "
            "ones. A character's head is not naturally a grid of rectangular "
            "patches.",
            "Covering an arbitrary closed surface with NURBS patches requires "
            "<b>trimming</b> and careful cross-patch continuity management, "
            "both of which are difficult and fragile.",
            "Subdivision surfaces (Module 06) handle arbitrary topology "
            "natively with a single control mesh, which is why film and games "
            "went that way while CAD stayed with NURBS.",
            "This is a genuine split by application, not one camp being "
            "behind the other."]},
 ],
 "takeaways": [
   "B-splines decouple degree from control point count, give local support, "
   "and make C^(p−1) continuity automatic.",
   "The basis is still non-negative and sums to one, so the convex hull and "
   "affine invariance properties carry over from Bézier unchanged.",
   "m = n + p + 1. Knots = control points + degree + 1. Check this first when "
   "spline code misbehaves.",
   "Continuity at a knot is C^(p−k) for multiplicity k — one "
   "mechanism gives both smooth joins and deliberate corners.",
   "NURBS add weights, making the curve rational. This buys exact conics and "
   "invariance under perspective.",
   "NURBS dominate CAD; subdivision dominates entertainment. The dividing "
   "line is arbitrary topology.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What B-splines fix"),
  ("p", "Module 03 ended with three objections to high-degree B&eacute;zier "
        "curves: degree tied to control point count, global control, and "
        "oscillation. The proposed remedy was many low-degree segments with "
        "hand-maintained continuity constraints. B-splines are that "
        "construction with the constraints built into the basis."),
  ("table", ["Property", "B&eacute;zier", "B-spline"],
   [["Degree", "Fixed by control point count: n+1 points &rarr; degree n.",
     "Chosen independently. Fifty control points, still cubic."],
    ["Support", "Global — every control point affects every parameter.",
     "<b>Local</b> — each affects p+1 spans only."],
    ["Continuity", "Maintained by hand across joins.",
     "<b>Automatic</b> C<super>p&minus;1</super> at every internal knot."],
    ["Endpoints", "Interpolated.",
     "Interpolated only if the knot vector is clamped."]],
   [0.14, 0.43, 0.43]),
  ("eq", "C(t) = &Sigma;<sub>i</sub> N<sub>i,p</sub>(t) P<sub>i</sub>"),
  ("p", "The form is identical to a B&eacute;zier curve — a weighted sum "
        "of control points. Only the basis functions differ. And critically, "
        "the B-spline basis functions are still non-negative and still sum to "
        "one at every parameter value, so the curve remains a convex "
        "combination of its control points. <b>Every property from Module 03 "
        "that followed from that fact carries over unchanged</b>: the convex "
        "hull property, affine invariance, variation diminishing. Only the "
        "support has become local."),

  ("h1", "2 &nbsp; Knot vectors"),
  ("p", "A B-spline is a piecewise polynomial, and the <b>knot vector</b> "
        "says where the pieces meet."),
  ("eq", "U = {u&#8320;, u&#8321;, &hellip;, u<sub>m</sub>}, &nbsp; non-decreasing, &nbsp; m = n + p + 1"),
  ("callout", "m = n + p + 1",
   ["Number of knots = number of control points + degree + 1.",
    "This relation is the single most useful check when spline code "
    "misbehaves. An off-by-one in knot count produces curves that are "
    "mysteriously truncated, that do not reach their endpoints, or that "
    "evaluate to garbage near the ends.",
    "Assert it on construction."]),
  ("h2", "2.1 &nbsp; Uniform and clamped"),
  ("ul", ["<b>Uniform:</b> knots evenly spaced, for example {0,1,2,3,4,5,6}. "
          "The curve does not reach its first or last control point — it "
          "starts and ends somewhere inside the control polygon, which is "
          "often surprising the first time.",
          "<b>Clamped:</b> the first and last knots repeated p+1 times, for "
          "example {0,0,0,0,1,2,3,3,3,3} for a cubic. The curve now "
          "interpolates P&#8320; and P<sub>n</sub>, recovering B&eacute;zier's "
          "endpoint behaviour. This is what you want almost always."]),
  ("h2", "2.2 &nbsp; Multiplicity and continuity"),
  ("eq", "continuity at a knot of multiplicity k &nbsp;=&nbsp; C<super>p&minus;k</super>"),
  ("table", ["Multiplicity", "Cubic (p = 3)", "Appearance"],
   [["1", "C&#178;", "Smooth, including curvature."],
    ["2", "C&#185;", "Tangent continuous; curvature breaks — visible in "
     "a reflection."],
    ["3", "C&#8304;", "A <b>corner</b>. Position continuous only."],
    ["4", "Discontinuous", "The curve splits into separate pieces. Used at "
     "the ends to clamp."]],
   [0.20, 0.22, 0.58]),
  ("callout", "One mechanism for both smoothness and corners",
   ["A designer wants a curve that is smooth everywhere except at one "
    "deliberate sharp point — a gear tooth, a letterform, a crease in a "
    "surface.",
    "With B&eacute;zier segments this means splitting into separate objects "
    "and managing the join by hand. With a B-spline it means repeating one "
    "interior knot p times: the curve stays a single object with a single "
    "control polygon and has a corner exactly where you asked.",
    "Clamping is the same mechanism at the ends. And a B&eacute;zier curve "
    "<i>is</i> a clamped B-spline with no interior knots — the general "
    "object contains the special one, which is the usual sign that the "
    "generalisation is the right one."]),
  ("h2", "2.3 &nbsp; Evaluation: de Boor"),
  ("code", """vec3 de_boor(int k, float t, const std::vector<float>& U,
             std::vector<vec3> P, int p) {
    // k is the knot span: U[k] <= t < U[k+1].
    // Only control points k-p .. k participate -- local support.
    std::vector<vec3> d(P.begin() + k - p, P.begin() + k + 1);

    for (int r = 1; r <= p; ++r)
        for (int j = p; j >= r; --j) {
            float a = (t - U[j + k - p]) /
                      (U[j + 1 + k - r] - U[j + k - p]);
            d[j] = (1 - a) * d[j - 1] + a * d[j];
        }
    return d[p];
}"""),
  ("p", "This is de Casteljau generalised: repeated linear interpolation, "
        "with the interpolation parameters derived from the knot vector "
        "rather than being t directly. Note that the loop touches only p+1 "
        "control points — local support is not an abstract property but "
        "a visible fact about which array elements are read."),

  ("break",),
  ("h1", "3 &nbsp; NURBS"),
  ("p", "<b>Non-Uniform Rational B-Splines.</b> 'Non-uniform' refers to "
        "arbitrary knot spacing, already covered. 'Rational' is the new "
        "ingredient: each control point gains a positive weight."),
  ("eq", "C(t) = [ &Sigma; w<sub>i</sub> N<sub>i,p</sub>(t) P<sub>i</sub> ] / [ &Sigma; w<sub>i</sub> N<sub>i,p</sub>(t) ]"),
  ("p", "With all weights equal to 1 the denominator is 1 and the curve "
        "reduces to an ordinary B-spline, so NURBS strictly generalise what "
        "came before. Raising a weight pulls the curve toward that control "
        "point, which is an intuitive handle for a designer."),
  ("p", "The division is what matters. It makes the curve a <i>rational</i> "
        "function rather than a polynomial, and rational functions can do two "
        "things polynomials cannot."),
  ("h2", "3.1 &nbsp; Exact conics"),
  ("callout", "No polynomial curve is a circle",
   ["A circular arc is not the image of any polynomial map. B&eacute;zier and "
    "B-spline curves can only approximate one, and the error, while small, is "
    "real and accumulates through boolean operations and offsets.",
    "A quadratic NURBS with weights (1, cos(&theta;/2), 1) on three control "
    "points <b>is</b> a circular arc, exactly. Likewise ellipses, parabolas, "
    "hyperbolas, and by extension cylinders, cones, spheres, and tori.",
    "This is the reason CAD is built on NURBS. A manufactured cylindrical "
    "bore must be a cylinder; an approximation that is correct to six decimal "
    "places is still an approximation, and the errors compound when you "
    "intersect it with something."]),
  ("h2", "3.2 &nbsp; Projective invariance"),
  ("p", "Module 03 noted that B&eacute;zier curves are affine invariant but "
        "not invariant under perspective projection, because perspective "
        "involves a division. Rational curves already involve a division, and "
        "that turns out to be exactly what is needed."),
  ("p", "To transform a NURBS curve by a projective transformation, transform "
        "its control points in homogeneous form (w<sub>i</sub>P<sub>i</sub>, "
        "w<sub>i</sub>) and re-evaluate. The result is exactly the projected "
        "curve. This is the same mechanism as homogeneous coordinates in "
        "CSCE 641 Module 02 — the fourth coordinate and the final "
        "division — and it is the same payoff: a non-linear operation "
        "becomes linear by moving to a higher-dimensional space and dividing "
        "at the end."),

  ("h1", "4 &nbsp; Choosing"),
  ("table", ["Representation", "Use for", "Because"],
   [["<b>B&eacute;zier</b>", "Font outlines, animation keyframes, short "
     "independent segments.",
     "Simple, direct endpoint and tangent control, and ubiquitous in file "
     "formats."],
    ["<b>B-spline</b>", "Long editable curves, camera paths, profiles.",
     "Local control makes editing practical; continuity is automatic."],
    ["<b>NURBS</b>", "CAD, surfaces of revolution, anything with exact "
     "circular or conic features.",
     "Exactness, projective invariance, and universal support in engineering "
     "software."],
    ["<b>Subdivision</b>", "Characters, organic models, anything with "
     "arbitrary topology.",
     "No patch layout or trimming required. Module 06."]],
   [0.17, 0.38, 0.45]),
  ("callout", "Why entertainment went one way and engineering the other",
   ["NURBS are excellent for shapes that decompose naturally into rectangular "
    "patches — which engineered parts largely do.",
    "A character's head does not. Covering an arbitrary closed surface with "
    "NURBS patches requires trimming curves and careful management of "
    "continuity across patch boundaries, both of which are difficult, "
    "fragile, and tedious to author.",
    "Subdivision surfaces handle arbitrary topology with a single control "
    "mesh and no boundaries to manage, which is why Pixar adopted them in the "
    "1990s and why every character pipeline since uses them.",
    "This is a genuine split by application rather than one community being "
    "behind the other. CAD's requirement for exactness is real, and "
    "subdivision does not provide it."]),
 ],
 "resources": [
   ("A Primer on Bézier Curves — B-spline sections (free, "
    "interactive)",
    "https://pomax.github.io/bezierinfo/",
    "Knot vectors explained interactively, which is the only way they ever "
    "make sense the first time."),
   ("The NURBS Book — Piegl & Tiller (reference)",
    "https://link.springer.com/book/10.1007/978-3-642-59223-2",
    "The standard reference. Check your library; the algorithms chapter is "
    "the one to consult when implementing de Boor and knot insertion."),
   ("Freya Holmér — The Continuity of Splines (free video)",
    "https://www.youtube.com/watch?v=jvPPXbo87ds",
    "An exceptionally clear visual treatment of continuity, knot "
    "multiplicity, and the spline families compared."),
   ("OpenNURBS / Rhino developer documentation",
    "https://developer.rhino3d.com/",
    "How NURBS are represented in a real CAD kernel, including trimming."),
 ],
 "exercises": [
   "Implement B-spline evaluation with de Boor's algorithm. Verify that a "
   "clamped cubic with no interior knots reproduces a B&eacute;zier curve "
   "exactly.",
   "Implement a knot vector validator that checks m = n + p + 1, "
   "non-decreasing order, and clamping. Deliberately break each condition and "
   "observe the failure mode.",
   "Demonstrate local support: move one control point of a 20-point cubic "
   "B-spline and plot which parameter range changed. Confirm it spans exactly "
   "p+1 knot spans.",
   "Vary the multiplicity of one interior knot from 1 to p and render each "
   "result. Capture the point at which a visible corner appears.",
   "Implement NURBS evaluation. Construct an exact quarter circle with "
   "weights (1, cos 45&deg;, 1) and verify that sampled points lie on the "
   "circle to machine precision. Compare against a cubic B&eacute;zier "
   "approximation and report the maximum error.",
   "Verify projective invariance: apply a perspective matrix to homogeneous "
   "control points and compare against projecting evaluated points. Then "
   "repeat with a non-rational B-spline and show it fails.",
   "Implement knot insertion and verify it changes the control polygon "
   "without changing the curve.",
 ],
 "selfcheck": [
   "Name the three things B-splines fix relative to B&eacute;zier curves.",
   "Why do the convex hull and affine invariance properties carry over "
   "unchanged?",
   "State the relation between knot count, control point count, and degree, "
   "and say why it is worth asserting.",
   "What is the continuity at a knot of multiplicity k, and how do you put a "
   "deliberate corner in a smooth B-spline?",
   "What does 'rational' add, and what two things does it buy?",
   "Why can no polynomial curve be exactly a circle, and why does that matter "
   "for CAD?",
   "Why do character pipelines use subdivision rather than NURBS?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Surfaces: Tensor Products and Patches",
 "subtitle": "Curves in two directions, and where the construction runs out.",
 "question": "How do you extend a curve scheme to a surface?",
 "outcomes": [
     "Construct tensor-product Bézier and B-spline surfaces.",
     "Evaluate a patch and compute its normals and derivatives.",
     "Explain why tensor products force quadrilateral topology.",
     "Explain trimming and why it is necessary and awkward.",
     "Explain cross-patch continuity and why it is hard.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The construction",
   "blurb": "Take a curve scheme and apply it twice."},

  {"t": "eq", "kicker": "Tensor product", "title": "Curves in two parameters",
   "eqs": [
     ("S(u,v)  =  Σᵢ Σⱼ  Bᵢ(u) Bⱼ(v) Pᵢⱼ",
      "A grid of control points, with the curve basis applied in each "
      "direction."),
     ("S(u,v)  =  Σᵢ Bᵢ(u) · [ Σⱼ Bⱼ(v) Pᵢⱼ ]",
      "Evaluate as curves in v, then one curve through the results."),
     ("bicubic:  4×4 = 16 control points",
      "The standard patch. Enough for C² joins in both directions."),
   ],
   "caption": "Evaluation is just the curve algorithm applied twice, which "
              "means de Casteljau and de Boor transfer directly.",
   "note": "The nested evaluation is how you actually implement it, and it "
           "makes the cost obvious: (p+1) curve evaluations plus one more."},

  {"t": "code", "kicker": "Evaluation", "title": "Nested de Casteljau",
   "lang": "cpp", "code": """
vec3 eval_patch(const vec3 P[4][4], float u, float v) {
    vec3 row[4];
    for (int i = 0; i < 4; i++)
        row[i] = de_casteljau({P[i][0], P[i][1], P[i][2], P[i][3]}, v);
    return de_casteljau({row[0], row[1], row[2], row[3]}, u);
}

// Partial derivatives for the normal: differentiate one direction,
// evaluate the other.
vec3 n = normalize(cross(dSdu(P,u,v), dSdv(P,u,v)));
// -> ANALYTIC normals, exact at every point. Meshes cannot do this.
""",
   "caption": "Exact analytic normals are a real advantage of parametric "
              "surfaces — no averaging, no tessellation dependence.",
   "note": "Tie back to Module 02's normal-weighting discussion: that whole "
           "problem does not exist here."},

  {"t": "section", "label": "Part 2", "title": "The limitation",
   "blurb": "A grid of control points implies a grid of topology."},

  {"t": "callout", "title": "Tensor products force quad topology",
   "kind": "The structural problem",
   "body": ["The construction needs a <b>rectangular grid</b> of control "
            "points. That is what 'tensor product' means.",
            "So a single patch is topologically a square. Any surface built "
            "from them is a quad mesh of patches.",
            "A sphere needs at least two patches and has degenerate poles. A "
            "torus works. A character's head, with its natural five- and "
            "three-valence vertices, does not fit at all.",
            "Every difficulty in the rest of this module descends from this "
            "one fact."]},

  {"t": "bullets", "kicker": "Trimming", "title": "Holes, and the price of them",
   "items": [
     "Want a hole in a patch? You cannot remove control points — the "
     "grid must stay rectangular.",
     "",
     "<b>Trimming:</b> keep the patch, and carry curves in parameter space "
     "marking which regions are valid.",
     "",
     "Now every operation must respect the trim curves:",
     ("Tessellation must triangulate a region bounded by curves, not a "
      "rectangle.", 1),
     ("Two trimmed patches meeting at an edge rarely match exactly — "
      "hence <b>gaps</b>.", 1),
     "",
     "Trimming is where CAD kernels spend much of their complexity and most "
     "of their bugs.",
   ],
   "note": "The gap problem is why CAD-to-mesh export is notoriously "
           "unreliable. Worth saying plainly."},

  {"t": "section", "label": "Part 3", "title": "Cross-patch continuity",
   "blurb": "Making two patches meet smoothly is harder than it looks."},

  {"t": "table", "kicker": "Continuity", "title": "Conditions across a patch boundary",
   "header": ["Want", "Requires", "Difficulty"],
   "widths": [2.4, 5.4, 4.3],
   "rows": [
     ["C⁰", "Shared boundary control points", "Easy"],
     ["G¹", "Boundary tangent planes agree along the whole edge", "Doable"],
     ["G²", "Curvature agrees along the whole edge", "Hard"],
     ["At a corner", "All meeting patches agree — the <b>vertex enclosure problem</b>", "Often impossible"],
   ],
   "note": "The corner case is the killer. For odd numbers of patches meeting "
           "at a point, G1 can be unachievable with the obvious construction."},

  {"t": "callout", "title": "The vertex enclosure problem",
   "kind": "Why this approach runs out",
   "body": ["Making two patches meet smoothly along an edge is manageable. "
            "Making n patches meet smoothly <i>at a corner</i> is a different "
            "matter.",
            "The tangent plane conditions along each of the n shared edges "
            "must all be mutually consistent at the shared vertex. For "
            "certain valences — particularly odd ones — the "
            "resulting system has no solution with the obvious patch degree.",
            "Workarounds exist: raise the degree, split patches, or accept "
            "approximate continuity. All add complexity, and all are why "
            "patch-based modelling of organic shapes is painful.",
            "<b>Subdivision surfaces (Module 06) sidestep this entirely</b> "
            "by never forming explicit patches. That is their central "
            "advantage."]},

  {"t": "bullets", "kicker": "Where patches work", "title": "An honest assessment",
   "items": [
     "<b>Work well:</b> engineered parts, surfaces of revolution, extrusions, "
     "lofts, anything naturally rectangular.",
     "<b>Work well:</b> exact representation and manufacturing tolerance "
     "— NURBS is the only serious option.",
     "",
     "<b>Work badly:</b> arbitrary topology, organic shapes, anything with "
     "irregular vertices.",
     "<b>Work badly:</b> local refinement — adding detail means "
     "inserting an entire row or column.",
     "",
     "That last point matters: T-splines and hierarchical B-splines exist "
     "specifically to allow local refinement.",
   ]},

  {"t": "code", "kicker": "Practice", "title": "Tessellating a patch for rendering",
   "lang": "cpp", "code": """
// Uniform: simple, and wastes triangles on flat regions.
for (i = 0; i <= N; i++)
  for (j = 0; j <= N; j++)
    vertex[i][j] = eval_patch(P, i/(float)N, j/(float)N);

// Adaptive: subdivide where curvature is high, as in Module 03.
// Screen-space error is the right criterion -- a patch covering
// 10 pixels needs no more than 10 pixels' worth of triangles.

// Hardware tessellation (CSCE 641 Module 12) evaluates patches
// on the GPU: the control cage is the vertex buffer, and the
// tessellation evaluation shader computes S(u,v).
""",
   "caption": "This is the direct connection to CSCE 641: GPU tessellation "
              "exists to evaluate exactly these surfaces at render time.",
   "note": "Closing the loop with 641's tessellation module makes both land "
           "better."},
 ],
 "takeaways": [
   "A tensor-product surface applies a curve basis in each parameter "
   "direction, over a rectangular grid of control points.",
   "Evaluation is the curve algorithm nested: evaluate rows, then evaluate "
   "across the results.",
   "Parametric surfaces give exact analytic normals, which meshes cannot — "
   "no averaging and no tessellation dependence.",
   "The construction forces quadrilateral topology. Every later difficulty "
   "descends from that.",
   "Trimming adds holes by marking invalid regions in parameter space, and is "
   "where CAD kernels keep most of their complexity and their gaps.",
   "The vertex enclosure problem makes smooth corners between many patches "
   "hard or impossible — which is what subdivision surfaces avoid.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The tensor product construction"),
  ("p", "Given a curve scheme with basis functions B<sub>i</sub>, the surface "
        "version applies it in two parameters over a rectangular grid of "
        "control points."),
  ("eq", "S(u,v) = &Sigma;<sub>i</sub> &Sigma;<sub>j</sub> B<sub>i</sub>(u) B<sub>j</sub>(v) P<sub>ij</sub>"),
  ("p", "The name is apt: the basis is the tensor product of the two "
        "one-dimensional bases. Every property carries over directionally "
        "— the surface lies in the convex hull of its control grid, is "
        "affine invariant, and interpolates its corner control points when "
        "clamped."),
  ("p", "The evaluation strategy follows from the factorisation:"),
  ("eq", "S(u,v) = &Sigma;<sub>i</sub> B<sub>i</sub>(u) &middot; [ &Sigma;<sub>j</sub> B<sub>j</sub>(v) P<sub>ij</sub> ]"),
  ("code", """vec3 eval_patch(const vec3 P[4][4], float u, float v) {
    vec3 row[4];
    for (int i = 0; i < 4; ++i)                  // evaluate each row in v
        row[i] = de_casteljau({P[i][0], P[i][1],
                               P[i][2], P[i][3]}, v);
    return de_casteljau({row[0], row[1],         // then across in u
                         row[2], row[3]}, u);
}"""),
  ("p", "A bicubic patch — 4&times;4 control points, degree 3 in each "
        "direction — is the standard unit, for the same reason cubics "
        "dominate curves: enough freedom for C&#178; joins, little enough to "
        "stay numerically well behaved."),
  ("h2", "1.1 &nbsp; Derivatives and exact normals"),
  ("p", "Partial derivatives come from differentiating the basis in one "
        "direction while evaluating normally in the other. The surface normal "
        "is then the normalised cross product:"),
  ("eq", "n(u,v) = normalize( &part;S/&part;u &times; &part;S/&part;v )"),
  ("callout", "This is genuinely better than a mesh normal",
   ["Module 02 spent a page on how to <i>weight</i> the average of face "
    "normals, because a mesh has no normal — only an approximation whose "
    "quality depends on tessellation.",
    "A parametric surface has an exact normal at every point, computed "
    "analytically. It does not depend on how finely you tessellate and does "
    "not change when you refine.",
    "This matters for manufacturing (tool paths need exact surface normals), "
    "for exact offsetting, and for high-quality rendering of smooth surfaces. "
    "It is one of the real advantages that keeps NURBS in engineering use."]),

  ("h1", "2 &nbsp; The structural limitation"),
  ("callout", "A rectangular grid of control points means rectangular topology",
   ["The tensor product construction requires control points indexed by (i, "
    "j) over a rectangle. There is no way to have a control point with five "
    "neighbours.",
    "So a single patch is topologically a square, and any surface assembled "
    "from patches is a quadrilateral mesh of them.",
    "A cylinder is fine. A torus is fine. A sphere needs at least two patches "
    "and has degenerate poles where the parameterisation collapses. A "
    "character's head — which naturally wants vertices of valence 3 and "
    "5 around the eyes, nose, and ears — does not fit the model at all.",
    "Every remaining difficulty in this module is a consequence of this one "
    "constraint."]),
  ("h2", "2.1 &nbsp; Trimming"),
  ("p", "Suppose you want a hole in a surface — a bolt hole in a plate. "
        "You cannot simply remove control points, because the grid must "
        "remain rectangular."),
  ("p", "The solution is <b>trimming</b>: retain the full rectangular patch "
        "and carry a set of curves in its parameter domain marking which "
        "regions are valid. The surface is the patch restricted to the "
        "untrimmed region."),
  ("p", "This works, and it propagates complexity into everything downstream:"),
  ("ul", ["<b>Tessellation</b> must triangulate a region bounded by arbitrary "
          "curves rather than a rectangle — a constrained triangulation "
          "problem rather than a grid.",
          "<b>Adjacency</b> between patches is no longer structural. Two "
          "trimmed patches meant to meet along a curve have independently "
          "computed trim curves that agree only to within a tolerance.",
          "<b>Gaps.</b> Those tolerance mismatches become visible holes when "
          "the model is tessellated for rendering or manufacturing."]),
  ("callout", "Why CAD-to-mesh export is notoriously unreliable",
   ["Anyone who has exported a CAD model for rendering or 3D printing has "
    "encountered meshes with gaps along patch boundaries, flipped normals, "
    "and non-manifold edges.",
    "The cause is usually trimming: the trim curves of adjacent patches do "
    "not agree exactly, so tessellating each independently produces edges "
    "that do not match. Healing these gaps is an entire category of "
    "commercial software.",
    "Keep this in mind in Project 2 — if your input is CAD-derived, "
    "expect the repair steps of Module 02 to earn their keep."]),

  ("break",),
  ("h1", "3 &nbsp; Cross-patch continuity"),
  ("p", "A single patch is smooth internally by construction. Making two "
        "patches meet smoothly requires explicit conditions, and the "
        "difficulty rises sharply with what you ask for."),
  ("table", ["Continuity", "Condition", "Difficulty"],
   [["<b>C&#8304;</b>", "The patches share their boundary control points.",
     "Trivial — just use the same points."],
    ["<b>G&#185;</b>", "The tangent planes agree along the entire shared "
     "edge, which constrains the row of control points adjacent to the "
     "boundary on both sides.",
     "Manageable for two patches meeting along an edge."],
    ["<b>G&#178;</b>", "Curvature agrees along the whole edge, constraining "
     "two rows on each side.",
     "Hard. Uses up most of the available freedom, and required for "
     "reflective surfaces."],
    ["<b>At a corner</b>", "All n patches meeting at a vertex must satisfy "
     "every edge condition simultaneously and consistently.",
     "<b>Often impossible</b> at the natural degree. See below."]],
   [0.14, 0.48, 0.38]),
  ("callout", "The vertex enclosure problem",
   ["When n patches meet at a single corner, the G&#185; conditions along the "
    "n shared edges are not independent: they must be mutually consistent at "
    "the shared vertex.",
    "For certain valences — odd numbers in particular — the "
    "resulting constraint system has no solution using patches of the natural "
    "degree. The surface simply cannot be made smooth there without changing "
    "something structural.",
    "Workarounds all cost something: raise the patch degree, split patches "
    "into more pieces, introduce small filling patches, or accept "
    "approximately-G&#185; continuity and hope it is below the visible "
    "threshold.",
    "This is the single strongest argument against patch-based modelling of "
    "organic shapes, and it is precisely what subdivision surfaces avoid "
    "— they never form explicit patches, so there is no boundary at "
    "which to impose conditions. Module 06."]),

  ("h1", "4 &nbsp; Where patches are the right tool"),
  ("table", ["Suits patches", "Does not"],
   [["Engineered parts: extrusions, lofts, surfaces of revolution, fillets.",
     "Organic shapes with irregular vertices — characters, creatures, "
     "scanned anatomy."],
    ["Anything requiring <b>exactness</b>: manufacturing tolerances, exact "
     "conics, offsets.",
     "Anything requiring arbitrary topology without a careful hand-built "
     "patch layout."],
    ["Analytic normals and derivatives for tool paths and simulation.",
     "Local refinement — adding detail requires inserting an entire row "
     "or column across the patch."],
    ["Interchange with manufacturing and engineering software, where NURBS is "
     "the lingua franca.",
     "Rapid iteration — maintaining cross-patch continuity by hand is "
     "slow."]],
   [0.5, 0.5]),
  ("p", "The local refinement limitation is worth noting: inserting a knot in "
        "a tensor-product surface inserts an entire row or column of control "
        "points, including in regions that needed no extra detail. "
        "<b>T-splines</b> and <b>hierarchical B-splines</b> were developed "
        "specifically to allow genuinely local refinement, and they are now "
        "standard in high-end CAD."),

  ("h1", "5 &nbsp; Tessellation and the connection to rendering"),
  ("code", """// Uniform tessellation: simple, wasteful on flat regions.
for (int i = 0; i <= N; ++i)
  for (int j = 0; j <= N; ++j)
    V[i][j] = eval_patch(P, i / float(N), j / float(N));"""),
  ("p", "Adaptive tessellation uses the same principle as Module 03: "
        "subdivide where the surface deviates from flat by more than a "
        "tolerance. For rendering, the right criterion is <b>screen-space</b> "
        "error — a patch covering ten pixels needs no more than ten "
        "pixels' worth of triangles, and CSCE 614 Module 10's warning about "
        "sub-pixel triangles applies directly."),
  ("callout", "This is what GPU tessellation is for",
   ["CSCE 641 Module 12 introduced the tessellation control, tessellator, and "
    "tessellation evaluation stages. The evaluation shader's job is exactly "
    "the computation in this module: given a patch's control points and a "
    "generated (u, v), compute S(u, v).",
    "So the control cage becomes the vertex buffer, the tessellation factors "
    "come from a screen-space error estimate computed in the control shader, "
    "and the surface is evaluated fresh every frame at whatever resolution "
    "the current view requires.",
    "That is the clean version of level of detail: one representation, "
    "resolution chosen at draw time, no LOD chain to author or to pop between."]),
 ],
 "resources": [
   ("The NURBS Book — surfaces chapters",
    "https://link.springer.com/book/10.1007/978-3-642-59223-2",
    "Tensor-product surfaces, trimming, and the continuity conditions, done "
    "rigorously."),
   ("Keenan Crane — DDG, surface representation material",
    "https://brickisland.net/ddg-web/",
    "The topological argument for why patches struggle with arbitrary "
    "surfaces."),
   ("OpenNURBS developer documentation — trimmed surfaces",
    "https://developer.rhino3d.com/",
    "How a production kernel actually represents trims and why export is "
    "difficult."),
   ("Cem Yuksel — Interactive Computer Graphics, tessellation lectures",
    "https://graphics.cs.utah.edu/courses/cs6610/",
    "GPU tessellation of parametric patches, connecting this module to "
    "CSCE 641."),
 ],
 "exercises": [
   "Implement bicubic B&eacute;zier patch evaluation with nested de "
   "Casteljau. Render the Utah teapot from its original 32-patch control "
   "data.",
   "Implement analytic partial derivatives and exact normals. Compare the "
   "shading against normals computed by averaging from a tessellated mesh, at "
   "coarse and fine tessellation.",
   "Join two bicubic patches with C&#8304; continuity, then with G&#185;. "
   "Render both with an environment map and capture the difference at the "
   "seam.",
   "Attempt a G&#185; join of three patches at a shared corner and document "
   "where the constraint system becomes over-determined.",
   "Implement uniform and adaptive patch tessellation. Compare triangle "
   "counts at matched visual quality for a curved patch and a nearly flat "
   "one.",
   "Implement a simple trimmed patch: a bicubic with a circular hole defined "
   "by a trim curve in parameter space. Triangulate the valid region and "
   "render it.",
   "Tessellate two adjacent trimmed patches independently and measure the gap "
   "between their boundaries. Explain where it comes from.",
 ],
 "selfcheck": [
   "Write the tensor-product surface formula and describe how evaluation "
   "factorises.",
   "Why can a parametric surface give exact normals when a mesh cannot?",
   "What topology does the tensor-product construction force, and name three "
   "consequences.",
   "What is trimming, why is it necessary, and what does it make difficult?",
   "State the vertex enclosure problem and say why it motivates subdivision "
   "surfaces.",
   "Why is local refinement awkward for tensor-product surfaces, and what "
   "addresses it?",
   "How does GPU tessellation relate to the content of this module?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Subdivision Surfaces",
 "subtitle": "Smoothness by refinement, with no patches to join.",
 "question": "How do you get a smooth surface on arbitrary topology?",
 "outcomes": [
     "Implement Catmull–Clark and Loop subdivision.",
     "Explain the relationship between subdivision and spline surfaces.",
     "Explain extraordinary vertices and what happens there.",
     "Implement creases and semi-sharp features.",
     "Explain adaptive and feature-adaptive subdivision.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The idea",
   "blurb": "Define the surface as the limit of refining a coarse mesh."},

  {"t": "bullets", "kicker": "Subdivision", "title": "Refinement as a definition",
   "items": [
     "Start with a coarse <b>control cage</b> — an ordinary mesh, any "
     "topology.",
     "Apply a fixed refinement rule: insert vertices, reposition existing "
     "ones.",
     "Repeat.",
     "",
     "In the limit, a smooth surface. In practice, two or three steps are "
     "visually indistinguishable from it.",
     "",
     "<b>No patches, no boundaries, no continuity conditions to impose.</b>",
     ("Which is exactly what Module 05 could not deliver.", 1),
   ],
   "note": "Lead with the problem it solves. Subdivision looks arbitrary "
           "until you have felt the vertex enclosure problem."},

  {"t": "table", "kicker": "Schemes", "title": "The two that matter",
   "header": ["Scheme", "Base mesh", "Limit continuity", "Used by"],
   "widths": [2.8, 2.8, 3.4, 3.1],
   "rows": [
     ["Catmull–Clark", "Quads (any polygons)", "C², C¹ at extraordinary", "Film, games"],
     ["Loop", "Triangles", "C², C¹ at extraordinary", "Triangle pipelines"],
     ["Doo–Sabin", "Any", "C¹", "Rare"],
     ["√3", "Triangles", "C²", "Slower refinement ratio"],
   ],
   "note": "Catmull-Clark dominates because artists model in quads and "
           "because Pixar standardised on it."},

  {"t": "code", "kicker": "Catmull-Clark", "title": "The three rules",
   "lang": "text", "code": """
For each FACE:   face point F = average of the face's vertices.

For each EDGE:   edge point E = average of the edge's two endpoints
                 and the two adjacent face points.

For each VERTEX: move it to
                     (F_avg + 2*R_avg + (n-3)*P) / n
                 where  F_avg = average of adjacent face points
                        R_avg = average of adjacent edge MIDPOINTS
                        n     = vertex valence

Then connect: each face point to its edge points, producing
quads everywhere -- even from triangles or pentagons.
""",
   "caption": "After one step the mesh is all quads. After two, all vertices "
              "except the original extraordinary ones have valence 4.",
   "note": "The all-quads-after-one-step property is why the scheme handles "
           "arbitrary input polygons gracefully."},

  {"t": "section", "label": "Part 2", "title": "Why it works",
   "blurb": "Subdivision is not an alternative to splines. It is a "
            "generalisation."},

  {"t": "callout", "title": "Catmull–Clark on a regular quad mesh IS a B-spline",
   "kind": "The key fact",
   "body": ["Apply Catmull–Clark to a mesh where every vertex has "
            "valence 4, and the limit surface is exactly a uniform bicubic "
            "B-spline surface — the Module 05 object.",
            "So subdivision did not replace spline surfaces. It <b>extended "
            "them to arbitrary topology</b>, by giving a refinement procedure "
            "that agrees with the spline wherever the spline is defined and "
            "still does something sensible elsewhere.",
            "The special behaviour at <b>extraordinary vertices</b> — "
            "valence ≠ 4 — is precisely the price of that "
            "generality. There the surface is only C¹, not C².",
            "This is why modellers are taught to keep quad topology regular "
            "where curvature matters, and to place poles where nobody looks."]},

  {"t": "bullets", "kicker": "Extraordinary", "title": "What happens at a pole",
   "items": [
     "An <b>extraordinary vertex</b> has valence ≠ 4 (quads) or "
     "≠ 6 (triangles).",
     "",
     "Their number is fixed by topology and by the base mesh — "
     "subdivision never creates new ones.",
     ("After one step, all new vertices are regular. The irregularity stays "
      "put and becomes locally isolated.", 1),
     "",
     "At an extraordinary vertex the limit surface is C¹ but not "
     "C².",
     ("Curvature is continuous <i>nowhere near</i> there, and reflections "
      "show it.", 1),
     "",
     "Practical rule: keep poles off smooth reflective regions.",
   ],
   "note": "The 'irregularity stays put and gets isolated' point explains why "
           "two subdivision levels is usually enough."},

  {"t": "section", "label": "Part 3", "title": "Creases and control",
   "blurb": "Making a smooth scheme produce sharp features deliberately."},

  {"t": "bullets", "kicker": "Creases", "title": "Sharp edges in a smooth surface",
   "items": [
     "Default subdivision smooths everything. Real objects have sharp edges.",
     "",
     "<b>Sharp crease:</b> tag an edge; use <i>curve</i> subdivision rules "
     "along it instead of surface rules.",
     ("The limit surface has a genuine crease there.", 1),
     "",
     "<b>Semi-sharp crease:</b> a sharpness value s. Apply crease rules for "
     "the first s levels, then smooth rules.",
     ("Produces a rounded-but-tight edge — which is what real "
      "manufactured objects have.", 1),
     "",
     "Pixar introduced semi-sharp creases for exactly this reason, and every "
     "modern implementation has them.",
   ],
   "footnote": "Fractional sharpness interpolates, so an artist can dial an "
               "edge from soft to knife-sharp continuously."},

  {"t": "callout", "title": "Why semi-sharp creases matter",
   "kind": "Practical",
   "body": ["A perfectly sharp edge looks computer-generated, because real "
            "manufactured edges have a small fillet from tooling and wear.",
            "Modelling that fillet as geometry costs edge loops everywhere "
            "and makes the cage hard to edit.",
            "A semi-sharp crease gives the same visual result from a single "
            "number per edge, with no extra control geometry — and "
            "because it is a property of the cage, it scales with "
            "subdivision level automatically.",
            "This is the feature that made subdivision practical for hard-"
            "surface modelling rather than only organic shapes."]},

  {"t": "section", "label": "Part 4", "title": "In practice",
   "blurb": "How subdivision is actually evaluated today."},

  {"t": "bullets", "kicker": "Evaluation", "title": "Three ways to get a surface",
   "items": [
     "<b>Iterative refinement.</b> Apply the rules k times, render the "
     "result. Simple; 4ᵏ growth in face count.",
     "",
     "<b>Exact evaluation.</b> Stam's method evaluates the limit surface "
     "directly at any (u,v), including near extraordinary vertices, using "
     "eigenstructure of the subdivision matrix.",
     "",
     "<b>Feature-adaptive subdivision.</b> Refine only near extraordinary "
     "vertices and creases; everywhere else the surface is already a bicubic "
     "patch, so evaluate it directly on the GPU.",
     ("This is what OpenSubdiv does, and it is how film-quality subdivision "
      "runs in real time.", 1),
   ],
   "note": "Feature-adaptive is the practically important one and the "
           "cleanest payoff of the 'regular regions are B-splines' fact."},

  {"t": "table", "kicker": "Comparison", "title": "Subdivision against the alternatives",
   "header": ["", "NURBS patches", "Subdivision", "Plain mesh"],
   "widths": [3.0, 3.1, 3.0, 3.0],
   "rows": [
     ["Arbitrary topology", "Hard", "<b>Free</b>", "<b>Free</b>"],
     ["Smoothness", "<b>Exact</b>", "C² (C¹ at poles)", "None"],
     ["Local editing", "Patch-wide", "<b>Local</b>", "<b>Local</b>"],
     ["LOD", "Tessellate", "<b>Built in</b>", "Author a chain"],
     ["Exactness for CAD", "<b>Yes</b>", "No", "No"],
   ],
   "note": "Subdivision wins everywhere except exactness, which is exactly "
           "the column CAD cannot give up."},
 ],
 "takeaways": [
   "Subdivision defines a surface as the limit of refining a coarse cage, "
   "with no patches and therefore no continuity conditions to impose.",
   "Catmull–Clark on a regular quad mesh is exactly a bicubic B-spline "
   "surface — subdivision generalises splines rather than replacing "
   "them.",
   "Extraordinary vertices are where the surface drops to C¹. Their "
   "number is fixed by the base mesh and never grows.",
   "After one subdivision step everything is quads and all new vertices are "
   "regular, so irregularity becomes isolated.",
   "Semi-sharp creases give tight-but-rounded edges from one number per edge, "
   "which is what made subdivision viable for hard-surface work.",
   "Feature-adaptive subdivision refines only near poles and creases, "
   "evaluating the regular majority directly as B-spline patches on the GPU.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Refinement as a definition"),
  ("p", "Module 05 ended at an impasse: tensor-product patches cannot cover "
        "arbitrary topology smoothly, and the vertex enclosure problem means "
        "the difficulty is structural rather than a matter of effort."),
  ("p", "Subdivision takes a different approach. Rather than defining the "
        "surface by a formula, define it as the <b>limit</b> of repeatedly "
        "refining a coarse control mesh by a fixed local rule. There are no "
        "patches, hence no patch boundaries, hence no continuity conditions "
        "to impose — the smoothness is a property of the limit process "
        "itself."),
  ("table", ["Scheme", "Base mesh", "Limit surface", "Notes"],
   [["<b>Catmull&ndash;Clark</b>", "Quads; handles any polygons",
     "C&#178; everywhere except at extraordinary vertices, where C&#185;",
     "The dominant scheme. Film and games standard."],
    ["<b>Loop</b>", "Triangles",
     "C&#178; except C&#185; at extraordinary vertices",
     "Natural for triangle-based pipelines."],
    ["<b>Doo&ndash;Sabin</b>", "Any polygons", "C&#185;",
     "Historically important, rarely used now."],
    ["<b>&radic;3</b>", "Triangles", "C&#178;",
     "Slower refinement ratio, so finer control over level of detail."]],
   [0.20, 0.20, 0.33, 0.27]),
  ("h2", "1.1 &nbsp; Catmull&ndash;Clark"),
  ("code", """FACE POINT    for each face: average of its vertices.

EDGE POINT    for each edge: average of its two endpoints and the
              two adjacent face points.

VERTEX POINT  for each original vertex of valence n, move it to
                  (F + 2R + (n-3)P) / n
              where F = average of adjacent face points,
                    R = average of adjacent edge midpoints,
                    P = the original position.

CONNECT       join each face point to the edge points of its face."""),
  ("p", "Two structural facts fall out immediately. First, <b>after one step "
        "every face is a quadrilateral</b>, regardless of the input — a "
        "pentagon becomes five quads. Second, every newly created vertex has "
        "valence 4 (new face points) or valence 4 (new edge points on a quad "
        "mesh), so <b>all irregularity remains at the original "
        "vertices</b>."),

  ("h1", "2 &nbsp; Why it works"),
  ("callout", "Catmull&ndash;Clark on a regular quad mesh is a bicubic B-spline",
   ["Take a mesh in which every vertex has valence 4. Apply Catmull&ndash;"
    "Clark. The limit surface is <i>exactly</i> the uniform bicubic B-spline "
    "surface over that control grid — the object from Module 05.",
    "This is not an approximation or an analogy. The subdivision rules were "
    "derived from the B-spline refinement relations, which is why they look "
    "arbitrary until you know where they came from.",
    "So subdivision is not a competitor to spline surfaces. It is their "
    "<b>extension to arbitrary topology</b>: a procedure that agrees exactly "
    "with the spline wherever a spline could be defined, and continues to "
    "produce a sensible smooth surface where one could not.",
    "The special behaviour at extraordinary vertices is precisely the price "
    "of that extension, and it is a small price."]),
  ("h2", "2.1 &nbsp; Extraordinary vertices"),
  ("p", "A vertex is <b>extraordinary</b> (or irregular, or a pole) if its "
        "valence differs from the regular value: 4 for quad schemes, 6 for "
        "triangle schemes. Module 01's Euler argument showed these cannot "
        "always be avoided — a closed surface of genus 0 cannot be made "
        "entirely of valence-4 quads."),
  ("ul", ["Their number and location are fixed by the base mesh. Subdivision "
          "never creates new extraordinary vertices.",
          "After one subdivision step, every extraordinary vertex is "
          "surrounded by regular vertices, so the irregularity becomes "
          "<b>isolated</b> — which is what makes feature-adaptive "
          "evaluation (&sect;4) possible.",
          "At an extraordinary vertex the limit surface is C&#185; but not "
          "C&#178;. Position and tangent plane are continuous; curvature is "
          "not."]),
  ("callout", "What a C&#185; point looks like",
   ["A curvature discontinuity is invisible in silhouette and clearly visible "
    "in a reflection — exactly as Module 03 described for curves.",
    "On a car body or any polished surface, an extraordinary vertex in the "
    "middle of a smooth panel shows as a subtle distortion in the reflected "
    "environment. This is why modelling guidelines insist on keeping quad "
    "topology regular across large smooth areas and placing poles where they "
    "will not be seen — inside an ear, under an arm, at a hard material "
    "boundary.",
    "It is also why zebra-stripe analysis exists in modelling packages: it "
    "makes curvature discontinuities visible before rendering."]),

  ("break",),
  ("h1", "3 &nbsp; Creases"),
  ("p", "Subdivision smooths everything by default, and real objects have "
        "sharp features. Two mechanisms address this."),
  ("h2", "3.1 &nbsp; Sharp creases"),
  ("p", "Tag an edge as a crease. Along tagged edges, apply <i>curve</i> "
        "subdivision rules — treating the crease as a B-spline curve "
        "— rather than surface rules. The limit surface then has a "
        "genuine tangent discontinuity there. Tagging a vertex similarly "
        "produces a corner."),
  ("h2", "3.2 &nbsp; Semi-sharp creases"),
  ("p", "A binary sharp/smooth choice is too coarse. <b>Semi-sharp</b> "
        "creases assign a sharpness value s to an edge: apply crease rules "
        "for the first s subdivision levels, then revert to smooth rules."),
  ("callout", "Why this was the feature that mattered",
   ["A perfectly sharp edge reads as computer-generated, because real "
    "manufactured edges have a small fillet from tooling, moulding, or wear. "
    "The eye notices its absence.",
    "Modelling that fillet explicitly requires extra edge loops along every "
    "hard edge, which bloats the control cage and makes it painful to edit.",
    "A semi-sharp crease produces the same appearance from a single number "
    "per edge, with no additional geometry. Fractional sharpness values "
    "interpolate between levels, so an artist can dial an edge continuously "
    "from soft to knife-sharp.",
    "Pixar introduced this (DeRose et al., 1998) and it is the development "
    "that made subdivision practical for hard-surface modelling rather than "
    "only organic forms. Every serious implementation has it."]),

  ("h1", "4 &nbsp; Evaluating a subdivision surface"),
  ("table", ["Method", "How", "Trade-off"],
   [["<b>Iterative refinement</b>", "Apply the rules k times and render the "
     "resulting mesh.",
     "Simple and obviously correct. Face count grows as 4&#7503;, so four "
     "levels is 256&times;. Memory and time become prohibitive quickly."],
    ["<b>Exact evaluation</b> (Stam)",
     "Use the eigenstructure of the subdivision matrix to evaluate the limit "
     "surface directly at any (u,v), including in the neighbourhood of an "
     "extraordinary vertex.",
     "Exact and arbitrary-resolution. Mathematically involved, and the "
     "eigen-decomposition must be precomputed per valence."],
    ["<b>Feature-adaptive</b>", "Refine only near extraordinary vertices and "
     "creases. Everywhere else the mesh is regular, so the surface is already "
     "a bicubic B-spline patch and can be evaluated directly.",
     "The practical answer. This is what OpenSubdiv does, and it is why "
     "film-quality subdivision runs at interactive rates."]],
   [0.20, 0.42, 0.38]),
  ("callout", "Feature-adaptive subdivision is the payoff of &sect;2",
   ["Because regular regions are <i>exactly</i> bicubic B-spline patches, "
    "they need no refinement at all — they can be handed to the GPU "
    "tessellator and evaluated as patches at whatever resolution the view "
    "requires (CSCE 641 Module 12).",
    "Only the small neighbourhoods around extraordinary vertices and creases "
    "need explicit refinement, and because irregularity is isolated after one "
    "step, those neighbourhoods are small and do not grow.",
    "So the cost is dominated by the number of poles in the cage, not by the "
    "subdivision level. A character with a few dozen extraordinary vertices "
    "evaluates in real time at film resolution. This is the single most "
    "important practical fact in the module."]),

  ("h1", "5 &nbsp; Subdivision against the alternatives"),
  ("table", ["", "NURBS patches", "Subdivision", "Plain triangle mesh"],
   [["Arbitrary topology", "Difficult — needs patch layout and trimming",
     "<b>Free</b>", "<b>Free</b>"],
    ["Smoothness", "<b>Exact, analytic</b>",
     "C&#178;, C&#185; at extraordinary vertices", "None"],
    ["Local editing", "Affects a whole patch", "<b>Local</b>", "<b>Local</b>"],
    ["Level of detail", "Re-tessellate", "<b>Intrinsic — just subdivide "
     "less</b>", "Author an LOD chain (Module 10)"],
    ["Exact conics", "<b>Yes</b>", "No", "No"],
    ["Authoring effort", "High — patch layout is skilled work",
     "<b>Low — model a quad cage</b>", "Medium"]],
   [0.20, 0.27, 0.27, 0.26]),
  ("p", "Subdivision wins on every row except exactness, and exactness is "
        "precisely what CAD cannot give up. That single column is the whole "
        "explanation for why the two representations coexist rather than one "
        "displacing the other."),
 ],
 "resources": [
   ("Keenan Crane — DDG, subdivision material",
    "https://brickisland.net/ddg-web/",
    "The rules derived rather than stated, with the B-spline connection made "
    "explicit."),
   ("DeRose, Kass & Truong — Subdivision Surfaces in Character Animation "
    "(free)",
    "https://graphics.pixar.com/library/Geri/paper.pdf",
    "The Pixar paper that introduced semi-sharp creases and put subdivision "
    "into production. Short and very readable."),
   ("Jos Stam — Exact Evaluation of Catmull-Clark Subdivision Surfaces "
    "(free)",
    "https://www.microsoft.com/en-us/research/publication/exact-evaluation-catmull-clark-subdivision-surfaces-arbitrary-parameter-values/",
    "How to evaluate the limit surface directly. The eigenstructure argument "
    "is worth working through once."),
   ("OpenSubdiv (Pixar, open source)",
    "https://graphics.pixar.com/opensubdiv/docs/intro.html",
    "The production implementation, with excellent documentation of "
    "feature-adaptive subdivision. Read the overview even if you do not use "
    "the library."),
 ],
 "exercises": [
   "Implement Catmull&ndash;Clark subdivision on your half-edge structure. "
   "Apply it to a cube three times and verify visually that it converges "
   "toward a sphere-like shape.",
   "Verify the B-spline equivalence: build a regular 4&times;4 quad grid, "
   "subdivide it several times, and compare the result against a bicubic "
   "B-spline surface evaluated over the same control points. Report the "
   "maximum deviation.",
   "Identify and visualise the extraordinary vertices of a subdivided cube "
   "(there are eight, of valence 3). Confirm that their number does not "
   "change with subdivision level.",
   "Render a subdivided surface with a mirror material and an environment "
   "map. Find the reflection distortion at an extraordinary vertex and "
   "capture it.",
   "Implement Loop subdivision for triangle meshes and compare the limit "
   "surfaces of Loop and Catmull&ndash;Clark on the same shape.",
   "Implement sharp creases, then semi-sharp creases with an integer "
   "sharpness. Render a cube with sharpness 0, 2, 4, and infinite, and "
   "compare.",
   "Implement feature-adaptive subdivision: detect regular regions and "
   "evaluate them as B-spline patches, refining only near poles. Measure the "
   "reduction in generated geometry against uniform subdivision at the same "
   "quality.",
 ],
 "selfcheck": [
   "Why does subdivision avoid the vertex enclosure problem entirely?",
   "State the three Catmull&ndash;Clark rules and two structural facts that "
   "follow after one step.",
   "What is the relationship between Catmull&ndash;Clark and bicubic B-spline "
   "surfaces, and why does it matter?",
   "What is an extraordinary vertex, what is the surface's continuity there, "
   "and how is it visible?",
   "Why are semi-sharp creases more useful than binary sharp edges?",
   "Explain feature-adaptive subdivision and why it depends on the fact in "
   "question 3.",
   "Which single column does subdivision lose to NURBS on, and why does that "
   "keep both alive?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Discrete Curvature",
 "subtitle": "Measuring bending on a surface that has none.",
 "question": "What is the curvature of a triangle mesh, which is flat "
             "everywhere?",
 "outcomes": [
     "Define principal, mean, and Gaussian curvature for smooth surfaces.",
     "Explain why naive discretisation fails on a mesh.",
     "Compute discrete Gaussian curvature by angle defect.",
     "Compute discrete mean curvature by the cotangent formula.",
     "State the discrete Gauss–Bonnet theorem and use it as a test.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Smooth curvature",
   "blurb": "The classical definitions, briefly."},

  {"t": "bullets", "kicker": "Smooth", "title": "Principal curvatures and their combinations",
   "items": [
     "At a point, slice the surface with planes containing the normal. Each "
     "slice is a curve with a curvature.",
     "",
     "<b>Principal curvatures</b> κ₁, κ₂: the maximum and "
     "minimum over all such slices. Their directions are orthogonal.",
     "",
     "<b>Mean curvature</b> H = (κ₁ + κ₂)/2 — how "
     "much the surface bends on average.",
     "<b>Gaussian curvature</b> K = κ₁κ₂ — how it "
     "bends intrinsically.",
     "",
     "K > 0 dome, K < 0 saddle, K = 0 developable (a plane or a cylinder).",
   ]},

  {"t": "callout", "title": "Gaussian curvature is intrinsic. Mean curvature is not.",
   "kind": "The distinction that matters",
   "body": ["<b>Theorema Egregium</b> (Gauss): K can be computed from "
            "measurements <i>within</i> the surface — distances and "
            "angles — without any reference to the surrounding space.",
            "Roll a flat sheet of paper into a cylinder: K stays 0 "
            "everywhere, because the paper did not stretch. But H changed, "
            "because the cylinder bends in space and the sheet did not.",
            "Consequence: you cannot flatten a sphere (K > 0) onto a plane "
            "(K = 0) without distortion. <b>That is why every world map lies, "
            "and why UV unwrapping always distorts</b> — Module 09.",
            "K is a property of the surface itself; H depends on how it sits "
            "in space."]},

  {"t": "section", "label": "Part 2", "title": "The problem with meshes",
   "blurb": "Zero on the faces, infinite on the edges, undefined at the "
            "vertices."},

  {"t": "callout", "title": "Naive discretisation gives nothing",
   "kind": "The difficulty",
   "body": ["A triangle mesh is flat on every face: curvature 0.",
            "It bends discontinuously across every edge: curvature is a delta "
            "function, so infinite.",
            "At vertices it is undefined.",
            "So 'compute the curvature of this mesh' by applying the smooth "
            "formulas pointwise yields {0, ∞, undefined} — useless.",
            "<b>The discrete definitions must be derived differently</b>: not "
            "by discretising the formula, but by asking which <i>theorem</i> "
            "we insist on preserving."]},

  {"t": "bullets", "kicker": "Method", "title": "The discrete differential geometry approach",
   "items": [
     "Do not discretise the formula. Discretise the <b>theorem</b>.",
     "",
     "Pick a property of the smooth quantity that you insist must survive "
     "— usually an integral identity.",
     "Define the discrete quantity so that the property holds <b>exactly</b>, "
     "not approximately.",
     "",
     "The result: a definition that is not an approximation but a genuine "
     "discrete analogue.",
     "",
     "<b>No free lunch:</b> you cannot preserve every smooth property at "
     "once. Which one you keep is a design decision.",
   ],
   "note": "This is the philosophical core of the subject and worth stating "
           "explicitly. It is why the definitions look odd and work well."},

  {"t": "section", "label": "Part 3", "title": "Gaussian curvature",
   "blurb": "Angle defect — and it is exact."},

  {"t": "eq", "kicker": "Angle defect", "title": "Discrete Gaussian curvature",
   "eqs": [
     ("Kᵥ  =  2π  −  Σ θᵢ",
      "2π minus the sum of the incident triangle angles at v."),
     ("flat vertex:  angles sum to 2π  ⇒  K = 0",
      "A vertex you can flatten onto a plane has no curvature. Correct."),
     ("dome:  angles sum to < 2π  ⇒  K > 0",
      "Saddle: angles exceed 2π, so K < 0. Also correct."),
   ],
   "caption": "This is an <b>integrated</b> quantity — the total "
              "curvature concentrated at the vertex, not a density. Divide by "
              "the vertex area for a pointwise value.",
   "note": "The integrated-vs-pointwise distinction is a frequent source of "
           "confusion and wrong units. Flag it."},

  {"t": "callout", "title": "Discrete Gauss–Bonnet holds exactly",
   "kind": "Why this definition and no other",
   "body": ["<b>Smooth:</b> ∫∫ K dA = 2πχ = "
            "2π(2 − 2g) for a closed surface.",
            "<b>Discrete:</b> Σᵥ Kᵥ = 2πχ "
            "— <i>exactly</i>, for any mesh, at any resolution, with no "
            "error term.",
            "A sphere mesh of any coarseness gives exactly 4π. A torus "
            "gives exactly 0.",
            "That is why angle defect is <b>the</b> discrete Gaussian "
            "curvature. It is not an approximation that converges — it "
            "satisfies the defining theorem identically.",
            "<b>And it is the best test in Project 1.</b> If your sum is not "
            "4π, your mesh or your code is wrong."]},

  {"t": "section", "label": "Part 4", "title": "Mean curvature",
   "blurb": "The cotangent formula, which reappears everywhere."},

  {"t": "eq", "kicker": "Mean curvature", "title": "The cotangent formula",
   "eqs": [
     ("2 Hᵥ nᵥ  =  ½ Σⱼ (cot αᵢⱼ + cot βᵢⱼ)(vᵢ − vⱼ)",
      "Sum over one-ring neighbours; α and β are the angles "
      "<i>opposite</i> the edge ij."),
     ("the right side is the discrete Laplacian of position",
      "Δv. Which is Module 08's operator, appearing here first."),
     ("Δ x  =  2 H n   (smooth identity)",
      "The Laplacian of the position function <i>is</i> mean curvature times "
      "the normal."),
   ],
   "caption": "Mean curvature and the Laplacian are the same object. That "
              "identity is why smoothing a mesh and reducing its curvature "
              "are the same operation.",
   "note": "This is the single most important formula in the course. Flag it "
           "hard — it returns in Modules 08, 09, and 13."},

  {"t": "bullets", "kicker": "Cotangents", "title": "Why cotangents, and where they bite",
   "items": [
     "The weights are not arbitrary — they come from finite element "
     "analysis on piecewise-linear functions.",
     ("They make the discrete Laplacian agree with the smooth one in a "
      "precise variational sense.", 1),
     "",
     "<b>The problem:</b> cot is negative for obtuse angles.",
     ("An obtuse triangle gives a <b>negative weight</b>.", 1),
     ("Smoothing can then move a vertex the wrong way, and the operator loses "
      "the maximum principle.", 1),
     "",
     "<b>Fix:</b> remesh to remove obtuse triangles (Module 10), or clamp the "
     "weights and accept the approximation.",
   ],
   "footnote": "Mesh quality is not cosmetic — it changes whether your "
               "operators behave.",
   "note": "The negative-weight issue is the practical reason remeshing "
           "matters, and connects Modules 07 and 10."},

  {"t": "table", "kicker": "Practice", "title": "Computing curvature reliably",
   "header": ["Step", "Detail"],
   "widths": [4.0, 8.1],
   "rows": [
     ["Choose a vertex area", "Barycentric (A/3) is simple; Voronoi is better; mixed handles obtuse triangles"],
     ["Integrated or pointwise?", "Angle defect is integrated. Divide by area for a density"],
     ["Validate on a sphere", "K = 1/r², H = 1/r everywhere. Check both"],
     ["Validate by Gauss–Bonnet", "ΣKᵥ = 4π for genus 0. Non-negotiable"],
     ["Watch for obtuse triangles", "Negative cotangent weights break the operator"],
   ]},
 ],
 "takeaways": [
   "Gaussian curvature is intrinsic — measurable within the surface. "
   "Mean curvature is not. This is why flattening always distorts.",
   "A mesh has zero curvature on faces and infinite curvature on edges, so "
   "the smooth formulas cannot simply be discretised.",
   "Discrete differential geometry discretises the <b>theorem</b>, not the "
   "formula — and you cannot preserve every property at once.",
   "Discrete Gaussian curvature is the angle defect 2π − Σθ, "
   "and discrete Gauss–Bonnet holds <i>exactly</i> at any resolution.",
   "ΣKᵥ = 4π for any genus-0 closed mesh. This is the single "
   "best correctness test in the course.",
   "The cotangent formula gives mean curvature, and it is the discrete "
   "Laplacian of position: Δx = 2Hn. Smoothing and reducing curvature "
   "are the same operation.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Curvature on a smooth surface"),
  ("p", "At a point p on a smooth surface with normal n, slice the surface "
        "with a plane containing n. The intersection is a curve, and it has a "
        "curvature. Rotating the plane around n gives a range of values; the "
        "maximum and minimum are the <b>principal curvatures</b> "
        "&kappa;&#8321; and &kappa;&#8322;, attained in orthogonal "
        "directions."),
  ("table", ["Quantity", "Definition", "Meaning", "Sign"],
   [["Mean curvature H", "(&kappa;&#8321; + &kappa;&#8322;)/2",
     "Average bending; how far from a minimal surface.",
     "Sign depends on the normal's orientation."],
    ["Gaussian curvature K", "&kappa;&#8321; &middot; &kappa;&#8322;",
     "Intrinsic bending; how far from flat.",
     "K &gt; 0 dome or bowl; K &lt; 0 saddle; K = 0 developable."]],
   [0.22, 0.20, 0.32, 0.26]),
  ("callout", "Theorema Egregium: K is intrinsic",
   ["Gauss's 'remarkable theorem': Gaussian curvature can be computed "
    "entirely from measurements made <i>within</i> the surface — lengths "
    "and angles — with no reference to the ambient space.",
    "Roll a flat sheet of paper into a cylinder. Nothing stretched, so every "
    "intrinsic measurement is unchanged, and K remains 0 everywhere. But H "
    "changed, because the cylinder bends in space and the flat sheet did not. "
    "K is a property of the surface; H is a property of its embedding.",
    "<b>The consequence that matters for this course:</b> a sphere has "
    "K = 1/r&#178; &gt; 0 and a plane has K = 0. Since K is intrinsic, no "
    "map from sphere to plane can preserve both lengths and angles — "
    "flattening <i>must</i> distort.",
    "That is why every world map misrepresents something, and it is the "
    "reason UV unwrapping (Module 09) is a problem of choosing which "
    "distortion to accept rather than one of avoiding distortion."]),

  ("h1", "2 &nbsp; Why a mesh has no curvature"),
  ("p", "Apply the smooth definitions pointwise to a triangle mesh:"),
  ("ul", ["On the <b>interior of a face</b>, the surface is planar. Both "
          "principal curvatures are 0, so H = K = 0.",
          "Across an <b>edge</b>, the normal changes discontinuously. "
          "Curvature is a delta function — infinite, concentrated on a "
          "set of zero area.",
          "At a <b>vertex</b>, the normal is not even well defined."]),
  ("p", "So the answer is {0, &infin;, undefined} and carries no information "
        "about the shape. Discretising the formula does not work."),
  ("callout", "Discretise the theorem, not the formula",
   ["The method of discrete differential geometry is to choose a "
    "<i>structural property</i> of the smooth quantity — typically an "
    "integral identity or a conservation law — and define the discrete "
    "version so that the property holds <b>exactly</b> on a mesh, not "
    "approximately.",
    "The resulting definition is then a genuine discrete analogue rather than "
    "a numerical approximation that happens to converge. Algorithms built on "
    "it inherit the structure, which is why they tend to be stable and to "
    "behave sensibly on coarse meshes.",
    "<b>There is no free lunch.</b> No discrete definition can preserve every "
    "property of its smooth counterpart simultaneously — this is a "
    "theorem, not a limitation of current knowledge. Which property you "
    "preserve is a design decision, and different applications make different "
    "choices."]),

  ("break",),
  ("h1", "3 &nbsp; Discrete Gaussian curvature: angle defect"),
  ("eq", "K<sub>v</sub> = 2&pi; &minus; &Sigma;<sub>faces f at v</sub> &theta;<sub>f</sub>"),
  ("p", "Sum the interior angles of all triangles meeting at a vertex and "
        "subtract from 2&pi;. The intuition is immediate: if the angles sum "
        "to exactly 2&pi;, the faces around the vertex can be flattened onto "
        "a plane without stretching, so the vertex is intrinsically flat. If "
        "they sum to less, there is a cone point — a dome. If more, "
        "there is excess material — a saddle."),
  ("table", ["&Sigma;&theta;", "K<sub>v</sub>", "Shape"],
   [["= 2&pi;", "0", "Flat: the one-ring unfolds into a plane."],
    ["&lt; 2&pi;", "&gt; 0", "Dome or cone point."],
    ["&gt; 2&pi;", "&lt; 0", "Saddle."]],
   [0.2, 0.2, 0.6]),
  ("callout", "Why this definition is <i>the</i> right one",
   ["The smooth Gauss&ndash;Bonnet theorem states that for a closed surface, "
    "&int;&int; K dA = 2&pi;&chi; where &chi; = 2 &minus; 2g is the Euler "
    "characteristic from Module 01.",
    "With angle defect as the definition, the <b>discrete</b> Gauss&ndash;"
    "Bonnet theorem holds <i>exactly</i>:",
    "&Sigma;<sub>v</sub> K<sub>v</sub> = 2&pi;&chi;, for any mesh, at any "
    "resolution, with no error term whatsoever.",
    "A four-triangle tetrahedron approximating a sphere gives exactly 4&pi;. "
    "A million-triangle sphere gives exactly 4&pi;. This is not convergence "
    "— it is an identity. That is what distinguishes a discrete "
    "<i>analogue</i> from an approximation."]),
  ("callout", "Use it as your test",
   ["Compute &Sigma;K<sub>v</sub> on any closed mesh you load. For genus 0 it "
    "must equal 4&pi; = 12.566&hellip; to within floating-point error. For a "
    "torus it must equal 0.",
    "If it does not, something is wrong: the mesh has holes or non-manifold "
    "elements, the winding is inconsistent, or your angle computation is "
    "buggy. This single check has caught more bugs in this course than any "
    "other, and it is required in Project 1."]),
  ("h2", "3.1 &nbsp; Integrated versus pointwise"),
  ("p", "Angle defect is an <b>integrated</b> quantity: it is the total "
        "curvature concentrated at the vertex, with units of a solid angle, "
        "not a curvature density. For a pointwise value comparable to the "
        "smooth K, divide by an associated vertex area:"),
  ("eq", "K<sub>pointwise</sub> = K<sub>v</sub> / A<sub>v</sub>"),
  ("p", "Confusing the two produces results that look right in shape and are "
        "wrong by a factor of the mesh resolution. Sanity-check on a sphere, "
        "where the pointwise value must be 1/r&#178; everywhere regardless of "
        "tessellation."),

  ("h1", "4 &nbsp; Discrete mean curvature: the cotangent formula"),
  ("eq", "2 H<sub>v</sub> n<sub>v</sub> = &frac12; &Sigma;<sub>j &isin; N(v)</sub> (cot &alpha;<sub>ij</sub> + cot &beta;<sub>ij</sub>)(v<sub>i</sub> &minus; v<sub>j</sub>)"),
  ("p", "where &alpha;<sub>ij</sub> and &beta;<sub>ij</sub> are the two angles "
        "<i>opposite</i> the edge (i, j) in the two triangles sharing it."),
  ("callout", "This expression is the discrete Laplacian",
   ["The right-hand side is the discrete Laplace&ndash;Beltrami operator "
    "applied to the position function — the subject of Module 08, "
    "appearing here first.",
    "The smooth identity it discretises is <b>&Delta;x = 2Hn</b>: the "
    "Laplacian of the position function equals mean curvature times the "
    "normal. Mean curvature and the Laplacian are not two things that happen "
    "to be related; they are the same object.",
    "The practical consequence is immediate and is the reason Module 08 "
    "follows directly: <b>smoothing a surface and reducing its mean curvature "
    "are the same operation</b>. Laplacian smoothing is literally mean "
    "curvature flow."]),
  ("h2", "4.1 &nbsp; Where the cotangents come from, and where they bite"),
  ("p", "The weights are not chosen for convenience. They arise from a finite "
        "element discretisation of the Laplacian using piecewise-linear hat "
        "functions on the triangulation, and they make the discrete operator "
        "agree with the smooth one in a precise variational sense — it "
        "is the gradient of the discrete Dirichlet energy."),
  ("callout", "Obtuse triangles produce negative weights",
   ["The cotangent of an obtuse angle is negative. An edge opposite two "
    "obtuse angles therefore receives a <b>negative weight</b>.",
    "A negative weight means the neighbour pushes the vertex <i>away</i> "
    "rather than pulling it, so Laplacian smoothing can move a vertex "
    "outward, the operator loses the maximum principle, and the resulting "
    "linear systems can lose positive-definiteness.",
    "Symptoms are distinctive: smoothing that increases noise in some region, "
    "parameterisations with flipped triangles (Module 09), or solvers that "
    "fail to converge.",
    "<b>Mesh quality is not cosmetic.</b> It determines whether your "
    "operators behave at all, which is the strongest argument for the "
    "remeshing of Module 10. The alternatives — clamping the weights to "
    "zero, or using the intrinsic Delaunay triangulation — both trade "
    "accuracy for robustness."]),

  ("h1", "5 &nbsp; Computing it reliably"),
  ("table", ["Decision", "Options", "Recommendation"],
   [["Vertex area", "Barycentric (one third of each incident triangle); "
     "Voronoi; mixed Voronoi-barycentric.",
     "Mixed. It handles obtuse triangles correctly, where pure Voronoi areas "
     "can fall outside the triangle."],
    ["Integrated or pointwise", "Angle defect is integrated by nature.",
     "Keep both; be explicit in your API about which you are returning. Most "
     "bugs here are unit confusion."],
    ["Validation", "Sphere: K = 1/r&#178;, H = 1/r. Torus: &Sigma;K = 0. "
     "Plane: both zero.",
     "Test on all three before trusting the code on real data."],
    ["Gauss&ndash;Bonnet check", "&Sigma;K<sub>v</sub> = 2&pi;&chi;.",
     "Assert it. Non-negotiable."],
    ["Obtuse triangles", "Leave, clamp, or remesh.",
     "Detect and report them. Remesh if the downstream algorithm is "
     "sensitive."]],
   [0.20, 0.44, 0.36]),
 ],
 "resources": [
   ("Keenan Crane — DDG, curvature lectures and notes",
    "https://brickisland.net/ddg-web/",
    "The primary source for this module. The 'discretise the theorem' "
    "philosophy is developed properly, with the angle defect derivation."),
   ("Meyer, Desbrun, Schröder & Barr — Discrete Differential-"
    "Geometry Operators (free)",
    "https://www.cs.caltech.edu/~mmeyer/Publications/diffGeomOps.pdf",
    "The paper that established the cotangent formula and the mixed area "
    "region in graphics. Short and still the standard reference."),
   ("Wardetzky et al. — Discrete Laplace operators: no free lunch (free)",
    "https://www.cs.columbia.edu/~keenan/Projects/Other/NoFreeLunch.pdf",
    "The proof that no discrete Laplacian preserves all the smooth "
    "properties. Three pages, and it reframes the whole subject."),
   ("libigl tutorial — curvature",
    "https://libigl.github.io/tutorial/",
    "Working implementations to check your own against."),
 ],
 "exercises": [
   "Implement discrete Gaussian curvature by angle defect. Verify that "
   "&Sigma;K<sub>v</sub> = 4&pi; on a sphere mesh and 0 on a torus. Report "
   "both numbers to six decimal places.",
   "Verify that Gauss&ndash;Bonnet holds at <i>every</i> resolution: compute "
   "the sum on sphere meshes of 20, 200, 2,000, and 200,000 triangles and "
   "confirm all four give 4&pi;.",
   "Compute pointwise Gaussian curvature on a sphere of radius r and confirm "
   "it equals 1/r&#178; everywhere. Identify and explain any deviation at "
   "irregular vertices.",
   "Implement the cotangent formula for mean curvature. Validate on a sphere "
   "(H = 1/r) and a cylinder (H = 1/2r).",
   "Visualise both curvatures as per-vertex colour on a scanned model. "
   "Identify ridges, valleys, and saddles by eye and confirm against the "
   "sign of K.",
   "Detect obtuse triangles in a mesh and count how many produce negative "
   "cotangent weights. Then apply Laplacian smoothing and look for vertices "
   "that move the wrong way.",
   "Implement all three vertex-area definitions and compare the pointwise "
   "curvature each produces on a mesh with some obtuse triangles.",
 ],
 "selfcheck": [
   "Define principal, mean, and Gaussian curvature.",
   "State Theorema Egregium and explain why it means UV unwrapping must "
   "distort.",
   "Why does applying the smooth curvature definitions pointwise to a mesh "
   "give no information?",
   "Explain 'discretise the theorem, not the formula', and state what the "
   "no-free-lunch result says.",
   "Give the angle defect formula and explain why it is the correct discrete "
   "Gaussian curvature.",
   "State discrete Gauss&ndash;Bonnet and say why it is the best test in this "
   "course.",
   "What identity connects mean curvature and the Laplacian, and what "
   "practical consequence follows?",
   "Why do obtuse triangles cause trouble, and what are your options?",
 ],
},

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "The Laplacian and Smoothing",
 "subtitle": "One operator, and most of geometry processing.",
 "question": "Why does the same matrix solve smoothing, parameterisation, "
             "and deformation?",
 "outcomes": [
     "Build the cotangent Laplacian as a sparse matrix.",
     "Implement explicit and implicit Laplacian smoothing.",
     "Explain the stability limit of explicit integration.",
     "Explain shrinkage and how to prevent it.",
     "Explain why the Laplacian underlies so many algorithms.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The operator",
   "blurb": "The difference between a value and the average of its "
            "neighbours."},

  {"t": "eq", "kicker": "The Laplacian", "title": "What it measures",
   "eqs": [
     ("(Δf)ᵢ  =  Σⱼ wᵢⱼ (fⱼ − fᵢ)",
      "How much f at i differs from a weighted average of its neighbours."),
     ("uniform:  wᵢⱼ = 1/deg(i)",
      "Simple, and depends on tessellation rather than on geometry."),
     ("cotangent:  wᵢⱼ = ½(cot α + cot β)",
      "From Module 07. Geometry-aware, and the one to use."),
   ],
   "caption": "The Laplacian measures <i>local deviation from average</i>. "
              "That one idea explains everything it is used for.",
   "note": "Framing it as 'deviation from the neighbourhood mean' makes every "
           "later application feel obvious."},

  {"t": "callout", "title": "Why this operator is everywhere",
   "kind": "Key idea",
   "body": ["<b>Δx = 2Hn</b> (Module 07) — so the Laplacian of "
            "position is mean curvature. Smoothing is curvature flow.",
            "<b>Δf = 0</b> — harmonic functions, which are as "
            "smooth as possible given their boundary. This is "
            "parameterisation (Module 09).",
            "<b>Minimising ∫|∇f|²</b> — the Dirichlet "
            "energy, whose gradient is the Laplacian. Deformation (Module 13) "
            "minimises exactly this.",
            "<b>Eigenvectors of Δ</b> — a Fourier basis for the "
            "surface, giving spectral filtering and shape descriptors.",
            "Four apparently unrelated problems, one matrix. Build it well "
            "once."]},

  {"t": "code", "kicker": "Construction", "title": "The cotangent Laplacian as a sparse matrix",
   "lang": "cpp", "code": """
// L is n x n, sparse, symmetric, with ~7 non-zeros per row.
std::vector<Triplet> trip;
for (each edge (i,j)) {
    float w = 0.5f * (cot(alpha_ij) + cot(beta_ij));
    trip.push_back({i, j,  w});       // off-diagonal
    trip.push_back({j, i,  w});
    trip.push_back({i, i, -w});       // rows must sum to ZERO
    trip.push_back({j, j, -w});
}
L.setFromTriplets(trip.begin(), trip.end());

// ROWS SUM TO ZERO is the invariant that matters:
// it means L annihilates constants, so a flat region has
// zero Laplacian. Assert it.
""",
   "caption": "Rows summing to zero is the structural property to assert. If "
              "they do not, a constant function has non-zero Laplacian and "
              "everything downstream is wrong.",
   "note": "The zero-row-sum assertion catches most construction bugs "
           "immediately."},

  {"t": "section", "label": "Part 2", "title": "Smoothing",
   "blurb": "Move each vertex toward the average of its neighbours."},

  {"t": "two", "kicker": "Integration", "title": "Explicit and implicit",
   "lh": "Explicit — x ← x + λΔx",
   "l": ["One sparse matrix-vector product. Trivial.",
         "<b>Conditionally stable:</b> λ must be small.",
         ("Too large and it oscillates and explodes.", 1),
         "Many small steps needed for visible smoothing.",
         ("Cheap per step, expensive overall.", 1)],
   "rh": "Implicit — (I − λΔ)xⁿ⁺¹ = xⁿ",
   "r": ["Solve a sparse linear system.",
         "<b>Unconditionally stable:</b> any λ works.",
         ("One large step is legitimate.", 1),
         "Needs a sparse Cholesky factorisation.",
         ("Expensive per step, far cheaper overall.", 1)]},

  {"t": "callout", "title": "The stability limit is real and worth seeing",
   "kind": "Why implicit wins",
   "body": ["Explicit smoothing is the heat equation integrated by forward "
            "Euler, and forward Euler on a diffusion equation is stable only "
            "if λ ≲ h², where h is the smallest edge length.",
            "So one small triangle anywhere in the mesh forces a tiny time "
            "step for the <b>whole</b> mesh.",
            "Implicit integration (backward Euler) has no such limit. The "
            "matrix (I − λΔ) is symmetric positive definite, "
            "so one Cholesky factorisation can be reused across steps.",
            "<b>Factor once, solve many times.</b> That is the pattern for "
            "the rest of this course."]},

  {"t": "bullets", "kicker": "Shrinkage", "title": "The problem everyone hits",
   "items": [
     "Laplacian smoothing is mean curvature flow, and mean curvature flow "
     "<b>shrinks closed surfaces</b>.",
     ("A sphere collapses to a point. This is correct behaviour, and "
      "unwanted.", 1),
     "",
     "<b>Fixes:</b>",
     ("<b>Volume preservation</b> — rescale after each step to restore "
      "the original volume.", 1),
     ("<b>Taubin λ|μ</b> — alternate a smoothing step "
      "(λ > 0) with an unsmoothing step (μ < 0, |μ| > λ). "
      "Acts as a low-pass filter with no shrinkage.", 1),
     ("<b>Tangential only</b> — project the update onto the tangent "
      "plane, so vertices redistribute without moving the surface.", 1),
   ],
   "note": "Taubin is elegant and cheap: two explicit steps, no solve, no "
           "shrinkage."},

  {"t": "section", "label": "Part 3", "title": "Better smoothing",
   "blurb": "Removing noise without removing features."},

  {"t": "callout", "title": "Laplacian smoothing cannot tell noise from features",
   "kind": "The limitation",
   "body": ["Both noise and a sharp crease are high-frequency. A low-pass "
            "filter removes both.",
            "Smooth a scanned mechanical part and you remove the scanner "
            "noise and round off every edge the part actually has.",
            "<b>Bilateral filtering</b> fixes this by weighting neighbours by "
            "both spatial distance <i>and</i> normal similarity — so a "
            "neighbour across a crease contributes little.",
            "This is exactly the bilateral filter from image processing, "
            "applied on a surface. The same idea appears in CSCE 748."]},

  {"t": "table", "kicker": "Methods", "title": "Choosing a smoothing method",
   "header": ["Method", "Preserves features", "Cost"],
   "widths": [3.4, 4.4, 4.3],
   "rows": [
     ["Explicit Laplacian", "No", "Cheap per step, many steps"],
     ["Implicit Laplacian", "No", "One factorisation, then cheap"],
     ["Taubin λ|μ", "No, but no shrinkage", "Two explicit steps"],
     ["Bilateral", "<b>Yes</b>", "More expensive; iterative"],
     ["Mean curvature flow", "No", "Same as implicit; geometric meaning"],
   ]},

  {"t": "bullets", "kicker": "Forward", "title": "What else this matrix does",
   "items": [
     "<b>Module 09, parameterisation:</b> solve Δu = 0 with boundary "
     "conditions. Harmonic maps.",
     "<b>Module 13, deformation:</b> minimise ∫|Δx − "
     "δ|² to preserve local detail under a handle constraint.",
     "<b>Spectral geometry:</b> eigenvectors of Δ give a Fourier basis "
     "on the surface — shape descriptors, segmentation, compression.",
     "<b>Geodesic distance:</b> the heat method solves two Laplace systems "
     "and gets distances.",
     "",
     "Build this matrix carefully. You will reuse it in every remaining "
     "module.",
   ],
   "footnote": "It is not an exaggeration that the Laplacian is most of "
               "geometry processing."},
 ],
 "takeaways": [
   "The Laplacian measures how much a value differs from the weighted average "
   "of its neighbours. Every application follows from that.",
   "Use cotangent weights, not uniform ones — uniform weights depend on "
   "tessellation rather than geometry.",
   "Rows of L must sum to zero, so that constants are annihilated. Assert it.",
   "Explicit smoothing is conditionally stable with λ ≲ h², so "
   "one small triangle throttles the whole mesh. Implicit is unconditionally "
   "stable.",
   "Factor once, solve many times. That pattern recurs through the rest of "
   "the course.",
   "Laplacian smoothing shrinks closed surfaces because it is mean curvature "
   "flow. Taubin λ|μ fixes it with two cheap steps.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What the Laplacian is"),
  ("eq", "(&Delta;f)<sub>i</sub> = &Sigma;<sub>j &isin; N(i)</sub> w<sub>ij</sub> (f<sub>j</sub> &minus; f<sub>i</sub>)"),
  ("p", "The Laplacian at vertex i measures how far the value there is from a "
        "weighted average of its neighbours. If f is already the average of "
        "its surroundings, &Delta;f = 0. The operator detects local deviation "
        "from smoothness, and that single description accounts for everything "
        "it is used for."),
  ("table", ["Weighting", "w<sub>ij</sub>", "Behaviour"],
   [["Uniform (graph Laplacian)", "1, or 1/deg(i)",
     "Depends only on connectivity, so it ignores the actual geometry. "
     "Smoothing with it redistributes vertices by valence rather than by "
     "shape. Useful for pure connectivity work; wrong for geometry."],
    ["<b>Cotangent</b>", "&frac12;(cot &alpha;<sub>ij</sub> + cot "
     "&beta;<sub>ij</sub>)",
     "Derived from a finite-element discretisation (Module 07). Geometry-"
     "aware and the correct choice for everything in this course."]],
   [0.24, 0.26, 0.50]),
  ("callout", "Why one operator serves so many problems",
   ["<b>&Delta;x = 2Hn.</b> The Laplacian of the position function is mean "
    "curvature times the normal (Module 07). So flowing along &minus;&Delta;x "
    "<i>is</i> mean curvature flow, and smoothing a surface is literally "
    "reducing its curvature.",
    "<b>&Delta;f = 0</b> defines harmonic functions — the smoothest "
    "function consistent with given boundary values. That is exactly the "
    "parameterisation problem of Module 09.",
    "<b>&Delta; is the gradient of the Dirichlet energy &int;|&nabla;f|&#178;."
    "</b> Any problem phrased as 'find the function that is as smooth as "
    "possible subject to constraints' leads to a Laplace system. Deformation "
    "(Module 13) is this.",
    "<b>The eigenvectors of &Delta; form a Fourier basis on the surface.</b> "
    "Spectral filtering, shape descriptors, segmentation, and compression all "
    "follow.",
    "Four unrelated-looking problems, one sparse matrix. It is worth building "
    "carefully."]),
  ("h2", "1.1 &nbsp; Building it"),
  ("code", """std::vector<Eigen::Triplet<double>> T;
for (Edge e : mesh.edges()) {
    int i = e.v0(), j = e.v1();
    double w = 0.5 * (cot(e.alpha()) + cot(e.beta()));
    T.emplace_back(i, j,  w);
    T.emplace_back(j, i,  w);
    T.emplace_back(i, i, -w);
    T.emplace_back(j, j, -w);
}
L.setFromTriplets(T.begin(), T.end());"""),
  ("callout", "Assert that rows sum to zero",
   ["Each edge contributes +w to two off-diagonal entries and &minus;w to two "
    "diagonal entries, so every row sums to exactly zero by construction.",
    "The property matters: a zero row sum means L annihilates constant "
    "functions, so a flat region has zero Laplacian and a rigid translation "
    "of the mesh does not change it.",
    "If your rows do not sum to zero, a constant function has non-zero "
    "Laplacian, smoothing will drift, and every system you solve will be "
    "subtly wrong. Assert it immediately after construction — it is the "
    "cheapest correctness check available."]),
  ("p", "L is symmetric and sparse, with roughly 7 non-zeros per row given "
        "average valence 6 (Module 01). Use a sparse matrix type; a dense "
        "100,000&times;100,000 matrix is 80 GB."),

  ("h1", "2 &nbsp; Smoothing"),
  ("p", "Move each vertex toward the average of its neighbours. Since "
        "&Delta;x = 2Hn, this is mean curvature flow: a geometric process "
        "with a precise meaning, not an ad hoc averaging."),
  ("h2", "2.1 &nbsp; Explicit integration"),
  ("eq", "x<super>n+1</super> = x<super>n</super> + &lambda; &Delta; x<super>n</super>"),
  ("p", "One sparse matrix-vector product per step. Trivial to implement, and "
        "<b>conditionally stable</b>."),
  ("callout", "The stability limit, and why it hurts",
   ["This is forward Euler applied to the heat equation, and forward Euler on "
    "a diffusion problem is stable only when &lambda; is roughly below "
    "h&#178;, where h is the <i>smallest</i> edge length in the mesh.",
    "Exceed it and the iteration oscillates with growing amplitude and the "
    "mesh explodes — a distinctive and memorable failure.",
    "The practical problem is the word 'smallest'. A single small triangle "
    "anywhere forces a tiny time step for the entire mesh, so a mesh with "
    "one bad triangle smooths hundreds of times more slowly than it should.",
    "Run this deliberately in the exercises. Finding the &lambda; at which "
    "your mesh explodes, and relating it to your shortest edge, makes the "
    "constraint concrete."]),
  ("h2", "2.2 &nbsp; Implicit integration"),
  ("eq", "(I &minus; &lambda;&Delta;) x<super>n+1</super> = x<super>n</super>"),
  ("p", "Backward Euler. Each step requires solving a sparse linear system "
        "rather than performing a multiplication, and in exchange the scheme "
        "is <b>unconditionally stable</b>: any &lambda; produces a sensible "
        "result, so a single large step can accomplish what would take "
        "thousands of explicit steps."),
  ("callout", "Factor once, solve many times",
   ["(I &minus; &lambda;&Delta;) is symmetric and positive definite for "
    "&lambda; &gt; 0, so it admits a sparse Cholesky factorisation.",
    "Compute that factorisation <b>once</b>; each subsequent solve is a cheap "
    "forward and back substitution. If the mesh connectivity and &lambda; do "
    "not change, the factorisation is reusable across every step and across "
    "all three coordinate columns.",
    "This pattern — an expensive factorisation amortised over many cheap "
    "solves — recurs in parameterisation (Module 09) and deformation "
    "(Module 13), where it is what makes interactive editing possible. It is "
    "the single most important performance idea in geometry processing."]),

  ("break",),
  ("h1", "3 &nbsp; Shrinkage"),
  ("p", "Mean curvature flow shrinks closed surfaces. A sphere under mean "
        "curvature flow contracts and vanishes in finite time. Since "
        "Laplacian smoothing <i>is</i> mean curvature flow, smoothing a "
        "closed mesh shrinks it — correct behaviour, and almost never "
        "what you wanted."),
  ("table", ["Fix", "Method", "Trade-off"],
   [["<b>Volume preservation</b>", "After each step, compute the enclosed "
     "volume and uniformly rescale to restore the original.",
     "Simple and effective globally; does not prevent local shrinkage of "
     "features."],
    ["<b>Taubin &lambda;|&mu;</b>", "Alternate a smoothing step with "
     "&lambda; &gt; 0 and an <i>unsmoothing</i> step with &mu; &lt; 0 and "
     "|&mu;| slightly greater than &lambda;.",
     "Acts as a genuine low-pass filter with a near-unit passband, so low "
     "frequencies are preserved and shrinkage essentially vanishes. Two cheap "
     "explicit steps, no linear solve. Usually the right answer."],
    ["<b>Tangential smoothing</b>", "Project the Laplacian update onto the "
     "tangent plane before applying it.",
     "Vertices redistribute across the surface without moving it, improving "
     "mesh quality with no shape change at all. Useful as a remeshing step "
     "(Module 10)."]],
   [0.20, 0.40, 0.40]),

  ("h1", "4 &nbsp; Feature-preserving smoothing"),
  ("callout", "A low-pass filter cannot distinguish noise from a crease",
   ["Scanner noise and a genuine sharp edge are both high-frequency content. "
    "Laplacian smoothing removes both, so cleaning a scanned mechanical part "
    "rounds off every edge the part actually has.",
    "<b>Bilateral filtering</b> weights each neighbour by two factors: "
    "spatial proximity, as usual, and <i>normal similarity</i>. A neighbour "
    "whose normal differs sharply — one across a crease — receives "
    "almost no weight, so the filter averages along features and not across "
    "them.",
    "This is precisely the bilateral filter from image processing, "
    "transplanted to a surface, and the same idea appears again in CSCE 748 "
    "for denoising photographs. Edge-aware filtering is one idea with many "
    "domains."]),
  ("table", ["Method", "Removes noise", "Preserves features", "Cost"],
   [["Explicit Laplacian", "Yes", "No",
     "Cheap per step; many steps needed."],
    ["Implicit Laplacian", "Yes", "No",
     "One factorisation, then cheap. Large steps allowed."],
    ["Taubin &lambda;|&mu;", "Yes", "No, but no shrinkage",
     "Two explicit steps. No solve."],
    ["Bilateral", "Yes", "<b>Yes</b>",
     "Several passes; more expensive per pass."],
    ["Tangential only", "No — redistributes vertices", "Shape unchanged",
     "Cheap. A mesh-quality tool rather than a denoiser."]],
   [0.22, 0.18, 0.28, 0.32]),

  ("h1", "5 &nbsp; What this matrix does next"),
  ("table", ["Module", "Problem", "System solved"],
   [["<b>09</b> Parameterisation",
     "Flatten a surface patch to the plane with least distortion.",
     "&Delta;u = 0 with fixed boundary — harmonic maps; or the "
     "least-squares conformal system."],
    ["<b>13</b> Deformation",
     "Move a handle while preserving local detail everywhere else.",
     "Minimise &#8741;&Delta;x &minus; &delta;&#8741;&#178; subject to handle "
     "constraints — a Laplace system with soft constraints."],
    ["Spectral geometry",
     "Shape descriptors, segmentation, compression, correspondence.",
     "Eigenvectors of &Delta;, which form a Fourier basis on the surface."],
    ["Geodesic distance",
     "Distance from a source across the surface.",
     "The heat method: one heat diffusion solve, then one Poisson solve. Two "
     "systems with the same matrix you already factored."]],
   [0.20, 0.38, 0.42]),
  ("p", "It is not an overstatement to say the Laplacian is most of geometry "
        "processing. Build it correctly, assert the zero row sum, keep the "
        "factorisation around, and the remaining modules become applications "
        "of work you have already done."),
 ],
 "resources": [
   ("Keenan Crane — DDG, the Laplace operator and smoothing lectures",
    "https://brickisland.net/ddg-web/",
    "The operator derived from exterior calculus, with smoothing as curvature "
    "flow."),
   ("Desbrun, Meyer, Schröder & Barr — Implicit Fairing of "
    "Irregular Meshes (free)",
    "https://www.cs.jhu.edu/~misha/Fall07/Papers/Desbrun99.pdf",
    "The paper that introduced implicit smoothing and the cotangent weights "
    "to graphics. Still the clearest account of the stability argument."),
   ("Taubin — A signal processing approach to fair surface design (free)",
    "https://dl.acm.org/doi/10.1145/218380.218473",
    "The &lambda;|&mu; filter, derived properly as a signal-processing "
    "problem."),
   ("libigl tutorial — Laplacian and smoothing",
    "https://libigl.github.io/tutorial/",
    "Working code with Eigen, including the sparse solve pattern."),
 ],
 "exercises": [
   "Build the cotangent Laplacian as a sparse matrix. Assert that every row "
   "sums to zero and that the matrix is symmetric.",
   "Verify &Delta;x = 2Hn numerically: compute the Laplacian of position and "
   "compare against the mean curvature normal from Module 07.",
   "Implement explicit smoothing. Increase &lambda; until the mesh explodes, "
   "record the threshold, and compare it against the square of your shortest "
   "edge length.",
   "Implement implicit smoothing with a sparse Cholesky factorisation. "
   "Confirm it is stable at &lambda; values a thousand times larger than the "
   "explicit limit, and measure the speedup for equivalent smoothing.",
   "Measure shrinkage: smooth a unit sphere and plot enclosed volume against "
   "iteration count. Then implement Taubin &lambda;|&mu; and plot it on the "
   "same axes.",
   "Implement bilateral mesh smoothing. Apply both it and plain Laplacian "
   "smoothing to a noisy scan of a mechanical part and capture the difference "
   "at the sharp edges.",
   "Implement tangential-only smoothing and show it improves triangle quality "
   "metrics without changing the surface.",
   "Compute the first ten eigenvectors of L on a simple mesh and visualise "
   "them as per-vertex colour. Observe that they look like vibration modes.",
 ],
 "selfcheck": [
   "What does the Laplacian measure, in one sentence?",
   "Why use cotangent weights rather than uniform ones?",
   "Why must the rows of L sum to zero, and what goes wrong if they do not?",
   "State the stability condition for explicit smoothing and explain why one "
   "small triangle is a problem.",
   "What does 'factor once, solve many times' mean and why does it matter?",
   "Why does Laplacian smoothing shrink a closed surface, and how does Taubin "
   "&lambda;|&mu; avoid it?",
   "Why can Laplacian smoothing not preserve sharp features, and what does "
   "bilateral filtering change?",
   "Name three other problems that reduce to solving a system with this same "
   "matrix.",
 ],
},

]
