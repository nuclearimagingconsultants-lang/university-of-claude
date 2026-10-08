# -*- coding: utf-8 -*-
"""CSCE 641 — Modules 05-07."""

MODULES = [

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Visibility: Depth, Culling, and the Z-Buffer",
 "subtitle": "Deciding what is in front, cheaply and in any order.",
 "question": "How do you resolve occlusion without sorting the whole scene?",
 "outcomes": [
     "Implement a depth buffer and explain why it is order-independent.",
     "Explain z-fighting quantitatively and apply the right fix.",
     "Implement backface and frustum culling, and state what each saves.",
     "Explain early-Z and the shader features that silently disable it.",
     "Describe why transparency breaks the depth buffer, and the options.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The occlusion problem",
   "blurb": "Nearer surfaces hide further ones. Deciding which is which is "
            "harder than it sounds."},

  {"t": "two", "kicker": "Two approaches", "title": "Sort the geometry, or sort per pixel",
   "lh": "Painter's algorithm — sort triangles",
   "l": ["Draw back to front; later writes cover earlier.",
         "O(n log n) per frame, and the sort is on the CPU.",
         "<b>Fails outright</b> on cyclic overlap and on "
         "interpenetrating geometry.",
         ("Three triangles can mutually overlap with no valid order at "
          "all.", 1),
         "Requires splitting triangles to fix, which is expensive and ugly."],
   "rh": "Z-buffer — sort per pixel",
   "r": ["Store the nearest depth seen so far at every pixel.",
         "O(1) per fragment. No sorting of any kind.",
         "<b>Order-independent</b> for opaque geometry.",
         ("Cyclic overlap and interpenetration are handled exactly, with no "
          "special case.", 1),
         "Costs memory and bandwidth — which in 1974 was prohibitive "
         "and today is nothing."],
   "note": "Catmull's z-buffer is a good example of trading memory for "
           "algorithmic simplicity, a trade that keeps getting better."},

  {"t": "code", "kicker": "Z-buffer", "title": "The entire algorithm",
   "lang": "cpp", "code": """
// Once per frame
clear(depth_buffer, +INFINITY);

// Per fragment, in any order whatsoever
if (fragment.z < depth_buffer[x][y]) {
    depth_buffer[x][y] = fragment.z;
    color_buffer[x][y] = shade(fragment);
}
""",
   "caption": "Four lines. The order-independence is the whole point: "
              "triangles may arrive in any sequence and the result is "
              "identical.",
   "note": "Ask students why this fails for transparency before showing Part "
           "4 — most will work it out."},

  {"t": "section", "label": "Part 2", "title": "Z-fighting",
   "blurb": "When two surfaces disagree about which is in front, and keep "
            "changing their minds."},

  {"t": "bullets", "kicker": "Diagnosis", "title": "What z-fighting actually is",
   "items": [
     "Two surfaces so close in depth that they quantise to the same buffer "
     "value.",
     "Whichever fragment arrives last wins — so the result flickers as "
     "the camera moves and the draw order shifts.",
     "",
     "Recall from Module 03: stored depth is a function of 1/z.",
     ("Precision is concentrated near the near plane.", 1),
     ("The <b>f/n ratio</b> is the number that matters, not the absolute "
      "far distance.", 1),
     "",
     "So the first thing to try is almost always: <b>push the near plane "
     "out</b>.",
   ]},

  {"t": "table", "kicker": "Fixes", "title": "Ranked by value for effort",
   "header": ["Fix", "What it does", "When to use it"],
   "widths": [3.0, 5.2, 3.9],
   "rows": [
     ["Increase near plane", "Attacks the dominant precision term directly",
      "Always try first. Nearly free."],
     ["Reversed-Z + float depth", "Cancels 1/z against float density",
      "Permanent fix. Do it once in Project 2."],
     ["Fix the geometry", "Stop authoring coplanar surfaces",
      "When it is a content problem, which is often."],
     ["Polygon offset", "Biases one surface away in depth",
      "Decals, coplanar overlays. Tune carefully."],
     ["Depth pre-pass", "Establishes exact depth, then draws equal",
      "Heavy fragment shaders; helps overdraw too."],
   ]},

  {"t": "section", "label": "Part 3", "title": "Not drawing things",
   "blurb": "Every form of culling is the same idea: reject early, at the "
            "coarsest granularity you can."},

  {"t": "bullets", "kicker": "Culling", "title": "The hierarchy of rejection",
   "items": [
     "<b>Frustum culling</b> (CPU, per object) — is the bounding volume "
     "outside the view? Rejects whole objects for the cost of six plane "
     "tests.",
     "<b>Occlusion culling</b> (CPU/GPU, per object) — is it entirely "
     "behind something already drawn? Hardest to do well, biggest win "
     "indoors.",
     "<b>Backface culling</b> (GPU, per triangle) — sign of the "
     "screen-space area. Removes about half of a closed mesh for one "
     "subtraction.",
     "<b>Hierarchical Z</b> (GPU, per tile) — reject a whole tile "
     "against the coarsest depth. Free, in hardware.",
     "<b>Early-Z</b> (GPU, per fragment) — depth test before shading "
     "rather than after.",
   ],
   "footnote": "Each level is cheaper per unit of work rejected than the one "
               "below it. Reject as high up as you can.",
   "note": "The organising principle is worth stating explicitly: coarse "
           "rejection is cheap per unit rejected, fine rejection is "
           "expensive. Spend effort at the top."},

  {"t": "callout", "title": "Early-Z, and how to lose it", "kind": "Performance cliff",
   "body": ["The depth test logically happens <i>after</i> the fragment "
            "shader. Hardware moves it before, so doomed fragments never "
            "shade — often the single largest saving in a frame.",
            "It is disabled automatically if your fragment shader writes "
            "<code>gl_FragDepth</code>, calls <code>discard</code>, or uses "
            "certain side-effecting operations — because then the "
            "hardware cannot know the depth in advance.",
            "Adding one <code>discard</code> for alpha-tested foliage can "
            "therefore cost far more than the discard itself. The fix is "
            "usually <code>layout(early_fragment_tests) in;</code> when you "
            "know the depth is still valid, or a depth pre-pass."]},

  {"t": "section", "label": "Part 4", "title": "Transparency",
   "blurb": "The case the depth buffer cannot handle, and what to do instead."},

  {"t": "bullets", "kicker": "The problem", "title": "Why transparency breaks the z-buffer",
   "items": [
     "The depth buffer keeps one depth per pixel: it assumes one visible "
     "surface.",
     "A transparent surface does not hide what is behind it — it "
     "<i>combines</i> with it.",
     "",
     "Blending is order-dependent: <code>over</code> does not commute.",
     ("So transparent geometry must be drawn back to front — which is "
      "the painter's algorithm, with all of its failure cases back.", 1),
     "",
     "And sorting per-object is not enough: a single object can self-overlap.",
   ]},

  {"t": "table", "kicker": "Options", "title": "Approaches to transparency",
   "header": ["Approach", "How", "Cost / limitation"],
   "widths": [3.2, 5.0, 3.9],
   "rows": [
     ["Sort back to front", "Sort draws by depth; depth-write off",
      "Cheap. Wrong on self-overlap and intersection."],
     ["Alpha testing", "discard below a threshold; stays opaque",
      "Order-independent, but hard edges and kills early-Z."],
     ["Weighted blended OIT", "Approximate, order-independent weighting",
      "One extra target. Approximate but robust."],
     ["Depth peeling", "Render the scene once per depth layer",
      "Exact; cost scales with layer count."],
     ["Per-pixel linked lists", "Capture all fragments, sort in a shader",
      "Exact; needs atomics and unbounded memory."],
   ],
   "note": "Weighted blended OIT is the pragmatic default in most engines "
           "today. Worth implementing in Project 2 as an extension."},

  {"t": "code", "kicker": "In practice", "title": "The standard opaque/transparent split",
   "lang": "cpp", "code": """
// 1. Opaque: front-to-back maximises early-Z rejection.
glEnable(GL_DEPTH_TEST);
glDepthMask(GL_TRUE);
glDisable(GL_BLEND);
sort_front_to_back(opaque);
draw(opaque);

// 2. Transparent: back-to-front, test against depth but do NOT write it.
glEnable(GL_BLEND);
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
glDepthMask(GL_FALSE);          // <-- the line everyone forgets
sort_back_to_front(transparent);
draw(transparent);
""",
   "caption": "<code>glDepthMask(GL_FALSE)</code> is the critical line: "
              "transparent surfaces must be occluded by opaque geometry, but "
              "must not occlude each other.",
   "note": "Forgetting the depth mask produces transparent objects that "
           "mysteriously erase each other. Very common bug."},

  {"t": "bullets", "kicker": "Project 1", "title": "What you now have",
   "items": [
     "Modules 02–03 gave you the transform chain.",
     "Module 04 gave you coverage, barycentrics, and perspective correction.",
     "Module 05 gives you depth and culling.",
     "",
     "<b>That is a complete renderer.</b> Project 1 is now buildable "
     "end to end.",
     ("Load a mesh, transform, cull, clip, rasterize, depth-test, write a "
      "PNG.", 1),
     ("No GPU. No graphics API. Nothing you did not write.", 1),
   ]},
 ],
 "takeaways": [
   "The z-buffer trades memory for order-independence — and that trade "
   "has only improved since 1974.",
   "Z-fighting is a precision problem dominated by the f/n ratio. Push the "
   "near plane out first; adopt reversed-Z permanently.",
   "Culling is a hierarchy. Reject at the coarsest granularity available, "
   "because that is where rejection is cheapest per unit of work saved.",
   "Early-Z is often the biggest single saving in a frame, and "
   "<code>discard</code> or depth-writing silently disables it.",
   "Transparency breaks the z-buffer's one-surface-per-pixel assumption; "
   "every solution is a different compromise between exactness and cost.",
   "Draw opaque front-to-back, transparent back-to-front with depth writes "
   "disabled.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Hidden surface removal"),
  ("p", "Several surfaces project onto the same pixel. Only the nearest "
        "opaque one should be visible. The question is how to determine which "
        "without an expensive global ordering."),
  ("h2", "1.1 &nbsp; Why sorting fails"),
  ("p", "The painter's algorithm sorts triangles by depth and draws them back "
        "to front. It is intuitive and it does not work. Three triangles can "
        "be arranged so that A occludes B, B occludes C, and C occludes A "
        "— a cycle, admitting no valid ordering. Interpenetrating "
        "triangles fail even more simply: neither is wholly in front. Both "
        "cases require splitting geometry at render time, which is expensive, "
        "introduces cracks, and changes your triangle count unpredictably."),
  ("h2", "1.2 &nbsp; The z-buffer"),
  ("p", "Catmull's 1974 solution resolves occlusion per pixel rather than per "
        "primitive. Keep a second buffer holding, for each pixel, the depth "
        "of the nearest fragment seen so far."),
  ("code", """clear(depth, +INF);

for each fragment f:            // ANY order
    if (f.z < depth[f.x][f.y]) {
        depth[f.x][f.y] = f.z;
        color[f.x][f.y] = shade(f);
    }"""),
  ("callout", "The property that matters",
   ["The result is <b>independent of submission order</b>. Cyclic overlap and "
    "interpenetration are handled exactly, with no special case, because the "
    "comparison happens at the only granularity where the question is "
    "well-posed: the individual sample.",
    "The cost is a full-resolution buffer and the bandwidth to read and write "
    "it. In 1974 that was prohibitive. Today the depth buffer is simply "
    "assumed, and hardware compresses it aggressively."]),

  ("h1", "2 &nbsp; Z-fighting"),
  ("p", "When two surfaces lie at nearly the same depth, their quantised "
        "depth values collide. Whichever fragment is processed last wins, and "
        "since processing order shifts with camera motion and draw order, the "
        "surfaces flicker against each other in a characteristic shimmering "
        "pattern."),
  ("p", "Module 03 established the cause: stored depth is a function of 1/z, "
        "so precision is concentrated near the camera and sparse far away. "
        "The governing quantity is the ratio f/n, not the absolute distances. "
        "A frustum with n = 0.01 and f = 1000 has a ratio of 100,000 and will "
        "z-fight on anything distant; raising n to 0.5 drops the ratio to "
        "2,000 and usually eliminates the problem entirely."),
  ("table", ["Fix", "Mechanism", "Trade-off"],
   [["Push the near plane out", "Directly reduces f/n, the dominant term.",
     "Geometry closer than n is clipped. Usually acceptable; try this first."],
    ["Reversed-Z with float depth",
     "Float precision is dense near 0; reversing maps the far plane to 0, so "
     "the two non-uniformities cancel.",
     "Requires GL_GREATER, zero-to-one clip control, and updating every "
     "shader that reads depth. Do it once, benefit forever."],
    ["Fix the content",
     "Do not author coplanar surfaces where they can be avoided.",
     "Free, and frequently the correct answer. A decal 0.5mm above a wall is "
     "a content decision, not a renderer bug."],
    ["Polygon offset",
     "Adds a slope-scaled bias in depth to push one surface away.",
     "Over-biasing detaches the surface visually — the same "
     "peter-panning failure mode as shadow bias in Module 10."],
    ["Depth pre-pass",
     "Render depth only, then render colour with GL_EQUAL.",
     "Doubles vertex work; pays for itself when fragment shaders are "
     "expensive, and helps overdraw as a side effect."]],
   [0.22, 0.38, 0.40]),

  ("break",),
  ("h1", "3 &nbsp; Culling: the hierarchy of not drawing"),
  ("p", "Every culling technique is the same idea applied at a different "
        "granularity: determine cheaply that something cannot contribute, and "
        "skip it. The organising principle is that coarse rejection is cheap "
        "<i>per unit of work avoided</i>, so you should reject as high up the "
        "hierarchy as you can."),
  ("table", ["Level", "Granularity", "Test", "Typical saving"],
   [["Frustum culling", "Object", "Bounding sphere or box against six planes",
     "Large in open scenes; most of the world is off-screen."],
    ["Occlusion culling", "Object",
     "Bounding volume against a depth representation of what is already drawn",
     "Very large indoors; hardest to implement well."],
    ["Backface culling", "Triangle", "Sign of signed screen-space area",
     "~50% of triangles on any closed mesh, for one subtraction."],
    ["Hierarchical Z", "Tile", "Tile depth range against coarse depth buffer",
     "Automatic in hardware; depends on draw order."],
    ["Early-Z", "Fragment", "Depth test moved before the fragment shader",
     "Proportional to overdraw; often the biggest single win."]],
   [0.19, 0.12, 0.38, 0.31]),
  ("h2", "3.1 &nbsp; Backface culling"),
  ("p", "After projection, compute the signed area of the triangle in screen "
        "space — the same edge-function sum from Module 04. Its sign is "
        "the winding direction; one sign means the triangle faces away from "
        "the camera. On a closed mesh, exactly half the triangles face away "
        "at any moment, so this removes half the rasterization work for the "
        "cost of a subtraction you had already computed."),
  ("p", "It is only valid for closed geometry. A single-sided plane, a sheet "
        "of cloth, or a leaf card must have culling disabled, or it vanishes "
        "when viewed from behind. This is the cause of the classic 'the wall "
        "disappears when I walk through it' behaviour."),
  ("h2", "3.2 &nbsp; Early-Z and how it is lost"),
  ("p", "Logically the depth test runs after the fragment shader, since the "
        "shader may modify depth. In practice the hardware runs it first "
        "whenever it can prove that is equivalent, which means occluded "
        "fragments are discarded before any shading work occurs. In a scene "
        "with significant overdraw this is frequently the largest single "
        "saving in the frame."),
  ("callout", "What silently disables early-Z",
   ["Writing <code>gl_FragDepth</code> — the hardware cannot know the "
    "depth in advance.",
    "Calling <code>discard</code> — the fragment might not write depth "
    "at all, so the depth buffer cannot be updated speculatively.",
    "Shader side effects: image stores, atomics, SSBO writes.",
    "The practical consequence: adding one <code>discard</code> to a foliage "
    "shader can cost far more than the discard itself, because it turns off "
    "early rejection for that entire draw. Mitigate with "
    "<code>layout(early_fragment_tests) in;</code> where the semantics permit "
    "it, or with a depth pre-pass."]),

  ("h1", "4 &nbsp; Transparency"),
  ("p", "The depth buffer stores one depth per pixel because it assumes one "
        "visible surface per pixel. Transparency violates that assumption "
        "directly: a transparent surface does not replace what is behind it, "
        "it combines with it, so the final colour depends on every surface "
        "along the ray and on the order they are composited."),
  ("p", "The standard <code>over</code> operator is not commutative:"),
  ("eq", "C = &alpha;&#8347;C&#8347; + (1 &minus; &alpha;&#8347;)C&#8336;"),
  ("p", "Swap two layers and you get a different colour. So transparent "
        "geometry must be composited back to front — which reintroduces "
        "the painter's algorithm and all of its failure cases, now at the "
        "level of individual transparent surfaces rather than the whole "
        "scene."),
  ("h2", "4.1 &nbsp; The practical approach"),
  ("code", """// Pass 1 -- opaque, front to back (maximises early-Z rejection)
glEnable(GL_DEPTH_TEST);
glDepthMask(GL_TRUE);
glDisable(GL_BLEND);
draw(sort_front_to_back(opaque));

// Pass 2 -- transparent, back to front
glEnable(GL_BLEND);
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
glDepthMask(GL_FALSE);     // test against depth, but do not write it
draw(sort_back_to_front(transparent));"""),
  ("p", "The depth mask is the line that is most often forgotten. Transparent "
        "surfaces must still be <i>occluded</i> by opaque geometry, so the "
        "depth test stays on; but if they <i>write</i> depth they will occlude "
        "each other, and the nearest transparent surface will erase every "
        "transparent surface behind it. The symptom is transparent objects "
        "that mysteriously punch holes in one another."),
  ("h2", "4.2 &nbsp; When sorting is not enough"),
  ("p", "Per-object sorting fails whenever a single object overlaps itself "
        "— a glass teapot, a particle cloud, foliage. The options then "
        "are: alpha testing (order-independent but hard-edged, and it kills "
        "early-Z); weighted blended order-independent transparency (an "
        "approximation that is robust and cheap, and the pragmatic default in "
        "most engines today); depth peeling (exact, but costs a full scene "
        "pass per depth layer); or per-pixel fragment lists with atomics "
        "(exact, but needs unbounded memory and careful fallbacks)."),

  ("h1", "5 &nbsp; You now have a renderer"),
  ("p", "Modules 02 and 03 gave you the transform chain. Module 04 gave you "
        "coverage, barycentric interpolation, and perspective correction. "
        "This module adds depth and culling. Those are, together, a complete "
        "renderer: Project 1 is now buildable end to end, with no GPU, no "
        "graphics API, and nothing in it you did not write yourself."),
 ],
 "resources": [
   ("GAMES101 Lecture 07 — Shading 1 (Z-buffering section)",
    "https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html",
    "The z-buffer and painter's algorithm comparison, including the cyclic "
    "overlap case."),
   ("NVIDIA — Depth Precision Visualized",
    "https://developer.nvidia.com/content/depth-precision-visualized",
    "The authoritative treatment of z-fighting and reversed-Z, with the "
    "diagrams that make the 1/z distribution obvious."),
   ("Fabian Giesen — 'A trip through the Graphics Pipeline', early-Z and "
    "hierarchical Z parts",
    "https://fgiesen.wordpress.com/2011/07/09/a-trip-through-the-graphics-pipeline-2011-index/",
    "How Hi-Z, early-Z, and depth compression actually work in hardware, and "
    "exactly what turns them off."),
   ("McGuire & Bavoil — Weighted Blended Order-Independent Transparency",
    "https://jcgt.org/published/0002/02/09/",
    "Open-access paper. The practical OIT method, with code."),
 ],
 "exercises": [
   "Add a z-buffer to your rasterizer. Verify order-independence by rendering "
   "the same scene with the triangle list shuffled and confirming the output "
   "images are bit-identical.",
   "Construct the three-triangle cyclic overlap case and render it with a "
   "painter's algorithm and with the z-buffer. Capture both; the painter's "
   "version cannot be made correct by any ordering.",
   "Implement backface culling. Measure the fragment count with and without "
   "on a closed mesh and confirm it is close to half.",
   "Deliberately set near = 0.001 and far = 10000 and find a camera position "
   "that z-fights. Then fix it by raising the near plane, and record the "
   "ratio at which the artifact disappears.",
   "Implement reversed-Z in your software rasterizer: it is just a different "
   "projection matrix and a flipped comparison. Compare depth precision "
   "across the view distance against the standard mapping.",
   "<b>Project 1 is now due.</b> Assemble Modules 02–05 into the "
   "complete software rasterizer described in the syllabus, with both "
   "required screenshots.",
 ],
 "selfcheck": [
   "Give a configuration of triangles for which no draw order is correct, and "
   "explain why the z-buffer handles it without a special case.",
   "Why is the f/n ratio the governing quantity for depth precision rather "
   "than the absolute far distance?",
   "Explain how reversed-Z recovers precision, and list the four changes "
   "required to adopt it.",
   "Name three things in a fragment shader that disable early-Z, and explain "
   "why each one does.",
   "Why must transparent geometry disable depth writes but keep the depth "
   "test?",
   "Per-object back-to-front sorting is insufficient for a glass teapot. Why, "
   "and what would you use instead?",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Light, Colour, and Local Shading",
 "subtitle": "Why surfaces look the way they do, and the models that fake it.",
 "question": "What determines the colour of a point on a surface?",
 "outcomes": [
     "Explain radiometric quantities and why irradiance falls off with cosine.",
     "Derive Lambert's cosine law and implement diffuse shading.",
     "Implement Blinn–Phong and state honestly where it is wrong.",
     "Explain gamma and linear workflow, and why ignoring it looks bad.",
     "Distinguish flat, Gouraud, and Phong interpolation and their artifacts.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What light is doing",
   "blurb": "Enough radiometry to stop guessing."},

  {"t": "table", "kicker": "Radiometry", "title": "The quantities that matter",
   "header": ["Quantity", "Units", "Intuitively"],
   "widths": [3.2, 3.0, 5.9],
   "rows": [
     ["Flux Φ", "W", "Total power carried by light"],
     ["Irradiance E", "W/m²", "Power <i>arriving</i> per unit area"],
     ["Radiance L", "W/(m²·sr)", "Power per area per solid angle — what a pixel measures"],
     ["BRDF fᵣ", "1/sr", "Fraction of incoming light reflected in a given direction"],
   ],
   "note": "Radiance is the key one: it is constant along a ray in vacuum, "
           "which is exactly why it is the quantity a renderer transports."},

  {"t": "callout", "title": "Why radiance is the right quantity",
   "kind": "Key idea",
   "body": ["Radiance is constant along a ray through empty space. Flux and "
            "irradiance are not.",
            "That invariance is what makes 'what colour is this pixel?' a "
            "well-posed question with a transportable answer — you can "
            "compute it at the surface and it is still valid at the eye.",
            "Every renderer, from this course's rasterizer to a production "
            "path tracer, transports radiance. Module 11 and CSCE 647 make "
            "this precise."]},

  {"t": "eq", "kicker": "Lambert", "title": "The cosine law",
   "eqs": [
     ("E  =  Φ / A",
      "Irradiance is power spread over area."),
     ("A_effective  =  A / cosθ",
      "Tilt a surface away from a beam and the same power covers more area."),
     ("E  =  E₀ cosθ  =  E₀ (n · l)",
      "Hence the cosine. This is geometry, not a material property."),
   ],
   "caption": "The n·l in every diffuse shader is not an approximation "
              "of anything — it is exactly the geometric foreshortening "
              "of the incoming beam.",
   "note": "Students often think n·l is an empirical hack. Stress that "
           "it is exact geometry, unlike the specular terms that follow."},

  {"t": "code", "kicker": "Diffuse", "title": "Lambertian shading",
   "lang": "glsl", "code": """
vec3 N = normalize(vNormal);         // renormalize after interpolation
vec3 L = normalize(lightPos - vPos);

float ndotl = max(dot(N, L), 0.0);   // clamp: no negative light

// 1/pi is the normalisation that makes the BRDF energy-conserving:
// a perfectly white surface must not reflect more than it receives.
vec3 diffuse = albedo / PI * lightColor * ndotl * attenuation;
""",
   "caption": "The 1/π is routinely omitted in older code, and then "
              "compensated for by tuning light intensities. That works until "
              "you want physically meaningful units — see Module 11.",
   "note": "Flag the 1/pi now; Module 11 depends on it being there."},

  {"t": "section", "label": "Part 2", "title": "Specular",
   "blurb": "Where the physics stops and the curve-fitting begins."},

  {"t": "two", "kicker": "Specular models", "title": "Phong and Blinn–Phong",
   "lh": "Phong (1975)",
   "l": ["Reflect L about N, compare to view.",
         "<code>R = reflect(-L, N)</code>",
         "<code>spec = pow(max(dot(R,V),0), s)</code>",
         ("Highlight cuts off abruptly at grazing angles.", 1),
         ("One extra reflect() per fragment.", 1)],
   "rh": "Blinn–Phong (1977)",
   "r": ["Halfway vector between L and V; compare to N.",
         "<code>H = normalize(L + V)</code>",
         "<code>spec = pow(max(dot(N,H),0), s)</code>",
         ("Highlight elongates at grazing angles — which is what real "
          "surfaces do.", 1),
         ("Cheaper, and closer to measured data.", 1)],
   "note": "Blinn-Phong is both cheaper and more accurate, which is why it "
           "won. The halfway vector reappears in Module 11 as the microfacet "
           "normal."},

  {"t": "callout", "title": "Be honest about what this is", "kind": "Caveat",
   "body": ["Blinn–Phong is a curve that happens to resemble a specular "
            "highlight. It is not derived from anything.",
            "It does not conserve energy: raise the shininess and the surface "
            "can reflect more light than it received. It has no notion of "
            "Fresnel, so it misses the bright rims on every real surface at "
            "grazing angles. Its parameters have no physical meaning, so "
            "materials must be retuned under every new lighting setup.",
            "It is still worth learning: it is cheap, it is everywhere in "
            "existing code, and Module 11's microfacet model is most easily "
            "understood as the principled replacement for exactly these "
            "defects."]},

  {"t": "section", "label": "Part 3", "title": "Where you evaluate it",
   "blurb": "Per face, per vertex, or per fragment — three different "
            "pictures."},

  {"t": "table", "kicker": "Interpolation", "title": "Three shading frequencies",
   "header": ["Model", "Evaluate at", "Interpolate", "Characteristic artifact"],
   "widths": [2.4, 2.5, 2.8, 4.4],
   "rows": [
     ["Flat", "Per face", "Nothing", "Visible facets; correct for genuinely flat surfaces"],
     ["Gouraud", "Per vertex", "Colour", "Highlights distort or vanish between vertices"],
     ["Phong", "Per fragment", "Normal", "Correct highlights; costs a normalize per fragment"],
   ],
   "note": "Gouraud's failure is instructive: a specular highlight smaller "
           "than a triangle simply disappears, because it was never sampled "
           "at a vertex."},

  {"t": "bullets", "kicker": "Gouraud", "title": "Why Gouraud fails on highlights",
   "items": [
     "A specular highlight is a narrow function — it falls off as "
     "cosⁿ with n often in the hundreds.",
     "Gouraud samples that function only at the three vertices.",
     "",
     "If the highlight falls <i>between</i> vertices, it is never sampled.",
     ("The highlight vanishes entirely.", 1),
     ("As the object moves, it pops in and out as it crosses vertices.", 1),
     "",
     "This is undersampling — the Module 01 theme, appearing again.",
   ]},

  {"t": "section", "label": "Part 4", "title": "Gamma",
   "blurb": "The step whose absence makes everything look wrong in a way "
            "that is hard to name."},

  {"t": "callout", "title": "Displays are not linear", "kind": "Essential",
   "body": ["An sRGB display emits light roughly proportional to "
            "<i>value</i>²·², not to <i>value</i>. A pixel "
            "value of 0.5 emits about 21% of maximum, not 50%.",
            "So textures authored on a display are already encoded with the "
            "inverse curve. If you light them without decoding first, you are "
            "doing arithmetic on perceptual values rather than on light.",
            "The result: dark midtones, muddy shadows, harsh highlights, and "
            "blends that look wrong. It is the single most common reason "
            "amateur renders look amateur."]},

  {"t": "code", "kicker": "Gamma", "title": "The linear workflow",
   "lang": "glsl", "code": """
// 1. DECODE on input. Colour textures are sRGB-encoded; data is not.
//    Use an sRGB texture format and the hardware decodes for free.
glTexImage2D(..., GL_SRGB8_ALPHA8, ...);   // albedo, emissive
glTexImage2D(..., GL_RGBA8, ...);          // normal, roughness, metallic
                                           //   <- NEVER sRGB

// 2. Do ALL lighting arithmetic in linear space.
vec3 color = lighting(albedo_linear, N, L, V);

// 3. ENCODE on output, once, at the very end.
glEnable(GL_FRAMEBUFFER_SRGB);             // hardware encodes for free
""",
   "caption": "Normal maps, roughness, metallic, and ambient occlusion are "
              "<b>data</b>, not colour. Tagging them sRGB corrupts them, and "
              "the error is subtle enough to survive review.",
   "note": "This slide prevents more bad-looking renders than any other in "
           "the course. Dwell on it."},

  {"t": "eq", "kicker": "Attenuation", "title": "Falloff, and why it is squared",
   "eqs": [
     ("E  ∝  1 / d²",
      "Energy spreads over a sphere of area 4πd². This is exact, "
      "not an approximation."),
     ("attenuation = 1 / (d² + ε)",
      "The epsilon prevents a division by zero at the light's position."),
     ("directional light: no falloff",
      "The sun is effectively at infinity — a w = 0 light, as Module 02 "
      "noted."),
   ],
   "caption": "Older engines used linear or tunable falloff to compensate for "
              "missing gamma correction. With a correct linear workflow, "
              "inverse-square is right and looks right."},
 ],
 "takeaways": [
   "Radiance is the quantity renderers transport, because it is constant "
   "along a ray in vacuum.",
   "The n·l in diffuse shading is exact geometry — the "
   "foreshortening of the incoming beam — not an empirical fudge.",
   "Blinn–Phong is a curve fit: cheap, ubiquitous, energy-violating, "
   "Fresnel-free. Learn it, then replace it in Module 11.",
   "Shading frequency determines the artifact: flat gives facets, Gouraud "
   "loses highlights between vertices, Phong costs a normalize.",
   "Decode sRGB on input, light in linear space, encode once on output. "
   "Normal and roughness maps are data and must never be tagged sRGB.",
   "Inverse-square falloff is correct. If it looks wrong, your gamma handling "
   "is wrong.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Just enough radiometry"),
  ("p", "Shading models are easier to reason about, and much easier to debug, "
        "if you know which physical quantity each term is supposed to "
        "represent. Four quantities suffice for this course."),
  ("table", ["Quantity", "Symbol", "Units", "What it is"],
   [["Radiant flux", "&Phi;", "W", "Total power carried by light."],
    ["Irradiance", "E", "W/m&#178;",
     "Flux arriving per unit surface area. Depends on the angle the surface "
     "makes with the beam."],
    ["Radiance", "L", "W/(m&#178;&middot;sr)",
     "Flux per unit projected area per unit solid angle. What a camera pixel "
     "and an eye both actually measure."],
    ["BRDF", "f&#7523;", "1/sr",
     "The fraction of radiance arriving from one direction that leaves in "
     "another. The complete description of a surface's appearance."]],
   [0.20, 0.09, 0.17, 0.54]),
  ("callout", "Why radiance",
   ["Radiance is invariant along a ray in a vacuum: the radiance leaving a "
    "surface toward the eye equals the radiance arriving at the eye from that "
    "surface, regardless of distance.",
    "Irradiance is not invariant — it falls off with distance. Flux is "
    "not invariant — it depends on the area considered.",
    "That invariance is precisely why 'what colour is this pixel' can be "
    "answered by computing something at the surface. Every renderer "
    "transports radiance."]),

  ("h1", "2 &nbsp; Diffuse reflection"),
  ("h2", "2.1 &nbsp; The cosine law, derived"),
  ("p", "Consider a parallel beam of light with cross-sectional area A "
        "striking a surface. If the surface is perpendicular to the beam, the "
        "power lands on area A. If the surface is tilted by &theta;, the same "
        "power is spread across A/cos&theta; — a larger area — so "
        "the irradiance is reduced by cos&theta;."),
  ("eq", "E = E&#8320; cos&theta; = E&#8320; (n &middot; l)"),
  ("p", "This is worth internalising properly: the n &middot; l factor "
        "appearing in every diffuse shader is not a property of the material "
        "and not an approximation of anything. It is the geometric "
        "foreshortening of the incident beam, and it would be there for any "
        "material whatsoever. The material's contribution is the BRDF, which "
        "for an ideal diffuse surface is a constant."),
  ("h2", "2.2 &nbsp; Energy conservation and the missing &pi;"),
  ("p", "A Lambertian surface scatters incoming light equally in all "
        "directions over the hemisphere. For the total reflected energy not "
        "to exceed the incoming energy, the BRDF must be albedo/&pi;, not "
        "albedo. The &pi; arises from integrating the cosine over the "
        "hemisphere:"),
  ("eq", "&int;<sub>&Omega;</sub> cos&theta; d&omega; = &pi;"),
  ("code", """vec3 N = normalize(vNormal);
vec3 L = normalize(lightPos - vPos);
float ndotl = max(dot(N, L), 0.0);

vec3 diffuse = (albedo / PI) * lightColor * ndotl * attenuation;""",
   "A great deal of older code omits the 1/&pi; and compensates by inflating "
   "light intensities. That is self-consistent but means your light units are "
   "arbitrary, which stops working as soon as you want physically based "
   "materials or image-based lighting. Keep the &pi;."),

  ("h1", "3 &nbsp; Specular reflection"),
  ("p", "Diffuse reflection is the easy case because it is directionless. "
        "Specular reflection depends on the view direction, and the classical "
        "models for it are curve fits rather than derivations."),
  ("h2", "3.1 &nbsp; Phong and Blinn&ndash;Phong"),
  ("table", ["", "Phong (1975)", "Blinn&ndash;Phong (1977)"],
   [["Construction", "Reflect the light direction about the normal, compare "
     "to the view.", "Compute the halfway vector between light and view, "
     "compare to the normal."],
    ["Formula", "(R &middot; V)&#8319; where R = reflect(&minus;L, N)",
     "(N &middot; H)&#8319; where H = normalize(L + V)"],
    ["Cost", "A reflect() per fragment.",
     "A normalize of a sum. Cheaper."],
    ["Grazing angles", "Highlight terminates abruptly.",
     "Highlight stretches and elongates — which is what real surfaces "
     "do."],
    ["Verdict", "Historical.",
     "Still the right classical choice, and the halfway vector returns in "
     "Module 11 as the microfacet normal."]],
   [0.14, 0.43, 0.43]),
  ("h2", "3.2 &nbsp; What is wrong with it"),
  ("callout", "Three real defects",
   ["<b>No energy conservation.</b> Increase the shininess exponent and total "
    "reflected energy changes arbitrarily. A surface can reflect more light "
    "than falls on it.",
    "<b>No Fresnel.</b> Every real surface becomes highly reflective at "
    "grazing angles — look along a sheet of paper and it is nearly a "
    "mirror. Blinn&ndash;Phong has no mechanism for this, so edges look flat "
    "and materials look like plastic.",
    "<b>No physical parameters.</b> 'Shininess 64' means nothing measurable, "
    "so materials must be retuned by hand whenever lighting changes. This is "
    "an enormous hidden cost in production.",
    "Module 11 fixes all three with a microfacet model. Learn "
    "Blinn&ndash;Phong anyway: it is cheap, it is in all existing code, and "
    "the better model is easiest to understand as a correction of these "
    "specific failures."]),

  ("break",),
  ("h1", "4 &nbsp; Shading frequency"),
  ("p", "A shading model says what to compute. Shading frequency says how "
        "often, and the choice produces three recognisably different images."),
  ("table", ["Model", "Evaluated", "Interpolated", "Result"],
   [["Flat", "Once per face", "Nothing",
     "Faceted appearance. Correct and desirable for genuinely flat surfaces; "
     "wrong for anything meant to look curved."],
    ["Gouraud", "Once per vertex", "The resulting colour",
     "Smooth gradients, but specular highlights distort badly and can "
     "disappear entirely."],
    ["Phong", "Once per fragment", "The normal",
     "Correct highlights at any triangle density. Costs one normalize and one "
     "shading evaluation per fragment. The default today."]],
   [0.13, 0.19, 0.22, 0.46]),
  ("p", "Gouraud's failure mode is the most instructive. A specular highlight "
        "falls off as a high power of a cosine — exponent 128 is "
        "ordinary — which makes it a very narrow function over the "
        "surface. Gouraud samples that function at exactly three points per "
        "triangle. If the highlight's peak falls between the vertices, it is "
        "never sampled and the highlight simply does not appear. As the object "
        "rotates, highlights pop into and out of existence as the peak crosses "
        "vertex positions."),
  ("p", "This is undersampling, which is the recurring theme of Module 01 "
        "appearing in a new place. The cure is to sample more often: evaluate "
        "per fragment instead of per vertex. Module 09 develops the general "
        "theory."),

  ("h1", "5 &nbsp; Gamma and the linear workflow"),
  ("p", "This section prevents more bad-looking renders than any other in the "
        "course, and the failure is insidious because the image does not look "
        "broken — it just looks wrong in a way that is hard to name."),
  ("h2", "5.1 &nbsp; The problem"),
  ("p", "Displays are not linear. An sRGB display emits luminance "
        "approximately proportional to the pixel value raised to 2.2. A value "
        "of 0.5 therefore emits about 21% of maximum brightness, not 50%. "
        "This curve exists for good reasons — human brightness perception "
        "is roughly logarithmic, so the encoding allocates more precision "
        "where the eye is more sensitive."),
  ("p", "The consequence is that image files are stored in this non-linear "
        "encoding. A texture painted by an artist on a calibrated display is "
        "sRGB-encoded. If you feed those values directly into lighting "
        "arithmetic, you are multiplying and adding perceptual values as "
        "though they were quantities of light. They are not, and the results "
        "are wrong in specific, recognisable ways: midtones too dark, shadows "
        "muddy, highlights blown out, and blended edges with a dark fringe."),
  ("h2", "5.2 &nbsp; The fix"),
  ("ol", ["<b>Decode on input.</b> Convert sRGB textures to linear before "
          "use. Use an sRGB texture format and the hardware does it free, "
          "including correctly filtered.",
          "<b>Compute in linear space.</b> All lighting, blending, and "
          "filtering happens on linear values.",
          "<b>Encode once on output.</b> Convert back to sRGB at the very "
          "end. <code>glEnable(GL_FRAMEBUFFER_SRGB)</code> does this free."]),
  ("callout", "The trap that survives code review",
   ["Only <b>colour</b> textures are sRGB-encoded: albedo, emissive, and "
    "anything an artist painted as a colour.",
    "Normal maps, roughness, metallic, ambient occlusion, height, and masks "
    "are <b>data</b>. They were never perceptual values, they were never "
    "encoded, and applying an sRGB decode to them corrupts them.",
    "A normal map tagged sRGB produces lighting that is subtly wrong "
    "everywhere and obviously wrong nowhere — which is why this error "
    "survives into shipped products."]),

  ("h1", "6 &nbsp; Attenuation"),
  ("p", "A point light radiates into a sphere. At distance d the energy is "
        "spread over 4&pi;d&#178;, so irradiance falls as 1/d&#178;. This is "
        "exact physics, not a model."),
  ("eq", "attenuation = 1 / (d&#178; + &epsilon;)"),
  ("p", "The &epsilon; avoids division by zero at the light's exact position. "
        "Directional lights — the sun — have no falloff at all: "
        "they are infinitely distant, which in homogeneous terms means w = 0, "
        "exactly as Module 02 described."),
  ("p", "Older engines frequently used linear or artist-tunable falloff "
        "curves, and the usual reason was that they were not gamma-correct: "
        "inverse-square looks far too harsh when applied to non-linear "
        "values. With a correct linear workflow, inverse-square is both "
        "correct and looks correct. If physically right falloff looks wrong in "
        "your renderer, suspect your gamma handling before you reach for a "
        "tunable curve."),
 ],
 "resources": [
   ("GAMES101 Lectures 07–09 — Shading",
    "https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html",
    "Lambert, Blinn–Phong, and the three shading frequencies, with the "
    "cosine-law derivation done geometrically."),
   ("John Hable — 'Why a Filmic Curve' and the gamma articles",
    "http://filmicworlds.com/blog/",
    "The clearest practical writing on linear workflow and tonemapping, from "
    "someone who shipped it."),
   ("LearnOpenGL — Basic Lighting and Gamma Correction",
    "https://learnopengl.com/Advanced-Lighting/Gamma-Correction",
    "The API mechanics of sRGB textures and framebuffers, with before/after "
    "images."),
   ("Naty Hoffman — 'Physics and Math of Shading' (SIGGRAPH course, free)",
    "https://blog.selfshadow.com/publications/s2013-shading-course/",
    "The best free introduction to radiometry for graphics. Read it before "
    "Module 11."),
 ],
 "exercises": [
   "Add Lambertian diffuse shading to your software rasterizer with a single "
   "point light and correct inverse-square attenuation.",
   "Implement Phong and Blinn&ndash;Phong side by side. Render a sphere lit "
   "at a grazing angle with both and capture the difference in highlight "
   "shape. Explain which is closer to a real surface and why.",
   "Implement flat, Gouraud, and Phong shading on the same low-polygon "
   "sphere. Use a shininess exponent of 128 and capture all three. Find a "
   "camera angle where the Gouraud highlight disappears entirely.",
   "Render the same scene with and without gamma correction. Then render a "
   "50% grey gradient both ways and measure the emitted values. Write two "
   "sentences on why the uncorrected version looks the way it does.",
   "Deliberately tag a normal map as sRGB and render. Describe the artifact "
   "precisely enough that you would recognise it in someone else's project.",
   "Verify energy conservation numerically: integrate your diffuse BRDF over "
   "the hemisphere and confirm it equals the albedo. Then do the same for "
   "Blinn&ndash;Phong and observe that it does not.",
 ],
 "selfcheck": [
   "Why do renderers transport radiance rather than irradiance or flux?",
   "Derive the cosine law from the geometry of a tilted surface, and explain "
   "why n &middot; l is not a material property.",
   "Where does the 1/&pi; in the Lambertian BRDF come from, and what breaks "
   "if you omit it?",
   "Give three specific defects of Blinn&ndash;Phong and say what each one "
   "looks like in a rendered image.",
   "Why can a Gouraud-shaded specular highlight disappear completely? What is "
   "the general principle this illustrates?",
   "State the three steps of a linear workflow, and list which texture types "
   "must not be sRGB-decoded.",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "The Programmable Pipeline: Shaders in Practice",
 "subtitle": "Moving everything you just built onto the GPU.",
 "question": "How does the pipeline you wrote by hand map onto real hardware?",
 "outcomes": [
     "Map each stage of your software rasterizer onto its GPU counterpart.",
     "Write vertex and fragment shaders and explain the data flow between "
     "them.",
     "Explain SIMD execution and why branching costs what it does.",
     "Use uniforms, buffers, and textures with an understanding of their cost.",
     "Capture and read a frame in RenderDoc.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The same pipeline, in silicon",
   "blurb": "Everything you wrote by hand, now fixed-function or "
            "massively parallel."},

  {"t": "table", "kicker": "Mapping", "title": "Your rasterizer, translated",
   "header": ["You wrote", "On the GPU it is", "Who controls it"],
   "widths": [4.1, 4.3, 3.7],
   "rows": [
     ["Your MVP multiply loop", "Vertex shader", "You — programmable"],
     ["Your clip and cull code", "Fixed-function", "Configured, not written"],
     ["Your edge-function loop", "Rasterizer", "Fixed-function, in hardware"],
     ["Your barycentric lerp", "Interpolators", "Declared via qualifiers"],
     ["Your shade() function", "Fragment shader", "You — programmable"],
     ["Your depth compare", "ROP / output merger", "Configured, not written"],
   ],
   "note": "The point of Project 1 is that nothing here is mysterious: they "
           "have already written every row."},

  {"t": "code", "kicker": "Minimal · 1 of 2", "title": "The vertex shader",
   "lang": "glsl", "code": """
#version 450 core

layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aNormal;

uniform mat4 uMVP;               // Module 03: P * V * M
uniform mat4 uModel;
uniform mat3 uNormalMatrix;      // Module 02: inverse transpose

out vec3 vWorldPos;              // interpolated for us, perspective-
out vec3 vNormal;                //   correctly, per Module 04

void main() {
    vWorldPos   = (uModel * vec4(aPos, 1.0)).xyz;
    vNormal     = uNormalMatrix * aNormal;
    gl_Position = uMVP * vec4(aPos, 1.0);
}
""",
   "caption": "Runs once per vertex. Its one obligation is to write "
              "<code>gl_Position</code> in clip space; everything else it "
              "writes becomes an interpolated input to the fragment shader.",
   "note": "Name the module each line came from. This is the payoff slide for "
           "the whole first half of the course."},

  {"t": "code", "kicker": "Minimal · 2 of 2", "title": "The fragment shader",
   "lang": "glsl", "code": """
#version 450 core

in  vec3 vWorldPos;
in  vec3 vNormal;
out vec4 fragColor;

uniform vec3 uLightPos, uLightColor, uAlbedo;

void main() {
    vec3  N  = normalize(vNormal);         // Module 02: renormalize
    vec3  Lv = uLightPos - vWorldPos;
    float d  = length(Lv);
    vec3  L  = Lv / d;

    vec3 c = uAlbedo / 3.14159             // Module 06: the 1/pi
           * uLightColor
           * max(dot(N, L), 0.0)           // Module 06: cosine law
           / (d * d);                      // Module 06: inverse square

    fragColor = vec4(c, 1.0);
}
""",
   "caption": "Runs once per fragment. Every line implements something from "
              "Modules 02–06 — nothing new is introduced here "
              "except the syntax.",
   "note": "The annotations are the point: they have already derived all of "
           "this. The GPU adds no new ideas, only a new execution model."},

  {"t": "section", "label": "Part 2", "title": "How the hardware runs this",
   "blurb": "Thousands of threads, executing in lockstep, whether you like "
            "it or not."},

  {"t": "bullets", "kicker": "SIMD", "title": "Threads execute in lockstep groups",
   "items": [
     "Fragments are grouped into <b>warps</b> or <b>waves</b> of 32 or 64.",
     "All threads in a group execute the <b>same instruction</b> at the same "
     "time, on different data.",
     "",
     "A branch where threads disagree must execute <b>both sides</b>.",
     ("Threads take the branch they need; the others are masked off and idle.", 1),
     ("Cost = cost of both branches, not the average. This is <b>divergence</b>.", 1),
     "",
     "A branch where the whole group agrees is nearly free.",
     ("Branching on a uniform is fine. Branching per-pixel on noise is not.", 1),
   ],
   "note": "Connect forward to CSCE 735, which treats this properly. Here "
           "they need the practical rule only."},

  {"t": "two", "kicker": "Divergence", "title": "Branching: cheap and expensive",
   "lh": "Nearly free",
   "l": ["Branch on a uniform — same for every thread.",
         "Branch on a value constant across a whole triangle.",
         "Early-out that an entire tile takes together.",
         ("The group agrees, so only one path executes.", 1)],
   "rh": "Expensive",
   "r": ["Branch on a texture sample that varies per pixel.",
         "Branch on screen position in a fine pattern.",
         "Loops whose trip count varies per pixel.",
         ("The group disagrees, so every path executes and most lanes sit "
          "idle.", 1)],
   "note": "Practical heuristic: ask 'would all 32 neighbouring pixels make "
           "the same decision?' If yes, branch freely."},

  {"t": "callout", "title": "Quads, derivatives, and why discard is costly",
   "kind": "Mechanism",
   "body": ["Fragments are always shaded in 2×2 <b>quads</b>, even at a "
            "triangle's edge where only one of the four is covered.",
            "This is how <code>dFdx</code> and <code>dFdy</code> work: the "
            "derivative is the difference between neighbouring threads in the "
            "quad. Texture mipmap selection (Module 08) depends on it.",
            "Consequence: small triangles waste up to 75% of shading work on "
            "helper lanes. This is why dense meshes get disproportionately "
            "expensive, and why nanite-style approaches matter.",
            "Consequence: <code>discard</code> cannot free its lane, because "
            "the neighbours still need it for derivatives."]},

  {"t": "section", "label": "Part 3", "title": "Feeding the machine",
   "blurb": "Where data comes from, and what each route costs."},

  {"t": "table", "kicker": "Data", "title": "Ways to get data into a shader",
   "header": ["Mechanism", "Changes", "Use for", "Cost"],
   "widths": [2.6, 2.4, 3.9, 3.2],
   "rows": [
     ["Vertex attribute", "Per vertex", "Position, normal, UV, tangent", "Cheap; fixed layout"],
     ["Uniform", "Per draw", "Matrices, light params, material constants", "Cheapest to read"],
     ["Uniform buffer (UBO)", "Per draw/frame", "Grouped constants, camera data", "Cheap; size-limited"],
     ["Storage buffer (SSBO)", "Anytime", "Large arrays, instance data", "Slower; unbounded"],
     ["Texture", "Per draw", "Images, lookup tables, data maps", "Cached; filtering free"],
   ]},

  {"t": "bullets", "kicker": "Cost", "title": "What actually makes frames slow",
   "items": [
     "<b>State changes and draw calls</b> — usually the CPU-side "
     "bottleneck. Batch aggressively.",
     "<b>Overdraw</b> — shading fragments that get covered. Sort "
     "front-to-back; use a depth pre-pass.",
     "<b>Bandwidth</b> — reading textures and writing targets. Often "
     "dominant at high resolution.",
     "<b>Divergence and occupancy</b> — idle lanes, or too few threads "
     "in flight because registers ran out.",
     "",
     "<b>Rarely the arithmetic.</b> Counting ALU instructions is almost never "
     "where the win is.",
   ],
   "footnote": "Measure before optimising. The bottleneck is seldom where "
               "intuition puts it.",
   "note": "This is the single most important practical slide in the second "
           "half of the course."},

  {"t": "section", "label": "Part 4", "title": "Reading a frame",
   "blurb": "RenderDoc is not a debugging tool of last resort. It is how you "
            "see what the GPU did."},

  {"t": "bullets", "kicker": "RenderDoc", "title": "What to look at, in order",
   "items": [
     "<b>Event browser</b> — every draw call in order. How many? Is "
     "anything drawn twice?",
     "<b>Texture viewer</b> — inspect any render target or texture at "
     "any point in the frame.",
     "<b>Pipeline state</b> — what was actually bound. Most 'shader "
     "bugs' are binding bugs.",
     "<b>Mesh viewer</b> — vertex data in and out. Catches bad "
     "matrices immediately.",
     "<b>Shader debugger</b> — step a single pixel's fragment shader, "
     "watching every variable.",
     "",
     "Black screen? Check the mesh viewer output first. Nine times in ten the "
     "vertices are not where you think.",
   ],
   "note": "Make them capture a frame in this module, not later. The skill "
           "compounds across every remaining module."},

  {"t": "table", "kicker": "Diagnosis", "title": "GPU-specific bugs",
   "header": ["Symptom", "Usual cause"],
   "widths": [5.3, 6.8],
   "rows": [
     ["Black screen, geometry is correct in mesh viewer", "Shader compile failed silently — check the info log"],
     ["Everything one flat colour", "Uniform not found: a typo, or optimised out as unused"],
     ["Works on your GPU, breaks elsewhere", "Undefined behaviour: uninitialised variable, or relying on a driver quirk"],
     ["Correct at distance, wrong up close", "Interpolation qualifier — flat vs smooth"],
     ["Lighting dark toward triangle centres", "Interpolated normal not renormalized (Module 02)"],
     ["Sudden frame-time cliff after a small edit", "Early-Z disabled, or register pressure dropped occupancy"],
   ]},
 ],
 "takeaways": [
   "The GPU pipeline is the pipeline you already wrote: some stages became "
   "fixed-function, two became programmable.",
   "Threads run in lockstep groups. A divergent branch executes both sides, "
   "so cost is the sum, not the average.",
   "Fragments shade in 2×2 quads for derivatives, so small triangles "
   "waste most of their shading work on helper lanes.",
   "Choose your data path by update frequency: attribute, uniform, UBO, SSBO, "
   "texture.",
   "Frames are slow because of draw calls, overdraw, bandwidth, and "
   "occupancy. Almost never because of arithmetic.",
   "Learn RenderDoc now. Most 'shader bugs' are binding bugs, and the "
   "pipeline state view shows them instantly.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The same pipeline, in hardware"),
  ("p", "Project 1 built every stage by hand. Moving to the GPU changes who "
        "executes each stage, not what the stages are. That is the whole "
        "pedagogical reason for doing the software rasterizer first: nothing "
        "below is new."),
  ("table", ["In your software rasterizer", "On the GPU", "Your control"],
   [["The loop applying P&middot;V&middot;M to each vertex", "Vertex shader",
     "Fully programmable."],
    ["Your near-plane clip and backface test", "Fixed-function clip/cull",
     "Configured through state, not written."],
    ["Your edge-function coverage loop", "Rasterizer",
     "None. Dedicated silicon, with a specified fill rule."],
    ["Your perspective-correct barycentric lerp", "Interpolators",
     "Controlled by qualifiers (<code>smooth</code>, <code>flat</code>, "
     "<code>noperspective</code>)."],
    ["Your shade() function", "Fragment shader", "Fully programmable."],
    ["Your depth compare and write", "ROP / output merger",
     "Configured through depth and blend state."]],
   [0.34, 0.24, 0.42]),

  ("h1", "2 &nbsp; Shader anatomy"),
  ("p", "A vertex shader runs once per vertex and must write "
        "<code>gl_Position</code> in clip space. Anything else it writes "
        "becomes a per-vertex output, which the rasterizer interpolates "
        "across the triangle — with perspective correction, exactly as "
        "derived in Module 04 — and delivers to the fragment shader."),
  ("code", """// ---- vertex ----
#version 450 core
layout(location=0) in vec3 aPos;
layout(location=1) in vec3 aNormal;

uniform mat4 uMVP, uModel;
uniform mat3 uNormalMatrix;

out vec3 vWorldPos;
out vec3 vNormal;

void main() {
    vWorldPos   = (uModel * vec4(aPos, 1.0)).xyz;
    vNormal     = uNormalMatrix * aNormal;   // Module 02
    gl_Position = uMVP * vec4(aPos, 1.0);    // Module 03
}

// ---- fragment ----
#version 450 core
in  vec3 vWorldPos, vNormal;
out vec4 fragColor;
uniform vec3 uLightPos, uLightColor, uAlbedo;

void main() {
    vec3  N = normalize(vNormal);            // Module 02: renormalize
    vec3  Lv = uLightPos - vWorldPos;
    float d = length(Lv);
    vec3  L = Lv / d;
    vec3  c = uAlbedo / 3.14159             // Module 06: the 1/pi
            * uLightColor
            * max(dot(N, L), 0.0)            // Module 06: cosine law
            / (d * d);                       // Module 06: inverse square
    fragColor = vec4(c, 1.0);
}"""),
  ("h2", "2.1 &nbsp; Interpolation qualifiers"),
  ("table", ["Qualifier", "Behaviour", "Use for"],
   [["<code>smooth</code> (default)", "Perspective-correct interpolation",
     "Almost everything: normals, UVs, world position."],
    ["<code>noperspective</code>", "Screen-space linear",
     "Quantities already in screen space — rare, but exactly right when "
     "you need it."],
    ["<code>flat</code>", "No interpolation; takes the provoking vertex's "
     "value",
     "Integer IDs, material indices, face normals. Interpolating an integer "
     "index is meaningless, and <code>flat</code> is how you say so."]],
   [0.22, 0.34, 0.44]),

  ("h1", "3 &nbsp; How the hardware executes shaders"),
  ("h2", "3.1 &nbsp; Lockstep execution"),
  ("p", "Shader threads are grouped into warps (NVIDIA, 32 threads) or waves "
        "(AMD, 32 or 64). Every thread in a group executes the same "
        "instruction at the same time on different data. This is what makes "
        "GPUs cheap per unit of arithmetic: one instruction decoder drives "
        "thirty-two lanes."),
  ("p", "The consequence is <b>divergence</b>. If threads within a group "
        "would take different branches, the hardware executes both branches, "
        "masking off the lanes that are not taking each one. The cost is "
        "therefore the <i>sum</i> of the branches, not the average, and the "
        "masked lanes do no useful work."),
  ("callout", "The practical rule",
   ["Before writing a branch in a fragment shader, ask: <i>would all 32 "
    "neighbouring pixels make the same decision?</i>",
    "If yes — branching on a uniform, on a per-draw constant, on "
    "something spatially coherent — the branch is nearly free and may "
    "save a great deal.",
    "If no — branching on a noise texture, on a per-pixel random value, "
    "on a fine checkerboard — you pay for every path and gain nothing. "
    "Prefer arithmetic selection (<code>mix</code>, <code>step</code>) in "
    "that case."]),
  ("h2", "3.2 &nbsp; Quads and derivatives"),
  ("p", "Fragments are always shaded in 2&times;2 quads, because screen-space "
        "derivatives are computed as differences between neighbouring threads "
        "in the quad. <code>dFdx(v)</code> is literally the difference "
        "between this thread's <i>v</i> and its horizontal neighbour's. "
        "Mipmap level selection (Module 08) depends entirely on this "
        "mechanism, which is why texture sampling inside non-uniform control "
        "flow is undefined."),
  ("p", "Two important consequences follow. First, at a triangle edge where "
        "only one fragment of a quad is covered, the other three still "
        "execute as <b>helper lanes</b> and their results are thrown away. "
        "A triangle covering a single pixel costs four fragment-shader "
        "invocations — a 4&times; waste. This is why very dense meshes "
        "become disproportionately expensive, and why micropolygon rendering "
        "needs a different architecture. Second, <code>discard</code> cannot "
        "free its lane, because the neighbours still need it for their "
        "derivatives."),

  ("break",),
  ("h1", "4 &nbsp; Getting data to the GPU"),
  ("p", "Choose the mechanism by how often the data changes. Using a slower "
        "path than necessary is a common and avoidable cost; using a faster "
        "path than the data allows produces stale results."),
  ("table", ["Mechanism", "Update frequency", "Typical contents", "Notes"],
   [["Vertex attribute", "Per vertex", "Position, normal, UV, tangent, colour",
     "Fixed layout declared at pipeline creation."],
    ["Uniform", "Per draw call", "MVP, light parameters, material scalars",
     "Cheapest to read. Unused uniforms are optimised out, and then "
     "<code>glGetUniformLocation</code> returns &minus;1 — a frequent "
     "source of confusion."],
    ["Uniform buffer (UBO)", "Per draw or per frame",
     "Grouped constants: camera block, light block",
     "Beware std140 layout rules; a vec3 occupies 16 bytes."],
    ["Storage buffer (SSBO)", "Any time, read/write",
     "Large arrays, per-instance transforms, compute results",
     "Unbounded size, but slower access than uniforms."],
    ["Texture", "Per draw", "Images, lookup tables, data maps",
     "Hardware filtering and caching are free. Often the fastest way to read "
     "a large table."]],
   [0.18, 0.17, 0.33, 0.32]),

  ("h1", "5 &nbsp; What actually costs time"),
  ("p", "Graphics performance intuition is unreliable, and arithmetic is "
        "almost never the answer. In rough order of how often each one turns "
        "out to be the real bottleneck:"),
  ("ol", ["<b>Draw calls and state changes.</b> CPU-side overhead per call is "
          "substantial. Thousands of small draws will bottleneck the CPU "
          "while the GPU idles.",
          "<b>Overdraw.</b> Fragments shaded and then covered. Sort opaque "
          "front-to-back; consider a depth pre-pass when fragment shaders are "
          "expensive.",
          "<b>Bandwidth.</b> Texture reads and render-target writes. Usually "
          "dominant at high resolution, and the reason for compressed "
          "textures and smaller render targets.",
          "<b>Occupancy.</b> A shader using too many registers reduces how "
          "many threads can be resident, which reduces the GPU's ability to "
          "hide memory latency. A small shader edit can push you over a "
          "threshold and cause a sudden frame-time cliff.",
          "<b>Divergence.</b> Idle lanes in divergent branches.",
          "<b>Arithmetic.</b> Last, and usually by a wide margin."]),
  ("callout", "Measure first",
   ["Every item above is observable. RenderDoc gives you draw counts, state, "
    "and per-draw timings; vendor tools (Nsight, Radeon GPU Profiler) give "
    "you occupancy and bandwidth.",
    "Optimising a shader's instruction count when the frame is "
    "bandwidth-bound is a way to spend a day and gain nothing. This happens "
    "constantly."]),

  ("h1", "6 &nbsp; Reading a frame in RenderDoc"),
  ("p", "Frame capture is not a tool of last resort; it is the normal way to "
        "find out what the GPU did. Learn it now, because every remaining "
        "module benefits."),
  ("ul", ["<b>Event browser</b> — every draw call in submission order. "
          "Check the count, and look for geometry drawn more than once.",
          "<b>Texture viewer</b> — inspect any render target at any "
          "point in the frame. Essential for shadow maps (Module 10) and any "
          "multi-pass effect.",
          "<b>Pipeline state</b> — what was actually bound when the draw "
          "executed. The majority of apparent shader bugs are binding bugs, "
          "and this view shows them in seconds.",
          "<b>Mesh viewer</b> — vertex buffer contents before and after "
          "the vertex shader. If the screen is black, look here first: nine "
          "times out of ten the vertices are not where you believe.",
          "<b>Shader debugger</b> — pick a pixel and step through its "
          "fragment shader, watching every intermediate value."]),
  ("table", ["Symptom", "Usual cause", "Where to look"],
   [["Black screen, mesh viewer output looks right",
     "Shader failed to compile and you did not check the log.",
     "Compile log; pipeline state."],
    ["Everything renders one flat colour",
     "Uniform location is &minus;1 — name typo, or the uniform was "
     "optimised out because it is unused.", "Pipeline state."],
    ["Correct on your machine, wrong on another",
     "Undefined behaviour: uninitialised variable, or depending on a "
     "driver-specific default.", "Shader source; validation layers."],
    ["Correct far away, wrong close up",
     "Wrong interpolation qualifier, or a precision issue.",
     "Shader source."],
    ["Dark patches toward the middle of large triangles",
     "Interpolated normals not renormalized (Module 02).",
     "Fragment shader."],
    ["Frame time collapsed after a trivial edit",
     "Early-Z disabled by a new <code>discard</code>, or register pressure "
     "reduced occupancy.", "Vendor profiler."]],
   [0.28, 0.44, 0.28]),
 ],
 "resources": [
   ("Cem Yuksel — Interactive Computer Graphics (Utah), GPU pipeline "
    "lectures",
    "https://graphics.cs.utah.edu/courses/cs6610/",
    "The best free treatment of the programmable pipeline and the API layer. "
    "Primary source from this module onward."),
   ("LearnOpenGL — Getting Started and Lighting sections",
    "https://learnopengl.com/",
    "Mechanics: context creation, buffers, shader compilation, uniforms. Use "
    "for the API, not for the theory."),
   ("Fabian Giesen — 'A trip through the Graphics Pipeline'",
    "https://fgiesen.wordpress.com/2011/07/09/a-trip-through-the-graphics-pipeline-2011-index/",
    "What the hardware is actually doing at each stage. The best free "
    "writing on the subject."),
   ("RenderDoc documentation and quick-start",
    "https://renderdoc.org/docs/getting_started/quick_start.html",
    "Work through this once with a real capture. It pays for itself within "
    "the week."),
   ("The Book of Shaders",
    "https://thebookofshaders.com/",
    "Fragment-shader intuition through small interactive examples. Good for "
    "building fluency in the language itself."),
 ],
 "exercises": [
   "Port your Project 1 scene to OpenGL: same mesh, same camera, same "
   "lighting. Render both and diff the images. Explain every remaining "
   "difference — there will be some, and each one is informative.",
   "Write a shader with a branch on a uniform and the same shader with the "
   "branch on a high-frequency noise texture. Measure both. Report the "
   "frame-time difference and explain it in terms of divergence.",
   "Visualise the quad overshading: render a mesh with triangles around one "
   "pixel in size and use <code>dFdx</code>/<code>dFdy</code> of a screen-"
   "space value to shade helper lanes differently. Observe the waste "
   "directly.",
   "Capture a frame of your own renderer in RenderDoc. Write a short "
   "annotation of what each draw call contributes, and find one thing you did "
   "not know your renderer was doing.",
   "Deliberately introduce three bugs — a typo in a uniform name, a "
   "missing <code>normalize</code>, and an sRGB-tagged normal map — and "
   "practise diagnosing each from the image alone before confirming in "
   "RenderDoc.",
 ],
 "selfcheck": [
   "Map each of the six pipeline stages onto what you wrote in Project 1, and "
   "say which became fixed-function.",
   "What does a divergent branch cost, and why? Give an example of a branch "
   "that is nearly free.",
   "Why are fragments shaded in 2&times;2 quads, and what two consequences "
   "does that have for performance?",
   "When would you use <code>flat</code> interpolation, and what goes wrong "
   "if you use <code>smooth</code> instead?",
   "List four things more likely than arithmetic to be your frame's "
   "bottleneck.",
   "<code>glGetUniformLocation</code> returns &minus;1 for a uniform you can "
   "see in the shader source. Give two possible explanations.",
 ],
},

]
