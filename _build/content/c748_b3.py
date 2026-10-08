# -*- coding: utf-8 -*-
"""CSCE 748 — Modules 08-13."""

MODULES = [

# =========================================================== MODULE 08 ======
{
 "n": 8,
 "title": "Gradient-Domain Processing",
 "subtitle": "Editing derivatives instead of values.",
 "question": "Why does pasting in the gradient domain look seamless?",
 "outcomes": [
     "Explain why humans perceive gradients rather than absolute values.",
     "Derive the Poisson equation from a least-squares gradient fit.",
     "Implement seamless cloning.",
     "Apply gradient-domain methods beyond compositing.",
     "Solve the resulting linear system efficiently.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why gradients",
   "blurb": "The visual system does not measure absolute brightness."},

  {"t": "callout", "title": "Vision responds to local differences, not absolute levels",
   "kind": "The perceptual basis",
   "body": ["<b>Retinal cells are differencing operators.</b> The "
            "centre-surround receptive field computes a local contrast, not "
            "an intensity.",
            "<b>Which is why simultaneous contrast illusions work</b> "
            "— identical grey patches look different against different "
            "surrounds.",
            "<b>And why you can read a page in sunlight and in a dim "
            "room</b>, despite a thousandfold difference in absolute "
            "luminance.",
            "<b>So: if you preserve the gradients, the result looks "
            "right</b> — even if every absolute value has changed. This "
            "is the entire premise of the module."]},

  {"t": "callout", "title": "The seam is a gradient discontinuity",
   "kind": "The reframing",
   "body": ["<b>Pasting a region creates a visible boundary because the "
            "values jump</b> at the edge — a large gradient where the "
            "scene has none.",
            "<b>If instead you copy the source's <i>gradients</i> and force "
            "the boundary values to match the destination</b>, no "
            "discontinuity exists.",
            "<b>The interior absolute values change</b> — the pasted "
            "region takes on the destination's colour and brightness.",
            "<b>And that is exactly what you want.</b> A face pasted from a "
            "sunlit photograph into a shaded one should become shaded."]},

  {"t": "section", "label": "Part 2", "title": "The Poisson equation",
   "blurb": "Where it comes from."},

  {"t": "eq", "kicker": "Derivation", "title": "From least squares to Poisson",
   "eqs": [
     ("minimise ∫∫ ‖∇f − v‖² over the region Ω",
      "Find the function f whose gradient best matches a guide field v, in "
      "a least-squares sense."),
     ("subject to  f = f* on ∂Ω",
      "With the boundary values fixed to the destination image. These "
      "constraints are what make the solution unique."),
     ("⟹  ∇²f = ∇·v     (the Poisson equation)",
      "The Euler-Lagrange condition. A linear PDE, discretised into a "
      "sparse linear system."),
   ],
   "caption": "A variational problem whose solution is a standard PDE. "
              "Discretised, it is one equation per pixel.",
   "note": "The derivation matters: it shows the method is a least-squares "
           "fit rather than an arbitrary procedure."},

  {"t": "code", "kicker": "Discrete", "title": "The linear system",
   "lang": "text", "code": """
  For each INTERIOR pixel p in the region:

     |N(p)| · f(p)  -  SUM over neighbours q in interior: f(q)
        =  SUM over ALL neighbours q: v(p,q)
         + SUM over BOUNDARY neighbours q: f*(q)
                                            ^ known destination values

  where v(p,q) = g(p) - g(q)   from the SOURCE image's gradients.

  This is A x = b with:
     A  sparse, symmetric, positive definite (a Laplacian matrix)
     x  the unknown interior pixel values
     b  the divergence of the guide field, plus boundary terms

  One system per colour channel. Solve with conjugate gradient
  or a multigrid method.
""",
   "caption": "Five non-zeros per row. The matrix is the graph Laplacian "
              "of the pixel grid, which is why the solvers are so well "
              "developed.",
   "note": "Recognising it as a Laplacian system connects it to the "
           "pressure solve in CSCE 649 Module 11."},

  {"t": "callout", "title": "The same system as the fluid pressure solve",
   "kind": "A connection worth noticing",
   "body": ["<b>CSCE 649 Module 11 solved ∇²p = ∇·u* to project a "
            "velocity field.</b>",
            "<b>This module solves ∇²f = ∇·v to integrate a gradient "
            "field.</b>",
            "<b>Same matrix, same solvers, same scaling behaviour.</b> "
            "Sparse, symmetric, positive definite; conjugate gradient with a "
            "preconditioner, or multigrid for speed.",
            "<b>Poisson problems recur throughout computational "
            "science</b>, and recognising one saves you from reinventing its "
            "solution. Multigrid is the asymptotically optimal answer in "
            "both cases."]},

  {"t": "section", "label": "Part 3", "title": "Applications",
   "blurb": "More than compositing."},

  {"t": "table", "kicker": "Guide field", "title": "Choose v and get a different tool",
   "header": ["Guide field v", "Result"],
   "widths": [4.6, 7.5],
   "rows": [
     ["Source gradients", "<b>Seamless cloning</b>"],
     ["<b>Max of source and destination gradients</b>", "<b>Mixed cloning — preserves destination texture</b>"],
     ["Source gradients, attenuated", "Softened insertion"],
     ["<b>Zero</b>", "<b>Object removal — smooth interpolation inward</b>"],
     ["Destination gradients with colour changed", "Local recolouring"],
     ["<b>Attenuated large gradients</b>", "<b>Tone mapping (Module 04)</b>"],
   ],
   "footnote": "<b>One solver, many tools.</b> The guide field is the "
               "entire interface.",
   "note": "That changing only v gives a different application is the "
           "elegant part and is worth demonstrating."},

  {"t": "callout", "title": "Mixed gradients preserve what is underneath",
   "kind": "The most useful variant",
   "body": ["<b>Plain seamless cloning replaces the destination entirely</b> "
            "within the region — including any texture that was there.",
            "<b>Mixed cloning takes, at each pixel, whichever gradient is "
            "larger</b> — the source's or the destination's.",
            "<b>So strong destination texture survives</b> and the source's "
            "content is laid over it rather than replacing it.",
            "<b>This is how you paste writing onto a brick wall</b> and "
            "have the brick texture show through. It is a one-line change "
            "and it looks like magic."]},

  {"t": "section", "label": "Part 4", "title": "Limits",
   "blurb": "Where it fails, and how to solve it quickly."},

  {"t": "bullets", "kicker": "Failures", "title": "When gradient-domain compositing fails",
   "items": [
     "<b>Very different colours.</b> Forcing the boundary to match can "
     "shift the interior drastically — a dark object pasted into a bright "
     "scene washes out.",
     "",
     "<b>Strong structure crossing the boundary</b> that does not "
     "continue — the solution smears to reconcile it.",
     "",
     "<b>Large regions</b> — the influence of the boundary decays, so "
     "the interior can drift.",
     "",
     "<b>Mismatched texture</b>, which no amount of boundary matching "
     "fixes. The composite is seamless and obviously wrong.",
     "",
     "<b>And it is not fast</b> — a global solve per edit.",
   ],
   "note": "The 'seamless and obviously wrong' failure is worth showing. "
           "The method fixes seams, not plausibility."},

  {"t": "callout", "title": "Solving it fast enough to be interactive",
   "kind": "The engineering",
   "body": ["<b>Direct sparse Cholesky</b> works for modest regions and "
            "can be factored once if the region does not change.",
            "<b>Conjugate gradient with a preconditioner</b> is the "
            "standard choice — the matrix is symmetric positive definite "
            "(Module 02 of CSCE 608's CG discussion applies).",
            "<b>Multigrid is asymptotically optimal</b> — O(n) rather "
            "than O(n^1.5), and it is what makes megapixel edits "
            "interactive.",
            "<b>Or approximate:</b> mean-value coordinates give a "
            "closed-form result that is visually close for a fraction of the "
            "cost, and is what several interactive tools actually use."]},
 ],
 "takeaways": [
   "Vision responds to local differences rather than absolute levels, so "
   "preserving gradients preserves appearance even when every value "
   "changes.",
   "A visible seam is a gradient discontinuity; copying gradients and fixing "
   "the boundary to the destination removes it by construction.",
   "Minimising the squared difference between the result's gradient and a "
   "guide field, with Dirichlet boundary conditions, gives the Poisson "
   "equation.",
   "Discretised it is a sparse symmetric positive definite system — the "
   "same matrix as the fluid pressure solve in CSCE 649.",
   "Changing the guide field changes the application: source gradients clone, "
   "zero removes objects, attenuated large gradients tone map.",
   "Mixed gradients take whichever is larger, so destination texture survives "
   "— which is how writing is pasted onto a brick wall.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why gradients"),
  ("callout", "The visual system measures differences, not levels",
   ["<b>Retinal ganglion cells have centre-surround receptive fields</b> "
    "— excited by light in the centre and inhibited by light in the "
    "surround, or the reverse. <b>The output is a local contrast, not an "
    "intensity.</b> Absolute brightness is largely discarded at the first "
    "stage of processing.",
    "<b>This is why simultaneous contrast illusions work.</b> Two patches of "
    "identical grey look markedly different against light and dark "
    "surrounds, because what is reported is the difference and the "
    "difference genuinely differs.",
    "<b>And why you can read a page in direct sunlight and in a dim "
    "room</b>, despite a factor of a thousand in absolute luminance. The "
    "contrast between ink and paper is roughly constant, and that is what is "
    "being measured.",
    "<b>So if you preserve the gradients, the result looks right</b> "
    "— even if every absolute value in the image has changed. <b>That "
    "is the entire premise of this module</b>, and it is why a technique "
    "that discards absolute values can nonetheless produce convincing "
    "images."]),
  ("callout", "A seam is a gradient discontinuity",
   ["<b>Pasting a region from one image into another creates a visible "
    "boundary because the values jump</b> at the edge — a large "
    "gradient where the underlying scene has none. The eye, which is "
    "measuring gradients, detects it immediately.",
    "<b>So reframe the operation.</b> Instead of copying the source's "
    "<i>values</i>, copy its <i>gradients</i>, and require the result to "
    "match the destination exactly along the boundary.",
    "<b>Then no discontinuity exists at the boundary by construction</b>, "
    "because the boundary values are the destination's own.",
    "<b>The interior absolute values change</b> — the pasted region "
    "takes on the destination's overall brightness and colour cast, since "
    "that is what the boundary conditions propagate inward. <b>And that is "
    "exactly what you want:</b> a face pasted from a sunlit photograph into "
    "a shaded scene <i>should</i> become shaded. The method does the colour "
    "matching for free, as a consequence of its structure rather than as an "
    "additional step."]),

  ("h1", "2 &nbsp; The Poisson equation"),
  ("eq", "min<sub>f</sub> &int;&int;<sub>&Omega;</sub> "
         "&#8214;&nabla;f &minus; v&#8214;&#178; "
         "&nbsp;&nbsp;subject to&nbsp;&nbsp; f = f* on &part;&Omega;"),
  ("p", "Find the function f over the region &Omega; whose gradient most "
        "closely matches a guide field v, in a least-squares sense, subject "
        "to f matching the destination image f* on the region's boundary. "
        "<b>The boundary conditions are what make the solution unique</b> "
        "— without them, any constant could be added to f."),
  ("eq", "&rArr; &nbsp; &nabla;&#178;f = &nabla; &middot; v"),
  ("p", "The Euler&ndash;Lagrange condition for that variational problem is "
        "the <b>Poisson equation</b>: the Laplacian of the unknown equals "
        "the divergence of the guide field. <b>The derivation matters</b> "
        "— it establishes that this is a principled least-squares fit "
        "rather than a procedure that happens to work."),
  ("code", """For each INTERIOR pixel p:
  |N(p)|*f(p) - SUM_{q in interior} f(q)
     = SUM_{all q} v(p,q)  +  SUM_{q on boundary} f*(q)
                                        ^ known destination values
  where v(p,q) = g(p) - g(q)   from the SOURCE image

A x = b with A sparse, symmetric, positive definite (a Laplacian),
x the unknown interior values, b the divergence plus boundary terms.
One system per colour channel."""),
  ("callout", "This is the same system as the fluid pressure solve",
   ["<b>CSCE 649 Module 11 solved &nabla;&#178;p = &nabla;&middot;u* to "
    "project a velocity field onto the divergence-free subspace.</b>",
    "<b>This module solves &nabla;&#178;f = &nabla;&middot;v to integrate a "
    "gradient field into an image.</b>",
    "<b>Same matrix, same solvers, same scaling behaviour.</b> The matrix is "
    "the graph Laplacian of the pixel grid: five non-zeros per row, "
    "symmetric, positive definite. Conjugate gradient with a preconditioner "
    "works; multigrid is asymptotically optimal.",
    "<b>Poisson problems recur throughout computational science</b> — "
    "electrostatics, heat flow, incompressible flow, image integration "
    "— and recognising one saves reinventing its solution. The decades "
    "of work on multigrid solvers were not done for image editing, and image "
    "editing benefits from all of it."]),

  ("break",),
  ("h1", "3 &nbsp; Applications"),
  ("table", ["Guide field v", "Resulting tool"],
   [["<b>The source image's gradients</b>",
     "<b>Seamless cloning.</b> The source's content appears, taking on the "
     "destination's lighting."],
    ["<b>At each pixel, whichever of the source and destination gradients "
     "is larger</b>",
     "<b>Mixed seamless cloning.</b> See below."],
    ["<b>Source gradients, scaled down</b>",
     "A softened insertion — the source's content appears faintly, as "
     "though printed on the destination."],
    ["<b>Zero everywhere</b>",
     "<b>Object removal.</b> With no gradient to match, the solution is the "
     "smoothest function satisfying the boundary — a membrane "
     "interpolating inward from the surrounding content. The simplest form "
     "of inpainting."],
    ["<b>Destination gradients with the colour channels altered</b>",
     "Local recolouring that respects the existing structure."],
    ["<b>The image's own gradients with large ones attenuated</b>",
     "<b>Gradient-domain tone mapping</b> (Module 04)."]],
   [0.37, 0.63]),
  ("p", "<b>One solver, many tools.</b> The guide field is the entire "
        "interface, and the elegance of that is worth noticing: a single "
        "piece of numerical machinery supports compositing, inpainting, "
        "recolouring, and tone mapping, and the difference between them is "
        "a few lines constructing v."),
  ("callout", "Mixed gradients preserve what is underneath",
   ["<b>Plain seamless cloning replaces the destination entirely within the "
    "region</b> — whatever texture was there is overwritten, because "
    "the guide field comes only from the source.",
    "<b>Mixed cloning takes, at each pixel and in each direction, whichever "
    "gradient has the larger magnitude</b> — the source's or the "
    "destination's.",
    "<b>So strong destination texture survives.</b> Where the destination "
    "has a prominent edge and the source is smooth, the destination's "
    "gradient wins and the edge is retained; where the source has content "
    "and the destination is flat, the source wins.",
    "<b>This is how you paste handwriting onto a brick wall</b> and have the "
    "brick texture show through the strokes, or paste an object onto a "
    "textured surface and have the texture read through it. <b>It is a "
    "one-line change to the guide field construction</b> and the result "
    "looks disproportionately impressive."]),

  ("h1", "4 &nbsp; Limits and solving"),
  ("ul", ["<b>Very different colours.</b> Forcing the boundary to match the "
          "destination propagates inward, so a dark object pasted into a "
          "bright scene is brightened throughout — sometimes to the "
          "point of washing out. <b>The method matches lighting, which is "
          "usually desirable and occasionally destructive.</b>",
          "<b>Strong structure crossing the boundary that does not "
          "continue.</b> If an edge in the source meets the boundary and has "
          "no counterpart in the destination, the solution smears to "
          "reconcile the two, producing a visible smudge.",
          "<b>Large regions.</b> The boundary's influence decays with "
          "distance, so the interior of a very large pasted region can drift "
          "away from both images.",
          "<b>Mismatched texture, perspective, or scale.</b> <b>No amount of "
          "boundary matching fixes a composite that is wrong for other "
          "reasons</b> — the result is seamless and obviously fake, "
          "which is a distinctive and instructive failure. <b>The method "
          "removes seams; it does not create plausibility.</b>",
          "<b>And it is not fast.</b> Each edit requires a global solve over "
          "the region, which is why the next callout matters for anything "
          "interactive."]),
  ("callout", "Solving it fast enough to be interactive",
   ["<b>Direct sparse Cholesky factorisation</b> works well for modest "
    "regions, and the factorisation can be reused if the region's shape is "
    "unchanged — so dragging a pasted object around is cheap after the "
    "first solve.",
    "<b>Preconditioned conjugate gradient</b> is the standard iterative "
    "choice, since the matrix is symmetric positive definite. An incomplete "
    "Cholesky preconditioner substantially reduces the iteration count.",
    "<b>Multigrid is asymptotically optimal</b> — O(n) rather than the "
    "O(n<super>1.5</super>) of preconditioned CG on this problem — and "
    "it is what makes megapixel-scale gradient-domain editing interactive.",
    "<b>Or approximate.</b> <b>Mean-value coordinates</b> give a "
    "closed-form interpolation of the boundary difference that is visually "
    "very close to the true Poisson solution at a small fraction of the "
    "cost, requires no solver at all, and is what several interactive tools "
    "actually ship. <b>An approximation that is visually indistinguishable "
    "is not a compromise</b> when the criterion is perceptual."]),
 ],
 "resources": [
   ("P&eacute;rez, Gangnet & Blake &mdash; Poisson Image Editing (free)",
    "https://www.cs.jhu.edu/~misha/Fall07/Papers/Perez03.pdf",
    "The paper. Seamless cloning, mixed gradients, and the variants of "
    "&sect;3, in eight pages. One of the most immediately useful graphics "
    "papers ever written."),
   ("CMU 15-463 &mdash; gradient-domain processing lecture and assignment "
    "(free)",
    "http://graphics.cs.cmu.edu/courses/15-463/",
    "The derivation and the implementation. The assignment is Project 2's "
    "third option."),
   ("Bhat et al. &mdash; GradientShop: A Gradient-Domain Optimization "
    "Framework (free)",
    "https://grail.cs.washington.edu/projects/gradientshop/",
    "The general framework of &sect;3 — many image operations as one "
    "gradient-domain optimisation."),
   ("Farbman et al. &mdash; Coordinates for Instant Image Cloning (free)",
    "https://www.cse.huji.ac.il/~danix/mvclone/",
    "Mean-value coordinates — the fast approximation in &sect;4."),
 ],
 "exercises": [
   "Demonstrate simultaneous contrast with two identical grey patches on "
   "different backgrounds, and measure that the pixel values are equal.",
   "Paste a region naively and observe the seam. Measure the gradient "
   "magnitude at the boundary.",
   "Derive the discrete Poisson system for a small region by hand and "
   "confirm the matrix structure.",
   "Implement seamless cloning with a conjugate gradient solver. Paste a "
   "face from a sunlit photograph into a shaded one and observe the colour "
   "adaptation.",
   "Implement mixed gradient cloning and paste text onto a textured surface. "
   "Compare against plain cloning.",
   "Set the guide field to zero and perform object removal. Compare against "
   "a modern inpainting tool.",
   "Implement gradient-domain tone mapping (Module 04) using the same solver "
   "and confirm the machinery is unchanged.",
   "Construct a failure case: paste something at the wrong scale and "
   "perspective, and observe that the result is seamless and obviously "
   "wrong.",
   "Compare solve times for direct Cholesky, preconditioned CG, and a "
   "multigrid solver at several region sizes. Plot the scaling.",
   "Implement mean-value coordinate cloning and compare against the true "
   "Poisson solution, both visually and numerically.",
 ],
 "selfcheck": [
   "Why does the visual system respond to gradients, and what two everyday "
   "observations follow?",
   "Why is a seam a gradient discontinuity, and what does fixing the "
   "boundary achieve?",
   "Derive the Poisson equation from the least-squares gradient fit.",
   "What is the structure of the discrete system, and what other problem "
   "shares it?",
   "Name six guide fields and the tool each produces.",
   "What do mixed gradients do, and give an example.",
   "Give five situations where gradient-domain compositing fails.",
   "Name four ways to solve the system, and say which is asymptotically "
   "optimal.",
 ],
},

