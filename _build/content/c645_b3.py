# -*- coding: utf-8 -*-
"""CSCE 645 — Modules 09-13."""

MODULES = [

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Parameterization",
 "subtitle": "Flattening a surface, and choosing which distortion to accept.",
 "question": "How do you lay a curved surface flat with the least damage?",
 "outcomes": [
     "Explain why distortion is unavoidable and quantify it.",
     "Distinguish conformal, authalic, and isometric maps.",
     "Implement harmonic and least-squares conformal parameterisation.",
     "Explain cutting, charts, and atlas packing.",
     "Diagnose a bad UV map from its distortion measure.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why it must distort",
   "blurb": "A theorem, not a limitation of current algorithms."},

  {"t": "callout", "title": "Theorema Egregium, applied",
   "kind": "The constraint",
   "body": ["Module 07: Gaussian curvature is <b>intrinsic</b> — "
            "computable from measurements within the surface alone.",
            "A sphere has K = 1/r². A plane has K = 0.",
            "An isometric map — one preserving all distances — "
            "would preserve all intrinsic quantities, including K. So no "
            "isometric map from sphere to plane exists.",
            "<b>This is a theorem.</b> No cleverer algorithm will ever "
            "flatten a sphere without distortion. The only question is which "
            "distortion you accept."]},

  {"t": "table", "kicker": "Map types", "title": "What you can preserve",
   "header": ["Map", "Preserves", "Distorts", "Exists for"],
   "widths": [2.6, 3.0, 3.0, 3.5],
   "rows": [
     ["Isometric", "Lengths (and so everything)", "Nothing", "Developables only"],
     ["Conformal", "<b>Angles</b>", "Area", "Any disc-topology patch"],
     ["Authalic", "<b>Area</b>", "Angles", "Any disc-topology patch"],
     ["Neither", "—", "Both, by less", "Always"],
   ],
   "footnote": "You may preserve angles or area, never both — that would "
               "be an isometry.",
   "note": "The Mercator/Peters map analogy lands immediately: conformal vs "
           "equal-area is the same choice cartographers make."},

  {"t": "callout", "title": "Why texture mapping wants conformal",
   "kind": "The practical choice",
   "body": ["Angle distortion is visible as <b>shearing</b>: a square texture "
            "pattern becomes a parallelogram, and text becomes italic.",
            "Area distortion is visible as <b>varying texel density</b>: some "
            "regions sharper than others.",
            "The eye tolerates the second far better than the first. A "
            "slightly blurrier region is unremarkable; sheared checkerboards "
            "are glaring.",
            "So texture parameterisation is almost always conformal or "
            "near-conformal — and area distortion is then controlled "
            "separately by cutting into charts."]},

  {"t": "section", "label": "Part 2", "title": "Harmonic maps",
   "blurb": "The simplest method, and the Laplacian again."},

  {"t": "eq", "kicker": "Harmonic", "title": "Fix the boundary, solve for the interior",
   "eqs": [
     ("Δu = 0,  Δv = 0   in the interior",
      "The smoothest interpolation of the boundary values."),
     ("(u,v) prescribed on the boundary",
      "Typically mapped to a circle or square."),
     ("⇒ solve Lₓ · u = b   twice",
      "Two sparse solves with the Module 08 matrix. That is the whole "
      "algorithm."),
   ],
   "caption": "Tutte's theorem: if the boundary is mapped to a convex polygon "
              "and all weights are positive, the result is guaranteed "
              "<b>bijective</b> — no triangle flips.",
   "note": "The Tutte guarantee is strong and unusual. Worth flagging, along "
           "with the positive-weights condition it depends on."},

  {"t": "bullets", "kicker": "Harmonic", "title": "Strengths and the catch",
   "items": [
     "<b>Simple:</b> build L, fix the boundary, solve twice. Reuses Module "
     "08 entirely.",
     "<b>Guaranteed bijective</b> with a convex boundary and positive weights "
     "(Tutte).",
     "",
     "<b>The catch:</b> you must fix the boundary, and that choice imposes "
     "distortion.",
     ("Forcing a long thin patch onto a circle stretches it badly.", 1),
     "",
     "<b>And:</b> cotangent weights can be negative on obtuse triangles "
     "(Module 07), which breaks Tutte's guarantee.",
     ("Triangles flip. Use uniform weights for a guarantee, or remesh.", 1),
   ],
   "note": "The negative-weight caveat connects Modules 07, 09, and 10 and is "
           "a real practical trap."},

  {"t": "section", "label": "Part 3", "title": "Free-boundary methods",
   "blurb": "Let the boundary find its own shape."},

  {"t": "bullets", "kicker": "LSCM", "title": "Least-squares conformal maps",
   "items": [
     "Do not fix the boundary. Instead, minimise deviation from "
     "conformality.",
     "",
     "A conformal map satisfies the Cauchy–Riemann equations. Minimise "
     "the squared violation of them.",
     "",
     "Pin only <b>two</b> vertices — enough to fix translation, "
     "rotation, and scale.",
     "",
     "The result: a sparse least-squares system, one solve, and a boundary "
     "that takes its natural shape.",
     ("Far lower distortion than harmonic with a forced boundary.", 1),
     "",
     "The standard method in production UV tools.",
   ],
   "note": "LSCM is what modelling packages actually run. Worth implementing "
           "for Project 2."},

  {"t": "table", "kicker": "Methods", "title": "Parameterisation methods compared",
   "header": ["Method", "Boundary", "Guarantees", "Distortion"],
   "widths": [2.8, 2.8, 3.2, 3.3],
   "rows": [
     ["Harmonic (Tutte)", "Fixed convex", "<b>Bijective</b>", "High if boundary forced"],
     ["LSCM", "Free", "Usually bijective", "<b>Low</b>"],
     ["ABF++", "Free", "Near-conformal", "<b>Very low</b>"],
     ["ARAP", "Free", "—", "Low; balances angle and area"],
     ["BFF", "Free", "Conformal, fast", "<b>Very low</b>"],
   ],
   "note": "BFF (Boundary First Flattening) is Crane's and is both the "
           "fastest and among the best. Worth pointing at."},

  {"t": "section", "label": "Part 4", "title": "Cutting and atlases",
   "blurb": "You cannot flatten a closed surface at all."},

  {"t": "bullets", "kicker": "Cutting", "title": "Every closed surface must be cut",
   "items": [
     "Parameterisation requires <b>disc topology</b>. A sphere and a torus "
     "are not discs.",
     "",
     "So: cut the surface along <b>seams</b> until it becomes one or more "
     "discs.",
     "",
     "Seams are where the texture is discontinuous — visible as a line "
     "if colours do not match across them.",
     "",
     "<b>The trade:</b> more seams → less distortion but more visible "
     "cuts and more wasted atlas space.",
     ("Fewer seams → cleaner appearance, worse distortion.", 1),
   ],
   "note": "This is the same three-way trade promised in CSCE 641 Module 08: "
           "stretch, seams, wasted space."},

  {"t": "callout", "title": "Where to put seams",
   "kind": "Practical guidance",
   "body": ["<b>In high-curvature regions</b> — cutting there relieves "
            "the most distortion for the least length.",
            "<b>Where they will not be seen</b> — under the arm, inside "
            "the ear, along an existing hard edge or material boundary.",
            "<b>Along existing feature lines</b> — a seam that follows a "
            "crease is already a discontinuity.",
            "Automatic seam generation exists and is decent; artists still "
            "place seams by hand on hero assets, because 'where will nobody "
            "look' is not a geometric criterion."]},

  {"t": "eq", "kicker": "Measuring", "title": "Quantifying distortion",
   "eqs": [
     ("singular values σ₁, σ₂ of the Jacobian per triangle",
      "How much the map stretches in each principal direction."),
     ("conformal:  σ₁ = σ₂",
      "Equal stretch in all directions — angles preserved."),
     ("authalic:  σ₁σ₂ = 1",
      "Area preserved. Isometric would need both at once."),
   ],
   "caption": "Visualise σ₁/σ₂ per triangle as colour and "
              "you can see exactly where a UV map is failing.",
   "note": "Visualising distortion is the single most useful debugging tool "
           "here and is required in Project 2."},

  {"t": "bullets", "kicker": "Atlas", "title": "Packing, and why it wastes space",
   "items": [
     "Charts must be packed into a single rectangular texture.",
     "",
     "This is 2D bin packing — NP-hard (CSCE 629 Module 12), so "
     "heuristics it is.",
     "",
     "<b>Practical constraints:</b>",
     ("Leave gutters so mipmapping does not bleed between charts.", 1),
     ("Keep texel density consistent, or some regions look blurry.", 1),
     ("Align charts to texel boundaries to avoid resampling artifacts.", 1),
     "",
     "70–85% utilisation is typical and considered good.",
   ],
   "footnote": "Gutter width must scale with the number of mip levels you "
               "intend to use."},
 ],
 "takeaways": [
   "No isometric map exists from a curved surface to the plane — "
   "Theorema Egregium makes this a theorem, not an algorithmic shortcoming.",
   "You can preserve angles (conformal) or area (authalic), never both. "
   "Texture mapping chooses conformal because shear is more visible than "
   "blur.",
   "Harmonic parameterisation fixes the boundary and solves Δu = 0 "
   "twice, reusing the Module 08 Laplacian. Tutte guarantees bijectivity.",
   "Cotangent weights go negative on obtuse triangles, which breaks Tutte's "
   "guarantee and flips triangles.",
   "LSCM frees the boundary and minimises conformal violation, giving far "
   "lower distortion. It is what production tools run.",
   "Closed surfaces must be cut into discs. More seams means less distortion "
   "and more visible cuts — the same trade as CSCE 641 Module 08.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Distortion is unavoidable"),
  ("p", "Parameterisation assigns a 2D coordinate to every point of a "
        "surface — the UV map of CSCE 641 Module 08, now constructed "
        "rather than assumed. The first thing to establish is that it cannot "
        "be done perfectly."),
  ("callout", "The argument, in three lines",
   ["Gaussian curvature is <b>intrinsic</b> (Module 07): computable from "
    "lengths and angles measured within the surface, with no reference to the "
    "ambient space.",
    "An <b>isometric</b> map preserves all lengths, hence all intrinsic "
    "quantities, hence K.",
    "A sphere has K = 1/r&#178; &ne; 0; a plane has K = 0. Therefore no "
    "isometric map between them exists.",
    "This is a theorem. No future algorithm will flatten a sphere without "
    "distortion. The entire subject is about <i>choosing which distortion to "
    "accept</i>."]),
  ("table", ["Map type", "Preserves", "Distorts", "When it exists"],
   [["<b>Isometric</b>", "Lengths, angles, areas — everything.",
     "Nothing.", "Only for <b>developable</b> surfaces: planes, cylinders, "
     "cones. K must already be 0."],
    ["<b>Conformal</b>", "<b>Angles.</b> Locally, shapes are preserved and "
     "only scaled.", "Area — regions grow or shrink.",
     "Any disc-topology patch. Guaranteed by the uniformisation theorem."],
    ["<b>Authalic</b>", "<b>Area.</b>", "Angles — shapes shear.",
     "Any disc-topology patch."],
    ["<b>Neither</b>", "—", "Both, but each by less.",
     "Always. ARAP and similar methods live here."]],
   [0.15, 0.27, 0.24, 0.34]),
  ("callout", "This is the map projection problem",
   ["Mercator is conformal: angles and local shapes are right, which is why "
    "it was used for navigation, and areas are badly wrong — Greenland "
    "appears the size of Africa.",
    "Equal-area projections get the areas right and shear the shapes.",
    "Cartographers have argued about this for four centuries and the "
    "constraint has never moved, because it is Theorema Egregium. UV "
    "unwrapping is the same problem with a different surface."]),
  ("h2", "1.1 &nbsp; Which distortion to accept"),
  ("p", "For texture mapping the answer is nearly always conformal, and the "
        "reason is perceptual rather than mathematical."),
  ("ul", ["<b>Angle distortion</b> appears as shearing: a checkerboard "
          "becomes a pattern of parallelograms, straight features bend, text "
          "becomes italic. The eye detects this immediately.",
          "<b>Area distortion</b> appears as varying texel density: some "
          "regions are sharper than others. The eye tolerates this well "
          "unless the variation is extreme.",
          "So: preserve angles, and control area distortion separately by "
          "cutting the surface into charts small enough that the area "
          "variation within each is acceptable."]),

  ("h1", "2 &nbsp; Harmonic parameterisation"),
  ("p", "The simplest method, and it is a direct application of Module 08."),
  ("ol", ["Cut the surface to disc topology (&sect;4).",
          "Map the boundary to a convex shape — a circle or square "
          "— by arc length.",
          "Solve &Delta;u = 0 and &Delta;v = 0 in the interior, with those "
          "boundary values fixed."]),
  ("p", "That is two sparse linear solves with the Laplacian you already "
        "built, with boundary rows replaced by identity constraints. The "
        "resulting map is harmonic: the smoothest possible interpolation of "
        "the boundary conditions."),
  ("callout", "Tutte's embedding theorem",
   ["If the boundary is mapped to a <b>convex</b> polygon and all edge "
    "weights are <b>positive</b>, the resulting map is guaranteed to be "
    "<b>bijective</b> — no triangle flips, no fold-over.",
    "This is an unusually strong guarantee and it is why harmonic "
    "parameterisation remains worth knowing despite its distortion.",
    "<b>But the positivity condition matters.</b> Cotangent weights are "
    "negative on obtuse triangles (Module 07), which violates the hypothesis "
    "and allows flips. Using uniform weights restores the guarantee at the "
    "cost of ignoring geometry; remeshing to remove obtuse triangles "
    "(Module 10) keeps both. This is a concrete case where mesh quality "
    "determines whether a theorem applies."]),
  ("p", "The real limitation is the fixed boundary. Forcing a long thin patch "
        "onto a circle stretches it severely, and the distortion is imposed "
        "by your boundary choice rather than by the surface. That is what "
        "free-boundary methods fix."),

  ("break",),
  ("h1", "3 &nbsp; Free-boundary methods"),
  ("h2", "3.1 &nbsp; Least-squares conformal maps"),
  ("p", "A map is conformal exactly when it satisfies the Cauchy&ndash;"
        "Riemann equations. LSCM does not attempt to satisfy them exactly "
        "— which is generally impossible on a triangulation — but "
        "minimises the squared violation over the whole mesh."),
  ("p", "Because no boundary is prescribed, the system has a four-dimensional "
        "null space corresponding to translation, rotation, and uniform "
        "scale. Pinning <b>two</b> vertices removes it. The result is a "
        "sparse least-squares problem, solved once, and the boundary takes "
        "whatever shape minimises distortion."),
  ("p", "Distortion is typically far lower than harmonic parameterisation "
        "with a forced boundary, and LSCM or a close relative is what "
        "production UV tools run when you press 'unwrap'."),
  ("table", ["Method", "Boundary", "Guarantee", "Distortion", "Cost"],
   [["Harmonic / Tutte", "Fixed, convex", "Bijective (positive weights)",
     "High when the boundary is forced", "Two sparse solves"],
    ["<b>LSCM</b>", "Free, two pins", "Usually bijective in practice",
     "<b>Low</b>", "One least-squares solve"],
    ["ABF++", "Free", "Near-conformal; angle-based formulation",
     "<b>Very low</b>", "Nonlinear, iterative"],
    ["ARAP", "Free", "—", "Low; balances angle and area",
     "Local/global iteration"],
    ["BFF", "Free", "Conformal, with boundary control",
     "<b>Very low</b>", "Fast; essentially two solves"]],
   [0.19, 0.16, 0.26, 0.21, 0.18]),
  ("p", "<b>Boundary First Flattening</b> (Sawhney and Crane) is worth "
        "knowing about: it is conformal, extremely fast, and gives direct "
        "control over the boundary shape or the boundary scale factor, which "
        "is exactly what an artist wants."),

  ("h1", "4 &nbsp; Cutting and atlases"),
  ("p", "Every method above requires <b>disc topology</b>. A sphere, a torus, "
        "and a character are not discs, so the surface must be cut first."),
  ("h2", "4.1 &nbsp; Seams"),
  ("p", "Cutting introduces <b>seams</b>: curves along which the texture "
        "coordinates are discontinuous. Across a seam, filtering and "
        "mipmapping break down (CSCE 641 Module 08), and any mismatch in the "
        "texture shows as a visible line."),
  ("callout", "The three-way trade, again",
   ["CSCE 641 Module 08 claimed that every UV map trades <b>stretch</b>, "
    "<b>seams</b>, and <b>wasted atlas space</b> against each other, and that "
    "none can be eliminated. This module is why.",
    "More cuts &rarr; each chart is flatter &rarr; less distortion — but "
    "more visible seams and more wasted space between packed charts.",
    "Fewer cuts &rarr; cleaner appearance and better packing — but "
    "higher distortion within each chart.",
    "There is no setting that wins on all three, and the balance depends on "
    "the asset. That is why UV layout remains skilled manual work on "
    "important models."]),
  ("p", "<b>Where to cut:</b> in regions of high Gaussian curvature, since "
        "that is where the most distortion is relieved per unit of seam "
        "length; along existing feature lines and material boundaries, which "
        "are already discontinuities; and in places that will not be looked "
        "at. Automatic seam generation handles the first two reasonably and "
        "cannot evaluate the third, which is why artists still place seams by "
        "hand on hero assets."),
  ("h2", "4.2 &nbsp; Measuring distortion"),
  ("p", "Per triangle, the map has a 2&times;2 Jacobian with singular values "
        "&sigma;&#8321; &ge; &sigma;&#8322; — the stretch factors along "
        "two principal directions."),
  ("table", ["Quantity", "Meaning", "Ideal"],
   [["&sigma;&#8321;/&sigma;&#8322;", "Anisotropy — angle distortion",
     "1 (conformal)"],
    ["&sigma;&#8321;&sigma;&#8322;", "Area scaling", "1 (authalic)"],
    ["max(&sigma;&#8321;, 1/&sigma;&#8322;)", "Worst-case stretch", "1"],
    ["sign of det J", "Orientation", "Positive everywhere, or a triangle has "
     "flipped"]],
   [0.26, 0.42, 0.32]),
  ("callout", "Visualise it",
   ["Colour each triangle by &sigma;&#8321;/&sigma;&#8322; and the failures "
    "of a UV map become obvious at a glance: stretched regions light up, and "
    "flipped triangles show as negative determinant.",
    "This is the most useful debugging tool in the module and is required in "
    "Project 2. A checkerboard texture applied to the model is the artist's "
    "version of the same diagnostic, and it works for the same reason."]),
  ("h2", "4.3 &nbsp; Packing"),
  ("p", "Charts must be arranged into one rectangular texture. This is 2D bin "
        "packing, which is NP-hard (CSCE 629 Module 12), so every "
        "implementation is a heuristic."),
  ("ul", ["<b>Gutters.</b> Leave empty space between charts so that mipmap "
          "filtering does not blend one chart into its neighbour. The gutter "
          "must be wide enough for the coarsest mip level you intend to use "
          "— which means it scales with the mip count, not with a fixed "
          "pixel value.",
          "<b>Consistent texel density.</b> Charts should be scaled so that "
          "equal surface area receives equal texture area, or some parts of "
          "the model will be visibly sharper than others.",
          "<b>Texel alignment.</b> Aligning chart boundaries to texel centres "
          "avoids resampling artifacts at the edges.",
          "<b>Utilisation.</b> 70&ndash;85% is typical and considered good. "
          "The remainder is gutters and packing waste."]),
 ],
 "resources": [
   ("Keenan Crane — DDG, conformal geometry lectures",
    "https://brickisland.net/ddg-web/",
    "Conformal maps, the uniformisation theorem, and why angles are the right "
    "thing to preserve."),
   ("Lévy et al. — Least Squares Conformal Maps (free)",
    "https://web.archive.org/web/20230321072033/https://members.loria.fr/Bruno.Levy/papers/LSCM_SIGGRAPH_2002.pdf",
    "The LSCM paper. Short, clear, and directly implementable."),
   ("Sawhney & Crane — Boundary First Flattening (free)",
    "https://www.cs.cmu.edu/~kmcrane/Projects/BoundaryFirstFlattening/",
    "A fast conformal method with direct boundary control, plus a free tool "
    "to compare your results against."),
   ("Hormann, Lévy & Sheffer — Mesh Parameterization SIGGRAPH "
    "course (free)",
    "https://www.inf.usi.ch/hormann/parameterization/",
    "The comprehensive survey. The reference when you need a method this "
    "module did not cover."),
 ],
 "exercises": [
   "Implement harmonic parameterisation: map the boundary to a circle and "
   "solve &Delta;u = 0 twice. Apply a checkerboard texture and capture the "
   "distortion.",
   "Repeat with uniform weights and with cotangent weights on a mesh "
   "containing obtuse triangles. Find a flipped triangle in the cotangent "
   "version and explain it via Tutte's hypothesis.",
   "Implement LSCM with two pinned vertices. Compare distortion against the "
   "harmonic result on the same patch, reporting the distribution of "
   "&sigma;&#8321;/&sigma;&#8322;.",
   "Implement per-triangle distortion visualisation. Colour by anisotropy and "
   "by area scaling, and render both.",
   "Cut a closed mesh into charts by hand, parameterise each, and pack them "
   "into an atlas. Report the utilisation percentage.",
   "Experiment with seam placement: parameterise the same model with two "
   "seams and with eight. Compare maximum distortion and atlas utilisation, "
   "and render both with a checkerboard.",
   "Implement gutter generation and demonstrate texture bleeding across "
   "charts at a coarse mip level when the gutter is too narrow.",
 ],
 "selfcheck": [
   "Why is distortion-free flattening impossible? Give the three-line "
   "argument.",
   "What do conformal and authalic maps each preserve, and why does texture "
   "mapping prefer conformal?",
   "Describe harmonic parameterisation in three steps, and state Tutte's "
   "guarantee with its hypotheses.",
   "Why can cotangent weights break Tutte's guarantee, and what are your "
   "options?",
   "What does LSCM minimise, and why must two vertices be pinned?",
   "What are the three quantities a UV layout trades against each other?",
   "How do you measure distortion per triangle, and what would a flipped "
   "triangle look like in that measure?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Simplification and Remeshing",
 "subtitle": "Fewer triangles, better triangles.",
 "question": "How do you remove 90% of the triangles and keep the shape?",
 "outcomes": [
     "Implement quadric error metric simplification.",
     "Preserve attributes and seams through simplification.",
     "Explain why mesh quality affects operator behaviour.",
     "Implement isotropic remeshing by local operations.",
     "Explain Delaunay and anisotropic remeshing.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Simplification",
   "blurb": "Edge collapse, scheduled by a cost metric."},

  {"t": "bullets", "kicker": "The algorithm", "title": "Greedy edge collapse",
   "items": [
     "Repeatedly collapse the <b>cheapest</b> edge until the target count is "
     "reached.",
     "",
     "Needs three things:",
     ("A <b>cost</b> for each candidate collapse.", 1),
     ("A <b>position</b> for the merged vertex.", 1),
     ("<b>Validity checks</b> — the link condition and the normal-flip "
      "test from Module 02.", 1),
     "",
     "A priority queue over edges, updated locally after each collapse.",
     "",
     "O(n log n) overall. The whole design is in the cost function.",
   ]},

  {"t": "eq", "kicker": "QEM", "title": "The quadric error metric",
   "eqs": [
     ("Qᵥ  =  Σ  (plane of each incident face) as a 4×4 matrix",
      "Encodes the sum of squared distances to those planes."),
     ("error(v)  =  vᵀ Q v",
      "The squared distance from v to the original surface, approximately."),
     ("Q_merged  =  Qₐ + Qᵇ",
      "<b>Quadrics simply add.</b> That is what makes this efficient."),
   ],
   "caption": "The optimal merged position is where ∇(vᵀQv) = 0, a "
              "4×4 solve. Constant time per collapse.",
   "note": "Additivity is the whole trick. Without it you would need to "
           "retain the original planes forever."},

  {"t": "callout", "title": "Why quadrics preserve silhouettes",
   "kind": "The useful property",
   "body": ["A quadric measures squared distance to the planes of the "
            "<i>original</i> faces, and that information is carried forward "
            "through every collapse by addition.",
            "In a flat region, all planes coincide, so the error of "
            "collapsing is near zero and the edge is collapsed early — "
            "correctly, since flat regions need few triangles.",
            "At a sharp silhouette, the incident planes differ greatly, so "
            "any merged position is far from at least one of them and the "
            "cost is high. Those edges survive.",
            "The method therefore concentrates triangles where the shape "
            "needs them, without being told what a feature is."]},

  {"t": "section", "label": "Part 2", "title": "Attributes",
   "blurb": "Where naive simplification destroys your asset."},

  {"t": "bullets", "kicker": "Attributes", "title": "Geometry is not the only thing to preserve",
   "items": [
     "A real mesh carries UVs, normals, colours, bone weights, material IDs.",
     "",
     "<b>Collapsing across a UV seam destroys the atlas.</b> Two vertices at "
     "the same position with different UVs are <i>not</i> the same vertex.",
     "",
     "<b>Fixes:</b>",
     ("Forbid collapses that cross a seam or a material boundary.", 1),
     ("Extend the quadric to the attribute space — a larger matrix "
      "measuring attribute error too.", 1),
     ("Weight seam edges heavily rather than forbidding them outright.", 1),
     "",
     "Production simplifiers do all three, with artist overrides.",
   ],
   "note": "This is the difference between a toy simplifier and one you can "
           "put in a pipeline."},

  {"t": "table", "kicker": "LOD", "title": "Using simplification in a pipeline",
   "header": ["Approach", "How", "Trade-off"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["Discrete LOD", "Prebuild several levels, switch by distance", "Simple; <b>pops</b>"],
     ["Progressive mesh", "Store the collapse sequence; undo to refine", "Smooth; complex runtime"],
     ["Normal baking", "Bake high-res detail into a normal map", "<b>Standard</b>; silhouette unchanged"],
     ["Virtualised", "Cluster-based, selected per frame", "Best; large system"],
   ],
   "note": "Normal baking is the one every pipeline uses and connects "
           "directly to CSCE 641 Module 08."},

  {"t": "section", "label": "Part 3", "title": "Remeshing",
   "blurb": "Not fewer triangles — better ones."},

  {"t": "callout", "title": "Why triangle quality is not cosmetic",
   "kind": "The reason this module exists",
   "body": ["Module 07: cotangent weights go <b>negative</b> on obtuse "
            "triangles, so the Laplacian loses the maximum principle.",
            "Module 09: negative weights break Tutte's bijectivity guarantee, "
            "and triangles flip in the parameterisation.",
            "Module 08: the explicit smoothing time step is limited by the "
            "<i>shortest</i> edge, so one sliver throttles the entire mesh.",
            "Numerical solvers converge more slowly on badly conditioned "
            "systems, and badly shaped triangles are what condition them "
            "badly.",
            "<b>Mesh quality determines whether your operators work.</b> It "
            "is not an aesthetic concern."]},

  {"t": "code", "kicker": "Isotropic remeshing", "title": "Four local operations, repeated",
   "lang": "text", "code": """
target edge length L.  Repeat 5-10 times:

  1. SPLIT   every edge longer than (4/3)L
  2. COLLAPSE every edge shorter than (4/5)L
  3. FLIP    edges to drive vertex valence toward 6
  4. SMOOTH  tangentially (Module 08), then project back
             onto the original surface

The 4/3 and 4/5 thresholds are chosen so that splitting and
collapsing do not undo each other and the process converges.

Result: near-equilateral triangles, uniform size, valence ~6.
""",
   "caption": "Nothing here is new — it is the Module 02 operations "
              "scheduled by the Module 08 smoothing. The projection step is "
              "what keeps the shape.",
   "note": "The threshold choice is the non-obvious part and the reason naive "
           "implementations oscillate forever."},

  {"t": "bullets", "kicker": "Valence", "title": "Why target valence 6",
   "items": [
     "Module 01: average valence in a closed triangle mesh is forced to be "
     "≈ 6 by Euler's formula.",
     "",
     "So valence 6 everywhere is the most uniform mesh topology allows.",
     "",
     "A flip is accepted if it reduces total valence deviation from 6.",
     "",
     "Combined with tangential smoothing, this drives triangles toward "
     "equilateral — which is what makes cotangent weights positive and "
     "operators well behaved.",
   ],
   "footnote": "Topology forced the number; the algorithm just pursues it."},

  {"t": "table", "kicker": "Variants", "title": "Other remeshing goals",
   "header": ["Goal", "Method", "For"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["Isotropic", "Uniform edge length; valence 6", "Simulation; operator quality"],
     ["Adaptive", "Edge length ∝ local feature size", "Detail where curvature is high"],
     ["Anisotropic", "Triangles aligned to curvature directions", "Fewer triangles, same accuracy"],
     ["Quad remeshing", "Cross field → quad layout", "Subdivision cages, animation"],
     ["Delaunay", "Flip to satisfy the empty-circle property", "Maximises minimum angle"],
   ],
   "note": "Quad remeshing is the hardest and the one artists most want, "
           "since subdivision cages should be quads."},

  {"t": "callout", "title": "Anisotropic remeshing: fewer triangles for the same error",
   "kind": "The idea worth knowing",
   "body": ["A cylinder is curved in one direction and flat in the other. "
            "Isotropic remeshing puts equally sized triangles everywhere, "
            "which wastes them along the flat direction.",
            "<b>Anisotropic</b> remeshing elongates triangles along "
            "directions of low curvature and shortens them across high "
            "curvature — aligning the mesh to the principal curvature "
            "directions from Module 07.",
            "The result approximates the same surface to the same tolerance "
            "with substantially fewer triangles.",
            "The cost: the triangles are no longer well-shaped, so the "
            "operator-quality benefits of isotropic remeshing are given up. "
            "Choose by what the mesh is for."]},
 ],
 "takeaways": [
   "Simplification is greedy edge collapse ordered by a cost metric, with the "
   "link condition and normal-flip checks from Module 02.",
   "Quadric error measures squared distance to the original face planes, and "
   "quadrics <b>add</b> — which is what makes the method efficient.",
   "Quadrics preserve silhouettes automatically, because high-curvature "
   "regions have disagreeing planes and therefore high collapse cost.",
   "Collapsing across a UV seam destroys the atlas. Real simplifiers forbid "
   "or heavily penalise those collapses.",
   "Mesh quality is not cosmetic: obtuse triangles break cotangent weights, "
   "Tutte's guarantee, and explicit smoothing stability.",
   "Isotropic remeshing is split, collapse, flip, and tangential smooth, "
   "repeated — driving valence toward the 6 that topology already "
   "demands on average.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Simplification"),
  ("p", "Reduce triangle count while keeping the shape. The standard approach "
        "is greedy: repeatedly perform the cheapest edge collapse until the "
        "target is met."),
  ("ol", ["Compute a <b>cost</b> for every edge and insert into a priority "
          "queue.",
          "Pop the cheapest. Check the <b>link condition</b> and the "
          "<b>normal-flip test</b> (Module 02); skip if either fails.",
          "Collapse, placing the merged vertex at the position the metric "
          "says is optimal.",
          "Recompute costs for the affected edges and update the queue.",
          "Repeat."]),
  ("p", "With a heap this is O(n log n). All of the design is in the cost "
        "function, and the standard answer has been the same since 1997."),
  ("h2", "1.1 &nbsp; Quadric error metrics"),
  ("p", "Garland and Heckbert's insight: associate with each vertex a "
        "<b>quadric</b> — a 4&times;4 symmetric matrix Q encoding the "
        "sum of squared distances to the planes of the faces originally "
        "incident to it."),
  ("eq", "error(v) = v&#7488; Q v &nbsp;&nbsp; (v in homogeneous coordinates)"),
  ("callout", "Quadrics add, and that is the whole trick",
   ["When two vertices merge, the quadric of the result is simply "
    "Q<sub>a</sub> + Q<sub>b</sub>. No list of original planes needs to be "
    "retained; the 4&times;4 matrix carries all the information forward.",
    "So the cost of any candidate collapse is computable in constant time, "
    "and the optimal position for the merged vertex is the solution of "
    "&nabla;(v&#7488;Qv) = 0 — a 4&times;4 linear solve. If the system "
    "is singular (a flat or symmetric configuration), fall back to the edge "
    "midpoint.",
    "Without additivity, every collapse would require re-examining the "
    "original geometry, and the algorithm would be quadratic."]),
  ("callout", "Why this preserves silhouettes without being told to",
   ["In a flat region every incident plane is the same plane, so a merged "
    "vertex anywhere on it has error near zero. These edges collapse first "
    "— correctly, because flat regions need few triangles.",
    "At a sharp edge or a high-curvature ridge, the incident planes disagree "
    "strongly. Any merged position is far from at least one of them, so the "
    "cost is high and the edge survives.",
    "The metric therefore concentrates triangles exactly where the shape "
    "requires them, with no feature detection and no parameters. That is why "
    "it has been the standard for nearly thirty years."]),

  ("h1", "2 &nbsp; Attributes: where naive simplification fails"),
  ("p", "A mesh in a real pipeline carries more than positions: texture "
        "coordinates, normals, vertex colours, skinning weights, material "
        "assignments, lightmap coordinates."),
  ("callout", "Collapsing across a UV seam destroys the atlas",
   ["Two vertices at the same 3D position on either side of a UV seam have "
    "<i>different</i> texture coordinates. They are the same point on the "
    "surface and different points in the parameterisation.",
    "A geometry-only simplifier sees one position and merges them, which "
    "silently destroys the seam and sends large regions of the texture to the "
    "wrong place. The geometry still looks correct, which makes the bug "
    "memorable.",
    "The same applies to normal splits at hard edges, to material boundaries, "
    "and to skinning weight discontinuities."]),
  ("table", ["Strategy", "How", "Trade-off"],
   [["<b>Forbid</b>", "Mark seam and boundary edges; never collapse them.",
     "Safe and simple. Seams become over-tessellated relative to their "
     "surroundings at aggressive reduction ratios."],
    ["<b>Extend the quadric</b>", "Enlarge Q to include attribute dimensions, "
     "so error measures geometric <i>and</i> attribute deviation.",
     "Principled and the best quality. Larger matrices, more arithmetic, more "
     "code."],
    ["<b>Weight heavily</b>", "Allow seam collapses but multiply their cost "
     "by a large factor.",
     "A middle path; a single tunable parameter that artists can override per "
     "asset."]],
   [0.20, 0.40, 0.40]),
  ("h2", "2.1 &nbsp; Level of detail in practice"),
  ("table", ["Approach", "Mechanism", "Assessment"],
   [["<b>Discrete LOD</b>", "Prebuild 3&ndash;5 levels; switch by screen-space "
     "size.",
     "Simple and predictable. Pops visibly at the switch; needs dithered or "
     "cross-faded transitions."],
    ["<b>Progressive mesh</b>", "Store the ordered sequence of collapses; "
     "reverse them to refine.",
     "Continuous and smooth. Complex runtime and awkward on the GPU."],
    ["<b>Normal map baking</b>", "Simplify the geometry, then bake the "
     "high-resolution surface's normals into a texture on the low-resolution "
     "mesh.",
     "<b>The standard pipeline.</b> Recovers almost all shading detail. The "
     "silhouette is still simplified, which is the limitation CSCE 641 "
     "Module 08 identified."],
    ["<b>Virtualised geometry</b>", "Cluster-level LOD selected per frame.",
     "Eliminates both popping and manual LOD authoring, at the cost of a "
     "substantial runtime system."]],
   [0.20, 0.40, 0.40]),

  ("break",),
  ("h1", "3 &nbsp; Remeshing"),
  ("p", "Simplification reduces triangle count. <b>Remeshing</b> improves "
        "triangle <i>quality</i>, usually at a similar count, and it matters "
        "far more than it appears to."),
  ("callout", "Quality determines whether your operators work",
   ["<b>Module 07:</b> cotangent weights are negative for obtuse angles, so "
    "the discrete Laplacian loses the maximum principle and smoothing can "
    "move vertices the wrong way.",
    "<b>Module 09:</b> negative weights violate Tutte's hypothesis, so the "
    "bijectivity guarantee fails and parameterisations develop flipped "
    "triangles.",
    "<b>Module 08:</b> the explicit smoothing stability limit scales with the "
    "<i>shortest</i> edge, so a single sliver forces a tiny time step for the "
    "whole mesh.",
    "<b>Numerics generally:</b> badly shaped triangles produce badly "
    "conditioned matrices, and iterative solvers converge slowly or not at "
    "all on them.",
    "Remeshing is therefore not tidying up. It is making the rest of the "
    "course's machinery function."]),
  ("h2", "3.1 &nbsp; Isotropic remeshing"),
  ("code", """Given a target edge length L, repeat 5-10 times:

  1. SPLIT    every edge longer than (4/3) L
  2. COLLAPSE every edge shorter than (4/5) L
  3. FLIP     edges where doing so reduces total valence
              deviation from 6
  4. SMOOTH   tangentially (Module 08), then project each
              vertex back onto the original surface"""),
  ("p", "Every ingredient is from earlier modules: the three local operations "
        "of Module 02, the tangential smoothing of Module 08. Only the "
        "schedule and the projection step are new."),
  ("ul", ["<b>The 4/3 and 4/5 thresholds</b> are chosen so that a newly split "
          "edge is not immediately a collapse candidate and vice versa. "
          "Choosing them naively — say, 1.5L and 0.5L with the wrong "
          "ratio — produces an algorithm that oscillates and never "
          "converges.",
          "<b>Projection back onto the original surface</b> is essential. "
          "Without it, repeated smoothing shrinks and distorts the shape "
          "(Module 08). With it, vertices redistribute across the surface "
          "while the surface itself is preserved."]),
  ("h2", "3.2 &nbsp; Why valence 6"),
  ("p", "Module 01 established that Euler's formula forces the <i>average</i> "
        "vertex valence of a closed triangle mesh to be approximately 6. "
        "Valence 6 everywhere is therefore the most uniform configuration the "
        "topology permits, and a mesh close to it has triangles close to "
        "equilateral — which is exactly the condition that keeps "
        "cotangent weights positive and matrices well conditioned."),
  ("p", "An edge flip is accepted when it reduces the total deviation from 6 "
        "across the four affected vertices. Topology sets the target; the "
        "algorithm merely pursues it."),

  ("h1", "4 &nbsp; Other remeshing goals"),
  ("table", ["Goal", "Method", "Use for"],
   [["<b>Isotropic</b>", "Uniform target edge length; valence 6; tangential "
     "smoothing.",
     "Simulation meshes, finite elements, and anything where operator quality "
     "matters."],
    ["<b>Adaptive</b>", "Target edge length proportional to local feature "
     "size or inverse curvature.",
     "Detail concentrated where the surface is curved, coarse where it is "
     "flat."],
    ["<b>Anisotropic</b>", "Triangles elongated along principal curvature "
     "directions (Module 07).",
     "Approximating a surface to a given tolerance with the fewest triangles."],
    ["<b>Quad remeshing</b>", "Compute a smooth cross field, then extract a "
     "quad layout aligned to it.",
     "Subdivision control cages, animation-friendly topology. The hardest of "
     "these and the one artists most want."],
    ["<b>Delaunay</b>", "Flip edges until the empty-circumcircle property "
     "holds.",
     "Maximises the minimum angle, which is precisely the condition that "
     "avoids negative cotangent weights."]],
   [0.17, 0.41, 0.42]),
  ("callout", "Anisotropic remeshing, and the trade it makes",
   ["A cylinder is curved in one direction and perfectly flat in the other. "
    "Isotropic remeshing gives it equally sized triangles everywhere, which "
    "spends triangles along the flat direction where none are needed.",
    "Anisotropic remeshing stretches triangles along low-curvature directions "
    "and compresses them across high-curvature ones, approximating the same "
    "surface to the same tolerance with substantially fewer triangles.",
    "The price is that the triangles are deliberately far from equilateral, "
    "so every operator-quality benefit of &sect;3 is given up. Use it when "
    "the mesh is for rendering and triangle budget is the constraint; use "
    "isotropic when the mesh is for computation."]),
  ("callout", "Intrinsic Delaunay triangulation",
   ["A more recent alternative worth knowing: rather than moving vertices, "
    "flip edges to obtain the <b>intrinsic</b> Delaunay triangulation — "
    "a different connectivity on the <i>same</i> vertex positions, where the "
    "edges are geodesics rather than straight lines in space.",
    "This guarantees non-negative cotangent weights without altering the "
    "geometry at all, which means operators become well behaved on a mesh you "
    "are not allowed to change. Crane's DDG notes cover it, and it is "
    "increasingly the preferred answer when remeshing is not an option."]),
 ],
 "resources": [
   ("Garland & Heckbert — Surface Simplification Using Quadric Error "
    "Metrics (free)",
    "https://www.cs.cmu.edu/~garland/Papers/quadrics.pdf",
    "The original paper. Short, clear, and still the basis of every "
    "production simplifier."),
   ("Botsch & Kobbelt — A Remeshing Approach to Multiresolution "
    "Modeling (free)",
    "https://www.graphics.rwth-aachen.de/publication/03/",
    "The isotropic remeshing algorithm of &sect;3, including the threshold "
    "choice."),
   ("Polygon Mesh Processing — simplification and remeshing chapters",
    "https://www.pmp-book.org/",
    "The comprehensive survey with implementation detail."),
   ("Sharp, Soliman & Crane — Navigating Intrinsic Triangulations (free)",
    "https://www.cs.cmu.edu/~kmcrane/Projects/NavigatingIntrinsicTriangulations/",
    "Intrinsic Delaunay: fixing operator quality without moving a single "
    "vertex."),
 ],
 "exercises": [
   "Implement quadric error simplification with the link condition and "
   "normal-flip checks. Reduce a 100,000-triangle scan to 10,000 and 1,000 "
   "and render all three at matched screen size.",
   "Visualise which edges survive longest by colouring the mesh with collapse "
   "cost. Confirm that silhouettes and creases are preserved.",
   "Simplify a textured mesh without seam handling and capture the destroyed "
   "UV atlas. Then add seam preservation and compare.",
   "Measure simplification quality properly: compute the Hausdorff distance "
   "between the original and simplified meshes at several reduction ratios "
   "and plot it.",
   "Implement isotropic remeshing. Plot the distribution of triangle angles "
   "before and after, and report the minimum angle in each.",
   "Count obtuse triangles and negative cotangent weights before and after "
   "remeshing. Then re-run the Module 09 parameterisation on both and compare "
   "the number of flipped triangles.",
   "Implement edge flipping to Delaunay and measure the improvement in "
   "minimum angle without moving any vertex.",
   "Bake a normal map from a high-resolution mesh onto its simplified "
   "version. Render both at a distance where they should be "
   "indistinguishable, and find the distance at which the silhouette "
   "difference becomes visible.",
 ],
 "selfcheck": [
   "Describe greedy edge-collapse simplification and the two validity checks "
   "it requires.",
   "What does a quadric measure, and which property makes the algorithm "
   "efficient?",
   "Why does quadric error preserve silhouettes without any feature "
   "detection?",
   "What happens when a simplifier collapses across a UV seam, and name three "
   "remedies?",
   "Give three specific ways poor triangle quality breaks algorithms from "
   "earlier modules.",
   "List the four steps of isotropic remeshing and explain why the 4/3 and "
   "4/5 thresholds are chosen as they are.",
   "Why is valence 6 the target, and where does that number come from?",
   "What does anisotropic remeshing gain and what does it give up?",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Implicit Surfaces and Distance Fields",
 "subtitle": "Defining shape by a function instead of by primitives.",
 "question": "What can you do with a shape defined as f(x) = 0?",
 "outcomes": [
     "Define signed distance fields and their properties.",
     "Compose shapes with CSG and smooth blending operators.",
     "Implement sphere tracing to render implicit surfaces.",
     "Extract a mesh with marching cubes and state its limitations.",
     "Choose between implicit and explicit for a given task.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Signed distance fields",
   "blurb": "The implicit representation that carries extra information."},

  {"t": "eq", "kicker": "SDF", "title": "More than just a zero set",
   "eqs": [
     ("f(x) = 0 on the surface,  < 0 inside,  > 0 outside",
      "Any implicit function does this much."),
     ("|f(x)|  =  distance to the nearest surface point",
      "A <b>signed distance</b> field. The magnitude is meaningful."),
     ("|∇f|  =  1  everywhere",
      "The eikonal property — and ∇f is the surface normal."),
   ],
   "caption": "The distance property is what makes sphere tracing possible "
              "and gives offsetting for free. It is worth preserving.",
   "note": "Many operations break the exact distance property. Knowing which "
           "is the practical skill here."},

  {"t": "code", "kicker": "Primitives", "title": "Exact distance functions",
   "lang": "glsl", "code": """
float sphere(vec3 p, float r)   { return length(p) - r; }

float box(vec3 p, vec3 b) {
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}                                  //  ^ outside        ^ inside

float torus(vec3 p, vec2 t) {
    return length(vec2(length(p.xz) - t.x, p.y)) - t.y;
}

// Transforms apply to the POINT, inverted:
float transformed(vec3 p) { return sphere(inverse(M) * p, r); }
// Non-uniform scale breaks the distance property -- it is then a
// bound, not a distance.
""",
   "caption": "Each is a closed-form exact distance. The box formula handles "
              "inside and outside with one expression, which is why it looks "
              "cryptic.",
   "note": "The transform inversion is a common bug source and worth "
           "highlighting."},

  {"t": "section", "label": "Part 2", "title": "Composition",
   "blurb": "The operations that are trivial here and awful on meshes."},

  {"t": "table", "kicker": "CSG", "title": "Boolean operations in one line each",
   "header": ["Operation", "Formula", "Note"],
   "widths": [3.0, 4.4, 4.7],
   "rows": [
     ["Union", "min(fₐ, fᵇ)", "Exact outside; a bound inside"],
     ["Intersection", "max(fₐ, fᵇ)", "Exact inside; a bound outside"],
     ["Difference", "max(fₐ, −fᵇ)", "Subtract b from a"],
     ["Offset / shell", "f(x) − d", "Grow or shrink by d. Free"],
     ["Infinite repeat", "f(mod(p, c) − 0.5c)", "Unbounded detail, O(1) memory"],
   ],
   "footnote": "Compare with doing any of these on a mesh (Module 01).",
   "note": "The 'exact outside, bound inside' caveat matters for sphere "
           "tracing and is usually glossed over."},

  {"t": "code", "kicker": "Blending", "title": "Smooth union — what meshes cannot do at all",
   "lang": "glsl", "code": """
// Hard union: a visible crease where the shapes meet.
float d = min(da, db);

// Smooth minimum: a controllable fillet, for free.
float smin(float a, float b, float k) {
    float h = clamp(0.5 + 0.5*(b - a)/k, 0.0, 1.0);
    return mix(b, a, h) - k*h*(1.0 - h);
}

// k controls the blend radius. There is no mesh equivalent --
// you would have to construct the fillet geometry explicitly,
// which is exactly what CAD fillet operations do and why they
// are difficult and fragile.
""",
   "caption": "Smooth blending is the operation implicit surfaces make "
              "trivial and meshes make hard. It is the main reason "
              "procedural modelling uses SDFs.",
   "note": "This slide usually sells the representation better than any "
           "argument about inside/outside tests."},

  {"t": "section", "label": "Part 3", "title": "Rendering",
   "blurb": "Sphere tracing — marching by the distance you know is "
            "safe."},

  {"t": "code", "kicker": "Sphere tracing", "title": "The algorithm the distance property enables",
   "lang": "glsl", "code": """
float trace(vec3 ro, vec3 rd) {
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; i++) {
        float d = scene(ro + rd * t);   // distance to NEAREST surface
        if (d < EPS)   return t;        // hit
        if (t > FAR)   break;           // miss
        t += d;                         // <- step by d: provably safe,
    }                                   //    nothing is closer than d
    return -1.0;
}

// Normals from the gradient, by central differences:
vec3 n = normalize(vec3(
    scene(p + e.xyy) - scene(p - e.xyy),
    scene(p + e.yxy) - scene(p - e.yxy),
    scene(p + e.yyx) - scene(p - e.yyx)));
""",
   "caption": "The step size is the distance field's value, which is exactly "
              "why the distance property matters. A mere inside/outside "
              "function would force tiny fixed steps.",
   "note": "Grazing rays are the pathological case: many small steps near a "
           "surface without hitting it."},

  {"t": "bullets", "kicker": "Sphere tracing", "title": "What it gives and what it costs",
   "items": [
     "<b>Gives:</b> exact surfaces at any resolution, no tessellation, no "
     "LOD, trivial CSG and blending.",
     "<b>Gives:</b> cheap soft shadows and ambient occlusion — both fall "
     "out of the distance field.",
     "",
     "<b>Costs:</b> every pixel evaluates the whole scene function. Cost "
     "scales with scene <i>complexity</i>, not with screen coverage.",
     "<b>Costs:</b> grazing rays take many tiny steps near a surface without "
     "converging.",
     "",
     "So: excellent for procedural and demo content, poor for large "
     "artist-authored scenes.",
   ],
   "note": "The complexity-not-coverage point is the key limitation and "
           "explains why games do not render primarily this way."},

  {"t": "section", "label": "Part 4", "title": "Converting to a mesh",
   "blurb": "Marching cubes, and what it loses."},

  {"t": "bullets", "kicker": "Marching cubes", "title": "Extracting a surface",
   "items": [
     "Sample f on a regular grid. Each cell has 8 corners, each inside or "
     "outside: 256 configurations.",
     "",
     "A lookup table gives the triangles for each configuration.",
     "Vertices are placed on edges by linear interpolation of f.",
     "",
     "<b>Loses sharp features.</b> A cube corner becomes rounded, because the "
     "vertex can only lie on a grid edge.",
     "",
     "<b>Dual contouring</b> fixes this: place a vertex anywhere in the cell, "
     "using gradient information to recover the corner.",
   ],
   "note": "The sharp-feature failure is the main practical limitation and "
           "the reason dual contouring exists."},

  {"t": "table", "kicker": "Choosing", "title": "Implicit or explicit?",
   "header": ["Favours implicit", "Favours mesh"],
   "widths": [6.0, 6.1],
   "rows": [
     ["Booleans, blending, offsetting", "Artist-authored detail"],
     ["Procedural and infinite content", "Texture mapping and UVs"],
     ["Collision and distance queries", "Rasterised rendering"],
     ["Topology changes during simulation", "Animation and skinning"],
     ["Compact storage of smooth shapes", "Fine control over every vertex"],
   ],
   "note": "Modern pipelines use both: SDFs for collision, soft shadows, and "
           "GI; meshes for rendering."},

  {"t": "callout", "title": "Where SDFs show up in engines today",
   "kind": "Practical relevance",
   "body": ["<b>Soft shadows:</b> cheap by marching toward the light and "
            "tracking the closest approach.",
            "<b>Ambient occlusion:</b> sample the field at a few points along "
            "the normal.",
            "<b>Global illumination:</b> Unreal's distance field GI traces "
            "coarse SDFs of the scene.",
            "<b>Collision:</b> penetration depth and contact normals come "
            "straight from f and ∇f.",
            "<b>Text and decals:</b> signed distance textures give "
            "resolution-independent sharp edges at any magnification.",
            "You will meet all of these in CSCE 641's successors. Meshes "
            "render; SDFs answer questions about space."]},
 ],
 "takeaways": [
   "A signed distance field carries distance, not just inside/outside, and "
   "satisfies |∇f| = 1 with ∇f as the normal.",
   "Booleans are min and max; offsetting is subtraction; infinite repetition "
   "is a modulo. All trivial, all hard on meshes.",
   "Smooth blending has no mesh equivalent and is the main reason procedural "
   "modelling uses SDFs.",
   "Sphere tracing steps by the distance value, which is provably safe — "
   "and is exactly why the distance property is worth preserving.",
   "Cost scales with scene complexity rather than screen coverage, which "
   "limits implicit rendering to procedural content.",
   "Marching cubes loses sharp features because vertices lie on grid edges; "
   "dual contouring recovers them using gradients.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Implicit surfaces and signed distance"),
  ("p", "An implicit surface is the zero set of a function: "
        "{x : f(x) = 0}, with f negative inside and positive outside. Any "
        "such f defines a surface, but a particular class of them carries "
        "much more information."),
  ("eq", "|f(x)| = distance from x to the nearest point of the surface"),
  ("p", "A function with this property is a <b>signed distance field</b>. "
        "Two consequences follow immediately:"),
  ("ul", ["<b>|&nabla;f| = 1 everywhere</b> (the eikonal equation). Moving a "
          "small step changes the distance by exactly that step.",
          "<b>&nabla;f is the unit surface normal.</b> No averaging, no "
          "weighting choice — just a gradient, available analytically or "
          "by finite differences."]),
  ("p", "Contrast with a mesh, where normals must be averaged with a "
        "weighting scheme (Module 02) and distance queries require a spatial "
        "acceleration structure and a search."),
  ("h2", "1.1 &nbsp; Primitives"),
  ("code", """float sphere(vec3 p, float r) { return length(p) - r; }

float box(vec3 p, vec3 b) {
    vec3 q = abs(p) - b;
    return length(max(q, 0.0))                   // outside distance
         + min(max(q.x, max(q.y, q.z)), 0.0);    // inside distance
}

float torus(vec3 p, vec2 t) {
    return length(vec2(length(p.xz) - t.x, p.y)) - t.y;
}"""),
  ("p", "Each is an exact closed-form distance. The box expression looks "
        "cryptic because it handles both cases in one branchless formula: "
        "outside the box, only the positive components of q contribute; "
        "inside, all components are negative and the largest (least negative) "
        "gives the distance to the nearest face."),
  ("callout", "Transforms, and what breaks the distance property",
   ["To transform a primitive, transform the <i>query point</i> by the "
    "inverse: <code>f(M&#8315;&#185;p)</code>. This is a frequent source of "
    "bugs, because the intuition points the other way.",
    "Rigid transforms preserve the distance property. <b>Non-uniform "
    "scale does not</b> — after scaling, f is a lower bound on the true "
    "distance rather than the distance itself.",
    "A lower bound is still safe for sphere tracing (&sect;3): you step less "
    "far than you could, so you take more steps but never overshoot. Knowing "
    "which operations preserve exactness and which only preserve the bound is "
    "the practical skill in SDF work."]),

  ("h1", "2 &nbsp; Composition"),
  ("table", ["Operation", "Expression", "Exactness"],
   [["Union", "min(f&#8336;, f&#7495;)",
     "Exact outside; a lower bound inside."],
    ["Intersection", "max(f&#8336;, f&#7495;)",
     "Exact inside; a lower bound outside."],
    ["Difference", "max(f&#8336;, &minus;f&#7495;)", "Bound in general."],
    ["Offset / shell", "f(x) &minus; d, or |f(x)| &minus; d",
     "Exact. Offsetting a mesh self-intersects; here it is a subtraction."],
    ["Infinite repetition", "f(mod(p, c) &minus; 0.5c)",
     "Exact for well-separated instances. Unbounded content in O(1) memory."],
    ["Twist, bend, displace", "f(warp(p)), or f(p) + noise(p)",
     "Bound only — the warp changes the metric."]],
   [0.20, 0.34, 0.46]),
  ("p", "Compare each row against doing the same thing to a triangle mesh "
        "(Module 01). Boolean operations on meshes require computing exact "
        "intersection curves, re-triangulating both surfaces along them, and "
        "resolving near-degenerate configurations — a genuinely "
        "difficult problem that commercial kernels still get wrong. Here it "
        "is <code>min</code>."),
  ("h2", "2.1 &nbsp; Smooth blending"),
  ("code", """float smin(float a, float b, float k) {
    float h = clamp(0.5 + 0.5 * (b - a) / k, 0.0, 1.0);
    return mix(b, a, h) - k * h * (1.0 - h);
}"""),
  ("callout", "The operation with no mesh equivalent",
   ["A hard union leaves a crease where the two shapes meet. A smooth minimum "
    "produces a controllable fillet, with k setting the blend radius, from a "
    "single extra line.",
    "There is no corresponding mesh operation. Filleting a mesh junction "
    "means constructing the blend geometry explicitly, which is what CAD "
    "fillet operations do — and they are notoriously fragile, failing on "
    "tight corners and self-intersections.",
    "This is the capability that drives most procedural and demoscene "
    "modelling toward SDFs: organic-looking blends between primitives, for "
    "almost nothing."]),

  ("break",),
  ("h1", "3 &nbsp; Rendering by sphere tracing"),
  ("code", """float trace(vec3 ro, vec3 rd) {
    float t = 0.0;
    for (int i = 0; i < MAX_STEPS; ++i) {
        float d = scene(ro + rd * t);
        if (d < EPS) return t;          // hit
        if (t > FAR) break;             // miss
        t += d;                         // step by the distance
    }
    return -1.0;
}"""),
  ("callout", "Why stepping by d is safe",
   ["f(p) is the distance to the <i>nearest</i> surface point in any "
    "direction. So a sphere of radius f(p) centred at p is guaranteed empty, "
    "and advancing along the ray by f(p) cannot pass through any surface.",
    "This is what the distance property buys. A function that only reported "
    "inside or outside would force small fixed steps, with the risk of "
    "stepping through thin geometry.",
    "If f is a lower bound rather than an exact distance — after a warp "
    "or non-uniform scale — the algorithm still works, taking more steps "
    "than necessary but never overshooting. Hence the common practice of "
    "multiplying warped fields by a safety factor."]),
  ("p", "Normals come from the gradient, estimated by central differences "
        "with four or six extra evaluations of the scene function."),
  ("table", ["Strength", "Limitation"],
   [["Exact surfaces at any resolution; no tessellation, no LOD, no popping.",
     "Every pixel evaluates the <i>entire</i> scene function. Cost scales "
     "with scene complexity, not with how much of the screen the object "
     "covers."],
    ["CSG and blending are nearly free.",
     "Grazing rays take many small steps while running nearly parallel to a "
     "surface without hitting it — the pathological case."],
    ["Soft shadows and ambient occlusion fall out of the distance field "
     "almost for free.",
     "Artist-authored detail is hard to express as a function."],
    ["Infinite repetition and procedural detail at no memory cost.",
     "Texture mapping requires a parameterisation, which an implicit surface "
     "does not have."]],
   [0.5, 0.5]),
  ("p", "The complexity-not-coverage property is the decisive limitation: a "
        "scene of a thousand distinct objects requires evaluating a thousand "
        "primitives per pixel unless you build acceleration structures, at "
        "which point much of the simplicity is gone. This is why sphere "
        "tracing dominates procedural and demoscene rendering and does not "
        "replace rasterisation for authored content."),

  ("h1", "4 &nbsp; Converting to a mesh"),
  ("p", "<b>Marching cubes</b> samples f on a regular grid. Each cell has "
        "eight corners, each inside or outside, giving 256 configurations "
        "(15 up to symmetry). A lookup table gives the triangles for each, "
        "with vertices positioned along cell edges by linear interpolation of "
        "f between the corner values."),
  ("callout", "Marching cubes rounds off sharp features",
   ["A vertex can only be placed <i>on a grid edge</i>. The corner of a cube "
    "lies in the interior of a cell, so it cannot be represented and the "
    "extracted mesh rounds it off.",
    "Refining the grid makes the rounding smaller and never removes it: at "
    "any resolution the corner is still a staircase of small facets. This is "
    "the characteristic 'melted' look of marching-cubes output on hard-"
    "surface shapes.",
    "<b>Dual contouring</b> fixes it by placing one vertex <i>anywhere inside</i> "
    "each cell, chosen to minimise error against the gradient information "
    "sampled on the cell's edges. Sharp corners are recovered exactly, at the "
    "cost of needing gradients and of producing non-manifold output in some "
    "configurations."]),
  ("p", "Marching cubes also produces many poorly shaped triangles — "
        "slivers where the surface grazes a cell corner — so output is "
        "normally remeshed (Module 10) before use."),

  ("h1", "5 &nbsp; Choosing, and using both"),
  ("table", ["Favours implicit", "Favours explicit mesh"],
   [["Boolean operations, blending, offsetting.",
     "Artist-authored detail and precise control."],
    ["Procedural, infinite, or very smooth content.",
     "Texture mapping, which needs a parameterisation (Module 09)."],
    ["Distance and collision queries.", "Rasterised rendering at scale."],
    ["Topology changes during simulation — merging and splitting fluids.",
     "Skeletal animation and skinning."],
    ["Compact storage of smooth shapes.",
     "Predictable, bounded per-frame cost."]],
   [0.5, 0.5]),
  ("callout", "Modern engines use both, for different jobs",
   ["<b>Soft shadows</b> — march toward the light and track the closest "
    "approach; the penumbra falls out of the distance values.",
    "<b>Ambient occlusion</b> — sample the field at a few points along "
    "the normal and compare against the distance travelled.",
    "<b>Global illumination</b> — Unreal Engine's distance field GI "
    "traces coarse per-object SDFs rather than the triangle geometry.",
    "<b>Collision</b> — penetration depth is f and the contact normal is "
    "&nabla;f, both immediate.",
    "<b>Text and decals</b> — signed distance textures give "
    "resolution-independent sharp edges under arbitrary magnification, which "
    "is why they replaced bitmap fonts in engines.",
    "The division of labour is clean: <b>meshes render; distance fields "
    "answer questions about space.</b>"]),
 ],
 "resources": [
   ("Inigo Quilez — distance functions and articles (free)",
    "https://iquilezles.org/articles/",
    "The primary practical source: exact SDFs for dozens of primitives, "
    "blending operators, soft shadows, and ambient occlusion, all with "
    "derivations and working code."),
   ("Shadertoy",
    "https://www.shadertoy.com/",
    "Thousands of sphere-traced scenes with readable source. The fastest way "
    "to learn the idioms."),
   ("Lorensen & Cline — Marching Cubes (free summaries widely "
    "available)",
    "https://dl.acm.org/doi/10.1145/37401.37422",
    "The original algorithm. The lookup-table construction is worth "
    "understanding once."),
   ("Ju et al. — Dual Contouring of Hermite Data (free)",
    "https://www.cse.wustl.edu/~taoju/research/dualContour.pdf",
    "How to recover sharp features that marching cubes loses."),
 ],
 "exercises": [
   "Implement a sphere tracer in a fragment shader. Render a sphere, a box, "
   "and a torus with gradient-based normals and simple lighting.",
   "Implement union, intersection, and difference. Build a shape that would "
   "be genuinely painful to construct as a mesh, and note how long it took.",
   "Implement <code>smin</code> and sweep k from 0 to a large value, "
   "capturing the blend at several settings.",
   "Implement infinite repetition with a modulo and render an unbounded field "
   "of objects. Confirm memory use does not depend on the number visible.",
   "Implement soft shadows and ambient occlusion from the distance field. "
   "Compare the result and the cost against shadow mapping from CSCE 641 "
   "Module 10.",
   "Apply a non-uniform scale to a primitive and demonstrate that the field "
   "is no longer an exact distance. Show that sphere tracing still terminates "
   "and count the extra steps.",
   "Implement marching cubes and extract a mesh from an SDF of a cube. "
   "Capture the rounded corners at three grid resolutions and confirm they "
   "never become sharp.",
   "Extract the same cube with dual contouring and compare.",
 ],
 "selfcheck": [
   "What distinguishes a signed distance field from an arbitrary implicit "
   "function, and what two properties follow?",
   "Give the expressions for union, intersection, difference, and offset.",
   "Which operations preserve exact distance and which leave only a bound? "
   "Why does the distinction not break sphere tracing?",
   "Why is smooth blending the operation that most favours implicit "
   "representations?",
   "Why is stepping by f(p) provably safe in sphere tracing?",
   "What is sphere tracing's main scaling limitation, and why does it rule "
   "out large authored scenes?",
   "Why does marching cubes round off sharp corners, and what does dual "
   "contouring change?",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Solid Modeling and Booleans",
 "subtitle": "Where exact geometry meets floating-point arithmetic.",
 "question": "Why are mesh booleans so unreliable?",
 "outcomes": [
     "Explain boundary representation and its validity conditions.",
     "Describe the mesh boolean pipeline and where it fails.",
     "Explain robustness predicates and exact arithmetic.",
     "Explain why implicit and voxel approaches trade accuracy for "
     "robustness.",
     "Choose an approach from the required guarantees.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "B-rep",
   "blurb": "Representing a solid by its boundary."},

  {"t": "bullets", "kicker": "B-rep", "title": "What makes a mesh a solid",
   "items": [
     "A <b>boundary representation</b> describes a solid by the surface "
     "enclosing it.",
     "",
     "For that to define a solid, the surface must be:",
     ("<b>Closed</b> — no boundary edges, no holes.", 1),
     ("<b>Manifold</b> — Module 01's conditions.", 1),
     ("<b>Orientable and consistently oriented</b> — normals all point "
      "outward.", 1),
     ("<b>Non-self-intersecting</b> — the hard one to check.", 1),
     "",
     "Only then is 'inside' well defined, and only then do booleans mean "
     "anything.",
   ],
   "note": "Self-intersection is the condition that is expensive to verify "
           "and that real assets violate constantly."},

  {"t": "eq", "kicker": "Inside test", "title": "Two ways to ask 'is this inside?'",
   "eqs": [
     ("ray parity:  cast a ray, count crossings",
      "Odd = inside. Simple, and fragile when the ray hits an edge or "
      "vertex."),
     ("winding number:  Σ solid angles / 4π",
      "Robust, handles self-intersection gracefully, and generalises."),
     ("generalised winding number",
      "Works on <b>open and broken</b> meshes — which is why it is now "
      "preferred."),
   ],
   "caption": "The generalised winding number gives a meaningful "
              "'insideness' even for meshes that are not watertight, which "
              "is most real meshes.",
   "note": "Jacobson's generalised winding number is the modern answer and "
           "worth knowing about."},

  {"t": "section", "label": "Part 2", "title": "Mesh booleans",
   "blurb": "The pipeline, and the step where it breaks."},

  {"t": "bullets", "kicker": "The pipeline", "title": "Four steps, one of them treacherous",
   "items": [
     "<b>1. Find all intersections</b> between triangles of A and B. "
     "Accelerated by a BVH.",
     "<b>2. Compute the intersection curves</b> — segments where "
     "triangles cross.",
     "<b>3. Re-triangulate</b> both surfaces so the curves become mesh edges.",
     "<b>4. Classify and keep</b> the pieces: inside/outside, per operation.",
     "",
     "Steps 1, 3, and 4 are routine.",
     "",
     "<b>Step 2 is where everything fails</b>, because it asks for exact "
     "answers from inexact arithmetic.",
   ]},

  {"t": "callout", "title": "Degeneracies are not rare — they are the common case",
   "kind": "Why booleans fail",
   "body": ["Real models are <b>aligned</b>. Faces are coplanar, edges are "
            "collinear, vertices coincide. People model that way "
            "deliberately.",
            "So the questions 'do these planes coincide?' and 'does this "
            "vertex lie exactly on that edge?' are asked constantly, and "
            "floating-point arithmetic cannot answer them reliably.",
            "An epsilon that is too small misses the coincidence and produces "
            "a sliver triangle; too large merges things that should stay "
            "apart. There is no correct epsilon.",
            "Worse, inconsistent answers to related questions produce a "
            "topologically impossible result — a surface that is not "
            "closed, or an edge with three faces. The output is garbage "
            "rather than slightly wrong."]},

  {"t": "section", "label": "Part 3", "title": "Robustness",
   "blurb": "Three strategies, each giving something up."},

  {"t": "table", "kicker": "Strategies", "title": "How robustness is bought",
   "header": ["Approach", "Idea", "Cost"],
   "widths": [3.0, 4.6, 4.5],
   "rows": [
     ["Exact predicates", "Adaptive-precision arithmetic for sign tests", "Slower; exactness only in predicates"],
     ["Exact arithmetic", "Rationals throughout", "Much slower; coordinates blow up"],
     ["Snap rounding", "Round everything to a fixed grid", "Alters geometry; can still fail"],
     ["Voxelise", "Convert to a grid, boolean, re-extract", "<b>Always works</b>; loses sharpness"],
     ["Implicit", "min/max on distance fields", "<b>Trivial</b>; approximate surface"],
   ],
   "note": "Shewchuk's adaptive predicates are the standard answer and are "
           "freely available."},

  {"t": "callout", "title": "Exact predicates: exactness where it matters",
   "kind": "The standard solution",
   "body": ["The insight is that booleans do not need exact <i>coordinates</i>. "
            "They need exact <b>signs</b> of a few geometric predicates: "
            "which side of a plane a point lies on, whether four points are "
            "coplanar, orientation tests.",
            "Shewchuk's adaptive predicates compute those signs exactly, "
            "using floating-point filters that are fast in the common case "
            "and escalate to higher precision only when the result is too "
            "close to call.",
            "The result is a correct answer at close to floating-point speed, "
            "and it makes the combinatorial structure of the output "
            "<i>consistent</i> — which is what prevents topologically "
            "impossible results.",
            "This is why CGAL and every serious geometry kernel use them."]},

  {"t": "bullets", "kicker": "Alternatives", "title": "Trading exactness for reliability",
   "items": [
     "<b>Voxelise.</b> Convert both solids to a grid, boolean per voxel "
     "(trivial), extract a mesh.",
     ("Always works, never fails, and rounds every sharp edge to the voxel "
      "size.", 1),
     "",
     "<b>Implicit.</b> Convert to distance fields, use min/max, extract "
     "(Module 11).",
     ("Same trade, plus smooth blending for free.", 1),
     "",
     "<b>This is a real engineering choice:</b> 3D printing pipelines "
     "routinely voxelise because a slightly rounded corner is far better than "
     "a failed boolean.",
   ],
   "note": "Framing it as a legitimate engineering trade rather than a "
           "cop-out is important — it is what production actually does."},

  {"t": "table", "kicker": "Choosing", "title": "What guarantee do you need?",
   "header": ["Need", "Use"],
   "widths": [5.6, 6.5],
   "rows": [
     ["Exact result, manufacturing tolerance", "NURBS B-rep with exact predicates (CAD kernel)"],
     ["Reliable result on messy input", "Voxelise or convert to SDF"],
     ["Smooth blends rather than sharp joins", "Implicit — Module 11"],
     ["Interactive editing", "Implicit, or defer the boolean to render time"],
     ["Game asset", "Do it offline in the DCC tool; ship the result"],
   ],
   "footnote": "The last row is the most common real answer."},

  {"t": "callout", "title": "Why this module is short",
   "kind": "Honest framing",
   "body": ["Robust mesh booleans are a genuinely hard, decades-old research "
            "problem, and commercial kernels representing many person-years "
            "still fail on adversarial input.",
            "The practically useful knowledge is: <b>know why it is hard</b>, "
            "<b>know that exact predicates are the real fix</b>, and "
            "<b>know that voxelising is a legitimate answer</b> when "
            "robustness matters more than sharpness.",
            "Do not write your own boolean kernel. Use CGAL, libigl's "
            "mesh_boolean, or Cork, and understand what they are protecting "
            "you from."]},
 ],
 "takeaways": [
   "A B-rep defines a solid only if the surface is closed, manifold, "
   "consistently oriented, and non-self-intersecting.",
   "The generalised winding number gives meaningful inside/outside even for "
   "open or broken meshes, which is most real meshes.",
   "Mesh booleans are four steps, and computing intersection curves is the "
   "one that fails — it demands exact answers from inexact arithmetic.",
   "Degeneracies are the common case, not an edge case, because people model "
   "with aligned and coincident geometry deliberately.",
   "Exact predicates give exact <i>signs</i> at near floating-point speed, "
   "which is what keeps the output topologically consistent.",
   "Voxelising or converting to an SDF always works and rounds sharp "
   "features. That is a legitimate engineering trade, and production uses it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Boundary representation"),
  ("p", "A <b>B-rep</b> describes a solid by the surface that bounds it "
        "— the mesh is not the object, it is the object's skin. For that "
        "to define a solid at all, the surface must satisfy four conditions."),
  ("table", ["Condition", "Meaning", "Cost to check"],
   [["<b>Closed</b>", "No boundary edges; the surface has no holes.",
     "Cheap: count half-edges with no twin."],
    ["<b>Manifold</b>", "Module 01's two conditions on edges and vertices.",
     "Cheap: local checks."],
    ["<b>Consistently oriented</b>", "All face normals point outward.",
     "Cheap: breadth-first traversal across shared edges."],
    ["<b>Non-self-intersecting</b>", "No two faces pass through each other.",
     "<b>Expensive</b>: requires all-pairs intersection testing, accelerated "
     "by a BVH. This is the condition real assets violate constantly."]],
   [0.22, 0.38, 0.40]),
  ("p", "Only when all four hold is 'inside' a well-defined notion, and only "
        "then do boolean operations mean anything."),
  ("h2", "1.1 &nbsp; Deciding inside"),
  ("ul", ["<b>Ray parity.</b> Cast a ray from the query point and count "
          "surface crossings; an odd count means inside. Simple, and fragile: "
          "if the ray passes exactly through an edge or vertex, the count is "
          "ambiguous. Perturbing the ray direction helps and does not fully "
          "fix it.",
          "<b>Winding number.</b> Sum the signed solid angles subtended by "
          "all faces, divided by 4&pi;. For a clean closed mesh this is 1 "
          "inside and 0 outside. It is numerically robust and degrades "
          "gracefully rather than catastrophically."]),
  ("callout", "The generalised winding number",
   ["Jacobson and colleagues observed that the winding number remains "
    "meaningful on meshes that are <i>not</i> watertight: it becomes a smooth "
    "real-valued function that is close to 1 well inside the shape, close to "
    "0 well outside, and intermediate near holes.",
    "Thresholding it gives a sensible inside/outside classification for "
    "meshes with holes, self-intersections, and inconsistent orientation "
    "— which describes most meshes that arrive from a scanner or from "
    "another studio.",
    "This has become the standard way to make downstream operations work on "
    "imperfect input, rather than demanding that the input be repaired first."]),

  ("h1", "2 &nbsp; The boolean pipeline"),
  ("ol", ["<b>Find intersecting triangle pairs</b> between A and B, using a "
          "BVH to avoid the quadratic all-pairs test. Routine.",
          "<b>Compute the intersection segments</b> for each pair and link "
          "them into closed intersection curves. <b>This is where it "
          "breaks.</b>",
          "<b>Re-triangulate</b> both surfaces so that the intersection "
          "curves appear as mesh edges, using a constrained triangulation. "
          "Routine, given correct input from step 2.",
          "<b>Classify and assemble</b>: each resulting patch is inside or "
          "outside the other solid, and the operation determines which "
          "patches to keep and whether to flip them. Routine."]),
  ("callout", "Degeneracies are the common case",
   ["Real models are built with aligned geometry: faces that are exactly "
    "coplanar, edges that are exactly collinear, vertices that coincide "
    "precisely. Designers do this deliberately, because that is how parts fit "
    "together.",
    "So step 2 is constantly asking questions like 'are these two planes the "
    "same plane?' and 'does this vertex lie exactly on that edge?', and "
    "floating-point arithmetic cannot answer them reliably. An epsilon too "
    "small misses genuine coincidences and emits degenerate slivers; too "
    "large merges features that should remain distinct. There is no correct "
    "epsilon.",
    "The serious failure is not inaccuracy but <b>inconsistency</b>. If the "
    "code concludes that point p is above plane Q in one test and below it in "
    "a related test, the resulting combinatorial structure is impossible: a "
    "surface that does not close, or an edge with three incident faces. The "
    "output is not slightly wrong, it is invalid."]),

  ("break",),
  ("h1", "3 &nbsp; Buying robustness"),
  ("table", ["Approach", "What it does", "What it costs"],
   [["<b>Exact predicates</b>", "Compute the <i>signs</i> of geometric "
     "predicates exactly, using floating-point filters that escalate to "
     "higher precision only when needed.",
     "Modest slowdown. Does not give exact coordinates — only exact "
     "decisions, which is what matters."],
    ["<b>Exact arithmetic throughout</b>", "Represent all coordinates as "
     "rationals.",
     "Much slower, and coordinate representations grow without bound through "
     "chained operations."],
    ["<b>Snap rounding</b>", "Round all coordinates to a fixed grid so "
     "near-coincidences become exact coincidences.",
     "Alters the geometry, can collapse small features, and can still produce "
     "invalid topology."],
    ["<b>Voxelise</b>", "Convert both solids to a volumetric grid, perform "
     "the boolean per voxel, extract a mesh.",
     "<b>Never fails.</b> Rounds every sharp feature to the voxel size and "
     "produces a dense mesh needing remeshing."],
    ["<b>Convert to implicit</b>", "Build distance fields and use min/max "
     "(Module 11).",
     "<b>Trivial and robust.</b> The surface is approximate, and you gain "
     "smooth blending as a bonus."]],
   [0.20, 0.42, 0.38]),
  ("callout", "Exact predicates are the real answer",
   ["The key observation is that a boolean algorithm does not need exact "
    "coordinates. It needs the correct <b>sign</b> of a small set of "
    "predicates: orientation of a point relative to a plane, whether four "
    "points are coplanar, in-circle and in-sphere tests.",
    "Shewchuk's <i>adaptive precision</i> predicates evaluate those signs "
    "exactly. They begin with an ordinary floating-point computation plus a "
    "rigorous error bound; if the bound proves the sign, they return "
    "immediately at full speed. Only when the value is too close to zero do "
    "they escalate to extended precision.",
    "In practice almost every call takes the fast path, so the cost is small, "
    "and every decision is correct. Correct decisions mean a <i>consistent</i> "
    "combinatorial structure, which is exactly what prevents impossible "
    "output.",
    "CGAL, libigl, and every serious geometry kernel use them. The code is "
    "freely available and should never be rewritten by hand."]),

  ("h1", "4 &nbsp; The voxel escape hatch"),
  ("p", "Converting to a volumetric or implicit representation makes booleans "
        "trivial, because inside/outside is a per-sample question with no "
        "combinatorial structure to corrupt. Union is a minimum, intersection "
        "a maximum, difference a negation — and no configuration of "
        "input geometry can cause a failure."),
  ("p", "The cost is sharpness: every feature is rounded to the sample "
        "spacing, and marching cubes rounds corners further (Module 11). The "
        "output is also dense and usually needs remeshing."),
  ("callout", "This is a legitimate production choice, not a cop-out",
   ["3D printing pipelines routinely voxelise before booleaning, because a "
    "corner rounded by 0.1 mm is vastly preferable to a boolean that fails "
    "and produces a non-watertight model that cannot be sliced at all.",
    "Game and VFX pipelines do the same for destruction, fluid interaction, "
    "and any case where robustness matters more than exact edges.",
    "The question is never 'which approach is best' but 'what does this "
    "application actually require'. If the answer is manufacturing tolerance, "
    "use a CAD kernel with exact predicates. If it is reliability on arbitrary "
    "input, voxelise."]),

  ("h1", "5 &nbsp; Choosing"),
  ("table", ["Requirement", "Approach"],
   [["Exact results to manufacturing tolerance.",
     "A NURBS B-rep kernel with exact predicates. This is what CAD software "
     "is."],
    ["Reliable results on messy, scanned, or third-party input.",
     "Voxelise, or convert to a distance field. Accept the rounding."],
    ["Smooth blends rather than sharp intersections.",
     "Implicit representation with <code>smin</code> (Module 11)."],
    ["Interactive editing with immediate feedback.",
     "Implicit, evaluated at render time — no mesh is extracted until "
     "export."],
    ["A game asset, booleaned once.",
     "Do it offline in the modelling package, fix the result by hand, ship "
     "the mesh. This is the most common real answer and there is nothing "
     "wrong with it."]],
   [0.42, 0.58]),
  ("callout", "The practical summary",
   ["Robust mesh booleans have been an active research problem for four "
    "decades, and commercial kernels representing enormous investment still "
    "fail on adversarial input.",
    "What is worth knowing: <b>why</b> it is hard (exact decisions from "
    "inexact arithmetic, with degeneracies as the common case), <b>what the "
    "real fix is</b> (exact predicates, giving consistency rather than "
    "accuracy), and <b>when to sidestep it</b> (voxelise when robustness "
    "beats sharpness).",
    "Do not write your own. Use CGAL, libigl's <code>mesh_boolean</code>, or "
    "Cork, and understand what they are protecting you from."]),
 ],
 "resources": [
   ("Shewchuk — Adaptive Precision Floating-Point Arithmetic and Fast "
    "Robust Geometric Predicates (free, with code)",
    "https://www.cs.cmu.edu/~quake/robust.html",
    "The paper and the freely usable implementation. The single most "
    "important reference for this module."),
   ("Jacobson et al. — Robust Inside-Outside Segmentation using "
    "Generalized Winding Numbers (free)",
    "https://igl.ethz.ch/projects/winding-number/",
    "How to get meaningful inside/outside answers from broken meshes."),
   ("CGAL — Polygon Mesh Processing and Boolean operations",
    "https://doc.cgal.org/latest/Polygon_mesh_processing/",
    "A production-quality implementation built on exact predicates. Read the "
    "preconditions section carefully."),
   ("libigl — mesh boolean tutorial",
    "https://libigl.github.io/tutorial/",
    "A usable boolean implementation with a short interface, built on "
    "CGAL/exact arithmetic."),
 ],
 "exercises": [
   "Implement a B-rep validator checking all four conditions of &sect;1. Run "
   "it on several downloaded models and report which conditions fail.",
   "Implement ray-parity and winding-number inside tests. Construct a query "
   "point whose ray passes exactly through a vertex and show the parity test "
   "failing while the winding number succeeds.",
   "Implement the generalised winding number on a mesh with a hole, and "
   "visualise it as a scalar field on a slice plane.",
   "Attempt a naive mesh boolean on two cubes sharing a face. Document the "
   "exact point at which floating-point ambiguity defeats it.",
   "Use Shewchuk's predicates for the orientation test in that code and "
   "report what changes.",
   "Implement a voxel boolean: convert two meshes to occupancy grids, "
   "combine, and extract with marching cubes. Measure the feature rounding "
   "against voxel size.",
   "Compare the voxel result against libigl's <code>mesh_boolean</code> on "
   "the same input, for both quality and robustness across twenty randomly "
   "perturbed configurations.",
 ],
 "selfcheck": [
   "What four conditions must a mesh satisfy to represent a solid, and which "
   "is expensive to verify?",
   "Why is the winding number more robust than ray parity, and what does the "
   "generalised version add?",
   "Name the four steps of a mesh boolean and say which one fails.",
   "Why are degeneracies the common case rather than an edge case?",
   "What specifically goes wrong when a geometric predicate is answered "
   "inconsistently?",
   "What do exact predicates compute exactly, and why is that sufficient?",
   "Give a situation where voxelising is the correct engineering choice.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "Deformation and Shape Editing",
 "subtitle": "Moving a handle and having the rest follow sensibly.",
 "question": "How do you edit a shape while preserving its detail?",
 "outcomes": [
     "Explain differential coordinates and why they encode detail.",
     "Implement Laplacian surface editing.",
     "Explain the rotation problem and how ARAP solves it.",
     "Explain cage-based and skeleton-based deformation.",
     "Choose a deformation method for a given task.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The problem",
   "blurb": "Absolute positions are the wrong thing to preserve."},

  {"t": "callout", "title": "Why naive editing destroys detail",
   "kind": "The difficulty",
   "body": ["Move one vertex and smoothly fall off the displacement to its "
            "neighbours. The result is a smooth bump — and every surface "
            "feature inside the affected region is flattened by it.",
            "The problem is that the method preserves <i>absolute "
            "positions</i>, weighted by distance, and detail is not stored in "
            "absolute positions.",
            "Detail is <b>local</b>: the way each vertex sits relative to its "
            "neighbours. Wrinkles, pores, and creases are deviations from the "
            "local average.",
            "So preserve the <i>differential</i> quantity and let absolute "
            "positions fall where they must."]},

  {"t": "eq", "kicker": "Differential coordinates", "title": "Detail is the Laplacian",
   "eqs": [
     ("δᵢ  =  (Δx)ᵢ  =  xᵢ − Σ wᵢⱼ xⱼ",
      "How far vertex i is from the average of its neighbours."),
     ("δ encodes <b>local shape</b>",
      "Large where there is detail; zero on a flat region."),
     ("edit: minimise ‖Δx′ − δ‖²  subject to handle constraints",
      "Keep the detail, satisfy the handles, let everything else move."),
   ],
   "caption": "This is the Module 08 Laplacian again, now as a "
              "representation of shape rather than an operator to apply.",
   "note": "Framing δ as 'the thing to preserve' rather than 'the thing "
           "to minimise' is the conceptual shift of the module."},

  {"t": "section", "label": "Part 2", "title": "Laplacian editing",
   "blurb": "One sparse least-squares system."},

  {"t": "code", "kicker": "The method", "title": "Laplacian surface editing",
   "lang": "text", "code": """
1. Compute delta = L * x        (the original differential coords)

2. Build the least-squares system:

       [    L    ]           [  delta  ]
       [ w * C   ]  x'  =    [ w * p   ]

   where C selects constrained (handle) vertices
         p are their target positions
         w is a large weight -- soft constraints

3. Solve the normal equations:

       (L^T L + w^2 C^T C) x'  =  L^T delta + w^2 C^T p

   Symmetric positive definite -> sparse Cholesky.
   Factor ONCE; re-solve per handle move -> interactive.
""",
   "caption": "The factorisation depends only on connectivity and the "
              "constraint <i>set</i>, not on the handle positions — "
              "which is what makes dragging interactive.",
   "note": "Factor-once-solve-many from Module 08, delivering real-time "
           "editing. The payoff is concrete here."},

  {"t": "callout", "title": "The rotation problem", "kind": "Where it fails",
   "body": ["δ is a <b>vector</b>, expressed in world coordinates. If "
            "you rotate part of the surface, the detail vectors should rotate "
            "with it.",
            "The linear system does not know that. It tries to preserve "
            "δ as a fixed world-space vector, so under large rotations "
            "the detail is preserved in the <i>wrong orientation</i>.",
            "A bent arm shows wrinkles pointing the way they did before the "
            "bend — unmistakably wrong, and the characteristic artifact "
            "of linear Laplacian editing.",
            "Small deformations are fine. Large rotations are not."]},

  {"t": "section", "label": "Part 3", "title": "ARAP",
   "blurb": "As-rigid-as-possible: solve for the rotations too."},

  {"t": "bullets", "kicker": "ARAP", "title": "Local/global alternation",
   "items": [
     "Allow each vertex a local rotation Rᵢ, and ask that each one-ring "
     "deform as rigidly as possible.",
     "",
     "Minimise Σᵢ Σⱼ wᵢⱼ ‖(xᵢ′ "
     "− xⱼ′) − Rᵢ(xᵢ − xⱼ)‖²",
     "",
     "<b>Nonlinear</b> — but it alternates cleanly:",
     ("<b>Local:</b> fix positions, solve each Rᵢ by SVD. Independent, "
      "parallel, closed-form.", 1),
     ("<b>Global:</b> fix rotations, solve for positions — the same "
      "sparse system as before.", 1),
     "",
     "Converges in a handful of iterations. <b>Same factorisation reused "
     "throughout.</b>",
   ],
   "note": "The local step being a closed-form SVD per vertex is what makes "
           "ARAP practical. It is not a general nonlinear solve."},

  {"t": "code", "kicker": "ARAP", "title": "The local step: optimal rotation by SVD",
   "lang": "cpp", "code": """
// For each vertex: find the rotation best matching the original
// one-ring to the deformed one. This is the orthogonal Procrustes
// problem, and it has a closed-form answer.

Matrix3d S = Matrix3d::Zero();
for (j : one_ring(i))
    S += w(i,j) * (x[i] - x[j]) * (xp[i] - xp[j]).transpose();

JacobiSVD<Matrix3d> svd(S, ComputeFullU | ComputeFullV);
Matrix3d R = svd.matrixV() * svd.matrixU().transpose();

if (R.determinant() < 0) {          // guard against a REFLECTION
    Matrix3d V = svd.matrixV();
    V.col(2) *= -1;                 // flip the smallest singular vector
    R = V * svd.matrixU().transpose();
}
""",
   "caption": "The determinant guard is essential — without it the "
              "'rotation' can be a reflection, which inverts the surface "
              "locally.",
   "note": "The reflection case is a classic bug and produces inside-out "
           "patches that are baffling without this context."},

  {"t": "section", "label": "Part 4", "title": "Other deformation methods",
   "blurb": "Not everything needs a linear solve."},

  {"t": "table", "kicker": "Methods", "title": "The deformation toolkit",
   "header": ["Method", "Control", "Best for"],
   "widths": [2.8, 4.4, 4.9],
   "rows": [
     ["Laplacian / ARAP", "Direct handles on the surface", "Detail-preserving editing"],
     ["Cage (MVC, harmonic)", "A coarse enclosing polyhedron", "Smooth global deformation"],
     ["Skeleton (LBS)", "A bone hierarchy", "Character animation — CSCE 641 Mod 13"],
     ["Free-form (FFD)", "A lattice of control points", "Simple global warps"],
     ["Blend shapes", "Interpolation of sculpted targets", "Faces; exactly authored results"],
   ],
   "note": "Blend shapes are the one artists trust most, because the result "
           "is exactly what was sculpted."},

  {"t": "callout", "title": "This is where CSCE 641 Module 13 connects",
   "kind": "The link",
   "body": ["Linear blend skinning averages <b>matrices</b>, which is why it "
            "produces the candy-wrapper collapse under large twists.",
            "The ARAP local step shows the principled alternative: recover "
            "the best <i>rotation</i> and apply that, rather than averaging "
            "the matrices that represent rotations.",
            "Dual-quaternion skinning is the real-time version of the same "
            "insight — interpolate the transformations rather than their "
            "matrix representations.",
            "Same problem, two courses, one idea: <b>rotations do not "
            "average linearly</b>, and every good method respects that."]},

  {"t": "bullets", "kicker": "End", "title": "Where this course leaves you",
   "items": [
     "You can build a half-edge mesh and trust it on real, broken data.",
     "You can compute curvature and verify it against Gauss–Bonnet.",
     "You can build the Laplacian and use it for smoothing, "
     "parameterisation, and deformation — one matrix, three problems.",
     "You can simplify, remesh, and unwrap an asset into something an engine "
     "can load.",
     "",
     "<b>CSCE 647</b> renders these surfaces with real light transport.",
     "<b>CSCE 649</b> makes them move under physics.",
     "<b>CSCE 748</b> captures them from photographs.",
   ]},
 ],
 "takeaways": [
   "Detail lives in <i>differential</i> coordinates — how a vertex sits "
   "relative to its neighbours — not in absolute positions.",
   "δ = Δx is the Module 08 Laplacian used as a representation of "
   "shape rather than as an operator.",
   "Laplacian editing is one sparse least-squares solve, and the "
   "factorisation is reusable across handle moves — hence interactive "
   "dragging.",
   "δ is a world-space vector, so linear Laplacian editing preserves "
   "detail in the wrong orientation under large rotations.",
   "ARAP solves for rotations too, alternating a closed-form per-vertex SVD "
   "with the same global sparse solve. Guard against reflections.",
   "Rotations do not average linearly — the same insight that explains "
   "candy-wrapper skinning in CSCE 641 Module 13.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why naive editing fails"),
  ("p", "The obvious approach to interactive editing is to displace a handle "
        "vertex and fall the displacement off smoothly over a neighbourhood. "
        "The result is a smooth bump, and every surface feature inside the "
        "affected region is flattened by it."),
  ("callout", "Detail is not stored in absolute positions",
   ["Wrinkles, pores, creases, and tooling marks are <b>local</b> phenomena: "
    "each vertex sits a particular way relative to its immediate neighbours. "
    "That relationship is the detail.",
    "Smoothly interpolating absolute positions preserves the large-scale "
    "shape and destroys the local relationships, which is exactly backwards.",
    "The fix is to make the <i>differential</i> quantity the thing you "
    "preserve, and let absolute positions go wherever satisfying the "
    "constraints requires."]),
  ("eq", "&delta;<sub>i</sub> = (&Delta;x)<sub>i</sub> = x<sub>i</sub> &minus; &Sigma;<sub>j</sub> w<sub>ij</sub> x<sub>j</sub>"),
  ("p", "This is the Laplacian of position from Module 08, now read "
        "differently: not as an operator to apply but as a <b>representation "
        "of shape</b>. &delta; is large where the surface deviates from its "
        "local average — that is, where there is detail — and zero "
        "on a flat region. And by Module 07, &delta; = 2Hn, so it encodes "
        "mean curvature directly."),

  ("h1", "2 &nbsp; Laplacian surface editing"),
  ("p", "Find new positions x&prime; that reproduce the original differential "
        "coordinates as closely as possible, while satisfying the handle "
        "constraints."),
  ("eq", "minimise &#8741;&Delta;x&prime; &minus; &delta;&#8741;&#178; &nbsp; subject to &nbsp; x&prime;<sub>handles</sub> = p"),
  ("code", """// Stacked least-squares system, with soft constraints:
//
//     [   L   ]          [  delta  ]
//     [ w * C ]  x'  =   [  w * p  ]
//
// Normal equations:
//     (L^T L + w^2 C^T C) x' = L^T delta + w^2 C^T p
//
// Symmetric positive definite -> sparse Cholesky."""),
  ("callout", "Factor once, drag interactively",
   ["The system matrix L&#7488;L + w&#178;C&#7488;C depends only on the mesh "
    "connectivity, the weights, and <i>which</i> vertices are constrained "
    "— not on <i>where</i> those vertices are being moved to.",
    "So the expensive Cholesky factorisation is computed once when the user "
    "selects a handle, and each frame of dragging requires only a back "
    "substitution against a new right-hand side.",
    "This is the Module 08 pattern delivering its clearest payoff: a solve "
    "that would take seconds becomes a few milliseconds, and detail-"
    "preserving editing becomes genuinely interactive. It is why this "
    "formulation found its way into modelling packages."]),
  ("h2", "2.1 &nbsp; The rotation problem"),
  ("callout", "&delta; is a world-space vector, and that is the flaw",
   ["The differential coordinate is a vector expressed in global coordinates. "
    "If part of the surface rotates, the detail vectors ought to rotate with "
    "it — a wrinkle on a bending arm should bend too.",
    "The linear system has no way to express that. It preserves &delta; as a "
    "fixed world-space vector, so under a large rotation the detail is "
    "faithfully reproduced in entirely the wrong orientation.",
    "The artifact is distinctive: bend a cylinder sharply and the surface "
    "features point the way they did before the bend, as though the detail "
    "had been painted on and the paint had not moved.",
    "For small deformations this is invisible and the linear method is "
    "excellent. For large rotations it is unusable, which is what motivates "
    "&sect;3."]),

  ("break",),
  ("h1", "3 &nbsp; As-rigid-as-possible deformation"),
  ("p", "Allow each vertex an unknown local rotation R<sub>i</sub>, and ask "
        "that each one-ring neighbourhood deform as close to rigidly as the "
        "constraints permit."),
  ("eq", "E = &Sigma;<sub>i</sub> &Sigma;<sub>j&isin;N(i)</sub> w<sub>ij</sub> &#8741;(x&prime;<sub>i</sub> &minus; x&prime;<sub>j</sub>) &minus; R<sub>i</sub>(x<sub>i</sub> &minus; x<sub>j</sub>)&#8741;&#178;"),
  ("p", "This is nonlinear — both the positions and the rotations are "
        "unknown — but it has a structure that makes it tractable: fixing "
        "either set makes solving for the other easy."),
  ("h2", "3.1 &nbsp; The local step"),
  ("p", "With positions fixed, each R<sub>i</sub> is independent and has a "
        "closed-form solution. Finding the rotation that best aligns one set "
        "of vectors with another is the <b>orthogonal Procrustes problem</b>, "
        "solved by an SVD of the covariance matrix."),
  ("code", """Matrix3d S = Matrix3d::Zero();
for (int j : one_ring(i))
    S += w(i,j) * (x[i] - x[j]) * (xp[i] - xp[j]).transpose();

JacobiSVD<Matrix3d> svd(S, ComputeFullU | ComputeFullV);
Matrix3d R = svd.matrixV() * svd.matrixU().transpose();

if (R.determinant() < 0) {          // reflection, not rotation
    Matrix3d V = svd.matrixV();
    V.col(2) *= -1;                 // flip the least significant axis
    R = V * svd.matrixU().transpose();
}"""),
  ("callout", "The determinant guard is not optional",
   ["V U&#7488; is orthogonal, which means it is either a rotation "
    "(determinant +1) or a <b>reflection</b> (determinant &minus;1).",
    "Under strong compression or a nearly degenerate configuration, the SVD "
    "can produce a reflection. Applying it turns that patch of surface "
    "inside out, producing locally inverted geometry that shades black and "
    "self-intersects.",
    "Flipping the sign of the column corresponding to the smallest singular "
    "value yields the closest genuine rotation. Omitting this check is a "
    "classic bug, and the symptom — isolated inverted patches appearing "
    "under large deformation — is baffling without knowing the cause."]),
  ("h2", "3.2 &nbsp; The global step"),
  ("p", "With rotations fixed, the energy is quadratic in the positions and "
        "its minimiser solves a sparse linear system — the <i>same</i> "
        "Laplacian system as before, with rotated differential coordinates on "
        "the right-hand side."),
  ("p", "Alternate the two steps. The energy decreases monotonically and the "
        "process typically converges in three to ten iterations. Crucially, "
        "the system matrix is unchanged throughout, so <b>one factorisation "
        "serves every iteration and every frame of dragging</b>. ARAP is "
        "therefore interactive despite being nonlinear, which is the reason "
        "it became the standard method."),

  ("h1", "4 &nbsp; The wider toolkit"),
  ("table", ["Method", "How it is controlled", "Suited to"],
   [["<b>Laplacian / ARAP</b>", "Handles placed directly on the surface.",
     "Detail-preserving editing of scanned or sculpted models."],
    ["<b>Cage-based</b> (mean value or harmonic coordinates)",
     "A coarse polyhedron enclosing the model; moving cage vertices deforms "
     "everything inside smoothly.",
     "Smooth large-scale deformation. Cheap to evaluate once the coordinates "
     "are precomputed."],
    ["<b>Skeleton / linear blend skinning</b>", "A bone hierarchy with "
     "per-vertex weights.",
     "Character animation. CSCE 641 Module 13."],
    ["<b>Free-form deformation</b>", "A lattice of control points, with the "
     "model embedded in a trivariate B&eacute;zier or B-spline volume.",
     "Simple global warps: squash, stretch, bend. Historically the first "
     "practical method."],
    ["<b>Blend shapes</b>", "Linear interpolation between explicitly "
     "sculpted target shapes.",
     "Facial animation. The result is exactly what an artist sculpted, which "
     "is why it remains dominant where appearance is critical."]],
   [0.21, 0.40, 0.39]),
  ("callout", "The idea this course shares with CSCE 641",
   ["Linear blend skinning averages <b>transformation matrices</b>, and "
    "CSCE 641 Module 13 showed the consequence: the average of two rotation "
    "matrices 180&deg; apart is degenerate, so a twisted wrist collapses "
    "— the candy-wrapper artifact.",
    "The ARAP local step is the principled alternative stated plainly: do not "
    "average the matrices, <i>recover the best rotation</i> and apply that. "
    "The SVD is precisely the operation that extracts a rotation from "
    "something that is nearly one.",
    "Dual-quaternion skinning is the real-time version of the same insight "
    "— interpolate the transformations rather than their matrix "
    "representations.",
    "Two courses, two contexts, one fact: <b>rotations do not average "
    "linearly</b>, and every method that works respects that."]),

  ("h1", "5 &nbsp; Where this leaves you"),
  ("p", "You can build a half-edge mesh and have it survive real, broken, "
        "scanned input. You can compute discrete curvature and verify it "
        "against a theorem rather than against intuition. You can build the "
        "cotangent Laplacian and use the same matrix for smoothing, for "
        "parameterisation, and for deformation — and you understand why "
        "one matrix serves all three. You can simplify, remesh, and unwrap an "
        "asset into something an engine will actually load."),
  ("p", "That is a geometry processing library you wrote and understand "
        "completely, which is a far better foundation than familiarity with "
        "someone else's. The remaining track courses build directly on it: "
        "<b>CSCE 647</b> renders these surfaces with physically correct light "
        "transport; <b>CSCE 649</b> makes them move under simulated physics; "
        "<b>CSCE 748</b> reconstructs them from photographs."),
 ],
 "resources": [
   ("Sorkine & Alexa — As-Rigid-As-Possible Surface Modeling (free)",
    "https://igl.ethz.ch/projects/ARAP/arap_web.pdf",
    "The ARAP paper. Short, clearly written, and directly implementable from "
    "the text."),
   ("Sorkine et al. — Laplacian Surface Editing (free)",
    "https://igl.ethz.ch/projects/Laplacian-mesh-processing/",
    "The linear method and the rotation problem, by the people who developed "
    "it."),
   ("Keenan Crane — DDG, the deformation material",
    "https://brickisland.net/ddg-web/",
    "Deformation framed in terms of the operators developed through the "
    "course."),
   ("libigl tutorial — deformation chapter",
    "https://libigl.github.io/tutorial/",
    "Working ARAP, biharmonic, and cage-based deformation to compare against "
    "your own."),
 ],
 "exercises": [
   "Implement naive editing with smooth falloff and capture the destruction "
   "of surface detail on a scanned model.",
   "Implement linear Laplacian editing. Confirm that detail is preserved "
   "under translation of a handle.",
   "Demonstrate the rotation problem: rotate a handle by 90&deg; and capture "
   "the detail preserved in the wrong orientation.",
   "Implement ARAP with the local SVD step and the global solve. Compare "
   "against the linear method under the same large rotation.",
   "Remove the determinant guard from the SVD step and find a deformation "
   "that produces an inverted patch. Capture it.",
   "Measure interactivity: time the factorisation and the per-drag solve "
   "separately on a 100,000-vertex mesh, and confirm dragging is "
   "interactive.",
   "Implement cage-based deformation with mean value coordinates and compare "
   "the result and the cost against ARAP on the same model.",
   "<b>Project 2 is now due.</b> Complete the simplification, "
   "parameterisation, and remeshing pipeline described in the syllabus, with "
   "a baked normal map and everything rendered in your CSCE 641 renderer.",
 ],
 "selfcheck": [
   "Why does smoothly interpolating absolute positions destroy detail?",
   "What are differential coordinates, and what earlier operator are they?",
   "Why can the Laplacian editing factorisation be reused across handle "
   "moves?",
   "Explain the rotation problem and describe its visual signature.",
   "Describe the ARAP local and global steps, and say why the method is "
   "interactive despite being nonlinear.",
   "Why must the determinant of the SVD result be checked, and what happens "
   "if you skip it?",
   "What single fact about rotations connects this module to CSCE 641 "
   "Module 13?",
 ],
},

]
