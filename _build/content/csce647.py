# -*- coding: utf-8 -*-
"""CSCE 647 Image Synthesis — original course content."""

COURSE = {
    "code": "CSCE 647",
    "title": "Image Synthesis",
    "tagline": "Light transport from first principles: the rendering "
               "equation, Monte Carlo, and a path tracer you write yourself",
    "term": "Semester 3 (with CSCE 649 and CSCE 608)",
    "prereqs": "CSCE 641 Computer Graphics; CSCE 629 helpful for the "
               "acceleration-structure analysis; probability to the level of "
               "expectation and variance, developed here as needed",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A physically based path tracer: BVH, microfacet BSDFs, "
                   "multiple importance sampling, participating media, and a "
                   "denoiser — written by you and validated against results "
                   "whose answers are known in advance",
    "description": [
        "CSCE 641 built a renderer that produces plausible images quickly. "
        "This course builds one that produces <i>correct</i> images, and "
        "defines what correct means. The difference is that every shortcut "
        "in the real-time pipeline — ambient terms, baked lighting, "
        "screen-space approximations — exists because the true answer "
        "was too expensive. Here we compute the true answer.",
        "The subject has an unusual shape. Almost all of it follows from one "
        "equation, published by Kajiya in 1986, that fits on a single line "
        "and has no closed-form solution. The rest of the course is the "
        "consequences: the integral is infinite-dimensional, so we estimate "
        "it statistically; the estimator is noisy, so we spend most of our "
        "effort on variance reduction; and the variance is concentrated in a "
        "few hard configurations, so most published research is about those "
        "configurations specifically.",
        "That structure makes this course unusually honest. A path tracer "
        "has a ground truth: run it long enough and it converges to the "
        "right answer, and any bug shows up as a measurable difference from "
        "a reference. Few areas of graphics let you check your work this "
        "directly, and the course leans on it constantly — <b>every "
        "component you write is validated against something whose answer is "
        "known analytically</b>.",
        "You will write the renderer. By the end it will handle glossy "
        "surfaces, environment lighting, smoke, and skin, and you will be "
        "able to explain, for any image it produces, why each pixel has the "
        "value it does.",
    ],
    "outcomes": [
        "State the rendering equation, explain every term, and derive the "
        "path-integral form.",
        "Implement robust ray-primitive intersection and a BVH that stands "
        "up to real scenes.",
        "Explain Monte Carlo integration, and analyse an estimator for bias "
        "and variance.",
        "Apply importance sampling, stratification, and low-discrepancy "
        "sequences, and measure what each one buys.",
        "Implement microfacet BSDFs with correct sampling, and verify energy "
        "conservation.",
        "Implement a path tracer with next-event estimation and multiple "
        "importance sampling.",
        "Render participating media with unbiased transmittance estimation.",
        "Compare bidirectional methods and say which light transport each "
        "one handles that path tracing does not.",
        "Diagnose rendering artefacts from their appearance and name the "
        "mechanism.",
    ],
    "materials": [
        ("Physically Based Rendering, 4th ed. — free online",
         "https://pbr-book.org/",
         "The primary text, and the most complete free resource in graphics. "
         "It is a literate program: the book is the renderer. Read the "
         "chapter before each module and read the code with it."),
        ("Ray Tracing in One Weekend series (free)",
         "https://raytracing.github.io/",
         "Three short books that get a working path tracer on screen fast. "
         "Do the first one before Module 03 — getting something rendering "
         "early makes the theory concrete."),
        ("TU Wien — Rendering / Light Transport (free video)",
         "https://www.youtube.com/playlist?list=PLujxSBD-JXgnGmsn7gEyN28P1DnRZG7qi",
         "Károly Zsolnai-Fehér's full graduate course. Excellent on the "
         "intuition behind Monte Carlo and on the comparative strengths of "
         "bidirectional methods."),
        ("Eric Veach — Robust Monte Carlo Methods for Light Transport "
         "(thesis, free)",
         "https://graphics.stanford.edu/papers/veach_thesis/",
         "Where multiple importance sampling, BDPT, and Metropolis light "
         "transport come from. Chapter 9 on MIS is the clearest exposition "
         "that exists and is worth reading in the original."),
        ("Scratchapixel — rendering lessons (free)",
         "https://www.scratchapixel.com/",
         "Slower and more elementary than PBRT, with the algebra written "
         "out. Useful when a PBRT derivation moves too fast."),
        ("Benedikt Bitterli — rendering resources and test scenes (free)",
         "https://benedikt-bitterli.me/resources/",
         "Scenes in PBRT format with reference renders. Your validation set "
         "from Module 08 onward."),
    ],
    "tooling": [
        "<b>C++17</b> and nothing else for the core. You need the "
        "performance, and this is a course where a 20× speed difference "
        "changes which experiments you can run.",
        "<b>No rendering library.</b> Intersection, sampling, and integration "
        "are the course. You may use a linear-algebra header and an image "
        "writer.",
        "<b>OpenEXR</b> for output. Rendering is high-dynamic-range work and "
        "writing 8-bit PNG from the start will hide errors that matter.",
        "<b>PBRT v4</b> installed as a <i>reference</i>, not a dependency. "
        "Render the same scene in both and difference the images — this is "
        "the single most effective debugging tool in the course.",
        "<b>A validation suite</b>: the white furnace test, a Cornell box "
        "with a known analytic solution for direct lighting, and a "
        "convergence plot script. Build it in Module 05 and never delete it.",
        "<b>A portfolio repository</b> with every image the course produces, "
        "its sample count, and its render time.",
    ],
    "projects": [
        {"title": "A correct path tracer", "after": 8,
         "brief": "The core renderer. Everything after Module 08 is an "
                  "extension of this, so it has to be right rather than "
                  "merely producing an image that looks acceptable.",
         "reqs": [
             "Ray–triangle and ray–sphere intersection, watertight, with "
             "the self-intersection problem solved by offsetting along the "
             "normal rather than by a magic epsilon.",
             "A BVH built with the surface area heuristic, with build time "
             "and traversal statistics reported.",
             "Lambertian and smooth-conductor BSDFs, plus a GGX microfacet "
             "BSDF with correct importance sampling.",
             "A unidirectional path tracer with Russian roulette "
             "termination.",
             "Next-event estimation combined with BSDF sampling through "
             "multiple importance sampling, using the power heuristic.",
             "Stratified and low-discrepancy sampling, selectable at "
             "runtime so they can be compared.",
         ],
         "done": [
             "<b>The white furnace test passes:</b> a white Lambertian sphere "
             "in a uniform unit-radiance environment renders to exactly 1.0 "
             "everywhere, to within noise. Report the measured mean and "
             "variance.",
             "A Cornell box rendered to convergence and differenced against "
             "the PBRT reference, with the RMSE reported and below a stated "
             "threshold.",
             "A convergence plot: RMSE against sample count on log-log axes, "
             "for uniform, BSDF-sampled, NEE, and MIS integrators on the same "
             "scene. <b>The MIS curve must sit below the others everywhere, "
             "and you must be able to explain each gap.</b>",
             "A scene with both a small bright light and a large dim one, "
             "showing the failure of each single strategy and the success of "
             "MIS — the figure from Veach's thesis, reproduced with your "
             "own renderer.",
         ]},
        {"title": "Volumes, spectra, and a usable renderer", "after": 12,
         "brief": "Extend the core into the cases that make rendering hard, "
                  "and make the result fast enough to iterate with.",
         "reqs": [
             "Homogeneous and heterogeneous participating media with "
             "unbiased transmittance by delta tracking.",
             "The Henyey–Greenstein phase function, importance sampled.",
             "An environment light importance sampled by luminance, with the "
             "2D CDF built at load time.",
             "Spectral rendering with hero wavelength sampling, demonstrated "
             "on a dispersive material.",
             "Adaptive sampling driven by a per-pixel variance estimate.",
             "A denoiser — at minimum an edge-aware à-trous filter guided "
             "by albedo and normal buffers.",
         ],
         "done": [
             "A heterogeneous medium rendered with delta tracking, shown to "
             "match a brute-force ratio-tracking reference to within noise.",
             "A dispersion render that produces the correct spectral "
             "ordering, beside the same scene in RGB showing the artefact "
             "RGB produces.",
             "A denoised image beside its noisy input and a converged "
             "reference, with RMSE for all three and an honest note on what "
             "the denoiser destroyed.",
             "An equal-time comparison: your renderer against PBRT on the "
             "same scene and hardware. <b>You will lose. Report by how "
             "much and say where the time goes.</b>",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "Radiometry: What Rendering Computes",
 "subtitle": "Five quantities, one of which is the one you actually want.",
 "question": "What is the number stored in a pixel?",
 "outcomes": [
     "Define flux, irradiance, intensity, and radiance, and say which one a "
     "pixel holds.",
     "Use solid angle and the projected-area cosine correctly.",
     "Explain why radiance is invariant along a ray in a vacuum, and why "
     "that makes ray tracing possible.",
     "State the BRDF as a ratio of differentials and give its three required "
     "properties.",
     "Explain what a pixel value is an integral of.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Five quantities",
   "blurb": "They differ by what you have divided by."},

  {"t": "table", "kicker": "Radiometry", "title": "The quantities, and their units",
   "header": ["Quantity", "Symbol", "Units", "Is"],
   "widths": [2.7, 1.5, 2.6, 5.3],
   "rows": [
     ["Radiant energy", "Q", "J", "Total energy"],
     ["Radiant flux (power)", "&#934;", "W", "Energy per second"],
     ["Irradiance", "E", "W/m&#178;", "<b>Power arriving per unit area</b>"],
     ["Radiant intensity", "I", "W/sr", "Power per unit solid angle"],
     ["<b>Radiance</b>", "<b>L</b>", "<b>W/(m&#178;&middot;sr)</b>",
      "<b>Power per area per solid angle</b>"],
   ],
   "footnote": "Each row divides the one above by something. Radiance is "
               "divided by both.",
   "note": "Do not let anyone memorise this table. The point is only that "
           "they differ by what has been divided out, and that radiance is "
           "the most divided."},

  {"t": "callout", "title": "Radiance is the quantity rendering transports",
   "kind": "The one that matters",
   "body": ["Everything else is obtained by integrating radiance, so a "
            "renderer that computes radiance computes everything.",
            "<b>It has a direction</b>, so it can describe a ray. Irradiance "
            "has already summed over directions and lost that "
            "information.",
            "<b>It is invariant along a ray in a vacuum</b> (Part 2), so it "
            "can be carried from a surface to a camera unchanged.",
            "<b>It is what a sensor responds to</b>, so a pixel value is an "
            "integral of radiance and nothing else.",
            "If you remember one thing from this module: <b>a ray carries "
            "radiance</b>."]},

  {"t": "eq", "kicker": "Solid angle", "title": "Measuring a set of directions",
   "eqs": [
     ("dω = dA cos θ / r²",
      "The solid angle a small patch subtends: its area, foreshortened by "
      "the viewing angle, divided by distance squared."),
     ("∫ over the hemisphere  dω  =  2π sr",
      "A hemisphere of directions has measure 2π steradians; the full sphere "
      "has 4π."),
     ("dω = sin θ dθ dφ",
      "In spherical coordinates. The sin θ is the part everyone forgets, and "
      "forgetting it biases every integral you write."),
   ],
   "caption": "Solid angle is to directions what area is to surfaces: the "
              "measure you integrate against.",
   "note": "The missing sin θ is the single most common bug in a first "
           "hemisphere integrator. Flag it hard here so it is recognised "
           "later."},

  {"t": "callout", "title": "The cosine is geometry, not physics",
   "kind": "Why cos θ keeps appearing",
   "body": ["A beam striking a surface at a grazing angle spreads its power "
            "over a larger area, so the power <i>per unit area</i> falls.",
            "<b>That is the whole content of Lambert's cosine law.</b> It is "
            "not a property of the material and not an approximation — it "
            "is the projected area of the beam.",
            "So the cosine appears whenever you convert between 'per unit "
            "area on the surface' and 'per unit area perpendicular to the "
            "beam'.",
            "<b>A Lambertian surface is not one that obeys the cosine law.</b> "
            "Everything obeys the cosine law. A Lambertian surface is one "
            "whose BRDF is constant."]},

  {"t": "section", "label": "Part 2", "title": "Invariance",
   "blurb": "The property that makes ray tracing possible at all."},

  {"t": "eq", "kicker": "Invariance", "title": "Radiance does not fall off with distance",
   "eqs": [
     ("L(x → y)  =  L(y → x)   in a vacuum, along the ray",
      "Radiance leaving one point toward another equals the radiance "
      "arriving at the second from the first. Nothing is lost."),
     ("E  ∝  1/r²   but   L  is constant",
      "Irradiance obeys the inverse square law. Radiance does not, because "
      "the solid angle shrinks by exactly the same factor."),
   ],
   "caption": "The 1/r² in the irradiance and the 1/r² in the solid angle "
              "cancel. This is the reason a wall does not look dimmer as you "
              "back away from it.",
   "note": "Ask: why doesn't a white wall get darker as you walk away? "
           "Nobody has thought about it, and the answer is exactly this."},

  {"t": "callout", "title": "Why this licenses the entire algorithm",
   "kind": "Consequence",
   "body": ["If radiance were attenuated along a ray, a renderer would have "
            "to integrate along every path through space.",
            "<b>Because it is invariant, a ray is a lookup.</b> Trace until "
            "you hit something, evaluate the radiance leaving that point "
            "toward you, and that value <i>is</i> the radiance arriving at "
            "the camera.",
            "Ray tracing is therefore not an approximation of light "
            "transport. It is an exact consequence of radiance invariance "
            "in a vacuum.",
            "<b>'In a vacuum' is doing real work here.</b> Module 10 removes "
            "it, and the lookup becomes an integral again."]},

  {"t": "section", "label": "Part 3", "title": "Reflection",
   "blurb": "The function that relates arriving light to leaving light."},

  {"t": "eq", "kicker": "BRDF", "title": "The bidirectional reflectance distribution function",
   "eqs": [
     ("f(p, ωi, ωo)  =  dLo(p, ωo) / dE(p, ωi)",
      "The differential radiance leaving in direction ωo, per unit "
      "differential irradiance arriving from ωi."),
     ("f(p, ωi, ωo)  =  dLo(p, ωo) / ( Li(p, ωi) cos θi dωi )",
      "The same thing with the irradiance expanded. Units are 1/sr."),
   ],
   "caption": "It is a ratio of differentials, which is why it is a "
              "<i>distribution</i> and why it is not bounded by 1.",
   "note": "The 'not bounded by 1' point surprises people: a mirror's BRDF "
           "is a delta distribution and is unbounded. Energy conservation "
           "constrains the integral, not the value."},

  {"t": "table", "kicker": "Constraints", "title": "What a physical BRDF must satisfy",
   "header": ["Property", "Statement", "Why it matters"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Non-negativity", "f &ge; 0 everywhere", "Negative light is not a thing"],
     ["<b>Reciprocity</b>", "f(ωi, ωo) = f(ωo, ωi)",
      "<b>Required by bidirectional methods</b> (Module 11)"],
     ["<b>Energy conservation</b>", "&#8747; f cos &theta; d&omega; &le; 1 for all &omega;o",
      "<b>Or paths gain energy and never terminate</b>"],
   ],
   "footnote": "A BRDF violating conservation can make a path tracer diverge "
               "rather than merely look wrong.",
   "note": "Energy conservation is the one that produces catastrophic rather "
           "than cosmetic failure. Stress it."},

  {"t": "callout", "title": "Reciprocity is not a formality",
   "kind": "Where it bites",
   "body": ["Reciprocity says the BRDF is unchanged if you swap the incoming "
            "and outgoing directions — light does not care which way it "
            "is travelling.",
            "<b>Every bidirectional method depends on it.</b> Light tracing, "
            "BDPT, and photon mapping all build paths from the light and use "
            "them as though they had been built from the camera.",
            "A non-reciprocal BRDF — and several popular shading models "
            "are not reciprocal — silently gives different answers "
            "depending on the direction a path was constructed.",
            "<b>This is why a model that works in your rasteriser may be "
            "unusable here.</b> Many real-time BRDFs were never required to "
            "be reciprocal."]},

  {"t": "section", "label": "Part 4", "title": "What a pixel is",
   "blurb": "An integral, over more dimensions than people expect."},

  {"t": "eq", "kicker": "The sensor", "title": "A pixel value",
   "eqs": [
     ("I  =  ∫ ∫ ∫ ∫  w(x,y) L(x,y,ω,t,λ) S(λ)  dλ dt dω dx dy",
      "Integrated over the pixel's footprint, the lens aperture, the shutter "
      "interval, and the spectral response of the sensor."),
   ],
   "caption": "Antialiasing, depth of field, motion blur, and colour are not "
              "four separate features. They are four of the dimensions of "
              "one integral, and Monte Carlo handles them identically.",
   "note": "This slide reframes a lot of CSCE 641 material. Spend time on "
           "it: it is the unifying observation of the whole course."},

  {"t": "two", "kicker": "Two systems", "title": "Radiometric and photometric",
   "lh": "Radiometric — physics",
   "l": ["Measures energy, in watts.",
         "Wavelength-independent weighting.",
         "<b>What a renderer computes.</b>",
         ("Radiance: W/(m²·sr)", 1),
         "Comparable across the spectrum, including light you cannot see."],
   "rh": "Photometric — perception",
   "r": ["Measures <i>perceived</i> brightness, in lumens.",
         "Weighted by human spectral sensitivity.",
         "<b>What lighting specifications use.</b>",
         ("Luminance: cd/m² = lm/(m²·sr)", 1),
         "Necessary when matching real fixtures, whose output is quoted in "
         "lumens."],
   "note": "Students mostly need to know the two systems exist and that "
           "converting requires the luminosity function. Do not belabour."},

  {"t": "bullets", "kicker": "Confusions", "title": "Four mistakes this module exists to prevent",
   "items": [
     "<b>Forgetting sin θ</b> in a spherical-coordinate integral. Your "
     "hemisphere integrates to the wrong constant and everything is "
     "uniformly wrong.",
     "",
     "<b>Treating the cosine as a material property.</b> It is projected "
     "area, and it applies to every surface.",
     "",
     "<b>Expecting radiance to fall off with distance.</b> It does not; "
     "irradiance does.",
     "",
     "<b>Assuming a BRDF is at most 1.</b> It is a density. A mirror's is "
     "unbounded.",
   ],
   "footnote": "Three of the four produce images that look plausible and are "
               "wrong, which is the dangerous kind of bug."},
 ],
 "takeaways": [
   "Flux, irradiance, intensity, and radiance differ by what has been "
   "divided out. Radiance is divided by both area and solid angle.",
   "A ray carries radiance. Everything else in rendering is an integral of "
   "it.",
   "Radiance is invariant along a ray in a vacuum, because the inverse "
   "square law and the shrinking solid angle cancel exactly.",
   "That invariance is why ray tracing is exact rather than approximate — "
   "and why participating media break it.",
   "The cosine is projected area, not a material property. The BRDF is a "
   "ratio of differentials, so it is unbounded.",
   "A pixel is one integral over area, lens, time, direction, and "
   "wavelength. Antialiasing, depth of field, and motion blur are the same "
   "problem.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why a whole module on units"),
  ("p", "A renderer that confuses irradiance with radiance produces images "
        "that are wrong by a factor involving &pi; and a cosine, and such "
        "images look entirely plausible. The error does not announce itself "
        "— it shows up as 'my renderer is darker than the reference and I "
        "do not know why', which is the most common complaint in this "
        "subject."),
  ("p", "There are five quantities. They are the same physical thing divided "
        "by different amounts."),
  ("table", ["Quantity", "Symbol", "SI units", "Definition"],
   [["Radiant energy", "Q", "joule (J)", "Total energy. Rarely used "
     "directly in rendering."],
    ["Radiant flux, or power", "&Phi;", "watt (W)",
     "d<i>Q</i>/d<i>t</i>. Energy per unit time. A light bulb's output."],
    ["Irradiance", "E", "W/m&#178;",
     "d&Phi;/d<i>A</i>. Power arriving per unit surface area, summed over "
     "all incoming directions."],
    ["Radiant intensity", "I", "W/sr",
     "d&Phi;/d&omega;. Power per unit solid angle. Natural for point "
     "lights, which have no area."],
    ["<b>Radiance</b>", "<b>L</b>", "<b>W/(m&#178;&middot;sr)</b>",
     "<b>d&#178;&Phi; / (d&omega; d<i>A</i> cos&theta;)</b>. Power per unit "
     "projected area per unit solid angle. The quantity rendering "
     "transports."]],
   [0.19, 0.09, 0.15, 0.57]),
  ("callout", "Radiance is the quantity you want, for four reasons",
   ["<b>It is complete.</b> Every other radiometric quantity is an integral "
    "of radiance, so a renderer that computes radiance has computed "
    "everything else implicitly.",
    "<b>It is directional.</b> Radiance is defined per solid angle, so it "
    "can describe what a single ray carries. Irradiance has already summed "
    "over all incoming directions and destroyed that information.",
    "<b>It is invariant along a ray in a vacuum</b>, developed in &sect;3. "
    "This is what makes a ray a lookup rather than an integral.",
    "<b>It is what a sensor responds to.</b> A pixel value is an integral of "
    "radiance over the sensor's footprint, aperture, exposure, and spectral "
    "response, and nothing else enters."]),

  ("h1", "2 &nbsp; Solid angle"),
  ("p", "Integrating over directions requires a measure on the set of "
        "directions, and that measure is solid angle. The construction is "
        "exactly parallel to area: just as an angle in the plane is arc "
        "length on the unit circle, a solid angle is area on the unit "
        "sphere."),
  ("eq", "d&omega; = dA cos&theta; / r&#178;"),
  ("p", "A patch of area d<i>A</i> at distance <i>r</i>, tilted so its "
        "normal makes angle &theta; with the direction to the viewer, "
        "subtends this solid angle. Both factors are doing necessary work: "
        "the cos&theta; foreshortens the patch to the area actually "
        "presented, and the 1/<i>r</i>&#178; accounts for its apparent size "
        "shrinking with distance."),
  ("p", "The full sphere has measure 4&pi; steradians and a hemisphere "
        "2&pi;. In spherical coordinates, with &theta; measured from the "
        "surface normal:"),
  ("eq", "d&omega; = sin&theta; d&theta; d&phi;"),
  ("callout", "The sin&theta; is the most commonly dropped term in rendering",
   ["A naive hemisphere integrator that loops over &theta; and &phi; "
    "uniformly and forgets the sin&theta; is integrating against the wrong "
    "measure. It over-weights directions near the pole and under-weights "
    "those near the horizon.",
    "The symptom is subtle: images look nearly right but are consistently "
    "off by a factor, and the error changes with surface orientation, so it "
    "cannot be corrected by scaling the output.",
    "<b>The check:</b> integrate the constant function 1 over your "
    "hemisphere. You must get 2&pi;. If you get something else, nothing "
    "downstream of that integrator can be trusted.",
    "Write that check as a unit test in Module 05 and keep it forever. It "
    "costs three lines and catches an entire class of error."]),
  ("h2", "2.1 &nbsp; The cosine, and what it is not"),
  ("p", "A cosine appears in almost every equation in this course, and it is "
        "the same cosine every time: the angle between a direction and the "
        "surface normal."),
  ("callout", "Lambert's cosine law is geometry",
   ["A beam of light with a fixed cross-section striking a surface "
    "head-on illuminates an area <i>A</i>. The same beam striking at "
    "angle &theta; illuminates an area <i>A</i>/cos&theta; — a larger "
    "patch. The same power is spread over more surface, so the power "
    "<i>per unit area</i> is reduced by cos&theta;.",
    "<b>That is the entire content of the cosine law.</b> It is not an "
    "approximation, not a property of any particular material, and not "
    "something a shading model chooses to obey.",
    "The cosine appears whenever you convert between 'per unit area measured "
    "on the surface' and 'per unit area measured perpendicular to the "
    "beam'.",
    "<b>A Lambertian surface is therefore not 'one that obeys the cosine "
    "law'</b>, which is how it is usually described and is wrong. Everything "
    "obeys the cosine law. A Lambertian surface is one whose <i>BRDF</i> is "
    "constant in direction — it scatters incoming light equally into all "
    "outgoing directions."]),

  ("break",),
  ("h1", "3 &nbsp; Invariance along a ray"),
  ("p", "This is the property the whole algorithm rests on, and it is worth "
        "the two minutes it takes to see why it holds."),
  ("p", "Consider two small patches, d<i>A</i>&#8321; and d<i>A</i>&#8322;, "
        "facing each other at distance <i>r</i>, with normals making angles "
        "&theta;&#8321; and &theta;&#8322; with the line between them. The "
        "flux leaving the first and arriving at the second is"),
  ("eq", "d&#178;&Phi; = L dA&#8321; cos&theta;&#8321; d&omega;&#8321; "
         "&nbsp;&nbsp;where&nbsp;&nbsp; d&omega;&#8321; = dA&#8322; "
         "cos&theta;&#8322; / r&#178;"),
  ("p", "This expression is symmetric in the two patches: substituting gives "
        "d&#178;&Phi; = <i>L</i> d<i>A</i>&#8321; cos&theta;&#8321; "
        "d<i>A</i>&#8322; cos&theta;&#8322; / <i>r</i>&#178;, which is "
        "unchanged if the labels are swapped. The same flux is leaving the "
        "first patch as is arriving at the second, and both are described by "
        "the same radiance <i>L</i>. Nothing has been lost in between."),
  ("callout", "Why irradiance falls off and radiance does not",
   ["Move a surface twice as far from a light. The irradiance it receives "
    "drops by a factor of four — the inverse square law, which is real.",
    "But the solid angle the <i>light</i> subtends at the surface also drops "
    "by a factor of four. Radiance is power per unit area <i>per unit solid "
    "angle</i>, so the two factors of four cancel exactly and the radiance "
    "is unchanged.",
    "<b>The everyday version:</b> a white wall does not get darker as you "
    "walk away from it. Each patch of wall sends you less power, and each "
    "patch occupies proportionally less of your visual field. The brightness "
    "per unit of visual field — which is radiance, and is what you "
    "perceive — is constant.",
    "<b>This also explains why the sun and a photograph of the sun can have "
    "the same apparent brightness</b> while differing enormously in total "
    "power."]),
  ("callout", "What this licenses",
   ["If radiance were attenuated along a ray, a renderer would have to "
    "integrate along every segment of every path through empty space, and "
    "the cost of a ray would depend on its length.",
    "Because radiance is invariant, <b>a ray is a lookup</b>: trace until "
    "you hit a surface, evaluate the radiance leaving that surface toward "
    "you, and that value is exactly the radiance arriving at the ray's "
    "origin. No integration along the way.",
    "So ray tracing is not an approximation to light transport. It is an "
    "exact consequence of radiance invariance in a vacuum, and the "
    "approximations in a ray tracer are all in how the integrals at "
    "<i>surfaces</i> are estimated.",
    "<b>The vacuum assumption is load-bearing.</b> Module 10 fills space "
    "with participating media, invariance fails, and the lookup becomes an "
    "integral along the ray again — which is why volumetric rendering is "
    "so much more expensive than it looks."]),

  ("h1", "4 &nbsp; The BRDF"),
  ("p", "Having established what travels along a ray, we need the function "
        "that describes what happens when it meets a surface."),
  ("eq", "f(p, &omega;<sub>i</sub>, &omega;<sub>o</sub>) &nbsp;=&nbsp; "
         "dL<sub>o</sub>(p, &omega;<sub>o</sub>) / dE(p, &omega;<sub>i</sub>) "
         "&nbsp;=&nbsp; dL<sub>o</sub>(p, &omega;<sub>o</sub>) / "
         "( L<sub>i</sub>(p, &omega;<sub>i</sub>) cos&theta;<sub>i</sub> "
         "d&omega;<sub>i</sub> )"),
  ("p", "In words: of the differential irradiance arriving at <i>p</i> from "
        "direction &omega;<sub>i</sub>, what fraction is scattered into "
        "direction &omega;<sub>o</sub> per unit solid angle? Its units are "
        "inverse steradians."),
  ("callout", "A BRDF is a density, so it is not bounded by 1",
   ["Students reasonably expect a 'fraction of light reflected' to lie "
    "between 0 and 1. The BRDF is not that fraction — it is a "
    "<i>density</i> with respect to solid angle, and densities can be "
    "arbitrarily large where they are concentrated.",
    "A perfect mirror is the extreme case: it reflects all the incoming "
    "light into a single direction of zero solid angle, so its BRDF is a "
    "Dirac delta and is unbounded. This is not a pathology to be "
    "regularised away; it is why specular surfaces need separate handling "
    "throughout a renderer (Module 07).",
    "<b>What is bounded is the integral.</b> Energy conservation constrains "
    "&int; f cos&theta; d&omega; &le; 1, not f itself."]),
  ("table", ["Property", "Statement", "Consequence of violating it"],
   [["<b>Non-negativity</b>", "f &ge; 0 for all directions.",
     "Negative radiance, which propagates and produces black or NaN pixels "
     "far from the offending surface."],
    ["<b>Reciprocity</b>",
     "f(p, &omega;<sub>i</sub>, &omega;<sub>o</sub>) = f(p, "
     "&omega;<sub>o</sub>, &omega;<sub>i</sub>).",
     "<b>Bidirectional methods give wrong answers</b> — see below."],
    ["<b>Energy conservation</b>",
     "&int; f(p, &omega;<sub>i</sub>, &omega;<sub>o</sub>) "
     "cos&theta;<sub>i</sub> d&omega;<sub>i</sub> &le; 1 for every "
     "&omega;<sub>o</sub>.",
     "<b>Paths gain energy at each bounce.</b> Russian roulette fails to "
     "terminate, images brighten without converging, and the renderer may "
     "diverge rather than merely look wrong."]],
   [0.20, 0.38, 0.42]),
  ("callout", "Reciprocity is not a formality",
   ["Reciprocity states that the BRDF is unchanged when the incoming and "
    "outgoing directions are exchanged: light does not care which way along "
    "the path it is travelling.",
    "<b>Every bidirectional method in Module 11 depends on it.</b> Light "
    "tracing, bidirectional path tracing, and photon mapping all construct "
    "paths starting from a light source and then use them as though they had "
    "been constructed from the camera. That substitution is valid precisely "
    "because the BRDF is reciprocal.",
    "A non-reciprocal BRDF gives different answers depending on how a path "
    "happened to be built, which shows up as an inconsistency between "
    "integrators on the same scene — an extremely confusing bug, because "
    "each integrator is individually self-consistent.",
    "<b>Several widely used real-time shading models are not reciprocal</b>, "
    "having never been required to be. A model that served you well in "
    "CSCE 641 may be unusable here, and checking is cheap: evaluate it with "
    "the arguments swapped."]),

  ("h1", "5 &nbsp; What a pixel actually is"),
  ("eq", "I = &int;&int;&int;&int;&int; w(x,y) L(x, y, &omega;, t, &lambda;) "
         "S(&lambda;) d&lambda; dt d&omega; dx dy"),
  ("table", ["Dimension", "Integrates over", "Which produces"],
   [["x, y", "The pixel's spatial footprint, weighted by the reconstruction "
     "filter w.", "<b>Antialiasing</b>"],
    ["&omega;", "The directions admitted by the lens aperture.",
     "<b>Depth of field</b>"],
    ["t", "The shutter interval.", "<b>Motion blur</b>"],
    ["&lambda;", "Wavelength, weighted by the sensor response S.",
     "<b>Colour</b>, and dispersion (Module 13)"]],
   [0.14, 0.52, 0.34]),
  ("callout", "Four features, one integral",
   ["In a rasteriser, antialiasing, depth of field, and motion blur are "
    "three separate systems with three separate implementations, three sets "
    "of artefacts, and three sets of tuning parameters.",
    "In a Monte Carlo renderer they are <b>three more dimensions of the same "
    "integral</b>, and the machinery that handles one handles all of them "
    "without modification: jitter the sample position within the pixel, the "
    "sample point on the lens, the sample time within the shutter interval, "
    "and the sampled wavelength.",
    "<b>This is the structural advantage of the approach</b>, and it is why "
    "offline renderers get these effects almost free while real-time "
    "renderers fight for each one separately.",
    "It is also why Module 06 — how to choose those sample points well "
    "— pays off across every feature at once."]),
 ],
 "resources": [
   ("PBRT 4th ed. &mdash; Chapter 4, Radiometry, Spectra, and Colour",
    "https://pbr-book.org/4ed/Radiometry,_Spectra,_and_Color",
    "The definitive treatment of this module. &sect;4.1 for the quantities "
    "and &sect;4.2 for radiance invariance. Skip the colour sections until "
    "Module 13."),
   ("Scratchapixel &mdash; Mathematics of Shading / solid angle",
    "https://www.scratchapixel.com/lessons/3d-basic-rendering/"
    "introduction-to-shading/",
    "Slower than PBRT with the algebra written out. The best free "
    "explanation of solid angle if the PBRT version moves too fast."),
   ("TU Wien Rendering &mdash; early lectures on radiometry",
    "https://www.youtube.com/playlist?list=PLujxSBD-JXgnGmsn7gEyN28P1DnRZG7qi",
    "The intuition for why radiance is the transported quantity, developed "
    "visually."),
   ("PBRT 4th ed. &mdash; &sect;5.4, The Camera Measurement Equation",
    "https://pbr-book.org/4ed/Cameras_and_Film",
    "The pixel integral of &sect;5, derived properly, including the "
    "importance function that makes bidirectional methods possible."),
 ],
 "exercises": [
   "Integrate the constant function 1 over the hemisphere numerically, in "
   "spherical coordinates. Confirm you get 2&pi;. Then delete the "
   "sin&theta; and report what you get instead — that number is the error "
   "you are protecting yourself against for the rest of the course.",
   "Write the hemisphere check as a unit test in the repository you will use "
   "all semester. It should run in under a millisecond.",
   "Compute the solid angle subtended by the sun from Earth, and by a 1&nbsp;m "
   "square light panel at 3&nbsp;m. Express both in steradians and as a "
   "fraction of the sphere.",
   "Derive the radiance invariance result of &sect;3 yourself, writing out "
   "both directions explicitly. Do not read it again first.",
   "Verify the Lambertian normalisation: show that a BRDF of "
   "&rho;/&pi; conserves energy for &rho; &le; 1, and explain where the "
   "&pi; comes from. Most people get this wrong the first time.",
   "Take a shading model from your CSCE 641 renderer and test it for "
   "reciprocity numerically over 1000 random direction pairs. Report the "
   "maximum relative asymmetry.",
   "Test the same model for energy conservation: integrate f cos&theta; over "
   "the hemisphere for twenty outgoing directions, including grazing ones. "
   "Report the maximum. Many popular models exceed 1 at grazing angles.",
   "Look up the luminous efficacy of a 60&nbsp;W-equivalent LED bulb and "
   "convert its lumen rating into watts of radiant flux, stating your "
   "assumption about its spectrum.",
 ],
 "selfcheck": [
   "Name the five radiometric quantities with their units, and say what "
   "distinguishes radiance from irradiance.",
   "Give four reasons radiance is the quantity a renderer transports.",
   "Write the solid angle element in spherical coordinates and say what goes "
   "wrong if the sin&theta; is dropped.",
   "Explain the cosine law in one sentence, without using the word "
   "'Lambertian'. Then define what a Lambertian surface actually is.",
   "Why is radiance invariant along a ray, and why does irradiance obey an "
   "inverse square law when radiance does not?",
   "What does radiance invariance license, and which assumption does "
   "Module 10 remove?",
   "Why is a BRDF not bounded by 1, and what quantity <i>is</i> bounded?",
   "State the three required properties of a BRDF, and say which one causes "
   "divergence rather than merely incorrect output.",
   "List the five dimensions of the pixel integral and the rendering effect "
   "each one produces.",
 ],
},

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "The Rendering Equation",
 "subtitle": "One line, published in 1986, with no closed-form solution.",
 "question": "What single equation describes all of light transport?",
 "outcomes": [
     "State the rendering equation and explain every term.",
     "Explain why its self-reference is the whole difficulty.",
     "Write it in operator form and expand it as a Neumann series.",
     "Interpret the k-th term of that series as the paths of length k.",
     "Convert between the hemispherical and area forms and say what each is "
     "for.",
     "State what the equation omits.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The equation",
   "blurb": "Kajiya, SIGGRAPH 1986."},

  {"t": "eq", "kicker": "Kajiya 1986", "title": "The rendering equation",
   "eqs": [
     ("Lo(p, ωo)  =  Le(p, ωo)  +  ∫  f(p, ωi, ωo) Li(p, ωi) |cos θi| dωi",
      "Radiance leaving a point equals what the point emits plus what it "
      "reflects, integrated over all incoming directions on the hemisphere."),
   ],
   "caption": "Every image in this course is an estimate of this integral. "
              "Nothing else is going on.",
   "note": "Leave this slide up longer than feels comfortable. Everything "
           "that follows for thirteen modules is a consequence."},

  {"t": "table", "kicker": "Term by term", "title": "What each symbol is",
   "header": ["Term", "Is", "Comes from"],
   "widths": [2.5, 5.0, 4.6],
   "rows": [
     ["Lo(p, ωo)", "Radiance leaving p toward ωo", "<b>What we want</b>"],
     ["Le(p, ωo)", "Radiance p emits itself", "The scene: zero except on lights"],
     ["f(p, ωi, ωo)", "The BRDF", "The material (Module 07)"],
     ["Li(p, ωi)", "Radiance arriving from ωi", "<b>Another point's Lo</b>"],
     ["|cos θi|", "Projected area", "Geometry (Module 01)"],
     ["∫ … dωi", "Over the hemisphere", "2&pi; steradians"],
   ],
   "note": "Line 4 is the one to dwell on. Li is not an input — it is Lo "
           "somewhere else."},

  {"t": "callout", "title": "The self-reference is the entire problem",
   "kind": "Why this is hard",
   "body": ["<b>Li on the right-hand side is Lo at another point.</b> The "
            "unknown appears inside its own integral.",
            "So this is a Fredholm integral equation of the second kind, and "
            "it has no closed-form solution for any scene of interest.",
            "<b>The physical meaning is global illumination:</b> a surface's "
            "brightness depends on every other surface, which depends on "
            "it.",
            "Every rendering algorithm ever published is a way of "
            "approximating this one integral. The differences between them "
            "are entirely differences in <i>how</i>."]},

  {"t": "section", "label": "Part 2", "title": "Operator form",
   "blurb": "The same equation, in a form you can solve by series."},

  {"t": "eq", "kicker": "Rewriting", "title": "As an operator equation",
   "eqs": [
     ("L  =  Le  +  T L",
      "Where T is the transport operator: 'reflect once and propagate'. "
      "Linear, because light is linear."),
     ("(I − T) L  =  Le        L  =  (I − T)⁻¹ Le",
      "Formally solvable — but inverting T means solving the original "
      "problem."),
     ("L  =  Le + T Le + T² Le + T³ Le + …",
      "The Neumann series. This one converges, and it is computable."),
   ],
   "caption": "The series converges because energy conservation makes T a "
              "contraction: each bounce loses energy.",
   "note": "Emphasise that convergence is guaranteed by the physics, not "
           "assumed. A non-conserving BRDF breaks it — Module 01's point."},

  {"t": "callout", "title": "The series is a sum over path lengths",
   "kind": "The key reinterpretation",
   "body": ["Each term of the Neumann series is the light that reaches the "
            "camera after exactly <i>k</i> bounces.",
            "<b>This converts an integral equation into a sum of ordinary "
            "integrals</b>, one per path length — and an ordinary "
            "integral is something Monte Carlo can estimate.",
            "So rendering becomes: sample paths of every length, weight each "
            "correctly, and add them up.",
            "<b>That is the path tracer of Module 08.</b> Everything between "
            "here and there is the machinery to do it efficiently."]},

  {"t": "table", "kicker": "The terms", "title": "What each term of the series is",
   "header": ["Term", "Path", "In an image"],
   "widths": [1.8, 4.6, 5.7],
   "rows": [
     ["Le", "camera → light", "Lights seen directly"],
     ["T Le", "camera → surface → light", "<b>Direct lighting</b>"],
     ["T&#178; Le", "camera → surface → surface → light", "<b>One bounce of indirect</b>"],
     ["T&#179; Le", "three surfaces", "Colour bleeding, soft fill light"],
     ["T&#8319; Le", "n surfaces", "Diminishing, but never exactly zero"],
   ],
   "footnote": "A rasteriser computes the first two terms exactly and "
               "approximates the rest with an ambient constant.",
   "note": "The footnote lands the comparison with CSCE 641. 'Ambient' was "
           "always a stand-in for the tail of this series."},

  {"t": "section", "label": "Part 3", "title": "The area form",
   "blurb": "The same equation, integrated over surfaces instead of "
            "directions."},

  {"t": "eq", "kicker": "Change of variable", "title": "Integrating over surfaces",
   "eqs": [
     ("Lo(p, ωo)  =  Le  +  ∫  f(p, p→q, ωo) Lo(q, q→p) G(p,q) V(p,q) dA(q)",
      "The integral now runs over every surface point q in the scene rather "
      "than over directions."),
     ("G(p,q)  =  cos θp cos θq / ‖p − q‖²",
      "The geometry term: the Jacobian of the change of variables from solid "
      "angle to area."),
     ("V(p,q)  =  1 if p and q see each other, else 0",
      "Visibility. Innocuous in notation; it is where all the cost is."),
   ],
   "caption": "The two forms describe the same physics. They differ in what "
              "is easy to sample.",
   "note": "V is a binary function with discontinuities everywhere. It is "
           "why the integrand is not smooth and why quadrature fails."},

  {"t": "two", "kicker": "Which form", "title": "When to use each",
   "lh": "Hemispherical form",
   "l": ["Integrate over directions.",
         "<b>Natural for sampling the BRDF:</b> pick a direction the "
         "material likes and trace.",
         "Visibility is implicit — you just trace the ray.",
         ("Fails on small bright lights: random directions miss them.", 1)],
   "rh": "Area form",
   "r": ["Integrate over surface points.",
         "<b>Natural for sampling lights:</b> pick a point on the light "
         "directly.",
         "Visibility is explicit — you must trace a shadow ray.",
         ("Fails on near-specular surfaces: the sampled point is rarely in "
          "the lobe.", 1)],
   "note": "The two failure modes are complementary. That observation is "
           "exactly what MIS exploits in Module 08 — plant it now."},

  {"t": "callout", "title": "Two forms, two failure modes, one fix",
   "kind": "Look ahead to Module 08",
   "body": ["Sampling directions handles glossy surfaces well and small "
            "lights terribly.",
            "Sampling light surfaces handles small lights well and glossy "
            "surfaces terribly.",
            "<b>Neither strategy is good enough alone, and the cases where "
            "each fails are exactly the cases where the other succeeds.</b>",
            "Veach's multiple importance sampling combines them with "
            "provably near-optimal weights. It is the single most important "
            "technique in the course, and it exists because of this slide."]},

  {"t": "section", "label": "Part 4", "title": "Limits",
   "blurb": "What the equation does not describe."},

  {"t": "bullets", "kicker": "Omissions", "title": "What Kajiya's equation leaves out",
   "items": [
     "<b>Participating media.</b> Assumes a vacuum between surfaces. "
     "Module 10 fixes this.",
     "<b>Subsurface scattering.</b> Light enters at one point and leaves at "
     "another; a BRDF cannot express it. Needs a BSSRDF.",
     "<b>Polarisation.</b> Light has a polarisation state the equation does "
     "not carry. Visible in some real materials.",
     "<b>Fluorescence and phosphorescence.</b> Wavelength in equals "
     "wavelength out, and emission is instantaneous.",
     "<b>Diffraction and interference.</b> It is a geometric-optics model; "
     "wave effects are absent. Thin films and iridescence need more.",
     "",
     "<b>None of these are approximations <i>within</i> the equation.</b> "
     "They are physics it does not model.",
   ],
   "note": "This matters: 'unbiased' means converging to the equation's "
           "answer, not to reality. Make that distinction explicit."},

  {"t": "callout", "title": "Unbiased means correct <i>for this equation</i>",
   "kind": "An important distinction",
   "body": ["When Module 05 says an estimator is unbiased, it means it "
            "converges to the value of the rendering equation.",
            "<b>It does not mean it converges to a photograph.</b> The "
            "equation omits the physics above, and the scene description "
            "omits far more.",
            "This distinction gets lost in practice, and it matters when a "
            "converged render still does not match a reference "
            "photograph — the bug may be in the model rather than the "
            "renderer.",
            "<b>Being clear about which you are debugging saves days.</b>"]},

  {"t": "table", "kicker": "Approaches", "title": "Three families of solution",
   "header": ["Family", "Method", "Status"],
   "widths": [2.7, 5.2, 4.2],
   "rows": [
     ["Finite element", "Radiosity: discretise surfaces, solve the linear system",
      "Largely abandoned — diffuse only"],
     ["<b>Monte Carlo</b>", "Sample paths, average the estimates",
      "<b>Won. The rest of this course</b>"],
     ["Approximation", "Ambient occlusion, irradiance probes, screen-space GI",
      "Real time — CSCE 641's domain"],
   ],
   "note": "Radiosity's failure is instructive: it was elegant, handled only "
           "diffuse, and scaled badly in the scene complexity that actually "
           "arrived."},

  {"t": "callout", "title": "Why Monte Carlo won",
   "kind": "The decisive properties",
   "body": ["<b>It is dimension-independent.</b> Error falls as 1/&radic;N "
            "regardless of how many dimensions the integral has — and a "
            "path of length k has about 2k dimensions. Every quadrature rule "
            "degrades catastrophically here.",
            "<b>It handles discontinuity.</b> Visibility makes the integrand "
            "discontinuous everywhere. Quadrature rules assume smoothness and "
            "lose their convergence guarantees without it.",
            "<b>It needs only point evaluation</b>, which is exactly what "
            "ray tracing provides.",
            "<b>It is unbiased</b>, so the answer improves monotonically in "
            "expectation and you can stop whenever the noise is acceptable."]},
 ],
 "takeaways": [
   "The rendering equation: outgoing radiance equals emitted plus the "
   "hemispherical integral of incoming radiance times BRDF times cosine.",
   "Its difficulty is entirely in the self-reference — the unknown "
   "appears inside its own integral, which is what global illumination "
   "means.",
   "In operator form L = Le + TL, with Neumann series L = &Sigma; "
   "T&#8319;Le. Energy conservation makes T a contraction, so the series "
   "converges.",
   "The k-th term is the light arriving after exactly k bounces. This turns "
   "an integral equation into a sum of ordinary integrals — which is "
   "the path tracer.",
   "The area form integrates over surfaces, with a geometry term and an "
   "explicit visibility term. Direction sampling and area sampling have "
   "complementary failure modes.",
   "The equation omits media, subsurface scattering, polarisation, "
   "fluorescence, and wave optics. 'Unbiased' means correct for the "
   "equation, not correct against a photograph.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The equation"),
  ("p", "James Kajiya's 1986 paper, <i>The Rendering Equation</i>, did "
        "something unusual: it did not propose an algorithm so much as "
        "identify what every rendering algorithm had been approximating "
        "without saying so. Once written down, the existing methods could be "
        "classified by which terms they kept."),
  ("eq", "L<sub>o</sub>(p, &omega;<sub>o</sub>) = "
         "L<sub>e</sub>(p, &omega;<sub>o</sub>) + "
         "&int;<sub>&Omega;</sub> f(p, &omega;<sub>i</sub>, "
         "&omega;<sub>o</sub>) L<sub>i</sub>(p, &omega;<sub>i</sub>) "
         "|cos&theta;<sub>i</sub>| d&omega;<sub>i</sub>"),
  ("table", ["Term", "Meaning", "Where it comes from"],
   [["L<sub>o</sub>(p, &omega;<sub>o</sub>)",
     "Radiance leaving point p in direction &omega;<sub>o</sub>.",
     "<b>The unknown.</b> This is what we are solving for."],
    ["L<sub>e</sub>(p, &omega;<sub>o</sub>)",
     "Radiance emitted by p itself.",
     "Given by the scene. Zero everywhere except on light sources."],
    ["f(p, &omega;<sub>i</sub>, &omega;<sub>o</sub>)",
     "The BRDF at p.", "The material model (Module 07)."],
    ["L<sub>i</sub>(p, &omega;<sub>i</sub>)",
     "Radiance arriving at p from direction &omega;<sub>i</sub>.",
     "<b>This is L<sub>o</sub> at whatever surface is visible along "
     "&omega;<sub>i</sub>.</b> Hence the difficulty."],
    ["|cos&theta;<sub>i</sub>|",
     "Cosine of the angle between &omega;<sub>i</sub> and the normal.",
     "Projected area (Module 01). Geometry, not material."],
    ["&int;<sub>&Omega;</sub> &hellip; d&omega;<sub>i</sub>",
     "Integral over the hemisphere above p.",
     "2&pi; steradians of incoming directions."]],
   [0.17, 0.38, 0.45]),
  ("callout", "The self-reference is the whole problem",
   ["Look at the fourth row. L<sub>i</sub> is not an input to the equation "
    "— it is L<sub>o</sub> evaluated at some other surface point, which "
    "is itself given by the same equation.",
    "The unknown appears on both sides, inside its own integral. "
    "Mathematically this is a <b>Fredholm integral equation of the second "
    "kind</b>, and for any scene more interesting than a sphere in a void it "
    "has no closed-form solution.",
    "Physically, the self-reference <i>is</i> global illumination: how "
    "bright a wall is depends on how bright the floor is, which depends on "
    "how bright the wall is. Every surface's appearance depends on every "
    "other surface's, simultaneously.",
    "<b>Every rendering algorithm ever published is a method for "
    "approximating this one integral.</b> Radiosity, path tracing, photon "
    "mapping, ambient occlusion, light probes, and screen-space global "
    "illumination differ only in how they approximate it and which terms "
    "they are willing to discard."]),

  ("h1", "2 &nbsp; Operator form and the Neumann series"),
  ("p", "The equation becomes tractable when written abstractly. Define the "
        "<b>transport operator</b> T, which takes a radiance distribution "
        "over the scene, reflects it once off every surface, and propagates "
        "the result. T is linear, because light is linear: doubling every "
        "source doubles every result, and the contribution of two sources is "
        "the sum of their individual contributions."),
  ("eq", "L = L<sub>e</sub> + T L"),
  ("p", "Formally this rearranges to L = (I &minus; T)<sup>&minus;1</sup> "
        "L<sub>e</sub>, which is useless as written — inverting T means "
        "solving the original problem. But the inverse has a series "
        "expansion:"),
  ("eq", "L = L<sub>e</sub> + T L<sub>e</sub> + T&#178; L<sub>e</sub> + "
         "T&#179; L<sub>e</sub> + &hellip; = &Sigma;<sub>k=0</sub><super>"
         "&infin;</super> T<super>k</super> L<sub>e</sub>"),
  ("callout", "Convergence is guaranteed by physics",
   ["A Neumann series converges when the operator is a contraction — "
    "when applying it reduces magnitude.",
    "<b>T is a contraction precisely because of energy conservation</b> "
    "(Module 01): each reflection returns at most as much energy as arrived, "
    "and in any real scene strictly less. So "
    "||T|| &lt; 1 and the series converges.",
    "This is a satisfying connection: the physical requirement that surfaces "
    "not create energy is exactly the mathematical condition that makes the "
    "series summable.",
    "<b>It also explains a failure mode.</b> A BRDF that violates energy "
    "conservation makes T non-contractive. The series diverges, which in a "
    "renderer appears as an image that gets brighter the longer you run it "
    "and Russian roulette that never terminates. If you see that, look for "
    "the non-conserving material before you look anywhere else."]),
  ("h2", "2.1 &nbsp; Reading the series as paths"),
  ("table", ["Term", "The path it represents", "What you see in the image"],
   [["L<sub>e</sub>", "camera &rarr; light",
     "Light sources viewed directly."],
    ["T L<sub>e</sub>", "camera &rarr; surface &rarr; light",
     "<b>Direct lighting.</b> Shadows and their boundaries."],
    ["T&#178; L<sub>e</sub>", "camera &rarr; surface &rarr; surface &rarr; "
     "light",
     "<b>One bounce of indirect.</b> Colour bleeding from a red wall onto a "
     "white floor; light reaching into shadow."],
    ["T&#179; L<sub>e</sub>", "three intervening surfaces",
     "Soft ambient fill. Individually subtle, collectively the difference "
     "between a render and a photograph."],
    ["T<super>k</super> L<sub>e</sub>", "k surfaces",
     "Diminishing geometrically, but never exactly zero. In a bright white "
     "room the tail is substantial."]],
   [0.13, 0.35, 0.52]),
  ("callout", "This is the step that makes rendering computable",
   ["The Neumann series converts an integral equation — the unknown "
    "inside its own integral — into an infinite <b>sum of ordinary "
    "integrals</b>. Each term is a perfectly conventional high-dimensional "
    "integral with no self-reference.",
    "And an ordinary integral is something Monte Carlo can estimate. So "
    "rendering becomes: generate light paths of every length, weight each "
    "one correctly, and sum.",
    "<b>That is the path tracer of Module 08.</b> Everything between here "
    "and there — intersection, acceleration, sampling theory, variance "
    "reduction, BSDFs — is the machinery needed to do it efficiently.",
    "It also explains the terminology you will meet constantly: a 'bounce "
    "limit' of 4 means truncating the series after T&#8308;, which is "
    "biased, and Russian roulette (Module 06) is the trick that terminates "
    "paths <i>without</i> introducing that bias."]),

  ("break",),
  ("h1", "3 &nbsp; The area form"),
  ("p", "The hemispherical form integrates over directions. An equivalent "
        "form integrates over the surfaces of the scene, obtained by a "
        "change of variables from solid angle to area."),
  ("eq", "L<sub>o</sub>(p, &omega;<sub>o</sub>) = L<sub>e</sub> + "
         "&int;<sub>A</sub> f(p, p&rarr;q, &omega;<sub>o</sub>) "
         "L<sub>o</sub>(q, q&rarr;p) G(p,q) V(p,q) dA(q)"),
  ("eq", "G(p,q) = cos&theta;<sub>p</sub> cos&theta;<sub>q</sub> / "
         "|p &minus; q|&#178; &nbsp;&nbsp;&nbsp;&nbsp; "
         "V(p,q) &isin; {0, 1}"),
  ("table", ["Term", "Role"],
   [["<b>G(p,q)</b>", "The <b>geometry term</b>: the Jacobian of the change "
     "of variables. The two cosines foreshorten both patches; the inverse "
     "square converts area at q into solid angle at p. It is symmetric in p "
     "and q, which matters for bidirectional methods."],
    ["<b>V(p,q)</b>", "<b>Visibility</b>: 1 if the segment between p and q "
     "is unobstructed, 0 otherwise. Trivial to write and the source of "
     "essentially all the computational cost — evaluating it once is a "
     "ray cast."]],
   [0.14, 0.86]),
  ("callout", "V is why quadrature fails",
   ["V is a binary function whose discontinuities lie along the silhouettes "
    "of every object in the scene, as seen from every point. The integrand "
    "is therefore discontinuous almost everywhere, in a pattern that depends "
    "on the full scene geometry.",
    "Classical numerical integration — Simpson's rule, Gaussian "
    "quadrature, anything with a convergence proof — assumes smoothness, "
    "usually several derivatives of it. On a discontinuous integrand those "
    "guarantees evaporate and the methods converge no faster than random "
    "sampling, often slower.",
    "<b>Monte Carlo does not care.</b> Its 1/&radic;N convergence requires "
    "only finite variance, not continuity, which is a large part of why it "
    "is the method that survived (&sect;5)."]),
  ("h2", "3.1 &nbsp; Which form to use"),
  ("table", ["", "Hemispherical form", "Area form"],
   [["Integrates over", "Directions on the hemisphere.",
     "Surface points in the scene."],
    ["Natural sampling", "<b>Sample the BRDF:</b> choose a direction the "
     "material is likely to scatter into, and trace a ray.",
     "<b>Sample the lights:</b> choose a point on a light source directly, "
     "and trace a shadow ray to it."],
    ["Visibility", "Implicit — tracing the ray resolves it.",
     "Explicit — V must be evaluated with a shadow ray."],
    ["<b>Fails when</b>",
     "<b>Lights are small or distant.</b> Random directions almost never hit "
     "a small light, so almost every sample returns zero and the few that "
     "hit return a large value. Enormous variance.",
     "<b>Surfaces are near-specular.</b> The sampled light point is almost "
     "never inside the narrow BRDF lobe, so almost every sample contributes "
     "nothing. Enormous variance."]],
   [0.13, 0.43, 0.44]),
  ("callout", "The complementary failure is the key observation",
   ["Direction sampling is excellent for glossy surfaces and terrible for "
    "small lights. Light sampling is excellent for small lights and terrible "
    "for glossy surfaces.",
    "<b>The cases where each strategy fails are precisely the cases where "
    "the other succeeds.</b> This is not a coincidence — both strategies "
    "are trying to concentrate samples where the integrand is large, and "
    "the integrand is a product of a BRDF factor and a light factor. Each "
    "strategy matches one factor and ignores the other.",
    "Eric Veach's <b>multiple importance sampling</b> combines several "
    "strategies with weights that are provably near-optimal, achieving "
    "variance close to the better strategy in every configuration without "
    "being told which one that is.",
    "<b>It is the single most important technique in this course</b>, it is "
    "about fifteen lines of code, and it exists because of the asymmetry on "
    "this page. Module 08."]),

  ("h1", "4 &nbsp; What the equation omits"),
  ("table", ["Omission", "What is assumed", "Consequence"],
   [["<b>Participating media</b>",
     "Vacuum between surfaces, so radiance is invariant along rays.",
     "No fog, smoke, clouds, or underwater scenes. <b>Module 10</b> "
     "generalises the equation to fix this."],
    ["<b>Subsurface scattering</b>",
     "Light leaves a surface at the point where it entered.",
     "Skin, marble, milk, and wax all look wrong. Requires a BSSRDF, which "
     "takes two surface points rather than one."],
    ["<b>Polarisation</b>",
     "Light has no polarisation state.",
     "Incorrect for some dielectric reflections and most sky models; "
     "visible through a polarising filter."],
    ["<b>Fluorescence, phosphorescence</b>",
     "Wavelength out equals wavelength in; emission is instantaneous.",
     "Fluorescent paints and optical brighteners — in laundry "
     "detergent, safety clothing — are unrepresentable."],
    ["<b>Wave optics</b>",
     "Geometric optics: light travels in rays and does not interfere.",
     "No diffraction, no thin-film iridescence, no structural colour. Soap "
     "bubbles, beetle shells, and CD surfaces need a different model."]],
   [0.20, 0.36, 0.44]),
  ("callout", "'Unbiased' means correct for this equation, not for reality",
   ["Module 05 will define an unbiased estimator as one whose expected value "
    "equals the quantity being estimated. The quantity being estimated is "
    "<b>the value of the rendering equation for the scene as described</b>.",
    "It is not the value a camera would record. The equation omits the "
    "physics in the table above, and the scene description omits far more: "
    "measured BRDFs are fitted approximations, geometry is tessellated, "
    "textures are sampled, and the light spectra are guesses.",
    "This distinction is routinely lost, and it matters practically. When a "
    "fully converged render does not match a reference photograph, the "
    "discrepancy is usually in the model, not the integrator — and those "
    "are debugged completely differently.",
    "<b>Knowing which one you are debugging saves days.</b> The test that "
    "separates them is convergence: a renderer bug typically shows as a "
    "difference that persists at any sample count <i>and</i> changes with "
    "the integrator; a model error shows as a stable, converged image that "
    "is simply not the photograph."]),

  ("h1", "5 &nbsp; Three families of solution"),
  ("table", ["Family", "Approach", "Where it stands"],
   [["<b>Finite element</b>",
     "<b>Radiosity.</b> Discretise surfaces into patches, assume every patch "
     "is Lambertian, compute form factors between all pairs, and solve the "
     "resulting linear system.",
     "Largely abandoned. It handles only diffuse transport, the form-factor "
     "matrix is O(n&#178;) in patch count, and the meshing required is "
     "itself a hard problem. Historically important and worth knowing about."],
    ["<b>Monte Carlo</b>",
     "Sample light paths at random, weight each by the probability of having "
     "chosen it, and average.",
     "<b>Won, comprehensively.</b> Every production offline renderer is "
     "built this way. The rest of this course."],
    ["<b>Approximation</b>",
     "Compute the first terms of the series properly and replace the tail "
     "with something cheap: ambient occlusion, irradiance probes, "
     "screen-space global illumination, baked lightmaps.",
     "The domain of real-time rendering and of CSCE 641. Not wrong — "
     "correct for a stated budget, and the budget is the design "
     "constraint."]],
   [0.15, 0.44, 0.41]),
  ("callout", "Why Monte Carlo won",
   ["<b>Dimension independence.</b> Monte Carlo error falls as "
    "1/&radic;N regardless of dimension. A path with k bounces is an "
    "integral in roughly 2k dimensions, and the series sums over all k, so "
    "the effective dimension is unbounded. Every deterministic quadrature "
    "rule degrades exponentially with dimension; this one does not degrade "
    "at all.",
    "<b>Discontinuity tolerance.</b> Convergence needs only finite variance, "
    "not smoothness. Given what &sect;3 said about V, this is decisive.",
    "<b>Point evaluation is sufficient.</b> Monte Carlo needs only the "
    "ability to evaluate the integrand at a point, which is exactly what a "
    "ray cast provides. No derivatives, no structure, no mesh.",
    "<b>Unbiasedness.</b> The estimate improves in expectation with every "
    "additional sample and converges to the right answer, so you can stop "
    "when the noise is acceptable rather than committing to a discretisation "
    "in advance. Module 05 makes all of this precise."]),
 ],
 "resources": [
   ("Kajiya &mdash; The Rendering Equation (1986, free PDF)",
    "https://www.cse.chalmers.se/edu/year/2011/course/TDA361/2007/rend_eq.pdf",
    "The original paper. Short, readable, and worth reading in the original "
    "— the framing of the problem is the contribution."),
   ("PBRT 4th ed. &mdash; Chapter 13, Light Transport I: Surface Reflection",
    "https://pbr-book.org/4ed/Light_Transport_I_Surface_Reflection",
    "The rendering equation, both forms, the path-integral formulation, and "
    "the derivation of the geometry term."),
   ("Veach thesis &mdash; Chapter 8, The Path Integral Formulation",
    "https://graphics.stanford.edu/papers/veach_thesis/",
    "The cleanest statement of the measurement equation and the path "
    "integral. Read it before Module 11; skim it now."),
   ("TU Wien Rendering &mdash; the rendering equation lectures",
    "https://www.youtube.com/playlist?list=PLujxSBD-JXgnGmsn7gEyN28P1DnRZG7qi",
    "The Neumann-series-as-path-lengths interpretation, built up visually. "
    "Good complement to &sect;2."),
 ],
 "exercises": [
   "Write the rendering equation from memory, then check it. Repeat until "
   "you can produce it exactly, including which quantities carry which "
   "arguments.",
   "Derive the area form from the hemispherical form, showing explicitly "
   "that the Jacobian of the change of variables is the geometry term.",
   "For a scene of two parallel unit squares facing each other at unit "
   "distance, both Lambertian with albedo 0.5, one emitting, compute the "
   "first three terms of the Neumann series by hand. Report the ratio "
   "between successive terms.",
   "Repeat the previous exercise with albedo 0.9 and report the ratio. "
   "Explain what this implies about bounce limits in bright scenes.",
   "In a renderer or in PBRT, render a Cornell box with maximum path depths "
   "of 1, 2, 3, 5, and 16. Difference consecutive images and report the "
   "energy in each difference. Plot it.",
   "For the same scene, measure what fraction of total image energy comes "
   "from paths of each length. Compare a white box against a dark one.",
   "Construct a scene where direction sampling has very high variance, and "
   "another where light sampling does. Render both with both strategies and "
   "report the variance in each of the four cases.",
   "Pick one omission from &sect;4 and write a page on what would have to "
   "change in the equation to include it. Participating media and "
   "fluorescence are the most instructive.",
 ],
 "selfcheck": [
   "State the rendering equation and name every term and its units.",
   "Why does the equation have no closed-form solution, and what is the "
   "physical meaning of that fact?",
   "Write the operator form and the Neumann series, and say what guarantees "
   "convergence.",
   "What does the k-th term of the series represent, and what does a bounce "
   "limit of 4 correspond to?",
   "What is the geometry term, and where does it come from?",
   "Why is the visibility term the reason classical quadrature is "
   "unsuitable?",
   "Give the failure mode of direction sampling and of area sampling, and "
   "say why their combination is promising.",
   "Name four things the rendering equation does not model.",
   "What exactly does 'unbiased' mean, and how would you tell a renderer bug "
   "from a scene-model error?",
   "Give three reasons Monte Carlo displaced radiosity.",
 ],
},

]

# --- additional module batches ----------------------------------------------
for _b in ("c647_b2", "c647_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
