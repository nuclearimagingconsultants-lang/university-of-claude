# -*- coding: utf-8 -*-
"""CSCE 641 — Modules 08-10."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Texture Mapping, Filtering, and Mipmaps",
 "subtitle": "Putting detail on surfaces without putting geometry there.",
 "question": "How do you map an image onto a surface without shimmering?",
 "outcomes": [
     "Explain UV parameterisation and the artifacts of a bad one.",
     "Choose correctly between magnification and minification filters.",
     "Explain why mipmaps exist in sampling terms, and what trilinear and "
     "anisotropic filtering each fix.",
     "Implement tangent-space normal mapping correctly.",
     "Name the common texture types and say which are colour and which are "
     "data.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Parameterisation",
   "blurb": "Assigning a 2D coordinate to every point on a 3D surface."},

  {"t": "bullets", "kicker": "UVs", "title": "What a UV map is",
   "items": [
     "Each vertex carries a 2D coordinate (u, v) into texture space.",
     "The rasterizer interpolates it — perspective-correctly, per "
     "Module 04.",
     "",
     "Making a good UV map is <b>flattening a 3D surface onto a plane</b>.",
     ("Only developable surfaces flatten without distortion.", 1),
     ("A sphere does not. Neither does almost anything interesting.", 1),
     "",
     "So every UV map trades off three things: <b>stretch</b>, <b>seams</b>, "
     "and <b>wasted texture space</b>.",
     ("You cannot have none of them. Module 12 revisits this properly.", 1),
   ],
   "note": "The map-projection analogy lands well: Mercator preserves angles "
           "and ruins areas, and UV unwrapping faces exactly that trade."},

  {"t": "table", "kicker": "UVs", "title": "Wrap modes, and when each is right",
   "header": ["Mode", "Behaviour outside [0,1]", "Use for"],
   "widths": [2.8, 4.5, 4.8],
   "rows": [
     ["Repeat", "Tiles seamlessly", "Floors, walls, any tiling detail"],
     ["Mirrored repeat", "Tiles, flipping alternately", "Hides a seam in a tiling texture"],
     ["Clamp to edge", "Holds the border texel", "Decals, UI, anything not meant to tile"],
     ["Clamp to border", "Returns a constant colour", "Shadow maps — border = 'fully lit'"],
   ],
   "note": "The shadow-map use of clamp-to-border matters in Module 10: it "
           "decides what happens outside the light's frustum."},

  {"t": "section", "label": "Part 2", "title": "Filtering",
   "blurb": "The texture is a grid of samples. The screen is a different grid "
            "of samples. These rarely line up."},

  {"t": "two", "kicker": "Two failure directions", "title": "Magnification and minification",
   "lh": "Magnification — texels larger than pixels",
   "l": ["One texel covers many pixels.",
         "Problem: <b>blockiness</b>.",
         "Nearest → hard squares.",
         "Bilinear → smooth, slightly soft.",
         ("Easy case. Bilinear is almost always right.", 1)],
   "rh": "Minification — texels smaller than pixels",
   "r": ["Many texels fall inside one pixel.",
         "Problem: <b>aliasing</b> — shimmer and moiré.",
         "Point sampling picks one texel arbitrarily.",
         "The pixel moves, a different texel is picked, it flickers.",
         ("Hard case. This is what mipmaps exist for.", 1)],
   "note": "Press the asymmetry: magnification is a resolution problem "
           "(annoying), minification is a sampling problem (actually broken)."},

  {"t": "callout", "title": "Minification is undersampling", "kind": "Key idea",
   "body": ["A pixel covers an area of the texture. Its correct value is the "
            "<i>average</i> over that area.",
            "Point sampling takes one texel from that area and pretends it "
            "represents the whole. When the pixel moves slightly, a different "
            "texel is chosen, and the result flickers.",
            "This is the Module 01 theme again: a continuous signal sampled "
            "too sparsely. Module 09 gives the theory; mipmapping is the "
            "practical fix."]},

  {"t": "bullets", "kicker": "Mipmaps", "title": "Precompute the averages",
   "items": [
     "Store the texture at every power-of-two reduction: full, 1/2, 1/4, "
     "1/8…",
     "Each level is a prefiltered average of the one above it.",
     "",
     "At render time, pick the level where <b>one texel ≈ one pixel</b>.",
     ("The averaging you needed has already been done, offline.", 1),
     "",
     "Costs 33% more memory. ∑ 1/4ⁿ = 4/3.",
     "",
     "Level chosen from the screen-space derivatives of the UV — which "
     "is why Module 07's 2×2 quads exist.",
   ]},

  {"t": "eq", "kicker": "Mipmaps", "title": "Choosing the level",
   "eqs": [
     ("ρ  =  max( |∂uv/∂x| , |∂uv/∂y| )",
      "How far the texture coordinate moves per pixel step, in texels."),
     ("level  =  log₂(ρ)",
      "Each mip level halves resolution, so the log is the natural measure."),
     ("trilinear: lerp between ⌊level⌋ and ⌈level⌉",
      "Removes the visible seam where the level changes."),
   ],
   "caption": "Derivatives come from neighbouring threads in the quad — "
              "hence undefined behaviour if you sample inside divergent "
              "control flow.",
   "note": "This closes the loop with Module 07 nicely. The quad is not an "
           "implementation curiosity; mipmapping depends on it."},

  {"t": "table", "kicker": "Filtering", "title": "What each filter fixes",
   "header": ["Filter", "Fixes", "Remaining problem", "Cost"],
   "widths": [2.6, 3.5, 3.9, 2.1],
   "rows": [
     ["Nearest", "Nothing", "Blocky and aliased", "1 tap"],
     ["Bilinear", "Blockiness within a level", "Still aliases on minification", "4 taps"],
     ["Bilinear + mipmap", "Aliasing", "Visible seams between levels", "4 taps"],
     ["Trilinear", "Level seams", "Over-blurs at oblique angles", "8 taps"],
     ["Anisotropic", "Oblique over-blur", "Cost; usually capped at 16×", "up to 16×"],
   ],
   "note": "Each row fixes the previous row's residual. That progression is "
           "the whole story of texture filtering."},

  {"t": "callout", "title": "Why trilinear blurs oblique surfaces",
   "kind": "The anisotropy problem",
   "body": ["A pixel on a floor seen at a shallow angle covers a long, thin "
            "footprint in texture space — perhaps 1 texel wide and 16 "
            "long.",
            "Mip level selection takes the <i>maximum</i> derivative, so it "
            "picks a level coarse enough for the long axis. The short axis is "
            "then blurred by 16× more than it needed.",
            "Result: distant floors look smeared. Anisotropic filtering takes "
            "several samples along the long axis at a finer level instead, "
            "which is why it has such a visible effect on ground textures for "
            "such a modest cost."]},

  {"t": "section", "label": "Part 3", "title": "Normal mapping",
   "blurb": "Faking geometry that is not there, convincingly."},

  {"t": "bullets", "kicker": "Normal maps", "title": "Perturb the normal, not the surface",
   "items": [
     "Store a normal per texel instead of a colour.",
     "Use it in the lighting equation in place of the interpolated normal.",
     "",
     "Lighting responds as though the surface had that shape.",
     ("Bumps, scratches, pores — at texture resolution, for no extra "
      "geometry.", 1),
     "",
     "<b>But the silhouette does not change.</b>",
     ("Look along the surface and it is visibly flat. This is the one "
      "limitation that nothing fixes.", 1),
   ]},

  {"t": "bullets", "kicker": "Tangent space", "title": "Why normals are stored in tangent space",
   "items": [
     "Object-space normal maps bake in the orientation of the mesh.",
     ("Cannot be reused on another model. Cannot tile. Breaks under "
      "deformation.", 1),
     "",
     "Tangent-space maps store the normal <i>relative to the surface</i>.",
     ("Reusable, tileable, and correct under skinning — which matters "
      "in Module 13.", 1),
     ("Mostly blue, because (0,0,1) means 'unperturbed'.", 1),
     "",
     "Needs a per-vertex frame: tangent, bitangent, normal — the TBN "
     "matrix.",
   ]},

  {"t": "code", "kicker": "Tangent space", "title": "Applying a normal map",
   "lang": "glsl", "code": """
