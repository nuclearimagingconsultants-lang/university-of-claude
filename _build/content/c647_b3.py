# -*- coding: utf-8 -*-
"""CSCE 647 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Path Tracing and Multiple Importance Sampling",
 "subtitle": "The algorithm, and the fifteen lines that make it usable.",
 "question": "How do you actually estimate the rendering equation?",
 "outcomes": [
     "Implement a correct unidirectional path tracer.",
     "Explain next-event estimation and why it is not optional.",
     "Derive the MIS estimator and the balance and power heuristics.",
     "Explain exactly why naive NEE plus BSDF sampling double-counts.",
     "Diagnose path tracer bugs from the images they produce.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The naive path tracer",
   "blurb": "Correct, and unusable."},

  {"t": "code", "kicker": "Naive", "title": "Path tracing in fifteen lines",
   "lang": "cpp", "code": """
vec3 radiance(Ray r, Scene& s) {
    vec3 L(0), throughput(1);
    for (int depth = 0; ; depth++) {
        Hit h;
        if (!s.intersect(r, h)) { L += throughput * s.env(r.d); break; }

        L += throughput * h.emission();            // did we hit a light?

        auto [wi, f, pdf, flags] = h.bsdf->sample(-r.d, rng.next2D());
        if (pdf <= 0) break;
        throughput *= f * fabs(dot(wi, h.ns)) / pdf;

        if (depth > 3) {                           // Russian roulette
            float q = fmaxf(0.05f, 1.0f - throughput.max());
            if (rng.next() < q) break;
            throughput /= (1.0f - q);
        }
        r = Ray(offset(h.p, h.ng), wi);
    }
    return L;
}
""",
   "caption": "This is complete and unbiased. Every term of the Neumann "
              "series is sampled with the correct probability.",
   "note": "Show it runs and produces a correct image before criticising "
           "it. The criticism lands harder."},

  {"t": "callout", "title": "It is correct and it is useless",
   "kind": "The problem",
   "body": ["A path contributes only if it <b>randomly happens to land on a "
            "light</b>.",
            "For a light subtending 0.01 steradians, that is about 1 in 600 "
            "samples. For a point light, <b>the probability is exactly "
            "zero</b> — the image is black forever.",
            "The 599 paths that miss contribute nothing but cost full "
            "price.",
            "<b>Smaller and brighter lights make this worse in both "
            "directions:</b> rarer hits, and larger values when they do hit. "
            "Variance explodes exactly where lighting artists want to "
            "work."]},

  {"t": "section", "label": "Part 2", "title": "Next-event estimation",
   "blurb": "Stop waiting for the path to find a light."},

  {"t": "callout", "title": "At every vertex, sample a light directly",
   "kind": "The fix",
   "body": ["At each surface, pick a point on a light, trace a shadow ray, "
            "and add its contribution — using the <b>area form</b> of "
            "Module 02, with the geometry term.",
            "<b>Then continue the path as before</b>, but no longer count "
            "emission when the continuation happens to hit a light, because "
            "that contribution was already taken.",
            "Point lights now work. Small lights converge in a handful of "
            "samples rather than thousands.",
            "<b>The cost is one shadow ray per vertex</b>, which is why "
            "Module 03's dedicated <code>occluded()</code> path matters — "
            "shadow rays are now the majority of all rays cast."]},

  {"t": "callout", "title": "And now it fails on glossy surfaces",
   "kind": "The new problem",
   "body": ["On a near-mirror surface, the sampled light point is almost "
            "never inside the narrow BSDF lobe. <b>The contribution is "
            "essentially always zero.</b>",
            "Meanwhile the BSDF-sampled continuation lands beautifully in "
            "the lobe — and we just told it not to count emission.",
            "<b>So NEE alone is worse than naive path tracing for sharp "
            "reflections of lights.</b> Glossy highlights disappear.",
            "<b>This is exactly the complementary failure of Module 02.</b> "
            "Two strategies, each excellent where the other collapses. "
            "Neither is sufficient, and the obvious fix — use both — "
            "double-counts."]},

  {"t": "section", "label": "Part 3", "title": "Multiple importance sampling",
   "blurb": "Veach 1995. The most valuable fifteen lines in rendering."},

  {"t": "eq", "kicker": "MIS", "title": "Combining strategies without double-counting",
   "eqs": [
     ("F  =  Σₛ (1/nₛ) Σᵢ wₛ(Xₛᵢ) f(Xₛᵢ) / pₛ(Xₛᵢ)",
      "Sum over strategies s, with a weighting function w applied to each "
      "sample."),
     ("Σₛ wₛ(x)  =  1   for every x with f(x) ≠ 0",
      "The only condition for unbiasedness. Any weights summing to one "
      "work."),
     ("wₛ(x)  =  nₛ pₛ(x) / Σₜ nₜ pₜ(x)",
      "The balance heuristic. Provably within a small additive constant of "
      "optimal."),
   ],
   "caption": "The weight asks: of all the strategies, how likely was *this* "
              "one to have generated this sample?",
   "note": "The intuition is the whole thing: a sample is trusted in "
           "proportion to how well-suited the strategy that found it was."},

  {"t": "callout", "title": "Why the weights fix double-counting exactly",
   "kind": "The intuition",
   "body": ["A direction reachable by both strategies gets sampled by both, "
            "so it would be counted twice.",
            "<b>MIS splits the credit</b>: each strategy's weight is its "
            "share of the total probability density at that point. The "
            "shares sum to one, so the direction is counted exactly once.",
            "<b>And the split is adaptive.</b> Near a small light, light "
            "sampling has the far higher density and takes almost all the "
            "weight. In a glossy lobe, BSDF sampling dominates and takes "
            "almost all of it.",
            "<b>Nobody told it which case it is in.</b> The densities "
            "themselves carry that information, which is why it is robust."]},

  {"t": "code", "kicker": "Implementation", "title": "The power heuristic in practice",
   "lang": "cpp", "code": """
// Veach's power heuristic, beta = 2. Slightly better than the balance
// heuristic in practice -- it suppresses low-weight samples harder.
inline float mis_weight(float pdf_a, float pdf_b) {
    float a = pdf_a * pdf_a, b = pdf_b * pdf_b;
    return a / (a + b);
}

// --- At a surface vertex -------------------------------------------------
// 1. SAMPLE THE LIGHT. Weight by how likely the BSDF was to find it.
auto [wi_L, Li, pdf_L] = scene.sample_light(h.p, rng.next2D());
if (pdf_L > 0 && !scene.occluded(h.p, wi_L)) {
    float pdf_B = h.bsdf->pdf(-r.d, wi_L);         // NOT a second sample
    float w     = mis_weight(pdf_L, pdf_B);
    L += throughput * w * h.bsdf->f(-r.d, wi_L)
                        * fabs(dot(wi_L, h.ns)) * Li / pdf_L;
}

// 2. SAMPLE THE BSDF. If it lands on a light, weight it symmetrically.
auto [wi_B, f, pdf_B, flags] = h.bsdf->sample(-r.d, rng.next2D());
// ... trace, and at the next hit, if it emits:
if (next.emits()) {
    float pdf_L2 = specular ? 0.0f               // delta: light sampling
                            : scene.pdf_light(h.p, wi_B);  // could not find it
    float w      = mis_weight(pdf_B, pdf_L2);
    L += throughput * w * next.emission();
}
""",
   "caption": "Specular lobes set the other strategy's PDF to zero, giving "
              "weight 1. That single line is how delta BSDFs stay correct.",
   "note": "The specular case is the bug everyone hits: without it, mirrors "
           "lose their reflected highlights entirely."},

  {"t": "table", "kicker": "Result", "title": "Variance by configuration",
   "header": ["Scene", "BSDF only", "Light only", "MIS"],
   "widths": [4.0, 2.7, 2.7, 2.7],
   "rows": [
     ["Small light, diffuse", "Terrible", "<b>Excellent</b>", "<b>Excellent</b>"],
     ["Large light, glossy", "<b>Excellent</b>", "Terrible", "<b>Excellent</b>"],
     ["Medium light, medium gloss", "Poor", "Poor", "<b>Good</b>"],
     ["Specular reflection of a light", "<b>Only option</b>", "Zero", "<b>Correct</b>"],
   ],
   "footnote": "The third row is the real argument: MIS beats <i>both</i> "
               "strategies where neither alone is adequate.",
   "note": "Row 3 is the one to emphasise. MIS is not just a selector — "
           "it genuinely outperforms both inputs."},

  {"t": "section", "label": "Part 4", "title": "Debugging",
   "blurb": "What each failure looks like."},

  {"t": "table", "kicker": "Diagnosis", "title": "Reading path tracer bugs",
   "header": ["Symptom", "Likely cause"],
   "widths": [5.4, 6.7],
   "rows": [
     ["Too bright, roughly 2&times; in lit areas", "<b>Double counting — MIS weights missing</b>"],
     ["Glossy highlights missing", "<b>Specular MIS case not handled</b>"],
     ["Black image with point lights", "No NEE"],
     ["Dark speckle everywhere", "Self-intersection (Module 03)"],
     ["Bright edge pixels on silhouettes", "Not watertight (Module 03)"],
     ["Too dark, worse at high roughness", "<b>Microfacet energy loss (Module 07)</b>"],
     ["Brightens the longer it runs", "Energy-creating BRDF"],
     ["Converges to the wrong answer", "Bias: clamp or bounce limit"],
   ],
   "note": "This table is the most-referenced slide in the module. Tell them "
           "to keep it open while implementing Project 1."},

  {"t": "callout", "title": "Validate component by component",
   "kind": "Method",
   "body": ["<b>Direct lighting only, diffuse only, one light.</b> Compare "
            "against an analytic solution. This must be exact.",
            "<b>Then add indirect.</b> Compare against PBRT on the same "
            "scene; the difference image should be noise with no "
            "structure.",
            "<b>Then add each BSDF.</b> Furnace test each one before it "
            "enters a scene.",
            "<b>Then enable MIS</b> and confirm the converged image is "
            "<i>unchanged</i> while the variance drops. <b>MIS must not "
            "change the answer</b> — if it does, the weights are wrong."]},
 ],
 "takeaways": [
   "The naive path tracer is fifteen lines, correct, and unusable — it "
   "needs a path to randomly hit a light, which never happens for a point "
   "light.",
   "Next-event estimation samples a light at every vertex, making small and "
   "point lights work, at the cost of a shadow ray per vertex.",
   "NEE alone then fails on glossy surfaces, where the light point is never "
   "in the BSDF lobe — the complementary failure from Module 02.",
   "MIS combines strategies with weights that sum to one, which is the only "
   "requirement for unbiasedness.",
   "The balance heuristic weights each strategy by its share of total "
   "density, which adapts automatically without being told the scene type.",
   "Specular lobes take weight 1 by setting the other strategy's PDF to "
   "zero. Omitting this loses all reflected highlights.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The naive path tracer"),
  ("p", "The algorithm follows directly from Module 02's Neumann series: "
        "sample paths of every length with the correct probability and "
        "average. The entire integrator fits on one screen."),
  ("code", """vec3 radiance(Ray r, Scene& s) {
    vec3 L(0), throughput(1);
    for (int depth = 0; ; depth++) {
        Hit h;
        if (!s.intersect(r, h)) { L += throughput * s.env(r.d); break; }
        L += throughput * h.emission();

        auto [wi, f, pdf, flags] = h.bsdf->sample(-r.d, rng.next2D());
        if (pdf <= 0) break;
        throughput *= f * fabs(dot(wi, h.ns)) / pdf;

        if (depth > 3) {
            float q = fmaxf(0.05f, 1.0f - throughput.max());
            if (rng.next() < q) break;
            throughput /= (1.0f - q);
        }
        r = Ray(offset(h.p, h.ng), wi);
    }
    return L;
}"""),
  ("p", "This is complete and unbiased. The throughput accumulates the "
        "product of f&middot;cos/pdf at each vertex — exactly the "
        "Monte Carlo weight for that path — and Russian roulette "
        "(Module 06) terminates without truncation bias. Run it on a scene "
        "with a large area light and it produces a correct image."),
  ("callout", "Correct, and unusable",
   ["A path contributes nothing unless it <b>randomly happens to hit a light "
    "source</b>. The probability of that depends entirely on how much of the "
    "hemisphere the light occupies.",
    "A light subtending 0.01 steradians is hit by roughly 1 in 600 "
    "cosine-weighted samples. The other 599 cost full price and return "
    "zero. For a <b>point light the probability is exactly zero</b> and the "
    "image is black no matter how long you run it.",
    "<b>The situation gets worse in both directions simultaneously.</b> As a "
    "light gets smaller, hits become rarer <i>and</i> — since a small "
    "light must be brighter to deliver the same illumination — each "
    "hit returns a larger value. Variance is the product of these, so it "
    "grows faster than either.",
    "Which is unfortunate, because small bright lights are what lighting "
    "artists use: they produce crisp shadows and controlled falloff. The "
    "naive algorithm is worst exactly where the demand is."]),

  ("h1", "2 &nbsp; Next-event estimation"),
  ("p", "Rather than hoping a path finds a light, sample one deliberately. "
        "At every surface vertex, choose a point on a light source, trace a "
        "shadow ray to it, and add its contribution using the <b>area "
        "form</b> of the rendering equation from Module 02 — with the "
        "geometry term converting the light's area measure into solid "
        "angle."),
  ("p", "The path then continues as before by sampling the BSDF, but "
        "<b>emission is no longer counted when the continuation happens to "
        "strike a light</b>, because that contribution was already accounted "
        "for by the explicit light sample at the previous vertex. Counting "
        "both would double it."),
  ("table", ["", "Before NEE", "After NEE"],
   [["Point lights", "<b>Impossible.</b> Probability exactly zero.",
     "Work correctly."],
    ["Small area lights", "Thousands of samples to converge.",
     "A handful."],
    ["Cost per vertex", "One BSDF sample.",
     "One BSDF sample <b>plus one shadow ray</b>."],
    ["Rays cast", "Mostly continuation rays.",
     "<b>Mostly shadow rays</b> — which is why Module 03's dedicated "
     "<code>occluded()</code> path is now worth its 2&ndash;3&times;."]],
   [0.17, 0.41, 0.42]),
  ("callout", "And now glossy surfaces break",
   ["Consider a near-mirror surface. Its BSDF lobe is extremely narrow: only "
    "directions within a degree or two of the mirror direction have any "
    "significant value.",
    "<b>The sampled light point is almost never in that lobe.</b> The BSDF "
    "evaluates to essentially zero, so the explicit light sample contributes "
    "nothing — at the cost of a shadow ray, every time.",
    "Meanwhile, the BSDF-sampled continuation lands precisely in the lobe "
    "and may well strike the light — and we have just instructed it "
    "not to count emission.",
    "<b>So NEE alone is strictly worse than naive path tracing for sharp "
    "reflections of light sources.</b> Glossy highlights vanish entirely. "
    "This is precisely the complementary failure identified in Module 02: "
    "two strategies, each excellent exactly where the other collapses, and "
    "the obvious combination — use both and add — double-counts "
    "every direction both can reach."]),

  ("break",),
  ("h1", "3 &nbsp; Multiple importance sampling"),
  ("p", "Veach and Guibas, 1995. The solution combines several sampling "
        "strategies with per-sample weights, and it is both simple and "
        "provably close to optimal."),
  ("eq", "F = &Sigma;<sub>s</sub> (1/n<sub>s</sub>) "
         "&Sigma;<sub>i</sub> w<sub>s</sub>(X<sub>s,i</sub>) "
         "f(X<sub>s,i</sub>) / p<sub>s</sub>(X<sub>s,i</sub>)"),
  ("p", "where s indexes the strategies, n<sub>s</sub> is the number of "
        "samples taken with strategy s, and w<sub>s</sub> is a weighting "
        "function. <b>The estimator is unbiased for any weights satisfying "
        "a single condition:</b>"),
  ("eq", "&Sigma;<sub>s</sub> w<sub>s</sub>(x) = 1 &nbsp;&nbsp; for every x "
         "with f(x) &ne; 0"),
  ("p", "That is the whole requirement. Any set of weights summing to one "
        "gives a correct answer; the choice affects variance only — "
        "the same structure as the choice of p in Module 05."),
  ("eq", "w<sub>s</sub>(x) = n<sub>s</sub> p<sub>s</sub>(x) / "
         "&Sigma;<sub>t</sub> n<sub>t</sub> p<sub>t</sub>(x) "
         "&nbsp;&nbsp;&nbsp;&nbsp;(balance heuristic)"),
  ("callout", "What the weights are doing",
   ["Each strategy's weight at a point is <b>its share of the total "
    "probability density</b> that the strategies collectively assign there. "
    "The shares sum to one by construction, so a direction both strategies "
    "can reach is counted exactly once.",
    "<b>The split is adaptive, and nobody has to classify the scene.</b> "
    "Near a small light, the light-sampling density is enormous and the BSDF "
    "density is small, so light sampling receives nearly all the weight. "
    "Inside a tight specular lobe, the reverse holds.",
    "<b>The densities themselves carry the information about which strategy "
    "is appropriate</b>, which is why MIS needs no heuristics about light "
    "size or material roughness and does not fail on configurations nobody "
    "anticipated.",
    "Veach proved the balance heuristic is within a small additive constant "
    "of the variance of the best possible weighting — so there is "
    "very little left on the table."]),
  ("p", "The <b>power heuristic</b> raises each density to a power (&beta; = "
        "2 in practice) before normalising. It suppresses low-weight samples "
        "more aggressively and performs slightly better than the balance "
        "heuristic in most scenes. It is what production renderers use."),
  ("code", """inline float mis_weight(float pdf_a, float pdf_b) {
    float a = pdf_a * pdf_a, b = pdf_b * pdf_b;   // power heuristic, beta=2
    return a / (a + b);
}

// 1. Light sample, weighted by how likely the BSDF was to find it.
auto [wi_L, Li, pdf_L] = scene.sample_light(h.p, rng.next2D());
if (pdf_L > 0 && !scene.occluded(h.p, wi_L)) {
    float pdf_B = h.bsdf->pdf(-r.d, wi_L);        // query, not sample
    float w     = mis_weight(pdf_L, pdf_B);
    L += throughput * w * h.bsdf->f(-r.d, wi_L)
                        * fabs(dot(wi_L, h.ns)) * Li / pdf_L;
}

