# -*- coding: utf-8 -*-
"""CSCE 650 — Modules 03-07."""

MODULES = [

# =========================================================== MODULE 03 ======
{
 "n": 3,
 "title": "Stereo Rendering",
 "subtitle": "Two views, and the several ways to get them wrong.",
 "question": "How do you render correctly for two eyes?",
 "outcomes": [
     "Construct asymmetric view frusta for an HMD.",
     "Explain why IPD must be the user's and not a default.",
     "Identify the standard stereo errors and their symptoms.",
     "Explain how UI and effects must be handled in stereo.",
     "Explain what the runtime supplies and what you must not override.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The geometry",
   "blurb": "Not two cameras pointed slightly inward."},

  {"t": "callout", "title": "Do not toe in the cameras",
   "kind": "The classic first mistake",
   "body": ["The intuitive construction rotates each eye's camera inward to "
            "converge on a point. <b>This is wrong</b>, and it is what "
            "stereo photography did badly for a century.",
            "<b>Toe-in introduces vertical disparity</b> that increases "
            "toward the corners of the image — the two eyes see points at "
            "different heights.",
            "<b>The eyes cannot fuse vertical disparity.</b> The result is "
            "strain, and at the edges, double vision.",
            "<b>The correct construction keeps both view directions "
            "parallel</b> and makes the <i>projection</i> asymmetric. Same "
            "convergence effect, no vertical disparity."]},

  {"t": "eq", "kicker": "Off-axis", "title": "Asymmetric frustum projection",
   "eqs": [
     ("eye_pos = head_pos ± (IPD/2) · right",
      "The two eye positions, offset along the head's right vector. "
      "Directions stay parallel."),
     ("left, right, top, bottom  —  all four differ per eye",
      "The frustum is not symmetric about the view axis. The runtime "
      "supplies these; it knows the optics."),
     ("tan(θ_left) ≠ tan(θ_right)",
      "That asymmetry is the whole of stereo. It is also why you cannot "
      "build the projection from a single FOV number."),
   ],
   "caption": "Parallel view directions, asymmetric frusta. Ask the runtime "
              "for the projection rather than constructing one.",
   "note": "The practical instruction is: take the matrices OpenXR gives "
           "you. Students who build their own get it subtly wrong."},

  {"t": "callout", "title": "IPD is a measurement, not a constant",
   "kind": "Why it matters",
   "body": ["Interpupillary distance ranges roughly <b>52 to 78 mm</b> "
            "across adults, and is smaller in children.",
            "<b>Too wide, and the world appears miniature</b> — the user "
            "feels like a giant and distances read as closer than intended.",
            "<b>Too narrow, and the world appears gigantic</b>, and "
            "distances stretch.",
            "<b>Users rarely identify the problem</b>, only that something "
            "feels off and their eyes tire. <b>Use the value the runtime "
            "reports</b>, which comes from the headset's own measurement or "
            "the user's setting."]},

  {"t": "section", "label": "Part 2", "title": "Common errors",
   "blurb": "What each one feels like from the inside."},

  {"t": "table", "kicker": "Errors", "title": "Stereo mistakes and their symptoms",
   "header": ["Error", "Symptom"],
   "widths": [4.4, 7.7],
   "rows": [
     ["<b>Toed-in cameras</b>", "<b>Eye strain; doubling at the edges</b>"],
     ["Wrong IPD", "World scale feels wrong; fatigue"],
     ["<b>Swapped eyes</b>", "<b>Depth inverted; deeply unpleasant</b>"],
     ["Effect in one eye only", "Binocular rivalry (Module 02)"],
     ["<b>UI at zero disparity</b>", "<b>UI appears at infinity; conflicts with occluders</b>"],
     ["Shared view-dependent effect", "Reflections sit at the wrong depth"],
   ],
   "footnote": "<b>Swapped eyes is worth experiencing once</b> — it is "
               "unmistakable, and it teaches you how much stereo is doing.",
   "note": "Have them deliberately induce each one. Reading about the "
           "symptoms is much weaker than feeling them."},

  {"t": "callout", "title": "UI in stereo must have a depth",
   "kind": "The most common application bug",
   "body": ["A flat overlay composited identically into both eyes has "
            "<b>zero disparity</b>, which the brain reads as <i>infinitely "
            "far away</i>.",
            "<b>But it is drawn on top of everything</b>, including objects "
            "that are near. So it is simultaneously behind everything and in "
            "front of everything.",
            "<b>The brain cannot resolve that</b>, and the result is "
            "strain and an unplaceable discomfort users cannot describe.",
            "<b>Put UI in the world, at a real depth</b> — typically 1 to "
            "2 m — and let it be occluded. Head-locked 2D overlays are "
            "the wrong instinct carried over from flat screens."]},

  {"t": "bullets", "kicker": "Effects", "title": "What must be computed per eye",
   "items": [
     "<b>Anything view-dependent:</b> specular highlights, reflections, "
     "refraction, parallax-mapped surfaces. Each eye has its own view "
     "vector.",
     "",
     "<b>Screen-space effects</b> — SSAO, screen-space reflections — "
     "which are per-eye by construction and may disagree at silhouettes.",
     "",
     "<b>Billboards and impostors</b>, which must face the head rather "
     "than either eye, or they disagree.",
     "",
     "<b>Not:</b> shadow maps, lightmaps, most of the shading setup. "
     "Sharing these is the main source of the per-eye savings in "
     "Module 10.",
   ],
   "note": "The shareable/non-shareable split is exactly what stereo "
           "instancing exploits."},

  {"t": "section", "label": "Part 3", "title": "Scale and comfort",
   "blurb": "Getting the world the right size."},

  {"t": "callout", "title": "Scale errors are invisible on a monitor and obvious in VR",
   "kind": "Why assets need rework",
   "body": ["On a flat screen, a room that is 20% too large reads as a room. "
            "<b>In VR the user has a body and compares against it.</b>",
            "<b>Doorways, stairs, chairs, and tables are the giveaways</b> "
            "— everyone has precise expectations for these and none for "
            "a spaceship corridor.",
            "<b>So build to real dimensions</b>, in metres, and check "
            "against a known object placed in the scene.",
            "<b>Assets authored for flat screens are frequently wrong</b>, "
            "because nobody noticed. Measuring them is part of porting."]},

  {"t": "bullets", "kicker": "Comfort", "title": "Stereo-specific comfort rules",
   "items": [
     "<b>Nothing closer than ~20 cm</b> — fusion fails (Module 02).",
     "",
     "<b>Avoid large disparities at the field edges</b>, where the frame "
     "cuts an object the two eyes see differently. The 'window violation' "
     "of stereo photography.",
     "",
     "<b>Avoid rapid depth changes</b> in the thing the user is looking "
     "at; vergence takes time.",
     "",
     "<b>Keep the horizon level.</b> A tilted horizon fights the "
     "vestibular system directly and is strongly nauseating.",
     "",
     "<b>Never move the horizon</b> without the user's head moving.",
   ],
   "footnote": "The horizon rules matter more than their brevity suggests "
               "— Module 07 explains why."},

  {"t": "callout", "title": "Take the matrices the runtime gives you",
   "kind": "The practical instruction",
   "body": ["<b>OpenXR reports, per frame and per eye:</b> the pose, the "
            "four frustum angles, and the recommended render target size.",
            "<b>These account for the optics, the IPD, the lens geometry, "
            "and any per-device calibration.</b> You cannot reconstruct "
            "them from a field-of-view number.",
            "<b>Overriding them is almost always a mistake</b>, and it is "
            "how applications end up with subtly wrong stereo that nobody "
            "can diagnose.",
            "<b>The legitimate exception is reducing render target "
            "resolution</b> for performance (Module 10) — which the "
            "runtime supports explicitly."]},
 ],
 "takeaways": [
   "Do not toe in the cameras: it produces vertical disparity the eyes "
   "cannot fuse. Keep view directions parallel and make the frusta "
   "asymmetric.",
   "IPD varies from about 52 to 78 mm. Wrong values make the world feel "
   "miniature or gigantic, and users report only that something is off.",
   "Swapped eyes, one-eye effects, and zero-disparity UI are the standard "
   "bugs; each has a recognisable symptom.",
   "UI composited identically into both eyes reads as infinitely distant "
   "while drawing on top of everything — put it in the world at 1–2 m.",
   "View-dependent and screen-space effects must be computed per eye; "
   "shadow maps and most shading setup can be shared, which is what stereo "
   "instancing exploits.",
   "Build to real dimensions in metres. Scale errors invisible on a monitor "
   "are obvious to a user who has a body to compare against.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The geometry of stereo"),
  ("callout", "Do not toe in the cameras",
   ["The intuitive construction places a camera at each eye and rotates both "
    "inward so their axes converge on a point of interest. <b>This is "
    "wrong</b>, and it is the mistake stereo photography made for most of a "
    "century before the geometry was properly understood.",
    "<b>Toeing in introduces vertical disparity.</b> Rotating the two "
    "projections about different vertical axes means a point in the world "
    "projects to different <i>heights</i> in the two images, and the "
    "discrepancy grows toward the corners.",
    "<b>The visual system cannot fuse vertical disparity.</b> It is "
    "equipped to handle horizontal disparity — that is what stereopsis "
    "is — and has no mechanism for vertical. The result is strain "
    "across the field and frank double vision near the edges.",
    "<b>The correct construction keeps the two view directions exactly "
    "parallel and makes the projection asymmetric instead.</b> This is "
    "'off-axis' or 'parallel asymmetric frustum' projection, it produces the "
    "same convergence, and it introduces no vertical disparity at all."]),
  ("eq", "eye<sub>L,R</sub> = head &plusmn; (IPD/2) &middot; right"),
  ("p", "The two eye positions are offset along the head's right vector, "
        "and both look in the same direction. What differs is the "
        "<b>frustum</b>: the left, right, top, and bottom planes are not "
        "symmetric about the view axis, and all four differ between the "
        "eyes. <b>That asymmetry is the whole of stereo rendering</b>, and "
        "it is why a projection matrix cannot be built from a single "
        "field-of-view number as it can on a flat screen."),
  ("callout", "IPD is a measurement, not a constant",
   ["Interpupillary distance varies from roughly <b>52 to 78 mm</b> across "
    "the adult population, and is smaller in children. The mean is around "
    "63 mm, which is the value hard-coded into a great deal of software that "
    "should not have hard-coded it.",
    "<b>Too wide and the world appears miniature.</b> Greater separation "
    "produces greater disparity for the same scene, which the brain "
    "interprets as the scene being smaller and nearer — the user feels "
    "like a giant looking at a model.",
    "<b>Too narrow and the world appears gigantic</b>, with distances "
    "stretched and everything feeling slightly unreal.",
    "<b>Users almost never identify the problem.</b> They report that "
    "something feels off, that the space is strange, or simply that their "
    "eyes are tired. <b>Use the IPD the runtime reports</b>, which comes "
    "either from the headset's own measurement hardware or from the user's "
    "configured setting — and never substitute an average."]),

  ("h1", "2 &nbsp; The standard errors"),
  ("table", ["Error", "Symptom from the inside"],
   [["<b>Toed-in cameras</b>",
     "Eye strain building over a minute or two; doubling of objects near "
     "the edges of the field. &sect;1."],
    ["<b>Wrong IPD</b>",
     "The world is the wrong size, in a way the user cannot name. Fatigue."],
    ["<b>Swapped eyes</b>",
     "<b>Depth is inverted</b> — near objects appear far and vice "
     "versa, fighting every monocular cue. <b>Deeply unpleasant and "
     "unmistakable</b>, and worth inducing deliberately once, because it "
     "demonstrates how much work stereopsis is doing."],
    ["<b>An effect rendered into one eye</b>",
     "Binocular rivalry (Module 02 &sect;3) — the image alternates "
     "unstably."],
    ["<b>UI at zero disparity</b>",
     "<b>See below.</b> The most common application-level stereo bug."],
    ["<b>A view-dependent effect computed once and shared</b>",
     "Reflections and highlights sit at the wrong depth, so a mirror reads "
     "as a painting of a mirror."]],
   [0.26, 0.74]),
  ("callout", "UI must have a depth",
   ["A flat interface element composited identically into both eye buffers "
    "has <b>zero disparity</b>. The visual system reads zero disparity as "
    "<i>infinitely distant</i>.",
    "<b>But the element is drawn on top of everything</b>, including objects "
    "a few centimetres from the face. So it is simultaneously the furthest "
    "thing in the scene by disparity and the nearest by occlusion.",
    "<b>These two cues are among the strongest the visual system has, and "
    "they are in direct contradiction.</b> The brain cannot resolve it. The "
    "result is eye strain and a diffuse discomfort that users consistently "
    "fail to attribute to the interface.",
    "<b>Put interface elements in the world, at a genuine depth</b> "
    "— 1 to 2 m is comfortable and near the display's focal distance "
    "(Module 02) — and allow them to be occluded by nearer geometry. "
    "<b>Head-locked two-dimensional overlays are an instinct carried over "
    "from flat screens</b>, and they are one of the clearest markers of an "
    "application designed without VR in mind."]),
  ("ul", ["<b>Compute per eye:</b> anything view-dependent — specular "
          "highlights, reflections, refraction, parallax-occlusion mapping "
          "— because each eye has its own view vector and the "
          "difference between them is real information the brain uses.",
          "<b>Compute per eye:</b> screen-space effects such as ambient "
          "occlusion and screen-space reflections. They are per-eye by "
          "construction, and they can disagree at silhouettes in ways that "
          "are visible; this is a known limitation rather than a bug to "
          "fix.",
          "<b>Orient billboards and impostors to the head</b>, not to either "
          "eye. Facing one eye's position makes them visibly disagree; "
          "facing the head makes them consistent and very slightly wrong for "
          "both, which is correct.",
          "<b>Share:</b> shadow map generation, lightmap baking, most "
          "culling, animation and skinning, and the majority of the shading "
          "setup. <b>This shareable fraction is exactly what stereo "
          "instancing and multiview exploit</b> (Module 10), and it is why "
          "two eyes cost considerably less than twice one."]),

  ("break",),
  ("h1", "3 &nbsp; Scale"),
  ("callout", "Scale errors are invisible on a monitor and obvious in VR",
   ["On a flat screen, a room modelled 20% too large simply reads as a room. "
    "There is no reference; the viewer has no body in the scene and no "
    "expectation to violate.",
    "<b>In VR the user has a body, and compares everything against it "
    "continuously and involuntarily.</b> They know how tall they are and how "
    "far they can reach, and the comparison is automatic.",
    "<b>Doorways, stair risers, chair seats, table heights, and door "
    "handles are the giveaways</b> — everyone has precise, "
    "unconsciously held expectations for these. Nobody has an expectation "
    "for the dimensions of a spaceship corridor, which is why invented "
    "environments tolerate scale error better than ordinary ones.",
    "<b>So build to real dimensions, in metres</b>, and keep a known "
    "object — a correctly sized doorway, or a human figure — in "
    "the scene while working. <b>Assets authored for flat screens are "
    "frequently wrong</b>, because nobody had any reason to notice, and "
    "measuring them is a necessary part of porting anything to VR."]),
  ("ul", ["<b>Place nothing closer than about 20 cm</b> — binocular "
          "fusion fails below that and the image doubles (Module 02).",
          "<b>Avoid large disparities at the edges of the field.</b> When "
          "the edge of the display cuts an object that the two eyes see "
          "differently, the conflict between the occluding frame and the "
          "stereo depth is uncomfortable. Stereo photography calls this a "
          "<i>window violation</i>, and the same geometry applies here.",
          "<b>Avoid rapid depth changes in whatever the user is attending "
          "to.</b> Vergence is a physical eye movement and takes time "
          "— forcing repeated large changes is tiring.",
          "<b>Keep the horizon level.</b> A tilted horizon conflicts "
          "directly with the vestibular system's own sense of down, and it "
          "is among the most reliably nauseating things you can do "
          "(Module 07).",
          "<b>Never move the horizon without the user's head moving.</b> "
          "The same rule, stated for the dynamic case, and it rules out a "
          "great many effects that are unremarkable on a flat screen."]),
  ("callout", "Take the matrices the runtime gives you",
   ["<b>OpenXR reports, per frame and per eye:</b> the eye pose, the four "
    "frustum half-angles, and the recommended render-target dimensions.",
    "<b>Those values account for the lens geometry, the display position, "
    "the user's configured IPD, and any per-device factory "
    "calibration.</b> They cannot be reconstructed from a published "
    "field-of-view figure, and they differ between units of the same "
    "model.",
    "<b>Overriding them is almost always a mistake.</b> It is the usual "
    "origin of applications with subtly incorrect stereo — the kind "
    "where users report fatigue and nobody can find a cause, because every "
    "individual component appears correct.",
    "<b>The legitimate exception is reducing the render target "
    "resolution</b> for performance, which the runtime supports explicitly "
    "and which Module 10 covers. Scaling the resolution is fine; "
    "substituting your own projection is not."]),
 ],
 "resources": [
   ("LaValle &mdash; Virtual Reality, Chapter 7 (free)",
    "http://lavalle.pl/vr/",
    "Visual rendering for VR, including the off-axis projection derivation "
    "of &sect;1."),
   ("Stanford EE267 &mdash; stereo rendering lecture and assignment (free)",
    "https://web.stanford.edu/class/ee267/",
    "Builds the asymmetric frustum from scratch. Do the assignment; it makes "
    "the geometry concrete."),
   ("OpenXR specification &mdash; view configuration and projection (free)",
    "https://registry.khronos.org/OpenXR/",
    "What the runtime actually supplies, and in what coordinate conventions. "
    "The authority for &sect;3's instruction."),
   ("Paul Bourke &mdash; calculating stereo pairs (free)",
    "https://paulbourke.net/stereographics/stereorender/",
    "The clearest short explanation of why toe-in is wrong, with diagrams."),
 ],
 "exercises": [
   "Construct asymmetric frusta from the runtime's reported angles and "
   "verify your projection matrices against the ones it supplies.",
   "Deliberately implement toe-in stereo. Experience it, and measure the "
   "vertical disparity at the image corners.",
   "Set the IPD 10 mm too wide and 10 mm too narrow. Write down what each "
   "does to apparent world scale.",
   "<b>Swap the eye buffers</b> and experience inverted depth. This is worth "
   "doing exactly once.",
   "Build a UI panel as a head-locked zero-disparity overlay, then as a "
   "world-space panel at 1.5 m. Compare the comfort over two minutes each.",
   "Render a reflective sphere with the reflection computed from one eye and "
   "shared. Describe where the reflection appears to sit.",
   "Build a room to real measured dimensions, then rebuild it 20% larger. "
   "Have someone else judge which is correct without being told.",
   "Place a door, a chair, and a staircase at correct dimensions and "
   "deliberately wrong ones, and record which error is noticed fastest.",
   "Tilt the horizon by 5 degrees and experience it for thirty seconds. Stop "
   "when uncomfortable.",
 ],
 "selfcheck": [
   "Why is toe-in wrong, and what does it introduce that the eyes cannot "
   "handle?",
   "Describe the correct stereo construction in one sentence.",
   "What is the range of human IPD, and what do wrong values do?",
   "Give six stereo errors and the symptom of each.",
   "Why does zero-disparity UI cause strain, and what is the fix?",
   "What must be computed per eye, and what can be shared?",
   "Why are scale errors obvious in VR and invisible on a monitor?",
   "Give five stereo comfort rules.",
   "What does the runtime supply, and what is the one legitimate thing to "
   "override?",
 ],
},

