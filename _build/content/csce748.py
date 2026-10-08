# -*- coding: utf-8 -*-
"""CSCE 748 Computational Photography — original course content."""

COURSE = {
    "code": "CSCE 748",
    "title": "Computational Photography",
    "tagline": "What a camera measures, what a photograph is, and the "
               "computation that now sits between them",
    "term": "Semester 4 (with CSCE 650 and CSCE 735)",
    "prereqs": "CSCE 641 Computer Graphics; CSCE 647 helpful for the "
               "radiometry; linear algebra; comfort with signals and "
               "convolution, developed here as needed",
    "effort": "10–12 hours per week · 13 modules + 2 project weeks",
    "deliverable": "An image pipeline you wrote: raw to display, HDR merge, "
                   "alignment, gradient-domain compositing, and a burst "
                   "denoiser — evaluated against ground truth you "
                   "captured yourself",
    "description": [
        "CSCE 647 computed images from a scene description. This course goes "
        "the other way: <b>it starts with measurements and asks what can be "
        "recovered from them</b>. The two are the same mathematics "
        "approached from opposite ends, and several results in this course "
        "are rendering results read backwards.",
        "The organising fact is that <b>a camera does not capture a "
        "photograph; it captures measurements from which a photograph is "
        "computed</b>. That was always true — film had a response curve "
        "and a development process — and it has become overwhelmingly "
        "true. A modern phone photograph is the output of alignment, "
        "merging, demosaicing, tone mapping, and several learned models "
        "operating on a burst of underexposed frames. The button press is "
        "the start of the computation, not the end.",
        "This has a consequence worth stating early: <b>the boundary "
        "between photography and synthesis has become difficult to "
        "locate</b>. A night-mode image shows detail no single exposure "
        "recorded; a portrait-mode image has a depth of field the lens never "
        "had; a learned upscaler produces texture that was never measured. "
        "Module 13 takes that seriously rather than treating it as a "
        "curiosity.",
        "You will implement the pipeline. By the end you will be able to "
        "take a raw file and produce a displayable image through code you "
        "wrote, and explain every decision between the two.",
    ],
    "outcomes": [
        "Explain image formation and what a raw file actually contains.",
        "Implement the core image operations: convolution, pyramids, and "
        "edge-aware filtering.",
        "Recover a camera response curve and merge exposures into an HDR "
        "radiance map.",
        "Implement tone mapping and explain why it is underdetermined.",
        "Implement demosaicing and the raw-to-display pipeline.",
        "Explain deconvolution and why blind deblurring is hard.",
        "Align and composite images robustly.",
        "Apply gradient-domain methods and explain why they work.",
        "Explain light fields and the plenoptic function.",
        "Implement a burst photography pipeline.",
        "Assess learned image methods honestly, including what they invent.",
    ],
    "materials": [
        ("CMU 15-463 Computational Photography — Gkioulekas (free "
         "lectures, slides, assignments)",
         "http://graphics.cs.cmu.edu/courses/15-463/",
         "The primary source. Complete lecture notes and programming "
         "assignments covering most of this course, with unusually careful "
         "treatment of the physics."),
        ("Marc Levoy — Lectures on Digital Photography (free)",
         "https://sites.google.com/site/marclevoylectures/",
         "From the person who led Google's camera work and co-invented light "
         "field photography. Exceptional on optics, exposure, and why the "
         "phone pipeline looks the way it does."),
        ("Szeliski — Computer Vision: Algorithms and Applications, 2nd ed. "
         "(free online)",
         "https://szeliski.org/Book/",
         "Chapters 3, 8, and 9 cover image processing, alignment, and "
         "stitching. The standard reference, free, and the alignment "
         "material for Module 07 is the best there is."),
        ("Georgia Tech CS6475 Computational Photography (free)",
         "https://www.udacity.com/course/computational-photography--ud955",
         "A second voice with more worked examples and a gentler pace. Good "
         "for Modules 03, 04, and 08."),
        ("Reinhard et al. — High Dynamic Range Imaging",
         "https://www.sciencedirect.com/book/9780123749147/",
         "The standard HDR reference. Library copy; the key papers by the "
         "same authors are free and linked per module."),
        ("Hasinoff et al. — Burst photography for high dynamic range and "
         "low-light imaging (free)",
         "https://hdrplusdata.org/",
         "The HDR+ paper, with a full dataset of raw bursts. This is what "
         "your phone does, documented by the people who built it."),
    ],
    "tooling": [
        "<b>Python with NumPy</b> for everything except the inner loops. "
        "This is a course about algorithms on arrays and the language "
        "should not be in the way.",
        "<b>No OpenCV for the core assignments.</b> Convolution, "
        "demosaicing, alignment, and blending are the course; calling a "
        "library function for them teaches nothing. Use it for I/O and for "
        "checking.",
        "<b>rawpy / LibRaw</b> to read raw files, and <b>a camera that "
        "shoots raw</b> — a phone with a raw mode is sufficient and many "
        "have one.",
        "<b>OpenEXR</b> for high dynamic range intermediates. Writing 8-bit "
        "PNG between stages destroys exactly what this course is about.",
        "<b>A tripod</b>, or a stable surface. Several assignments need "
        "aligned exposures, and hand-held alignment is Module 07's problem "
        "rather than Module 03's.",
        "<b>A colour chart</b> if you can get one — even a printed one "
        "helps for white balance and response curve work.",
    ],
    "projects": [
        {"title": "From raw to a displayed image", "after": 7,
         "brief": "The complete classical pipeline, written by you, on "
                  "photographs you took. Everything afterwards builds on "
                  "this, and the discipline of handling linear data "
                  "correctly is the point.",
         "reqs": [
             "A raw decoder path: black level, white balance, demosaic, "
             "colour matrix, and display encoding, each as a separate "
             "inspectable stage.",
             "A camera response curve recovered from a bracketed exposure "
             "sequence you captured.",
             "An HDR radiance map merged from those exposures, with weights "
             "justified.",
             "At least two tone mapping operators, one global and one "
             "local, implemented rather than called.",
             "A panorama from at least five hand-held images, with feature "
             "matching, RANSAC homography, and blending.",
             "Every intermediate stage saved and shown.",
         ],
         "done": [
             "<b>Your raw pipeline's output compared against the camera's "
             "own JPEG</b>, with the differences identified and explained "
             "rather than apologised for.",
             "A recovered response curve plotted against the exposures used "
             "to recover it, with the fit shown.",
             "<b>A tone mapping comparison on the same radiance map</b>, "
             "with an honest statement of what each operator destroyed.",
             "A panorama with no visible seams, plus the same panorama with "
             "naive blending for comparison.",
         ]},
        {"title": "A modern computational pipeline", "after": 12,
         "brief": "Something a phone does, implemented and measured. "
                  "Choose one and do it properly rather than three "
                  "partially.",
         "reqs": [
             "<b>Either</b> a burst denoising pipeline — align, merge, "
             "and denoise a burst of underexposed raws; <b>or</b> a "
             "portrait-mode pipeline — depth estimation and "
             "physically-motivated synthetic defocus; <b>or</b> a "
             "gradient-domain compositing tool with seamless cloning and "
             "a usable interface.",
             "Quantitative evaluation against a ground truth you captured "
             "— a long exposure, a measured depth, or a reference "
             "composite.",
             "A failure analysis: the input on which your implementation "
             "produces a visibly wrong result.",
             "A comparison against a learned method if one is available, "
             "with an honest account of what it does better and what it "
             "invents.",
         ],
         "done": [
             "<b>A quantitative result against ground truth</b> — PSNR, "
             "SSIM, or a task-appropriate measure, with the measurement "
             "method stated.",
             "A figure showing the pipeline stage by stage on one input.",
             "<b>A documented failure with its mechanism explained.</b> "
             "Every pipeline has one.",
             "A written paragraph on which parts of your output were "
             "<i>measured</i> and which were <i>inferred</i>. "
             "<b>Module 13's question, answered for your own work.</b>",
         ]},
    ],
}