// 2. BSDF sample; if the continuation hits a light, weight symmetrically.
if (next.emits()) {
    float pdf_L2 = specular ? 0.0f : scene.pdf_light(h.p, wi_B);
    float w      = mis_weight(pdf_B, pdf_L2);
    L += throughput * w * next.emission();
}"""),
  ("callout", "Two implementation details that cause most MIS bugs",
   ["<b>The other strategy's PDF is queried, not sampled.</b> When "
    "evaluating the light sample's weight, you need the density the "
    "<i>BSDF</i> would have assigned to that direction — you do not "
    "draw another BSDF sample. This is exactly why Module 07 insisted that "
    "<code>pdf()</code> be callable independently of <code>sample()</code>.",
    "<b>Specular lobes set the other strategy's PDF to zero.</b> A delta "
    "BSDF has infinite density in one direction, so its MIS weight is 1 and "
    "light sampling's is 0 — light sampling could never have produced "
    "that direction. Implement it by passing 0 for the other PDF, which "
    "makes the weight exactly 1.",
    "<b>Omitting the specular case is the single most common MIS bug</b>, "
    "and its symptom is distinctive: mirrors and polished metals lose the "
    "reflections of light sources while everything else looks correct. If a "
    "chrome sphere shows the room but not the lamp, this is why."]),
  ("table", ["Configuration", "BSDF sampling", "Light sampling", "MIS"],
   [["Small light, diffuse surface", "Terrible", "<b>Excellent</b>",
     "<b>Excellent</b>"],
    ["Large light, glossy surface", "<b>Excellent</b>", "Terrible",
     "<b>Excellent</b>"],
    ["<b>Medium light, medium roughness</b>", "Poor", "Poor",
     "<b>Good</b> — better than either"],
    ["Specular reflection of a light", "<b>The only option</b>",
     "Contributes zero", "<b>Correct, weight 1</b>"]],
   [0.34, 0.22, 0.22, 0.22]),
  ("p", "<b>The third row is the real argument for MIS.</b> It is easy to "
        "assume MIS merely selects whichever strategy is better. It does "
        "more than that: in intermediate configurations, where <i>neither</i> "
        "strategy is adequate alone, the weighted combination has lower "
        "variance than either. That is the behaviour Veach's figure in the "
        "original paper demonstrates, and reproducing that figure is part of "
        "Project 1."),

  ("h1", "4 &nbsp; Debugging a path tracer"),
  ("table", ["Symptom", "Likely cause", "Check"],
   [["Image roughly twice as bright in directly lit areas.",
     "<b>Double counting.</b> MIS weights missing, or emission counted after "
     "an NEE sample.",
     "Disable NEE; if brightness becomes correct, the weighting is wrong."],
    ["Glossy and specular highlights of lights missing.",
     "<b>The specular MIS case is unhandled.</b>",
     "Check that a delta lobe forces the other PDF to zero."],
    ["Black image with point or very small lights.",
     "No next-event estimation.", "&sect;2."],
    ["Dark speckle across all surfaces.",
     "Self-intersection.", "Module 03 &sect;3 — use the ULP offset."],
    ["Isolated bright pixels on silhouettes and creases.",
     "Intersection is not watertight.", "Module 03 &sect;2."],
    ["Uniformly too dark, worsening with roughness.",
     "<b>Microfacet single-scattering energy loss.</b>",
     "Module 07 — furnace test across the roughness range."],
    ["Image brightens the longer it runs.",
     "A BRDF that creates energy.",
     "Furnace test every material; check for albedo &gt; 1."],
    ["Converges cleanly to the wrong answer.",
     "<b>Bias.</b> A clamp, a bounce limit, or a biased estimator.",
     "Convergence plot (Module 05) — the curve flattens."]],
   [0.27, 0.36, 0.37]),
  ("callout", "Validate one component at a time",
   ["<b>Direct lighting, diffuse only, one area light.</b> There are "
    "configurations with analytic solutions — a disk light above a "
    "diffuse plane, for instance. Match them exactly. If this is wrong, "
    "nothing downstream can be right.",
    "<b>Add indirect.</b> Render a Cornell box and difference it against "
    "PBRT's output. <b>The difference image should be unstructured "
    "noise.</b> Any visible structure — a bright wall, a dark corner "
    "— localises the bug immediately.",
    "<b>Add BSDFs one at a time</b>, furnace-testing each before it enters a "
    "scene (Module 07 &sect;4).",
    "<b>Finally enable MIS, and confirm the converged image does not "
    "change</b> while the variance falls. <b>This is the critical test:</b> "
    "MIS is a variance reduction technique and must not alter the answer. If "
    "the converged image shifts when MIS is enabled, the weights do not sum "
    "to one and the estimator is biased."]),
 ],
 "resources": [
   ("PBRT 4th ed. &mdash; Chapter 13, Light Transport I",
    "https://pbr-book.org/4ed/Light_Transport_I_Surface_Reflection",
    "Path tracing, NEE, and MIS with complete code. &sect;13.10 on MIS is "
    "the implementation to compare yours against."),
   ("Veach & Guibas &mdash; Optimally Combining Sampling Techniques (1995, "
    "free)",
    "https://graphics.stanford.edu/papers/combine/",
    "The original MIS paper. Short, and the figure comparing strategies "
    "across light sizes is the one to reproduce."),
   ("Veach thesis &mdash; Chapter 9",
    "https://graphics.stanford.edu/papers/veach_thesis/",
    "The fuller treatment, including the optimality proof for the balance "
    "heuristic."),
   ("Benedikt Bitterli &mdash; rendering resources",
    "https://benedikt-bitterli.me/resources/",
    "Scenes in PBRT format with reference images. Your validation set for "
    "&sect;4."),
 ],
 "exercises": [
   "Implement the naive path tracer. Render a scene with a large area light "
   "and confirm it converges. Then shrink the light by factors of ten and "
   "plot variance against light solid angle.",
   "Add a point light and confirm the naive tracer renders it black. This is "
   "worth seeing once.",
   "Implement next-event estimation. Confirm point lights work and report "
   "the variance reduction on the small-light scene from exercise 1.",
   "Construct a scene with a polished metal plane reflecting a small light. "
   "Render with NEE only and confirm the highlight is absent.",
   "Implement MIS with the balance heuristic. Confirm the converged image "
   "matches the NEE-only result in diffuse regions and recovers the "
   "highlight.",
   "Implement the power heuristic and compare variance against the balance "
   "heuristic on three scenes. Report whether the difference is worth "
   "having.",
   "<b>Reproduce Veach's figure:</b> a row of plates of increasing roughness "
   "lit by lights of increasing size, rendered with BSDF sampling only, "
   "light sampling only, and MIS. This single image demonstrates the whole "
   "module.",
   "Deliberately omit the specular MIS case and render a chrome sphere "
   "beside a light. Document the artefact.",
   "Produce a four-way convergence plot — naive, NEE, BSDF, MIS "
   "— on the same scene. The MIS curve must sit below the others "
   "everywhere, and you must be able to explain each gap.",
 ],
 "selfcheck": [
   "Write the naive path tracer from memory and say why it is unbiased.",
   "Why does it fail for small lights, and why does the failure compound?",
   "What does next-event estimation do, and why must emission then be "
   "skipped on the continuation?",
   "Why does NEE alone fail on glossy surfaces?",
   "State the MIS estimator and the single condition required for it to be "
   "unbiased.",
   "What does the balance heuristic weight represent, and why does it adapt "
   "without being told the scene type?",
   "Why is the other strategy's PDF queried rather than sampled?",
   "How are specular lobes handled in MIS, and what is the symptom of "
   "getting it wrong?",
   "Give four path tracer symptoms and their likely causes.",
   "What must be true of the converged image when MIS is enabled, and why?",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Lights and Sampling Them",
 "subtitle": "Where the energy comes from, and how to find it.",
 "question": "How do you sample a light — or a million of them?",
 "outcomes": [
     "Implement area, point, directional, and environment lights with "
     "correct PDFs.",
     "Sample a sphere light by solid angle rather than by area.",
     "Build a 2D CDF for environment map importance sampling.",
     "Explain the many-lights problem and the structures that solve it.",
     "Explain why light sampling PDFs must be expressed in a consistent "
     "measure.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Kinds of light",
   "blurb": "Four types, and which are physical."},

  {"t": "table", "kicker": "Types", "title": "The light types a renderer needs",
   "header": ["Type", "Is", "Sampling"],
   "widths": [2.6, 5.0, 4.5],
   "rows": [
     ["Point", "Delta in position. <b>Not physical</b>", "One direction, pdf = 1"],
     ["Directional", "Delta in direction; infinitely far", "One direction, pdf = 1"],
     ["<b>Area</b>", "Emitting geometry. <b>The physical one</b>", "<b>Sample the surface</b>"],
     ["Environment", "Radiance from every direction", "<b>2D CDF over luminance</b>"],
   ],
   "footnote": "Point and directional lights are conveniences. They produce "
               "perfectly sharp shadows, which no real light does.",
   "note": "Worth saying: point lights exist because they were cheap in "
           "1980, not because they are correct."},

  {"t": "callout", "title": "Delta lights are a special case throughout",
   "kind": "Consequences",
   "body": ["A point light has <b>zero probability of being hit</b> by a "
            "BSDF-sampled ray, so it exists only through next-event "
            "estimation.",
            "<b>Its MIS weight is therefore always 1</b> — the BSDF "
            "strategy could never have found it. Same structure as the "
            "specular BSDF case in Module 08, mirrored.",
            "<b>It cannot be seen directly</b> by a camera ray, so it needs "
            "no geometry.",
            "Flag delta lights explicitly, exactly as you flag delta BSDFs. "
            "Every integrator branch that asks 'could the other strategy "
            "have produced this?' needs the answer."]},

  {"t": "section", "label": "Part 2", "title": "Sampling area lights",
   "blurb": "The measure you sample in determines the PDF you report."},

  {"t": "eq", "kicker": "Measure", "title": "Area measure and solid angle measure",
   "eqs": [
     ("p(ω)  =  p(A) · ‖p − q‖² / |cos θq|",
      "Converting a density over the light's area into a density over solid "
      "angle at the shading point. The geometry term, again."),
     ("Everything in the integrator must use ONE measure",
      "Mixing area-measure and solid-angle-measure PDFs in an MIS weight is "
      "silently, systematically wrong."),
   ],
   "caption": "Pick solid angle for the whole renderer and convert at the "
              "boundary. Mixed measures are the hardest light bug to find.",
   "note": "This is the bug that costs people days. State it flatly and "
           "repeat it in the notes."},

  {"t": "callout", "title": "Sample a sphere light by solid angle, not by area",
   "kind": "A large, cheap win",
   "body": ["The obvious approach samples uniformly over the sphere's "
            "surface. <b>Half those samples are on the far side</b>, facing "
            "away, contributing nothing.",
            "Worse, samples near the silhouette have a grazing cosine and "
            "near-zero contribution, so the useful fraction is well under "
            "half.",
            "<b>Sampling the visible cone instead</b> — the cone of "
            "directions subtended by the sphere — makes every sample "
            "useful.",
            "<b>Typically 2–4× less variance, and the code is shorter.</b> "
            "The same argument applies to every closed light shape."]},

  {"t": "bullets", "kicker": "Shapes", "title": "Per-shape sampling notes",
   "items": [
     "<b>Triangle:</b> uniform barycentric sampling via √u. Reject if the "
     "shading point is behind the light's plane.",
     "",
     "<b>Quad:</b> uniform in 2D, or solid-angle sampling (Ureña et al.) "
     "for a further large win on big nearby quads.",
     "",
     "<b>Sphere:</b> cone sampling, as above. Degenerates correctly when "
     "the shading point is inside.",
     "",
     "<b>Disk:</b> √ for the radius, as in Module 06.",
     "",
     "<b>Mesh light:</b> choose a triangle proportional to its area times "
     "emitted radiance, then sample within it.",
   ],
   "footnote": "In every case, return the PDF in the same measure the "
               "integrator uses."},

  {"t": "section", "label": "Part 3", "title": "Environment lights",
   "blurb": "An image as a light source."},

  {"t": "code", "kicker": "Env maps", "title": "2D CDF importance sampling",
   "lang": "cpp", "code": """
// Build once at load. Sample proportionally to luminance * sin(theta).
void build(const Image& env) {
    for (int y = 0; y < H; y++) {
        float sinTheta = sinf(PI * (y + 0.5f) / H);   // <-- the Jacobian
        for (int x = 0; x < W; x++)
            f[y][x] = luminance(env(x,y)) * sinTheta;
        rowCdf[y] = build_1d_cdf(f[y]);               // conditional p(x|y)
    }
    marginalCdf = build_1d_cdf(rowSums);              // marginal p(y)
}

// Sample: pick a row from the marginal, a column from that row's
// conditional. Two binary searches, O(log W + log H).
Sample sample(float u1, float u2) {
    auto [y, pdf_y] = sample_1d(marginalCdf, u1);
    auto [x, pdf_x] = sample_1d(rowCdf[y],   u2);
    vec3  dir  = equirect_to_direction(x, y);
    float sinT = sinf(PI * (y + 0.5f) / H);
    // Convert from image-space density to solid-angle density:
    float pdf  = (pdf_x * pdf_y * W * H) / (2 * PI * PI * sinT);
    return { dir, env(x,y), pdf };
}
""",
   "caption": "The sin θ appears twice and means different things: in the "
              "build it corrects for the map's area distortion; in the PDF "
              "it is the measure conversion.",
   "note": "The two sin θ factors confuse everyone. Be explicit that they "
           "are separate and both necessary."},

  {"t": "callout", "title": "Without importance sampling, the sun is noise",
   "kind": "Why this matters",
   "body": ["A typical outdoor HDRI has the sun occupying perhaps 0.001% of "
            "the pixels and carrying <b>most of the total energy</b>.",
            "Uniform sampling finds it once in 100,000 samples, and returns "
            "an enormous value when it does.",
            "<b>That is a firefly generator, not a light.</b> The image is "
            "unusable at any practical sample count.",
            "With a luminance-weighted CDF, the sun is found in proportion "
            "to its energy. <b>This single structure is the difference "
            "between HDRI lighting working and not working.</b>"]},

  {"t": "section", "label": "Part 4", "title": "Many lights",
   "blurb": "What happens at ten thousand light sources."},

  {"t": "callout", "title": "The many-lights problem",
   "kind": "Why uniform selection fails",
   "body": ["With N lights, picking one uniformly costs a factor of N in "
            "variance — you sample the one light that matters 1/N of the "
            "time.",
            "A city scene has 10&#8308;–10&#8310; emitters. Most "
            "contribute nothing to any given shading point: wrong side of a "
            "wall, too far, facing away.",
            "<b>Sampling all of them is far too expensive; sampling one at "
            "random is far too noisy.</b>",
            "The answer is to build a structure that selects lights roughly "
            "in proportion to their actual contribution <i>at this "
            "point</i>."]},

  {"t": "table", "kicker": "Solutions", "title": "Approaches, in increasing order of power",
   "header": ["Method", "Idea", "Cost"],
   "widths": [2.8, 5.2, 4.1],
   "rows": [
     ["Power sampling", "Choose proportional to total emitted power", "Trivial; ignores distance"],
     ["<b>Light BVH</b>", "Hierarchy over lights; descend by estimated contribution", "<b>The standard answer</b>"],
     ["Lightcuts", "Cluster lights; bound the error of each cluster", "Strong bounds; complex"],
     ["<b>ReSTIR</b>", "Resample across space and time, reusing neighbours", "<b>Transformative, real time</b>"],
   ],
   "note": "ReSTIR is the most significant rendering result of the last "
           "decade. Module 12 returns to it."},

  {"t": "callout", "title": "Light sampling has to be unbiased too",
   "kind": "The constraint",
   "body": ["Every one of these schemes must report the <b>exact "
            "probability</b> with which it selected the light it selected.",
            "That probability enters the estimator and the MIS weight. If "
            "the structure's heuristic says a light is unimportant and the "
            "reported PDF does not match the actual selection probability, "
            "<b>the result is biased</b>.",
            "<b>A light with zero selection probability is a light that does "
            "not exist.</b> Every scheme must give every potentially "
            "contributing light a non-zero chance.",
            "This is Module 06's defensive sampling rule, applied to light "
            "selection."]},
 ],
 "takeaways": [
   "Point and directional lights are deltas: never hit by BSDF sampling, MIS "
   "weight always 1, invisible to camera rays. Flag them.",
   "Area lights are the physical case. Sampling them requires converting "
   "between area measure and solid angle via the geometry term.",
   "Use one measure throughout the integrator. Mixing measures in an MIS "
   "weight is silently and systematically wrong.",
   "Sample sphere lights by the subtended cone rather than by surface area "
   "— 2–4&times; less variance and shorter code.",
   "Environment maps need a luminance-weighted 2D CDF; without it the sun is "
   "a firefly generator rather than a light.",
   "With many lights, selection must be proportional to contribution, and "
   "the selection probability must be reported exactly or the result is "
   "biased.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Kinds of light"),
  ("table", ["Type", "Definition", "Physical?", "Sampling"],
   [["<b>Point</b>", "All energy emitted from a single position.",
     "<b>No.</b> Infinite radiance from zero area.",
     "One direction, probability 1."],
    ["<b>Spot</b>", "A point light with an angular falloff.",
     "No, for the same reason.", "As point."],
    ["<b>Directional</b>", "Parallel rays from infinitely far away.",
     "An idealisation of a very distant source.",
     "One direction, probability 1."],
    ["<b>Area</b>", "Emitting geometry with finite extent.",
     "<b>Yes.</b> This is what real lights are.",
     "Sample a point on the surface."],
    ["<b>Environment</b>",
     "Radiance arriving from every direction at infinity; an image.",
     "An idealisation of distant surroundings.",
     "<b>2D CDF over luminance</b> (&sect;3)."]],
   [0.14, 0.33, 0.26, 0.27]),
  ("p", "Point and directional lights are conveniences inherited from an era "
        "when area lights were unaffordable. They produce perfectly sharp "
        "shadow boundaries, which no real light source does, and they are "
        "the main reason early computer graphics has its characteristic "
        "look. Support them — they are useful and artists expect them "
        "— but understand that an area light is the physical object."),
  ("callout", "Delta lights are a special case through the whole integrator",
   ["<b>They cannot be hit by a BSDF-sampled ray.</b> The probability of a "
    "randomly chosen direction passing exactly through a point is zero, so a "
    "delta light exists in the image <i>only</i> through next-event "
    "estimation.",
    "<b>Their MIS weight is therefore always exactly 1.</b> The BSDF "
    "strategy could never have generated that direction, so its share of the "
    "density is zero. This is the mirror image of the specular-BSDF case in "
    "Module 08: there the light strategy had zero density; here the BSDF "
    "strategy does.",
    "<b>They cannot be seen directly by a camera ray</b>, so they need no "
    "geometry and contribute nothing when looked at.",
    "<b>Flag them explicitly</b>, exactly as Module 07 flagged delta BSDFs. "
    "Every place the integrator asks 'could the other strategy have produced "
    "this sample?' requires the answer, and deriving it from the light type "
    "at each site is how inconsistencies creep in."]),

  ("h1", "2 &nbsp; Sampling area lights"),
  ("p", "An area light is sampled by choosing a point on its surface. But "
        "the integrator works in solid angle, so the density must be "
        "converted."),
  ("eq", "p(&omega;) = p(A) &middot; |p &minus; q|&#178; / "
         "|cos&theta;<sub>q</sub>|"),
  ("p", "This is the geometry term from Module 02 appearing in a new role: "
        "the Jacobian relating a density over the light's area to a density "
        "over directions at the shading point."),
  ("callout", "Use one measure throughout, and convert at the boundary",
   ["This is the hardest class of bug in light sampling, because it produces "
    "a plausible image that is systematically wrong by a factor varying with "
    "distance and orientation.",
    "<b>An MIS weight combines two densities, and they must be in the same "
    "measure.</b> If the light sampler reports a density per unit area and "
    "the BSDF reports one per unit solid angle, the weight is meaningless "
    "and the result is biased — but it converges smoothly to the "
    "wrong answer, so it looks like success.",
    "<b>Pick solid angle for the entire renderer.</b> Every "
    "<code>pdf()</code> returns a solid-angle density; light samplers "
    "convert internally before returning. Then the question can never arise "
    "at a call site.",
    "<b>The test:</b> render a scene with a light at distance 1 and the same "
    "scene scaled up by 100. The converged images must be identical. If they "
    "differ, a measure conversion is missing."]),
  ("callout", "Sample a sphere light by solid angle, not by area",
   ["The obvious implementation samples uniformly over the sphere's surface. "
    "<b>Half the samples land on the far side</b>, facing away from the "
    "shading point, and contribute exactly nothing.",
    "It is worse than half. Samples near the visible silhouette have a "
    "grazing cos&theta;<sub>q</sub> and contribute almost nothing either, so "
    "the genuinely useful fraction is well under 50%.",
    "<b>Sample the cone of directions the sphere subtends instead.</b> Every "
    "direction in that cone strikes the visible hemisphere, and the density "
    "is uniform over the cone, which is a closed-form construction of about "
    "ten lines.",
    "<b>Typically two to four times less variance, with shorter code.</b> "
    "The general principle — sample the directions that can contribute, "
    "rather than the geometry that may not — applies to every closed "
    "light shape, and Ure&ntilde;a's solid-angle quad sampling does the same "
    "for rectangles."]),
  ("table", ["Shape", "Method", "Watch for"],
   [["<b>Triangle</b>", "Uniform barycentric sampling using &radic;u&#8321;.",
     "Reject when the shading point is behind the light's plane — "
     "otherwise you sample a light that cannot illuminate it."],
    ["<b>Quad</b>", "Uniform in 2D, or solid-angle sampling "
     "(Ure&ntilde;a et al. 2013).",
     "Solid-angle sampling is a large win for big nearby quads — "
     "softboxes, windows — and roughly neutral for small distant ones."],
    ["<b>Sphere</b>", "Cone sampling, as above.",
     "Must degenerate correctly to full-sphere sampling when the shading "
     "point is inside the sphere."],
    ["<b>Disk</b>", "&radic; for the radius, uniform in angle.",
     "The same &radic; as Module 06."],
    ["<b>Mesh light</b>",
     "Select a triangle with probability proportional to area &times; "
     "emitted radiance, then sample within it.",
     "Build the selection CDF once at load, not per sample."]],
   [0.13, 0.37, 0.50]),

  ("break",),
  ("h1", "3 &nbsp; Environment lights"),
  ("p", "An environment light surrounds the scene with an image — "
        "typically a high-dynamic-range photograph in equirectangular "
        "projection — providing radiance from every direction. It is "
        "the standard way to light a scene realistically, and it is useless "
        "without importance sampling."),
  ("callout", "Why uniform sampling of an environment map fails completely",
   ["A typical outdoor HDRI has the sun occupying on the order of 0.001% of "
    "its pixels while carrying the <b>majority of the total energy</b> "
    "— a dynamic range of 10<super>5</super> or more between the sun "
    "and the sky beside it.",
    "Uniform directional sampling finds the sun roughly once in 100,000 "
    "samples, and returns an enormous value when it does.",
    "<b>That is a firefly generator, not a light source.</b> The image is "
    "unusable at any practical sample count, and no amount of waiting fixes "
    "it, because the variance is dominated by an event that almost never "
    "occurs.",
    "With a luminance-weighted CDF, the sun is sampled roughly in proportion "
    "to the energy it carries. <b>This single data structure is the "
    "difference between HDRI lighting working and not working</b>, and it is "
    "about eighty lines."]),
  ("code", """// Build once at load.
