# -*- coding: utf-8 -*-
"""CSCE 753 — Modules 02-07."""

MODULES = [

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Cameras and Calibration",
 "subtitle": "What the numbers in a camera matrix mean.",
 "question": "How does a point in the world become a pixel, and how do "
             "you measure the mapping?",
 "outcomes": [
     "Write the full projection from world to pixel.",
     "State what each intrinsic and extrinsic parameter means.",
     "Explain lens distortion and when it matters.",
     "Calibrate a camera and assess the result.",
     "Explain why homogeneous coordinates are used.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The projection chain",
   "blurb": "World to camera to image to pixel, in four steps."},

  {"t": "eq", "kicker": "Projection", "title": "World point to pixel",
   "eqs": [
     ("x_cam = R · X_world + t",
      "Extrinsics: a rigid transform. Six degrees of freedom — three "
      "rotation, three translation."),
     ("x_img = ( X/Z , Y/Z )",
      "Perspective division. This is the only non-linear step, and it "
      "is where the information is lost."),
     ("u = fₓ·x + cₓ ,   v = f_y·y + c_y",
      "Intrinsics: focal lengths in pixels and the principal point."),
     ("p ≃ K [R | t] X",
      "The whole chain, in homogeneous coordinates, as one 3×4 matrix."),
   ],
   "caption": "<b>The perspective division is the lossy step</b> "
              "— everything else is invertible, which is why "
              "Module 01's ambiguities are all depth-related.",
   "note": "Pointing out which single step loses the information is the "
           "key insight here."},

  {"t": "callout", "title": "Why homogeneous coordinates",
   "kind": "Not a formality",
   "body": ["<b>Perspective projection is not linear</b> — it divides "
            "by Z — so it cannot be a matrix in ordinary "
            "coordinates.",
            "<b>Append a 1, work up to scale, and it becomes linear.</b> "
            "The entire projection is then one matrix multiply, and "
            "composing transforms is composing matrices.",
            "<b>Points at infinity become representable</b> — a "
            "direction is a point with last coordinate 0 — which "
            "makes vanishing points first-class objects rather than "
            "special cases.",
            "<b>And lines and points become dual</b>: a line is a "
            "3-vector, a point is on a line when their dot product is "
            "zero, and the line through two points is their cross "
            "product. <b>That duality makes Module 04's algebra "
            "tractable.</b>"]},

  {"t": "section", "label": "Part 2", "title": "The intrinsics",
   "blurb": "Five numbers, and what each one is."},

  {"t": "table", "kicker": "Intrinsics", "title": "What the parameters mean physically",
   "header": ["Parameter", "Meaning", "Typical behaviour"],
   "widths": [2.4, 4.4, 5.3],
   "rows": [
     ["<b>fₓ, f_y</b>", "<b>Focal length in PIXELS, not millimetres</b>", "<b>Equal unless pixels are non-square</b>"],
     ["<b>cₓ, c_y</b>", "<b>Principal point — where the optical axis hits the sensor</b>", "<b>Near the centre; offset by sensor mounting</b>"],
     ["<b>s (skew)</b>", "Non-perpendicular pixel axes", "<b>Essentially always 0. Fix it at 0</b>"],
     ["<b>k₁, k₂, k₃</b>", "<b>Radial distortion</b>", "<b>Large on wide lenses; k₁ dominates</b>"],
     ["<b>p₁, p₂</b>", "Tangential distortion (lens not parallel to sensor)", "Small; often fixed at 0"],
   ],
   "footnote": "<b>Focal length in pixels is the point people trip "
               "over:</b> it is (focal length in mm) × (pixels per "
               "mm), so it changes when you resize the image.",
   "note": "The resize gotcha causes real bugs; state it explicitly."},

  {"t": "callout", "title": "Distortion, and when to care",
   "kind": "The practical judgement",
   "body": ["<b>Radial distortion bends straight lines</b> — barrel on "
            "wide lenses, pincushion on some telephotos — and it is "
            "a function of radius from the principal point only.",
            "<b>It is largest at the image corners and zero at the "
            "centre</b>, so a method using only central features may "
            "ignore it and one using the whole frame cannot.",
            "<b>At 10 pixels of corner displacement, ignoring it costs "
            "you more than every other error source combined.</b> On a "
            "narrow lens it may be under a pixel.",
            "<b>Undistort once, then work in ideal coordinates</b> "
            "— every geometric method in Modules 04–07 assumes "
            "a pinhole camera, and feeding it distorted points produces "
            "a plausible, wrong answer."]},

  {"t": "section", "label": "Part 3", "title": "Calibrating",
   "blurb": "Measuring the parameters from images of a known object."},

  {"t": "code", "kicker": "Calibration", "title": "The procedure, and the three ways it goes wrong",
   "lang": "python", "code": """
  # 1. Print a checkerboard. MEASURE the square size with a
  #    ruler -- "printed at 100%" is frequently false.
  # 2. Capture 15-25 images with the board at VARIED
  #    orientations, filling different parts of the frame.
  # 3. Detect corners to sub-pixel accuracy.
  # 4. Solve for K, distortion, and each board's pose by
  #    minimising REPROJECTION ERROR (a bundle adjustment,
  #    Module 05, in miniature).
  # 5. Report mean reprojection error in pixels.
  #    Good: < 0.3 px.  Suspicious: < 0.05 px (overfit).
  #    Bad: > 1 px.

  # THE THREE FAILURES, in order of frequency:
  #   ALL BOARDS NEAR-FRONTAL -> f and Z are confounded,
  #       the error looks fine, f is wrong. TILT THE BOARD.
  #   AUTOFOCUS ON -> intrinsics differ between frames and
  #       no single K fits. LOCK THE FOCUS.
  #   BOARD ONLY IN THE CENTRE -> distortion unconstrained,
  #       k1 is garbage. FILL THE CORNERS.
""",
   "caption": "<b>A low reprojection error does not mean a correct "
              "calibration</b> — it means the model fits the images "
              "you gave it, which is CSCE 633's overfitting in a "
              "geometric costume.",
   "note": "The frontal-board degeneracy is the one that silently ruins "
           "student projects."},

  {"t": "section", "label": "Part 4", "title": "Checking it",
   "blurb": "Verifying a calibration against something other than its "
            "own residual."},

  {"t": "bullets", "kicker": "Verification", "title": "Independent checks on a calibration",
   "items": [
     "<b>Undistort an image of a straight edge</b> — a door frame, "
     "a building. <b>It should be straight. This catches a wrong k₁ "
     "instantly.</b>",
     "",
     "<b>Measure a known distance</b> by triangulating from two "
     "calibrated views, and compare against a ruler.",
     "",
     "<b>Hold out some calibration images</b> and report the error on "
     "them. <b>CSCE 633's train/test split, applied to geometry.</b>",
     "",
     "<b>Check f against the specification:</b> focal length in mm "
     "× pixels per mm should roughly match your estimate.",
     "",
     "<b>Recalibrate on a different day</b> and compare. <b>Large "
     "disagreement means the procedure, not the camera, is "
     "unstable.</b>",
   ],
   "footnote": "<b>The straight-edge test takes two minutes and catches "
               "most bad calibrations</b>, and almost nobody does it."},

  {"t": "callout", "title": "Calibration drifts",
   "kind": "The deployment fact",
   "body": ["<b>Thermal expansion changes the focal length measurably</b> "
            "over a camera's warm-up period, which is minutes.",
            "<b>Mechanical shock moves the sensor relative to the "
            "lens</b>, changing the principal point — and a dropped "
            "camera is silently decalibrated.",
            "<b>So production systems either recalibrate "
            "continuously</b> (self-calibration from the scene) <b>or "
            "treat the intrinsics as slowly-varying unknowns</b> in the "
            "bundle adjustment.",
            "<b>Which is why Module 13 returns to this:</b> <b>a "
            "calibration is a measurement with a validity period</b>, not "
            "a constant, and systems that assume otherwise degrade "
            "invisibly."]},
 ],
 "takeaways": [
   "The projection chain is a rigid transform, a perspective division, and "
   "an affine pixel mapping — and only the division loses "
   "information.",
   "Homogeneous coordinates make projection linear, make points at "
   "infinity representable, and make point-line duality available.",
   "Focal length is in pixels, so it changes when you resize the image "
   "— a common and silent bug.",
   "Radial distortion is zero at the centre and largest at the corners, so "
   "whether it matters depends on which features you use.",
   "A low reprojection error means the model fits the images you supplied, "
   "which is overfitting in geometric costume — hold images out.",
   "Near-frontal boards confound focal length with distance, which is the "
   "most common silent calibration failure.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The projection chain"),
  ("eq", "x<sub>cam</sub> = R X<sub>world</sub> + t &nbsp;&nbsp; "
         "(extrinsics: 6 degrees of freedom)"),
  ("eq", "(x, y) = (X/Z, &nbsp; Y/Z) &nbsp;&nbsp; (perspective "
         "division)"),
  ("eq", "u = f<sub>x</sub> x + c<sub>x</sub>, &nbsp;&nbsp; "
         "v = f<sub>y</sub> y + c<sub>y</sub> &nbsp;&nbsp; (intrinsics)"),
  ("eq", "p &asymp; K [R | t] X &nbsp;&nbsp; (the whole chain, up to "
         "scale)"),
  ("p", "<b>The perspective division is the only non-linear step and the "
        "only lossy one.</b> The rigid transform is invertible, the pixel "
        "mapping is invertible, and the division discards Z while keeping "
        "X/Z and Y/Z. <b>Which is why every ambiguity in Module 01 was "
        "ultimately a depth ambiguity</b> — that is literally the "
        "quantity the camera throws away, and recovering it is the whole "
        "project of Modules 04 through 06."),
  ("callout", "Why homogeneous coordinates",
   ["<b>Perspective projection divides by Z, so it is not a linear map</b> "
    "and cannot be written as a matrix in ordinary Cartesian coordinates. "
    "This is a genuine obstacle rather than a notational inconvenience.",
    "<b>Append a 1 to each point, treat vectors as equivalent up to "
    "scale, and the projection becomes linear.</b> The entire world-to-"
    "pixel chain is then a single 3&times;4 matrix, and composing "
    "transformations is matrix multiplication — which is what makes "
    "the algebra of the next three modules manageable.",
    "<b>Points at infinity become representable:</b> a point with final "
    "coordinate 0 is a direction rather than a location, so <b>vanishing "
    "points become ordinary objects you can compute with</b> rather than "
    "special cases needing separate code. Two parallel lines genuinely do "
    "intersect, at an infinite point, and the formula is the same one as "
    "for any other pair.",
    "<b>And points and lines become dual.</b> A 2D line is a 3-vector, a "
    "point lies on a line exactly when their dot product vanishes, the "
    "line through two points is their cross product, and the intersection "
    "of two lines is also their cross product. <b>That duality is what "
    "makes Module 04's epipolar algebra tractable</b> rather than a "
    "trigonometric mess."]),

  ("h1", "2 &nbsp; The intrinsics"),
  ("table", ["Parameter", "What it is", "Typical behaviour"],
   [["<b>f<sub>x</sub>, f<sub>y</sub></b>",
     "<b>Focal length expressed in PIXELS, not millimetres.</b>",
     "<b>Equal unless the pixels are non-square</b>, which is rare on "
     "modern sensors. <b>It is (focal length in mm) &times; (pixels per "
     "mm), so it scales when you resize the image</b> — halve the "
     "resolution and f halves. This is the single most common intrinsics "
     "bug."],
    ["<b>c<sub>x</sub>, c<sub>y</sub></b>",
     "<b>The principal point — where the optical axis meets the "
     "sensor.</b>",
     "Near the image centre, displaced by a few pixels to a few tens by "
     "sensor mounting tolerance. <b>Fixing it at the exact centre is a "
     "reasonable approximation and a measurable error.</b>"],
    ["<b>s (skew)</b>", "Non-perpendicular pixel axes.",
     "<b>Essentially always zero on real sensors. Fix it at zero</b> "
     "— estimating it absorbs noise and destabilises the rest."],
    ["<b>k<sub>1</sub>, k<sub>2</sub>, k<sub>3</sub></b>",
     "<b>Radial lens distortion coefficients.</b>",
     "<b>Large on wide-angle lenses, small on narrow ones, and "
     "k<sub>1</sub> dominates.</b> Estimating k<sub>3</sub> without "
     "corner coverage produces an unstable fit — prefer a two-"
     "coefficient model unless the lens is extreme."],
    ["<b>p<sub>1</sub>, p<sub>2</sub></b>",
     "Tangential distortion, from the lens not being exactly parallel to "
     "the sensor.",
     "Small on assembled cameras. Often fixed at zero, and estimating it "
     "rarely improves the reprojection error meaningfully."]],
   [0.16, 0.34, 0.50]),
  ("callout", "Distortion, and when to care",
   ["<b>Radial distortion bends straight lines</b> — barrel on "
    "wide-angle lenses, pincushion on some telephotos — and it is a "
    "function of radius from the principal point alone, which is why one "
    "or two coefficients suffice.",
    "<b>It is exactly zero at the principal point and largest at the "
    "corners.</b> <b>So whether it matters depends on which image "
    "regions your features occupy:</b> a method using only central "
    "features can reasonably ignore it, and one using the whole frame "
    "cannot.",
    "<b>On a wide lens with 10 pixels of corner displacement, ignoring "
    "distortion dominates every other error source combined.</b> On a "
    "narrow lens it may be well under a pixel and safely neglected. "
    "<b>Measure it rather than assuming either way.</b>",
    "<b>Undistort once, then work in ideal pinhole coordinates.</b> "
    "<b>Every geometric method in Modules 04 through 07 assumes a "
    "pinhole camera</b>, and feeding distorted points into the essential "
    "matrix estimation produces a plausible-looking, systematically wrong "
    "answer — which is far worse than an obvious failure, because "
    "nothing signals it."]),

  ("break",),
  ("h1", "3 &nbsp; Calibrating a camera"),
  ("code", """# 1. Print a checkerboard. MEASURE the square size with a
#    ruler -- "printed at 100%" is frequently false, and a
#    5% scale error becomes a 5% error in every distance
#    you later triangulate.
# 2. Capture 15-25 images with the board at VARIED
#    orientations, filling different parts of the frame.
# 3. Detect corners to sub-pixel accuracy.
# 4. Solve for K, the distortion coefficients, and each
#    board pose by minimising REPROJECTION ERROR -- which
#    is Module 05's bundle adjustment in miniature.
# 5. Report the mean reprojection error in pixels.
#    Good:        below 0.3 px
#    Suspicious:  below 0.05 px  (you are overfitting)
#    Bad:         above 1 px

# THE THREE FAILURES, in order of frequency:
#
#   ALL BOARDS NEAR-FRONTAL
#       f and board distance Z are confounded -- a longer
#       lens further away fits identically. The residual
#       looks excellent and f is wrong. TILT THE BOARD.
#
#   AUTOFOCUS LEFT ON
#       the intrinsics differ between frames, so no single
#       K fits any of them. LOCK FOCUS AND EXPOSURE.
#
#   BOARD ONLY NEAR THE IMAGE CENTRE
#       distortion is unconstrained where it is largest,
#       so k1 is noise. FILL THE CORNERS."""),
  ("p", "<b>A low reprojection error does not mean a correct "
        "calibration.</b> It means the model fits the images you supplied, "
        "<b>which is CSCE 633 Module 03's overfitting wearing a "
        "geometric costume</b> — and the frontal-board degeneracy is "
        "the clearest case, because it produces an excellent residual and "
        "a focal length that may be wrong by tens of percent. <b>The "
        "remedy is the same as it was there: hold data out</b> (&sect;4), "
        "and check against something that is not the fit's own residual."),

  ("h1", "4 &nbsp; Checking a calibration"),
  ("ul", ["<b>Undistort an image of a known straight edge</b> — a "
          "door frame, a building, a taped line — and confirm it is "
          "straight in the undistorted image. <b>This catches a wrong "
          "k<sub>1</sub> instantly, takes two minutes, and almost nobody "
          "does it.</b>",
          "<b>Measure a known distance</b> by triangulating a pair of "
          "points from two calibrated views and comparing against a "
          "ruler. <b>This is the end-to-end check</b> and it tests the "
          "whole chain rather than one parameter.",
          "<b>Hold out five calibration images</b> and report the "
          "reprojection error on them without having fitted to them. "
          "<b>CSCE 633's train/test split, applied to geometry</b> "
          "— and a large train/held-out gap is exactly the "
          "degeneracy signal of &sect;3.",
          "<b>Sanity-check f against the hardware specification:</b> the "
          "lens's focal length in millimetres times the sensor's pixels "
          "per millimetre should land within a few percent of your "
          "estimate. <b>A factor-of-two disagreement usually means an "
          "image-resize bug</b> (&sect;2).",
          "<b>Recalibrate on a different day with fresh images</b> and "
          "compare the parameters. <b>Large disagreement indicates that "
          "the procedure is unstable rather than that the camera "
          "changed</b>, and the usual cause is insufficient orientation "
          "variety."]),
  ("callout", "Calibration drifts",
   ["<b>Thermal expansion changes the effective focal length "
    "measurably</b> over a camera's warm-up period, which is a matter of "
    "minutes — so a calibration captured cold does not describe the "
    "same camera an hour later, at precision that matters for metrology.",
    "<b>Mechanical shock moves the sensor relative to the lens</b>, "
    "changing the principal point and sometimes the distortion. <b>A "
    "dropped camera is silently decalibrated</b> and reports nothing "
    "about it.",
    "<b>So production systems either recalibrate continuously</b> "
    "— self-calibration from scene structure, which Module 05's "
    "bundle adjustment supports naturally — <b>or treat the "
    "intrinsics as slowly-varying unknowns</b> rather than constants.",
    "<b>Which is why Module 13 returns to this.</b> <b>A calibration is "
    "a measurement with a validity period, not a constant</b>, and "
    "systems built on the assumption that it is constant degrade "
    "invisibly — the geometry stays self-consistent and drifts away "
    "from the world, which is the hardest class of failure to notice."]),
 ],
 "resources": [
   ("Szeliski &mdash; Computer Vision, chapter 2 (free PDF)",
    "https://szeliski.org/Book/",
    "<b>Image formation, camera models, and distortion</b> — the "
    "reference for &sect;1 and &sect;2."),
   ("Zhang &mdash; A Flexible New Technique for Camera Calibration "
    "(free)",
    "https://www.microsoft.com/en-us/research/publication/a-flexible-new-technique-for-camera-calibration/",
    "<b>The method &sect;3 describes</b>, and what OpenCV implements. "
    "Short and worth reading in full."),
   ("OpenCV &mdash; camera calibration tutorial (free)",
    "https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html",
    "The working procedure, with code. Follow it once exactly before "
    "deviating."),
   ("Hartley & Zisserman &mdash; Multiple View Geometry, chapters 2–6",
    "https://www.robots.ox.ac.uk/~vgg/hzbook/",
    "<b>Projective geometry and camera models done properly</b>, "
    "including the duality of &sect;1's callout."),
 ],
 "exercises": [
   "<b>Implement the projection chain yourself</b> and verify it against "
   "OpenCV's <code>projectPoints</code> on random inputs.",
   "<b>Resize an image by half and confirm f halves</b> by recalibrating "
   "on the resized images.",
   "<b>Calibrate your own camera</b> with 20 varied images and report K "
   "and the reprojection error.",
   "<b>Deliberately calibrate with near-frontal boards only</b> and "
   "compare f against the good calibration. Report the error.",
   "<b>Calibrate with autofocus enabled</b> and report what happens to "
   "the residual.",
   "<b>Calibrate with the board only in the image centre</b> and compare "
   "k₁ against the good calibration.",
   "<b>Undistort a photograph of a straight edge</b> and measure the "
   "residual curvature in pixels.",
   "<b>Hold out five images</b> and report the error on them.",
   "<b>Triangulate a known distance</b> from two views and compare "
   "against a ruler measurement.",
   "<b>Recalibrate after warming the camera for twenty minutes</b> and "
   "report the change in f.",
 ],
 "selfcheck": [
   "Write the full projection chain and say which step loses "
   "information.",
   "Give three reasons homogeneous coordinates are used.",
   "What are the five intrinsic parameters, and which should be fixed?",
   "Why does focal length change when you resize an image?",
   "When does radial distortion matter and when can it be ignored?",
   "Describe the calibration procedure and name its three common "
   "failures.",
   "Why is a low reprojection error insufficient evidence?",
   "Give five independent checks on a calibration.",
 ],
},

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Features and Correspondence",
 "subtitle": "The problem everything geometric depends on.",
 "question": "How do you decide that this pixel and that pixel are the "
             "same world point?",
 "outcomes": [
     "Explain what makes a good feature point.",
     "Explain scale and rotation invariance and how it is achieved.",
     "Match descriptors and filter the matches.",
     "Apply RANSAC and choose its parameters.",
     "Explain why learned matchers improved on hand-designed ones.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "What to detect",
   "blurb": "Corners, because edges are not enough."},

  {"t": "callout", "title": "A good feature is one you can localise in two dimensions",
   "kind": "The aperture problem",
   "body": ["<b>A flat patch matches everywhere</b> — no information "
            "about position at all.",
            "<b>An edge patch matches anywhere along the edge</b> "
            "— one degree of freedom remains unresolved. <b>This is "
            "the aperture problem</b>, and it returns in Module 07 as the "
            "reason optical flow is under-determined.",
            "<b>A corner matches in one place.</b> Intensity varies in "
            "both directions, so both coordinates are determined.",
            "<b>Harris formalises this</b> as the eigenvalues of the "
            "local gradient covariance: <b>two large eigenvalues means a "
            "corner, one means an edge, none means flat</b> — and the "
            "response is a function of those eigenvalues."]},

  {"t": "code", "kicker": "Harris", "title": "The corner response, derived",
   "lang": "text", "code": """
  Consider shifting a window by (dx, dy). The intensity
  change, to first order, is

      E(dx,dy) = [dx dy] M [dx dy]^T

  where M is the GRADIENT COVARIANCE over the window:

      M = sum_w [ Ix*Ix   Ix*Iy ]
                [ Ix*Iy   Iy*Iy ]

  M's eigenvalues say how much the patch changes when moved
  in each of two principal directions:

      both small     -> flat, moves freely, USELESS
      one large      -> edge, one free direction, PARTIAL
      both large     -> corner, pinned in 2D, GOOD

  Harris avoids computing eigenvalues explicitly:

      R = det(M) - k * trace(M)^2,     k ~ 0.04-0.06

  which is large and positive only when both eigenvalues
  are large. Threshold R, then non-maximum suppress.

  NOTE THE STRUCTURE: a 2x2 covariance whose eigenvalues
  tell you how determined an estimate is. That is the
  condition number of Module 01 again, locally.
""",
   "caption": "<b>The same matrix appears in Module 07's optical "
              "flow</b>, where its conditioning decides whether flow is "
              "recoverable at a pixel — one idea, two uses.",
   "note": "Connecting Harris to Lucas-Kanade via the structure tensor is "
           "the insight that makes both memorable."},

  {"t": "section", "label": "Part 2", "title": "Invariance",
   "blurb": "The same point, detected from a different distance and "
            "angle."},

  {"t": "table", "kicker": "Invariance", "title": "What must be invariant, and how",
   "header": ["Nuisance", "Why it breaks naive matching", "The standard answer"],
   "widths": [2.5, 4.3, 5.2],
   "rows": [
     ["<b>Scale</b>", "<b>A corner at 2 m is a blur at 20 m</b>", "<b>Detect across a scale pyramid; keep the scale</b>"],
     ["<b>Rotation</b>", "Patch orientation changes with camera roll", "<b>Estimate a dominant orientation; rotate the patch</b>"],
     ["<b>Illumination</b>", "Brightness and contrast shift", "<b>Normalise the descriptor; use gradients not intensities</b>"],
     ["<b>Viewpoint</b>", "<b>Surfaces foreshorten — a circle becomes an ellipse</b>", "<b>Affine adaptation, or accept a limited range</b>"],
     ["<b>Occlusion</b>", "Part of the patch is a different surface", "<b>Nothing. This is why RANSAC exists</b>"],
   ],
   "footnote": "<b>Viewpoint invariance is the one nobody fully "
               "solves</b> — which is why wide-baseline matching "
               "remains hard and is where learned matchers won.",
   "note": "Being clear that viewpoint is the unsolved one sets up Part "
           "4."},

  {"t": "callout", "title": "A descriptor is a vector designed to be comparable",
   "kind": "How SIFT works, in four sentences",
   "body": ["<b>Take the patch at the detected scale, rotated to the "
            "detected orientation.</b> Scale and rotation are now "
            "removed.",
            "<b>Compute gradients, and histogram their orientations in a "
            "4×4 grid of spatial cells</b> with 8 orientation bins "
            "— 128 numbers.",
            "<b>Normalise the vector, clip large values, normalise "
            "again.</b> Contrast and brightness are now removed, and the "
            "clipping limits the damage from a single bright edge.",
            "<b>Compare by Euclidean distance.</b> <b>The design is "
            "entirely about making the comparison meaningful</b> — "
            "spatial histogramming buys tolerance to small localisation "
            "error, which is the single most important property."]},

  {"t": "section", "label": "Part 3", "title": "Matching and RANSAC",
   "blurb": "Most matches are wrong, and that is manageable."},

  {"t": "code", "kicker": "RANSAC", "title": "Fitting a model when half the data is garbage",
   "lang": "text", "code": """
  MATCHING gives you correspondences, maybe 40-70% correct.
  Least squares on that is worthless -- one gross outlier
  moves the fit arbitrarily.

  RANSAC:
    repeat N times:
        sample the MINIMUM set needed to fit the model
            (4 points for a homography, 5 for essential)
        fit the model to exactly those
        count how many of ALL correspondences agree
            within a threshold -- the INLIERS
    keep the model with the most inliers
    refit on all of its inliers

  HOW MANY ITERATIONS? For inlier fraction w, sample size s,
  and desired success probability p:

      N = log(1-p) / log(1 - w^s)

  w=0.5, s=4, p=0.99  ->  N = 72
  w=0.5, s=8, p=0.99  ->  N = 1177

  THE SAMPLE SIZE IS IN THE EXPONENT. That is why minimal
  solvers matter: the 5-point essential algorithm is not
  elegance, it is a 100x reduction in iterations over an
  8-point one.
""",
   "caption": "<b>The exponential dependence on sample size is the whole "
              "reason minimal solvers are a research area</b>, and it "
              "makes the trade immediately quantitative.",
   "note": "Students usually see RANSAC as a trick; the iteration formula "
           "makes it a design decision."},

  {"t": "callout", "title": "The three parameters that decide whether RANSAC works",
   "kind": "Getting it right",
   "body": ["<b>The threshold.</b> Too tight rejects true inliers and "
            "RANSAC finds nothing; too loose admits outliers and the "
            "refit is wrong. <b>Set it from your measured feature "
            "localisation error</b>, typically 1–3 pixels.",
            "<b>The iteration count.</b> Use the formula, and prefer "
            "<i>adaptive</i> RANSAC: recompute N from the best inlier "
            "fraction seen so far, which usually terminates far earlier.",
            "<b>The ratio test before RANSAC.</b> Keep a match only if "
            "the best descriptor distance is well below the second best "
            "— <b>typically 0.7–0.8</b>. <b>This single filter "
            "raises the inlier fraction enormously</b> and therefore cuts "
            "N exponentially.",
            "<b>And check the final inlier count, not just that it "
            "returned.</b> <b>RANSAC always returns something</b>, and a "
            "model supported by 12 of 800 matches is noise with a "
            "confident interface."]},

  {"t": "section", "label": "Part 4", "title": "Learned matching",
   "blurb": "Where the hand-designed pipeline was beaten."},

  {"t": "bullets", "kicker": "Learned", "title": "What learning changed, and what it did not",
   "items": [
     "<b>Learned descriptors</b> beat SIFT modestly — the "
     "hand-designed one was close to optimal for its patch size.",
     "",
     "<b>Learned <i>matchers</i> beat it decisively.</b> SuperGlue and "
     "its successors match the whole set jointly, using attention, "
     "rather than comparing pairs independently.",
     "",
     "<b>Because matching is a global assignment problem</b>, and "
     "nearest-neighbour-with-ratio-test treats it as many independent "
     "ones. <b>The joint formulation is the real contribution.</b>",
     "",
     "<b>Biggest gains at wide baselines and low texture</b> — "
     "exactly the cases Part 2's table could not fix.",
     "",
     "<b>And geometry is unchanged.</b> <b>RANSAC, the essential "
     "matrix, and bundle adjustment all still run on the output.</b>",
   ],
   "footnote": "<b>Learning replaced one stage of the pipeline, not the "
               "pipeline</b> — which is the realistic picture of "
               "learned geometric vision."},
 ],
 "takeaways": [
   "A good feature is localisable in both dimensions; edges leave one "
   "degree of freedom, which is the aperture problem that returns in "
   "optical flow.",
   "Harris uses the eigenvalues of the local gradient covariance, which is "
   "a local conditioning estimate and the same matrix as Lucas–Kanade "
   "uses.",
   "Scale, rotation, and illumination invariance have standard solutions; "
   "viewpoint invariance does not, which is where learned matchers won.",
   "RANSAC's iteration count depends exponentially on the sample size, "
   "which is why minimal solvers are a research area.",
   "The ratio test before RANSAC raises the inlier fraction and therefore "
   "cuts the iteration count exponentially — it is the cheapest "
   "available win.",
   "RANSAC always returns something, so the inlier count must be checked "
   "rather than assumed.",
 ],
 "notes": [
  ("h1", "1 &nbsp; What makes a good feature"),
  ("callout", "A good feature is one you can localise in two dimensions",
   ["<b>A flat patch matches everywhere</b> in a uniform region, giving no "
    "information about position at all. Nothing can be done with it.",
    "<b>An edge patch matches anywhere along the edge.</b> One degree of "
    "freedom is determined and one is not. <b>This is the aperture "
    "problem</b>, and it returns in Module 07 as the reason optical flow "
    "is under-determined at every pixel individually — the same "
    "geometry, in a different application.",
    "<b>A corner matches in exactly one place.</b> Intensity varies in "
    "both directions, so both image coordinates are pinned down, which is "
    "what correspondence requires.",
    "<b>Harris formalises this as the eigenvalues of the local gradient "
    "covariance matrix</b>: two large eigenvalues is a corner, one large "
    "is an edge, neither is a flat region — and the corner response "
    "is a cheap function of those eigenvalues that avoids computing them "
    "(&sect;1's code)."]),
  ("code", """Consider shifting a window by (dx, dy). To first order the
intensity change is

    E(dx,dy) = [dx dy] M [dx dy]^T

where M is the GRADIENT COVARIANCE (the structure tensor)
over the window:

    M = sum_w [ Ix*Ix   Ix*Iy ]
              [ Ix*Iy   Iy*Iy ]

M's eigenvalues say how much the patch changes when moved
along each of two principal directions:

    both small   -> flat region, moves freely:   USELESS
    one large    -> edge, one free direction:    PARTIAL
    both large   -> corner, pinned in 2D:        GOOD

Harris avoids an eigendecomposition:

    R = det(M) - k * trace(M)^2,    k about 0.04 to 0.06

which is large and positive only when both eigenvalues are
large. Threshold R, then apply non-maximum suppression.

NOTE THE STRUCTURE: a 2x2 covariance whose eigenvalues say
how well-determined a local estimate is. That is the
condition number of Module 01 section 2, computed locally."""),
  ("p", "<b>The same matrix appears in Module 07's Lucas–Kanade "
        "optical flow</b>, where its conditioning decides whether flow is "
        "recoverable at a given pixel at all — and the pixels where "
        "it is well-conditioned are precisely the corners Harris finds. "
        "<b>One idea with two uses, which is worth noticing because it "
        "means 'good feature to track' and 'good feature to match' are the "
        "same property</b>, and Shi and Tomasi's refinement of Harris was "
        "derived from exactly that observation."),

  ("h1", "2 &nbsp; Invariance"),
  ("table", ["Nuisance", "Why it breaks naive matching", "The standard answer"],
   [["<b>Scale</b>",
     "<b>A corner photographed at 2 metres is a smooth blur at 20 "
     "metres</b> — the patches are not comparable at all.",
     "<b>Detect across a scale pyramid and record the scale at which the "
     "response peaked</b>, then describe the patch at that scale. This is "
     "the core of SIFT's detector."],
    ["<b>Rotation</b>",
     "Patch orientation changes with camera roll, so a raw patch "
     "comparison fails.",
     "<b>Estimate a dominant gradient orientation and rotate the patch to "
     "a canonical frame</b> before describing it."],
    ["<b>Illumination</b>",
     "Brightness and contrast change between exposures and between times "
     "of day.",
     "<b>Describe gradients rather than intensities</b> (removing additive "
     "brightness) <b>and normalise the descriptor</b> (removing "
     "multiplicative contrast)."],
    ["<b>Viewpoint</b>",
     "<b>Surfaces foreshorten: a circular patch becomes an ellipse, and "
     "the mapping is not a similarity.</b>",
     "<b>Affine adaptation estimates the local shape, or you accept a "
     "limited viewpoint range.</b> <b>Nobody solves this fully</b>, which "
     "is why wide-baseline matching stayed hard and is precisely where "
     "&sect;4's learned matchers won."],
    ["<b>Occlusion</b>",
     "Part of the patch is a different surface entirely, so the "
     "descriptor is a blend of two things.",
     "<b>Nothing, at the descriptor level. This is why RANSAC "
     "exists</b> — some fraction of matches will simply be wrong and "
     "the pipeline must survive it (&sect;3)."]],
   [0.17, 0.39, 0.44]),
  ("callout", "A descriptor is a vector designed to be comparable",
   ["<b>Take the patch at the detected scale, rotated to the detected "
    "dominant orientation.</b> Scale and rotation have now been removed "
    "by construction rather than by the descriptor's own design.",
    "<b>Compute image gradients and histogram their orientations within "
    "a 4&times;4 grid of spatial cells, with 8 orientation bins per "
    "cell</b> — 128 numbers. <b>The spatial histogramming is the "
    "most important design decision</b>: it buys tolerance to small "
    "localisation errors, because a gradient that moves by a pixel lands "
    "in the same cell.",
    "<b>Normalise the vector, clip any component above 0.2, normalise "
    "again.</b> Contrast and brightness are removed by the "
    "normalisation, and <b>the clipping limits the damage a single very "
    "strong edge can do</b> to the whole descriptor.",
    "<b>Compare by Euclidean distance.</b> <b>Every element of the "
    "design exists to make that one comparison meaningful</b> — "
    "which is worth stating because it is the general principle behind "
    "descriptors, including the learned ones of &sect;4, whose training "
    "objective is exactly 'make the distance meaningful'."]),

  ("break",),
  ("h1", "3 &nbsp; Matching, and surviving the errors"),
  ("code", """MATCHING gives correspondences that are maybe 40-70%
correct. Least squares on that is worthless -- a single
gross outlier moves the fit arbitrarily far.

RANSAC:
  repeat N times:
      sample the MINIMUM set needed to fit the model
          (4 points for a homography, 5 for an essential
           matrix, 3 for a similarity)
      fit the model to exactly those points
      count how many of ALL correspondences agree with it
          within a threshold -- the INLIERS
  keep the model with the most inliers
  refit on all of that model's inliers

HOW MANY ITERATIONS? For inlier fraction w, sample size s,
and desired success probability p:

    N = log(1 - p) / log(1 - w^s)

    w=0.5, s=4, p=0.99   ->  N = 72
    w=0.5, s=5, p=0.99   ->  N = 145
    w=0.5, s=8, p=0.99   ->  N = 1177
    w=0.3, s=8, p=0.99   ->  N = 70188

THE SAMPLE SIZE IS IN THE EXPONENT, and so is the inlier
fraction. That is why minimal solvers matter: the 5-point
essential algorithm is not elegance for its own sake, it
is an order-of-magnitude reduction in iterations over an
8-point one -- and why the ratio test, which raises w,
pays off exponentially."""),
  ("callout", "The three parameters that decide whether RANSAC works",
   ["<b>The inlier threshold.</b> Too tight and true inliers are "
    "rejected, so no model gathers support and RANSAC reports nothing; "
    "too loose and outliers are admitted, so the final refit is wrong "
    "while the inlier count looks healthy. <b>Set it from your measured "
    "feature localisation error</b> — typically 1 to 3 pixels, and "
    "measurable by matching an image against itself under a known "
    "transform.",
    "<b>The iteration count.</b> Use the formula, and prefer <i>adaptive "
    "RANSAC</i>: recompute N from the best inlier fraction observed so "
    "far, which terminates far earlier than a fixed conservative N when "
    "the data is good.",
    "<b>The ratio test, applied before RANSAC.</b> Keep a match only if "
    "the nearest descriptor distance is well below the second nearest "
    "— <b>a ratio under about 0.7 to 0.8</b>. <b>This single filter "
    "raises the inlier fraction w substantially, and since w appears in "
    "the exponent, it cuts N by orders of magnitude.</b> It is the "
    "cheapest available improvement in the whole pipeline.",
    "<b>And check the final inlier count rather than merely that it "
    "returned a model.</b> <b>RANSAC always returns something</b> "
    "— it reports the best-supported sample, however poorly "
    "supported — and <b>a model supported by 12 of 800 matches is "
    "noise presented through a confident interface</b>, which is exactly "
    "the kind of failure that propagates silently into Module 05's "
    "reconstruction."]),

  ("h1", "4 &nbsp; Learned matching"),
  ("ul", ["<b>Learned descriptors beat SIFT, but only modestly.</b> This "
          "is a genuinely interesting result: <b>the hand-designed "
          "descriptor turned out to be close to optimal for its patch "
          "size and task</b>, and twenty years of design were not easily "
          "improved by gradient descent.",
          "<b>Learned <i>matchers</i> beat the pipeline decisively.</b> "
          "SuperGlue and its successors take the full set of features "
          "from both images and match them <i>jointly</i>, using "
          "attention (CSCE 636 Module 06) over both sets plus an "
          "optimal-transport assignment layer.",
          "<b>Because matching is a global assignment problem and "
          "nearest-neighbour-with-ratio-test treats it as many "
          "independent local ones.</b> <b>The joint formulation is the "
          "real contribution</b>, not the learning as such — a "
          "point that becomes clear when you notice the assignment layer "
          "is a classical algorithm (CSCE 669 Module 11's matching).",
          "<b>The gains are largest at wide baselines and on low-texture "
          "surfaces</b> — precisely the cases &sect;2's table "
          "identified as unsolved. <b>Learning attacked the exact "
          "residual weakness</b>, which is the pattern worth looking for "
          "when deciding where learning will help.",
          "<b>And the geometry is entirely unchanged.</b> <b>RANSAC, the "
          "essential matrix, triangulation, and bundle adjustment all "
          "still run on the matcher's output</b>, exactly as before. "
          "<b>Learning replaced one stage of the pipeline, not the "
          "pipeline</b> — which is the realistic picture of learned "
          "geometric vision and a useful corrective to the impression "
          "that deep learning displaced it."]),
 ],
 "resources": [
   ("Szeliski &mdash; Computer Vision, chapter 7 (free PDF)",
    "https://szeliski.org/Book/",
    "<b>Feature detection, description, and matching</b> — the "
    "reference for &sect;1 through &sect;3."),
   ("Lowe &mdash; Distinctive Image Features from Scale-Invariant "
    "Keypoints (free)",
    "https://www.cs.ubc.ca/~lowe/papers/ijcv04.pdf",
    "<b>SIFT, in the author's own words.</b> The ratio test of &sect;3 is "
    "introduced here, with the distance distributions that justify it."),
   ("Fischler & Bolles &mdash; Random Sample Consensus (free)",
    "https://dl.acm.org/doi/10.1145/358669.358692",
    "<b>The original RANSAC paper</b>, including the iteration-count "
    "derivation of &sect;3."),
   ("Sarlin et al. &mdash; SuperGlue (free)",
    "https://arxiv.org/abs/1911.11763",
    "<b>The &sect;4 result.</b> The attention-plus-assignment "
    "architecture, and the wide-baseline evaluation."),
 ],
 "exercises": [
   "<b>Implement Harris from the structure tensor</b> and visualise the "
   "two eigenvalues as a colour image.",
   "<b>Confirm that edges have one large eigenvalue</b> and corners two, "
   "by inspecting known regions.",
   "<b>Detect features across a scale pyramid</b> and verify the same "
   "world point is found at the right scale from two distances.",
   "<b>Implement a SIFT-like descriptor</b> and match two images of the "
   "same scene.",
   "<b>Measure the inlier fraction with and without the ratio test</b>, "
   "at ratios 0.6, 0.7, 0.8, and 0.9.",
   "<b>Compute the required RANSAC iterations for each</b> and report the "
   "ratio.",
   "<b>Implement RANSAC for a homography</b> and plot inlier count "
   "against threshold.",
   "<b>Run RANSAC on deliberately bad matches</b> (random pairs) and "
   "report what it returns.",
   "<b>Match a wide-baseline pair with SIFT and with a learned "
   "matcher</b> and compare inlier counts.",
   "<b>Find a pair where SIFT fails completely</b> and explain which "
   "invariance broke.",
 ],
 "selfcheck": [
   "What makes a feature localisable, and what is the aperture problem?",
   "Derive the Harris response from the structure tensor.",
   "Where else does the structure tensor appear in this course?",
   "Name five nuisances and the standard answer to each.",
   "Which invariance is unsolved, and what follows from that?",
   "Describe SIFT's descriptor and say what each design step buys.",
   "State RANSAC's iteration formula and explain why minimal solvers "
   "matter.",
   "Name RANSAC's three parameters and how to set each.",
   "What did learned matching change, and what did it leave alone?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Two-View Geometry",
 "subtitle": "What two pictures determine.",
 "question": "Given two images of a scene, what can be recovered "
             "exactly?",
 "outcomes": [
     "Derive the epipolar constraint.",
     "Distinguish the fundamental and essential matrices.",
     "Recover relative pose and triangulate.",
     "Explain the homography and when it applies instead.",
     "Diagnose the degenerate configurations.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The epipolar constraint",
   "blurb": "A point in one image restricts its match to a line in the "
            "other."},

  {"t": "callout", "title": "Two cameras and a world point are coplanar, and that is the whole constraint",
   "kind": "The derivation in four lines",
   "body": ["<b>The two camera centres and the world point define a "
            "plane</b> — the epipolar plane. Both image rays lie in "
            "it.",
            "<b>So the three vectors are coplanar</b>, and coplanarity of "
            "three vectors is a vanishing triple product: x′ · "
            "(t × R x) = 0.",
            "<b>Write that as x′ᵀ E x = 0 with E = [t]ₓ R.</b> "
            "That is the essential matrix, and it is just the triple "
            "product rearranged.",
            "<b>The consequence is the useful part:</b> <b>a point in one "
            "image constrains its match to a <i>line</i> in the "
            "other</b> — a one-dimensional search instead of "
            "two-dimensional. That is what makes dense stereo feasible "
            "(Module 06)."]},

  {"t": "table", "kicker": "Matrices", "title": "Fundamental against essential",
   "header": ["", "Fundamental F", "Essential E"],
   "widths": [2.3, 4.6, 5.1],
   "rows": [
     ["<b>Works in</b>", "<b>Pixel coordinates</b>", "<b>Calibrated (normalised) coordinates</b>"],
     ["<b>Needs</b>", "<b>Nothing — no calibration</b>", "<b>Known intrinsics K</b>"],
     ["<b>Relation</b>", "F = K'^-T E K^-1", "E = K'^T F K"],
     ["<b>DoF</b>", "<b>7 (rank 2, scale-free)</b>", "<b>5 (rank 2, two equal singular values)</b>"],
     ["<b>Min points</b>", "7", "<b>5 — and RANSAC cares (M03)</b>"],
     ["<b>Yields</b>", "Epipolar lines only", "<b>Epipolar lines AND relative pose</b>"],
   ],
   "footnote": "<b>Calibration is what converts epipolar geometry into "
               "metric pose</b> — which is the concrete payoff for "
               "Module 02's work.",
   "note": "The DoF count explains the minimal-solver sizes, which "
           "students otherwise memorise."},

  {"t": "section", "label": "Part 2", "title": "Pose and triangulation",
   "blurb": "From E to geometry."},

  {"t": "code", "kicker": "Decomposition", "title": "E to pose, and the four-way ambiguity",
   "lang": "text", "code": """
  SVD of E gives FOUR candidate (R, t) pairs:
      two rotations, and t up to sign.

  Only ONE puts the triangulated points IN FRONT of both
  cameras. The other three place points behind one or both,
  which is physically impossible.

  SO: triangulate one correspondence under each candidate
  and pick the one with positive depth in both views. This
  is the CHEIRALITY check, and it is two lines of code.

  AND t HAS NO SCALE. |t| = 1 by construction, because
  Module 01's scale ambiguity is a theorem. Your
  reconstruction is metric in SHAPE and arbitrary in SIZE.

  TRIANGULATION: given two rays that should meet but do not
  (noise), find the 3D point minimising REPROJECTION ERROR
  in both images -- NOT the midpoint of the closest
  approach between the rays, which is the intuitive answer
  and is biased. The reprojection formulation is the one
  that is statistically correct under image-plane noise.
""",
   "caption": "<b>Minimise error where the noise is</b> — in the "
              "image, not in the world. The same principle governs bundle "
              "adjustment in Module 05.",
   "note": "The midpoint-vs-reprojection distinction is a real and common "
           "error."},

  {"t": "section", "label": "Part 3", "title": "Homographies",
   "blurb": "When the scene is a plane, or the camera only rotates."},

  {"t": "callout", "title": "A homography applies in exactly two situations",
   "kind": "And both matter",
   "body": ["<b>The scene is planar.</b> All points lie on one plane, so "
            "the image-to-image map is a projective transform of that "
            "plane — 8 degrees of freedom, 4 point pairs.",
            "<b>Or the camera only rotates</b>, with no translation. "
            "Then depth is irrelevant to the mapping and any scene maps "
            "by a homography. <b>This is why panorama stitching "
            "works.</b>",
            "<b>Both cases are degenerate for the essential matrix</b> "
            "— which is Part 4's subject and the most common failure "
            "in practice.",
            "<b>So estimate both models and compare their inlier "
            "counts.</b> <b>If the homography explains the data as well "
            "as the essential matrix, you are in a degenerate "
            "configuration</b> and must not trust the pose. That test is "
            "cheap and almost nobody runs it."]},

  {"t": "section", "label": "Part 4", "title": "Degeneracies",
   "blurb": "When two views determine nothing."},

  {"t": "bullets", "kicker": "Degeneracies", "title": "The configurations that break two-view geometry",
   "items": [
     "<b>Pure rotation.</b> <b>No baseline means no triangulation, and "
     "E is undefined</b> — t is zero. Symptom: a plausible pose, "
     "wild depths. <b>The most common real failure.</b>",
     "",
     "<b>All points coplanar.</b> F is not uniquely determined by a "
     "plane; the 8-point algorithm returns noise. <b>Use the "
     "homography.</b>",
     "",
     "<b>Very small baseline relative to depth.</b> Not degenerate, but "
     "badly conditioned — Module 01's stability failure. "
     "<b>Depth error scales as depth² / baseline.</b>",
     "",
     "<b>Repeated structure.</b> Matching is confidently wrong, and "
     "RANSAC finds a consistent incorrect model. <b>Brick walls and "
     "office carpets.</b>",
     "",
     "<b>All points at great distance.</b> Translation becomes "
     "unobservable; the configuration approaches pure rotation.",
   ],
   "footnote": "<b>Every one of these returns a confident answer</b>, "
               "which is why the homography comparison and a conditioning "
               "check are mandatory rather than optional."},

  {"t": "callout", "title": "Depth error grows with the square of depth",
   "kind": "The number to remember",
   "body": ["<b>For a stereo pair with baseline b, focal length f in "
            "pixels, and disparity error δd, the depth error "
            "is</b> δZ ≈ Z² · δd / (f · b).",
            "<b>So doubling the distance quadruples the error.</b> A rig "
            "accurate to a centimetre at 2 m is accurate to 25 cm at "
            "10 m.",
            "<b>And the only levers are baseline and focal length</b>, "
            "both linear. <b>Widening the baseline improves depth and "
            "worsens matching</b>, which is the fundamental stereo trade "
            "(Module 06).",
            "<b>Compute this number for your rig before building "
            "anything on it.</b> <b>It decides whether the system is "
            "possible</b>, and it takes one line."]},
 ],
 "takeaways": [
   "The epipolar constraint is coplanarity of two rays and the baseline, "
   "written as a vanishing triple product.",
   "It reduces correspondence search from two dimensions to one, which is "
   "what makes dense stereo feasible.",
   "The fundamental matrix needs no calibration and yields only epipolar "
   "lines; the essential matrix needs intrinsics and yields relative "
   "pose.",
   "E decomposes to four candidate poses and the cheirality check selects "
   "the one with points in front of both cameras.",
   "Triangulate by minimising reprojection error, not by taking the "
   "midpoint of closest approach, which is biased.",
   "Depth error grows as the square of depth, so a rig's useful range is "
   "computable in one line before anything is built.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The epipolar constraint"),
  ("callout", "Two cameras and a world point are coplanar, and that is the "
              "whole constraint",
   ["<b>The two camera centres and the world point define a plane</b> "
    "— the epipolar plane — and both image rays, being rays "
    "from those centres to that point, lie within it.",
    "<b>So three vectors are coplanar: the ray in the first camera, the "
    "ray in the second, and the baseline between the centres.</b> "
    "Coplanarity of three vectors is precisely the vanishing of their "
    "triple product, so the constraint is x&prime; &middot; (t &times; "
    "R x) = 0.",
    "<b>Rewriting the triple product as a matrix gives x&prime;<super>T</super> "
    "E x = 0 with E = [t]<sub>&times;</sub> R</b>, where "
    "[t]<sub>&times;</sub> is the skew matrix representing the cross "
    "product. <b>The essential matrix is the triple product "
    "rearranged</b>, and seeing it that way removes most of its "
    "mystery.",
    "<b>The consequence is the useful part.</b> <b>A point in one image "
    "constrains its match to a <i>line</i> in the other</b> — the "
    "epipolar line, the projection of the first ray into the second "
    "image. <b>Correspondence search drops from two dimensions to "
    "one</b>, which is exactly what makes dense stereo computationally "
    "feasible (Module 06) and what makes sparse matching far more "
    "reliable once an initial pose is known."]),
  ("table", ["", "Fundamental matrix F", "Essential matrix E"],
   [["<b>Operates on</b>", "<b>Raw pixel coordinates.</b>",
     "<b>Calibrated (normalised) image coordinates</b> — pixels "
     "premultiplied by K<super>&minus;1</super>."],
    ["<b>Requires</b>", "<b>Nothing. No calibration at all.</b>",
     "<b>Known intrinsics</b> (Module 02)."],
    ["<b>Relation</b>", "F = K&prime;<super>&minus;T</super> E "
     "K<super>&minus;1</super>",
     "E = K&prime;<super>T</super> F K"],
    ["<b>Degrees of freedom</b>",
     "<b>7</b> — a 3&times;3 matrix, less one for overall scale and "
     "one for the rank-2 constraint.",
     "<b>5</b> — three for rotation, two for translation direction. "
     "Equivalently rank 2 with two equal singular values."],
    ["<b>Minimum points</b>", "7 (or 8 for the linear algorithm)",
     "<b>5 — and RANSAC cares a great deal</b>, since the sample "
     "size sits in the exponent (Module 03 &sect;3)."],
    ["<b>What you get</b>", "Epipolar lines only.",
     "<b>Epipolar lines AND the relative pose</b>, up to scale "
     "(&sect;2)."]],
   [0.19, 0.37, 0.44]),
  ("p", "<b>Calibration is what converts epipolar geometry into metric "
        "pose</b>, which is the concrete payoff for Module 02's "
        "care — and the reason an uncalibrated pipeline can stitch "
        "images but cannot measure the scene."),

  ("h1", "2 &nbsp; Pose and triangulation"),
  ("code", """SVD of E gives FOUR candidate (R, t) pairs: two possible
rotations, and t up to sign.

Only ONE of the four puts the triangulated points IN FRONT
of both cameras. The other three place points behind one or
both, which is physically impossible.

SO: triangulate one correspondence under each candidate and
keep the one with positive depth in both views. This is the
CHEIRALITY check, and it is two lines of code.

AND t CARRIES NO SCALE. |t| = 1 by construction, because
Module 01's scale ambiguity is a theorem rather than a
software limitation. Your reconstruction is correct in
SHAPE and arbitrary in SIZE.

TRIANGULATION: two rays that should meet do not, because of
noise. Find the 3D point minimising REPROJECTION ERROR in
both images -- NOT the midpoint of the rays' closest
approach, which is the intuitive answer and is biased.

The noise is in the image plane, not in the world, so the
objective belongs in the image plane. The midpoint method
weights a distant point's angular error the same as a near
one's, which is wrong by a factor of the depth."""),
  ("p", "<b>Minimise error where the noise actually is.</b> That single "
        "principle explains the triangulation choice, and <b>it governs "
        "bundle adjustment in Module 05</b> and the loss function of "
        "Module 11's neural reconstruction as well — all three "
        "minimise image-plane residuals rather than world-space ones, for "
        "the same reason."),

  ("break",),
  ("h1", "3 &nbsp; Homographies"),
  ("callout", "A homography applies in exactly two situations",
   ["<b>The scene is planar.</b> If every point lies on a single plane, "
    "the map from one image to the other is a projective transformation of "
    "that plane — 8 degrees of freedom, determined by 4 point "
    "correspondences. Facades, floors, tabletops, documents, and "
    "whiteboards all qualify.",
    "<b>Or the camera rotates about its centre without translating.</b> "
    "Then depth plays no part in the mapping, because the two rays to any "
    "world point differ only by a rotation, and <b>any scene whatsoever "
    "maps by a homography</b>. <b>This is exactly why panorama stitching "
    "works</b> and why it fails if you walk while shooting.",
    "<b>Both cases are degenerate for the essential matrix</b> "
    "— &sect;4's subject, and the most common failure in practice "
    "rather than a theoretical curiosity.",
    "<b>So estimate both models and compare their inlier counts.</b> "
    "<b>If a homography explains the correspondences as well as the "
    "essential matrix does, you are in a degenerate or near-degenerate "
    "configuration and must not trust the recovered pose.</b> <b>That "
    "test costs one extra RANSAC run and almost nobody performs it</b> "
    "— it is the single highest-value check in a two-view "
    "pipeline."]),

  ("h1", "4 &nbsp; Degeneracies"),
  ("ul", ["<b>Pure rotation.</b> <b>No baseline means no triangulation "
          "is possible and E is undefined</b>, because t is zero and "
          "[t]<sub>&times;</sub> vanishes. <b>The symptom is a plausible "
          "rotation with wild, unstable depths</b> — and it is the "
          "most common real failure, because a person photographing a "
          "scene from one spot while turning produces exactly this.",
          "<b>All points coplanar.</b> A plane does not determine F "
          "uniquely, so the 8-point algorithm returns an arbitrary member "
          "of a family — noise with a confident interface. <b>Use "
          "the homography instead</b>, which is well-determined here.",
          "<b>Very small baseline relative to scene depth.</b> Not "
          "strictly degenerate but badly conditioned, which is Module 01 "
          "&sect;2's stability failure in its most practical form. "
          "<b>The depth error scales as depth squared over baseline</b> "
          "(see below).",
          "<b>Repeated structure.</b> Brick walls, office carpet, "
          "railings, windows. <b>Matching is confidently wrong at a "
          "consistent offset, so RANSAC finds a large, coherent, "
          "incorrect inlier set</b> — which defeats the usual "
          "defence entirely, because the outliers agree with each other.",
          "<b>All points at great distance.</b> Translation becomes "
          "unobservable as depth grows, so the configuration tends toward "
          "the pure-rotation case continuously rather than abruptly.",
          "<b>Every one of these returns a confident answer.</b> <b>Which "
          "is why the homography comparison of &sect;3 and a conditioning "
          "check on the estimate are mandatory</b> rather than "
          "refinements — nothing else distinguishes a good estimate "
          "from a degenerate one."]),
  ("eq", "&delta;Z &nbsp;&asymp;&nbsp; Z&#178; &middot; &delta;d / "
         "(f &middot; b)"),
  ("callout", "Depth error grows with the square of depth",
   ["<b>For a stereo pair with baseline b, focal length f in pixels, and "
    "disparity measurement error &delta;d, the resulting depth error is "
    "approximately Z&#178;&delta;d/(fb).</b> The derivation is one line "
    "from Z = fb/d.",
    "<b>So doubling the distance quadruples the error.</b> A rig accurate "
    "to one centimetre at 2 metres is accurate to about 25 centimetres at "
    "10 metres — which is frequently the difference between a system "
    "that works and one that does not, and it is usually discovered after "
    "the hardware is built.",
    "<b>The only levers are baseline and focal length, and both are "
    "linear.</b> <b>Widening the baseline improves depth precision and "
    "worsens matching</b>, because the viewpoint change grows and "
    "Module 03's unsolved viewpoint invariance starts to bite. <b>That "
    "is the fundamental stereo trade</b> and Module 06 returns to it.",
    "<b>Compute this number for your configuration before building "
    "anything on it.</b> <b>It decides whether the system is possible at "
    "all</b>, it takes one line, and it is the most useful single "
    "calculation in this module."]),
 ],
 "resources": [
   ("Hartley & Zisserman &mdash; Multiple View Geometry, chapters 9–12",
    "https://www.robots.ox.ac.uk/~vgg/hzbook/",
    "<b>The definitive treatment of this module.</b> Epipolar geometry, "
    "F and E, triangulation, and the degeneracies of &sect;4."),
   ("Nistér &mdash; An Efficient Solution to the Five-Point "
    "Relative Pose Problem (free)",
    "https://ieeexplore.ieee.org/document/1288525",
    "<b>The 5-point solver of &sect;1's table</b>, and why the sample "
    "size matters so much."),
   ("Szeliski &mdash; Computer Vision, chapter 11 (free PDF)",
    "https://szeliski.org/Book/",
    "A gentler path through the same material, with the practical "
    "pipeline."),
   ("Hartley &mdash; In Defense of the Eight-Point Algorithm (free)",
    "https://ieeexplore.ieee.org/document/601246",
    "<b>Why normalisation of coordinates matters so much</b> — "
    "CSCE 620's and CSCE 669's conditioning lesson, in this exact "
    "setting."),
 ],
 "exercises": [
   "<b>Derive the epipolar constraint from the triple product</b> and "
   "write E in terms of R and t.",
   "<b>Implement the 8-point algorithm</b> with and without coordinate "
   "normalisation, and compare the errors.",
   "<b>Draw epipolar lines</b> on a real image pair and verify matches "
   "lie on them.",
   "<b>Decompose E and implement the cheirality check</b>, reporting how "
   "many points pass under each of the four candidates.",
   "<b>Triangulate by midpoint and by reprojection minimisation</b> and "
   "compare the bias on synthetic data with known ground truth.",
   "<b>Photograph a scene by pure rotation</b> and run essential matrix "
   "estimation. Report the depths you get.",
   "<b>Estimate a homography on the same pair</b> and compare the inlier "
   "counts. Confirm the degeneracy test fires.",
   "<b>Photograph a planar facade</b> and show the 8-point algorithm "
   "returns garbage.",
   "<b>Compute the depth error formula for your own rig</b> at 1, 5, and "
   "20 metres.",
   "<b>Verify it empirically</b> by triangulating objects at measured "
   "distances.",
 ],
 "selfcheck": [
   "Derive the epipolar constraint in four lines.",
   "Why does it reduce search from two dimensions to one?",
   "Compare F and E on five axes.",
   "Why does E have five degrees of freedom?",
   "Describe the four-way decomposition and the cheirality check.",
   "Why triangulate by reprojection error rather than by midpoint?",
   "Name the two situations where a homography applies.",
   "Name five degeneracies and the symptom of each.",
   "State the depth error formula and its practical consequence.",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Structure from Motion",
 "subtitle": "Many views, one global solution.",
 "question": "How do you reconstruct a scene from a hundred photographs?",
 "outcomes": [
     "Explain the structure-from-motion pipeline end to end.",
     "Explain bundle adjustment and why it is sparse.",
     "Explain drift and loop closure.",
     "Distinguish incremental from global approaches.",
     "Diagnose a reconstruction that has failed.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The pipeline",
   "blurb": "From unordered photographs to poses and points."},

  {"t": "code", "kicker": "Pipeline", "title": "Incremental structure from motion",
   "lang": "text", "code": """
  1. FEATURES in every image             (Module 03)
  2. MATCH candidate image pairs
         -- all pairs is O(n^2); use vocabulary trees or
            image retrieval to shortlist
  3. GEOMETRIC VERIFICATION per pair     (Module 04)
         -- RANSAC an essential matrix; a pair survives
            only if it has enough inliers
  4. TRACKS: chain pairwise matches into multi-view
         observations of the same world point
  5. SEED: pick the best-conditioned pair -- wide baseline,
         many inliers, NOT near-planar -- and reconstruct it
  6. LOOP:
         register a new image by PnP against known points
         triangulate newly visible points
         BUNDLE ADJUST                   (Part 2)
         remove points with large residuals
  7. FINAL global bundle adjustment

  THE SEED CHOICE MATTERS MORE THAN ANYTHING ELSE. A
  near-degenerate seed pair (Module 04 Part 4) poisons
  everything built on it, and the symptom appears fifty
  images later.
""",
   "caption": "<b>Step 3 is what makes it robust:</b> a pair that cannot "
              "be geometrically verified is discarded before it can "
              "contaminate the reconstruction.",
   "note": "The seed-choice warning is the single most useful practical "
           "point in the module."},

  {"t": "callout", "title": "PnP: pose from known points",
   "kind": "The registration step",
   "body": ["<b>Once some world points are known, a new image's pose "
            "follows from its 2D observations of them</b> — the "
            "perspective-n-point problem.",
            "<b>Three points give up to four solutions; four or more "
            "resolve it.</b> So P3P inside RANSAC is the standard, with "
            "the small sample size paying off exponentially "
            "(Module 03 §3).",
            "<b>This is how each new image joins</b>, and it is why "
            "incremental reconstruction grows rather than solving "
            "everything at once.",
            "<b>And it is the core of camera tracking</b> — a "
            "running AR or SLAM system is doing PnP against a map, every "
            "frame, at 60 Hz."]},

  {"t": "section", "label": "Part 2", "title": "Bundle adjustment",
   "blurb": "The global refinement, and why it is tractable."},

  {"t": "eq", "kicker": "Bundle adjustment", "title": "One objective over everything",
   "eqs": [
     ("minimise  Σᵢⱼ ‖ π(Cᵢ, Xⱼ) − xᵢⱼ ‖²",
      "Over all camera parameters Cᵢ and all world points Xⱼ, "
      "summed over every observation."),
     ("Thousands of cameras, millions of points",
      "Millions of unknowns — and it is solved routinely, in "
      "seconds to minutes."),
     ("Because the Jacobian is extremely SPARSE",
      "Camera i's residuals do not involve point j unless i observed "
      "j, and most cameras see a tiny fraction of points."),
   ],
   "caption": "<b>Exploiting the sparsity is what makes bundle adjustment "
              "possible</b> — the Schur complement eliminates the "
              "points block and leaves a small dense camera system.",
   "note": "The sparsity structure is the whole engineering content."},

  {"t": "callout", "title": "What bundle adjustment needs to work",
   "kind": "Practical requirements",
   "body": ["<b>A good initialisation.</b> It is a non-convex "
            "least-squares problem (CSCE 669 M01) and converges to a "
            "local minimum — which is why the incremental pipeline "
            "exists at all.",
            "<b>A robust loss.</b> Plain squared error lets one "
            "mismatched point dominate; Huber or Cauchy bounds each "
            "residual's influence. <b>This is not optional.</b>",
            "<b>Gauge fixing.</b> The solution is free up to a global "
            "similarity (Module 01's scale, plus rotation and "
            "translation) — <b>fix one camera and one distance, or "
            "the system is singular.</b>",
            "<b>And Levenberg–Marquardt, not plain "
            "Gauss–Newton</b> — the damping term is what keeps it "
            "stable when the Jacobian is near-singular, which it "
            "frequently is."]},

  {"t": "section", "label": "Part 3", "title": "Drift and loop closure",
   "blurb": "Why a long sequence bends."},

  {"t": "callout", "title": "Drift is accumulated error with no reference",
   "kind": "The sequential problem",
   "body": ["<b>Each frame's pose is estimated relative to the "
            "previous</b>, so errors compound — a 0.1° "
            "per-frame rotation error becomes 36° over 360 "
            "frames.",
            "<b>The reconstruction is locally excellent and globally "
            "bent.</b> A corridor that is straight comes out curved; a "
            "closed loop does not close.",
            "<b>Loop closure fixes it:</b> recognise that the current "
            "frame sees a previously-mapped place, add that constraint, "
            "and redistribute the accumulated error over the whole "
            "trajectory.",
            "<b>Place recognition is therefore essential, not a "
            "feature</b> — and it is an image-retrieval problem "
            "(CSCE 670's subject), which is why bag-of-words and learned "
            "global descriptors appear inside SLAM systems."]},

  {"t": "table", "kicker": "Approaches", "title": "Incremental against global",
   "header": ["", "Incremental", "Global"],
   "widths": [2.3, 4.6, 5.1],
   "rows": [
     ["<b>Method</b>", "<b>Add one image at a time, bundle adjust often</b>", "<b>Solve all rotations, then all translations, then refine</b>"],
     ["<b>Robustness</b>", "<b>High — bad images are rejected on entry</b>", "Lower — one bad constraint affects everything"],
     ["<b>Cost</b>", "<b>O(n⁴) in the worst case — repeated BA</b>", "<b>Much cheaper on large sets</b>"],
     ["<b>Drift</b>", "Accumulates; needs loop closure", "<b>Less, by construction</b>"],
     ["<b>Used by</b>", "<b>COLMAP, most SLAM front ends</b>", "<b>Large internet-scale reconstruction</b>"],
   ],
   "footnote": "<b>Incremental wins on robustness and loses on scale</b>, "
               "which is why production systems are hybrid — global "
               "rotations, then incremental refinement.",
   "note": "The hybrid answer is what the field actually settled on."},

  {"t": "section", "label": "Part 4", "title": "Diagnosis",
   "blurb": "Reading a failed reconstruction."},

  {"t": "bullets", "kicker": "Diagnosis", "title": "Symptoms and their causes",
   "items": [
     "<b>Reconstruction splits into disconnected components.</b> Not "
     "enough matched pairs bridging them — capture transition "
     "images.",
     "",
     "<b>Everything collapses to a plane or a point.</b> Degenerate "
     "seed pair, or a genuinely planar scene (Module 04 §4).",
     "",
     "<b>A corridor comes out curved.</b> Drift. Needs loop closure or "
     "more overlap.",
     "",
     "<b>High residuals concentrated on one object.</b> It moved. "
     "<b>Structure from motion assumes a static scene</b> and will "
     "silently distort to accommodate a moving one.",
     "",
     "<b>Duplicated structure — two copies of one wall.</b> "
     "<b>Repeated texture fooled place recognition.</b> The hardest "
     "failure to fix.",
   ],
   "footnote": "<b>Always render the point cloud from a novel viewpoint "
               "and compare against a photograph.</b> Residual numbers do "
               "not reveal a doubled wall; a picture does."},
 ],
 "takeaways": [
   "The pipeline is features, pairwise matching, geometric verification, "
   "tracks, a seed pair, then incremental registration with repeated bundle "
   "adjustment.",
   "The seed pair choice matters more than anything else, and a degenerate "
   "seed poisons everything built on it.",
   "Bundle adjustment minimises reprojection error over all cameras and "
   "points at once, and is tractable only because the Jacobian is sparse.",
   "It needs a good initialisation, a robust loss, gauge fixing, and "
   "Levenberg–Marquardt damping — none of which is optional.",
   "Drift is accumulated relative error, fixed by loop closure, which makes "
   "place recognition essential rather than a feature.",
   "Structure from motion assumes a static scene and silently distorts to "
   "accommodate a moving object.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The pipeline"),
  ("code", """1. FEATURES in every image                   (Module 03)

2. MATCH candidate image pairs
     all pairs is O(n^2) and prohibitive past a few
     hundred images -- use a vocabulary tree or a learned
     global descriptor to shortlist candidates

3. GEOMETRIC VERIFICATION per pair           (Module 04)
     RANSAC an essential matrix; a pair is retained only
     if it has enough geometrically consistent inliers

4. TRACKS: chain pairwise matches into multi-view
     observations of a single world point

5. SEED: choose the best-conditioned pair -- wide baseline,
     many inliers, NOT near-planar, homography test passed
     -- and reconstruct it

6. LOOP, until no image can be added:
     register a new image by PnP against known points
     triangulate newly visible points
     BUNDLE ADJUST                           (section 2)
     remove points with large residuals

7. FINAL global bundle adjustment

THE SEED CHOICE MATTERS MORE THAN ANYTHING ELSE. A
near-degenerate seed pair (Module 04 section 4) poisons
every pose built on it, and the symptom shows up fifty
images later as a reconstruction that will not converge."""),
  ("p", "<b>Step 3 is what makes the whole thing robust.</b> A pair whose "
        "matches cannot be explained by a single rigid geometry is "
        "discarded before it can contaminate anything — <b>and it is "
        "the reason structure from motion works at all on internet "
        "photographs</b>, where a large fraction of candidate pairs are "
        "simply unrelated images that happened to share visual words."),
  ("callout", "PnP: pose from known points",
   ["<b>Once some world points are known, a new image's pose is "
    "determined by its 2D observations of them</b> — the "
    "perspective-n-point problem, which is the inverse of Module 02's "
    "projection with the points known and the camera unknown.",
    "<b>Three points give up to four solutions and a fourth resolves "
    "the ambiguity.</b> So <b>P3P inside RANSAC is the standard "
    "approach</b>, and the sample size of 3 pays off exponentially in "
    "iteration count (Module 03 &sect;3) — another instance of why "
    "minimal solvers are worth deriving.",
    "<b>This is how each new image joins the reconstruction</b>, and it "
    "is why the incremental pipeline is incremental: each image needs "
    "existing structure to register against, so the reconstruction must "
    "grow rather than appear at once.",
    "<b>And PnP is the core of camera tracking.</b> <b>A running AR or "
    "SLAM system is performing PnP against a map, every frame, at 60 "
    "Hz</b> — which means the whole of this module's machinery is "
    "what sits behind a phone placing a virtual object on a table, and is "
    "the direct bridge from this course to CSCE 650's virtual "
    "reality."]),

  ("h1", "2 &nbsp; Bundle adjustment"),
  ("eq", "minimise &nbsp; &Sigma;<sub>ij</sub> &rho;( &#8741; "
         "&pi;(C<sub>i</sub>, X<sub>j</sub>) &minus; x<sub>ij</sub> "
         "&#8741;&#178; )"),
  ("p", "<b>One objective over every camera parameter and every world "
        "point simultaneously</b>, summed over all observations, with "
        "&rho; a robust loss. Thousands of cameras and millions of points "
        "means millions of unknowns — <b>and it is solved routinely, "
        "in seconds to minutes</b>, which is initially surprising."),
  ("p", "<b>It is tractable because the Jacobian is extremely sparse.</b> "
        "Camera i's residuals do not involve point j unless camera i "
        "actually observed point j, and in any real dataset each camera "
        "sees a tiny fraction of the points. <b>The standard exploitation "
        "is the Schur complement:</b> the points block is "
        "block-diagonal (each point is independent of every other, given "
        "the cameras), so it can be eliminated analytically, leaving a "
        "much smaller dense system in the camera parameters alone. "
        "<b>That reduction is the entire engineering content of a bundle "
        "adjustment library</b>, and it is why Ceres and g2o exist as "
        "specialised tools rather than everyone calling a generic "
        "optimiser."),
  ("callout", "What bundle adjustment needs to work",
   ["<b>A good initialisation.</b> It is a non-convex least-squares "
    "problem (CSCE 669 Module 01 &sect;2) and converges to a local "
    "minimum — <b>which is the entire reason the incremental "
    "pipeline of &sect;1 exists</b>. Bundle adjustment is a refinement "
    "step, not a solver; something else must get close first.",
    "<b>A robust loss.</b> Plain squared error lets a single mismatched "
    "observation dominate the objective, because the residual is "
    "quadratic and a gross outlier's residual is enormous. <b>Huber or "
    "Cauchy bounds each observation's influence, and this is not "
    "optional</b> — a pipeline without it fails on real data "
    "regardless of how good the matching was.",
    "<b>Gauge fixing.</b> The solution is free up to a global similarity "
    "transform — Module 01's scale ambiguity plus an arbitrary "
    "global rotation and translation — so <b>the normal equations "
    "are singular with a 7-dimensional null space unless you fix one "
    "camera's pose and one distance</b>. Omitting this produces a solver "
    "that wanders or fails to converge for reasons that look numerical "
    "and are structural.",
    "<b>And Levenberg–Marquardt rather than plain "
    "Gauss–Newton.</b> <b>The damping term is what keeps the step "
    "stable when the Jacobian is near-singular</b>, which happens "
    "routinely at near-degenerate configurations — it interpolates "
    "between Gauss–Newton when the model is trustworthy and gradient "
    "descent when it is not, which is CSCE 669 Module 07's trust-region "
    "idea in its most-used form."]),

  ("break",),
  ("h1", "3 &nbsp; Drift and loop closure"),
  ("callout", "Drift is accumulated error with no external reference",
   ["<b>Each frame's pose is estimated relative to what came before, so "
    "errors compound multiplicatively rather than averaging out.</b> A "
    "per-frame rotation error of 0.1 degree becomes 36 degrees over 360 "
    "frames, and nothing in a purely sequential estimator corrects it.",
    "<b>The result is a reconstruction that is locally excellent and "
    "globally bent.</b> A straight corridor comes out curved; a trajectory "
    "that returned to its starting point does not close. <b>Every local "
    "measurement is consistent and the global structure is wrong</b>, "
    "which is why residual statistics do not reveal drift.",
    "<b>Loop closure fixes it:</b> recognise that the current frame "
    "observes a place already in the map, add the corresponding "
    "constraint, and <b>redistribute the accumulated error over the whole "
    "trajectory</b> by re-optimising with that constraint in place "
    "(pose-graph optimisation, which is bundle adjustment over poses "
    "alone).",
    "<b>So place recognition is essential infrastructure rather than a "
    "feature.</b> <b>And it is an image-retrieval problem</b> — "
    "find the database image most similar to this query — which is "
    "CSCE 670's subject, and is why bag-of-visual-words indexes and "
    "learned global descriptors appear inside SLAM systems that otherwise "
    "contain no learning at all."]),
  ("table", ["", "Incremental", "Global"],
   [["<b>Method</b>",
     "<b>Add one image at a time, bundle adjusting repeatedly.</b>",
     "<b>Solve for all rotations at once, then all translations, then "
     "refine everything.</b>"],
    ["<b>Robustness</b>",
     "<b>High — a bad image fails to register and is simply "
     "rejected</b>, with no effect on what exists.",
     "Lower — one bad pairwise constraint influences the whole "
     "rotation-averaging solution."],
    ["<b>Cost</b>",
     "<b>Up to O(n&#8308;) in the worst case</b>, because bundle "
     "adjustment is repeated as the reconstruction grows.",
     "<b>Substantially cheaper on large image sets</b>, which is what "
     "motivated it."],
    ["<b>Drift</b>", "Accumulates; requires explicit loop closure.",
     "<b>Less drift by construction</b>, since all constraints enter "
     "simultaneously."],
    ["<b>Used by</b>", "<b>COLMAP, and most SLAM front ends.</b>",
     "<b>Internet-scale reconstruction</b>, where n is in the "
     "hundreds of thousands."]],
   [0.15, 0.42, 0.43]),
  ("p", "<b>Incremental wins on robustness and loses on scale</b>, which "
        "is why production systems are hybrid: solve global rotations "
        "first (which is well-conditioned and cheap), then refine "
        "incrementally with the robustness that provides. <b>The field "
        "did not settle on either pure approach</b>, and that is worth "
        "knowing before implementing one."),

  ("h1", "4 &nbsp; Diagnosing a failed reconstruction"),
  ("ul", ["<b>The reconstruction splits into disconnected "
          "components.</b> Not enough geometrically verified pairs bridge "
          "them. <b>The fix is capture, not code</b> — photograph "
          "the transition between the two regions.",
          "<b>Everything collapses onto a plane or toward a point.</b> A "
          "degenerate seed pair, or a genuinely planar scene (Module 04 "
          "&sect;4). <b>Check the seed pair's homography test "
          "first.</b>",
          "<b>A straight corridor comes out curved.</b> Drift "
          "(&sect;3). Needs loop closure, or more overlap between "
          "non-adjacent frames so that long-range constraints exist.",
          "<b>High residuals concentrated on one object.</b> <b>It "
          "moved.</b> <b>Structure from motion assumes a rigid, static "
          "scene, and it will silently distort the geometry to "
          "accommodate a moving object</b> rather than reporting a "
          "problem — which is why reconstructions of streets with "
          "traffic have characteristic smears.",
          "<b>Duplicated structure — two copies of the same "
          "wall in the model.</b> <b>Repeated texture fooled place "
          "recognition into a false loop closure, or prevented a true "
          "one.</b> <b>The hardest failure to fix</b>, because the "
          "incorrect constraint is strongly supported.",
          "<b>Always render the point cloud from a novel viewpoint and "
          "compare against a photograph taken from roughly there.</b> "
          "<b>Residual statistics do not reveal a doubled wall or a bent "
          "corridor; a picture reveals both immediately</b> — which "
          "is the same 'test the frame, not the numbers' discipline that "
          "CSCE 647 insisted on."]),
 ],
 "resources": [
   ("Schönberger & Frahm &mdash; Structure-from-Motion Revisited "
    "(COLMAP) (free)",
    "https://demuc.de/papers/schoenberger2016sfm.pdf",
    "<b>The reference pipeline of &sect;1</b>, with the seed selection "
    "and verification details that matter most."),
   ("Triggs et al. &mdash; Bundle Adjustment: A Modern Synthesis (free)",
    "https://lear.inrialpes.fr/pubs/2000/TMHF00/Triggs-va99.pdf",
    "<b>The &sect;2 reference.</b> Long, thorough, and the source for the "
    "sparsity and gauge-fixing treatment."),
   ("Ceres Solver documentation — bundle adjustment example (free)",
    "http://ceres-solver.org/nnls_tutorial.html#bundle-adjustment",
    "<b>A working sparse bundle adjustment you can read and run</b>, with "
    "the Schur complement option exposed."),
   ("Cadena et al. &mdash; Past, Present, and Future of SLAM (free "
    "survey)",
    "https://arxiv.org/abs/1606.05830",
    "<b>The &sect;3 material in its SLAM form</b>, including loop closure "
    "and place recognition."),
 ],
 "exercises": [
   "<b>Run COLMAP on 50 of your own photographs</b> and inspect the "
   "reported statistics.",
   "<b>Implement the pipeline's steps 1 to 5 yourself</b> and compare the "
   "seed pair you choose against COLMAP's.",
   "<b>Deliberately seed from a near-planar pair</b> and report what "
   "happens.",
   "<b>Implement PnP with P3P inside RANSAC</b> and verify against "
   "OpenCV.",
   "<b>Implement bundle adjustment for 10 cameras</b> using a sparse "
   "solver, and report the error before and after.",
   "<b>Run it with squared loss and with Huber</b> on data containing "
   "deliberate mismatches, and compare.",
   "<b>Omit gauge fixing</b> and report what the solver does.",
   "<b>Capture a loop</b> — walk a circuit and return — and "
   "measure the closure error without loop closure.",
   "<b>Add the loop constraint</b> and report the improvement across the "
   "trajectory.",
   "<b>Reconstruct a scene containing a moving object</b> and locate the "
   "distortion it causes.",
 ],
 "selfcheck": [
   "Give the seven steps of the incremental pipeline.",
   "Why is geometric verification what makes it robust?",
   "Why does the seed pair matter so much?",
   "What is PnP, and where is it used at 60 Hz?",
   "State the bundle adjustment objective and explain why it is "
   "tractable.",
   "Name its four practical requirements.",
   "What is drift, why do residuals not reveal it, and what fixes it?",
   "Compare incremental and global approaches.",
   "Name five failure symptoms and their causes.",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Stereo and Dense Depth",
 "subtitle": "A depth value at every pixel.",
 "question": "How do you get depth everywhere, not just at features?",
 "outcomes": [
     "Explain rectification and why it is done first.",
     "Explain the cost volume and the matching cost choices.",
     "Explain why smoothness is required and how it is imposed.",
     "Compare passive stereo against active depth sensing.",
     "State where dense stereo fails and why.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Rectification",
   "blurb": "Making the epipolar lines horizontal."},

  {"t": "callout", "title": "Rectify first, and the search becomes a scan along a row",
   "kind": "Why every stereo pipeline starts here",
   "body": ["<b>Module 04 reduced the match search to a line.</b> "
            "Rectification warps both images so that line is the <i>same "
            "horizontal row</i> in both.",
            "<b>Then the correspondence for pixel (u,v) lies at "
            "(u−d, v) for some disparity d ≥ 0</b> "
            "— a one-dimensional search over integers, per pixel.",
            "<b>Which makes the problem cache-friendly and "
            "vectorisable</b>, and that is why it is done even though the "
            "geometry does not require it.",
            "<b>Depth follows from disparity directly:</b> "
            "Z = f·b / d. <b>Disparity and inverse depth are the "
            "same quantity up to a constant</b>, which is why stereo "
            "methods work in disparity throughout."]},

  {"t": "code", "kicker": "Cost volume", "title": "The structure every stereo method builds",
   "lang": "text", "code": """
  For each pixel (u,v) and each candidate disparity d,
  compute a MATCHING COST:

      C[v][u][d] = cost of matching left(u,v)
                   against right(u-d, v)

  That three-dimensional array is the COST VOLUME, and it
  is the common structure of classical and learned stereo
  alike.

  MATCHING COSTS, weakest to strongest:
    SAD / SSD        sum of absolute/squared differences.
                     Fast; breaks under any exposure change.
    NCC              normalised cross-correlation.
                     Invariant to affine intensity change.
    CENSUS           compare each neighbour's intensity to
                     the centre, Hamming-distance the bit
                     strings. INVARIANT TO ANY MONOTONIC
                     intensity change -- the best classical
                     choice, and cheap.
    LEARNED          a small CNN scores patch pairs.
                     Better, especially on low texture.

  WINNER-TAKE-ALL over d gives a disparity map that is
  recognisable and noisy. Everything after this is about
  the noise.
""",
   "caption": "<b>Census is the right default for classical stereo</b> "
              "— monotonic-invariance costs almost nothing and "
              "handles the exposure differences real rigs have.",
   "note": "Census is underused relative to how well it works."},

  {"t": "section", "label": "Part 2", "title": "Smoothness",
   "blurb": "Why per-pixel matching is not enough."},

  {"t": "callout", "title": "Per-pixel matching is ambiguous, so a prior is required",
   "kind": "Module 01, concretely",
   "body": ["<b>A textureless region matches equally well at every "
            "disparity.</b> The cost volume is flat and the argmin is "
            "noise.",
            "<b>A repeated pattern matches well at several "
            "disparities</b>, and winner-take-all picks one arbitrarily "
            "— confidently.",
            "<b>So impose smoothness:</b> neighbouring pixels probably "
            "have similar disparity, because surfaces are mostly "
            "continuous.",
            "<b>But not at object boundaries</b>, where disparity jumps. "
            "<b>So the smoothness penalty must be edge-aware</b> "
            "— weak across image edges, strong within regions. "
            "<b>That single refinement is most of what separates good "
            "stereo from bad.</b>"]},

  {"t": "table", "kicker": "Methods", "title": "How smoothness is imposed",
   "header": ["Method", "How", "Note"],
   "widths": [2.6, 4.3, 5.1],
   "rows": [
     ["<b>Window matching</b>", "<b>Aggregate cost over a patch</b>", "<b>Implicit smoothness; blurs boundaries</b>"],
     ["<b>Graph cuts</b>", "<b>Global energy, solved exactly for two labels</b>", "<b>Min-cut — CSCE 669 M11</b>"],
     ["<b>Semi-global (SGM)</b>", "<b>Dynamic programming along 8 directions, summed</b>", "<b>The classical sweet spot; fast and good</b>"],
     ["<b>Bilateral / guided</b>", "Edge-aware cost aggregation", "Cheap and surprisingly effective"],
     ["<b>Learned</b>", "<b>3D convolutions over the cost volume</b>", "<b>Best accuracy; needs training data</b>"],
   ],
   "footnote": "<b>SGM is the method to implement first:</b> it is a "
               "hundred lines, runs in real time, and is still "
               "competitive on textured scenes.",
   "note": "The graph-cuts link back to the optimisation course is worth "
           "making explicit."},

  {"t": "section", "label": "Part 3", "title": "Active depth",
   "blurb": "Projecting the texture you need."},

  {"t": "callout", "title": "If the scene has no texture, supply some",
   "kind": "The engineering escape",
   "body": ["<b>Structured light projects a known pattern</b> and "
            "triangulates its deformation — so a blank wall becomes "
            "a textured one and stereo works.",
            "<b>Time of flight measures the round trip of modulated "
            "light</b> per pixel, with no correspondence problem at "
            "all.",
            "<b>Each has its own failures:</b> structured light loses to "
            "sunlight and to dark surfaces; time of flight suffers "
            "multi-path on corners and interference between units.",
            "<b>And both fail on the same materials as passive "
            "stereo:</b> <b>glass, polished metal, and water defeat every "
            "method here</b>, because the assumption that a surface "
            "returns light from where it is located fails."]},

  {"t": "section", "label": "Part 4", "title": "Failure",
   "blurb": "Where dense depth cannot work."},

  {"t": "bullets", "kicker": "Failure", "title": "Where stereo fails, and why",
   "items": [
     "<b>Textureless surfaces.</b> No signal to match. <b>Walls, "
     "skies, tabletops.</b> The dominant failure indoors.",
     "",
     "<b>Repeated texture.</b> Confident wrong matches. <b>Brick, "
     "tile, railings, keyboards.</b>",
     "",
     "<b>Occlusion.</b> Pixels visible in one view only have no "
     "correct disparity at all — they must be detected and "
     "labelled, not estimated.",
     "",
     "<b>Specular and transparent surfaces.</b> The apparent "
     "brightness depends on viewpoint, so brightness constancy fails "
     "outright.",
     "",
     "<b>And distance.</b> <b>Error grows as Z²</b> "
     "(Module 04 §4), so every rig has a usable range that is "
     "computable in advance.",
   ],
   "footnote": "<b>Report a confidence or validity mask with every depth "
               "map.</b> <b>A depth value in a textureless region is "
               "fabrication</b>, and downstream code must be able to tell "
               "the difference."},

  {"t": "callout", "title": "Multi-view stereo is the same idea with more views",
   "kind": "The generalisation",
   "body": ["<b>With n calibrated views, build the cost volume by "
            "projecting each candidate depth into every view and "
            "measuring photo-consistency.</b>",
            "<b>More views resolve the ambiguities of two</b> — a "
            "repeated pattern is unlikely to be consistent across six "
            "viewpoints — which is Module 01's first strategy, "
            "applied harder.",
            "<b>And occlusion becomes tractable</b>, because a point "
            "hidden in some views is visible in others, if the view "
            "selection accounts for it.",
            "<b>This is what COLMAP's dense stage does</b>, and it is "
            "the classical method that <b>Module 11's neural "
            "representations replaced</b> — by optimising a renderer "
            "instead of a cost volume."]},
 ],
 "takeaways": [
   "Rectification makes epipolar lines coincide with image rows, turning "
   "correspondence into a horizontal scan — done for computational "
   "reasons, not geometric ones.",
   "Disparity and inverse depth are the same quantity up to a constant, "
   "which is why stereo methods work in disparity.",
   "The cost volume is the common structure of classical and learned "
   "stereo, and census matching is the best cheap classical cost.",
   "Per-pixel matching is ambiguous in textureless and repeated regions, so "
   "a smoothness prior is required — and it must be edge-aware.",
   "Active depth supplies the texture passive stereo lacks, and fails on "
   "the same materials for the same reason.",
   "A depth value in a textureless region is fabrication, so every depth "
   "map needs a validity mask.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Rectification and the cost volume"),
  ("callout", "Rectify first, and the search becomes a scan along a row",
   ["<b>Module 04 reduced the correspondence search to a line.</b> "
    "Rectification warps both images with homographies so that line is "
    "<i>the same horizontal row</i> in both images.",
    "<b>Then the match for pixel (u, v) in the left image lies at "
    "(u &minus; d, v) in the right, for some disparity d &ge; 0</b> "
    "— a one-dimensional search over integers, independently per "
    "pixel.",
    "<b>Which makes the computation cache-coherent and vectorisable</b>, "
    "and that is the actual reason it is done: the geometry does not "
    "require rectification, and the arithmetic is far faster with it. "
    "<b>CSCE 735's memory-locality lesson, in a vision pipeline.</b>",
    "<b>Depth follows from disparity directly: Z = fb/d.</b> "
    "<b>Disparity and inverse depth are therefore the same quantity up "
    "to a constant factor</b>, which is why stereo methods work in "
    "disparity throughout, and why uniform disparity sampling is a "
    "sensible choice while uniform depth sampling is not — it "
    "matches where the precision actually lies (Module 04 &sect;4's "
    "Z&#178; relationship)."]),
  ("code", """For each pixel (u,v) and each candidate disparity d,
compute a MATCHING COST:

    C[v][u][d] = cost of matching left(u,v) against
                 right(u-d, v)

That three-dimensional array is the COST VOLUME, and it is
the common structure of classical and learned stereo alike.

MATCHING COSTS, weakest to strongest:

  SAD / SSD   sum of absolute or squared differences.
              Fast. Breaks under any exposure difference
              between the two cameras, which real rigs
              always have.

  NCC         normalised cross-correlation. Invariant to
              affine intensity change (gain and offset).

  CENSUS      compare each neighbour's intensity to the
              window centre, producing a bit string; cost
              is the Hamming distance between the two
              strings. INVARIANT TO ANY MONOTONIC intensity
              transform, and very cheap. The best classical
              choice, and underused.

  LEARNED     a small CNN scores patch pairs. Better still,
              especially on weak texture.

WINNER-TAKE-ALL over d gives a disparity map that is
recognisable and very noisy. Everything after this point is
about the noise."""),

  ("h1", "2 &nbsp; Smoothness"),
  ("callout", "Per-pixel matching is ambiguous, so a prior is required",
   ["<b>A textureless region matches equally well at every disparity.</b> "
    "The cost volume is flat along d and the argmin is determined by "
    "sensor noise — which is Module 01's under-determination "
    "appearing per-pixel.",
    "<b>A repeated pattern matches well at several disparities</b>, and "
    "winner-take-all selects one of them arbitrarily and confidently. "
    "<b>The failure is worse than the textureless case</b>, because the "
    "cost at the chosen disparity is genuinely low, so confidence "
    "measures based on cost value do not catch it.",
    "<b>So impose smoothness:</b> neighbouring pixels probably have "
    "similar disparity, because surfaces are mostly continuous. This is "
    "a prior, chosen because the inversion needs one.",
    "<b>But it is false at object boundaries</b>, where disparity jumps "
    "discontinuously. <b>So the smoothness penalty must be edge-aware "
    "— weak across image intensity edges, strong within uniform "
    "regions.</b> <b>That single refinement is most of what separates "
    "good stereo from bad</b>, and it is the same insight as the "
    "edge-aware filtering of CSCE 748 Module 03."]),
  ("table", ["Method", "How it works", "Note"],
   [["<b>Window aggregation</b>",
     "<b>Sum the matching cost over a patch rather than a pixel.</b>",
     "<b>Smoothness imposed implicitly, and it blurs depth "
     "boundaries</b> — a larger window means less noise and worse "
     "edges."],
    ["<b>Graph cuts</b>",
     "<b>Minimise a global energy of data plus smoothness terms, solved "
     "exactly for two labels and approximately for more.</b>",
     "<b>Minimum cut — CSCE 669 Module 11 &sect;1's reduction, "
     "used in anger.</b> Accurate and slow."],
    ["<b>Semi-global matching (SGM)</b>",
     "<b>Dynamic programming along 8 directions through the image, with "
     "the costs summed.</b>",
     "<b>The classical sweet spot.</b> Approximates the global solution, "
     "runs in real time, around a hundred lines. <b>Implement this "
     "one first.</b>"],
    ["<b>Bilateral / guided aggregation</b>",
     "Aggregate the cost volume with an edge-aware filter.",
     "Cheap, parallel, and surprisingly effective; the filter does the "
     "edge-awareness for you."],
    ["<b>Learned</b>",
     "<b>3D convolutions over the cost volume, trained end to end.</b>",
     "<b>Best accuracy on benchmarks</b>, requires training data with "
     "ground-truth depth, and inherits Module 12's distribution-shift "
     "problem."]],
   [0.20, 0.39, 0.41]),

  ("break",),
  ("h1", "3 &nbsp; Active depth sensing"),
  ("callout", "If the scene has no texture, supply some",
   ["<b>Structured light projects a known pattern — stripes, dots, "
    "or a pseudorandom speckle — and triangulates from how the "
    "pattern deforms.</b> <b>A blank wall becomes a textured wall</b>, "
    "and the correspondence problem becomes easy because the projected "
    "pattern is designed to be locally unique.",
    "<b>Time of flight measures the round-trip delay of modulated light "
    "per pixel</b>, so there is no correspondence problem at all — "
    "depth is measured directly rather than inferred.",
    "<b>Each has characteristic failures.</b> Structured light is "
    "overwhelmed by sunlight (the projector cannot compete) and fails on "
    "dark surfaces (insufficient return) and at range (pattern "
    "divergence). Time of flight suffers multi-path error at concave "
    "corners, where light arrives by two routes, and interference "
    "between multiple units in the same room.",
    "<b>And both fail on the same materials as passive stereo.</b> "
    "<b>Glass, polished metal, and water defeat every method in this "
    "module</b>, because they all assume a surface returns light from the "
    "place where the surface is — and a mirror returns light from "
    "somewhere else entirely, which is a correct measurement of the wrong "
    "geometry. <b>No amount of sensing resolves it; it needs a prior "
    "about materials</b> (Module 01 &sect;3's fourth strategy)."]),

  ("h1", "4 &nbsp; Where dense stereo fails"),
  ("ul", ["<b>Textureless surfaces.</b> No signal to match against. "
          "<b>Painted walls, skies, tabletops, doors.</b> <b>The dominant "
          "failure indoors</b>, and the reason consumer depth cameras are "
          "active rather than passive.",
          "<b>Repeated texture.</b> Confident wrong matches, as "
          "&sect;2 described. <b>Brick, tile, railings, keyboards, "
          "textiles.</b>",
          "<b>Occlusion.</b> Pixels visible in one view and not the other "
          "<b>have no correct disparity at all</b> — there is "
          "nothing to match. <b>They must be detected and labelled "
          "invalid, not estimated</b>, and a left-right consistency check "
          "is the standard detector.",
          "<b>Specular and transparent surfaces.</b> Apparent brightness "
          "depends on viewpoint, so the brightness-constancy assumption "
          "underlying every matching cost fails outright rather than "
          "degrading.",
          "<b>And distance.</b> <b>Error grows as Z&#178;</b> "
          "(Module 04 &sect;4), so every rig has a usable range that is "
          "computable before it is built, and operating beyond it produces "
          "depth maps that look plausible and are meaningless.",
          "<b>So report a confidence or validity mask with every depth "
          "map.</b> <b>A depth value in a textureless region is "
          "fabrication</b> — the algorithm had no information and "
          "returned a number anyway — and downstream code must be "
          "able to distinguish 'measured 2.3 m' from 'guessed 2.3 m'. "
          "<b>Systems that propagate depth without validity fail in ways "
          "that are extremely hard to trace</b>, because the error enters "
          "as a plausible measurement."]),
  ("callout", "Multi-view stereo is the same idea with more views",
   ["<b>With n calibrated views, build the cost volume by projecting each "
    "candidate depth into every view and measuring photo-consistency "
    "across all of them.</b> The structure is identical; only the cost's "
    "support changes.",
    "<b>More views resolve the ambiguities that two cannot.</b> A "
    "repeated pattern is unlikely to be consistent across six genuinely "
    "different viewpoints, and a textureless region at least becomes "
    "better constrained by its boundaries. <b>This is Module 01's first "
    "strategy applied harder</b>, and it is the only one of the four with "
    "guarantees.",
    "<b>And occlusion becomes tractable</b> rather than fatal, because a "
    "point hidden in some views is visible in others — provided the "
    "view selection accounts for visibility, which is the main "
    "engineering difficulty.",
    "<b>This is what COLMAP's dense reconstruction stage does</b>, and it "
    "is the classical method that <b>Module 11's neural representations "
    "displaced</b> — by optimising a differentiable renderer against "
    "the photographs instead of searching a cost volume. <b>Same "
    "problem, same input, entirely different formulation</b>, and the "
    "comparison is the most instructive thing in this course."]),
 ],
 "resources": [
   ("Szeliski &mdash; Computer Vision, chapter 12 (free PDF)",
    "https://szeliski.org/Book/",
    "<b>Stereo correspondence, rectification, and the cost volume</b> "
    "— the reference for &sect;1 and &sect;2."),
   ("Hirschmüller &mdash; Stereo Processing by Semi-Global Matching "
    "(free)",
    "https://core.ac.uk/download/pdf/11134866.pdf",
    "<b>SGM, the method of &sect;2's table.</b> Implementable directly "
    "from the paper."),
   ("Scharstein & Szeliski &mdash; the Middlebury stereo benchmark "
    "(free)",
    "https://vision.middlebury.edu/stereo/",
    "<b>Ground-truth data and a leaderboard</b>, plus the taxonomy that "
    "organises &sect;2's methods."),
   ("Zabih & Woodfill &mdash; Non-parametric Local Transforms (census) "
    "(free)",
    "https://link.springer.com/chapter/10.1007/BFb0028345",
    "<b>The census transform of &sect;1</b>, and the monotonic-invariance "
    "argument."),
 ],
 "exercises": [
   "<b>Rectify a calibrated stereo pair</b> and verify that matched "
   "features land on the same row.",
   "<b>Build a cost volume with SAD, NCC, and census</b> and compare the "
   "winner-take-all disparity maps.",
   "<b>Change the exposure on one camera</b> and report which cost "
   "survives.",
   "<b>Implement SGM</b> and compare against winner-take-all on the same "
   "cost volume.",
   "<b>Make the smoothness penalty edge-aware</b> and measure the "
   "improvement at depth boundaries.",
   "<b>Implement a left-right consistency check</b> and visualise the "
   "occlusion mask.",
   "<b>Measure the fraction of pixels your method should refuse</b> on a "
   "real indoor scene.",
   "<b>Compare your depth against an active depth camera</b> if you have "
   "one, and locate where each fails.",
   "<b>Photograph a glass or chrome object</b> with both and report what "
   "each returns.",
   "<b>Verify the Z² error law</b> on objects at measured distances.",
 ],
 "selfcheck": [
   "Why rectify, given the geometry does not require it?",
   "Why are disparity and inverse depth the same quantity?",
   "What is the cost volume, and which matching cost is the best cheap "
   "classical one and why?",
   "Why is per-pixel matching insufficient, and why must smoothness be "
   "edge-aware?",
   "Compare five ways of imposing smoothness.",
   "What do structured light and time of flight each do, and how does "
   "each fail?",
   "Which materials defeat every method here, and why?",
   "Name five stereo failure modes.",
   "Why must a depth map carry a validity mask?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Motion and Tracking",
 "subtitle": "Correspondence over time.",
 "question": "How do you follow a point, or a whole image, from frame to "
             "frame?",
 "outcomes": [
     "Derive the optical flow constraint and the aperture problem.",
     "Explain Lucas–Kanade and its conditioning.",
     "Explain coarse-to-fine estimation.",
     "Explain filtering for tracking, and what a Kalman filter assumes.",
     "Distinguish tracking from detection, and explain when each "
     "fails.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Optical flow",
   "blurb": "One equation, two unknowns."},

  {"t": "eq", "kicker": "Flow", "title": "The brightness constancy constraint",
   "eqs": [
     ("I(x, y, t) = I(x + u, y + v, t + 1)",
      "A moving point keeps its intensity. The assumption, stated."),
     ("Iₓ u + I_y v + I_t = 0",
      "First-order expansion. ONE equation, TWO unknowns, per pixel."),
     ("So flow is under-determined at every pixel",
      "The aperture problem of Module 03 §1, now as an "
      "algebraic fact rather than an intuition."),
   ],
   "caption": "<b>Only the flow component along the image gradient is "
              "recoverable</b> — the perpendicular component is "
              "invisible, which is exactly why a rotating barber pole "
              "appears to move upward.",
   "note": "The barber pole is the clearest demonstration of normal flow "
           "and is worth showing."},

  {"t": "callout", "title": "Lucas–Kanade: assume the flow is constant over a window",
   "kind": "The standard resolution",
   "body": ["<b>One equation per pixel is not enough. So assume all "
            "pixels in a small window share the same flow</b> and solve "
            "the overdetermined system by least squares.",
            "<b>The normal equations involve the structure tensor "
            "again</b> — the same 2×2 gradient covariance as "
            "Harris (Module 03 §1).",
            "<b>So flow is recoverable exactly where Harris finds "
            "corners</b>, and unrecoverable on edges and flat regions. "
            "<b>'Good feature to track' and 'good feature to match' are "
            "the same property</b>, which is how Shi–Tomasi was "
            "derived.",
            "<b>And the matrix's condition number tells you the "
            "uncertainty</b> — <b>report it, and discard tracks where "
            "it is poor</b> rather than propagating a confident wrong "
            "velocity."]},

  {"t": "section", "label": "Part 2", "title": "Large motion",
   "blurb": "The first-order expansion only holds for small "
            "displacements."},

  {"t": "code", "kicker": "Coarse to fine", "title": "Why pyramids are not an optimisation",
   "lang": "text", "code": """
  THE PROBLEM: the flow equation came from a FIRST-ORDER
  Taylor expansion, valid only for displacements of about
  one pixel. A 30-pixel motion violates it completely, and
  the estimate is not merely inaccurate -- it is unrelated
  to the true motion.

  THE FIX: build an image pyramid. At 1/32 resolution, a
  30-pixel motion IS about one pixel.

      estimate flow at the coarsest level
      upsample the flow, scale by 2
      WARP the next image by the current estimate
      estimate the RESIDUAL flow at this level
      repeat down to full resolution

  Each level only ever estimates a small residual, so the
  linearisation is valid at every level.

  THIS IS NOT A SPEED OPTIMISATION. Without it the method
  does not work at all for realistic motion. It is also
  exactly CSCE 669's trust-region idea: take a step only
  as large as the local model justifies.

  AND IT FAILS when a small object moves far -- the object
  vanishes at coarse scales, so the coarse estimate misses
  it and the fine levels cannot recover.
""",
   "caption": "<b>The small-fast-object failure is intrinsic to "
              "coarse-to-fine</b>, and is a large part of why learned flow "
              "methods won on benchmarks that contain it.",
   "note": "Naming the intrinsic failure explains the learned-method "
           "transition honestly."},

  {"t": "section", "label": "Part 3", "title": "Tracking over time",
   "blurb": "Using history, and what that assumes."},

  {"t": "callout", "title": "A Kalman filter is optimal under assumptions you should check",
   "kind": "What filtering buys and costs",
   "body": ["<b>Predict the state forward with a motion model, then "
            "correct it with the measurement, weighting each by its "
            "covariance.</b> That is the whole algorithm.",
            "<b>It is provably optimal when the dynamics are linear, "
            "the noise is Gaussian, and the model is correct.</b> All "
            "three fail in real tracking.",
            "<b>Non-linear dynamics get the extended or unscented "
            "variants; multi-modal uncertainty needs a particle "
            "filter</b> — because a Gaussian cannot represent 'the "
            "object is in one of two places'.",
            "<b>And the failure mode is overconfidence:</b> <b>a filter "
            "whose model is wrong reports small covariance while being "
            "badly wrong</b>, and will reject the correct measurement as "
            "an outlier. <b>Monitor the innovation, not the "
            "covariance.</b>"]},

  {"t": "table", "kicker": "Tracking", "title": "Tracking against detection",
   "header": ["", "Tracking", "Detection per frame"],
   "widths": [2.3, 4.5, 5.2],
   "rows": [
     ["<b>Uses</b>", "<b>Previous position; small search</b>", "<b>Nothing; searches the whole frame</b>"],
     ["<b>Cost</b>", "<b>Cheap</b>", "Expensive"],
     ["<b>Identity</b>", "<b>Maintained naturally</b>", "<b>Must be re-associated every frame</b>"],
     ["<b>Fails by</b>", "<b>DRIFT — slow accumulation onto the background</b>", "Missed detections, flicker"],
     ["<b>Recovery</b>", "<b>Cannot recover once lost</b>", "<b>Recovers automatically next frame</b>"],
   ],
   "footnote": "<b>So real systems do both:</b> track for cheapness and "
               "identity, detect periodically to correct drift and "
               "recover losses. <b>Tracking-by-detection is the "
               "standard.</b>",
   "note": "The hybrid is the practical answer and should be stated "
           "plainly."},

  {"t": "section", "label": "Part 4", "title": "In practice",
   "blurb": "What breaks, and what to measure."},

  {"t": "bullets", "kicker": "Practice", "title": "Motion estimation in real systems",
   "items": [
     "<b>Rolling shutter.</b> <b>Most cameras expose rows at "
     "different times</b>, so a fast-moving object is sheared and the "
     "rigid-motion assumption is false. <b>Model it or use a global "
     "shutter.</b>",
     "",
     "<b>Motion blur.</b> The feature you are tracking is smeared "
     "across the direction of motion, which biases localisation along "
     "that same direction.",
     "",
     "<b>Illumination change.</b> Brightness constancy fails under "
     "auto-exposure, flicker, or a cloud. <b>Lock exposure if you "
     "can.</b>",
     "",
     "<b>Occlusion.</b> The track must be <i>suspended</i>, not "
     "continued — continuing it is how trackers end up following "
     "the occluder.",
     "",
     "<b>And measure drift directly:</b> <b>track a point out and back "
     "to its start and report the closure error in pixels.</b>",
   ],
   "footnote": "<b>The out-and-back test is the honest measure of a "
               "tracker</b> and needs no ground truth, which is why it is "
               "worth building into the loop."},

  {"t": "callout", "title": "Where motion connects to the rest of the course",
   "kind": "Why this module sits here",
   "body": ["<b>Flow gives dense correspondence, which is dense "
            "stereo's input when the two frames come from a moving "
            "camera</b> — structure from motion and optical flow are "
            "the same problem under different parameterisations.",
            "<b>Tracked features give the tracks of Module 05</b>, so a "
            "video is a structure-from-motion problem with free, reliable "
            "correspondence.",
            "<b>And PnP against a map at 60 Hz is SLAM</b>, which is "
            "what Module 05 §1 was building toward and what every "
            "AR system runs.",
            "<b>So Modules 03–07 are one subject:</b> "
            "<b>correspondence, across space or across time, and "
            "everything geometric depends on it.</b>"]},
 ],
 "takeaways": [
   "Brightness constancy gives one equation in two unknowns per pixel, so "
   "flow is under-determined — the aperture problem as algebra.",
   "Lucas–Kanade assumes constant flow over a window, and its normal "
   "equations contain the same structure tensor as Harris.",
   "So flow is recoverable exactly where corners are found, and the "
   "condition number is the uncertainty — report it.",
   "Coarse-to-fine is not a speed optimisation: without it the "
   "linearisation is invalid and the method does not work at realistic "
   "motion.",
   "A Kalman filter is optimal under three assumptions that all fail in "
   "practice, and its failure mode is confident wrongness.",
   "Tracking drifts and cannot recover; detection recovers and loses "
   "identity — so real systems do both.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Optical flow"),
  ("eq", "I(x, y, t) = I(x + u, y + v, t + 1) &nbsp;&nbsp; (brightness "
         "constancy)"),
  ("eq", "I<sub>x</sub> u + I<sub>y</sub> v + I<sub>t</sub> = 0 "
         "&nbsp;&nbsp; (first order)"),
  ("p", "<b>One equation, two unknowns, at every pixel.</b> Flow is "
        "under-determined pointwise — <b>which is Module 03 "
        "&sect;1's aperture problem, now as an algebraic fact rather than "
        "an intuition about windows</b>. <b>Only the flow component "
        "along the image gradient is recoverable</b> (the normal flow); "
        "the component perpendicular to the gradient does not appear in "
        "the equation at all. <b>This is exactly why a rotating barber "
        "pole appears to move upward</b>: the stripes' gradients are "
        "perpendicular to the stripes, so the recoverable motion is across "
        "them, and the true horizontal rotation is invisible. <b>The "
        "illusion is not a quirk of human vision; it is the correct answer "
        "to an under-determined problem</b>, and any algorithm using only "
        "local information makes the same report."),
  ("callout", "Lucas–Kanade: assume the flow is constant over a window",
   ["<b>One equation per pixel is insufficient, so assume that all pixels "
    "within a small window share a single flow vector</b> and solve the "
    "resulting overdetermined system by least squares. The assumption is "
    "the prior that resolves the under-determination (Module 01 "
    "&sect;3).",
    "<b>The normal equations involve the structure tensor again</b> "
    "— exactly the 2&times;2 gradient covariance matrix of "
    "Module 03 &sect;1's Harris derivation, summed over the same kind "
    "of window.",
    "<b>So flow is recoverable precisely where Harris finds corners</b>, "
    "and unrecoverable on edges (one eigenvalue near zero) and flat "
    "regions (both near zero). <b>'Good feature to track' and 'good "
    "feature to match' are literally the same property</b>, and "
    "<b>Shi–Tomasi's refinement of Harris was derived from exactly "
    "this observation</b> — use the smaller eigenvalue directly, "
    "since that is what bounds the tracking accuracy.",
    "<b>And the matrix's condition number is the uncertainty of the "
    "estimate.</b> <b>Report it, and discard tracks whose conditioning "
    "is poor</b>, rather than propagating a confident wrong velocity into "
    "Module 05's bundle adjustment — which is Module 01 &sect;2's "
    "stability problem, with a cheap and local diagnostic available."]),

  ("h1", "2 &nbsp; Large motion"),
  ("code", """THE PROBLEM: the flow equation came from a FIRST-ORDER
Taylor expansion, valid only for displacements of about one
pixel. A 30-pixel motion violates it completely, and the
resulting estimate is not merely inaccurate -- it is
unrelated to the true motion.

THE FIX: build an image pyramid. At 1/32 resolution, a
30-pixel motion IS about one pixel.

    estimate flow at the coarsest level
    upsample the flow field, scale it by 2
    WARP the next image by the current estimate
    estimate the RESIDUAL flow at this level
    repeat down to full resolution

Each level only ever estimates a small residual, so the
linearisation is valid everywhere it is used.

THIS IS NOT A SPEED OPTIMISATION. Without it the method
does not work at all for realistic motion. It is also
precisely CSCE 669 Module 07's trust-region idea: take a
step only as large as the local model justifies, then
rebuild the model.

AND IT FAILS when a SMALL object moves FAR. The object
disappears at coarse scales, so the coarse estimate does
not see it, and the fine levels are initialised from an
estimate that is already in the wrong basin."""),
  ("p", "<b>The small-fast-object failure is intrinsic to coarse-to-fine "
        "estimation</b> rather than a tuning problem, and <b>it is a large "
        "part of why learned flow methods won on benchmarks that contain "
        "such motion</b> — a learned matcher with a large receptive "
        "field or an all-pairs correlation volume is not constrained to "
        "search locally, so it can find a correspondence that no "
        "coarse-to-fine scheme could reach. <b>Which is the same pattern "
        "as Module 03 &sect;4: learning won where the classical method "
        "had a structural, identifiable weakness</b>, and that is where to "
        "expect it to win in general."),

  ("break",),
  ("h1", "3 &nbsp; Tracking over time"),
  ("callout", "A Kalman filter is optimal under assumptions you should check",
   ["<b>Predict the state forward using a motion model, then correct it "
    "with the new measurement, weighting prediction and measurement by "
    "their respective covariances.</b> That is the entire algorithm, and "
    "it is two matrix equations.",
    "<b>It is provably optimal when the dynamics are linear, the noise "
    "is Gaussian, and the motion model is correct.</b> <b>All three "
    "assumptions fail in real tracking</b> — objects accelerate "
    "unpredictably, outliers are not Gaussian, and a constant-velocity "
    "model is wrong whenever anything interesting happens.",
    "<b>Non-linear dynamics are handled by the extended or unscented "
    "variants; genuinely multi-modal uncertainty requires a particle "
    "filter</b>, because <b>a Gaussian cannot represent 'the object is "
    "in one of two places'</b> — it represents that as 'the object "
    "is probably between them', which is the one place it is not.",
    "<b>And the failure mode is overconfidence.</b> <b>A filter whose "
    "model is wrong reports a small covariance while being badly "
    "wrong</b>, because the covariance reflects the model's own "
    "self-assessment and not reality — and once confident, it "
    "<i>rejects the correct measurement as an outlier</i> and diverges "
    "further. <b>So monitor the innovation (the measurement residual), "
    "not the reported covariance</b>: persistently large innovations mean "
    "the model is wrong, whatever the covariance claims. This is the same "
    "lesson as CSCE 633 Module 12's calibration — a confident "
    "estimator is not a correct one."]),
  ("table", ["", "Tracking", "Detection every frame"],
   [["<b>Uses</b>",
     "<b>The previous position, so the search region is small.</b>",
     "<b>Nothing from the past; searches the entire frame.</b>"],
    ["<b>Cost</b>", "<b>Cheap — a local search.</b>",
     "Expensive — a full inference pass."],
    ["<b>Identity</b>",
     "<b>Maintained naturally</b> — the track <i>is</i> the "
     "identity.",
     "<b>Must be re-associated across frames</b>, which is its own "
     "assignment problem (CSCE 669 Module 11)."],
    ["<b>Fails by</b>",
     "<b>DRIFT — the window slides gradually onto the background "
     "and the track is lost without any discrete event.</b>",
     "Missed detections and flicker, which are visible and discrete."],
    ["<b>Recovery</b>",
     "<b>Cannot recover once lost</b>, because its only reference was "
     "the thing it lost.",
     "<b>Recovers automatically on the next frame</b>, with no memory "
     "of the failure."]],
   [0.14, 0.43, 0.43]),
  ("p", "<b>So real systems do both:</b> track for cheapness and for "
        "identity continuity, and detect periodically to correct drift and "
        "to recover after occlusion. <b>Tracking-by-detection is the "
        "standard architecture</b>, and the interesting engineering is in "
        "the association step between the two."),

  ("h1", "4 &nbsp; Motion in real systems"),
  ("ul", ["<b>Rolling shutter.</b> <b>Most CMOS cameras expose image "
          "rows at different times</b>, spread over milliseconds, so a "
          "fast-moving object is sheared and a fast-rotating camera "
          "produces a warped frame. <b>The rigid single-pose assumption "
          "behind Modules 04 and 05 is then false</b>, and the symptom is "
          "a reconstruction that will not converge for no visible reason. "
          "<b>Model it, or use a global-shutter camera.</b>",
          "<b>Motion blur.</b> The feature being tracked is smeared along "
          "the direction of motion, <b>which biases its localisation "
          "along that same direction</b> — a systematic error "
          "correlated with the quantity being estimated, which is the "
          "worst kind.",
          "<b>Illumination change.</b> Brightness constancy fails under "
          "auto-exposure adjustment, mains flicker, or a cloud passing. "
          "<b>Lock the exposure if the application permits</b>; otherwise "
          "use a cost that is invariant to monotonic intensity change "
          "(Module 06 &sect;1's census).",
          "<b>Occlusion.</b> <b>The track must be suspended, not "
          "continued.</b> <b>Continuing to update through an occlusion is "
          "exactly how trackers end up following the occluder</b> instead "
          "of the target, and then confidently reporting it.",
          "<b>And measure drift directly.</b> <b>Track a point out and "
          "back to its starting frame and report the closure error in "
          "pixels.</b> <b>This needs no ground truth, takes minutes, and "
          "is the honest measure of a tracker</b> — which is why it "
          "is worth building into the development loop rather than "
          "reserving for evaluation."]),
  ("callout", "Where motion connects to the rest of the course",
   ["<b>Flow gives dense correspondence, which is dense stereo's input "
    "when the two frames come from a moving camera</b> — <b>structure "
    "from motion and optical flow are the same problem under different "
    "parameterisations</b>, one solving for a sparse set of poses and "
    "points and the other for a dense displacement field.",
    "<b>Tracked features supply the tracks of Module 05 &sect;1</b>, so "
    "<b>a video is a structure-from-motion problem with free and "
    "unusually reliable correspondence</b> — temporal adjacency makes "
    "matching far easier than it is between unordered photographs.",
    "<b>And PnP against a map at 60 Hz is SLAM</b> (Module 05 "
    "&sect;1), which is what that module was building toward and what "
    "every phone AR system runs continuously — the direct bridge "
    "from this course into CSCE 650's tracking requirements.",
    "<b>So Modules 03 through 07 are one subject.</b> "
    "<b>Correspondence — across space or across time — and "
    "everything geometric in this course depends entirely on it.</b> "
    "<b>Which is why correspondence failure, not algorithm failure, is the "
    "cause of most broken geometric pipelines</b>, and why the diagnostic "
    "habit is always to inspect the matches first."]),
 ],
 "resources": [
   ("Szeliski &mdash; Computer Vision, chapter 9 (free PDF)",
    "https://szeliski.org/Book/",
    "<b>Motion estimation, optical flow, and the pyramid scheme</b> "
    "— the reference for &sect;1 and &sect;2."),
   ("Baker & Matthews &mdash; Lucas-Kanade 20 Years On (free)",
    "https://www.ri.cmu.edu/pub_files/pub3/baker_simon_2002_3/baker_simon_2002_3.pdf",
    "<b>The &sect;1 method, developed properly</b>, including the "
    "inverse-compositional formulation that makes it fast."),
   ("Welch & Bishop &mdash; An Introduction to the Kalman Filter (free)",
    "https://web.archive.org/web/20260514081034/http://www.cs.unc.edu/~welch/kalman/",
    "<b>The clearest free introduction to &sect;3</b>, with the "
    "assumptions stated explicitly."),
   ("Teed & Deng &mdash; RAFT: Recurrent All-Pairs Field Transforms "
    "(free)",
    "https://arxiv.org/abs/2003.12039",
    "<b>The learned flow method that addresses &sect;2's intrinsic "
    "failure</b>, by correlating all pairs rather than searching "
    "locally."),
 ],
 "exercises": [
   "<b>Derive the flow constraint</b> and show that only the gradient-"
   "aligned component is determined.",
   "<b>Render a rotating barber pole</b> and compute its optical flow. "
   "Confirm it points upward.",
   "<b>Implement Lucas–Kanade</b> and visualise the structure "
   "tensor's smaller eigenvalue as a trackability map.",
   "<b>Compare it against your Harris response</b> from Module 03 and "
   "confirm they agree.",
   "<b>Estimate flow for a 30-pixel motion without a pyramid</b> and "
   "report the result.",
   "<b>Add the pyramid</b> and report the improvement.",
   "<b>Construct a small fast-moving object</b> and show the pyramid "
   "fails on it.",
   "<b>Implement a constant-velocity Kalman filter</b> and track an "
   "object that accelerates. Plot the innovation.",
   "<b>Show the filter rejects correct measurements</b> once its model "
   "diverges.",
   "<b>Run the out-and-back drift test</b> on your tracker and report the "
   "closure error.",
 ],
 "selfcheck": [
   "Derive the brightness constancy constraint and state the aperture "
   "problem algebraically.",
   "Why does a barber pole appear to move upward?",
   "What does Lucas–Kanade assume, and what matrix appears in its "
   "solution?",
   "Why are good features to track the same as good features to match?",
   "Why is coarse-to-fine not a speed optimisation?",
   "What motion does coarse-to-fine intrinsically fail on?",
   "State the Kalman filter's three assumptions and its failure mode.",
   "Why monitor the innovation rather than the covariance?",
   "Compare tracking against per-frame detection on five axes.",
 ],
},

]