# =========================================================== MODULE 09 ======
{
 "n": 9,
 "title": "Light Fields and Plenoptic Cameras",
 "subtitle": "Capturing rays instead of pixels.",
 "question": "What if you recorded direction as well as position?",
 "outcomes": [
     "Define the plenoptic function and the 4D light field.",
     "Explain how a plenoptic camera trades resolution for angle.",
     "Explain digital refocusing and synthetic aperture.",
     "Explain why light field cameras failed commercially.",
     "Identify where light fields are actually used.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The plenoptic function",
   "blurb": "Everything that could be seen."},

  {"t": "eq", "kicker": "Plenoptic", "title": "From seven dimensions to four",
   "eqs": [
     ("P(x, y, z, θ, φ, λ, t)",
      "The full plenoptic function: radiance at every position, in every "
      "direction, at every wavelength and time. Seven dimensions."),
     ("L(u, v, s, t)",
      "Fix time and wavelength, and assume free space, where radiance is "
      "constant along a ray (CSCE 647 Module 01). A ray is then determined "
      "by where it crosses two planes."),
   ],
   "caption": "<b>Radiance invariance reduces five spatial dimensions to "
              "four.</b> The same fact that made ray tracing a lookup makes "
              "light fields finite.",
   "note": "The connection to CSCE 647 Module 01 is exact and worth "
           "drawing — the same invariance, used in reverse."},

  {"t": "callout", "title": "A photograph is a 2D slice of a 4D function",
   "kind": "The reframing",
   "body": ["<b>A conventional camera integrates over the aperture</b>, "
            "collapsing all the rays arriving at a sensor point into one "
            "value.",
            "<b>That integration is irreversible</b> — the angular "
            "information is destroyed at capture.",
            "<b>A light field camera records the rays separately</b>, "
            "keeping which direction each one came from.",
            "<b>So the integration can be performed afterwards, "
            "differently</b> — a different aperture, a different focus, a "
            "different viewpoint. <b>Capture the function; compute the "
            "photograph.</b>"]},

  {"t": "section", "label": "Part 2", "title": "Capture",
   "blurb": "Three ways to sample four dimensions."},

  {"t": "table", "kicker": "Capture", "title": "How to record a light field",
   "header": ["Method", "How", "Trade"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["Camera array", "Many cameras on a grid", "<b>Full resolution; bulky, expensive</b>"],
     ["Gantry", "One camera moved mechanically", "<b>Static scenes only</b>"],
     ["<b>Plenoptic (microlens)</b>", "A microlens array over the sensor", "<b>One shot; resolution falls hard</b>"],
     ["Coded mask", "A patterned mask near the sensor", "Compressive; needs reconstruction"],
   ],
   "footnote": "<b>A plenoptic camera trades spatial resolution for "
               "angular</b> — and the trade is severe.",
   "note": "The severity of the resolution trade is the commercial story "
           "in Part 4."},

  {"t": "callout", "title": "The resolution trade is brutal",
   "kind": "The arithmetic that decided the market",
   "body": ["<b>A microlens array places a small lens over each group of "
            "sensor pixels.</b> The pixels under one microlens record "
            "different <i>directions</i>.",
            "<b>So a 20 megapixel sensor with 10×10 angular samples "
            "gives a 0.2 megapixel image.</b>",
            "<b>That is a 200,000-pixel photograph from a 20-million-pixel "
            "sensor</b> — and consumers compare megapixels.",
            "<b>Later designs recovered some resolution</b> by refocusing "
            "the microlenses, trading angular range instead. The trade "
            "moved; it did not disappear."]},

  {"t": "section", "label": "Part 3", "title": "What you can compute",
   "blurb": "The payoff for capturing four dimensions."},

  {"t": "bullets", "kicker": "Operations", "title": "Rendering from a light field",
   "items": [
     "<b>Refocusing:</b> integrate over a sheared slice of the 4D "
     "function. Different shear, different focal plane.",
     "",
     "<b>Synthetic aperture:</b> integrate over a chosen subset of "
     "directions. A small subset gives deep focus; a large one gives shallow.",
     "",
     "<b>Viewpoint change</b>, within the capture aperture. Small "
     "parallax, computed for free.",
     "",
     "<b>Depth estimation:</b> the focal plane at which a region is "
     "sharpest gives its depth. <b>Depth from one shot</b>.",
     "",
     "<b>Seeing through occluders:</b> a synthetic aperture wider than the "
     "occluder integrates around it.",
   ],
   "note": "Seeing through foliage with a camera array is the most "
           "striking demo and is worth showing."},

  {"t": "callout", "title": "Refocusing is a shear followed by an integral",
   "kind": "The core operation",
   "body": ["<b>Reparameterising the two planes to a different separation "
            "is a shear of the 4D function.</b>",
            "<b>Integrating the sheared function over the angular "
            "dimensions produces an image focused at the corresponding "
            "depth.</b>",
            "<b>So refocusing is: shear, then sum.</b> A few lines, once "
            "the light field is in hand.",
            "<b>And the Fourier slice theorem gives a faster route</b> "
            "— a slice of the 4D Fourier transform is the transform of "
            "the 2D projection, so refocusing can be done in frequency space "
            "at lower cost."]},

  {"t": "section", "label": "Part 4", "title": "What happened",
   "blurb": "An honest commercial post-mortem."},

  {"t": "callout", "title": "Lytro failed, and the reasons are instructive",
   "kind": "The commercial story",
   "body": ["<b>Resolution.</b> A 1-megapixel output in an era of "
            "12-megapixel phones. The headline feature cost the thing "
            "everyone compares.",
            "<b>The problem was not acute.</b> Autofocus is good and "
            "getting better; photographers rarely wished they could refocus "
            "afterwards.",
            "<b>Depth from stereo and from learned monocular estimation "
            "arrived</b>, giving portrait mode without the resolution "
            "cost.",
            "<b>And bokeh could be synthesised</b> (Module 11) convincingly "
            "enough. <b>The capability survived; the capture method did "
            "not.</b>"]},

  {"t": "table", "kicker": "Where it lives", "title": "Where light fields are actually used",
   "header": ["Domain", "Use"],
   "widths": [3.6, 8.5],
   "rows": [
     ["<b>Microscopy</b>", "<b>Single-shot volumetric capture of fast biological processes</b>"],
     ["Industrial inspection", "Depth and surface detail in one shot"],
     ["<b>Film and VFX</b>", "<b>Capture rigs for relighting and view synthesis</b>"],
     ["<b>Research into displays</b>", "<b>Light field displays may fix vergence-accommodation (CSCE 650)</b>"],
     ["Neural scene representations", "<b>NeRF and successors are light fields learned, not sampled</b>"],
   ],
   "footnote": "<b>The idea succeeded; the consumer camera did not.</b> "
               "Which is a common pattern worth recognising.",
   "note": "The NeRF connection is the live one — it is the same "
           "representation reached by a different route."},

  {"t": "callout", "title": "Neural radiance fields are the idea, reached differently",
   "kind": "Where this went",
   "body": ["<b>A NeRF represents a scene as a function from position and "
            "direction to radiance</b> — which is the plenoptic "
            "function, learned rather than sampled.",
            "<b>Instead of capturing the 4D function densely</b>, fit a "
            "network to a sparse set of photographs and query it anywhere.",
            "<b>This solves the sampling problem</b> that made light field "
            "capture impractical — you no longer need every ray, only "
            "enough to constrain the fit.",
            "<b>And it inherits the question of Module 13:</b> the "
            "rendered novel views are inferred, not measured, and the "
            "distinction matters."]},
 ],
 "takeaways": [
   "The plenoptic function has seven dimensions; radiance invariance in free "
   "space reduces it to a 4D light field — the same fact that made ray "
   "tracing a lookup.",
   "A conventional photograph is a 2D slice: the aperture integral destroys "
   "angular information irreversibly at capture.",
   "A plenoptic camera trades spatial resolution for angular — a 20 MP "
   "sensor with 10&times;10 angular samples yields 0.2 MP.",
   "Refocusing is a shear of the 4D function followed by an integral, and "
   "the Fourier slice theorem gives a faster route.",
   "Lytro failed on resolution against a problem that was not acute, and "
   "depth estimation plus synthetic bokeh delivered the capability without "
   "the cost.",
   "The representation survives in microscopy, VFX, light field displays, "
   "and — learned rather than sampled — in NeRF.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The plenoptic function"),
  ("eq", "P(x, y, z, &theta;, &phi;, &lambda;, t)"),
  ("p", "The <b>plenoptic function</b> describes the radiance at every "
        "point in space, in every direction, at every wavelength, at every "
        "instant. It is everything that could possibly be seen from "
        "anywhere — seven dimensions, and far too much to record."),
  ("eq", "L(u, v, s, t)"),
  ("callout", "Radiance invariance reduces seven dimensions to four",
   ["Fix the time and the wavelength and you have five dimensions: three of "
    "position and two of direction.",
    "<b>Now recall CSCE 647 Module 01: radiance is invariant along a ray in "
    "free space.</b> So specifying a point and a direction over-determines "
    "the ray — every point along that ray carries the same radiance, so "
    "they are not independent measurements.",
    "<b>A ray in free space is therefore determined by where it crosses two "
    "parallel planes</b> — two coordinates on each, four in total. This "
    "is the <b>two-plane parameterisation</b> and the resulting L(u,v,s,t) "
    "is the <b>4D light field</b>.",
    "<b>The same physical fact that made ray tracing a lookup rather than an "
    "integral makes light field capture finite rather than impossible.</b> "
    "It is worth noticing that the two courses depend on the same property "
    "for opposite purposes."]),
  ("callout", "A photograph is a 2D slice of a 4D function",
   ["<b>A conventional camera integrates over its aperture.</b> Every ray "
    "arriving at a given sensor location, from every direction the aperture "
    "admits, is summed into a single value.",
    "<b>That integration is irreversible.</b> Once the rays have been added "
    "together, there is no way to recover which came from which direction "
    "— the angular information is destroyed at the moment of capture, "
    "before any processing.",
    "<b>A light field camera records the rays separately</b>, retaining the "
    "direction each arrived from.",
    "<b>So the integration can be performed afterwards, and differently.</b> "
    "A different aperture, a different focal plane, a slightly different "
    "viewpoint — all are different integrals over the same recorded "
    "data. <b>Capture the function; compute the photograph.</b> This is "
    "Module 06's closing idea in its purest form."]),

  ("h1", "2 &nbsp; Capturing a light field"),
  ("table", ["Method", "Mechanism", "Trade-off"],
   [["<b>Camera array</b>",
     "Many cameras arranged on a plane, each recording one angular sample.",
     "<b>Full spatial resolution per view</b>, and physically large, "
     "expensive, and requiring careful calibration. The Stanford array had "
     "128 cameras."],
    ["<b>Gantry</b>",
     "A single camera moved mechanically to each position in turn.",
     "Cheap and high quality, and <b>static scenes only</b> — capture "
     "takes minutes."],
    ["<b>Plenoptic (microlens array)</b>",
     "A microlens array placed just in front of the sensor; the pixels "
     "beneath each microlens record different directions.",
     "<b>A single shot, from a hand-held camera</b> — and the spatial "
     "resolution falls catastrophically. See below."],
    ["<b>Coded mask</b>",
     "A patterned attenuating mask near the sensor; the light field is "
     "reconstructed computationally from the multiplexed measurement.",
     "Compressive — fewer measurements than the full light field, "
     "recovered by assuming sparsity. Requires a reconstruction step and "
     "loses light to the mask."]],
   [0.19, 0.36, 0.45]),
  ("callout", "The resolution trade is brutal, and it decided the market",
   ["<b>A microlens array places a small lens over each group of sensor "
    "pixels.</b> Each microlens forms a tiny image of the main lens's "
    "aperture, so the pixels beneath it record light arriving from different "
    "<i>directions</i> through that aperture.",
    "<b>So each microlens contributes one spatial sample and as many "
    "angular samples as it covers pixels.</b> The sensor's resolution is "
    "divided between the two.",
    "<b>A 20-megapixel sensor with 10&times;10 angular sampling yields a "
    "0.2-megapixel image.</b> Two hundred thousand pixels from a "
    "twenty-million-pixel sensor — and consumers compare megapixels, "
    "directly and unforgivingly.",
    "<b>Later designs recovered some of it</b> by placing the microlens "
    "array at a different position so that it images the focal plane rather "
    "than the aperture — trading angular range for spatial resolution "
    "instead. <b>The trade moved; it did not disappear</b>, because the "
    "sensor has a fixed number of pixels and four dimensions to cover."]),

  ("break",),
  ("h1", "3 &nbsp; What you can compute"),
  ("ul", ["<b>Digital refocusing.</b> Integrate over a <i>sheared</i> slice "
          "of the 4D function; different shears correspond to different "
          "focal planes. See below.",
          "<b>Synthetic aperture.</b> Integrate over a chosen subset of the "
          "angular samples. A small central subset gives a small effective "
          "aperture and deep depth of field; the full set gives the widest "
          "aperture the capture supports. <b>Aperture becomes a "
          "post-processing parameter.</b>",
          "<b>Viewpoint change</b>, within the extent of the capture "
          "aperture. The parallax available is small — limited by the "
          "physical size of the lens or the array — but it is genuine "
          "and free.",
          "<b>Depth estimation.</b> The focal setting at which a region "
          "appears sharpest indicates its depth, so a <b>depth map comes "
          "from a single exposure</b> with no stereo baseline and no "
          "projected pattern.",
          "<b>Seeing through partial occluders.</b> A synthetic aperture "
          "wider than an occluding object integrates light arriving around "
          "it from many directions, so the occluder blurs into "
          "near-transparency while the subject behind stays sharp. "
          "<b>Looking through foliage with a camera array is the most "
          "striking demonstration of the idea</b> and is worth seeing."]),
  ("callout", "Refocusing is a shear followed by an integral",
   ["<b>Reparameterising the two planes to a different separation is a "
    "shear of the 4D light field.</b> A ray's coordinates on the new planes "
    "are a linear function of its coordinates on the old ones, and the "
    "transformation is a shear in the (u,s) and (v,t) pairs.",
    "<b>Integrating the sheared function over the two angular dimensions "
    "produces an image focused at the depth corresponding to that "
    "shear.</b>",
    "<b>So refocusing is: shear, then sum.</b> A few lines of code once the "
    "light field is in hand, and it is the operation that made the idea "
    "famous.",
    "<b>And the Fourier slice theorem gives a faster route.</b> A 2D slice "
    "through the origin of the 4D Fourier transform is the Fourier transform "
    "of the corresponding 2D projection — so refocusing can be "
    "performed by extracting a slice in frequency space and inverse "
    "transforming, at O(n&#178; log n) rather than O(n&#8308;). The same "
    "theorem underlies computed tomography, which is another place "
    "projections and slices meet."]),

  ("h1", "4 &nbsp; What actually happened"),
  ("callout", "Lytro failed, and the reasons are worth understanding",
   ["<b>Resolution.</b> The first consumer Lytro produced roughly a "
    "one-megapixel final image at a time when phones produced twelve. "
    "<b>The headline feature cost exactly the quantity consumers use to "
    "compare cameras</b>, and no amount of explanation overcame that.",
    "<b>The problem it solved was not acute.</b> Autofocus was already good "
    "and improving; photographers did not frequently find themselves wishing "
    "they could change the focus after the fact. <b>A technically "
    "impressive solution to a problem few people had</b> is a recurring "
    "pattern worth recognising.",
    "<b>Depth estimation arrived by other routes.</b> Dual-pixel sensors, "
    "stereo from two lenses, and learned monocular depth all gave adequate "
    "depth maps without surrendering any resolution at all.",
    "<b>And bokeh could be synthesised</b> (Module 11) convincingly enough "
    "for the intended purpose. <b>The capability survived; the capture "
    "method did not</b> — portrait mode is what people wanted from "
    "light field photography, and it was delivered without it."]),
  ("table", ["Domain", "Use", "Why it works there"],
   [["<b>Microscopy</b>",
     "<b>Single-shot volumetric capture</b> of fast biological processes "
     "— neural activity, beating cilia.",
     "<b>The subject moves faster than a focal sweep allows</b>, and "
     "microscope resolution is abundant relative to the field of view. The "
     "trade that killed the consumer camera is acceptable here."],
    ["<b>Industrial inspection</b>",
     "Depth and surface detail from one exposure, on a production line.",
     "Robustness and single-shot capture matter more than resolution."],
    ["<b>Film and VFX</b>",
     "Capture rigs for relighting, view synthesis, and set reconstruction.",
     "Cost and bulk are acceptable; the output is a 3D asset rather than a "
     "photograph."],
    ["<b>Display research</b>",
     "<b>Light field displays</b> present a genuine range of focal depths.",
     "<b>This would resolve the vergence-accommodation conflict</b> of "
     "CSCE 650 Module 02, which no shipping headset solves."],
    ["<b>Neural scene representations</b>",
     "<b>NeRF and its successors.</b>", "See below."]],
   [0.19, 0.38, 0.43]),
  ("callout", "Neural radiance fields are the same idea, reached differently",
   ["<b>A NeRF represents a scene as a function from position and viewing "
    "direction to radiance and density</b> — which is the plenoptic "
    "function of &sect;1, <b>learned rather than sampled</b>.",
    "<b>Instead of capturing the 4D function densely</b>, which was always "
    "the impractical part, a network is fitted to a sparse set of ordinary "
    "photographs and can then be queried for any ray.",
    "<b>This dissolves the sampling problem that defeated light field "
    "capture.</b> You no longer need to record every ray — only enough "
    "photographs to constrain the fit, which is a few dozen rather than "
    "millions of samples.",
    "<b>And it inherits Module 13's question in full.</b> A novel view "
    "rendered from a NeRF is <i>inferred</i> from the training photographs, "
    "not measured — it is a plausible completion, and in regions the "
    "training views did not cover it is a confident invention. <b>The "
    "distinction between measurement and inference, which this course keeps "
    "returning to, applies here as sharply as anywhere.</b>"]),
 ],
 "resources": [
   ("Levoy & Hanrahan &mdash; Light Field Rendering (1996, free)",
    "https://graphics.stanford.edu/papers/light/",
    "The paper that introduced the 4D parameterisation of &sect;1. Short "
    "and foundational."),
   ("Ng &mdash; Digital Light Field Photography (thesis, free)",
    "https://web.archive.org/web/20210507012606/https://stanford.edu/class/ee367/reading/Ren%20Ng-thesis%20Lytro.pdf",
    "The plenoptic camera and the refocusing mathematics of &sect;3, by "
    "Lytro's founder. The Fourier slice refocusing is here."),
   ("Stanford Light Field Archive (free data)",
    "http://lightfield.stanford.edu/",
    "Captured light fields to experiment with, including the camera array "
    "datasets. You can implement refocusing on real data without any "
    "hardware."),
   ("Mildenhall et al. &mdash; NeRF (free)",
    "https://www.matthewtancik.com/nerf",
    "The &sect;4 connection. Read it as a light field paper and the "
    "lineage is obvious."),
 ],
 "exercises": [
   "Download a light field from the Stanford archive and visualise slices "
   "of the 4D function in several ways.",
   "Implement digital refocusing by shear-and-sum. Produce a focal stack "
   "from a single light field.",
   "Implement synthetic aperture and produce the same scene with deep and "
   "shallow depth of field.",
   "Implement refocusing via the Fourier slice theorem and compare the cost "
   "against shear-and-sum.",
   "Estimate depth from the light field by finding the focal setting that "
   "maximises local sharpness. Compare against the dataset's ground truth if "
   "available.",
   "Use a camera array dataset to see through a partial occluder. This is "
   "the most striking demonstration in the module.",
   "Compute the spatial resolution a plenoptic camera would give for a "
   "sensor and angular sampling of your choice, and compare against a "
   "conventional camera with the same sensor.",
   "Synthesise a light field from a rendered scene using CSCE 647's "
   "renderer, and verify your refocusing against ground-truth renders at "
   "each focal depth.",
   "Write a page on why Lytro failed, drawing on &sect;4, and identify "
   "another technology that followed the same pattern.",
 ],
 "selfcheck": [
   "State the plenoptic function and explain the reduction to four "
   "dimensions.",
   "Why is a conventional photograph a 2D slice, and what is irreversibly "
   "lost?",
   "Name four capture methods with their trade-offs.",
   "Compute the output resolution of a plenoptic camera from sensor "
   "resolution and angular sampling.",
   "Name five operations computable from a light field.",
   "Describe refocusing as an operation on the 4D function, and the faster "
   "frequency-domain route.",
   "Give four reasons the consumer light field camera failed.",
   "Name four places light fields are genuinely used.",
   "What is a NeRF in terms of this module, and what question does it "
   "inherit?",
 ],
},

