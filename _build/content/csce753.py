# -*- coding: utf-8 -*-
"""CSCE 753 Computer Vision — original course content."""

COURSE = {
    "code": "CSCE 753",
    "title": "Computer Vision",
    "tagline": "Recovering the scene from the image — the inverse of "
               "everything CSCE 647 did forward",
    "term": "Semester 7 (with CSCE 625 and CSCE 642)",
    "prereqs": "CSCE 641 Computer Graphics and CSCE 647 Image Synthesis "
               "for the forward model; CSCE 636 Deep Learning for "
               "Modules 08–11; linear algebra, thoroughly",
    "effort": "12–14 hours per week · 13 modules + 2 project weeks",
    "deliverable": "A working geometric reconstruction of a real scene you "
                   "captured yourself, with calibration, reprojection "
                   "error, and an honest account of where it fails — "
                   "plus a learned-vision component evaluated under "
                   "distribution shift",
    "description": [
        "<b>CSCE 647 computed an image from a scene. This course "
        "computes a scene from images.</b> That is the entire framing, and "
        "it explains both why the subject is hard and why the graphics "
        "courses were the right preparation: <b>you cannot invert a "
        "process you do not understand forward.</b>",
        "<b>The inversion is ill-posed.</b> Infinitely many scenes "
        "produce any given image — a small near object and a large "
        "far one are indistinguishable, a dark surface in bright light "
        "matches a bright surface in dim light. <b>Module 01 establishes "
        "this properly</b>, because every method in the course is a "
        "strategy for constraining the ambiguity: more views, known "
        "geometry, motion over time, or a learned prior over what scenes "
        "are plausible.",
        "<b>The course has two halves that are genuinely different "
        "subjects.</b> <b>Modules 02 through 07 are geometric vision</b> "
        "— projective geometry, calibration, correspondence, "
        "triangulation, bundle adjustment — which is "
        "well-conditioned, provably correct where its assumptions hold, "
        "and the basis of every working camera-tracking system. "
        "<b>Modules 08 through 11 are learned vision</b>, which handles "
        "the semantic questions geometry cannot touch and offers no "
        "guarantees at all.",
        "<b>They meet at Module 11</b>, where neural scene "
        "representations solve the reconstruction problem by optimising a "
        "renderer against photographs — <b>which is CSCE 647's "
        "forward model used as a loss function</b>, and is the clearest "
        "demonstration in the program of why the forward and inverse "
        "subjects belong together.",
    ],
    "outcomes": [
        "Explain why vision is ill-posed and classify the strategies for "
        "constraining it.",
        "Calibrate a camera and state what each intrinsic parameter "
        "means.",
        "Detect, describe, and match features robustly, including "
        "RANSAC.",
        "Derive the epipolar constraint and recover relative pose from "
        "two views.",
        "Run structure from motion and diagnose drift and degeneracy.",
        "Compute dense depth from stereo and explain where it fails.",
        "Estimate and track motion, and state the brightness-constancy "
        "assumption.",
        "Train and evaluate detection and segmentation models honestly.",
        "Explain vision transformers and self-supervised pretraining.",
        "Explain neural radiance fields and Gaussian splatting as inverse "
        "rendering.",
        "Evaluate a vision system under distribution shift and state what "
        "it can be trusted to do.",
    ],
    "materials": [
        ("Szeliski — Computer Vision: Algorithms and Applications, "
         "2nd edition (free PDF)",
         "https://szeliski.org/Book/",
         "<b>The primary source, free in full from the author.</b> The "
         "geometric chapters are the reference for Modules 02 through 07 "
         "and the second edition covers the learned material of "
         "Modules 08–10."),
        ("Hartley & Zisserman — Multiple View Geometry",
         "https://www.robots.ox.ac.uk/~vgg/hzbook/",
         "<b>The definitive treatment of Modules 04 and 05.</b> Dense "
         "and worth the effort; the sample chapters are free and the "
         "errata page is useful. Library copy for the rest."),
        ("Michigan EECS 498/598 — Deep Learning for Computer Vision "
         "(free lectures and assignments)",
         "https://web.archive.org/web/20260824025044/https://web.eecs.umich.edu/~justincj/teaching/eecs498/",
         "<b>The best free course for Modules 08 through 10.</b> Full "
         "video lectures, slides, and assignments, taught at the right "
         "level for someone who has already done CSCE 636."),
        ("Mildenhall et al. — NeRF; and Kerbl et al. — 3D "
         "Gaussian Splatting (both free)",
         "https://www.matthewtancik.com/nerf",
         "<b>The two papers Module 11 is built on.</b> Both are readable "
         "and both have reference implementations, and the contrast "
         "between them is instructive."),
        ("OpenCV documentation and tutorials (free)",
         "https://docs.opencv.org/",
         "<b>The working toolkit for Modules 02–07.</b> The "
         "calibration and <code>findEssentialMat</code> tutorials are "
         "worth following exactly once before writing your own."),
        ("COLMAP documentation (free, open source)",
         "https://colmap.github.io/",
         "<b>A production structure-from-motion pipeline you can read.</b> "
         "Module 05's reference point, and what your own implementation "
         "should be compared against."),
    ],
    "tooling": [
        "<b>A camera you control.</b> A phone is adequate if you can lock "
        "the focus and exposure; <b>autofocus between frames changes the "
        "intrinsics and silently breaks calibration</b>, which is a "
        "lesson best learned once and deliberately.",
        "<b>Python with OpenCV, NumPy, and PyTorch.</b> OpenCV for the "
        "geometric pipeline, PyTorch for Modules 08–11.",
        "<b>A printed calibration target</b> — a checkerboard on "
        "stiff card, measured. <b>A target printed at the wrong scale is "
        "the most common cause of a calibration that looks fine and is "
        "wrong.</b>",
        "<b>COLMAP installed</b>, as the reference against which your own "
        "structure from motion is measured.",
        "<b>A GPU for Modules 08–11.</b> The 4 GB budget of "
        "CSCE 636 still applies — NeRF training at reduced "
        "resolution and Gaussian splatting on small scenes both fit, with "
        "care.",
        "<b>A scene you can recapture.</b> <b>Every geometric failure in "
        "this course is diagnosed by capturing again with one thing "
        "changed</b>, and a dataset you cannot extend cannot be debugged.",
    ],
    "projects": [
        {"title": "Reconstruct a real scene", "after": 7,
         "brief": "Capture a scene yourself, calibrate, and reconstruct "
                  "its geometry from your own images with your own code.",
         "reqs": [
             "<b>Your own calibration</b> from your own target images, "
             "with the intrinsics reported and the reprojection error "
             "stated in pixels.",
             "<b>Feature detection, matching, and RANSAC</b> implemented "
             "or configured, with the inlier fraction reported.",
             "<b>Relative pose from two views</b>, triangulated to a "
             "sparse point cloud.",
             "<b>Bundle adjustment</b> over at least ten views, with the "
             "error before and after.",
             "<b>A comparison against COLMAP</b> on the same images.",
             "<b>A deliberate failure case</b>: a textureless surface, a "
             "pure rotation, or a repeated pattern, with the symptom "
             "diagnosed.",
         ],
         "done": [
             "<b>Sub-pixel reprojection error after bundle adjustment</b>, "
             "reported as a number rather than described.",
             "<b>The point cloud visibly matches the scene</b> — "
             "rendered from a novel viewpoint and compared against a "
             "photograph from roughly that viewpoint.",
             "<b>The COLMAP comparison honest</b>, including where it "
             "beats you and by how much.",
             "<b>The failure case explained in terms of the "
             "geometry</b>, not described as 'it did not work'.",
         ]},
        {"title": "A learned component, evaluated honestly", "after": 12,
         "brief": "Train or fine-tune a vision model for a task you care "
                  "about, and establish what it can actually be trusted "
                  "to do.",
         "reqs": [
             "<b>A task with a real use</b> and a held-out test set "
             "collected separately from the training data.",
             "<b>A trivial baseline</b> — CSCE 633's discipline, "
             "unchanged.",
             "<b>Detection or segmentation metrics computed "
             "correctly</b>, with the IoU threshold stated.",
             "<b>An evaluation under distribution shift</b>: different "
             "lighting, camera, or location than training.",
             "<b>A failure gallery</b> of at least twenty cases, grouped "
             "by cause.",
             "<b>Latency measured</b> on the hardware it would actually "
             "run on.",
         ],
         "done": [
             "<b>The shifted-distribution number reported as "
             "prominently as the test number</b>, and it will be worse.",
             "<b>The failure modes named and grouped</b>, with a stated "
             "guess at the cause of each group.",
             "<b>A statement of what the system can be trusted to "
             "do</b>, scoped to conditions — which is the "
             "deliverable.",
             "<b>Latency on real hardware</b>, not on a cloud GPU, if it "
             "would deploy on a device.",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "The Inverse Problem",
 "subtitle": "Why vision is hard in a way graphics is not.",
 "question": "Why can an image not simply be read backwards into a "
             "scene?",
 "outcomes": [
     "State the forward model and explain what inverting it loses.",
     "Explain ill-posedness with concrete ambiguities.",
     "Classify the four strategies for constraining the inversion.",
     "Explain why priors are unavoidable rather than a shortcut.",
     "Place every module in the course against that classification.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Forward and backward",
   "blurb": "Graphics is a function. Vision is its inverse, and the "
            "function is not injective."},

  {"t": "callout", "title": "Rendering is a function; vision inverts a function that loses information",
   "kind": "The framing for the whole course",
   "body": ["<b>CSCE 647's rendering equation maps a scene — "
            "geometry, materials, lights, camera — to an "
            "image.</b> Given the scene, the image is determined.",
            "<b>Vision asks for the scene given the image.</b> But the "
            "forward map is <i>many-to-one</i>: enormous numbers of "
            "distinct scenes produce pixel-identical images.",
            "<b>So the inverse is not a function at all.</b> There is no "
            "unique answer to recover, and any method that returns a "
            "single answer has added information from somewhere.",
            "<b>That is the central fact of the subject.</b> <b>Every "
            "technique in this course is a way of supplying the missing "
            "information</b> — and knowing which information a method "
            "assumes tells you exactly when it will fail."]},

  {"t": "table", "kicker": "Ambiguities", "title": "What a single image cannot determine",
   "header": ["Ambiguity", "The confusion", "What resolves it"],
   "widths": [2.6, 4.4, 5.1],
   "rows": [
     ["<b>Depth / scale</b>", "<b>A small near object and a large far one project identically</b>", "<b>A second view, or known size</b>"],
     ["<b>Albedo / illumination</b>", "<b>Dark surface in bright light = bright surface in dim light</b>", "<b>A prior, or controlled lighting</b>"],
     ["<b>Shape / shading</b>", "A curved surface and a painted gradient", "Motion, or multiple lights"],
     ["Specular / texture", "A highlight and a white patch", "<b>Viewpoint change — highlights move</b>"],
     ["<b>Occlusion</b>", "<b>What is behind an object is simply absent</b>", "<b>Another view, or a learned prior</b>"],
     ["<b>Bas-relief</b>", "<b>A flattened scene with scaled lighting matches exactly</b>", "<b>Nothing, from shading alone</b>"],
   ],
   "footnote": "<b>The bas-relief ambiguity is provable and exact</b>, "
               "which is why shape-from-shading cannot be made to work "
               "without additional constraints.",
   "note": "Naming the ambiguities early gives students a vocabulary for "
           "every later failure."},

  {"t": "section", "label": "Part 2", "title": "Ill-posed",
   "blurb": "The precise sense in which the problem is broken."},

  {"t": "callout", "title": "Three ways a problem can be ill-posed",
   "kind": "Hadamard's conditions",
   "body": ["<b>Existence:</b> no scene explains the image. Rare in "
            "practice, and usually means the model is wrong rather than "
            "the image impossible.",
            "<b>Uniqueness:</b> many scenes explain it equally well. "
            "<b>This is the dominant failure in vision</b> and the subject "
            "of Part 1's table.",
            "<b>Stability:</b> a tiny change in the image produces a huge "
            "change in the recovered scene. <b>This is the one that "
            "silently ruins working systems</b> — the answer is unique "
            "but useless.",
            "<b>Stability is the condition-number problem again</b> "
            "(CSCE 620 M01, CSCE 669 M05) — <b>a near-degenerate "
            "configuration gives a unique answer with enormous error "
            "bars</b>, and Module 04's pure-rotation failure is exactly "
            "this."]},

  {"t": "code", "kicker": "Concretely", "title": "The depth-scale ambiguity, in four lines",
   "lang": "python", "code": """
  # A pinhole camera projects a 3D point to pixels by
  #     u = f * X / Z,    v = f * Y / Z
  # Scale the entire scene by k:
  #     u' = f * (kX) / (kZ) = f * X / Z = u
  #
  # THE IMAGE IS IDENTICAL. Scene scale is UNRECOVERABLE
  # from any number of images from an uncalibrated-baseline
  # camera. Structure from motion returns geometry up to an
  # unknown global scale, and that is not a limitation of
  # the algorithm -- it is a property of projection.
  #
  # TO FIX THE SCALE you must measure something:
  #   a known object size in the scene
  #   a measured camera baseline (stereo rig)
  #   an inertial measurement unit (visual-inertial odometry)
  #   a depth sensor
  #
  # This is why monocular SLAM drifts in scale and why every
  # phone AR system fuses the camera with the IMU.
""",
   "caption": "<b>Scale ambiguity is not a bug to be engineered "
              "around</b> — it is a theorem, and systems that need "
              "scale must measure it.",
   "note": "The AR connection makes this immediately concrete for the "
           "track."},

  {"t": "section", "label": "Part 3", "title": "The four strategies",
   "blurb": "Every method in this course is one of these."},

  {"t": "bullets", "kicker": "Strategies", "title": "How to constrain an under-determined inversion",
   "items": [
     "<b>1 · More measurements.</b> More views, more lights, more "
     "time. <b>Modules 04–07</b> — and it is the only strategy "
     "with provable guarantees.",
     "",
     "<b>2 · Known structure.</b> Calibrated cameras, a planar "
     "scene, a rigid object, a known target. <b>Modules 02–03.</b>",
     "",
     "<b>3 · Physical assumptions.</b> Brightness constancy, "
     "Lambertian surfaces, small motion. <b>Modules 06–07</b> "
     "— cheap, powerful, and each one is a failure mode.",
     "",
     "<b>4 · Learned priors.</b> What scenes are plausible, learned "
     "from data. <b>Modules 08–11</b> — the only strategy that "
     "addresses semantics, and the only one with no guarantees.",
   ],
   "footnote": "<b>These are ordered by how much they can be trusted and "
               "inversely by how much they can do</b>, which is the "
               "trade the whole course negotiates."},

  {"t": "callout", "title": "A prior is not cheating, and it is not optional",
   "kind": "The point people resist",
   "body": ["<b>Since the inversion is under-determined, choosing an "
            "answer <i>requires</i> a preference over scenes.</b> There "
            "is no neutral choice.",
            "<b>So-called assumption-free methods have implicit "
            "priors</b> — smoothness, Lambertian reflectance, "
            "general position — which are no less assumptions for "
            "being unstated.",
            "<b>A learned prior is an explicit, measurable version of "
            "the same thing</b>, and its advantage is that you can test "
            "where it holds.",
            "<b>Which is why Module 12 is about distribution shift:</b> "
            "<b>a prior is exactly as good as the match between its "
            "training distribution and your scene</b>, and that match is "
            "measurable rather than assumable."]},

  {"t": "section", "label": "Part 4", "title": "The course",
   "blurb": "Two subjects, meeting at Module 11."},

  {"t": "callout", "title": "Where this course goes",
   "kind": "The shape of the semester",
   "body": ["<b>Modules 02–07: geometric vision.</b> Projective "
            "geometry, calibration, correspondence, triangulation, bundle "
            "adjustment, stereo, flow. <b>Well-conditioned, provably "
            "correct where its assumptions hold, and the basis of every "
            "camera-tracking system that ships.</b>",
            "<b>Modules 08–10: learned vision.</b> Recognition, "
            "detection, segmentation, transformers, self-supervision. "
            "<b>Answers the semantic questions geometry cannot "
            "touch</b>, with no guarantees.",
            "<b>Module 11: they meet.</b> Neural scene representations "
            "optimise a <i>renderer</i> against photographs — "
            "<b>CSCE 647's forward model used as a loss "
            "function</b>.",
            "<b>Modules 12–13: what you can claim.</b> Evaluation "
            "under shift, and deployment. <b>The same closing discipline "
            "as every course in this program.</b>"]},
 ],
 "takeaways": [
   "Rendering maps scenes to images and is many-to-one, so the inverse is "
   "not a function and any single answer has added information.",
   "The standard ambiguities — depth/scale, albedo/illumination, "
   "shape/shading, bas-relief — are each resolved by a specific kind "
   "of extra information.",
   "Scale is unrecoverable from projection alone; this is a theorem, which "
   "is why every phone AR system fuses camera with inertial "
   "measurement.",
   "Ill-posedness has three forms, and instability — a unique answer "
   "with enormous error — is the one that ruins working systems.",
   "The four strategies are more measurements, known structure, physical "
   "assumptions, and learned priors, ordered by trustworthiness and "
   "inversely by reach.",
   "A prior is not optional: under-determination means choosing an answer "
   "requires a preference over scenes.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Forward and backward"),
  ("callout", "Rendering is a function; vision inverts one that loses "
              "information",
   ["<b>CSCE 647's rendering equation maps a scene — geometry, "
    "materials, lights, camera parameters — to an image.</b> Given "
    "the scene, the image is fully determined; the only difficulty is "
    "computing the integral, which is what that course was about.",
    "<b>Vision asks for the scene given the image, and the forward map "
    "is many-to-one.</b> Enormous numbers of genuinely distinct scenes "
    "produce pixel-identical images — not approximately identical, "
    "but exactly so, as &sect;2's scale argument shows.",
    "<b>So the inverse is not a function at all.</b> There is no unique "
    "scene to recover, and <b>any method that returns a single answer has "
    "supplied information from outside the image</b>. Identifying what "
    "that information is, for any given method, is the most useful "
    "analytical habit in the subject.",
    "<b>That is the central fact of the course.</b> <b>Every technique "
    "here is a strategy for supplying the missing information</b> "
    "(&sect;3), and <b>knowing which information a method assumes tells "
    "you precisely when it will fail</b> — a stereo method fails on "
    "textureless walls because its missing information was "
    "correspondence; a learned depth model fails on an unusual room "
    "because its missing information was a prior over rooms."]),
  ("table", ["Ambiguity", "The confusion", "What resolves it"],
   [["<b>Depth and scale</b>",
     "<b>A small near object and a large far one project to identical "
     "pixels.</b>",
     "<b>A second view with a known baseline, a known object size, or an "
     "inertial sensor</b> (&sect;2)."],
    ["<b>Albedo and illumination</b>",
     "<b>A dark surface under bright light is indistinguishable from a "
     "bright surface under dim light.</b>",
     "<b>A prior over materials and lighting, or control of the "
     "illumination.</b> This is the intrinsic-image problem and it "
     "remains unsolved in general."],
    ["<b>Shape and shading</b>",
     "A genuinely curved surface and a flat surface with a painted "
     "gradient produce the same intensities.",
     "Motion (the gradient moves with the surface), or multiple known "
     "light directions (photometric stereo)."],
    ["<b>Specularity and texture</b>",
     "A specular highlight and a white painted patch look the same in one "
     "frame.",
     "<b>Viewpoint change — highlights move across the surface and "
     "paint does not</b>, which is a two-frame test."],
    ["<b>Occlusion</b>",
     "<b>What lies behind an object is not attenuated or degraded; it is "
     "simply absent from the measurement.</b>",
     "<b>Another viewpoint, or a learned prior about object "
     "completion.</b> No amount of processing one image recovers it."],
    ["<b>Bas-relief</b>",
     "<b>A scene flattened along the view direction, with the lighting "
     "scaled correspondingly, produces an exactly identical image.</b>",
     "<b>Nothing, from shading alone.</b> The ambiguity is a proved "
     "theorem (Belhumeur, Kriegman and Yuille), which is why "
     "shape-from-shading cannot be made to work without additional "
     "constraints — and why decades of effort on it produced "
     "methods that need them."]],
   [0.19, 0.42, 0.39]),

  ("h1", "2 &nbsp; In what sense ill-posed"),
  ("callout", "Three ways a problem can be ill-posed",
   ["<b>Existence</b> — no scene explains the image. Rare in "
    "practice, and when it happens it almost always means the model is "
    "wrong (an unmodelled lens distortion, a rolling shutter) rather than "
    "that the image is impossible.",
    "<b>Uniqueness</b> — many scenes explain the image equally "
    "well. <b>This is the dominant failure in vision</b> and the subject "
    "of &sect;1's table.",
    "<b>Stability</b> — a tiny change in the image produces a huge "
    "change in the recovered scene. <b>This is the condition that "
    "silently ruins working systems</b>: the answer is unique, the solver "
    "reports success, and the result is noise.",
    "<b>Stability is the condition-number problem arriving for a third "
    "time</b> (CSCE 620 Module 01's robust predicates, CSCE 669 "
    "Module 05's convergence rate). <b>A near-degenerate configuration "
    "yields a unique answer with enormous error bars</b> — and "
    "Module 04's pure-rotation failure, where the essential matrix is "
    "unrecoverable because the baseline is zero, is exactly this. <b>The "
    "practical consequence is that you must report a conditioning "
    "estimate alongside every geometric estimate</b>, which working "
    "pipelines do and student code typically does not."]),
  ("code", """# A pinhole camera projects a 3D point to pixels by
#     u = f * X / Z,    v = f * Y / Z
#
# Scale the ENTIRE SCENE by k:
#     u' = f * (kX) / (kZ) = f * X / Z = u
#
# THE IMAGE IS BIT-IDENTICAL. Scene scale is unrecoverable
# from any number of images taken by a camera whose motion
# is itself unmeasured. Structure from motion returns
# geometry up to an unknown global scale, and that is not a
# limitation of the algorithm -- it is a property of
# perspective projection.
#
# TO FIX THE SCALE, something must be measured:
#     a known object size in the scene
#     a known camera baseline (a calibrated stereo rig)
#     an inertial measurement unit (visual-inertial odometry)
#     an active depth sensor
#
# This is why monocular SLAM drifts in scale, and why every
# phone AR system fuses the camera with the IMU rather than
# relying on vision alone."""),
  ("p", "<b>Scale ambiguity is a theorem, not an engineering "
        "shortcoming.</b> It is worth internalising early, because a great "
        "deal of time is lost trying to recover from a single camera "
        "something that provably is not there — and because the "
        "correct response (measure one thing) is cheap once the situation "
        "is understood."),

  ("break",),
  ("h1", "3 &nbsp; The four strategies"),
  ("ul", ["<b>More measurements.</b> More viewpoints, more light "
          "directions, more frames over time. <b>Modules 04 through "
          "07</b> — and it is the <b>only strategy with provable "
          "guarantees</b>: two calibrated views in general position "
          "determine depth up to scale, and that is a theorem rather than "
          "an empirical finding.",
          "<b>Known structure.</b> Calibrated intrinsics, a planar scene, "
          "a rigid object, a printed target of known geometry. "
          "<b>Modules 02 and 03</b> — cheap when available, and the "
          "reason calibration is worth doing carefully rather than "
          "approximately.",
          "<b>Physical assumptions.</b> Brightness constancy, Lambertian "
          "reflectance, small inter-frame motion, smooth surfaces. "
          "<b>Modules 06 and 07</b> — powerful and nearly free, and "
          "<b>each assumption is precisely a failure mode</b>: optical "
          "flow fails on a specular surface because brightness constancy "
          "fails there, and knowing the assumption predicts the failure "
          "exactly.",
          "<b>Learned priors.</b> What scenes are plausible, learned from "
          "a large collection of them. <b>Modules 08 through 11</b> "
          "— <b>the only strategy that addresses semantic questions "
          "at all</b> ('is that a door?' is not a geometric question), and "
          "<b>the only one with no guarantees whatsoever</b>.",
          "<b>These are ordered by how much they can be trusted and "
          "inversely by how much they can do</b>, which is the trade this "
          "course negotiates from beginning to end. <b>A working system "
          "uses all four</b>, and the engineering judgement is about which "
          "part of the problem to give to which."]),
  ("callout", "A prior is not cheating, and it is not optional",
   ["<b>Because the inversion is under-determined, choosing an answer "
    "<i>requires</i> a preference over scenes.</b> There is no neutral "
    "selection from an infinite set of equally consistent explanations.",
    "<b>Methods described as assumption-free have implicit priors</b> "
    "— surface smoothness, Lambertian reflectance, general position, "
    "the absence of degenerate configurations. <b>These are no less "
    "assumptions for being unstated</b>, and being unstated makes them "
    "harder to test rather than weaker.",
    "<b>A learned prior is an explicit and measurable version of the same "
    "thing.</b> Its genuine advantage over a hand-written assumption is "
    "not that it is more accurate but that <b>you can measure where it "
    "holds</b>, by evaluating on data drawn from a different distribution "
    "(Module 12).",
    "<b>Which is exactly why Module 12 is about distribution shift.</b> "
    "<b>A prior is as good as the match between its training "
    "distribution and the scene in front of you</b> — and that match "
    "is a measurable quantity rather than something to be assumed, which "
    "makes it the central evaluation question for any learned vision "
    "component (CSCE 633 Module 12's discipline, applied to perception)."]),

  ("h1", "4 &nbsp; The shape of the course"),
  ("callout", "Where this course goes",
   ["<b>Modules 02 through 07 are geometric vision.</b> Projective "
    "geometry and camera models, calibration, feature correspondence, "
    "two-view and multi-view geometry, bundle adjustment, dense stereo, "
    "and motion estimation. <b>Well-conditioned where its assumptions "
    "hold, provably correct, and the basis of every camera-tracking and "
    "mapping system that ships in a product.</b>",
    "<b>Modules 08 through 10 are learned vision.</b> Convolutional "
    "features and transfer, detection and segmentation with their "
    "metrics, vision transformers, and self-supervised pretraining. "
    "<b>These answer the semantic questions geometry cannot "
    "touch</b> — identity, category, affordance — and offer no "
    "guarantees.",
    "<b>Module 11 is where the two meet.</b> Neural radiance fields and "
    "Gaussian splatting reconstruct a scene by <i>optimising a renderer "
    "against photographs</i> — <b>CSCE 647's forward model used as "
    "a loss function, with CSCE 669's gradient methods as the "
    "optimiser</b>. It is the clearest single demonstration in this "
    "program of why the forward and inverse subjects belong in the same "
    "track.",
    "<b>Modules 12 and 13 are about what you can claim.</b> Evaluation "
    "under distribution shift, benchmark pathologies, latency, "
    "calibration drift, and deployment. <b>The same closing discipline as "
    "every course in this program</b>, in the form it takes when the "
    "system's input is the physical world."]),
 ],
 "resources": [
   ("Szeliski &mdash; Computer Vision, chapter 1 (free PDF)",
    "https://szeliski.org/Book/",
    "<b>The framing of &sect;1</b> and a survey of the whole subject, "
    "with a good history section."),
   ("Belhumeur, Kriegman & Yuille &mdash; The Bas-Relief Ambiguity "
    "(free)",
    "https://link.springer.com/article/10.1023/A:1008154927611",
    "<b>The proved ambiguity from &sect;1's table</b>, and worth reading "
    "as an example of establishing that something is impossible."),
   ("Marr &mdash; Vision (1982), chapter 1",
    "https://mitpress.mit.edu/9780262514620/vision/",
    "<b>Where the inverse-problem framing of this module originates.</b> "
    "Dated in its specifics and still the clearest statement of the "
    "problem. Library copy."),
   ("Hartley & Zisserman &mdash; Multiple View Geometry, chapter 1 "
    "(free sample)",
    "https://www.robots.ox.ac.uk/~vgg/hzbook/",
    "The projective-geometry preview, which Module 02 develops "
    "properly."),
 ],
 "exercises": [
   "<b>Photograph two objects of very different sizes</b> so that they "
   "occupy identical image regions. Report the depths and sizes.",
   "<b>Photograph a dark object in sunlight and a light object in "
   "shade</b> and measure the pixel intensities. Confirm the "
   "confusion.",
   "<b>Render the same scene twice with all coordinates scaled by 2</b>, "
   "using your CSCE 647 renderer, and diff the images.",
   "Confirm they are bit-identical, and explain why in one sentence.",
   "<b>Photograph a specular surface from two viewpoints</b> and track "
   "where the highlight moves relative to the texture.",
   "<b>Find a photograph where you cannot tell whether a surface is "
   "curved or painted</b>, and state what extra measurement would "
   "settle it.",
   "<b>Take any five vision methods you have heard of</b> and classify "
   "each by which of the four strategies it uses.",
   "<b>For each, name the assumption that constitutes its failure "
   "mode.</b>",
   "<b>Find a paper claiming an assumption-free method</b> and identify "
   "its implicit prior.",
   "<b>Write down, before the course proceeds, what you expect a camera "
   "to be able to measure about a scene.</b> Keep it and revisit after "
   "Module 07.",
 ],
 "selfcheck": [
   "Why is the inverse of rendering not a function?",
   "Name six single-image ambiguities and what resolves each.",
   "Prove the scale ambiguity in two lines.",
   "Why does every phone AR system use an inertial sensor?",
   "Name Hadamard's three conditions and say which dominates in "
   "vision.",
   "Which form of ill-posedness silently ruins working systems, and "
   "why?",
   "List the four strategies in order of trustworthiness.",
   "Why is a prior unavoidable rather than a shortcut?",
 ],
},

]

for _b in ("c753_b2", "c753_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