for (int y = 0; y < H; y++) {
    float sinTheta = sinf(PI * (y + 0.5f) / H);     // area distortion
    for (int x = 0; x < W; x++)
        f[y][x] = luminance(env(x,y)) * sinTheta;
    rowCdf[y] = build_1d_cdf(f[y]);                 // conditional p(x|y)
}
marginalCdf = build_1d_cdf(rowSums);                // marginal p(y)

// Sample: marginal then conditional. Two binary searches.
auto [y, pdf_y] = sample_1d(marginalCdf, u1);
auto [x, pdf_x] = sample_1d(rowCdf[y],   u2);
float sinT = sinf(PI * (y + 0.5f) / H);
float pdf  = (pdf_x * pdf_y * W * H) / (2 * PI * PI * sinT);"""),
  ("callout", "The two sin&theta; factors mean different things",
   ["<b>In the build:</b> an equirectangular map distorts area. A pixel row "
    "near the pole covers far less solid angle than one at the equator, "
    "despite having the same number of pixels. Weighting by sin&theta; "
    "corrects for this, so the CDF is proportional to <i>energy</i> rather "
    "than to pixel value.",
    "<b>In the PDF:</b> the sampling procedure produced a density over image "
    "coordinates, and the integrator needs one over solid angle. Dividing by "
    "sin&theta; performs that measure conversion — &sect;2's rule "
    "again.",
    "<b>They are separate corrections that happen to involve the same "
    "function</b>, and conflating them — or applying one and not the "
    "other — is the usual bug here. The symptom is an environment "
    "light that is systematically wrong near the poles, which in an outdoor "
    "scene means the sky directly overhead.",
    "<b>The test:</b> render a diffuse white sphere under a constant white "
    "environment and compare against the analytic answer. It must match "
    "exactly, because a constant environment has an analytic solution."]),

  ("h1", "4 &nbsp; Many lights"),
  ("callout", "The problem",
   ["Next-event estimation needs a light to sample. With N lights, selecting "
    "one uniformly and dividing by 1/N is unbiased, and costs roughly a "
    "factor of N in variance — the one light that actually illuminates "
    "the shading point is chosen only 1/N of the time.",
    "A city at night, an interior with hundreds of fixtures, or a scene with "
    "emissive geometry can have 10<super>4</super> to 10<super>6</super> "
    "emitters. <b>Most contribute nothing at all to any given shading "
    "point:</b> they are behind a wall, facing away, or far enough that "
    "their contribution is negligible.",
    "<b>Sampling all of them is prohibitively expensive. Sampling one "
    "uniformly is prohibitively noisy.</b>",
    "The answer is a structure that selects lights approximately in "
    "proportion to their actual contribution <i>at the shading point being "
    "considered</i> — which is a different distribution at every "
    "point."]),
  ("table", ["Method", "Idea", "Assessment"],
   [["<b>Power sampling</b>",
     "Build one global CDF over total emitted power.",
     "Trivial, and better than uniform. Ignores distance and visibility "
     "entirely, so a powerful light on the other side of the building is "
     "still chosen often."],
    ["<b>Light BVH</b>",
     "A hierarchy over the lights, each node storing bounds, total power, "
     "and an orientation cone. Descend stochastically, choosing children in "
     "proportion to an estimate of their contribution at the shading point.",
     "<b>The standard answer in production renderers.</b> Logarithmic in "
     "light count, adapts per shading point, and the selection probability "
     "is exactly computable — which &sect;4's constraint requires."],
    ["<b>Lightcuts</b>",
     "Cluster lights into a hierarchy and compute an error bound for "
     "treating a whole cluster as one representative light. Refine until the "
     "bound is acceptable.",
     "Gives a genuine error bound rather than a heuristic. More complex, and "
     "the bounds can be loose."],
    ["<b>ReSTIR</b>",
     "Resampled importance sampling with reservoirs, reusing samples across "
     "neighbouring pixels and across frames.",
     "<b>Transformative.</b> Makes millions of lights tractable in real "
     "time. Arguably the most significant rendering result of the last "
     "decade. Module 12 returns to it."]],
   [0.14, 0.42, 0.44]),
  ("callout", "Whatever the scheme, the probability must be exact",
   ["Every selection scheme must report <b>the exact probability with which "
    "it chose the light it chose</b>. That probability divides the "
    "contribution in the estimator and feeds the MIS weight in Module 08.",
    "<b>If the reported probability does not match the actual selection "
    "behaviour, the result is biased</b> — and, as always, biased in a "
    "way that converges confidently. A light BVH whose descent probabilities "
    "do not match its stated PDF produces a smooth, wrong image.",
    "<b>A light with zero selection probability is a light that does not "
    "exist.</b> Any heuristic that prunes 'unimportant' lights outright "
    "introduces bias. Schemes must give every potentially contributing light "
    "a non-zero chance, however small.",
    "This is Module 06's defensive sampling rule applied to light selection, "
    "and it is why light hierarchies use <i>stochastic</i> traversal rather "
    "than descending into the apparently best child."]),
 ],
 "resources": [
   ("PBRT 4th ed. &mdash; Chapter 12, Light Sources",
    "https://pbr-book.org/4ed/Light_Sources",
    "Every light type with its sampling routine and PDF, including the "
    "environment map 2D distribution of &sect;3."),
   ("PBRT 4th ed. &mdash; &sect;12.6, Light Sampling (BVH)",
    "https://pbr-book.org/4ed/Light_Sources",
    "The light BVH of &sect;4, with the importance heuristic and the "
    "orientation cone bounds."),
   ("Ure&ntilde;a, Fajardo & King &mdash; An Area-Preserving Parametrization "
    "for Spherical Rectangles (free)",
    "https://www.arnoldrenderer.com/research/",
    "Solid-angle sampling for quads. Arnold's research page has a great deal "
    "of production-grade free material."),
   ("Bitterli et al. &mdash; Spatiotemporal Reservoir Resampling (ReSTIR, "
    "free)",
    "https://research.nvidia.com/publication/2020-07_spatiotemporal-"
    "reservoir-resampling-real-time-ray-tracing-dynamic-direct",
    "The many-lights result of &sect;4. Read it after Module 12."),
   ("Poly Haven &mdash; free HDRIs (CC0)",
    "https://polyhaven.com/hdris",
    "High-quality environment maps, CC0 licensed, for testing &sect;3."),
 ],
 "exercises": [
   "Implement area lights with triangle and quad sampling. Verify the PDF "
   "with a &chi;&#178; test in solid-angle measure.",
   "Implement sphere light sampling by area and by subtended cone. Report "
   "the variance ratio at several distances.",
   "Perform the scale test from &sect;2: render a scene, then the same scene "
   "scaled by 100&times;, and confirm the converged images match. If they do "
   "not, find the missing measure conversion.",
   "Build the 2D CDF for an environment map. Visualise the sampling density "
   "as an image and confirm the sun is bright in it.",
   "Render a scene with an outdoor HDRI with and without environment "
   "importance sampling at 64 samples per pixel. The difference is the "
   "entire point of &sect;3.",
   "Verify the constant-environment test: a diffuse white sphere under a "
   "uniform environment must match the analytic answer exactly.",
   "Implement power-proportional light selection and compare against uniform "
   "selection on a scene with 100 lights of widely varying brightness.",
   "Implement a simple light BVH and compare against power sampling on a "
   "scene with 10,000 lights spread over a large area. Report variance and "
   "time.",
   "Deliberately prune lights below a contribution threshold and demonstrate "
   "the resulting bias with a convergence plot.",
 ],
 "selfcheck": [
   "Name the five light types and say which are physical.",
   "Give three ways delta lights are special in the integrator.",
   "Write the conversion between area-measure and solid-angle-measure "
   "densities.",
   "Why must the whole renderer use one measure, and what test detects a "
   "mixed-measure bug?",
   "Why is cone sampling better than area sampling for a sphere light?",
   "Why does uniform sampling of an environment map fail, and what does the "
   "2D CDF fix?",
   "Explain the two different roles sin&theta; plays in environment map "
   "sampling.",
   "What is the many-lights problem, and why does uniform selection cost a "
   "factor of N?",
   "What must every light selection scheme report, and why is pruning a "
   "light biased?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Participating Media",
 "subtitle": "Removing the vacuum assumption, and what it costs.",
 "question": "What happens when light scatters between surfaces?",
 "outcomes": [
     "State the volume rendering equation and its coefficients.",
     "Explain transmittance and why it is an integral.",
     "Sample distances in homogeneous media analytically.",
     "Implement delta tracking for heterogeneous media and say why it is "
     "unbiased.",
     "Explain phase functions and sample Henyey–Greenstein.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The coefficients",
   "blurb": "Three numbers that describe a medium."},

  {"t": "table", "kicker": "Coefficients", "title": "What a medium does to a ray",
   "header": ["Symbol", "Name", "Effect"],
   "widths": [2.0, 3.4, 6.7],
   "rows": [
     ["σₐ", "Absorption", "Light is removed and converted to heat"],
     ["σₛ", "Scattering", "Light is redirected, not removed"],
     ["σₜ = σₐ + σₛ", "<b>Extinction</b>", "<b>Total removal from the ray</b>"],
     ["σₛ/σₜ", "Single-scattering albedo", "Fraction redirected rather than absorbed"],
   ],
   "footnote": "Units are inverse length. A σₜ of 0.1 per metre means "
               "roughly 10% of the energy is removed per metre.",
   "note": "Albedo near 1 means light bounces many times — clouds, milk, "
           "marble. That is what makes those materials expensive."},

  {"t": "callout", "title": "Radiance is no longer invariant along a ray",
   "kind": "What breaks",
   "body": ["Module 01 established that radiance is unchanged along a ray in "
            "a vacuum, and Module 02 used this to make a ray a "
            "<i>lookup</i>.",
            "<b>In a medium, radiance changes continuously along the ray:</b> "
            "energy is removed by absorption and out-scattering, and added "
            "by in-scattering from every other direction.",
            "<b>So a ray becomes an integral again</b> — and the "
            "in-scattering term is itself an integral over directions.",
            "<b>That is the entire reason volumetric rendering is expensive.</b> "
            "The structural assumption that made ray tracing cheap has been "
            "removed."]},

  {"t": "eq", "kicker": "Transport", "title": "The volume rendering equation",
   "eqs": [
     ("dL/ds  =  −σₜ L  +  σₛ ∫ p(ω,ω') L(ω') dω'  +  σₐ Le",
      "Radiance along the ray loses to extinction, gains from in-scattering, "
      "and gains from emission."),
     ("T(a,b)  =  exp( −∫ₐᵇ σₜ(x) ds )",
      "Transmittance: the fraction surviving from a to b. Beer–Lambert."),
     ("L(camera)  =  ∫ T(0,s) σₛ(s) Ls(s) ds  +  T(0,d) L(surface)",
      "The integral form: every point along the ray contributes, attenuated "
      "by the transmittance up to it."),
   ],
   "caption": "The surface rendering equation is the special case where σₜ "
              "is zero everywhere between surfaces.",
   "note": "Point out the structure: the final equation has a volume term "
           "plus an attenuated surface term."},

  {"t": "section", "label": "Part 2", "title": "Homogeneous media",
   "blurb": "When σₜ is constant, everything is analytic."},

  {"t": "eq", "kicker": "Homogeneous", "title": "Sampling a scattering distance",
   "eqs": [
     ("T(s)  =  exp(−σₜ s)",
      "Transmittance is a simple exponential when σₜ is constant."),
     ("s  =  −ln(1 − ξ) / σₜ",
      "Inverting the CDF gives the distance to the next scattering event. "
      "Module 06's inversion method."),
     ("pdf(s)  =  σₜ exp(−σₜ s)",
      "And the σₜ cancels against the σₛ in the estimator, leaving the "
      "albedo — exactly as the cosine cancelled in Module 06."),
   ],
   "caption": "Homogeneous media are cheap: one logarithm per scattering "
              "event and a perfect importance sample.",
   "note": "Call back to Malley's method. The same pleasing cancellation, "
           "for the same reason."},

  {"t": "callout", "title": "Phase functions are the BRDF of a medium",
   "kind": "The analogy",
   "body": ["A phase function gives the probability of scattering from one "
            "direction into another. <b>It is normalised to integrate to "
            "1</b> over the sphere — unlike a BRDF, which may absorb.",
            "<b>Isotropic:</b> p = 1/4π. Equal in all directions. Thin "
            "smoke.",
            "<b>Henyey–Greenstein:</b> one parameter g ∈ (−1,1). "
            "Forward scattering (g > 0) for clouds and skin; backward "
            "(g < 0) for some atmospheric effects.",
            "<b>Analytic inversion makes HG cheap to sample</b>, which is "
            "most of why it is used despite being an empirical fit to "
            "measured scattering."]},

  {"t": "section", "label": "Part 3", "title": "Heterogeneous media",
   "blurb": "When σₜ varies, the integral has no closed form."},

  {"t": "callout", "title": "Ray marching is biased, and tempting",
   "kind": "What not to do",
   "body": ["The obvious approach steps along the ray in fixed increments, "
            "accumulating transmittance.",
            "<b>It is biased.</b> The exponential of an approximated "
            "integral is not the approximated exponential, and the error "
            "does not vanish with more samples per pixel — only with a "
            "smaller step.",
            "<b>It also aliases</b>: a regular step through a structured "
            "density produces banding.",
            "<b>It is still widely used</b> in real time, where the bias is "
            "acceptable and the cost is predictable. Know that you are "
            "choosing it."]},

  {"t": "code", "kicker": "Unbiased", "title": "Delta tracking (Woodcock tracking)",
   "lang": "cpp", "code": """
// Fill the medium with fictitious matter so total density is constant
// at a known majorant. Then sample as if homogeneous, and at each
// event decide whether it was real or fictitious.
//
// UNBIASED. No step size. No bias. One ln per event.