# =========================================================== MODULE 10 ======
{
 "n": 10,
 "title": "Burst Photography",
 "subtitle": "What your phone actually does.",
 "question": "How does a small sensor produce a usable night photograph?",
 "outcomes": [
     "Explain why bursts beat single exposures.",
     "Implement robust alignment for a burst.",
     "Implement merging that rejects misaligned content.",
     "Explain the complete modern phone pipeline.",
     "Explain super-resolution from a handheld burst.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why bursts",
   "blurb": "Trading time for light, without blur."},

  {"t": "callout", "title": "More frames is more photons without more blur",
   "kind": "The core argument",
   "body": ["<b>A long exposure collects more photons and blurs</b> "
            "— from hand shake and from subject motion.",
            "<b>Many short exposures collect the same photons with no "
            "blur in any single frame.</b>",
            "<b>Averaging n aligned frames improves SNR by √n</b> "
            "(Module 01) — the signal adds linearly, the noise in "
            "quadrature.",
            "<b>So 16 short frames are equivalent to one 16× exposure, "
            "sharp.</b> The cost is alignment, and alignment is "
            "computation — which is cheap and getting cheaper, unlike "
            "sensor area."]},

  {"t": "table", "kicker": "Why it won", "title": "The constraints that made bursts inevitable",
   "header": ["Constraint", "Consequence"],
   "widths": [4.0, 8.1],
   "rows": [
     ["<b>Phone sensors are small</b>", "<b>Few photons; shot-noise limited</b>"],
     ["<b>Apertures are fixed and small</b>", "No way to gather more light optically"],
     ["Phones are handheld", "<b>Long exposures blur</b>"],
     ["<b>Computation is abundant</b>", "<b>And improves faster than optics</b>"],
     ["Users expect one button", "The pipeline must be automatic"],
   ],
   "footnote": "<b>Every constraint points the same way:</b> capture many "
               "frames and compute.",
   "note": "Framing it as forced by constraints explains why every "
           "manufacturer converged on the same approach."},

  {"t": "section", "label": "Part 2", "title": "Alignment",
   "blurb": "Making the frames line up."},

  {"t": "callout", "title": "Burst alignment is easier than panorama alignment",
   "kind": "Why a simpler method works",
   "body": ["<b>The frames are nearly identical</b> — same exposure, "
            "same scene, milliseconds apart.",
            "<b>Displacement is small</b> — hand tremor, a few pixels.",
            "<b>So feature detection and RANSAC (Module 07) are "
            "unnecessary.</b> Hierarchical block matching suffices.",
            "<b>Align tiles rather than the whole frame</b>, because "
            "different parts of the scene may move differently — which "
            "handles subject motion as well as camera motion."]},

  {"t": "code", "kicker": "Alignment", "title": "Hierarchical tile alignment",
   "lang": "text", "code": """
  Build a Gaussian pyramid of the reference and each alternate frame.

  For each level, coarse to fine:
      for each tile in the alternate frame:
          search a small window around the previous level's estimate
          minimise L1 or L2 distance to the reference tile
          upsample the displacement to the next level

  Result: a per-tile displacement field, not a single global transform.

  WHY TILES: the camera rotates (global) AND things in the scene move
  (local). A single homography handles only the first.

  WHY COARSE-TO-FINE (Module 02): the search window stays small at
  every level, so a large displacement costs little.
""",
   "caption": "A per-tile displacement field rather than a global "
              "transform, because local motion is the normal case.",
   "note": "This is HDR+'s actual alignment and it is simpler than most "
           "students expect."},

  {"t": "callout", "title": "Merging must reject what does not match",
   "kind": "The robustness requirement",
   "body": ["<b>Alignment will fail somewhere</b> — occlusion, a moving "
            "subject, a region with no texture to match.",
            "<b>Averaging a misaligned tile produces ghosting</b>, which is "
            "worse than the noise it was meant to remove.",
            "<b>So merge with a robustness test:</b> compare each aligned "
            "frame against the reference, and down-weight where they "
            "disagree beyond what noise explains.",
            "<b>HDR+ does this in the frequency domain</b> — a Wiener-like "
            "shrinkage per frequency band, which handles partial "
            "misalignment more gracefully than a per-pixel decision."]},

  {"t": "section", "label": "Part 3", "title": "The pipeline",
   "blurb": "End to end, as shipped."},

  {"t": "code", "kicker": "HDR+", "title": "The modern phone pipeline",
   "lang": "text", "code": """
  1. CAPTURE a burst of 10-15 RAW frames, all UNDEREXPOSED
        -> highlights never clip; every frame is short so none blur

  2. SELECT a reference frame (sharpest, usually near the middle)

  3. ALIGN all others to it, per tile, hierarchically

  4. MERGE with robustness -- reject tiles that disagree

  5. Now a clean, LINEAR, high-bit-depth image. Then:
       black level, white balance, DEMOSAIC (Module 05)
       chroma denoise, local tone map (Module 04)
       sharpen, colour correct
       ENCODE

  The user pressed one button. Roughly a second of computation
  happened. The output is a photograph no single exposure could
  have produced.
""",
   "caption": "Steps 1 to 4 are the computational part; step 5 is the "
              "classical pipeline from Module 05 applied to a far better "
              "input.",
   "note": "The key structural point: burst processing happens BEFORE "
           "demosaicing, on linear raw data."},

  {"t": "callout", "title": "Merge before demosaicing, in linear space",
   "kind": "The ordering that matters",
   "body": ["<b>Merging must happen on linear data</b> (Module 01), or the "
            "averaging is wrong.",
            "<b>And before demosaicing</b>, because demosaicing is an "
            "interpolation that invents data — averaging invented data is "
            "less useful than averaging measurements.",
            "<b>Merging raw also means the merged result has more "
            "bits</b> than any input frame, which the subsequent tone "
            "mapping can use.",
            "<b>So the burst machinery sits between the sensor and the "
            "classical pipeline</b>, not after it."]},

  {"t": "section", "label": "Part 4", "title": "Super-resolution",
   "blurb": "Hand tremor as a feature."},

  {"t": "callout", "title": "Hand shake samples between the pixels",
   "kind": "The surprising result",
   "body": ["<b>Natural hand tremor moves the sensor by sub-pixel "
            "amounts</b> between frames.",
            "<b>So each frame samples the scene at slightly different "
            "positions</b> — and the Bayer pattern means different "
            "colours land on different scene points.",
            "<b>Combining them on a finer grid recovers detail beyond one "
            "frame's sampling limit</b>, and demosaicing becomes "
            "unnecessary — every colour is measured somewhere.",
            "<b>Hand tremor, normally a defect, is the mechanism.</b> "
            "Google's super-res zoom <i>adds</i> motion when the phone is on "
            "a tripod, because without tremor it does not work."]},

  {"t": "bullets", "kicker": "Honest", "title": "What burst processing cannot do",
   "items": [
     "<b>It cannot recover clipped highlights</b> — which is why the "
     "frames are underexposed in the first place.",
     "",
     "<b>It cannot handle fast subject motion</b>. A moving person is "
     "taken from one frame, with that frame's noise.",
     "",
     "<b>It struggles in near-darkness</b>, where even the sum of fifteen "
     "frames is photon-starved.",
     "",
     "<b>And the characteristic artefacts are visible</b> once you know "
     "them: oversharpening, unnaturally even noise, and detail that is "
     "slightly too clean.",
     "",
     "<b>Which is the lead-in to Modules 12 and 13.</b>",
   ],
   "note": "The 'slightly too clean' artefact is the signature of modern "
           "phone photography and is worth learning to see."},
 ],
 "takeaways": [
   "Many short exposures collect the same photons as one long one without "
   "blur, and averaging n aligned frames improves SNR by &radic;n.",
   "Every phone constraint — small sensor, fixed aperture, handheld, "
   "abundant computation — points toward capturing many frames and "
   "computing.",
   "Burst alignment is easier than panorama alignment: hierarchical tile "
   "matching suffices, and per-tile displacement handles subject motion.",
   "Merging must reject tiles that disagree beyond what noise explains, or "
   "misalignment produces ghosting worse than the noise removed.",
   "Merge before demosaicing and in linear space — averaging "
   "interpolated data is less useful than averaging measurements.",
   "Hand tremor samples between pixels, so combining frames on a finer grid "
   "gives super-resolution and removes the need to demosaic.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why bursts"),
  ("callout", "More frames is more photons without more blur",
   ["<b>A long exposure collects more photons</b>, which is what reduces "
    "shot noise (Module 01) — <b>and it blurs</b>, from hand tremor and "
    "from anything in the scene that moves.",
    "<b>Many short exposures collect the same total photons with no motion "
    "blur in any individual frame.</b> Each frame is noisy, and none is "
    "blurred.",
    "<b>Averaging n aligned frames improves signal-to-noise by "
    "&radic;n</b> — the signal adds linearly and the independent noise "
    "adds in quadrature. Sixteen frames gives a factor of four, which is two "
    "stops.",
    "<b>So sixteen short exposures are equivalent to one sixteen-times "
    "longer exposure, and sharp.</b> The cost is the alignment, which is "
    "computation — and computation is cheap and improving quickly, "
    "while sensor area in a phone is fixed by the thickness of the device."]),
  ("table", ["Constraint", "Consequence"],
   [["<b>Phone sensors are physically small</b>",
     "Few photons per pixel, so images are <b>shot-noise limited</b> in all "
     "but bright light (Module 01)."],
    ["<b>Apertures are fixed and small</b>",
     "No optical route to gathering more light — the usual photographic "
     "lever is unavailable."],
    ["<b>Phones are handheld</b>",
     "<b>Long exposures blur.</b> The usual alternative lever is also "
     "unavailable."],
    ["<b>Computation is abundant</b>",
     "<b>And it improves faster than optics or sensor physics.</b> A phone "
     "has a capable image signal processor and several seconds of thermal "
     "budget."],
    ["<b>Users press one button</b>",
     "Whatever happens must be fully automatic, with no bracketing choices "
     "or post-processing expected."]],
   [0.28, 0.72]),
  ("p", "<b>Every constraint points the same way:</b> capture many frames "
        "and compute the photograph. This is why every manufacturer "
        "converged on essentially the same approach within a few years "
        "— it was not a design preference but the only direction "
        "available."),

  ("h1", "2 &nbsp; Alignment"),
  ("callout", "Burst alignment is easier than panorama alignment",
   ["<b>The frames are nearly identical.</b> Same exposure, same scene, "
    "captured milliseconds apart under the same light — which is "
    "precisely the condition Module 03 noted that bracketed exposures do not "
    "satisfy.",
    "<b>The displacements are small</b> — hand tremor over a few tens "
    "of milliseconds moves the frame by a few pixels, not by a large "
    "rotation.",
    "<b>So the full feature-detection and RANSAC machinery of Module 07 is "
    "unnecessary.</b> Hierarchical block matching — directly minimising "
    "the difference between tiles — is sufficient, far simpler, and "
    "much faster.",
    "<b>Align tiles rather than whole frames.</b> A single global transform "
    "captures camera motion but not the fact that a person in the scene "
    "moved independently. <b>A per-tile displacement field handles both</b>, "
    "and it is what makes robust merging possible in &sect;2.1."]),
  ("code", """Build a Gaussian pyramid of the reference and each alternate frame.
For each level, coarse to fine:
    for each tile:
        search a small window around the previous level's estimate
        minimise L1 or L2 distance to the reference tile
        upsample the displacement to the next level

Result: a PER-TILE displacement field, not a global transform."""),
  ("p", "<b>Tiles</b> because the camera rotates (a global effect) "
        "<i>and</i> things in the scene move (a local one), and only a "
        "per-tile field captures both. <b>Coarse-to-fine</b> (Module 02) "
        "because it keeps the search window small at every level, so a "
        "displacement of fifty pixels costs barely more to find than one of "
        "five."),
  ("callout", "Merging must reject what does not match",
   ["<b>Alignment will fail somewhere.</b> A region occluded in one frame "
    "and not another, a subject that moved, a patch of sky with no texture "
    "to match against — these are normal, not exceptional.",
    "<b>Averaging a misaligned tile produces ghosting</b>, which is a worse "
    "artefact than the noise the averaging was intended to remove. Naive "
    "averaging is therefore not an option.",
    "<b>So merge with a robustness test:</b> compare each aligned frame "
    "against the reference and down-weight contributions wherever they "
    "disagree by more than the noise model (Module 01) can explain. Where "
    "frames agree, average fully; where they do not, fall back toward the "
    "reference alone.",
    "<b>HDR+ performs this in the frequency domain</b>, applying a "
    "Wiener-like shrinkage per frequency band rather than a binary per-pixel "
    "decision. <b>This handles partial misalignment gracefully</b> — a "
    "tile may be well aligned at low frequencies and poorly at high ones, "
    "and a frequency-wise decision uses what is usable rather than "
    "discarding the tile."]),

  ("break",),
  ("h1", "3 &nbsp; The pipeline, end to end"),
  ("code", """1. CAPTURE 10-15 RAW frames, all UNDEREXPOSED
      -> highlights never clip; all frames short, so none blur
2. SELECT a reference frame (sharpest, usually near the middle)
3. ALIGN all others to it, per tile, hierarchically
4. MERGE with robustness -- reject tiles that disagree
5. Then the classical pipeline on a far better input:
      black level, white balance, DEMOSAIC (Module 05)
      chroma denoise, local tone map (Module 04)
      sharpen, colour correct, ENCODE"""),
  ("callout", "Merge before demosaicing, in linear space",
   ["<b>Merging must happen on linear data</b> (Module 01). Averaging "
    "gamma-encoded values does not give the encoding of the average "
    "radiance, and the error is largest exactly where the signal is "
    "weakest.",
    "<b>And it must happen before demosaicing.</b> Demosaicing is an "
    "interpolation — it invents two-thirds of the colour data at every "
    "pixel (Module 05). <b>Averaging sixteen frames' worth of invented data "
    "is far less useful than averaging sixteen frames' worth of "
    "measurements</b>, and the invented values are correlated with the "
    "measurement errors that produced them.",
    "<b>Merging raw also means the merged result carries more bits than any "
    "input frame.</b> Averaging sixteen 10-bit frames yields roughly 12 bits "
    "of real precision, which the subsequent tone mapping can use — and "
    "which is part of why night mode images tolerate aggressive shadow "
    "lifting.",
    "<b>So the burst machinery sits between the sensor and the classical "
    "pipeline</b>, not after it. Module 05's nine steps are unchanged; they "
    "simply operate on a much better input."]),

  ("h1", "4 &nbsp; Super-resolution from hand tremor"),
  ("callout", "Hand shake samples between the pixels",
   ["<b>Natural hand tremor displaces the sensor by sub-pixel amounts "
    "between frames</b> — fractions of a pixel, essentially at random.",
    "<b>So each frame samples the scene at slightly different "
    "positions.</b> Frame one measures the scene at one grid of points, "
    "frame two at a grid offset by 0.3 pixels, and so on.",
    "<b>Combining them onto a finer grid recovers detail beyond any single "
    "frame's sampling limit.</b> And because the Bayer pattern moves with "
    "the sensor, different colour filters land on different scene points "
    "across the burst — so <b>every colour is directly measured "
    "somewhere, and demosaicing becomes unnecessary.</b> The interpolation "
    "of Module 05 is replaced by measurement.",
    "<b>Hand tremor, normally a defect to be corrected, is the mechanism "
    "that makes it work.</b> Google's super-resolution zoom <i>deliberately "
    "introduces</i> sensor motion via the optical stabiliser when the phone "
    "is on a tripod, because without tremor every frame samples identically "
    "and there is nothing to recover. <b>This is a genuinely delightful "
    "result</b> and a good example of a constraint turning out to be a "
    "resource."]),
  ("ul", ["<b>It cannot recover clipped highlights.</b> Nothing can "
          "(Module 03) — which is exactly why the frames are "
          "deliberately underexposed.",
          "<b>It cannot handle fast subject motion.</b> A moving person is "
          "taken from the reference frame alone, with that single frame's "
          "noise — so a night photograph of a moving subject is noisy "
          "precisely where the subject is, which is a recognisable "
          "signature.",
          "<b>It struggles in near-darkness</b>, where even the sum of "
          "fifteen frames is photon-starved and the result is dominated by "
          "whatever the denoiser decided to do.",
          "<b>And the artefacts are visible once you know them:</b> "
          "oversharpened edges with faint halos, noise that is unnaturally "
          "even across the frame, and detail that is <b>slightly too "
          "clean</b> — foliage and hair in particular take on a "
          "characteristic smoothed-and-resharpened quality.",
          "<b>Which is the lead-in to Modules 12 and 13</b>, where the "
          "question of what was measured and what was synthesised becomes "
          "the subject rather than a footnote."]),
 ],
 "resources": [
   ("Hasinoff et al. &mdash; Burst photography for high dynamic range and "
    "low-light imaging (free, with dataset)",
    "https://hdrplusdata.org/",
    "<b>The HDR+ paper and the raw burst dataset.</b> This module is "
    "essentially a reading of it, and the dataset lets you implement the "
    "pipeline on real data."),
   ("Wronski et al. &mdash; Handheld Multi-Frame Super-Resolution (free)",
    "https://sites.google.com/view/handheld-super-res/",
    "The &sect;4 result, including the deliberate motion on a tripod."),
   ("Levoy & Pritch &mdash; Night Sight blog posts (free)",
    "https://blog.research.google/",
    "How the pipeline was extended to very low light, written by the people "
    "who did it."),
   ("Liba et al. &mdash; Handheld Mobile Photography in Very Low Light "
    "(free)",
    "https://google.github.io/night-sight/",
    "Motion metering, exposure selection, and the limits in &sect;4."),
 ],
 "exercises": [
   "Capture a burst of 16 raw frames handheld in dim light. Align and "
   "average them and compare against a single frame and against a long "
   "exposure.",
   "Measure the SNR improvement against frame count and confirm the "
   "&radic;n relationship on real data.",
   "Implement hierarchical tile alignment on the HDR+ dataset. Visualise the "
   "displacement field.",
   "Average without any robustness test on a burst containing a moving "
   "subject, and photograph the resulting ghosting.",
   "Implement a robustness-weighted merge and show the ghosting removed.",
   "Merge before and after demosaicing on the same burst and compare the "
   "result.",
   "Merge in linear space and in gamma space and quantify the difference.",
   "Implement a simple multi-frame super-resolution: align a burst to "
   "sub-pixel accuracy, accumulate onto a 2&times; grid, and compare against "
   "upsampling a single frame.",
   "Find the burst-processing artefacts of &sect;4 in photographs from your "
   "own phone. Foliage and hair are the places to look.",
 ],
 "selfcheck": [
   "Why do many short exposures beat one long one, and by how much?",
   "Give five constraints that made burst photography inevitable for "
   "phones.",
   "Why is burst alignment easier than panorama alignment, and what method "
   "suffices?",
   "Why align per tile rather than globally?",
   "Why must merging reject disagreement, and what does HDR+ do in the "
   "frequency domain?",
   "Give the eight steps of the modern phone pipeline.",
   "Why must merging precede demosaicing and happen in linear space?",
   "How does hand tremor enable super-resolution, and what happens on a "
   "tripod?",
   "Give four things burst processing cannot do, and three visible "
   "artefacts.",
 ],
},