MODULES = [

# =========================================================== MODULE 01 ======
{
 "n": 1,
 "title": "What a Camera Measures",
 "subtitle": "The measurement, and everything that is not in it.",
 "question": "What is actually in a raw file?",
 "outcomes": [
     "Describe image formation from scene radiance to stored value.",
     "Explain the exposure triangle in terms of what each control does to "
     "the measurement.",
     "Explain what a raw file contains and what it does not.",
     "Explain noise sources and why they behave as they do.",
     "Explain why linearity matters and where it is lost.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Formation",
   "blurb": "From the scene to a number."},

  {"t": "code", "kicker": "Pipeline", "title": "Scene radiance to stored value",
   "lang": "text", "code": """
  scene radiance  L(x, y, lambda)          [W / m^2 / sr]
        |  lens: aperture, focal length, vignetting, aberration
        v
  image irradiance  E(x, y, lambda)        [W / m^2]
        |  shutter: integrate over exposure time t
        v
  photon count per sensor well             [electrons]
        |  colour filter array: one channel per pixel
        |  quantum efficiency, full well capacity
        v
  analogue voltage
        |  analogue gain (ISO)
        v
  ADC  -->  RAW INTEGER                    [12-14 bits, LINEAR]
        |  demosaic, white balance, colour matrix, tone curve
        v
  display image                            [8 bits, NON-LINEAR]

  *** The raw integer is proportional to photon count. ***
  *** Everything after the ADC is interpretation. ***
""",
   "caption": "The raw value is a measurement. Everything below the ADC "
              "line is a series of choices, and this course is about those "
              "choices.",
   "note": "The measurement/interpretation boundary is the spine of the "
           "whole course. Place it carefully."},

  {"t": "table", "kicker": "Exposure", "title": "What each control actually does",
   "header": ["Control", "Changes", "Side effect"],
   "widths": [2.6, 4.4, 5.1],
   "rows": [
     ["<b>Aperture</b>", "Light gathered per unit time", "<b>Depth of field; diffraction when small</b>"],
     ["<b>Shutter</b>", "Integration time", "<b>Motion blur</b>"],
     ["<b>ISO</b>", "<b>Gain, not light</b>", "<b>Amplifies signal AND noise</b>"],
   ],
   "footnote": "<b>ISO does not make the sensor more sensitive.</b> It "
               "amplifies what was already measured, which is why high ISO "
               "is noisy.",
   "note": "The ISO misconception is near-universal and worth correcting "
           "explicitly."},

  {"t": "callout", "title": "Only two controls change how many photons you collect",
   "kind": "The consequence",
   "body": ["<b>Aperture and shutter time determine the photon count.</b> "
            "ISO does not.",
            "<b>Photon count determines the noise floor</b> (Part 3), so "
            "image quality is set by those two alone.",
            "<b>ISO is a decision about where to put the measurement in the "
            "ADC's range</b> — useful, and not a way to get more "
            "signal.",
            "<b>This is why 'expose to the right' works</b>: collect as "
            "many photons as the highlights permit, because you cannot add "
            "them afterwards."]},

  {"t": "section", "label": "Part 2", "title": "The raw file",
   "blurb": "What is in it, and what is not."},

  {"t": "two", "kicker": "Contents", "title": "Raw and JPEG",
   "lh": "Raw contains",
   "l": ["<b>Linear</b> sensor values, 12–14 bits.",
         "One colour per pixel (the CFA pattern).",
         "<b>No white balance applied</b> — only recorded as metadata.",
         ("Black level, saturation point, colour matrix.", 1),
         "<b>The measurement.</b>"],
   "rh": "JPEG contains",
   "r": ["<b>Non-linear</b>, 8 bits, gamma encoded.",
         "Three colours per pixel, demosaiced.",
         "<b>White balance baked in</b>, irreversibly.",
         ("Tone curve, sharpening, noise reduction applied.", 1),
         "<b>An interpretation.</b>"],
   "note": "The irreversibility of the JPEG decisions is the practical "
           "argument for shooting raw."},

  {"t": "callout", "title": "Linearity is the property that makes everything work",
   "kind": "Why it matters so much",
   "body": ["<b>A raw value of 2000 corresponds to twice the light of "
            "1000.</b> Exactly.",
            "<b>So you can add, average, and scale radiance "
            "meaningfully</b> — which is what HDR merging (Module 03), "
            "burst averaging (Module 10), and every physically-based "
            "operation require.",
            "<b>A gamma-encoded JPEG value does not have this "
            "property.</b> Averaging two gamma-encoded pixels gives the "
            "wrong answer, and the error is not small.",
            "<b>So: do all processing in linear space and encode at the "
            "very end</b> — exactly the rule CSCE 647 Module 13 arrived "
            "at from the rendering side."]},

  {"t": "section", "label": "Part 3", "title": "Noise",
   "blurb": "Where it comes from and how it scales."},

  {"t": "eq", "kicker": "Noise", "title": "The sources, and which dominates",
   "eqs": [
     ("shot noise:  σ = √N",
      "Photon arrival is Poisson. The noise is the square root of the "
      "count — a property of light, not of the sensor."),
     ("SNR = N / √N = √N",
      "So signal-to-noise improves as the square root of photon count. "
      "Four times the light, twice the SNR."),
     ("read noise: constant;  dark current: ∝ time, temperature",
      "Sensor-dependent, and dominant only in very dim conditions or long "
      "exposures."),
   ],
   "caption": "Shot noise dominates in normal conditions and cannot be "
              "engineered away — it is in the light itself.",
   "note": "That shot noise is a property of light rather than of the "
           "sensor surprises people and explains a lot."},

  {"t": "callout", "title": "Shot noise is why low light is hard",
   "kind": "The fundamental limit",
   "body": ["<b>Photons arrive as a Poisson process.</b> Count N on "
            "average, and the standard deviation is √N.",
            "<b>In bright light N is large</b> — 10,000 photons gives an "
            "SNR of 100, and the noise is invisible.",
            "<b>In dim light N is small</b> — 100 photons gives an SNR "
            "of 10, and the noise is the image.",
            "<b>No sensor improvement fixes this</b>, because the noise is "
            "in the light. <b>The only remedy is collecting more "
            "photons</b> — a larger aperture, a longer exposure, or "
            "<i>more frames</i>, which is Module 10's entire premise."]},

  {"t": "bullets", "kicker": "Consequences", "title": "What follows for the rest of the course",
   "items": [
     "<b>Averaging n frames improves SNR by √n</b> — because the "
     "signal adds and the noise adds in quadrature. Module 10.",
     "",
     "<b>Denoising is estimation under a known noise model</b>, not "
     "guesswork. Knowing the noise is Poisson-Gaussian is what makes it "
     "tractable.",
     "",
     "<b>Noise is signal-dependent</b>, so it is stronger in the "
     "highlights and more visible in the shadows.",
     "",
     "<b>Which means denoising must be applied in linear space</b>, before "
     "the tone curve changes the relationship.",
   ],
   "footnote": "Applying denoising after gamma encoding is a common "
               "mistake and produces visibly worse results."},
 ],
 "takeaways": [
   "A raw value is proportional to photon count. Everything after the ADC "
   "— demosaic, white balance, tone curve — is interpretation.",
   "Aperture and shutter change how many photons you collect; ISO is gain "
   "and amplifies signal and noise alike.",
   "Raw is linear, single-channel-per-pixel, and keeps white balance as "
   "metadata; JPEG is encoded, demosaiced, and has every decision baked in.",
   "Linearity is what makes averaging and merging meaningful, which is why "
   "all processing happens in linear space and encoding happens last.",
   "Shot noise is &radic;N because photon arrival is Poisson — it is a "
   "property of light, not of the sensor, and cannot be engineered away.",
   "SNR improves as &radic;N, so averaging n frames gains &radic;n — "
   "which is the entire premise of burst photography.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Image formation"),
  ("code", """scene radiance L(x,y,lambda)    [W/m^2/sr]
   | lens: aperture, focal length, vignetting, aberration
image irradiance E(x,y,lambda)  [W/m^2]
   | shutter: integrate over exposure time
photon count per well           [electrons]
   | colour filter array; quantum efficiency; full well
analogue voltage
   | analogue gain (ISO)
ADC  ->  RAW INTEGER            [12-14 bits, LINEAR]
   | demosaic, white balance, colour matrix, tone curve
display image                   [8 bits, NON-LINEAR]"""),
  ("p", "<b>The raw integer is proportional to photon count.</b> That "
        "proportionality is the measurement, and it is the only thing in the "
        "pipeline that has a defensible claim to being what the camera "
        "<i>saw</i>. <b>Everything below the ADC line is interpretation</b> "
        "— a series of choices about how to turn a measurement into "
        "something that looks right on a screen, and this course is largely "
        "about those choices."),
  ("table", ["Control", "What it changes", "Side effect"],
   [["<b>Aperture</b>", "<b>How much light is gathered per unit time.</b> "
     "A wider aperture collects more.",
     "<b>Depth of field</b> narrows as the aperture widens. And at very "
     "small apertures, <b>diffraction</b> softens the image — so "
     "stopping down past a point loses sharpness rather than gaining it."],
    ["<b>Shutter speed</b>", "<b>How long the sensor integrates.</b> Twice "
     "the time, twice the photons.",
     "<b>Motion blur</b>, from subject movement or camera shake."],
    ["<b>ISO</b>",
     "<b>Analogue gain applied after the measurement.</b> It does not "
     "change how many photons were collected.",
     "<b>Amplifies signal and noise together</b>, so the signal-to-noise "
     "ratio is unchanged or slightly worsened. High ISO is noisy because it "
     "is used in situations where few photons were available, not because "
     "the gain creates noise."]],
   [0.15, 0.37, 0.48]),
  ("callout", "Only two controls change the photon count",
   ["<b>Aperture and shutter time determine how many photons reach the "
    "sensor. ISO does not.</b> This is the most commonly misunderstood fact "
    "in photography, and it has direct consequences for every computational "
    "technique in this course.",
    "<b>Photon count determines the noise floor</b> (&sect;3), so image "
    "quality in the sense that matters — signal-to-noise — is "
    "fixed by aperture and shutter alone.",
    "<b>ISO is a decision about where to place the measurement within the "
    "converter's range.</b> It is genuinely useful — raising gain "
    "before the ADC can keep a dim signal above the quantisation floor and "
    "the read noise — and it is not a way to obtain more signal.",
    "<b>This is why 'expose to the right' is sound advice:</b> collect as "
    "many photons as the highlights will tolerate without clipping, because "
    "photons you did not collect cannot be recovered afterwards by any "
    "amount of processing. A dark raw file brightened later is noisier than "
    "a bright raw file darkened later, and the difference is not subtle."]),

  ("h1", "2 &nbsp; The raw file"),
  ("table", ["", "Raw", "JPEG"],
   [["Values", "<b>Linear</b> in scene radiance, 12–14 bits per "
     "pixel.",
     "<b>Non-linear</b> — gamma or sRGB encoded — 8 bits."],
    ["Colour", "<b>One channel per pixel</b>, in the colour filter array's "
     "pattern (Module 05).", "Three channels per pixel, already "
     "interpolated."],
    ["White balance", "<b>Not applied</b> — recorded in metadata as "
     "multipliers you may use or ignore.",
     "<b>Baked in, irreversibly.</b> Correcting it later means scaling "
     "already-clipped, already-encoded values."],
    ["Also contains", "Black level, saturation point, the sensor's colour "
     "matrix, and the CFA pattern — everything needed to interpret the "
     "numbers.",
     "An embedded profile, and the camera manufacturer's opinion about "
     "sharpening and noise reduction."],
    ["In short", "<b>The measurement.</b>", "<b>An interpretation.</b>"]],
   [0.14, 0.44, 0.42]),
  ("callout", "Linearity is the property everything depends on",
   ["<b>A raw value of 2000 corresponds to exactly twice the light of a "
    "value of 1000.</b> The relationship is proportional, by construction, "
    "because the sensor counts photons and the ADC is linear.",
    "<b>So raw values can be added, averaged, and scaled meaningfully.</b> "
    "Merging exposures into a radiance map (Module 03), averaging a burst to "
    "reduce noise (Module 10), and every physically-motivated operation in "
    "this course require exactly this property.",
    "<b>A gamma-encoded JPEG value does not have it.</b> Averaging two "
    "gamma-encoded pixels does not give the encoding of the average "
    "radiance — the result is systematically wrong, and for "
    "high-contrast pairs it is badly wrong. Half of a bright highlight and "
    "half of a shadow is not what you get.",
    "<b>So: do all processing in linear space, and encode for display at "
    "the very end.</b> This is the identical rule that CSCE 647's Module 13 "
    "arrived at from the rendering direction — the two courses meet "
    "here, and for the same reason."]),

  ("break",),
  ("h1", "3 &nbsp; Noise"),
  ("eq", "shot noise: &sigma; = &radic;N &nbsp;&nbsp;&nbsp;&nbsp; "
         "SNR = N / &radic;N = &radic;N"),
  ("table", ["Source", "Behaviour", "Dominant when"],
   [["<b>Shot noise</b>",
     "Photon arrival is a Poisson process, so the standard deviation of a "
     "count N is &radic;N. <b>A property of light itself.</b>",
     "<b>Essentially always, in normal photography.</b>"],
    ["<b>Read noise</b>",
     "Added by the readout electronics and the ADC. Roughly constant "
     "regardless of signal.",
     "Very dim scenes, where the photon count is small enough that a "
     "constant additive term matters."],
    ["<b>Dark current</b>",
     "Thermally generated electrons, proportional to exposure time and "
     "strongly dependent on temperature.",
     "Long exposures, and warm sensors. Astrophotography subtracts a 'dark "
     "frame' for exactly this."],
    ["<b>Fixed pattern noise</b>",
     "Per-pixel variation in gain and offset. Static, so it can be "
     "calibrated out.",
     "Visible mainly after heavy amplification."]],
   [0.19, 0.44, 0.37]),
  ("callout", "Shot noise is why low light is hard, and it is not the sensor's fault",
   ["<b>Photons arrive as a Poisson process.</b> If the expected count in a "
    "well is N, the standard deviation of the actual count is &radic;N. This "
    "is a statement about light, not about any particular sensor.",
    "<b>In bright light N is large and the relative noise is small.</b> "
    "Ten thousand photons gives a signal-to-noise ratio of 100, and the "
    "noise is invisible.",
    "<b>In dim light N is small and the relative noise is large.</b> A "
    "hundred photons gives an SNR of 10, and the noise is a substantial "
    "fraction of the image. Ten photons gives an SNR of about 3, at which "
    "point the measurement barely constrains anything.",
    "<b>No improvement in sensor technology removes this.</b> A perfect "
    "sensor — one that detected every photon with no read noise "
    "whatsoever — would still produce this noise, because it is in the "
    "signal being measured. <b>The only remedy is collecting more "
    "photons:</b> a wider aperture, a longer exposure, a larger sensor, or "
    "<b><i>more frames</i></b> — which is the entire premise of "
    "Module 10 and of modern phone photography."]),
  ("ul", ["<b>Averaging n frames improves SNR by &radic;n.</b> The signal "
          "adds linearly and the independent noise adds in quadrature, so "
          "the ratio improves as the square root. Four frames is equivalent "
          "to one frame with twice the exposure — without the motion "
          "blur. Module 10.",
          "<b>Denoising is estimation under a known noise model</b> rather "
          "than general-purpose smoothing. Knowing the noise is "
          "Poisson-Gaussian with measurable parameters is what makes "
          "principled denoising possible at all.",
          "<b>Noise is signal-dependent.</b> It is larger in absolute terms "
          "in the highlights (more photons, so more &radic;N) and larger in "
          "relative terms in the shadows (fewer photons, so worse SNR) "
          "— which is why shadows look noisy even though the highlights "
          "carry more noise.",
          "<b>Which means denoising must be applied in linear space</b>, "
          "before any tone curve. A tone curve lifts the shadows and "
          "compresses the highlights, destroying the simple relationship "
          "between signal level and noise level that a denoiser depends on. "
          "<b>Denoising after gamma encoding is a common mistake</b> and "
          "produces visibly worse results for a reason that is easy to "
          "state."]),
 ],
 "resources": [
   ("Marc Levoy &mdash; Lectures on Digital Photography, lectures 1–6 "
    "(free)",
    "https://sites.google.com/site/marclevoylectures/",
    "Image formation, exposure, and sensors, from someone who built camera "
    "pipelines. The clearest treatment of &sect;1 available free."),
   ("CMU 15-463 &mdash; Image formation and the camera pipeline (free)",
    "http://graphics.cs.cmu.edu/courses/15-463/",
    "The lecture notes and the raw-processing assignment, which is "
    "essentially Project 1's first requirement."),
   ("Emil Martinec &mdash; Noise, Dynamic Range and Bit Depth in Digital "
    "SLRs (free)",
    "https://www.photons-to-photos.net/",
    "The clearest explanation of &sect;3 for photographers, with "
    "measurements. The site also publishes measured sensor data."),
   ("Hasinoff &mdash; Photon, Poisson Noise (free chapter)",
    "https://people.csail.mit.edu/hasinoff/pubs/hasinoff-photon-2012-preprint.pdf",
    "The noise model of &sect;3 stated precisely, by one of the HDR+ "
    "authors."),
 ],
 "exercises": [
   "Shoot the same scene at several ISO values with compensating shutter "
   "speeds. Confirm that the noise depends on the photon count rather than "
   "on the ISO setting.",
   "Open a raw file with <code>rawpy</code> and examine the array directly: "
   "the bit depth, the black level, the saturation point, and the CFA "
   "pattern.",
   "Plot a histogram of raw values for a scene and identify the black level "
   "and the clipping point.",
   "Photograph a uniform grey surface at several exposure levels and plot "
   "measured variance against mean. <b>The slope gives the gain and the "
   "intercept gives the read noise</b> — this is how noise models are "
   "calibrated.",
   "Confirm the &radic;N relationship from that plot and report the "
   "deviation.",
   "Average 4, 16, and 64 frames of a static scene and measure the noise "
   "reduction. Compare against the predicted &radic;n.",
   "Demonstrate why averaging must happen in linear space: average two "
   "very different exposures in linear and in gamma space and compare "
   "against ground truth.",
   "Take the same scene as raw and as JPEG, and attempt to correct a "
   "deliberate white balance error in both. Report what is recoverable.",
 ],
 "selfcheck": [
   "Trace the pipeline from scene radiance to a stored raw value.",
   "Where is the boundary between measurement and interpretation?",
   "What does each of aperture, shutter, and ISO change, and which affect "
   "photon count?",
   "Why does 'expose to the right' work?",
   "Give four differences between raw and JPEG content.",
   "Why does linearity matter, and what goes wrong when averaging encoded "
   "values?",
   "Why is shot noise &radic;N, and why can no sensor improvement remove "
   "it?",
   "How does SNR scale with frame count, and why?",
   "Why must denoising be applied in linear space?",
 ],
},