float sample_distance(Ray r, const Medium& m, RNG& rng) {
    float t      = 0.0f;
    float sigma_bar = m.majorant;              // >= sigma_t everywhere
    while (true) {
        t -= logf(1.0f - rng.next()) / sigma_bar;   // homogeneous step
        if (t >= r.tmax) return INFINITY;           // escaped the medium

        // Did we hit real matter, or the fictitious filler?
        if (rng.next() < m.sigma_t(r.at(t)) / sigma_bar)
            return t;                               // REAL collision
        // else: null collision -- continue, unchanged.
    }
}
""",
   "caption": "The fictitious matter cancels exactly in expectation. The "
              "cost is that a loose majorant means many wasted null "
              "collisions.",
   "note": "The null-collision idea is genuinely clever and students find it "
           "surprising that it is exactly unbiased."},

  {"t": "table", "kicker": "Variants", "title": "The tracking family",
   "header": ["Method", "Estimates", "Note"],
   "widths": [3.0, 4.8, 4.3],
   "rows": [
     ["Delta tracking", "A scattering position", "<b>Unbiased; the workhorse</b>"],
     ["Ratio tracking", "Transmittance", "<b>Lower variance for shadow rays</b>"],
     ["Residual ratio", "Transmittance with a control variate", "Better in dense media"],
     ["Spectral tracking", "Wavelength-dependent media", "Needed for coloured smoke"],
   ],
   "footnote": "Use delta tracking for scattering positions and ratio "
               "tracking for transmittance. They solve different problems.",
   "note": "The common bug is using delta tracking for shadow rays, which "
           "gives a binary estimate and enormous variance."},

  {"t": "callout", "title": "The majorant determines the cost",
   "kind": "The practical constraint",
   "body": ["Delta tracking needs an upper bound σ̄ on σₜ. <b>Any valid bound "
            "gives a correct answer.</b>",
            "<b>A loose bound is correct and slow:</b> a cloud that is dense "
            "in one small region and nearly empty elsewhere, with a single "
            "global majorant, spends almost all its time on null "
            "collisions.",
            "<b>The fix is a spatial majorant grid</b> — a coarse grid "
            "storing a local maximum, so empty regions are crossed in one "
            "step.",
            "This is the same structural idea as the BVH in Module 04: a "
            "cheap conservative bound that lets you skip the empty space, "
            "which is most of it."]},

  {"t": "bullets", "kicker": "In practice", "title": "What makes volumes expensive",
   "items": [
     "<b>High albedo means many scattering events.</b> A cloud has albedo "
     "≈ 0.9999; light scatters hundreds of times before escaping.",
     "",
     "<b>NEE through a medium needs transmittance</b>, which is itself an "
     "estimate — so every shadow ray is a tracking loop.",
     "",
     "<b>Equiangular sampling</b> is essential near a light inside a "
     "medium: sample distance by proximity to the light rather than by "
     "transmittance alone.",
     "",
     "<b>Subsurface scattering is just a dense medium</b> inside a "
     "boundary. Skin, marble, milk. The diffusion approximation is the cheap "
     "version.",
   ],
   "note": "The albedo-0.9999 fact is the one that explains why clouds "
           "render slowly. It is not the tracking; it is the bounce count."},
 ],
 "takeaways": [
   "A medium is three coefficients: absorption, scattering, and their sum, "
   "extinction. Albedo near 1 means many bounces and high cost.",
   "Radiance is no longer invariant along a ray, so a ray becomes an "
   "integral — this is the entire reason volumes are expensive.",
   "In homogeneous media the transmittance is a simple exponential and "
   "distance sampling inverts analytically, with a pleasing cancellation.",
   "Phase functions are the medium's BRDF, normalised to 1. "
   "Henyey–Greenstein is used because it inverts in closed form.",
   "Ray marching is biased; delta tracking adds fictitious matter so the "
   "medium appears homogeneous, and is exactly unbiased with no step size.",
   "Any valid majorant is correct; a loose one is slow. A majorant grid is "
   "the same idea as a BVH — skip the empty space cheaply.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What a medium is"),
  ("table", ["Symbol", "Name", "Meaning", "Units"],
   [["&sigma;<sub>a</sub>", "Absorption coefficient",
     "Probability per unit length that a photon is absorbed and converted to "
     "heat.", "1/length"],
    ["&sigma;<sub>s</sub>", "Scattering coefficient",
     "Probability per unit length that a photon is redirected without loss "
     "of energy.", "1/length"],
    ["&sigma;<sub>t</sub>", "<b>Extinction coefficient</b>",
     "<b>&sigma;<sub>a</sub> + &sigma;<sub>s</sub>.</b> Total probability "
     "per unit length of being removed from the current ray, by either "
     "mechanism.", "1/length"],
    ["&sigma;<sub>s</sub>/&sigma;<sub>t</sub>", "Single-scattering albedo",
     "Of the light removed from the ray, the fraction redirected rather than "
     "absorbed.", "dimensionless"]],
   [0.12, 0.21, 0.55, 0.12]),
  ("p", "The albedo is the number that governs cost. A medium with albedo "
        "near 1 absorbs almost nothing, so light scatters many times before "
        "it escapes or reaches the camera. <b>A cloud has an albedo of "
        "roughly 0.9999</b>, and photons scatter hundreds of times inside "
        "it. That bounce count, not the cost of any individual operation, is "
        "why clouds are slow to render."),
  ("callout", "The vacuum assumption is what made ray tracing cheap",
   ["Module 01 established that radiance is invariant along a ray in a "
    "vacuum, and Module 02 used that to make a ray a <b>lookup</b>: trace "
    "until you hit something, read the radiance leaving it, done.",
    "<b>In a participating medium that fails.</b> Radiance changes "
    "continuously along the ray: energy is removed by absorption and by "
    "scattering out of the ray's direction, and added by light scattering "
    "<i>into</i> the ray from every other direction.",
    "<b>So a ray becomes an integral along its length</b> — and the "
    "in-scattering term inside that integral is itself an integral over the "
    "whole sphere of directions, at every point along the ray.",
    "<b>This is the structural reason volumetric rendering is expensive.</b> "
    "It is not an implementation inefficiency; the assumption that made ray "
    "tracing a lookup rather than an integral has been removed."]),
  ("eq", "dL/ds = &minus;&sigma;<sub>t</sub> L + &sigma;<sub>s</sub> "
         "&int; p(&omega;,&omega;&prime;) L(&omega;&prime;) "
         "d&omega;&prime; + &sigma;<sub>a</sub> L<sub>e</sub>"),
  ("eq", "T(a,b) = exp( &minus;&int;<sub>a</sub><super>b</super> "
         "&sigma;<sub>t</sub>(x) ds )"),
  ("p", "<b>Transmittance</b> T is the fraction of radiance surviving "
        "between two points — the Beer&ndash;Lambert law. Note that "
        "the exponent is an <i>integral</i> of the extinction along the "
        "path, which is why heterogeneous media are difficult: that integral "
        "has no closed form for a general density field."),
  ("eq", "L = &int;<sub>0</sub><super>d</super> T(0,s) &sigma;<sub>s</sub>(s) "
         "L<sub>s</sub>(s) ds + T(0,d) L<sub>surface</sub>"),
  ("p", "The integral form: every point along the ray scatters some light "
        "toward the camera, attenuated by the transmittance accumulated up "
        "to that point, plus the surface at the far end attenuated by the "
        "transmittance across the whole medium. <b>The surface rendering "
        "equation of Module 02 is the special case where "
        "&sigma;<sub>t</sub> = 0 everywhere between surfaces</b>, so T = 1 "
        "and only the second term survives."),

  ("h1", "2 &nbsp; Homogeneous media"),
  ("p", "When &sigma;<sub>t</sub> is constant, the transmittance integral "
        "collapses to a product and everything becomes analytic."),
  ("eq", "T(s) = exp(&minus;&sigma;<sub>t</sub> s) &nbsp;&nbsp;&rArr;"
         "&nbsp;&nbsp; s = &minus;ln(1 &minus; &xi;) / &sigma;<sub>t</sub>, "
         "&nbsp;&nbsp; pdf(s) = &sigma;<sub>t</sub> "
         "exp(&minus;&sigma;<sub>t</sub> s)"),
  ("p", "This is the inversion method from Module 06 applied to the "
        "exponential distribution. Sampling the distance to the next "
        "scattering event costs one logarithm, and it is a <i>perfect</i> "
        "importance sample of the transmittance — so the "
        "&sigma;<sub>t</sub> in the PDF cancels against the "
        "&sigma;<sub>s</sub> in the estimator, leaving the albedo. <b>The "
        "same pleasing cancellation as Malley's method in Module 06</b>, "
        "and for the same reason: the density was chosen to match a factor "
        "of the integrand exactly."),
  ("callout", "Phase functions are the BRDF of a medium",
   ["A phase function p(&omega;, &omega;&prime;) gives the probability "
    "density of scattering from one direction into another. <b>It is "
    "normalised to integrate to 1 over the sphere</b> — unlike a BRDF, "
    "which may absorb, because absorption is already accounted for "
    "separately by &sigma;<sub>a</sub>.",
    "<b>Isotropic:</b> p = 1/4&pi;, scattering equally in all directions. A "
    "reasonable model for thin smoke and a good default.",
    "<b>Henyey&ndash;Greenstein:</b> a single parameter g &isin; "
    "(&minus;1, 1) controls the anisotropy. Positive g is forward "
    "scattering — clouds, skin, and most biological tissue scatter "
    "strongly forward. Negative g is backward scattering.",
    "HG was an empirical fit to measured scattering in interstellar dust, "
    "and it is used in rendering largely because <b>it inverts in closed "
    "form</b>, making it cheap to importance sample. More accurate models "
    "exist — Mie scattering for water droplets — and are rarely "
    "worth the cost."]),

  ("break",),
  ("h1", "3 &nbsp; Heterogeneous media"),
  ("p", "When &sigma;<sub>t</sub> varies through space — a cloud, a "
        "smoke simulation, a VDB volume — the transmittance integral "
        "has no closed form and distance sampling cannot be inverted "
        "analytically."),
  ("callout", "Ray marching is biased",
   ["The obvious approach steps along the ray in fixed increments, "
    "accumulating optical depth and attenuating as it goes.",
    "<b>It is biased, and not in a way that more samples per pixel "
    "fixes.</b> The exponential of a numerically approximated integral is "
    "not an unbiased estimate of the exponential of the true integral, and "
    "the error depends on the step size rather than the sample count. "
    "Doubling the pixel samples does not help; only reducing the step does.",
    "<b>It also aliases.</b> A regular step through a structured density "
    "field produces visible banding, which is usually hidden by jittering "
    "the starting offset — converting a structured artefact into "
    "noise, which is an improvement but not a fix.",
    "<b>It remains widely used in real time</b>, where the bias is "
    "acceptable and the predictable cost is worth more than correctness. "
    "That is a legitimate engineering choice. The problem is making it "
    "without realising."]),
  ("code", """float sample_distance(Ray r, const Medium& m, RNG& rng) {
    float t = 0.0f, sigma_bar = m.majorant;   // majorant >= sigma_t everywhere
    while (true) {
        t -= logf(1.0f - rng.next()) / sigma_bar;   // homogeneous step
        if (t >= r.tmax) return INFINITY;           // escaped
        if (rng.next() < m.sigma_t(r.at(t)) / sigma_bar)
            return t;                               // real collision
        // otherwise a NULL collision: continue unchanged
    }
}"""),
  ("callout", "Why delta tracking is exactly unbiased",
   ["The idea is to imagine filling the medium with <b>fictitious "
    "matter</b> — 'null' scatterers that do not interact with light "
    "at all — until the total density everywhere equals a known "
    "constant majorant &sigma;&#772;.",
    "The medium is now homogeneous, so distances can be sampled analytically "
    "by &sect;2. At each sampled collision, decide whether it was real "
    "matter or fictitious filler, with probability "
    "&sigma;<sub>t</sub>(x)/&sigma;&#772;. A null collision changes nothing "
    "and the walk continues.",
    "<b>The fictitious matter cancels exactly in expectation</b>, because a "
    "null collision leaves the photon's direction and energy untouched. The "
    "estimator is unbiased, and — crucially — <b>there is no step "
    "size</b> and therefore no step-size parameter to tune or bias to "
    "accept.",
    "This is an idea from neutron transport (Woodcock, 1965) that arrived in "
    "graphics decades later, and it is the standard approach now."]),
  ("table", ["Method", "Estimates", "When to use"],
   [["<b>Delta tracking</b>", "The position of the next real scattering "
     "event.", "<b>The workhorse.</b> Use for path continuation inside a "
     "medium."],
    ["<b>Ratio tracking</b>", "Transmittance between two points, as a "
     "continuous value rather than a binary outcome.",
     "<b>Shadow rays.</b> Delta tracking gives a binary 0-or-1 estimate of "
     "transmittance, which has enormous variance; ratio tracking multiplies "
     "a running weight instead and is far smoother."],
    ["<b>Residual ratio tracking</b>",
     "Transmittance, with a homogeneous control variate subtracted out.",
     "Dense media, where plain ratio tracking still has significant "
     "variance."],
    ["<b>Spectral tracking</b>",
     "Transport in media whose coefficients vary with wavelength.",
     "Coloured smoke, absorbing liquids, skin. Needed with Module 13's "
     "spectral rendering."]],
   [0.17, 0.35, 0.48]),
  ("p", "<b>Using delta tracking for shadow rays is a common and costly "
        "mistake.</b> It answers 'did the ray get through?' with a yes or "
        "no, which is an unbiased but extremely high-variance estimate of "
        "transmittance. Ratio tracking answers 'what fraction got through?' "
        "and is the right tool."),
  ("callout", "The majorant determines the cost",
   ["Delta tracking requires an upper bound &sigma;&#772; on "
    "&sigma;<sub>t</sub> throughout the medium. <b>Any valid bound gives a "
    "correct answer</b> — correctness does not depend on the bound "
    "being tight.",
    "<b>But a loose bound is slow.</b> Consider a cloud that is dense in one "
    "small region and nearly empty elsewhere. With a single global majorant "
    "set by the dense core, a ray through the empty periphery takes "
    "thousands of tiny steps, almost all of them null collisions, before it "
    "escapes.",
    "<b>The fix is a majorant grid:</b> a coarse spatial grid storing the "
    "local maximum of &sigma;<sub>t</sub> in each cell. Empty cells have a "
    "majorant of zero and are crossed in a single step; dense cells use a "
    "tight local bound.",
    "<b>This is structurally the same idea as the BVH of Module 04:</b> a "
    "cheap conservative bound that allows the empty space — which is "
    "most of the volume — to be skipped. The pattern recurs throughout "
    "rendering."]),
  ("h2", "3.1 &nbsp; What else volumes need"),
  ("ul", ["<b>Next-event estimation through a medium</b> requires the "
          "transmittance along the shadow ray, which is itself an estimate "
          "— so every shadow ray becomes a tracking loop. This is why "
          "volumetric NEE is so much more expensive than surface NEE.",
          "<b>Equiangular sampling</b> is essential when a light is inside "
          "or near a medium. Sampling distance by transmittance alone "
          "concentrates samples near the ray's start, while the "
          "contribution is concentrated near the light. Sampling by angle "
          "subtended at the light, combined with transmittance sampling via "
          "MIS, is the standard solution — and it is Module 08's "
          "structure applied again.",
          "<b>Subsurface scattering is a dense medium inside a boundary.</b> "
          "Skin, marble, milk, and wax are all media with very high albedo "
          "enclosed by a refractive surface. Brute-force volumetric "
          "transport is correct and slow; the <b>diffusion approximation</b> "
          "exploits the fact that after many scattering events the "
          "distribution becomes smooth and can be approximated analytically, "
          "which is far cheaper and is what most production renderers use "
          "for skin."]),
 ],
 "resources": [
   ("PBRT 4th ed. &mdash; Chapters 11 and 14, Volume Scattering and Light "
    "Transport II",
    "https://pbr-book.org/4ed/Volume_Scattering",
    "The coefficients, phase functions, and the complete delta-tracking and "
    "ratio-tracking implementations."),
   ("Nov&aacute;k et al. &mdash; Monte Carlo Methods for Volumetric Light "
    "Transport (survey, free)",
    "https://cs.dartmouth.edu/~wjarosz/publications/novak18monte.html",
    "The definitive survey. Everything in &sect;3, with the unbiasedness "
    "proofs and the full tracking family."),
   ("Fong et al. &mdash; Production Volume Rendering (SIGGRAPH course, free)",
    "https://graphics.pixar.com/library/",
    "How volumes are actually rendered in film, including majorant grids and "
    "the practical compromises."),
   ("Wrenninge &mdash; Production Volume Rendering (book site)",
    "http://magnuswrenninge.com/productionvolumerendering",
    "Course notes and code, free. Strong on the data structures."),
   ("Disney &mdash; Cloud data set (CC0)",
    "https://disneyanimation.com/resources/clouds/",
    "A production cloud volume, free to use. Your test asset for Project 2."),
 ],
 "exercises": [
   "Implement homogeneous media with analytic distance sampling. Render a "
   "fog-filled Cornell box and verify the transmittance against the "
   "analytic Beer&ndash;Lambert value.",
   "Implement isotropic and Henyey&ndash;Greenstein phase functions. Verify "
   "both with &chi;&#178; tests. Render a medium at g = &minus;0.5, 0, and "
   "0.8 and describe the difference.",
   "Implement ray marching for a heterogeneous medium. Plot the result "
   "against step size and demonstrate that the error does not vanish with "
   "more pixel samples.",
   "Implement delta tracking. Confirm it matches the ray-marched result as "
   "the step size goes to zero, and that it needs no step parameter.",
   "Implement ratio tracking for transmittance. Compare the variance of "
   "shadow rays against using delta tracking for the same purpose.",
   "Build a majorant grid for the Disney cloud and report the reduction in "
   "null collisions against a single global majorant.",
   "Render the Disney cloud. Report render time as a function of maximum "
   "scattering events, and identify where the image stops changing.",
   "Implement equiangular sampling for a light inside a medium and combine "
   "it with transmittance sampling using MIS. Report the variance reduction.",
   "Render a dense high-albedo medium inside a dielectric boundary to "
   "produce subsurface scattering. Compare against a diffusion "
   "approximation if you implement one.",
 ],
 "selfcheck": [
   "Define the three coefficients and the single-scattering albedo, and say "
   "which governs cost.",
   "Why does a medium break radiance invariance, and what does that do to "
   "the cost of a ray?",
   "Write the transmittance and explain why heterogeneous media are hard.",
   "How is distance sampled in a homogeneous medium, and what cancels in the "
   "estimator?",
   "How does a phase function differ from a BRDF, and why is "
   "Henyey–Greenstein popular?",
   "Why is ray marching biased, and why does increasing pixel samples not "
   "fix it?",
   "Explain delta tracking and say precisely why the fictitious matter does "
   "not bias the result.",
   "When should you use ratio tracking instead of delta tracking, and why?",
   "What does the majorant affect, and what does a majorant grid do?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Bidirectional Methods",
 "subtitle": "Building paths from both ends, and when it is worth it.",
 "question": "What transport can a path tracer not find?",
 "outcomes": [
     "Explain why path tracing fails on caustics and SDS paths.",
     "Describe light tracing and its complementary strengths.",
     "Explain bidirectional path tracing and its connection strategies.",
     "Explain photon mapping and what kind of bias it has.",
     "Choose an algorithm from the transport a scene contains.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What path tracing cannot do",
   "blurb": "Specific transport, specifically hard."},

  {"t": "callout", "title": "Caustics are the canonical failure",
   "kind": "Why",
   "body": ["Light through a glass sphere converges onto a floor. The path "
            "is: eye → floor → <b>specular</b> → light.",
            "<b>NEE cannot help at the specular vertex</b>, because a shadow "
            "ray from the glass has zero probability of being the exact "
            "refracted direction (Module 08).",
            "<b>So the path must find the light by BSDF sampling through the "
            "glass</b>, which requires hitting a small light through a "
            "narrow refracted cone.",
            "The probability is tiny, the contribution is large, and the "
            "result is fireflies that never converge. <b>Caustics are the "
            "standard demonstration that unidirectional path tracing is "
            "incomplete.</b>"]},

  {"t": "table", "kicker": "Notation", "title": "Heckbert path notation",
   "header": ["Notation", "Means", "Example"],
   "widths": [2.4, 5.0, 4.7],
   "rows": [
     ["L", "The light source", "—"],
     ["E", "The eye", "—"],
     ["D", "A diffuse vertex", "Wall, floor"],
     ["S", "A specular vertex", "Mirror, glass"],
     ["LDE", "Direct lighting", "<b>Easy</b>"],
     ["LD*E", "Diffuse global illumination", "<b>Path tracing's home</b>"],
     ["LSDE", "A caustic", "<b>Hard for path tracing</b>"],
     ["LSDSE", "<b>SDS — the hard case</b>", "<b>Light in water, seen through glass</b>"],
   ],
   "note": "The notation is worth learning: papers assume it, and it names "
           "the problem precisely."},

  {"t": "callout", "title": "SDS paths defeat both directions",
   "kind": "The genuinely hard case",
   "body": ["A specular-diffuse-specular path: a light submerged in water "
            "and seen through the glass of the tank; a car headlight behind "
            "its lens, reflected in a puddle.",
            "<b>From the eye</b>, you must hit the light through a specular "
            "chain — probability near zero.",
            "<b>From the light</b>, you must hit the <i>eye</i> through a "
            "specular chain — also near zero.",
            "<b>Bidirectional path tracing does not fix this either</b>, "
            "because the connection between the two subpaths also lands on a "
            "specular vertex and has zero contribution. This is what "
            "Metropolis and photon mapping exist for."]},

  {"t": "section", "label": "Part 2", "title": "Light tracing",
   "blurb": "The same algorithm, run backwards."},

  {"t": "two", "kicker": "Mirror image", "title": "Path tracing and light tracing",
   "lh": "Path tracing — from the eye",
   "l": ["Start at the camera, scatter, connect to lights.",
         "<b>Good:</b> most direct and diffuse transport.",
         "<b>Bad:</b> caustics; small bright lights behind specular.",
         ("Every path contributes to one known pixel.", 1)],
   "rh": "Light tracing — from the light",
   "r": ["Start at a light, scatter, connect to the camera.",
         "<b>Good:</b> caustics; light through glass.",
         "<b>Bad:</b> directly visible surfaces, which are trivially easy "
         "from the eye.",
         ("Paths splat into whichever pixel they reach.", 1)],
   "note": "The asymmetry is the point: they are good at different things "
           "because of where their samples are concentrated."},

  {"t": "callout", "title": "Light tracing requires a camera you can connect to",
   "kind": "A practical constraint",
   "body": ["To connect a light path to the camera you must evaluate the "
            "camera's <b>importance function</b> — the sensitivity of a "
            "pixel to radiance arriving from a direction.",
            "<b>A pinhole camera has an importance that is a delta "
            "distribution</b>, so the probability of a random light path "
            "hitting it is zero, exactly as for a point light.",
            "<b>So light tracing needs a camera with a finite aperture</b>, "
            "or a special connection step that projects the vertex onto the "
            "sensor.",
            "The symmetry with Module 09's delta lights is exact, and it is "
            "the reason the measurement equation in Veach's thesis is "
            "written the way it is."]},

  {"t": "section", "label": "Part 3", "title": "Bidirectional path tracing",
   "blurb": "Build both, connect every way, weight with MIS."},

  {"t": "bullets", "kicker": "BDPT", "title": "The algorithm",
   "items": [
     "<b>1.</b> Trace a subpath from the camera: vertices z&#8320;, "
     "z&#8321;, …",
     "<b>2.</b> Trace a subpath from a light: y&#8320;, y&#8321;, …",
     "<b>3.</b> <b>Connect every camera vertex to every light vertex</b> "
     "with a shadow ray.",
     "<b>4.</b> A path of length k can be formed in k+1 ways — these are "
     "<i>different sampling strategies for the same path</i>.",
     "<b>5.</b> <b>Weight them with MIS.</b> Module 08's machinery, applied "
     "across strategies rather than within a vertex.",
     "",
     "The strategies include path tracing (connect at the light) and light "
     "tracing (connect at the camera) as special cases.",
   ],
   "note": "Step 5 is why BDPT was possible: Veach invented MIS in the same "
           "thesis, because BDPT does not work without it."},

  {"t": "callout", "title": "BDPT is strictly more capable and often slower",
   "kind": "An honest assessment",
   "body": ["<b>It handles everything path tracing does, plus caustics and "
            "difficult indirect lighting</b>, with no configuration.",
            "<b>But each sample is far more expensive</b> — O(k²) "
            "connections per path pair, each one a shadow ray — and on "
            "ordinary diffuse scenes those extra strategies contribute "
            "almost nothing.",
            "<b>At equal time it frequently loses to a well-tuned path "
            "tracer</b> on the scenes people actually render.",
            "<b>It is also substantially harder to implement correctly</b>, "
            "because the MIS weights must account for every way each path "
            "could have been generated. This is the usual reason production "
            "renderers offer it and default to path tracing."]},

  {"t": "section", "label": "Part 4", "title": "Photon mapping and Metropolis",
   "blurb": "Two ways to trade correctness guarantees for capability."},

  {"t": "bullets", "kicker": "Photon mapping", "title": "Store the light paths, then look them up",
   "items": [
     "<b>Pass 1:</b> trace photons from the lights; store each interaction "
     "in a spatial structure.",
     "<b>Pass 2:</b> trace from the eye; at each vertex, estimate radiance "
     "by gathering nearby photons.",
     "",
     "<b>Biased:</b> the gather radius blurs over a finite area, so the "
     "estimate is not local.",
     "<b>Consistent:</b> with more photons the radius shrinks and the bias "
     "vanishes — in the limit.",
     "",
     "<b>Excellent at caustics</b>, because photons naturally concentrate "
     "exactly where caustics are bright.",
     "<b>Progressive photon mapping</b> removes the memory limit by "
     "shrinking the radius across passes.",
   ],
   "note": "The bias is spatial blur. It is why photon-mapped caustics look "
           "slightly soft even when converged."},

  {"t": "callout", "title": "Metropolis light transport: explore near paths that worked",
   "kind": "The idea",
   "body": ["Treat path space as a distribution to be sampled, and use "
            "Markov chain Monte Carlo: having found a bright path, mutate it "
            "slightly and accept or reject.",
            "<b>Once a hard path is found, its neighbours are found "
            "cheaply.</b> This is exactly what SDS transport needs — the "
            "paths are rare but clustered.",
            "<b>The costs are real:</b> samples are correlated, so error "
            "appears as splotches rather than noise; convergence is hard to "
            "assess; and it is difficult to implement and to tune.",
            "<b>Used in production mostly for specific hard shots</b>, not "
            "as a default. Primary-sample-space MLT is the easier variant to "
            "implement."]},

  {"t": "table", "kicker": "Choosing", "title": "Which algorithm for which scene",
   "header": ["Scene", "Best choice"],
   "widths": [6.0, 6.1],
   "rows": [
     ["Diffuse interior, area lights", "<b>Path tracing + MIS</b>"],
     ["Caustics through glass or water", "Photon mapping or BDPT"],
     ["Strong indirect through a small opening", "BDPT"],
     ["<b>SDS paths</b>", "<b>MLT or photon mapping</b>"],
     ["Production, general", "<b>Path tracing + MIS + denoiser</b>"],
   ],
   "footnote": "The last row is what almost everyone actually ships.",
   "note": "Be honest here: the sophisticated methods lost to a good path "
           "tracer plus a denoiser for most work."},

  {"t": "callout", "title": "Why the simple method won",
   "kind": "An honest conclusion",
   "body": ["Path tracing with MIS is <b>simple, robust, parallelises "
            "trivially, and has predictable memory</b>.",
            "The sophisticated methods each win decisively on a narrow class "
            "of transport and lose or merely tie elsewhere — while "
            "costing far more to implement and maintain.",
            "<b>Then denoising (Module 12) changed the economics.</b> If a "
            "noisy path-traced image can be cleaned acceptably, the "
            "variance advantage of BDPT on a few scenes stops justifying "
            "its complexity.",
            "<b>Know these methods anyway.</b> They tell you what kind of "
            "transport your scene contains, which is exactly what you need "
            "when the default renderer will not converge."]},
 ],
 "takeaways": [
   "Path tracing fails on caustics because NEE cannot operate at a specular "
   "vertex, so the light must be found through a narrow refracted cone.",
   "Heckbert notation names paths precisely: LDE is direct, LD*E is "
   "path tracing's home, LSDE is a caustic, LSDSE is the hard case.",
   "SDS paths defeat both directions and BDPT's connections, which is what "
   "Metropolis and photon mapping exist for.",
   "Light tracing is the mirror image, good at exactly what path tracing is "
   "bad at — and needs a camera with finite aperture.",
   "BDPT connects every camera vertex to every light vertex and weights the "
   "strategies with MIS. Strictly more capable, often slower at equal time.",
   "Photon mapping is biased but consistent — the bias is spatial blur "
   "from the gather radius — and excels at caustics.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What path tracing cannot find"),
  ("callout", "The caustic problem",
   ["Consider light focused through a glass sphere onto a floor. The "
    "transport path is: eye &rarr; floor (diffuse) &rarr; glass "
    "(<b>specular</b>) &rarr; light.",
    "<b>Next-event estimation cannot help at the specular vertex.</b> As "
    "Module 08 established, a shadow ray from a specular surface has zero "
    "probability of being the exact refracted direction, so the light "
    "sampling strategy contributes nothing there.",
    "<b>So the path must find the light by BSDF sampling</b>: refract "
    "through the glass and happen to strike the light. For a small light "
    "and a narrow refracted cone, the probability is minute — and when "
    "it succeeds, the contribution is enormous, because the caustic is "
    "bright.",
    "<b>That is precisely the firefly condition of Module 05</b>: rare "
    "events with large values. The caustic appears as scattered bright "
    "pixels that converge extraordinarily slowly, and it is the standard "
    "demonstration that unidirectional path tracing is incomplete rather "
    "than merely slow."]),
  ("h2", "1.1 &nbsp; Heckbert path notation"),
  ("table", ["Notation", "Meaning", "Difficulty"],
   [["<b>L</b>, <b>E</b>", "Light source; eye.", "—"],
    ["<b>D</b>, <b>S</b>", "A diffuse vertex; a specular vertex.", "—"],
    ["<b>LDE</b>", "Light, one diffuse bounce, eye. Direct lighting.",
     "<b>Easy.</b> NEE handles it."],
    ["<b>LD*E</b>", "Any number of diffuse bounces.",
     "<b>Path tracing's home ground.</b> This is what it is good at."],
    ["<b>LSDE</b>", "Light, specular, diffuse, eye. <b>A caustic.</b>",
     "<b>Hard for path tracing</b>, easy for light tracing and photon "
     "mapping."],
    ["<b>LSDSE</b>", "<b>Specular&ndash;diffuse&ndash;specular.</b> A light "
     "under water, viewed through the glass of the tank.",
     "<b>Hard for everything.</b> See below."]],
   [0.14, 0.48, 0.38]),
  ("p", "The notation is worth learning: the literature assumes it, and it "
        "names a transport problem precisely enough to reason about which "
        "algorithm can handle it."),
  ("callout", "SDS paths defeat both directions",
   ["A specular&ndash;diffuse&ndash;specular path requires reaching a "
    "diffuse surface through a specular chain from <i>both</i> ends. The "
    "canonical examples are a light submerged in a water tank viewed through "
    "the glass, and a car headlight behind its lens reflected in a wet road.",
    "<b>From the eye:</b> you must traverse the specular chain and then hit "
    "the light. Probability near zero.",
    "<b>From the light:</b> you must traverse the other specular chain and "
    "then hit the eye. Also near zero.",
    "<b>And bidirectional path tracing does not rescue it</b>, because the "
    "connection step between the camera and light subpaths must land on a "
    "vertex where a deterministic connection has non-zero contribution "
    "— and a specular vertex does not. Every BDPT strategy for an SDS "
    "path has zero or near-zero probability.",
    "This is the transport that Metropolis light transport and photon "
    "mapping exist to handle, and it is why those methods survive despite "
    "their disadvantages."]),

  ("h1", "2 &nbsp; Light tracing"),
  ("table", ["", "Path tracing", "Light tracing"],
   [["Starts at", "The camera.", "A light source."],
    ["Connects to", "Lights, by shadow ray (NEE).",
     "The camera, by projecting the vertex onto the sensor."],
    ["Good at", "Directly visible surfaces; diffuse interreflection; most "
     "ordinary transport.",
     "<b>Caustics</b>; light through glass; illumination that is hard to "
     "find from the eye."],
    ["Bad at", "<b>Caustics</b>; small bright lights behind specular "
     "surfaces.",
     "Directly visible surfaces — trivially easy from the eye, and "
     "wasteful to find from the light."],
    ["Pixel assignment", "Every path contributes to one known pixel.",
     "Paths splat into whichever pixel they happen to reach, so the image "
     "must be accumulated rather than computed per pixel."]],
   [0.14, 0.42, 0.44]),
  ("callout", "Light tracing needs a camera with an aperture",
   ["To connect a light path to the camera you must evaluate the camera's "
    "<b>importance function</b> — the sensitivity of a given pixel to "
    "radiance arriving from a given direction. This is the exact dual of a "
    "light's emitted radiance, and Veach's measurement equation is written "
    "to make the symmetry explicit.",
    "<b>A pinhole camera's importance is a delta distribution.</b> The "
    "probability that a randomly generated light path passes exactly through "
    "an infinitesimal pinhole is zero, so no light path can ever be "
    "connected to it by chance.",
    "<b>So light tracing requires either a camera with a finite aperture</b> "
    "— a thin-lens model — <b>or a deterministic connection "
    "step</b> that projects the vertex onto the sensor plane and evaluates "
    "the importance there.",
    "<b>The symmetry with Module 09's delta lights is exact.</b> A point "
    "light cannot be hit by a BSDF-sampled ray and exists only through "
    "explicit connection; a pinhole camera cannot be hit by a light path and "
    "exists only through explicit connection. The same mathematics, mirrored."]),

  ("break",),
  ("h1", "3 &nbsp; Bidirectional path tracing"),
  ("ol", ["Trace a subpath from the camera, producing vertices z&#8320;, "
          "z&#8321;, z&#8322;, &hellip;",
          "Trace a subpath from a light, producing y&#8320;, y&#8321;, "
          "y&#8322;, &hellip;",
          "<b>Connect every camera vertex to every light vertex</b> with a "
          "shadow ray, evaluating the BSDFs at both ends and the geometry "
          "term between.",
          "A complete path with k vertices can be constructed in k+1 "
          "different ways, depending on how many vertices came from each "
          "subpath. <b>These are different sampling strategies for the same "
          "path.</b>",
          "<b>Combine them with multiple importance sampling.</b>"]),
  ("p", "Step 5 is the reason BDPT works, and it is why MIS and BDPT appear "
        "in the same thesis: Veach needed MIS in order to make BDPT "
        "function. Without a principled way to weight the many strategies "
        "that can generate the same path, the method either double-counts or "
        "must arbitrarily discard strategies."),
  ("p", "Note that the family of strategies <i>includes</i> the ones we "
        "already know. Connecting the camera subpath directly to a light is "
        "path tracing with NEE; connecting a light subpath directly to the "
        "camera is light tracing. BDPT generalises both and adds every "
        "intermediate option."),
  ("callout", "Strictly more capable, frequently slower",
   ["<b>BDPT handles everything path tracing handles, plus caustics and "
    "difficult indirect illumination</b> — light entering a room "
    "through a small gap, for instance — without any per-scene "
    "configuration.",
    "<b>But each sample costs far more.</b> Connecting every pair of "
    "vertices is O(k&#178;) shadow rays per path pair, and on an ordinary "
    "diffuse scene the great majority of those extra strategies contribute "
    "almost nothing to the final image.",
    "<b>At equal time it frequently loses to a well-implemented path tracer "
    "with MIS</b> on the kinds of scene people actually render. It wins "
    "decisively on the scenes it was designed for and ties or loses "
    "elsewhere.",
    "<b>It is also considerably harder to implement correctly.</b> The MIS "
    "weights must account for the probability of generating each path under "
    "every strategy, including ones that were not used, and a subtle error "
    "produces a result that is wrong only in certain configurations. "
    "Production renderers typically offer BDPT and default to path "
    "tracing."]),

  ("h1", "4 &nbsp; Photon mapping"),
  ("p", "A two-pass method that decouples finding light transport from "
        "shading."),
  ("ol", ["<b>Pass 1:</b> trace photons from the light sources into the "
          "scene, storing each interaction — position, incoming "
          "direction, and power — in a spatial data structure, "
          "typically a kd-tree or a hash grid.",
          "<b>Pass 2:</b> trace paths from the camera. At each vertex where "
          "a radiance estimate is needed, gather the nearest photons within "
          "some radius and estimate the incoming radiance from their density "
          "and power."]),
  ("table", ["Property", "Assessment"],
   [["<b>Biased</b>",
     "The gather averages photons over a finite area, so the estimate is not "
     "local. Radiance is blurred spatially — which is why "
     "photon-mapped caustics look slightly soft even when fully converged."],
    ["<b>Consistent</b>",
     "As the photon count grows the gather radius can shrink, and the bias "
     "vanishes in the limit. This is the standard example of the "
     "consistent-but-biased category from Module 05."],
    ["<b>Excellent at caustics</b>",
     "Photons travel from the light <i>through</i> the glass and land "
     "exactly where the caustic is bright. The density of stored photons is "
     "naturally proportional to the illumination, which is precisely what "
     "the hard case needs."],
    ["<b>Memory-bound</b>",
     "Quality is limited by how many photons fit in memory. <b>Progressive "
     "photon mapping</b> removes this constraint by running many passes with "
     "a shrinking radius and accumulating, trading memory for time and "
     "remaining consistent."]],
   [0.17, 0.83]),

  ("h1", "5 &nbsp; Metropolis light transport"),
  ("callout", "Explore the neighbourhood of paths that worked",
   ["MLT treats the space of all light paths as a distribution to be sampled "
    "and applies Markov chain Monte Carlo: having found a path that carries "
    "significant energy, propose a small mutation of it, and accept or "
    "reject according to the Metropolis rule.",
    "<b>Once a difficult path has been found, its neighbours are found "
    "almost for free.</b> That is exactly the property SDS transport "
    "requires — such paths are extremely rare but strongly clustered "
    "in path space, so a method that explores locally once it arrives is "
    "ideally suited.",
    "<b>The costs are substantial.</b> Successive samples are correlated, so "
    "the error does not look like noise — it looks like splotches and "
    "uneven brightness, which many people find more objectionable. "
    "Convergence is difficult to assess, because the usual variance "
    "estimates assume independence. And start-up bias, mutation design, and "
    "chain management are all genuinely hard to get right.",
    "<b>In production it is used for specific difficult shots rather than as "
    "a default.</b> Primary-sample-space MLT, which mutates the random "
    "numbers driving an ordinary path tracer rather than the path vertices "
    "themselves, is far easier to implement and is the version to try "
    "first."]),

  ("h1", "6 &nbsp; Choosing"),
  ("table", ["Scene characteristics", "Best choice", "Why"],
   [["Diffuse interior lit by area lights.",
     "<b>Path tracing with MIS.</b>",
     "LD*E transport is exactly what it is good at."],
    ["Caustics through glass or water.", "Photon mapping, or BDPT.",
     "Light-side construction finds LSDE paths naturally."],
    ["Strong indirect through a small opening.", "BDPT.",
     "Light subpaths get through the opening; camera subpaths struggle to "
     "find it."],
    ["<b>SDS paths</b> — submerged lights, lens caustics.",
     "<b>MLT, or photon mapping.</b>",
     "Nothing else can construct these paths with non-zero probability."],
    ["<b>General production work.</b>",
     "<b>Path tracing + MIS + a denoiser.</b>",
     "<b>What almost everyone ships.</b>"]],
   [0.30, 0.27, 0.43]),
  ("callout", "Why the simple method won",
   ["Path tracing with MIS is simple to implement, robust across scene "
    "types, trivially parallel, and has flat, predictable memory use. Those "
    "properties matter enormously in a production pipeline, where "
    "an algorithm that is occasionally twice as fast and occasionally "
    "catastrophically wrong is worse than one that is uniformly adequate.",
    "The sophisticated methods each win decisively on a narrow class of "
    "transport and tie or lose elsewhere, while costing far more to "
    "implement, tune, and maintain.",
    "<b>Then denoising changed the economics entirely.</b> If a noisy "
    "path-traced image at 64 samples can be cleaned to an acceptable "
    "result, BDPT's variance advantage on a subset of scenes no longer "
    "justifies its complexity. Module 12 covers this.",
    "<b>Learn these methods anyway</b>, and not out of completeness. They "
    "give you the vocabulary to say what kind of transport a scene contains "
    "— and when your default renderer refuses to converge on a shot, "
    "knowing that it is an SDS problem rather than a sampling problem is the "
    "difference between fixing it and not."]),
 ],
 "resources": [
   ("Veach thesis &mdash; Chapters 10 and 11, BDPT and MLT",
    "https://graphics.stanford.edu/papers/veach_thesis/",
    "The original source for both methods, including the measurement "
    "equation and the camera importance function of &sect;2."),
   ("PBRT 4th ed. &mdash; Chapter 13 and the online BDPT chapter",
    "https://pbr-book.org/",
    "BDPT with complete code, including the MIS weight computation, which is "
    "the part that is hard to get right."),
   ("Jensen &mdash; Realistic Image Synthesis Using Photon Mapping",
    "https://graphics.stanford.edu/~henrik/papers/",
    "Photon mapping from its author; the papers are free on this page."),
   ("Hachisuka & Jensen &mdash; Progressive Photon Mapping (free)",
    "https://cs.uwaterloo.ca/~thachisu/",
    "The method that removed photon mapping's memory limit while keeping "
    "consistency."),
   ("Kelemen et al. &mdash; Primary Sample Space MLT (free)",
    "https://www.sciencedirect.com/science/article/pii/S0097849302001441",
    "The far simpler MLT variant mentioned in &sect;5. Start here if you "
    "implement one."),
 ],
 "exercises": [
   "Render a glass sphere above a diffuse floor with your path tracer. "
   "Report how many samples are needed before the caustic is acceptable, "
   "and whether it ever is.",
   "Classify ten transport paths in a scene of your choosing using Heckbert "
   "notation, and predict which your path tracer will struggle with.",
   "Implement light tracing. Render the glass sphere scene with it and "
   "compare against path tracing at equal time.",
   "Demonstrate the pinhole problem: attempt light tracing with a pinhole "
   "camera and explain the result. Then add a finite aperture.",
   "Construct an SDS scene — a light inside a glass enclosure, viewed "
   "through another glass surface. Render it with path tracing and with "
   "light tracing and document that both fail.",
   "Implement BDPT with the full set of connection strategies. Verify that "
   "disabling all strategies except one reproduces path tracing, and another "
   "reproduces light tracing.",
   "For a BDPT implementation, render each connection strategy to a separate "
   "image buffer. Looking at which strategies contribute where is the "
   "clearest possible explanation of the algorithm.",
   "Implement basic photon mapping for caustics only, combined with path "
   "tracing for everything else. Compare the caustic quality against path "
   "tracing at equal time.",
   "Vary the photon gather radius and show the bias explicitly: the caustic "
   "should visibly blur as the radius grows.",
   "Write a page recommending an algorithm for three scenes of your choice, "
   "justifying each from the transport they contain.",
 ],
 "selfcheck": [
   "Why does path tracing fail on caustics? Be precise about which strategy "
   "fails and why.",
   "Write Heckbert notation for direct lighting, diffuse GI, a caustic, and "
   "the hard case.",
   "Why do SDS paths defeat both path tracing and light tracing, and why "
   "does BDPT not fix them?",
   "What is light tracing good at, and why does it need a camera with an "
   "aperture?",
   "What is the camera importance function, and what is it the dual of?",
   "Describe BDPT's connection strategies and say why MIS is essential to "
   "it.",
   "Why is BDPT often slower than path tracing at equal time despite being "
   "more capable?",
   "In what sense is photon mapping biased, and in what sense consistent?",
   "What property of SDS transport makes Metropolis suited to it, and what "
   "does MLT's error look like?",
   "Why did path tracing with MIS win, and what did denoising change?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Denoising and Adaptive Sampling",
 "subtitle": "Spending samples where they help, and cleaning up what is "
             "left.",
 "question": "How do you get a clean image without waiting for convergence?",
 "outcomes": [
     "Estimate per-pixel variance and drive adaptive sampling with it.",
     "Explain how auxiliary feature buffers make denoising possible.",
     "Implement an edge-aware à-trous filter.",
     "Compare hand-designed and learned denoisers honestly.",
     "Explain ReSTIR's core idea and why it mattered.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Adaptive sampling",
   "blurb": "Not every pixel needs the same effort."},

  {"t": "callout", "title": "Variance is enormously uneven across an image",
   "kind": "The opportunity",
   "body": ["A flat, directly lit wall converges in a handful of samples. "
            "A caustic or a glossy reflection of a small light may need "
            "thousands.",
            "<b>Uniform sampling gives both the same budget</b>, which is "
            "simultaneously wasteful and insufficient.",
            "<b>Estimate per-pixel variance and allocate accordingly.</b> "
            "The running variance of the samples already drawn is free — "
            "accumulate sum and sum-of-squares.",
            "Typical gains are <b>2–4× at equal quality</b>, which is "
            "worth having and is not transformative on its own."]},

  {"t": "callout", "title": "Adaptive sampling can introduce bias",
   "kind": "The subtlety",
   "body": ["If the decision to take more samples depends on the samples "
            "themselves, the estimator is <b>no longer independent</b> and "
            "may be biased.",
            "A pixel that happens to draw low samples early looks converged "
            "and is starved — so dark pixels stay dark.",
            "<b>The usual defence:</b> take a fixed initial budget before "
            "adapting, and cap the ratio between the largest and smallest "
            "allocation.",
            "<b>In practice the bias is small and everyone accepts it</b> "
            "— but say so, rather than claiming an unbiased renderer "
            "while adapting."]},

  {"t": "section", "label": "Part 2", "title": "Feature buffers",
   "blurb": "The information that makes denoising tractable."},

  {"t": "callout", "title": "Denoising an image is hard; denoising a render is not",
   "kind": "Why rendering is a special case",
   "body": ["General image denoising must guess what is signal and what is "
            "noise. It is an underdetermined problem.",
            "<b>A renderer knows things a photograph does not.</b> It can "
            "output, noise-free: albedo, surface normal, depth, object ID, "
            "and motion vectors.",
            "<b>These tell the filter exactly where the edges are</b>, so it "
            "can blur aggressively <i>along</i> a surface and not at all "
            "across a boundary.",
            "<b>That is why render denoising works far better than photo "
            "denoising.</b> The hard part of the problem was solved by "
            "having access to the scene."]},

  {"t": "table", "kicker": "Buffers", "title": "What to output alongside the image",
   "header": ["Buffer", "Tells the denoiser", "Noise-free?"],
   "widths": [2.8, 5.8, 3.5],
   "rows": [
     ["Albedo", "Texture detail, so it is not smoothed away", "<b>Yes</b>"],
     ["Normal", "Geometric edges and curvature", "<b>Yes</b>"],
     ["Depth", "Depth discontinuities", "<b>Yes</b>"],
     ["Object ID", "Hard boundaries between objects", "<b>Yes</b>"],
     ["Motion vectors", "Where each pixel was last frame", "<b>Yes</b>"],
     ["Variance", "How much to trust each pixel", "Estimated"],
   ],
   "footnote": "<b>Demodulate by albedo before filtering, then remodulate.</b> "
               "Filtering illumination rather than colour preserves texture.",
   "note": "The demodulation trick is the single most effective detail here "
           "and is often omitted."},

  {"t": "code", "kicker": "Filter", "title": "Edge-aware à-trous wavelet filter",
   "lang": "cpp", "code": """