# =========================================================== MODULE 11 ======
{
 "n": 11,
 "title": "Depth, Matting, and Synthetic Defocus",
 "subtitle": "Separating a scene into layers.",
 "question": "How does portrait mode work, and when does it fail?",
 "outcomes": [
     "Compare the methods of obtaining depth from a camera.",
     "Explain the matting equation and why it is underdetermined.",
     "Implement a matting method.",
     "Explain physically motivated synthetic defocus.",
     "Identify the failure modes and their causes.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Getting depth",
   "blurb": "Five approaches, with different failures."},

  {"t": "table", "kicker": "Depth", "title": "Sources of depth",
   "header": ["Method", "How", "Fails on"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["<b>Stereo</b>", "Two cameras; disparity gives depth", "<b>Textureless regions; occlusion</b>"],
     ["<b>Dual-pixel</b>", "Split photodiodes give a tiny baseline", "<b>Small baseline → near field only</b>"],
     ["Depth from defocus", "Blur size indicates distance", "Needs texture; ambiguous in sign"],
     ["Active (ToF, structured light)", "Project and measure", "<b>Sunlight; range; power</b>"],
     ["<b>Learned monocular</b>", "A network predicts depth from one image", "<b>It is inference, not measurement</b>"],
   ],
   "footnote": "<b>All of them fail at the places that matter most</b> "
               "— hair, edges, and transparent objects.",
   "note": "That every method fails at boundaries is the unifying point "
           "and leads into matting."},

  {"t": "callout", "title": "Dual-pixel depth is why portrait mode works on one lens",
   "kind": "A neat piece of engineering",
   "body": ["<b>Each photosite is split into two halves</b>, originally for "
            "phase-detect autofocus.",
            "<b>The two halves see slightly different parts of the "
            "aperture</b> — which is a stereo pair with a baseline of "
            "millimetres.",
            "<b>So a single lens yields a disparity map</b>, free, with no "
            "extra hardware.",
            "<b>The baseline is tiny</b>, so depth resolution is poor "
            "beyond a metre or two — which is fine, because portrait mode "
            "only needs to separate a near subject from a far background."]},

  {"t": "callout", "title": "Learned monocular depth is inference",
   "kind": "The honest framing",
   "body": ["<b>A single image does not determine depth.</b> A small near "
            "object and a large far one project identically.",
            "<b>So a monocular depth network is using priors</b> — "
            "learned regularities about object sizes, perspective, texture "
            "gradients, and typical scene layouts.",
            "<b>It works well because those regularities are real</b>, and "
            "it fails when a scene violates them — a photograph of a "
            "photograph, or an unusual scale.",
            "<b>Which is not a criticism.</b> Human monocular depth is also "
            "inference. The point is to be clear about which outputs are "
            "measurements and which are estimates."]},

  {"t": "section", "label": "Part 2", "title": "Matting",
   "blurb": "The boundary is not binary."},

  {"t": "eq", "kicker": "Matting", "title": "The compositing equation",
   "eqs": [
     ("I = α F + (1 − α) B",
      "Each observed pixel is a blend of foreground and background, with "
      "opacity α."),
     ("3 equations, 7 unknowns  (per pixel)",
      "Three colour channels observed; α, F, and B unknown. "
      "Underdetermined by four."),
   ],
   "caption": "The problem is underdetermined per pixel, so every method "
              "is a different way of adding constraints.",
   "note": "Counting the unknowns makes the need for priors obvious."},

  {"t": "callout", "title": "A hard mask is wrong at every interesting boundary",
   "kind": "Why matting matters",
   "body": ["<b>Hair, fur, motion blur, glass, and smoke are genuinely "
            "partially transparent</b> at pixel scale.",
            "<b>A binary mask produces a hard cut</b> that reads as a "
            "cut-out, which is the single most recognisable sign of a bad "
            "composite.",
            "<b>And the pixels at a boundary are real mixtures</b> — a "
            "pixel spanning a hair strand genuinely contains both.",
            "<b>So α must be continuous</b>, and recovering it is the "
            "matting problem."]},

  {"t": "bullets", "kicker": "Methods", "title": "Approaches to matting",
   "items": [
     "<b>Trimap-based:</b> the user marks definite foreground, definite "
     "background, and unknown. The classical setting.",
     "",
     "<b>Bayesian matting:</b> model local F and B colour distributions "
     "and solve for the most probable α.",
     "",
     "<b>Closed-form matting:</b> assume F and B are locally linear in "
     "colour, which makes α the solution of a sparse linear system. "
     "<b>Elegant, and the system is a Laplacian again</b> (Module 08).",
     "",
     "<b>Blue screen:</b> constrain B to a known colour. Underdetermination "
     "removed by construction, which is why film does it.",
     "",
     "<b>Learned:</b> best results now, and it infers.",
   ],
   "note": "The matting Laplacian is a nice third appearance of the same "
           "linear system."},

  {"t": "section", "label": "Part 3", "title": "Synthetic defocus",
   "blurb": "Faking a lens you do not have."},

  {"t": "callout", "title": "Blurring by depth is not what a lens does",
   "kind": "Why naive defocus looks wrong",
   "body": ["<b>A real lens integrates over its aperture</b>, so an "
            "out-of-focus background object is spread over a disc — and "
            "light from <i>behind</i> a foreground object contributes to "
            "pixels beside it.",
            "<b>Blurring the image by a depth-dependent radius does the "
            "opposite</b>: it smears the foreground <i>into</i> the "
            "background.",
            "<b>The symptom is a halo of foreground colour</b> around the "
            "subject — the classic bad portrait mode.",
            "<b>The correct approach is scatter, not gather:</b> each "
            "source pixel contributes to a disc of destination pixels, with "
            "depth ordering respected."]},

  {"t": "bullets", "kicker": "Getting it right", "title": "What convincing synthetic bokeh needs",
   "items": [
     "<b>Scatter, with depth ordering.</b> Nearer contributions occlude "
     "farther ones.",
     "",
     "<b>A realistic aperture shape.</b> Real bokeh is polygonal from the "
     "diaphragm blades, not Gaussian.",
     "",
     "<b>Operate in linear space</b> (Module 01), or bright highlights do "
     "not bloom into the characteristic bright discs.",
     "",
     "<b>Blur radius proportional to |1/d − 1/d_focus|</b>, which is the "
     "actual thin-lens relation — not proportional to depth.",
     "",
     "<b>And handle the matte</b> — the subject boundary needs α, not a "
     "hard edge.",
   ],
   "footnote": "The linear-space point is what produces the bright "
               "out-of-focus highlights people associate with fast lenses."},

  {"t": "callout", "title": "The failures are all at boundaries",
   "kind": "What to look for",
   "body": ["<b>Hair and fur</b> — matting is hardest exactly where "
            "detail is finest.",
            "<b>Glasses and transparency</b> — the depth is ambiguous and "
            "the matte is partial.",
            "<b>Objects at the same depth as the subject</b> are blurred or "
            "kept inconsistently.",
            "<b>Thin structures</b> — a railing behind a subject gets "
            "sliced.",
            "<b>And the giveaway is a uniformly blurred background with a "
            "sharply cut subject</b>, which no lens produces."]},
 ],
 "takeaways": [
   "Stereo, dual-pixel, defocus, active sensing, and learned monocular each "
   "give depth, and all fail at hair, edges, and transparency.",
   "Dual-pixel sensors give a millimetre-baseline stereo pair for free, "
   "which is enough to separate a near subject from a far background.",
   "Learned monocular depth is inference from priors, not measurement — "
   "which is fine, and worth being explicit about.",
   "The matting equation has three observations and seven unknowns per "
   "pixel, so every method adds constraints.",
   "A hard mask is wrong wherever pixels genuinely mix — hair, motion "
   "blur, glass — which is every interesting boundary.",
   "Real defocus scatters light from background around foreground; blurring "
   "by depth smears foreground outward and produces the characteristic halo.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Obtaining depth"),
  ("table", ["Method", "Mechanism", "Characteristic failure"],
   [["<b>Stereo</b>",
     "Two cameras a known distance apart; disparity between corresponding "
     "points gives depth.",
     "<b>Textureless regions</b> offer nothing to match, and <b>occlusion "
     "boundaries</b> have no correspondence because the surface is visible "
     "to only one camera."],
    ["<b>Dual-pixel</b>",
     "Each photosite split into two halves, each seeing a different half of "
     "the aperture.",
     "<b>A baseline of millimetres</b>, so depth resolution falls off "
     "rapidly beyond a metre or two. See below."],
    ["<b>Depth from defocus</b>",
     "The size of the blur circle indicates distance from the focal plane.",
     "Requires texture to measure blur against, and is <b>ambiguous in "
     "sign</b> — equally blurred in front of and behind focus — "
     "unless multiple focal settings are captured."],
    ["<b>Active: time of flight, structured light</b>",
     "Project light and measure its return time or its deformation.",
     "<b>Defeated by sunlight</b>, limited in range, and costs power and "
     "hardware. Excellent indoors at short range."],
    ["<b>Learned monocular</b>",
     "A network predicts depth from a single image.",
     "<b>It is inference rather than measurement.</b> See below."]],
   [0.17, 0.37, 0.46]),
  ("p", "<b>Every one of these fails at the places that matter most for "
        "compositing</b> — hair, fine structures, transparent objects, "
        "and occlusion boundaries. This is not coincidence: those are "
        "precisely the places where the assumption underlying each method "
        "(a locally continuous surface) breaks down. It leads directly into "
        "&sect;2."),
  ("callout", "Dual-pixel depth is why portrait mode works on a single lens",
   ["<b>Each photosite is split into two independently readable halves</b>, "
    "a design introduced for phase-detect autofocus rather than for depth.",
    "<b>The two halves see light arriving through slightly different parts "
    "of the lens aperture</b> — which makes them a stereo pair with a "
    "baseline equal to roughly half the aperture diameter, a few "
    "millimetres.",
    "<b>So a single-lens camera produces a disparity map for free</b>, with "
    "no additional hardware, no second camera, and no projected pattern. The "
    "sensor was already built that way.",
    "<b>The baseline is tiny, so depth resolution is poor beyond a metre or "
    "two.</b> <b>Which is entirely adequate</b>, because portrait mode needs "
    "only to separate a subject at one or two metres from a background that "
    "is further away — it does not need metric depth. A good example of "
    "a method whose limitations happen not to matter for its application."]),
  ("callout", "Learned monocular depth is inference, and that is worth saying",
   ["<b>A single image does not determine depth.</b> A small object nearby "
    "and a large object far away project identically, and no computation on "
    "the pixels distinguishes them. The problem is underdetermined in "
    "principle, not merely in practice.",
    "<b>So a monocular depth network is applying priors</b> — learned "
    "regularities about how large objects usually are, how perspective lines "
    "converge, how texture density falls with distance, and what scene "
    "layouts are common.",
    "<b>It works well because those regularities are genuinely true of most "
    "photographs</b>, and it fails when a scene violates them: a photograph "
    "of a photograph, a scale model, an unusual viewpoint, a mirror.",
    "<b>This is not a criticism of the method.</b> Human monocular depth "
    "perception is also inference from priors, and it fails on the same "
    "cases — forced-perspective photographs fool people reliably. "
    "<b>The point is to be clear about which outputs of a pipeline are "
    "measurements and which are estimates</b>, which is Module 13's "
    "question and worth asking continuously."]),

  ("h1", "2 &nbsp; Matting"),
  ("eq", "I = &alpha;F + (1 &minus; &alpha;)B"),
  ("p", "Each observed pixel I is a blend of a foreground colour F and a "
        "background colour B, in proportion &alpha;. <b>Three equations "
        "— one per colour channel — and seven unknowns per pixel: "
        "three for F, three for B, and &alpha;.</b> Underdetermined by four, "
        "at every pixel independently. <b>Every matting method is therefore "
        "a different way of supplying the missing constraints.</b>"),
  ("callout", "A hard mask is wrong at every interesting boundary",
   ["<b>Hair, fur, motion blur, glass, smoke, and fine foliage are "
    "genuinely partially transparent at pixel scale.</b> A pixel spanning a "
    "single hair strand really does contain light from both the hair and "
    "whatever is behind it — the mixture is physical, not an artefact "
    "of sampling.",
    "<b>A binary mask produces a hard cut</b>, which reads immediately as a "
    "cut-out. It is the single most recognisable sign of a poor composite, "
    "and the eye detects it before the viewer can say why.",
    "<b>So &alpha; must be continuous</b>, taking intermediate values "
    "wherever the pixel is genuinely mixed.",
    "<b>Recovering that continuous &alpha; is the matting problem</b>, and "
    "it is substantially harder than segmentation — which only has to "
    "decide which side each pixel is on."]),
  ("ul", ["<b>Trimap-based methods.</b> The user marks regions as definitely "
          "foreground, definitely background, and unknown. The method solves "
          "only within the unknown band, using the certain regions as "
          "constraints. This is the classical setting and it reduces the "
          "underdetermination substantially.",
          "<b>Bayesian matting.</b> Model the local distributions of "
          "foreground and background colours as Gaussians estimated from "
          "nearby known pixels, and solve for the most probable &alpha;, F, "
          "and B jointly.",
          "<b>Closed-form matting.</b> Assume F and B are each locally "
          "linear in colour within a small window — the 'colour line' "
          "model, which holds remarkably well for real images. <b>&alpha; "
          "then satisfies a sparse linear system whose matrix is a "
          "Laplacian</b>, which is the same structure as Module 08's Poisson "
          "system and CSCE 649's pressure solve. <b>A third appearance of "
          "the same machinery.</b>",
          "<b>Blue or green screen.</b> Constrain B to a known colour. The "
          "underdetermination is removed by controlling the scene rather "
          "than by inference, which is why film does it and why it works so "
          "much better than anything else.",
          "<b>Learned matting.</b> The best results now, requiring little or "
          "no user input — and inferring the matte from training data "
          "rather than deriving it."]),

  ("break",),
  ("h1", "3 &nbsp; Synthetic defocus"),
  ("callout", "Blurring by depth is not what a lens does",
   ["<b>A real lens integrates over its aperture.</b> An out-of-focus point "
    "in the background is spread across a disc on the sensor — and "
    "crucially, <b>light from behind a foreground object reaches sensor "
    "positions beside that object</b>, because it arrives through parts of "
    "the aperture the foreground does not block. A blurred background wraps "
    "slightly <i>around</i> a sharp foreground.",
    "<b>Blurring the image by a depth-dependent radius does the "
    "opposite.</b> A gather-based blur at a background pixel near the "
    "subject averages in foreground pixels, smearing the subject's colour "
    "outward into the background.",
    "<b>The symptom is a halo of foreground colour around the subject</b> "
    "— a faint glow of skin tone or shirt colour in the blurred "
    "background. This is the classic signature of poor synthetic defocus and "
    "it is immediately recognisable once you know to look.",
    "<b>The correct formulation is scatter rather than gather:</b> each "
    "source pixel contributes to a disc of destination pixels, with depth "
    "ordering respected so that nearer contributions occlude farther ones. "
    "More expensive, and physically right."]),
  ("ul", ["<b>Scatter with depth ordering</b>, per the callout above.",
          "<b>Use a realistic aperture shape.</b> Real bokeh discs are "
          "polygonal, their shape set by the number of diaphragm blades, and "
          "they have a characteristic edge profile — bright-rimmed for "
          "some lens designs. A Gaussian blur looks nothing like it.",
          "<b>Operate in linear space</b> (Module 01). This is what produces "
          "the bright, distinct out-of-focus highlights people associate "
          "with fast lenses: a small very bright highlight spread over a disc "
          "remains bright in linear space and is washed out if the operation "
          "is done on encoded values. <b>Doing the blur in gamma space is "
          "the difference between convincing bokeh and grey smudges.</b>",
          "<b>Make the blur radius proportional to |1/d &minus; "
          "1/d<sub>focus</sub>|</b>, which is the thin-lens relation "
          "— <i>not</i> proportional to depth, and not proportional to "
          "depth difference. The non-linearity matters: the falloff in front "
          "of the focal plane differs from behind it.",
          "<b>And handle the matte</b> (&sect;2). The subject boundary needs "
          "a continuous &alpha;, or the composite has a cut-out edge however "
          "good the blur is."]),
  ("callout", "The failures are all at boundaries",
   ["<b>Hair and fur.</b> Matting is hardest exactly where the detail is "
    "finest, and portrait mode's subject is usually a person with hair. This "
    "is the most common visible failure.",
    "<b>Glasses and transparency.</b> The depth is genuinely ambiguous "
    "— the glass is at one depth and what is seen through it is at "
    "another — and the matte is partial. Spectacle lenses are "
    "frequently blurred or sharpened wrongly.",
    "<b>Objects at the same depth as the subject</b> are blurred or kept "
    "inconsistently, because the depth estimate cannot separate them and the "
    "segmentation must guess.",
    "<b>Thin structures.</b> A railing, a branch, or a microphone stand "
    "passing behind the subject gets sliced where the depth map's resolution "
    "cannot resolve it.",
    "<b>And the overall giveaway is a uniformly blurred background with a "
    "uniformly sharp subject</b> — <b>which no real lens produces</b>, "
    "because a real lens's blur varies continuously with depth throughout "
    "the scene, including across the subject itself. A real portrait has the "
    "near shoulder slightly softer than the eyes."]),
 ],
 "resources": [
   ("Wadhwa et al. &mdash; Synthetic Depth-of-Field with a Single-Camera "
    "Mobile Phone (free)",
    "https://research.google/pubs/pub47409/",
    "<b>The portrait mode paper.</b> Dual-pixel depth, segmentation, and "
    "the defocus rendering of &sect;3, from the team that shipped it."),
   ("Levin, Lischinski & Weiss &mdash; A Closed-Form Solution to Natural "
    "Image Matting (free)",
    "https://www.cse.huji.ac.il/~danix/matting/",
    "The matting Laplacian of &sect;2. Elegant, and a third appearance of "
    "the same linear system."),
   ("Chuang et al. &mdash; A Bayesian Approach to Digital Matting (free)",
    "https://grail.cs.washington.edu/projects/digital-matting/",
    "The Bayesian formulation, and a clear statement of the "
    "underdetermination."),
   ("Szeliski &mdash; Computer Vision, Chapter 12 (free)",
    "https://szeliski.org/Book/",
    "Stereo and depth estimation, with the failure analysis of &sect;1."),
 ],
 "exercises": [
   "Compute depth from a stereo pair and identify every region where it "
   "fails. Classify each failure as textureless or occluded.",
   "If your phone exposes dual-pixel data, extract it and compute "
   "disparity. Measure the usable depth range.",
   "Run a learned monocular depth model on a photograph of a photograph and "
   "document the failure.",
   "Construct a forced-perspective photograph that fools both a depth "
   "network and a human.",
   "Implement closed-form matting and extract a matte for a subject with "
   "hair. Compare against a binary segmentation.",
   "Composite the same subject with a hard mask and with a continuous matte, "
   "and compare at the hair boundary.",
   "Implement gather-based depth blur and produce the foreground halo "
   "artefact deliberately.",
   "Implement scatter-based defocus with depth ordering and show the halo "
   "removed.",
   "Implement a polygonal aperture and blur in linear and in gamma space. "
   "Photograph point highlights to make the difference obvious.",
   "Collect five portrait mode photographs from any phone and identify the "
   "failure mode in each.",
 ],
 "selfcheck": [
   "Name five sources of depth and the characteristic failure of each.",
   "How does dual-pixel depth work, and why is its small baseline "
   "acceptable?",
   "Why is monocular depth inference rather than measurement, and when does "
   "it fail?",
   "Write the matting equation and count the equations and unknowns.",
   "Why is a hard mask wrong, and where specifically?",
   "Name five matting approaches and say which removes the "
   "underdetermination by construction.",
   "Why does blurring by depth produce a halo, and what is the correct "
   "formulation?",
   "Give five requirements for convincing synthetic bokeh.",
   "Name five portrait mode failure modes and the overall giveaway.",
 ],
},