# =========================================================== MODULE 02 ======
{
 "n": 2,
 "title": "Image Processing Foundations",
 "subtitle": "The operations everything else is built from.",
 "question": "What are the primitives of image computation?",
 "outcomes": [
     "Implement convolution and explain separability.",
     "Explain the frequency-domain view and when it helps.",
     "Build and use Gaussian and Laplacian pyramids.",
     "Implement an edge-aware filter and explain why it is needed.",
     "Explain aliasing in images and how to avoid it.",
 ],
 "slides": [
  {"t": "section", "label": "Part 1", "title": "Convolution",
   "blurb": "The operation underneath nearly everything."},

  {"t": "eq", "kicker": "Definition", "title": "Convolution and its properties",
   "eqs": [
     ("(f * g)[x,y] = Σᵢ Σⱼ f[i,j] · g[x−i, y−j]",
      "Slide a kernel over the image, multiply, and sum. The whole "
      "operation."),
     ("f * g = g * f,   (f*g)*h = f*(g*h)",
      "Commutative and associative — so successive blurs compose into one "
      "kernel."),
     ("separable:  g(x,y) = gₓ(x) · g_y(y)",
      "A 2D Gaussian is the product of two 1D ones, so an n×n blur becomes "
      "two n-tap passes: O(n) instead of O(n²)."),
   ],
   "caption": "Separability is the difference between a 31×31 blur costing "
              "961 multiplies per pixel and costing 62.",
   "note": "Separability is the single most important practical fact in "
           "this module."},

  {"t": "table", "kicker": "Kernels", "title": "The standard kernels",
   "header": ["Kernel", "Does", "Note"],
   "widths": [2.8, 4.6, 4.7],
   "rows": [
     ["<b>Box</b>", "Uniform average", "<b>Cheap; ringing in frequency</b>"],
     ["<b>Gaussian</b>", "Weighted average", "<b>Separable; no ringing; the default</b>"],
     ["Sobel / Prewitt", "First derivative", "Edge magnitude and direction"],
     ["Laplacian", "Second derivative", "<b>Zero crossings are edges</b>"],
     ["<b>Laplacian of Gaussian</b>", "Blur then second derivative", "<b>Scale-selective edges</b>"],
     ["Unsharp mask", "image + k(image − blur)", "<b>Sharpening is adding back high frequencies</b>"],
   ],
   "footnote": "Unsharp masking is worth understanding: sharpening is not "
               "recovering detail, it is amplifying what survived.",
   "note": "The unsharp mask insight — sharpening amplifies rather than "
           "recovers — matters for Module 06."},

  {"t": "callout", "title": "The frequency view explains what filters do",
   "kind": "Why Fourier helps",
   "body": ["<b>Convolution in space is multiplication in frequency.</b> So "
            "a filter is a frequency response — it attenuates some "
            "frequencies and passes others.",
            "<b>A blur is a low-pass filter.</b> A Laplacian is a "
            "high-pass. Sharpening boosts high frequencies.",
            "<b>And a box filter's frequency response oscillates</b>, which "
            "is why box blur produces artefacts that Gaussian blur does "
            "not.",
            "<b>It also makes large convolutions cheap</b> — FFT, "
            "multiply, inverse FFT, at O(n log n) regardless of kernel "
            "size. Which is how Module 06's deconvolution works."]},

  {"t": "section", "label": "Part 2", "title": "Pyramids",
   "blurb": "The same image at many scales."},

  {"t": "two", "kicker": "Two pyramids", "title": "Gaussian and Laplacian",
   "lh": "Gaussian pyramid",
   "l": ["Repeatedly blur and downsample by 2.",
         "Each level is a lower-frequency version.",
         "<b>Blur before downsampling</b> or you alias (Part 3).",
         ("Used for coarse-to-fine search, mipmaps, scale-space.", 1)],
   "rh": "Laplacian pyramid",
   "r": ["Each level is the <b>difference</b> between a Gaussian level and "
         "the upsampled next one.",
         "<b>A band-pass decomposition</b> — each level holds one octave "
         "of detail.",
         "<b>Invertible</b> — sum the levels to recover the original.",
         ("Used for blending, compression, detail manipulation.", 1)],
   "note": "The invertibility of the Laplacian pyramid is what makes it "
           "useful for blending in Module 07."},

  {"t": "callout", "title": "Coarse-to-fine is the standard search strategy",
   "kind": "Why pyramids appear everywhere",
   "body": ["<b>Searching for an alignment at full resolution is expensive "
            "and gets stuck</b> in local optima.",
            "<b>Solve at the coarsest level first</b> — the search space "
            "is tiny and the function is smooth.",
            "<b>Then refine at each finer level</b>, using the previous "
            "answer as the starting point. Each refinement is a small local "
            "search.",
            "<b>This is how alignment (Module 07), optical flow, and stereo "
            "all work</b>, and it is one of the most reusable ideas in the "
            "course."]},

  {"t": "section", "label": "Part 3", "title": "Edge-aware filtering",
   "blurb": "Smoothing without destroying structure."},

  {"t": "callout", "title": "A Gaussian blur does not know what an edge is",
   "kind": "The problem",
   "body": ["<b>Gaussian weights depend only on distance.</b> A pixel ten "
            "pixels away contributes the same whether it is the same surface "
            "or a different object.",
            "<b>So blurring to remove noise also removes edges</b>, and "
            "there is no setting that separates them.",
            "<b>The bilateral filter adds a range term:</b> weight by "
            "distance <i>and</i> by similarity in value.",
            "<b>So pixels across an edge contribute little</b>, and the "
            "filter smooths within regions while preserving boundaries. One "
            "extra factor in the weight."]},

  {"t": "eq", "kicker": "Bilateral", "title": "Distance and similarity",
   "eqs": [
     ("w(p,q) = G_σs(‖p−q‖) · G_σr(|I(p)−I(q)|)",
      "Spatial Gaussian times range Gaussian. σs controls the "
      "neighbourhood; σr controls what counts as 'similar'."),
     ("output(p) = Σ w(p,q) I(q) / Σ w(p,q)",
      "A normalised weighted average, as always. Only the weights have "
      "changed."),
   ],
   "caption": "The range term makes it non-linear and "
              "signal-dependent — which is why it cannot be done with an "
              "FFT and why fast approximations exist.",
   "note": "Emphasise that it is still just a weighted average. The "
           "conceptual step is small."},

  {"t": "bullets", "kicker": "Variants", "title": "The edge-aware family",
   "items": [
     "<b>Bilateral filter.</b> The original. Slow naively; fast "
     "approximations use a bilateral grid.",
     "",
     "<b>Joint/cross bilateral:</b> take the range weights from a "
     "<i>different</i> image. Powerful — filter a noisy image using a "
     "clean flash image's edges.",
     "",
     "<b>Guided filter:</b> faster, linear-time, and often better "
     "behaved. The usual modern choice.",
     "",
     "<b>Anisotropic diffusion:</b> the PDE formulation of the same idea.",
     "",
     "<b>Base/detail decomposition</b> — filter, then divide — is the "
     "foundation of local tone mapping (Module 04).",
   ],
   "note": "Joint bilateral is the one with the most surprising "
           "applications and is worth a demo."},

  {"t": "callout", "title": "Aliasing: blur before you downsample",
   "kind": "The rule people break",
   "body": ["<b>Downsampling without filtering first folds high "
            "frequencies into low ones</b> — the same Nyquist argument as "
            "CSCE 641 Module 09.",
            "<b>The symptom is moiré</b> on fine repeating detail, and "
            "jagged edges that shimmer when the image moves.",
            "<b>So always low-pass before decimating</b>, with a cutoff "
            "matched to the new sampling rate.",
            "<b>And it applies to raw sensor data too</b> — which is why "
            "cameras have optical low-pass filters, and why removing them "
            "trades sharpness for moiré."]},
 ],
 "takeaways": [
   "Convolution is a sliding weighted sum; separability turns an "
   "n&times;n kernel into two n-tap passes and is the key practical fact.",
   "Convolution in space is multiplication in frequency, which explains what "
   "each filter does and makes large kernels cheap via FFT.",
   "Sharpening by unsharp masking amplifies surviving high frequencies — "
   "it does not recover lost detail.",
   "A Gaussian pyramid is a multi-scale low-pass sequence; a Laplacian "
   "pyramid is an invertible band-pass decomposition.",
   "Coarse-to-fine search over a pyramid is how alignment, optical flow, and "
   "stereo all avoid local optima.",
   "The bilateral filter weights by spatial distance and value similarity, "
   "so it smooths within regions and preserves edges.",
 ],
 "notes": [
  ("h1", "1 &nbsp; Convolution"),
  ("eq", "(f * g)[x,y] = &Sigma;<sub>i</sub> &Sigma;<sub>j</sub> "
         "f[i,j] &middot; g[x&minus;i, y&minus;j]"),
  ("p", "Slide a kernel over the image, multiply element-wise, and sum. "
        "Nearly every operation in this course is either a convolution or "
        "built from several."),
  ("table", ["Property", "Statement", "Why it matters"],
   [["<b>Commutative, associative</b>", "f*g = g*f and (f*g)*h = f*(g*h).",
     "Successive blurs compose into a single equivalent kernel, so a chain "
     "of filters can be collapsed."],
    ["<b>Separability</b>",
     "If g(x,y) = g<sub>x</sub>(x)&middot;g<sub>y</sub>(y), the 2D "
     "convolution is two 1D convolutions.",
     "<b>An n&times;n kernel costs n&#178; multiplies per pixel; two "
     "n-tap passes cost 2n.</b> For a 31&times;31 Gaussian that is 961 "
     "against 62 — a factor of fifteen. <b>The single most important "
     "practical fact in this module.</b>"],
    ["<b>Linearity</b>", "f*(ag + bh) = a(f*g) + b(f*h).",
     "Filters can be combined and decomposed algebraically."]],
   [0.21, 0.37, 0.42]),
  ("table", ["Kernel", "Effect", "Notes"],
   [["<b>Box</b>", "Uniform average over a window.",
     "Cheapest, and its frequency response oscillates — which produces "
     "visible artefacts on structured content."],
    ["<b>Gaussian</b>", "Distance-weighted average.",
     "<b>Separable, no ringing, and the only kernel whose repeated "
     "application stays Gaussian.</b> The default for good reason."],
    ["<b>Sobel, Prewitt</b>", "Approximate first derivative.",
     "Gradient magnitude gives edge strength and the ratio gives "
     "direction."],
    ["<b>Laplacian</b>", "Approximate second derivative.",
     "Zero crossings mark edges. Sensitive to noise, hence the next row."],
    ["<b>Laplacian of Gaussian</b>", "Blur, then second derivative.",
     "<b>Scale-selective</b> — the Gaussian's width selects which "
     "scale of edge is detected. The basis of blob detection."],
    ["<b>Unsharp mask</b>", "image + k&middot;(image &minus; blur).",
     "<b>Sharpening is adding back high frequencies that survived, not "
     "recovering detail that was lost.</b> Worth internalising before "
     "Module 06, where the distinction between amplification and recovery "
     "becomes the whole subject."]],
   [0.21, 0.30, 0.49]),
  ("callout", "The frequency-domain view",
   ["<b>Convolution in the spatial domain is multiplication in the frequency "
    "domain.</b> So every filter can be described by a frequency "
    "response — what it does to each spatial frequency.",
    "<b>This makes filter behaviour predictable.</b> A Gaussian blur is a "
    "low-pass filter with a smooth rolloff. A Laplacian is a high-pass. "
    "Unsharp masking boosts high frequencies. These are statements about the "
    "response rather than metaphors.",
    "<b>And it explains the box filter's artefacts.</b> A box in space is a "
    "sinc in frequency, which oscillates and has negative lobes — so a "
    "box blur does not monotonically attenuate high frequencies and can "
    "<i>amplify</i> some of them. This is why box blur looks wrong on "
    "structured content and Gaussian blur does not.",
    "<b>It also makes large convolutions cheap:</b> forward FFT, multiply, "
    "inverse FFT, at O(n log n) in the image size and independent of kernel "
    "size. <b>This is how the deconvolution of Module 06 is computed</b>, "
    "and it is why a 200-pixel-wide blur kernel is no more expensive than a "
    "5-pixel one."]),

  ("h1", "2 &nbsp; Pyramids"),
  ("table", ["", "Gaussian pyramid", "Laplacian pyramid"],
   [["Construction", "Repeatedly blur and downsample by a factor of two.",
     "Each level is the difference between a Gaussian level and the "
     "upsampled version of the next coarser one."],
    ["Each level is", "A successively lower-frequency version of the "
     "image.",
     "<b>One octave of spatial frequency</b> — a band-pass "
     "decomposition."],
    ["Invertible?", "No — information is discarded at each level.",
     "<b>Yes.</b> Summing the levels (with the coarsest residual) recovers "
     "the original exactly, which is what makes it useful for blending "
     "(Module 07)."],
    ["Used for", "Coarse-to-fine search, mipmaps, scale-space analysis.",
     "Blending, compression, and detail manipulation — amplifying one "
     "band sharpens at that scale only."]],
   [0.15, 0.40, 0.45]),
  ("p", "<b>Blur before downsampling</b>, always, or the result aliases "
        "(&sect;3). This is the most common pyramid bug and it produces "
        "artefacts that persist through every subsequent level."),
  ("callout", "Coarse-to-fine is the standard search strategy",
   ["<b>Searching for an alignment, a flow field, or a disparity at full "
    "resolution is both expensive and prone to local optima</b> — the "
    "objective function has many shallow minima from repeated texture.",
    "<b>Solve at the coarsest pyramid level first.</b> The image is small, "
    "so the search space is tiny; and the aggressive blurring has removed "
    "the high-frequency structure that created the spurious minima, so the "
    "objective is smooth and the global optimum is easy to find.",
    "<b>Then refine at each successively finer level</b>, using the previous "
    "level's answer (scaled up) as the starting point. Each refinement is a "
    "small local search in a neighbourhood already known to be correct.",
    "<b>This is how image alignment (Module 07), optical flow, and stereo "
    "matching all work</b>, and it is among the most reusable ideas in the "
    "course — it appears any time a search over a large displacement "
    "is needed."]),

  ("break",),
  ("h1", "3 &nbsp; Edge-aware filtering"),
  ("callout", "A Gaussian blur does not know what an edge is",
   ["<b>Gaussian weights depend only on spatial distance.</b> A pixel ten "
    "pixels away contributes the same amount whether it belongs to the same "
    "surface or to a completely different object across a strong boundary.",
    "<b>So blurring to suppress noise necessarily blurs edges too</b>, and "
    "no choice of &sigma; separates the two — noise and edges occupy "
    "overlapping frequency bands.",
    "<b>The bilateral filter adds a second factor to the weight:</b> "
    "similarity in <i>value</i> as well as proximity in <i>space</i>. Pixels "
    "that are nearby and similar in intensity contribute strongly; pixels "
    "that are nearby but very different contribute almost nothing.",
    "<b>So contributions do not cross strong edges</b>, and the filter "
    "smooths within regions while leaving boundaries intact. <b>The "
    "conceptual step is small</b> — it is still a normalised weighted "
    "average, with one extra term in the weight — and the consequences "
    "are large."]),
  ("eq", "w(p,q) = G<sub>&sigma;s</sub>(&#8214;p&minus;q&#8214;) &middot; "
         "G<sub>&sigma;r</sub>(|I(p)&minus;I(q)|)"),
  ("p", "where &sigma;<sub>s</sub> sets the spatial neighbourhood and "
        "&sigma;<sub>r</sub> sets what counts as similar in value. <b>The "
        "range term makes the filter non-linear and signal-dependent</b>, "
        "which means it cannot be evaluated with an FFT and a naive "
        "implementation is slow — hence the fast approximations below."),
  ("ul", ["<b>Bilateral filter.</b> The original formulation. Naively "
          "O(window size) per pixel; the <b>bilateral grid</b> and related "
          "techniques make it fast by treating it as a linear operation in a "
          "higher-dimensional space.",
          "<b>Joint (cross) bilateral filter.</b> Take the <i>range</i> "
          "weights from a different image than the one being filtered. "
          "<b>This is more powerful than it sounds:</b> a noisy ambient-light "
          "photograph can be filtered using the edges from a clean flash "
          "photograph of the same scene, giving noise reduction that "
          "preserves detail the noisy image alone could not have supported.",
          "<b>Guided filter.</b> Linear time regardless of window size, "
          "often better behaved near edges than the bilateral filter, and "
          "the usual modern choice. Also accepts a separate guide image.",
          "<b>Anisotropic diffusion.</b> The partial differential equation "
          "formulation of the same idea — diffuse heat through the "
          "image, with conductivity reduced across edges.",
          "<b>Base/detail decomposition.</b> Edge-aware filter to get a "
          "'base' layer, divide the original by it to get a 'detail' layer, "
          "and then process the two differently. <b>This is the foundation "
          "of local tone mapping</b> (Module 04) and of a great deal of "
          "photographic retouching."]),
  ("callout", "Blur before you downsample",
   ["<b>Downsampling without first low-pass filtering folds high "
    "frequencies down into low ones</b> — the same Nyquist argument as "
    "CSCE 641 Module 09, arriving from the image-processing side.",
    "<b>The symptoms are moir&eacute; patterns</b> on fine repeating detail "
    "— fabric, brickwork, distant fences — <b>and jagged edges</b> "
    "that shimmer distractingly when the image or the camera moves.",
    "<b>So always low-pass before decimating</b>, with the cutoff matched to "
    "the new sampling rate. Halving the resolution means removing everything "
    "above half the original Nyquist frequency first.",
    "<b>And this applies to the sensor itself.</b> The colour filter array "
    "samples the image, so scene detail finer than the pixel pitch aliases. "
    "<b>This is why cameras have historically included an optical low-pass "
    "filter in front of the sensor</b>, and why removing it — as many "
    "modern cameras do — is a deliberate trade of sharpness against "
    "moir&eacute;."]),
 ],
 "resources": [
   ("Szeliski &mdash; Computer Vision, Chapter 3 (free)",
    "https://szeliski.org/Book/",
    "Linear filtering, pyramids, and edge-aware filters, with the frequency "
    "analysis. The reference for this module."),
   ("CMU 15-463 &mdash; image processing and pyramids lectures (free)",
    "http://graphics.cs.cmu.edu/courses/15-463/",
    "Convolution, pyramids, and the assignment that builds them."),
   ("Paris et al. &mdash; Bilateral Filtering: Theory and Applications "
    "(free)",
    "https://people.csail.mit.edu/sparis/publi/2009/fntcgv/",
    "The definitive survey of &sect;3, including the fast approximations "
    "and the joint bilateral applications."),
   ("He, Sun & Tang &mdash; Guided Image Filtering (free)",
    "https://web.archive.org/web/20231129221257/https://kaiminghe.github.io/eccv10/",
    "The guided filter. Short paper, linear time, and a few lines of code."),
 ],
 "exercises": [
   "Implement 2D convolution directly and with a separable pass. Verify they "
   "agree and report the speedup for kernel sizes from 3 to 51.",
   "Implement convolution via FFT and find the kernel size at which it "
   "overtakes the direct separable method.",
   "Plot the frequency response of a box filter and a Gaussian of the same "
   "width. Identify the box filter's negative lobes.",
   "Apply both to an image of a brick wall and explain the difference from "
   "the frequency plots.",
   "Implement unsharp masking and demonstrate that it cannot recover detail "
   "that has been blurred away — blur an image, sharpen it, and compare "
   "against the original.",
   "Build Gaussian and Laplacian pyramids. Reconstruct the image from the "
   "Laplacian pyramid and confirm the error is at floating-point level.",
   "Downsample an image with and without pre-blurring. Photograph or render "
   "something with fine repeating detail to make the aliasing obvious.",
   "Implement the bilateral filter. Compare against a Gaussian of the same "
   "spatial &sigma; on a noisy image with strong edges.",
   "Implement a joint bilateral filter and use a flash image to denoise a "
   "no-flash image of the same scene.",
   "Implement base/detail decomposition and amplify the detail layer. This "
   "is the core of local tone mapping and of most 'clarity' sliders.",
 ],
 "selfcheck": [
   "Write the convolution sum and state three properties.",
   "What is separability and what does it save for a 31&times;31 kernel?",
   "What does convolution correspond to in the frequency domain, and what "
   "does that explain?",
   "Why does a box filter produce artefacts a Gaussian does not?",
   "Why is sharpening not detail recovery?",
   "Distinguish Gaussian and Laplacian pyramids, and say which is "
   "invertible.",
   "Describe coarse-to-fine search and say what problem it solves.",
   "Why can a Gaussian blur not preserve edges, and what does the bilateral "
   "filter add?",
   "Name four edge-aware filters and one application of the joint bilateral "
   "filter.",
   "Why must you blur before downsampling, and what does that have to do "
   "with optical low-pass filters?",
 ],
},

]

# --- additional module batches ----------------------------------------------
for _b in ("c748_b2", "c748_b3"):
    try:
        MODULES += __import__(_b).MODULES
    except ImportError:
        pass
MODULES.sort(key=lambda m: m["n"])