# =========================================================== MODULE 04 ======
{
 "n": 4,
 "title": "Display Optics and Distortion",
 "subtitle": "What the lens does, and what you must undo.",
 "question": "Why does the rendered image look nothing like the submitted "
             "one?",
 "outcomes": [
     "Explain why HMDs need lenses at all.",
     "Explain barrel and pincushion distortion and the correction order.",
     "Explain chromatic aberration correction.",
     "Explain why distortion must happen after timewarp.",
     "Name the display artefacts and their causes.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Why a lens",
   "blurb": "The display is 3 cm from your eye."},

  {"t": "callout", "title": "You cannot focus on a screen 3 cm away",
   "kind": "The problem the lens solves",
   "body": ["The nearest an adult eye can focus is roughly <b>10 cm</b>, and "
            "it is uncomfortable well before that. A headset display sits "
            "<b>3 to 5 cm</b> from the eye.",
            "<b>The lens makes the display appear to be at 1.5 to 2 m</b>, "
            "where the eye is relaxed.",
            "<b>It also magnifies</b>, so a small panel fills a wide field "
            "of view — which is the other reason it is there.",
            "<b>And it introduces distortion, chromatic aberration, and a "
            "fixed focal plane</b>, which are Modules 04 and 02's problems "
            "respectively. The lens creates as many problems as it "
            "solves."]},

  {"t": "two", "kicker": "Distortion", "title": "Barrel and pincushion",
   "lh": "The lens produces pincushion",
   "l": ["Magnification increases with distance from the axis.",
         "Straight lines bow <b>inward</b> at the edges.",
         "<b>A property of the optics</b> — unavoidable.",
         ("Worse with wider fields of view.", 1)],
   "rh": "So you render barrel",
   "r": ["Pre-distort the image the opposite way.",
         "Straight lines bow <b>outward</b> in the submitted frame.",
         "<b>The two cancel</b>, and the user sees straight lines.",
         ("Which is why a raw VR frame looks wrong on a monitor.", 1)],
   "note": "The 'raw frame looks wrong' point is how students first "
           "encounter this, usually in a screenshot."},

  {"t": "callout", "title": "Chromatic aberration is corrected per channel",
   "kind": "Three distortions, not one",
   "body": ["A lens refracts different wavelengths by different amounts, so "
            "red, green, and blue focus at slightly different "
            "magnifications.",
            "<b>Uncorrected, this appears as coloured fringing</b> at the "
            "edges of the field — a red or blue halo on high-contrast "
            "edges.",
            "<b>The correction applies a slightly different distortion mesh "
            "to each colour channel.</b>",
            "<b>It is never perfect</b>, which is why you can still see "
            "fringing at the extreme edges of most headsets if you look for "
            "it."]},

  {"t": "section", "label": "Part 2", "title": "Where distortion happens",
   "blurb": "And why the order is not negotiable."},

  {"t": "code", "kicker": "Order", "title": "The compositor pipeline",
   "lang": "text", "code": """
  APPLICATION                          COMPOSITOR (the runtime)
  -----------                          ------------------------
  1. predict head pose
  2. render left eye   ---------->
  3. render right eye  ---------->     4. take the LATEST head pose
     (submit undistorted,                 (newer than step 1's)
      flat, linear images)             5. TIMEWARP: reproject the
                                          submitted image to it
                                       6. apply LENS DISTORTION
                                          (per colour channel)
                                       7. scan out to the display

  *** DISTORTION MUST COME AFTER TIMEWARP. ***
  Timewarp is a rotation in the undistorted image space. Applying
  it to an already-distorted image warps the distortion itself,
  and the correction no longer matches the lens.
""",
   "caption": "You submit flat, undistorted images. The compositor owns "
              "steps 4 to 7, and the ordering is the reason.",
   "note": "This slide answers 'why can't I just do the distortion myself' "
           "— which students ask, and the answer is timewarp."},

  {"t": "callout", "title": "Do not implement your own distortion",
   "kind": "The practical rule",
   "body": ["<b>The distortion mesh is device-specific and sometimes "
            "unit-specific</b>, derived from factory calibration of the "
            "actual lenses.",
            "<b>It must compose correctly with timewarp</b>, which the "
            "compositor applies after you are finished.",
            "<b>And it changes with eye relief and IPD</b> — the "
            "correction depends on where the eye actually is.",
            "<b>Submit flat undistorted images and let the runtime do "
            "it.</b> Early VR required applications to distort; OpenXR "
            "exists partly so they no longer have to."]},

  {"t": "section", "label": "Part 3", "title": "Consequences for rendering",
   "blurb": "Distortion is not free, and it changes pixel density."},

  {"t": "callout", "title": "Distortion compresses the periphery",
   "kind": "Where your pixels go",
   "body": ["Barrel pre-distortion <b>stretches the centre and compresses "
            "the edges</b> of the submitted image.",
            "<b>So peripheral pixels you rendered are thrown away</b> "
            "— several submitted pixels collapse into one displayed "
            "pixel at the edges.",
            "<b>And central pixels are stretched</b>, so the submitted "
            "image must be rendered <i>larger</i> than the display to keep "
            "the centre sharp.",
            "<b>That is why the recommended render target exceeds the panel "
            "resolution</b>, often by 30–40%. You are rendering extra "
            "pixels so that the centre survives the warp."]},

  {"t": "bullets", "kicker": "Exploit it", "title": "Techniques that follow",
   "items": [
     "<b>Radial density masking:</b> skip rendering the corners entirely "
     "— they are outside the visible lens area.",
     "",
     "<b>A stencil mesh</b> supplied by the runtime marks the pixels that "
     "will never be seen. Free performance; apply it.",
     "",
     "<b>Fixed foveated rendering</b> (Module 10) reduces shading rate "
     "toward the edges, which the distortion is going to compress anyway.",
     "",
     "<b>Lower-resolution periphery</b> matches both the distortion and "
     "the eye's acuity falloff (Module 02). The two agree, which is "
     "convenient.",
   ],
   "footnote": "The hidden area mesh is the single easiest VR performance "
               "win and is frequently left unapplied."},

  {"t": "table", "kicker": "Artefacts", "title": "Display artefacts and their causes",
   "header": ["Artefact", "Cause"],
   "widths": [3.6, 8.5],
   "rows": [
     ["<b>Screen door</b>", "Visible gaps between pixels; fill factor"],
     ["<b>Mura</b>", "<b>Per-pixel brightness variation; panel manufacturing</b>"],
     ["God rays", "<b>Internal reflection in Fresnel lenses; bright on dark</b>"],
     ["Chromatic fringing", "Imperfect aberration correction at the edges"],
     ["Pupil swim", "<b>Distortion is wrong when the eye moves off-axis</b>"],
     ["Glare, ghosting", "Lens surface reflections"],
   ],
   "footnote": "<b>God rays are why dark scenes with bright highlights are "
               "a poor choice</b> on Fresnel-lens headsets.",
   "note": "Pupil swim is the subtle one — distortion is calibrated for a "
           "fixed eye position and the eye rotates."},

  {"t": "callout", "title": "Pupil swim, and why eye tracking helps",
   "kind": "The residual error",
   "body": ["<b>The distortion correction is calibrated for the eye at one "
            "position</b> — looking straight ahead, at a nominal eye "
            "relief.",
            "<b>When the eye rotates, the pupil moves</b>, and the "
            "correction is no longer exactly right.",
            "<b>The world appears to warp slightly as you look around</b> "
            "— subtle, and a real contributor to the sense that something "
            "is not quite solid.",
            "<b>Eye tracking allows dynamic distortion correction</b>, "
            "adjusting the mesh for the current gaze. This is one of the "
            "less-discussed benefits of eye tracking and may matter more "
            "than foveated rendering."]},
 ],
 "takeaways": [
   "A lens is needed because the eye cannot focus at 3 cm; it also "
   "magnifies, and it introduces distortion, aberration, and a fixed focal "
   "plane.",
   "The lens produces pincushion distortion, so the application's image is "
   "pre-distorted with barrel distortion and the two cancel.",
   "Chromatic aberration is corrected with a slightly different mesh per "
   "colour channel, and never perfectly.",
   "Distortion must be applied <i>after</i> timewarp, because timewarp "
   "operates in undistorted image space — which is why the compositor "
   "owns it.",
   "Pre-distortion compresses the periphery and stretches the centre, which "
   "is why the recommended render target exceeds the panel resolution.",
   "Apply the runtime's hidden-area stencil mesh — it is the easiest "
   "VR performance win and is routinely left on the table.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Why there is a lens"),
  ("callout", "The eye cannot focus on a display 3 cm away",
   ["The near point of accommodation — the closest distance an eye can "
    "bring into focus — is roughly 10 cm for a young adult and recedes "
    "with age. Focusing near that limit is effortful and uncomfortable well "
    "before reaching it.",
    "<b>A headset display sits 3 to 5 cm from the eye.</b> Without optics it "
    "would be an unfocusable blur.",
    "<b>The lens forms a virtual image at 1.5 to 2 m</b>, where the eye is "
    "relaxed and can comfortably remain for long periods. <b>It also "
    "magnifies</b>, so a panel a few centimetres across subtends a field of "
    "view around 100&deg; — which is the other reason it is there, and "
    "arguably the more important one.",
    "<b>And it introduces distortion, chromatic aberration, a fixed focal "
    "plane, and several named artefacts.</b> The lens creates roughly as "
    "many problems as it solves, and this module is about the ones that fall "
    "to software."]),
  ("table", ["", "What the lens does", "What you do about it"],
   [["<b>Distortion</b>",
     "Magnification increases with distance from the optical axis, so "
     "straight lines bow inward. This is <b>pincushion</b> distortion, and "
     "it is worse at wider fields of view.",
     "<b>Pre-distort the submitted image with the inverse — barrel "
     "distortion.</b> The two cancel and the user sees straight lines. This "
     "is why a raw VR frame looks visibly warped when viewed on a monitor, "
     "which is how most people first encounter the subject."],
    ["<b>Chromatic aberration</b>",
     "Different wavelengths refract by different amounts, so red, green, and "
     "blue are magnified slightly differently. Uncorrected, high-contrast "
     "edges near the periphery acquire coloured fringes.",
     "<b>Apply a slightly different distortion mesh per colour "
     "channel.</b> The correction is never exact, which is why fringing "
     "remains faintly visible at the extreme edges of most headsets if you "
     "look for it deliberately."]],
   [0.15, 0.42, 0.43]),

  ("h1", "2 &nbsp; Where distortion happens, and why the order matters"),
  ("code", """APPLICATION                     COMPOSITOR (the runtime)
1. predict head pose
2. render left eye  ------->
3. render right eye ------->    4. take the LATEST head pose
   (flat, undistorted,             (newer than step 1's)
    linear images)              5. TIMEWARP to that pose
                                6. apply LENS DISTORTION (per channel)
                                7. scan out

DISTORTION MUST COME AFTER TIMEWARP."""),
  ("callout", "Why distortion cannot be applied by the application",
   ["<b>Timewarp operates in undistorted image space.</b> It is, in "
    "essence, a rotation of the rendered image to account for how the head "
    "has moved since the frame was rendered (Module 06). That rotation is "
    "only meaningful on an image with a straightforward projective "
    "relationship to the world.",
    "<b>Applying timewarp to an already-distorted image warps the "
    "distortion itself.</b> The barrel correction is no longer the exact "
    "inverse of the lens's pincushion, so the cancellation fails and the "
    "user sees residual warping that varies with head motion — which is "
    "both visible and nauseating.",
    "<b>So the ordering is forced:</b> the application submits flat, "
    "undistorted images; the compositor reprojects them to the newest "
    "available pose, and only then applies the lens correction.",
    "<b>This is the answer to 'why can I not do the distortion myself'</b>, "
    "which is a reasonable question with a specific answer."]),
  ("ul", ["<b>The distortion mesh is device-specific and sometimes "
          "unit-specific</b>, derived from factory calibration of the "
          "individual lenses. You do not have the data and should not want "
          "it.",
          "<b>It must compose correctly with timewarp</b>, which the "
          "compositor applies after your frame is submitted.",
          "<b>It varies with eye relief and IPD</b>, because the required "
          "correction depends on where the eye actually sits relative to the "
          "lens.",
          "<b>Submit flat undistorted images and let the runtime handle "
          "it.</b> The first generation of VR SDKs required applications to "
          "perform their own distortion, and the resulting inconsistency is "
          "part of why OpenXR exists."]),

  ("break",),
  ("h1", "3 &nbsp; What distortion does to your pixels"),
  ("callout", "The periphery is compressed and the centre is stretched",
   ["Barrel pre-distortion maps the submitted image onto the display "
    "non-uniformly: <b>the centre is stretched outward and the edges are "
    "compressed inward</b>.",
    "<b>So peripheral pixels you rendered are discarded.</b> Several "
    "submitted pixels near the edge collapse into a single displayed pixel "
    "— all the shading work that produced them is thrown away.",
    "<b>And central pixels are magnified.</b> One submitted pixel near the "
    "centre covers more than one displayed pixel, so if the submitted image "
    "matched the panel resolution the centre of the view — where the "
    "user is looking — would be soft.",
    "<b>This is why the runtime's recommended render target exceeds the "
    "panel resolution</b>, frequently by 30 to 40% in each dimension. You "
    "are deliberately rendering surplus pixels so that the centre survives "
    "the warp at full sharpness, and accepting that the periphery's surplus "
    "is wasted."]),
  ("ul", ["<b>Radial density masking</b> skips rendering the extreme corners "
          "of the submitted image, which fall outside the visible lens area "
          "entirely and are never displayed under any circumstances.",
          "<b>The runtime supplies a hidden-area stencil mesh</b> marking "
          "exactly those pixels. Rendering with it bound costs nothing and "
          "saves a meaningful fraction of the fragment work. <b>It is the "
          "single easiest performance win in VR and it is routinely left "
          "unapplied</b>, usually because nobody knew it existed.",
          "<b>Fixed foveated rendering</b> (Module 10) reduces the shading "
          "rate toward the edges of the image — which the distortion is "
          "about to compress anyway, so much of the detail would have been "
          "discarded regardless.",
          "<b>The distortion's compression and the eye's acuity falloff "
          "(Module 02) agree.</b> Both say that peripheral detail is worth "
          "less, which is convenient: one optimisation satisfies two "
          "independent arguments."]),
  ("table", ["Artefact", "Cause", "What to do"],
   [["<b>Screen door effect</b>",
     "Visible dark gaps between pixels — a consequence of fill factor "
     "and of magnifying the panel.",
     "Nothing in software. It diminishes with panel density, and modern "
     "headsets have largely overcome it."],
    ["<b>Mura</b>",
     "Per-pixel variation in brightness and colour arising from panel "
     "manufacturing, magnified along with everything else.",
     "Corrected by a calibration map in the runtime. Visible on uniform "
     "dark fields, which is one reason to avoid large flat dark areas."],
    ["<b>God rays</b>",
     "<b>Internal reflection between the concentric steps of a Fresnel "
     "lens</b>, producing radial streaks from bright objects.",
     "<b>Avoid bright objects on dark backgrounds</b> — white text on "
     "black is the worst case. This is a genuine content constraint on "
     "Fresnel-lens headsets."],
    ["<b>Chromatic fringing</b>",
     "Imperfect aberration correction, worst at the field edges.",
     "Nothing; it is residual error in the runtime's correction."],
    ["<b>Pupil swim</b>",
     "<b>The distortion correction assumes a fixed eye position; the eye "
     "rotates.</b>", "See below."],
    ["<b>Glare and ghosting</b>",
     "Reflections from the lens surfaces.",
     "Reduce extreme contrast; the rest is hardware."]],
   [0.17, 0.42, 0.41]),
  ("callout", "Pupil swim, and the case for eye tracking",
   ["<b>The distortion correction is calibrated for the eye in one "
    "position</b> — looking straight ahead at a nominal eye relief.",
    "<b>When the eye rotates to look at something off-centre, the pupil "
    "moves</b>, and the geometry the correction assumed no longer holds. The "
    "correction is then slightly wrong, in a way that changes as the gaze "
    "changes.",
    "<b>The world appears to warp subtly as you look around.</b> It is "
    "faint, most people cannot describe it, and it is a genuine contributor "
    "to the impression that a virtual space is not quite solid — one of "
    "those effects that is below the threshold of articulation and above the "
    "threshold of perception.",
    "<b>Eye tracking permits dynamic distortion correction</b>, adjusting "
    "the mesh for the current pupil position. <b>This is one of the "
    "less-discussed benefits of eye tracking and arguably matters more than "
    "foveated rendering</b>, because it improves the experience rather than "
    "merely the frame rate."]),
 ],
 "resources": [
   ("Stanford EE267 &mdash; optics and distortion lectures and assignment "
    "(free)",
    "https://web.stanford.edu/class/ee267/",
    "Builds the distortion correction from the lens equation and has you "
    "implement it. The best free treatment of this module."),
   ("LaValle &mdash; Virtual Reality, Chapter 4 (free)",
    "http://lavalle.pl/vr/",
    "Light and optics, including the aberrations and why Fresnel lenses "
    "behave as they do."),
   ("Oculus &mdash; asynchronous timewarp and the compositor (free "
    "developer blog archive)",
    "https://developers.meta.com/horizon/blog/",
    "Why the compositor owns distortion, written when the decision was "
    "being made."),
   ("OpenXR &mdash; visibility mask extension (free)",
    "https://registry.khronos.org/OpenXR/",
    "The hidden-area mesh of &sect;3. Short specification, immediate "
    "benefit."),
 ],
 "exercises": [
   "Take a screenshot of a submitted VR frame before distortion and view it "
   "on a monitor. Describe the barrel warping.",
   "Implement barrel distortion as a post-process on a flat image and verify "
   "that applying pincushion afterwards recovers the original.",
   "Implement per-channel chromatic correction on a test image with "
   "high-contrast edges, and measure the residual fringing at the corners.",
   "Deliberately apply distortion before a simulated timewarp rotation and "
   "show that the correction no longer cancels.",
   "Compare the runtime's recommended render target size against the "
   "headset's panel resolution and compute the ratio.",
   "<b>Apply the hidden-area stencil mesh</b> and measure the fragment work "
   "saved. Report the percentage.",
   "Render white text on black and look for god rays. Then render the same "
   "text dark-on-light and compare.",
   "Look at a uniform dark grey field in a headset and look for mura.",
   "Look at the extreme edge of the field while keeping your head still, and "
   "then rotate only your eyes. Try to detect pupil swim.",
 ],
 "selfcheck": [
   "Why does a headset need a lens? Give two reasons.",
   "What distortion does the lens produce, and what do you render to cancel "
   "it?",
   "How is chromatic aberration corrected, and why is it imperfect?",
   "Why must distortion be applied after timewarp?",
   "Give three reasons not to implement your own distortion.",
   "What does pre-distortion do to peripheral and central pixels, and what "
   "follows for render target size?",
   "What is the hidden-area mesh and why should you always use it?",
   "Name five display artefacts and their causes.",
   "What is pupil swim, and what fixes it?",
 ],
},