// Several passes with an increasing hole size: a wide filter at
// O(n) cost instead of O(n^2). SVGF is built on this.
vec3 atrous(const Buffers& b, ivec2 p, int step) {
    vec3  sum(0);  float wsum = 0;
    for (int dy = -2; dy <= 2; dy++)
    for (int dx = -2; dx <= 2; dx++) {
        ivec2 q = p + ivec2(dx, dy) * step;       // <-- the hole
        if (!inside(q)) continue;

        // Edge-stopping: each term kills the weight across a discontinuity.
        float wn = powf(fmaxf(0.f, dot(b.normal[p], b.normal[q])), SIGMA_N);
        float wz = expf(-fabs(b.depth[p] - b.depth[q]) / (SIGMA_Z + 1e-6f));
        float wl = expf(-fabs(lum(b.color[p]) - lum(b.color[q]))
                        / (SIGMA_L * sqrtf(b.variance[p]) + 1e-6f));

        float w = kernel[dy+2][dx+2] * wn * wz * wl;
        sum += b.color[q] * w;  wsum += w;
    }
    return wsum > 0 ? sum / wsum : b.color[p];
}
""",
   "caption": "The luminance weight is scaled by the estimated variance: "
              "where the image is noisy, large differences are tolerated as "
              "noise rather than defended as edges.",
   "note": "That variance-scaled luminance term is the clever part. Without "
           "it the filter preserves noise as though it were detail."},

  {"t": "section", "label": "Part 3", "title": "Learned denoisers",
   "blurb": "What they buy and what they cost."},

  {"t": "two", "kicker": "Comparison", "title": "Hand-designed and learned",
   "lh": "À-trous / SVGF",
   "l": ["Explicit, inspectable weights.",
         "Fails predictably: over-blur, ghosting.",
         "<b>Tunable when it fails.</b>",
         ("Fast; real-time viable.", 1),
         "Weaker on very low sample counts."],
   "rh": "Learned (OIDN, OptiX)",
   "r": ["Trained on pairs of noisy and converged images.",
         "<b>Substantially better at low sample counts.</b>",
         "<b>Fails unpredictably</b> — may hallucinate detail that was "
         "never there.",
         ("Heavier; needs a GPU.", 1),
         "The production default for offline work."],
   "note": "The hallucination point is the honest one. A learned denoiser "
           "can invent plausible detail, which is a correctness problem."},

  {"t": "callout", "title": "Denoising is biased, and it is the right trade",
   "kind": "Be explicit about it",
   "body": ["A denoiser changes pixel values based on neighbouring pixels. "
            "<b>The result is not an unbiased estimate of anything.</b>",
            "It can remove real high-frequency detail — fine texture, "
            "small highlights, thin shadows — and a learned denoiser can "
            "add detail that was never in the scene.",
            "<b>And it is still correct to use one.</b> A denoised 64-sample "
            "image is usually closer to the truth than a 1024-sample noisy "
            "one at the same cost.",
            "<b>Report it.</b> Say the image is denoised, give the sample "
            "count, and show the noisy input and a converged reference "
            "alongside. That is what Project 2 asks for."]},

  {"t": "section", "label": "Part 4", "title": "ReSTIR",
   "blurb": "The most consequential rendering result of the last decade."},

  {"t": "bullets", "kicker": "ReSTIR", "title": "Resample instead of sampling again",
   "items": [
     "<b>Reservoir sampling</b> keeps one sample from a stream, chosen with "
     "the correct probability, in constant memory.",
     "",
     "<b>Spatial reuse:</b> a neighbouring pixel's light sample is probably "
     "good for this pixel too — combine reservoirs.",
     "",
     "<b>Temporal reuse:</b> last frame's sample for this surface is "
     "probably still good — combine across time.",
     "",
     "<b>The effect is an enormous increase in effective sample count</b> "
     "for a small cost, because each pixel benefits from work done "
     "elsewhere and earlier.",
     "",
     "<b>Millions of lights, in real time, with one sample per pixel.</b>",
   ],
   "note": "Reservoir resampling is old; the contribution was realising it "
           "could be reused across space and time."},

  {"t": "callout", "title": "Why ReSTIR mattered",
   "kind": "Assessment",
   "body": ["It attacks the <b>constant</b> in Module 05's 1/√N, which is "
            "the only thing that can be attacked — and it attacks it by "
            "orders of magnitude rather than factors.",
            "<b>It changed what is possible in real time</b>, not just what "
            "is faster offline. Many-light direct illumination went from "
            "impossible to routine.",
            "<b>The costs are real:</b> reused samples are correlated, which "
            "shows as structured rather than random error; and the bias "
            "correction (MIS weights across reservoirs) is subtle and easy "
            "to get wrong.",
            "<b>It also generalises</b> — ReSTIR GI and ReSTIR PT extend "
            "the idea to full path reuse."]},

  {"t": "callout", "title": "Denoising changed what the field optimises",
   "kind": "The honest conclusion",
   "body": ["Before practical denoising, variance reduction was the only "
            "lever, and the sophisticated algorithms of Module 11 competed "
            "on it.",
            "<b>Now the question is: what noise does the denoiser handle "
            "well?</b> That is a different objective and favours different "
            "methods.",
            "<b>High-frequency noise denoises well. Fireflies and correlated "
            "splotches do not.</b> So a method with slightly higher variance "
            "but better-behaved noise can win outright.",
            "<b>This is why blue noise (Module 06) matters</b> and why "
            "Metropolis's splotchy error is a liability rather than a "
            "cosmetic complaint."]},
 ],
 "takeaways": [
   "Per-pixel variance is extremely uneven; adaptive sampling buys "
   "2–4&times; at equal quality, with a small bias that should be "
   "acknowledged.",
   "A renderer can output albedo, normal, depth, ID, and motion noise-free. "
   "That is why render denoising works where photo denoising struggles.",
   "Demodulate by albedo before filtering and remodulate after — filter "
   "illumination, not colour, so texture survives.",
   "The &agrave;-trous filter gets a wide kernel at linear cost; the "
   "variance-scaled luminance weight is what stops it preserving noise as "
   "detail.",
   "Learned denoisers are better at low sample counts and fail "
   "unpredictably, including hallucinating detail. Report that an image is "
   "denoised.",
   "ReSTIR reuses samples across space and time, attacking the constant in "
   "1/&radic;N by orders of magnitude. Reused samples are correlated.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Adaptive sampling"),
  ("callout", "Variance is wildly uneven across an image",
   ["A flat wall lit directly by a large area light converges in a handful "
    "of samples. A caustic on the floor beside it, or a glossy reflection of "
    "a small bright light, may need thousands to reach the same error.",
    "<b>Uniform sampling gives both the same budget</b>, which "
    "simultaneously wastes effort on the easy regions and starves the hard "
    "ones.",
    "<b>The fix is to estimate per-pixel variance and allocate "
    "accordingly.</b> The estimate is essentially free: accumulate the sum "
    "and the sum of squares of the samples already drawn, and the running "
    "variance follows.",
    "<b>Typical gains are two to four times at equal quality.</b> Worth "
    "having, and not transformative on its own — the techniques later "
    "in this module matter more."]),
  ("callout", "Adaptive sampling introduces a small bias",
   ["If the decision to draw more samples depends on the values of the "
    "samples already drawn, those samples are <b>no longer independent of "
    "the stopping rule</b>, and the estimator is not strictly unbiased.",
    "The mechanism is concrete: a pixel whose first few samples happen to be "
    "low looks converged, gets starved of further samples, and stays low. "
    "The effect is systematic and slightly darkens regions with "
    "high-variance, high-value transport.",
    "<b>The standard defences</b> are to draw a fixed initial budget before "
    "any adaptation, and to cap the ratio between the largest and smallest "
    "per-pixel allocation.",
    "<b>In practice the residual bias is small and essentially everyone "
    "accepts it.</b> The point is to accept it knowingly — do not "
    "describe a renderer as unbiased while it adapts."]),

  ("h1", "2 &nbsp; Feature buffers"),
  ("callout", "Rendering is a uniquely favourable case for denoising",
   ["Denoising a photograph is fundamentally underdetermined: the algorithm "
    "must infer which variations are signal and which are sensor noise, with "
    "no information beyond the image itself.",
    "<b>A renderer knows a great deal that a camera does not.</b> It can "
    "output, with no noise at all, the surface albedo, the shading normal, "
    "the depth, the object identifier, and the motion vector for every "
    "pixel — because these are properties of the first intersection, "
    "which is deterministic.",
    "<b>These buffers tell the filter precisely where the edges are.</b> It "
    "can then blur aggressively along a smooth surface while refusing to "
    "blur across a geometric boundary, a depth discontinuity, or an object "
    "edge.",
    "<b>This is why render denoising works far better than photo "
    "denoising.</b> The genuinely hard part of the problem — "
    "identifying structure — was handed to us by the renderer."]),
  ("table", ["Buffer", "What it provides", "Cost"],
   [["<b>Albedo</b>", "The surface colour at the first hit, so texture "
     "detail is not mistaken for noise and smoothed away.",
     "Free — it is the material evaluated at the primary hit."],
    ["<b>Normal</b>", "Geometric edges, creases, and curvature.", "Free."],
    ["<b>Depth</b>", "Depth discontinuities; also enables reprojection.",
     "Free."],
    ["<b>Object ID</b>", "Hard boundaries between distinct objects that may "
     "happen to have similar normals and depths.", "Free."],
    ["<b>Motion vectors</b>", "Where each pixel's surface was in the "
     "previous frame, enabling temporal accumulation.",
     "Free in an animation; requires the previous frame's transforms."],
    ["<b>Variance</b>", "How much to trust each pixel.",
     "Estimated from the samples (&sect;1)."]],
   [0.14, 0.52, 0.34]),
  ("callout", "Demodulate by albedo before filtering",
   ["Filtering the final colour blurs texture along with noise: a noisy "
    "brick wall comes back as a smooth brown wall.",
    "<b>Instead, divide by the albedo buffer before filtering and multiply "
    "it back afterwards.</b> The filter then operates on the "
    "<i>illumination</i> alone, which is smooth and low-frequency, while the "
    "texture — which was never noisy — is reapplied intact.",
    "<b>This single step is the largest quality improvement available for a "
    "modest amount of code</b>, and it is frequently omitted in first "
    "implementations.",
    "Handle the edge cases: guard against division by a near-zero albedo, "
    "and keep emissive surfaces out of the demodulation, since their "
    "radiance is not a product of albedo and illumination."]),
  ("code", """vec3 atrous(const Buffers& b, ivec2 p, int step) {
    vec3 sum(0); float wsum = 0;
    for (int dy = -2; dy <= 2; dy++)
    for (int dx = -2; dx <= 2; dx++) {
        ivec2 q = p + ivec2(dx, dy) * step;          // the "hole"
        if (!inside(q)) continue;
        float wn = powf(fmaxf(0.f, dot(b.normal[p], b.normal[q])), SIGMA_N);
        float wz = expf(-fabs(b.depth[p] - b.depth[q]) / (SIGMA_Z + 1e-6f));
        float wl = expf(-fabs(lum(b.color[p]) - lum(b.color[q]))
                        / (SIGMA_L * sqrtf(b.variance[p]) + 1e-6f));
        float w  = kernel[dy+2][dx+2] * wn * wz * wl;
        sum += b.color[q] * w; wsum += w;
    }
    return wsum > 0 ? sum / wsum : b.color[p];
}"""),
  ("p", "The <b>&agrave;-trous</b> construction runs several passes with an "
        "increasing gap between the sampled taps, achieving the effect of a "
        "very wide filter at linear rather than quadratic cost. Each of the "
        "three edge-stopping weights suppresses blurring across a different "
        "kind of discontinuity."),
  ("callout", "The variance-scaled luminance weight is the clever part",
   ["The luminance term <code>wl</code> suppresses blurring between pixels "
    "whose brightness differs substantially — which protects genuine "
    "edges in the illumination, such as a shadow boundary.",
    "<b>But in a noisy image, neighbouring pixels differ substantially "
    "because of noise, not because of an edge.</b> A naive luminance weight "
    "therefore refuses to blur exactly where blurring is most needed, and "
    "preserves the noise as though it were detail.",
    "<b>Scaling the tolerance by the estimated standard deviation fixes "
    "this.</b> Where variance is high, large differences are interpreted as "
    "noise and blurred through; where variance is low, the same difference "
    "is interpreted as a real edge and preserved.",
    "This is the central idea of SVGF (spatiotemporal variance-guided "
    "filtering), and it is what makes the filter work at low sample counts "
    "rather than merely at moderate ones."]),

  ("break",),
  ("h1", "3 &nbsp; Learned denoisers"),
  ("table", ["", "Hand-designed (&agrave;-trous, SVGF)", "Learned (OIDN, "
             "OptiX)"],
   [["How it works", "Explicit edge-stopping weights, designed and tuned by "
     "hand.",
     "A convolutional network trained on pairs of noisy and converged "
     "renders."],
    ["Quality at 4–16 spp", "Adequate; visible over-blurring.",
     "<b>Substantially better.</b> This is where the gap is largest."],
    ["Failure mode", "<b>Predictable:</b> over-blurring, ghosting on "
     "motion, loss of fine shadows.",
     "<b>Unpredictable:</b> may smooth away real detail, or "
     "<b>hallucinate detail that was never in the scene</b> because it "
     "resembles the training data."],
    ["Tunability", "<b>Parameters you can reason about and adjust.</b>",
     "Retrain, or accept the result."],
    ["Cost", "Fast; viable in real time.",
     "Heavier; needs a GPU. Fine for offline, and increasingly viable "
     "interactively."],
    ["Status", "Used in real time and as a component of larger systems.",
     "<b>The production default for offline rendering.</b>"]],
   [0.15, 0.40, 0.45]),
  ("callout", "Denoising is biased, and using it is still correct",
   ["A denoiser modifies each pixel using information from its neighbours. "
    "<b>The output is not an unbiased estimate of the rendering "
    "equation</b>, and no amount of care makes it one.",
    "It can remove genuine high-frequency content — fine texture "
    "detail, small sharp highlights, thin contact shadows — and a "
    "learned denoiser can introduce detail that has no counterpart in the "
    "scene, because the network has learned what such regions usually look "
    "like.",
    "<b>And using one is still the right engineering decision.</b> At a "
    "fixed compute budget, a denoised 64-sample image is usually closer to "
    "the converged truth, by any error metric, than a noisy image at the "
    "sample count the same budget would otherwise buy.",
    "<b>What is not acceptable is silence about it.</b> Report that an image "
    "is denoised, give the sample count, name the denoiser, and show the "
    "noisy input and a converged reference beside the result. Project 2 "
    "requires exactly this, and the requirement is not pedantry — a "
    "denoised image presented as a render is a claim about convergence that "
    "has not been earned."]),

  ("h1", "4 &nbsp; ReSTIR"),
  ("p", "Reservoir-based spatiotemporal importance resampling, from "
        "Bitterli et al. in 2020. It is the most consequential rendering "
        "result of the last decade, and the core idea is simple."),
  ("ol", ["<b>Reservoir sampling</b> maintains a single sample selected from "
          "an arbitrarily long stream, with the correct probability, in "
          "constant memory. The technique itself is decades old.",
          "<b>Resampled importance sampling</b> draws M candidate samples "
          "from a cheap distribution and resamples one of them according to "
          "a better target distribution — giving approximately the "
          "better distribution's quality for roughly the cheap one's cost.",
          "<b>Spatial reuse:</b> a neighbouring pixel usually shades a "
          "similar surface under similar lighting, so <i>its</i> chosen "
          "light sample is probably good here too. Combine the reservoirs.",
          "<b>Temporal reuse:</b> the same surface point last frame is "
          "probably still well served by the sample chosen then. Combine "
          "across frames using motion vectors."]),
  ("callout", "Why it mattered",
   ["<b>It attacks the constant in 1/&radic;N</b>, which Module 05 "
    "identified as the only available target — and it attacks it by "
    "orders of magnitude rather than by factors, because each pixel "
    "effectively benefits from work done by all its neighbours across many "
    "frames.",
    "<b>It changed what is possible rather than merely what is fast.</b> "
    "Direct illumination from millions of light sources, which Module 09 "
    "described as the many-lights problem, went from intractable to real "
    "time at one sample per pixel.",
    "<b>The costs are genuine.</b> Reused samples are correlated, so the "
    "residual error is structured rather than random — which, per "
    "&sect;3, is exactly the kind of error denoisers handle worst. And the "
    "bias correction, which requires MIS weights across reservoirs, is "
    "subtle; early implementations were biased in ways that took time to "
    "diagnose.",
    "<b>It generalises.</b> ReSTIR GI extends the idea to indirect "
    "illumination and ReSTIR PT to full path reuse, which is an active area "
    "and the most likely place for the next significant result."]),
  ("callout", "Denoising changed what the field optimises for",
   ["Before practical denoising, variance reduction was the only lever "
    "available, and the sophisticated algorithms of Module 11 competed "
    "directly on it.",
    "<b>The question now is different: what kind of noise does the denoiser "
    "handle well?</b> That is a different objective, and it favours "
    "different methods.",
    "<b>High-frequency, spatially uncorrelated noise denoises "
    "beautifully. Fireflies, correlated splotches, and structured error do "
    "not.</b> So an algorithm with somewhat higher variance but "
    "better-behaved noise can now beat one with lower variance outright.",
    "<b>This is why blue-noise sampling (Module 06) matters</b> despite not "
    "improving RMSE, and it is why Metropolis's splotchy error is a serious "
    "liability rather than a cosmetic complaint. The metric changed, and so "
    "did the ranking."]),
 ],
 "resources": [
   ("Schied et al. &mdash; Spatiotemporal Variance-Guided Filtering (SVGF, "
    "free)",
    "https://research.nvidia.com/publication/2017-07_spatiotemporal-"
    "variance-guided-filtering-real-time-reconstruction-path-traced",
    "The filter of &sect;2, including the variance estimation and temporal "
    "accumulation. The paper to implement from."),
   ("Intel Open Image Denoise",
    "https://www.openimagedenoise.org/",
    "A free, production-quality learned denoiser with a simple API. Use it "
    "as the comparison point for your own filter."),
   ("Bitterli et al. &mdash; Spatiotemporal Reservoir Resampling (ReSTIR, "
    "free)",
    "https://research.nvidia.com/publication/2020-07_spatiotemporal-"
    "reservoir-resampling-real-time-ray-tracing-dynamic-direct",
    "The &sect;4 paper. Read the supplemental material for the bias "
    "discussion."),
   ("Wyman & Panteleev &rsaquo; A Gentle Introduction to ReSTIR (SIGGRAPH "
    "course, free)",
    "https://intro-to-restir.cwyman.org/",
    "Far more approachable than the paper. Start here."),
   ("Zwicker et al. &mdash; Recent Advances in Adaptive Sampling and "
    "Reconstruction (survey, free)",
    "https://www.cs.umd.edu/~zwicker/publications.html",
    "The survey covering &sect;1 and &sect;2, including the bias analysis of "
    "adaptive sampling."),
 ],
 "exercises": [
   "Implement per-pixel variance estimation and output it as an image. The "
   "variance map is informative on its own — it shows exactly which "
   "transport is expensive.",
   "Implement adaptive sampling driven by that estimate. Report equal-time "
   "RMSE against uniform sampling.",
   "Demonstrate adaptive sampling bias: use no initial fixed budget and an "
   "uncapped allocation ratio, and compare the converged result against a "
   "uniform render.",
   "Output albedo, normal, depth, and object ID buffers. Confirm they are "
   "noise-free.",
   "Implement the &agrave;-trous filter. Then disable each edge-stopping "
   "weight in turn and document what breaks in each case.",
   "Implement albedo demodulation. Compare a filtered brick wall with and "
   "without it — this comparison belongs in your portfolio.",
   "Replace the fixed luminance tolerance with the variance-scaled version "
   "and report the difference at 4 and 64 samples per pixel.",
   "Run Intel Open Image Denoise on the same inputs and compare against your "
   "filter at 4, 16, and 64 samples per pixel. Report RMSE and look at the "
   "images — the ranking may differ.",
   "Find a case where the learned denoiser removes real detail or invents "
   "it. Document it honestly; such cases are not hard to construct.",
   "Implement reservoir sampling for light selection with spatial reuse "
   "only. Report the variance reduction on a scene with 1,000 lights.",
 ],
 "selfcheck": [
   "Why does adaptive sampling help, and what gain is typical?",
   "How does adaptive sampling introduce bias, and what are the standard "
   "defences?",
   "Why is denoising a render easier than denoising a photograph?",
   "Name five noise-free buffers and say what each contributes.",
   "What is albedo demodulation, why does it matter, and what edge cases "
   "need handling?",
   "What does the &agrave;-trous construction achieve, and what do the three "
   "edge-stopping weights do?",
   "Why must the luminance weight be scaled by variance?",
   "Compare hand-designed and learned denoisers on quality, failure mode, "
   "and tunability.",
   "In what sense is denoising biased, and what must you report?",
   "What is ReSTIR's core idea, what did it change, and what are its costs?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Spectral Rendering, Cameras, and Getting the Image Right",
 "subtitle": "From radiance to pixels, and whether to believe them.",
 "question": "How do you turn computed radiance into a correct image?",
 "outcomes": [
     "Explain when RGB rendering is wrong and what spectral rendering "
     "fixes.",
     "Implement hero wavelength sampling.",
     "Implement a thin-lens camera and explain the parameters "
     "photographically.",
     "Explain tone mapping and colour management end to end.",
     "Validate a renderer against something whose answer is known.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Spectral rendering",
   "blurb": "Three numbers are not a spectrum."},

  {"t": "callout", "title": "Where RGB rendering is actually wrong",
   "kind": "Four cases",
   "body": ["<b>Dispersion.</b> Refractive index varies with wavelength. "
            "With three channels you get three sharp bands, not a "
            "spectrum.",
            "<b>Fluorescence.</b> Light absorbed at one wavelength is "
            "emitted at another. Unrepresentable in RGB.",
            "<b>Multiplication of spectra.</b> Multiplying RGB triples is "
            "not the same as multiplying spectra and then converting — "
            "and the error compounds with each bounce.",
            "<b>Thin films and structural colour.</b> Interference depends "
            "on wavelength directly.",
            "<b>Everything else is fine in RGB</b>, which is why most "
            "renderers still default to it."]},

  {"t": "eq", "kicker": "Why", "title": "Why multiplying triples is not multiplying spectra",
   "eqs": [
     ("∫ S₁(λ) S₂(λ) x̄(λ) dλ   ≠   (∫S₁x̄) · (∫S₂x̄)",
      "Projecting to RGB and then multiplying is not the same as "
      "multiplying and then projecting."),
     ("Error compounds per bounce",
      "A room with saturated coloured walls diverges visibly from the "
      "spectral answer after two or three bounces."),
   ],
   "caption": "The approximation is exact only when one of the spectra is "
              "flat. Saturated colours are exactly where it fails.",
   "note": "This is the case people do not expect — no glass required, "
           "just strongly coloured interreflection."},

  {"t": "callout", "title": "Hero wavelength sampling",
   "kind": "How spectral rendering is made affordable",
   "body": ["Naively, each path carries one wavelength — correct, and "
            "four times the paths for the same colour noise.",
            "<b>Hero wavelength sampling carries four</b>: one sampled "
            "'hero' wavelength plus three rotated through the visible range, "
            "all following the <i>same</i> path.",
            "<b>They are combined with MIS</b> — the same machinery as "
            "Module 08, applied across wavelengths.",
            "<b>Nearly eliminates colour noise at almost no extra cost</b>, "
            "because the expensive part is the path, not the four "
            "evaluations. Standard practice since 2014."]},

  {"t": "section", "label": "Part 2", "title": "Cameras",
   "blurb": "The other end of the light path."},

  {"t": "eq", "kicker": "Thin lens", "title": "Depth of field, properly",
   "eqs": [
     ("Sample a point on the aperture; aim through the focal plane point",
      "Two extra random numbers per camera ray. That is the entire "
      "implementation."),
     ("CoC  =  A · |s − f| / s",
      "Circle of confusion grows with aperture A and with distance from the "
      "focal plane."),
     ("N  =  f / A",
      "The f-number. f/1.4 is a wide aperture and shallow depth of field; "
      "f/16 is narrow and deep."),
   ],
   "caption": "Expose the parameters as focal length, f-number, and focus "
              "distance. Photographers already know what those mean.",
   "note": "Using real photographic units is worth insisting on — it makes "
           "the camera usable by someone who has used a camera."},

  {"t": "bullets", "kicker": "Camera", "title": "What a usable camera model has",
   "items": [
     "<b>Thin lens</b> for depth of field. Two random numbers.",
     "<b>Aperture shape</b> — a polygon, not a disk. Bokeh takes the "
     "shape of the blades.",
     "<b>Shutter interval</b> for motion blur: sample a time per ray.",
     "<b>Rolling shutter</b>, if you want the characteristic skew of a CMOS "
     "sensor.",
     "<b>A reconstruction filter</b> over the pixel — box, tent, "
     "Mitchell, or Gaussian.",
     "",
     "<b>Use a filter that is not a box.</b> Mitchell is the usual default; "
     "a box filter visibly aliases.",
   ],
   "note": "Bokeh shape is cheap and is what makes rendered depth of field "
           "look photographic rather than blurred."},

  {"t": "section", "label": "Part 3", "title": "From radiance to pixels",
   "blurb": "The step most often done wrong."},

  {"t": "table", "kicker": "Pipeline", "title": "The order of operations",
   "header": ["Step", "Does", "Get it wrong and"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Spectral → XYZ", "Integrate against the CIE observer", "Hues are wrong"],
     ["XYZ → working RGB", "A matrix", "Saturated colours shift"],
     ["<b>Tone map</b>", "HDR → displayable range", "<b>Highlights clip or go grey</b>"],
     ["Gamut map", "Handle out-of-gamut colours", "Bright saturated areas clip oddly"],
     ["<b>Encode</b>", "Apply the display transfer function", "<b>The image looks washed out</b>"],
   ],
   "footnote": "Do all rendering in linear space. Apply the transfer "
               "function last, once.",
   "note": "The last row is the most common single error in a student "
           "renderer: forgetting the sRGB encode."},

  {"t": "callout", "title": "Tone mapping is not a gamma curve",
   "kind": "The distinction",
   "body": ["<b>The transfer function</b> (sRGB, or 'gamma') is a display "
            "encoding. It is <i>required</i>, it is invertible, and it loses "
            "nothing.",
            "<b>Tone mapping</b> compresses an unbounded dynamic range into "
            "the range a display can show. It is <i>lossy</i>, it is a "
            "creative choice, and there is no correct answer.",
            "<b>Doing only the first</b> gives blown highlights: the sun is "
            "10&#8309; and the display shows 1.",
            "<b>Doing only the second</b> gives a washed-out image, because "
            "linear values were sent to a display expecting encoded ones. "
            "<b>This is the single most common error in a student "
            "renderer.</b>"]},

  {"t": "table", "kicker": "Operators", "title": "Tone mapping operators",
   "header": ["Operator", "Character"],
   "widths": [4.0, 8.1],
   "rows": [
     ["Reinhard", "Simple, desaturates highlights, never clips"],
     ["Filmic (Hable)", "Film-like toe and shoulder; contrasty"],
     ["<b>ACES</b>", "<b>Industry standard; well-behaved highlights</b>"],
     ["AgX", "Recent; strong hue preservation into the highlights"],
   ],
   "footnote": "Pick one, use it consistently, and report which when "
               "comparing images. A tone map comparison is not a renderer "
               "comparison.",
   "note": "Stress the last point: students compare their render to PBRT's "
           "with different tone maps and conclude their renderer is wrong."},

  {"t": "section", "label": "Part 4", "title": "Validation",
   "blurb": "The course's closing argument."},

  {"t": "bullets", "kicker": "Validation", "title": "Everything this course can check",
   "items": [
     "<b>Analytic:</b> hemisphere = 2π; furnace test; constant "
     "environment; a disk light over a plane.",
     "<b>Statistical:</b> χ² on every sampler; convergence slope "
     "must be −0.5.",
     "<b>Comparative:</b> difference against PBRT; the difference image must "
     "be structureless noise.",
     "<b>Internal consistency:</b> different integrators must agree at "
     "convergence; MIS must not change the answer.",
     "<b>Physical:</b> a Cornell box against the measured radiometric data "
     "— the original was built and measured, not invented.",
     "",
     "<b>A renderer is one of the few programs with a ground truth. Use "
     "it.</b>",
   ],
   "note": "This is the slide to end on. The course's method, stated as a "
           "list."},

  {"t": "callout", "title": "Where this leaves you",
   "kind": "Closing",
   "body": ["You can state what a pixel is an integral of, and estimate that "
            "integral correctly.",
            "You can tell a <i>noise</i> problem from a <i>bias</i> problem "
            "from a <i>model</i> problem — which is most of the skill.",
            "<b>CSCE 649</b> gives the geometry motion to render; "
            "<b>CSCE 748</b> is the camera and the image side in depth; "
            "<b>CSCE 650</b> adds the constraint of a frame budget and a "
            "person inside it.",
            "<b>And you have a renderer whose every image you can "
            "defend.</b> That is a rarer thing than it sounds."]},
 ],
 "takeaways": [
   "RGB rendering is wrong for dispersion, fluorescence, thin films, and "
   "— unexpectedly — repeated multiplication of saturated "
   "spectra.",
   "Hero wavelength sampling carries four correlated wavelengths down one "
   "path and combines them with MIS, nearly eliminating colour noise.",
   "A thin-lens camera costs two random numbers. Expose focal length, "
   "f-number, and focus distance, because photographers know those.",
   "The transfer function is a required, lossless display encoding; tone "
   "mapping is a lossy creative compression. They are different operations.",
   "Render linear, tone map, then encode — once, last. Omitting the "
   "encode is the most common error in a student renderer.",
   "A renderer has a ground truth: analytic cases, statistical tests, "
   "reference comparison, and internal consistency. Few programs can be "
   "checked this thoroughly.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Spectral rendering"),
  ("p", "Light is a continuous function of wavelength. RGB rendering "
        "represents it with three numbers, and for most purposes that is "
        "adequate. These are the cases where it is not."),
  ("table", ["Case", "Why RGB fails", "Visibility"],
   [["<b>Dispersion</b>",
     "The refractive index varies with wavelength, so different wavelengths "
     "refract differently. With three channels you get three sharply "
     "separated bands.",
     "Obvious and wrong-looking in prisms, diamonds, and thick glass edges."],
    ["<b>Fluorescence</b>",
     "Energy absorbed at one wavelength is re-emitted at another. There is "
     "no RGB operation that moves energy between channels in this way.",
     "Optical brighteners, safety clothing, some minerals."],
    ["<b>Repeated multiplication</b>",
     "<b>Multiplying RGB triples is not equivalent to multiplying spectra "
     "and converting afterwards</b> — see below.",
     "<b>The case people do not expect.</b> No glass required."],
    ["<b>Thin films, structural colour</b>",
     "Interference depends on the wavelength directly.",
     "Soap bubbles, oil films, beetle shells, CD surfaces."]],
   [0.17, 0.48, 0.35]),
  ("callout", "Why repeated multiplication is the surprising case",
   ["Converting a spectrum to RGB is a projection onto three basis "
    "functions. <b>Projection does not commute with multiplication.</b>",
    "Concretely: light with spectrum S&#8321; reflecting off a surface with "
    "reflectance S&#8322; gives a result whose RGB is &int;S&#8321;S&#8322;"
    "x&#772;(&lambda;)d&lambda;, which is <i>not</i> the product of the "
    "individual RGB projections. The approximation is exact only when one of "
    "the spectra is flat.",
    "<b>And the error compounds with every bounce.</b> In a room with "
    "saturated coloured walls, the RGB answer diverges visibly from the "
    "spectral one after two or three interreflections — the colour "
    "bleeding is noticeably more saturated than it should be.",
    "<b>This is the case that surprises people</b>, because it requires no "
    "glass, no exotic material, and no obviously spectral phenomenon. Just "
    "strongly coloured surfaces lit indirectly, which is an ordinary "
    "interior."]),
  ("callout", "Hero wavelength sampling",
   ["The naive approach assigns each path a single randomly chosen "
    "wavelength. This is correct, and it costs roughly four times as many "
    "paths to reach the same colour noise, because each path now carries "
    "information about only a slice of the spectrum.",
    "<b>Hero wavelength sampling (Wilkie et al., 2014) carries four "
    "wavelengths down the same path:</b> one sampled 'hero' wavelength plus "
    "three more, rotated evenly through the visible range. The path geometry "
    "is shared; only the spectral quantities are evaluated four times.",
    "<b>The four are combined using multiple importance sampling</b> "
    "— Module 08's machinery applied across wavelengths rather than "
    "across light-sampling strategies. Where the path was chosen based on "
    "the hero wavelength (at a dispersive interface, say), the hero gets the "
    "weight; elsewhere all four contribute equally.",
    "<b>The result nearly eliminates colour noise at almost no additional "
    "cost</b>, because the expensive part of a sample is tracing the path, "
    "not evaluating four spectral values along it. It has been standard "
    "practice in spectral renderers since it was published."]),

  ("h1", "2 &nbsp; Cameras"),
  ("p", "A pinhole camera is a useful default and is not what photographs "
        "come from. The <b>thin lens</b> model adds depth of field for the "
        "cost of two extra random numbers per ray: sample a point on the "
        "aperture disk, and aim the ray through the point where the pinhole "
        "ray would have crossed the focal plane."),
  ("eq", "CoC = A &middot; |s &minus; f| / s &nbsp;&nbsp;&nbsp;&nbsp; "
         "N = f / A"),
  ("table", ["Parameter", "Meaning", "Why expose it this way"],
   [["Focal length f", "Field of view.",
     "A photographer knows what 35&nbsp;mm and 135&nbsp;mm look like. "
     "'Field of view in degrees' is less useful to the person operating "
     "it."],
    ["f-number N", "Aperture size, as f/N.",
     "f/1.4 is wide with shallow depth of field; f/16 is narrow and deep. "
     "Again, already understood."],
    ["Focus distance", "Where the focal plane sits.",
     "Usually better specified by picking a point in the scene than by "
     "typing a number."]],
   [0.17, 0.26, 0.57]),
  ("ul", ["<b>Aperture shape.</b> Real apertures are polygons formed by the "
          "diaphragm blades, and out-of-focus highlights take that shape. "
          "Sampling a hexagon instead of a disk is a few lines and is most "
          "of what makes rendered bokeh look photographic.",
          "<b>Shutter interval.</b> Sample a time per ray within the "
          "exposure window; the scene is evaluated at that time. Motion blur "
          "then costs nothing beyond the transforms.",
          "<b>Rolling shutter.</b> Make the sampled time depend on the "
          "pixel's row, and you get the characteristic skew of a CMOS "
          "sensor on fast motion.",
          "<b>Reconstruction filter.</b> The pixel integral of Module 01 is "
          "weighted by a filter. <b>Use something other than a box</b> "
          "— Mitchell is the usual default, Gaussian is softer. A box "
          "filter visibly aliases, and switching costs nothing."]),

  ("break",),
  ("h1", "3 &nbsp; From radiance to pixels"),
  ("table", ["Step", "Operation", "Symptom if wrong"],
   [["<b>Spectral &rarr; XYZ</b>",
     "Integrate the spectrum against the CIE standard observer functions.",
     "Hues are systematically wrong, particularly for saturated colours."],
    ["<b>XYZ &rarr; working RGB</b>",
     "A 3&times;3 matrix for the chosen primaries (sRGB, ACEScg, Rec.2020).",
     "Saturated colours shift; the image does not match other tools."],
    ["<b>Tone map</b>",
     "Compress unbounded HDR values into displayable range.",
     "<b>Highlights clip to white or wash out to grey.</b>"],
    ["<b>Gamut map</b>",
     "Handle colours outside the display's gamut.",
     "Bright saturated regions clip in one channel and shift hue."],
    ["<b>Encode</b>",
     "Apply the display transfer function (sRGB, or a gamma curve).",
     "<b>The image looks washed out and too bright in the midtones.</b>"]],
   [0.17, 0.44, 0.39]),
  ("callout", "The transfer function and tone mapping are different things",
   ["<b>The transfer function</b> — sRGB encoding, loosely called "
    "'gamma' — exists because displays and human perception are not "
    "linear in intensity. It is <b>required</b>, it is <b>invertible</b>, "
    "and it discards no information. Not applying it is simply a bug.",
    "<b>Tone mapping</b> compresses an unbounded dynamic range into what a "
    "display can show. It is <b>lossy</b>, it is a <b>creative choice</b>, "
    "and there is no uniquely correct operator.",
    "<b>Doing only the transfer function</b> gives blown highlights: the "
    "rendered sun has a value of 10<super>5</super> and the display can show "
    "1, so everything bright becomes a flat white region.",
    "<b>Doing only the tone map</b> gives a washed-out, low-contrast image, "
    "because linear values were handed to a display expecting encoded ones. "
    "<b>This is the single most common error in a first renderer</b>, and "
    "it is worth recognising on sight: midtones too bright, the whole image "
    "looking slightly foggy."]),
  ("table", ["Operator", "Character", "Use"],
   [["<b>Reinhard</b>", "Simple, never clips, desaturates highlights "
     "noticeably.", "A reasonable default for debugging."],
    ["<b>Filmic (Hable)</b>", "Film-like toe and shoulder; higher contrast.",
     "Games, where a punchy look is wanted."],
    ["<b>ACES</b>", "Industry standard; well-behaved highlight roll-off and "
     "a defined colour pipeline around it.",
     "<b>Film and most production work.</b>"],
    ["<b>AgX</b>", "Recent; strong hue preservation as values approach "
     "white, so bright saturated lights do not shift.",
     "Increasingly a default — Blender adopted it."]],
   [0.14, 0.46, 0.40]),
  ("p", "<b>Pick one, use it consistently, and state which one when "
        "comparing images.</b> A great deal of confusion in this course "
        "comes from comparing your render against a reference that used a "
        "different tone map and concluding the renderer is wrong. <b>Compare "
        "linear HDR values, not tone-mapped pixels</b>, when you are "
        "measuring correctness — tone mapping is a display decision "
        "applied after the rendering is finished."),

  ("h1", "4 &nbsp; Validation, and what this course was about"),
  ("table", ["Kind", "Test", "What it proves"],
   [["<b>Analytic</b>",
     "Hemisphere integrates to 2&pi;. White furnace test. Constant "
     "environment on a diffuse sphere. A disk light over a diffuse plane.",
     "The result is exactly right in cases where the right answer is known "
     "in closed form."],
    ["<b>Statistical</b>",
     "&chi;&#178; tests on every sampler. Convergence plots with slope "
     "&minus;0.5.",
     "The samplers draw from the densities they claim, and the estimator is "
     "converging as theory says it must."],
    ["<b>Comparative</b>",
     "Difference against PBRT on the same scene. <b>The difference image "
     "must be structureless noise.</b>",
     "Agreement with an independent, heavily validated implementation."],
    ["<b>Internal consistency</b>",
     "Different integrators must agree at convergence. <b>Enabling MIS must "
     "not change the converged image</b>, only the variance.",
     "No single strategy is systematically wrong in a way the others share."],
    ["<b>Physical</b>",
     "The Cornell box against its published measured radiometric data.",
     "Agreement with reality — the original Cornell box was built and "
     "measured, not invented, which is precisely why it exists."]],
   [0.15, 0.45, 0.40]),
  ("callout", "A renderer has a ground truth, which is unusual",
   ["Most programs cannot be checked this thoroughly. There is no analytic "
    "answer for whether a compiler's optimisation was correct in general, or "
    "whether a user interface is right.",
    "<b>A path tracer converges to a defined quantity</b> — the value "
    "of the rendering equation for the scene as described — and that "
    "value can be computed independently, bounded analytically in special "
    "cases, and compared against measurements of physical scenes.",
    "<b>This course has leaned on that throughout</b>, and the habit is the "
    "most transferable thing in it: when a quantity has a ground truth, "
    "build the comparison before building the thing. Module 05 asked you to "
    "write the validation suite before the integrator, and everything since "
    "has used it.",
    "<b>The distinction that matters most</b> is the one from Module 02: a "
    "<i>noise</i> problem, a <i>bias</i> problem, and a <i>model</i> problem "
    "look similar in an image and are fixed completely differently. Being "
    "able to tell them apart quickly is most of the practical skill this "
    "course teaches."]),
  ("p", "Where this leaves you: able to state what a pixel is an integral "
        "of and to estimate that integral correctly; able to diagnose a "
        "rendering failure by its appearance; and in possession of a "
        "renderer whose every image you can defend. <b>CSCE 649</b> supplies "
        "the motion worth rendering, <b>CSCE 748</b> takes the camera and "
        "image side far further, and <b>CSCE 650</b> adds the constraint of "
        "a frame budget with a person inside it."),
 ],
 "resources": [
   ("PBRT 4th ed. &mdash; Chapters 4.5 and 5, Colour and Cameras",
    "https://pbr-book.org/4ed/Cameras_and_Film",
    "Spectral representation, the CIE observer, colour spaces, the thin lens "
    "model, and the film and filter machinery."),
   ("Wilkie et al. &mdash; Hero Wavelength Spectral Sampling (2014, free)",
    "https://cgg.mff.cuni.cz/publications/hero-wavelength-spectral-sampling/",
    "The technique of &sect;1, with the MIS derivation."),
   ("Cornell Box data and measurements",
    "https://www.graphics.cornell.edu/online/box/data.html",
    "Geometry, measured spectral reflectances, and radiometric measurements. "
    "The physical validation of &sect;4."),
   ("Troy Sobotka &mdash; AgX and colour management writing",
    "https://github.com/sobotka/AgX",
    "The display transform of &sect;3, with a clear account of why hue "
    "preservation in highlights matters."),
   ("Poynton &mdash; Frequently Asked Questions about Gamma (free)",
    "https://poynton.ca/GammaFAQ.html",
    "The clearest explanation of the transfer function, and why calling it "
    "'gamma' causes so much confusion."),
 ],
 "exercises": [
   "Implement spectral rendering with a single wavelength per path. Render a "
   "prism and confirm you get a continuous spectrum rather than three bands.",
   "Implement hero wavelength sampling with four wavelengths. Compare colour "
   "noise against single-wavelength sampling at equal time.",
   "Construct the multiplication error of &sect;1: a room with saturated "
   "coloured walls, rendered in RGB and spectrally. Report the difference "
   "after two, four, and eight bounces.",
   "Implement a thin-lens camera. Render the same scene at f/1.4, f/4, and "
   "f/16 and confirm the depth of field behaves as a photographer would "
   "expect.",
   "Implement a polygonal aperture and render out-of-focus point highlights. "
   "Confirm the bokeh takes the blade shape.",
   "Implement box, tent, and Mitchell reconstruction filters. Compare on a "
   "high-contrast edge and report which aliases.",
   "Implement the full colour pipeline of &sect;3. Then remove the sRGB "
   "encode and document the result — recognising this on sight is "
   "worth the exercise.",
   "Implement Reinhard, ACES, and AgX tone mapping. Render a scene with a "
   "very bright saturated light and compare how each handles the highlight.",
   "Render the Cornell box and compare against the published measured "
   "radiometric data, not just against another renderer. Report the "
   "agreement.",
   "<b>Project 2 is now due.</b> Submit the renderer, the validation suite "
   "results, the convergence plots, and the portfolio of images with sample "
   "counts and render times stated.",
 ],
 "selfcheck": [
   "Name four cases where RGB rendering is wrong, and say which is the "
   "surprising one.",
   "Why is multiplying RGB triples not the same as multiplying spectra?",
   "What is hero wavelength sampling, and why is it nearly free?",
   "How does a thin-lens camera work, and what three parameters should be "
   "exposed?",
   "What determines bokeh shape, and why does it matter?",
   "List the five steps from spectral radiance to a displayed pixel.",
   "Distinguish the transfer function from tone mapping on three axes.",
   "What does an image look like when the sRGB encode is omitted?",
   "Why must correctness comparisons be made on linear values rather than "
   "tone-mapped ones?",
   "Give the five kinds of validation and what each one proves.",
 ],
},

]
