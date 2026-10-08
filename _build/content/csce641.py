# -*- coding: utf-8 -*-
"""CSCE 641 Computer Graphics — original course content."""

EM = "—"

COURSE = {
    "code": "CSCE 641",
    "title": "Computer Graphics",
    "tagline": "The real-time pipeline from first principles: transforms, "
               "rasterization, shading, texturing, and animation",
    "term": "Semester 1 (with CSCE 629 and CSCE 614)",
    "prereqs": "Linear algebra (UC LINA 600); C++ fluency; no prior graphics "
               "assumed",
    "effort": "10–12 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A software rasterizer written from scratch, then the same "
                   "scene reproduced on the GPU with a programmable pipeline",
    "description": [
        "Computer graphics is the problem of deciding, for every pixel on a "
        "screen, what colour it should be — fast enough that the answer "
        "arrives sixty times a second. Stated that way it sounds like a "
        "question about colour. It is really a question about geometry, "
        "sampling, and parallelism, and the colour falls out at the end.",
        "This course builds the real-time pipeline from the bottom. You will "
        "write a rasterizer that has no GPU underneath it, so that nothing is "
        "magic: your own matrix stack, your own triangle setup, your own "
        "depth test, your own texture filtering. Only once that works do we "
        "move to the GPU, where the same stages reappear as hardware and the "
        "parts you programmed by hand become the parts you configure.",
        "The emphasis throughout is on <i>why each stage exists</i>. Almost "
        "every stage in the pipeline is there to make a sampling problem "
        "tractable or to exploit parallelism, and once you can see which, the "
        "design stops looking arbitrary. By the end you should be able to "
        "look at a rendering artifact and localise it to a stage before you "
        "open a debugger.",
    ],
    "outcomes": [
        "Derive and compose the model, view, and projection transforms, and "
        "explain what the perspective divide does geometrically.",
        "Implement triangle rasterization with correct fill rules, "
        "perspective-correct interpolation, and depth testing.",
        "Explain aliasing as a sampling phenomenon and implement at least two "
        "antialiasing strategies with their trade-offs.",
        "Write vertex and fragment shaders for a physically based material "
        "under image-based lighting.",
        "Implement shadow mapping and diagnose its characteristic artifacts.",
        "Build a transform hierarchy with skinned skeletal animation.",
        "Localise a rendering bug to a pipeline stage from the artifact "
        "alone.",
    ],
    "materials": [
        ("GAMES101 — Lingqi Yan, Introduction to Modern Computer "
         "Graphics (free, English slides)",
         "https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html",
         "Primary lecture series. Clear, modern, and closely aligned to this "
         "course's order. Watch the mapped lecture before each module."),
        ("CMU 15-462/662 Computer Graphics — Keenan Crane (free video)",
         "https://15462.courses.cs.cmu.edu/",
         "Second voice, more mathematical. Best for geometry, sampling, and "
         "the parts where you want the theory tightened."),
        ("Cem Yuksel — Interactive Computer Graphics, Utah (free video)",
         "https://graphics.cs.utah.edu/courses/cs6610/",
         "Best practical treatment of the GPU pipeline and the API layer. "
         "Use from Module 07 onward."),
        ("UC San Diego CSE167x Computer Graphics (edX, free audit)",
         "https://www.edx.org/learn/computer-graphics/the-university-of-california-san-diego-computer-graphics",
         "Structured assignments with automated feedback. Good if you want "
         "graded checkpoints."),
        ("Scratchapixel — graphics from scratch (free)",
         "https://www.scratchapixel.com/",
         "Written reference with full derivations. The place to go when a "
         "lecture moved too fast."),
        ("LearnOpenGL (free)",
         "https://learnopengl.com/",
         "The API tutorial. Use for mechanics only — the theory comes "
         "from this course, not from here."),
    ],
    "tooling": [
        "<b>C++17 or newer</b>, with CMake. The rasterizer should have no "
        "dependencies beyond a PNG writer — that is the point.",
        "<b>GLM</b> for vector and matrix types once you are past Module 03. "
        "Write your own first, then switch, so you know what it does.",
        "<b>OpenGL 4.5 core</b> or <b>Vulkan</b> from Module 07. OpenGL is "
        "recommended for this course: less ceremony per concept.",
        "<b>RenderDoc</b> for frame capture. Non-negotiable from Module 07 "
        "— reading a captured frame is a core skill, not a debugging "
        "last resort.",
        "<b>A portfolio repository</b>, public, from day one. Each module's "
        "output committed with a README image.",
    ],
    "projects": [
        {"title": "Software rasterizer", "after": 5,
         "brief": "Write a complete software rasterizer: load a triangle "
                  "mesh, transform it through the full MVP chain, rasterize "
                  "with correct fill rules and perspective-correct "
                  "interpolation, depth-test it, and write a PNG. No GPU, no "
                  "graphics API, no matrix library you did not write.",
         "reqs": [
             "Loads an OBJ mesh with positions, normals, and texture "
             "coordinates.",
             "Full model/view/projection chain with a configurable camera, "
             "including perspective divide and viewport transform.",
             "Triangle rasterization using edge functions, with a consistent "
             "fill rule so that shared edges are neither doubled nor gapped.",
             "Perspective-correct interpolation of all vertex attributes.",
             "Z-buffer with correct depth precision handling.",
             "Backface culling and near-plane clipping.",
         ],
         "done": [
             "Renders a 5,000-triangle mesh correctly at 1920&times;1080.",
             "A screenshot showing no cracks along shared triangle edges "
             "under magnification.",
             "A second screenshot with perspective-correct interpolation "
             "disabled, demonstrating that you can see the difference and "
             "explain it.",
         ]},
        {"title": "GPU renderer with physically based shading", "after": 11,
         "brief": "Reproduce the same scene on the GPU with a programmable "
                  "pipeline, then take it past what the software renderer "
                  "could do: a physically based material model under "
                  "image-based lighting, with shadow mapping and "
                  "antialiasing.",
         "reqs": [
             "Vertex and fragment shaders implementing a Cook–Torrance "
             "microfacet BRDF with metallic/roughness parameters.",
             "Image-based lighting from an HDR environment map, with both "
             "diffuse irradiance and specular prefiltering.",
             "Shadow mapping with a documented strategy for acne and peter-"
             "panning.",
             "At least one antialiasing method, with a measured frame-cost "
             "comparison against no antialiasing.",
             "A RenderDoc capture of one frame, annotated with what each draw "
             "call contributes.",
         ],
         "done": [
             "A material sphere grid sweeping roughness against metallic, "
             "rendered under a real HDR environment.",
             "Side-by-side shadow comparison showing the artifact before your "
             "fix and after it.",
             "A written paragraph on where the frame time actually goes, "
             "backed by the capture rather than by guesswork.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "The Graphics Pipeline, End to End",
 "subtitle": "Where a triangle goes, and what happens to it on the way.",
 "question": "What actually happens between a vertex buffer and a lit pixel?",
 "outcomes": [
     "Name every stage of the real-time pipeline and state what it consumes "
     "and produces.",
     "Explain why rendering is structured as a pipeline at all, and where the "
     "parallelism lives.",
     "Trace one triangle from object space to a shaded pixel.",
     "Distinguish fixed-function stages from programmable ones.",
     "Localise a rendering artifact to a stage before opening a debugger.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What problem is this?",
   "blurb": "Before the stages, the statement of the problem they solve."},

  {"t": "bullets", "kicker": "Framing", "title": "Rendering, stated precisely",
   "items": [
     "Given a description of a scene and a camera, produce an image.",
     ("Scene: geometry, materials, lights — a continuous 3D description.", 1),
     ("Camera: a position, an orientation, and a field of view.", 1),
     ("Image: a finite grid of pixels, each needing one colour.", 1),
     "",
     "The mismatch in that sentence is the whole subject.",
     ("The scene is continuous. The image is discrete.", 1),
     ("Every hard problem in graphics lives in that gap.", 1),
   ],
   "note": "Students arrive expecting graphics to be about colour and "
           "lighting. Push the framing hard here: continuous-to-discrete is "
           "the recurring theme, and aliasing, texture filtering, and "
           "antialiasing are all the same problem reappearing."},

  {"t": "callout", "title": "The central difficulty", "kind": "Key idea",
   "body": ["A scene is continuous. A screen is a finite grid of samples.",
            "Rendering is therefore a sampling problem wearing a geometry "
            "costume — and almost every artifact you will ever chase is "
            "a sampling failure.",
            "Hold on to this. It explains stage after stage that would "
            "otherwise look arbitrary."]},

  {"t": "bullets", "kicker": "Two answers", "title": "Two ways to answer the question",
   "items": [
     "<b>Ray tracing</b> — for each pixel, ask which geometry it sees.",
     ("Loop over pixels on the outside, geometry on the inside.", 1),
     ("Natural for light transport. Expensive to make interactive.", 1),
     "",
     "<b>Rasterization</b> — for each triangle, ask which pixels it covers.",
     ("Loop over geometry on the outside, pixels on the inside.", 1),
     ("Awkward for global effects. Astonishingly fast, and parallel.", 1),
     "",
     "This course is rasterization. CSCE 647 is the other loop order.",
   ],
   "note": "Worth stating explicitly that these are the same integral "
           "evaluated with the loops swapped. That framing pays off in 647."},

  {"t": "section", "label": "Part 2", "title": "The stages",
   "blurb": "Six stages, each consuming the previous one's output."},

  {"t": "table", "kicker": "The pipeline", "title": "What each stage does",
   "header": ["Stage", "Consumes", "Produces"],
   "widths": [3.3, 4.4, 4.4],
   "rows": [
     ["Application", "Scene graph, input", "Draw calls + vertex buffers"],
     ["Vertex processing", "Vertices in object space", "Vertices in clip space"],
     ["Clipping & assembly", "Clip-space vertices", "Triangles inside frustum"],
     ["Rasterization", "Screen-space triangles", "Fragments with interpolants"],
     ["Fragment processing", "Fragments", "Shaded colour + depth"],
     ["Output merging", "Shaded fragments", "Final framebuffer pixels"],
   ],
   "note": "Have students memorise the consumes/produces columns rather than "
           "the names. Knowing what crosses each boundary is what makes bug "
           "localisation possible."},

  {"t": "bullets", "kicker": "Stage 1", "title": "Application: deciding what to draw",
   "items": [
     "Runs on the CPU. The only stage you fully control.",
     "Culling: discard what cannot be seen before it costs anything.",
     ("Frustum culling — outside the camera volume.", 1),
     ("Occlusion culling — hidden behind something else.", 1),
     "Level of detail: choose a cheaper mesh when it will not be noticed.",
     "Sorting: opaque front-to-back for early-Z, transparent back-to-front.",
     "Batching: fewer, larger draw calls. Draw-call overhead is real cost.",
   ],
   "footnote": "The fastest triangle is the one you never submitted.",
   "note": "Emphasise that the biggest performance wins in real engines are "
           "almost always here, not in the shader."},

  {"t": "bullets", "kicker": "Stage 2", "title": "Vertex processing: moving points",
   "items": [
     "Runs once per vertex, massively in parallel, on the GPU.",
     "Its job: take each vertex from the space the artist authored it in to "
     "the space the rasterizer needs.",
     "",
     "Object space → world → camera → clip space.",
     ("One matrix multiply per step, composed into one matrix.", 1),
     "",
     "Also computes per-vertex attributes to be interpolated later:",
     ("normals, texture coordinates, tangents, vertex colours.", 1),
   ],
   "note": "Module 03 derives every one of these matrices. Here they only "
           "need to know the chain exists and why it is a chain."},

  {"t": "eq", "kicker": "Stage 2", "title": "The transform chain",
   "eqs": [
     ("v_clip  =  P · V · M · v_object",
      "One composed matrix per object. M = model, V = view, P = projection."),
     ("v_ndc  =  v_clip.xyz / v_clip.w",
      "The perspective divide. This is where distant things get smaller."),
     ("v_screen  =  viewport(v_ndc)",
      "Map the [-1,1] cube to pixel coordinates and a depth range."),
   ],
   "caption": "Three lines that every real-time renderer executes billions of "
              "times a second. Module 03 derives each one."},

  {"t": "bullets", "kicker": "Stage 3", "title": "Clipping and primitive assembly",
   "items": [
     "Vertices are grouped into triangles according to the index buffer.",
     "Triangles crossing the view frustum boundary are clipped.",
     ("A clipped triangle becomes one or more new triangles.", 1),
     ("The near plane is the one that <i>must</i> be clipped — "
      "geometry behind the eye produces nonsense after the divide.", 1),
     "",
     "Backface culling: discard triangles facing away from the camera.",
     ("Determined by winding order after projection — a signed area "
      "test, nothing more.", 1),
     ("Roughly halves the triangles on a closed mesh, for free.", 1),
   ]},

  {"t": "bullets", "kicker": "Stage 4", "title": "Rasterization: geometry becomes fragments",
   "items": [
     "For each triangle, determine which pixel samples it covers.",
     "Each covered sample becomes a <b>fragment</b>: a candidate pixel.",
     "",
     "A fragment is not a pixel. It is a proposal for one.",
     ("Several fragments may compete for the same pixel.", 1),
     ("Some will be rejected by the depth test, some blended.", 1),
     "",
     "Vertex attributes are interpolated across the triangle here — "
     "and the interpolation must account for perspective.",
   ],
   "note": "The fragment-is-not-a-pixel distinction prevents a large class of "
           "confusions later, especially around MSAA."},

  {"t": "bullets", "kicker": "Stage 5", "title": "Fragment processing: deciding colour",
   "items": [
     "Runs once per fragment. This is where almost all your shader code goes.",
     "Inputs: interpolated attributes, textures, uniforms, lights.",
     "Output: a colour, and usually a depth.",
     "",
     "Cost here scales with <b>overdraw</b>, not triangle count.",
     ("Shading a fragment that a later fragment covers is wasted work.", 1),
     ("Hence front-to-back sorting and early-Z: reject before shading.", 1),
   ],
   "footnote": "Fragment cost dominates most real frames. Optimise here last, "
               "but measure here first."},

  {"t": "bullets", "kicker": "Stage 6", "title": "Output merging: writing pixels",
   "items": [
     "Depth test: is this fragment nearer than what is already there?",
     "Stencil test: does a mask permit writing here?",
     "Blending: combine with what is already in the framebuffer.",
     ("Required for transparency, which is why transparency needs sorting.", 1),
     "",
     "Fixed-function and strictly ordered per pixel — even though "
     "everything before it ran out of order.",
   ],
   "note": "Good place to note that GPUs give the illusion of in-order "
           "results while executing wildly out of order. That guarantee costs "
           "hardware, and it is why blending is a fixed-function stage."},

  {"t": "section", "label": "Part 3", "title": "Why a pipeline?",
   "blurb": "The structure is not an accident of history. It is what makes "
            "the parallelism possible."},

  {"t": "two", "kicker": "Division of labour", "title": "Fixed-function and programmable",
   "lh": "Fixed-function (you configure)",
   "l": ["Primitive assembly", "Clipping", "Rasterization / coverage",
         "Depth and stencil test", "Blending",
         ("Hardwired because they are universal and benefit enormously from "
          "dedicated silicon.", 1)],
   "rh": "Programmable (you write)",
   "r": ["Vertex shader", "Fragment shader", "Geometry / tessellation (optional)",
         "Compute shader (adjacent)",
         ("Programmable because the interesting variation between renderers "
          "lives almost entirely here.", 1)],
   "note": "The boundary has moved over thirty years, always in the direction "
           "of more programmability — but coverage and blending have "
           "stayed fixed, which tells you something about their cost."},

  {"t": "bullets", "kicker": "The real reason", "title": "Where the parallelism lives",
   "items": [
     "Every stage is embarrassingly parallel over its own unit of work.",
     ("Vertex shading: vertices are independent.", 1),
     ("Rasterization: triangles are independent.", 1),
     ("Fragment shading: fragments are independent.", 1),
     "",
     "So the hardware can keep all stages busy at once on different data.",
     "This is why the pipeline is a <i>pipeline</i> and not a function call: "
     "throughput, not latency, is the design target.",
     "",
     "One frame's latency is ~16 ms. The pipeline depth is far longer than "
     "that — and it does not matter, because stages overlap.",
   ],
   "note": "Connect forward to CSCE 735. The GPU is a throughput machine, and "
           "every architectural decision follows from that."},

  {"t": "callout", "title": "Throughput, not latency", "kind": "The design target",
   "body": ["A GPU is not a fast CPU. It is a machine that tolerates enormous "
            "latency by always having other work ready.",
            "Every design choice downstream — wide SIMD, thousands of "
            "threads in flight, fixed-function coverage — follows from "
            "that one commitment.",
            "When you optimise graphics code, you are almost always feeding "
            "the machine better, not making any single operation faster."]},

  {"t": "section", "label": "Part 4", "title": "Reading artifacts",
   "blurb": "The practical payoff: the picture tells you which stage is "
            "wrong."},

  {"t": "table", "kicker": "Diagnosis", "title": "What the artifact tells you",
   "header": ["What you see", "Stage at fault", "Usual cause"],
   "widths": [4.1, 3.0, 5.0],
   "rows": [
     ["Nothing renders at all", "Vertex / assembly",
      "Wrong matrix order, or winding backwards into culling"],
     ["Geometry inside out", "Assembly",
      "Winding order or inverted scale in the model matrix"],
     ["Objects stretched with the window", "Vertex",
      "Aspect ratio not in the projection matrix"],
     ["Texture swims toward the horizon", "Rasterization",
      "Interpolation not perspective-correct"],
     ["Flickering between two surfaces", "Output merging",
      "Z-fighting — depth precision, usually near plane too close"],
     ["Jagged stair-stepped edges", "Rasterization",
      "Point sampling of coverage — aliasing (Module 09)"],
     ["Transparency in the wrong order", "Output merging",
      "Blending without back-to-front sorting"],
   ],
   "note": "This table is the single most useful artifact of Module 01. "
           "Students should keep it open for the whole course."},

  {"t": "code", "kicker": "The whole thing", "title": "The pipeline as twelve lines",
   "lang": "pseudocode", "code": """
for each draw call:
    for each vertex v in buffer:                 # vertex processing
        clip_pos[v] = P * V * M * v.position     #   (parallel)

    for each triangle t assembled from indices:  # assembly + clip
        if backfacing(t): continue
        for t' in clip_to_frustum(t):
            ndc  = t'.clip_pos / t'.clip_pos.w   # perspective divide
            tri  = viewport_transform(ndc)

            for each sample s covered by tri:    # rasterization
                attrs = perspective_correct_lerp(tri, s)
                color, depth = fragment_shader(attrs)   # (parallel)

                if depth_test(s, depth):         # output merging
                    framebuffer[s] = blend(framebuffer[s], color)
""",
   "caption": "Every renderer in this course is an elaboration of these "
              "twelve lines. Project 1 is literally writing them.",
   "note": "Tell students to copy this into their repo README now. By Module "
           "05 they will have implemented every line."},

  {"t": "bullets", "kicker": "This course", "title": "Where we are going",
   "items": [
     "<b>Modules 02–03</b> — the mathematics of moving points.",
     "<b>Modules 04–05</b> — rasterization and visibility. "
     "<i>Project 1: the software rasterizer.</i>",
     "<b>Modules 06–07</b> — light, colour, and the programmable "
     "pipeline.",
     "<b>Modules 08–09</b> — texturing and the sampling theory that "
     "makes it work.",
     "<b>Modules 10–11</b> — shadows and physically based shading. "
     "<i>Project 2: the GPU renderer.</i>",
     "<b>Modules 12–13</b> — geometry and animation.",
   ]},
 ],
 "takeaways": [
   "Rendering is a continuous-to-discrete sampling problem. Nearly every "
   "artifact in this course is a sampling failure in disguise.",
   "Rasterization and ray tracing are the same question with the loops "
   "swapped: per-triangle-find-pixels versus per-pixel-find-triangles.",
   "Six stages: application, vertex processing, clipping and assembly, "
   "rasterization, fragment processing, output merging. Know what crosses "
   "each boundary.",
   "The pipeline exists for throughput. Each stage is independently "
   "parallel over its own work unit, so all stages stay busy at once.",
   "A fragment is a candidate pixel, not a pixel. Several fragments compete "
   "for one pixel and most of them lose.",
   "The artifact tells you the stage. Learn to read the picture before you "
   "reach for the debugger.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The problem, stated honestly"),
  ("p", "A renderer is a function. It takes a scene and a camera, and it "
        "returns an image. Written that way the whole subject fits on one "
        "line, and the line is worth keeping in view, because everything "
        "else in this course is an implementation detail of it:"),
  ("eq", "image = render(scene, camera)"),
  ("p", "The difficulty is hidden in the types. A scene is continuous: "
        "surfaces are defined everywhere, light varies smoothly, and there is "
        "detail at every scale you care to look. An image is a finite grid of "
        "samples. Rendering has to cross that boundary, and it has to do it "
        "about sixteen million times per frame, sixty times a second."),
  ("callout", "Hold on to this",
   ["Every stage of the pipeline exists either to make the continuous-to-"
    "discrete crossing tractable, or to expose parallelism. If a stage looks "
    "arbitrary, you have not yet identified which of the two it is doing."]),
  ("p", "This framing pays off immediately. Jagged edges, shimmering "
        "textures, moir&eacute; patterns on a checkerboard floor, and the "
        "crawling you see on thin geometry in motion are not four different "
        "bugs. They are one phenomenon — undersampling — observed "
        "in four places. Module 09 treats it properly; for now, notice that "
        "you were told."),

  ("h1", "2 &nbsp; Two loop orders"),
  ("p", "There are exactly two sensible ways to organise the computation, "
        "and they differ only in which loop is on the outside."),
  ("table", ["", "Ray tracing", "Rasterization"],
   [["Outer loop", "Pixels", "Triangles"],
    ["Inner question", "Which geometry does this pixel see?",
     "Which pixels does this triangle cover?"],
    ["Natural strength", "Global effects: reflection, refraction, soft "
     "shadows, indirect light — anything requiring a secondary ray.",
     "Raw speed and parallelism. Coverage is a cheap geometric test that "
     "hardware does extremely well."],
    ["Natural weakness", "Expense. Every effect costs more rays.",
     "Anything non-local. A triangle does not know what else is in the "
     "scene, so reflections and shadows must be faked or precomputed."],
    ["Where it is used", "Film; offline rendering; increasingly, hybrid "
     "real-time.", "Real-time: games, visualisation, UI, VR."]],
   [0.14, 0.43, 0.43]),
  ("p", "This course is rasterization, because rasterization is where the "
        "pipeline lives and because you cannot understand a GPU without it. "
        "CSCE 647 takes the other loop order seriously and derives light "
        "transport properly. They are complementary, not competing — and "
        "modern engines run both at once."),

  ("h1", "3 &nbsp; The six stages"),
  ("p", "What follows is the canonical real-time pipeline. The names vary "
        "between APIs and the hardware fuses stages freely, but the logical "
        "structure has been stable for twenty-five years. Learn what crosses "
        "each boundary, not just the stage names — the boundaries are "
        "what let you localise a bug."),

  ("h2", "3.1 &nbsp; Application"),
  ("p", "The CPU side. This stage decides what to draw and in what order, "
        "and it is the only stage you control completely. Four jobs matter:"),
  ("ul", ["<b>Culling.</b> Discard geometry that cannot contribute. Frustum "
          "culling removes what is outside the camera volume; occlusion "
          "culling removes what is hidden behind something nearer.",
          "<b>Level of detail.</b> Swap in cheaper meshes when the object is "
          "small on screen. A 50,000-triangle model covering nine pixels is "
          "pure waste.",
          "<b>Sorting.</b> Opaque geometry front-to-back so the depth test "
          "rejects early; transparent geometry back-to-front because blending "
          "is order-dependent.",
          "<b>Batching.</b> Each draw call carries fixed overhead. Ten "
          "thousand draw calls of one triangle is far slower than one draw "
          "call of ten thousand triangles."]),
  ("callout", "Where the wins are",
   ["In real engines, the largest performance improvements almost always come "
    "from this stage — from <i>not drawing things</i> — and not "
    "from making shaders faster. The fastest triangle is the one you never "
    "submitted."]),

  ("h2", "3.2 &nbsp; Vertex processing"),
  ("p", "Runs once per vertex, in parallel, on the GPU. Its central job is "
        "to move each vertex from the coordinate system it was authored in to "
        "the one the rasterizer requires. This is a chain of four spaces:"),
  ("eq", "object &rarr; world &rarr; camera &rarr; clip"),
  ("table", ["Space", "Origin is at", "Why it exists"],
   [["Object", "The model's own pivot",
     "Artists model one object at a time, without knowing where it will be "
     "placed."],
    ["World", "A chosen scene origin",
     "A common frame so objects can be positioned relative to each other and "
     "lit by shared lights."],
    ["Camera (view)", "The eye, looking down &minus;Z",
     "Makes the camera's position and orientation implicit, so projection "
     "need not account for them."],
    ["Clip", "Homogeneous, pre-divide",
     "The space where the frustum becomes an axis-aligned box, which makes "
     "clipping a simple comparison."]],
   [0.17, 0.26, 0.57]),
  ("p", "Each step is a matrix multiplication, and matrix multiplication is "
        "associative, so all three collapse into one matrix per object. The "
        "vertex shader therefore does one multiply, not three. Module 03 "
        "derives each matrix from scratch."),
  ("code", """// The entire mathematical content of a basic vertex shader.
out_position = projection * view * model * vec4(in_position, 1.0);

// Note the order. Matrices apply right to left:
// model first (object -> world), then view, then projection.""",
   "Reversing this order is the single most common beginner error, and it "
   "usually produces a black screen rather than a wrong image, which makes it "
   "harder to diagnose."),

  ("h2", "3.3 &nbsp; Clipping and primitive assembly"),
  ("p", "Vertices are grouped into triangles using the index buffer, and "
        "triangles that cross the frustum boundary are cut. Clipping against "
        "the side planes is an optimisation; clipping against the <i>near</i> "
        "plane is a correctness requirement. Geometry behind the eye has "
        "negative <i>w</i>, and dividing by a negative <i>w</i> turns the "
        "projection inside out — points behind the camera land in front "
        "of it, mirrored. This is why the near plane cannot be zero."),
  ("p", "Backface culling also happens here. After projection, compute the "
        "signed area of the triangle in screen space; its sign is the winding "
        "direction, and one sign means the triangle faces away. On a closed "
        "mesh this removes about half of all triangles for the cost of one "
        "cross product."),
  ("eq", "2A = (x&#8321;&minus;x&#8320;)(y&#8322;&minus;y&#8320;) &minus; (x&#8322;&minus;x&#8320;)(y&#8321;&minus;y&#8320;)"),
  ("cap", "Signed area of a screen-space triangle. The sign is the winding; "
          "the magnitude is twice the area, which Module 04 reuses for "
          "barycentric coordinates."),

  ("h2", "3.4 &nbsp; Rasterization"),
  ("p", "For each triangle, find the sample points it covers. Each covered "
        "sample becomes a <b>fragment</b>, carrying interpolated copies of "
        "every vertex attribute."),
  ("callout", "A fragment is not a pixel",
   ["A fragment is a <i>candidate</i> for a pixel — a proposal that this "
    "triangle should determine this pixel's colour.",
    "Many fragments may be generated for one pixel by different triangles. "
    "The depth test resolves most of that competition; blending resolves the "
    "rest. Keeping the distinction clear prevents real confusion later, "
    "especially around multisampling, where a pixel has several coverage "
    "samples but may run the fragment shader only once."]),
  ("p", "Attribute interpolation here must account for perspective. Linear "
        "interpolation in screen space is wrong for any attribute that varies "
        "linearly in 3D, because projection is not an affine map. Module 04 "
        "derives the correction; the symptom when you get it wrong is a "
        "texture that appears to slide or swim across a surface as the camera "
        "moves, most visible on large floor polygons."),

  ("h2", "3.5 &nbsp; Fragment processing"),
  ("p", "Runs once per fragment, and this is where nearly all shader code "
        "lives: texture lookups, lighting, material evaluation. The output is "
        "a colour and usually a depth."),
  ("p", "The cost of this stage scales with <b>overdraw</b> — how many "
        "fragments are generated per pixel — not with triangle count. "
        "Shading a fragment that a nearer fragment will later cover is wasted "
        "work, which is the entire justification for front-to-back sorting "
        "and for hardware early-Z, where the depth test is moved <i>before</i> "
        "the fragment shader so that doomed fragments never execute it."),
  ("callout", "Early-Z has conditions",
   ["Early-Z is disabled automatically if the fragment shader writes to "
    "<code>gl_FragDepth</code>, or uses <code>discard</code>, because then "
    "the hardware cannot know the fragment's depth before running it.",
    "This is a classic silent performance cliff: adding one "
    "<code>discard</code> for alpha-testing foliage can cost far more than "
    "the discard itself appears to."]),

  ("h2", "3.6 &nbsp; Output merging"),
  ("p", "The last stage, fixed-function, and strictly ordered per pixel. "
        "Depth test, stencil test, blending, and the write. The ordering "
        "guarantee is significant: everything upstream ran out of order "
        "across thousands of concurrent threads, yet blending must behave as "
        "though triangles were processed in submission order. Hardware spends "
        "real resources to maintain that illusion, which is a large part of "
        "why blending has never become programmable."),

  ("break",),
  ("h1", "4 &nbsp; Why a pipeline at all"),
  ("p", "The pipeline structure is not historical accident. Each stage is "
        "embarrassingly parallel over its own unit of work — vertices "
        "are independent of each other, triangles of each other, fragments of "
        "each other — so the hardware can run all six stages "
        "simultaneously on different data. While fragments from triangle "
        "<i>n</i> are being shaded, triangle <i>n+1</i> is being rasterized "
        "and the vertices of <i>n+2</i> are being transformed."),
  ("p", "The consequence is that a GPU optimises <b>throughput</b>, not "
        "latency. A single vertex may take microseconds to traverse the whole "
        "pipeline — an eternity — and it does not matter, because "
        "millions of other vertices are in flight at the same time. This one "
        "commitment explains nearly every architectural feature of GPUs: very "
        "wide SIMD, enormous register files, thousands of resident threads, "
        "and a willingness to tolerate memory latency that would be "
        "catastrophic on a CPU."),
  ("callout", "The optimisation mindset this implies",
   ["On a CPU you usually make code faster by reducing the work in the "
    "critical path.",
    "On a GPU you usually make code faster by <i>feeding the machine "
    "better</i>: fewer state changes, better batching, higher occupancy, "
    "more coherent memory access. The arithmetic is rarely the bottleneck.",
    "CSCE 614 and CSCE 735 make this precise. For now, be suspicious of any "
    "graphics optimisation that counts instructions."]),

  ("h1", "5 &nbsp; Reading artifacts"),
  ("p", "Because each stage has a well-defined input and output, a visual "
        "artifact usually implicates one stage. Developing this reflex early "
        "will save you more time than any other single habit in this course. "
        "Keep the following table somewhere you will actually look at it."),
  ("table", ["What you see", "Stage", "Usual cause", "First thing to check"],
   [["Black screen, nothing drawn", "Vertex / assembly",
     "Matrix multiplication order reversed, or all triangles culled by "
     "winding.",
     "Disable backface culling. If geometry appears, it is winding."],
    ["Geometry appears inside-out", "Assembly",
     "Negative determinant in the model matrix (mirrored scale) flipping "
     "winding.",
     "Check for a negative scale component."],
    ["Image stretches when window resizes", "Vertex",
     "Aspect ratio not recomputed in the projection matrix.",
     "Is the projection rebuilt on resize?"],
    ["Texture swims or slides on a floor", "Rasterization",
     "Screen-space linear interpolation without perspective correction.",
     "Interpolate attribute/w, then divide by interpolated 1/w."],
    ["Two surfaces flicker against each other", "Output merging",
     "Z-fighting from insufficient depth precision.",
     "Push the near plane out. Precision loss is dominated by near, not far."],
    ["Hard jagged edges, crawling in motion", "Rasterization",
     "Point-sampled coverage — aliasing.",
     "Module 09. Enable MSAA to confirm the diagnosis."],
    ["Transparent objects in wrong order", "Output merging",
     "Blending is order-dependent and geometry was not sorted.",
     "Sort transparent draws back-to-front."],
    ["Shadows detached from objects", "Fragment",
     "Shadow map depth bias too large (peter-panning).",
     "Module 10."]],
   [0.22, 0.13, 0.35, 0.30]),

  ("h1", "6 &nbsp; The pipeline in twelve lines"),
  ("p", "Everything above, condensed. Project 1 asks you to implement "
        "literally this, so copy it into your repository now and delete "
        "comments as you replace them with working code."),
  ("code", """for each draw call:
    # ---- vertex processing (parallel over vertices)
    for each vertex v:
        clip[v] = P * V * M * v.position

    # ---- assembly, culling, clipping
    for each triangle t:
        if backfacing(t):     continue
        for t2 in clip_near(t):

            # ---- perspective divide + viewport
            ndc = t2.clip.xyz / t2.clip.w
            tri = viewport(ndc)

            # ---- rasterization (parallel over fragments)
            for each sample s covered by tri:
                a = perspective_correct_lerp(tri, s)
                color, depth = fragment_shader(a)

                # ---- output merging (ordered)
                if depth_test(s, depth):
                    framebuffer[s] = blend(framebuffer[s], color)""",
   "By the end of Module 05 you will have written every line of this with no "
   "graphics API underneath it."),
 ],
 "resources": [
   ("GAMES101 Lecture 01 — Overview of Computer Graphics",
    "https://sites.cs.ucsb.edu/~lingqi/teaching/games101.html",
    "The same framing of what graphics is and why. Watch before this "
    "module."),
   ("CMU 15-462 Lecture 01 — Course Introduction",
    "https://15462.courses.cs.cmu.edu/",
    "Crane's framing of graphics as a sampling-and-representation problem "
    "is unusually clear and complements this module directly."),
   ("Cem Yuksel — Introduction to Computer Graphics, Lecture 1",
    "https://graphics.cs.utah.edu/courses/cs6610/",
    "The most hardware-grounded overview of the three. Good second pass."),
   ("Scratchapixel — 'An Overview of the Rasterization Algorithm'",
    "https://www.scratchapixel.com/lessons/3d-basic-rendering/rasterization-practical-implementation/overview-rasterization-algorithm.html",
    "Written, with code, covering the twelve-line pipeline in detail."),
   ("LearnOpenGL — Hello Triangle",
    "https://learnopengl.com/Getting-started/Hello-Triangle",
    "Mechanics only: how the stages appear in an actual API. Do not take "
    "the theory from here."),
 ],
 "exercises": [
   "Set up your portfolio repository. Add a README containing the twelve-line "
   "pipeline from &sect;6, and a checklist of the six stages. You will delete "
   "items from it as you implement them.",
   "Write a program that produces a PNG with no graphics library: allocate a "
   "framebuffer, write a gradient, save it. You need this harness for every "
   "module through Module 05, and getting it out of the way now means you "
   "never again confuse an image-writing bug with a rendering bug.",
   "Draw a filled triangle into that framebuffer with the crudest method you "
   "can think of — brute-force test every pixel against the triangle, "
   "however you like. It will be slow and probably slightly wrong along the "
   "edges. Keep it; Module 04 replaces it and you will want the comparison.",
   "For each of the eight artifacts in the diagnosis table of &sect;5, write "
   "one sentence predicting what you would check first. Then keep the file "
   "— you will revisit your predictions at the end of the course and "
   "some of them will be wrong in instructive ways.",
   "Install RenderDoc. Capture a single frame from any game or application on "
   "your machine and find: the draw call count, the depth buffer, and one "
   "shader's source. You are not expected to understand the frame yet; the "
   "goal is to know the tool exists and opens.",
 ],
 "selfcheck": [
   "Name the six stages in order, and for each one state what it consumes and "
   "what it produces.",
   "Why must the near clip plane be greater than zero? What specifically goes "
   "wrong at <i>w</i> = 0, and what does geometry behind the eye look like if "
   "you fail to clip it?",
   "Explain the difference between a fragment and a pixel, and give a "
   "situation where one pixel is associated with many fragments.",
   "Rasterization and ray tracing differ in loop order. State both loop "
   "orders, and give one effect that is natural in each and awkward in the "
   "other.",
   "A GPU targets throughput rather than latency. Give two concrete "
   "architectural consequences of that choice, and one consequence for how "
   "you should optimise graphics code.",
   "You see a texture on a large floor plane appear to slide as the camera "
   "moves forward. Which stage is at fault and what is the specific cause?",
 ],
},

]

# --- additional module batches ----------------------------------------------
for _b in ("c641_b2", "c641_b3", "c641_b4", "c641_b5"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