# =========================================================== MODULE 05 ======
{
 "n": 5,
 "title": "Tracking",
 "subtitle": "Knowing where the head is, continuously and without drift.",
 "question": "How does the system know where you are?",
 "outcomes": [
     "Explain what an IMU measures and why it drifts.",
     "Explain sensor fusion and the role of each sensor.",
     "Compare inside-out and outside-in tracking.",
     "Explain prediction and why it is necessary.",
     "Explain tracking failure modes and how to handle them.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The IMU",
   "blurb": "Fast, and it drifts."},

  {"t": "table", "kicker": "Sensors", "title": "What an IMU actually measures",
   "header": ["Sensor", "Measures", "Problem"],
   "widths": [2.8, 4.4, 4.9],
   "rows": [
     ["<b>Gyroscope</b>", "Angular <i>velocity</i>", "<b>Integrate once → drift</b>"],
     ["<b>Accelerometer</b>", "Linear acceleration + gravity", "<b>Integrate twice → drift fast</b>"],
     ["Magnetometer", "Magnetic field direction", "Distorted by metal, speakers"],
   ],
   "footnote": "<b>None of them measures position.</b> Position has to be "
               "inferred, and the inference accumulates error.",
   "note": "The 'integrate twice' point explains why position tracking "
           "needs cameras and orientation nearly does not."},

  {"t": "callout", "title": "Double integration is why position drifts so fast",
   "kind": "The arithmetic",
   "body": ["<b>Orientation comes from integrating angular velocity "
            "once.</b> A small bias accumulates linearly — degrees per "
            "minute.",
            "<b>Position comes from integrating acceleration twice.</b> A "
            "small bias accumulates <i>quadratically</i> — and gravity is "
            "a 9.8 m/s² signal you must subtract perfectly.",
            "<b>An accelerometer bias of 0.01 m/s² gives half a metre of "
            "error in ten seconds.</b>",
            "<b>So inertial position tracking alone is hopeless</b>, and "
            "every system corrects it with an optical reference. The IMU "
            "provides the <i>rate</i>; the cameras provide the <i>truth</i>."]},

  {"t": "section", "label": "Part 2", "title": "Fusion",
   "blurb": "Fast and drifting, plus slow and absolute."},

  {"t": "two", "kicker": "Complementary", "title": "The two halves",
   "lh": "IMU",
   "l": ["<b>1000 Hz</b>, latency under a millisecond.",
         "Smooth, no jitter.",
         "<b>Drifts</b> — no absolute reference.",
         ("Tells you how you are moving right now.", 1)],
   "rh": "Optical (cameras)",
   "r": ["<b>30–90 Hz</b>, tens of milliseconds of latency.",
         "Noisy, and can fail entirely.",
         "<b>Absolute</b> — no drift.",
         ("Tells you where you actually are, late.", 1)],
   "note": "The complementarity is exact: each sensor's weakness is the "
           "other's strength. That is what makes fusion work so well."},

  {"t": "callout", "title": "The fusion principle",
   "kind": "How the two are combined",
   "body": ["<b>Use the IMU for high-frequency motion</b> — it is fast, "
            "smooth, and correct over short intervals.",
            "<b>Use the optical estimate to correct low-frequency drift</b> "
            "— it is slow and absolute.",
            "<b>A complementary filter is the simple version</b>; an "
            "extended or unscented Kalman filter is the usual production "
            "answer, estimating sensor biases as part of the state.",
            "<b>The output is better than either sensor alone</b> by a wide "
            "margin, which is the standard result for complementary sensors "
            "and the reason every tracking system looks like this."]},

  {"t": "table", "kicker": "Topology", "title": "Inside-out and outside-in",
   "header": ["", "Outside-in", "Inside-out"],
   "widths": [2.6, 4.6, 4.9],
   "rows": [
     ["Cameras", "Fixed in the room", "<b>On the headset</b>"],
     ["Tracks", "Markers on the headset", "<b>Features in the room</b>"],
     ["Accuracy", "<b>Higher; well-conditioned</b>", "Good; depends on the room"],
     ["Setup", "<b>Base stations required</b>", "<b>None</b>"],
     ["Play space", "Bounded by the stations", "<b>Unbounded</b>"],
     ["Fails when", "Occluded by your body", "<b>Blank walls; poor light</b>"],
   ],
   "footnote": "Inside-out won on convenience. The failure modes are "
               "different, not absent.",
   "note": "The blank-wall failure is worth knowing: a featureless white "
           "room is genuinely hard for inside-out tracking."},

  {"t": "section", "label": "Part 3", "title": "Prediction",
   "blurb": "Rendering for where the head will be."},

  {"t": "callout", "title": "You must render for the future",
   "kind": "Why prediction is not optional",
   "body": ["By the time a frame reaches the display, the pose used to "
            "render it is <b>tens of milliseconds old</b> (Module 06).",
            "<b>So the runtime predicts</b> where the head will be at the "
            "moment of photon emission, and you render for that pose.",
            "<b>Short-horizon prediction is remarkably accurate</b>, "
            "because heads have mass and cannot change direction "
            "instantly — 20 to 40 ms ahead is reliable.",
            "<b>Beyond that it degrades</b>, and overshoot during direction "
            "changes produces a characteristic swimming sensation. This is "
            "the limit on how much latency prediction can hide."]},

  {"t": "bullets", "kicker": "Using it", "title": "Prediction in practice",
   "items": [
     "<b>Ask the runtime for the pose at the predicted display time</b>, "
     "not for the current pose. OpenXR's API is built around this.",
     "",
     "<b>Use the same predicted pose for both eyes and for all rendering "
     "in the frame.</b> Mixing poses within a frame produces inconsistency.",
     "",
     "<b>Late latching</b> reads the pose as late as possible — after "
     "the CPU work, just before the GPU needs it.",
     "",
     "<b>Do not predict further than necessary.</b> Longer horizons mean "
     "larger errors, and timewarp (Module 06) handles the residual better "
     "than prediction does.",
   ],
   "note": "The 'same pose for everything in the frame' rule catches people "
           "who query the pose per object."},

  {"t": "callout", "title": "Tracking loss must be handled, not ignored",
   "kind": "The design requirement",
   "body": ["<b>Tracking will fail.</b> Occlusion, a featureless wall, "
            "direct sunlight, a user covering a camera with their hand.",
            "<b>Snapping the view to a default pose is the worst possible "
            "response</b> — an unrequested instantaneous viewpoint change "
            "is maximally disorienting.",
            "<b>Degrade gracefully:</b> fall back to orientation-only "
            "tracking, hold the last known position, and fade the world out "
            "if it persists.",
            "<b>Tell the user.</b> A clear indication that tracking is lost "
            "is far better than a world that behaves inexplicably."]},

  {"t": "bullets", "kicker": "Failure", "title": "What makes tracking fail",
   "items": [
     "<b>Featureless surfaces.</b> A blank white wall gives inside-out "
     "tracking nothing to lock onto.",
     "",
     "<b>Poor or changing light.</b> Cameras need photons; a dark room is "
     "hard and a flickering one is worse.",
     "",
     "<b>Repetitive texture.</b> A tiled floor or a regular brick wall "
     "produces false matches.",
     "",
     "<b>Moving environments.</b> A train, a car, or a boat — the IMU "
     "reports the vehicle's acceleration as the head's.",
     "",
     "<b>Occlusion of controllers</b> behind the body or outside the camera "
     "field, which is constant in practice.",
   ],
   "footnote": "Vehicles are a genuine unsolved case, and the reason VR on "
               "a train is unpleasant."},
 ],
 "takeaways": [
   "A gyroscope measures angular velocity and an accelerometer measures "
   "acceleration plus gravity. Neither measures position.",
   "Orientation integrates once and drifts linearly; position integrates "
   "twice and drifts quadratically — so inertial position tracking "
   "alone is hopeless.",
   "IMU and cameras are exactly complementary: fast and drifting against "
   "slow and absolute. Fusion is better than either by a wide margin.",
   "Inside-out tracking won on convenience; its failure modes are blank "
   "walls, poor light, and repetitive texture rather than occlusion.",
   "You must render for a predicted future pose. Prediction is reliable to "
   "20–40 ms because heads have mass.",
   "Tracking loss must degrade gracefully — never snap to a default "
   "pose, and tell the user what happened.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The inertial measurement unit"),
  ("table", ["Sensor", "Measures", "Rate", "Problem"],
   [["<b>Gyroscope</b>", "Angular velocity about three axes.",
     "~1000 Hz",
     "<b>Must be integrated once to get orientation</b>, so any bias "
     "accumulates linearly — degrees per minute of drift."],
    ["<b>Accelerometer</b>",
     "Linear acceleration along three axes, <i>including gravity</i>.",
     "~1000 Hz",
     "<b>Must be integrated twice to get position</b>, so bias accumulates "
     "quadratically. Gravity must also be separated out perfectly, and it is "
     "an order of magnitude larger than the signal of interest."],
    ["<b>Magnetometer</b>", "The local magnetic field direction.",
     "~100 Hz",
     "Gives an absolute heading reference — and is distorted by "
     "ferrous metal, speaker magnets, and electrical wiring, which is "
     "everything in an ordinary room."]],
   [0.17, 0.33, 0.12, 0.38]),
  ("callout", "Double integration is why position drifts so quickly",
   ["<b>Orientation requires integrating angular velocity once.</b> A "
    "constant bias of b degrees per second produces an error of b&middot;t "
    "— linear in time, and recoverable with an occasional absolute "
    "reference.",
    "<b>Position requires integrating acceleration twice.</b> A constant "
    "bias b produces an error of &frac12;bt&#178; — quadratic. And "
    "before the first integration, gravity must be subtracted, which "
    "requires knowing the orientation precisely, which has its own error.",
    "<b>Concretely: an accelerometer bias of 0.01 m/s&#178; — a very "
    "good sensor — gives half a metre of position error after ten "
    "seconds</b>, and two metres after twenty.",
    "<b>So purely inertial position tracking is hopeless</b> on any useful "
    "timescale, and every system corrects it against an optical reference. "
    "<b>The IMU supplies the rate; the cameras supply the truth.</b> This "
    "division is the whole architecture of modern tracking."]),

  ("h1", "2 &nbsp; Sensor fusion"),
  ("table", ["", "IMU", "Optical"],
   [["Rate", "<b>~1000 Hz</b>", "30–90 Hz"],
    ["Latency", "<b>Under a millisecond</b>",
     "Tens of milliseconds — exposure, transfer, and feature "
     "extraction all cost time."],
    ["Noise", "Smooth; little jitter.",
     "Noisy, and subject to outright failure."],
    ["Drift", "<b>Accumulates without bound.</b>",
     "<b>None — it is an absolute reference.</b>"],
    ["Tells you", "How you are moving <i>right now</i>.",
     "Where you actually are, <i>somewhat late</i>."]],
   [0.14, 0.38, 0.48]),
  ("callout", "The fusion principle",
   ["<b>The two sensors are exactly complementary:</b> each one's weakness "
    "is the other's strength. This is unusually clean, and it is why "
    "tracking works as well as it does.",
    "<b>Use the IMU for high-frequency motion.</b> Over tens of "
    "milliseconds it is fast, smooth, and accurate, and it is the only thing "
    "that can respond quickly enough for VR.",
    "<b>Use the optical estimate to correct low-frequency drift.</b> It "
    "arrives late and noisily, and it never drifts, so it anchors the "
    "integration.",
    "<b>A complementary filter is the simple implementation</b> — a "
    "high-pass on the IMU and a low-pass on the optical estimate, summed. "
    "<b>An extended or unscented Kalman filter is the production answer</b>, "
    "estimating the sensor biases as part of its state so that the "
    "integration improves over time rather than merely being corrected.",
    "<b>The fused result is substantially better than either sensor "
    "alone</b>, which is the standard outcome for genuinely complementary "
    "sensors and the reason every tracking system in existence has this "
    "shape."]),
  ("table", ["", "Outside-in", "Inside-out"],
   [["Cameras", "Fixed in the room — base stations or sensors.",
     "<b>Mounted on the headset.</b>"],
    ["Tracks", "Markers or emitters on the headset and controllers.",
     "<b>Natural features in the room</b> — essentially SLAM."],
    ["Accuracy", "<b>Higher, and better conditioned</b> — the "
     "geometry is known and fixed.",
     "Good, and dependent on the room having trackable features."],
    ["Setup", "<b>Base stations must be mounted and calibrated.</b>",
     "<b>None.</b> Put the headset on."],
    ["Play space", "Bounded by the base stations' coverage.",
     "<b>Unbounded in principle.</b>"],
    ["Characteristic failure",
     "<b>Occlusion</b> — your own body between the station and a "
     "controller, which happens constantly.",
     "<b>Featureless or repetitive surfaces, and poor light.</b>"]],
   [0.16, 0.42, 0.42]),
  ("p", "<b>Inside-out won on convenience</b>, decisively, once the "
        "computer-vision quality was adequate. Its failure modes are "
        "different rather than absent: a large blank white wall gives it "
        "nothing to track against, and a featureless room is genuinely "
        "difficult in a way that is invisible until you are in one."),

  ("break",),
  ("h1", "3 &nbsp; Prediction"),
  ("callout", "You must render for a future pose",
   ["By the time a rendered frame's photons leave the display, the pose it "
    "was rendered from is <b>tens of milliseconds old</b> — the full "
    "motion-to-photon pipeline of Module 06.",
    "<b>So the runtime predicts.</b> It extrapolates the head's trajectory "
    "to the expected moment of display, and that predicted pose is what you "
    "render from. You are never rendering where the head <i>is</i>.",
    "<b>Short-horizon prediction is remarkably accurate</b>, because a head "
    "is a mass on a neck and cannot change direction instantaneously. "
    "Angular velocity is strongly autocorrelated over short intervals, so "
    "<b>20 to 40 ms ahead is reliable</b> — reliable enough that the "
    "residual error is below perceptual threshold for most motion.",
    "<b>Beyond that it degrades</b>, and the characteristic failure is "
    "overshoot at the moment the head changes direction: the prediction "
    "continues the old motion briefly, and the world appears to swim. "
    "<b>This is the fundamental limit on how much latency prediction can "
    "conceal</b>, and it is why prediction supplements rather than replaces "
    "actually reducing latency."]),
  ("ul", ["<b>Ask the runtime for the pose at the predicted display "
          "time</b>, which is what OpenXR's API is built around — you "
          "pass the target display time and receive the predicted pose. "
          "Asking for 'the current pose' is the wrong question.",
          "<b>Use one predicted pose for the whole frame</b>, for both eyes "
          "and all objects. Querying the pose separately per object produces "
          "objects rendered from slightly different viewpoints, which is "
          "inconsistent in a way that is hard to diagnose.",
          "<b>Late latching</b> defers reading the pose until as late as "
          "possible — after the CPU-side frame setup, immediately "
          "before the GPU needs it — which shortens the prediction "
          "horizon and therefore reduces the prediction error.",
          "<b>Do not predict further ahead than necessary.</b> A longer "
          "horizon means a larger error, and timewarp (Module 06) corrects "
          "residual error more accurately than prediction avoids it, because "
          "timewarp uses a pose measured rather than extrapolated."]),
  ("callout", "Tracking loss must be handled explicitly",
   ["<b>Tracking will fail.</b> A hand over a camera, a user who walks into "
    "a dark corner, direct sunlight saturating a sensor, a controller held "
    "behind the back. This is a normal operating condition, not an "
    "exceptional one.",
    "<b>Snapping the view to a default pose is the worst available "
    "response.</b> An instantaneous, unrequested change of viewpoint is "
    "maximally disorienting and is a reliable way to make someone ill "
    "(Module 07). It is also, unfortunately, the default behaviour of naive "
    "code that simply uses whatever pose it last received.",
    "<b>Degrade gracefully instead:</b> fall back to orientation-only "
    "tracking, which the IMU can sustain for a while; hold the last known "
    "position rather than jumping; and if the loss persists, fade the world "
    "to black rather than showing something wrong.",
    "<b>And tell the user.</b> A clear indication that tracking has been "
    "lost is far better than a world that has begun behaving inexplicably "
    "— people tolerate a known failure and are disturbed by an "
    "unexplained one."]),
  ("ul", ["<b>Featureless surfaces.</b> A large blank white wall offers "
          "inside-out tracking nothing to lock onto.",
          "<b>Poor or changing light.</b> Cameras need photons; a dark room "
          "is hard, and a room with flickering or rapidly changing light is "
          "harder.",
          "<b>Repetitive texture.</b> A regularly tiled floor or a brick "
          "wall produces false feature matches, which can cause the "
          "estimated position to jump by exactly one tile.",
          "<b>Moving environments.</b> In a car, train, or boat, the "
          "accelerometer reports the vehicle's acceleration as the head's, "
          "and the optical system sees a stationary interior. The two "
          "disagree permanently. <b>This is a genuinely unsolved case</b> "
          "and the reason using VR on a train is unpleasant.",
          "<b>Controller occlusion</b> behind the body or outside the "
          "headset cameras' field of view — which with inside-out "
          "tracking happens whenever the user puts their hands at their "
          "sides, draws a bow, or reaches behind their head. Predicted "
          "controller poses bridge short gaps; long ones cannot be hidden."]),
 ],
 "resources": [
   ("LaValle &mdash; Virtual Reality, Chapter 9 (free)",
    "http://lavalle.pl/vr/",
    "Tracking in full: IMU models, drift, filtering, and the mathematics of "
    "fusion. Written by someone who built the Oculus tracker, and the best "
    "free source for this module."),
   ("Stanford EE267 &mdash; IMU and pose tracking assignment (free)",
    "https://web.stanford.edu/class/ee267/",
    "Implement a complementary filter on real IMU data. The drift is far "
    "more convincing when you have watched it accumulate."),
   ("Madgwick &mdash; An efficient orientation filter for IMUs (free)",
    "https://x-io.co.uk/open-source-imu-and-ahrs-algorithms/",
    "A widely used practical fusion filter, with source. A good "
    "implementation target."),
   ("OpenXR &mdash; space and pose prediction (free)",
    "https://registry.khronos.org/OpenXR/",
    "The predicted-display-time API of &sect;3, and the pose validity flags "
    "you need for tracking loss."),
 ],
 "exercises": [
   "Log raw gyroscope data from any device and integrate it. Plot the "
   "orientation drift over five minutes.",
   "Integrate accelerometer data twice to get position and plot the drift "
   "over ten seconds. Compare the growth rate against the gyroscope.",
   "Implement a complementary filter fusing a drifting fast signal with a "
   "noisy slow one, and show the fused result beats both.",
   "In a headset, cover a camera and observe what happens. Then try a blank "
   "wall, a dark room, and a tiled floor.",
   "Measure the practical play-space limits of an inside-out system by "
   "walking until tracking degrades.",
   "Request the pose at the predicted display time and at the current time, "
   "and compare them during head motion. Report the difference in degrees.",
   "Deliberately render from an un-predicted pose and describe the "
   "sensation.",
   "Implement graceful tracking-loss handling: orientation-only fallback, "
   "position hold, and a user-visible indicator. Test by covering a camera.",
   "Use a headset in a moving vehicle, briefly, and document why it fails.",
 ],
 "selfcheck": [
   "What do a gyroscope and accelerometer measure, and which measures "
   "position?",
   "Why does position drift faster than orientation? Give the growth rates.",
   "Compare IMU and optical tracking on rate, latency, noise, and drift.",
   "State the fusion principle and name the usual filters.",
   "Compare inside-out and outside-in on six axes.",
   "Why must you render from a predicted pose, and why is prediction "
   "accurate?",
   "What limits the prediction horizon, and what does overshoot feel like?",
   "Give four rules for using prediction correctly.",
   "Why is snapping to a default pose the worst response to tracking loss?",
   "Name five causes of tracking failure.",
 ],
},