// Vertex shader: build the TBN basis and pass it along.
vec3 T = normalize(uNormalMatrix * aTangent);
vec3 N = normalize(uNormalMatrix * aNormal);
T = normalize(T - dot(T, N) * N);     // Gram-Schmidt: re-orthogonalise,
                                      // because interpolation drifts
vec3 B = cross(N, T) * aTangent.w;    // w stores handedness (+1 / -1)
vTBN = mat3(T, B, N);

// Fragment shader
vec3 n = texture(uNormalMap, vUV).rgb * 2.0 - 1.0;   // [0,1] -> [-1,1]
vec3 N = normalize(vTBN * n);                        // -> world space
""",
   "caption": "Two details that are routinely wrong: the handedness in "
              "tangent.w (mirrored UVs flip it, and without it mirrored parts "
              "light inside out), and the Gram–Schmidt step.",
   "note": "Mirrored UV islands are extremely common in game assets — "
           "character faces especially. The handedness bug shows up as one "
           "cheek lit wrong."},

  {"t": "table", "kicker": "Reference", "title": "Texture types and colour space",
   "header": ["Map", "Stores", "Colour space"],
   "widths": [3.2, 5.6, 3.3],
   "rows": [
     ["Albedo / base colour", "Surface colour with no lighting baked in", "<b>sRGB</b>"],
     ["Normal", "Tangent-space normal, encoded to [0,1]", "Linear — never sRGB"],
     ["Roughness", "Microfacet spread (Module 11)", "Linear"],
     ["Metallic", "Dielectric or conductor, usually 0 or 1", "Linear"],
     ["Ambient occlusion", "Local self-shadowing factor", "Linear"],
     ["Emissive", "Light emitted by the surface itself", "<b>sRGB</b>"],
     ["Height / displacement", "Offset along the normal", "Linear"],
   ],
   "note": "This table is the practical form of Module 06's gamma rule. "
           "Colour is sRGB; everything else is data."},
 ],
 "takeaways": [
   "UV mapping is flattening a surface onto a plane: stretch, seams, and "
   "wasted space are a three-way trade you cannot escape.",
   "Magnification is a resolution problem; minification is a sampling "
   "problem. Only the second one actually breaks.",
   "Mipmaps precompute the averages that correct minification aliasing, for "
   "33% extra memory.",
   "Mip level comes from screen-space UV derivatives, which is why fragments "
   "shade in 2×2 quads.",
   "Trilinear over-blurs oblique surfaces because level selection uses the "
   "maximum derivative; anisotropic filtering is the fix.",
   "Tangent-space normal maps are reusable and survive deformation, but need "
   "a correct TBN including handedness.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Parameterisation"),
  ("p", "A texture is an image; a surface is a 2D manifold embedded in 3D. "
        "Texture mapping needs a function from the surface to the image "
        "plane, and supplying it per vertex as a (u, v) coordinate, then "
        "interpolating, is the standard approach. Module 04 already "
        "established that the interpolation must be perspective-correct."),
  ("p", "Constructing a good UV map is the problem of flattening a curved "
        "surface onto a plane, and it is exactly the problem cartographers "
        "have. Only <i>developable</i> surfaces — cylinders, cones "
        "— flatten without distortion. A sphere does not, which is why "
        "every world map distorts something. Three costs trade against each "
        "other:"),
  ("ul", ["<b>Stretch.</b> Texels cover unequal areas of the surface, so "
          "detail density varies visibly.",
          "<b>Seams.</b> Cuts in the UV layout. Across a seam, filtering and "
          "mipmapping break down and a visible line appears.",
          "<b>Wasted space.</b> Gaps between UV islands are texture memory "
          "that holds nothing."]),
  ("p", "You cannot eliminate all three. Module 12 returns to this with the "
        "geometry-processing tools to reason about it properly."),
  ("h2", "1.1 &nbsp; Wrap modes"),
  ("table", ["Mode", "Outside [0,1]", "Typical use"],
   [["<code>REPEAT</code>", "Fractional part; tiles infinitely",
     "Floors, walls, fabric — any tiling detail."],
    ["<code>MIRRORED_REPEAT</code>", "Tiles with alternate flipping",
     "Hides the seam of a texture that does not tile perfectly."],
    ["<code>CLAMP_TO_EDGE</code>", "Holds the edge texel",
     "Decals, UI, skyboxes. Prevents bleeding from the opposite edge."],
    ["<code>CLAMP_TO_BORDER</code>", "Returns a specified constant",
     "Shadow maps (Module 10): a border of 'fully lit' means geometry "
     "outside the light's frustum is not spuriously shadowed."]],
   [0.24, 0.30, 0.46]),

  ("h1", "2 &nbsp; Filtering"),
  ("p", "A texture is a grid of samples. The screen is a different grid of "
        "samples. They almost never align, and the two ways they fail to "
        "align are qualitatively different problems."),
  ("h2", "2.1 &nbsp; Magnification"),
  ("p", "When texels are larger than pixels, several pixels fall inside one "
        "texel. Nearest-neighbour sampling produces visible squares; bilinear "
        "interpolation between the four nearest texels produces a smooth, "
        "slightly soft result. This is a resolution problem: there genuinely "
        "is not enough information, and all you can do is interpolate "
        "plausibly. It is annoying but not broken, and bilinear is almost "
        "always the right answer."),
  ("h2", "2.2 &nbsp; Minification"),
  ("p", "When texels are smaller than pixels, many texels fall inside one "
        "pixel. The pixel's correct value is the <i>average</i> of the "
        "texture over its footprint. Point sampling instead picks one texel "
        "from that footprint and treats it as representative."),
  ("callout", "Why that flickers",
   ["Move the camera slightly. The footprint shifts, a different texel is "
    "selected, and the pixel's colour jumps — with no relation to the "
    "actual average, which barely changed.",
    "Across a whole surface this produces shimmering, crawling, and "
    "moir&eacute; patterns on regular detail like brickwork or a "
    "checkerboard. It is at its worst exactly where it is most visible: "
    "distant ground planes in motion.",
    "This is undersampling — the same phenomenon as the jagged edges of "
    "Module 01 and the vanishing highlights of Module 06. Module 09 develops "
    "the theory."]),

  ("h1", "3 &nbsp; Mipmapping"),
  ("p", "The correct value is an average over the pixel's footprint. "
        "Computing that average at render time would require reading every "
        "texel in the footprint — potentially thousands. The solution is "
        "to precompute the averages."),
  ("p", "A <b>mipmap</b> is a chain of progressively halved versions of the "
        "texture, each level the filtered average of the one above. At render "
        "time, select the level at which one texel corresponds to "
        "approximately one pixel, and the averaging has already been done "
        "offline. The storage cost is the geometric series "
        "1 + 1/4 + 1/16 + &hellip; = 4/3: just 33% extra."),
  ("h2", "3.1 &nbsp; Level selection"),
  ("eq", "&rho; = max( |&part;(u,v)/&part;x|, |&part;(u,v)/&part;y| ) &nbsp;&nbsp;&nbsp; level = log&#8322;&rho;"),
  ("p", "The derivatives are computed from neighbouring threads in the "
        "2&times;2 quad, which is the mechanism Module 07 described. This is "
        "the reason that quad exists, and the reason that sampling a texture "
        "inside non-uniform control flow has undefined results: the "
        "neighbouring threads may not have executed the sample, so there is "
        "nothing to difference against."),
  ("p", "Selecting a single integer level produces a visible band where the "
        "level changes. <b>Trilinear</b> filtering samples the two "
        "neighbouring levels bilinearly and interpolates between them, "
        "removing the band for eight taps instead of four."),
  ("h2", "3.2 &nbsp; Anisotropy"),
  ("p", "Level selection takes the <i>maximum</i> of the two derivatives, "
        "which is correct only when the pixel's texture-space footprint is "
        "roughly square. On a surface seen at a shallow angle it is not: the "
        "footprint is a long thin quadrilateral, perhaps one texel across and "
        "sixteen long."),
  ("p", "Taking the maximum selects a level coarse enough for the long axis, "
        "and the short axis is then blurred sixteen times more than necessary. "
        "The surface looks correct in the direction it is stretched and "
        "smeared across it. This is why untreated floors in older games go "
        "mushy in the distance."),
  ("p", "<b>Anisotropic filtering</b> instead takes several samples along the "
        "long axis of the footprint, at a level appropriate to the "
        "<i>short</i> axis. Sixteen-tap anisotropic filtering costs four times "
        "trilinear and transforms the appearance of ground planes, which is "
        "why it is historically the single highest-value graphics setting per "
        "unit of performance."),

  ("break",),
  ("h1", "4 &nbsp; Normal mapping"),
  ("p", "Geometric detail is expensive: more triangles means more vertex "
        "work, more memory, and smaller triangles (which Module 07 showed are "
        "disproportionately costly because of quad overshading). Normal "
        "mapping provides the <i>appearance</i> of fine geometric detail "
        "without the geometry, by perturbing the normal used for lighting."),
  ("p", "Because almost all shading depends on the normal — the cosine "
        "law, the specular lobe, the Fresnel term — changing the normal "
        "changes the lighting exactly as though the surface had that shape. "
        "Bumps, scratches, fabric weave, and skin pores all become texture "
        "resolution rather than geometry."),
  ("callout", "The one thing it cannot do",
   ["The silhouette is unchanged. Viewed edge-on, a normal-mapped brick wall "
    "is visibly a flat plane with no bricks protruding.",
    "Parallax occlusion mapping and displacement mapping address this at "
    "greater cost. Nothing fixes it for free, and knowing the limit tells you "
    "when to spend real geometry."]),
  ("h2", "4.1 &nbsp; Tangent space"),
  ("p", "A normal map could store normals in object space, but then the map "
        "is tied to one specific mesh in one specific pose: it cannot be "
        "reused, cannot tile, and is wrong the moment the surface deforms "
        "under skinning (Module 13)."),
  ("p", "<b>Tangent space</b> stores the normal relative to the surface "
        "itself: Z along the surface normal, X and Y along the directions in "
        "which u and v increase. An unperturbed normal is (0, 0, 1), which "
        "encodes to (0.5, 0.5, 1.0) — hence the characteristic lavender "
        "blue of normal maps. Such a map is reusable across models, tileable, "
        "and correct under arbitrary deformation."),
  ("h2", "4.2 &nbsp; Building the TBN"),
  ("code", """// Vertex shader
