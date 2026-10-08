# -*- coding: utf-8 -*-
"""CSCE 641 — Modules 11-13."""

MODULES = [

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Physically Based Shading and Image-Based Lighting",
 "subtitle": "Replacing the curve fit with something that conserves energy.",
 "question": "What would a shading model look like if it were derived rather "
             "than fitted?",
 "outcomes": [
     "State the reflectance equation and identify each term in a shader.",
     "Explain the microfacet model and the role of D, F, and G.",
     "Implement a Cook–Torrance BRDF with metallic/roughness parameters.",
     "Explain the split-sum approximation and implement image-based lighting.",
     "Explain why tonemapping is required once lighting is physical.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The equation everything "
                                              "approximates",
   "blurb": "Module 06 fitted curves. This module derives them."},

  {"t": "eq", "kicker": "Reflectance", "title": "The reflectance equation",
   "eqs": [
     ("L_o(v) = ∫_Ω f_r(l,v) L_i(l) (n·l) dω",
      "Outgoing radiance is incoming radiance, weighted by the BRDF and the "
      "cosine, integrated over the hemisphere."),
     ("f_r(l,v)",
      "The BRDF — the material. This is the only part you choose."),
     ("(n·l)",
      "Module 06's cosine law. Geometry, not material."),
   ],
   "caption": "Every shading model in real-time graphics is an approximation "
              "of this integral. CSCE 647 evaluates it properly; here we "
              "approximate it cheaply.",
   "note": "Point out that Module 06's diffuse shader is this integral with a "
           "constant BRDF and a single-direction light — so the integral "
           "collapses to a product."},

  {"t": "bullets", "kicker": "Requirements", "title": "What a physical BRDF must satisfy",
   "items": [
     "<b>Positivity</b> — fᵣ ≥ 0. Surfaces do not emit "
     "negative light.",
     "<b>Reciprocity</b> — fᵣ(l,v) = fᵣ(v,l). Swapping light "
     "and eye changes nothing.",
     "<b>Energy conservation</b> — the integral of outgoing light cannot "
     "exceed incoming.",
     "",
     "Blinn–Phong satisfies the first, roughly the second, and "
     "<b>fails</b> the third.",
     ("That failure is why materials had to be retuned under every lighting "
      "change.", 1),
     ("Fixing it is most of the practical benefit of PBR.", 1),
   ]},

  {"t": "section", "label": "Part 2", "title": "Microfacets",
   "blurb": "A rough surface is a mirror you cannot resolve."},

  {"t": "callout", "title": "The microfacet idea", "kind": "Key idea",
   "body": ["Model the surface as an enormous number of tiny perfect mirrors, "
            "each too small to see.",
            "Roughness describes the <i>distribution of their orientations</i>. "
            "Smooth means they all point the same way; rough means they are "
            "scattered.",
            "Only facets oriented exactly halfway between light and view can "
            "reflect light to the eye. So the halfway vector from Module 06 "
            "stops being a convenient trick and becomes a physical quantity: "
            "the normal of the facets that matter."]},

  {"t": "eq", "kicker": "Cook-Torrance", "title": "The specular BRDF, term by term",
   "eqs": [
     ("f_spec  =  D · F · G  /  (4 (n·l)(n·v))",
      "Three terms over a normalisation factor."),
     ("D(h)  —  normal distribution",
      "What fraction of facets point along h. Controls highlight shape and "
      "size."),
     ("F(v,h)  —  Fresnel",
      "How much light reflects rather than refracts. Rises sharply at "
      "grazing angles."),
     ("G(l,v)  —  geometry / masking-shadowing",
      "Facets blocking each other. Matters most on rough surfaces at grazing "
      "angles."),
   ],
   "caption": "Each term fixes one of the three defects of Blinn–Phong "
              "named in Module 06.",
   "note": "Make the correspondence explicit: D replaces the arbitrary "
           "exponent, F adds the missing rim brightening, G plus the "
           "denominator provide energy conservation."},

  {"t": "two", "kicker": "The terms", "title": "What each term actually does",
   "lh": "D — GGX / Trowbridge-Reitz",
   "l": ["Distribution of facet normals.",
         "Roughness α = (perceptual roughness)².",
         "GGX has a <b>long tail</b>: a tight core with a wide dim halo.",
         ("That tail is why GGX looks far more realistic than Beckmann or "
          "Phong on metals.", 1)],
   "rh": "F — Fresnel (Schlick)",
   "r": ["Reflectance rises toward 1 at grazing angles. Always.",
         "F₀ = reflectance at normal incidence.",
         "Dielectrics: F₀ ≈ 0.04, achromatic.",
         ("Metals: F₀ is the metal's colour — which is why gold "
          "has a gold highlight.", 1)],
   "note": "The metal/dielectric split in F0 is the single most important "
           "practical consequence of the model."},

  {"t": "code", "kicker": "Implementation", "title": "Cook-Torrance, complete",
   "lang": "glsl", "code": """
float D_GGX(float NdotH, float a) {
    float a2 = a * a;
    float d  = NdotH * NdotH * (a2 - 1.0) + 1.0;
    return a2 / (PI * d * d);
}
vec3 F_Schlick(float VdotH, vec3 F0) {
    return F0 + (1.0 - F0) * pow(1.0 - VdotH, 5.0);
}
float V_SmithGGX(float NdotL, float NdotV, float a) {
    // Visibility = G / (4 NdotL NdotV): folds in the denominator
    float l = NdotV * (NdotL * (1.0 - a) + a);
    float v = NdotL * (NdotV * (1.0 - a) + a);
    return 0.5 / max(l + v, 1e-5);
}

// F0: dielectrics are 0.04; metals take their colour from albedo.
vec3  F0      = mix(vec3(0.04), albedo, metallic);
vec3  F       = F_Schlick(VdotH, F0);
vec3  spec    = D_GGX(NdotH, a) * V_SmithGGX(NdotL, NdotV, a) * F;

// Metals have NO diffuse. Energy not reflected specularly is absorbed.
vec3  kD      = (1.0 - F) * (1.0 - metallic);
vec3  diffuse = kD * albedo / PI;

vec3  Lo = (diffuse + spec) * lightColor * NdotL;
""",
   "caption": "<code>kD = (1−F)(1−metallic)</code> is the energy "
              "bookkeeping: what is not reflected specularly is available to "
              "scatter diffusely, and metals have none of it.",
   "note": "Walk through kD slowly. It is the line that makes the model "
           "conserve energy, and it is the line people delete when 'metals "
           "look too dark'."},

  {"t": "table", "kicker": "Parameters", "title": "The metallic/roughness workflow",
   "header": ["Parameter", "Dielectric", "Metal"],
   "widths": [3.3, 4.4, 4.4],
   "rows": [
     ["Albedo means", "Diffuse colour", "Specular colour (F₀)"],
     ["F₀", "0.04, achromatic", "The albedo — coloured"],
     ["Diffuse", "Present", "<b>None</b>"],
     ["Examples", "Plastic, wood, skin, stone", "Gold, copper, iron, aluminium"],
   ],
   "note": "Intermediate metallic values are physically meaningless; they "
           "exist only to blend between material regions in a texture."},

  {"t": "section", "label": "Part 3", "title": "Image-based lighting",
   "blurb": "Lighting from an environment, not from a list of point lights."},

  {"t": "bullets", "kicker": "IBL", "title": "The problem and the trick",
   "items": [
     "Real environments light surfaces from <b>every</b> direction, not from "
     "three point lights.",
     "Store the environment as an HDR cube map and integrate over it.",
     "",
     "But the integral has thousands of samples per pixel. Not real time.",
     "",
     "<b>Split-sum approximation:</b> factor the integral into two parts, "
     "each precomputable.",
     ("One depends only on the environment — prefilter it once.", 1),
     ("One depends only on roughness and viewing angle — a 2D lookup "
      "table, computed once ever.", 1),
   ]},

  {"t": "eq", "kicker": "IBL", "title": "The split-sum approximation",
   "eqs": [
     ("∫ f_r L_i (n·l) dω  ≈  (prefiltered L) × (BRDF integral)",
      "Separate the lighting from the material response."),
     ("prefiltered environment map",
      "Mip level n = roughness n. Convolved with the GGX lobe, offline."),
     ("BRDF LUT(n·v, roughness)  →  (scale, bias) for F₀",
      "A 2D texture. Scene-independent — generate it once and ship it."),
   ],
   "caption": "Two texture fetches replace an integral over the hemisphere. "
              "This is the technique that made PBR viable in real time.",
   "note": "Worth stating how good the approximation is: it assumes v = n = r, "
           "which is exact head-on and degrades at grazing angles. Visible "
           "mainly on rough metal."},

  {"t": "code", "kicker": "IBL", "title": "Evaluating IBL",
   "lang": "glsl", "code": """
// --- diffuse: irradiance map, cosine-convolved offline
vec3 irradiance = texture(uIrradianceMap, N).rgb;
vec3 diffuseIBL = irradiance * albedo;

// --- specular: prefiltered env + BRDF LUT
vec3  R          = reflect(-V, N);
float lod        = roughness * MAX_REFLECTION_LOD;
vec3  prefiltered = textureLod(uPrefilteredMap, R, lod).rgb;
vec2  ab          = texture(uBRDFLut, vec2(max(dot(N,V),0.0), roughness)).rg;
vec3  specularIBL = prefiltered * (F0 * ab.x + ab.y);

// --- combine. AO applies to ambient only, never to direct light.
vec3 kD     = (1.0 - F) * (1.0 - metallic);
vec3 ambient = (kD * diffuseIBL + specularIBL) * occlusion;
""",
   "caption": "Three precomputed resources: an irradiance cube map, a "
              "roughness-mipped prefiltered cube map, and one scene-"
              "independent 2D LUT.",
   "note": "Stress that AO multiplies ambient only. Applying it to direct "
           "light double-darkens and is a very common error."},

  {"t": "callout", "title": "Now you must tonemap", "kind": "Consequence",
   "body": ["Physical lighting produces physical values. The sun is "
            "~100,000 lux; an interior is ~300. These do not fit in [0,1].",
            "Rendering in HDR and then simply clipping to the display range "
            "destroys everything bright: highlights become flat white blobs "
            "and all colour in them is lost.",
            "A tonemapping curve compresses the high dynamic range to the "
            "display's range while preserving contrast where the eye looks. "
            "ACES and Khronos PBR Neutral are the current standards; Reinhard "
            "is the simple one to start with.",
            "Tonemap, <i>then</i> apply the sRGB encode from Module 06. In "
            "that order."]},
 ],
 "takeaways": [
   "The reflectance equation is what every shading model approximates. The "
   "BRDF is the only part that is the material.",
   "A physical BRDF must be positive, reciprocal, and energy-conserving. "
   "Blinn–Phong fails the third, and that failure is why materials never "
   "transferred between scenes.",
   "Microfacet theory makes the halfway vector physical: it is the normal of "
   "the facets that can reflect light to the eye.",
   "D sets the highlight shape, F adds the grazing-angle brightening every "
   "real surface has, G and the denominator conserve energy.",
   "Metals have coloured F₀ and no diffuse; dielectrics have F₀ "
   "≈ 0.04 and a diffuse term. That split is the whole workflow.",
   "The split-sum approximation reduces an environment integral to two "
   "texture fetches — and physical lighting then forces you to tonemap.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The reflectance equation"),
  ("p", "Module 06 built shading from plausible curves. This module starts "
        "from the physics and derives what the curve should have been. The "
        "starting point is the reflectance equation, which says how much "
        "light leaves a surface in a given direction:"),
  ("eq", "L&#8338;(v) = &int;<sub>&Omega;</sub> f<sub>r</sub>(l, v) &middot; L&#7522;(l) &middot; (n &middot; l) d&omega;"),
  ("table", ["Term", "Meaning"],
   [["L&#8338;(v)", "Radiance leaving toward the viewer — what the pixel "
     "measures."],
    ["&int;<sub>&Omega;</sub>", "Integrate over the hemisphere above the "
     "surface: light arrives from every direction, not just from a list of "
     "lights."],
    ["f<sub>r</sub>(l, v)", "The BRDF. The complete description of the material, "
     "and the only term you get to choose."],
    ["L&#7522;(l)", "Radiance arriving from direction l."],
    ["(n &middot; l)", "Module 06's cosine law: the geometric foreshortening "
     "of the incoming beam."]],
   [0.16, 0.84]),
  ("p", "Module 06's diffuse shader is this integral in a degenerate case: a "
        "constant BRDF and a single delta-function light direction, so the "
        "integral collapses to a product. Everything in this module is about "
        "doing better on the BRDF, and then about evaluating the integral "
        "when the light is an entire environment rather than a point."),
  ("h2", "1.1 &nbsp; What a BRDF must satisfy"),
  ("ol", ["<b>Positivity.</b> f<sub>r</sub> &ge; 0 everywhere. Surfaces do not "
          "remove light.",
          "<b>Helmholtz reciprocity.</b> f<sub>r</sub>(l, v) = f<sub>r</sub>(v, l). "
          "Exchanging the light and the eye gives the same result. This is "
          "required for bidirectional path tracing to be valid at all.",
          "<b>Energy conservation.</b> For any incoming direction, the "
          "integral of the BRDF times the cosine over the outgoing hemisphere "
          "is at most 1. A surface cannot reflect more light than it "
          "receives."]),
  ("callout", "Why energy conservation is the practical one",
   ["Blinn&ndash;Phong violates it: changing the shininess exponent changes "
    "total reflected energy arbitrarily.",
    "The production consequence is that materials do not transfer. A material "
    "tuned to look right in one lighting setup looks wrong in another, so "
    "every asset must be re-authored per environment. That cost, multiplied "
    "across a large project, is enormous.",
    "An energy-conserving model with physically meaningful parameters makes "
    "materials portable. That, far more than any single image being prettier, "
    "is why the industry moved to PBR."]),

  ("h1", "2 &nbsp; Microfacet theory"),
  ("p", "Model the surface as a vast collection of microscopic perfect "
        "mirrors — <b>microfacets</b> — each far too small to "
        "resolve. What we call roughness is the statistical distribution of "
        "their orientations: a smooth surface has facets mostly aligned with "
        "the macroscopic normal, a rough one has them scattered widely."),
  ("p", "A perfect mirror reflects light from <b>l</b> to <b>v</b> only if "
        "its normal is exactly the halfway vector <b>h</b> = normalize(l + v). "
        "So the only facets contributing to what you see are those oriented "
        "along <b>h</b>. The halfway vector of Blinn&ndash;Phong, introduced "
        "in Module 06 as a cheaper approximation to the reflection vector, "
        "turns out to be the physically meaningful quantity all along."),
  ("h2", "2.1 &nbsp; The Cook&ndash;Torrance form"),
  ("eq", "f<sub>spec</sub> = D(h) &middot; F(v, h) &middot; G(l, v) / (4 (n&middot;l)(n&middot;v))"),
  ("table", ["Term", "Models", "Controls", "Fixes which Blinn&ndash;Phong defect"],
   [["<b>D</b> &mdash; normal distribution",
     "What fraction of facets are oriented along h.",
     "Highlight size and shape.",
     "The arbitrary, unnormalised exponent."],
    ["<b>F</b> &mdash; Fresnel",
     "How much light reflects rather than refracting into the surface.",
     "Grazing-angle brightening; metal colour.",
     "The missing rim reflection that made everything look like plastic."],
    ["<b>G</b> &mdash; geometry term",
     "Facets shadowing and masking each other.",
     "Darkening at grazing angles on rough surfaces.",
     "Energy conservation, together with the 4(n&middot;l)(n&middot;v) "
     "denominator."]],
   [0.22, 0.26, 0.22, 0.30]),
  ("h2", "2.2 &nbsp; D: GGX"),
  ("eq", "D<sub>GGX</sub>(h) = &alpha;&#178; / [ &pi; ( (n&middot;h)&#178;(&alpha;&#178; &minus; 1) + 1 )&#178; ]"),
  ("p", "GGX (Trowbridge&ndash;Reitz) replaced Beckmann and Phong "
        "distributions in production for one reason: its <b>long tail</b>. "
        "Real measured materials show a tight bright core surrounded by a "
        "wide, dim halo, and GGX reproduces that while Gaussian-like "
        "distributions cut off too quickly. The difference is most striking "
        "on metals, where the halo carries a great deal of the perceived "
        "material character."),
  ("p", "Note the parameterisation: &alpha; = (perceptual roughness)&#178;. "
        "Artists author perceptual roughness because the squared mapping "
        "distributes visual change more evenly across the slider. Getting "
        "this wrong makes the bottom half of the roughness range nearly "
        "unusable."),
  ("h2", "2.3 &nbsp; F: Fresnel"),
  ("eq", "F<sub>Schlick</sub>(v,h) = F&#8320; + (1 &minus; F&#8320;)(1 &minus; v&middot;h)&#8309;"),
  ("p", "Every surface becomes more reflective as the viewing angle "
        "approaches grazing — look along a sheet of paper and it is "
        "nearly a mirror. Schlick's approximation captures this in one line "
        "and is accurate enough that essentially nobody uses the full Fresnel "
        "equations in real time."),
  ("callout", "F&#8320; is where metals and dielectrics part",
   ["<b>Dielectrics</b> (plastic, wood, skin, stone, water): F&#8320; is "
    "about 0.04 and achromatic. Light that is not reflected refracts into the "
    "surface, scatters, and emerges as diffuse colour.",
    "<b>Metals</b> (gold, copper, iron): F&#8320; is high and <i>coloured</i> "
    "— it is the metal's characteristic colour. Light that is not "
    "reflected is absorbed by the free electrons, so there is <b>no diffuse "
    "term at all</b>.",
    "This is why a gold highlight is gold while a red plastic ball has a "
    "white highlight, and it is the single most useful fact in the whole "
    "metallic/roughness workflow."]),

  ("break",),
  ("h1", "3 &nbsp; Implementation"),
  ("code", """float D_GGX(float NdotH, float a) {
    float a2 = a*a;
    float d  = NdotH*NdotH * (a2 - 1.0) + 1.0;
    return a2 / (PI * d * d);
}

vec3 F_Schlick(float VdotH, vec3 F0) {
    return F0 + (1.0 - F0) * pow(1.0 - VdotH, 5.0);
}

// Smith height-correlated visibility: G / (4 NdotL NdotV) in one term.
float V_SmithGGX(float NdotL, float NdotV, float a) {
    float l = NdotV * (NdotL * (1.0 - a) + a);
    float v = NdotL * (NdotV * (1.0 - a) + a);
    return 0.5 / max(l + v, 1e-5);
}

void shade() {
    float a  = roughness * roughness;        // perceptual -> alpha
    vec3  F0 = mix(vec3(0.04), albedo, metallic);
    vec3  F  = F_Schlick(VdotH, F0);

    vec3 specular = D_GGX(NdotH, a) * V_SmithGGX(NdotL, NdotV, a) * F;

    // Energy bookkeeping: what is not reflected specularly may scatter
    // diffusely -- and metals have no diffuse at all.
    vec3 kD      = (1.0 - F) * (1.0 - metallic);
    vec3 diffuse = kD * albedo / PI;         // Module 06's 1/pi

    Lo += (diffuse + specular) * lightColor * NdotL;
}"""),
  ("callout", "The line people delete",
   ["<code>kD = (1 &minus; F) * (1 &minus; metallic)</code> is what makes the "
    "model conserve energy. It says: light reflected specularly is not "
    "available to scatter diffusely, and metals absorb rather than scatter.",
    "When a metal 'looks too dark', the instinct is to remove the "
    "<code>(1 &minus; metallic)</code> factor. Do not. A dark metal under a "
    "single point light is <i>correct</i> — metals derive almost all "
    "their appearance from reflecting their environment, and the fix is "
    "image-based lighting, not breaking the energy balance."]),

  ("h1", "4 &nbsp; Image-based lighting"),
  ("p", "Real surfaces are lit from every direction by a whole environment, "
        "not by two or three point lights. The reflectance equation is an "
        "integral over the hemisphere, and with an environment map as "
        "L&#7522; it would require thousands of samples per pixel. That is "
        "not a real-time budget."),
  ("h2", "4.1 &nbsp; The split-sum approximation"),
  ("p", "Karis's observation, from the Unreal Engine 4 course notes, is that "
        "the integral factors approximately into two independent pieces:"),
  ("eq", "&int; f<sub>r</sub> L<sub>i</sub> (n&middot;l) d&omega; &nbsp;&asymp;&nbsp; "
         "[ &int; L&#7522; d&omega; ] &times; [ &int; f<sub>r</sub> (n&middot;l) d&omega; ]"),
  ("ul", ["The <b>first</b> factor depends only on the environment and the "
          "roughness. Precompute it by convolving the environment map with "
          "the GGX lobe at several roughness values, stored in the mip chain "
          "of a cube map. Done once per environment.",
          "The <b>second</b> factor depends only on roughness and "
          "n&middot;v, not on the environment at all. It is therefore a "
          "scene-independent 2D lookup table, computed once ever and shipped "
          "with the engine."]),
  ("p", "The approximation assumes the view, normal, and reflection "
        "directions coincide, which is exact head-on and degrades toward "
        "grazing angles. The error shows mainly as slightly wrong stretching "
        "of reflections on rough metal at oblique angles, and in practice "
        "nobody notices."),
  ("code", """// Diffuse: irradiance map, cosine-convolved offline
vec3 irradiance = texture(uIrradianceMap, N).rgb;
vec3 diffuseIBL = irradiance * albedo;

// Specular: prefiltered environment + BRDF LUT
vec3  R           = reflect(-V, N);
vec3  prefiltered = textureLod(uPrefilteredMap, R,
                               roughness * MAX_REFLECTION_LOD).rgb;
vec2  ab          = texture(uBRDFLut, vec2(NdotV, roughness)).rg;
vec3  specularIBL = prefiltered * (F0 * ab.x + ab.y);

vec3 kD      = (1.0 - F) * (1.0 - metallic);
vec3 ambient = (kD * diffuseIBL + specularIBL) * occlusion;"""),
  ("callout", "Ambient occlusion multiplies ambient only",
   ["AO represents local self-occlusion of <i>indirect</i> light arriving "
    "from the environment. Direct light already has a shadow map (Module 10) "
    "telling it what is occluded.",
    "Multiplying direct light by AO as well double-darkens creases and makes "
    "the image look dirty. It is one of the most common PBR implementation "
    "errors, and it is visible once you know to look for it."]),

  ("h1", "5 &nbsp; Tonemapping"),
  ("p", "Once lighting is physically based, the values are physical. Sunlight "
        "is on the order of 100,000 lux; a lit interior is a few hundred. The "
        "ratio between the brightest and darkest meaningful values in a scene "
        "can easily exceed 10&#8309;:1, and a display offers roughly 100:1."),
  ("p", "Clipping the excess destroys it: every highlight becomes a flat "
        "white region, all colour within it is lost, and the image acquires "
        "the blown-out look characteristic of early HDR rendering. A "
        "<b>tonemapping</b> operator instead compresses the range smoothly, "
        "preserving contrast where the eye attends and rolling off gracefully "
        "into the highlights."),
  ("table", ["Operator", "Character", "Use"],
   [["Reinhard", "Simple, desaturates highlights noticeably.",
     "Easy starting point; fine for learning."],
    ["ACES filmic", "Film-like roll-off, slightly contrasty, well understood.",
     "The de facto standard for a decade; still a good default."],
    ["Khronos PBR Neutral", "Preserves material colour into highlights.",
     "Preferred where material fidelity matters, e.g. product visualisation."],
    ["AgX", "Very graceful hue handling at extreme exposure.",
     "Increasingly common; Blender's current default."]],
   [0.20, 0.44, 0.36]),
  ("callout", "Order matters",
   ["Render in HDR &rarr; tonemap &rarr; encode to sRGB (Module 06). In that "
    "order, every time.",
    "Tonemapping an already sRGB-encoded image applies a curve to a curve and "
    "produces muddy, low-contrast output. Encoding before tonemapping is the "
    "same error in the other direction."]),

  ("h1", "6 &nbsp; Project 2"),
  ("p", "You now have everything the second project requires: the microfacet "
        "BRDF from this module, image-based lighting from the split sum, "
        "shadow mapping from Module 10, antialiasing from Module 09, and the "
        "GPU pipeline from Module 07. Build the material sphere grid "
        "— roughness across one axis, metallic across the other — "
        "under a real HDR environment. It is the standard validation image "
        "for a PBR implementation, and errors in any of the above are "
        "immediately visible in it."),
 ],
 "resources": [
   ("Brian Karis — 'Real Shading in Unreal Engine 4' (SIGGRAPH course, "
    "free)",
    "https://blog.selfshadow.com/publications/s2013-shading-course/",
    "The split-sum approximation in the author's own words, with the "
    "practical shortcuts. The single most important reference for this "
    "module."),
   ("Sébastien Lagarde & Charles de Rousiers — 'Moving Frostbite to "
    "PBR' (free)",
    "https://seblagarde.wordpress.com/2015/07/14/siggraph-2014-moving-frostbite-to-physically-based-rendering-3-0/",
    "The most complete free account of a production PBR pipeline, including "
    "all the details other papers omit."),
   ("LearnOpenGL — PBR Theory, Lighting, and IBL",
    "https://learnopengl.com/PBR/Theory",
    "Complete working implementation of everything in this module, including "
    "generating the irradiance map, prefiltered map, and BRDF LUT."),
   ("Naty Hoffman — 'Physics and Math of Shading' (free)",
    "https://blog.selfshadow.com/publications/s2013-shading-course/",
    "The derivation of microfacet theory from first principles. Read this if "
    "the D, F, G decomposition feels arbitrary."),
   ("Physically Based Rendering, 4th ed. — free online",
    "https://pbr-book.org/",
    "Chapter 9 on reflection models. The rigorous treatment, and the bridge "
    "to CSCE 647."),
 ],
 "exercises": [
   "Implement the Cook&ndash;Torrance BRDF with GGX, Schlick Fresnel, and "
   "Smith visibility. Render a 7&times;7 sphere grid sweeping roughness "
   "against metallic under a single point light.",
   "Verify energy conservation numerically: integrate your BRDF times the "
   "cosine over the hemisphere by Monte Carlo sampling, for several roughness "
   "values, and confirm the result never exceeds 1. Do the same for "
   "Blinn&ndash;Phong and record where it fails.",
   "Generate the three IBL resources yourself from an HDR environment map: "
   "the irradiance cube map, the roughness-mipped prefiltered cube map, and "
   "the BRDF lookup table. Do not use a precomputed LUT.",
   "Render the same sphere grid under IBL. Compare the metals against the "
   "point-light version and explain in writing why they looked wrong before.",
   "Implement Reinhard and ACES tonemapping with an exposure control. Capture "
   "a high-dynamic-range scene with no tonemapping, with Reinhard, and with "
   "ACES.",
   "Deliberately apply ambient occlusion to direct light as well as ambient. "
   "Capture the difference and describe the artifact.",
   "<b>Project 2 is now due.</b> Assemble Modules 07&ndash;11 into the GPU "
   "renderer described in the syllabus, including the annotated RenderDoc "
   "capture.",
 ],
 "selfcheck": [
   "Write the reflectance equation and identify which term is the material, "
   "which is geometry, and which is the lighting.",
   "State the three properties a physical BRDF must satisfy. Which does "
   "Blinn&ndash;Phong violate, and what is the production consequence?",
   "Explain the microfacet model, and why the halfway vector is the "
   "physically meaningful direction.",
   "What does each of D, F, and G control, and which Blinn&ndash;Phong defect "
   "does each repair?",
   "Why do metals have no diffuse term? Why is their F&#8320; coloured?",
   "Explain the split-sum approximation: what are the two factors, what does "
   "each depend on, and what does the approximation assume?",
   "Why does physically based lighting force you to tonemap, and in what "
   "order do tonemapping and sRGB encoding occur?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Geometry: Meshes, Curves, and Tessellation",
 "subtitle": "How surfaces are represented, and what each representation "
             "makes easy.",
 "question": "What is the right data structure for a surface?",
 "outcomes": [
     "Explain mesh connectivity structures and what queries each makes fast.",
     "Evaluate Bezier and B-spline curves and state their continuity "
     "properties.",
     "Explain subdivision surfaces and their relationship to splines.",
     "Describe LOD strategies and the popping problem.",
     "Explain what the tessellation stages do and when they are worth it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Meshes",
   "blurb": "Triangles are the output format. They are rarely the authoring "
            "format."},

  {"t": "table", "kicker": "Representations", "title": "Mesh data structures",
   "header": ["Structure", "Stores", "Fast at", "Weak at"],
   "widths": [2.7, 3.4, 3.1, 2.9],
   "rows": [
     ["Triangle soup", "Three vertices per triangle", "Rendering, nothing else", "Any adjacency query"],
     ["Indexed mesh", "Vertex array + index array", "Rendering, vertex reuse", "Adjacency; neighbours"],
     ["Half-edge", "Directed edge pairs with links", "All adjacency, in O(1)", "Memory; non-manifold meshes"],
     ["Winged-edge", "Edges with four neighbours", "Adjacency", "Fiddlier than half-edge"],
   ],
   "note": "Indexed is what you render. Half-edge is what you edit. Most "
           "pipelines convert between them, which is itself a design "
           "decision."},

  {"t": "bullets", "kicker": "Half-edge", "title": "Why half-edge is the editing structure",
   "items": [
     "Each edge is split into two directed half-edges, one per adjacent face.",
     "Each half-edge knows: its twin, its next, its origin vertex, its face.",
     "",
     "That is enough for every adjacency query in constant time:",
     ("All faces around a vertex — walk twin/next.", 1),
     ("All edges of a face — follow next until you return.", 1),
     ("The neighbour across an edge — follow twin.", 1),
     "",
     "Required for: simplification, subdivision, smoothing, remeshing, UV "
     "unwrapping.",
     ("Assumes a <b>manifold</b> mesh. Real assets often are not, and "
      "handling that is most of the engineering.", 1),
   ],
   "note": "Non-manifold handling is where mesh libraries get hard. Worth "
           "saying out loud so they are not surprised in CSCE 645."},

  {"t": "section", "label": "Part 2", "title": "Curves and surfaces",
   "blurb": "Smooth by construction rather than by having enough triangles."},

  {"t": "eq", "kicker": "Bezier", "title": "Bezier curves",
   "eqs": [
     ("B(t)  =  Σ C(n,i) tⁱ (1−t)ⁿ⁻ⁱ Pᵢ",
      "A weighted average of control points; the weights are Bernstein "
      "polynomials."),
     ("de Casteljau: repeated linear interpolation",
      "Numerically stable, geometrically meaningful, and trivially "
      "subdivides the curve."),
     ("B(0) = P₀,   B(1) = Pₙ",
      "Interpolates the endpoints only. Interior control points pull without "
      "being touched."),
   ],
   "caption": "The curve lies inside the convex hull of its control points "
              "— which is what makes conservative culling of curved "
              "geometry possible.",
   "note": "de Casteljau is worth implementing: it makes the convex hull "
           "property and the subdivision property both obvious."},

  {"t": "two", "kicker": "Compare", "title": "Bezier and B-spline",
   "lh": "Bezier",
   "l": ["Degree tied to control point count.",
         "Moving one point changes the <b>whole</b> curve.",
         "Interpolates the endpoints.",
         ("Joining segments smoothly requires manual constraints.", 1),
         ("Right for short, independently controlled segments.", 1)],
   "rh": "B-spline",
   "r": ["Degree independent of control point count.",
         "<b>Local control</b> — a point affects only nearby spans.",
         "Does not generally interpolate control points.",
         ("Cⁿ⁻¹ continuity automatically at the joins.", 1),
         ("Right for long curves. NURBS adds weights, and exact conics.", 1)],
   "note": "Local control is the decisive practical difference and the reason "
           "CAD uses NURBS rather than Bezier patches."},

  {"t": "bullets", "kicker": "Continuity", "title": "Two kinds of smoothness",
   "items": [
     "<b>Cⁿ</b> — parametric continuity: derivatives match as "
     "functions of t.",
     "<b>Gⁿ</b> — geometric continuity: the shape is smooth, "
     "direction matches, speed need not.",
     "",
     "G¹ is what the eye sees. C¹ is what the mathematics gives you.",
     ("A curve can be G¹ but not C¹ — smooth to look at, "
      "with a speed discontinuity.", 1),
     ("That matters for camera paths and animation, where speed is "
      "visible.", 1),
     "",
     "<b>C²</b> matters for reflections: highlights reveal curvature "
     "discontinuities the silhouette hides.",
   ]},

  {"t": "bullets", "kicker": "Subdivision", "title": "Subdivision surfaces",
   "items": [
     "Start with a coarse control cage. Refine it by a fixed rule. Repeat.",
     "In the limit, a smooth surface — and the limit is reached quickly "
     "enough to be practical.",
     "",
     "<b>Catmull–Clark</b> — quads, C² except at extraordinary "
     "vertices. The film and games standard.",
     "<b>Loop</b> — triangles, C² except at extraordinary vertices.",
     "",
     "Advantages over patches: arbitrary topology, no trimming, one "
     "representation for all LODs.",
     ("Catmull–Clark on a regular quad mesh is exactly a uniform bicubic "
      "B-spline. It is a generalisation, not an alternative.", 1),
   ],
   "note": "That last point surprises people and is worth stating: "
           "subdivision did not replace splines, it extended them to "
           "arbitrary topology."},

  {"t": "section", "label": "Part 3", "title": "Level of detail",
   "blurb": "Spending triangles where they are visible."},

  {"t": "bullets", "kicker": "LOD", "title": "Strategies and their costs",
   "items": [
     "<b>Discrete LOD</b> — several prebuilt versions, switch by "
     "distance. Simple; <b>pops</b> at the switch.",
     ("Cross-fade or dither between levels to hide it.", 1),
     "",
     "<b>Continuous LOD</b> — progressive meshes; add or remove one edge "
     "collapse at a time. No popping; more complex.",
     "",
     "<b>Virtualised geometry</b> — cluster-based, selected per cluster "
     "per frame. Essentially eliminates both popping and authoring effort, at "
     "the cost of a large runtime system.",
     "",
     "<b>Impostors</b> — replace distant geometry with a billboard. "
     "Cheapest; breaks under parallax.",
   ]},

  {"t": "bullets", "kicker": "Simplification", "title": "Edge collapse and quadric error",
   "items": [
     "The standard simplification primitive: collapse an edge, merging two "
     "vertices into one.",
     "Choose which edge by a cost metric and collapse the cheapest "
     "repeatedly.",
     "",
     "<b>Quadric error metric</b> (Garland–Heckbert): cost = sum of "
     "squared distances to the planes of the original faces.",
     ("Representable as a 4×4 matrix per vertex, and matrices add.", 1),
     ("So the cost of a collapse is computable in constant time.", 1),
     "",
     "Preserves silhouettes well, because silhouette edges have high error.",
     ("Needs extra care for UV seams and normals — collapsing across a "
      "seam destroys the UV layout.", 1),
   ]},

  {"t": "section", "label": "Part 4", "title": "Tessellation on the GPU",
   "blurb": "Generating geometry during the frame."},

  {"t": "table", "kicker": "Stages", "title": "The tessellation stages",
   "header": ["Stage", "Runs per", "Produces"],
   "widths": [3.6, 3.5, 5.0],
   "rows": [
     ["Tessellation control", "Patch", "Per-edge and inner tessellation factors"],
     ["Tessellator", "Patch (fixed-function)", "A grid of barycentric coordinates"],
     ["Tessellation evaluation", "Generated vertex", "The actual vertex position"],
   ],
   "note": "The control shader is where adaptive LOD logic lives: factors can "
           "depend on screen-space edge length, curvature, or silhouette."},

  {"t": "bullets", "kicker": "Judgement", "title": "When tessellation pays, and when it does not",
   "items": [
     "<b>Pays:</b> terrain with a heightmap — huge detail from little "
     "memory, adaptive to distance.",
     "<b>Pays:</b> smooth silhouettes on curved surfaces that normal maps "
     "cannot fix.",
     "<b>Pays:</b> displacement where the silhouette genuinely matters.",
     "",
     "<b>Does not pay:</b> anything producing sub-pixel triangles.",
     ("Module 07: 2×2 quad shading means a one-pixel triangle wastes "
      "75% of its work.", 1),
     ("Over-tessellation is a common and expensive mistake.", 1),
     "",
     "Rule: aim for triangles of roughly 8–16 pixels, not 1.",
   ],
   "footnote": "Mesh shaders are increasingly replacing this pipeline, with "
               "the same arithmetic about triangle size still applying."},
 ],
 "takeaways": [
   "Indexed meshes are for rendering; half-edge is for editing. The "
   "conversion between them is a real design decision.",
   "Bezier curves are weighted averages of control points, lie in their "
   "convex hull, and have global control. B-splines add local control, which "
   "is why CAD uses them.",
   "Cⁿ is parametric continuity, Gⁿ is geometric. The eye sees G, "
   "animation speed depends on C, and reflections expose C².",
   "Catmull–Clark subdivision on a regular quad mesh is exactly a "
   "bicubic B-spline — it generalises splines to arbitrary topology.",
   "Quadric error metrics make edge-collapse simplification tractable because "
   "the error matrices simply add.",
   "Tessellation pays for terrain and silhouettes, and loses badly the moment "
   "triangles go sub-pixel.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Mesh representations"),
  ("p", "Triangles are what the rasterizer consumes, but they are a poor "
        "structure for almost everything else you might want to do with a "
        "surface. The representation you choose determines which operations "
        "are cheap."),
  ("table", ["Structure", "Contents", "O(1) queries", "Use"],
   [["Triangle soup", "9 floats per triangle, no sharing", "None",
     "Legacy formats. Avoid: no vertex reuse, no adjacency."],
    ["Indexed mesh", "Vertex array plus index array",
     "Vertex lookup",
     "The rendering format. Vertices are shared, so the post-transform cache "
     "works."],
    ["Half-edge", "Two directed half-edges per edge, with twin/next/vertex/"
     "face links", "All adjacency queries",
     "The editing format: simplification, subdivision, smoothing, "
     "parameterisation."]],
   [0.17, 0.33, 0.18, 0.32]),
  ("h2", "1.1 &nbsp; Half-edge"),
  ("p", "Each undirected edge is represented as two directed half-edges "
        "pointing in opposite directions, one belonging to each adjacent "
        "face. A half-edge stores its twin, the next half-edge around its "
        "face, its origin vertex, and its face. Four pointers, and every "
        "adjacency question becomes a constant-time walk:"),
  ("ul", ["<b>Faces around a vertex:</b> alternate <code>twin</code> and "
          "<code>next</code> until you return to the start.",
          "<b>Edges of a face:</b> follow <code>next</code> until you cycle.",
          "<b>The face across an edge:</b> <code>twin.face</code>.",
          "<b>Vertex valence:</b> count the one-ring walk."]),
  ("callout", "The manifold assumption",
   ["Half-edge assumes the mesh is <b>manifold</b>: every edge has exactly "
    "two adjacent faces (or one, at a boundary), and the faces around every "
    "vertex form a single fan.",
    "Real production assets violate this constantly — T-junctions, "
    "duplicated vertices, edges shared by three faces, isolated vertices. "
    "Handling or repairing non-manifold input is where most of the "
    "engineering in a mesh library actually goes. CSCE 645 treats this "
    "properly."]),

  ("h1", "2 &nbsp; Curves"),
  ("h2", "2.1 &nbsp; Bezier"),
  ("eq", "B(t) = &Sigma;&#7522; C(n,i) t<super>i</super> (1&minus;t)<super>n&minus;i</super> P&#7522;"),
  ("p", "A B&eacute;zier curve is a weighted average of its control points, "
        "with Bernstein polynomials as the weights. Because the weights are "
        "non-negative and sum to one at every t, the curve lies entirely "
        "within the <b>convex hull</b> of its control points — which is "
        "what makes conservative bounding and culling of curved geometry "
        "possible without evaluating the curve."),
  ("p", "The <b>de Casteljau algorithm</b> evaluates the curve by repeated "
        "linear interpolation: interpolate between adjacent control points at "
        "parameter t, then between the results, and so on until one point "
        "remains. It is numerically stable, geometrically transparent, and it "
        "produces the two control polygons that split the curve at t as a "
        "by-product — which is how curves are adaptively subdivided for "
        "rendering."),
  ("p", "The weakness is global control: every control point's weight is "
        "non-zero over the entire parameter range, so moving any one of them "
        "alters the whole curve. Raising the degree to add control points "
        "makes this worse."),
  ("h2", "2.2 &nbsp; B-splines and NURBS"),
  ("p", "B-splines decouple degree from control point count by giving each "
        "control point a basis function with <b>local support</b> — "
        "non-zero only over a few spans. Moving a control point therefore "
        "changes only the nearby curve, which is what makes long splines "
        "editable. Continuity at the joins between spans is automatic: a "
        "degree-n B-spline is C&#8319;&#8315;&#185; by construction, with no "
        "constraints for the user to maintain."),
  ("p", "NURBS add a weight per control point, making the curve a <i>rational</i> "
        "function. The payoff is exact representation of conic sections "
        "— circles, ellipses, cylinders — which polynomial splines "
        "cannot represent at all. That is why NURBS, not B&eacute;zier "
        "patches, are the foundation of CAD."),
  ("h2", "2.3 &nbsp; Continuity"),
  ("table", ["Type", "Condition", "What it governs"],
   [["C&#8304; / G&#8304;", "Positions match", "No visible gap."],
    ["C&#185;", "First derivatives match as functions of t",
     "Smooth <i>and</i> constant speed. Matters for anything travelling along "
     "the curve: cameras, animation timing."],
    ["G&#185;", "Tangent <i>directions</i> match; magnitudes need not",
     "Looks smooth. This is what the eye judges. A curve can be G&#185; "
     "without being C&#185;, which looks fine but animates with a visible "
     "speed jolt."],
    ["C&#178; / G&#178;", "Curvature matches",
     "Reflections and specular highlights. A G&#185;-but-not-G&#178; join is "
     "invisible in silhouette and shows as a crease in a reflection, which is "
     "why car body surfacing demands G&#178;."]],
   [0.13, 0.33, 0.54]),

  ("break",),
  ("h1", "3 &nbsp; Subdivision surfaces"),
  ("p", "Rather than defining a surface by a parametric formula, define it as "
        "the limit of repeatedly refining a coarse control mesh by a fixed "
        "rule. Each step inserts new vertices and repositions existing ones; "
        "in the limit the result is a smooth surface, and in practice two or "
        "three steps are visually indistinguishable from the limit."),
  ("table", ["Scheme", "Base mesh", "Continuity", "Used by"],
   [["Catmull&ndash;Clark", "Quads (any polygons)",
     "C&#178; except at extraordinary vertices, where C&#185;",
     "Film and games. The dominant scheme."],
    ["Loop", "Triangles",
     "C&#178; except at extraordinary vertices",
     "Triangle-based pipelines."],
    ["Doo&ndash;Sabin", "Any", "C&#185;", "Less common."]],
   [0.20, 0.20, 0.33, 0.27]),
  ("callout", "Subdivision generalises splines",
   ["Catmull&ndash;Clark applied to a <i>regular</i> quad mesh — every "
    "vertex of valence 4 — produces exactly a uniform bicubic B-spline "
    "surface.",
    "So subdivision did not replace spline patches; it extended them to "
    "arbitrary topology. The special behaviour at extraordinary vertices "
    "(valence &ne; 4) is precisely the price of that generality, and it is "
    "why modellers are taught to keep quad topology regular where curvature "
    "matters."]),
  ("p", "Practical advantages over patch-based modelling: arbitrary topology "
        "with no trimming, a single representation that yields every level of "
        "detail, and a control cage that is itself an editable mesh. This is "
        "why it became the standard authoring representation for organic "
        "models."),

  ("h1", "4 &nbsp; Level of detail"),
  ("p", "A model covering nine pixels should not cost fifty thousand "
        "triangles. Module 07 gives the sharper version of this: because "
        "fragments shade in 2&times;2 quads, triangles smaller than a few "
        "pixels waste most of their shading work on helper lanes. Dense "
        "geometry is not merely wasteful, it is <i>disproportionately</i> "
        "wasteful."),
  ("table", ["Strategy", "Mechanism", "Cost"],
   [["Discrete LOD", "Prebuilt variants, switched by screen-space size.",
     "Simple and predictable. <b>Pops</b> visibly at the switch; needs "
     "cross-fading or dithering to hide."],
    ["Continuous LOD", "Progressive mesh: one edge collapse at a time.",
     "No popping, smooth transitions. Complex runtime, awkward on the GPU."],
    ["Virtualised geometry", "Clusters selected per-cluster per-frame.",
     "Effectively removes popping and LOD authoring entirely. Large runtime "
     "system; this is what Nanite-style renderers do."],
    ["Impostors", "Replace distant geometry with a textured billboard.",
     "Cheapest by far. Breaks under parallax and at close range; good for "
     "distant forests and crowds."]],
   [0.20, 0.34, 0.46]),
  ("h2", "4.1 &nbsp; Quadric error simplification"),
  ("p", "The standard automatic simplification algorithm collapses edges one "
        "at a time, cheapest first. The question is how to price a collapse."),
  ("p", "Garland and Heckbert's <b>quadric error metric</b> assigns each "
        "vertex a 4&times;4 matrix representing the sum of squared distances "
        "to the planes of its incident faces. The error of placing a merged "
        "vertex at position <b>v</b> is then v&#7488;Qv, and — this is "
        "the key property — the quadric of a merged vertex is simply the "
        "<i>sum</i> of the two original quadrics. Collapse costs are "
        "therefore computable in constant time, and the whole simplification "
        "runs in O(n log n) with a priority queue."),
  ("p", "The metric preserves silhouettes well, because collapsing an edge on "
        "a sharp silhouette incurs large distances to the original planes. It "
        "needs explicit extra handling for attribute discontinuities: "
        "collapsing across a UV seam or a normal split destroys the texture "
        "layout, so those edges must be weighted heavily or forbidden."),

  ("h1", "5 &nbsp; GPU tessellation"),
  ("table", ["Stage", "Invocation", "Responsibility"],
   [["Tessellation control (hull)", "Once per patch",
     "Decide the tessellation factors: how finely to subdivide each edge and "
     "the interior. This is where adaptive LOD logic lives."],
    ["Tessellator", "Fixed-function, per patch",
     "Generate a grid of barycentric or UV coordinates at the requested "
     "density. Not programmable."],
    ["Tessellation evaluation (domain)", "Once per generated vertex",
     "Compute the actual position: evaluate the patch, sample a displacement "
     "map, apply the surface definition."]],
   [0.26, 0.21, 0.53]),
  ("p", "Factors can be driven by screen-space edge length, by distance, by "
        "local curvature, or by whether an edge lies on the silhouette "
        "— silhouette-adaptive tessellation gives most of the visual "
        "benefit for a fraction of the triangles, since interior smoothness "
        "is already handled by normal mapping."),
  ("callout", "The failure mode",
   ["Over-tessellation is one of the most common and most expensive mistakes "
    "in real pipelines. Once triangles approach one pixel, quad overshading "
    "means up to 75% of fragment-shader work is discarded, and vertex cost "
    "has risen to match.",
    "Target triangles of roughly 8&ndash;16 pixels. More than that wastes "
    "detail; fewer wastes the machine. Measure, do not assume.",
    "Mesh shaders increasingly replace this fixed pipeline with a more "
    "flexible compute-like model, but the arithmetic about triangle size is "
    "unchanged."]),
 ],
 "resources": [
   ("Keenan Crane — Discrete Differential Geometry (free notes, video, "
    "code)",
    "https://brickisland.net/ddg-web/",
    "The proper treatment of mesh processing and geometry. This is the "
    "primary text for CSCE 645; start it here."),
   ("GAMES101 Lectures 11–12 — Geometry",
    "https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html",
    "Curves, surfaces, subdivision, and simplification at the right level for "
    "this module."),
   ("libigl tutorial (free)",
    "https://libigl.github.io/tutorial/",
    "Working code for half-edge traversal, simplification, smoothing, and "
    "parameterisation. Read the source."),
   ("Garland & Heckbert — 'Surface Simplification Using Quadric Error "
    "Metrics' (free)",
    "https://www.cs.cmu.edu/~garland/Papers/quadrics.pdf",
    "The original paper. Short, clear, and still the basis of every "
    "production simplifier."),
   ("Brian Karis — 'Nanite: A Deep Dive' (SIGGRAPH, free)",
    "https://advances.realtimerendering.com/s2021/",
    "How virtualised geometry actually works. Read after the rest of this "
    "module."),
 ],
 "exercises": [
   "Implement a half-edge mesh from an indexed triangle mesh. Write and test "
   "the one-ring traversal: all faces around a vertex, all neighbours of a "
   "vertex, the face across an edge.",
   "Implement de Casteljau evaluation for a cubic B&eacute;zier curve, and "
   "use it to subdivide the curve at an arbitrary t. Verify that the two "
   "halves reproduce the original.",
   "Construct two cubic B&eacute;zier segments joined G&#185; but not "
   "C&#185;. Animate a point travelling along the pair at constant parameter "
   "speed and observe the velocity discontinuity.",
   "Implement one step of Catmull&ndash;Clark subdivision. Apply it to a cube "
   "three times and confirm convergence toward a smooth shape. Identify the "
   "extraordinary vertices.",
   "Implement quadric error simplification. Reduce a 50,000-triangle mesh to "
   "5,000 and 500 triangles and capture all three. Note where the silhouette "
   "first fails.",
   "Implement GPU tessellation on a displaced terrain patch with "
   "distance-based factors. Measure frame time against tessellation factor "
   "and find the point where triangles go sub-pixel and performance collapses.",
 ],
 "selfcheck": [
   "What adjacency queries does a half-edge structure make O(1), and what "
   "assumption does it require that real assets frequently violate?",
   "Why does a B&eacute;zier curve lie within the convex hull of its control "
   "points, and what practical use does that property have?",
   "Give the decisive practical difference between B&eacute;zier and "
   "B-spline curves, and say why CAD uses NURBS.",
   "Distinguish C&#185; from G&#185; continuity, and give a situation where "
   "the difference is visible.",
   "What is the relationship between Catmull&ndash;Clark subdivision and "
   "bicubic B-spline surfaces?",
   "Why does the quadric error metric make edge-collapse simplification "
   "efficient?",
   "When does GPU tessellation stop paying for itself, and why specifically?",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Animation: Hierarchies, Skinning, and Interpolation",
 "subtitle": "Making it move, and the mathematics of interpolating rotations.",
 "question": "How do you deform a mesh smoothly with a skeleton?",
 "outcomes": [
     "Build a transform hierarchy and compute world transforms correctly.",
     "Explain why Euler angles and matrices both interpolate badly.",
     "Use quaternions and slerp for rotation interpolation.",
     "Implement linear blend skinning and explain the candy-wrapper artifact.",
     "Describe the animation pipeline from clip to final vertex.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Hierarchies",
   "blurb": "A skeleton is a tree of transforms. Nothing more."},

  {"t": "bullets", "kicker": "Hierarchy", "title": "Local and world transforms",
   "items": [
     "Each joint stores its transform <b>relative to its parent</b>.",
     ("Rotating a shoulder moves the whole arm for free — that is the "
      "entire reason for the structure.", 1),
     "",
     "World transform = parent's world transform × own local transform.",
     ("Computed by one depth-first traversal per frame.", 1),
     ("Parents must be processed before children, so store joints in "
      "topological order and the traversal becomes a flat loop.", 1),
     "",
     "Order matters, exactly as in Module 03. Parent first, then child.",
   ]},

  {"t": "eq", "kicker": "Skinning", "title": "The bind pose and why it is inverted",
   "eqs": [
     ("M_skin  =  W_current · (W_bind)⁻¹",
      "Undo the bind pose, then apply the current pose."),
     ("(W_bind)⁻¹  —  the inverse bind matrix",
      "Precomputed once per joint and stored with the mesh."),
     ("v' = M_skin · v",
      "Vertices are authored in bind pose, so they must be un-posed first."),
   ],
   "caption": "The inverse bind matrix is the step people forget. Without it "
              "the mesh explodes the moment any joint is not at the origin.",
   "note": "Worth showing the broken result once — it is memorable and "
           "instantly diagnostic."},

  {"t": "section", "label": "Part 2", "title": "Interpolating rotations",
   "blurb": "Translation and scale interpolate trivially. Rotation does not."},

  {"t": "table", "kicker": "Representations", "title": "Four ways to store a rotation",
   "header": ["Representation", "Size", "Interpolates", "Problem"],
   "widths": [3.0, 1.6, 2.9, 4.6],
   "rows": [
     ["Euler angles", "3", "Badly", "Gimbal lock; order-dependent; non-unique"],
     ["Rotation matrix", "9", "Badly", "Lerping leaves the rotation group — shears and scales"],
     ["Axis–angle", "4", "Partially", "No clean composition rule"],
     ["Quaternion", "4", "<b>Correctly</b>", "Double cover: q and −q are the same rotation"],
   ],
   "note": "The matrix row surprises people: the set of rotation matrices is "
           "not convex, so the average of two rotations is not a rotation."},

  {"t": "callout", "title": "Gimbal lock", "kind": "Why not Euler angles",
   "body": ["Three sequential axis rotations. When the middle rotation "
            "reaches 90°, the first and third axes align — and one "
            "degree of freedom is lost.",
            "No amount of changing the first and third angles can produce "
            "rotation about the missing axis. The parameterisation has "
            "collapsed, not the rotation.",
            "This is not an implementation flaw; it is a topological fact "
            "about mapping three angles onto the rotation group. Any "
            "three-parameter representation has it somewhere.",
            "It is also why Euler angles remain fine as an <i>authoring</i> "
            "interface and unacceptable as an <i>interpolation</i> "
            "representation."]},

  {"t": "bullets", "kicker": "Quaternions", "title": "Why quaternions work",
   "items": [
     "A unit quaternion is a point on the 4D unit sphere; rotations are "
     "points on that sphere.",
     "Interpolating along the sphere's surface stays on the sphere — so "
     "every intermediate value is a valid rotation.",
     "",
     "<b>slerp</b> — spherical linear interpolation — moves at "
     "constant angular velocity along the shortest arc.",
     "",
     "<b>The sign trap:</b> q and −q represent the <i>same</i> rotation.",
     ("If the dot product of the two quaternions is negative, negate one "
      "before interpolating.", 1),
     ("Otherwise you take the long way round — up to 358° instead "
      "of 2°. Spectacular, and the most common quaternion bug.", 1),
   ],
   "note": "Everyone hits the sign bug once. Showing it here saves them the "
           "afternoon."},

  {"t": "code", "kicker": "Quaternions", "title": "slerp, with the sign fix",
   "lang": "cpp", "code": """
quat slerp(quat a, quat b, float t) {
    float d = dot(a, b);

    // q and -q are the same rotation. Without this you may take
    // the 358-degree path instead of the 2-degree one.
    if (d < 0.0f) { b = -b; d = -d; }

    // Nearly parallel: slerp is numerically unstable, lerp is fine.
    if (d > 0.9995f) return normalize(a + t * (b - a));

    float theta = acosf(d);
    float s     = sinf(theta);
    return (sinf((1 - t) * theta) * a + sinf(t * theta) * b) / s;
}
""",
   "caption": "Three lines of actual interpolation and two guards. Both "
              "guards are necessary — the second prevents a division by "
              "a vanishing sine.",
   "note": "Note that nlerp (normalized lerp) is often used instead: cheaper, "
           "not constant-velocity, and usually indistinguishable between "
           "adjacent keyframes."},

  {"t": "section", "label": "Part 3", "title": "Skinning",
   "blurb": "Each vertex follows several joints at once."},

  {"t": "eq", "kicker": "LBS", "title": "Linear blend skinning",
   "eqs": [
     ("v'  =  Σ wᵢ · Mᵢ · v",
      "Weighted sum of the vertex transformed by each influencing joint."),
     ("Σ wᵢ  =  1",
      "Weights must be normalised or the mesh changes size."),
     ("typically 4 influences per vertex",
      "Fits neatly in a vec4 of weights and a uvec4 of indices."),
   ],
   "caption": "Simple, fast, GPU-friendly, and wrong in a specific way that "
              "the next slide names.",
   "note": "Note that the per-vertex data layout is itself the reason 4 "
           "influences became standard."},

  {"t": "callout", "title": "The candy-wrapper artifact", "kind": "Why LBS is wrong",
   "body": ["Averaging <i>transformation matrices</i> is not the same as "
            "averaging <i>transformations</i>.",
            "The midpoint of two rotation matrices 180° apart is not a "
            "rotation — it is a degenerate matrix that collapses the "
            "space. So a wrist twisted 180° pinches to nothing, like the "
            "twist in a sweet wrapper.",
            "Mitigations: add more joints so no single joint twists far; "
            "paint weights carefully; or switch to dual-quaternion skinning, "
            "which interpolates the <i>transformations</i> rather than their "
            "matrices and preserves volume at the cost of a slight bulge."]},

  {"t": "code", "kicker": "Skinning", "title": "Skinning in the vertex shader",
   "lang": "glsl", "code": """
layout(location=0) in vec3  aPos;
layout(location=1) in vec3  aNormal;
layout(location=5) in uvec4 aJoints;    // 4 joint indices
layout(location=6) in vec4  aWeights;   // 4 weights, summing to 1

layout(std430) buffer Skin { mat4 uSkin[]; };   // world * inverseBind

void main() {
    mat4 S = aWeights.x * uSkin[aJoints.x]
           + aWeights.y * uSkin[aJoints.y]
           + aWeights.z * uSkin[aJoints.z]
           + aWeights.w * uSkin[aJoints.w];

    vec3 pos = (S * vec4(aPos, 1.0)).xyz;
    vec3 nrm = mat3(S) * aNormal;        // w=0: Module 02, no translation

    gl_Position = uViewProj * vec4(pos, 1.0);
    vNormal     = normalize(nrm);
}
""",
   "caption": "Blend the matrices first, then transform once — not four "
              "transforms averaged. Same result, a quarter of the work.",
   "note": "Tie back to Module 02: normals use mat3 so translation does not "
           "reach them. And to Module 08: this is why normal maps must be "
           "tangent-space, since the tangent frame deforms too."},

  {"t": "bullets", "kicker": "Pipeline", "title": "From clip to pixel",
   "items": [
     "<b>1. Sample</b> the animation clip at the current time — "
     "translation, rotation, scale per joint.",
     ("Interpolate between keyframes: lerp position and scale, slerp "
      "rotation.", 1),
     "<b>2. Blend</b> between clips (walk→run) or layer them (aim over "
     "walk).",
     "<b>3. Apply</b> inverse kinematics corrections — foot placement, "
     "look-at.",
     "<b>4. Traverse</b> the hierarchy to world transforms.",
     "<b>5. Multiply</b> by inverse bind matrices to get skinning matrices.",
     "<b>6. Upload</b> the palette and skin in the vertex shader.",
   ],
   "footnote": "Steps 1–5 are CPU and cheap. Step 6 is GPU and scales "
               "with vertex count."},

  {"t": "bullets", "kicker": "End", "title": "Where this leaves you",
   "items": [
     "You have built a renderer twice: once in software, once on the GPU.",
     "You can transform, rasterize, shade physically, shadow, antialias, "
     "texture, and animate.",
     "",
     "<b>CSCE 647</b> replaces the rasterizer with real light transport.",
     "<b>CSCE 645</b> goes deeper into the geometry you have only sampled "
     "here.",
     "<b>CSCE 649</b> makes the motion physical rather than keyframed.",
     "<b>CSCE 735</b> explains the machine underneath all of it.",
     "",
     "Build the capstone on this codebase. It is the artifact.",
   ]},
 ],
 "takeaways": [
   "A skeleton is a tree of local transforms; world transforms come from one "
   "ordered traversal per frame.",
   "The inverse bind matrix un-poses vertices before the current pose is "
   "applied. Forget it and the mesh explodes.",
   "Euler angles suffer gimbal lock; rotation matrices do not interpolate "
   "because the rotation group is not convex.",
   "Unit quaternions interpolate correctly via slerp — but q and "
   "−q are the same rotation, so check the dot product sign.",
   "Linear blend skinning averages matrices, not transformations, which "
   "collapses the mesh under large twists: the candy-wrapper artifact.",
   "Dual-quaternion skinning interpolates transformations instead, fixing the "
   "collapse at the cost of a bulge.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Transform hierarchies"),
  ("p", "A skeleton is a tree in which each joint stores its transform "
        "relative to its parent. The reason is immediate: rotating a shoulder "
        "should carry the elbow, wrist, and fingers with it, and expressing "
        "each joint locally makes that automatic rather than something the "
        "animator has to maintain."),
  ("eq", "W<sub>joint</sub> = W<sub>parent</sub> &times; L<sub>joint</sub>"),
  ("p", "World transforms are computed by a depth-first traversal, parents "
        "before children. If joints are stored in topological order — "
        "which exporters generally guarantee — the traversal degenerates "
        "into a flat loop over an array, which is both simpler and far more "
        "cache-friendly than following pointers."),
  ("h2", "1.1 &nbsp; The bind pose"),
  ("p", "Mesh vertices are authored in a specific rest configuration: the "
        "<b>bind pose</b>, usually a T-pose or A-pose. The skeleton has a "
        "matching set of world transforms in that pose. To animate a vertex, "
        "you must first undo the bind pose and then apply the current pose:"),
  ("eq", "M<sub>skin</sub> = W<sub>current</sub> &middot; W<sub>bind</sub><super>&minus;1</super>"),
  ("callout", "The inverse bind matrix",
   ["W<sub>bind</sub><super>&minus;1</super> is precomputed once per "
    "joint and shipped with the mesh. It is the step most often omitted by "
    "people writing their first skinning implementation.",
    "The symptom is unmistakable: the mesh explodes into scattered fragments "
    "the instant any joint is not at the origin, because every vertex is "
    "being transformed as though it were authored at the world origin.",
    "If you see that, this is the cause. It is worth producing the broken "
    "result once deliberately."]),

  ("h1", "2 &nbsp; Interpolating rotations"),
  ("p", "Animation is interpolation between keyframes. Position and scale "
        "interpolate linearly without difficulty. Rotation is the hard case, "
        "and the difficulty is intrinsic rather than an artifact of any "
        "particular representation."),
  ("h2", "2.1 &nbsp; Euler angles and gimbal lock"),
  ("p", "Three sequential rotations about three axes. Compact, intuitive to "
        "author, and degenerate. When the middle rotation reaches 90&deg;, "
        "the first and third rotation axes become parallel: two of the three "
        "parameters now do the same thing, and one rotational degree of "
        "freedom cannot be expressed at all."),
  ("p", "This is a topological fact, not a bug. There is no way to cover the "
        "rotation group smoothly with three parameters, so every "
        "three-parameter representation has a degeneracy somewhere. Euler "
        "angles remain a perfectly good <i>authoring</i> interface — "
        "artists think in pitch, yaw, and roll — and an unacceptable "
        "<i>interpolation</i> representation. Interpolating Euler angles also "
        "produces paths that depend on the chosen axis order and that are not "
        "shortest-arc."),
  ("h2", "2.2 &nbsp; Why matrices do not interpolate either"),
  ("p", "A less familiar problem: linearly interpolating two rotation "
        "matrices element-wise does not give a rotation matrix. The set of "
        "rotation matrices is a curved manifold embedded in the space of all "
        "3&times;3 matrices, and it is not convex — the straight line "
        "between two points on it leaves it. Intermediate values therefore "
        "include shear and non-uniform scale, and at 180&deg; apart the "
        "midpoint is degenerate. This is the same fact that will cause the "
        "candy-wrapper artifact in &sect;3."),
  ("h2", "2.3 &nbsp; Quaternions"),
  ("p", "A unit quaternion is a point on the unit 3-sphere in four "
        "dimensions, and unit quaternions correspond to rotations. "
        "Interpolating <i>along the surface of the sphere</i> stays on the "
        "sphere, so every intermediate value is a valid rotation. <b>Slerp</b> "
        "traverses the shortest great-circle arc at constant angular "
        "velocity, which is exactly what rotational interpolation should mean."),
  ("code", """quat slerp(quat a, quat b, float t) {
    float d = dot(a, b);

    // THE classic quaternion bug: q and -q are the same rotation, so a
    // negative dot product means the shortest path is toward -b. Without
    // this you can interpolate 358 degrees instead of 2.
    if (d < 0.0f) { b = -b; d = -d; }

    // Nearly parallel: sin(theta) -> 0 and the formula is unstable.
    // Plain lerp is indistinguishable here.
    if (d > 0.9995f) return normalize(a + t * (b - a));

    float theta = acosf(d);
    return (sinf((1-t)*theta)*a + sinf(t*theta)*b) / sinf(theta);
}"""),
  ("callout", "Double cover",
   ["Every rotation corresponds to <i>two</i> quaternions, q and &minus;q. "
    "The quaternion sphere covers the rotation group twice.",
    "Practically this means a sign check before every interpolation. Omit it "
    "and a character's arm occasionally swings the wrong way round the entire "
    "circle between two nearly identical keyframes. It is dramatic, "
    "intermittent, and confusing until you know the cause — which is why "
    "it is worth meeting here rather than in production."]),
  ("p", "<b>nlerp</b> — linear interpolation followed by normalisation "
        "— is a common cheaper alternative. It stays on the sphere and "
        "is commutative, but moves at non-constant angular velocity. Between "
        "adjacent keyframes a few frames apart the difference is invisible, "
        "so many engines use nlerp for skeletal animation and reserve slerp "
        "for large interpolations such as camera moves."),

  ("break",),
  ("h1", "3 &nbsp; Skinning"),
  ("p", "Rigid attachment of each vertex to one joint produces visible cracks "
        "and intersections at every joint. <b>Linear blend skinning</b> lets "
        "each vertex be influenced by several joints with weights that sum to "
        "one."),
  ("eq", "v&prime; = &Sigma;<sub>i</sub> w<sub>i</sub> &middot; M<sub>i</sub> &middot; v, &nbsp;&nbsp; &Sigma;<sub>i</sub> w<sub>i</sub> = 1"),
  ("p", "Four influences per vertex is the near-universal standard, because "
        "four weights fit in a <code>vec4</code> and four indices in a "
        "<code>uvec4</code>, giving a tidy vertex layout. The weights must be "
        "normalised: if they do not sum to one the vertex is scaled toward or "
        "away from the origin, and the mesh visibly inflates or shrinks."),
  ("code", """layout(location=5) in uvec4 aJoints;
layout(location=6) in vec4  aWeights;
layout(std430) buffer Skin { mat4 uSkin[]; };   // world * inverseBind

void main() {
    // Blend the MATRICES, then transform once. Transforming four times
    // and averaging the results gives the same answer for four times
    // the work.
    mat4 S = aWeights.x * uSkin[aJoints.x]
           + aWeights.y * uSkin[aJoints.y]
           + aWeights.z * uSkin[aJoints.z]
           + aWeights.w * uSkin[aJoints.w];

    vec3 pos = (S * vec4(aPos, 1.0)).xyz;
    vec3 nrm = mat3(S) * aNormal;      // mat3: w = 0, Module 02
    gl_Position = uViewProj * vec4(pos, 1.0);
}"""),
  ("h2", "3.1 &nbsp; The candy-wrapper artifact"),
  ("callout", "Averaging matrices is not averaging transformations",
   ["This is &sect;2.2's problem arriving with consequences. The weighted "
    "average of two rotation matrices is not a rotation matrix.",
    "For a 180&deg; twist — a forearm, a wrist — the two joint "
    "matrices are nearly opposite, and their average is close to degenerate. "
    "The affected vertices collapse toward the bone axis, and the limb "
    "pinches to a point exactly like the twist in a sweet wrapper.",
    "The artifact is proportional to the angle between the influencing "
    "joints, which is why it appears on wrists and shoulders and never on "
    "fingers."]),
  ("p", "Three responses, in increasing order of cost:"),
  ("ol", ["<b>Add joints.</b> Twist bones distribute a 180&deg; rotation over "
          "several joints, so no single blend spans a large angle. Cheap, "
          "effective, and the standard production answer.",
          "<b>Paint weights carefully.</b> Reduces but does not remove the "
          "problem, and is labour the rigger would rather spend elsewhere.",
          "<b>Dual-quaternion skinning.</b> Represent each joint transform as "
          "a dual quaternion and interpolate <i>those</i> — interpolating "
          "transformations rather than their matrix representations. The "
          "collapse disappears entirely. The cost is a characteristic slight "
          "bulge at bent joints, and a somewhat more expensive vertex shader. "
          "Many engines offer both and let the rigger choose per mesh."]),
  ("h2", "3.2 &nbsp; Normals and tangents deform too"),
  ("p", "A skinned vertex's normal must be transformed by the same skinning "
        "matrix, using only its upper 3&times;3 part so that translation does "
        "not reach it — Module 02's w = 0 rule. Strictly the inverse "
        "transpose is required, but since skinning matrices are usually "
        "rigid, the 3&times;3 part is correct and the full inverse transpose "
        "per vertex is not worth the cost."),
  ("p", "The tangent frame deforms as well, which is the deeper reason "
        "Module 08 insisted on tangent-space normal maps: an object-space "
        "normal map would be wrong the moment the surface moved, while a "
        "tangent-space map remains correct because the frame it is relative "
        "to deforms with the surface."),

  ("h1", "4 &nbsp; The animation pipeline"),
  ("table", ["Step", "Where", "What happens"],
   [["Sample the clip", "CPU",
     "Find the keyframes bracketing the current time; lerp translation and "
     "scale, slerp or nlerp rotation."],
    ["Blend and layer", "CPU",
     "Blend between clips (walk to run) and layer additively (aim offset over "
     "a locomotion base). This is where a modern animation graph lives."],
    ["Inverse kinematics", "CPU",
     "Correct the result to meet constraints: feet on uneven ground, hands on "
     "a weapon, head tracking a target."],
    ["Hierarchy traversal", "CPU",
     "Compose local transforms into world transforms, parents first."],
    ["Build the palette", "CPU",
     "Multiply each world transform by that joint's inverse bind matrix; "
     "upload the array."],
    ["Skin", "GPU",
     "Blend matrices per vertex and transform position, normal, and tangent."]],
   [0.19, 0.09, 0.72]),
  ("p", "The first five steps cost roughly one hundred joints' worth of "
        "matrix arithmetic per character per frame — negligible. The "
        "last scales with vertex count and runs on the GPU. This is why "
        "animation systems can afford to be sophisticated on the CPU: the "
        "expensive part is elsewhere."),

  ("h1", "5 &nbsp; Where this leaves you"),
  ("p", "You have now built a renderer twice: once in software with nothing "
        "underneath it, and once on the GPU with a programmable pipeline. You "
        "can derive and compose transforms, rasterize with correct fill rules "
        "and perspective-correct interpolation, resolve visibility, shade with "
        "a physically based microfacet model under image-based lighting, cast "
        "and filter shadows, reason about aliasing as a sampling problem, "
        "texture with correct filtering and tangent-space normal maps, "
        "represent and simplify geometry, and animate a skinned character."),
  ("p", "That is the content of a graduate computer graphics course, and more "
        "importantly it is a working codebase. The remaining track courses "
        "each take one layer of it seriously: CSCE 647 replaces the "
        "rasterizer with real light transport; CSCE 645 goes properly into "
        "the geometry; CSCE 649 replaces keyframes with physics; CSCE 650 "
        "addresses the perceptual constraints of stereo and latency; CSCE 735 "
        "explains the machine the whole thing runs on."),
  ("callout", "The capstone",
   ["Build it on this codebase. A renderer you wrote from the triangle up, "
    "extended into a research-scale project, with a written report and a "
    "recorded demonstration, is a more legible credential in this field than "
    "a transcript.",
    "That is not a consolation for the lack of accreditation. In graphics it "
    "is genuinely how people are evaluated."]),
 ],
 "resources": [
   ("GAMES101 Lectures 19–20 — Animation",
    "https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html",
    "Keyframing, rigging, and skinning at the right level, with the "
    "rotation-interpolation problem shown clearly."),
   ("3Blue1Brown & Ben Eater — 'Visualizing quaternions' (interactive)",
    "https://eater.net/quaternions",
    "The best available intuition for why quaternions represent rotations. "
    "Interactive and free."),
   ("Kavan et al. — 'Skinning with Dual Quaternions' (free)",
    "https://www.cs.utah.edu/~ladislav/kavan08geometric/kavan08geometric.pdf",
    "The paper that fixed candy-wrapping, with the derivation and the honest "
    "account of the bulging trade-off."),
   ("glTF 2.0 specification — skins and animations",
    "https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html",
    "The standard runtime format. Reading the skinning section is the fastest "
    "way to see exactly what data a real pipeline ships."),
   ("Jason Gregory — Game Engine Architecture, animation chapter "
    "(sample chapters free)",
    "https://www.gameenginebook.com/",
    "How animation systems are actually structured in production engines."),
 ],
 "exercises": [
   "Implement a transform hierarchy with world-transform computation. Verify "
   "that rotating a parent joint carries all descendants correctly.",
   "Load a skinned glTF model. Implement linear blend skinning in the vertex "
   "shader and play back an animation clip.",
   "Deliberately omit the inverse bind matrix and capture the result. Then "
   "fix it. Write one sentence describing the artifact precisely enough to "
   "recognise it instantly next time.",
   "Implement slerp. Then remove the <code>d &lt; 0</code> sign check and "
   "find two keyframes where the rotation takes the long path. Record both.",
   "Build a wrist twisting through 180&deg; with two joint influences and "
   "capture the candy-wrapper collapse. Then add a twist bone and capture "
   "again.",
   "Compare slerp and nlerp on the same animation. Measure both and determine "
   "experimentally at what angular separation the difference becomes visible.",
   "<b>Course complete.</b> Assemble your portfolio: both projects, every "
   "module's output image, and a README describing what you built and what "
   "was hard.",
 ],
 "selfcheck": [
   "How is a joint's world transform computed, and why must joints be "
   "processed in topological order?",
   "What does the inverse bind matrix do, and what exactly goes wrong without "
   "it?",
   "Explain gimbal lock, and why it is a topological fact rather than an "
   "implementation flaw.",
   "Why does linear interpolation of two rotation matrices not produce a "
   "rotation?",
   "What does slerp do, and what is the double-cover problem? What does the "
   "bug look like?",
   "Explain the candy-wrapper artifact, its cause, and three mitigations with "
   "their trade-offs.",
   "Why does skinning make tangent-space normal maps necessary rather than "
   "merely convenient?",
 ],
},

]