# =========================================================== MODULE 06 ======
{
 "n": 6,
 "title": "Latency",
 "subtitle": "The central problem, and everything built to hide it.",
 "question": "Where do the milliseconds go, and how do you get them back?",
 "outcomes": [
     "Account for every stage of the motion-to-photon budget.",
     "State the latency threshold and what exceeding it does.",
     "Explain timewarp and what it can and cannot correct.",
     "Explain spacewarp and its artefacts.",
     "Measure latency rather than estimating it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The budget",
   "blurb": "Motion to photon, stage by stage."},

  {"t": "table", "kicker": "Pipeline", "title": "Where the milliseconds go",
   "header": ["Stage", "Typical", "Can you reduce it?"],
   "widths": [4.0, 2.4, 5.7],
   "rows": [
     ["Sensor sampling", "1 ms", "No"],
     ["Fusion and pose", "1 ms", "No"],
     ["<b>Application CPU</b>", "<b>2–11 ms</b>", "<b>Yes — this is yours</b>"],
     ["<b>Application GPU</b>", "<b>2–11 ms</b>", "<b>Yes — this is yours</b>"],
     ["Compositor", "1–2 ms", "No"],
     ["<b>Scan-out</b>", "<b>Up to 11 ms</b>", "Higher refresh rate only"],
     ["Pixel response", "1–3 ms", "Panel technology"],
   ],
   "footnote": "<b>Total under 20 ms is the target.</b> Note how much of "
               "it you do not control.",
   "note": "The point of the table is that the application owns maybe half "
           "the budget and must be ruthless with it."},

  {"t": "callout", "title": "20 ms is the threshold, and it is not a preference",
   "kind": "What the research says",
   "body": ["<b>Below roughly 20 ms motion-to-photon, the world feels "
            "attached to the room.</b> Above it, it feels attached to your "
            "head, and lags.",
            "<b>People detect latency differences down to a few "
            "milliseconds</b> in controlled tests, well below the threshold "
            "at which they can describe what is wrong.",
            "<b>And the symptom is not 'it feels laggy'</b> — it is "
            "discomfort, disorientation, and eventually nausea (Module 07).",
            "<b>This single number drove the entire architecture</b> of "
            "modern VR: low persistence, timewarp, prediction, and the "
            "compositor all exist to get under it."]},

  {"t": "section", "label": "Part 2", "title": "Timewarp",
   "blurb": "The most important trick in VR."},

  {"t": "callout", "title": "Reproject the finished frame to a newer pose",
   "kind": "How timewarp works",
   "body": ["The application renders from a pose predicted some "
            "milliseconds ago. <b>Before scan-out, the compositor takes a "
            "fresh pose</b> — much newer — and reprojects the finished "
            "image to it.",
            "<b>For rotation this is nearly exact</b>, because rotating the "
            "view of a distant scene is a simple image warp with no missing "
            "information.",
            "<b>It cuts effective latency enormously</b> — the user's "
            "rotation is reflected with only the compositor's own latency.",
            "<b>And it is why head rotation feels solid even when the "
            "application is struggling.</b> Rotation is the dominant head "
            "motion, so this covers most of the problem."]},

  {"t": "two", "kicker": "Limits", "title": "What timewarp can and cannot fix",
   "lh": "Rotation — handled well",
   "l": ["A pure rotation of the view.",
         "<b>No information is missing</b> — the same scene, seen from "
         "the same point, rotated.",
         "Edges of the field may lack data; the render target is oversized "
         "to cover it.",
         ("Nearly exact.", 1)],
   "rh": "Translation — handled badly",
   "r": ["The head moves to a new <i>position</i>.",
         "<b>Parallax changes</b> — you would see behind objects, and "
         "that data was never rendered.",
         "Requires a depth buffer and still leaves holes.",
         ("Positional timewarp exists and is approximate.", 1)],
   "note": "The rotation/translation asymmetry is the key limitation and "
           "explains why translation latency matters more."},

  {"t": "callout", "title": "Asynchronous timewarp runs whether you finish or not",
   "kind": "The safety net",
   "body": ["<b>ATW runs on its own schedule</b>, in a high-priority "
            "context, and reprojects whatever the most recent complete frame "
            "is.",
            "<b>So a missed frame does not mean a repeated frame.</b> The "
            "old frame is re-warped to the current pose, and head rotation "
            "stays correct.",
            "<b>The world stays stable; moving objects stutter.</b> Which "
            "is a far better failure than the whole world juddering.",
            "<b>It is a safety net, not a licence.</b> Shipping an "
            "application that relies on ATW to hit its rate means every "
            "animation runs at half rate, which users notice."]},

  {"t": "section", "label": "Part 3", "title": "Spacewarp",
   "blurb": "Synthesising frames you did not render."},

  {"t": "callout", "title": "Spacewarp extrapolates motion, with artefacts",
   "kind": "What it costs",
   "body": ["<b>Asynchronous spacewarp generates an entirely new frame</b> "
            "by extrapolating object motion from previous frames, using "
            "motion vectors and depth.",
            "<b>So an application running at 45 Hz can present at 90</b>, "
            "with synthesised alternate frames.",
            "<b>The artefacts are characteristic:</b> wobbling at object "
            "edges, smearing behind fast movers, and disocclusion holes "
            "where background was never rendered.",
            "<b>Supply accurate motion vectors and depth</b> if your engine "
            "can; the quality depends heavily on them. And treat it, again, "
            "as a net rather than a plan."]},

  {"t": "bullets", "kicker": "Reducing", "title": "What actually reduces latency",
   "items": [
     "<b>Hit the frame budget.</b> Everything else is secondary; a missed "
     "frame costs a whole refresh period.",
     "",
     "<b>Late latching:</b> read the pose as late as possible in the frame "
     "(Module 05).",
     "",
     "<b>Shorten the CPU-GPU pipeline.</b> Deep buffering adds a frame of "
     "latency per stage; VR wants a shallow pipeline even at some "
     "throughput cost.",
     "",
     "<b>Avoid temporal effects</b> that need several frames of history "
     "— they add perceived latency even when the timing is correct.",
     "",
     "<b>Higher refresh rate</b> reduces scan-out latency directly.",
   ],
   "footnote": "The deep-pipeline point is the one that surprises people "
               "porting from flat-screen engines."},

  {"t": "callout", "title": "Measure latency; do not estimate it",
   "kind": "How to actually know",
   "body": ["<b>The pendulum method:</b> swing a tracked controller in "
            "front of a camera that sees both the controller and the "
            "display, and count frames between the two.",
            "<b>A photodiode on the display</b> plus an instrumented input "
            "gives a precise electrical measurement.",
            "<b>Some runtimes report it</b> — use it, and verify it "
            "against a physical measurement at least once.",
            "<b>Estimating from frame time is wrong</b>, because it omits "
            "scan-out, pixel response, and the compositor. The usual "
            "estimate is roughly half the true figure."]},
 ],
 "takeaways": [
   "Motion-to-photon latency has seven stages and the application controls "
   "roughly half of them. The target is under 20 ms total.",
   "Below ~20 ms the world feels attached to the room; above it, attached to "
   "the head. The symptom is discomfort, not a perception of lag.",
   "Timewarp reprojects the finished frame to a newer pose. For rotation it "
   "is nearly exact, because no information is missing.",
   "For translation it is not, because parallax changes reveal geometry that "
   "was never rendered — which is why translation latency matters more.",
   "Asynchronous timewarp keeps the world stable through a missed frame; it "
   "is a safety net, and relying on it halves your animation rate.",
   "Measure latency physically. Estimating it from frame time omits "
   "scan-out, pixel response, and the compositor, and understates it by "
   "about half.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The motion-to-photon budget"),
  ("table", ["Stage", "Typical cost", "Under your control?"],
   [["Sensor sampling and readout", "~1 ms", "No."],
    ["Fusion, filtering, pose computation", "~1 ms", "No."],
    ["<b>Application CPU — simulation, culling, draw submission</b>",
     "<b>2–11 ms</b>", "<b>Yes. This is yours.</b>"],
    ["<b>Application GPU — rendering both eyes</b>",
     "<b>2–11 ms</b>", "<b>Yes. This is yours.</b>"],
    ["Compositor — timewarp and distortion", "1–2 ms", "No."],
    ["<b>Scan-out — writing the image to the panel</b>",
     "<b>Up to a full refresh period</b>",
     "Only by increasing the refresh rate."],
    ["Pixel response — the panel physically changing state",
     "1–3 ms", "Panel technology; OLED is faster than LCD."]],
   [0.42, 0.22, 0.36]),
  ("p", "<b>The target is under 20 ms end to end.</b> Notice how much of the "
        "budget the application does not control — which is precisely "
        "why the portion it does control must be managed ruthlessly."),
  ("callout", "20 ms is a threshold, not a preference",
   ["<b>Below roughly 20 ms motion-to-photon, the virtual world feels "
    "attached to the room.</b> You turn your head and the world stays put, "
    "as the real world does.",
    "<b>Above it, the world feels attached to your head</b> and dragged "
    "along behind it. The sensation is distinctive once you have "
    "experienced both.",
    "<b>Controlled experiments find people detecting latency differences "
    "down to a few milliseconds</b> — far below the level at which they "
    "can say what is wrong. Sensitivity substantially exceeds the ability to "
    "describe.",
    "<b>And the symptom is not a perception of lag.</b> Users do not report "
    "'the image is late'; they report feeling unwell, disoriented, or simply "
    "that the experience is unpleasant. <b>The latency is converted into "
    "discomfort</b> by the mechanism in Module 07, which is why it is a "
    "physiological constraint rather than a quality setting.",
    "<b>This one number drove the entire architecture of modern VR:</b> low "
    "persistence displays, timewarp, pose prediction, the separate "
    "compositor process, and the high refresh rates all exist to get under "
    "it."]),

  ("h1", "2 &nbsp; Timewarp"),
  ("callout", "Reproject the finished frame to a newer pose",
   ["The application renders from a pose that was predicted some "
    "milliseconds earlier. <b>Just before scan-out, the compositor takes a "
    "fresh pose — much newer — and reprojects the completed image "
    "to match it.</b>",
    "<b>For rotation this is nearly exact.</b> Rotating the view of a scene "
    "from the same viewpoint is a pure image-space warp: every pixel that "
    "was visible before is still visible, merely in a different place on the "
    "display. No information is missing.",
    "<b>The reduction in effective latency is large.</b> The user's head "
    "rotation is reflected on screen with only the compositor's own latency "
    "— a millisecond or two — rather than the full pipeline's.",
    "<b>This is why head rotation feels solid even when an application is "
    "struggling</b>, and since rotation is by far the dominant component of "
    "head motion, timewarp covers most of the problem. It is the single most "
    "important technique in VR engineering."]),
  ("table", ["", "Rotation", "Translation"],
   [["What changes", "The view direction, from the same point.",
     "The viewpoint itself moves."],
    ["Information needed", "<b>None beyond the rendered image.</b> Every "
     "visible surface is still visible.",
     "<b>Geometry that was occluded before and is visible now</b> — "
     "which was never rendered and does not exist in the frame."],
    ["Quality", "<b>Nearly exact.</b>",
     "<b>Approximate at best.</b> Positional timewarp uses the depth buffer "
     "to reproject, and leaves disocclusion holes that must be filled by "
     "guessing."],
    ["Edge handling", "The field edges may lack data, which is why the "
     "render target is slightly oversized.",
     "Holes appear in the interior of the image, not only at the edges."]],
   [0.17, 0.38, 0.45]),
  ("p", "<b>This asymmetry is the key limitation.</b> It means translation "
        "latency is intrinsically harder to hide than rotation latency "
        "— and it is one reason that applications involving a lot of "
        "positional head movement, such as anything requiring leaning or "
        "crouching, are more demanding than they appear."),
  ("callout", "Asynchronous timewarp is a safety net",
   ["<b>ATW runs on its own schedule</b>, in a high-priority GPU context "
    "that can pre-empt the application, and reprojects whatever the most "
    "recent <i>complete</i> frame is — whether or not the application "
    "has finished a new one.",
    "<b>So a missed frame does not mean a repeated frame.</b> The previous "
    "frame is re-warped to the current head pose, and head rotation remains "
    "correct and smooth even though the content is one frame old.",
    "<b>The world stays stable; moving objects stutter.</b> That is a far "
    "better failure mode than the entire world juddering, because it is the "
    "world's stability relative to the head that the vestibular system cares "
    "about.",
    "<b>It is a safety net and not a licence.</b> An application that "
    "relies on ATW to reach its presentation rate is effectively running its "
    "animation and simulation at half rate, which users notice as stutter in "
    "everything that moves — and it leaves no headroom for the "
    "occasional genuinely expensive frame."]),

  ("break",),
  ("h1", "3 &nbsp; Spacewarp"),
  ("callout", "Synthesising frames, and what it costs",
   ["<b>Asynchronous spacewarp goes further than timewarp:</b> it generates "
    "an entirely new frame by extrapolating the motion of objects within the "
    "scene, using motion vectors and the depth buffer from previous frames.",
    "<b>So an application rendering at 45 Hz can present at 90 Hz</b>, with "
    "every alternate frame synthesised rather than rendered.",
    "<b>The artefacts are characteristic and recognisable once you know "
    "them:</b> wobbling or rippling at the edges of moving objects; smearing "
    "behind fast-moving things; and <b>disocclusion holes</b> where "
    "background is revealed that was never rendered, filled by inpainting "
    "that is sometimes obviously wrong.",
    "<b>Supply accurate motion vectors and depth if your engine can.</b> "
    "The synthesis quality depends heavily on them, and an engine that "
    "provides good motion vectors gets markedly better results. <b>And as "
    "with ATW, treat it as a net rather than a plan</b> — an "
    "application designed around spacewarp is an application with permanent "
    "artefacts."]),
  ("ul", ["<b>Hit the frame budget.</b> Everything else in this list is "
          "secondary, because a missed frame costs an entire refresh period "
          "— more than every other optimisation combined.",
          "<b>Late latching:</b> read the head pose as late as possible in "
          "the frame, after CPU work and immediately before the GPU needs it "
          "(Module 05). This shortens the prediction horizon and therefore "
          "the error.",
          "<b>Shorten the CPU–GPU pipeline.</b> Flat-screen engines "
          "buffer two or three frames deep to maximise throughput, and "
          "<b>each buffered frame is a full refresh period of added "
          "latency</b>. VR wants a shallow pipeline even at some cost in "
          "average throughput. <b>This surprises people porting an existing "
          "engine</b>, because it trades away a tuning decision that was "
          "correct in the original context.",
          "<b>Avoid temporal effects requiring several frames of "
          "history.</b> They add perceived latency even when frame timing is "
          "correct, because the image lags the pose by more than one frame "
          "(Module 02 &sect;3).",
          "<b>A higher refresh rate reduces scan-out latency directly</b>, "
          "which is the one stage outside your control that responds to "
          "anything."]),
  ("callout", "Measure latency; do not estimate it",
   ["<b>The pendulum or high-speed-camera method:</b> swing a tracked "
    "controller in front of a camera positioned to see both the physical "
    "controller and the headset display simultaneously, record at a high "
    "frame rate, and count the frames between the physical motion and the "
    "displayed response. Crude, cheap, and it measures the whole pipeline "
    "including everything you cannot instrument.",
    "<b>A photodiode taped to the display</b>, triggered against an "
    "instrumented input event, gives a precise electrical measurement and is "
    "the method used in published comparisons.",
    "<b>Some runtimes report an estimate.</b> Use it for iteration, and "
    "verify it against a physical measurement at least once — runtime "
    "figures frequently omit scan-out and pixel response.",
    "<b>Estimating latency from frame time is wrong and badly so.</b> Frame "
    "time omits sensor sampling, the compositor, scan-out, and pixel "
    "response — which together are usually as large as the rendering "
    "itself. <b>The frame-time estimate is typically about half the true "
    "figure</b>, which is exactly the kind of error that leads someone to "
    "conclude they are comfortably within budget when they are not."]),
 ],
 "resources": [
   ("Abrash &mdash; Latency: the sine qua non of AR and VR (free)",
    "http://blogs.valvesoftware.com/abrash/latency-the-sine-qua-non-of-ar-and-vr/",
    "<b>Required reading for this module.</b> The clearest account of why "
    "latency matters and what the threshold means."),
   ("LaValle &mdash; Virtual Reality, Chapter 7.4 (free)",
    "http://lavalle.pl/vr/",
    "Timewarp, prediction, and the latency budget, with the mathematics."),
   ("Van Waveren &mdash; The Asynchronous Time Warp for Virtual Reality on "
    "Consumer Hardware (free)",
    "https://dl.acm.org/doi/10.1145/2993369.2993378",
    "The ATW paper of &sect;2, including the GPU pre-emption problem that "
    "made it hard."),
   ("Meta &mdash; Asynchronous Spacewarp documentation (free)",
    "https://developers.meta.com/horizon/documentation/",
    "What spacewarp needs from your application, and the artefacts to "
    "expect."),
 ],
 "exercises": [
   "Account for your own application's latency budget stage by stage, "
   "measuring what you can and citing typical figures for the rest.",
   "<b>Measure motion-to-photon latency physically</b>, with a high-speed "
   "camera or a phone's slow-motion mode. Compare against your estimate from "
   "frame time.",
   "Deliberately add 20 ms of artificial latency and describe the "
   "experience. Then 40 ms. Stop when uncomfortable.",
   "Disable timewarp if your runtime allows it, and compare head rotation "
   "with and without.",
   "Construct a scene with strong parallax and translate your head "
   "laterally, looking for the limits of positional timewarp.",
   "Deliberately miss the frame budget — add GPU work until you drop "
   "to half rate — and observe ATW keeping the world stable while "
   "moving objects stutter.",
   "Trigger spacewarp and photograph the disocclusion artefacts behind a "
   "fast-moving object.",
   "Reduce your engine's pipeline depth from three frames to one and measure "
   "the latency change and the throughput cost.",
   "Compare measured latency at 72 Hz and 90 Hz on the same application.",
 ],
 "selfcheck": [
   "List the seven stages of the motion-to-photon pipeline and say which you "
   "control.",
   "What is the latency threshold, and what is the symptom of exceeding it?",
   "Explain timewarp in one sentence and say why rotation is nearly exact.",
   "Why is translation handled badly, and what does that imply?",
   "What does asynchronous timewarp guarantee, and why is relying on it a "
   "mistake?",
   "What does spacewarp do, and name its three characteristic artefacts.",
   "Give five things that actually reduce latency.",
   "Why does pipeline depth matter more in VR than on a flat screen?",
   "Why is estimating latency from frame time wrong, and by roughly how "
   "much?",
 ],
},