vec3 T = normalize(uNormalMatrix * aTangent.xyz);
vec3 N = normalize(uNormalMatrix * aNormal);

// Gram-Schmidt: interpolation and the normal matrix both cause T to
// drift out of perpendicularity with N. Re-orthogonalise.
T = normalize(T - dot(T, N) * N);

// aTangent.w carries handedness, +1 or -1. Mirrored UV islands have
// the opposite handedness, and without this they light inside out.
vec3 B = cross(N, T) * aTangent.w;

vTBN = mat3(T, B, N);

// Fragment shader
vec3 n = texture(uNormalMap, vUV).rgb * 2.0 - 1.0;  // decode [0,1]->[-1,1]
vec3 N = normalize(vTBN * n);                       // tangent -> world"""),
  ("callout", "Two details that are frequently wrong",
   ["<b>Handedness.</b> Mirroring UV islands is standard practice — a "
    "character's two halves share texture space, which halves memory. "
    "Mirrored islands have reversed handedness, and omitting the w term "
    "lights one side of every mirrored object incorrectly. On a face it is "
    "subtle and deeply confusing.",
    "<b>Gram&ndash;Schmidt.</b> The interpolated tangent is not exactly "
    "perpendicular to the interpolated normal, and the normal matrix can "
    "shear them further apart. Without re-orthogonalisation the basis is "
    "skewed and lighting is subtly wrong across the whole surface."]),

  ("h1", "5 &nbsp; The texture set"),
  ("p", "A physically based material (Module 11) is typically four to six "
        "textures. The critical practical point, carried over from Module 06, "
        "is which are colour and which are data."),
  ("table", ["Map", "Contents", "Space", "Notes"],
   [["Albedo / base colour", "Surface colour, no lighting baked in",
     "<b>sRGB</b>",
     "Must contain no shadows or highlights; those come from lighting."],
    ["Normal", "Tangent-space normal, encoded", "<b>Linear</b>",
     "Tagging this sRGB is the classic subtle bug."],
    ["Roughness", "Microfacet distribution width", "<b>Linear</b>",
     "Often packed into a channel alongside metallic and AO."],
    ["Metallic", "Conductor vs dielectric", "<b>Linear</b>",
     "Physically near-binary; intermediate values usually mean a blend "
     "boundary."],
    ["Ambient occlusion", "Local self-occlusion", "<b>Linear</b>",
     "Applies to ambient and indirect light only, never to direct light."],
    ["Emissive", "Self-emitted light", "<b>sRGB</b>",
     "Added after lighting, not multiplied by it."],
    ["Height", "Offset along the normal", "<b>Linear</b>",
     "For parallax or tessellation displacement."]],
   [0.18, 0.28, 0.12, 0.42]),
 ],
 "resources": [
   ("GAMES101 Lectures 09–10 — Texture Mapping, Advanced Texturing",
    "https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html",
    "Mipmapping derived as a sampling fix, with excellent diagrams of the "
    "anisotropic footprint problem."),
   ("LearnOpenGL — Textures, Normal Mapping, Parallax Mapping",
    "https://learnopengl.com/Advanced-Lighting/Normal-Mapping",
    "Complete working TBN construction including the handedness detail."),
   ("Scratchapixel — Texture Mapping",
    "https://www.scratchapixel.com/",
    "Written treatment with the mip-level derivation in full."),
   ("Nathan Reed — 'Understanding BCn Texture Compression Formats'",
    "https://www.reedbeta.com/blog/understanding-bcn-texture-compression-formats/",
    "Why normal maps use BC5 and colour uses BC7, and what each format "
    "sacrifices. Short, practical, free."),
 ],
 "exercises": [
   "Add texture sampling to your software rasterizer with nearest and "
   "bilinear filtering. Render a textured plane filling the screen with each "
   "and capture the difference.",
   "Build a mipmap chain yourself by repeated box filtering. Implement level "
   "selection from UV derivatives and trilinear interpolation between levels.",
   "Render a large checkerboard floor receding to the horizon with: point "
   "sampling, bilinear, trilinear, and 16&times; anisotropic. Capture all "
   "four. Record a short video of each with the camera moving forward — "
   "the aliasing is a motion artifact and still images undersell it.",
   "Implement tangent-space normal mapping on a mesh with mirrored UVs. "
   "Render with and without the handedness term and capture the difference on "
   "the mirrored half.",
   "Remove the Gram&ndash;Schmidt step and render a mesh with a non-uniform "
   "scale. Describe the resulting error.",
   "Measure the memory cost of your mipmap chain and confirm it is 4/3 of the "
   "base texture.",
 ],
 "selfcheck": [
   "Why can a sphere not be UV-unwrapped without distortion, and what three "
   "costs trade against each other in any UV layout?",
   "Explain the difference between magnification and minification artifacts, "
   "and why only one of them is a sampling failure.",
   "What problem do mipmaps solve, what do they cost in memory, and where "
   "does the 4/3 come from?",
   "How is the mip level selected, and why does this make texture sampling "
   "inside divergent control flow undefined?",
   "Why does trilinear filtering over-blur a floor seen at a shallow angle, "
   "and how does anisotropic filtering address it?",
   "Give two reasons to store normal maps in tangent space rather than object "
   "space, and name the two construction details most often got wrong.",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Sampling, Aliasing, and Antialiasing",
 "subtitle": "The theory behind every artifact in this course.",
 "question": "Why do jagged edges, shimmering textures, and lost highlights "
             "all have the same cause?",
 "outcomes": [
     "State the sampling theorem and apply it to rendering.",
     "Explain aliasing as frequency folding, not as 'jaggies'.",
     "Compare supersampling, MSAA, and post-process AA honestly.",
     "Explain why MSAA is cheap and why deferred rendering breaks it.",
     "Choose an antialiasing strategy for a given renderer and justify it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "One cause, many symptoms",
   "blurb": "Module 01 promised this. Here is the theory."},

  {"t": "table", "kicker": "Unification", "title": "The same failure, five places",
   "header": ["Symptom", "The signal being undersampled"],
   "widths": [5.0, 7.1],
   "rows": [
     ["Jagged edges", "Coverage — a step function, sampled at pixel centres"],
     ["Shimmering textures", "The texture, sampled once per pixel"],
     ["Vanishing specular highlights", "A narrow lighting function, sampled per vertex"],
     ["Crawling on thin geometry", "Coverage of a sub-pixel feature"],
     ["Shadow map acne and stairs", "The depth function, sampled at shadow-map resolution"],
   ],
   "note": "This table is the point of the module. Every artifact chased so "
           "far is one phenomenon."},

  {"t": "callout", "title": "Aliasing, properly defined", "kind": "Key idea",
   "body": ["Aliasing is not 'jagged edges'. Jagged edges are one visible "
            "consequence.",
            "Aliasing is what happens when a signal containing frequencies "
            "above half the sampling rate is sampled: those high frequencies "
            "<i>reappear as low frequencies</i>. They do not vanish; they "
            "masquerade.",
            "That is why the artifact is a pattern rather than noise, and why "
            "it moves coherently with the camera. A moir&eacute; pattern on a "
            "distant fence is high-frequency detail folded down into a "
            "low-frequency shape that was never there."]},

  {"t": "eq", "kicker": "Theory", "title": "Nyquist",
   "eqs": [
     ("f_s  >  2 f_max",
      "Sample at more than twice the highest frequency present, or lose it."),
     ("f_alias  =  |f − n·f_s|",
      "Frequencies above the limit fold back and appear as lower ones."),
     ("rendering: f_max is often ∞",
      "A triangle edge is a step function, with unbounded frequency content."),
   ],
   "caption": "The last line is the real problem. You cannot sample your way "
              "out of a step edge — you must prefilter, or accept "
              "residual error.",
   "note": "Press this: geometry edges genuinely have infinite bandwidth, so "
           "no finite sample rate suffices. That reframes AA as damage "
           "control rather than solution."},

  {"t": "two", "kicker": "Two strategies", "title": "Prefilter, or sample more",
   "lh": "Prefilter — remove the high frequencies first",
   "l": ["Band-limit the signal before sampling.",
         "<b>Mipmapping</b> is exactly this (Module 08).",
         "Correct, cheap, and done offline.",
         ("Only possible when you know the signal in advance.", 1),
         ("You do not know geometry coverage in advance.", 1)],
   "rh": "Supersample — raise the sampling rate",
   "r": ["Take more samples, then average.",
         "Works on any signal, including coverage.",
         "Cost scales directly with sample count.",
         ("Never eliminates aliasing, only pushes it higher.", 1),
         ("All geometric AA is a cheaper approximation of this.", 1)],
   "note": "Mipmapping is prefiltering; MSAA is supersampling restricted to "
           "coverage. Framing them as the two available strategies organises "
           "the whole module."},

  {"t": "section", "label": "Part 2", "title": "Antialiasing in practice",
   "blurb": "Every method is a different compromise."},

  {"t": "bullets", "kicker": "SSAA", "title": "Supersampling: correct and unaffordable",
   "items": [
     "Render at N× resolution, then downsample.",
     "Antialiases <b>everything</b>: coverage, shading, textures, "
     "specular highlights.",
     "",
     "Cost is N× in every respect — fragments, bandwidth, memory.",
     ("4× SSAA is roughly a quarter of your frame rate.", 1),
     "",
     "Correct, trivially implemented, and almost never used in real time.",
     ("Still the ground truth you compare other methods against.", 1),
   ]},

  {"t": "callout", "title": "MSAA: the key insight", "kind": "Why it is cheap",
   "body": ["Edges alias because <i>coverage</i> is undersampled. The "
            "<i>shading</i> within a triangle is usually smooth and does not "
            "need more samples.",
            "So: store N depth and coverage samples per pixel, but run the "
            "fragment shader <b>once</b>, at the pixel centre, and write that "
            "one result to every covered sample.",
            "You get N× coverage resolution for roughly 1× shading "
            "cost. Only the bandwidth and memory scale. This is why MSAA was "
            "the standard for fifteen years."]},

  {"t": "table", "kicker": "Methods", "title": "Antialiasing, compared honestly",
   "header": ["Method", "Fixes", "Misses", "Cost"],
   "widths": [2.4, 3.4, 3.8, 2.5],
   "rows": [
     ["SSAA", "Everything", "Nothing", "N× shading"],
     ["MSAA", "Geometric edges", "Shader aliasing, alpha-test edges", "N× bandwidth"],
     ["FXAA", "Edges in the final image", "Blurs; no sub-pixel information", "~1 ms, trivial"],
     ["TAA", "Edges, shading, and specular", "Ghosting, blur, disocclusion", "1 frame history"],
     ["DLSS/FSR", "As TAA, plus upscaling", "Same failure modes, better hidden", "Vendor-specific"],
   ],
   "note": "The honest summary: every real-time method trades a different "
           "artifact for the aliasing. There is no free antialiasing."},

  {"t": "bullets", "kicker": "MSAA", "title": "Why MSAA fell out of favour",
   "items": [
     "<b>Deferred rendering breaks it.</b> Lighting happens in a later pass, "
     "per pixel — so coverage samples have already been resolved away.",
     ("Keeping per-sample G-buffers costs N× the memory, which defeats "
      "the purpose of deferring.", 1),
     "",
     "<b>It only fixes geometry.</b> Modern aliasing is increasingly in the "
     "shading: sharp specular, high-frequency normal maps, thin highlights.",
     "",
     "<b>Alpha-tested foliage is invisible to it.</b> The edge is created by "
     "<code>discard</code>, not by coverage.",
     ("Alpha-to-coverage partially recovers this.", 1),
   ]},

  {"t": "bullets", "kicker": "TAA", "title": "Temporal antialiasing: samples from the past",
   "items": [
     "Jitter the projection by a sub-pixel offset each frame.",
     "Reproject the previous frame using motion vectors, and blend.",
     "",
     "Effectively supersamples <i>over time</i> — many samples for the "
     "cost of one per frame.",
     ("Antialiases shading and specular too, which MSAA cannot.", 1),
     "",
     "The cost is in the failure modes:",
     ("<b>Ghosting</b> when reprojection is wrong.", 1),
     ("<b>Blur</b> in motion, because history is resampled repeatedly.", 1),
     ("<b>Disocclusion</b> — newly revealed pixels have no history.", 1),
   ],
   "note": "TAA is the current default and the current complaint. Both are "
           "deserved. Understanding why explains most 'modern games look "
           "blurry' discourse."},

  {"t": "bullets", "kicker": "Practice", "title": "Choosing a method",
   "items": [
     "<b>Forward renderer, simple shading</b> → MSAA. Still excellent.",
     "<b>Deferred renderer</b> → TAA, or FXAA if you cannot afford "
     "motion vectors.",
     "<b>Heavy specular or dense normal maps</b> → TAA; MSAA will not "
     "touch the real problem.",
     "<b>Offline or reference renders</b> → SSAA. It is correct and you "
     "have the time.",
     "<b>Any renderer</b> → fix shader aliasing at the source too: "
     "roughness clamping, specular antialiasing, mip-biased normal maps.",
   ],
   "footnote": "The best antialiasing is a signal that was band-limited "
               "before you sampled it."},
 ],
 "takeaways": [
   "Aliasing is high frequencies folding down into low ones. Jagged edges are "
   "one symptom; shimmer, moiré, and lost highlights are others.",
   "Nyquist says sample above twice the highest frequency. Geometry edges "
   "have unbounded frequency content, so no sample rate is sufficient.",
   "There are two strategies: prefilter (mipmapping) or sample more "
   "(supersampling). Everything else is an approximation of one of them.",
   "MSAA is cheap because coverage is sampled N× while shading runs "
   "once. Deferred rendering destroys that trick.",
   "TAA supersamples across time, antialiases shading as well as geometry, "
   "and pays for it in ghosting and motion blur.",
   "The best fix is upstream: band-limit the signal before sampling it.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The unifying diagnosis"),
  ("p", "Module 01 claimed that nearly every artifact in this course is a "
        "sampling failure. This module makes that precise, and the payoff is "
        "that five apparently unrelated bugs become one phenomenon with one "
        "body of theory behind it."),
  ("table", ["Symptom", "Signal", "Sampling rate"],
   [["Jagged, stair-stepped edges",
     "Coverage: a step function at the triangle boundary",
     "One sample per pixel, at the centre."],
    ["Textures shimmer and crawl in motion",
     "The texture image projected onto the surface",
     "One sample per pixel; the footprint may span hundreds of texels."],
    ["Specular highlights vanish and pop",
     "A narrow cos&#8319; lobe over the surface",
     "Three samples per triangle, under Gouraud shading."],
    ["Thin geometry flickers and breaks up",
     "Coverage of a feature smaller than a pixel",
     "One sample per pixel, which the feature may fall between."],
    ["Shadow edges are blocky and stair-stepped",
     "The depth function of the scene from the light",
     "One sample per shadow-map texel."]],
   [0.26, 0.42, 0.32]),

  ("h1", "2 &nbsp; What aliasing actually is"),
  ("p", "The word is often used loosely to mean 'jagged edges'. The real "
        "definition is more useful because it predicts the artifacts you have "
        "not seen yet."),
  ("callout", "The definition",
   ["When a signal is sampled at rate f&#8347;, any frequency component above "
    "f&#8347;/2 does not disappear. It reappears — is <i>aliased</i> "
    "— as a lower frequency, specifically at |f &minus; n&middot;f&#8347;|.",
    "This is why aliasing artifacts are structured rather than noisy: a "
    "moir&eacute; pattern on a distant fence is the fence's high-frequency "
    "detail folded down into a coarse pattern that does not exist in the "
    "scene.",
    "It is also why aliasing moves coherently and distractingly with the "
    "camera: as the sampling grid shifts relative to the signal, the folded "
    "frequencies shift too."]),
  ("h2", "2.1 &nbsp; Nyquist, and why rendering violates it"),
  ("eq", "f&#8347; &gt; 2 f<sub>max</sub>"),
  ("p", "Sample at more than twice the highest frequency present and the "
        "signal can be reconstructed exactly. Sample below it and information "
        "is irrecoverably corrupted — not merely lost, but replaced by "
        "false low-frequency content."),
  ("p", "Rendering has a structural problem with this. A triangle edge is a "
        "step function: the coverage goes from 0 to 1 discontinuously. A step "
        "function has energy at <i>all</i> frequencies, without bound. There "
        "is no sampling rate high enough. Doubling the resolution halves the "
        "visible stair step and does not remove it."),
  ("p", "So antialiasing in rendering is not 'satisfy Nyquist'. It is "
        "'suppress the artifact to below the threshold of notice, as cheaply "
        "as possible'. Knowing that reframes every technique below as damage "
        "control, which is what they are."),

  ("h1", "3 &nbsp; The two strategies"),
  ("h2", "3.1 &nbsp; Prefiltering"),
  ("p", "Remove the high frequencies before sampling. If the signal is "
        "band-limited below f&#8347;/2 then one sample per pixel is correct "
        "and nothing folds. This is ideal, and it is available exactly when "
        "you know the signal in advance."),
  ("p", "Mipmapping is prefiltering. Each mip level is a band-limited version "
        "of the texture, computed offline, and level selection chooses the "
        "band limit appropriate to the current sampling rate. This is why "
        "mipmapping works so well and costs so little: the expensive part "
        "happened before the frame started."),
  ("p", "It is not available for geometric coverage, because coverage depends "
        "on the camera and cannot be precomputed. That asymmetry explains why "
        "texture aliasing is a solved problem and edge aliasing is not."),
  ("h2", "3.2 &nbsp; Supersampling"),
  ("p", "Raise the sampling rate, then average down. This works on any "
        "signal, known in advance or not. The cost scales directly with the "
        "sample count, and because step edges have unbounded bandwidth it "
        "never eliminates aliasing — it pushes the folding up to a "
        "frequency where it is less visible."),

  ("break",),
  ("h1", "4 &nbsp; The methods"),
  ("h2", "4.1 &nbsp; SSAA"),
  ("p", "Render the whole frame at N&times; resolution and downsample. "
        "Antialiases everything — coverage, shading, textures, specular "
        "highlights, alpha test — because every part of the pipeline "
        "genuinely runs at the higher rate. It is also N&times; the cost in "
        "fragments, bandwidth, and memory. 4&times; SSAA is approximately a "
        "quarter of your frame rate."),
  ("p", "Almost never used in real time, but it is the reference you compare "
        "everything else against, and you should implement it once so you "
        "know what correct looks like."),
  ("h2", "4.2 &nbsp; MSAA"),
  ("callout", "The insight that makes MSAA cheap",
   ["Geometric edges alias because <i>coverage</i> is undersampled. The "
    "shading <i>inside</i> a triangle is usually smooth and does not need a "
    "higher rate.",
    "So MSAA stores N depth and coverage samples per pixel, but invokes the "
    "fragment shader only <b>once per pixel per triangle</b>, writing that "
    "single result to every sample the triangle covers.",
    "Coverage resolution goes up N&times;; shading cost stays at 1&times;. "
    "Only memory and bandwidth scale. For a forward renderer with smooth "
    "shading this is close to a free lunch, and it is why MSAA dominated for "
    "fifteen years."]),
  ("p", "Its limitations follow directly from the same insight:"),
  ("ul", ["<b>It does not touch shader aliasing.</b> A high-frequency normal "
          "map producing sparkling specular highlights is sampled once per "
          "pixel regardless of MSAA level, because the shader ran once.",
          "<b>Alpha-tested edges are invisible to it.</b> The visual edge of "
          "a leaf card is created by <code>discard</code> inside the shader, "
          "not by triangle coverage. <i>Alpha-to-coverage</i> partially "
          "recovers this by converting alpha into a coverage mask.",
          "<b>Deferred rendering breaks it.</b> In a deferred renderer "
          "lighting happens in a later full-screen pass, by which point the "
          "G-buffer has been resolved to one value per pixel. Keeping "
          "per-sample G-buffers costs N&times; the memory and bandwidth of "
          "the G-buffer, which defeats the reason for deferring in the first "
          "place."]),
  ("h2", "4.3 &nbsp; Post-process AA (FXAA, SMAA)"),
  ("p", "Analyse the finished image, find edge-like patterns, and blur across "
        "them. Extremely cheap — around a millisecond — and "
        "independent of how the frame was rendered, so it works with deferred "
        "shading, alpha test, and anything else."),
  ("p", "The fundamental limitation is that it has no information that was "
        "not in the final image. It cannot recover a sub-pixel feature that "
        "was never sampled, and it cannot distinguish a genuine edge from a "
        "deliberate high-contrast texture detail, so it blurs some things "
        "that should stay sharp. It is a plausible-looking smoothing, not a "
        "reconstruction."),
  ("h2", "4.4 &nbsp; TAA"),
  ("p", "Temporal antialiasing jitters the projection matrix by a sub-pixel "
        "offset each frame, so successive frames sample the scene at "
        "different positions. Previous frames are reprojected into the "
        "current frame using motion vectors and blended in. Over several "
        "frames this accumulates many samples per pixel for the cost of one "
        "sample per frame — supersampling spread across time."),
  ("p", "Crucially, it antialiases <i>shading</i> as well as geometry, "
        "because the whole pipeline runs at each jittered position. That is "
        "why TAA displaced MSAA as modern rendering became more "
        "shading-limited and more deferred."),
  ("callout", "What TAA costs",
   ["<b>Ghosting.</b> When reprojection is wrong — a shadow moves "
    "without the object, a reflection changes, a transparent surface has no "
    "sensible motion vector — stale colour trails behind.",
    "<b>Blur in motion.</b> The history buffer is resampled every frame, and "
    "repeated bilinear resampling is a low-pass filter. Movement progressively "
    "softens the image.",
    "<b>Disocclusion.</b> Pixels revealed from behind an object have no "
    "history at all and must fall back to a single sample, so newly exposed "
    "regions alias visibly.",
    "Neighbourhood clamping, variance clipping, and sharpening mitigate all "
    "three without removing them. DLSS and FSR are this same architecture "
    "with learned or hand-tuned reconstruction, and they inherit the same "
    "failure modes in better-disguised form."]),

  ("h1", "5 &nbsp; Choosing"),
  ("table", ["Situation", "Choice", "Why"],
   [["Forward renderer, smooth shading", "MSAA 4&times;",
     "Near-free for what it fixes, and no temporal artifacts at all."],
    ["Deferred renderer", "TAA",
     "MSAA is impractical; TAA also handles the shading aliasing that "
     "deferred pipelines tend to have."],
    ["Heavy specular, dense normal maps", "TAA + specular antialiasing",
     "The aliasing is in the shading, so MSAA cannot reach it. Clamp "
     "roughness and use normal-map mip bias as well."],
    ["Mobile or very tight budget", "FXAA or SMAA",
     "About a millisecond, no history buffer, no motion vectors."],
    ["Offline or reference image", "SSAA",
     "Correct, simple, and you have the time. Use it to judge everything "
     "else."]],
   [0.26, 0.21, 0.53]),
  ("callout", "The best antialiasing happens before sampling",
   ["Every method above is mitigation after the fact. Reducing the signal's "
    "bandwidth is better and often cheaper:",
    "Clamp roughness to a minimum so specular lobes are never narrower than a "
    "pixel. Bias normal-map mip selection so distant surfaces lose "
    "high-frequency normals. Filter normal maps into roughness (LEAN or "
    "Toksvig mapping) so that shrinking geometry becomes rougher rather than "
    "sparklier.",
    "These cost almost nothing and attack the cause rather than the symptom."]),
 ],
 "resources": [
   ("GAMES101 Lectures 06 and 09 — Antialiasing, Texture aliasing",
    "https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html",
    "Aliasing presented properly in the frequency domain, with the "
    "spatial/frequency duality made visual."),
   ("CMU 15-462 — Sampling and Aliasing",
    "https://15462.courses.cs.cmu.edu/",
    "The most rigorous free treatment: Fourier analysis applied directly to "
    "the rendering case."),
   ("Jorge Jimenez et al. — SMAA and 'Filmic SMAA' (SIGGRAPH course, "
    "free)",
    "http://www.iryoku.com/smaa/",
    "Post-process antialiasing done well, with an honest account of its "
    "limits."),
   ("Brian Karis — 'High Quality Temporal Supersampling' (SIGGRAPH "
    "course, free)",
    "https://advances.realtimerendering.com/s2014/",
    "The reference presentation on practical TAA, including neighbourhood "
    "clamping. Still the clearest explanation of why TAA ghosts."),
 ],
 "exercises": [
   "Implement 4&times; and 16&times; SSAA in your software rasterizer. "
   "Capture a scene with near-horizontal edges at 1&times;, 4&times;, and "
   "16&times; and measure the render time of each.",
   "Implement MSAA in the software rasterizer: multiple coverage and depth "
   "samples per pixel, one shading evaluation. Verify that shading cost does "
   "not scale with sample count by counting shader invocations.",
   "Construct a case where MSAA fails: a surface with a high-frequency normal "
   "map producing specular sparkle. Capture it at MSAA 1&times; and "
   "8&times;. Explain why they look the same.",
   "Render a converging line pattern (a Siemens star or a fine picket fence "
   "receding to the horizon) and capture the moir&eacute; pattern. Then "
   "mipmap it properly and capture again.",
   "Implement specular antialiasing by clamping roughness based on the "
   "screen-space derivative of the normal. Capture before and after on a "
   "sharp metallic surface in motion.",
   "Write a one-page comparison of MSAA and TAA for a renderer you would "
   "actually build, with a recommendation and a justification.",
 ],
 "selfcheck": [
   "Define aliasing without using the word 'jagged'. Why do aliasing "
   "artifacts form patterns rather than noise?",
   "State the Nyquist criterion and explain why geometric edges make it "
   "unsatisfiable in principle.",
   "What are the two general strategies against aliasing? Give an example of "
   "each from this course.",
   "Why is MSAA much cheaper than SSAA for the same edge quality, and what "
   "exactly does it fail to fix?",
   "Give the specific reason deferred rendering makes MSAA impractical.",
   "Name TAA's three characteristic artifacts and the underlying cause of "
   "each.",
   "Give two ways to reduce aliasing by changing the signal rather than the "
   "sampling.",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Shadows",
 "subtitle": "Visibility from the light's point of view, and everything that "
             "goes wrong with it.",
 "question": "How do you decide whether a point can see the light?",
 "outcomes": [
     "Implement basic shadow mapping end to end.",
     "Diagnose acne, peter-panning, and aliasing, and explain the cause of "
     "each.",
     "Apply slope-scaled bias and normal offset correctly.",
     "Implement PCF and explain what it does and does not fix.",
     "Explain cascaded shadow maps and why directional lights need them.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The idea",
   "blurb": "A point is lit if the light can see it. So render from the light."},

  {"t": "bullets", "kicker": "Shadow mapping", "title": "The algorithm in two passes",
   "items": [
     "<b>Pass 1.</b> Render the scene from the light's position, storing "
     "depth only.",
     ("This is a depth buffer — the nearest surface the light can see "
      "in every direction.", 1),
     "",
     "<b>Pass 2.</b> Render normally. For each fragment:",
     ("Transform its world position into the light's clip space.", 1),
     ("Compare its depth to the stored depth at that location.", 1),
     ("Greater → something is between it and the light → in "
      "shadow.", 1),
     "",
     "Image-space, geometry-independent, and the standard technique "
     "everywhere.",
   ],
   "note": "Emphasise that pass 1 is literally the Module 05 depth buffer "
           "with a different camera. Nothing new is required to build it."},

  {"t": "code", "kicker": "Shadow mapping", "title": "The lookup",
   "lang": "glsl", "code": """
float shadow(vec3 worldPos, vec3 N, vec3 L) {
    vec4 lp = uLightVP * vec4(worldPos, 1.0);
    vec3 pc = lp.xyz / lp.w;             // perspective divide
    pc = pc * 0.5 + 0.5;                 // NDC [-1,1] -> UV [0,1]

    // Outside the light's frustum: treat as lit, not as shadowed.
    if (pc.z > 1.0) return 1.0;

    float stored  = texture(uShadowMap, pc.xy).r;
    float current = pc.z;

    return (current - BIAS) > stored ? 0.0 : 1.0;
}
""",
   "caption": "Four lines of real work. Everything difficult about shadows is "
              "in the choice of BIAS and in what happens at the edges.",
   "note": "Note the pc.z > 1.0 early out, and tie it back to Module 08's "
           "clamp-to-border wrap mode."},

  {"t": "section", "label": "Part 2", "title": "Three artifacts",
   "blurb": "Each has a different cause, and fixing one often causes another."},

  {"t": "callout", "title": "Shadow acne", "kind": "Artifact 1",
   "body": ["Moiré-like stripes of self-shadowing across lit surfaces.",
            "<b>Cause:</b> the shadow map stores one depth per texel, but the "
            "texel covers an <i>area</i> of a sloped surface. Points within "
            "that area are nearer or further than the single stored value, so "
            "roughly half of them test as shadowed by themselves.",
            "The steeper the surface relative to the light, the wider the "
            "depth range inside one texel, and the worse the acne. On a "
            "surface perpendicular to the light there is no acne at all "
            "— which is the clue to the fix."]},

  {"t": "eq", "kicker": "Fix 1", "title": "Slope-scaled bias",
   "eqs": [
     ("bias  =  c₁ + c₂ · tan(θ)   where cosθ = n·l",
      "The depth range within a texel grows with the surface slope, so the "
      "bias should too."),
     ("bias = max(c₂ · (1 − n·l), c₁)",
      "The usual cheap approximation. Constant floor plus a slope term."),
     ("normal offset:  p' = p + n · k",
      "Move the sample point along the normal instead of biasing depth. "
      "Often better behaved."),
   ],
   "caption": "Constant bias alone forces you to choose between acne (too "
              "small) and peter-panning (too large). Slope scaling removes "
              "most of that dilemma.",
   "note": "Normal offset is underused and often the better answer; it "
           "translates in world space rather than along the light ray."},

  {"t": "callout", "title": "Peter-panning", "kind": "Artifact 2",
   "body": ["The shadow detaches from the object and floats, so objects "
            "appear to hover above the ground.",
            "<b>Cause:</b> too much bias. The contact point where the object "
            "meets the floor is pushed out of shadow.",
            "This is the direct consequence of over-correcting artifact 1, "
            "which is why constant bias alone is a losing game: the value "
            "that removes acne on sloped surfaces detaches shadows on flat "
            "ones.",
            "Partial fix: render only back faces into the shadow map, so the "
            "biasing happens on surfaces you never see. Works well on closed "
            "geometry, badly on open sheets."]},

  {"t": "callout", "title": "Shadow aliasing", "kind": "Artifact 3",
   "body": ["Blocky, stair-stepped shadow edges — Module 09's "
            "phenomenon, now in the shadow map.",
            "<b>Cause:</b> the shadow map is a finite-resolution sampling of "
            "the depth function. One texel may cover many screen pixels, "
            "especially near the camera or for a light covering a large area.",
            "This is <i>perspective aliasing</i>: the mismatch between shadow "
            "map resolution and screen resolution varies enormously with "
            "distance. It is the reason cascades exist."]},

  {"t": "section", "label": "Part 3", "title": "Softening and scaling",
   "blurb": "PCF for the edges; cascades for the distance."},

  {"t": "code", "kicker": "PCF", "title": "Percentage-closer filtering",
   "lang": "glsl", "code": """
// Average the COMPARISON RESULTS, not the depths.
// Averaging depths and then comparing is wrong and gives you nothing.
float pcf(vec3 pc, float bias) {
    float sum = 0.0;
    vec2 texel = 1.0 / textureSize(uShadowMap, 0);

    for (int y = -1; y <= 1; ++y)
    for (int x = -1; x <= 1; ++x) {
        float d = texture(uShadowMap, pc.xy + vec2(x,y) * texel).r;
        sum += (pc.z - bias) > d ? 0.0 : 1.0;
    }
    return sum / 9.0;
}
""",
   "caption": "Comparison is a step function, so averaging before comparing "
              "returns a step function again. Averaging after comparing is "
              "what produces a gradient.",
   "note": "This is the single most important conceptual point about PCF and "
           "it is easy to get backwards."},

  {"t": "bullets", "kicker": "PCF", "title": "What PCF does and does not do",
   "items": [
     "<b>Does:</b> antialias the shadow edge. The hard step becomes a "
     "gradient over the filter width.",
     "<b>Does:</b> hide residual acne, by averaging it away.",
     "",
     "<b>Does not:</b> produce physically correct soft shadows.",
     ("A real penumbra widens with distance from the occluder.", 1),
     ("PCF's width is constant — it is blur, not penumbra.", 1),
     "",
     "PCSS estimates blocker distance to vary the radius. More correct, more "
     "expensive, and still an approximation.",
   ]},

  {"t": "bullets", "kicker": "Cascades", "title": "Why directional lights need cascades",
   "items": [
     "The sun must shadow everything from 1 m to 1000 m.",
     "One shadow map covering that range gives perhaps 1 texel per metre "
     "nearby — unusably coarse.",
     "",
     "<b>Cascaded shadow maps:</b> split the view frustum by depth, one "
     "shadow map per slice.",
     ("Near slice: small area, high effective resolution.", 1),
     ("Far slice: large area, low resolution — and nobody notices.", 1),
     "",
     "Typically 3–4 cascades, split logarithmically.",
     ("Blend across cascade boundaries, or the seam is visible.", 1),
   ],
   "note": "The split scheme matters: pure logarithmic wastes near detail, "
           "pure uniform wastes far. Practical schemes blend the two."},

  {"t": "table", "kicker": "Reference", "title": "Shadows by light type",
   "header": ["Light", "Projection", "Maps needed", "Notes"],
   "widths": [2.6, 3.0, 2.6, 3.9],
   "rows": [
     ["Directional (sun)", "Orthographic", "3–4 cascades", "Fit each cascade to its frustum slice"],
     ["Spot", "Perspective", "1", "Simplest case; frustum matches the cone"],
     ["Point", "Perspective ×6", "Cube map", "Six renders, or one with layered geometry"],
     ["Area", "—", "Many / stochastic", "No exact shadow map method; sample or raytrace"],
   ],
   "note": "Point lights costing six renders is why engines limit the number "
           "of shadow-casting point lights so aggressively."},

  {"t": "table", "kicker": "Diagnosis", "title": "Shadow bugs at a glance",
   "header": ["What you see", "Cause"],
   "widths": [5.3, 6.8],
   "rows": [
     ["Striped self-shadowing on lit surfaces", "Bias too small — acne"],
     ["Shadows detached, objects float", "Bias too large — peter-panning"],
     ["Blocky stair-stepped shadow edges", "Shadow map resolution; needs PCF and/or cascades"],
     ["Everything in shadow beyond a distance", "Outside the light frustum; needs the pc.z > 1 early out"],
     ["Hard line across the scene at a fixed depth", "Cascade boundary without blending"],
     ["Shadow swims as the camera moves", "Cascade not snapped to texel boundaries"],
   ]},
 ],
 "takeaways": [
   "Shadow mapping is a depth buffer rendered from the light. Pass 1 is "
   "Module 05 with a different camera.",
   "Acne comes from one depth per texel covering a sloped area; peter-panning "
   "comes from over-correcting it. Slope-scaled bias and normal offset break "
   "the dilemma.",
   "Shadow aliasing is Module 09 again, with the shadow map as the sampling "
   "grid.",
   "PCF averages comparison results, not depths. Averaging depths first is "
   "wrong and achieves nothing.",
   "PCF produces blur, not penumbra. Real soft shadows widen with occluder "
   "distance; PCSS approximates that.",
   "Directional lights need cascades because one map cannot cover 1 m and "
   "1000 m usefully. Snap cascades to texels or the shadows swim.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Shadows as a visibility problem"),
  ("p", "A point is lit if there is an unobstructed path between it and the "
        "light. That is a visibility query, and you have already built a "
        "machine that answers visibility queries: the depth buffer. The only "
        "change is where the camera is."),
  ("p", "Render the scene from the light's position, storing depth only. The "
        "resulting buffer records, for every direction the light looks, how "
        "far away the nearest surface is — that is, the surface the "
        "light illuminates. Then, during normal rendering, transform each "
        "fragment into the light's clip space and compare: if the fragment is "
        "further from the light than the stored depth, something is in "
        "between, and it is in shadow."),
  ("code", """// Pass 1: from the light, depth only.
glViewport(0, 0, SHADOW_W, SHADOW_H);
glBindFramebuffer(GL_FRAMEBUFFER, shadowFBO);
glClear(GL_DEPTH_BUFFER_BIT);
draw_scene(lightView, lightProj);      // no colour, no shading

// Pass 2: from the camera, with the lookup.
float shadow(vec3 worldPos) {
    vec4 lp = uLightVP * vec4(worldPos, 1.0);
    vec3 pc = lp.xyz / lp.w;
    pc = pc * 0.5 + 0.5;               // NDC -> texture coordinates

    if (pc.z > 1.0) return 1.0;        // beyond the light's far plane: lit

    float stored = texture(uShadowMap, pc.xy).r;
    return (pc.z - BIAS) > stored ? 0.0 : 1.0;
}"""),
  ("p", "The technique is image-space and geometry-independent: it does not "
        "care how the scene is built, handles arbitrary geometry including "
        "alpha-tested foliage, and costs one extra pass. It is, for these "
        "reasons, essentially universal. Everything difficult about it is in "
        "the artifacts."),

  ("h1", "2 &nbsp; Acne"),
  ("p", "The first thing you will see is striped self-shadowing: a "
        "moir&eacute;-like pattern of dark bands across surfaces that should "
        "be fully lit."),
  ("p", "The cause is a resolution mismatch. The shadow map stores one depth "
        "per texel, but that texel corresponds to an <i>area</i> of the "
        "receiving surface. If the surface is sloped relative to the light, "
        "the true depth varies continuously across that area while the stored "
        "value is a single number sampled somewhere within it. Points on the "
        "far side of the sample are deeper than the stored depth and therefore "
        "test as shadowed — by themselves."),
  ("callout", "The diagnostic clue",
   ["Acne is worst on surfaces oblique to the light and absent on surfaces "
    "facing it directly.",
    "That is because the depth range spanned by one texel is proportional to "
    "the surface slope: a perpendicular surface has constant depth within the "
    "texel, so there is nothing to misjudge.",
    "This immediately tells you the correction should scale with slope."]),
  ("h2", "2.1 &nbsp; Bias"),
  ("p", "Offset the comparison so a surface must be meaningfully deeper than "
        "the stored value before it counts as shadowed. A constant bias "
        "works, badly: the value large enough to suppress acne on steep "
        "surfaces is large enough to detach shadows on flat ones."),
  ("eq", "bias = max( c&#8322; &middot; (1 &minus; n&middot;l), c&#8321; )"),
  ("p", "Slope-scaled bias makes the offset proportional to the surface "
        "slope, which is proportional to the depth range inside a texel. A "
        "small constant floor handles the perpendicular case. This removes "
        "most of the dilemma."),
  ("h2", "2.2 &nbsp; Normal offset"),
  ("p", "A frequently better alternative: rather than biasing the depth "
        "comparison, move the <i>sample position</i> along the surface normal "
        "before projecting into light space."),
  ("eq", "p&prime; = p + n &middot; k &nbsp;&nbsp; (k scaled by texel world size and slope)"),
  ("p", "This translates the sample in world space, perpendicular to the "
        "surface, rather than pushing it along the light ray. It tends to "
        "produce less peter-panning for the same acne suppression, because it "
        "does not move the contact point away from the floor in the direction "
        "that matters. In practice a combination of a small slope-scaled "
        "depth bias and a normal offset works best."),

  ("h1", "3 &nbsp; Peter-panning"),
  ("p", "Over-correct the bias and shadows detach from their objects: the "
        "contact shadow where an object meets the floor is pushed out of "
        "shadow, so the object appears to hover. The name is self-explanatory "
        "once you have seen it."),
  ("p", "A partial fix is to render only <b>back faces</b> into the shadow "
        "map. The surfaces being biased are then ones the camera never sees, "
        "so the bias cannot detach a visible contact point. This works well "
        "for closed watertight geometry and fails for open sheets — a "
        "single-sided wall, a leaf card — which have no back faces to "
        "render. Most engines therefore do it selectively."),

  ("break",),
  ("h1", "4 &nbsp; Shadow aliasing and PCF"),
  ("p", "Shadow edges are blocky because the shadow map is a finite sampling "
        "of the depth function, and one shadow texel frequently covers many "
        "screen pixels. This is exactly Module 09's phenomenon with the "
        "shadow map as the sampling grid, and the same two strategies apply: "
        "sample more, or filter."),
  ("h2", "4.1 &nbsp; Percentage-closer filtering"),
  ("callout", "Filter the results, not the depths",
   ["The obvious approach — average the depths in a neighbourhood, then "
    "compare once — does not work. Comparison is a step function, so "
    "comparing a single averaged depth still yields a hard 0 or 1. You get a "
    "slightly wrong hard edge instead of a soft one.",
    "PCF compares <i>first</i>, at each tap, and averages the binary results. "
    "Nine taps give ten possible values between 0 and 1, which is a gradient. "
    "This ordering is the entire content of the technique, and it is easy to "
    "implement backwards."]),
  ("code", """float pcf(vec3 pc, float bias) {
    float sum = 0.0;
    vec2 texel = 1.0 / vec2(textureSize(uShadowMap, 0));
    for (int y = -1; y <= 1; ++y)
    for (int x = -1; x <= 1; ++x) {
        float d = texture(uShadowMap, pc.xy + vec2(x,y)*texel).r;
        sum += (pc.z - bias) > d ? 0.0 : 1.0;   // compare, THEN accumulate
    }
    return sum / 9.0;
}"""),
  ("p", "Hardware comparison samplers (<code>sampler2DShadow</code>) do the "
        "compare-then-filter in one instruction with bilinear weighting, "
        "which is both faster and smoother than a manual loop. Use them."),
  ("h2", "4.2 &nbsp; PCF is blur, not penumbra"),
  ("p", "A real soft shadow has a penumbra whose width grows with the "
        "distance between occluder and receiver: the shadow under your foot "
        "is sharp, the shadow of a cloud is diffuse. PCF applies a "
        "<i>constant</i> filter width everywhere, so it produces uniformly "
        "soft edges regardless of geometry. It looks better than a hard edge "
        "and it is not physically meaningful."),
  ("p", "Percentage-closer soft shadows (PCSS) adds a blocker-search step: "
        "sample the shadow map to estimate the average depth of occluders, "
        "compute the penumbra width that geometry implies, and size the PCF "
        "kernel accordingly. More correct, several times the cost, and still "
        "an approximation — but a convincing one."),

  ("h1", "5 &nbsp; Cascaded shadow maps"),
  ("p", "A directional light has no position, so its shadow map must cover "
        "the entire visible scene. For an outdoor view that might be one "
        "metre to one kilometre. A single 2048&times;2048 map spread over a "
        "kilometre gives roughly half a metre per texel, which is useless for "
        "anything near the camera."),
  ("p", "The mismatch is not uniform: nearby geometry occupies many screen "
        "pixels per shadow texel, distant geometry occupies few. This is "
        "<b>perspective aliasing</b>, and the fix is to match shadow "
        "resolution to screen resolution by splitting the problem."),
  ("ul", ["Divide the camera frustum into 3&ndash;4 depth slices.",
          "Render a separate shadow map fitted tightly to each slice.",
          "In the fragment shader, select the cascade by view depth.",
          "Blend across cascade boundaries, or a hard line appears across "
          "the scene at a fixed distance.",
          "<b>Snap each cascade to shadow-texel boundaries</b> as the camera "
          "moves. Without this the shadow map's sampling grid slides "
          "continuously relative to the world, and shadow edges crawl and "
          "shimmer — a distinctive, very visible artifact."]),
  ("p", "Split placement matters. Pure logarithmic splits are theoretically "
        "right for perspective aliasing but waste resolution at the far end; "
        "uniform splits waste it at the near end. Practical schemes blend the "
        "two with a tunable weight, and then let an artist adjust it."),

  ("h1", "6 &nbsp; By light type"),
  ("table", ["Light", "Shadow projection", "Cost", "Notes"],
   [["Directional (sun)", "Orthographic, one per cascade",
     "3&ndash;4 scene renders",
     "Fit each cascade to its frustum slice; snap to texels."],
    ["Spot", "Perspective matching the cone", "1 scene render",
     "The simplest case. The light frustum is the cone."],
    ["Point", "Six perspective renders into a cube map",
     "6 scene renders",
     "Expensive, which is why engines limit shadow-casting point lights "
     "severely. Layered rendering can reduce it to one pass."],
    ["Area", "No exact method",
     "Stochastic or ray-traced",
     "Shadow maps assume a point source. Area lights need many samples, or "
     "ray tracing."]],
   [0.17, 0.27, 0.19, 0.37]),
 ],
 "resources": [
   ("GAMES101 Lecture 10 — Shadow Mapping",
    "https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html",
    "The algorithm and the bias problem, clearly derived."),
   ("LearnOpenGL — Shadow Mapping and Point Shadows",
    "https://learnopengl.com/Advanced-Lighting/Shadows/Shadow-Mapping",
    "Working implementation including the cube-map point-light case."),
   ("Microsoft — 'Common Techniques to Improve Shadow Depth Maps'",
    "https://learn.microsoft.com/en-us/windows/win32/dxtecharts/common-techniques-to-improve-shadow-depth-maps",
    "The definitive free reference on cascades, bias strategies, and texel "
    "snapping. Read it in full before implementing cascades."),
   ("Fernando — Percentage-Closer Soft Shadows (NVIDIA, free)",
    "https://developer.nvidia.com/gpugems/gpugems/part-ii-lighting-and-shadows",
    "The original PCSS formulation with the blocker-search derivation."),
 ],
 "exercises": [
   "Implement basic shadow mapping for a single spot light. Capture the "
   "result with zero bias and observe acne in its natural state.",
   "Implement constant bias, then slope-scaled bias, then normal offset. "
   "Capture a scene with both steep and flat surfaces under each, and find "
   "the constant-bias value that trades acne for peter-panning. Document "
   "that there is no good value.",
   "Implement 3&times;3 PCF manually, then switch to a hardware comparison "
   "sampler. Measure both and compare quality.",
   "Deliberately implement PCF backwards — average the depths, then "
   "compare — and capture the result. Explain in one sentence why it "
   "produces a hard edge.",
   "Implement 3-cascade shadow maps for a directional light. First without "
   "texel snapping: move the camera slowly and record the crawling. Then add "
   "snapping and record again.",
   "Visualise your cascade selection by tinting each cascade a different "
   "colour. Use it to check your split distances are sensible for your "
   "scene.",
 ],
 "selfcheck": [
   "Explain shadow mapping in two sentences, and say which earlier module "
   "pass 1 reuses unchanged.",
   "What causes shadow acne, and why is it worst on surfaces oblique to the "
   "light?",
   "Why is a constant bias a losing proposition? What two techniques break "
   "the dilemma, and how does each work?",
   "Why must PCF compare before averaging? What happens if you reverse the "
   "order?",
   "Explain why PCF does not produce physically correct soft shadows, and "
   "what PCSS adds.",
   "Why do directional lights need cascades? What goes wrong if cascades are "
   "not snapped to texel boundaries?",
 ],
},

]