# =========================================================== MODULE 12 ======
{
 "n": 12,
 "title": "Learned Image Processing",
 "subtitle": "What networks changed, and what they invent.",
 "question": "When a model produces detail, where did it come from?",
 "outcomes": [
     "Explain why learned methods outperform hand-designed ones on these "
     "tasks.",
     "Explain the role of the loss function in what the output looks like.",
     "Distinguish restoration from synthesis.",
     "Evaluate learned methods honestly, including their failure modes.",
     "Explain why perceptual metrics and distortion metrics disagree.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why learning works here",
   "blurb": "These are exactly the problems priors solve."},

  {"t": "callout", "title": "Every problem in this course is underdetermined",
   "kind": "The unifying observation",
   "body": ["<b>Demosaicing</b> invents two-thirds of the colour data. "
            "<b>Deconvolution</b> cannot recover frequencies the blur "
            "removed. <b>Matting</b> has seven unknowns and three "
            "equations.",
            "<b>Every one is solved by adding a prior</b> — an assumption "
            "about what real images look like.",
            "<b>Hand-designed priors are crude:</b> smoothness, sparse "
            "gradients, local colour lines. Real and very approximate.",
            "<b>A network learns the prior from data</b>, which is a far "
            "richer description of what photographs look like than anything "
            "anyone could write down. <b>That is the whole reason it "
            "works.</b>"]},

  {"t": "table", "kicker": "Tasks", "title": "Where learned methods won",
   "header": ["Task", "Classical", "Learned"],
   "widths": [3.0, 4.4, 4.7],
   "rows": [
     ["Denoising", "BM3D — strong, principled", "<b>Better, especially at high noise</b>"],
     ["<b>Demosaicing</b>", "Gradient-corrected", "<b>Noticeably better on hard texture</b>"],
     ["Super-resolution", "Interpolation, sparse coding", "<b>Transformed</b>"],
     ["<b>Deblurring</b>", "Hard, fragile", "<b>Much better and still hard</b>"],
     ["Matting", "Trimap required", "<b>Automatic and good</b>"],
     ["<b>The whole ISP</b>", "Nine hand-tuned stages", "<b>End to end, raw to RGB</b>"],
   ],
   "footnote": "<b>Joint solving beats staged solving</b> — doing "
               "demosaic and denoise together is better than either in "
               "sequence.",
   "note": "The joint-versus-staged point is the strongest technical "
           "argument and is often underappreciated."},

  {"t": "section", "label": "Part 2", "title": "The loss decides the look",
   "blurb": "What you optimise is what you get."},

  {"t": "callout", "title": "L2 loss produces blurry output, necessarily",
   "kind": "Why the loss matters so much",
   "body": ["<b>When several outputs are plausible, L2 loss is minimised "
            "by their average.</b>",
            "<b>The average of several plausible textures is a blur.</b> "
            "So an L2-trained model hedges — and hedging looks soft.",
            "<b>This is not a training failure.</b> It is the correct "
            "answer to the question that was asked.",
            "<b>Adversarial and perceptual losses ask a different "
            "question:</b> make it look like a real photograph, rather than "
            "minimise expected error. <b>The output is sharper and less "
            "faithful.</b>"]},

  {"t": "table", "kicker": "Losses", "title": "What each loss optimises for",
   "header": ["Loss", "Optimises", "Output looks"],
   "widths": [2.8, 4.4, 4.9],
   "rows": [
     ["L2 / MSE", "Expected squared error", "<b>Blurry; high PSNR</b>"],
     ["L1", "Expected absolute error", "Slightly sharper than L2"],
     ["<b>Perceptual (VGG)</b>", "Distance in a feature space", "<b>Sharper; plausible texture</b>"],
     ["<b>Adversarial</b>", "Indistinguishable from real", "<b>Sharpest; may invent</b>"],
     ["Diffusion", "The full distribution", "<b>Samples; different each time</b>"],
   ],
   "footnote": "<b>The perception-distortion tradeoff is provable:</b> you "
               "cannot optimise both.",
   "note": "That the tradeoff is a theorem rather than an engineering "
           "limitation is the key point."},

  {"t": "callout", "title": "The perception–distortion tradeoff is a theorem",
   "kind": "Not an engineering limitation",
   "body": ["<b>Blau and Michaeli proved it:</b> improving perceptual "
            "quality necessarily worsens distortion, beyond a certain "
            "point.",
            "<b>So 'sharper and more accurate' is not available.</b> A "
            "method that looks better than another has, past that bound, "
            "measurably higher error.",
            "<b>Which explains why PSNR rankings and visual rankings "
            "disagree</b> — they are measuring genuinely opposed "
            "objectives.",
            "<b>And why papers report both</b>, and why you should ask "
            "which one a claim is about."]},

  {"t": "section", "label": "Part 3", "title": "Restoration or synthesis",
   "blurb": "The distinction that matters."},

  {"t": "two", "kicker": "Two things", "title": "Recovering and inventing",
   "lh": "Restoration",
   "l": ["Recover information that is <b>present but degraded</b>.",
         "Denoising, mild deblurring, demosaicing.",
         "<b>The answer is constrained by the measurement.</b>",
         ("More data would converge to the truth.", 1)],
   "rh": "Synthesis",
   "r": ["Produce information that <b>was never measured</b>.",
         "Large upscaling, inpainting, frequencies past the lens cutoff.",
         "<b>The answer comes from the prior.</b>",
         ("More data changes what is invented, not whether.", 1)],
   "note": "Most real methods do both, and the boundary is where the "
           "honesty is required."},

  {"t": "callout", "title": "The upscaled face is not that person's face",
   "kind": "The concrete case",
   "body": ["<b>Upscale a 16×16 face by 8× and you get a plausible, "
            "sharp, detailed face.</b>",
            "<b>It is not the face of the person photographed.</b> The "
            "information was never recorded; the model produced a face "
            "consistent with the low-resolution evidence and its training "
            "data.",
            "<b>Different models give different faces</b> from the same "
            "input, which is the proof.",
            "<b>This matters in forensics, medicine, and journalism</b>, and "
            "it is the reason the distinction is not academic. Module 13."]},

  {"t": "bullets", "kicker": "Failures", "title": "How learned methods fail",
   "items": [
     "<b>Distribution shift.</b> Trained on one camera's noise, applied to "
     "another's.",
     "",
     "<b>Confident wrongness.</b> No uncertainty estimate by default, and "
     "the output looks equally plausible when it is wrong.",
     "",
     "<b>Hallucinated structure</b> — text that is not text, patterns in "
     "noise, faces in clouds.",
     "",
     "<b>Averaging away rare content.</b> Unusual but real detail is "
     "treated as noise.",
     "",
     "<b>And bias from the training set</b>, which for face-related tasks "
     "has been demonstrated repeatedly.",
   ],
   "note": "Confident wrongness is the one that matters most operationally "
           "— there is no signal that the output is unreliable."},
 ],
 "takeaways": [
   "Every problem in this course is underdetermined and solved by a prior; a "
   "network learns a far richer prior than anyone could hand-design.",
   "Joint solving beats staged solving — demosaicing and denoising "
   "together outperform either in sequence.",
   "L2 loss is minimised by the average of plausible outputs, and the "
   "average of plausible textures is a blur. The softness is correct, not a "
   "bug.",
   "The perception–distortion tradeoff is a theorem: past a bound, "
   "sharper necessarily means measurably less accurate.",
   "Restoration recovers degraded information; synthesis produces "
   "information never measured. Most methods do both.",
   "An upscaled face is a plausible face, not that person's — different "
   "models produce different faces from the same input.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why learned methods work on these problems"),
  ("callout", "Every problem in this course is underdetermined",
   ["<b>Demosaicing</b> must produce three colour values per pixel from one "
    "measurement (Module 05). <b>Deconvolution</b> cannot recover "
    "frequencies the blur attenuated to zero (Module 06). <b>Matting</b> has "
    "seven unknowns and three equations per pixel (Module 11). <b>Monocular "
    "depth</b> is not determined by the image at all.",
    "<b>Every one of them is made solvable by adding a prior</b> — an "
    "assumption about what real photographs look like, which selects among "
    "the solutions consistent with the measurement.",
    "<b>Hand-designed priors are crude.</b> Smoothness, sparse gradients, "
    "piecewise constancy, local colour lines — each captures something "
    "real about natural images and each is a drastic simplification of a "
    "very complicated distribution.",
    "<b>A network learns the prior from data.</b> What it learns is a far "
    "richer description of what photographs look like than anything anyone "
    "could write down in closed form. <b>That is the entire reason learned "
    "methods outperform classical ones on these tasks</b> — not greater "
    "cleverness about the forward model, which is well understood, but a "
    "better prior over the solutions."]),
  ("table", ["Task", "Best classical method", "Learned"],
   [["<b>Denoising</b>", "BM3D — genuinely strong and principled, "
     "exploiting self-similarity.",
     "<b>Better, particularly at high noise levels</b> where BM3D's patch "
     "matching degrades."],
    ["<b>Demosaicing</b>", "Gradient-corrected interpolation (Module 05).",
     "<b>Noticeably better on difficult texture</b> — exactly where "
     "the classical assumption that chrominance varies slowly fails."],
    ["<b>Super-resolution</b>", "Interpolation, then sparse coding.",
     "<b>Transformed.</b> The gap is larger here than for any other task on "
     "this list — and so is the amount of invention (&sect;3)."],
    ["<b>Deblurring</b>", "Fragile, and heavily dependent on priors "
     "(Module 06).", "<b>Much better, and still hard.</b>"],
    ["<b>Matting</b>", "Required a user-supplied trimap (Module 11).",
     "<b>Automatic and good</b>, which changed it from a specialist "
     "operation into a feature."],
    ["<b>The entire ISP</b>", "Nine hand-tuned stages (Module 05).",
     "<b>End to end, raw to RGB, in one model.</b>"]],
   [0.17, 0.40, 0.43]),
  ("p", "<b>Joint solving beats staged solving</b>, and this is the "
        "strongest technical argument for the end-to-end approach. "
        "Demosaicing and denoising performed together outperform either in "
        "sequence, because the noise affects the interpolation and the "
        "interpolation correlates the noise — so solving one first "
        "throws away information the other needed. The classical pipeline's "
        "stage boundaries were a decomposition for human comprehensibility, "
        "not a property of the problem."),

  ("h1", "2 &nbsp; The loss function decides the appearance"),
  ("callout", "L2 loss produces blurry output, necessarily",
   ["<b>When several outputs are plausible given the input, the expected "
    "squared error is minimised by their average.</b> This is elementary and "
    "it has a severe consequence.",
    "<b>The average of several plausible textures is a blur.</b> If a "
    "degraded region could plausibly be grass, or gravel, or fabric, the "
    "L2-optimal prediction is a smooth grey-green haze that is none of them "
    "— because hedging minimises expected error.",
    "<b>So the softness of L2-trained models is not a training failure or a "
    "capacity limitation.</b> It is the correct answer to the question that "
    "was asked. Asking for minimum expected squared error and receiving a "
    "blur is the system working.",
    "<b>Adversarial and perceptual losses ask a different question:</b> "
    "produce something that looks like a real photograph, rather than "
    "something that minimises expected error. <b>The output is sharper and "
    "less faithful</b>, and both halves of that are consequences of the "
    "change in objective."]),
  ("table", ["Loss", "What it optimises", "Resulting appearance"],
   [["<b>L2 / MSE</b>", "Expected squared error.",
     "<b>Blurry, and it maximises PSNR</b> — which is why PSNR "
     "rankings favour blurry results."],
    ["<b>L1</b>", "Expected absolute error.",
     "Slightly sharper than L2, because the median is less sensitive to "
     "outlying possibilities than the mean."],
    ["<b>Perceptual (VGG / LPIPS)</b>",
     "Distance in the feature space of a pretrained network.",
     "<b>Sharper, with plausible texture</b>, because feature-space "
     "distance is insensitive to exact pixel placement."],
    ["<b>Adversarial (GAN)</b>",
     "Indistinguishability from real images, judged by a discriminator.",
     "<b>Sharpest, and most willing to invent</b> — the objective "
     "rewards plausibility, with no term for correspondence to the input."],
    ["<b>Diffusion</b>", "The full conditional distribution.",
     "<b>Samples from it</b> — so running it twice gives two different "
     "plausible answers, which is an honest representation of the "
     "underdetermination and an awkward property for a tool."]],
   [0.20, 0.35, 0.45]),
  ("callout", "The perception-distortion tradeoff is a theorem",
   ["<b>Blau and Michaeli proved that improving perceptual quality "
    "necessarily worsens distortion</b>, beyond a certain bound. It is a "
    "mathematical result about estimators, not an observation about current "
    "architectures.",
    "<b>So 'sharper and more accurate' is not available.</b> Past the "
    "bound, a method that looks better than another has measurably higher "
    "error against the ground truth, and this cannot be engineered away.",
    "<b>Which explains why PSNR rankings and human visual rankings "
    "disagree</b>, sometimes dramatically. They are not measuring the same "
    "thing badly; they are measuring genuinely opposed objectives, and a "
    "method can only move along the tradeoff curve rather than off it.",
    "<b>And it is why serious papers report both</b>, and why you should "
    "always ask which objective a claim is about. 'State of the art' means "
    "nothing without saying on which axis."]),

  ("break",),
  ("h1", "3 &nbsp; Restoration and synthesis"),
  ("table", ["", "Restoration", "Synthesis"],
   [["Recovers", "Information that is <b>present but degraded</b> — "
     "buried in noise, attenuated by blur, subsampled.",
     "Information that <b>was never measured</b> at all."],
    ["Examples", "Denoising; mild deblurring; demosaicing; modest "
     "upscaling.",
     "Large-factor upscaling; inpainting; recovering frequencies beyond the "
     "lens cutoff; filling occluded regions."],
    ["The answer is determined by",
     "<b>The measurement</b>, with the prior resolving residual ambiguity.",
     "<b>The prior</b>, with the measurement providing loose constraints."],
    ["More training data", "Converges toward the true answer.",
     "<b>Changes what is invented, not whether</b> something is invented."]],
   [0.17, 0.41, 0.42]),
  ("p", "<b>Most real methods do both</b>, often within a single output and "
        "without marking the boundary. <b>That boundary is where the honesty "
        "is required</b>, and it is almost never reported."),
  ("callout", "The upscaled face is not that person's face",
   ["<b>Take a 16&times;16 pixel face and upscale it by a factor of eight "
    "with a modern model.</b> The result is a sharp, detailed, entirely "
    "plausible face.",
    "<b>It is not the face of the person who was photographed.</b> The "
    "information distinguishing one face from another at that scale was "
    "never recorded — it is below the sampling limit. The model has "
    "produced <i>a</i> face consistent with the low-resolution evidence and "
    "with its training distribution.",
    "<b>Different models produce different faces from the same input</b>, "
    "and the same model with a different random seed can too. <b>That is the "
    "proof</b>: if the information were present in the input, they would "
    "agree.",
    "<b>This matters in forensics, in medical imaging, and in "
    "journalism</b>, where an image is used as evidence about what was "
    "there. A plausible reconstruction presented as a photograph is a claim "
    "that has not been earned. <b>Module 13 takes this up as the subject "
    "rather than the caveat.</b>"]),
  ("ul", ["<b>Distribution shift.</b> A model trained on one camera's noise "
          "characteristics, or one population of scenes, degrades on "
          "another — and degrades silently.",
          "<b>Confident wrongness.</b> Most deployed models produce no "
          "uncertainty estimate, and <b>the output looks exactly as "
          "plausible when it is wrong as when it is right</b>. There is no "
          "signal to the user that this particular output should not be "
          "trusted. <b>Operationally this is the most serious of the "
          "failures</b>, because every other one could be managed if it "
          "announced itself.",
          "<b>Hallucinated structure.</b> Text rendered as text-like marks "
          "that are not words, regular patterns found in noise, faces "
          "constructed from ambiguous evidence. The model produces what its "
          "training distribution says is likely.",
          "<b>Averaging away rare content.</b> Genuinely unusual but real "
          "detail is improbable under the learned prior, so it is treated as "
          "noise and removed — which is exactly backwards for "
          "scientific or forensic imaging, where the unusual thing is the "
          "point.",
          "<b>And bias from the training distribution</b>, which for "
          "face-related tasks has been demonstrated repeatedly: upscaling "
          "and restoration models have been shown to shift facial features "
          "toward the demographics over-represented in their training data. "
          "<b>This is not a hypothetical failure</b> and it is a direct "
          "consequence of synthesis from a prior."]),
 ],
 "resources": [
   ("Blau & Michaeli &mdash; The Perception-Distortion Tradeoff (free)",
    "https://arxiv.org/abs/1711.06077",
    "<b>The theorem in &sect;2.</b> Read it before making any claim that one "
    "method is better than another."),
   ("Zhang et al. &mdash; The Unreasonable Effectiveness of Deep Features "
    "as a Perceptual Metric (LPIPS, free)",
    "https://richzhang.github.io/PerceptualSimilarity/",
    "Perceptual metrics, and a clear demonstration of where PSNR fails to "
    "track human judgement."),
   ("Chen et al. &mdash; Learning to See in the Dark (free)",
    "https://cchen156.github.io/SID.html",
    "End-to-end raw-to-RGB in extreme low light. The clearest demonstration "
    "of the &sect;1 argument, with a dataset."),
   ("Menon et al. &mdash; PULSE, and the subsequent discussion (free)",
    "https://arxiv.org/abs/2003.03808",
    "<b>The upscaling case of &sect;3</b>, including the bias findings that "
    "followed publication. Read the paper and the critique together."),
 ],
 "exercises": [
   "Train or download a denoiser with an L2 loss and one with an adversarial "
   "loss. Compare PSNR and compare appearance, and confirm the ranking "
   "inverts.",
   "Demonstrate the L2 blurring argument directly: construct a case with two "
   "equally plausible outputs and show that the L2-optimal prediction is "
   "neither.",
   "Measure PSNR and LPIPS for several methods and plot them against each "
   "other. The tradeoff curve should be visible.",
   "<b>Upscale the same low-resolution face with three different models</b> "
   "and compare the results. Document that they disagree.",
   "Run the same diffusion-based restoration twice with different seeds and "
   "compare.",
   "Apply a denoiser trained on one camera's noise to another camera's raw "
   "files and document the degradation.",
   "Find a case where a learned method removes real but unusual detail. "
   "Astronomical or microscopy images are the easiest place to look.",
   "Compare a learned demosaicer against the Malvar method (Module 05) on "
   "difficult texture, and identify where the learned one invents.",
   "For one output of a learned pipeline, mark the regions that are "
   "restoration and the regions that are synthesis, and justify the "
   "boundary.",
 ],
 "selfcheck": [
   "Why are learned methods well suited to the problems in this course?",
   "What is the argument for end-to-end over staged processing?",
   "Why does L2 loss necessarily produce blur, and why is that not a bug?",
   "Name five losses and the appearance each produces.",
   "State the perception–distortion tradeoff and say what kind of "
   "result it is.",
   "Distinguish restoration from synthesis on four axes.",
   "Why is an upscaled face not that person's face, and what is the proof?",
   "Name five failure modes of learned methods and say which is most serious "
   "operationally.",
 ],
},