# =========================================================== MODULE 07 ======
{
 "n": 7,
 "title": "Cybersickness",
 "subtitle": "Why people feel ill, and what actually helps.",
 "question": "What makes VR nauseating, and what can you do about it?",
 "outcomes": [
     "Explain sensory conflict theory and its predictions.",
     "Explain vection and why it is the central mechanism.",
     "Identify the specific design choices that provoke sickness.",
     "Explain individual variation and why your tolerance is misleading.",
     "Apply and evaluate the standard mitigations.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "The mechanism",
   "blurb": "Why a visual mismatch produces nausea."},

  {"t": "callout", "title": "Sensory conflict theory",
   "kind": "The standard explanation",
   "body": ["<b>The eyes report motion. The vestibular system reports "
            "none.</b> The brain has two authoritative signals that "
            "disagree.",
            "<b>The leading explanation is evolutionary:</b> historically, "
            "the most common cause of such a conflict was a neurotoxin "
            "affecting the nervous system — and the adaptive response to "
            "suspected poisoning is to vomit.",
            "<b>It explains the predictions well</b> — why passengers are "
            "sicker than drivers, why closing your eyes helps, why "
            "acclimatisation occurs.",
            "<b>It is a theory, not a settled mechanism</b>, and postural "
            "instability theory is a serious competitor. The design "
            "implications are similar either way."]},

  {"t": "callout", "title": "Vection is the specific culprit",
   "kind": "The thing to design against",
   "body": ["<b>Vection is the illusion of self-motion produced by visual "
            "motion</b> — the sensation when the train beside yours "
            "pulls away and you feel yourself moving.",
            "<b>It is strongest in the peripheral field</b>, which is "
            "specialised for motion detection (Module 02).",
            "<b>In VR, any camera motion the user did not initiate "
            "physically produces vection</b> — and the vestibular system "
            "contradicts it.",
            "<b>So: visually induced motion without physical motion is the "
            "core problem</b>, and almost every mitigation in this module "
            "reduces either the vection or the conflict."]},

  {"t": "table", "kicker": "Provocation", "title": "What provokes sickness, worst first",
   "header": ["Provocation", "Why"],
   "widths": [4.2, 7.9],
   "rows": [
     ["<b>Camera motion the user did not cause</b>", "<b>Maximal conflict; no vestibular signal at all</b>"],
     ["<b>Acceleration</b>", "<b>The vestibular system measures acceleration specifically</b>"],
     ["Rotation that is not head rotation", "Worst of all — the semicircular canals are very sensitive"],
     ["<b>Latency and dropped frames</b>", "Module 06 — conflict even when the user moves"],
     ["Tilting or moving the horizon", "Direct conflict with gravity sensing"],
     ["Large peripheral motion", "Maximal vection"],
   ],
   "footnote": "<b>Constant velocity is far less provocative than "
               "acceleration</b> — which is the key to comfortable "
               "locomotion design (Module 08).",
   "note": "The acceleration point is the most actionable item in the whole "
           "module."},

  {"t": "section", "label": "Part 2", "title": "Variation",
   "blurb": "Why you are not a good test subject."},

  {"t": "callout", "title": "Susceptibility varies enormously and systematically",
   "kind": "The data",
   "body": ["<b>Some people are unaffected by experiences that make others "
            "ill within two minutes.</b> The range is very wide.",
            "<b>Known correlates:</b> prior VR experience (acclimatisation "
            "is real and substantial), migraine history, age, and "
            "— reported consistently though the mechanism is "
            "debated — sex.",
            "<b>Acclimatisation is the big one.</b> People who use VR "
            "regularly tolerate far more, and they stop being able to judge "
            "what a novice experiences.",
            "<b>Which is exactly why VR developers ship uncomfortable "
            "VR.</b> You are the most acclimatised person who will ever use "
            "your application."]},

  {"t": "bullets", "kicker": "Testing", "title": "Testing honestly",
   "items": [
     "<b>Test on novices.</b> Someone who has never used VR is the only "
     "person who can tell you what a first experience is like.",
     "",
     "<b>Use a standard questionnaire</b> — SSQ or VRSQ. Free, "
     "validated, and it makes your claims comparable to published work.",
     "",
     "<b>Ask before and after</b>, because some people arrive unwell.",
     "",
     "<b>Report everyone</b>, including the person who stopped after a "
     "minute. <b>Averaging away a dropout is the central dishonesty</b> in "
     "comfort reporting.",
     "",
     "<b>Have a stopping rule and state it.</b> Nobody should be pushed "
     "through discomfort for your data.",
   ],
   "footnote": "The dropout point matters: the person who quit is the most "
               "informative participant you had."},

  {"t": "section", "label": "Part 3", "title": "Mitigation",
   "blurb": "What works, ranked honestly."},

  {"t": "table", "kicker": "What helps", "title": "Mitigations by strength of evidence",
   "header": ["Mitigation", "Effect"],
   "widths": [4.4, 7.7],
   "rows": [
     ["<b>Hit the frame rate; minimise latency</b>", "<b>Strong. The precondition for everything else</b>"],
     ["<b>Avoid unrequested camera motion</b>", "<b>Strong</b>"],
     ["<b>Avoid acceleration; prefer constant velocity</b>", "<b>Strong</b>"],
     ["<b>Teleport rather than smooth locomotion</b>", "<b>Strong (Module 08)</b>"],
     ["Vignette during movement", "Moderate; reduces peripheral vection"],
     ["A stable reference frame — a cockpit, a nose", "Moderate; well supported"],
     ["Snap turning rather than smooth", "Moderate to strong"],
     ["Reduce field of view during motion", "Moderate; same mechanism as vignette"],
     ["A fixed rest frame or grid", "Mixed evidence"],
   ],
   "note": "The top four are the ones that matter. The rest are "
           "refinements and are frequently reached for first."},

  {"t": "callout", "title": "A stable reference frame helps, and is cheap",
   "kind": "The most underused mitigation",
   "body": ["<b>Give the user something that moves with them and does not "
            "move in their view</b> — a cockpit, a vehicle interior, a "
            "virtual nose, a helmet rim.",
            "<b>It provides a visual reference consistent with the "
            "vestibular signal of not moving</b>, which reduces the "
            "conflict.",
            "<b>This is why cockpit games are so much more comfortable</b> "
            "than first-person movement, and the effect is large.",
            "<b>A virtual nose works</b> and sounds absurd. Users do not "
            "consciously notice it, and it measurably helps — your real "
            "nose is always in view and the brain expects it."]},

  {"t": "callout", "title": "Design around it, do not mitigate afterwards",
   "kind": "The ordering",
   "body": ["<b>Vignettes and comfort options are patches.</b> They help, "
            "and they are applied to a design that has already made the "
            "problem.",
            "<b>The comfortable experiences are comfortable by "
            "construction:</b> the user is seated, or stationary, or moving "
            "at constant velocity in a cockpit.",
            "<b>Decide the locomotion model before anything else</b>, "
            "because it determines what the application can be.",
            "<b>And offer options.</b> Given the variation in Part 2, no "
            "single choice suits everyone — comfort settings are an "
            "accessibility feature, not a nicety."]},
 ],
 "takeaways": [
   "Sensory conflict theory: the eyes report motion the vestibular system "
   "does not, and the evolutionary response to that conflict is nausea.",
   "Vection — visually induced self-motion, strongest in the periphery "
   "— is the specific mechanism to design against.",
   "Acceleration provokes far more than constant velocity, because the "
   "vestibular system measures acceleration specifically.",
   "Susceptibility varies enormously, and acclimatisation is real — "
   "which is why developers, the most acclimatised people alive, ship "
   "uncomfortable VR.",
   "The strong mitigations are frame rate, no unrequested camera motion, no "
   "acceleration, and teleport locomotion. Vignettes are refinements.",
   "A stable reference frame — a cockpit or even a virtual nose — "
   "is cheap, well supported, and underused.",
 ],
 "notes": [
  ("h1", "1 &nbsp; The mechanism"),
  ("callout", "Sensory conflict theory",
   ["<b>The eyes report that you are moving. The vestibular system reports "
    "that you are not.</b> The brain receives two signals it has every "
    "reason to trust, and they contradict each other.",
    "<b>The leading explanation for why this produces nausea is "
    "evolutionary.</b> For most of human history, the commonest cause of a "
    "sustained mismatch between visual and vestibular signals was a "
    "neurotoxin disrupting the nervous system — and the adaptive "
    "response to suspected poisoning is to empty the stomach.",
    "<b>It accounts for the observations well.</b> Passengers are sicker "
    "than drivers, because the driver anticipates the motion and has "
    "control. Closing the eyes helps, because it removes one of the "
    "conflicting signals. Acclimatisation occurs, because the brain learns "
    "the conflict is not poison.",
    "<b>It is a theory rather than a settled mechanism.</b> <b>Postural "
    "instability theory</b> — that sickness arises from prolonged "
    "failure to maintain postural control — is a serious competitor "
    "with its own supporting evidence. <b>Fortunately the design "
    "implications are substantially the same either way</b>, so the dispute "
    "does not need resolving in order to build comfortable experiences."]),
  ("callout", "Vection is the specific culprit",
   ["<b>Vection is the illusion of self-motion produced by visual motion "
    "alone.</b> The familiar example is sitting in a stationary train and "
    "feeling yourself move when the train on the adjacent platform pulls "
    "away.",
    "<b>It is strongest in the peripheral visual field</b>, which Module 02 "
    "established is specialised for motion detection rather than detail. "
    "Large, coherent motion across the periphery is the most potent "
    "stimulus.",
    "<b>In VR, any camera motion the user did not physically initiate "
    "produces vection</b> — and the vestibular system flatly "
    "contradicts it, because the user is standing still.",
    "<b>So the core problem is visually induced motion without "
    "corresponding physical motion</b>, and essentially every mitigation in "
    "&sect;3 works by reducing either the strength of the vection or the "
    "size of the conflict."]),
  ("table", ["Provocation", "Why it is provocative"],
   [["<b>Camera motion the user did not cause</b>",
     "<b>Maximal conflict.</b> The visual system reports motion and the "
     "vestibular system reports nothing whatsoever. Cutscenes that move the "
     "camera are the worst case."],
    ["<b>Acceleration rather than constant velocity</b>",
     "<b>The vestibular system measures acceleration specifically</b> "
     "— the semicircular canals measure angular acceleration and the "
     "otoliths linear acceleration. At constant velocity it reports nothing, "
     "so there is far less to contradict. <b>This is the single most "
     "actionable fact in the module</b> and it underlies most of "
     "Module 08."],
    ["<b>Rotation that is not the user's head rotation</b>",
     "The semicircular canals are extremely sensitive to rotation, and "
     "visually rotating the world while the head is still is among the most "
     "reliably sickening things possible."],
    ["<b>Latency and dropped frames</b>",
     "Module 06. These create conflict <i>even when the user is moving "
     "their own head</i>, which is otherwise the safe case."],
    ["<b>Tilting or moving the horizon</b>",
     "The otoliths sense gravity, so the horizon's orientation is directly "
     "contradicted."],
    ["<b>Large coherent motion in the periphery</b>",
     "Maximal vection, per the callout above."]],
   [0.28, 0.72]),

  ("h1", "2 &nbsp; Individual variation"),
  ("callout", "Susceptibility varies enormously, and you are an outlier",
   ["<b>Some people experience no discomfort from content that makes others "
    "ill within two minutes.</b> The range across individuals is very wide "
    "— wider than for almost any other perceptual response you will "
    "design around.",
    "<b>Known correlates include</b> prior VR experience, migraine history, "
    "age, inner-ear conditions, and — reported consistently across "
    "studies, with the mechanism still debated — sex.",
    "<b>Acclimatisation is the largest single factor and the most relevant "
    "one.</b> People who use VR regularly develop substantial tolerance over "
    "weeks, and in doing so they lose the ability to judge what a first-time "
    "user experiences. The adaptation is real, durable, and invisible from "
    "the inside.",
    "<b>Which is exactly why VR developers ship uncomfortable VR.</b> You "
    "spend every working day in a headset. <b>You are, almost by definition, "
    "the most acclimatised person who will ever use your application</b>, "
    "and your judgement of its comfort is therefore the least reliable "
    "available. This is not a failure of care; it is a structural problem "
    "with the role."]),
  ("ul", ["<b>Test on novices.</b> Someone who has never worn a headset is "
          "the only person who can tell you what a first experience is like, "
          "and that experience determines whether most people continue.",
          "<b>Use a standard instrument</b> — the Simulator Sickness "
          "Questionnaire, or the shorter VR Sickness Questionnaire. Both are "
          "free and validated, and using one makes your results comparable "
          "to the published literature rather than being an impression.",
          "<b>Administer it before as well as after.</b> Some participants "
          "arrive with a headache, and without a baseline you will attribute "
          "it to your application.",
          "<b>Report every participant, including the one who stopped after "
          "ninety seconds.</b> <b>Averaging away a dropout is the central "
          "dishonesty in comfort reporting</b> — the person who could "
          "not continue is the most informative participant you had, and "
          "excluding them produces a mean that describes only the people who "
          "tolerated it.",
          "<b>Have an explicit stopping rule and state it in advance.</b> "
          "Participants stop whenever they wish, without explanation, and "
          "nobody is encouraged to continue through discomfort. This is "
          "basic research ethics and it also produces better data."]),

  ("break",),
  ("h1", "3 &nbsp; Mitigation"),
  ("table", ["Mitigation", "Strength of evidence", "Notes"],
   [["<b>Hit the frame rate; minimise latency</b>", "<b>Strong</b>",
     "<b>The precondition for everything else.</b> No comfort technique "
     "compensates for a dropped frame."],
    ["<b>Avoid camera motion the user did not initiate</b>", "<b>Strong</b>",
     "Including cutscenes, forced perspective changes, and snapping on "
     "tracking loss (Module 05)."],
    ["<b>Avoid acceleration; prefer constant velocity</b>", "<b>Strong</b>",
     "If you must accelerate, do it quickly — a short sharp change is "
     "less provocative than a long gentle one, which is counterintuitive and "
     "well supported."],
    ["<b>Teleport rather than smooth locomotion</b>", "<b>Strong</b>",
     "Module 08. The largest single design decision available."],
    ["<b>Vignette during movement</b>", "Moderate",
     "Darkening the periphery reduces vection at its strongest point. "
     "Widely used and genuinely effective."],
    ["<b>A stable reference frame</b>", "Moderate, well supported",
     "See below."],
    ["<b>Snap turning rather than smooth turning</b>", "Moderate to strong",
     "Removes the visually induced rotation that the canals object to most."],
    ["<b>Reduce field of view during motion</b>", "Moderate",
     "The same mechanism as the vignette."],
    ["<b>A fixed rest frame or grid overlay</b>", "<b>Mixed</b>",
     "Studied repeatedly with inconsistent results. Worth trying; do not "
     "assume."]],
   [0.30, 0.20, 0.50]),
  ("callout", "A stable reference frame is cheap and underused",
   ["<b>Give the user something that moves with them and remains stationary "
    "in their view</b> — a cockpit, a vehicle interior, a helmet rim, "
    "the edge of a visor.",
    "<b>It supplies a visual reference consistent with the vestibular "
    "signal</b> — part of the visual field is saying 'you are not "
    "moving relative to this', which is what the inner ear is also saying. "
    "The conflict is reduced rather than merely masked.",
    "<b>This is a large part of why cockpit-based games are so much more "
    "comfortable</b> than free first-person movement, and the effect is "
    "substantial rather than marginal. Driving and flying games were "
    "comfortable in VR years before walking games were.",
    "<b>A virtual nose works.</b> It sounds absurd, users do not "
    "consciously notice it when asked, and it measurably reduces sickness "
    "— presumably because your real nose is always in the visual field "
    "and the brain treats its presence as evidence about self-motion. It is "
    "a few triangles and it is worth trying."]),
  ("callout", "Design around it rather than mitigating afterwards",
   ["<b>Vignettes, comfort modes, and snap turning are patches.</b> They "
    "help genuinely, and every one of them is applied to a design that has "
    "already created the problem they address.",
    "<b>The comfortable experiences are comfortable by construction.</b> The "
    "user is seated; or stationary and the world comes to them; or in a "
    "cockpit moving at constant velocity; or moving by teleport. No patch "
    "was needed because no conflict was created.",
    "<b>Decide the locomotion model first</b>, before art, before mechanics, "
    "before anything. It determines what the application can be, and "
    "changing it later is a redesign rather than an adjustment "
    "(Module 08).",
    "<b>And offer options.</b> Given the variation in &sect;2, no single "
    "choice suits everyone — the comfort settings menu is not a "
    "courtesy but <b>an accessibility feature</b>, and an application with "
    "only one locomotion scheme has excluded part of its audience by "
    "construction."]),
 ],
 "resources": [
   ("LaValle &mdash; Virtual Reality, Chapter 10 (free)",
    "http://lavalle.pl/vr/",
    "VR sickness: the competing theories, the evidence, and the design "
    "implications. The best free treatment."),
   ("Kennedy et al. &mdash; Simulator Sickness Questionnaire (free, widely "
    "reproduced)",
    "https://www.tandfonline.com/doi/abs/10.1207/s15327108ijap0303_3",
    "The standard instrument of &sect;2. Use it rather than inventing your "
    "own scale."),
   ("Meta &mdash; VR comfort and locomotion guidelines (free)",
    "https://developers.meta.com/horizon/resources/",
    "The practical mitigations with the vendor's own testing behind them."),
   ("Rebenitsch & Owen &mdash; Review on cybersickness in applications and "
    "visual displays (free)",
    "https://link.springer.com/article/10.1007/s10055-016-0285-9",
    "A survey of the evidence for &sect;3's mitigations, including which "
    "ones replicate and which do not."),
 ],
 "exercises": [
   "Experience vection deliberately: find a VR scene with large peripheral "
   "motion and stand still. Describe the sensation.",
   "Build a scene with smooth forward movement at constant velocity, and "
   "another with acceleration and deceleration. Compare on six people.",
   "Add a vignette during movement and measure its effect with a "
   "questionnaire rather than by impression.",
   "Add a cockpit or helmet frame and compare comfort against the same "
   "motion without one.",
   "<b>Add a virtual nose</b> and test whether anyone notices it, and "
   "whether comfort scores change.",
   "Implement snap turning and smooth turning and compare across "
   "participants.",
   "Administer an SSQ before and after a five-minute session on six people, "
   "including at least two novices. Report every score.",
   "Tilt the horizon by 10 degrees for ten seconds and record how quickly "
   "participants ask to stop.",
   "Write a comfort settings menu for your Project 2 application and justify "
   "each option from this module.",
 ],
 "selfcheck": [
   "State sensory conflict theory and the evolutionary explanation, and name "
   "its main competitor.",
   "What is vection, where is it strongest, and why does that matter?",
   "Give six provocations in order, and say which fact about them is most "
   "actionable.",
   "Why does acceleration provoke more than constant velocity?",
   "Why is a VR developer a poor judge of their own application's comfort?",
   "Give five rules for testing comfort honestly, and say which is most "
   "often violated.",
   "Rank the mitigations by evidence and name the four that matter most.",
   "Why does a stable reference frame help, and why does a virtual nose "
   "work?",
   "Why should locomotion be decided first, and why are comfort options an "
   "accessibility feature?",
 ],
},

]