# =========================================================== MODULE 13 ======
{
 "n": 13,
 "title": "What a Photograph Is Now",
 "subtitle": "Measurement, inference, and what you can claim.",
 "question": "If the image is computed, what does it document?",
 "outcomes": [
     "Articulate where the boundary between photography and synthesis sits.",
     "Explain provenance approaches and their limits.",
     "Evaluate computational imaging claims critically.",
     "State the obligations that follow for a practitioner.",
     "Situate this course's methods against those questions.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The boundary",
   "blurb": "It was never where people thought."},

  {"t": "callout", "title": "Photography was never a pure measurement",
   "kind": "The historical correction",
   "body": ["<b>Film had a response curve</b>, a spectral sensitivity, and "
            "a development process with choices in it.",
            "<b>Dodging and burning are as old as the darkroom.</b> Ansel "
            "Adams's prints are heavily interpreted and nobody considers them "
            "fraudulent.",
            "<b>So 'the camera does not lie' was always false</b>, and the "
            "question is one of degree rather than kind.",
            "<b>But the degree has changed enormously</b>, and a difference "
            "of several orders of magnitude in degree is worth treating as a "
            "difference in kind."]},

  {"t": "table", "kicker": "Spectrum", "title": "From measurement to synthesis",
   "header": ["Operation", "Status"],
   "widths": [4.6, 7.5],
   "rows": [
     ["Exposure, white balance, tone curve", "<b>Interpretation of a measurement</b>"],
     ["Demosaicing", "<b>Interpolation — 2/3 invented, constrained</b>"],
     ["Burst merging", "<b>Still measurement — more of it</b>"],
     ["Denoising", "Estimation under a noise model"],
     ["<b>Learned denoising, upscaling</b>", "<b>Inference from a prior</b>"],
     ["<b>Generative fill, sky replacement</b>", "<b>Synthesis</b>"],
   ],
   "footnote": "<b>There is no sharp line</b>, and the gradient is real. "
               "The obligation is to say where on it you are.",
   "note": "The spectrum framing is more useful than any attempt to draw a "
           "line, which always fails."},

  {"t": "section", "label": "Part 2", "title": "Provenance",
   "blurb": "Attempts to record what happened."},

  {"t": "bullets", "kicker": "Approaches", "title": "Establishing what an image is",
   "items": [
     "<b>C2PA / Content Credentials:</b> cryptographically signed metadata "
     "recording capture and every edit. The most serious current effort.",
     "",
     "<b>Signed capture:</b> the camera signs the raw file at the moment of "
     "capture.",
     "",
     "<b>Forensic analysis:</b> detect manipulation from sensor noise "
     "patterns, compression artefacts, and lighting inconsistency.",
     "",
     "<b>Watermarking</b> generated content, which the generator must "
     "cooperate with.",
     "",
     "<b>And each has real limits.</b>",
   ],
   "note": "C2PA is the one with institutional momentum and is worth "
           "knowing by name."},

  {"t": "callout", "title": "Provenance establishes history, not truth",
   "kind": "The limit worth understanding",
   "body": ["<b>A signed chain tells you what was done to an image</b>, not "
            "whether it depicts what it appears to.",
            "<b>A photograph of a staged scene is unmanipulated and "
            "misleading.</b> Signing it changes nothing.",
            "<b>And the chain breaks easily</b> — a screenshot, a "
            "re-encode, a crop by a tool that does not participate.",
            "<b>Absence of credentials cannot mean fake</b>, or every "
            "legitimate photograph from a non-participating camera is "
            "condemned. <b>Which makes the signal much weaker than it first "
            "appears.</b>"]},

  {"t": "section", "label": "Part 3", "title": "Evaluating claims",
   "blurb": "Reading computational imaging results critically."},

  {"t": "bullets", "kicker": "Questions", "title": "What to ask of any result",
   "items": [
     "<b>What was measured, and what was inferred?</b> The question this "
     "whole course keeps returning to.",
     "",
     "<b>What is the ground truth, and how was it obtained?</b> A "
     "comparison against another algorithm is not a comparison against "
     "reality.",
     "",
     "<b>Which metric, and on which axis of the tradeoff?</b> "
     "(Module 12.)",
     "",
     "<b>What are the failure cases, and were any shown?</b> A paper with "
     "no failure figure has not looked.",
     "",
     "<b>Is the comparison equal-effort?</b> A tuned new method against an "
     "untuned baseline is not a comparison.",
   ],
   "footnote": "These generalise well beyond this subject and are worth "
               "carrying.",
   "note": "This checklist is probably the most transferable thing in the "
           "module."},

  {"t": "callout", "title": "The obligations are modest and specific",
   "kind": "What follows for you",
   "body": ["<b>Say what you did.</b> If the image is a burst merge with a "
            "learned denoiser, say so — in a caption, a methods section, "
            "or metadata.",
            "<b>Distinguish the pleasing result from the measurement</b>, "
            "and keep both when the measurement matters.",
            "<b>Do not present synthesis as evidence.</b> An upscaled "
            "licence plate is not a reading of a licence plate.",
            "<b>And know which you are doing</b> — which requires "
            "understanding the pipeline, which is what this course was "
            "for."]},

  {"t": "section", "label": "Part 4", "title": "Where this leaves you",
   "blurb": "The course, closed."},

  {"t": "bullets", "kicker": "Summary", "title": "What you can now do",
   "items": [
     "Take a raw file and produce a displayable image through code you "
     "wrote, justifying every stage.",
     "Merge exposures, align bursts, composite seamlessly, and estimate "
     "depth.",
     "Recognise an underdetermined problem and identify the prior being "
     "used to resolve it.",
     "Read a computational imaging claim critically and ask the right "
     "questions of it.",
     "",
     "<b>And say, of any image you produce, which parts were measured and "
     "which were inferred.</b>",
   ],
   "note": "The last line is the course's actual thesis and the thing worth "
           "retaining."},

  {"t": "callout", "title": "The connections across the program",
   "kind": "Closing",
   "body": ["<b>CSCE 647</b> computed images from scenes; this course "
            "recovered scenes from images. <b>Radiance invariance and linear "
            "workflow appear in both</b>, from opposite directions.",
            "<b>CSCE 649's Poisson solve, Module 08's seamless cloning, and "
            "Module 11's matting Laplacian are the same linear system</b>, "
            "arrived at three times.",
            "<b>CSCE 650</b> put a person inside the result; <b>CSCE 735</b> "
            "makes any of it fast enough.",
            "<b>And the discipline is the same throughout:</b> know what "
            "your method assumes, know where it fails, and say which is "
            "which."]},
 ],
 "takeaways": [
   "Photography was never a pure measurement — film had a response "
   "curve and the darkroom had choices. The change is of degree, and the "
   "degree is enormous.",
   "The spectrum runs from interpretation through interpolation and "
   "estimation to inference and outright synthesis, with no sharp line.",
   "Provenance systems like C2PA record an image's history; they do not "
   "establish that it depicts what it appears to.",
   "Absence of credentials cannot imply fakery, which makes the signal much "
   "weaker than it first appears.",
   "Ask of any result: what was measured, what was inferred, what is the "
   "ground truth, which metric, and which failures were shown.",
   "The obligation is modest: say what you did, keep the measurement when it "
   "matters, and never present synthesis as evidence.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Where the boundary sits"),
  ("callout", "Photography was never a pure measurement",
   ["<b>Film had a characteristic response curve</b> — non-linear, "
    "with a toe and a shoulder — a particular spectral sensitivity that "
    "did not match the eye, and a development process with substantial "
    "latitude in it.",
    "<b>Dodging and burning are as old as the darkroom.</b> Ansel Adams's "
    "prints are heavily and deliberately interpreted — his zone system "
    "is a methodology for deciding what the print should say — and "
    "nobody regards them as fraudulent.",
    "<b>So 'the camera does not lie' was always false</b>, and anyone "
    "framing the current situation as a fall from a prior state of "
    "mechanical objectivity is mistaken about the history.",
    "<b>But the degree has changed by orders of magnitude.</b> A tone curve "
    "interprets a measurement; a generative fill produces content that was "
    "never in front of the lens. <b>A sufficiently large difference of "
    "degree is worth treating as a difference in kind</b>, and the "
    "appropriate response is to be precise rather than to deny that anything "
    "has changed."]),
  ("table", ["Operation", "What it is"],
   [["<b>Exposure, white balance, tone curve</b>",
     "<b>Interpretation of a measurement.</b> The data constrains the "
     "result tightly; the choices are about presentation (Modules 04, 05)."],
    ["<b>Demosaicing</b>",
     "<b>Interpolation.</b> Two-thirds of the colour data is produced "
     "rather than measured — and tightly constrained by the "
     "surrounding measurements (Module 05)."],
    ["<b>Burst merging</b>",
     "<b>Still measurement, and more of it.</b> Averaging aligned frames "
     "produces an estimate that converges to the truth with more frames "
     "(Module 10)."],
    ["<b>Classical denoising</b>",
     "Estimation under an explicit noise model. The prior is simple and "
     "stated (Module 01)."],
    ["<b>Learned denoising and upscaling</b>",
     "<b>Inference from a learned prior.</b> The result is plausible given "
     "the data and the training distribution, and it is not determined by "
     "the data (Module 12)."],
    ["<b>Generative fill, sky replacement, object removal</b>",
     "<b>Synthesis.</b> Content that was not photographed."]],
   [0.33, 0.67]),
  ("p", "<b>There is no sharp line, and the gradient is real.</b> Attempts "
        "to legislate a boundary — 'adjustments are acceptable and "
        "manipulations are not' — fail immediately on contact with the "
        "cases. <b>The obligation is not to locate a line but to say where "
        "on the spectrum a given image sits</b>, which is a question anyone "
        "who understands their pipeline can answer."),

  ("h1", "2 &nbsp; Provenance"),
  ("ul", ["<b>C2PA and Content Credentials.</b> Cryptographically signed "
          "metadata recording the capture device and every subsequent edit, "
          "forming a verifiable chain. Backed by camera manufacturers, "
          "software vendors, and news organisations. <b>The most serious "
          "current effort</b> and the one to know by name.",
          "<b>Signed capture.</b> The camera signs the raw file at the "
          "moment of capture, so any later alteration invalidates the "
          "signature. Requires hardware support and secure key storage.",
          "<b>Forensic analysis.</b> Detect manipulation after the fact from "
          "sensor pattern noise (every sensor has a unique fingerprint), "
          "inconsistent compression history, impossible lighting or shadow "
          "geometry, and resampling traces. Works, and is an arms race.",
          "<b>Watermarking generated content</b>, so that synthetic images "
          "identify themselves. Requires the generator's cooperation, which "
          "means it addresses responsible actors only.",
          "<b>Each has real and specific limits</b>, and the one in the "
          "callout below applies to all of them."]),
  ("callout", "Provenance establishes history, not truth",
   ["<b>A signed chain of custody tells you what was done to an image.</b> "
    "It does not tell you whether the image depicts what it appears to "
    "depict.",
    "<b>A photograph of a staged scene is entirely unmanipulated and "
    "completely misleading.</b> So is a true photograph with a false "
    "caption, or one cropped to exclude context, or one taken at a moment "
    "unrepresentative of events. <b>Signing changes none of this</b>, and it "
    "is the larger share of how photographs actually mislead.",
    "<b>And the chain breaks easily.</b> A screenshot, a re-encode, an "
    "upload through a platform that strips metadata, or a crop by a tool "
    "that does not participate — any of these severs it, and all of "
    "them are routine.",
    "<b>Which creates the asymmetry that limits the whole approach:</b> "
    "absence of credentials cannot be taken to mean an image is fake, or "
    "every legitimate photograph from a non-participating camera, or any "
    "image that passed through ordinary tooling, stands condemned. <b>So the "
    "signal is positive-only and therefore much weaker than it first "
    "appears</b> — it can support a claim of authenticity and cannot "
    "refute one."]),

  ("break",),
  ("h1", "3 &nbsp; Evaluating claims"),
  ("ol", ["<b>What was measured, and what was inferred?</b> The question "
          "this course has returned to in every module. For any output, ask "
          "which parts are constrained by the data and which by a prior.",
          "<b>What is the ground truth, and how was it obtained?</b> A "
          "comparison against another algorithm's output is not a comparison "
          "against reality. Ground truth for restoration means a genuinely "
          "clean capture — a long exposure, a controlled setup, a "
          "higher-quality instrument — and if none was available, the "
          "evaluation is relative rather than absolute.",
          "<b>Which metric, and on which axis of the tradeoff?</b> PSNR "
          "favours blur; perceptual metrics favour plausibility; they are "
          "opposed by a theorem (Module 12). A method cannot be better on "
          "both past the bound, so a claim of being better needs to say "
          "better at what.",
          "<b>What are the failure cases, and were any shown?</b> <b>A "
          "paper or product with no failure figure has not looked</b>, or "
          "has looked and declined to report. Every method in this course "
          "has inputs that defeat it, and knowing them is more useful than "
          "another percentage point.",
          "<b>Is the comparison equal-effort?</b> A carefully tuned new "
          "method against a baseline run at its defaults is not a "
          "comparison. Nor is a comparison at equal iterations when the "
          "methods have different per-iteration costs — the equal-time "
          "discipline from CSCE 647 applies here too."]),
  ("p", "<b>These questions generalise well beyond computational "
        "photography</b>, and they are probably the most transferable thing "
        "in this module."),
  ("callout", "The obligations are modest and specific",
   ["<b>Say what you did.</b> If an image is a fifteen-frame burst merge "
    "with a learned denoiser and a local tone map, say so — in a "
    "caption, a methods section, or the metadata. This costs nothing and it "
    "is the whole of the obligation in most contexts.",
    "<b>Distinguish the pleasing result from the measurement, and keep both "
    "when the measurement matters.</b> In science, medicine, forensics, and "
    "journalism, the processed image is a derived product and the "
    "measurement should be retained and available.",
    "<b>Do not present synthesis as evidence.</b> <b>An upscaled licence "
    "plate is not a reading of a licence plate</b> (Module 12), a "
    "reconstructed face is not an identification, and an inpainted region is "
    "not a record of what was there. This is the one that has real "
    "consequences.",
    "<b>And know which you are doing</b> — which requires "
    "understanding the pipeline you are using, including the parts a vendor "
    "has not documented. <b>That understanding is what this course was "
    "for.</b>"]),

  ("h1", "4 &nbsp; Where this leaves you"),
  ("ul", ["<b>You can take a raw file and produce a displayable image "
          "through code you wrote</b>, and justify every stage between the "
          "two — black level, white balance, demosaic, colour matrix, "
          "denoise, tone map, encode.",
          "<b>You can merge exposures, align and merge bursts, composite "
          "seamlessly, estimate depth, and render synthetic defocus</b>, and "
          "you have measured the results against ground truth you captured "
          "yourself.",
          "<b>You can recognise an underdetermined problem</b> — which "
          "is nearly all of them — <b>and identify the prior being used "
          "to resolve it</b>, whether it is hand-designed or learned.",
          "<b>You can read a computational imaging claim critically</b> and "
          "ask the five questions in &sect;3 of it.",
          "<b>And you can say, of any image you produce, which parts were "
          "measured and which were inferred.</b> <b>That is the course's "
          "actual thesis</b>, and it is the thing worth retaining when the "
          "specific algorithms have been superseded — which, given the "
          "pace of this field, they will be."]),
  ("callout", "The connections across the program",
   ["<b>CSCE 647 computed images from scene descriptions; this course "
    "recovered scene properties from images.</b> The two share more than the "
    "subject suggests: radiance invariance underlies both ray tracing and "
    "the 4D light field (Module 09), and the rule that all processing "
    "happens in linear space with encoding last was reached independently "
    "from both directions.",
    "<b>CSCE 649's pressure projection, Module 08's seamless cloning, and "
    "Module 11's matting Laplacian are the same sparse linear system</b>, "
    "arrived at three times from three unrelated problems. Recognising a "
    "Poisson problem is worth more than any individual algorithm.",
    "<b>CSCE 650 put a person inside the result</b> and made the constraint "
    "physiological; <b>CSCE 735 makes any of it fast enough to matter.</b>",
    "<b>And the discipline has been the same throughout the program:</b> "
    "know what your method assumes, know where it fails, measure rather than "
    "assert, and be explicit about which of your claims are "
    "measurements and which are inferences. <b>That is more durable than any "
    "of the techniques</b>, and it is what the whole degree was for."]),
 ],
 "resources": [
   ("C2PA &mdash; Coalition for Content Provenance and Authenticity (free "
    "specification)",
    "https://c2pa.org/",
    "The provenance standard of &sect;2. The specification is readable and "
    "the threat model section is the honest part."),
   ("Farid &mdash; Photo Forensics",
    "https://farid.berkeley.edu/",
    "The forensic analysis of &sect;2, from the leading researcher. His "
    "papers and course material are free."),
   ("Levoy &mdash; writings on computational photography and what it means "
    "(free)",
    "https://sites.google.com/site/marclevoylectures/",
    "Thoughtful on the &sect;1 question from someone who built the "
    "pipelines that raised it."),
   ("Reuters and AP photo manipulation standards (free)",
    "https://www.reuters.com/",
    "How news organisations actually draw the line — worth reading "
    "because they had to be specific where academics can be vague."),
 ],
 "exercises": [
   "Take one of your own photographs and write a complete account of every "
   "transformation between the sensor and the file, including the ones your "
   "camera performed without telling you.",
   "Mark, on one output image from your Project 2 pipeline, the regions that "
   "are measurement, interpolation, estimation, and synthesis.",
   "Examine the Content Credentials of an image that has them, and then "
   "screenshot it and observe what survives.",
   "Find a photograph that is unmanipulated and misleading, and one that is "
   "manipulated and honest. Write a paragraph on each.",
   "Take a published computational imaging result and apply the five "
   "questions of &sect;3. Report which it answers.",
   "Find a paper with no failure cases shown, and construct an input that "
   "defeats its method.",
   "Write the caption you would attach to a night-mode photograph submitted "
   "as evidence, describing what it does and does not document.",
   "Compare the photo manipulation standards of two news organisations and "
   "identify where they differ.",
   "<b>Project 2 is now due.</b> Submit the pipeline, the quantitative "
   "evaluation against ground truth, the stage-by-stage figure, the "
   "documented failure, and the written account of what was measured and "
   "what was inferred.",
 ],
 "selfcheck": [
   "Why was photography never a pure measurement, and what has actually "
   "changed?",
   "Place six operations on the spectrum from interpretation to synthesis.",
   "Name four provenance approaches.",
   "What does provenance establish, and what does it not?",
   "Why is absence of credentials not evidence of fakery, and what does that "
   "imply?",
   "Give the five questions to ask of any computational imaging claim.",
   "State the four obligations that follow for a practitioner.",
   "What is the course's thesis in one sentence?",
   "Name three connections between this course and others in the program.",
 ],
},

]
